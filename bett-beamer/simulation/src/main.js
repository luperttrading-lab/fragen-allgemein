// Simulation: Bett 200x200 mit Holzverkleidung und Beamer-Fussbank (Variante A offen, Variante C Motor-Schieber)
// Masse wie in zeichnungen.py (Meter). three.js-Koordinaten: x = Breite (X), y = Hoehe (Z), z = -Laengsachse (-Y)
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { RoundedBoxGeometry } from 'three/addons/geometries/RoundedBoxGeometry.js';
import { RectAreaLightUniformsLib } from 'three/addons/lights/RectAreaLightUniformsLib.js';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';

// ------------------------------------------------------------------ Masse (m)
const M = {
  bettB: 2.098, bettL: 2.098, bettH: 0.21, vk: 0.019, boden: 0.01,
  matrH: 0.20, bankT: 0.52, fuge: 0.01, pl: 0.019,
  wand: 2.5 + 0.53, raumH: 2.5, wandLinks: -1.65, wandRechts: 2.55, kopfwand: 2.118,
  linseY: 0.103, linseZ: 0.466, linseR: 0.028,
  fx: 0.08, fz0: 0.068, fz1: 0.191,
  bildB: 2.2, bildUK: 0.75,
};
M.bildH = M.bildB * 10 / 16;
const XB = M.bettB / 2;
const zB0 = -M.fuge, zB1 = -(M.fuge + M.bankT);           // Bank: bettseitig / wandseitig
const yBo = M.boden + M.pl, yDe = M.bettH - M.pl;          // OK Boden, UK Deckel

// ------------------------------------------------------------------ Renderer, Szene
const canvas = document.getElementById('c');
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, preserveDrawingBuffer: true });
renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 0.82;
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x101010);
const pmrem = new THREE.PMREMGenerator(renderer);
scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;
scene.environmentIntensity = 0.35;
RectAreaLightUniformsLib.init();
const camera = new THREE.PerspectiveCamera(55, 1, 0.02, 40);
const controls = new OrbitControls(camera, canvas);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
const ANISO = renderer.capabilities.getMaxAnisotropy();

// ------------------------------------------------------------------ Texturen
function rng(seed) {
  let s = seed >>> 0;
  return () => { s = (Math.imul(s, 1664525) + 1013904223) >>> 0; return s / 4294967296; };
}

function holzCanvas(art, seed) {
  // 2,4 m x 0,6 m Leimholz: Lamellen 40-90 mm, Maserung, Poren (Eiche) bzw. Aeste (Kiefer)
  const W = 2048, H = 512, c = document.createElement('canvas');
  c.width = W; c.height = H;
  const g = c.getContext('2d');
  const R = rng(seed);
  const base = art === 'eiche' ? [150, 104, 62] : [214, 172, 118];
  let y = 0;
  while (y < H) {
    const h = (0.04 + R() * 0.05) / 0.6 * H;
    const t = (R() - 0.5) * (art === 'eiche' ? 0.22 : 0.14);
    const col = base.map(v => Math.max(0, Math.min(255, v * (1 + t))));
    const grad = g.createLinearGradient(0, y, 0, y + h);
    grad.addColorStop(0, `rgb(${col.map(v => v * 0.97)})`);
    grad.addColorStop(0.5, `rgb(${col})`);
    grad.addColorStop(1, `rgb(${col.map(v => v * 0.95)})`);
    g.fillStyle = grad;
    g.fillRect(0, y, W, h + 1);
    const n = Math.floor(h / (art === 'eiche' ? 2.2 : 3.5));
    for (let i = 0; i < n; i++) {
      const yy = y + R() * h, amp = 0.6 + R() * 3.5, f = 0.0015 + R() * 0.005, ph = R() * 6.28;
      const d = 0.55 + R() * 0.3;
      g.strokeStyle = `rgba(${col.map(v => Math.floor(v * d))},${0.10 + R() * 0.30})`;
      g.lineWidth = 0.5 + R() * (art === 'eiche' ? 1.4 : 2.4);
      g.beginPath();
      for (let x = 0; x <= W; x += 12) {
        const yv = yy + Math.sin(x * f + ph) * amp + Math.sin(x * f * 3.3 + ph * 1.7) * amp * 0.35;
        if (x === 0) g.moveTo(x, yv); else g.lineTo(x, yv);
      }
      g.stroke();
    }
    if (art === 'eiche') {
      for (let i = 0; i < h * 9; i++) {
        const px = R() * W, py = y + R() * h;
        g.fillStyle = `rgba(70,45,25,${0.10 + R() * 0.25})`;
        g.fillRect(px, py, 2 + R() * 9, 0.8);
      }
      for (let i = 0; i < h / 25; i++) { // Spiegel (Markstrahlen)
        const px = R() * W, py = y + R() * h;
        g.fillStyle = `rgba(230,200,160,${0.08 + R() * 0.1})`;
        g.beginPath();
        g.ellipse(px, py, 8 + R() * 30, 1 + R() * 2, 0, 0, 6.28);
        g.fill();
      }
    } else if (R() < 0.6) {
      const kx = R() * W, ky = y + h * (0.3 + R() * 0.4), kr = 5 + R() * 12;
      for (let r = kr * 2.4; r > 0; r -= 2.2) {
        g.strokeStyle = `rgba(120,70,30,${0.25 + 0.5 * (1 - r / (kr * 2.4))})`;
        g.lineWidth = 1.2;
        g.beginPath();
        g.ellipse(kx, ky, r * 1.6, r * 0.7, 0, 0, 6.28);
        g.stroke();
      }
      g.fillStyle = 'rgba(95,55,25,0.85)';
      g.beginPath();
      g.ellipse(kx, ky, kr * 0.9, kr * 0.55, 0, 0, 6.28);
      g.fill();
    }
    g.fillStyle = 'rgba(60,40,20,0.25)';
    g.fillRect(0, y + h - 1, W, 1);
    y += h;
  }
  return c;
}

