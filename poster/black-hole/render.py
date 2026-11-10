#!/usr/bin/env python3
"""Anatomy of a Black Hole - Poster 67,5 x 48 cm quer, 300 dpi.

Das Bild wird physikalisch gerechnet (Schwarzschild-Metrik, Einheiten G = c = M = 1):
  * Jeder Bildpunkt ist ein Lichtstrahl. Er laeuft in einer Ebene durch das Loch, seine Bahn
    haengt nur vom Stossparameter b ab: u'' + u = 3u^2 mit u = 1/r (Bahngleichung).
  * Die Bahn wird einmal fuer ~12.000 Werte von b tabelliert (RK4), jeder Pixel schlaegt
    darin nach: wo kreuzt der Strahl die Scheibenebene (1., 2., 3. Mal), wo entkommt er.
  * Scheibe: duenn, leicht aufgefaechert (mehrere gekippte Lagen), Keplerrotation mit
    Doppler- und Gravitations-Rotverschiebung g = sqrt(1-3/r)/(1-Omega*lambda), abgeschwaecht.
  * Sternhimmel wird ueber die Fluchtrichtung der Strahlen gelinst.

Aufruf:
  python3 render.py --preview            # kleine Vorschau (1400 px breit)
  python3 render.py                      # Druckfassung 7972 x 5669 px + 3 mm Beschnitt
"""
import argparse
import math
import os
import time
from multiprocessing import Pool

import numpy as np
from scipy import ndimage

HERE = os.path.dirname(os.path.abspath(__file__))
B_C = math.sqrt(27.0)

# ------------------------------------------------------------------ Format
DPI = 300
TRIM_W, TRIM_H = 7972, 5669           # 675 x 480 mm bei 300 dpi
BLEED = 36                            # 3,05 mm je Seite
FULL_W, FULL_H = TRIM_W + 2 * BLEED, TRIM_H + 2 * BLEED

# ------------------------------------------------------------------ Szene
CAM = dict(
    r0=300.0,          # Abstand Kamera - Loch (in M)
    incl=87.0,         # Winkel Sichtlinie zur Scheibennormalen (90 = genau seitlich)
    roll=29.0,         # Drehung im Bild: Scheibe steigt nach rechts an
    cx=0.502,          # Lage des Lochs im beschnittenen Format (Anteil Breite)
    cy=0.545,          # (Anteil Hoehe, von oben)
    shadow_r=0.075,    # Schattenradius als Anteil der Breite
)
DISK = dict(
    r_in=3.8, r_out=30.0,  # Emission reicht bis nahe an den Photonenring (wie bei schneller Rotation)
    spin=+1,           # Drehsinn: +1 = linke Seite kommt auf uns zu (heller)
    beam=2.2,          # Exponent der Doppler-Aufhellung (Physik: 3-4; abgeschwaecht)
    tshift=0.7,
    src=24.0,          # Quellfunktion (Helligkeit der leuchtenden Schicht)
    tau_e=0.035,       # optische Tiefe der Leuchtschicht senkrecht (wird durch cos(theta) geteilt)
    tau_d=0.08,        # Staub aussen (macht das Band von der Seite deckend)       # wie stark g die Farbtemperatur verschiebt
    layers=[(0.0, 0.0), (1.9, 0.0), (-1.9, 0.0), (3.8, 15.0), (-3.8, 15.0), (3.2, 100.0), (-3.2, 100.0)],  # (Kippung Grad, Achse Grad)
)


# ================================================================== Bahntabelle
def b_grid(bmax):
    parts = [np.geomspace(2e-3, 4.0, 700, endpoint=False),
             np.arange(4.0, B_C - 0.06, 0.001),
             np.arange(B_C - 0.06, B_C + 0.06, 0.00004),
             np.arange(B_C + 0.06, 8.0, 0.001),
             np.arange(8.0, 20.0, 0.004),
             np.arange(20.0, bmax, 0.02)]
    return np.concatenate(parts)


