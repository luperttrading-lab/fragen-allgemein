# Erzeugt stile/out3/clay/KOSTEN.md aus den Bild-Logs (nichts wird geschätzt, was nicht im Log steht).
import json, pathlib, re
root = pathlib.Path(__file__).resolve().parents[2]
gen = root / "stile/out3/clay/gen"; verworfen = {p.name for p in (gen / "verworfen").glob("*.png")}
verwendet = {"bg_v1", "hero_v2", "figur_ratlos_v3", "figur_aktiv_v1", "ballons_v1", "umschlag_v1", "wecker_v1"}
zweck = {"bg": "Hintergrund (zerknittertes Papier)", "hero": "Hero: Gehirn mit Zahnrädern + Etikett", "figur_ratlos": "Figur ratlos (Bogenfenster)",
         "figur_aktiv": "Figur aktiviert (Blob)", "ballons": "Gehirn mit Luftballons", "umschlag": "Umschlag + Uhr (Paradox)",
         "wecker": "Wecker + Pfeilkreis (Deadline-Falle)", "pult": "Steuerpult (optional)"}
def de(x, nk=1):  # deutsche Zahlschreibweise: 13 839,6
    return f"{x:,.{nk}f}".replace(",", " ").replace(".", ",")
rows = []; summe = 0.0
for i, line in enumerate((gen / "bild_log.jsonl").read_text().splitlines(), 1):
    j = json.loads(line); name = pathlib.Path(j["dateien"][0]).stem; base = re.sub(r"_v\d+$", "", name)
    pts = j["compute_points_used"]; summe += pts
    status = "verwendet" if name in verwendet else ("verworfen" if name + ".png" in verworfen else "erzeugt, nicht verwendet")
    rows.append(f"| {i} | {zweck.get(base, base)} ({name}) | {j['model']} | {j['cfg'].get('resolution','–')}, {j['cfg'].get('aspect_ratio','–')} | "
                f"ja | {de(pts)} | {status} |")
# Referenzen: aus dem Aufruf bekannt (alle nano_banana_pro-Aufrufe hier liefen mit --ref), im Log nicht gespeichert → aus Aufrufhistorie
tests = 0.0; ntests = 0
for line in (root / "stile/out3/bild_log.jsonl").read_text().splitlines():
    tests += json.loads(line)["compute_points_used"]; ntests += 1
diag = 13837.2  # Diagnoseaufruf 18.10. ohne gespeicherte Datei (aus der Sitzungsausgabe, nicht im Log)
md = f"""# Kostenprotokoll Clay (Stufe B, Hybrid) – Stand {json.loads(line)['zeit'][:10]}

Alle Werte sind `usage.compute_points_used` aus der RouteLLM-Antwort (stile/out3/clay/gen/bild_log.jsonl). Referenzbilder: alle
Aufrufe liefen mit `--ref` (Original Clay.jpg; ab Szene 3 zusätzlich hero_v2.png; figur_ratlos_v3 zusätzlich figur_ratlos_v1.png).
Der Log speichert die Referenzen selbst nicht, nur die übrigen Parameter.

| Nr. | Zweck (Datei) | Modell | Auflösung, Seitenverhältnis | Referenzen | Punkte | Status |
|---|---|---|---|---|---|---|
""" + "\n".join(rows) + f"""

**Summe Clay: {de(summe)} Punkte bei {len(rows)} Aufrufen** (Ø {de(summe/len(rows),0)} je Bild).

## Umrechnung
- 1 000 Punkte = 1 Credit (Modellliste „rate“ 8 ↔ 8 000 Punkte bei recraft_svg; App zeigt Credits mit zwei Nachkommastellen). [Wahrscheinlich]
- Bisherige Annahme Listenpreis: 1 000 Punkte ≈ 1 US-Cent → Clay ≈ {de(summe/1000)} ct ≈ {de(summe/100000,2)} $. [Wahrscheinlich]
- Abo-Durchschnitt (Pro, 20 $ für 30 000 Credits laut Nutzer): 1 Credit ≈ 0,067 ct → Clay ≈ {de(summe/1000*0.0667)} ct. [Wahrscheinlich]

## Frühere Testaufrufe (getrennt, stile/out3/bild_log.jsonl)
- {ntests} gespeicherte Testbilder: {de(tests)} Punkte; plus 1 Diagnoseaufruf ohne Datei: {de(diag)} Punkte → {de(tests+diag)} Punkte.
- Gesamt Stufe B bis jetzt: {de(summe+tests+diag)} Punkte ≈ {de((summe+tests+diag)/1000,0)} Credits.

Fehlaufrufe (HTTP 400: seed, image_prompt, aspect_ratio bei recraft_svg, rewrite_prompt=false) lieferten keine usage-Angabe; ob sie
Punkte kosten, ist nicht belegt.
"""
(root / "stile/out3/clay/KOSTEN.md").write_text(md); print(md)
