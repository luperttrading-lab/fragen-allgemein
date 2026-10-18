const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const page = await browser.newPage({ viewport: { width: 768, height: 1376 }, deviceScaleFactor: 1 });
  await page.goto('file://' + path.resolve(process.argv[2]));
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(300);
  const r = await page.evaluate(() => {
    const q = s => [...document.querySelectorAll(s)].map(e => { const r = e.getBoundingClientRect(); return (e.id||e.className.baseVal||e.className) + ' ' + [r.left, r.top, r.right, r.bottom].map(Math.round).join(','); });
    return { header: q('header'), panels: q('.panel'), caps: q('.cap'), footer: q('footer'), sheet: q('.sheet'), pics: q('.pic'), cnodes: q('.cnode'), cc: q('.ccenter'), bubs: q('.pic .bub, .pic .narr, .pic .tagw, .pic .lab, .neqb'), chips: q('.chip'), h2: q('h2') };
  });
  for (const k in r) console.log(k, JSON.stringify(r[k]));
  await browser.close();
})();
