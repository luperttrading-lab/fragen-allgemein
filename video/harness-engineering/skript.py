"""Sprechtexte der zwei Testvideos, Drehbuch Entwurf 3 (07.11.2026): ohne Composio-Test, mit „Wo steckt der Harness?“
und „Was musst du tun?“; Fakten nach der Claude-Code-Dokumentation (Quellen in drehbuch.md).

A: Peter erzählt allein.
B: wie A, aber Szene 5 (Werkzeuge) und 7 (Berechtigungen) mit Funk-Einwurf: Modell (Mila) und Harness (Helmut, Funkfilter).

Marker ‹name› vor einem Wort setzen einen Zeitpunkt für die Bildeinblendung (film.html). Sie werden vor dem Senden
an ElevenLabs entfernt. Gesprochen „Claude Punkt M D“ und „Slash init“, im Bild CLAUDE.md und /init.
"""
import re

STIMMEN = {'PETER': 'AMJfLTmTy3vPtjSvrGqZ',    # Peter Hartlapp – Tiefe Podcaststimme (Erzähler)
           'MODELL': 'dCnu06FiOZma2KVNUoPZ',   # Mila – jung, meinungsstark
           'HARNESS': 'Cqbq4nsuUe1we6J45miU'}  # Helmut – Deep Authority News, bekommt Funkfilter

P = 'PETER'

S1 = [(P, 'Frag Claude im ‹chat›Chat, wie man eine Datei umbenennt, und du bekommst eine Anleitung. Sag dasselbe in '
          '‹code›Claude Code, und kurz darauf ‹fertig›ist die Datei umbenannt. Dahinter steckt ‹gleich›dasselbe Modell. '
          'Den Unterschied macht ein Programm drumherum: der ‹harness›Harness. Wörtlich heißt das ‹pferd›Geschirr, das, '
          'womit man ein Pferd vor den Wagen spannt. In fünf Minuten weißt du, ‹was›was so ein Harness macht, ‹wo›wo er '
          'steckt und ‹wie›wie du ihn selbst einstellst.')]

S2 = [(P, 'Ein Sprachmodell kann allein ‹wenig›erstaunlich wenig. Es sagt das ‹wort›nächste Wort voraus, dann das '
          'nächste, und so weiter. Es ‹sieht›sieht deine Dateien nicht, es ‹vergisst›vergisst nach jeder Sitzung alles, '
          'und es ‹kann›kann nichts ausführen. Es ist wie ein ‹pilot›Pilot ohne Flugzeug: Er weiß genau, wie Fliegen geht, '
          'und steht trotzdem auf dem Rollfeld. Der Harness ist das ‹flugzeug›Flugzeug drumherum.')]

S3 = [(P, 'Und ‹titel›wo steckt dieser Harness? Bei Claude Code ist er ‹programm›das Programm selbst. Anthropic schreibt '
          'in der Anleitung sinngemäß: ‹zitat›Claude Code ist die Schicht um das Modell. Sie stellt die Werkzeuge bereit '
          'und bestimmt, was das Modell zu sehen bekommt. Das Modell läuft im ‹rz›Rechenzentrum des Anbieters. Claude Code '
          'läuft ‹bei›bei dir: im ‹terminal›Terminal, in der ‹app›Desktop-App oder auf einem ‹cloud›Rechner in der Cloud. '
          'Zwischen beiden geht ‹text›nur Text hin und her. Das Modell schreibt, ‹was›was getan werden soll. Claude Code '
          '‹tut›tut es, dort, wo deine Dateien liegen. Und ‹chat›der Chat? Auch der hat so eine Schicht, nur eine '
          '‹klein›kleinere: mit Websuche und den Dateien, die du hochlädst, aber ‹ohne›ohne direkten Zugriff auf deinen '
          'Projektordner.')]

S4 = [(P, 'Der Harness hat ‹vier›vier Teile. Erstens: das, was das Modell ‹titel›vor Augen hat. Bevor du etwas tippst, '
          'legt Claude Code schon Unterlagen hin: ‹b1›Anweisungen von Anthropic, ‹b2›welcher Ordner gerade offen ist, und '
          'deine ‹b3›Notizdatei mit deinen Regeln. Sie heißt ‹claudemd›Claude Punkt M D. Dann füllt sich der Schreibtisch, '
          'mit ‹voll›jeder Nachricht und jeder gelesenen Datei. Wird er zu voll, ‹zusammen›fasst Claude Code alles '
          'zusammen und räumt den Rest ab. Dabei ‹verlust›gehen Details verloren. Deshalb gehört alles Wichtige ‹datei›in '
          'diese Notizdatei, nicht nur in den Chat.')]

S5_SCHLUSS = ('Für das Modell wirkt das wie Zauberei: Kurz darauf ‹ergebnis›liegt das Ergebnis auf dem Schreibtisch. '
              'Eingebaut sind ‹liste›Werkzeuge zum Lesen, Schreiben, Suchen und für Befehle im Terminal. Weitere schließt '
              'du über einen ‹mcp›Steckerstandard namens MCP an, zum Beispiel für den Kalender oder eine Datenbank.')
S5_A = [(P, 'Zweitens: ‹titel›Werkzeuge. Das Modell kann keinen Knopf drücken. Es schreibt einen ‹wunsch›Wunsch in einem '
            'festen Format auf, etwa: Lies die Datei mit den Notizen. Claude Code ‹erkennt›erkennt das und führt es aus. '
            + S5_SCHLUSS)]
