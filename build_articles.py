"""Baut die Ratgeber-Seiten, die Ratgeber-Übersicht und die Sitemap. Aufruf: python3 build_articles.py"""
import pathlib, json, html, sys, re
ROOT = pathlib.Path(__file__).parent
sys.path.insert(0, str(ROOT / "src"))
from articles import ARTICLES, STAND, BEISPIEL, CHART_BASE
import images
print("Vorschaubilder/Icons neu:", images.build(ARTICLES))
import subprocess
from urllib.parse import quote

from chrome import header, footer, analytics, head_meta, video_trigger, video_live, video_tag, VIDEO

FAV = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 26 26'%3E%3Crect x='5' y='4' width='16' height='20' rx='2.5' fill='none' stroke='%2315212B' stroke-width='2'/%3E%3Crect x='10' y='1.5' width='6' height='3' rx='1' fill='%2315212B'/%3E%3Crect x='8' y='14' width='10' height='7' rx='1' fill='%23E39A0B'/%3E%3C/svg%3E")
# Gleiche Grundstyles wie die Startseite (Farben, Schriften, Kopf, Fuß, Breite), dazu Textseiten-Typografie unter .doc
BASE = (ROOT / "src/fonts.css").read_text() + (ROOT / "src/style.css").read_text()
DOC = """
.kwege{list-style:none;padding:0;margin:26px 0 8px;display:grid;gap:12px;max-width:68ch}
.kwege li{background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:16px 18px;display:grid;gap:2px}
.kw-label{font-family:var(--f-mono);font-size:12.5px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
.kw-link{font-family:var(--f-display);font-weight:800;font-stretch:105%;font-size:21px;color:var(--ink);text-decoration-color:var(--sun);text-underline-offset:4px;overflow-wrap:anywhere}
.kw-note{font-size:16px;color:var(--muted)}
.about{display:grid;grid-template-columns:minmax(0,1fr) 340px;column-gap:56px;align-items:start}
.about-text{grid-column:1;grid-row:1}.about-body{grid-column:1;grid-row:2}
.about-photo{grid-column:2;grid-row:1/span 2;margin:8px 0 0;position:sticky;top:88px}
.about-photo img{display:block;width:100%;height:auto;border-radius:18px;box-shadow:0 1px 0 var(--line),0 18px 40px -24px rgba(0,0,0,.35);background:var(--meter)}
html.js .about-photo img{opacity:0;transform:translateY(10px) scale(.985);transition:opacity .6s var(--ease-out),transform .6s var(--ease-out)}
html.js .about-photo.in img{opacity:1;transform:none}
@media (max-width:760px){.about{grid-template-columns:minmax(0,1fr)}.about-photo{grid-column:1;grid-row:2;position:static;max-width:300px;margin:6px 0 4px}.about-body{grid-row:3}}
@media (prefers-reduced-motion:reduce){html.js .about-photo img{opacity:1;transform:none;transition:none}}
.cta .vid-open{justify-self:start}
.sg{max-width:1000px}
.sg-head{max-width:760px}
.sg .eyebrow{font-family:var(--f-mono);font-size:12.5px;letter-spacing:.08em;text-transform:uppercase;color:var(--sun-ink)}
.sg h1{font-family:var(--f-display);font-weight:800;font-stretch:110%;font-size:clamp(32px,5vw,52px);line-height:1.05;margin:10px 0 14px;text-wrap:balance;hyphens:auto}
.sg .lead{font-size:21px;line-height:1.5;margin:0 0 22px}
.sg-video .vid-player{border-radius:14px;width:min(100%,calc((100vh - 110px)*16/9));width:min(100%,calc((100svh - 110px)*16/9));margin:0 auto}
.sg-ph{aspect-ratio:16/9;border-radius:14px;background:#15212B;color:#fff;display:grid;place-content:center;justify-items:center;gap:14px;text-align:center;padding:24px}
.sg-ph b{font-family:var(--f-display);font-weight:800;font-stretch:110%;font-size:clamp(22px,4vw,40px);line-height:1.1}
.sg-ph span{font-family:var(--f-mono);font-size:12.5px;letter-spacing:.1em;text-transform:uppercase;color:#F2B33D}
.sg-cta{display:flex;flex-wrap:wrap;align-items:center;gap:6px 18px;margin:20px 0 8px}.sg-cta .facts{margin-top:0}
.sg-steps{padding-left:1.2em}.sg-steps li{margin:0 0 10px}
.sg-ex{margin:24px 0;max-width:760px;background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:18px;display:grid;gap:12px}
.sg-meter{background:var(--meter);color:var(--meter-digit);border-radius:8px;padding:16px;display:flex;flex-wrap:wrap;gap:12px 28px;align-items:center;font-family:var(--f-mono);font-weight:700}
.sg-num{display:inline-flex;align-items:center;gap:8px}.sg-num small{font-size:14px;font-weight:500}
.sg-meter .dg{display:inline-flex;gap:3px}.sg-plus{font-size:28px}
.sg-ex figcaption{font-size:14px;color:var(--muted);line-height:1.5}
.sg-end{background:#15212B;color:#fff;border-radius:14px;padding:26px 24px;margin:36px 0 8px;display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:16px;max-width:1000px}
.sg-end b{font-family:var(--f-display);font-weight:800;font-stretch:105%;font-size:clamp(22px,3.4vw,30px);line-height:1.15}
main.page{padding-block:36px 40px}
.doc{max-width:760px;font-size:18px;line-height:1.65}
.doc .eyebrow{font-family:var(--f-mono);font-size:12.5px;letter-spacing:.08em;text-transform:uppercase;color:var(--sun-ink)}
.doc h1{max-width:none;hyphens:auto;overflow-wrap:break-word;font-family:var(--f-display);font-weight:800;font-stretch:110%;font-size:clamp(32px,5vw,48px);line-height:1.05;margin:10px 0 14px;text-wrap:balance}
.doc h2{hyphens:auto;overflow-wrap:break-word;font-family:var(--f-display);font-weight:800;font-stretch:105%;font-size:25px;line-height:1.2;margin:36px 0 8px;text-wrap:balance}
.doc p,.doc li{max-width:68ch;overflow-wrap:break-word}
.doc .lead{font-size:21px;line-height:1.5;margin:0 0 8px;color:var(--ink)}
.doc .meta,.doc .note{font-size:14px;color:var(--muted)}
.doc .tablewrap{overflow-x:auto;margin:16px 0}
.doc table{border-collapse:collapse;width:100%;min-width:520px;font-size:16px}.doc table.fit{min-width:0}
.doc th,.doc td{text-align:left;padding:9px 12px 9px 0;border-bottom:1px solid var(--line);vertical-align:top}
.doc th{font-family:var(--f-mono);font-size:12px;letter-spacing:.05em;text-transform:uppercase;color:var(--muted);font-weight:500}
.doc td.num{font-family:var(--f-mono);font-size:15px;white-space:nowrap;font-variant-numeric:tabular-nums}
.doc tr.hl td{background:var(--sun-soft);font-weight:700}
.doc tr.hl td:first-child{box-shadow:inset 4px 0 0 var(--sun);padding-left:12px}
.art{display:grid;grid-template-columns:minmax(0,760px) minmax(0,1fr);column-gap:48px;align-items:start}
.kbox{position:sticky;top:88px;margin-top:8px;background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:20px;display:grid;gap:14px}
.kbox .cap{font-family:var(--f-mono);font-size:11.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted)}
.kbox .kmeter{background:var(--meter);color:var(--meter-digit);border-radius:8px;padding:14px;display:flex;flex-wrap:wrap;align-items:center;gap:4px 6px;font-family:var(--f-mono);font-weight:700;font-size:17px}
.kbox .kmeter .wheel{font-size:30px}
.kbox .kmeter .dg{display:inline-flex;gap:3px}
.kbox p{margin:0;font-size:15.5px;line-height:1.45}
.kbox .btn{opacity:1;cursor:pointer;text-align:center}
.kbox small{font-size:13px;color:var(--muted);line-height:1.4}
@media (max-width:1020px){.art{grid-template-columns:minmax(0,1fr)}.kbox{display:none}}
.hbars{display:grid;gap:10px;margin:4px 0 2px}
.hbar{display:grid;grid-template-columns:minmax(64px,auto) minmax(0,1fr) auto;gap:12px;align-items:center;font-family:var(--f-mono);font-size:14px;font-variant-numeric:tabular-nums}
.hbar .hl{color:var(--muted);line-height:1.2} .hbar .hl small{display:block;font-size:11px}
.hbar .ht{height:24px;display:block}
.hbar .ht i{display:block;height:100%;border-radius:0 4px 4px 0;background:var(--c-imp);transform-origin:left center}
.hbar .hv{font-weight:700;white-space:nowrap}
.hbar.best .hl,.hbar.best .hv{color:var(--sun-ink);font-weight:700} .hbar.best .ht i{background:var(--sun)}
.hbar.mark .hl{color:var(--ink)} .hbar.mark .ht i{outline:1.5px solid var(--ink);outline-offset:2px}
html.js .chart .hbar .ht i{transform:scaleX(0);transition:transform 700ms var(--ease-out)}
html.js .chart.in .hbar .ht i{transform:none}
html.js .chart .hbar:nth-child(2) .ht i{transition-delay:50ms}html.js .chart .hbar:nth-child(3) .ht i{transition-delay:100ms}html.js .chart .hbar:nth-child(4) .ht i{transition-delay:150ms}html.js .chart .hbar:nth-child(5) .ht i{transition-delay:200ms}html.js .chart .hbar:nth-child(n+6) .ht i{transition-delay:250ms}
@media (prefers-reduced-motion:reduce){html.js .chart .hbar .ht i{transform:none;transition:none}}
.doc details{border-bottom:1px solid var(--line);padding:12px 0} .doc summary{font-weight:600;cursor:pointer}
.ask{border:1px dashed var(--line);border-radius:10px;padding:20px 22px;margin:32px 0 8px;display:grid;gap:8px;max-width:760px}
.ask b{font-family:var(--f-display);font-stretch:105%;font-size:19px}
.ask span{font-size:16px;color:var(--muted);line-height:1.5}
.ask .btn.ghost{display:inline-block;justify-self:start;opacity:1;cursor:pointer;text-decoration:none;background:transparent;color:var(--ink);border:1.5px solid var(--ink);padding:10px 16px;transition:transform 160ms var(--ease-out),background-color 150ms ease,color 150ms ease}
@media (hover:hover) and (pointer:fine){.ask .btn.ghost:hover{background:var(--ink);color:var(--surface)}}
.ask .btn.ghost:active{transform:scale(0.97)}
@media (prefers-reduced-motion:reduce){.ask .btn.ghost:active{transform:none}}
.ask .ask-addr{font-size:14px;color:var(--muted);line-height:1.45}
.ask .ask-addr a{color:var(--sun-ink)}
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
    return f'<figure class="chart"><figcaption><b>{html.escape(c["title"])}</b> <span>{html.escape(c.get("caption", ""))}</span></figcaption>{g["html"]}</figure>'

ARTICLES_BY = {a["slug"]: a for a in ARTICLES}

def _eur(v):
    return ("+" if v > 0 else "−" if v < 0 else "") + f"{abs(v):,}".replace(",", ".") + " €"

def _val(v, unit):
    """Balkenwert: ohne Einheit als Euro mit Vorzeichen, sonst Zahl mit Einheit (z. B. "kWh")."""
    return _eur(v) if not unit else f"{v:,}".replace(",", ".") + " " + unit

def bars(a):
    """Waagerechte Balken (Feld "bars": title, caption, rows [[Name, Wert, Zusatz?]], best = Name der besten Zeile, mark = Name der Zeile aus dem Angebot, unit = Einheit statt €)."""
    b = a.get("bars")
    if not b: return ""
    top = max(v for _, v, *_ in b["rows"]) or 1
    unit = b.get("unit")
    rows = ""
    for name, v, *extra in b["rows"]:
        cls = " best" if name == b.get("best") else " mark" if name == b.get("mark") else ""
        sub = f" <small>{html.escape(extra[0])}</small>" if extra else ""
        rows += (f'<div class="hbar{cls}"><span class="hl">{html.escape(name)}{sub}</span> '
                 f'<span class="ht"><i style="width:{max(1, round(v / top * 100, 1))}%"></i></span> <span class="hv">{_val(v, unit)}</span></div>\n')
    alt = html.escape(b["title"] + ": " + ", ".join(f"{n} {_val(v, unit)}" for n, v, *_ in b["rows"]))
    return (f'<figure class="chart"><figcaption><b>{html.escape(b["title"])}</b> <span>{html.escape(b.get("caption", ""))}</span></figcaption>'
            f'<div class="hbars" role="img" aria-label="{alt}">{rows}</div></figure>')

def kbox(a):
    """Mitlaufende Karte neben dem Artikel: Kernzahl im Zählerkasten und der Weg zum Rechner."""
    k = a.get("kennzahl")
    if not k: return ""
    parts = re.split(r"(\d+)", k["v"])
    meter = "".join(('<span class="dg">' + "".join(f'<span class="wheel">{d}</span>' for d in t) + "</span>") if t.isdigit() else html.escape(t) for t in parts if t)
    return (f'<aside class="kbox" aria-label="Kurz gesagt"><span class="cap">Kurz gesagt</span> <div class="kmeter" role="img" aria-label="{html.escape(k["v"])}">{meter}</div>'
            f'<p>{html.escape(k["t"][:1].upper() + k["t"][1:])}.</p>'
            f'<a class="btn btn-on" href="../#rechner" data-umami-event="artikel-zum-rechner" data-umami-event-artikel="{a["slug"]}">Mit deinen Zahlen rechnen</a> '
            f'<small>Kostenlos und ohne Anmeldung.</small></aside>')

def _with_figure(a):
    body, fig = a["body"], figure(a["slug"])
    if not fig: return body
    i = body.find("</p>")
    return body[:i + 4] + fig + body[i + 4:] if i >= 0 else fig + body

def _body(a):
    return _with_figure(a).replace("<!--BARS-->", bars(a))


def page(title, desc, canonical, main, extra_head="", prefix="../", active="ratgeber", robots=False, og_image=None, og_type="article"):
    base = BASE.replace("url(fonts/", f"url({prefix}fonts/")
    meta = '<meta name="robots" content="noindex">' if robots else (f'<link rel="canonical" href="{canonical}"><meta property="og:title" content="{html.escape(title)}"><meta property="og:description" content="{html.escape(desc)}"><meta property="og:url" content="{canonical}"><meta property="og:type" content="{og_type}"><meta property="og:locale" content="de_DE">')
    return f"""<!doctype html>
