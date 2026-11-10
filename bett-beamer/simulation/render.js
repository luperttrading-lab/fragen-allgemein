// Standbilder aus der Simulation: node render.js <ausgabeordner> name=query ...
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
(async () => {
  const out = process.argv[2];
  const jobs = process.argv.slice(3).map(a => { const i = a.indexOf('='); return [a.slice(0, i), a.slice(i + 1)]; });
  const b = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const ctx = await b.newContext({ viewport: { width: 1400, height: 875 }, deviceScaleFactor: Number(process.env.DSF || 1) });
  for (const [name, query] of jobs) {
    const page = await ctx.newPage();
    page.on('pageerror', e => console.log('FEHLER:', e.message));
    const url = 'file://' + path.resolve(__dirname, 'dist/index.html') + '?ui=0&shot=1&' + query.replace(/,/g, '&');
    const t0 = Date.now();
    await page.goto(url, { timeout: 280000 });
    await page.waitForFunction(() => window.__ready === true, null, { timeout: 280000, polling: 500 });
    const data = await page.evaluate(() => document.getElementById('c').toDataURL('image/jpeg', 0.9));
    fs.writeFileSync(path.join(out, name + '.jpg'), Buffer.from(data.split(',')[1], 'base64'));
    console.log('ok', name, ((Date.now() - t0) / 1000).toFixed(1) + ' s');
    await page.close();
  }
  await b.close();
})().catch(e => { console.log('ABBRUCH', e.message.split('\n')[0]); process.exit(1); });
