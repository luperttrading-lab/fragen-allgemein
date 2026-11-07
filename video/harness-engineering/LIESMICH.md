# Harness-Video – zwei Testvideos (07.11.2026)

Test, was wir zusammen produzieren können: 5 Minuten „Was ist ein Harness?“ für Leute, die ChatGPT oder Claude nutzen,
aber nicht programmieren. Inhalt nach [Alex Sprogis](https://youtu.be/SU0EyB45x6Q) und
[Composio](https://composio.dev/content/best-ai-agent-harnesses), eigene Texte, eigene Bilder, eigener Statistik-Teil.

- **A:** Peter (ElevenLabs „Peter Hartlapp – Tiefe Podcaststimme“) erzählt allein.
- **B:** wie A, dazu zwei Funk-Einwürfe (Szene 4 Werkzeuge, Szene 6 Datenbank): Modell = Mila, Harness = Helmut mit
  Funkfilter und „Harness an Modell: …“; unten eine Fußzeile, wer gerade funkt.
- Vorschau: [Harness-Video · Vorschau](https://claude.ai/artifact/SUukL3chTe1w4JZjKeV1B6)
  (Slug `ce5a0e07-ef2e-4787-9c06-3ee1966d84b9`, 720p, je ≈ 10 MB).

## Bauen

    ./video.sh A /pfad/zum/ausgabeordner     # bzw. B; Ton kommt aus tts_cache/, kostet dann nichts

- `skript.py` – Sprechtexte beider Varianten; Marker `‹name›` vor einem Wort = Zeitpunkt einer Bildeinblendung.
- `ton.py` – je Szene ElevenLabs Text-to-Dialogue mit Zeitmarken (`eleven_v4`, höchstens 2.000 Zeichen je Anfrage),
  Cache `tts_cache/`, Funkfilter + Klick nur auf Harness-Zeilen, Pausen, −16 LUFS; schreibt `zeitplan_<V>.json`.
- `film.html` – alle Szenen als HTML/SVG, `render(t)` setzt jeden Zustand aus der Zeit; Texte als echter Text (keine
  Tippfehler wie in KI-Bildern). `render.js` – Playwright, 4 Seiten parallel, je ein ffmpeg-Teil, 25 fps, 1080p.
- `bilder/` – Illustrationen mit GPT Image 2 über RouteLLM (`bilder/erzeugen.sh`, Referenz `pilot_rollfeld.png`
  für einheitlichen Stil; Schlüssel `ABACUS_API_KEY`, in dieser Umgebung vorhanden).
- Ältere Proben: `drehbuch.md` (Dialogfassung, verworfen), `hoerprobe*.py`, `probe/`.

## Messwerte (Maßstab: Zeit und Kosten je Runde)

| Schritt | Zeit | Kosten |
|---|---|---|
| 6 Illustrationen (GPT Image 2, 1536×1024, parallel) | ≈ 35 s | 8.903 Punkte ≈ 89 Credits ≈ 6 ct |
| Ton A, 9 Szenen, 4.307 Zeichen gesendet | 76 s | |
| Ton B, nur die 2 Funk-Szenen neu, 973 Zeichen | 19 s | |
| ElevenLabs-Zähler für A + B zusammen | | 2.268 Zeichen abgerechnet (5.280 gesendet) |
| Video rendern (Bilder 3 min + Kodieren) | A 4:09, B 4:25 | – |
| Neu bauen ohne Textänderung (Ton aus Cache) | ≈ 4,5 min je Variante | 0 |

- Eine Textänderung in einer Szene vertont nur diese Szene neu (≈ 400–800 Zeichen), dann ≈ 4,5 min Rendern.
- Remotion nicht benutzt: hier nicht installiert, und das eigene HTML-Rendern braucht ≈ 4 min für 5 min Video;
  nach der Remotion-Probe (38–54 s je 30 s) wären es ≈ 6–9 min. [Wahrscheinlich, hochgerechnet]
