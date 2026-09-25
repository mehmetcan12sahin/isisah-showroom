# Entegrasyon Doğrulama Raporu — revizyon/b2b (2026-09-25)

Bu rapor, 8 uygulama ajanının (S1, F, H, T, C, S2, G, P) çalışmasının bitmiş hâli üzerinde,
"I" (entegrasyon doğrulama) ajanı tarafından yapılan I1–I6 kontrollerinin sonucudur.
Bu ajan hiçbir repo dosyasını değiştirmemiştir; sadece `docs/revizyon-2026-09-25/` altına
ekran görüntüsü ve bu raporu yazmıştır. Tüm testler local'de (localhost:8080 / 8096) çalıştırılmıştır,
isisah.com.tr veya github.io mirror'ına hiçbir istek gitmemiştir.

## I1 — check-site.py

`python3 tools/check-site.py` çıktısı: **18 dosya, 14 HATA, 51 UYARI**.

14 HATA'nın **12'si yanlış-pozitif**: `check-site.py`'ın kendi `top_level_keys()` fonksiyonu
sadece tırnaksız (unquoted) JS anahtarlarını (`key:`) yakalayan bir regex kullanıyor; ama
`build-teklif.py` `KONU_MAP`/`URUN_MAP`'i `json.dumps()` ile tırnaklı üretiyor (`"agir-sanayi...":`).
Bu yüzden bu fonksiyon her zaman boş küme döndürüyor ve teklif.html'e giden
`teklif.html?konu=...` linklerinin hepsi "haritada tanımlı değil" diye HATA basılıyor —
11 kategori sayfası + fabrika.html, hepsi bu aynı kalıp. Bağımsız olarak `teklif.html`
içindeki `KONU_MAP`'i Python `json.loads()` ile ayrıştırıp 23 anahtarın da geçerli ve
referans verilen tüm slug'ların karşılığı olduğunu doğruladım — site kusuru değil,
check-site.py'ın parser hatası (ajan C/S1'in de kendi özetlerinde bildirdiği bulguyla örtüşüyor).

Geri kalan **2 HATA gerçek ama önemsiz**: `404.html`'de description/canonical eksik
(404 sayfası olduğu için SEO açısından önemi düşük).

51 UYARI ayrıntılı taranmadı (kapsam dışı — I görevi sadece HATA'ları raporlamayı istiyor);
hiçbiri HATA seviyesine yükselen bir kusur değil.

## I2 — Üreteç idempotency

4 üreteç (`build-products.py`, `build-pages.py`, `build-category-pages.py`, `build-teklif.py`)
art arda 2 kez çalıştırıldı; her koşudan önce/sonra tüm `*.html` dosyalarının sha256 checksum'ı
ve `git status --porcelain` çıktısı karşılaştırıldı.

**Sonuç: 4/4 üreteç idempotent.** İkinci koşudan sonra sıfır checksum farkı, sıfır git-status
değişikliği, tüm koşular exit=0. Her ajanın kendi idempotency iddiası doğrulandı.

## I3 — smoke-browser.mjs

`node tools/smoke-browser.mjs http://localhost:8080` → exit code 1, 3 kontrol de FAIL:

```
FAIL ana sayfa — FAIL beklenen bölümler eksik (wcard=4 vcard=0 tourbox=1)
FAIL showroom — HTTP 404
FAIL fabrika turu — HTTP 404
```

- **showroom / fabrika turu (404): sadece path-topolojisi farkı, gerçek kusur değil.**
  Script `/showroom/urunler.html` ve `/showroom/fabrika.html`'i sabit kodlamış (canlı deploy
  topolojisi — `deploy-ftp.sh` bu path'leri yeniden yazıyor); local preview repo kökünden
  servis ediyor. `curl` ile doğrulandı: `localhost:8080/urunler.html`=200,
  `localhost:8080/fabrika.html`=200, `localhost:8080/showroom/urunler.html`=404.
- **ana sayfa (vcard=0): gerçek ama beklenen, script eskimiş.** Şu anki `index.html`'de
  `class="vcard"` sayısı 0 — çünkü ajan H, brief'in IA sadeleştirme talebi (H2) kapsamında
  `#vitrin` 12 kartlık bölümü kasıtlı olarak kaldırdı. Smoke test bu redesign'dan önceki
  varsayımı kontrol ediyor; script'in kendisi güncellenmeli (benim dosya sahipliğim dışında).

## I4 — Ekran görüntüleri (before/after)

`git archive HEAD` ile çıkarılan HEAD snapshot'ı port 8096'da, güncel çalışma ağacı
localhost:8080'de servis edilerek Playwright ile karşılaştırıldı. 5 sayfa (index, urunler
[swMuted=1], fabrika, sanayi-tipi-rezistans, hakkimizda) × 4 genişlik (360/390/768/1440),
tam sayfa ek çekim 390/1440'ta; teklif.html sadece after (before yok, brief gereği).
Görseller: `docs/revizyon-2026-09-25/screens/{before,after}/<sayfa>-<genişlik>[-fold].png`.

