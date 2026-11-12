"""Baut die Ratgeber-Seiten, die Ratgeber-Übersicht und die Sitemap. Aufruf: python3 build_articles.py"""
import pathlib, json, html, sys, re
ROOT = pathlib.Path(__file__).parent
sys.path.insert(0, str(ROOT / "src"))
from articles import ARTICLES, STAND, BEISPIEL, CHART_BASE
import images
print("Vorschaubilder/Icons neu:", images.build(ARTICLES))
import subprocess
from urllib.parse import quote

from chrome import header, footer, analytics, head_meta

FAV = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 26 26'%3E%3Crect x='5' y='4' width='16' height='20' rx='2.5' fill='none' stroke='%2315212B' stroke-width='2'/%3E%3Crect x='10' y='1.5' width='6' height='3' rx='1' fill='%2315212B'/%3E%3Crect x='8' y='14' width='10' height='7' rx='1' fill='%23E39A0B'/%3E%3C/svg%3E")
# Gleiche Grundstyles wie die Startseite (Farben, Schriften, Kopf, Fuß, Breite), dazu Textseiten-Typografie unter .doc
BASE = (ROOT / "src/fonts.css").read_text() + (ROOT / "src/style.css").read_text()
DOC = """
.about{display:grid;grid-template-columns:minmax(0,1fr) 340px;column-gap:56px;align-items:start}
.about-text{grid-column:1;grid-row:1}.about-body{grid-column:1;grid-row:2}
.about-photo{grid-column:2;grid-row:1/span 2;margin:8px 0 0;position:sticky;top:24px}
.about-photo img{display:block;width:100%;height:auto;border-radius:18px;box-shadow:0 1px 0 var(--line),0 18px 40px -24px rgba(0,0,0,.35);background:var(--meter)}
html.js .about-photo img{opacity:0;transform:translateY(10px) scale(.985);transition:opacity .6s var(--ease-out),transform .6s var(--ease-out)}
html.js .about-photo.in img{opacity:1;transform:none}
@media (max-width:760px){.about{grid-template-columns:minmax(0,1fr)}.about-photo{grid-column:1;grid-row:2;position:static;max-width:300px;margin:6px 0 4px}.about-body{grid-row:3}}
@media (prefers-reduced-motion:reduce){html.js .about-photo img{opacity:1;transform:none;transition:none}}
main.page{padding-block:36px 40px}
.doc{max-width:760px;font-size:18px;line-height:1.65}
.doc .eyebrow{font-family:var(--f-mono);font-size:12.5px;letter-spacing:.08em;text-transform:uppercase;color:var(--sun-ink)}
.doc h1{max-width:none;hyphens:auto;overflow-wrap:break-word;font-family:var(--f-display);font-weight:800;font-stretch:110%;font-size:clamp(32px,5vw,48px);line-height:1.05;margin:10px 0 14px;text-wrap:balance}
.doc h2{hyphens:auto;overflow-wrap:break-word;font-family:var(--f-display);font-weight:800;font-stretch:105%;font-size:25px;line-height:1.2;margin:36px 0 8px;text-wrap:balance}
.doc p,.doc li{max-width:68ch;overflow-wrap:break-word}
.doc .lead{font-size:21px;line-height:1.5;margin:0 0 8px;color:var(--ink)}
.doc .meta,.doc .note{font-size:14px;color:var(--muted)}
.doc .tablewrap{overflow-x:auto;margin:16px 0}
.doc table{border-collapse:collapse;width:100%;min-width:520px;font-size:16px}
.doc th,.doc td{text-align:left;padding:9px 12px 9px 0;border-bottom:1px solid var(--line);vertical-align:top}
.doc th{font-family:var(--f-mono);font-size:12px;letter-spacing:.05em;text-transform:uppercase;color:var(--muted);font-weight:500}
.doc td.num{font-family:var(--f-mono);font-size:15px;white-space:nowrap;font-variant-numeric:tabular-nums}
.doc tr.hl td{background:var(--sun-soft)}
.doc details{border-bottom:1px solid var(--line);padding:12px 0} .doc summary{font-weight:600;cursor:pointer}
.ask{border:1px dashed var(--line);border-radius:10px;padding:20px 22px;margin:32px 0 8px;display:grid;gap:8px;max-width:760px}
.ask b{font-family:var(--f-display);font-stretch:105%;font-size:19px}
.ask span{font-size:16px;color:var(--muted);line-height:1.5}
.ask .btn.ghost{display:inline-block;justify-self:start;opacity:1;cursor:pointer;text-decoration:none;background:transparent;color:var(--ink);border:1.5px solid var(--ink);padding:10px 16px;transition:transform 160ms var(--ease-out),background-color 150ms ease,color 150ms ease}
@media (hover:hover) and (pointer:fine){.ask .btn.ghost:hover{background:var(--ink);color:var(--surface)}}
.ask .btn.ghost:active{transform:scale(0.97)}
@media (prefers-reduced-motion:reduce){.ask .btn.ghost:active{transform:none}}
.cta{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:22px;margin:32px 0;display:grid;gap:10px;max-width:760px}
.cta b{font-family:var(--f-display);font-stretch:105%;font-size:21px}
.cta .btn{display:inline-block;justify-self:start;opacity:1;cursor:pointer;text-decoration:none}
.cta .cta-pro{border-top:1px solid var(--line);padding-top:12px;margin-top:4px;font-size:15px}
.page .rlist{margin:8px 0 0}
.chart{margin:28px 0;max-width:760px;background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:18px 18px 14px}
.chart figcaption{display:grid;gap:2px;margin-bottom:10px}
.chart figcaption b{font-family:var(--f-display);font-stretch:105%;font-size:18px;line-height:1.25}
.chart figcaption span{font-size:14px;color:var(--muted);line-height:1.45}
.chart .c-wide svg,.chart .c-narrow svg{display:block;width:100%;height:auto}
.chart .c-narrow{display:none}
@media (max-width:560px){.chart .c-wide{display:none}.chart .c-narrow{display:block}}
.chart svg .ax{font-size:12px} .chart .slabel{font-size:12px}
.cpanels{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,280px),1fr));gap:14px}
.cpanel svg{display:block;width:100%;height:auto}
.ctitle{font-family:var(--f-mono);font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted)}

html.js .chart .sline{stroke-dasharray:1;stroke-dashoffset:1;transition:stroke-dashoffset 1100ms var(--ease-in-out)}
html.js .chart .sdot,html.js .chart .slabel{opacity:0;transition:opacity 300ms var(--ease-out) 900ms}
html.js .chart .cpanel svg{clip-path:inset(0 100% 0 0);transition:clip-path 1000ms var(--ease-in-out)}
html.js .chart.in .sline{stroke-dashoffset:0} html.js .chart.in .sdot,html.js .chart.in .slabel{opacity:1}
html.js .chart.in .cpanel svg{clip-path:inset(0 0 0 0)}
@media (prefers-reduced-motion:reduce){html.js .chart .sline{stroke-dasharray:none;transition:none} html.js .chart .sdot,html.js .chart .slabel{opacity:1;transition:none} html.js .chart .cpanel svg{clip-path:none;transition:none}}
"""
# Blendet Diagramme einmal ein, wenn sie ins Bild kommen. Ohne JavaScript sind sie sofort sichtbar.
REVEAL = """<script>try{if("IntersectionObserver" in window){document.documentElement.classList.add("js");var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add("in");io.unobserve(e.target);}});},{threshold:0.35});document.querySelectorAll(".chart,.about-photo").forEach(function(c){io.observe(c);});}}catch(e){}</script>"""

