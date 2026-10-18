# -*- coding: utf-8 -*-
"""Baut v2.html (Stil „Professional“, NotebookLM-Vorbild) aus Python heraus:
alle Illustrationen sind flache SVGs, das Low-Poly-Gehirn entsteht per Delaunay."""
import math, random, colorsys, os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "v2.html")

# ---------- Palette ----------
BG      = "#eff0f4"
INK     = "#15181d"
LINE_D  = "#4a5560"   # dunkle Rahmenlinien
NAVY    = "#2d4461"
NAVY2   = "#3b5878"
NAVY_D  = "#1f3148"
SLATE   = "#6f879f"
SLATE_L = "#a3b3c2"
SAND    = "#e8c76c"
SAND_L  = "#f1dc9a"
OCHRE   = "#d3a243"
OCHRE_L = "#d9b25a"   # Linien
SAGE    = "#6c8a70"
SAGE_D  = "#4c6a57"
TAUPE   = "#b7ab97"
GREY    = "#8b949c"
GREY_L  = "#b9bfc5"
ORANGE  = "#d8672d"
ORANGE_D= "#b8501d"
TEAL    = "#2a7f7f"
BEIGE   = "#e3d9c3"
WHITE   = "#f7f7f9"

def shade(hexcol, dl):
    h = hexcol.lstrip("#"); r, g, b = (int(h[i:i+2], 16)/255 for i in (0, 2, 4))
    hh, l, s = colorsys.rgb_to_hls(r, g, b)
    l = max(0, min(1, l + dl))
    r, g, b = colorsys.hls_to_rgb(hh, l, s)
    return "#%02x%02x%02x" % (round(r*255), round(g*255), round(b*255))

# ---------- Geometrie ----------
def catmull(points, n_per=8, closed=True):
    pts = list(points)
    out = []
    m = len(pts)
    for i in range(m if closed else m-1):
        p0 = pts[(i-1) % m]; p1 = pts[i]; p2 = pts[(i+1) % m]; p3 = pts[(i+2) % m]
        for k in range(n_per):
            t = k / n_per; t2 = t*t; t3 = t2*t
            x = 0.5*((2*p1[0]) + (-p0[0]+p2[0])*t + (2*p0[0]-5*p1[0]+4*p2[0]-p3[0])*t2 + (-p0[0]+3*p1[0]-3*p2[0]+p3[0])*t3)
            y = 0.5*((2*p1[1]) + (-p0[1]+p2[1])*t + (2*p0[1]-5*p1[1]+4*p2[1]-p3[1])*t2 + (-p0[1]+3*p1[1]-3*p2[1]+p3[1])*t3)
            out.append((x, y))
    return out

def resample(poly, step):
    # gleichmäßig entlang des Umfangs
    pts = poly + [poly[0]]
    out = [pts[0]]; acc = 0.0
    for a, b in zip(pts, pts[1:]):
        seg = math.dist(a, b)
        while acc + seg >= step:
            t = (step - acc) / seg
            a = (a[0] + (b[0]-a[0])*t, a[1] + (b[1]-a[1])*t)
            out.append(a); seg = math.dist(a, b); acc = 0.0
        acc += seg
    return out

def inside(poly, x, y):
    c = False; n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]; x2, y2 = poly[(i+1) % n]
        if (y1 > y) != (y2 > y):
            xi = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
            if x < xi: c = not c
    return c

def dist_to_poly(poly, x, y):
    best = 1e9; n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]; x2, y2 = poly[(i+1) % n]
        dx, dy = x2-x1, y2-y1
        L2 = dx*dx+dy*dy
        t = 0 if L2 == 0 else max(0, min(1, ((x-x1)*dx+(y-y1)*dy)/L2))
        best = min(best, math.hypot(x-(x1+t*dx), y-(y1+t*dy)))
    return best

def delaunay(pts):
    minx = min(p[0] for p in pts); maxx = max(p[0] for p in pts)
    miny = min(p[1] for p in pts); maxy = max(p[1] for p in pts)
    dmax = max(maxx-minx, maxy-miny); mx = (minx+maxx)/2; my = (miny+maxy)/2
    P = list(pts) + [(mx-20*dmax, my-dmax), (mx, my+20*dmax), (mx+20*dmax, my-dmax)]
    n = len(pts)
    def circ(t):
        (ax, ay), (bx, by), (cx, cy) = P[t[0]], P[t[1]], P[t[2]]
        d = 2*(ax*(by-cy)+bx*(cy-ay)+cx*(ay-by))
        if abs(d) < 1e-12: return (0, 0, 1e18)
        ux = ((ax*ax+ay*ay)*(by-cy)+(bx*bx+by*by)*(cy-ay)+(cx*cx+cy*cy)*(ay-by))/d
        uy = ((ax*ax+ay*ay)*(cx-bx)+(bx*bx+by*by)*(ax-cx)+(cx*cx+cy*cy)*(bx-ax))/d
        return (ux, uy, (ax-ux)**2+(ay-uy)**2)
    tris = {(n, n+1, n+2): circ((n, n+1, n+2))}
    for i in range(n):
        x, y = P[i]
        bad = [t for t, c in tris.items() if (x-c[0])**2+(y-c[1])**2 < c[2]]
        edges = {}
        for t in bad:
            for e in ((t[0], t[1]), (t[1], t[2]), (t[2], t[0])):
                k = tuple(sorted(e)); edges[k] = edges.get(k, 0)+1
        for t in bad: del tris[t]
        for k, cnt in edges.items():
            if cnt == 1:
                nt = (k[0], k[1], i); tris[nt] = circ(nt)
    return [t for t in tris if all(v < n for v in t)]

