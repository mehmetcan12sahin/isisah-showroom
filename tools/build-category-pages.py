#!/usr/bin/env python3
# 10 kategori (gam) sayfası + 3 marka hub sayfası — index.html'in stil/header/footer'ından (tools/pagegen.py).
# İçerik urunler.html'deki ISISAH_LIST/SALMEX_LIST/BORSAH_LIST metinlerinin AYNISI (fabrikasyon yok).
# Ürün metni değişince önce urunler.html'i güncelle, bu dosyadaki mirror'ı da elle senkron et.
# Çalıştır: python3 tools/build-category-pages.py  (repo kökünden veya tools/ içinden)
import pathlib
from pagegen import ROOT, page, ORG

# ---------------- ürün mirror'ı (urunler.html ISISAH_LIST/SALMEX_LIST/BORSAH_LIST ile birebir) ----------------
ISISAH = {
 'rezistans':('Özel Tip Flanş Rezistansları','Daldırma ve boru tipi ısıtıcı elemanlar; sanayi ve proses uygulamaları için.',['Daldırma Tip','Boru Tip','Yerli Üretim']),
 'izgara':('Konveksiyonel Fırın Rezistansları','Konveksiyonel fırınlar için dairesel ısıtıcı elemanlar.',['Konveksiyon','Fırın','Paslanmaz']),
 'fritoz':('Fritöz Rezistansları (Yassı Rezistans)','Endüstriyel fritözler için daldırma tip ısıtıcı raflar; hızlı ve homojen ısıtma.',['Fritöz','Daldırma Tip','Hızlı Isıtma']),
 'bulasik':('Bulaşık Makinesi Rezistansları','Sanayi tipi bulaşık makineleri için boyler ve tank ısıtıcı elemanları.',['Boyler Tip','Tank Isıtıcı','Sanayi Tipi']),
 'makarna':('Makarna Haşlama Rezistansları (Yassı Rezistans)','Makarna haşlama üniteleri için daldırma tip ısıtıcı elemanlar.',['Haşlama','Daldırma Tip','Mutfak']),
 'beyaz':('Arçelik & Vestel Kurutma Makinesi Isıtıcıları','Arçelik ve Vestel kurutma makineleri için ısıtıcı üniteler.',['Arçelik','Vestel','Kurutma']),
 'defrost':('Defrost Rezistansları','Soğutma sistemleri için defrost elemanları; Ø6,5–11,2 mm, yüksek sıcaklığa dayanıklı.',['Ø6,5–11,2 mm','Yüksek Sıcaklık','Paslanmaz']),
 'firin':('Endüstriyel Fırın','Kontrol panelli sanayi tipi ısıl işlem ve kurutma fırınları; projeye özel.',['PLC Kontrol','Isıl İşlem','Projeye Özel']),
 'kanal':('Kanal Tipi Isıtıcı','Kanatlı rezistanslı santral, dikdörtgen ve yuvarlak kanal ısıtıcıları.',['Santral','Dikdörtgen','Yuvarlak']),
 'mobil':('Mobil Elektrikli Isıtıcı','Uğur Böceği serisi taşınabilir fanlı ısıtıcılar; atölye ve saha için.',['Taşınabilir','Fanlı','3 Boy']),
 'fincoil':('Fan-Coil & Ortam Isıtıcısı','Fan-coil üniteleri ve ortam ısıtması için dik finli paslanmaz ısıtıcılar.',['FCU','Ortam','Finli']),
 'panel':('Klima Santrali (AHU) Isıtıcısı','Klima santralleri için yüksek kapasiteli paslanmaz ısıtıcı üniteler.',['AHU','Yüksek Kapasite','Paslanmaz']),
 'duct':('Silindirik Kanal Fan Isıtıcısı','Havalandırma kanalları için fanlı silindirik paslanmaz ısıtıcı.',['Kanal','Fanlı','Kompakt']),
 'boykur':('BOYKUR Boya Kurutma','Infrared, bilgisayar kontrollü mobil oto boya kurutma. Tofaş Ar-Ge projesi.',['Infrared','Bilgisayar Kontrollü','Tofaş Ar-Ge']),
 'tren':('Demiryolu İklimlendirme Çözümleri',"80'lerin sonundan beri demiryolu sanayine: klima ısıtıcıları, yolcu/koltuk altı ve makinist ısıtıcıları, ray & makas ısıtıcıları.",['TÜVASAŞ · TÜRASAŞ','Metro & Tramvay','Yüksek Gerilim İzolasyonu']),
 'railcar':('Demiryolu Araç Isıtıcısı','Raylı araçlar için paslanmaz ısıtıcı üniteler; şok ve vibrasyon testli, yüksek gerilim izolasyonu.',['Raylı Araç','Şok & Vibrasyon','Paslanmaz']),
 'gemi':('Askeri Gemi İklimlendirme Çözümleri','TCG Anadolu (L400) dahil amfibi hücum gemileri ve MİLGEM sınıfı platformlar için ısıtma ve iklimlendirme çözümleri.',['TCG Anadolu','MİLGEM','Savunma Sanayi']),
 'blast':('Savunma Tipi Blast Heater','MİLGEM sınıfı gemiler ve savunma platformları için fanlı blast ısıtıcı; NBC uyumlu klima santrali entegrasyonu.',['MİLGEM','Fanlı','Savunma Sanayi']),
 'baseboard':('Baseboard Konvektör Isıtıcı','Gemi ve savunma platformları için delikli kasalı süpürgelik tipi konvektör üniteler.',['Gemi Tipi','Konvektör','Paslanmaz']),
 'ocak':('Ocak Rezistansları (Spiral)','Elektrikli ocaklar için spiral boru rezistanslar; ev tipi ve sanayi tipi formlarda.',['Spiral','Ocak','Boru Tip']),
 'disk':('Kahve & Çaydanlık Isıtıcıları','Kahve makinesi, çaydanlık ve bulaşık makineleri için paslanmaz disk ısıtıcılar.',['Disk Tip','Paslanmaz','Ev Aletleri']),
 'firinrez':('Fırın Rezistansları','Ev tipi fırınlar için alt-üst ve turbo rezistanslar; farklı form ve güçlerde.',['Fırın','Alt-Üst','Turbo']),
 'makas':('Ray & Makas Isıtıcıları','Karlı ve düşük sıcaklıkta makasların donmasını önler; olası kazaların önüne geçer. 1000 W / 230 V.',['1000W / 230V','Makas','Dona Karşı']),
 'personel':('Görevli Personel Isıtıcıları','Raylı araç personel kabinleri için finli paslanmaz ısıtıcı üniteler.',['Finli','Paslanmaz','TÜVASAŞ']),
 'proses':('Proses Isıtıcı Ünitesi','Endüstriyel proses hatları için flanşlı, kanal gövdeli ısıtıcı üniteler.',['Proses','Flanşlı','Yüksek Kapasite']),
}
SALMEX = {
 'salmex':('Yoğuşmalı Isı Eşanjörü','Paslanmaz çelik sarmal eşanjör borusu; yüksek verimli, farklı kapasitelerde yoğuşmalı tasarım.',['Paslanmaz Çelik','Yüksek Verim','Değiştirilebilir']),
 'condhex':('Yoğuşmalı Kombi Eşanjörü','Duvar tipi yoğuşmalı kombiler için alüminyum döküm eşanjör hücresi; pompa grubu ve gaz valfiyle komple ünite.',['Yoğuşmalı','Alüminyum Döküm','CondHex']),
 'ehex':('Elektrikli Kombi Eşanjörü','Elektrikli kombiler için eşanjör ünitesi; sirkülasyon pompası ve kontrol donanımıyla komple çözüm.',['Elektrikli','E-Hex','Komple Ünite']),
 'bitermik':('Kanatlı Kombi Ana Eşanjörü','Konvansiyonel kombiler için kanatlı borulu ana eşanjör blokları; kompakt ve yüksek ısı transferi.',['Kanatlı Boru','Konvansiyonel','Kompakt']),
 'kazan':('Kazan Tipi Yoğuşmalı Eşanjör','Yüksek kapasiteli kazanlar için paslanmaz gövdeli, alüminyum döküm flanşlı yoğuşmalı eşanjör.',['Kazan Tipi','Yüksek Kapasite','Paslanmaz']),
 'boyler':('Elektrikli Isıtıcı Ünitesi','Silindirik paslanmaz gövdeli elektrikli ısıtıcı; flanşlı rezistans grubuyla kombi ve kazan sistemleri için.',['Elektrikli','Paslanmaz','Flanşlı']),
 'helis':('Helisel Boru Eşanjörü','Paslanmaz borudan helisel sarım eşanjör; kompakt hacimde yüksek ısı transfer yüzeyi.',['Helisel Sarım','Paslanmaz Boru','Kompakt']),
 'serpantin':('Spiral Serpantin','Yassı spiral sarımlı paslanmaz serpantin; kazan ve boyler uygulamaları için.',['Spiral Sarım','Serpantin','Paslanmaz']),
 'hucre':('Premix Yoğuşmalı Eşanjör Hücresi','Kompozit gövdeli, alüminyum brülör kapaklı premix yoğuşmalı eşanjör hücresi; ateşleme elektrotu montajlı.',['Premix','Yoğuşmalı','Kompozit Gövde']),
 'emodul':('Elektrikli Isıtma Modülü','Paslanmaz plakalı gövde, kırmızı/mavi döküm kolektörlü kompakt elektrikli ısıtma modülü.',['Elektrikli','Plakalı','Kompakt']),
}
BORSAH = {
 'boru':('Paslanmaz Borular','Dikişli paslanmaz boru; Ø6–42 mm çap, 0,35–2 mm et kalınlığı, 70–300 bar test, 9 kalite kontrolü.',['Ø6–42 mm','0,35–2 mm','TIG Kaynak']),
 'oval':('Oval Borular','Rezistans imalatı, mobilya ve sanayi için oval kesitli paslanmaz profiller.',['Oval Kesit','Rezistans İmalatı','Profil']),
 'kangal':('Tavlı & Kangal Borular','Ø6–42 mm aralığında tavlı ve kangal boru; 100–400 m kangal, 100 bar test.',['Ø6–42 mm','100–400 m','Tavlı & Kangal']),
}

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