def integrate(bs, r0, dphi=0.002, sub=4, phi_store=3 * np.pi + 0.3, phi_int=7 * np.pi):
    """u(phi) fuer alle b. Rueckgabe: U[b, phi] (NaN nach Einfang/Flucht), phi_end, kind."""
    u0 = 1.0 / r0
    w0 = np.sqrt(np.maximum(1.0 / bs ** 2 - u0 ** 2 * (1 - 2 * u0), 0.0))
    u = np.full(bs.shape, u0)
    w = w0.copy()
    alive = np.ones(bs.shape, bool)
    nstore = int(phi_store / dphi) + 2
    U = np.full((len(bs), nstore), np.nan, np.float32)
    U[:, 0] = u0
    phi_end = np.full(bs.shape, np.inf)
    kind = np.zeros(bs.shape, np.int8)            # 1 = eingefangen, 2 = entkommen
    h = dphi / sub
    f = lambda uu: -uu + 3.0 * uu * uu
    nsteps = int(phi_int / h)
    for i in range(1, nsteps + 1):
        k1u, k1w = w, f(u)
        k2u, k2w = w + 0.5 * h * k1w, f(u + 0.5 * h * k1u)
        k3u, k3w = w + 0.5 * h * k2w, f(u + 0.5 * h * k2u)
        k4u, k4w = w + h * k3w, f(u + h * k3u)
        un = u + h / 6 * (k1u + 2 * k2u + 2 * k3u + k4u)
        wn = w + h / 6 * (k1w + 2 * k2w + 2 * k3w + k4w)
        phi0 = (i - 1) * h
        cap = alive & (un >= 0.5)
        esc = alive & (un <= 0.0)
        if cap.any():
            phi_end[cap] = phi0 + h * (0.5 - u[cap]) / (un[cap] - u[cap])
            kind[cap] = 1
        if esc.any():
            phi_end[esc] = phi0 + h * u[esc] / (u[esc] - un[esc])
            kind[esc] = 2
        alive &= ~(cap | esc)
        u = np.where(alive, un, u)
        w = np.where(alive, wn, w)
        if i % sub == 0:
            j = i // sub
            if j < nstore:
                U[:, j] = np.where(alive, u, np.nan)
        if not alive.any():
            break
    return U, phi_end, kind


