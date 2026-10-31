#!/usr/bin/env python3
"""Info-Video aus Ausschnitten einer Grafik plus Sprachausgabe.

Aufruf:
  python3 render.py szenen.json grafik.png ausgabe.mp4            # komplettes Video
  python3 render.py szenen.json grafik.png ausgabe.mp4 --nur-ton  # nur Ton, Zeitplan, Untertitel
  python3 render.py szenen.json grafik.png ausgabe.mp4 --vorschau # Kontaktbogen statt Video

Ton: je Satz eine edge-tts-Datei (zwischengespeichert in tts_cache/). Die Tonquelle ist austauschbar:
mit --ton-dir liest das Skript je Satz <szene>_<nr>.mp3/.wav aus einem Ordner (z. B. ElevenLabs-Exporte).
"""
import argparse
import hashlib
import json
import math
import os
import subprocess
import sys
import time
import wave

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, FPS, SR = 1920, 1080, 25, 24000
PAPER = (250, 243, 234)
INK = (34, 38, 50)
ACCENT = (50, 78, 122)
MUTED = (120, 114, 110)
TRACK = (232, 223, 212)
LEVELS = {
    'stark': ((52, 128, 86), 3, 'gut belegt'),
    'mittel': ((190, 136, 30), 2, 'teilweise belegt'),
    'schwach': ((206, 98, 46), 1, 'schwach belegt'),
    'keine': ((178, 52, 48), 0, 'nicht belegt'),
}
INTER = '/usr/share/fonts/opentype/inter/Inter-{}.otf'
SERIF_B = '/usr/share/fonts/truetype/crosextra/Caladea-Bold.ttf'
TX0, TX1 = 100, 760            # Textspalte links
PIC = (830, 64, 1864, 1004)    # Bildfeld rechts
GAP_SENT, GAP_SCENE, PRE, LEAD, TAIL = 0.28, 0.75, 0.6, 1.0, 2.0
XF_SCENE, XF_SHOT, FADE = 0.6, 0.5, 0.45
MAX_SCALE = 3.4

_fonts = {}


def font(path, size):
    if (path, size) not in _fonts:
        _fonts[(path, size)] = ImageFont.truetype(path, size)
    return _fonts[(path, size)]


def wrap(draw, text, fnt, width):
    lines, cur = [], ''
    for word in text.split():
        test = (cur + ' ' + word).strip()
        if draw.textlength(test, font=fnt) <= width or not cur:
            cur = test
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


# ---------------------------------------------------------------- Ton
def decode(path):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-f', 's16le', '-ac', '1', '-ar', str(SR), '-'],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768


def trim(x, thr_db=-45, margin=0.04):
    env = np.abs(x)
    thr = 10 ** (thr_db / 20) * max(env.max(), 1e-6)
    idx = np.where(env > thr)[0]
    if len(idx) == 0:
        return x
    m = int(margin * SR)
    return x[max(idx[0] - m, 0):idx[-1] + m]


def tts_edge(text, voice, rate, cache):
    key = hashlib.sha1(f'{voice}|{rate}|{text}'.encode()).hexdigest()[:16]
    mp3 = os.path.join(cache, key + '.mp3')
    if not os.path.exists(mp3):
        cmd = ['edge-tts', '--voice', voice, f'--rate={rate}', '--text', text, '--write-media', mp3 + '.tmp']
        if os.environ.get('HTTPS_PROXY'):
            cmd[1:1] = ['--proxy', os.environ['HTTPS_PROXY']]
        for attempt in range(5):
            r = subprocess.run(cmd, capture_output=True, text=True)
            if r.returncode == 0 and os.path.getsize(mp3 + '.tmp') > 1000:
                os.replace(mp3 + '.tmp', mp3)
                break
            time.sleep(2 ** attempt)
        else:
            sys.exit(f'TTS fehlgeschlagen: {text[:60]} … {r.stderr[-300:]}')
    return trim(decode(mp3))


