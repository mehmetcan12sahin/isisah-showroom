---
name: isisah-deploy
description: ISIŞAH GROUP sitesini (isisah.com.tr + github.io aynası) yayınlar ve canlıda doğrular. Kullanıcı "deploy et", "canlıya al", "yayınla", "push'la" dediğinde veya ~/isisah-scroll-world'de yayınlanacak değişiklik biriktiğinde devreye girer.
---

# ISIŞAH Site Yayın Hattı

Repo: `~/isisah-scroll-world`. İKİ hedef var, ikisi de güncellenmeli:

| Hedef | Ne | Nasıl |
|---|---|---|
| **ANA CANLI** | https://isisah.com.tr/ (kök ana sayfa) + /showroom/* | `bash tools/deploy-ftp.sh` |
| Ayna | https://mehmetcan12sahin.github.io/isisah-showroom/ | `git push origin main` |

## Sıra
1. Commit (Türkçe mesaj, ne değiştiyse özetle) → `git push origin main`.
2. `bash tools/deploy-ftp.sh` — showroom dosyalarını FTP'ler VE kök `httpdocs/index.html`'i türetip yükler.
   - Kimlik: `~/.isisah-ftp.netrc` (git DIŞINDA, repoya girmez).
   - Bash timeout'unu uzun tut (600000); yine de kesilirse eksikleri tek tek yükle:
     `curl -s --netrc-file ~/.isisah-ftp.netrc -T <dosya> "ftp://ftp.isisah.com.tr/httpdocs/showroom/<dosya>"`
3. Kök türetimi (script yapar; elle gerekirse aynı kuralları uygula): repo `index.html` üzerinde
   `src="assets/` → `src="/showroom/assets/`, `href="assets/` → `href="/showroom/assets/`,
   `href="urunler.html` → `href="/showroom/urunler.html`, `poster="assets/img/` → `poster="/showroom/assets/img/`,
   `href="fabrika.html"` → `href="/showroom/fabrika.html"` → `httpdocs/index.html`e yükle.
   Yeni sayfa/yol türü eklersen bu kural setine (script + bu skill) da ekle.

## Canlı doğrulama (yayın bitmeden kapatma)
- `bash tools/smoke-test.sh` — deploy scripti sonunda OTOMATİK koşar; elle de çalıştırılabilir. curl katmanı (HTTP/içerik/Range) + Playwright katmanı (3 sayfa, konsol hataları; bağımlılık `~/.isisah-smoke/node_modules/playwright`, yoksa `npm i --prefix ~/.isisah-smoke playwright`). "DUMAN TESTİ TEMİZ" görmeden işi kapatma.
- Değişen sayfa: `curl -s "https://isisah.com.tr/...?v=$(date +%s)" | grep <yeni içerik>` (≥1).
- Yeni statik dosya: HTTP 200; **video ise ayrıca `-H "Range: bytes=0-1023"` → 206** (Safari şartı).
- github.io tarafı: Pages build ~1-2dk; `gh api repos/mehmetcan12sahin/isisah-showroom/pages/builds/latest --jq .status`.
- Değişen video/medya dosya adı aynı kaldıysa HTML'de `?v=N` cache-buster artır.

## Kurallar / tuzaklar
- **WP sitesine DOKUNMA**: `httpdocs/` kökünde bizim olan yalnız `index.html`, `sitemap.xml`, `googlebfb5098152a94f7b.html` (Search Console doğrulaması — ASLA silme) ve `showroom/` dizini. `wp-*` her şey eski site; kök `index.html` silinirse eski WP ana sayfası geri gelir (bilinçli geri dönüş yolu).
- Yeni sayfa eklendiyse: `sitemap.xml`'e URL ekle (kök + showroom kopyası aynı dosya) ve FTP'de HEM `showroom/sitemap.xml` HEM kök `sitemap.xml` güncelle.
- CDN/tarayıcı HTML'i cache'ler → kullanıcıya "Cmd+Shift+R" hatırlat.
- Localhost python server byte-range VERMEZ → videolar lokalde oynamayabilir; video doğrulaması canlıda yapılır.
- Search Console: sahiplik kullanıcının Chrome'undaki Google hesabında; büyük içerik değişiminde URL denetimi → "dizine eklenmesini iste" (kullanıcının Chrome'u üzerinden, izinle).
