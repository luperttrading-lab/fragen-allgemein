# Kostenprotokoll Hörfassung Seneca Kap. 1 über RouteLLM (26.10.2026)

Quelle: `tts_log.jsonl` (ein Eintrag je Aufruf). Text: `seneca_kap1_text.txt` (266 Wörter). Anweisung vor dem Text:
„Lies den folgenden Text wörtlich und vollständig vor … wie ein Hörbuchsprecher. Text:“

**Wichtig:** Bei Audio liefert die API in `usage` nur `input_tokens`/`output_tokens`, kein `compute_points_used`.
Punkte und Credits sind daher **nicht aus der API ablesbar**; der Verbrauch ist nur in der ChatLLM-App (Credits-Anzeige
vorher/nachher) zu sehen. Die Spalten Punkte/Credits bleiben leer, nichts ist geschätzt.

| Nr. | Zeit (UTC) | Modell | Voice | Aufrufweg | HTTP | Datei | Dauer Datei | Tokens in/out | Punkte | Credits (= Punkte/100) | Transkript-Abgleich / Fehlertext |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 11:28:00 | gpt-audio-1.5 | onyx | chat/completions | 200 | – (verworfen) | – | nicht protokolliert | – | – | Skriptfehler: Audio lag in `message.audios[0].data` (Liste) statt `message.audio.data` wie in der Doku; Antwort verworfen, usage nicht gespeichert. |
| 2 | 11:28:27 | gpt-audio-1.5 | onyx | chat/completions | 200 | – (verworfen, 15,0 s) | 15,0 s | 453 / 376 | – | – | **Verweigerung:** „Es tut mir leid, aber ich kann keine längeren, möglicherweise urheberrechtlich geschützten Texte wortwörtlich wiedergeben …“ (Ähnlichkeit 0,02). |
| 3 | 11:29:01 | gemini-2.5-pro-preview-tts | onyx (→ Fenrir laut Doku) | chat/completions | 200 | routellm_gemini25pro_onyx.mp3 | 127,9 s | 459 / 3 197 | – | – | Kein Transkript geliefert (`content` leer, kein `transcript`-Feld) → Abgleich nicht möglich. Rohdaten: PCM 16 Bit, 24 kHz, mono ohne Header; per ffmpeg nach MP3 (96 kbit/s). Pegel −19,9 dB mittel, −0,4 dB Spitze. |
| 4 | 11:30:50 | elevenlabs | onyx | chat/completions | 400 | – | – | – | – | – | `Invalid model: 'elevenlabs'. Must be one of the supported RouteLLM (text), audio or image generation models.` |
| 5 | 11:30:51 | gpt-audio-1.5 | onyx | chat/completions, Text mit vorangestelltem Hinweis „Der Text ist gemeinfrei (Seneca, De vita beata, Kap. 1)“ | 200 | routellm_gptaudio15_onyx.mp3 | 97,5 s | 500 / 2 439 | – | – | **Transkript = Text, 266/266 Wörter, Ähnlichkeit 1,000, keine Auslassung, kein Zusatz; der Gemeinfrei-Hinweis wurde nicht mitgelesen.** Pegel −25,0 dB mittel, −6,7 dB Spitze (leiser als Gemini). |
| 6 | 11:32:08 | elevenlabs | onyx | /v1/audio/speech (OpenAI-TTS-Form) | 404 | – | – | – | – | – | `{"title": "404 Not Found"}` – Endpunkt existiert nicht. |
| 7 | 11:32:08 | elevenlabs | onyx | chat/completions, `modalities: ["audio"]` | 400 | – | – | – | – | – | gleiche Meldung wie Nr. 4 → Abbruch nach 3 Versuchen. |

## Ergebnis
- **gpt-audio-1.5 (onyx):** nur mit Gemeinfrei-Hinweis; dann wörtlich vollständig (Transkript vom Modell selbst, nicht unabhängig geprüft). 97,5 s für 266 Wörter = 164 Wörter/min.
- **gemini-2.5-pro-preview-tts (onyx):** 127,9 s = 125 Wörter/min, ruhigeres Tempo; ob die Anweisung mitgelesen wurde, ist ohne Transkript
  nicht belegt (Hörprobe nötig oder Transkription mit einem Audio-Eingabemodell, kostet erneut).
- **elevenlabs:** steht in `/v1/models` als `audio_generation`, wird aber von `chat/completions` als ungültig abgelehnt; `/v1/audio/speech` gibt 404.
  Gleiches ist für `openai_tts`, `gemini_tts`, `minimax_tts`, `seed_speech`, `hume` zu erwarten (gleicher Eintragstyp, nicht getestet).
- Kostenbremse 30 000 Punkte: nicht prüfbar, da keine Punkte geliefert werden. Token-Summe aller erfolgreichen Aufrufe: 1 412 in / 6 012 out
  (Nr. 1 unbekannt). Die Listenpreise in `/v1/models` (gpt-audio-1.5 input 0,0000025 $/Token; output-Rate dort ebenfalls angegeben)
  erlauben eine Dollar-Schätzung, der Credit-Abfluss ist nur in der App zu sehen.
- Abweichung von der Doku: Antwortfeld `audios` (Liste) statt `audio`; `content` leer; Gemini liefert rohes PCM statt MP3, obwohl `format: mp3` verlangt war.