function canvasTex(cv, repeat = [1, 1]) {
  const t = new THREE.CanvasTexture(cv);
  t.colorSpace = THREE.SRGBColorSpace;
  t.wrapS = t.wrapT = THREE.RepeatWrapping;
  t.repeat.set(repeat[0], repeat[1]);
  t.anisotropy = ANISO;
  return t;
}

function parkettCanvas() {
  const W = 2048, H = 2048, c = document.createElement('canvas'); // 2,4 m x 2,4 m
  c.width = W; c.height = H;
  const g = c.getContext('2d');
  const R = rng(7);
  const bw = 0.09 / 2.4 * W;
  for (let x = 0; x < W; x += bw) {
    let y = -R() * 400;
    while (y < H) {
      const len = (0.4 + R() * 0.35) / 2.4 * H;
      const t = (R() - 0.5) * 0.14;
      const col = [136, 72, 46].map(v => Math.max(0, Math.min(255, v * (1 + t))));
      g.fillStyle = `rgb(${col})`;
      g.fillRect(x, y, bw, len);
      for (let i = 0; i < 26; i++) {
        const xx = x + R() * bw, amp = 0.5 + R() * 2;
        g.strokeStyle = `rgba(${col.map(v => Math.floor(v * 0.72))},${0.12 + R() * 0.25})`;
        g.lineWidth = 0.6 + R() * 1.2;
        g.beginPath();
        for (let yy = y; yy <= y + len; yy += 10) {
          const xv = xx + Math.sin(yy * 0.01 + i) * amp;
          if (yy === y) g.moveTo(xv, yy); else g.lineTo(xv, yy);
        }
        g.stroke();
      }
      g.fillStyle = 'rgba(50,25,10,0.55)';
      g.fillRect(x, y, bw, 1.5);
      y += len;
    }
    g.fillStyle = 'rgba(50,25,10,0.55)';
    g.fillRect(x, 0, 1.5, H);
  }
  return c;
}

function karoCanvas() {
  const c = document.createElement('canvas');
  c.width = c.height = 512;
  const g = c.getContext('2d');
  g.fillStyle = '#b4b8b2';
  g.fillRect(0, 0, 512, 512);
  g.strokeStyle = 'rgba(250,250,246,0.35)';
  g.lineWidth = 3;
  for (let i = 0; i <= 512; i += 32) {
    g.beginPath(); g.moveTo(i, 0); g.lineTo(i, 512); g.stroke();
    g.beginPath(); g.moveTo(0, i); g.lineTo(512, i); g.stroke();
  }
  return c;
}

function bildCanvas() {
  // Filmbild: Bergsee bei Sonnenuntergang (16:10)
  const W = 1600, H = 1000, c = document.createElement('canvas');
  c.width = W; c.height = H;
  const g = c.getContext('2d');
  const sky = g.createLinearGradient(0, 0, 0, H * 0.62);
  sky.addColorStop(0, '#1d2b5a'); sky.addColorStop(0.45, '#7b4a8e');
  sky.addColorStop(0.75, '#f08a4b'); sky.addColorStop(1, '#ffd27a');
  g.fillStyle = sky; g.fillRect(0, 0, W, H * 0.62);
  const sun = g.createRadialGradient(W * 0.62, H * 0.56, 10, W * 0.62, H * 0.56, 260);
  sun.addColorStop(0, 'rgba(255,250,215,1)'); sun.addColorStop(0.18, 'rgba(255,225,150,0.95)');
  sun.addColorStop(1, 'rgba(255,170,90,0)');
  g.fillStyle = sun; g.fillRect(0, 0, W, H * 0.62);
  const R = rng(3);
  const berg = (yb, amp, col, seed) => {
    const r = rng(seed);
    g.fillStyle = col;
    g.beginPath(); g.moveTo(0, H * 0.62);
    let y = yb;
    for (let x = 0; x <= W; x += 20) { y += (r() - 0.5) * amp; y = Math.max(yb - amp * 4, Math.min(yb + amp * 2, y)); g.lineTo(x, y); }
    g.lineTo(W, H * 0.62); g.closePath(); g.fill();
  };
  berg(H * 0.38, 26, '#5b3f6e', 11);
  berg(H * 0.47, 22, '#3a2b4f', 12);
  berg(H * 0.55, 14, '#1e1a2c', 13);
  const see = g.createLinearGradient(0, H * 0.62, 0, H);
  see.addColorStop(0, '#e9915a'); see.addColorStop(0.3, '#6c4a78'); see.addColorStop(1, '#141a33');
  g.fillStyle = see; g.fillRect(0, H * 0.62, W, H * 0.38);
  for (let i = 0; i < 120; i++) {
    g.fillStyle = `rgba(255,220,160,${0.15 + R() * 0.35})`;
    const w = 20 + R() * 160;
    g.fillRect(W * 0.62 - w / 2 + (R() - 0.5) * 120, H * 0.63 + R() * H * 0.3, w, 2);
  }
  return c;
}

