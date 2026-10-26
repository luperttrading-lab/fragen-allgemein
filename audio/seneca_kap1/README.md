# Hörfassung Seneca, Vom glücklichen Leben, Kap. 1 (Stand 26.10.2026)

- `seneca_kap1_seite_zeilengetreu.txt`: Buchseite Zeile für Zeile, mit Trennstrichen, Absatznummern, Fußnotenziffer.
- `seneca_kap1_text.txt`: Lesefassung v2. Wortlaut und Satzzeichen exakt wie im Buch (auch „daß“, „muß“, Gedankenstriche);
  entfernt sind nur Absatznummern „1 (1)“ und „(2)“, Fußnotenziffer und Silbentrennung; vorangestellt die Ansage
  „Seneca. Vom glücklichen Leben. Erstes Kapitel.“ Wortvergleich gegen die Seite: nur die Ansage weicht ab.
- Fassung v1 (bis 26.10. 12:30) hatte zwei Wortlautfehler: „, da ja die Situation hier nicht dieselbe ist“ war zu
  „. Denn die Situation ist hier nicht dieselbe“ umformuliert, und „– kurz wie es selbst dann ist“ hatte ein falsches
  Komma nach „kurz“ (Sinn: „kurz, wie es [das Leben] selbst dann ist“, nicht „kurz gesagt“). Dazu Satzzeichen geglättet.
  Alle MP3s ohne „_v2“ beruhen auf v1.
- Prüfung der Audios: Rückschrift mit faster-whisper large-v3-turbo und Wortabgleich. Gemini 2.5 Pro TTS (v1) sprach
  „hinein eilt“ statt „hineilt“, „auf welchem Wege“ statt „Weg“ und ein doppeltes „die“.

## Kostenlose Stimmen (hier erzeugt)
- `seneca_edge_*.mp3`: Microsoft-Neuralstimmen über `edge-tts` (Conrad, Florian multilingual, Katja), Tempo -8 %.
  Voraussetzung im Cloud-Container: Proxy-CA an certifi anhängen und `--proxy "$HTTPS_PROXY"` übergeben.
  Weitere deutsche Stimmen: Amala, Killian, Seraphina (multilingual).
- `seneca_piper_thorsten.mp3`: Piper (offline, ONNX), Stimme de_DE-thorsten-high (114 MB von huggingface.co/rhasspy/piper-voices),
  `--length-scale 1.1 --sentence-silence 0.4`; 14 s Rechenzeit für 82 s Audio.

## Bezahlte Stimmen über ChatLLM (RouteLLM API)
Endpoint /v1/chat/completions mit `modalities: ["text","audio"]`, `audio: {voice, format}`; Modelle gpt-audio-1.5, gpt-audio-mini,
gemini-2.5-flash-preview-tts, gemini-2.5-pro-preview-tts (Doku); zusätzlich in /v1/models: elevenlabs, openai_tts, gemini_tts,
minimax_tts, seed_speech, hume (undokumentiert). Ergebnisse und Kosten: KOSTEN_AUDIO.md (aus der Abacus-Sitzung).

## Befehle
    edge-tts --proxy "$HTTPS_PROXY" --voice de-DE-FlorianMultilingualNeural --rate=-8% --file seneca_kap1_text.txt --write-media out.mp3
    piper --model de_DE-thorsten-high.onnx --length-scale 1.1 --sentence-silence 0.4 --output_file out.wav < seneca_kap1_text.txt

## Wortprüfung der Gemini-Läufe (Whisper large-v3-turbo, Gegenprobe Whisper medium; Kontrolle Edge Florian v2: 0 echte Abweichungen)
Nicht gezählt: Schreibvarianten der Erkennung („umso“, „wie viel“, „das/dass“).

| Datei | echte Abweichungen vom Buch |
|---|---|
| routellm_gemini25pro_onyx (v1-Text) | „hinein eilt“; „auf welchem Wege“ statt „Weg“; doppeltes „die“ |
| routellm_gemini25pro_onyx_v2 | „hineineilt“; „auf welchem Wege“ statt „Weg“ |
| routellm_gemini25pro_echo_v2 | „hineineilt“; „Wo diese“ statt „dieser“; „daher die Situation“ statt „da ja die Situation“ |
| routellm_gemini25pro_onyx_v3 („hin-eilt“ im Sprechtext) | „zu Ursache“ statt „zur Ursache“; „Auf jenen lässt es“ statt „lassen es“ |

Befund: Gemini 2.5 Pro TTS glättet bei jedem Lauf 1–3 Stellen nach eigenem Sprachgefühl, an wechselnden Stellen.
Anweisungen im Prompt helfen nicht, Aussprache-Schreibweise im Sprechtext („hin-eilt“) schon. Für ein ganzes Buch:
satz- oder absatzweise erzeugen, jeden Abschnitt per Whisper prüfen, nur fehlerhafte Abschnitte neu erzeugen, zusammensetzen.
