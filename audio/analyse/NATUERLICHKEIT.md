# Welche Hörfassung klingt am natürlichsten? (Seneca Kap. 1, Stand 26.10.2026)

## Methode
- Referenz: 7 echte deutsche Vorleser von LibriVox (gemeinfrei, `referenzen_librivox.txt`), je 100 s ab Sekunde 45,
  darunter „Vom glückseligen Leben“ (Seneca, ältere Übersetzung, Sprecher „redaer“) und zwei Sprecherinnen.
- Alle Dateien auf 16 kHz mono, 100 s. Wort-Zeitstempel mit faster-whisper large-v3-turbo (`stt_wav.py`).
- `prosodie.py`: Tempo (Wörter je Sekunde Sprechzeit), Tempo-Schwankung, Pausenanteil, Pausen-Schwankung, Wörter je Phrase,
  Melodie-Spannweite (Halbtöne 5.–95. Perzentil), Tonhöhenabfall innerhalb der Phrase, Jitter, Shimmer, HNR, Atemgeräusche.
  Pausenschwelle: max(p95 − 35 dB, p10 + 6 dB), damit verrauschte Heimaufnahmen funktionieren.
- `dnsmos_run.py`: Microsoft DNSMOS (Paket `speechmos`), misst technische Sprachqualität, nicht Natürlichkeit.
- UTMOS (Natürlichkeitsmodell) nicht genutzt: Laden über torch.hub vom Auto-Modus blockiert (fremder Code); PyPI-Paket
  `utmos` ist eine inoffizielle Neuverpackung mit fairseq-Abhängigkeit.

## Ergebnis
- Gesamtabstand (RMS der z-Werte) trennt nicht: echte Sprecher liegen untereinander bei 0,6–4,4, alle Synthese-Dateien bei 1,0–1,8.
- Merkmal für Merkmal gegen die Spannweite der Menschen ohne Extremwerte (7 Merkmale):

| Datei | im menschlichen Bereich | auffällig |
|---|---|---|
| Gemini Fenrir v1 (`routellm_gemini25pro_onyx.mp3`) | 5/7 | Melodie lebhafter, Phrasenenden fallen stark; 2 echte Atemzüge |
| Edge Katja | 4/7 | kein Atem, stark fallende Phrasenenden |
| gpt-audio Onyx | 3/7 | monoton (6,1 Halbtöne, unter allen Menschen), schnell |
| Gemini Fenrir v2 | 2/7 | wenig Pausen, lange Phrasen, schnell |
| Edge Florian | 2/7 | sehr schnell, gleichförmige Pausen |
| Gemini Fenrir v3 | 1/7 | liest durch: 5,9 % Pausen, 19 Wörter je Phrase, gleichförmige Pausen |
| Piper Thorsten, Edge Conrad, Gemini Charon v2 | 0–1/7 | |

- Atem-Prüfung Fenrir v1: Ereignisse bei 6,7 s und 42,8 s stimmlos, spektrale Flachheit 0,65, −40 dB: echte Atemzüge.
- DNSMOS: alle modernen Synthese-Stimmen technisch sauberer als die LibriVox-Aufnahmen; nur Piper fällt ab.
- Folgerung: Dieselbe Stimme schwankt zwischen zwei Durchläufen stärker als zwischen Stimmen. Für ein Buch je Absatz mehrere
  Durchläufe erzeugen, erst nach Worttreue (Whisper) filtern, dann nach Prosodie auswählen.

## Best-of-N, satzweise (26.10.2026, 15:21–15:25 Uhr erzeugt)
14 Takes Gemini 2.5 Pro TTS onyx (je Satz Stil A/B/C, Ansage A/C), Auswahl mit `bestof.py`:
- Worttreue: 2 von 14 Takes echt fehlerhaft verworfen bzw. nicht gewählt („zielen“ statt „ziehen“ in s4_A; s1_A unklar „Galliot“).
  „Gallio“/„Galio“ ist nur Schreibweise der Erkennung und wird gleich behandelt.
- Gewählt: s0_C, s1_C, s2_B, s3_A, s4_B. Ränder geschnitten, Lautheit angeglichen, Pausen 1,4 s nach Ansage und zwischen
  Absätzen, 0,75 s zwischen Sätzen. Ergebnis `seneca_kap1/seneca_kap1_bestof.mp3`, 118 s.
- Endkontrolle: Whisper large-v3-turbo wortgetreu; medium meldete ein fehlendes „uns“, large-v3, turbo und medium auf dem
  Ausschnitt hören es: Fehlalarm.
- Summe der Überschreitungen der menschlichen Spannweite (in Bereichsbreiten, 6 Merkmale, 0 = ganz im Bereich):

| Fassung | Abstand |
|---|---|
| Best-of-Montage | 0,66 |
| Edge Katja | 2,14 |
| Edge Conrad | 2,66 |
| Piper Thorsten | 3,08 |
| Gemini Fenrir v1 | 3,17 |
| gpt-audio Onyx | 4,00 |
| Gemini Fenrir v2 | 5,71 |
| Gemini Charon v2 | 6,93 |
| Edge Florian | 7,43 |
| Gemini Fenrir v3 | 7,96 |

  Montage knapp außerhalb bei Tempo (2,69 statt ≤ 2,57 W/s), Melodie (12,2 statt ≤ 11,7 HT) und Abfall (−1,71 statt ≥ −1,58).