def sentence(s):
    """Satz als (Anzeigetext, Sprechtext)."""
    return (s, s) if isinstance(s, str) else (s['t'], s.get('say', s['t']))


def build_audio(cfg, args):
    os.makedirs(args.cache, exist_ok=True)
    clips, t = [], 0.0
    for k, sc in enumerate(cfg['scenes']):
        sc['v0'] = t
        t += LEAD if k == 0 else PRE
        sc['st'] = []
        for i, s in enumerate(sc['sentences']):
            shown, say = sentence(s)
            if args.ton_dir:
                base = os.path.join(args.ton_dir, f"{sc['id']}_{i + 1:02d}")
                path = next((base + e for e in ('.wav', '.mp3', '.flac') if os.path.exists(base + e)), None)
                if not path:
                    sys.exit(f'fehlt: {base}.mp3')
                pcm = trim(decode(path))
            else:
                pcm = tts_edge(say, cfg['voice'], cfg['rate'], args.cache)
            dur = len(pcm) / SR
            sc['st'].append((t, dur, shown))
            clips.append((t, pcm))
            t += dur + GAP_SENT
        t += GAP_SCENE - GAP_SENT - PRE
    total = t + PRE + TAIL
    for k, sc in enumerate(cfg['scenes']):
        sc['v1'] = cfg['scenes'][k + 1]['v0'] if k + 1 < len(cfg['scenes']) else total
    buf = np.zeros(int(total * SR) + SR, np.float32)
    for t0, pcm in clips:
        i = int(t0 * SR)
        buf[i:i + len(pcm)] += pcm
    peak = np.abs(buf).max()
    buf = buf / peak * 0.89 if peak > 0 else buf
    return total, (buf * 32767).astype(np.int16)


def write_wav(path, pcm):
    with wave.open(path, 'wb') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())


def srt_time(t):
    ms = int(round(t * 1000))
    return f'{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}'


def write_srt(cfg, path):
    cues = []
    for sc in cfg['scenes']:
        for t0, dur, text in sc['st']:
            parts = [text]
            if len(text) > 84 and ', ' in text:          # lange Saetze am mittleren Komma teilen
                cut = min((abs(i - len(text) / 2), i) for i in range(len(text)) if text.startswith(', ', i))[1]
                parts = [text[:cut + 1], text[cut + 2:]]
            n = sum(len(p) for p in parts)
            a = t0
            for p in parts:
                b = a + dur * len(p) / n
                cues.append((a, b + 0.15, p))
                a = b
    with open(path, 'w', encoding='utf-8') as f:
        for i, (a, b, p) in enumerate(cues, 1):
            f.write(f'{i}\n{srt_time(a)} --> {srt_time(b)}\n{p}\n\n')


