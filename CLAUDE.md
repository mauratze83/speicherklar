# CLAUDE.md – Speicherklar

Kostenloser Stromspeicher-Rechner für **geplante** PV-Anlagen plus bezahltes Pro-Tool (Angebots-Check) auf https://speicherklar.de. Statische Seite auf GitHub Pages, Kauf und Freischaltung über einen Cloudflare Worker mit Stripe Managed Payments. Betreiber: Manuel (Kleinunternehmer § 19 UStG), Nebenprojekt mit 2–4 h/Woche – Änderungen klein, nachvollziehbar und sicher halten.

Details zu Aufbau, Lizenzen, KV und Freischlüsseln stehen im `README.md`. Diese Datei sagt, **wie hier gearbeitet wird**.

## Stand (Nov. 2026)

- Rechner und Pro sind live und funktionieren.
- Der Kauf-Button ist bis `publicFrom` (`2026-12-01` in `src/pro-config.js`) inaktiv („Kauf ab 1.12.2026“). Kaufen geht vorher nur mit `?vorab=1` (wird im Browser gemerkt, `?vorab=0` nimmt es weg) – nur zum internen Testen, **nirgends verlinken**.
- Preise: 49 € Einführungspreis bis 31.01.2027, danach 89 €, einmalig, 90 Tage Laufzeit ab erster Freischaltung, max. 3 Geräte.

## Goldene Regeln

1. **Generierte Dateien nie direkt bearbeiten.** `index.html`, `pro/index.html`, `ratgeber/*.html`, `methodik.html`, `ueber-mich.html`, `impressum.html`, `datenschutz.html`, `sitemap.xml`, `img/og/*` entstehen aus `src/`. Immer die Quelle ändern und neu bauen.
2. **Push auf `main` ist live.** GitHub Pages veröffentlicht sofort; Änderungen unter `worker/` deployen per Workflow „Worker“ direkt den Bezahl-Worker. Worker-Änderungen deshalb nur nach Rückfrage und mit Testplan.
3. **Keine Geheimnisse im Repo.** Stripe-, Cloudflare-, MailerLite- und Lizenz-Secrets liegen nur in GitHub/Cloudflare. Freischlüssel nur als SHA-256-Hash in `FREE_KEYS`. Keine Klartext-Schlüssel, Mailadressen oder Checkout-IDs von Käufern in Code, Commits oder Logs.
4. **Zahlen kommen aus dem Simulationskern.** Jede Zahl in Artikeln, auf der Startseite oder in Social-Texten muss mit `src/sim.js` bzw. `src/pro.js` gerechnet sein – nie schätzen oder runden „nach Gefühl“. Annahmen der Beispiele: `BEISPIEL` und `CHART_BASE` in `src/articles.py`.
5. **Werte, die an mehreren Stellen stehen, immer gemeinsam ändern** (siehe Tabelle unten).

## Bauen und testen

```bash
node test/pro.test.js                 # Pro-Rechnung + Abgleich mit dem kostenlosen Rechner, muss ohne Fehler laufen
python3 build_articles.py             # nur wenn Artikel, chrome.py, legal/, methodik/über-mich oder Bilder betroffen (braucht Playwright für img/og)
python3 build.py                      # baut index.html, pro/index.html, sitemap.xml – immer als letzter Schritt
python3 -m http.server                # lokal prüfen: localhost:8000/ und localhost:8000/pro/
python3 scripts/musterbericht.py      # pro/musterbericht.pdf neu, wenn sim.js, pro.js oder pro-ui.js geändert wurden
```

Reihenfolge: Quelle ändern → Tests → `build_articles.py` (falls nötig) → `build.py` → `git diff` prüfen, dass nur erwartete Dateien geändert sind. Ein Build ohne Quelländerung darf keinen Diff erzeugen.

## Werte, die zusammengehören

