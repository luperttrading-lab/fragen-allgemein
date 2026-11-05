// Kapitel „Der Trick“ (Nachbau von s_regel aus regel.py): 16 · 18 in drei Schritten.
import React from 'react';
import {useCurrentFrame, useVideoConfig, AbsoluteFill} from 'remotion';
import {F, T, ZeileBei, Svg, Kreis, Spur, Funken, useSchriften, breite, tinte, mitten, glatt, zurueck, p, mix, klemm,
  ein, mischfarbe} from './lib';
import {Hintergrund, Rahmen} from './Rahmen';
import {Karte} from './Karte';
import Z from './zeiten.json';

const {T: TT, t_zweite, t_mult} = Z;
const X = 400, YT = 175, G = 112, YR = 345, GR = 92, Y3 = 462, XS = 560;
const OBEN = [['1', F.INK], ['6', F.CA], [' · ', F.INK], ['1', F.INK], ['8', F.CB]];

const Einkreisen = ({ziffer, x, y, g, c, a, skala}) => {
  if (a <= 0) return null;
  const [ox, oy, w, h] = tinte(ziffer, g);                // Ellipse mittig um die Tinte, nicht um die Zeichenbox
  return <ellipse cx={x + ox * skala} cy={y + oy * skala} rx={(w / 2 + 9) * skala} ry={(h / 2 + 11) * skala}
    fill={c} fillOpacity={28 / 255 * a} stroke={c} strokeOpacity={230 / 255 * a} strokeWidth={4} />;
};

