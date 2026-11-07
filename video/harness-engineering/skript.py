"""Sprechtexte der zwei Testvideos (07.11.2026), Grundlage Drehbuch 2.1.

A: Peter erzählt allein.
B: wie A, aber Szene 4 (Werkzeuge) und 6 (Berechtigungen) mit Funk-Einwurf: Modell (Mila) und Harness (Helmut, Funkfilter).

Marker ‹name› vor einem Wort setzen einen Zeitpunkt für die Bildeinblendung (film.html). Sie werden vor dem Senden
an ElevenLabs entfernt. TTS-Schreibweisen: „Kimi K drei“ (gesprochen), im Bild „Kimi K3“.
"""
import re

STIMMEN = {'PETER': 'AMJfLTmTy3vPtjSvrGqZ',    # Peter Hartlapp – Tiefe Podcaststimme (Erzähler)
           'MODELL': 'dCnu06FiOZma2KVNUoPZ',   # Mila – jung, meinungsstark
           'HARNESS': 'Cqbq4nsuUe1we6J45miU'}  # Helmut – Deep Authority News, bekommt Funkfilter

P = 'PETER'

S1 = [(P, 'Stell dir vor, du steckst ‹modell›dasselbe KI-Modell in ‹acht›acht verschiedene Programme und gibst allen '
          'dieselben fünfundzwanzig Aufgaben. Das ‹best›beste löst zweiundzwanzig, das ‹worst›schwächste nur siebzehn. '
          'Und ‹cc›Claude Code, eines der bekanntesten, landet im Mittelfeld. Dafür ist es das ‹teuer›langsamste und '
          'mit Abstand das teuerste. Das Programm um das Modell herum heißt ‹harness›Harness. Wörtlich: das '
          '‹pferd›Geschirr, mit dem man ein Pferd vor den Wagen spannt. In fünf Minuten weißt du, was so ein Harness '
          'macht. Und am Ende zeige ich dir, ‹zweifel›warum du diesem Test trotzdem nicht trauen solltest.')]

S2 = [(P, 'Was kann so ein ‹frage›Sprachmodell eigentlich allein? Erstaunlich wenig. Es sagt das ‹wort›nächste Wort '
          'vorher, dann das nächste, und so weiter. Es kann dir ‹erklaeren›erklären, wie man eine Datei umbenennt. '
          '‹nicht›Umbenennen kann es sie nicht. Es ist wie ein ‹pilot›Pilot ohne Flugzeug: Er weiß genau, wie Fliegen '
          'geht, und steht trotzdem auf dem Rollfeld. Der Harness ist das ‹flugzeug›Flugzeug drumherum. Und das hat '
          '‹vier›vier Teile.')]

S3 = [(P, 'Erstens: das, was das Modell ‹titel›vor Augen hat. Bevor du überhaupt etwas tippst, legt der Harness schon '
          'Unterlagen hin: die ‹b1›Anweisungen des Herstellers, ‹b2›welcher Ordner gerade offen ist, und eine '
          '‹b3›Notizdatei mit deinen eigenen Regeln. Dann füllt sich der Schreibtisch, mit ‹voll›jeder Nachricht und '
          'jeder gelesenen Datei. Irgendwann ist er so voll, dass das Modell das ‹uebersieht›Wichtige übersieht. Dann '
          '‹zusammen›fasst der Harness alles auf wenigen Seiten zusammen und wirft den Rest weg. Und dabei ‹verlust›gehen '
          'Details verloren. Deshalb gehört alles Wichtige ‹datei›in eine Datei, nicht nur in den Chat.')]

S4_A = [(P, 'Zweitens: ‹titel›Werkzeuge. Wie drückt ein Modell, das nur Text schreiben kann, einen Knopf? ‹gar›Gar '
            'nicht. Es schreibt einen ‹wunsch›Wunsch in einem festen Format auf, etwa: Lies die Datei mit den Notizen. '
            'Der Harness ‹erkennt›erkennt das und drückt den Knopf. Für das Modell wirkt das wie Zauberei: Kurz darauf '
            '‹ergebnis›liegt das Ergebnis auf dem Schreibtisch. Weitere Werkzeuge kommen über einen ‹mcp›Steckerstandard '
            'namens MCP dazu, zum Beispiel für den Kalender oder eine Datenbank. Für das Modell ist das einfach eine '
            '‹liste›längere Werkzeugliste.')]

S4_B = [(P, 'Zweitens: ‹titel›Werkzeuge. Wie drückt ein Modell, das nur Text schreiben kann, einen Knopf? ‹gar›Gar '
            'nicht. Es schreibt einen Wunsch auf. Geben wir dem Modell mal eine Stimme.'),
        ('MODELL', '‹wunsch›Ich möchte die Datei mit den Notizen lesen.'),
        (P, 'Und der Harness antwortet wie der Tower im Funk.'),
        ('HARNESS', '‹erkennt›Harness an Modell: erlaubt. Hier ist die Datei.'),
        (P, 'Für das Modell wirkt das wie Zauberei: Kurz darauf ‹ergebnis›liegt das Ergebnis auf dem Schreibtisch. '
            'Weitere Werkzeuge kommen über einen ‹mcp›Steckerstandard namens MCP dazu, zum Beispiel für den Kalender '
            'oder eine Datenbank. Für das Modell ist das einfach eine ‹liste›längere Werkzeugliste.')]

