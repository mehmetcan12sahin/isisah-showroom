#!/bin/bash
# isisah.com.tr/showroom FTP deploy — şifre ~/.isisah-ftp.netrc'de (git'e girmez)
# Kullanım: bash tools/deploy-ftp.sh   (repo kökünden; sadece kullanılan varlıkları yükler)
# Uzaktan: gh workflow run deploy-ftp.yml  (GitHub Actions; ofis IP'si engelliyken tek yol)
# Kuru çalışma (ağa hiç dokunmadan doğrulama): DRY_RUN=1 [DRY_RUN_OUT=/yol] bash tools/deploy-ftp.sh
#   -> yükleme listesini basar, showroom/ ve kök sayfa yeniden-yazımlarını DRY_RUN_OUT'a yazar,
#      ilk curl/ağ isteğinden ÖNCE çıkar (varsayılan DRY_RUN_OUT: /tmp/isisah-deploy-dry-run).
set -e
cd "$(dirname "$0")/.."
NETRC="${NETRC:-$HOME/.isisah-ftp.netrc}"   # CI: secrets'tan yazılan geçici dosya (bkz. .github/workflows/deploy-ftp.yml)
LIST=$(python3 - <<'PY'
import re,os
import glob
PAGES=sorted(glob.glob('*.html'))  # kökteki tüm sayfalar otomatik (yeni sayfa eklenince listeye elle girmeye gerek yok)
used=set(PAGES+['sitemap.xml','robots.txt','llms.txt','favicon.ico','assets/img/og-cover.jpg','assets/site.webmanifest'])  # og-cover: mutlak URL ile referanslı, regex yakalamaz
for f in PAGES:
    s=open(f).read()
    for m in re.findall(r'(?:src|href|data-src|poster)="(assets/[^"?]+)',s): used.add(m)
    for m in re.findall(r'srcset="([^"]*)"',s):
        # her srcset birden çok "url Nw" adayı taşır (virgülle ayrılmış) — genişlik tanımlayıcısını at
        for cand in m.split(','):
            cand=cand.strip().split(' ')[0].split('?')[0]
            if cand.startswith('assets/'): used.add(cand)
    for m in re.findall(r"envTex\('(assets/[^']+)'|load\('(assets/[^']+)'",s):
        for g in m:
            if g: used.add(g)
    for m in re.findall(r"'(assets/audio/[^']+)'",s): used.add(m)
    # JS içinde tek tırnaklı varlık yolları (fabrika SRC vb.) — ?v= cache-buster'ı at
    for m in re.findall(r"'(assets/[^'?]+)(?:\?[^']*)?'",s): used.add(m)
for fn in os.listdir('assets/products'): used.add('assets/products/'+fn)
for fn in os.listdir('assets/catalog'):
    if fn.startswith('logo-'): used.add('assets/catalog/'+fn)
for fn in os.listdir('assets/fonts'): used.add('assets/fonts/'+fn)
for root,_,fns in os.walk('vendor'):
    for fn in fns: used.add(os.path.join(root,fn))
print('\n'.join(sorted(u for u in used if os.path.isfile(u))))
PY
)
# showroom sayfaları: göreli kök-sayfa linkleri köke çevrilerek yazılır (kopya /showroom/*.html'e göreli link vermesin).
# Bu adım ağa dokunmaz — DRY_RUN ve gerçek yükleme aynı /tmp/sr_* çıktısını kullanır.
python3 - <<'PY'
import glob
import re
import sys
PAGES = [p for p in sorted(glob.glob('*.html')) if p not in ('urunler.html', 'fabrika.html')]
bad = []
for f in ('urunler.html', 'fabrika.html'):
    s = open(f).read()
    s = s.replace('href="index.html#', 'href="/#').replace('href="index.html"', 'href="/"')
    # JS dizgileri (setAttribute('href','teklif.html?urun=...') vb.) — nitelik kuralları bunları yakalamaz
    s = s.replace("'index.html#", "'/#").replace("'index.html'", "'/'")
    for p in PAGES:
        if p == 'index.html':
            continue  # yukarıda özel olarak zaten ele alındı (#-anchor + bare href)
        for q in ('href="', "'"):
            s = s.replace(f'{q}{p}#', f'{q}/{p}#')
            s = s.replace(f'{q}{p}?', f'{q}/{p}?')
            s = s.replace(f'{q}{p}{q[-1]}', f'{q}/{p}{q[-1]}')
    # güvenlik ağı: kök sayfaya hâlâ göreli giden bir dizgi kaldıysa canlıda /showroom/<sayfa> 404 verir → yayını durdur
    for p in PAGES:
        for m in re.finditer(r'["\'`]' + re.escape(p), s):
            bad.append(f"{f}:{s.count(chr(10), 0, m.start()) + 1}: {s[m.start():m.start() + 60]!r}")
    open('/tmp/sr_'+f,'w').write(s)
