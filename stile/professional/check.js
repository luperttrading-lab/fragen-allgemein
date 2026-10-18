// prüft Textbreiten/Überläufe einzelner Blöcke
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const page = await browser.newPage({ viewport: { width: 768, height: 1376 }, deviceScaleFactor: 2 });
  await page.goto('file://' + path.resolve(process.argv[2]));
  await page.evaluate(() => document.fonts.ready); await page.waitForTimeout(300);
  const r = await page.evaluate(() => {
    const out = [];
    for (const el of document.querySelectorAll('h1,.intro,.col,.sub,.tx,.lab,.fazit,.quelle')) {
      const b = el.getBoundingClientRect();
      out.push(`${el.className||el.tagName} x${Math.round(b.left)}-${Math.round(b.right)} y${Math.round(b.top)}-${Math.round(b.bottom)} sw=${el.scrollWidth} ${el.textContent.slice(0,28)}`);
    }
    // SVG-Texte, die über ihr SVG hinausragen
    for (const t of document.querySelectorAll('svg text')) {
      const b = t.getBoundingClientRect(); const s = t.ownerSVGElement.getBoundingClientRect();
      if (b.right > s.right + 0.5 || b.left < s.left - 0.5 || b.bottom > s.bottom + 0.5) out.push(`SVG-TEXT ÜBER RAND: ${t.textContent} ${Math.round(b.left)}-${Math.round(b.right)} / svg ${Math.round(s.left)}-${Math.round(s.right)} y${Math.round(b.bottom)}/${Math.round(s.bottom)}`);
    }
    const words = document.body.innerText.split(/\s+/).filter(w => /[A-Za-zÄÖÜäöüß0-9]/.test(w)).length;
    out.push('WÖRTER: ' + words);
    return out;
  });
  console.log(r.join('\n'));
  await browser.close();
})();
