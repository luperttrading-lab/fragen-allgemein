// Rendert film.html zu Video: node render.js <plan.json> <ausgabe.mp4> [fps] [nur Standbilder: t1,t2,...]
const {chromium}=require('playwright'); const fs=require('fs'); const path=require('path'); const {spawn}=require('child_process');
const [planPfad, aus, fpsS='25', standbilder]=process.argv.slice(2); const fps=+fpsS;
const plan=JSON.parse(fs.readFileSync(planPfad)); const N=Math.ceil(plan.dauer*fps); const W=4;
async function seite(b){const p=await b.newPage({viewport:{width:1920,height:1080}});
  await p.goto('file://'+path.resolve(__dirname,'film.html')); await p.evaluate(pl=>window.starten(pl),plan);
  await p.evaluate(()=>document.fonts.ready);
  await p.evaluate(()=>Promise.all([...document.images].map(i=>i.complete?1:new Promise(r=>{i.onload=i.onerror=r}))));
  return p;}
(async()=>{const b=await chromium.launch(); const t0=Date.now();
  if(standbilder){const p=await seite(b); for(const t of standbilder.split(',')){await p.evaluate(x=>window.render(x),+t); await p.screenshot({path:`${aus}_${t}.jpg`,type:'jpeg',quality:80});} await b.close(); return;}
  const teile=[];
  await Promise.all([...Array(W)].map(async(_,w)=>{const p=await seite(b); const von=Math.floor(w*N/W), bis=Math.floor((w+1)*N/W);
    const ziel=`${aus}.teil${w}.mp4`; teile[w]=ziel;
    const ff=spawn('ffmpeg',['-v','error','-y','-f','image2pipe','-framerate',String(fps),'-i','-','-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p',ziel]);
    for(let i=von;i<bis;i++){await p.evaluate(x=>window.render(x),i/fps); const buf=await p.screenshot({type:'jpeg',quality:92});
      if(!ff.stdin.write(buf)) await new Promise(r=>ff.stdin.once('drain',r));}
    ff.stdin.end(); await new Promise(r=>ff.on('close',r));}));
  await b.close();
  fs.writeFileSync(`${aus}.liste.txt`,teile.map(f=>`file '${path.resolve(f)}'`).join('\n'));
  console.log('Bilder fertig in',((Date.now()-t0)/1000).toFixed(0),'s,',N,'Frames');
})();