def lowpoly(outline_ctrl, spacing, seed, palette, band_scale, band_dir=(0.55, 0.85), jitter=0.45, light=0.05, extra=None):
    """outline_ctrl: Kontrollpunkte (Catmull-Rom). Liefert SVG-Polygone (als String) in lokalen Koordinaten."""
    rnd = random.Random(seed)
    outline = catmull(outline_ctrl, 6)
    border = resample(outline, spacing*0.85)
    xs = [p[0] for p in outline]; ys = [p[1] for p in outline]
    pts = list(border)
    y = min(ys) + spacing*0.6
    row = 0
    while y < max(ys):
        x = min(xs) + (spacing*0.5 if row % 2 else 0) + spacing*0.3
        while x < max(xs):
            px = x + rnd.uniform(-0.3, 0.3)*spacing; py = y + rnd.uniform(-0.3, 0.3)*spacing
            if inside(outline, px, py) and dist_to_poly(outline, px, py) > spacing*0.42:
                pts.append((px, py))
            x += spacing
        y += spacing*0.87; row += 1
    tris = delaunay(pts)
    polys = []
    for t in tris:
        (ax, ay), (bx, by), (cx, cy) = pts[t[0]], pts[t[1]], pts[t[2]]
        gx, gy = (ax+bx+cx)/3, (ay+by+cy)/3
        if not inside(outline, gx, gy): continue
        v = (band_dir[0]*gx + band_dir[1]*gy)/band_scale + rnd.uniform(-jitter, jitter)
        col = palette[int(math.floor(v)) % len(palette)]
        r = rnd.random()
        if extra and r < extra[1]: col = extra[0]
        col = shade(col, rnd.uniform(-light, light))
        polys.append((f"{ax:.1f},{ay:.1f} {bx:.1f},{by:.1f} {cx:.1f},{cy:.1f}", col))
    return polys, outline

def polys_svg(polys, stroke_w=0.7):
    return "".join(f'<polygon points="{p}" fill="{c}" stroke="{c}" stroke-width="{stroke_w}" stroke-linejoin="round"/>' for p, c in polys)

# ---------- Großes Gehirn (Seitenansicht, Stirn rechts) ----------
# lokale Box 300 x 300
BRAIN_CTRL = [
    (20, 160), (24, 124), (36, 92), (56, 64), (84, 42), (118, 26), (156, 18), (196, 16), (236, 22), (270, 36),
    (296, 60), (312, 90), (320, 124), (318, 156), (308, 184), (292, 204), (270, 216), (254, 212),
    (246, 226), (226, 242), (200, 250), (176, 246), (164, 236), (158, 226),
    (146, 240), (126, 254), (100, 258), (74, 250), (52, 232), (34, 208), (24, 184),
]
STEM = "150,228 176,230 186,256 182,290 162,296 150,270 142,244"
def brain_stem(x, y, sx, sy):
    pts = " ".join(f"{x+float(a)*sx:.1f},{y+float(b)*sy:.1f}" for a, b in (q.split(",") for q in STEM.split()))
    return f'<polygon points="{pts}" fill="{NAVY}"/>' 
BRAIN_PAL = [NAVY, SLATE, SAND, SAGE, NAVY2, TAUPE, SAND_L, GREY, SAGE_D, SLATE_L, NAVY_D]

def big_brain(x0, y0, sc=0.9):
    polys, outline = lowpoly(BRAIN_CTRL, 34, 11, BRAIN_PAL, 46, jitter=0.4, extra=(ORANGE, 0.025))
    W = round(330*sc); H = round(300*sc)
    return (f'<svg class="abs" style="left:{x0}px;top:{y0}px" width="{W}" height="{H}" viewBox="0 0 330 300">'
            + brain_stem(0, 0, 1, 1) + f'<polygon points="162,236 176,230 186,256 172,262" fill="{SLATE}"/>' + polys_svg(polys) + '</svg>')

# ---------- kleines Gehirn (Illustration 1) ----------
SMALL_PAL = [SLATE, NAVY, SAND, SLATE_L, TAUPE, NAVY2, SAGE]
def small_brain(x, y, w, h, seed=5):
    polys, outline = lowpoly(BRAIN_CTRL, 44, seed, SMALL_PAL, 52, light=0.04, extra=(ORANGE, 0.03))
    sx, sy = w/330, h/300
    return f'<g transform="translate({x} {y}) scale({sx:.3f} {sy:.3f})">' + brain_stem(0, 0, 1, 1) + polys_svg(polys, 1.0) + '</g>'

# ---------- Hilfen ----------
def gear(cx, cy, r, teeth, fill, hole=0.42):
    pts = []
    for i in range(teeth*2):
        a = math.pi*2*i/(teeth*2)
        rr = r if i % 2 == 0 else r*0.74
        for da in (-0.55, 0.55):
            aa = a + da*math.pi/(teeth*2)
            pts.append((cx+rr*math.cos(aa), cy+rr*math.sin(aa)))
    d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + "Z"
    d += f" M{cx+r*hole:.1f} {cy:.1f} a{r*hole:.1f} {r*hole:.1f} 0 1 0 {-2*r*hole:.1f} 0 a{r*hole:.1f} {r*hole:.1f} 0 1 0 {2*r*hole:.1f} 0Z"
    return f'<path d="{d}" fill="{fill}" fill-rule="evenodd"/>'

def arrow(x1, y1, x2, y2, col, w=1.6, head=7):
    ang = math.atan2(y2-y1, x2-x1)
    hx = x2 - head*math.cos(ang); hy = y2 - head*math.sin(ang)
    px = -math.sin(ang)*head*0.5; py = math.cos(ang)*head*0.5
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{hx:.1f}" y2="{hy:.1f}" stroke="{col}" stroke-width="{w}"/>'
            f'<polygon points="{x2:.1f},{y2:.1f} {hx+px:.1f},{hy+py:.1f} {hx-px:.1f},{hy-py:.1f}" fill="{col}"/>')

def text(x, y, s, size=13, weight=700, fill=INK, anchor="start", upper=True, family="Roboto Condensed", extra=""):
    if upper: s = s.upper()
    s = s.replace("&", "&amp;")
    return f'<text x="{x}" y="{y}" font-family="{family}" font-weight="{weight}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" {extra}>{s}</text>'

