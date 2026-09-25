#!/usr/bin/env python3
# TEK KAYNAK: assets/data/products.json. Bu script urunler.html icindeki 5 marker blogunu
# (3x @products:count, @jsonld, @katalog, @products) bu JSON'dan uretir:
#   - JS urun dizileri (ISISAH_LIST / SALMEX_LIST / BORSAH_LIST)
#   - JSON-LD ItemList (numberOfItems + 38 Product ogesi)
#   - statik katalog <details id="katalog"> metin listesi
#   - meta description / og:description / twitter:description icindeki urun sayisi
# Marker disindaki hicbir satira dokunmaz. Idempotent: iki kez calistirmak fark uretmez.
# Kullanim: python3 tools/build-products.py
# Urun eklemek/degistirmek icin: assets/data/products.json'u duzenleyip bunu, ardindan
# tools/build-category-pages.py ve tools/build-teklif.py'yi calistirin
# (bkz. .claude/skills/isisah-urun-ekle/SKILL.md).
import json
import re
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / 'assets/data/products.json'
HTML_PATH = ROOT / 'urunler.html'

REQUIRED_FIELDS = ('img', 'brand', 'tag', 'h', 'en', 'p', 'chips')
BRAND_ARR_NAME = {'isisah': 'ISISAH_LIST', 'salmex': 'SALMEX_LIST', 'borsah': 'BORSAH_LIST'}
BRAND_ORDER = ('isisah', 'salmex', 'borsah')
# JSON-LD "brand" + katalog <h3> her zaman GERÇEK marka adını kullanır (3 marka: isisah/salmex/borsah).
# Not: bazı ISIŞAH ürünlerinin urunler.html'deki UI "tag" alanı daha dar bir alt-etiket tasir
# (ör. boykur -> 'ISIŞAH · BOYKUR', tren/railcar -> 'ISIŞAH · DEMİRYOLU') — bu sadece showroom
# rafındaki rozet metnidir, schema.org Brand adi degildir; JSON-LD/katalog icin kullanilmaz.
BRAND_DISPLAY_NAME = {'isisah': 'ISIŞAH ENDÜSTRİYEL', 'salmex': 'SALMEX', 'borsah': 'BORŞAH BORU'}


def load_products():
    if not DATA_PATH.exists():
        sys.exit(f'HATA: {DATA_PATH} bulunamadi.')
    data = json.loads(DATA_PATH.read_text(encoding='utf-8'))
    products = data.get('products')
    if not isinstance(products, list) or not products:
        sys.exit('HATA: products.json icinde "products" listesi bos veya eksik.')
    seen_imgs = set()
    for p in products:
        for k in REQUIRED_FIELDS:
            if k not in p:
                sys.exit(f'HATA: products.json — img={p.get("img","?")} alaninda "{k}" eksik.')
        if p['brand'] not in BRAND_ORDER:
            sys.exit(f'HATA: products.json — img={p["img"]} icin gecersiz brand "{p["brand"]}".')
        if p['img'] in seen_imgs:
            sys.exit(f'HATA: products.json — tekrarlanan img slug "{p["img"]}".')
        seen_imgs.add(p['img'])
    return products


# ---------- JS dizi uretimi ----------

def js_str(s):
    # Mevcut kural (urunler.html): varsayilan tek tirnak; icinde ' varsa cift tirnak (bkz. 'tren').
    if "'" in s:
        return '"' + s.replace('\\', '\\\\').replace('"', '\\"') + '"'
    return "'" + s.replace('\\', '\\\\') + "'"


def js_chip_list(chips):
    return '[' + ','.join(js_str(c) for c in chips) + ']'


def build_list_js(name, products):
    lines = [f'const {name}=[']
    for p in products:
        logo = 'logo-' + p['brand']
        lines.append(
            f"  {{img:'{p['img']}',logo:'{logo}',tag:{js_str(p['tag'])},"
            f"h:{js_str(p['h'])},en:{js_str(p['en'])},"
        )
        lines.append(f"   p:{js_str(p['p'])},chips:{js_chip_list(p['chips'])}}},")
    lines.append('];')
    return '\n'.join(lines)


