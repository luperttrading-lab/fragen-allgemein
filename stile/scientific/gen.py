#!/usr/bin/env python3
# Erzeugt scientific.html (Stil "Scientific") – alle Grafiken als Inline-SVG.
import math, os
HERE = os.path.dirname(os.path.abspath(__file__))

# ---------- Palette ----------
NAVY = '#15294d'; NAVY2 = '#22406f'; STEEL = '#3f6b98'; STEEL_L = '#d3e0ee'; STEEL_LL = '#eaf1f8'
PETROL = '#1d6f77'; PETROL_L = '#d6eaeb'; GREY = '#566170'; GREY_M = '#8b95a3'; GREY_L = '#d6dbe2'
ORANGE = '#e2761b'; ORANGE_D = '#a9520c'; ORANGE_L = '#fde6cf'; INK = '#1b2430'; LINE = '#2b3442'

# ---------- Geometrie-Helfer ----------
def bez(p0, p1, p2, p3, n=24):
    out = []
    for i in range(n + 1):
        t = i / n; u = 1 - t
        out.append((u**3*p0[0] + 3*u*u*t*p1[0] + 3*u*t*t*p2[0] + t**3*p3[0],
                    u**3*p0[1] + 3*u*u*t*p1[1] + 3*u*t*t*p2[1] + t**3*p3[1]))
    return out

def sample(cp, n=24):
    pts = [cp[0]]
    for i in range(1, len(cp), 3):
        pts += bez(cp[i-1], cp[i], cp[i+1], cp[i+2], n)[1:]
    return pts

def dpath(cp, close=False):
    s = f"M{cp[0][0]},{cp[0][1]}"
    for i in range(1, len(cp), 3):
        s += f" C{cp[i][0]},{cp[i][1]} {cp[i+1][0]},{cp[i+1][1]} {cp[i+2][0]},{cp[i+2][1]}"
    return s + (" Z" if close else "")

def poly(pts, close=True):
    return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + (" Z" if close else "")

def hexagon(cx, cy, r, fill, stroke='none', sw=0.6):
    pts = [(cx + r*math.cos(math.radians(a)), cy + r*math.sin(math.radians(a))) for a in range(30, 390, 60)]
    return f'<path d="{poly(pts)}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'

def diamond(cx, cy, r, fill, stroke='none', sw=0.6):
    pts = [(cx, cy-r), (cx+r*0.82, cy), (cx, cy+r), (cx-r*0.82, cy)]
    return f'<path d="{poly(pts)}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'

MONO = "font-family:'IBM Plex Mono';font-size:12px;font-weight:500"

def lbl(text, x, y, anchor='start', color=INK, weight=500, size=12, fam='IBM Plex Mono', extra=''):
    return (f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" fill="{color}" '
            f'style="font-family:\'{fam}\';font-size:{size}px;font-weight:{weight}{extra}">{text}</text>')

def leader(x1, y1, x2, y2, color=LINE, dot=True, sw=0.8):
    s = f'<path d="M{x1:.1f},{y1:.1f} L{x2:.1f},{y2:.1f}" stroke="{color}" stroke-width="{sw}" fill="none"/>'
    if dot:
        s += f'<circle cx="{x2:.1f}" cy="{y2:.1f}" r="2.3" fill="{color}" stroke="#fff" stroke-width="0.9"/>'
    return s

def leader_poly(pts, color=LINE, sw=0.8):
    s = f'<path d="{poly(pts, False)}" stroke="{color}" stroke-width="{sw}" fill="none"/>'
    x2, y2 = pts[-1]
    s += f'<circle cx="{x2:.1f}" cy="{y2:.1f}" r="2.3" fill="{color}" stroke="#fff" stroke-width="0.9"/>'
    return s

