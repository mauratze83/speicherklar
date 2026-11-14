"""Baut ein Reel für @speicherklar (1080x1920, 30 fps) aus Slides + Voice-over.

Aufruf:  SPEICHERKLAR_SITE=<Checkout von main> python3 reel.py reels/<name>.json
Spec (JSON):
  {"name": "reel1-angebot", "audio": "pfad/zur/stimme.mp3", "tempo": 1.08,
   "slides": [{"text": "Satz, der zu dieser Slide gesprochen wird", "dark": false, "html": "<h1>…</h1>"}, …]}
- "text" aller Slides hintereinander = genau der Text, der an ElevenLabs ging (ohne Tags wie [confident]).
  Schreibweise für die Untertitel: [[4.500 kWh|viertausendfünfhundert Kilowattstunden]] – links steht im Untertitel,
  rechts wird gesprochen (nur der rechte Teil geht an ElevenLabs, siehe spoken()).
- Untertitel werden immer eingebrannt (Wort-Zeitpunkte per faster-whisper), außer "untertitel": false.
- Die Schnitte setzt das Skript selbst: Wort-Zeitpunkte per faster-whisper, Schnitt kurz vor dem ersten Wort der nächsten Slide.
- "cover": Nummer der Slide fürs Titelbild (Standard 1; bei geteiltem Hook die Slide mit dem ganzen Hook).
  Das Titelbild wird eigens gerendert: Inhalt mittig im 3:4-Ausschnitt des Profilrasters (y 240–1680),
  Hook innerhalb des 1:1-Ausschnitts (y 420–1500), keine Untertitel.
- Ausgabe: out/<name>.mp4, out/<name>-titelbild.png, out/<name>-<n>.png (Slides) und out/<name>-uebersicht.png (zum Prüfen).

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
.reel.cover{padding:330px 170px 330px 110px}
.reel.cover .hook h1{font-size:160px}
.sub{position:absolute;left:0;top:0;display:inline-block;max-width:860px;padding:14px 28px 18px;border-radius:22px;
 background:rgba(21,33,43,.9);color:#fff;font-family:"Archivo";font-weight:800;font-stretch:105%;font-size:56px;white-space:nowrap;line-height:1.12;text-align:center}
.sub b{color:#F2B33D;font-weight:800}
.brandrow{display:flex;gap:16px;align-items:center;font-family:"Archivo";font-stretch:118%;font-weight:800;font-size:40px}
"""

def wheels(n):
    return '<div class="wheels">' + "".join(f'<span class="wheel">{d}</span>' for d in str(n)) + "</div>"

SUB_Y = 1530  # Mitte der Untertitel-Zeile: unter dem Slide-Inhalt (bis 1450), über der Instagram-Leiste (ab ~1600)
SUB_CX = 510  # Mitte zwischen linkem Rand 110 und den Instagram-Symbolen rechts

def spoken(text):
    """Text, der an ElevenLabs geht: [[Anzeige|gesprochen]] -> gesprochen."""
    return re.sub(r"\[\[([^|\]]*)\|([^\]]*)\]\]", r"\2", text)

def units(text):
    """Anzeige-Einheiten einer Slide: [(anzeige, [gesprochene Wörter])]."""
    out = []
    for m in re.finditer(r"\[\[([^|\]]*)\|([^\]]*)\]\]|(\S+)", text):
        if m.group(3): out.append((m.group(3), [m.group(3)]))
        else:
            disp, sp = m.group(1), m.group(2).split()
            # Satzzeichen direkt hinter der Klammer gehört zur Einheit
            out.append((disp, sp))
    # "]]." -> Satzzeichen an die vorige Einheit hängen
    fixed = []
    for d, sp in out:
        if fixed and re.fullmatch(r"[.,!?:;]+", d): fixed[-1] = (fixed[-1][0] + d, fixed[-1][1])
        else: fixed.append((d, sp))
    return fixed

def norm(w):
    return re.sub(r"[^a-zäöüß0-9]", "", w.lower())

