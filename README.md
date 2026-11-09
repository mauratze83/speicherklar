# Speicherklar

Kostenloser Speicher-Rechner für geplante PV-Anlagen – https://speicherklar.de

- `src/` – Quellen: `sim.js` (Simulationskern, auch in Node testbar), `ui.js`, `body.html`, `style.css`, `fonts.css`
- `python3 build.py` – baut `index.html` aus `src/`
- `fonts/` – selbst gehostete Schriften (SIL Open Font License), kein Google Fonts
- Sonnendaten: PVGIS-SARAH3 Monatsmittel 2014–2023 je PLZ-Region © Europäische Union
- `src/articles.py` – Ratgeber-Artikel; `python3 build_articles.py` baut `ratgeber/`, die Sitemap und die Artikelliste der Startseite, danach `python3 build.py`
- `src/chrome.py` – gemeinsame Kopf- und Fußzeile für alle Seiten; `src/legal/` – Inhalt von Impressum und Datenschutz (werden von `build_articles.py` gebaut). Seiten nie direkt bearbeiten, nur die Quellen in `src/`.
