"""Formatprobe: dieselbe Stelle (Werkzeuge + Berechtigungen) als
V1 Peter allein und V2 Peter + Hörspiel-Einwürfe (Modell, Harness).
Aufruf: python3 hoerprobe_format.py <zielordner>  (ohne ELEVENLABS_API_KEY: nur Zeichen zählen)"""
import json, os, sys, urllib.request
STIMMEN = {'PETER': 'AMJfLTmTy3vPtjSvrGqZ',   # Peter Hartlapp – Tiefe Podcaststimme (Erzähler)
           'MODELL': 'dCnu06FiOZma2KVNUoPZ',  # Mila – jung, meinungsstark (das eifrige Modell)
           'HARNESS': 'zKHQdbB8oaQ7roNTiDTK'} # Laura – scharf, sachlich (der strenge Harness)
V1 = [('PETER', 'Wie drückt ein Modell, das nur Text schreiben kann, einen Knopf? Gar nicht. Es schreibt einen Wunsch in einem festen Format auf, etwa: Lies die Datei mit den Notizen. Der Harness erkennt das, prüft, ob es erlaubt ist, und drückt den Knopf. Für das Modell wirkt das wie Zauberei: Kurz darauf liegt das Ergebnis auf dem Schreibtisch. Und wenn das Modell etwas Gefährliches will, etwa eine Datenbank löschen? Dann sagt der Harness Nein, oder er fragt erst dich. Das Modell darf alles vorschlagen. Ausführen tut nur der Harness.')]
V2 = [('PETER', 'Wie drückt ein Modell, das nur Text schreiben kann, einen Knopf? Gar nicht. Es schreibt einen Wunsch auf.'),
      ('MODELL', 'Ich möchte die Datei mit den Notizen lesen.'),
      ('HARNESS', 'Erlaubt. Hier ist sie.'),
      ('PETER', 'Für das Modell wirkt das wie Zauberei: Kurz darauf liegt das Ergebnis auf dem Schreibtisch. Spannend wird es, wenn das Modell etwas Gefährliches will.'),
      ('MODELL', 'Ich lösche jetzt die alte Datenbank. Die stört nur.'),
      ('HARNESS', 'Abgelehnt. Das muss erst der Mensch freigeben.'),
      ('PETER', 'Das Modell darf alles vorschlagen. Ausführen tut nur der Harness.')]
def dialog(zeilen, datei):
    body = {'model_id': 'eleven_v4', 'inputs': [{'text': t, 'voice_id': STIMMEN[s]} for s, t in zeilen]}
    req = urllib.request.Request('https://api.elevenlabs.io/v1/text-to-dialogue?output_format=mp3_44100_128',
        data=json.dumps(body).encode(), method='POST',
        headers={'xi-api-key': os.environ['ELEVENLABS_API_KEY'], 'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=300) as r:
        open(datei, 'wb').write(r.read())
if __name__ == '__main__':
    for n, z in (('v1', V1), ('v2', V2)):
        print(n, sum(len(t) for _, t in z), 'Zeichen')
    if 'ELEVENLABS_API_KEY' in os.environ:
        for n, z in (('v1', V1), ('v2', V2)):
            dialog(z, os.path.join(sys.argv[1], f'format_{n}.mp3')); print(n, 'ok')