# ---------------------------------------------------------------- Bild
def panel_states(sc):
    """Vollbilder (ohne Grafik) fuer 0..n sichtbare Stichpunkte."""
    base = Image.new('RGB', (W, H), PAPER)
    d = ImageDraw.Draw(base)
    y = 104
    if sc.get('kicker'):
        f = font(INTER.format('SemiBold'), 25)
        d.text((TX0, y), sc['kicker'].upper(), font=f, fill=ACCENT)
        y += 52
    fh = font(SERIF_B, 64)
    for line in wrap(d, sc['headline'], fh, TX1 - TX0):
        d.text((TX0, y), line, font=fh, fill=INK)
        y += 72
    y += 18
    d.rectangle([TX0, y, TX0 + 90, y + 5], fill=ACCENT)
    y += 44
    ev = sc.get('evidence')
    if ev:
        col, dots, label = LEVELS[ev['level']]
        by = 850
        fb = font(INTER.format('SemiBold'), 25)
        txt = 'Beweislage: ' + ev.get('label', label)
        tw = d.textlength(txt, font=fb)
        bw = int(tw + 40 + 3 * 26 + 22)
        tint = tuple(int(c * 0.14 + p * 0.86) for c, p in zip(col, PAPER))
        d.rounded_rectangle([TX0, by, TX0 + bw, by + 54], radius=27, fill=tint, outline=col, width=2)
        for j in range(3):
            cx, cy = TX0 + 30 + j * 26, by + 27
            d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=col if j < dots else None, outline=col, width=2)
        d.text((TX0 + 30 + 3 * 26 + 6, by + 12), txt, font=fb, fill=col)
        if ev.get('note'):
            fn = font(INTER.format('Regular'), 22)
            yy = by + 70
            for line in wrap(d, ev['note'], fn, TX1 - TX0 + 20):
                d.text((TX0, yy), line, font=fn, fill=MUTED)
                yy += 30
    if sc.get('source'):
        fs = font(INTER.format('Regular'), 19)
        lines = wrap(d, sc['source'], fs, 1700)
        yy = H - 30 - 26 * len(lines)
        for line in lines:
            d.text((TX0, yy), line, font=fs, fill=MUTED)
            yy += 26
    states = [base]
    fb = font(INTER.format('Medium'), 34)
    for b in sc.get('bullets', []):
        img = states[-1].copy()
        d = ImageDraw.Draw(img)
        lines = wrap(d, b['t'], fb, TX1 - TX0 - 40)
        d.ellipse([TX0, y + 15, TX0 + 12, y + 27], fill=ACCENT)
        for line in lines:
            d.text((TX0 + 34, y), line, font=fb, fill=INK)
            y += 45
        y += 20
        states.append(img)
    if y > 830:
        print(f"WARNUNG {sc['id']}: Stichpunkte reichen bis y={y}, ueberlappen die Ampel")
    return states


_masks = {}


def mask(size):
    if size not in _masks:
        m = Image.new('L', size, 0)
        ImageDraw.Draw(m).rounded_rectangle([26, 26, size[0] - 27, size[1] - 27], radius=40, fill=255)
        _masks[size] = m.filter(ImageFilter.GaussianBlur(17))
    return _masks[size]


def fit_box(a, b, img_size):
    """Zielgroesse im Bildfeld und Endbox mit gleichem Seitenverhaeltnis wie a."""
    aw, ah = a[2] - a[0], a[3] - a[1]
    asp = aw / ah
    bw_max, bh_max = PIC[2] - PIC[0], PIC[3] - PIC[1]
    pw, ph = (bw_max, round(bw_max / asp)) if asp > bw_max / bh_max else (round(bh_max * asp), bh_max)
    if pw / aw > MAX_SCALE:                       # kleine Ausschnitte nicht matschig aufblasen
        pw, ph = round(aw * MAX_SCALE), round(ah * MAX_SCALE)
    if b is None:
        z = 0.92
        cx, cy = (a[0] + a[2]) / 2, (a[1] + a[3]) / 2
        b = [cx - aw * z / 2, cy - ah * z / 2, cx + aw * z / 2, cy + ah * z / 2]
    else:
        cx, cy, bw = (b[0] + b[2]) / 2, (b[1] + b[3]) / 2, b[2] - b[0]
        b = [cx - bw / 2, cy - bw / asp / 2, cx + bw / 2, cy + bw / asp / 2]
    out = []
    for box in (a, b):
        x0, y0, x1, y1 = map(float, box)
        dx = -min(x0, 0) - max(x1 - img_size[0], 0)
        dy = -min(y0, 0) - max(y1 - img_size[1], 0)
        out.append((x0 + dx, y0 + dy, x1 + dx, y1 + dy))
    return (pw, ph), out[0], out[1]


def ease(u):
    u = min(max(u, 0.0), 1.0)
    return 0.5 * u + 0.5 * (0.5 - 0.5 * math.cos(math.pi * u))


