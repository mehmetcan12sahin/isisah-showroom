# ISIŞAH GROUP Web Sitesi — Devir / Devam Dokümanı

> Yeni bir Claude Code oturumu bu dosyayı okuyarak projeye tam bağlamla devam edebilir.
> Ek olarak kalıcı hafıza: `~/.claude/projects/-Users-mehmetcansahin/memory/isisah-scroll-world-site.md`

## Proje nedir
Bursa/DOSAB merkezli **ISIŞAH GROUP** (1982; markalar: **ISIŞAH Endüstriyel** rezistans/ısıtma, **SALMEX** ısı eşanjörleri, **BORŞAH** paslanmaz boru) için iki sayfalı site:
- `index.html` — kurumsal ana sayfa (gerçek fotoğraflar, Demiryolu İklimlendirme bölümü dahil)
- `urunler.html` — **3B WebGL showroom**: 3 kapılı fotogerçekçi marka lobisi → kapıdan geçince o markanın holünde scroll ile uçuş; kaidelerde ürünler, marka başına asansör müziği

## Canlı & Deploy
- **ANA CANLI: https://isisah.com.tr/showroom/** (+ `/urunler.html`) — Birhost Plesk `httpdocs/showroom/`, FTP deploy: `bash tools/deploy-ftp.sh` (kimlik `~/.isisah-ftp.netrc`, git DIŞINDA; kullanılan ~73 dosyayı yükler). Mevcut WP sitesine DOKUNMA — sadece showroom/ dizini bizim.
- Yedek/ayna: https://mehmetcan12sahin.github.io/isisah-showroom/ (canonical'lar ana domaini gösterir)
- GitHub Pages, public repo `mehmetcan12sahin/isisah-showroom`, branch `main`, `.nojekyll` var
- Deploy = **`git push` (github.io aynası) + `bash tools/deploy-ftp.sh` (ANA site)** — ikisini de çalıştır.
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

