// Szenen 1–4: Problem, Lösung, Staffellauf, Übergabe
import React from 'react';
import {F, Ein, Chip, Karte, Haken, Kreuz, Schloss, Roboter, Mensch, Browser, Tab, Pfeil, Kopf, ein, aus, klemm, glatt, feder, useT} from './lib';

const Zeile = ({breite, farbe = '#24314f', h = 18, style}) => (
  <div style={{width: breite, height: h, borderRadius: h / 2, background: farbe, ...style}} />
);

// 1 · Die Login-Wand
export const S01 = ({c}) => {
  const t = useT();
  const stoss = klemm((t - c.login) / 0.5);
  const robX = Math.sin(Math.PI * stoss) * 90 - (t > c.login + 0.5 ? Math.sin((t - c.login - 0.5) * 30) * 6 * aus(t, c.login + 0.5, 0.5) : 0);
  const aufgaben = [
    ['Ganze App bauen', c.app, true],
    ['Dashboard prüfen', c.login + 0.2, false],
    ['E-Mail beantworten', c.login + 0.5, false],
  ];
  return (
    <>
      <Kopf t={t} nr="1" titel="Das Problem: die Login-Wand" />
      <div style={{position: 'absolute', left: 150 + robX, top: 210}}><Roboter g={190} blick={stoss > 0 ? 1 : 0} /></div>
      <Ein t={t} at={0.4} style={{left: 370, top: 250}}>
        <div style={{fontSize: 40, fontWeight: 800, color: F.TEXT}}>Dein KI-Agent</div>
        <div style={{fontSize: 28, fontWeight: 500, color: F.GRAU, marginTop: 6}}>Aufgaben</div>
      </Ein>
      {aufgaben.map(([s, at, ok], i) => (
        <Ein key={s} t={t} at={at} dx={-30} dy={0} style={{left: 130, top: 470 + i * 118}}>
          <Karte farbe={ok ? F.GRUEN : F.ROT} style={{width: 560, padding: '22px 30px', display: 'flex', alignItems: 'center', gap: 22}}>
            {ok ? <Haken g={44} /> : <Kreuz g={44} />}
            <div style={{fontSize: 36, fontWeight: 700, color: F.TEXT}}>{s}</div>
          </Karte>
        </Ein>
      ))}
      <Ein t={t} at={c.login - 0.3} dx={40} dy={0} style={{left: 880, top: 190}}>
        <Browser breite={920} hoehe={600} url="https://dashboard.example.com/login" tabs={[{el: <Tab aktiv>Anmelden</Tab>}]}>
          <div style={{position: 'absolute', left: 230, top: 50, width: 460}}>
            <div style={{display: 'flex', justifyContent: 'center', transform: `scale(${1 + 0.25 * Math.sin(Math.PI * stoss)})`}}><Schloss g={84} /></div>
            <div style={{fontSize: 38, fontWeight: 800, color: F.TEXT, textAlign: 'center', margin: '14px 0 26px'}}>Anmelden</div>
            {['E-Mail', 'Passwort'].map((s) => (
              <div key={s} style={{height: 62, borderRadius: 14, border: `3px solid ${F.RAND}`, marginBottom: 18, color: F.DUNKEL,
                fontSize: 26, display: 'flex', alignItems: 'center', padding: '0 20px'}}>{s}</div>
            ))}
            <div style={{height: 62, borderRadius: 14, background: F.BLAU, color: F.BG1, fontSize: 28, fontWeight: 800,
              display: 'flex', alignItems: 'center', justifyContent: 'center'}}>Anmelden</div>
          </div>
        </Browser>
      </Ein>
      <Ein t={t} at={c.leer} style={{left: 880, top: 830, width: 920}}>
        <div style={{fontSize: 34, fontWeight: 800, color: F.TEXT, marginBottom: 18}}>Agenten-Browser: frisch und leer</div>
      </Ein>
      <Ein t={t} at={c.keine} style={{left: 880, top: 900}}>
        <div style={{display: 'flex', gap: 20}}>
          <Chip farbe={F.ROT}><Kreuz g={30} />keine Cookies</Chip>
          <Chip farbe={F.ROT}><Kreuz g={30} />keine Anmeldung</Chip>
        </div>
      </Ein>
    </>
  );
};

