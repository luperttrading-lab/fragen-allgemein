# Bett 200 × 200 mit Verkleidung und verdecktem Beamer

Vorentwurf vom 10.11.2026 für das Massivholzbett (200 × 200 cm, Rahmenhöhe 22 cm gemessen). Gezeichnet ist der
Panasonic PT-VMZ51S (5.200 lm, WUXGA, Laser). Die Bank passt auch für den vorhandenen PT-VX500 (379 × 305 mm,
mit Steckern etwa 420 mm tief, gemessen).

- `Bauzeichnungen_Bett_Beamer.pdf`: vier A3-Blätter
  1. Raum: Draufsicht und Längsschnitt mit Strahlengang und Sichtlinien, Tabelle Bildgröße je Wandabstand
  2. Beamer-Fußbank: Ansicht, Draufsicht, Schnitt A–A, Stirnseite mit Lüftern
  3. Details: Schieber mit Linearantrieb, Fensterschnitt, Bettverkleidung, Blockschaltbild der Steuerung
  4. Zuschnittliste, Einkaufsliste, Berechnungen (Bildlage, Wärme, Helligkeit, Erschütterung), Inbetriebnahme
- `zeichnungen.py`: erzeugt das PDF. Die Annahmen stehen oben als Parameter (`A_WAND`, `RAUM_H`, `BETT_*`,
  `MATR_H`, `BILD_B`, `BILD_UK`). Nach dem Messen anpassen und `python3 zeichnungen.py` ausführen. Das Skript prüft,
  ob Zoom und Lens-Shift für das gewünschte Bild reichen, und bricht sonst ab.

## Konzept

Der Beamer sitzt nicht im Bett, sondern in einer frei stehenden Bank am Fußende. Optisch gehört sie zur Verkleidung,
mechanisch ist sie durch eine 10-mm-Fuge vom Bett getrennt.

- **Entkopplung:** 1 Pixel entspricht bei 2 m Bildbreite 0,41 mrad Kippung. Schon 0,5 mm Durchbiegung im Bettrahmen
  verschiebt das Bild um etwa 3,5 Pixel.
- **Bildlage per Lens-Shift:** Linse auf +380 mm (Bank 500 hoch). Mit Lens-Shift h = 0,34 (zulässig 0,056–0,50 laut Datenblatt)
  liegt die Bildunterkante auf 800 mm, damit Füße und Decke auch im Liegen nichts verdecken. Eine Trapezkorrektur
  ist nicht nötig.
- **Zwangslüftung:** Zuluft von unten durch ein Bodengitter (400 × 180). Abluft durch einen eigenen Kanal mit zwei
  140-mm-Lüftern (≈ 150 m³/h), seitlich hinaus und weg vom Strahl. Ausgelegt ist sie für den heißeren VX500
  (365 W) plus etwa 40 W Geräte. Panasonic verlangt beim Einbau in engen Räumen eine Lüftung (Anleitung S. 21).
- **Schieber:** Alu-Verbundplatte in U-Führungen, bewegt von einem 12-V-Linearantrieb mit 200 mm Hub. Eine
  Master-Slave-Steckdosenleiste öffnet den Schieber automatisch, sobald der Beamer Strom zieht. Mit geschlossenem
  Schieber zu projizieren wäre eine Brandgefahr (Anleitung S. 13).

- **Technikfach und Kabel:** Apple TV, Mac mini, Switch-Dock (Zugang über Klappdeckel), HDMI-Umschalter 3→1 und
  LAN-Switch sitzen in der Bank. Von der Wanddose kommen nur ein Strom- und ein LAN-Kabel, in einem Kanal unter der
  Bank. Der Ton geht vom Audio-Out des Beamers zum Marshall (AUX).

## Annahmen, vor dem Zuschnitt messen

Die Produktbilder bei XXXLutz sind als KI-generiert gekennzeichnet, die Maße des Betts waren nicht abrufbar.
Folgende Werte sind deshalb angenommen:

- Rahmen außen 2060 × 2060 (die Höhe von 220 ist gemessen), Matratze 200
- Wandabstand Bank–Wand 2500, Raumhöhe 2500

Quellen: Panasonic Spec File PT-VMZ51S (Stand 04/2023) und Operating Instructions PT-VMZ71/61/51/51S/41. Die PDFs
liegen nicht im Repo.
