// Zeichnet alle handgezeichneten Elemente (rough.js) passend zu den gemessenen HTML-Boxen.
(function () {
  const INK = '#1c1c1c', PET = '#0f6f7b', YEL = '#ffe14d', WHITE = '#ffffff';
  const svg = document.getElementById('ink');
  const rc = rough.svg(svg);
  const G = { shadow: byId('gShadow'), box: byId('gBox'), hl: byId('gHl'), ink: byId('gInk') };
  function byId(i) { return document.getElementById(i); }
  let SEED = 7;
  const nx = () => (SEED += 13);
  const O = (o) => Object.assign({ roughness: 1.3, bowing: 1, stroke: INK, strokeWidth: 2, seed: nx() }, o || {});
  const add = (n, g) => { (g || G.ink).appendChild(n); return n; };
  const bx = (el) => { const r = el.getBoundingClientRect(); return { x: r.left, y: r.top, w: r.width, h: r.height, r: r.right, b: r.bottom, cx: r.left + r.width / 2, cy: r.top + r.height / 2 }; };
  const fit = (b, uw, uh) => {
    const s = Math.min(b.w / uw, b.h / uh), ox = b.x + (b.w - uw * s) / 2, oy = b.y + (b.h - uh * s) / 2;
    return { s, p: (x, y) => (ox + x * s).toFixed(1) + ' ' + (oy + y * s).toFixed(1), X: (x) => ox + x * s, Y: (y) => oy + y * s };
  };
  const P = (d, o, g) => add(rc.path(d, O(o)), g);
  const L = (x1, y1, x2, y2, o, g) => add(rc.line(x1, y1, x2, y2, O(o)), g);
  // Textausdehnung (erste Zeile) eines Blockelements
  const textBox = (el) => { const r = document.createRange(); r.selectNodeContents(el.firstChild); const q = r.getClientRects()[0]; return { x: q.left, y: q.top, r: q.right, b: q.bottom, cy: (q.top + q.bottom) / 2 }; };

  // ---------- Grundformen ----------
  function sparkle(cx, cy, r, o) {
    const k = r * 0.22;
    P(`M${cx} ${cy - r} Q${cx + k} ${cy - k} ${cx + r} ${cy} Q${cx + k} ${cy + k} ${cx} ${cy + r} Q${cx - k} ${cy + k} ${cx - r} ${cy} Q${cx - k} ${cy - k} ${cx} ${cy - r} Z`, Object.assign({ roughness: 0.6, strokeWidth: 1.6 }, o));
  }
  function head(p, ang, col, len) {
    const a1 = ang + Math.PI * 0.8, a2 = ang - Math.PI * 0.8;
    add(rc.linearPath([[p[0] + len * Math.cos(a1), p[1] + len * Math.sin(a1)], p, [p[0] + len * Math.cos(a2), p[1] + len * Math.sin(a2)]], O({ stroke: col, strokeWidth: 2.4, roughness: 0.5 })));
  }
  function arrow(pts, o) {
    o = o || {};
    const col = o.stroke || INK;
    const opt = O({ stroke: col, strokeWidth: o.w || 2.2, roughness: o.r == null ? 0.8 : o.r, bowing: 0.6 });
    if (o.dash) opt.strokeLineDash = o.dash;
    if (pts.length === 2) add(rc.line(pts[0][0], pts[0][1], pts[1][0], pts[1][1], opt));
    else add(rc.curve(pts, opt));
    const a = pts[pts.length - 2], b = pts[pts.length - 1];
    head(b, Math.atan2(b[1] - a[1], b[0] - a[0]), col, o.hs || 11);
  }
  // Pfeil mit Schlaufe in der Mitte (wie im Vorschaubild)
  function loopArrow(S, E, r, o) {
    const dx = E[0] - S[0], dy = E[1] - S[1], len = Math.hypot(dx, dy), ux = dx / len, uy = dy / len;
    let nxv = uy, nyv = -ux; if (nyv > 0) { nxv = -nxv; nyv = -nyv; } // Normal nach oben
    if (o && o.down) { nxv = -nxv; nyv = -nyv; }
    const M = [S[0] + dx * 0.44, S[1] + dy * 0.44];
    const C = [M[0] + nxv * r, M[1] + nyv * r];
    const a0 = Math.atan2(M[1] - C[1], M[0] - C[0]);
    // Richtung so wählen, dass die Schlaufe vorwärts startet
    const t1 = [-Math.sin(a0), Math.cos(a0)];
    const dir = (t1[0] * ux + t1[1] * uy) > 0 ? 1 : -1;
    const pts = [S, [S[0] + dx * 0.22 + nxv * 3, S[1] + dy * 0.22 + nyv * 3]];
    for (let i = 1; i <= 12; i++) { const a = a0 + dir * i * (Math.PI * 2 / 12); pts.push([C[0] + Math.cos(a) * r + ux * i * 2.2, C[1] + Math.sin(a) * r + uy * i * 2.2]); }
    pts.push([S[0] + dx * 0.78 + nxv * 4, S[1] + dy * 0.78 + nyv * 4]);
    pts.push([E[0] - ux * 6, E[1] - uy * 6]);
    pts.push(E);
    arrow(pts, o);
  }
  function cloudBurst(b, padX, padY, spikes, o) {
    const cx = b.cx, cy = b.cy, pts = [];
    for (let i = 0; i < spikes * 2; i++) {
      const a = -Math.PI / 2 + i * Math.PI / spikes, out = i % 2 === 0;
      const rx = b.w / 2 + (out ? padX + 10 : padX), ry = b.h / 2 + (out ? padY + 9 : padY);
      pts.push([cx + Math.cos(a) * rx, cy + Math.sin(a) * ry]);
    }
    add(rc.polygon(pts, O(Object.assign({ fill: YEL, fillStyle: 'solid', strokeWidth: 1.8, roughness: 0.9 }, o))), G.box);
  }

  // ---------- Icons (eigene Pfade, durch rough.js gewackelt) ----------
  const ICON = {
    brain(b, el, pfc) {
      const { p } = fit(b, 120, 100);
      if (pfc) P(`M${p(22, 62)} C${p(8, 58)} ${p(6, 38)} ${p(20, 32)} C${p(18, 16)} ${p(36, 8)} ${p(50, 14)} C${p(44, 30)} ${p(42, 48)} ${p(40, 70)} C${p(32, 74)} ${p(20, 70)} ${p(22, 62)} Z`,
        { stroke: 'none', fill: PET, fillStyle: 'hachure', hachureGap: 3.6, fillWeight: 1.3, roughness: 0.8 });
      P(`M${p(22, 62)} C${p(8, 58)} ${p(6, 38)} ${p(20, 32)} C${p(18, 16)} ${p(36, 8)} ${p(50, 14)} C${p(58, 4)} ${p(80, 4)} ${p(88, 14)} C${p(102, 12)} ${p(116, 26)} ${p(110, 42)} C${p(120, 52)} ${p(112, 70)} ${p(98, 68)} C${p(92, 76)} ${p(80, 78)} ${p(72, 72)} C${p(62, 80)} ${p(44, 80)} ${p(38, 70)} C${p(30, 74)} ${p(20, 70)} ${p(22, 62)} Z`,
        { strokeWidth: 2.2, roughness: 0.9 });
      P(`M${p(90, 70)} C${p(96, 82)} ${p(108, 80)} ${p(108, 66)}`, { strokeWidth: 1.8, roughness: 0.7 });
      P(`M${p(72, 74)} C${p(74, 84)} ${p(76, 90)} ${p(80, 98)} M${p(82, 74)} C${p(84, 84)} ${p(86, 90)} ${p(90, 97)}`, { strokeWidth: 1.8, roughness: 0.7 });
      const folds = ['M34 30 C40 24 48 34 56 26', 'M62 18 C66 28 76 22 80 30', 'M86 28 C92 36 100 30 104 40', 'M28 48 C36 42 42 52 50 44',
        'M56 42 C62 50 72 44 78 52', 'M84 50 C90 56 96 52 100 58', 'M46 62 C54 56 60 64 68 58'];
      folds.forEach((f) => { const n = f.match(/-?\d+(\.\d+)?/g).map(Number); let d = `M${p(n[0], n[1])} C${p(n[2], n[3])} ${p(n[4], n[5])} ${p(n[6], n[7])}`; P(d, { strokeWidth: 1.6, roughness: 0.7 }); });
    },
    brainpfc(b, el) { ICON.brain(b, el, true); },
    bolt(b) {
      const { X, Y } = fit(b, 60, 100);
      const pts = [[32, 0], [4, 56], [27, 56], [16, 100], [58, 38], [35, 38], [48, 0]].map(([x, y]) => [X(x), Y(y)]);
      add(rc.polygon(pts, O({ fill: YEL, fillStyle: 'solid', strokeWidth: 2.2, roughness: 0.8 })));
    },
    mail(b) {
      const { p } = fit(b, 132, 80);
      P(`M${p(2, 12)} L${p(92, 12)} L${p(92, 76)} L${p(2, 76)} Z`, { fill: WHITE, fillStyle: 'solid', strokeWidth: 2.2, roughness: 1 });
      P(`M${p(2, 12)} L${p(47, 48)} L${p(92, 12)}`, { roughness: 0.9 });
      P(`M${p(2, 76)} L${p(36, 44)} M${p(92, 76)} L${p(58, 44)}`, { roughness: 0.8, strokeWidth: 1.6 });
      // Sanduhr
      P(`M${p(102, 10)} L${p(130, 10)} M${p(102, 78)} L${p(130, 78)}`, { strokeWidth: 2.2, roughness: 0.6 });
      P(`M${p(106, 10)} C${p(106, 32)} ${p(116, 38)} ${p(116, 44)} C${p(116, 50)} ${p(106, 56)} ${p(106, 78)} M${p(126, 10)} C${p(126, 32)} ${p(116, 38)} ${p(116, 44)} C${p(116, 50)} ${p(126, 56)} ${p(126, 78)}`, { strokeWidth: 1.8, roughness: 0.6 });
      P(`M${p(108, 76)} L${p(116, 62)} L${p(124, 76)} Z`, { fill: YEL, fillStyle: 'solid', strokeWidth: 1.2, roughness: 0.5 });
      P(`M${p(110, 20)} L${p(122, 20)} L${p(116, 30)} Z`, { fill: YEL, fillStyle: 'solid', strokeWidth: 1.2, roughness: 0.5 });
    },
    heart(b) {
      const { p, X, Y } = fit(b, 120, 90);
      P(`M${p(50, 86)} C${p(18, 64)} ${p(4, 46)} ${p(10, 28)} C${p(16, 10)} ${p(42, 6)} ${p(50, 26)} C${p(58, 6)} ${p(84, 10)} ${p(90, 28)} C${p(96, 46)} ${p(82, 64)} ${p(50, 86)} Z`,
        { fill: INK, fillStyle: 'hachure', hachureGap: 4.2, fillWeight: 1.1, strokeWidth: 2.2, roughness: 0.9 });
      // Bewegungs-/Glanzstriche
      L(X(98), Y(16), X(110), Y(6), { strokeWidth: 1.8, roughness: 0.5 });
      L(X(102), Y(32), X(118), Y(30), { strokeWidth: 1.8, roughness: 0.5 });
      L(X(90), Y(6), X(94), Y(-6), { strokeWidth: 1.8, roughness: 0.5 });
      sparkle(X(108), Y(56), 7);
    },
    gauge(b) {
      const { p, X, Y, s } = fit(b, 100, 66);
      P(`M${p(6, 58)} C${p(6, 33.7)} ${p(25.7, 14)} ${p(50, 14)} C${p(74.3, 14)} ${p(94, 33.7)} ${p(94, 58)} Z`, { fill: INK, fillStyle: 'hachure', hachureGap: 5, fillWeight: 0.9, strokeWidth: 2.2, roughness: 0.9 });
      for (let a = 180; a >= 0; a -= 30) { const t = -a * Math.PI / 180; L(X(50 + 34 * Math.cos(t)), Y(58 + 34 * Math.sin(t)), X(50 + 44 * Math.cos(t)), Y(58 + 44 * Math.sin(t)), { strokeWidth: 1.6, roughness: 0.4 }); }
      const t = -55 * Math.PI / 180;
      L(X(50), Y(58), X(50 + 32 * Math.cos(t)), Y(58 + 32 * Math.sin(t)), { strokeWidth: 2.8, roughness: 0.4 });
      add(rc.circle(X(50), Y(58), 9 * s, O({ fill: INK, fillStyle: 'solid', roughness: 0.4 })));
      // Fragezeichen-Striche (Bewegung)
      L(X(16), Y(6), X(8), Y(-2), { strokeWidth: 1.6, roughness: 0.4 });
      L(X(4), Y(18), X(-6), Y(13), { strokeWidth: 1.6, roughness: 0.4 });
    },
    check(b) { const { p } = fit(b, 100, 100); P(`M${p(6, 54)} L${p(38, 86)} L${p(96, 10)}`, { stroke: PET, strokeWidth: 3.2, roughness: 0.7 }); },
    cross(b) { const { p } = fit(b, 100, 100); P(`M${p(10, 10)} L${p(90, 90)} M${p(90, 10)} L${p(10, 90)}`, { strokeWidth: 3.2, roughness: 0.7 }); },
    wave(b) { const { p } = fit(b, 34, 16); P(`M${p(1, 8)} C${p(5, 0)} ${p(9, 0)} ${p(12, 8)} C${p(15, 16)} ${p(19, 16)} ${p(22, 8)} C${p(25, 0)} ${p(29, 0)} ${p(33, 8)}`, { stroke: INK, strokeWidth: 2.2, roughness: 0.5 }); },
    brace(b) { const { p } = fit(b, 12, 118); P(`M${p(10, 2)} C${p(2, 2)} ${p(6, 30)} ${p(6, 50)} C${p(6, 56)} ${p(2, 59)} ${p(0, 59)} C${p(2, 59)} ${p(6, 62)} ${p(6, 68)} C${p(6, 88)} ${p(2, 116)} ${p(10, 116)}`, { strokeWidth: 2, roughness: 0.6 }); },
    bulb(b) {
      const { p, X, Y } = fit(b, 80, 120);
      P(`M${p(40, 22)} C${p(18, 22)} ${p(6, 40)} ${p(10, 58)} C${p(13, 70)} ${p(24, 76)} ${p(26, 88)} L${p(54, 88)} C${p(56, 76)} ${p(67, 70)} ${p(70, 58)} C${p(74, 40)} ${p(62, 22)} ${p(40, 22)} Z`,
        { fill: YEL, fillStyle: 'hachure', hachureGap: 3.6, fillWeight: 1.4, strokeWidth: 2.2, roughness: 0.9 });
      P(`M${p(33, 88)} L${p(33, 66)} L${p(37, 60)} L${p(40, 66)} L${p(43, 60)} L${p(47, 66)} L${p(47, 88)}`, { strokeWidth: 1.5, roughness: 0.5 });
      P(`M${p(27, 94)} L${p(53, 94)} M${p(28, 101)} L${p(52, 101)} M${p(33, 108)} L${p(47, 108)}`, { strokeWidth: 2, roughness: 0.6 });
      for (let a = -160; a <= -20; a += 35) { const t = a * Math.PI / 180; L(X(40 + 38 * Math.cos(t)), Y(54 + 38 * Math.sin(t)), X(40 + 50 * Math.cos(t)), Y(54 + 50 * Math.sin(t)), { strokeWidth: 1.8, roughness: 0.4 }); }
    },
    clock(b) {
      const { p, X, Y, s } = fit(b, 100, 100);
      P(`M${p(12, 34)} C${p(6, 18)} ${p(22, 4)} ${p(38, 12)} Z`, { fill: INK, fillStyle: 'hachure', hachureGap: 2.6, strokeWidth: 2, roughness: 0.6 });
      P(`M${p(88, 34)} C${p(94, 18)} ${p(78, 4)} ${p(62, 12)} Z`, { fill: INK, fillStyle: 'hachure', hachureGap: 2.6, strokeWidth: 2, roughness: 0.6 });
      P(`M${p(50, 22)} L${p(50, 13)} M${p(42, 12)} L${p(58, 12)}`, { strokeWidth: 2, roughness: 0.4 });
      P(`M${p(28, 84)} L${p(18, 96)} M${p(72, 84)} L${p(82, 96)}`, { strokeWidth: 2.4, roughness: 0.4 });
      add(rc.circle(X(50), Y(56), 68 * s, O({ fill: WHITE, fillStyle: 'solid', strokeWidth: 2.4, roughness: 0.9 })));
      [[50, 26, 50, 31], [80, 56, 75, 56], [50, 86, 50, 81], [20, 56, 25, 56]].forEach(([a, c, d, e]) => L(X(a), Y(c), X(d), Y(e), { strokeWidth: 1.8, roughness: 0.3 }));
      P(`M${p(50, 56)} L${p(50, 36)} M${p(50, 56)} L${p(65, 62)}`, { strokeWidth: 2.4, roughness: 0.4 });
      // Wackel-Linien
      P(`M${p(3, 46)} C${p(-2, 54)} ${p(-2, 62)} ${p(3, 70)} M${p(97, 46)} C${p(102, 54)} ${p(102, 62)} ${p(97, 70)}`, { strokeWidth: 1.8, roughness: 0.4 });
      P(`M${p(-8, 42)} C${p(-14, 54)} ${p(-14, 64)} ${p(-8, 76)} M${p(108, 42)} C${p(114, 54)} ${p(114, 64)} ${p(108, 76)}`, { strokeWidth: 1.6, roughness: 0.4 });
    },
    magnifier(b) {
      const { p, X, Y, s } = fit(b, 100, 100);
      add(rc.polygon([[X(58), Y(66)], [X(66), Y(58)], [X(96), Y(88)], [X(88), Y(96)]], O({ fill: INK, fillStyle: 'solid', strokeWidth: 2, roughness: 0.6 })));
      add(rc.circle(X(40), Y(40), 62 * s, O({ fill: WHITE, fillStyle: 'solid', strokeWidth: 2.6, roughness: 0.8 })));
      P(`M${p(22, 36)} C${p(24, 27)} ${p(30, 21)} ${p(39, 19)}`, { strokeWidth: 1.8, roughness: 0.4 });
    },
  };

  function draw() {
    // ---- Titel-Banner ----
    const t = bx(byId('titleText'));
    const x0 = t.x - 26, y0 = t.y + 2, w = t.w + 52, h = t.h - 2, dy = 16, tail = 36, inset = 26;
    [[-1, x0], [1, x0 + w]].forEach(([sgn, ex]) => {
      const inner = ex - sgn * inset, outer = ex + sgn * tail;
      add(rc.polygon([[inner, y0 + dy], [outer, y0 + dy], [outer - sgn * 14, y0 + dy + h / 2], [outer, y0 + dy + h], [inner, y0 + dy + h]],
        O({ fill: INK, fillStyle: 'hachure', hachureGap: 4.5, fillWeight: 1.1, strokeWidth: 2.2, roughness: 1.1 })), G.box);
      add(rc.polygon([[ex, y0 + h], [inner, y0 + h + dy], [inner, y0 + h]], O({ fill: INK, fillStyle: 'solid', strokeWidth: 2, roughness: 0.5 })), G.box);
    });
    add(rc.rectangle(x0, y0, w, h, O({ fill: WHITE, fillStyle: 'solid', strokeWidth: 2.8, roughness: 1.4 })), G.box);
    sparkle(x0 + w + 8, y0 - 2, 8); sparkle(x0 - 16, y0 + 2, 6); sparkle(x0 + w - 12, y0 + h + 22, 6);

    // ---- Abschnittsrahmen + Nummern ----
    document.querySelectorAll('.sec').forEach((el) => {
      const b = bx(el);
      if (el.dataset.shadow) add(rc.rectangle(b.x + 7, b.y + 7, b.w, b.h, O({ stroke: 'none', fill: INK, fillStyle: 'hachure', hachureGap: 5.5, fillWeight: 1.1, roughness: 1.1 })), G.shadow);
      add(rc.rectangle(b.x, b.y, b.w, b.h, O({ fill: WHITE, fillStyle: 'solid', strokeWidth: 2.3, roughness: 1.5 })), G.box);
      if (el.dataset.n) {
        const cx = b.x + 8, cy = b.y + 8, d = document.createElement('div');
        d.className = 'num'; d.textContent = el.dataset.n; d.style.left = (cx - 20) + 'px'; d.style.top = (cy - 21) + 'px';
        document.body.appendChild(d);
        add(rc.circle(cx, cy, 40, O({ fill: WHITE, fillStyle: 'solid', strokeWidth: 2.6, roughness: 1.2 })));
      }
    });

    // ---- innere Kästen ----
    document.querySelectorAll('[data-box]').forEach((el) => {
      const b = bx(el), k = el.dataset.box;
      if (k === 'merk') add(rc.rectangle(b.x, b.y, b.w, b.h, O({ strokeWidth: 1.8, roughness: 1.2 })), G.box);
      if (k === 'dashed') add(rc.rectangle(b.x, b.y, b.w, b.h, Object.assign(O({ strokeWidth: 1.6, roughness: 1.1 }), { strokeLineDash: [7, 5] })), G.box);
      if (k === 'solid') add(rc.rectangle(b.x, b.y, b.w, b.h, O({ strokeWidth: 2, roughness: 1.2 })), G.box);
      if (k === 'bubble') {
        const r = 12, x = b.x, y = b.y, W = b.w, H = b.h;
        P(`M${x + r} ${y} L${x + W - r} ${y} Q${x + W} ${y} ${x + W} ${y + r} L${x + W} ${y + H - r} Q${x + W} ${y + H} ${x + W - r} ${y + H} L${x + r} ${y + H} Q${x} ${y + H} ${x} ${y + H - r} L${x} ${y + H * 0.74} L${x - 17} ${y + H * 0.86} L${x} ${y + H * 0.36} L${x} ${y + r} Q${x} ${y} ${x + r} ${y} Z`, { strokeWidth: 2, roughness: 1, fill: WHITE, fillStyle: 'solid' }, G.box);
      }
    });

    // ---- Textmarker ----
    document.querySelectorAll('.hl').forEach((el) => {
      for (const r of el.getClientRects()) add(rc.rectangle(r.left - 3, r.top + r.height * 0.2, r.width + 6, r.height * 0.72, O({ stroke: 'none', fill: YEL, fillStyle: 'solid', roughness: 1.1, bowing: 2 })), G.hl);
    });

    // ---- Icons ----
    document.querySelectorAll('.ico').forEach((el) => { const f = ICON[el.dataset.i]; if (f) f(bx(el), el); });

    // ---- Aufzählungszeichen ----
    document.querySelectorAll('#s3 li').forEach((li) => { const b = bx(li); add(rc.circle(b.x + 6, b.y + 12, 7, O({ fill: INK, fillStyle: 'solid', roughness: 0.6 }))); });
    document.querySelectorAll('.tasks li').forEach((li) => {
      const b = bx(li);
      add(rc.rectangle(b.x + 2, b.y + 4, 14, 14, O({ strokeWidth: 1.6, roughness: 0.8 })));
      P(`M${b.x + 4} ${b.y + 11} L${b.x + 8} ${b.y + 16} L${b.x + 18} ${b.y + 2}`, { stroke: PET, strokeWidth: 2.2, roughness: 0.4 });
    });
    document.querySelectorAll('.act li').forEach((li) => { const b = bx(li); ICON.bolt({ x: b.x + 1, y: b.y + 2, w: 13, h: 19 }); });
    document.querySelectorAll('.qs li').forEach((li) => {
      const b = bx(li), cx = b.x + 12, cy = b.y + 11;
      add(rc.circle(cx, cy, 27, O({ strokeWidth: 1.8, roughness: 0.6 })));
      const q = document.createElement('div'); q.textContent = '?'; q.className = 'cav';
      Object.assign(q.style, { position: 'absolute', zIndex: 3, left: (cx - 9.5) + 'px', top: (cy - 12) + 'px', width: '20px', textAlign: 'center', font: "700 20px/24px 'Caveat'" });
      document.body.appendChild(q);
    });

    // ---- Abschnitt 5: Klippen ----
    const g = bx(byId('gapbox'));
    const ll = document.querySelector('.gapbox .l'), lr = document.querySelector('.gapbox .r');
    const lb = bx(ll), rb = bx(lr);
    const top = g.y + 56, bot = g.b, lx2 = g.x + Math.max(lb.w + 14, 128), rx0 = rb.x + 6;
    const leftC = [[g.x, top + 2], [g.x + 34, top - 1], [lx2 - 12, top + 1], [lx2, top + 3], [lx2 - 6, top + 16], [lx2 + 4, top + 27], [lx2 - 3, bot]];
    const rightC = [[rx0 + 2, top + 3], [rx0 + 14, top], [g.r - 34, top - 1], [g.r, top + 2]];
    // Fels: helle Schraffur im Körper, dichte an der Abbruchkante
    add(rc.polygon([...leftC, [g.x, bot]], O({ stroke: 'none', fill: INK, fillStyle: 'hachure', hachureGap: 8, fillWeight: 0.7, roughness: 0.9 })), G.box);
    add(rc.polygon([[lx2 - 20, top + 6], [lx2, top + 3], [lx2 - 6, top + 16], [lx2 + 4, top + 27], [lx2 - 3, bot], [lx2 - 22, bot]], O({ stroke: 'none', fill: INK, fillStyle: 'hachure', hachureGap: 3.4, fillWeight: 1, roughness: 0.8, hachureAngle: 60 })), G.box);
    add(rc.linearPath(leftC, O({ strokeWidth: 2.4, roughness: 1 })));
    const rWall = [[rx0 + 2, top + 3], [rx0 + 5, top + 15], [rx0 - 4, top + 27], [rx0 + 4, bot]];
    add(rc.polygon([...rightC, [g.r, bot], [rx0 + 4, bot], [rx0 - 4, top + 27], [rx0 + 5, top + 15]], O({ stroke: 'none', fill: INK, fillStyle: 'hachure', hachureGap: 8, fillWeight: 0.7, roughness: 0.9 })), G.box);
    add(rc.polygon([[rx0 + 2, top + 3], [rx0 + 22, top + 6], [rx0 + 24, bot], [rx0 + 4, bot], [rx0 - 4, top + 27], [rx0 + 5, top + 15]], O({ stroke: 'none', fill: INK, fillStyle: 'hachure', hachureGap: 3.4, fillWeight: 1, roughness: 0.8, hachureAngle: 120 })), G.box);
    add(rc.linearPath([...rWall.slice().reverse(), ...rightC.slice(1)], O({ strokeWidth: 2.4, roughness: 1 })));
    // Sprung-Pfeil über die Lücke
    const gx1 = lx2 + 2, gx2 = rx0 + 14, mid = (gx1 + gx2) / 2;
    arrow([[gx1, top - 4], [gx1 + 12, top - 22], [mid, top - 36], [gx2 - 12, top - 22], [gx2, top - 5]], { dash: [6, 5], w: 2.2, hs: 10 });
    // fallende Steinchen + Bewegungslinien in der Lücke
    const gm = (lx2 + rx0) / 2;
    add(rc.circle(gm - 7, top + 18, 6, O({ fill: INK, fillStyle: 'solid', roughness: 0.5 })));
    add(rc.circle(gm + 8, top + 36, 5, O({ fill: INK, fillStyle: 'solid', roughness: 0.5 })));
    L(gm - 7, top + 1, gm - 7, top + 10, { strokeWidth: 1.4, roughness: 0.3 });
    L(gm + 8, top + 19, gm + 8, top + 28, { strokeWidth: 1.4, roughness: 0.3 });
    L(gm - 15, top + 5, gm - 15, top + 12, { strokeWidth: 1.2, roughness: 0.3 });

    // ---- Abschnitt 7: Kreislauf ----
    const cy = byId('cycle'), cb = bx(cy), RX = 160, RY = 88;
    const nodes = [...cy.querySelectorAll('.node')];
    nodes.forEach((n) => { const a = +n.dataset.a * Math.PI / 180; n.style.left = (cb.w / 2 + RX * Math.cos(a)) + 'px'; n.style.top = (cb.h / 2 + RY * Math.sin(a)) + 'px'; });
    const nb = nodes.map((n) => bx(n));
    nodes.forEach((n, i) => {
      const b = nb[i];
      if (n.dataset.style === 'burst') cloudBurst(b, 6, 4, 9);
      else add(rc.rectangle(b.x, b.y, b.w, b.h, O({ fill: WHITE, fillStyle: 'solid', strokeWidth: 1.8, roughness: 1.1 })), G.box);
    });
    const ccx = cb.cx, ccy = cb.cy;
    const inside = (pt, b, pad) => pt[0] > b.x - pad && pt[0] < b.r + pad && pt[1] > b.y - pad && pt[1] < b.b + pad;
    nodes.forEach((n, i) => {
      const j = (i + 1) % nodes.length;
      let a1 = +n.dataset.a, a2 = +nodes[j].dataset.a; if (a2 <= a1) a2 += 360;
      const padI = nodes[i].dataset.style === 'burst' ? 16 : 7, padJ = nodes[j].dataset.style === 'burst' ? 18 : 9;
      const pts = [];
      for (let a = a1; a <= a2; a += 2) {
        const r = a * Math.PI / 180, pt = [ccx + RX * Math.cos(r), ccy + RY * Math.sin(r)];
        if (!inside(pt, nb[i], padI) && !inside(pt, nb[j], padJ)) pts.push(pt);
      }
      if (pts.length < 3) return;
      const sel = pts.filter((_, k) => k % 3 === 0 || k === pts.length - 1);
      if (sel.length >= 3) arrow(sel, { w: 2.4, hs: 10, r: 0.7 });
    });
    // Ausrufezeichen bei "Deadline naht"
    const dn = nb[1];
    [[dn.r + 6, dn.y - 16], [dn.r + 16, dn.y - 10]].forEach(([x, y], k) => { L(x, y, x - 2 + k, y + 13, { strokeWidth: 2.4, roughness: 0.3 }); add(rc.circle(x - 2 + k, y + 19, 3.5, O({ fill: INK, fillStyle: 'solid', roughness: 0.3 }))); });

    // ---- Fazit-Etikett ----
    const ftEl = byId('fazitTag'), ft = bx(ftEl);
    const gt = document.createElementNS('http://www.w3.org/2000/svg', 'g'); gt.setAttribute('transform', `rotate(-3 ${ft.cx} ${ft.cy})`); G.box.appendChild(gt);
    add(rc.rectangle(ft.x - 10, ft.y + 2, ft.w + 20, ft.h - 4, O({ fill: YEL, fillStyle: 'solid', strokeWidth: 2.2, roughness: 1.1 })), gt);
    ftEl.style.transform = 'rotate(-3deg)';
    const fz = bx(byId('fazit'));
    sparkle(fz.r + 22, fz.y + 30, 7); sparkle(fz.r + 18, fz.y + 62, 4); sparkle(fz.x - 18, fz.y + 64, 6); sparkle(fz.x - 12, fz.y + 30, 4);

    // ---- Fußzeile: Trennlinie ----
    const fo = bx(byId('foot'));

    // ---- Verbindungspfeile (Lesefluss) ----
    const S = (id) => bx(byId(id));
    const s1 = S('s1'), s2 = S('s2'), s3 = S('s3'), s4 = S('s4'), s5 = S('s5'), s6 = S('s6'), s7 = S('s7'), s8 = S('s8');
    const h1 = textBox(document.querySelector('#s1 h2')), h3 = textBox(document.querySelector('#s3 h2')), h5 = textBox(document.querySelector('#s5 h2')), h7 = textBox(document.querySelector('#s7 h2'));
    // Rückläufer: langer Schwung durch die Zeilenlücke zum nächsten Nummernkreis
    const sweep = (A, Bx, By) => { const gy = (A.b + By) / 2 + 1; arrow([[A.x + 46, A.b + 1], [A.x + 18, gy], [(A.x + Bx) / 2, gy + 2], [Bx + 70, gy - 1], [Bx + 40, gy + 1], [Bx + 20, By - 11]], { w: 2, r: 0.9 }); };
    loopArrow([h1.r + 16, h1.cy + 4], [s2.x - 16, s2.y + 14], 9);
    arrow([[h3.r + 16, h3.cy + 4], [(h3.r + s4.x) / 2, h3.cy - 8], [s4.x - 16, s4.y + 14]]);
    arrow([[h5.r + 8, h5.cy + 6], [(h5.r + s6.x) / 2 - 2, h5.cy - 6], [s6.x - 16, s6.y + 14]]);
    loopArrow([h7.r + 18, h7.cy + 2], [s8.x - 16, s8.y + 14], 11, { down: true });
    arrow([[s8.cx - 10, s8.b + 1], [s8.cx - 20, s8.b + 11], [fz.r - 120, fz.y - 2]]);
    // Bewegungsstriche am Titel-Blitz
    const bt = bx(byId('icoBoltTop'));
    L(bt.x - 6, bt.b - 6, bt.x - 16, bt.b + 4, { strokeWidth: 1.6, roughness: 0.3 }); L(bt.x + 4, bt.b + 2, bt.x - 4, bt.b + 14, { strokeWidth: 1.6, roughness: 0.3 });
    L(bt.r + 2, bt.y + 10, bt.r + 10, bt.y + 2, { strokeWidth: 1.6, roughness: 0.3 });
  }

  window.__measure = () => {
    const out = {};
    document.querySelectorAll('.sec').forEach((el) => {
      const b = el.getBoundingClientRect();
      let last = 0; [...el.children].forEach((c) => { const r = c.getBoundingClientRect(); if (getComputedStyle(c).position !== 'absolute') last = Math.max(last, r.bottom); });
      out[el.id] = { h: Math.round(b.height), scrollH: el.scrollHeight, slackBottom: Math.round(b.bottom - last) };
    });
    const f = byId('foot').getBoundingClientRect(); out.foot = [Math.round(f.top), Math.round(f.bottom)];
    const st = byId('subtitle').getBoundingClientRect(); out.sub = [Math.round(st.left), Math.round(st.right), Math.round(st.top), Math.round(st.bottom)];
    const tt = byId('titleText').getBoundingClientRect(); out.title = [Math.round(tt.left), Math.round(tt.right), Math.round(tt.top), Math.round(tt.bottom)];
    return out;
  };

  const go = () => Promise.all([
    document.fonts.load("700 40px 'Caveat'", 'AäÄ'), document.fonts.load("18px 'Patrick Hand'", 'aäÄ'), document.fonts.load("700 18px 'Kalam'", 'aäÄ'),
  ]).then(() => document.fonts.ready).then(draw);
  if (document.readyState === 'complete') go(); else window.addEventListener('load', go);
})();
