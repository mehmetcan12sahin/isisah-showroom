#!/usr/bin/env python3
# 10 kategori (gam) sayfası + 3 marka hub sayfası — index.html'in stil/header/footer'ından (tools/pagegen.py).
# İçerik TEK KAYNAK assets/data/products.json'dan gelir (fabrikasyon yok; bkz. tools/build-products.py,
# .claude/skills/isisah-urun-ekle/SKILL.md). Ürün metni değişince önce products.json'u güncelleyip
# build-products.py'yi, ardından bu scripti çalıştırın. Kategori/hub başlıkları, girişleri ve her
# sayfanın hangi ürün anahtarlarını (keys) içerdiği hâlâ bu dosyada elle tanımlanır.
# Çalıştır: python3 tools/build-category-pages.py  (repo kökünden veya tools/ içinden)
import json, pathlib, re, subprocess
from urllib.parse import quote
from pagegen import ROOT, page, ORG

def img_size(rel_path):
    """Görselin GERÇEK piksel boyutu (macOS 'sips' ile, yeni bağımlılık eklemeden).
    Okunamazsa (None, None) döner — çağıran taraf bu durumda eski 1200x800/1200x630
    varsayılanına düşer; ASLA sahte/tahmini boyut iddia ETME (G2 kuralı)."""
    try:
        out = subprocess.run(['sips', '-g', 'pixelWidth', '-g', 'pixelHeight', str(ROOT / rel_path)],
                              capture_output=True, text=True, timeout=10, check=True).stdout
        w = re.search(r'pixelWidth:\s*(\d+)', out)
        h = re.search(r'pixelHeight:\s*(\d+)', out)
        if w and h:
            return int(w.group(1)), int(h.group(1))
    except Exception:
        pass
    return None, None

# ---------------- ürün verisi: TEK KAYNAK assets/data/products.json (fabrikasyon yok) ----------------
_PRODUCTS_PATH = ROOT / 'assets/data/products.json'
_products = json.loads(_PRODUCTS_PATH.read_text(encoding='utf-8'))['products']
if len(_products) < 30:
    raise SystemExit(f'HATA: {_PRODUCTS_PATH} beklenenden az ürün içeriyor ({len(_products)}).')


def _by_brand(brand):
    return {p['img']: (p['h'], p['p'], p['chips']) for p in _products if p['brand'] == brand}


ISISAH = _by_brand('isisah')
SALMEX = _by_brand('salmex')
BORSAH = _by_brand('borsah')

def cards(src, keys):
    out = ['<div class="katgrid reveal">']
    for k in keys:
        h, p, chips = src[k]
        chipstr = ''.join(f'<span>{c}</span>' for c in chips)
        out.append(f'<article class="katcard"><h3>{h}</h3><p>{p}</p><div class="chips">{chipstr}</div></article>')
    out.append('</div>')
    return '\n'.join(out)

def breadcrumb_ld(name, url):
    return ('{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":['
            '{"@type":"ListItem","position":1,"name":"Ana Sayfa","item":"https://isisah.com.tr/"},'
            '{"@type":"ListItem","position":2,"name":"Ürünler","item":"https://isisah.com.tr/showroom/urunler.html"},'
            f'{{"@type":"ListItem","position":3,"name":"{name}","item":"{url}"}}]}}')

def collection_ld(name, url, desc, items, brandname):
    # brandname: sayfanın gerçek marka hub'ı (ISIŞAH ENDÜSTRİYEL / SALMEX / BORŞAH BORU) —
    # urunler.html'in kendi JSON-LD ItemList'indeki marka adlarıyla birebir (fabrikasyon yok, F1 düzeltmesi).
    li = ','.join(f'{{"@type":"Product","position":{i+1},"name":"{h}","description":"{p}","brand":{{"@type":"Brand","name":"{brandname}"}}}}' for i,(h,p,_) in enumerate(items))
    return ('{"@context":"https://schema.org","@type":"CollectionPage","name":"'+name+'","url":"'+url+'","description":"'+desc+'",'
            '"isPartOf":{"@type":"WebSite","name":"ISIŞAH GROUP","url":"https://isisah.com.tr/"},'
            '"mainEntity":{"@type":"ItemList","itemListElement":['+li+']}}')