def word_times(audio, script_words, prompt):
    """Zeitpunkte je Skript-Wort: Whisper-Wörter per difflib zuordnen, Lücken linear füllen."""
    import difflib, numpy as np
    from faster_whisper import WhisperModel
    raw = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", str(audio), "-f", "s16le", "-ac", "1", "-ar", "16000", "-"],
                         capture_output=True, check=True).stdout
    a = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
    segs, _ = WhisperModel("small", device="cpu", compute_type="int8").transcribe(a, language="de", word_timestamps=True, initial_prompt=prompt)
    ww = [w for sg in segs for w in sg.words]
    A, B = [norm(w) for w in script_words], [norm(w.word) for w in ww]
    times = [None] * len(A)
    for blk in difflib.SequenceMatcher(None, A, B, autojunk=False).get_matching_blocks():
        for k in range(blk.size): times[blk.a + k] = (ww[blk.b + k].start, ww[blk.b + k].end)
    ends = ww[-1].end if ww else 0.0
    i = 0
    while i < len(times):
        if times[i] is None:
            j = i
            while j < len(times) and times[j] is None: j += 1
            t0 = times[i - 1][1] if i else 0.0
            t1 = times[j][0] if j < len(times) else ends
            n = j - i
            for k in range(n): times[i + k] = (t0 + (t1 - t0) * k / n, t0 + (t1 - t0) * (k + 1) / n)
            i = j
        else: i += 1
    return times

def sub_chunks(slides, times):
    """Untertitel-Blöcke je Slide: max. 4 Einheiten / 24 Zeichen, Umbruch nach Satzzeichen."""
    res, wi = [], 0
    for si, s in enumerate(slides):
        cur, out = [], []
        for disp, sp in units(s["text"]):
            t = (times[wi][0], times[wi + len(sp) - 1][1]); wi += len(sp)
            if cur and (len(cur) >= 4 or len(" ".join(d for d, _ in cur) + " " + disp) > 24):
                carry = []  # kurzes Füllwort (im, in, der, du …) nicht am Zeilenende stehen lassen
                if len(cur) > 1 and re.fullmatch(r"[a-zäöü]{1,3}", cur[-1][0]): carry = [cur.pop()]
                out.append(cur); cur = carry
            cur.append((disp, t))
            if re.search(r"[.,!?:;]$", disp): out.append(cur); cur = []
        if cur: out.append(cur)
        for c in out: res.append({"slide": si, "start": c[0][1][0], "end": c[-1][1][1], "text": " ".join(d for d, _ in c)})
    for a, b in zip(res, res[1:]):  # bis zum nächsten Block stehen lassen, bei langer Pause 0,3 s nach dem letzten Wort weg
        a["end"] = b["start"] if b["start"] - a["end"] < 0.6 else a["end"] + 0.3
    if res: res[-1]["end"] += 0.6
    return res

def sub_html(text):
    h = " ".join(f"<b>{w}</b>" if re.search(r"\d", w) or w in ("€", "kWh", "kWp") else w for w in text.split())
    return h.replace("</b> <b>", " ")

def slide(html, dark, cover=False):
    html = re.sub(r"\{\{wheels:(\d+)\}\}", lambda m: wheels(m.group(1)), html)
    c = "#E6ECF1" if dark else "#15212B"
    return f'<div class="reel{" dark" if dark else ""}{" cover" if cover else ""}"><div class="brandrow">{LOGO.format(s=46, c=c)}Speicherklar</div><div class="main">{html}</div></div>'

