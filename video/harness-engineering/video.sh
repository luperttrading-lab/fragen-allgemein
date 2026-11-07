#!/bin/bash
# Rendert Variante $1 (A oder B): Bilder aus film.html, Ton aus ton.py; Ausgabe in $2
set -e
cd "$(dirname "$0")"
V=$1; O=$2
env -u ELEVENLABS_API_KEY python3 ton.py $V $O
node render.js $O/zeitplan_$V.json $O/film_$V 25
ffmpeg -v error -y -f concat -safe 0 -i $O/film_$V.liste.txt -i $O/ton_$V.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart $O/harness_${V}_1080p.mp4
ffmpeg -v error -y -i $O/harness_${V}_1080p.mp4 -vf "scale=1280:720:flags=lanczos" -c:v libx264 -preset slow -crf 26 -tune stillimage -pix_fmt yuv420p -c:a aac -b:a 128k -movflags +faststart $O/harness_${V}_720p.mp4
ls -la $O/harness_${V}_*.mp4
