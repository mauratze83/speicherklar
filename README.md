# Speicherklar

Kostenloser Speicher-Rechner für geplante PV-Anlagen – https://speicherklar.de

- `src/` – Quellen: `sim.js` (Simulationskern, auch in Node testbar), `ui.js`, `body.html`, `style.css`, `fonts.css`
- `python3 build.py` – baut `index.html` aus `src/`
- `fonts/` – selbst gehostete Schriften (SIL Open Font License), kein Google Fonts
- Sonnendaten: PVGIS-SARAH3 Monatsmittel 2014–2023 je PLZ-Region © Europäische Union
- `src/articles.py` – Ratgeber-Artikel; `python3 build_articles.py` baut `ratgeber/`, die Sitemap und die Artikelliste der Startseite, danach `python3 build.py`
- `src/chrome.py` – gemeinsame Kopf- und Fußzeile für alle Seiten; `src/legal/` – Inhalt von Impressum und Datenschutz (werden von `build_articles.py` gebaut). Seiten nie direkt bearbeiten, nur die Quellen in `src/`.

## Speicherklar Pro (Angebots-Check)

- `pro/index.html` wird von `python3 build.py` mitgebaut. Quellen: `src/pro-body.html`, `src/pro-ui.js` (Seite, Freischaltung, Bericht), `src/pro.js` (Rechnung, in Node testbar), `src/pro.css`
- `src/pro-config.js` – Adresse des Workers, angezeigte Preise, Einführungsende, Starttermin. Leere Worker-Adresse = kein Verkauf.
- `worker/` – Cloudflare Worker für Kauf (Stripe Managed Payments) und Freischaltung. Preis-IDs und Einführungsende in `worker/wrangler.toml`. Deploy per Workflow „Worker“ mit den GitHub-Secrets CLOUDFLARE_API_TOKEN, CLOUDFLARE_ACCOUNT_ID, STRIPE_SECRET_KEY, LICENSE_SECRET. Der Lizenzschlüssel ist die Stripe-Checkout-ID mit Signatur, gespeichert wird nichts.
- `src/plz2.json` – Sonnendaten je zweistelligem PLZ-Gebiet für Pro (PVGIS-SARAH3 2014–2023, Ortsmittelpunkte aus GeoNames, CC BY 4.0). Erzeugt von `scripts/pvgis_plz2.py` per GitHub Actions (Workflow „Sonnendaten“, von Hand startbar), mit Gegenprobe gegen Region 4.
- `src/markt.js` – Marktspannen für den Preis-Check, ein- bis zweimal im Jahr aktualisieren
- `node test/pro.test.js` – Beispielrechnungen und Abgleich mit dem kostenlosen Rechner
- Lokal testen: `python3 -m http.server`, dann `localhost:8000/pro/`; der Schlüssel `DEV-SPEICHERKLAR` schaltet nur auf localhost frei
- Vorab-Zugang für die Warteliste: Link `https://speicherklar.de/pro/?vorab=1` in der Start-Mail
