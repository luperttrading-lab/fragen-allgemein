#!/usr/bin/env python3
# Erzeugt v2.html (Stil "Scientific", Poster mit einem Hero-Gehirn in Aufsicht, Vorbild NotebookLM).
import math, random, os
HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 768, 1376
rng = random.Random(11)

# ---------------- Geometrie ----------------
def cr_path(pts, closed=False):
    """Catmull-Rom-Spline als kubischer Bezier-Pfad."""
    if closed:
        P = [pts[-1]] + list(pts) + [pts[0], pts[1]]
    else:
        P = [pts[0]] + list(pts) + [pts[-1]]
    d = f"M{P[1][0]:.1f},{P[1][1]:.1f}"
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i-1], P[i], P[i+1], P[i+2]
        c1 = (p1[0] + (p2[0]-p0[0])/6, p1[1] + (p2[1]-p0[1])/6)
        c2 = (p2[0] - (p3[0]-p1[0])/6, p2[1] - (p3[1]-p1[1])/6)
        d += f" C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}"
    return d + (" Z" if closed else "")

def cr_sample(pts, closed=False, n=12):
    """Dichte Punktfolge entlang des Catmull-Rom-Splines."""
    if closed:
        P = [pts[-1]] + list(pts) + [pts[0], pts[1]]
    else:
        P = [pts[0]] + list(pts) + [pts[-1]]
    out = []
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i-1], P[i], P[i+1], P[i+2]
        c1 = (p1[0] + (p2[0]-p0[0])/6, p1[1] + (p2[1]-p0[1])/6)
        c2 = (p2[0] - (p3[0]-p1[0])/6, p2[1] - (p3[1]-p1[1])/6)
        for k in range(n):
            t = k / n; u = 1 - t
            out.append((u**3*p1[0] + 3*u*u*t*c1[0] + 3*u*t*t*c2[0] + t**3*p2[0],
                        u**3*p1[1] + 3*u*u*t*c1[1] + 3*u*t*t*c2[1] + t**3*p2[1]))
    if not closed:
        out.append(P[-2])
    return out

def hexagon(cx, cy, r, fill, stroke, sw=2, rot=0):
    pts = [(cx + r*math.cos(math.radians(a + rot)), cy + r*math.sin(math.radians(a + rot))) for a in range(30, 390, 60)]
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + " Z"
    return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"/>'

def ekg(x, y, w, h, color, sw=2):
    rel = [(0,0),(0.22,0),(0.28,-0.2),(0.33,0.15),(0.38,-0.95),(0.44,0.75),(0.49,-0.1),(0.55,0),(0.62,-0.25),(0.68,0),(1,0)]
    pts = [(x + a*w, y + b*h) for a, b in rel]
    d = "M" + " L".join(f"{px:.1f},{py:.1f}" for px, py in pts)
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round"/>'

# ---------------- Hemisphären ----------------
# Linke Hemisphäre (Seitenkoordinaten), im Uhrzeigersinn ab oben-medial
LEFT_BASE = [(370,408),(352,390),(322,382),(288,386),(256,402),(230,434),(208,482),(190,538),(172,604),
             (157,670),(151,740),(154,806),(166,866),(190,922),(224,962),(266,984),(310,990),(347,980),
             (367,956),(374,926),(375,860),(372,790),(373,720),(375,650),(373,580),(374,510),(372,450)]
LEFT_MED = 376

def mirror_right(pts):
    out = []
    for x, y in pts:
        xm = 762 - x
        out.append((384 + (xm - 384)*0.95, y - 2))
    return out
RIGHT_BASE = mirror_right(LEFT_BASE)
RIGHT_MED = 384

def bumpy_outline(base, medial_x, side, amp=5.5, lam=26.0):
    """Dichte Kontur mit Windungsbuckeln (nicht an der Längsfurche)."""
    dense = cr_sample(base, closed=True, n=16)
    n = len(dense)
    cx = sum(p[0] for p in dense)/n; cy = sum(p[1] for p in dense)/n
    # Bogenlänge
    s = [0.0]
    for i in range(1, n):
        s.append(s[-1] + math.hypot(dense[i][0]-dense[i-1][0], dense[i][1]-dense[i-1][1]))
    L = s[-1] + math.hypot(dense[0][0]-dense[-1][0], dense[0][1]-dense[-1][1])
    k = max(8, round(L / lam)); lam2 = L / k
    out = []
    for i in range(n):
        x, y = dense[i]
        xp, yp = dense[i-1]; xn, yn = dense[(i+1) % n]
        tx, ty = xn-xp, yn-yp; tl = math.hypot(tx, ty) or 1
        nx, ny = -ty/tl, tx/tl
        if (x-cx)*nx + (y-cy)*ny < 0: nx, ny = -nx, -ny
        dist_med = (medial_x - x) if side == 'L' else (x - medial_x)
        m = 0.45 + 0.55*min(1, max(0, (dist_med - 9) / 16))
        ph = math.pi * s[i] / lam2
        bi = int(s[i] / lam2)
        fac = 0.65 + 0.7 * random.Random(bi * 7919 + (1 if side == 'L' else 2)).random()
        delta = amp * fac * (abs(math.sin(ph)) ** 0.85) - 0.32*amp
        out.append((x + nx*delta*m, y + ny*delta*m))
    # auf ~5 px Abstand neu abtasten
    res = [out[0]]; acc = 0
    for i in range(1, n):
        acc += math.hypot(out[i][0]-out[i-1][0], out[i][1]-out[i-1][1])
        if acc >= 4.5:
            res.append(out[i]); acc = 0
    return res, dense

def lateral_fn(dense, side):
    ys = {}
    for x, y in dense:
        yi = int(round(y))
        for yy in (yi-1, yi, yi+1):
            if side == 'L':
                ys[yy] = min(ys.get(yy, 1e9), x)
            else:
                ys[yy] = max(ys.get(yy, -1e9), x)
    keys = sorted(ys)
    def f(y):
        yi = int(round(y))
        if yi in ys: return ys[yi]
        yi = min(keys, key=lambda k: abs(k - y))
        return ys[yi]
    return f, min(keys), max(keys)

def _poly_inside(poly, x, y):
    inside = False; n = len(poly); j = n - 1
    for i in range(n):
        xi, yi = poly[i]; xj, yj = poly[j]
        if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / ((yj - yi) or 1e-9) + xi:
            inside = not inside
        j = i
    return inside