# Grafiken aus dem Simulationsmodell rechnen (Node)
_specs = {a["slug"]: a["chart"] for a in ARTICLES if a.get("chart")}
CHARTS = json.loads(subprocess.run(["node", str(ROOT / "src/charts.js")], input=json.dumps({"base": CHART_BASE, "charts": _specs}),
                                   capture_output=True, text=True, check=True).stdout) if _specs else {}

def figure(slug):
    c = ARTICLES_BY[slug].get("chart"); g = CHARTS.get(slug)
    if not c or not g: return ""
    return f'<figure class="chart"><figcaption><b>{html.escape(c["title"])}</b><span>{html.escape(c.get("caption", ""))}</span></figcaption>{g["html"]}</figure>'

ARTICLES_BY = {a["slug"]: a for a in ARTICLES}

def _with_figure(a):
    body, fig = a["body"], figure(a["slug"])
    if not fig: return body
    i = body.find("</p>")
    return body[:i + 4] + fig + body[i + 4:] if i >= 0 else fig + body


def page(title, desc, canonical, main, extra_head="", prefix="../", active="ratgeber", robots=False, og_image=None, og_type="article"):
    base = BASE.replace("url(fonts/", f"url({prefix}fonts/")
    meta = '<meta name="robots" content="noindex">' if robots else (f'<link rel="canonical" href="{canonical}"><meta property="og:title" content="{html.escape(title)}"><meta property="og:description" content="{html.escape(desc)}"><meta property="og:url" content="{canonical}"><meta property="og:type" content="{og_type}"><meta property="og:locale" content="de_DE">')
    return f"""<!doctype html>
<html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{html.escape(title)}</title><meta name="description" content="{html.escape(desc)}">
{meta}
<link rel="icon" href="{FAV}">{head_meta(None if robots else og_image, html.escape(title))}{analytics()}<style>{base}{DOC}</style>{extra_head}</head>
<body>
{header(prefix, active)}
<main class="wrap page">{main}</main>
{footer(prefix)}
{REVEAL}
</body></html>
"""

