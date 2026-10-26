#!/usr/bin/env python3
"""Mehrfach-Durchläufe satzweise über die RouteLLM-API (Gemini TTS), verlustfrei als FLAC.

Aufruf: python3 takes.py [segmente.json]
Für jedes Segment und jeden Stil (takes: s0 → takes["s0"], sonst takes["rest"]) genau ein Aufruf; bei HTTP-Fehler oder leerer
Antwort eine Wiederholung, sonst als fehlgeschlagen protokolliert. Rohes PCM (L16, s16le, 24 kHz, mono) → ffmpeg → FLAC.
Kostenbremse: Summe output_tokens ≤ MAX_OUTPUT_TOKENS, sonst Stopp vor dem nächsten Aufruf.
Schlüssel nur aus ROUTELLM_API_KEY, wird nie ausgegeben. Log: takes_log.jsonl neben der Segmentdatei.
"""
import base64, datetime, json, os, pathlib, re, subprocess, sys, time, urllib.error, urllib.request
from zoneinfo import ZoneInfo

BASE = "https://routellm.abacus.ai/v1"
MAX_OUTPUT_TOKENS = 15000
BERLIN = ZoneInfo("Europe/Berlin")


def jetzt():
    return datetime.datetime.now(BERLIN).strftime("%Y-%m-%d %H:%M:%S %Z")


def dauer_s(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                         capture_output=True, text=True, timeout=60).stdout.strip()
    return round(float(out), 2) if out else None


def aufruf(modell, voice, content, timeout=600):
    body = {"model": modell, "messages": [{"role": "user", "content": content}], "modalities": ["text", "audio"],
            "audio": {"voice": voice, "format": "mp3"}}
    req = urllib.request.Request(BASE + "/chat/completions", json.dumps(body).encode(),
                                 {"Authorization": f"Bearer {os.environ['ROUTELLM_API_KEY']}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()


def main():
    cfg_path = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else pathlib.Path(__file__).with_name("segmente.json"))
    cfg = json.loads(cfg_path.read_text(encoding="utf-8")); ordner = cfg_path.parent
    logpfad = ordner / "takes_log.jsonl"
    summe_out = summe_in = 0; erfolge = 0; plan = []
    for seg in cfg["segmente"]:
        for stil in cfg["takes"].get(seg["id"], cfg["takes"]["rest"]):
            plan.append((seg, stil))
    print(f"{len(plan)} Aufrufe geplant, Modell {cfg['modell']}, Voice {cfg['voice']}")
    for seg, stil in plan:
        if summe_out >= MAX_OUTPUT_TOKENS:
            print(f"STOPP Kostenbremse: output_tokens {summe_out} ≥ {MAX_OUTPUT_TOKENS}"); break
        content = cfg["anweisung"][stil] + " " + seg["sprech"]
        ziel = ordner / f"{seg['id']}_{stil}.flac"
        for versuch in (1, 2):
            log = {"segment_id": seg["id"], "stil": stil, "versuch": versuch, "start_berlin": jetzt(), "modell": cfg["modell"], "voice": cfg["voice"]}
            t0 = time.time(); st, raw = aufruf(cfg["modell"], cfg["voice"], content)
            log["ende_berlin"] = jetzt(); log["dauer_aufruf_s"] = round(time.time() - t0, 1); log["http"] = st
            data = None; fmt = None
            if st == 200:
                try:
                    resp = json.loads(raw); msg = resp["choices"][0]["message"]
                    audio = msg.get("audio") or ((msg.get("audios") or [{}])[0]) or {}
                    data = audio.get("data"); fmt = audio.get("format")
                    u = resp.get("usage", {}); log["input_tokens"] = u.get("input_tokens"); log["output_tokens"] = u.get("output_tokens")
                    log["compute_points_used"] = u.get("compute_points_used")
                except Exception as e:
                    log["fehler"] = f"Antwort nicht lesbar: {e}: {raw[:300].decode(errors='ignore')}"
            else:
                log["fehler"] = raw[:600].decode(errors="ignore")
            if data:
                pcm = base64.b64decode(data); roh = ziel.with_suffix(".pcm"); roh.write_bytes(pcm)
                kopf = pcm[:4]; m = re.search(r"rate=(\d+)", str(fmt or "")); rate = m.group(1) if m else "24000"
                cmd = ["ffmpeg", "-y", "-loglevel", "error"] + ([] if kopf == b"RIFF" else ["-f", "s16le", "-ar", rate, "-ac", "1"]) + ["-i", str(roh), str(ziel)]
                subprocess.run(cmd, check=True); roh.unlink()
                log.update({"audio_format": fmt, "datei": ziel.name, "bytes": ziel.stat().st_size, "dauer_datei_s": dauer_s(str(ziel)), "status": "ok"})
                summe_out += log.get("output_tokens") or 0; summe_in += log.get("input_tokens") or 0; erfolge += 1
            elif "fehler" not in log:
                log["fehler"] = "leere Antwort (kein audio.data)"
            if "fehler" in log:
                log["status"] = "fehlgeschlagen" if versuch == 2 else "wiederholung"
                summe_out += log.get("output_tokens") or 0; summe_in += log.get("input_tokens") or 0
            with open(logpfad, "a", encoding="utf-8") as f:
                f.write(json.dumps(log, ensure_ascii=False) + "\n")
            print(json.dumps({k: v for k, v in log.items() if k != "fehler"} | ({"fehler": log["fehler"][:200]} if "fehler" in log else {}), ensure_ascii=False))
            if log["status"] == "ok":
                break
    print(f"FERTIG: {erfolge}/{len(plan)} Takes, input_tokens {summe_in}, output_tokens {summe_out}")


if __name__ == "__main__":
    main()
