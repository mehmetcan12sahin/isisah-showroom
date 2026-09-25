#!/usr/bin/env python3
"""ISIŞAH statik site otomatik denetleyici — stdlib-only, ağ erişimi YOK, salt okur.

Depo kökünden çalıştırın: python3 tools/check-site.py [--json]
docs/, server/, vendor/ altındaki dosyalar atlanır.

Şiddet (severity) kuralı — brief'te açıkça "(warn)" diye işaretlenenler UYARI,
Offer/price/aggregateRating/review açıkça "ERROR" diye işaretli; kalan
işaretsiz kalemlerde şu tutarlı ayrım uygulanır:
  HATA  = ikili/kesin bir bozukluk (kırık link, eksik dosya, geçersiz JSON,
          sahte ticaret şeması, yanlış canonical/H1/noindex, eksik alt metni,
          ham "0…" sayaç, "gönderildi" gibi doğrulanmamış başarı metni).
  UYARI = yumuşak/kalite kuralı (karakter aralığı, eksik width/height, >200KB
          görsel, marka eşleşmesi, sitemap kapsaması, nav'da teklif linki,
          teklif.html haritası bulunamadığında doğrulanamayan değerler).
Bu ayrım docstring'de açık tutuluyor ki bir insan itiraz edip değiştirebilsin.

Çıkış kodu: 1 tane bile HATA varsa exit 1; sadece UYARI varsa exit 0.
"""
import argparse
import json
import os
import re
import sys
import time
import xml.etree.ElementTree as ET

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_ROOT = os.path.dirname(SCRIPT_DIR)
ROOT = os.getcwd() if os.path.isfile(os.path.join(os.getcwd(), "index.html")) else DEFAULT_ROOT

DOMAIN = "https://isisah.com.tr"
SKIP_DIRS = {"docs", "server", "vendor", ".git", "node_modules"}
ALLOWED_BRANDS = {"ISIŞAH ENDÜSTRİYEL", "SALMEX", "BORŞAH BORU"}
ALLOWED_MARKA_KEYS = {"isisah", "salmex", "borsah"}
SHOWROOM_PAGES = {"urunler.html", "fabrika.html"}

# Sayfa dosya adı -> tekil marka bağlamı (çok-markalı/lobi sayfaları burada YOK,
# çünkü onlarda "sayfa bağlamı" belirlenebilir değil — spec'in "where determinable"
# şartı gereği o sayfalar brand-context uyum kontrolünden hariç tutulur).
BRAND_CONTEXT = {
    "salmex-isi-esanjoru.html": "SALMEX",
    "paslanmaz-celik-boru-ureticisi.html": "BORŞAH BORU",
    "isisah-endustriyel.html": "ISIŞAH ENDÜSTRİYEL",
    "sanayi-tipi-rezistans.html": "ISIŞAH ENDÜSTRİYEL",
    "endustriyel-mutfak-isiticilari.html": "ISIŞAH ENDÜSTRİYEL",
    "beyaz-esya-isiticilari.html": "ISIŞAH ENDÜSTRİYEL",
    "agir-sanayi-isiticilari.html": "ISIŞAH ENDÜSTRİYEL",
    "endustriyel-isitma-klima-santrali.html": "ISIŞAH ENDÜSTRİYEL",
    "demiryolu-isiticilari.html": "ISIŞAH ENDÜSTRİYEL",
    "savunma-sanayi-isitma-sistemleri.html": "ISIŞAH ENDÜSTRİYEL",
    "boya-kurutma-firini.html": "ISIŞAH ENDÜSTRİYEL",
}

HATA, UYARI = "HATA", "UYARI"


# ---------------------------------------------------------------- yardımcılar
def find_html_files(root):
    out = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith(".")]
        for fn in filenames:
            if fn.lower().endswith(".html"):
                rel = os.path.relpath(os.path.join(dirpath, fn), root).replace(os.sep, "/")
                out.append(rel)
    return sorted(out)


