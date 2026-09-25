#!/usr/bin/env python3
"""ISIŞAH sitemap.xml lastmod bakım aracı — stdlib-only, ağ erişimi YOK.

Her <url><loc> girdisini gerçek dosyaya eşler (kök sayfa -> X.html,
/showroom/X.html -> X.html, / -> index.html) ve o dosyayı en son değiştiren
commit'in tarihini (`git log -1 --format=%cs -- <dosya>`) <lastmod>'a yazar.

Kullanım:
  python3 tools/update-sitemap.py --check   # sadece sapmaları raporla, DOSYAYI DEĞİŞTİRME, sapma varsa exit 1
  python3 tools/update-sitemap.py           # yazma modu — sadece gerçekten değişen lastmod'ları günceller;
                                             # hiçbiri değişmiyorsa dosyaya dokunmaz.

NOT: Bu depoda yazma modunu ajanlar DEĞİL, ana oturum (commit sonrası) çalıştırır.
Otomatik ajan çalıştırmaları --check ile sınırlı tutulmalı.
"""
import argparse
import os
import re
import subprocess
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_ROOT = os.path.dirname(SCRIPT_DIR)
ROOT = os.getcwd() if os.path.isfile(os.path.join(os.getcwd(), "index.html")) else DEFAULT_ROOT
SITEMAP = os.path.join(ROOT, "sitemap.xml")
DOMAIN = "https://isisah.com.tr"

URL_LINE_RE = re.compile(r"(<url><loc>(.*?)</loc><lastmod>)(.*?)(</lastmod>.*?</url>)")


def loc_to_file(loc):
    if not loc.startswith(DOMAIN):
        return None
    path = loc[len(DOMAIN):]
    if path in ("", "/"):
        return "index.html"
    path = path.lstrip("/")
    if path.startswith("showroom/"):
        path = path[len("showroom/"):]
    return path


def git_lastmod(relfile):
    try:
        p = subprocess.run(
            ["git", "log", "-1", "--format=%cs", "--", relfile],
            cwd=ROOT, capture_output=True, text=True, timeout=10,
        )
    except Exception as e:
        return None, f"git log çalıştırılamadı: {e}"
    if p.returncode != 0:
        return None, (p.stderr or "git log hata verdi").strip()
    date = p.stdout.strip()
    if not date:
        return None, f"{relfile} için git geçmişi yok (commit edilmemiş mi?)"
    return date, None


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="sadece sapmaları raporla, sitemap.xml'i değiştirme")
    args = ap.parse_args()

    if not os.path.isfile(SITEMAP):
        print(f"HATA: {SITEMAP} yok")
        return 2

    text = open(SITEMAP, encoding="utf-8").read()

    drift = []       # (loc, old, new) — gerçek tarih sapması
    problems = []     # (loc, old, hata_mesaji) — eşlenemedi / dosya yok / git hatası

    def repl(m):
        loc, old = m.group(2), m.group(3)
        f = loc_to_file(loc)
        if f is None:
            problems.append((loc, old, "bilinmeyen host/biçim — eşleştirilemedi"))
            return m.group(0)
        fpath = os.path.join(ROOT, f)
        if not os.path.isfile(fpath):
            problems.append((loc, old, f"eşlenen dosya yok: {f}"))
            return m.group(0)
        new, err = git_lastmod(f)
        if err:
            problems.append((loc, old, err))
            return m.group(0)
        if new != old:
            drift.append((loc, old, new))
            return m.group(1) + new + m.group(4)
        return m.group(0)

    new_text = URL_LINE_RE.sub(repl, text)

    total_url_tags = text.count("<url>")
    matched = len(URL_LINE_RE.findall(text))
    if matched != total_url_tags:
        problems.append((None, None,
                          f"{total_url_tags - matched} <url> girdisi beklenen "
                          f"<url><loc>...</loc><lastmod>...</lastmod>...</url> tek-satır biçiminde değil, atlandı"))

    print(f"sitemap.xml — {len(drift)} lastmod sapması, {len(problems)} sorun "
          f"({matched}/{total_url_tags} <url> işlendi)")
    for loc, old, new in drift:
        print(f"  ~ {loc}: {old} -> {new}")
    for loc, old, msg in problems:
        if loc:
            print(f"  ! {loc} (lastmod={old}): {msg}")
        else:
            print(f"  ! {msg}")

    if args.check:
        return 1 if (drift or problems) else 0

    if not drift:
        print("Yazma atlandı: değişecek bir şey yok (dosya dokunulmadı).")
        return 1 if problems else 0

    with open(SITEMAP, "w", encoding="utf-8") as fh:
        fh.write(new_text)
    print(f"sitemap.xml güncellendi: {len(drift)} lastmod değişti.")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