KATGRID_CSS = '''
  .katgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:10px}
  .katcard{border:1px solid rgba(255,255,255,.07);border-radius:16px;padding:24px;background:linear-gradient(165deg,rgba(16,16,24,.9),rgba(4,4,8,.95))}
  .katcard h3{font-size:1.08rem;margin:0}
  .katcard p{color:var(--steel);font-size:.92rem;margin-top:10px;line-height:1.55}
  .katcard .chips{display:flex;flex-wrap:wrap;gap:8px;margin-top:14px}
  .katcard .chips span{font-family:var(--tech);font-size:.72rem;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);border:1px solid var(--line);border-radius:40px;padding:5px 10px}
  .hubgrid{display:grid;grid-template-columns:repeat(2,1fr);gap:16px;margin-top:10px}
  .hubcard{display:flex;flex-direction:column;gap:8px;border:1px solid rgba(255,255,255,.07);border-radius:16px;padding:22px;background:linear-gradient(165deg,rgba(16,16,24,.9),rgba(4,4,8,.95));transition:border-color 200ms}
  .hubcard:hover{border-color:var(--vio1)}
  .hubcard b{font-size:1rem}
  .hubcard span{color:var(--muted);font-size:.86rem}
  @media(max-width:900px){.katgrid{grid-template-columns:1fr 1fr}.hubgrid{grid-template-columns:1fr}}
  @media(max-width:640px){.katgrid{grid-template-columns:1fr}}
  .pgcta-mail{margin-top:14px;color:var(--steel);font-size:.92rem}
  .pgcta-mail a{color:var(--ink);text-decoration:underline;text-underline-offset:3px}
'''

def cat_body(h1, slug_noext, holkey, brandhub, brandhubname, intro_p, src, keys,
             secim_kriterleri=None, teklif_bilgileri=None, extra_body=''):
    # secim_kriterleri / teklif_bilgileri: veri yok (CC-3) — hiçbir çağrı bunları şu an geçmiyor.
    # Şirketten gerçek "nasıl seçilir" kriterleri / teklif için istenen bilgi listesi gelmeden
    # buraya fabrikasyon madde EKLENMEMELİ; parametreler sadece veri gelince render edilsin diye var.
    h1_plain = h1.replace('<br>', ' ')
    mail_subject = quote(f'Teklif Talebi — {h1_plain}')
    extra = ''
    if secim_kriterleri:
        lis = ''.join(f'<li>{x}</li>' for x in secim_kriterleri)
        extra += f'''
<section class="pad" style="padding-top:0">
  <div class="wrap prose" style="max-width:820px">
    <h2>Nasıl seçilir?</h2>
    <ul>{lis}</ul>
  </div>
</section>'''
    if teklif_bilgileri:
        lis = ''.join(f'<li>{x}</li>' for x in teklif_bilgileri)
        extra += f'''
<section class="pad" style="padding-top:0">
  <div class="wrap prose" style="max-width:820px">
    <h2>Teklif için gerekli bilgiler</h2>
    <ul>{lis}</ul>
  </div>
</section>'''
    return f'''
<style>{KATGRID_CSS}</style>
<section class="pad" style="padding-top:30px">
  <div class="wrap prose" style="max-width:900px">
    <p>{intro_p}</p>
    <div class="pgcta">
      <a class="btn" href="teklif.html?konu={slug_noext}">Teklif İste <span>→</span></a>
      <a class="btn ghost" href="urunler.html#hol={holkey}">3B Showroom'da incele</a>
      <a class="btn ghost" href="tel:+902242610527">Ara</a>
    </div>
    <p class="pgcta-mail">veya e-posta ile yazın: <a href="mailto:info@isisah.com.tr?subject={mail_subject}">info@isisah.com.tr</a></p>
  </div>
</section>
<section class="pad" style="padding-top:0">
  <div class="wrap">
    <div class="sec-head reveal"><h2>Ürün gamı.</h2><p>{len(keys)} ürün — tam teknik detay ve 3B görünüm için showroom'a geçin.</p></div>
    {cards(src, keys)}
  </div>
</section>
{extra}{extra_body}
<section class="pad" style="padding-top:0">
  <div class="wrap">
    <div class="pgcta reveal">
      <a class="btn ghost sc" href="{brandhub}">{brandhubname} markasının tamamı <span>→</span></a>
      <a class="btn ghost" href="hakkimizda.html">Hakkımızda</a>
      <a class="btn ghost" href="index.html#iletisim">İletişim</a>
    </div>
  </div>
</section>
'''

