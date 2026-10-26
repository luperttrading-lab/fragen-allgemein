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

## v2 (26.10.2026): Lesefassung v2, Gemini 2.5 Pro TTS, zwei Stimmen

Text: `seneca_kap1_text.txt` (v2, 1 651 Zeichen, 267 Wörter nach Normalisierung). Anweisung: `anweisung_v2.txt` (mit Aussprachehinweisen
„hineilt“, „Weg/Wege“). Aufruf: `tts.py --model gemini-2.5-pro-preview-tts --voice … --anweisung @anweisung_v2.txt`. Rohdaten beide Male
`audios[0].format = "L16"` (PCM 16 Bit, 24 kHz, mono, ohne Header) → ffmpeg s16le → MP3 96 kbit/s. Zeiten Europe/Berlin (CET).

| Nr. | Voice | Start | Ende | Aufruf | Datei | Dauer Datei | Tokens in/out | Pegel mittel / Spitze | Transkript |
|---|---|---|---|---|---|---|---|---|---|
| v2-1 | onyx (→ Fenrir) | 12:59:51 | 13:00:55 | 64,0 s | routellm_gemini25pro_onyx_v2.mp3 (1 184 301 B) | 98,7 s | 545 / 2 465 | −19,6 dB / −0,4 dB | keins geliefert (content leer) |
| v2-2 | echo (→ Charon) | 13:01:10 | 13:02:11 | 60,5 s | routellm_gemini25pro_echo_v2.mp3 (1 320 813 B) | 110,0 s | 545 / 2 749 | −18,9 dB / −0,3 dB | keins geliefert (content leer) |

**Kosten-/Credit-Felder:** keine. Geprüft wurden `usage` (nur input_tokens, output_tokens, raw_input_tokens), alle übrigen
Top-Level-Felder der Antwort (id, object, created, model) und sämtliche HTTP-Antwort-Header (CF-RAY, Content-Type, Date, Server-Timing,
x-envoy-upstream-service-time, x-request-id, CORS-Header, cf-cache-status, vary, server, Connection, Transfer-Encoding). Nichts davon
nennt Punkte, Credits oder Beträge. Der Credit-Abfluss ist nur in der ChatLLM-App ablesbar.

**Beobachtung:** output_tokens = 25 × Audiosekunden (2 465 / 98,7 = 24,97; 2 749 / 110,0 = 24,99). Gemini zählt Audio also mit
25 Token je Sekunde; eine Minute Sprache = 1 500 Output-Token.

**Dollar-Schätzung aus Listenpreisen** (Tokens beider Aufrufe: 1 090 in, 5 214 out):
- `/v1/models`: input_token_rate 0,000001 $/Token, **output_token_rate 0** → 0,0011 $ für beide Aufrufe zusammen.
- Audio-Doku laut Hauptsitzung: 0,005 $ je 1 000 Output-Token → 5 214 × 0,005 / 1 000 = 0,0261 $ plus Input 0,0011 $ = **≈ 0,027 $**
  für beide Seiten, d. h. ≈ 1,3 ct je Aufruf bzw. 0,75 ct je Audiominute.
- **Widerspruch:** `/v1/models` nennt für gemini-2.5-pro-preview-tts (und -flash-preview-tts) output_token_rate 0, die Doku 0,005 $/1K.
  Ein Output-Preis von 0 ist für ein TTS-Modell unplausibel; die Modellliste ist hier wahrscheinlich unvollständig, nicht gratis.
  Welche Zahl der Credit-Abrechnung zugrunde liegt, lässt sich nur per App-Vergleich (Credits vor/nach) klären. [Wahrscheinlich]

## v3 (26.10.2026): Gemini 2.5 Pro TTS onyx, Aussprache-Schreibweise „hin-eilt“

Whisper-Befund der Hauptsitzung zu v2: Fenrir sprach „hineineilt“ und „auf welchem Wege“ statt „Weg“, Charon „hineineilt“, „Wo diese“ statt
„dieser“, „daher die Situation“ statt „da ja die Situation“. Die Aussprachehinweise in der Anweisung wirkten nicht.
**Ersetzung für v3:** gesprochener Text = `seneca_kap1_text.txt` mit genau einer Ersetzung „hineilt“ → „hin-eilt“ (Scratch-Datei,
die Textdatei im Repo ist unverändert). Anweisung `anweisung_v3.txt`: Satz zu „hineilt“ ersetzt durch „„hin-eilt“ wird wie ein Wort
gesprochen: hin-eilt;“, Hinweis zu „Weg/Wege“ unverändert. Ein fehlgeschlagener Startversuch um 13:06 (Skript nicht gestartet, kein
API-Aufruf, keine Kosten) ist im Log nicht enthalten.

| Nr. | Voice | Start (CET) | Ende | Aufruf | Datei | Dauer Datei | Tokens in/out | Pegel mittel / Spitze | Transkript |
|---|---|---|---|---|---|---|---|---|---|
| v3-1 | onyx (→ Fenrir) | 13:11:45 | 13:12:47 | 61,7 s | routellm_gemini25pro_onyx_v3.mp3 (1 276 461 B) | 106,3 s | 541 / 2 657 | −19,5 dB / −1,0 dB | keins geliefert |

