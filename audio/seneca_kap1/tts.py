#!/usr/bin/env python3
"""Sprachausgabe über die RouteLLM-API (Abacus.AI), OpenAI-kompatibel.

Aufruf:
  python3 tts.py --model gpt-audio-1.5 --voice onyx --text seneca_kap1_text.txt --out ausgabe.mp3 [--format mp3]
Der Schlüssel kommt nur aus der Umgebungsvariable ROUTELLM_API_KEY und wird nie ausgegeben.
Antwort laut Doku: Audio base64 in choices[0].message.audio.data; tatsächlich (26.10.2026) liegt es in
message.audios[0].data (Liste), content ist leer, Transkript ggf. in audios[0].transcript. Verbrauch in usage.compute_points_used. Jeder Aufruf wird in tts_log.jsonl (neben --out) protokolliert.
"""
import argparse, base64, datetime, difflib, json, os, pathlib, re, subprocess, sys, time, urllib.request, urllib.error
from zoneinfo import ZoneInfo

BASE = "https://routellm.abacus.ai/v1"
ANWEISUNG = ("Lies den folgenden Text wörtlich und vollständig vor, ohne Begrüßung, ohne Kommentar, ohne etwas wegzulassen "
             "oder hinzuzufügen. Ruhig, klar, in gemäßigtem Tempo wie ein Hörbuchsprecher. Text:")


def key():
    k = os.environ.get("ROUTELLM_API_KEY")
    if not k:
        sys.exit("ROUTELLM_API_KEY fehlt in der Umgebung.")
    return k


def norm(s):
    return re.sub(r"[^\wäöüß]+", " ", s.lower()).strip()


def vergleich(text, transkript):
    """Wortweiser Vergleich; liefert Ähnlichkeit (0–1) und die ersten Abweichungen."""
    a, b = norm(text).split(), norm(transkript or "").split()
    sm = difflib.SequenceMatcher(a=a, b=b, autojunk=False)
    diffs = []
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op != "equal":
            diffs.append(f"{op}: '{' '.join(a[i1:i2])[:80]}' -> '{' '.join(b[j1:j2])[:80]}'")
    return round(sm.ratio(), 4), len(a), len(b), diffs[:12]


def pegel(path):
    try:
        out = subprocess.run(["ffmpeg", "-i", path, "-af", "volumedetect", "-f", "null", "-"], capture_output=True, text=True, timeout=120).stderr
        return {k: float(re.search(k + r": (-?[\d.]+) dB", out).group(1)) for k in ("mean_volume", "max_volume")}
    except Exception:
        return None


