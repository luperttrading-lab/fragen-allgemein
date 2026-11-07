# Harness Engineering – Drehbuch, Entwurf 3 (07.11.2026)

**Ziel:** 5 Minuten für Leute, die Claude im Chat kennen, aber nicht wissen, was Claude Code anders macht.
Danach sollen sie wissen: was ein Harness ist, **wo** er bei Claude Code steckt, und **was sie selbst** daran einstellen.

**Neu gegenüber Entwurf 2:** ohne den Composio-Test, die Statistik und die Kosten (kamen aus dem fremden Video).
Neu sind die Szenen „Wo steckt der Harness?“ und „Was musst du tun?“, außerdem bei jedem Baustein, wie er in Claude Code
heißt. Fakten nach der Claude-Code-Dokumentation (Quellen unten).

Sprecher: **PETER** allein (Variante A). Variante B: dieselben Szenen, in Szene 5 und 7 je ein Funk-Einwurf von
MODELL (Mila) und HARNESS (Helmut, Funkfilter), wie bisher.

## Szene 1 – Chat oder Claude Code? (Bild: links Chat-Antwort, rechts Terminal „✓ umbenannt“, darunter „gleiches Modell“)

PETER: Frag Claude im Chat, wie man eine Datei umbenennt, und du bekommst eine Anleitung. Sag dasselbe in Claude Code, und kurz darauf ist die Datei umbenannt. Dahinter steckt dasselbe Modell. Den Unterschied macht ein Programm drumherum: der Harness. Wörtlich heißt das Geschirr, das, womit man ein Pferd vor den Wagen spannt. In fünf Minuten weißt du, was so ein Harness macht, wo er steckt und wie du ihn selbst einstellst.

## Szene 2 – Pilot ohne Flugzeug (Bild: Pilot auf leerem Rollfeld, dann im Cockpit)

PETER: Ein Sprachmodell kann allein erstaunlich wenig. Es sagt das nächste Wort voraus, dann das nächste, und so weiter. Es sieht deine Dateien nicht, es vergisst nach jeder Sitzung alles, und es kann nichts ausführen. Es ist wie ein Pilot ohne Flugzeug: Er weiß genau, wie Fliegen geht, und steht trotzdem auf dem Rollfeld. Der Harness ist das Flugzeug drumherum.

## Szene 3 – Wo steckt der Harness? (Bild: links Rechenzentrum „Modell“, rechts Laptop „Claude Code“, dazwischen nur Text-Pfeile; dann der Chat als kleinere Hülle)

PETER: Und wo steckt dieser Harness? Bei Claude Code ist er das Programm selbst. Anthropic schreibt in der Anleitung sinngemäß: Claude Code ist die Schicht um das Modell. Sie stellt die Werkzeuge bereit und bestimmt, was das Modell zu sehen bekommt. Das Modell läuft im Rechenzentrum des Anbieters. Claude Code läuft bei dir: im Terminal, in der Desktop-App oder auf einem Rechner in der Cloud. Zwischen beiden geht nur Text hin und her. Das Modell schreibt, was getan werden soll. Claude Code tut es, dort, wo deine Dateien liegen. Und der Chat? Auch der hat so eine Schicht, nur eine kleinere: mit Websuche und den Dateien, die du hochlädst, aber ohne direkten Zugriff auf deinen Projektordner.

## Szene 4 – 1 · Was das Modell vor Augen hat (Bild: Schreibtisch, der volläuft; Notizdatei „CLAUDE.md“)

PETER: Der Harness hat vier Teile. Erstens: das, was das Modell vor Augen hat. Bevor du etwas tippst, legt Claude Code schon Unterlagen hin: Anweisungen von Anthropic, welcher Ordner gerade offen ist, und deine Notizdatei mit deinen Regeln. Sie heißt Claude Punkt M D. Dann füllt sich der Schreibtisch, mit jeder Nachricht und jeder gelesenen Datei. Wird er zu voll, fasst Claude Code alles zusammen und räumt den Rest ab. Dabei gehen Details verloren. Deshalb gehört alles Wichtige in diese Notizdatei, nicht nur in den Chat.

## Szene 5 – 2 · Werkzeuge (Bild: Modell schreibt Wunsch, Harness drückt den Knopf; Werkzeugliste)

PETER: Zweitens: Werkzeuge. Das Modell kann keinen Knopf drücken. Es schreibt einen Wunsch in einem festen Format auf, etwa: Lies die Datei mit den Notizen. Claude Code erkennt das und führt es aus. Für das Modell wirkt das wie Zauberei: Kurz darauf liegt das Ergebnis auf dem Schreibtisch. Eingebaut sind Werkzeuge zum Lesen, Schreiben, Suchen und für Befehle im Terminal. Weitere schließt du über einen Steckerstandard namens MCP an, zum Beispiel für den Kalender oder eine Datenbank.

*Variante B ersetzt die Mitte:* PETER: … Es schreibt einen Wunsch auf. Geben wir dem Modell mal eine Stimme. MODELL: Ich möchte die Datei mit den Notizen lesen. PETER: Und der Harness antwortet wie der Tower im Funk. HARNESS: Harness an Modell: erlaubt. Hier ist die Datei. PETER: Für das Modell wirkt das wie Zauberei …

## Szene 6 – 3 · Prüfung (Bild: Schüler korrigiert sich selbst; Testliste mit drei roten Kreuzen)

