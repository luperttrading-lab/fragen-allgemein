# Bett 200 × 200 mit Verkleidung und verdecktem Beamer

Vorentwurf vom 10.11.2026 für das Massivholzbett von XXXLutz (Art.-Nr. 800001553254, 200 × 200 cm) und den Beamer
Panasonic PT-VMZ51S (5.200 lm, WUXGA, Laser).

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
- **Bildlage per Lens-Shift:** Linse auf +420 mm. Mit Lens-Shift h = 0,30 (zulässig 0,056–0,50 laut Datenblatt)
  liegt die Bildunterkante auf 800 mm, damit Füße und Decke auch im Liegen nichts verdecken. Eine Trapezkorrektur
  ist nicht nötig.
- **Zwangslüftung:** Zuluft von unten durch ein Bodengitter. Abluft durch einen eigenen Kanal mit zwei 120-mm-Lüftern,
  seitlich hinaus und weg vom Strahl. Panasonic verlangt beim Einbau in engen Räumen eine Lüftung (Anleitung S. 21).
- **Schieber:** Alu-Verbundplatte in U-Führungen, bewegt von einem 12-V-Linearantrieb mit 200 mm Hub. Eine
  Master-Slave-Steckdosenleiste öffnet den Schieber automatisch, sobald der Beamer Strom zieht. Mit geschlossenem
  Schieber zu projizieren wäre eine Brandgefahr (Anleitung S. 13).

## Annahmen, vor dem Zuschnitt messen

Die Produktbilder bei XXXLutz sind als KI-generiert gekennzeichnet, die Maße des Betts waren nicht abrufbar.
Folgende Werte sind deshalb angenommen:

- Rahmen außen 2060 × 2060, Höhe 250, Lattenrost auf 230, Matratze 220
- Wandabstand Bank–Wand 2500, Raumhöhe 2500

Quellen: Panasonic Spec File PT-VMZ51S (Stand 04/2023) und Operating Instructions PT-VMZ71/61/51/51S/41. Die PDFs
liegen nicht im Repo.
