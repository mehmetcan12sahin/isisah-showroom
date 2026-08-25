#!/bin/bash
# isisah.com.tr/showroom FTP deploy — şifre ~/.isisah-ftp.netrc'de (git'e girmez)
# Kullanım: bash tools/deploy-ftp.sh   (repo kökünden; sadece kullanılan varlıkları yükler)
set -e
cd "$(dirname "$0")/.."
NETRC=~/.isisah-ftp.netrc
LIST=$(python3 - <<'PY'
import re,os
used=set(['index.html','urunler.html','sitemap.xml'])
for f in ['index.html','urunler.html']:
    s=open(f).read()
    for m in re.findall(r'(?:src|href)="(assets/[^"]+)"',s): used.add(m)
    for m in re.findall(r"envTex\('(assets/[^']+)'|load\('(assets/[^']+)'",s):
        for g in m:
            if g: used.add(g)
    for m in re.findall(r"'(assets/audio/[^']+)'",s): used.add(m)
for fn in os.listdir('assets/products'): used.add('assets/products/'+fn)
for fn in os.listdir('assets/catalog'):
    if fn.startswith('logo-'): used.add('assets/catalog/'+fn)
for root,_,fns in os.walk('vendor'):
    for fn in fns: used.add(os.path.join(root,fn))
print('\n'.join(sorted(u for u in used if os.path.isfile(u))))
PY
)
echo "$LIST" | xargs -P 4 -I{} curl -s --netrc-file $NETRC --ftp-create-dirs -T "{}" "ftp://ftp.isisah.com.tr/httpdocs/showroom/{}"
echo "deploy tamam: https://isisah.com.tr/showroom/"