# ---------- Illustration 1: Gehirn, Ziel, bröckelnder Block, Klemmbrett, Stoppuhr ----------
def illu_paradox():
    s = '<svg class="abs" style="left:42px;top:346px" width="300" height="222" viewBox="0 0 300 222">'
    # Gehirn
    s += small_brain(54, 22, 160, 142, seed=21)
    # Pfeil vom Gehirn zur Zielscheibe (Sand) und Zielscheibe
    s += f'<polygon points="150,86 230,38 236,48 158,96" fill="{SAND}"/>'
    cx, cy = 252, 34
    s += f'<circle cx="{cx}" cy="{cy}" r="30" fill="{SAGE}"/><circle cx="{cx}" cy="{cy}" r="22" fill="{WHITE}"/><circle cx="{cx}" cy="{cy}" r="14" fill="{NAVY}"/><circle cx="{cx}" cy="{cy}" r="6" fill="{ORANGE}"/>'
    s += f'<line x1="{cx+2}" y1="{cy-2}" x2="{cx+32}" y2="{cy-34}" stroke="{ORANGE_D}" stroke-width="3" stroke-linecap="round"/><polygon points="{cx+24},{cy-38} {cx+40},{cy-42} {cx+36},{cy-26}" fill="{ORANGE}"/>'
    # weißer Pfeil (Impuls) aus dem Gehirn nach rechts unten in den Block
    s += f'<path d="M118 100 L160 112 L196 148" fill="none" stroke="{WHITE}" stroke-width="7" stroke-linejoin="round"/>'
    s += f'<polygon points="186,146 206,160 196,136" fill="{WHITE}"/>'
    # bröckelnder Block (isometrisch): Deckel Sand, links Navy, rechts Slate
    s += f'<polygon points="214,122 262,108 294,124 246,140" fill="{SAND}"/>'
    s += f'<polygon points="214,122 246,140 246,206 214,190" fill="{NAVY}"/>'
    s += f'<polygon points="246,140 294,124 294,190 246,206" fill="{SLATE}"/>'
    # Risse (weiß) und Bruchstück
    s += f'<path d="M222 126 l8 14 l-6 10 l12 14 l-8 10 l10 14 l-6 10" fill="none" stroke="{WHITE}" stroke-width="2.6" stroke-linejoin="round"/>'
    s += f'<path d="M232 150 l-10 6 M236 164 l-12 2" stroke="{WHITE}" stroke-width="2"/>'
    s += f'<path d="M270 136 l-4 14 l10 10 l-8 12 l8 10 l-6 12" fill="none" stroke="{WHITE}" stroke-width="2.4" stroke-linejoin="round"/>'
    s += f'<polygon points="196,172 212,166 214,182 198,188" fill="{NAVY}"/><polygon points="206,194 218,190 220,202 208,206" fill="{SLATE}"/>'
    # Klemmbrett
    s += f'<rect x="6" y="118" width="62" height="78" rx="5" fill="{SAGE}"/><rect x="12" y="130" width="50" height="60" rx="2" fill="{WHITE}"/><rect x="24" y="112" width="26" height="12" rx="3" fill="{NAVY}"/>'
    for i, yy in enumerate((140, 156, 172)):
        s += f'<rect x="17" y="{yy}" width="10" height="10" fill="{NAVY if i<2 else GREY_L}"/>'
        if i < 2: s += f'<path d="M19 {yy+5} l3 3 l5 -6" fill="none" stroke="{WHITE}" stroke-width="1.8"/>'
        s += f'<rect x="31" y="{yy+3}" width="26" height="4" fill="{GREY_L}"/>'
    # Stoppuhr (unten mittig)
    cx, cy = 98, 184
    s += f'<rect x="{cx-6}" y="{cy-42}" width="12" height="9" fill="{NAVY}"/><line x1="{cx+16}" y1="{cy-30}" x2="{cx+22}" y2="{cy-36}" stroke="{NAVY}" stroke-width="4" stroke-linecap="round"/>'
    s += f'<circle cx="{cx}" cy="{cy}" r="32" fill="{NAVY}"/><circle cx="{cx}" cy="{cy}" r="25" fill="{WHITE}"/>'
    s += f'<path d="M{cx} {cy} L{cx} {cy-25} A25 25 0 0 1 {cx+21.7} {cy-12.5} Z" fill="{SAND}"/>'
    s += f'<line x1="{cx}" y1="{cy}" x2="{cx+14}" y2="{cy-16}" stroke="{ORANGE}" stroke-width="3" stroke-linecap="round"/><circle cx="{cx}" cy="{cy}" r="3" fill="{NAVY}"/>'
    s += '</svg>'
    return s

# ---------- Illustration 2: Knäuel + Scherben ----------
def illu_tangle():
    rnd = random.Random(7)
    s = '<svg class="abs" style="left:42px;top:752px" width="320" height="150" viewBox="0 0 320 150">'
    cx, cy, R, r0 = 76, 75, 72, 30
    cols = [NAVY, ORANGE, TEAL, BEIGE, SAGE, NAVY2, ORANGE_D, SAND]
    s += f'<circle cx="{cx}" cy="{cy}" r="26" fill="{ORANGE}"/>'
    for i in range(34):
        a = math.pi*2*i/34 + rnd.uniform(-0.05, 0.05)
        rr = r0 + rnd.uniform(-6, 10)
        tx, ty = cx + rr*math.cos(a), cy + rr*math.sin(a)
        dx, dy = -math.sin(a), math.cos(a)
        L = math.sqrt(max(0, R*R - rr*rr))
        x1, y1 = tx - dx*L, ty - dy*L; x2, y2 = tx + dx*L, ty + dy*L
        s += f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{cols[i % len(cols)]}" stroke-width="2.2" stroke-linecap="round"/>'
    # Scherben
    cx2, cy2 = 232, 75
    shard_cols = [SLATE_L, SLATE, GREY, TAUPE, SLATE_L, GREY_L, NAVY, SLATE]
    for i in range(46):
        a = rnd.uniform(0, math.pi*2); d = 70*math.sqrt(rnd.random())
        px, py = cx2 + d*math.cos(a), cy2 + d*math.sin(a)
        size = rnd.uniform(5, 14) * (1.1 - d/110)
        n = rnd.choice([3, 3, 4, 4, 5, 6])
        pts = []
        rot = rnd.uniform(0, 6.3)
        for k in range(n):
            ang = rot + math.pi*2*k/n + rnd.uniform(-0.3, 0.3)
            rr = size*rnd.uniform(0.6, 1.0)
            pts.append(f"{px+rr*math.cos(ang):.1f},{py+rr*math.sin(ang):.1f}")
        col = shard_cols[i % len(shard_cols)]
        if n == 6:  # Wölkchen
            s += f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{size*0.7:.1f}" fill="{col}"/><circle cx="{px+size*0.6:.1f}" cy="{py+size*0.3:.1f}" r="{size*0.55:.1f}" fill="{col}"/>'
        else:
            s += f'<polygon points="{" ".join(pts)}" fill="{col}"/>'
    s += '</svg>'
    return s

