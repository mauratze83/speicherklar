"""Erzeugt Vorschaubilder für geteilte Links (Open Graph, 1200×630) und App-Icons.

Wird von build_articles.py aufgerufen. Bilder werden nur neu gebaut, wenn sich ihr Inhalt
geändert hat (Signatur in img/og/sig.json) oder die Datei fehlt.
"""
import base64, hashlib, html, json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
IMG = ROOT / "img"
OG = IMG / "og"

def _font(name):
    return "data:font/woff2;base64," + base64.b64encode((ROOT / "fonts" / name).read_bytes()).decode()

CSS = f"""
@font-face{{font-family:"Archivo";src:url({_font('archivo-var.woff2')}) format("woff2");font-weight:100 900;font-stretch:62% 125%}}
@font-face{{font-family:"Source Sans 3";src:url({_font('source-sans-3-latin-400-normal.woff2')});font-weight:400}}
@font-face{{font-family:"Source Sans 3";src:url({_font('source-sans-3-latin-600-normal.woff2')});font-weight:600}}
@font-face{{font-family:"JetBrains Mono";src:url({_font('jetbrains-mono-latin-500-normal.woff2')});font-weight:500}}
*{{box-sizing:border-box;margin:0}}
body{{width:1200px;height:630px;overflow:hidden;background:#EDF0F2;color:#15212B;font-family:"Source Sans 3",sans-serif}}
.card{{width:1200px;height:630px;padding:64px 80px 56px;display:flex;flex-direction:column}}
.top{{display:flex;justify-content:space-between;align-items:center;font-family:"JetBrains Mono";font-size:24px;letter-spacing:.06em;text-transform:uppercase;color:#56666F}}
.brand{{display:flex;gap:14px;align-items:center;font-family:"Archivo";font-stretch:118%;font-weight:800;font-size:34px;letter-spacing:.01em;text-transform:none;color:#15212B}}
.main{{flex:1;display:flex;flex-direction:column;justify-content:center;gap:22px}}
h1{{font-family:"Archivo";font-weight:800;font-stretch:106%;font-size:68px;line-height:1.04;letter-spacing:-.01em;max-width:1000px;text-wrap:balance}}
.kz{{display:flex;align-items:baseline;gap:20px}}
.kz b{{font-family:"Archivo";font-weight:800;font-stretch:85%;font-size:64px;line-height:1;color:#8A5A00}}
.kz span{{font-size:30px;color:#56666F;max-width:640px;line-height:1.25}}
.sub{{font-size:34px;line-height:1.3;color:#56666F;max-width:960px}}
.sub em{{font-style:normal;color:#8A5A00;font-weight:600}}
.foot{{display:flex;justify-content:space-between;align-items:center;font-size:26px;color:#56666F}}
.foot b{{font-family:"Archivo";font-weight:800;font-stretch:105%;color:#15212B;background:#E39A0B;padding:10px 18px;border-radius:10px;font-size:26px}}
.bar{{height:10px;background:#E39A0B;margin:30px -80px -56px}}
"""

LOGO = ('<svg width="{s}" height="{s}" viewBox="0 0 26 26"><rect x="5" y="4" width="16" height="20" rx="2.5" fill="none" stroke="#15212B" stroke-width="2"/>'
        '<rect x="10" y="1.5" width="6" height="3" rx="1" fill="#15212B"/><rect x="8" y="14" width="10" height="7" rx="1" fill="#E39A0B"/></svg>')

ICON = ('<div style="width:{s}px;height:{s}px;background:#15212B;display:flex;align-items:center;justify-content:center">'
        '<svg width="{i}" height="{i}" viewBox="0 0 26 26"><rect x="5.6" y="4.4" width="14.8" height="19" rx="2.6" fill="none" stroke="#E6ECF1" stroke-width="1.7"/>'
        '<rect x="10" y="1.7" width="6" height="2.6" rx="0.9" fill="#E6ECF1"/><rect x="8.2" y="13.6" width="9.6" height="7.4" rx="1" fill="#E39A0B"/>'
        '<rect x="8.2" y="9.4" width="9.6" height="2.8" rx="1" fill="#E39A0B" opacity=".45"/></svg></div>')

def card_html(kicker, title, kz=None, sub=None):
    mid = f"<h1>{html.escape(title)}</h1>"
    if kz:
        mid += f'<div class="kz"><b>{html.escape(kz["v"])}</b><span>{html.escape(kz["t"])}</span></div>'
    if sub:
        mid += f'<p class="sub">{sub}</p>'
    return (f'<div class="card"><div class="top"><div class="brand">{LOGO.format(s=40)}Speicherklar</div><div>{html.escape(kicker)}</div></div>'
            f'<div class="main">{mid}</div>'
            f'<div class="foot"><span>Kostenloser Stromspeicher-Rechner mit echten Sonnendaten</span><b>speicherklar.de</b></div><div class="bar"></div></div>')

def build(articles):
    """articles: Liste mit slug, title, kennzahl. Gibt nichts zurück; schreibt img/og/*.png und die Icons."""
    OG.mkdir(parents=True, exist_ok=True)
    sigf = OG / "sig.json"
    try:
        sig = json.loads(sigf.read_text())
    except Exception:
        sig = {}
    jobs = []  # (Pfad, html, breite, höhe)
    def want(path, content, w, h):
        key = path.relative_to(ROOT).as_posix()
        hsh = hashlib.sha1((content + CSS[-400:]).encode()).hexdigest()[:12]
        if sig.get(key) != hsh or not path.exists():
            jobs.append((path, content, w, h)); sig[key] = hsh
    want(OG / "start.png", card_html("PV-Anlage planen", "Lohnt sich dein Stromspeicher?",
         sub="Verkäufer rechnen mit Juli. <em>Wir rechnen mit November.</em> Jahressimulation für deine Region, Ausrichtung und deinen Verbrauch."), 1200, 630)
    want(OG / "ratgeber.png", card_html("Ratgeber", "Stromspeicher, ehrlich gerechnet",
         sub="Fragen rund um PV-Anlage und Speicher, beantwortet mit Zahlen aus der Jahressimulation."), 1200, 630)
    for a in articles:
        want(OG / f"{a['slug']}.png", card_html("Ratgeber", a["title"], kz=a.get("kennzahl")), 1200, 630)
    for name, s, i in (("apple-touch-icon.png", 180, 112), ("icon-192.png", 192, 120), ("icon-512.png", 512, 320),
                       ("icon-maskable-512.png", 512, 250), ("favicon-32.png", 32, 26)):
        want(IMG / name, ICON.format(s=s, i=i), s, s)
    if not jobs:
        return 0
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page()
        for path, content, w, h in jobs:
            pg.set_viewport_size({"width": w, "height": h})
            pg.set_content(f"<html><head><style>{CSS}body{{width:{w}px;height:{h}px}}</style></head><body>{content}</body></html>")
            pg.evaluate("document.fonts.ready.then(()=>1)")
            pg.wait_for_timeout(120)
            pg.screenshot(path=str(path))
        b.close()
    # Apple sucht das Icon zusätzlich im Hauptordner
    (ROOT / "apple-touch-icon.png").write_bytes((IMG / "apple-touch-icon.png").read_bytes())
    sigf.write_text(json.dumps(sig, indent=1, sort_keys=True))
    return len(jobs)
