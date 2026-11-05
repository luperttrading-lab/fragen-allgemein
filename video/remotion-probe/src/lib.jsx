// Gemeinsame Bausteine: Farben, Bewegungskurven (wie animationen.py), Schrift messen, Text und Zeilen.
import React, {useEffect, useState} from 'react';
import {continueRender, delayRender, staticFile} from 'remotion';

export const F = {INK: '#2b2d42', GRAU: '#6f7380', BG: '#f6f1e7', HELL: '#e6dfd2', CA: '#ff9f1c', CB: '#8338ec',
  CBLAU: '#3a86ff', CD: '#e63946', TEAL: '#0f766e', GRUEN: '#2a9d4a'};

export const klemm = (x) => Math.max(0, Math.min(1, x));
export const glatt = (x) => { x = klemm(x); return x * x * (3 - 2 * x); };
export const zurueck = (x) => { x = klemm(x); return 1 + 2.7 * (x - 1) ** 3 + 1.7 * (x - 1) ** 2; };
export const p = (t, start, dauer) => klemm((t - start) / dauer);
export const mix = (a, b, f) => a + (b - a) * f;
export const ein = (t, start, dauer = 0.5) => glatt(p(t, start, dauer));
export const mischfarbe = (h1, h2, f) => {
  const a = [1, 3, 5].map((i) => parseInt(h1.slice(i, i + 2), 16));
  const b = [1, 3, 5].map((i) => parseInt(h2.slice(i, i + 2), 16));
  return `rgb(${a.map((v, i) => Math.round(v + (b[i] - v) * klemm(f))).join(',')})`;
};

// Schriften einmal laden; erst danach wird gemessen und gezeichnet
const FAMILIE = 'InterV';
let geladen = null;
const lade = () => geladen || (geladen = Promise.all([
  new FontFace(FAMILIE, `url(${staticFile('Inter-ExtraBold.otf')})`, {weight: '800'}),
  new FontFace(FAMILIE, `url(${staticFile('Inter-Bold.otf')})`, {weight: '700'}),
].map((f) => f.load().then((ff) => document.fonts.add(ff)))));
export const useSchriften = () => {
  const [bereit, setBereit] = useState(false);
  const [h] = useState(() => delayRender('Schriften'));
  useEffect(() => { lade().then(() => { setBereit(true); continueRender(h); }); }, [h]);
  return bereit;
};

const ASC = 0.969, DESC = 0.242, LH = ASC + DESC;          // Inter: Oberlänge, Unterlänge (em)
let ctx = null;
const mess = (s, g, w) => {
  ctx = ctx || document.createElement('canvas').getContext('2d');
  ctx.font = `${w} ${g}px ${FAMILIE}`;
  return ctx.measureText(s);
};
export const breite = (s, g, w = 800) => mess(s, g, w).width;
// Tintenkasten relativ zur Textmitte (wie tinte() im Original): Versatz x, y und Breite, Höhe
export const tinte = (s, g, w = 800) => {
  const m = mess(s, g, w);
  const ox = (m.actualBoundingBoxRight - m.actualBoundingBoxLeft) / 2 - m.width / 2;
  const oy = (m.actualBoundingBoxDescent - m.actualBoundingBoxAscent) / 2 + (ASC - DESC) / 2 * g;
  return [ox, oy, m.actualBoundingBoxRight + m.actualBoundingBoxLeft, m.actualBoundingBoxAscent + m.actualBoundingBoxDescent];
};
export const mitten = (teile, x, g, w = 800) => {
  const ws = teile.map(([s]) => breite(s, g, w));
  let x0 = x - ws.reduce((a, b) => a + b, 0) / 2;
  return ws.map((b) => { const m = x0 + b / 2; x0 += b; return m; });
};

const textStil = (g, w) => ({fontFamily: FAMILIE, fontWeight: w, fontSize: g, lineHeight: `${LH * g}px`,
  whiteSpace: 'pre', fontKerning: 'normal'});

// Text, y = Zeilenmitte (wie Bild.text im Original); anker 'm' = Mitte, 'l' = linker Rand
export const T = ({s, x, y, g, c, w = 800, anker = 'm', alpha = 1, skala = 1}) => {
  if (alpha <= 0 || skala <= 0.01) return null;
  return <div style={{...textStil(g, w), position: 'absolute', left: x, top: y - LH * g / 2, color: c, opacity: alpha,
    transform: `${anker === 'm' ? 'translateX(-50%) ' : ''}scale(${skala})`,
    transformOrigin: anker === 'm' ? '50% 50%' : '0 50%'}}>{s}</div>;
};

// Mehrfarbige Zeile: die Teile setzt der Browser nebeneinander (Flexbox), keine Einzelkoordinaten
export const Zeile = ({teile, g, w = 800, alpha = 1, skalen = {}, stil = {}}) => (
  <div style={{...textStil(g, w), display: 'flex', opacity: alpha, ...stil}}>
    {teile.map(([s, c], i) => (
      <span key={i} style={{color: c, display: 'inline-block', transform: `scale(${skalen[i] ?? 1})`}}>{s}</span>
    ))}
  </div>
);
export const ZeileBei = ({x, y, g, anker = 'm', ...rest}) => (
  <div style={{position: 'absolute', left: x, top: y - LH * g / 2,
    transform: anker === 'm' ? 'translateX(-50%)' : 'none'}}><Zeile g={g} {...rest} /></div>
);

export const Svg = ({children}) => (
  <svg width={1280} height={720} style={{position: 'absolute', left: 0, top: 0, overflow: 'visible'}}>{children}</svg>
);

export const Kreis = ({cx, cy, r, c, alpha = 1}) => (alpha > 0 && r > 0 ?
  <circle cx={cx} cy={cy} r={r} fill={c} fillOpacity={alpha} /> : null);

// Flugspur: Punkte an den Orten der letzten Augenblicke
export const Spur = ({ort, t, c, n = 7, abstand = 0.045, r = 5, alpha = 0.4}) => (
  <>{Array.from({length: n}, (_, i) => i + 1).map((k) => {
    const q = ort(t - k * abstand);
    return q && <Kreis key={k} cx={q[0]} cy={q[1]} r={r * (1 - 0.1 * k)} c={c} alpha={alpha * (1 - k / (n + 1))} />;
  })}</>
);

// Funkenkranz um ein Ergebnis, 0,8 s
export const Funken = ({t, start, cx, cy, r0 = 46, r1 = 150, n = 16, dauer = 0.8, fy = 0.75}) => {
  const f = p(t, start, dauer);
  if (!(f > 0 && f < 1)) return null;
  const aus = 1 - (1 - f) ** 3;
  const farben = [F.GRUEN, F.CA, F.CB, F.CBLAU, F.CD];
  return <>{Array.from({length: n}, (_, k) => {
    const w = 2 * Math.PI * (k + 0.37 * ((k * 7) % 5) / 5) / n;
    const r = mix(r0, r1 * (0.85 + 0.3 * ((k * 3) % 4) / 3), aus);
    return <Kreis key={k} cx={cx + r * Math.cos(w)} cy={cy + fy * r * Math.sin(w)} r={6.5 - 3.5 * f}
      c={farben[k % farben.length]} alpha={0.9 * (1 - f) ** 1.4} />;
  })}</>;
};
