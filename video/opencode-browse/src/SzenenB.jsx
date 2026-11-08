// Szenen 5–8: Passwörter, lokale Modelle, Vergleich, Daten und Regeln
import React from 'react';
import {F, Ein, Chip, Karte, Haken, Kreuz, Warn, Roboter, Browser, Tab, Pfeil, Kopf, Quelle, ein, aus, klemm, glatt, feder, useT} from './lib';

const MONO = 'ui-monospace, "DejaVu Sans Mono", monospace';

// 5 · Gespeicherte Passwörter
export const S05 = ({c}) => {
  const t = useT();
  const punkte = Math.floor(12 * klemm((t - c.tippt - 0.3) / 1.6));
  return (
    <>
      <Kopf t={t} nr="5" titel="Passwörter, ohne dass der Agent sie sieht" />
      <Ein t={t} at={0.3} style={{left: 110, top: 190}}>
        <Browser breite={800} hoehe={500} url="https://shop.example.com/login" tabs={[{el: <Tab aktiv>Anmelden</Tab>}]}>
          <div style={{position: 'absolute', left: 150, top: 46, width: 500}}>
            <div style={{fontSize: 24, color: F.GRAU, marginBottom: 8}}>E-Mail</div>
            <div style={{height: 62, borderRadius: 14, border: `3px solid ${F.RAND}`, color: F.TEXT, fontSize: 26,
              display: 'flex', alignItems: 'center', padding: '0 20px', marginBottom: 22}}>max@example.com</div>
            <div style={{fontSize: 24, color: F.GRAU, marginBottom: 8}}>Passwort</div>
            <div style={{height: 62, borderRadius: 14, border: `3px solid ${t > c.tippt ? F.CYAN : F.RAND}`, color: F.TEXT, fontSize: 34,
              display: 'flex', alignItems: 'center', padding: '0 20px', letterSpacing: 4}}>{'•'.repeat(punkte)}</div>
          </div>
        </Browser>
      </Ein>
      <Ein t={t} at={c.tippt} style={{left: 110, top: 730, width: 800}}>
        <Karte farbe={F.CYAN} style={{display: 'flex', alignItems: 'center', gap: 26, padding: '20px 30px'}}>
          <Roboter g={90} />
          <div>
            <div style={{fontSize: 30, fontWeight: 800, color: F.TEXT}}>Agent tippt das Passwort ein …</div>
            <div style={{fontSize: 26, fontWeight: 600, color: F.CYAN, marginTop: 4}}>… und sieht den Wert nie</div>
          </div>
        </Karte>
      </Ein>
      <Ein t={t} at={c.pruef} style={{left: 1010, top: 200, width: 800}}>
        <div style={{fontSize: 30, fontWeight: 700, color: F.GRAU, marginBottom: 16}}>Vorher prüft das Werkzeug das Feld:</div>
        <div style={{display: 'flex', flexDirection: 'column', gap: 14}}>
          <Chip farbe={F.GRUEN}><Haken g={32} />Feld gehört zu shop.example.com</Chip>
          <div style={{opacity: ein(t, c.pruef + 0.8, 0.4)}}><Chip farbe={F.ROT}><Kreuz g={32} />fremde Seite oder Umleitung: bekommt nichts</Chip></div>
        </div>
      </Ein>
      <Ein t={t} at={c.warnung} style={{left: 1010, top: 470, width: 800}}>
        <Karte farbe={F.GELB} style={{padding: '30px 36px'}}>
          <div style={{display: 'flex', alignItems: 'center', gap: 18}}>
            <Warn g={52} />
            <div style={{fontSize: 32, fontWeight: 800, color: F.GELB}}>Aber nicht hinterlegen: das Geheimnis deiner Authenticator-App</div>
          </div>
          <div style={{fontSize: 26, color: F.GRAU, marginTop: 12}}>daraus entstehen die sechsstelligen Zwei-Faktor-Codes</div>
          <div style={{display: 'flex', alignItems: 'center', gap: 24, marginTop: 26, opacity: ein(t, c.eins, 0.4)}}>
            <div style={{fontSize: 44, fontWeight: 800, color: F.TEXT, position: 'relative'}}>
              2 Faktoren
              <div style={{position: 'absolute', left: -6, top: '52%', height: 6, borderRadius: 3, background: F.ROT,
                width: `${104 * glatt((t - c.eins - 0.4) / 0.5)}%`}} />
            </div>
            <div style={{fontSize: 50, fontWeight: 800, color: F.ROT, opacity: ein(t, c.eins + 0.6, 0.4)}}>→</div>
            <div style={{fontSize: 44, fontWeight: 800, color: F.ROT, opacity: ein(t, c.eins + 0.9, 0.4)}}>1 Faktor</div>
          </div>
        </Karte>
      </Ein>
    </>
  );
};

