#!/usr/bin/env python3
"""Bauzeichnungen: Bett 200 x 200 mit Holzverkleidung und Beamer-Fussbank
(Panasonic PT-VMZ51S, verdeckt, motorischer Schieber).

Erzeugt Bauzeichnungen_Bett_Beamer.pdf (A3 quer, 4 Blaetter). Alle Masse in mm.
Annahmen (Bettmasse, Wandabstand, Raumhoehe) stehen oben als Parameter:
anpassen und neu erzeugen mit   python3 zeichnungen.py
Beamerwerte aus dem Panasonic-Datenblatt PT-VMZ51S (Stand 04/2023) und der
Bedienungsanleitung PT-VMZ71/61/51/51S/41.
"""
import math
import os

from reportlab.lib.colors import Color, black, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

HIER = os.path.dirname(os.path.abspath(__file__))
AUSGABE = os.path.join(HIER, "Bauzeichnungen_Bett_Beamer.pdf")

# ------------------------------------------------------------------ Parameter
DATUM = "10.11.2026"
# Raum – ANNAHMEN, bitte messen
A_WAND = 2500          # Vorderkante Bank (Wandseite) bis gegenueberliegende Wand
RAUM_H = 2500          # Raumhoehe
# Bett – Hoehe gemessen (Foto 10.11.), Laenge/Breite/Matratze noch ANNAHMEN
BETT_L = 2060          # Rahmen aussen, Laenge (A)
BETT_B = 2060          # Rahmen aussen, Breite (A)
BETT_H = 220           # Rahmenhoehe, gemessen
ROST_Z = 220           # Matratze liegt auf Rahmenoberkante (Foto)
MATR_H = 200           # Matratzenhoehe (A)  -> Matratzenoberkante 420
VK = 19                # Verkleidung Plattenstaerke
VK_BODEN = 10          # Luft Verkleidung - Fussboden
# Bank
FUGE = 10              # Trennfuge Bett | Bank (mechanische Entkopplung)
BANK_T = 520           # Tiefe
BANK_H = 500           # Hoehe
SOCKEL = 60            # Fusshoehe (verstellbare Moebelfuesse)
PL = 19                # Plattenstaerke Korpus
FRONTSPALT = 45        # Linsenfront bis Innenseite Frontplatte
# Beamer Panasonic PT-VMZ51S (Datenblatt)
PJ_B, PJ_T, PJ_H = 399, 348, 125   # B x T, H mit Fuessen kuerzeste Stellung
PJ_LINSE_SEITE = 104   # Linsenmitte ab Gehaeuseseite (Linsenseite)
PJ_LINSE_OBEN = 51     # Linsenmitte unter Gehaeuseoberkante
LINSE_R = 28           # Radius Frontlinse (aus Masszeichnung geschaetzt)
TR_MIN, TR_MAX = 1.09, 1.77
H_MIN, H_MAX = 0.056, 0.499        # Unterkante Bild ueber Linsenmitte / Bildhoehe
P_NORMAL, P_ECO, P_QUIET = 255, 180, 175   # W bei 200-240 V
LM_NORMAL, LM_ECO = 5200, 3640
# Vorhandener Beamer Panasonic PT-VX500 (Haendlerdaten, 2012) – passt ebenfalls in die Bank
VX_B, VX_T, VX_H = 379, 305, 107
VX_TIEFE_KABEL = 420   # gemessen inkl. Stecker
P_VX = 365             # W, Lampe 280 W
VX_TR_MIN, VX_TR_MAX = 1.18, 1.90
# Lueftung
LUEFTER = 140          # 2 Luefter, Kantenlaenge mm
VDOT_M3H = 150         # Volumenstrom (A)
P_GERAETE = 40         # Apple TV, Mac mini, Switch-Dock, HDMI-/LAN-Switch (A)
# Bildziel
BILD_B = 2000          # Bildbreite 16:10
BILD_UK = 800          # Unterkante Bild ueber Fussboden

# ------------------------------------------------------------------ Ableitungen
BETT_AX = BETT_B + 2 * VK               # Bett mit Verkleidung, Breite (X)
BETT_AY = BETT_L + 2 * VK               # Bett mit Verkleidung, Laenge (Y)
XB = BETT_AX / 2                        # halbe Breite = Bank-Halbbreite
MATR_OK = ROST_Z + MATR_H
Y_B0 = FUGE                             # Bank bettseitig
Y_B1 = FUGE + BANK_T                    # Bank wandseitig
Y_FI = Y_B1 - PL                        # Innenseite Front
Y_LF = Y_FI - FRONTSPALT                # Linsenfront
Y_PR = Y_LF - PJ_T                      # Beamer Rueckseite
Y_RI = Y_B0 + PL                        # Innenseite Rueckwand
Z_K0 = SOCKEL                           # Unterkante Korpus
Z_BO = SOCKEL + PL                      # Oberkante Boden
Z_DE = BANK_H - PL                      # Unterkante Deckel
Z_FB = BANK_H - PL - 50 - PJ_H         # Oberkante Beamerboden (50 mm Luft unter dem Deckel)
Z_L = Z_FB + PJ_H - PJ_LINSE_OBEN       # Linsenmitte
X_PJ0 = PJ_LINSE_SEITE - PJ_B           # Beamer Abluftseite (-X)
X_PJ1 = PJ_LINSE_SEITE                  # Beamer Linsenseite (+X)
X_T1 = -349                             # Trennwand 1 (Abluft), linke Kante
X_T2 = 620                              # Trennwand 2 (Technik), linke Kante
Y_WAND = Y_B1 + A_WAND
L_PROJ = Y_WAND - Y_LF                  # Projektionsabstand ab Linsenfront
SW, SH = BILD_B, BILD_B * 10 / 16
TR = L_PROJ / SW
H_SHIFT = (BILD_UK - Z_L) / SH
BILD_OK = BILD_UK + SH
# Fenster in der Front
F_X = 80                                # halbe Breite
F_Z0, F_Z1 = Z_L - 35, Z_L + 85
# Schieber
S_X0, S_X1 = -100, 100
S_Z0, S_Z1 = F_Z0 - 10, F_Z1 + 10
HUB = 200

assert TR_MIN <= TR <= TR_MAX, TR
assert H_MIN <= H_SHIFT <= H_MAX, H_SHIFT
assert S_Z1 + 4 < BANK_H - PL, "obere Schieberfuehrung stoesst an den Deckel"
assert VX_TIEFE_KABEL + 20 <= (FUGE + BANK_T - PL) - (FUGE + PL), "VX500 passt nicht in die Tiefe"

