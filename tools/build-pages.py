#!/usr/bin/env python3
# Kurumsal alt sayfaları (hakkimizda.html, vizyon-misyon.html) index.html'in stil/header/footer'ından türetir.
# index.html'in CSS'i değişince yeniden çalıştır: python3 tools/build-pages.py
import re, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
idx = (ROOT/'index.html').read_text(encoding='utf-8')
style  = re.search(r'<style>.*?</style>', idx, re.S).group(0)
fonts  = re.search(r'<link href="https://fonts\.googleapis\.com[^>]+>', idx).group(0)
header = re.search(r'<header id="hdr">.*?</header>', idx, re.S).group(0)
footer = re.search(r'<footer>.*?</footer>', idx, re.S).group(0)
def sub(html, cur):
    html = html.replace('href="#top"', 'href="index.html"')
    html = re.sub(r'href="#([a-z-]+)"', r'href="index.html#\1"', html)
    html = html.replace(f'href="{cur}"', f'href="{cur}" aria-current="page"')
    return html

EXTRA_CSS = '''
  .pg{padding:150px 0 40px;position:relative;z-index:1}
  .pg .wrap{display:grid;grid-template-columns:1.1fr .9fr;gap:44px;align-items:center}
  .pg .hero-visual{aspect-ratio:16/11}
  .pg .hero-visual .tag{position:absolute;left:16px;bottom:16px;z-index:2}
  .kareler{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:8px}
  .kareler figure{position:relative;border-radius:14px;overflow:hidden;border:1px solid rgba(255,255,255,.07);aspect-ratio:16/10;background:#0a0a12}
  .kareler img{width:100%;height:100%;object-fit:cover;transition:transform 600ms var(--ease-out)}
  .kareler figcaption{position:absolute;left:14px;bottom:12px;z-index:2;font-family:var(--tech);font-size:.7rem;letter-spacing:.18em;text-transform:uppercase;color:#fff;background:#000b;backdrop-filter:blur(4px);padding:6px 10px;border-radius:8px}
  @media(hover:hover){.kareler figure:hover img{transform:scale(1.04)}}
  .logorow{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:8px}
  .logorow a{display:flex;flex-direction:column;align-items:center;gap:14px;padding:30px 22px;border:1px solid rgba(255,255,255,.07);border-radius:16px;background:linear-gradient(165deg,rgba(16,16,24,.9),rgba(4,4,8,.95));transition:transform 200ms var(--ease-out),border-color 200ms var(--ease-out)}
  .logorow a img{height:54px;width:auto}
  .logorow a span{font-family:var(--tech);font-size:.72rem;letter-spacing:.16em;text-transform:uppercase;color:var(--muted)}
  .logorow a[data-b=isisah]:hover{border-color:var(--emb1)}.logorow a[data-b=borsah]:hover{border-color:var(--mnt1)}.logorow a[data-b=salmex]:hover{border-color:var(--ele1)}
  @media(hover:hover){.logorow a:hover{transform:translateY(-4px)}}
  @media(max-width:960px){.pg{padding:120px 0 30px}.pg .wrap{grid-template-columns:1fr}.pg .hero-visual{aspect-ratio:16/9}.kareler{grid-template-columns:1fr}.logorow{grid-template-columns:1fr}}
  .pg .kick{display:inline-flex;align-items:center;gap:10px;border:1px solid var(--line);border-radius:40px;padding:7px 16px;font-family:var(--tech);font-size:.72rem;letter-spacing:.2em;color:var(--steel);text-transform:uppercase;background:#05050acc}
  .pg h1{font-size:clamp(2.6rem,6vw,4.6rem);margin:22px 0 0;line-height:1.02}
  .pg .lead{color:var(--muted);font-size:1.12rem;max-width:760px;margin-top:22px}
  .prose{max-width:820px}
  .prose p{color:var(--steel);margin-top:18px;font-size:1.02rem}
  .prose h2{font-size:clamp(1.8rem,3.6vw,2.6rem);margin-top:70px}
  .prose h2:first-child{margin-top:0}
  .prose ul{list-style:none;margin-top:18px;display:flex;flex-direction:column;gap:10px}
  .prose li{display:flex;gap:12px;color:var(--steel)}
  .prose li::before{content:"";flex:none;width:7px;height:7px;margin-top:10px;border-radius:2px;background:var(--grad);box-shadow:0 0 8px var(--vio2)}
  .quote{border-left:2px solid var(--vio1);padding:6px 0 6px 24px;margin-top:26px;color:var(--steel);font-size:1.05rem}
  .quote footer{border:0;padding:12px 0 0;background:none;color:var(--muted);font-size:.86rem;font-family:var(--tech);letter-spacing:.08em;text-transform:uppercase}
  .two{display:grid;grid-template-columns:1fr 1fr;gap:40px;align-items:start}
  .two .time{margin-top:0}
  .badges{display:flex;flex-wrap:wrap;gap:10px;margin-top:22px}
  .badges span{font-family:var(--tech);font-size:.74rem;letter-spacing:.08em;text-transform:uppercase;color:var(--steel);border:1px solid var(--line);border-radius:40px;padding:8px 14px}
  .badges span b{color:var(--vio1);font-weight:600;margin-left:6px}
  .vmbox{border:1px solid rgba(255,255,255,.07);border-radius:18px;padding:38px;background:linear-gradient(165deg,rgba(16,16,24,.9),rgba(4,4,8,.95));position:relative;overflow:hidden}
  .vmbox::before{content:"";position:absolute;top:0;left:0;width:100%;height:3px;background:linear-gradient(90deg,transparent,var(--bc,var(--vio2)),transparent)}
  .vmbox h2{font-size:2rem;margin:0 0 14px}
  .vmbox p{color:var(--steel);font-size:1.08rem;line-height:1.7}
  .vmbox .k{font-family:var(--tech);font-size:.72rem;letter-spacing:.2em;text-transform:uppercase;color:var(--bc,var(--vio1));margin-bottom:12px;display:block}
  .pgcta{display:flex;gap:14px;flex-wrap:wrap;margin-top:44px}
  @media(max-width:900px){.two{grid-template-columns:1fr}}
'''

