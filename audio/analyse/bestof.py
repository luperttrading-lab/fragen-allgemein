#!/usr/bin/env python3
"""Best-of-N für eine Hörbuchseite: jeden Take auf Worttreue prüfen (Whisper turbo, Gegenprobe medium), Prosodie gegen
echte Vorleser bewerten, je Segment den besten wortgetreuen Take wählen, Ränder schneiden, Lautheit angleichen, mit
Pausen zusammensetzen, Ergebnis erneut prüfen.
Aufruf: python3 bestof.py <takes-ordner> <arbeitsordner> <ausgabe.mp3>
"""
import sys, json, re, glob, subprocess, difflib, numpy as np, parselmouth
from pathlib import Path
TAKES, WORK, OUT = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]); WORK.mkdir(parents=True, exist_ok=True)
CFG = json.load(open(TAKES / "segmente.json", encoding="utf-8")); SEG = {s["id"]: s for s in CFG["segmente"]}
REF = json.load(open(Path(__file__).with_name("merkmale_seneca_kap1.json"), encoding="utf-8"))
SR = 24000; FL = 0.01
PAUSE = {"kopf": 1.4, "satz": 0.75, "absatz": 1.4}      # Sekunden zwischen Segmenten

def pcm(f, sr):
    b = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", str(f), "-ac", "1", "-ar", str(sr), "-f", "s16le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(b, np.int16).astype(np.float32) / 32768

def norm(t):     # Vergleich ohne Leerzeichen: umso/um so, wieviel/wie viel, hineilt/hin eilt gleich; das/dass/daß gleich
    t = t.lower().replace("ß", "ss")
    t = re.sub(r"\bdass\b", "das", t)
    return re.sub(r"[^a-zäöü0-9]", "", t)

_models = {}
def stt(f, name):
    cache = WORK / f"{Path(f).stem}.{name}.json"
    if cache.exists(): return json.load(open(cache, encoding="utf-8"))
    from faster_whisper import WhisperModel
    if name not in _models: _models[name] = WhisperModel(name, device="cpu", compute_type="int8", cpu_threads=4)
    segs, _ = _models[name].transcribe(pcm(f, 16000), language="de", beam_size=5, word_timestamps=True, condition_on_previous_text=False, vad_filter=True)
    w = [{"w": x.word.strip(), "s": round(x.start, 2), "e": round(x.end, 2)} for s in segs for x in s.words]
    json.dump(w, open(cache, "w", encoding="utf-8"), ensure_ascii=False); return w

def abweichung(soll, words):
    a, b = norm(soll), norm(" ".join(x["w"] for x in words))
    if a == b: return []
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    return [f"{a[max(0,i1-12):i1]}[{a[i1:i2]}→{b[j1:j2]}]" for op, i1, i2, j1, j2 in sm.get_opcodes() if op != "equal"]

def bereich(k):  # Spannweite echter Vorleser ohne Extremwert oben/unten
    v = sorted(REF[r][k] for r in REF if r.startswith("ref_")); return v[1], v[-2]

