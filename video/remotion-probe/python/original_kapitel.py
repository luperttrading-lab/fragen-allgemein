# Rendert nur das Kapitel „Der Trick“ mit dem unveränderten Original-Renderer (regel.py), samt Original-Tonkette.
import json, os, subprocess, sys, time, wave
from multiprocessing import Pool
import numpy as np
REPO, AUS = sys.argv[1], sys.argv[2]
sys.path.insert(0, os.path.join(REPO, 'werkzeug'))
sys.path.insert(0, os.path.join(REPO, 'themen/mathe-einmaleins'))
import regel as G
R = G.R
os.makedirs(AUS, exist_ok=True)
t_start = time.time()
ton, gesamt = G.ton_und_zeitplan()
wav = os.path.join(AUS, 'gesamt.wav')
with wave.open(wav, 'wb') as f:
    f.setnchannels(1); f.setsampwidth(2); f.setframerate(R.SR)
    f.writeframes((np.clip(ton, -1, 1) * 32767).astype(np.int16).tobytes())
R.aufbereiten(wav)
with wave.open(wav) as f:
    stimme = np.frombuffer(f.readframes(f.getnframes()), np.int16).astype(np.float32) / 32768
stimme = G.tiefpass(G.entknacksen(stimme, R.SR, []), R.SR)
mix_ = np.clip(stimme + G.klangspur(len(stimme)), -0.97, 0.97)
with wave.open(wav, 'wb') as f:
    f.setnchannels(1); f.setsampwidth(2); f.setframerate(R.SR)
    f.writeframes((mix_ * 32767).astype(np.int16).tobytes())
t_ton = time.time()
i = [s['id'] for s in G.SZENEN].index('regel')
sc = G.SZENEN[i]
a, e = sc['start'], sc['start'] + sc['dauer'] + 0.3
k0, k1 = round(a * G.FPS), round(e * G.FPS)
grenzen = [k0 + (k1 - k0) * j // 4 for j in range(5)]
auftraege = [(grenzen[j], grenzen[j + 1], os.path.join(AUS, f'teil{j}.mp4')) for j in range(4)]
with Pool(4) as pool:
    pfade = pool.map(G.rendere_teil, auftraege)
t_bild = time.time()
liste = os.path.join(AUS, 'teile.txt')
open(liste, 'w').writelines(f"file '{q}'\n" for q in pfade)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{k0 / G.FPS:.4f}', '-t', f'{(k1 - k0) / G.FPS:.4f}', '-i', wav,
                os.path.join(AUS, 'kapitel.wav')], check=True)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', liste, '-i', os.path.join(AUS, 'kapitel.wav'),
                '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart',
                os.path.join(AUS, 'original_trick.mp4')], check=True)
for q in pfade + [liste]:
    os.remove(q)
json.dump(dict(start=a, dauer=sc['dauer'], k0=k0, k1=k1, ton_s=t_ton - t_start, bild_s=t_bild - t_ton),
          open(os.path.join(AUS, 'lauf.json'), 'w'), indent=1)
print(f'Ton vorbereiten {t_ton - t_start:.1f} s, Bilder rendern {t_bild - t_ton:.1f} s, Frames {k1 - k0}, '
      f'Kapitel {a:.2f}–{e:.2f} s')
