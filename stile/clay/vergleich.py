# Original | Nachbau nebeneinander (gleiche Höhe): python3 vergleich.py original.jpg nachbau.png ausgabe.jpg
import sys
from PIL import Image
o, n, out = sys.argv[1:4]
a = Image.open(o).convert("RGB"); b = Image.open(n).convert("RGB")
H = 1835
a = a.resize((round(a.width * H / a.height), H), Image.LANCZOS); b = b.resize((round(b.width * H / b.height), H), Image.LANCZOS)
s = Image.new("RGB", (a.width + b.width + 30, H), "white"); s.paste(a, (0, 0)); s.paste(b, (a.width + 30, 0))
s.save(out, quality=90); print(out, s.size)
