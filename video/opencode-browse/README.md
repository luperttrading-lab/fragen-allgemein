# Erklärvideo „OpenCode Browse“ (08.11.2026)

Anlass: Video [„Alle zahlen für Claude in Chrome. Dabei geht es jetzt kostenlos!“](https://youtu.be/u0io4JD3CTk)
(ZeldoReacts, Reaktion auf ein Video des Kanals Hinter). Das Erklärvideo übernimmt weder Bild noch Ton daraus. Text und
Grafik sind neu, die Fakten sind an den Primärquellen geprüft (Tabelle unten).

- **Veröffentlicht:** [luperttrading-lab.github.io/ki-videos/opencode-browse](https://luperttrading-lab.github.io/ki-videos/opencode-browse/)
  (Repo `luperttrading-lab/ki-videos`, Web-Fassung 9,5 MB: CRF 32, Ton mono 64 kbit/s).
- **Endfassung v3** (09.11.2026): 7:53 min, Titelkarte (3,5 s), 14 Begriffs-Einblendungen (Zeit aus den Wortmarken),
  Einordnung „Agent oder Werkzeug“ in Szene 7, Web-App-Test in Szene 4, „nur am Computer“ in Szene 12.
  ElevenLabs gesamt: 2.604 + 826 = **3.430 Credits** (Zähler 84.217 → 87.647).
  Ausgabe: `out/opencode-browse_final.mp4` (Szene 1 einzeln nachgerendert und per concat-Filter eingesetzt;
  der concat-Demuxer brach dabei die Bildspur nach 80 s ab, weil die Teile yuvj420p und yuv420p hatten).
- **Fassung v2** (freigegeben 08.11.2026): 13 Szenen + 8 s Quellen, 7:13 min, 1920 × 1080, 30 fps, Remotion 4.0.541.
  Fassung v1 (4:48 min, Edge-Stimme) liegt im Git-Verlauf.
- Stimme: ElevenLabs „Christian – Warm and Captivating“ (`NBqeXKdZHweef6y0B67V`), Modell `eleven_v4`, Originaltempo.
  Tempo 0,93 (Seneca-Vorliebe) wirkte hier zu langsam: Christian liest diesen Text roh mit 2,2 Wörtern/s.
  Ton am Ende auf −16 LUFS normalisiert (`loudnorm`).
- **ElevenLabs-Kosten gemessen:** 6.060 Zeichen gesendet → 2.604 Credits abgebucht (Zähler 84.217 → 86.821), also
  ≈ 0,43 Credits je Zeichen, obwohl die Modellliste für `eleven_v4` 1,0 angibt. Probe vorher: 321 Zeichen → 138 Credits.
  Passt zur Messung beim Mathe-Video (7.162 gesendet, 3.079 abgerechnet).
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
| Claude in Chrome nur mit Claude, nur Abo | stimmt, aber es fehlt: läuft auch in Claude Code (`claude --chrome`), nur mit Abo-Login, nicht mit API-Schlüssel | [Claude-Code-Doku](https://code.claude.com/docs/en/chrome) |
| (fehlt im Video) Firma | Anomaly (Anomaly Innovations), Firma hinter SST und OpenCode | Recherche, [anoma.ly](https://anoma.ly) |
| (fehlt im Video) Alternativen | Playwright MCP `--extension` und Chrome DevTools MCP `--autoConnect` nutzen ebenfalls den eingeloggten Browser | Repos von Microsoft und Google |
| (fehlt im Video) Datenschutz | Erweiterung sammelt nichts, aber gelesene Inhalte gehen an den eingestellten Modellanbieter | [Datenschutzerklärung](https://raw.githubusercontent.com/anomalyco/browse/main/store/privacy-policy.md) |
| (fehlt im Video) echter Angriff | Brave, 20.08.2025: versteckter Reddit-Kommentar → Comet liest Gmail-Einmalcode aus und postet ihn | [brave.com](https://brave.com/blog/comet-prompt-injection/) |
| (fehlt im Video) Angriffe im Netz | Unit 42, 03.03.2026: indirekte Prompt Injection auf echten Webseiten gefunden | [unit42](https://unit42.paloaltonetworks.com/ai-agent-prompt-injection/) |
| (fehlt im Video) Tokens je Seite | ≈ 14.500–19.400 Tokens je voller Snapshot bei Playwright MCP (Einzelmessung) | [dev.to](https://dev.to/kuroko1t/how-accessibility-tree-formatting-affects-token-cost-in-browser-mcps-n2a) |
| Brave-Zitat „authenticated privileges“ | so nicht im Brave-Text; dort „operates with the user's full privileges across authenticated sessions“ | brave.com |
| Titel „geht jetzt kostenlos“ | irreführend: kostenlos ist nur das Werkzeug, das Modell kostet weiter (außer lokal) | – |

## Nachbauen

    python3 -m pip install edge-tts          # Proxy-CA an certifi anhängen, siehe audio/seneca_kap1/README.md
    python3 -I tts/eleven.py                 # Vorschau: was würde ElevenLabs kosten? (sendet nichts)
    python3 -I tts/eleven.py --ja            # vertont nur Szenen, die nicht im Cache tts/eleven_cache/ liegen
    # kostenloser Entwurf statt ElevenLabs: env -u ELEVENLABS_API_KEY python3 -I tts/entwurf.py
    cp /usr/share/fonts/opentype/inter/Inter-{ExtraBold,Bold,Medium,Regular}.otf public/
    npm install
    B=/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell
    npx remotion render src/index.js Erklaervideo out/opencode-browse_entwurf.mp4 --crf=20 --browser-executable=$B
    node stills.mjs 16.5 62 210            # Prüfbilder (Sekunden) in out/

Nur eine Szene neu sprechen: `python3 -I tts/entwurf.py --nur s07_vergleich`. Jede Szene hat eine eigene Tonspur;
die Animationen rasten an Stichwörtern ein (`cues` in `tts/skript.json`), Zeiten kommen aus den Wortgrenzen der Stimme.
Eine Textänderung kostet bei der späteren ElevenLabs-Fassung also nur die Zeichen der betroffenen Szene.
