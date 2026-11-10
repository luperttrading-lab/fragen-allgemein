# Poster „Anatomy of a Black Hole“, 67,5 × 48 cm quer

Nachbau der Vorlage (Querformat, Interstellar-Look), aber **neu gerechnet statt hochskaliert**: Die Vorlage ist 1179 px
breit, der Druck braucht 7972 × 5669 px (300 dpi), also das 6,8-Fache.

## Erzeugen

    python3 render.py --preview            # Vorschau 1400 px, ca. 25 s
    python3 annotate.py --tag preview
    python3 render.py                      # Druckfassung, Bild ohne Text -> out/render_full.npy
    python3 annotate.py --tag full --variant korrigiert
    python3 annotate.py --tag full --variant original

Ergebnis je Textfassung in `out/`: JPEG und PDF, einmal exakt 675 × 480 mm, einmal mit 3 mm Beschnitt rundum
(681 × 486 mm, für Druckereien, die Beschnittzugabe verlangen). Die Schrift (Saira, SIL Open Font License) lädt
`annotate.py` beim ersten Lauf nach `fonts/`.

## Was physikalisch gerechnet ist und was nicht

- Gerechnet (Schwarzschild, G = c = M = 1): Lichtbahnen über `u'' + u = 3u²`, tabelliert für ~12.000 Stoßparameter b.
  Daraus ergeben sich der Schatten (Radius √27 M), der Photonenring und das Linsenbild: Der Bogen über dem Schatten ist
  die Rückseite der Scheibe, der Ring unten ihre Unterseite. Hinzu kommen Doppler- und Gravitationsverschiebung
  `g = √(1−3/r) / (1−Ωλ)` der Kepler-Scheibe.
- Abgeschwächt bzw. gestaltet:
  - Die Doppler-Aufhellung ist `g^2,2` statt physikalisch `g^3…4`, wie bei Interstellar, sonst wäre eine Seite fast schwarz.
  - Die Scheibe leuchtet bis r = 3,8 M statt nur bis zur ISCO bei 6 M (Look eines schnell rotierenden Lochs).
  - Die Textur (Schlieren, Flocken) und der Jet sind gestaltet.
  - Die Scheibe ist als optisch dünne Leuchtschicht gerechnet, die Helligkeit wächst mit dem Lichtweg 1/cos θ.
    Den Auftreffwinkel liefert die Bahn geschlossen: cos θ = √(a² + c²) / √(r²/b² + 2/r).
    Deshalb ist das Band von der Seite hell und deckend, der gelinste Halo und der untere Ring sind zart.
    Außen dunkelt Staub ab.
  - Die Sterne sind ungelinst: Im Bildausschnitt läge sonst fast alles im Einstein-Ring und die Sterne würden zu Bögen.
- Textfassung `korrigiert` berichtigt zwei Aussagen der Vorlage:
  - Der Photonenring liegt beim 1,5-Fachen des Horizontradius, nicht „knapp darüber“.
  - Die schwarze Scheibe ist der Schatten, rund 2,6-mal größer als der Horizont.
