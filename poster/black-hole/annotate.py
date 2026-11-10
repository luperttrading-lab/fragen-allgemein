#!/usr/bin/env python3
"""Beschriftung fuer das Black-Hole-Poster: Titel, fuenf Etiketten mit Fuehrungslinien.

Aufruf:
  python3 annotate.py --tag preview --variant korrigiert
  python3 annotate.py --tag full --variant korrigiert      # Druckfassung (JPEG + PDF, mit/ohne Beschnitt)
  python3 annotate.py --tag full --variant original

Koordinaten sind Anteile des beschnittenen Formats (x von links, y von oben).
"""
import argparse
import json
import math
import os
import urllib.request

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(HERE, 'fonts')
SAIRA = 'Saira[wdth,wght].ttf'
SAIRA_URL = 'https://raw.githubusercontent.com/google/fonts/main/ofl/saira/Saira%5Bwdth,wght%5D.ttf'

TEXTS = {
    'korrigiert': {
        'jets': ['POWERFUL BEAMS OF PLASMA BLASTED OUTWARD',
                 'FROM THE POLES AT NEARLY THE SPEED OF LIGHT,',
                 'DRIVEN BY INTENSE MAGNETIC FIELDS'],
        'photon': ['A THIN RING OF LIGHT AT 1.5 TIMES THE HORIZON',
                   'RADIUS, WHERE GRAVITY BENDS PHOTONS INTO',
                   'ORBIT AROUND THE BLACK HOLE'],
        'disc': ['SUPERHEATED GAS SPIRALING INWARD. THE ARC',
                 'OVER THE TOP IS THE FAR SIDE OF THE DISC,',
                 'BENT INTO VIEW BY GRAVITY'],
        'horizon': ['THE POINT OF NO RETURN: ONCE ANYTHING - EVEN',
                    'LIGHT - CROSSES IT, IT CANNOT ESCAPE. THE BLACK',
                    'DISC IS ITS SHADOW, ABOUT 2.6 TIMES LARGER'],
        'sing': ['THE CENTER, WHERE GENERAL RELATIVITY PREDICTS',
                 'INFINITE DENSITY - AND WHERE THE KNOWN LAWS',
                 'OF PHYSICS BREAK DOWN'],
    },
    'original': {
        'jets': ['POWERFUL BEAMS OF PLASMA BLASTED OUTWARD',
                 'FROM THE POLES AT NEARLY THE SPEED OF LIGHT,',
                 'DRIVEN BY INTENSE MAGNETIC FIELDS'],
        'photon': ['A THIN ZONE JUST ABOVE THE EVENT HORIZON WHERE',
                   'GRAVITY IS SO STRONG THAT PHOTONS ARE FORCED',
                   'TO ORBIT THE BLACK HOLE'],
        'disc': ['THIN ROTATING SUPERHEATED GAS',
                 'AND DUST SPIRALING INWARD'],
        'horizon': ['THE BOUNDARY OF THE "POINT OF NO RETURN."',
                    'ONCE ANYTHING - INCLUDING LIGHT - CROSSES THIS',
                    'THRESHOLD, IT CANNOT ESCAPE'],
        'sing': ['THE ABSOLUTE CENTER WHERE ALL MATTER IS',
                 'CRUSHED TO INFINITE DENSITY, AND THE KNOWN',
                 'LAWS OF PHYSICS BREAK DOWN'],
    },
}
HEADS = {'jets': 'RELATIVISTIC JETS', 'photon': 'PHOTON RING', 'disc': 'ACCRETION DISC',
         'horizon': 'EVENT HORIZON', 'sing': 'SINGULARITY'}


def font(size, wght, wdth):
    path = os.path.join(FONT_DIR, SAIRA)
    if not os.path.exists(path):
        os.makedirs(FONT_DIR, exist_ok=True)
        urllib.request.urlretrieve(SAIRA_URL, path)
    f = ImageFont.truetype(path, int(round(size)))
    f.set_variation_by_axes([wght, wdth])
    return f


def tracked_width(draw, text, f, track):
    w = 0.0
    for i, ch in enumerate(text):
        w += draw.textlength(ch, font=f)
        if i < len(text) - 1:
            w += track
    return w


def draw_tracked(draw, xy, text, f, track, fill=255, anchor_x='left'):
    x, y = xy
    if anchor_x == 'center':
        x -= tracked_width(draw, text, f, track) / 2
    for ch in text:
        draw.text((x, y), ch, font=f, fill=fill, anchor='ls')   # y = Grundlinie
        x += draw.textlength(ch, font=f) + track
    return x


def layout(meta, bh):
    """Etiketten: Kopf (x, y Grundlinie), Linie (Start -> Ziel). Ziel aus Lage des Lochs."""
    cx, cy, rs = bh['cx'], bh['cy'], bh['rs']      # Anteile; rs als Anteil der Breite
    asp = meta['trim_w'] / meta['trim_h']

    def at(ang_deg, dist):                         # Punkt in Richtung ang (Grad, math. positiv) und dist*rs
        a = math.radians(ang_deg)
        return (cx + dist * rs * math.cos(a), cy - dist * rs * math.sin(a) * asp)

    return {
        'jets': dict(head=(0.112, 0.312), line=((0.170, 0.290), at(119, 3.0))),
        'photon': dict(head=(0.075, 0.543), line=((0.282, 0.552), at(172, 1.04))),
        'disc': dict(head=(0.789, 0.466), line=((0.842, 0.440), at(29, 3.35))),
        'horizon': dict(head=(0.684, 0.662), line=((0.700, 0.632), at(42, 0.62))),
        'sing': dict(head=(0.4215, 0.822), line=((cx, 0.792), (cx, cy + 0.004))),
    }