CORE_JS = '''<script>
  const hdr=document.getElementById('hdr');
  addEventListener('scroll',()=>hdr.classList.toggle('small',scrollY>40),{passive:true});
  const menuBtn=document.getElementById('menuBtn');
  const syncMenu=()=>menuBtn.setAttribute('aria-expanded',hdr.classList.contains('open')?'true':'false');
  menuBtn.onclick=()=>{hdr.classList.toggle('open');syncMenu();};
  document.querySelectorAll('#links a').forEach(a=>a.addEventListener('click',()=>{hdr.classList.remove('open');syncMenu();}));
  addEventListener('keydown',(e)=>{if(e.key==='Escape'&&hdr.classList.contains('open')){hdr.classList.remove('open');syncMenu();menuBtn.focus();}});
  const reveals=[...document.querySelectorAll('.reveal')];
  let raf=0;
  function showReveals(){raf=0;const vh=innerHeight;let remaining=false;
    for(const el of reveals){if(!el.classList.contains('in')){
      if(el.getBoundingClientRect().top<vh*0.92)el.classList.add('in');else remaining=true;}}
    return remaining;}
  const kick=()=>{if(!raf)raf=requestAnimationFrame(showReveals)};
  addEventListener('scroll',kick,{passive:true,capture:true});
  addEventListener('resize',kick,{passive:true});
  addEventListener('load',showReveals);
  const iv=setInterval(()=>{if(!showReveals())clearInterval(iv);},250);
  setTimeout(()=>{reveals.forEach(el=>el.classList.add('in'));clearInterval(iv);},3000);
  showReveals();
  const counters=[...document.querySelectorAll('[data-count]')];
  const redM=matchMedia('(prefers-reduced-motion: reduce)').matches;
  const fmt=(el,v)=>{el.textContent=(el.dataset.prefix||'')+v.toLocaleString('tr-TR')+(el.dataset.suffix||'');};
  const io=new IntersectionObserver(es=>es.forEach(e=>{
    if(!e.isIntersecting)return; io.unobserve(e.target);
    const el=e.target,end=+el.dataset.count;
    if(redM){fmt(el,end);return;}
    const t0=performance.now(),D=1400;
    (function tick(t){const k=Math.min(1,(t-t0)/D),ease=1-Math.pow(1-k,3);
      fmt(el,Math.round(end*ease)); if(k<1)requestAnimationFrame(tick);})(t0);
  }),{threshold:0.4});
  counters.forEach(el=>io.observe(el));
  document.getElementById('yr').textContent=new Date().getFullYear();
</script>'''

