---
name: isisah-urun-ekle
description: ISIŞAH GROUP 3B showroom'una (urunler.html) yeni ürün ekler. Kullanıcı ürün fotoğrafı atıp "ürün ekle", "showroom'a koy", "SALMEX'e/ISIŞAH'a/BORŞAH'a ekle" dediğinde veya bir marka holüne ürün ekleme istendiğinde devreye girer. Foto → Higgsfield stüdyo çekimi → kesim → WebP → kart → test hattının tamamını tuzaklarıyla yürütür.
---

# ISIŞAH Showroom'a Ürün Ekleme Hattı

Repo: `~/isisah-scroll-world` · Sayfa: `urunler.html` · Görseller: `assets/products/*.webp`
Tam bağlam için önce `~/isisah-scroll-world/HANDOFF.md` oku (özellikle sürüm/mimari değiştiyse).

## 0. Kaynak fotoğraf
- Chat'e atılan fotoğraflar genelde `~/Downloads`'ta da vardır (IMG_*.HEIC / IMG_*.jpg / PHOTO-*.jpg) — önce oraya bak, `ls -lat ~/Downloads | head`.
- HEIC ise `sips -s format jpeg` ile çevir. Scratchpad UÇUCUDUR (oturumlar arası silinir) — kaynakları Downloads'tan yeniden üretebilirsin.
- Birden çok foto = önce küçük grid'le eşleştir, ürün başına EN İYİ açıyı seç (tüm parçalar görünür, 3/4 açı ideal).

## 1. Higgsfield stüdyo çekimi
- CLI: `higgsfield` (hesap mehmetcan12sahin@gmail.com, ultra plan). Oturum düşerse: `higgsfield auth login` → device linkini KULLANICIYA ver, o onaylar. (Onay gerektiren tek adım budur.)
- **REFERANS MUTLAKA PNG** — JPG upload'ı S3 imza hatası verir (`SignatureDoesNotMatch`). JPG kaynağı önce PIL ile PNG'ye çevir (2048px yeter).
- Komut şablonu:
```bash
higgsfield generate create gpt_image_2 --prompt "<ürünün birebir tarifi>. professional studio product photograph, plain uniform light gray seamless background, soft even diffused studio lighting, no text, no watermarks, generous empty margins, product centered, photorealistic, keep the original product design exactly as in the reference photo" --image ref.png --aspect_ratio 1:1 --resolution 2k --quality high --wait --wait-timeout 10m --json
```
→ `.[0].result_url` → curl ile indir. Ürün kutu/araç/gemi gibi genişse 16:9.
- Üretimler sunucuda kalır: scratchpad silinirse `higgsfield generate list --json` içinden prompt anahtar kelimesiyle bul, result_url'den KREDİSİZ yeniden indir.

## 2. Arka plan kesimi
- Varsayılan: `TOL=55 python3 ~/.claude/skills/scroll-world/references/knockout.py cikti.png` (stüdyo grisi 55-70; beyaz cisim 22).
- **Halka/çerçeve ürünlerde iç boşluk beyaz kalır** → iç-blob temizliği: alpha=255 + köşe rengine yakın + kenar-bağlantısız blobları sil (MIN_BLOB ürüne göre 2500-5000; HANDOFF'ta hazır script örneği var).
- **Gri-üstü-gri veya parlak gövde** (gemi, kazan, alüminyum kapak): knockout DELER, TOL artırmak da deler → Higgsfield MCP `remove_background` kullan: `media_id` = tamamlanmış üretim job id'si, `media_type: image`; `jobs_wait` ile bekle, result_url'i indir. Pürüzsüz çıkar.
- Kontrolü HEP koyu zeminde yap (hol koyu): kesimleri (16,20,26) zemine yapıştırıp grid'e bak.

## 3. WebP
```python
# alpha bbox + 12px pad kırp → ≤900px → assets/products/<img>.webp
im.save(out, 'WEBP', quality=88, method=6)
```
Hedef 40-200KB.

## 4. urunler.html kartı
- Kart şablonu (ilgili listeye — `SALMEX_LIST`, `BORSAH_LIST` veya `ISISAH_LIST`):
```js
{img:'<anahtar>',logo:'logo-<marka>',tag:'<MARKA/GAM ETİKETİ>',h:'Türkçe Başlık',en:'English Title',
 p:'Tek cümle açıklama (müşteri sonradan düzeltir).',chips:['3','Kısa','Çip']},
```
- ISIŞAH ürünü ise ayrıca `ISISAH_CATS` içindeki doğru gamın `byImg(...)` listesine anahtarı ekle (gamlar resmi katalog sektörleri).
- `GHOSTS` map'ine hayalet kelime ekle (`anahtar:'KELİME'`).
- Teknik iddiaları uydurma; katalog/kullanıcı verisinden al, emin değilsen nötr yaz ve kullanıcıya "metin onayı bekliyor" de.

## 5. Test (ZORUNLU protokol)
- Önizleme: http://localhost:8080 (LaunchAgent'lı python server — kapalıysa `launchctl load ~/Library/LaunchAgents/com.isisah.preview.plist`).
- **SES: kapı tıklaması simüle etmeden ÖNCE `localStorage.setItem('swMuted','1')`** — yoksa müzik kullanıcının hoparlöründe çalar ve DOM'dan durdurulamaz.
- Kapıdan gir → `#hallName` doğru, `#tot` = ürün sayısı + 2, `#warn` boş, konsol temiz, yeni webp network'te 200.
- Arka plan sekmesinde rAF/layout donar (innerHeight=0, WebGL siyah) — DOM/JS state ile doğrula, scroll simülasyonuna güvenme.

## 6. Yayın
`isisah-deploy` skill'i ile (çift hedef + kök türetimi + canlı doğrulama). Commit mesajına eklenen ürünleri yaz.
