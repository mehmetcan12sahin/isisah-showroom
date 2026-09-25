# server/teklif.php — devreye alma

`server/` klasörü `tools/deploy-ftp.sh` tarafından YÜKLENMEZ (script yalnız kök `*.html` +
`showroom/` içeriğini tarar). Bu klasördeki hiçbir dosya otomatik olarak canlıya gitmez —
aşağıdaki adımlar elle yapılır.

`teklif.php` bu ortamda test edilmedi — bu makinede `php` komutu yok (`command -v php` boş
döner), yalnızca statik olarak okunarak yazıldı. Devreye almadan önce mutlaka gerçek bir PHP
ortamında (önce yerelde `php -l server/teklif.php` ile sözdizimi kontrolü, sonra Plesk'te)
test edin.

## 1. Ön koşullar

- Barındırmada gerçekten PHP çalıştığının Plesk panelinden teyidi (bu oturumda yalnız dolaylı
  kanıt var: `httpdocs`'ta WordPress bulunması → PHP muhtemelen çalışıyor, ama teyit edilmedi).
- PHP `mail()` fonksiyonunun sunucuda aktif ve SPF/DKIM açısından `FROM_ADDRESS` alan adına
  uygun yapılandırılmış olması (aksi halde e-postalar spam'e düşer veya reddedilir).
- `mbstring` ve `ctype` eklentileri (paylaşımlı barındırmada genelde varsayılan açık).

## 2. Sabitleri doldur/gözden geçir (dosyanın başı)

- `RECIPIENT` — teklif e-postalarının gideceği kutu. Şu an `info@isisah.com.tr`; işletme
  ayrı bir satış/teknik kutusu istiyorsa değiştirin.
- `FROM_ADDRESS` — **placeholder** (`teklif-formu@isisah.com.tr`). Plesk'te bu adresin var
  olduğunu/alan adına ait olduğunu doğrulayın; yoksa `mail()` sunucu tarafından reddedilebilir
  veya alıcıda spam'e düşer. Kullanıcı girdisinden ASLA türetilmez — sabit kalmalı.
- `ALLOWED_ORIGIN` — fetch ile bu uca POST edebilecek kaynaklar. Varsayılan
  `https://isisah.com.tr,https://mehmetcan12sahin.github.io` (ana site + github.io aynası;
  HANDOFF.md'deki "action MUTLAK URL olmalı, ayna da çalışsın" kararı nedeniyle ayna da
  buraya cross-origin istek atabilmeli). Alan adı değişirse güncelleyin.
- `RATE_LIMIT_DIR` — boş bırakılırsa `sys_get_temp_dir()` kullanılır. Plesk'te kalıcı bir dizin
  istiyorsanız **httpdocs dışında**, web'den erişilemeyen bir yol verin (örn. `private/` altı).

## 3. Yükle

`server/teklif.php` dosyasını **`httpdocs/teklif.php`** olarak yükleyin (kök, `showroom/`
DIŞINDA — `teklif.html` de köke gidiyor, aynı hizada kalsın).

## 4. `build-teklif.py`'de uç noktayı ayarla

`tools/build-teklif.py` içinde:

```python
FORM_ENDPOINT = ''
```

satırını **mutlak URL** ile değiştirin:

```python
FORM_ENDPOINT = 'https://isisah.com.tr/teklif.php'
```

Göreli bir yol (`/teklif.php`) YAZMAYIN — HANDOFF.md'deki 2. Dalga kararı gereği uç nokta
mutlak olmalı, çünkü site github.io aynasında (`mehmetcan12sahin.github.io`) da yayında ve
göreli yol orada `mehmetcan12sahin.github.io/teklif.php`'ye (yok, 404) işaret eder.

Değiştirdikten sonra yeniden üretin ve `teklif.html`'i deploy listesine dahil edin:

```bash
python3 tools/build-teklif.py
```

## 5. Test sırası (gerçek müşteriye ASLA deneme göndermeyin)

1. Yerelde `php -l server/teklif.php` ile sözdizimini doğrulayın (bu ortamda `php` yok, başka
   bir makinede/CI'de yapın).
2. Plesk'e yükledikten sonra **sandbox/test alıcısı** ile uçtan uca deneyin: `RECIPIENT`'ı
   geçici olarak kendi test kutunuza çevirip gerçek bir form gönderimi yapın, e-postanın
   doğru konu/gövde/Reply-To ile geldiğini doğrulayın, SONRA `RECIPIENT`'ı gerçek kutuya geri
   alın.
3. Hata yollarını test edin: bal küpü doldurulmuş istek (400 bekleniyor), 4 saniyeden kısa
   sürede gönderim (400), aynı IP'den art arda `RATE_LIMIT_MAX` üstü istek (429), eksik alan
   (400 + `fields` listesi), geçersiz Origin başlıklı istek (403).
4. Ancak bu testler net bittikten sonra site üzerinden gerçek kullanıcı trafiğine açın.

## 6. Bilinen sınırlar / veri ihtiyaçları (data_needed'e bakın)

- Dosya eki YOK (v1 kapsamı dışı — brief §10, "gerçekten ihtiyaçsa" notu; şu an hiçbir akışta
  teknik çizim eki talebi yok).
- KVKK aydınlatma metni formda YOK — `tools/build-teklif.py`'deki `tkvkk-slot` yorumlu boş
  kalıyor; şirket onaylı metin gelince oraya `<p>` olarak eklenip generator yeniden çalıştırılmalı.
  Onay kutusu (checkbox) atıfta bulunduğu metin olmadan EKLENMEMELİDİR.
- `mail()` başarısı e-postanın gerçekten teslim olduğu anlamına gelmez (SMTP kuyruğa
  girdiğini gösterir) — teslim garantisi için Plesk sunucu loglarına bakmak gerekir.