def srt_t(t):
    ms = int(round(t * 1000)); return f"{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}"

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
        c = int(spec.get("cover", 1))
        pg.set_content(f"<html><head><style>{CSS}</style></head><body>{slide(slides[c-1]['html'], slides[c-1].get('dark', False), cover=True)}</body></html>")
        pg.evaluate("document.fonts.ready.then(()=>document.fonts.size)"); pg.wait_for_timeout(150)
        pg.screenshot(path=str(out / f"{name}-titelbild.png"))
        b.close()
    # 2. Stimme beschleunigen, 1,2 s Ruhe anhängen
    audio = tmp / "vo.m4a"
    run("ffmpeg", "-nostdin", "-y", "-loglevel", "error", "-i", spec["audio"], "-af", f"atempo={tempo},apad=pad_dur=1.2", "-ar", "48000", "-c:a", "aac", "-b:a", "192k", str(audio))
    dur = float(run("ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(audio)).stdout)
    speech = dur - 1.2
    # 3. Wort-Zeitpunkte (Whisper) und Schnitte: kurz vor dem ersten Wort der nächsten Slide
    words = [w for s in slides for _, sp in units(s["text"]) for w in sp]
    times = word_times(audio, words, " ".join(spoken(s["text"]) for s in slides))
    cuts, wi = [0.0], 0
    for s in slides[:-1]:
        wi += sum(len(sp) for _, sp in units(s["text"]))
        last_end, nxt = times[wi - 1][1], times[wi][0]
        cuts.append(round(max(last_end, nxt - min(0.15, (nxt - last_end) / 2)), 3))
    cuts.append(dur)
    # 4. Untertitel: Wort-Zeitpunkte, Blöcke, je Block ein PNG
    subs = []
    if spec.get("untertitel", True):
        subs = sub_chunks(slides, times)
        with sync_playwright() as pw:
            b = pw.chromium.launch(); pg = b.new_page(viewport={"width": 1080, "height": 400})
            for k, c in enumerate(subs):
                pg.set_content(f"<html><head><style>{CSS} body{{width:1080px;height:400px;background:transparent}}</style></head>"
                               f"<body><div class='sub'>{sub_html(c['text'])}</div></body></html>")
                pg.evaluate("document.fonts.ready.then(()=>document.fonts.size)"); pg.wait_for_timeout(50)
                el = pg.query_selector(".sub"); bb = el.bounding_box()
                c["png"] = tmp / f"sub{k}.png"; el.screenshot(path=str(c["png"]), omit_background=True)
                c["x"], c["y"] = int(SUB_CX - bb["width"] / 2), int(SUB_Y - bb["height"] / 2)
            b.close()
        (out / f"{name}.srt").write_text("".join(
            f"{k+1}\n{srt_t(c['start'])} --> {srt_t(c['end'])}\n{c['text']}\n\n" for k, c in enumerate(subs)))
    # 5. Szenen kodieren (mit Untertiteln), verbinden, Ton anlegen
    lst = tmp / "list.txt"; lines = []
    enc = ["-c:v", "libx264", "-preset", "veryfast", "-pix_fmt", "yuv420p", "-r", "30", "-g", "60",
           "-b:v", "6M", "-minrate", "6M", "-maxrate", "6M", "-bufsize", "12M", "-x264-params", "nal-hrd=cbr"]
    for i in range(len(slides)):
        d = round(cuts[i + 1] - cuts[i], 3)
        f = tmp / f"sc{i+1}.mp4"; t = tmp / f"tmp{i+1}.mp4"
        mine = [c for c in subs if c["end"] > cuts[i] and c["start"] < cuts[i + 1]]
        inp = ["-framerate", "30", "-i", str(out / f"{name}-{i+1}.png")]
        fc = f"[0:v]format=yuv420p,loop=-1:1,trim=duration={d},setpts=PTS-STARTPTS[v0]"
        for k, c in enumerate(mine):
            inp += ["-i", str(c["png"])]
            a0, a1 = max(c["start"] - cuts[i], 0), min(c["end"], cuts[i + 1]) - cuts[i]
            fc += f";[v{k}][{k+1}:v]overlay={c['x']}:{c['y']}:enable='between(t,{a0:.3f},{a1:.3f})'[v{k+1}]"
        fc += f";[v{len(mine)}]format=yuv420p[out]"
        run("ffmpeg", "-nostdin", "-y", "-loglevel", "error", *inp, "-filter_complex", fc, "-map", "[out]", *enc, str(t))
        t.rename(f); lines.append(f"file '{f.name}'")
    lst.write_text("\n".join(lines) + "\n")
    run("ffmpeg", "-nostdin", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(tmp / "video.mp4"))
    final, t = out / f"{name}.mp4", tmp / "final.mp4"
    run("ffmpeg", "-nostdin", "-y", "-loglevel", "error", "-i", str(tmp / "video.mp4"), "-i", str(audio), "-map", "0:v", "-map", "1:a",
        "-c:v", "copy", "-c:a", "copy", "-shortest", "-movflags", "+faststart", str(t))
    t.rename(final)
    # 5. Titelbild: oben in Schritt 1 eigens gerendert (mittig im 3:4-Ausschnitt)
    # 6. Übersicht zum Prüfen (plus je Slide ein Bild mit Untertitel aus dem fertigen Video)
    if subs:
        for i in range(len(slides)):
            mine = [c for c in subs if c["slide"] == i]
            if mine:
                run("ffmpeg", "-nostdin", "-y", "-loglevel", "error", "-ss", f"{(mine[0]['start']+mine[0]['end'])/2:.2f}", "-i", str(final),
                    "-frames:v", "1", str(tmp / f"check{i+1}.png"))
    from PIL import Image
    W, H = 270, 480; n = len(slides)
    im = Image.new("RGB", (W * min(n, 5), H * ((n + 4) // 5)), "white")
    for i in range(n):
        src = tmp / f"check{i+1}.png"
        im.paste(Image.open(src if src.exists() else out / f"{name}-{i+1}.png").resize((W, H)), ((i % 5) * W, (i // 5) * H))
    im.save(out / f"{name}-uebersicht.png")
    print(json.dumps({"video": str(final), "dauer_s": round(dur, 1), "untertitel": len(subs), "schnitte_s": [round(c, 2) for c in cuts]}, ensure_ascii=False))

if __name__ == "__main__":
    main(sys.argv[1])
