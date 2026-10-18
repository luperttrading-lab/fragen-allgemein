# Kostenprotokoll Clay (Stufe B, Hybrid) – Stand 2026-10-18

Alle Werte sind `usage.compute_points_used` aus der RouteLLM-Antwort (stile/out3/clay/gen/bild_log.jsonl). Referenzbilder: alle
Aufrufe liefen mit `--ref` (Original Clay.jpg; ab Szene 3 zusätzlich hero_v2.png; figur_ratlos_v3 zusätzlich figur_ratlos_v1.png).
Der Log speichert die Referenzen selbst nicht, nur die übrigen Parameter.

| Nr. | Zweck (Datei) | Modell | Auflösung, Seitenverhältnis | Referenzen | Punkte | Status |
|---|---|---|---|---|---|---|
| 1 | Hintergrund (zerknittertes Papier) (bg_v1) | nano_banana_pro | 2K, 9:16 | ja | 13 839,6 | verwendet |
| 2 | Hintergrund (zerknittertes Papier) (bg_v2) | nano_banana_pro | 2K, 9:16 | ja | 13 850,4 | verworfen |
| 3 | Hero: Gehirn mit Zahnrädern + Etikett (hero_v1) | nano_banana_pro | 2K, 1:1 | ja | 13 928,8 | verworfen |
| 4 | Hero: Gehirn mit Zahnrädern + Etikett (hero_v2) | nano_banana_pro | 2K, 1:1 | ja | 13 880,8 | verwendet |
| 5 | Figur ratlos (Bogenfenster) (figur_ratlos_v1) | nano_banana_pro | 2K, 3:4 | ja | 14 078,4 | verworfen |
| 6 | Figur ratlos (Bogenfenster) (figur_ratlos_v2) | nano_banana_pro | 2K, 3:4 | ja | 14 053,2 | verworfen |
| 7 | Figur aktiviert (Blob) (figur_aktiv_v1) | nano_banana_pro | 2K, 3:4 | ja | 14 028,2 | verwendet |
| 8 | Figur aktiviert (Blob) (figur_aktiv_v2) | nano_banana_pro | 2K, 3:4 | ja | 14 070,2 | verworfen |
| 9 | Gehirn mit Luftballons (ballons_v1) | nano_banana_pro | 2K, 1:1 | ja | 14 052,8 | verwendet |
| 10 | Gehirn mit Luftballons (ballons_v2) | nano_banana_pro | 2K, 1:1 | ja | 14 031,2 | verworfen |
| 11 | Umschlag + Uhr (Paradox) (umschlag_v1) | nano_banana_pro | 2K, 1:1 | ja | 14 081,0 | verwendet |
| 12 | Umschlag + Uhr (Paradox) (umschlag_v2) | nano_banana_pro | 2K, 1:1 | ja | 14 006,6 | verworfen |
| 13 | Wecker + Pfeilkreis (Deadline-Falle) (wecker_v1) | nano_banana_pro | 2K, 1:1 | ja | 14 041,8 | verwendet |
| 14 | Wecker + Pfeilkreis (Deadline-Falle) (wecker_v2) | nano_banana_pro | 2K, 1:1 | ja | 14 041,8 | verworfen |
| 15 | Steuerpult (optional) (pult_v1) | nano_banana_pro | 2K, 1:1 | ja | 13 995,4 | verworfen |
| 16 | Steuerpult (optional) (pult_v2) | nano_banana_pro | 2K, 1:1 | ja | 13 994,2 | erzeugt, nicht verwendet |
| 17 | Figur ratlos (Bogenfenster) (figur_ratlos_v3) | nano_banana_pro | 2K, 3:4 | ja | 14 158,2 | verwendet |

**Summe Clay: 238 132,6 Punkte bei 17 Aufrufen** (Ø 14 008 je Bild).

## Umrechnung
- 1 000 Punkte = 1 Credit (Modellliste „rate“ 8 ↔ 8 000 Punkte bei recraft_svg; App zeigt Credits mit zwei Nachkommastellen). [Wahrscheinlich]
- Bisherige Annahme Listenpreis: 1 000 Punkte ≈ 1 US-Cent → Clay ≈ 238,1 ct ≈ 2,38 $. [Wahrscheinlich]
- Abo-Durchschnitt (Pro, 20 $ für 30 000 Credits laut Nutzer): 1 Credit ≈ 0,067 ct → Clay ≈ 15,9 ct. [Wahrscheinlich]

## Frühere Testaufrufe (getrennt, stile/out3/bild_log.jsonl)
- 7 gespeicherte Testbilder: 77 967,3 Punkte; plus 1 Diagnoseaufruf ohne Datei: 13 837,2 Punkte → 91 804,5 Punkte.
- Gesamt Stufe B bis jetzt: 329 937,1 Punkte ≈ 330 Credits.

Fehlaufrufe (HTTP 400: seed, image_prompt, aspect_ratio bei recraft_svg, rewrite_prompt=false) lieferten keine usage-Angabe; ob sie
Punkte kosten, ist nicht belegt.
