"""Prosodie-Merkmale je Ausschnitt und Abstand zu echten Vorlesern (z-Werte gegen die Referenzgruppe)."""
import sys, glob, json, wave, numpy as np, parselmouth
from parselmouth.praat import call
FL = 0.01

def lade(f):
    w = wave.open(f); return np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float64) / 32768

def merkmale(f):
    x = lade(f); sr = 16000; n = int(sr * FL)
    fr = x[: len(x) // n * n].reshape(-1, n); db = 10 * np.log10((fr ** 2).mean(1) + 1e-12)
    laut = db > max(np.percentile(db, 95) - 35, np.percentile(db, 10) + 6)   # Schwelle über dem Grundrauschen
    # Inseln (Schall) und Pausen ≥ 0,15 s
    idx = np.flatnonzero(laut); a, b = idx[0], idx[-1]; lb = laut[a:b + 1].copy()
    runs = []; cur = lb[0]; start = 0
    for i in range(1, len(lb) + 1):
        if i == len(lb) or lb[i] != cur:
            runs.append([cur, start, i]); start = i
            if i < len(lb): cur = lb[i]
    for r in runs:                                   # kurze Stillen < 0,15 s zählen als Schall
        if not r[0] and (r[2] - r[1]) * FL < 0.15: r[0] = True
    merged = []
    for r in runs:
        if merged and merged[-1][0] == r[0]: merged[-1][2] = r[2]
        else: merged.append(list(r))
    inseln = [((s + a) * FL, (e + a) * FL) for v, s, e in merged if v]
    pausen = [(e - s) * FL for v, s, e in merged if not v]
    words = json.load(open(f[:-4] + ".words.json"))
    mids = np.array([(w["s"] + w["e"]) / 2 for w in words])
    snd = parselmouth.Sound(x, sr)
    pitch = snd.to_pitch(time_step=FL, pitch_floor=60, pitch_ceiling=450)
    f0 = pitch.selected_array["frequency"]; t0 = pitch.xs()
    ref = np.median(f0[f0 > 0])
    ipu_rate, ipu_med, slopes, ipu_w, atem = [], [], [], [], 0
    for s, e in inseln:
        k = int(((mids >= s) & (mids < e)).sum())
        if k == 0:
            if 0.1 <= e - s <= 1.2: atem += 1            # Schallinsel ohne Wort: Atem/Geräusch
            continue
        ipu_w.append(k)
        if k >= 3: ipu_rate.append(k / (e - s))
        m = (t0 >= s) & (t0 < e) & (f0 > 0)
        if m.sum() > 20:
            st = 12 * np.log2(f0[m] / ref); tt = t0[m]
            ipu_med.append(np.median(st)); slopes.append(np.polyfit(tt - tt[0], st, 1)[0])
    sprech = sum(e - s for s, e in inseln); dauer = inseln[-1][1] - inseln[0][0]
    st_all = 12 * np.log2(f0[f0 > 0] / ref)
    pp = call(snd, "To PointProcess (periodic, cc)", 60, 450)
    jitter = call(pp, "Get jitter (local)", 0, 0, 0.0001, 0.02, 1.3) * 100
    shimmer = call([snd, pp], "Get shimmer (local)", 0, 0, 0.0001, 0.02, 1.3, 1.6) * 100
    hnr = call(call(snd, "To Harmonicity (cc)", 0.01, 60, 0.1, 1.0), "Get mean", 0, 0)
    return {
        "Tempo W/s": len(words) / sprech,
        "Tempo-Schwankung": np.std(ipu_rate) / np.mean(ipu_rate),
        "Pausenanteil %": sum(pausen) / dauer * 100,
        "Pausen-Schwankung": np.std(pausen) / np.mean(pausen),
        "Wörter/Phrase": np.mean(ipu_w),
        "Melodie-Spannweite HT": np.percentile(st_all, 95) - np.percentile(st_all, 5),
        "Phrasen-Tonhöhe HT": np.std(ipu_med),
        "Abfall HT/s": np.mean(slopes),
        "Jitter %": jitter, "Shimmer %": shimmer, "HNR dB": hnr,
        "Atem/min": atem / dauer * 60,
    }

W = sys.argv[1]
M = {f.rsplit("/", 1)[-1][:-4]: merkmale(f) for f in sorted(glob.glob(W + "/*.wav")) if glob.glob(f[:-4] + ".words.json")}
json.dump(M, open(W + "/../merkmale.json", "w"), ensure_ascii=False, indent=1)
keys = list(next(iter(M.values())).keys()); refs = [k for k in M if k.startswith("ref_")]
def abstand(name, pool):
    R = np.array([[M[r][k] for k in keys] for r in pool]); mu, sd = R.mean(0), R.std(0, ddof=1)
    z = (np.array([M[name][k] for k in keys]) - mu) / sd
    return np.sqrt(np.mean(z ** 2)), z
print(f"{'':30}" + "".join(f"{k[:11]:>12}" for k in keys) + f"{'Abstand':>9}")
rows = []
for name in M:
    pool = [r for r in refs if r != name]                 # Referenzen: leave-one-out
    d, z = abstand(name, pool); rows.append((d, name, z))
    print(f"{name[:30]:30}" + "".join(f"{M[name][k]:12.2f}" for k in keys) + f"{d:9.2f}")
print("\nRangfolge nach Abstand zur Gruppe echter Vorleser (RMS der z-Werte; Referenzen leave-one-out):")
for d, name, z in sorted(rows):
    top = sorted(zip(keys, z), key=lambda t: -abs(t[1]))[:3]
    print(f"  {d:5.2f}  {name:34} stärkste Abweichungen: " + ", ".join(f"{k} {v:+.1f}" for k, v in top))
