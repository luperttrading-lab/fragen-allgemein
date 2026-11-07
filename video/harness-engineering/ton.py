"""Ton für Variante A oder B: je Szene ElevenLabs Text-to-Dialogue mit Zeitmarken (Cache in tts_cache/),
Funkfilter + Funkklick auf Harness-Zeilen, Szenen mit Pausen zusammensetzen, auf -16 LUFS bringen.

Aufruf: python3 ton.py A|B <ausgabeordner>
Ergebnis: <ausgabeordner>/ton_<V>.wav und zeitplan_<V>.json (Szenenzeiten, Cue-Zeiten, Sprecherabschnitte).
Ohne ELEVENLABS_API_KEY wird nur aus dem Cache gearbeitet (fehlt etwas, bricht es ab).
"""
import base64, hashlib, json, os, subprocess, sys, urllib.request
import numpy as np
from skript import STIMMEN, VARIANTEN, zerlege

HIER = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HIER, 'tts_cache')
SR = 44100
VORLAUF, PAUSE, NACHLAUF = 0.6, 0.8, 3.0
EXTRA = {}  # Szenen mit längerer Pause danach, z. B. {'s2': 1.6}
FUNK = ('highpass=f=400,highpass=f=400,lowpass=f=2800,lowpass=f=2800,lowpass=f=2800,'
        'acompressor=threshold=-24dB:ratio=6:attack=3:release=50,acrusher=bits=12:mix=0.25,volume=6dB')


def zusammenfassen(zeilen):
    """Aufeinanderfolgende Zeilen desselben Sprechers zu einer Eingabe verbinden (bessere Satzmelodie)."""
    aus = []
    for s, t in zeilen:
        if aus and aus[-1][0] == s:
            aus[-1] = (s, aus[-1][1] + ' ' + t)
        else:
            aus.append((s, t))
    return aus