def line_of(text, pos):
    return text.count("\n", 0, pos) + 1


def get_attr_line(text, pattern, flags=0):
    """(değer, satır) döner; yoksa (None, None)."""
    m = re.search(pattern, text, flags)
    if not m:
        return None, None
    return m.group(1), line_of(text, m.start())


def walk_json(node):
    if isinstance(node, dict):
        yield node
        for v in node.values():
            yield from walk_json(v)
    elif isinstance(node, list):
        for item in node:
            yield from walk_json(item)


def split_top_level_values(text):
    """Bitişik kök JSON değerlerini ('{...}{...}') ayrı parçalara böler."""
    text = text.strip()
    parts, depth, in_str, esc, start, started = [], 0, None, False, 0, False
    i, n = 0, len(text)
    while i < n:
        c = text[i]
        if in_str:
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif c == in_str:
                in_str = None
        else:
            if c in ("'", '"'):
                in_str = c
            elif c in "{[":
                depth += 1
                started = True
            elif c in "}]":
                depth -= 1
                if depth == 0 and started:
                    parts.append(text[start:i + 1])
                    j = i + 1
                    while j < n and text[j] in " \t\r\n,":
                        j += 1
                    start = j
                    i = j
                    started = False
                    continue
        i += 1
    if start < n and text[start:].strip():
        parts.append(text[start:].strip())
    return parts if parts else [text]


def extract_object_literal(js_text, var_name):
    """`const VAR = { ... };` bloğunun iç metnini (dış süslü parantezler hariç) döner."""
    m = re.search(rf"const\s+{re.escape(var_name)}\s*=\s*\{{", js_text)
    if not m:
        return None
    start = m.end() - 1
    depth, in_str, esc = 0, None, False
    i, n = start, len(js_text)
    while i < n:
        c = js_text[i]
        if in_str:
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif c == in_str:
                in_str = None
        else:
            if c in ("'", '"', "`"):
                in_str = c
            elif c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    return js_text[start + 1:i]
        i += 1
    return None


def top_level_keys(obj_inner):
    if obj_inner is None:
        return []
    keys, depth, in_str, esc = [], 0, None, False
    i, n, seg_start, segments = 0, len(obj_inner), 0, []
    while i < n:
        c = obj_inner[i]
        if in_str:
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif c == in_str:
                in_str = None
        else:
            if c in ("'", '"', "`"):
                in_str = c
            elif c in "{[(":
                depth += 1
            elif c in "}])":
                depth -= 1
            elif c == "," and depth == 0:
                segments.append(obj_inner[seg_start:i])
                seg_start = i + 1
        i += 1
    if obj_inner[seg_start:].strip():
        segments.append(obj_inner[seg_start:])
    for seg in segments:
        seg = seg.strip()
        km = re.match(r"""^(?:([A-Za-z_$][A-Za-z0-9_$]*)|'([^']*)'|"([^"]*)")\s*:""", seg)
        if km:
            keys.append(next(g for g in km.groups() if g is not None))
    return keys


def resolve_local_path(base_file, raw_value):
    """href/src değerini repo köküne göre gerçek bir dosya yoluna çevirir.
    Dönüş: (dosya_yolu_veya_None, atlanmalı_mı_bool). atlanmalı=True -> harici/şema/şablon,
    kontrol dışı (mailto/tel/http(s)/data/js şablonu/boş)."""
    v = raw_value.strip()
    if not v or v.startswith("#"):
        return None, True if not v else False
    low = v.lower()
    if low.startswith(("http://", "https://", "//", "mailto:", "tel:", "sms:",
                        "javascript:", "data:", "blob:", "ftp:")):
        return None, True
    if "${" in v:
        return None, True
    # ?query / #hash kırp
    v = v.split("#", 1)[0].split("?", 1)[0]
    if not v:
        return None, True
    if v.startswith("/showroom/"):
        rel = v[len("/showroom/"):]
    elif v == "/":
        rel = "index.html"
    elif v.startswith("/"):
        rel = v[1:]
    else:
        base_dir = os.path.dirname(base_file)
        rel = os.path.normpath(os.path.join(base_dir, v)).replace(os.sep, "/")
    if not rel or rel.endswith("/"):
        return None, True
    return rel, False


