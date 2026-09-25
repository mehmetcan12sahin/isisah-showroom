<?php
/**
 * teklif.php — ISIŞAH GROUP teklif formu sunucu tarafı işleyicisi (self-host, PHP mail()).
 *
 * DEĞİL: Bu dosya deploy-ftp.sh tarafından yüklenmez (script yalnız kök *.html + showroom/ tarar).
 * Bu dosya YEREL OLARAK TEST EDİLMEMİŞTİR — bu ortamda PHP çalıştırılabilir değil (bkz. server/README.md).
 * Devreye almadan önce README.md'deki adımları TAMAMEN uygula.
 *
 * Tasarım kararları (brief §10, HANDOFF 2. Dalga, audit F2):
 *  - Formspree/reCAPTCHA YOK — self-host, üçüncü taraf sıfır.
 *  - Sadece POST + JSON yanıt. Başarı SADECE mail() true dönerse {ok:true}.
 *  - Bal küpü + minimum doldurma süresi + IP-hash tabanlı dosya rate limit + CRLF/header injection koruması.
 *  - From: adresi SABİT (kullanıcı girdisiyle asla belirlenmez) — spoofing/injection yüzeyi kapalı.
 *  - Kişisel veri hiçbir zaman loglanmaz (rate limit dosyasına sadece hash + sayaç yazılır).
 */

declare(strict_types=1);

// ================= AYAR SABİTLERİ (devreye almadan önce doldur/gözden geçir) =================
// Alıcı e-posta — İŞLETME ONAYLI kutuyla değiştir (bkz. data_needed: ayrı satış/teknik kutusu mu, info@ mi?).
const RECIPIENT = 'info@isisah.com.tr';

// mail() From: adresi — barındırmanın kabul ettiği, alan adına ait bir gönderen olmalı (Plesk/SPF uyumlu).
// PLACEholder: gerçek göndermeden önce Plesk panelinden bu adresin var/yetkili olduğunu doğrula.
const FROM_ADDRESS = 'teklif-formu@isisah.com.tr';

// Tarayıcıdan fetch ile POST edilebilecek kaynaklar (virgülle ayrılmış, şema+host, sonda / yok).
// isisah.com.tr (ana site) + mehmetcan12sahin.github.io (github.io aynası — HANDOFF: action/endpoint MUTLAK URL
// olduğu için ayna da bu PHP'ye cross-origin istek atabilmeli). Origin göndermeyen aynı-origin istekler
// (tarayıcı bazen göndermez) engellenmez; sadece YANLIŞ bir Origin geldiğinde reddedilir.
const ALLOWED_ORIGIN = 'https://isisah.com.tr,https://mehmetcan12sahin.github.io';

// Rate limit dosyalarının yazılacağı dizin. Boş bırakılırsa sys_get_temp_dir() kullanılır.
// Plesk'te kalıcılık istenirse örn. '/var/www/vhosts/isisah.com.tr/private/teklif-ratelimit' gibi
// httpdocs DIŞINDA, web'den erişilemez bir dizin ver (sabit dizin webroot içinde OLMAMALI).
const RATE_LIMIT_DIR = '';

// Aynı IP-hash için izin verilen istek sayısı / pencere (saniye).
const RATE_LIMIT_MAX = 5;
const RATE_LIMIT_WINDOW = 3600;

// Bal küpü doldurulmuşsa VEYA t_start'tan bu yana geçen süre bundan azsa spam say (ms).
const MIN_FILL_MS = 4000;

// Alan uzunluk sınırları (istemci tarafındaki maxlength'lerle eşleşir, bkz. tools/build-teklif.py).
const MAX_LEN = [
    'firma' => 120, 'ad_soyad' => 120, 'eposta' => 160, 'telefon' => 32,
    'urun_konu' => 160, 'adet' => 60, 'aciklama' => 2000,
];

// ================= YARDIMCI FONKSİYONLAR =================

// (Dönüş tipi bilerek belirtilmedi: 'never' PHP 8.1+ ister, hedef barındırmanın PHP sürümü teyit edilmedi.)
function json_out(int $status, array $body) {
    http_response_code($status);
    header('Content-Type: application/json; charset=UTF-8');
    echo json_encode($body, JSON_UNESCAPED_UNICODE);
    exit;
}