def build_cat(slug, holkey, title, desc, kick, h1, lead, intro_p, src, keys, brandhub, brandhubname, vis_img, vis_alt,
              secim_kriterleri=None, teklif_bilgileri=None, extra_body=''):
    url = f'https://isisah.com.tr/{slug}'
    slug_noext = slug[:-5] if slug.endswith('.html') else slug
    items = [src[k] for k in keys]
    h1_plain = h1.replace('<br>',' ')
    ld = '[' + collection_ld(h1_plain, url, desc, items, brandhubname) + ',' + breadcrumb_ld(h1_plain, url) + ']'
    body = cat_body(h1, slug_noext, holkey, brandhub, brandhubname, intro_p, src, keys,
                     secim_kriterleri, teklif_bilgileri, extra_body)
    w, h = img_size(vis_img)  # gerçek piksel boyutu (sips) — okunamazsa eski 1200x800 varsayılanına düş
    dims = f'width="{w}" height="{h}"' if w and h else 'width="1200" height="800"'
    vis = f'<img src="{vis_img}" alt="{vis_alt}" loading="eager" {dims}><span class="tag">{brandhubname}</span>'
    og_w, og_h = (w, h) if w and h else (1200, 630)
    (ROOT/slug).write_text(page(slug, title, desc, kick, h1, lead, body, ld, vis,
                                 og_image=vis_img, og_w=og_w, og_h=og_h), encoding='utf-8')
    return len(title), len(desc)

def build_hub(slug, title, desc, kick, h1, lead, intro_p, spokes, doorkey, logo, vis_img, vis_alt):
    url = f'https://isisah.com.tr/{slug}'
    slug_noext = slug[:-5] if slug.endswith('.html') else slug
    mail_subject = quote(f'Teklif Talebi — {h1}')
    cardsHtml = ''.join(f'<a class="hubcard reveal" href="{s[0]}"><b>{s[1]}</b><span>{s[2]}</span></a>' for s in spokes)
    body = f'''
<style>{KATGRID_CSS}</style>
<section class="pad" style="padding-top:30px">
  <div class="wrap prose" style="max-width:900px">
    <p>{intro_p}</p>
    <div class="pgcta">
      <a class="btn" href="teklif.html?konu={slug_noext}">Teklif İste <span>→</span></a>
      <a class="btn ghost sc" href="urunler.html#marka={doorkey}">3B Showroom'da marka kapısını aç</a>
      <a class="btn ghost" href="tel:+902242610527">Ara</a>
    </div>
    <p class="pgcta-mail">veya e-posta ile yazın: <a href="mailto:info@isisah.com.tr?subject={mail_subject}">info@isisah.com.tr</a></p>
  </div>
</section>
<section class="pad" style="padding-top:0">
  <div class="wrap">
    <div class="sec-head reveal"><h2>Ürün gamları.</h2><p>Kategoriye göre incele, showroom'da 3B gör.</p></div>
    <div class="hubgrid">{cardsHtml}</div>
  </div>
</section>
<section class="pad" style="padding-top:0">
  <div class="wrap">
    <div class="pgcta reveal">
      <a class="btn ghost" href="hakkimizda.html">Hakkımızda</a>
      <a class="btn ghost" href="vizyon-misyon.html">Vizyon &amp; Misyon</a>
      <a class="btn ghost" href="index.html#iletisim">İletişim</a>
    </div>
  </div>
</section>
'''
    ld = '[' + ('{"@context":"https://schema.org","@type":"CollectionPage","name":"'+h1+'","url":"'+url+'","description":"'+desc+'",'
          '"isPartOf":{"@type":"WebSite","name":"ISIŞAH GROUP","url":"https://isisah.com.tr/"}}') + ',' + breadcrumb_ld(h1, url) + ']'
    w, h = img_size(vis_img)  # gerçek piksel boyutu (sips) — okunamazsa eski 1200x800 varsayılanına düş
    dims = f'width="{w}" height="{h}"' if w and h else 'width="1200" height="800"'
    vis = f'<img src="{vis_img}" alt="{vis_alt}" loading="eager" {dims}><span class="tag">{h1}</span>'
    og_w, og_h = (w, h) if w and h else (1200, 630)
    (ROOT/slug).write_text(page(slug, title, desc, kick, h1, lead, body, ld, vis,
                                 og_image=vis_img, og_w=og_w, og_h=og_h), encoding='utf-8')
    return len(title), len(desc)