if bad:
    print("!! showroom sayfalarında kök sayfaya göreli link kaldı (canlıda /showroom/ altında 404 olur):", *bad, sep="\n  ")
    sys.exit(1)
PY
# kök sayfalar: index + kurumsal alt sayfalar showroom kopyasından türetilir, httpdocs/ köküne yazılır.
# Bu adım da ağa dokunmaz — DRY_RUN ve gerçek yükleme aynı /tmp/root_* çıktısını kullanır.
# PAGES = kökteki tüm sayfalar (urunler.html/fabrika.html hariç) — yeni bir kök sayfa (kategori, teklif.html vb.)
# eklenince burayı elle güncellemeye gerek yok; ?konu=/?urun= gibi sorgu dizeli linkler de kapsanır.
python3 - <<'PY'
import os
import re
import sys
import glob
bad=[]
ROOT_PAGES=[f for f in sorted(glob.glob('*.html')) if f not in ('urunler.html','fabrika.html','404.html')]  # showroom-only sayfalar hariç, kalan her sayfa köke türetilir
open('/tmp/root_pages.txt','w').write(' '.join(ROOT_PAGES))
def _rewrite_srcset(m):
    # srcset="a.webp 480w, b.webp 800w" -> her adayı ayrı ayrı /showroom/'a çevir
    cands=[]
    for part in m.group(1).split(','):
        part=part.strip()
        if not part: continue
        bits=part.split(' ',1)
        url=bits[0]
        rest=' '+bits[1] if len(bits)>1 else ''
        if url.startswith('assets/'): url='/showroom/'+url
        cands.append(url+rest)
    return 'srcset="'+', '.join(cands)+'"'
for f in ROOT_PAGES:
    s=open(f).read()
    s=s.replace('src="assets/','src="/showroom/assets/').replace('href="assets/','href="/showroom/assets/').replace('data-src="assets/','data-src="/showroom/assets/')
    s=re.sub(r'srcset="([^"]*)"', _rewrite_srcset, s)
    s=s.replace('href="urunler.html','href="/showroom/urunler.html')
    s=s.replace('poster="assets/img/','poster="/showroom/assets/img/')
    s=s.replace('href="fabrika.html"','href="/showroom/fabrika.html"')
    # güvenlik ağı: kökte göreli kalan showroom yolu httpdocs/<yol> olarak 404 verir → yayını durdur
    for m in re.finditer(r'["\'`(](?:assets/|urunler\.html|fabrika\.html)', s):
        bad.append(f"{f}:{s.count(chr(10), 0, m.start()) + 1}: {s[m.start():m.start() + 60]!r}")
    open('/tmp/root_'+f,'w').write(s)
if bad:
    print("!! kök sayfalarda /showroom/'a çevrilmemiş göreli yol kaldı (canlıda 404 olur):", *bad, sep="\n  ")
    sys.exit(1)
PY