PETER: Drittens: die Prüfung. Ein Modell, das Programmcode schreibt, kann nur nachlesen, ob er gut aussieht. Ob er wirklich läuft, weiß es nicht. Das ist wie ein Schüler, der seine Klassenarbeit selbst korrigiert. Da gibt es selten eine Fünf. Deshalb lässt der Harness echte Tests laufen. Steht da „drei Tests fehlgeschlagen“, weiß das Modell: noch nicht fertig. In Claude Code kannst du das mit sogenannten Hooks festlegen: Regeln, die nach jeder Änderung von selbst die Tests starten.

## Szene 7 – 4 · Berechtigungen (Bild: Tower; drei Modi; Sandbox)

PETER: Viertens: Wer passt auf, dass nichts kaputtgeht? Claude Code prüft jeden Befehl, bevor er läuft. Wie der Tower, der jede Startfreigabe einzeln gibt. Wie streng, stellst du selbst ein: Soll Claude bei jeder Änderung fragen? Darf es Dateien ohne Nachfrage ändern? Oder soll es erst nur einen Plan machen? Und wer ganz sicher gehen will, schaltet die Sandbox ein: Dann laufen Befehle in einem abgeschotteten Bereich.

*Variante B, nach „Startfreigabe einzeln gibt.“:* MODELL: Ich lösche jetzt die alte Datenbank. Die stört nur. HARNESS: Harness an Modell: abgelehnt. Das muss erst der Mensch freigeben. PETER: Wie streng, stellst du selbst ein: …

## Szene 8 – Die Schleife (Bild: Kreis mit vier Schritten)

PETER: So spielt alles zusammen, in einer Schleife: Unterlagen hinlegen, das Modell entscheidet, Claude Code prüft und führt aus, das Ergebnis kommt zurück auf den Tisch. Und wieder von vorn, oft dutzende Male, bis die Aufgabe erledigt ist. Das Modell entscheidet also, was als Nächstes passiert. Alles andere macht der Harness.

## Szene 9 – Was musst du tun? (Bild: vier Karten zum Abhaken; Fußnote „Claude Code: ab Pro-Abo“)

PETER: Und was musst du tun, um den Harness zu benutzen? Nichts extra. Wer Claude Code öffnet, im Terminal oder im Code-Bereich der Desktop-App, benutzt ihn schon. Aber du kannst ihn einstellen, und genau das meint Harness Engineering. Erstens: eine Notizdatei mit deinen Regeln. Der Befehl Slash init legt dir eine an. Zweitens: festlegen, was Claude ohne Nachfrage darf. Drittens: die Werkzeuge anschließen, die du brauchst. Und viertens: Prüfungen von selbst laufen lassen. Dein Prompt sagt, was du willst. Der Harness bestimmt, was Claude dafür tun kann.

## Szene 10 – Schluss (Bild: Merksatz)

PETER: Merk dir: Das Modell denkt, der Harness handelt. Und wenn Claude das nächste Mal etwas vergisst oder Unsinn baut, liegt es vielleicht gar nicht am Modell, sondern an seiner Umgebung.

---

## Quellen (Claude-Code-Dokumentation, geprüft 07.11.2026)

- Harness-Begriff: „Claude Code is the layer around the model that provides the tools and manages the context the model
  sees. This surrounding layer is what the term agentic harness refers to.“
  [How Claude Code works](https://code.claude.com/docs/en/how-claude-code-works.md)
- Wo es läuft: lokal (Standard, „Your machine“), Cloud (von Anthropic betriebene VMs), Remote Control; Terminal,
  Desktop-App, IDE, Web. Ebenda.
- Kontext: CLAUDE.md und Auto-Memory beim Start; automatische Zusammenfassung nahe am Limit, „detailed instructions from
  early in the conversation may be lost“. [Memory](https://code.claude.com/docs/en/memory.md), How Claude Code works.
- Werkzeuge: Read, Edit, Write, Glob, Grep, Bash, WebSearch, WebFetch …
  [Agent loop](https://code.claude.com/docs/en/agent-sdk/agent-loop.md)
- Modi: Manual (fragt), Accept edits, Plan, Auto (mit Sicherheitsprüfung im Hintergrund).
  [Permission modes](https://code.claude.com/docs/en/permission-modes.md)
- Sandbox: standardmäßig aus, isoliert Terminal-Befehle. [Sandboxing](https://code.claude.com/docs/en/sandboxing.md)
- Hooks: „user-defined shell commands … at specific points in its lifecycle“.
  [Hooks guide](https://code.claude.com/docs/en/hooks-guide.md)
- Einstieg: „New to Claude Code? Start with CLAUDE.md“; `/init` legt eine an.
  [Extend Claude Code](https://code.claude.com/docs/en/features-overview.md)
- Abo: Claude Code „requires a Pro, Max, Ultra, Team, or Enterprise subscription“.
  [Desktop quickstart](https://code.claude.com/docs/en/desktop-quickstart.md)
- Chat: eigener Systemprompt, Werkzeuge wie Websuche, Code-Ausführung, Dateien, Connectors.
  [System prompts](https://platform.claude.com/docs/en/release-notes/system-prompts/overview).
  „Auch der Chat hat so eine Schicht“ ist unsere Deutung; Anthropic nennt den Chat nicht Harness.
