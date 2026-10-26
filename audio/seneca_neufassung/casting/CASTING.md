# Casting-Vorprüfung: neue Sprachmodelle über RouteLLM (26.10.2026)

**Ergebnis: Keines der fünf Modelle ist über die RouteLLM-API erreichbar. Kein Audio erzeugt, 0 erfolgreiche Aufrufe, Casting entfällt.**

## Schritt 1: Erreichbarkeit (je 3 Versuche über POST /v1/chat/completions, alle HTTP 400, kostenlos)
Versuche je Modell: (a) modalities ["text","audio"], audio {voice echo, format wav}; (b) modalities ["audio"]; (c) voice alloy, format mp3.
Die Fehlermeldung ist bei allen 15 Aufrufen identisch und nennt weder Voices noch Parameter noch einen anderen Endpunkt:

    {"success": false, "error": "Invalid model: '<id>'. Must be one of the supported RouteLLM (text), audio or image generation models.
     See https://abacus.ai/help/developer-platform/route-llm for the full list.", "errorType": "UserFeedbackError"}

| Modell (`/v1/models`) | display_name | Ergebnis |
|---|---|---|
| gemini_tts | Gemini 3.8 Flash TTS | 400 Invalid model (3×) |
| minimax_tts | MiniMax Speech 2.8 HD | 400 Invalid model (3×) |
| openai_tts | OpenAI | 400 Invalid model (3×) |
| hume | Hume | 400 Invalid model (3×) |
| seed_speech | Seed Speech | 400 Invalid model (3×) |
| gemini-3.8-flash-tts, gemini-3.8-flash-preview-tts (Probe mit Google-Namen) | – | 400 Invalid model |

## Befund zur Modellliste
`/v1/models` führt 10 Einträge mit `model_type: audio_generation`. Nur vier davon tragen `api_formats: ["openai"]`, und genau diese
vier sind aufrufbar: **gpt-audio-1.5, gpt-audio-mini, gemini-2.5-flash-preview-tts, gemini-2.5-pro-preview-tts**. Die sechs ohne
`api_formats` (hume, elevenlabs, openai_tts, gemini_tts, minimax_tts, seed_speech) haben auch keine Token-Preise und sind offenbar
nur in der ChatLLM-Oberfläche nutzbar, nicht über RouteLLM. [Wahrscheinlich; Abacus dokumentiert das nicht]
Gemini 3.8 Flash TTS mit den 30 Google-Stimmen (Charon, Sadaltager, Iapetus, …), `<short pause>`-Tags und `speech_metadata.style`
ist über RouteLLM damit derzeit nicht erreichbar; Schritt 2 (Stimmen-Casting) und Schritt 3 (Stilfeld-Probe) konnten nicht laufen.

## Was bleibt
- Über RouteLLM: gemini-2.5-pro-preview-tts mit den sechs OpenAI-Namen (onyx→Fenrir, echo→Charon, …), kein Stilfeld bekannt.
- Direkt bei Google (Gemini API, eigener Schlüssel) wäre gemini-3.8-flash-tts mit allen 30 Stimmen und Pausen-Tags nutzbar.
- Log aller 17 Aufrufe: `casting_log.jsonl` (Zeiten Europe/Berlin, Body ohne Text, vollständige Fehlertexte).