Kosten-/Credit-Felder: wie v2 keine. output_tokens / Sekunden = 2 657 / 106,3 = 24,99 (wieder 25 Token je Audiosekunde).
Dollar-Schätzung: Doku-Satz 0,005 $/1K Output → 0,0133 $ + Input 0,0005 $ ≈ **1,4 ct**; nach `/v1/models` (Output 0) 0,0005 $.

## Mehrfach-Durchläufe (26.10.2026): 14 satzweise Takes, Gemini 2.5 Pro TTS onyx, FLAC

Skript `takes/takes.py`, Vorgaben `takes/segmente.json` (5 Segmente, Stile A/B/C, s0 nur A/C), Log `takes/takes_log.jsonl`.
Rohdaten je Aufruf `L16` (PCM 16 Bit, 24 kHz, mono) → FLAC verlustfrei. 14 von 14 Aufrufen im ersten Versuch erfolgreich, keine Wiederholung.

| | Wert |
|---|---|
| Zeitfenster (Europe/Berlin, CET) | erster Start **15:21:02**, letztes Ende **15:24:51** |
| Aufrufe | 14 (alle HTTP 200) |
| Tokens gesamt | **2 469 in / 7 864 out** (Kostenbremse 15 000 out nicht erreicht) |
| Audio gesamt | 314,7 s (Takes 3,4 s bis 34,1 s) |
| Output-Token je Audiosekunde | 24,99 |
| Dollar nach `/v1/models` (in 0,000001 $/Token, out 0) | 0,0025 $ |
| Dollar nach Audio-Doku (out 0,005 $/1K) | **0,0418 $** |

Je Take (Start–Ende, Tokens in/out, Dauer): s0_A 15:21:02–15:21:08 97/106 4,25 s · s0_C 15:21:12–15:21:17 109/84 3,37 s ·
s1_A 15:21:17–15:21:36 201/730 29,21 s · s1_B 15:21:36–15:21:57 208/797 31,89 s · s1_C 15:21:57–15:22:15 213/696 27,85 s ·
s2_A 15:22:15–15:22:32 172/533 21,33 s · s2_B 15:22:33–15:22:51 179/650 26,01 s · s2_C 15:22:51–15:23:06 184/508 20,33 s ·
s3_A 15:23:06–15:23:22 167/541 21,65 s · s3_B 15:23:23–15:23:38 174/558 22,33 s · s3_C 15:23:38–15:23:52 179/485 19,41 s ·
s4_A 15:23:52–15:24:10 189/640 25,61 s · s4_B 15:24:10–15:24:34 196/851 34,05 s · s4_C 15:24:34–15:24:51 201/685 27,41 s.
Keine Kosten-/Credit-Felder in den Antworten (wie zuvor). Stil B ist durchweg am längsten (langsamer, mehr Pausen), C am kürzesten.

## Neufassung, Mehrfach-Durchläufe (26.10.2026): 42 satzweise Takes, Gemini 2.5 Pro TTS onyx, FLAC

Vorgaben `audio/seneca_neufassung/takes/segmente.json` (14 Segmente s0–s13 × Stile A/B/C), Skript `audio/seneca_kap1/takes/takes.py`
mit `TAKES_MAX_OUTPUT_TOKENS=30000`, Log `audio/seneca_neufassung/takes/takes_log.jsonl`. Alle 42 Aufrufe im ersten Versuch erfolgreich.

| | Wert |
|---|---|
| Zeitfenster (Europe/Berlin, CET) | erster Start **15:36:57**, letztes Ende **15:42:47** |
| Aufrufe | 42 (alle HTTP 200, keine Wiederholung) |
| Tokens gesamt | **4 535 in / 9 305 out** (Bremse 30 000 nicht erreicht) |
| Audio gesamt | 372,6 s (A 118,4 s · B 151,1 s · C 103,2 s) |
| Output-Token je Audiosekunde | 24,97 |
| Dollar nach `/v1/models` (in 0,000001 $/Token, out 0) | 0,0045 $ |
| Dollar nach Audio-Doku (out 0,005 $/1K) | **0,0511 $** |

Keine Kosten-/Credit-Felder in den Antworten. Stil B wieder am längsten (+28 % gegenüber A), C am kürzesten.

## Neufassung zügig (26.10.2026): 42 Takes mit Stilen D/E/F, Gemini 2.5 Pro TTS onyx, FLAC

Vorgaben `audio/seneca_neufassung/takes/segmente_zuegig.json` (14 Segmente × D/E/F), gleiches Skript, Log angehängt an
`audio/seneca_neufassung/takes/takes_log.jsonl`; A/B/C-Dateien unverändert. Alle 42 Aufrufe im ersten Versuch erfolgreich.

