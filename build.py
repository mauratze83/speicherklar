"""Baut index.html aus src/. Aufruf: python3 build.py"""
import pathlib, sys
S = pathlib.Path(__file__).parent / "src"
sys.path.insert(0, str(S))
from chrome import header, footer, analytics
FAVICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 26 26'%3E%3Crect x='5' y='4' width='16' height='20' rx='2.5' fill='none' stroke='%2315212B' stroke-width='2'/%3E%3Crect x='10' y='1.5' width='6' height='3' rx='1' fill='%2315212B'/%3E%3Crect x='8' y='14' width='10' height='7' rx='1' fill='%23E39A0B'/%3E%3C/svg%3E")
sim = (S / "sim.js").read_text().split('if(typeof module!=="undefined")')[0]
head = f"""<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Speicherklar – Lohnt sich ein Stromspeicher für deine PV-Anlage?</title>
<meta name="description" content="Kostenloser Speicher-Rechner für geplante PV-Anlagen: Jahressimulation mit Sonnendaten für deine Region, Ausrichtung, Dachneigung und EEG-Reform 2027. Ohne Anmeldung.">
<link rel="canonical" href="https://speicherklar.de/">
<meta property="og:title" content="Speicherklar – Lohnt sich dein Stromspeicher?">
<meta property="og:description" content="Verkäufer rechnen mit Juli. Wir rechnen mit November. Kostenloser Speicher-Rechner für PV-Anlagen.">
<meta property="og:url" content="https://speicherklar.de/">
<meta property="og:type" content="website">
<meta property="og:locale" content="de_DE">
<meta name="theme-color" content="#EDF0F2">
<link rel="icon" href="{FAVICON}">
{analytics()}
<style>
{(S / "fonts.css").read_text()}{(S / "style.css").read_text()}</style>
</head>
<body>
"""
html = head + (S / "body.html").read_text().replace("<!--RATGEBER-->", (S / "ratgeber-teaser.html").read_text()).replace("<!--HEADER-->", header("./", "rechner")).replace("<!--FOOTER-->", footer("./")) + "\n<script>\n" + sim + "\n" + (S / "draw.js").read_text().split("if (typeof module")[0] + "\n" + (S / "ui.js").read_text() + "</script>\n</body>\n</html>\n"
(S.parent / "index.html").write_text(html)
print("index.html:", len(html), "Zeichen")

# Speicherklar Pro: pro/index.html (Angebots-Check)
def js(name): return (S / name).read_text().split('if(typeof module!=="undefined")')[0].split("if (typeof module")[0]
import json
_plz2 = S / "plz2.json"
_areas = json.loads(_plz2.read_text())["gebiete"] if _plz2.exists() else {}
plz2_js = "var PLZ2=" + json.dumps({k: {"n": a["n"], "lat": a["lat"], "lon": a["lon"], "H": a["H"], "Kd": a["Kd"]} for k, a in _areas.items()}, ensure_ascii=False, separators=(",", ":")) + ";"
pro_css = ((S / "fonts.css").read_text() + (S / "style.css").read_text()).replace("url(fonts/", "url(../fonts/") + (S / "pro.css").read_text()
pro_head = f"""<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Angebots-Check für PV-Speicher – Speicherklar Pro</title>
<meta name="description" content="Passt der Speicher in deinem PV-Angebot? Angebot eintragen, kostenlos die Einordnung sehen, Bericht mit passender Größe, Preis-Check und Fragen an den Installateur.">
<link rel="canonical" href="https://speicherklar.de/pro/">
<meta property="og:title" content="Speicherklar Pro – Angebots-Check für deinen Stromspeicher">
<meta property="og:description" content="Ist der Speicher in deinem Angebot zu groß? Rechne es nach, bevor du unterschreibst.">
<meta property="og:url" content="https://speicherklar.de/pro/">
<meta property="og:type" content="website">
<meta property="og:locale" content="de_DE">
<meta name="theme-color" content="#EDF0F2">
<link rel="icon" href="{FAVICON}">
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
