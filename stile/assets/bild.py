#!/usr/bin/env python3
"""Bilderzeugung über die RouteLLM API (Abacus.AI / ChatLLM Teams), OpenAI-kompatibel.

Aufruf:
  python3 bild.py --prompt "…" --out bild.png [--model nano_banana_pro] [--ratio 1:1]
                  [--resolution 2K] [--seed 7] [--n 1] [--ref referenz.png …] [--rewrite]
  python3 bild.py --check          # nur Erreichbarkeit und Schlüssel prüfen

Der API-Schlüssel kommt aus der Umgebungsvariable ROUTELLM_API_KEY (ersatzweise ABACUS_API_KEY).
Er wird nie ausgegeben. Doku: https://abacus.ai/help/route-llm/chat-completions/image-analysis
"""
import argparse, base64, json, mimetypes, os, pathlib, sys, time, urllib.request, urllib.error

BASE = "https://routellm.abacus.ai/v1"


def key_var():
    """Name der Umgebungsvariable mit dem Schlüssel; bevorzugt feste Namen, sonst alles mit ABACUS/ROUTELLM im Namen."""
    for n in ("ROUTELLM_API_KEY", "ABACUS_API_KEY", "ABACUSAI_API_KEY"):
        if os.environ.get(n):
            return n
    for n in sorted(os.environ):
        if ("ABACUS" in n.upper() or "ROUTELLM" in n.upper()) and len(os.environ[n]) > 15:
            return n
    return None


def key():
    n = key_var()
    if not n:
        sys.exit("Kein API-Schlüssel gefunden: keine Umgebungsvariable mit ROUTELLM/ABACUS im Namen "
                 "(Secret in den Einstellungen der Umgebung „Abacus-API“ prüfen, Sitzung dort starten).")
    return os.environ[n]


def http(url, data=None, headers=None, timeout=180):
    req = urllib.request.Request(url, data=data, headers=headers or {}, method="POST" if data else "GET")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()


def data_url(path):
    mime = mimetypes.guess_type(path)[0] or "image/png"
    return f"data:{mime};base64," + base64.b64encode(pathlib.Path(path).read_bytes()).decode()


def check():
    st, body = http(BASE + "/models")
    print("GET /v1/models ->", st, "(Host erreichbar)" if st == 200 else "")
    n = key_var()
    if not n:
        print("Schlüssel: FEHLT (keine Variable mit ROUTELLM/ABACUS im Namen)"); return 1
    print("Schlüssel gefunden in Variable:", n, "(Wert wird nicht angezeigt)")
    k = os.environ[n]
    payload = json.dumps({"model": "route-llm", "messages": [{"role": "user", "content": "Antworte nur mit OK."}], "max_tokens": 5}).encode()
    st, body = http(BASE + "/chat/completions", payload, {"Authorization": f"Bearer {k}", "Content-Type": "application/json"}, timeout=60)
    print("Test-Textaufruf ->", st, body[:200].decode(errors="ignore") if st != 200 else "Schlüssel gültig")
    return 0 if st == 200 else 1


def generate(a):
    cfg = {"num_images": a.n, "rewrite_prompt": a.rewrite}
    if a.ratio: cfg["aspect_ratio"] = a.ratio
    if a.resolution: cfg["resolution"] = a.resolution
    if a.size: cfg["size"] = a.size
    if a.seed is not None: cfg["seed"] = a.seed
    if a.negative: cfg["negative_prompt"] = a.negative
    if a.ref: cfg["image_prompt"] = [data_url(p) for p in a.ref] if len(a.ref) > 1 else data_url(a.ref[0])
    payload = {"model": a.model, "modalities": ["image"], "messages": [{"role": "user", "content": a.prompt}], "image_config": cfg}
    t0 = time.time()
    st, body = http(BASE + "/chat/completions", json.dumps(payload).encode(),
                    {"Authorization": f"Bearer {key()}", "Content-Type": "application/json"})
    if st != 200:
        sys.exit(f"Fehler {st}: {body[:600].decode(errors='ignore')}")
    resp = json.loads(body)
    msg = resp["choices"][0]["message"]
    images = msg.get("images") or []
    if not images and isinstance(msg.get("content"), list):  # tolerant: Bild als Content-Part
        images = [p for p in msg["content"] if p.get("type") == "image_url"]
    if not images:
        sys.exit("Keine Bilder in der Antwort: " + json.dumps(resp)[:600])
    out = pathlib.Path(a.out); out.parent.mkdir(parents=True, exist_ok=True)
    saved = []
    for i, item in enumerate(images):
        url = item["image_url"]["url"]
        target = out if len(images) == 1 else out.with_name(f"{out.stem}_{i+1}{out.suffix}")
        if url.startswith("data:"):
            target.write_bytes(base64.b64decode(url.split(",", 1)[1]))
        else:
            st2, img = http(url, timeout=120)
            if st2 != 200: sys.exit(f"Download fehlgeschlagen ({st2}): {url[:120]}")
            target.write_bytes(img)
        saved.append(str(target))
    usage = resp.get("usage", {})
    log = {"zeit": time.strftime("%Y-%m-%d %H:%M:%S"), "model": a.model, "cfg": {k: v for k, v in cfg.items() if k != "image_prompt"},
           "prompt": a.prompt, "dateien": saved, "compute_points_used": usage.get("compute_points_used"), "dauer_s": round(time.time() - t0, 1)}
    with open(out.parent / "bild_log.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(log, ensure_ascii=False) + "\n")
    print(json.dumps(log, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--check", action="store_true")
    p.add_argument("--prompt"); p.add_argument("--out", default="bild.png")
    p.add_argument("--model", default="nano_banana_pro")
    p.add_argument("--ratio", default="1:1", help="z. B. 1:1, 9:16, 3:2; leer lassen mit ''")
    p.add_argument("--resolution", default=None, help="nano_banana_pro: 1K, 2K, 4K (4K kostet doppelt)")
    p.add_argument("--size", default=None, help="für gpt_image*/flux_pro/recraft, z. B. 1024x1536")
    p.add_argument("--seed", type=int, default=None); p.add_argument("--n", type=int, default=1)
    p.add_argument("--negative", default=None); p.add_argument("--ref", nargs="*", help="Referenzbilder (image_prompt)")
    p.add_argument("--rewrite", action="store_true", help="Prompt vom Dienst umschreiben lassen (Standard: aus, damit 'kein Text' hält)")
    a = p.parse_args()
    if a.check: sys.exit(check())
    if not a.prompt: p.error("--prompt fehlt")
    generate(a)
