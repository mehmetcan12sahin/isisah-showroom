# isisah.com.tr SEO Denetimi — 8 Eylül 2026 (7 uzman ajan, 2. tur)

Kaynak: Workflow wf_c371d90a-66f. Canlı durum dış kaynaklardan (r.jina.ai, hackertarget, check-host) doğrulandı; ofis IP 443/21 engelli. Not: Bu turda "sprint-1 canlıda yok" tespiti doğrudur — deploy IP engeli yüzünden bekliyor.


## teknik-2
**Skor:** Teknik SEO 54/100 (benim değerlendirmem; canlı durum 8 Eyl 2026 12:09 TRT, dış kaynaklardan doğrulandı — ofis IP'si 443'te engelli). Lighthouse SEO=100 yanıltıcı: 5 çekirdek URL indekslenebilir ve canonical/og/lang/viewport tutarlı, ama 36 ürünün HİÇBİRİ HTML'de yok, 10 kategori "sayfası" yalnızca hash-fragment (Google için tek URL), 404 sayfası eski WP teması (PHP 5.6.40), favicon kare değil + /favicon.ico 0 bayt, güvenlik/cache başlıkları sıfır, showroom sayfaları ana sayfanın KOPYASINA link veriyor. Ayrıca: repodaki "SEO sprint-1" (cd3b9b9, 11:59) canlıya YANSIMAMIŞ — canlı index Last-Modified hâlâ 7 Eyl 11:15 GMT.


