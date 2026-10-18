const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const page = await browser.newPage({ viewport: { width: 768, height: 1376 } });
  await page.goto('file://' + path.resolve('professional.html'));
  await page.evaluate(() => document.fonts.ready);
  const r = await page.evaluate(() => {
    const out = [];
    document.querySelectorAll('.panel').forEach((p, i) => {
      // natural content height: sum of children
      let need = 0; const cs = getComputedStyle(p);
      const kids = [...p.children];
      const first = kids[0].getBoundingClientRect(), last = kids[kids.length-1].getBoundingClientRect();
      out.push(`panel ${i+1}: h=${Math.round(p.clientHeight)} scroll=${p.scrollHeight} lastBottom=${Math.round(last.bottom - p.getBoundingClientRect().top)}`);
    });
    const c = document.createElement('canvas').getContext('2d');
    const m = (f, t) => { c.font = f; return Math.round(c.measureText(t).width); };
    out.push('neuro 600 16.5: ' + m("600 16.5px 'Source Sans 3'", 'neuroentwicklungs-'));
    out.push('neuro 600 15.5: ' + m("600 15.5px 'Source Sans 3'", 'neuroentwicklungs-'));
    out.push('neuro 400 16: ' + m("400 16px 'Source Sans 3'", 'neuroentwicklungs-'));
    out.push('undiszipliniert, 400 16: ' + m("400 16px 'Source Sans 3'", 'undiszipliniert,'));
    out.push('Selbststeuerung. 600 16: ' + m("600 16px 'Source Sans 3'", 'Selbststeuerung.'));
    out.push('Unmittelbare Konsequenzen 600 15: ' + m("600 15px 'Source Sans 3'", 'Unmittelbare Konsequenzen'));
    out.push('Aufm steuern: schwierig: ' + (m("700 15px 'Source Sans 3'", 'Aufmerksamkeit steuern:')+m("400 15px 'Source Sans 3'", ' schwierig.')));
    out.push('real col: ' + Math.round(document.querySelector('.real').getBoundingClientRect().width));
    return out.join('\n');
  });
  console.log(r);
  await browser.close();
})();