def page(fn, title, desc, kick, h1, lead, body, ld, vis):
    url = f'https://isisah.com.tr/{fn}'
    return f'''<!doctype html>
<html lang="tr">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
<title>{title}</title>
<meta name="description" content="{desc}" />
<meta name="theme-color" content="#000000" />
<link rel="canonical" href="{url}" />
<meta property="og:type" content="website" />
<meta property="og:site_name" content="ISIŞAH GROUP" />
<meta property="og:title" content="{title}" />
<meta property="og:description" content="{desc}" />
<meta property="og:url" content="{url}" />
<meta property="og:image" content="https://isisah.com.tr/showroom/assets/img/og-cover.jpg" />
<meta property="og:image:width" content="1200" /><meta property="og:image:height" content="630" />
<meta name="twitter:card" content="summary_large_image" />
<script type="application/ld+json">{ld}</script>
<link rel="icon" href="assets/img/logo.png" />
<script>document.documentElement.classList.add('js')</script>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
{fonts}
{style[:-8]}{EXTRA_CSS}</style>
</head>
<body>
<a id="top"></a>
<div class="wm" aria-hidden="true">ISIŞAH GROUP</div>
<div class="glow a"></div><div class="glow b"></div>
{sub(header, fn)}

<main>
<section class="pg">
  <div class="wrap">
    <div class="reveal in">
      <span class="kick">{kick}</span>
      <h1>{h1}</h1>
      <p class="lead">{lead}</p>
    </div>
    <div class="hero-visual reveal in" data-d="2">{vis}</div>
  </div>
</section>
{body}
</main>

{sub(footer, fn)}
{CORE_JS}
</body>
</html>
'''

ORG = '{"@context":"https://schema.org","@type":"Organization","name":"ISIŞAH GROUP","legalName":"ISIŞAH Endüstriyel","url":"https://isisah.com.tr/","foundingDate":"1982","address":{"@type":"PostalAddress","streetAddress":"DOSAB Ali Osman Sönmez Cad. No:11","addressLocality":"Osmangazi","addressRegion":"Bursa","postalCode":"16369","addressCountry":"TR"},"telephone":"+90 224 261 05 27","email":"info@isisah.com.tr","sameAs":["https://www.instagram.com/isisah_group","https://www.linkedin.com/in/isi%C5%9Fah-group-9b45aa125/"],"brand":[{"@type":"Brand","name":"ISIŞAH ENDÜSTRİYEL"},{"@type":"Brand","name":"BORŞAH BORU"},{"@type":"Brand","name":"SALMEX"}]}'

