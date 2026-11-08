// Gemeinsame Bausteine: Farben, Bewegung, Schrift, Symbole.
import React, {useEffect, useState} from 'react';
import {continueRender, delayRender, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';

export const F = {
  BG1: '#0b1220', BG2: '#111c33', KARTE: '#18243f', KARTE2: '#1f2d4d', RAND: '#2c3c63',
  TEXT: '#f1f5f9', GRAU: '#94a3b8', DUNKEL: '#64748b',
  CYAN: '#22d3ee', BLAU: '#60a5fa', VIOLETT: '#a78bfa', GRUEN: '#4ade80', GELB: '#fbbf24', ROT: '#f87171', ROSA: '#f472b6',
};
export const SCHRIFT = 'InterV';

export const klemm = (x) => Math.max(0, Math.min(1, x));
export const glatt = (x) => { x = klemm(x); return x * x * (3 - 2 * x); };
export const raus = (x) => { x = klemm(x); return 1 - (1 - x) ** 3; };
export const feder = (x) => { x = klemm(x); return 1 + 2.4 * (x - 1) ** 3 + 1.4 * (x - 1) ** 2; };
export const ein = (t, start, dauer = 0.45) => (start == null ? 0 : raus((t - start) / dauer));
export const aus = (t, start, dauer = 0.4) => (start == null ? 1 : 1 - glatt((t - start) / dauer));

// Zeit der Szene in Sekunden
export const useT = () => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  return f / fps;
};

const lade = (() => {
  let p = null;
  return () => p || (p = Promise.all([
    ['Inter-Regular.otf', '400'], ['Inter-Medium.otf', '500'], ['Inter-Bold.otf', '700'], ['Inter-ExtraBold.otf', '800'],
  ].map(([d, w]) => new FontFace(SCHRIFT, `url(${staticFile(d)})`, {weight: w}).load().then((ff) => document.fonts.add(ff)))));
})();
export const useSchriften = () => {
  const [bereit, setBereit] = useState(false);
  const [h] = useState(() => delayRender('Schriften'));
  useEffect(() => { lade().then(() => { setBereit(true); continueRender(h); }); }, [h]);
  return bereit;
};

// Einblenden mit kleinem Versatz von unten (oder links/rechts)
export const Ein = ({t, at, dauer = 0.5, dy = 24, dx = 0, skala = false, bis, style, children}) => {
  const a = ein(t, at, dauer) * aus(t, bis);
  if (a <= 0.001) return null;
  const s = skala ? 0.85 + 0.15 * feder((t - at) / (dauer * 1.4)) : 1;
  return (
    <div style={{position: 'absolute', opacity: a, transform: `translate(${(1 - a) * dx}px, ${(1 - a) * dy}px) scale(${s})`, ...style}}>
      {children}
    </div>
  );
};

export const Chip = ({farbe = F.CYAN, children, gross = 30, style, gefuellt = false}) => (
  <div style={{display: 'inline-flex', alignItems: 'center', gap: 12, padding: `${gross * 0.35}px ${gross * 0.7}px`,
    borderRadius: 999, border: `3px solid ${farbe}`, color: gefuellt ? F.BG1 : farbe, background: gefuellt ? farbe : `${farbe}1a`,
    fontSize: gross, fontWeight: 700, whiteSpace: 'nowrap', ...style}}>{children}</div>
);

export const Karte = ({children, farbe = F.RAND, style}) => (
  <div style={{background: F.KARTE, border: `3px solid ${farbe}`, borderRadius: 28, padding: '28px 36px',
    boxShadow: '0 20px 50px rgba(0,0,0,.35)', ...style}}>{children}</div>
);

export const Haken = ({farbe = F.GRUEN, g = 36}) => (
  <svg width={g} height={g} viewBox="0 0 24 24" style={{flex: 'none'}}>
    <circle cx="12" cy="12" r="11" fill={farbe} />
    <path d="M6.5 12.5l3.5 3.5 7.5-8" stroke={F.BG1} strokeWidth="2.8" fill="none" strokeLinecap="round" strokeLinejoin="round" />
  </svg>
);
export const Kreuz = ({farbe = F.ROT, g = 36}) => (
  <svg width={g} height={g} viewBox="0 0 24 24" style={{flex: 'none'}}>
    <circle cx="12" cy="12" r="11" fill={farbe} />
    <path d="M8 8l8 8M16 8l-8 8" stroke={F.BG1} strokeWidth="2.8" strokeLinecap="round" />
  </svg>
);
export const Warn = ({farbe = F.GELB, g = 40}) => (
  <svg width={g} height={g} viewBox="0 0 24 24" style={{flex: 'none'}}>
    <path d="M12 2.5L23 21.5H1z" fill={farbe} strokeLinejoin="round" />
    <path d="M12 9v6" stroke={F.BG1} strokeWidth="2.6" strokeLinecap="round" />
    <circle cx="12" cy="18.2" r="1.4" fill={F.BG1} />
  </svg>
);
export const Schloss = ({farbe = F.GELB, g = 60}) => (
  <svg width={g} height={g} viewBox="0 0 24 24">
    <rect x="4" y="10.5" width="16" height="11" rx="2.5" fill={farbe} />
    <path d="M7.5 10.5V7.5a4.5 4.5 0 0 1 9 0v3" stroke={farbe} strokeWidth="2.6" fill="none" />
    <circle cx="12" cy="15.5" r="1.8" fill={F.BG1} />
  </svg>
);

