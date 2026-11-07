#!/bin/bash
# Illustrationen für das Harness-Video (GPT Image 2 über RouteLLM), Stil wie pilot_rollfeld.png
cd "$(dirname "$0")"
STIL="Warm flat editorial illustration with subtle paper grain, calm muted palette on a warm off-white background (#F7F3EA), accents in deep teal (#0A8F80) and burnt orange (#C2410C), soft shadows, clean simple shapes, generous empty space, wide 3:2 composition. Same illustration style as the reference image. Absolutely no text, no letters, no numbers, no logos, no signs."
B="python3 ../../../stile/assets/bild.py --model gpt_image2 --ratio '' --size 1536x1024 --ref pilot_rollfeld.png"
erz(){ [ -s "$1.png" ] || eval $B --out "$1.png" --prompt "\"$2 $STIL\"" > "$1.log" 2>&1; }
erz pferd "A sturdy draft horse in side view wearing a leather harness with collar and straps, hitched to a simple wooden cart; the harness visibly connects the horse to the cart." &
erz cockpit "The pilot from the reference image sits confidently in the cockpit of an airliner, hands on the controls, instrument panel with abstract glowing shapes (no readable numbers), bright sky through the windshield." &
erz cockpit_fremd "A different pilot, a woman with short hair in the same teal uniform, sits in an airliner cockpit whose seat and controls are clearly adjusted for someone else: seat pushed far back, she stretches awkwardly to reach the controls, puzzled expression. Gently humorous." &
erz schueler "A teenage student at a school desk grading his own exam paper with a red pen, drawing a big tick and looking very pleased with himself; the paper only shows abstract grey lines. Gently humorous." &
erz tower "An airport control tower at golden hour, an air traffic controller with headset visible behind the tower windows, a small airliner waiting on the taxiway below." &
wait
