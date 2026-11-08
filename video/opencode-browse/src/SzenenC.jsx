// Szenen 9–11 und Abspann: Schutz, Haken, Faustregel, Quellen
import React from 'react';
import {F, Ein, Chip, Karte, Haken, Kreuz, Warn, Schloss, Kopf, ein, aus, glatt, feder, useT} from './lib';

const MONO = 'ui-monospace, "DejaVu Sans Mono", monospace';

// 9 · Was Browse selbst absichert
export const S09 = ({c}) => {
  const t = useT();
  const punkte = [
    [c.relay, 'Relay nur auf deinem Rechner erreichbar', 'und nur mit geheimem Schlüssel', F.GRUEN, 'ok'],
    [c.code, 'Kopplungscode: gilt einmal, 10 Minuten lang', 'danach hat jeder Browser einen eigenen Schlüssel', F.GRUEN, 'ok'],
    [c.cookies, 'Cookies löschen, Browser schließen: verboten', 'Cookies nur für die Seiten des Agenten', F.GRUEN, 'ok'],
    [c.liste, 'Liste erlaubter Seiten: möglich', 'ab Werk ausgeschaltet', F.GELB, 'warn'],
  ];
  return (
    <>
      <Kopf t={t} nr="9" titel="Was Browse selbst absichert" farbe={F.GRUEN} />
      {punkte.map(([at, a, b, farbe, art], i) => (
        <Ein key={a} t={t} at={at} dx={-30} dy={0} style={{left: 140, top: 165 + i * 132, width: 1640}}>
          <Karte farbe={farbe} style={{display: 'flex', alignItems: 'center', gap: 28, padding: '20px 34px'}}>
            {art === 'ok' ? <Haken g={50} /> : <Warn g={50} />}
            <div>
              <div style={{fontSize: 34, fontWeight: 800, color: F.TEXT}}>{a}</div>
              <div style={{fontSize: 26, color: F.GRAU, marginTop: 2}}>{b}</div>
            </div>
          </Karte>
        </Ein>
      ))}
      <Ein t={t} at={c.zitat} skala style={{left: 140, top: 735, width: 1640}}>
        <div style={{borderLeft: `10px solid ${F.ROT}`, padding: '18px 0 18px 40px'}}>
          <div style={{fontSize: 46, fontWeight: 800, color: F.TEXT, lineHeight: 1.25}}>
            „Behandle Code, den der Agent ausführt, wie Code, der als du läuft.“
          </div>
          <div style={{fontSize: 24, color: F.GRAU, marginTop: 12}}>sinngemäß aus der Browse-Dokumentation („treat code an agent runs as code running as you“)</div>
        </div>
      </Ein>
    </>
  );
};

// 10 · Praktische Haken
export const S10 = ({c}) => {
  const t = useT();
  const ja = ['Chrome', 'Edge', 'Brave', 'Arc', 'Vivaldi', 'Opera', 'Helium'];
  return (
    <>
      <Kopf t={t} nr="10" titel="Zwei praktische Haken" farbe={F.GELB} />
      <Ein t={t} at={c.chromium} style={{left: 140, top: 200}}>
        <div style={{fontSize: 34, fontWeight: 800, color: F.TEXT, marginBottom: 20}}>Nur Chromium-Browser</div>
        <div style={{display: 'flex', gap: 16, flexWrap: 'wrap', width: 1640}}>
          {ja.map((s, i) => <div key={s} style={{opacity: ein(t, c.chromium + 0.3 + i * 0.22, 0.3)}}><Chip farbe={F.GRUEN}><Haken g={30} />{s}</Chip></div>)}
        </div>
      </Ein>
      <Ein t={t} at={c.nicht} style={{left: 140, top: 400, display: 'flex', gap: 16}}>
        <Chip farbe={F.ROT}><Kreuz g={30} />Firefox</Chip>
        <Chip farbe={F.ROT}><Kreuz g={30} />Safari</Chip>
      </Ein>
      <Ein t={t} at={c.neu} style={{left: 140, top: 560, width: 1640}}>
        <Karte farbe={F.GELB} style={{display: 'flex', alignItems: 'center', gap: 50, padding: '34px 44px'}}>
          <div style={{fontSize: 110, fontWeight: 800, color: F.GELB, fontFamily: MONO, letterSpacing: -4}}>0.0.15</div>
          <div>
            <div style={{fontSize: 36, fontWeight: 800, color: F.TEXT}}>brandneu: Ecken und Kanten einplanen</div>
            <div style={{fontSize: 28, color: F.GRAU, marginTop: 8, opacity: ein(t, c.neu + 1.8, 0.4)}}>
              Updates spielt es ab Werk selbst ein (Prüfung mindestens stündlich, abschaltbar)
            </div>
          </div>
        </Karte>
      </Ein>
    </>
  );
};

