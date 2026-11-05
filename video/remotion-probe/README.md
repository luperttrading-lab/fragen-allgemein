# Remotion-Probe (05.11.2026)

Frage: Lohnt sich [Remotion](https://www.remotion.dev) (Videos als React/HTML-Code) für die Mathe-Lernvideos aus
`luperttrading-lab/5-Minuten-videos` gegenüber dem eigenen Python-Renderer (`themen/mathe-einmaleins/regel.py`, PIL)?

Ergebnisseite mit Nebeneinander-Video, Layout-Test und Formel-Vergleich:
[Remotion-Probe Mathe-Video](https://claude.ai/artifact/PAM9enLvXtKJQBCDBVPBgS)

## Ergebnis

| Punkt | Python (PIL) | Remotion |
|---|---|---|
| Aussehen | Original | identisch (mittlere Abweichung 1–2 von 255) |
| Rendern, 919 Bilder (30,6 s Video) | 27 s | 38–54 s |
| Code für das Kapitel | ≈ 360 Zeilen | 272 Zeilen |
| Rechenzeilen größer (36 → 44 px) | 1 Zahl | 1 Zahl |
| Langer Titel mit Umbruch reparieren | 32 Zeilen | 3 Zeilen |
| Bruch, Wurzel, Σ mit Grenzen, Binomialkoeffizient | nur Textzeile | KaTeX, eine Zeile TeX |

Entscheidung: Kopfrechen-Videos bleiben beim Python-Renderer (Rendern schneller, Änderungen meist gleich aufwendig).
Folgen mit Formeln oder Diagrammen entstehen in Remotion + KaTeX. Siehe Abschnitt in der `CLAUDE.md` des Repos.

## Inhalt

- `src/Trick.jsx`, `Karte.jsx`, `Rahmen.jsx`, `lib.jsx`: Nachbau von `s_regel`, `schritte`, `rahmen` aus `regel.py`
  (gleiche Koordinaten 1280 × 720, Ausgabe mit `--scale=1.5` in 1920 × 1080).
- `src/Formeln.jsx`, `src/FormelVergleich.jsx`: Formelsatz mit KaTeX im Look der Mathe-Videos.
- `src/zeiten.json`: Stichwortzeiten des Kapitels aus den ElevenLabs-Zeitmarken.
- `python/cache_pruefen.py`: prüft ohne `regel.py` auszuführen, ob alle Sprechtexte im TTS-Cache liegen (sonst kostet ein
  Lauf ElevenLabs-Zeichen); schreibt `szenen.json`.
- `python/prep.py`: berechnet Szenendauern und Stichwortzeiten aus dem Cache (Regeln aus `regel.py` nachgebaut).
- `python/original_kapitel.py`: rendert nur dieses Kapitel mit dem unveränderten Original-Renderer, samt Tonkette.

## Nachbauen (Cloud-Umgebung)

    git clone https://github.com/luperttrading-lab/5-Minuten-videos /tmp/5mv
    python3 -I python/cache_pruefen.py /tmp/5mv          # muss „ALLE IM CACHE“ melden
    python3 -I python/prep.py /tmp/5mv daten              # zeiten.json + kapitel.wav
    cp daten/zeiten.json src/ && mkdir -p public
    cp /usr/share/fonts/opentype/inter/Inter-{ExtraBold,Bold}.otf public/
    npm install
    B=/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell
    npx remotion render src/index.js Trick out/trick.mp4 --scale=1.5 --crf=19 --browser-executable=$B
    npx remotion still src/index.js FormelVergleich out/formeln.png --scale=1.5 --browser-executable=$B
    # Original zum Vergleich, ohne ElevenLabs-Schlüssel, damit ein Cache-Fehlgriff nichts kostet:
    env -u ELEVENLABS_API_KEY python3 python/original_kapitel.py /tmp/5mv $PWD/original

Remotion ist für Einzelpersonen und Firmen bis 3 Personen kostenlos, ab 4 Personen braucht es eine Firmenlizenz
([Lizenz](https://www.remotion.pro/license)).
