// Misst Boxen von Elementen mit [data-m] und zaehlt Zeilen
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const p = await b.newPage({ viewport: { width: 768, height: 1376 }, deviceScaleFactor: 1 });
  await p.goto('file://' + path.resolve(process.argv[2]));
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(200);
  const r = await p.evaluate(() => [...document.querySelectorAll('[data-m]')].map(e => {
    const r = e.getBoundingClientRect();
    const lh = parseFloat(getComputedStyle(e).lineHeight) || 1;
    return e.dataset.m + ': x' + Math.round(r.left) + ' y' + Math.round(r.top) + ' w' + Math.round(r.width) + ' h' + Math.round(r.height) + ' bottom' + Math.round(r.bottom) + ' lines~' + (r.height / lh).toFixed(1);
  }));
  console.log(r.join('\n'));
  await b.close();
})();
