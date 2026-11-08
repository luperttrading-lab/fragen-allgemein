// Prüfbilder: einmal bündeln, mehrere Einzelbilder rendern. Aufruf: node stills.mjs 12.5 40 ...  (Sekunden)
import {bundle} from '@remotion/bundler';
import {renderStill, selectComposition} from '@remotion/renderer';
import path from 'node:path';
const B = '/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell';
const serveUrl = await bundle({entryPoint: path.resolve('src/index.js')});
const comp = await selectComposition({serveUrl, id: 'Erklaervideo', browserExecutable: B});
for (const s of process.argv.slice(2)) {
  const frame = Math.round(parseFloat(s) * 30);
  const out = `out/still_${String(s).replace('.', '_')}.png`;
  await renderStill({serveUrl, composition: comp, frame, output: out, browserExecutable: B, scale: 0.5});
  console.log(out);
}