# G4: index.html'in eski #demiryolu bölümünden VERBATİM taşınan zaman çizelgesi + test/malzeme kutuları
# (kaynak: git show HEAD:index.html, eski #demiryolu satır ~741-783). Metin harfiyen aynı, olgular değişmedi.
# "Referanslar" listesi (railrefs) buraya taşınMADI — H tarafından zaten #kurumsal'a "Referanslarımızdan"
# olarak taşındı; burada tekrarlanırsa aynı liste iki yerde mükerrer olur.
DEMIRYOLU_EXTRA = '''
<section class="pad" style="padding-top:0">
  <div class="wrap">
    <div class="sec-head reveal"><h2>Proje geçmişi.</h2><p>1986'dan bugüne demiryolu projelerimiz.</p></div>
    <div class="railtime reveal">
      <div class="row"><span class="yr">1986</span><span class="tx"><b>TÜVASAŞ TIJ Projesi:</b> yolcu vagonları pencere altı ısıtma üniteleri.</span></div>
      <div class="row"><span class="yr">1995</span><span class="tx"><b>TÜVASAŞ TVS 2000:</b> vagon altı (şasi) ısıtıcılar.</span></div>
      <div class="row"><span class="yr">2009-10</span><span class="tx"><b>TÜLOMSAŞ Projesi:</b> lokomotif rezistans üniteleri.</span></div>
      <div class="row"><span class="yr">2011-26</span><span class="tx"><b>Makas & Ray Isıtıcıları + Personel Isıtıcıları:</b> tamamı paslanmaz personel ısıtma üniteleri; termostatik aşırı ısınma emniyeti.</span></div>
      <div class="row"><span class="yr">2014</span><span class="tx"><b>Ankara Metro:</b> koltuk ısıtıcıları (750 W / 1300 W – 380 V), HVAC ısıtma elemanları ve fren borusu projesi (Borşah paslanmaz borularıyla).</span></div>
      <div class="row"><span class="yr">2015-16</span><span class="tx"><b>Tramvay Klima Isıtıcısı · TÜVASAŞ DMU · İstanbul Ulaşım Modernizasyon · YZK 850 İBB:</b> yüksek hızlı tren yolcu ısıtıcıları, yüksek gerilim dayanımı.</span></div>
      <div class="row"><span class="yr">2016-17</span><span class="tx"><b>E-14000 / İstanbul Ulaşım:</b> tren klima ısıtıcıları (M1 hattı).</span></div>
      <div class="row"><span class="yr">2018</span><span class="tx"><b>Samsun Projesi:</b> ray ve makas ısıtıcıları.</span></div>
      <div class="row"><span class="yr">2018-19</span><span class="tx"><b>Durmazlar Alibeyköy:</b> koltuk altı ısıtıcılar (Eminönü–Alibeyköy hattı) ve <b>Yazkar</b> klima batarya ısıtıcısı.</span></div>
      <div class="row"><span class="yr">2018-21</span><span class="tx"><b>İzmir Tramvay Projesi:</b> klima rezistans üniteleri.</span></div>
      <div class="row"><span class="yr">2019-23</span><span class="tx"><b>MERAK Brüksel Projesi:</b> ihracat: fanlı ısıtma üniteleri.</span></div>
      <div class="row"><span class="yr">2020</span><span class="tx"><b>TÜLOMSAŞ & TÜVASAŞ:</b> vagon mutfağı ısıtma plakaları (AC-DC), kOhm dirençler, çubuk rezistanslar.</span></div>
      <div class="row"><span class="yr">2021-26</span><span class="tx"><b>Romanya Projesi:</b> Bükreş tramvayları için koltuk düzenine özel elektrikli ısıtıcılar.</span></div>
      <div class="row"><span class="yr">2022-26</span><span class="tx"><b>Kayseri 5 UT:</b> Bozankaya üretimi; Prag–Belgrad–Kayseri hatları için ısıtıcılar.</span></div>
      <div class="row"><span class="yr">2023-26</span><span class="tx"><b>TÜRASAŞ EMU 225:</b> yolcu, vestibül ve makinist ısıtıcıları.</span></div>
      <div class="row"><span class="yr">2025-26</span><span class="tx"><b>İstanbul Metro:</b> klima ve koltuk altı ısıtıcıları.</span></div>
      <div class="row"><span class="yr">2026</span><span class="tx"><b>Samsun Projesi:</b> tramvay koltuk düzenine özel elektrikli ısıtıcılar.</span></div>
      <div class="row"><span class="yr">—</span><span class="tx"><b>Havalimanı Treni Projesi:</b> raylı araç ısıtıcı üniteleri.</span></div>
    </div>

    <div class="railcols">
      <div class="railbox reveal">
        <h3>Standart Testler</h3>
        <ul>
          <li>Güç testi ve izolasyon direnci testi</li>
          <li>Yüksek gerilimde kaçak akım (dielektrik) testi</li>
          <li>Şok ve vibrasyon testleri (demiryolu standartlarına uygun); yangına dayanım</li>
          <li>Boyut kontrolleri, çekme testi, topraklama direnci</li>
          <li>Yüzey/ısıtıcı sıcaklık ve IP seviye testleri; fan gürültü seviyesi (desibel) ölçümü</li>
        </ul>
      </div>
      <div class="railbox reveal" data-d="2">
        <h3>Malzeme Seçimi</h3>
        <ul>
          <li>Korozyona dayanıklı AISI 304 / AISI 316 sac parçalar</li>
          <li>Isıya dayanıklı cam elyaf izoleli, alev geciktirici 3GKW / 4GKW kablolar</li>
          <li>Yüksek kaliteli EBM fanlar</li>
          <li>Titreşime dayanıklı, çözülmez bağlantı ekipmanları</li>
          <li>Her ünitede çift kademeli termostat koruması</li>
        </ul>
      </div>
    </div>
  </div>
</section>
'''

