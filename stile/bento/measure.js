// Prüfhilfe: meldet je Kachel Größe, Inhaltsüberlauf und Elemente, die aus der Kachel ragen.
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const page = await browser.newPage({ viewport: { width: 768, height: 1376 }, deviceScaleFactor: 1 });
  await page.goto('file://' + path.resolve(process.argv[2] || 'bento.html'));
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(200);
  const res = await page.evaluate(() => {
    const out = [];
    for (const t of document.querySelectorAll('.tile')) {
      const r = t.getBoundingClientRect();
      const cs = getComputedStyle(t);
      const pb = parseFloat(cs.paddingBottom), pr = parseFloat(cs.paddingRight);
      let maxB = 0, maxR = 0, bad = [];
      for (const el of t.querySelectorAll('*')) {
        if (el.closest('svg') && el.tagName !== 'svg') continue;
        const e = el.getBoundingClientRect();
        if (!e.width) continue;
        maxB = Math.max(maxB, e.bottom); maxR = Math.max(maxR, e.right);
        if (e.bottom > r.bottom - pb + 0.5 || e.right > r.right - pr + 0.5 || e.left < r.left + 1 || e.top < r.top + 1)
          bad.push(el.tagName + '.' + (el.className.baseVal ?? el.className) + ' b' + Math.round(e.bottom - (r.bottom - pb)) + ' r' + Math.round(e.right - (r.right - pr)));
      }
      out.push(`${t.className.padEnd(22)} ${Math.round(r.width)}x${Math.round(r.height)}  frei unten: ${Math.round(r.bottom - pb - maxB)}  ${bad.slice(0, 4).join(' | ')}`);
    }
    // Textzeilen: kleinste Schriftgröße
    let min = 99, minEl = '';
    for (const el of document.querySelectorAll('body *')) {
      if (el.closest('svg')) continue;
      const hasText = [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim());
      if (!hasText) continue;
      const fs = parseFloat(getComputedStyle(el).fontSize);
      if (fs < min) { min = fs; minEl = el.className + ' "' + el.textContent.trim().slice(0, 30) + '"'; }
    }
    out.push('kleinste Schrift: ' + min + 'px ' + minEl);
    return out;
  });
  console.log(res.join('\n'));
  await browser.close();
})();
