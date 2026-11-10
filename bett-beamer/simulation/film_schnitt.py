#!/usr/bin/env python3
"""Filmbilder + Untertitel -> MP4. Aufruf: python3 film_schnitt.py <bildordner> <ausgabe.mp4> [fps]"""
import json
import os
import subprocess
import sys

ordner, ausgabe = sys.argv[1], sys.argv[2]
fps = int(sys.argv[3]) if len(sys.argv) > 3 else 25
texte = json.load(open(sorted(d for d in (os.path.join(ordner, f) for f in os.listdir(ordner)) if "texte_" in d)[0], encoding="utf-8"))
dauer = len([f for f in os.listdir(ordner) if f.startswith("f") and f.endswith(".jpg")]) / fps
fett = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
normal = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
filter_ = ["scale=1280:720"]
for i, (a, b, t) in enumerate(texte):
    datei = os.path.join(ordner, f"text{i}.txt")
    open(datei, "w", encoding="utf-8").write(t)
    ein = f"if(lt(t,{a}+0.3),(t-{a})/0.3,if(gt(t,{b}-0.3),({b}-t)/0.3,1))"
    filter_.append(
        f"drawtext=fontfile={fett}:textfile={datei}:fontsize=30:fontcolor=white:alpha='{ein}':"
        f"box=1:boxcolor=black@0.55:boxborderw=14:x=(w-text_w)/2:y=h-86:enable='between(t,{a},{b})'")
fuss = os.path.join(ordner, "fuss.txt")
open(fuss, "w", encoding="utf-8").write("3D-Simulation · Vorentwurf · Maße wie Bauzeichnung, Wand 2,5 m angenommen")
filter_.append(f"drawtext=fontfile={normal}:textfile={fuss}:fontsize=16:fontcolor=white@0.75:x=16:y=16")
filter_.append(f"fade=t=in:st=0:d=0.6,fade=t=out:st={dauer - 0.7:.2f}:d=0.7")
cmd = ["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(fps), "-i", os.path.join(ordner, "f%04d.jpg"),
       "-vf", ",".join(filter_), "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "21", "-preset", "slow",
       "-movflags", "+faststart", ausgabe]
subprocess.run(cmd, check=True)
print("geschrieben:", ausgabe)