# =====================================================================
# Abb. 1 – Gehirn, Lateralansicht der rechten Hemisphäre (Stirn rechts)
# lokale Koordinaten: Stirn LINKS, wird per scale(-1,1) gespiegelt
# =====================================================================
def brain_svg():
    W, H = 696, 246
    S, TX, TY = 0.75, 461, 12
    def P(x, y): return (TX - S*x, TY + S*y)

    outline = [(152,198),(122,210),(82,206),(60,190),(36,172),(28,136),(38,108),(50,72),(92,40),(145,28),
               (195,16),(255,14),(305,26),(362,40),(408,74),(428,118),(442,150),(440,182),(426,198),
               (410,212),(385,218),(360,220),(318,226),(270,240),(228,242),(192,244),(162,236),(154,222),
               (150,214),(151,205),(152,198)]
    lat_main = [(153,199),(175,186),(205,176),(240,168),(275,160),(300,152),(322,142)]
    lat_asc = [(322,142),(332,136),(338,126),(340,116)]
    central = [(258,17),(252,40),(262,58),(248,80),(236,100),(246,118),(232,138),(222,152),(226,160),(219,167)]

    O = dpath(outline, True)
    lat_pts = sample(lat_main, 40)
    cen_pts = sample(central, 40)
    # Schnittpunkt Zentralfurche-Verlängerung mit Seitenfurche
    xl, yl = min(lat_pts, key=lambda p: abs(p[0] - 219))
    front_poly = [(-30,-30),(258,-30)] + cen_pts + [(xl, yl)] + [p for p in reversed(lat_pts) if p[0] < xl] + \
                 [(153,199),(140,208),(130,320),(-30,320)]
    pari_poly = [(258,-30),(392,-30),(392,58),(385.2,142),(322,142)] + \
                [p for p in reversed(lat_pts) if p[0] >= xl] + [(xl, yl)] + list(reversed(cen_pts))
    temp_poly = [(150,201)] + lat_pts + [(385.2,142),(380,206),(380,330),(140,330)]
    occ_poly = [(392,-30),(480,-30),(480,330),(380,330),(380,206),(385.2,142),(392,58)]
    pfc_poly = [(-30,-30),(193,-30),(191,10),(188,40),(184,75),(180,110),(175,140),(170,165),(165,185),
                (158,215),(120,320),(-30,320)]

    sulci = [
        central,
        [(229,20),(224,40),(230,58),(220,80)],
        [(214,96),(206,116),(212,136),(200,152),(194,162),(196,170),(192,176)],
        [(287,20),(281,42),(291,60),(278,84),(267,104),(275,122),(263,142),(257,152),(258,158),(253,161)],
        lat_main, lat_asc,
        [(178,186),(176,178),(174,172),(171,165)],
        [(168,190),(162,188),(155,188),(147,186)],
        [(222,60),(190,56),(160,62),(130,56),(105,52),(86,62),(70,70)],
        [(209,110),(180,106),(150,116),(120,111),(100,108),(82,118),(64,124)],
        [(172,214),(205,204),(240,196),(275,190),(305,184),(330,176),(348,160),(356,150),(360,140),(362,130)],
        [(205,234),(240,226),(280,220),(320,214),(340,211),(356,209),(372,207)],
        [(279,88),(305,86),(330,92),(352,100),(375,108),(392,122),(404,140)],
        [(404,150),(396,164),(396,178),(405,190)],
        [(398,96),(406,104),(412,112),(418,124)],
        [(392,58),(388,66),(386,74),(388,82)],
        [(378,219),(376,214),(377,209),(380,205)],
        # kleinere Furchen für Detail
        [(118,40),(128,46),(138,46),(148,43)],
        [(95,84),(110,90),(130,84),(150,90)],
        [(160,84),(168,80),(176,82),(182,78)],
        [(300,120),(310,112),(318,110),(326,104)],
        [(320,50),(330,58),(345,60),(360,58)],
        [(250,206),(262,209),(275,206),(290,210)],
        [(300,198),(312,200),(322,196),(334,196)],
        [(372,128),(380,136),(380,148),(374,156)],
        [(415,160),(420,168),(424,176),(422,186)],
        [(235,186),(240,184),(248,183),(255,180)],
        [(60,96),(66,100),(72,98),(80,100)],
    ]
    cereb = [(300,226),(320,214),(380,208),(418,206),(436,214),(438,240),(424,258),(408,280),(372,290),
             (342,284),(316,279),(298,264),(294,248),(291,238),(294,230),(300,226)]
    C = dpath(cereb, True)
    BS = "M266,236 C252,248 250,268 262,280 C272,290 280,302 283,318 L307,318 C305,302 306,290 312,276 C316,262 310,246 302,236 Z"

    # Schnittfenster (Cutaway) im ventralen präfrontalen Cortex
    # Fensterpolygon: entlang Außenkontur von (31,150) bis (100,208), dann Schnittkanten
    seg_a = sample([(152,198),(122,210),(82,206),(60,190)], 30)   # Unterseite (rückwärts zur Stirn)
    seg_b = sample([(60,190),(36,172),(28,136),(38,108)], 30)      # Stirnpol
    cut_top_y, cut_x = 124, 124
    rim = [p for p in seg_a if p[0] <= cut_x]
    rim += [p for p in seg_b[1:] if p[1] >= cut_top_y]
    win = [(cut_x, cut_top_y)] + [(cut_x, rim[0][1]-0.5)] + rim[1:] + [(rim[-1][0], cut_top_y)]
    WIN = poly(win)

    g = []
    g.append('<defs>')
    g.append(f'<clipPath id="cer"><path d="{O}"/></clipPath>')
    g.append(f'<clipPath id="frontc"><path d="{poly(front_poly)}"/></clipPath>')
    g.append(f'<clipPath id="cbl"><path d="{C}"/></clipPath>')
    g.append(f'<clipPath id="winc"><path d="{WIN}"/></clipPath>')
    g.append('''<linearGradient id="metal" gradientUnits="userSpaceOnUse" x1="40" y1="10" x2="300" y2="260">
      <stop offset="0" stop-color="#f7f9fb"/><stop offset=".28" stop-color="#d3d9e0"/>
      <stop offset=".5" stop-color="#eef1f4"/><stop offset=".78" stop-color="#b9c1cb"/><stop offset="1" stop-color="#99a3af"/></linearGradient>
    <linearGradient id="metal2" gradientUnits="userSpaceOnUse" x1="300" y1="205" x2="420" y2="295">
      <stop offset="0" stop-color="#e9edf1"/><stop offset=".45" stop-color="#bfc7d0"/><stop offset=".7" stop-color="#dde2e8"/><stop offset="1" stop-color="#8f9aa7"/></linearGradient>
    <linearGradient id="metal3" gradientUnits="userSpaceOnUse" x1="250" y1="240" x2="315" y2="250">
      <stop offset="0" stop-color="#eef1f4"/><stop offset=".5" stop-color="#c3cad3"/><stop offset="1" stop-color="#9aa4b0"/></linearGradient>
    <linearGradient id="pfcg" gradientUnits="userSpaceOnUse" x1="0" y1="20" x2="120" y2="215">
      <stop offset="0" stop-color="#f9c48f"/><stop offset=".55" stop-color="#ee9447"/><stop offset="1" stop-color="#d0660f"/></linearGradient>
    <linearGradient id="wmg" gradientUnits="userSpaceOnUse" x1="30" y1="146" x2="112" y2="210">
      <stop offset="0" stop-color="#7fa6cf"/><stop offset=".6" stop-color="#4f7fb3"/><stop offset="1" stop-color="#2f5d90"/></linearGradient>
    <radialGradient id="shine" gradientUnits="userSpaceOnUse" cx="250" cy="70" r="230">
      <stop offset="0" stop-color="#fff" stop-opacity=".55"/><stop offset=".55" stop-color="#fff" stop-opacity="0"/>
      <stop offset="1" stop-color="#0d1622" stop-opacity=".22"/></radialGradient>
    <pattern id="hatchO" patternUnits="userSpaceOnUse" width="4" height="4" patternTransform="rotate(45)">
      <line x1="0" y1="0" x2="0" y2="4" stroke="#8a3f05" stroke-width="0.7" stroke-opacity=".35"/></pattern>
    <pattern id="hatchS" patternUnits="userSpaceOnUse" width="3.2" height="3.2" patternTransform="rotate(-45)">
      <line x1="0" y1="0" x2="0" y2="3.2" stroke="#1b2430" stroke-width="0.6" stroke-opacity=".55"/></pattern>''')
    g.append('</defs>')

    # Orientierung (Kompass)
    g.append(f'<g stroke="{GREY}" stroke-width="1" fill="none">'
             f'<path d="M14,44 L14,10"/><path d="M10,15 L14,8 L18,15" fill="{GREY}"/>'
             f'<path d="M14,44 L52,44"/><path d="M47,40 L54,44 L47,48" fill="{GREY}"/></g>')
    g.append(lbl('dorsal', 22, 16, color=GREY, size=12))
    g.append(lbl('anterior (Stirn)', 60, 48, color=GREY, size=12))

    g.append(f'<g transform="translate({TX},{TY}) scale({-S},{S})">')
    # Hirnstamm
    g.append(f'<path d="{BS}" fill="url(#metal3)" stroke="{LINE}" stroke-width="1.4"/>')
    for yy in (250, 258, 266, 274):
        g.append(f'<path d="M{257 + (yy-250)*0.25:.1f},{yy} C{272},{yy+3} {292},{yy+3} {311 - (yy-250)*0.05:.1f},{yy-2}" stroke="#6b7583" stroke-width="0.7" fill="none" opacity=".8"/>')
    g.append(f'<path d="M262,281 C278,285 296,285 311,278" stroke="{LINE}" stroke-width="1" fill="none"/>')
    g.append(f'<path d="M286,284 C288,296 292,306 294,318" stroke="#7d8794" stroke-width="0.8" fill="none"/>')
    # Schnittfläche unten (Schnitt durch das verlängerte Mark)
    g.append(f'<ellipse cx="295" cy="318" rx="12" ry="3.6" fill="#fff" stroke="{LINE}" stroke-width="1.1"/>')
    g.append(f'<ellipse cx="295" cy="318" rx="12" ry="3.6" fill="url(#hatchS)"/>')
    # Kleinhirn
    g.append(f'<path d="{C}" fill="url(#metal2)" stroke="none"/>')
    g.append('<g clip-path="url(#cbl)" fill="none">')
    for k in range(1, 20):
        rx, ry = 14 + 5.4*k, 7 + 4.3*k
        sw = 1.2 if k in (8, 13) else 0.65
        col = '#3b4553' if k in (8, 13) else '#5f6977'
        g.append(f'<ellipse cx="372" cy="204" rx="{rx:.1f}" ry="{ry:.1f}" stroke="{col}" stroke-width="{sw}"/>')
        g.append(f'<ellipse cx="372.8" cy="205.3" rx="{rx:.1f}" ry="{ry:.1f}" stroke="#fff" stroke-opacity=".55" stroke-width=".55"/>')
    g.append(f'<path d="{C}" stroke="#101820" stroke-opacity=".18" stroke-width="9"/>')
    g.append('</g>')
    g.append(f'<path d="{C}" fill="none" stroke="{LINE}" stroke-width="1.5"/>')

    # Großhirn
    g.append('<g clip-path="url(#cer)">')
    g.append(f'<path d="{O}" fill="url(#metal)"/>')
    g.append(f'<path d="{poly(front_poly)}" fill="{STEEL}" fill-opacity=".30"/>')
    g.append(f'<path d="{poly(pari_poly)}" fill="#e9ecf0" fill-opacity=".25"/>')
    g.append(f'<path d="{poly(temp_poly)}" fill="#6f7b8a" fill-opacity=".22"/>')
    g.append(f'<path d="{poly(occ_poly)}" fill="#5d6876" fill-opacity=".16"/>')
    g.append(f'<g clip-path="url(#frontc)"><path d="{poly(pfc_poly)}" fill="url(#pfcg)"/>'
             f'<path d="{poly(pfc_poly)}" fill="url(#hatchO)"/></g>')
    g.append(f'<path d="{O}" fill="url(#shine)"/>')
    # Furchen (Schatten, Linie, Lichtkante)
    for s in sulci:
        d = dpath(s)
        g.append(f'<path d="{d}" fill="none" stroke="#141c26" stroke-opacity=".13" stroke-width="5.5" stroke-linecap="round"/>')
    for s in sulci:
        d = dpath(s)
        g.append(f'<path d="{d}" fill="none" stroke="#3a4351" stroke-width="1.45" stroke-linecap="round"/>')
        g.append(f'<path d="{d}" transform="translate(-1.1,1.4)" fill="none" stroke="#fff" stroke-opacity=".7" stroke-width=".9" stroke-linecap="round"/>')
    # Lappengrenzen (gedachte Linien)
    g.append(f'<path d="M390,84 L380,204 M322,142 L385,142" stroke="{GREY}" stroke-width="1" stroke-dasharray="3 2.5" fill="none"/>')
    # PFC-Grenze
    g.append(f'<g clip-path="url(#frontc)"><path d="{poly(pfc_poly[1:11], False)}" stroke="{ORANGE_D}" stroke-width="1.3" stroke-dasharray="4 2.5" fill="none"/></g>')
    # Rand-Schattierung
    g.append(f'<path d="{O}" fill="none" stroke="#0d1520" stroke-opacity=".17" stroke-width="13"/>')

    # ---- Schnittfenster ----
    g.append(f'<g clip-path="url(#winc)">')
    g.append(f'<path d="{WIN}" fill="url(#wmg)"/>')
    # Faserbahnen der weißen Substanz
    for i in range(14):
        y0 = 124 + i*6.5
        g.append(f'<path d="M126,{y0} C105,{y0+5} 80,{y0+2+i*0.8} 30,{y0 + 18 + i*1.2}" stroke="#e3edf8" stroke-opacity=".5" stroke-width=".75" fill="none"/>')
    # Rinde (graue Substanz) als Band entlang der Außenkontur, mit Einfaltungen
    g.append(f'<path d="{O}" fill="none" stroke="url(#pfcg)" stroke-width="19"/>')
    g.append(f'<path d="{O}" fill="none" stroke="url(#hatchO)" stroke-width="19"/>')
    # Einfaltungen der Rinde (Furchen im Querschnitt): senkrecht zur Kontur nach innen
    for idx in (6, 13, 21, 30, 38, 46):
        if idx + 1 >= len(rim): continue
        (x0, y0), (x1, y1) = rim[idx], rim[idx + 1]
        tx, ty = x1 - x0, y1 - y0; n = math.hypot(tx, ty) or 1
        nx, ny = -ty / n, tx / n
        if (80 - x0) * nx + (165 - y0) * ny < 0: nx, ny = -nx, -ny
        xa, ya, xb, yb = x0 + nx*2, y0 + ny*2, x0 + nx*21, y0 + ny*21
        g.append(f'<path d="M{xa:.1f},{ya:.1f} L{xb:.1f},{yb:.1f}" stroke="#de7a22" stroke-width="10" stroke-linecap="round"/>')
        g.append(f'<path d="M{xa:.1f},{ya:.1f} L{xb:.1f},{yb:.1f}" stroke="url(#hatchO)" stroke-width="10" stroke-linecap="round"/>')
        g.append(f'<path d="M{x0:.1f},{y0:.1f} L{xb-nx*3:.1f},{yb-ny*3:.1f}" stroke="#3a4351" stroke-width="1.2" stroke-linecap="round"/>')
    # Schnittkanten: Rinde quer geschnitten (Band entlang der Schnittlinien), schraffiert
    cutd = f'M{cut_x},{rim[0][1]+4} L{cut_x},{cut_top_y} L{rim[-1][0]-4},{cut_top_y}'
    g.append(f'<path d="{cutd}" fill="none" stroke="#f4b77c" stroke-width="20"/>')
    g.append(f'<path d="{cutd}" fill="none" stroke="url(#hatchS)" stroke-width="20"/>')
    cutd2 = f'M{cut_x-10},{rim[0][1]+4} L{cut_x-10},{cut_top_y+10} L{rim[-1][0]-4},{cut_top_y+10}'
    g.append(f'<path d="{cutd2}" fill="none" stroke="#2c4b72" stroke-width="1.1"/>')
    g.append('</g>')
    g.append(f'<path d="{WIN}" fill="none" stroke="{LINE}" stroke-width="1.5"/>')
    g.append('</g>')  # Ende clip cer
    g.append(f'<path d="{O}" fill="none" stroke="{LINE}" stroke-width="1.7"/>')
    g.append('</g>')  # Ende Spiegelung

    # ---- Beschriftungen ----
    L = []
    def A(x, y): return P(x, y)
    # links
    ax, ay = A(335, 72); L.append(leader(116, ay, ax, ay)); L.append(lbl('Parietallappen', 112, ay + 4, 'end'))
    ax, ay = A(418, 160); L.append(leader(116, ay, ax, ay)); L.append(lbl('Okzipitallappen', 112, ay + 4, 'end'))
    ax, ay = A(385, 255); L.append(leader(116, ay, ax, ay)); L.append(lbl('Kleinhirn', 112, ay + 4, 'end'))
    ax, ay = A(292, 302); L.append(leader(116, ay, ax, ay)); L.append(lbl('Hirnstamm', 112, ay + 4, 'end'))
    # oben
    ax, ay = A(256, 49); L.append(leader(ax, 16, ax, ay)); L.append(lbl('Zentralfurche', ax, 12, 'middle'))
    ax, ay = A(208, 48); L.append(leader(331, 9, ax, ay)); L.append(lbl('Frontallappen', 335, 12))
    # unten
    ax, ay = A(250, 212); L.append(leader_poly([(276, 228), (ax, ay)])); L.append(lbl('Temporallappen', 280, 239))
    # Schnittfenster
    ax, ay = A(119, 172); L.append(leader_poly([(370, 199), (ax, ay)], color=ORANGE_D)); L.append(lbl('Graue Substanz', 374, 203, color=ORANGE_D))
    ax, ay = A(84, 160); L.append(leader_poly([(370, 217), (ax, ay)], color=NAVY2))
    L.append(f'<text x="374" y="221" fill="{NAVY2}" style="font-family:\'IBM Plex Mono\';font-size:12px;font-weight:500">Wei<tspan style="font-family:\'IBM Plex Sans\'">ß</tspan>e Substanz</text>')

    # ---- Aufgabenliste (rechts) ----
    pfx, pfy = A(88, 88)
    items = ['Planen', 'Arbeitsgedächtnis', 'Ablenkung ausblenden', 'Impulse bremsen', 'Langfristige Ziele']
    by0 = 50
    L.append(lbl('Präfrontaler Cortex', 494, 18, color=ORANGE_D, weight=600, size=13))
    L.append(lbl('Fünf Aufgaben:', 494, 37, color=GREY, size=13, fam='IBM Plex Sans', weight=500))
    for i, t in enumerate(items):
        y = by0 + 15 + i*26
        L.append(f'<rect x="494" y="{y-13}" width="18" height="18" fill="{NAVY}"/>')
        L.append(lbl(str(i+1), 503, y, 'middle', color='#fff', weight=600, size=12))
        L.append(lbl(t, 520, y + 0.5, color=INK, size=15, fam='IBM Plex Sans', weight=500))
    top, bot = by0 - 2, by0 + 15 + 4*26 + 7
    mid = (top + bot) / 2
    L.append(f'<path d="M490,{top} Q484,{top} 484,{top+6} L484,{mid-6} Q484,{mid} 478,{mid} Q484,{mid} 484,{mid+6} L484,{bot-6} Q484,{bot} 490,{bot}" fill="none" stroke="{ORANGE_D}" stroke-width="1.2"/>')
    L.append(leader_poly([(478, mid), (452, mid), (pfx, pfy)], color=ORANGE_D, sw=1))
    # Hinweis
    ny = bot + 14
    L.append(f'<rect x="494" y="{ny}" width="200" height="44" fill="{ORANGE_L}" stroke="none"/>')
    L.append(f'<rect x="494" y="{ny}" width="3" height="44" fill="{ORANGE}"/>')
    L.append(f'<text x="504" y="{ny+18}" fill="{INK}" style="font-family:\'IBM Plex Sans\';font-size:14px;font-weight:500">'
             f'<tspan>Bei reizarmen Aufgaben</tspan><tspan x="504" dy="18">weniger stabil.</tspan></text>')

    return f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">' + ''.join(g) + ''.join(L) + '</svg>'