PRODUCTS_DOC_COMMENT = (
    '/* assets/data/products.json → tools/build-products.py ile üretilir '
    '(tek kaynak, bkz. .claude/skills/isisah-urun-ekle/SKILL.md). '
    'Bu blok içinde elle değişiklik yapmayın. */'
)


def build_products_block(products):
    by_brand = {b: [] for b in BRAND_ORDER}
    for p in products:
        by_brand[p['brand']].append(p)
    parts = [PRODUCTS_DOC_COMMENT]
    for brand in BRAND_ORDER:
        parts.append(build_list_js(BRAND_ARR_NAME[brand], by_brand[brand]))
    return '\n'.join(parts)


# ---------- JSON-LD uretimi ----------

def build_jsonld_obj(products):
    items = []
    for i, p in enumerate(products, start=1):
        items.append({
            '@type': 'ListItem',
            'position': i,
            'item': {
                '@type': 'Product',
                'name': p['h'],
                'description': p['p'],
                'image': f"https://isisah.com.tr/showroom/assets/products/{p['img']}.webp",
                'brand': {'@type': 'Brand', 'name': BRAND_DISPLAY_NAME[p['brand']]},
                'manufacturer': {'@type': 'Organization', 'name': 'ISIŞAH GROUP'},
                'url': 'https://isisah.com.tr/showroom/urunler.html',
            },
        })
    return {
        '@context': 'https://schema.org',
        '@type': 'ItemList',
        'name': 'ISIŞAH GROUP Ürünleri',
        'numberOfItems': len(products),
        'itemListElement': items,
    }


JSONLD_DOC_COMMENT_TMPL = (
    '<!-- ÜRÜN SAYISI ({n}): assets/data/products.json → tools/build-products.py ile üretilir; '
    'meta description/katalog <summary> ile aynı kaynaktan (tek kaynak, bkz. '
    '.claude/skills/isisah-urun-ekle/SKILL.md). Elle değiştirmeyin. -->'
)


def build_jsonld_block(products):
    doc = JSONLD_DOC_COMMENT_TMPL.format(n=len(products))
    payload = json.dumps(build_jsonld_obj(products), ensure_ascii=False, separators=(',', ':'))
    script = f'<script type="application/ld+json">{payload}</script>'
    return doc + '\n' + script


# ---------- katalog <details> uretimi ----------

KATALOG_CAT_LINKS = (
    '<p class="kn">Kategori sayfaları: '
    '<a href="isisah-endustriyel.html">ISIŞAH ENDÜSTRİYEL</a> · '
    '<a href="sanayi-tipi-rezistans.html">Sanayi Tipi Rezistans</a> · '
    '<a href="endustriyel-mutfak-isiticilari.html">Endüstriyel Mutfak</a> · '
    '<a href="beyaz-esya-isiticilari.html">Beyaz Eşya</a> · '
    '<a href="agir-sanayi-isiticilari.html">Ağır Sanayi</a> · '
    '<a href="endustriyel-isitma-klima-santrali.html">Endüstriyel Isıtma &amp; HVAC</a> · '
    '<a href="demiryolu-isiticilari.html">Demiryolu</a> · '
    '<a href="savunma-sanayi-isitma-sistemleri.html">Savunma Sanayi</a> · '
    '<a href="boya-kurutma-firini.html">Boya Kurutma Fırını</a> · '
    '<a href="salmex-isi-esanjoru.html">SALMEX Isı Eşanjörü</a> · '
    '<a href="paslanmaz-celik-boru-ureticisi.html">Paslanmaz Çelik Boru</a></p>'
)