# ---------------- HAKKIMIZDA ----------------
hak_body = '''
<section class="stats" style="margin-top:30px">
  <div class="wrap">
    <div class="stat reveal"><div class="n grad-text" data-count="44" data-suffix=" yıl">0 yıl</div><div class="k">Kesintisiz Üretim</div></div>
    <div class="stat reveal" data-d="1"><div class="n grad-text" data-count="3" data-suffix=" marka">0 marka</div><div class="k">Tek Çatı Altında</div></div>
    <div class="stat reveal" data-d="2"><div class="n grad-text" data-count="8">0</div><div class="k">Ürün Gamı · Mutfaktan Savunmaya</div></div>
    <div class="stat reveal" data-d="3"><div class="n grad-text" data-count="100" data-prefix="%">%0</div><div class="k">Yerli Üretim</div></div>
  </div>
</section>

<section class="pad" style="padding-top:90px">
  <div class="wrap two">
    <div class="prose reveal">
      <h2>Kuruluş ve gelişim</h2>
      <p>ISIŞAH markası, 1982 yılında çeşitli endüstri kolları için sanayi tipi rezistansların üretimini ve satışını yapmak amacıyla kurulmuştur. 1995 yılında kurduğu entegre tesis ile elektrikli ev aletleri için seri üretime başlamıştır. 2003 yılında sanayi tipi endüstriyel üretim için ayrı bir tesis oluşturulmuş; seri üretimden tamamen bağımsız, özel üretime yönelik çalışmalar yürütülmüştür.</p>
      <p>Pazarlama alanında yaptığı yeniliklerle şirketin hizmet alanı her geçen gün genişlemiş; müşterilerine daha profesyonel hizmet verebilmek için kurumsal bir yapıya dönüşme ihtiyacı doğmuştur. 2011 yılı itibariyle ISIŞAH GROUP çatısı altında yeniden yapılanan grup, bugün <b>ISIŞAH ENDÜSTRİYEL</b> (sanayi tipi rezistans ve ısıtma sistemleri), <b>BORŞAH BORU</b> (paslanmaz çelik boru) ve <b>SALMEX</b> (ısı eşanjörleri) markalarıyla üretim yapmaktadır.</p>
      <p>Türkiye'de sektörünün en büyük firmalarından biri olarak ISIŞAH, 44 yılın verdiği güç ve tecrübeyle elektrikli ev aletlerine yönelik ve çeşitli endüstri grupları için ısıtma sistemlerini ISO 9001:2015 kalite yönetim sistemi altında üretmeyi kendine prensip edinmiştir.</p>
      <div class="badges">
        <span>Kuruluş<b>1982</b></span><span>Merkez<b>DOSAB · Bursa</b></span><span>Kalite<b>ISO 9001:2015</b></span><span>Marka<b>3</b></span>
      </div>
    </div>
    <div class="reveal" data-d="2">
      <h2 style="font-size:1.6rem;margin-bottom:10px">Tarihçe</h2>
      <div class="about" style="display:block"><div class="time">
        <div class="row"><span class="yr">1982</span><span class="tx">Sanayi tipi rezistans üretimi için kuruluş.</span></div>
        <div class="row"><span class="yr">1986</span><span class="tx">İlk demiryolu projesi: TÜVASAŞ yolcu vagonu ısıtma üniteleri.</span></div>
        <div class="row"><span class="yr">1988</span><span class="tx">TSE — Türk Standartlarına Uygunluk Belgesi.</span></div>
        <div class="row"><span class="yr">1995</span><span class="tx">Entegre tesis; elektrikli ev aletleri için seri üretime geçiş.</span></div>
        <div class="row"><span class="yr">1997</span><span class="tx">VDE — DIN EN normlarına uygunluk sertifikaları (Almanya).</span></div>
        <div class="row"><span class="yr">2003</span><span class="tx">Sanayi tipi özel üretim için ayrı tesis.</span></div>
        <div class="row"><span class="yr">2004</span><span class="tx">TS EN ISO 9001 kalite sistem belgesi.</span></div>
        <div class="row"><span class="yr">2010</span><span class="tx">UL — ABD standartlarına uygunluk sertifikası.</span></div>
        <div class="row"><span class="yr">2011</span><span class="tx">ISIŞAH GROUP çatısı altında yeniden yapılanma.</span></div>
      </div></div>
    </div>
  </div>
</section>

<section class="pad" style="padding-top:0">
  <div class="wrap">
    <div class="sec-head reveal"><h2>Üretimden kareler.</h2><p>DOSAB Bursa tesislerimizden — robotlu eşanjör hattı, profil hattı ve test istasyonu.</p></div>
    <div class="kareler reveal">
      <figure><img src="assets/img/uretim-k1.webp" alt="Robotlu üretim hücresi" loading="lazy" decoding="async"><figcaption>Robotlu Hat</figcaption></figure>
      <figure><img src="assets/img/uretim-k2.webp" alt="Profil şekillendirme hattı" loading="lazy" decoding="async"><figcaption>Şekillendirme</figcaption></figure>
      <figure><img src="assets/img/uretim-k3.webp" alt="Sızdırmazlık test istasyonu" loading="lazy" decoding="async"><figcaption>Test İstasyonu</figcaption></figure>
    </div>
    <div class="pgcta reveal" style="margin-top:22px"><a class="btn ghost" href="fabrika.html">Fabrika turuna çık <span>→</span></a></div>
  </div>
</section>

<section class="pad" style="padding-top:0">
  <div class="wrap">
    <div class="two">
      <div class="prose reveal">
        <h2>Yönetimden</h2>
        <p>ISIŞAH A.Ş., 1982 yılında çeşitli endüstri kolları için sanayi tipi rezistansların üretimini ve pazarlamasını yapmak için kurulmuştur. Üretim ve pazarlama faaliyetleri alanında yapılan değişiklikler şirketin aktivite alanını genişletmiş, sektördeki iddiasını ve gücünü artırmıştır.</p>
        <div class="quote">Şirketimiz bugün sahip olduğu gücünü kalite sisteminin varlığına, sektördeki tecrübe ve birikimine, yerel sermaye ile kurulmuş en büyük ve gelişmiş firma olmasına, müşterilerimizde oluşmuş marka güvenine, insan ve sisteme dayalı düşünce yapımıza, köklü geçmişimize, piyasadaki itibarımıza, yüksek kaliteli makine parkımıza, gelişmiş altyapı ve donanımımıza borçludur.
          <footer>Mehmet Şahin — Yönetim Kurulu Başkanı</footer></div>
      </div>
      <div class="prose reveal" data-d="2">
        <h2>İnovasyon ve Ar-Ge</h2>
        <p><b>Tasarım politikamız:</b> İnovasyon (sürekli değişim) felsefesi benimsenmiş olup, genç ve dinamik tasarım ekibiyle gerek mevcut trendleri takip ederek gerekse kendi trendini oluşturarak müşterilerin ihtiyaç ve beklentilerini karşılayacak özgün, fonksiyonel modeller tasarlamak; tasarımlarıyla takip edilen ve gelecek trendleri belirleyen marka olmak.</p>
        <p><b>Ar-Ge politikamız:</b></p>
        <ul>
          <li>Hedef müşteri kitlesine uygun modelleri CAD sistemiyle optimum şekilde üretime hazırlamak.</li>
          <li>Müşterilerden gelen istek ve talepleri, teknik ekibimizle sahada sistem analizi yaparak çözüme dönüştürmek.</li>
          <li>Üretim ve tedarikçi zincirleriyle güçlü bir bağ kurarak dinamik bir yapıya sahip olmak.</li>
          <li>İnovatif yaklaşımlar ve öneri sistemiyle üretilmekte olan ürünleri sürekli geliştirmek.</li>
          <li>ERP sistemiyle üretimin teknik altyapıyla ilişkisini güçlendirmek.</li>
          <li>Kalite, Çevre, İş Sağlığı ve Güvenliği politikalarıyla eşgüdümlü çalışmak.</li>
        </ul>
        <p><b>Ar-Ge çalışmaları:</b> Türkiye'de ilk defa mobil elektrikli ısıtma ünitelerinde patentli ürünler üretilmiştir. Türkiye'de ilk defa yerli imalat olarak patentli infrared teknolojili oto boya kurutma ünitesi (BOYKUR) üretilmiştir.</p>
      </div>
    </div>
  </div>
</section>

<section class="pad" style="padding-top:0">
  <div class="wrap">
    <div class="sec-head reveal"><h2>Belgelerimiz.</h2><p>Sistem ve ürün standardı uygunluk belgeleri.</p></div>
    <div class="railcols reveal" style="margin-top:0">
      <div class="railbox"><h3>Sistem standardı</h3><ul>
        <li>TS EN ISO 9001:2015 Kalite Yönetim Sistemi (ISO 9001 belgeli: 2004'ten beri)</li>
        <li>Entegre Kalite, Çevre ve İş Sağlığı-Güvenliği yönetim sistemi politikası</li>
      </ul></div>
      <div class="railbox"><h3>Ürün standardı</h3><ul>
        <li>TSE — Türk Standartlarına Uygunluk Belgesi (1988'den beri)</li>
        <li>CE — Avrupa Birliği uygunluğu; EN 60204-1 uygunluk</li>
        <li>VDE — DIN EN normlarına uygunluk sertifikaları, Almanya (1997'den beri)</li>
        <li>UL — ABD UL standartlarına uygunluk sertifikası (2010'dan beri)</li>
        <li>RoHS uyumlu malzeme kullanımı</li>
      </ul></div>
    </div>
    <div class="pgcta reveal">
      <a class="btn" href="vizyon-misyon.html">Vizyonumuz &amp; Misyonumuz <span>→</span></a>
      <a class="btn ghost" href="urunler.html">3B Showroom</a>
      <a class="btn ghost" href="fabrika.html">Fabrika Turu</a>
      <a class="btn ghost" href="index.html#iletisim">İletişim</a>
    </div>
  </div>
</section>
'''
hak_ld = '{"@context":"https://schema.org","@type":"AboutPage","name":"Hakkımızda — ISIŞAH GROUP","url":"https://isisah.com.tr/hakkimizda.html","mainEntity":'+ORG+'}'
(ROOT/'hakkimizda.html').write_text(page('hakkimizda.html',
    'Hakkımızda — ISIŞAH GROUP | 1982\'den bugüne Bursa DOSAB',
    'ISIŞAH GROUP hakkında: 1982 kuruluş, entegre tesisler, ISIŞAH ENDÜSTRİYEL · BORŞAH BORU · SALMEX markaları, tarihçe, yönetim, Ar-Ge ve kalite belgeleri.',
    'ISIŞAH GROUP · 1982\'den bugüne', 'Hakkımızda.',
    'Bursa DOSAB\'da sanayi tipi rezistanstan paslanmaz çelik boruya ve ısı eşanjörlerine uzanan üç marka, tek çatı: 44 yıllık mühendislik birikimi.',
    hak_body, hak_ld,
    '<img src="assets/img/bina-gece-3marka.webp" alt="ISIŞAH GROUP merkez binası — üç marka, DOSAB Bursa" width="1600" height="905" fetchpriority="high"><span class="tag">ISIŞAH GROUP · DOSAB Bursa</span>'), encoding='utf-8')

