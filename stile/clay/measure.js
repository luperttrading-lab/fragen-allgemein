const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const page = await browser.newPage({ viewport: { width: 768, height: 1376 }, deviceScaleFactor: 1 });
  await page.goto('file://' + path.resolve(process.argv[2]));
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(200);
  const r = await page.evaluate(() => [...document.querySelectorAll('.card')].map(c => {
    const cr = c.getBoundingClientRect(); let maxB = 0, maxR = 0;
    c.querySelectorAll('*').forEach(e => { if (e.closest('svg') && e.tagName !== 'svg') return; const r = e.getBoundingClientRect(); if (r.width) { maxB = Math.max(maxB, r.bottom); maxR = Math.max(maxR, r.right); } });
    return (c.querySelector('h2,div')?.textContent.trim().slice(0, 22)) + ` top ${cr.top} bottom ${cr.bottom} contentBottom ${Math.round(maxB)} (Rest ${Math.round(cr.bottom - maxB)}) right ${cr.right} contentRight ${Math.round(maxR)}`;
  }));
  console.log(r.join('\n'));
  await browser.close();
})();
