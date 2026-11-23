# CLAUDE.md – Speicherklar

Kostenloser Stromspeicher-Rechner für **geplante** PV-Anlagen plus bezahltes Pro-Tool (Angebots-Check) auf https://speicherklar.de. Statische Seite auf GitHub Pages, Kauf und Freischaltung über einen Cloudflare Worker mit Stripe Managed Payments. Betreiber: Manuel (Kleinunternehmer § 19 UStG), Nebenprojekt mit 2–4 h/Woche – Änderungen klein, nachvollziehbar und sicher halten.

Details zu Aufbau, Lizenzen, KV und Freischlüsseln stehen im `README.md`. Diese Datei sagt, **wie hier gearbeitet wird**.

## Stand (Nov. 2026)

- Rechner und Pro sind live und funktionieren.
- Speicherklar Pro ist seit 22.11.2026 für alle kaufbar (`publicFrom` = `2026-11-22` in `src/pro-config.js`, vorgezogen vom 01.12.2026). Die Vorab-Logik (`?vorab=1`/`?vorab=0` in `pro-ui.js`) bleibt im Code, wirkt aber nur vor `publicFrom`; **nirgends verlinken**. Der Worker prüft kein Datum.
- Preise: 49 € Einführungspreis bis 31.01.2027, danach 89 €, einmalig, 90 Tage Laufzeit ab erster Freischaltung, max. 3 Geräte.
- Eigene Besuche nicht zählen (seit 14.11.2026): `speicherklar.de/?ich=1` setzt `umami.disabled` im localStorage, `?ich=0` entfernt es; der Parameter verschwindet danach aus der Adresse. Code: `OPTOUT_JS` in `src/chrome.py`, Hinweis in der Datenschutzerklärung (`UMAMI_TEXT` in `build_articles.py`). **Nirgends verlinken.**
- Verbrauchsmodell (seit 14.11.2026): Die Wärmepumpe (`hp`) steht in `load.steady` und bekommt in `runBattery`/`daySeries` keine Lastspitzen innerhalb der Stunde (`stepLoad` in `src/sim.js`); Haushalt und E-Auto behalten sie. Der kostenlose Rechner hat dafür das Feld „Wärmepumpe pro Jahr“ (`#hp`, wird an Pro übergeben). Ohne Wärmepumpe sind alle Ergebnisse unverändert. Geprüft an Manuels eigener Anlage, Ergebnis im Projekt unter `claude/sim-pruefung-eigene-anlage.md` und auf der Methodik-Seite (`#eigene-anlage`). Verteilung der Wärmepumpe auf Monate/Stunden (`HP_M`, `HP_H`) gemessen an den WPuQ-Häusern (ISFH, 2019–2020).
- Wetter (seit 14.11.2026): kein gewürfeltes Tageswetter mehr. `WY` in `src/sim.js` enthält die Stundenwerte eines echten Jahres (PVGIS-SARAH3 2020, Region 4: Globalstrahlung/4 und Diffusanteil·250 als Base64, Ortszeit, ohne 29.2.). `pvProfile` übernimmt daraus nur den Verlauf; Monatssummen `H` und mittlerer Diffusanteil `Kd` kommen aus der Region bzw. `plz2.json`. Geprüft an 30 gemessenen Häusern (WPuQ 2019, Minutenwerte) und Manuels Anlage; Ergebnisse auf der Methodik-Seite (`#eigene-anlage`) und im Projekt unter `claude/sim-pruefung-eigene-anlage.md`. Wetterjahr nicht ohne neue Prüfung tauschen: Es verschiebt alle Zahlen.
- Erklärvideo (seit 15.11.2026 live): `video/erklaer-16x9.mp4`, `video/erklaer-9x16.mp4`, `video/erklaer.jpg` (1:13 Min., Voice-over Manuels ElevenLabs-Stimme, Untertitel eingebrannt, daher keine VTT), eingetragen in `VIDEO` in `src/chrome.py` (selbst gehostet, kein YouTube). Zahlen im Video: 6 statt 10 kWh, rund 670 € (beste Größe, Region 4, `pro.js`); bei Änderungen an `sim.js`/`pro.js` prüfen und das Video ggf. neu erzeugen (Quellen unter `scripts/erklaervideo/`, siehe README dort; Preis-Hinweis am Ende nennt 49 € bis 31.01.2027, ab Februar 2027 neu rendern). Wäre `VIDEO["quer"]` leer, `VIDEO["quer"]` leer ist, gibt es keine Video-Knöpfe und kein Overlay, und `/so-gehts/` (Quelle `src/so-gehts.html`, gebaut in `build_articles.py`) steht mit Platzhalter und `noindex` außerhalb von Sitemap und `llms.txt`. Mit Video: Knopf „In 75 Sekunden erklärt“ (`video_trigger`) im Hero der Startseite (`<!--VIDEO-->` in `body.html`), im Pro-Kopf (`pro-body.html`) und im Rechner-Kasten der Artikel (`CTA`), Overlay `#vid-dlg` aus `footer()` mit der einen Bitte „Rechner starten“; Hochkant-Fassung (`hoch`) am Handy hochkant; bei niedrigen Fenstern im Querformat (max. 560 px hoch) schrumpft das Overlay, damit Video und „Rechner starten“ zusammen passen; im Hero zwischen 561 und 900 px wird „Jetzt rechnen“ nicht auf volle Breite gezogen, der Video-Knopf steht daneben. Umami: `video-open`, `video-start` (Wiedergabe läuft, einmal je Seitenaufruf, auch auf `/so-gehts/`), `video-ende`, `video-cta` (jeweils mit `ort`). „Rechner starten“ im Overlay schließt das Overlay immer; auf der Startseite (Rechner auf derselben Seite) scrollt es selbst zu `#rechner`, sonst bliebe das modale Fenster offen (Fehler in Safari/iPhone, behoben 15.11.2026, getestet mit WebKit und Chromium, hoch und quer). Preise und Termine auf `/so-gehts/` kommen aus `pro-config.js`; „Kaufen ab …“ und der Einführungspreis blenden sich per Datum im Browser selbst aus.
- Navigation (seit 15.11.2026): Rechner · Speicherklar Pro · So geht's · Ratgeber · Annahmen · Über mich · Instagram (`header()` in `src/chrome.py`). Die sieben Punkte passen ab 818 px in eine Zeile; Burger-Menü deshalb bis 840 px (zwei `@media (max-width:840px)` in `src/style.css` und `min-width:841px` in `MENU_JS`, immer gemeinsam ändern).
- Klara, die KI-Hilfe (seit 17.11.2026 **live für alle**): Chat-Widget aus `src/chrome.py` (`KLARA`, `klara_widget()`, kommt mit `footer()` auf jede Seite), eigener Worker `worker-klara/` (Claude Haiku 5.5 über die Claude API, getrennt vom Bezahl-Worker), Deploy über Workflow „Klara“ (`.github/workflows/klara.yml`, Secret `ANTHROPIC_API_KEY`). `KLARA["aktiv"]` = True (False = nur Browser mit `?klara=1` sehen sie; daran hängen auch Datenschutz-Abschnitt und Klara-Ereignisse im Umami-Abschnitt). Claude Haiku 5.5 mit `thinking: disabled` (sonst brechen Antworten ab). Regeln für Klara: `worker-klara/regeln.js` (keine Empfehlung fürs eigene Haus, keine eigenen Zahlen, Politik nur aus `src/klara-politik.md` mit Stand und Quelle, Weiterleitung an kontakt@speicherklar.de). Ihr Wissen erzeugt `scripts/klara_wissen.py` bei jedem `build.py` aus Artikeln, Methodik, Eingabefeldern, Annahmen, `so-gehts` und `pro-config.js` nach `worker-klara/wissen.js` (generiert, nicht von Hand ändern). Budget: Worker schaltet Klara ab 10 $ im Monat ab (`BUDGET_USD`), Not-Aus KV `cfg:aus` = `1`. Umami: `klara-open`, `klara-frage`, `klara-knopf`, `klara-mail`. Auswertung ohne Inhalte (seit 17.11.2026): Daumen unter jeder Antwort (`/feedback`, einmal je Antwort) und Klaras Selbsteinschätzung im Werkzeug `thema` (`beantwortet` ja/teilweise/nein, `unzufrieden`, `luecke` als Stichwort, im Worker gefiltert: keine Ziffern, kein @, höchstens 40 Zeichen); Summen in KV `stat:JJJJ-MM` (`selbst`, `daumen`, `luecken`), abrufbar über `GET /stats` mit `Authorization: Bearer` + GitHub-Secret `KLARA_STATS_KEY` (fehlt es, antwortet `/stats` mit 404). Der Umsatz-Review liest das. Gespräche mitlesen (mit Einwilligung) steht im Backlog. Konzept im Projekt unter `claude/chatbot-konzept.md`.
- Messung: Ein wöchentlicher Umsatz-Review (geplante Claude-Aufgabe, sonntags) liest Umami über den Freigabe-Link „Umsatz-Review“ und Stripe über einen eingeschränkten Lese-Schlüssel; Ergebnis im Claude-Projekt unter `claude/umsatz-review.md`. Neue Umami-Ereignisse dort und in der Datenschutzerklärung nachziehen.

