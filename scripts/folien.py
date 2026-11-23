#!/usr/bin/env python3
"""Baut die Präsentationen unter /folien/<name>/ aus src/folien/<name>/.

Quelle je Deck: deck.json (Titel, Reihenfolge), deck.css, slides/<id>.html
(Export aus dem Slides-Artefakt in Claude). Die Seiten sind bewusst nicht
verlinkt, haben noindex und stehen nicht in Sitemap oder llms.txt.

Aufruf: python3 scripts/folien.py
"""
import html
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "src" / "folien"
FONTS = (ROOT / "src" / "fonts.css").read_text().replace("url(fonts/", "url(/fonts/")

VIEWER_CSS = """
*{box-sizing:border-box}
html,body{margin:0;height:100%;background:#0E161D;overflow:hidden}
#stage{position:absolute;left:50%;top:50%;width:1920px;height:1080px;transform-origin:0 0}
#stage section{position:absolute;inset:0;width:1920px;height:1080px;display:none!important}
#stage section.on{display:flex!important}
#stage aside{display:none}
x-shape{display:block;flex:none}
x-shape[kind=ellipse]{border-radius:50%}
x-shape[kind=rounded]{border-radius:16px}
x-shape[kind=arrow-right]{clip-path:polygon(0 32%,58% 32%,58% 0,100% 50%,58% 100%,58% 68%,0 68%)}
#nav{position:fixed;right:16px;top:14px;opacity:0;transition:opacity .25s;display:flex;gap:8px;align-items:center;font:500 14px "JetBrains Mono",monospace;color:#CBD3DA;z-index:2}
#nav button{all:unset;cursor:pointer;width:40px;height:40px;border-radius:8px;background:rgba(255,255,255,.08);color:#fff;text-align:center;line-height:40px;font-size:18px}
body.ui #nav,#nav:focus-within{opacity:1}
#nav button:hover{background:rgba(255,255,255,.18)}
#nav button:focus-visible{outline:2px solid #F2B33D}
@media print{
  @page{size:1920px 1080px;margin:0}
  html,body{overflow:visible;height:auto;background:none}
  #nav{display:none}
  #stage{position:static;transform:none!important;width:1920px;height:auto}
  #stage section{position:relative;display:flex!important;break-after:page}
  #stage *{animation:none!important}
}
"""

VIEWER_JS = """
(function(){
  var st=document.getElementById('stage'), s=st.querySelectorAll('section'), n=s.length, i=0;
  var c=document.getElementById('cnt');
  function fit(){var k=Math.min(innerWidth/1920,innerHeight/1080);
    st.style.transform='scale('+k+') translate(-50%,-50%)';}
  function show(j){i=Math.max(0,Math.min(n-1,j));
    for(var a=0;a<n;a++)s[a].classList.toggle('on',a===i);
    c.textContent=(i+1)+' / '+n; history.replaceState(null,'','#'+(i+1));}
  addEventListener('resize',fit);
  addEventListener('keydown',function(e){
    if(['ArrowRight','ArrowDown','PageDown',' ','Enter'].indexOf(e.key)>=0){e.preventDefault();show(i+1);}
    else if(['ArrowLeft','ArrowUp','PageUp','Backspace'].indexOf(e.key)>=0){e.preventDefault();show(i-1);}
    else if(e.key==='Home')show(0); else if(e.key==='End')show(n-1);
    else if(e.key==='f'&&document.documentElement.requestFullscreen)document.documentElement.requestFullscreen();});
  document.getElementById('prev').onclick=function(){show(i-1)};
  document.getElementById('next').onclick=function(){show(i+1)};
  document.getElementById('full').onclick=function(){
    if(document.fullscreenElement)document.exitFullscreen();
    else if(document.documentElement.requestFullscreen)document.documentElement.requestFullscreen();};
  var t=null; function ui(){document.body.classList.add('ui');clearTimeout(t);t=setTimeout(function(){document.body.classList.remove('ui')},2500);}
  addEventListener('mousemove',ui); addEventListener('touchstart',ui,{passive:true});
  var x0=null;
  addEventListener('touchstart',function(e){x0=e.touches[0].clientX},{passive:true});
  addEventListener('touchend',function(e){if(x0===null)return;var d=e.changedTouches[0].clientX-x0;
    if(Math.abs(d)>40)show(i+(d<0?1:-1));x0=null},{passive:true});
  fit(); show((parseInt(location.hash.slice(1),10)||1)-1);
})();
"""


def build(deck_dir: pathlib.Path) -> pathlib.Path:
    meta = json.loads((deck_dir / "deck.json").read_text())
    css = (deck_dir / "deck.css").read_text()
    slides = []
    for sid in meta["order"]:
        if not re.fullmatch(r"[A-Za-z0-9_-]{1,64}", sid):
            raise SystemExit(f"Ungültige Folien-ID: {sid}")
        slides.append((deck_dir / "slides" / f"{sid}.html").read_text().strip())
    title = html.escape(meta["title"])
    page = f"""<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{title}</title>
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<style>{FONTS}
{css}
{VIEWER_CSS}</style>
</head>
<body>
<div id="stage">
{chr(10).join(slides)}
</div>
<div id="nav"><span id="cnt"></span> <button id="prev" aria-label="Vorherige Folie">‹</button> <button id="next" aria-label="Nächste Folie">›</button> <button id="full" aria-label="Vollbild">⛶</button></div>
<script>{VIEWER_JS}</script>
</body>
</html>
"""
    out = ROOT / "folien" / deck_dir.name / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page)
    return out


if __name__ == "__main__":
    for d in sorted(p for p in SRC.iterdir() if p.is_dir()):
        print("gebaut:", build(d).relative_to(ROOT))
