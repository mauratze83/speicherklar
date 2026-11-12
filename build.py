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
<link rel="icon" href="{FAVICON}">
{head_meta("img/og/start.png", "Speicherklar: Lohnt sich dein Stromspeicher? Verkäufer rechnen mit Juli, wir rechnen mit November.")}
{analytics()}
<style>
{(S / "fonts.css").read_text()}{(S / "style.css").read_text()}</style>
</head>
<body>
"""
html = head + (S / "body.html").read_text().replace("<!--RATGEBER-->", (S / "ratgeber-teaser.html").read_text()).replace("<!--HEADER-->", header("./", "rechner")).replace("<!--FOOTER-->", footer("./")) + "\n<script>\n" + sim + "\n" + (S / "draw.js").read_text().split("if (typeof module")[0] + "\n" + (S / "ui.js").read_text() + "</script>\n</body>\n</html>\n"
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
<link rel="icon" href="{FAVICON}">
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
(ROOT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(rows) + "</urlset>\n")
print("sitemap.xml:", len(rows), "Seiten")
