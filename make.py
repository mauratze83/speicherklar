"""Erzeugt Profilbild und Karussell-Slides für @speicherklar als PNG (Playwright)."""
import pathlib, json, os, sys, base64
from playwright.sync_api import sync_playwright

# Aufruf: SPEICHERKLAR_SITE=<Checkout von main> python3 make.py [Name-Präfix ...]
# Ohne Präfix werden alle Posts gebaut, sonst nur die, deren Name mit einem Präfix beginnt (z. B. post4).
HERE = pathlib.Path(__file__).parent
SITE = pathlib.Path(os.environ.get("SPEICHERKLAR_SITE", HERE.parent / "speicherklar-site"))
ONLY = sys.argv[1:]
OUT = HERE / "out"
OUT.mkdir(exist_ok=True)
_FD = SITE / "fonts"
def _f(name): return "data:font/woff2;base64," + base64.b64encode((_FD / name).read_bytes()).decode()

BASE_CSS = f"""
@font-face{{font-family:"Archivo";src:url({_f('archivo-var.woff2')}) format("woff2");font-weight:100 900;font-stretch:62% 125%}}
@font-face{{font-family:"Source Sans 3";src:url({_f('source-sans-3-latin-400-normal.woff2')});font-weight:400}}
@font-face{{font-family:"Source Sans 3";src:url({_f('source-sans-3-latin-600-normal.woff2')});font-weight:600}}
@font-face{{font-family:"Source Sans 3";src:url({_f('source-sans-3-latin-700-normal.woff2')});font-weight:700}}
@font-face{{font-family:"JetBrains Mono";src:url({_f('jetbrains-mono-latin-500-normal.woff2')});font-weight:500}}
@font-face{{font-family:"JetBrains Mono";src:url({_f('jetbrains-mono-latin-700-normal.woff2')});font-weight:700}}
:root{{--bg:#EDF0F2;--surface:#fff;--ink:#15212B;--muted:#56666F;--line:#CBD3DA;--sun:#E39A0B;--sun-ink:#8A5A00;--pos:#2E7D5B;--neg:#B4412F;--meter:#1B1F23;--red:#C9302C}}
*{{box-sizing:border-box;margin:0}}
body{{width:1080px;height:1350px;background:var(--bg);color:var(--ink);font-family:"Source Sans 3",sans-serif;overflow:hidden}}
.slide{{width:1080px;height:1350px;padding:120px 130px 100px;display:flex;flex-direction:column;position:relative}}
.slide.dark{{background:var(--ink);color:#E6ECF1}}
.top{{display:flex;justify-content:space-between;align-items:center;font-family:"JetBrains Mono";font-size:26px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted)}}
.dark .top{{color:#97A7B3}}
.brand{{display:flex;gap:14px;align-items:center;font-family:"Archivo";font-stretch:118%;font-weight:800;font-size:34px;letter-spacing:.01em;text-transform:none;color:var(--ink)}}
.dark .brand{{color:#E6ECF1}}
.main{{flex:1;display:flex;flex-direction:column;justify-content:center;gap:36px}}
h1{{font-family:"Archivo";font-weight:800;font-stretch:108%;font-size:112px;line-height:1.0;text-wrap:balance;letter-spacing:-.01em}}
h1 em{{font-style:normal;font-stretch:72%;color:var(--sun-ink)}}
.dark h1 em{{color:#F2B33D}}
h2{{font-family:"Archivo";font-weight:800;font-stretch:105%;font-size:74px;line-height:1.05;text-wrap:balance}}
p{{font-size:44px;line-height:1.35;max-width:900px}}
.muted{{color:var(--muted)}} .dark .muted{{color:#97A7B3}}
.foot{{display:flex;justify-content:space-between;align-items:center;font-family:"JetBrains Mono";font-size:26px;color:var(--muted)}}
.dark .foot{{color:#97A7B3}}
.swipe{{font-family:"Archivo";font-stretch:100%;font-weight:700;font-size:30px;color:var(--sun-ink)}}
.dark .swipe{{color:#F2B33D}}
.big{{font-family:"Archivo";font-weight:800;font-stretch:88%;font-size:220px;line-height:.9;font-variant-numeric:tabular-nums}}
.pair{{display:grid;grid-template-columns:1fr 1fr;gap:28px}}
.card{{background:var(--surface);border:2px solid var(--line);border-radius:20px;padding:36px}}
.card .k{{font-size:30px;color:var(--muted)}}
.card .v{{font-family:"Archivo";font-weight:800;font-stretch:90%;font-size:96px;line-height:1.05;font-variant-numeric:tabular-nums}}
.card .d{{font-size:28px;color:var(--muted)}}
.wheels{{display:flex;gap:10px}}
.wheel{{font-family:"JetBrains Mono";font-weight:700;font-size:120px;width:96px;text-align:center;background:linear-gradient(#000 0,#2a2f35 12%,#15191d 50%,#2a2f35 88%,#000 100%);color:#F3F1EA;border-radius:8px;line-height:1.25}}
.main svg{{max-width:100%;height:auto}}
.src{{font-size:24px;color:var(--muted);line-height:1.35}}
.dark .src{{color:#97A7B3}}
.sum{{list-style:none;padding:0;display:grid;gap:22px}}
.sum li{{font-size:44px;line-height:1.25;display:grid;grid-template-columns:56px 1fr;gap:18px;align-items:baseline}}
.sum li b{{font-family:"Archivo";font-weight:800;font-size:44px;color:var(--sun-ink)}}
.promise{{font-size:46px;line-height:1.3;color:var(--muted);max-width:820px}}
.cta{{display:inline-block;background:var(--sun);color:var(--ink);font-family:"Archivo";font-weight:800;font-stretch:105%;font-size:48px;padding:22px 36px;border-radius:16px}}
"""

