"""Baut index.html aus src/. Aufruf: python3 build.py"""
import pathlib, sys, re
S = pathlib.Path(__file__).parent / "src"
sys.path.insert(0, str(S))
from chrome import header, footer, analytics, head_meta
FAVICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 26 26'%3E%3Crect x='5' y='4' width='16' height='20' rx='2.5' fill='none' stroke='%2315212B' stroke-width='2'/%3E%3Crect x='10' y='1.5' width='6' height='3' rx='1' fill='%2315212B'/%3E%3Crect x='8' y='14' width='10' height='7' rx='1' fill='%23E39A0B'/%3E%3C/svg%3E")
sim = (S / "sim.js").read_text().split('if(typeof module!=="undefined")')[0]
import json
SITE = "https://speicherklar.de/"
# Strukturierte Daten der Startseite: Website, Betreiber und der kostenlose Rechner als Web-Anwendung
_org = {"@type": "Organization", "@id": SITE + "#org", "name": "Speicherklar", "url": SITE, "logo": SITE + "img/icon-512.png",
        "email": "kontakt@speicherklar.de", "sameAs": ["https://www.instagram.com/speicherklar/"]}
HOME_LD = '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@graph": [
    {"@type": "WebSite", "@id": SITE + "#website", "name": "Speicherklar", "url": SITE, "inLanguage": "de", "publisher": {"@id": SITE + "#org"}},
    _org,
    {"@type": "WebApplication", "name": "Speicherklar Stromspeicher-Rechner", "url": SITE, "applicationCategory": "UtilitiesApplication",
     "operatingSystem": "Web-Browser", "inLanguage": "de", "isAccessibleForFree": True,
     "description": "Jahressimulation in 5-Minuten-Schritten mit Sonnendaten der Region. Zeigt, welche Speichergröße sich für eine geplante PV-Anlage lohnt.",
     "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"}, "publisher": {"@id": SITE + "#org"}}]}, ensure_ascii=False) + '</script>'
import subprocess, re as _re0
def prerender(body):
    """Ergebnis des Standard-Beispiels fest ins HTML schreiben (für Crawler ohne JavaScript).
    Startwerte kommen aus body.html und ui.js, gerechnet wird mit src/sim.js (scripts/prerender.js)."""
    val = lambda i: float(_re0.search(rf'id="{i}"[^>]*value="([^"]+)"', body).group(1))
    d = {k: val(k) for k in ("pv", "tilt", "cons", "ev", "bat", "bprice", "life", "price", "feed")}
    d = {k: int(v) if v == int(v) else v for k, v in d.items()}
    d["region"] = _re0.search(r'region:"(\d)"', (S / "ui.js").read_text()).group(1)
    r = json.loads(subprocess.run(["node", str(S.parent / "scripts/prerender.js"), json.dumps(d)], check=True, capture_output=True, text=True).stdout)
    global PRERENDER; PRERENDER = r
    rep = {'id="verdict">Rechne…<': f'id="verdict">{r["verdict"]}<',
           'id="k-save">–<': f'id="k-save">{r["save"]}<', 'id="k-pay">–<': f'id="k-pay">{r["pay"]}<',
           'id="k-cost">–<': f'id="k-cost">{r["cost"]}<', 'id="k-netd">–<': f'id="k-netd">{r["netd"]}<',
           'id="k-net">–<': f'id="k-net" style="color:var(--{"pos" if r["netPos"] else "neg"})">{r["net"]}<',
           '<!--SWEEPSUM-->': f'{r["example"]} {r["sweep"]}'}
    for a, b in rep.items():
        assert a in body, f"prerender: {a} fehlt in body.html"
        body = body.replace(a, b)
    return body
