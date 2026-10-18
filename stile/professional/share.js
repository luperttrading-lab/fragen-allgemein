const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const page = await browser.newPage({ viewport: { width: 768, height: 1376 }, deviceScaleFactor: 2 });
  await page.goto('file://' + path.resolve(process.argv[2]));
  await page.evaluate(() => document.fonts.ready); await page.waitForTimeout(300);
  const r = await page.evaluate(() => {
    let area = 0, cells = new Set();
    for (const el of document.querySelectorAll('svg.abs')) {
      const b = el.getBoundingClientRect(); if (b.width >= 760) continue;
      for (let x = Math.floor(b.left/8); x < Math.ceil(b.right/8); x++) for (let y = Math.floor(b.top/8); y < Math.ceil(b.bottom/8); y++) cells.add(x+','+y);
    }
    const tcells = new Set();
    for (const el of document.querySelectorAll('h1,.intro,.col,.sub,.tx,.lab,.fazit,.quelle')) {
      const b = el.getBoundingClientRect();
      for (let x = Math.floor(b.left/8); x < Math.ceil(b.right/8); x++) for (let y = Math.floor(b.top/8); y < Math.ceil(b.bottom/8); y++) tcells.add(x+','+y);
    }
    const total = (768/8)*(1376/8);
    const words = document.body.innerText.split(/\s+/).filter(w => /[A-Za-zÄÖÜäöüß0-9]/.test(w)).length;
    const svgwords = [...document.querySelectorAll('svg text')].map(t=>t.textContent).join(' ').split(/\s+/).filter(w=>/[A-Za-zÄÖÜäöüß]/.test(w)).length;
    return {bild: (cells.size/total*100).toFixed(1)+'%', text: (tcells.size/total*100).toFixed(1)+'%', woerter_gesamt: words, davon_in_illustrationen: svgwords};
  });
  console.log(JSON.stringify(r));
  await browser.close();
})();
