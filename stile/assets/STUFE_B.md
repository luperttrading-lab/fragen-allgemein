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
