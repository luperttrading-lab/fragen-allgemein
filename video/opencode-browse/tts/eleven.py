"""ElevenLabs-Fassung (Christian, eleven_v4) je Szene mit Zeitmarken -> public/<id>.mp3, src/zeiten.json.

Sicherheitsregeln (Kosten!):
- Ohne --ja wird NICHTS gesendet: das Skript zeigt nur, welche Szenen neu vertont würden und wie viele Zeichen das kostet.
- Jede Szene wird nach Stimme|Modell|Text im Cache tts/eleven_cache/ abgelegt; gleicher Text kostet nie zweimal.
- --nur s01_wand ... begrenzt auf einzelne Szenen (z. B. Probe).

Aufruf:  python3 -I tts/eleven.py [--nur ID ...]          # Vorschau, kostenlos
         python3 -I tts/eleven.py --ja [--nur ID ...]     # vertont fehlende Szenen
Tempo: Rubber Band (ffmpeg rubberband, Formanten erhalten) auf TEMPO, Zeitmarken werden mitskaliert.
"""
import base64, hashlib, json, os, re, subprocess, sys, urllib.request
from pathlib import Path

BASIS = Path(__file__).resolve().parent.parent
SKRIPT = json.loads((BASIS / 'tts/skript.json').read_text())
STIMME = 'NBqeXKdZHweef6y0B67V'      # Christian - Warm and Captivating
MODELL = 'eleven_v4'                # 1 Zeichen = 1 Credit (Modellliste, 08.11.2026)
TEMPO = 1.0                         # Seneca wirkte bei 0,93 besser; dieser Text ist roh schon ruhig (2,2 W/s), daher 1,0
VORLAUF, PAUSE_NACH = 0.25, 0.7
CACHE = BASIS / 'tts/eleven_cache'


def norm(w):
    return re.sub(r'[^\w]', '', w.lower())


def sig(text):
    return hashlib.sha256(f'{STIMME}|{MODELL}|{text}'.encode()).hexdigest()[:16]


def hole(text, ziel_mp3, ziel_json):
    req = urllib.request.Request(
        f'https://api.elevenlabs.io/v1/text-to-speech/{STIMME}/with-timestamps?output_format=mp3_44100_128',
        data=json.dumps({'text': text, 'model_id': MODELL}).encode(),
        headers={'xi-api-key': os.environ['ELEVENLABS_API_KEY'], 'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=300) as r:
        d = json.load(r)
    ziel_mp3.write_bytes(base64.b64decode(d['audio_base64']))
    ziel_json.write_text(json.dumps({'text': text, 'alignment': d['alignment']}, ensure_ascii=False))


def woerter(text, al):
    zeichen, starts = al['characters'], al['character_start_times_seconds']
    voll = ''.join(zeichen)
    res, pos = [], 0
    for m in re.finditer(r'\S+', text):
        i = voll.find(m.group(0)[0], pos) if voll != text else m.start()
        if i < 0:
            continue
        res.append({'w': m.group(0), 't': starts[i] / TEMPO})
        pos = i + 1
    return res


def cues_finden(ws, cues, sid):
    n = [norm(w['w']) for w in ws]
    ab, res = 0, {}
    for name, phrase in cues.items():
        ziel = [norm(x) for x in phrase.split() if norm(x)]
        treffer = next((i for i in range(ab, len(n) - len(ziel) + 1) if n[i:i + len(ziel)] == ziel), None)
        if treffer is None:
            sys.exit(f'Cue {sid}.{name} ({phrase!r}) nicht gefunden')
        res[name] = round(ws[treffer]['t'] + VORLAUF, 3)
        ab = treffer + 1
    return res


def dauer(datei):
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(datei)],
                                capture_output=True, text=True, check=True).stdout)


def main():
    ja = '--ja' in sys.argv
    nur = [a for a in sys.argv[sys.argv.index('--nur') + 1:] if not a.startswith('--')] if '--nur' in sys.argv else None
    CACHE.mkdir(exist_ok=True)
    szenen = [s for s in SKRIPT['szenen'] if not nur or s['id'] in nur]
    fehlend = [s for s in szenen if not (CACHE / f"{sig(s['text'])}.json").exists()]
    kosten = sum(len(s['text']) for s in fehlend)
    print(f'{len(szenen)} Szenen gewählt, {len(fehlend)} nicht im Cache -> {kosten} Zeichen ({MODELL}, 1 Credit/Zeichen)')
    for s in fehlend:
        print(f"  neu: {s['id']} ({len(s['text'])} Zeichen)")
    if fehlend and not ja:
        print('Vorschau, nichts gesendet. Mit --ja vertonen.')
        return
    zd = BASIS / 'src/zeiten.json'
    zeiten = json.loads(zd.read_text()) if zd.exists() else {'szenen': {}}
    for s in szenen:
        k = sig(s['text'])
        roh, al = CACHE / f'{k}.mp3', CACHE / f'{k}.json'
        if not al.exists():
            print(f"  ElevenLabs: {s['id']} …", flush=True)
            hole(s['text'], roh, al)
        ziel = BASIS / 'public' / f"{s['id']}.mp3"
        filt = ['-af', f'rubberband=tempo={TEMPO}:formant=preserved'] if TEMPO != 1.0 else []
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(roh), *filt, '-b:a', '160k', str(ziel)], check=True)
        d = dauer(ziel)
        ws = woerter(s['text'], json.loads(al.read_text())['alignment'])
        zeiten['szenen'][s['id']] = {'audio': d, 'dauer': round(VORLAUF + d + PAUSE_NACH, 3), 'vorlauf': VORLAUF,
                                     'cues': cues_finden(ws, s['cues'], s['id'])}
        print(f"  {s['id']}: {d:5.1f} s")
    reihen = [s['id'] for s in SKRIPT['szenen']]
    zeiten['reihenfolge'] = reihen
    zeiten['laenge'] = round(sum(zeiten['szenen'][i]['dauer'] for i in reihen if i in zeiten['szenen']), 3)
    zeiten['stimme'] = f'ElevenLabs Christian ({MODELL}), Tempo {TEMPO}'
    zd.write_text(json.dumps(zeiten, ensure_ascii=False, indent=1))
    print(f"Gesamt {zeiten['laenge']:.1f} s")


main()