def collection_ld(name, url, desc, items):
    li = ','.join(f'{{"@type":"Product","position":{i+1},"name":"{h}","description":"{p}","brand":{{"@type":"Brand","name":"ISIŞAH GROUP"}}}}' for i,(h,p,_) in enumerate(items))
    return ('{"@context":"https://schema.org","@type":"CollectionPage","name":"'+name+'","url":"'+url+'","description":"'+desc+'",'
            '"isPartOf":{"@type":"WebSite","name":"ISIŞAH GROUP","url":"https://isisah.com.tr/"},'
            '"mainEntity":{"@type":"ItemList","itemListElement":['+li+']}}')

KATGRID_CSS = '''
  .katgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:10px}
  .katcard{border:1px solid rgba(255,255,255,.07);border-radius:16px;padding:24px;background:linear-gradient(165deg,rgba(16,16,24,.9),rgba(4,4,8,.95))}
  .katcard h3{font-size:1.08rem;margin:0}
  .katcard p{color:var(--steel);font-size:.92rem;margin-top:10px;line-height:1.55}
  .katcard .chips{display:flex;flex-wrap:wrap;gap:8px;margin-top:14px}
  .katcard .chips span{font-family:var(--tech);font-size:.66rem;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);border:1px solid var(--line);border-radius:40px;padding:5px 10px}
  .hubgrid{display:grid;grid-template-columns:repeat(2,1fr);gap:16px;margin-top:10px}
  .hubcard{display:flex;flex-direction:column;gap:8px;border:1px solid rgba(255,255,255,.07);border-radius:16px;padding:22px;background:linear-gradient(165deg,rgba(16,16,24,.9),rgba(4,4,8,.95));transition:border-color 200ms}
  .hubcard:hover{border-color:var(--vio1)}
  .hubcard b{font-size:1rem}
  .hubcard span{color:var(--muted);font-size:.86rem}
  @media(max-width:900px){.katgrid{grid-template-columns:1fr 1fr}.hubgrid{grid-template-columns:1fr}}
  @media(max-width:640px){.katgrid{grid-template-columns:1fr}}
'''

