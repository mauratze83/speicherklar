# Speicherklar Instagram (Branch `instagram`)

Dieser Branch wird von GitHub Pages nicht veröffentlicht. Er enthält den Bildgenerator für @speicherklar.

- `make.py`: Baukasten (Rahmen, Diagramme, Zählerrollen, Karten) und alle Posts als Liste von Slides. Neue Posts unten an `posts` anhängen, Name `postN-thema`.
- Aufruf: `SPEICHERKLAR_SITE=<Checkout von main> python3 make.py postN` baut nur die Posts, die mit `postN` beginnen, nach `out/`.
- `numbers.json` + `gen/update.js <ct>`: Zahlen der ersten Posts aus `src/sim.js`. Neue Posts rechnen ihre Zahlen direkt mit `src/sim.js` (Node), nie schätzen.
- Format: 1080×1350 (4:5). Mehr erlaubt die Meta Business Suite nicht. Rand 130 px seitlich (das Profilraster schneidet 3:4 aus), 120 px oben, 100 px unten. Diagramme nie breiter als der Inhalt.
- `themen.md`: Themenliste, erledigte Themen mit Datum markieren.
- `captions-*.md`: Captions, Alt-Texte und Hinweise je Woche.
- `wochen/JJJJ-MM-TT/`: fertige PNGs und captions.md der Woche. Die Aufgabe „Speicherklar Instagram-Ablage“ kopiert neue Wochenordner auf Manuels Mac (Insta/speicherklar/JJJJ-MM-TT).

## Reels (seit 14.11.2026)

- `reel.py`: baut ein Reel 1080×1920, 30 fps, aus einer Spec `reels/<name>.json` (Slides als HTML-Bausteine + Satz je Slide) und dem Voice-over von ElevenLabs (Stimme „Manuel“, voice_id `rnjPXZEdioENHjl9ZHCZ`, Modell eleven_v4, 1 Take). Schnitte setzt das Skript selbst auf die Sprechpausen. Aufruf: `SPEICHERKLAR_SITE=<Checkout von main> python3 reel.py reels/<name>.json` → `out/<name>.mp4` + Übersichtsbild.
- Länge 30–35 s (rund 75–85 gesprochene Wörter, `tempo` 1.05). Ein Satz = eine Slide, 7–9 Slides.
- Beispiel: `reels/reel1-angebot-6-statt-10.json` (Pilot vom 14.11.2026).
- Fertige Reels kommen mit in `wochen/JJJJ-MM-TT/` (MP4 + Abschnitt in captions.md).