Her after-sayfası scroll edilerek (native `loading="lazy"` görsellerin native lazy-load
eşiğine girmesi için adım adım kaydırma) yatay taşma / kırık görsel / konsol hatası kontrol
edildi.

**Sonuç: sadece 1 gerçek bulgu.**
- `[overflow] index.html @360px: scrollWidth=362 clientWidth=360 (Δ2px)` — ajan H'in kendi
  özetinde zaten bildirdiği, düzeltilmemiş, önemsiz (2px) yatay taşma.
- Kırık görsel: **0** (ilk taramada native lazy-load nedeniyle çok sayıda yanlış-pozitif
  çıktı; sayfa tam kaydırıldıktan sonra tekrar kontrol edilince hepsi temiz çıktı).
- Konsol hatası: **0** (tüm sayfa × genişlik kombinasyonlarında).

## I5 — Klavye-only geçiş

**index.html (390/1440):** Tab#1 skip-link'e düşüyor (PASS), dropdown tetikleyicisi Enter ile
`aria-expanded=true` açılıyor, Escape ile `aria-expanded=false`'a dönüp fokus tetikleyicide
kalıyor (PASS), 390'da hamburger menü Enter ile açılıp Escape ile kapanıp fokus geri
hamburger butonuna dönüyor (PASS).

**urunler.html:**
- `#catalogDialog` (liste paneli): `#catalogBtn`'e Enter → diyalog açılıyor, fokus tuzağı
  15 Tab boyunca tutuluyor, Escape kapatıp fokusu `#catalogBtn`'e geri veriyor (PASS).
  (İlk denemede genel `[role="dialog"][aria-modal="true"]` seçicisi DOM'da her zaman var olan
  `#inspectbar`'ı yakalayıp yanlış "fokus tuzağı tutmuyor" sonucu verdi — `#catalogDialog`'u
  ID ile hedefleyince gerçek davranış doğru çıktı: tuzak çalışıyor.)
- `#navPrev`/`#navNext`: 46×46px, klavye ile (focus+Enter) `posLabel` değişimini tetikliyor (PASS).
- **İncele / Teklif Al / E-posta düğmeleri (masaüstü/1440px'de, "künye kartı" `#infoIn`
  içinde) — P3 bulgusu:** Bir ürün seçildiğinde/hall'a girildiğinde bu düğmelerin ekran
  konumu (`getBoundingClientRect`) ~5-7 saniye boyunca sürekli kayıyor (İncele: 3.0s'de
  x≈1085 → 6.85s'de x≈1159, hâlâ ~1px/150ms hareket; Teklif Al linkinde de ölçüldü, aynı
  davranış: 4.0s'de x≈875 → 6.85s'de x≈962). Bu, HANDOFF.md'de belgelenen "künye kartı
  masaüstünde 3D projeksiyonla takip ediyor" mimarisinin bir sonucu — ürünün kendi
  idle/rotasyon animasyonunu 2D overlay'e izdüşürüyor. **Fonksiyonel etki yok**: hem
  zorlanmış tıklama (`{force:true}`) hem de klavye ile (`element.focus()` + Enter) her iki
  düğmede de sorunsuz çalışıyor, İncele diyaloğunu doğru açıyor (fokus `#inspectClose`'a
  gidiyor). **Etkilenen tek şey**: Playwright'ın normal `.click()` metodu (hedefin
  frame-to-frame konum kararlılığını bekleyen "actionability" kontrolü) bu sürekli kayma
  yüzünden 3-5s içinde timeout veriyor — hem İncele hem Teklif Al linkinde doğrulandı.
  **Bu, bu oturumda eklenen bir regresyon değil, önceden var olan davranış**: `git diff HEAD`
  incelemesinde bu oturumun `setInfo()`/künye kartı HTML üretimine (E-posta linki ekleme,
  `h2`→`h3`, İncele için klavye-erişilebilir `onclick` ekleme gibi) dokunduğu ama kartın
  ekran-konumu güncelleme/projeksiyon koduna hiç dokunmadığı görüldü; `inspectBtn`/`İncele`/
  `inspectbar` referans sayısı HEAD ile güncel dosyada birebir aynı (12/12). HEAD ağacında
  (port 8096) aynı senaryo hash-deep-link ile tekrarlanamadı (HEAD'de `#urun=` hash'i ile
  doğrudan hall'a giriş tetiklenmiyor, body "ready" durumunda kalıyor — muhtemelen bu
  oturumda geliştirilen deep-link özelliğinin bir parçası), ama kod-kimliği üzerinden
  projeksiyon/kayma davranışının önceden var olduğu güvenle söylenebilir.
  **Handoff**: otomatik regresyon testi yazacak biri (ör. S2) `#infoIn .act`/`.inspectBtn`
  üzerinde `page.click()` kullanırken `force:true` geçmeli veya tıklamadan önce ~5-7s
  beklemeli; aksi hâlde test flaky olur.