def resolve_isisah_absolute(url):
    """https://isisah.com.tr/... (showroom dahil) -> repo-relative yol. Eşleşmezse None."""
    if not url.startswith(DOMAIN):
        return None
    path = url[len(DOMAIN):]
    if path in ("", "/"):
        return "index.html"
    path = path.lstrip("/")
    if path.startswith("showroom/"):
        path = path[len("showroom/"):]
    return path.split("#", 1)[0].split("?", 1)[0]


class Findings:
    def __init__(self):
        self.items = []  # (file, line, severity, category, message)

    def add(self, file, line, severity, category, message):
        self.items.append((file, line or 0, severity, category, message))

    def by_file(self):
        groups = {}
        for f, line, sev, cat, msg in self.items:
            groups.setdefault(f, []).append((line, sev, cat, msg))
        for f in groups:
            groups[f].sort(key=lambda t: (t[0], t[1]))
        return groups

    def counts(self):
        e = sum(1 for i in self.items if i[2] == HATA)
        w = sum(1 for i in self.items if i[2] == UYARI)
        return e, w


# --------------------------------------------------------------- urunler.html verisi
def load_urunler_model(files_text):
    """urunler.html'den hol/marka/ürün anahtarlarını ve (varsa) teklif.html haritalarını çıkarır."""
    model = {"hol_keys": set(), "urun_slugs": set(), "marka_keys": set(ALLOWED_MARKA_KEYS)}
    src = files_text.get("urunler.html")
    if src:
        brands = extract_object_literal(src, "BRANDS")
        cats = extract_object_literal(src, "ISISAH_CATS")
        model["hol_keys"] = set(top_level_keys(brands)) | set(top_level_keys(cats))
        model["urun_slugs"] = set(re.findall(r"img:'([a-zA-Z0-9_-]+)'", src))
    model["index_ids"] = set()
    idx = files_text.get("index.html")
    if idx:
        model["index_ids"] = set(re.findall(r'\bid="([a-zA-Z][a-zA-Z0-9_-]*)"', idx))
    # teklif.html varsa gömülü URUN/KONU haritalarını oku (yoksa None -> "warn")
    model["urun_map"] = None
    model["konu_map"] = None
    teklif = files_text.get("teklif.html")
    if teklif:
        m = re.search(r"const\s+(\w*URUN\w*)\s*=", teklif, re.I)
        if m:
            model["urun_map"] = set(top_level_keys(extract_object_literal(teklif, m.group(1))))
        m = re.search(r"const\s+(\w*KONU\w*)\s*=", teklif, re.I)
        if m:
            model["konu_map"] = set(top_level_keys(extract_object_literal(teklif, m.group(1))))
    return model


