"""Baut ein Reel für @speicherklar (1080x1920, 30 fps) aus Slides + Voice-over.

Aufruf:  SPEICHERKLAR_SITE=<Checkout von main> python3 reel.py reels/<name>.json
Spec (JSON):
  {"name": "reel1-angebot", "audio": "pfad/zur/stimme.mp3", "tempo": 1.08,
   "slides": [{"text": "Satz, der zu dieser Slide gesprochen wird", "dark": false, "html": "<h1>…</h1>"}, …]}
- "text" aller Slides hintereinander = genau der Text, der an ElevenLabs ging (ohne Tags wie [confident]).
- Die Schnitte setzt das Skript selbst: erwartete Zeit nach Textlänge, dann auf die nächste Sprechpause geschnappt.
- Ausgabe: out/<name>.mp4, out/<name>-<n>.png (Slides) und out/<name>-uebersicht.png (zum Prüfen).

Bausteine für "html" (CSS unten): .tag (kleine Zeile in Versalien), h1 / h1 em (Bernstein), h2, p, p.muted,
.card(.best) mit .k/.v/.d, .pair (zwei Karten), .wheels (wheels-Funktion: {{wheels:670}}), .amp (Ampel-Liste,
<div><i class="y|g|r"></i><span>Titel<small>Text</small></span></div>), .price, .cta, p.src (Beispielwerte),
.hook (großer Einstieg, mit "dark": true). Sichere Zone: Text bleibt zwischen y=250 und y=1450, rechts 170 px frei.
"""
import json, os, pathlib, re, subprocess, sys
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).parent
SITE = os.environ.get("SPEICHERKLAR_SITE", str(HERE.parent / "speicherklar-site"))
os.environ["SPEICHERKLAR_SITE"] = SITE
head = (HERE / "make.py").read_text().split("def frame(")[0].replace("ONLY = sys.argv[1:]", "ONLY = []")
ns = {"__file__": str(HERE / "make.py")}
exec(head, ns)
LOGO = ns["LOGO"]
CSS = ns["BASE_CSS"] + """
body{width:1080px;height:1920px}
.reel{width:1080px;height:1920px;padding:250px 170px 470px 110px;display:flex;flex-direction:column;background:var(--bg)}
.reel.dark{background:var(--ink);color:#E6ECF1}
.reel .main{gap:44px}
.reel h1{font-size:128px} .reel h2{font-size:84px} .reel p{font-size:50px}
.tag{font-family:"JetBrains Mono";font-size:30px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
.dark .tag{color:#97A7B3}
.hl{background:linear-gradient(transparent 62%,#F2B33D88 62%)}
.amp{display:grid;gap:22px}
.amp div{display:grid;grid-template-columns:48px 1fr;align-items:center;gap:22px;background:#fff;border:2px solid var(--line);border-radius:18px;padding:26px 30px;font-size:42px;color:var(--ink)}
.amp i{width:44px;height:44px;border-radius:50%;display:block} .amp i.y{background:#E3B008} .amp i.g{background:#2E7D5B} .amp i.r{background:#B4412F}
.amp small{display:block;font-size:30px;color:var(--muted)}
.card{color:var(--ink)} .card.best{border:4px solid var(--sun)} .card .v{white-space:nowrap} .pair .card .v{font-size:84px}
.hook h1{font-size:150px;line-height:.98} .hook .tag{font-size:34px}
.reel .price{font-family:"Archivo";font-weight:800;font-stretch:105%;font-size:150px;color:#F2B33D;line-height:1}
.reel .cta{font-size:64px;padding:28px 44px}
.reel p.src{font-size:28px;line-height:1.35}
.brandrow{display:flex;gap:16px;align-items:center;font-family:"Archivo";font-stretch:118%;font-weight:800;font-size:40px}
"""

def wheels(n):
    return '<div class="wheels">' + "".join(f'<span class="wheel">{d}</span>' for d in str(n)) + "</div>"

def slide(html, dark):
    html = re.sub(r"\{\{wheels:(\d+)\}\}", lambda m: wheels(m.group(1)), html)
    c = "#E6ECF1" if dark else "#15212B"
    return f'<div class="reel{" dark" if dark else ""}"><div class="brandrow">{LOGO.format(s=46, c=c)}Speicherklar</div><div class="main">{html}</div></div>'

def run(*a):
    return subprocess.run(a, check=True, capture_output=True, text=True)

