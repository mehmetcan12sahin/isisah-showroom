#!/bin/bash
# isisah.com.tr/showroom FTP deploy — şifre ~/.isisah-ftp.netrc'de (git'e girmez)
# Kullanım: bash tools/deploy-ftp.sh   (repo kökünden; sadece kullanılan varlıkları yükler)
set -e
cd "$(dirname "$0")/.."
NETRC=~/.isisah-ftp.netrc
LIST=$(python3 - <<'PY'
import re,os
used=set(['index.html','urunler.html','fabrika.html','hakkimizda.html','vizyon-misyon.html','sitemap.xml'])
for f in ['index.html','urunler.html','fabrika.html','hakkimizda.html','vizyon-misyon.html']:
    s=open(f).read()
    for m in re.findall(r'(?:src|href)="(assets/[^"]+)"',s): used.add(m)
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
echo "$LIST" | xargs -P 4 -I{} curl -s --netrc-file $NETRC --ftp-create-dirs -T "{}" "ftp://ftp.isisah.com.tr/httpdocs/showroom/{}"
echo "deploy tamam: https://isisah.com.tr/showroom/"

# kök sayfalar: index + kurumsal alt sayfalar showroom kopyasından türetilir, httpdocs/ köküne yazılır
python3 - <<'PY'
import os
for f in ['index.html','hakkimizda.html','vizyon-misyon.html']:
    s=open(f).read()
    s=s.replace('src="assets/','src="/showroom/assets/').replace('href="assets/','href="/showroom/assets/')
    s=s.replace('href="urunler.html','href="/showroom/urunler.html')
    s=s.replace('poster="assets/img/','poster="/showroom/assets/img/')
    s=s.replace('href="fabrika.html"','href="/showroom/fabrika.html"')
    open('/tmp/root_'+f,'w').write(s)
PY
for f in index.html hakkimizda.html vizyon-misyon.html; do
  curl -s --netrc-file $NETRC -T /tmp/root_$f "ftp://ftp.isisah.com.tr/httpdocs/$f" && rm /tmp/root_$f
done
curl -s --netrc-file $NETRC -T sitemap.xml "ftp://ftp.isisah.com.tr/httpdocs/sitemap.xml"
echo "kok sayfalar guncellendi: https://isisah.com.tr/ + /hakkimizda.html + /vizyon-misyon.html"

# yayın sonrası otomatik duman testi
bash "$(dirname "$0")/smoke-test.sh" || echo "!! DUMAN TESTİNDE SORUN VAR — çıktıyı incele"