def annotate(img8, meta, variant):
    W, H = meta['W'], meta['H']
    s = meta['trim_w'] / 7972.0                    # Massstab relativ zur Druckfassung
    ox, oy = meta['bleed'], meta['bleed']
    tw, th = meta['trim_w'], meta['trim_h']
    P = lambda x, y: (ox + x * tw, oy + y * th)
    bh = dict(cx=(meta['cx'] - ox) / tw, cy=(meta['cy'] - oy) / th, rs=meta['shadow_r'])

    m_title = Image.new('L', (W, H), 0)
    m_head = Image.new('L', (W, H), 0)
    m_body = Image.new('L', (W, H), 0)
    m_line = Image.new('L', (W, H), 0)
    dt, dh, db, dl = (ImageDraw.Draw(m) for m in (m_title, m_head, m_body, m_line))

    # ---- Titel
    f_sub = font(132 * s, 300, 125)
    f_tit = font(318 * s, 290, 125)
    x0, y0 = P(0.5, 0.098)
    draw_tracked(dt, (x0, y0), 'ANATOMY OF A', f_sub, 0.42 * 132 * s, anchor_x='center')
    x0, y0 = P(0.5, 0.157)
    draw_tracked(dt, (x0, y0), 'BLACK HOLE', f_tit, 0.62 * 318 * s, anchor_x='center')

    # ---- Etiketten
    f_head = font(78 * s, 460, 125)
    f_body = font(46 * s, 520, 110)
    lw = max(1, int(round(2.6 * s)))
    lab = layout(meta, bh)
    texts = TEXTS[variant]
    for key, L in lab.items():
        hx, hy = P(*L['head'])
        draw_tracked(dh, (hx, hy), HEADS[key], f_head, 0.30 * 78 * s)
        for i, line in enumerate(texts[key]):
            draw_tracked(db, (hx, hy + (82 + i * 76) * s), line, f_body, 0.20 * 44 * s)
        (ax, ay), (bx, by) = L['line']
        dl.line([P(ax, ay), P(bx, by)], fill=255, width=lw)
        # kleiner Punkt am Ziel
        px, py = P(bx, by)
        rr = 5 * s
        dl.ellipse([px - rr, py - rr, px + rr, py + rr], fill=255)

    out = img8.astype(np.float32) / 255.0
    for mask, colr, op in ((m_line, (1.0, 0.97, 0.93), 0.55), (m_body, (0.93, 0.91, 0.89), 1.0),
                           (m_head, (0.97, 0.96, 0.95), 1.0), (m_title, (0.97, 0.96, 0.95), 1.0)):
        m = np.asarray(mask, np.float32)[..., None] / 255.0 * op
        out = out * (1 - m) + np.array(colr, np.float32) * m
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--tag', default='preview')
    ap.add_argument('--variant', default='korrigiert', choices=list(TEXTS))
    ap.add_argument('--out', default=os.path.join(HERE, 'out'))
    args = ap.parse_args()
    meta = json.load(open(os.path.join(args.out, f'render_{args.tag}.json')))
    arr = np.load(os.path.join(args.out, f'render_{args.tag}.npy')).astype(np.float32) / 65535.0
    rng = np.random.default_rng(1)
    # 8 bit mit Dither (gegen Stufen in dunklen Verlaeufen beim Druck)
    img8 = np.clip(arr * 255 + rng.uniform(-0.5, 0.5, arr.shape).astype(np.float32), 0, 255)
    del arr
    out = annotate(img8, meta, args.variant)
    out8 = (np.clip(out, 0, 1) * 255 + 0.5).astype(np.uint8)
    del out
    im = Image.fromarray(out8)
    b = meta['bleed']
    trim = im.crop((b, b, b + meta['trim_w'], b + meta['trim_h']))
    base = os.path.join(args.out, f'black-hole_{args.variant}_{args.tag}')
    if args.tag == 'preview':
        trim.save(base + '.png')
        print(base + '.png')
        return
    import img2pdf
    mm = lambda v: img2pdf.mm_to_pt(v)
    for name, imx in (('67.5x48cm', trim), ('mit-3mm-Beschnitt', im)):
        jpg = f'{base}_{name}.jpg'
        imx.save(jpg, quality=95, subsampling=0, dpi=(300, 300), optimize=True)
        wmm = imx.width / 300 * 25.4
        hmm = imx.height / 300 * 25.4
        with open(f'{base}_{name}.pdf', 'wb') as fh:
            fh.write(img2pdf.convert(jpg, layout_fun=img2pdf.get_fixed_dpi_layout_fun((300, 300))))
        print(jpg, f'{wmm:.1f} x {hmm:.1f} mm')


if __name__ == '__main__':
    main()
