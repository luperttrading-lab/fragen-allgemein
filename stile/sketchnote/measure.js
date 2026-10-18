// Hilfsskript: lädt HTML, führt window.__measure() aus und gibt JSON aus
const { chromium } = require('playwright');
const path = require('path');
const [html] = process.argv.slice(2);
(async () => {
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const page = await browser.newPage({ viewport: { width: 768, height: 1376 }, deviceScaleFactor: 1 });
  page.on('console', m => console.log('console:', m.text()));
  page.on('pageerror', e => console.log('PAGEERROR:', e.message));
  await page.goto('file://' + path.resolve(html));
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(400);
  const out = await page.evaluate(() => window.__measure ? window.__measure() : null);
  console.log(JSON.stringify(out, null, 1));
  await browser.close();
})();
