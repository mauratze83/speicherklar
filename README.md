# Speicherklar

Kostenloser Speicher-Rechner für geplante PV-Anlagen – https://speicherklar.de

- `src/` – Quellen: `sim.js` (Simulationskern, auch in Node testbar), `ui.js`, `body.html`, `style.css`, `fonts.css`
- `python3 build.py` – baut `index.html` aus `src/`
- `fonts/` – selbst gehostete Schriften (SIL Open Font License), kein Google Fonts
- Sonnendaten: PVGIS-SARAH3 Monatsmittel 2014–2023 je PLZ-Region © Europäische Union
- `src/articles.py` – Ratgeber-Artikel; `python3 build_articles.py` baut `ratgeber/`, die Sitemap und die Artikelliste der Startseite, danach `python3 build.py`
- `src/chrome.py` – gemeinsame Kopf- und Fußzeile für alle Seiten; `src/legal/` – Inhalt von Impressum und Datenschutz (werden von `build_articles.py` gebaut). Seiten nie direkt bearbeiten, nur die Quellen in `src/`.
- `src/images.py` – Vorschaubilder für geteilte Links (`img/og/`, 1200×630, je Artikel mit Titel und Kennzahl) und App-Icons (`img/`, `apple-touch-icon.png`, `site.webmanifest`); wird von `build_articles.py` aufgerufen und braucht Playwright. Gebaut wird nur, was sich geändert hat (`img/og/sig.json`).

## Speicherklar Pro (Angebots-Check)

- `pro/index.html` wird von `python3 build.py` mitgebaut. Quellen: `src/pro-body.html`, `src/pro-ui.js` (Seite, Freischaltung, Bericht), `src/pro.js` (Rechnung, in Node testbar), `src/pro.css`
- `src/pro-config.js` – Adresse des Workers, angezeigte Preise, Einführungsende, Starttermin. Leere Worker-Adresse = kein Verkauf.
- `worker/` – Cloudflare Worker für Kauf (Stripe Managed Payments) und Freischaltung. Preis-IDs und Einführungsende in `worker/wrangler.toml`. Deploy per Workflow „Worker“ mit den GitHub-Secrets CLOUDFLARE_API_TOKEN, CLOUDFLARE_ACCOUNT_ID, STRIPE_SECRET_KEY, LICENSE_SECRET. Der Lizenzschlüssel ist die Stripe-Checkout-ID mit Signatur. Cloudflare KV (`LICENSES`, legt der Workflow an) speichert je Kauf die Geräte-IDs (Limit `MAX_DEVICES`), die gekürzte Mailadresse, ob die Schlüssel-Mail raus ist, und `activatedAt` (erste Freischaltung).
- Laufzeit: ein gekaufter Schlüssel gilt `ACCESS_DAYS` Tage (90) ab der ersten Freischaltung (`wrangler.toml`, Anzeige `accessDays` in `pro-config.js`). Danach meldet `/validate` `expired`; die Seite prüft das gespeicherte Ablaufdatum auch offline. Kostenlos verlängern: im KV-Eintrag `lic:<checkout-id>` `"until": "JJJJ-MM-TT"` (letzter gültiger Tag) setzen.
- Freischlüssel (Familie und Freunde): gelten ohne Kauf, ohne Gerätelimit und ohne Ablauf. Im Repo steht nur der SHA-256-Hash in `FREE_KEYS` (`worker/wrangler.toml`, kommagetrennt). Neuer Schlüssel: `printf '%s' 'SK.…' | sha256sum`, Hash ergänzen, pushen. Sperren: Hash löschen, pushen.
- Gerät freigeben oder Schlüssel sperren: Cloudflare-Dashboard → Storage & Databases → Workers KV → `speicherklar-pro-LICENSES` → Eintrag `lic:<checkout-id>`: in `devices` IDs löschen bzw. `"blocked": true` setzen.
- Schlüssel-Mail: MailerLite-Gruppen `ML_GROUP_BUYERS` (nach dem Kauf) und `ML_GROUP_RESEND` (Schlüssel vergessen) mit Automatisierung „tritt Gruppe bei“, Feld `lizenz`; Secret `MAILERLITE_API_KEY`.
- `src/plz2.json` – Sonnendaten je zweistelligem PLZ-Gebiet für Pro (PVGIS-SARAH3 2014–2023, Ortsmittelpunkte aus GeoNames, CC BY 4.0). Erzeugt von `scripts/pvgis_plz2.py` per GitHub Actions (Workflow „Sonnendaten“, von Hand startbar), mit Gegenprobe gegen Region 4.
- `src/markt.js` – Marktspannen für den Preis-Check, ein- bis zweimal im Jahr aktualisieren
- `node test/pro.test.js` – Beispielrechnungen und Abgleich mit dem kostenlosen Rechner
- Lokal testen: `python3 -m http.server`, dann `localhost:8000/pro/` (Einordnung ohne Freischaltung). Den vollständigen Bericht prüft `python3 scripts/musterbericht.py` (beantwortet die Lizenzprüfung nur im Testbrowser); auf speicherklar.de mit einem Freischlüssel.
- Freischaltung: ein gespeicherter Schlüssel wird bei jedem Aufruf der Pro-Seite beim Worker gegengeprüft (`/validate`); ohne Verbindung bleibt Pro bis zum gespeicherten Ablaufdatum freigeschaltet.
- `pro/musterbericht.pdf` – Musterbericht, erzeugt mit `python3 scripts/musterbericht.py` nach `build.py`; neu erzeugen, wenn sich `pro.js`, `pro-ui.js` oder `sim.js` ändern
- Kauf vor dem Starttermin (`publicFrom`) nur intern zum Testen: `https://speicherklar.de/pro/?vorab=1`