def cat_body(name, holkey, brandhub, brandhubname, intro_p, src, keys, extra_cta=''):
    return f'''
<style>{KATGRID_CSS}</style>
<section class="pad" style="padding-top:30px">
  <div class="wrap prose" style="max-width:900px">
    <p>{intro_p}</p>
    <div class="pgcta">
      <a class="btn" href="urunler.html#hol={holkey}">3B Showroom'da incele <span>→</span></a>
      <a class="btn ghost" href="tel:+902242610527">Ara</a>
      <a class="btn ghost" href="mailto:info@isisah.com.tr?subject=Teklif%20Talebi">Teklif İste</a>
    </div>
  </div>
</section>
<section class="pad" style="padding-top:0">
  <div class="wrap">
    <div class="sec-head reveal"><h2>Ürün gamı.</h2><p>{len(keys)} ürün — tam teknik detay ve 3B görünüm için showroom'a geçin.</p></div>
    {cards(src, keys)}
  </div>
</section>
<section class="pad" style="padding-top:0">
  <div class="wrap">
    <div class="pgcta reveal">
      <a class="btn ghost" href="{brandhub}">{brandhubname} markasının tamamı <span>→</span></a>
      <a class="btn ghost" href="hakkimizda.html">Hakkımızda</a>
      <a class="btn ghost" href="index.html#iletisim">İletişim</a>
    </div>
  </div>
</section>
'''