// ------------------------------------------------------------------ Materialien
const holzTex = { eiche: [], kiefer: [] };
for (let i = 0; i < 4; i++) {
  holzTex.eiche.push(canvasTex(holzCanvas('eiche', 101 + i)));
  holzTex.kiefer.push(canvasTex(holzCanvas('kiefer', 201 + i)));
}
const matHolz = [0, 1, 2, 3].map(i => new THREE.MeshStandardMaterial({ map: holzTex.eiche[i], roughness: 0.58, metalness: 0 }));
const matHolzBank = [0, 1, 2, 3].map(i => new THREE.MeshStandardMaterial({ map: holzTex.eiche[i], roughness: 0.58, metalness: 0 }));
const matKiefer = new THREE.MeshStandardMaterial({ map: holzTex.kiefer[0], roughness: 0.65 });
const matSchwarz = new THREE.MeshStandardMaterial({ color: 0x0b0b0b, roughness: 0.9 });
const matWand = new THREE.MeshStandardMaterial({ color: 0xe9e5dd, roughness: 0.95 });
const matDecke = new THREE.MeshStandardMaterial({ color: 0xf6f4ef, roughness: 0.95 });
const matLaken = new THREE.MeshStandardMaterial({ color: 0xf4f5f7, roughness: 0.92 });
const matDuvet = new THREE.MeshStandardMaterial({ map: canvasTex(karoCanvas(), [3, 3]), roughness: 0.95 });
const matDecke2 = new THREE.MeshStandardMaterial({ color: 0x2c2d31, roughness: 0.98 });
const matWeissKunst = new THREE.MeshStandardMaterial({ color: 0xeeeeea, roughness: 0.45 });
const matAlu = new THREE.MeshStandardMaterial({ color: 0xb8bcc2, roughness: 0.35, metalness: 0.9 });
const matAluSchwarz = new THREE.MeshStandardMaterial({ color: 0x151515, roughness: 0.55, metalness: 0.4 });
const matLinse = new THREE.MeshPhysicalMaterial({ color: 0x05070c, roughness: 0.05, metalness: 0.1, clearcoat: 1, emissive: 0x000000 });
const matSockel = new THREE.MeshStandardMaterial({ color: 0x5a3220, roughness: 0.6 });
const parkett = canvasTex(parkettCanvas(), [M.wandRechts - M.wandLinks, M.wand + M.kopfwand].map(v => v / 2.4));
const matBoden = new THREE.MeshStandardMaterial({ map: parkett, roughness: 0.45 });

// ------------------------------------------------------------------ Bauteile
const SU = 1 / 2.4, SV = 1 / 0.6;
function holzBox(w, h, d, mat, x, y, z, seed = 1) {
  const geo = new THREE.BoxGeometry(w, h, d);
  const uv = geo.attributes.uv;
  const dims = [[d, h], [d, h], [w, d], [w, d], [w, h], [w, h]];
  const R = rng(seed * 977 + Math.floor((x + y + z) * 1000));
  for (let f = 0; f < 6; f++) {
    const [du, dv] = dims[f];
    const ox = R() * 3, oy = R() * 3;
    for (let i = f * 4; i < f * 4 + 4; i++) {
      const u0 = uv.getX(i), v0 = uv.getY(i);
      if (dv > du) uv.setXY(i, v0 * dv * SU + ox, u0 * du * SV + oy);
      else uv.setXY(i, u0 * du * SU + ox, v0 * dv * SV + oy);
    }
  }
  const m = new THREE.Mesh(geo, mat);
  m.position.set(x, y, z);
  m.castShadow = m.receiveShadow = true;
  return m;
}

function box(w, h, d, mat, x, y, z, rund = 0) {
  const geo = rund > 0 ? new RoundedBoxGeometry(w, h, d, 3, rund) : new THREE.BoxGeometry(w, h, d);
  const m = new THREE.Mesh(geo, mat);
  m.position.set(x, y, z);
  m.castShadow = m.receiveShadow = true;
  return m;
}

function platteMitLoechern(umriss, loecher, dicke, mat, kante = matSchwarz) {
  const s = new THREE.Shape(umriss.map(p => new THREE.Vector2(p[0], p[1])));
  for (const l of loecher) s.holes.push(new THREE.Path(l.map(p => new THREE.Vector2(p[0], p[1]))));
  const geo = new THREE.ExtrudeGeometry(s, { depth: dicke, bevelEnabled: false });
  const uv = geo.attributes.uv;
  for (let i = 0; i < uv.count; i++) uv.setXY(i, uv.getX(i) * SU + 0.37, uv.getY(i) * SV + 0.11);
  const m = new THREE.Mesh(geo, [mat, kante]);
  m.castShadow = m.receiveShadow = true;
  return m;
}
const rechteck = (x0, y0, x1, y1) => [[x0, y0], [x1, y0], [x1, y1], [x0, y1]];