sizes = []

# ---------------- 8 ISIŞAH alt-kategori sayfası ----------------
sizes.append(build_cat('sanayi-tipi-rezistans.html', 'isisah_rezistans',
    'Sanayi Tipi Rezistans Üreticisi Bursa | ISIŞAH',
    'ISIŞAH, Bursa DOSAB\'da flanşlı, daldırma, boru tipi ve proses rezistansları üretir. 44 yıllık tecrübe, ISO 9001:2015 kalite, yerli üretim.',
    'ISIŞAH ENDÜSTRİYEL · Ürün Gamı', 'Sanayi Tipi Rezistans',
    'Endüstriyel mutfaktan proses hatlarına: flanşlı, daldırma ve boru tipi rezistanslar — DOSAB Bursa\'da tasarım ve üretim.',
    'ISIŞAH, 1982\'den beri Bursa DOSAB\'da sanayi tipi rezistans üretir. Flanşlı, daldırma ve boru tipi ısıtıcı elemanlar; endüstriyel mutfak, fırın ve proses hatları için tasarlanır. Tüm gam ISO 9001:2015 kalite yönetim sistemi altında, yerli üretimle çıkar.',
    ISISAH, ['rezistans','izgara','fritoz','bulasik','makarna','defrost','firinrez','ocak','proses'],
    'isisah-endustriyel.html','ISIŞAH ENDÜSTRİYEL',
    'assets/products/rezistans.webp','Sanayi tipi flanş rezistansı — ISIŞAH'))

sizes.append(build_cat('endustriyel-mutfak-isiticilari.html', 'isisah_mutfak',
    'Endüstriyel Mutfak Isıtıcıları | ISIŞAH Bursa',
    'Izgara, fritöz, bulaşık makinesi ve makarna haşlama rezistansları. Endüstriyel mutfak ekipmanları için ISIŞAH ısıtıcı elemanları, Bursa DOSAB üretimi.',
    'ISIŞAH ENDÜSTRİYEL · Ürün Gamı', 'Endüstriyel Mutfak Isıtıcıları',
    'Konveksiyonel fırından fritöze: profesyonel mutfak ekipmanlarının ısıtıcı kalbi.',
    'Endüstriyel mutfak ekipmanı üreticileri için konveksiyon fırın, fritöz, bulaşık makinesi ve makarna haşlama üniteleri ısıtıcı elemanları. Hızlı ısınma ve homojen dağılım için tasarlanmış daldırma ve boyler tipi rezistanslar.',
    ISISAH, ['izgara','fritoz','bulasik','makarna'],
    'isisah-endustriyel.html','ISIŞAH ENDÜSTRİYEL',
    'assets/products/izgara.webp','Konveksiyonel fırın rezistansı — ISIŞAH'))