def build_cat(slug, holkey, title, desc, kick, h1, lead, intro_p, src, keys, brandhub, brandhubname, vis_img, vis_alt):
    url = f'https://isisah.com.tr/{slug}'
    items = [src[k] for k in keys]
    ld = collection_ld(h1.replace('<br>',' '), url, desc, items) + breadcrumb_ld(h1.replace('<br>',' '), url)
    body = cat_body(h1, holkey, brandhub, brandhubname, intro_p, src, keys)
    vis = f'<img src="{vis_img}" alt="{vis_alt}" loading="eager" width="1200" height="800"><span class="tag">{brandhubname}</span>'
    (ROOT/slug).write_text(page(slug, title, desc, kick, h1, lead, body, ld, vis), encoding='utf-8')
    return len(title), len(desc)

def build_hub(slug, title, desc, kick, h1, lead, intro_p, spokes, doorkey, logo, vis_img, vis_alt):
    url = f'https://isisah.com.tr/{slug}'
    cardsHtml = ''.join(f'<a class="hubcard reveal" href="{s[0]}"><b>{s[1]}</b><span>{s[2]}</span></a>' for s in spokes)
    body = f'''
<style>{KATGRID_CSS}</style>
<section class="pad" style="padding-top:30px">
  <div class="wrap prose" style="max-width:900px">
    <p>{intro_p}</p>
    <div class="pgcta">
      <a class="btn" href="urunler.html#marka={doorkey}">3B Showroom'da marka kapısını aç <span>→</span></a>
      <a class="btn ghost" href="tel:+902242610527">Ara</a>
      <a class="btn ghost" href="mailto:info@isisah.com.tr?subject=Teklif%20Talebi">Teklif İste</a>
    </div>
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
    ld = ('{"@context":"https://schema.org","@type":"CollectionPage","name":"'+h1+'","url":"'+url+'","description":"'+desc+'",'
          '"isPartOf":{"@type":"WebSite","name":"ISIŞAH GROUP","url":"https://isisah.com.tr/"}}') + breadcrumb_ld(h1, url)
    vis = f'<img src="{vis_img}" alt="{vis_alt}" loading="eager" width="1200" height="800"><span class="tag">{h1}</span>'
    (ROOT/slug).write_text(page(slug, title, desc, kick, h1, lead, body, ld, vis), encoding='utf-8')
    return len(title), len(desc)

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
    'assets/products/tren.webp','Demiryolu iklimlendirme çözümü — ISIŞAH'))

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