// 6 · Lokale Modelle und ihre zwei Haken
export const S06 = ({c}) => {
  const t = useT();
  const teilA = aus(t, c.haken - 0.1, 0.5);
  const breiteMax = 1150;
  const balken = [
    ['Ollama-Standard unter 24 GB Grafikspeicher', '4.000', 4, F.ROT, c.k4],
    ['eine einzige Webseite (gemessen bei einem ähnlichen Werkzeug)', '≈ 15.000', 15, F.GELB, c.seite],
    ['Empfehlung von Ollama für Agenten', '64.000', 64, F.GRUEN, c.k64],
  ];
  const schalter = glatt((t - c.an) / 0.4);
  return (
    <>
      <Kopf t={t} nr="6" titel="Jedes Modell, auch lokal" />
      {teilA > 0.01 && (
        <div style={{position: 'absolute', inset: 0, opacity: teilA}}>
          <Ein t={t} at={0.4} style={{left: 160, top: 400}}>
            <Karte farbe={F.BLAU} style={{width: 340, textAlign: 'center'}}>
              <div style={{fontSize: 36, fontWeight: 800, color: F.BLAU}}>OpenCode Browse</div>
              <div style={{fontSize: 24, color: F.GRAU}}>spricht MCP</div>
            </Karte>
          </Ein>
          <Pfeil x={540} y={470} laenge={220} f={ein(t, 1.2, 0.5)} farbe={F.TEXT} />
          <Ein t={t} at={1.6} style={{left: 800, top: 240}}>
            <div style={{display: 'flex', flexDirection: 'column', gap: 24}}>
              <Karte style={{width: 640}}>
                <div style={{fontSize: 32, fontWeight: 800, color: F.TEXT}}>Modell eines Anbieters (Cloud)</div>
                <div style={{fontSize: 24, color: F.GRAU}}>Claude, GPT, Gemini, DeepSeek …</div>
              </Karte>
              <div style={{opacity: 0.35 + 0.65 * ein(t, c.lokal, 0.5)}}>
                <Karte farbe={t > c.lokal ? F.GRUEN : F.RAND} style={{width: 640}}>
                  <div style={{fontSize: 32, fontWeight: 800, color: t > c.lokal ? F.GRUEN : F.TEXT}}>lokales Modell, eigene Grafikkarte</div>
                  <div style={{fontSize: 24, color: F.GRAU}}>z. B. über Ollama oder LM Studio</div>
                </Karte>
              </div>
            </div>
          </Ein>
          <Ein t={t} at={c.nichts} style={{left: 120, top: 210, width: 1380, height: 560}}>
            <div style={{position: 'absolute', left: 0, top: 170, width: 1380, height: 410, border: `4px dashed ${F.GRUEN}`, borderRadius: 34}} />
            <div style={{position: 'absolute', left: 0, top: 600, width: 1380, textAlign: 'center', fontSize: 34, fontWeight: 800, color: F.GRUEN}}>
              Dann verlässt nichts deinen Rechner
            </div>
          </Ein>
        </div>
      )}
      <Ein t={t} at={c.haken} style={{left: 90, top: 150, width: 1740}}>
        <Karte farbe={F.GELB} style={{padding: '26px 40px'}}>
          <div style={{fontSize: 36, fontWeight: 800, color: F.GELB}}>Haken 1 · Kontext, das Arbeitsgedächtnis des Modells</div>
          <div style={{fontSize: 26, color: F.GRAU, marginTop: 4}}>gemessen in Tokens, also Wortstücken</div>
          {balken.map(([s, n, wert, farbe, at]) => (
            <div key={s} style={{marginTop: 18, opacity: ein(t, at - 0.3, 0.4)}}>
              <div style={{fontSize: 25, fontWeight: 600, color: F.GRAU, marginBottom: 6}}>{s}</div>
              <div style={{display: 'flex', alignItems: 'center', gap: 20}}>
                <div style={{width: Math.max(4, breiteMax * wert / 64 * feder((t - at) / (0.6 + wert / 64))), height: 44, borderRadius: 12, background: farbe}} />
                <div style={{fontSize: 34, fontWeight: 800, color: farbe, whiteSpace: 'nowrap'}}>{n} Tokens</div>
              </div>
            </div>
          ))}
          <div style={{marginTop: 16, fontSize: 25, color: F.GRAU, opacity: ein(t, c.k64 + 1.2, 0.5)}}>
            einstellbar mit <span style={{fontFamily: MONO, color: F.TEXT}}>OLLAMA_CONTEXT_LENGTH=64000</span>
          </div>
        </Karte>
      </Ein>
      <Ein t={t} at={c.tools} style={{left: 90, top: 745, width: 1740}}>
        <Karte farbe={F.GELB} style={{padding: '26px 40px', display: 'flex', alignItems: 'center', justifyContent: 'space-between'}}>
          <div>
            <div style={{fontSize: 36, fontWeight: 800, color: F.GELB}}>Haken 2 · Tool-Aufrufe</div>
            <div style={{fontSize: 28, color: F.GRAU, marginTop: 8}}>Befehle wie „klicke hier“: daraus besteht ein Browser-Agent fast nur.</div>
            <div style={{fontSize: 28, color: F.TEXT, marginTop: 4}}>Dein Modell muss sie können, und sie müssen eingeschaltet sein.</div>
          </div>
          <div style={{display: 'flex', alignItems: 'center', gap: 20}}>
            <div style={{width: 130, height: 68, borderRadius: 34, background: schalter > 0.5 ? F.GRUEN : '#334155', position: 'relative'}}>
              <div style={{position: 'absolute', top: 7, left: 7 + 62 * schalter, width: 54, height: 54, borderRadius: 27, background: F.TEXT}} />
            </div>
            <div style={{fontSize: 30, fontWeight: 800, color: schalter > 0.5 ? F.GRUEN : F.ROT, width: 60}}>{schalter > 0.5 ? 'an' : 'aus'}</div>
          </div>
        </Karte>
      </Ein>
      <Quelle t={t} at={c.seite}>Ollama-Doku „Context length“ · Token-Messung mit Playwright MCP (dev.to, Feb. 2026, Einzelmessung: 14.500–19.400 Tokens je Seite)</Quelle>
    </>
  );
};