# =====================================================================
# Abb. 2 – Synapse (zwei Endknöpfchen: dopaminerg / noradrenerg)
# =====================================================================
def synapse_svg():
    W, H = 426, 172
    yM, yP = 86, 97        # präsynaptische / postsynaptische Membran
    sT, sB = 136, 162      # Dendritenschaft
    out = ['<defs>',
           '''<linearGradient id="preg" x1="0" y1="0" x2="1" y2="1">
              <stop offset="0" stop-color="#f3f6f9"/><stop offset=".45" stop-color="#cfd8e2"/><stop offset=".7" stop-color="#e6ebf0"/><stop offset="1" stop-color="#a9b5c3"/></linearGradient>
           <linearGradient id="postg" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0" stop-color="#cfe0f0"/><stop offset=".5" stop-color="#a9c4df"/><stop offset="1" stop-color="#7fa2c7"/></linearGradient>
           <radialGradient id="vesg" cx=".38" cy=".35" r=".7">
              <stop offset="0" stop-color="#ffffff"/><stop offset=".7" stop-color="#e3e8ee"/><stop offset="1" stop-color="#aeb8c4"/></radialGradient>
           <linearGradient id="mitog" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0" stop-color="#9fb8d4"/><stop offset="1" stop-color="#4f78a6"/></linearGradient>
           <pattern id="hatchC" patternUnits="userSpaceOnUse" width="3" height="3" patternTransform="rotate(45)">
              <line x1="0" y1="0" x2="0" y2="3" stroke="#1b2430" stroke-width="0.6" stroke-opacity=".6"/></pattern>
           <pattern id="dots" patternUnits="userSpaceOnUse" width="6" height="6">
              <circle cx="1.5" cy="1.5" r=".55" fill="#8b95a3"/><circle cx="4.5" cy="4.5" r=".45" fill="#b4bcc7"/></pattern>''',
           '</defs>']
    # Extrazellulärraum leicht gepunktet
    out.append(f'<rect x="114" y="0" width="252" height="{H}" fill="url(#dots)" opacity=".5"/>')
    # Dendritenschaft mit Schnittkanten links/rechts
    out.append(f'<path d="M118,{sT} L362,{sT} L362,{sB} L118,{sB} Z" fill="url(#postg)" stroke="none"/>')
    out.append(f'<path d="M118,{sT} L362,{sT} M118,{sB} L362,{sB}" stroke="{NAVY2}" stroke-width="1.3"/>')
    out.append(f'<path d="M118,{sT+1.6} L362,{sT+1.6}" stroke="{NAVY2}" stroke-width=".5" opacity=".7"/>')
    for x in (118, 362):
        out.append(f'<ellipse cx="{x}" cy="{(sT+sB)/2}" rx="4" ry="{(sB-sT)/2}" fill="#fff" stroke="{NAVY2}" stroke-width="1"/>')
        out.append(f'<ellipse cx="{x}" cy="{(sT+sB)/2}" rx="4" ry="{(sB-sT)/2}" fill="url(#hatchC)"/>')
    # Mikrotubuli im Schaft
    for yy in (143, 149, 155):
        out.append(f'<path d="M124,{yy} L356,{yy}" stroke="#ffffff" stroke-opacity=".6" stroke-width=".8" stroke-dasharray="6 3"/>')

    def unit(cx, kind):
        mol = (lambda x, y, r=2.4: hexagon(x, y, r, ORANGE, ORANGE_D, .5)) if kind == 'DA' else \
              (lambda x, y, r=2.6: diamond(x, y, r, PETROL, '#0f4a50', .5))
        s = []
        # Dornfortsatz (Spine) – postsynaptisch
        sp = (f"M{cx-42},{yP} L{cx+42},{yP} C{cx+49},{yP+3} {cx+47},{yP+18} {cx+30},{yP+24} "
              f"C{cx+20},{yP+28} {cx+11},{yP+28} {cx+10},{yP+33} L{cx+10},{sT+1} L{cx-10},{sT+1} L{cx-10},{yP+33} "
              f"C{cx-11},{yP+28} {cx-20},{yP+28} {cx-30},{yP+24} C{cx-47},{yP+18} {cx-49},{yP+3} {cx-42},{yP} Z")
        s.append(f'<path d="{sp}" fill="url(#postg)" stroke="{NAVY2}" stroke-width="1.3"/>')
        # PSD
        s.append(f'<path d="M{cx-38},{yP+1.5} L{cx+38},{yP+1.5}" stroke="{NAVY}" stroke-width="3.2" stroke-opacity=".55"/>')
        # Endknöpfchen (präsynaptisch) inkl. Axon
        b = (f"M{cx-10},-2 L{cx-10},20 C{cx-14},24 {cx-48},24 {cx-50},48 C{cx-52},66 {cx-50},{yM-4} {cx-44},{yM} "
             f"L{cx+44},{yM} C{cx+50},{yM-4} {cx+52},66 {cx+50},48 C{cx+48},24 {cx+14},24 {cx+10},20 L{cx+10},-2 Z")
        s.append(f'<path d="{b}" fill="url(#preg)" stroke="{LINE}" stroke-width="1.3"/>')
        s.append(f'<path d="M{cx-43},{yM-2} L{cx+43},{yM-2}" stroke="{LINE}" stroke-width=".55" opacity=".8"/>')
        # aktive Zone
        for dx in (-30, -14, 2, 18, 34):
            s.append(f'<path d="M{cx+dx-3},{yM-1} L{cx+dx},{yM-5} L{cx+dx+3},{yM-1}" fill="#5d6876"/>')
        # Mitochondrium
        mx, my = (cx - 36, 58) if kind == 'DA' else (cx + 22, 40)
        rot = 78 if kind == 'DA' else -18
        s.append(f'<g transform="translate({mx},{my}) rotate({rot})"><ellipse rx="15" ry="6.8" fill="url(#mitog)" stroke="{NAVY2}" stroke-width="1"/>'
                 f'<path d="M-11,0 L-8,-4 L-5,3 L-2,-4 L1,3 L4,-4 L7,3 L10,-2" fill="none" stroke="#e8eff7" stroke-width=".8"/></g>')
        # Vesikel
        sign = 1 if kind == 'DA' else -1
        ves = [(6,36),(28,48),(-14,42),(-10,62),(12,62),(33,70),(-21,76)] if kind == 'DA' else [(6,38),(28,48),(-12,60),(12,63),(34,70),(-32,70),(-4,76)]
        for dx, dy in ves:
            x = cx + sign*dx
            s.append(f'<circle cx="{x}" cy="{dy}" r="8.3" fill="url(#vesg)" stroke="#5f6c7c" stroke-width=".9"/>')
            for ddx, ddy in ((-3,-2),(3,-1.5),(0,3)):
                s.append(mol(x+ddx, dy+ddy, 1.9 if kind=='DA' else 2.1))
        # Vesikel bei der Ausschüttung (Omega-Form)
        fx = cx + sign*18
        s.append(f'<path d="M{fx-7},{yM} C{fx-9},{yM-10} {fx+9},{yM-10} {fx+7},{yM}" fill="url(#vesg)" stroke="#5f6c7c" stroke-width=".9"/>')
        # Botenstoff im Spalt
        for dx, dy in ((-34,91.5),(-22,90.5),(10,91.8),(16,90),(24,92),(32,90.8),(-6,91.6)):
            s.append(mol(cx + sign*dx, dy))
        # Rezeptoren
        for i, dx in enumerate((-30, -12, 6, 24)):
            x = cx + sign*dx
            s.append(f'<path d="M{x-4},{yP-4} L{x-4},{yP+6} L{x+4},{yP+6} L{x+4},{yP-4} L{x+1.6},{yP-4} L{x+1.6},{yP-1} L{x-1.6},{yP-1} L{x-1.6},{yP-4} Z" fill="{NAVY}" stroke="#0b1730" stroke-width=".5"/>')
            if i in (1, 3):
                s.append(mol(x, yP-3.2, 2.1))
        return s

    c1, c2 = 166, 308
    out += unit(c1, 'DA')
    out += unit(c2, 'NA')
    # Kopfmarken an den Axonen
    out.append(hexagon(c1 + 21, 8, 4.2, ORANGE, ORANGE_D, .7))
    out.append(lbl('Dopamin', c1 + 29, 12, color=ORANGE_D, weight=600))
    out.append(diamond(c2 + 21, 8, 4.6, PETROL, '#0f4a50', .7))
    out.append(lbl('Noradrenalin', c2 + 29, 12, color=PETROL, weight=600))
    # Beschriftungen links
    out.append(leader(112, 28, c1 - 30, 31)); out.append(lbl('Präsynapse', 108, 32, 'end'))
    out.append(leader(112, 58, c1 - 36, 58)); out.append(lbl('Mitochondrium', 108, 62, 'end'))
    out.append(leader(112, 91.5, c1 - 38, 91.5)); out.append(lbl('Synaptischer', 108, 88, 'end')); out.append(lbl('Spalt', 108, 101, 'end'))
    out.append(leader(112, 120, c1 - 30, 114)); out.append(lbl('Postsynapse', 108, 124, 'end'))
    out.append(leader(112, 150, 124, 150)); out.append(lbl('Dendrit', 108, 154, 'end'))
    # rechts
    out.append(leader(364, 64, c2 + 35, 69)); out.append(lbl('Vesikel', 368, 68))
    out.append(leader(364, 110, c2 + 30, yP + 3)); out.append(lbl('Rezeptor', 368, 114))
    return f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">' + ''.join(out) + '</svg>'

