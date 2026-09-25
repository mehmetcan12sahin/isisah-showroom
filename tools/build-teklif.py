#!/usr/bin/env python3
# teklif.html jeneratörü — ortak iskelet: tools/pagegen.py (index.html'in stil/header/footer'ını alır).
# ?urun=<slug> bağlam haritası (URUN_MAP) artık TEK KAYNAK assets/data/products.json'dan yüklenir
# (fabrikasyon yok; bkz. tools/build-products.py, .claude/skills/isisah-urun-ekle/SKILL.md).
# ?konu=<key> haritası (KONU_MAP) hâlâ urunler.html'den REGEX ile çıkarılır — BRANDS/ISISAH_CATS marka+gam
# görünen-adı/ikon meta verisidir, products.json'un ürün veri modelinde yok.
# 11 kategori sayfası adı tools/build-category-pages.py'den elle mirror'lanır (o script import edilemez —
# import edilince kendi dosyalarını hemen yazar; bu script'in aynı mirror-ve-elle-senkron kuralına
# tabi olduğu tools/build-category-pages.py:3-4'te zaten belirtilmiş).
# index.html header'ı başka bir ajan tarafından paralel değiştiriliyor olabilir — bu script pagegen.page()
# dışında header/nav içeriğine dair HİÇBİR ŞEY varsaymaz (idempotent, nav yapısına bağımlı değil).
# Çalıştır: python3 tools/build-teklif.py  (repo kökünden veya tools/ içinden)
import re, json, pathlib
from pagegen import ROOT, page

SRC = (ROOT/'urunler.html').read_text(encoding='utf-8')

def _dict_block(name, text):
    m = re.search(r"const %s=\{(.*?)\n\};" % name, text, re.S)
    if not m:
        raise SystemExit(f'build-teklif.py: urunler.html içinde {name} bulunamadı (yapı değişti mi?)')
    return m.group(1)

# ---------------- ?urun=<slug> → ürün adı (assets/data/products.json, img=slug, h=ad) ----------------
_PRODUCTS_PATH = ROOT / 'assets/data/products.json'
_products = json.loads(_PRODUCTS_PATH.read_text(encoding='utf-8'))['products']
URUN_MAP = {p['img']: p['h'] for p in _products}
if len(URUN_MAP) < 30:
    raise SystemExit(f'build-teklif.py: {_PRODUCTS_PATH} içinde sadece {len(URUN_MAP)} ürün var')

# ---------------- ?konu=<key> → marka/hol adı (BRANDS + ISISAH_CATS, urunler.html'den) ----------------
KONU_MAP = {}
_bb = _dict_block('BRANDS', SRC)
for _m in re.finditer(r"(\w+):\{name:'([^']*)',logo:'[^']*',list:(?:\w+),doorX:", _bb):
    KONU_MAP[_m.group(1)] = _m.group(2)
_cb = _dict_block('ISISAH_CATS', SRC)
for _m in re.finditer(r"(\w+):\{cat:'[^']*',icon:'.*?',desc:'[^']*',\s*name:'([^']*)'", _cb, re.S):
    KONU_MAP[_m.group(1)] = _m.group(2)
if len(KONU_MAP) < 11:  # 3 marka + 8 ISIŞAH gamı
    raise SystemExit(f'build-teklif.py: sadece {len(KONU_MAP)} hol/marka ayrıştırıldı — regex urunler.html ile senkron değil')

