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