class Scene:
    def __init__(self, sc, src):
        self.sc, self.src = sc, src
        self.states = panel_states(sc)
        st = sc['st']
        self.bullet_t = []
        for b in sc.get('bullets', []):                 # gleiche Satznummer: nacheinander einblenden
            t = st[b.get('at', 0)][0] + 0.15
            if self.bullet_t and t <= self.bullet_t[-1]:
                t = self.bullet_t[-1] + 1.1
            self.bullet_t.append(t)
        self.shots = []
        for j, sh in enumerate(sc['shots']):
            t0 = sc['v0'] if j == 0 else st[sh['at']][0] - 0.35
            size, a, b = fit_box(sh['a'], sh.get('b'), src.size)
            if sh.get('zoom') == 'out':
                a, b = b, a
            self.shots.append({'t0': t0, 'size': size, 'a': a, 'b': b})
        for j, sh in enumerate(self.shots):
            sh['t1'] = self.shots[j + 1]['t0'] if j + 1 < len(self.shots) else sc['v1']

    def panel(self, t):
        n = sum(1 for bt in self.bullet_t if bt <= t)
        img = self.states[n]
        if n > 0 and t - self.bullet_t[n - 1] < FADE:
            img = Image.blend(self.states[n - 1], img, (t - self.bullet_t[n - 1]) / FADE)
        return img

    def frame_shot(self, j, t, panel):
        sh = self.shots[j]
        u = ease((t - sh['t0']) / (sh['t1'] - sh['t0'] + XF_SHOT))
        box = tuple(a + (b - a) * u for a, b in zip(sh['a'], sh['b']))
        pic = self.src.resize(sh['size'], Image.BICUBIC, box=box)
        if sh['size'][0] / (box[2] - box[0]) > 1.8:
            pic = pic.filter(ImageFilter.UnsharpMask(radius=2, percent=55, threshold=2))
        img = panel.copy()
        px = PIC[0] + (PIC[2] - PIC[0] - sh['size'][0]) // 2
        py = PIC[1] + (PIC[3] - PIC[1] - sh['size'][1]) // 2
        img.paste(pic, (px, py), mask(sh['size']))
        return img

    def frame(self, t):
        panel = self.panel(t)
        j = max(i for i, sh in enumerate(self.shots) if sh['t0'] <= t) if t >= self.shots[0]['t0'] else 0
        img = self.frame_shot(j, t, panel)
        if j + 1 < len(self.shots) and t > self.shots[j]['t1'] - XF_SHOT:
            nxt = self.frame_shot(j + 1, self.shots[j + 1]['t0'], panel)
            img = Image.blend(img, nxt, (t - (self.shots[j]['t1'] - XF_SHOT)) / XF_SHOT)
        return img


def progress(arr, t, total):
    x = int(W * min(t / total, 1))
    arr[H - 6:, :] = TRACK
    arr[H - 6:, :x] = ACCENT