# ---------------- ?konu=<key> → 11 kategori sayfası adı (tools/build-category-pages.py h1'leri, elle mirror) ----------------
# Kaynak: build_cat(...)/build_hub(...) çağrılarındaki h1 argümanı. build-category-pages.py import edilemediği
# için (üst seviyede dosya yazıyor) burada literal kopya tutulur — o dosyadaki h1 değişirse burayı da güncelle.
KATEGORI_SAYFA_ADI = {
    'sanayi-tipi-rezistans': 'Sanayi Tipi Rezistans',
    'endustriyel-mutfak-isiticilari': 'Endüstriyel Mutfak Isıtıcıları',
    'beyaz-esya-isiticilari': 'Beyaz Eşya Isıtıcı Elemanları',
    'agir-sanayi-isiticilari': 'Ağır Sanayi Isıtıcı Üniteleri',
    'endustriyel-isitma-klima-santrali': 'Endüstriyel Isıtma & Klima Santrali',
    'demiryolu-isiticilari': 'Demiryolu Isıtıcıları',
    'savunma-sanayi-isitma-sistemleri': 'Savunma Sanayi Isıtma Sistemleri',
    'boya-kurutma-firini': 'Boya Kurutma Fırını — BOYKUR',
    'salmex-isi-esanjoru': 'Isı Eşanjörü Üreticisi — SALMEX',
    'paslanmaz-celik-boru-ureticisi': 'Paslanmaz Çelik Boru Üreticisi — BORŞAH',
    'isisah-endustriyel': 'ISIŞAH ENDÜSTRİYEL',
}
KONU_MAP.update(KATEGORI_SAYFA_ADI)
KONU_MAP['fabrika-turu'] = 'Fabrika Turu'

def _json_for_js(d):
    s = json.dumps(d, ensure_ascii=False, separators=(',', ':'))
    # </script> kaçışı + JS string literal içinde geçersiz olabilecek U+2028/2029 satır ayırıcıları (savunma amaçlı;
    # şu anki verilerde yok ama üretilen HTML'e gömülen JS'te sessiz bir sözdizimi hatasına dönüşmesin)
    return s.replace('</', '<\\/').replace('\u2028', '\\u2028').replace('\u2029', '\\u2029')

URUN_MAP_JS = _json_for_js(URUN_MAP)
KONU_MAP_JS = _json_for_js(KONU_MAP)

# ================= SAYFA İÇERİĞİ =================
# FORM_ENDPOINT boşken (mevcut durum — backend henüz onaylı/test edilmiş değil): mailto: ile e-posta istemcisi açılır.
# server/README.md'deki etkinleştirme adımlarını tamamlayınca BURAYI mutlak URL ile değiştirip yeniden çalıştırın
# (HANDOFF.md 2. DALGA kararı: action/endpoint MUTLAK URL olmalı — github.io aynasında da çalışsın, örn.
# 'https://isisah.com.tr/teklif.php'; göreli '/teklif.php' ayna alan adında (mehmetcan12sahin.github.io) çalışmaz).
FORM_ENDPOINT = ''