S5_B = [(P, 'Zweitens: ‹titel›Werkzeuge. Das Modell kann keinen Knopf drücken. Es schreibt einen Wunsch auf. Geben wir '
            'dem Modell mal eine Stimme.'),
        ('MODELL', '‹wunsch›Ich möchte die Datei mit den Notizen lesen.'),
        (P, 'Und der Harness antwortet wie der Tower im Funk.'),
        ('HARNESS', '‹erkennt›Harness an Modell: erlaubt. Hier ist die Datei.'),
        (P, S5_SCHLUSS)]

S6 = [(P, 'Drittens: die ‹titel›Prüfung. Ein Modell, das Programmcode schreibt, kann nur nachlesen, ob er gut aussieht. '
          'Ob er wirklich läuft, weiß es nicht. Das ist wie ein ‹schueler›Schüler, der seine Klassenarbeit selbst '
          'korrigiert. Da gibt es selten eine Fünf. Deshalb lässt der Harness ‹tests›echte Tests laufen. Steht da '
          '‹rot›„drei Tests fehlgeschlagen“, weiß das Modell: noch nicht fertig. In Claude Code kannst du das mit '
          'sogenannten ‹hooks›Hooks festlegen: Regeln, die nach jeder Änderung von selbst die Tests starten.')]

S7_ANFANG = ('Viertens: ‹titel›Wer passt auf, dass nichts kaputtgeht? Claude Code prüft jeden Befehl, bevor er läuft. '
             'Wie der ‹tower›Tower, der jede Startfreigabe einzeln gibt.')
S7_SCHLUSS = ('Wie streng, stellst du selbst ein: Soll Claude ‹m1›bei jeder Änderung fragen? Darf es ‹m2›Dateien ohne '
              'Nachfrage ändern? Oder soll es ‹m3›erst nur einen Plan machen? Und wer ganz sicher gehen will, schaltet die '
              '‹sandbox›Sandbox ein: Dann laufen Befehle in einem abgeschotteten Bereich.')
S7_A = [(P, S7_ANFANG + ' ' + S7_SCHLUSS)]
S7_B = [(P, S7_ANFANG),
        ('MODELL', '‹db›Ich lösche jetzt die alte Datenbank. Die stört nur.'),
        ('HARNESS', '‹abgelehnt›Harness an Modell: abgelehnt. Das muss erst der Mensch freigeben.'),
        (P, S7_SCHLUSS)]

S8 = [(P, 'So spielt alles zusammen, in einer ‹titel›Schleife: ‹l1›Unterlagen hinlegen, ‹l2›das Modell entscheidet, '
          '‹l3›Claude Code prüft und führt aus, ‹l4›das Ergebnis kommt zurück auf den Tisch. Und ‹wieder›wieder von vorn, '
          'oft dutzende Male, bis die Aufgabe erledigt ist. Das Modell ‹entscheidet›entscheidet also, was als Nächstes '
          'passiert. Alles andere macht der Harness.')]

S9 = [(P, 'Und ‹titel›was musst du tun, um den Harness zu benutzen? ‹nichts›Nichts extra. Wer Claude Code öffnet, im '
          'Terminal oder im Code-Bereich der Desktop-App, benutzt ihn schon. Aber du kannst ihn ‹einstellen›einstellen, und '
          'genau das meint Harness Engineering. Erstens: eine ‹e1›Notizdatei mit deinen Regeln. Der Befehl ‹init›Slash '
          'init legt dir eine an. Zweitens: festlegen, ‹e2›was Claude ohne Nachfrage darf. Drittens: die ‹e3›Werkzeuge '
          'anschließen, die du brauchst. Und viertens: ‹e4›Prüfungen von selbst laufen lassen. Dein Prompt sagt, '
          '‹prompt›was du willst. Der Harness bestimmt, ‹harness›was Claude dafür tun kann.')]

S10 = [(P, 'Merk dir: ‹denkt›Das Modell denkt, ‹handelt›der Harness handelt. Und wenn Claude das nächste Mal '
           '‹unsinn›etwas vergisst oder Unsinn baut, liegt es vielleicht gar nicht am Modell, sondern an seiner Umgebung.')]

VARIANTEN = {
    'A': [('s1', S1), ('s2', S2), ('s3', S3), ('s4', S4), ('s5', S5_A), ('s6', S6), ('s7', S7_A), ('s8', S8),
          ('s9', S9), ('s10', S10)],
    'B': [('s1', S1), ('s2', S2), ('s3', S3), ('s4', S4), ('s5', S5_B), ('s6', S6), ('s7', S7_B), ('s8', S8),
          ('s9', S9), ('s10', S10)],
}

MARKER = re.compile(r'‹(\w+)›')


def zerlege(zeilen):
    """Entfernt Marker. Liefert (zeilen_ohne_marker, cues) mit cues = {name: zeichenposition im Gesamttext}."""
    sauber, cues, pos = [], {}, 0
    for sprecher, text in zeilen:
        t, versatz = '', 0
        for m in MARKER.finditer(text):
            t += text[versatz:m.start()]
            cues[m.group(1)] = pos + len(t)
            versatz = m.end()
        t += text[versatz:]
        sauber.append((sprecher, t)); pos += len(t)
    return sauber, cues


if __name__ == '__main__':
    for v, szenen in VARIANTEN.items():
        n = sum(len(t) for _, z in szenen for _, t in zerlege(z)[0])
        print(v, n, 'Zeichen', {s: sum(len(t) for _, t in zerlege(z)[0]) for s, z in szenen})
