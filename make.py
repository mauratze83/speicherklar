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

# ---------- Post 5: Faustformel Speichergröße (9 Slides), Ableger zum Artikel stromspeicher-groesse-berechnen ----------
import subprocess
_js = r"""
const S=require(process.argv[1]);
const b={region:"4",tilt:35,ev:0,evTime:"eve",bat:6,bprice:500,life:15,price:%s,feed:7.7,feedLimit:0};
const e=(cons,kwp)=>S.evaluate({...b,cons,roofs:[{kwp,tilt:35,aspect:0}]});
const at=(r,c)=>r.sweep[c-1];
const out={};
for(const kwp of [6,9,12]){const r=e(4500,kwp);out["k"+kwp]={best:r.best.cap,bestNet:Math.round(r.best.net),rule:kwp,ruleNet:Math.round(at(r,kwp).net)};}
const r=e(4500,9);
out.std={best:[r.best.cap,Math.round(r.best.net)],v1:[5,Math.round(at(r,5).net)],v15:[7,Math.round(at(r,7).net)],kwp:[9,Math.round(at(r,9).net)]};
out.big={aut6:Math.round(at(r,6).r.autarky*100),aut10:Math.round(at(r,10).r.autarky*100),save:Math.round(at(r,10).save-at(r,6).save),cost:at(r,10).cost-at(r,6).cost,net:Math.round(at(r,6).net-at(r,10).net)};
console.log(JSON.stringify(out));
"""
_price = float(__import__("re").search(r'id="price"[^>]*value="([^"]+)"', (SITE / "src/body.html").read_text()).group(1))
F = json.loads(subprocess.run(["node", "-e", _js % _price, str(SITE / "src/sim.js")], capture_output=True, text=True, check=True).stdout)
def hbars(rows, lo=0, hi=3000):
    """Waagerechte Balken: rows = [(Beschriftung, Wert, Farbe, fett)]."""
    W, rh, lw = 820, 92, 0
    s = f'<svg width="{W}" height="{len(rows)*rh}" viewBox="0 0 {W} {len(rows)*rh}" font-family="Source Sans 3">'
    for i, (lab, v, col, bold) in enumerate(rows):
        y = i * rh
        w = (W - 190) * (v - lo) / (hi - lo)
        s += (f'<text x="0" y="{y+30}" font-size="30" fill="#15212B" font-weight="{700 if bold else 400}">{lab}</text>'
              f'<rect x="0" y="{y+44}" width="{max(4,w)}" height="34" rx="4" fill="{col}"/>'
              f'<text x="{w+16}" y="{y+72}" font-family="JetBrains Mono" font-size="28" font-weight="700" fill="#15212B">+{fmt(v)} €</text>')
    return s + "</svg>"