## Neufassung (Text des Nutzers), Best-of-N (26.10.2026, Takes 15:36:57–15:42:47 Uhr)
42 Takes Gemini 2.5 Pro TTS onyx (14 Sätze × Stil A/B/C), 9 305 Output-Token. Verworfen: s0_C („Gallie“). Gewichtung der
einheitlichen Stimmlage (`BESTOF_F0W`, Halbtöne je Strafpunkt) verglichen:

| F0W | Abstand | Melodie HT | Abfall HT/s |
|---|---|---|---|
| 3 | 1,77 | 13,58 | −2,34 |
| 1,5 | 1,61 | 13,27 | −2,36 |
| 0,75 | **0,70** | 12,81 | −1,67 |

Gewählt F0W 0,75 (jetzt Voreinstellung): Tempo 2,26 W/s, Pausen 16,4 %, 6,0 Wörter/Phrase, Pausen-Schwankung 0,64 im
menschlichen Bereich; Melodie knapp darüber. Endkontrolle turbo und medium wortgetreu. `seneca_neufassung/seneca_neufassung_bestof.mp3`, 145 s.

## Neufassung zügig (26.10.2026, Takes D/E/F 17:28–17:33 Uhr)
Rückmeldung des Nutzers: erste Auswahl zu langsam; in Satz 1 klingt „wollen alle“ gesungen („aaalle“).
- Messbar als Schlussbogen: Tonhöhenumfang in der letzten Sekunde vor der Pause, s0_A 10,1 Halbtöne, die anderen Varianten 5,8–9,5.
  Ein Bogen innerhalb des Wortes allein (4,5) und die Wortdauer zeigen nichts. Kriterium in `bestof.py`: Strafe ab 9 Halbtönen.
- Zieltempo nach Nutzerwunsch `BESTOF_TEMPO=2.6,3.0` statt LibriVox-Bereich (2,08–2,57).
- 42 neue Takes mit Stilen D/E/F (zügig, ruhige Satzmelodie), zusammen mit A/B/C 84 Kandidaten. Endkontrolle jetzt satzweise
  (am Stück übersprang Whisper Passagen): alle 14 Segmente wortgetreu.
- Ergebnis `seneca_neufassung_bestof.mp3`, 121,9 s, Tempo 2,66 W/s (vorher 2,27), Pausenanteil 16 %; Satz 1 aus Take E (Schlussbogen 5,8).
  Abstand mit Wunschtempo: 0,42 (erste Auswahl 1,54). Erste Auswahl bleibt als `seneca_neufassung_bestof_v1.mp3`.

## Neufassung v2 (überarbeiteter Text, 26.10.2026 abends)
- Befund: Gemini bricht viele Takes mitten im letzten Laut ab (erste Neufassung: 45/84 laut endend, 23/84 hart abgeschnitten;
  Stil E 14/14). Anfänge sind sauber, die Sprache setzt nur sofort ein.
- Gegenmittel „Nachlauf“: Satz plus die ersten vier Wörter des nächsten Satzes einsprechen (letzter Satz: „Ende des ersten
  Kapitels.“), `bestof.py` findet das Satzende und schneidet in der Pause davor. Abgeschnittene Enden: ohne Nachlauf 21/48,
  mit Nachlauf 10/48 (ruhige Stile G und J je 1/12).
- Randprüfung auf Sample-Ebene (letzte 2 ms > 3 % der Spitze oder letzte 30 ms laut); abgeschnittene Takes nur, wenn kein sauberer da ist.
- 96 Takes (A/D/E/F ohne, G/H/I/J mit Nachlauf). Gewichtung der Stimmlage verglichen: F0W 0,75 → Abstand 1,79; 1,5 → 1,33;
  3 → 1,12 (gewählt). Alle 11 Satzübergänge klingen auf ≤ −50 dB aus, kein harter Abbruch. Endkontrolle satzweise wortgetreu.
- Ergebnis `seneca_neufassung_v2/seneca_neufassung_v2_bestof.mp3`, 103,8 s, Tempo 2,75 W/s; noch über dem Zielbereich:
  Wörter je Phrase 9,2 (Ziel ≤ 7,4) und Melodie 12,7 Halbtöne (≤ 11,7).

## ElevenLabs eleven v4 (Aufnahmen des Nutzers, 26.10.2026)
Christian „Warm and Captivating“ und Robert Ranger „Cool Storyteller“, je Absatz 1–2 des überarbeiteten Textes am Stück (51 s).
Beide wortgetreu (turbo und medium), keine Atemgeräusche, saubere Enden. Vergleich auf genau diesem Textteil (Gemini-Montage auf
denselben 7 Sätzen zugeschnitten, 56,6 s):

| Fassung | Abstand | Tempo W/s | Pausen % | W/Phrase | Pausen-Schwankung | Melodie HT | Abfall HT/s |
|---|---|---|---|---|---|---|---|
| ElevenLabs Christian | 2,47 | 2,87 | 12,1 | 8,1 | 0,52 | 13,3 | −2,43 |
| Gemini-Montage v2 | 3,12 | 2,63 | 12,3 | 10,9 | 0,56 | 12,8 | −2,65 |
| ElevenLabs Robert Ranger | 4,33 | 2,93 | 12,2 | 7,7 | 0,35 | 15,4 | −2,58 |

Hinweis: Der Abstand hängt vom Ausschnitt ab (Gemini-Montage auf 100 s: 1,12, auf diesen 57 s: 3,12); nur gleiche Textteile vergleichen.
