// Sketch Note v2 – freie Komposition nach NotebookLM-Vorbild. Alle Zeichnungen mit rough.js (feste Seeds).
(function () {
  const INK = '#161616', BLUE = '#5b8fc4', BLUE2 = '#b9d2ea', BLUE3 = '#8fb4dc', RED = '#e05a5a', GRAY = '#8d8d8d', LG = '#d9d9d9', WHITE = '#ffffff';
  const svg = document.getElementById('ink');
  const NS = 'http://www.w3.org/2000/svg';
  const CUT = []; // Boxen, an denen der Rahmen unterbrochen wird
  const cutBox = (x, y, w, h) => CUT.push({ x, y, w, h });
  const rc = rough.svg(svg);
  const G = { back: byId('gBack'), fill: byId('gFill'), ink: byId('gInk'), top: byId('gTop') };
  function byId(i) { return document.getElementById(i); }
  let SEED = 11;
  const nx = () => (SEED += 7);
  const O = (o) => Object.assign({ roughness: 0.9, bowing: 0.8, stroke: INK, strokeWidth: 2, seed: nx(), disableMultiStroke: true, preserveVertices: true }, o || {});
  const add = (n, g) => { (g || G.ink).appendChild(n); return n; };
  const bx = (el) => { const r = el.getBoundingClientRect(); return { x: r.left, y: r.top, w: r.width, h: r.height, r: r.right, b: r.bottom, cx: r.left + r.width / 2, cy: r.top + r.height / 2 }; };
  // Einheitskoordinaten -> Seite
  const fit = (x0, y0, w, h, uw, uh) => {
    const s = Math.min(w / uw, h / uh), ox = x0 + (w - uw * s) / 2, oy = y0 + (h - uh * s) / 2;
    return { s, p: (x, y) => (ox + x * s).toFixed(1) + ' ' + (oy + y * s).toFixed(1), X: (x) => ox + x * s, Y: (y) => oy + y * s };
  };
  const P = (d, o, g) => add(rc.path(d, O(o)), g);
  const L = (x1, y1, x2, y2, o, g) => add(rc.line(x1, y1, x2, y2, O(o)), g);
  const C = (cx, cy, d, o, g) => add(rc.circle(cx, cy, d, O(o)), g);
  const E = (cx, cy, w, h, o, g) => add(rc.ellipse(cx, cy, w, h, O(o)), g);
  const PG = (pts, o, g) => add(rc.polygon(pts, O(o)), g);
  const CV = (pts, o, g) => add(rc.curve(pts, O(o)), g);
  // Pfad aus Einheits-Koordinaten umrechnen ("M10 20 C ..." mit Zahlenpaaren)
  const U = (f, d) => {
    const toks = d.match(/[A-Za-z]|-?\d+(?:\.\d+)?/g); let cmd = 'M', out = '', buf = [];
    const flush = () => {
      if (!buf.length) return;
      if (cmd === cmd.toUpperCase()) for (let i = 0; i < buf.length; i += 2) out += f.p(buf[i], buf[i + 1]) + ' ';
      else for (let i = 0; i < buf.length; i++) out += (buf[i] * f.s).toFixed(1) + ' ';
      buf = [];
    };
    for (const t of toks) { if (/[A-Za-z]/.test(t)) { flush(); cmd = t; out += t + ' '; } else buf.push(+t); }
    flush(); return out.trim();
  };

  // Schraffur-Schatten unter Objekten
  function shadow(cx, cy, w, h, ang) {
    add(rc.ellipse(cx, cy, w, h, O({ stroke: 'none', fill: '#4a4a4a', fillStyle: 'hachure', hachureAngle: ang == null ? -42 : ang, hachureGap: 3.4, fillWeight: 0.7, roughness: 0.7 })), G.back);
  }
  // Catmull-Rom -> dichte Polylinie
  function spline(pts, n) {
    const out = [];
    for (let i = 0; i < pts.length - 1; i++) {
      const p0 = pts[Math.max(i - 1, 0)], p1 = pts[i], p2 = pts[i + 1], p3 = pts[Math.min(i + 2, pts.length - 1)];
      for (let k = 0; k < n; k++) {
        const t = k / n, t2 = t * t, t3 = t2 * t;
        out.push([0.5 * (2 * p1[0] + (-p0[0] + p2[0]) * t + (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t2 + (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t3),
          0.5 * (2 * p1[1] + (-p0[1] + p2[1]) * t + (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t2 + (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t3)]);
      }
    }
    out.push(pts[pts.length - 1]); return out;
  }
  function head(p, ang, col, len, w) {
    const a1 = ang + Math.PI * 0.78, a2 = ang - Math.PI * 0.78;
    add(rc.linearPath([[p[0] + len * Math.cos(a1), p[1] + len * Math.sin(a1)], p, [p[0] + len * Math.cos(a2), p[1] + len * Math.sin(a2)]], O({ stroke: col, strokeWidth: w || 2.4, roughness: 0.5 })));
  }
  function arrow(pts, o) {
    o = o || {};
    const col = o.stroke || INK, w = o.w || 2, r = o.r == null ? 0.5 : o.r;
    if (pts.length === 2) { // gerade Verbinder leicht bogenförmig
      const [a, b] = pts, dx = b[0] - a[0], dy = b[1] - a[1], l = Math.hypot(dx, dy) || 1, k = (o.bow == null ? 0.09 : o.bow) * l;
      pts = [a, [(a[0] + b[0]) / 2 - dy / l * k, (a[1] + b[1]) / 2 + dx / l * k], b];
    }
    const d = spline(pts, 10), n = d.length;
    const segs = o.taper === false ? [[0, n - 1, w]] : [[0, Math.floor(n * 0.5), w], [Math.floor(n * 0.5), Math.floor(n * 0.8), w * 0.78], [Math.floor(n * 0.8), n - 1, w * 0.58]];
    segs.forEach(([i0, i1, ww]) => {
      const c = d.slice(i0, i1 + 1); if (c.length < 2) return;
      const opt = O({ stroke: col, strokeWidth: ww, roughness: r, bowing: 0.3, disableMultiStroke: !o.multi });
      if (o.dash) opt.strokeLineDash = o.dash;
      add(c.length === 2 ? rc.line(c[0][0], c[0][1], c[1][0], c[1][1], opt) : rc.curve(c, opt));
    });
    const a = d[Math.max(n - 4, 0)], b = d[n - 1];
    head(b, Math.atan2(b[1] - a[1], b[0] - a[0]), col, o.hs || 10, o.hw || w * 0.9 + 0.6);
  }
  // Strahlenstriche (blau), Mittelpunkt + Richtung
  function rays(cx, cy, ang, n, len, gap, col, w) {
    for (let i = 0; i < n; i++) {
      const a = ang + (i - (n - 1) / 2) * gap;
      L(cx + Math.cos(a) * 6, cy + Math.sin(a) * 6, cx + Math.cos(a) * (6 + len), cy + Math.sin(a) * (6 + len), { stroke: col || BLUE, strokeWidth: w || 2.6, roughness: 0.5 });
    }
  }
  function scribble(cx, cy, w, h, n, o) {
    const pts = [];
    for (let i = 0; i <= n; i++) { const t = i / n; pts.push([cx + (Math.sin(t * Math.PI * 7) * 0.5 + (t - 0.5)) * w, cy + Math.cos(t * Math.PI * 5.3 + 0.4) * h * 0.5]); }
    CV(pts, O(Object.assign({ strokeWidth: 1.6, roughness: 0.6 }, o)));
  }
  // Wolke um ein Rechteck
  function cloud(x, y, w, h, o) {
    const pts = []; const n = 14;
    for (let i = 0; i < n; i++) {
      const a = -Math.PI / 2 + i * Math.PI * 2 / n, rx = w / 2, ry = h / 2;
      pts.push([x + w / 2 + Math.cos(a) * rx, y + h / 2 + Math.sin(a) * ry]);
    }
    let d = '';
    for (let i = 0; i < n; i++) {
      const a = pts[i], b = pts[(i + 1) % n], mx = (a[0] + b[0]) / 2, my = (a[1] + b[1]) / 2;
      const cx = x + w / 2, cy = y + h / 2, dx = mx - cx, dy = my - cy, l = Math.hypot(dx, dy);
      const k = 1.22; const qx = cx + dx / l * (l * k), qy = cy + dy / l * (l * k);
      d += (i ? '' : `M${a[0]} ${a[1]} `) + `Q${qx} ${qy} ${b[0]} ${b[1]} `;
    }
    P(d + 'Z', Object.assign({ fill: WHITE, fillStyle: 'solid', strokeWidth: 2.6, roughness: 0.8 }, o), G.fill);
  }
  // Textmarker-Welle hinter einem Textelement
  function marker(el, col, dy, th) {
    const b = bx(el); const y = b.y + b.h * 0.62 + (dy || 0); const pts = [];
    for (let i = 0; i <= 8; i++) pts.push([b.x - 6 + (b.w + 12) * i / 8, y + Math.sin(i * 1.9) * 2.2]);
    add(rc.curve(pts, O({ stroke: col, strokeWidth: th || 14, roughness: 0.6, bowing: 1.5 })), G.back);
  }
  function underline(el, col, dy, th) {
    const b = bx(el); const y = b.b + (dy || 0);
    CV([[b.x - 4, y], [b.x + b.w * 0.3, y + 2], [b.x + b.w * 0.7, y - 1], [b.r + 6, y + 1]], O({ stroke: col, strokeWidth: th || 5, roughness: 0.7 }), G.back);
  }
  // Strichmännchen-Kopf mit Gesicht
  function face(cx, cy, r, mood) {
    C(cx, cy, r * 2, { fill: WHITE, fillStyle: 'solid', strokeWidth: 2.5, roughness: 0.7 }, G.fill);
    C(cx - r * 0.35, cy - r * 0.1, 2.4, { fill: INK, fillStyle: 'solid', roughness: 0.2, strokeWidth: 1 });
    C(cx + r * 0.35, cy - r * 0.1, 2.4, { fill: INK, fillStyle: 'solid', roughness: 0.2, strokeWidth: 1 });
    if (mood === 'sad') P(`M${cx - r * 0.35} ${cy + r * 0.5} Q${cx} ${cy + r * 0.25} ${cx + r * 0.35} ${cy + r * 0.5}`, { strokeWidth: 1.6, roughness: 0.3 });
    else if (mood === 'flat') L(cx - r * 0.3, cy + r * 0.45, cx + r * 0.3, cy + r * 0.45, { strokeWidth: 1.6, roughness: 0.3 });
    else if (mood === 'worry') { P(`M${cx - r * 0.35} ${cy + r * 0.5} Q${cx} ${cy + r * 0.3} ${cx + r * 0.35} ${cy + r * 0.5}`, { strokeWidth: 1.6, roughness: 0.3 }); L(cx - r * 0.55, cy - r * 0.5, cx - r * 0.2, cy - r * 0.38, { strokeWidth: 1.4, roughness: 0.3 }); L(cx + r * 0.55, cy - r * 0.5, cx + r * 0.2, cy - r * 0.38, { strokeWidth: 1.4, roughness: 0.3 }); }
    // Haarsträhnen
    P(`M${cx - r * 0.5} ${cy - r * 0.95} q${r * 0.2} ${-r * 0.35} ${r * 0.45} ${-r * 0.1} M${cx + r * 0.1} ${cy - r * 1.02} q${r * 0.25} ${-r * 0.3} ${r * 0.5} ${-r * 0.05}`, { strokeWidth: 1.5, roughness: 0.4 });
  }

  // =============== Zeichnungen ===============
  function frame() {
    const g = document.createElementNS(NS, 'g'); g.setAttribute('mask', 'url(#frameMask)'); G.back.appendChild(g);
    add(rc.rectangle(30, 28, 708, 1326, O({ stroke: BLUE3, strokeWidth: 2.4, roughness: 1.25, bowing: 1.6 })), g);
    add(rc.rectangle(34, 32, 702, 1318, O({ stroke: INK, strokeWidth: 1.9, roughness: 1.1, bowing: 1.3 })), g);
  }
  function buildMask() {
    const m = document.createElementNS(NS, 'mask'); m.id = 'frameMask'; m.setAttribute('maskUnits', 'userSpaceOnUse');
    ['x', 'y', 'width', 'height'].forEach((k, i) => m.setAttribute(k, [0, 0, 768, 1376][i]));
    const R = (x, y, w, h, c) => { const r = document.createElementNS(NS, 'rect'); r.setAttribute('x', x); r.setAttribute('y', y); r.setAttribute('width', w); r.setAttribute('height', h); r.setAttribute('fill', c); m.appendChild(r); };
    R(0, 0, 768, 1376, '#fff');
    const boxes = CUT.slice();
    // HTML-Glyphen: Tintenbox statt Zeilenbox (Versalhöhe liegt bei ~0,13 bis ~0,9 der Schriftgröße)
    document.querySelectorAll('.cut').forEach((el) => { const b = el.getBoundingClientRect(), fs = parseFloat(getComputedStyle(el).fontSize); boxes.push({ x: b.left + 2, y: b.top + fs * 0.13, w: b.width - 4, h: b.height - fs * 0.22 }); });
    boxes.forEach((b) => R(b.x - 6, b.y - 6, b.w + 12, b.h + 12, '#000'));
    svg.querySelector('defs').appendChild(m);
    window.__cutBoxes = boxes;
  }

  function ribbon(x, y, w, h, tail, opts) {
    // Schatten, Körper mit gebogener Ober-/Unterkante, Falten, Schwalbenschwanz-Enden
    const o = opts || {};
    const curve = o.curve == null ? 10 : o.curve;
    cutBox(x - tail - 2, y - curve - 2, w + 2 * tail + 4, h + curve + 16);
    const bodyD = `M${x} ${y} Q${x + w / 2} ${y - curve} ${x + w} ${y} L${x + w} ${y + h} Q${x + w / 2} ${y + h - curve} ${x} ${y + h} Z`;
    add(rc.path(`M${x + 3} ${y + 4} Q${x + w / 2 + 3} ${y - curve + 4} ${x + w + 3} ${y + 4} L${x + w + 3} ${y + h + 4} Q${x + w / 2 + 3} ${y + h - curve + 4} ${x + 3} ${y + h + 4} Z`, O({ stroke: 'none', fill: '#cfcfcf', fillStyle: 'solid', roughness: 0.6 })), G.back);
    [[-1, x], [1, x + w]].forEach(([s, ex]) => {
      const inner = ex - s * 22, outer = ex + s * tail, ty = y + 12, th = h - 4;
      add(rc.polygon([[inner, ty], [outer, ty], [outer - s * 13, ty + th / 2], [outer, ty + th], [inner, ty + th]], O({ fill: WHITE, fillStyle: 'solid', strokeWidth: 2.4, roughness: 0.8 })), G.back);
      // Falte
      add(rc.polygon([[ex, y + h - 1], [inner, y + h + 11], [inner, y + h - 1]], O({ fill: GRAY, fillStyle: 'solid', strokeWidth: 1.8, roughness: 0.5 })), G.back);
    });
    add(rc.path(bodyD, O({ fill: WHITE, fillStyle: 'solid', strokeWidth: 2.8, roughness: 0.9 })), G.back);
    // leichte Innenlinie oben als Dicke
    P(`M${x + 6} ${y + h - 7} Q${x + w / 2} ${y + h - 7 - curve} ${x + w - 6} ${y + h - 7}`, { stroke: '#bdbdbd', strokeWidth: 1.2, roughness: 0.4 }, G.back);
  }

  function bulb(x, y, w, h, o) {
    const f = fit(x, y, w, h, 80, 120); const p = f.p;
    P(`M${p(40, 20)} C${p(16, 20)} ${p(4, 40)} ${p(10, 58)} C${p(14, 70)} ${p(26, 76)} ${p(28, 88)} L${p(52, 88)} C${p(54, 76)} ${p(66, 70)} ${p(70, 58)} C${p(76, 40)} ${p(64, 20)} ${p(40, 20)} Z`, Object.assign({ fill: WHITE, fillStyle: 'solid', strokeWidth: 2.6, roughness: 0.8 }, o), G.fill);
    // Glanz-Schatten blau links
    P(`M${p(22, 42)} C${p(18, 52)} ${p(22, 64)} ${p(30, 70)}`, { stroke: BLUE2, strokeWidth: 5, roughness: 0.5 }, G.fill);
    P(`M${p(33, 88)} L${p(34, 70)} L${p(40, 62)} L${p(46, 70)} L${p(47, 88)}`, { strokeWidth: 1.5, roughness: 0.5 });
    P(`M${p(28, 94)} L${p(52, 94)} M${p(29, 101)} L${p(51, 101)} M${p(33, 108)} L${p(47, 108)}`, { strokeWidth: 2, roughness: 0.6 });
    for (let a = -150; a <= -30; a += 40) { const t = a * Math.PI / 180; L(f.X(40 + 40 * Math.cos(t)), f.Y(52 + 40 * Math.sin(t)), f.X(40 + 50 * Math.cos(t)), f.Y(52 + 50 * Math.sin(t)), { strokeWidth: 1.6, roughness: 0.4 }); }
  }
  function gear(cx, cy, r, col, teeth) {
    const n = teeth || 8, pts = [];
    for (let i = 0; i < n * 2; i++) { const a = i * Math.PI / n, rr = i % 2 ? r : r * 1.32; pts.push([cx + Math.cos(a) * rr, cy + Math.sin(a) * rr]); }
    // Zähne als Rechteckprofil
    const q = [];
    for (let i = 0; i < n; i++) {
      const a0 = i * 2 * Math.PI / n, d = Math.PI / n * 0.5;
      q.push([cx + Math.cos(a0 - d) * r, cy + Math.sin(a0 - d) * r], [cx + Math.cos(a0 - d * 0.7) * r * 1.35, cy + Math.sin(a0 - d * 0.7) * r * 1.35], [cx + Math.cos(a0 + d * 0.7) * r * 1.35, cy + Math.sin(a0 + d * 0.7) * r * 1.35], [cx + Math.cos(a0 + d) * r, cy + Math.sin(a0 + d) * r]);
    }
    cutBox(cx - r * 1.4, cy - r * 1.4, r * 2.8, r * 2.8);
    PG(q, { fill: col || '#c8c8c8', fillStyle: 'solid', strokeWidth: 2.2, roughness: 0.7 }, G.fill);
    C(cx, cy, r * 0.8, { fill: WHITE, fillStyle: 'solid', strokeWidth: 2, roughness: 0.6 }, G.fill);
  }
  function brainSmall(x, y, w, h, fillCol) {
    const f = fit(x, y, w, h, 120, 100), p = f.p;
    P(`M${p(22, 62)} C${p(8, 58)} ${p(6, 38)} ${p(20, 32)} C${p(18, 16)} ${p(36, 8)} ${p(50, 14)} C${p(58, 4)} ${p(80, 4)} ${p(88, 14)} C${p(102, 12)} ${p(116, 26)} ${p(110, 42)} C${p(120, 52)} ${p(112, 70)} ${p(98, 68)} C${p(92, 76)} ${p(80, 78)} ${p(72, 72)} C${p(62, 80)} ${p(44, 80)} ${p(38, 70)} C${p(30, 74)} ${p(20, 70)} ${p(22, 62)} Z`,
      { fill: fillCol || WHITE, fillStyle: 'solid', strokeWidth: 2.6, roughness: 0.8 }, G.fill);
    P(`M${p(90, 70)} C${p(96, 82)} ${p(108, 80)} ${p(108, 66)}`, { strokeWidth: 1.4, roughness: 0.6 });
    P(`M${p(72, 74)} C${p(74, 84)} ${p(76, 90)} ${p(80, 98)} M${p(82, 74)} C${p(84, 84)} ${p(86, 90)} ${p(90, 97)}`, { strokeWidth: 1.4, roughness: 0.6 });
    ['M34 30 C40 24 48 34 56 26', 'M62 18 C66 28 76 22 80 30', 'M86 28 C92 36 100 30 104 40', 'M28 48 C36 42 42 52 50 44', 'M56 42 C62 50 72 44 78 52', 'M84 50 C90 56 96 52 100 58', 'M46 62 C54 56 60 64 68 58']
      .forEach((d) => P(U(f, d), { strokeWidth: 1.25, roughness: 0.6 }));
    return f;
  }
  function pulse(x1, y, x2, col) {
    cutBox(x1, y - 14, x2 - x1, 28);
    const w = x2 - x1, pts = [[x1, y], [x1 + w * 0.2, y], [x1 + w * 0.28, y - 9], [x1 + w * 0.36, y + 11], [x1 + w * 0.44, y - 14], [x1 + w * 0.52, y + 8], [x1 + w * 0.6, y - 4], [x1 + w * 0.68, y], [x2, y]];
    add(rc.linearPath(pts, O({ stroke: col || BLUE, strokeWidth: 2.2, roughness: 0.5 })));
  }

  // ---- Großes Gehirn (Sagittalschnitt) ----
  function brainHero(x, y, w, h) {
    const f = fit(x, y, w, h, 260, 250), p = f.p;
    // Kleinhirn
    shadow(f.X(206), f.Y(232), 150 * f.s, 16 * f.s, -30);
    P(U(f, 'M172 170 C176 150 214 142 236 158 C252 170 248 196 230 206 C210 216 180 212 172 196 Z'), { fill: LG, fillStyle: 'solid', strokeWidth: 2.6, roughness: 0.8 }, G.fill);
    for (let i = 0; i < 5; i++) { const t = i * 7; P(U(f, `M${186 + t * 0.6} ${160 + t} C${196 + t * 0.5} ${152 + t * 1.1} ${222 + t * 0.4} ${156 + t * 1.2} ${236 - t * 0.5} ${168 + t}`), { strokeWidth: 1.3, roughness: 0.5 }); }
    P(U(f, 'M190 196 C200 190 214 190 226 198'), { strokeWidth: 1.2, roughness: 0.5 });
    // Hirnstamm
    P(U(f, 'M150 150 C142 172 144 200 148 222 C150 236 156 246 164 250 L186 250 C190 236 186 214 184 196 C182 176 182 160 186 150 Z'), { fill: '#e6e6e6', fillStyle: 'solid', strokeWidth: 2.6, roughness: 0.8 }, G.fill);
    // Pons-Wulst
    P(U(f, 'M148 178 C142 184 142 200 150 208 M184 180 C190 186 190 200 184 206'), { strokeWidth: 1.3, roughness: 0.5 });
    P(U(f, 'M154 186 C160 182 172 182 180 186 M154 198 C160 194 172 194 180 198'), { strokeWidth: 1.2, roughness: 0.5 });
    // Großhirn: Umriss abtasten und mit Gyri-Buckeln versehen
    const outline = 'M18 118 C14 80 42 36 90 22 C130 10 180 10 212 30 C244 48 258 88 250 124 C246 148 228 164 206 170 C196 176 184 172 176 164 C164 166 150 170 136 164 C118 176 92 180 62 170 C38 162 20 144 18 118 Z';
    const tmp = document.createElementNS('http://www.w3.org/2000/svg', 'path'); tmp.setAttribute('d', U(f, outline)); svg.appendChild(tmp);
    const len = tmp.getTotalLength(), N = 160, opts = [];
    for (let i = 0; i <= N; i++) {
      const t = i / N, q = tmp.getPointAtLength(t * len), q2 = tmp.getPointAtLength(((i + 1) % N) / N * len);
      const dx = q2.x - q.x, dy = q2.y - q.y, l = Math.hypot(dx, dy) || 1;
      // Buckel nur auf der Oberseite/Rückseite (erste ~62 % der Länge), unten glatt
      const amp = t < 0.62 ? 2.4 * f.s : 0.6 * f.s;
      const off = Math.sin(t * Math.PI * 2 * 26) * amp;
      opts.push([q.x + (-dy / l) * off, q.y + (dx / l) * off]);
    }
    svg.removeChild(tmp);
    PG(opts, { fill: WHITE, fillStyle: 'solid', strokeWidth: 2.9, roughness: 0.4 }, G.fill);
    // Balken (Corpus callosum)
    P(U(f, 'M60 106 C64 60 160 48 194 96 C200 106 190 114 182 108 C160 76 94 80 80 108 C76 116 60 116 60 106 Z'), { fill: '#dadada', fillStyle: 'solid', strokeWidth: 1.6, roughness: 0.6 }, G.fill);
    // Thalamus + Hypothalamus
    E(f.X(132), f.Y(124), 52 * f.s, 34 * f.s, { fill: '#cfcfcf', fillStyle: 'solid', strokeWidth: 1.5, roughness: 0.6 }, G.fill);
    P(U(f, 'M112 140 C106 150 112 160 124 158 C134 156 136 146 130 140'), { fill: '#e2e2e2', fillStyle: 'solid', strokeWidth: 1.6, roughness: 0.6 }, G.fill);
    // Furchen: fließende S-Kurven vom Rand nach innen, mit grauem Schatten im Sulcus
    const cx = 134, cy = 98, rx = 118, ry = 80;
    const sulcus = (pts, w) => { CV(pts, { stroke: '#bcbcbc', strokeWidth: w * 2.3, roughness: 0.2 }); CV(pts, { strokeWidth: w, roughness: 0.3 }); };
    for (let i = 0; i < 19; i++) {
      const a = Math.PI * 1.03 - i * (Math.PI * 1.1 / 18);
      const r0 = 0.965, r1 = [0.52, 0.66, 0.6, 0.72][i % 4];
      const pts = [];
      for (let k = 0; k <= 6; k++) {
        const t = r0 + (r1 - r0) * k / 6; const wig = Math.sin(k * 0.9 + i * 0.8) * 3.6;
        const px = cx + Math.cos(a) * rx * t - Math.sin(a) * wig, py = cy + Math.sin(a) * ry * t + Math.cos(a) * wig;
        pts.push([f.X(px), f.Y(py)]);
      }
      sulcus(pts, 1.4);
      // kurzer Seitenast
      if (i % 3 === 1) { const b = a + 0.075, t0 = 0.86, t1 = 0.72; const q = []; for (let k = 0; k <= 3; k++) { const t = t0 + (t1 - t0) * k / 3; const wig = Math.sin(k * 1.4 + i) * 2.2; q.push([f.X(cx + Math.cos(b) * rx * t - Math.sin(b) * wig), f.Y(cy + Math.sin(b) * ry * t + Math.cos(b) * wig)]); } sulcus(q, 1.2); }
    }
    // Gyrus cinguli-Bogen über dem Balken
    P(U(f, 'M56 96 C70 44 170 32 204 86'), { strokeWidth: 1.3, roughness: 0.5 });
    // Schläfenlappen-Furchen unten
    ['M40 148 C52 142 62 152 74 146', 'M80 164 C92 156 104 164 118 156', 'M28 134 C36 128 46 134 56 128'].forEach((d) => { P(U(f, d), { stroke: '#bcbcbc', strokeWidth: 3, roughness: 0.2 }); P(U(f, d), { strokeWidth: 1.3, roughness: 0.5 }); });
    // Hinterhaupt-Furchen
    ['M214 140 C224 136 230 146 240 140', 'M200 156 C210 150 220 158 230 152'].forEach((d) => { P(U(f, d), { stroke: '#bcbcbc', strokeWidth: 3, roughness: 0.2 }); P(U(f, d), { strokeWidth: 1.3, roughness: 0.5 }); });
    return f;
  }

  // ---- Synapse ----
  function synapse(x, y, w, h) {
    const f = fit(x, y, w, h, 230, 100), p = f.p;
    const bl = { fill: BLUE2, fillStyle: 'solid', stroke: BLUE, strokeWidth: 2.7, roughness: 0.8 };
    // präsynaptisch (links) – Endknopf mit konvexer Front
    P(U(f, 'M0 36 L54 34 C86 30 106 10 126 14 C140 18 146 34 142 50 C146 66 140 82 126 86 C106 90 86 68 54 64 L0 62 Z'), bl, G.fill);
    P(U(f, 'M0 40 L52 38 M0 58 L52 58'), { stroke: BLUE, strokeWidth: 1.1, roughness: 0.5 });
    // Vesikel
    C(f.X(108), f.Y(50), 26 * f.s, { fill: WHITE, fillStyle: 'solid', stroke: INK, strokeWidth: 1.4, roughness: 0.5 }, G.fill);
    [[-5, -4], [5, -3], [-3, 5], [5, 5]].forEach(([dx, dy]) => C(f.X(108 + dx), f.Y(50 + dy), 5 * f.s, { fill: INK, fillStyle: 'solid', strokeWidth: 1, roughness: 0.3 }));
    // Freisetzungs-Kerben an der Front
    P(U(f, 'M140 36 c6 2 6 8 0 10 M140 54 c6 2 6 8 0 10'), { stroke: INK, strokeWidth: 1.3, roughness: 0.4 });
    // postsynaptisch (rechts) – konkav
    P(U(f, 'M230 34 L186 32 C170 30 160 36 164 50 C160 64 170 70 186 68 L230 66 Z'), bl, G.fill);
    P(U(f, 'M184 36 c-6 4 -6 24 0 28'), { stroke: INK, strokeWidth: 1.3, roughness: 0.4 });
    // Botenstoffe im Spalt
    [[150, 40, RED], [156, 50, BLUE], [150, 60, RED], [158, 34, BLUE], [160, 64, RED]].forEach(([a, b, c]) => C(f.X(a), f.Y(b), 6 * f.s, { fill: c, fillStyle: 'solid', stroke: c, strokeWidth: 1, roughness: 0.3 }));
    // rote Strahlen über/unter dem Spalt
    rays(f.X(152), f.Y(4), -Math.PI / 2, 3, 10 * f.s, 0.5, RED, 2.2);
    rays(f.X(152), f.Y(96), Math.PI / 2, 3, 10 * f.s, 0.5, RED, 2.2);
  }

  // ---- Gehirn mit Steuerpult ----
  function brainPanel(x, y, w, h) {
    const f = brainSmall(x, y, w, h, WHITE);
    const p = f.p;
    // blauer Frontbereich
    P(U(f, 'M22 62 C8 58 6 38 20 32 C18 16 36 8 50 14 C46 30 44 50 42 70 C34 74 22 70 22 62 Z'), { fill: BLUE2, fillStyle: 'solid', stroke: 'none', roughness: 0.6 }, G.fill);
    // Panel 1: Schieberegler
    add(rc.rectangle(f.X(14), f.Y(30), 30 * f.s, 34 * f.s, O({ fill: WHITE, fillStyle: 'solid', stroke: INK, strokeWidth: 1.8, roughness: 0.5 })), G.fill);
    [20, 29, 38].forEach((sx, i) => { L(f.X(sx), f.Y(36), f.X(sx), f.Y(58), { strokeWidth: 1.4, roughness: 0.3 }); C(f.X(sx), f.Y(40 + i * 7), 5 * f.s, { fill: BLUE, fillStyle: 'solid', stroke: INK, strokeWidth: 1, roughness: 0.2 }); });
    // Panel 2: Anzeige + Knöpfe
    add(rc.rectangle(f.X(50), f.Y(26), 38 * f.s, 36 * f.s, O({ fill: WHITE, fillStyle: 'solid', stroke: INK, strokeWidth: 1.8, roughness: 0.5 })), G.fill);
    P(U(f, 'M56 46 C58 34 80 34 82 46'), { strokeWidth: 1.4, roughness: 0.3 });
    L(f.X(69), f.Y(46), f.X(76), f.Y(37), { stroke: RED, strokeWidth: 1.6, roughness: 0.2 });
    [58, 69, 80].forEach((sx) => C(f.X(sx), f.Y(55), 6 * f.s, { fill: BLUE2, fillStyle: 'solid', stroke: INK, strokeWidth: 1, roughness: 0.2 }));
    rays(f.X(26), f.Y(4), -Math.PI * 0.62, 3, 12, 0.45, BLUE, 2.4);
  }

  // ---- Strichmännchen mit Handy ----
  function phoneFigure(x, y, w, h) {
    const f = fit(x, y, w, h, 100, 160), p = f.p, X = f.X, Y = f.Y;
    face(X(44), Y(22), 16 * f.s, 'sad');
    L(X(44), Y(38), X(42), Y(104), { strokeWidth: 2.7, roughness: 0.6 });
    // linker Arm hängend
    P(U(f, 'M42 54 C30 70 22 84 22 96'), { strokeWidth: 2.4, roughness: 0.6 });
    // rechter Arm mit Handy
    P(U(f, 'M42 54 C56 62 66 68 72 72'), { strokeWidth: 2.4, roughness: 0.6 });
    const g = document.createElementNS('http://www.w3.org/2000/svg', 'g'); g.setAttribute('transform', `rotate(-28 ${X(80)} ${Y(66)})`); G.fill.appendChild(g);
    add(rc.rectangle(X(72), Y(50), 18 * f.s, 32 * f.s, O({ fill: WHITE, fillStyle: 'solid', strokeWidth: 1.6, roughness: 0.5 })), g);
    for (let r = 0; r < 4; r++) for (let c = 0; c < 2; c++) add(rc.rectangle(X(75 + c * 7), Y(54 + r * 6), 5 * f.s, 4 * f.s, O({ fill: LG, fillStyle: 'solid', strokeWidth: 0.8, roughness: 0.2 })), g);
    // Beine
    P(U(f, 'M42 104 C36 120 30 138 26 154 M42 104 C50 122 56 138 60 154'), { strokeWidth: 2.7, roughness: 0.6 });
    P(U(f, 'M26 154 L14 156 M60 154 L72 156'), { strokeWidth: 2.2, roughness: 0.5 });
    // Bodenschatten
    shadow(X(42), Y(159), 74 * f.s, 8 * f.s);
  }

  // ---- Schreibtisch-Szene ----
  function deskScene(x, y, w, h) {
    const f = fit(x, y, w, h, 220, 180), p = f.p, X = f.X, Y = f.Y;
    // Denkwolke mit Gekritzel
    cloud(X(4), Y(6), 72 * f.s, 50 * f.s, {});
    scribble(X(40), Y(31), 36 * f.s, 24 * f.s, 40, {});
    C(X(70), Y(66), 7 * f.s, { fill: WHITE, fillStyle: 'solid', strokeWidth: 1.6, roughness: 0.5 }, G.fill);
    C(X(84), Y(78), 5 * f.s, { fill: WHITE, fillStyle: 'solid', strokeWidth: 1.4, roughness: 0.5 }, G.fill);
    // Wanduhr (blau)
    C(X(176), Y(36), 46 * f.s, { fill: BLUE2, fillStyle: 'solid', stroke: BLUE, strokeWidth: 3, roughness: 0.6 }, G.fill);
    C(X(176), Y(36), 36 * f.s, { fill: WHITE, fillStyle: 'solid', stroke: INK, strokeWidth: 1.4, roughness: 0.4 }, G.fill);
    for (let a = 0; a < 12; a++) { const t = a * Math.PI / 6; L(X(176 + 15 * Math.cos(t)), Y(36 + 15 * Math.sin(t)), X(176 + 17 * Math.cos(t)), Y(36 + 17 * Math.sin(t)), { strokeWidth: 1.2, roughness: 0.2 }); }
    P(U(f, 'M176 36 L176 24 M176 36 L185 40'), { strokeWidth: 2, roughness: 0.3 });
    // Figur
    face(X(108), Y(74), 15 * f.s, 'flat');
    P(U(f, 'M108 89 L108 104 M96 104 C100 98 116 98 120 104'), { strokeWidth: 2.4, roughness: 0.5 });
    // Arme auf dem Tisch, Kinn in die Hand gestützt
    P(U(f, 'M100 104 C84 112 72 118 70 124 M116 104 C124 112 128 116 128 124'), { strokeWidth: 2.4, roughness: 0.5 });
    // Schreibtischplatte mit Dicke
    PG([[X(28), Y(124)], [X(200), Y(124)], [X(204), Y(132)], [X(24), Y(132)]], { fill: WHITE, fillStyle: 'solid', strokeWidth: 2.8, roughness: 0.8 }, G.fill);
    // Schraffur an der Plattenkante
    PG([[X(28), Y(126)], [X(200), Y(126)], [X(204), Y(132)], [X(24), Y(132)]], { stroke: 'none', fill: '#555', fillStyle: 'hachure', hachureAngle: -45, hachureGap: 3, fillWeight: 0.6, roughness: 0.5 }, G.fill);
    // Tischbeine
    P(U(f, 'M36 132 L38 176 M192 132 L190 176 M38 176 L48 176 M190 176 L180 176'), { strokeWidth: 2.6, roughness: 0.6 });
    // Umschlag auf dem Tisch
    add(rc.rectangle(X(148), Y(108), 34 * f.s, 16 * f.s, O({ fill: WHITE, fillStyle: 'solid', strokeWidth: 1.5, roughness: 0.5 })), G.fill);
    P(U(f, 'M148 108 L165 118 L182 108'), { strokeWidth: 1.2, roughness: 0.4 });
    shadow(X(114), Y(178), 160 * f.s, 8 * f.s);
  }

  // ---- Zwei Köpfe: Wissen | Handeln ----
  function heads(x, y, w, h) {
    const f = fit(x, y, w, h, 340, 160), p = f.p, X = f.X, Y = f.Y;
    // Profil nach rechts blickend, Einheitsbox 110 x 160 (x 0..110)
    const prof = (m) => `M${m(36, 160)} L${m(38, 128)} C${m(14, 116)} ${m(4, 92)} ${m(8, 64)} C${m(12, 24)} ${m(44, 2)} ${m(72, 8)} C${m(94, 14)} ${m(104, 36)} ${m(100, 58)} L${m(104, 70)} C${m(110, 78)} ${m(110, 86)} ${m(114, 94)} C${m(112, 100)} ${m(104, 100)} ${m(102, 102)} C${m(104, 108)} ${m(108, 110)} ${m(104, 116)} C${m(100, 118)} ${m(104, 122)} ${m(102, 128)} C${m(100, 138)} ${m(92, 142)} ${m(84, 142)} C${m(78, 150)} ${m(72, 156)} ${m(68, 160)} Z`;
    // linker Kopf (Blick nach rechts)
    shadow(X(80), Y(161), 70 * f.s, 8 * f.s); shadow(X(236), Y(161), 70 * f.s, 8 * f.s);
    P(prof((a, b) => p(a + 30, b)), { fill: WHITE, fillStyle: 'solid', strokeWidth: 2.8, roughness: 0.8 }, G.fill);
    // Gehirn im linken Kopf
    const g = fit(X(48), Y(26), 80 * f.s, 66 * f.s, 120, 100);
    P(U(g, 'M22 62 C8 58 6 38 20 32 C18 16 36 8 50 14 C58 4 80 4 88 14 C102 12 116 26 110 42 C120 52 112 70 98 68 C92 76 80 78 72 72 C62 80 44 80 38 70 C30 74 20 70 22 62 Z'), { fill: BLUE2, fillStyle: 'solid', stroke: BLUE, strokeWidth: 1.6, roughness: 0.7 }, G.fill);
    ['M34 30 C40 24 48 34 56 26', 'M62 18 C66 28 76 22 80 30', 'M86 28 C92 36 100 30 104 40', 'M28 48 C36 42 42 52 50 44', 'M56 42 C62 50 72 44 78 52', 'M84 50 C90 56 96 52 100 58', 'M46 62 C54 56 60 64 68 58'].forEach((d) => P(U(g, d), { stroke: BLUE, strokeWidth: 1.15, roughness: 0.5 }));
    // rechter Kopf (gespiegelt, Blick nach links)
    P(prof((a, b) => p(310 - a, b)), { fill: WHITE, fillStyle: 'solid', strokeWidth: 2.8, roughness: 0.8 }, G.fill);
    // gestrichelte Trennlinie
    add(rc.line(X(170), Y(-4), X(170), Y(166), O({ strokeWidth: 1.8, roughness: 0.6, strokeLineDash: [8, 6] })));
    // Hand mit Stift rechts
    const hx = 300, hy = 120;
    P(U(f, `M${hx + 10} ${hy + 30} C${hx - 6} ${hy + 26} ${hx - 8} ${hy + 8} ${hx + 8} ${hy + 2} C${hx + 18} ${hy - 2} ${hx + 30} ${hy + 4} ${hx + 34} ${hy + 14} C${hx + 36} ${hy + 24} ${hx + 26} ${hy + 32} ${hx + 10} ${hy + 30} Z`), { fill: WHITE, fillStyle: 'solid', strokeWidth: 2.2, roughness: 0.7 }, G.fill);
    P(U(f, `M${hx + 8} ${hy + 10} C${hx + 14} ${hy + 6} ${hx + 20} ${hy + 8} ${hx + 24} ${hy + 12} M${hx + 8} ${hy + 18} C${hx + 14} ${hy + 14} ${hx + 20} ${hy + 16} ${hx + 24} ${hy + 20}`), { strokeWidth: 1.2, roughness: 0.4 });
    // Stift
    PG([[X(hx - 2), Y(hy + 12)], [X(hx + 50), Y(hy - 30)], [X(hx + 56), Y(hy - 24)], [X(hx + 4), Y(hy + 18)]], { fill: WHITE, fillStyle: 'solid', strokeWidth: 1.8, roughness: 0.5 }, G.fill);
    PG([[X(hx - 2), Y(hy + 12)], [X(hx + 4), Y(hy + 18)], [X(hx - 8), Y(hy + 22)]], { fill: INK, fillStyle: 'solid', strokeWidth: 1.4, roughness: 0.4 }, G.fill);
    L(X(hx + 44), Y(hy - 20), X(hx + 50), Y(hy - 14), { strokeWidth: 1.4, roughness: 0.3 });
    // Schreiblinie
    P(U(f, `M${hx - 16} ${hy + 30} c6 -3 12 3 18 0 c6 -3 10 2 14 0`), { strokeWidth: 1.4, roughness: 0.5 });
    return f;
  }

  // ---- Stoppuhr + Bombe + Läufer ----
  function stopwatch(x, y, w, h) {
    const f = fit(x, y, w, h, 110, 124), X = f.X, Y = f.Y, p = f.p;
    shadow(X(55), Y(120), 96 * f.s, 9 * f.s);
    add(rc.rectangle(X(49), Y(2), 12 * f.s, 12 * f.s, O({ fill: BLUE, fillStyle: 'solid', stroke: INK, strokeWidth: 1.8, roughness: 0.4 })), G.fill);
    L(X(55), Y(14), X(55), Y(24), { strokeWidth: 3, roughness: 0.3 });
    P(U(f, 'M86 30 L96 20'), { strokeWidth: 3.5, roughness: 0.3 });
    C(X(55), Y(70), 90 * f.s, { fill: BLUE2, fillStyle: 'solid', stroke: BLUE, strokeWidth: 3.5, roughness: 0.6 }, G.fill);
    C(X(55), Y(70), 72 * f.s, { fill: WHITE, fillStyle: 'solid', stroke: INK, strokeWidth: 1.3, roughness: 0.4 }, G.fill);
    for (let a = 0; a < 12; a++) { const t = a * Math.PI / 6; L(X(55 + 30 * Math.cos(t)), Y(70 + 30 * Math.sin(t)), X(55 + 34 * Math.cos(t)), Y(70 + 34 * Math.sin(t)), { strokeWidth: a % 3 ? 1.2 : 2, roughness: 0.2 }); }
    L(X(55), Y(70), X(55), Y(44), { strokeWidth: 2.4, roughness: 0.3 });
    L(X(55), Y(70), X(76), Y(54), { stroke: RED, strokeWidth: 2.4, roughness: 0.3 });
    C(X(55), Y(70), 5 * f.s, { fill: INK, fillStyle: 'solid', roughness: 0.2, strokeWidth: 1 });
    // Bewegungslinien links
    P(U(f, 'M10 50 C4 60 4 80 10 90 M2 60 C-2 68 -2 76 2 84'), { strokeWidth: 1.6, roughness: 0.4 });
    return f;
  }
  function bomb(x, y, w, h) {
    const f = fit(x, y, w, h, 80, 90), X = f.X, Y = f.Y, p = f.p;
    C(X(36), Y(58), 50 * f.s, { fill: '#3a3a3a', fillStyle: 'solid', stroke: INK, strokeWidth: 2.4, roughness: 0.6 }, G.fill);
    P(U(f, 'M24 48 C26 42 32 38 40 38'), { stroke: '#bdbdbd', strokeWidth: 2.2, roughness: 0.4 });
    add(rc.rectangle(X(28), Y(26), 16 * f.s, 10 * f.s, O({ fill: '#6b6b6b', fillStyle: 'solid', strokeWidth: 1.8, roughness: 0.4 })), G.fill);
    P(U(f, 'M36 26 C36 14 48 14 54 10 C60 6 64 4 70 6'), { strokeWidth: 2, roughness: 0.5 });
    // Funken
    const sx = 72, sy = 6, pts = [];
    for (let i = 0; i < 16; i++) { const a = i * Math.PI / 8, rr = i % 2 ? 6 : 13; pts.push([X(sx + Math.cos(a) * rr), Y(sy + Math.sin(a) * rr)]); }
    PG(pts, { fill: '#f6c3c3', fillStyle: 'solid', stroke: RED, strokeWidth: 1.8, roughness: 0.7 }, G.fill);
  }
  function runner(x, y, w, h) {
    const f = fit(x, y, w, h, 110, 130), X = f.X, Y = f.Y, p = f.p;
    face(X(68), Y(18), 13 * f.s, 'worry');
    // Schweißtropfen
    [[88, 4], [94, 18], [52, 2]].forEach(([a, b]) => P(U(f, `M${a} ${b} c-3 5 -3 8 0 9 c3 -1 3 -4 0 -9 Z`), { fill: BLUE, fillStyle: 'solid', stroke: BLUE, strokeWidth: 1, roughness: 0.3 }, G.fill));
    // Rumpf
    P(U(f, 'M64 31 C58 46 52 58 48 70'), { strokeWidth: 2.8, roughness: 0.5 });
    // Arme
    P(U(f, 'M60 42 C72 50 82 54 94 44 M60 42 C48 36 40 36 32 48'), { strokeWidth: 2.4, roughness: 0.5 });
    // Beine (Laufpose)
    P(U(f, 'M48 70 C62 80 76 86 84 100 C88 108 92 114 100 118 M48 70 C40 86 32 96 20 104 C14 108 10 116 12 124'), { strokeWidth: 2.6, roughness: 0.5 });
    P(U(f, 'M100 118 L108 110 M12 124 L24 126'), { strokeWidth: 2.2, roughness: 0.4 });
    // Bewegungslinien
    P(U(f, 'M2 60 L22 60 M-4 74 L18 74 M4 88 L24 88'), { strokeWidth: 1.6, roughness: 0.4 });
  }

  // ---- kleine Icons für die Checkliste ----
  const ICO = {
    calendar(x, y, s) {
      add(rc.rectangle(x, y + s * 0.15, s, s * 0.85, O({ fill: WHITE, fillStyle: 'solid', strokeWidth: 1.6, roughness: 0.5 })), G.fill);
      add(rc.rectangle(x, y + s * 0.15, s, s * 0.22, O({ fill: BLUE2, fillStyle: 'solid', stroke: INK, strokeWidth: 1.2, roughness: 0.3 })), G.fill);
      L(x + s * 0.28, y, x + s * 0.28, y + s * 0.25, { strokeWidth: 1.6, roughness: 0.2 }); L(x + s * 0.72, y, x + s * 0.72, y + s * 0.25, { strokeWidth: 1.6, roughness: 0.2 });
      for (let r = 0; r < 2; r++) for (let c = 0; c < 3; c++) add(rc.rectangle(x + s * (0.16 + c * 0.26), y + s * (0.46 + r * 0.22), s * 0.16, s * 0.12, O({ fill: INK, fillStyle: 'solid', strokeWidth: 0.6, roughness: 0.2 })), G.fill);
    },
    headbrain(x, y, s) {
      const f = fit(x, y, s, s, 100, 100);
      P(U(f, 'M60 98 C40 98 18 86 18 60 C18 30 40 10 66 12 C86 14 94 34 90 50 L98 60 L90 64 L90 76 C86 86 76 86 68 84 L66 98 Z'), { fill: WHITE, fillStyle: 'solid', strokeWidth: 1.6, roughness: 0.5 }, G.fill);
      P(U(f, 'M34 44 C34 28 50 22 62 30 C72 24 84 36 78 46 C84 56 70 64 60 58 C50 66 34 58 34 44 Z'), { fill: BLUE2, fillStyle: 'solid', stroke: BLUE, strokeWidth: 1.2, roughness: 0.4 }, G.fill);
    },
    eyeoff(x, y, s) {
      const f = fit(x, y, s, s, 100, 100);
      P(U(f, 'M6 50 C30 16 70 16 94 50 C70 84 30 84 6 50 Z'), { fill: WHITE, fillStyle: 'solid', strokeWidth: 1.6, roughness: 0.5 }, G.fill);
      C(f.X(50), f.Y(50), 26 * f.s, { fill: BLUE2, fillStyle: 'solid', stroke: INK, strokeWidth: 1.2, roughness: 0.3 }, G.fill);
      L(f.X(14), f.Y(86), f.X(86), f.Y(14), { stroke: RED, strokeWidth: 2.4, roughness: 0.3 });
    },
    stop(x, y, s) {
      const pts = []; for (let i = 0; i < 8; i++) { const a = Math.PI / 8 + i * Math.PI / 4; pts.push([x + s / 2 + Math.cos(a) * s / 2, y + s / 2 + Math.sin(a) * s / 2]); }
      PG(pts, { fill: RED, fillStyle: 'solid', stroke: INK, strokeWidth: 1.4, roughness: 0.4 }, G.fill);
      add(rc.rectangle(x + s * 0.2, y + s * 0.42, s * 0.6, s * 0.16, O({ fill: WHITE, fillStyle: 'solid', stroke: 'none', roughness: 0.3 })), G.fill);
    },
    target(x, y, s) {
      C(x + s / 2, y + s / 2, s, { fill: WHITE, fillStyle: 'solid', strokeWidth: 1.6, roughness: 0.5 }, G.fill);
      C(x + s / 2, y + s / 2, s * 0.62, { fill: BLUE2, fillStyle: 'solid', strokeWidth: 1.2, roughness: 0.4 }, G.fill);
      C(x + s / 2, y + s / 2, s * 0.24, { fill: RED, fillStyle: 'solid', stroke: RED, strokeWidth: 1, roughness: 0.3 }, G.fill);
    },
    clock(x, y, s) {
      C(x + s / 2, y + s / 2, s, { fill: WHITE, fillStyle: 'solid', stroke: BLUE, strokeWidth: 2.2, roughness: 0.5 }, G.fill);
      L(x + s / 2, y + s / 2, x + s / 2, y + s * 0.2, { strokeWidth: 1.8, roughness: 0.2 }); L(x + s / 2, y + s / 2, x + s * 0.72, y + s * 0.6, { stroke: RED, strokeWidth: 1.8, roughness: 0.2 });
    },
  };

  // =============== Komposition ===============
  function draw() {
    frame();

    // ---- Spruchband oben ----
    const bn = bx(byId('banner'));
    ribbon(158, 34, 452, 66, 34, { curve: 12 });

    // ---- Kopf-Dekor ----
    // gestrichelter Pfeil vom kleinen ? zum Banner
    arrow([[112, 100], [126, 88], [150, 76]], { dash: [5, 4], w: 1.8, hs: 8 });
    scribble(104, 188, 30, 22, 30, {});
    rays(150, 262, -Math.PI * 0.72, 3, 44, 0.34, BLUE, 3);
    // rechts
    scribble(700, 40, 24, 9, 30, {});
    arrow([[660, 130], [644, 114], [630, 100]], { dash: [5, 4], w: 1.8, hs: 8 });
    gear(704, 196, 20, '#c8c8c8', 8);
    // roter Bogenpfeil
    arrow([[712, 236], [724, 262], [708, 290], [694, 304]], { stroke: RED, w: 3.2, hs: 10, r: 0.6 });
    rays(620, 234, -Math.PI * 0.28, 3, 44, 0.34, BLUE, 3);
    // kleiner "Knall"-Stern
    P('M624 322 l6 -10 M632 320 l10 -6 M636 330 l12 0 M622 334 l-8 8', { strokeWidth: 1.6, roughness: 0.4 });

    // ---- Spaltenüberschriften: Marker + Unterstreichung ----
    marker(byId('hl1b'), BLUE2, 3, 15);
    marker(byId('hl1c'), BLUE2, 3, 15);
    marker(byId('hl2b'), BLUE2, 3, 15);
    underline(byId('hl2c'), RED, 7, 5.5);
    bulb(58, 304, 54, 78, {});
    // gestrichelter Pfeil unter dem Titel zur linken Überschrift
    arrow([[148, 282], [160, 316], [196, 338], [222, 346]], { dash: [6, 5], w: 1.8, hs: 9 });
    // dicker blauer Pfeil zur linken Überschrift
    arrow([[318, 316], [296, 342], [272, 362], [250, 380]], { stroke: BLUE, w: 4.2, hs: 14, r: 0.4, multi: true });
    // Locken-Pfeil Titel -> Gehirn (blau, Marker)
    const curl = [[372, 320], [392, 306], [418, 316], [420, 342], [398, 356], [380, 342], [386, 322], [412, 324], [424, 352], [408, 392], [372, 410], [360, 446], [380, 486], [392, 520], [386, 544]];
    add(rc.curve(curl, O({ stroke: BLUE, strokeWidth: 4, roughness: 0.6, bowing: 0.5, disableMultiStroke: false })));
    head([386, 546], Math.PI / 2 + 0.1, BLUE, 13, 3.6);
    // kleines Gehirn mit Pulslinie rechts oben
    const bs = brainSmall(650, 302, 78, 64, BLUE2);
    pulse(574, 334, 646, BLUE);
    pulse(700, 486, 752, BLUE);

    // ---- Mitte: Gehirn ----
    brainHero(254, 548, 242, 238);
    rays(314, 534, -Math.PI * 0.72, 2, 16, 0.5, BLUE, 2.6);
    rays(494, 534, -Math.PI * 0.28, 2, 18, 0.5, BLUE, 2.6);

    // ---- Links A ----
    const c1 = bx(byId('cloud1'));
    cloud(c1.x - 22, c1.y - 22, c1.w + 44, c1.h + 44, {});
    C(258, 654, 13, { fill: WHITE, fillStyle: 'solid', strokeWidth: 2, roughness: 0.6 }, G.fill);
    C(272, 670, 8, { fill: WHITE, fillStyle: 'solid', strokeWidth: 1.8, roughness: 0.6 }, G.fill);
    phoneFigure(30, 530, 94, 140);

    // ---- Links B ----
    deskScene(26, 758, 226, 154);

    // ---- Links C ----
    heads(42, 1056, 350, 150);
    bulb(40, 1062, 26, 40, {});
    gear(33, 1134, 10, '#dcdcdc', 7); // sitzt auf der Rahmenlinie
    rays(404, 1086, -Math.PI * 0.35, 3, 16, 0.5, BLUE, 2.4);

    // ---- Mitte: Kreislauf ----
    const nodes = [...document.querySelectorAll('.node')].map((n) => ({ el: n, b: bx(n) }));
    // Ring durch die Knotenmitten (abgerundetes Rechteck)
    const Lx = 318, Rx = 450, Ty = 862, By = 996, rr = 40;
    const ring = `M${Lx + rr} ${Ty} L${Rx - rr} ${Ty} Q${Rx} ${Ty} ${Rx} ${Ty + rr} L${Rx} ${By - rr} Q${Rx} ${By} ${Rx - rr} ${By} L${Lx + rr} ${By} Q${Lx} ${By} ${Lx} ${By - rr} L${Lx} ${Ty + rr} Q${Lx} ${Ty} ${Lx + rr} ${Ty} Z`;
    P(ring, { strokeWidth: 2.4, roughness: 0.9, bowing: 2.2 }, G.back);
    // Pfeilspitzen auf dem Ring (Uhrzeigersinn)
    head([386, Ty], 0, INK, 9, 2.4); head([Rx, 897], Math.PI / 2, INK, 9, 2.4); head([Rx, 965], Math.PI / 2, INK, 9, 2.4);
    head([378, By], Math.PI, INK, 9, 2.4); head([Lx, 963], -Math.PI / 2, INK, 9, 2.4); head([Lx, 895], -Math.PI / 2, INK, 9, 2.4);
    nodes.forEach(({ el, b }) => {
      if (el.classList.contains('red')) {
        const pts = []; const cx = b.cx, cy = b.cy, n = 9;
        for (let i = 0; i < n * 2; i++) { const a = -Math.PI / 2 + i * Math.PI / n, out = i % 2 === 0; pts.push([cx + Math.cos(a) * (b.w / 2 + (out ? 16 : 7)), cy + Math.sin(a) * (b.h / 2 + (out ? 14 : 6))]); }
        PG(pts, { fill: WHITE, fillStyle: 'solid', stroke: RED, strokeWidth: 2, roughness: 0.8 }, G.fill);
      } else add(rc.rectangle(b.x - 6, b.y - 4, b.w + 12, b.h + 8, O({ fill: WHITE, fillStyle: 'solid', strokeWidth: 2, roughness: 0.9 })), G.fill);
    });
    // Uhr in der Mitte
    ICO.clock(382, 917, 24);

    // ---- Rechts A ----
    synapse(524, 506, 206, 90);

    // ---- Rechts B ----
    brainPanel(536, 752, 160, 120);
    // Pfeil zum Steuerpult (von links unten)
    arrow([[506, 866], [502, 842], [514, 828], [524, 838], [514, 846], [506, 832], [518, 814], [538, 802]], { w: 2.2, hs: 9, r: 0.4 });
    // Checkliste: Kästchen + Haken, Pfeile zu Icons
    const icons = ['calendar', 'headbrain', 'eyeoff', 'stop', 'target'];
    [...document.querySelectorAll('#tasks li')].forEach((li, i) => {
      const b = bx(li);
      add(rc.rectangle(b.x + 2, b.y + 3, 13, 13, O({ fill: WHITE, fillStyle: 'solid', strokeWidth: 1.6, roughness: 0.6 })), G.fill);
      P(`M${b.x + 4} ${b.y + 10} L${b.x + 8} ${b.y + 15} L${b.x + 17} ${b.y + 1}`, { stroke: BLUE, strokeWidth: 2.2, roughness: 0.4 });
      // Textbreite
      const rg = document.createRange(); rg.selectNodeContents(li); const tr = rg.getBoundingClientRect();
      const x1 = b.x + 24 + tr.width + 8, ix = 700, iy = b.y - 1, s = 20;
      arrow([[x1, b.cy + 1], [ix - 6, b.cy]], { w: 1.7, hs: 6, bow: (i % 2 ? -0.07 : 0.07), taper: false });
      ICO[icons[i]](ix, iy, s);
    });

    // ---- Rechts C ----
    stopwatch(488, 1066, 88, 94);
    bomb(568, 1056, 56, 62);
    runner(628, 1054, 106, 110);
    P('M592 1128 c-6 8 -6 20 0 28', { strokeWidth: 1.4, roughness: 0.4 });

    // ---- Spruchband unten (Fazit) ----
    ribbon(112, 1304, 544, 48, 32, { curve: 8 });

    buildMask();

  }

  // Messung für Überlappungsprüfung
  window.__measure = () => {
    const out = [];
    document.querySelectorAll('.t').forEach((el) => { const b = el.getBoundingClientRect(); out.push({ id: el.id || el.className, x: Math.round(b.left), y: Math.round(b.top), r: Math.round(b.right), b: Math.round(b.bottom), text: (el.textContent || '').slice(0, 30) }); });
    return out;
  };

  const go = () => Promise.all([
    document.fonts.load("900 60px 'Roboto Condensed'", 'AäÄ'), document.fonts.load("800 24px 'Roboto Condensed'", 'aäÄ'), document.fonts.load("500 18px 'Roboto Condensed'", 'aäÄ'), document.fonts.load("700 18px 'Roboto Condensed'", 'aäÄ'),
  ]).then(() => document.fonts.ready).then(draw);
  if (document.readyState === 'complete') go(); else window.addEventListener('load', go);
})();