LOGO = """<svg width="{s}" height="{s}" viewBox="0 0 26 26"><rect x="5" y="4" width="16" height="20" rx="2.5" fill="none" stroke="{c}" stroke-width="2"/><rect x="10" y="1.5" width="6" height="3" rx="1" fill="{c}"/><rect x="8" y="14" width="10" height="7" rx="1" fill="#E39A0B"/></svg>"""

def frame(body, n, total, topic, dark=False, swipe=True):
    c = "#E6ECF1" if dark else "#15212B"
    return f"""<div class="slide{' dark' if dark else ''}">
<div class="top"><div class="brand">{LOGO.format(s=40,c=c)}Speicherklar</div><div>{topic}</div></div>
<div class="main">{body}</div>
<div class="foot"><div>@speicherklar</div><div>{'<span class="swipe">weiter →</span>&nbsp;&nbsp;' if swipe and n < total else ''}{n}/{total}</div></div>
</div>"""

def monthly_chart(w0, w8):
    W, H, pl, pb, pt = 912, 560, 70, 56, 20
    iw, ih = W - pl, H - pb - pt
    bw = iw / 12
    months = "JFMAMJJASOND"
    s = f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="JetBrains Mono" font-size="24">'
    for t in (0, 25, 50, 75, 100):
        y = pt + ih * (1 - t / 100)
        s += f'<line x1="{pl}" x2="{W}" y1="{y}" y2="{y}" stroke="#CBD3DA" stroke-dasharray="{"" if t==0 else "4 6"}"/><text x="{pl-12}" y="{y+8}" text-anchor="end" fill="#56666F">{t}</text>'
    for i in range(12):
        x = pl + i * bw
        for j, (val, col) in enumerate(((w0[i], "#B9C3CB"), (w8[i], "#E39A0B"))):
            h = ih * val / 100
            s += f'<rect x="{x + bw*0.14 + j*bw*0.37}" y="{pt+ih-h}" width="{bw*0.33}" height="{h}" rx="4" fill="{col}"/>'
        hl = i in (5, 11)
        s += f'<text x="{x+bw/2}" y="{H-16}" text-anchor="middle" fill="{"#15212B" if hl else "#56666F"}" font-weight="{700 if hl else 500}">{months[i]}</text>'
    return s + "</svg>"