class _Grid:
    def __init__(self, cell=10):
        self.cell = cell; self.d = {}
    def add(self, x, y):
        self.d.setdefault((int(x // self.cell), int(y // self.cell)), []).append((x, y))
    def near(self, x, y, dist):
        cx, cy = int(x // self.cell), int(y // self.cell); rr = int(dist // self.cell) + 1
        d2 = dist * dist
        for i in range(cx - rr, cx + rr + 1):
            for j in range(cy - rr, cy + rr + 1):
                for (px, py) in self.d.get((i, j), ()):
                    if (px - x) ** 2 + (py - y) ** 2 < d2:
                        return True
        return False
    def mind(self, x, y, dist):
        cx, cy = int(x // self.cell), int(y // self.cell); rr = int(dist // self.cell) + 1
        best = dist * dist
        for i in range(cx - rr, cx + rr + 1):
            for j in range(cy - rr, cy + rr + 1):
                for (px, py) in self.d.get((i, j), ()):
                    d2 = (px - x) ** 2 + (py - y) ** 2
                    if d2 < best: best = d2
        return math.sqrt(best)

def sulci_for(dense, side, medial_x, seed, gap=17.5, edge=11.0, step=5.0, n_seeds=150):
    """Furchen als sich nicht kreuzende, mäandernde Zufallswege innerhalb der Hemisphäre."""
    r = random.Random(seed)
    eg = _Grid(10)
    for (x, y) in dense: eg.add(x, y)
    xs = [p[0] for p in dense]; ys = [p[1] for p in dense]
    minx, maxx, miny, maxy = min(xs), max(xs), min(ys), max(ys)
    occ = _Grid(10)
    def ok(x, y, own):
        if not _poly_inside(dense, x, y): return False
        if eg.mind(x, y, edge + 1) < edge: return False
        if occ.near(x, y, gap): return False
        for (px, py) in own[:-4]:
            if (px - x) ** 2 + (py - y) ** 2 < gap * gap: return False
        return True
    def walk(x, y, ang, target, own_other):
        pts = [(x, y)]; k = r.uniform(-0.1, 0.1); L = 0
        while L < target:
            k += r.gauss(0, 0.06); k = max(-0.24, min(0.24, k))
            ang += k
            moved = False
            for dlt in (0, 0.5, -0.5, 1.0, -1.0, 1.6, -1.6):
                a2 = ang + dlt
                nx, ny = x + step * math.cos(a2), y + step * math.sin(a2)
                if ok(nx, ny, own_other + pts):
                    ang = a2; x, y = nx, ny; pts.append((x, y)); L += step; moved = True; break
            if not moved: break
        return pts
    paths = []
    for _ in range(n_seeds):
        for _t in range(60):
            x = r.uniform(minx, maxx); y = r.uniform(miny, maxy)
            if ok(x, y, []): break
        else:
            continue
        ang = r.uniform(0, 2 * math.pi)
        tgt = r.uniform(140, 420)
        pf = walk(x, y, ang, tgt * 0.5, [])
        pb = walk(x, y, ang + math.pi, tgt * 0.5, pf)
        pts = list(reversed(pb))[:-1] + pf
        if len(pts) * step < 60: continue
        paths.append(pts)
        for (px, py) in pts: occ.add(px, py)
    return paths

def hemisphere_svg(base, side, medial_x, gid, colors, seed):
    outline, dense = bumpy_outline(base, medial_x, side)
    O = cr_path(outline, closed=True)
    sul = sulci_for(dense, side, medial_x, seed)
    r = random.Random(seed + 1)
    g = [f'<clipPath id="clip{gid}"><path d="{O}"/></clipPath>']
    g.append(f'<g clip-path="url(#clip{gid})">')
    g.append(f'<path d="{O}" fill="url(#fill{gid})"/>')
    # Furchen: Lichtkamm oberhalb, Schatten, Rille, Glanzlinie
    for p in sul:
        d = cr_path(p)
        g.append(f'<path d="{d}" transform="translate(-2,-6)" fill="none" stroke="{colors["light"]}" stroke-opacity=".55" stroke-width="13" stroke-linecap="round" stroke-linejoin="round"/>')
    for p in sul:
        d = cr_path(p)
        g.append(f'<path d="{d}" transform="translate(1,3)" fill="none" stroke="{colors["shadow"]}" stroke-opacity=".64" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>')
    for p in sul:
        d = cr_path(p)
        g.append(f'<path d="{d}" fill="none" stroke="{colors["groove"]}" stroke-width="5.8" stroke-linecap="round" stroke-linejoin="round"/>')
    for p in sul:
        d = cr_path(p)
        hl = colors["hl"][0] if r.random() < 0.7 else r.choice(colors["hl"][1:])
        g.append(f'<path d="{d}" transform="translate(0,-1.6)" fill="none" stroke="{hl}" stroke-opacity=".95" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>')
    g.append(f'<path d="{O}" fill="url(#shade{gid})"/>')
    g.append(f'<path d="{O}" fill="none" stroke="{colors["rim"]}" stroke-opacity=".35" stroke-width="16"/>')
    return g, O

def wobble(base, amp=3.0, lam=17.0, seed=2):
    """Glatte Kontur mit kleiner, unregelmäßiger Randstörung ("aufgerissen")."""
    r = random.Random(seed)
    dense = cr_sample(base, closed=True, n=10)
    n = len(dense)
    cx = sum(p[0] for p in dense)/n; cy = sum(p[1] for p in dense)/n
    s = [0.0]
    for i in range(1, n):
        s.append(s[-1] + math.hypot(dense[i][0]-dense[i-1][0], dense[i][1]-dense[i-1][1]))
    L = s[-1]; k = max(6, round(L/lam)); lam2 = L/k
    out = []
    ph2 = r.uniform(0, 6.28)
    for i in range(n):
        x, y = dense[i]
        xp, yp = dense[i-1]; xn, yn = dense[(i+1) % n]
        tx, ty = xn-xp, yn-yp; tl = math.hypot(tx, ty) or 1
        nx, ny = -ty/tl, tx/tl
        if (x-cx)*nx + (y-cy)*ny < 0: nx, ny = -nx, -ny
        dlt = amp*math.sin(2*math.pi*s[i]/lam2) + 0.5*amp*math.sin(2*math.pi*s[i]/(lam2*2.7) + ph2)
        out.append((x + nx*dlt, y + ny*dlt))
    res = [out[0]]; acc = 0
    for i in range(1, n):
        acc += math.hypot(out[i][0]-out[i-1][0], out[i][1]-out[i-1][1])
        if acc >= 4:
            res.append(out[i]); acc = 0
    return res

# ---------------- Rechte Hemisphäre: Cutaway ----------------
CUT_UP = [(442,452),(486,436),(514,454),(530,498),(540,546),(537,600),(515,640),(480,656),(446,642),(424,598),(419,540),(425,490)]
CUT_LOW = [(400,706),(458,690),(528,696),(576,730),(587,800),(577,862),(551,912),(512,946),(458,954),(412,930),(398,870),(396,790)]

def cutaway_svg():
    g = []
    up = cr_path(wobble(CUT_UP, 3.2, 19, 2), closed=True); low = cr_path(wobble(CUT_LOW, 3.6, 23, 4), closed=True)
    g.append(f'<clipPath id="clipUp"><path d="{up}"/></clipPath><clipPath id="clipLow"><path d="{low}"/></clipPath>')
    # ---- oberes Fenster: Dopamin-Sechsecke, Leiterbahnen ----
    g.append(f'<path d="{up}" fill="url(#cutg)"/>')
    g.append('<g clip-path="url(#clipUp)">')
    r = random.Random(5)
    # Leiterbahnen (orange, mit Punktenden)
    traces = [[(430,620),(455,585),(470,560),(478,520)], [(520,470),(505,505),(498,540)], [(455,470),(468,500),(495,515)],
              [(470,640),(488,610),(512,590),(528,560)], [(505,620),(525,600)], [(440,560),(452,540),(470,540)]]
    for t in traces:
        d = cr_path(t)
        g.append(f'<path d="{d}" fill="none" stroke="#f6a35c" stroke-width="2" stroke-linecap="round" stroke-opacity=".95"/>')
        for (x, y) in (t[0], t[-1]):
            g.append(f'<circle cx="{x}" cy="{y}" r="3.2" fill="#ffb878"/>')
    # Punkte
    for _ in range(26):
        x = r.uniform(428, 536); y = r.uniform(445, 650)
        col = r.choice(['#5ee6dc', '#ffb070', '#ff8fd0', '#8fb8ff', '#d7f26a'])
        g.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r.uniform(1.6,3.2):.1f}" fill="{col}" fill-opacity=".9"/>')
    # gestrichelte Verbindungen (abstrakt)
    g.append('<g stroke="#9fe7ff" stroke-width="1.3" stroke-dasharray="2 4" fill="none" stroke-opacity=".8">'
             '<path d="M470,560 C490,575 500,590 512,615"/><path d="M478,520 C495,505 510,495 520,470"/><path d="M450,500 C465,520 480,540 495,545"/></g>')
    # Sechsecke
    for (x, y, rad, f, s) in [(478,520,13,'#4fd3c8','#2a6fd6'),(520,470,10,'#f7923f','#c25a12'),(512,615,13,'#ef6fb4','#a8367c'),
                               (455,585,10,'#5d8ff0','#2d4fb8'),(498,540,8,'#d7f26a','#7fa21a'),(530,560,9,'#4fd3c8','#2a6fd6')]:
        g.append(hexagon(x, y, rad, f, s, 2.2, rot=r.uniform(0, 30)))
    g.append('</g>')
    g.append(f'<path d="{up}" fill="none" stroke="#2b2466" stroke-opacity=".6" stroke-width="7"/>')
    g.append(f'<path d="{up}" fill="none" stroke="#f9b67c" stroke-width="3.2"/>')
    # ---- unteres Fenster: Platten mit EKG ----
    g.append(f'<path d="{low}" fill="url(#lowg)"/>')
    g.append('<g clip-path="url(#clipLow)">')
    # Risse
    g.append('<g stroke="#f6a35c" stroke-width="1.6" fill="none" stroke-linecap="round" stroke-opacity=".9">'
             '<path d="M405,760 L430,790 L420,830 L445,860"/><path d="M560,740 L540,780 L565,810"/><path d="M500,920 L520,900 L515,870"/>'
             '<path d="M470,700 L480,730"/><path d="M585,840 L560,870 L570,900"/></g>')
    rp = random.Random(17)
    gx = [392, 458, 524, 592]; gy = [686, 752, 818, 884, 958]
    nodes = {(i, j): (gx[i] + rp.uniform(-15, 15) + (j % 2) * 14, gy[j] + rp.uniform(-13, 13) + i * 7) for i in range(4) for j in range(5)}
    grads = ['pA', 'pB', 'pC', 'pD']; ecs = {'pA': '#f6a35c', 'pB': '#8ff1ff', 'pC': '#f6a35c', 'pD': '#ffa0d8'}
    for i in range(3):
        for j in range(4):
            q = [nodes[(i, j)], nodes[(i+1, j)], nodes[(i+1, j+1)], nodes[(i, j+1)]]
            cx = sum(p[0] for p in q)/4; cy = sum(p[1] for p in q)/4
            sh = 0.84 + 0.08 * rp.random()
            q2 = [(cx + (px-cx)*sh, cy + (py-cy)*sh) for px, py in q]
            d = "M" + " L".join(f"{px:.1f},{py:.1f}" for px, py in q2) + " Z"
            grad = grads[(i + 2*j) % 4]
            g.append(f'<path d="{d}" fill="url(#{grad})" stroke="#86e8f6" stroke-width="2.2" stroke-linejoin="round"/>')
            q3 = [(cx + (px-cx)*0.78, cy + (py-cy)*0.78) for px, py in q]
            d3 = "M" + " L".join(f"{px:.1f},{py:.1f}" for px, py in q3) + " Z"
            g.append(f'<path d="{d3}" fill="none" stroke="#ffffff" stroke-opacity=".22" stroke-width="1.2" stroke-linejoin="round"/>')
            if (i + j) % 3 != 1:
                w = (q2[1][0] - q2[0][0]) * 0.8; h = (q2[3][1] - q2[0][1]) * 0.4
                ang = math.degrees(math.atan2(q2[1][1]-q2[0][1], q2[1][0]-q2[0][0]))
                g.append(f'<g transform="translate({cx:.1f},{cy:.1f}) rotate({ang:.1f})">' + ekg(-w/2, 0, w, h, ecs[grad], 2.2) + '</g>')
    # kleine Punkte
    r2 = random.Random(9)
    for _ in range(14):
        x = r2.uniform(405, 580); y = r2.uniform(700, 945)
        g.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r2.uniform(1.5,2.6):.1f}" fill="{r2.choice(["#8ff1ff","#ffb878","#ff9fd4"])}" fill-opacity=".85"/>')
    g.append('</g>')
    g.append(f'<path d="{low}" fill="none" stroke="#1f2a66" stroke-opacity=".55" stroke-width="7"/>')
    g.append(f'<path d="{low}" fill="none" stroke="#6ad9ea" stroke-width="2.8"/>')
    # ---- Sechseck-Ketten auf der Oberfläche ----
    chains = [[(404,520),(408,598),(412,672)], [(561,560),(573,616),(557,668)]]
    for ch in chains:
        d = cr_path(ch)
        g.append(f'<path d="{d}" fill="none" stroke="#f6a35c" stroke-width="2.4" stroke-linecap="round"/>')
        for (x, y) in ch:
            g.append(f'<circle cx="{x}" cy="{y}" r="3.6" fill="#ffb878"/>')
        for i, (x, y) in enumerate(ch):
            g.append(hexagon(x, y, 9.5 if i != 1 else 11, '#4fd3c8', '#2a6fd6', 2.4, rot=15*i))
    return g

# ---------------- Synapse oben rechts ----------------
def synapse_svg():
    g = []
    # Axon (Röhre) von oben rechts, am Seitenrand x=766 geschnitten
    ax, ay = 708, 346; dx, dy = 104, -132; dl = math.hypot(dx, dy); dx, dy = dx/dl, dy/dl
    px, py = -dy, dx
    def edge_pt(off, xcut=766):
        sx, sy = ax + px*off, ay + py*off
        lam = (xcut - sx) / dx
        return (sx, sy), (xcut, sy + dy*lam)
    (a1, b1), (a2, b2) = edge_pt(23), edge_pt(-23)
    g.append(f'<path d="M{a1[0]:.1f},{a1[1]:.1f} L{b1[0]:.1f},{b1[1]:.1f} L{b2[0]:.1f},{b2[1]:.1f} L{a2[0]:.1f},{a2[1]:.1f} Z" fill="url(#axg)"/>')
    (a1, b1), (a2, b2) = edge_pt(16), edge_pt(-16)
    g.append(f'<path d="M{a1[0]:.1f},{a1[1]:.1f} L{b1[0]:.1f},{b1[1]:.1f} L{b2[0]:.1f},{b2[1]:.1f} L{a2[0]:.1f},{a2[1]:.1f} Z" fill="#b9a8f3"/>')
    for off, col in ((7, '#7fe4f0'), (-6, '#ff9ad6')):
        a1, b1 = edge_pt(off)
        g.append(f'<path d="M{a1[0]:.1f},{a1[1]:.1f} L{b1[0]:.1f},{b1[1]:.1f}" stroke="{col}" stroke-width="2.4" fill="none" stroke-opacity=".9"/>')
    # Endknöpfchen
    g.append('<g transform="translate(670,392) rotate(-38) scale(1.08)">')
    g.append('<ellipse cx="0" cy="0" rx="74" ry="54" fill="url(#bulbg)" stroke="#6fc8e8" stroke-width="3.5"/>')
    g.append('<ellipse cx="-4" cy="-8" rx="62" ry="40" fill="none" stroke="#ffffff" stroke-opacity=".35" stroke-width="3"/>')
    # Öffnung (wellige Kante links unten)
    pts = []
    for i in range(28):
        a = 2*math.pi*i/28
        rr = 1.0
        if math.cos(a) < -0.1:
            rr = 1.0 + 0.09*math.sin(a*9.0)
        pts.append((-18 + 58*rr*math.cos(a), 3 + 40*rr*math.sin(a)))
    g.append('<clipPath id="bulbclip"><ellipse cx="0" cy="0" rx="72" ry="52"/></clipPath>')
    g.append(f'<path d="{cr_path(pts, closed=True)}" clip-path="url(#bulbclip)" fill="url(#bulbin)" stroke="#5a3fae" stroke-width="2"/>')
    g.append('<path d="M-30,-8 C-18,6 -4,10 14,2" fill="none" stroke="#f6a35c" stroke-width="1.8" stroke-dasharray="2 3"/>')
    g.append('<path d="M-36,14 C-20,22 0,18 18,20" fill="none" stroke="#5ee6dc" stroke-width="1.6" stroke-dasharray="2 3"/>')
    g.append(hexagon(-28, 0, 8, '#f7923f', '#c25a12', 2, 10))
    g.append(hexagon(-2, -12, 7.5, '#4fd3c8', '#2a6fd6', 2, 0))
    g.append(hexagon(6, 14, 8.5, '#ef6fb4', '#a8367c', 2, 20))
    g.append(hexagon(24, -4, 6.5, '#5d8ff0', '#2d4fb8', 2, 0))
    for (x, y, c) in [(-40,-14,'#5ee6dc'),(-18,16,'#ffb070'),(14,-20,'#ff8fd0'),(30,12,'#d7f26a'),(-14,-2,'#8fb8ff')]:
        g.append(f'<circle cx="{x}" cy="{y}" r="2.4" fill="{c}"/>')
    g.append('</g>')
    # freigesetzte Moleküle (abstrakte Sechsecke) Richtung Gehirn
    mols = [(612,432,8.5,'#4fd3c8','#2a6fd6'),(588,456,9.5,'#5d8ff0','#2d4fb8'),(632,468,7.5,'#f7923f','#c25a12'),
            (600,490,8.5,'#ef6fb4','#a8367c'),(571,428,6.5,'#4fd3c8','#2a6fd6'),(560,480,7,'#f7923f','#c25a12')]
    for (x, y, rad, f, s) in mols:
        g.append(hexagon(x, y, rad, f, s, 2, rot=rng.uniform(0, 30)))
    r = random.Random(3)
    for _ in range(16):
        x = r.uniform(548, 646); y = r.uniform(408, 500)
        g.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r.uniform(1.8,3.2):.1f}" fill="{r.choice(["#5ee6dc","#ffb070","#ff8fd0","#8fb8ff"])}"/>')
    return g

# ---------------- Straße, Sperre, Scheinwerfer ----------------
def road_svg():
    g = []
    g.append('<path d="M232,352 L232,640 C232,680 244,700 266,724" stroke="url(#roadg)" stroke-width="30" fill="none" stroke-linecap="butt"/>')
    g.append('<path d="M232,380 L232,640 C232,680 244,700 266,724" stroke="url(#roadg2)" stroke-width="6" fill="none" stroke-opacity=".9"/>')
    return g

def barrier_svg():
    g = ['<g transform="translate(232,576)">']
    # Füße
    for x in (-42, 30):
        g.append(f'<rect x="{x}" y="12" width="12" height="30" rx="2.5" fill="#9aa3d6" stroke="#3e4594" stroke-width="2"/>')
    # Balken
    g.append('<rect x="-52" y="-16" width="104" height="30" rx="3.5" fill="#eef0fa" stroke="#3e4594" stroke-width="2.4"/>')
    g.append('<rect x="-52" y="-16" width="104" height="10" rx="3" fill="#8a95cf"/>')
    g.append('<rect x="-49" y="-3" width="98" height="14" fill="url(#stripes)" stroke="#3e4594" stroke-width="1.4"/>')
    g.append('</g>')
    return g

def spotlight_svg():
    g = []
    g.append('<path d="M291,364 L342,364 L318,604 Z" fill="url(#spotg)" fill-opacity=".92"/>')
    g.append('<path d="M291,364 L342,364 L318,604 Z" fill="none" stroke="#eef7a0" stroke-opacity=".6" stroke-width="1"/>')
    g.append('<circle cx="318" cy="602" r="16" fill="url(#glow)"/>')
    g.append('<circle cx="318" cy="602" r="3.5" fill="#ffffff"/>')
    return g

# ---------------- Icons unten links ----------------
def stopwatch_svg(cx, cy, r):
    g = [f'<g transform="translate({cx},{cy})">']
    g.append(f'<rect x="-9" y="{-r-18}" width="18" height="12" rx="3" fill="#8a95cf" stroke="#3b3a8c" stroke-width="2.4"/>')
    g.append(f'<rect x="-5" y="{-r-9}" width="10" height="8" fill="#5c62b0" stroke="#3b3a8c" stroke-width="2"/>')
    g.append(f'<g transform="rotate(-40)"><rect x="-6" y="{-r-12}" width="12" height="9" rx="2.5" fill="#8a95cf" stroke="#3b3a8c" stroke-width="2.2"/></g>')
    g.append(f'<circle cx="0" cy="0" r="{r}" fill="#ffffff" stroke="#3b3a8c" stroke-width="4"/>')
    g.append(f'<circle cx="0" cy="0" r="{r-7}" fill="#eef0fb" stroke="#8a95cf" stroke-width="1.5"/>')
    # Sektor 12 bis ca. 4 Uhr
    a = math.radians(125); rr = r - 8
    g.append(f'<path d="M0,0 L0,{-rr} A{rr},{rr} 0 0 1 {rr*math.sin(a):.1f},{-rr*math.cos(a):.1f} Z" fill="url(#secg)"/>')
    for i in range(12):
        ang = math.radians(i*30); r1 = r - 10; r2 = r - (16 if i % 3 == 0 else 13)
        g.append(f'<line x1="{r1*math.sin(ang):.1f}" y1="{-r1*math.cos(ang):.1f}" x2="{r2*math.sin(ang):.1f}" y2="{-r2*math.cos(ang):.1f}" stroke="#3b3a8c" stroke-width="{2.2 if i%3==0 else 1.4}" stroke-linecap="round"/>')
    g.append(f'<line x1="0" y1="4" x2="{(r-16)*math.sin(a):.1f}" y2="{-(r-16)*math.cos(a):.1f}" stroke="#3b3a8c" stroke-width="3.2" stroke-linecap="round"/>')
    g.append(f'<line x1="0" y1="0" x2="0" y2="{-(r-20)}" stroke="#3b3a8c" stroke-width="3" stroke-linecap="round"/>')
    g.append('<circle cx="0" cy="0" r="4" fill="#3b3a8c"/><circle cx="0" cy="0" r="1.6" fill="#fff"/>')
    g.append('</g>')
    return g

def calendar_svg(x, y, w, h):
    g = [f'<g transform="translate({x},{y})">']
    g.append(f'<path d="M0,10 Q0,4 6,4 L{w-6},4 Q{w},4 {w},10 L{w},{h-6} Q{w},{h} {w-6},{h} L16,{h} L6,{h+10} L7,{h} Q0,{h} 0,{h-6} Z" fill="#ffffff" stroke="#3b3a8c" stroke-width="2.8" stroke-linejoin="round"/>')
    g.append(f'<path d="M1.4,10 Q1.4,5.4 6,5.4 L{w-6},5.4 Q{w-1.4},5.4 {w-1.4},10 L{w-1.4},17 L1.4,17 Z" fill="url(#secg)"/>')
    for rx in (10, w-10):
        g.append(f'<rect x="{rx-2}" y="-2" width="4" height="12" rx="2" fill="#3b3a8c"/>')
    g.append(f'<path d="M11,{h*0.62:.0f} L{w*0.42:.0f},{h*0.78:.0f} L{w-9},{h*0.42:.0f}" fill="none" stroke="#e95a9c" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>')
    g.append('</g>')
    return g

def small_brain_svg(x, y, s):
    """Kleines Gehirn in Seitenansicht (Stirn rechts), Verlaufsfarben."""
    outline = [(152,198),(122,210),(82,206),(60,190),(36,172),(28,136),(38,108),(50,72),(92,40),(145,28),
               (195,16),(255,14),(305,26),(362,40),(408,74),(428,118),(442,150),(440,182),(426,198),
               (410,212),(385,218),(360,220),(318,226),(270,240),(228,242),(192,244),(162,236),(154,222)]
    cereb = [(300,226),(320,214),(380,208),(418,206),(436,214),(438,240),(424,258),(408,280),(372,290),
             (342,284),(316,279),(298,264),(294,248),(291,238),(294,230)]
    stem = [(266,236),(252,252),(258,276),(276,300),(283,318),(307,318),(305,296),(312,276),(310,250),(300,236)]
    sulci = [[(258,17),(252,40),(262,58),(248,80),(236,100),(246,118),(232,138),(222,152)],
             [(153,199),(175,186),(205,176),(240,168),(275,160),(300,152),(322,142),(338,126)],
             [(222,60),(190,56),(160,62),(130,56),(105,52),(86,62),(70,70)],
             [(209,110),(180,106),(150,116),(120,111),(100,108),(82,118),(64,124)],
             [(172,214),(205,204),(240,196),(275,190),(305,184),(330,176),(348,160),(360,140)],
             [(279,88),(305,86),(330,92),(352,100),(375,108),(392,122),(404,140)],
             [(287,20),(281,42),(291,60),(278,84),(267,104),(275,122),(263,142)],
             [(229,20),(224,40),(230,58),(220,80)],[(404,150),(396,164),(396,178),(405,190)],
             [(95,84),(110,90),(130,84),(150,90)],[(118,40),(128,46),(138,46),(148,43)],
             [(60,96),(66,100),(72,98),(80,100)],[(320,50),(330,58),(345,60),(360,58)],
             [(205,234),(240,226),(280,220),(320,214),(340,211)]]
    def T(pts): return [(x + (480 - px)*s, y + py*s) for px, py in pts]
    g = ['<g>']
    O = cr_path(T(outline), closed=True); C = cr_path(T(cereb), closed=True); S = cr_path(T(stem), closed=True)
    g.append(f'<path d="{S}" fill="#8e6fd0" stroke="#4a3a9a" stroke-width="2"/>')
    g.append(f'<path d="{C}" fill="url(#sbc)" stroke="#4a3a9a" stroke-width="2"/>')
    g.append(f'<clipPath id="sbcl"><path d="{C}"/></clipPath><g clip-path="url(#sbcl)" fill="none" stroke="#d9c6ff" stroke-width="1.2" stroke-opacity=".8">')
    for k in range(1, 9):
        cx, cy = x + (480-372)*s, y + 204*s
        g.append(f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{(10+9*k)*s:.1f}" ry="{(6+7*k)*s:.1f}"/>')
    g.append('</g>')
    g.append(f'<clipPath id="sbo"><path d="{O}"/></clipPath>')
    g.append(f'<path d="{O}" fill="url(#sbg)"/>')
    g.append('<g clip-path="url(#sbo)">')
    for p in sulci:
        d = cr_path(T(p))
        g.append(f'<path d="{d}" transform="translate(0,1.4)" fill="none" stroke="#3b2a86" stroke-opacity=".5" stroke-width="4.2" stroke-linecap="round"/>')
    for p in sulci:
        d = cr_path(T(p))
        g.append(f'<path d="{d}" fill="none" stroke="#4e3aa6" stroke-width="2.2" stroke-linecap="round"/>')
        g.append(f'<path d="{d}" transform="translate(0,-1)" fill="none" stroke="#b9ecff" stroke-opacity=".9" stroke-width="1" stroke-linecap="round"/>')
    g.append(f'<path d="{O}" fill="url(#sbshine)"/>')
    g.append('</g>')
    g.append(f'<path d="{O}" fill="none" stroke="#4a3a9a" stroke-width="2.4"/>')
    g.append('</g>')
    return g

# ---------------- Deadline-Kreislauf ----------------
def cycle_svg(x0, y0):
    g = [f'<g transform="translate({x0},{y0})">']
    nodes = ['Aufschieben', 'Deadline naht', 'Stress', 'Arbeitsphase', 'Erleichterung']
    cols = ['#6b4fbb', '#3b6fd6', '#f08a3c', '#3cc8c0', '#e86aa8']
    nw, gap, nh = 100, 18, 30
    xs = [i*(nw+gap) for i in range(5)]
    for i, (n, c) in enumerate(zip(nodes, cols)):
        x = xs[i]
        fill = c if i == 2 else '#ffffff'
        tc = '#ffffff' if i == 2 else '#111'
        g.append(f'<rect x="{x}" y="0" width="{nw}" height="{nh}" rx="15" fill="{fill}" stroke="{c}" stroke-width="2.4"/>')
        g.append(f'<text x="{x+nw/2}" y="{nh/2+5}" text-anchor="middle" fill="{tc}" style="font:700 14px \'Roboto Condensed\'">{n}</text>')
        if i < 4:
            ax = x + nw + 2; bx = x + nw + gap - 2
            g.append(f'<path d="M{ax},{nh/2} L{bx-4},{nh/2}" stroke="#333" stroke-width="2"/>')
            g.append(f'<path d="M{bx-6},{nh/2-4} L{bx},{nh/2} L{bx-6},{nh/2+4}" fill="none" stroke="#333" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>')
    # Rückführung
    lx = xs[-1] + nw/2; fx = xs[0] + nw/2; yb = nh + 14
    g.append(f'<path d="M{lx},{nh+2} L{lx},{yb} L{fx},{yb} L{fx},{nh+9}" fill="none" stroke="#f08a3c" stroke-width="2" stroke-dasharray="5 4"/>')
    g.append(f'<path d="M{fx-5},{nh+13} L{fx},{nh+5} L{fx+5},{nh+13}" fill="none" stroke="#f08a3c" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>')
    g.append(f'<text x="{(lx+fx)/2}" y="{yb+16}" text-anchor="middle" fill="#c9661c" style="font:italic 500 13px \'Roboto Condensed\'">wieder von vorn</text>')
    g.append('</g>')
    return g

# =====================================================================
def build():
    left_cols = dict(shadow='#3d2f8c', groove='#5243a8', hl=['#8dd4f5', '#e58fcf', '#b7e0ff'], rim='#b4a6ee', light='#a393e6')
    right_cols = dict(shadow='#45267e', groove='#653a9a', hl=['#f8aa6a', '#ff9fd4', '#8be0f0'], rim='#f2b8d8', light='#b985d6')
    gl, OL = hemisphere_svg(LEFT_BASE, 'L', LEFT_MED, 'L', left_cols, 21)
    gr, OR = hemisphere_svg(RIGHT_BASE, 'R', RIGHT_MED, 'R', right_cols, 34)

    defs = f'''<defs>
<filter id="shadow" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="0" dy="6" stdDeviation="7" flood-color="#2a1f5e" flood-opacity=".28"/></filter>
<linearGradient id="fillL" gradientUnits="userSpaceOnUse" x1="160" y1="400" x2="380" y2="980">
 <stop offset="0" stop-color="#8b7dd8"/><stop offset=".45" stop-color="#6c5cbe"/><stop offset="1" stop-color="#55479f"/></linearGradient>
<radialGradient id="shadeL" gradientUnits="userSpaceOnUse" cx="270" cy="640" r="330">
 <stop offset="0" stop-color="#fff" stop-opacity=".10"/><stop offset=".6" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#1d1350" stop-opacity=".35"/></radialGradient>
<linearGradient id="fillR" gradientUnits="userSpaceOnUse" x1="400" y1="400" x2="600" y2="980">
 <stop offset="0" stop-color="#a06cc8"/><stop offset=".5" stop-color="#8a55b4"/><stop offset="1" stop-color="#6e49a6"/></linearGradient>
<radialGradient id="shadeR" gradientUnits="userSpaceOnUse" cx="500" cy="640" r="330">
 <stop offset="0" stop-color="#fff" stop-opacity=".08"/><stop offset=".6" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#4a1050" stop-opacity=".32"/></radialGradient>
<linearGradient id="cutg" gradientUnits="userSpaceOnUse" x1="420" y1="440" x2="540" y2="660">
 <stop offset="0" stop-color="#36327e"/><stop offset="1" stop-color="#231e5a"/></linearGradient>
<linearGradient id="lowg" gradientUnits="userSpaceOnUse" x1="400" y1="700" x2="590" y2="950">
 <stop offset="0" stop-color="#3c3392"/><stop offset="1" stop-color="#27477f"/></linearGradient>
<linearGradient id="pA" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#55d6cf"/><stop offset="1" stop-color="#4b78d6"/></linearGradient>
<linearGradient id="pB" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#a86fde"/><stop offset="1" stop-color="#6a4fb8"/></linearGradient>
<linearGradient id="pC" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#5fb0ee"/><stop offset="1" stop-color="#3d64cc"/></linearGradient>
<linearGradient id="pD" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#48c9cc"/><stop offset="1" stop-color="#7a5fd2"/></linearGradient>
<linearGradient id="axg" gradientUnits="userSpaceOnUse" x1="766" y1="272" x2="708" y2="346">
 <stop offset="0" stop-color="#5fc9e6"/><stop offset="1" stop-color="#7f5fd0"/></linearGradient>
<linearGradient id="bulbg" gradientUnits="userSpaceOnUse" x1="-60" y1="-50" x2="60" y2="50">
 <stop offset="0" stop-color="#c8bdf6"/><stop offset=".55" stop-color="#9f88e6"/><stop offset="1" stop-color="#6fc8e8"/></linearGradient>
<radialGradient id="bulbin" gradientUnits="userSpaceOnUse" cx="-6" cy="0" r="52">
 <stop offset="0" stop-color="#4a3c92"/><stop offset="1" stop-color="#2b2366"/></radialGradient>
<linearGradient id="roadg" gradientUnits="userSpaceOnUse" x1="0" y1="352" x2="0" y2="724">
 <stop offset="0" stop-color="#c9c5de" stop-opacity="0"/><stop offset=".18" stop-color="#cbc7df" stop-opacity=".9"/><stop offset=".7" stop-color="#b1acce" stop-opacity=".92"/><stop offset="1" stop-color="#b1acce" stop-opacity="0"/></linearGradient>
<linearGradient id="roadg2" gradientUnits="userSpaceOnUse" x1="0" y1="380" x2="0" y2="724">
 <stop offset="0" stop-color="#eeedf7" stop-opacity="0"/><stop offset=".2" stop-color="#eeedf7"/><stop offset=".75" stop-color="#e2e0f0"/><stop offset="1" stop-color="#e2e0f0" stop-opacity="0"/></linearGradient>
<pattern id="stripes" patternUnits="userSpaceOnUse" width="16" height="14" patternTransform="skewX(-30)">
 <rect width="8" height="14" fill="#f26a2c"/><rect x="8" width="8" height="14" fill="#ffffff"/></pattern>
<linearGradient id="spotg" gradientUnits="userSpaceOnUse" x1="0" y1="364" x2="0" y2="604">
 <stop offset="0" stop-color="#dbe95e"/><stop offset="1" stop-color="#c9e03f"/></linearGradient>
<radialGradient id="glow"><stop offset="0" stop-color="#ffffff" stop-opacity=".95"/><stop offset=".4" stop-color="#eef7a0" stop-opacity=".8"/><stop offset="1" stop-color="#eef7a0" stop-opacity="0"/></radialGradient>
<linearGradient id="secg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f6933f"/><stop offset="1" stop-color="#e95a9c"/></linearGradient>
<linearGradient id="sbg" gradientUnits="userSpaceOnUse" x1="200" y1="1000" x2="320" y2="1110">
 <stop offset="0" stop-color="#58cfd2"/><stop offset=".5" stop-color="#7f7fe0"/><stop offset="1" stop-color="#c06fc4"/></linearGradient>
<radialGradient id="sbshine" gradientUnits="userSpaceOnUse" cx="250" cy="1020" r="110">
 <stop offset="0" stop-color="#fff" stop-opacity=".35"/><stop offset=".6" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#2a1a60" stop-opacity=".25"/></radialGradient>
<linearGradient id="sbc" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#a67fe0"/><stop offset="1" stop-color="#6f52b8"/></linearGradient>
</defs>'''

    svg = [f'<svg class="art" width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">', defs]
    # Hero-Gehirn
    svg.append('<g filter="url(#shadow)">')
    svg += gl
    svg.append('</g>')
    svg.append(f'<path d="{OL}" fill="none" stroke="#b4e6f8" stroke-opacity=".45" stroke-width="8"/>')
    svg.append(f'<path d="{OL}" fill="none" stroke="#67c9ee" stroke-width="3.4" stroke-linejoin="round"/>')
    svg.append('<g filter="url(#shadow)">')
    svg += gr
    svg.append('</g>')
    svg.append('<g clip-path="url(#clipR)">')
    svg += cutaway_svg()
    svg.append('</g>')
    svg.append(f'<path d="{OR}" fill="none" stroke="#fdd3b5" stroke-opacity=".45" stroke-width="8"/>')
    svg.append(f'<path d="{OR}" fill="none" stroke="#f5a66f" stroke-width="3.4" stroke-linejoin="round"/>')
    # Straße, Scheinwerfer, Sperre
    svg += road_svg()
    svg += spotlight_svg()
    svg += barrier_svg()
    # Synapse
    svg += synapse_svg()
    # Icons unten links
    svg += stopwatch_svg(96, 1058, 40)
    svg += calendar_svg(140, 986, 42, 40)
    svg += small_brain_svg(184, 990, 0.33)
    # Deadline-Kreislauf
    svg += cycle_svg(176, 1207)
    svg.append('</svg>')
    SVG = "\n".join(svg)

    css = """
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:768px;height:1376px;overflow:hidden;background:#fff}
body{position:relative;font-family:'Roboto Condensed';color:#111}
.art{position:absolute;left:0;top:0}
.abs{position:absolute}
.title{left:44px;top:50px;width:704px;font:700 42px/1.1 'Roboto';letter-spacing:-1.3px;color:#070707}
.kopf{font:700 15.5px/1.2 'Roboto';text-transform:uppercase;color:#0a0a0a;letter-spacing:.1px}
.sub{font:700 21px/1.06 'Roboto Condensed';color:#0a0a0a}
.sub.s{font-size:17px}
.txt{font:400 14.5px/18.5px 'Roboto Condensed';color:#111}
.txt b{font-weight:700}
.sub + .txt{margin-top:9px}
.txt + .sub{margin-top:14px}
.r{text-align:right}
.pill{display:inline-block;background:#0b0b0b;color:#fff;font:700 14.5px/1 'Roboto Condensed';text-transform:uppercase;letter-spacing:.3px;padding:6px 11px 6px;border-radius:7px;white-space:nowrap}
.pill.two{text-align:center;line-height:1.1;padding:6px 12px}
.fazit{left:44px;top:1300px;width:690px;font:400 14.5px/18.5px 'Roboto Condensed';color:#111}
.fazit b{font-weight:700}
.foot{left:44px;width:690px;font:400 10.5px/13px 'Roboto Condensed';color:#555}
.arrow{color:#f08a3c;font-weight:700}
.arr{display:inline-block;vertical-align:-1px;margin:0 2px}
"""
    html = f'''<!doctype html>
<html lang="de"><head><meta charset="utf-8"><title>ADHS im Gehirn</title>
<link rel="stylesheet" href="../assets/fonts.css">
<style>{css}</style></head><body>
{SVG}
<div class="abs title">ADHS im Gehirn: Kein Willensproblem,<br>sondern ein Steuerungsproblem</div>

<div class="abs kopf" style="left:44px;top:198px;width:260px">Typische<br>Verhaltensparadoxa</div>
<div class="abs kopf" style="left:416px;top:198px;width:300px">Die neurobiologischen<br>Ursachen</div>

<div class="abs" style="left:44px;top:254px;width:150px">
 <div class="sub">Blockade vs.<br>Hyperfokus</div>
 <div class="txt">Die wichtige E-Mail (5&nbsp;Minuten Arbeit) bleibt eine Stunde liegen. Beim Lieblingsthema: stundenlanger Hyperfokus.<br>Aufmerksamkeit haben: ja. Aufmerksamkeit steuern: schwierig.<br><b>Dasselbe Gehirn, andere Aktivierung.</b></div>
</div>

<div class="abs pill" style="left:262px;top:330px">Hyperfokus</div>
<div class="abs pill" style="left:44px;top:672px">Blockade</div>

<div class="abs sub" style="left:416px;top:254px;width:230px">Der Bewerter:<br>Dopamin &amp; Noradrenalin</div>
<div class="abs pill" style="right:36px;top:478px">Dopamin</div>
<div class="abs r" style="left:608px;top:514px;width:124px">
 <div class="txt">Fragt ständig: „Lohnt sich das jetzt?“ Nicht einfach „zu wenig Dopamin“, sondern veränderte Signalwege.<br>Wichtig finden ≠ jetzt Motivation aufbringen.</div>
 <div class="sub s">Die Lücke zwischen Wissen und Tun</div>
 <div class="txt">„Ich sollte …“ <svg class="arr" width="18" height="10" viewBox="0 0 18 10"><path d="M1,5 H15 M11,1 L15,5 L11,9" fill="none" stroke="#f08a3c" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg> „Ich mache es jetzt.“<br>Ich weiß es und schaffe es trotzdem nicht anzufangen.</div>
</div>

<div class="abs sub" style="left:44px;top:932px;width:160px">Leistung unter<br>Zeitdruck</div>
<div class="abs txt" style="left:44px;top:1118px;width:300px">Zeitdruck, Neuheit, unmittelbare Konsequenzen und persönliches Interesse schalten die Aktivierung ein.</div>

<div class="abs pill two" style="right:36px;top:984px">Präfrontaler<br>Cortex</div>
<div class="abs txt r" style="left:556px;top:1040px;width:176px">Die Steuerzentrale für fünf Aufgaben:<br>Planen · Arbeitsgedächtnis<br>Ablenkung ausblenden<br>Impulse bremsen<br>Langfristige Ziele<br>Bei reizarmen Aufgaben weniger stabil.</div>

<div class="abs sub s" style="left:44px;top:1205px;width:120px">Die Deadline-Falle</div>

<div class="abs fazit"><b>Fazit:</b> ADHS heißt nicht „keine Aufmerksamkeit“. Es heißt: Aufmerksamkeit, Motivation und Verhalten zuverlässig an das anzupassen, was gerade nötig ist, fällt schwer.</div>
<div class="abs foot" style="top:1346px">Quelle: NeuroWissen TV, „NEUROLOGE ERKLÄRT: Das macht ADHS wirklich in deinem Gehirn“ (2026)</div>
<div class="abs foot" style="top:1359px">Hinweis: Kein Hirnscan kann ADHS diagnostizieren, es gibt nur Gruppenunterschiede. Die Diagnose gehört zu Fachleuten.</div>
</body></html>'''
    with open(os.path.join(HERE, 'v2.html'), 'w', encoding='utf-8') as f:
        f.write(html)
    print('v2.html geschrieben,', len(html), 'Zeichen')

if __name__ == '__main__':
    build()
