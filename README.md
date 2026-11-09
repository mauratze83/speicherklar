# Speicherklar

Kostenloser Speicher-Rechner für geplante PV-Anlagen – https://speicherklar.de

- `src/` – Quellen: `sim.js` (Simulationskern, auch in Node testbar), `ui.js`, `body.html`, `style.css`, `fonts.css`
- `python3 build.py` – baut `index.html` aus `src/`
- `fonts/` – selbst gehostete Schriften (SIL Open Font License), kein Google Fonts
- Sonnendaten: PVGIS-SARAH3 Monatsmittel 2014–2023 je PLZ-Region © Europäische Union
- `src/articles.py` – Ratgeber-Artikel; `python3 build_articles.py` baut `ratgeber/`, die Sitemap und die Artikelliste der Startseite, danach `python3 build.py`
- `src/chrome.py` – gemeinsame Kopf- und Fußzeile für alle Seiten; `src/legal/` – Inhalt von Impressum und Datenschutz (werden von `build_articles.py` gebaut). Seiten nie direkt bearbeiten, nur die Quellen in `src/`.
- `src/images.py` – Vorschaubilder für geteilte Links (`img/og/`, 1200×630, je Artikel mit Titel und Kennzahl) und App-Icons (`img/`, `apple-touch-icon.png`, `site.webmanifest`); wird von `build_articles.py` aufgerufen und braucht Playwright. Gebaut wird nur, was sich geändert hat (`img/og/sig.json`).