sizes.append(build_cat('beyaz-esya-isiticilari.html', 'isisah_beyaz',
    'Beyaz Eşya Isıtıcı Elemanları | ISIŞAH Bursa',
    'Kurutma makinesi, ocak, fırın ve disk ısıtıcıları. Arçelik ve Vestel için ISIŞAH beyaz eşya rezistansları, Bursa DOSAB üretimi.',
    'ISIŞAH ENDÜSTRİYEL · Ürün Gamı', 'Beyaz Eşya Isıtıcı Elemanları',
    'Arçelik ve Vestel kurutma makinesinden ev tipi fırına: beyaz eşya markalarının ısıtıcı tedarikçisi.',
    'Kurutma makinesi, elektrikli ocak, ev tipi fırın ve küçük ev aletleri için ısıtıcı elemanlar. Arçelik ve Vestel kurutma makineleri dahil, spiral, disk ve turbo rezistans formlarında üretim.',
    ISISAH, ['beyaz','defrost','ocak','disk','firinrez'],
    'isisah-endustriyel.html','ISIŞAH ENDÜSTRİYEL',
    'assets/products/beyaz.webp','Kurutma makinesi ısıtıcısı — ISIŞAH'))

sizes.append(build_cat('agir-sanayi-isiticilari.html', 'isisah_agir',
    'Ağır Sanayi Isıtıcı Üniteleri | ISIŞAH Bursa',
    'Endüstriyel fırın, proses ısıtıcı ünitesi ve mobil ısıtıcılar. Ağır sanayi için ISIŞAH ısıtma çözümleri, Bursa DOSAB tesisi.',
    'ISIŞAH ENDÜSTRİYEL · Ürün Gamı', 'Ağır Sanayi Isıtıcı Üniteleri',
    'Projeye özel endüstriyel fırından mobil ısıtıcıya: ağır sanayinin ısı ihtiyacı.',
    'Kontrol panelli sanayi tipi ısıl işlem fırınları, taşınabilir fanlı ısıtıcılar (Uğur Böceği serisi) ve flanşlı proses ısıtıcı üniteleri. Projeye özel kapasite ve gövde seçenekleriyle üretilir.',
    ISISAH, ['rezistans','firin','mobil','proses'],
    'isisah-endustriyel.html','ISIŞAH ENDÜSTRİYEL',
    'assets/products/firin.webp','Endüstriyel fırın — ISIŞAH'))

sizes.append(build_cat('endustriyel-isitma-klima-santrali.html', 'isisah_hvac',
    'Endüstriyel Isıtma & Klima Santrali Isıtıcısı | ISIŞAH',
    'Kanal tipi ısıtıcı, fan-coil ve klima santrali (AHU) ısıtıcı üniteleri. Endüstriyel ısıtma ve HVAC için ISIŞAH, Bursa DOSAB üretimi.',
    'ISIŞAH ENDÜSTRİYEL · Ürün Gamı', 'Endüstriyel Isıtma & Klima Santrali',
    'Santral, fan-coil ve kanal ısıtıcıları: HVAC sistemlerinin ısıtma katmanı.',
    'Havalandırma ve iklimlendirme sistemleri için kanatlı rezistanslı kanal ısıtıcıları, fan-coil ünitesi ısıtıcıları ve yüksek kapasiteli klima santrali (AHU) ısıtıcı grupları. Dikdörtgen, yuvarlak ve silindirik gövde seçenekleri.',
    ISISAH, ['kanal','fincoil','panel','duct'],
    'isisah-endustriyel.html','ISIŞAH ENDÜSTRİYEL',
    'assets/products/kanal.webp','Kanal tipi ısıtıcı — ISIŞAH'))

