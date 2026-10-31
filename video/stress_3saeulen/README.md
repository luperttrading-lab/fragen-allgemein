# Info-Video „Chronischer Stress: Was hilft wirklich?“ (Stand 31.10.2026)

Aus einer Infografik wird ein Erklärvideo (1920×1080, 25 fps): rechts Bildausschnitte mit langsamer Kamerafahrt,
links ein Tafelbild mit Stichpunkten, Beweislage-Ampel und Quellenzeile, dazu Sprecherstimme und Untertitel.

## Dateien
- `szenen.json`: das Drehbuch. Je Szene Überschrift, Stichpunkte (`at` = ab welchem Satz), Ampel (`stark`/`mittel`/
  `schwach`/`keine`), Quellenzeile, Sätze und Einstellungen. Eine Einstellung ist ein Bildausschnitt `a` = [x0, y0, x1, y1]
  in Pixeln der Grafik. Ohne `b` zoomt die Kamera langsam um 8 % hinein, mit `"zoom": "out"` heraus, mit `b` fährt sie
  von `a` nach `b`. Ein Satz kann `{"t": Anzeigetext, "say": Sprechtext}` sein (Zahlen ausgeschrieben sprechen lassen).
- `fix_grafik.py`: malt die Tippfehler der KI-Grafik weg und setzt den Text neu → `grafik_korrigiert.png`.
- `render.py`: erzeugt Ton, Zeitplan, Untertitel und Video.
- `beschreibung.md`: Beschreibungstext mit Kapiteln und allen Quellen.

## Befehle
    python3 fix_grafik.py original.png grafik_korrigiert.png
    python3 render.py szenen.json grafik_korrigiert.png stress_video.mp4 --nur-ton    # Dauer prüfen
    python3 render.py szenen.json grafik_korrigiert.png stress_video.mp4 --vorschau   # Kontaktbogen
    python3 render.py szenen.json grafik_korrigiert.png stress_video.mp4 --bild 140   # Einzelbild bei 140 s
    python3 render.py szenen.json grafik_korrigiert.png stress_video.mp4              # Video (≈ 4–5 min Rechenzeit)

Voraussetzungen: ffmpeg, Pillow, numpy, `edge-tts` (im Cloud-Container Proxy-CA an certifi anhängen, siehe
`audio/seneca_kap1/README.md`). Satz-Audios landen in `tts_cache/` und werden nur bei geändertem Text neu erzeugt.

## Tonquelle austauschen
- Vorläufig: Microsoft Neural „Katja“ über edge-tts, Tempo +5 %, satzweise.
- Eigene Aufnahmen (z. B. ElevenLabs): je Satz eine Datei `<szene>_<nr>.mp3` (z. B. `s2_04.mp3`) in einen Ordner legen
  und `--ton-dir ordner` übergeben. Zeitplan, Stichpunkte, Kamerafahrten und Untertitel richten sich automatisch danach.
