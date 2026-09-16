#!/usr/bin/env python3
# Kurumsal alt sayfaları (hakkimizda.html, vizyon-misyon.html) — ortak iskelet: tools/pagegen.py
# index.html'in CSS'i değişince yeniden çalıştır: python3 tools/build-pages.py
import pathlib
from pagegen import ROOT, page, ORG

# ---------------- HAKKIMIZDA ----------------
hak_body = '''
<section class="stats" style="margin-top:30px">
  <div class="wrap">
    <div class="stat reveal"><div class="n grad-text" data-count="44" data-suffix=" yıl">0 yıl</div><div class="k">Kesintisiz Üretim</div></div>
    <div class="stat reveal" data-d="1"><div class="n grad-text" data-count="3" data-suffix=" marka">0 marka</div><div class="k">Tek Çatı Altında</div></div>
    <div class="stat reveal" data-d="2"><div class="n grad-text" data-count="8">0</div><div class="k">Ürün Gamı · Mutfaktan Savunmaya</div></div>
    <div class="stat reveal" data-d="3"><div class="n grad-text" data-count="100" data-prefix="%">%0</div><div class="k">Yerli Üretim</div></div>
  </div>
</section>

<section class="pad" style="padding-top:90px">
  <div class="wrap two">
    <div class="prose reveal">
      <h2>Kuruluş ve gelişim</h2>
      <p>ISIŞAH markası, 1982 yılında çeşitli endüstri kolları için sanayi tipi rezistansların üretimini ve satışını yapmak amacıyla kurulmuştur. 1995 yılında kurduğu entegre tesis ile elektrikli ev aletleri için seri üretime başlamıştır. 2003 yılında sanayi tipi endüstriyel üretim için ayrı bir tesis oluşturulmuş; seri üretimden tamamen bağımsız, özel üretime yönelik çalışmalar yürütülmüştür.</p>
      <p>Pazarlama alanında yaptığı yeniliklerle şirketin hizmet alanı her geçen gün genişlemiş; müşterilerine daha profesyonel hizmet verebilmek için kurumsal bir yapıya dönüşme ihtiyacı doğmuştur. 2011 yılı itibariyle ISIŞAH GROUP çatısı altında yeniden yapılanan grup, bugün <b>ISIŞAH ENDÜSTRİYEL</b> (sanayi tipi rezistans ve ısıtma sistemleri), <b>BORŞAH BORU</b> (paslanmaz çelik boru) ve <b>SALMEX</b> (ısı eşanjörleri) markalarıyla üretim yapmaktadır.</p>
      <p>Türkiye'de sektörünün en büyük firmalarından biri olarak ISIŞAH, 44 yılın verdiği güç ve tecrübeyle elektrikli ev aletlerine yönelik ve çeşitli endüstri grupları için ısıtma sistemlerini ISO 9001:2015 kalite yönetim sistemi altında üretmeyi kendine prensip edinmiştir.</p>
      <div class="badges">
        <span>Kuruluş<b>1982</b></span><span>Merkez<b>DOSAB · Bursa</b></span><span>Kalite<b>ISO 9001:2015</b></span><span>Marka<b>3</b></span>
      </div>
    </div>
    <div class="reveal" data-d="2">
      <h2 style="font-size:1.6rem;margin-bottom:10px">Tarihçe</h2>
      <div class="about" style="display:block"><div class="time">
        <div class="row"><span class="yr">1982</span><span class="tx">Sanayi tipi rezistans üretimi için kuruluş.</span></div>
        <div class="row"><span class="yr">1986</span><span class="tx">İlk demiryolu projesi: TÜVASAŞ yolcu vagonu ısıtma üniteleri.</span></div>
        <div class="row"><span class="yr">1988</span><span class="tx">TSE — Türk Standartlarına Uygunluk Belgesi.</span></div>
        <div class="row"><span class="yr">1995</span><span class="tx">Entegre tesis; elektrikli ev aletleri için seri üretime geçiş.</span></div>
        <div class="row"><span class="yr">1997</span><span class="tx">VDE — DIN EN normlarına uygunluk sertifikaları (Almanya).</span></div>
        <div class="row"><span class="yr">2003</span><span class="tx">Sanayi tipi özel üretim için ayrı tesis.</span></div>
        <div class="row"><span class="yr">2004</span><span class="tx">TS EN ISO 9001 kalite sistem belgesi.</span></div>
        <div class="row"><span class="yr">2010</span><span class="tx">UL — ABD standartlarına uygunluk sertifikası.</span></div>
        <div class="row"><span class="yr">2011</span><span class="tx">ISIŞAH GROUP çatısı altında yeniden yapılanma.</span></div>
      </div></div>
    </div>
  </div>
</section>

<section class="pad" style="padding-top:0">
  <div class="wrap">
    <div class="sec-head reveal"><h2>Üretimden kareler.</h2><p>DOSAB Bursa tesislerimizden — robotlu eşanjör hattı, profil hattı ve test istasyonu.</p></div>
    <div class="kareler reveal">
      <figure><img src="assets/img/uretim-k1.webp" alt="Robotlu üretim hücresi" loading="lazy" decoding="async"><figcaption>Robotlu Hat</figcaption></figure>
      <figure><img src="assets/img/uretim-k2.webp" alt="Profil şekillendirme hattı" loading="lazy" decoding="async"><figcaption>Şekillendirme</figcaption></figure>
      <figure><img src="assets/img/uretim-k3.webp" alt="Sızdırmazlık test istasyonu" loading="lazy" decoding="async"><figcaption>Test İstasyonu</figcaption></figure>
    </div>
    <div class="pgcta reveal" style="margin-top:22px"><a class="btn ghost" href="fabrika.html">Fabrika turuna çık <span>→</span></a></div>
  </div>
</section>

<section class="pad" style="padding-top:0">
  <div class="wrap">
    <div class="two">
      <div class="prose reveal">
        <h2>Yönetimden</h2>
        <p>ISIŞAH A.Ş., 1982 yılında çeşitli endüstri kolları için sanayi tipi rezistansların üretimini ve pazarlamasını yapmak için kurulmuştur. Üretim ve pazarlama faaliyetleri alanında yapılan değişiklikler şirketin aktivite alanını genişletmiş, sektördeki iddiasını ve gücünü artırmıştır.</p>
        <div class="quote">Şirketimiz bugün sahip olduğu gücünü kalite sisteminin varlığına, sektördeki tecrübe ve birikimine, yerel sermaye ile kurulmuş en büyük ve gelişmiş firma olmasına, müşterilerimizde oluşmuş marka güvenine, insan ve sisteme dayalı düşünce yapımıza, köklü geçmişimize, piyasadaki itibarımıza, yüksek kaliteli makine parkımıza, gelişmiş altyapı ve donanımımıza borçludur.
          <footer>Mehmet Şahin — Yönetim Kurulu Başkanı</footer></div>
      </div>
      <div class="prose reveal" data-d="2">
        <h2>İnovasyon ve Ar-Ge</h2>
        <p><b>Tasarım politikamız:</b> İnovasyon (sürekli değişim) felsefesi benimsenmiş olup, genç ve dinamik tasarım ekibiyle gerek mevcut trendleri takip ederek gerekse kendi trendini oluşturarak müşterilerin ihtiyaç ve beklentilerini karşılayacak özgün, fonksiyonel modeller tasarlamak; tasarımlarıyla takip edilen ve gelecek trendleri belirleyen marka olmak.</p>
        <p><b>Ar-Ge politikamız:</b></p>
        <ul>
          <li>Hedef müşteri kitlesine uygun modelleri CAD sistemiyle optimum şekilde üretime hazırlamak.</li>
          <li>Müşterilerden gelen istek ve talepleri, teknik ekibimizle sahada sistem analizi yaparak çözüme dönüştürmek.</li>
          <li>Üretim ve tedarikçi zincirleriyle güçlü bir bağ kurarak dinamik bir yapıya sahip olmak.</li>
          <li>İnovatif yaklaşımlar ve öneri sistemiyle üretilmekte olan ürünleri sürekli geliştirmek.</li>
          <li>ERP sistemiyle üretimin teknik altyapıyla ilişkisini güçlendirmek.</li>
          <li>Kalite, Çevre, İş Sağlığı ve Güvenliği politikalarıyla eşgüdümlü çalışmak.</li>
        </ul>
        <p><b>Ar-Ge çalışmaları:</b> Türkiye'de ilk defa mobil elektrikli ısıtma ünitelerinde patentli ürünler üretilmiştir. Türkiye'de ilk defa yerli imalat olarak patentli infrared teknolojili oto boya kurutma ünitesi (BOYKUR) üretilmiştir.</p>
      </div>
    </div>
  </div>
</section>

<section class="pad" style="padding-top:0">
  <div class="wrap">
    <div class="sec-head reveal"><h2>Belgelerimiz.</h2><p>ISIŞAH GROUP, 2004\'ten bu yana ISO 9001 (bugün TS EN ISO 9001:2015) kalite yönetim sistemi belgesine; ürünlerinde TSE (1988), VDE / DIN EN (Almanya, 1997), UL (ABD, 2010) ve CE (EN 60204-1) uygunluk belgelerine sahiptir ve RoHS uyumlu malzeme kullanır.</p></div>
    <div class="railcols reveal" style="margin-top:0">
      <div class="railbox"><h3>Sistem standardı</h3><ul>
        <li>TS EN ISO 9001:2015 Kalite Yönetim Sistemi (ISO 9001 belgeli: 2004'ten beri)</li>
        <li>Entegre Kalite, Çevre ve İş Sağlığı-Güvenliği yönetim sistemi politikası</li>
      </ul></div>
      <div class="railbox"><h3>Ürün standardı</h3><ul>
        <li>TSE — Türk Standartlarına Uygunluk Belgesi (1988'den beri)</li>
        <li>CE — Avrupa Birliği uygunluğu; EN 60204-1 uygunluk</li>
        <li>VDE — DIN EN normlarına uygunluk sertifikaları, Almanya (1997'den beri)</li>
        <li>UL — ABD UL standartlarına uygunluk sertifikası (2010'dan beri)</li>
        <li>RoHS uyumlu malzeme kullanımı</li>
      </ul></div>
    </div>
    <div class="pgcta reveal">
      <a class="btn" href="vizyon-misyon.html">Vizyonumuz &amp; Misyonumuz <span>→</span></a>
      <a class="btn ghost" href="urunler.html">3B Showroom</a>
      <a class="btn ghost" href="fabrika.html">Fabrika Turu</a>
      <a class="btn ghost" href="index.html#iletisim">İletişim</a>
    </div>
  </div>
</section>
'''
hak_ld = '{"@context":"https://schema.org","@type":"AboutPage","name":"Hakkımızda — ISIŞAH GROUP","url":"https://isisah.com.tr/hakkimizda.html","mainEntity":'+ORG+'}'
(ROOT/'hakkimizda.html').write_text(page('hakkimizda.html',
    'Hakkımızda: 1982\'den Bugüne Bursa\'da Isıtma Üretimi | ISIŞAH',
    'ISIŞAH GROUP: 1982 kuruluş, 1995 entegre tesis, 2011 grup yapısı. Rezistans, paslanmaz boru ve eşanjör markaları; TSE, VDE, UL ve ISO 9001:2015 belgeleri.',
    'ISIŞAH GROUP · 1982\'den bugüne', 'Hakkımızda.',
    'Bursa DOSAB\'da sanayi tipi rezistanstan paslanmaz çelik boruya ve ısı eşanjörlerine uzanan üç marka, tek çatı: 44 yıllık mühendislik birikimi.',
    hak_body, hak_ld,
    '<img src="assets/img/bina-gece-3marka.webp" alt="ISIŞAH GROUP merkez binası — üç marka, DOSAB Bursa" width="1600" height="905" fetchpriority="high"><span class="tag">ISIŞAH GROUP · DOSAB Bursa</span>'), encoding='utf-8')

