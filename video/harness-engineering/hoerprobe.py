"""Hörprobe Szene 1 mit drei Stimmenpaaren über die ElevenLabs Text-to-Dialogue-API.
Aufruf: python3 hoerprobe.py <zielordner> [paar ...]   (ohne ELEVENLABS_API_KEY: nur Zeichen zählen)"""
import json, os, re, sys, urllib.request, urllib.error
HIER = os.path.dirname(os.path.abspath(__file__))
PAARE = {  # Mara (w), Ben (m): (Name, voice_id, public_owner_id oder None)
    'A': (('Susi', 'v3V1d2rk6528UrLKRuy8', 'e7fea8016e07cbf918ca753255d7085b26536539ab23d1c18100164e2a920dfc'),
          ('Jan', '4u3R5vsV3x092eJ1kFuh', None)),
    'B': (('Laura', 'zKHQdbB8oaQ7roNTiDTK', 'c11ce606b8d6aa00677cf6c90265a06f645cb140c3641e82d4cc3c3d7d14f669'),
          ('Stephan', 'IWm8DnJ4NGjFI7QAM5lM', None)),
    'C': (('Mila', 'dCnu06FiOZma2KVNUoPZ', 'dfad8b2f4835158499a4fc8aa6b1570d022c5196a553d7fca7788446fb3fa4a6'),
          ('Peter', 'AMJfLTmTy3vPtjSvrGqZ', None)),
}
def szene1():
    t = open(os.path.join(HIER, 'drehbuch.md')).read().split('## Szene 2')[0]
    return [(m.group(1), m.group(2).strip()) for m in re.finditer(r'^(MARA|BEN): (.+)$', t, re.M)]
def api(pfad, daten=None, roh=False):
    req = urllib.request.Request('https://api.elevenlabs.io' + pfad, method='POST' if daten is not None else 'GET',
        data=json.dumps(daten).encode() if daten is not None else None,
        headers={'xi-api-key': os.environ['ELEVENLABS_API_KEY'], 'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=300) as r:
        b = r.read()
    return b if roh else json.loads(b)
if __name__ == '__main__':
    ziel = sys.argv[1]; wahl = sys.argv[2:] or list(PAARE)
    zeilen = szene1(); n = sum(len(t) for _, t in zeilen)
    print('Szene 1:', len(zeilen), 'Zeilen,', n, 'Zeichen je Paar,', n * len(wahl), 'gesamt')
    if 'ELEVENLABS_API_KEY' not in os.environ: sys.exit(0)
    for p in wahl:
        mara, ben = PAARE[p]
        # Bibliotheksstimmen gehen direkt über ihre voice_id; ins Konto holen ist nicht nötig
        # (der Schlüssel hat auch kein voices_write).
        stimme = {'MARA': mara[1], 'BEN': ben[1]}
        body = {'model_id': 'eleven_v4', 'inputs': [{'text': t, 'voice_id': stimme[s]} for s, t in zeilen]}
        try:
            mp3 = api('/v1/text-to-dialogue?output_format=mp3_44100_128', body, roh=True)
        except urllib.error.HTTPError as e:
            print(p, 'Fehler', e.code, e.read()[:400]); continue
        open(os.path.join(ziel, f'paar_{p}.mp3'), 'wb').write(mp3); print(p, 'ok', len(mp3), 'Bytes')