head = f"""<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Stromspeicher-Rechner: Welche Größe lohnt sich? | Speicherklar</title>
<meta name="description" content="Kostenloser Stromspeicher-Rechner ohne Anmeldung: Jahressimulation mit Sonnendaten deiner Region. Zeigt, welche Speichergröße zu deiner PV-Anlage passt.">
<link rel="canonical" href="https://speicherklar.de/">
{HOME_LD}
<meta property="og:title" content="Speicherklar – Passen Speicher und PV-Anlage zu deinem Haus?">
<meta property="og:description" content="Verkäufer rechnen mit Juli. Wir rechnen mit November. Kostenloser Speicher-Rechner und Angebots-Check für PV-Anlage und Speicher.">
<meta property="og:url" content="https://speicherklar.de/">
<meta property="og:type" content="website">
<meta property="og:locale" content="de_DE">
<meta name="theme-color" content="#EDF0F2">
{head_meta("img/og/start.png", "Speicherklar: Lohnt sich dein Stromspeicher? Verkäufer rechnen mit Juli, wir rechnen mit November.")}
{analytics()}
<style>
{(S / "fonts.css").read_text()}{(S / "style.css").read_text()}</style>
</head>
<body>
"""
html = head + prerender((S / "body.html").read_text()).replace("<!--RATGEBER-->", (S / "ratgeber-teaser.html").read_text()).replace("<!--HEADER-->", header("./", "rechner")).replace("<!--FOOTER-->", footer("./")) + "\n<script>\n" + sim + "\n" + (S / "draw.js").read_text().split("if (typeof module")[0] + "\n" + (S / "ui.js").read_text() + "</script>\n</body>\n</html>\n"
_cfg = (S / "pro-config.js").read_text()
_cv = lambda k: re.search(k + r'\s*:\s*"?([^",\n]*)"?', _cfg).group(1)
PRO_VALUES = {"{{PRO_PUBLIC}}": _cv("publicFrom"), "{{PRO_INTRO}}": _cv("introUntil"), "{{PRO_PRICE}}": _cv("price"), "{{PRO_REGULAR}}": _cv("regularPrice")}
PRO_VALUES["{{PRO_INTRO_DE}}"] = ".".join(reversed(PRO_VALUES["{{PRO_INTRO}}"].split("-")))
for _k, _v in PRO_VALUES.items(): html = html.replace(_k, _v)
assert "{{PRO_" not in html
(S.parent / "index.html").write_text(html)
print("index.html:", len(html), "Zeichen")

# Speicherklar Pro: pro/index.html (Angebots-Check)
def js(name): return (S / name).read_text().split('if(typeof module!=="undefined")')[0].split("if (typeof module")[0]
_plz2 = S / "plz2.json"
_areas = json.loads(_plz2.read_text())["gebiete"] if _plz2.exists() else {}
plz2_js = "var PLZ2=" + json.dumps({k: {"n": a["n"], "lat": a["lat"], "lon": a["lon"], "H": a["H"], "Kd": a["Kd"]} for k, a in _areas.items()}, ensure_ascii=False, separators=(",", ":")) + ";"
pro_css = ((S / "fonts.css").read_text() + (S / "style.css").read_text()).replace("url(fonts/", "url(../fonts/") + (S / "pro.css").read_text()
pro_head = f"""<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Angebots-Check für PV-Anlage und Speicher – Speicherklar Pro</title>
<meta name="description" content="Passen Speicher und PV-Anlage in deinem Angebot? Angebot eintragen, kostenlos die Einordnung sehen, Bericht mit bester Kombination aus PV-Größe und Speicher, Preis-Check und Fragen an den Installateur.">
<link rel="canonical" href="https://speicherklar.de/pro/">
<meta property="og:title" content="Speicherklar Pro – Angebots-Check für PV-Anlage und Speicher">
<meta property="og:description" content="Ist der Speicher zu groß, die Anlage zu klein? Rechne dein Angebot nach, bevor du unterschreibst.">
<meta property="og:url" content="https://speicherklar.de/pro/">
<meta property="og:type" content="website">
<meta property="og:locale" content="de_DE">
<meta name="theme-color" content="#EDF0F2">
{head_meta("img/og/pro.png", "Speicherklar Pro: Die zweite Rechnung zu deinem Angebot. Bevor du unterschreibst.")}
{analytics()}
<style>
{pro_css}</style>
</head>
<body>
"""
pro_html = pro_head + (S / "pro-body.html").read_text().replace("<!--HEADER-->", header("../", "pro")).replace("<!--FOOTER-->", footer("../")) + \
    "\n<script>\n" + "\n".join([js("sim.js"), plz2_js, js("draw.js"), js("markt.js"), (S / "pro-config.js").read_text(), js("pro.js"), (S / "pro-ui.js").read_text()]) + "</script>\n</body>\n</html>\n"
(S.parent / "pro").mkdir(exist_ok=True)
(S.parent / "pro" / "index.html").write_text(pro_html)
print("pro/index.html:", len(pro_html), "Zeichen,", len(_areas), "PLZ-Gebiete")

