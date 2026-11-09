// Standbilder rendern: node stills2.mjs ID:ausgabe.jpg ...  (Skalierung 2/3 -> 1280x720)
import {bundle} from '@remotion/bundler';
import {renderStill, selectComposition} from '@remotion/renderer';
import path from 'node:path';
const B = '/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell';
const serveUrl = await bundle({entryPoint: path.resolve('src/index.js')});
for (const arg of process.argv.slice(2)) {
  const [id, out, frame] = arg.split(':');
  const comp = await selectComposition({serveUrl, id, browserExecutable: B});
  await renderStill({serveUrl, composition: comp, frame: Number(frame || 0), output: out, browserExecutable: B,
    scale: 2 / 3, imageFormat: out.endsWith('.png') ? 'png' : 'jpeg', jpegQuality: 92});
  console.log(out);
}