/** CRLF/header-injection koruması: satır sonlarını boşluğa çevirir, baş/son boşluğu kırpar. */
function clean_field(string $v): string {
    $v = preg_replace('/[\r\n]+/', ' ', $v);
    return trim($v ?? '');
}

function client_ip(): string {
    // Yalnız REMOTE_ADDR güvenilir (X-Forwarded-For istemci tarafından sahtelenebilir; ters proxy
    // varsa ve doğru yapılandırılmışsa Plesk/nginx REMOTE_ADDR'ı doğru ayarlar — burada güvene alınmaz).
    return $_SERVER['REMOTE_ADDR'] ?? '0.0.0.0';
}

function rate_limit_dir(): string {
    $d = RATE_LIMIT_DIR !== '' ? RATE_LIMIT_DIR : sys_get_temp_dir();
    if (!is_dir($d)) { @mkdir($d, 0700, true); }
    return rtrim($d, '/');
}

/** IP'yi HİÇBİR ZAMAN düz metin saklamaz — sadece sabit-uzunluklu hash. Kişisel veri değildir. */
function ip_hash(string $ip): string {
    return hash('sha256', 'isisah-teklif-v1|' . $ip);
}

/**
 * Dosya tabanlı sabit-pencere rate limit. Döner: true = izinli, false = limit aşıldı.
 * Kilitleme (flock) ile eşzamanlı isteklerde yarış durumunu önler. Dosyada SADECE hash + sayaç + pencere
 * başlangıcı tutulur — kişisel veri yok.
 */
function rate_limit_check(string $hash): bool {
    $path = rate_limit_dir() . '/teklif-rl-' . $hash . '.json';
    $fh = @fopen($path, 'c+');
    if ($fh === false) return true; // dosya sistemi yazılamıyorsa formu tıkama — sessizce izin ver
    $ok = true;
    if (flock($fh, LOCK_EX)) {
        $raw = stream_get_contents($fh);
        $data = $raw ? json_decode($raw, true) : null;
        $now = time();
        if (!is_array($data) || !isset($data['start']) || ($now - (int)$data['start']) > RATE_LIMIT_WINDOW) {
            $data = ['start' => $now, 'count' => 0];
        }
        $data['count'] = (int)$data['count'] + 1;
        $ok = $data['count'] <= RATE_LIMIT_MAX;
        ftruncate($fh, 0);
        rewind($fh);
        fwrite($fh, json_encode($data));
        fflush($fh);
        flock($fh, LOCK_UN);
    }
    fclose($fh);
    return $ok;
}

function is_valid_email(string $v): bool {
    return $v !== '' && filter_var($v, FILTER_VALIDATE_EMAIL) !== false;
}

function allowed_origins(): array {
    return array_map('trim', explode(',', ALLOWED_ORIGIN));
}

/** Origin başlığı VARSA ve izin listesinde değilse reddet; Origin YOKSA (bazı aynı-origin istekler) engellemez. */
function origin_ok(): bool {
    $origin = $_SERVER['HTTP_ORIGIN'] ?? '';
    if ($origin === '') return true;
    return in_array($origin, allowed_origins(), true);
}

function send_cors_headers(): void {
    $origin = $_SERVER['HTTP_ORIGIN'] ?? '';
    if ($origin !== '' && in_array($origin, allowed_origins(), true)) {
        header('Access-Control-Allow-Origin: ' . $origin);
        header('Vary: Origin');
    }
    header('Access-Control-Allow-Methods: POST, OPTIONS');
    header('Access-Control-Allow-Headers: Content-Type');
}

// ================= İSTEK İŞLEME =================

send_cors_headers();

if (($_SERVER['REQUEST_METHOD'] ?? '') === 'OPTIONS') {
    // CORS ön-uçuş isteği — gövde yok, sadece başlıklar.
    http_response_code(204);
    exit;
}

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    json_out(405, ['ok' => false, 'error' => 'method_not_allowed']);
}

if (!origin_ok()) {
    json_out(403, ['ok' => false, 'error' => 'origin_not_allowed']);
}

// Gövdeyi oku: JSON veya klasik form-encoded (X-www-form-urlencoded) — ikisi de kabul edilir.
$contentType = $_SERVER['CONTENT_TYPE'] ?? '';
$input = [];
if (stripos($contentType, 'application/json') !== false) {
    $raw = file_get_contents('php://input');
    $decoded = json_decode($raw ?: '', true);
    if (is_array($decoded)) $input = $decoded;
} else {
    $input = $_POST;
}

