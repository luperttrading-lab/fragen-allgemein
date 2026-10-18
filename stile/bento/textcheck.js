// Prüft, ob die Inhaltssätze wörtlich im gerenderten Text vorkommen
const { chromium } = require('playwright'); const path=require('path');
(async()=>{
  const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'}); const pg=await b.newPage();
  await pg.goto('file://'+path.resolve('bento.html'));
  const txt=(await pg.evaluate(()=>document.body.innerText)).replace(/\s+/g,' ');
  const must=["ADHS im Gehirn","Kein Willensproblem, sondern ein Steuerungsproblem",
   "Quelle: NeuroWissen TV, „NEUROLOGE ERKLÄRT: Das macht ADHS wirklich in deinem Gehirn“ (2026)",
   "Die wichtige E-Mail (5 Minuten Arbeit) bleibt eine Stunde liegen.","Beim Lieblingsthema: stundenlanger Hyperfokus.","Dasselbe Gehirn, andere Aktivierung.",
   "faul, undiszipliniert, „ist mir egal“.","neuroentwicklungsbedingte Störung der Selbststeuerung.",
   "Fragt ständig: „Lohnt sich das jetzt?“","Nicht einfach „zu wenig Dopamin“, sondern veränderte Signalwege.",
   "Wichtig finden","jetzt Motivation aufbringen.","Die Steuerzentrale","präfrontaler Cortex","Planen","Arbeitsgedächtnis","Ablenkung ausblenden","Impulse bremsen","Langfristige Ziele",
   "Bei reizarmen Aufgaben weniger stabil.","Die Lücke zwischen Wissen und Tun","„Ich sollte …“","„Ich mache es jetzt.“","Ich weiß es und schaffe es trotzdem nicht anzufangen.",
   "Was die Aktivierung einschaltet","Neuheit","Unmittelbare Konsequenzen","Persönliches Interesse","Zeitdruck",
   "Die Deadline-Falle","Aufschieben","Deadline naht","Stress","Arbeitsphase","Erleichterung","wieder von vorn",
   "ADHS heißt nicht „keine Aufmerksamkeit“. Es heißt: Aufmerksamkeit, Motivation und Verhalten zuverlässig an das anzupassen, was gerade nötig ist, fällt schwer.",
   "Kein Hirnscan kann ADHS diagnostizieren, es gibt nur Gruppenunterschiede.","Die Diagnose gehört zu Fachleuten.","Der Bewerter: Dopamin & Noradrenalin","Das Paradox"];
  const low=txt.toLowerCase();
  for(const m of must){ const ok=txt.includes(m)||low.includes(m.toLowerCase()); if(!ok) console.log('FEHLT:',m); }
  console.log('Text geprüft,', must.length, 'Sätze');
  await b.close();})();
