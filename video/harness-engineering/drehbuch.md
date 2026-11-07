# Harness Engineering – Drehbuch, Entwurf 2 (07.11.2026)

**Ziel:** 5 Minuten, kurzweilig, für Leute, die ChatGPT oder Claude nutzen, aber nicht programmieren. Wer zuschaut,
soll danach wissen, was ein Harness ist, und den Begriff zuordnen können. Test, was wir zusammen produzieren können.

Inhalt angelehnt an [Alex Sprogis: „Hör auf Agents zu prompten. Starte mit Harness Engineering!“](https://youtu.be/SU0EyB45x6Q)
(03.11.2026), eigene Formulierungen und Bilder, eigener Statistik-Teil. Zahlenquelle:
[Composio, „Best AI agent harnesses“](https://composio.dev/content/best-ai-agent-harnesses) (04.08.2026).

Rollen: **MARA** = Statistikerin, fragt nach. **BEN** = Entwickler, erklärt knapp.
Kein NotebookLM-Muster: kein gegenseitiges „Genau!“ und „Wow“, keine Echo-Sätze; jede Zeile bringt etwas Neues.
Aufbau: offene Frage am Anfang (Test mit 22 zu 17), Auflösung am Ende (Münzwurf).

Gegenüber Entwurf 1 gestrichen: Szene „Prompt, Context, Harness Engineering“ (nur noch ein Satz am Schluss),
Fachwörter Linter, Unit-Test, Hook, Compaction, Context Rot, AGENTS.md.

## Szene 1 – Einstieg (Bild: acht Balken, Claude Code markiert)

BEN: Stell dir vor, du steckst dasselbe KI-Modell in acht verschiedene Programme und gibst allen dieselben fünfundzwanzig Aufgaben. Das beste löst zweiundzwanzig, das schwächste nur siebzehn.

MARA: Und Claude Code, eines der bekanntesten, landet im Mittelfeld. Dafür ist es das langsamste und mit Abstand das teuerste.

BEN: Das Programm um das Modell herum heißt Harness. Wörtlich: das Geschirr, mit dem man ein Pferd vor den Wagen spannt.

MARA: In fünf Minuten weißt du, was so ein Harness macht. Und am Ende zeige ich dir, warum du diesem Test trotzdem nicht trauen solltest.

## Szene 2 – Pilot ohne Flugzeug (Bild: Pilot auf leerem Rollfeld)

MARA: Was kann so ein Sprachmodell eigentlich allein?

BEN: Erstaunlich wenig. Es sagt das nächste Wort vorher, dann das nächste, und so weiter. Es kann dir erklären, wie man eine Datei umbenennt. Umbenennen kann es sie nicht.

MARA: Wie ein Pilot ohne Flugzeug. Weiß genau, wie Fliegen geht, und steht trotzdem auf dem Rollfeld.

BEN: Der Harness ist das Flugzeug drumherum. Und das hat vier Teile.

## Szene 3 – Was das Modell vor Augen hat (Bild: Schreibtisch, der volläuft)

BEN: Erstens: das, was das Modell vor Augen hat. Bevor du überhaupt etwas tippst, legt der Harness schon Unterlagen hin: die Anweisungen des Herstellers, welcher Ordner gerade offen ist, und eine Notizdatei mit deinen eigenen Regeln.

MARA: Und dann füllt sich der Schreibtisch.

BEN: Mit jeder Nachricht und jeder gelesenen Datei. Irgendwann ist er so voll, dass das Modell das Wichtige übersieht. Dann fasst der Harness alles auf wenigen Seiten zusammen und wirft den Rest weg.

MARA: Und genau dabei gehen Details verloren. Deshalb gehört alles Wichtige in eine Datei, nicht nur in den Chat.

## Szene 4 – Werkzeuge (Bild: Textzeile wird zum Knopfdruck)

MARA: Zweitens: Werkzeuge. Wie drückt ein Modell, das nur Text schreibt, einen Knopf?

BEN: Gar nicht. Es schreibt einen Satz in einem festen Format, etwa: Benutze das Werkzeug „Datei lesen“ für die Notizdatei. Der Harness erkennt das, drückt den Knopf und legt das Ergebnis zurück auf den Schreibtisch.

MARA: Und wenn man mehr Werkzeuge will?

BEN: Dann kommen sie über einen Steckerstandard namens MCP dazu, zum Beispiel für den Kalender oder eine Datenbank. Für das Modell ist das einfach eine längere Werkzeugliste.

## Szene 5 – Prüfung (Bild: Klassenarbeit, rot korrigiert)

MARA: Drittens, mein Lieblingsteil: die Prüfung.

BEN: Ein Modell, das Programmcode schreibt, kann nur nachlesen, ob er gut aussieht. Ob er wirklich läuft, weiß es nicht.

MARA: Wie ein Schüler, der seine Klassenarbeit selbst korrigiert. Da gibt es selten eine Fünf.

BEN: Deshalb lässt der Harness echte Tests laufen. Steht da „drei Tests fehlgeschlagen“, weiß das Modell: noch nicht fertig. Und ein guter Harness startet die Tests von selbst, auch wenn das Modell es vergisst.

## Szene 6 – Berechtigungen (Bild: Tower, Startfreigabe)

MARA: Viertens: Wer passt auf, dass nichts kaputtgeht?

BEN: Der Harness prüft jeden Befehl, bevor er läuft: erlaubt, erst nachfragen oder verboten. Wie der Tower, der die Startfreigabe gibt. Und wer ganz sicher gehen will, lässt den Agenten in einem abgeschotteten Bereich arbeiten, einer Sandbox.

## Szene 7 – Die Schleife (Bild: Kreis mit vier Schritten)

MARA: Und wie spielt das zusammen?

BEN: Als Schleife. Unterlagen hinlegen, das Modell entscheidet, der Harness prüft und führt aus, das Ergebnis kommt zurück auf den Tisch. Und wieder von vorn, oft dutzende Male, bis die Aufgabe erledigt ist.

MARA: Das Modell entscheidet also nur, was als Nächstes passiert. Den Rest erledigt der Harness. Und deshalb schneidet dasselbe Modell in verschiedenen Programmen so unterschiedlich ab.

## Szene 8 – Statistik-Check (Bild: fünf Münzen, dann acht Balken mit „alle mit Kimi K3“)

MARA: Und jetzt zum Test vom Anfang. Jedes Programm hatte nur einen Versuch pro Aufgabe.

BEN: Und zwischen dem besten und dem schwächsten liegen fünf Aufgaben.

MARA: Nehmen wir an, beide wären gleich gut. Dann ist jede Aufgabe, die nur einer von beiden schafft, wie ein Münzwurf. Fünfmal dieselbe Seite passiert in einem von sechzehn Fällen. Und das ist noch die günstigste Rechnung. Als Beweis reicht das nicht.

BEN: Und was ist mit Claude Code?

MARA: Alle acht liefen mit demselben fremden Modell, Kimi K3. Claude Code ist aber für Claude gebaut. Da sitzt also ein fremder Pilot in einem Cockpit, das für jemand anderen eingestellt ist.

BEN: Bleibt dann überhaupt etwas übrig?

MARA: Die Kosten. Claude Code hat pro gelöster Aufgabe knapp zwei Dollar gekostet, das nächstteure Programm zweiundsiebzig Cent. So ein Abstand ist kaum Zufall.

## Szene 9 – Schluss (Bild: Merksatz)

BEN: Merk dir: Das Modell denkt, der Harness handelt. Deshalb reden inzwischen alle nicht mehr nur über gute Prompts, sondern über den Harness.

MARA: Und trau keiner Rangliste mit einem Versuch pro Aufgabe.
