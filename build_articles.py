"""Baut die Ratgeber-Seiten, die Ratgeber-Übersicht und die Sitemap. Aufruf: python3 build_articles.py"""
import pathlib, json, html, sys
ROOT = pathlib.Path(__file__).parent
sys.path.insert(0, str(ROOT / "src"))
from articles import ARTICLES, STAND, BEISPIEL

fonts = (ROOT / "src/fonts.css").read_text().replace("url(fonts/", "url(../fonts/")
FAV = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 26 26'%3E%3Crect x='5' y='4' width='16' height='20' rx='2.5' fill='none' stroke='%2315212B' stroke-width='2'/%3E%3Crect x='10' y='1.5' width='6' height='3' rx='1' fill='%2315212B'/%3E%3Crect x='8' y='14' width='10' height='7' rx='1' fill='%23E39A0B'/%3E%3C/svg%3E")
CSS = fonts + """
:root{--bg:#EDF0F2;--surface:#fff;--ink:#15212B;--muted:#56666F;--line:#CBD3DA;--sun:#E39A0B;--sun-ink:#8A5A00;--sun-soft:#FBEFD6}
@media (prefers-color-scheme:dark){:root{--bg:#0F161C;--surface:#17212A;--ink:#E6ECF1;--muted:#97A7B3;--line:#2A3742;--sun:#F2B33D;--sun-ink:#F2B33D;--sun-soft:#2E2614;color-scheme:dark}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:18px/1.65 "Source Sans 3","Segoe UI",system-ui,sans-serif}
.wrap{max-width:760px;margin:0 auto;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
header{border-bottom:1px solid var(--line)}
header .wrap{display:flex;justify-content:space-between;align-items:center;gap:16px;padding-block:14px;flex-wrap:wrap}
.brand{font-family:"Archivo","Arial Narrow",sans-serif;font-weight:800;font-stretch:118%;font-size:21px;display:flex;gap:10px;align-items:center;color:var(--ink);text-decoration:none}
nav{display:flex;gap:18px;font-size:15px} nav a{color:var(--muted);text-decoration:none} nav a:hover{color:var(--ink)}
a{color:var(--sun-ink)}
article{padding-block:36px 24px}
.eyebrow{font-family:"JetBrains Mono",monospace;font-size:12.5px;letter-spacing:.08em;text-transform:uppercase;color:var(--sun-ink)}
h1{font-family:"Archivo","Arial Narrow",sans-serif;font-weight:800;font-stretch:110%;font-size:clamp(32px,5vw,48px);line-height:1.05;margin:10px 0 14px;text-wrap:balance}
h2{font-family:"Archivo","Arial Narrow",sans-serif;font-weight:800;font-stretch:105%;font-size:25px;line-height:1.2;margin:36px 0 8px;text-wrap:balance}
.lead{font-size:21px;line-height:1.5;margin:0 0 8px}
.meta{font-size:14px;color:var(--muted)}
.tablewrap{overflow-x:auto;margin:16px 0}
table{border-collapse:collapse;width:100%;min-width:520px;font-size:16px}
th,td{text-align:left;padding:9px 12px 9px 0;border-bottom:1px solid var(--line);vertical-align:top}
th{font-family:"JetBrains Mono",monospace;font-size:12px;letter-spacing:.05em;text-transform:uppercase;color:var(--muted);font-weight:500}
td.num{font-family:"JetBrains Mono",monospace;font-size:15px;white-space:nowrap;font-variant-numeric:tabular-nums}
tr.hl td{background:var(--sun-soft)}
.cta{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:22px;margin:32px 0;display:grid;gap:10px}
.cta b{font-family:"Archivo","Arial Narrow",sans-serif;font-stretch:105%;font-size:21px}
.btn{display:inline-block;justify-self:start;background:var(--ink);color:var(--surface);font-weight:700;padding:11px 18px;border-radius:8px;text-decoration:none}
details{border-bottom:1px solid var(--line);padding:12px 0} summary{font-weight:600;cursor:pointer}
.note{font-size:14px;color:var(--muted)}
.list{display:grid;gap:14px;padding:0;list-style:none}
.list a{display:block;background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:18px;text-decoration:none;color:var(--ink)}
.list b{font-family:"Archivo","Arial Narrow",sans-serif;font-stretch:105%;font-size:20px;display:block}
.list span{color:var(--muted);font-size:16px}
footer{border-top:1px solid var(--line);color:var(--muted);font-size:14px;margin-top:24px}
footer .wrap{padding-block:20px 32px}
"""
LOGO = '<svg width="24" height="24" viewBox="0 0 26 26" aria-hidden="true"><rect x="5" y="4" width="16" height="20" rx="2.5" fill="none" stroke="currentColor" stroke-width="2"/><rect x="10" y="1.5" width="6" height="3" rx="1" fill="currentColor"/><rect x="8" y="14" width="10" height="7" rx="1" fill="#E39A0B"/></svg>'