TEKLIF_CSS = '''
  .tgrid{display:grid;grid-template-columns:1.35fr .65fr;gap:40px;align-items:start}
  @media(max-width:900px){.tgrid{grid-template-columns:1fr}}
  .tcard{border:1px solid rgba(255,255,255,.07);border-radius:18px;padding:32px;background:linear-gradient(165deg,rgba(16,16,24,.9),rgba(4,4,8,.95))}
  .tform fieldset{border:0;padding:0;margin:0 0 28px}
  .tform legend{font-family:var(--tech);font-weight:600;font-size:.78rem;letter-spacing:.14em;text-transform:uppercase;color:var(--vio-text);margin-bottom:16px;padding:0}
  .tfield{display:flex;flex-direction:column;gap:7px;margin-bottom:18px}
  .tfield label{font-family:var(--tech);font-size:.82rem;letter-spacing:.02em;color:var(--steel);display:flex;gap:8px;align-items:baseline;flex-wrap:wrap}
  .tfield .req{font-size:.72rem;color:var(--muted);text-transform:none;letter-spacing:0}
  .tfield input,.tfield textarea{width:100%;min-height:44px;background:var(--panel2);border:1px solid var(--line);border-radius:10px;
    padding:11px 14px;color:var(--ink);font:inherit;font-size:.95rem;line-height:1.5;transition:border-color 160ms var(--ease-out),box-shadow 160ms var(--ease-out)}
  .tfield textarea{min-height:132px;resize:vertical}
  .tfield input::placeholder,.tfield textarea::placeholder{color:var(--muted)}
  .tfield input:focus-visible,.tfield textarea:focus-visible{outline:2px solid var(--vio-text);outline-offset:1px;border-color:var(--vio-text)}
  .trow2{display:grid;grid-template-columns:1fr 1fr;gap:16px}
  @media(max-width:560px){.trow2{grid-template-columns:1fr}}
  .tferr{display:none;gap:7px;align-items:flex-start;color:var(--mag2);font-size:.84rem;line-height:1.4}
  .tferr::before{content:"!";flex:none;width:18px;height:18px;border-radius:50%;background:color-mix(in srgb,var(--mag2) 20%,transparent);
    color:var(--mag2);font-weight:700;font-size:.78rem;display:flex;align-items:center;justify-content:center;margin-top:1px}
  .tfield.has-error .tferr{display:flex}
  /* errContact (E-posta/Telefon paylaşımlı hata) .tfield içinde DEĞİL — .trow2'nin dışında, iki alanın
     ortak hatası olduğu için tek bir .tfield'a ait değil; yukarıdaki ata-seçici onu asla açamaz.
     JS validate() bunu doğrudan .show sınıfıyla açar/kapatır (A2: aria-describedby görünür olmalı). */
  #errContact.show{display:flex}
  .tfield.has-error input,.tfield.has-error textarea{border-color:var(--mag2);box-shadow:0 0 0 1px color-mix(in srgb,var(--mag2) 40%,transparent)}
  .hp{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}
  #errSummary{display:none;border:1px solid color-mix(in srgb,var(--mag2) 55%,transparent);border-radius:12px;padding:18px 20px;margin-bottom:26px;
    background:color-mix(in srgb,var(--mag2) 10%,var(--panel2))}
  #errSummary:focus-visible{outline:2px solid var(--vio-text);outline-offset:2px}
  #errSummary h2{font-size:.95rem;text-transform:none;letter-spacing:0;color:#fff;margin:0 0 10px}
  #errSummary ul{list-style:none;display:flex;flex-direction:column;gap:6px}
  #errSummary a{color:var(--mag2);font-size:.88rem;text-decoration:underline;text-underline-offset:2px}
  #errSummary a:focus-visible{outline:2px solid var(--vio-text);outline-offset:2px}
  .ctxline{font-size:.86rem;color:var(--vio-text);margin:-4px 0 4px}
  .tactions{display:flex;flex-wrap:wrap;gap:14px;align-items:center;margin-top:8px}
  .tactions button{border:0;cursor:pointer;min-height:44px}
  #formStatus{display:none;margin-top:18px;padding:14px 16px;border-radius:10px;font-size:.88rem;line-height:1.55;color:var(--steel);
    background:var(--panel2);border:1px solid var(--line)}
  #formStatus.is-error{color:#fff;border-color:color-mix(in srgb,var(--mag2) 55%,transparent);background:color-mix(in srgb,var(--mag2) 12%,var(--panel2))}
  #formStatus[data-show="1"]{display:block}
  #mailtoOpenLink{margin-top:14px}
  /* .btn{display:inline-flex} (index.html stili) [hidden]'ın display:none'ını author-stili olarak ezer
     (UA stylesheet her zaman author stilinden düşük öncelikli) — id-özgüllüğüyle geri kazan, yoksa
     buton sayfa yüklenirken submit edilmeden önce de görünür kalır. */
  #mailtoOpenLink[hidden]{display:none}
  .tfallback{margin-top:22px;padding-top:20px;border-top:1px solid var(--line);display:flex;flex-wrap:wrap;gap:18px;font-size:.9rem;color:var(--muted)}
  .tfallback a{color:var(--steel);text-decoration:underline;text-underline-offset:2px;min-height:44px;display:inline-flex;align-items:center}
  .tfallback a:focus-visible{outline:2px solid var(--vio-text);outline-offset:2px}
  .tguide h2{font-size:1.15rem;margin:0 0 14px}
  .tguide ul{list-style:none;display:flex;flex-direction:column;gap:12px}
  .tguide li{display:flex;gap:10px;color:var(--steel);font-size:.92rem;line-height:1.5}
  .tguide li::before{content:"";flex:none;width:7px;height:7px;margin-top:8px;border-radius:2px;background:var(--grad);box-shadow:0 0 8px var(--vio2)}
  .tguide .note{margin-top:18px;color:var(--muted);font-size:.84rem;line-height:1.5}
  /* KVKK yuvası — onaylı metin gelene dek BİLEREK boş; bkz. data_needed. Metin gelince <p> içine koy, checkbox EKLEME
     (onay kutusu, atıfta bulunduğu metin yoksa erişilebilirlik/hukuk açısından yanlış — F2/§10). */
  .tkvkk-slot{display:none}
'''

