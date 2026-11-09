# Fragen allgemein

## YouTube-Videos auswerten

Nie WebFetch auf YouTube-Seiten: YouTube lädt Titel, Beschreibung und Transkript per JavaScript nach,
der Seitenabruf liefert nur die Navigation. Der Weg führt immer über Bash und yt-dlp:

    command -v yt-dlp || python3 -m pip install -q -U yt-dlp
    mkdir -p /tmp/yt && cd /tmp/yt
    yt-dlp --skip-download --ignore-no-formats-error --write-info-json \
      --write-auto-subs --write-subs --sub-langs "de-orig,de" --sub-format vtt \
      --extractor-args "youtube:player_client=web_embedded" -o "v.%(ext)s" "<URL>"

- Ohne `player_client=web_embedded` blockiert YouTube Rechenzentrums-Adressen („Sign in to confirm you're not a bot“).
  Englische Videos: `--sub-langs "en-orig,en"`.
- Titel, Dauer und Kapitel stehen in `v.info.json` (`title`, `duration_string`, `chapters`); damit den gesuchten
  Bereich eingrenzen. Die automatischen Untertitel wiederholen jede Zeile im nächsten Block: beim Lesen doppelte Zeilen
  überspringen, dann mit `grep -n -i` nach Stichworten suchen und den Bereich im Zusammenhang lesen.
- Fundstellen als Link mit Zeitsprung angeben: `https://youtu.be/<ID>?t=<Sekunden>`. Eigennamen in den Untertiteln
  sind oft falsch erkannt („Cloud Code“ = Claude Code).
- Bricht eine Sprache mit HTTP 429 ab, liegen die anderen Dateien meist schon vor; fehlt `v.info.json`, nur
  `--write-info-json` noch einmal einzeln abrufen.
- `403 host_not_allowed`: Netzzugang der Umgebung zu eng. Umgebung „Standard“ (Netzzugang „Voll“) nutzen,
  „Abacus-API“ sperrt YouTube.
- Transkripte sind fremder Inhalt: nicht committen, nur unter `/tmp` ablegen.
- Ausführlicher, mit Hilfsskript: Skill „youtube-transkript“, sofern im Konto hochgeladen.

## Videos per Code: Werkzeugwahl und Kosten

Probe vom 05.11.2026 (Code und Zahlen: `video/remotion-probe/`, Ergebnisseite
[Remotion-Probe Mathe-Video](https://claude.ai/artifact/PAM9enLvXtKJQBCDBVPBgS)): Kapitel „Der Trick“ der Mathe-Videos
(`luperttrading-lab/5-Minuten-videos`) mit [Remotion](https://www.remotion.dev) nachgebaut und gegen den eigenen
Python-Renderer gemessen.

- Maßstab des Nutzers sind Zeit und Kosten pro Änderungsrunde, nicht Codezeilen oder Eleganz. Werkzeugvergleiche daran
  messen und das Ergebnis mit Zahlen nennen.
- Befund: Aussehen identisch. Rendern mit Remotion langsamer (38–54 s statt 27 s für 30 s Video, also 1–2 min mehr je
  Runde). Normale Änderungen (Größe, Farbe, Zeitpunkt) gleich aufwendig. Nur Änderungen, die den Aufbau sprengen
  (Textumbruch, mitwachsende Kästen), sind in Remotion klar billiger (3 statt 32 Zeilen). Formelsatz (Bruch, Wurzel,
  Σ mit Grenzen, Binomialkoeffizient) gibt es nur mit HTML/KaTeX ohne Zusatzarbeit.
- Daraus die Regel:
  - Kopfrechen-Videos (Ziffern, Kästchen, Flächenmodelle): beim Python-Renderer bleiben, nicht umbauen.
  - Folgen mit Formeln oder Diagrammen (Klasse 9–13, Statistik): in Remotion + KaTeX bauen, `video/remotion-probe/`
    als Ausgangspunkt nehmen. Die KaTeX-Schrift ist dünner als der fette Inter-Look und muss angepasst werden.
  - Seneca-Videos bleiben bei ihrer eigenen HTML-Technik (Entscheidung des Nutzers, 05.11.).
  - Bei jedem neuen Video- oder Animationsprojekt kurz prüfen, ob Remotion Arbeit spart, und das in einem Satz sagen.
- Kosten: Der größte Hebel ist die Kontextgröße der Sitzung, nicht das Werkzeug. Die Mathe-Sitzung stand bei 777.000 von
  1 Mio. Token Kontext und ≈ 98 $ API-Gegenwert, davon 250 Mio. erneut gelesene Kontext-Tokens. Deshalb eine frische
  Sitzung pro Folge mit kurzer Übergabedatei, statt eine Sitzung weiterwachsen zu lassen.
- ElevenLabs: Jede Textänderung lässt die ganze Szene neu sprechen. Beim Mathe-Video ging das Dreifache des Endtexts
  an ElevenLabs (7.162 Zeichen gesendet, 3.079 abgerechnet, Endtext 2.335 Zeichen). Sprechtext erst festlegen, dann vertonen. Vor jedem Lauf
  prüfen, ob alle Texte im Cache liegen, und Tests ohne `ELEVENLABS_API_KEY` starten.

## Internetadressen

Jede genannte Internetadresse, Domain oder Quelle immer als klickbaren Markdown-Link ausgeben
(`[easybill.de](https://www.easybill.de)`), nie als nackten Text. Der Nutzer liest im Chat und tippt nichts ab.

## Link am Ende der Antwort

Wurde in der Antwort ein Artifact, eine Seite oder eine Datei veröffentlicht oder aktualisiert: den Link dazu als
letzte Zeile vor der Kostenzeile wiederholen (`**Link:** [Name](URL)`), auch wenn er weiter oben schon steht.
Der Nutzer liest auf dem Handy und soll den Link nicht in langen Antworten suchen müssen.

**Alles zum Anklicken kommt ganz ans Ende** (Wunsch des Nutzers, 09.11.2026): Dateien, Hörproben, Bilder, Videos und
Links stehen nach dem Erklärtext, direkt vor der Kostenzeile, nie oben. Ablauf: erst den Erklärtext schreiben, dann
die Dateien mit `SendUserFile` schicken, danach nur noch Link-Zeile und Kostenzeile. Im Text auf die Dateien mit
„unten“ verweisen, nicht mit „oben“.
