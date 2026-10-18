const { chromium } = require('playwright'); const path=require('path');
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});const p=await b.newPage({viewport:{width:768,height:1376}});
await p.goto('file://'+path.resolve('instructional.html'));await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(300);
const r=await p.evaluate(()=>{const m={};const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let n;while(n=w.nextNode()){if(!n.textContent.trim())continue;const e=n.parentElement;const fs=parseFloat(getComputedStyle(e).fontSize);(m[fs]=m[fs]||[]).push(n.textContent.trim().slice(0,30));}return m;});
console.log(Object.keys(r).sort((a,b)=>a-b).map(k=>k+': '+r[k].slice(0,4).join(' | ')).join('\n'));await b.close();})();
