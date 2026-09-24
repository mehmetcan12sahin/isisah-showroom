# isisah.com.tr — Faz 1 teknik envanter (24 Eylül 2026)

Eski denetim bulguları güncel kaynak + canlı sitede tek tek yeniden doğrulandı. Varsayım yapılmadı — her satır curl/grep/kod okumasıyla teyitli.

## 1. URL / kanonik / sitemap
- Sitemap: **16 URL**, hepsi canlıda **200**, hepsinin `<link rel="canonical">`'ı kendi URL'ine self-referencing (doğru).
- `/showroom/` altında **13 kök-sayfa kopyası** var (hakkimizda, vizyon-misyon, 11 kategori/marka sayfası — deploy script'in showroom klasörüne de kopyaladığı ham dosyalar). Hepsinin canonical'ı kök URL'e işaret ediyor → **duplicate-content riski yok**, sadece gereksiz FTP transferi (küçük, önemsiz).
- `urunler.html` / `fabrika.html` sadece `/showroom/` altında var, kökte kopyası yok (doğru).

## 2. HTTP / HTTPS / 404
- `http://isisah.com.tr/` → **200, redirect yok** (eski bulgu hâlâ geçerli — Plesk/nginx seviyesinde 301 kuralı eksik).
- `www.isisah.com.tr` → **DNS çözülmüyor** (000, eski bulgu hâlâ geçerli).
- 404 davranışı: **eski denetimin "hâlâ WP teması" iddiası artık YANLIŞ** — gerçek 404 kodu + kendi `404.html`'i dönüyor (`Sayfa bulunamadı — ISIŞAH ENDÜSTRİ`). Bu ara düzeltilmiş.
- robots.txt: doğru, `Sitemap:` satırı var, WP `/wp-admin/` korunuyor. AI bot izinleri (GPTBot, ClaudeBot vb.) tanımlı ama dosyanın kendi yorumu doğru not düşmüş: sunucudaki 502 kuralı kalkmadan bu blok etkisiz.

## 3. Sıkıştırma / header
- Brotli sıkıştırma **çalışıyor** (`content-encoding: br`, nginx) — sorun yok.
- **Cache-Control header hiçbir statik kaynakta yok** (HTML, woff2, webp, sitemap.xml hepsi kontrol edildi, hiçbirinde `Cache-Control` dönmüyor) — eski bulgu **doğrulandı, hâlâ geçerli**. Sunucu/Plesk config seviyesinde, repo'dan düzeltilemez.

## 4. JSON-LD (bu oturumda düzeltildi)
- 11 kategori/marka sayfasında `CollectionPage`+`BreadcrumbList` iki JSON kökü aynı `<script>` içinde array'e sarılmadan yapıştırılmıştı → `JSON.parse` "Extra data" hatası. **Düzeltildi, 17/17 sayfa artık geçerli JSON, canlıya alındı.**
- Sayfa başına şema türü haritası:
  - `index.html`: Organization, Brand, PostalAddress, ContactPoint, EducationalOccupationalCredential
  - `hakkimizda.html`: Organization, AboutPage, Brand, PostalAddress
  - `vizyon-misyon.html`: Organization, WebPage, Brand, PostalAddress
  - `urunler.html`: Organization, CollectionPage, ItemList, Product, Brand, BreadcrumbList, WebSite
  - `fabrika.html`: Organization, VideoObject — **BreadcrumbList yok** (küçük eksik, diğer tüm sayfalarda var)
  - 11 kategori/marka sayfası: CollectionPage, ItemList, Product, Brand, BreadcrumbList, WebSite (tutarlı)

## 5. Font (bu oturumda düzeltildi)
- `inter-400/600/700-latin(-ext).woff2` **byte-eşitti** (Inter zaten wght 100-900 variable font) — 3 ağırlık aynı içeriği 3 ayrı URL'den indiriyordu (~267KB gereksiz tekrar, eski bulgu doğrulandı).
- **Düzeltildi**: `inter.css` artık 2 `@font-face` (latin/latin-ext), `font-weight:100 900` aralığıyla tek dosyaya işaret ediyor. 4 gereksiz kopya silindi. Tarayıcıda variable font axis'in ağırlığa göre gerçek glyph genişliği ürettiği doğrulandı (canvas measureText: 400→486px, 600→494px, 700→498px, aynı metin) — kalın/yarı-kalın metin zaten doğru render oluyordu, sorun sadece bayt tekrarıydı.
- Sunucuda eski 4 dosya hâlâ duruyor (orphan, referans yok, zararsız — deploy script sadece yükler, silmez).

## 6. Showroom (urunler.html) — ALLIMGS eager-load (DÜZELTİLMEDİ, Faz 3 kapsamı)
- **Doğrulandı, eski bulgu hâlâ geçerli**: `ALLIMGS=[...ISISAH_LIST,...SALMEX_LIST,...BORSAH_LIST]` — **38 ürünün TAMAMI** (3 marka birleşik, 3.0MB webp) lobiye girişte, kapı seçiminden ÖNCE eager yükleniyor. Loader (`#loader`/`body.ready`) bu 38 texture'ın tamamı yüklenene kadar (`warmed>=ALLIMGS.length`) kapanmıyor.
- **Ek confirmed bug**: `setTimeout(finishLoad,6000)` (satır 1096) — 6 saniye sonra yükleme bitmemiş olsa da loader'ı gizleyip "%100" gösteriyor. Gerçek yükleme durumuyla "başarı" iddiası ayrışmamış — eski denetimin "6-7 saniyelik timeout" bulgusu tam doğrulandı.
- Düzeltme kapsamı büyük (lobi→hol→ürün kademeli yükleme mimarisi) — bu oturumda dokunulmadı, ayrı faz gerektiriyor.

## 7. İç link haritası — deep-link bütünlüğü
- Index.html kartları + 11 kategori/marka sayfasının `urunler.html#hol=<key>` bağlantıları, `urunler.html`'in gerçek `ISISAH_CATS`/`BRANDS` anahtarlarıyla (`isisah_rezistans`, `isisah_mutfak`, `isisah_beyaz`, `isisah_agir`, `isisah_hvac`, `isisah_rayli`, `isisah_savunma`, `isisah_otomotiv`, `salmex`, `borsah`) **%100 eşleşiyor** — kırık deep-link yok.

## Sonuç — öncelik sırası (düzeltilmemiş, doğrulanmış kalemler)
1. **Showroom ALLIMGS eager-load + sahte 6sn timeout** — en yüksek etkili, en büyük iş (Faz 3).
2. **Cache-Control / HTTP→HTTPS 301 / www DNS** — sunucu (Plesk/nginx) config, koddan değil, yetkili erişim gerekiyor.
3. `fabrika.html`'e BreadcrumbList eklenmesi — küçük, hızlı.
4. `/showroom/` kopyalarının FTP'ye gitmemesi (deploy script optimizasyonu) — küçük, kozmetik.

Bu oturumda düzeltilip canlıya alınanlar: JSON-LD geçersizliği (11 sayfa), font byte-tekrarı (267KB).
