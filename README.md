# Speicherklar Instagram (Branch `instagram`)

Dieser Branch wird von GitHub Pages nicht veröffentlicht. Er enthält den Bildgenerator für @speicherklar.

- `make.py`: Baukasten (Rahmen, Diagramme, Zählerrollen, Karten) und alle Posts als Liste von Slides. Neue Posts unten an `posts` anhängen, Name `postN-thema`.
- Aufruf: `SPEICHERKLAR_SITE=<Checkout von main> python3 make.py postN` baut nur die Posts, die mit `postN` beginnen, nach `out/`.
- `numbers.json` + `gen/update.js <ct>`: Zahlen der ersten Posts aus `src/sim.js`. Neue Posts rechnen ihre Zahlen direkt mit `src/sim.js` (Node), nie schätzen.
- Format: 1080×1350 (4:5). Mehr erlaubt die Meta Business Suite nicht. Rand 130 px seitlich (das Profilraster schneidet 3:4 aus), 120 px oben, 100 px unten. Diagramme nie breiter als der Inhalt.
- `themen.md`: Themenliste, erledigte Themen mit Datum markieren.
- `captions-*.md`: Captions, Alt-Texte und Hinweise je Woche.
- `wochen/JJJJ-MM-TT/`: fertige PNGs und captions.md der Woche. Die Aufgabe „Speicherklar Instagram-Ablage“ kopiert neue Wochenordner auf Manuels Mac (Insta/speicherklar/JJJJ-MM-TT).