# ---------- Illustration 3: Sanduhr-Komposition ----------
def illu_hourglass(x0, y0):
    s = f'<svg class="abs" style="left:{x0}px;top:{y0}px" width="296" height="122" viewBox="0 0 330 136">'
    # gelbes Dreieck hinten links
    s += f'<polygon points="4,8 118,68 4,128" fill="{SAND}"/>'
    # Aufziehschlüssel
    s += f'<circle cx="34" cy="52" r="13" fill="{NAVY}"/><circle cx="34" cy="84" r="13" fill="{NAVY}"/><rect x="28" y="52" width="12" height="32" fill="{NAVY}"/><rect x="40" y="62" width="40" height="12" fill="{NAVY}"/>'
    s += f'<circle cx="34" cy="52" r="5" fill="{SAND}"/><circle cx="34" cy="84" r="5" fill="{SAND}"/>'
    # Sanduhr
    hx = 150
    s += f'<rect x="{hx-42}" y="6" width="84" height="9" fill="{NAVY}"/><rect x="{hx-42}" y="121" width="84" height="9" fill="{NAVY}"/>'
    s += f'<path d="M{hx-34} 15 H{hx+34} C{hx+34} 48 {hx+6} 60 {hx+6} 68 C{hx+6} 76 {hx+34} 88 {hx+34} 121 H{hx-34} C{hx-34} 88 {hx-6} 76 {hx-6} 68 C{hx-6} 60 {hx-34} 48 {hx-34} 15Z" fill="{SLATE}"/>'
    s += f'<path d="M{hx-34} 15 H{hx} V121 H{hx-34} C{hx-34} 88 {hx-6} 76 {hx-6} 68 C{hx-6} 60 {hx-34} 48 {hx-34} 15Z" fill="{SLATE_L}"/>'
    # Sand oben (orange, rechts) und unten (Haufen)
    s += f'<path d="M{hx-16} 40 H{hx+30} C{hx+26} 54 {hx+8} 60 {hx+4} 68 L{hx-2} 68 C{hx-2} 60 {hx-14} 50 {hx-16} 40Z" fill="{ORANGE}"/>'
    s += f'<path d="M{hx-30} 121 C{hx-24} 100 {hx-8} 96 {hx} 92 C{hx+8} 96 {hx+24} 100 {hx+30} 121Z" fill="{ORANGE}"/><rect x="{hx-1.2}" y="68" width="2.4" height="26" fill="{ORANGE}"/>'
    # Basis grau
    s += f'<polygon points="{hx-70},136 {hx-46},118 {hx+46},118 {hx+70},136" fill="{GREY_L}"/>'
    # grüner Winkel
    s += f'<polygon points="206,14 226,14 258,68 226,122 206,122 238,68" fill="{SAGE}"/>'
    # orangefarbener Ball + Bewegungsstriche
    s += f'<circle cx="252" cy="78" r="18" fill="{ORANGE}"/><circle cx="246" cy="72" r="5" fill="{ORANGE_D}" opacity=".5"/>'
    s += f'<g stroke="{GREY}" stroke-width="2" stroke-linecap="round"><line x1="236" y1="28" x2="246" y2="40"/><line x1="226" y1="40" x2="236" y2="48"/><line x1="236" y1="128" x2="246" y2="116"/><line x1="226" y1="116" x2="236" y2="108"/></g>'
    # Stoppuhr-Zielscheibe
    cx, cy = 294, 70
    s += f'<rect x="{cx-5}" y="{cy-44}" width="10" height="8" fill="{SAGE}"/>'
    s += f'<circle cx="{cx}" cy="{cy}" r="34" fill="{NAVY}"/><circle cx="{cx}" cy="{cy}" r="26" fill="{WHITE}"/><circle cx="{cx}" cy="{cy}" r="18" fill="{SLATE}"/><circle cx="{cx}" cy="{cy}" r="10" fill="{WHITE}"/><circle cx="{cx}" cy="{cy}" r="5" fill="{ORANGE}"/>'
    s += f'<line x1="{cx}" y1="{cy}" x2="{cx+28}" y2="{cy-36}" stroke="{ORANGE_D}" stroke-width="3" stroke-linecap="round"/><polygon points="{cx+20},{cy-40} {cx+34},{cy-44} {cx+32},{cy-30}" fill="{SAGE_D}"/>'
    s += '</svg>'
    return s

# ---------- Illustration 3b: Deadline-Falle (kompakter Kreislauf) ----------
def illu_cycle(x0, y0):
    W, H = 330, 74
    s = f'<svg class="abs" style="left:{x0}px;top:{y0}px" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
    ph = 20; yt = 6; yb = 48
    def pill(x, y, w, label, fill, fg):
        return f'<rect x="{x}" y="{y}" width="{w}" height="{ph}" rx="3" fill="{fill}"/>' + text(x+w/2, y+14, label, 10.5, 700, fg, "middle")
    s += pill(30, yt, 100, "Aufschieben", NAVY, WHITE) + pill(146, yt, 100, "Deadline naht", SAND, INK) + pill(262, yt, 62, "Stress", ORANGE, WHITE)
    s += pill(200, yb, 100, "Arbeitsphase", NAVY2, WHITE) + pill(70, yb, 110, "Erleichterung", SAGE, WHITE)
    s += arrow(131, 16, 145, 16, LINE_D, 1.4, 6) + arrow(247, 16, 261, 16, LINE_D, 1.4, 6)
    s += f'<path d="M324 16 H336 V58 H310" fill="none" stroke="{LINE_D}" stroke-width="1.4"/>' + arrow(312, 58, 301, 58, LINE_D, 1.4, 6)
    s += arrow(199, 58, 181, 58, LINE_D, 1.4, 6)
    s += f'<path d="M70 58 H16 V16 H22" fill="none" stroke="{LINE_D}" stroke-width="1.4"/>' + arrow(20, 16, 29, 16, LINE_D, 1.4, 6)
    s += text(24, 40, "wieder von vorn", 9.5, 400, ORANGE_D, "start", upper=False, extra='font-style="italic"')
    s += '</svg>'
    return s