# ---------------- VİZYON & MİSYON ----------------
viz_body = '''
<section class="pad" style="padding-top:40px">
  <div class="wrap two">
    <div class="vmbox reveal" style="--bc:var(--emb1)">
      <span class="k">Vizyonumuz</span>
      <h2>Zirvede, güvenilir, global.</h2>
      <p>Müşterilerimizi, çalışanlarımızı ve bayilerimizi her daim memnun ve mutluluğa ulaştıran; kaliteden ödün vermeden zirvede, güvenilir ve lider global şirket olmak.</p>
    </div>
    <div class="vmbox reveal" data-d="2" style="--bc:var(--ele1)">
      <span class="k">Misyonumuz</span>
      <h2>Müşterimize ortağımız gibi.</h2>
      <p>Türkiye'de sektörünün en büyük firmalarından biri olarak ISIŞAH, 44 yılın verdiği güç ve tecrübeyle elektrikli ev aletlerine yönelik ve çeşitli endüstri grupları için ısıtma sistemlerinin ISO 9001 kalite standardında üretimini kendine prensip edinmiştir. Müşterilerimize şirket ortağımız gibi davranmak ve kıymetli müşterilerimiz için değer yaratmak misyonumuzdur.</p>
    </div>
  </div>
</section>

<section class="pad" style="padding-top:0">
  <div class="wrap">
    <div class="sec-head reveal"><h2>Üç marka, tek vizyon.</h2><p>Aynı çatı, aynı kalite disiplini.</p></div>
    <div class="logorow reveal">
      <a data-b="isisah" href="index.html#marka=isisah"><img src="assets/catalog/logo-isisah.webp" alt="ISIŞAH ENDÜSTRİYEL"><span>Rezistans &amp; Isıtma Sistemleri</span></a>
      <a data-b="borsah" href="index.html#marka=borsah"><img src="assets/catalog/logo-borsah.webp" alt="BORŞAH BORU"><span>Paslanmaz Çelik Boru</span></a>
      <a data-b="salmex" href="index.html#marka=salmex"><img src="assets/catalog/logo-salmex.webp" alt="SALMEX"><span>Isı Eşanjörleri</span></a>
    </div>
  </div>
</section>

<section class="pad" style="padding-top:0">
  <div class="wrap">
    <div class="prose reveal" style="max-width:900px;margin:0 auto">
      <h2>Kalite, İSG ve Çevre Politikamız</h2>
      <p>Müşteri kalite beklentilerini algılayan, değer zincirindeki tüm ürün ve süreçlerini bu doğrultuda sürekli geliştiren lider bir şirket olmayı hedefleriz. Bu amaçla;</p>
      <ul>
        <li>İnsan odaklı bir yaklaşımla çalışanlarımızı geliştirir; yapılan her faaliyette kalite bilincini ve sorgulayıcı bakış açısını dikkate alan şirket kültürünü benimseriz.</li>
        <li>Tüm değer zincirindeki standartların dünya klasında olması için rekabetçilik hedefiyle sürekli gelişim sağlarız.</li>
        <li>Yeniliklere açık oluruz; her noktada sürekli iyileşmeyi ve mükemmel olanı üretmeyi hedefleriz.</li>
        <li>Tüm üretim ve hizmet aşamalarımızda çevre kirliliğinin önlenmesini izler; sürdürülebilir doğal kaynak kullanımını ve çevresel performansımızı geliştiririz.</li>
        <li>Firmamızda müşteri, ziyaretçi ve tüm çalışanların iş sağlığı ve güvenliğini sağlarız.</li>
        <li>Sürekli müşteri memnuniyetini tam zamanında hizmet ve teknolojik üretimle artırırız.</li>
        <li>Sürekli iyileştirme kapsamında çalışanların gelişimi, çevre bilincinin artırılması ve iş sağlığı-güvenliğinin sağlanması için eğitimler düzenleriz.</li>
        <li>Süreçlerimizde ISO 9001 kalite yönetim sistemine ve sektörümüze uygun tüm yasal standartlara, iş sağlığı-güvenliği ve çevre mevzuatına uyarız.</li>
        <li>Sürdürülebilir, yalın ve proaktif bir şekilde Entegre Kalite, Çevre ve İş Sağlığı-Güvenliği yönetim sistemine tüm personelin katılımını sağlar; etkinliğini izler ve sürekli iyileştiririz.</li>
      </ul>
      <div class="quote">ISIŞAH GROUP bu politikanın tüm çalışanlarına iletileceğini ve anlaşılmasını sağlayacağını taahhüt eder.
        <footer>Mehmet Şahin — Genel Müdür</footer></div>
      <div class="pgcta">
        <a class="btn" href="hakkimizda.html">Hakkımızda <span>→</span></a>
        <a class="btn ghost" href="urunler.html">3B Showroom</a>
        <a class="btn ghost" href="index.html#iletisim">İletişim</a>
      </div>
    </div>
  </div>
</section>
'''
viz_ld = '{"@context":"https://schema.org","@type":"WebPage","name":"Vizyonumuz ve Misyonumuz — ISIŞAH GROUP","url":"https://isisah.com.tr/vizyon-misyon.html","about":'+ORG+'}'
(ROOT/'vizyon-misyon.html').write_text(page('vizyon-misyon.html',
    'Vizyonumuz ve Misyonumuz — ISIŞAH GROUP',
    'ISIŞAH GROUP vizyonu, misyonu ve Kalite-İSG-Çevre politikası: kaliteden ödün vermeden güvenilir, lider global şirket olmak; müşterilerimize şirket ortağımız gibi davranmak.',
    'ISIŞAH GROUP · Kurumsal', 'Vizyonumuz &amp;<br>Misyonumuz.',
    'Kaliteden ödün vermeden, müşterimize şirket ortağımız gibi davranarak.',
    viz_body, viz_ld,
    '<img src="assets/img/salmex-hat.webp" alt="SALMEX robotlu eşanjör üretim hattı" loading="eager"><span class="tag">DOSAB Bursa · Robotlu Hat</span>'), encoding='utf-8')
print('hakkimizda.html', (ROOT/'hakkimizda.html').stat().st_size//1024, 'KB |', 'vizyon-misyon.html', (ROOT/'vizyon-misyon.html').stat().st_size//1024, 'KB')
