// Titelkarte (Intro + Vorschaubild) und YouTube-Thumbnails
import React from 'react';
import {AbsoluteFill} from 'remotion';
import {F, SCHRIFT, Chip, Roboter, Browser, Tab, Warn, Haken, ein, aus, useT, useSchriften} from './lib';

const Hintergrund = ({children}) => (
  <AbsoluteFill style={{fontFamily: SCHRIFT, color: F.TEXT, background: `radial-gradient(ellipse at 30% 0%, ${F.BG2} 0%, ${F.BG1} 65%)`}}>
    <AbsoluteFill style={{backgroundImage: 'linear-gradient(rgba(148,163,184,.05) 2px, transparent 2px), linear-gradient(90deg, rgba(148,163,184,.05) 2px, transparent 2px)',
      backgroundSize: '80px 80px'}} />
    {children}
  </AbsoluteFill>
);

// Browserfenster mit Agentengruppe und Roboter davor
const Motiv = ({x, y, g = 1}) => (
  <div style={{position: 'absolute', left: x, top: y, transform: `scale(${g})`, transformOrigin: 'top left'}}>
    <Browser breite={760} hoehe={520} url="https://mail.example.com" tabs={[
      {el: <Tab aktiv>Posteingang</Tab>}, {el: <Tab>Bank</Tab>},
      {el: <div style={{height: 44, display: 'flex', alignItems: 'center'}}><Chip farbe={F.VIOLETT} gross={22} gefuellt>Agents · 3</Chip></div>},
    ]}>
      <div style={{position: 'absolute', left: 40, top: 40, display: 'flex', flexDirection: 'column', gap: 22}}>
        {[520, 640, 460, 580, 400].map((w, i) => <div key={i} style={{width: w, height: 18, borderRadius: 9, background: '#24314f'}} />)}
      </div>
    </Browser>
    <div style={{position: 'absolute', left: 470, top: 250, filter: `drop-shadow(0 0 40px ${F.CYAN})`}}><Roboter g={330} blick={-1} /></div>
  </div>
);

// Titelkarte: Intro im Video und Vorschaubild der Webseite
export const Titelkarte = ({animiert = true}) => {
  useSchriften();
  const t = useT();
  const a = (at) => (animiert ? ein(t, at, 0.5) : 1);
  return (
    <Hintergrund>
      <div style={{position: 'absolute', left: 120, top: 250, width: 1000}}>
        <div style={{fontSize: 34, fontWeight: 700, color: F.GRAU, opacity: a(0.1), letterSpacing: 1}}>ERKLÄRVIDEO</div>
        <div style={{fontSize: 128, fontWeight: 800, color: F.CYAN, letterSpacing: -4, lineHeight: 1.0, marginTop: 10, opacity: a(0.2)}}>OpenCode<br />Browse</div>
        <div style={{fontSize: 46, fontWeight: 700, color: F.TEXT, marginTop: 26, opacity: a(0.6)}}>KI-Agenten im echten Browser</div>
        <div style={{display: 'flex', gap: 16, marginTop: 40, flexWrap: 'wrap', opacity: a(1.0)}}>
          <Chip farbe={F.GRUEN} gross={28}>wie es funktioniert</Chip>
          <Chip farbe={F.GELB} gross={28}>was es kostet</Chip>
          <Chip farbe={F.ROT} gross={28}>wo das Risiko liegt</Chip>
        </div>
      </div>
      <div style={{opacity: a(0.4)}}><Motiv x={1080} y={230} g={1} /></div>
      <div style={{position: 'absolute', left: 120, bottom: 70, fontSize: 26, fontWeight: 600, color: F.DUNKEL, opacity: a(1.2)}}>Stand: November 2026</div>
    </Hintergrund>
  );
};

// Intro im Video: Titelkarte mit Blende
export const Intro = ({frames}) => {
  const t = useT();
  return <AbsoluteFill style={{opacity: aus(t, frames / 30 - 0.45, 0.4)}}><Titelkarte /></AbsoluteFill>;
};

// Thumbnail A: Hauptaussage groß, darunter „kostenlos, aber …“
export const ThumbnailA = () => {
  useSchriften();
  const zeile = {fontSize: 150, fontWeight: 800, lineHeight: 0.98, letterSpacing: -5};
  return (
    <Hintergrund>
      <div style={{position: 'absolute', left: 80, top: 150, width: 1000}}>
        <div style={{...zeile, color: F.TEXT}}>KI-AGENT IM</div>
        <div style={{...zeile, color: F.CYAN}}>ECHTEN</div>
        <div style={{...zeile, color: F.CYAN}}>BROWSER</div>
        <div style={{display: 'flex', flexDirection: 'column', alignItems: 'flex-start', gap: 22, marginTop: 50}}>
          <div style={{background: F.GRUEN, color: F.BG1, fontSize: 84, fontWeight: 800, padding: '8px 36px', borderRadius: 22}}>kostenlos</div>
          <div style={{background: F.ROT, color: F.BG1, fontSize: 84, fontWeight: 800, padding: '8px 36px', borderRadius: 22}}>aber riskant</div>
        </div>
      </div>
      <Motiv x={1040} y={230} g={1.1} />
      <div style={{position: 'absolute', left: 1700, top: 110}}><Warn g={180} /></div>
    </Hintergrund>
  );
};

// Thumbnail B: Vergleich mit Claude in Chrome als Frage
export const ThumbnailB = () => {
  useSchriften();
  const zeile = {fontSize: 138, fontWeight: 800, lineHeight: 0.98, letterSpacing: -5};
  return (
    <Hintergrund>
      <div style={{position: 'absolute', left: 80, top: 150, width: 1100}}>
        <div style={{fontSize: 60, fontWeight: 800, color: F.GELB}}>Claude in Chrome: 20 $ im Monat</div>
        <div style={{...zeile, color: F.TEXT, marginTop: 34}}>GRATIS-</div>
        <div style={{...zeile, color: F.CYAN}}>ALTERNATIVE?</div>
        <div style={{display: 'inline-block', background: F.TEXT, color: F.BG1, fontSize: 70, fontWeight: 800, padding: '10px 36px',
          borderRadius: 22, marginTop: 50}}>OpenCode Browse im Check</div>
      </div>
      <Motiv x={1130} y={280} g={0.92} />
    </Hintergrund>
  );
};