def render(cfg, src, total, out_mp4, wav, srt):
    scenes = [Scene(sc, src) for sc in cfg['scenes']]
    first = {}
    n = int(math.ceil(total * FPS))
    cmd = ['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS),
           '-i', '-', '-i', wav, '-i', srt, '-map', '0:v', '-map', '1:a', '-map', '2:s',
           '-c:v', 'libx264', '-preset', 'medium', '-crf', '24', '-pix_fmt', 'yuv420p',
           '-af', 'loudnorm=I=-16:TP=-1.5:LRA=11', '-c:a', 'aac', '-b:a', '128k', '-ar', '48000',
           '-c:s', 'mov_text', '-metadata:s:s:0', 'language=ger', '-movflags', '+faststart', '-t', f'{total:.2f}', out_mp4]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    k = 0
    t_start = time.time()
    for f in range(n):
        t = f / FPS
        while k + 1 < len(scenes) and t >= scenes[k + 1].sc['v0']:
            k += 1
        img = scenes[k].frame(t)
        if k + 1 < len(scenes) and t > scenes[k].sc['v1'] - XF_SCENE:
            if k + 1 not in first:
                first[k + 1] = scenes[k + 1].frame(scenes[k + 1].sc['v0'])
            img = Image.blend(img, first[k + 1], (t - (scenes[k].sc['v1'] - XF_SCENE)) / XF_SCENE)
        if f < FPS // 2:                               # Einblenden aus Papierfarbe
            img = Image.blend(Image.new('RGB', (W, H), PAPER), img, f / (FPS // 2))
        arr = np.array(img)
        progress(arr, t, total)
        p.stdin.write(arr.tobytes())
        if f % (FPS * 30) == 0:
            print(f'  {t:6.1f} s / {total:.1f} s  ({time.time() - t_start:.0f} s Rechenzeit)', flush=True)
    p.stdin.close()
    if p.wait() != 0:
        sys.exit('ffmpeg-Fehler')


def preview(cfg, src, path):
    scenes = [Scene(sc, src) for sc in cfg['scenes']]
    thumbs = []
    for s in scenes:
        for sh in s.shots:
            t = (sh['t0'] + sh['t1']) / 2
            thumbs.append(s.frame(min(t + 30, s.sc['v1'] - XF_SCENE - 0.01) if False else t).resize((480, 270)))
    cols = 4
    rows = math.ceil(len(thumbs) / cols)
    sheet = Image.new('RGB', (cols * 490, rows * 280), 'white')
    for i, th in enumerate(thumbs):
        sheet.paste(th, ((i % cols) * 490, (i // cols) * 280))
    sheet.save(path)
    print('Kontaktbogen:', path, len(thumbs), 'Einstellungen')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('szenen')
    ap.add_argument('grafik')
    ap.add_argument('ausgabe')
    ap.add_argument('--nur-ton', action='store_true')
    ap.add_argument('--vorschau', action='store_true')
    ap.add_argument('--ton-dir')
    ap.add_argument('--bild', type=float, action='append', help='Einzelbild bei Sekunde T als PNG')
    ap.add_argument('--cache', default=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tts_cache'))
    args = ap.parse_args()
    cfg = json.load(open(args.szenen, encoding='utf-8'))
    total, pcm = build_audio(cfg, args)
    stem = os.path.splitext(args.ausgabe)[0]
    write_wav(stem + '.wav', pcm)
    write_srt(cfg, stem + '.srt')
    words = sum(len(sentence(s)[0].split()) for sc in cfg['scenes'] for s in sc['sentences'])
    speech = sum(d for sc in cfg['scenes'] for _, d, _ in sc['st'])
    print(f'Gesamtdauer {total:.1f} s ({int(total // 60)}:{int(total % 60):02d}), {words} Woerter, '
          f'Tempo {words / speech:.2f} W/s Sprechzeit')
    for sc in cfg['scenes']:
        print(f"  {sc['id']:<4} {sc['v0']:6.1f}–{sc['v1']:6.1f} s  ({sc['v1'] - sc['v0']:5.1f} s)  {sc['headline'][:50]}")
    json.dump([{k: sc[k] for k in ('id', 'v0', 'v1', 'st')} for sc in cfg['scenes']],
              open(stem + '_zeitplan.json', 'w'), ensure_ascii=False, indent=1)
    if args.nur_ton:
        return
    src = Image.open(args.grafik).convert('RGB')
    if args.bild:
        scenes = [Scene(sc, src) for sc in cfg['scenes']]
        for t in args.bild:
            k = max(i for i, sc in enumerate(cfg['scenes']) if sc['v0'] <= t)
            scenes[k].frame(t).save(f'{stem}_bild_{t:.0f}.png')
            print('Bild', t)
        return
    if args.vorschau:
        preview(cfg, src, stem + '_vorschau.png')
        return
    render(cfg, src, total, args.ausgabe, stem + '.wav', stem + '.srt')
    print('fertig:', args.ausgabe)


if __name__ == '__main__':
    main()