if [ "${DRY_RUN:-0}" = "1" ]; then
  OUT="${DRY_RUN_OUT:-/tmp/isisah-deploy-dry-run}"
  rm -rf "$OUT"
  mkdir -p "$OUT/showroom" "$OUT/root"
  echo "$LIST" > "$OUT/upload-list.txt"
  echo "== DRY_RUN: yüklenecek $(echo "$LIST" | grep -c .) dosya (liste: $OUT/upload-list.txt) =="
  echo "$LIST"
  for f in urunler.html fabrika.html; do
    [ -f "/tmp/sr_$f" ] && cp "/tmp/sr_$f" "$OUT/showroom/$f"
  done
  for f in $(cat /tmp/root_pages.txt); do
    [ -f "/tmp/root_$f" ] && cp "/tmp/root_$f" "$OUT/root/$f"
  done
  for extra in sitemap.xml robots.txt llms.txt favicon.ico 404.html; do
    [ -f "$extra" ] && cp "$extra" "$OUT/root/$extra"
  done
  rm -f /tmp/sr_urunler.html /tmp/sr_fabrika.html
  for f in $(cat /tmp/root_pages.txt); do rm -f "/tmp/root_$f"; done
  rm -f /tmp/root_pages.txt
  echo "DRY_RUN tamam — hiçbir ağ isteği yapılmadı. Çıktı: $OUT"
  exit 0
fi

# bağlantı ön testi — sunucu bu IP'yi engelliyorsa sessiz düşme yerine anlaşılır dur
curl -s -m 20 --netrc-file $NETRC -l "ftp://ftp.isisah.com.tr/httpdocs/" > /dev/null || { echo "!! FTP'ye bağlanılamadı (timeout/engel). Deploy yapılmadı. Bkz. HANDOFF: IP engeli / Birhost whitelist."; exit 1; }
# .html hariç: kök sayfalar sadece httpdocs/ köküne gider (aşağıda), showroom'a ham kopyaları gereksiz.
echo "$LIST" | grep -v '\.html$' | xargs -P 4 -I{} curl -sS --netrc-file $NETRC --ftp-create-dirs -T "{}" "ftp://ftp.isisah.com.tr/httpdocs/showroom/{}"
# showroom sayfaları (yukarıda /tmp/sr_* olarak zaten hazırlandı; göreli kök-sayfa linkleri köke çevrilmiş durumda)
for f in urunler.html fabrika.html; do curl -sS --netrc-file $NETRC -T /tmp/sr_$f "ftp://ftp.isisah.com.tr/httpdocs/showroom/$f" && rm /tmp/sr_$f; done
echo "deploy tamam: https://isisah.com.tr/showroom/"

# kök sayfalar (yukarıda /tmp/root_* olarak zaten hazırlandı; assets/href/srcset/poster /showroom/'a çevrilmiş durumda)
for f in $(cat /tmp/root_pages.txt); do
  curl -sS --netrc-file $NETRC -T /tmp/root_$f "ftp://ftp.isisah.com.tr/httpdocs/$f" && rm /tmp/root_$f
done
rm -f /tmp/root_pages.txt
curl -sS --netrc-file $NETRC -T sitemap.xml "ftp://ftp.isisah.com.tr/httpdocs/sitemap.xml"
curl -sS --netrc-file $NETRC -T robots.txt "ftp://ftp.isisah.com.tr/httpdocs/robots.txt"
for f in llms.txt favicon.ico 404.html; do curl -sS --netrc-file $NETRC -T $f "ftp://ftp.isisah.com.tr/httpdocs/$f"; done
echo "kok sayfalar guncellendi: https://isisah.com.tr/ + /hakkimizda.html + /vizyon-misyon.html"

# yayın sonrası otomatik duman testi (SMOKE=0 → atla; CI ayrı adımda koşar ve sonucu iş durumuna yansıtır)
if [ "${SMOKE:-1}" != "0" ]; then
  bash "$(dirname "$0")/smoke-test.sh" || echo "!! DUMAN TESTİNDE SORUN VAR — çıktıyı incele"
fi
