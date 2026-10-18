const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const page = await browser.newPage({ viewport: { width: 768, height: 1376 }, deviceScaleFactor: 2 });
  await page.setContent(`<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="file://${path.resolve(__dirname,'../assets/fonts.css')}"></head><body><span id="m" style="white-space:nowrap;position:absolute"></span></body></html>`);
  await page.waitForTimeout(200);
  const tests = [
    ["700 34px Roboto", "ADHS im Gehirn: Kein Willensproblem,"],
    ["700 34px Roboto", "sondern ein Steuerungsproblem"],
    ["700 36px Roboto", "ADHS im Gehirn: Kein Willensproblem,"],
    ["700 42px Roboto", "ADHS im Gehirn: Warum es"],
    ["700 26px 'Roboto Condensed'", "DIE NEUROBIOLOGISCHE"],
    ["700 20px 'Roboto Condensed'", "KEIN MANGEL AN WILLE"],
    ["700 20px 'Roboto Condensed'", "DAS AUFMERKSAMKEITS-"],
    ["700 20px 'Roboto Condensed'", "VERÄNDERTES DOPAMIN-"],
    ["700 20px 'Roboto Condensed'", "& NORADRENALINSYSTEM"],
    ["400 16px 'Roboto Condensed'", "ADHS bedeutet nicht, grundsätzlich zu wenig Aufmerksamkeit oder Disziplin zu haben. Es"],
    ["400 16px 'Roboto Condensed'", "Das Problem ist nicht das"],
    ["700 13px 'Roboto Condensed'", "Fazit: ADHS heißt nicht „keine Aufmerksamkeit“ – Aufmerksamkeit, Motivation und Verhalten zuverlässig an das Nötige anzupassen, fällt schwer."],
    ["400 13px 'Roboto Condensed'", "Fazit: ADHS heißt nicht „keine Aufmerksamkeit“ – Aufmerksamkeit, Motivation und Verhalten zuverlässig an das Nötige anzupassen, fällt schwer."],
    ["400 14px 'Roboto Condensed'", "ADHS heißt nicht „keine Aufmerksamkeit“. Es heißt: Aufmerksamkeit, Motivation und Verhalten zuverlässig an das anzupassen, was gerade nötig ist, fällt schwer."],
    ["400 11px 'Roboto Condensed'", "Quelle: NeuroWissen TV, „NEUROLOGE ERKLÄRT: Das macht ADHS wirklich in deinem Gehirn“ (2026)"],
    ["700 10px 'Roboto Condensed'", "ERLEICHTERUNG"],
    ["700 10px 'Roboto Condensed'", "ABLENKUNG AUSBLENDEN"],
    ["700 11px 'Roboto Condensed'", "ARBEITSGEDÄCHTNIS"],
  ];
  for (const [font, txt] of tests) {
    const w = await page.evaluate(([f,t]) => { const m=document.getElementById('m'); m.style.font=f; m.textContent=t; return m.getBoundingClientRect().width; }, [font, txt]);
    console.log(w.toFixed(1).padStart(7), '|', font, '|', txt.slice(0,50));
  }
  await browser.close();
})();