# Sitemap: alle indexierbaren Seiten. lastmod = Tag, an dem sich die gebaute Seite zuletzt geändert hat
# (Prüfsumme in src/sitemap-dates.json). Läuft hier, weil build.py immer als Letztes gebaut wird.
import hashlib, datetime, re as _re
ROOT = S.parent
pages = ["index.html", "ratgeber/index.html"] + sorted(str(p.relative_to(ROOT)) for p in (ROOT / "ratgeber").glob("*.html") if p.name != "index.html") \
    + ["methodik.html", "ueber-mich.html", "pro/index.html"]
_df = S / "sitemap-dates.json"
dates = json.loads(_df.read_text()) if _df.exists() else {}
today = datetime.date.today().isoformat()
rows = []
for rel in pages:
    txt = (ROOT / rel).read_text()
    if 'name="robots" content="noindex"' in txt: continue
    url = SITE + _re.sub(r"(^|/)index\.html$", r"\1", rel)
    h = hashlib.sha1(txt.encode()).hexdigest()[:12]
    if dates.get(url, {}).get("hash") != h: dates[url] = {"date": today, "hash": h}
    rows.append(f"  <url><loc>{url}</loc><lastmod>{dates[url]['date']}</lastmod></url>\n")
dates = {u: v for u, v in dates.items() if any(f"<loc>{u}</loc>" in r for r in rows)}
_df.write_text(json.dumps(dates, indent=1, sort_keys=True) + "\n")
# llms.txt: kurze Übersicht der Seite für KI-Suchdienste (Format llmstxt.org). Wird aus den Artikeln und
# dem vorgerechneten Standard-Beispiel erzeugt, damit die Zahlen immer zu sim.js passen.
import sys as _sys
_sys.path.insert(0, str(S))
from articles import ARTICLES as _ARTS
_b = PRERENDER["best"]
_nf = lambda v: f"{v:,.0f}".replace(",", ".")
llms = f"""# Speicherklar

> Kostenloser Stromspeicher-Rechner für Leute, die eine PV-Anlage planen: Welche Speichergröße lohnt sich? Ohne Anmeldung, ohne Provision, ohne Werbung. Jahressimulation in 5-Minuten-Schritten mit Sonnendaten aus PVGIS 2014–2023, Rechenweg offen auf GitHub.

Betrieben von Manuel Maurer, Krefeld. Speicherklar verdient nichts an verkauften Speichern und hat keine Partner-Installateure. Die Seite finanziert sich nur über Speicherklar Pro.

Ergebnis des Rechners mit den Startwerten. {PRERENDER["example"]} Am meisten bleibt bei {_b["cap"]} kWh nutzbarer Speicherkapazität: +{_nf(_b["net"])} € {PRERENDER["netd"]}, bezahlt nach {str(_b["payback"]).replace(".", ",")} Jahren. Größere Speicher sparen pro Jahr etwas mehr, kosten aber mehr, als sie zusätzlich sparen.

Nicht im Modell: Wärmepumpen-Lastprofil (nur in Speicherklar Pro), Notstrom, Verschattung, Alterung des Speichers, dynamische Stromtarife.

## Rechner und Methodik

- [Stromspeicher-Rechner]({SITE}): PLZ, Dachausrichtung, Neigung, kWp, Jahresverbrauch und E-Auto eingeben; zeigt Ersparnis, Amortisation, Bilanz und die wirtschaftlichste Speichergröße von 1 bis 15 kWh.
- [Methodik]({SITE}methodik.html): Rechenweg, Annahmen, Quellen, Grenzen und Vergleich mit dem Unabhängigkeitsrechner der HTW Berlin.
- [Speicherklar Pro]({SITE}pro/): Angebots-Check für ein konkretes Installateur-Angebot. Erste Einschätzung kostenlos als Ampel (Speichergröße, PV-Größe, Preis je kWh und je kWp), danach ein PDF-Bericht mit der besten Kombination aus PV-Anlage und Speicher.

## Ratgeber

""" + "".join(f"- [{a['title']}]({SITE}ratgeber/{a['slug']}.html): {a['desc']}\n" for a in _ARTS) + f"""
## Optional

- [Über mich]({SITE}ueber-mich.html)
- [Quellcode auf GitHub](https://github.com/mauratze83/speicherklar): öffentlich zum Nachlesen, alle Rechte vorbehalten.
"""
(ROOT / "llms.txt").write_text(llms)
(ROOT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(rows) + "</urlset>\n")
print("sitemap.xml:", len(rows), "Seiten")
