# Freigestellte PNGs auf Schachbrett nebeneinander: python3 vorschau.py ziel.jpg a.png b.png …
import sys
from PIL import Image
out, files = sys.argv[1], sys.argv[2:]
ims = []
for f in files:
    im = Image.open(f).convert("RGBA"); im.thumbnail((420, 420))
    cb = Image.new("RGB", im.size, (205, 205, 205)); px = cb.load()
    for y in range(im.height):
        for x in range(im.width):
            if ((x // 16) + (y // 16)) % 2 == 0: px[x, y] = (240, 240, 240)
    cb.paste(im, (0, 0), im); ims.append(cb)
W = sum(i.width for i in ims) + 10 * len(ims); H = max(i.height for i in ims)
sheet = Image.new("RGB", (W, H), "white"); x = 0
for im in ims: sheet.paste(im, (x, 0)); x += im.width + 10
sheet.save(out, quality=88); print(out, sheet.size)
