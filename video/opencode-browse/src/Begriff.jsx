// Begriffs-Einblendung: erscheint, wenn das Wort fällt, ca. 5,5 s, unten links oder rechts
import React from 'react';
import {F, ein, aus, useT} from './lib';

const Symbol = () => (
  <svg width="58" height="58" viewBox="0 0 24 24" style={{flex: 'none', marginTop: 4}}>
    <rect x="1" y="1" width="22" height="22" rx="6" fill={F.VIOLETT} />
    <path d="M6 6.5h4.2a1.8 1.8 0 0 1 1.8 1.8V18a1.5 1.5 0 0 0-1.5-1.5H6zM18 6.5h-4.2A1.8 1.8 0 0 0 12 8.3V18a1.5 1.5 0 0 1 1.5-1.5H18z"
      fill="none" stroke={F.BG1} strokeWidth="1.8" strokeLinejoin="round" />
  </svg>
);

export const Begriffe = ({liste = []}) => {
  const t = useT();
  const sichtbar = liste.filter((b) => b.pos !== 'w');
  return sichtbar.map((b, i) => {
    const naechster = sichtbar[i + 1] ? sichtbar[i + 1].t - 0.3 : 1e9;
    const ende = Math.min(b.t + 5.5, naechster);
    const a = ein(t, b.t - 0.15, 0.35) * aus(t, ende, 0.4);
    if (a <= 0.01) return null;
    const seite = b.pos === 'l' ? {left: 70} : {right: 70};
    return (
      <div key={b.begriff} style={{position: 'absolute', bottom: 36, ...seite, maxWidth: b.breite || 900, opacity: a,
        transform: `translateY(${(1 - a) * 30}px)`, background: 'rgba(11,18,32,0.95)', border: `3px solid ${F.VIOLETT}`,
        borderRadius: 22, padding: '16px 30px 20px 22px', boxShadow: '0 18px 50px rgba(0,0,0,.55)', display: 'flex', gap: 20}}>
        <Symbol />
        <div>
          <div style={{fontSize: 22, fontWeight: 800, color: F.VIOLETT, letterSpacing: 3}}>BEGRIFF</div>
          <div style={{fontSize: 44, fontWeight: 800, color: F.TEXT, lineHeight: 1.1, marginTop: 2}}>{b.begriff}</div>
          <div style={{fontSize: 30, fontWeight: 500, color: '#cbd5e1', lineHeight: 1.3, marginTop: 6}}>{b.erklaerung}</div>
        </div>
      </div>
    );
  });
};
