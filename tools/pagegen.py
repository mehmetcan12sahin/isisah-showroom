#!/usr/bin/env python3
# Ortak sayfa iskeleti: index.html'in stil/header/footer'ından statik alt sayfalar üretir.
# build-pages.py (kurumsal) ve build-category-pages.py (kategori/marka) BUNU import eder.
# index.html'in CSS'i değişince ÜÇÜNÜ de yeniden çalıştır.
import re, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
idx = (ROOT/'index.html').read_text(encoding='utf-8')
style  = re.search(r'<style>.*?</style>', idx, re.S).group(0)
fonts  = re.search(r'<link rel="stylesheet" href="assets/fonts/inter\.css">', idx).group(0)
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
  // header shrink
  const hdr=document.getElementById('hdr');
  addEventListener('scroll',()=>hdr.classList.toggle('small',scrollY>40),{passive:true});
  // mobile menu
  const menuBtn=document.getElementById('menuBtn');
  const linksNav=document.getElementById('links');
  const syncMenu=()=>menuBtn.setAttribute('aria-expanded',hdr.classList.contains('open')?'true':'false');
  function closeAllDD(){document.querySelectorAll('.navdd').forEach(dd=>{dd.classList.remove('open');dd.querySelector('.dd-btn').setAttribute('aria-expanded','false');});}
  function openMenu(){hdr.classList.add('open');syncMenu();const first=linksNav.querySelector('a,button');if(first)first.focus();}
  function closeMenu(focusBtn){hdr.classList.remove('open');syncMenu();closeAllDD();if(focusBtn)menuBtn.focus();}
  menuBtn.onclick=()=>{hdr.classList.contains('open')?closeMenu(false):openMenu();};
  document.querySelectorAll('#links a').forEach(a=>a.addEventListener('click',()=>closeMenu(false)));
  addEventListener('keydown',(e)=>{if(e.key==='Escape'&&hdr.classList.contains('open')){closeMenu(true);}});
  // nav açılır menüleri (Sektörler / Kurumsal) — disclosure pattern (index.html ile birebir)
  document.querySelectorAll('.navdd').forEach(dd=>{
    const btn=dd.querySelector('.dd-btn'),menu=dd.querySelector('.dd-menu');
    const open=()=>{closeAllDD();dd.classList.add('open');btn.setAttribute('aria-expanded','true');};
    const close=(focusBtn)=>{dd.classList.remove('open');btn.setAttribute('aria-expanded','false');if(focusBtn)btn.focus();};
    btn.addEventListener('click',e=>{e.stopPropagation();dd.classList.contains('open')?close(false):open();});
    btn.addEventListener('keydown',e=>{
      if(e.key==='Escape'&&dd.classList.contains('open')){e.stopPropagation();close(true);}
      else if(e.key==='ArrowDown'&&!dd.classList.contains('open')){e.preventDefault();open();const f=menu.querySelector('a');if(f)f.focus();}
    });
    menu.addEventListener('keydown',e=>{if(e.key==='Escape'){e.stopPropagation();close(true);}});
  });
  document.addEventListener('click',e=>{if(!e.target.closest('.navdd'))closeAllDD();});
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

def page(fn, title, desc, kick, h1, lead, body, ld, vis, og_image=None, og_w=1200, og_h=630):
    # og_image: assets/... köküne göreli yol (gerçek görsel, showroom altında barındırılır — deploy topolojisi).
    # Verilmezse (veya boyutu okunamadıysa) jenerik og-cover.jpg 1200x630'a düşer; ASLA sahte 1200x630 iddia etme
    # (çağıran taraf gerçek piksel boyutunu sips/python ile ölçüp og_w/og_h ile geçirmeli).
    url = f'https://isisah.com.tr/{fn}'
    og_url = f'https://isisah.com.tr/showroom/{og_image}' if og_image else 'https://isisah.com.tr/showroom/assets/img/og-cover.jpg'
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
<meta property="og:image" content="{og_url}" />
<meta property="og:image:width" content="{og_w}" /><meta property="og:image:height" content="{og_h}" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1" />
<meta property="og:locale" content="tr_TR" />
<meta name="twitter:title" content="{title}" />
<meta name="twitter:description" content="{desc}" />
<meta name="twitter:image" content="{og_url}" />
<script type="application/ld+json">{ld}</script>
<link rel="icon" href="/favicon.ico" sizes="32x32" />
<link rel="icon" type="image/png" sizes="48x48" href="assets/img/favicon-48.png" />
<link rel="icon" type="image/png" sizes="192x192" href="assets/img/favicon-192.png" />
<link rel="apple-touch-icon" sizes="180x180" href="assets/img/apple-touch-icon.png" />
<link rel="manifest" href="assets/site.webmanifest" />
<script>document.documentElement.classList.add('js')</script>
{fonts}
{style[:-8]}{EXTRA_CSS}</style>
</head>
<body>
<a class="skip-link" href="#main">İçeriğe atla</a>
<div class="wm" aria-hidden="true">ISIŞAH GROUP</div>
<div class="glow a"></div><div class="glow b"></div>
{sub(header, fn)}

<main id="main">
<a id="top"></a>
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