def main(spec_path):
    spec = json.loads(pathlib.Path(spec_path).read_text())
    name, tempo, slides = spec["name"], float(spec.get("tempo", 1.0)), spec["slides"]
    out = HERE / "out"; out.mkdir(exist_ok=True)
    tmp = HERE / "out" / f".{name}"; tmp.mkdir(exist_ok=True)
    # 1. Slides rendern
    with sync_playwright() as pw:
        b = pw.chromium.launch(); pg = b.new_page(viewport={"width": 1080, "height": 1920})
        for i, s in enumerate(slides, 1):
            pg.set_content(f"<html><head><style>{CSS}</style></head><body>{slide(s['html'], s.get('dark', False))}</body></html>")
            pg.evaluate("document.fonts.ready.then(()=>document.fonts.size)"); pg.wait_for_timeout(150)
            pg.screenshot(path=str(out / f"{name}-{i}.png"))
        b.close()
    # 2. Stimme beschleunigen, 1,2 s Ruhe anhängen
    audio = tmp / "vo.m4a"
    run("ffmpeg", "-nostdin", "-y", "-loglevel", "error", "-i", spec["audio"], "-af", f"atempo={tempo},apad=pad_dur=1.2", "-ar", "44100", "-c:a", "aac", "-b:a", "160k", str(audio))
    dur = float(run("ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(audio)).stdout)
    speech = dur - 1.2
    # 3. Pausen finden und Schnitte setzen
    sd = subprocess.run(["ffmpeg", "-nostdin", "-i", str(audio), "-af", "silencedetect=noise=-32dB:d=0.15", "-f", "null", "-"], capture_output=True, text=True).stderr
    pauses = [float(m) for m in re.findall(r"silence_end: ([\d.]+)", sd)]
    lens = [max(len(s["text"]), 1) for s in slides]
    wants, acc = [], 0
    for L in lens[:-1]:
        acc += L; wants.append(speech * acc / sum(lens))
    pauses = [p for p in pauses if 0.5 < p < speech]
    k, n = len(wants), len(pauses)
    if n >= k:
        # Pausen der Reihe nach den Schnitten zuordnen, Summe der quadrierten Abweichungen minimal (DP)
        INF = float("inf"); best = [[INF] * (n + 1) for _ in range(k + 1)]; best[0] = [0.0] * (n + 1)
        for i in range(1, k + 1):
            for j in range(i, n + 1):
                best[i][j] = min(best[i][j - 1], best[i - 1][j - 1] + (pauses[j - 1] - wants[i - 1]) ** 2)
        chosen, i, j = [], k, n
        while i > 0:
            if best[i][j] == best[i][j - 1] and j > i: j -= 1
            else: chosen.append(pauses[j - 1]); i -= 1; j -= 1
        cuts = [0.0] + chosen[::-1] + [dur]
    else:
        cuts = [0.0] + wants + [dur]
    # 4. Szenen kodieren, verbinden, Ton anlegen
    lst = tmp / "list.txt"; lines = []
    for i in range(len(slides)):
        d = round(cuts[i + 1] - cuts[i], 3)
        f = tmp / f"sc{i+1}.mp4"; t = tmp / f"tmp{i+1}.mp4"
        run("ffmpeg", "-nostdin", "-y", "-loglevel", "error", "-framerate", "30", "-i", str(out / f"{name}-{i+1}.png"),
            "-vf", f"format=yuv420p,loop=-1:1,trim=duration={d},setpts=PTS-STARTPTS", "-r", "30",
            "-c:v", "libx264", "-crf", "18", "-preset", "veryfast", "-pix_fmt", "yuv420p", str(t))
        t.rename(f); lines.append(f"file '{f.name}'")
    lst.write_text("\n".join(lines) + "\n")
    run("ffmpeg", "-nostdin", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(tmp / "video.mp4"))
    final, t = out / f"{name}.mp4", tmp / "final.mp4"
    run("ffmpeg", "-nostdin", "-y", "-loglevel", "error", "-i", str(tmp / "video.mp4"), "-i", str(audio), "-map", "0:v", "-map", "1:a",
        "-c:v", "copy", "-c:a", "copy", "-shortest", "-movflags", "+faststart", str(t))
    t.rename(final)
    # 5. Übersicht zum Prüfen
    from PIL import Image
    W, H = 270, 480; n = len(slides)
    im = Image.new("RGB", (W * min(n, 5), H * ((n + 4) // 5)), "white")
    for i in range(n):
        im.paste(Image.open(out / f"{name}-{i+1}.png").resize((W, H)), ((i % 5) * W, (i // 5) * H))
    im.save(out / f"{name}-uebersicht.png")
    print(json.dumps({"video": str(final), "dauer_s": round(dur, 1), "schnitte_s": [round(c, 2) for c in cuts]}, ensure_ascii=False))

if __name__ == "__main__":
    main(sys.argv[1])