T = 9; tp = "Speichergröße"
k6, k9, k12, st, bg = F["k6"], F["k9"], F["k12"], F["std"], F["big"]
loss12 = k12["bestNet"] - k12["ruleNet"]
posts["post5-faustformel"] = [
  frame('<h1>1 kWh je kWp? <em>Lieber nicht.</em></h1><p class="promise">Welche Faustformel für die Speichergröße wirklich passt. Hab’s durchgerechnet.</p>', 1, T, tp),
  frame(f'<h2>Diese Faustregel kostet hier</h2>{wheels(loss12)}<p>Euro in 15 Jahren. 4.500 kWh Verbrauch, 12&nbsp;kWp auf dem Dach. Die Regel sagt {k12["rule"]}&nbsp;kWh Speicher, am meisten bleibt bei {k12["best"]} kWh.</p>', 2, T, tp),
  frame('<h2>Drei Faustformeln kursieren</h2>' + summary(["1 kWh je 1.000 kWh Verbrauch", "1,5 kWh je 1.000 kWh Verbrauch", "1 kWh je kWp Anlagenleistung"]) + '<p class="muted">Ich hab alle drei gegen eine Jahressimulation in 5-Minuten-Schritten gerechnet.</p>', 3, T, tp),
  frame(f'<h2>Im Normalfall liegen alle nah dran</h2><p class="muted" style="font-size:32px">4.500 kWh, 9 kWp Süd. Bilanz nach 15 Jahren</p>'
        + hbars([(f"Beste Größe: {st['best'][0]} kWh", st["best"][1], "#E39A0B", True), (f"1 kWh je 1.000 kWh: {st['v1'][0]} kWh", st["v1"][1], "#B9C3CB", False),
                 (f"1,5 kWh je 1.000 kWh: {st['v15'][0]} kWh", st["v15"][1], "#B9C3CB", False), (f"1 kWh je kWp: {st['kwp'][0]} kWh", st["kwp"][1], "#B9C3CB", False)]), 4, T, tp),
  frame('<h2>Je größer das Dach, desto teurer</h2><p class="muted" style="font-size:32px">4.500 kWh Verbrauch. Bilanz nach 15 Jahren</p>'
        + hbars([(f"6 kWp: beste Größe {k6['best']} kWh", k6["bestNet"], "#E39A0B", True), (f"6 kWp: Regel {k6['rule']} kWh", k6["ruleNet"], "#B9C3CB", False),
                 (f"9 kWp: beste Größe {k9['best']} kWh", k9["bestNet"], "#E39A0B", True), (f"9 kWp: Regel {k9['rule']} kWh", k9["ruleNet"], "#B9C3CB", False),
                 (f"12 kWp: beste Größe {k12['best']} kWh", k12["bestNet"], "#E39A0B", True), (f"12 kWp: Regel {k12['rule']} kWh", k12["ruleNet"], "#B9C3CB", False)]), 5, T, tp),
  frame(f'<h2>Der Abend zählt, nicht das Dach</h2><p>Der Speicher spart nur mit Strom, den du abends und nachts brauchst. Bei 4.500&nbsp;kWh bleibt die beste Größe {k9["best"]}&nbsp;kWh, mit 9 und mit 12&nbsp;kWp.</p>', 6, T, tp),
  frame(f'<h2>Größer sieht nur besser aus</h2><div class="pair"><div class="card"><div class="k">Autarkie, 10 statt 6 kWh</div><div class="v" style="font-size:72px;white-space:nowrap">{bg["aut6"]}&nbsp;→ {bg["aut10"]}&nbsp;%</div><div class="d">klingt nach viel</div></div><div class="card"><div class="k">Bilanz nach 15 Jahren</div><div class="v" style="color:var(--neg)">−{fmt(bg["net"])} €</div><div class="d">gegenüber 6 kWh</div></div></div><p>{bg["save"]} € mehr Ersparnis im Jahr, aber {fmt(bg["cost"])} € mehr Kaufpreis.</p>', 7, T, tp),
  frame('<h2>Kurz gesagt</h2>' + summary(["Rechne mit deinem Verbrauch, nicht mit kWp.", "Rund 1 kWh je 1.000 kWh passt meist.", "E-Auto lädt abends? Eher größer.", "Ost-West-Dach? Eher kleiner."]), 8, T, tp),
  frame(f'<h1>Wie viel kWh <em>für deinen Verbrauch?</em></h1><p>Der Rechner probiert 1 bis 15 kWh durch. Kostenlos, ohne Anmeldung. Link in der Bio.</p><div><span class="cta">speicherklar.de</span></div><p class="src">Beispiel: Ruhrgebiet, Süd 35°, 4.500 kWh/Jahr, Speicher 500 €/kWh, Strom {de(_price).rstrip("0").rstrip(",")} ct, Einspeisung 7,70 ct, 15 Jahre. Sonnendaten PVGIS (EU-Kommission), eigene Simulation.</p>', 9, T, tp, dark=True),
]