# =====================================================================
# Abb. 3 – Aktivierung: vier Eingänge
# =====================================================================
def icon(kind, x, y):
    c = NAVY2
    if kind == 'neu':
        return (f'<path d="M{x},{y-8} L{x+2.2},{y-2.2} L{x+8},{y} L{x+2.2},{y+2.2} L{x},{y+8} L{x-2.2},{y+2.2} L{x-8},{y} L{x-2.2},{y-2.2} Z" fill="{ORANGE_L}" stroke="{c}" stroke-width="1.2"/>'
                f'<circle cx="{x+7}" cy="{y-7}" r="1.4" fill="{c}"/>')
    if kind == 'kons':
        return f'<path d="M{x+2},{y-9} L{x-5},{y+1} L{x},{y+1} L{x-2},{y+9} L{x+6},{y-2} L{x+1},{y-2} Z" fill="{ORANGE_L}" stroke="{c}" stroke-width="1.2" stroke-linejoin="round"/>'
    if kind == 'int':
        return (f'<path d="M{x-7},{y-8} L{x-7},{y+1} A7,7 0 0 0 {x+7},{y+1} L{x+7},{y-8} L{x+3},{y-8} L{x+3},{y+1} A3,3 0 0 1 {x-3},{y+1} L{x-3},{y-8} Z" fill="{ORANGE_L}" stroke="{c}" stroke-width="1.2"/>'
                f'<path d="M{x-7},{y-4.5} L{x-3},{y-4.5} M{x+3},{y-4.5} L{x+7},{y-4.5}" stroke="{c}" stroke-width="1.2"/>')
    if kind == 'zeit':
        return (f'<path d="M{x-6},{y-9} L{x+6},{y-9} M{x-6},{y+9} L{x+6},{y+9}" stroke="{c}" stroke-width="1.4"/>'
                f'<path d="M{x-5},{y-9} C{x-5},{y-3} {x},{y-2} {x},{y} C{x},{y+2} {x-5},{y+3} {x-5},{y+9} L{x+5},{y+9} C{x+5},{y+3} {x},{y+2} {x},{y} C{x},{y-2} {x+5},{y-3} {x+5},{y-9} Z" fill="{ORANGE_L}" stroke="{c}" stroke-width="1.2"/>'
                f'<path d="M{x-3},{y+8} L{x+3},{y+8} L{x},{y+4} Z" fill="{ORANGE}"/>')
    return ''