sizes.append(build_cat('demiryolu-isiticilari.html', 'isisah_rayli',
    'Demiryolu Isıtıcıları ve Ray Makas Isıtıcısı | ISIŞAH',
    'TÜVASAŞ ve TÜRASAŞ tedarikçisi ISIŞAH: demiryolu araç ısıtıcısı, ray & makas ısıtıcısı, personel kabini ısıtıcıları. 80\'lerden beri üretimde.',
    'ISIŞAH · DEMİRYOLU', 'Demiryolu Isıtıcıları',
    "80'lerin sonundan beri raylı sisteme: araç, makas ve personel kabini ısıtıcıları.",
    "1980'lerin sonundan beri demiryolu sanayine tedarik: TÜVASAŞ ve TÜRASAŞ için raylı araç ısıtıcıları, metro/tramvay klima ısıtıcıları, ray & makas donma önleyici ısıtıcılar ve personel kabini ısıtıcıları. Şok/vibrasyon testli, yüksek gerilim izolasyonlu üretim.",
    ISISAH, ['tren','railcar','makas','personel'],
    'isisah-endustriyel.html','ISIŞAH ENDÜSTRİYEL',
    'assets/products/tren.webp','Demiryolu iklimlendirme çözümü — ISIŞAH',
    extra_body=DEMIRYOLU_EXTRA))

sizes.append(build_cat('savunma-sanayi-isitma-sistemleri.html', 'isisah_savunma',
    'Savunma Sanayi Isıtma Sistemleri | ISIŞAH Bursa',
    'TCG Anadolu ve MİLGEM sınıfı gemiler için ısıtma ve iklimlendirme çözümleri. ISIŞAH savunma sanayi blast heater ve konvektör ısıtıcı, Bursa.',
    'ISIŞAH · SAVUNMA', 'Savunma Sanayi Isıtma Sistemleri',
    'TCG Anadolu ve MİLGEM sınıfı platformlar için gemi ısıtma ve iklimlendirme.',
    'Askeri gemi ve savunma platformları için ısıtma ve iklimlendirme çözümleri: TCG Anadolu (L400) dahil amfibi hücum gemileri, MİLGEM sınıfı fanlı blast heater ve NBC uyumlu klima santrali entegrasyonu, gemi tipi baseboard konvektör ısıtıcılar.',
    ISISAH, ['gemi','blast','baseboard'],
    'isisah-endustriyel.html','ISIŞAH ENDÜSTRİYEL',
    'assets/products/gemi.webp','Askeri gemi iklimlendirme çözümü — ISIŞAH'))

sizes.append(build_cat('boya-kurutma-firini.html', 'isisah_otomotiv',
    'Boya Kurutma Fırını (Infrared) | BOYKUR — ISIŞAH',
    'BOYKUR: Tofaş Ar-Ge işbirliğiyle geliştirilen infrared, bilgisayar kontrollü mobil oto boya kurutma fırını. ISIŞAH otomotiv üretimi, Bursa.',
    'ISIŞAH · OTOMOTİV', 'Boya Kurutma Fırını — BOYKUR',
    'Tofaş Ar-Ge işbirliğiyle geliştirilen infrared oto boya kurutma.',
    'BOYKUR, Türkiye\'de ilk yerli imalat patentli infrared teknolojili oto boya kurutma ünitesidir — Tofaş Ar-Ge işbirliğiyle geliştirilmiştir. Bilgisayar kontrollü, mobil gövdeli sistem oto servis ve karoser atölyeleri için tasarlanmıştır.',
    ISISAH, ['boykur'],
    'isisah-endustriyel.html','ISIŞAH ENDÜSTRİYEL',
    'assets/products/boykur.webp','BOYKUR infrared boya kurutma — ISIŞAH'))

# ---------------- SALMEX (marka = kategori, tek gam) ----------------
sizes.append(build_cat('salmex-isi-esanjoru.html', 'salmex',
    'Isı Eşanjörü ve Kombi Eşanjörü Üreticisi | SALMEX',
    'SALMEX: yoğuşmalı kombi eşanjörü, kazan tipi eşanjör, helisel ve spiral serpantin. Paslanmaz çelik ısı eşanjörü üretimi, Bursa DOSAB.',
    'SALMEX · Isı Eşanjörleri', 'Isı Eşanjörü Üreticisi — SALMEX',
    'Yoğuşmalı kombi eşanjöründen kazan tipi eşanjöre: paslanmaz çelik ısı transferi.',
    'SALMEX, kombi ve kazan üreticileri için paslanmaz çelik ısı eşanjörleri üretir: yoğuşmalı kombi eşanjörü, elektrikli kombi eşanjörü, kanatlı ana eşanjör, kazan tipi yoğuşmalı eşanjör, helisel boru eşanjörü ve premix yoğuşmalı eşanjör hücresi. Alüminyum döküm ve paslanmaz gövde seçenekleriyle komple ünite olarak da tedarik edilir.',
    SALMEX, ['salmex','condhex','ehex','bitermik','kazan','boyler','helis','serpantin','hucre','emodul'],
    'index.html#markalar','SALMEX',
    'assets/img/salmex-hat.webp','SALMEX robotlu eşanjör üretim hattı'))