# ------------------------------------------------------------------ Grafik
pdfmetrics.registerFont(TTFont("DV", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DVB", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))
MM = 72 / 25.4
SEITE_B, SEITE_H = 420, 297

C_HOLZ = Color(0.93, 0.84, 0.66)
C_VK = Color(0.80, 0.64, 0.42)
C_PJ = Color(0.35, 0.50, 0.80)
C_STRAHL = Color(1.0, 0.82, 0.15)
C_KALT = Color(0.10, 0.45, 0.90)
C_WARM = Color(0.85, 0.15, 0.10)
C_GRAU = Color(0.55, 0.55, 0.55)
C_HELLGRAU = Color(0.90, 0.90, 0.90)
C_ALU = Color(0.62, 0.64, 0.68)
C_ROT = Color(0.80, 0.10, 0.10)
C_BILD = Color(0.20, 0.35, 0.75)

LW_DICK, LW_MITTEL, LW_DUENN, LW_FEIN = 0.5, 0.35, 0.18, 0.12


def fmt(v, nk=0):
    s = f"{v:,.{nk}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return s


class Blatt:
    def __init__(self, c, nr, gesamt, titel, inhalt, massstab):
        self.c = c
        c.saveState()
        c.scale(MM, MM)
        c.setLineJoin(1)
        c.setLineCap(1)
        c.setStrokeColor(black)
        c.setLineWidth(0.5)
        c.rect(10, 10, SEITE_B - 20, SEITE_H - 20)
        # Schriftfeld
        x0, y0, w, h = 250, 10, 160, 34
        c.setLineWidth(0.35)
        c.rect(x0, y0, w, h)
        c.setLineWidth(0.18)
        for yy in (y0 + 8, y0 + 15, y0 + 22):
            c.line(x0, yy, x0 + w, yy)
        c.line(x0 + 110, y0, x0 + 110, y0 + 15)
        c.setFont("DVB", 3.6)
        c.drawString(x0 + 2, y0 + 27.5, titel)
        c.setFont("DV", 2.6)
        c.drawString(x0 + 2, y0 + 17.2, inhalt)
        c.drawString(x0 + 2, y0 + 10.2, f"Maßstab: {massstab}   ·   Maße in mm   ·   Stand {DATUM}")
        c.drawString(x0 + 112, y0 + 10.2, f"Blatt {nr} / {gesamt}")
        c.setFont("DV", 2.2)
        c.setFillColor(C_ROT)
        c.drawString(x0 + 2, y0 + 3, "VORENTWURF – Bett- und Raummaße sind Annahmen (A): vor dem Zuschnitt messen!")
        c.setFillColor(black)
        c.drawString(x0 + 112, y0 + 3, "Beamer: PT-VMZ51S / PT-VX500")

    def fertig(self):
        self.c.restoreState()
        self.c.showPage()


class Ansicht:
    """Abbildung realer Koordinaten (mm) auf Papier (mm)."""

    def __init__(self, c, px, py, s, rx=0.0, ry=0.0, spiegel_x=False):
        self.c, self.px, self.py, self.s = c, px, py, s
        self.rx, self.ry, self.sx = rx, ry, (-1 if spiegel_x else 1)

    def p(self, x, y):
        return (self.px + self.sx * (x - self.rx) * self.s, self.py + (y - self.ry) * self.s)

    # --- Grundformen
    def _stil(self, lw, col, dash, alpha=1.0):
        c = self.c
        c.setLineWidth(lw)
        c.setStrokeColor(col)
        c.setStrokeAlpha(alpha)
        c.setDash(list(dash), 0) if dash else c.setDash()

    def linie(self, x1, y1, x2, y2, lw=LW_MITTEL, col=black, dash=None, alpha=1.0):
        self._stil(lw, col, dash, alpha)
        a, b = self.p(x1, y1), self.p(x2, y2)
        self.c.line(a[0], a[1], b[0], b[1])
        self.c.setStrokeAlpha(1)

    def poly(self, pts, fill=None, falpha=1.0, lw=LW_MITTEL, col=black, dash=None, rand=True, zu=True):
        c = self.c
        path = c.beginPath()
        q = [self.p(*pt) for pt in pts]
        path.moveTo(*q[0])
        for pt in q[1:]:
            path.lineTo(*pt)
        if zu:
            path.close()
        self._stil(lw, col, dash)
        if fill is not None:
            c.setFillColor(fill)
            c.setFillAlpha(falpha)
        c.drawPath(path, stroke=1 if rand else 0, fill=1 if fill is not None else 0)
        c.setFillAlpha(1)
        c.setFillColor(black)

    def rechteck(self, x, y, w, h, **kw):
        self.poly([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], **kw)

    def kreis(self, x, y, r, fill=None, falpha=1.0, lw=LW_MITTEL, col=black, dash=None, rand=True):
        cx, cy = self.p(x, y)
        self._stil(lw, col, dash)
        if fill is not None:
            self.c.setFillColor(fill)
            self.c.setFillAlpha(falpha)
        self.c.circle(cx, cy, r * self.s, stroke=1 if rand else 0, fill=1 if fill is not None else 0)
        self.c.setFillAlpha(1)
        self.c.setFillColor(black)

    def schraffur(self, x, y, w, h, abstand=1.0, winkel=45, lw=LW_FEIN, col=black, fill=None):
        """Schnittschraffur; abstand in Papier-mm."""
        c = self.c
        x0, y0 = self.p(x, y)
        x1, y1 = self.p(x + w, y + h)
        xa, xb = min(x0, x1), max(x0, x1)
        ya, yb = min(y0, y1), max(y0, y1)
        c.saveState()
        path = c.beginPath()
        path.rect(xa, ya, xb - xa, yb - ya)
        if fill is not None:
            c.setFillColor(fill)
            c.drawPath(path, stroke=0, fill=1)
        c.clipPath(path, stroke=0, fill=0)
        c.setLineWidth(lw)
        c.setStrokeColor(col)
        c.setDash()
        d = (xb - xa) + (yb - ya)
        t = math.tan(math.radians(winkel))
        k = -(yb - ya)
        while k < (xb - xa) + d:
            c.line(xa + k, ya, xa + k + (yb - ya) / t, yb)
            k += abstand / math.sin(math.radians(winkel))
        c.restoreState()
        self._stil(LW_MITTEL, black, None)
        c.rect(xa, ya, xb - xa, yb - ya, stroke=1, fill=0)

    def text(self, x, y, s, gr=2.5, anker="l", font="DV", col=black, rot=0, dx=0, dy=0):
        c = self.c
        px, py = self.p(x, y)
        c.saveState()
        c.translate(px + dx, py + dy)
        c.rotate(rot)
        c.setFont(font, gr)
        c.setFillColor(col)
        if anker == "l":
            c.drawString(0, 0, s)
        elif anker == "c":
            c.drawCentredString(0, 0, s)
        else:
            c.drawRightString(0, 0, s)
        c.restoreState()

    def pfeil(self, x1, y1, x2, y2, col=black, lw=0.45, kopf=1.8):
        a, b = self.p(x1, y1), self.p(x2, y2)
        c = self.c
        c.setStrokeColor(col)
        c.setFillColor(col)
        c.setLineWidth(lw)
        c.setDash()
        ang = math.atan2(b[1] - a[1], b[0] - a[0])
        ende = (b[0] - kopf * 0.8 * math.cos(ang), b[1] - kopf * 0.8 * math.sin(ang))
        c.line(a[0], a[1], ende[0], ende[1])
        path = c.beginPath()
        path.moveTo(*b)
        path.lineTo(b[0] - kopf * math.cos(ang - 0.38), b[1] - kopf * math.sin(ang - 0.38))
        path.lineTo(b[0] - kopf * math.cos(ang + 0.38), b[1] - kopf * math.sin(ang + 0.38))
        path.close()
        c.drawPath(path, stroke=0, fill=1)
        c.setFillColor(black)
        c.setStrokeColor(black)

    def mass(self, x1, y1, x2, y2, ab, txt=None, gr=2.2, col=black):
        """Bemassung zwischen zwei realen Punkten, ab = Abstand der Masslinie in Papier-mm
        (bezogen aufs Papier: positiv = oben bzw. links, negativ = unten bzw. rechts)."""
        c = self.c
        a, b = self.p(x1, y1), self.p(x2, y2)
        if (b[0] - a[0]) < -1e-6 or (abs(b[0] - a[0]) < 1e-6 and b[1] < a[1]):
            a, b = b, a
        dxp, dyp = b[0] - a[0], b[1] - a[1]
        ln = math.hypot(dxp, dyp)
        if ln < 1e-6:
            return
        ux, uy = dxp / ln, dyp / ln
        nx, ny = -uy, ux
        sg = 1 if ab >= 0 else -1
        a2 = (a[0] + nx * ab, a[1] + ny * ab)
        b2 = (b[0] + nx * ab, b[1] + ny * ab)
        c.setStrokeColor(col)
        c.setLineWidth(LW_FEIN)
        c.setDash()
        for p0, p1 in ((a, a2), (b, b2)):
            c.line(p0[0] + nx * sg * 0.8, p0[1] + ny * sg * 0.8, p1[0] + nx * sg * 1.2, p1[1] + ny * sg * 1.2)
        c.line(a2[0] - ux * 1.2, a2[1] - uy * 1.2, b2[0] + ux * 1.2, b2[1] + uy * 1.2)
        c.setLineWidth(LW_MITTEL)
        for q in (a2, b2):
            vx, vy = (ux + nx) * 0.75, (uy + ny) * 0.75
            c.line(q[0] - vx, q[1] - vy, q[0] + vx, q[1] + vy)
        if txt is None:
            txt = fmt(math.hypot((x2 - x1), (y2 - y1)))
        ang = math.degrees(math.atan2(uy, ux))
        if ang <= -90 or ang > 90:
            ang += 180
            nx, ny = -nx, -ny
        m = ((a2[0] + b2[0]) / 2 + nx * 0.7, (a2[1] + b2[1]) / 2 + ny * 0.7)
        c.saveState()
        c.translate(*m)
        c.rotate(ang)
        c.setFont("DV", gr)
        c.setFillColor(col)
        c.drawCentredString(0, 0, txt)
        c.restoreState()
        c.setStrokeColor(black)

    def hinweis(self, x, y, dxp, dyp, txt, gr=2.3, col=black, zeilen=None):
        """Hinweislinie vom realen Punkt zu Papier-Offset, Text daneben."""
        c = self.c
        a = self.p(x, y)
        b = (a[0] + dxp, a[1] + dyp)
        c.setStrokeColor(col)
        c.setFillColor(col)
        c.setLineWidth(LW_FEIN)
        c.setDash()
        c.circle(a[0], a[1], 0.45, stroke=0, fill=1)
        c.line(a[0], a[1], b[0], b[1])
        rechts = dxp >= 0
        e = (b[0] + (2 if rechts else -2), b[1])
        c.line(b[0], b[1], e[0], e[1])
        c.setFont("DV", gr)
        lines = txt.split("\n")
        for i, t in enumerate(lines):
            yy = e[1] - 0.8 - i * gr * 1.2 + (len(lines) - 1) * gr * 0.6
            if rechts:
                c.drawString(e[0] + 0.8, yy, t)
            else:
                c.drawRightString(e[0] - 0.8, yy, t)
        c.setFillColor(black)
        c.setStrokeColor(black)

    def hinweis_abs(self, x, y, tx, ty, txt, gr=2.0, col=black):
        """Hinweislinie vom realen Punkt zum Papierpunkt (tx, ty)."""
        a = self.p(x, y)
        self.hinweis(x, y, tx - a[0], ty - a[1], txt, gr=gr, col=col)

    def kote(self, x, y, txt, gr=2.2, links=False):
        """Hoehenkote (Dreieck auf Hoehe y bei x)."""
        c = self.c
        px, py = self.p(x, y)
        c.setLineWidth(LW_FEIN)
        c.setStrokeColor(black)
        c.setDash()
        path = c.beginPath()
        path.moveTo(px, py)
        path.lineTo(px - 1.1, py + 1.6)
        path.lineTo(px + 1.1, py + 1.6)
        path.close()
        c.setFillColor(black)
        c.drawPath(path, stroke=0, fill=1)
        c.line(px - 3, py, px + 3, py)
        c.setFont("DV", gr)
        if links:
            c.drawRightString(px - 2, py + 0.5, txt)
        else:
            c.drawString(px + 2, py + 0.5, txt)


def titel(c, x, y, txt, massstab=None, gr=3.4):
    c.setFont("DVB", gr)
    c.setFillColor(black)
    c.drawString(x, y, txt)
    w = pdfmetrics.stringWidth(txt, "DVB", gr)
    c.setLineWidth(0.3)
    c.line(x, y - 0.9, x + w, y - 0.9)
    if massstab:
        c.setFont("DV", gr * 0.75)
        c.drawString(x + w + 2.5, y, massstab)


def absatz(c, x, y, zeilen, gr=2.4, zab=1.3, font="DV", breite=None, col=black):
    """Mehrzeiliger Text; Zeilen mit '**' am Anfang fett. Gibt neue y-Position zurueck."""
    c.setFillColor(col)
    for z in zeilen:
        f = font
        if z.startswith("**"):
            z = z[2:]
            f = "DVB"
        if breite:
            woerter = z.split(" ")
            akt = ""
            teile = []
            for wo in woerter:
                test = (akt + " " + wo).strip()
                if pdfmetrics.stringWidth(test, f, gr) > breite and akt:
                    teile.append(akt)
                    akt = "    " + wo if teile == [] and z.startswith("•") else ("   " + wo if z.startswith(("•", "–", "1", "2", "3", "4", "5", "6", "7", "8", "9")) else wo)
                else:
                    akt = test
            teile.append(akt)
        else:
            teile = [z]
        for t in teile:
            c.setFont(f, gr)
            c.drawString(x, y, t)
            y -= gr * zab
    c.setFillColor(black)
    return y


def tabelle(c, x, y, spalten, zeilen, gr=2.3, zh=None, kopf=True, ausr=None):
    """spalten: Liste Breiten (mm); zeilen: Liste Listen von Strings. Gibt y-Ende zurueck."""
    zh = zh or gr * 1.6
    ausr = ausr or ["l"] * len(spalten)
    c.setLineWidth(LW_FEIN)
    gesamt = sum(spalten)
    for i, z in enumerate(zeilen):
        fett = kopf and i == 0
        if fett:
            c.setFillColor(C_HELLGRAU)
            c.rect(x, y - zh, gesamt, zh, stroke=0, fill=1)
            c.setFillColor(black)
        xx = x
        for j, (w, t) in enumerate(zip(spalten, z)):
            c.setFont("DVB" if fett else "DV", gr)
            ty = y - zh + (zh - gr) / 2 + 0.35
            if ausr[j] == "r":
                c.drawRightString(xx + w - 1, ty, t)
            elif ausr[j] == "c":
                c.drawCentredString(xx + w / 2, ty, t)
            else:
                c.drawString(xx + 1, ty, t)
            xx += w
        c.line(x, y - zh, x + gesamt, y - zh)
        y -= zh
    top = y + zh * len(zeilen)
    c.line(x, top, x + gesamt, top)
    xx = x
    for w in spalten:
        c.line(xx, top, xx, y)
        xx += w
    c.line(xx, top, xx, y)
    return y


# ------------------------------------------------------------------ Bauteile
def bett_draufsicht(v):
    # Verkleidung + Matratze + Kissen
    v.rechteck(-XB, -BETT_AY, BETT_AX, BETT_AY, fill=C_VK, falpha=0.55, lw=LW_DICK)
    v.rechteck(-XB + VK, -BETT_AY + VK, BETT_B, BETT_L, lw=LW_FEIN, dash=(1, 0.8))
    v.rechteck(-1000, -BETT_AY + VK + 30, 2000, 2000, fill=white, lw=LW_MITTEL)
    for x0 in (-900, 150):
        v.rechteck(x0, -BETT_AY + 90, 750, 380, fill=C_HELLGRAU, lw=LW_DUENN)


def bank_draufsicht_aussen(v, innen=True):
    v.rechteck(-XB, Y_B0, BETT_AX, BANK_T, fill=C_HOLZ, falpha=0.8, lw=LW_DICK)
    if innen:
        d = (1.2, 0.8)
        for xt in (X_T1, X_T2):
            v.rechteck(xt, Y_RI, PL, Y_FI - Y_RI, lw=LW_FEIN, dash=d)
        v.rechteck(X_PJ0, Y_PR, PJ_B, PJ_T, fill=C_PJ, falpha=0.35, lw=LW_DUENN, dash=d)


# ------------------------------------------------------------------ Blatt 1
def blatt1(c):
    b = Blatt(c, 1, 4, "Bett 200×200 mit Verkleidung und verdecktem Beamer",
              "Übersicht: Draufsicht Raum, Längsschnitt mit Strahlengang und Sichtlinien", "1:25")
    s = 1 / 25

    # ---------------- Draufsicht
    v = Ansicht(c, 88, 136, s)
    titel(c, 18, 274, "Draufsicht Raum", "M 1:25")
    yw0 = -BETT_AY - 20
    v.schraffur(-1350, yw0 - 120, 2700, 120, abstand=1.2)
    v.schraffur(-1350, Y_WAND, 2700, 120, abstand=1.2)
    # Strahl
    v.poly([(-LINSE_R, Y_LF), (-SW / 2, Y_WAND), (SW / 2, Y_WAND), (LINSE_R, Y_LF)],
           fill=C_STRAHL, falpha=0.35, lw=LW_FEIN, col=C_STRAHL)
    v.linie(-SW / 2, Y_WAND - 15, SW / 2, Y_WAND - 15, lw=1.2, col=C_BILD)
    bett_draufsicht(v)
    bank_draufsicht_aussen(v)
    v.kreis(0, Y_LF, 25, fill=C_PJ, lw=LW_DUENN)
    # Bettachse
    v.linie(0, yw0 - 60, 0, Y_WAND + 60, lw=LW_FEIN, dash=(4, 1, 0.6, 1))
    v.text(0, Y_WAND + 190, "Bettachse = Bildmitte = Linsenmitte", gr=2.1, anker="c")
    # Zuschauer
    for x0 in (-480, 480):
        v.kreis(x0, -BETT_AY + 300, 105, fill=Color(0.95, 0.85, 0.75), lw=LW_DUENN)
    # Luft
    v.pfeil(-XB, Y_B0 + 270, -XB - 330, Y_B0 + 270, col=C_WARM)
    v.text(-XB - 40, Y_B0 + 400, "Abluft", gr=2.2, anker="r", col=C_WARM)
    v.kreis(380, 290, 45, lw=0.35, col=C_KALT)
    v.kreis(380, 290, 12, fill=C_KALT, rand=False)
    # Bemassung
    v.mass(-XB, -BETT_AY, XB, -BETT_AY, -10, f"{fmt(BETT_AX)} (Bett + Verkleidung) (A)")
    v.mass(-XB, -BETT_AY, -XB, 0, 7, f"{fmt(BETT_AY)} (A)")
    v.mass(XB, Y_B0, XB, Y_B1, -5, fmt(BANK_T))
    v.mass(XB, Y_B1, XB, Y_WAND, -5, f"A = {fmt(A_WAND)} (A) – messen!")
    v.mass(-SW / 2, Y_WAND, SW / 2, Y_WAND, -9, f"Bild {fmt(SW)} breit (16:10)")
    # Hinweise
    v.hinweis(-XB, 5, -6, -8, f"Fuge {FUGE}:\nBank steht frei,\nkeine Verbindung\nzum Bett", gr=2.0)
    v.hinweis(X_PJ0 + 60, Y_PR + 200, -40, 23, "Beamer PT-VMZ51S\nin der Bank (Blatt 2)", gr=2.0)
    v.hinweis(380, 290, 26, 14, "Zuluft von unten", gr=2.0, col=C_KALT)
    v.hinweis(-SW / 2 + 300, Y_WAND - 15, -30, -16, "Projektionsfläche:\nWand glatt, matt\nweiß oder hellgrau", gr=2.0)

    # ---------------- Laengsschnitt
    w = Ansicht(c, 266, 166, s)
    titel(c, 180, 274, "Längsschnitt in Bettachse mit Strahlengang", "M 1:25")
    w.schraffur(-2350, -100, 2350 + Y_WAND + 120, 100, abstand=1.2)
    w.schraffur(yw0 - 120, 0, 120, RAUM_H, abstand=1.2)
    w.schraffur(Y_WAND, 0, 120, RAUM_H, abstand=1.2)
    w.linie(yw0, RAUM_H, Y_WAND, RAUM_H, lw=LW_DUENN, dash=(3, 1.5))
    w.text(yw0 + 60, RAUM_H - 120, f"Decke {fmt(RAUM_H)} (A)", gr=2.0)
    # Strahl
    w.poly([(Y_LF, Z_L - LINSE_R), (Y_WAND, BILD_UK), (Y_WAND, BILD_OK), (Y_LF, Z_L + LINSE_R)],
           fill=C_STRAHL, falpha=0.35, lw=LW_FEIN, col=C_STRAHL)
    w.linie(Y_WAND - 15, BILD_UK, Y_WAND - 15, BILD_OK, lw=1.4, col=C_BILD)
    # Bett
    w.rechteck(-BETT_AY + VK + 30, ROST_Z, 2000, MATR_H, fill=white, lw=LW_MITTEL)
    w.rechteck(-BETT_AY + 30, MATR_OK, 400, 110, fill=C_HELLGRAU, lw=LW_DUENN)
    w.rechteck(-BETT_AY, VK_BODEN, BETT_AY, BETT_H - VK_BODEN, fill=C_VK, falpha=0.6, lw=LW_DICK)
    # Person liegend (Decke) + Kopf
    decke = [(-BETT_AY + 400, MATR_OK), (-BETT_AY + 420, MATR_OK + 170), (-1300, MATR_OK + 200),
             (-700, MATR_OK + 170), (-330, MATR_OK + 150), (-270, MATR_OK + 270), (-170, MATR_OK + 260),
             (-110, MATR_OK + 120), (-60, MATR_OK)]
    w.poly(decke, fill=Color(0.75, 0.70, 0.62), falpha=0.6, lw=LW_DUENN)
    w.kreis(-BETT_AY + 330, MATR_OK + 200, 100, fill=Color(0.95, 0.85, 0.75), lw=LW_DUENN)
    # Bank
    w.rechteck(Y_B0 + 50, 0, BANK_T - 100, SOCKEL, fill=C_GRAU, lw=LW_DUENN)
    w.rechteck(Y_B0, SOCKEL, BANK_T, BANK_H - SOCKEL, fill=C_HOLZ, lw=LW_DICK)
    w.rechteck(Y_PR, Z_FB, PJ_T, PJ_H, fill=C_PJ, falpha=0.4, lw=LW_DUENN, dash=(1.2, 0.8))
    w.kreis(Y_LF, Z_L, 18, fill=C_PJ, lw=LW_FEIN)
    # Sichtlinien
    z_e1, z_e2 = MATR_OK + 250, MATR_OK + 500
    augen = [((-BETT_AY + 360, z_e1), f"Auge liegend ≈ {z_e1}"), ((-BETT_AY + 480, z_e2), f"Auge halb sitzend ≈ {z_e2}")]
    for (ya, za), t in augen:
        for zz in (BILD_UK, BILD_OK):
            w.linie(ya, za, Y_WAND - 15, zz, lw=LW_FEIN, col=Color(0.1, 0.5, 0.2), dash=(2, 1))
        w.kreis(ya, za, 18, fill=Color(0.1, 0.5, 0.2), rand=False)
    w.hinweis(augen[0][0][0], z_e1, 4, -13, augen[0][1], gr=2.0)
    w.hinweis(augen[1][0][0], z_e2, -4, 13, augen[1][1], gr=2.0)
    # Koten Wand
    for zz, t in ((BILD_OK, f"+{fmt(BILD_OK)} OK"), (BILD_UK, f"+{fmt(BILD_UK)} UK"),
                  (0, "±0")):
        w.kote(Y_WAND + 140, zz, t, gr=2.1)
    w.mass(Y_WAND + 120, BILD_UK, Y_WAND + 120, BILD_OK, -3.5, f"{fmt(SH)}")
    # Hinweise Bank/Bett
    w.hinweis(Y_LF, Z_L, 12, 18, f"Linsenmitte +{Z_L}", gr=2.0)
    w.hinweis(Y_B1, BANK_H, 22, 9, f"Bank +{BANK_H}", gr=2.0)
    w.hinweis(-600, MATR_OK, -4, 30, f"Matratze OK ≈ +{MATR_OK} (A)", gr=2.0)
    w.text(-BETT_AY / 2, 80, f"Bettrahmen +{BETT_H} (gemessen) mit Verkleidung 19 mm", gr=2.0, anker="c")
    w.hinweis(-220, MATR_OK + 265, 6, 26, f"Zehen unter Decke ≈ {MATR_OK + 270}", gr=2.0)
    # Bemassung unten
    w.mass(-BETT_AY, -100, 0, -100, -5, f"Bett {fmt(BETT_AY)} (A)")
    w.mass(Y_B0, -100, Y_B1, -100, -5, fmt(BANK_T))
    w.mass(Y_B1, -100, Y_WAND, -100, -5, f"A = {fmt(A_WAND)} (A)")
    # Strahl-Notiz
    w.text(Y_B1 + 300, 2250,
           f"Projektionsabstand L = {fmt(L_PROJ)} → Zoom TR = {fmt(TR, 2)} (möglich 1,09–1,77)", gr=2.1)
    w.text(Y_B1 + 300, 2130,
           f"Lens-Shift vertikal h = {fmt(H_SHIFT, 2)} (möglich 0,06–0,50) → kein Trapez nötig", gr=2.1)

    # ---------------- Tabelle Bildgroesse
    x0, y0 = 180, 150
    titel(c, x0, y0, "Bildgröße abhängig vom Wandabstand A", gr=3.0)
    zeilen = [["A (Bank–Wand)", "L ab Linse", "Bildbreite Zoom min–max", "Diagonale", f"größtes Bild mit UK {BILD_UK} ¹",
               "kleinstes Bild ohne Trapez ²"]]
    for a in (2000, 2500, 3000, 3500, 4000):
        lp = a + (Y_B1 - Y_LF)
        swmin, swmax = lp / TR_MAX, lp / TR_MIN
        dmin, dmax = swmin / 0.848 / 25.4, swmax / 0.848 / 25.4
        swgr = min(swmax, (RAUM_H - 100 - BILD_UK) * 1.6)
        swkl = max(swmin, (BILD_UK - Z_L) / H_MAX * 1.6)
        zeilen.append([f"{fmt(a)}", f"{fmt(lp)}", f"{fmt(swmin)} – {fmt(swmax)}", f"{fmt(dmin)}–{fmt(dmax)} Zoll",
                       f"{fmt(swgr)} breit", f"{fmt(swkl)} breit"])
    y = tabelle(c, x0, y0 - 3, [26, 20, 40, 28, 44, 44], zeilen, gr=2.2,
                ausr=["c", "c", "c", "c", "c", "c"])
    absatz(c, x0, y - 4, [
        f"¹ begrenzt durch Zoom (TR 1,09) oder Raumhöhe: Bildoberkante ≤ Decke − 100.",
        f"² Unterkante {BILD_UK} braucht Lens-Shift h = ({BILD_UK} − {Z_L}) / Bildhöhe ≤ 0,50 → Bildhöhe ≥ "
        f"{fmt((BILD_UK - Z_L) / H_MAX)}. Kleinere Bilder: Fachboden höher setzen (Lochreihe) oder Beamer neigen.",
        "Werte aus Panasonic-Datenblatt PT-VMZ51S: Throw Ratio 1,09–1,77; H = 0,056–0,50 × Bildhöhe (Tabelle S. 7).",
        f"Grundlage Sichtlinie: Unterkante ≥ 800, damit Zehen/Decke (≈ {MATR_OK + 270}) das Bild auch im Liegen nicht anschneiden.",
        f"Vorhandener PT-VX500 (4:3, TR 1,18–1,90): bei A = {fmt(A_WAND)} Bildbreite "
        f"{fmt(L_PROJ / VX_TR_MAX)}–{fmt(L_PROJ / VX_TR_MIN)}, Lens-Shift vertikal laut Händler +40 % (nicht im Original geprüft).",
    ], gr=2.1, breite=226)
    b.fertig()


# ------------------------------------------------------------------ Blatt 2
def blatt2(c):
    b = Blatt(c, 2, 4, "Beamer-Fußbank (frei stehend, vom Bett entkoppelt)",
              "Ansicht Wandseite, Draufsicht ohne Deckel, Schnitt A–A, Stirnseiten", "1:10 / 1:5")
    s = 1 / 10
    d = (1.2, 0.8)

    # ---------------- Ansicht Wandseite (gespiegelt: Blick vom Raum auf die Bank)
    v = Ansicht(c, 135, 210, s, spiegel_x=True)
    titel(c, 25, 276, "Ansicht von der Wand (Vorderseite)", "M 1:10")
    for xf in (-980, 0, 980):
        v.rechteck(xf - 25, 0, 50, SOCKEL, fill=C_GRAU, lw=LW_DUENN)
    v.rechteck(-XB, SOCKEL, BETT_AX, BANK_H - SOCKEL, fill=C_HOLZ, lw=LW_DICK)
    v.linie(-XB, Z_BO, XB, Z_BO, lw=LW_DUENN)
    v.linie(-XB, Z_DE, XB, Z_DE, lw=LW_DUENN)
    for xx in (-XB + PL, XB - PL):
        v.linie(xx, Z_BO, xx, Z_DE, lw=LW_DUENN)
    for xx in (X_T1 + PL / 2, X_T2 + PL / 2):
        v.linie(xx, Z_DE, xx, BANK_H, lw=LW_DUENN)
    for xt in (X_T1, X_T2):
        v.rechteck(xt, Z_BO, PL, Z_DE - Z_BO, lw=LW_FEIN, dash=d)
    v.rechteck(X_PJ0, Z_FB, PJ_B, PJ_H, lw=LW_FEIN, dash=d, fill=C_PJ, falpha=0.15)
    v.rechteck(X_T1 + PL, Z_FB - PL, X_T2 - X_T1 - PL, PL, lw=LW_FEIN, dash=d)
    v.rechteck(S_X1, Z_L - 18, 500, 36, lw=LW_FEIN, dash=d)
    v.rechteck(-F_X, F_Z0, 2 * F_X, F_Z1 - F_Z0, fill=Color(0.12, 0.12, 0.12), lw=LW_MITTEL)
    v.linie(0, -40, 0, BANK_H + 60, lw=LW_FEIN, dash=(4, 1, 0.6, 1))
    v.text(0, BANK_H + 80, "Bettachse", gr=2.0, anker="c")
    v.text(-XB + 60, 300, "Abluftseite", gr=2.4, font="DVB", anker="r", col=C_WARM)
    v.text(-XB + 60, 230, "(vom Bett aus links)", gr=2.0, anker="r")
    v.text(XB - 60, 300, "Technikseite", gr=2.4, font="DVB", col=C_KALT)
    v.text(XB - 60, 230, "(vom Bett aus rechts)", gr=2.0)
    v.hinweis_abs(F_X, F_Z1, 160, 281, "Fenster 160 × 120, Schieber dahinter (Alu, mattschwarz),\n"
                                      "fährt beim Einschalten seitlich auf", gr=2.0)
    v.hinweis_abs(X_PJ0 + 120, Z_FB + 20, 180, 222, "Beamer (verdeckt)", gr=2.0)
    v.hinweis_abs(S_X1 + 250, Z_L, 70, 222, "Linearantrieb (verdeckt)", gr=2.0)
    v.mass(-XB, 0, XB, 0, -6, f"{fmt(BETT_AX)} = Bettbreite mit Verkleidung")
    v.mass(XB, 0, XB, BANK_H, 9, fmt(BANK_H))
    v.mass(XB, 0, XB, SOCKEL, 4, fmt(SOCKEL))
    v.mass(-F_X, F_Z0, -F_X, F_Z1, -3, "120")
    v.mass(-XB, 0, -XB, F_Z0, -4, f"{fmt(F_Z0)}")
    v.mass(-XB, 0, -XB, Z_L, -9, f"Linse {Z_L}")

    # ---------------- Draufsicht ohne Deckel
    t = Ansicht(c, 135, 122, s)
    titel(c, 25, 190, "Draufsicht, Deckel abgenommen", "M 1:10")
    t.rechteck(-XB, Y_B0, BETT_AX, BANK_T, fill=C_HOLZ, lw=LW_DICK)
    for (x, y, w_, h_) in ((-XB, Y_B0, BETT_AX, PL), (-XB, Y_FI, BETT_AX, PL), (-XB, Y_RI, PL, Y_FI - Y_RI),
                           (XB - PL, Y_RI, PL, Y_FI - Y_RI), (X_T1, Y_RI, PL, Y_FI - Y_RI),
                           (X_T2, Y_RI, PL, Y_FI - Y_RI)):
        t.schraffur(x, y, w_, h_, abstand=0.7, fill=C_VK)
    t.rechteck(-F_X, Y_FI, 2 * F_X, PL, fill=white, lw=LW_DUENN)
    t.rechteck(X_T1 + PL, Y_RI, X_T2 - X_T1 - PL, Y_LF - Y_RI, lw=LW_FEIN, dash=d)
    t.rechteck(150, 60, 450, 380, lw=LW_FEIN, dash=d)
    t.rechteck(180, 160, 400, 180, lw=LW_FEIN, dash=(0.6, 0.6), col=C_KALT)
    t.rechteck(X_PJ0, Y_PR, PJ_B, PJ_T, fill=C_PJ, falpha=0.45, lw=LW_MITTEL)
    t.rechteck(-LINSE_R - 8, Y_LF - 30, 2 * LINSE_R + 16, 30, fill=C_PJ, lw=LW_DUENN)
    t.text(X_PJ0 + PJ_B / 2, Y_PR + 175, "PT-VMZ51S", gr=2.2, anker="c", font="DVB")
    t.text(X_PJ0 + PJ_B / 2, Y_PR + 125, "399 × 348", gr=2.0, anker="c")
    t.schraffur(X_T1 + PL, Y_PR + 40, X_PJ0 - X_T1 - PL, PJ_T - 80, abstand=0.5, col=C_WARM)
    for yy in (180, 360):
        t.pfeil(X_PJ0 + 40, yy, -XB - 90, yy, col=C_WARM)
    t.rechteck(-XB + PL + 80, Y_RI, PL, Y_FI - Y_RI, fill=C_VK, lw=LW_DUENN)
    for yc in (180, 360):
        t.rechteck(-XB + PL + 80 - 25, yc - LUEFTER / 2, 25, LUEFTER, fill=C_GRAU, lw=LW_DUENN)
    for yy in (180, 360):
        t.pfeil(XB + 110, yy, X_T2 + 60, yy, col=C_KALT)
    t.text(-690, 420, "Abluftkanal – frei halten", gr=2.2, anker="c", col=C_WARM)
    t.pfeil(380, 275, X_PJ1 + 10, 275, col=C_KALT)
    t.kreis(380, 275, 35, lw=0.3, col=C_KALT)
    t.kreis(380, 275, 9, fill=C_KALT, rand=False)
    t.linie(S_X0, Y_FI - 5, S_X1, Y_FI - 5, lw=0.8, col=C_ALU)
    t.linie(S_X0 + HUB, Y_FI - 5, S_X1 + HUB, Y_FI - 5, lw=0.5, col=C_ALU, dash=(2, 0.6, 0.4, 0.6))
    t.rechteck(S_X1, Y_FI - 22, 200, 8, fill=C_GRAU, lw=LW_DUENN)
    t.rechteck(S_X1 + 200, Y_FI - 36, 300, 36, fill=C_GRAU, lw=LW_DUENN)
    t.rechteck(S_X1 + 500, Y_FI - 44, 30, 44, fill=C_VK, lw=LW_DUENN)
    for (x, y, w_, h_, txt) in ((665, 395, 173, 60, "Switch-Dock"), (665, 240, 127, 127, "Mac mini"),
                                (860, 260, 95, 95, "Apple TV"), (860, 395, 150, 60, "HDMI 3→1"),
                                (665, 95, 160, 110, "LAN-Switch")):
        t.rechteck(x, y, w_, h_, fill=white, lw=LW_DUENN)
        t.text(x + w_ / 2, y + h_ / 2 - 8, txt, gr=1.7, anker="c")
    t.text(925, 175, "Ebene 1: Geräte", gr=1.7, anker="c")
    t.text(925, 135, "darunter: Leisten,", gr=1.6, anker="c")
    t.text(925, 100, "Netzteil, Relais", gr=1.6, anker="c")
    # Kabelkanal unter dem Boden (Wanddose auf der Abluftseite)
    t.rechteck(-XB - 60, 35, XB + 1050, 40, lw=LW_DUENN, dash=(2.5, 0.8), col=Color(0.45, 0.2, 0.6))
    t.kreis(990, 55, 22, fill=white, lw=LW_DUENN, col=Color(0.45, 0.2, 0.6))
    t.kreis(0, Y_B0 + 4, 12, fill=C_ROT, rand=False)
    t.linie(0, Y_B0 - 60, 0, Y_B1 + 110, lw=LW_DUENN, dash=(4, 1, 0.6, 1))
    for yy in (Y_B0 - 60, Y_B1 + 110):
        t.pfeil(0, yy, -120, yy, lw=0.5, kopf=1.5)
        t.text(-150, yy - 25, "A", gr=2.6, font="DVB", anker="r")
    t.hinweis_abs(-XB + 75, 110, 40, 108, f"2 × Lüfter {LUEFTER} mm auf Träger,\n80 mm hinter dem Schlitzfeld", gr=1.9)
    t.hinweis_abs(X_T1 + 10, Y_PR + 70, 100, 100, "Trennwand T1: Ausschnitt 280 × 100 vor\nAbluftgitter, Moosgummi-Dichtrahmen", gr=1.9)
    t.hinweis_abs(0, Y_B0 + 4, 141, 110, "IR-Empfänger (zum Bett)", gr=1.9)
    t.hinweis_abs(380, 240, 176, 100, "Zuluftgitter im Boden 400 × 180 + Filtermatte,\nFachboden mit Ausschnitt 450 × 380", gr=1.9, col=C_KALT)
    t.hinweis_abs(-XB - 40, 75, 140, 186, "Kabelkanal unter dem Boden: Strom + LAN von der Wanddose\n(Wandseite prüfen) bis ins Technikfach",
                  gr=1.9, col=Color(0.45, 0.2, 0.6))
    t.hinweis_abs(S_X1 + 350, Y_FI - 18, 214, 186, "Linearantrieb 12 V, Hub 200 (Blatt 3)", gr=1.9)
    t.mass(-XB, Y_B0, -XB, Y_B1, 8, fmt(BANK_T))
    t.mass(-XB, Y_B1, X_T1, Y_B1, 4, fmt(XB + X_T1))
    t.mass(X_T1 + PL, Y_B1, X_T2, Y_B1, 4, fmt(X_T2 - X_T1 - PL))
    t.mass(X_T2 + PL, Y_B1, XB, Y_B1, 4, fmt(XB - X_T2 - PL))
    t.mass(X_PJ0, Y_PR, 0, Y_PR, -3.5, fmt(-X_PJ0))
    t.mass(0, Y_PR, X_PJ1, Y_PR, -3.5, fmt(X_PJ1))

    # ---------------- Schnitt A-A  M 1:5
    a = Ansicht(c, 262, 140, 1 / 5, rx=-60)
    titel(c, 262, 276, "Schnitt A–A (Bettachse)", "M 1:5")
    a.rechteck(-60, VK_BODEN, 60, BETT_H - VK_BODEN, fill=C_VK, falpha=0.6, lw=LW_MITTEL)
    a.rechteck(-60, ROST_Z, 30, MATR_H, fill=white, lw=LW_DUENN)
    a.text(-30, 120, "Bett", gr=1.9, anker="c", rot=90)
    a.linie(-60, 0, Y_B1 + 25, 0, lw=LW_DICK)
    a.schraffur(-60, -18, Y_B1 + 85, 18, abstand=1.0)
    for yf in (Y_B0 + 50, Y_B1 - 100):
        a.rechteck(yf, 0, 50, SOCKEL, fill=C_GRAU, lw=LW_DUENN)
    teile = [(Y_B0, Z_K0, BANK_T, PL), (Y_B0, Z_BO, PL, Z_DE - Z_BO), (Y_FI, Z_BO, PL, F_Z0 - Z_BO),
             (Y_FI, F_Z1, PL, Z_DE - F_Z1), (Y_B0, Z_DE, BANK_T, PL), (Y_RI, Z_FB - PL, Y_LF - Y_RI, PL)]
    for (y, z, w_, h_) in teile:
        a.schraffur(y, z, w_, h_, abstand=0.8, fill=C_HOLZ)
    a.rechteck(Y_PR, Z_FB + 10, PJ_T, PJ_H - 10, fill=C_PJ, falpha=0.45, lw=LW_MITTEL)
    for yf in (Y_PR + 30, Y_LF - 60):
        a.rechteck(yf, Z_FB, 25, 10, fill=C_PJ, lw=LW_FEIN)
    a.rechteck(Y_LF - 25, Z_L - LINSE_R, 25, 2 * LINSE_R, fill=Color(0.2, 0.3, 0.6), lw=LW_DUENN)
    a.text(Y_PR + PJ_T / 2, Z_FB + 70, "PT-VMZ51S", gr=2.4, anker="c", font="DVB", col=white)
    ende = Y_B1 + 25
    st_u = H_SHIFT * SH / L_PROJ
    st_o = (H_SHIFT + 1) * SH / L_PROJ
    a.poly([(Y_LF, Z_L - LINSE_R), (ende, Z_L - LINSE_R + st_u * (ende - Y_LF)),
            (ende, Z_L + LINSE_R + st_o * (ende - Y_LF)), (Y_LF, Z_L + LINSE_R)],
           fill=C_STRAHL, falpha=0.45, lw=LW_FEIN, col=C_STRAHL)
    a.linie(Y_LF - 40, Z_L, ende, Z_L, lw=LW_FEIN, dash=(4, 1, 0.6, 1))
    a.rechteck(Y_FI - 7, S_Z0, 3, S_Z1 - S_Z0, lw=LW_FEIN, dash=(1.2, 0.6), col=C_GRAU)
    for zz in (S_Z0 - 4, S_Z1 - 6):
        a.rechteck(Y_FI - 10, zz, 10, 10, fill=C_ALU, lw=LW_FEIN)
    a.pfeil(Y_FI - 25, 110, Y_FI - 25, Z_FB - 10, col=C_KALT)
    a.pfeil(Y_B0 + 140, -14, Y_B0 + 140, Z_K0 - 4, col=C_KALT)
    for zz, txt in ((BANK_H, f"+{BANK_H}"), (Z_FB + PJ_H, f"+{Z_FB + PJ_H} Beamer"),
                    (Z_L, f"+{Z_L} Linse"), (Z_FB, f"+{Z_FB} Fachboden"),
                    (Z_K0, f"+{Z_K0}"), (0, "±0")):
        a.kote(Y_B1 + 55, zz, txt, gr=1.9)
    a.mass(Y_FI, F_Z0, Y_FI, F_Z1, 3, "120")
    a.text(5, 330, f"Fuge {FUGE}", gr=1.7, anker="c", rot=90)
    kette = [(Y_B0, Y_RI), (Y_RI, Y_PR), (Y_PR, Y_LF), (Y_LF, Y_FI), (Y_FI, Y_B1)]
    for y1, y2 in kette:
        a.mass(y1, -18, y2, -18, -4, fmt(y2 - y1))
    a.mass(Y_B0, -18, Y_B1, -18, -10, fmt(BANK_T))
    a.hinweis_abs(Y_B0 + 200, BANK_H, 318, 260, "Deckel abnehmbar (Dübel + Magnete):\n"
                                                "Zugang Zoom, Fokus, Lens-Shift, Filter", gr=1.9)
    a.hinweis_abs(Y_FI - 6, S_Z1 - 1, 340, 229, "Schieber (zu) in Alu-U-Führungen", gr=1.8)
    a.hinweis_abs(Y_RI + 40, Z_FB + 60, 288, 192, "Kabelraum 89 mm: HDMI/Netz\nmit Winkelsteckern", gr=1.8)
    a.hinweis_abs(Y_RI + 150, Z_FB - PL / 2, 313, 186, "Fachboden auf Bodenträgern,\nLochreihe 32 mm in T1/T2\n(Linsenhöhe verstellbar)", gr=1.8)
    a.hinweis_abs(Y_FI - 25, 160, 330, 166, "Zuluft von unten\n(Gitter seitlich,\ns. Draufsicht)", gr=1.8, col=C_KALT)

    # ---------------- Stirnseite Abluft M 1:10 (Blick von -X, Bettseite rechts)
    e = Ansicht(c, 278, 56, s, spiegel_x=True, rx=Y_B1)
    titel(c, 262, 121, "Stirnseiten (links = rechts)", "M 1:10")
    for yf in (Y_B0 + 50, Y_B1 - 100):
        e.rechteck(yf, 0, 50, SOCKEL, fill=C_GRAU, lw=LW_DUENN)
    e.rechteck(Y_B0, SOCKEL, BANK_T, BANK_H - SOCKEL, fill=C_HOLZ, lw=LW_DICK)
    e.linie(Y_B0, Z_DE, Y_B1, Z_DE, lw=LW_DUENN)
    e.linie(Y_B0, Z_BO, Y_B1, Z_BO, lw=LW_DUENN)
    for k in range(9):
        e.rechteck(100, 140 + 30 * k, 340, 12, fill=Color(0.2, 0.2, 0.2), lw=LW_FEIN)
    e.mass(Y_B1, 0, Y_B0, 0, -5, fmt(BANK_T))
    e.mass(100, 140, 440, 140, -3, "340")
    e.mass(Y_B0, 140, Y_B0, 392, -4, "9 × 12, Teilung 30")
    e.text(270, 95, "Schlitzfeld 367 cm² frei", gr=1.8, anker="c")
    e.text(Y_B1, 575, "Wand", gr=1.9, anker="c")
    e.text(Y_B0, 575, "Bett", gr=1.9, anker="c")

    # ---------------- Legende
    lx, ly = 340, 112
    c.setFont("DVB", 2.4)
    c.drawString(lx, ly, "Legende")
    eintraege = [(C_KALT, "Zuluft (Raumluft)"), (C_WARM, "Abluft (warm)"), (C_STRAHL, "Lichtstrahl"),
                 (C_PJ, "Beamer"), (C_HOLZ, "Holz 19 mm"), (C_ALU, "Alu (Schieber, Führung)")]
    for i, (col, txt) in enumerate(eintraege):
        yy = ly - 5 - i * 4.2
        c.setFillColor(col)
        c.rect(lx, yy - 0.3, 5, 2.6, stroke=0, fill=1)
        c.setFillColor(black)
        c.setFont("DV", 2.1)
        c.drawString(lx + 7, yy, txt)
    c.setFont("DV", 2.1)
    c.drawString(lx, ly - 5 - 6 * 4.2, "(A) = Annahme, messen")
    c.drawString(lx, ly - 5 - 7 * 4.2, "- - - verdeckte Kante")

    absatz(c, 25, 90, [
        "**Luftführung (Panasonic verlangt im engen Raum Zwangslüftung, Anleitung S. 21)",
        "1. Zuluft (zusätzlich zur rechten Stirnseite, Punkt 5): Raumluft strömt unter der Bank (Sockelfuge 60 mm, offen) durch das Bodengitter mit Filtermatte nach oben, "
        "durch den Ausschnitt im Fachboden an die Ansaugseiten des Beamers (Linsenseite + Front). Bei offenem Schieber auch durchs Fenster.",
        "2. Der Beamer bläst seitlich auf der Abluftseite aus. Moosgummi-Rahmen und Trennwand T1 führen die warme Luft in den "
        "Abluftkanal – kein Kurzschluss zurück zur Ansaugung.",
        "3. Zwei 140-mm-Lüfter in der linken Stirnseite saugen den Kanal ab (Unterdruck in der Bank). Die warme Luft verlässt die "
        "Bank seitlich, weit weg vom Strahl (Hitzeflimmern vor der Linse vermeiden, Anleitung S. 19).",
        "4. Lüfter laufen mit „Kino an“ und 5 min nach (Zeitrelais, Blatt 3). Vor beiden Stirnseiten ≥ 50 cm frei halten.",
        "5. Beide Stirnseiten bekommen das gleiche Schlitzfeld (9 × 340 × 12). Links Abluft: Lüfter sitzen unsichtbar 80 mm dahinter. "
        "Rechts Zuluft: Filtermatte dahinter, die Luft kühlt Mac mini und Switch und strömt durch 2 Öffnungen 300 × 80 unten in "
        "T2 zum Beamer. Vorne (Wandseite) keine Abluft (Hitzeflimmern) und keine Schlitze in den Abluftkanal (Lüfter saugen sonst "
        "Raumluft statt Beamer-Abluft).",
        "**Entkopplung",
        "Die Bank berührt das Bett nicht (Fuge 10 mm, optisch eine Schattenfuge). Bewegung auf der Matratze würde sonst das Bild "
        "zittern lassen: schon 0,5 mm Kippen über 348 mm Gerätetiefe verschiebt das Bild um ≈ 3,7 mm ≈ 3,5 Pixel (Blatt 4).",
        "**Passt für beide Beamer und alle Geräte",
        "PT-VMZ51S 399 × 348 und vorhandener PT-VX500 379 × 305 (mit Steckern ≈ 420 tief, gemessen). Linsenhöhe über die Lochreihe "
        "des Fachbodens anpassen. Technikfach: Apple TV, Mac mini, Switch-Dock (Zugang über Klappdeckel), HDMI- und LAN-Switch; "
        "darunter Steckdosenleisten, Netzteile, Relais. Von der Wand kommen nur 1 Stromkabel + 1 LAN-Kabel, unsichtbar im Kanal unter der Bank.",
    ], gr=2.15, breite=222)
    b.fertig()


# ------------------------------------------------------------------ Blatt 3
def blatt3(c):
    b = Blatt(c, 3, 4, "Details: Schieber, Fenster, Bettverkleidung, Steuerung",
              "Detail 1–3 und Blockschaltbild", "1:4 / 1:2,5")
    # ---------------- Detail 1 Schieber, Ansicht von innen  M 1:4
    v = Ansicht(c, 77, 192, 1 / 4, ry=200)
    titel(c, 22, 276, "Detail 1: Schieber mit Antrieb – Ansicht von innen (Blick zur Wand, Beamer weggelassen)", "M 1:4")
    v.rechteck(-220, 200, 900, Z_DE - 200, fill=C_HOLZ, lw=LW_DUENN)
    v.schraffur(-220, Z_DE, 900, PL, abstand=0.8, fill=C_HOLZ)
    v.rechteck(-F_X, F_Z0, 2 * F_X, F_Z1 - F_Z0, fill=white, lw=LW_MITTEL)
    v.kreis(0, Z_L, LINSE_R, lw=LW_FEIN, dash=(1, 0.6), col=C_PJ)
    v.linie(-60, Z_L, 60, Z_L, lw=LW_FEIN, dash=(3, 0.8, 0.5, 0.8))
    for zz in (S_Z0 - 4, S_Z1 - 6):
        v.rechteck(-130, zz, 470, 10, fill=C_ALU, lw=LW_DUENN)
    v.rechteck(S_X0, S_Z0, S_X1 - S_X0, S_Z1 - S_Z0, fill=C_ALU, falpha=0.55, lw=LW_MITTEL)
    v.rechteck(S_X0 + HUB, S_Z0, S_X1 - S_X0, S_Z1 - S_Z0, lw=LW_DUENN, dash=(3, 0.8, 0.5, 0.8))
    v.text(0, S_Z1 - 40, "Schieber ZU", gr=2.0, anker="c")
    v.text(S_X0 + HUB + 100, S_Z1 - 40, "AUF", gr=2.0, anker="c")
    v.rechteck(S_X1 - 10, Z_L - 15, 20, 30, fill=C_GRAU, lw=LW_DUENN)
    v.rechteck(S_X1 + 10, Z_L - 5, 190, 10, fill=Color(0.75, 0.75, 0.75), lw=LW_DUENN)
    v.rechteck(S_X1 + 200, Z_L - 18, 300, 36, fill=C_GRAU, lw=LW_DUENN)
    v.rechteck(S_X1 + 500, Z_L - 40, 40, 80, fill=C_VK, lw=LW_DUENN)
    v.kreis(S_X1 + 515, Z_L, 6, fill=white, lw=LW_FEIN)
    v.mass(S_X0, S_Z0 - 4, S_X1, S_Z0 - 4, -4, "Schieber 200")
    v.mass(S_X1, S_Z0 - 4, S_X1 + HUB, S_Z0 - 4, -4, f"Hub {HUB}")
    v.mass(S_X0 - 30, S_Z0, S_X0 - 30, S_Z1, 4, fmt(S_Z1 - S_Z0))
    v.hinweis_abs(330, S_Z1 + 3, 252, 262, "Alu-U-Profil 10 × 10 oben + unten,\nPTFE-Gleitband, auf Front geschraubt", gr=1.9)
    v.hinweis_abs(S_X1 + 350, Z_L + 18, 252, 249, "Linearantrieb 12 V DC, Hub 200, ≥ 30 N,\n≥ 40 mm/s, Endschalter intern", gr=1.9)
    v.hinweis_abs(S_X1 + 540, Z_L - 30, 252, 236, "Hartholzklotz, Gabelkopf verschraubt", gr=1.9)
    v.rechteck(S_X1 + HUB + 4, S_Z0 + 8, 22, 12, fill=Color(1.0, 0.85, 0.85), lw=LW_DUENN)
    v.linie(S_X1 + HUB + 6, S_Z0 + 20, S_X1 + HUB + 1, S_Z0 + 30, lw=0.4, col=C_ROT)
    v.hinweis_abs(S_X1 + HUB + 26, S_Z0 + 14, 252, 222, "Endschalter S2: schließt nur, wenn der Schieber\n"
                  "ganz AUF ist → erst dann Strom für den Beamer", gr=1.9, col=C_ROT)
    v.hinweis_abs(S_X0 + 30, S_Z0 + 20, 120, 205, "Schieber: Alu-Verbundplatte 3 mm, Wandseite mattschwarz,\n"
                                                  "Linsenseite blank (Hitzeschild)", gr=1.9)
    v.hinweis_abs(S_X1, Z_L - 15, 120, 197, "Winkel + Gabelkopf am Schieberrand", gr=1.9)
    v.hinweis_abs(0, Z_L - LINSE_R, 40, 199, f"Linse +{Z_L}\n= Bettachse", gr=1.9, col=C_PJ)
    v.text(0, F_Z0 + 25, "Fenster 160 × 120", gr=1.8, anker="c")

    # ---------------- Detail 2 Vertikalschnitt Fenster  M 1:2,5
    w = Ansicht(c, 338, 168, 1 / 2.5, rx=400, ry=290)
    titel(c, 336, 276, "Detail 2: Schnitt Fenster", "M 1:2,5", gr=3.0)
    w.schraffur(Y_FI, 290, PL, F_Z0 - 290, abstand=0.8, fill=C_HOLZ)
    w.schraffur(Y_FI, F_Z1, PL, Z_DE - F_Z1, abstand=0.8, fill=C_HOLZ)
    w.schraffur(400, Z_DE, Y_B1 - 400, PL, abstand=0.8, fill=C_HOLZ)
    w.rechteck(400, Z_L - 45, Y_LF - 400, 90, fill=C_PJ, falpha=0.45, lw=LW_DUENN)
    w.rechteck(Y_LF - 25, Z_L - LINSE_R, 25, 2 * LINSE_R, fill=Color(0.2, 0.3, 0.6), lw=LW_DUENN)
    w.text(420, Z_L - 5, "Beamer", gr=1.8, rot=90, anker="c")
    ende = Y_B1 + 30
    st_u = H_SHIFT * SH / L_PROJ
    st_o = (H_SHIFT + 1) * SH / L_PROJ
    st_omax = (H_MAX + 1) * 0.625 / TR_MIN
    w.poly([(Y_LF, Z_L - LINSE_R), (ende, Z_L - LINSE_R + st_u * (ende - Y_LF)),
            (ende, Z_L + LINSE_R + st_o * (ende - Y_LF)), (Y_LF, Z_L + LINSE_R)],
           fill=C_STRAHL, falpha=0.45, lw=LW_FEIN, col=C_STRAHL)
    w.linie(Y_LF, Z_L + LINSE_R, ende, Z_L + LINSE_R + st_omax * (ende - Y_LF), lw=LW_DUENN, col=C_ROT, dash=(1.5, 0.8))
    w.linie(Y_LF - 30, Z_L, ende + 5, Z_L, lw=LW_FEIN, dash=(4, 1, 0.6, 1))
    w.rechteck(Y_FI - 7, S_Z0, 3, S_Z1 - S_Z0, lw=LW_FEIN, dash=(1.2, 0.6), col=C_GRAU)
    for zz in (S_Z0 - 4, S_Z1 - 6):
        w.rechteck(Y_FI - 10, zz, 10, 10, fill=C_ALU, lw=LW_FEIN)
    w.mass(Y_LF, 295, Y_FI, 295, -3, fmt(FRONTSPALT))
    w.mass(Y_FI, 295, Y_B1, 295, -3, "19")
    w.mass(Y_B1, F_Z0, Y_B1, Z_L, -3, "35")
    w.mass(Y_B1, Z_L, Y_B1, F_Z1, -3, "85")
    absatz(c, 288, 214, [
        "gelb: Strahl bei gewähltem Bild",
        "rot: Extremfall Weitwinkel +",
        "voller Lens-Shift – bleibt im Fenster",
        "grau gestrichelt: Schieber zu (3 mm)",
        "Fensterkanten 3 mm gefast,",
        "Beamerfach innen mattschwarz",
    ], gr=1.9, zab=1.3)

    # ---------------- Detail 3 Bettverkleidung  M 1:4
    k = Ansicht(c, 40, 64, 1 / 4, rx=880)
    titel(c, 22, 184, "Detail 3: Bettverkleidung (Schnitt Längsseite)", "M 1:4", gr=3.0)
    k.linie(880, 0, 1110, 0, lw=LW_DICK)
    k.schraffur(880, -25, 230, 25, abstand=1.0)
    k.schraffur(1030 - 20, 0, 20, BETT_H, abstand=0.8, fill=C_HOLZ)
    k.schraffur(1030, VK_BODEN, VK, BETT_H - VK_BODEN, abstand=0.5, fill=C_VK)
    k.schraffur(1030 - 20 - 25, ROST_Z - 50, 25, 50, abstand=0.8, fill=C_HOLZ)
    k.rechteck(880, ROST_Z - 20, 1010 - 25 - 880, 20, fill=C_HOLZ, lw=LW_DUENN)
    k.rechteck(880, ROST_Z, 1010 - 880 - 5, MATR_H, fill=white, lw=LW_DUENN)
    for zz in (80, 190):
        k.linie(1030 - 20 - 3, zz, 1030 + 13, zz, lw=0.4, col=C_ROT)
        k.linie(1030 - 20 - 3, zz - 4, 1030 - 20 - 3, zz + 4, lw=0.6, col=C_ROT)
    k.mass(1030, BETT_H, 1049, BETT_H, 4, "19")
    k.mass(1049, VK_BODEN, 1049, BETT_H, -3, fmt(BETT_H - VK_BODEN))
    k.text(940, ROST_Z + 110, "Matratze", gr=1.8, anker="c")
    k.text(930, ROST_Z - 15, "Rost", gr=1.6, anker="c")
    k.hinweis_abs(1020, 245, 110, 140, "Bettrahmen: Stärke/Höhe\nam Bett messen (A)", gr=1.8)
    k.hinweis_abs(1040, 150, 110, 120, "Verkleidung 19 mm (wie Bank:\nEiche-Leimholz oder Multiplex)", gr=1.8)
    k.hinweis_abs(1035, 80, 110, 100, "Spax 4 × 35 von innen, alle 300 mm,\nBohrung im Rahmen Ø 6 (Holz arbeitet)", gr=1.8, col=C_ROT)
    k.hinweis_abs(1045, 5, 110, 80, "10 mm Luft zum Boden", gr=1.8)
    absatz(c, 22, 50, [
        "Oberkante Verkleidung = Oberkante Rahmen (nicht höher: Sitzkante).",
        "Ecken auf Gehrung 45° oder Längsseiten überstehend (2098).",
        "Fächerseite: in jedes Fach oben + unten Leiste 20×40 einsetzen und die",
        "Verkleidung von innen daran schrauben – oder Fächer behalten",
        "(Verkleidung mit Push-to-open-Türen).",
    ], gr=1.9, zab=1.3)

    # ---------------- Detail 4 Blockschaltbild
    titel(c, 152, 166, "Detail 4: Steuerung – Blockschaltbild (Grundvariante ohne Smart Home)", gr=3.0)

    def box(x, y, w_, h_, t, fill=white, gr=1.9, fett=False):
        c.setFillColor(fill)
        c.setStrokeColor(black)
        c.setLineWidth(0.3)
        c.setDash()
        c.rect(x, y, w_, h_, stroke=1, fill=1)
        c.setFillColor(black)
        zeilen = t.split("\n")
        for i, z in enumerate(zeilen):
            c.setFont("DVB" if (fett and i == 0) else "DV", gr)
            c.drawCentredString(x + w_ / 2, y + h_ / 2 + (len(zeilen) / 2 - i - 0.75) * gr * 1.2, z)

    def ver(pts, col=black, txt=None, tpos=None, dash=None):
        c.setStrokeColor(col)
        c.setLineWidth(0.35)
        c.setDash(list(dash), 0) if dash else c.setDash()
        for p0, p1 in zip(pts[:-1], pts[1:]):
            c.line(p0[0], p0[1], p1[0], p1[1])
        c.setDash()
        if txt:
            c.setFont("DV", 1.7)
            c.setFillColor(col)
            c.drawString(tpos[0], tpos[1], txt)
            c.setFillColor(black)
        c.setStrokeColor(black)

    C_230 = Color(0.65, 0.1, 0.1)
    box(152, 141, 34, 12, "Wandsteckdose\n230 V")
    box(196, 136, 46, 20, "Netzrelais K3\nSpule 12 V · 230 V ≥ 10 A\nin Dose (Elektriker)", fill=Color(1.0, 0.9, 0.9), fett=True)
    box(254, 140, 48, 14, "Beamer\nINITIAL START UP: ON", fill=Color(0.85, 0.9, 1.0), fett=True)
    box(314, 140, 42, 14, "Marshall (AUX)\nLautsprecher")
    box(366, 140, 38, 14, "Endschalter S2\nSchieber ganz AUF", fill=Color(1.0, 0.9, 0.9), fett=True)
    box(152, 114, 34, 14, "Steckdosenleiste\nDauer")
    box(254, 114, 48, 14, "Netzteil 12 V / 5 A\nimmer an")
    box(314, 112, 42, 16, "Kino-Relais K1\nFunk/WLAN\noder Schalter", fett=True)
    box(366, 112, 38, 16, "Zeitrelais K4\n5 min Nachlauf\n→ 2 Lüfter 140")
    box(152, 88, 34, 14, "HDMI-Switch\n3 → 1")
    box(196, 88, 46, 14, "Apple TV · Mac mini\nSwitch-Dock · LAN")
    box(254, 88, 48, 14, "IR-Verlängerung\nAuge zum Bett")
    box(314, 84, 42, 20, "Polwender K2\n2 Wechsler\nSpule an → AUF")
    box(366, 84, 38, 20, "Linearantrieb\n12 V, Hub 200\n→ Schieber")
    # 230 V
    ver([(186, 147), (196, 147)], col=C_230)
    ver([(242, 147), (254, 147)], col=C_230)
    ver([(169, 141), (169, 128)], col=C_230)
    ver([(186, 121), (254, 121)], col=C_230, txt="Dauer", tpos=(220, 122))
    ver([(178, 114), (178, 108), (219, 108), (219, 102)], col=C_230)
    ver([(186, 117), (248, 117), (248, 95), (254, 95)], col=C_230)
    # 12 V
    ver([(302, 121), (314, 121)])
    ver([(302, 117), (309, 117), (309, 94), (314, 94)])
    ver([(335, 112), (335, 104)], txt="Spule", tpos=(336, 106.5))
    ver([(356, 121), (366, 121)])
    ver([(356, 94), (366, 94)], txt="±12 V", tpos=(357, 95.5))
    ver([(302, 125), (308, 125), (308, 135), (385, 135), (385, 140)], txt="12 V", tpos=(372, 136))
    ver([(385, 154), (385, 158), (219, 158), (219, 156)], col=C_ROT, dash=(1.2, 0.6),
        txt="Verriegelung: K3 nur an, wenn S2 geschlossen", tpos=(290, 159.2))
    # Signale
    ver([(196, 95), (186, 95)], col=C_KALT)
    ver([(152, 95), (147, 95), (147, 161), (272, 161), (272, 154)], col=C_KALT, dash=(1.5, 0.8),
        txt="HDMI → Beamer", tpos=(150, 156))
    ver([(302, 147), (314, 147)], txt="Audio", tpos=(303, 148.5))
    absatz(c, 152, 78, [
        "**Ablauf",
        "Kino an: K1 ein → K2 zieht an → Antrieb fährt ein → Schieber AUF (≈ 5 s) → Endschalter S2 schließt → K3 gibt die "
        "Beamer-Steckdose frei → Beamer startet sofort ([INITIAL START UP] = ON, VMZ51S Anleitung S. 89). Lüfter an.",
        "Kino aus: K1 aus → Schieber fährt zu → S2 öffnet nach 1–2 mm → Beamer sofort stromlos; der Schieber erreicht das "
        "Fenster erst ≈ 0,5 s später. Direct Power Off ist laut Panasonic zulässig. Lüfter laufen 5 min nach (K4).",
    ], gr=1.95, breite=94, zab=1.28)
    absatz(c, 254, 78, [
        "**Harte Verriegelung: Beamer hat nur Strom, wenn der Schieber ganz offen ist",
        "Endschalter S2 (Mikroschalter mit Rollenhebel) sitzt an der Endlage AUF und schaltet die 12-V-Spule von K3. Ohne "
        "Software und ohne WLAN: Fällt Antrieb, Netzteil oder Relais aus, bleibt der Beamer aus. Projizieren auf den "
        "geschlossenen Schieber (Brandgefahr, Anleitung S. 13) ist damit ausgeschlossen.",
        "K3 schaltet 230 V: nur als geschlossenes Modul in einer Dose, Anschluss durch eine Elektrofachkraft. Alles andere ist 12 V.",
        "Beamer-Fernbedienung (IR-Verlängerung) bleibt für Eingang, Lautstärke und Bildmodus.",
    ], gr=1.95, breite=150, zab=1.28)
    b.fertig()


# ------------------------------------------------------------------ Blatt 4
def blatt4(c):
    b = Blatt(c, 4, 4, "Listen, Berechnungen, Inbetriebnahme", "Zuschnitt, Einkauf, Rechenwerte, Checkliste", "–")
    x0 = 18
    titel(c, x0, 274, "Zuschnittliste (Platte 19 mm; Maße L × B)", gr=3.4)
    hoehe_innen = Z_DE - Z_BO
    tiefe_innen = Y_FI - Y_RI
    zeilen = [["Pos", "Teil", "Stk", "L", "B", "Bemerkung"],
              ["1", "Boden Bank", "1", fmt(BETT_AX), fmt(BANK_T), "Ausschnitt 400 × 180 (Zuluft), Kabeldurchlass"],
              ["2", "Stirnseite links (Abluft)", "1", fmt(hoehe_innen), fmt(BANK_T), "Schlitzfeld 9 × 340 × 12"],
              ["3", "Stirnseite rechts (Zuluft)", "1", fmt(hoehe_innen), fmt(BANK_T), "Schlitzfeld 9 × 340 × 12"],
              ["4", "Front (Wandseite)", "1", fmt(BETT_AX - 2 * PL), fmt(hoehe_innen), f"Fenster 160 × 120, Linse +{Z_L}"],
              ["5", "Rückwand (Bettseite)", "1", fmt(BETT_AX - 2 * PL), fmt(hoehe_innen), "IR-Auge (Ø 10)"],
              ["6", "Trennwand T1 (Abluft)", "1", fmt(hoehe_innen), fmt(tiefe_innen), "Ausschnitt 280 × 100, Lochreihe"],
              ["7", "Trennwand T2 (Technik)", "1", fmt(hoehe_innen), fmt(tiefe_innen), "2 Öffnungen 300 × 80 unten, Lochreihe"],
              ["8", "Fachboden Beamer", "1", fmt(X_T2 - X_T1 - PL - 2), fmt(Y_LF - Y_RI), "Ausschnitt 450 × 380 (Luft)"],
              ["9", "Deckel links (Kanal)", "1", "709", fmt(BANK_T), "verschraubt"],
              ["10", "Deckel Mitte (Beamer)", "1", "968", fmt(BANK_T), "abnehmbar: Dübel + Magnete"],
              ["11", "Deckel rechts", "1", "419", fmt(BANK_T), "Scharniere, Stauraum"],
              ["12", "Verkleidung Längsseiten", "2", fmt(BETT_AY), fmt(BETT_H - VK_BODEN), "Maß nach Bett (A)"],
              ["13", "Verkleidung Kopf/Fuß", "2", fmt(BETT_B), fmt(BETT_H - VK_BODEN), "Maß nach Bett (A)"],
              ["14", "Zwischenboden Technik", "1", fmt(XB - PL - X_T2 - PL), fmt(tiefe_innen), "Bodenträger, Lochreihe"],
              ["15", "Lüfterträger", "1", fmt(hoehe_innen), fmt(tiefe_innen), f"2 Ausschnitte Ø {LUEFTER - 5}"],
              ]
    flaeche = (BETT_AX * BANK_T + 2 * hoehe_innen * BANK_T + 2 * (BETT_AX - 2 * PL) * hoehe_innen
               + 2 * hoehe_innen * tiefe_innen + (X_T2 - X_T1 - PL) * (Y_LF - Y_RI) + BETT_AX * BANK_T
               + 2 * BETT_AY * (BETT_H - VK_BODEN) + 2 * BETT_B * (BETT_H - VK_BODEN)) / 1e6
    y = tabelle(c, x0, 269, [10, 46, 9, 16, 14, 72], zeilen, gr=2.5, ausr=["c", "l", "c", "r", "r", "l"])
    y = absatz(c, x0, y - 5, [
        f"Plattenfläche netto ≈ {fmt(flaeche, 1)} m², mit 15 % Verschnitt ≈ {fmt(flaeche * 1.15, 1)} m² "
        f"(≈ {math.ceil(flaeche * 1.15 / 3.125)} Platten 2500 × 1250).",
        "Bank: Korpus verdübelt/verschraubt, Front und Rückwand zwischen den Stirnseiten, alles auf dem Boden.",
        "Füße: 6 verstellbare Möbelfüße 60 mm (Höhe ±10), 50 mm zurückgesetzt, mit Gummi-/Filzteller.",
        "Beamerfach innen mattschwarz streichen (kein Streulicht durchs Fenster).",
    ], gr=2.35, breite=165, zab=1.35)

    titel(c, x0, y - 5, "Einkaufsliste Technik und Beschläge", gr=3.4)
    teile = [["Teil", "Anforderung"],
             ["Kino-Relais K1 12 V", "Funk- oder WLAN-Relais (Handsender/App) oder Schalter"],
             ["Netzrelais K3", "Spule 12 V, Kontakt 230 V ≥ 10 A, in Dose (Elektriker)"],
             ["Mikroschalter S2", "Rollenhebel, Schließer, Endlage Schieber AUF"],
             ["Zeitrelais K4 12 V", "Abfallverzögerung, einstellbar ≈ 5 min (Lüfter)"],
             ["Steckdosenleiste (Dauer)", "≥ 6 Plätze: Apple TV, Mac, Dock, Switches, Netzteil"],
             ["HDMI-Switch 3 → 1", "4K, automatische Umschaltung, mit Fernbedienung"],
             ["LAN-Switch 5 Port", "für Mac mini, Apple TV, Beamer (PJLink)"],
             ["Kabelkanal", "unter der Bank + flach auf dem Boden bis zur Dose"],
             ["Netzteil 12 V DC", "≥ 5 A (Antrieb, Lüfter, Relais), immer an"],
             ["Relaismodul K2 12 V", "2 Wechsler (DPDT) ≥ 5 A als Polwender"],
             ["Linearantrieb 12 V", "Hub 200, ≥ 30 N, ≥ 40 mm/s, Endschalter intern"],
             ["2 Lüfter 140 mm 12 V", "je ≥ 75 m³/h, leise, + 2 Schutzgitter"],
             ["IR-Verlängerung", "Empfänger + Sender, USB 5 V"],
             ["Alu-Verbundplatte 3 mm", "≈ 200 × 152 (Schieber)"],
             ["Alu-U-Profil 10 × 10", "2 × 470, + PTFE-Gleitband"],
             ["Filtermatte G3", "Stirnseite rechts + Bodengitter"],
                                       ["Bodenträger, Möbelfüße", "4 × Ø 5 mm; 6 Füße 60 mm"],
             ["Schrauben", "Spax 4×35 (Verkleidung), 4×50 (Korpus), Dübel 8×40"],
             ]
    tabelle(c, x0, y - 9, [60, 107], teile, gr=2.4)

    # ---------------- Berechnungen
    x1 = 196
    titel(c, x1, 274, "Berechnungen", gr=3.4)
    rho_cp = 1.2 * 1005
    vdot = VDOT_M3H / 3600
    dt_n = (P_NORMAL + P_GERAETE) / (rho_cp * vdot)
    dt_q = (P_VX + P_GERAETE) / (rho_cp * vdot)
    a_frei = vdot / 1.5 * 1e4
    flaeche_bild = SW / 1000 * SH / 1000
    e_lx = LM_ECO / flaeche_bild
    leucht = e_lx * 0.8 / math.pi
    px = SW / 1920
    delta_px = px / L_PROJ * 1000
    kipp = 0.5 / PJ_T * 1000
    versatz = kipp * L_PROJ / 1000
    jahr_kwh = 15 * 8760 / 1000
    yb = absatz(c, x1, 267, [
        "**1  Bildlage (Formeln aus dem Datenblatt)",
        f"L = A + 64 = {fmt(L_PROJ)} mm. Bildbreite SW = {fmt(SW)} → TR = L/SW = {fmt(TR, 3)} (zulässig 1,09–1,77) ✓",
        f"SH = SW · 10/16 = {fmt(SH)}. Unterkante = Linse + h · SH → h = ({BILD_UK} − {Z_L}) / {fmt(SH)} = "
        f"{fmt(H_SHIFT, 3)} (zulässig 0,056–0,50) ✓",
        f"Oberkante = {BILD_UK} + {fmt(SH)} = {fmt(BILD_OK)} mm. Keine Trapezkorrektur → volle 1920 × 1200 Pixel.",
        "**2  Wärme und Lüftung",
        f"Leistung: VMZ51S Normal {P_NORMAL} W / Quiet {P_QUIET} W (Datenblatt); vorhandener VX500 {P_VX} W, Lampe 280 W "
        f"(Händlerdaten); Geräte im Technikfach ≈ {P_GERAETE} W (A). Praktisch alles wird Wärme.",
        f"ΔT = P / (ρ · c_p · V̇), ρ·c_p = 1,2 · 1005 = {fmt(rho_cp)} J/(m³K), V̇ = {VDOT_M3H} m³/h = {fmt(vdot, 3)} m³/s "
        f"(A: 2 × {LUEFTER} mm)",
        f"→ Abluft wärmer als Raum: VMZ51S + Geräte {fmt(dt_n, 1)} K, VX500 + Geräte {fmt(dt_q, 1)} K. Bei 24 °C Raum: "
        f"Abluft ≈ {fmt(24 + dt_q, 0)} °C.",
        "Die Ansaugung bekommt Raumluft (Unterdruck in der Bank). Grenzen: VMZ51S 45 °C (drosselt ab 36 °C), VX500 40 °C.",
        f"Freier Querschnitt je Seite bei v ≤ 1,5 m/s: A ≥ V̇/v = {fmt(a_frei)} cm². Bodengitter 400 × 180 mit 50 % frei "
        f"= 360 cm² ✓, Schlitzfeld je Stirnseite 9 × 340 × 12 = 367 cm² ✓, 2 Lüfter Ø 135 = 286 cm² ✓",
        "Kontrolle: VMZ51S zeigt Ansaug-/Ablufttemperatur im STATUS-Menü. VX500: Thermometer in den Abluftkanal, 2-h-Test.",
        "**3  Helligkeit und Auflösung",
        f"Quiet/Eco {fmt(LM_ECO)} lm auf {fmt(flaeche_bild, 2)} m² → E = {fmt(e_lx)} lx; weiße Wand (ρ ≈ 0,8): "
        f"L = E·ρ/π ≈ {fmt(leucht)} cd/m².",
        "Kino-Referenz 48 cd/m², Heimkino im Dunkeln ≈ 50–150 cd/m² → beide Beamer sind 2,5- bis 7-mal zu hell: Eco/Quiet, Bildmodus Kino.",
        f"16:9-Film: VX500 (XGA 1024 × 768) nutzt 1024 × 576 = 0,59 MP, VMZ51S 1920 × 1080 = 2,07 MP (3,5-fach). Pixel bei "
        f"{fmt(SW)} Breite: {fmt(SW / 1024, 2)} mm statt {fmt(SW / 1920, 2)} mm; aus 4,8 m Abstand "
        f"{fmt(SW / 1024 / 4800 * 3437.7, 1)}′ statt {fmt(SW / 1920 / 4800 * 3437.7, 1)}′ (Sehschärfe ≈ 1′) → beim VX500 Pixel sichtbar.",
        "**4  Erschütterung (warum die Bank frei steht)",
        f"1 Pixel = {fmt(SW)}/1920 = {fmt(px, 2)} mm → 1 Pixel Versatz entspricht {fmt(px, 2)}/{fmt(L_PROJ)} = "
        f"{fmt(delta_px, 2)} mrad Kippung.",
        f"Beamer auf dem Bettrahmen: 0,5 mm Durchbiegung (A) über 348 mm = {fmt(kipp, 2)} mrad → Bildversatz "
        f"{fmt(versatz, 1)} mm ≈ {fmt(versatz / px, 1)} Pixel.",
        "**5  Standby",
        f"VMZ51S Standby NORMAL (Netzwerk) 15 W → {fmt(jahr_kwh)} kWh/Jahr, ECO 0,5 W. VX500: Netzwerk-Standby 11,5 W, Eco 0,3 W.",
    ], gr=2.3, breite=202, zab=1.38)

    titel(c, x1, yb - 4, "Inbetriebnahme – Reihenfolge", gr=3.4)
    yb = absatz(c, x1, yb - 10, [
        "1. Bett liefern lassen, Rahmen messen (L, B, H, Brettstärke, Fächer) → Parameter in zeichnungen.py anpassen.",
        "2. Wandabstand A und Raumhöhe messen; Bildgröße aus der Tabelle auf Blatt 1 wählen.",
        "3. Beamer VOR dem Bau frei auf einen Hocker an die Bankposition stellen: Bildlage, Zoom, Lens-Shift, Geräusch prüfen.",
        "4. Bank bauen, Beamer einsetzen, Linse exakt auf die Bettachse; Bild mit Lens-Shift (Drehregler oben) setzen.",
        "5. Schieber ohne Beamer testen (20 × auf/zu), Prüflampe an der Beamer-Steckdose: nur bei ganz offenem Schieber an.",
        "6. Beamer-Menü [INITIAL START UP] = ON (VMZ51S, S. 89); beim VX500 prüfen, sonst nach dem Öffnen per Fernbedienung.",
        "7. Zeitrelais K4 auf ≈ 5 min Lüfternachlauf stellen.",
        "8. 2-h-Test im Normal-Modus, Temperaturen im STATUS-Menü notieren; danach Quiet als Standard.",
        "9. Menü: HDMI CEC → GERÄT → PROJEKTOR: EIN/AUS; Bildmodus Kino; Lens-Shift statt Trapez.",
        "10. Laufweg zwischen Bank und Wand: nicht in den Strahl schauen (Risikogruppe 2), Kinder!",
    ], gr=2.3, breite=202, zab=1.38)

    # ---------------- Kurzfassung + Quellen
    c.setFillColor(Color(1.0, 0.96, 0.85))
    c.setStrokeColor(C_ROT)
    c.setLineWidth(0.35)
    c.rect(x0, 50, 167, 32, stroke=1, fill=1)
    c.setFillColor(black)
    c.setStrokeColor(black)
    absatz(c, x0 + 3, 77, [
        "**Die sechs Punkte, an denen das Projekt scheitern kann",
        "1. Beamer nie aufs Bett: Die Bank steht frei auf dem Boden, sonst zittert das Bild.",
        "2. Zwangslüftung ist Pflicht: Panasonic verlangt sie bei Einbau in engen Räumen und haftet nicht für Schäden.",
        "3. Nie auf den geschlossenen Schieber projizieren (Brandgefahr): Endschalter S2 + Netzrelais K3 sperren den Strom.",
        "4. Linse auf die Bettachse, Bildhöhe nur per Lens-Shift einstellen, kein Trapez (sonst Pixelverlust).",
        "5. Beide Beamer sind fürs dunkle Schlafzimmer viel zu hell; der VX500 hat nur XGA (Pixel sichtbar) und braucht mehr Kühlung.",
        "6. Erst messen, dann sägen: Bettmaße und Wandabstand sind hier Annahmen.",
    ], gr=2.3, breite=160, zab=1.4)
    absatz(c, x0, 44, [
        "Quellen: Panasonic Spec File PT-VMZ51S (Stand 04/2023): Maße, Projektionstabelle, Lens-Shift, Leistung, Geräusch;",
        "Panasonic Operating Instructions PT-VMZ71/61/51/51S/41: Abstände zu Lüftungsöffnungen (S. 12, 21), Objektivdeckel (S. 13), "
        "Hitzeflimmern (S. 19), CEC (S. 97 f.), Shutter (S. 84).",
    ], gr=1.9, breite=228, zab=1.3)
    b.fertig()


def main():
    c = canvas.Canvas(AUSGABE, pagesize=(SEITE_B * MM, SEITE_H * MM))
    c.setTitle("Bauzeichnungen Bett mit verdecktem Beamer")
    c.setAuthor("Vorentwurf")
    for f in (blatt1, blatt2, blatt3, blatt4):
        f(c)
    c.save()
    print(f"geschrieben: {AUSGABE}")
    print(f"L = {L_PROJ}, TR = {TR:.3f}, h = {H_SHIFT:.3f}, Bild {SW:.0f} x {SH:.0f}, UK {BILD_UK}, OK {BILD_OK:.0f}")


if __name__ == "__main__":
    main()
