import sys, glob, wave, numpy as np
from speechmos import dnsmos
for f in sorted(glob.glob(sys.argv[1] + "/*.wav")):
    w = wave.open(f); a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    r = []
    for i in range(0, len(a) - 16000 * 10 + 1, 16000 * 10):         # 10-s-Fenster
        seg = a[i:i + 160000]
        if np.abs(seg).max() < 1e-3: continue
        r.append(dnsmos.run(seg / max(1e-6, np.abs(seg).max()) * 0.9, 16000))
    m = {k: np.mean([x[k] for x in r]) for k in ("p808_mos", "sig_mos", "bak_mos", "ovrl_mos")}
    print(f"{f.rsplit('/',1)[-1][:-4]:36} P808 {m['p808_mos']:.2f}  SIG {m['sig_mos']:.2f}  BAK {m['bak_mos']:.2f}  OVRL {m['ovrl_mos']:.2f}  n={len(r)}", flush=True)
