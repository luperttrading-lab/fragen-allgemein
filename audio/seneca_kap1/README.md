# Hörfassung Seneca, Vom glücklichen Leben, Kap. 1 (Stand 26.10.2026)

Text: aus dem Foto der Buchseite abgetippt, Lesefassung (ohne Absatznummern "1 (1)", ohne Fußnotenziffer,
Gedankenstriche durch Kommas/Punkte ersetzt, "daß" → "dass", Überschrift mit Autor vorangestellt).

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