| | Wert |
|---|---|
| Zeitfenster (Europe/Berlin, CET) | erster Start **17:28:07**, letztes Ende **17:32:54** |
| Aufrufe | 42 (alle HTTP 200, keine Wiederholung) |
| Tokens gesamt | **4 857 in / 6 841 out** (Bremse 30 000 nicht erreicht) |
| Audio gesamt | 274,1 s (D 89,3 s · E 88,4 s · F 96,3 s) |
| Output-Token je Audiosekunde | 24,96 |
| Dollar nach `/v1/models` (in 0,000001 $/Token, out 0) | 0,0049 $ |
| Dollar nach Audio-Doku (out 0,005 $/1K) | **0,0391 $** |

Tempo-Vergleich über alle 14 Segmente: A 118,4 s · B 151,1 s · C 103,2 s · D 89,3 s · E 88,4 s · F 96,3 s. D und E sind damit
rund 25 % schneller als A und 41 % schneller als B; der Text (270 Wörter) läuft bei E mit ≈ 183 Wörtern/min.

## Neufassung v2 (überarbeiteter Text), 26.10.2026: 48 Takes A/D/E/F, Gemini 2.5 Pro TTS onyx, FLAC

Vorgaben `audio/seneca_neufassung_v2/takes/segmente.json` (12 Segmente s0–s11 × A/D/E/F, 240 Wörter), gleiches Skript,
Log `audio/seneca_neufassung_v2/takes/takes_log.jsonl`. Alle 48 Aufrufe im ersten Versuch erfolgreich.

| | Wert |
|---|---|
| Zeitfenster (Europe/Berlin, CET) | erster Start **21:31:09**, letztes Ende **21:36:51** |
| Aufrufe | 48 (alle HTTP 200, keine Wiederholung) |
| Tokens gesamt | **5 424 in / 8 497 out** (Bremse 30 000 nicht erreicht) |
| Audio gesamt | 340,4 s (A 101,5 s · D 75,7 s · E 75,9 s · F 87,3 s) |
| Output-Token je Audiosekunde | 24,96 |
| Dollar nach `/v1/models` (in 0,000001 $/Token, out 0) | 0,0054 $ |
| Dollar nach Audio-Doku (out 0,005 $/1K) | **0,0479 $** |

Tempo: D und E lesen die 240 Wörter in rund 76 s (≈ 190 Wörter/min), A in 101,5 s (≈ 142 Wörter/min).

## Neufassung v2, Nachlauf-Takes (26.10.2026): 48 Takes G/H/I/J mit Anfang des Folgesatzes, Gemini 2.5 Pro TTS onyx, FLAC

Vorgaben `audio/seneca_neufassung_v2/takes/segmente_puffer.json` (12 Segmente × G/H/I/J, Anweisungen wie A/D/E/F, Sprechtext mit
Nachlauf). Log angehängt an `audio/seneca_neufassung_v2/takes/takes_log.jsonl`; A/D/E/F-Dateien unverändert.
**Zwei Läufe:** Lauf 1 brach nach 10 Takes beim 11. Aufruf (s2_I) mit „ConnectionResetError: Connection reset by peer“ ab, bevor
eine Antwort vorlag; dieser Aufruf steht nicht im Log, sein Verbrauch ist unbekannt (ob der Dienst dafür Credits abzog, ist nicht
belegt). takes.py fängt seitdem Netzfehler ab und überspringt bei Wiederaufnahme vorhandene FLACs. Lauf 2 erzeugte die übrigen 38.

| | Wert |
|---|---|
| Zeitfenster Lauf 1 (Europe/Berlin, CET) | 21:41:51 – 21:43:08 (10 Takes) |
| Zeitfenster Lauf 2 | 21:43:55 – 21:49:25 (38 Takes) |
| Protokollierte Aufrufe | 48 (alle HTTP 200, keine Wiederholung) + 1 abgebrochener ohne Antwort |
| Tokens gesamt (protokolliert) | **5 652 in / 11 185 out** (Bremse 30 000 nicht erreicht) |
| Audio gesamt | 447,9 s (G 132,8 s · H 104,5 s · I 103,0 s · J 107,6 s) |
| Output-Token je Audiosekunde | 24,97 |
| Dollar nach `/v1/models` (in 0,000001 $/Token, out 0) | 0,0057 $ |
| Dollar nach Audio-Doku (out 0,005 $/1K) | **0,0616 $** |

## Neufassung v2, Satz 1 neu (26.10.2026): 6 Takes K–P für s0 („Glücklich leben, …“ ohne „zu“, mit Nachlauf)

Vorgaben `audio/seneca_neufassung_v2/takes/segmente_satz1.json`, Gemini 2.5 Pro TTS onyx, FLAC `s0_{K..P}.flac`. 6/6 im ersten Versuch.
Zeitfenster (Europe/Berlin, CET) **23:04:21 – 23:04:57**, Tokens **594 in / 717 out**, Audio 28,7 s (K 5,21 · L 4,85 · M 4,33 · N 4,93 ·
O 5,45 · P 3,97 s). Dollar: 0,0006 $ nach `/v1/models`, 0,0042 $ nach Doku-Satz.
