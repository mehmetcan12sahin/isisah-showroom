# Perf baseline — 2026-09-25 — tekrar-koşum talimatı

Bu klasördeki JSON'lar ve aşağıdaki ölçümler **değişiklik öncesi** (revizyon/b2b, main ile aynı içerik) baseline'dır. Aynı koşullarda tekrar ölçüp bu klasördeki sayılarla karşılaştırın.

## Önkoşullar

- Yerel sunucu (sıkıştırma YOK, byte-range YOK — Python `http.server`):
  ```
  python3 -m http.server 8080 --bind 127.0.0.1 --directory /Users/mehmetcansahin/isisah-scroll-world
  ```
  (Bu depoda zaten arka planda çalışıyordu: PID kontrolü için `ps aux | grep "http.server 8080"`.)
- Lighthouse 13.4.1: `/opt/homebrew/bin/lighthouse --version`
- Playwright'ın Chromium'u (Google Chrome for Testing 151.0.7922.34), lighthouse'a `CHROME_PATH` ile verilir:
  ```
  export CHROME_PATH="/Users/mehmetcansahin/Library/Caches/ms-playwright/chromium-1234/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing"
  ```
- Playwright (node modülü) `~/.isisah-smoke/node_modules/playwright` altında (v1.62.1), `tools/smoke-browser.mjs` deseniyle `createRequire` ile yüklenir.

## Tek komutla tekrar koşum

Betik (bu oturumun scratchpad'inde kalır, silinmeyecekse projeye kopyalanabilir):

```
/private/tmp/claude-501/-Users-mehmetcansahin/d209b939-08cb-428f-baef-cec84195f7ab/scratchpad/audit/run-baseline.sh
```

İçeriği (özet — tam dosya yukarıdaki yolda):

```bash
export CHROME_PATH="/Users/mehmetcansahin/Library/Caches/ms-playwright/chromium-1234/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing"
OUT=/Users/mehmetcansahin/isisah-scroll-world/docs/lighthouse-2026-09-25-baseline
cd /Users/mehmetcansahin/isisah-scroll-world
for page in index urunler sanayi-tipi-rezistans; do
  for run in 1 2 3; do
    /opt/homebrew/bin/lighthouse "http://localhost:8080/${page}.html" \
      --output=json --output-path="$OUT/${page}-run${run}.json" \
      --only-categories=performance,accessibility,best-practices,seo \
      --chrome-flags="--headless=new" --quiet
  done
done
```

Sıralı çalışır (paralel değil), mobil varsayılan (Lighthouse default: mobil emülasyon 412×823, `throttlingMethod=simulate`). Çıktı dosyaları: `index-run{1,2,3}.json`, `urunler-run{1,2,3}.json`, `sanayi-tipi-rezistans-run{1,2,3}.json`.

## Sonuçları özetleme

```
node /private/tmp/claude-501/-Users-mehmetcansahin/d209b939-08cb-428f-baef-cec84195f7ab/scratchpad/audit/parse-lh.mjs
```
Her sayfa için perf/a11y/bp/seo skorlarını (3 koşu + ortanca), LCP/CLS/TBT/FCP/SI ortancalarını, LCP elementini (`lcp-breakdown-insight` audit'inin `node` tipi item'ından) ve başarısız a11y denetimlerini yazdırır.

## Showroom yükü (lobi + SALMEX hol geçişi)

```
node /private/tmp/claude-501/-Users-mehmetcansahin/d209b939-08cb-428f-baef-cec84195f7ab/scratchpad/audit/showroom-measure.mjs
```
`localStorage.setItem('swMuted','1')` sayfa yüklenmeden `addInitScript` ile enjekte edilir (ses çalmasın). `/urunler.html` açılır → `body.ready` anına kadarki tüm istekler "lobi" fazı sayılır → `networkidle` + 3 sn ek bekleme → `button.doorcard[data-brand="salmex"]` tıklanır (ISIŞAH değil, doğrudan hole giden marka) → `body.classList.contains('inhall')` anına kadarki + 1.5 sn sonraki istekler "hol" fazı sayılır. Çıktı: istek sayısı, toplam bayt, en büyük 10 kaynak (her faz için).

## Ana sayfa görsel envanteri

```
node /private/tmp/claude-501/-Users-mehmetcansahin/d209b939-08cb-428f-baef-cec84195f7ab/scratchpad/audit/index-images.mjs
```
`/index.html`'i açar, tüm `<img>` etiketlerinin `naturalWidth/Height` (doğal boyut) ve `getBoundingClientRect()` (gösterim boyutu) değerlerini + gerçek transfer byte'ını (network response'tan) karşılaştırır; ayrıca sayfanın en büyük 12 kaynağını listeler. Not: ekran altı `loading="lazy"` görseller sayfa ilk yüklendiğinde henüz talep edilmediği için `naturalWidth=0` / `transferBytes=0` görünür — bu bir hata değil, henüz viewport'a girmediklerinin göstergesi.

## Önemli tekrarlanabilirlik notları

- Bu makine ölçüm sırasında başka yükler taşıyordu (`uptime` çıktısı: load average 3.47 / 5.33 / 9.33, 15G RAM'in çoğu kullanımda). Bu, Lighthouse "simulate" throttling kullandığı için mutlak CPU zamanlamasını değil ama bazı skorların koşu-arası varyansını etkileyebilir (bkz. index run1 speed-index'in diğer 2 koşudan ~15× yüksek çıkması, urunler run1'in perf skorunun 41 iken run2/3'te 67 olması — TBT run1'de 1343ms'ye sıçramış). Aynı betiği makine boştayken tekrar çalıştırıp karşılaştırmak, "revizyon etkisi mi yoksa gürültü mü" sorusunu netleştirir.
- Yerel `python -m http.server` sıkıştırma (gzip/br) ve `Range` isteklerini desteklemiyor (doğrulandı: `curl -H "Accept-Encoding: gzip"` ve `curl -r 0-100` ikisi de tam 200 + sıkıştırılmamış body döndürdü). Bu ortamda ölçülen "total-byte-weight" ve transfer bayt sayıları, üretim sunucusunda (Plesk, muhtemelen gzip/br + Range) daha düşük çıkabilir. Baseline'ı canlıyla karşılaştırırken bu farkı hesaba katın.
