"""Story-Frames (1080×1920) für @speicherklar. Nutzt CSS und Logo aus make.py.
Aufruf: SPEICHERKLAR_SITE=<Checkout von main> python3 story.py"""
import pathlib, os, sys, json, subprocess, re
from playwright.sync_api import sync_playwright
HERE = pathlib.Path(__file__).parent
SITE = pathlib.Path(os.environ.get("SPEICHERKLAR_SITE", HERE.parent / "speicherklar-site"))
src = (HERE / "make.py").read_text()
ns = {"__file__": str(HERE / "make.py")}
sys.argv = sys.argv[:1]
exec(src[:src.index("D = json.loads")], ns)   # Importe, Schriften, BASE_CSS, LOGO, frame, Helfer
BASE_CSS, LOGO, wheels = ns["BASE_CSS"], ns["LOGO"], ns["wheels"]
OUT = HERE / "out"; OUT.mkdir(exist_ok=True)

# Zahlen frisch aus sim.js (Standard-Beispiel, Strompreis = Standardwert im Rechner)
price = float(re.search(r'id="price"[^>]*value="([\d.]+)"', (SITE / "src/body.html").read_text()).group(1))
js = r"""
const S=require(process.argv[1]);const P=%s;const cut=(2.05-0.1)*1.19;
const b={region:"4",roofs:[{kwp:9,tilt:35,aspect:0}],cons:4500,ev:0,evTime:"eve",bat:6,bprice:500,life:15,feed:7.7,feedLimit:0};
const a=S.evaluate({...b,price:P}),c=S.evaluate({...b,price:P-cut});
const best=a.best.cap,x=a.sweep[best-1],y=c.sweep[best-1];
console.log(JSON.stringify({cut,best,pay:x.payback,pay27:1+(x.cost-y.save)/x.save}));
"""
H = json.loads(subprocess.run(["node", "-e", js % price, str(SITE / "src/sim.js")], capture_output=True, text=True, check=True).stdout)
d1 = lambda v: f"{v:.1f}".replace(".", ","); d2 = lambda v: f"{v:.2f}".replace(".", ",")
pr = d1(price).replace(",0", "") if price == int(price) else d2(price)

STORY_CSS = """
body{height:1920px}
.story{width:1080px;height:1920px;padding:250px 110px 340px;display:flex;flex-direction:column;gap:44px;background:var(--bg)}
.story .top{font-size:26px}
.tag{display:inline-block;align-self:flex-start;font-family:"JetBrains Mono";font-weight:700;font-size:28px;letter-spacing:.06em;text-transform:uppercase;background:var(--ink);color:#F2B33D;padding:10px 18px;border-radius:10px}
.story h1{font-size:108px}
.story p{font-size:46px}
.story p.src{font-size:26px;line-height:1.4}
.sticker{flex-shrink:0;margin-top:auto;border:3px dashed var(--line);border-radius:24px;height:200px;display:flex;align-items:center;justify-content:center;font-family:"Archivo";font-weight:700;font-size:38px;color:var(--sun-ink)}
"""
story = f"""<div class="story">
<div class="top"><div class="brand">{LOGO.format(s=40,c="#15212B")}Speicherklar</div><div>Stromsteuer</div></div>
<span class="tag">Update 28.11.2026</span>
<h1>Jetzt beschlossen: <em>Stromsteuer sinkt 2027.</em></h1>
<p>Bundestag, 27.11.: 0,1 statt 2,05&nbsp;ct je kWh, vom 1.1. bis 31.12.2027. Strom wird bis zu {d2(H["cut"])}&nbsp;ct billiger.</p>
<div class="card"><div class="k">Für deinen Speicher</div><div class="v">bleibt {H["best"]} kWh</div><div class="d" style="font-size:34px">die beste Größe. Bezahlt nach {d1(H["pay27"])} statt {d1(H["pay"])} Jahren.</div></div>
<div class="sticker">Ganze Rechnung im Artikel ↓</div>
<p class="src">Beispiel: Ruhrgebiet, 9 kWp Süd 35°, 4.500 kWh/Jahr, Speicher 500 €/kWh, Strom {pr} ct, Einspeisung 7,70 ct, 15 Jahre; Senkung ein Jahr. Bundesrat steht noch aus. Quelle: Bundesregierung, Bundestag, 27.11.2026.</p>
</div>"""

with sync_playwright() as pw:
    b = pw.chromium.launch(); pg = b.new_page(viewport={"width": 1080, "height": 1920})
    pg.set_content(f"<html><head><style>{BASE_CSS}{STORY_CSS}</style></head><body>{story}</body></html>")
    pg.evaluate("document.fonts.ready.then(()=>document.fonts.size)"); pg.wait_for_timeout(200)
    pg.screenshot(path=str(OUT / "story-stromsteuer-beschlossen.png")); b.close()
print(H)
