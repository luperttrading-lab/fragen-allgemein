#!/usr/bin/env python3
"""Erreichbarkeit neuer Sprachmodelle über RouteLLM und Stimmen-Casting (Gemini 3.8 Flash TTS = gemini_tts).

Schritt 1: gemini_tts, minimax_tts, openai_tts, hume, seed_speech je ≤ 3 Versuche über POST /v1/chat/completions
  (1) modalities ["text","audio"], audio {voice: echo, format: wav}; (2) modalities ["audio"]; (3) aus der Fehlermeldung abgeleitet
  (erlaubte Voice/Format, sonst alloy + mp3). Alle Fehlertexte wörtlich ins Log.
Schritt 2 (nur wenn gemini_tts antwortet): Testsatz mit voice Charon, Sadaltager, Iapetus, Orus, Algenib, Schedar; Ersatz: OpenAI-Namen.
Schritt 3: Probe, ob ein Stilfeld akzeptiert wird (audio.style, speech_metadata) – Fehler kosten nichts.
Kostenbremse: höchstens MAX_OK erfolgreiche Audio-Aufrufe. Schlüssel nur aus ROUTELLM_API_KEY. Log: casting_log.jsonl.
"""
import base64, datetime, json, os, pathlib, re, subprocess, time, urllib.error, urllib.request
from zoneinfo import ZoneInfo

BASE = "https://routellm.abacus.ai/v1"; BERLIN = ZoneInfo("Europe/Berlin"); MAX_OK = 12
ORDNER = pathlib.Path(__file__).parent; LOG = ORDNER / "casting_log.jsonl"
TESTSATZ = "Glücklich zu leben, mein lieber Gallio, wollen alle. <short pause> Aber der Blick der Meisten ist getrübt."
CONTENT = "Lies wörtlich vor, ruhig und natürlich wie ein Hörbuchsprecher: " + TESTSATZ
ok_zaehler = 0


def jetzt():
    return datetime.datetime.now(BERLIN).strftime("%Y-%m-%d %H:%M:%S %Z")


def post(pfad, body):
    req = urllib.request.Request(BASE + pfad, json.dumps(body).encode(),
                                 {"Authorization": f"Bearer {os.environ['ROUTELLM_API_KEY']}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            return r.status, r.read(), dict(r.headers)
    except urllib.error.HTTPError as e:
        return e.code, e.read(), dict(e.headers)


def speichern(data, fmt, ziel_basis):
    roh = base64.b64decode(data); kopf = roh[:4]
    if kopf[:3] == b"ID3" or (roh[0] == 0xFF and (roh[1] & 0xE0) == 0xE0):
        ziel = ziel_basis.with_suffix(".mp3"); ziel.write_bytes(roh); art = "mp3 belassen"
    elif kopf == b"RIFF":
        ziel = ziel_basis.with_suffix(".wav"); ziel.write_bytes(roh); art = "wav belassen"
    else:
        m = re.search(r"rate=(\d+)", str(fmt or "")); rate = m.group(1) if m else "24000"
        pcm = ziel_basis.with_suffix(".pcm"); pcm.write_bytes(roh); ziel = ziel_basis.with_suffix(".flac")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "s16le", "-ar", rate, "-ac", "1", "-i", str(pcm), str(ziel)], check=True)
        pcm.unlink(); art = f"pcm s16le {rate} Hz mono → flac"
    d = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(ziel)],
                       capture_output=True, text=True).stdout.strip()
    return ziel.name, art, round(float(d), 2) if d else None


def versuch(modell, body, ziel_basis, schritt, zusatz=None):
    """Ein Aufruf; gibt (erfolg, fehlertext) zurück und protokolliert alles."""
    global ok_zaehler
    log = {"schritt": schritt, "modell": modell, "body_ohne_content": {k: v for k, v in body.items() if k != "messages"},
           "start_berlin": jetzt()}
    if zusatz: log.update(zusatz)
    t0 = time.time(); st, raw, hdr = post("/chat/completions", body)
    log["ende_berlin"] = jetzt(); log["dauer_aufruf_s"] = round(time.time() - t0, 1); log["http"] = st
    if st != 200:
        log["fehler"] = raw[:1500].decode(errors="ignore"); log["status"] = "fehler"
    else:
        try:
            resp = json.loads(raw); msg = resp["choices"][0]["message"]
            audio = msg.get("audio") or ((msg.get("audios") or [{}])[0]) or {}
            log["usage"] = resp.get("usage"); log["antwort_felder"] = sorted(msg.keys())
            log["audio_felder"] = sorted(k for k in audio if k != "data")
            log["content"] = msg.get("content"); log["transcript"] = audio.get("transcript")
            if audio.get("data"):
                name, art, dauer = speichern(audio["data"], audio.get("format"), ziel_basis)
                log.update({"datei": name, "umwandlung": art, "audio_format": audio.get("format"), "dauer_datei_s": dauer, "status": "ok"})
                ok_zaehler += 1
            else:
                log["fehler"] = "HTTP 200, aber kein audio.data: " + json.dumps(resp)[:800]; log["status"] = "leer"
        except Exception as e:
            log["fehler"] = f"Antwort nicht lesbar: {e}: {raw[:400].decode(errors='ignore')}"; log["status"] = "fehler"
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(log, ensure_ascii=False) + "\n")
    print(f"[{schritt}] {modell} {body.get('audio')} -> {st} {log['status']} {log.get('datei', '')} {log.get('fehler', '')[:160]}")
    return log["status"] == "ok", log.get("fehler", "")


