import sys, json, glob, wave, numpy as np
from faster_whisper import WhisperModel
m = WhisperModel("large-v3-turbo", device="cpu", compute_type="int8", cpu_threads=4)
for f in sorted(glob.glob(sys.argv[1] + "/*.wav")):
    out = f[:-4] + ".words.json"
    w = wave.open(f); a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    segs, _ = m.transcribe(a, language="de", beam_size=5, word_timestamps=True, condition_on_previous_text=False, vad_filter=True)
    words = [{"w": x.word.strip(), "s": round(x.start, 2), "e": round(x.end, 2), "p": round(x.probability, 3)} for s in segs for x in s.words]
    json.dump(words, open(out, "w"), ensure_ascii=False); print("ok", f.rsplit("/", 1)[-1], len(words), flush=True)
