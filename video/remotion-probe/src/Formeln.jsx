// Ausblick: Formelsatz mit KaTeX im Look der Mathe-Videos (Karte, Farben, Inter für Text).
import React, {useEffect, useState} from 'react';
import {AbsoluteFill, continueRender, delayRender} from 'remotion';
import katex from 'katex';
import 'katex/dist/katex.min.css';
import {F, Zeile, useSchriften} from './lib';
import {Hintergrund} from './Rahmen';

const tex = (s) => katex.renderToString(s, {displayMode: true, throwOnError: true});
const A = (s) => `\\textcolor{${F.CA}}{${s}}`, B = (s) => `\\textcolor{${F.CB}}{${s}}`, T = (s) => `\\textcolor{${F.TEAL}}{${s}}`;
const FORMELN = [
  ['Binomische Formel', `(${A('a')}+${B('b')})^2 = ${A('a')}^2 + ${T('2' + A('a') + B('b'))} + ${B('b')}^2`],
  ['Quadratische Gleichung', `x_{1,2} = \\frac{-${B('b')} \\pm \\sqrt{${B('b')}^2 - 4${A('a')}c}}{2${A('a')}}`],
  ['Stichprobenvarianz', `s^2 = \\frac{1}{n-1}\\sum_{i=1}^{n}\\left(x_i - ${T('\\bar{x}')}\\right)^2`],
  ['Binomialverteilung', `P(X = k) = ${T('\\binom{n}{k}')}\\, ${A('p')}^{k}\\,(1-${A('p')})^{\\,n-k}`],
];

export const Formeln = () => {
  const schrift = useSchriften();
  const [h] = useState(() => delayRender('KaTeX-Schriften'));
  const [fertig, setFertig] = useState(false);
  useEffect(() => { document.fonts.ready.then(() => setTimeout(() => { setFertig(true); continueRender(h); }, 300)); }, [h]);
  if (!schrift) return null;
  return (
    <AbsoluteFill style={{opacity: fertig ? 1 : 0.99}}>
      <Hintergrund />
      <div style={{position: 'absolute', left: 60, top: 34}}>
        <Zeile teile={[['AUSBLICK: FORMELSATZ (KaTeX)', F.GRAU]]} g={22} />
      </div>
      <div style={{position: 'absolute', left: 60, right: 60, top: 90, bottom: 60, display: 'grid',
        gridTemplateColumns: 'minmax(0, 1fr) minmax(0, 1fr)', gap: 28}}>
        {FORMELN.map(([titel, f]) => (
          <div key={titel} style={{background: '#fff', borderRadius: 22, boxShadow: '0 8px 24px rgba(70,50,25,0.22)',
            padding: '22px 28px', display: 'flex', flexDirection: 'column'}}>
            <Zeile teile={[[titel.toUpperCase(), F.GRAU]]} g={20} />
            <div style={{flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center', color: F.INK,
              fontSize: 31}} dangerouslySetInnerHTML={{__html: tex(f)}} />
          </div>
        ))}
      </div>
    </AbsoluteFill>
  );
};