// 7 · Vergleich mit Claude in Chrome
export const S07 = ({c}) => {
  const t = useT();
  const sp = [280, 720, 640];
  const zeilen = [
    ['Modell', 'nur Claude', 'jedes, auch lokal', c.abo],
    ['Zugang', 'Claude-Abo ab 20 $/Monat, kein API-Schlüssel', 'Abo, API-Schlüssel oder lokal', c.abo + 1.8],
    ['Agenten', 'Claude-Apps und Claude Code', 'OpenCode, Claude Code, Codex, Cursor …', c.claude + 1.4],
    ['Schutz gemessen', 'ja, von Anthropic', 'für dein Modell: nein', c.jedes + 1.6],
  ];
  const kostenSicht = ein(t, c.kosten, 0.5) * aus(t, c.alt - 0.2, 0.4);
  return (
    <>
      <Kopf t={t} nr="7" titel="Und Claude in Chrome?" />
      <Ein t={t} at={0.4} style={{left: 140, top: 150}}>
        <div style={{display: 'flex', borderBottom: `3px solid ${F.RAND}`, paddingBottom: 14}}>
          <div style={{width: sp[0]}} />
          <div style={{width: sp[1], fontSize: 36, fontWeight: 800, color: F.GELB}}>Claude in Chrome</div>
          <div style={{width: sp[2], fontSize: 36, fontWeight: 800, color: F.CYAN, opacity: ein(t, c.jedes - 0.3, 0.4)}}>OpenCode Browse</div>
        </div>
        {zeilen.map(([a, b, d, at], i) => (
          <div key={a} style={{display: 'flex', alignItems: 'center', minHeight: 84, padding: '8px 0', borderBottom: `2px solid ${F.KARTE2}`,
            background: kostenSicht > 0.01 && i === 1 ? `rgba(251,191,36,${0.12 * kostenSicht})` : 'none'}}>
            <div style={{width: sp[0], fontSize: 28, fontWeight: 700, color: F.GRAU, opacity: ein(t, Math.min(at, c.jedes + i * 0.4), 0.4)}}>{a}</div>
            <div style={{width: sp[1] - 30, marginRight: 30, fontSize: 29, fontWeight: 700, color: F.TEXT, lineHeight: 1.2, opacity: ein(t, at, 0.4)}}>{b}</div>
            <div style={{width: sp[2], fontSize: 29, fontWeight: 700, color: F.TEXT, lineHeight: 1.2, opacity: ein(t, c.jedes + i * 0.4, 0.4)}}>{d}</div>
          </div>
        ))}
      </Ein>
      {kostenSicht > 0.01 && (
        <div style={{position: 'absolute', left: 140, top: 700, width: 1640, opacity: kostenSicht}}>
          <Karte farbe={F.GELB} style={{display: 'flex', alignItems: 'center', gap: 26}}>
            <Warn g={60} />
            <div>
              <div style={{fontSize: 38, fontWeight: 800, color: F.GELB}}>Kostenlos ist nur das Werkzeug.</div>
              <div style={{fontSize: 30, color: F.TEXT, marginTop: 6}}>Das Modell kostet weiter Geld, außer es läuft bei dir lokal.</div>
            </div>
          </Karte>
        </div>
      )}
      <Ein t={t} at={c.alt} style={{left: 140, top: 700, display: 'flex', alignItems: 'center', gap: 20}}>
        <div style={{fontSize: 30, fontWeight: 700, color: F.GRAU, width: 380}}>können das auch</div>
        <Chip farbe={F.GRAU}>Playwright MCP (Microsoft)</Chip>
        <Chip farbe={F.GRAU}>Chrome DevTools MCP (Google)</Chip>
      </Ein>
      <Ein t={t} at={c.neu} style={{left: 140, top: 820, display: 'flex', alignItems: 'center', gap: 20}}>
        <div style={{fontSize: 30, fontWeight: 800, color: F.CYAN, width: 380}}>neu: Komplettpaket</div>
        {['eine Installation', 'Übergaben', 'Passwörter', 'Aufzeichnung'].map((s, i) => (
          <div key={s} style={{opacity: ein(t, c.neu + 0.8 + i * 0.5, 0.35)}}><Chip farbe={F.CYAN}>{s}</Chip></div>
        ))}
      </Ein>
      <Quelle t={t} at={c.abo}>code.claude.com/docs/en/chrome · claude.com/pricing (Pro 20 $/Monat, monatlich) · Stand 08.11.2026</Quelle>
    </>
  );
};