// Agent als kleiner Roboterkopf
export const Roboter = ({g = 120, farbe = F.CYAN, blick = 0}) => (
  <svg width={g} height={g} viewBox="0 0 100 100">
    <line x1="50" y1="8" x2="50" y2="22" stroke={farbe} strokeWidth="5" strokeLinecap="round" />
    <circle cx="50" cy="8" r="6" fill={farbe} />
    <rect x="14" y="22" width="72" height="62" rx="18" fill={F.KARTE2} stroke={farbe} strokeWidth="5" />
    <circle cx={37 + blick * 4} cy="50" r="8" fill={farbe} />
    <circle cx={63 + blick * 4} cy="50" r="8" fill={farbe} />
    <rect x="36" y="66" width="28" height="6" rx="3" fill={farbe} />
    <rect x="4" y="44" width="10" height="20" rx="4" fill={farbe} />
    <rect x="86" y="44" width="10" height="20" rx="4" fill={farbe} />
  </svg>
);
export const Mensch = ({g = 120, farbe = F.GELB}) => (
  <svg width={g} height={g} viewBox="0 0 100 100">
    <circle cx="50" cy="32" r="18" fill={farbe} />
    <path d="M16 92c0-20 15-34 34-34s34 14 34 34z" fill={farbe} />
  </svg>
);

// Browserfenster mit Tabs und Adresszeile
export const Browser = ({breite, hoehe, tabs = [], url, children, style}) => (
  <div style={{position: 'absolute', width: breite, height: hoehe, borderRadius: 22, overflow: 'hidden',
    background: '#0f172a', border: `3px solid ${F.RAND}`, boxShadow: '0 30px 70px rgba(0,0,0,.45)', ...style}}>
    <div style={{height: 58, background: F.KARTE2, display: 'flex', alignItems: 'flex-end', padding: '0 18px', gap: 10}}>
      <div style={{display: 'flex', gap: 10, alignSelf: 'center', marginRight: 14}}>
        {['#ef4444', '#f59e0b', '#22c55e'].map((c) => <div key={c} style={{width: 16, height: 16, borderRadius: 8, background: c}} />)}
      </div>
      {tabs.map((tb, i) => <div key={i} style={{opacity: tb.alpha ?? 1}}>{tb.el}</div>)}
    </div>
    {url != null && (
      <div style={{height: 54, background: '#162036', display: 'flex', alignItems: 'center', padding: '0 22px'}}>
        <div style={{flex: 1, height: 36, borderRadius: 18, background: '#0b1220', color: F.GRAU, fontSize: 22,
          fontWeight: 500, display: 'flex', alignItems: 'center', padding: '0 20px'}}>{url}</div>
      </div>
    )}
    <div style={{position: 'relative', width: '100%', height: hoehe - 58 - (url != null ? 54 : 0)}}>{children}</div>
  </div>
);
export const Tab = ({children, aktiv = false, farbe}) => (
  <div style={{height: 44, padding: '0 22px', borderRadius: '12px 12px 0 0', display: 'flex', alignItems: 'center', gap: 10,
    background: aktiv ? '#162036' : 'transparent', color: farbe || (aktiv ? F.TEXT : F.GRAU), fontSize: 22, fontWeight: 600,
    whiteSpace: 'nowrap'}}>{children}</div>
);

// Pfeil von links nach rechts, wächst mit f (0..1)
export const Pfeil = ({x, y, laenge, f = 1, farbe = F.GRAU, dick = 5, doppelt = false}) => {
  const l = laenge * klemm(f);
  if (l < 2) return null;
  return (
    <svg style={{position: 'absolute', left: x, top: y - 20, overflow: 'visible'}} width={laenge} height={40}>
      <line x1={doppelt ? 6 : 0} y1={20} x2={Math.max(0, l - 8)} y2={20} stroke={farbe} strokeWidth={dick} strokeLinecap="round" />
      <path d={`M${l - 16},9 L${l},20 L${l - 16},31`} stroke={farbe} strokeWidth={dick} fill="none" strokeLinecap="round" strokeLinejoin="round" />
      {doppelt && f >= 1 && <path d="M16,9 L0,20 L16,31" stroke={farbe} strokeWidth={dick} fill="none" strokeLinecap="round" strokeLinejoin="round" />}
    </svg>
  );
};

// Kopfzeile der Szene
export const Kopf = ({t, nr, titel, farbe = F.CYAN}) => (
  <div style={{position: 'absolute', left: 90, top: 56, display: 'flex', alignItems: 'center', gap: 22,
    opacity: ein(t, 0.05, 0.5), transform: `translateX(${(1 - ein(t, 0.05, 0.5)) * -30}px)`}}>
    <div style={{width: 58, height: 58, borderRadius: 16, background: farbe, color: F.BG1, fontSize: 30, fontWeight: 800,
      display: 'flex', alignItems: 'center', justifyContent: 'center'}}>{nr}</div>
    <div style={{fontSize: 40, fontWeight: 800, color: F.TEXT, letterSpacing: -0.5}}>{titel}</div>
  </div>
);

export const Quelle = ({children, t, at = 0.6}) => (
  <div style={{position: 'absolute', left: 90, right: 90, bottom: 44, fontSize: 21, color: F.DUNKEL, fontWeight: 500,
    opacity: ein(t, at, 0.6)}}>{children}</div>
);