# ---------- Post 6: Stromsteuer bleibt (9 Slides), Stand 13.11.2026 ----------
_js6 = r"""
const S=require(process.argv[1]);const P=%s;const cut=(2.05-0.1)*1.19;
const b={region:"4",roofs:[{kwp:9,tilt:35,aspect:0}],cons:4500,ev:0,evTime:"eve",bat:6,bprice:500,life:15,feed:7.7,feedLimit:0};
const a=S.evaluate({...b,price:P}),c=S.evaluate({...b,price:P-cut});
const s=r=>r.sweep[a.best.cap-1];
console.log(JSON.stringify({cut:cut,pc:P-cut,best:a.best.cap,bestCut:c.best.cap,
 bill0:4500*cut/100,billPV:a.base.grid*cut/100,billBat:s(a).r.grid*cut/100,
 pay:s(a).payback,payCut:s(c).payback,net:s(a).net,netCut:s(c).net,save:s(a).save,saveCut:s(c).save}));
"""
G = json.loads(subprocess.run(["node", "-e", _js6 % _price, str(SITE / "src/sim.js")], capture_output=True, text=True, check=True).stdout)
d1 = lambda v: f"{v:.1f}".replace(".", ",")
d2 = lambda v: f"{v:.2f}".replace(".", ",")
def ebars(rows, hi):
    W, rh = 820, 92
    s = f'<svg width="{W}" height="{len(rows)*rh}" viewBox="0 0 {W} {len(rows)*rh}" font-family="Source Sans 3">'
    for i, (lab, v, col, bold) in enumerate(rows):
        y = i * rh; w = (W - 190) * v / hi
        s += (f'<text x="0" y="{y+30}" font-size="30" fill="#15212B" font-weight="{700 if bold else 400}">{lab}</text>'
              f'<rect x="0" y="{y+44}" width="{max(4,w)}" height="34" rx="4" fill="{col}"/>'
              f'<text x="{w+16}" y="{y+72}" font-family="JetBrains Mono" font-size="28" font-weight="700" fill="#15212B">{round(v)} €</text>')
    return s + "</svg>"
T = 9; tp = "Stromsteuer"
pr = de(_price).rstrip("0").rstrip(",")
posts["post6-stromsteuer"] = [
  frame('<h1>Stromsteuer bleibt. <em>Was heißt das für den Speicher?</em></h1><p class="promise">Was eine Senkung gebracht hätte. Hab’s durchgerechnet.</p>', 1, T, tp),
  frame(f'<h2>So viel hätte die Senkung gespart</h2>{wheels(round(G["bill0"]))}<p>Euro im Jahr, bei 4.500&nbsp;kWh Verbrauch ohne PV-Anlage. Für Haushalte bleibt die Steuer aber vorerst, wie sie ist.</p>', 2, T, tp),
  frame('<h2>Was entschieden ist</h2>' + summary(["Für Haushalte bleibt es bei 2,05&nbsp;ct je kWh.", "Die Senkung aufs EU-Minimum von 0,1&nbsp;ct fehlt im Haushalt 2027."]) + '<p class="muted" style="font-size:34px">Stand 13.11.2026. Noch nicht endgültig: Koalitionsausschuss am 17.11., Bundestag 24. bis 27.11.</p>', 3, T, tp),
  frame(f'<h2>Strom wäre {d2(G["cut"])} ct billiger</h2><div class="pair"><div class="card"><div class="k">Steuer bleibt</div><div class="v">{pr} ct</div><div class="d">je kWh, Beispielpreis</div></div><div class="card"><div class="k">mit Senkung</div><div class="v">{d1(G["pc"])} ct</div><div class="d">je kWh</div></div></div><p>1,95 ct weniger Steuer, dazu fällt die Umsatzsteuer darauf weg.</p>', 4, T, tp),
  frame(f'<h2>Mit PV merkst du’s weniger</h2><p class="muted" style="font-size:32px">Ersparnis durch die Senkung, Euro im Jahr</p>'
        + ebars([("ohne PV-Anlage", G["bill0"], "#B9C3CB", False), ("9 kWp, ohne Speicher", G["billPV"], "#B9C3CB", False), (f"9 kWp, {G['best']} kWh Speicher", G["billBat"], "#E39A0B", True)], G["bill0"])
        + '<p>Wer weniger Netzstrom kauft, zahlt auch weniger Stromsteuer.</p>', 5, T, tp),
  frame(f'<h2>Der Speicher rechnet sich schneller</h2><div class="pair"><div class="card"><div class="k">Steuer bleibt</div><div class="v" style="color:var(--pos)">{d1(G["pay"])} J.</div><div class="d">bis {G["best"]} kWh bezahlt sind</div></div><div class="card"><div class="k">mit Senkung</div><div class="v">{d1(G["payCut"])} J.</div><div class="d">bis {G["best"]} kWh bezahlt sind</div></div></div><p>Jede kWh aus dem Speicher ersetzt Netzstrom. Je teurer der, desto mehr spart sie.</p>', 6, T, tp),
  frame(f'<h2>Die beste Größe bleibt gleich</h2><p>{G["best"]}&nbsp;kWh sind in beiden Fällen die beste Größe. Nach 15 Jahren bleiben {fmt(round(G["net"]))} € statt {fmt(round(G["netCut"]))} € übrig.</p><p class="muted">Für deine Planung ändert die Entscheidung also wenig. Wär die Steuer gesunken, hätte sich der Speicher etwas später bezahlt.</p>', 7, T, tp),
  frame('<h2>Kurz gesagt</h2>' + summary(["Die Stromsteuer bleibt vorerst bei 2,05&nbsp;ct.", f"Eine Senkung hätte Strom um {d2(G['cut'])}&nbsp;ct billiger gemacht.", f"Der Speicher bezahlt sich so in {d1(G['pay'])} statt {d1(G['payCut'])}&nbsp;Jahren.", "An der passenden Größe ändert das&nbsp;nichts."]), 8, T, tp),
  frame(f'<h1>Rechne mit <em>deinem Strompreis.</em></h1><p>Im Rechner den Strompreis verschieben und sehen, was sich ändert. Kostenlos, ohne Anmeldung. Link in der Bio.</p><div><span class="cta">speicherklar.de</span></div><p class="src">Beispiel: Ruhrgebiet, 9 kWp Süd 35°, 4.500 kWh/Jahr, Speicher 500 €/kWh, Strom {pr} ct, Einspeisung 7,70 ct, 15 Jahre. Stromsteuer: § 3 StromStG, EU-Minimum 0,1 ct (Richtlinie 2003/96/EG). Stand 13.11.2026.</p>', 9, T, tp, dark=True),
]