// kleine Symbole für Szene 8
const Brief = ({g = 64, farbe = F.TEXT}) => (
  <svg width={g} height={g * 0.75} viewBox="0 0 32 24">
    <rect x="1.5" y="1.5" width="29" height="21" rx="3" fill="none" stroke={farbe} strokeWidth="2.5" />
    <path d="M2.5 3.5L16 13.5L29.5 3.5" fill="none" stroke={farbe} strokeWidth="2.5" strokeLinejoin="round" />
  </svg>
);
const Wolke = ({g = 90, farbe = F.BLAU}) => (
  <svg width={g} height={g * 0.66} viewBox="0 0 48 32">
    <path d="M12 30h26a9 9 0 0 0 1-17.9A12 12 0 0 0 16 9.5 8 8 0 0 0 12 30z" fill={farbe} />
  </svg>
);
const Chipkarte = ({g = 80, farbe = F.GRUEN}) => (
  <svg width={g} height={g} viewBox="0 0 32 32">
    <rect x="7" y="7" width="18" height="18" rx="3" fill={farbe} />
    {[10, 16, 22].map((v) => <g key={v}>
      <line x1={v} y1="2" x2={v} y2="7" stroke={farbe} strokeWidth="2" /><line x1={v} y1="25" x2={v} y2="30" stroke={farbe} strokeWidth="2" />
      <line x1="2" y1={v} x2="7" y2={v} stroke={farbe} strokeWidth="2" /><line x1="25" y1={v} x2="30" y2={v} stroke={farbe} strokeWidth="2" />
    </g>)}
  </svg>
);
const Knoten = ({icon, titel, farbe}) => (
  <div style={{width: 210, height: 170, borderRadius: 24, background: F.KARTE, border: `3px solid ${farbe}`, display: 'flex',
    flexDirection: 'column', alignItems: 'center', justifyContent: 'center', gap: 10}}>
    {icon}
    <div style={{fontSize: 25, fontWeight: 800, color: farbe, textAlign: 'center', lineHeight: 1.15, padding: '0 10px'}}>{titel}</div>
  </div>
);