// --- Raum
const raum = new THREE.Group();
scene.add(raum);
const rb = M.wandRechts - M.wandLinks, rl = M.wand + M.kopfwand;
const boden = new THREE.Mesh(new THREE.PlaneGeometry(rb, rl), matBoden);
boden.rotation.x = -Math.PI / 2;
boden.position.set((M.wandLinks + M.wandRechts) / 2, 0, (M.kopfwand - M.wand) / 2);
boden.receiveShadow = true;
raum.add(boden);
const decke = new THREE.Mesh(new THREE.PlaneGeometry(rb, rl), matDecke);
decke.rotation.x = Math.PI / 2;
decke.position.set(boden.position.x, M.raumH, boden.position.z);
raum.add(decke);
function wand(w, x, z, ry) {
  const m = new THREE.Mesh(new THREE.PlaneGeometry(w, M.raumH), matWand);
  m.position.set(x, M.raumH / 2, z);
  m.rotation.y = ry;
  m.receiveShadow = true;
  raum.add(m);
  return m;
}
wand(rb, boden.position.x, -M.wand, 0);                        // Projektionswand
wand(rb, boden.position.x, M.kopfwand, Math.PI);               // Kopfwand
wand(rl, M.wandLinks, boden.position.z, Math.PI / 2);          // Heizkoerperwand
wand(rl, M.wandRechts, boden.position.z, -Math.PI / 2);
// Sockelleisten
raum.add(box(rb, 0.06, 0.012, matSockel, boden.position.x, 0.03, -M.wand + 0.006));
raum.add(box(rb, 0.06, 0.012, matSockel, boden.position.x, 0.03, M.kopfwand - 0.006));
raum.add(box(0.012, 0.06, rl, matSockel, M.wandLinks + 0.006, 0.03, boden.position.z));
raum.add(box(0.012, 0.06, rl, matSockel, M.wandRechts - 0.006, 0.03, boden.position.z));
// Heizkoerper an der linken Wand (vom Bett aus)
const hk = new THREE.Group();
for (let i = 0; i < 26; i++) hk.add(box(0.1, 0.6, 0.035, matWeissKunst, M.wandLinks + 0.07, 0.45, 0.45 + i * 0.045, 0.006));
raum.add(hk);
// Dosen + Kabelkanal zur Bank
raum.add(box(0.012, 0.08, 0.16, matWeissKunst, M.wandLinks + 0.006, 0.45, -0.28));
raum.add(box(0.012, 0.08, 0.24, matWeissKunst, M.wandLinks + 0.006, 0.25, -1.05));
raum.add(box(0.02, 0.015, 0.8, matWeissKunst, M.wandLinks + 0.07, 0.0075, -0.65));
raum.add(box(0.6 - 0.07, 0.012, 0.05, matWeissKunst, (M.wandLinks + 0.07 - XB) / 2 - 0.02, 0.006, -0.27));
// Deckenleuchte
raum.add(box(0.35, 0.05, 0.35, matWeissKunst, 0.3, M.raumH - 0.025, -0.2, 0.02));

// --- Bett
const bett = new THREE.Group();
scene.add(bett);
const zBett = M.bettL / 2;
bett.add(holzBox(M.bettB - 2 * M.vk, M.bettH - 0.002, M.bettL - 2 * M.vk, matKiefer, 0, M.bettH / 2, zBett, 3));
bett.add(holzBox(M.vk, M.bettH - M.boden, M.bettL, matHolz[0], -XB + M.vk / 2, M.boden + (M.bettH - M.boden) / 2, zBett, 4));
bett.add(holzBox(M.vk, M.bettH - M.boden, M.bettL, matHolz[1], XB - M.vk / 2, M.boden + (M.bettH - M.boden) / 2, zBett, 5));
bett.add(holzBox(M.bettB - 2 * M.vk, M.bettH - M.boden, M.vk, matHolz[2], 0, M.boden + (M.bettH - M.boden) / 2, M.vk / 2, 6));
bett.add(holzBox(M.bettB - 2 * M.vk, M.bettH - M.boden, M.vk, matHolz[3], 0, M.boden + (M.bettH - M.boden) / 2, M.bettL - M.vk / 2, 7));
for (const xm of [-0.5, 0.5]) bett.add(box(0.995, M.matrH, 1.995, matLaken, xm, M.bettH + M.matrH / 2, zBett, 0.035));
const yM = M.bettH + M.matrH;
for (const xm of [-0.5, 0.5]) bett.add(box(0.62, 0.11, 0.4, matLaken, xm, yM + 0.05, M.bettL - 0.3, 0.05));
const duvet = box(0.98, 0.07, 1.35, matDuvet, 0.5, yM + 0.035, 0.95, 0.03);
duvet.rotation.y = 0.04;
bett.add(duvet);
const decke2 = box(0.8, 0.09, 0.9, matDecke2, -0.45, yM + 0.045, 1.35, 0.04);
decke2.rotation.y = -0.25;
bett.add(decke2);

// --- Bank
const bank = new THREE.Group();
scene.add(bank);
const huelle = [];                    // Teile, die im Roentgenmodus durchsichtig werden
function hb(m) { bank.add(m); huelle.push(m); return m; }
const zMit = (zB0 + zB1) / 2;
hb(holzBox(M.bettB, M.pl, M.bankT, matHolzBank[0], 0, M.boden + M.pl / 2, zMit, 11));          // Boden
hb(holzBox(M.bettB - 2 * M.pl, yDe - yBo, M.pl, matHolzBank[1], 0, (yBo + yDe) / 2, zB0 - M.pl / 2, 12)); // Rueckwand
// Front mit Fensterausschnitt (bis unter den Deckel)
const xi = XB - M.pl;
const front = platteMitLoechern([[-xi, yBo], [xi, yBo], [xi, yDe], [M.fx, yDe], [M.fx, M.fz0], [-M.fx, M.fz0], [-M.fx, yDe], [-xi, yDe]],
  [], M.pl, matHolzBank[2], matHolzBank[2]);
front.position.z = zB1;
hb(front);
// Stirnseiten mit Schlitzfeld 5 x 440 x 13
const schlitze = [];
for (let k = 0; k < 5; k++) schlitze.push(rechteck(0.03, 0.05 + 0.025 * k, 0.47, 0.063 + 0.025 * k));
for (const sx of [-XB, XB - M.pl]) {
  const st = platteMitLoechern(rechteck(0, yBo, M.bankT, yDe), schlitze, M.pl, matHolzBank[3]);
  st.rotation.y = Math.PI / 2;
  st.position.set(sx, 0, zB0);
  hb(st);
}
// Deckel in drei Teilen mit Fugen
const deckelTeile = [[-XB, -0.3405], [-0.3385, 0.6285], [0.6305, XB]];
deckelTeile.forEach(([a, b], i) => hb(holzBox(b - a, M.pl, M.bankT, matHolzBank[i], (a + b) / 2, yDe + M.pl / 2, zMit, 20 + i)));