FORM_HTML = '''
<style>{TEKLIF_CSS}</style>
<section class="pad" style="padding-top:30px">
  <div class="wrap tgrid">
    <div class="tcard reveal">
      <form id="teklifForm" class="tform" method="post" novalidate autocomplete="on">
        <div id="errSummary" role="alert" tabindex="-1">
          <h2>Formda eksik veya hatalı alan var</h2>
          <ul id="errList"></ul>
        </div>

        <!-- Bal küpü (honeypot): gerçek kullanıcı görmez/doldurmaz, dolduran bot sayılır -->
        <div class="hp" aria-hidden="true">
          <label for="fWeb">Web siteniz</label>
          <input type="text" id="fWeb" name="hp_web" tabindex="-1" autocomplete="off">
        </div>
        <input type="hidden" id="fStart" name="t_start" value="">

        <fieldset>
          <legend>İletişim bilgileri</legend>
          <div class="tfield">
            <label for="fFirma">Firma</label>
            <input type="text" id="fFirma" name="firma" autocomplete="organization" maxlength="120" placeholder="Örn: ABC Makine San. Tic. Ltd. Şti.">
          </div>
          <div class="tfield">
            <label for="fAd">Ad Soyad <span class="req">(gerekli)</span></label>
            <input type="text" id="fAd" name="ad_soyad" autocomplete="name" maxlength="120" aria-describedby="errAd" required>
            <p class="tferr" id="errAd">Ad Soyad girin.</p>
          </div>
          <div class="trow2">
            <div class="tfield">
              <label for="fEposta">E-posta <span class="req">(e-posta veya telefon gerekli)</span></label>
              <input type="email" id="fEposta" name="eposta" autocomplete="email" inputmode="email" maxlength="160" aria-describedby="errContact" placeholder="ornek@firma.com">
            </div>
            <div class="tfield">
              <label for="fTel">Telefon <span class="req">(e-posta veya telefon gerekli)</span></label>
              <input type="tel" id="fTel" name="telefon" autocomplete="tel" inputmode="tel" maxlength="32" aria-describedby="errContact" placeholder="0 (5xx) xxx xx xx">
            </div>
          </div>
          <p class="tferr" id="errContact">E-posta veya telefondan en az birini girin; e-posta yazdıysanız geçerli biçimde olsun.</p>
        </fieldset>

        <fieldset>
          <legend>Talep detayı</legend>
          <div class="tfield">
            <label for="fUrun">Ürün / Konu</label>
            <input type="text" id="fUrun" name="urun_konu" maxlength="160" placeholder="Örn: Sanayi Tipi Rezistans, SALMEX Eşanjör, Fabrika Turu">
            <p class="ctxline" id="ctxLine" hidden></p>
          </div>
          <div class="tfield">
            <label for="fAdet">Adet / Miktar</label>
            <input type="text" id="fAdet" name="adet" inputmode="numeric" maxlength="60" placeholder="Örn: 50 adet, aylık 200 adet">
          </div>
          <div class="tfield">
            <label for="fAciklama">İhtiyaç açıklaması <span class="req">(gerekli)</span></label>
            <textarea id="fAciklama" name="aciklama" maxlength="2000" aria-describedby="errAciklama" required
              placeholder="Uygulamayı, ölçüleri/çizim numarasını, çalışma koşullarını ve teslim beklentinizi kısaca yazın."></textarea>
            <p class="tferr" id="errAciklama">İhtiyaç açıklaması girin.</p>
          </div>
        </fieldset>

        <div class="tkvkk-slot"><!-- KVKK aydınlatma metni onaylanınca buraya <p> olarak eklenecek; onay kutusu metinsiz eklenmez --></div>

        <div class="tactions">
          <button type="button" class="btn" id="submitBtn" disabled>Teklif İste <span>→</span></button>
          <a class="btn ghost" href="tel:+902242610527">Ara: 0224 261 05 27</a>
        </div>
        <p id="formStatus" role="status" aria-live="polite"></p>
        <a id="mailtoOpenLink" class="btn ghost sc" href="#" hidden>E-posta hazır — burada da açabilirsiniz</a>

        <div class="tfallback">
          <span>Formu kullanmadan doğrudan ulaşın:</span>
          <a href="tel:+902242610527">0224 261 05 27</a>
          <a href="mailto:info@isisah.com.tr">info@isisah.com.tr</a>
        </div>
        <noscript><p class="tferr" style="display:flex;margin-top:16px">Bu form JavaScript gerektirir. Lütfen doğrudan 0224 261 05 27'yi arayın veya info@isisah.com.tr'ye yazın.</p></noscript>
      </form>
    </div>

    <div class="tcard tguide reveal" data-d="2">
      <h2>Teklifinizi hızlandıracak bilgiler</h2>
      <ul>
        <li>Ürün / uygulama tanımı</li>
        <li>Ölçüler veya çizim numarası</li>
        <li>Adet</li>
        <li>Çalışma koşulları — gerilim/güç veya basınç/sıcaklık</li>
        <li>Teslim yeri ve hedef tarih</li>
      </ul>
      <p class="note">Bu liste genel bir kontrol listesidir; yukarıdaki bilgilerden elinizde olanları paylaşmanız yeterlidir, hepsi zorunlu değildir.</p>
    </div>
  </div>
</section>

<section class="pad" style="padding-top:0">
  <div class="wrap">
    <div class="pgcta reveal">
      <a class="btn ghost" href="hakkimizda.html">Hakkımızda</a>
      <a class="btn ghost" href="index.html#markalar">Markalarımız</a>
      <a class="btn ghost" href="index.html#iletisim">İletişim</a>
    </div>
  </div>
</section>

<script>
(function(){
  var FORM_ENDPOINT = {FORM_ENDPOINT_JS};
  // tools/check-site.py sitedeki tüm teklif.html?urun=/?konu= deep-link'lerini doğrulamak için
  // bu dosyada "const *URUN*=" / "const *KONU*=" regex'i arıyor — isim/anahtar kelimesini değiştirme.
  const URUN_MAP = {URUN_MAP_JS};
  const KONU_MAP = {KONU_MAP_JS};

  var form = document.getElementById('teklifForm');
  var fFirma = document.getElementById('fFirma'), fAd = document.getElementById('fAd'),
      fEposta = document.getElementById('fEposta'), fTel = document.getElementById('fTel'),
      fUrun = document.getElementById('fUrun'), fAdet = document.getElementById('fAdet'),
      fAciklama = document.getElementById('fAciklama'), fWeb = document.getElementById('fWeb'),
      fStart = document.getElementById('fStart');
  var errSummary = document.getElementById('errSummary'), errList = document.getElementById('errList');
  var formStatus = document.getElementById('formStatus');
  var mailtoOpenLink = document.getElementById('mailtoOpenLink');
  var submitBtn = document.getElementById('submitBtn');
  var ctxLine = document.getElementById('ctxLine');

  try { fStart.value = String(Date.now()); } catch (e) {}

  // A1: buton statik HTML'de type="button" disabled — JS'siz ziyaretçi hiçbir şekilde native
  // GET submit tetikleyemez (form ayrıca method="post" ile de korunur). Script çalıştığına göre
  // artık gerçek submit kontrolüne dönüştür.
  try { submitBtn.disabled = false; submitBtn.type = 'submit'; } catch (e) {}

  // ---- Bağlam ön-doldurma: ?urun=<slug> veya ?konu=<key> — yalnız bilinen anahtarlar, HTML enjeksiyonu yok ----
  try {
    var qs = new URLSearchParams(location.search);
    var urun = qs.get('urun'), konu = qs.get('konu'), ad = null;
    if (urun && Object.prototype.hasOwnProperty.call(URUN_MAP, urun)) ad = URUN_MAP[urun];
    else if (konu && Object.prototype.hasOwnProperty.call(KONU_MAP, konu)) ad = KONU_MAP[konu];
    if (ad) {
      fUrun.value = ad;
      ctxLine.textContent = 'Bağlamdan alındı: ' + ad;
      ctxLine.hidden = false;
    }
  } catch (e) {}

  function setError(fieldWrap, errEl, msg, show) {
    if (show) {
      fieldWrap.classList.add('has-error');
      if (errEl && msg) errEl.textContent = msg;
    } else {
      fieldWrap.classList.remove('has-error');
    }
  }

  function validate() {
    var errs = []; // {id, label, focusEl}
    var adWrap = fAd.closest('.tfield');
    var adOk = fAd.value.trim().length > 0;
    setError(adWrap, null, '', !adOk);
    fAd.setAttribute('aria-invalid', adOk ? 'false' : 'true');
    if (!adOk) errs.push({id: 'fAd', label: 'Ad Soyad girin.'});

    var epostaWrap = fEposta.closest('.tfield'), telWrap = fTel.closest('.tfield');
    var errContact = document.getElementById('errContact');
    var epostaVal = fEposta.value.trim(), telVal = fTel.value.trim();
    var emailRe = /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/;
    var epostaGecerli = epostaVal === '' || emailRe.test(epostaVal);
    var contactOk = (epostaVal !== '' || telVal !== '') && epostaGecerli;
    setError(epostaWrap, null, '', !contactOk);
    setError(telWrap, null, '', !contactOk);
    fEposta.setAttribute('aria-invalid', contactOk ? 'false' : 'true');
    fTel.setAttribute('aria-invalid', contactOk ? 'false' : 'true');
    // A2: errContact .trow2'nin DIŞINDA, iki alanın paylaştığı tek mesaj — .tfield.has-error ata-seçicisi
    // onu hiçbir zaman gösteremez (bkz. CSS'teki not). Görünürlüğünü doğrudan .show ile yönet, aksi halde
    // aria-describedby="errContact" görünmeyen (display:none) bir elemana işaret eder ve hiçbir AT'ye
    // okutulmaz.
    if (errContact) errContact.classList.toggle('show', !contactOk);
    if (!contactOk) {
      var msg = (epostaVal !== '' && !epostaGecerli)
        ? 'Geçerli bir e-posta adresi yazın veya telefon numarası girin.'
        : 'E-posta veya telefondan en az birini girin.';
      errs.push({id: 'fEposta', label: msg});
    }

    var acWrap = fAciklama.closest('.tfield');
    var acOk = fAciklama.value.trim().length > 0;
    setError(acWrap, null, '', !acOk);
    fAciklama.setAttribute('aria-invalid', acOk ? 'false' : 'true');
    if (!acOk) errs.push({id: 'fAciklama', label: 'İhtiyaç açıklaması girin.'});

    return errs;
  }

  function showErrors(errs) {
    errList.innerHTML = '';
    errs.forEach(function(er) {
      var li = document.createElement('li');
      var a = document.createElement('a');
      a.href = '#' + er.id;
      a.textContent = er.label;
      a.addEventListener('click', function(ev) {
        ev.preventDefault();
        var t = document.getElementById(er.id);
        if (t) { t.focus(); }
      });
      li.appendChild(a);
      errList.appendChild(li);
    });
    errSummary.style.display = 'block';
    errSummary.focus();
  }

  function hideErrors() {
    errSummary.style.display = 'none';
  }

  function setStatus(msg, isError) {
    formStatus.textContent = msg;
    formStatus.className = isError ? 'is-error' : '';
    formStatus.setAttribute('data-show', msg ? '1' : '0');
  }

  function bodyLines(aciklamaOverride) {
    var rows = [
      ['Firma', fFirma.value.trim()],
      ['Ad Soyad', fAd.value.trim()],
      ['E-posta', fEposta.value.trim()],
      ['Telefon', fTel.value.trim()],
      ['Ürün/Konu', fUrun.value.trim()],
      ['Adet/Miktar', fAdet.value.trim()],
    ];
    var lines = rows.filter(function(r){return r[1];}).map(function(r){return r[0] + ': ' + r[1];});
    lines.push('');
    lines.push('İhtiyaç açıklaması:');
    lines.push(aciklamaOverride !== undefined ? aciklamaOverride : fAciklama.value.trim());
    return lines.join('\\n');
  }

  // A3: mailto: href'in uzunluğunu koru — bazı OS/e-posta istemci mailto handler'ları ~2000-2083 karakter
  // civarında sessizce keser. Sınırı aşarsa SADECE aciklama'yı (tek serbest-uzunluklu alan) görünür bir
  // Türkçe işaretle kısalt; kullanıcıyı durum mesajıyla bilgilendir. Teslim edildi iddiası YOK — mailto sadece
  // istemciyi hazırlar, gönderimi kullanıcı yapar.
  var MAILTO_MAX_LEN = 1800;

  function composeMailto() {
    var subject = 'Teklif Talebi — ' + (fUrun.value.trim() || 'Genel');
    var acFull = fAciklama.value.trim();
    var marker = ' … (devamı kısaltıldı — tam metni telefon veya e-posta ile iletin)';

    function buildUrl(ac) {
      return 'mailto:info@isisah.com.tr'
        + '?subject=' + encodeURIComponent(subject)
        + '&body=' + encodeURIComponent(bodyLines(ac));
    }

    var url = buildUrl(acFull);
    var truncated = false;
    if (url.length > MAILTO_MAX_LEN && acFull.length > 0) {
      truncated = true;
      // acFull karakter sayısı üzerinde ikili arama: encodeURIComponent Türkçe karakterlerde sabit
      // olmayan bir oranda büyüdüğü için doğrudan hesap yerine deneyerek en uzun sığan kesimi bul.
      var lo = 0, hi = acFull.length, fit = 0;
      while (lo <= hi) {
        var mid = (lo + hi) >> 1;
        if (buildUrl(acFull.slice(0, mid).trim() + marker).length <= MAILTO_MAX_LEN) { fit = mid; lo = mid + 1; }
        else hi = mid - 1;
      }
      url = buildUrl(acFull.slice(0, fit).trim() + marker);
    }

    if (truncated) {
      setStatus('E-posta uygulamanızda hazırlandı; ancak açıklamanız uzun olduğu için kısaltıldı. Tam metni iletmek için lütfen 0224 261 05 27\\'yi arayın veya info@isisah.com.tr\\'ye yazın.', true);
    } else {
      setStatus('E-posta uygulamanızda teklif e-postası hazırlandı. Göndermek için e-postada Gönder\\'e basın. Açılmadıysa 0224 261 05 27\\'yi arayabilir veya info@isisah.com.tr\\'ye yazabilirsiniz.', false);
    }
    mailtoOpenLink.href = url;
    mailtoOpenLink.hidden = false;
    location.href = url;
  }

  var sending = false;
  function submitToEndpoint() {
    if (sending) return;
    sending = true;
    submitBtn.disabled = true;
    setStatus('Gönderiliyor…', false);
    var payload = {
      firma: fFirma.value.trim(), ad_soyad: fAd.value.trim(), eposta: fEposta.value.trim(),
      telefon: fTel.value.trim(), urun_konu: fUrun.value.trim(), adet: fAdet.value.trim(),
      aciklama: fAciklama.value.trim(), hp_web: fWeb.value, t_start: fStart.value
    };
    var ctrl = ('AbortController' in window) ? new AbortController() : null;
    var timer = setTimeout(function(){ if (ctrl) ctrl.abort(); }, 15000);
    fetch(FORM_ENDPOINT, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(payload),
      signal: ctrl ? ctrl.signal : undefined
    }).then(function(res) {
      clearTimeout(timer);
      return res.json().then(function(data) {
        return {ok2xx: res.ok, data: data};
      }, function() {
        return {ok2xx: res.ok, data: null};
      });
    }).then(function(r) {
      sending = false; submitBtn.disabled = false;
      if (r.ok2xx && r.data && r.data.ok === true) {
        setStatus('Teklif talebiniz iletildi. Ekibimiz en kısa sürede size dönüş yapacak.', false);
        form.reset();
        try { fStart.value = String(Date.now()); } catch (e) {}
      } else {
        setStatus('Talebiniz gönderilemedi. Bilgileriniz korunuyor — lütfen tekrar deneyin veya doğrudan 0224 261 05 27\\'yi arayın / info@isisah.com.tr\\'ye yazın.', true);
      }
    }).catch(function() {
      clearTimeout(timer);
      sending = false; submitBtn.disabled = false;
      setStatus('Talebiniz gönderilemedi (bağlantı/zaman aşımı). Bilgileriniz korunuyor — lütfen tekrar deneyin veya doğrudan 0224 261 05 27\\'yi arayın / info@isisah.com.tr\\'ye yazın.', true);
    });
  }

  form.addEventListener('submit', function(ev) {
    ev.preventDefault();
    if (sending) return;
    if (fWeb.value.trim() !== '') return; // bal küpü dolu → sessizce yok say
    hideErrors();
    var errs = validate();
    if (errs.length) { showErrors(errs); return; }
    if (FORM_ENDPOINT === '') composeMailto();
    else submitToEndpoint();
  });
})();
</script>
'''