# --------------------------------------------------------------------- per-file kontroller
IMG_TAG_RE = re.compile(r"<img\b([^>]*)>", re.I)
ATTR_RE = re.compile(r'\b([a-zA-Z-]+)\s*=\s*"([^"]*)"')
LINK_RE = re.compile(r'\b(?:href|src)\s*=\s*"([^"]*)"')
JSONLD_RE = re.compile(r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', re.S | re.I)


def check_jsonld(fname, text, F, agg_brand):
    for m in JSONLD_RE.finditer(text):
        block = m.group(1)
        line = line_of(text, m.start())
        parsed_objs = None
        try:
            data = json.loads(block)
            parsed_objs = data if isinstance(data, list) else [data]
        except json.JSONDecodeError as e:
            parts = split_top_level_values(block)
            if len(parts) > 1:
                sub, all_ok = [], True
                for p in parts:
                    try:
                        sub.append(json.loads(p))
                    except Exception:
                        all_ok = False
                if all_ok:
                    F.add(fname, line, HATA, "jsonld",
                          f"{len(parts)} adet bitişik kök JSON nesnesi array içine alınmamış "
                          f"(tarayıcıda JSON.parse patlar) — script içeriğini [obj1,obj2,...] yapın.")
                    parsed_objs = sub
                else:
                    F.add(fname, line, HATA, "jsonld", f"JSON-LD parse hatası: {e}")
            else:
                F.add(fname, line, HATA, "jsonld", f"JSON-LD parse hatası: {e}")

        if parsed_objs is None:
            # parse tamamen başarısız — ham metinde yasak ticaret anahtarlarını yine ara
            if re.search(r'"@type"\s*:\s*"(Offer|AggregateOffer)"|"(price|priceCurrency|offers|aggregateRating|reviews?)"\s*:', block):
                F.add(fname, line, HATA, "jsonld-commerce",
                      "JSON-LD parse edilemedi ama Offer/price/aggregateRating/review benzeri "
                      "anahtar(lar) ham metinde görünüyor — politika: sahte ticaret verisi yasak.")
            continue

        found_keys = set()
        product_count = 0
        for d in walk_json(parsed_objs):
            t = d.get("@type")
            types = t if isinstance(t, list) else [t]
            if any(x in ("Offer", "AggregateOffer") for x in types):
                found_keys.add("Offer/@type")
            for k in ("price", "priceCurrency", "offers", "aggregateRating", "review", "reviews"):
                if k in d:
                    found_keys.add(k)
            if "Product" in types:
                product_count += 1
                brand = d.get("brand")
                bname = brand.get("name") if isinstance(brand, dict) else (brand if isinstance(brand, str) else None)
                agg_brand.setdefault(fname, {"missing": 0, "invalid": {}, "mismatch": {}})
                if not bname:
                    agg_brand[fname]["missing"] += 1
                elif bname not in ALLOWED_BRANDS:
                    agg_brand[fname]["invalid"][bname] = agg_brand[fname]["invalid"].get(bname, 0) + 1
                else:
                    ctx = BRAND_CONTEXT.get(fname)
                    if ctx and bname != ctx:
                        key = (bname, ctx)
                        agg_brand[fname]["mismatch"][key] = agg_brand[fname]["mismatch"].get(key, 0) + 1
        if found_keys:
            F.add(fname, line, HATA, "jsonld-commerce",
                  "Sahte/ticari şema politikaya aykırı — bulunan anahtar(lar): " + ", ".join(sorted(found_keys)))


def flush_brand_findings(F, agg_brand):
    for fname, info in agg_brand.items():
        if info["missing"]:
            F.add(fname, None, UYARI, "brand",
                  f"Product.brand eksik — {info['missing']} üründe brand/name yok")
        for bname, cnt in info["invalid"].items():
            F.add(fname, None, UYARI, "brand",
                  f"Product.brand geçersiz değer: '{bname}' — {cnt} üründe "
                  f"(izinli: {', '.join(sorted(ALLOWED_BRANDS))})")
        for (bname, ctx), cnt in info["mismatch"].items():
            F.add(fname, None, UYARI, "brand",
                  f"Product.brand ('{bname}') sayfanın marka bağlamıyla ('{ctx}') uyuşmuyor — {cnt} üründe")


def check_meta(fname, text, F, titles, descs):
    h1s = list(re.finditer(r"<h1\b", text, re.I))
    if len(h1s) != 1:
        F.add(fname, line_of(text, h1s[0].start()) if h1s else None, HATA, "h1",
              f"tam olarak 1 <h1> olmalı, bulunan: {len(h1s)}")

    title, tline = get_attr_line(text, r"<title[^>]*>(.*?)</title>", re.S)
    if not title:
        F.add(fname, None, HATA, "title", "<title> etiketi yok")
    else:
        tl = len(title.strip())
        if not (30 <= tl <= 65):
            F.add(fname, tline, UYARI, "title", f"title uzunluğu {tl} karakter (önerilen 30-65)")
        titles.setdefault(title.strip(), []).append(fname)

    robots, rline = get_attr_line(text, r'<meta[^>]+name="robots"[^>]+content="([^"]*)"')
    noindex = bool(robots and "noindex" in robots.lower())

    desc, dline = get_attr_line(text, r'<meta[^>]+name="description"[^>]+content="([^"]*)"')
    if desc is None and noindex:
        pass  # noindex sayfa (404): description zorunlu değil
    elif desc is None:
        F.add(fname, None, HATA, "description", 'meta name="description" yok')
    else:
        dl = len(desc)
        if not (70 <= dl <= 160):
            F.add(fname, dline, UYARI, "description", f"description uzunluğu {dl} karakter (önerilen 70-160)")
        descs.setdefault(desc, []).append(fname)

    canon, cline = get_attr_line(text, r'<link[^>]+rel="canonical"[^>]+href="([^"]*)"')
    if not canon and noindex:
        pass  # noindex sayfa (404) kendini canonical göstermemeli
    elif not canon:
        F.add(fname, None, HATA, "canonical", "canonical link yok")
    else:
        if fname in SHOWROOM_PAGES:
            expected = f"{DOMAIN}/showroom/{fname}"
        elif fname == "index.html":
            expected = f"{DOMAIN}/"
        else:
            expected = f"{DOMAIN}/{fname}"
        if canon != expected:
            F.add(fname, cline, HATA, "canonical", f"canonical '{canon}' beklenen '{expected}' değil")

    if noindex and fname != "404.html":
        F.add(fname, rline, HATA, "noindex", f"beklenmeyen noindex: content=\"{robots}\"")

    og, ogline = get_attr_line(text, r'<meta[^>]+property="og:image"[^>]+content="([^"]*)"')
    if not og:
        F.add(fname, None, UYARI, "og-image", "og:image meta etiketi yok")
    else:
        rel = resolve_isisah_absolute(og)
        if rel is None:
            F.add(fname, ogline, UYARI, "og-image", f"og:image harici/host doğrulanamıyor: {og}")
        elif not os.path.isfile(os.path.join(ROOT, rel)):
            F.add(fname, ogline, HATA, "og-image", f"og:image dosyası yok: {og} -> {rel}")

    twimg, twline = get_attr_line(text, r'<meta[^>]+name="twitter:image"[^>]+content="([^"]*)"')
    if twimg:
        rel = resolve_isisah_absolute(twimg)
        if rel is not None and not os.path.isfile(os.path.join(ROOT, rel)):
            F.add(fname, twline, HATA, "og-image", f"twitter:image dosyası yok: {twimg} -> {rel}")


def check_images(fname, text, F):
    for m in IMG_TAG_RE.finditer(text):
        attrs_str = m.group(1)
        if not attrs_str.strip():
            # öznitelik taşımayan "<img>" gerçek bir markup değil, JS yorumu içinde
            # geçen bir söz olabilir (örn. "DOM logo <img>)." açıklaması) — atla.
            continue
        line = line_of(text, m.start())
        attrs = dict(ATTR_RE.findall(attrs_str))
        src = attrs.get("src")
        alt = attrs.get("alt")
        decorative = attrs.get("aria-hidden") == "true" or attrs.get("role") in ("presentation", "none")
        if alt is None:
            F.add(fname, line, HATA, "img-alt", f"<img> alt özniteliği yok (src={src})")
        elif alt == "" and not decorative:
            F.add(fname, line, UYARI, "img-alt",
                  f"boş alt yalnızca dekoratif görsellerde uygun — aria-hidden=\"true\" veya "
                  f"role=\"presentation\" ekleyin (src={src})")
        if "width" not in attrs or "height" not in attrs:
            F.add(fname, line, UYARI, "img-dims", f"width/height eksik (src={src})")
        if src is not None:
            rel, skip = resolve_local_path(fname, src)
            if not skip:
                if rel is None:
                    continue
                full = os.path.join(ROOT, rel)
                if not os.path.isfile(full):
                    F.add(fname, line, HATA, "img-missing", f"görsel bulunamadı: {src} -> {rel}")
                else:
                    size = os.path.getsize(full)
                    if size > 200 * 1024:
                        F.add(fname, line, UYARI, "img-size",
                              f"görsel > 200KB: {src} ({size // 1024} KB)")


DATA_COUNT_RE = re.compile(
    r'<([a-zA-Z0-9]+)([^>]*\bdata-count="([0-9.]+)"[^>]*)>(.*?)</\1>', re.S)


def check_stat_counters(fname, text, F):
    for m in DATA_COUNT_RE.finditer(text):
        count_val = m.group(3)
        inner = re.sub(r"<[^>]+>", "", m.group(4)).strip()
        line = line_of(text, m.start())
        if re.match(r"^%?0(\D|$)", inner) and count_val not in ("0", "0.0"):
            F.add(fname, line, HATA, "stat-zero",
                  f'data-count="{count_val}" olan öğenin ham metni "{inner}" — JS çalışmadan/'
                  f'arama motoru için de gerçek değer görünmeli')


FORBIDDEN_RE = re.compile(r"gönderildi|başarıyla gönder", re.I)


def check_forbidden_copy(fname, text, F):
    for m in FORBIDDEN_RE.finditer(text):
        line = line_of(text, m.start())
        window = text[max(0, m.start() - 400):m.start()]
        if re.search(r"\bok\s*(===?|:)\s*true\b|\.ok\b|response\.ok", window, re.I):
            F.add(fname, line, UYARI, "forbidden-copy",
                  f'"{m.group(0)}" bulundu — yakınında ok:true benzeri koşul var, insan kontrolü gerek')
        else:
            F.add(fname, line, HATA, "forbidden-copy",
                  f'"{m.group(0)}" bulundu — gerçek backend teslimatı yoksa gösterilmemeli')


def check_nav_teklif(fname, text, F):
    if fname == "404.html":
        return
    hm = re.search(r'<header[^>]*id="hdr".*?</header>', text, re.S)
    if not hm:
        return
    nm = re.search(r"<nav\b.*?</nav>", hm.group(0), re.S)
    if not nm:
        F.add(fname, line_of(text, hm.start()), UYARI, "nav-teklif", "header#hdr içinde <nav> bulunamadı")
        return
    if not re.search(r"teklif", nm.group(0), re.I):
        F.add(fname, line_of(text, hm.start()), UYARI, "nav-teklif", "ana nav'da 'teklif' içeren bir link yok")


def check_links(fname, text, F, model, all_files):
    for m in LINK_RE.finditer(text):
        raw = m.group(1)
        line = line_of(text, m.start())

        # #hol=, #marka=, #urun= özel durumlar (sadece urunler.html hedefliyken)
        hm = re.match(r"^urunler\.html#hol=([a-zA-Z_]+)$", raw)
        if hm:
            if hm.group(1) not in model["hol_keys"]:
                F.add(fname, line, HATA, "deep-link", f"urunler.html#hol={hm.group(1)} — böyle bir hol yok")
            continue
        mm = re.match(r"^urunler\.html#marka=([a-zA-Z_]+)$", raw)
        if mm:
            if mm.group(1) not in ALLOWED_MARKA_KEYS:
                F.add(fname, line, HATA, "deep-link", f"urunler.html#marka={mm.group(1)} — izinli değil")
            continue
        um = re.match(r"^urunler\.html#urun=([a-zA-Z0-9_-]+)$", raw)
        if um:
            if um.group(1) not in model["urun_slugs"]:
                F.add(fname, line, HATA, "deep-link", f"urunler.html#urun={um.group(1)} — ürün slug'ı yok")
            continue
        im = re.match(r"^index\.html#([a-zA-Z][a-zA-Z0-9_-]*)$", raw)
        if im:
            if im.group(1) not in model["index_ids"]:
                F.add(fname, line, HATA, "deep-link", f"index.html#{im.group(1)} — index.html'de böyle bir id yok")
            continue
        tk = re.match(r"^teklif\.html\?(urun|konu)=([a-zA-Z0-9_-]+)$", raw)
        if tk:
            kind, val = tk.group(1), tk.group(2)
            mp = model["urun_map"] if kind == "urun" else model["konu_map"]
            if mp is None:
                F.add(fname, line, UYARI, "deep-link",
                      f"teklif.html?{kind}={val} — teklif.html'de gömülü harita bulunamadı, değer doğrulanamadı")
            elif val not in mp:
                F.add(fname, line, HATA, "deep-link", f"teklif.html?{kind}={val} — haritada tanımlı değil")
            continue
        # sadece kendi dosyasındaki bir id'ye işaret eden çıplak "#id"
        if raw.startswith("#") and len(raw) > 1 and "=" not in raw:
            frag = raw[1:]
            if not re.search(rf'\bid="{re.escape(frag)}"', text) and not re.search(rf'\bname="{re.escape(frag)}"', text):
                F.add(fname, line, HATA, "anchor", f"#{frag} — bu dosyada böyle bir id/name yok")
            continue

        rel, skip = resolve_local_path(fname, raw)
        if skip or rel is None:
            continue
        full = os.path.join(ROOT, rel)
        if not os.path.isfile(full):
            F.add(fname, line, HATA, "broken-link", f"'{raw}' -> '{rel}' repo'da yok")


# ------------------------------------------------------------------------- sitemap
def check_sitemap(F, all_root_html, files_text):
    path = os.path.join(ROOT, "sitemap.xml")
    if not os.path.isfile(path):
        F.add("sitemap.xml", None, HATA, "sitemap", "sitemap.xml yok")
        return
    raw = open(path, encoding="utf-8").read()
    try:
        ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        tree = ET.parse(path)
        urls = tree.getroot().findall("s:url", ns)
    except ET.ParseError as e:
        F.add("sitemap.xml", None, HATA, "sitemap", f"XML parse hatası: {e}")
        return

    seen_locs = set()
    for u in urls:
        loc_el = u.find("s:loc", ns)
        lastmod_el = u.find("s:lastmod", ns)
        loc = loc_el.text.strip() if loc_el is not None and loc_el.text else None
        if not loc:
            F.add("sitemap.xml", None, HATA, "sitemap", "<url> içinde <loc> yok/boş")
            continue
        seen_locs.add(loc)
        lm = re.search(re.escape(loc), raw)
        line = line_of(raw, lm.start()) if lm else None
        rel = resolve_isisah_absolute(loc)
        if rel is None:
            F.add("sitemap.xml", line, HATA, "sitemap", f"beklenmeyen host: {loc}")
        elif not os.path.isfile(os.path.join(ROOT, rel)):
            F.add("sitemap.xml", line, HATA, "sitemap", f"{loc} -> {rel} repo'da yok")
        if lastmod_el is not None and lastmod_el.text:
            lm_val = lastmod_el.text.strip()
            if not re.match(r"^\d{4}-\d{2}-\d{2}$", lm_val):
                F.add("sitemap.xml", line, UYARI, "sitemap", f"{loc}: lastmod biçimi geçersiz görünüyor: {lm_val}")
            else:
                import datetime
                try:
                    datetime.date.fromisoformat(lm_val)
                except ValueError:
                    F.add("sitemap.xml", line, UYARI, "sitemap", f"{loc}: lastmod geçerli bir tarih değil: {lm_val}")

    for fname in all_root_html:
        if fname == "404.html":
            continue
        text = files_text.get(fname, "")
        robots, _ = get_attr_line(text, r'<meta[^>]+name="robots"[^>]+content="([^"]*)"')
        if robots and "noindex" in robots.lower():
            continue
        if fname == "index.html":
            expected = f"{DOMAIN}/"
        elif fname in SHOWROOM_PAGES:
            expected = f"{DOMAIN}/showroom/{fname}"
        else:
            expected = f"{DOMAIN}/{fname}"
        if expected not in seen_locs:
            F.add("sitemap.xml", None, UYARI, "sitemap", f"indekslenebilir sayfa sitemap'te yok: {expected}")


# ------------------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json", action="store_true", help="rapor yerine JSON çıktı ver")
    args = ap.parse_args()

    t0 = time.time()
    all_html = find_html_files(ROOT)
    # sadece repo KÖKündeki *.html dosyaları sayfa denetimine girer (docs/server/vendor
    # find_html_files içinde zaten atlanıyor; burada ayrıca "kök" listesini ayırıyoruz
    # çünkü sitemap eşlemesi ve showroom topolojisi kök dosyalara göre tanımlı).
    root_html = sorted(f for f in all_html if "/" not in f)

    files_text = {}
    for f in root_html:
        try:
            files_text[f] = open(os.path.join(ROOT, f), encoding="utf-8").read()
        except OSError as e:
            files_text[f] = ""
            print(f"UYARI: {f} okunamadı: {e}", file=sys.stderr)

    model = load_urunler_model(files_text)

    F = Findings()
    titles, descs = {}, {}
    agg_brand = {}

    for fname in root_html:
        text = files_text[fname]
        if not text:
            continue
        check_jsonld(fname, text, F, agg_brand)
        check_meta(fname, text, F, titles, descs)
        check_images(fname, text, F)
        check_stat_counters(fname, text, F)
        check_forbidden_copy(fname, text, F)
        check_nav_teklif(fname, text, F)
        check_links(fname, text, F, model, all_html)

    flush_brand_findings(F, agg_brand)

    for t, fs in titles.items():
        if len(fs) > 1:
            for f in fs:
                F.add(f, None, UYARI, "duplicate", f"title tekrarlanıyor ({len(fs)} sayfa): {sorted(fs)}")
    for d, fs in descs.items():
        if len(fs) > 1:
            for f in fs:
                F.add(f, None, UYARI, "duplicate", f"description tekrarlanıyor ({len(fs)} sayfa): {sorted(fs)}")

    check_sitemap(F, root_html, files_text)

    elapsed = time.time() - t0
    errors, warnings = F.counts()

    if args.json:
        out = {
            "root": ROOT,
            "files_scanned": len(root_html),
            "errors": errors,
            "warnings": warnings,
            "elapsed_s": round(elapsed, 3),
            "findings": [
                {"file": f, "line": line, "severity": sev, "category": cat, "message": msg}
                for f, line, sev, cat, msg in sorted(F.items, key=lambda t: (t[0], t[1]))
            ],
        }
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return 1 if errors else 0

    print(f"=== check-site.py — {len(root_html)} HTML dosyası tarandı ({ROOT}) ===\n")
    groups = F.by_file()
    for fname in sorted(groups):
        print(f"[{fname}]")
        for line, sev, cat, msg in groups[fname]:
            loc = f"L{line}" if line else "-"
            print(f"  {sev:<6} {loc:<6} ({cat}) {msg}")
        print()

    print("=== ÖZET ===")
    print(f"HATA: {errors}   UYARI: {warnings}   dosya: {len(root_html)}   "
          f"sorunlu dosya: {len(groups)}   süre: {elapsed:.2f}s")
    if errors:
        print("Sonuç: BAŞARISIZ (en az bir HATA var)")
    else:
        print("Sonuç: OK (sadece uyarılar olabilir)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