def sweep_chart(sued, ow):
    W, H, pl, pb, pt = 912, 560, 100, 56, 30
    vals = [v for _, v in sued + ow]
    top, bot = 3000, -2000
    iw, ih = W - pl, H - pb - pt
    y = lambda v: pt + ih * (top - v) / (top - bot)
    bw = iw / 12
    s = f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="JetBrains Mono" font-size="24">'
    for t in range(bot, top + 1, 1000):
        s += f'<line x1="{pl}" x2="{W}" y1="{y(t)}" y2="{y(t)}" stroke="#CBD3DA" stroke-dasharray="{"" if t==0 else "4 6"}"/><text x="{pl-12}" y="{y(t)+8}" text-anchor="end" fill="#56666F">{"−" if t<0 else ""}{abs(t):,}</text>'.replace(",", ".")
    for i in range(12):
        x = pl + i * bw
        for j, (series, col) in enumerate(((sued, "#15212B"), (ow, "#E39A0B"))):
            v = series[i][1]
            s += f'<rect x="{x + bw*0.14 + j*bw*0.37}" y="{min(y(0), y(v))}" width="{bw*0.33}" height="{max(2, abs(y(v)-y(0)))}" rx="3" fill="{col}"/>'
        s += f'<text x="{x+bw/2}" y="{H-16}" text-anchor="middle" fill="#56666F">{i+1}</text>'
    return s + "</svg>"

def legend(items):
    return '<div style="display:flex;gap:40px;font-size:30px">' + "".join(
        f'<span style="display:flex;align-items:center;gap:12px"><i style="width:26px;height:26px;border-radius:5px;background:{c};display:inline-block"></i>{t}</span>' for c, t in items) + "</div>"

def wheels(n):
    s = str(n)
    return '<div class="wheels">' + "".join(f'<span class="wheel">{d}</span>' for d in s) + "</div>"

D = json.loads((pathlib.Path(__file__).parent / "numbers.json").read_text())
fmt = lambda v: f"{v:,}".replace(",", ".")
de = lambda v: str(v).replace(".", ",")

posts = {}

# ---------- Post 1: Speicher im Winter (7 Slides) ----------
m0 = [r[2] for r in D["monat0"]]; m8 = [r[2] for r in D["monat8"]]
g = [r[0] for r in D["monat8"]]; l = [r[1] for r in D["monat8"]]
S_ = D["sued_heute"]; s15 = S_["sweep"][14]
def summary(items):
    return '<ul class="sum">' + "".join(f"<li><b>{i}</b><span>{t}</span></li>" for i, t in enumerate(items, 1)) + "</ul>"
T = 7; tp = "Speicher im Winter"
posts["post1-juni-dezember"] = [
  frame(f'<h1>Juni <em>{m8[5]} %</em>. Dezember <em>{m8[11]} %</em>.</h1><p class="promise">Was ein Stromspeicher im Winter wirklich schafft.</p>', 1, T, tp),
  frame('<h2>Viele kaufen den Speicher für den Winter.</h2><p>Genau da hilft er am wenigsten. Gerechnet für ein typisches Haus mit 9 kWp und 8 kWh Speicher.</p>', 2, T, tp),
  frame(f'<h2>Sommer fast autark, Winter nicht</h2><p class="muted" style="font-size:32px">Anteil Strom vom eigenen Dach je Monat, in Prozent</p>{monthly_chart(m0, m8)}{legend([("#B9C3CB","ohne Speicher"),("#E39A0B","mit 8 kWh")])}', 3, T, tp),
  frame(f'<h2>Im Dezember fehlt die Sonne</h2><div class="pair"><div class="card"><div class="k">Erzeugung</div><div class="v">{g[11]}</div><div class="d">kWh im Dezember</div></div><div class="card"><div class="k">Verbrauch</div><div class="v">{l[11]}</div><div class="d">kWh im Dezember</div></div></div><p>Was nicht erzeugt wird, kann kein Speicher speichern.</p>', 4, T, tp),
  frame(f'<h2>Größer rettet den Winter nicht</h2><p>Mit 15 statt 8 kWh steigt die Autarkie übers Jahr nur von {S_["s8"]["aut"]} auf {s15[4]} %. Der Speicher kostet aber fast doppelt so viel.</p>', 5, T, tp),
  frame(f'<h2>Kurz gesagt</h2>' + summary(["Im Sommer ist das Haus fast autark.", f"Im Dezember deckt es nur {m8[11]} %.", "Ein größerer Speicher ändert daran kaum etwas.", f"Beste Größe für dieses Haus: {S_['best']} kWh."]), 6, T, tp),
  frame('<h1>Wie sieht das <em>bei deinem Dach</em> aus?</h1><p>Kostenloser Rechner mit Sonnendaten für deine Region. Link in der Bio.</p><div><span class="cta">speicherklar.de</span></div><p class="src">Beispiel: Ruhrgebiet, 9 kWp Süd 35°, 4.500 kWh/Jahr, 8 kWh Speicher. Sonnendaten PVGIS 2014–2023 (EU-Kommission), eigene Simulation.</p>', 7, T, tp, dark=True),
]