BODY = (FORM_HTML
        .replace('{TEKLIF_CSS}', TEKLIF_CSS)
        .replace('{FORM_ENDPOINT_JS}', json.dumps(FORM_ENDPOINT))
        .replace('{URUN_MAP_JS}', URUN_MAP_JS)
        .replace('{KONU_MAP_JS}', KONU_MAP_JS))

LD = ('[{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":['
      '{"@type":"ListItem","position":1,"name":"Ana Sayfa","item":"https://isisah.com.tr/"},'
      '{"@type":"ListItem","position":2,"name":"Teklif Al","item":"https://isisah.com.tr/teklif.html"}]}]')

VIS = ('<img src="assets/img/uretim-k1.webp" alt="Robotlu üretim hücresi — ISIŞAH GROUP" '
       'width="1200" height="675" loading="eager"><span class="tag">ISIŞAH GROUP · DOSAB Bursa</span>')

(ROOT/'teklif.html').write_text(page(
    'teklif.html',
    'Teklif Al — Rezistans, Eşanjör, Paslanmaz Boru | ISIŞAH GROUP',
    'ISIŞAH GROUP\'tan ürün veya proje teklifi isteyin: firma, iletişim ve ihtiyaç bilgilerinizi kısaca iletin, ekibimiz size dönüş yapsın.',
    'ISIŞAH GROUP · Teklif', 'Teklif Al.',
    'Ürününüzü veya projenizi kısaca anlatın — firma, iletişim ve ihtiyaç bilgileriniz ekibimize gitsin, size dönüş yapalım.',
    BODY, LD, VIS,
), encoding='utf-8')

print('teklif.html', (ROOT/'teklif.html').stat().st_size // 1024, 'KB |', len(URUN_MAP), 'ürün |', len(KONU_MAP), 'konu anahtarı')