def akt_svg():
    W, H = 236, 232
    out = [f'<defs><marker id="ahE" viewBox="0 0 10 10" refX="9" refY="5" markerUnits="userSpaceOnUse" markerWidth="9" markerHeight="9" orient="auto"><path d="M0,1 L10,5 L0,9 Z" fill="{NAVY}"/></marker></defs>']
    boxes = [('neu', ['Neuheit']), ('kons', ['Unmittelbare', 'Konsequenzen']),
             ('int', ['Persönliches', 'Interesse']), ('zeit', ['Zeitdruck'])]
    bh, gap, y0, bw = 48, 12, 4, 130
    bus = 150
    ys = [y0 + i*(bh + gap) + bh/2 for i in range(4)]
    ncx, ncy, nr = 200, (ys[0] + ys[-1]) / 2, 25
    for i, (k, lines) in enumerate(boxes):
        y = y0 + i*(bh + gap)
        out.append(f'<rect x="2.5" y="{y+2}" width="{bw}" height="{bh}" fill="#c6cdd6"/>')
        out.append(f'<rect x="0.5" y="{y}" width="{bw}" height="{bh}" fill="#fff" stroke="{NAVY2}" stroke-width="1.2"/>')
        out.append(f'<rect x="0.5" y="{y}" width="27" height="{bh}" fill="{STEEL_LL}" stroke="{NAVY2}" stroke-width="1.2"/>')
        out.append(icon(k, 14, y + bh/2))
        if len(lines) == 1:
            out.append(lbl(lines[0], 35, y + bh/2 + 5, fam='IBM Plex Sans', size=14, weight=500))
        else:
            out.append(lbl(lines[0], 35, y + 20, fam='IBM Plex Sans', size=13.5, weight=500))
            out.append(lbl(lines[1], 35, y + 37, fam='IBM Plex Sans', size=13.5, weight=500))
        out.append(f'<path d="M{bw+0.5},{ys[i]} L{bus},{ys[i]}" stroke="{NAVY}" stroke-width="1.3"/>')
        out.append(f'<circle cx="{bus}" cy="{ys[i]}" r="2.6" fill="{NAVY}"/>')
    out.append(f'<path d="M{bus},{ys[0]} L{bus},{ys[-1]}" stroke="{NAVY}" stroke-width="1.6"/>')
    out.append(f'<path d="M{bus},{ncy} L{ncx-nr-7},{ncy}" stroke="{NAVY}" stroke-width="1.6" marker-end="url(#ahE)"/>')
    # Knoten mit Einschalt-Symbol
    out.append(f'<circle cx="{ncx}" cy="{ncy}" r="{nr+5}" fill="none" stroke="{ORANGE}" stroke-width="1" stroke-dasharray="2 2.5"/>')
    out.append(f'<circle cx="{ncx}" cy="{ncy}" r="{nr}" fill="{NAVY}"/>')
    out.append(f'<path d="M{ncx-6.5},{ncy-7.5} A10,10 0 1 0 {ncx+6.5},{ncy-7.5}" fill="none" stroke="{ORANGE}" stroke-width="2.6" stroke-linecap="round"/>')
    out.append(f'<path d="M{ncx},{ncy-13} L{ncx},{ncy-1}" stroke="{ORANGE}" stroke-width="2.6" stroke-linecap="round"/>')
    out.append(lbl('Aktivierung', ncx - 2, ncy + nr + 24, 'middle', color=NAVY, weight=600, size=13.5, fam='IBM Plex Sans'))
    return f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">' + ''.join(out) + '</svg>'

