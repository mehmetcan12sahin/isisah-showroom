#!/bin/bash
# isisah.com.tr/showroom FTP deploy — şifre ~/.isisah-ftp.netrc'de (git'e girmez)
# Kullanım: bash tools/deploy-ftp.sh   (repo kökünden; sadece kullanılan varlıkları yükler)
# Uzaktan: gh workflow run deploy-ftp.yml  (GitHub Actions; ofis IP'si engelliyken tek yol)
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
    for m in re.findall(r'(?:src|href|data-src)="(assets/[^"?]+)',s): used.add(m)
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
# bağlantı ön testi — sunucu bu IP'yi engelliyorsa sessiz düşme yerine anlaşılır dur
curl -s -m 20 --netrc-file $NETRC -l "ftp://ftp.isisah.com.tr/httpdocs/" > /dev/null || { echo "!! FTP'ye bağlanılamadı (timeout/engel). Deploy yapılmadı. Bkz. HANDOFF: IP engeli / Birhost whitelist."; exit 1; }
echo "$LIST" | grep -vE '^(urunler|fabrika)\.html$' | xargs -P 4 -I{} curl -sS --netrc-file $NETRC --ftp-create-dirs -T "{}" "ftp://ftp.isisah.com.tr/httpdocs/showroom/{}"
# showroom sayfaları: göreli ana sayfa/kurumsal linkleri köke çevrilerek yüklenir (kopya /showroom/index.html'e link vermesin)
python3 - <<'PY'
for f in ('urunler.html','fabrika.html'):
    s=open(f).read()
    s=s.replace('href="index.html#','href="/#').replace('href="index.html"','href="/"')
    s=s.replace('href="hakkimizda.html"','href="/hakkimizda.html"').replace('href="vizyon-misyon.html"','href="/vizyon-misyon.html"')
    open('/tmp/sr_'+f,'w').write(s)
PY
for f in urunler.html fabrika.html; do curl -sS --netrc-file $NETRC -T /tmp/sr_$f "ftp://ftp.isisah.com.tr/httpdocs/showroom/$f" && rm /tmp/sr_$f; done
echo "deploy tamam: https://isisah.com.tr/showroom/"

# kök sayfalar: index + kurumsal alt sayfalar showroom kopyasından türetilir, httpdocs/ köküne yazılır
python3 - <<'PY'
import os
import glob
ROOT_PAGES=[f for f in sorted(glob.glob('*.html')) if f not in ('urunler.html','fabrika.html','404.html')]  # showroom-only sayfalar hariç, kalan her sayfa köke türetilir
open('/tmp/root_pages.txt','w').write(' '.join(ROOT_PAGES))
for f in ROOT_PAGES:
    s=open(f).read()
    s=s.replace('src="assets/','src="/showroom/assets/').replace('href="assets/','href="/showroom/assets/').replace('data-src="assets/','data-src="/showroom/assets/')
    s=s.replace('href="urunler.html','href="/showroom/urunler.html')
    s=s.replace('poster="assets/img/','poster="/showroom/assets/img/')
    s=s.replace('href="fabrika.html"','href="/showroom/fabrika.html"')
    open('/tmp/root_'+f,'w').write(s)
PY
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