# ---------- Post 2: Süd gegen Ost-West (8 Slides) ----------
O_ = D["ow_heute"]
T = 8; tp = "Süd oder Ost-West"
sw_s = [(r[0], r[3]) for r in S_["sweep"]][:12]; sw_o = [(r[0], r[3]) for r in O_["sweep"]][:12]
posts["post2-sued-ost-west"] = [
  frame('<h1>Ost-West braucht <em>weniger Speicher.</em></h1><p class="promise">Warum oft 4 kWh reichen, wo 8 angeboten werden.</p>', 1, T, tp),
  frame('<h2>Ein zu großer Speicher kostet schnell 2.000 € mehr.</h2><p>Und bringt dir fast nichts zurück. Gerechnet für zwei gleiche Häuser, eins mit Süd-, eins mit Ost-West-Dach.</p>', 2, T, tp),
  frame(f'<h2>Ost-West erzeugt weniger</h2><div class="pair"><div class="card"><div class="k">Süd, 9 kWp</div><div class="v">{fmt(round(S_["gen"],-1))}</div><div class="d">kWh im Jahr</div></div><div class="card"><div class="k">Ost-West, 9 kWp</div><div class="v">{fmt(round(O_["gen"],-1))}</div><div class="d">kWh im Jahr</div></div></div><p>Rund ein Fünftel weniger bei gleicher Leistung.</p>', 3, T, tp),
  frame(f'<h2>Aber zur richtigen Zeit</h2><p>Ost-West liefert morgens und abends, wenn das Haus Strom braucht. Ohne Speicher bleiben {O_["ev0"]} statt {S_["ev0"]} % des Solarstroms im Haus.</p><p class="muted">Mittags bleibt weniger übrig, was in den Speicher könnte.</p>', 4, T, tp),
  frame(f'<h2>Gewinn nach 15 Jahren</h2><p class="muted" style="font-size:32px">in Euro, je Speichergröße von 1 bis 12 kWh</p>{sweep_chart(sw_s, sw_o)}{legend([("#15212B","Süd"),("#E39A0B","Ost-West")])}', 5, T, tp),
  frame(f'<h2>Der teure Fehler: 8 kWh</h2><div class="pair"><div class="card"><div class="k">{O_["best"]} kWh Speicher</div><div class="v">{de(O_["bestPay"])} J.</div><div class="d">bis er sich bezahlt hat</div></div><div class="card"><div class="k">8 kWh Speicher</div><div class="v">{de(O_["s8"]["pay"])} J.</div><div class="d">bis er sich bezahlt hat</div></div></div><p>2.000 € mehr für {O_["s8"]["save"]-O_["bestSave"]} € Ersparnis im Jahr.</p>', 6, T, tp),
  frame('<h2>Kurz gesagt</h2>' + summary([f"Bei Süd rechnen sich {S_['best']} kWh am besten.", f"Bei Ost-West reichen {O_['best']} kWh.", "Ost-West nutzt mehr Strom direkt.", "Lieber mehr Module als mehr Speicher."]), 7, T, tp),
  frame(f'<h1>Welche Größe passt <em>zu deinem Dach?</em></h1><p>Ausrichtung, Neigung und Verbrauch eingeben. Link in der Bio.</p><div><span class="cta">speicherklar.de</span></div><p class="src">Beispiel: Ruhrgebiet, 9 kWp, 35°, 4.500 kWh/Jahr, Speicher 500 €/kWh, Strom {D["price"]} ct, Einspeisung 7,70 ct, 15 Jahre. Sonnendaten PVGIS (EU-Kommission).</p>', 8, T, tp, dark=True),
]