## TV fuar modu
- `urunler.html?fuar` → attract loop (sergi salonu/fuar TV'si): kapı turu TOUR dizisi, hız SPEED (vh-orantılı), müdahale→dur, 60sn idle→devam. Parametresiz sıfır etki. TV kurulumunda tam ekran kiosk tarayıcıda bu URL açılır; ses istenirse TV'de bir kez 🔊 açılır (localStorage kalıcı).

## Search Console (25 Ağu 2026, kullanıcının Chrome'u ile kuruldu)
- Mülk: URL öneki `https://isisah.com.tr/` — HTML dosya doğrulaması: `httpdocs/googlebfb5098152a94f7b.html` (SİLME!)
- sitemap.xml gönderildi (kök + showroom/urunler); kök ve showroom için "dizine eklenme" talebi verildi
- Kök index.html artık yeni site (WP index.php'nin önünde); eski siteye dönüş = httpdocs/index.html'i sil

## v6.2 (26 Ağu 2026 — ölçek/netlik düzeltmeleri)
- **KÖK BUG:** showroom header+loader logo img'lerine verilen width/height ATTRIBUTE'ları CSS height:30/42px ile çakışıp logoyu 400x30 EZİYOR ve mobilde header sağ kontrollerini ekran dışına itiyordu — attr'lar kaldırıldı, CSS'e width:auto eklendi. DERS: CSS'i yalnız height yöneten img'lere width attribute VERME.
- Tüm logolar + salmex fotoları yüksek kaliteyle YENİDEN üretildi (canvas imageSmoothingQuality:'high' + çok adımlı küçültme; önceki dönüşüm default 'low' ile bulanıktı). Logolar 160px, salmex-hat 1800w, salmex-robot 1400w. hqconvert.mjs deseni: her adım ≤%50 küçültme.
- index header/footer logosu assets/img/logo.png (koyu metin, siyahta görünmez) → assets/catalog/logo-isisah.webp (beyaz metinli), height 38px.
- SALMEX hat fotoğrafı Kurumsal'dan (ISIŞAH bağlamı — kullanıcı düzeltti) çıkarıldı → kendi bölümü `#salmex-hat` (.feature.salmex, electric accent), MARKALAR ile ÜRÜNLER arası. Kurumsal imgcol eski üçlüye döndü. salmex-robot.webp şu an SAYFADA KULLANILMIYOR (repoda duruyor).

## v6.1 (KULLANICI KARARI — 26 Ağu 2026): v6 redesign REDDEDİLDİ, seçmeli geri alım
- Kullanıcı v6 antrasit/amber redesign'ı BEĞENMEDİ → index.html `v5.2-konsey` haline geri alındı (neon canlı kimliktir, tartışmaya kapalı say).
- KORUNANLAR (kullanıcı beğendi/istedi): (1) `.bridge` 3B Showroom köprü kartı — v5.2 neon diliyle index'e yeniden eklendi (id=showroom, assets/img/showroom-preview.webp), CANLIDA; (2) tren ölçek sınırı (.rail-hero img max-width 540/420px); (3) tren.webp Higgsfield image_background_remover ile YENİDEN kesildi + alfa eşiği defringe (a<200→0, 200-255 rampa) — beyaz sis gitti (assets/products/tren.webp değişti, showroom da aynı dosyayı kullanır).
- YENİ GERÇEK VARLIK: kullanıcının çektiği SALMEX robotlu üretim hattı fotoğrafları → assets/img/salmex-hat.webp (1600w, geniş plan) + salmex-robot.webp (1200w, robot hücresi). Kurumsal imgcol'a girdi (firin.jpg ve paslanmaz-boru.jpg imgcol'dan çıktı; dosyalar duruyor), SALMEX marka kartına 'Robotlu Üretim Hattı' çipi eklendi. Kaynak HEIC'ler: ~/Downloads/IMG_9711/9712.HEIC.
- v6 tasarımı `v6-gercekcilik` tag'inde duruyor (geri dönülebilir); assets/fonts self-host Inter dosyaları repoda KALDI ama index yine Google Fonts kullanıyor (KVKK paketinde devreye alınabilir). v6'da silinen riskli görseller (vizyon/kurumsal/boru-stack/banner-boykur jpg) SİLİNMİŞ KALDI — hiçbiri v5.2 index'inde referanslı değil.

## v6 (gerçekçilik turu — 26 Ağu 2026, "ana sayfa AI duruyor" konseyi) — REDDEDİLDİ (tag v6-gercekcilik'te yaşıyor)
- Konsey oyları: Mimar A, Müşteri A, Şüpheci B, Güvenlik C → Hakem kararı **A-disiplinli**: index antrasit (#0d0f12) + logodan türeyen TEK amber accent (--a1/--a2/--a3); violet neon SADECE `.bridge` (3B Showroom köprü kartı) içinde yaşar. urunler.html'e DOKUNULMADI (neon kimliği canlıda, beğenildi).
- SÖKÜLENLER: .glow blob'ları, .wm watermark, .grad-text gradyanı (düz amber oldu), tüm renkli box/text-shadow glow'lar, marka-başına kart haleleri (mnt/ele/emb aileleri index'ten kalktı), magenta CTA/ikonlar, marquee (yerine statik `.refs` referans isim şeridi: TÜVASAŞ·TOFAŞ·Ankara Metro·İBB·Arçelik...), Google Maps CSS filtresi (ToS + bozuk görünüm).
- EKLENENLER: `.bridge` köprü bölümü (id=showroom; assets/img/showroom-preview.webp = showroom'un GERÇEK ekran görüntüsü — Güvenlik kuralı: index'e yeni AI 'fotoğraf' girmez, dürüst temsil); hero CTA sırası Teklif Al (amber solid) / Ara / 3B Showroom; tren.webp kirli alfa kenarı `.railvisual` panel karta alınarak gizlendi.
- **Google Fonts self-host**: assets/fonts/inter.css + 6 woff2 (latin+latin-ext, 400/600/700). inter.css içindeki url'ler GÖRELİ (kök türetmede de çalışır); deploy-ftp.sh'a assets/fonts eklendi. preconnect satırları kalktı — Google'a giden tek şey Maps iframe kaldı (tıkla-yükle 2. dalgada).
- Silinen riskli görseller: vizyon.jpg (lisansı belirsiz stok insan), kurumsal.jpg (düşük çöz. render), boru-stack.jpg (CGI klipart), banner-boykur.jpg (gömülü metinli eski banner).
- 6 HEIC sergi fotoğrafı çevrilip DEĞERLENDİRİLDİ ve KULLANILMADI (fayans zemin/yangın tüpü — Şüpheci: zayıf foto büyük basılırsa 'ucuz durur'). Eksik: üretim hattı geniş plan, ekip, gerçek cephe fotoğrafı — kullanıcıdan telefon çekimi istenebilir.
- Konseyin REDDETTİKLERİ: sektör grid'i + m²/ihracat rakam şeridi (kaynak yok — fabrikasyon riski), stok fotoğraf, index'te Higgsfield 'fotoğraf', referans LOGO şeridi (yazılı izin yok — gri METİN kullanıldı).
- Tag: `v6-gercekcilik`. Dönüş: `git checkout v5.2-konsey -- index.html` (urunler.html zaten değişmedi).

## v5.2 (konsey turu 2 — 26 Ağu 2026, 5 denetçi + 4 üye konseyi)
- **Dayanıklılık:** WebGL renderer try/catch (yoksa loader kalkar + ana sayfaya yönlendirme); modül DIŞI klasik script 7 sn emniyeti loader'ı her koşulda kaldırır. index reveal artık `.js` sınıfı arkasında (JS'siz bot/önizleme İÇERİĞİ GÖRÜR) + 3 sn sonra koşulsuz `.in`.
- **Perf:** `vendor/three.module.min.js` (655K; unminified 1.27M SİLİNDİ — deploy os.walk vendor'u komple yükler). Loader lobby.webp inince kapanır (`!FAIR` şartlı; fuar TV tam ısınmayı bekler). Tema glow/ring dokuları GLOWTEX/RINGTEX cache (kiosk sızıntısı kapandı); buildHall söküm artık hole özgü malzemeleri dispose eder (`hallMats`; TEXCACHE'e dokunma). Logolar webp 96px (~417K→50K; favicon png kaldı). index görselleri: hero preload+fetchpriority, gerisi lazy+width/height. Mobilde hero görseli 16:9 GERİ GELDİ (display:none kalktı).
- **Dönüşüm:** mobil sticky bar (Ara / Teklif İste), hero'da tel CTA, showroom header 'Teklif Al', lobide tel+mail satırı, outro'da Ara butonu, künyede 'İncele' butonu (canvas tıklamasına klavye/dokunma alternatifi). Tüm 'ISO 9001-2015' → 'ISO 9001:2015'.
- **Taste:** BOYKUR banner'ı temiz ürün fotosuyla değişti (banner-boykur.jpg SİLİNMEDİ ama kullanılmıyor→silindi listesinde). Demiryolu accent'i SALMEX cyan'ından grup violet'ine döndü. Marka kartı eyebrow'ları kategoriye çevrildi (numara/tekrar kalktı). Lobi başlığı h1 + UPPERCASE (index ile case birleşti); sublobby/outro h2. Timeline em-dash'leri ':' oldu, 2018-21 İzmir satırı kronolojik yerine taşındı. İletişim emoji ikonları tek aile inline SVG oldu.
- **A11y:** doorcard/catcard artık gerçek `<button>` (tam UA reset ile — görsel birebir), rail aria-label+aria-current, mute aria-pressed, menü aria-expanded+Escape, harita iframe title, #warn role=alert (failed listesi hol başında sıfırlanır), künye aria-live, scroll-margin-top, theme-color+color-scheme.
- **BUG FIX (QA yakaladı):** outro `.cta` görünmezken de tıklama yutuyordu (pointer-events:auto sabitti) — artık frame() opacity ile senkron. Bu, lobide SALMEX kapısının orta bölgesini ölü bırakabiliyordu.
- **Hijyen:** legacy silindi (index-cinematic, urunler-video, urunler-kaide, scrub-engine.js, assets/vid 69MB, kök jpg'ler, kullanılmayan img'ler, webp'i olan ürün PNG'leri) — assets 94MB→14MB; dönüş = v-tag'ler (`v5.1-pre` bu turun öncesi). `.gitignore` eklendi. deploy-ftp.sh FTPS DENENDİ ve GERİ ALINDI: Birhost 'AUTH SSL successful' diyor ama TLS handshake SSL_ERROR_SYSCALL ile ölüyor (curl 35) — düz FTP'de kalındı. Barındırıcı FTPS'i düzeltirse `--ssl-reqd` yeniden eklenebilir.
- **Bilinçli istisna:** fuar drive() ikinci hafif rAF zinciri kurar — çalışıyor, refactor edilmedi.
- **loadProductTex png dalı:** ürün PNG'leri silindiği için webp başarısız olursa .png 404 → fallbackTex'e düşer (davranış korunur, fazladan tek istek).

## Bekleyen / olası sonraki adımlar
- Kullanıcı son istek: mobil entegrasyon (lobby dahil — v4.2.3'te yapıldı) ✓
- KULLANICIDAN BEKLENEN: (1) WhatsApp numarası → urunler.html `WHATSAPP` sabiti (Güvenlik üyesi: kişisel GSM değil WhatsApp Business şirket hattı olmalı); (2) 14 yeni ürün kartının metin onayı; (3) violet lobi varyantı onayı; (4) **BORŞAH çap teyidi**: index 'Ø6–25' vs showroom 'Ø4–25' çelişkisi katalogdan doğrulanacak (bilerek DÜZELTİLMEDİ); (5) KVKK sayfaları için ticaret unvanı + MERSİS/vergi bilgisi.
- 2. DALGA (konsey kararı, tek koordineli paket): KVKK aydınlatma+çerez+künye sayfaları, self-host teklif formu (Plesk PHP mail + honeypot; Formspree/reCAPTCHA YOK — konsey reddetti; action MUTLAK URL olmalı ki github.io aynasında da çalışsın), Google Fonts self-host + Maps tıkla-yükle (üçüncü parti sıfırlanır, çerez banner'ı gereksizleşir), referans şeridini hero altına taşıma, Demiryolu timeline mobil katlama. Bu paket deploy-ftp.sh'a yeni sayfaların eklenmesini GEREKTİRİR (script yalnız index+urunler tarar!).
- Fikirler: EN sürüm (metin onayından SONRA), lobby görselinin violet varyantı, çerezsiz analytics
- Kullanıcı Türkçe yazar; caveman modu aktif olabilir; onay gerektiren tek şey Higgsfield device login.
