# Erklärvideo „OpenCode Browse“ (08.11.2026)

Anlass: Video [„Alle zahlen für Claude in Chrome. Dabei geht es jetzt kostenlos!“](https://youtu.be/u0io4JD3CTk)
(ZeldoReacts, Reaktion auf ein Video des Kanals Hinter). Das Erklärvideo übernimmt weder Bild noch Ton daraus. Text und
Grafik sind neu, die Fakten sind an den Primärquellen geprüft (Tabelle unten).

- Länge 4:48 min (11 Szenen + 6 s Quellen), 1920 × 1080, 30 fps, Remotion 4.0.541. Rendern: 6:16 min auf 4 Kernen,
  22,6 MB (`--crf=20`). Pegel der Entwurfsstimme −24,5 dB im Mittel, für YouTube vor dem Hochladen anheben.
- Stimme im Entwurf: Microsoft Edge `de-DE-FlorianMultilingualNeural` über `edge-tts` (kostenlos). ElevenLabs erst nach
  Freigabe des Sprechtexts (`SPRECHTEXT.md`), siehe Kostenregel in der `CLAUDE.md` des Repos.
- Werkzeugwahl: Remotion, weil das Video aus Diagrammen, Pfeilketten, Tabellen und Kästen mit Textumbruch besteht. Das
  ist der Fall, in dem Remotion in der Probe (`video/remotion-probe/`) klar billiger war.

## Faktencheck (Stand 08.11.2026)

| Aussage im Quellvideo | Befund | Quelle |
|---|---|---|
| Agent → MCP-Server → Relay (lokal) → Erweiterung → Chrome-Debugger | stimmt, Relay auf `127.0.0.1:19988`, Erweiterung über WebSocket, `chrome.debugger` | [README](https://github.com/anomalyco/browse) |
| Updates: stündlich (Original) bzw. „nur einmal am Tag“ (Korrektur des Reaktors) | **Korrektur falsch**: „at launch and at least once an hour“, abschaltbar | README, Abschnitt Install |
| Version 0.0.14 | inzwischen 0.0.15 (npm `latest`), Paket seit 30.10.2026 auf npm | [npm](https://www.npmjs.com/package/@opencode/browse) |
| Kopplungscode einmal, 10 Minuten | stimmt | README, Security |
| Cookies löschen, Browser schließen verboten; Allowlist ab Werk aus | stimmt (Allowlist „opt-in“) | README, Security |
| „Behandle Agenten-Code wie Code, der als du läuft“ | stimmt sinngemäß („treat code an agent runs as code running as you“) | README, Security |
| Ollama: unter 24 GB VRAM 4k Kontext, Agenten ≥ 64.000 | stimmt | [Ollama-Doku](https://docs.ollama.com/context-length) |
| Prompt Injection: fast 1 von 4, mit Schutz etwa 1 von 9 | stimmt: 23,6 % → 11,2 % (Aug. 2025, 123 Testfälle) | [Anthropic, Aug. 2025](https://www.anthropic.com/news/claude-for-chrome) |
| Später etwa 1,5 % | 1,4 % (Opus 4.5 mit neuen Schutzmaßnahmen, Nov. 2025), **anderer Test** (adaptiver Best-of-N-Angreifer) | [Anthropic, Nov. 2025](https://www.anthropic.com/research/prompt-injection-defenses) |
| Claude in Chrome nur im Abo ab 20 $/Monat | wahrscheinlich: alle bezahlten Pläne, Pro 20 $; nur Drittquellen geprüft | Websuche 08.11.2026 |
| „Claude hat bei GitHub 112.000 Passwörter geleakt“ | nicht belegt, nicht ins Video übernommen | – |
| „Claude in Chrome läuft mit Haiku“ | nicht belegt („mein Wissensstand“), nicht übernommen | – |
| Titel „geht jetzt kostenlos“ | irreführend: kostenlos ist nur das Werkzeug, das Modell kostet weiter (außer lokal) | – |

## Nachbauen

    python3 -m pip install edge-tts          # Proxy-CA an certifi anhängen, siehe audio/seneca_kap1/README.md
    env -u ELEVENLABS_API_KEY python3 -I tts/entwurf.py      # public/*.mp3, src/zeiten.json, Wortzeiten
    cp /usr/share/fonts/opentype/inter/Inter-{ExtraBold,Bold,Medium,Regular}.otf public/
    npm install
    B=/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell
    npx remotion render src/index.js Erklaervideo out/opencode-browse_entwurf.mp4 --crf=20 --browser-executable=$B
    node stills.mjs 16.5 62 210            # Prüfbilder (Sekunden) in out/

Nur eine Szene neu sprechen: `python3 -I tts/entwurf.py --nur s07_vergleich`. Jede Szene hat eine eigene Tonspur;
die Animationen rasten an Stichwörtern ein (`cues` in `tts/skript.json`), Zeiten kommen aus den Wortgrenzen der Stimme.
Eine Textänderung kostet bei der späteren ElevenLabs-Fassung also nur die Zeichen der betroffenen Szene.
