# Stufe B: Bildmodell über ChatLLM (RouteLLM API) + Layout/Text in HTML

## Zugang
- Es gibt bereits eine Cloud-Umgebung **„Abacus-API“** (env_013iyfavpbLr8v6YFCeK2mXP, angelegt 05.09.2026) mit dem Schlüssel
  als Secret. Sitzungen für Stufe B müssen in DIESER Umgebung laufen; in „Standard“ ist der Schlüssel nicht sichtbar.
- `bild.py` findet den Schlüssel unter `ROUTELLM_API_KEY`, `ABACUS_API_KEY` oder jeder Variable mit ABACUS/ROUTELLM im Namen.
- Falls der Schlüssel neu erzeugt werden muss: in ChatLLM unten links „RouteLLM API“ (https://abacus.ai/app/route-llm-apis),
  dann in den Umgebungs-Einstellungen als Network secret hinterlegen, nie in den Chat posten.
- Netzwerk: `routellm.abacus.ai` ist aus der Standard-Umgebung erreichbar (geprüft 18.10.2026, HTTP 200); in „Abacus-API“ erneut prüfen.

## Prüfen
    python3 stile/assets/bild.py --check

## Erste Testbilder (je Stil eine Szene, 1:1, 1K, ohne Text)
    python3 bild.py --model nano_banana_pro --ratio 1:1 --resolution 1K --seed 1 \
      --prompt "…" --out out3/test_clay.png

## Fakten aus der Doku (abacus.ai/help/route-llm/chat-completions/image-analysis)
- Endpoint: POST https://routellm.abacus.ai/v1/chat/completions, `modalities: ["image"]`, Einstellungen in `image_config`.
- Bild-IDs u. a.: nano_banana_pro, nano_banana2, nano_banana, flux2_pro, flux_pro_ultra, gpt_image2, gpt_image25,
  ideogram45, recraft, recraft_svg (liefert SVG!), seedream5_pro, midjourney.
- `aspect_ratio` (1:1, 9:16, 3:2, …), `resolution` für Nano Banana (1K/2K/4K; 4K kostet doppelt), `seed`,
  `num_images` 1–4, `rewrite_prompt` (Standard an → wir setzen aus), `image_prompt` = Referenzbilder
  (nano_banana_pro max 4, nano_banana2 max 14, flux2_pro max 3).
- Antwort: `choices[0].message.images[].image_url.url` (HTTPS-URL), `usage.compute_points_used`.
- Kosten: Modellliste nennt „rate“ je Bild; Vergleich mit den Listenpreisen legt nahe: rate ≈ US-Cent je Bild
  (flux2_pro 3 ↔ „from $0.03“, recraft 4 ↔ $0.04, recraft_svg 8 ↔ $0.08). Danach: nano_banana_pro ≈ 13 ct,
  nano_banana2 ≈ 7 ct, nano_banana21 ≈ 3,4 ct, ideogram45 3–22 ct. [Wahrscheinlich, nicht bestätigt]
  ChatLLM-Abo: 20.000 Credits/Monat; wie Credits auf Cent abbilden, ist in der FAQ nicht erklärt.

## Pipeline-Plan
1. Je Stil: 1 Hero-Bild + 4–6 Szenen als Einzelbilder, PROMPT OHNE TEXT („no text, no letters, no labels“),
   definierter Hintergrund (Weiß/Beige/transparent nicht möglich → gleiche Farbe wie Seite), fester seed.
2. Stil-Konsistenz: erstes gutes Bild als `image_prompt`-Referenz für die weiteren Szenen desselben Stils.
3. Freistellen bei Bedarf (einfarbiger Hintergrund → Pillow/rembg), Einbau in das HTML-Layout, Text pixelgenau.
4. Für Flat-Stile (Professional, Instructional) alternativ `recraft_svg` testen: echte Vektoren, skalierbar.

## Befunde aus dem ersten Bildtest (18.10.2026, Umgebung „Abacus-API“, Schlüssel in ROUTELLM_API_KEY)
- `seed` wird abgelehnt (nano_banana_pro und recraft_svg): „Invalid image config param seed. Supported params are:
  aspect_ratio, image_size, model, num_images, quality, resolution, rewrite_prompt, size.“ → keine Reproduzierbarkeit über seed.
- `image_prompt` in `image_config` wird ebenfalls abgelehnt. Referenzbilder funktionieren als `image_url`-Teile
  (data-URL) im `content` der Nachricht; bild.py macht das jetzt so.
- `rewrite_prompt: false` → 400 „Could not generate an image prompt from the conversation“ (nano_banana_pro, mit und ohne
  resolution). Rewrite muss an bleiben; „no text, no letters, no labels“ im Prompt hat trotzdem bei 4/4 Bildern gehalten.
- recraft_svg: `aspect_ratio` wird abgelehnt („Supported values are: “ leer) → ohne Ratio aufrufen, Ergebnis 1024×1024,
  echte SVG (nur <path>, kein <text>), mit großem C2PA-Metadatenblock.
- Punkte je Bild: nano_banana_pro 1K ≈ 13 850, recraft_svg 8 000. 1 000 Compute-Punkte = 1 Credit (Modellliste „rate“ 8 ↔
  8 000 Punkte; Credits in der App haben wie Punkte/1000 zwei Nachkommastellen). Abo laut Nutzer: Pro 20 $/Monat mit
  30 000 Credits → 1 Credit ≈ 0,067 ct, nano_banana_pro ≈ 0,9 ct, gpt_image25 ≈ 0,05 ct je Bild im Abo-Durchschnitt.
  Listenpreis-Sicht (recraft_svg 8 Credits ↔ 0,08 $): 1 Credit ≈ 1 ct. Preis der Zusatzpakete unbekannt.
- abacus.ai (Doku-Seiten) ist aus der Umgebung „Abacus-API“ nicht erreichbar (Proxy 403); routellm.abacus.ai schon.
- Vergleich (gleicher Tag): nano_banana_pro 2K kostet dasselbe wie 1K (13 877,8 vs. 13 889,8 Punkte) und liefert echte
  2048×2048 px; gpt_image25 (size 1024x1024, Referenz als image_url akzeptiert) nur 687,5 Punkte je Bild.
  Ohne Referenzbild bleibt nano_banana_pro beim Knete-Motiv, trifft aber den warmen Rosa-Beige-Ton der Vorlage schlechter.

## Clay fertig (18.10.2026): stile/clay/b.html → stile/out3/clay/Clay_B.png (+ Clay_B_vergleich.jpg, KOSTEN.md)
- 17 Aufrufe nano_banana_pro 2K (238 133 Punkte ≈ 238 Credits), 7 Bilder verwendet, alle Varianten in out3/clay/gen (verworfen/).
- Freistellen: rembg (u2net) + Schattenbereinigung (stile/clay/freistellen.py); Schwellwert nur beim flachen Wecker.
- Stand: 2K kostet wie 1K; Referenzbilder stabilisieren Farbwelt und Material; „kein Text“ hielt bei 17/17.
