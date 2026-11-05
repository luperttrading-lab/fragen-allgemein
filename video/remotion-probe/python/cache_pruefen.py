# Prüft ohne Ausführung von regel.py, ob alle Sprechtexte im TTS-Cache liegen (sonst kostet ein Lauf ElevenLabs-Zeichen).
import ast, hashlib, json, os, sys
REPO = sys.argv[1]
src = open(os.path.join(REPO, 'themen/mathe-einmaleins/regel.py'), encoding='utf-8').read()
ns = {'BRUECKE': 'Klingt nach Zauberei? Ist es nicht.', 'SPRUCH': 'Das ist kein Hexenwerk.', 'DENKPAUSE': 6.0, 'dict': dict}
for node in ast.parse(src).body:
    if isinstance(node, ast.Assign) and getattr(node.targets[0], 'id', '') == 'SZENEN':
        szenen = eval(compile(ast.Expression(node.value), 'SZENEN', 'eval'), {'__builtins__': {}}, ns)
cache = os.path.join(REPO, 'themen/mathe-einmaleins/tts_cache')
cfg = {'voice_id': 'NBqeXKdZHweef6y0B67V', 'model': 'eleven_v4'}
ok = True
for sc in szenen:
    sig = f"el|{cfg['voice_id']}|{cfg['model']}|{json.dumps(None, sort_keys=True)}|{sc['text']}"
    h = hashlib.sha1(sig.encode()).hexdigest()[:16]
    da = os.path.exists(os.path.join(cache, h + '.json'))
    ok &= da
    print(f"{sc['id']:11s} {h} {'im Cache' if da else 'FEHLT'}  {len(sc['text'])} Zeichen")
print('ALLE IM CACHE' if ok else 'NICHT ALLE IM CACHE')
json.dump(szenen, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'szenen.json'), 'w'), ensure_ascii=False, indent=1)