const Szene = ({t}) => {
  const cs = mitten(OBEN, X, G);
  const p8 = Math.sin(Math.PI * p(t, TT.acht, 0.6));
  const p68 = Math.sin(Math.PI * p(t, TT.f68, 0.6));
  const sk = (i) => 1 + 0.12 * Math.max(i === 4 ? p8 : 0, i === 1 || i === 4 ? p68 : 0);
  // „die zweite Zahl“: 18 unterstrichen, bis die Acht eingekreist wird
  const au = ein(t, t_zweite, 0.4) * (1 - ein(t, TT.acht - 0.1, 0.3));
  const [ox1, , w1] = tinte('1', G), [ox8, , w8, h8] = tinte('8', G);
  const kreise = [[4, F.CB, TT.acht, TT.flug + 0.4], [1, F.CA, t_mult, TT.f68 + 0.5], [4, F.CB, t_mult, TT.f68 + 0.5]];

  // Schritt 1: 16 und die 8 wandern nach unten und werden zu 24
  const fl = glatt(p(t, TT.flug, 1.1));
  const m24 = glatt(p(t, TT.z24, 0.45));
  const zc = mitten([['16'], [' + '], ['8']], X, GR);
  const ort8 = (tt) => { const f = glatt(p(tt, TT.flug, 1.1));
    return f > 0 && f < 1 ? [mix(cs[4], zc[2], f), mix(YT, YR, f) - Math.sin(f * Math.PI) * 110] : null; };
  // Schritt 2: eine Null fällt an die 24; danach Umbau zur schriftlichen Addition
  const sm = glatt(p(t, TT.summe, 0.8));
  const w2 = breite('24', GR), w0 = breite('0', GR);
  const nul = p(t, TT.null, 0.55), rueck = glatt(p(t, TT.null, 0.35));
  const links = X - (w2 + w0 * rueck) / 2;
  const dx = (XS - (X + (w2 + w0) / 2)) * sm;
  const c240 = mischfarbe(F.INK, F.TEAL, p(t, TT.z240, 0.4));
  // Schritt 3: die Einer 6 und 8 wandern nach unten und werden zu 48
  const f3 = glatt(p(t, TT.f68 + 0.05, 0.7));
  const m48 = glatt(p(t, TT.z48, 0.45));
  const zc3 = mitten([['6'], [' · '], ['8']], X, GR * 0.9);
  const ort3 = (tt, i) => { const f = glatt(p(tt, TT.f68 + 0.05, 0.7));
    if (!(f > 0 && f < 1)) return null;
    const bg = Math.sin(f * Math.PI) * 190;
    return i === 0 ? [mix(cs[1], zc3[0], f) - bg, mix(YT, Y3, f)] : [mix(cs[4], zc3[2], f) + bg, mix(YT, Y3, f)]; };
  const bogen = Math.sin(f3 * Math.PI) * 190;
  const w48 = breite('48', GR), w240 = w2 + w0, w288 = breite('288', GR);
  const q = zurueck(p(t, TT.z288, 0.6));
  const ring = p(t, TT.z288, 0.9);

  const zeilen = [
    {nr: '1', farbe: F.CB, titel: 'Einer rüber', tTitel: TT.s1, tRech: TT.z24, aktiv: [TT.s1, TT.s2],
      teile: [['16', F.INK], [' + ', F.INK], ['8', F.CB], [' = 24', F.INK]]},
    {nr: '2', farbe: F.TEAL, titel: 'mal 10', tTitel: TT.s2, tRech: TT.z240, aktiv: [TT.s2, TT.s3],
      teile: [['24 · 10 = ', F.INK], ['240', F.TEAL]]},
    {nr: '3', farbe: F.CD, titel: 'Einer · Einer dazu', tTitel: TT.s3, tRech: TT.z48, aktiv: [TT.s3, TT.summe],
      teile: [['+ ', F.INK], ['6', F.CA], [' · ', F.INK], ['8', F.CB], [' = ', F.INK], ['48', F.CD]]},
  ];

  return (
    <>
      <Svg>
        {au > 0 && <line x1={cs[3] + ox1 - w1 / 2} x2={cs[4] + ox8 + w8 / 2} y1={YT + h8 / 2 + 14} y2={YT + h8 / 2 + 14}
          stroke={F.CB} strokeWidth={6} strokeOpacity={au} />}
        {kreise.map(([i, c, von, bis], k) => <Einkreisen key={k} ziffer={OBEN[i][0]} x={cs[i]} y={YT} g={G} c={c}
          a={ein(t, von, 0.3) * (1 - ein(t, bis, 0.3))} skala={sk(i)} />)}
      </Svg>
      <ZeileBei x={X} y={YT} g={G} teile={OBEN} skalen={Object.fromEntries(OBEN.map((_, i) => [i, sk(i)]))} />

      <Svg><Spur ort={ort8} t={t} c={F.CB} /></Svg>
      {fl > 0 && m24 < 1 && <>
        <T s="16" x={mix((cs[0] + cs[1]) / 2, zc[0], fl)} y={mix(YT, YR, fl)} g={mix(G, GR, fl)} c={F.INK}
          alpha={(1 - m24) * klemm(fl * 3)} />
        <T s=" + " x={zc[1]} y={YR} g={GR} c={F.INK} alpha={(1 - m24) * fl} />
        <T s="8" x={mix(cs[4], zc[2], fl)} y={mix(YT, YR, fl) - Math.sin(fl * Math.PI) * 110} g={mix(G, GR, fl)}
          c={F.CB} alpha={(1 - m24) * klemm(fl * 3)} />
      </>}
      {m24 > 0 && <T s="24" x={links + w2 / 2 + dx} y={YR} g={GR} c={c240} skala={0.6 + 0.4 * zurueck(m24)} alpha={m24} />}
      {nul > 0 && <>
        <T s="0" x={links + w2 + w0 / 2 + dx} y={YR - 120 * (1 - zurueck(nul))} g={GR} c={c240} alpha={klemm(nul * 2)} />
        <T s="· 10" x={X + dx} y={YR - 72} g={32} c={F.GRAU} alpha={glatt(nul * 2) * (1 - sm)} />
      </>}

      <Svg><Spur ort={(tt) => ort3(tt, 0)} t={t} c={F.CA} /><Spur ort={(tt) => ort3(tt, 1)} t={t} c={F.CB} /></Svg>
      {f3 > 0 && m48 < 1 && <>
        <T s="6" x={mix(cs[1], zc3[0], f3) - bogen} y={mix(YT, Y3, f3)} g={mix(G, GR * 0.9, f3)} c={F.CA}
          alpha={(1 - m48) * klemm(f3 * 3)} />
        <T s=" · " x={zc3[1]} y={Y3} g={GR * 0.9} c={F.INK} alpha={(1 - m48) * f3} />
        <T s="8" x={mix(cs[4], zc3[2], f3) + bogen} y={mix(YT, Y3, f3)} g={mix(G, GR * 0.9, f3)} c={F.CB}
          alpha={(1 - m48) * klemm(f3 * 3)} />
      </>}
      {m48 > 0 && <T s="48" x={mix(X, XS - w48 / 2, sm)} y={Y3} g={GR} c={F.CD} skala={0.6 + 0.4 * zurueck(m48)} alpha={m48} />}
      {sm > 0 && <>
        <T s="+" x={XS - w240 - 46} y={Y3} g={GR} c={F.INK} alpha={sm} />
        <Svg><line x1={XS - w240 - 80} x2={mix(XS - w240 - 80, XS + 12, sm)} y1={522} y2={522} stroke={F.INK} strokeWidth={5} /></Svg>
      </>}
      {q > 0 && <T s="288" x={XS - w288 / 2} y={590} g={GR} c={F.GRUEN} skala={0.5 + 0.5 * q} alpha={klemm(q * 2)} />}
      <Svg>
        <Funken t={t} start={TT.z288 + 0.05} cx={XS - w288 / 2} cy={590} r0={70} r1={190} />
        {ring > 0 && ring < 1 && <circle cx={XS - w288 / 2} cy={590} r={60 + 120 * ring} fill="none" stroke={F.GRUEN}
          strokeOpacity={160 / 255 * (1 - ring)} strokeWidth={5} />}
      </Svg>

      <Karte t={t} x={780} y={120} breite={440} titel="Der Trick" zeilen={zeilen} tErgebnis={TT.z288}
        ergebnis={[['16 · 18 = ', F.INK], ['288', F.GRUEN]]} />
    </>
  );
};

export const Trick = () => {
  const bereit = useSchriften();
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  if (!bereit) return null;
  const t = frame / fps;
  return (
    <AbsoluteFill>
      <Hintergrund />
      <Szene t={t} />
      <Rahmen tl={t} nr={Z.szene.nr} kicker={Z.szene.kicker} kapitel={Z.kapitel} tGesamt={Z.szene.start + t} />
    </AbsoluteFill>
  );
};