def merkmale(x, words):
    n = int(SR * FL); fr = x[: len(x) // n * n].reshape(-1, n); db = 10 * np.log10((fr.astype(np.float64) ** 2).mean(1) + 1e-12)
    laut = db > max(np.percentile(db, 95) - 35, np.percentile(db, 10) + 6)
    i0, i1 = np.flatnonzero(laut)[[0, -1]]; lb = laut[i0:i1 + 1]
    # Pausen ≥ 0,15 s innerhalb des Satzes
    pausen, cur = [], 0
    for v in lb:
        if not v: cur += 1
        else:
            if cur * FL >= 0.15: pausen.append(cur * FL)
            cur = 0
    dauer = (i1 - i0 + 1) * FL; sprech = dauer - sum(pausen)
    snd = parselmouth.Sound(x.astype(np.float64), SR); p = snd.to_pitch(time_step=FL, pitch_floor=60, pitch_ceiling=300)
    f0 = p.selected_array["frequency"]; t = p.xs(); v = f0 > 0
    st = 12 * np.log2(f0[v] / np.median(f0[v]))
    # Abfall: Steigung in den letzten 0,6 s vor jeder Pause bzw. vor Satzende (Halbtöne/s)
    enden, pos, cur = [], i0, 0
    for k, vv in enumerate(lb):
        if not vv: cur += 1
        else:
            if cur * FL >= 0.15: enden.append((i0 + k - cur) * FL)
            cur = 0
    enden.append((i1 + 1) * FL); sl = []
    for e in enden:
        m = (t > e - 0.6) & (t <= e) & v
        if m.sum() > 15: sl.append(np.polyfit(t[m], 12 * np.log2(f0[m] / np.median(f0[v])), 1)[0])
    return {"Tempo W/s": len(words) / sprech, "Pausenanteil %": sum(pausen) / dauer * 100,
            "Wörter/Phrase": len(words) / (len(pausen) + 1), "Melodie-Spannweite HT": float(np.percentile(st, 95) - np.percentile(st, 5)),
            "Endabfall HT/s": float(np.mean(sl)) if sl else 0.0, "F0 Hz": float(np.median(f0[v])), "Pegel dB": float(np.percentile(db[laut], 50))}

PRUEF = ["Tempo W/s", "Pausenanteil %", "Wörter/Phrase", "Melodie-Spannweite HT"]
def ki_wert(m):   # 0 = alle Merkmale im Bereich echter Vorleser; sonst Summe der Überschreitung in Bereichsbreiten
    s = 0.0
    for k in PRUEF:
        lo, hi = bereich(k); w = hi - lo
        s += max(0, lo - m[k]) / w + max(0, m[k] - hi) / w
    return s

# 1) Prüfen und bewerten
takes = {}
for f in sorted(TAKES.glob("s*_*.flac")):
    sid, stil = f.stem.split("_"); soll = SEG[sid]["buch"]
    w = stt(f, "large-v3-turbo"); d = abweichung(soll, w); quelle = "turbo"
    if d:
        w2 = stt(f, "medium"); d2 = abweichung(soll, w2)
        quelle = "medium" if not d2 else "keins"
        if not d2: w = w2
    x = pcm(f, SR); m = merkmale(x, w) if len(w) > 2 else {}
    takes.setdefault(sid, []).append({"datei": f.name, "stil": stil, "treu": quelle != "keins", "quelle": quelle, "abw_turbo": d,
                                       "words": w, "m": m, "ki": ki_wert(m) if len(w) > 2 else 9})

# 2) Auswahl: wortgetreu zuerst; dann geringster KI-Wert plus Abweichung von der Gesamtlage (Tonhöhe, Tempo)
alle = [t for v in takes.values() for t in v if t["treu"] and t["m"]]
f0_med = np.median([t["m"]["F0 Hz"] for t in alle]); tempo_med = np.median([t["m"]["Tempo W/s"] for t in alle if t["datei"][:2] != "s0"])
wahl = {}
for sid in sorted(takes):
    kand = [t for t in takes[sid] if t["treu"]] or takes[sid]
    for t in kand:
        t["gesamt"] = t["ki"] + abs(12 * np.log2(t["m"]["F0 Hz"] / f0_med)) / 3 + (abs(t["m"]["Tempo W/s"] - tempo_med) / 0.5 if sid != "s0" else 0)
    wahl[sid] = min(kand, key=lambda t: t["gesamt"])

print("Segment Take   treu   KI-Wert Gesamt  Tempo  Pausen%  W/Phrase  Melodie  Endabfall  F0    Abweichungen (turbo)")
for sid in sorted(takes):
    for t in sorted(takes[sid], key=lambda t: t["stil"]):
        m = t["m"]; mark = "  <== gewählt" if t is wahl[sid] else ""
        print(f"{sid:7} {t['stil']:5} {('ja ('+t['quelle']+')') if t['treu'] else 'NEIN':12} {t['ki']:5.2f} {t.get('gesamt', float('nan')):6.2f} {m.get('Tempo W/s',0):6.2f} {m.get('Pausenanteil %',0):7.1f} {m.get('Wörter/Phrase',0):8.1f} {m.get('Melodie-Spannweite HT',0):8.1f} {m.get('Endabfall HT/s',0):9.2f} {m.get('F0 Hz',0):5.0f}  {'; '.join(t['abw_turbo'])[:90]}{mark}")
print("Bereich echter Vorleser:", {k: tuple(round(v, 2) for v in bereich(k)) for k in PRUEF})

# 3) Montage: Ränder auf Sprache schneiden (Atem/Stille weg), Lautheit angleichen, Pausen einfügen
teile, ziel = [], np.median([wahl[s]["m"]["Pegel dB"] for s in wahl])
reihen = sorted(wahl)
for i, sid in enumerate(reihen):
    t = wahl[sid]; x = pcm(TAKES / t["datei"], SR).astype(np.float64)
    n = int(SR * FL); fr = x[: len(x) // n * n].reshape(-1, n); db = 10 * np.log10((fr ** 2).mean(1) + 1e-12)
    schw = max(np.percentile(db, 95) - 35, np.percentile(db, 10) + 6)
    w0, w1 = t["words"][0]["s"], t["words"][-1]["e"]
    on = [k for k in range(int(max(0, w0 - 0.3) / FL), int((w0 + 0.15) / FL)) if k < len(db) and db[k] > schw]
    off = [k for k in range(int((w1 - 0.1) / FL), min(len(db), int((w1 + 0.6) / FL))) if db[k] > schw]
    a = max(0, (on[0] if on else int(w0 / FL)) * n - int(0.03 * SR)); b = min(len(x), ((off[-1] + 1) if off else int(w1 / FL)) * n + int(0.12 * SR))
    y = x[a:b] * 10 ** ((ziel - t["m"]["Pegel dB"]) / 20)
    fi, fo = int(0.01 * SR), int(0.06 * SR); y[:fi] *= np.linspace(0, 1, fi); y[-fo:] *= np.linspace(1, 0, fo)
    teile.append(y)
    if i < len(reihen) - 1:
        nxt = SEG[reihen[i + 1]]
        p = PAUSE["kopf"] if sid == "s0" else PAUSE["absatz"] if nxt["absatz"] != SEG[sid]["absatz"] else PAUSE["satz"]
        teile.append(np.zeros(int(p * SR)))
y = np.concatenate([np.zeros(int(0.3 * SR))] + teile + [np.zeros(int(0.8 * SR))])
y = y / max(1.0, np.abs(y).max() / 0.95)
roh = WORK / "montage.wav"
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "s16le", "-ar", str(SR), "-ac", "1", "-i", "-", str(roh)], input=(y * 32767).astype(np.int16).tobytes(), check=True)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(roh), "-codec:a", "libmp3lame", "-q:a", "2",
                "-metadata", "title=Vom glücklichen Leben, Kapitel 1", "-metadata", "artist=Seneca", str(OUT)], check=True)

# 4) Endkontrolle des Ganzen
soll = " ".join(SEG[s]["buch"] for s in reihen)
for name in ("large-v3-turbo", "medium"):
    cache = WORK / f"montage.{name}.json"
    if cache.exists(): cache.unlink()
    d = abweichung(soll, stt(roh, name)); print(f"Endkontrolle {name}: {'wortgetreu' if not d else d}")
json.dump({s: {k: v for k, v in wahl[s].items() if k != 'words'} for s in wahl}, open(WORK / "auswahl.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("Dauer", round(len(y) / SR, 1), "s →", OUT)