def anfrage(zeilen):
    body = {'model_id': 'eleven_v4', 'inputs': [{'text': t, 'voice_id': STIMMEN[s]} for s, t in zeilen]}
    h = hashlib.sha1(json.dumps(body, sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:16]
    pfad = os.path.join(CACHE, h + '.json')
    if os.path.exists(pfad):
        return json.load(open(pfad)), True
    if 'ELEVENLABS_API_KEY' not in os.environ:
        sys.exit('Nicht im Cache und kein ELEVENLABS_API_KEY: ' + pfad)
    req = urllib.request.Request('https://api.elevenlabs.io/v1/text-to-dialogue/with-timestamps?output_format=mp3_44100_128',
                                 data=json.dumps(body).encode(), method='POST',
                                 headers={'xi-api-key': os.environ['ELEVENLABS_API_KEY'], 'Content-Type': 'application/json'})
    d = json.load(urllib.request.urlopen(req, timeout=600))
    d['anfrage'] = body
    os.makedirs(CACHE, exist_ok=True)
    json.dump(d, open(pfad, 'w'), ensure_ascii=False)
    return d, False


def dekodieren(mp3_bytes, filter_harness=()):
    """MP3 -> float32 mono 44,1 kHz; Funkfilter nur in den angegebenen Abschnitten, dort auch ein kurzer Klick."""
    if filter_harness:
        bed = '+'.join(f'between(t,{a:.3f},{b:.3f})' for a, b in filter_harness)
        fc = (f"[0:a]aformat=sample_rates={SR}:channel_layouts=mono,asplit=2[o][f];[f]{FUNK}[ff];"
              f"[o]volume='if({bed},0,1)':eval=frame[o2];[ff]volume='if({bed},1,0)':eval=frame[f2];"
              f"[o2][f2]amix=inputs=2:normalize=0[out]")
        cmd = ['ffmpeg', '-v', 'error', '-i', '-', '-filter_complex', fc, '-map', '[out]', '-f', 'f32le', '-']
    else:
        cmd = ['ffmpeg', '-v', 'error', '-i', '-', '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-']
    x = np.frombuffer(subprocess.run(cmd, input=mp3_bytes, capture_output=True, check=True).stdout, np.float32).copy()
    rng = np.random.default_rng(7)
    for a, _ in filter_harness:  # Funkklick: 70 ms gefiltertes Rauschen, leise, kurz vor dem ersten Wort
        n = int(0.07 * SR); i0 = max(0, int((a - 0.09) * SR))
        k = rng.standard_normal(n).astype(np.float32) * np.linspace(1, 0, n, dtype=np.float32) ** 2 * 0.05
        k = np.convolve(k, np.ones(6, np.float32) / 6, mode='same') - np.convolve(k, np.ones(40, np.float32) / 40, mode='same')
        x[i0:i0 + n] += k[:max(0, min(n, len(x) - i0))]
    return x


def lufs(wav):
    r = subprocess.run(['ffmpeg', '-hide_banner', '-i', wav, '-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True)
    zeilen = [z for z in r.stderr.splitlines() if z.strip().startswith('I:')]
    return float(zeilen[-1].split()[1])


def main(v, aus):
    os.makedirs(aus, exist_ok=True)
    teile, plan, t, neu = [np.zeros(int(VORLAUF * SR), np.float32)], {'variante': v, 'szenen': []}, VORLAUF, 0
    for sid, zeilen in VARIANTEN[v]:
        sauber, cues = zerlege(zeilen)
        eingaben = zusammenfassen(sauber)
        d, aus_cache = anfrage(eingaben)
        neu += 0 if aus_cache else sum(len(x) for _, x in eingaben)
        al = d['alignment']; zeichen = al['characters']; st = al['character_start_times_seconds']
        text = ''.join(x for _, x in eingaben).replace('  ', ' ')
        if len(zeichen) != len(''.join(x for _, x in eingaben)):
            print(f'Warnung {sid}: Zeitmarken {len(zeichen)} Zeichen, Text {len(text)} Zeichen')
        # Marker-Positionen beziehen sich auf den Text vor dem Zusammenfassen; durch die eingefügten Leerzeichen
        # verschieben sie sich je Zusammenfassung um 1. Neu berechnen über den zusammengefassten Text:
        zusammen, cues2, pos, alt = [], {}, 0, 0
        cue_namen = sorted(cues.items(), key=lambda kv: kv[1])
        roh = ''.join(x for _, x in sauber)
        verbunden = ''.join(x for _, x in eingaben)
        # Zuordnung roh -> verbunden: verbunden enthält roh plus zusätzliche Leerzeichen an Zeilenverbindungen
        abb, j = [], 0
        for i, c in enumerate(roh):
            while j < len(verbunden) and verbunden[j] != c:
                j += 1
            abb.append(j); j += 1
        for name, p in cue_namen:
            q = abb[p] if p < len(abb) else len(verbunden) - 1
            while q < len(zeichen) - 1 and zeichen[q].isspace():
                q += 1
            cues2[name] = round(t + st[min(q, len(st) - 1)], 3)
        segmente = []
        for s in d.get('voice_segments') or []:
            sprecher = eingaben[s['dialogue_input_index']][0]
            segmente.append({'sprecher': sprecher, 'start': round(t + s['start_time_seconds'], 3), 'ende': round(t + s['end_time_seconds'], 3)})
        harness = [(s['start_time_seconds'], s['end_time_seconds']) for s in d.get('voice_segments') or []
                   if eingaben[s['dialogue_input_index']][0] == 'HARNESS']
        x = dekodieren(base64.b64decode(d['audio_base64']), harness)
        dauer = len(x) / SR
        plan['szenen'].append({'id': sid, 'start': round(t, 3), 'ende': round(t + dauer, 3), 'cues': cues2, 'segmente': segmente})
        pz = PAUSE + EXTRA.get(sid, 0)
        teile += [x, np.zeros(int(pz * SR), np.float32)]
        t += dauer + pz
    teile[-1] = np.zeros(int(NACHLAUF * SR), np.float32)
    y = np.concatenate(teile)
    plan['dauer'] = round(len(y) / SR, 3)
    roh_wav = os.path.join(aus, f'ton_{v}_roh.wav'); ziel = os.path.join(aus, f'ton_{v}.wav')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ar', str(SR), '-ac', '1', '-i', '-', roh_wav], input=y.tobytes(), check=True)
    g = -16.0 - lufs(roh_wav)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', roh_wav, '-af', f'volume={g:.2f}dB,alimiter=limit=0.84:level=false',
                    '-ar', str(SR), ziel], check=True)
    json.dump(plan, open(os.path.join(aus, f'zeitplan_{v}.json'), 'w'), ensure_ascii=False, indent=1)
    print(f'{v}: {plan["dauer"]:.1f} s, neu an ElevenLabs gesendet: {neu} Zeichen, Lautheit {lufs(ziel):.1f} LUFS')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
