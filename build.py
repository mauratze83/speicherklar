"""Baut index.html aus src/. Aufruf: python3 build.py"""
import pathlib, sys
S = pathlib.Path(__file__).parent / "src"
sys.path.insert(0, str(S))
from chrome import header, footer, analytics, head_meta
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
{head_meta("img/og/start.png", "Speicherklar: Lohnt sich dein Stromspeicher? Verkäufer rechnen mit Juli, wir rechnen mit November.")}
{analytics()}
<style>
{(S / "fonts.css").read_text()}{(S / "style.css").read_text()}</style>
</head>
<body>
"""
html = head + (S / "body.html").read_text().replace("<!--RATGEBER-->", (S / "ratgeber-teaser.html").read_text()).replace("<!--HEADER-->", header("./", "rechner")).replace("<!--FOOTER-->", footer("./")) + "\n<script>\n" + sim + "\n" + (S / "draw.js").read_text().split("if (typeof module")[0] + "\n" + (S / "ui.js").read_text() + "</script>\n</body>\n</html>\n"
(S.parent / "index.html").write_text(html)
print("index.html:", len(html), "Zeichen")
