"""Entwurfsstimme (kostenlos, edge-tts) je Szene + Wortzeiten -> public/<id>.mp3, src/zeiten.json.

Aufruf: python3 -I tts/entwurf.py [--nur s03_kette ...]
Im Cloud-Container braucht edge-tts den Proxy (HTTPS_PROXY) und die Proxy-CA in certifi.
ElevenLabs wird hier NIE aufgerufen: die bezahlte Fassung kommt erst nach Freigabe des Textes.
"""
import asyncio, json, os, re, subprocess, sys
from pathlib import Path

import edge_tts

BASIS = Path(__file__).resolve().parent.parent
SKRIPT = json.loads((BASIS / 'tts/skript.json').read_text())
STIMME = SKRIPT['stimme_entwurf']
RATE = '+0%'
PAUSE_NACH = 0.7   # Sekunden Luft am Szenenende
VORLAUF = 0.25     # Sekunden Stille vor dem Sprechen


def norm(w):
    return re.sub(r'[^\w]', '', w.lower())


async def sprich(text, ziel):
    kom = edge_tts.Communicate(text, STIMME, rate=RATE, boundary='WordBoundary',
                               proxy=os.environ.get('HTTPS_PROXY'))
    woerter = []
    with open(ziel, 'wb') as f:
        async for ch in kom.stream():
            if ch['type'] == 'audio':
                f.write(ch['data'])
            elif ch['type'] == 'WordBoundary':
                woerter.append({'w': ch['text'], 't': ch['offset'] / 1e7, 'd': ch['duration'] / 1e7})
    return woerter


def dauer(datei):
    out = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(datei)],
                         capture_output=True, text=True, check=True).stdout
    return float(out)


def cues_finden(woerter, cues, sid):
    n = [norm(w['w']) for w in woerter]
    ab, res = 0, {}
    for name, phrase in cues.items():
        ziel = [norm(x) for x in phrase.split() if norm(x)]
        treffer = None
        for i in range(ab, len(n) - len(ziel) + 1):
            if n[i:i + len(ziel)] == ziel:
                treffer = i
                break
        if treffer is None:   # Zahlen o. Ä. anders zerlegt: nur erstes Wort suchen
            for i in range(ab, len(n)):
                if n[i].startswith(ziel[0][:4]):
                    treffer = i
                    break
        if treffer is None:
            sys.exit(f'Cue {sid}.{name} ({phrase!r}) nicht gefunden')
        res[name] = round(woerter[treffer]['t'] + VORLAUF, 3)
        ab = treffer + 1
    return res


async def main():
    nur = sys.argv[sys.argv.index('--nur') + 1:] if '--nur' in sys.argv else None
    zeiten_datei = BASIS / 'src/zeiten.json'
    zeiten = json.loads(zeiten_datei.read_text()) if zeiten_datei.exists() else {'szenen': {}}
    for sz in SKRIPT['szenen']:
        sid = sz['id']
        if nur and sid not in nur:
            continue
        mp3 = BASIS / 'public' / f'{sid}.mp3'
        woerter = await sprich(sz['text'], mp3)
        d = dauer(mp3)
        zeiten['szenen'][sid] = {'audio': d, 'dauer': round(VORLAUF + d + PAUSE_NACH, 3), 'vorlauf': VORLAUF,
                                 'cues': cues_finden(woerter, sz['cues'], sid)}
        (BASIS / 'tts' / f'{sid}.woerter.json').write_text(json.dumps(woerter, ensure_ascii=False))
        print(f'{sid}: {d:5.1f} s  {len(sz["text"])} Zeichen  cues={zeiten["szenen"][sid]["cues"]}')
    reihen = [s['id'] for s in SKRIPT['szenen']]
    zeiten['reihenfolge'] = reihen
    zeiten['laenge'] = round(sum(zeiten['szenen'][s]['dauer'] for s in reihen if s in zeiten['szenen']), 3)
    zeiten['stimme'] = STIMME
    zeiten_datei.write_text(json.dumps(zeiten, ensure_ascii=False, indent=1))
    zeichen = sum(len(s['text']) for s in SKRIPT['szenen'])
    print(f'Gesamt {zeiten["laenge"]:.1f} s, {zeichen} Zeichen Sprechtext')


asyncio.run(main())