# ---------- Post 7: Rechner an echten Häusern geprüft (10 Slides), Ableger zum Artikel stromspeicher-rechner-test-echte-daten ----------
# Messwerte (eigene Anlage, SENEC-Export, Prüfjahr 26.10.2025–25.10.2026) und WPuQ-Ergebnisse stehen im Projekt unter
# claude/sim-pruefung-eigene-anlage.md; Ost-West und Standard-Beispiel rechnet sim.js hier live.
_js7 = r"""
const S=require(process.argv[1]);const P=%s;
const b={region:"4",cons:4500,ev:0,evTime:"eve",bat:6,bprice:500,life:15,price:P,feed:7.7,feedLimit:0};
const s=S.evaluate({...b,roofs:[{kwp:9,tilt:35,aspect:0}]}),o=S.evaluate({...b,roofs:[{kwp:4.5,tilt:35,aspect:-90},{kwp:4.5,tilt:35,aspect:90}]});
console.log(JSON.stringify({sBest:s.best.cap,sNet:Math.round(s.best.net),oBest:o.best.cap}));
"""
K = json.loads(subprocess.run(["node", "-e", _js7 % _price, str(SITE / "src/sim.js")], capture_output=True, text=True, check=True).stdout)
M = {"gemessen": 1860, "vorher": 2819, "heute": 1735, "netzMess": 9493, "netzSim": 9716, "julAlt": 11, "julMess": 41, "haus10": 76, "sim10": 77}
def kbars(rows, hi):
    W, rh = 820, 92
    s = f'<svg width="{W}" height="{len(rows)*rh}" viewBox="0 0 {W} {len(rows)*rh}" font-family="Source Sans 3">'
    for i, (lab, v, col, bold) in enumerate(rows):
        y = i * rh; w = (W - 230) * v / hi
        s += (f'<text x="0" y="{y+30}" font-size="30" fill="#15212B" font-weight="{700 if bold else 400}">{lab}</text>'
              f'<rect x="0" y="{y+44}" width="{max(4,w)}" height="34" rx="4" fill="{col}"/>'
              f'<text x="{w+16}" y="{y+72}" font-family="JetBrains Mono" font-size="28" font-weight="700" fill="#15212B">{fmt(v)} kWh</text>')
    return s + "</svg>"