def page(title, desc, canonical, main, extra_head=""):
    return f"""<!doctype html>
<html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{html.escape(title)}</title><meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{canonical}"><meta property="og:title" content="{html.escape(title)}"><meta property="og:description" content="{html.escape(desc)}"><meta property="og:url" content="{canonical}"><meta property="og:type" content="article"><meta property="og:locale" content="de_DE">
<link rel="icon" href="{FAV}"><style>{CSS}</style>{extra_head}</head>
<body><header><div class="wrap"><a class="brand" href="../">{LOGO}Speicherklar</a><nav><a href="../#rechner">Rechner</a><a href="./">Ratgeber</a><a href="https://www.instagram.com/speicherklar/" target="_blank" rel="noopener">Instagram</a></nav></div></header>
<main class="wrap">{main}</main>
<footer><div class="wrap">Speicherklar ist eine Schätzung, keine Anlagen- oder Finanzberatung. · <a href="https://www.instagram.com/speicherklar/" target="_blank" rel="noopener">Instagram @speicherklar</a> · <a href="../impressum.html">Impressum</a> · <a href="../datenschutz.html">Datenschutz</a></div></footer>
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
    main = f"""<article><div class="eyebrow">Ratgeber</div><h1>{a['h1']}</h1><p class="lead">{a['lead']}</p><p class="meta">Stand: {STAND}</p>
{a['body']}{CTA}<h2>Häufige Fragen</h2>{faq_html}<p class="note" style="margin-top:28px">{BEISPIEL}</p></article>"""
    (out / f"{a['slug']}.html").write_text(page(f"{a['title']} | Speicherklar", a["desc"], url, main, head))
    urls.append((url, a["date"]))

items = "".join(f'<li><a href="{a["slug"]}.html"><b>{a["title"]}</b><span>{a["desc"]}</span></a></li>' for a in ARTICLES)
(out / "index.html").write_text(page("Ratgeber Stromspeicher | Speicherklar", "Artikel rund um Stromspeicher und PV-Anlagen, mit Zahlen aus der Jahressimulation statt aus dem Prospekt.", "https://speicherklar.de/ratgeber/",
    f'<article><div class="eyebrow">Ratgeber</div><h1>Stromspeicher, ehrlich gerechnet</h1><p class="lead">Fragen rund um PV-Anlage und Speicher, beantwortet mit Zahlen aus unserer Jahressimulation.</p><ul class="list">{items}</ul>{CTA}</article>'))

(ROOT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    "".join(f"  <url><loc>{u}</loc><lastmod>{d}</lastmod></url>\n" for u, d in urls) + "</urlset>\n")

# Ratgeber-Liste für die Startseite
(ROOT / "src/ratgeber-teaser.html").write_text("".join(f'<li><a href="ratgeber/{a["slug"]}.html"><b>{a["title"]}</b><span>{a["desc"]}</span></a></li>' for a in ARTICLES[:6]))
print("Artikel:", len(ARTICLES))