## Goldene Regeln

1. **Generierte Dateien nie direkt bearbeiten.** `index.html`, `pro/index.html`, `ratgeber/*.html`, `methodik.html`, `ueber-mich.html`, `impressum.html`, `datenschutz.html`, `sitemap.xml`, `img/og/*` entstehen aus `src/`. Immer die Quelle ändern und neu bauen.
2. **Push auf `main` ist live.** GitHub Pages veröffentlicht sofort; Änderungen unter `worker/` deployen per Workflow „Worker“ direkt den Bezahl-Worker, Änderungen unter `worker-klara/` (auch das generierte `wissen.js`) per Workflow „Klara“ den Klara-Worker. Worker-Änderungen deshalb nur nach Rückfrage und mit Testplan.
3. **Keine Geheimnisse im Repo.** Stripe-, Cloudflare-, MailerLite- und Lizenz-Secrets liegen nur in GitHub/Cloudflare. Freischlüssel nur als SHA-256-Hash in `FREE_KEYS`. Keine Klartext-Schlüssel, Mailadressen oder Checkout-IDs von Käufern in Code, Commits oder Logs.
4. **Zahlen kommen aus dem Simulationskern.** Jede Zahl in Artikeln, auf der Startseite oder in Social-Texten muss mit `src/sim.js` bzw. `src/pro.js` gerechnet sein – nie schätzen oder runden „nach Gefühl“. Annahmen der Beispiele: `BEISPIEL` und `CHART_BASE` in `src/articles.py`.
5. **Werte, die an mehreren Stellen stehen, immer gemeinsam ändern** (siehe Tabelle unten).