### Kritik
- [DEPLOY DOĞRULA] Sprint-1 canlıda YOK: hackertarget 12:09 TRT → https://isisah.com.tr/ Last-Modified 'Mon, 07 Sep 2026 11:15:38 GMT'; r.jina.ai robots.txt → 'Sitemap:' satırı yok; r.jina.ai /showroom/fabrika.html → title 'Fabrika Turu — ISIŞAH GROUP', H1=0. Repo HEAD cd3b9b9 (11:59) bunları düzeltiyor, docs/seo-baseline-2026-09-07.md son satır 'Sprint-1 yayına alındı' diyor ama canlıyla ÇELİŞİYOR — deploy-ftp.sh muhtemelen ofis IP engeli (85.97.200.122; ftp.isisah.com.tr aynı sunucu) yüzünden tamamlanmadı ve duman testi bağlanamadığı için yakalayamadı. Düzeltme: başka ağdan (hotspot / Tailscale kutu) `bash tools/deploy-ftp.sh`, ardından dış doğrulama: `curl -s https://r.jina.ai/https://isisah.com.tr/robots.txt | grep Sitemap`.
- JS render: /showroom/urunler.html — 36 ürün adı YALNIZCA <script> içinde (urunler.html:393-473 PRODUCTS/SALMEX_LIST/BORSAH_LIST). Script dışı HTML'de 'Kanal Tipi Isıtıcı' 0, 'Isıtıcı' 0, 'BOYKUR' 0, 'Ray' 0 kez; görünür metin 133 kelime; Jina render'ı da ürün adlarını görmüyor. JSON-LD ItemList 36 eleman var ama `url` 36/36 BOŞ → Google'ın bağlayacağı sayfa yok. Düzeltme: (a) urunler.html .sublobby altına JS'siz görünür ürün listesi <ul class='srlist'> (36 <li><a href='/urunler/<slug>.html'>), (b) ItemList her elemana url, (c) statik landing'ler (orta vade #1).
- Hash-fragment URL'leri Google'a görünmez: index.html'de 28 link `/showroom/urunler.html#hol=…` (salmex 9, borsah 5, isisah_agir 4, isisah_savunma 3, isisah_rayli 2, isisah_otomotiv 2, isisah_rezistans/hvac/beyaz 1) — repo index.html:783-795 (.vcard) + marka kartları; vizyon-misyon.html 3 link `index.html#marka=…`. urunler.html:523 `location.hash.match(/^#hol=([a-z_]+)$/)` yalnız istemcide çözülür. Sonuç: 8 ISIŞAH gamı + SALMEX + BORŞAH = 10 'kategori sayfası' Google'da TEK URL; kategori sorgusu 0 gösterimin teknik kökü bu. Düzeltme: /urunler/<slug>.html 10 statik landing (hazir_kod G), index'teki 28 href landing'e, landing sonunda '3B holde gez →' hash CTA korunur.
- İç link grafı — showroom sayfaları ana sayfanın KOPYASINA link veriyor: urunler.html:296 ve :303 `href="index.html"`, fabrika.html:106 ve :110 `href="index.html"` → canlıda /showroom/index.html (kopya) olarak çözülür, kök / değil (4 iç link canonical olmayan sayfaya). Ayrıca yetim kopyalar: /showroom/hakkimizda.html 200 (51783 B, 12:09), /showroom/vizyon-misyon.html, /showroom/index.html — kaynak deploy-ftp.sh:10 `PAGES=sorted(glob.glob('*.html'))` tüm kök sayfaları showroom/'a da yüklüyor; hiçbir sayfadan link almıyor (canonical köke işaret ettiği için zarar sınırlı ama tarama bütçesi + GSC 'kopya' uyarısı). Düzeltme: deploy-ftp.sh yaması (hazir_kod D) + nginx 301 (hazir_kod C, kullanıcı kararı).
- 404 davranışı: /olmayan-sayfa ve /showroom/olmayan-sayfa.html → HTTP 404 (kod DOĞRU, soft-404 yok) ama gövde ESKİ WP TEMASI: title 'Sayfa bulunamadı – ISIŞAH ENDÜSTRİ', H1 'Hata 404 - sayfa bulunamadı', eski nav + arama kutusu + 'popüler yazılar'. Başlıklar: `X-Powered-By: PHP/5.6.40` (EOL Ocak 2019), `Set-Cookie: PHPSESSID` (404'te çerez, banner yok — KVKK), `Link: rel="https://api.w.org/"` (WP REST). Düzeltme: httpdocs/404.html statik (hazir_kod F) + nginx `error_page 404 /404.html;` (WP dosyasına dokunmadan). PHP 5.6→7.4+/8.x barındırıcıda [ONAY — WP 4.8 uyumluluk testi şart].
- HTTP başlıkları (HTML + statik, hepsi eksik): Cache-Control YOK (logo-isisah.webp 35258 B, three.module.min.js 655K her ziyarette yeniden doğrulanıyor), Strict-Transport-Security yok, X-Content-Type-Options yok, Referrer-Policy yok, Permissions-Policy yok, CSP yok, `X-Powered-By: PleskLin` sızıntısı, `Content-Type: text/html` charset'siz, http://isisah.com.tr/ → 200 (301 yok, 76631 B tam sayfa). Düzeltme: Plesk > Apache & nginx Ayarları > Ek nginx yönergeleri (hazir_kod C — kullanıcı kararı).

### Hızlı kazanımlar
- Favicon: index.html:31 / hakkimizda.html:19 / vizyon-misyon.html:19 `<link rel="icon" href="assets/img/logo.png">` → 340×105 (kare DEĞİL); urunler.html:28 / fabrika.html:10 `assets/catalog/logo-group.png` 300×120 (kare değil). /favicon.ico → 200 ama Content-Length: 0 (BOŞ, PHP servis ediyor); /apple-touch-icon.png → 404. Google SERP favicon şartı: kare, 48px katı. Düzeltme: logo-group'tan kare kırpım → assets/img/favicon.svg, favicon-48.png, favicon-192.png, apple-touch-icon.png (180) + kök favicon.ico (32/48 çoklu) + hazir_kod A link seti; deploy-ftp.sh'a favicon.ico kök yüklemesi ekle.
- Sosyal meta eksikleri (5 sayfa): twitter:title/description/image 0 adet (yalnız twitter:card), og:locale yok, og:image:alt yok; fabrika.html canlıda og:* ve JSON-LD HİÇ yok (repo VideoObject ekledi, yayınlanmadı). index.html:11 og:title 'ISIŞAH ENDÜSTRİYEL — Isının gücü…' ve urunler.html:11 og:title '3B Ürün Showroom' anahtar kelimesiz — yeni title'larla hizala. Set: hazir_kod A/B; tools/build-pages.py:107-114 şablonuna da ekle.
- urunler.html:785 künye `<img class="blogo" src="assets/catalog/${d.logo}.webp" alt="">` → `alt="${d.tag} logosu"`. (Kapı kartı logoları :320/:325/:330 alt="" aria-hidden — DOĞRU, buton aria-label var, dokunma.) Diğer 4 sayfada boş/eksik alt: 0 (index 35/35 dolu).
- sitemap.xml:6-7 lastmod urunler 2026-08-25 / fabrika 2026-08-29 ama dosyalar 8 Eyl'de değişti (title/H1/JSON-LD) → 2026-09-08 yap; yanlış lastmod Google'ın sitemap güvenini düşürür. Deploy ile birlikte gönder.
- Anchor metni: index.html'de 14× 'Showroom'da Gör →' aynı generic metin 9 farklı #hol= hedefine (#urunler kartları .card). Kart başlığını anchor'a taşı ('Paslanmaz boruları showroom'da gör →'). Landing'ler gelince zorunlu olur.
- urunler.html → fabrika.html'e 0 iç link (fabrika yalnız index/hakkimizda/vizyon'dan 2'şer). urunler.html SALMEX holü outro'suna (:350 civarı 'Yolun sonu' bloğu) `<a href="fabrika.html">SALMEX fabrika turu →</a>`.
- index.html JSON-LD sameAs içinde 'https://isisah.com.tr' (kendi URL'si — anlamsız, kaldır); LinkedIn `/in/isi%C5%9Fah-group-9b45aa125/` kişisel profil → şirket sayfası bekleniyor (HANDOFF). Organization'a `foundingDate` var ✓; `numberOfEmployees`/ciro YAZMA [ONAY].
- Hreflang: tek dil (tr), hreflang YOK — bu DOĞRU; EN olmadan ekleme. EN çıkınca 3 satır: `<link rel="alternate" hreflang="tr" href=…>` + `en` + `x-default` (her iki sayfada karşılıklı). lang="tr" 5/5 ✓, viewport 5/5 ✓, meta robots yok (varsayılan index,follow — sorun değil; hazir_kod'da max-image-preview:large eklendi).
- Title uzunlukları (canlı): index 88, urunler 81 karakter (SERP'te ~60'ta kesilir) — repo sprint-1 title'ları index 87 / urunler 90 karakter, yine uzun. Marka sona, 60-65'e sıkıştır: 'Endüstriyel Rezistans, Isı Eşanjörü, Paslanmaz Boru | ISIŞAH Bursa' (66).

### Orta vade
- 10 statik kategori landing'i /urunler/ altında (build-pages.py ile PRODUCTS dizisinden üret; veri tek kaynak: urunler.html:393-473'ü products.json'a çıkar, hem showroom hem landing okusun): rezistans (9 ürün), endustriyel-mutfak-rezistanslari (4), beyaz-esya-rezistanslari (5), agir-sanayi-isiticilari (4), hvac-kanal-tipi-isitici (4), rayli-sistem-isiticilari (4), savunma-sanayi-isiticilari (3), boykur-boya-kurutma (1), salmex-esanjor-borulari (10), borsah-paslanmaz-celik-boru (3). Her landing: H1 kategori, 300+ kelime, ürün kartları (webp + alt), Product/ItemList + BreadcrumbList JSON-LD, sonunda '3B holde gez' hash CTA. Sitemap 5→15 URL; index #hol= 28 link → landing. (Rakip sitemap: 142–888 URL vs 5.)
- nginx (Plesk ek yönergeler — KULLANICI KARARI, WP dosyalarına dokunmaz): http→https 301, /showroom/ + /showroom/index.html → /, /showroom/hakkimizda.html → /hakkimizda.html, /showroom/vizyon-misyon.html → /vizyon-misyon.html, eski WP /hakkimizda/ → /hakkimizda.html, /vizyon-misyon/ → /vizyon-misyon.html, /urunler-2/ → /showroom/urunler.html (landing'ler gelince /urunler/), error_page 404 → /404.html, güvenlik + cache başlıkları, X-Powered-By gizle (hazir_kod C).
- www: DNS'te www için A/CNAME yok (dig boş) → CNAME www→isisah.com.tr + Plesk alan adı alias + nginx 301 www→kök (baseline'da bilinen; nginx bloğuna eklendi).
- Güvenlik borcu yeni siteyi de etkiliyor (aynı origin): PHP 5.6.40 (EOL 2019) + WordPress 4.8 (2017) + xmlrpc/wp-json açık ihtimali. 'WP'ye dokunulmaz' kuralı korunarak: WP yalnızca 301 kaynağı olsun, barındırıcıdan PHP yükseltme + WP dizinine nginx erişim kısıtı (wp-login/xmlrpc deny) [ONAY].
- urunler.html JS'siz içerik katmanı: index'teki `.js` sınıfı deseni (HANDOFF v5.2) showroom'a da uygulanır — görünür <section class='srlist'> 36 ürün (landing'lere link), WebGL yüklendiğinde CSS ile gizlenir (display:none DEĞİL — Google gizli metni değersizleştirir; sublobby altına küçük, gerçekten okunur liste koy).
- Görsel sitemap: 36 ürün webp (assets/products/) + fabrika görüntüleri için image:image genişletmeli sitemap veya ayrı sitemap-images.xml → Google Görseller trafiği (rezistans/eşanjör görsel arama yoğun).
- Ölçüm altyapısı 0 → çerezsiz self-host analytics (Plausible/Umami, Tailscale kutuda çalışabilir); GSC 15 Eyl okuması + Lighthouse 3 koşu medyan protokolü baseline'da var — landing'ler yayına girince 'dizine eklenen' 30→45 hedefi.
- build-pages.py:106-114 head şablonu tek kaynak olsun: index/urunler/fabrika head'leri de bu şablondan üretilsin (şu an 3 sayfa elle, 2 sayfa scriptten → twitter/og eksikleri bu yüzden tutarsız).

### Ek alanlar / hazır kod


#### hazir_kod
```
<!-- ================================================================
A) EKSİK META/LINK SETİ — index.html <head>'e, satır 17 (<link rel="canonical">) SONRASINA yapıştır.
   Diğer sayfalarda title/description/url/og:title değerlerini o sayfaya göre değiştir.
   Yollar: repo'da "assets/…" (deploy-ftp.sh kök sayfalarda /showroom/assets/'e çevirir).
================================================================ -->
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1" />
<meta property="og:locale" content="tr_TR" />
<meta property="og:image:alt" content="ISIŞAH GROUP merkez binası, Bursa DOSAB — ISIŞAH ENDÜSTRİYEL, BORŞAH BORU, SALMEX" />
<meta name="twitter:title" content="Endüstriyel Rezistans, Isı Eşanjörü, Paslanmaz Boru | ISIŞAH Bursa" />
<meta name="twitter:description" content="1982'den bu yana Bursa DOSAB'da sanayi tipi rezistans, endüstriyel ısıtıcı, SALMEX sarmal eşanjör boruları ve BORŞAH paslanmaz çelik boru üretimi." />
<meta name="twitter:image" content="https://isisah.com.tr/showroom/assets/img/og-cover.jpg" />
<meta name="twitter:image:alt" content="ISIŞAH GROUP merkez binası, Bursa DOSAB" />
<!-- favicon seti: assets/img/ altına kare dosyalar üret (logo-group'tan), favicon.ico'yu httpdocs KÖKÜNE de yükle -->
<link rel="icon" href="/favicon.ico" sizes="32x32" />
<link rel="icon" type="image/svg+xml" href="assets/img/favicon.svg" />
<link rel="icon" type="image/png" sizes="48x48" href="assets/img/favicon-48.png" />
<link rel="icon" type="image/png" sizes="192x192" href="assets/img/favicon-192.png" />
<link rel="apple-touch-icon" sizes="180x180" href="assets/img/apple-touch-icon.png" />
<link rel="manifest" href="assets/site.webmanifest" />
<!-- MEVCUT satır 31 <link rel="icon" href="assets/img/logo.png" /> SİLİNİR (kare değil: 340x105) -->

<!-- assets/site.webmanifest -->
{"name":"ISIŞAH GROUP","short_name":"ISIŞAH","icons":[{"src":"/showroom/assets/img/favicon-192.png","sizes":"192x192","type":"image/png"},{"src":"/showroom/assets/img/favicon-512.png","sizes":"512x512","type":"image/png"}],"theme_color":"#000000","background_color":"#000000","display":"browser","start_url":"/"}

<!-- Favicon üretimi (repo kökünde; logo-group.png 300x120 → kare tuval, şeffaf) -->
<!--
python3 - <<'PY'
from PIL import Image
src=Image.open('assets/catalog/logo-group.png').convert('RGBA')
for name,size in [('favicon-48',48),('favicon-192',192),('favicon-512',512),('apple-touch-icon',180)]:
    canvas=Image.new('RGBA',(size,size),(0,0,0,0)); s=src.copy(); s.thumbnail((int(size*.9),int(size*.9)),Image.LANCZOS)
    canvas.paste(s,((size-s.width)//2,(size-s.height)//2),s); canvas.save(f'assets/img/{name}.png')
Image.open('assets/img/favicon-48.png').save('favicon.ico',sizes=[(16,16),(32,32),(48,48)])
PY
-->

<!-- ================================================================
B) fabrika.html <head> — satır 9 (<link rel="canonical">) SONRASINA (canlıda og:* ve twitter HİÇ yok)
================================================================ -->
<meta name="theme-color" content="#000000" />
<meta name="robots" content="index,follow,max-image-preview:large,max-video-preview:-1" />
<meta property="og:type" content="video.other" />
<meta property="og:locale" content="tr_TR" />
<meta property="og:site_name" content="ISIŞAH GROUP" />
<meta property="og:title" content="SALMEX Sarmal Eşanjör Üretim Hattı — Fabrika Turu | ISIŞAH GROUP" />
<meta property="og:description" content="Kaydırın; SALMEX eşanjör üretim hattında presten robotlu paketlemeye uçun. Bursa DOSAB'daki gerçek fabrika filmi." />
<meta property="og:url" content="https://isisah.com.tr/showroom/fabrika.html" />
<meta property="og:image" content="https://isisah.com.tr/showroom/assets/img/og-cover.jpg" />
<meta property="og:image:width" content="1200" /><meta property="og:image:height" content="630" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="SALMEX Sarmal Eşanjör Üretim Hattı — Fabrika Turu" />
<meta name="twitter:description" content="Scroll'un sürdüğü gerçek fabrika filmi: pres, profil, sarım, test, robotlu paketleme." />
<meta name="twitter:image" content="https://isisah.com.tr/showroom/assets/img/og-cover.jpg" />

<!-- urunler.html:785 — künye logosu boş alt düzeltmesi -->
infoIn.innerHTML=`<img class="blogo" src="assets/catalog/${d.logo}.webp" alt="${d.tag} logosu"><div class="idx">${d.idx}</div>`

# ================================================================
# C) NGINX — Plesk > Web Sitesi > Apache & nginx Ayarları > "Ek nginx yönergeleri"
#    KULLANICI KARARI. WP dosyalarına dokunmaz; sadece yönlendirme+başlık. www için önce DNS CNAME + Plesk alias.
# ================================================================
# --- güvenlik + gizlilik başlıkları (tüm yanıtlar) ---
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
add_header X-Content-Type-Options "nosniff" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
add_header Permissions-Policy "camera=(), microphone=(), geolocation=()" always;
add_header X-Frame-Options "SAMEORIGIN" always;
server_tokens off;
proxy_hide_header X-Powered-By;
charset utf-8;

# --- http→https ve www→kök (Plesk'te "SEO-safe 301" seçeneği de aynı işi yapar) ---
if ($scheme = http) { return 301 https://isisah.com.tr$request_uri; }
if ($host = www.isisah.com.tr) { return 301 https://isisah.com.tr$request_uri; }

# --- kopya URL'ler → kanonik ---
location = /showroom/ { return 301 /; }
location = /showroom/index.html { return 301 /; }
location = /index.html { return 301 /; }
location = /showroom/hakkimizda.html { return 301 /hakkimizda.html; }
location = /showroom/vizyon-misyon.html { return 301 /vizyon-misyon.html; }

# --- eski WP sayfaları → yeni (WP dizini yerinde kalır) ---
location = /hakkimizda/ { return 301 /hakkimizda.html; }
location = /vizyon-misyon/ { return 301 /vizyon-misyon.html; }
location = /urunler-2/ { return 301 /showroom/urunler.html; }   # landing'ler gelince: /urunler/
location = /iletisim/ { return 301 /#iletisim; }

# --- 404: yeni sitenin statik sayfası (httpdocs/404.html) ---
error_page 404 /404.html;
location = /404.html { internal; }

# --- statik cache (dosya adları değişmez; ?v= cache-buster kullanılıyor) ---
location ~* ^/showroom/.*\.(webp|png|jpg|svg|woff2|mp3|mp4)$ { add_header Cache-Control "public, max-age=31536000, immutable"; }
location ~* ^/showroom/vendor/.*\.js$ { add_header Cache-Control "public, max-age=31536000, immutable"; }
location ~* \.html$ { add_header Cache-Control "public, max-age=600, must-revalidate"; }

# ================================================================
# D) tools/deploy-ftp.sh YAMASI — (1) kök sayfaları showroom/'a KOPYA yükleme, (2) showroom sayfalarında göreli ana sayfa linkini köke çevir
# ================================================================
# satır 10:   PAGES=sorted(glob.glob('*.html'))
# YERİNE:
PAGES=sorted(glob.glob('*.html'))
SHOWROOM_ONLY=('urunler.html','fabrika.html')          # showroom/'a yalnız bunlar gider; kök sayfalar kopyalanmaz
used=set(list(SHOWROOM_ONLY)+['sitemap.xml','robots.txt','assets/img/og-cover.jpg'])
# (for f in PAGES döngüsü varlık toplama için AYNI kalır)

# satır 30 (xargs … httpdocs/showroom/{}) ÖNCESİNE — showroom kopyasında ana sayfa linklerini köke çevir:
python3 - <<'PY'
for f in ('urunler.html','fabrika.html'):
    s=open(f).read()
    s=s.replace('href="index.html#','href="/#').replace('href="index.html"','href="/"')
    s=s.replace('href="hakkimizda.html"','href="/hakkimizda.html"').replace('href="vizyon-misyon.html"','href="/vizyon-misyon.html"')
    open('/tmp/sr_'+f,'w').write(s)
PY
for f in urunler.html fabrika.html; do curl -s --netrc-file $NETRC -T /tmp/sr_$f "ftp://ftp.isisah.com.tr/httpdocs/showroom/$f" && rm /tmp/sr_$f; done
# ve LIST'ten urunler.html/fabrika.html ham yüklemesini çıkar:  echo "$LIST" | grep -vE '^(urunler|fabrika)\.html$' | xargs …
# kök yüklemelerine ekle:  curl -s --netrc-file $NETRC -T favicon.ico "ftp://ftp.isisah.com.tr/httpdocs/favicon.ico"
#                          curl -s --netrc-file $NETRC -T 404.html    "ftp://ftp.isisah.com.tr/httpdocs/404.html"
# smoke-test.sh'a ekle:  [ "$(http "$BASE/olmayan-$bust")" = "404" ] && has "$BASE/olmayan-$bust" "ISIŞAH GROUP" && say OK "404 yeni sayfa" || say FAIL "404 WP temasına düşüyor"
#                        [ "$(curl -s -o /dev/null -w '%{size_download}' $BASE/favicon.ico)" -gt 500 ] && say OK "favicon.ico dolu" || say FAIL "favicon.ico boş"

<!-- ================================================================
E) sitemap.xml — lastmod düzeltmesi (satır 6-7) + landing'ler gelince eklenecek 10 URL
================================================================ -->
  <url><loc>https://isisah.com.tr/showroom/urunler.html</loc><lastmod>2026-09-08</lastmod><changefreq>weekly</changefreq><priority>0.9</priority></url>
  <url><loc>https://isisah.com.tr/showroom/fabrika.html</loc><lastmod>2026-09-08</lastmod><changefreq>monthly</changefreq><priority>0.7</priority></url>
  <!-- landing'ler (dosyalar oluşturulduğunda) -->
  <url><loc>https://isisah.com.tr/urunler/rezistans.html</loc><lastmod>2026-09-15</lastmod><priority>0.9</priority></url>
  <url><loc>https://isisah.com.tr/urunler/endustriyel-mutfak-rezistanslari.html</loc><lastmod>2026-09-15</lastmod><priority>0.8</priority></url>
  <url><loc>https://isisah.com.tr/urunler/beyaz-esya-rezistanslari.html</loc><lastmod>2026-09-15</lastmod><priority>0.8</priority></url>
  <url><loc>https://isisah.com.tr/urunler/agir-sanayi-isiticilari.html</loc><lastmod>2026-09-15</lastmod><priority>0.8</priority></url>
  <url><loc>https://isisah.com.tr/urunler/hvac-kanal-tipi-isitici.html</loc><lastmod>2026-09-15</lastmod><priority>0.8</priority></url>
  <url><loc>https://isisah.com.tr/urunler/rayli-sistem-isiticilari.html</loc><lastmod>2026-09-15</lastmod><priority>0.8</priority></url>
  <url><loc>https://isisah.com.tr/urunler/savunma-sanayi-isiticilari.html</loc><lastmod>2026-09-15</lastmod><priority>0.7</priority></url>
  <url><loc>https://isisah.com.tr/urunler/boykur-boya-kurutma.html</loc><lastmod>2026-09-15</lastmod><priority>0.7</priority></url>
  <url><loc>https://isisah.com.tr/urunler/salmex-esanjor-borulari.html</loc><lastmod>2026-09-15</lastmod><priority>0.9</priority></url>
  <url><loc>https://isisah.com.tr/urunler/borsah-paslanmaz-celik-boru.html</loc><lastmod>2026-09-15</lastmod><priority>0.9</priority></url>

<!-- ================================================================
F) httpdocs/404.html — statik, WP temasına düşmeyi keser (nginx error_page ile). Kök yolları /showroom/assets/…
================================================================ -->
<!doctype html>
<html lang="tr">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Sayfa bulunamadı | ISIŞAH GROUP</title>
<meta name="robots" content="noindex,follow" />
<link rel="icon" href="/favicon.ico" />
<link rel="stylesheet" href="/showroom/assets/fonts/inter.css">
<style>body{margin:0;background:#000;color:#fff;font:16px/1.6 Inter,system-ui,sans-serif;display:grid;place-items:center;min-height:100vh;padding:24px}main{max-width:560px}h1{font-size:clamp(1.8rem,5vw,2.6rem);margin:0 0 12px}p{color:#8f93a3}ul{list-style:none;padding:0;display:grid;gap:8px;margin:24px 0}a{color:#fff;border:1px solid #1d1e2a;border-radius:10px;padding:12px 16px;display:block;text-decoration:none}a:hover{border-color:#6b5bff}</style>
</head>
<body>
<main>
<img src="/showroom/assets/catalog/logo-group.webp" alt="ISIŞAH GROUP" height="42" width="auto">
<h1>Aradığınız sayfa burada değil.</h1>
<p>Adres değişmiş ya da yanlış yazılmış olabilir. Sizi doğru yere götürelim:</p>
<ul>
<li><a href="/">Ana sayfa — ISIŞAH GROUP</a></li>
<li><a href="/showroom/urunler.html">3B Ürün Showroom — rezistans, eşanjör, paslanmaz boru</a></li>
<li><a href="/hakkimizda.html">Hakkımızda — 1982'den bugüne Bursa DOSAB</a></li>
<li><a href="/#iletisim">İletişim &amp; teklif</a></li>
</ul>
</main>
</body>
</html>

<!-- ================================================================
G) LANDING İSKELETİ — /urunler/salmex-esanjor-borulari.html (diğer 9'u aynı kalıp; build-pages.py'ye page() benzeri fonksiyon).
   Metinler SALMEX_LIST (urunler.html:444-465) p alanlarından; sayısal iddia ekleme, ekleyeceksen [ONAY].
================================================================ -->
<!doctype html>
<html lang="tr">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
<title>Yoğuşmalı Kombi ve Kazan Eşanjörleri — SALMEX Sarmal Eşanjör Boruları | ISIŞAH</title>
<meta name="description" content="SALMEX: yoğuşmalı kombi ve kazanlar için paslanmaz çelik sarmal eşanjör boruları, helisel boru eşanjörü, premix eşanjör hücresi. Bursa DOSAB'da robotlu üretim hattı." />
<meta name="robots" content="index,follow,max-image-preview:large" />
<link rel="canonical" href="https://isisah.com.tr/urunler/salmex-esanjor-borulari.html" />
<meta property="og:type" content="website" /><meta property="og:locale" content="tr_TR" /><meta property="og:site_name" content="ISIŞAH GROUP" />
<meta property="og:title" content="SALMEX Sarmal Eşanjör Boruları — Yoğuşmalı Kombi ve Kazan Eşanjörleri" />
<meta property="og:description" content="Paslanmaz çelik sarmal eşanjör boruları, helisel ve kazan tipi yoğuşmalı eşanjörler. Bursa DOSAB." />
<meta property="og:url" content="https://isisah.com.tr/urunler/salmex-esanjor-borulari.html" />
<meta property="og:image" content="https://isisah.com.tr/showroom/assets/img/og-cover.jpg" />
<meta name="twitter:card" content="summary_large_image" />
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"CollectionPage",
 "name":"SALMEX Sarmal Eşanjör Boruları","url":"https://isisah.com.tr/urunler/salmex-esanjor-borulari.html",
 "isPartOf":{"@type":"WebSite","name":"ISIŞAH GROUP","url":"https://isisah.com.tr/"},
 "breadcrumb":{"@type":"BreadcrumbList","itemListElement":[
  {"@type":"ListItem","position":1,"name":"Ana Sayfa","item":"https://isisah.com.tr/"},
  {"@type":"ListItem","position":2,"name":"Ürünler","item":"https://isisah.com.tr/showroom/urunler.html"},
  {"@type":"ListItem","position":3,"name":"SALMEX Eşanjör Boruları","item":"https://isisah.com.tr/urunler/salmex-esanjor-borulari.html"}]},
 "mainEntity":{"@type":"ItemList","numberOfItems":10,"itemListElement":[
  {"@type":"ListItem","position":1,"item":{"@type":"Product","name":"Yoğuşmalı Isı Eşanjörü","image":"https://isisah.com.tr/showroom/assets/products/salmex.webp","brand":{"@type":"Brand","name":"SALMEX"},"manufacturer":{"@type":"Organization","name":"ISIŞAH GROUP"},"description":"Paslanmaz çelik sarmal eşanjör borusu; yüksek verimli, farklı kapasitelerde yoğuşmalı tasarım.","url":"https://isisah.com.tr/urunler/salmex-esanjor-borulari.html#yogusmali-isi-esanjoru"}},
  {"@type":"ListItem","position":2,"item":{"@type":"Product","name":"Helisel Boru Eşanjörü","image":"https://isisah.com.tr/showroom/assets/products/helis.webp","brand":{"@type":"Brand","name":"SALMEX"},"description":"Paslanmaz borudan helisel sarım eşanjör; kompakt hacimde yüksek ısı transfer yüzeyi.","url":"https://isisah.com.tr/urunler/salmex-esanjor-borulari.html#helisel-boru-esanjoru"}}
  /* … SALMEX_LIST'ten kalan 8 ürün aynı kalıp … */ ]}}
</script>
<link rel="icon" href="/favicon.ico" /><link rel="apple-touch-icon" href="/showroom/assets/img/apple-touch-icon.png" />
<link rel="stylesheet" href="/showroom/assets/fonts/inter.css">
<!-- index.html <style> bloğu build-pages.py'deki gibi enjekte edilir -->
</head>
<body>
<header><!-- build-pages.py sub(header) ile index'ten; nav'a "Ürünler ▾" açılır menüsü: 10 landing --></header>
<main>
<nav aria-label="breadcrumb"><ol><li><a href="/">Ana Sayfa</a></li><li><a href="/showroom/urunler.html">Ürünler</a></li><li aria-current="page">SALMEX Eşanjör Boruları</li></ol></nav>
<h1>SALMEX sarmal eşanjör boruları: yoğuşmalı kombi ve kazan eşanjörleri</h1>
<p class="lead">SALMEX, ISIŞAH GROUP'un ısı eşanjörü markasıdır. Bursa DOSAB'daki robotlu üretim hattında yoğuşmalı kombi ve kazanlar için paslanmaz çelik sarmal eşanjör boruları, helisel eşanjörler ve premix eşanjör hücreleri üretir. <!-- 250+ kelime: uygulama alanları, malzeme, test, OEM iş birliği — sayısal iddia [ONAY] --></p>
<section aria-labelledby="urunler-h">
<h2 id="urunler-h">SALMEX ürün gamı</h2>
<ul class="pgrid">
  <li id="yogusmali-isi-esanjoru"><img src="/showroom/assets/products/salmex.webp" alt="SALMEX yoğuşmalı ısı eşanjörü — paslanmaz çelik sarmal eşanjör borusu" width="600" height="600" loading="lazy"><h3>Yoğuşmalı Isı Eşanjörü</h3><p>Paslanmaz çelik sarmal eşanjör borusu; yüksek verimli, farklı kapasitelerde yoğuşmalı tasarım.</p></li>
  <li id="helisel-boru-esanjoru"><img src="/showroom/assets/products/helis.webp" alt="SALMEX helisel boru eşanjörü" width="600" height="600" loading="lazy"><h3>Helisel Boru Eşanjörü</h3><p>Paslanmaz borudan helisel sarım eşanjör; kompakt hacimde yüksek ısı transfer yüzeyi.</p></li>
  <!-- … kalan 8 ürün … -->
</ul>
</section>
<section>
<h2>Üretim hattı</h2>
<p>Sarmal eşanjör boruları robotik hücrede işlenir, hat çıkışında sızdırmazlık testinden geçer. <a href="/showroom/fabrika.html">Fabrika turunu kaydırarak izleyin →</a></p>
</section>
<section class="sr-cta">
<h2>3B showroom'da gezin</h2>
<p><a class="btn" href="/showroom/urunler.html#hol=salmex">SALMEX holüne gir →</a> <a class="btn ghost" href="/#iletisim">Teklif iste</a></p>
</section>
<nav aria-label="Diğer ürün grupları"><!-- 9 kardeş landing linki (iç link grafı) --></nav>
</main>
<footer><!-- build-pages.py footer --></footer>
</body>
</html>

<!-- index.html vitrin/marka kartı link değişimi örneği (satır 783-795 .vcard + #urunler .card):
     href="urunler.html#hol=salmex"  →  href="urunler/salmex-esanjor-borulari.html"
     (deploy-ftp.sh kök çevirisinde 'href="urunler/' → 'href="/urunler/' kuralı eklenir) -->
```

### Kanıt
Yöntem: 5 canlı sayfa 8 Eyl 11:52 TRT'de `curl -4 -A Googlebot` ile scratchpad'e indirildi (index 76631 B, hakkimizda 51903, vizyon 47365, urunler 82198, fabrika 12163; hepsi HTTP 200, HTML başlıkları: server nginx, x-powered-by PleskLin, Cache-Control/HSTS/XCTO/Referrer-Policy YOK). ~11:56'da sunucu ofis IP'sine kapandı (nc 443 rc=1, ping %100 kayıp; baseline notu 85.97.200.122 engeli). Sonraki doğrulamalar dış çıkışlardan: api.hackertarget.com/httpheaders ve r.jina.ai (12:09-12:10 TRT).
— Deploy durumu: hackertarget https://isisah.com.tr/ → `Last-Modified: Mon, 07 Sep 2026 11:15:38 GMT`, 76631 B (repo sprint-1 index 76473 B); r.jina.ai robots.txt → 3 satır, Sitemap yok; r.jina.ai fabrika → title 'Fabrika Turu — ISIŞAH GROUP', H1 yok. Repo: `git log` cd3b9b9 11:59 sprint-1, bd6a5b4 12:06 baseline 'Sprint-1 yayına alındı'. Canlı≠repo diff: index 54 satır, hakkimizda 25, urunler 19, fabrika 11 (yol çevirisi normalize edildikten sonra). Canlı Google Fonts satırları index:34-36 (`fonts.googleapis.com`), repo index:35 `assets/fonts/inter.css`.
— JS render: python (script/style sıyrılmış) görünür kelime: index 1530, hakkimizda 650, vizyon 347, urunler 133, fabrika 133. urunler script-dışı eşleşme: 'Kanal Tipi' 0 (script içinde 2), 'Isıtıcı' 0/27, 'BOYKUR' 0/5, 'Ray' 0/8, 'Makas' 0/3. JSON-LD blok1 ItemList numberOfItems=36, url'siz 36/36. r.jina.ai urunler: ürün adları görünmüyor, ~300 kelime (gam kart metinleri dahil).
— Hash linkler: `grep -oE 'href="[^"]*#(hol|marka)=…'` canlı index 28 (salmex 9, borsah 5, isisah_agir 4, isisah_savunma 3, rayli 2, otomotiv 2, rezistans/hvac/beyaz 1), vizyon-misyon 3 `#marka=`; urunler.html:523 `location.hash.match(/^#hol=([a-z_]+)$/)`; index.html:929 `#marka=` regex.
— İç link grafı (canlı <a href>, dış/mailto/tel hariç): index→urunler 7 düz + 28 hash, →hakkimizda 3, →vizyon 3, →fabrika 2; hakkimizda→index 6 (4'ü #iletisim), →vizyon 3, →urunler 3, →fabrika 2; vizyon→hakkimizda 3, →urunler 3, →index 6+3 hash; urunler→'index.html' 2 + 'index.html#urunler' 1, →fabrika 0; fabrika→'index.html' 2, →'urunler.html' 2. Göreli 'index.html' /showroom/ altında /showroom/index.html'e çözülür (urunler.html:296,303; fabrika.html:106,110). Yetim: hackertarget /showroom/hakkimizda.html → 200, 51783 B, Last-Modified 7 Sep 11:15:37; kaynak deploy-ftp.sh:10 `PAGES=sorted(glob.glob('*.html'))` + :30 xargs → httpdocs/showroom/{}.
— 404: hackertarget /olmayan-sayfa → `HTTP/1.1 404 Not Found`, `X-Powered-By: PHP/5.6.40`, `Set-Cookie: PHPSESSID=…`, `Link: ; rel="https://api.w.org/"`, `Cache-Control: no-cache, must-revalidate, max-age=0`; /showroom/olmayan-sayfa.html → aynı 404 WP yanıtı. r.jina.ai /olmayan-sayfa → title 'Sayfa bulunamadı – ISIŞAH ENDÜSTRİ', H1 'Hata 404 - sayfa bulunamadı', arama kutusu + eski nav. r.jina.ai /hakkimizda/ → 200, title 'HAKKIMIZDA – ISIŞAH ENDÜSTRİ', /wp-content/uploads/2017/10/ görselleri.
— Favicon: hackertarget /favicon.ico → `200`, `Content-Type: image/vnd.microsoft.icon`, `Content-Length: 0`, `X-Powered-By: PHP/5.6.40, PleskLin`; /apple-touch-icon.png → 404 (WP). `file assets/img/logo.png` → PNG 340x105; logo-group.png 300x120. Repo kökünde favicon.ico/apple-touch-icon.png/site.webmanifest yok (`ls` hata).
— Meta tutarlılık (canlı grep): 5/5 lang="tr", viewport, charset; canonical=og:url 4/4 (fabrika og yok); meta robots 0/5; hreflang 0/5; twitter:title|description|image 0/5; og:locale 0/5; apple-touch-icon 0/5; manifest 0/5; JSON-LD: index Organization+3 Brand, hakkimizda AboutPage, vizyon WebPage, urunler CollectionPage+Breadcrumb+ItemList, fabrika 0. Title uzunluğu canlı: 88/62/43/81/31; description 222/165/187/215/127.
— Heading: H1 sayısı canlı index 1, hakkimizda 1, vizyon 1, urunler 1, fabrika 0 (repo fabrika.html:100 H1 eklendi, yayında değil). Hiyerarşi atlaması yok (H1→H2→H3).
— img alt (canlı): index 35 img, boş 0, eksik 0; hakkimizda 6/0/0; vizyon 6/0/0; urunler 6 img, alt="" 4 (kapı kartı 3 — aria-hidden + buton aria-label, kabul edilebilir; künye :785 template 1 — düzeltilmeli); fabrika 2/0/0.
— Statik başlıklar: hackertarget logo-isisah.webp → 200 image/webp 35258 B, ETag var, Cache-Control YOK; http://isisah.com.tr/ → 200 (301 yok). DNS: `dig +short www.isisah.com.tr A/CNAME` boş; isisah.com.tr A 46.20.7.162. Sitemap canlı (r.jina.ai): 5 URL, lastmod 09-07/09-07/09-07/08-25/08-29; repo `git log -1 -- urunler.html fabrika.html` → 2026-09-08 11:59 (lastmod eski).
Sınırlar: IP engeli nedeniyle 12:00 sonrası ölçümler üçüncü taraf çıkışlardan; /showroom/index.html ve /showroom/vizyon-misyon.html 200 durumu baseline'daki 'kopya URL 200: 5' bulgusuna dayanır (bu turda yalnız /showroom/hakkimizda.html yeniden doğrulandı). Sunucu tarafı yapılandırma (nginx/Plesk/PHP sürümü) önerileri kullanıcı kararına bırakıldı; WP dosyalarına dokunulmadı.


## icerik-2
**Skor:** İçerik / E-E-A-T: 4,5/10 CANLI (07 Eyl 11:15 GMT yayını) → 5,5/10 yerel bekleyen düzeltmeler yayınlanırsa → hedef 8/10 (11 yeni sayfa + güven sinyalleri). Gerekçe: 5 URL'de toplam ~2.800 görünür kelime (index 1.530 · hakkımızda 650 · vizyon 347 · ürünler 133 · fabrika 133); 8 hedef anahtar kelimeden yalnız 1'i ("boya kurutma") herhangi bir H1/H2'de; "paslanmaz çelik boru üreticisi" ve "demiryolu ısıtıcı" (tam eşleşme) 5 sayfada 0 kez; "Bursa" hiçbir H1/H2'de yok; 36 ürünün açıklaması yalnız JS dizisinde (dizinlenmez); belgeler/referanslar/iletişim tek sayfada, kanıtsız metin.


### Kritik
- K1 · CANLI ≠ YEREL — ilk tur düzeltmeleri YAYINLANMAMIŞ. `git status` → M index.html, urunler.html, fabrika.html, hakkimizda.html, vizyon-misyon.html, robots.txt (son commit b703c7e 07 Eyl 14:57; yerel dosya mtime 15:23). Canlı Last-Modified: Mon, 07 Sep 2026 11:15 GMT (=14:15 TR) → yerel düzenlemelerden ÖNCE. Google hâlâ şunu görüyor: canlı / <title> "ISIŞAH ENDÜSTRİYEL — Isının gücü, teknolojinin hassasiyeti · 1982'den bugüne" (76 kr, anahtar kelime yok), canlı /showroom/fabrika.html <title> "Fabrika Turu — ISIŞAH GROUP" (27 kr) ve H1 YOK, canlı /robots.txt Sitemap satırı hâlâ /showroom/sitemap.xml (yanlış yol), Google Fonts hâlâ dış kaynak. DÜZELTME: `cd ~/isisah-scroll-world && git add -A && git commit -m 'SEO tur-1: title/H1/robots/self-host font' && bash tools/deploy-ftp.sh` → duman testi → GSC'de 5 URL için yeniden dizin isteği. Bu yapılmadan aşağıdaki hiçbir içerik işi ölçülemez.
- K2 · Yerel yeni title'lar da SERP'te kesilir; açıklamalar sınır dışı. index.html:6 title 84 kr (hedef 50-60), urunler.html:6 92 kr, fabrika.html:6 64 kr; index.html:7 description 210 kr (hedef 140-155), urunler.html:7 195 kr, tools/build-pages.py:319 (vizyon desc) 172 kr, fabrika.html:8 114 kr (kısa, CTA yok), hakkımızda (build-pages.py:254-255) 55/152 → tek uygun olan. Marka konumu: fabrika yerel title'da marka ortada ('— Fabrika Turu | ISIŞAH GROUP' yerine slogan önde). DÜZELTME: hazir_kod'daki 5 blok (hepsi 56-60 / 152-154 kr ölçülmüş) → index.html:6-7, urunler.html:6-7, fabrika.html:6+8, build-pages.py:254-255 ve :318-319 sonra `python3 tools/build-pages.py`.
- K3 · Hedef anahtar kelimeler başlık hiyerarşisinde SIFIR. 5 sayfada 5 H1 + 34 H2 var; 8 hedef kelimeden H1/H2'de geçen tek kelime "boya kurutma" (index.html:696 <h2>BOYKUR Oto Boya Kurutma</h2>). H1'ler slogan: index.html:466 "Isının gücü, teknolojinin hassasiyeti.", urunler.html:315 "Üç marka, üç kapı.", vizyon-misyon.html:486 "Vizyonumuz & Misyonumuz.", hakkimizda.html:486 "Hakkımızda." H2'ler de marka sesi: index.html:485 "Üç uzmanlık, tek çatı.", :522 "Üretim yelpazesi.", :711 "Demiryolu İklimlendirme." (kelime 'demiryolu ısıtıcı' değil). Gövde sayımı (canlı): 'sanayi tipi rezistans' index 4 / hakkımızda 5 / diğer 0; 'endüstriyel rezistans' index 1 / ürünler 1; 'paslanmaz çelik boru üreticisi' 5 sayfada 0; 'ısı eşanjörü' index 1 / ürünler 1; 'kombi eşanjörü' yalnız index 1; 'demiryolu ısıtıcı' tam eşleşme 0 (site 'demiryolu ... ısıtıcıları' ve 'Demiryolu Araç Isıtıcısı' der); 'bursa' index 5 / hakkımızda 6 / vizyon 2 / ürünler 1 / fabrika 0 — hiçbiri H1/H2'de. DÜZELTME: H1'lere anahtar kelimeli alt satır (index.html:466 → <h1>Isının gücü, teknolojinin hassasiyeti.<span class="l2 grad-text">Bursa'da sanayi tipi rezistans, ısı eşanjörü ve paslanmaz boru üretimi</span></h1>; urunler.html:315 → "Rezistans, ısı eşanjörü ve paslanmaz boru ürünleri: üç marka, üç kapı.") + hizli_kazanimlar'daki H2/H3 yeniden yazımları.
- K4 · urunler.html'de 36 ürünün metni dizinlenemez (133 görünür kelime). Ürün adı+açıklama+çipler yalnız JS dizilerinde: ISISAH_LIST urunler.html:392-443 (25 ürün), SALMEX_LIST :444-465 (10), BORSAH_LIST :466-473 (3); gam tanımları ISISAH_CATS :485-502. HTML'de yalnız kapı kartları (:315-336) ve ItemList JSON-LD (:27, sadece 'name', description yok). ~600 kelimelik gerçek ürün metni (örn. 'Defrost Rezistansları — Soğutma sistemleri için defrost elemanları; Ø6,5–11,2 mm') hiçbir DOM düğümünde yok → Googlebot JS çalıştırsa da bu metinler yalnız kaide tıklamasında (setInfo, :784-785) DOM'a giriyor. DÜZELTME (build adımı): dizilerden statik `<section id="katalog" class="katalog">` üret — 3 marka × gam <h2>, ürün <h3>+<p>+çip <ul>, urunler.html:348 .outro'dan önce; görsel olarak katlanabilir (<details>) ama display:none DEĞİL. ItemList'e her ürün için "description" ve "url":"…urunler.html#hol=<gam>" ekle. Bu tek adım sayfayı 133 → ~750 kelimeye çıkarır.
- K5 · Eski WP URL'leri fiilen yanıt vermiyor. 08 Eyl 11:50-12:05 arası 3 deneme (25/40/90/150 s zaman aşımı): /hakkimizda/, /vizyon-misyon/, /urunler-2/, /yonetim/, /inovasyon/, /iletisim/, /referanslar/, /kalite-belgelerimiz/, /kalite-politikamiz/ → curl 000 (bağlantı kuruluyor, PHP yanıtı gelmiyor); aynı dakikada statik /hakkimizda.html 200 <1 s. GSC 'dizine eklenen 30 sayfa'nın çoğu bu WP URL'leri → Google için yavaş/soft-error kopya içerik (hakkımızda metni WP'den birebir alındı, HANDOFF notu). WP dosyalarına dokunulmaz kuralı gereği çözüm nginx/Plesk seviyesinde ve KULLANICI KARARI: 301 haritası → /hakkimizda/→/hakkimizda.html, /vizyon-misyon/→/vizyon-misyon.html, /yonetim/ ve /inovasyon/→/hakkimizda.html, /urunler-2/→/showroom/urunler.html, /kalite-*→/hakkimizda.html#belgeler, /iletisim/→/#iletisim, /referanslar/→/#demiryolu (referans satırı). Karar verilmezse en azından GSC'de bu URL'leri izlemeye al.
- K6 · Güven sinyalleri kanıtsız ve tek sayfada. (a) Belgeler: hakkimizda.html:571-583 yalnız metin (TS EN ISO 9001:2015, TSE 1988, CE/EN 60204-1, VDE 1997, UL 2010, RoHS) — belge numarası, veren kuruluş, geçerlilik tarihi, kapsam (hangi ürün grubu) ve PDF/tarama yok [ONAY: kullanıcıdan güncel sertifika PDF'leri]. (b) Referanslar: yalnız index.html:772 tek <p> satırında 27 isim (TÜVASAŞ · TÜLOMSAŞ · TÜRASAŞ · Durmazlar · Bozankaya · MERAK · Safkar · Yazkar · Elite KL · Eltesan · CSR MNG · Air Trade Centre · Heinen & Hopman · Hispacold · Alfa Laval · Bronswerk · Erdemir · Eti Maden · Componenta · Mimsan Grup · Akkim · Elsitel · Alp Enerji · Calorflex · Revenga · Trakya Cam · TPI), Demiryolu bölümünün içine gömülü; hakkımızda'da yok, sektör gruplaması yok, referans sayfası yok. (c) İletişim: adres/tel/faks/e-posta yalnız index.html:812-832 (#iletisim) ve urunler.html:335 (tel+mail); hakkimizda/vizyon-misyon/fabrika gövde ve footer'ında adres/telefon YOK (yalnız 'İletişim' bağlantısı); iletisim.html yok (sitemap 5 URL). Organization JSON-LD (index.html:18-33) ContactPoint, geo, openingHours, tam ticaret unvanı ve vergi/MERSİS bilgisi içermiyor [ONAY: unvan — GSC sorgusunda görülen 'ISIŞAH Endüstriyel Rezistans ve Isı Ekipmanları San. Tic. A.Ş.' doğrulanmalı]. (d) Yönetici unvanı çelişkisi: hakkimizda.html:549 'Mehmet Şahin — Yönetim Kurulu Başkanı' vs vizyon-misyon.html:536 'Mehmet Şahin — Genel Müdür' (kaynak build-pages.py:207 ve :306) [ONAY]. (e) Doğrulanamayan üstünlük iddiaları: 'Türkiye'de sektörünün en büyük firmalarından biri' (hakkimizda.html:508, vizyon-misyon.html:503), 'yerel sermaye ile kurulmuş en büyük ve gelişmiş firma' (hakkimizda.html:548), '%100 Yerli Üretim' (index.html:590, hakkimizda.html:498) — kaynak yoksa yumuşat veya [ONAY].

### Hızlı kazanımlar
- H1 · Title/description değişimi (hazir_kod): index.html:6-7 · urunler.html:6-7 · fabrika.html:6 ve :8 · tools/build-pages.py:254-255 (hakkımızda) ve :318-319 (vizyon) → `python3 tools/build-pages.py` → commit → deploy. Aynı anda og:title senkronu: index.html:11 hâlâ slogan ('ISIŞAH ENDÜSTRİYEL — Isının gücü…'), urunler.html:11 'ISIŞAH GROUP — 3B Ürün Showroom' → yeni title ile aynı yap (paylaşım kartı = arama başlığı).
- H2 · H2/H3'lere anahtar kelime (metin değişikliği, tasarım aynı): index.html:485 'Üç uzmanlık, tek çatı.' → 'Üç uzmanlık, tek çatı: rezistans, paslanmaz boru, ısı eşanjörü.' · index.html:522 'Üretim yelpazesi.' → 'Üretim yelpazesi: sanayi tipi rezistanstan kombi eşanjörüne.' · index.html:711 'Demiryolu İklimlendirme.' → 'Demiryolu Isıtıcıları ve İklimlendirme.' · index.html:606 'Hakkımızda.' → 'Hakkımızda: 1982'den bugüne Bursa'da ısıtma üretimi.' · hakkimizda.html (build-pages.py:163) 'Kuruluş ve gelişim' → 'Kuruluş ve gelişim: Bursa DOSAB'da 1982'den bugüne sanayi tipi rezistans' · urunler.html:340 'ISIŞAH ürün gamları.' → 'ISIŞAH endüstriyel rezistans ve ısıtıcı gamları.' · fabrika.html:124 'Gördüğünüz hat, ürettiğimiz güven.' → 'Gördüğünüz hat, ürettiğimiz güven: SALMEX kombi eşanjörleri, Bursa.'
- H3 · Marka kartı H3'leri (index.html:491, :498, :505): 'Borşah Boru' → 'Borşah Boru — Paslanmaz Çelik Boru Üreticisi' · 'ISIŞAH Endüstriyel' → 'ISIŞAH Endüstriyel — Sanayi Tipi Rezistans ve Isıtıcılar' · 'Salmex Isı Eşanjörleri' → 'SALMEX — Kombi ve Kazan Isı Eşanjörleri'. 'paslanmaz çelik boru üreticisi' ve 'kombi eşanjörü' böylece ilk kez bir başlığa girer.
- H4 · Sayaçlar ham HTML'de sıfır: index.html:587-590 ve hakkimizda.html:495-498 (build-pages.py) başlangıç metni '0 yıl · 0 marka · 0 · %0' (JS data-count ile animasyon). Görünür-metin çıktısında 'Türkiye'de 0 yıl kesintisiz üretim' okunuyor. Başlangıç metnini gerçek değer yap (44 yıl / 3 marka / 8 / %100); index.html:881 counter fonksiyonu animasyonu 0'dan kendisi başlatsın.
- H5 · fabrika.html H1 gizli sayılabilir: :88 `.fh1{position:fixed;font-size:.72rem…}` + :89 `@media(max-width:640px){.fh1{display:none}}` → mobilde H1 yok, masaüstünde 11px. H1'i ilk .cap'in (:115) üstüne görünür başlık olarak taşı; .fin (:124) altına 60-100 kelimelik giriş paragrafı: 'Bursa DOSAB'daki SALMEX hattında doğalgazlı yoğuşmalı kombiler için paslanmaz sarmal eşanjör boruları üretiliyor…' (kelime: sarmal eşanjör, kombi eşanjörü, Bursa, robotlu üretim, sızdırmazlık testi). Sayfa 133 → ~250 kelime.
- H6 · Haberler tarih işaretleme: index.html:805-807 <time> öğelerinde datetime yok, iki haberde yalnız '2026'. → <time datetime="2026-08">Ağustos 2026</time>, <time datetime="2026-07">Temmuz 2026</time> [ONAY: gerçek ay]. Tazelik sinyali + ileride NewsArticle şeması için zemin.
- H7 · İletişim bloğunu her sayfaya: build-pages.py footer şablonuna (page() fonksiyonu, ~:140) ve fabrika.html .fin'e adres satırı 'DOSAB Ali Osman Sönmez Cad. No:11, 16369 Osmangazi / Bursa · +90 224 261 05 27 · info@isisah.com.tr' → NAP tutarlılığı 5/5 sayfa. index.html:18-33 Organization JSON-LD'ye ekle: "contactPoint":[{"@type":"ContactPoint","telephone":"+90-224-261-05-27","contactType":"sales","areaServed":"TR","availableLanguage":["tr"]}], "faxNumber":"+90-224-261-01-77", "geo" [ONAY: koordinat], "numberOfEmployees" YAZMA (kaynak yok).
- H8 · Referans satırını (index.html:772) hakkimizda.html'e 'Referanslarımız' H2 bölümü olarak taşı/kopyala, sektör gruplu METİN (logo için yazılı izin gerekir [ONAY]): Raylı sistemler — TÜVASAŞ · TÜLOMSAŞ · TÜRASAŞ · Durmazlar · Bozankaya · MERAK · Safkar · Yazkar · Elite KL · Eltesan · CSR MNG · Revenga · Calorflex; Gemi/HVAC — Heinen & Hopman · Hispacold · Bronswerk · Air Trade Centre · Alfa Laval · Alp Enerji · Elsitel; Sanayi — Erdemir · Eti Maden · Componenta · Mimsan Grup · Akkim · Trakya Cam · TPI; Otomotiv — Tofaş (BOYKUR ortak Ar-Ge). Her isim sitede zaten var; yeni isim ekleme.
- H9 · Belgeler bölümüne (hakkimizda.html:571-583 / build-pages.py:229-240) her belge için 'Belge no · Veren kuruluş · Geçerlilik · Kapsam' alt satırı ve PDF bağlantısı [ONAY: kullanıcıdan taramalar; eski ISO 9001:2008 taramaları bilerek konmadı — güncel 2015 belgesi şart]. PDF'ler /showroom/assets/docs/ altına; deploy-ftp.sh href="assets/…" regex'i otomatik yakalar.
- H10 · Üstünlük iddialarını yumuşat veya kaynakla: hakkimizda.html:508 & vizyon-misyon.html:503 'Türkiye'de sektörünün en büyük firmalarından biri' → 'Türkiye'nin en köklü sanayi tipi rezistans üreticilerinden biri (1982)'; hakkimizda.html:548 alıntı içindeki 'en büyük ve gelişmiş firma' → alıntı olduğu için koru ama tırnak/atıf net; index.html:590 '%100 Yerli Üretim' → '%100 yerli tasarım ve üretim' yalnız hammadde dâhil doğrulanırsa [ONAY], aksi hâlde 'Bursa'da kendi tesisimizde üretim'.
- H11 · Ürün kartları tek URL'ye akıyor: index.html:533-563'teki 11 kart ve :779-800 vitrin kartlarının hepsi urunler.html#hol=… (hash) → tüm iç bağlantı gücü 1 URL'de. Gam sayfaları açılınca kart başlığı → gam sayfası, 'Showroom'da Gör' → hash bağlantısı olarak ikinci link kalsın.
- H12 · sitemap.xml elle bakım: yeni sayfa eklendiğinde <url> eklenmesi unutulmasın (deploy-ftp.sh:38 ROOT_PAGES glob kök *.html'i otomatik yükler ama sitemap'i güncellemez). Öneri: build-pages.py sonuna sitemap üretimi (ROOT_PAGES + showroom 2 URL) eklemek — 5 dakikalık iş, ileride 16+ URL'de hata önler.

### Orta vade
- O1 · MARKA SAYFASI /isisah-endustriyel.html (kök, deploy-ftp.sh glob otomatik yükler; sitemap'e ekle). H1: Sanayi Tipi Rezistans ve Endüstriyel Isıtıcı Üreticisi — ISIŞAH Endüstriyel, Bursa. H2'ler: 1982'den bugüne endüstriyel rezistans üretimi · 8 ürün gamı: mutfaktan savunmaya · Test ve kalite: her ünite sınanır · Malzeme seçimi · Referans projeler · Teklif ve teknik destek. ÖRNEK METİN (~150 kelime, yalnız sitedeki bilgiler): «ISIŞAH Endüstriyel, 1982'de Bursa'da çeşitli endüstri kolları için sanayi tipi rezistans üretmek üzere kuruldu. 1995'te entegre tesisiyle elektrikli ev aletleri için seri üretime geçti; 2003'te sanayi tipi özel üretim için ayrı bir tesis kurdu. Bugün DOSAB'daki tesislerinde flanşlı, daldırma ve boru tipi rezistanslardan endüstriyel fırınlara, kanal tipi ve mobil ısıtıcılardan demiryolu ve savunma platformu ısıtıcılarına uzanan sekiz ürün gamında üretim yapıyor. Ürünler ISO 9001:2015 kalite yönetim sistemi altında; TSE (1988), VDE (1997) ve UL (2010) uygunluk belgeleriyle üretilir [ONAY: belge kapsamı ürün bazında]. Her ısıtma ünitesi güç, izolasyon direnci ve yüksek gerilimde kaçak akım testinden geçer; demiryolu ürünlerinde şok-vibrasyon ve yangına dayanım testleri uygulanır [ONAY]. Korozyona dayanıklı AISI 304/316 sac, alev geciktirici cam elyaf izoleli kablolar ve çift kademeli termostat koruması standarttır [ONAY]. Ar-Ge tarafında Türkiye'de ilk patentli mobil elektrikli ısıtma ünitesi ve BOYKUR infrared boya kurutma sistemi geliştirildi [ONAY: patent numaraları].» JSON-LD: Organization→Brand 'ISIŞAH ENDÜSTRİYEL' + BreadcrumbList.
- O2 · MARKA SAYFASI /borsah-boru.html. H1: Paslanmaz Çelik Boru Üreticisi — BORŞAH Boru, Bursa. H2'ler: Ø6–42 mm dikişli paslanmaz boru · Tavlı ve kangal boru · Oval kesitli profiller · Üretim yöntemi: roll forming ve TIG kaynak · Kalite kontrol ve basınç testi · Teklif. ÖRNEK METİN (~160 kelime): «BORŞAH Boru, ISIŞAH GROUP'un paslanmaz çelik boru markasıdır; Bursa DOSAB'daki tesiste rezistans imalatı ve genel sanayi için dikişli paslanmaz boru üretir. Borular soğuk şekillendirme (roll forming) ile form alır, argon/hidrojen koruyucu gaz altında TIG kaynağıyla birleştirilir. Standart üretim aralığı Ø6–42 mm dış çap ve 0,35–2 mm et kalınlığıdır [ONAY: paslanmaz kalite/alaşım listesi — sitede yok, eklenmeli]. Aynı çap aralığında tavlı ve kangal boru üretilir; kangal boyu 100–400 m'dir ve kangallar 100 bar basınç testinden geçer [ONAY]. Düz borularda 70–300 bar test ve dokuz aşamalı kalite kontrol uygulanır [ONAY: aşamaların adı]. Rezistans gövdesi, mobilya ve sanayi uygulamaları için oval kesitli profiller de gamda yer alır. BORŞAH boruları grubun kendi rezistans ve SALMEX eşanjör üretiminde kullanılır; Ankara Metro fren borusu projesi (2014) gibi raylı sistem işlerinde referansı vardır. Tüm üretim ISO 9001:2015 kalite yönetim sistemi altındadır; teklif ve numune için DOSAB merkez.» Not: 'paslanmaz çelik boru üreticisi' ilk kez H1'de.
- O3 · MARKA SAYFASI /salmex.html. H1: Kombi ve Kazan Isı Eşanjörü Üreticisi — SALMEX, Bursa. H2'ler: Yoğuşmalı kombi eşanjörleri · Kazan tipi yoğuşmalı eşanjör · Elektrikli kombi eşanjörleri ve ısıtıcı üniteler · Helisel boru ve spiral serpantin · Robotlu üretim hattı ve sızdırmazlık testi · Fabrika turu (fabrika.html'e iç bağlantı). ÖRNEK METİN (~170 kelime): «SALMEX, ISIŞAH GROUP'un ısı eşanjörü markasıdır. Bursa DOSAB'daki robotlu üretim hattında doğalgazlı yoğuşmalı kombiler için paslanmaz çelik sarmal eşanjör boruları, alüminyum döküm eşanjör hücreleri, premix yoğuşmalı hücreler, elektrikli kombi eşanjörleri ve kazan tipi yoğuşmalı eşanjörler üretilir. Ürün ailesi helisel boru eşanjörleri, yassı spiral serpantinler, kanatlı borulu konvansiyonel ana eşanjörler ve elektrikli ısıtma modülleriyle tamamlanır. Sarmal eşanjör borusu tek parça sacdan kendi presimizde şekillendirilir; boru ve kanat formları CNC kontrolünde işlenir, sarım robotik hücrede yapılır, gövdeler ısıl işlemden geçer [ONAY: ısıl işlem türü]. Hat çıkışında her ünite sızdırmazlık ve güç testinden geçer. Yeni robotlu yatırım seri üretimde tutarlı kaynak ve form kalitesiyle artan kapasite sağlar [ONAY: kapasite rakamı yazılmadı]. Paslanmaz borular grup içindeki BORŞAH'tan gelir; hammaddeden bitmiş eşanjöre üretim tek çatı altında kalır. Kombi ve kazan üreticileri için OEM tedarik ve projeye özel tasarım desteği sunulur [ONAY].» 'kombi eşanjörü' ilk kez H1'de; fabrika.html VideoObject'e bu sayfadan bağlantı.
- O4 · GAM SAYFASI /endustriyel-rezistanslar.html (urunler.html ISISAH_CATS.isisah_rezistans, 9 ürün). H1: Endüstriyel Rezistanslar: Flanşlı, Daldırma ve Boru Tipi Isıtıcı Elemanlar. H2'ler: Özel tip flanş rezistansları · Yassı rezistanslar (fritöz, haşlama) · Defrost rezistansları · Proses ısıtıcı üniteleri · Malzeme ve test · Teklif. ÖRNEK METİN (~135 kelime): «ISIŞAH Endüstriyel'in çekirdek gamı sanayi tipi rezistanslardır: daldırma ve boru tipi ısıtıcı elemanlar, özel tip flanş rezistansları ve endüstriyel proses hatları için flanşlı, kanal gövdeli proses ısıtıcı üniteleri. Endüstriyel mutfak ekipmanları için fritöz ve makarna haşlama yassı rezistansları, sanayi tipi bulaşık makineleri için boyler ve tank ısıtıcıları, konveksiyonel fırınlar için dairesel elemanlar üretilir. Soğutma sistemlerine yönelik defrost rezistansları Ø6,5–11,2 mm boru çaplarında yapılır [ONAY]. Tüm rezistanslar yüksek sıcaklığa dayanıklı, yerli üretimdir; gövdelerde BORŞAH paslanmaz boru kullanılır. Her ürün güç ve izolasyon direnci testinden geçer; yüksek gerilimde kaçak akım (dielektrik) testi standarttır [ONAY]. Projeye özel güç, gerilim, form ve bağlantı tipi için teknik ekip sahada sistem analizi yapar. 1982'den bu yana Bursa DOSAB'da üretim.» Hedef: 'endüstriyel rezistans' + 'sanayi tipi rezistans' + 'bursa'.
- O5 · GAM SAYFASI /endustriyel-mutfak-rezistanslari.html (isisah_mutfak, 4 ürün). H1: Endüstriyel Mutfak Rezistansları — Fritöz, Konveksiyonel Fırın, Bulaşık Makinesi, Haşlama. H2'ler: Konveksiyonel fırın rezistansları · Fritöz yassı rezistansları · Bulaşık makinesi boyler/tank ısıtıcıları · Makarna haşlama rezistansları · Disk ısıtıcılar · OEM üretim. ÖRNEK METİN (~130 kelime): «Endüstriyel mutfak ekipmanı üreticileri için ISIŞAH dört ana rezistans ailesi sunar: konveksiyonel fırınlar için dairesel ısıtıcı elemanlar; endüstriyel fritözler için hızlı ve homojen ısıtan daldırma tip yassı rezistans rafları; sanayi tipi bulaşık makineleri için boyler ve tank ısıtıcı elemanları; makarna haşlama üniteleri için daldırma tip yassı rezistanslar. Ürünler paslanmaz gövdelidir ve yüksek sıcaklığa dayanıklı olarak üretilir. Kahve makinesi, çaydanlık ve bulaşık makineleri için paslanmaz disk ısıtıcılar bu gamı tamamlar. Elektrikli ev aletleri için seri üretim deneyimi 1995'teki entegre tesise dayanır; 1997'den beri VDE (DIN EN) ve 2010'dan beri UL uygunluk sertifikaları ihracat pazarlarına üretimi destekler [ONAY: hangi ürün grupları kapsamda]. Cihaz üreticileri için mevcut tasarıma uygun ölçü, güç ve bağlantı seçenekleriyle OEM üretim yapılır [ONAY].»
- O6 · GAM SAYFASI /beyaz-esya-rezistanslari.html (isisah_beyaz, 5 ürün). H1: Beyaz Eşya ve Elektrikli Ev Aletleri Rezistansları. H2'ler: Kurutma makinesi ısıtıcıları · Defrost rezistansları · Ocak (spiral) rezistansları · Fırın alt-üst ve turbo rezistansları · Disk ısıtıcılar · Belgeler ve seri üretim. ÖRNEK METİN (~125 kelime): «ISIŞAH, 1995'ten bu yana elektrikli ev aletleri için seri rezistans üretir. Gamda kurutma makinesi ısıtıcı üniteleri (sitede Arçelik ve Vestel kurutma makineleri için belirtilmiştir [ONAY: marka adı kullanım izni]), soğutucular için defrost rezistansları, elektrikli ocaklar için spiral boru rezistanslar, ev tipi fırınlar için alt-üst ve turbo rezistanslar ile kahve makinesi ve çaydanlık disk ısıtıcıları yer alır. Defrost elemanları Ø6,5–11,2 mm çapta, yüksek sıcaklığa dayanıklı paslanmaz gövdelidir [ONAY]. Ürünler TSE (1988'den beri), VDE (1997) ve UL (2010) uygunluk belgeleri ve RoHS uyumlu malzemelerle üretilir [ONAY: ürün bazlı kapsam]. Seri üretim ISO 9001:2015 altında; hammadde borusu grup içinden (BORŞAH) gelir. OEM projelerde CAD ile üretime hazırlık ve ERP destekli tedarik planlaması uygulanır.»
- O7 · GAM SAYFASI /endustriyel-firin-proses-isitici.html (isisah_agir, 4 ürün). H1: Ağır Sanayi Isıtma: Endüstriyel Fırın, Proses Isıtıcı ve Mobil Elektrikli Isıtıcı. H2'ler: Endüstriyel ısıl işlem ve kurutma fırınları · Proses ısıtıcı üniteleri ve flanş rezistansları · Uğur Böceği mobil elektrikli ısıtıcılar · Sanayi referansları · Malzeme ve emniyet. ÖRNEK METİN (~130 kelime): «Ağır sanayi gamı üç ürün ailesinden oluşur. Endüstriyel fırınlar: kontrol panelli (PLC) sanayi tipi ısıl işlem ve kurutma fırınları, projeye özel boyut ve sıcaklık profiliyle [ONAY: sıcaklık aralığı sitede yok]. Proses ısıtıcı üniteleri: endüstriyel proses hatları için flanşlı, kanal gövdeli, yüksek kapasiteli ısıtıcılar ve özel tip flanş rezistansları. Mobil elektrikli ısıtıcılar: 'Uğur Böceği' serisi taşınabilir fanlı ısıtıcılar, üç boyda, atölye ve saha ısıtması için; Türkiye'de ilk patentli mobil elektrikli ısıtma ünitesi ISIŞAH tarafından üretilmiştir [ONAY: patent no]. Referanslar arasında Erdemir, Eti Maden, Componenta, Trakya Cam ve Mimsan Grup gibi sanayi kuruluşları bulunur [ONAY: izin]. Ürünler AISI 304/316 paslanmaz sac, alev geciktirici kablolar ve EBM fanlarla üretilir; her ünitede çift kademeli termostat koruması vardır [ONAY].»
- O8 · GAM SAYFASI /kanal-tipi-isitici-hvac.html (isisah_hvac, 4 ürün). H1: HVAC Isıtıcıları: Kanal Tipi, Fan-Coil ve Klima Santrali (AHU) Isıtıcıları. H2'ler: Kanal tipi elektrikli ısıtıcılar (santral, dikdörtgen, yuvarlak) · Fan-coil ve ortam ısıtıcıları · Klima santrali (AHU) ısıtıcı üniteleri · Silindirik kanal fan ısıtıcısı · Test ve gürültü ölçümü · Raylı ve gemi HVAC uygulamaları. ÖRNEK METİN (~135 kelime): «İklimlendirme gamında kanatlı rezistanslı kanal tipi hava ısıtıcıları (santral, dikdörtgen ve yuvarlak kanal), fan-coil üniteleri ve ortam ısıtması için dik finli paslanmaz ısıtıcılar, klima santralleri için yüksek kapasiteli paslanmaz AHU ısıtıcı üniteleri ve havalandırma kanalları için fanlı silindirik kanal ısıtıcıları üretilir. Üniteler havalandırma ve proses hatlarına göre boyutlandırılır; düşük yüzey yükü ve fin etkili verimli ısıtma prensibiyle tasarlanır. Yüksek kaliteli EBM fanlar, titreşime dayanıklı çözülmez bağlantı ekipmanları ve çift kademeli termostat koruması standarttır [ONAY]. Fan gürültü seviyesi (desibel), yüzey sıcaklığı ve IP seviyesi testleri yapılır. Aynı ısıtıcı teknolojisi tren ve tramvay klima santrallerinde (İstanbul Ulaşım M1, İzmir Tramvay, Ankara Metro) ve askeri gemi klima santrallerinde uygulanmıştır. HVAC üreticileri için OEM ve projeye özel üretim yapılır.»
- O9 · GAM SAYFASI /demiryolu-isiticilari.html (isisah_rayli, 4 ürün + index Demiryolu bölümü). H1: Demiryolu Isıtıcıları: Klima, Koltuk Altı, Ray ve Makas Isıtıcıları. H2'ler: Klima (HVAC) ısıtıcı elemanları · Yolcu, vestibül ve makinist ısıtıcıları · TIJ kasaları ve şasi ısıtıcıları · Ray ve makas ısıtıcıları (1000 W / 230 V) · Personel kabini ısıtıcıları · Test ve izolasyon · 1986'dan bugüne proje geçmişi (index.html:727-771 zaman çizelgesi buraya taşınır/kopyalanır). ÖRNEK METİN (~150 kelime): «ISIŞAH Endüstriyel 1986'daki TÜVASAŞ TIJ projesinden bu yana demiryolu sanayine ısıtıcı üretir: tren ve tramvay klima santralleri için HVAC ısıtıcı elemanları, koltuk düzenine göre tasarlanan yolcu, vestibül ve makinist ısıtıcıları, pencere altı TIJ kasaları, vagon altı şasi ısıtıcıları (TVS 2000'den bu yana), 1000 W / 230 V ray ve makas ısıtıcıları, finli paslanmaz personel kabini ısıtıcıları, vagon mutfağı AC-DC ısıtma plakaları, kOhm dirençler ve batarya ısıtıcıları. Rezistanslar yüksek hızlı tren standartlarında yüksek gerilime dayanıklıdır; GP03 ve mika izolasyonla kaçak akım gövdeye iletilmez; şok-vibrasyon ve yangına dayanım testleri uygulanır [ONAY: standart numaraları]. Projeler: Ankara Metro (2014), İstanbul Ulaşım E-14000 (2016-17), Durmazlar Alibeyköy (2018-19), İzmir Tramvay (2018-21), MERAK Brüksel ihracatı (2019-23), Bükreş tramvayları (2021-26), Bozankaya Kayseri (2022-26), TÜRASAŞ EMU 225 (2023-26), İstanbul Metro (2025-26). Fren borusu projesinde BORŞAH paslanmaz borular kullanılmıştır.» 'demiryolu ısıtıcı' ilk kez tam eşleşme + H1.
- O10 · GAM SAYFASI /savunma-sanayi-isitma.html (isisah_savunma, 3 ürün). H1: Savunma Sanayi Isıtma ve İklimlendirme: Askeri Gemi Isıtıcıları. H2'ler: Askeri gemi iklimlendirme çözümleri · Savunma tipi blast heater · Baseboard konvektör ısıtıcı · Malzeme, test ve izolasyon · Gemi HVAC entegratörü referansları. ÖRNEK METİN (~125 kelime): «ISIŞAH Endüstriyel, milli savunma platformları için ısıtma ve iklimlendirme ekipmanı üretir. Gamda askeri gemi klima santralleri için fanlı blast heater üniteleri (NBC uyumlu klima santrali entegrasyonu [ONAY]), gemi ve savunma platformları için delikli kasalı süpürgelik tipi baseboard konvektör ısıtıcılar ve amfibi hücum gemileri ile MİLGEM sınıfı platformlar için ısıtma-iklimlendirme çözümleri yer alır; TCG Anadolu (L400) referansı showroom'da belirtilmiştir [ONAY: kamuya açıklama izni]. Ürünler korozyona dayanıklı AISI 304/316 paslanmaz sac, alev geciktirici cam elyaf izoleli kablolar ve titreşime dayanıklı bağlantı ekipmanlarıyla üretilir; şok ve vibrasyon testleri ile yüksek gerilimde kaçak akım testi uygulanır [ONAY: askeri standart]. Gemi HVAC entegratörleri Heinen & Hopman, Hispacold ve Bronswerk referans listesindedir [ONAY]. Tamamı yerli üretim; ISO 9001:2015 altında, Bursa DOSAB'da.»
- O11 · GAM SAYFASI /boykur-oto-boya-kurutma.html (isisah_otomotiv, 1 ürün + index.html:690-706 bölümü). H1: BOYKUR İnfrared Oto Boya Kurutma Sistemi — Mobil, Bilgisayar Kontrollü. H2'ler: Tofaş ile ortak Ar-Ge · İnfrared kurutma nasıl çalışır · Kullanım alanları (otomotiv yan sanayi, servis, tekne, mobilya) · Teknik özellikler [ONAY] · Servis ve teklif. ÖRNEK METİN (~125 kelime): «BOYKUR, ISIŞAH Ar-Ge çalışması sonucunda Tofaş ile birlikte yürütülen projeyle geliştirilen, infrared teknolojili, bilgisayar kontrollü mobil oto boya kurutma sistemidir. Türkiye'de ilk defa yerli imalat olarak patentli infrared boya kurutma ünitesi ISIŞAH tarafından üretilmiştir [ONAY: patent no ve yılı]. Hızlı, homojen ve enerji verimli kurutma sağlar; taşınabilir gövdesi ve hassas sıcaklık kontrolüyle otomotiv yan sanayi, servis istasyonları, tekne ve mobilya imalathanelerinde kullanılır. Kurutma sırasında yüzey sıcaklığı bilgisayar kontrolüyle izlenir; program boya tipine göre ayarlanabilir [ONAY]. Kurutma süresi, güç ve panel sayısı gibi teknik veriler katalogdan eklenecektir [ONAY — sitede yok, uydurma yazılmadı]. Ürün ISIŞAH Endüstriyel otomotiv gamının tek ürünüdür ve 3B showroom Otomotiv holünde incelenebilir. Servis ve yedek parça desteği Bursa DOSAB merkezden verilir [ONAY].» 'boya kurutma' + 'bursa' H1/H2'de.
- O12 · GÜVEN SAYFALARI (HANDOFF 2. dalga paketiyle birlikte): /iletisim.html (H1 'İletişim — ISIŞAH GROUP Bursa DOSAB', NAP + harita tıkla-yükle + teklif formu self-host PHP; ContactPage + ContactPoint JSON-LD), /referanslar.html (H8'deki sektör gruplu liste + 'Proje geçmişi' zaman çizelgesi; logo yalnız yazılı izinle [ONAY]), /belgeler.html (her sertifika: kuruluş, no, tarih, kapsam, PDF [ONAY]), künye/KVKK (tam ticaret unvanı, MERSİS, vergi no [ONAY]). Organization JSON-LD legalName'i doğrulanmış unvanla güncelle. Bu 4 sayfa E-E-A-T'nin 'Trust' ayağını tek seferde kurar.
- O13 · HABER DETAY SAYFALARI: index.html:805-807'deki 3 haber → /haberler/<slug>.html (deploy-ftp.sh ROOT_PAGES yalnız kök *.html tarar → ya kök düz dosya /haber-3b-showroom.html kullan ya da :38 glob'u 'haberler/*.html' ile genişlet). Her biri NewsArticle JSON-LD (headline, datePublished, publisher=Organization, image). Metin onayı HANDOFF'ta bekliyor [ONAY].
- O14 · İÇ BAĞLANTI MİMARİSİ: nav 'Ürünler' → açılır menü (3 marka + 8 gam); index.html:533-563 kartları → gam sayfaları; her gam sayfasında 'Showroom'da gez' → urunler.html#hol=<gam> ve ilgili marka sayfasına link; marka sayfaları ↔ fabrika.html ↔ hakkimizda.html çapraz; her yeni sayfada BreadcrumbList JSON-LD (Ana Sayfa › Marka › Gam). Hedef: 5 → 16+ dizinlenebilir URL (rakip 142–888'e karşı ilk adım), GSC 30 gün hedefi 'kategori sorgusu gösterim >200' için zemin.
- O15 · WP 301 HARİTASI (kullanıcı kararı, K5) + eski WP alt sayfa içeriğinin tekilleştirilmesi: statik sayfalar yayında olduğu sürece /hakkimizda/ ile /hakkimizda.html aynı metin → canonical çakışması. 301 verilemezse en azından WP tarafına dokunmadan GSC'de 'URL kaldırma' değil, sadece izleme; 90 günde WP URL'lerinin dizinden düşmesi beklenir.

### Ek alanlar / hazır kod


#### hazir_kod
```
<!-- ============================================================
     ISIŞAH GROUP — 5 sayfa title + description (ölçülü: title 56-60 kr, description 152-154 kr)
     Marka sonda, Türkçe, anahtar kelime önde. og:title/og:description aynı değerle senkronlanır.
     ============================================================ -->

<!-- 1) ANA SAYFA — index.html:6-7 (og: index.html:11-12) -->
<title>Sanayi Tipi Rezistans, Isı Eşanjörü, Paslanmaz Boru | ISIŞAH</title>
<meta name="description" content="1982'den beri Bursa DOSAB'da sanayi tipi rezistans, endüstriyel fırın, kanal tipi ısıtıcı, kombi eşanjörü ve paslanmaz çelik boru üretimi. ISO 9001:2015." />
<meta property="og:title" content="Sanayi Tipi Rezistans, Isı Eşanjörü, Paslanmaz Boru | ISIŞAH" />
<meta property="og:description" content="1982'den beri Bursa DOSAB'da sanayi tipi rezistans, endüstriyel fırın, kanal tipi ısıtıcı, kombi eşanjörü ve paslanmaz çelik boru üretimi. ISO 9001:2015." />

<!-- 2) HAKKIMIZDA — tools/build-pages.py:254-255 (page() 2. ve 3. argüman), sonra `python3 tools/build-pages.py` -->
<title>Hakkımızda: 1982'den Bugüne Bursa'da Isıtma Üretimi | ISIŞAH</title>
<meta name="description" content="ISIŞAH GROUP: 1982 kuruluş, 1995 entegre tesis, 2011 grup yapısı. Rezistans, paslanmaz boru ve eşanjör markaları; TSE, VDE, UL ve ISO 9001:2015 belgeleri." />
<!-- build-pages.py için Python satırları: -->
<!--     'Hakkımızda: 1982\'den Bugüne Bursa\'da Isıtma Üretimi | ISIŞAH',
         'ISIŞAH GROUP: 1982 kuruluş, 1995 entegre tesis, 2011 grup yapısı. Rezistans, paslanmaz boru ve eşanjör markaları; TSE, VDE, UL ve ISO 9001:2015 belgeleri.', -->

<!-- 3) VİZYON & MİSYON — tools/build-pages.py:318-319 -->
<title>Vizyon, Misyon ve Kalite Politikası | ISIŞAH GROUP Bursa</title>
<meta name="description" content="ISIŞAH GROUP vizyonu, misyonu ve Kalite-İSG-Çevre politikası: rezistans, paslanmaz boru ve ısı eşanjörü üretiminde ISO 9001 disiplini, güvenilir şirket." />
<!--     'Vizyon, Misyon ve Kalite Politikası | ISIŞAH GROUP Bursa',
         'ISIŞAH GROUP vizyonu, misyonu ve Kalite-İSG-Çevre politikası: rezistans, paslanmaz boru ve ısı eşanjörü üretiminde ISO 9001 disiplini, güvenilir şirket.', -->

<!-- 4) 3B SHOWROOM / ÜRÜNLER — urunler.html:6-7 (og: urunler.html:11-12) -->
<title>Rezistans, Isı Eşanjörü ve Paslanmaz Boru Ürünleri | ISIŞAH</title>
<meta name="description" content="36 ürün: sanayi tipi rezistans, kanal tipi ısıtıcı, demiryolu ısıtıcıları, kombi eşanjörü ve Ø6–42 mm paslanmaz çelik boru. 3B showroom'da teklif isteyin." />
<meta property="og:title" content="Rezistans, Isı Eşanjörü ve Paslanmaz Boru Ürünleri | ISIŞAH" />
<meta property="og:description" content="36 ürün: sanayi tipi rezistans, kanal tipi ısıtıcı, demiryolu ısıtıcıları, kombi eşanjörü ve Ø6–42 mm paslanmaz çelik boru. 3B showroom'da teklif isteyin." />

<!-- 5) FABRİKA TURU — fabrika.html:6 (title) ve :8 (description); og meta bu sayfada yok → ekle -->
<title>SALMEX Eşanjör Üretim Hattı: Fabrika Turu | ISIŞAH Bursa</title>
<meta name="description" content="Bursa DOSAB'daki SALMEX sarmal eşanjör hattını kaydırarak gezin: pres, CNC şekillendirme, sarmal sarım, ısıl işlem, robotlu üretim ve sızdırmazlık testi." />
<meta property="og:type" content="video.other" />
<meta property="og:site_name" content="ISIŞAH GROUP" />
<meta property="og:title" content="SALMEX Eşanjör Üretim Hattı: Fabrika Turu | ISIŞAH Bursa" />
<meta property="og:description" content="Bursa DOSAB'daki SALMEX sarmal eşanjör hattını kaydırarak gezin: pres, CNC şekillendirme, sarmal sarım, ısıl işlem, robotlu üretim ve sızdırmazlık testi." />
<meta property="og:url" content="https://isisah.com.tr/showroom/fabrika.html" />
<meta property="og:image" content="https://isisah.com.tr/showroom/assets/img/og-cover.jpg" />
<meta name="twitter:card" content="summary_large_image" />

<!-- ============================================================
     EK A — H1 alt satırları (tasarım aynı, anahtar kelime H1'e girer)
     ============================================================ -->
<!-- index.html:466 -->
<h1>Isının gücü,<span class="l2 grad-text">teknolojinin hassasiyeti.</span><span class="l3">Bursa'da sanayi tipi rezistans, ısı eşanjörü ve paslanmaz çelik boru üretimi.</span></h1>
<!-- CSS (index <style> içine): .hero h1 .l3{display:block;font-size:clamp(1rem,1.6vw,1.25rem);font-weight:500;letter-spacing:0;color:var(--muted);margin-top:14px} -->

<!-- urunler.html:315 -->
<h1 class="big">Üç marka,<br><span class="g">üç kapı.</span><span class="sr">Rezistans, ısı eşanjörü ve paslanmaz boru ürünleri</span></h1>
<!-- CSS: .intro h1 .sr{display:block;font-size:.95rem;font-weight:500;letter-spacing:.02em;color:var(--muted);margin-top:10px} (görünür kalsın; display:none / clip KULLANMA) -->

<!-- ============================================================
     EK B — Organization JSON-LD'ye eklenecek alanlar (index.html:18-33, "knowsAbout"tan sonra)
     ============================================================ -->
,"faxNumber":"+90-224-261-01-77",
"contactPoint":[{"@type":"ContactPoint","telephone":"+90-224-261-05-27","contactType":"sales","areaServed":"TR","availableLanguage":["tr"]},
                {"@type":"ContactPoint","telephone":"+90-224-443-61-00","contactType":"customer service","areaServed":"TR","availableLanguage":["tr"]}],
"hasCredential":[{"@type":"EducationalOccupationalCredential","name":"TS EN ISO 9001:2015 Kalite Yönetim Sistemi","credentialCategory":"certification"},
                 {"@type":"EducationalOccupationalCredential","name":"TSE Türk Standartlarına Uygunluk Belgesi","credentialCategory":"certification"},
                 {"@type":"EducationalOccupationalCredential","name":"VDE DIN EN Uygunluk Sertifikası","credentialCategory":"certification"},
                 {"@type":"EducationalOccupationalCredential","name":"UL Uygunluk Sertifikası","credentialCategory":"certification"}]
/* "geo" ve "legalName" (tam ticaret unvanı) → [ONAY] alınmadan EKLENMEZ */

<!-- ============================================================
     EK C — urunler.html statik katalog (K4) — build adımı şablonu; :348 <div class="outro"> ÖNCESİNE
     Dizilerden (ISISAH_CATS / SALMEX_LIST / BORSAH_LIST) üretilir; örnek 1 gam:
     ============================================================ -->
<section id="katalog" class="katalog" aria-label="Ürün kataloğu (metin)">
  <h2>Tüm ürünler — 3 marka, 36 ürün</h2>
  <details open>
    <summary><h3>ISIŞAH · Endüstriyel Rezistanslar</h3><span>Flanşlı, daldırma, boru tipi ve proses rezistansları</span></summary>
    <ul>
      <li><h4>Özel Tip Flanş Rezistansları</h4><p>Daldırma ve boru tipi ısıtıcı elemanlar; sanayi ve proses uygulamaları için.</p><a href="#hol=isisah_rezistans">Showroom'da gör →</a></li>
      <li><h4>Defrost Rezistansları</h4><p>Soğutma sistemleri için defrost elemanları; Ø6,5–11,2 mm, yüksek sıcaklığa dayanıklı.</p><a href="#hol=isisah_rezistans">Showroom'da gör →</a></li>
      <!-- … dizideki her d için: <li><h4>${d.h}</h4><p>${d.p}</p> … -->
    </ul>
  </details>
  <!-- … 8 ISIŞAH gamı + SALMEX + BORŞAH aynı kalıpla -->
</section>
```

### Kanıt
## 1. Canlı ≠ yerel (08 Eyl 2026, 11:50-12:05 TR)
- `curl -I https://isisah.com.tr/hakkimizda.html` → HTTP/2 200, `last-modified: Mon, 07 Sep 2026 11:15:45 GMT`, server nginx/PleskLin; /showroom/urunler.html 11:15:38; /showroom/fabrika.html 11:15:34.
- `git status --short` (repo /Users/mehmetcansahin/isisah-scroll-world): M index.html · M urunler.html · M fabrika.html · M hakkimizda.html · M vizyon-misyon.html · M robots.txt · M tools/build-pages.py · M tools/deploy-ftp.sh · M tools/smoke-test.sh (son commit b703c7e, 07 Eyl 14:57).
- `git diff -U0` kanıtı: index.html:6 `-<title>ISIŞAH ENDÜSTRİYEL — Isının gücü…` → `+<title>Endüstriyel Rezistans, Isı Eşanjörü…`; fabrika.html:6 `-<title>Fabrika Turu — ISIŞAH GROUP</title>` + `+<h1 class="fh1">…` (:100); robots.txt `-Sitemap: …/showroom/sitemap.xml` → `+Sitemap: https://isisah.com.tr/sitemap.xml`; Google Fonts → assets/fonts/inter.css (5 dosya). Canlı HTML'de bunların hiçbiri yok.

## 2. Görünür metin (script/style/svg/yorum çıkarıldı, HTML entity çözüldü)
| Sayfa | Canlı kelime | Yerel kelime | Title kr (canlı→yerel) | Desc kr | H1 | H2/H3 |
|---|---|---|---|---|---|---|
| / | 1.530 | 1.532 | 76 → 84 | 210 | 1 (slogan) | 13 / 32 |
| /hakkimizda.html | 650 | 650 | 55 | 152 | 1 | 6 / 2 |
| /vizyon-misyon.html | 347 | 347 | 39 | 172 | 1 | 4 / 0 |
| /showroom/urunler.html | 133 | 135 | 71 → 92 | 195 | 1 (slogan) | 3 / 0 |
| /showroom/fabrika.html | 133 | 147 | 27 → 64 | 114 | 0 → 1 (mobilde display:none, fabrika.html:89) | 8 / 0 |
Toplam ~2.800 kelime / 5 URL. urunler.html'de 36 ürün × (ad+açıklama+3 çip) ≈ 600 kelime yalnız JS'te (urunler.html:392-473).

## 3. Anahtar kelime kapsama (canlı; gövde adet / H1+H2 adet / title adet)
| Kelime | index | hakkımızda | vizyon | ürünler | fabrika |
|---|---|---|---|---|---|
| sanayi tipi rezistans | 4 / 0 / 0 | 5 / 0 / 0 | 0 | 0 | 0 |
| endüstriyel rezistans | 1 / 0 / 0 (yerel 2/0/1) | 0 | 0 | 1 / 0 / 0 | 0 |
| paslanmaz çelik boru üreticisi | 0 | 0 | 0 | 0 | 0 |
| paslanmaz çelik boru | 3 / 0 / 0 | 2 / 0 / 0 | 1 / 0 / 0 | 1 / 0 / 0 | 0 |
| ısı eşanjörü | 1 / 0 / 0 (yerel 2/0/1) | 0 | 0 | 1 / 0 / 1 | 0 |
| kombi eşanjörü | 1 / 0 / 0 | 0 | 0 | 0 | 0 |
| demiryolu ısıtıcı (tam) | 0 (varyant: "demiryolu … ısıtıcıları" :712, "Demiryolu Araç Isıtıcısı" JS) | 0 | 0 | 0 | 0 |
| boya kurutma | 8 / 1 / 0 (H2 index.html:696) | 1 / 0 / 0 | 0 | 0 | 0 |
| bursa | 5 / 0 / 0 (yerel title 1) | 6 / 0 / 1 | 2 / 0 / 0 | 1 / 0 / 0 | 0 |
| rezistans (kök) | 18 / 0 / 0 | 5 / 0 / 0 | 1 / 0 / 0 | 2 / 0 / 1 | 0 |
| eşanjör (kök) | 22 / 1 / 0 | 3 / 0 / 0 | 1 / 0 / 0 | 2 / 0 / 1 | 1 / 0 / 0 (yerel 3/1/1) |
Sonuç: 8 hedef kelime × 5 sayfa = 40 hücrede H1/H2 isabeti 1 (boya kurutma, index). 'Bursa' 34 H2'nin hiçbirinde yok.

## 4. Eski WP URL'leri
/hakkimizda/, /vizyon-misyon/, /urunler-2/, /yonetim/, /inovasyon/, /iletisim/, /referanslar/, /kalite-belgelerimiz/, /kalite-politikamiz/ → 3 deneme (max-time 25/40/90/150 s, UA Mozilla) tamamı curl exit 28 / HTTP 000 (75-150 s yanıt yok). Aynı dakikada statik .html sayfalar 200 (<1 s). HANDOFF: hakkımızda/vizyon metinleri WP'den birebir alındı → statik ve WP sürümü aynı içerik.

## 5. Güven sinyali envanteri (DOSYA:SATIR)
- Belgeler: hakkimizda.html:571-583 (build-pages.py:229-240) — 7 madde metin; belge no/PDF/geçerlilik 0.
- Referanslar: index.html:772 tek <p>, 27 isim; başka sayfada 0; sektör grubu 0; logo 0 (izin yok, doğru karar).
- İletişim: index.html:812-832 (#iletisim: adres, 2 tel, faks, e-posta, Instagram, LinkedIn kişisel profil), urunler.html:335 (tel+mail), hakkimizda/vizyon/fabrika gövde ve footer'da adres/tel 0; iletisim.html yok (sitemap.xml 5 URL).
- JSON-LD: index.html:18-33 Organization (address, telephone, email, sameAs, brand, knowsAbout var; contactPoint/geo/openingHours/faxNumber/hasCredential yok); hakkimizda AboutPage, vizyon WebPage, urunler CollectionPage+Breadcrumb+ItemList(36 name-only), fabrika VideoObject (yerel).
- Yönetici unvanı: hakkimizda.html:549 'Yönetim Kurulu Başkanı' vs vizyon-misyon.html:536 'Genel Müdür' (kaynak build-pages.py:207/306).
- Sayaçlar ham HTML: index.html:587-590, hakkimizda.html:495-498 → '0 yıl / 0 marka / 0 / %0'.
- Haber tarihleri: index.html:805-807 <time> datetime yok.
- Görsel alt: index 35/35 dolu; hakkımızda 6/6; vizyon 6/6; urunler 5 img, 3 boş alt (:319, :324, :329 — aria-hidden dekoratif logo, KABUL); fabrika 2/2.

## 6. Ölçüm yöntemi
Canlı HTML `curl -sL -A Mozilla` → scratchpad; görünür metin Python regex (script/style/noscript/template/svg/yorum sil, tag→boşluk, html.unescape); Türkçe küçük harf (I→ı, İ→i) ile sayım; yerel dosyalar aynı betikle (`~/isisah-scroll-world/*.html`). Title/desc uzunlukları `len()` (kod noktası). Önerilen 5 title 56-60 kr, 5 desc 152-154 kr doğrulandı. Şirket hakkında sitede olmayan hiçbir sayısal iddia yazılmadı; belirsiz teknik iddialar [ONAY] işaretli.


## sema-2
**Skor:** Şema olgunluğu 34/100 — Sözdizimi: 4/5 canlı sayfada JSON-LD geçerli (python json.loads OK), fabrika.html canlıda 0 blok. Tip kapsaması: var olanlar Organization (index), AboutPage+Organization (hakkimizda), WebPage+Organization (vizyon-misyon), CollectionPage+BreadcrumbList+ItemList (urunler); yok olanlar VideoObject, Product (0/36), FAQPage, LocalBusiness, WebSite (yalnızca urunler'de ve yanlış kök URL ile). Varlık birleştirme: 0 — hiçbir düğümde @id yok, Organization 3 farklı içerikle 4 URL'de tekrar ediyor. Google zengin sonuç uygunluğu: 1/6 tip (yalnız Breadcrumb; logo 340×105 px Organization logo şartını sağlamaz). Not: denetim sırasında 12:00–12:06 (+03) sunucu iki bağımsız noktadan erişilemezdi (TCP 80/443 kapalı, WebFetch ECONNREFUSED 46.20.7.162:443).


### Kritik
- SUNUCU ERİŞİLEMEZ (12:00–12:06 +03, 8 Eyl 2026): https://isisah.com.tr → Mac'ten TCP 80 ve 443 kapalı/timeout (nc -z 46.20.7.162 443 → başarısız; curl exit 28), Anthropic WebFetch servisinden de 'connect ECONNREFUSED 46.20.7.162:443'. 11:5x'te aynı HTML sayfalar 0,7 s'de 200 dönüyordu. İki farklı IP'den aynı sonuç → tek IP rate-limit'ten çok gerçek kesinti/hosting sorunu (Birhost Plesk). Googlebot 5xx/timeout görürse tarama hızını düşürür; GSC 'Tarama istatistikleri' ve Plesk/fail2ban loglarını kontrol et, ücretsiz bir uptime monitörü (UptimeRobot vb.) kur. [ONAY: kesintinin süresi ve nedeni]
- AYNI ORGANIZATION 3 FARKLI TANIM, @id YOK: index.html:18–30 (logo, image, knowsAbout var; brand adları 'ISIŞAH Endüstriyel'/'BORŞAH Boru'; sameAs listesinde kendi domaini 'https://isisah.com.tr' — sameAs yalnız dış profil URL'leri için) ↔ tools/build-pages.py:147 ORG sabiti → hakkimizda.html:18 (AboutPage.mainEntity) ve vizyon-misyon.html:18 (WebPage.about): logo/image yok, brand 'ISIŞAH ENDÜSTRİYEL'/'BORŞAH BORU', iç içe gereksiz ikinci @context. Ayrıca /showroom/ ham kopyaları aynı bloğu 4. ve 5. kez yayınlıyor. Google bunları tek varlık olarak birleştiremez → Knowledge Panel/marka sinyali bölünür. Düzeltme: hazir_kod §1'deki tek düğüm (@id https://isisah.com.tr/#organization) HER sayfada birebir aynı içerikle tekrar eder (Google sayfalar arası @id çözmez).
- fabrika.html CANLI: 0 JSON-LD, <title> 'Fabrika Turu — ISIŞAH GROUP' (satır 6), H1 yok. Repo fabrika.html:7'de VideoObject ve :100'de <h1 class="fh1"> ZATEN HAZIR ama deploy edilmemiş (git status: M fabrika.html; canlı md5 8be96c5a ≠ repo). Repo bloğundaki eksikler: uploadDate saat dilimsiz ('2026-08-29' kabul edilir ama ISO 8601+TZ önerilir), width/height/encodingFormat yok, embedUrl sayfanın kendisine işaret ediyor (oynatıcı URL'si değil — kaldır), publisher @id'siz. Doğrulama: ffprobe assets/img/fabrika-scrub.mp4 → 52,08 s (PT52S ✓), 1440×810 h264 ✓; thumbnail og-cover.jpg 1200×630 ✓ (Google min 60×30).
- urunler.html CANLI :18 CollectionPage — isPartOf.WebSite.url = 'https://isisah.com.tr/showroom/' ve breadcrumb 1. öğe 'Ana Sayfa' → '/showroom/' (kopya URL'ye işaret ediyor; canonical köke gitmeli). Repo'da köke düzeltilmiş (urunler.html:18–25), deploy bekliyor. :27 ItemList: 36 ListItem yalnızca 'name' — Google karusel/ItemList için ListItem.url veya gömülü item.url zorunlu → hiçbir zengin sonuç üretmez, 36 ürün adı Google için bağlantısız metin.
- LOGO ŞARTI SAĞLANMIYOR: assets/img/logo.png 340×105 px, alfa kanallı (canlı: /showroom/assets/img/logo.png; index.html:22 'logo' alanı). Google Organization logo kuralı: en az 112×112 px ve beyaz zeminde okunur → yükseklik 105 < 112, logo zengin sonucu reddedilir. 512×512 dolgulu PNG üret (logo-512.png) ve tüm 'logo' alanlarını ona çevir (hazir_kod §7 komutu).
- PRODUCT MARKUP 0/36: 36 ürün yalnız JS dizilerinde (urunler.html:392 ISISAH_LIST, :444 SALMEX_LIST, :466 BORSAH_LIST) ve ad listesi ItemList'te; hiçbir Product/Brand/manufacturer ilişkisi yok. Kategori sorgusu 0'ın şema ayağı bu. Not: schema.org'da 'Manufacturer' diye bir @type YOK; manufacturer Product üzerinde bir özelliktir → hazir_kod §5 şablonları Product.manufacturer ve brand'i @id ile Organization/Brand düğümlerine bağlar. offers BİLEREK dışarıda (B2B özel üretim; Google Offer'da price zorunlu, fiyatsız Offer = hata, availability:PreOrder da price ister).

### Hızlı kazanımlar
- index.html:18–30 bloğunu hazir_kod §1 @graph (Organization+WebSite+WebPage) ile değiştir; yayınlamadan önce §0 filtre betiğiyle tüm [ONAY] ve '_' ile başlayan anahtarları temizle (geo.latitude gibi alanlarda placeholder metin = doğrulama HATASI).
- tools/build-pages.py:147 ORG sabitini §1'deki Organization düğümünün birebir kopyasıyla değiştir (tek kaynak: tools/schema/org.json okusun), hak_ld/viz_ld'yi §3b'deki @graph biçimine çevir (WebPage + BreadcrumbList), scripti çalıştır → hakkimizda.html/vizyon-misyon.html yeniden üretilir.
- Repo'da bekleyen dosyaları deploy et: fabrika.html (VideoObject+H1), urunler.html (kök URL düzeltmesi), robots.txt (Sitemap: satırı), sitemap.xml (5 URL) → `bash tools/deploy-ftp.sh`; ardından 5 URL'yi Rich Results Test (search.google.com/test/rich-results) ve validator.schema.org'da kontrol et.
- fabrika.html:7 VideoObject'i §4 ile güncelle: uploadDate '2026-08-29T00:00:00+03:00', width 1440, height 810, encodingFormat video/mp4, publisher {@id}; embedUrl'ü kaldır. hasPart/Clip'i YALNIZ §4b '#t=' işleyicisi eklenirse koy (Clip.url'nin sayfada çalışması şart).
- urunler.html:27 ItemList'i ya kaldır ya her ListItem'a 'url' ekle: mevcut hash yönlendirmesi urunler.html:522 `#hol=<anahtar>` (isisah, salmex, borsah, isisah_hvac, isisah_rezistans … ISISAH_CATS :485–500). ItemList.item olarak §5 Product düğümlerini gömmek daha iyi.
- sameAs'tan kendi domainini çıkar (index.html:26); telefonları şemada tutarla: '+90 224 261 05 27' + ikinci hat '+90 224 443 61 00' (index.html:822'de var, hiçbir şemada yok) + faxNumber '+90 224 261 01 77' (index.html:823) — §1'de hazır.
- tools/smoke-test.sh'a §8 JSON-LD kontrolünü ekle (şu an ld+json/schema kontrolü yok) — deploy sonrası her sayfada blok sayısı + json.loads + @id varlığı otomatik doğrulansın.

### Orta vade
- LocalBusiness KARARI (öneri): ayrı @graph düğümü değil, TEK düğümde çoklu tip ["Organization","LocalBusiness"] (§1'de böyle). Ayrı düğüm = varlık bölünmesi; 'Manufacturer' tipi yok. Ama LocalBusiness tipini yalnız geo (lat/lon), openingHoursSpecification [ONAY] dolduğunda ve Google Business Profile ile ad-adres-telefon birebir eşleştiğinde bırak; GBP yoksa önce aç (Bursa 'rezistans üreticisi' yerel paket). Doldurulamazsa @type'ı yalnız 'Organization' yap — Rich Results Test LocalBusiness için priceRange/geo uyarısı verir (B2B'de priceRange anlamsız, boş bırak).
- 36 ürün için Product JSON-LD + kalıcı URL: urunler.html hash desteği hol seviyesinde (#hol=…), ürün seviyesinde yok → `#hol=salmex&urun=<slug>` işleyicisi ekle ya da statik /urunler/<slug>.html sayfaları üret (indekslenebilir URL 5 → 41; rakip 142–888). Her sayfaya §5 şablonu + §3 breadcrumb (Ana Sayfa → Marka → Ürün) + görsel (assets/products/*.webp 800×600 mevcut; Google ürün görseli için ≥1200 px geniş önerilir).
- FAQ gerçekçilik notu: Ağustos 2023'ten beri Google FAQ zengin sonucunu yalnız yetkili kamu/sağlık sitelerinde gösteriyor → isisah için SERP kazancı beklenmez; değeri AI Overviews/LLM anlama tarafında. Soru-cevaplar sayfada GÖRÜNÜR olmalı (index.html'e #sss bölümü; görünmeyen FAQ = yapılandırılmış veri spam politikası ihlali). Cevaplar [ONAY].
- hasCertification: schema.org v30.0'da (2026-03) 'pending' değil, Organization/Product/Service'te geçerli, 10K–100K domain kullanıyor; Google zengin sonuç göstermez ama varlık/güven sinyali. Sertifika no ve kapsam [ONAY] gelince aynı Certification öğelerini ilgili Product düğümlerine de bağla (VDE 1997 ve UL 2010 hangi rezistans grupları için — hakkimizda.html:518–523 tarihçe kaynağı). Yıllar (TSE 1988, VDE 1997, ISO 9001 2004, UL 2010) eski WP listesinden; ISO 9001:2008 tarama görselleri bilerek konmamış (site 9001:2015 diyor) — güncel belge PDF'i eklenirse `url` alanı aç.
- Eski WP sayfalarında (/hakkimizda/, /vizyon-misyon/, /urunler-2/) Yoast/WP Organization–WebSite JSON-LD çakışması DOĞRULANAMADI (sunucu kapalıydı). Sunucu açılınca: `curl -s https://isisah.com.tr/hakkimizda/ | grep -c 'ld+json'` — 0'dan büyükse aynı kuruluş iki farklı tanımla yayında; WP dosyalarına dokunulmaz kuralı gereği çözüm nginx/Plesk 301 (kullanıcı kararı) veya WP sayfalarına noindex.
- Video 'Key moments': §4b '#t=' işleyicisi + Clip listesi (7 bölüm, fabrika.html:115–121 caption zamanlamalarından türetildi, ±1 s [ONAY]). Sunucu açılınca fabrika-scrub.mp4 için `Content-Type: video/mp4`, Accept-Ranges ve robots engeli olmadığı doğrulanmalı (bu turda 000/timeout). Video 15,9 MB — Googlebot indirir, sorun değil; ayrıca video sitemap girdisi (sitemap.xml'e <video:video>) ekle.
- Ürün gamlarını (ISISAH_CATS 8 gam, urunler.html:485–500) Organization.hasOfferCatalog → OfferCatalog (fiyatsız, itemListElement: Product @id'leri) olarak yapılandır; knowsAbout metin listesinin yerini yapısal katalog alsın.
- www DNS ve http→https 301 (ilk tur bulgusu) çözülünce şemadaki tüm URL'ler zaten https://isisah.com.tr/ kökünde — değişiklik gerekmez; ama @id'ler URL'e bağlı olduğu için ileride domain/yol değişirse tools/schema/org.json tek yerden güncellenir.

### Ek alanlar / hazır kod


#### hazir_kod
```
/* ============================================================
   §0 YAYIN ÖNCESİ ZORUNLU FİLTRE — [ONAY] placeholder'ları ve "_" ile başlayan
   not anahtarlarını siler. Placeholder bırakılırsa (örn. geo.latitude metin) Rich
   Results Test HATA verir. Kullanım: python3 tools/schema_filter.py in.json > out.json
   ============================================================ */
import json, sys
def clean(x):
    if isinstance(x, dict):
        out = {}
        for k, v in x.items():
            if k.startswith('_'): continue
            v2 = clean(v)
            if v2 is None: continue
            if isinstance(v2, (dict, list)) and not v2: continue
            out[k] = v2
        return out
    if isinstance(x, list):
        return [c for c in (clean(i) for i in x) if c is not None and not (isinstance(c,(dict,list)) and not c)]
    if isinstance(x, str) and '[ONAY' in x: return None
    return x
print(json.dumps(clean(json.load(open(sys.argv[1], encoding='utf-8'))), ensure_ascii=False, separators=(',',':')))

/* ============================================================
   §1 index.html:18–30 YERİNE — tek Organization düğümü (@id) + WebSite + WebPage.
   AYNI Organization düğümü hakkimizda/vizyon-misyon/urunler/fabrika'da da birebir
   tekrar eder (tools/schema/org.json tek kaynak; build-pages.py:147 ORG buradan okur).
   KARAR: @type ["Organization","LocalBusiness"] tek düğüm (ayrı düğüm varlığı böler).
   geo/openingHours [ONAY] dolmadan yayına alınırsa @type'ı yalnız "Organization" yap.
   ============================================================ */
<script type="application/ld+json">
{
 "@context": "https://schema.org",
 "@graph": [
  {
   "@type": ["Organization", "LocalBusiness"],
   "@id": "https://isisah.com.tr/#organization",
   "name": "ISIŞAH GROUP",
   "legalName": "ISIŞAH Endüstriyel [ONAY: ticaret sicilindeki tam unvan, örn. '... San. ve Tic. Ltd. Şti.']",
   "alternateName": ["ISIŞAH Endüstriyel", "Isışah", "Isisah Group"],
   "url": "https://isisah.com.tr/",
   "logo": {
    "@type": "ImageObject",
    "@id": "https://isisah.com.tr/#logo",
    "url": "https://isisah.com.tr/showroom/assets/img/logo-512.png",
    "contentUrl": "https://isisah.com.tr/showroom/assets/img/logo-512.png",
    "width": 512,
    "height": 512,
    "caption": "ISIŞAH GROUP logosu"
   },
   "image": "https://isisah.com.tr/showroom/assets/img/og-cover.jpg",
   "description": "1982'den bu yana Bursa DOSAB'da sanayi tipi rezistans, endüstriyel fırın, kanal tipi ve mobil ısıtıcılar, demiryolu ve savunma ısıtıcıları (ISIŞAH ENDÜSTRİYEL); Ø6–42 mm paslanmaz çelik boru (BORŞAH BORU) ve yoğuşmalı kombi/kazan için sarmal eşanjör boruları (SALMEX) üreten üretici grup. ISO 9001:2015.",
   "slogan": "Isının gücü, teknolojinin hassasiyeti.",
   "foundingDate": "1982",
   "foundingLocation": { "@type": "Place", "name": "Bursa, Türkiye" },
   "address": {
    "@type": "PostalAddress",
    "streetAddress": "DOSAB Ali Osman Sönmez Cad. No:11",
    "addressLocality": "Osmangazi",
    "addressRegion": "Bursa",
    "postalCode": "16369",
    "addressCountry": "TR"
   },
   "geo": {
    "@type": "GeoCoordinates",
    "latitude": "[ONAY: Google Haritalar'dan enlem, örn. 40.2xxxx]",
    "longitude": "[ONAY: boylam, örn. 29.1xxxx]"
   },
   "hasMap": "https://www.google.com/maps?q=DOSAB%20Ali%20Osman%20S%C3%B6nmez%20Cad.%20No:11%20Osmangazi%20Bursa",
   "telephone": ["+90 224 261 05 27", "+90 224 443 61 00"],
   "faxNumber": "+90 224 261 01 77",
   "email": "info@isisah.com.tr",
   "contactPoint": [
    {
     "@type": "ContactPoint",
     "contactType": "sales",
     "telephone": "+90 224 261 05 27",
     "email": "info@isisah.com.tr",
     "areaServed": ["TR", "[ONAY: ihracat ülkeleri, örn. BE]"],
     "availableLanguage": ["tr", "[ONAY: en]"]
    }
   ],
   "openingHoursSpecification": {
    "@type": "OpeningHoursSpecification",
    "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
    "opens": "[ONAY: 08:00]",
    "closes": "[ONAY: 18:00]"
   },
   "sameAs": [
    "https://www.instagram.com/isisah_group",
    "https://www.linkedin.com/in/isi%C5%9Fah-group-9b45aa125/"
   ],
   "brand": [
    { "@type": "Brand", "@id": "https://isisah.com.tr/#brand-isisah", "name": "ISIŞAH ENDÜSTRİYEL", "url": "https://isisah.com.tr/showroom/urunler.html#hol=isisah", "logo": "https://isisah.com.tr/showroom/assets/catalog/logo-isisah.webp", "description": "Sanayi tipi rezistanslar, endüstriyel fırınlar, kanal tipi ve mobil ısıtıcılar, demiryolu ve savunma sanayi ısıtıcıları." },
    { "@type": "Brand", "@id": "https://isisah.com.tr/#brand-borsah", "name": "BORŞAH BORU", "url": "https://isisah.com.tr/showroom/urunler.html#hol=borsah", "logo": "https://isisah.com.tr/showroom/assets/catalog/logo-borsah.webp", "description": "Dikişli paslanmaz çelik boru; Ø6–42 mm çap, 0,35–2 mm et kalınlığı; tavlı ve kangal boru." },
    { "@type": "Brand", "@id": "https://isisah.com.tr/#brand-salmex", "name": "SALMEX", "url": "https://isisah.com.tr/showroom/urunler.html#hol=salmex", "logo": "https://isisah.com.tr/showroom/assets/catalog/logo-salmex.webp", "description": "Yoğuşmalı kombi ve kazanlar için sarmal eşanjör boruları ve eşanjör üniteleri." }
   ],
   "hasCertification": [
    { "@type": "Certification", "name": "ISO 9001:2015 Kalite Yönetim Sistemi", "certificationStatus": "https://schema.org/CertificationActive", "issuedBy": { "@type": "Organization", "name": "[ONAY: belgelendirme kuruluşu, örn. TSE / TÜV SÜD]" }, "validFrom": "2004", "certificationIdentification": "[ONAY: sertifika no]", "description": "TS EN ISO 9001 kalite sistem belgesi ilk kez 2004'te alındı; güncel sürüm ISO 9001:2015." },
    { "@type": "Certification", "name": "TSE Türk Standartlarına Uygunluk Belgesi", "certificationStatus": "https://schema.org/CertificationActive", "issuedBy": { "@type": "Organization", "name": "Türk Standardları Enstitüsü", "url": "https://www.tse.org.tr/" }, "validFrom": "1988", "certificationIdentification": "[ONAY: belge no]" },
    { "@type": "Certification", "name": "VDE — DIN EN normlarına uygunluk sertifikaları", "certificationStatus": "https://schema.org/CertificationActive", "issuedBy": { "@type": "Organization", "name": "VDE Prüf- und Zertifizierungsinstitut", "url": "https://www.vde.com/" }, "validFrom": "1997", "certificationIdentification": "[ONAY: VDE dosya no]", "description": "[ONAY: kapsam — hangi rezistans/ısıtıcı grupları]" },
    { "@type": "Certification", "name": "UL — ABD standartlarına uygunluk sertifikası", "certificationStatus": "https://schema.org/CertificationActive", "issuedBy": { "@type": "Organization", "name": "UL Solutions", "url": "https://www.ul.com/" }, "validFrom": "2010", "certificationIdentification": "[ONAY: UL dosya no, örn. E-xxxxxx]", "description": "[ONAY: kapsam]" }
   ],
   "_alternatif_hasCredential": "Doğrulayıcı hasCertification'ı tanımazsa her öğeyi {\"@type\":\"EducationalOccupationalCredential\",\"credentialCategory\":\"certification\",\"name\":…,\"recognizedBy\":issuedBy,\"dateCreated\":validFrom} yap ve anahtarı hasCredential'a çevir.",
   "areaServed": [
    { "@type": "Country", "name": "Türkiye", "identifier": "TR" },
    { "@type": "Country", "name": "[ONAY: Belçika — MERAK Brüksel projesi ihracat referansı (index.html:739); diğer ihracat ülkeleri]" }
   ],
   "knowsAbout": ["endüstriyel rezistans", "sanayi tipi rezistans", "flanş rezistans", "endüstriyel fırın", "kanal tipi elektrikli ısıtıcı", "mobil elektrikli ısıtıcı", "klima santrali ısıtıcısı", "demiryolu araç ısıtıcısı", "ray ve makas ısıtıcısı", "savunma sanayi blast heater", "paslanmaz çelik boru", "dikişli paslanmaz boru", "tavlı kangal boru", "yoğuşmalı ısı eşanjörü", "sarmal eşanjör borusu", "kombi eşanjörü", "oto boya kurutma"],
   "naics": "[ONAY: 333414 (ısıtma ekipmanı) / 331210 (çelik boru)]",
   "vatID": "[ONAY: TR vergi no]",
   "numberOfEmployees": { "@type": "QuantitativeValue", "value": "[ONAY]" }
  },
  {
   "@type": "WebSite",
   "@id": "https://isisah.com.tr/#website",
   "url": "https://isisah.com.tr/",
   "name": "ISIŞAH GROUP",
   "inLanguage": "tr",
   "publisher": { "@id": "https://isisah.com.tr/#organization" }
  },
  {
   "@type": "WebPage",
   "@id": "https://isisah.com.tr/#webpage",
   "url": "https://isisah.com.tr/",
   "name": "Endüstriyel Rezistans, Isı Eşanjörü ve Paslanmaz Boru Üreticisi | ISIŞAH GROUP Bursa",
   "isPartOf": { "@id": "https://isisah.com.tr/#website" },
   "about": { "@id": "https://isisah.com.tr/#organization" },
   "primaryImageOfPage": "https://isisah.com.tr/showroom/assets/img/og-cover.jpg",
   "inLanguage": "tr"
  }
 ]
}
</script>

/* ============================================================
   §2 KARAR NOTU — LocalBusiness / "Manufacturer"
   - schema.org'da Manufacturer @type'ı YOK; manufacturer = Product özelliği (→ §5).
   - Tek düğüm, çoklu tip ["Organization","LocalBusiness"] önerilir; ayrı @graph düğümü
     (ör. #tesis + parentOrganization) aynı kuruluşu ikiye böler.
   - LocalBusiness'ı GBP (Google Business Profile) NAP'ı ile birebir eşleştir; GBP yoksa önce aç.
   - Rich Results Test LocalBusiness için priceRange/geo/openingHours UYARI verir (hata değil);
     B2B'de priceRange boş kalır. geo+saat [ONAY] dolmazsa @type = "Organization".
   ============================================================ */

/* ============================================================
   §3 BREADCRUMB ŞABLONU — her alt sayfaya (kök → sayfa). Son öğede item opsiyonel.
   ============================================================ */
<script type="application/ld+json">
{
 "@context": "https://schema.org",
 "@type": "BreadcrumbList",
 "@id": "https://isisah.com.tr/hakkimizda.html#breadcrumb",
 "itemListElement": [
  { "@type": "ListItem", "position": 1, "name": "Ana Sayfa", "item": "https://isisah.com.tr/" },
  { "@type": "ListItem", "position": 2, "name": "Hakkımızda", "item": "https://isisah.com.tr/hakkimizda.html" }
 ]
}
</script>
<!-- 3 seviyeli varyant (urunler.html:18 CollectionPage.breadcrumb yerine) -->
<script type="application/ld+json">
{
 "@context": "https://schema.org",
 "@type": "BreadcrumbList",
 "@id": "https://isisah.com.tr/showroom/urunler.html#breadcrumb",
 "itemListElement": [
  { "@type": "ListItem", "position": 1, "name": "Ana Sayfa", "item": "https://isisah.com.tr/" },
  { "@type": "ListItem", "position": 2, "name": "Ürünler", "item": "https://isisah.com.tr/#urunler" },
  { "@type": "ListItem", "position": 3, "name": "3B Showroom", "item": "https://isisah.com.tr/showroom/urunler.html" }
 ]
}
</script>

/* ---- §3b tools/build-pages.py YAMASI (satır 147 ve 252/316) ----
ORG = open('tools/schema/org.json', encoding='utf-8').read().strip()   # §1'deki Organization düğümü (yalnız o obje, @context'siz)
def page_ld(url, name, page_type, crumb_name):
    return ('{"@context":"https://schema.org","@graph":[' + ORG + ','
      '{"@type":"WebSite","@id":"https://isisah.com.tr/#website","url":"https://isisah.com.tr/","name":"ISIŞAH GROUP","inLanguage":"tr","publisher":{"@id":"https://isisah.com.tr/#organization"}},'
      '{"@type":"' + page_type + '","@id":"' + url + '#webpage","url":"' + url + '","name":"' + name + '","inLanguage":"tr",'
      '"isPartOf":{"@id":"https://isisah.com.tr/#website"},"about":{"@id":"https://isisah.com.tr/#organization"},'
      '"breadcrumb":{"@id":"' + url + '#breadcrumb"}},'
      '{"@type":"BreadcrumbList","@id":"' + url + '#breadcrumb","itemListElement":['
      '{"@type":"ListItem","position":1,"name":"Ana Sayfa","item":"https://isisah.com.tr/"},'
      '{"@type":"ListItem","position":2,"name":"' + crumb_name + '","item":"' + url + '"}]}]}')
hak_ld = page_ld("https://isisah.com.tr/hakkimizda.html", "Hakkımızda — ISIŞAH GROUP", "AboutPage", "Hakkımızda")
viz_ld = page_ld("https://isisah.com.tr/vizyon-misyon.html", "Vizyonumuz ve Misyonumuz — ISIŞAH GROUP", "WebPage", "Vizyon & Misyon")
# AboutPage'de "about" yerine "mainEntity" kullanmak istersen page_type=='AboutPage' iken anahtarı değiştir.
---- */

/* ============================================================
   §4 fabrika.html:7 YERİNE — VideoObject (ffprobe doğrulandı: 52,08 s, 1440×810, h264)
   embedUrl KALDIRILDI (sayfanın kendisiydi). hasPart/Clip'i yalnız §4b eklenirse tut.
   ============================================================ */
<script type="application/ld+json">
{
 "@context": "https://schema.org",
 "@type": "VideoObject",
 "@id": "https://isisah.com.tr/showroom/fabrika.html#video",
 "name": "SALMEX sarmal eşanjör üretim hattı — ISIŞAH GROUP fabrika turu (Bursa DOSAB)",
 "description": "ISIŞAH GROUP Bursa DOSAB tesisinde SALMEX sarmal eşanjör üretim hattı: pres, profil hattı, CNC şekillendirme, sarmal sarım, ısıl işlem, robotlu üretim hücreleri ve sızdırmazlık/güç testi. 52 saniyelik kesintisiz üretim filmi.",
 "thumbnailUrl": ["https://isisah.com.tr/showroom/assets/img/og-cover.jpg"],
 "uploadDate": "2026-08-29T00:00:00+03:00",
 "duration": "PT52S",
 "contentUrl": "https://isisah.com.tr/showroom/assets/img/fabrika-scrub.mp4",
 "width": 1440,
 "height": 810,
 "encodingFormat": "video/mp4",
 "inLanguage": "tr",
 "isFamilyFriendly": true,
 "publisher": { "@id": "https://isisah.com.tr/#organization" },
 "about": { "@id": "https://isisah.com.tr/#brand-salmex" },
 "locationCreated": { "@type": "Place", "name": "ISIŞAH GROUP DOSAB tesisi", "address": { "@type": "PostalAddress", "addressLocality": "Osmangazi", "addressRegion": "Bursa", "addressCountry": "TR" } },
 "hasPart": [
  { "@type": "Clip", "name": "Pres — çelik biçim alır", "startOffset": 1, "endOffset": 7, "url": "https://isisah.com.tr/showroom/fabrika.html#t=1" },
  { "@type": "Clip", "name": "Üretim hattı — kesintisiz akış", "startOffset": 8, "endOffset": 14, "url": "https://isisah.com.tr/showroom/fabrika.html#t=8" },
  { "@type": "Clip", "name": "Şekillendirme — CNC hassasiyet", "startOffset": 15, "endOffset": 21, "url": "https://isisah.com.tr/showroom/fabrika.html#t=15" },
  { "@type": "Clip", "name": "Sarmal sarım — SALMEX imzası", "startOffset": 22, "endOffset": 28, "url": "https://isisah.com.tr/showroom/fabrika.html#t=22" },
  { "@type": "Clip", "name": "Isıl işlem", "startOffset": 30, "endOffset": 36, "url": "https://isisah.com.tr/showroom/fabrika.html#t=30" },
  { "@type": "Clip", "name": "Robotlu üretim", "startOffset": 37, "endOffset": 43, "url": "https://isisah.com.tr/showroom/fabrika.html#t=37" },
  { "@type": "Clip", "name": "Sızdırmazlık ve güç testi", "startOffset": 44, "endOffset": 48, "url": "https://isisah.com.tr/showroom/fabrika.html#t=44" }
 ]
}
</script>
<!-- §4b fabrika.html: '#t=<saniye>' derin bağlantı işleyicisi (Clip.url'nin çalışması için). 
     Sayfa hazır olunca scroll ilerlemesini t/52 oranına taşır; SCROLL_H = toplam kaydırma yüksekliği değişkeninin adı sayfadaki ile eşleştirilmeli [ONAY]. -->
<script>
(function(){
  var m=location.hash.match(/^#t=(\d+(?:\.\d+)?)$/); if(!m) return;
  var t=Math.min(52,Math.max(0,parseFloat(m[1])));
  function go(){ var h=document.documentElement.scrollHeight-window.innerHeight; window.scrollTo(0,h*(t/52)); }
  if(document.body.classList.contains('ready')) go(); else { var w=setInterval(function(){ if(document.body.classList.contains('ready')){clearInterval(w);setTimeout(go,300);} },200); }
})();
</script>

/* ============================================================
   §5 PRODUCT ŞABLONU — 3 örnek. offers BİLEREK YOK:
   B2B projeye özel üretim, liste fiyatı yok. Google Offer'da price zorunlu → fiyatsız Offer
   veya availability:PreOrder+fiyatsız = HATA. offers/review/aggregateRating olmadan Product
   zengin sonucu çıkmaz ama markup geçerli; varlık/LLM anlama ve Brand↔manufacturer bağı için
   değerli. Teklif akışı = Organization.contactPoint(sales). Kaynak alanlar: urunler.html:409–410
   (kanal), :445–446 (salmex), :467–468 (boru). Görseller: assets/products/{kanal,salmex,boru}.webp
   (800×600 / 900×645 / 800×600 — mevcut). url: mevcut hash yönlendirmesi urunler.html:522 (#hol=…).
   ============================================================ */
<script type="application/ld+json">
{
 "@context": "https://schema.org",
 "@type": "Product",
 "@id": "https://isisah.com.tr/showroom/urunler.html#salmex-yogusmali-isi-esanjoru",
 "name": "Yoğuşmalı Isı Eşanjörü (Sarmal Eşanjör Borusu)",
 "alternateName": "Condensing Heat Exchanger",
 "description": "Yoğuşmalı kombi ve kazanlar için paslanmaz çelik sarmal eşanjör borusu; yüksek verimli, farklı kapasitelerde yoğuşmalı tasarım. Bursa DOSAB'daki robotlu üretim hattında üretilir; her ünite hat çıkışında sızdırmazlık testinden geçer.",
 "image": ["https://isisah.com.tr/showroom/assets/products/salmex.webp"],
 "url": "https://isisah.com.tr/showroom/urunler.html#hol=salmex",
 "sku": "[ONAY: dahili ürün kodu]",
 "category": "Isı Eşanjörleri > Yoğuşmalı Eşanjör",
 "brand": { "@id": "https://isisah.com.tr/#brand-salmex" },
 "manufacturer": { "@id": "https://isisah.com.tr/#organization" },
 "material": "Paslanmaz çelik",
 "audience": { "@type": "BusinessAudience", "name": "Kombi ve kazan üreticileri (OEM)" },
 "additionalProperty": [
  { "@type": "PropertyValue", "name": "Uygulama", "value": "Yoğuşmalı kombi / kazan" },
  { "@type": "PropertyValue", "name": "Boru tipi", "value": "Sarmal (helisel) eşanjör borusu" },
  { "@type": "PropertyValue", "name": "Kapasite aralığı", "value": "[ONAY: kW aralığı]" },
  { "@type": "PropertyValue", "name": "Test", "value": "Sızdırmazlık testi (her ünite)" }
 ]
}
</script>
<script type="application/ld+json">
{
 "@context": "https://schema.org",
 "@type": "Product",
 "@id": "https://isisah.com.tr/showroom/urunler.html#borsah-paslanmaz-boru",
 "name": "Paslanmaz Çelik Boru Ø6–42 mm (Dikişli, TIG Kaynaklı)",
 "alternateName": "Stainless Steel Tubes",
 "description": "BORŞAH BORU dikişli paslanmaz çelik boru; Ø6–42 mm dış çap, 0,35–2 mm et kalınlığı, TIG kaynak, 70–300 bar test, 9 aşamalı kalite kontrolü. Düz boy, tavlı ve kangal (100–400 m) formlarında; eşanjör, ısıtıcı ve tesisat uygulamaları için.",
 "image": ["https://isisah.com.tr/showroom/assets/products/boru.webp"],
 "url": "https://isisah.com.tr/showroom/urunler.html#hol=borsah",
 "category": "Paslanmaz Çelik Boru > Dikişli Boru",
 "brand": { "@id": "https://isisah.com.tr/#brand-borsah" },
 "manufacturer": { "@id": "https://isisah.com.tr/#organization" },
 "material": "[ONAY: AISI 304 / 316L / 430 vb. kalite]",
 "audience": { "@type": "BusinessAudience", "name": "Eşanjör, ısıtıcı ve tesisat üreticileri" },
 "additionalProperty": [
  { "@type": "PropertyValue", "name": "Dış çap", "minValue": 6, "maxValue": 42, "unitCode": "MMT", "unitText": "mm" },
  { "@type": "PropertyValue", "name": "Et kalınlığı", "minValue": 0.35, "maxValue": 2, "unitCode": "MMT", "unitText": "mm" },
  { "@type": "PropertyValue", "name": "Test basıncı", "minValue": 70, "maxValue": 300, "unitCode": "BAR", "unitText": "bar" },
  { "@type": "PropertyValue", "name": "Kaynak yöntemi", "value": "TIG" },
  { "@type": "PropertyValue", "name": "Kalite kontrol", "value": "9 aşamalı" },
  { "@type": "PropertyValue", "name": "Teslim formu", "value": "Düz boy, tavlı, kangal (100–400 m)" }
 ]
}
</script>
<script type="application/ld+json">
{
 "@context": "https://schema.org",
 "@type": "Product",
 "@id": "https://isisah.com.tr/showroom/urunler.html#isisah-kanal-tipi-isitici",
 "name": "Kanal Tipi Elektrikli Isıtıcı",
 "alternateName": "Duct Type Electric Heater",
 "description": "Klima santrali ve havalandırma kanalları için kanatlı rezistanslı elektrikli kanal ısıtıcısı; dikdörtgen ve yuvarlak kanal tipleri, santral içi ısıtıcı bataryalar. Bursa'da ISO 9001:2015 kapsamında üretilir.",
 "image": ["https://isisah.com.tr/showroom/assets/products/kanal.webp"],
 "url": "https://isisah.com.tr/showroom/urunler.html#hol=isisah_hvac",
 "category": "İklimlendirme (HVAC) > Elektrikli Kanal Isıtıcısı",
 "brand": { "@id": "https://isisah.com.tr/#brand-isisah" },
 "manufacturer": { "@id": "https://isisah.com.tr/#organization" },
 "audience": { "@type": "BusinessAudience", "name": "HVAC yüklenicileri ve klima santrali üreticileri" },
 "additionalProperty": [
  { "@type": "PropertyValue", "name": "Tip", "value": "Dikdörtgen kanal / yuvarlak kanal / santral" },
  { "@type": "PropertyValue", "name": "Isıtıcı eleman", "value": "Kanatlı rezistans" },
  { "@type": "PropertyValue", "name": "Güç aralığı", "value": "[ONAY: kW]" },
  { "@type": "PropertyValue", "name": "Koruma", "value": "[ONAY: çift kademeli termostat / emniyet termostatı]" }
 ]
}
</script>

/* ============================================================
   §6 FAQPage — 6 soru; cevaplar [ONAY]. Sayfada GÖRÜNÜR #sss bölümüyle birlikte yayınla
   (index.html'de #iletisim'den önce). Google FAQ zengin sonucu 2023'ten beri yalnız
   kamu/sağlık sitelerine → SERP kazancı beklenmez; AI Overviews/LLM için değerli.
   ============================================================ */
<script type="application/ld+json">
{
 "@context": "https://schema.org",
 "@type": "FAQPage",
 "@id": "https://isisah.com.tr/#faq",
 "mainEntity": [
  { "@type": "Question", "name": "ISIŞAH GROUP hangi ürünleri üretiyor?", "acceptedAnswer": { "@type": "Answer", "text": "[ONAY]" } },
  { "@type": "Question", "name": "Projeye özel (ölçü ve güce göre) rezistans veya ısıtıcı üretiyor musunuz?", "acceptedAnswer": { "@type": "Answer", "text": "[ONAY]" } },
  { "@type": "Question", "name": "BORŞAH paslanmaz borular hangi çap, et kalınlığı ve kalitelerde üretiliyor?", "acceptedAnswer": { "@type": "Answer", "text": "[ONAY]" } },
  { "@type": "Question", "name": "SALMEX sarmal eşanjör boruları hangi kombi ve kazan tiplerine uygundur?", "acceptedAnswer": { "@type": "Answer", "text": "[ONAY]" } },
  { "@type": "Question", "name": "Hangi kalite belgelerine ve sertifikalara sahipsiniz (ISO 9001, TSE, VDE, UL)?", "acceptedAnswer": { "@type": "Answer", "text": "[ONAY]" } },
  { "@type": "Question", "name": "Teklif nasıl alınır, minimum sipariş ve termin süreleri nedir?", "acceptedAnswer": { "@type": "Answer", "text": "[ONAY]" } }
 ]
}
</script>

/* ============================================================
   §7 LOGO 512×512 (Google: min 112×112, beyaz zeminde okunur). macOS, ImageMagick'siz:
   ============================================================ */
cd ~/isisah-scroll-world && cp assets/img/logo.png assets/img/logo-512.png && sips -p 512 512 --padColor FFFFFF assets/img/logo-512.png >/dev/null && sips -g pixelWidth -g pixelHeight assets/img/logo-512.png
# Logo koyu zemin için beyaz çizilmişse padColor'ı 0D0F12 yap ve ayrıca beyaz zeminli ikinci sürüm üret [ONAY: logo rengi].

/* ============================================================
   §8 tools/smoke-test.sh EK — deploy sonrası JSON-LD doğrulama (mevcut scriptte yok)
   ============================================================ */
for u in / /hakkimizda.html /vizyon-misyon.html /showroom/urunler.html /showroom/fabrika.html; do
  curl -sS -m 30 -A "Mozilla/5.0" "https://isisah.com.tr$u" | python3 -c '
import sys,re,json; h=sys.stdin.read(); b=re.findall(r"<script[^>]*ld\+json[^>]*>(.*?)</script>",h,re.S)
ok=0; ids=0
for x in b:
    try: d=json.loads(x); ok+=1; ids+=("#organization" in json.dumps(d))
    except Exception as e: print("  JSON HATASI:",e)
print(f"'"$u"' blok={len(b)} gecerli={ok} org_id={ids}"); sys.exit(0 if (b and ok==len(b) and ids) else 1)' || echo "  !! $u şema kontrolü BAŞARISIZ"
done

/* ============================================================
   §9 RICH RESULTS UYUMLULUK NOTLARI (özet)
   - Organization: name+url+logo(≥112×112)+sameAs+address+contactPoint → Knowledge Panel/logo sinyali. hasCertification/knowsAbout/naics Google'da görünmez, geçerli schema.
   - LocalBusiness: name+address zorunlu; geo/openingHours/priceRange eksikse UYARI. Tek düğüm çoklu tip kabul edilir.
   - BreadcrumbList: ≥2 öğe, item mutlak URL; son öğede item opsiyonel. Sayfa görünür breadcrumb'la örtüşmeli (header'a görünür breadcrumb ekle).
   - VideoObject: name+thumbnailUrl+uploadDate zorunlu; contentUrl erişilebilir, robots engelsiz, Content-Type video/mp4; Clip → Key moments (url sayfada çalışmalı). Video sayfada görünür olmalı (fabrika.html <video id="film"> ✓).
   - Product: offers/review/aggregateRating olmadan zengin sonuç YOK; markup yine geçerli. Sahte Offer koyma (Merchant/Product politikası).
   - FAQPage: yalnız kamu/sağlık için zengin sonuç; içerik sayfada görünür olmalı, aynı Q&A tek sayfada.
   - Genel: her sayfada Organization düğümü aynı @id ile tam tekrar; @context tek (iç içe @context yok); "_" anahtarları ve [ONAY] yayına çıkmaz (§0).
   ============================================================ */
```

### Kanıt
CANLI JSON-LD ÇEKİMİ (8 Eyl 2026 11:5x +03, curl -A Mozilla, python json.loads): https://isisah.com.tr/ → 1 blok satır 18, GEÇERLİ, @type Organization (logo/image/knowsAbout var; sameAs[0]='https://isisah.com.tr' kendi domaini; @id yok; brand 'ISIŞAH Endüstriyel','SALMEX','BORŞAH Boru'). /hakkimizda.html → 1 blok satır 18, GEÇERLİ, AboutPage.mainEntity=Organization (iç içe ikinci @context; logo/image yok; brand 'ISIŞAH ENDÜSTRİYEL','BORŞAH BORU','SALMEX'; @id yok). /vizyon-misyon.html → 1 blok satır 18, GEÇERLİ, WebPage.about=Organization (hakkimizda ile aynı sabit). /showroom/urunler.html → 2 blok satır 18 (CollectionPage; isPartOf.WebSite.url='https://isisah.com.tr/showroom/'; breadcrumb item1='https://isisah.com.tr/showroom/') ve satır 27 (ItemList numberOfItems 36, tüm ListItem yalnız name, url yok). /showroom/fabrika.html → 0 blok; <title> 'Fabrika Turu — ISIŞAH GROUP' (satır 6); H1 yok; canonical /showroom/fabrika.html (satır 8). REPO (/Users/mehmetcansahin/isisah-scroll-world, HEAD b703c7e, git status: M index/hakkimizda/vizyon-misyon/urunler/fabrika/robots/tools/*): index.html:18–30 Organization inline; tools/build-pages.py:147 ORG sabiti → :252 hak_ld, :316 viz_ld (tek kaynak; hakkimizda.html:18, vizyon-misyon.html:18 üretir); urunler.html:18–25 CollectionPage köke düzeltilmiş (deploy bekliyor), :27 ItemList aynı, :392 ISISAH_LIST / :444 SALMEX_LIST / :466 BORSAH_LIST / :474–478 BRANDS{isisah,salmex,borsah} / :485–500 ISISAH_CATS 8 gam (isisah_hvac 'kanal' içerir) / :522 location.hash '#hol=' yönlendirmesi; :409–410 Kanal Tipi Isıtıcı ('Kanatlı rezistanslı santral, dikdörtgen ve yuvarlak kanal ısıtıcıları'), :445–446 Yoğuşmalı Isı Eşanjörü ('Paslanmaz çelik sarmal eşanjör borusu…'), :467–468 Paslanmaz Borular ('Ø6–42 mm çap, 0,35–2 mm et kalınlığı, 70–300 bar test, 9 kalite kontrolü', chips TIG Kaynak). fabrika.html:7 VideoObject (uploadDate '2026-08-29', duration PT52S, embedUrl=sayfa, width/height yok), :100 <h1 class=\"fh1\">, :101 <video id=\"film\"> src'siz (JS), :149 'fabrika-scrub.mp4?v=2', :115–121 7 caption (Pres, Üretim Hattı, Şekillendirme, Sarmal Sarım, Isıl İşlem, Robotlu Üretim, Test). VARLIKLAR (yerel, sips/ffprobe): assets/img/logo.png 340×105 hasAlpha=yes; assets/img/og-cover.jpg 1200×630; assets/img/fabrika-scrub.mp4 15.924.194 B, h264 1440×810, duration=52.083333 s; assets/products/kanal.webp 800×600, salmex.webp 900×645, boru.webp 800×600; assets/catalog/logo-{isisah,salmex,borsah}.webp mevcut (urunler.html:319–329). SERTİFİKA KAYNAĞI: hakkimizda.html:518 'TSE 1988', :520 'VDE 1997', :522 'TS EN ISO 9001 2004', :523 'UL 2010'; ISO 9001:2015 ifadesi index.html:7,465,845; HANDOFF.md:123 'belge yılları WP listesinden; eski ISO 9001:2008 taramaları bilerek konmadı'. İLETİŞİM KAYNAĞI: index.html:822 tel '+90 224 261 05 27' ve '+90 224 443 61 00', :823 Faks '+90 224 261 01 77', :812 #iletisim Google Maps embed q=DOSAB Ali Osman Sönmez Cad. No:11; ihracat tek kanıt index.html:739 'MERAK Brüksel Projesi: ihracat'. robots.txt (repo) Sitemap satırı var; sitemap.xml (repo) 5 URL — canlı sürümleri bu turda DOĞRULANAMADI. SUNUCU: 12:00–12:06 +03 'nc -z 46.20.7.162 443/80' başarısız, curl exit 28 (15–45 s timeout), WebFetch 'connect ECONNREFUSED 46.20.7.162:443' (sitemap.xml, robots.txt, /hakkimizda/ üçü de); dig isisah.com.tr → 46.20.7.162; www A kaydı yok. Eski WP /hakkimizda/ JSON-LD çakışması ve varlıkların canlı HTTP durumu bu nedenle doğrulanamadı. schema.org/hasCertification (WebFetch, v30.0 2026-03-19): pending değil, Certification tipi, Organization/Person/Place/Product/Service'te kullanılır. ÜRETİLEN PAKET: scratchpad/schema_paketi.json 8 blok, python json.loads GEÇERLİ, 15.295 B, 29 [ONAY] işareti (hepsi §0 filtreyle yayına çıkmadan silinir).


## geo-2
**Skor:** GEO / AI-arama hazırlığı: 2/10 (08 Eyl 2026, 11:50–12:25). Alt kırılım — AI tarayıcı erişimi 1/10 (GPTBot, ClaudeBot, CCBot sunucuda 502 ile anlık reddediliyor; 23 dk tam kesinti ölçüldü) · makine-okunur içerik 4/10 (5 sayfada Organization JSON-LD var, ama 38 ürün yalnız JS dizisinde, ItemList sadece "name", sayaçlar HTML'de "0 yıl") · varlık tutarlılığı 3/10 (grup sitelerinde 1978 vs 1982, No:11/B vs No:11, ŞAHTERM ilişkisi, legalName eksik; Wikidata/Wikipedia yok) · alıntılanabilirlik 4/10 (hakkımızda metni iyi, ama "X nedir?" cevabı veren tek-cümle pasajlar yok, llms.txt yok — 2 rakipte var) · görünürlük baseline 0/10 (3 test sorgusunda 0/3; marka+kategori sorgusunda bile isisah.com.tr ilk 9'da yok).


### Kritik
- SUNUCU AI BOTLARINI 502 İLE REDDEDİYOR — https://isisah.com.tr/robots.txt (ve /hakkimizda.html) için User-Agent GPTBot → 502, ClaudeBot → 502 (0,039 s, anlık), CCBot → 502; aynı saniyede PerplexityBot → 200, Google-Extended → 200, Chrome → 200. İki ayrı zamanda doğrulandı (08:53 UTC 3/3 ve 09:22 UTC 1/1). 502 gövdesi nginx standart sayfası (content-length 150) → Plesk nginx ek direktifi veya ModSecurity 'drop' kuralı (Birhost seviyesi). robots.txt'te izin vermenin hiçbir etkisi olmaz; ChatGPT (GPTBot/OAI-SearchBot ailesi), Claude ve Common Crawl (LLM eğitim verisinin ana kaynağı) siteyi hiç göremiyor. DÜZELTME [ONAY — sunucu ayarı]: Plesk → isisah.com.tr → 'Apache & nginx Ayarları → Ek nginx direktifleri'nde user-agent koşullu return/deny satırı var mı bak; yoksa 'Web Application Firewall (ModSecurity)' loglarında GPTBot/ClaudeBot/CCBot ara; bulunamazsa Birhost'a ticket: 'GPTBot, ClaudeBot, CCBot user-agent'ları 502 alıyor, engel kaldırılsın'. Doğrulama: curl -sI -A 'ClaudeBot/1.0' https://isisah.com.tr/robots.txt | head -1 → HTTP/2 200 beklenir. smoke-test.sh'a ekle (hazir_kod §5).
- SUNUCU 23 DAKİKA TAMAMEN ERİŞİLEMEZ OLDU — 11:58–12:21 (yerel) arası Mac'ten tüm istekler zaman aşımı (000), Anthropic WebFetch 'connect ECONNREFUSED 46.20.7.162:443', FTP 21 de cevapsız → IP yasağı değil, sunucu çöktü. Öncesinde de kök sayfa GET >60 s (robots.txt 0,5 s). AI tarayıcılar 5–10 s zaman aşımıyla çalışır; bu sunucuda kök sayfayı çoğu zaman alamazlar. Aynı makinede PHP 5.6.40 + WordPress 4.8 çalışıyor (x-powered-by başlıkları). DÜZELTME [ONAY]: Birhost'a arıza kaydı + ücretsiz uptime izleme (UptimeRobot, 5 dk, / ve /robots.txt); orta vadede statik siteyi WP'den ayrı bir statik host/CDN önüne alma kararı.
- CANLI robots.txt WORDPRESS'İN SANAL DOSYASI — https://isisah.com.tr/robots.txt başlıkları: x-powered-by PHP/5.6.40, link <…/wp-json/>, Set-Cookie PHPSESSID, Cache-Control no-store → PHP üretiyor; gövde WP varsayılanı (User-agent: * / Disallow: /wp-admin/ / Allow: admin-ajax.php), Sitemap satırı YOK. Repo /Users/mehmetcansahin/isisah-scroll-world/robots.txt:5'teki Sitemap satırı commit cd3b9b9 (08 Eyl 11:59) ile eklendi ama henüz deploy edilmedi (kök <title> da hâlâ eski: 'ISIŞAH ENDÜSTRİYEL — Isının gücü…' — repo index.html:6'daki anahtar kelimeli title canlıda değil). DÜZELTME: bash tools/deploy-ftp.sh çalıştır; ardından curl -sI https://isisah.com.tr/robots.txt → content-type text/plain ve x-powered-by OLMAMALI. Hâlâ PHP üretiyorsa fiziksel dosya isteğe rağmen WP'ye gidiyor demektir → nginx 'location = /robots.txt { try_files $uri =404; }' kararı kullanıcıda. robots.txt'e AI bot bölümü ekle (hazir_kod §2).
- llms.txt YOK (404) — https://isisah.com.tr/llms.txt, /llms-full.txt, /ai.txt → 404. Rakiplerden isierrezistans.com/llms.txt (200, 7.469 B, 7 bölüm, ~70 link, 'Contact & Notes for AI Systems') ve isielektrik.com.tr/llms.txt (200, 7.757 B, 'Priority SEO/GEO Keywords', 'Notes for AI Assistants') mevcut; bursarezistans/baykal/safir/ser/sg yok. DÜZELTME: hazir_kod §1'deki dosyayı repo köküne llms.txt olarak koy; tools/deploy-ftp.sh:11 set'ine 'llms.txt' ekle ve satır 52'den sonra köke yükleyen curl satırını ekle (hazir_kod §5); [ONAY] işaretli 3 satırı onaylayıp işareti sil.
- VARLIK (ENTITY) ÇELİŞKİLERİ — LLM'ler bugün şirket için 1978 diyor: WebSearch özeti 'ISIŞAH A.Ş. was established in 1978 by Mehmet Şahin' (kaynak: rezistansdunyasi.com/Hakkimizda — 'ISIŞAH GROUP/ ISI ŞAH END REZS SAN TİC A.Ş' imzalı, gruba ait görünen site: '1978 yılında Yönetim Kurulu Başkanı Mehmet Şahin tarafından kurulan ISIŞAH A.Ş.', adres 'No:11/B', 'ISI ŞAH GROUP çatısı altındaki ŞAH TERM'). Yeni site: 1982, No:11, ŞAHTERM yok (HANDOFF.md:123 'ŞAHTERM çıkarıldı'). Ayrıca index.html:20 ve tools/build-pages.py:147 legalName 'ISIŞAH Endüstriyel' — ticaret sicili/LinkedIn/GSC sorgusu: 'ISI-ŞAH ENDÜSTRİYEL REZİSTANS VE ISI EKİPMANLARI SANAYİ TİCARET A.Ş.'; sameAs'teki LinkedIn URL'si /in/ (kişisel profil tipi). firmabulucu: SALMEX ISI SAN. VE TİC. A.Ş. aynı adres, tel (224) 271 24 70 (sitede 261 05 27). DÜZELTME [ONAY — her madde patron kararı]: (a) 1978/1982 için tek resmi ifade (ör. '1978'de aile şirketi olarak başladı, ISIŞAH markası 1982' veya sadece 1982) ve rezistansdunyasi.com'un aynı metne çekilmesi; (b) hakkımızda'ya ŞAHTERM ilişkisini tek cümlede anlatan pasaj (hazir_kod §3 P12); (c) JSON-LD legalName tam unvan + sameAs Facebook + Salmex telefonu (hazir_kod §4).
- ÜRÜNLER AI TARAYICILARINA GÖRÜNMEZ — urunler.html:393-471 ISISAH_LIST (25) + SALMEX_LIST (10) + BORSAH_LIST (3) = 38 ürün yalnız JS dizisinde; GPTBot/ClaudeBot/PerplexityBot JS çalıştırmaz; sayfanın görünür statik metni lobby metinleri (urunler.html:315-330, ~133 kelime). urunler.html JSON-LD ItemList numberOfItems 36 (JS'teki 38 ile UYUMSUZ) ve her ListItem yalnız {"name"} — description/brand/url yok. DÜZELTME: ItemList'i JS dizilerinden üret (Product + description + brand + url#hol=, hazir_kod §4b) ve lobby altına statik <section id="urun-listesi"> ile 38 ürünün marka-gam-ad-açıklama listesini koy (görünür, CSS ile küçük; <noscript> DEĞİL — bazı AI tarayıcılar noscript'i atar).
- SAYAÇLAR JS'SİZ OKUMADA '0' — index.html:587-590 stats bloğu HTML'de '0 yıl Kesintisiz Üretim', '0 marka', '%0 Yerli Üretim' (data-count ile JS 881. satırda animasyon). JS çalıştırmayan AI tarayıcı sayfadan 'ISIŞAH: 0 yıl kesintisiz üretim, %0 yerli üretim' cümlesini çıkarır. DÜZELTME: nihai değerleri metin olarak yaz (hazir_kod §4c); JS zaten 0'dan sayarak üzerine yazıyor.
- TEST SORGULARINDA 0/3 GÖRÜNÜRLÜK + MARKA KARIŞMASI — 'Bursa'da sanayi tipi rezistans üreticisi': bursarezistans, aymet, sgrezistans, basakisi, baykalrezistans, termorezistans, isierrezistans (ISIŞAH yok). 'yoğuşmalı kombi eşanjörü üreticisi Türkiye': kombiparcadeposu, ecostar, yedepa, dragonn, teknikparca, termoline, parcabayim, yedek-parcam (SALMEX yok; SERP yedek parça perakendecileriyle dolu → hedef sorguyu 'yoğuşmalı eşanjör OEM/üretici' + 'kombi eşanjörü imalatçısı' olarak da izle). 'demiryolu araç ısıtıcısı üreticisi': vvkb (×4), imkar, railwayturkey firma-ara, lojistikhatti (ISIŞAH yok; railwayturkey.com/isisah/ profili var ama çıkmıyor). Marka+kategori 'Isışah endüstriyel rezistans Bursa': 1. facebook.com/isisahcomtr, isisah.com.tr ilk 9'da YOK. 'site:isisah.com.tr': Google Wikipedia 'Isis/ISIS' sayfalarını karıştırdı ve indekste yalnız eski WP URL'leri (/iletisim/, /urunler-2/, /yonetim/, /english/aboutus/) 'ISIŞAH ENDÜSTRİ' başlığıyla görünüyor. DÜZELTME: llms.txt 'Yapay zekâ notları' bölümündeki ad-varyantları + 'ISIS ile ilgisi yok' satırı; pasajlar (§3); ChatGPT/Perplexity/Google AI Overview için manuel protokol (hazir_kod §6) — bugün Google-vekili baseline 0/3; ChatGPT/Perplexity bu ortamdan çalıştırılamadı, ilk manuel ölçüm yapılmalı.

### Hızlı kazanımlar
- Deploy'u çalıştır (bash tools/deploy-ftp.sh) → repo robots.txt (Sitemap satırı) + anahtar kelimeli title'lar canlıya çıkar; ardından robots başlığında x-powered-by yoksa statik dosya kazanmış demektir.
- robots.txt'e açık AI-bot izin bloğu ekle (hazir_kod §2): GPTBot, OAI-SearchBot, ChatGPT-User, ClaudeBot, Claude-SearchBot, Claude-User, anthropic-ai, PerplexityBot, Perplexity-User, Google-Extended, CCBot, Applebot-Extended, Amazonbot, Bytespider, meta-externalagent — hepsi Allow. (Öneri: hepsine izin; içerik B2B tanıtım, gizli veri yok.)
- llms.txt'i yayınla (hazir_kod §1) + deploy-ftp.sh ve smoke-test.sh yamaları (§5). Yayın sonrası curl -s https://isisah.com.tr/llms.txt | head -3.
- 10 (+2) tek-cümle cevap pasajını yerleştir (hazir_kod §3): index.html:467/492/499/506/607/697/712/816, tools/build-pages.py:164/229 (sonra python3 tools/build-pages.py), urunler.html:316, fabrika.html:100. Her pasaj 'Özne + fiil + sayısal olgu' kalıbında, ≤45 kelime.
- index.html:587-590 sayaçlara nihai metin (44 yıl / 3 marka / 8 / %100) — hazir_kod §4c.
- JSON-LD Organization'ı zenginleştir (index.html:19-29, tools/build-pages.py:147, fabrika.html Organization): legalName tam unvan [ONAY yazım], founder Mehmet Şahin [ONAY], sameAs'e Facebook + Instagram + LinkedIn company [ONAY resmi hesaplar], knowsAbout genişletme (12 terim), hasCertification ISO 9001:2015 — hazir_kod §4a.
- urunler.html ItemList'i JS dizilerinden üret: 38 Product, description + brand + url — hazir_kod §4b (build adımı olarak tools/build-pages.py'ye 20 satır eklenebilir).
- Bing Webmaster Tools'a siteyi ekle ('GSC'den içe aktar' tek tık) + IndexNow anahtarı: ChatGPT arama ve Copilot Bing indeksini kullanır; site şu an Bing için de yalnız WP sayfalarıyla var. [ONAY: hesap açma]
- Facebook (facebook.com/isisahcomtr) ve LinkedIn profillerinde 'Hakkında' metnini P1 pasajıyla birebir aynı yap (1982, DOSAB, 3 marka) — LLM'lerin çektiği ilk kaynaklar bunlar.
- İlk manuel AI ölçümü: hazir_kod §6 protokolüyle 3 sorgu × 3 motor; sonucu docs/seo-baseline-2026-09-07.md 'AI alıntı testi' satırına yaz (bugün: Google-vekili 0/3).

### Orta vade
- Gam/ürün sayfaları: 8 ISIŞAH gamı + SALMEX + BORŞAH için gerçek URL'ler (/urunler/rayli-sistemler.html gibi, statik HTML; tek JSON kaynağından üretim — HANDOFF yol haritasıyla aynı). Her sayfa: tek-cümle tanım pasajı, teknik tablo, 3-5 soruluk SSS (FAQPage JSON-LD), showroom #hol= bağlantısı. Hedef: 5 → 20+ indekslenebilir URL (rakipler 142–888).
- Wikidata öğesi oluştur [ONAY — kamuya açık içerik]: Wikipedia için kayda değerlik yok (arama 0 sonuç), Wikidata eşiği düşük. Kaynaklar hazır: anadoluraylisistemler.org/isisah-firmasi-97 (1982, ISO 9001, adres), railwayturkey.com/isisah/, dosabsiad.org.tr firma PDF'i, ekohaber.com.tr 05.06.2023 (Salmex yatırım haberi), find.com.tr ticaret unvanı. Özellikler: instance of=business, inception=1982, HQ=Bursa, industry=heating equipment, official website, brands (Salmex, Borşah ayrı öğe olabilir). Ayrıca 'Demirtaş, Osmangazi' TR Wikipedia maddesi var — DOSAB firmaları listesi varsa doğal atıf yeri (düzenleme kararı patronda).
- Üçüncü taraf tutarlılık turu: railwayturkey, anadoluraylisistemler, turkosb, placedigger, find.com.tr, firmabulucu profillerinde aynı NAP + aynı kuruluş yılı; rezistansdunyasi.com 'Hakkımızda' metninin yeni siteyle hizalanması; LinkedIn kişisel-profil yerine şirket sayfası. AI cevapları ağırlıkla bu dizinlerden besleniyor.
- İngilizce katman: llms.txt'e '## English' bölümü + /en/ sayfaları (hreflang). Rakip llms.txt'ler İngilizce; ihracat referansları (MERAK Brüksel, Bükreş, Kayseri-Bozankaya) İngilizce sorgularda hiç yok.
- Eski WP URL'leri için 301 kararı [kullanıcı kararı, WP dosyalarına dokunulmaz]: Google indeksi ve LLM'ler hâlâ /hakkimizda/, /urunler-2/, /english/aboutus/ içeriğini ('30 years', ŞAHTERM) okuyor. 301 olmayacaksa en azından yeni sayfalarda canonical + llms.txt'teki 'arşiv' notu kalsın.
- Haber/vaka içeriği üretimi: 'SALMEX robotlu eşanjör hattı' ve 'ERP uyumlu %100 yerli yoğuşmalı kombi projesi' (ekohaber 2023'te var) için basın bülteni + sektör portalları (railwayturkey, makinegundemi). AI Overview/Perplexity alıntıları çoğunlukla üçüncü taraf haberlerden gelir.
- Altyapı: statik siteyi WP/PHP 5.6 sunucusundan ayır (ayrı statik host veya Cloudflare önü; HSTS, Cache-Control, http→https ve www 301 aynı pakette). 23 dk kesinti ve >60 s TTFB devam ederse hiçbir GEO çalışması tarayıcıya ulaşmaz.
- Ölçüm ritmi: 30 günde bir §6 protokolü (3 sorgu × ChatGPT / Perplexity / Google AI Overview) + GSC kategori sorgu gösterimi + Bing WMT; sonuçları docs/ altında tarihli tabloya ekle. ClaudeBot/GPTBot 200 kontrolü smoke-test'te kalıcı.

### Ek alanlar / hazır kod


#### hazir_kod
```
===== §1 · llms.txt (repo köküne koy; [ONAY] satırlarını onayla/sil) =====
# ISIŞAH GROUP

> ISIŞAH GROUP, 1982'de Bursa'da kurulan, Bursa DOSAB (Demirtaş Organize Sanayi Bölgesi) merkezli bir ısıtma teknolojisi üreticisidir. Üç markası vardır: ISIŞAH ENDÜSTRİYEL (sanayi tipi rezistans ve endüstriyel ısıtma sistemleri), BORŞAH BORU (paslanmaz çelik dikişli boru, Ø6–42 mm) ve SALMEX (kombi ve kazan ısı eşanjörleri). ISO 9001:2015 belgelidir.

## Kimlik
- Ticari unvan: ISIŞAH Endüstriyel Rezistans ve Isı Ekipmanları San. Tic. A.Ş. [ONAY: tam unvan ve yazım]
- Kuruluş: 1982 (ISIŞAH markası) · 1995 entegre tesis, seri üretim · 2003 sanayi tipi özel üretim için ayrı tesis · 2011 ISIŞAH GROUP çatısı
- Adres: DOSAB Ali Osman Sönmez Cad. No:11, 16369 Osmangazi / Bursa, Türkiye
- Telefon: +90 224 261 05 27 · E-posta: info@isisah.com.tr
- Yönetim Kurulu Başkanı: Mehmet Şahin
- Belgeler: TS EN ISO 9001:2015 (ISO 9001: 2004'ten beri) · TSE (1988) · VDE / DIN EN (Almanya, 1997) · UL (ABD, 2010) · CE (EN 60204-1) · RoHS uyumlu malzeme

## Markalar ve ürün gamları

### ISIŞAH ENDÜSTRİYEL — sanayi tipi rezistans ve ısıtma sistemleri
- Endüstriyel rezistanslar: özel tip flanş rezistansları, konveksiyonel fırın rezistansları, yassı rezistanslar (fritöz, makarna haşlama), bulaşık makinesi ve defrost rezistansları, proses ısıtıcı üniteleri
- Endüstriyel fırınlar
- İklimlendirme (HVAC): kanal tipi elektrikli ısıtıcı, silindirik kanal fan ısıtıcısı, klima santrali (AHU) ısıtıcısı, fan-coil / ortam ısıtıcısı, mobil elektrikli ısıtıcı
- Raylı sistemler (1986'dan bu yana): tren, tramvay ve metro klima (HVAC) ısıtıcıları; yolcu ve koltuk altı ısıtıcıları; TIJ (pencere altı) kasaları; şasi ısıtıcıları; ray ve makas ısıtıcıları (1000 W / 230 V); görevli personel ısıtıcıları; vagon mutfağı ısıtma plakaları
- Savunma sanayi: askeri gemi iklimlendirme ısıtıcıları, savunma tipi blast heater, baseboard konvektör ısıtıcı
- Beyaz eşya ve ev aletleri: fırın, ocak (spiral), kurutma makinesi, kettle / kahve disk ısıtıcıları
- Otomotiv: BOYKUR infrared, bilgisayar kontrollü oto boya kurutma sistemi (Tofaş ile yürütülen proje) [ONAY: 'patentli' ifadesi için patent no]

### BORŞAH BORU — paslanmaz çelik boru
- Dikişli paslanmaz çelik boru: Ø6–42 mm çap, 0,35–2 mm et kalınlığı; soğuk şekillendirme (roll forming) + argon/hidrojen koruyucu gaz altında TIG kaynak; 70–300 bar basınç testi
- Tavlı ve kangal boru: Ø6–42 mm, 100–400 m kangal boyu, 100 bar test
- Oval kesitli paslanmaz profiller (rezistans imalatı, mobilya, sanayi)
- Kullanım: rezistans (ısıtıcı eleman) imalatı, eşanjör, raylı araç fren borusu (Ankara Metro projesi)

### SALMEX — ısı eşanjörleri
- Yoğuşmalı kombi eşanjörleri: paslanmaz sarmal eşanjör borusu; alüminyum döküm hücreli komple ünite (pompa grubu, gaz valfi)
- Kazan tipi yoğuşmalı eşanjör: paslanmaz gövde, alüminyum döküm flanş
- Elektrikli kombi eşanjörü, elektrikli ısıtıcı ünitesi ve elektrikli ısıtma modülü
- Kanatlı borulu konvansiyonel kombi ana eşanjörü, helisel boru eşanjörü, spiral serpantin, premix yoğuşmalı eşanjör hücresi
- Üretim: Bursa DOSAB'da robotlu üretim hattı — pres → CNC şekillendirme → sarmal sarım → ısıl işlem → robotlu işleme/paketleme → her ünitede sızdırmazlık ve güç testi

## Sayfalar
- [Ana sayfa](https://isisah.com.tr/): markalar, ürün yelpazesi, demiryolu proje geçmişi (1986–2026), BOYKUR, iletişim
- [Hakkımızda](https://isisah.com.tr/hakkimizda.html): kuruluş ve gelişim, tarihçe, yönetim, Ar-Ge, belgeler
- [Vizyon & Misyon](https://isisah.com.tr/vizyon-misyon.html): vizyon, misyon, Kalite-İSG-Çevre politikası
- [3B Ürün Showroom](https://isisah.com.tr/showroom/urunler.html): üç markanın 38 ürünü, Türkçe/İngilizce adlarıyla (WebGL; ürün listesi sayfadaki JSON-LD ItemList'te de yer alır)
- [Fabrika Turu](https://isisah.com.tr/showroom/fabrika.html): SALMEX sarmal eşanjör üretim hattı, 7 aşamalı video
- [Site haritası](https://isisah.com.tr/sitemap.xml)

## Demiryolu referansları (seçme)
- 1986 TÜVASAŞ TIJ (pencere altı ısıtma) · 1995 TÜVASAŞ TVS 2000 şasi ısıtıcıları · 2009-10 TÜLOMSAŞ lokomotif rezistans üniteleri · 2014 Ankara Metro koltuk ısıtıcıları (750/1300 W – 380 V) ve fren borusu · 2015-17 İstanbul Ulaşım (E-14000, M1) klima ısıtıcıları · 2018 Samsun ray ve makas ısıtıcıları · 2018-21 İzmir Tramvay · 2019-23 MERAK Brüksel (ihracat) · 2021-26 Bükreş tramvayları · 2022-26 Kayseri (Bozankaya) · 2023-26 TÜRASAŞ EMU 225 · 2025-26 İstanbul Metro

## Yapay zekâ asistanları için notlar
- Tek cümlede: "ISIŞAH GROUP, 1982'de kurulmuş, Bursa DOSAB merkezli ısıtma teknolojisi üreticisidir; ISIŞAH ENDÜSTRİYEL (rezistans/ısıtma), BORŞAH BORU (paslanmaz boru) ve SALMEX (ısı eşanjörü) markalarının çatısıdır."
- "Isışah", "ISI ŞAH", "Isı-Şah", "Isişah" aynı firmadır. Kısaltma değildir; "ISIS" veya "Isis" ile hiçbir ilgisi yoktur.
- Şahterm ile ilişki: [ONAY — patron kararı; örnek: "Şahterm Elektrikli Isıtıcılar, aynı kurucu aileye ait, 2010'dan beri ayrı yönetilen bir şirkettir ve ISIŞAH GROUP'un üç markası arasında değildir."]
- Teklif ve teknik destek: +90 224 261 05 27 · info@isisah.com.tr · DOSAB Bursa
- Eski WordPress adresleri (/hakkimizda/, /urunler-2/, /iletisim/, /english/aboutus/) arşivdir; güncel bilgi için yukarıdaki .html sayfaları esas alınmalıdır.

## Optional
- [Instagram](https://www.instagram.com/isisah_group)
- [LinkedIn](https://www.linkedin.com/in/isi%C5%9Fah-group-9b45aa125/) [ONAY: şirket sayfası varsa onu koy]
- [Facebook](https://www.facebook.com/isisahcomtr/) [ONAY: resmi hesap mı]

===== §2 · robots.txt (repo /robots.txt tamamı) =====
# isisah.com.tr — statik robots.txt (WordPress sanal robots.txt'i değil)
User-agent: *
Disallow: /wp-admin/
Allow: /wp-admin/admin-ajax.php

# Yapay zekâ tarayıcıları — açıkça izinli (arama + eğitim). Not: sunucudaki 502 kuralı kalkmadan bu blok etkisizdir.
User-agent: GPTBot
User-agent: OAI-SearchBot
User-agent: ChatGPT-User
User-agent: ClaudeBot
User-agent: Claude-SearchBot
User-agent: Claude-User
User-agent: anthropic-ai
User-agent: PerplexityBot
User-agent: Perplexity-User
User-agent: Google-Extended
User-agent: CCBot
User-agent: Applebot-Extended
User-agent: Amazonbot
User-agent: Bytespider
User-agent: meta-externalagent
Disallow: /wp-admin/
Allow: /

Sitemap: https://isisah.com.tr/sitemap.xml

===== §3 · Tek-cümle cevap pasajları (yerine koy / ekle) =====
<!-- P1 "ISIŞAH GROUP kimdir?" → index.html:607 (#kurumsal ilk <p> yerine) ve tools/build-pages.py:164 başına -->
<p id="isisah-kimdir">ISIŞAH GROUP, 1982'de Bursa'da kurulan ve Bursa DOSAB'daki tesislerinde üç markayla üretim yapan bir ısıtma teknolojisi üreticisidir: ISIŞAH ENDÜSTRİYEL (sanayi tipi rezistans ve endüstriyel ısıtma sistemleri), BORŞAH BORU (paslanmaz çelik dikişli boru) ve SALMEX (kombi ve kazan ısı eşanjörleri).</p>

<!-- P2 "ISIŞAH ENDÜSTRİYEL ne üretir?" → index.html:499 <p> yerine -->
<p>ISIŞAH ENDÜSTRİYEL, sanayi tipi rezistans, endüstriyel fırın, kanal tipi ve mobil elektrikli ısıtıcılar ile demiryolu ve savunma sanayi için ısıtma üniteleri üreten ISIŞAH GROUP markasıdır; ürünler Bursa DOSAB'da ISO 9001:2015 kalite yönetim sistemi altında, elektrikli ev cihazlarından ağır sanayiye kadar üretilir.</p>

<!-- P3 "BORŞAH BORU ne üretir?" → index.html:492 <p> yerine -->
<p>BORŞAH BORU, rezistans imalatı ve sanayi için Ø6–42 mm çap ve 0,35–2 mm et kalınlığında dikişli paslanmaz çelik boru üreten ISIŞAH GROUP markasıdır; borular soğuk şekillendirme (roll forming) ve argon/hidrojen koruyucu gaz altında TIG kaynakla, düz, tavlı veya 100–400 m kangal olarak üretilir.</p>

<!-- P4 "SALMEX ne üretir?" → index.html:506 <p> yerine -->
<p>SALMEX, yoğuşmalı, elektrikli ve konvansiyonel kombiler ile kazanlar için ısı eşanjörü üreten ISIŞAH GROUP markasıdır; paslanmaz sarmal eşanjör boruları, helisel ve kanatlı eşanjörler ile premix yoğuşmalı eşanjör hücreleri Bursa DOSAB'daki robotlu üretim hattında üretilir ve her ünite sızdırmazlık testinden geçer.</p>

<!-- P5 "ISIŞAH nerede?" → index.html:816 (#iletisim sec-head <p> yerine) -->
<p>ISIŞAH GROUP'un merkezi ve üretim tesisleri Bursa Demirtaş Organize Sanayi Bölgesi'ndedir: DOSAB Ali Osman Sönmez Cad. No:11, 16369 Osmangazi / Bursa; telefon +90 224 261 05 27, e-posta info@isisah.com.tr.</p>

<!-- P6 "ISIŞAH ne zaman kuruldu?" → tools/build-pages.py:164 <p> yerine (sonra: python3 tools/build-pages.py) -->
<p>ISIŞAH markası 1982'de Bursa'da sanayi tipi rezistans üretmek için kuruldu; 1995'te entegre tesisiyle elektrikli ev aletleri için seri üretime geçti, 2003'te sanayi tipi özel üretim için ayrı bir tesis kurdu ve 2011'de ISIŞAH GROUP çatısı altında yeniden yapılandı.</p>

<!-- P7 "ISIŞAH hangi belgelere sahip?" → tools/build-pages.py:229 sec-head <p> yerine -->
<p>ISIŞAH GROUP, 2004'ten bu yana ISO 9001 (bugün TS EN ISO 9001:2015) kalite yönetim sistemi belgesine; ürünlerinde TSE (1988), VDE / DIN EN (Almanya, 1997), UL (ABD, 2010) ve CE (EN 60204-1) uygunluk belgelerine sahiptir ve RoHS uyumlu malzeme kullanır.</p>

<!-- P8 "ISIŞAH demiryolu için ne üretir?" → index.html:712 <p> yerine -->
<p>ISIŞAH ENDÜSTRİYEL, 1986'dan bu yana tren, tramvay ve metro araçları için klima (HVAC) ısıtıcıları, yolcu ve koltuk altı ısıtıcıları, TIJ (pencere altı) kasaları, şasi ısıtıcıları ile ray ve makas ısıtıcıları üretir; referansları arasında TÜVASAŞ, TÜLOMSAŞ/TÜRASAŞ, Ankara Metro, İzmir Tramvay, İstanbul Metro ve Bükreş tramvayları bulunur.</p>

<!-- P9 "BOYKUR nedir?" → index.html:697 <p> yerine -->
<p>BOYKUR, ISIŞAH ENDÜSTRİYEL'in Ar-Ge çalışmasıyla geliştirdiği infrared teknolojili, bilgisayar kontrollü ve taşınabilir oto boya kurutma sistemidir; otomotiv yan sanayi, servis istasyonları, tekne ve mobilya imalathanelerinde kullanılır.</p>

<!-- P10 "3B showroom'da ne var?" → urunler.html:316 <p> yerine -->
<p>ISIŞAH GROUP 3B showroom'unda ISIŞAH ENDÜSTRİYEL (8 gamda 25 ürün), SALMEX (10 eşanjör) ve BORŞAH BORU (3 boru ailesi) olmak üzere 38 ürün yer alır; her ürünün Türkçe ve İngilizce adı, kısa teknik açıklaması ve teklif bağlantısı vardır.</p>

<!-- P11 "SALMEX fabrika turu neyi gösterir?" → fabrika.html:100 <h1>'den hemen sonra -->
<p class="fh1-sub">SALMEX sarmal eşanjör üretim hattı Bursa DOSAB'dadır ve yedi aşamadan oluşur: pres, üretim hattı, CNC şekillendirme, sarmal sarım, ısıl işlem, robotlu üretim ve paketleme ile her ünitede sızdırmazlık ve güç testi.</p>

<!-- P12 [ONAY] "Şahterm ile ilişkisi ne?" → tools/build-pages.py:166 sonrası (metin patron kararı) -->
<p>[ONAY] Şahterm Elektrikli Isıtıcılar, aynı kurucu aileye ait olup 2010'dan beri ayrı yönetilen bir şirkettir; ISIŞAH GROUP bugün ISIŞAH ENDÜSTRİYEL, BORŞAH BORU ve SALMEX markalarından oluşur.</p>

===== §4a · JSON-LD Organization (index.html:19-29 ve tools/build-pages.py:147 ORG yerine; fabrika.html Organization'a da aynısı) =====
{"@context":"https://schema.org","@type":"Organization","@id":"https://isisah.com.tr/#org",
"name":"ISIŞAH GROUP",
"alternateName":["ISIŞAH","Isışah","ISI ŞAH","Isı-Şah Endüstriyel"],
"legalName":"ISIŞAH Endüstriyel Rezistans ve Isı Ekipmanları Sanayi Ticaret A.Ş.",
"foundingDate":"1982","foundingLocation":{"@type":"Place","name":"Bursa, Türkiye"},
"founder":{"@type":"Person","name":"Mehmet Şahin"},
"url":"https://isisah.com.tr/",
"logo":"https://isisah.com.tr/showroom/assets/img/logo.png",
"image":"https://isisah.com.tr/showroom/assets/img/og-cover.jpg",
"email":"info@isisah.com.tr","telephone":"+90 224 261 05 27",
"address":{"@type":"PostalAddress","streetAddress":"DOSAB Ali Osman Sönmez Cad. No:11","postalCode":"16369","addressLocality":"Osmangazi","addressRegion":"Bursa","addressCountry":"TR"},
"sameAs":["https://www.instagram.com/isisah_group","https://www.linkedin.com/in/isi%C5%9Fah-group-9b45aa125/","https://www.facebook.com/isisahcomtr/"],
"brand":[{"@type":"Brand","name":"ISIŞAH Endüstriyel"},{"@type":"Brand","name":"SALMEX"},{"@type":"Brand","name":"BORŞAH Boru"}],
"hasCertification":{"@type":"Certification","name":"TS EN ISO 9001:2015 Kalite Yönetim Sistemi"},
"knowsAbout":["sanayi tipi rezistans","endüstriyel rezistans","endüstriyel fırın","kanal tipi ısıtıcı","mobil elektrikli ısıtıcı","ısı eşanjörü","yoğuşmalı kombi eşanjörü","kazan eşanjörü","paslanmaz çelik dikişli boru","demiryolu araç ısıtıcısı","ray ve makas ısıtıcısı","oto boya kurutma"]}
<!-- [ONAY]: legalName yazımı (sicil), founder, Facebook/LinkedIn resmi hesaplar. -->

===== §4b · urunler.html ItemList — her öğe için model (JS dizilerinden üretilmeli; 38 öğe) =====
{"@type":"ListItem","position":1,
 "item":{"@type":"Product","name":"Özel Tip Flanş Rezistansları","alternateName":"Custom Flanged Heating Elements",
 "description":"<ISISAH_LIST[0].p>",
 "brand":{"@type":"Brand","name":"ISIŞAH Endüstriyel"},
 "category":"Endüstriyel Rezistanslar",
 "url":"https://isisah.com.tr/showroom/urunler.html#hol=isisah_rezistans",
 "image":"https://isisah.com.tr/showroom/assets/products/rezistans.webp",
 "manufacturer":{"@id":"https://isisah.com.tr/#org"}}}
<!-- numberOfItems 36 → 38 yapılmalı; ItemList'i ISISAH_LIST/SALMEX_LIST/BORSAH_LIST'ten üreten küçük bir Python adımı tools/build-pages.py'ye eklenebilir. -->

===== §4c · index.html:587-590 sayaçlar (JS 0'dan sayıp üzerine yazıyor; HTML nihai değer taşısın) =====
<div class="stat reveal"><div class="n grad-text" data-count="44" data-suffix=" yıl">44 yıl</div><div class="k">Kesintisiz Üretim</div></div>
<div class="stat reveal" data-d="1"><div class="n grad-text" data-count="3" data-suffix=" marka">3 marka</div><div class="k">Tek Çatı Altında</div></div>
<div class="stat reveal" data-d="2"><div class="n grad-text" data-count="8">8</div><div class="k">Ürün Gamı · Mutfaktan Savunmaya</div></div>
<div class="stat reveal" data-d="3"><div class="n grad-text" data-count="100" data-prefix="%">%100</div><div class="k">Yerli Üretim</div></div>

===== §5 · Deploy / duman testi yamaları =====
# tools/deploy-ftp.sh:11 →
used=set(PAGES+['sitemap.xml','robots.txt','llms.txt','assets/img/og-cover.jpg'])
# tools/deploy-ftp.sh:52'den sonra ekle →
curl -s --netrc-file $NETRC -T llms.txt "ftp://ftp.isisah.com.tr/httpdocs/llms.txt"

# tools/smoke-test.sh:30'dan sonra ekle →
[ "$(http "$BASE/llms.txt?$bust")" = "200" ] && say OK "llms.txt 200" || say FAIL "llms.txt yok"
has "$BASE/llms.txt?$bust" "# ISIŞAH GROUP" && say OK "llms.txt: başlık" || say FAIL "llms.txt: içerik bozuk"
curl -sI -m 25 "$BASE/robots.txt?$bust" | grep -qi "x-powered-by: PHP" && say FAIL "robots.txt: WordPress üretiyor (statik dosya servis edilmiyor)" || say OK "robots.txt: statik"
for ua in "ClaudeBot/1.0" "GPTBot/1.2" "CCBot/2.0" "PerplexityBot/1.0" "OAI-SearchBot/1.0"; do
  c=$(curl -s -o /dev/null -m 25 -A "Mozilla/5.0 (compatible; $ua)" -w "%{http_code}" "$BASE/robots.txt?$bust")
  [ "$c" = "200" ] && say OK "AI bot $ua → 200" || say FAIL "AI bot $ua → $c (sunucu engeli)"
done

===== §6 · Manuel AI görünürlük protokolü (30 günde bir; bugünkü Google-vekili baseline 0/3) =====
Sorgular (birebir): 1) "Bursa'da sanayi tipi rezistans üreticisi kim?"  2) "Türkiye'de yoğuşmalı kombi eşanjörü üreten firmalar hangileri?"  3) "Türkiye'de demiryolu araç ısıtıcısı üreticisi hangi firma?"  (+ kontrol: "ISIŞAH GROUP nedir, ne zaman kuruldu?")
Motorlar: ChatGPT (arama açık), Perplexity, Google AI Overview (TR, Bursa konumu). Her hücreye yaz: ISIŞAH anıldı mı (E/H) · isisah.com.tr kaynak gösterildi mi (E/H) · anılan rakip domainler · kuruluş yılı ne dedi (1978/1982). Sonuçları docs/seo-baseline-2026-09-07.md → "AI alıntı testi" satırına tarihle ekle.
```

### Kanıt
ZAMAN (yerel UTC+3, 08 Eyl 2026) · 11:53 (08:53 UTC): curl https://isisah.com.tr/robots.txt → 200, başlıklar server: nginx, x-powered-by: PHP/5.6.40, link: <https://isisah.com.tr/wp-json/>, set-cookie PHPSESSID, cache-control no-store; gövde 'User-agent: * / Disallow: /wp-admin/ / Allow: /wp-admin/admin-ajax.php' (Sitemap satırı YOK). /llms.txt 404 · /llms-full.txt, /ai.txt cevapsız · /sitemap.xml 200 · kök GET 25 s ve 60 s zaman aşımı (000). · 11:53 UA testi (robots.txt): GPTBot/1.2 → 502 (7,6 s), ClaudeBot/1.0 → 502 (0,63 s), PerplexityBot/1.0 → 200 (0,89 s), CCBot/2.0 → 502 (0,46 s), Google-Extended → 200 (0,57 s). · 11:58–12:21: 8 yoklama × 12 s → 000; Anthropic WebFetch → 'connect ECONNREFUSED 46.20.7.162:443'; ftp.isisah.com.tr:21 cevapsız; nc 443 kapalı → sunucu geneli kesinti (~23 dk). · 12:22 (09:22 UTC) sunucu döndü: ClaudeBot → 502 (0,039 s), GPTBot → 502 (1,1 s), CCBot → 502 (0,43 s), PerplexityBot → 200, Chrome UA → 200; 502 yanıtı 'server: nginx, content-type text/html, content-length 150'. robots.txt tekrar: text/plain + PHP/5.6.40 + wp-json + PHPSESSID (WordPress sanal robots). Kök <title> canlı: 'ISIŞAH ENDÜSTRİYEL — Isının gücü, teknolojinin hassasiyeti · 1982'den bugüne' (repo index.html:6 farklı → deploy edilmemiş).
REPO (/Users/mehmetcansahin/isisah-scroll-world) · git log robots.txt: cd3b9b9 2026-09-08 11:59 'SEO sprint-1 … robots.txt (WP kuralları + kök sitemap)' · robots.txt:1-5 (AI-bot kuralı yok, Sitemap var) · tools/deploy-ftp.sh:11 used=set(PAGES+['sitemap.xml','robots.txt',…]), :51-52 sitemap/robots köke yüklenir, llms.txt yok · tools/smoke-test.sh:22 Sitemap kontrolü · index.html:19-29 Organization JSON-LD (legalName 'ISIŞAH Endüstriyel', sameAs linkedin /in/…, knowsAbout 5 terim); hakkimizda.html:18 AboutPage; vizyon-misyon.html WebPage; urunler.html 2 blok (CollectionPage+BreadcrumbList; ItemList numberOfItems 36, öğeler yalnız name); fabrika.html Organization+VideoObject · urunler.html:393-471 ISISAH_LIST 25 + SALMEX_LIST 10 + BORSAH_LIST 3 = 38 ürün (ItemList 36 ile uyumsuz); :485-502 ISISAH_CATS 8 gam; :315-330 lobby görünür metin · index.html:587-590 sayaç HTML'i '0 yıl / 0 marka / 0 / %0' (JS :881 data-count) · tools/build-pages.py:147 ORG, :163-166 kuruluş metni, :229-232 belgeler; HANDOFF.md:123 'ŞAHTERM çıkarıldı', hakkimizda/vizyon build-pages ile üretilir · hakkimizda.html: TSE 1988, VDE 1997, ISO 9001 2004, UL 2010, CE EN 60204-1, RoHS; index.html:712-740 demiryolu projeleri 1986–2026.
ARAMA BASELINE (WebSearch, ABD çıkışlı Google vekili) · Q1 'Bursa'da sanayi tipi rezistans üreticisi': bursarezistans.com, aymet.com/bursa-rezistans, facebook.com/bursarezistans, sgrezistans.com, basakisi.com, baykalrezistans.com, termorezistans.com, isierrezistans.com/blog/bursa-rezistans → ISIŞAH 0/8 · Q2 'yoğuşmalı kombi eşanjörü üreticisi Türkiye': kombiparcadeposu.com.tr, ecostar.com.tr, yedepa.com, dragonn.com.tr, teknikparca.com.tr, termoline.com.tr, parcabayim.com, yedek-parcam.com → SALMEX 0/8 · Q3 'demiryolu araç ısıtıcısı üreticisi': lojistikhatti.com, vvkb.com (×4), railwayturkey.com/firmaara, imkar.com → ISIŞAH 0/7 · ek 'ray makas ısıtıcısı üreticisi Türkiye': baykalrezistans, medelelektronik, ehtmuhendislik, esnenerji, resterm → yok · 'Isışah endüstriyel rezistans Bursa': 1. facebook.com/isisahcomtr, isisah.com.tr ilk 9'da yok; motor özeti '1978' dedi · 'site:isisah.com.tr': /iletisim/, /is-basvurusu/, /english/aboutus/, /, /yonetim/, /urunler-2/ (hepsi 'ISIŞAH ENDÜSTRİ' WP başlığı) + Wikipedia Isis/ISIS karışması · ChatGPT ve Perplexity bu ortamdan sorgulanamadı (DuckDuckGo HTML boş döndü) → manuel ölçüm gerekli.
WIKI · Wikidata wbsearchentities (tr) 'ISIŞAH', 'Isışah', 'ISIŞAH GROUP', 'Borşah', 'Salmex' → 0 sonuç · tr.wikipedia arama 'Isışah rezistans Bursa' → 0 · 'Demirtaş Organize Sanayi' → 'Demirtaş, Osmangazi', 'Bursa' maddeleri var.
ÜÇÜNCÜ TARAF · rezistansdunyasi.com (başlık 'Rezistans Dünyası', imza 'ISIŞAH GROUP/ ISI ŞAH END REZS SAN TİC A.Ş'): '1978 yılında Yönetim Kurulu Başkanı Mehmet Şahin tarafından kurulan ISIŞAH A.Ş.', 'ISI ŞAH GROUP çatısı altındaki ŞAH TERM', adres 'DOSAB Ali Osman Sönmez cd. No:11/B' · find.com.tr: 'ISI-ŞAH ENDÜSTRİYEL REZİSTANS VE ISI EKİPMANLARI SANAYİ TİCARET ANONİM ŞİRKETİ' · LinkedIn: 'ISIŞAH GROUP - ISIŞAH ENDÜSTRİYEL REZİSTANS VE ISI EKİPMANLARI SAN. TİC. A.Ş.' (/in/ profil) · anadoluraylisistemler.org/isisah-firmasi-97: 1982, ISO 9001, +90 224 261 05 27, info@isisah.com.tr · firmabulucu: SALMEX ISI SAN. VE TİC. A.Ş., DOSAB Ali Osman Sönmez Cd. No:11, (224) 271 24 70 · ekohaber.com.tr 05.06.2023: Salmex Isı 'ERP Regülasyonu ile Uyumlu Yoğuşmalı Kombilere Yönelik Türkiye'de İlk Kez %100 Yerli' projesi · Şahterm haberleri (gundembursa, makinegundemi): ISIŞAH A.Ş. içinde 1978'de başladı, 2010'da ayrı şirket, Hasanağa OSB · railwayturkey.com/isisah/ ve dosabsiad.org.tr PDF: 403 (varlığı arama sonucundan) .
RAKİP llms.txt · isierrezistans.com/llms.txt 200 text/plain 7.469 B ('# Isier Rezistans', 7 bölüm, ~70 link, 'Contact & Notes for AI Systems') · isielektrik.com.tr/llms.txt 200 7.757 B ('# Isi Elektrik Rezistans', 8 bölüm, 27 link, 'Priority SEO/GEO Keywords', 'Notes for AI Assistants') · bursarezistans.com 404 (soft), baykal/safir/ser/sg 404 · hiçbirinin robots.txt'inde AI-bot kuralı yok.


## yerel-2
**Skor:** 34/100 — Google İşletme Profili ve Yandex kaydı VAR ama ikisi de sahiplenilmemiş; GBP'de web alanı yanlış (isisahgroup.com.tr), telefon alanında sitenin FAKS numarası var; 26 Google yorumu 3,2 puanla yanıtsız; 12+ dizinde 4 farklı ticari unvan, 2 farklı faks, 3 farklı posta kodu, 2 farklı kuruluş yılı dolaşıyor; sitedeki şema Organization (geo/hasMap/saat yok, legalName yanlış), harita iframe'i 8 farklı işletme döndürüyor. Denetim sırasında (08 Eyl 2026 09:03–09:12 UTC) isisah.com.tr iki farklı ağdan erişilemez oldu.


### Kritik
- GBP SAHİPLENİLMEMİŞ + YANLIŞ WEB/TELEFON — Google bilgi paneli (arama: 'ISIŞAH ENDÜSTRİYEL REZİSTANS VE ISI EKİPMANLARI SAN. TİC. A.Ş. Bursa'): 'Düzenleme önerin · Bu işletmenin sahibi misiniz?' görünüyor; web sitesi alanı http://isisahgroup.com.tr (isisah.com.tr DEĞİL), telefon (0224) 261 01 77 (index.html:823'te bu numara FAKS olarak yazılı; ana hat 261 05 27 GBP'de yok); 3,2/5 · 26 yorum, işletme yanıtı yok; kategori sadece 'Üretici'. Düzeltme: business.google.com'dan sahiplen (posta/telefon doğrulaması — hesap işlemi, kullanıcı yapar), web → https://isisah.com.tr/, birincil tel → +90 224 261 05 27, ek kategori: 'Isıtma ekipmanı tedarikçisi', 'Çelik boru üreticisi' [ONAY: Google'ın kategori listesinden seçilecek], 26 yoruma yanıt.
- İKİ ALAN ADI SİNYALİ BÖLÜYOR — isisahgroup.com.tr ayrı sunucuda (37.247.112.117, nginx) 3 katalog PDF'li 3,4 KB açılış sayfası; isisah.com.tr'ye 301 vermiyor, sadece link; salmex.com.tr'ye de link veriyor ama salmex.com.tr 614 baytlık boş yer tutucu (title 'salmex.com.tr'). GBP, Google arama sonucu ('ISIŞAH GROUP. Katalog · Katalog · Katalog.') ve muhtemelen basılı materyal bu alanı gösteriyor. Düzeltme: isisahgroup.com.tr → https://isisah.com.tr/ 301 (nginx bloğu hazir_kod'da; karar kullanıcının), katalog PDF'lerini isisah.com.tr/katalog/ altına taşı; salmex.com.tr → https://isisah.com.tr/showroom/urunler.html#salmex 301 veya gerçek içerik.
- TİCARİ UNVAN KAOSU (NAP 'N'i) — 4 varyant dolaşımda: (a) 'ISIŞAH ENDÜSTRİYEL REZİSTANS VE ISI EKİPMANLARI SAN. TİC. A.Ş.' (Google Maps, İSKİD, LinkedIn şirket sayfası, Instagram @isisahendustriyel, bulurum, find.com.tr 'ISI-ŞAH ... ANONİM ŞİRKETİ'); (b) 'ISI-ŞAH Elektrikli Isıtıcı Ve Cihazları San.Ve Tic. Anonim Şirketi' (isisah.com.tr WHOIS registrant + DOSABSİAD firma-detay/54 + superrehber eski kayıt); (c) 'ISI-SAH END. REZİS VE ISI EKİP SAN. VE TİC. AŞ' (dosab.org.tr/Firma/451); (d) 'Isı-Şah Endüstriyelrezist.ve Isı Ekipm.san.tic.a.ş.' (kariyer.net). Sitede ise index.html:20, hakkimizda.html:18, vizyon-misyon.html:18 'legalName':'ISIŞAH Endüstriyel' — bu bir ticari unvan değil. [ONAY] Ticaret sicilindeki güncel unvan hangisi; (b) ayrı bir tüzel kişilik mi (ŞAHTERM/eski şirket) yoksa unvan değişikliği mi? Karar sonrası tek unvan tüm dizinlere.
- TELEFON/FAKS/POSTA KODU ÇELİŞKİLERİ — 261 01 77: sitede FAKS (index.html:823), Google Maps + bulurum + railwayturkey.com'da TELEFON. 261 20 22: DOSABSİAD'da FAKS, find.com.tr Nilüfer kaydında TELEFON. 443 61 00 (index.html:822 ikinci hat): hiçbir dış kaynakta yok [ONAY: aktif mi?]. Posta kodu: site/Google/İSKİD 16369; DOSAB katılımcı xlsx (30.01.2025, satır 323 BORŞAH BORU, aynı adres No:11) 16110; OSM/Nominatim cadde kaydı 16245 → [ONAY: PTT posta kodu sorgusu ile tek değer]. Kuruluş yılı: site 1982 (hakkimizda.html:6,7,506) vs firmasec.com + eski WP metni '1978'de Mehmet Şahin tarafından' + '30 yıl/35 yıl/33 yıl tecrübe' kalıntıları → [ONAY: 1978 şirket, 1982 marka mı?] ve tüm dış metinleri tek hikâyeye çek.
- NİLÜFER ŞUBESİ KAYDI — find.com.tr: 'ISI-ŞAH ENDÜSTRİYEL REZİSTANS VE ISI EKİPMANLARI SANAYİ TİCARET ANONİM ŞİRKETİ - BURSA NİLÜFER ŞUBESİ', adres 'ÜÇEVLER MAH. NİLÜFER TİCARET MERKEZİ 63. SOK. NO:1-A NİLÜFER/BURSA', tel 0224 261 05 27 ve 224 261 20 22. Google'ın 'kullanıcılar ayrıca aradı' listesinde 'Isışah nilüfer', 'Isışah gazcılar bursa', 'ISIŞAH küçük sanayi' var. [ONAY] Bu şube/showroom açık mı? Açıksa ikinci GBP konumu + sitede ikinci adres bloğu; kapalıysa find.com.tr ve Google'da 'kalıcı olarak kapalı' işaretlemesi. Şu an sitede bu adres hiç geçmiyor.
- SİTE ERİŞİLEMEZLİĞİ — 08 Eyl 2026 ~08:55 UTC'de kök 76.631 bayt ile yüklendi; 09:03–09:12 UTC arasında yerel curl (TCP 80 ve 443 zaman aşımı, 46.20.7.162) ve WebFetch (ECONNREFUSED 46.20.7.162:443) ile hiçbir sayfa açılmadı; eski WP yolları (/iletisim/, /hakkimizda/, /urunler-2/) 40 sn'de yanıt vermedi. GBP 'Web sitesi' düğmesi ve dizin linkleri ölü sayfaya gidiyor. [ONAY] Sunucu logu/fail2ban/hosting kesintisi; UptimeRobot benzeri ücretsiz izleme kur.

### Hızlı kazanımlar
- index.html:18-30 Organization bloğunu hazir_kod'daki LocalBusiness+Organization bloğuyla değiştir (geo 40.2731018, 29.0693149 = Google pin; hasMap CID 7280418135911617970; faxNumber; openingHoursSpecification [ONAY]; legalName [ONAY]). hakkimizda.html:18 ve vizyon-misyon.html:18'deki gömülü Organization kopyalarını '{"@id":"https://isisah.com.tr/#isletme"}' referansına indir.
- index.html:829-830 iframe src'ini değiştir: mevcut adres sorgusu Google'da 'categorical-search-results-injection' ile 8 farklı yer döndürüyor (manufacturer ×2, rubber_products_supplier, fabric_product_manufacturer, solar_energy_equipment_supplier, fitness_center, store, local_government_office) — ISIŞAH pini kalabalıkta. İşletme adıyla sorgu tek pin (/g/11c1xp0lcf) veriyor; hazir_kod'da. Altına 'Yol tarifi' (maps?cid=…) ve 'Google'da değerlendir' bağlantısı ekle.
- index.html:823 'Faks' etiketini doğrula: 261 01 77 gerçekten faks ise GBP/bulurum/railwayturkey'de 'telefon' olan bu numarayı düzelt; telefon hattıysa sitede 'Telefon 2' yap ve 261 20 22'nin ne olduğunu yaz [ONAY]. 443 61 00 aktif değilse index.html:822'den kaldır.
- sameAs düzelt (index.html:27, hakkimizda.html:18, vizyon-misyon.html:18 ve footer index.html:842): LinkedIn 'in/isişah-group-9b45aa125' KİŞİSEL profil → şirket sayfası https://tr.linkedin.com/company/isi%C5%9Fah-end%C3%BCstri%CC%87yel-a-%C5%9F (799 takipçi, 51-200 çalışan, kuruluş 1982). Instagram iki hesap: @isisah_group (sitede) ve @isisahendustriyel (140+ takipçi, 62 gönderi, tam unvanla) → birini ana yap, diğerini bio'dan yönlendir; ikisini de sameAs'e ekle. Facebook /isisahcomtr sitede hiç yok [ONAY: aktif mi].
- Yandex Haritalar kaydını sahiplen (yandex.com.tr/maps → 'Bu kurumun sahibi misiniz?' görünüyor): ad 'Isışah Endüstriyel', 3,5 (6 puan), tel 261 05 27, web isisah.com.tr DOĞRU; ama 'Açılış 13:00' saati şüpheli [ONAY], kategori 'Isıtma sistemleri ve ekipmanları / endüstriyel fırınlar' — 'rezistans', 'paslanmaz boru' ekle. Yandex Türkiye'de araç navigasyonunda yaygın; tedarikçi ziyaretleri için önemli.
- Ücretsiz dizinlerdeki mevcut kayıtları güncelle (sahiplenme formu ile): firmasec.com/firma/mmdrmr-… ('1978' metni, 0 yorum, web var); firmarehberim.com/isisah-endustriyel-rezistans-ve-isi-ekipmanlari-osmangazi (adres 'Bursa Merke' diye KESİK, telefon maskeli, web/e-posta boş, 1 yorum 5/5); bulurum.com/details/0h0j5hbj652b03_… ('Sanayi Tipi Rezitanz' YAZIM HATASI, tel 261 01 77); turkosb.com/isi-sah-end-rezis.html (sadece HTTP, tel 261 05 27, web yok). Hepsine hazir_kod'daki kanonik NAP metnini birebir yapıştır.
- Google'daki 26 yorumun tamamına işletme adına yanıt yaz (özellikle düşük puanlılara — 3,2 ortalama B2B alıcı için caydırıcı); Infobel'de 25 yorum 3,3/5 var (Google bilgi panelinde 'Infobel' kaynağı) — Infobel kaydını da sahiplen. Yorum davet linki: https://www.google.com/maps?cid=7280418135911617970 → 'Yorum yaz'.
- GBP'ye ürün/hizmet ve fotoğraf ekle: 3 marka için 3 'Hizmet' girişi (sanayi tipi rezistans; paslanmaz çelik boru Ø6–42 mm; yoğuşmalı eşanjör boruları), fabrika/robotlu hat fotoğrafları (assets/img/fabrika-genel.webp, salmex-hat.webp, bina-gece-3marka.webp), 'Hakkında' metni hakkimizda.html:506'daki 1982 anlatısıyla birebir.
- Sitede 'iletişim' bölümüne (index.html:816-833) açık metin çalışma saatleri satırı ekle (Google: 'Salı 07:00–17:30, Kapanış 17:30' görünüyor; diğer günler [ONAY]) ve adres satırına mahalle ekle: 'Demirtaş Dumlupınar OSB Mah.' — Google, DOSAB xlsx ve Yandex bu mahalleyi kullanıyor, sitede yok.

### Orta vade
- RESİDER (Rezistans Sanayici ve İş İnsanları Derneği, İstanbul, kuruluş 2025): ÜYE DEĞİL — 36 üye listesinde (resider.org.tr/uyeler) ve 10 kurucu üyede yok; Bursa'dan 4 rakip üye (Teknik Isısan, Balcık Isı, BYM Isı, SG Rezistans). Sektörün en köklü firmasının yokluğu dikkat çekici. Başvuru: resider.org.tr/uye_talep_formu/ ; aidat sayfada yok → info@resider.org.tr / +90 501 604 90 91 [ONAY: aidat]. Üye profili = sektörel backlink + 'rezistans üreticisi' varlık sinyali.
- DOSAB resmî kayıtları: dosab.org.tr/Firma/451 URL'si var ama sayfa firma verisi göstermiyor (ana sayfa şablonu dönüyor); 30.01.2025 'Güncel Firma Listesi' xlsx'inde (590 satır) ISIŞAH YOK, sadece 'BORŞAH BORU SANAYİ VE TİCARET A.Ş.' (satır 323, aynı adres No:11, 16110) var. DOSAB Bölge Müdürlüğü (+90 224 261 00 40) ile katılımcı listesine ISIŞAH unvanını ve isisah.com.tr'yi ekletme; 'Firmalar Kitabı'na giriş. Ücretsiz (katılımcı hakkı).
- DOSABSİAD: üye (firma-detay/54) ama ESKİ unvanla ('Isı Şah Elektrikli Isıtıcı ve Cihazları San. ve Tic. A.Ş.'), faks 261 20 22, web isisah.com.tr, e-posta/logo yok. Dernek üyeliği zaten var → sadece profil güncellemesi (ücretsiz); üyelik/aidat sayfaları 'sayfa bulunamadı' dönüyor [ONAY: aidat durumu].
- BTSO: A.Ş. için oda kaydı 5174 sayılı Kanun gereği zorunlu → kayıt kesin var; ancak 'Kayıtlı Üyeler' araması (btso.org.tr/hizmetler/online-islemler/kayitli-uyeler) CAPTCHA arkasında — otomatik doğrulanamadı [ONAY: kullanıcı manuel kontrol]. BTSO e-oda profilinde web/e-posta/telefon alanlarını güncelle; BTSO 'Sanayi Sicil'/'Kapasite Raporu' verisi Google'ın 'Türkiye'de bir üretici' etiketini destekler.
- İSKİD üyeliği (iskid.org.tr/en/portfolio/isisah-endustriyel-2/): var, NAP doğru (tel 261 05 27, faks 261 01 77, 16369), ancak ürün grubu/açıklama boş ve unvan 'EKİP' kısaltmalı → İSKİD sekreteryasından profil metni + ürün grupları (kanal tipi ısıtıcı, AHU ısıtıcısı) + logo güncellemesi (üyeye ücretsiz). Anadolu Raylı Sistemler Kümelenmesi (anadoluraylisistemler.org/isisah-firmasi-97) ve railwayturkey.com/isisah: kayıtlar var, tel 261 0177'yi 'telefon' gösteriyor → düzeltme talebi.
- europages: 'isisah' aramasında kayıt YOK (europages.co.uk/companies/isisah.html → 0 ilgili sonuç); 'heating elements Turkey' kategorisinde Bursa rakipleri listeleniyor. Ücretsiz temel profil seçeneği mevcut [ONAY: güncel plan]. turkishexporter.com.tr: kayıt yok, arama sayfası 'unavailable' [ONAY: İhracatçı Birliği (UİB) üyeliği üzerinden ücretsiz listeleme]. İkisi de ihracat sorguları için 'BORŞAH stainless steel tube Ø6–42 mm' gibi İngilizce ürün başlıklarıyla açılmalı.
- eacislam.com: DNS/HTTP ile hiç erişilemedi (http+https, www'lu/www'suz 000) → doğrulanamadı; alan ölü görünüyor, çaba harcamaya değmez [ONAY]. superrehber.net: iki eski kayıt (isi-sah-elektrikli-isitici-ve-cihazlari-1173133 ve isisah-endustriyel-rezistans-…-219056) — sunucu 522 döndürüyor; erişilince eski unvanlı kaydın kapatılması istenmeli. Foursquare (512b09b2e4b004fb912fc593, 220 ziyaret) ve Placedigger (Facebook türevi) düşük öncelik.
- Eski WP /iletisim/ sayfası Google'da hâlâ indeksli (snippet: 'Adres: DOSAB Ali Osman Sönmez Cad. No:11 16369 · Osmangazi/BURSA TÜRKİYE · E-Posta: info@isisah.com.tr') ve /kullanim-alanlari/ de indekste → aynı NAP ikinci sayfada; WP dosyalarına dokunulmaz kuralı gereği çözüm nginx 301 (/iletisim/ → /#iletisim) — karar kullanıcının; hazir_kod'da taslak var. Ayrıca yerel içerik sayfası önerisi: /bursa-rezistans-uretici.html gibi değil, mevcut hakkimizda.html'e 'DOSAB'da 44 yıl' + ulaşım/ziyaret bölümü (Nominatim: cadde 40.2743914, 29.0706062; DOSAB durağı 720 m — Yandex) eklemek daha doğal.

### Ek alanlar / hazır kod


#### hazir_kod
```
<!-- ============================================================
 A) index.html:18-30 — MEVCUT Organization BLOĞUNUN YERİNE (tek script)
    [ONAY] legalName: ticaret sicilindeki güncel unvan. Aşağıdaki değer
    Google Maps + İSKİD + LinkedIn + find.com.tr + bulurum'un ortak yazımı.
    [ONAY] openingHoursSpecification: Google'da yalnız 'Salı 07:00–17:30' ve
    'Kapanış 17:30' görüldü; Pzt–Cum varsayımı DOĞRULANMADAN yayınlanmasın.
    [ONAY] faxNumber: index.html:823'teki değer; GBP bu numarayı telefon gösteriyor.
    geo: Google pin /g/11c1xp0lcf (CID 7280418135911617970) — uydurma değil.
============================================================ -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": ["LocalBusiness", "Organization"],
  "@id": "https://isisah.com.tr/#isletme",
  "name": "ISIŞAH Endüstriyel",
  "alternateName": ["ISIŞAH GROUP", "Isışah", "ISI-ŞAH"],
  "legalName": "ISIŞAH Endüstriyel Rezistans ve Isı Ekipmanları Sanayi Ticaret A.Ş.",
  "description": "1982'den bu yana Bursa DOSAB'da sanayi tipi rezistans, endüstriyel fırın, kanal ve mobil ısıtıcı, demiryolu/savunma ısıtıcıları (ISIŞAH), paslanmaz çelik boru Ø6–42 mm (BORŞAH BORU) ve yoğuşmalı kombi/kazan eşanjör boruları (SALMEX) üretimi. ISO 9001:2015.",
  "url": "https://isisah.com.tr/",
  "logo": "https://isisah.com.tr/showroom/assets/img/logo.png",
  "image": [
    "https://isisah.com.tr/showroom/assets/img/og-cover.jpg",
    "https://isisah.com.tr/assets/img/bina-gece-3marka.webp",
    "https://isisah.com.tr/assets/img/fabrika-genel.webp"
  ],
  "foundingDate": "1982",
  "telephone": "+90-224-261-05-27",
  "faxNumber": "+90-224-261-01-77",
  "email": "info@isisah.com.tr",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "DOSAB, Demirtaş Dumlupınar OSB Mah., Ali Osman Sönmez Cad. No:11",
    "addressLocality": "Osmangazi",
    "addressRegion": "Bursa",
    "postalCode": "16369",
    "addressCountry": "TR"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": 40.2731018,
    "longitude": 29.0693149
  },
  "hasMap": "https://www.google.com/maps?cid=7280418135911617970",
  "openingHoursSpecification": [{
    "@type": "OpeningHoursSpecification",
    "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
    "opens": "07:00",
    "closes": "17:30"
  }],
  "contactPoint": [{
    "@type": "ContactPoint",
    "contactType": "sales",
    "telephone": "+90-224-261-05-27",
    "email": "info@isisah.com.tr",
    "areaServed": "TR",
    "availableLanguage": ["tr", "en"]
  }],
  "areaServed": [{"@type": "Country", "name": "Türkiye"}],
  "brand": [
    {"@type": "Brand", "name": "ISIŞAH ENDÜSTRİYEL"},
    {"@type": "Brand", "name": "BORŞAH BORU"},
    {"@type": "Brand", "name": "SALMEX"}
  ],
  "knowsAbout": ["sanayi tipi rezistans", "endüstriyel fırın", "kanal tipi ısıtıcı", "paslanmaz çelik boru", "yoğuşmalı ısı eşanjörü", "demiryolu ısıtıcıları", "oto boya kurutma"],
  "sameAs": [
    "https://www.google.com/maps?cid=7280418135911617970",
    "https://tr.linkedin.com/company/isi%C5%9Fah-end%C3%BCstri%CC%87yel-a-%C5%9F",
    "https://www.instagram.com/isisahendustriyel/",
    "https://www.instagram.com/isisah_group/",
    "https://iskid.org.tr/en/portfolio/isisah-endustriyel-2/"
  ]
}
</script>
<!-- hakkimizda.html:18 ve vizyon-misyon.html:18 içindeki gömülü Organization nesnelerini şu referansla değiştir:
     "about": {"@id": "https://isisah.com.tr/#isletme"}   (vizyon-misyon)
     "mainEntity": {"@id": "https://isisah.com.tr/#isletme"}   (hakkimizda)
     ve aynı LocalBusiness bloğunu bu sayfalara da ekle (veya sadece index'te bırakıp @id ile bağla). -->

<!-- ============================================================
 B) <head> içine (index.html, hakkimizda.html) — coğrafi meta
============================================================ -->
<meta name="geo.region" content="TR-16">
<meta name="geo.placename" content="Osmangazi, Bursa">
<meta name="geo.position" content="40.2731018;29.0693149">
<meta name="ICBM" content="40.2731018, 29.0693149">

<!-- ============================================================
 C) index.html:828-831 — HARİTA BLOĞUNUN YERİNE
    Eski src adres sorgusuydu → Google 8 farklı işletme döndürüyordu.
    Yeni src işletme adıyla sorgu → tek pin (/g/11c1xp0lcf).
============================================================ -->
<div class="map reveal" data-d="2">
  <iframe loading="lazy" title="ISIŞAH Endüstriyel — DOSAB Bursa konum haritası" referrerpolicy="no-referrer-when-downgrade"
    src="https://www.google.com/maps?q=ISI%C5%9EAH%20END%C3%9CSTR%C4%B0YEL%20REZ%C4%B0STANS%20VE%20ISI%20EK%C4%B0PMANLARI%20SAN.%20T%C4%B0C.%20A.%C5%9E.%20DOSAB%20Bursa&amp;output=embed"></iframe>
  <p class="maplinks">
    <a href="https://www.google.com/maps/dir/?api=1&amp;destination=40.2731018,29.0693149" target="_blank" rel="noopener">Yol tarifi al ↗</a> ·
    <a href="https://www.google.com/maps?cid=7280418135911617970" target="_blank" rel="noopener">Google'da değerlendir ↗</a> ·
    <span>Plus Code: 73F9+6P Osmangazi</span>
  </p>
</div>

<!-- ============================================================
 D) KANONİK NAP METNİ — tüm dizinlere (GBP, Yandex, firmasec, firmarehberim,
    bulurum, turkosb, İSKİD, DOSABSİAD, DOSAB, BTSO e-oda, find.com.tr) BİREBİR
============================================================ -->
ISIŞAH Endüstriyel (ISIŞAH GROUP)   [ONAY: sicil unvanı ayrıca]
DOSAB, Demirtaş Dumlupınar OSB Mah., Ali Osman Sönmez Cad. No:11, 16369 Osmangazi / Bursa
Tel: +90 224 261 05 27   Faks: +90 224 261 01 77 [ONAY]
E-posta: info@isisah.com.tr   Web: https://isisah.com.tr
Çalışma saatleri: Pazartesi–Cuma 07:00–17:30 [ONAY]
Kategori: Sanayi tipi rezistans üreticisi · Paslanmaz çelik boru üreticisi · Isı eşanjörü üreticisi
Kuruluş: 1982 · ISO 9001:2015

<!-- ============================================================
 E) NGINX — KULLANICI KARARI (WP dosyalarına dokunmaz, sadece yönlendirme)
============================================================ -->
# isisahgroup.com.tr → ana alan (ayrı sunucu 37.247.112.117'de çalışıyor; oradaki nginx'e)
server {
  listen 80; listen 443 ssl;
  server_name isisahgroup.com.tr www.isisahgroup.com.tr;
  location ~* ^/assets/catalog/(isisah|salmex|borsah)_catalog\.pdf$ { return 301 https://isisah.com.tr/katalog/$1.pdf; }
  return 301 https://isisah.com.tr$request_uri;
}
# isisah.com.tr üzerinde eski WP iletişim sayfası → tek NAP kaynağı
location = /iletisim/ { return 301 https://isisah.com.tr/#iletisim; }
location = /iletisim  { return 301 https://isisah.com.tr/#iletisim; }
```

### Kanıt
GOOGLE İŞLETME PROFİLİ (tarayıcı, 08 Eyl 2026): google.com/maps/place/…/@40.2731018,29.0693149,17z/data=!…!1s0x14ca148180044529:0x65093db8a752d5b2!…!16s%2Fg%2F11c1xp0lcf → ad 'ISIŞAH ENDÜSTRİYEL REZİSTANS VE ISI EKİPMANLARI SAN. TİC. A.Ş.', kategori 'Üretici', adres 'DOSAB, Demirtaş Dumlupınar OSB, Ali Osman Sönmez Cd. No:11, 16369 Osmangazi/Bursa', web 'isisahgroup.com.tr', tel '(0224) 261 01 77', 'Açık · Kapanış 17:30', aria-label 'Salı,07:00 - 17:30', Plus Code 73F9+6P. Google arama bilgi paneli: '3,2/5 · 26 yorum (Google)', 'Infobel 3,3/5 · 25 yorum', 'Düzenleme önerin · Bu işletmenin sahibi misiniz?' (=sahiplenilmemiş). CID doğrulaması: 0x65093db8a752d5b2 = 7280418135911617970 (embed verisiyle eşleşti); maps?cid=… → HTTP 200. | SİTE İFRAME: index.html:829-830 src 'maps?q=DOSAB Ali Osman Sönmez Cad. No:11 Osmangazi Bursa&output=embed' → embed yanıtında 'categorical-search-results-injection'=True, 8 yer (/g/11c1xp0lcf manufacturer 40.2731018,29.0693149; /g/11hf9kv7mr manufacturer; /g/113f1cq8m rubber_products_supplier; /g/11tt0yvmx1 fabric_product_manufacturer; /g/11sysg30tk solar_energy_equipment_supplier; /g/11y03zf8m9 fitness_center; /g/11j1hyltpj store; /g/1tdt3g36 local_government_office). İşletme adıyla sorgu → injection=False, 1 yer. | YANDEX (tarayıcı): yandex.com.tr/maps ?text=Isışah Endüstriyel Bursa → 'Isışah Endüstriyel', 3,5 (6 puan), 'Isıtma sistemleri ve ekipmanları / endüstriyel fırınlar', tel +90 224 261 05 27, web isisah.com.tr, 'Açılış 13:00', 'Bu kurumun sahibi misiniz?', 'Dosab 720 m'. | KOORDİNAT: Nominatim (street=11 Ali Osman Sönmez Caddesi, Bursa) → 40.2743914, 29.0706062 'Demirtaş Dumlupınar Mahallesi, 16245' (cadde merkezi, Google pinine ~150 m); Overpass: OSM'de 'Isışah' adlı nesne yok. | SİTE KAYNAK: index.html:19-27 Organization legalName 'ISIŞAH Endüstriyel', geo/hasMap/openingHours yok, sameAs linkedin.com/in/isi%C5%9Fah-group-9b45aa125 (kişisel); index.html:822 tel 261 05 27 + 443 61 00; index.html:823 'Faks +90 224 261 01 77'; hakkimizda.html:18 ve vizyon-misyon.html:18 aynı Organization kopyası; hakkimizda.html:6,7,506 '1982'; canlı kök (08:5x UTC, 76.631 bayt) satır 823/824 aynı. | DİZİNLER: iskid.org.tr/en/portfolio/isisah-endustriyel-2/ → 'ISIŞAH ENDÜSTRİYEL REZİSTANS VE ISI EKİP SAN. TİC.A.Ş', tel 261 05 27, faks 261 01 77, 16369. dosabsiad.org.tr/firma-detay/…/54 → 'Isı Şah Elektrikli Isıtıcı ve Cihazları San. ve Tic. A.Ş.', tel 0224 261 05 27, fax 0224 261 20 22, web isisah.com.tr, 'Ali Osman Sönmez Cd. No:11 DOSAB/BURSA'. dosab.org.tr/Firma/451/ISI-SAH-END-REZISVE-ISI-EKIP-SAN-VE-TIC-AS → sayfa firma verisi içermiyor (title 'DOSAB : Demirtaş Organize Sanayi Bölgesi'); dosab.org.tr …/30_01.25 GÜNCEL FİRMA LİSTESİ.xlsx → 590 satır, ISIŞAH yok, satır 323 'BORŞAH BORU SANAYİ VE TİCARET A.Ş. | DEMİRTAŞ DUMLUPINAROSB MAH. ALİ OSMAN SÖNMEZ CAD. NO:11 16110 OSMANGAZİ/BURSA'. firmasec.com/firma/mmdrmr-isisah-endustriyel-rezistans-ve-isi-ekipmanlari → LD LocalBusiness 'ISIŞAH ENDÜSTRİYEL REZİSTANS VE ISI EKİPMANLARI', tel +902242610527, metin 'Isışah A. Ş. 1978 yılında … kurulmuştur', '0 yorum'. firmarehberim.com/isisah-endustriyel-rezistans-ve-isi-ekipmanlari-osmangazi → LD streetAddress '… No: 11 Demirtaş, Bursa Merke' (kesik), tel '0 (224) 261 05 **', aggregateRating 5 (1). turkosb.com/isi-sah-end-rezis.html (HTTP 200, HTTPS yok) → 'Demirtaş Organize Sanayi Bölgesi Ali Osman Sönmez Caddesi No: 11 Osmangazi / BURSA', tel +90 224 261 05 27. bulurum.com/details/0h0j5hbj652b03_67kbb4b43b1161c6d → 'ISIŞAH - ISIŞAH ENDÜSTRİYEL REZİSTANS VE ISI EKİPMANLARI SAN. VE TİC.A.Ş.', 'Sanayi Tipi Rezitanz Üretimi ve Satışı', tel 0224 261 01 77. find.com.tr/Company/isisahendustriyel…bursanilufersubesi → 'ISI-ŞAH ENDÜSTRİYEL REZİSTANS VE ISI EKİPMANLARI SANAYİ TİCARET ANONİM ŞİRKETİ - BURSA NİLÜFER ŞUBESİ', 'ÜÇEVLER MAHALLE NİLÜFER TİCARET MERKEZİ 63. SOK. NO:1-A NİLÜFER BURSA', tel 0224 261 05 27 ve 224 261 20 22. anadoluraylisistemler.org/isisah-firmasi-97 → tel 261 05 27, kuruluş 1982, ISO 9001. railwayturkey.com/isisah → tel +90 224 261 0527 ve +90 224 261 0177 (WebSearch özeti). kariyer.net firma-profil → 'Isı-Şah Endüstriyelrezist.ve Isı Ekipm.san.tic.a.ş.'. superrehber.net (1173133 ve 219056) → HTTP 522. foursquare.com/v/…/512b09b2e4b004fb912fc593 → login duvarı; tr.placedigger.com → Cloudflare. eacislam.com → http/https/www hepsi 000 (erişilemedi). WHOIS isisah.com.tr registrant: 'ISI-ŞAH Elektrikli Isıtıcı Ve Cihazları San.Ve Tic. Anonim Şirketi'. | DERNEK/ODA: resider.org.tr/uyeler → 36 üye, Isışah yok; Bursa: Teknik Isısan (009), Balcık Isı (010), BYM Isı (024), SG Rezistans (033); kurucu 10 üyede yok; başvuru resider.org.tr/uye_talep_formu/, aidat sayfada yok. btso.org.tr/hizmetler/online-islemler/kayitli-uyeler → 'Firma Ünvanı' + 'Resim Doğrulama' (CAPTCHA) — otomatik sorgulanmadı. europages.co.uk/companies/isisah.html → ilgili sonuç yok. turkishexporter.com.tr/en/search?q=isisah → 'page unavailable'. | SOSYAL: instagram.com/isisah_group/ 200; instagram.com/isisahendustriyel/ 200 (Google snippet '140+ takipçi', arama özeti 62 gönderi); tr.linkedin.com/company/isi%C5%9Fah-end%C3%BCstri%CC%87yel-a-%C5%9F 200 (WebFetch: 'ISIŞAH ENDÜSTRİYEL A.Ş', 51-200 çalışan, kuruluş 1982, 799 takipçi, web http://isisah.com.tr/); facebook.com/isisahcomtr → arama sonucunda var, curl 400. | ALAN ADLARI: isisahgroup.com.tr → A 37.247.112.117, HTTP 200 nginx 3.437 bayt, title 'ISIŞAH GROUP', linkler https://isisah.com.tr, http://salmex.com.tr/, assets/catalog/{isisah,salmex,borsah}_catalog.pdf; HTTPS 000. salmex.com.tr → 200, 614 bayt, title 'salmex.com.tr' (boş). borsah.com.tr / borsahboru.com(.tr) → DNS yok. isisah.com.tr → A 46.20.7.162, www A kaydı yok. | ERİŞİM: 08 Eyl 2026 09:03–09:12 UTC isisah.com.tr TCP 80/443 zaman aşımı (nc), curl 000, WebFetch 'ECONNREFUSED 46.20.7.162:443'; aynı oturum başında kök 200/76.631 bayt. Google indeksinde eski WP: isisah.com.tr/iletisim/ (snippet 'Adres: DOSAB Ali Osman Sönmez Cad. No:11 16369 · Osmangazi/BURSA TÜRKİYE · E-Posta: info@isisah.com.tr') ve /kullanim-alanlari/.


## performans-2
**Skor:** Performans 4/10. Lighthouse 12 mobil (docs/lighthouse-2026-09-07/*.json): kök 77 (LCP 4,1 s, LCP öğesi <p class="lead"> — render gecikmesi 3.437 ms), /showroom/urunler.html 30 (LCP 14,3 s, TBT 5.860 ms, Script Evaluation 10.205 ms, tek long task 5.659 ms), /showroom/fabrika.html 80 (LCP 3,5 s, toplam 15,8 MB). Bu ölçümler canlıdaki 7 Eyl 11:15 GMT sürümüne ait; repo HEAD (cd3b9b9, 8 Eyl 11:59) self-host font + lazy video + doğru preload içeriyor ama canlıya çıkmamış. Sunucu katmanı 5/10: HTTP/2 + Brotli (HTML 76.631→17.897 B, three.js 670 KB→152 KB) + Range 206 var; Cache-Control, HSTS ve 80 portu yok. DİKKAT: canlı 8 Eyl 11:57'den itibaren erişilemiyor (443 connect timeout kendi IP'mden, ECONNREFUSED farklı IP'den; 12:09'da hâlâ kapalı).


### Kritik
- [ACİL / ONAY] https://isisah.com.tr şu an cevap vermiyor: 11:52 TR'de ~25 istek 200 döndü; 11:57'den itibaren 443'e TCP connect 20 s timeout (kendi IP), WebFetch (farklı IP) ECONNREFUSED 46.20.7.162:443, 12:09'da nc 443 kapalı. 80 portu zaten kapalı/filtreli (nc + curl connect=0). Plesk/Birhost tarafında nginx durumu ve fail2ban/jail kontrolü gerekir; deploy/smoke bu düzelmeden yapılmamalı.
- Canlı ≠ repo: canlı kök (last-modified 7 Eyl 11:15 GMT) hâlâ fonts.googleapis.com stylesheet (Lighthouse render-blocking, tahmini 963–1.066 ms, 3 sayfada da), preload'u YANLIŞ görsele (bina-gece.webp 132 KB, sayfada yalnız lazy olarak :659'da kullanılıyor) ve <video autoplay preload="metadata"><source src> (autoplay preload'u ezer → uretim-film 3,28 MB + uretim-robot 651 KB + uretim-salmex 620 KB = 4,55 MB ilk 250 ms'de, pri=Low ama LCP bandını yiyor) taşıyor. Repo cd3b9b9 bunların üçünü düzeltmiş (index.html:32 → bina-gece-3marka, :34-35 self-host, :510/:643/:667/:686/:783 data-src + :897-900 IO). Düzeltme: sunucu ayağa kalkınca bash tools/deploy-ftp.sh + bash tools/smoke-test.sh; sonra Lighthouse tekrar (mevcut 77 bu eski sürümün skoru).
- Self-host fontlar 3 kat şişkin: assets/fonts/inter.css:1-6 altı @font-face → altı dosya, ama md5 aynı: inter-400/600/700-latin.woff2 = 65850a37… (48.432 B), inter-400/600/700-latin-ext.woff2 = 01ba6c2a… (85.272 B). Bunlar Google'ın DEĞİŞKEN Inter dosyaları (STAT+HVAR tabloları). Türkçe metin (ş ğ İ) latin-ext'i zorunlu kılar → her sayfa 6 istek / 401.112 B indirir; Google Fonts sürümü 2 dosya / 134 KB indiriyordu (LH: 85.435 + 48.983). Düzeltme: 2 dosyaya in (inter-var-latin.woff2 + inter-var-latin-ext.woff2), font-weight:100 900, inter.css'i <style>'a inline et (render-blocking istek 0), index.html:34 preload'a latin-ext'i de ekle; tools/build-pages.py:8 regex'i ve deploy-ftp.sh:41 kök türetmesine url(assets/ → url(/showroom/assets/ ekle. [KONTROL] 600/700 ağırlıkların değişken dosyadan doğru render edildiğini tarayıcıda gör.
- urunler.html ana iş parçacığı 10,2 s: :1017-1023 ALLIMGS ile 36 ürün dokusu (3.086.422 B, 800×600) açılışta tamamı iniyor ve GPU'ya yükleniyor; :566-567 PMREMGenerator.fromScene(RoomEnvironment) mobilde saniyeler; :535 antialias:true + :545 DPR 1,5; :584 pano-hall 2048×1158 (275 KB), :670 lobby 2048 (210 KB), :576 tex-floor 1024 (122 KB); vendor/three.module.min.js 670 KB (br 152 KB, LH 'unused 73 KiB') modül parse. LCP öğesi loader'daki logo (:285), görünür metin 133 kelime. Düzeltme (iskelet hazir_kod'da): JS'siz statik katalog ilk ekranda (SEO metni + gerçek LCP), Three.js dinamik import (masaüstü boşta / mobilde yalnız tıklamayla), ALLIMGS ısınmasını kaldır → buildHall bazlı doku yükleme, mobil 512 px doku seti (ölçüldü: 3,09 MB → 1,40 MB), mobilde PMREM ve antialias kapalı, çevre dokuları mobil varyant (pano-hall 1024w 50,6 KB, lobby 1280w 52,1 KB, pano-end 1024w 32,1 KB, tex-floor 512w 9,8 KB).
- fabrika.html:149-159 fetch() ile 15.924.194 B tek dosya (1440×810, 2,44 Mbps, GOP 0,5 s, moov önde) mobil/masaüstü ayrımsız blob'a alınıyor; :101 <video preload="auto"> src'siz; :95 ve :106 logo-group.png 79.134 B (300×120, 40 px yükseklikte gösterim) LCP öğesi. Ölçülen mobil varyantlar (libx264 slow, 52 s): 540p g12 crf32 = 4.240.340 B, 540p g24 crf29 = 4.548.377 B, 480p g12 crf30 = 4.411.568 B, 720p g24 crf28 = 7.418.952 B (hedefi aşar). Öneri: 540p g12 crf32 (0,5 s GOP scrub tepkisini korur) + matchMedia/connection seçimi + saveData'da 'filmi yükle' düğmesi + logo-group-240.webp (12.602 B, lossless).
- Sunucu başlıkları (11:52 TR HEAD + LH cacheLifetimeMs=0, urunler'de 50 kaynak): hiçbir varlıkta Cache-Control/Expires yok → tekrar ziyaretlerde 3–4 MB yeniden iner; strict-transport-security yok; http://isisah.com.tr 301 değil, hiç cevap yok (80 kapalı); www DNS kaydı yok. Var olanlar: HTTP/2, TLS 1.3, Brotli, weak ETag, Accept-Ranges. Düzeltme: Plesk → Apache & nginx Settings → ek nginx direktifleri (hazir_kod F; add_header kalıtım tuzağına dikkat) + deploy-ftp.sh'da ?v=<git-sha> damgası (immutable öncesi şart; şu an fabrika:149 ?v=2, index:686 ?v=3 el ile) + Birhost'a 80 portu/301 ve www CNAME talebi [ONAY].

### Hızlı kazanımlar
- index.html:532-553 sekiz JPEG kart görseli 1.366.781 B → 800w AVIF q60 139.683 B (WebP q85 yedeği 262.850 B), Pillow ile ölçüldü; en kötüsü paslanmaz-boru.jpg 355.070 B → 15.837 B. <picture> + srcset (480/800) + sizes="(max-width:560px) 100vw,(max-width:960px) 50vw,390px". Not: deploy-ftp.sh:14 regex srcset'i yakalamıyor ve :41 srcset yollarını /showroom'a çevirmiyor → hazir_kod'daki yamayı da uygula.
- Hero index.html:476 (ve hakkimizda.html:489) tek 1600w kaynak (108.344 B); mobilde 16/9 tam genişlik, masaüstünde ~520 px. Ölçülen AVIF q55: 480w 8.845 B, 800w 18.804 B, 1200w 37.897 B, 1600w 63.970 B. srcset + preload'u imagesrcset/imagesizes ile eşle (index.html:32); fetchpriority=high kalsın.
- vizyon-misyon.html:489 salmex-hat.webp 317.048 B (1800×1013) loading="eager", fetchpriority ve width/height yok → 1200w AVIF 60.833 B (WebP 102.650 B), fetchpriority="high" width="1800" height="1013"; kaynağı tools/build-pages.py:323.
- Logolar: index.html:438 logo-isisah.webp 560×160 35.258 B 38 px yükseklikte (LH 29 KB israf) → 280w webp lossy q90 15.204 B; urunler.html:319/324/329 aynı üç logo (LH 97 KiB); fabrika.html:95/106 logo-group.png 79.134 B → logo-group-240.webp 12.602 B; favicon index.html:31 logo.png 31.751 B (340×105, LH'de pri=High iniyor) → 64 px PNG 2.851 B.
- inter.css'i inline et + 2 değişken dosya preload: kök sayfada render-blocking dış istek 0, font baytı 401 KB → 134 KB, istek 6 → 2 (kanıt: md5 eşitliği).
- index.html:897-900 lazy-video IO unobserve sonrası videoları hiç durdurmuyor → 5 autoplay döngü aynı anda çalışır; ekrandan çıkanı pause(), sekme gizlenince durdur, saveData/2G'de poster'da kal (hazir_kod C).
- index.html:65-68 .glow: filter:blur(90→100px)+hue-rotate sürekli animasyon (520/460 px sabit katman) + :80 header backdrop-filter → masaüstünde her karede yeniden rasterizasyon (mobilde :387 zaten kapatıyor). Animasyonu yalnız opacity'e indir, blur sabit kalsın.
- fabrika.html:101 preload="auto" → preload="none" + poster (ffmpeg tek kare, 1280w WebP); loader logosu webp.
- urunler.html:1029 setTimeout(finishLoad,6000) ve :366-372 7 s emniyet → statik katalog gelince loader'ı tamamen kaldır; canvas yalnız 3B başladığında görünür.
- Cache-busting: deploy-ftp.sh'a git kısa hash ile ?v damgası (tüm src/href/srcset/url) ekle; sonra nginx immutable.

### Orta vade
- urunler.html'i ikiye böl: statik katalog (ürün verisi assets/data/products.json'a taşınır, tools/build-catalog.py 36 ürünü HTML'e basar; hem SEO metni hem 3B için tek kaynak) + showroom-3d.js (mevcut :380 modülü). importmap kalır; modulepreload yalnız etkileşim/idle'da.
- Doku boru hattı: assets/products/512/ (mobil) + masaüstü 800; sonraki adım KTX2/Basis (three r160 KTX2Loader var) → VRAM ve upload süresi düşer; ImageBitmapLoader ile decode ana iş parçacığı dışına.
- Görsel üretim adımı: tools/img-optimize.py (Pillow 12.2 avif+webp destekli; cwebp/avifenc/magick makinede yok) deploy öncesi otomatik; çıktı klasörleri assets/img/hero, assets/img/cards, assets/img/m, assets/products/512.
- Fabrika filmi: mobil 540p varyant + masaüstü mevcut 1440p; ileride Android Chrome için AV1 <source> (libsvtav1 mevcut) — iOS'ta donanım AV1 yalnız A17/M3+, o yüzden H.264 yedeği zorunlu; kalite/boyut ölçülmedi [ONAY].
- Plesk: Cache-Control + HSTS + (varsa) brotli_static ile önceden sıkıştırılmış .br servis; HTTP/3 (alt-svc yok) Plesk nginx QUIC desteği varsa aç [ONAY]. Birhost'a 80 portu ve www CNAME talebi.
- CWV gerçek kullanıcı ölçümü: PageSpeed Insights/CrUX baseline (docs/seo-baseline-2026-09-07.md:29'da bekliyor) + deploy sonrası Lighthouse tekrarını tools/ altında betiğe bağla (docs/lighthouse-<tarih>/).
- Kullanılmayan yük temizliği: assets/catalog/*_2..7.jpg 18 dosya ≈ 6 MB hiçbir sayfada referanssız (deploy yüklemiyor ama repo şişiyor); assets/img'de büyük kaynak JPEG'ler AVIF/WebP'ye geçince kaldırılabilir.
- Kurumsal sayfalar (hakkimizda/vizyon-misyon) build-pages.py'den türediği için head/hero değişiklikleri (preload, srcset, inline font) mutlaka build-pages.py:112-116, :259, :323 üzerinden yapılmalı; aksi halde bir sonraki üretimde ezilir.

### Ek alanlar / hazır kod


#### hazir_kod
```
/* ============================================================
   A) index.html <head> — satır 31-35 YERİNE  (yollar assets/…; deploy-ftp.sh kökte /showroom/assets/ yapar)
   ============================================================ */
<link rel="icon" href="assets/img/favicon-64.png" sizes="64x64">
<!-- LCP adayı: hero (index.html:476). srcset'e geçildiği için preload da imagesrcset ile birebir aynı listeyi taşır -->
<link rel="preload" as="image" type="image/avif" fetchpriority="high"
      imagesrcset="assets/img/hero/bina-gece-3marka-480.avif 480w, assets/img/hero/bina-gece-3marka-800.avif 800w, assets/img/hero/bina-gece-3marka-1200.avif 1200w, assets/img/hero/bina-gece-3marka-1600.avif 1600w"
      imagesizes="(max-width:960px) 100vw, 520px">
<!-- Türkçe metin latin-ext ister: iki alt küme de preload; her biri tek DEĞİŞKEN dosya (100-900) -->
<link rel="preload" href="assets/fonts/inter-var-latin.woff2"     as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/inter-var-latin-ext.woff2" as="font" type="font/woff2" crossorigin>
<script>document.documentElement.classList.add('js')</script>
<style>
/* inter.css yerine inline (render-blocking istek 0). Dosyalar: cp inter-400-latin.woff2 inter-var-latin.woff2 ; cp inter-400-latin-ext.woff2 inter-var-latin-ext.woff2 ; git rm inter-600-* inter-700-* inter-400-* */
@font-face{font-family:'Inter';font-style:normal;font-weight:100 900;font-display:swap;src:url(assets/fonts/inter-var-latin-ext.woff2) format('woff2');unicode-range:U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,U+0329,U+1D00-1DBF,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF}
@font-face{font-family:'Inter';font-style:normal;font-weight:100 900;font-display:swap;src:url(assets/fonts/inter-var-latin.woff2) format('woff2');unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD}
/* …mevcut :root ve kurallar (index.html:37-428) buradan devam… */
/* .glow (index.html:65-68) — filter animasyonu yerine yalnız opacity: */
@keyframes glowDrift{0%,100%{opacity:.24}50%{opacity:.34}}
.glow{position:fixed;border-radius:50%;filter:blur(90px);opacity:.26;pointer-events:none;z-index:0;animation:glowDrift 5.5s var(--ease-in-out) infinite;will-change:opacity}
</style>
<!-- assets/fonts/inter.css (showroom sayfaları hâlâ <link> ile alıyorsa) aynı iki @font-face, url(inter-var-latin-ext.woff2) / url(inter-var-latin.woff2) göreli -->

/* ============================================================
   B) Hero (index.html:476, hakkimizda.html:489 → build-pages.py:259) ve kart (index.html:532 örneği)
   ============================================================ */
<picture>
  <source type="image/avif" sizes="(max-width:960px) 100vw, 520px"
          srcset="assets/img/hero/bina-gece-3marka-480.avif 480w, assets/img/hero/bina-gece-3marka-800.avif 800w, assets/img/hero/bina-gece-3marka-1200.avif 1200w, assets/img/hero/bina-gece-3marka-1600.avif 1600w">
  <img src="assets/img/bina-gece-3marka.webp"
       srcset="assets/img/hero/bina-gece-3marka-800.webp 800w, assets/img/hero/bina-gece-3marka-1600.webp 1600w"
       sizes="(max-width:960px) 100vw, 520px" width="1600" height="905" fetchpriority="high" decoding="async"
       alt="ISIŞAH GROUP merkez binası — ISIŞAH ENDÜSTRİYEL, BORŞAH BORU ve SALMEX aynı çatı altında">
</picture>

<picture>
  <source type="image/avif" srcset="assets/img/cards/paslanmaz-boru-480.avif 480w, assets/img/cards/paslanmaz-boru-800.avif 800w"
          sizes="(max-width:560px) 100vw, (max-width:960px) 50vw, 390px">
  <img src="assets/img/cards/paslanmaz-boru-800.webp"
       srcset="assets/img/cards/paslanmaz-boru-480.webp 480w, assets/img/cards/paslanmaz-boru-800.webp 800w"
       sizes="(max-width:560px) 100vw, (max-width:960px) 50vw, 390px"
       width="800" height="533" loading="lazy" decoding="async" alt="Paslanmaz Boru">
</picture>

/* --- tools/deploy-ftp.sh yaması (srcset/url( yolları yoksa deploy eksik yükler ve kök sayfada kırık görsel olur) ---
   :14 satırının ALTINA (python bloğu içinde): */
    for m in re.findall(r'(?:src|href|data-src|poster)="(assets/[^"?]+)',s): used.add(m)
    for m in re.findall(r'(?:srcset|imagesrcset)="([^"]+)"',s):
        for part in m.split(','): used.add(part.strip().split(' ')[0].split('?')[0])
    for m in re.findall(r"url\((assets/[^)?]+)",s): used.add(m)
/* :21 altına: */
for fn in os.listdir('assets/products/512'): used.add('assets/products/512/'+fn)
/* :41 kök türetmesine EK: */
    s=s.replace('srcset="assets/','srcset="/showroom/assets/').replace(', assets/',', /showroom/assets/').replace('url(assets/','url(/showroom/assets/')

/* ============================================================
   C) Video lazy-load — index.html:895-900 YERİNE (IntersectionObserver: yakınken yükle, ekrandan çıkınca DURDUR)
   HTML tarafı aynı kalır: <video muted loop playsinline preload="none" poster="…"><source data-src="assets/img/….mp4" type="video/mp4"></video>
   (autoplay ATTRIBUTE'unu HTML'den de kaldır: autoplay, preload ipucunu ezer)
   ============================================================ */
(()=>{
  const prm=matchMedia('(prefers-reduced-motion: reduce)').matches;
  const c=navigator.connection||{};
  const lite=!!c.saveData||/(^|-)2g$/.test(c.effectiveType||'');
  const vids=[...new Set([...document.querySelectorAll('video source[data-src]')].map(s=>s.closest('video')))];
  const attach=v=>{ if(v.dataset.ready)return; v.querySelectorAll('source[data-src]').forEach(s=>{s.src=s.dataset.src;s.removeAttribute('data-src');}); v.dataset.ready='1'; v.load(); };
  const play=v=>{ attach(v); v.play().catch(()=>{}); };
  const stop=v=>{ if(!v.paused)v.pause(); };
  vids.forEach(v=>{ v.removeAttribute('autoplay'); v.muted=true; v.loop=true; v.playsInline=true; v.preload='none'; });
  if(prm||lite) return;                                  // poster kalır; kullanıcı isterse controls ile açar
  if(!('IntersectionObserver' in window)){ vids.forEach(play); return; }
  const io=new IntersectionObserver(es=>es.forEach(e=>e.isIntersecting?play(e.target):stop(e.target)),{rootMargin:'200px 0px',threshold:0.01});
  vids.forEach(v=>io.observe(v));
  document.addEventListener('visibilitychange',()=>{ if(document.hidden) vids.forEach(stop); });
})();

/* ============================================================
   D) fabrika.html — :101 ve :149-159 YERİNE  (mobil ≤5 MB varyant + saveData kapısı + Range yedeği)
   ============================================================ */
<div class="stage"><video id="film" muted playsinline preload="none" poster="assets/img/fabrika-poster.webp"></video></div>

const V={ desk:{src:'assets/img/fabrika-scrub.mp4',    v:'3'},   // 1440×810, 15,9 MB, GOP 0,5 s
          mob: {src:'assets/img/fabrika-scrub-540.mp4',v:'1'} }; // 960×540, 4,24 MB (crf32 g12) — ffmpeg aşağıda
const con=navigator.connection||{};
const small=matchMedia('(max-width: 820px), (max-height: 500px)').matches;
const slow=!!con.saveData||/(^|-)2g$|^3g$/.test(con.effectiveType||'')||(con.downlink&&con.downlink<3);
const pick=(small||slow)?V.mob:V.desk;
const SRC=pick.src+'?v='+pick.v;
function loadFilm(){
  fetch(SRC).then(async r=>{
    if(!r.ok||!r.body) throw 0;
    const total=+r.headers.get('Content-Length')||0, reader=r.body.getReader(), chunks=[]; let got=0;
    for(;;){ const {done,value}=await reader.read(); if(done)break; chunks.push(value); got+=value.length;
      const p=total?got/total:0.5; document.getElementById('lbar').style.transform='scaleX('+p.toFixed(3)+')';
      document.getElementById('lpct').textContent='%'+Math.round(p*100); }
    film.src=URL.createObjectURL(new Blob(chunks,{type:'video/mp4'}));
  }).catch(()=>{ film.preload='auto'; film.src=SRC; });   // sunucu Range 206 veriyor: akış yedeği
}
if(con.saveData){                                          // veri tasarrufu: kullanıcı onayıyla indir
  const lt=document.querySelector('.loader .lt'); lt.innerHTML='<button id="ldBtn" class="hbtn" type="button">Filmi yükle (~4 MB)</button>';
  document.getElementById('ldBtn').onclick=()=>{lt.textContent='Yükleniyor %0';loadFilm();};
} else loadFilm();

# ffmpeg — mobil varyant (ölçüldü: 4.240.340 B; GOP 12 kare = 0,5 s, kaynakla aynı scrub tepkisi)
ffmpeg -i assets/img/fabrika-scrub.mp4 -an -vf "scale=-2:540:flags=lanczos" -c:v libx264 -preset slow -crf 32 -profile:v high -level 4.0 -pix_fmt yuv420p -g 12 -keyint_min 12 -sc_threshold 0 -movflags +faststart assets/img/fabrika-scrub-540.mp4
# alternatif, daha yüksek kalite, 1 s GOP (ölçüldü 4.548.377 B):  -crf 29 -g 24 -keyint_min 24
# poster (tek kare) → sonra Pillow ile WebP
ffmpeg -ss 1 -i assets/img/fabrika-scrub.mp4 -frames:v 1 -vf "scale=1280:-2" -q:v 3 assets/img/fabrika-poster.jpg

/* ============================================================
   E) urunler.html — Three.js'i ilk ekrandan çıkarma iskeleti
   1) <canvas id="c"> (:290) ÖNCESİNE JS'siz katalog (SEO metni + gerçek LCP; 36 ürün ISISAH_LIST/SALMEX_LIST/BORSAH_LIST'ten üretilir)
   ============================================================ */
<main id="katalog" class="katalog">
  <h1>Endüstriyel Rezistans, Isı Eşanjörü ve Paslanmaz Boru Ürün Kataloğu</h1>
  <p class="k3d"><button id="enter3d" class="btn" type="button">3B Showroom'a gir</button>
     <small>3B sahne için ~150 KB script ve ürün dokuları yüklenir</small></p>
  <section data-b="isisah"><h2>ISIŞAH ENDÜSTRİYEL</h2><ul>
    <li><img src="assets/products/512/rezistans.webp" width="512" height="384" loading="lazy" decoding="async" alt="Özel tip flanş rezistansı">
        <h3>Özel Tip Flanş Rezistansları</h3><p>Daldırma ve boru tipi ısıtıcı elemanlar; sanayi ve proses uygulamaları için.</p></li>
    <!-- … diğer 35 ürün aynı kalıpta … -->
  </ul></section>
</main>

/* 2) :380 <script type="module"> gövdesini showroom-3d.js'e taşı; içini export async function boot({mobile}){ …mevcut kod… } ile sar.
      importmap (:374-378) aynı kalır. :366-372 ve :1029 zamanlayıcılarını sil (loader yalnız 3B başlarken görünür). */
<script>
(()=>{
  const btn=document.getElementById('enter3d'), c=navigator.connection||{};
  const mobile=matchMedia('(max-width: 820px)').matches||(navigator.deviceMemory&&navigator.deviceMemory<=4);
  const lite=!!c.saveData||/(^|-)2g$/.test(c.effectiveType||'');
  let started=false;
  const warm=()=>{ if(document.getElementById('mp3d'))return; const l=document.createElement('link'); l.id='mp3d'; l.rel='modulepreload'; l.href='vendor/three.module.min.js'; document.head.appendChild(l); };
  const start=async()=>{ if(started)return; started=true; document.body.classList.add('loading3d');
    try{ const m=await import('./showroom-3d.js'); await m.boot({mobile}); document.body.classList.add('in3d'); }
    catch(e){ document.body.classList.remove('loading3d'); btn.textContent='3B açılamadı — katalogdan devam edin'; } };
  btn.addEventListener('pointerenter',warm,{once:true}); btn.addEventListener('touchstart',warm,{once:true,passive:true});
  btn.addEventListener('click',start);
  if(!mobile&&!lite) (window.requestIdleCallback||(f=>setTimeout(f,1200)))(()=>{warm();start();},{timeout:2500}); // masaüstü: boşta kendiliğinden
  if(/^#hol=/.test(location.hash)) start();                                                                 // derin bağlantı = açık niyet
})();
</script>

/* 3) showroom-3d.js içindeki değişiklikler (satır no'lar urunler.html'e göre) */
// :535  renderer=new THREE.WebGLRenderer({canvas,antialias:!mobile,powerPreference:'high-performance'});
// :545  renderer.setPixelRatio(Math.min(devicePixelRatio, mobile?1:1.5));
// :566  if(!mobile){ const pmrem=new THREE.PMREMGenerator(renderer); scene.environment=pmrem.fromScene(new RoomEnvironment(),0.04).texture; pmrem.dispose(); }
//       else { scene.add(new THREE.HemisphereLight(0xffffff,0x222233,1.4)); }   // PMREM yok: ışığı telafi et
// :576/:584/:670  const ENV=mobile?'assets/img/m/':'assets/img/';  envTex(ENV+'tex-floor.webp',…)  envLoader.load(ENV+'pano-hall.webp',…)  envLoader.load(ENV+'lobby.webp',…)
// :696-702  loadProductTex — ImageBitmapLoader (decode ana iş parçacığı dışında) + mobil 512 seti:
const TEXDIR=mobile?'assets/products/512/':'assets/products/';
const bmp=new THREE.ImageBitmapLoader(); bmp.setOptions({imageOrientation:'flipY'});
function loadProductTex(img,label,cb){
  if(TEXCACHE[img]){cb(TEXCACHE[img]);return;}
  bmp.load(TEXDIR+img+'.webp',(b)=>{const t=new THREE.CanvasTexture(b);t.colorSpace=THREE.SRGBColorSpace;t.anisotropy=mobile?2:4;TEXCACHE[img]=t;cb(t);},
    undefined,()=>{const t=fallbackTex(label);TEXCACHE[img]=t;cb(t);});
}
// :1017-1023  ALLIMGS ısınmasını SİL. buildHall(brandKey) başında yalnız o holün listesi; komşu hol boşta:
function warmList(list){ list.forEach(d=>loadProductTex(d.img,d.h,()=>{})); }
//   buildHall içinde: warmList(hallDef(brandKey).list);  (window.requestIdleCallback||setTimeout)(()=>warmList(nextHallList),{timeout:4000});
// Not: TEXDIR+img birleşimi deploy-ftp.sh regex'ine görünmez → :21 altına products/512 walk'u eklendi (B bölümü).

/* ============================================================
   F) Plesk → Websites & Domains → isisah.com.tr → Apache & nginx Settings → "Additional nginx directives"
   Tuzak: bir location içinde add_header varsa üst seviyenin add_header'ları KALITILMAZ → HSTS her blokta tekrar.
   Önkoşul: ?v=<git-sha> damgası (immutable) ve http→https 301 (Hosting Settings → SEO-safe redirect; 80 portu Birhost'ta açılmalı) [ONAY]
   ============================================================ */
add_header Strict-Transport-Security "max-age=31536000" always;
location ~* ^/showroom/.*\.(?:woff2|avif|webp|jpe?g|png|svg|ico|mp4|webm|mp3|js|mjs|css)$ {
  expires 365d;
  add_header Cache-Control "public, max-age=31536000, immutable";
  add_header Strict-Transport-Security "max-age=31536000" always;
  access_log off;
}
location ~* \.html$ {
  add_header Cache-Control "no-cache";
  add_header Strict-Transport-Security "max-age=31536000" always;
}
# WP eski yollarına (/hakkimizda/, /urunler-2/ …) DOKUNMAZ; yalnız /showroom/ varlıkları ve .html kapsanır.

/* ============================================================
   G) tools/img-optimize.py — AVIF+WebP srcset, mobil dokular, logolar, favicon  (python3 3.14 + Pillow 12.2: avif ✓ webp ✓; cwebp/avifenc yok)
   ============================================================ */
#!/usr/bin/env python3
from PIL import Image; from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]/'assets'
def fit(im,w): return im if im.width<=w else im.resize((w,round(im.height*w/im.width)),Image.LANCZOS)
def out(im,p,fmt,**kw): p.parent.mkdir(parents=True,exist_ok=True); im.save(p,fmt,**kw); return p.stat().st_size
JOBS={'img/bina-gece-3marka.webp':('img/hero',(480,800,1200,1600)),'img/salmex-hat.webp':('img/hero',(800,1200,1600)),
 **{f'img/{n}.jpg':('img/cards',(480,800)) for n in ('paslanmaz-boru','kangal-boru','oval-boru','rezistanslar','firin','kanal-tipi','mobil-isitici','boykur')}}
for src,(dst,ws) in JOBS.items():
    im=Image.open(ROOT/src).convert('RGB'); stem=Path(src).stem
    for w in ws:
        i=fit(im,w); a=out(i,ROOT/dst/f'{stem}-{w}.avif','AVIF',quality=58,speed=4); b=out(i,ROOT/dst/f'{stem}-{w}.webp','WEBP',quality=82,method=6)
        print(f'{stem}-{w}: avif {a} B  webp {b} B')
for src,w in [('img/pano-hall.webp',1024),('img/lobby.webp',1280),('img/pano-end.webp',1024),('img/tex-floor.webp',512)]:   # showroom mobil çevre
    im=Image.open(ROOT/src).convert('RGB'); print(src, out(fit(im,w),ROOT/'img/m'/Path(src).name,'WEBP',quality=80,method=6))
for p in sorted((ROOT/'products').glob('*.webp')):                                                                         # 36 doku 512w, alfa korunur
    out(fit(Image.open(p).convert('RGBA'),512),ROOT/'products/512'/p.name,'WEBP',quality=80,method=6)
for src,w,dst in [('catalog/logo-isisah.webp',280,'catalog/logo-isisah-280.webp'),('catalog/logo-salmex.webp',280,'catalog/logo-salmex-280.webp'),
                  ('catalog/logo-borsah.webp',280,'catalog/logo-borsah-280.webp'),('catalog/logo-group.png',240,'catalog/logo-group-240.webp')]:
    print(dst, out(fit(Image.open(ROOT/src).convert('RGBA'),w),ROOT/dst,'WEBP',lossless=True))
im=Image.open(ROOT/'img/logo.png').convert('RGBA'); print('favicon', out(im.resize((64,round(64*im.height/im.width)),Image.LANCZOS),ROOT/'img/favicon-64.png','PNG',optimize=True))
im=Image.open(ROOT/'img/fabrika-poster.jpg').convert('RGB'); print('poster', out(im,ROOT/'img/fabrika-poster.webp','WEBP',quality=78,method=6))

/* H) Deploy sonrası ölçüm (aynı koşullar, docs/lighthouse-<tarih>/) */
for p in "" "showroom/urunler.html" "showroom/fabrika.html"; do n=${p:-root}; n=${n##*/}; npx lighthouse "https://isisah.com.tr/$p" --form-factor=mobile --screenEmulation.mobile --throttling-method=simulate --only-categories=performance --output=json --output-path="docs/lighthouse-$(date +%F)/lh_${n%.html}.json" --chrome-flags="--headless=new"; done
```

### Kanıt
TÜM SAYILAR ÖLÇÜLDÜ (uydurma yok). Kaynaklar ve komutlar:
1) Canlı HTTP (8 Eyl 2026 11:52 TR, curl -sI / -D -): HTTP/2 200, server: nginx, x-powered-by: PleskLin, content-length: 76631, etag "6a9e9cda-12b57", last-modified Mon 07 Sep 2026 11:15:38 GMT; Cache-Control/Expires/Strict-Transport-Security/alt-svc YOK. Accept-Encoding: br → content-encoding: br, 17.897 B indi (brotli -d ile açıldı, 76.631 B). three.module.min.js: content-type application/javascript, content-encoding br. TLS 1.3, ALPN h2, Let's Encrypt (02 Ağu–31 Eki 2026). /vendor/three.module.min.js kökte 404 (varlıklar yalnız /showroom/ altında).
2) Erişim kesintisi: 11:57 TR'den itibaren tüm https istekleri connect=0.000 total=20 s (curl --max-time 20, 3 ardışık); nc -z -w 6 46.20.7.162 80 → kapalı/filtreli; 443 → 12:09'da kapalı; WebFetch (farklı çıkış IP'si) → "connect ECONNREFUSED 46.20.7.162:443" iki kez. http://isisah.com.tr/ code=000. dig www.isisah.com.tr → kayıt yok. Bu yüzden 11:52 sonrası varlık başlıkları LH JSON'dan alındı.
3) Canlı ≠ repo: root.dec.html vs index.html diff → canlı title "ISIŞAH ENDÜSTRİYEL — Isının gücü…", canlı :32 preload /showroom/assets/img/bina-gece.webp, canlı :34-36 fonts.googleapis.com/gstatic preconnect+stylesheet, canlı :511/:644/:668/:687/:784 <video autoplay … preload="metadata"><source src=…>. git log: cd3b9b9 2026-09-08 11:59:42 +0300 "SEO sprint-1: … self-host Inter … lazy videolar"; -S araması: self-host, data-src ve 3marka preload'un üçü de bu commit'te.
4) Fontlar: md5 -q → inter-400/600/700-latin.woff2 üçü 65850a373e258f1c897a2b3d75eb74de (48.432 B); latin-ext üçü 01ba6c2a184b8cba08b0d57167664d75 (85.272 B); tablo taraması STAT+HVAR (değişken font). inter.css:1-6 altı @font-face. Toplam 6×: 401.112 B; 2×: 133.704 B. LH canlı Google Fonts: 2 dosya 85.435 + 48.983 B.
5) Lighthouse JSON (docs/lighthouse-2026-09-07/): root FCP 3,4 s, LCP 4,1 s (öğe <p class="lead">, render delay 3.437 ms), render-blocking fonts.googleapis 963 ms, uses-responsive-images 497 KiB (paslanmaz-boru 276.679 B israf, bina-gece 110.576, 3marka 92.283, logo-isisah 29.167), uses-long-cache-ttl 12 kaynak cacheLifetimeMs 0, toplam 5.503.464 B/17 istek (uretim-film 3.280.512 start 252 ms pri Low; robot 651.764; salmex 620.829), mainthread Style&Layout 619 ms / Other 757 ms. urunler: LCP 14,3 s (öğe loader <img logo-group.webp>), TBT 5.860 ms, Script Evaluation 10.205 ms, long tasks 5.659/1.379/940 ms, bootup 10.930 ms, three transfer 151.972 B (resource 670.681; unused 74.779), toplam 4.370.578 B/55 istek, cache 50 kaynak 0. fabrika: LCP 3,5 s (logo-group.png 79.357 B), fetch fabrika-scrub 15.941.826 B pri High 693→1.804 ms, toplam 16.161.245 B.
6) Repo satır kanıtları: index.html :31 icon logo.png, :32 preload, :34-35 font, :36-429 <style> 31.895 B, :65-68 glow filter animasyonu, :80 backdrop-filter, :387 (@media ≤960) glow animation:none, :476 hero img fetchpriority, :510/:643/:667/:686/:783 video, :532-553 sekiz JPEG, :897-900 IO lazy (pause yok). urunler.html :29 inter.css, :285/:296 logo-group.webp, :290 canvas, :349 bumper 21.176 B, :374-378 importmap, :380 module, :392-472 ürün listeleri, :535 antialias:true, :545 DPR 1,5, :566-567 PMREM RoomEnvironment, :576 tex-floor, :584 pano-hall, :670 lobby, :696-702 loadProductTex, :1017-1023 ALLIMGS, :1029 setTimeout 6000. fabrika.html :10-11, :95, :101 preload="auto", :106, :149-159 fetch blob. vizyon-misyon.html:489 salmex-hat loading="eager"; hakkimizda.html:489; her ikisinde :21 inter.css, preload yok. tools/deploy-ftp.sh :14 regex, :21 products, :24 fonts, :30 FTP, :41 kök yol çevirisi (srcset/url( yok). build-pages.py :8, :112-116, :259, :323.
7) Medya (ffprobe): fabrika-scrub.mp4 15.924.194 B, h264 High L4.0, 1440×810, 24 fps, 52,08 s, 2.443.566 bps, 2 b-frame, 104 keyframe (0,5 s GOP), atom sırası ftyp/moov/free/mdat (faststart ✓). Encode testleri (libx264 -preset slow, -an, faststart, bu Mac): 720p g24 crf28 7.418.952 B; 720p g12 crf28 9.105.154; 540p g12 crf27 6.934.363; 540p g12 crf30 5.159.057; 540p g24 crf29 4.548.377; 480p g12 crf28 5.380.260; 480p g12 crf30 4.411.568; 540p g12 crf32 4.240.340; 540p 12fps g6 crf27 6.640.585. Diğer mp4: uretim-film 3.416.643 B (1280×720, 22,6 s), uretim-robot 650.898, uretim-salmex 619.999. mp3 ×3 961.449 B (md5 farklı, kopya değil).
8) Görseller (Pillow 12.2, sips): kartlar 800w AVIF q60 / WebP q85: paslanmaz-boru 355.070→15.837/55.188; kangal-boru 324.432→16.680/34.776; oval-boru 194.366→14.314/21.126; boykur 111.811→21.811/35.216; mobil-isitici 147.578→25.832/47.178; kanal-tipi 90.129→18.656/29.610; rezistanslar 82.268→16.729/25.058; firin 61.127→9.824/14.698; toplam 1.366.781→139.683/262.850. Hero 3marka (1600×905, 108.344): AVIF q55 480w 8.845, 800w 18.804, 1200w 37.897, 1600w 63.970; WebP q80 12.360/27.510/55.738/97.138. salmex-hat 317.048 (1800×1013) → 1200w AVIF 60.833, WebP 102.650. Logolar: logo-isisah.webp 560×160 35.258 → 280w q90 15.204 (lossless 23.590); logo-group.png 300×120 79.134 → 240w lossless 12.602; logo.png 340×105 31.751 → 64 px 2.851. Showroom: pano-hall 275.448 (2048×1158) → 1024w 50.610; lobby 209.832 → 1280w 52.086; pano-end 132.242 → 1024w 32.124; tex-floor 121.808 → 512w 9.794; 36 ürün dokusu 3.086.422 → 512w q80 1.403.956. Araçlar: ffmpeg/ffprobe/brotli/sips/cjpeg var; cwebp, avifenc, magick yok; ffmpeg encoder'ları libsvtav1, libx264, libx265, libvpx (libwebp yok). assets/catalog/*_2..7.jpg 18 dosya referanssız (grep *.html tools/*.py boş).
9) Yerel sıkıştırma oranları (brotli -q 11 / gzip -9): index.html 76.480 → 16.613 / 19.241; urunler.html 82.021 → 21.898 / 24.707; three.module.min.js 670.681 → 135.314 / 166.250.


## sxo-2
**Skor:** SXO / SERP-niyet uyumu: 2,5/10. Gerekçe: (1) 8 hedef sorgunun 8'inde SERP'in ödüllendirdiği sayfa tipi (kategori/rehber, ürün detay, çözüm/sektör, şehir sayfası) bizde yok; 5 indekslenebilir URL'nin 5'i marka/kurumsal/deneyim tipi. (2) Tek tip uyuşan sorgu "endüstriyel rezistans üreticisi" (SERP = ana sayfa+hakkımızda) — ama canlı title hâlâ anahtar kelimesiz: sprint-1 (repo index.html:6) github.io aynasında canlı, isisah.com.tr'de DEĞİL (IP engeli, HANDOFF.md "8 Eyl 12:15 — DEPLOY BEKLİYOR"). (3) Ana sayfa 10-sn persona testi: satın alma mühendisi kısmen (lead cümlesini okursa), bayi ve ihracat müşterisi başarısız. (4) Sitenin en derin rakipsiz içeriği (demiryolu, index.html:707-772) kendi URL'si olmadan ana sayfaya gömülü. Önceki tur bulguları (robots/301/HSTS/fonts/Lighthouse) tekrarlanmadı; bu tur yalnız niyet-tip eşleşmesi ve ilk-ekran.


### Kritik
- CANLI TITLE'LAR HÂLÂ ESKİ — sprint-1 yayında değil. r.jina.ai ile 8 Eyl ölçüm: https://isisah.com.tr/ → 'ISIŞAH ENDÜSTRİYEL — Isının gücü, teknolojinin hassasiyeti · 1982'den bugüne'; /showroom/urunler.html → 'ISIŞAH GROUP — 3B Ürün Showroom'; /showroom/fabrika.html → 'Fabrika Turu — ISIŞAH GROUP'. Repo index.html:6 / urunler.html:6 / fabrika.html:6 anahtar kelimeli ve github.io aynasında canlı (curl doğrulandı). Ofis IP'sinden curl 443 timeout, WebFetch bile ECONNREFUSED 46.20.7.162:443 (sunucu bizim fetcher'ı da reddediyor). Düzeltme: SEO'da başka hiçbir iş bu çözülmeden ölçülemez → Birhost'a 85.97.200.122 whitelist talebi veya GitHub Actions FTP deploy (workflow_dispatch + repo secret; kullanıcı onayı). 15 Eyl ölçümü sprint-1 canlı değilse anlamsız.
- SAYFA TİPİ UYUŞMAZLIĞI (kök neden) — 'sanayi tipi rezistans' SERP'i: slug=sorgu, H1=sorgu, 900–1.200+ kelime kategori/rehber sayfaları (rezistansmarket.com/sanayi-tipi-rezistans ~900 kelime kategori-hub; serrezistans.com/sanayi-tipi-rezistans 1.200+ kelime, alt tipler listeli, tel+WhatsApp; sanalisi.com/urun-kategori/tup-rezistanslar/sanayi-tipi-rezistanslar/ WooCommerce kategori; ozenisi.com/kategori/rezistans/sanayi-tipi-rezistanlar/ kategori; cetinlerrezistans.com/blog/... rehber). Bizde bu sorguya en yakın varlık: index.html:542-543 tek cümlelik kart ('Boru ve daldırma tipi ısıtıcı elemanlar…') + urunler.html:393-441 JS dizisi (canlı görünür metin 236 kelime, Jina). Ana-sayfa-bölümü ≠ kategori sayfası. Düzeltme: kök /sanayi-tipi-rezistans.html kategori sayfası (hazir_kod A, build-pages.py page() ile; kök slug → tools/deploy-ftp.sh:37 glob otomatik yükler).
- DEMİRYOLU İÇERİĞİ ANA SAYFAYA GÖMÜLÜ — index.html:707-772: 6 ürün kartı (HVAC ısıtıcı, koltuk altı, TIJ, şasi, ray&makas 1000 W/230 V, özel), 1986→ proje geçmişi, test/malzeme blokları, referanslar TÜVASAŞ · TÜLOMSAŞ · TÜRASAŞ · Durmazlar · Bozankaya · MERAK · Safkar… Bu, sitenin en derin ve rakiplerde olmayan içeriği ama kendi URL'si yok; 'demiryolu ısıtıcı' SERP'i çözüm/ürün sayfaları ödüllendiriyor (savronik.com.tr/en/solutions/rail-transportation-systems/railway-switch-heating-system/ çözüm; revenga.com.tr/.../63-makas-isiticilari çözüm; ehtmuhendislik.com hizmet+ürün; trotec.com sektör). 'makas ısıtıcısı üreticisi' → baykalrezistans.com/urunler/tren-yolu-makas-isiticilari-….html ürün sayfası ~800-1.000 kelime, 4x6…8x6 kW, PLC, katalog PDF, breadcrumb. Düzeltme: bölümü /demiryolu-isitma-sistemleri.html (çözüm/sektör) + /ray-makas-isiticilari.html (ürün) olarak ayır; index'te 3 kart özet + link kalsın.
- SALMEX YANLIŞ SORGU HEDEFİNDE — 'kombi eşanjörü' ve 'yoğuşmalı kombi eşanjörü üreticisi' SERP'i %100 tüketici/servis/yedek parça (kombiparcadeposu.com.tr, yedek-parcam.com, yedepa.com, cimri.com fiyat, kombiteknik.net, pomeka.com, kombimuhendisi.com, YouTube; yedek parça markaları HRALE/SERMETA/Valmex). 'ısı eşanjörü üreticisi' = plakalı/endüstriyel eşanjör (alfalaval.com.tr, mersen.com.tr, termoline.com.tr, jeotes.com, experphe.com). SALMEX'in gerçek alıcısı kombi/kazan OEM'i; bu iki başlık sorgu kovalanmamalı. Doğru küme: 'sarmal eşanjör borusu paslanmaz' (SERP zayıf: tuzlapaslanmaz.com/paslanmaz-esanjor-borusu/, metalticareti.com/esanjor-borusu, Çin siteleri mtstainlesssteel/sincosteel, konukisi.com gövde-borulu) + 'yoğuşmalı eşanjör OEM üretici' + EN 'condensing heat exchanger coil manufacturer'. Bizde: index.html:557-564 üç kart + fabrika.html (canlı 151 kelime) + showroom #hol=salmex. Düzeltme: /yogusmali-esanjor.html ürün-ailesi sayfası (TR + EN sürüm; ürün EN adları urunler.html:445-463 en: alanlarında hazır).
- 'BURSA REZİSTANS' — 1982'den beri DOSAB'da üreten firma yerel SERP'te yok. SERP kalıbı: şehir sayfası (isierrezistans.com/blog/bursa-rezistans ~2.500 kelime, İstanbul firması; aymet.com/bursa-rezistans ~2.500 kelime, Beylikdüzü; isielektrik.com.tr/blog-tr/bursa-rezistans; isiturkrezistans.com/bursa-rezistans) + yerel firmaların ana sayfası (bursarezistans.com 2014 kuruluş, 8 kategori, tel+WhatsApp ilk ekran; ozturkrezistans.com; isiplustr.com; sgrezistans.com) + facebook.com/bursarezistans. GSC'de 'ısışah bursa' 13 tıklama ve '…san. tic. a.ş. fotoğraflar' 86 gösterim yalnız marka/harita niyeti. Düzeltme: (a) Google Business Profile sahiplen/doldur [ONAY: mevcut mu?], (b) /bursa-rezistans-ureticisi.html — GERÇEK yerel içerik (DOSAB fabrika fotoları hakkimizda.html:532, adres/harita, 1982, belgeler); İstanbul firmalarının kopya doorway kalıbı DEĞİL, (c) Organization JSON-LD'ye (index.html:18, build-pages.py:147 ORG) hasMap + areaServed ekle.
- ANA SAYFA İLK EKRAN PERSONA TESTİ (index.html:455-478; canlı metin Jina ile aynı) — Görülen: ribbon '3B Showroom yayında' (:456), kick 'KURULUŞ 1982 · DOSAB BURSA · ISO 9001:2015' (:465), H1 'Isının gücü, teknolojinin hassasiyeti.' (:466, patron seçimi — ürün söylemiyor), 40 kelimelik tek cümle lead (:467), CTA sırası 'Ürün Showroom'u Gez' (birincil, :469) / 'Ürünler' / 'Ara' (:470-471), marka çipleri, gece bina fotosu. SATIN ALMA MÜHENDİSİ: ne üretildiğini yalnız lead'i sonuna kadar okursa anlıyor; ürün-grubu listesi yok; birincil CTA Lighthouse 30 / LCP 14,3 s'lik 3B deneyime gönderiyor; katalog PDF/teknik föy linki sitede 0 (grep 'katalog|.pdf' index.html = 0; kataloglar isisahgroup.com.tr'de, HANDOFF assets/catalog) → KISMEN BAŞARISIZ. BAYİ: 'bayi' kelimesi sadece vizyon cümlesinde (index.html:616); başvuru/fiyat listesi/bayi girişi yok → BAŞARISIZ. İHRACAT MÜŞTERİSİ: EN sürüm/hreflang 0 (html lang=tr :2, hreflang yok), belgeler (TSE 1988, VDE 1997, UL 2010, CE EN 60204-1) yalnız hakkimizda.html:574-581, ihracat/ülke/referans ilk ekranda yok → BAŞARISIZ. Düzeltme: hazir_kod B (kategori çipleri + belge şeridi + CTA sırası), katalog PDF, EN (orta vade).

### Hızlı kazanımlar
- Deploy blokajını çöz ve sprint-1'i canlıya al (HANDOFF.md 'DEPLOY BEKLİYOR'): Birhost'a 85.97.200.122 whitelist veya GitHub Actions FTP (kullanıcı onayı). Doğrulama: r.jina.ai/https://isisah.com.tr/ Title satırı 'Endüstriyel Rezistans, Isı Eşanjörü ve Paslanmaz Boru Üreticisi | ISIŞAH GROUP Bursa' olmalı.
- Hero ilk ekran (index.html:465-475): kick satırına 'TSE · VDE · UL · CE' ekle (kaynak hakkimizda.html:574-581), CTA sırasını 'Teklif İste' (birincil) → 'Ürün Grupları' (#urunler) → '3B Showroom' (ribbon zaten showroom'u taşıyor, :456) yap, .bchips altına kategori-sayfası çip satırı ekle (hazir_kod B). H1'e dokunma.
- Katalog PDF'lerini yayınla: isisahgroup.com.tr'deki 3 katalog (HANDOFF: assets/catalog sayfa görselleri var) → assets/catalog/isisah-katalog.pdf vb.; hero ve iletişim bölümüne 'Katalog (PDF)' linki [ONAY: güncel sürüm ve dosya boyutu]. SERP'te baykalrezistans.com ve venco.com.tr ilk ekranda katalog indirme veriyor.
- index.html:533-564 ürün kartlarına showroom linkinin yanına 'Teknik detay →' (yeni kategori sayfası) linki ekle; showroom '#hol=' derin bağlantıları kalsın (urunler.html:517-522 çalışıyor).
- Footer'a 'Ürün Grupları' link bloğu (hazir_kod D): build-pages.py footer'ı index'ten regex ile alıyor (tools/build-pages.py:10) → tek düzenleme tüm kurumsal sayfalara yayılır; kategori sayfalarına site-geneli iç link.
- sitemap.xml'e yeni kök URL'leri ekle (hazir_kod E); yeni sayfaları KÖK slug ile üret ki tools/deploy-ftp.sh:37 ROOT_PAGES glob'u (yalnız kök *.html) otomatik yüklesin — alt klasör (/urunler/…) kullanırsan script değişmeli.
- urunler.html lobisine görünür statik ürün listesi: PRODUCTS dizisindeki 36 ürünü (urunler.html:393-471) lobi DOM'unda 'Tüm ürünler' katlanır <ul> olarak bas (display:none DEĞİL; details/summary). JSON-LD ItemList (urunler.html:27) var ama görünür metin 236 kelime; bot ve JS'siz önizleme ürün adı görmüyor.
- İsim netleştirme: index.html:545 'Endüstriyel Fırın' → 'Sanayi Tipi Isıl İşlem ve Kurutma Fırını' — 'endüstriyel fırın üreticisi bursa' SERP'i tamamen endüstriyel mutfak (Burtek, Starlinee, Ceya, armut.com) → yanlış niyet; 'ısıl işlem / kurutma fırını' kümesi hedeflenmeli.
- Organization JSON-LD (index.html:18 ve tools/build-pages.py:147 ORG): '@type':['Organization','Manufacturer'] değil — schema.org'da Manufacturer tipi yok; bunun yerine 'knowsAbout':['Sanayi tipi rezistans','Paslanmaz çelik boru','Yoğuşmalı eşanjör'] + 'hasMap' (GBP linki [ONAY]) + 'areaServed':'TR' ekle; kategori sayfalarında BreadcrumbList (hazir_kod A içinde).

### Orta vade
- SORGU → SAYFA → TİP HARİTASI (WebSearch 8 Eyl; hacim yazılmadı): 'sanayi tipi rezistans' → YENİ /sanayi-tipi-rezistans.html, tip KATEGORİ+rehber (H1=sorgu, alt tipler, teknik tablo, SSS, 900+ kelime). 'endüstriyel rezistans üreticisi' → MEVCUT / (ana sayfa, title sprint-1) + hakkimizda.html; tip ANA SAYFA — SERP'te safirezistans.com/tr, baykalrezistans.com(+/hakkimizda/), isierrezistans.com, uralrezistans.com, huzurrezistans.com ana sayfa/hakkımızda; eksik olan alt kategori derinliği. 'paslanmaz çelik boru üreticisi' → YENİ /paslanmaz-celik-rezistans-borusu.html, tip KATEGORİ; SERP genel boru/fittings (eskopaslanmaz.com/paslanmaz-boru/ 2.500-3.000 kelime ASTM A312/A269, EN 10204 tabloları; kuzeypaslanmaz.com ana sayfa+SSS; metalavm.com e-ticaret; europages dizin) → BORŞAH'ın nişi ince cidarlı Ø6–42 mm rezistans borusu; baş sorgu yerine 'paslanmaz rezistans borusu' (SERP: rezistansuretim.com/paslanmaz-rezistans-borusu/, telmika.com.tr/boru-rezistans/, isielektrik blog — çoğu rezistansçı, boru TEDARİKÇİSİ açısı boş). 'ısı eşanjörü üreticisi' ve 'kombi eşanjörü' → HEDEFLEME (plakalı eşanjör / tüketici yedek parça niyeti); yerine YENİ /yogusmali-esanjor.html, tip ÜRÜN AİLESİ TR+EN ('sarmal eşanjör borusu', 'yoğuşmalı eşanjör OEM'). 'demiryolu ısıtıcı' → YENİ /demiryolu-isitma-sistemleri.html, tip ÇÖZÜM/SEKTÖR (index.html:707-772 taşınır) + /ray-makas-isiticilari.html tip ÜRÜN. 'boya kurutma fırını' → HEDEFLEME (SERP kutu/tünel toz-yaş boya fırını: infraheat.com.tr/UrunListesi/224/5/ 60+ ürün, focusendustri, ems-boyamakineleri, acrotech); yerine 'infrared oto boya kurutucu' (SERP ürün sayfaları: elcon.com.tr/.../o-tipi-oto-boya-kurutma ~800 kelime 6 kW/3 ünite/LED kontrol; infraheat, fanped, inframak) → YENİ /boykur-infrared-oto-boya-kurutma.html tip ÜRÜN [ONAY: BOYKUR kW/lamba/kontrol]. 'bursa rezistans' → YENİ /bursa-rezistans-ureticisi.html tip YEREL SAYFA + GBP. Ek: 'kanal tipi elektrikli ısıtıcı üreticisi' SERP'i seri adlı ürün sayfaları (venco.com.tr VCE-VRE-VTL ~1.200 kelime+katalog, pitsan.com EKI serisi, sayfan, xair, solerpalau, kanaltipielektrikliisitici.com EMD) → YENİ /kanal-tipi-elektrikli-isitici.html tip ÜRÜN [ONAY: model/kW/ölçü tablosu].
- Kategori/ürün sayfa üretim hattı: tools/build-pages.py page() fonksiyonu (satır 96) zaten head/canonical/og/JSON-LD/header/footer üretiyor → ürün verisini tek JSON'a (ürün adı, en, p, gam, görsel = urunler.html PRODUCTS ile AYNI kaynak) al; hem showroom dizisi hem kategori sayfaları ondan türesin (HANDOFF yol haritası 'ürün/gam sayfaları tek JSON'dan' ile uyumlu). Her sayfa: H1=sorgu, 900+ kelime, teknik tablo, SSS (FAQPage), breadcrumb, showroom holü linki, mailto/tel CTA.
- EN sürüm (/en/ veya en-*.html) + hreflang: ihracat personası için zorunlu; SERP'te safirezistans ve baykalrezistans TR/EN. Ürün EN adları urunler.html:393-471 'en:' alanlarında hazır; SALMEX ve demiryolu sayfaları önce (OEM/ihracat alıcısı).
- Yerel ve dizin katmanı: Google Business Profile (adres DOSAB Ali Osman Sönmez Cad. No:11, tel +90 224 261 05 27 — build-pages.py:147 ORG ile birebir), europages.com.tr kaydı (SERP 'paslanmaz çelik boru üreticisi'nde europages listesi çıkıyor) [ONAY: mevcut kayıt var mı], turkishexporter.com.tr ('endüstriyel fırın' SERP'inde dizin).
- Eski WP URL'leri için 301 haritası — KULLANICI KARARI, WP dosyalarına dokunulmaz (Plesk/nginx kuralı): /urunler-2/ (canlı 200, 189 kelime, 35 jpg, title 'ÜRÜNLER – ISIŞAH ENDÜSTRİ') → /sanayi-tipi-rezistans.html veya kategori hub'ı; /hakkimizda/ (157 kelime) → /hakkimizda.html; /vizyon-misyon/ → /vizyon-misyon.html. Kategori sayfaları yayınlanmadan 301 verilmesin (hedef yoksa ana sayfaya toplanır, niyet kaybolur).
- Dönüşüm katmanı: mailto 'Teklif İste' (index.html:826, :851; urunler.html outro) yerine self-host teklif formu (HANDOFF 2. dalga: Plesk PHP mail + honeypot) — alanlar: ürün grubu, güç/gerilim/adet, dosya eki; 'Bayilik başvurusu' seçeneği (bayi personası); WhatsApp Business hattı (urunler.html WHATSAPP sabiti boş) — rakiplerde ilk ekran WhatsApp standart (bursarezistans, safirezistans, baykal, eskopaslanmaz).
- Rehber içerik (kategori sayfalarından SONRA): 'rezistans seçim rehberi', 'flanşlı rezistans nasıl boyutlandırılır' — SERP'te cetinlerrezistans.com/blog ve isierrezistans.com/blog kalıbı; kategori sayfalarına iç link verir, AI alıntı testinin ('Bursa'da sanayi tipi rezistans üreticisi kim?') kaynağı olur.
- Showroom'u deneyim katmanına indir: kategori sayfaları organik giriş olduğunda urunler.html (Lighthouse 30, LCP 14,3 s) 'ana ürün sayfası' rolünden çıkar; mobilde 3B yerine kart görünümü seçeneği; sitemap priority 0.9 → 0.6, kategori sayfaları 0.9.

### Ek alanlar / hazır kod


#### hazir_kod
```
# ============================================================
# A) tools/build-pages.py — dosyanın SONUNA (son print satırından ÖNCE) yapıştır; sonra: python3 tools/build-pages.py
#    Kök slug (sanayi-tipi-rezistans.html) → tools/deploy-ftp.sh:37 glob otomatik yükler. [ONAY] satırları katalogdan doldurulmadan YAYINLAMA.
# ============================================================
rez_body = '''
<section class="pad" id="tipler">
  <div class="wrap">
    <div class="sec-head reveal"><h2>Rezistans tipleri.</h2><p>Boru ve daldırma tipi ısıtıcı elemanlardan projeye özel flanşlı gruplara — hepsi kendi paslanmaz borumuzdan.</p></div>
    <div class="grid3">
      <article class="card" data-b="isisah"><div class="body"><div class="cat">Flanşlı</div><h3>Özel Tip Flanş Rezistansları</h3><p>Daldırma ve boru tipi ısıtıcı elemanlar; sanayi ve proses uygulamaları için.</p><a class="go3d" href="urunler.html#hol=isisah_rezistans">Showroom'da gör →</a></div></article>
      <article class="card" data-b="isisah"><div class="body"><div class="cat">Proses</div><h3>Proses Isıtıcı Ünitesi</h3><p>Endüstriyel proses hatları için flanşlı, kanal gövdeli ısıtıcı üniteler.</p><a class="go3d" href="urunler.html#hol=isisah_rezistans">Showroom'da gör →</a></div></article>
      <article class="card" data-b="isisah"><div class="body"><div class="cat">Endüstriyel mutfak</div><h3>Konveksiyonel Fırın Rezistansları</h3><p>Konveksiyonel fırınlar için dairesel ısıtıcı elemanlar.</p><a class="go3d" href="urunler.html#hol=isisah_mutfak">Showroom'da gör →</a></div></article>
      <article class="card" data-b="isisah"><div class="body"><div class="cat">Endüstriyel mutfak</div><h3>Fritöz Rezistansları (Yassı Rezistans)</h3><p>Endüstriyel fritözler için daldırma tip ısıtıcı raflar; hızlı ve homojen ısıtma.</p><a class="go3d" href="urunler.html#hol=isisah_mutfak">Showroom'da gör →</a></div></article>
      <article class="card" data-b="isisah"><div class="body"><div class="cat">Endüstriyel mutfak</div><h3>Bulaşık Makinesi Rezistansları</h3><p>Sanayi tipi bulaşık makineleri için boyler ve tank ısıtıcı elemanları.</p><a class="go3d" href="urunler.html#hol=isisah_mutfak">Showroom'da gör →</a></div></article>
      <article class="card" data-b="isisah"><div class="body"><div class="cat">Endüstriyel mutfak</div><h3>Makarna Haşlama Rezistansları</h3><p>Makarna haşlama üniteleri için daldırma tip ısıtıcı elemanlar.</p><a class="go3d" href="urunler.html#hol=isisah_mutfak">Showroom'da gör →</a></div></article>
      <article class="card" data-b="isisah"><div class="body"><div class="cat">Soğutma</div><h3>Defrost Rezistansları</h3><p>Soğutma sistemleri için defrost elemanları; Ø6,5–11,2 mm, yüksek sıcaklığa dayanıklı.</p><a class="go3d" href="urunler.html#hol=isisah_beyaz">Showroom'da gör →</a></div></article>
      <article class="card" data-b="isisah"><div class="body"><div class="cat">Beyaz eşya</div><h3>Ocak Rezistansları (Spiral)</h3><p>Elektrikli ocaklar için spiral boru rezistanslar; ev tipi ve sanayi tipi formlarda.</p><a class="go3d" href="urunler.html#hol=isisah_beyaz">Showroom'da gör →</a></div></article>
      <article class="card" data-b="isisah"><div class="body"><div class="cat">Beyaz eşya</div><h3>Fırın Rezistansları</h3><p>Ev tipi fırınlar için alt-üst ve turbo rezistanslar; farklı form ve güçlerde.</p><a class="go3d" href="urunler.html#hol=isisah_beyaz">Showroom'da gör →</a></div></article>
    </div>
  </div>
</section>

<section class="pad" id="neden">
  <div class="wrap prose reveal">
    <h2>Neden ISIŞAH sanayi tipi rezistans?</h2>
    <p><strong>Boru kendi hattımızdan.</strong> Rezistans kılıf borusunu grup şirketimiz BORŞAH BORU, Bursa DOSAB'daki hattında üretir: paslanmaz çelik, Ø6–42 mm çap, 0,35–2 mm et kalınlığı, argon/hidrojen koruyucu gaz altında TIG kaynak. Hammaddeden bitmiş ısıtıcıya tek çatı.</p>
    <p><strong>1982'den bu yana.</strong> Elektrikli ev aletlerinden ağır sanayiye ısıtma elemanları; endüstriyel mutfak, beyaz eşya, ağır sanayi, iklimlendirme (HVAC), raylı sistemler, savunma ve otomotiv gamları.</p>
    <p><strong>Belgeli üretim.</strong> TS EN ISO 9001:2015 (2004'ten beri), TSE (1988'den beri), VDE — DIN EN uygunluk (1997'den beri), UL (2010'dan beri), CE — EN 60204-1.</p>
    <p><strong>Projeye özel.</strong> Flanşlı gruplar ve proses üniteleri; ölçü, güç ve bağlantı projeye göre tasarlanır.</p>
  </div>
</section>

<section class="pad" id="teknik">
  <div class="wrap">
    <div class="sec-head reveal"><h2>Teknik özet.</h2><p>Teklif öncesi hızlı kontrol için.</p></div>
    <div class="tablewrap reveal"><table class="spec">
      <tr><th>Kılıf boru malzemesi</th><td>Paslanmaz çelik (BORŞAH BORU) — kalite: [ONAY: 304 / 316 / 321]</td></tr>
      <tr><th>Boru çapı</th><td>Ø6–42 mm aralığında (BORŞAH üretim aralığı); rezistans için standart çaplar: [ONAY]</td></tr>
      <tr><th>Et kalınlığı</th><td>0,35–2 mm</td></tr>
      <tr><th>Güç / gerilim</th><td>[ONAY: W–kW aralığı] · [ONAY: 230 V / 400 V]</td></tr>
      <tr><th>Bağlantı</th><td>Flanşlı · daldırma · boru tipi · [ONAY: rakor / kelepçe]</td></tr>
      <tr><th>Uygunluk</th><td>CE (EN 60204-1) · VDE · UL · TSE · ISO 9001:2015</td></tr>
    </table></div>
  </div>
</section>

<section class="pad" id="sss">
  <div class="wrap prose reveal">
    <h2>Sık sorulan sorular.</h2>
    <details open><summary>Özel ölçü ve güçte rezistans üretiyor musunuz?</summary><p>Evet. Flanşlı gruplar ve proses üniteleri projeye göre tasarlanır. Teklif için güç, gerilim, ısıtılan ortam, montaj ölçüleri ve adet bilgisi yeterlidir.</p></details>
    <details><summary>Rezistans borusunu nereden tedarik ediyorsunuz?</summary><p>Grup şirketimiz BORŞAH BORU'nun Bursa DOSAB'daki hattında ürettiğimiz paslanmaz çelik borudan (Ø6–42 mm, et 0,35–2 mm, TIG kaynak).</p></details>
    <details><summary>Hangi sektörlere üretim yapıyorsunuz?</summary><p>Endüstriyel mutfak, beyaz eşya ve ev aletleri, ağır sanayi, iklimlendirme (HVAC), raylı sistemler, savunma sanayi ve otomotiv.</p></details>
    <details><summary>Kalite belgeleriniz nelerdir?</summary><p>TS EN ISO 9001:2015 (2004'ten beri), TSE (1988), VDE — DIN EN uygunluk (1997), UL (2010) ve CE — EN 60204-1.</p></details>
  </div>
</section>

<section class="pad" id="teklif">
  <div class="wrap reveal">
    <h2>Teklif isteyin.</h2>
    <p class="lead">Güç, gerilim, ölçü ve adet bilgisini gönderin; DOSAB Bursa'daki mühendislik ekibimiz dönüş yapsın.</p>
    <div class="cta">
      <a class="btn" href="mailto:info@isisah.com.tr?subject=Teklif%20Talebi%20%E2%80%94%20Sanayi%20Tipi%20Rezistans">Teklif İste <span>→</span></a>
      <a class="btn ghost" href="tel:+902242610527">Ara: +90 224 261 05 27</a>
      <a class="btn ghost" href="urunler.html#hol=isisah_rezistans">3B Showroom: Rezistans holü</a>
    </div>
  </div>
</section>
'''

rez_ld = '''[{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Ana Sayfa","item":"https://isisah.com.tr/"},{"@type":"ListItem","position":2,"name":"Ürünler","item":"https://isisah.com.tr/#urunler"},{"@type":"ListItem","position":3,"name":"Sanayi Tipi Rezistans","item":"https://isisah.com.tr/sanayi-tipi-rezistans.html"}]},
{"@context":"https://schema.org","@type":"CollectionPage","name":"Sanayi Tipi Rezistans — ISIŞAH ENDÜSTRİYEL","url":"https://isisah.com.tr/sanayi-tipi-rezistans.html","inLanguage":"tr","isPartOf":{"@type":"WebSite","url":"https://isisah.com.tr/","name":"ISIŞAH GROUP"},"about":{"@type":"Thing","name":"Sanayi tipi rezistans"},"mainEntity":{"@type":"ItemList","itemListElement":[
{"@type":"ListItem","position":1,"item":{"@type":"Product","name":"Özel Tip Flanş Rezistansları","description":"Daldırma ve boru tipi ısıtıcı elemanlar; sanayi ve proses uygulamaları için.","brand":{"@type":"Brand","name":"ISIŞAH ENDÜSTRİYEL"},"manufacturer":{"@type":"Organization","name":"ISIŞAH Endüstriyel","url":"https://isisah.com.tr/"},"url":"https://isisah.com.tr/sanayi-tipi-rezistans.html#tipler"}},
{"@type":"ListItem","position":2,"item":{"@type":"Product","name":"Proses Isıtıcı Ünitesi","description":"Endüstriyel proses hatları için flanşlı, kanal gövdeli ısıtıcı üniteler.","brand":{"@type":"Brand","name":"ISIŞAH ENDÜSTRİYEL"},"url":"https://isisah.com.tr/sanayi-tipi-rezistans.html#tipler"}},
{"@type":"ListItem","position":3,"item":{"@type":"Product","name":"Konveksiyonel Fırın Rezistansları","brand":{"@type":"Brand","name":"ISIŞAH ENDÜSTRİYEL"},"url":"https://isisah.com.tr/sanayi-tipi-rezistans.html#tipler"}},
{"@type":"ListItem","position":4,"item":{"@type":"Product","name":"Fritöz Rezistansları (Yassı Rezistans)","brand":{"@type":"Brand","name":"ISIŞAH ENDÜSTRİYEL"},"url":"https://isisah.com.tr/sanayi-tipi-rezistans.html#tipler"}},
{"@type":"ListItem","position":5,"item":{"@type":"Product","name":"Bulaşık Makinesi Rezistansları","brand":{"@type":"Brand","name":"ISIŞAH ENDÜSTRİYEL"},"url":"https://isisah.com.tr/sanayi-tipi-rezistans.html#tipler"}},
{"@type":"ListItem","position":6,"item":{"@type":"Product","name":"Makarna Haşlama Rezistansları","brand":{"@type":"Brand","name":"ISIŞAH ENDÜSTRİYEL"},"url":"https://isisah.com.tr/sanayi-tipi-rezistans.html#tipler"}},
{"@type":"ListItem","position":7,"item":{"@type":"Product","name":"Defrost Rezistansları","brand":{"@type":"Brand","name":"ISIŞAH ENDÜSTRİYEL"},"url":"https://isisah.com.tr/sanayi-tipi-rezistans.html#tipler"}},
{"@type":"ListItem","position":8,"item":{"@type":"Product","name":"Ocak Rezistansları (Spiral)","brand":{"@type":"Brand","name":"ISIŞAH ENDÜSTRİYEL"},"url":"https://isisah.com.tr/sanayi-tipi-rezistans.html#tipler"}},
{"@type":"ListItem","position":9,"item":{"@type":"Product","name":"Fırın Rezistansları","brand":{"@type":"Brand","name":"ISIŞAH ENDÜSTRİYEL"},"url":"https://isisah.com.tr/sanayi-tipi-rezistans.html#tipler"}}]}},
{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
{"@type":"Question","name":"Özel ölçü ve güçte rezistans üretiyor musunuz?","acceptedAnswer":{"@type":"Answer","text":"Evet. Flanşlı gruplar ve proses üniteleri projeye göre tasarlanır. Teklif için güç, gerilim, ısıtılan ortam, montaj ölçüleri ve adet bilgisi yeterlidir."}},
{"@type":"Question","name":"Rezistans borusunu nereden tedarik ediyorsunuz?","acceptedAnswer":{"@type":"Answer","text":"Grup şirketimiz BORŞAH BORU'nun Bursa DOSAB'daki hattında ürettiğimiz paslanmaz çelik borudan (Ø6–42 mm, et 0,35–2 mm, TIG kaynak)."}},
{"@type":"Question","name":"Hangi sektörlere üretim yapıyorsunuz?","acceptedAnswer":{"@type":"Answer","text":"Endüstriyel mutfak, beyaz eşya ve ev aletleri, ağır sanayi, iklimlendirme (HVAC), raylı sistemler, savunma sanayi ve otomotiv."}},
{"@type":"Question","name":"Kalite belgeleriniz nelerdir?","acceptedAnswer":{"@type":"Answer","text":"TS EN ISO 9001:2015 (2004'ten beri), TSE (1988), VDE — DIN EN uygunluk (1997), UL (2010) ve CE — EN 60204-1."}}]}]'''

(ROOT/'sanayi-tipi-rezistans.html').write_text(page('sanayi-tipi-rezistans.html',
    'Sanayi Tipi Rezistans | Flanşlı, Daldırma ve Boru Tipi Rezistans Üreticisi — ISIŞAH Bursa',
    '1982\\'den beri Bursa DOSAB\\'da sanayi tipi rezistans üretimi: flanşlı, daldırma, boru tipi ve proses rezistansları. Kendi paslanmaz borumuzla (Ø6–42 mm), ISO 9001:2015, projeye özel imalat. Teklif isteyin.',
    'ISIŞAH ENDÜSTRİYEL · REZİSTANS · DOSAB BURSA', 'Sanayi Tipi Rezistans.',
    'Flanşlı, daldırma, boru tipi ve proses rezistansları — 1982\\'den bu yana Bursa DOSAB\\'da, kendi ürettiğimiz BORŞAH paslanmaz borusuyla.',
    rez_body, rez_ld,
    '<img src="assets/products/rezistans.webp" alt="Özel tip flanş rezistansı — ISIŞAH Endüstriyel, sanayi tipi rezistans" width="900" height="900" fetchpriority="high"><span class="tag">ISIŞAH · Sanayi Tipi Rezistans</span>'), encoding='utf-8')

# EXTRA_CSS (tools/build-pages.py:17) içine ekle:
#   .grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
#   .tablewrap{overflow-x:auto}
#   .spec{width:100%;border-collapse:collapse;font-size:.98rem}.spec th,.spec td{padding:12px 14px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}.spec th{color:var(--muted);font-family:var(--tech);font-size:.78rem;letter-spacing:.12em;text-transform:uppercase;width:32%}
#   .prose details{border-bottom:1px solid var(--line);padding:14px 0}.prose summary{cursor:pointer;font-weight:600;font-size:1.05rem}.prose details p{margin-top:10px}
#   @media(max-width:960px){.grid3{grid-template-columns:1fr}}

# ============================================================
# B) index.html:465 kick satırı ve :475 .bchips SONRASI (hero ilk ekran)
# ============================================================
<!-- index.html:465 — mevcut satırı bununla değiştir -->
<span class="kick">KURULUŞ <b>1982</b> · DOSAB BURSA · ISO 9001:2015 · TSE · VDE · UL · CE</span>

<!-- index.html:468-472 — CTA sırası: teklif birincil -->
<div class="cta">
  <a class="btn" href="mailto:info@isisah.com.tr?subject=Teklif%20Talebi">Teklif İste <span>→</span></a>
  <a class="btn ghost" href="#urunler">Ürün Grupları</a>
  <a class="btn ghost" href="urunler.html">3B Showroom</a>
  <a class="btn ghost" href="tel:+902242610527">Ara: +90 224 261 05 27</a>
</div>

<!-- index.html:475 .bchips satırının HEMEN ALTINA -->
<nav class="catchips" aria-label="Ürün grupları">
  <a href="sanayi-tipi-rezistans.html">Sanayi Tipi Rezistans</a>
  <a href="kanal-tipi-elektrikli-isitici.html">Kanal Tipi Isıtıcı</a>
  <a href="yogusmali-esanjor.html">Yoğuşmalı Eşanjör</a>
  <a href="paslanmaz-celik-rezistans-borusu.html">Paslanmaz Rezistans Borusu</a>
  <a href="demiryolu-isitma-sistemleri.html">Demiryolu Isıtma</a>
  <a href="boykur-infrared-oto-boya-kurutma.html">BOYKUR Boya Kurutma</a>
</nav>
<!-- index.html <style> içine -->
<style>
.catchips{display:flex;flex-wrap:wrap;gap:8px;margin-top:18px}
.catchips a{font-family:var(--tech);font-size:.78rem;letter-spacing:.06em;text-transform:uppercase;padding:8px 14px;border:1px solid var(--line);border-radius:40px;color:var(--steel);text-decoration:none;transition:border-color 200ms var(--ease-out),color 200ms var(--ease-out)}
@media(hover:hover){.catchips a:hover{border-color:#fff;color:#fff}}
.catchips a:active{transform:scale(.97)}
</style>

# ============================================================
# D) index.html:836 <footer> içine (build-pages.py footer'ı buradan alır → tüm sayfalara yayılır). Sayfa yayınlanmadan linki EKLEME (404 verir).
# ============================================================
<nav class="fcats" aria-label="Ürün grupları">
  <strong>Ürün grupları</strong>
  <a href="sanayi-tipi-rezistans.html">Sanayi Tipi Rezistans</a>
  <a href="kanal-tipi-elektrikli-isitici.html">Kanal Tipi Elektrikli Isıtıcı</a>
  <a href="yogusmali-esanjor.html">Yoğuşmalı Eşanjör (SALMEX)</a>
  <a href="paslanmaz-celik-rezistans-borusu.html">Paslanmaz Çelik Rezistans Borusu (BORŞAH)</a>
  <a href="demiryolu-isitma-sistemleri.html">Demiryolu Isıtma Sistemleri</a>
  <a href="boykur-infrared-oto-boya-kurutma.html">BOYKUR İnfrared Oto Boya Kurutma</a>
  <a href="bursa-rezistans-ureticisi.html">Bursa Rezistans Üreticisi</a>
</nav>

# ============================================================
# E) sitemap.xml — </urlset> ÖNCESİNE (yalnız yayınlanan sayfalar; lastmod gerçek tarih)
# ============================================================
  <url><loc>https://isisah.com.tr/sanayi-tipi-rezistans.html</loc><lastmod>2026-09-15</lastmod><changefreq>monthly</changefreq><priority>0.9</priority></url>
  <url><loc>https://isisah.com.tr/demiryolu-isitma-sistemleri.html</loc><lastmod>2026-09-15</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>
  <url><loc>https://isisah.com.tr/yogusmali-esanjor.html</loc><lastmod>2026-09-15</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>
  <url><loc>https://isisah.com.tr/paslanmaz-celik-rezistans-borusu.html</loc><lastmod>2026-09-15</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>
  <url><loc>https://isisah.com.tr/kanal-tipi-elektrikli-isitici.html</loc><lastmod>2026-09-15</lastmod><changefreq>monthly</changefreq><priority>0.7</priority></url>
  <url><loc>https://isisah.com.tr/boykur-infrared-oto-boya-kurutma.html</loc><lastmod>2026-09-15</lastmod><changefreq>monthly</changefreq><priority>0.7</priority></url>
  <url><loc>https://isisah.com.tr/bursa-rezistans-ureticisi.html</loc><lastmod>2026-09-15</lastmod><changefreq>monthly</changefreq><priority>0.7</priority></url>
# ve mevcut showroom satırı: priority 0.9 → 0.6 (deneyim katmanı).
```

### Kanıt
YÖNTEM (8 Eyl 2026): canlı sayfalar r.jina.ai reader üzerinden (ofis IP 443 DROP: curl 10 URL'de timeout; WebFetch ECONNREFUSED 46.20.7.162:443; Jina 200), github.io aynası curl, repo grep/sed (/Users/mehmetcansahin/isisah-scroll-world), SERP: WebSearch (ABD tabanlı — TR sıralaması farklı olabilir; konum/hacim YAZILMADI), rakip sayfa derinliği WebFetch özetleri.

CANLI ÖLÇÜM (Jina, kelime = görünür metin): / Title 'ISIŞAH ENDÜSTRİYEL — Isının gücü, teknolojinin hassasiyeti · 1982'den bugüne' 1.430 kelime · /showroom/urunler.html 'ISIŞAH GROUP — 3B Ürün Showroom' 236 · /showroom/fabrika.html 'Fabrika Turu — ISIŞAH GROUP' 151 · /hakkimizda.html 620 · /vizyon-misyon.html 307 · WP /urunler-2/ 'ÜRÜNLER – ISIŞAH ENDÜSTRİ' 189 kelime + 35 jpg (2018/03) · WP /hakkimizda/ 157. Ayna: mehmetcan12sahin.github.io/isisah-showroom/ title 'Endüstriyel Rezistans, Isı Eşanjörü ve Paslanmaz Boru Üreticisi | ISIŞAH GROUP Bursa' (= repo index.html:6) → sprint-1 aynada var, ana domainde yok; git log 3dd85f6 'deploy IP engeli nedeniyle bekliyor'.

REPO REFERANSLARI: index.html:456 ribbon; :465 kick; :466 H1; :467 lead; :469-471 CTA; :475 .bchips; :533-564 ürün kartları (#hol= linkleri); :557-564 SALMEX kartları; :585 stats; :616 'bayilerimizi' (tek bayi geçişi); :696 #boykur; :707-772 #demiryolu (railcard ×6, :723 '1000 W / 230 V', :727 proje geçmişi, :772 referanslar); :812-826 #iletisim mailto; :849-851 stickybar mailto. urunler.html:6 title; :27 ItemList 36 ürün; :315 H1 'Üç marka, üç kapı.'; :393-471 PRODUCTS (h/en/p); :485-502 ISISAH_CATS 8 gam; :517-522 #hol= derin bağlantı. fabrika.html:6-7 title+VideoObject; :100 H1. hakkimizda.html:518-523 & :574-581 belgeler (TSE 1988, VDE 1997, ISO 9001 2004, UL 2010, CE EN 60204-1). tools/build-pages.py:96 page(fn,title,desc,kick,h1,lead,body,ld,vis); :147 ORG JSON-LD; :253 hakkimizda çağrısı (kalıp). tools/deploy-ftp.sh:37 ROOT_PAGES = glob('*.html') (yalnız kök); :51-52 sitemap/robots kök yükleme. grep sonuçları: index.html 'katalog|.pdf|hreflang|bayi' → yalnız :616 vizyon cümlesi; html lang=tr (:2), EN sürüm yok.

SERP (WebSearch, ilk 6-9 sonuç, domain + tip):
1) 'sanayi tipi rezistans': rezistansmarket.com/sanayi-tipi-rezistans (kategori-hub/blog, H1=sorgu, ~900 kelime, fiyat yok, kategori linkleri) · sanalisi.com/urun-kategori/tup-rezistanslar/sanayi-tipi-rezistanslar/ (Woo kategori) · serrezistans.com/sanayi-tipi-rezistans (rehber/kategori, H1=sorgu, 1.200+ kelime, alt tipler, tel/WhatsApp) · ozenisi.com/kategori/rezistans/sanayi-tipi-rezistanlar/ (kategori) · cetinlerrezistans.com/blog/... (rehber) · isierrezistans.com/blog/sanayi-tipi-su-isitici-rezistans (blog). Kalıp: slug=sorgu, H1=sorgu, 900+ kelime, alt tip listesi, iletişim CTA. Bizde: index.html:542-543 (1 cümle) → tip uyuşmazlığı.
2) 'endüstriyel rezistans üreticisi': baykalrezistans.com/hakkimizda/ + / (ana sayfa ~650 kelime, 12 kategori, katalog PDF ×2, WhatsApp, TR/EN, 1970) · safirezistans.com/tr (ana sayfa, title 'Rezistans | Endüstriyel Rezistans Üreticisi – Safi', H1 'Endüstriyel Rezistans Üreticisi Safi Rezistans', 19 kategori, 2.000+ kelime, TR/EN, WhatsApp, 1983) · uralrezistans.com · huzurrezistans.com · anadolurezistans.com · isierrezistans.com (+/hakkimizda) · onurrezistans.com. Kalıp: ana sayfa/hakkımızda, title'da 'üreticisi'. Bizde: / — tip UYUŞUYOR, title sprint-1 ile uyuşur (canlıda değil), alt kategori derinliği 0.
3) 'paslanmaz çelik boru üreticisi': celikborupaslanmaz.com.tr (ana sayfa) · metalavm.com/paslanmaz-boru (e-ticaret kategori, fiyat) · aco.com.tr (drenaj — alakasız) · ankarametal.com.tr/urunler/paslanmaz-celik/paslanmaz-boru/ (kategori) · kuzeypaslanmaz.com (ana sayfa 1.200-1.400 kelime, SSS, 2006) · erturkpaslanmaz.com (ürün) · eskopaslanmaz.com/paslanmaz-boru/ (kategori 2.500-3.000 kelime, ASTM A312/A269, EN 10204, DIN 11850, ağırlık/DN tabloları, WhatsApp) · umitpaslanmaz.com (ana sayfa) · europages.com.tr (dizin). Niyet: genel boru/fittings ≠ BORŞAH ince cidar Ø6–42. Yardımcı: 'rezistans borusu paslanmaz üretici' → telmika.com.tr/boru-rezistans/, rezistansuretim.com/paslanmaz-rezistans-borusu/, isielektrik.com.tr blog, bymrezistans, techrom, baykal /urunler/boru-rezistanslar.html, elitrezistans, bursarezistans manşonlu, borurezistans.net — hepsi rezistans ÜRETİCİSİ; boru tedarikçisi açısı boş.
4) 'ısı eşanjörü üreticisi': mersen.com.tr (grafit/SiC ürün) · alfalaval.com.tr (kategori) · termoline.com.tr (plakalı, ana sayfa) · trox.com.tr (kategori) · tpsproje.com/urun/plakali-isi-esanjoru (ürün) · experphe.com (ana sayfa) · frigoduman.com.tr · jeotes.com/esanjor (kategori). Niyet: plakalı/endüstriyel eşanjör ≠ SALMEX OEM sarmal boru.
5) 'kombi eşanjörü': kombiparcadeposu.com.tr (yedek parça bilgi) · YouTube · cimri.com (fiyat karşılaştırma) · kombiteknik.net (servis blog) · pomeka.com (rehber) · sanaltesisat.com blog · kombimuhendisi.com · yedek-parcam.com (yedek parça e-ticaret) · rsrenerji.com blog. 'yoğuşmalı kombi eşanjörü üreticisi': kombiparcadeposu /yogusmali-esanjorler (HRALE/PRO-LAB/SERMETA/Valmex yedek parça) · yedepa.com · epey.com · ecostar.com.tr blog · dragonn.com.tr · kombi servis blogları. Niyet: tüketici/servis → hedeflenmez. 'sarmal eşanjör borusu paslanmaz': tuzlapaslanmaz.com/paslanmaz-esanjor-borusu/ (kategori) · mtstainlesssteel (Çin ürün) · metalticareti.com/esanjor-borusu · bowman-mdt.com/tr · chinaheatingexchanger · erametal.net · sincosteel (Çin) · konukisi.com (gövde-borulu) → zayıf SERP, fırsat.
6) 'demiryolu ısıtıcı': tr.trotec.com sektör · İTÜ tez PDF · erzincannet haber · savronik.com.tr/en/solutions/.../railway-switch-heating-system/ (çözüm) · tr.thermon.com/products/specialty-products/transportation (ürün) · revenga.com.tr/.../63-makas-isiticilari (çözüm) · formmuhendislik.com/cozumler/raylarda-buzlanma-onleme/ (çözüm) · ehtmuhendislik.com hizmet+ürün. 'makas ısıtıcısı üreticisi': Çağlayan Makas (alakasız, makas=scissors) · revenga · baykalrezistans.com/urunler/tren-yolu-makas-isiticilari-demir-yolu-makas-isiticilari.html (ürün, ~800-1.000 kelime, 4x6…8x6 kW, PLC, katalog PDF, breadcrumb, 'ÜCRETSİZ BİLGİ ALIN'). Bizde: index.html:707-772 (ana sayfa bölümü) → tip uyuşmazlığı; içerik derinliği rakipten fazla ama URL yok.
7) 'boya kurutma fırını': acrotech.com.tr (ana sayfa) · makinaturkiye.com kategori (pazar yeri) · slcoating.com (Çin) · infraheat.com.tr/UrunListesi/224/5/ (kategori 60+ ürün, spec yok, WhatsApp, H1 yok) · focusendustri.com.tr (kategori) · ems-boyamakineleri.com (ürün) · elektrosis.com (ürün) · beykaptanmakina.com (ürün) · ercanmakine.com (kategori). Niyet: kutu/tünel toz-yaş boya fırını ≠ BOYKUR mobil infrared. 'infrared boya kurutma sistemi oto': infratech.com.tr (kategori) · elcon.com.tr/.../o-tipi-oto-boya-kurutma (ürün ~800 kelime, 6 kW, 3 kısa dalga ünite 0,7-1,2 µm, LED kontrol, 4 görsel, Teklif Al ×2, breadcrumb) · infraheat ×3 kategori · fanped.com (ürün) · inframak.com (kategori). Bizde: index.html:696 bölüm + showroom kartı ('Tofaş Ar-Ge projesi' urunler.html:419 p:).
8) 'bursa rezistans': facebook.com/bursarezistans · isielektrik.com.tr/blog-tr/bursa-rezistans (şehir sayfası) · isiturkrezistans.com/bursa-rezistans (şehir) · bursarezistans.com (yerel ana sayfa, 2014, 8 kategori, tel+WhatsApp ilk ekran, ~800-1.000 kelime) · aymet.com/bursa-rezistans (şehir sayfası ~2.500 kelime, firma Beylikdüzü/İstanbul, 40+ kategori linki) · bursarezistans.com/iletisim · ozturkrezistans.com (Bursa, anahtar kelime yığılı title) · sgrezistans.com · isiplustr.com (Bursa) · isierrezistans.com/blog/bursa-rezistans (şehir sayfası ~2.500 kelime, İstanbul firması, 'TEKLİF AL!'). ISIŞAH: yok.
Ek) 'kanal tipi elektrikli ısıtıcı üreticisi': venco.com.tr/products/vce-vre-vtl-... (ürün ~1.200-1.400 kelime, katalog linki, form) · sayfan.com.tr (ürün detay) · xairiklimlendirme.com (ürün) · elektroteknik.com.tr (kategori) · solerpalau.com.tr (ürün+kategori) · pitsan.com EKI serisi (ürün) · mirsa.com.tr (ürün) · kanaltipielektrikliisitici.com (EMD) · havalandirmagross.com (ürün). Bizde: index.html:548-549 kart + urunler.html:409 → ürün sayfası yok. 'endüstriyel fırın üreticisi bursa': Burtek (Facebook), armut.com, erkasendustriyel, pimak, starlinee, budavarmis, ceyamutfak, turkishexporter → endüstriyel MUTFAK niyeti; ISIŞAH 'sanayi tipi ısıl işlem/kurutma fırını' (urunler.html:407 p:) farklı küme.

PERSONA 10-SN (ilk ekran, index.html:455-478 + canlı Jina metni birebir): görülen öğeler ribbon/kick/H1/lead/3 CTA/marka çipleri/bina fotosu; mobilde ek sticky 'Ara / Teklif İste' (:849-851). Eksikler grep ile doğrulandı: katalog/PDF 0, EN/hreflang 0, 'bayi' yalnız :616, belgeler yalnız hakkimizda.html:574-581, ürün-grubu linki ilk ekranda 0 (yalnız #urunler anchor). [ONAY] işaretliler: GBP kaydının varlığı, europages/turkishexporter kayıtları, BOYKUR kW/lamba/kontrol, kanal ısıtıcı model/kW tablosu, rezistans kılıf kalitesi 304/316/321 ve güç/gerilim aralıkları, katalog PDF güncel sürümü.