// 2 · Die Lösung
export const S02 = ({c}) => {
  const t = useT();
  const zentriert = {left: 0, width: 1920, display: 'flex', justifyContent: 'center', gap: 24};
  const agenten = ['OpenCode', 'Claude Code', 'Codex', 'Cursor', 'Gemini CLI', 'Zed', '+ viele mehr'];
  return (
    <>
      <Kopf t={t} nr="2" titel="Die Lösung" />
      <Ein t={t} at={c.titel} skala style={{...zentriert, top: 150, flexDirection: 'column', alignItems: 'center'}}>
        <div style={{fontSize: 112, fontWeight: 800, color: F.CYAN, letterSpacing: -3}}>OpenCode Browse</div>
        <div style={{fontSize: 38, fontWeight: 500, color: F.GRAU}}>dein echter Browser für KI-Agenten</div>
      </Ein>
      <Ein t={t} at={c.firma} style={{...zentriert, top: 375}}>
        <div style={{fontSize: 30, fontWeight: 600, color: F.TEXT}}>von <span style={{color: F.CYAN, fontWeight: 800}}>Anomaly</span>, der Firma hinter dem Coding-Agenten OpenCode</div>
      </Ein>
      <Ein t={t} at={c.bausteine} style={{...zentriert, top: 450, alignItems: 'center', gap: 40}}>
        <Karte style={{width: 520, textAlign: 'center'}}>
          <div style={{fontSize: 36, fontWeight: 800, color: F.TEXT}}>Browser-Erweiterung</div>
          <div style={{fontSize: 26, color: F.GRAU, marginTop: 6}}>für Chrome und Co.</div>
        </Karte>
        <div style={{fontSize: 70, fontWeight: 800, color: F.GRAU}}>+</div>
        <Karte style={{width: 520, textAlign: 'center'}}>
          <div style={{fontSize: 36, fontWeight: 800, color: F.TEXT}}>kleines Hilfsprogramm</div>
          <div style={{fontSize: 26, color: F.GRAU, marginTop: 6}}>auf deinem Rechner</div>
        </Karte>
      </Ein>
      <Ein t={t} at={c.frei} style={{...zentriert, top: 640}}>
        {[['gerade erschienen (Nov. 2026)', c.frei], ['Open Source (MIT)', c.frei + 1.0], ['kostenlos', c.frei + 1.8]].map(([s, at]) => (
          <div key={s} style={{opacity: ein(t, at, 0.4)}}><Chip farbe={F.GRUEN}>{s}</Chip></div>
        ))}
      </Ein>
      <Ein t={t} at={c.echt} style={{...zentriert, top: 740}}>
        {['deine Tabs', 'deine Logins', 'deine Erweiterungen'].map((s, i) => (
          <div key={s} style={{opacity: ein(t, c.echt + i * 0.6, 0.4)}}><Chip farbe={F.VIOLETT} gross={34}>{s}</Chip></div>
        ))}
      </Ein>
      <Ein t={t} at={c.agenten} style={{...zentriert, top: 865, alignItems: 'center', gap: 16}}>
        <div style={{fontSize: 30, fontWeight: 700, color: F.GRAU, marginRight: 8}}>läuft mit</div>
        {agenten.map((s, i) => (
          <div key={s} style={{opacity: ein(t, c.agenten + 0.6 + i * 0.35, 0.35)}}>
            <Chip farbe={i === agenten.length - 1 ? F.GRAU : F.CYAN} gross={28}>{s}</Chip>
          </div>
        ))}
      </Ein>
    </>
  );
};