T = 10; tp = "Rechner geprüft"
posts["post7-rechner-geprueft"] = [
  frame('<h1>Ich hab meinen Rechner <em>nachgeprüft.</em></h1><p class="promise">An meiner eigenen Anlage und 30 echten Häusern. Zwei Fehler gefunden.</p>', 1, T, tp),
  frame(f'<h2>So viel Netzstrom ersetzt mein Speicher</h2>{wheels(M["gemessen"])}<p>kWh im Jahr, gemessen. Mein Rechner hatte für dasselbe Haus {fmt(M["vorher"])} kWh ausgegeben. Das war mir zu viel.</p>', 2, T, tp),
  frame('<h2>Das Setup</h2>' + summary(["12,92 kWp Ost-West, 45° Neigung", "10 kWh Speicher", "Wärmepumpe, Pool und E-Auto an einem Zähler", "Messwerte alle 5 Minuten, seit 2021"]), 3, T, tp),
  frame(f'<h2>Der Speicher selbst rechnet richtig</h2><div class="pair"><div class="card"><div class="k">Netzbezug gemessen</div><div class="v">{fmt(M["netzMess"])}</div><div class="d">kWh an 336 Tagen</div></div><div class="card"><div class="k">Rechner, mit meinen Daten</div><div class="v">{fmt(M["netzSim"])}</div><div class="d">kWh, 2,3 % daneben</div></div></div><p>Gibt man dem Rechner echte Erzeugung und echten Verbrauch, passt es.</p>', 4, T, tp),
  frame(f'<h2>Fehler 1: die Wärmepumpe</h2><p class="muted" style="font-size:32px">Netzstrom, den der Speicher im Jahr ersetzt</p>'
        + kbars([("Gemessen", M["gemessen"], "#15212B", True), ("Rechner vorher", M["vorher"], "#B9C3CB", False), ("Rechner heute", M["heute"], "#E39A0B", True)], M["vorher"])
        + '<p>Der Rechner kannte nur kurze Haushaltsspitzen. Wärmepumpe und Pool laufen aber gleichmäßig. Jetzt trägst du sie getrennt ein.</p>', 5, T, tp),
  frame(f'<h2>Fehler 2: das Wetter</h2><div class="pair"><div class="card"><div class="k">Trübste Julitage, Rechner vorher</div><div class="v">{M["julAlt"]} %</div><div class="d">eines normalen Tages</div></div><div class="card"><div class="k">Gemessen (PVGIS, 10 Jahre)</div><div class="v" style="color:var(--pos)">{M["julMess"]} %</div><div class="d">eines normalen Tages</div></div></div><p>Der Sommer war im Rechner viel zu wechselhaft. Jetzt nimmt er Sonne und Wolken aus einem echten Jahr, Stunde für Stunde.</p>', 6, T, tp),
  frame(f'<h2>Gegenprobe: 30 fremde Häuser</h2><div class="pair"><div class="card"><div class="k">Gemessen</div><div class="v">{M["haus10"]} %</div><div class="d">Autarkie mit 10 kWh</div></div><div class="card"><div class="k">Rechner</div><div class="v" style="color:var(--sun-ink)">{M["sim10"]} %</div><div class="d">Autarkie mit 10 kWh</div></div></div><p>Minutenwerte vom Institut für Solarenergieforschung Hameln. Mit Speicher liegt der Rechner jetzt auf 1–2 Punkte genau.</p>', 7, T, tp),
  frame(f'<h2>Eine Korrektur an euch</h2><p>Am 09.11. hab ich geschrieben: Bei Ost-West reichen 4&nbsp;kWh. Mit dem geprüften Rechner sind es {K["oBest"]}&nbsp;kWh.</p><p class="muted">Beim Süddach bleibt es bei {K["sBest"]}&nbsp;kWh, nach 15 Jahren bleiben {fmt(K["sNet"])}&nbsp;€ übrig.</p>', 8, T, tp),
  frame('<h2>Kurz gesagt</h2>' + summary(["Der Speicher-Teil stimmte schon.", "Wärmepumpe und Wetter waren falsch, jetzt behoben.", "30 echte Häuser: 1–2 Punkte genau.", f"Ost-West: {K['oBest']} statt 4 kWh."]), 9, T, tp),
  frame(f'<h1>Der ganze Test <em>mit allen Zahlen.</em></h1><p>Setup, Messwerte, beide Fehler und die 30 Häuser. Im Artikel auf speicherklar.de. Link in der Bio.</p><div><span class="cta">speicherklar.de</span></div><p class="src">Eigene Messwerte: SENEC-Export, 26.10.2025–25.10.2026. Vergleichshäuser: WPuQ, ISFH 2019, CC BY 4.0. Wetter: PVGIS-SARAH3 (EU-Kommission). Beispiel: Ruhrgebiet, 9 kWp, 35°, 4.500 kWh/Jahr, Speicher 500 €/kWh, Strom {pr} ct, Einspeisung 7,70 ct, 15 Jahre.</p>', 10, T, tp, dark=True),
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