| Was | Stellen |
|---|---|
| Preise 49/89 € | Stripe-Preise, `PRICE_INTRO`/`PRICE_REGULAR` in `worker/wrangler.toml`, `price`/`regularPrice` in `src/pro-config.js`, Texte in Artikeln/Pro-Seite |
| Ende Einführungspreis | `INTRO_UNTIL` (Worker) = `introUntil` (`pro-config.js`) |
| Laufzeit 90 Tage | `ACCESS_DAYS` (Worker) = `accessDays` (`pro-config.js`) |
| Verkaufsstart | `publicFrom` in `pro-config.js` |
| Rechenlogik | `src/sim.js` ↔ `src/pro.js` (Test gleicht beide ab), danach Musterbericht neu |
| Kopf/Fuß, Analytics (Umami) | nur `src/chrome.py` |

## Wo was liegt

- `src/sim.js` – Simulationskern (5-Minuten-Schritte, PVGIS-Sonnendaten je Region), in Node testbar
- `src/ui.js`, `src/body.html`, `src/charts.js`, `src/draw.js`, `src/style.css` – kostenloser Rechner
- `src/pro.js` (Rechnung) · `src/pro-ui.js` (Seite, Freischaltung, Bericht, Vorab-Logik) · `src/pro-body.html` · `src/pro.css` · `src/pro-config.js`
- `src/markt.js` – Marktspannen für den Preis-Check, 1–2× im Jahr aktualisieren
- `src/plz2.json` – Sonnendaten je PLZ-Gebiet für Pro; nur über Workflow „Sonnendaten“ (`scripts/pvgis_plz2.py`) erzeugen, nicht von Hand
- `src/articles.py` – alle Ratgeber-Artikel (slug, title, desc, date, kennzahl, chart, body …); `build_articles.py` baut daraus `ratgeber/`
- `worker/index.js` – Endpunkte `/checkout`, `/verify`, `/validate`; `worker/wrangler.toml` – Variablen

## Ratgeber-Artikel

- Neue Artikel in `src/articles.py` eintragen (neueste nach Datum), nie als HTML-Datei anlegen.
- Zielgruppe: Leute, die eine PV-Anlage **erst planen** und wissen wollen, ob und welcher Speicher sich lohnt. Ton: sachlich, du-Form, Zahlen statt Prospekt, unabhängig von Herstellern.
- `kennzahl` muss wörtlich im Artikel vorkommen; Stand-Angabe (`STAND`) aktuell halten.
- Kein Newsletter-CTA – Kommunikation läuft über Website und Instagram @speicherklar.
- Für Artikel gibt es den Skill `/sk-artikel`, für Instagram `/sk-instagram`.

## Konventionen

- Sprache in Code-Kommentaren, Commits und UI: Deutsch. Commit-Nachricht beschreibt das Ergebnis, z. B. „Artikel Größe berechnen: Mehr-Ersparnis genau gerundet“.
- Keine Frameworks, keine Build-Tools außer Python 3 und Node; keine externen CDNs oder Google Fonts (Schriften liegen in `fonts/`).
- Datenschutz: keine Cookies, keine Inhalte von fremden Servern, Reichweite nur über die cookielose Messung mit Umami (`src/chrome.py`); neue externe Dienste nur nach Rückfrage und mit Anpassung in `src/legal/datenschutz.html`.
- Leerzeichen zwischen nebeneinanderstehenden Inline-Elementen (`<span>`, `<b>`, `<a>`, `<small>`, `<em>`), auch wenn CSS sie optisch trennt (Kapseln, Legenden, Karten). Google nimmt Seitentext fürs Snippet und klebt sonst Wörter zusammen („kostenlosohne Anmeldung“). In Flex/Grid ändert das Leerzeichen die Darstellung nicht. Ausnahme: Ziffern der Zählerrollen (`.dg .wheel`) bleiben ohne Leerzeichen.
- Vor jedem Commit: Tests grün, Build gelaufen, Diff durchgesehen.
