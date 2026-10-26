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

## Internetadressen

Jede genannte Internetadresse, Domain oder Quelle immer als klickbaren Markdown-Link ausgeben
(`[easybill.de](https://www.easybill.de)`), nie als nackten Text. Der Nutzer liest im Chat und tippt nichts ab.

## Link am Ende der Antwort

Wurde in der Antwort ein Artifact, eine Seite oder eine Datei veröffentlicht oder aktualisiert: den Link dazu als
letzte Zeile vor der Kostenzeile wiederholen (`**Link:** [Name](URL)`), auch wenn er weiter oben schon steht.
Der Nutzer liest auf dem Handy und soll den Link nicht in langen Antworten suchen müssen.