# ================================================================== Texturen
def gaussian_field(shape, ks_scale, kp_scale, beta, seed):
    """Anisotrope Zufallsflaeche (periodisch) in (s = ln r, psi)."""
    rng = np.random.default_rng(seed)
    ns, npsi = shape
    ks = np.fft.fftfreq(ns, d=1.0 / ns)[:, None] * ks_scale
    kp = np.fft.rfftfreq(npsi, d=1.0 / npsi)[None, :] * kp_scale
    k2 = ks ** 2 + kp ** 2 + 1.0
    amp = k2 ** (-beta / 2)
    noise = rng.standard_normal((ns, npsi // 2 + 1)) + 1j * rng.standard_normal((ns, npsi // 2 + 1))
    field = np.fft.irfft2(noise * amp, s=shape)
    field -= field.mean()
    field /= field.std()
    return field.astype(np.float32)


S_MIN, S_MAX = math.log(5.0), math.log(95.0)


def make_disk_texture(ns=2048, npsi=8192, seed=7):
    fine = gaussian_field((ns, npsi), 1.0, 22.0, 1.05, seed)        # feine, lange Faeden
    mid = gaussian_field((ns, npsi), 0.6, 8.0, 1.35, seed + 1)       # mittlere Baender
    env = gaussian_field((ns, npsi), 1.0, 3.0, 1.6, seed + 2)        # Huelle: zerreisst die Faeden
    clump = gaussian_field((ns, npsi), 1.0, 1.3, 1.25, seed + 3)     # Wolken und Flocken
    wa = gaussian_field((ns, npsi), 1.0, 2.0, 1.8, seed + 4)
    wb = gaussian_field((ns, npsi), 1.0, 2.0, 1.8, seed + 5)
    ii, jj = np.mgrid[0:ns, 0:npsi].astype(np.float32)
    coords = [ii + 7.0 * wa, jj + 45.0 * wb]                          # Faeden wellig verbiegen
    del ii, jj, wa, wb
    streak = (0.75 * ndimage.map_coordinates(fine, coords, order=1, mode='grid-wrap')
              + 0.55 * ndimage.map_coordinates(mid, coords, order=1, mode='grid-wrap'))
    del fine, mid, coords
    streak /= streak.std()
    soft = ndimage.gaussian_filter(streak, (8, 40), mode='wrap')      # weich: fuer die gelinsten Ringe
    soft /= soft.std()
    return np.stack([streak.astype(np.float32), env, clump, soft.astype(np.float32)])


def sample_tex(tex, s, psi):
    ns, npsi = tex.shape[1:]
    cs = (s - S_MIN) / (S_MAX - S_MIN) * (ns - 1)
    cp = (psi % (2 * np.pi)) / (2 * np.pi) * npsi
    coords = np.stack([cs, cp])
    out = [ndimage.map_coordinates(tex[c], coords, order=1, mode='grid-wrap') for c in range(tex.shape[0])]
    return out


RAMP_X = np.array([0.0, 0.18, 0.38, 0.58, 0.78, 1.0])
RAMP_C = np.array([[0.030, 0.012, 0.006],
                   [0.22, 0.085, 0.035],
                   [0.56, 0.26, 0.12],
                   [0.86, 0.56, 0.37],
                   [0.97, 0.86, 0.76],
                   [1.00, 0.98, 0.96]])


def ramp(h):
    h = np.clip(h, 0, 1)
    return np.stack([np.interp(h, RAMP_X, RAMP_C[:, c]) for c in range(3)], -1)


# ================================================================== Kamera
def rot(axis, ang):
    axis = np.asarray(axis, float) / np.linalg.norm(axis)
    a = math.radians(ang)
    K = np.array([[0, -axis[2], axis[1]], [axis[2], 0, -axis[0]], [-axis[1], axis[0], 0]])
    return np.eye(3) + math.sin(a) * K + (1 - math.cos(a)) * K @ K


def camera(W, H, off_x, off_y, trim_w, trim_h):
    i = math.radians(CAM['incl'])
    O = np.array([0.0, -math.sin(i), math.cos(i)])
    f = -O
    z = np.array([0.0, 0.0, 1.0])
    up = z - (z @ f) * f
    up /= np.linalg.norm(up)
    right = np.cross(f, up)
    r0 = CAM['r0']
    sin_sh = B_C * math.sqrt(1 - 2 / r0) / r0
    k = math.tan(math.asin(sin_sh)) / (CAM['shadow_r'] * trim_w)    # tan pro Pixel
    cx = off_x + CAM['cx'] * trim_w
    cy = off_y + CAM['cy'] * trim_h
    return dict(O=O, f=f, up=up, right=right, k=k, cx=cx, cy=cy, r0=r0,
                roll=math.radians(CAM['roll']))


# ================================================================== Pixel-Raytracing
G = {}


def init_worker(state):
    G.update(state)


def interp_b(b):
    bs = G['bs']
    ib = np.clip(np.searchsorted(bs, b) - 1, 0, len(bs) - 2)
    tb = (b - bs[ib]) / (bs[ib + 1] - bs[ib])
    return ib, np.clip(tb, 0, 1)


def lookup_u(ib, tb, phi):
    U = G['U']
    dphi = G['dphi']
    fp = phi / dphi
    ip = np.floor(fp).astype(np.int64)
    ok = (ip >= 0) & (ip < U.shape[1] - 1)
    ip = np.clip(ip, 0, U.shape[1] - 2)
    tp = fp - ip
    u = ((1 - tb) * (1 - tp) * U[ib, ip] + (1 - tb) * tp * U[ib, ip + 1]
         + tb * (1 - tp) * U[ib + 1, ip] + tb * tp * U[ib + 1, ip + 1])
    u = np.where(ok, u, np.nan)
    return u


def trace_rows(job):
    y0, y1 = job
    cam, W = G['cam'], G['W']
    py, px = np.mgrid[y0:y1, 0:W].astype(np.float64)
    px = px.ravel() + 0.5
    py = py.ravel() + 0.5
    X = px - cam['cx']
    Y = cam['cy'] - py
    cr, sr = math.cos(cam['roll']), math.sin(cam['roll'])
    Xc = X * cr + Y * sr
    Yc = -X * sr + Y * cr
    k = cam['k']
    d = (cam['f'][None, :] + (k * Xc)[:, None] * cam['right'][None, :] + (k * Yc)[:, None] * cam['up'][None, :])
    d /= np.linalg.norm(d, axis=1, keepdims=True)
    e1 = cam['O']
    cosa = -(d @ e1)
    sina = np.sqrt(np.maximum(1 - cosa ** 2, 1e-30))
    e2 = (d + cosa[:, None] * e1[None, :]) / sina[:, None]
    r0 = cam['r0']
    b = r0 * sina / math.sqrt(1 - 2 / r0)
    ib, tb = interp_b(b)
    # Drehimpuls des (echten, umgekehrt laufenden) Photons um z, pro Energie
    L = np.cross(np.broadcast_to(e1, e2.shape), e2)
    lam = -b * L[:, 2]

    n = len(b)
    col = np.zeros((n, 3), np.float32)
    T = np.ones(n, np.float32)
    dk = G['disk']
    tex = G['tex']
    spin = dk['spin']
    for kk in range(3):
        for li, nrm in enumerate(G['normals']):
            a = float(e1 @ nrm)
            c = e2 @ nrm
            phi = np.mod(np.arctan2(a, -c), np.pi) + kk * np.pi
            u = lookup_u(ib, tb, phi)
            r = 1.0 / u
            hit = np.isfinite(r) & (r > dk['r_in'] * 0.92) & (r < dk['r_out'] * 1.25)
            if not hit.any():
                continue
            idx = np.nonzero(hit)[0]
            rr = r[idx]
            ph = phi[idx]
            P = rr[:, None] * (np.cos(ph)[:, None] * e1[None, :] + np.sin(ph)[:, None] * e2[idx])
            phid = np.arctan2(P[:, 1], P[:, 0])
            s = np.log(rr)
            # Keplersche Scherung -> nachlaufende Spiralstreifen
            psi = spin * phid + 1.9 * s + li * 1.37
            st, ev, cl, sm = sample_tex(tex, s + li * 0.031, psi)
            if kk >= 1:   # gelinste Ringe: weichere, rauchige Struktur statt feiner Kreislinien
                st = 0.3 * st + 0.85 * sm
            near = np.clip(-P[:, 1] / rr, 0, 1)        # 1 = Vorderseite (zur Kamera)
            x6 = 6.0 / rr
            # Neigung des Strahls gegen die Scheibe beim Durchstoss (geschlossen aus der Bahngleichung):
            # cos(theta) = sqrt(a^2 + c^2) / sqrt(r^2/b^2 + 2/r)  ->  Lichtweg durch die Schicht ~ 1/cos
            cth = np.sqrt(a * a + c[idx] ** 2) / np.sqrt(rr ** 2 / b[idx] ** 2 + 2.0 / rr)
            cth = np.clip(cth, 0.035, 1.0)
            edge = np.clip((rr - dk['r_in']) / 2.0, 0, 1)
            edge = edge * edge * (3 - 2 * edge)
            # Doppler + Gravitation
            Om = spin * rr ** -1.5
            g = np.sqrt(np.clip(1 - 3 / rr, 1e-4, None)) / np.maximum(1 - Om * lam[idx], 0.05)
            # Dichte / Struktur
            fade = np.exp(-(rr / (dk['r_out'] * np.clip(1 + 0.22 * cl, 0.4, None))) ** 2.5)    # ausgefranster Rand
            if li == 0:
                dens = 1 / (1 + np.exp(-(2.7 * st * (0.65 + 0.35 * np.tanh(ev)) + 0.9 * cl + 0.15)))
            else:   # gekippte Lagen: nur Flocken -> Volumen an den Kanten
                dens = 1 / (1 + np.exp(-(2.8 * cl + 1.2 * st - 2.0 + (2.4 * near if kk == 0 else 0.0))))
            prof = edge * x6 ** 2.4 * fade + 0.07 * edge * fade
            heat = np.clip(0.10 + 1.05 * x6 ** 0.9, 0, 1.2) * (0.42 + 0.72 * dens)
            heat = heat * g ** dk['tshift']
            S = dk['src'] * prof * (0.08 + 1.5 * dens ** 2.0) * g ** dk['beam']     # Quellfunktion
            if kk >= 1:
                S *= 0.45
                patch = 1 / (1 + np.exp(-(3.6 * cl + 2.0 * ev - 0.4)))          # rauchige Luecken
                kres = np.clip((b[idx] / B_C - 1.05) / 0.30, 0, 1)               # Kernschatten unter dem Band
                kres = kres * kres * (3 - 2 * kres)
                S *= (0.12 + 1.3 * patch) * (0.12 + 0.88 * kres)
            if li > 0:
                S *= 0.8
            if kk == 0:   # Vorderseite: wir sehen auf die kuehlere, staubige Oberkante -> Rostbraun
                front = np.clip(-P[:, 1] / rr, 0, 1) ** 2
                S *= 1 - 0.72 * front
                heat *= 1 - 0.38 * front
            # Optisch duenne Schicht: Tiefe waechst mit dem Lichtweg 1/cos(theta).
            # Seitlich (Band) langer Weg -> hell und deckend; steil (gelinster Halo, unterer Ring) -> zart.
            inner = 0.4 + 0.6 * np.clip((rr - 5.0) / 6, 0, 1)
            tau_e = dk['tau_e'] * (0.2 + dens ** 1.3) * inner * fade ** 0.5 / cth
            tau_d = dk['tau_d'] * dens ** 1.2 * np.clip((rr - 8.0) / 10, 0, 1) * fade ** 0.5 / cth   # Staub aussen
            if li > 0:
                tau_e *= 0.7
                tau_d *= 0.7
            if kk == 0:   # Vorderseite dick und staubig: deckt den Schatten als rostbraunes Band ab
                tau_d = tau_d * (1 + 3.0 * near) + 0.06 * near * dens / cth
                if li > 0:
                    S *= 1 - 0.5 * near
            emit = (S * (1 - np.exp(-tau_e))).astype(np.float32)
            alpha = (1 - np.exp(-(tau_e + tau_d))).astype(np.float32)
            em = ramp(heat) * emit[:, None]
            Ti = T[idx]
            col[idx] += Ti[:, None] * em.astype(np.float32)
            T[idx] = Ti * (1 - alpha)

    # Hintergrund nur dort, wo der Strahl entkommt (nicht eingefangen)
    kd = G['kind']
    esc = (kd[ib] == 2) & (kd[ib + 1] == 2)
    T_bg = np.where(esc, T, 0).astype(np.float32)
    col = np.nan_to_num(col, nan=0.0, posinf=0.0, neginf=0.0)   # ein NaN wuerde der Bloom zum Quadrat verschmieren
    shape = (y1 - y0, W)
    return y0, col.reshape(shape + (3,)), T_bg.reshape(shape), b.astype(np.float32).reshape(shape)


# ================================================================== Hintergrund
def star_layer(W, H, scale, seed=3):
    rng = np.random.default_rng(seed)
    img = np.zeros((H, W, 3), np.float32)
    area = W * H / (scale ** 2)
    n = int(area * 0.00035)
    xs = rng.uniform(0, W, n)
    ys = rng.uniform(0, H, n)
    mag = rng.pareto(1.6, n) + 1.0
    peak = np.minimum(0.035 * mag, 1.8)                       # Spitzenhelligkeit in der Druckfassung
    temp = rng.uniform(0, 1, n)
    tint = np.stack([1.0 + 0.10 * (temp - 0.5) * -1, np.ones(n), 1.0 + 0.25 * (temp - 0.5)], -1)
    sig_full = 1.05 + 0.32 * np.sqrt(np.minimum(mag, 40))     # 0,1 ... 0,25 mm
    flux = peak * 2 * math.pi * sig_full ** 2 * scale ** 2    # Lichtmenge flaechentreu
    sig = np.maximum(sig_full * scale, 0.45)
    for x, y, fl, s, t in zip(xs, ys, flux, sig, tint):
        R = int(math.ceil(3 * s)) + 1
        x0, x1 = max(int(x) - R, 0), min(int(x) + R + 1, W)
        y0, y1 = max(int(y) - R, 0), min(int(y) + R + 1, H)
        if x0 >= x1 or y0 >= y1:
            continue
        gx = np.arange(x0, x1) + 0.5 - x
        gy = np.arange(y0, y1) + 0.5 - y
        kern = np.exp(-(gy[:, None] ** 2 + gx[None, :] ** 2) / (2 * s * s))
        img[y0:y1, x0:x1] += (fl / (2 * math.pi * s * s) * kern)[..., None] * t[None, None, :]
    return img


def smooth_noise(W, H, cell, seed):
    rng = np.random.default_rng(seed)
    gw, gh = max(W // cell + 3, 4), max(H // cell + 3, 4)
    g = rng.standard_normal((gh, gw)).astype(np.float32)
    g = ndimage.gaussian_filter(g, 1.0, mode='wrap')
    yy = np.linspace(1, gh - 2, H, dtype=np.float32)
    xx = np.linspace(1, gw - 2, W, dtype=np.float32)
    YY, XX = np.meshgrid(yy, xx, indexing='ij')
    out = ndimage.map_coordinates(g, [YY, XX], order=3, mode='wrap')
    return out / (out.std() + 1e-6)


def blur_ds(img, sigma_full, ds):
    """Gausssche Unschaerfe ueber verkleinertes Bild (schnell fuer grosse Radien)."""
    H, W = img.shape[:2]
    small = img[:H - H % ds, :W - W % ds].reshape(H // ds, ds, W // ds, ds, -1).mean((1, 3))
    small = ndimage.gaussian_filter(small, (sigma_full / ds, sigma_full / ds, 0))
    zy = H / small.shape[0]
    zx = W / small.shape[1]
    big = ndimage.zoom(small, (zy, zx, 1), order=1)
    out = np.zeros_like(img)
    hh, ww = min(H, big.shape[0]), min(W, big.shape[1])
    out[:hh, :ww] = big[:hh, :ww]
    return out


def aces(x):
    return np.clip((x * (2.51 * x + 0.03)) / (x * (2.43 * x + 0.59) + 0.14), 0, 1)


# ================================================================== Hauptlauf
def render(W, H, off_x, off_y, trim_w, trim_h, procs=4, rows=None):
    t0 = time.time()
    cam = camera(W, H, off_x, off_y, trim_w, trim_h)
    # groesstes noetiges b (Ecken)
    corners = []
    for (px, py) in [(0, 0), (W, 0), (0, H), (W, H)]:
        dx, dy = px - cam['cx'], py - cam['cy']
        corners.append(math.hypot(dx, dy) * cam['k'])
    bmax = cam['r0'] * math.sin(math.atan(max(corners))) / math.sqrt(1 - 2 / cam['r0']) * 1.05 + 1
    bs = b_grid(bmax)
    print(f'b-Gitter: {len(bs)} Werte bis b={bmax:.1f}', flush=True)
    U, phi_end, kind = integrate(bs, cam['r0'])
    print(f'Bahnen integriert: {time.time() - t0:.1f}s, Tabelle {U.nbytes / 1e6:.0f} MB', flush=True)
    tex = make_disk_texture()
    print(f'Textur: {time.time() - t0:.1f}s', flush=True)
    normals = []
    for tilt, ax in DISK['layers']:
        a = math.radians(ax)
        R = rot([math.cos(a), math.sin(a), 0.0], tilt)
        normals.append(R @ np.array([0.0, 0.0, 1.0]))
    state = dict(U=U, bs=bs, phi_end=phi_end, kind=kind, dphi=0.002, cam=cam, W=W,
                 tex=tex, disk=DISK, normals=normals)
    step = rows or max(8, int(2_000_000 / W))
    jobs = [(y, min(y + step, H)) for y in range(0, H, step)]
    col = np.zeros((H, W, 3), np.float32)
    Tb = np.zeros((H, W), np.float32)
    bmap = np.zeros((H, W), np.float32)
    init_worker(state)
    with Pool(procs, initializer=init_worker, initargs=(state,)) as pool:
        for n_done, (y0, c, t, bb) in enumerate(pool.imap_unordered(trace_rows, jobs), 1):
            y1 = y0 + c.shape[0]
            col[y0:y1] = c
            Tb[y0:y1] = t
            bmap[y0:y1] = bb
            if n_done % max(1, len(jobs) // 10) == 0:
                print(f'  Strahlen {n_done}/{len(jobs)}  {time.time() - t0:.0f}s', flush=True)
    print(f'Raytracing fertig: {time.time() - t0:.1f}s', flush=True)
    return dict(col=col, Tb=Tb, b=bmap, cam=cam)


def compose(R, W, H, scale):
    cam = R['cam']
    col, Tb = R['col'], R['Tb']
    # --- Sterne (gelinst)
    stars = star_layer(W, H, scale)
    lens = stars   # ungelinst: im Bildausschnitt laege sonst alles im Einstein-Ring (Sternspuren)
    # --- Nebel / Grundton (nicht gelinst, weich)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    dx = (xx - cam['cx']) / W
    dy = (yy - cam['cy']) / W
    rad = np.sqrt(dx * dx + dy * dy)
    n1 = smooth_noise(W, H, max(W // 6, 4), 11)
    n2 = smooth_noise(W, H, max(W // 18, 4), 12)
    base = np.array([0.0105, 0.0072, 0.0058], np.float32)
    neb = (1 + 0.22 * n1 + 0.10 * n2)[..., None] * base
    neb += (np.exp(-(rad / 0.30) ** 2) * 0.020)[..., None] * np.array([1.0, 0.62, 0.38], np.float32)
    # --- Jet: entlang der projizierten Scheibennormalen (Bild-oben vor Drehung -> nach links oben)
    ang = math.radians(90 + CAM['roll'])
    jx, jy = math.cos(ang), -math.sin(ang)           # Bildkoordinaten (y nach unten)
    along = (xx - cam['cx']) * jx + (yy - cam['cy']) * jy
    perp = -(xx - cam['cx']) * jy + (yy - cam['cy']) * jx
    sh = CAM['shadow_r'] * (W if scale == 1 else W)
    sh = CAM['shadow_r'] * R['trim_w']
    a = along / sh
    p = perp / sh
    width = 0.40 + 0.20 * np.clip(a, 0, None)          # weicher Lichtkegel (in Schattenradien)
    ramp_in = np.clip((a - 1.2) / 3.0, 0, 1)
    ramp_in = ramp_in * ramp_in * (3 - 2 * ramp_in)
    q = p / width
    var = 1 + 0.10 * smooth_noise(W, H, max(W // 25, 4), 13)
    jet = np.exp(-q * q) * ramp_in * np.exp(-a / 14.0) * var
    # Farbverlauf quer: links orange, Mitte blassgelb, rechts gruenlich (wie Streulicht in der Vorlage)
    t = np.clip((q + 1.3) / 2.6, 0, 1)
    hue = np.stack([np.interp(t, [0, 0.5, 1], [1.00, 1.00, 0.72]),
                    np.interp(t, [0, 0.5, 1], [0.60, 0.88, 0.95]),
                    np.interp(t, [0, 0.5, 1], [0.34, 0.68, 0.78])], -1).astype(np.float32)
    jet_rgb = (jet * 0.085)[..., None] * hue
    glow = np.exp(-(q / 2.4) ** 2) * ramp_in * np.exp(-a / 10.0) * 0.014
    jet_rgb += glow[..., None] * np.array([1.0, 0.78, 0.55], np.float32)
    del t, hue, glow
    a2 = -a
    r2 = np.clip((a2 - 1.4) / 2.5, 0, 1)
    jet2 = np.exp(-q * q) * r2 * np.exp(-a2 / 9.0) * 0.014 * var
    jet_rgb += jet2[..., None] * np.array([1.0, 0.80, 0.60], np.float32)
    del q, var
    a = None
    del xx, yy, n1, n2, along, perp, p, a2, jet, jet2, r2
    # --- Photonenring: duenne Ueberhoehung knapp ausserhalb b_c (Bilder hoeherer Ordnung)
    ring = np.exp(-((R['b'] - (B_C + 0.012)) / 0.010) ** 2)
    ring_rgb = (ring * 0.6)[..., None] * np.array([1.0, 0.86, 0.70], np.float32)
    bg = neb + lens * 1.0 + jet_rgb + ring_rgb
    hdr = col + Tb[..., None] * bg
    del lens, neb, jet_rgb, bg, ring_rgb, ring
    # --- Bloom
    lum = hdr.mean(-1, keepdims=True)
    bright = hdr * np.clip((lum - 0.15) / 0.6, 0, 1)
    glow = (0.22 * blur_ds(bright, 6 * scale, max(2, int(4 * scale) // 1)) +
            0.18 * blur_ds(bright, 30 * scale, max(2, int(8 * scale))) +
            0.14 * blur_ds(bright, 120 * scale, max(2, int(16 * scale))))
    hdr = hdr + glow
    del glow, bright
    # --- Tonemapping und Gradation
    exposure = 1.3
    out = aces(hdr * exposure)
    out = np.power(out, 1 / 2.2)
    # matter und blasser wie die Vorlage: Saettigung -25 %, Tiefen leicht angehoben, Lichter gedaempft
    luma = (out @ np.array([0.2126, 0.7152, 0.0722], np.float32))[..., None]
    out = luma + 0.75 * (out - luma)
    out = 0.014 + 0.95 * out
    del luma
    # Vignette
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    v = ((xx / W - 0.5) ** 2 + (yy / H - 0.5) ** 2 * 0.7)
    out *= (1 - 0.45 * v)[..., None]
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--preview', action='store_true')
    ap.add_argument('--width', type=int, default=1400)
    ap.add_argument('--out', default=os.path.join(HERE, 'out'))
    ap.add_argument('--procs', type=int, default=4)
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    if args.preview:
        scale = args.width / TRIM_W
    else:
        scale = 1.0
    trim_w = int(round(TRIM_W * scale))
    trim_h = int(round(TRIM_H * scale))
    bleed = int(round(BLEED * scale))
    W, H = trim_w + 2 * bleed, trim_h + 2 * bleed
    print(f'Format {W}x{H} (beschnitten {trim_w}x{trim_h}), Massstab {scale:.3f}', flush=True)
    R = render(W, H, bleed, bleed, trim_w, trim_h, procs=args.procs)
    R['trim_w'] = trim_w
    img = compose(R, W, H, scale)
    t = (np.clip(img, 0, 1) * 65535 + 0.5).astype(np.uint16)
    tag = 'preview' if args.preview else 'full'
    np.save(os.path.join(args.out, f'render_{tag}.npy'), t)
    meta = dict(W=W, H=H, bleed=bleed, trim_w=trim_w, trim_h=trim_h, scale=scale,
                cx=R['cam']['cx'], cy=R['cam']['cy'], shadow_r=CAM['shadow_r'])
    import json
    with open(os.path.join(args.out, f'render_{tag}.json'), 'w') as fh:
        json.dump(meta, fh)
    from PIL import Image
    Image.fromarray((np.clip(img, 0, 1) * 255 + 0.5).astype(np.uint8)).save(
        os.path.join(args.out, f'render_{tag}.png'))
    print('fertig', flush=True)


if __name__ == '__main__':
    main()