# ---------------- VİZYON & MİSYON ----------------
viz_body = '''
<section class="pad" style="padding-top:40px">
  <div class="wrap two">
    <div class="vmbox reveal" style="--bc:var(--emb1)">
      <span class="k">Vizyonumuz</span>
      <h2>Zirvede, güvenilir, global.</h2>
      <p>Müşterilerimizi, çalışanlarımızı ve bayilerimizi her daim memnun ve mutluluğa ulaştıran; kaliteden ödün vermeden zirvede, güvenilir ve lider global şirket olmak.</p>
    </div>
    <div class="vmbox reveal" data-d="2" style="--bc:var(--ele1)">
      <span class="k">Misyonumuz</span>
      <h2>Müşterimize ortağımız gibi.</h2>
      <p>Türkiye'de sektörünün en büyük firmalarından biri olarak ISIŞAH, 44 yılın verdiği güç ve tecrübeyle elektrikli ev aletlerine yönelik ve çeşitli endüstri grupları için ısıtma sistemlerinin ISO 9001 kalite standardında üretimini kendine prensip edinmiştir. Müşterilerimize şirket ortağımız gibi davranmak ve kıymetli müşterilerimiz için değer yaratmak misyonumuzdur.</p>
    </div>
  </div>
</section>

<section class="pad" style="padding-top:0">
  <div class="wrap">
    <div class="sec-head reveal"><h2>Üç marka, tek vizyon.</h2><p>Aynı çatı, aynı kalite disiplini.</p></div>
    <div class="logorow reveal">
      <a data-b="isisah" href="index.html#marka=isisah"><img src="assets/catalog/logo-isisah.webp" alt="ISIŞAH ENDÜSTRİYEL"><span>Rezistans &amp; Isıtma Sistemleri</span></a>
      <a data-b="borsah" href="index.html#marka=borsah"><img src="assets/catalog/logo-borsah.webp" alt="BORŞAH BORU"><span>Paslanmaz Çelik Boru</span></a>
      <a data-b="salmex" href="index.html#marka=salmex"><img src="assets/catalog/logo-salmex.webp" alt="SALMEX"><span>Isı Eşanjörleri</span></a>
    </div>
  </div>
</section>

<section class="pad" style="padding-top:0">
  <div class="wrap">
    <div class="prose reveal" style="max-width:900px;margin:0 auto">
      <h2>Kalite, İSG ve Çevre Politikamız</h2>
      <p>Müşteri kalite beklentilerini algılayan, değer zincirindeki tüm ürün ve süreçlerini bu doğrultuda sürekli geliştiren lider bir şirket olmayı hedefleriz. Bu amaçla;</p>
      <ul>
        <li>İnsan odaklı bir yaklaşımla çalışanlarımızı geliştirir; yapılan her faaliyette kalite bilincini ve sorgulayıcı bakış açısını dikkate alan şirket kültürünü benimseriz.</li>
        <li>Tüm değer zincirindeki standartların dünya klasında olması için rekabetçilik hedefiyle sürekli gelişim sağlarız.</li>
        <li>Yeniliklere açık oluruz; her noktada sürekli iyileşmeyi ve mükemmel olanı üretmeyi hedefleriz.</li>
        <li>Tüm üretim ve hizmet aşamalarımızda çevre kirliliğinin önlenmesini izler; sürdürülebilir doğal kaynak kullanımını ve çevresel performansımızı geliştiririz.</li>
        <li>Firmamızda müşteri, ziyaretçi ve tüm çalışanların iş sağlığı ve güvenliğini sağlarız.</li>
        <li>Sürekli müşteri memnuniyetini tam zamanında hizmet ve teknolojik üretimle artırırız.</li>
        <li>Sürekli iyileştirme kapsamında çalışanların gelişimi, çevre bilincinin artırılması ve iş sağlığı-güvenliğinin sağlanması için eğitimler düzenleriz.</li>
        <li>Süreçlerimizde ISO 9001 kalite yönetim sistemine ve sektörümüze uygun tüm yasal standartlara, iş sağlığı-güvenliği ve çevre mevzuatına uyarız.</li>
        <li>Sürdürülebilir, yalın ve proaktif bir şekilde Entegre Kalite, Çevre ve İş Sağlığı-Güvenliği yönetim sistemine tüm personelin katılımını sağlar; etkinliğini izler ve sürekli iyileştiririz.</li>
      </ul>
      <div class="quote">ISIŞAH GROUP bu politikanın tüm çalışanlarına iletileceğini ve anlaşılmasını sağlayacağını taahhüt eder.
        <footer>Mehmet Şahin — Genel Müdür</footer></div>
      <div class="pgcta">
        <a class="btn" href="hakkimizda.html">Hakkımızda <span>→</span></a>
        <a class="btn ghost" href="urunler.html">3B Showroom</a>
        <a class="btn ghost" href="index.html#iletisim">İletişim</a>
      </div>
    </div>
  </div>
</section>
'''
viz_ld = '{"@context":"https://schema.org","@type":"WebPage","name":"Vizyonumuz ve Misyonumuz — ISIŞAH GROUP","url":"https://isisah.com.tr/vizyon-misyon.html","about":'+ORG+'}'
(ROOT/'vizyon-misyon.html').write_text(page('vizyon-misyon.html',
    'Vizyon, Misyon ve Kalite Politikası | ISIŞAH GROUP Bursa',
    'ISIŞAH GROUP vizyonu, misyonu ve Kalite-İSG-Çevre politikası: rezistans, paslanmaz boru ve ısı eşanjörü üretiminde ISO 9001 disiplini, güvenilir şirket.',
    'ISIŞAH GROUP · Kurumsal', 'Vizyonumuz &amp;<br>Misyonumuz.',
    'Kaliteden ödün vermeden, müşterimize şirket ortağımız gibi davranarak.',
    viz_body, viz_ld,
    '<img src="assets/img/salmex-hat.webp" alt="SALMEX robotlu eşanjör üretim hattı" loading="eager"><span class="tag">DOSAB Bursa · Robotlu Hat</span>'), encoding='utf-8')
print('hakkimizda.html', (ROOT/'hakkimizda.html').stat().st_size//1024, 'KB |', 'vizyon-misyon.html', (ROOT/'vizyon-misyon.html').stat().st_size//1024, 'KB')
