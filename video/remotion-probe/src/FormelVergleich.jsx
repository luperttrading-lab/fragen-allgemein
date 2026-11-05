// Dieselben drei Formeln wie im Python-Bild, gesetzt mit KaTeX, gleiche Karte und Farben.
import React, {useEffect, useState} from 'react';
import {AbsoluteFill, continueRender, delayRender} from 'remotion';
import katex from 'katex';
import 'katex/dist/katex.min.css';
import {F, Zeile, useSchriften} from './lib';
import {Hintergrund} from './Rahmen';

const tex = (s) => katex.renderToString('\\displaystyle ' + s, {throwOnError: true});
const A = (s) => `\\textcolor{${F.CA}}{${s}}`, B = (s) => `\\textcolor{${F.CB}}{${s}}`, T = (s) => `\\textcolor{${F.TEAL}}{${s}}`;
const FORMELN = [
  `x_{1,2} = \\frac{-${B('b')} \\pm \\sqrt{${B('b')}^2 - 4${A('a')}c}}{2${A('a')}}`,
  `s^2 = \\frac{1}{n-1}\\sum_{i=1}^{n}\\left(x_i - ${T('\\bar{x}')}\\right)^2`,
  `P(X = k) = ${T('\\binom{n}{k}')}\\, ${A('p')}^{k}\\,(1-${A('p')})^{\\,n-k}`,
];

export const FormelVergleich = () => {
  const schrift = useSchriften();
  const [h] = useState(() => delayRender('KaTeX-Schriften'));
  useEffect(() => { document.fonts.ready.then(() => setTimeout(() => continueRender(h), 300)); }, [h]);
  if (!schrift) return null;
  return (
    <AbsoluteFill>
      <Hintergrund />
      <div style={{position: 'absolute', left: 80, top: 110, width: 1120, height: 520, background: '#fff', borderRadius: 22,
        boxShadow: '0 8px 24px rgba(70,50,25,0.22)', padding: '36px 40px', display: 'flex', flexDirection: 'column'}}>
        <Zeile teile={[['MIT REMOTION: FORMELSATZ (KaTeX)', F.GRAU]]} g={22} />
        <div style={{flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'space-around', color: F.INK, fontSize: 30}}>
          {FORMELN.map((f) => <div key={f} dangerouslySetInnerHTML={{__html: tex(f)}} />)}
        </div>
      </div>
    </AbsoluteFill>
  );
};
