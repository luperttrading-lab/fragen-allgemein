// Gesamtvideo: Szenen nacheinander, je Szene eigene Tonspur (Länge aus zeiten.json)
import React from 'react';
import {AbsoluteFill, Audio, Sequence, staticFile, useCurrentFrame} from 'remotion';
import {F, SCHRIFT, glatt, useSchriften} from './lib';
import {S01, S02, S03, S04} from './SzenenA';
import {S05, S06, S07, S08} from './SzenenB';
import {S09, S10, S11, S12, S13, Abspann} from './SzenenC';
import {Intro} from './Titel';
import {Begriffe} from './Begriff';
import Z from './zeiten.json';

const FPS = 30;
const KOMP = {s01_wand: S01, s02_browse: S02, s03_kette: S03, s04_uebergabe: S04, s05_geheim: S05, s06_lokal: S06,
  s07_vergleich: S07, s08_daten: S08, s09_injection: S09, s10_zahlen: S10, s11_schutz: S11, s12_haken: S12, s13_regel: S13};
const ABSPANN = 8;
export const INTRO = Math.round(3.5 * FPS);   // stille Titelkarte vor Szene 1

let start = INTRO;
const PLAN = Z.reihenfolge.map((id) => {
  const s = Z.szenen[id];
  const frames = Math.round(s.dauer * FPS);
  const e = {id, von: start, frames, s};
  start += frames;
  return e;
});
const abspannVon = start;
export const gesamtFrames = start + ABSPANN * FPS;

const Blende = ({frames, children}) => {
  const f = useCurrentFrame();
  const a = Math.min(glatt(f / 9), glatt((frames - f) / 9));
  return <AbsoluteFill style={{opacity: a}}>{children}</AbsoluteFill>;
};

const Hintergrund = () => (
  <AbsoluteFill style={{background: `radial-gradient(ellipse at 30% 0%, ${F.BG2} 0%, ${F.BG1} 65%)`}}>
    <AbsoluteFill style={{backgroundImage: 'linear-gradient(rgba(148,163,184,.05) 2px, transparent 2px), linear-gradient(90deg, rgba(148,163,184,.05) 2px, transparent 2px)',
      backgroundSize: '80px 80px'}} />
  </AbsoluteFill>
);

const Fortschritt = () => {
  const f = useCurrentFrame();
  return <div style={{position: 'absolute', left: 0, bottom: 0, height: 6, width: `${(100 * f) / gesamtFrames}%`, background: F.CYAN, opacity: 0.8}} />;
};

export const Video = () => {
  const bereit = useSchriften();
  return (
    <AbsoluteFill style={{fontFamily: SCHRIFT, color: F.TEXT}}>
      <Hintergrund />
      {bereit && (
        <Sequence from={0} durationInFrames={INTRO} name="Titelkarte"><Intro frames={INTRO} /></Sequence>
      )}
      {bereit && PLAN.map(({id, von, frames, s}) => {
        const K = KOMP[id];
        return (
          <Sequence key={id} from={von} durationInFrames={frames} name={id}>
            <Blende frames={frames}><K c={s.cues} /><Begriffe liste={s.begriffe} /></Blende>
            <Sequence from={Math.round(s.vorlauf * FPS)} name={`${id} Ton`}>
              <Audio src={staticFile(`${id}.mp3`)} />
            </Sequence>
          </Sequence>
        );
      })}
      {bereit && (
        <Sequence from={abspannVon} durationInFrames={ABSPANN * FPS} name="Abspann">
          <Blende frames={ABSPANN * FPS}><Abspann /></Blende>
        </Sequence>
      )}
      <Fortschritt />
    </AbsoluteFill>
  );
};