## I6 — İçerik koruması (content guard)

`git diff HEAD -- '*.html'` üzerinde eklenen (`+`) satırlar; rakam+birim, sertifika/ISO/TSE/
UL/CE/VDE, müşteri adları, "gönderildi", "garanti", "en büyük", "lider", "ilk" kalıpları için
regex taraması yapıldı, hunk-header satır numarası takip edilerek. Her eşleşme HEAD'deki tüm
`*.html` dosyalarının birleşik metninde aranarak moved (taşınmış) / new (yeni) diye
sınıflandı.

**120 ham eşleşme** (digits_unit:75, customer_name:36, certificate:5, first:4;
moved:27, new:93). Elle 120 satırın hepsi incelendi. Çoğu (~93 "new" damgalı olanların
büyük bölümü) CSS/JSON-LD/kod yorumu gibi bağlamlarda geniş regex'in yanlış-pozitifi
(örn. CSS'te `2px`, JSON-LD'de zaten var olan ürün açıklamaları farklı satır numarasıyla).

Gerçek/önemli bulgular:
1. **YENİ keşif (hiçbir önceki denetim/ajan bildirmemiş): `boya-kurutma-firini.html:584`**
   — "Türkiye'de ilk yerli imalat patentli infrared teknolojili oto boya kurutma ünitesidir —
   Tofaş Ar-Ge işbirliğiyle geliştirilmiştir" iddiası. Kaynağı `tools/build-category-pages.py:335`
   (sabit kodlanmış string). **Önceden var** (HEAD'de `boya-kurutma-firini.html:521`'de de
   aynı metin mevcut — bu oturumda eklenmemiş), ama doğrulanmamış patent + "ilk" iddiası,
   brief'in açıkça kırmızı-bayrak dediği kalıpla birebir örtüşüyor. **P1** (yüksek risk:
   doğrulanmamış patent/hukuki iddia, marka/hukuki sorumluluk riski) — kapsamım dışı
   (üreteç sahibi ajan G), düzeltmedim, sadece flag'liyorum.
2. 27 kişilik "Referanslarımızdan" müşteri listesi (index.html) — HEAD'deki eski
   "Referanslar:" ön-ekli listeyle aynı isimler, sadece başlık/wrap değişmiş — **taşınmış,
   fabrikasyon değil**.
3. `--line` design-token tutarsızlığı: `#1b1c26` (index/hakkimizda/teklif/kategori sayfaları)
   vs `#1d1e2a` (urunler.html/fabrika.html) — ajan H tarafından zaten bildirilmiş, küçük,
   düzeltilmemiş. **P3**.
4. Hero H1 (`"Isının gücü, teknolojinin hassasiyeti."`), istatistik bloğu
   (`data-count="44"/"3"/"8"/"100"`), `:root{}` palet token'ları, BORŞAH Ø6–42 mm / et
   0,35–2 mm, ve 1982/1986 kuruluş yılları — **hepsi HEAD ile bayt-bayt aynı**, bağımsız
   olarak Python regex/karşılaştırma ile doğrulandı (hem index.html hem urunler.html).

## Genel özet

| Kontrol | Sonuç |
|---|---|
| check-site.py | 14 HATA (12 yanlış-pozitif/parser hatası, 2 gerçek-önemsiz), 51 UYARI |
| Üreteç idempotency | 4/4 PASS (2 koşu, sıfır diff) |
| smoke-browser.mjs | 3/3 FAIL ama hepsi açıklanabilir (2 path-topoloji, 1 stale test) |
| Ekran görüntüleri | 5 sayfa × 4 genişlik before/after, 1 gerçek bulgu (360px Δ2px taşma) |
| Klavye-only | index.html PASS; urunler.html PASS + 1 P3 (masaüstü künye kartı kayması) |
| İçerik koruması | 120→triaged; 1 YENİ P1 (BOYKUR patent iddiası), 1 bilinen P3 (--line token) |
| Sabit gerçekler | H1/istatistik/palet/BORŞAH ölçüleri/kuruluş yılları: değişmemiş, doğrulandı |