KATALOG_FOOTER = (
    '<p class="kn">Tüm ürünler için teklif: <a href="teklif.html">teklif formu</a> · '
    '<a href="mailto:info@isisah.com.tr">info@isisah.com.tr</a> · '
    '<a href="tel:+902242610527">+90 224 261 05 27</a> · '
    '<a href="fabrika.html">SALMEX fabrika turu →</a></p>'
)


def build_katalog_block(products):
    total = len(products)
    brands_present = []
    seen = set()
    for p in products:
        if p['brand'] not in seen:
            seen.add(p['brand'])
            brands_present.append(p['brand'])
    brand_count = len(brands_present)

    lines = []
    lines.append(
        f'<!-- ÜRÜN SAYISI ({total}): assets/data/products.json → tools/build-products.py '
        'ile üretilir (tek kaynak, bkz. .claude/skills/isisah-urun-ekle/SKILL.md). '
        'Elle değiştirmeyin. -->'
    )
    lines.append(f'<summary>Tüm ürünler — {brand_count} marka, {total} ürün (metin listesi)</summary>')
    lines.append('<h2>Tüm ürünler</h2>')
    lines.append(KATALOG_CAT_LINKS)
    for brand in brands_present:
        brand_products = [p for p in products if p['brand'] == brand]
        h3name = BRAND_DISPLAY_NAME[brand]
        lines.append(f'<h3>{h3name}</h3><ul>')
        for p in brand_products:
            lines.append(f"<li><b>{p['h']}</b> — {p['p']}</li>")
        lines.append('</ul>')
    lines.append(KATALOG_FOOTER)
    return '\n'.join('  ' + l for l in lines)


# ---------- meta sayim bloklari ----------

def fix_count_block(inner, total):
    inner = re.sub(r'(ÜRÜN SAYISI \()\d+(\))', lambda m: m.group(1) + str(total) + m.group(2), inner)
    inner = re.sub(r'\d+(?=\s*ürün)', str(total), inner, count=1)
    return inner


# ---------- marker degistirme yardimcisi ----------

def replace_marker_block(html, start_marker, end_marker, build_fn, products, expected=1):
    pattern = re.compile(re.escape(start_marker) + r'\n(.*?)\n' + re.escape(end_marker), re.S)
    matches = list(pattern.finditer(html))
    if len(matches) != expected:
        sys.exit(
            f'HATA: urunler.html icinde "{start_marker}" .. "{end_marker}" '
            f'bekleniyordu {expected}, bulundu {len(matches)}.'
        )

    def repl(m):
        return start_marker + '\n' + build_fn(products) + '\n' + end_marker

    return pattern.sub(repl, html)


def replace_count_blocks(html, total, expected=3):
    pattern = re.compile(r'<!-- @products:count:start -->\n(.*?)\n<!-- @products:count:end -->', re.S)
    matches = list(pattern.finditer(html))
    if len(matches) != expected:
        sys.exit(f'HATA: @products:count marker cifti {expected} bekleniyordu, bulundu {len(matches)}.')

    def repl(m):
        return '<!-- @products:count:start -->\n' + fix_count_block(m.group(1), total) + '\n<!-- @products:count:end -->'

    return pattern.sub(repl, html)


def main():
    products = load_products()
    total = len(products)
    html = HTML_PATH.read_text(encoding='utf-8')

    html = replace_marker_block(html, '<!-- @jsonld:start -->', '<!-- @jsonld:end -->', build_jsonld_block, products)
    html = replace_marker_block(html, '  <!-- @katalog:start -->', '  <!-- @katalog:end -->', build_katalog_block, products)
    html = replace_marker_block(html, '/* @products:start */', '/* @products:end */', build_products_block, products)
    html = replace_count_blocks(html, total)

    HTML_PATH.write_text(html, encoding='utf-8')
    print(f'urunler.html güncellendi: {total} ürün ({", ".join(BRAND_ORDER)}).')


if __name__ == '__main__':
    main()