## Bauen und testen

```bash
node test/pro.test.js                 # Pro-Rechnung + Abgleich mit dem kostenlosen Rechner, muss ohne Fehler laufen
node test/klara.test.mjs              # Klara-Worker ohne echte API (Prompt, Schutz, Budget, Stream), muss ohne Fehler laufen
ANTHROPIC_API_KEY=… node test/klara-eval.mjs   # Klara gegen die echte API mit test/klara-faelle.json (kostet Cent, Antworten lesen)
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
| Rechenlogik | `src/sim.js` ↔ `src/pro.js` (Test gleicht beide ab), danach Musterbericht neu; Zahlen der Methodik-Abschnitte HTW-Vergleich, Strompreis und eigene Anlage neu rechnen |
| Kopf/Fuß, Analytics (Umami) | nur `src/chrome.py` |
| Klara sichtbar | `KLARA["aktiv"]` in `src/chrome.py` (auch Datenschutz-Abschnitt hängt daran), `KLARA["api"]` = Worker-Adresse |
| Klara-Budget, Preise, Modell | `BUDGET_USD`, `PREIS_*`, `MODEL` in `worker-klara/wrangler.toml`; Ausgabenlimit in der Claude Console gleich setzen |
| Politik für Klara | `src/klara-politik.md` (Stand, Status, Quelle, Prüfen bis); bei Änderungen an EEG/Steuern in Artikeln auch hier nachziehen |

## Wo was liegt

- `src/sim.js` – Simulationskern (5-Minuten-Schritte, PVGIS-Sonnendaten je Region), in Node testbar
- `src/ui.js`, `src/body.html`, `src/charts.js`, `src/draw.js`, `src/style.css` – kostenloser Rechner
- `src/pro.js` (Rechnung) · `src/pro-ui.js` (Seite, Freischaltung, Bericht, Vorab-Logik) · `src/pro-body.html` · `src/pro.css` · `src/pro-config.js`
- `src/markt.js` – Marktspannen für den Preis-Check, 1–2× im Jahr aktualisieren
- `src/plz2.json` – Sonnendaten je PLZ-Gebiet für Pro; nur über Workflow „Sonnendaten“ (`scripts/pvgis_plz2.py`) erzeugen, nicht von Hand
- `src/articles.py` – alle Ratgeber-Artikel (slug, title, desc, date, kennzahl, chart, body …); `build_articles.py` baut daraus `ratgeber/`
- `worker/index.js` – Endpunkte `/checkout`, `/verify`, `/validate`; `worker/wrangler.toml` – Variablen
- `worker-klara/` – Klara: `index.js` (`/status`, `/start`, `/session`, `/chat`), `regeln.js` (Systemprompt, von Hand), `wissen.js` (generiert), `wrangler.toml`
- `src/klara-politik.md` – Politik, Steuern, Förderung für Klara; `scripts/klara_wissen.py` – erzeugt `worker-klara/wissen.js`
- `src/folien/<name>/` – Präsentationen (Export aus den Slides-Artefakten: `deck.json`, `deck.css`, `slides/*.html`); `python3 scripts/folien.py` baut `folien/<name>/index.html`. Seit 23.11.2026: `/folien/kunden/` und `/folien/energieberater/`. **Nirgends verlinken**, `noindex`, nicht in Sitemap, `llms.txt` oder Klaras Wissen. Zahlen darin bei Änderungen an `sim.js`/`pro.js` mitprüfen.

## Ratgeber-Artikel

- Neue Artikel in `src/articles.py` eintragen (neueste nach Datum), nie als HTML-Datei anlegen.
- Zielgruppe: Leute, die eine PV-Anlage **erst planen** und wissen wollen, ob und welcher Speicher sich lohnt. Ton: sachlich, du-Form, Zahlen statt Prospekt, unabhängig von Herstellern. Absender ist immer „ich“ (Manuel), nie „wir“/„unser“ – auf allen Seiten, auch in Formularen und Meldungen (seit 16.11.2026 durchgehend umgestellt; „unser Dach“ in Über mich meint die Familie und bleibt). Das Bezahlprodukt heißt immer „Speicherklar Pro“, auch in Zusammensetzungen („Zugang zu Speicherklar Pro“ statt „Pro-Zugang“). Umgangssprache wie „rauskommen“, „prüf“, „hab’s“ ist gewollt.
- Suchtitel (`<title>`) = `seo_title` (sonst `title`) + „ | Speicherklar“, höchstens 60 Zeichen (SEO-Tools warnen ab 70). `build_articles.py` meldet „WARNUNG: Titel …“, wenn es länger wird; dann `seo_title` setzen. `title` bleibt für Karten, Brotkrumen und `headline`, die Überschrift kommt aus `h1`.
- `kennzahl` muss wörtlich im Artikel vorkommen; Stand-Angabe (`STAND`) aktuell halten.
- Balken (`bars`) zeigen Euro mit Vorzeichen; mit `"unit": "kWh"` (oder einer anderen Einheit) eine Zahl mit Einheit. Der Prüf-Artikel `stromspeicher-rechner-test-echte-daten` enthält Messwerte von Manuels Anlage und WPuQ-Ergebnisse: bei Änderungen an `sim.js` die Rechner-Zahlen dort mit neu rechnen.
- Kein Newsletter-CTA – Kommunikation läuft über Website und Instagram @speicherklar.
- Für Artikel gibt es den Skill `/sk-artikel`, für Instagram `/sk-instagram`.

## Konventionen

- Sprache in Code-Kommentaren, Commits und UI: Deutsch. Commit-Nachricht beschreibt das Ergebnis, z. B. „Artikel Größe berechnen: Mehr-Ersparnis genau gerundet“.
- Keine Frameworks, keine Build-Tools außer Python 3 und Node; keine externen CDNs oder Google Fonts (Schriften liegen in `fonts/`).
- Datenschutz: keine Cookies, keine Inhalte von fremden Servern, Reichweite nur über die cookielose Messung mit Umami (`src/chrome.py`); neue externe Dienste nur nach Rückfrage und mit Anpassung in `src/legal/datenschutz.html`.
- Leerzeichen zwischen nebeneinanderstehenden Inline-Elementen (`<span>`, `<b>`, `<a>`, `<small>`, `<em>`), auch wenn CSS sie optisch trennt (Kapseln, Legenden, Karten). Google nimmt Seitentext fürs Snippet und klebt sonst Wörter zusammen („kostenlosohne Anmeldung“). In Flex/Grid ändert das Leerzeichen die Darstellung nicht. Ausnahme: Ziffern der Zählerrollen (`.dg .wheel`) bleiben ohne Leerzeichen.
- Vor jedem Commit: Tests grün, Build gelaufen, Diff durchgesehen.