// Innenleben
const innen = new THREE.Group();
bank.add(innen);
const matInnenSchwarz = new THREE.MeshStandardMaterial({ color: 0x111111, roughness: 0.95 });
innen.add(box(0.019, yDe - yBo, M.bankT - 2 * M.pl, matHolzBank[1], -0.3395, (yBo + yDe) / 2, zMit));       // T1
innen.add(box(0.019, yDe - yBo, M.bankT - 2 * M.pl, matHolzBank[2], 0.6295, (yBo + yDe) / 2, zMit));        // T2
innen.add(box(0.9, 0.002, M.bankT - 2 * M.pl, matInnenSchwarz, 0.14, yBo + 0.001, zMit));                   // schwarzer Boden Beamerfach
// Luefter + Traeger, Filtermatte
innen.add(box(0.019, yDe - yBo, M.bankT - 2 * M.pl, matHolzBank[3], -XB + M.pl + 0.09, (yBo + yDe) / 2, zMit));
for (const zz of [-0.18, -0.36]) {
  innen.add(box(0.025, 0.14, 0.14, new THREE.MeshStandardMaterial({ color: 0x1b1b1b, roughness: 0.6 }), -XB + M.pl + 0.068, 0.11, zz, 0.008));
}
innen.add(box(0.012, yDe - yBo - 0.01, 0.46, new THREE.MeshStandardMaterial({ color: 0x2a2a2e, roughness: 1 }), XB - M.pl - 0.008, (yBo + yDe) / 2, -0.27));
// Beamer
const beamer = new THREE.Group();
innen.add(beamer);
const pjX0 = 0.104 - 0.399;
beamer.add(box(0.399, 0.115, 0.348, matWeissKunst, pjX0 + 0.1995, yBo + 0.01 + 0.0575, -(0.466 - 0.174), 0.012));
for (const [fx, fz] of [[pjX0 + 0.05, -0.15], [pjX0 + 0.35, -0.15], [pjX0 + 0.2, -0.42]]) {
  beamer.add(box(0.03, 0.01, 0.03, matSchwarz, fx, yBo + 0.005, fz));
}
const ring = new THREE.Mesh(new THREE.CylinderGeometry(0.036, 0.038, 0.018, 40), matAlu);
ring.rotation.x = Math.PI / 2;
ring.position.set(0, M.linseY, -M.linseZ + 0.004);
beamer.add(ring);
const glas = new THREE.Mesh(new THREE.CircleGeometry(0.027, 40), matLinse);
glas.position.set(0, M.linseY, -M.linseZ - 0.0055);
glas.rotation.y = Math.PI;
beamer.add(glas);
const gitter = box(0.2, 0.06, 0.004, new THREE.MeshStandardMaterial({ color: 0x9a9a9a, roughness: 0.7 }), pjX0 + 0.13, yBo + 0.075, -M.linseZ - 0.001);
beamer.add(gitter);
// Technik
const geraete = [
  [0.127, 0.05, 0.127, 0xc9cbd0, 0.7235, -0.3635, 0.02, 0.6],   // Mac mini
  [0.095, 0.031, 0.095, 0x111111, 0.8525, -0.3775, 0.012, 0.4], // Apple TV
  [0.173, 0.104, 0.054, 0x202020, 0.7465, -0.472, 0.008, 0.5],  // Switch-Dock
  [0.16, 0.025, 0.054, 0x303030, 0.93, -0.472, 0.004, 0.5],     // HDMI-Switch
  [0.10, 0.02, 0.125, 0x1f6b3a, 0.965, -0.3625, 0.002, 0.6],    // Relais K1 K2 K4
  [0.15, 0.05, 0.09, 0x2b2b2b, 0.735, -0.235, 0.004, 0.6],      // Netzteil
  [0.09, 0.07, 0.09, 0xeeeeee, 0.87, -0.235, 0.006, 0.5],       // K3 in Dose
  [0.085, 0.03, 0.09, 0x2f2f2f, 0.9725, -0.235, 0.004, 0.5],    // LAN
  [0.3, 0.04, 0.06, 0xf0f0f0, 0.81, -0.125, 0.008, 0.5],        // Steckdosenleiste
];
for (const [w, h, d, col, x, z, r, rough] of geraete) {
  innen.add(box(w, h, d, new THREE.MeshStandardMaterial({ color: col, roughness: rough, metalness: col === 0xc9cbd0 ? 0.8 : 0 }), x, yBo + h / 2, z, r));
}

// Schieber-Mechanik (nur Variante C)
const mech = new THREE.Group();
bank.add(mech);
const zFi = zB1 + M.pl;                 // Innenseite Front
const schieber = holzBox(0.2, 0.127, 0.004, matHolzBank[1], 0, 0.1215, zFi + 0.006, 31);   // Eiche-Sperrholz 4 mm, wie die Bank
mech.add(schieber);
for (const yy of [0.058, 0.185]) mech.add(holzBox(0.47, 0.012, 0.012, matHolzBank[0], 0.105, yy, zFi + 0.006, 40 + yy * 100));  // Eiche-Nutleisten
const antrieb = new THREE.Mesh(new THREE.CylinderGeometry(0.018, 0.018, 0.3, 24), new THREE.MeshStandardMaterial({ color: 0x5a5d63, roughness: 0.5, metalness: 0.5 }));
antrieb.rotation.z = Math.PI / 2;
antrieb.position.set(0.45, M.linseY, zFi + 0.025);
mech.add(antrieb);
const stange = new THREE.Mesh(new THREE.CylinderGeometry(0.006, 0.006, 1, 16), matAlu);
stange.rotation.z = Math.PI / 2;
mech.add(stange);
mech.add(box(0.04, 0.08, 0.044, matHolzBank[0], 0.62, M.linseY, zFi + 0.022));
const endschalter = box(0.022, 0.012, 0.012, new THREE.MeshStandardMaterial({ color: 0xd04040, roughness: 0.6 }), 0.315, 0.072, zFi + 0.01);
mech.add(endschalter);

