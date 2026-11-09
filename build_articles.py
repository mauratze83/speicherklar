"""Baut die Ratgeber-Seiten, die Ratgeber-Übersicht und die Sitemap. Aufruf: python3 build_articles.py"""
import pathlib, json, html, sys
ROOT = pathlib.Path(__file__).parent
sys.path.insert(0, str(ROOT / "src"))
from articles import ARTICLES, STAND, BEISPIEL

from chrome import header, footer

FAV = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 26 26'%3E%3Crect x='5' y='4' width='16' height='20' rx='2.5' fill='none' stroke='%2315212B' stroke-width='2'/%3E%3Crect x='10' y='1.5' width='6' height='3' rx='1' fill='%2315212B'/%3E%3Crect x='8' y='14' width='10' height='7' rx='1' fill='%23E39A0B'/%3E%3C/svg%3E")
# Gleiche Grundstyles wie die Startseite (Farben, Schriften, Kopf, Fuß, Breite), dazu Textseiten-Typografie unter .doc
BASE = (ROOT / "src/fonts.css").read_text() + (ROOT / "src/style.css").read_text()
DOC = """
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
.cta{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:22px;margin:32px 0;display:grid;gap:10px;max-width:760px}
.cta b{font-family:var(--f-display);font-stretch:105%;font-size:21px}
.cta .btn{display:inline-block;justify-self:start;opacity:1;cursor:pointer;text-decoration:none}
.page .rlist{margin:8px 0 0}
"""

def page(title, desc, canonical, main, extra_head="", prefix="../", active="ratgeber", robots=False):
    base = BASE.replace("url(fonts/", f"url({prefix}fonts/")
    meta = '<meta name="robots" content="noindex">' if robots else (f'<link rel="canonical" href="{canonical}"><meta property="og:title" content="{html.escape(title)}"><meta property="og:description" content="{html.escape(desc)}"><meta property="og:url" content="{canonical}"><meta property="og:type" content="article"><meta property="og:locale" content="de_DE">')
    return f"""<!doctype html>
<html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{html.escape(title)}</title><meta name="description" content="{html.escape(desc)}">
{meta}
<link rel="icon" href="{FAV}"><style>{base}{DOC}</style>{extra_head}</head>
<body>
{header(prefix, active)}
<main class="wrap page">{main}</main>
{footer(prefix)}
</body></html>
"""

CTA = """<div class="cta"><b>Rechne dein eigenes Haus durch</b><span>Postleitzahl, Dachausrichtung und Verbrauch eingeben. Der kostenlose Rechner zeigt dir die wirtschaftlichste Speichergröße, auch für das Szenario EEG-Reform 2027.</span><a class="btn" href="../#rechner">Zum Rechner</a></div>"""

out = ROOT / "ratgeber"; out.mkdir(exist_ok=True)
urls = [("https://speicherklar.de/", "2026-11-08"), ("https://speicherklar.de/ratgeber/", max(a["date"] for a in ARTICLES))]
for a in ARTICLES:
    url = f"https://speicherklar.de/ratgeber/{a['slug']}.html"
    faq_html = "".join(f"<details><summary>{html.escape(q)}</summary><p>{html.escape(x)}</p></details>" for q, x in a["faq"])
    ld = [{"@context": "https://schema.org", "@type": "Article", "headline": a["title"], "description": a["desc"], "datePublished": a["date"], "dateModified": a["date"], "inLanguage": "de", "author": {"@type": "Organization", "name": "Speicherklar"}, "mainEntityOfPage": url},
          {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": x}} for q, x in a["faq"]]}]
    head = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ld)
    main = f"""<article class="doc"><div class="eyebrow">Ratgeber</div><h1>{a['h1']}</h1><p class="lead">{a['lead']}</p><p class="meta">Stand: {STAND}</p>
{a['body']}{CTA}<h2>Häufige Fragen</h2>{faq_html}<p class="note" style="margin-top:28px">{BEISPIEL}</p></article>"""
    (out / f"{a['slug']}.html").write_text(page(f"{a['title']} | Speicherklar", a["desc"], url, main, head))
    urls.append((url, a["date"]))

items = "".join(f'<li><a href="{a["slug"]}.html"><b>{a["title"]}</b><span>{a["desc"]}</span></a></li>' for a in ARTICLES)
(out / "index.html").write_text(page("Ratgeber Stromspeicher | Speicherklar", "Artikel rund um Stromspeicher und PV-Anlagen, mit Zahlen aus der Jahressimulation statt aus dem Prospekt.", "https://speicherklar.de/ratgeber/",
    f'<div class="doc"><div class="eyebrow">Ratgeber</div><h1>Stromspeicher, ehrlich gerechnet</h1><p class="lead">Fragen rund um PV-Anlage und Speicher, beantwortet mit Zahlen aus unserer Jahressimulation.</p></div><ul class="rlist">{items}</ul>{CTA}'))

(ROOT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    "".join(f"  <url><loc>{u}</loc><lastmod>{d}</lastmod></url>\n" for u, d in urls) + "</urlset>\n")

# Impressum und Datenschutz mit derselben Kopf- und Fußzeile
for f in ("impressum", "datenschutz"):
    raw = (ROOT / f"src/legal/{f}.html").read_text()
    title = raw.split("<!--TITLE:", 1)[1].split("-->", 1)[0]
    body = raw.split("-->", 1)[1]
    (ROOT / f"{f}.html").write_text(page(f"{title} – Speicherklar", title, "", f'<div class="doc">{body}</div>', prefix="./", active=None, robots=True))

# Ratgeber-Liste für die Startseite
(ROOT / "src/ratgeber-teaser.html").write_text("".join(f'<li><a href="ratgeber/{a["slug"]}.html"><b>{a["title"]}</b><span>{a["desc"]}</span></a></li>' for a in ARTICLES[:6]))
print("Artikel:", len(ARTICLES))
