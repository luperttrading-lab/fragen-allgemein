#!/usr/bin/env python3
"""Freistellen von Knet-Objekten auf uniformem Beige-Grund (Schwellwert auf Farbabstand + Flood-Fill vom Rand + weiche Kante).
Aufruf: python3 freistellen.py quelle.png ziel.png [--method rembg|schwelle] [--tol 22] [--chroma 9] [--feather 2] [--pad 8]
Befund 18.10.2026: rembg (u2net) ist bei Objekten mit Verlauf im Grund (Hero, Ballons, Umschlag) klar besser; der
Schwellwert gewinnt nur bei flachen Objekten mit Grund-farbigen Innenflächen (Wecker: rembg füllt das Zifferblatt).
Kontaktschatten (gleiche Farbigkeit wie der Grund, nur dunkler) wird als Hintergrund behandelt; der Schatten kommt später aus CSS."""
import argparse, numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage

def cutout(src, dst, tol=22, chroma=9, feather=2.0, pad=8, keep_shadow=False):
    im = Image.open(src).convert("RGB"); a = np.asarray(im).astype(np.float32); h, w, _ = a.shape
    b = 24
    border = np.concatenate([a[:b].reshape(-1, 3), a[-b:].reshape(-1, 3), a[:, :b].reshape(-1, 3), a[:, -b:].reshape(-1, 3)])
    bg = np.median(border, axis=0)
    d = np.sqrt(((a - bg) ** 2).sum(-1))                       # RGB-Abstand
    n = a / np.clip(a.sum(-1, keepdims=True), 1, None); nb = bg / bg.sum()
    cd = np.sqrt(((n - nb) ** 2).sum(-1)) * 765                 # Farbigkeits-Abstand (schattenunabhängig)
    lum = a.mean(-1); lb = bg.mean()
    if keep_shadow:
        bglike = d < tol
    else:
        bglike = ((cd < chroma) & (lum < lb + tol)) | (d < tol * 0.6)  # gleich farbig und nicht heller → Grund oder Schatten
    lab, nlab = ndimage.label(bglike)
    edge = np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]])); edge = edge[edge > 0]
    obj = ~np.isin(lab, edge)
    obj = ndimage.binary_opening(obj, iterations=2)
    obj = ndimage.binary_closing(obj, iterations=3)
    lab2, n2 = ndimage.label(obj)
    if n2 > 1:
        sizes = ndimage.sum(obj, lab2, range(1, n2 + 1)); keep = [i + 1 for i, s in enumerate(sizes) if s > 0.002 * obj.sum()]
        obj = np.isin(lab2, keep)
    alpha = Image.fromarray((obj * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(feather))
    al = np.asarray(alpha).astype(np.float32) / 255
    out = a.copy(); m = (al > 0.02) & (al < 0.98)
    out[m] = np.clip((a[m] - (1 - al[m][:, None]) * bg) / np.clip(al[m][:, None], 0.05, 1), 0, 255)
    rgba = np.dstack([out, al * 255]).astype(np.uint8)
    ys, xs = np.where(al > 0.02)
    y0, y1, x0, x1 = max(ys.min() - pad, 0), min(ys.max() + pad, h), max(xs.min() - pad, 0), min(xs.max() + pad, w)
    Image.fromarray(rgba[y0:y1, x0:x1]).save(dst)
    print(f"{dst}: bg={bg.astype(int).tolist()} box=({x0},{y0})-({x1},{y1}) {x1-x0}x{y1-y0}")

def cutout_rembg(src, dst, pad=8, schatten_weg=True):
    """rembg (u2net); danach Reste des Kontaktschattens entfernen: Pixel mit der Farbigkeit des Grundes, die nicht heller
    als der Grund sind, werden transparent (das cremefarbene Etikett ist heller und bleibt)."""
    from rembg import remove, new_session
    im = Image.open(src).convert("RGB"); out = remove(im, session=new_session("u2net"))
    if schatten_weg:
        a = np.asarray(im).astype(np.float32); o = np.asarray(out).astype(np.float32); b = 24
        border = np.concatenate([a[:b].reshape(-1, 3), a[-b:].reshape(-1, 3), a[:, :b].reshape(-1, 3), a[:, -b:].reshape(-1, 3)])
        bg = np.median(border, axis=0)
        n = a / np.clip(a.sum(-1, keepdims=True), 1, None); nb = bg / bg.sum()
        cd = np.sqrt(((n - nb) ** 2).sum(-1)) * 765; lum = a.mean(-1)
        shadow = (cd < 12) & (lum < bg.mean() - 15)   # nur deutlich dunkler: Creme-Flächen (Etikett, Umschlag) bleiben
        shadow = ndimage.binary_opening(shadow, iterations=2)
        al = o[:, :, 3]; al[shadow] = 0
        alpha = Image.fromarray(al.astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.8))
        o[:, :, 3] = np.minimum(np.asarray(alpha), al + 40)  # nur weich ausblenden, nicht aufhellen
        out = Image.fromarray(o.astype(np.uint8))
    al = np.asarray(out)[:, :, 3]; ys, xs = np.where(al > 5); h, w = al.shape
    y0, y1, x0, x1 = max(ys.min() - pad, 0), min(ys.max() + pad, h), max(xs.min() - pad, 0), min(xs.max() + pad, w)
    out.crop((x0, y0, x1, y1)).save(dst); print(f"{dst}: rembg box=({x0},{y0})-({x1},{y1}) {x1-x0}x{y1-y0}")


if __name__ == "__main__":
    p = argparse.ArgumentParser(); p.add_argument("src"); p.add_argument("dst")
    p.add_argument("--tol", type=float, default=22); p.add_argument("--chroma", type=float, default=9)
    p.add_argument("--feather", type=float, default=2.0); p.add_argument("--pad", type=int, default=8)
    p.add_argument("--keep-shadow", action="store_true", help="Schattenbereinigung aus (nötig bei cremefarbenen Objekten mit Schattenseite, z. B. Umschlag)")
    p.add_argument("--method", default="rembg", choices=["rembg", "schwelle"])
    a = p.parse_args()
    if a.method == "rembg": cutout_rembg(a.src, a.dst, a.pad, schatten_weg=not a.keep_shadow)
    else: cutout(a.src, a.dst, a.tol, a.chroma, a.feather, a.pad, a.keep_shadow)
