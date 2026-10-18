const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const page = await browser.newPage({ viewport: { width: 768, height: 1376 } });
  await page.goto('file://' + path.resolve(process.argv[2] || 'professional.html'));
  await page.evaluate(() => document.fonts.ready);
  await page.addStyleTag({content: '.grid{grid-template-rows:auto auto auto auto !important;height:auto !important;align-items:start} .panel>*{flex-shrink:0 !important} .panel .merk2,.panel .merk,.panel .cyc{margin-top:10px !important} .pfc{flex:none !important}'});
  const r = await page.evaluate(() => [...document.querySelectorAll('.panel')].map((p,i)=>`${i+1}: ${Math.round(p.getBoundingClientRect().height)}`).join('  '));
  console.log('natürliche Höhen:', r);
  await browser.close();
})();
