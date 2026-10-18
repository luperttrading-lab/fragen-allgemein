const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const page = await browser.newPage({ viewport: { width: 768, height: 1376 }, deviceScaleFactor: 2 });
  await page.setContent(`<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="file://${path.resolve(__dirname,'../assets/fonts.css')}"></head><body><span id="m" style="white-space:nowrap;position:absolute;font-family:Oswald">x</span><span style="font-family:'Roboto Condensed';font-weight:800">y</span><canvas id="c"></canvas></body></html>`);
  await page.evaluate(() => document.fonts.ready); await page.waitForTimeout(400);
  const tests = [
    ["700 20px Oswald", "DIE NEUROBIOLOGISCHE"],
    ["600 20px Oswald", "DIE NEUROBIOLOGISCHE"],
    ["500 20px Oswald", "DIE NEUROBIOLOGISCHE"],
    ["700 20px Oswald", "KEIN MANGEL AN WILLE"],
    ["700 20px Oswald", "ARBEITSGEDÄCHTNIS"],
    ["800 20px 'Roboto Condensed'", "DIE NEUROBIOLOGISCHE"],
    ["900 20px 'Roboto Condensed'", "DIE NEUROBIOLOGISCHE"],
    ["700 20px 'Roboto Condensed'", "DIE NEUROBIOLOGISCHE"],
    ["700 20px Roboto", "ADHS im Gehirn: Warum es"],
    ["400 20px 'Roboto Condensed'", "ADHS bedeutet nicht, grundsätzlich zu wenig Aufmerksamkeit oder Disziplin zu haben. Es"],
    ["400 20px Roboto", "ADHS bedeutet nicht, grundsätzlich zu wenig Aufmerksamkeit oder Disziplin zu haben. Es"],
  ];
  for (const [font, txt] of tests) {
    const r = await page.evaluate(([f,t]) => { const m=document.getElementById('m'); m.style.font=f; m.textContent=t; const w=m.getBoundingClientRect().width;
      const c=document.getElementById('c').getContext('2d'); c.font=f; const mt=c.measureText('H'); return [w, mt.actualBoundingBoxAscent, c.measureText('x').actualBoundingBoxAscent]; }, [font, txt]);
    console.log(r[0].toFixed(1).padStart(7), 'capH', r[1].toFixed(1), 'xH', r[2].toFixed(1), '|', font, '|', txt.slice(0,40));
  }
  await browser.close();
})();