def ask(a):
    """Kasten „Frage offen?“: öffnet das Mailprogramm mit vorausgefülltem Betreff, kein Fremddienst."""
    subj = quote(f"Frage zu: {a['title']}")
    body = quote(f"Hallo Manuel,\n\nmeine Frage zum Artikel https://speicherklar.de/ratgeber/{a['slug']}.html:\n\n")
    return (f'<div class="ask"><b>Noch eine Frage offen?</b><span>Schreib sie mir. Ich antworte dir per Mail, und was öfter gefragt wird, ergänze ich hier im Artikel, ohne deinen Namen.</span>'
            f'<a class="btn ghost" href="mailto:kontakt@speicherklar.de?subject={subj}&amp;body={body}" data-umami-event="frage-mail">Frage per Mail stellen</a></div>')

CTA = """<div class="cta"><b>Rechne dein eigenes Haus durch</b><span>Postleitzahl, Dachausrichtung und Verbrauch eingeben. Der kostenlose Rechner zeigt dir die wirtschaftlichste Speichergröße, auch für das Szenario EEG-Reform 2027.</span><a class="btn" href="../#rechner" data-umami-event="artikel-zum-rechner" data-umami-event-artikel="{slug}">Zum Rechner</a><span class="cta-pro">Du hast schon ein Angebot? <a href="../pro/" data-umami-event="artikel-zu-pro" data-umami-event-artikel="{slug}">Speicherklar Pro</a> prüft Speicher und PV-Anlage zusammen und zeigt die beste Kombination für dein Dach. Die Einordnung ist kostenlos.</span></div>"""

# Kernzahl auf den Ratgeber-Karten (Feld "kennzahl": {"v": Wert, "t": kurzer Zusatz}); Zahlen müssen im Artikel stehen
def sp(a):
    k = a.get("kennzahl")
    return f'<i class="kz"><em>{k["v"]}</em><small>{k["t"]}</small></i>' if k else ""

# Neueste zuerst (gleiches Datum: später eingetragen = neuer). Gilt für Übersicht und Startseite.
NEWEST = [a for _, a in sorted(enumerate(ARTICLES), key=lambda x: (x[1]["date"], x[0]), reverse=True)]

# „Weiterlesen“: optionales Feld "related" (Liste von Slugs), sonst automatisch nach gemeinsamen Stichwörtern in Titel und Beschreibung
_STOP = {"lohnt", "sich", "dein", "deine", "deinen", "einen", "einer", "speicher", "stromspeicher", "welche", "warum", "wann", "nicht", "kwh", "jahre", "jahren", "beispiel", "bringt", "mehr", "rund"}
def _words(a):
    t = re.sub(r"[^a-zäöüß0-9 ]", " ", (a["title"] + " " + a["desc"]).lower())
    return {w for w in t.split() if len(w) >= 4 and w not in _STOP}
def related(a, n=3):
    picks = [ARTICLES_BY[s] for s in a.get("related", []) if s in ARTICLES_BY and s != a["slug"]]
    if len(picks) < n:
        wa = _words(a)
        rest = [b for b in NEWEST if b["slug"] != a["slug"] and b not in picks]
        rest.sort(key=lambda b: len(wa & _words(b)), reverse=True)  # stabil: bei Gleichstand neueste zuerst
        picks += rest[:n - len(picks)]
    return picks[:n]
