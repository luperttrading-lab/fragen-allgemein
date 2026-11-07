"""Formatprobe V3: Peter erzählt, Modell = Mila (w), Harness = Helmut (m) mit Funkfilter wie ein Tower.
Ganzer Dialog in einem Aufruf (natürliche Übergänge), Zeitmarken je Zeile, dann Funkfilter nur auf die Harness-Zeilen.
Aufruf: python3 hoerprobe_v3.py <zielordner>"""
import base64, json, os, subprocess, sys, urllib.request
STIMMEN = {'PETER': 'AMJfLTmTy3vPtjSvrGqZ', 'MODELL': 'dCnu06FiOZma2KVNUoPZ', 'HARNESS': 'Cqbq4nsuUe1we6J45miU'}
V3 = [('PETER', 'Wie drückt ein Modell, das nur Text schreiben kann, einen Knopf? Gar nicht. Es schreibt einen Wunsch auf. Geben wir dem Modell mal eine Stimme.'),
      ('MODELL', 'Ich möchte die Datei mit den Notizen lesen.'),
      ('PETER', 'Und der Harness antwortet wie der Tower im Funk.'),
      ('HARNESS', 'Harness an Modell: erlaubt. Hier ist die Datei.'),
      ('PETER', 'Für das Modell wirkt das wie Zauberei: Kurz darauf liegt das Ergebnis auf dem Schreibtisch. Spannend wird es, wenn das Modell etwas Gefährliches will.'),
      ('MODELL', 'Ich lösche jetzt die alte Datenbank. Die stört nur.'),
      ('HARNESS', 'Harness an Modell: abgelehnt. Das muss erst der Mensch freigeben.'),
      ('PETER', 'Das Modell darf alles vorschlagen. Ausführen tut nur der Harness.')]
FUNK = 'highpass=f=400,highpass=f=400,lowpass=f=2800,lowpass=f=2800,lowpass=f=2800,acompressor=threshold=-24dB:ratio=6:attack=3:release=50,acrusher=bits=12:mix=0.25,volume=6dB'
if __name__ == '__main__':
    ziel = sys.argv[1]; print('Zeichen', sum(len(t) for _, t in V3))
    body = {'model_id': 'eleven_v4', 'inputs': [{'text': t, 'voice_id': STIMMEN[s]} for s, t in V3]}
    req = urllib.request.Request('https://api.elevenlabs.io/v1/text-to-dialogue/with-timestamps?output_format=mp3_44100_128',
        data=json.dumps(body).encode(), method='POST',
        headers={'xi-api-key': os.environ['ELEVENLABS_API_KEY'], 'Content-Type': 'application/json'})
    d = json.load(urllib.request.urlopen(req, timeout=300))
    roh = os.path.join(ziel, 'v3_roh.mp3'); open(roh, 'wb').write(base64.b64decode(d['audio_base64']))
    json.dump({k: v for k, v in d.items() if k != 'audio_base64'}, open(os.path.join(ziel, 'v3_zeiten.json'), 'w'))
    seg = d.get('voice_segments') or []
    harness = [(s['start_time_seconds'], s['end_time_seconds']) for s in seg if V3[s['dialogue_input_index']][0] == 'HARNESS']
    print('Harness-Abschnitte', harness)
    # Funkfilter nur in den Harness-Abschnitten (Grenzen liegen in Pausen), sonst Original
    bed = '+'.join(f'between(t,{a:.3f},{b:.3f})' for a, b in harness) or '0'
    fc = (f"[0:a]asplit=2[o][f];[f]{FUNK}[ff];"
          f"[o]volume='if({bed},0,1)':eval=frame[o2];[ff]volume='if({bed},1,0)':eval=frame[f2];"
          f"[o2][f2]amix=inputs=2:normalize=0,loudnorm=I=-16:TP=-1.5:LRA=11[out]")
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', roh, '-filter_complex', fc, '-map', '[out]',
                    '-ar', '44100', '-c:a', 'libmp3lame', '-b:a', '128k', os.path.join(ziel, 'format_v3.mp3')], check=True)
    print('ok')