# ---------------- BORŞAH (marka = kategori, tek gam) ----------------
sizes.append(build_cat('paslanmaz-celik-boru-ureticisi.html', 'borsah',
    'Paslanmaz Çelik Boru Üreticisi Bursa | BORŞAH',
    'BORŞAH: Ø6–42 mm dikişli paslanmaz boru, oval ve tavlı kangal boru. Rezistans imalatı ve sanayi için paslanmaz çelik boru üretimi, Bursa DOSAB.',
    'BORŞAH BORU · Paslanmaz Çelik Boru', 'Paslanmaz Çelik Boru Üreticisi — BORŞAH',
    'Ø6–42 mm dikişli, oval ve kangal paslanmaz boru — rezistans imalatından sanayiye.',
    'BORŞAH BORU, Ø6–42 mm çap aralığında dikişli paslanmaz çelik boru üretir: standart borular 70–300 bar test basıncında 9 kalite kontrol adımından geçer; tavlı ve kangal borular 100–400 m kangal halinde, 100 bar test ile tedarik edilir. Oval kesitli profiller rezistans imalatı ve mobilya sektörü için üretilir.',
    BORSAH, ['boru','oval','kangal'],
    'index.html#markalar','BORŞAH BORU',
    'assets/products/boru.webp','Paslanmaz çelik boru — BORŞAH'))

# ---------------- ISIŞAH ENDÜSTRİYEL marka hub'ı (8 alt-kategoriyi bağlar) ----------------
sizes.append(build_hub('isisah-endustriyel.html',
    'ISIŞAH ENDÜSTRİYEL Rezistans ve Isıtma Sistemleri',
    'ISIŞAH ENDÜSTRİYEL: 8 ürün gamında sanayi tipi rezistans, endüstriyel mutfak, beyaz eşya, HVAC, demiryolu, savunma ve otomotiv ısıtıcıları.',
    'ISIŞAH GROUP · Marka', 'ISIŞAH ENDÜSTRİYEL',
    '8 ürün gamı, tek marka: mutfaktan savunma sanayine ısıtma elemanları.',
    'ISIŞAH ENDÜSTRİYEL, 1982\'den beri Bursa DOSAB\'da sanayi tipi rezistans ve ısıtma sistemleri üretir. Ürün gamı endüstriyel mutfak, beyaz eşya, ağır sanayi, iklimlendirme (HVAC), demiryolu, savunma sanayi ve otomotiv sektörlerine uzanır — sekiz farklı uygulama alanında, tek marka altında.',
    [('sanayi-tipi-rezistans.html','Sanayi Tipi Rezistans','Flanşlı, daldırma, boru tipi ve proses rezistansları'),
     ('endustriyel-mutfak-isiticilari.html','Endüstriyel Mutfak','Izgara, fritöz, bulaşık ve haşlama rezistansları'),
     ('beyaz-esya-isiticilari.html','Beyaz Eşya & Ev Aletleri','Kurutma, defrost, ocak, fırın ve disk ısıtıcıları'),
     ('agir-sanayi-isiticilari.html','Ağır Sanayi','Proses üniteleri, endüstriyel fırın ve mobil ısıtıcılar'),
     ('endustriyel-isitma-klima-santrali.html','İklimlendirme (HVAC)','Kanal tipi, fan-coil ve klima santrali ısıtıcıları'),
     ('demiryolu-isiticilari.html','Raylı Sistemler','Araç, makas ve personel ısıtıcıları'),
     ('savunma-sanayi-isitma-sistemleri.html','Savunma Sanayi','Askeri gemi ısıtma ve iklimlendirme'),
     ('boya-kurutma-firini.html','Otomotiv — BOYKUR','İnfrared oto boya kurutma, Tofaş Ar-Ge')],
    'isisah','assets/catalog/logo-isisah.webp',
    'assets/img/bina-gece-3marka.webp','ISIŞAH GROUP merkez binası — DOSAB Bursa'))

for t, d in sizes:
    print(f'title={t}kr desc={d}kr' + ('  !! title uzun' if t>62 else '') + ('  !! desc uzun' if d>158 else ''))
print(len(sizes), 'sayfa üretildi')
