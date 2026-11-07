# Harness Engineering – Drehbuch, Entwurf 1 (07.11.2026)

Eigenes Skript für zwei Sprecher, angelehnt an den Inhalt von
[Alex Sprogis: „Hör auf Agents zu prompten. Starte mit Harness Engineering!“](https://youtu.be/SU0EyB45x6Q)
(03.11.2026, 13:50 min), mit eigenen Bildern (Pilot, Schreibtisch, Prognosemodell) und eigenem Statistik-Teil.
Zahlenquelle: [Composio, „Best AI agent harnesses“](https://composio.dev/content/best-ai-agent-harnesses) (04.08.2026).

Rollen: **MARA** = Statistikerin, fragt kritisch nach. **BEN** = Entwickler, erklärt knapp.
Kein NotebookLM-Muster: kein gegenseitiges „Genau!“ und „Wow“, keine Echo-Sätze; jede Zeile bringt etwas Neues.

## Szene 1 – Einstieg (Bild: Balken, alle acht Harnesses)

BEN: Gleiches Sprachmodell, gleiche Werkzeuge, gleiche fünfundzwanzig Aufgaben. Nur die Software drumherum ist eine andere. Und plötzlich löst das eine System zweiundzwanzig Aufgaben, das andere nur siebzehn.

MARA: Claude Code liegt mit neunzehn im Mittelfeld, ist aber am langsamsten und am teuersten. So steht es in einem Test der Firma Composio vom August.

BEN: Diese Software drumherum heißt Harness. Heute geht es darum, was ein Harness ist, woraus er besteht und warum er so viel ausmacht.

MARA: Und am Ende prüfen wir, ob die Zahlen halten, was sie versprechen. Kleiner Hinweis vorab: nur zum Teil.

## Szene 2 – Das Modell allein (Bild: Pilot auf dem Rollfeld, ohne Flugzeug)

MARA: Fangen wir vorne an. Was kann ein Sprachmodell eigentlich allein?

BEN: Eine einzige Sache: das nächste Stück Text vorhersagen. Es kann dir erklären, wie man eine Datei anlegt. Anlegen kann es sie nicht. Es sieht dein Projekt nicht, es vergisst nach jeder Sitzung alles, und ob sein Code läuft, weiß es auch nicht.

MARA: Also ein Pilot ohne Flugzeug. Weiß genau, wie Fliegen geht, und steht trotzdem auf dem Rollfeld.

BEN: Und der Harness ist das Flugzeug: Instrumente, Steuerung, Checklisten und der Funk zum Tower. Erst Modell und Harness zusammen ergeben einen Agenten.

## Szene 3 – Vier Bausteine (Bild: vier Kacheln)

MARA: Woraus besteht so ein Harness?

BEN: Aus vier Bausteinen: Kontext, Werkzeuge, Prüfung und Berechtigungen.

## Szene 4 – Kontext (Bild: Schreibtisch, der volläuft)

MARA: Kontext heißt: Was weiß das Modell gerade?

BEN: Bevor du die erste Nachricht schreibst, hat der Harness schon einiges eingefügt: den Systemprompt des Anbieters, Angaben zu deinem Rechner und deinem Ordner, und deine eigenen Regeln. Bei Claude Code stehen die in der Datei CLAUDE.md, bei vielen anderen Werkzeugen heißt sie AGENTS.md.

MARA: Da steht dann zum Beispiel: Wir arbeiten mit Python, und nach jeder Änderung laufen die Tests.

BEN: Einmal geschrieben, und jede neue Sitzung startet mit diesem Wissen. Dazu kommt bei vielen Harnesses ein Gedächtnis, in dem sich der Agent selbst Notizen macht.

MARA: Und während der Arbeit?

BEN: Da wird es eng, denn das Kontextfenster ist begrenzt. Stell dir einen Schreibtisch vor. Jede Nachricht, jede gelesene Datei, jedes Ergebnis landet als Blatt darauf. Je voller er wird, desto schlechter findet das Modell das Wichtige. Das nennt man Context Rot.

MARA: Und wenn der Tisch voll ist?

BEN: Dann fasst der Harness alles auf wenigen Seiten zusammen und räumt den Rest ab. Das heißt Compaction. Dabei gehen Details verloren.

MARA: Deshalb gehört Wichtiges in Dateien und nicht nur in den Chat. Dateien kann der Agent jederzeit neu lesen.

## Szene 5 – Werkzeuge und MCP (Bild: Textzeile „Tool-Call“, Harness drückt den Knopf)

MARA: Baustein zwei, Werkzeuge. Wie drückt ein Modell, das nur Text schreibt, einen Knopf?

BEN: Gar nicht. Es schreibt Text in einem festen Format, sinngemäß: Rufe das Werkzeug „Datei lesen“ auf, für die Datei README. Das ist ein Tool-Call. Der Harness erkennt das Format, führt das Werkzeug wirklich aus und gibt das Ergebnis zurück.

MARA: Und das passiert in einer normalen Sitzung dutzende Male, ohne dass man es merkt.

BEN: Über MCP, das Model Context Protocol, lassen sich außerdem fremde Systeme anschließen: Notion, der Kalender, Datenbanken. Für das Modell ist das am Ende nur eine längere Werkzeugliste.

## Szene 6 – Prüfung (Bild: Tests, rot und grün)

MARA: Baustein drei, Prüfung. Das ist mein Lieblingsteil.

BEN: Ein Modell kann seinen Code nur lesen. Ob er läuft, weiß es nicht. Fragst du es, sagt es meistens: sieht gut aus.

MARA: Wie ein Prognosemodell, das man nur an den Daten prüft, mit denen es gebaut wurde. Es sieht immer gut aus.

BEN: Deshalb gibt der Harness echte Prüfwerkzeuge: Unit-Tests, einen Linter, der typische Fehler findet, oder einen Browser, der die App wirklich anklickt. Steht da „drei Tests fehlgeschlagen“, weiß das Modell: Ich bin noch nicht fertig.

MARA: Und wenn das Modell vergisst zu testen?

BEN: Dann sorgt ein guter Harness trotzdem dafür, zum Beispiel mit Hooks. Das sind kleine Regeln, die nach jeder Änderung automatisch die Tests starten.

## Szene 7 – Berechtigungen (Bild: Tower, Freigabe)

MARA: Und Baustein vier schützt dich.

BEN: Die Berechtigungen. Ein Agent, der Befehle ausführen darf, kann auch Daten löschen. Deshalb prüft der Harness jeden Tool-Call, bevor er läuft: erlaubt, erst nachfragen oder verboten.

MARA: Wie der Tower, der jede Startfreigabe erteilt.

BEN: Dazu kommt die Sandbox. Der Agent arbeitet in einem abgeschotteten Bereich und kann draußen nichts kaputt machen.

## Szene 8 – Der Agent-Loop (Bild: Kreis mit vier Schritten)

MARA: Wie spielt das alles zusammen?

BEN: In einer Schleife. Erstens: Der Harness sammelt Aufgabe und Kontext. Zweitens: Das Modell wählt eine Aktion und schreibt einen Tool-Call. Drittens: Der Harness prüft die Rechte und führt aus. Viertens: Das Ergebnis geht zurück ans Modell. Und dann von vorn, bis das Ziel erreicht ist.

MARA: Von vier Schritten macht das Modell also nur einen.

BEN: Und deshalb schneidet dasselbe Modell in verschiedenen Harnesses so unterschiedlich ab. Andere Werkzeuge, andere Beschreibungen, ein anderer Systemprompt, andere Prüfungen.

## Szene 9 – Prompt, Context, Harness Engineering (Bild: drei Stufen)

MARA: Man hört ständig Prompt Engineering, Context Engineering, Harness Engineering. Was ist der Unterschied?

BEN: Das ist eher eine Entwicklung. Ende zweitausendzweiundzwanzig, mit ChatGPT, ging es um den Prompt: Wie formuliere ich die Frage? Dann kamen Werkzeuge und eigene Daten dazu, und die Frage wurde: Was gehört ins Kontextfenster und was nicht? Das ist Context Engineering.

MARA: Und heute laufen Agenten stundenlang.

BEN: Genau da reicht guter Kontext nicht mehr. Der Tisch läuft voll, nach der Zusammenfassung fehlen Details, und am Ende hält sich der Agent für fertig, obwohl die Hälfte fehlt. Also gestaltet man den Ablauf: eine Liste aller geplanten Funktionen, und der Agent arbeitet pro Runde genau eine ab, testet sie und speichert den Stand. Jede Runde startet mit frischem Kontext.

MARA: Das ist Harness Engineering. Du gestaltest nicht mehr nur die Frage, sondern die ganze Umgebung und den Ablauf.

## Szene 10 – Statistik-Check (Bild: acht Balken, Hinweis „alle mit Kimi K3“)

MARA: Und jetzt zu den Zahlen vom Anfang. Da muss ich als Statistikerin einhaken.

BEN: Bitte.

MARA: Erstens: Jedes System hatte genau einen Versuch pro Aufgabe. Eine Aufgabe sind vier Prozentpunkte. Zwischen zweiundzwanzig und siebzehn liegen fünf Aufgaben. Wären beide Systeme gleich gut, käme so ein Abstand selbst in der günstigsten Rechnung in sechs von hundert Fällen durch Zufall zustande. Das reicht nicht als Beleg.

MARA: Zweitens: Verglichen werden der Beste und der Schlechteste von acht. Wer die Extreme herauspickt, überschätzt den Unterschied fast immer.

MARA: Drittens: Alle acht liefen mit demselben Modell, Kimi K3 von Moonshot. Claude Code ist für Claude gebaut, Codex für die Modelle von OpenAI. Beide liefen hier mit einem fremden Modell.

BEN: Und Codex war mit siebzehn das Schlusslicht.

MARA: Eben. Außerdem waren die Aufgaben Büroabläufe in Gmail, Kalender und Slack, nicht Programmieren.

BEN: Was bleibt dann übrig?

MARA: Die Kosten. Claude Code hat pro gelöster Aufgabe knapp zwei Dollar gekostet, das nächstteure System zweiundsiebzig Cent. Fast dreimal so viel. Ein so großer Abstand ist kaum Zufall.

BEN: Also: Der Harness zählt. Aber welcher der beste ist, zeigt dieser Test nicht.

## Szene 11 – Schluss (Bild: Merksätze)

MARA: Zum Mitnehmen: Das Modell denkt, der Harness handelt.

BEN: Und wenn du selbst mit einem Agenten arbeitest: Schreib deine Regeln in eine Datei, lass Tests automatisch laufen und fang große Aufgaben mit einer Liste an, nicht mit einem endlosen Chat.

MARA: Und trau keiner Rangliste mit fünfundzwanzig Aufgaben und einem Versuch.
