# ISIŞAH GROUP Web Sitesi — Devir / Devam Dokümanı

> Yeni bir Claude Code oturumu bu dosyayı okuyarak projeye tam bağlamla devam edebilir.
> Ek olarak kalıcı hafıza: `~/.claude/projects/-Users-mehmetcansahin/memory/isisah-scroll-world-site.md`

## Proje nedir
Bursa/DOSAB merkezli **ISIŞAH GROUP** (1982; markalar: **ISIŞAH Endüstriyel** rezistans/ısıtma, **SALMEX** ısı eşanjörleri, **BORŞAH** paslanmaz boru) için iki sayfalı site:
- `index.html` — kurumsal ana sayfa (gerçek fotoğraflar, Demiryolu İklimlendirme bölümü dahil)
- `urunler.html` — **3B WebGL showroom**: 3 kapılı fotogerçekçi marka lobisi → kapıdan geçince o markanın holünde scroll ile uçuş; kaidelerde ürünler, marka başına asansör müziği

## Canlı & Deploy
- **Canlı:** https://mehmetcan12sahin.github.io/isisah-showroom/ (+ `/urunler.html`)
- GitHub Pages, public repo `mehmetcan12sahin/isisah-showroom`, branch `main`, `.nojekyll` var
- **Deploy = `git push`** (bu klasörden; ~1 dk'da yayılır, CDN HTML'i ~10 dk cache'leyebilir → Cmd+Shift+R)
- Yerel önizleme: LaunchAgent `com.isisah.preview` (kalıcı `python3 -m http.server 8080`, KeepAlive) → http://localhost:8080 . Kaldırmak: `launchctl unload ~/Library/LaunchAgents/com.isisah.preview.plist`

## Git sürüm geçmişi (geri dönüş noktaları)
`v1-showroom` (tek koridor, refine öncesi — kullanıcı "beğenmezsem dönerim" yedeği) → `v2-refine` (Emil/impeccable design pass) → `v3-wow` (sinematik katman) → `v4-lobby` (3 kapı) → sonrası: v4.1 (18 ürün), v4.2 (fotogerçekçi lobi+müzik), v4.2.x (kadraj/mobil düzeltmeleri). Dönüş: `git checkout <tag> -- .`

## urunler.html mimarisi (vanilla Three.js r160, unpkg importmap — build yok)
- **MODE:** `lobby | entering | hall`. Lobby: fotogerçekçi portal duvarı (`assets/img/lobby.webp`, 30 birim genişlik plane z=3; sol kor=ISIŞAH, orta buhar=SALMEX, sağ altın boru tüneli=BORŞAH), görünmez hitbox'lar `doorX=±8.1/0`, DOM kapı kartları (mobilde birincil UI). Lobide hol dekoru `setHallDress(false)` ile gizli (tavan/kiriş/kolon/şerit/spot) — yoksa görseli keser.
- **enterHall(brand):** kapıya uçuş (mevcut kamera z'sinden, 900ms) → fade → `buildHall()` (hallGroup'u söküp markanın kaidelerini kurar; PRODUCTS/NP/TOT/rail/scroll yeniden; idx `d.tag`'den numaralanır) → giriş crane animasyonu → `playTrack(brand)`.
- **Hol mekaniği:** scroll→progress (geometri tabanlı) → yumuşatılmış kamera koridor uçuşu; aktif ürüne yaslanma+FOV daralması (52→47; portrede taban 66); dev hayalet tipografi (`GHOSTS` map); hologram halkası; ürün bob; künye kartı (masaüstünde projeksiyonla, portrede alta sabit); tıkla→OrbitControls inceleme (yazısı bilerek YOK — kullanıcı istemedi).
- **Markalar:** `BRANDS{isisah:25, salmex:8, borsah:3}` + **ISIŞAH alt-lobisi**: ISIŞAH kapısı hol yerine `.sublobby` (7 ürün gamı kartı — resmi katalog kapağındaki sektörler: Mutfak 4, Beyaz Eşya 5, Ağır Sanayi 4, HVAC 4, Raylı 4, Savunma 3, Otomotiv/BOYKUR 1) açar; gam kartı `enterHall('isisah_*')` → `ISISAH_CATS` sanal holleri (`hallDef`/`brandRoot` lookup; TRACKS/HALL_THEMES/CSS accent köke düşer). SALMEX/BORŞAH doğrudan hole uçar. `HALLLEN=22`. Kaynak: `~/Downloads/catalogue.pdf` (8 s., resmi katalog).
- **v5 neon tema:** saf siyah zemin+fog, Inter tipografi, marka başına neon ışık ailesi (lobi violet, ISIŞAH ember, SALMEX electric, BORŞAH mint) — CSS `--a*` accent'leri `body[data-brand]`, 3B ışıklar `applyTheme()`; kaide başına ürün dibi glow kanopisi; magenta CTA'lar. index.html hero: `assets/img/bina-gece.webp` (Higgsfield gece dönüşümü; duvar logolarındaki sedil PİKSELLE elle işlendi — model Ş basamıyor).
- **Müzik:** `assets/audio/{isisah,salmex,borsah}.mp3` (Higgsfield sonilo_music, 60s loop). Kapı tıklaması=user gesture→autoplay OK; lobiye dönüşte durur; 🔇 butonu localStorage `swMuted`; sekme gizlenince otomatik pause.
- **Perf kuralları:** ≤7 ışık (tek gezici spot), DPR≤1.5, tek rAF, WebP ürün dokuları `TEXCACHE`'te önceden ısıtılır. `prefers-reduced-motion` her animasyonu kapatır.

## Varlık üretim hatları (hepsi kanıtlanmış)
- **Higgsfield CLI** (`higgsfield`, hesap mehmetcan12sahin@gmail.com, **ultra plan ~2478 kredi**). Oturum düşerse: `higgsfield auth login` → çıkan device linkini kullanıcı tarayıcıda onaylar.
  - Görsel: `generate create gpt_image_2 --prompt ... [--image ref.png] --aspect_ratio 16:9|1:1 --resolution 2k --quality high --wait --json` → `.[0].result_url` → curl.
  - Müzik: `generate create sonilo_music --prompt ... --duration 60` (çıktı M4A → ffmpeg ile mp3 128k).
  - Ürün fotoğrafı temizleme: gerçek/karmaşık foto → `--image` referansla "studio product photo, plain light gray background, generous margins" → knockout.
- **Knockout:** `~/.claude/skills/scroll-world/references/knockout.py` (TOL=22 beyaz cisimler, 55-70 stüdyo grisi). Halka ürünlerde beyaz göbek → iç-blob temizliği (MIN_BLOB ürüne göre; parlak gövdeli ürünlerde UYGULAMA — deler). Gri-üstü-gri ürünlerde (gemi, kazan gibi) TOL artırma da deler → Higgsfield MCP `remove_background` kullan (media_id = tamamlanmış job id; jobs_wait ile bekle) — pürüzsüz kesim. Çıktı ≤900px WebP q88 → `assets/products/`.
- Kaynak fotoğraflar/scratch bu oturumların scratchpad'indeydi (uçucu) — orijinaller: kullanıcının Downloads'ı + `assets/catalog/*.jpg` (katalog PDF sayfaları).

## Veri kaynakları
- isisah.com.tr (iletişim/ürün bilgisi; logo URL'leri NFD Türkçe karakterli — `ISIS%CC%A7AH-LOGO.png`)
- isisahgroup.com.tr → 3 katalog PDF'i (`assets/catalog/` içinde sayfa görselleri + logolar)
- `~/Downloads/Demiryolu Proje Sunum 01.07.2026.pdf` → index'teki Demiryolu bölümünün tamamı (1986-2026 projeler, testler, malzemeler, referanslar)
- Kullanıcının sergi salonu fotoğrafları (IMG_1585-1601.heic) → 6 yeni ürün (blast, baseboard, fincoil, panel, railcar, duct)

## Tasarım kuralları (v2 refine'da oturdu — bozma)
- Kurulu skiller: `impeccable` (detektör: `node ~/.claude/skills/impeccable/scripts/detect.mjs --json <dosya>`), `emil-design-eng`, `taste`, animasyon skilleri
- Güçlü ease-out token `--ease-out`, spesifik transition'lar, `:active scale(.97)`, hover `@media(hover:hover)` arkasında, nötr gölgeler (renkli glow yok), eyebrow yok
- Bilinçli istisnalar: index'teki blueprint grid (sanayi kimliği) + marquee (yavaş+hover-pause)

## Test/önizleme tuzakları (zaman kaybetme)
- Uygulama-içi tarayıcı: arka plan sekmesinde rAF donar → WebGL screenshot SİYAH gelir; taze `navigate` sonrası ilk kareler görünür. FPS ölçülemez. DOM/JS state kontrolüyle doğrula.
- Sayfada `window.scrollTo` bazı sayfalarda çalışmıyordu (eski sürümlerde); showroom'da çalışıyor.
- **SES TEST PROTOKOLÜ (zorunlu):** showroom'da kapı tıklaması simüle etmeden ÖNCE `localStorage.setItem('swMuted','1')` çalıştır — yoksa müzik kullanıcının hoparlöründe çalar ve `new Audio()` DOM dışı olduğu için `querySelectorAll('audio')` ile durdurULAMAZ; tek kesin susturma sekmeyi başka sayfaya `navigate` etmek. (Bu hata iki kez yaşandı.)
- python http.server byte-range vermez → videolar blob ile oynatılırdı (artık video yok).

## v5.1 (council turu) notları
- **Three.js vendorlandı:** `vendor/three.module.js` + addons (0.160.0), importmap yerel — unpkg bağımlılığı YOK artık.
- **SEO:** robots.txt, sitemap.xml, canonical, JSON-LD (index: Organization; urunler: CollectionPage/Breadcrumb), og:/twitter meta + `assets/img/og-cover.jpg`. TÜM mutlak URL'ler github.io — ana domaine geçişte sitemap+canonical+og+robots toplu değişmeli.
- **Künye teklif köprüsü:** setInfo() kartlara "Teklif İste" (mailto, ürün adlı konu) basıyor; `WHATSAPP` sabiti (905xxxxxxxxx) doldurulunca yeşil WhatsApp butonu da görünür — numara kullanıcıdan BEKLENİYOR.
- index Markalar: 3 kart (SALMEX eklendi, "Üç uzmanlık").
- impeccable hook'u gradient-text/dark-glow/Inter işaretler — v5 neon temasının bilinçli dili, false positive.

## Bekleyen / olası sonraki adımlar
- Kullanıcı son istek: mobil entegrasyon (lobby dahil — v4.2.3'te yapıldı) ✓
- KULLANICIDAN BEKLENEN: (1) WhatsApp GSM numarası → urunler.html `WHATSAPP` sabiti; (2) ana domain DNS bilgileri → CNAME + URL'lerin toplu değişimi + Search Console; (3) 14 yeni ürün kartının metin onayı (kullanıcı düzeltme verdikçe).
- Fikirler: TV fuar modu (attract loop), EN sürüm (metin onayından SONRA), lobby görselinin violet varyantı, çerezsiz analytics
- Kullanıcı Türkçe yazar; caveman modu aktif olabilir; onay gerektiren tek şey Higgsfield device login.
