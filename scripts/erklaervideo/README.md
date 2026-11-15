# Erklärvideo – Quellen

Baut `video/erklaer-16x9.mp4` und `video/erklaer-9x16.mp4` (Stand 15.11.2026, 1:13 Min.).

- `stage.html`: alle Szenen als eine Seite, `render(T)` zeichnet den Zeitpunkt T (Sekunden). Zeiten der Einblendungen stehen in `data-in` auf der Zeitachse der ersten Sprachaufnahme (`words.json`) und werden über `setWarp` auf die aktuelle Aufnahme umgerechnet.
- `vo-a.mp3`: Voice-over (ElevenLabs v4, Manuels Stimme, Take 1), `words-a.json` die Wortzeiten dazu.
- `prep.py a` erzeugt `time-a.json` (Untertitel und Zeitumrechnung), `render.py h a` bzw. `render.py v a` rendert die Szenen nach `sc-h-a/`, `sc-v-a/` (Playwright + ffmpeg).
- Danach: Szenen mit dem concat-Demuxer zusammenfügen, Ton mit 0,4 s Versatz anlegen (siehe Doku im Projekt `claude/website-doku.md`).
- Bilder (`a-*.png`, `c-*.png`) sind Bildschirmfotos der Seite (`assets.py`) und Seiten aus `pro/musterbericht.pdf`.
- `fonts.css` und `fonts/` erwartet `stage.html` im selben Ordner: vorher `ln -s ../../fonts fonts` und `cp ../../src/fonts.css .`.

Muss neu gebaut werden, wenn sich der Preis-Hinweis am Ende (49 € bis 31.01.2027, danach 89 €) oder die Beispielzahlen (6 statt 10 kWh, rund 670 €) ändern.