def more(a):
    r = related(a)
    if not r: return ""
    li = "".join(f'<li><a href="{b["slug"]}.html">{sp(b)}<b>{b["title"]}</b><span>{b["desc"]}</span></a></li>' for b in r)
    return f'<h2>Weiterlesen</h2><ul class="rlist">{li}</ul>'

out = ROOT / "ratgeber"; out.mkdir(exist_ok=True)
RATGEBER_URL = "https://speicherklar.de/ratgeber/"
def crumbs(*items):
    """Brotkrumen für Google (speicherklar.de › Ratgeber › Artikel). items: (Name, URL)."""
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate((("Speicherklar", "https://speicherklar.de/"),) + items)]}
def ld_tags(*objs):
    return "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in objs)
for a in ARTICLES:
    url = f"https://speicherklar.de/ratgeber/{a['slug']}.html"
    faq_html = "".join(f"<details><summary>{html.escape(q)}</summary><p>{html.escape(x)}</p></details>" for q, x in a["faq"])
    ld = [{"@context": "https://schema.org", "@type": "Article", "headline": a["title"], "description": a["desc"], "datePublished": a["date"], "dateModified": a["date"], "inLanguage": "de", "author": {"@type": "Organization", "name": "Speicherklar"}, "mainEntityOfPage": url},
          {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": x}} for q, x in a["faq"]]},
          crumbs(("Ratgeber", RATGEBER_URL), (a["title"], url))]
    head = ld_tags(*ld)
    main = f"""<article class="doc"><div class="eyebrow">Ratgeber</div><h1>{a['h1']}</h1><p class="lead">{a['lead']}</p><p class="meta">Stand: {STAND}</p>
{_with_figure(a)}{CTA.replace("{slug}", a["slug"])}<h2>Häufige Fragen</h2>{faq_html}{ask(a)}{more(a)}<p class="note" style="margin-top:28px">{BEISPIEL}</p></article>"""
    (out / f"{a['slug']}.html").write_text(page(f"{a['title']} | Speicherklar", a["desc"], url, main, head, og_image=f"img/og/{a['slug']}.png"))

items = "".join(f'<li><a href="{a["slug"]}.html">{sp(a)}<b>{a["title"]}</b><span>{a["desc"]}</span></a></li>' for a in NEWEST)
(out / "index.html").write_text(page("Ratgeber Stromspeicher | Speicherklar", "Artikel rund um Stromspeicher und PV-Anlagen, mit Zahlen aus der Jahressimulation statt aus dem Prospekt. Mit Angebots-Check für PV-Anlage und Speicher.", "https://speicherklar.de/ratgeber/",
    f'<div class="doc"><div class="eyebrow">Ratgeber</div><h1>Stromspeicher, ehrlich gerechnet</h1><p class="lead">Fragen rund um PV-Anlage und Speicher, beantwortet mit Zahlen aus unserer Jahressimulation.</p></div><ul class="rlist">{items}</ul>{CTA.replace("{slug}", "uebersicht")}', ld_tags(crumbs(("Ratgeber", RATGEBER_URL))), og_image="img/og/ratgeber.png", og_type="website"))

# Über mich
ABOUT_URL = "https://speicherklar.de/ueber-mich.html"
ABOUT_HEAD = ('<script type="application/ld+json">{"@context":"https://schema.org","@type":"AboutPage","url":"' + ABOUT_URL + '",'
  '"mainEntity":{"@type":"Person","name":"Manuel Maurer","url":"' + ABOUT_URL + '","image":"https://speicherklar.de/img/manuel-960.jpg",'
  '"homeLocation":{"@type":"Place","name":"Krefeld"},"sameAs":["https://www.instagram.com/speicherklar/"]}}</script>')
(ROOT / "ueber-mich.html").write_text(page("Über mich | Speicherklar", "Wer hinter Speicherklar steckt, warum der Rechner ein ganzes Jahr simuliert und womit sich die Seite finanziert.",
    ABOUT_URL, (ROOT / "src/ueber-mich.html").read_text(), ABOUT_HEAD, prefix="./", active=None, og_image="img/manuel-og.jpg"))

# Methodik: Rechenweg, öffentlicher Code, Unabhängigkeit, Vergleich mit der HTW Berlin
METHODIK_URL = "https://speicherklar.de/methodik.html"
(ROOT / "methodik.html").write_text(page("Methodik: So rechnet Speicherklar | Speicherklar",
    "Wie der Speicherklar-Rechner rechnet, warum der Code öffentlich ist, wer die Seite bezahlt und wie die Ergebnisse zum Unabhängigkeitsrechner der HTW Berlin passen.",
    METHODIK_URL, (ROOT / "src/methodik.html").read_text() + CTA.replace("../", "./").replace("{slug}", "methodik"),
    prefix="./", active=None, og_image="img/og/start.png"))
# Die Sitemap schreibt build.py am Ende (mit Änderungsdatum je Seite), weil es zuletzt läuft.

from chrome import UMAMI_ID
UMAMI_TEXT = """<h2 id="reichweite">7. Reichweitenmessung mit Umami</h2>
<p>Um zu sehen, wie viele Menschen Speicherklar nutzen und welche Seiten gelesen werden, setze ich Umami Cloud ein, einen Dienst der Umami Software, Inc. (USA). Ich habe als Speicherort die EU gewählt. Weil Umami ein US-Unternehmen ist, können Daten trotzdem in die USA übermittelt werden, etwa für Support oder Sicherheit; dafür gelten die EU-Standardvertragsklauseln, die Teil des Vertrags zur Auftragsverarbeitung sind. Umami setzt keine Cookies und speichert nichts auf deinem Gerät.</p>
<p>Erfasst werden die aufgerufene Seite, die Seite, von der du kommst, Browser, Betriebssystem, Gerätetyp, Bildschirmgröße, Land und Sprache sowie einige Ereignisse ohne Inhalt: dass der Rechner benutzt wurde, dass der Mail-Link für Fragen angeklickt wurde, dass der Musterbericht geöffnet, ein Angebot geprüft, der Kauf-Knopf geklickt, Speicherklar Pro freigeschaltet oder ein Bericht gespeichert wurde. Den Inhalt einer Mail sieht Umami nicht. Was du in den Rechner oder den Angebots-Check eingibst, wird nicht übertragen. Deine IP-Adresse wird nur kurz für die Übertragung verarbeitet und nicht in den Statistiken gespeichert. Ich sehe nur zusammengefasste Zahlen und kann daraus keine einzelne Person erkennen.</p>
<p>Rechtsgrundlage ist mein berechtigtes Interesse an einer datensparsamen Auswertung der Nutzung (Art. 6 Abs. 1 lit. f DSGVO, § 25 Abs. 2 Nr. 2 TDDDG). Umami verarbeitet die Daten in meinem Auftrag; es besteht ein Vertrag zur Auftragsverarbeitung nach Art. 28 DSGVO (<a href="https://umami.is/dpa">umami.is/dpa</a>). Die Daten werden nach 6 Monaten gelöscht. Du kannst widersprechen, indem du in deinem Browser Skripte von cloud.umami.is blockierst, oder per Mail an kontakt@speicherklar.de. Mehr in der <a href="https://umami.is/privacy">Datenschutzerklärung von Umami</a>.</p>
"""

# Impressum und Datenschutz mit derselben Kopf- und Fußzeile
for f in ("impressum", "datenschutz"):
    raw = (ROOT / f"src/legal/{f}.html").read_text()
    title = raw.split("<!--TITLE:", 1)[1].split("-->", 1)[0]
    body = raw.split("-->", 1)[1]
    if f == "datenschutz":
        body = body.replace("<!--ANALYTICS-->", UMAMI_TEXT if UMAMI_ID else "")
        if not UMAMI_ID: body = body.replace("<h2>8. Deine Rechte</h2>", "<h2>7. Deine Rechte</h2>")
    (ROOT / f"{f}.html").write_text(page(f"{title} – Speicherklar", title, "", f'<div class="doc">{body}</div>', prefix="./", active=None, robots=True))

# Ratgeber-Liste für die Startseite
(ROOT / "src/ratgeber-teaser.html").write_text("".join(f'<li><a href="ratgeber/{a["slug"]}.html">{sp(a)}<b>{a["title"]}</b><span>{a["desc"]}</span></a></li>' for a in NEWEST[:6]))
print("Artikel:", len(ARTICLES))
for slug, g in CHARTS.items():
    for f in g.get("facts", []): print(f"  Grafik {slug}: {f['label']} -> beste Größe {f['best']} kWh, {f['net']:+} €")