# ---------- Illustration 4: Schaltkreis-Gehirn (Steuerzentrale) ----------
def illu_circuit(x0, y0):
    s = f'<svg class="abs" style="left:{x0}px;top:{y0}px" width="300" height="236" viewBox="0 0 300 236">'
    cx, cy = 74, 112
    k = 0.88
    # zwei Hemisphären aus Kreisbuckeln (Salbei)
    bumps = []
    for side in (-1, 1):
        for (bx, by, r) in [(26, 0, 44), (40, -46, 36), (18, -74, 30), (46, 36, 36), (20, 70, 30), (52, -14, 30), (54, 16, 28)]:
            bumps.append((cx + side*bx*k, cy + by*k, r*k))
    for bx, by, r in bumps:
        s += f'<circle cx="{bx}" cy="{by}" r="{r}" fill="{SAGE}"/>'
    # Mittelfurche
    s += f'<rect x="{cx-2}" y="{cy-92}" width="4" height="184" fill="{BG}"/>'
    # Innenflächen Navy
    for side in (-1, 1):
        s += f'<path d="M{cx+side*8} {cy-70} C{cx+side*46} {cy-68} {cx+side*60} {cy-36} {cx+side*56} {cy-6} C{cx+side*62} {cy+26} {cx+side*40} {cy+62} {cx+side*8} {cy+64} Z" fill="{NAVY}"/>'
    # Leiterbahnen (Sand) mit Knotenpunkten
    paths = [f"M{cx-10} {cy-54} h-18 v22 h-14", f"M{cx-10} {cy-18} h-26 v18 h-8", f"M{cx-10} {cy+28} h-16 v20 h-12",
             f"M{cx+10} {cy-62} h20 v16 h18", f"M{cx+10} {cy-6} h26 v-24 h10", f"M{cx+10} {cy+36} h18 v-12 h20"]
    s += f'<g fill="none" stroke="{SAND}" stroke-width="2.4" stroke-linejoin="round" stroke-linecap="round">' + "".join(f'<path d="{d}"/>' for d in paths) + '</g>'
    for (px, py) in [(cx-42, cy-32), (cx-44, cy), (cx-38, cy+48), (cx+48, cy-46), (cx+46, cy-30), (cx+48, cy+24)]:
        s += f'<circle cx="{px}" cy="{py}" r="3.4" fill="{SAND}"/>'
    # Zahnräder
    s += gear(cx-28, cy+6, 18, 9, SAND) + gear(cx+30, cy-40, 14, 8, SAND) + gear(cx-34, cy+50, 9, 7, SAND_L)
    # Tortenkreis (Impuls) und Quadrat (Plan)
    s += f'<circle cx="{cx+38}" cy="{cy+2}" r="13" fill="{WHITE}"/><path d="M{cx+38} {cy+2} L{cx+38} {cy-11} A13 13 0 0 1 {cx+50.5} {cy+6} Z" fill="{ORANGE}"/><path d="M{cx+38} {cy+2} L{cx+50.5} {cy+6} A13 13 0 0 1 {cx+27} {cy+9} Z" fill="{NAVY2}"/>'
    s += f'<rect x="{cx+20}" y="{cy+30}" width="28" height="24" rx="2" fill="{SLATE}"/><polyline points="{cx+24},{cy+50} {cx+31},{cy+39} {cx+38},{cy+45} {cx+44},{cy+34}" fill="none" stroke="{SAND}" stroke-width="2"/>'
    # Blitze (orange)
    s += f'<polygon points="{cx+60},{cy-88} {cx+52},{cy-70} {cx+60},{cy-72} {cx+50},{cy-52} {cx+66},{cy-76} {cx+58},{cy-74}" fill="{ORANGE}"/>'
    s += f'<polygon points="{cx+66},{cy+50} {cx+56},{cy+70} {cx+64},{cy+68} {cx+54},{cy+88} {cx+72},{cy+62} {cx+64},{cy+64}" fill="{ORANGE}"/>'
    # Pfeile nach rechts zu den fünf Aufgaben
    ix = 180  # Icon-Spalte
    rows = [("Planen", 24), ("Arbeits-|gedächtnis", 70), ("Ablenkung|ausblenden", 116), ("Impulse|bremsen", 162), ("Langfristige|Ziele", 208)]
    starts = [(cx+54, cy-62), (cx+56, cy-26), (cx+62, cy+2), (cx+56, cy+32), (cx+44, cy+68)]
    for (lab, ry), (sx, sy) in zip(rows, starts):
        mid = ix - 22
        s += f'<path d="M{sx} {sy} H{mid-8} L{mid} {ry} H{ix-12}" fill="none" stroke="{LINE_D}" stroke-width="1.3"/>' + arrow(ix-14, ry, ix-6, ry, LINE_D, 1.3, 6)
    # Icons (flach) 28x28 bei (ix, ry-14)
    def icon(kind, x, y):
        if kind == "Planen":   # Karte
            return (f'<polygon points="{x},{y+4} {x+10},{y} {x+19},{y+4} {x+28},{y} {x+28},{y+24} {x+19},{y+28} {x+10},{y+24} {x},{y+28}" fill="{SLATE}"/>'
                    f'<polygon points="{x+10},{y} {x+19},{y+4} {x+19},{y+28} {x+10},{y+24}" fill="{SLATE_L}"/>'
                    f'<path d="M{x+4} {y+20} C{x+10} {y+8} {x+18} {y+20} {x+24} {y+8}" fill="none" stroke="{WHITE}" stroke-width="1.6" stroke-dasharray="3 2"/><circle cx="{x+24}" cy="{y+8}" r="3" fill="{ORANGE}"/>')
        if kind.startswith("Arbeits"):  # Ordner
            return (f'<path d="M{x} {y+6} h10 l3 3 h15 v19 h-28z" fill="{NAVY}"/><rect x="{x}" y="{y+12}" width="28" height="16" fill="{SAND}"/>')
        if kind.startswith("Ablenkung"):  # Trichter
            return (f'<polygon points="{x},{y+2} {x+28},{y+2} {x+17},{y+15} {x+17},{y+27} {x+11},{y+24} {x+11},{y+15}" fill="{TEAL}"/>'
                    f'<g fill="{GREY}"><circle cx="{x+6}" cy="{y-3}" r="2.2"/><circle cx="{x+14}" cy="{y-5}" r="2.2"/><circle cx="{x+22}" cy="{y-3}" r="2.2"/></g>')
        if kind.startswith("Impulse"):  # Stoppschild
            return (f'<polygon points="{x+8},{y} {x+20},{y} {x+28},{y+8} {x+28},{y+20} {x+20},{y+28} {x+8},{y+28} {x},{y+20} {x},{y+8}" fill="{ORANGE}"/><rect x="{x+6}" y="{y+11.5}" width="16" height="5" fill="{WHITE}"/>')
        # Fahne / Ziel
        return (f'<rect x="{x+3}" y="{y}" width="3" height="28" fill="{NAVY}"/><polygon points="{x+6},{y+1} {x+27},{y+1} {x+22},{y+8} {x+27},{y+15} {x+6},{y+15}" fill="{SAND}"/><rect x="{x}" y="{y+26}" width="14" height="2.5" fill="{NAVY}"/>')
    for lab, ry in rows:
        s += icon(lab.split("|")[0], ix, ry-14)
        parts = lab.split("|")
        lx = ix + 36
        if len(parts) == 1:
            s += text(lx, ry+4, parts[0], 11.5, 700)
        else:
            s += text(lx, ry-1, parts[0], 11.5, 700) + text(lx, ry+12, parts[1], 11.5, 700)
    s += '</svg>'
    return s

