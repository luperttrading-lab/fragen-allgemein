const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const page = await browser.newPage({ viewport: { width: 768, height: 1376 }, deviceScaleFactor: 2 });
  await page.goto('file://' + path.resolve(__dirname, 'measure.html'));
  await page.evaluate(() => document.fonts.ready); await page.waitForTimeout(500);
  const tests = [
    ["700 20px Oswald", "KEIN MANGEL AN WILLE"],
    ["700 20px 'Roboto Condensed'", "KEIN MANGEL AN WILLE"],
    ["800 20px 'Roboto Condensed'", "KEIN MANGEL AN WILLE"],
    ["700 20px Oswald", "MYTHOS VS."],
    ["700 20px 'Roboto Condensed'", "MYTHOS VS."],
    ["700 20px Oswald", "ARBEITSGEDÄCHTNIS"],
    ["700 20px 'Roboto Condensed'", "ARBEITSGEDÄCHTNIS"],
    ["700 20px Roboto", "ADHS im Gehirn: Warum es"],
    ["700 20px Roboto", "ADHS im Gehirn: Kein Willensproblem,"],
    ["400 20px 'Roboto Condensed'", "ADHS bedeutet nicht, grundsätzlich zu wenig Aufmerksamkeit oder Disziplin zu haben. Es"],
    ["400 20px 'Roboto Condensed'", "Das Problem ist nicht das"],
    ["400 20px Roboto", "Das Problem ist nicht das"],
    ["400 20px 'Roboto Condensed'", "Fazit: ADHS heißt nicht „keine Aufmerksamkeit“ – Aufmerksamkeit, Motivation und Verhalten zuverlässig an das Nötige anzupassen, fällt schwer."],
    ["700 20px 'Roboto Condensed'", "Fazit: ADHS heißt nicht „keine Aufmerksamkeit“ – Aufmerksamkeit, Motivation und Verhalten zuverlässig an das Nötige anzupassen, fällt schwer."],
    ["400 20px 'Roboto Condensed'", "Quelle: NeuroWissen TV, „NEUROLOGE ERKLÄRT: Das macht ADHS wirklich in deinem Gehirn“ (2026)"],
  ];
  for (const [font, txt] of tests) {
    const r = await page.evaluate(([f,t]) => { const m=document.getElementById('m'); m.style.font=f; m.textContent=t; const w=m.getBoundingClientRect().width;
      const c=document.getElementById('c').getContext('2d'); c.font=f; const mt=c.measureText('H'); return [w, mt.actualBoundingBoxAscent, c.measureText('x').actualBoundingBoxAscent]; }, [font, txt]);
    console.log(r[0].toFixed(1).padStart(7), 'capH', r[1].toFixed(2), 'xH', r[2].toFixed(2), '|', font, '|', txt.slice(0,40));
  }
  await browser.close();
})();