// --- Bild an der Wand + Strahl + Licht
const bildMat = new THREE.MeshBasicMaterial({ map: canvasTex(bildCanvas()), toneMapped: false, transparent: true, opacity: 0 });
const bild = new THREE.Mesh(new THREE.PlaneGeometry(M.bildB, M.bildH), bildMat);
bild.position.set(0, M.bildUK + M.bildH / 2, -M.wand + 0.003);
scene.add(bild);
const apex = new THREE.Vector3(0, M.linseY, -M.linseZ - 0.01);
const ecken = [[-1, 0], [1, 0], [1, 1], [-1, 1]].map(([sx, sy]) => new THREE.Vector3(sx * M.bildB / 2, M.bildUK + sy * M.bildH, -M.wand + 0.004));
const pos = [], cols = [];
for (let i = 0; i < 4; i++) {
  const a = ecken[i], b = ecken[(i + 1) % 4];
  pos.push(apex.x, apex.y, apex.z, a.x, a.y, a.z, b.x, b.y, b.z);
  cols.push(1, 0.95, 0.85, 0.18, 0.16, 0.14, 0.18, 0.16, 0.14);
}
const strahlGeo = new THREE.BufferGeometry();
strahlGeo.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
strahlGeo.setAttribute('color', new THREE.Float32BufferAttribute(cols, 3));
const strahlMat = new THREE.MeshBasicMaterial({ vertexColors: true, transparent: true, opacity: 0, blending: THREE.AdditiveBlending, depthWrite: false, side: THREE.DoubleSide, toneMapped: false });
scene.add(new THREE.Mesh(strahlGeo, strahlMat));
const bildLicht = new THREE.RectAreaLight(0xffc89a, 0, M.bildB, M.bildH);
bildLicht.position.copy(bild.position);
bildLicht.position.z += 0.02;
bildLicht.lookAt(0, bild.position.y, 0);
scene.add(bildLicht);

// --- Raumlicht
const hemi = new THREE.HemisphereLight(0xfff6ec, 0x8a6448, 0.75);
scene.add(hemi);
const spot = new THREE.SpotLight(0xffe2c0, 26, 0, 1.25, 0.9, 2);
spot.position.set(0.3, M.raumH - 0.06, -0.2);
spot.target.position.set(0.1, 0, -0.1);
spot.castShadow = true;
spot.shadow.mapSize.set(2048, 2048);
spot.shadow.bias = -0.0004;
spot.shadow.radius = 4;
scene.add(spot, spot.target);
const fenster = new THREE.DirectionalLight(0xdfe9ff, 0.55);
fenster.position.set(4, 3, -1);
scene.add(fenster);
const fuell = new THREE.DirectionalLight(0xfff1e0, 0.55);
fuell.position.set(-0.8, 1.8, -4);
scene.add(fuell);

// ------------------------------------------------------------------ Zustand, Animation
const state = { variant: 'C', kino: false, view: 'raum', xray: false, holz: 'eiche' };
let schieberT = 0, schieberZiel = 0, bildT = 0, bildZiel = 0, raumT = 1, raumZiel = 1;
const VIEWS = {
  raum:    { p: [2.25, 1.75, 1.85], t: [-0.25, 0.55, -1.6], fov: 62, name: 'Raum' },
  bett:    { p: [0.42, 0.67, 1.72], t: [0.0, 1.35, -3.03], fov: 62, name: 'Vom Bett (liegend)' },
  sitzend: { p: [0.42, 0.96, 1.55], t: [0.0, 1.2, -3.03], fov: 58, name: 'Halb sitzend' },
  bank:    { p: [1.25, 0.95, -2.35], t: [0.0, 0.12, -0.3], fov: 50, name: 'Bank von vorne' },
  detail:  { p: [0.3, 0.32, -1.0], t: [0.0, 0.11, -0.52], fov: 40, name: 'Fenster-Detail' },
  seite:   { p: [1.95, 0.62, -1.05], t: [0.85, 0.12, -0.27], fov: 50, name: 'Stirnseite' },
};
let camAnim = null;
let basisFov = 55;
function fovFuer(f) {
  // Hochformat (Handy): vertikalen Winkel so weiten, dass der horizontale Ausschnitt wie bei 16:10 bleibt
  const a = camera.aspect || 1.6;
  if (a >= 1.6) return f;
  const h = 2 * Math.atan(Math.tan(f * Math.PI / 360) * 1.6 / a) * 180 / Math.PI;
  return Math.min(h, 100);
}

function setView(name, sofort) {
  const v = VIEWS[name];
  state.view = name;
  const ziel = { p: new THREE.Vector3(...v.p), t: new THREE.Vector3(...v.t), fov: v.fov };
  if (sofort) {
    camera.position.copy(ziel.p); controls.target.copy(ziel.t); basisFov = ziel.fov; camera.fov = fovFuer(basisFov); camera.updateProjectionMatrix();
    camAnim = null;
  } else {
    camAnim = { p0: camera.position.clone(), t0: controls.target.clone(), f0: basisFov, ziel, t: 0 };
  }
  ui();
}