# ---------- Post 3: EEG-Reform (7 Slides) ----------
H_, R_ = D["sued_heute"], D["sued_reform"]
T = 7; tp = "EEG-Reform 2027"
posts["post3-eeg-reform"] = [
  frame('<h1>EEG-Reform: <em>Speicher rechnet sich schneller.</em></h1><p class="promise">Was der Kabinettsentwurf für neue PV-Anlagen heißt.</p>', 1, T, tp),
  frame('<h2>Wer 2027 eine PV-Anlage plant, rechnet mit neuen Regeln.</h2><p>Und dann sieht die Speicherfrage ganz anders aus.</p>', 2, T, tp),
  frame('<h2>Was geplant ist</h2>' + summary(["Keine feste Vergütung mehr nach einer Übergangszeit.", "Ins Netz darf höchstens die Hälfte der Anlagenleistung."]) + '<p class="muted">Kabinettsentwurf vom 29.07.2026. Noch nicht beschlossen.</p>', 3, T, tp),
  frame(f'<h2>Die 50-%-Grenze kostet Strom</h2>{wheels(round(R_["curt0"],-1))}<p>So viele kWh im Jahr gingen bei 9 kWp ohne Speicher verloren. Rund {round(R_["curt0"]/R_["gen"]*100)} % des Solarstroms.</p>', 4, T, tp),
  frame(f'<h2>Der Speicher bezahlt sich schneller</h2><div class="pair"><div class="card"><div class="k">EEG heute</div><div class="v">{de(H_["bestPay"])} J.</div><div class="d">bester Speicher {H_["best"]} kWh</div></div><div class="card"><div class="k">Reform</div><div class="v" style="color:var(--pos)">{de(R_["bestPay"])} J.</div><div class="d">bester Speicher {R_["best"]} kWh</div></div></div><p>Jede selbst genutzte kWh spart {D["price"]} ct. Eingespeist bringt sie nichts mehr.</p>', 5, T, tp),
  frame('<h2>Kurz gesagt</h2>' + summary(["Einspeisen lohnt sich kaum noch.", f"Ohne Speicher verpuffen rund {fmt(round(R_['curt0'],-1))} kWh im Jahr.", f"Amortisation: {de(R_['bestPay'])} statt {de(H_['bestPay'])} Jahre.", "Der Speicher darf etwas größer sein."]), 6, T, tp),
  frame(f'<h1>Beide Szenarien <em>für dein Haus.</em></h1><p>Im Rechner zwischen EEG heute und Reform umschalten. Link in der Bio.</p><div><span class="cta">speicherklar.de</span></div><p class="src">Beispiel: Ruhrgebiet, 9 kWp Süd 35°, 4.500 kWh/Jahr, Speicher 500 €/kWh, Strom {D["price"]} ct. Reform laut Kabinettsentwurf vom 29.07.2026, Stand November 2026.</p>', 7, T, tp, dark=True),
]

PROFILE = f"""<div style="width:1080px;height:1080px;background:#15212B;display:flex;align-items:center;justify-content:center">
<svg width="620" height="620" viewBox="0 0 26 26"><rect x="5.6" y="4.4" width="14.8" height="19" rx="2.6" fill="none" stroke="#E6ECF1" stroke-width="1.7"/><rect x="10" y="1.7" width="6" height="2.6" rx="0.9" fill="#E6ECF1"/><rect x="8.2" y="13.6" width="9.6" height="7.4" rx="1" fill="#E39A0B"/><rect x="8.2" y="9.4" width="9.6" height="2.8" rx="1" fill="#E39A0B" opacity=".45"/></svg></div>"""

with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page(viewport={"width": 1080, "height": 1350})
    def shot(html, path, h=1350):
        pg.set_viewport_size({"width": 1080, "height": h})
        pg.set_content(f"<html><head><style>{BASE_CSS}</style></head><body style='height:{h}px'>{html}</body></html>")
        pg.evaluate("document.fonts.ready.then(()=>document.fonts.size)")
        pg.wait_for_timeout(150)
        pg.screenshot(path=str(path))
    if not ONLY: shot(PROFILE, OUT / "profilbild.png", 1080)
    for name, slides in posts.items():
        if ONLY and not any(name.startswith(o) for o in ONLY): continue
        for i, html in enumerate(slides, 1):
            shot(html, OUT / f"{name}-{i}.png")
    b.close()
print(sorted(p.name for p in OUT.iterdir()))