# ---------- Illustration 5: Synapse ----------
def illu_synapse(x0, y0):
    W, H = 306, 196
    s = f'<svg class="abs" style="left:{x0}px;top:{y0}px" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
    cy = 100
    # Präsynapse (Navy)
    s += (f'<path d="M0 {cy-20} H46 C62 {cy-20} 70 {cy-62} 110 {cy-66} C150 {cy-70} 176 {cy-40} 176 {cy-10} '
          f'C176 {cy+6} 170 {cy+12} 170 {cy+22} C170 {cy+42} 160 {cy+66} 118 {cy+66} C74 {cy+66} 64 {cy+22} 46 {cy+20} H0 Z" fill="{NAVY}"/>')
    # Vesikel/Pfeile im Inneren (Sand)
    s += f'<circle cx="52" cy="{cy-18}" r="7" fill="{SAND}"/><circle cx="56" cy="{cy+22}" r="7" fill="{SAND}"/>'
    s += f'<g stroke="{SAND}" stroke-width="2.4" fill="none"><path d="M58 {cy-18} H80"/><path d="M62 {cy+22} H80"/><path d="M80 {cy-18} V{cy+22}"/><path d="M80 {cy} H140"/><path d="M80 {cy-18} L150 {cy-36}"/><path d="M80 {cy+22} L150 {cy+40}"/></g>'
    for (ax, ay, dx, dy) in [(140, cy, 1, 0), (150, cy-36, 1, -0.26), (150, cy+40, 1, 0.26)]:
        s += arrow(ax, ay, ax+10*dx, ay+10*dy, SAND, 2.4, 9)
    # Spaltbalken (grau)
    s += f'<rect x="186" y="{cy-72}" width="9" height="34" fill="{GREY}"/><rect x="186" y="{cy+40}" width="9" height="34" fill="{GREY}"/>'
    # Postsynapse (Slate-hell)
    s += (f'<path d="M{W} {cy-20} H262 C246 {cy-20} 240 {cy-58} 212 {cy-56} C196 {cy-54} 198 {cy-30} 206 {cy-16} C210 {cy-8} 206 {cy-2} 206 {cy+2} '
          f'C206 {cy+6} 210 {cy+12} 206 {cy+20} C198 {cy+34} 196 {cy+58} 212 {cy+60} C240 {cy+62} 246 {cy+20} 262 {cy+20} H{W} Z" fill="{SLATE_L}"/>')
    # Rezeptoren
    s += f'<path d="M212 {cy-34} l-6 -8 l6 -2 l4 6 l6 -5 z" fill="{TEAL}"/><path d="M214 {cy+4} l-7 -6 l5 -4 l5 5 l5 -6 l3 5 z" fill="{ORANGE}"/><path d="M212 {cy+40} l-6 8 l6 2 l4 -6 l6 5 z" fill="{ORANGE_D}"/>'
    # Botenstoffe im Spalt und außen
    parts = [("c", 170, cy-52, 5, TEAL), ("t", 182, cy-30, 6, ORANGE), ("c", 194, cy-12, 5, SAND), ("c", 176, cy-8, 4, TEAL), ("t", 188, cy+8, 6, SAND),
             ("c", 172, cy+18, 5, ORANGE), ("t", 184, cy+30, 6, ORANGE_D), ("c", 196, cy+22, 4, TEAL), ("c", 200, cy-36, 4, NAVY2), ("t", 170, cy+2, 5, ORANGE),
             ("c", 150, cy-92, 8, TEAL), ("t", 176, cy-98, 9, SAND), ("c", 206, cy-94, 9, NAVY), ("t", 162, cy-80, 7, ORANGE),
             ("c", 170, cy+92, 8, TEAL), ("c", 194, cy+84, 9, ORANGE), ("t", 214, cy+96, 7, TEAL), ("t", 236, cy-84, 6, ORANGE_D)]
    for k, px, py, r, col in parts:
        if k == "c": s += f'<circle cx="{px}" cy="{py}" r="{r}" fill="{col}"/>'
        else: s += f'<polygon points="{px},{py-r} {px+r*0.9},{py+r*0.6} {px-r*0.9},{py+r*0.6}" fill="{col}"/>'
    # orangefarbene dünne Linien (wie im Original) im Spalt
    s += f'<g stroke="{ORANGE_D}" stroke-width="1.5"><line x1="150" y1="{cy-96}" x2="200" y2="{cy-56}"/><line x1="200" y1="{cy+56}" x2="150" y2="{cy+96}"/></g>'
    s += '</svg>'
    return s