def dauer_s(path):
    try:
        out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                             capture_output=True, text=True, timeout=60).stdout.strip()
        return round(float(out), 1)
    except Exception:
        return None


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--model", required=True); p.add_argument("--voice", default="onyx")
    p.add_argument("--text", required=True); p.add_argument("--out", required=True)
    p.add_argument("--format", default="mp3"); p.add_argument("--extra", default=None, help="zusätzliches JSON, wird in den Body gemischt")
    p.add_argument("--anweisung", default=None, help="eigene Anweisung vor dem Text (Text oder @datei); Standard: ANWEISUNG")
    a = p.parse_args()
    text = pathlib.Path(a.text).read_text(encoding="utf-8").strip()
    anweisung = ANWEISUNG
    if a.anweisung:
        anweisung = pathlib.Path(a.anweisung[1:]).read_text(encoding="utf-8").strip() if a.anweisung.startswith("@") else a.anweisung
    body = {"model": a.model, "messages": [{"role": "user", "content": anweisung + "\n\n" + text}],
            "modalities": ["text", "audio"], "audio": {"voice": a.voice, "format": a.format}}
    if a.extra:
        body.update(json.loads(a.extra))
    out = pathlib.Path(a.out); out.parent.mkdir(parents=True, exist_ok=True)
    berlin = ZoneInfo("Europe/Berlin"); jetzt = lambda: datetime.datetime.now(berlin).strftime("%Y-%m-%d %H:%M:%S %Z")
    log = {"zeit": time.strftime("%Y-%m-%d %H:%M:%S"), "start_berlin": jetzt(), "model": a.model, "voice": a.voice, "format": a.format,
           "extra": a.extra, "anweisung": anweisung[:400], "textdatei": a.text, "text_zeichen": len(text)}
    t0 = time.time()
    req = urllib.request.Request(BASE + "/chat/completions", json.dumps(body).encode(),
                                 {"Authorization": f"Bearer {key()}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=600) as r:
            st, raw, hdr = r.status, r.read(), dict(r.headers)
    except urllib.error.HTTPError as e:
        st, raw, hdr = e.code, e.read(), dict(e.headers)
    log["ende_berlin"] = jetzt(); log["dauer_aufruf_s"] = round(time.time() - t0, 1); log["http"] = st
    log["antwort_header"] = hdr  # vollständig, falls Kosten-/Credit-Felder darin auftauchen
    if st != 200:
        log["fehler"] = raw[:800].decode(errors="ignore")
        with open(out.parent / "tts_log.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps(log, ensure_ascii=False) + "\n")
        print(json.dumps(log, ensure_ascii=False, indent=1)); sys.exit(1)
    resp = json.loads(raw)
    msg = resp["choices"][0]["message"]
    log["usage"] = resp.get("usage", {}); log["compute_points_used"] = log["usage"].get("compute_points_used")
    log["antwort_toplevel"] = {k: v for k, v in resp.items() if k not in ("choices",)}  # alles außer dem Audio, für Kosten-Felder
    audio = msg.get("audio") or ((msg.get("audios") or [{}])[0]) or {}
    data = audio.get("data")
    log["antwort_felder"] = sorted(msg.keys()) + ["audio:" + ",".join(sorted(k for k in audio if k != "data"))]
    if not data:
        log["fehler"] = "kein audio.data in der Antwort: " + json.dumps(resp)[:600]
        with open(out.parent / "tts_log.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps(log, ensure_ascii=False) + "\n")
        print(json.dumps(log, ensure_ascii=False, indent=1)); sys.exit(1)
    rohdaten = base64.b64decode(data)
    kopf = rohdaten[:12]
    ist_mp3 = kopf[:3] == b"ID3" or (kopf[0] == 0xFF and (kopf[1] & 0xE0) == 0xE0)
    ist_wav = kopf[:4] == b"RIFF"
    log["audio_format_antwort"] = audio.get("format")
    if a.format == "mp3" and not ist_mp3:
        # Gemini-TTS liefert rohes PCM ohne Header (26.10.2026: 16 Bit, 24 kHz, mono; audios[0].format nennt das Format).
        fmt = str(audio.get("format") or "")
        m = re.search(r"rate=(\d+)", fmt); rate = m.group(1) if m else "24000"
        roh = out.with_suffix(".wav" if ist_wav else ".pcm"); roh.write_bytes(rohdaten)
        cmd = ["ffmpeg", "-y", "-loglevel", "error"] + ([] if ist_wav else ["-f", "s16le", "-ar", rate, "-ac", "1"]) + ["-i", str(roh), "-b:a", "96k", str(out)]
        subprocess.run(cmd, check=True); roh.unlink()
        log["konvertiert_von"] = ("wav" if ist_wav else f"pcm s16le {rate} Hz mono")
    else:
        out.write_bytes(rohdaten)
    transkript = msg.get("content") or audio.get("transcript") or ""
    if isinstance(transkript, list):
        transkript = " ".join(p.get("text", "") for p in transkript if isinstance(p, dict))
    ratio, nw_text, nw_tr, diffs = vergleich(text, transkript)
    usage = resp.get("usage", {})
    log.update({"datei": str(out), "bytes": out.stat().st_size, "dauer_datei_s": dauer_s(str(out)), "pegel": pegel(str(out)),
                "transkript_woerter": nw_tr, "text_woerter": nw_text, "aehnlichkeit": ratio, "abweichungen": diffs,
                "transkript": transkript[:3000]})
    with open(out.parent / "tts_log.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(log, ensure_ascii=False) + "\n")
    kurz = {k: v for k, v in log.items() if k not in ("transkript", "antwort_header", "anweisung")}
    print(json.dumps(kurz, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