<html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{html.escape(title)}</title><meta name="description" content="{html.escape(desc)}">
{meta}
{head_meta(None if robots else og_image, html.escape(title))}{analytics()}<style>{base}{DOC}</style>{extra_head}</head>
<body>
{header(prefix, active)}
<main class="wrap page">{main}</main>
{footer(prefix)}
{REVEAL}
</body></html>
"""

def ask(a):
    """Kasten „Frage offen?“: öffnet das Mailprogramm mit vorausgefülltem Betreff, kein Fremddienst.
    Gezählt wird per umami.track im onclick, nicht per data-umami-event: Umami würde den Klick sonst abfangen und
    den mailto-Link erst nach dem Senden öffnen, und Safari blockiert das Öffnen des Mailprogramms dann."""
    subj = quote(f"Frage zu: {a['title']}")
    body = quote(f"Hallo Manuel,\n\nmeine Frage zum Artikel https://speicherklar.de/ratgeber/{a['slug']}.html:\n\n")
    return (f'<div class="ask"><b>Noch eine Frage offen?</b> <span>Schreib sie mir. Ich antworte dir per Mail, und was öfter gefragt wird, ergänze ich hier im Artikel, ohne deinen Namen.</span> '
            f'<a class="btn ghost" href="mailto:kontakt@speicherklar.de?subject={subj}&amp;body={body}" onclick="try{{window.umami&amp;&amp;umami.track(\'frage-mail\')}}catch(e){{}}">Frage per Mail stellen</a> '
            f'<small class="ask-addr">Öffnet sich kein Mailprogramm? Schreib an <a href="mailto:kontakt@speicherklar.de">kontakt@speicherklar.de</a>.</small></div>')

CTA = """<div class="cta"><b>Rechne dein eigenes Haus durch</b> <span>Postleitzahl, Dachausrichtung und Verbrauch eingeben. Der kostenlose Rechner zeigt dir die wirtschaftlichste Speichergröße, auch für das Szenario EEG-Reform 2027.</span> <a class="btn" href="../#rechner" data-umami-event="artikel-zum-rechner" data-umami-event-artikel="{slug}">Zum Rechner</a> <span class="cta-pro">Du hast schon ein Angebot? <a href="../pro/" data-umami-event="artikel-zu-pro" data-umami-event-artikel="{slug}">Speicherklar Pro</a> prüft Speicher und PV-Anlage zusammen und zeigt die beste Kombination für dein Dach. Die Einordnung ist kostenlos.</span>""" + video_trigger("artikel") + "</div>"

# Kernzahl auf den Ratgeber-Karten (Feld "kennzahl": {"v": Wert, "t": kurzer Zusatz}); Zahlen müssen im Artikel stehen
def sp(a):
    k = a.get("kennzahl")
    return f'<i class="kz"><em>{k["v"]}</em> <small>{k["t"]}</small></i> ' if k else ""

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
    li = "\n".join(f'<li><a href="{b["slug"]}.html">{sp(b)}<b>{b["title"]}</b> <span>{b["desc"]}</span></a></li>' for b in r)
    return f'<h2>Weiterlesen</h2><ul class="rlist">{li}</ul>'

out = ROOT / "ratgeber"; out.mkdir(exist_ok=True)
RATGEBER_URL = "https://speicherklar.de/ratgeber/"
def _de(d): y, m, t = d.split("-"); return f"{int(t)}.{int(m)}.{y}"
def datum(a):
    """Sichtbares Datum mit <time>: 'Aktualisiert am …', wenn das Feld updated gesetzt ist, sonst 'Veröffentlicht am …'."""
    if a.get("updated") and a["updated"] != a["date"]:
        return f'Aktualisiert am <time datetime="{a["updated"]}">{_de(a["updated"])}</time>'
    return f'Veröffentlicht am <time datetime="{a["date"]}">{_de(a["date"])}</time>'
def crumbs(*items):
    """Brotkrumen für Google (speicherklar.de › Ratgeber › Artikel). items: (Name, URL)."""
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate((("Speicherklar", "https://speicherklar.de/"),) + items)]}
def ld_tags(*objs):
    return "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in objs)
for a in ARTICLES:
    url = f"https://speicherklar.de/ratgeber/{a['slug']}.html"
    faq_html = "".join(f"<details><summary>{html.escape(q)}</summary><p>{html.escape(x)}</p></details>" for q, x in a["faq"])
    ld = [{"@context": "https://schema.org", "@type": "Article", "headline": a["title"], "description": a["desc"], "datePublished": a["date"], "dateModified": a.get("updated", a["date"]), "inLanguage": "de",
           "author": {"@type": "Person", "name": "Manuel Maurer", "url": "https://speicherklar.de/ueber-mich.html"},
           "publisher": {"@type": "Organization", "@id": "https://speicherklar.de/#org", "name": "Speicherklar", "url": "https://speicherklar.de/", "logo": {"@type": "ImageObject", "url": "https://speicherklar.de/img/icon-512.png"}},
           "isBasedOn": "https://speicherklar.de/methodik.html", "image": f"https://speicherklar.de/img/og/{a['slug']}.png", "mainEntityOfPage": url},
          {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": x}} for q, x in a["faq"]]},
          crumbs(("Ratgeber", RATGEBER_URL), (a["title"], url))]
    head = ld_tags(*ld)
    main = f"""<div class="art"><article class="doc"><div class="eyebrow">Ratgeber</div><h1>{a['h1']}</h1><p class="lead">{a['lead']}</p><p class="meta">{datum(a)} · Von <a href="../ueber-mich.html">Manuel Maurer</a> · <a href="#annahmen">Annahmen</a> · <a href="../methodik.html">Rechenweg</a></p>
{_body(a)}{CTA.replace("{slug}", a["slug"])}<h2>Häufige Fragen</h2>{faq_html}{ask(a)}{more(a)}<p class="note" id="annahmen" style="margin-top:28px">{BEISPIEL}</p></article>{kbox(a)}</div>"""
    seo = f"{a.get('seo_title', a['title'])} | Speicherklar"
    if len(seo) > 60:
        print(f"WARNUNG: Titel {len(seo)} Zeichen (max. 60), Feld seo_title setzen: {a['slug']}")
    (out / f"{a['slug']}.html").write_text(page(seo, a["desc"], url, main, head, og_image=f"img/og/{a['slug']}.png"))

items = "\n".join(f'<li><a href="{a["slug"]}.html">{sp(a)}<b>{a["title"]}</b> <span>{a["desc"]}</span></a></li>' for a in NEWEST)
(out / "index.html").write_text(page("Ratgeber Stromspeicher | Speicherklar", "Artikel rund um Stromspeicher und PV-Anlagen, mit Zahlen aus der Jahressimulation statt aus dem Prospekt. Mit Angebots-Check für PV-Anlage und Speicher.", "https://speicherklar.de/ratgeber/",
    f'<div class="doc"><div class="eyebrow">Ratgeber</div><h1>Stromspeicher, ehrlich gerechnet</h1><p class="lead">Fragen rund um PV-Anlage und Stromspeicher (auch Batteriespeicher, PV-Speicher oder Solarspeicher genannt), beantwortet mit Zahlen aus meiner Jahressimulation.</p></div><ul class="rlist">{items}</ul>{CTA.replace("{slug}", "uebersicht")}', ld_tags(crumbs(("Ratgeber", RATGEBER_URL))), og_image="img/og/ratgeber.png", og_type="website"))

# Über mich
ABOUT_URL = "https://speicherklar.de/ueber-mich.html"
ABOUT_HEAD = ('<script type="application/ld+json">{"@context":"https://schema.org","@type":"AboutPage","url":"' + ABOUT_URL + '",'
  '"mainEntity":{"@type":"Person","name":"Manuel Maurer","url":"' + ABOUT_URL + '","image":"https://speicherklar.de/img/manuel-960.jpg",'
  '"homeLocation":{"@type":"Place","name":"Krefeld"},"sameAs":["https://www.instagram.com/speicherklar/","https://www.linkedin.com/in/manuel-maurer-36821295/"]}}</script>')
(ROOT / "ueber-mich.html").write_text(page("Über mich | Speicherklar", "Wer hinter Speicherklar steckt, warum der Rechner ein ganzes Jahr simuliert und womit sich die Seite finanziert.",
    ABOUT_URL, (ROOT / "src/ueber-mich.html").read_text(), ABOUT_HEAD, prefix="./", active="ueber", og_image="img/manuel-og.jpg"))

# Kontakt
KONTAKT_URL = "https://speicherklar.de/kontakt.html"
KONTAKT_HEAD = ('<script type="application/ld+json">{"@context":"https://schema.org","@type":"ContactPage","url":"' + KONTAKT_URL + '",'
  '"mainEntity":{"@type":"Organization","name":"Speicherklar","url":"https://speicherklar.de/","email":"kontakt@speicherklar.de",'
  '"sameAs":["https://www.instagram.com/speicherklar/"]}}</script>')
(ROOT / "kontakt.html").write_text(page("Kontakt | Speicherklar", "So erreichst du Speicherklar: per Mail an kontakt@speicherklar.de, auf Instagram oder LinkedIn. Fragen zum Rechner, zu Pro oder Fehler gefunden? Schreib mir.",
    KONTAKT_URL, (ROOT / "src/kontakt.html").read_text(), KONTAKT_HEAD, prefix="./", active="kontakt", og_type="website"))

# So funktioniert Speicherklar: Landingpage mit Erklärvideo (/so-gehts/). Eine Bitte: Rechner starten.
# Ohne Video (VIDEO["quer"] leer in chrome.py): Platzhalter, noindex, nicht in der Sitemap, nirgends verlinkt.
SG_URL = "https://speicherklar.de/so-gehts/"
_cfg = (ROOT / "src/pro-config.js").read_text()
_cv = lambda k: re.search(k + r'\s*:\s*"?([^",\n/]*)"?', _cfg).group(1).strip()
import datetime as _dt
_de2 = lambda d: ".".join(reversed(d.split("-")))
_intro_end = (_dt.date.fromisoformat(_cv("introUntil")) + _dt.timedelta(days=1)).isoformat()
SG_FAQ = [
    ("Was kostet der Rechner?", "Nichts. Ohne Anmeldung, ohne E-Mail, ohne Telefonnummer."),
    ("Was ist der Unterschied zwischen Rechner und Speicherklar Pro?", "Der Rechner sagt dir, welche Speichergröße zu deinem Haus passt. Speicherklar Pro nimmt dein konkretes Angebot und zeigt dir, welche PV-Anlage und welcher Speicher am besten zusammenpassen, was du bei der passenden Größe sparst und was du deinen Installateur fragen solltest."),
    ("Ruft mich danach jemand an?", "Nein. Ich gebe keine Daten weiter und arbeite mit keinem Installateur zusammen."),
    ("Wie genau ist das?", "An 30 gemessenen Häusern lag die Autarkie mit 10 kWh Speicher gemessen bei 76 %, gerechnet bei 77 %. Mit Wärmepumpe rechnet der Rechner die Autarkie rund 4 Punkte zu hoch, den Zugewinn durch den Speicher trifft er."),
    ("Was rechnet der Rechner nicht?", "Notstrom, Verschattung, Alterung des Speichers und dynamische Stromtarife. Wenn das bei dir eine große Rolle spielt, nimm das Ergebnis als Ausgangspunkt für deine Fragen an den Installateur, nicht als letzte Antwort."),
    ("Brauche ich schon ein Angebot?", "Für den Rechner nicht. Für den Angebots-Check in Speicherklar Pro ja."),
]
_sg_desc = "Stromspeicher-Rechner ohne Anmeldung und Speicherklar Pro: die zweite Rechnung zu deinem PV-Angebot. Keine Provision, kein Abo. Erklärt in 75 Sekunden."
if video_live():
    _sg_video = video_tag("../", preload="metadata").replace('<video ', '<video data-ort="so-gehts" ', 1)
else:
    _sg_video = '<div class="sg-ph" role="img" aria-label="Platzhalter für das Erklärvideo"><b>Verkäufer rechnen mit Juli.<br>Ich rechne mit November.</b> <span>Video folgt</span></div>'
_sg = (ROOT / "src/so-gehts.html").read_text()
for k, v in {"{{VIDEO}}": _sg_video, "{{PRO_PRICE}}": _cv("price"), "{{PRO_REGULAR}}": _cv("regularPrice"), "{{PRO_INTRO_DE}}": _de2(_cv("introUntil")),
             "{{PRO_INTRO_END}}": _intro_end, "{{PRO_PUBLIC}}": _cv("publicFrom"), "{{PRO_PUBLIC_DE}}": _de2(_cv("publicFrom")), "{{PRO_DAYS}}": _cv("accessDays"),
             "{{FAQ}}": "".join(f"<details><summary>{html.escape(q)}</summary><p>{html.escape(x)}</p></details>" for q, x in SG_FAQ)}.items():
    assert k in _sg, k
    _sg = _sg.replace(k, v)
_sg_ld = [{"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": x}} for q, x in SG_FAQ]},
          crumbs(("So funktioniert Speicherklar", SG_URL))]
if video_live():
    _sg_ld.insert(0, {"@context": "https://schema.org", "@type": "VideoObject", "name": "So funktioniert Speicherklar", "description": _sg_desc,
        "thumbnailUrl": "https://speicherklar.de/" + (VIDEO["bild"] or "img/og/start.png"), "uploadDate": VIDEO["datum"], "duration": VIDEO["dauer"],
        "contentUrl": "https://speicherklar.de/" + VIDEO["quer"], "inLanguage": "de"})
(ROOT / "so-gehts").mkdir(exist_ok=True)
(ROOT / "so-gehts/index.html").write_text(page("So funktioniert Speicherklar: Rechner und Angebots-Check", _sg_desc, SG_URL, _sg, ld_tags(*_sg_ld),
    active="sogehts", robots=not video_live(), og_image=VIDEO["bild"] or "img/og/start.png", og_type="website"))

# Methodik: Rechenweg, öffentlicher Code, Unabhängigkeit, Vergleich mit der HTW Berlin
METHODIK_URL = "https://speicherklar.de/methodik.html"
(ROOT / "methodik.html").write_text(page("Methodik: So rechnet Speicherklar | Speicherklar",
    "Wie der Speicherklar-Rechner rechnet, warum der Code öffentlich ist, wer die Seite bezahlt und wie die Ergebnisse zum Unabhängigkeitsrechner der HTW Berlin passen.",
    METHODIK_URL, (ROOT / "src/methodik.html").read_text() + CTA.replace("../", "./").replace("{slug}", "methodik"),
    prefix="./", active=None, og_image="img/og/start.png"))
# Die Sitemap schreibt build.py am Ende (mit Änderungsdatum je Seite), weil es zuletzt läuft.

from chrome import UMAMI_ID, KLARA
# Klara (KI-Hilfe): erscheint in der Datenschutzerklärung erst, wenn KLARA["aktiv"] True ist.
# Angaben zu Anthropic am 17.11.2026 geprüft: DPA mit SCCs ist Teil der Commercial Terms, API-Daten kein Training,
# Löschung innerhalb von 30 Tagen (privacy.claude.com). Bei Änderungen der Bedingungen nachziehen. Nicht anwaltlich geprüft.
KLARA_TEXT = """<h2 id="klara">{N}. Klara (KI-Hilfe)</h2>
<p>Klara ist ein Chat, in dem eine KI Fragen zu Speicherklar, zum Rechner und zu PV-Anlagen mit Speicher beantwortet. Die Antworten erzeugt ein Sprachmodell (Claude von Anthropic). Sie können Fehler enthalten und ersetzen kein Angebot und keine Fachberatung. Wenn du Klara öffnest, fragt dein Browser nur ab, ob Klara gerade erreichbar ist.</p>
<p>Sobald du eine Frage eintippst, löst dein Browser eine kleine Rechenaufgabe, damit Bots den Chat nicht missbrauchen. Wenn du eine Frage stellst, schickt dein Browser die Frage, den bisherigen Verlauf dieses Gesprächs, die Adresse der Seite und auf der Startseite die Werte und Ergebnisse, die gerade im Rechner stehen (von der Postleitzahl nur die erste Ziffer), an einen kleinen Dienst, den ich bei Cloudflare betreibe (Cloudflare, Inc., 101 Townsend St, San Francisco, CA 94107, USA). Dabei wird auch deine IP-Adresse verarbeitet. Der Dienst gibt Frage, Verlauf und Werte an die Schnittstelle von Anthropic weiter (Anthropic, PBC, San Francisco, USA), die die Antwort erzeugt.</p>
<p>Ich speichere deine Fragen und Klaras Antworten nicht. Der Dienst bei Cloudflare speichert nur Summen ohne Inhalt, je Monat: Kosten, Anzahl der Fragen, die Themen-Kategorie je Frage, welche Knöpfe Klara gezeigt hat und wie oft Antworten mit dem Daumen als hilfreich oder nicht hilfreich markiert wurden. Dazu schätzt Klara bei jeder Antwort selbst ein, ob sie die Frage beantworten konnte; fehlte ihr Wissen, notiert sie das Thema als kurzes allgemeines Stichwort in eigenen Worten (zum Beispiel „Notstrom nachrüsten“), ohne Zahlen, Namen oder Angaben zu dir. Damit verbessere ich Klaras Wissen. Gegen Missbrauch zählt er außerdem je Tag die Fragen zu einem nicht umkehrbaren Kürzel (Hash) deiner IP-Adresse; dieser Zähler wird nach zwei Tagen gelöscht. Den Verlauf deines Gesprächs speichert dein Browser im sessionStorage dieses Tabs, damit er beim Seitenwechsel erhalten bleibt, dazu am Handy, ob der Hinweis „Frag Klara“ schon gezeigt wurde. Er ist weg, sobald du den Tab schließt, auf „Neu starten“ tippst oder 30 Minuten lang nichts fragst. Wenn du auf „Frage an Manuel mailen“ tippst, übernimmt dein Mailprogramm den Verlauf in eine neue Mail; ob du sie abschickst, entscheidest du.</p>
<p>Anthropic verarbeitet die Daten in meinem Auftrag; es besteht ein Vertrag zur Auftragsverarbeitung nach Art. 28 DSGVO. Für die Übermittlung in die USA gelten die EU-Standardvertragsklauseln aus diesem Vertrag (<a href="https://www.anthropic.com/legal">anthropic.com/legal</a>). Anthropic nutzt Daten aus der Schnittstelle nach eigenen Angaben nicht zum Trainieren seiner Modelle und löscht Fragen und Antworten innerhalb von 30 Tagen. Mehr in den <a href="https://www.anthropic.com/legal/privacy">Datenschutzhinweisen von Anthropic</a>. Rechtsgrundlage ist mein berechtigtes Interesse, deine Fragen zu Speicherklar zu beantworten und den Chat vor Missbrauch zu schützen (Art. 6 Abs. 1 lit. f DSGVO); den Verlauf im Browser speichere ich nur, weil er für den Chat, den du nutzen willst, nötig ist (§ 25 Abs. 2 Nr. 2 TDDDG).</p>
"""
KLARA_EVENTS = "dass Klara geöffnet, eine Frage gestellt (ohne Inhalt) oder ein Knopf in Klaras Antwort angeklickt wurde, "
UMAMI_TEXT = """<h2 id="reichweite">{N}. Reichweitenmessung mit Umami</h2>
<p>Um zu sehen, wie viele Menschen Speicherklar nutzen und welche Seiten gelesen werden, setze ich Umami Cloud ein, einen Dienst der Umami Software, Inc. (USA). Ich habe als Speicherort die EU gewählt. Weil Umami ein US-Unternehmen ist, können Daten trotzdem in die USA übermittelt werden, etwa für Support oder Sicherheit; dafür gelten die EU-Standardvertragsklauseln, die Teil des Vertrags zur Auftragsverarbeitung sind. Umami setzt keine Cookies und speichert nichts auf deinem Gerät. Nur wenn du eine Adresse mit dem Zusatz <code>?ich=1</code> aufrufst (gedacht für mich als Betreiber), legt die Seite in deinem Browser den Eintrag <code>umami.disabled</code> an; dann zählt Umami deine Besuche nicht mehr. <code>?ich=0</code> entfernt ihn wieder.</p>
<p>Erfasst werden die aufgerufene Seite, die Seite, von der du kommst, Browser, Betriebssystem, Gerätetyp, Bildschirmgröße, Land und Sprache sowie einige Ereignisse ohne Inhalt: dass der Rechner benutzt wurde, dass das Erklärvideo geöffnet, gestartet oder bis zum Ende angesehen wurde, <!--KLARA_EVENTS-->dass der Mail-Link für Fragen angeklickt wurde, dass der Musterbericht geöffnet, ein Angebot geprüft, der Hinweis auf den Bericht unter der Ampel oder der Kauf-Knopf geklickt, Speicherklar Pro freigeschaltet oder ein Bericht gespeichert wurde. Den Inhalt einer Mail sieht Umami nicht. Was du in den Rechner oder den Angebots-Check eingibst, wird nicht übertragen. Beim geprüften Angebot zählt Umami nur die Farben der vier Ampel-Punkte (grün, gelb, rot), keine Werte aus deinem Angebot. Deine IP-Adresse wird nur kurz für die Übertragung verarbeitet und nicht in den Statistiken gespeichert. Ich sehe nur zusammengefasste Zahlen und kann daraus keine einzelne Person erkennen.</p>
<p>Rechtsgrundlage ist mein berechtigtes Interesse an einer datensparsamen Auswertung der Nutzung (Art. 6 Abs. 1 lit. f DSGVO, § 25 Abs. 2 Nr. 2 TDDDG). Umami verarbeitet die Daten in meinem Auftrag; es besteht ein Vertrag zur Auftragsverarbeitung nach Art. 28 DSGVO (<a href="https://umami.is/dpa">umami.is/dpa</a>). Die Daten werden nach 6 Monaten gelöscht. Du kannst widersprechen, indem du in deinem Browser Skripte von cloud.umami.is blockierst, oder per Mail an kontakt@speicherklar.de. Mehr in der <a href="https://umami.is/privacy">Datenschutzerklärung von Umami</a>.</p>
"""

# Impressum und Datenschutz mit derselben Kopf- und Fußzeile
for f in ("impressum", "datenschutz"):
    raw = (ROOT / f"src/legal/{f}.html").read_text()
    title = raw.split("<!--TITLE:", 1)[1].split("-->", 1)[0]
    body = raw.split("-->", 1)[1]
    if f == "datenschutz":
        # Abschnitte, die nur erscheinen, wenn der Dienst läuft; ab 7 durchnummeriert, danach „Deine Rechte“
        extra = ([KLARA_TEXT] if KLARA["aktiv"] else []) + ([UMAMI_TEXT.replace("<!--KLARA_EVENTS-->", KLARA_EVENTS if KLARA["aktiv"] else "")] if UMAMI_ID else [])
        extra = [x.replace("{N}", str(7 + i)) for i, x in enumerate(extra)]
        body = body.replace("<!--ANALYTICS-->", "".join(extra)).replace("<h2>8. Deine Rechte</h2>", f"<h2>{7 + len(extra)}. Deine Rechte</h2>")
        if KLARA["aktiv"]: body = body.replace("MailerLite schickt dir den Schlüssel per Mail.</p>", "MailerLite schickt dir den Schlüssel per Mail. Wenn du Klara, der KI-Hilfe, eine Frage stellst, geht sie über einen Dienst bei Cloudflare an Anthropic.</p>")
    (ROOT / f"{f}.html").write_text(page(f"{title} – Speicherklar", title, "", f'<div class="doc">{body}</div>', prefix="./", active=None, robots=True))

# Ratgeber-Liste für die Startseite
_FEAT = ' class="feat"'
(ROOT / "src/ratgeber-teaser.html").write_text("\n".join(f'<li{_FEAT if i == 0 else ""}><a href="ratgeber/{a["slug"]}.html">{sp(a)}<b>{a["title"]}</b> <span>{a["desc"]}</span></a></li>' for i, a in enumerate(NEWEST[:6])))
print("Artikel:", len(ARTICLES))
for slug, g in CHARTS.items():
    for f in g.get("facts", []): print(f"  Grafik {slug}: {f['label']} -> beste Größe {f['best']} kWh, {f['net']:+} €")