$get = static function (array $arr, string $key): string {
    $v = $arr[$key] ?? '';
    return is_string($v) ? $v : '';
};

$firma     = clean_field($get($input, 'firma'));
$adSoyad   = clean_field($get($input, 'ad_soyad'));
$eposta    = clean_field($get($input, 'eposta'));
$telefon   = clean_field($get($input, 'telefon'));
$urunKonu  = clean_field($get($input, 'urun_konu'));
$adet      = clean_field($get($input, 'adet'));
$aciklama  = clean_field($get($input, 'aciklama'));
$hpWeb     = trim($get($input, 'hp_web'));
$tStartRaw = $get($input, 't_start');

// ---- Bal küpü + minimum doldurma süresi (bot tespiti; bilgi vermeden reddet) ----
if ($hpWeb !== '') {
    json_out(400, ['ok' => false, 'error' => 'invalid']);
}
$tStart = ctype_digit($tStartRaw) ? (int)$tStartRaw : 0;
$elapsedMs = $tStart > 0 ? (int)(microtime(true) * 1000) - $tStart : -1;
if ($tStart <= 0 || $elapsedMs < MIN_FILL_MS) {
    json_out(400, ['ok' => false, 'error' => 'invalid']);
}

// ---- Rate limit (kişisel veri yok — sadece IP hash) ----
if (!rate_limit_check(ip_hash(client_ip()))) {
    json_out(429, ['ok' => false, 'error' => 'rate_limited']);
}

// ---- Doğrulama ----
$errors = [];
if ($adSoyad === '' || mb_strlen($adSoyad) > MAX_LEN['ad_soyad']) $errors[] = 'ad_soyad';
if ($firma !== '' && mb_strlen($firma) > MAX_LEN['firma']) $errors[] = 'firma';
if ($eposta !== '' && (mb_strlen($eposta) > MAX_LEN['eposta'] || !is_valid_email($eposta))) $errors[] = 'eposta';
if ($telefon !== '' && (mb_strlen($telefon) > MAX_LEN['telefon'] || !preg_match('/^[0-9 ()+.\-]{7,32}$/', $telefon))) $errors[] = 'telefon';
if ($eposta === '' && $telefon === '') $errors[] = 'contact';
if ($urunKonu !== '' && mb_strlen($urunKonu) > MAX_LEN['urun_konu']) $errors[] = 'urun_konu';
if ($adet !== '' && mb_strlen($adet) > MAX_LEN['adet']) $errors[] = 'adet';
if ($aciklama === '' || mb_strlen($aciklama) > MAX_LEN['aciklama']) $errors[] = 'aciklama';

if (!empty($errors)) {
    json_out(400, ['ok' => false, 'error' => 'validation', 'fields' => $errors]);
}

// ---- E-posta oluştur ----
$subject = 'Teklif Talebi — ' . ($urunKonu !== '' ? $urunKonu : 'Genel');
$subjectEncoded = mb_encode_mimeheader($subject, 'UTF-8', 'B', "\n");

$bodyRows = [
    'Firma' => $firma,
    'Ad Soyad' => $adSoyad,
    'E-posta' => $eposta,
    'Telefon' => $telefon,
    'Ürün/Konu' => $urunKonu,
    'Adet/Miktar' => $adet,
];
$lines = [];
foreach ($bodyRows as $label => $val) {
    if ($val !== '') $lines[] = $label . ': ' . $val;
}
$lines[] = '';
$lines[] = 'İhtiyaç açıklaması:';
$lines[] = $aciklama;
$body = implode("\r\n", $lines);

$headers = [];
$headers[] = 'From: ISIŞAH GROUP Teklif Formu <' . FROM_ADDRESS . '>';
if (is_valid_email($eposta)) {
    $headers[] = 'Reply-To: ' . $eposta;
}
$headers[] = 'Content-Type: text/plain; charset=UTF-8';
$headers[] = 'Content-Transfer-Encoding: 8bit';
$headers[] = 'X-Mailer: ISISAH-Teklif-Formu/1.0';

$sent = @mail(RECIPIENT, $subjectEncoded, $body, implode("\r\n", $headers));

if ($sent) {
    json_out(200, ['ok' => true]);
}
json_out(500, ['ok' => false, 'error' => 'mail_failed']);