// 8 · Datenschutz und Regeln
export const S08 = ({c}) => {
  const t = useT();
  const X0 = 90, Y1 = 260, Y2 = 590;
  const xs = [0, 315, 630].map((x) => X0 + x);
  const flug = klemm((t - c.mails) / 2.2);
  return (
    <>
      <Kopf t={t} nr="8" titel="Zwei Dinge, die oft untergehen" farbe={F.VIOLETT} />
      <Ein t={t} at={c.daten} style={{left: X0, top: 165}}>
        <div style={{fontSize: 36, fontWeight: 800, color: F.VIOLETT}}>1 · Datenschutz</div>
      </Ein>
      <Ein t={t} at={c.daten + 0.6} style={{left: 0, top: 0, width: 1000, height: 1080}}>
        {[[<Brief g={64} />, 'dein Postfach', F.TEXT], [<Roboter g={70} />, 'Agent liest', F.CYAN], [<Wolke g={90} />, 'Modell-Anbieter (Cloud)', F.BLAU]]
          .map(([icon, s, farbe], i) => <div key={s} style={{position: 'absolute', left: xs[i], top: Y1}}><Knoten icon={icon} titel={s} farbe={farbe} /></div>)}
        <Pfeil x={xs[0] + 220} y={Y1 + 85} laenge={85} farbe={F.TEXT} />
        <Pfeil x={xs[1] + 220} y={Y1 + 85} laenge={85} farbe={F.TEXT} />
      </Ein>
      {t > c.mails && flug < 1 && [0, 1, 2].map((k) => {
        const f = klemm(flug * 1.4 - k * 0.2);
        return <div key={k} style={{position: 'absolute', left: xs[0] + 70 + f * 630, top: Y1 + 40 - Math.sin(Math.PI * f) * 60, opacity: f > 0 && f < 1 ? 1 : 0}}>
          <Brief g={50} farbe={F.ROT} /></div>;
      })}
      <Ein t={t} at={c.mails + 0.8} style={{left: X0, top: Y1 + 190, width: 840}}>
        <Chip farbe={F.ROT} gross={26}>deine Mails, samt Daten anderer Leute</Chip>
      </Ein>
      <Ein t={t} at={c.lokal} style={{left: 0, top: 0, width: 1000, height: 1080}}>
        {[[<Brief g={64} />, 'dein Postfach', F.TEXT], [<Roboter g={70} farbe={F.GRUEN} />, 'Agent liest', F.GRUEN], [<Chipkarte g={70} />, 'lokales Modell', F.GRUEN]]
          .map(([icon, s, farbe], i) => <div key={s} style={{position: 'absolute', left: xs[i], top: Y2}}><Knoten icon={icon} titel={s} farbe={farbe} /></div>)}
        <Pfeil x={xs[0] + 220} y={Y2 + 85} laenge={85} farbe={F.GRUEN} />
        <Pfeil x={xs[1] + 220} y={Y2 + 85} laenge={85} farbe={F.GRUEN} />
        <div style={{position: 'absolute', left: X0 - 20, top: Y2 - 20, width: 880, height: 210, border: `4px dashed ${F.GRUEN}`, borderRadius: 30}} />
        <div style={{position: 'absolute', left: X0, top: Y2 + 210, fontSize: 30, fontWeight: 800, color: F.GRUEN}}>bleibt auf deinem Rechner</div>
      </Ein>
      <div style={{position: 'absolute', left: 1005, top: 170, width: 4, height: 760, background: F.KARTE2, opacity: ein(t, c.regeln - 0.3, 0.4)}} />
      <Ein t={t} at={c.regeln} style={{left: 1060, top: 165}}>
        <div style={{fontSize: 36, fontWeight: 800, color: F.VIOLETT}}>2 · Regeln</div>
      </Ein>
      <Ein t={t} at={c.linkedin - 0.6} style={{left: 1060, top: 260, width: 770}}>
        <Karte farbe={F.GELB}>
          <div style={{fontSize: 32, fontWeight: 800, color: F.TEXT}}>Nutzungsbedingungen</div>
          <div style={{fontSize: 28, color: F.GELB, fontWeight: 700, marginTop: 8}}>Bots oft verboten, z. B. bei LinkedIn</div>
        </Karte>
      </Ein>
      <Ein t={t} at={c.bank} style={{left: 1060, top: 480, width: 770}}>
        <Karte farbe={F.ROT}>
          <div style={{fontSize: 32, fontWeight: 800, color: F.TEXT}}>Online-Banking</div>
          <div style={{fontSize: 28, color: F.ROT, fontWeight: 700, marginTop: 8}}>grob fahrlässig gehandelt → du haftest selbst</div>
          <div style={{fontSize: 22, color: F.GRAU, marginTop: 10}}>Beispiel: Bedingungen für das Online-Banking einer Sparkasse</div>
        </Karte>
      </Ein>
      <Quelle t={t} at={c.linkedin}>Datenschutzerklärung von Browse: Inhalte gehen an den Modellanbieter, den du einstellst · LinkedIn User Agreement · keine Rechtsberatung</Quelle>
    </>
  );
};
