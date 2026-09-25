# Design tokens — ISIŞAH GROUP static site

Bu doküman, `index.html`'in `<style>` bloğundaki `:root` değişkenlerini **kanonik** kaynak olarak tanımlar. `tools/pagegen.py` bu `<style>` bloğunu 13 üretilmiş sayfaya (hakkimizda.html, vizyon-misyon.html ve 11 kategori sayfası) olduğu gibi kopyaladığı için, index.html'deki değerler otomatik olarak o sayfalarda da geçerli olur. `urunler.html` ve `fabrika.html` bu mekanizmanın DIŞINDA, kendi `<style>` bloklarını elle tutar — bu iki dosya benim düzenleme kapsamımın dışında (bkz. "Bilinen sapmalar").

Bu dosya sadece belgeler; hiçbir CSS dosyasını değiştirmez.

## Kanonik `:root` (index.html kaynaklı)

```css
:root{
  color-scheme:dark;
  --bg:#000; --bg2:#050508; --panel:#0a0a10; --panel2:#0e0e16;
  --ink:#fff; --muted:#8f93a3; --line:#1b1c26; --steel:#c3c7d4;
  --vio1:#6b5bff; --vio2:#7a2bff; --vio3:#8b3bff; --vio-text:#9d94ff;
  --emb1:#ff8a2b; --emb2:#ff5c2b; --emb3:#ffd08a;
  --ele1:#00d0ff; --ele2:#2f8bff; --ele3:#1f4cff;
  --mnt1:#35ffa8; --mnt2:#00ffa8; --mnt3:#4ec8ff;
  --mag1:#c04cff; --mag2:#ff2f7a;
  --grad:linear-gradient(100deg,var(--vio1),var(--vio3));
  --magrad:linear-gradient(100deg,var(--mag1),var(--mag2));
  --disp:'Inter',sans-serif; --body:'Inter',sans-serif; --tech:'Inter',sans-serif;
  --maxw:1240px;
  --ease-out:cubic-bezier(0.23,1,0.32,1);
  --ease-in-out:cubic-bezier(0.45,0,0.55,1);
}
```

Bu, mevcut neon marka kimliğinin (ISIŞAH v5.2) birebir aynısıdır — hiçbir renk değeri bu revizyonda değişmedi. Amaç yeni bir palet değil, üç ayrı stylesheet'te (index.html, urunler.html, fabrika.html) birbirinden hafifçe sapan aynı token'ları tek bir referansta sabitlemek.

## Bilinen sapmalar

| Token | index.html (kanonik) | urunler.html | fabrika.html | Not |
|---|---|---|---|---|
| `--line` | `#1b1c26` | `#1b1c26` (hizalandı) | `#1b1c26` (hizalandı) | Revizyon sonunda üç stylesheet tek değere çekildi. **Kanonik: `#1b1c26`** — çünkü pagegen.py bu değeri 13 üretilmiş sayfaya da kopyalıyor (toplam 14 sayfa `#1b1c26` kullanıyor, sadece 2 sayfa `#1d1e2a` kullanıyor). |
| `--steel`, `--vio-text`, `--bg2`, `--panel`, `--panel2`, `--maxw` | var | yok | yok | urunler.html/fabrika.html bu token'ları hiç tanımlamıyor; kendi yerel karşılıklarını (örn. sabit hex değerler) kullanıyor olabilirler. Kapsam dışı — bu ajan (H) urunler.html/fabrika.html'e dokunmuyor. |
| `--a1`/`--a2`/`--a3` (aktif marka accent'i) | yok | var (`body[data-brand]` ile değişir) | yok | urunler.html'e özgü bir 3B showroom mekanizması; index.html'de karşılığı yok, bu bir hata değil, kasıtlı bir mimari fark. |

**Durum:** `--line` urunler.html ve fabrika.html'de `#1b1c26` olarak hizalandı (entegrasyon adımı).

## Bu revizyonda eklenen yeni token'lar / utility'ler (index.html)

Marka paletine yeni bir renk eklenmedi. Eklenenler salt erişilebilirlik/okunabilirlik altyapısı:

```css
.sr-only{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}
.skip-link{ /* "İçeriğe atla" bağlantısı, klavye focus'unda görünür */ }
:focus-visible{outline:2px solid var(--vio-text);outline-offset:3px;border-radius:4px}
```

`--vio-text` (`#9d94ff`), zaten paletin bir parçasıydı (mor ailenin metin-kontrastlı tonu) — `:focus-visible` halkası ve `.wcard[data-c=violet]` metni için kullanıldı; yeni bir renk icat edilmedi, mevcut token yeniden kullanıldı.

## Dokunma (touch target) ve tipografi kuralları — kalıcı sözleşme

Bu revizyonla birlikte site genelinde şu asgari kurallar geçerli:

- Etkileşimli her öğe (buton, link, sekme, dropdown öğesi) en az **44×44 CSS px** dokunma alanına sahip olmalı (`min-height:44px` + yeterli `padding`).
- Gövde metninde **contrast oranı ≥ 4.5:1** olmalı (`.wcard[data-c=violet]` düzeltmesi: `--vio1` → `--vio-text`).
- Uzun metinde (cümle/paragraf) `text-transform:uppercase` **kullanılmaz**; sadece kısa etiket/kicker'larda (nav öğeleri, buton metinleri, `.kick`, `.bnum` gibi 1-4 kelimelik teknik etiketler) kabul edilir.
- Gövde metninin arkasında `blur`/`glow` efekti olamaz (görsel dekorasyon `.glow`, `.hero-visual::after` gibi arka plan katmanlarıyla sınırlı).
- Tüm etkileşimli öğelerde `:focus-visible` halkası görünür olmalı (yukarıdaki kural, `--vio-text` rengiyle global olarak tanımlı).

## Kaynak

Bu dosya, B2B revizyon görevinin H7 kalemi kapsamında ajan **H** tarafından `index.html`'in mevcut `<style>` bloğu okunarak oluşturulmuştur. urunler.html/fabrika.html içerikleri sadece karşılaştırma için okunmuş, değiştirilmemiştir.