# =====================================================================
# Abb. 4 – Deadline-Falle als Regelkreis
# =====================================================================
def loop_svg():
    W, H = 376, 172
    cx, cy, rx, ry = 188, 90, 134, 69
    names = ['Aufschieben', 'Deadline naht', 'Stress', 'Arbeitsphase', 'Erleichterung']
    angs = [-90, -18, 54, 126, 198]
    bw, bh = 114, 30
    boxes = []
    for a in angs:
        boxes.append((cx + rx*math.cos(math.radians(a)), cy + ry*math.sin(math.radians(a))))
    def inside(p, m=5):
        for (bx, by) in boxes:
            if abs(p[0]-bx) <= bw/2 + m and abs(p[1]-by) <= bh/2 + m:
                return True
        return False
    out = [f'<defs><marker id="ahF" viewBox="0 0 10 10" refX="9" refY="5" markerUnits="userSpaceOnUse" markerWidth="9" markerHeight="9" orient="auto"><path d="M0,1 L10,5 L0,9 Z" fill="{NAVY}"/></marker>'
           f'<marker id="ahF2" viewBox="0 0 10 10" refX="9" refY="5" markerUnits="userSpaceOnUse" markerWidth="9" markerHeight="9" orient="auto"><path d="M0,1 L10,5 L0,9 Z" fill="{ORANGE}"/></marker></defs>']
    # Mittelpunkt: Kreislauf-Symbol
    out.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" stroke="{GREY_L}" stroke-width="1" stroke-dasharray="1.5 3"/>')
    out.append(f'<path d="M{cx+14},{cy-18} A17,17 0 1 0 {cx+17},{cy-4}" fill="none" stroke="{GREY_M}" stroke-width="1.6"/>')
    out.append(f'<path d="M{cx+10},{cy-24} L{cx+17},{cy-17} L{cx+8},{cy-13}" fill="none" stroke="{GREY_M}" stroke-width="1.6"/>')
    out.append(lbl('Kreislauf', cx, cy + 22, 'middle', color=GREY, size=12))
    for i in range(5):
        a0, a1 = angs[i], angs[i+1] if i < 4 else angs[0] + 360
        pts = []
        steps = 200
        for k in range(steps + 1):
            a = a0 + (a1 - a0) * k / steps
            p = (cx + rx*math.cos(math.radians(a)), cy + ry*math.sin(math.radians(a)))
            if not inside(p):
                pts.append(p)
        if len(pts) < 2: continue
        last = i == 4
        col = ORANGE if last else NAVY
        dash = ' stroke-dasharray="5 3"' if last else ''
        out.append(f'<path d="{poly(pts, False)}" fill="none" stroke="{col}" stroke-width="{1.6 if last else 1.4}"{dash} marker-end="url(#{"ahF2" if last else "ahF"})"/>')
        if last:
            mid = pts[len(pts)//2]
    for i, ((bx, by), n) in enumerate(zip(boxes, names)):
        hot = n == 'Stress'
        fill = ORANGE_L if hot else ('#fff')
        stroke = ORANGE_D if hot else NAVY2
        out.append(f'<rect x="{bx-bw/2+2}" y="{by-bh/2+2}" width="{bw}" height="{bh}" fill="#c6cdd6"/>')
        out.append(f'<rect x="{bx-bw/2}" y="{by-bh/2}" width="{bw}" height="{bh}" fill="{fill}" stroke="{stroke}" stroke-width="1.2"/>')
        out.append(f'<rect x="{bx-bw/2}" y="{by-bh/2}" width="16" height="{bh}" fill="{NAVY if not hot else ORANGE}"/>')
        out.append(lbl(str(i+1), bx-bw/2+8, by+4.5, 'middle', color='#fff', size=12, weight=600))
        out.append(lbl(n, bx + 8, by + 4.5, 'middle', color=INK, size=13, fam='IBM Plex Sans', weight=500))
    out.append(lbl('wieder von vorn', 2, 24, color=ORANGE_D, weight=600))
    return f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">' + ''.join(out) + '</svg>'

# =====================================================================
# Abb. 5 – Lücke zwischen Wissen und Tun (unterbrochener Pfeil)
# =====================================================================
def gap_svg():
    W, H = 286, 112
    out = [f'<defs><marker id="ahG" viewBox="0 0 10 10" refX="9" refY="5" markerUnits="userSpaceOnUse" markerWidth="9" markerHeight="9" orient="auto"><path d="M0,1 L10,5 L0,9 Z" fill="{NAVY}"/></marker>'
           f'<marker id="dimA" viewBox="0 0 10 10" refX="5" refY="5" markerUnits="userSpaceOnUse" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,2 L10,5 L0,8 Z" fill="{ORANGE_D}"/></marker></defs>']
    b1x, b2x, bw, by, bh = 0.5, 174, 112, 18, 50
    out.append(lbl('WISSEN', b1x + bw/2, 12, 'middle', color=NAVY2, weight=600))
    out.append(lbl('TUN', b2x + bw/2, 12, 'middle', color=NAVY2, weight=600))
    for x in (b1x, b2x):
        out.append(f'<rect x="{x+2}" y="{by+2}" width="{bw}" height="{bh}" fill="#c6cdd6"/>')
        out.append(f'<rect x="{x}" y="{by}" width="{bw}" height="{bh}" fill="{STEEL_LL if x == b1x else "#fff"}" stroke="{NAVY2}" stroke-width="1.2"/>')
    out.append(f'<text x="{b1x+bw/2}" y="{by+31}" text-anchor="middle" fill="{INK}" style="font-family:\'IBM Plex Serif\';font-style:italic;font-size:15px">„Ich sollte …“</text>')
    out.append(f'<text x="{b2x+bw/2}" y="{by+21}" text-anchor="middle" fill="{INK}" style="font-family:\'IBM Plex Serif\';font-style:italic;font-size:15px">'
               f'<tspan>„Ich mache</tspan><tspan x="{b2x+bw/2}" dy="18">es jetzt.“</tspan></text>')
    yA = by + bh/2
    # unterbrochener Pfeil mit Bruchzeichen
    out.append(f'<path d="M{b1x+bw+1},{yA} L{136},{yA}" stroke="{NAVY}" stroke-width="1.6"/>')
    out.append(f'<path d="M{152},{yA} L{b2x-1},{yA}" stroke="{NAVY}" stroke-width="1.6" marker-end="url(#ahG)"/>')
    out.append(f'<path d="M{133},{yA+8} L{139},{yA-8} M{149},{yA+8} L{155},{yA-8}" stroke="{ORANGE_D}" stroke-width="1.6"/>')
    # Maßlinie „Lücke“
    yd = by + bh + 16
    out.append(f'<path d="M{b1x+bw},{by+bh+3} L{b1x+bw},{yd+5} M{b2x},{by+bh+3} L{b2x},{yd+5}" stroke="{ORANGE_D}" stroke-width=".8"/>')
    out.append(f'<path d="M{b1x+bw+1},{yd} L{b2x-1},{yd}" stroke="{ORANGE_D}" stroke-width="1" marker-start="url(#dimA)" marker-end="url(#dimA)"/>')
    out.append(lbl('Lücke', (b1x + bw + b2x)/2, yd + 18, 'middle', color=ORANGE_D, weight=600))
    return f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">' + ''.join(out) + '</svg>'

# ---------- kleine Icons für Abschnitt A ----------
ICON_MAIL = f'''<svg style="flex:none" width="30" height="30" viewBox="0 0 34 34"><rect x="2" y="7" width="26" height="18" fill="{STEEL_LL}" stroke="{NAVY2}" stroke-width="1.3"/>
<path d="M2,7 L15,18 L28,7" fill="none" stroke="{NAVY2}" stroke-width="1.3"/><circle cx="26" cy="24" r="7" fill="#fff" stroke="{ORANGE_D}" stroke-width="1.3"/>
<path d="M26,20 L26,24 L29,26" fill="none" stroke="{ORANGE_D}" stroke-width="1.3"/></svg>'''
ICON_FOCUS = f'''<svg style="flex:none" width="30" height="30" viewBox="0 0 34 34"><circle cx="16" cy="16" r="12" fill="{ORANGE_L}" stroke="{ORANGE_D}" stroke-width="1.3"/>
<circle cx="16" cy="16" r="7.5" fill="#fff" stroke="{ORANGE_D}" stroke-width="1.3"/><circle cx="16" cy="16" r="3" fill="{ORANGE}"/>
<path d="M16,1 L16,6 M16,26 L16,31 M1,16 L6,16 M26,16 L31,16" stroke="{NAVY2}" stroke-width="1.2"/></svg>'''

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:768px;height:1376px;overflow:hidden;background:#f3f5f8}
body{position:relative;font-family:'IBM Plex Sans';color:INK;
 background-color:#f3f5f8;
 background-image:linear-gradient(#e4e8ee 1px,transparent 1px),linear-gradient(90deg,#e4e8ee 1px,transparent 1px);
 background-size:16px 16px;background-position:-1px -1px}
.topbar{position:absolute;left:0;top:0;width:768px;height:6px;background:NAVY}
.head{position:absolute;left:24px;top:6px;width:720px;height:98px;border-bottom:2px solid NAVY}
.head::after{content:'';position:absolute;left:0;right:0;bottom:-6px;border-bottom:1px solid NAVY}
.kicker{position:absolute;left:0;top:14px;font:500 12px 'IBM Plex Mono';letter-spacing:1.6px;color:STEEL}
.title{position:absolute;left:-2px;top:28px;font:700 46px/1 'IBM Plex Sans';color:NAVY;letter-spacing:-.6px}
.sub{position:absolute;left:0;top:78px;font:500 17px/1 'IBM Plex Sans';color:STEEL}
.toc{position:absolute;right:0;top:12px;width:214px;font:400 12px/15.4px 'IBM Plex Mono';color:GREY;border-left:1px solid #b8c1cd;padding-left:12px}
.toc b{font-weight:600;color:NAVY}
.toc .h{font-weight:600;color:NAVY;letter-spacing:1.2px;margin-bottom:2px}
.panel{position:absolute;background:#fff;border:1px solid #aeb8c5;padding:9px 12px 8px}
.ph{display:flex;align-items:center;gap:9px;border-bottom:1px solid #d3d9e1;padding-bottom:6px;margin-bottom:8px}
.pl{flex:none;width:22px;height:22px;background:NAVY;color:#fff;font:600 13px/22px 'IBM Plex Mono';text-align:center}
.pt{font:600 16px/1.15 'IBM Plex Sans';color:NAVY}
.pr{margin-left:auto;flex:none;font:500 12px 'IBM Plex Mono';color:GREY_M}
.cap{font:italic 13px/1.35 'IBM Plex Serif';color:#3b4554}
.cap b{font:600 12px 'IBM Plex Mono';font-style:normal;color:NAVY;margin-right:4px}
.txt{font:400 14px/1.38 'IBM Plex Sans';color:INK}
.row{display:flex;gap:9px;align-items:flex-start}
.merk{display:flex;align-items:baseline;gap:8px;border-top:1px dashed #c3cbd5;padding-top:6px}
.mk{flex:none;font:600 12px 'IBM Plex Mono';color:ORANGE_D;letter-spacing:.4px}
.mt{font:600 15px/1.3 'IBM Plex Sans';color:NAVY}
.tag{flex:none;width:90px;font:600 12px/1 'IBM Plex Mono';padding:5px 6px;letter-spacing:.6px;display:flex;align-items:center;gap:6px}
.bul{list-style:none}
.bul li{position:relative;padding-left:15px;font:400 14px/1.36 'IBM Plex Sans';margin-bottom:3px}
.bul li::before{content:'';position:absolute;left:1px;top:7px;width:6px;height:6px;background:STEEL}
.fazit{position:absolute;left:24px;width:720px;background:NAVY;color:#fff;padding:0 18px 0 16px;display:flex;gap:16px;align-items:center}
.fz{flex:none;width:74px;font:600 13px/1.2 'IBM Plex Mono';color:#f6a560;letter-spacing:1.4px;border-right:1px solid #3c5682;height:46px;display:flex;align-items:center}
.fz small{display:block;font:400 12px 'IBM Plex Mono';color:#9fb2cf;letter-spacing:.3px;margin-top:6px}
.ft{font:400 16px/1.42 'IBM Plex Sans';color:#f2f5fa}
.ft b{font-weight:600;color:#fff}
.foot{position:absolute;left:24px;width:720px;display:flex;gap:16px;border-top:1px solid #8f9aa8;padding-top:7px}
.foot .c{font:400 12px/1.45 'IBM Plex Sans';color:#3b4554}
.foot .k{font:600 12px 'IBM Plex Mono';color:NAVY;letter-spacing:1px;display:block;margin-bottom:1px}
"""
for k, v in dict(INK=INK, NAVY=NAVY, STEEL=STEEL, GREY_M=GREY_M, GREY=GREY, ORANGE_D=ORANGE_D).items():
    CSS = CSS.replace(k, v)

def panel(letter, title, x, y, w, h, body, ref=''):
    r = f'<div class="pr">{ref}</div>' if ref else ''
    return (f'<section class="panel" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px">'
            f'<div class="ph"><div class="pl">{letter}</div><div class="pt">{title}</div>{r}</div>{body}</section>')

# ---------- Layout ----------
Y1, H1 = 112, 156
YC, HC = 276, 318
Y3, H3 = 602, 340
Y4, H4 = 950, 252
YF, HF = 1210, 74
YFt = 1296

A_body = f'''
<div class="row" style="margin-bottom:7px">{ICON_MAIL}<div class="txt" style="padding-top:0">Die wichtige E-Mail (5 Minuten Arbeit) bleibt eine Stunde liegen.</div></div>
<div class="row" style="margin-bottom:8px">{ICON_FOCUS}<div class="txt" style="padding-top:0">Beim Lieblingsthema: stundenlanger Hyperfokus.</div></div>
<div class="merk"><span class="mk">MERKSATZ</span><span class="mt">Dasselbe Gehirn, andere Aktivierung.</span></div>'''

B_body = f'''
<div class="row" style="margin-bottom:9px;align-items:flex-start">
 <div class="tag" style="background:#eceff3;color:{GREY};border:1px solid #c3cbd5"><svg width="10" height="10"><path d="M1,1 L9,9 M9,1 L1,9" stroke="{GREY}" stroke-width="1.6"/></svg>MYTHOS</div>
 <div class="txt" style="color:#4a5463">faul, undiszipliniert,<br>„ist mir egal“.</div></div>
<div class="row" style="align-items:flex-start">
 <div class="tag" style="background:{PETROL};color:#fff;border:1px solid {PETROL}"><svg width="11" height="10"><path d="M1,5 L4.2,8.4 L10,1.5" fill="none" stroke="#fff" stroke-width="1.7"/></svg>REALITÄT</div>
 <div class="txt" style="font-weight:500;color:{INK}">neuroentwicklungsbedingte Störung der Selbststeuerung.</div></div>'''

C_body = f'''{brain_svg()}
<div class="cap" style="margin-top:2px"><b>Abb. 1</b>Gehirn in Seitenansicht von rechts (Stirn rechts), präfrontaler Cortex hervorgehoben. Schematisch.</div>'''

D_body = f'''{synapse_svg()}
<div class="cap" style="margin:3px 0 7px"><b>Abb. 2</b>Der Bewerter: Lohnt sich das jetzt? – Synapsen, schematisch.</div>
<ul class="bul">
<li>Fragt ständig: <b style="font-weight:600;color:{NAVY}">„Lohnt sich das jetzt?“</b></li>
<li>Nicht einfach „zu wenig Dopamin“, sondern veränderte Signalwege.</li>
<li>Wichtig finden <b style="font-weight:600;color:{ORANGE_D}">≠</b> jetzt Motivation aufbringen.</li></ul>'''

E_body = f'''{akt_svg()}
<div class="cap" style="margin-top:6px"><b>Abb. 3</b>Vier Auslöser, die die Aktivierung einschalten.</div>'''

F_body = f'''{loop_svg()}
<div class="cap" style="margin-top:4px"><b>Abb. 4</b>Kreislauf als Regelkreis (Blockschema).</div>'''

G_body = f'''{gap_svg()}
<div class="merk" style="margin-top:4px;align-items:flex-start"><span class="mk" style="padding-top:2px">MERKSATZ</span>
<span style="font:italic 14.5px/1.35 'IBM Plex Serif';color:{NAVY}">Ich weiß es und schaffe es trotzdem nicht anzufangen.</span></div>
<div class="cap" style="margin-top:6px"><b>Abb. 5</b>Prozessschema mit unterbrochenem Pfeil.</div>'''

html = f'''<!doctype html>
<html lang="de"><head><meta charset="utf-8"><title>ADHS im Gehirn</title>
<link rel="stylesheet" href="../assets/fonts.css">
<style>{CSS}</style></head>
<body>
<div class="topbar"></div>
<header class="head">
 <div class="kicker">SCHEMATISCHE ÜBERSICHT</div>
 <div class="title">ADHS im Gehirn</div>
 <div class="sub">Kein Willensproblem, sondern ein Steuerungsproblem</div>
 <div class="toc">
  <div><b>Abb. 1</b> Steuerzentrale</div><div><b>Abb. 2</b> Bewerter</div><div><b>Abb. 3</b> Aktivierung</div>
  <div><b>Abb. 4</b> Deadline-Falle</div><div><b>Abb. 5</b> Wissen und Tun</div></div>
</header>
{panel('A', 'Das Paradox', 24, Y1, 384, H1, A_body)}
{panel('B', 'Mythos vs. Realität', 418, Y1, 326, H1, B_body)}
{panel('C', 'Die Steuerzentrale: präfrontaler Cortex', 24, YC, 720, HC, C_body, 'ABB. 1')}
{panel('D', 'Der Bewerter: Dopamin &amp; Noradrenalin', 24, Y3, 450, H3, D_body, 'ABB. 2')}
{panel('E', 'Was die Aktivierung einschaltet', 484, Y3, 260, H3, E_body, 'ABB. 3')}
{panel('F', 'Die Deadline-Falle', 24, Y4, 400, H4, F_body, 'ABB. 4')}
{panel('G', 'Die Lücke zwischen Wissen und Tun', 434, Y4, 310, H4, G_body, 'ABB. 5')}
<section class="fazit" style="top:{YF}px;height:{HF}px">
 <div class="fz">FAZIT</div>
 <div class="ft"><b>ADHS heißt nicht „keine Aufmerksamkeit“.</b> Es heißt: Aufmerksamkeit, Motivation und Verhalten zuverlässig an das anzupassen, was gerade nötig ist, fällt schwer.</div>
</section>
<footer class="foot" style="top:{YFt}px">
 <div class="c" style="flex:none;width:412px"><span class="k">HINWEISE</span>Kein Hirnscan kann ADHS diagnostizieren, es gibt nur Gruppenunterschiede.<br>Die Diagnose gehört zu Fachleuten.</div>
 <div class="c" style="flex:1"><span class="k" style="letter-spacing:0">Quelle:</span>NeuroWissen TV, „NEUROLOGE ERKLÄRT: Das macht ADHS wirklich in deinem Gehirn“ (2026)</div>
</footer>
<div style="position:absolute;left:0;top:1370px;width:768px;height:6px;background:{NAVY}"></div>
</body></html>'''

with open(os.path.join(HERE, 'scientific.html'), 'w', encoding='utf-8') as f:
    f.write(html)
print('geschrieben')
