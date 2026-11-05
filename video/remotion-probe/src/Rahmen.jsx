// Hintergrund (Papier, Punktraster, Vignette), Kapitelkopf und Fortschrittsbalken
import React from 'react';
import {F, T, Svg, Kreis, ein, zurueck, glatt, p, klemm} from './lib';

export const Hintergrund = () => (
  <div style={{position: 'absolute', inset: 0, backgroundColor: F.BG,
    backgroundImage: 'radial-gradient(ellipse 1075px 691px at 640px 360px, rgba(222,210,190,0) 78%, rgba(222,210,190,0.6) 100%),'
      + 'radial-gradient(circle at 16px 16px, rgba(120,100,70,0.133) 1.4px, rgba(120,100,70,0) 1.9px)',
    backgroundSize: '100% 100%, 32px 32px'}} />
);

export const Rahmen = ({tl, nr, kicker, kapitel, tGesamt}) => {
  const a = ein(tl, 0, 0.4);
  const sp = zurueck(p(tl, 0.05, 0.45));
  const dx = 18 * (1 - glatt(p(tl, 0.1, 0.5)));
  return (
    <>
      <Svg><Kreis cx={78} cy={46} r={17 * sp} c={F.TEAL} alpha={a} /></Svg>
      <T s={String(nr)} x={78} y={46} g={21} c="#ffffff" alpha={a} skala={Math.max(sp, 0.02)} />
      <T s={kicker.toUpperCase()} x={106 + dx} y={46} g={22} c={F.GRAU} anker="l" alpha={a} />
      {/* Fortschritt: ein Balken je Kapitel, Breite nach Dauer – verteilt der Browser (flex-grow) */}
      <div style={{position: 'absolute', left: 60, top: 697.5, width: 1160, height: 5, display: 'flex', gap: 6}}>
        {kapitel.map((k, i) => (
          <div key={i} style={{flexGrow: k.dauer, flexBasis: 0, background: F.HELL}}>
            <div style={{height: '100%', width: `${100 * klemm((tGesamt - k.start) / k.dauer)}%`, background: F.TEAL}} />
          </div>
        ))}
      </div>
    </>
  );
};
