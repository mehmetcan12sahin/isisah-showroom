// Canlı duman testi — tarayıcı katmanı: 3 sayfayı headless açar,
// konsol hatalarını toplar, sayfa-özel canlılık kontrolleri yapar.
// Kullanım: node tools/smoke-browser.mjs [taban_url] [showroom_öneki]
//   canlı:  node tools/smoke-browser.mjs                         (https://isisah.com.tr, /showroom)
//   yerel:  node tools/smoke-browser.mjs http://localhost:8080 ''  (depo kökü düz topoloji)
import { createRequire } from 'module';
const require = createRequire(import.meta.url);
const { chromium } = require(process.env.HOME + '/.isisah-smoke/node_modules/playwright');

const BASE = process.argv[2] || 'https://isisah.com.tr';
const SR = process.argv[3] ?? '/showroom';
const results = [];
let fail = 0;

const browser = await chromium.launch();
const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 } });

async function check(path, name, probe) {
  const page = await ctx.newPage();
  const errors = [];
  page.on('console', m => { if (m.type() === 'error') errors.push(m.text().slice(0, 160)); });
  page.on('pageerror', e => errors.push(('PAGEERROR: ' + e.message).slice(0, 160)));
  try {
    const resp = await page.goto(BASE + path, { waitUntil: 'domcontentloaded', timeout: 45000 });
    if (!resp || resp.status() >= 400) throw new Error('HTTP ' + (resp && resp.status()));
    const extra = await probe(page);
    // font/analytics dışı gerçek hataları say
    const real = errors.filter(e => !/googleapis|gstatic|favicon/.test(e));
    const ok = real.length === 0 && !extra.startsWith('FAIL');
    if (!ok) fail++;
    results.push(`${ok ? 'OK  ' : 'FAIL'} ${name} — ${extra}${real.length ? ' | konsol: ' + real.join(' ;; ') : ''}`);
  } catch (e) {
    fail++; results.push(`FAIL ${name} — ${e.message.slice(0, 120)}`);
  }
  await page.close();
}

await check('/', 'ana sayfa', async p => {
  const wc = await p.locator('.wcard').count();
  const tour = await p.locator('.tourbox').count();
  const cta = await p.locator('.hero a[href^="teklif.html"]').count();
  const navq = await p.locator('#links a[href^="teklif.html"]').count();
  const main = await p.locator('main#main').count();
  return (wc >= 4 && tour === 1 && cta >= 1 && navq >= 1 && main === 1)
    ? `wcard=${wc} tourbox=${tour} hero-teklif=${cta} nav-teklif=${navq}`
    : `FAIL beklenen bölümler eksik (wcard=${wc} tourbox=${tour} hero-teklif=${cta} nav-teklif=${navq} main=${main})`;
});

await check('/teklif.html?urun=kangal', 'teklif formu', async p => {
  const form = await p.locator('form').count();
  const hp = await p.locator('#fWeb').count();
  const pre = await p.evaluate(() => [...document.querySelectorAll('textarea,input,select')].some(e => /kangal/i.test(e.value || '')));
  return (form >= 1 && hp === 1) ? `form=${form} honeypot=ok onDoldurma=${pre}` : `FAIL form=${form} honeypot=${hp}`;
});

await check(SR + '/urunler.html', 'showroom', async p => {
  // kapı tıklaması YOK (ses protokolü) — yalnız lobinin kurulduğunu doğrula
  await p.waitForSelector('body.ready', { timeout: 30000 });
  const doors = await p.locator('.doorcard').count();
  const canvasOk = await p.evaluate(() => !!document.querySelector('canvas'));
  return (doors === 3 && canvasOk) ? `kapı=3 canvas=ok` : `FAIL kapı=${doors} canvas=${canvasOk}`;
});

await check(SR + '/fabrika.html', 'fabrika turu', async p => {
  await p.waitForFunction(() => {
    const v = document.getElementById('film');
    return v && v.duration > 0;
  }, { timeout: 60000 });
  const dur = await p.evaluate(() => document.getElementById('film').duration.toFixed(1));
  const caps = await p.locator('.cap').count();
  // 52.08 sn = kırpılmış film (52.17 = eski, son 2 karede eski çalışan) — üst sınır bilinçli
  return (+dur > 20 && +dur < 52.15 && caps === 7) ? `film=${dur}sn başlık=7` : `FAIL film=${dur} (beklenen ≤52.1) başlık=${caps}`;
});

await browser.close();
console.log(results.join('\n'));
process.exit(fail ? 1 : 0);