S5 = [(P, 'Drittens: die ‹titel›Prüfung. Ein Modell, das Programmcode schreibt, kann nur nachlesen, ob er gut aussieht. '
          'Ob er wirklich läuft, weiß es nicht. Das ist wie ein ‹schueler›Schüler, der seine Klassenarbeit selbst '
          'korrigiert. Da gibt es selten eine Fünf. Deshalb lässt der Harness ‹tests›echte Tests laufen, und zwar von '
          'selbst. Steht da ‹rot›„drei Tests fehlgeschlagen“, weiß das Modell: noch nicht fertig. Es muss also nicht '
          'glauben, dass alles klappt. ‹gruen›Der Harness prüft es nach.')]

S6_A = [(P, 'Viertens: ‹titel›Wer passt auf, dass nichts kaputtgeht? Der Harness prüft jeden Befehl, bevor er läuft: '
            '‹ok›erlaubt, ‹frage›erst nachfragen oder ‹nein›verboten. Wie der ‹tower›Tower, der die Startfreigabe gibt. '
            'Will das Modell zum Beispiel eine ‹db›Datenbank löschen, sagt der Harness ‹abgelehnt›Nein, oder er fragt '
            'erst dich. Und wer ganz sicher gehen will, lässt den Agenten in einem ‹sandbox›abgeschotteten Bereich '
            'arbeiten, einer Sandbox.')]

S6_B = [(P, 'Viertens: ‹titel›Wer passt auf, dass nichts kaputtgeht? Der Harness prüft jeden Befehl, bevor er läuft: '
            '‹ok›erlaubt, ‹frage›erst nachfragen oder ‹nein›verboten. Wie der ‹tower›Tower, der die Startfreigabe gibt.'),
        ('MODELL', '‹db›Ich lösche jetzt die alte Datenbank. Die stört nur.'),
        ('HARNESS', '‹abgelehnt›Harness an Modell: abgelehnt. Das muss erst der Mensch freigeben.'),
        (P, 'Und wer ganz sicher gehen will, lässt den Agenten in einem ‹sandbox›abgeschotteten Bereich arbeiten, '
            'einer Sandbox.')]

S7 = [(P, 'Und wie spielt das zusammen? Als ‹titel›Schleife. ‹l1›Unterlagen hinlegen, ‹l2›das Modell entscheidet, '
          '‹l3›der Harness prüft und führt aus, ‹l4›das Ergebnis kommt zurück auf den Tisch. Und ‹wieder›wieder von '
          'vorn, oft dutzende Male, bis die Aufgabe erledigt ist. Oder bis zu viel schiefgeht. Dann ‹mensch›holt der '
          'Harness dich dazu. Das Modell ‹entscheidet›entscheidet also nur, was als Nächstes passiert. Den Rest erledigt '
          'der Harness. Und ‹deshalb›deshalb schneidet dasselbe Modell in verschiedenen Programmen so unterschiedlich ab.')]

S8 = [(P, 'Und jetzt zum ‹titel›Test vom Anfang. Jedes Programm hatte nur ‹einer›einen Versuch pro Aufgabe. Zwischen '
          'dem besten und dem schwächsten liegen ‹fuenf›fünf Aufgaben. Nehmen wir an, beide wären gleich gut. Dann ist '
          'jede Aufgabe, die nur einer von beiden schafft, wie ein ‹muenze›Münzwurf. Fünfmal dieselbe Seite passiert in '
          '‹sechzehn›einem von sechzehn Fällen. Und das ist noch die günstigste Rechnung. Als ‹beweis›Beweis reicht das '
          'nicht. Dazu kommt: Alle acht liefen mit demselben fremden Modell, ‹kimi›Kimi K drei. Claude Code ist aber '
          '‹claude›für Claude gebaut. Da sitzt also ein ‹fremd›fremder Pilot in einem Cockpit, das für jemand anderen '
          'eingestellt ist. Was übrig bleibt, sind die ‹kosten›Kosten. Claude Code hat pro gelöster Aufgabe ‹zwei›knapp '
          'zwei Dollar gekostet, das nächstteure Programm ‹cent›zweiundsiebzig Cent. Fast ‹drei›dreimal so viel. So ein '
          'Abstand ist kaum Zufall.')]

S9 = [(P, 'Merk dir: ‹denkt›Das Modell denkt, ‹handelt›der Harness handelt. Und wenn dein KI-Assistent das nächste Mal '
          '‹unsinn›Unsinn baut, liegt es vielleicht gar nicht am Modell. Und ‹rangliste›trau keiner Rangliste mit einem '
          'Versuch pro Aufgabe.')]

VARIANTEN = {
    'A': [('s1', S1), ('s2', S2), ('s3', S3), ('s4', S4_A), ('s5', S5), ('s6', S6_A), ('s7', S7), ('s8', S8), ('s9', S9)],
    'B': [('s1', S1), ('s2', S2), ('s3', S3), ('s4', S4_B), ('s5', S5), ('s6', S6_B), ('s7', S7), ('s8', S8), ('s9', S9)],
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