# ---------- Illustration 6: Waage ----------
def illu_scale(x0, y0):
    W, H = 300, 136
    s = f'<svg class="abs" style="left:{x0}px;top:{y0}px" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
    px, py = 150, 30
    lx, ly = 50, 50; rx, ry = 250, 10
    s += f'<line x1="{lx}" y1="{ly}" x2="{rx}" y2="{ry}" stroke="{NAVY}" stroke-width="5" stroke-linecap="round"/>'
    s += f'<circle cx="{px}" cy="{py}" r="7" fill="{NAVY}"/><circle cx="{px}" cy="{py}" r="3" fill="{SLATE_L}"/>'
    s += f'<rect x="{px-4}" y="{py}" width="8" height="82" fill="{NAVY}"/><path d="M{px-18} 126 V116 a18 12 0 0 1 36 0 V126Z" fill="{SAGE}"/><path d="M{px-18} 126 V116 a18 12 0 0 1 18 -12 V126Z" fill="{ORANGE}"/>'
    s += f'<rect x="{px-46}" y="124" width="92" height="8" rx="3" fill="{NAVY}"/>'
    s += text(px, 22, "≠", 16, 700, ORANGE_D, "middle", upper=False)
    # linke Schale (unten, schwer): Stapel „Wissen“
    s += f'<g stroke="{NAVY}" stroke-width="1.6" fill="none"><line x1="{lx}" y1="{ly}" x2="{lx-30}" y2="{ly+40}"/><line x1="{lx}" y1="{ly}" x2="{lx+30}" y2="{ly+40}"/></g>'
    s += f'<rect x="{lx-22}" y="{ly+6}" width="44" height="34" fill="{TAUPE}"/><g fill="{WHITE}"><rect x="{lx-14}" y="{ly+13}" width="28" height="3"/><rect x="{lx-14}" y="{ly+20}" width="28" height="3"/><rect x="{lx-14}" y="{ly+27}" width="18" height="3"/></g>'
    s += f'<path d="M{lx-34} {ly+40} H{lx+34} a34 10 0 0 1 -68 0Z" fill="{NAVY}"/>'
    # rechte Schale (oben, leicht, „leuchtend“): Würfel
    s += f'<g stroke="{NAVY}" stroke-width="1.6" fill="none"><line x1="{rx}" y1="{ry}" x2="{rx-28}" y2="{ry+48}"/><line x1="{rx}" y1="{ry}" x2="{rx+28}" y2="{ry+48}"/></g>'
    s += f'<polygon points="{rx-14},{ry+20} {rx},{ry+12} {rx+14},{ry+20} {rx},{ry+28}" fill="{SAND_L}"/><polygon points="{rx-14},{ry+20} {rx},{ry+28} {rx},{ry+48} {rx-14},{ry+40}" fill="{SAND}"/><polygon points="{rx},{ry+28} {rx+14},{ry+20} {rx+14},{ry+40} {rx},{ry+48}" fill="{OCHRE}"/>'
    s += f'<path d="M{rx-32} {ry+48} H{rx+32} a32 10 0 0 1 -64 0Z" fill="{NAVY}"/>'
    s += f'<g stroke="{SAND}" stroke-width="2" stroke-linecap="round"><line x1="{rx-32}" y1="{ry+14}" x2="{rx-25}" y2="{ry+18}"/><line x1="{rx-33}" y1="{ry+30}" x2="{rx-25}" y2="{ry+29}"/><line x1="{rx+32}" y1="{ry+14}" x2="{rx+25}" y2="{ry+18}"/><line x1="{rx+33}" y1="{ry+30}" x2="{rx+25}" y2="{ry+29}"/></g>'
    # Beschriftungen
    s += text(lx, ly+66, "Wichtig finden", 12, 700, INK, "middle") + text(lx, ly+80, "„Ich sollte …“", 11, 400, INK, "middle", upper=False)
    s += text(rx, ry+72, "Jetzt Motivation", 12, 700, INK, "middle") + text(rx, ry+85, "aufbringen", 12, 700, INK, "middle") + text(rx, ry+98, "„Ich mache es jetzt.“", 11, 400, INK, "middle", upper=False)
    s += '</svg>'
    return s

# ---------- Verbindungs-/Rahmenlinien ----------
def lines():
    s = '<svg class="abs" style="left:0;top:0" width="768" height="1376" viewBox="0 0 768 1376">'
    d = f'stroke="{LINE_D}" stroke-width="1.2" fill="none"'
    o = f'stroke="{OCHRE_L}" stroke-width="1.3" fill="none"'
    # Spaltenteiler
    s += f'<line x1="382" y1="214" x2="382" y2="582" {d}/>'
    s += f'<line x1="382" y1="1040" x2="382" y2="1312" {d}/>'
    # Rahmen L1 (ocker): waagerecht, diagonal, senkrecht bis zum Knoten im Gehirn
    s += f'<path d="M42 290 H282 L357 365 V612" {o}/>'
    # Rahmen R1 (dunkel)
    s += f'<path d="M726 290 H412 V581" {d}/>'
    # Linie vom Gehirnknoten nach links (= Rahmen L2)
    s += f'<line x1="272" y1="690" x2="42" y2="690" {d}/>'
    # Ocker senkrecht vom unteren Gehirnknoten, dann diagonal und waagerecht (= Rahmen L3)
    s += f'<path d="M357 760 V930 L282 1005 H42" {o}/>'
    # Rahmen R2 (dunkel): waagerecht, diagonal, senkrecht, kurz waagerecht
    s += f'<path d="M726 774 H526 L412 888 V1092 H726" {d}/>'
    # verlängerte Facettenkanten aus dem Gehirn
    s += f'<line x1="318" y1="700" x2="536" y2="874" stroke="{ORANGE_D}" stroke-width="1.4"/>'
    s += f'<line x1="300" y1="612" x2="470" y2="664" stroke="{NAVY}" stroke-width="1.1"/>'
    s += f'<line x1="430" y1="600" x2="556" y2="768" stroke="{SAGE_D}" stroke-width="1.1"/>'
    s += f'<line x1="400" y1="560" x2="400" y2="760" stroke="{NAVY}" stroke-width="1.0"/>'
    # Knotenpunkte
    for (x, y, c) in [(357, 612, OCHRE_L), (357, 760, OCHRE_L), (272, 690, LINE_D)]:
        s += f'<circle cx="{x}" cy="{y}" r="4.5" fill="{c}"/>'
    # Fazit-Linie
    s += f'<line x1="42" y1="1324" x2="726" y2="1324" {d}/>'
    s += '</svg>'
    return s

# ---------- Kleine Icons für Beschriftungen ----------
def icon_lens(x, y):
    return (f'<svg class="abs" style="left:{x}px;top:{y}px" width="26" height="26" viewBox="0 0 26 26"><circle cx="13" cy="13" r="13" fill="{ORANGE}"/>'
            f'<circle cx="11" cy="11" r="5" fill="none" stroke="{WHITE}" stroke-width="2.2"/><line x1="14.5" y1="14.5" x2="19.5" y2="19.5" stroke="{WHITE}" stroke-width="2.6" stroke-linecap="round"/></svg>')
