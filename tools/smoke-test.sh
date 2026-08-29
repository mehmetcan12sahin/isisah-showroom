#!/bin/bash
# Canlı duman testi — katman 1: curl (HTTP + içerik imzaları + video Range)
#                     katman 2: Playwright (konsol hataları + canlılık) — varsa
# Kullanım: bash tools/smoke-test.sh [taban_url]
BASE="${1:-https://isisah.com.tr}"
FAIL=0
bust="v=$(date +%s)"

say(){ printf "%-4s %s\n" "$1" "$2"; if [ "$1" = "FAIL" ]; then FAIL=1; fi; }

http(){ curl -s -o /dev/null -m 25 -w "%{http_code}" "$1"; }
rng(){ curl -s -o /dev/null -m 25 -H "Range: bytes=0-1023" -w "%{http_code}" "$1"; }
has(){ curl -s -m 25 "$1" | grep -qc "$2"; }

# --- katman 1: HTTP ---
[ "$(http "$BASE/?$bust")" = "200" ] && say OK "kök 200" || say FAIL "kök HTTP"
[ "$(http "$BASE/showroom/urunler.html?$bust")" = "200" ] && say OK "showroom 200" || say FAIL "showroom HTTP"
[ "$(http "$BASE/showroom/fabrika.html?$bust")" = "200" ] && say OK "fabrika 200" || say FAIL "fabrika HTTP"
[ "$(http "$BASE/sitemap.xml")" = "200" ] && say OK "sitemap 200" || say FAIL "sitemap HTTP"
[ "$(http "$BASE/googlebfb5098152a94f7b.html")" = "200" ] && say OK "search-console dosyası duruyor" || say FAIL "search-console dosyası KAYIP"

for v in uretim-film.mp4 uretim-robot.mp4 uretim-salmex.mp4 marka-bumper.mp4 fabrika-scrub.mp4; do
  [ "$(rng "$BASE/showroom/assets/img/$v")" = "206" ] && say OK "video Range: $v" || say FAIL "video Range: $v"
done

has "$BASE/?$bust" "tourbox"            && say OK "kök: tourbox var"           || say FAIL "kök: tourbox yok"
has "$BASE/?$bust" "/showroom/assets/"  && say OK "kök: yollar /showroom/'a çevrili" || say FAIL "kök: yol çevirisi bozuk"
has "$BASE/showroom/urunler.html?$bust" "sublobby" && say OK "showroom: gam sistemi" || say FAIL "showroom: gam sistemi yok"
has "$BASE/showroom/urunler.html?$bust" "vendor/three.module" && say OK "showroom: vendored three" || say FAIL "showroom: three import bozuk"

# --- katman 2: tarayıcı (varsa) ---
if [ -d "$HOME/.isisah-smoke/node_modules/playwright" ]; then
  NODE_PATH="$HOME/.isisah-smoke/node_modules" node "$(dirname "$0")/smoke-browser.mjs" "$BASE" || FAIL=1
else
  echo "SKIP tarayıcı katmanı (playwright yok)"
fi

if [ $FAIL -eq 0 ]; then echo "== DUMAN TESTİ TEMİZ =="; else echo "== DUMAN TESTİ: SORUN VAR =="; fi
exit $FAIL
