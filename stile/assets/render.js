// Rendert eine HTML-Datei als Hochformat-Infografik in Gemini-Größe: 1536 x 2752 px (9:16, "2K").
// Aufruf: NODE_PATH=$(npm root -g) node render.js <datei.html> <ausgabe.png>
const { chromium } = require('playwright');
const path = require('path');
const [html, png] = process.argv.slice(2);
const W = 768, H = 1376, DPR = 2;

(async () => {
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const page = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: DPR });
  await page.goto('file://' + path.resolve(html));
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(300);
  const info = await page.evaluate(([W, H]) => {
    const d = document.documentElement;
    const over = [];
    for (const el of document.querySelectorAll('body *')) {
      const r = el.getBoundingClientRect();
      if (r.width && (r.right > W + 1 || r.bottom > H + 1)) over.push(el.tagName + '.' + (el.className || '') + ' ' + Math.round(r.right) + 'x' + Math.round(r.bottom));
      if (el.scrollHeight > el.clientHeight + 2 && getComputedStyle(el).overflow === 'hidden') over.push('ABGESCHNITTEN ' + el.tagName + '.' + el.className);
    }
    return { scrollW: d.scrollWidth, scrollH: d.scrollHeight, over: over.slice(0, 12) };
  }, [W, H]);
  if (info.scrollW > W || info.scrollH > H || info.over.length) console.log('WARNUNG Überlauf:', JSON.stringify(info));
  await page.screenshot({ path: png, clip: { x: 0, y: 0, width: W, height: H } });
  console.log('ok', png, (W * DPR) + 'x' + (H * DPR));
  await browser.close();
})();