def icon_wall(x, y):
    s = f'<svg class="abs" style="left:{x}px;top:{y}px" width="26" height="26" viewBox="0 0 26 26"><rect width="26" height="26" rx="3" fill="{SLATE}"/>'
    for i, yy in enumerate((6, 11, 16)):
        off = 0 if i % 2 == 0 else 4
        for xx in range(-4+off, 26, 8):
            s += f'<rect x="{max(xx,4)}" y="{yy}" width="{min(xx+6,22)-max(xx,4)}" height="3" fill="{WHITE}"/>'
    return s + '</svg>'

# ---------- HTML ----------
CSS = f"""
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:768px;height:1376px;overflow:hidden;background:{BG}}}
body{{position:relative;font-family:'Roboto Condensed',sans-serif;color:{INK};background:{BG}}}
.abs{{position:absolute;display:block}}
h1{{position:absolute;left:42px;top:40px;width:690px;font:700 37.5px/40px 'Roboto';letter-spacing:-.012em;color:{INK}}}
.intro{{position:absolute;left:42px;top:130px;width:684px;font:400 18px/19.5px 'Roboto Condensed'}}
.col{{position:absolute;top:214px;font:700 28px/28.5px 'Roboto Condensed';text-transform:uppercase;letter-spacing:-.005em}}
.sub{{position:absolute;font:700 20px/20.5px 'Roboto Condensed';text-transform:uppercase;letter-spacing:-.005em}}
.sub.sm{{font-size:19px;line-height:19.5px}}
.tx{{position:absolute;font:400 15px/17px 'Roboto Condensed'}}
.r{{text-align:right}}
.lab{{position:absolute;font:700 13px/14px 'Roboto Condensed';text-transform:uppercase}}
.fazit{{position:absolute;left:42px;top:1331px;width:684px;font:400 13px/15px 'Roboto Condensed';white-space:nowrap}}
.fazit b{{font-weight:700}}
.quelle{{position:absolute;left:42px;top:1352px;width:684px;font:400 11px/12px 'Roboto Condensed';color:#5b6470}}
"""

def html():
    parts = []
    parts.append(f"<!doctype html>\n<html lang=\"de\"><head><meta charset=\"utf-8\"><title>ADHS im Gehirn</title>"
                 f"<link rel=\"stylesheet\" href=\"../assets/fonts.css\"><style>{CSS}</style></head><body>")
    parts.append('<h1>ADHS im Gehirn: Kein Willensproblem,<br>sondern ein Steuerungsproblem</h1>')
    parts.append('<p class="intro">ADHS bedeutet nicht faul, undiszipliniert oder „ist mir egal“. Es handelt sich um eine neuroentwicklungsbedingte Störung der Selbststeuerung, bei der Botenstoffe wie Dopamin anders wirken: dasselbe Gehirn, andere Aktivierung.</p>')
    parts.append('<div class="col" style="left:42px">Mythos vs.<br>Alltagserleben</div>')
    parts.append('<div class="col" style="left:412px">Die neurobiologische<br>Realität</div>')

    # ---- linke Spalte ----
    parts.append('<div class="sub" style="left:42px;top:300px">Kein Mangel an Wille<br>oder Disziplin</div>')
    parts.append(illu_paradox())
    parts.append('<p class="tx" style="left:42px;top:578px;width:200px">Das Paradox: Die wichtige E-Mail (5 Minuten Arbeit) bleibt eine Stunde liegen – beim Lieblingsthema: stundenlanger Hyperfokus.</p>')

    parts.append('<div class="sub" style="left:42px;top:702px">Hyperfokus ist<br>kein Widerspruch</div>')
    parts.append(illu_tangle())
    parts.append(icon_lens(52, 910) + '<div class="lab" style="left:86px;top:916px">Hyperfokus</div>')
    parts.append(icon_wall(214, 910) + '<div class="lab" style="left:248px;top:909px">Plötzliche<br>Blockade</div>')
    parts.append('<p class="tx" style="left:42px;top:946px;width:300px">Aufmerksamkeit haben: ja. Aufmerksamkeit steuern: schwierig – wann beginnen, worauf richten, was ausblenden, wann wieder lösen?</p>')

    parts.append('<div class="sub" style="left:42px;top:1016px">Produktivität<br>unter Zeitdruck</div>')
    parts.append(illu_hourglass(42, 1062))
    parts.append('<div class="lab" style="left:42px;top:1186px;font-size:11px;color:#5b6470">Die Deadline-Falle</div>')
    parts.append(illu_cycle(42, 1198))
    parts.append('<p class="tx" style="left:42px;top:1278px;width:320px">Neuheit, unmittelbare Konsequenzen, persönliches Interesse und Zeitdruck schalten die Aktivierung ein.</p>')

    # ---- rechte Spalte ----
    parts.append('<div class="sub" style="left:426px;top:300px">Die Steuerzentrale<br>arbeitet weniger stabil</div>')
    parts.append(illu_circuit(426, 350))
    parts.append('<p class="tx r" style="left:540px;top:596px;width:186px">Der präfrontale Cortex übernimmt fünf Aufgaben – bei reizarmen Aufgaben weniger stabil.</p>')

    parts.append('<div class="sub r sm" style="left:430px;top:784px;width:296px">Der Bewerter: Dopamin<br>&amp; Noradrenalin</div>')
    parts.append(illu_synapse(420, 832))
    parts.append('<p class="tx" style="left:432px;top:1030px;width:294px">Fragt ständig: „Lohnt sich das jetzt?“ Nicht einfach „zu wenig Dopamin“, sondern veränderte Signalwege.</p>')

    parts.append('<div class="sub" style="left:432px;top:1102px">Die Lücke zwischen<br>Wissen und Tun</div>')
    parts.append(illu_scale(426, 1142))
    parts.append('<p class="tx" style="left:432px;top:1282px;width:294px">Ich weiß es und schaffe es trotzdem nicht anzufangen.</p>')

    # ---- Gehirn (zuletzt, liegt vorn) ----
    parts.append(big_brain(240, 566))
    parts.append(lines())

    # ---- Fazit und Quelle ----
    parts.append('<p class="fazit"><b>Fazit:</b> ADHS heißt nicht „keine Aufmerksamkeit“ – Aufmerksamkeit, Motivation und Verhalten zuverlässig anzupassen, fällt schwer.</p>')
    parts.append('<p class="quelle">Quelle: NeuroWissen TV, „NEUROLOGE ERKLÄRT: Das macht ADHS wirklich in deinem Gehirn“ (2026)</p>')
    parts.append('</body></html>')
    return "\n".join(parts)

if __name__ == "__main__":
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(html())
    print("geschrieben:", OUT)