function setHolz(art) {
  state.holz = art;
  [...matHolz, ...matHolzBank].forEach((m, i) => { m.map = holzTex[art][i % 4]; m.needsUpdate = true; });
  ui();
}

function setXray(on) {
  state.xray = on;
  for (const m of huelle) {
    const mats = Array.isArray(m.material) ? m.material : [m.material];
    m.material = mats.map(mt => {
      const c = mt.userData.orig || mt;
      if (!on) return c;
      const x = c.clone();
      x.userData.orig = c;
      x.transparent = true; x.opacity = 0.14; x.depthWrite = false;
      return x;
    });
    if (m.material.length === 1) m.material = m.material[0];
    m.castShadow = !on;
  }
  ui();
}

function setVariant(v, sofort) {
  state.variant = v;
  mech.visible = v === 'C';
  if (v === 'A') { schieberZiel = 1; if (sofort) schieberT = 1; }
  else { schieberZiel = state.kino ? 1 : 0; if (sofort) schieberT = schieberZiel; }
  if (sofort) { bildT = bildZiel = state.kino ? 1 : 0; }
  ui();
}

function setKino(on, sofort) {
  state.kino = on;
  raumZiel = on ? 0.05 : 1;
  if (state.variant === 'C') {
    schieberZiel = on ? 1 : 0;
    bildZiel = on && schieberT >= 0.999 ? 1 : 0;
  } else {
    schieberZiel = 1;
    bildZiel = on ? 1 : 0;
  }
  if (sofort) { schieberT = schieberZiel; bildT = on ? 1 : 0; raumT = raumZiel; }
  ui();
}

function status() {
  if (state.variant === 'A') return state.kino ? 'Variante A: offenes Fenster, Beamer läuft (Ein/Aus mit seiner Fernbedienung).'
    : 'Variante A: offenes Fenster, Beamer aus. Linse sichtbar – nur von der Wandseite.';
  if (state.kino && schieberT < 0.999) return 'Einmal gedrückt → Motorschieber fährt auf (hier beschleunigt, in echt ≈ 5 s) …';
  if (state.kino) return 'Schieber ganz offen → Beamer bekommt Strom und startet von selbst. Nochmal drücken = zu und Beamer aus.';
  if (schieberT > 0.001) return 'Nochmal gedrückt → Beamer sofort stromlos, Holzschieber fährt zu, Lüfter laufen 5 min nach.';
  return 'Holzschieber zu (gleiches Holz wie die Bank, 2,5 cm zurückgesetzt), Beamer stromlos.';
}

let uiFn = () => {};
function ui() { uiFn(); }

const uhr = new THREE.Clock();
function update(dt) {
  const vS = state.variant === 'C' ? 0.5 : 10;          // Schieber: 2 s Demo
  if (schieberT < schieberZiel) schieberT = Math.min(schieberZiel, schieberT + dt * vS);
  if (schieberT > schieberZiel) schieberT = Math.max(schieberZiel, schieberT - dt * vS);
  if (state.variant === 'C' && state.kino && schieberT >= 0.999) bildZiel = 1;
  if (!state.kino) bildZiel = 0;
  bildT += Math.sign(bildZiel - bildT) * Math.min(Math.abs(bildZiel - bildT), dt * (bildZiel > bildT ? 1.6 : 6));
  raumT += Math.sign(raumZiel - raumT) * Math.min(Math.abs(raumZiel - raumT), dt * 1.2);
  anwenden();
  if (camAnim) {
    camAnim.t = Math.min(1, camAnim.t + dt / 0.9);
    const k = camAnim.t < 0.5 ? 2 * camAnim.t * camAnim.t : 1 - Math.pow(-2 * camAnim.t + 2, 2) / 2;
    camera.position.lerpVectors(camAnim.p0, camAnim.ziel.p, k);
    controls.target.lerpVectors(camAnim.t0, camAnim.ziel.t, k);
    basisFov = camAnim.f0 + (camAnim.ziel.fov - camAnim.f0) * k;
    camera.fov = fovFuer(basisFov);
    camera.updateProjectionMatrix();
    if (camAnim.t >= 1) camAnim = null;
  }
}

function anwenden() {
  const sx = 0.2 * schieberT;
  schieber.position.x = sx;
  const stEnd = 0.1 + sx;
  stange.position.set((stEnd + 0.3) / 2, M.linseY, zFi + 0.025);
  stange.scale.set(1, Math.max(0.001, 0.3 - stEnd), 1);
  bildMat.opacity = bildT;
  strahlMat.opacity = 0.018 * bildT;
  bildLicht.intensity = 2.2 * bildT;
  matLinse.emissive.setRGB(bildT * 0.9, bildT * 0.85, bildT * 0.75);
  hemi.intensity = 0.75 * raumT + 0.015;
  spot.intensity = 26 * raumT;
  fenster.intensity = 0.55 * raumT;
  fuell.intensity = 0.55 * raumT;
  scene.environmentIntensity = 0.35 * raumT + 0.02;
}

