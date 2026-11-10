// Filmbilder rendern: node film.js <ordner> <fps> <breite> <hoehe> [von] [bis]
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
(async () => {
  const [out, fps, w, h, von, bis] = process.argv.slice(2);
  fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const page = await b.newPage({ viewport: { width: Number(w), height: Number(h) } });
  page.on('pageerror', e => console.log('FEHLER', e.message));
  await page.goto('file://' + path.resolve(__dirname, 'dist/index.html') + '?ui=0&shot=1&variant=C&view=detail', { timeout: 280000 });
  await page.waitForFunction(() => window.__ready === true, null, { timeout: 280000, polling: 500 });
  const dauer = await page.evaluate(() => window.__filmDauer), n = Math.round(dauer * fps);
  const i0 = Number(von || 0), i1 = Math.min(n, Number(bis || n));
  const t0 = Date.now();
  for (let i = i0; i < i1; i++) {
    const data = await page.evaluate(t => { window.__filmZeit(t); return document.getElementById('c').toDataURL('image/jpeg', 0.92); }, i / fps);
    fs.writeFileSync(path.join(out, `f${String(i).padStart(4, '0')}.jpg`), Buffer.from(data.split(',')[1], 'base64'));
    if (i % 25 === 0) console.log('Bild', i, '/', n, ((Date.now() - t0) / 1000 / (i - i0 + 1)).toFixed(2), 's/Bild');
  }
  fs.writeFileSync(path.join(out, `texte_${i0}.json`), JSON.stringify(await page.evaluate(() => window.__filmText)));
  console.log('FERTIG', i0, i1);
  await b.close();
})().catch(e => { console.log('ABBRUCH', e.message.split('\n')[0]); process.exit(1); });