// 3 · Staffellauf: Agent → Server → Relay → Erweiterung → Chrome
const KNOTEN = [
  {titel: 'Agent', unter: 'z. B. Claude Code', farbe: F.CYAN},
  {titel: 'Server', unter: 'Hilfsprogramm', farbe: F.BLAU},
  {titel: 'Relay', unter: 'Vermittlungsstelle', farbe: F.VIOLETT},
  {titel: 'Erweiterung', unter: 'in deinem Browser', farbe: F.ROSA},
  {titel: 'Chrome', unter: 'eingebaute Fernsteuerung', farbe: F.GRUEN},
];
const PFEILE = ['MCP-Stecker', 'Befehl', 'Leitung', 'Steuerung'];
export const S03 = ({c}) => {
  const t = useT();
  const W = 250, G = 135, X0 = 65, Y = 480, H = 200;
  const xs = KNOTEN.map((_, i) => X0 + i * (W + G));
  const knotenAb = [c.n1, c.n1 + 0.5, c.n2, c.n3, c.n4];
  const pfeilAb = [c.n1 + 1.0, c.n2 + 0.6, c.n3 + 0.6, c.n4 + 0.6];
  // Staffelstab: läuft nach "viertens" hin und zurück
  const lauf = t - (c.n4 + 1.4);
  const zyklus = 3.2;
  let stab = null;
  if (lauf > 0) {
    const ph = (lauf % zyklus) / zyklus;
    const hin = ph < 0.5;
    const f = glatt(hin ? ph * 2 : (ph - 0.5) * 2);
    const xa = xs[0] + W / 2, xb = xs[4] + W / 2;
    stab = {x: hin ? xa + (xb - xa) * f : xb - (xb - xa) * f, farbe: hin ? F.GELB : F.GRUEN};
  }
  return (
    <>
      <Kopf t={t} nr="3" titel="So kommt der Agent in deinen Browser" />
      <Ein t={t} at={c.n2 + 0.9} style={{left: xs[1] - 30, top: Y - 70, width: xs[2] + W - xs[1] + 60, height: H + 230}}>
        <div style={{width: '100%', height: '100%', border: `3px dashed ${F.VIOLETT}`, borderRadius: 30}} />
        <div style={{position: 'absolute', bottom: 18, width: '100%', textAlign: 'center', fontSize: 26, fontWeight: 700, color: F.VIOLETT}}>
          nur auf deinem Rechner erreichbar
        </div>
      </Ein>
      {stab && (
        <div style={{position: 'absolute', left: stab.x - 16, top: Y + H / 2 - 16, width: 32, height: 32, borderRadius: 16,
          background: stab.farbe, boxShadow: `0 0 30px ${stab.farbe}`}} />
      )}
      {KNOTEN.map((k, i) => (
        <Ein key={k.titel} t={t} at={knotenAb[i]} skala style={{left: xs[i], top: Y}}>
          <div style={{width: W, height: H, borderRadius: 26, background: F.KARTE, border: `4px solid ${k.farbe}`,
            display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', gap: 10,
            boxShadow: `0 0 ${stab && Math.abs(stab.x - (xs[i] + W / 2)) < 60 ? 40 : 0}px ${k.farbe}`}}>
            {i === 0 && <Roboter g={74} />}
            <div style={{fontSize: 34, fontWeight: 800, color: k.farbe, whiteSpace: 'nowrap'}}>{k.titel}</div>
            <div style={{fontSize: 22, fontWeight: 500, color: F.GRAU, textAlign: 'center', padding: '0 12px'}}>{k.unter}</div>
          </div>
        </Ein>
      ))}
      {PFEILE.map((s, i) => {
        const x = xs[i] + W + 12, L = G - 24;
        return (
          <React.Fragment key={s}>
            <Pfeil x={x} y={Y + H / 2} laenge={L} f={ein(t, pfeilAb[i], 0.5)} farbe={F.TEXT} doppelt />
            <Ein t={t} at={pfeilAb[i] + 0.2} style={{left: x - 20, top: Y + H / 2 + 30, width: L + 40, textAlign: 'center'}}>
              <div style={{fontSize: 22, fontWeight: 700, color: F.GRAU}}>{s}</div>
            </Ein>
            <Ein t={t} at={pfeilAb[i] - 0.3} skala style={{left: x + L / 2 - 30, top: Y + H / 2 - 100}}>
              <div style={{width: 60, height: 60, borderRadius: 30, background: F.GELB, color: F.BG1, fontSize: 32, fontWeight: 800,
                display: 'flex', alignItems: 'center', justifyContent: 'center'}}>{i + 1}</div>
            </Ein>
          </React.Fragment>
        );
      })}
      <Ein t={t} at={c.n1 + 0.2} style={{left: 0, width: 1920, top: 290, textAlign: 'center'}}>
        <div style={{fontSize: 34, fontWeight: 600, color: F.GRAU}}>vier Stationen, jeder Befehl läuft wie ein Staffelstab hindurch</div>
      </Ein>
      <Ein t={t} at={c.aktionen} style={{left: 0, width: 1920, top: 870, display: 'flex', justifyContent: 'center', gap: 22}}>
        {['klicken', 'tippen', 'scrollen', 'lesen'].map((s, i) => (
          <div key={s} style={{opacity: ein(t, c.aktionen + i * 0.45, 0.35)}}><Chip farbe={F.GRUEN} gross={34}>{s}</Chip></div>
        ))}
      </Ein>
    </>
  );
};

