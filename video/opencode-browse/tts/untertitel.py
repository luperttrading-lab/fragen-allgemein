"""Untertitel (SRT + WebVTT) aus Sprechtext und ElevenLabs-Zeitmarken.

Aufruf: python3 -I tts/untertitel.py   -> untertitel/opencode-browse.de.srt und .vtt
Regeln: höchstens 2 Zeilen à 42 Zeichen, Schnitt bevorzugt an Satzzeichen, mindestens 1 s Standzeit,
ausgeschriebene Zahlen (für die Stimme) werden in der Anzeige wieder Ziffern.
"""
import hashlib, json, re, textwrap
from pathlib import Path

BASIS = Path(__file__).resolve().parent.parent
SKRIPT = {s['id']: s for s in json.loads((BASIS / 'tts/skript.json').read_text())['szenen']}
Z = json.loads((BASIS / 'src/zeiten.json').read_text())
STIMME, MODELL, FPS, BREITE = 'NBqeXKdZHweef6y0B67V', 'eleven_v4', 30, 42
ZAHLEN = [('null punkt null punkt fünfzehn', '0.0.15'), ('eins Komma vier Prozent', '1,4 Prozent'),
          ('vierundzwanzig Gigabyte', '24 Gigabyte'), ('vierundsechzigtausend', '64.000'),
          ('fünfzehntausend', '15.000'), ('viertausend', '4.000'), ('zwanzig Dollar', '20 Dollar')]


def passt(text):
    return len(textwrap.wrap(text, BREITE, break_on_hyphens=False)) <= 2


def zeilen(text):
    for alt, neu in ZAHLEN:
        text = text.replace(alt, neu)
    return '\n'.join(textwrap.wrap(text, BREITE, break_on_hyphens=False))


def szene_cues(sid, start):
    text = SKRIPT[sid]['text']
    k = hashlib.sha256(f'{STIMME}|{MODELL}|{text}'.encode()).hexdigest()[:16]
    al = json.loads((BASIS / f'tts/eleven_cache/{k}.json').read_text())['alignment']
    assert ''.join(al['characters']) == text, sid
    st, en = al['character_start_times_seconds'], al['character_end_times_seconds']
    off = start + Z['szenen'][sid]['vorlauf']
    woerter = [(m.start(), m.end(), m.group(0)) for m in re.finditer(r'\S+', text)]
    cues, akt = [], []
    for i, w in enumerate(woerter):
        kandidat = ' '.join(x[2] for x in akt + [w])
        if akt and not passt(kandidat):
            cues.append(akt)
            akt = []
        akt.append(w)
        satzende = w[2][-1] in '.?!'
        komma = w[2][-1] in ',:' and len(' '.join(x[2] for x in akt)) >= 45
        if satzende or komma:
            cues.append(akt)
            akt = []
    if akt:
        cues.append(akt)
    return [(off + st[c[0][0]], off + en[c[-1][1] - 1], ' '.join(x[2] for x in c)) for c in cues]


def zeit(t, trenner):
    ms = int(round(t * 1000))
    return f'{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d}{trenner}{ms % 1000:03d}'


def main():
    alle, f = [], 0
    for sid in Z['reihenfolge']:
        alle += szene_cues(sid, f / FPS)
        f += round(Z['szenen'][sid]['dauer'] * FPS)
    fertig = []
    for i, (a, e, txt) in enumerate(alle):
        naechster = alle[i + 1][0] if i + 1 < len(alle) else e + 2
        ende = min(max(e + 0.35, a + 1.0), naechster - 0.05)
        fertig.append((a, ende, zeilen(txt)))
    ziel = BASIS / 'untertitel'
    ziel.mkdir(exist_ok=True)
    srt = '\n'.join(f'{i}\n{zeit(a, ",")} --> {zeit(e, ",")}\n{t}\n' for i, (a, e, t) in enumerate(fertig, 1))
    vtt = 'WEBVTT\n\n' + '\n'.join(f'{zeit(a, ".")} --> {zeit(e, ".")}\n{t}\n' for a, e, t in fertig)
    (ziel / 'opencode-browse.de.srt').write_text(srt)
    (ziel / 'opencode-browse.de.vtt').write_text(vtt)
    laengste = max(len(z) for _, _, t in fertig for z in t.split('\n'))
    print(f'{len(fertig)} Untertitel, längste Zeile {laengste} Zeichen, '
          f'max. {max(t.count(chr(10)) + 1 for _, _, t in fertig)} Zeilen, letzte Ende {fertig[-1][1]:.1f} s')


main()
