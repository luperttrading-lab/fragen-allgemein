# Eigene Nachrechnung (ohne regel.py auszuführen): Szenendauern, Kapitel, Stichwortzeiten für „Der Trick“, Kapitel-Ton.
# Regeln aus regel.py gelesen: Tempo 1,05; Stille-Schwelle −45 dB; 0,04 s Vorlauf, 0,08 s Nachlauf; Pause 0,7 s
# (Merke 6,0 s); keine Atempausen; C(sc, wort) = Zeichen-Startzeit / Tempo − Vorlauf.
import base64, hashlib, json, os, subprocess, sys
import numpy as np
REPO, AUS = sys.argv[1], sys.argv[2]
SR, TEMPO, PAUSE = 44100, 1.05, 0.7
szenen = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'szenen.json')))
cache = os.path.join(REPO, 'themen/mathe-einmaleins/tts_cache')
os.makedirs(AUS, exist_ok=True)
t, kap = 0.0, []
for sc in szenen:
    sig = f"el|NBqeXKdZHweef6y0B67V|eleven_v4|null|{sc['text']}"
    d = json.load(open(os.path.join(cache, hashlib.sha1(sig.encode()).hexdigest()[:16] + '.json')))
    mp3 = os.path.join(AUS, sc['id'] + '.mp3')
    open(mp3, 'wb').write(base64.b64decode(d['audio_base64']))
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', mp3, '-af', f'atempo={TEMPO}', '-f', 's16le', '-ac', '1',
                          '-ar', str(SR), '-'], capture_output=True, check=True).stdout
    x = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
    idx = np.where(np.abs(x) > 10 ** (-45 / 20) * np.abs(x).max())[0]
    a, b = max(idx[0] - int(0.04 * SR), 0), idx[-1] + int(0.08 * SR)
    sc['_x'], sc['_lead'] = x[a:b], a / SR
    sc['_starts'] = d['alignment']['character_start_times_seconds']
    sc['_skala'] = len(sc['_starts']) / max(len(sc['text']), 1)
    sc['start'], sc['dauer'] = t, len(sc['_x']) / SR
    pause = sc.get('pause', PAUSE)
    if sc.get('anhang') and kap:
        kap[-1]['dauer'] += sc['dauer'] + pause
    else:
        kap.append(dict(start=t, dauer=sc['dauer'] + pause))
    t += sc['dauer'] + pause

def C(sc, wort, nach=None):
    s = sc['text'].find(nach) + len(nach) if nach else 0
    i = sc['text'].find(wort, s)
    assert i >= 0, wort
    j = min(int(round(i * sc['_skala'])), len(sc['_starts']) - 1)
    return max(0.0, sc['_starts'][j] / TEMPO - sc['_lead'])

sc = next(s for s in szenen if s['id'] == 'regel')
T = {k: C(sc, w) for k, w in dict(s1='Schritt eins', acht='die Acht', flug='zur ersten Zahl', z24='gibt vierundzwanzig',
     s2='Schritt zwei', null='eine Null', z240='wird zweihundert', s3='Schritt drei', f68='sechs mal acht',
     z48='gleich acht', summe='Zweihundertvierzig plus', z288='macht zwei').items()}
zeiten = dict(T=T, t_zweite=C(sc, 'Einer der zweiten Zahl'), t_mult=C(sc, 'Multipliziere'),
              szene=dict(start=sc['start'], dauer=sc['dauer'], kicker=sc['kicker'], nr=1), kapitel=kap,
              laenge=sc['dauer'] + 0.3)
json.dump(zeiten, open(os.path.join(AUS, 'zeiten.json'), 'w'), indent=1)
y = np.concatenate([sc['_x'], np.zeros(int(0.3 * SR), np.float32)])
wav = os.path.join(AUS, 'roh.wav')
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ar', str(SR), '-ac', '1', '-i', '-', wav],
               input=y.tobytes(), check=True)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', wav, '-af', 'highpass=f=60,loudnorm=I=-16:TP=-1.5:LRA=11,lowpass=f=12000',
                '-ar', str(SR), os.path.join(AUS, 'kapitel.wav')], check=True)
for s in szenen:
    os.remove(os.path.join(AUS, s['id'] + '.mp3'))
os.remove(wav)
print(json.dumps({k: (round(v, 2) if isinstance(v, float) else v) for k, v in zeiten.items() if k != 'kapitel'}, indent=0)[:900])
print('Kapitel-Start im Gesamtvideo:', round(sc['start'], 2), 's; Gesamtlänge', round(t, 1), 's')