def body_fuer(modell, voice="echo", fmt="wav", modalities=("text", "audio"), extra=None):
    b = {"model": modell, "messages": [{"role": "user", "content": CONTENT}], "modalities": list(modalities), "audio": {"voice": voice, "format": fmt}}
    if extra: b.update(extra)
    return b


def main():
    # Schritt 1: Erreichbarkeit
    erreichbar = {}
    for modell in ["gemini_tts", "minimax_tts", "openai_tts", "hume", "seed_speech"]:
        ziel = ORDNER / f"{modell}_echo"
        ok, fehler = versuch(modell, body_fuer(modell), ziel, "1a")
        if not ok and ok_zaehler < MAX_OK:
            ok, fehler = versuch(modell, body_fuer(modell, modalities=("audio",)), ziel, "1b")
        if not ok and ok_zaehler < MAX_OK:
            # aus der Fehlermeldung ableiten: genannte Voices/Formate verwenden
            m = re.search(r"[Vv]oices?[^:]*:\s*([A-Za-z0-9_ ,\-]+)", fehler); voice = m.group(1).split(",")[0].strip() if m else "alloy"
            f = re.search(r"[Ff]ormats?[^:]*:\s*([A-Za-z0-9_ ,\-]+)", fehler); fmt = f.group(1).split(",")[0].strip() if f else "mp3"
            ok, fehler = versuch(modell, body_fuer(modell, voice=voice, fmt=fmt, modalities=("audio",)), ORDNER / f"{modell}_{voice}", "1c",
                                 {"abgeleitet_aus_fehler": True})
        erreichbar[modell] = ok
    print("Erreichbar:", erreichbar, "erfolgreiche Audio-Aufrufe bisher:", ok_zaehler)
    # Schritt 2: Casting
    if erreichbar.get("gemini_tts"):
        stimmen = ["Charon", "Sadaltager", "Iapetus", "Orus", "Algenib", "Schedar"]
        ok1, fehler = (None, "")
        for i, v in enumerate(stimmen):
            if ok_zaehler >= MAX_OK:
                print("STOPP Kostenbremse"); break
            ok, fehler = versuch("gemini_tts", body_fuer("gemini_tts", voice=v), ORDNER / f"gemini_tts_{v}", "2")
            if i == 0 and not ok:
                print("Gemini-Stimmennamen abgelehnt, Ersatz OpenAI-Namen:", fehler[:200])
                stimmen = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
                for v2 in stimmen:
                    if ok_zaehler >= MAX_OK: break
                    versuch("gemini_tts", body_fuer("gemini_tts", voice=v2), ORDNER / f"gemini_tts_{v2}", "2")
                break
        # Schritt 3: Stilfeld-Probe (nur falls Budget übrig; ein 400 kostet nichts)
        if ok_zaehler < MAX_OK:
            versuch("gemini_tts", body_fuer("gemini_tts", voice="Charon", extra={"audio": {"voice": "Charon", "format": "wav", "style": "ruhig, wie ein Hörbuchsprecher"}}),
                    ORDNER / "gemini_tts_Charon_style", "3a", {"probe": "audio.style"})
        if ok_zaehler < MAX_OK:
            versuch("gemini_tts", body_fuer("gemini_tts", voice="Charon", extra={"speech_metadata": {"style": "ruhig, wie ein Hörbuchsprecher"}}),
                    ORDNER / "gemini_tts_Charon_speechmeta", "3b", {"probe": "speech_metadata.style"})
    print("FERTIG, erfolgreiche Audio-Aufrufe:", ok_zaehler)


if __name__ == "__main__":
    main()