// 4 · Tabs im Hintergrund und Übergabe
export const S04 = ({c}) => {
  const t = useT();
  const aktiv = t < c.du ? 0 : t < c.agent ? 1 : 2;
  const rollen = [
    {el: <Roboter g={130} />, text: 'Agent arbeitet', farbe: F.CYAN},
    {el: <Mensch g={130} />, text: 'Du erledigst den heiklen Teil', farbe: F.GELB},
    {el: <Roboter g={130} farbe={F.GRUEN} />, text: 'Agent macht weiter', farbe: F.GRUEN},
  ];
  const rx = [300, 960, 1620];
  const druck = t > c.weiter && t < c.weiter + 0.35 ? 0.9 : 1;
  const karteSicht = ein(t, c.faelle, 0.4) * aus(t, c.agent, 0.4);
  return (
    <>
      <Kopf t={t} nr="4" titel="Im Hintergrund, mit Übergabe an dich" />
      <Ein t={t} at={c.tabs} style={{left: 210, top: 150}}>
        <Browser breite={1500} hoehe={420} url="https://mail.example.com" tabs={[
          {el: <Tab aktiv>Posteingang</Tab>}, {el: <Tab>Kalender</Tab>},
          {el: <div style={{height: 44, display: 'flex', alignItems: 'center', opacity: ein(t, c.tabs + 1.2, 0.4)}}>
            <Chip farbe={F.VIOLETT} gross={22} gefuellt>Agents · 3</Chip></div>},
        ]}>
          <div style={{position: 'absolute', left: 40, top: 40, display: 'flex', flexDirection: 'column', gap: 22, opacity: 1 - 0.6 * karteSicht}}>
            <Zeile breite={620} /><Zeile breite={880} /><Zeile breite={760} /><Zeile breite={540} /><Zeile breite={700} />
          </div>
          <Ein t={t} at={c.zehn} style={{right: 40, top: 30}}>
            <Chip farbe={F.VIOLETT} gross={26}>Agenten-Tabs: eingeklappt · nach 10 min Leerlauf zu</Chip>
          </Ein>
          {karteSicht > 0.01 && (
            <div style={{position: 'absolute', left: 300, top: 105, width: 660, opacity: karteSicht,
              transform: `translateY(${(1 - karteSicht) * 20}px)`}}>
              <Karte farbe={F.GELB} style={{padding: '24px 32px'}}>
                <div style={{fontSize: 34, fontWeight: 800, color: F.GELB}}>Du bist dran</div>
                <div style={{fontSize: 26, color: F.GRAU, margin: '6px 0 18px'}}>login.example.com · Anmeldung mit 2-Faktor</div>
                <div style={{display: 'inline-block', padding: '12px 34px', borderRadius: 14, background: F.GELB, color: F.BG1,
                  fontSize: 28, fontWeight: 800, transform: `scale(${druck})`}}>Weiter</div>
              </Karte>
            </div>
          )}
        </Browser>
      </Ein>
      <Ein t={t} at={c.uebergabe} style={{left: 0, top: 610, width: 1920, height: 400}}>
        {rollen.map((r, i) => {
          const an = i === aktiv;
          return (
            <div key={i} style={{position: 'absolute', left: rx[i] - 150, top: 0, width: 300, display: 'flex', flexDirection: 'column',
              alignItems: 'center', opacity: an ? 1 : 0.35, transform: `scale(${an ? 1.06 : 0.94})`}}>
              <div style={{filter: an ? `drop-shadow(0 0 22px ${r.farbe})` : 'none'}}>{r.el}</div>
              <div style={{fontSize: 30, fontWeight: 800, color: an ? r.farbe : F.GRAU, textAlign: 'center', marginTop: 10}}>{r.text}</div>
            </div>
          );
        })}
        <Pfeil x={rx[0] + 170} y={80} laenge={rx[1] - rx[0] - 340} f={ein(t, c.faelle, 0.6)} farbe={F.GELB} />
        <Pfeil x={rx[1] + 170} y={80} laenge={rx[2] - rx[1] - 340} f={ein(t, c.weiter, 0.6)} farbe={F.GRUEN} />
        <div style={{position: 'absolute', left: rx[0] + 115, width: rx[1] - rx[0] - 230, top: 6, display: 'flex',
          justifyContent: 'center', gap: 8}}>
          {['Login', '2-Faktor', 'Captcha', 'Zahlung'].map((s, i) => (
            <div key={s} style={{opacity: ein(t, c.faelle + 0.3 + i * 0.5, 0.35)}}><Chip farbe={F.GELB} gross={20}>{s}</Chip></div>
          ))}
        </div>
        <div style={{position: 'absolute', left: rx[1] + 150, width: rx[2] - rx[1] - 300, top: 0, display: 'flex',
          justifyContent: 'center', opacity: ein(t, c.weiter, 0.35)}}>
          <Chip farbe={F.GRUEN} gross={24}>Klick auf „Weiter“</Chip>
        </div>
      </Ein>
    </>
  );
};
