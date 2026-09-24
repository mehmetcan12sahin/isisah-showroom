# isisah.com.tr — Plesk/sunucu config kalemleri (kendin uygulaman gerekiyor)

Bunlar repo/koddan yapılamaz — Plesk panel erişimi (https://46.20.7.162:8443/) veya Birhost destek talebi gerekiyor. Bende yalnız FTP (httpdocs) kimliği var, Plesk admin/SSH yok — şifre girişi/hesap ayarı değişikliği zaten yapmam yasak. Aşağıdakiler doğrulanmış, güncel, sırayla öncelikli.

## 1. AI bot 502 engeli (EN YÜKSEK ÖNCELİK — robots.txt/llms.txt zaten izin veriyor ama etkisiz)
Doğrulandı (24 Eyl): GPTBot/ClaudeBot/CCBot User-Agent'ıyla istek → **502**, normal tarayıcı → 200.
```
curl -A "GPTBot" -o /dev/null -w "%{http_code}\n" https://isisah.com.tr/   # 502
```
502 (Bad Gateway) tipik olarak Plesk'in kendi WAF'ı değil, **Birhost'un edge/anti-bot katmanı** — bu genelde Plesk panelinde görünmez. Yapılacak: **Birhost destek talebi** aç, şunu iste: "isisah.com.tr için GPTBot, ClaudeBot, Claude-SearchBot, Claude-User, PerplexityBot, Perplexity-User, Google-Extended, CCBot, Applebot-Extended, Amazonbot, anthropic-ai, OAI-SearchBot, ChatGPT-User user-agent'larına uygulanan 502 engelini kaldırın — robots.txt/llms.txt bu botlara açıkça izin veriyor." Panelde "Web Application Firewall" / ModSecurity sekmesi varsa önce orada özel bir kural olup olmadığına bak, yoksa direkt destek talebi.

## 2. HTTP → HTTPS 301 yönlendirmesi (kolay, tek tık)
Doğrulandı: `http://isisah.com.tr/` → 200, redirect yok (301 olmalı).
Plesk: **Domains → isisah.com.tr → SSL/TLS Certificates** sekmesi → **"Permanent SEO-safe 301 redirect from HTTP to HTTPS"** kutusunu işaretle → Apply/Uygula. (Bu Plesk'in kendi hazır özelliği, nginx yazmana gerek yok.)

## 3. HSTS header (yok)
Doğrulandı: `Strict-Transport-Security` header'ı hiç dönmüyor.
Plesk: **Domains → isisah.com.tr → Apache & nginx Settings** → "Additional nginx directives" kutusuna ekle:
```
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
```
Uygula. (includeSubDomains www için de geçerli olsun diye — www henüz DNS'te yok, madde 5'e bak.)

## 4. Cache-Control header (statik varlıklarda hiç yok)
Doğrulandı: HTML, woff2, webp, sitemap.xml — hiçbirinde Cache-Control dönmüyor.
Aynı "Additional nginx directives" kutusuna ekle (madde 3'ün altına):
```
location ~* \.(woff2?|jpg|jpeg|png|webp|svg|ico|mp4)$ {
    add_header Cache-Control "public, max-age=31536000, immutable";
}
location ~* \.(css|js)$ {
    add_header Cache-Control "public, max-age=86400";
}
```
Not: dosya adları değişmeden içerik güncellenirse (örn. aynı `og-cover.jpg`) tarayıcı 1 yıl eski sürümü gösterebilir — güncellemede dosya adına `?v=N` ekle (zaten bazı yerlerde yapılıyor) veya dosya adını değiştir.

## 5. www.isisah.com.tr DNS (ayrı konu — nginx değil, DNS zone)
Doğrulandı: `www.isisah.com.tr` hiç çözülmüyor (000/timeout).
Bu Plesk'in "Apache & nginx Settings" kısmında değil, **DNS zone** kaydı meselesi: Birhost DNS panelinde (veya Plesk'in "DNS Settings" sekmesinde) `www` için `isisah.com.tr`'e işaret eden bir **CNAME** (veya aynı IP'ye A kaydı) eklenmesi gerekiyor. Kayıt eklendikten sonra Plesk'te domain'e `www.isisah.com.tr` alias'ı tanımlanmalı, sonra madde 2'deki 301 otomatik www'yi de kapsar (SEO-safe redirect www→non-www ya da tersi — hangisi kanonik istiyorsan onu Plesk'te seç, isisah.com.tr zaten canonical olarak kullanılıyor, yani www→non-www yönlendirmesi doğru olur).

## Bilgi: bu turda ZATEN düzelmiş, artık ELLE dokunma
- **404 davranışı** — eski not "hâlâ WP teması" diyordu, 24 Eyl'de doğrulandı: artık gerçek `404.html` dönüyor. Ekstra `error_page` direktifi gerekmiyor.
- Brotli sıkıştırma zaten çalışıyor, dokunma.

## Uygulama sırası önerisi
1 (destek talebi, süre alır — hemen aç) → 2 (30 saniye) → 3+4 (aynı kutu, 2 dakika) → 5 (DNS + Plesk alias, destek + panel).