// ------------------------------------------------------------------ Film (deterministisch, Variante C)
const glatt = x => x <= 0 ? 0 : x >= 1 ? 1 : x * x * (3 - 2 * x);
function rampe(t, a, b) { return glatt((t - a) / (b - a)); }
const linear = (t, a, b) => Math.max(0, Math.min(1, (t - a) / (b - a)));
const FILM_DAUER = 29;
const FILM_KAMERA = [            // [Zeit s, Ansicht]
  [0, { p: [2.3, 1.95, 1.95], t: [-0.2, 0.5, -1.5], fov: 62 }], [3, 'raum'], [5.2, 'detail'], [13.6, 'detail'],
  [16.6, 'sitzend'], [20, 'sitzend'], [22.2, 'detail'], [FILM_DAUER, 'detail'],
];
const FILM_TEXT = [
  [0, 3, 'Beamer unsichtbar in der Fußbank am Bettende'],
  [3, 5.5, 'Von der Wandseite: Holzschieber zu, Beamer stromlos'],
  [5.5, 7, 'Einmal drücken: Motorschieber auf'],
  [7, 11.5, 'Schieber fährt auf – echte Geschwindigkeit (≈ 5 s)'],
  [11.5, 14, 'Schieber ganz offen: Beamer bekommt Strom und startet'],
  [16.6, 20, 'Blick vom Bett (halb sitzend), Bild 2,2 m breit'],
  [22.2, 23.7, 'Nochmal drücken: Motorschieber zu'],
  [23.7, FILM_DAUER, 'Beamer sofort stromlos – Holzschieber fährt zu, Lüfter laufen nach'],
];
function filmZeit(t) {
  state.variant = 'C'; mech.visible = true;
  schieberT = linear(t, 6.5, 11.5) * (1 - linear(t, 22.8, 27.8));     // Linearantrieb: konstante Geschwindigkeit
  const an = t >= 11.5 && t < 22.9;                                    // Endschalter oeffnet nach 1-2 mm Weg
  bildT = an ? rampe(t, 11.7, 13.2) : 0;
  raumT = 1 - 0.95 * rampe(t, 14, 16.3) * (1 - rampe(t, 20, 21.8));    // Raumlicht aus / wieder an
  anwenden();
  let i = 0;
  while (i < FILM_KAMERA.length - 2 && t > FILM_KAMERA[i + 1][0]) i++;
  const [t0, v0] = FILM_KAMERA[i], [t1, v1] = FILM_KAMERA[i + 1];
  const k = glatt((t - t0) / (t1 - t0));
  const a = typeof v0 === 'string' ? VIEWS[v0] : v0, b = typeof v1 === 'string' ? VIEWS[v1] : v1;
  camera.position.lerpVectors(new THREE.Vector3(...a.p), new THREE.Vector3(...b.p), k);
  controls.target.lerpVectors(new THREE.Vector3(...a.t), new THREE.Vector3(...b.t), k);
  basisFov = a.fov + (b.fov - a.fov) * k;
  resize();
  camera.fov = fovFuer(basisFov);
  camera.updateProjectionMatrix();
  camera.lookAt(controls.target);
  renderer.render(scene, camera);
}
window.__filmZeit = filmZeit;
window.__filmText = FILM_TEXT;
window.__filmDauer = FILM_DAUER;

function resize() {
  const w = canvas.clientWidth, h = canvas.clientHeight;
  if (canvas.width !== Math.floor(w * renderer.getPixelRatio()) || canvas.height !== Math.floor(h * renderer.getPixelRatio())) {
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    camera.fov = fovFuer(basisFov);
    camera.updateProjectionMatrix();
  }
}

let statusAlt = '';
function loop() {
  const dt = Math.min(uhr.getDelta(), 0.1);
  update(dt);
  resize();
  controls.update();
  renderer.render(scene, camera);
  const s = status();
  if (s !== statusAlt) { statusAlt = s; ui(); }
  requestAnimationFrame(loop);
}

// ------------------------------------------------------------------ Bedienoberflaeche
function knopf(text, aktiv, fn) {
  const b = document.createElement('button');
  b.textContent = text;
  if (aktiv) b.className = 'an';
  b.onclick = fn;
  return b;
}
const leiste = document.getElementById('leiste');
const info = document.getElementById('info');
uiFn = () => {
  leiste.innerHTML = '';
  // Bedienung nur noch ueber den Motorschieber (Variante A bleibt per ?variant=A fuer Standbilder erreichbar)
  const g2 = document.createElement('div');
  const kText = state.variant === 'C' ? (state.kino ? '■ Motorschieber zu' : '▶ Motorschieber auf') : (state.kino ? '■ Beamer aus' : '▶ Beamer an');
  g2.append(knopf(kText, state.kino, () => setKino(!state.kino)),
    knopf('Innenleben', state.xray, () => setXray(!state.xray)),
    knopf('Eiche', state.holz === 'eiche', () => setHolz('eiche')),
    knopf('Kiefer', state.holz === 'kiefer', () => setHolz('kiefer')));
  const g3 = document.createElement('div');
  for (const [k, v] of Object.entries(VIEWS)) g3.append(knopf(v.name, state.view === k, () => setView(k)));
  leiste.append(g2, g3);
  info.textContent = status();
};

// ------------------------------------------------------------------ Start
const q = new URLSearchParams(location.search);
if (q.get('holz')) setHolz(q.get('holz'));
setVariant(q.get('variant') || 'C', true);
setKino(q.get('kino') === '1', true);
if (q.get('xray') === '1') setXray(true);
setView(q.get('view') || 'raum', true);
if (q.get('ui') === '0') for (const id of ['leiste', 'kopf', 'hinweis']) document.getElementById(id).style.display = 'none';
update(0);
if (q.get('shot') === '1') {
  // Standbild: genau ein Bild rendern, keine Schleife (Software-Rendering ist langsam)
  resize();
  controls.update();
  renderer.render(scene, camera);
  window.__ready = true;
} else {
  loop();
}