// 11 · Faustregel und Fazit
export const S11 = ({c}) => {
  const t = useT();
  const teilA = aus(t, c.fazit - 0.2, 0.5);
  const regeln = [
    [c.r1, 'Eigenes Browserprofil', 'nicht dein Hauptbrowser mit Bank und E-Mail'],
    [c.r2, 'Liste erlaubter Seiten an', 'ab Werk ist sie aus'],
    [c.r3, 'Geld und Passwörter: du', 'per Übergabe selbst erledigen'],
  ];
  const stempel = feder((t - c.vorsicht) / 0.6);
  return (
    <>
      <Kopf t={t} nr="11" titel={t < c.fazit ? 'Die Faustregel' : 'Kurz gesagt'} />
      {teilA > 0.01 && (
        <div style={{position: 'absolute', inset: 0, opacity: teilA}}>
          {regeln.map(([at, a, b], i) => (
            <Ein key={a} t={t} at={at} skala style={{left: 120 + i * 573, top: 290}}>
              <Karte farbe={F.CYAN} style={{width: 530, height: 420, display: 'flex', flexDirection: 'column', gap: 24}}>
                <div style={{width: 84, height: 84, borderRadius: 24, background: F.CYAN, color: F.BG1, fontSize: 50, fontWeight: 800,
                  display: 'flex', alignItems: 'center', justifyContent: 'center'}}>{i + 1}</div>
                <div style={{fontSize: 44, fontWeight: 800, color: F.TEXT, lineHeight: 1.15}}>{a}</div>
                <div style={{fontSize: 28, color: F.GRAU, lineHeight: 1.3}}>{b}</div>
              </Karte>
            </Ein>
          ))}
        </div>
      )}
      {[[c.f1, 'Du zahlst schon für Claude und Chrome reicht dir', 'Claude in Chrome', F.GELB],
        [c.f2, 'Eigenes Modell, lokal oder andere Agenten', 'OpenCode Browse', F.CYAN]].map(([at, a, b, farbe], i) => (
        <Ein key={b} t={t} at={at} dy={30} style={{left: 140 + i * 840, top: 260}}>
          <Karte farbe={farbe} style={{width: 800, height: 400, display: 'flex', flexDirection: 'column', justifyContent: 'space-between'}}>
            <div style={{fontSize: 38, fontWeight: 700, color: F.TEXT, lineHeight: 1.25}}>{a}</div>
            <div>
              <div style={{fontSize: 60, color: farbe, fontWeight: 800}}>→ {b}</div>
              <div style={{fontSize: 28, color: F.GRAU, marginTop: 6}}>{i === 1 ? 'das Werkzeug kostet nichts' : 'im Abo enthalten'}</div>
            </div>
          </Karte>
        </Ein>
      ))}
      {t > c.vorsicht && (
        <div style={{position: 'absolute', left: 1180, top: 700, transform: `rotate(-6deg) scale(${0.6 + 0.4 * stempel})`, opacity: glatt((t - c.vorsicht) / 0.3)}}>
          <div style={{border: `6px solid ${F.GELB}`, borderRadius: 20, padding: '14px 40px', fontSize: 64, fontWeight: 800, color: F.GELB}}>mit Vorsicht</div>
        </div>
      )}
    </>
  );
};

// Abspann ohne Ton
export const Abspann = () => {
  const t = useT();
  const q = [
    'github.com/anomalyco/browse (README, Abschnitte Security und How it works)',
    'opencode.ai/product/browse · npm @opencode/browse (Version 0.0.15)',
    'anthropic.com/news/claude-for-chrome (Aug. 2025)',
    'anthropic.com/research/prompt-injection-defenses (Nov. 2025)',
    'docs.ollama.com/context-length',
  ];
  return (
    <>
      <Ein t={t} at={0.2} style={{left: 140, top: 150}}>
        <div style={{fontSize: 56, fontWeight: 800, color: F.TEXT}}>Quellen</div>
        <div style={{fontSize: 28, color: F.GRAU, marginTop: 6}}>Stand 08.11.2026 · alle Angaben ohne Gewähr, das Projekt ändert sich täglich</div>
      </Ein>
      {q.map((s, i) => (
        <Ein key={s} t={t} at={0.5 + i * 0.25} style={{left: 140, top: 330 + i * 80}}>
          <div style={{fontSize: 32, fontWeight: 600, color: F.TEXT}}><span style={{color: F.CYAN}}>›</span> {s}</div>
        </Ein>
      ))}
      <Ein t={t} at={2} style={{left: 140, top: 820}}>
        <div style={{fontSize: 26, color: F.GRAU}}>Angeregt durch das Video von ZeldoReacts (Reaktion auf Hinter). Text und Grafik eigenständig erstellt.</div>
      </Ein>
    </>
  );
};
