// Schritte-Karte: Höhe, Zeilenabstände und Ausrichtung ergeben sich aus dem Inhalt (Flexbox), nicht aus Formeln.
import React from 'react';
import {F, Zeile, ein} from './lib';

const Schritt = ({z, t}) => {
  const at = ein(t, z.tTitel);
  const akt = z.aktiv ? ein(t, z.aktiv[0], 0.3) * (1 - ein(t, z.aktiv[1], 0.3)) : 0;
  return (
    <div style={{position: 'relative', display: 'flex', alignItems: 'center', gap: 17, padding: '14px 0 14px 29px',
      opacity: at}}>
      <div style={{position: 'absolute', inset: '-4px 14px 4px 14px', borderRadius: 14, background: z.farbe,
        opacity: 0.13 * akt}} />
      <div style={{position: 'relative', width: 46, height: 46, borderRadius: '50%', background: z.farbe, color: '#fff',
        display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: 'InterV', fontWeight: 800,
        fontSize: 25}}>{z.nr}</div>
      <div style={{position: 'relative', display: 'flex', flexDirection: 'column', gap: 2}}>
        <Zeile teile={[[z.titel, F.GRAU]]} g={25} w={700} />
        <Zeile teile={z.teile} g={36} alpha={ein(t, z.tRech)} />
      </div>
    </div>
  );
};

export const Karte = ({t, x, y, breite, titel, zeilen, ergebnis, tErgebnis}) => (
  <div style={{position: 'absolute', left: x, top: y, width: breite, background: '#fff', borderRadius: 22,
    boxShadow: '0 8px 24px rgba(70,50,25,0.22)', padding: '25px 0 14px'}}>
    <Zeile teile={[[titel.toUpperCase(), F.GRAU]]} g={22} stil={{paddingLeft: 30, marginBottom: 8}} />
    {zeilen.map((z) => <Schritt key={z.nr} z={z} t={t} />)}
    <div style={{margin: '8px 30px 0', borderTop: `2px solid ${F.HELL}`, paddingTop: 10, display: 'flex',
      justifyContent: 'center', opacity: ein(t, tErgebnis)}}>
      <Zeile teile={ergebnis} g={46} />
    </div>
  </div>
);
