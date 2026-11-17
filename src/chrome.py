"""Gemeinsame Kopf- und Fußzeile für alle Seiten von speicherklar.de.

prefix: Pfad zur Website-Wurzel aus Sicht der Seite ("./" für Seiten im Hauptordner, "../" für ratgeber/).
active: "rechner" | "ratgeber" | "pro" | None – markiert den aktuellen Menüpunkt.
"""

IG = "https://www.instagram.com/speicherklar/"

# Reichweitenmessung mit Umami Cloud (ohne Cookies). Leer = kein Skript und kein Abschnitt in der Datenschutzerklärung.
UMAMI_ID = "f4570047-b7d7-42e7-944e-a06941b94082"
UMAMI_SRC = "https://cloud.umami.is/script.js"

# Eigene Besuche nicht zählen: einmal speicherklar.de/?ich=1 aufrufen, dann misst Umami in diesem Browser nicht mehr
# (Umami beachtet den Eintrag umami.disabled im localStorage). ?ich=0 hebt das auf. Der Parameter wird danach
# aus der Adresse entfernt, damit er nicht versehentlich geteilt wird. Läuft vor dem Umami-Skript (das ist defer).
OPTOUT_JS = ("<script>try{var u=new URL(location.href),q=u.searchParams.get('ich');"
             "if(q==='1')localStorage.setItem('umami.disabled','1');else if(q==='0')localStorage.removeItem('umami.disabled');"
             "if(q!==null){u.searchParams.delete('ich');history.replaceState(null,'',u.pathname+u.search+u.hash);"
             "console.info('Speicherklar: Zählung in diesem Browser '+(q==='1'?'aus':'an'));}}catch(e){}</script>")

def analytics():
    return OPTOUT_JS + f'<script defer src="{UMAMI_SRC}" data-website-id="{UMAMI_ID}" data-domains="speicherklar.de"></script>' if UMAMI_ID else ""

LOGO = ('<svg width="26" height="26" viewBox="0 0 26 26" aria-hidden="true">'
        '<rect x="5" y="4" width="16" height="20" rx="2.5" fill="none" stroke="currentColor" stroke-width="2"/>'
        '<rect x="10" y="1.5" width="6" height="3" rx="1" fill="currentColor"/>'
        '<rect x="8" y="14" width="10" height="7" rx="1" fill="var(--sun)"/></svg>')


# Burger-Menü für kleine Bildschirme. Ohne JavaScript bleibt die Navigation einfach sichtbar.
BURGER = ('<svg width="22" height="22" viewBox="0 0 22 22" aria-hidden="true">'
          '<path class="l1" d="M3 6h16"/><path class="l2" d="M3 11h16"/><path class="l3" d="M3 16h16"/></svg>')

MENU_JS = """<script>(function(){var h=document.querySelector('header.top');if(!h)return;var b=h.querySelector('.menu-btn'),n=h.querySelector('nav');h.classList.add('js');
function set(o){h.classList.toggle('open',o);b.setAttribute('aria-expanded',o);b.setAttribute('aria-label',o?'Menü schließen':'Menü öffnen');}
b.addEventListener('click',function(){set(!h.classList.contains('open'))});
n.addEventListener('click',function(e){if(e.target.closest('a'))set(false)});
document.addEventListener('keydown',function(e){if(e.key==='Escape'&&h.classList.contains('open')){set(false);b.focus()}});
document.addEventListener('click',function(e){if(h.classList.contains('open')&&!h.contains(e.target))set(false)});
matchMedia('(min-width:841px)').addEventListener('change',function(m){if(m.matches)set(false)});})();</script>"""


def header(prefix="./", active=None):
    def item(href, label, key=None):
        cur = ' aria-current="page"' if key and key == active else ""
        return f'<a href="{href}"{cur}>{label}</a>'
    nav = "".join([
        item(f"{prefix}#rechner", "Rechner", "rechner"),
        item(f"{prefix}pro/", "Speicherklar Pro", "pro"),
        item(f"{prefix}so-gehts/", "So geht's", "sogehts"),
        item(f"{prefix}ratgeber/", "Ratgeber", "ratgeber"),
        item(f"{prefix}#annahmen", "Annahmen"),
        item(f"{prefix}ueber-mich.html", "Über mich", "ueber"),
        f'<a href="{IG}" target="_blank" rel="noopener">Instagram</a>',
    ])
    return f"""<header class="top">
  <div class="wrap">
    <a class="brand" href="{prefix}" aria-label="Speicherklar, zur Startseite">
      {LOGO}
      Speicherklar
    </a>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="hauptmenu" aria-label="Menü öffnen">{BURGER}</button>
    <nav id="hauptmenu" aria-label="Seitenbereiche">{nav}</nav>
  </div>
</header>
{MENU_JS}"""


# Erklärvideo (Speicherklar und Speicherklar Pro, ca. 75 s). Dateien liegen selbst gehostet unter video/,
# kein YouTube und kein fremder Server. Solange "quer" leer ist, gibt es keine Video-Knöpfe und kein Overlay,
# und /so-gehts/ steht mit noindex und Platzhalter außerhalb der Sitemap.
# quer: 16:9 (Desktop) · hoch: 9:16 oder 4:5 (Handy hochkant, optional) · bild: Vorschaubild 16:9 (JPG)
# untertitel: WebVTT, optional · dauer: ISO 8601, z. B. "PT1M15S" · datum: Tag der Veröffentlichung (JJJJ-MM-TT)
VIDEO = {"quer": "video/erklaer-16x9.mp4", "hoch": "video/erklaer-9x16.mp4", "bild": "video/erklaer.jpg", "untertitel": "", "dauer": "PT1M13S", "datum": "2026-11-15"}

def video_live():
    return bool(VIDEO["quer"])

PLAY = ('<svg width="16" height="16" viewBox="0 0 16 16" aria-hidden="true"><circle cx="8" cy="8" r="7.25" fill="none" stroke="currentColor" stroke-width="1.5"/>'
        '<path d="M6.5 5.2v5.6L11 8z" fill="currentColor"/></svg>')

def video_trigger(ort, label="In 75 Sekunden erklärt"):
    """Knopf, der das Erklärvideo im Overlay öffnet. ort = wo der Knopf steht (für Umami). Leer, solange kein Video da ist."""
    if not video_live(): return ""
    return f'<button type="button" class="vid-open" data-vid-ort="{ort}">{PLAY} <span>{label}</span></button>'

def video_tag(prefix, cls="vid-player", preload="none"):
    """Video-Element mit Quer- und Hochkant-Fassung; die Auswahl trifft VIDEO_JS je nach Bildschirm."""
    v = VIDEO
    attrs = f' data-quer="{prefix}{v["quer"]}"' + (f' data-hoch="{prefix}{v["hoch"]}"' if v["hoch"] else "")
    poster = f' poster="{prefix}{v["bild"]}"' if v["bild"] else ""
    track = f'<track kind="subtitles" srclang="de" label="Deutsch" src="{prefix}{v["untertitel"]}" default>' if v["untertitel"] else ""
    return f'<video class="{cls}" controls playsinline preload="{preload}"{poster}{attrs}>{track}</video>'

# Overlay: <dialog> mit Video, darunter die eine Bitte „Rechner starten“. Zählt video-open (Overlay geöffnet, mit Ort),
# video-start (Wiedergabe läuft, einmal je Seitenaufruf), video-ende (bis zum Schluss gesehen) und video-cta (Klick auf Rechner starten).
VIDEO_JS = """<script>(function(){var T=function(n,d){try{window.umami&&umami.track(n,d)}catch(e){}};
var hoch=matchMedia('(max-width:760px) and (orientation:portrait)');
function src(v){var s=(hoch.matches&&v.dataset.hoch)||v.dataset.quer;if(v.getAttribute('src')!==s)v.setAttribute('src',s);}
document.querySelectorAll('video[data-quer]').forEach(function(v){src(v);var st=false,done=false;
v.addEventListener('playing',function(){if(!st){st=true;T('video-start',{ort:v.dataset.ort||'seite'})}});
v.addEventListener('ended',function(){if(!done){done=true;T('video-ende',{ort:v.dataset.ort||'seite'})}});});
var d=document.getElementById('vid-dlg');if(!d||!d.showModal)return;var v=d.querySelector('video'),ort='';
function zu(){v.pause();d.close();}
document.addEventListener('click',function(e){var b=e.target.closest('.vid-open');if(!b)return;ort=b.dataset.vidOrt||'';v.dataset.ort=ort;src(v);d.showModal();T('video-open',{ort:ort});try{v.play()}catch(x){}});
d.querySelector('.vid-x').addEventListener('click',zu);
d.addEventListener('click',function(e){if(e.target===d)zu()});
d.addEventListener('close',function(){v.pause()});
// „Rechner starten“: Overlay immer schließen. Liegt der Rechner auf derselben Seite (Startseite), selbst hinscrollen,
// sonst bleibt das modale Fenster offen und es passiert sichtbar nichts (gesehen in Safari auf dem iPhone).
d.querySelector('.vid-cta').addEventListener('click',function(e){T('video-cta',{ort:ort});var a=this,u=new URL(a.href,location.href);zu();
if(u.pathname===location.pathname){var t=document.querySelector(u.hash);if(t){e.preventDefault();history.replaceState(null,'',u.hash);setTimeout(function(){t.scrollIntoView({behavior:matchMedia('(prefers-reduced-motion:reduce)').matches?'auto':'smooth',block:'start'})},30);}}});
d.querySelector('.vid-more').addEventListener('click',function(){zu()});})();</script>"""

def video_overlay(prefix):
    if not video_live(): return ""
    return f"""<dialog class="vid-dlg" id="vid-dlg" aria-label="Erklärvideo Speicherklar">
  <div class="vid-box">
    <button type="button" class="vid-x" aria-label="Video schließen"><svg width="18" height="18" viewBox="0 0 18 18" aria-hidden="true"><path d="M4 4l10 10M14 4L4 14" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg></button>
    {video_tag(prefix)}
    <div class="vid-foot"><a class="btn btn-on btn-sun vid-cta" href="{prefix}#rechner">Rechner starten</a> <a class="vid-more" href="{prefix}so-gehts/">Mehr dazu</a></div>
  </div>
</dialog>
{VIDEO_JS}"""


# ---------- Klara, die KI-Hilfe (Worker in worker-klara/) ----------
# api: Adresse des Workers. Leer = kein Widget, kein Abschnitt in der Datenschutzerklärung.
# aktiv: False = nur sichtbar in Browsern, in denen einmal ?klara=1 aufgerufen wurde (zum Testen, ?klara=0 nimmt es weg).
#        True = für alle sichtbar. Erst nach Test und Freigabe durch Manuel umstellen.
KLARA = {"api": "https://speicherklar-klara.speicherklar.workers.dev", "aktiv": True}

def klara_live():
    return bool(KLARA["api"])

def klara_avatar(size=40):
    """Zählerrolle mit Fragezeichen in einer dunklen Sprechblase (Spitze unten links), gesichtslos.
    Feste Farben, passt in Hell und Dunkel."""
    return (f'<svg class="kl-ava" width="{size}" height="{size}" viewBox="0 0 40 40" aria-hidden="true">'
            '<defs><linearGradient id="kl-rolle" x1="0" y1="0" x2="0" y2="1">'
            '<stop offset="0" stop-color="#000"/><stop offset=".14" stop-color="#2a2f35"/><stop offset=".5" stop-color="#15191d"/>'
            '<stop offset=".86" stop-color="#2a2f35"/><stop offset="1" stop-color="#000"/></linearGradient></defs>'
            '<path d="M9 0h22a9 9 0 0 1 9 9v17a9 9 0 0 1-9 9H15.5L6.5 40.5 8.2 34.8A9 9 0 0 1 0 26V9a9 9 0 0 1 9-9z" fill="#15212B"/>'
            '<rect x="11.5" y="4" width="17" height="26.5" rx="3" fill="url(#kl-rolle)" stroke="#56666F" stroke-width="1"/>'
            '<path d="M7.5 17.25h3.5M29 17.25h3.5" stroke="#E39A0B" stroke-width="2.4" stroke-linecap="round"/>'
            '<path d="M16.6 14a3.5 3.5 0 1 1 5.3 3c-1.15.7-1.85 1.35-1.85 2.6v.6" fill="none" stroke="#EDF0F2" stroke-width="2.2" stroke-linecap="round"/>'
            '<circle cx="20.05" cy="24.3" r="1.45" fill="#EDF0F2"/></svg>')

KLARA_CSS = """<style>
.kl-fab{position:fixed;z-index:40;right:max(16px,env(safe-area-inset-right,0px));bottom:max(16px,env(safe-area-inset-bottom,0px));display:flex;align-items:center;gap:10px;padding:6px 16px 6px 6px;border:1px solid var(--line);border-radius:999px;background:var(--surface);color:var(--ink);font:inherit;font-weight:700;cursor:pointer;box-shadow:0 6px 24px rgba(10,20,30,.18);transition:transform .15s ease}
.kl-fab:hover{transform:translateY(-1px)} .kl-fab .kl-ava{display:block}
.kl-fab[aria-expanded="true"]{display:none}
body:has(#rbar.show) .kl-fab{bottom:calc(max(10px,env(safe-area-inset-bottom,0px)) + 84px)}
@media (max-width:560px){.kl-fab{padding:4px;gap:0}.kl-fab .kl-ava{width:36px;height:36px}
 .kl-fab-t{max-width:0;overflow:hidden;white-space:nowrap;opacity:0;transition:max-width .35s ease,opacity .25s ease,margin .35s ease}
 .kl-fab.hinweis{padding-right:14px}.kl-fab.hinweis .kl-fab-t{max-width:120px;opacity:1;margin-left:8px}
 .kl-fab.spaeter{opacity:0;visibility:hidden;transform:translateY(12px);transition:opacity .2s ease,transform .2s ease,visibility 0s .2s}
 .kl-fab{transition:opacity .2s ease,transform .2s ease}}
.kl-panel{position:fixed;z-index:41;right:max(16px,env(safe-area-inset-right,0px));bottom:max(16px,env(safe-area-inset-bottom,0px));width:min(390px,calc(100vw - 32px));height:min(620px,calc(100svh - 110px));display:flex;flex-direction:column;background:var(--surface);color:var(--ink);border:1px solid var(--line);border-radius:16px;box-shadow:0 18px 60px rgba(10,20,30,.28);overflow:hidden}
.kl-panel[hidden]{display:none}
@media (max-width:560px){.kl-panel{left:0;right:0;bottom:0;width:100%;height:min(88svh,calc(100svh - 40px));border-radius:16px 16px 0 0;border-bottom:0}}
.kl-head{display:flex;align-items:center;gap:10px;padding:12px 12px 12px 14px;border-bottom:1px solid var(--line)}
.kl-head div{flex:1;min-width:0;display:grid;gap:1px} .kl-head b{font-size:16px}
.kl-head span{font-size:12.5px;color:var(--muted)}
.kl-x,.kl-neu{border:0;background:none;color:var(--muted);cursor:pointer;font:inherit}
.kl-neu{width:40px;height:40px;display:grid;place-items:center;border-radius:999px} .kl-neu:hover{background:var(--bg);color:var(--ink)} .kl-neu[hidden]{display:none}
.kl-frage{align-self:stretch;display:grid;gap:8px;padding:12px;border:1px solid var(--line);border-radius:12px;background:var(--surface);font-size:14.5px}
.kl-frage div{display:flex;gap:8px;flex-wrap:wrap} .kl-frage button{border:1px solid var(--line);border-radius:999px;padding:7px 14px;font:inherit;font-weight:700;cursor:pointer;background:var(--surface);color:var(--ink)} .kl-frage .ja{background:var(--sun);border-color:var(--sun);color:var(--btn-ink)}
.kl-x{width:40px;height:40px;display:grid;place-items:center;border-radius:999px;flex:none} .kl-x:hover{background:var(--bg);color:var(--ink)}
.kl-log{flex:1;overflow-y:auto;padding:14px;display:flex;flex-direction:column;gap:10px;overscroll-behavior:contain}
.kl-m{max-width:88%;padding:9px 12px;border-radius:14px;line-height:1.45;font-size:15px;overflow-wrap:anywhere}
.kl-m p{margin:0} .kl-m small{color:var(--muted);font-size:13px} .kl-m small a{color:inherit} .kl-m p+p,.kl-m ul{margin-top:6px} .kl-m ul{margin-bottom:0;padding-left:18px}
.kl-k{align-self:flex-start;background:var(--bg);border-bottom-left-radius:4px}
.kl-i{align-self:flex-end;background:var(--ink);color:var(--bg);border-bottom-right-radius:4px}
.kl-err{color:var(--muted);font-style:italic}
.kl-wait::after{content:"…";display:inline-block;animation:kl-p 1s steps(3) infinite;width:1.2em;overflow:hidden;vertical-align:bottom}
@keyframes kl-p{from{width:0}to{width:1.2em}}
.kl-fb{align-self:flex-start;display:flex;align-items:center;gap:2px;margin:-4px 0 0 4px;font-size:12.5px;color:var(--muted)}
.kl-fb button{width:32px;height:32px;display:grid;place-items:center;border:0;border-radius:999px;background:none;color:var(--muted);cursor:pointer} .kl-fb button:hover{background:var(--bg);color:var(--ink)}
.kl-fb span{margin-right:4px}
.kl-btn{align-self:flex-start;display:inline-block;padding:9px 14px;border-radius:999px;background:var(--sun);color:var(--btn-ink);font-weight:700;text-decoration:none;font-size:14.5px}
.kl-form{display:flex;gap:8px;align-items:flex-end;padding:10px 12px 6px;border-top:1px solid var(--line)}
.kl-form textarea{flex:1;resize:none;max-height:120px;min-height:42px;padding:10px 12px;border:1px solid var(--line);border-radius:12px;background:var(--bg);color:var(--ink);font:inherit;font-size:16px;line-height:1.35}
.kl-form textarea:focus{outline:2px solid var(--sun);outline-offset:0;border-color:transparent}
.kl-send{flex:none;width:42px;height:42px;border:0;border-radius:12px;background:var(--sun);color:var(--btn-ink);display:grid;place-items:center;cursor:pointer}
.kl-send:disabled{opacity:.5;cursor:default}
.kl-foot{margin:0;padding:2px 14px 12px;font-size:12.5px;color:var(--muted)} .kl-foot a{color:inherit}
@media (prefers-reduced-motion:reduce){.kl-fab,.kl-fab-t{transition:none!important}.kl-wait::after{animation:none;width:auto}}
</style>"""

def klara_widget(prefix="./"):
    if not klara_live(): return ""
    send = ('<svg width="18" height="18" viewBox="0 0 18 18" aria-hidden="true"><path d="M2.5 9h11M9.5 4l5 5-5 5" fill="none" stroke="currentColor" '
            'stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>')
    close = ('<svg width="18" height="18" viewBox="0 0 18 18" aria-hidden="true"><path d="M4 4l10 10M14 4L4 14" stroke="currentColor" stroke-width="2" '
             'stroke-linecap="round"/></svg>')
    neu = ('<svg width="18" height="18" viewBox="0 0 18 18" aria-hidden="true"><path d="M3.2 9a5.8 5.8 0 1 0 1.9-4.3" fill="none" stroke="currentColor" '
           'stroke-width="2" stroke-linecap="round"/><path d="M4.6 1.8v3.4H8" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>')
    js = KLARA_JS.replace("%API%", KLARA["api"]).replace("%AKTIV%", "true" if KLARA["aktiv"] else "false")
    return f"""<div class="kl" id="kl-root" hidden>
  <button type="button" class="kl-fab" aria-expanded="false" aria-controls="kl-panel">{klara_avatar(40)} <span class="kl-fab-t">Frag Klara</span></button>
  <section class="kl-panel" id="kl-panel" role="dialog" aria-label="Klara, die KI-Assistentin von Speicherklar" hidden>
    <div class="kl-head">{klara_avatar(36)} <div><b>Klara</b> <span>KI-Assistentin von Speicherklar. Antworten können Fehler enthalten.</span></div> <button type="button" class="kl-neu" aria-label="Gespräch neu starten" title="Gespräch neu starten" hidden>{neu}</button> <button type="button" class="kl-x" aria-label="Chat schließen">{close}</button></div>
    <div class="kl-log" aria-live="polite"></div>
    <form class="kl-form"><label class="sr-only" for="kl-in">Deine Frage an Klara</label> <textarea id="kl-in" rows="1" maxlength="600" placeholder="Deine Frage …"></textarea> <button type="submit" class="kl-send" aria-label="Frage senden">{send}</button></form>
    <p class="kl-foot">Lieber direkt an Manuel? <a class="kl-mail" href="mailto:kontakt@speicherklar.de">kontakt@speicherklar.de</a> · <a href="{prefix}datenschutz.html#klara">Datenschutz</a></p>
  </section>
</div>
{KLARA_CSS}
{js}"""

# Chat-Logik. Verlauf nur im sessionStorage dieses Tabs (bleibt beim Seitenwechsel, weg beim Schließen).
# Umami: klara-open, klara-frage (ohne Inhalt), klara-knopf (ziel), klara-mail. Mail-Links zählen per umami.track, nie data-umami-event.
# Daumen unter Klaras Antworten gehen an /feedback des Workers (nur Thema und hoch/runter, kein Inhalt), nicht an Umami.
KLARA_JS = r"""<script>(function(){var C={api:"%API%",aktiv:%AKTIV%};
try{var u=new URL(location.href),q=u.searchParams.get('klara');if(q==='1')localStorage.setItem('klara.test','1');else if(q==='0')localStorage.removeItem('klara.test');
if(q!==null){u.searchParams.delete('klara');history.replaceState(null,'',u.pathname+u.search+u.hash);}}catch(e){}
var test=false;try{test=localStorage.getItem('klara.test')==='1'}catch(e){}
var R=document.getElementById('kl-root');if(!R||!C.api||!(C.aktiv||test)||!window.fetch||!window.crypto||!crypto.subtle)return;R.hidden=false;
var T=function(n,d){try{window.umami&&umami.track(n,d)}catch(e){}};
var S={get:function(k){try{return JSON.parse(sessionStorage.getItem(k))}catch(e){return null}},set:function(k,v){try{sessionStorage.setItem(k,JSON.stringify(v))}catch(e){}}};
var fab=R.querySelector('.kl-fab'),P=R.querySelector('.kl-panel'),L=R.querySelector('.kl-log'),F=R.querySelector('.kl-form'),I=F.querySelector('textarea'),B=F.querySelector('.kl-send'),NEU=R.querySelector('.kl-neu');
var V=S.get('klara.verlauf')||[],tok=S.get('klara.token'),busy=false,stat=null,MAX=10,MAIL='kontakt@speicherklar.de';
var DS=R.querySelector('.kl-foot a[href*="datenschutz"]').getAttribute('href'),pfad=location.pathname,ort=/\/pro\//.test(pfad)?'pro':/\/ratgeber\/./.test(pfad)?'artikel':(document.getElementById('inputs')?'start':'seite');
function esc(s){return s.replace(/[&<>"']/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]})}
function fmt(t){var o='',li=false;esc(t).split(/\n/).forEach(function(z){z=z.replace(/\*\*(.+?)\*\*/g,'<b>$1</b>');var m=z.match(/^\s*[-•]\s+(.*)/);
 if(m){if(!li){o+='<ul>';li=true}o+='<li>'+m[1]+'</li>';return}if(li){o+='</ul>';li=false}if(z.trim())o+='<p>'+z+'</p>'});return o+(li?'</ul>':'')}
function mailto(){var b='Hallo Manuel,\n\n\n\n';var m=V.filter(function(x){return x.text&&!x.nicht});if(m.length){b+='---\nMein Chat mit Klara (KI-Assistentin):\n';
 m.forEach(function(x){b+=(x.rolle==='ich'?'Ich: ':'Klara: ')+x.text+'\n'})}var s='mailto:'+MAIL+'?subject='+encodeURIComponent('Frage an Speicherklar')+'&body=';
 var e=encodeURIComponent(b);if(e.length>1800)e=encodeURIComponent(b.slice(0,1100)+'\n[gekürzt]');return s+e}
function el(tag,cls,html){var e=document.createElement(tag);if(cls)e.className=cls;if(html!=null)e.innerHTML=html;return e}
function knopfEl(k){var a=el('a','kl-btn');a.textContent=k.text;
 if(k.ziel==='mail'){a.href=mailto();a.addEventListener('click',function(){a.href=mailto();T('klara-mail',{ort:ort})})}
 else{a.href=k.url;a.addEventListener('click',function(){T('klara-knopf',{ziel:k.ziel,ort:ort});if(new URL(k.url).pathname===pfad)zu(false)})}return a}
var HOCH='<svg width="16" height="16" viewBox="0 0 16 16" aria-hidden="true"><path d="M5 7l2.6-5c1.2 0 2 .9 1.8 2.1L9 6.5h3.6c.9 0 1.6.9 1.4 1.8l-1 4.6c-.2.7-.8 1.1-1.4 1.1H5zM1.5 7H5v7H1.5z" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/></svg>';
var RUNTER=HOCH.replace('aria-hidden="true"','aria-hidden="true" style="transform:rotate(180deg)"');
function daumenEl(m){var d=el('div','kl-fb');if(m.daumen){d.textContent='Danke fürs Feedback.';return d}
 d.appendChild(el('span',null,'Hilfreich?'));[['hoch',HOCH,'Ja, hilfreich'],['runter',RUNTER,'Nein, nicht hilfreich']].forEach(function(w){var b=el('button',null,w[1]);b.type='button';b.setAttribute('aria-label',w[2]);b.title=w[2];
  b.addEventListener('click',function(){var fb=m.fb;m.daumen=w[0];delete m.fb;sichern();d.replaceWith(daumenEl(m));
   fetch(C.api+'/feedback',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({fb:fb,wert:w[0]})}).catch(function(){})});d.appendChild(b)});return d}
function zeigen(){L.innerHTML='';var g=el('div','kl-m kl-k',fmt('Hi, ich bin Klara, die KI-Assistentin von Speicherklar. Ich beantworte deine Fragen zum Rechner, zu Speicherklar Pro und rund um PV-Anlage und Speicher. Ich bin eine KI und kann mich irren.')+'<p><small>Deine Fragen gehen zum Beantworten an Anthropic (Claude). Speicherklar speichert sie nicht. <a href="'+DS+'">Datenschutz</a></small></p>');L.appendChild(g);
 if(abgelaufen)L.appendChild(el('div','kl-m kl-k kl-err',fmt('Dein letztes Gespräch war über 30 Minuten still, deshalb habe ich es gelöscht.')));

 V.forEach(function(m){var d=el('div','kl-m '+(m.rolle==='ich'?'kl-i':'kl-k')+(m.fehler?' kl-err':''),m.rolle==='ich'?'<p>'+esc(m.text)+'</p>':fmt(m.text||m.fehler||''));L.appendChild(d);if(m.knopf)L.appendChild(knopfEl(m.knopf));if(m.fb||m.daumen)L.appendChild(daumenEl(m))});
 if(stat&&!stat.on)L.appendChild(el('div','kl-m kl-k',fmt(stat.grund==='budget'?'Ich mache gerade Pause und bin am Monatsersten wieder da. Bis dahin: Schreib Manuel an '+MAIL+'.':'Ich bin gerade nicht da. Schreib Manuel an '+MAIL+'.')));
 var n=V.filter(function(m){return m.rolle==='ich'&&!m.nicht}).length;if(n>=MAX)L.appendChild(el('div','kl-m kl-k kl-err',fmt('Für dieses Gespräch sind die Fragen aufgebraucht. Mit dem Pfeil oben („Neu starten“) geht es weiter.')));
 NEU.hidden=!V.length;var aus=(stat&&!stat.on)||n>=MAX;I.disabled=aus;B.disabled=aus||busy;L.scrollTop=L.scrollHeight;R.querySelector('.kl-mail').href=mailto()}
function sichern(){S.set('klara.verlauf',V);S.set('klara.zeit',Date.now())}
// Nach 30 Minuten ohne Aktivität ist das Gespräch weg (wie das Token); Hinweis einmal im Fenster
var STILL=30*60000,abgelaufen=false;function ablauf(){var z=S.get('klara.zeit')||0;if(V.length&&Date.now()-z>STILL){V=[];abgelaufen=true;S.set('klara.verlauf',V);return true}return false}ablauf();
function werte(){if(ort!=='start')return null;var g=function(i){var e=document.getElementById(i);return e?e.textContent.trim():''};
 var p=function(i){var e=document.querySelector('#'+i+' [aria-pressed="true"]');return e?e.textContent.trim():''};
 var plz=(document.getElementById('plz')||{}).value||'';
 return{region:plz.replace(/\D/g,'').slice(0,1),ausrichtung:p('aspect'),neigung:g('o-tilt'),pv:g('o-pv'),verbrauch:g('o-cons'),waermepumpe:g('o-hp'),eauto:g('o-ev'),laden:+((document.getElementById('ev')||{}).value||0)>0?p('evtime'):'',
  speicher:g('o-bat'),speicherpreis:g('o-bprice'),lebensdauer:g('o-life'),strompreis:g('o-price'),eeg:p('eeg'),einspeisung:g('o-feed'),
  urteil:g('verdict'),ersparnis:g('k-save'),amortisation:g('k-pay'),kosten:g('k-cost'),bilanz:g('k-net')+' '+g('k-netd'),autarkie:g('b-aut'),beste:g('sweepsum')}}
function nb(h){var n=0;for(var i=0;i<h.length;i++){if(h[i]===0){n+=8;continue}n+=Math.clz32(h[i])-24;break}return n}
async function loesen(a,bits){var e=new TextEncoder();for(var s=0;s<4e6;s+=256){var ps=[];for(var n=s;n<s+256;n++)ps.push(crypto.subtle.digest('SHA-256',e.encode(a+':'+n)));
 var hs=await Promise.all(ps);for(var j=0;j<hs.length;j++)if(nb(new Uint8Array(hs[j]))>=bits)return String(s+j)}throw new Error('pow')}
var tokP=null;function token(neu){if(neu)tok=null;if(tok&&tok.exp>Date.now()+60000)return Promise.resolve(tok.t);
 if(!tokP)tokP=(async function(){var s=await(await fetch(C.api+'/start',{method:'POST',headers:{'Content-Type':'application/json'},body:'{}'})).json();
  var nonce=await loesen(s.aufgabe,s.bits);var r=await fetch(C.api+'/session',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({aufgabe:s.aufgabe,nonce:nonce})});
  if(!r.ok)throw new Error('session');var t=(await r.json()).token,exp=Date.now()+25*60000;try{exp=JSON.parse(atob(t.split('.')[0].replace(/-/g,'+').replace(/_/g,'/'))).exp}catch(e){}
  tok={t:t,exp:exp};S.set('klara.token',tok);return t})().finally(function(){tokP=null});return tokP}
var FEHLER={langsam:'Kurz durchatmen: Gerade kommen zu viele Fragen auf einmal. Versuch es gleich noch mal.',lang:'Die Frage ist zu lang. Magst du sie kürzer fassen?',genug:'Für dieses Gespräch sind die Fragen aufgebraucht. Mit dem Pfeil oben („Neu starten“) geht es weiter.',
 voll:'Ich komme gerade nicht durch. Versuch es gleich noch mal, oder schreib Manuel an '+MAIL+'.',api:'Da ist etwas schiefgegangen. Versuch es noch mal, oder schreib Manuel an '+MAIL+'.'};
async function frage(text){text=(text||'').trim();if(!text||busy)return;if(ablauf())zeigen();if(text.length>600){text=text.slice(0,600)}busy=true;I.value='';groesse();
 var q={rolle:'ich',text:text},a={rolle:'klara',text:''};V.push(q);sichern();zeigen();T('klara-frage',{ort:ort});
 var box=el('div','kl-m kl-k kl-wait');L.appendChild(box);L.scrollTop=L.scrollHeight;
 function fehlschlag(f){q.nicht=true;a.nicht=true;a.fehler=f;a.text='';V.push(a);sichern()}
 try{var send=V.filter(function(m){return!m.nicht&&m.text}).map(function(m){return{rolle:m.rolle,text:m.text}});
  var r,versuch=0;for(;;){var t=await token(versuch>0);r=await fetch(C.api+'/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({token:t,seite:pfad,werte:werte(),verlauf:send})});
   if(r.status===401&&versuch===0){versuch++;continue}break}
  if(!r.ok){var j={};try{j=await r.json()}catch(e){}if(j.error==='pause'){stat={on:false,grund:j.grund};q.nicht=true;sichern()}else fehlschlag(FEHLER[j.error]||FEHLER.api);return}
  var rd=r.body.getReader(),dec=new TextDecoder(),buf='',ok=false;box.classList.remove('kl-wait');
  for(;;){var x=await rd.read();if(x.done)break;buf+=dec.decode(x.value,{stream:true});var i;while((i=buf.indexOf('\n\n'))>=0){var line=buf.slice(0,i);buf=buf.slice(i+2);if(line.indexOf('data: ')!==0)continue;
   var d;try{d=JSON.parse(line.slice(6))}catch(e){continue}
   if(d.t==='text'){a.text+=d.v;box.innerHTML=fmt(a.text);L.scrollTop=L.scrollHeight}else if(d.t==='knopf'){a.knopf={ziel:d.ziel,text:d.text,url:d.url}}else if(d.t==='ende'){ok=true;if(d.fb)a.fb=d.fb}else if(d.t==='fehler'){fehlschlag(FEHLER[d.grund]||FEHLER.api);return}}}
  if(!ok&&!a.text){fehlschlag(FEHLER.api);return}V.push(a);sichern()}
 catch(e){fehlschlag(FEHLER.api)}finally{busy=false;zeigen();if(!I.disabled)I.focus()}}
function groesse(){I.style.height='auto';I.style.height=Math.min(I.scrollHeight,120)+'px'}
async function auf(){ablauf();P.hidden=false;fab.setAttribute('aria-expanded','true');S.set('klara.offen',1);zeigen();if(matchMedia('(min-width:561px)').matches)I.focus();T('klara-open',{ort:ort});
 if(!stat){try{stat=await(await fetch(C.api+'/status')).json()}catch(e){stat={on:false,grund:'aus'}}zeigen()}}
var vor=function(){if(stat&&stat.on&&!tok&&!tokP)token().catch(function(){})};I.addEventListener('focus',vor);I.addEventListener('input',vor);
function zu(fokus){P.hidden=true;fab.setAttribute('aria-expanded','false');S.set('klara.offen',0);if(fokus!==false)fab.focus()}
fab.addEventListener('click',auf);R.querySelector('.kl-x').addEventListener('click',zu);
NEU.addEventListener('click',function(){if(busy||L.querySelector('.kl-frage'))return;var f=el('div','kl-frage','<p>Gespräch neu starten? Der bisherige Verlauf wird gelöscht.</p>');
 var d=el('div'),ja=el('button','ja'),nein=el('button');ja.type=nein.type='button';ja.textContent='Neu starten';nein.textContent='Abbrechen';d.appendChild(ja);d.appendChild(nein);f.appendChild(d);
 L.appendChild(f);L.scrollTop=L.scrollHeight;nein.focus();
 nein.addEventListener('click',function(){f.remove();NEU.focus()});ja.addEventListener('click',function(){V=[];abgelaufen=false;sichern();zeigen();I.focus()})});
P.addEventListener('keydown',function(e){if(e.key==='Escape')zu()});
F.addEventListener('submit',function(e){e.preventDefault();frage(I.value)});
I.addEventListener('keydown',function(e){if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();frage(I.value)}});I.addEventListener('input',groesse);
R.querySelector('.kl-mail').addEventListener('click',function(){this.href=mailto();T('klara-mail',{ort:ort})});
var handy=matchMedia('(max-width:560px)');
function scroll(){var weg=handy.matches&&!V.length&&window.scrollY<innerHeight*0.6;fab.classList.toggle('spaeter',weg);
 if(!weg&&handy.matches&&!gezeigt){gezeigt=true;var schon=false;schon=S.get('klara.hinweis')===1;S.set('klara.hinweis',1);
  if(!schon){fab.classList.add('hinweis');setTimeout(function(){fab.classList.remove('hinweis')},4500)}}}
var gezeigt=false;addEventListener('scroll',scroll,{passive:true});handy.addEventListener('change',scroll);scroll();
if(S.get('klara.offen')===1&&V.length)auf();})();</script>"""


def footer(prefix="./"):
    return video_overlay(prefix) + klara_widget(prefix) + f"""<footer>
  <div class="wrap">
    <span>Speicherklar ist eine Schätzung, keine Anlagen- oder Finanzberatung. Für eine Kaufentscheidung hol dir Angebote von Fachbetrieben.</span>
    <span>Unabhängig: kein Geld von Herstellern oder Installateuren, keine Werbung. Der Rechenweg ist <a href="{prefix}methodik.html">offen</a>.</span>
    <span>Sonnendaten: PVGIS © Europäische Union, 2001–2026.</span>
    <span><a href="{IG}" target="_blank" rel="noopener">Instagram @speicherklar</a> · <a href="{prefix}methodik.html">Methodik</a> · <a href="{prefix}ueber-mich.html">Über mich</a> · <a href="{prefix}kontakt.html">Kontakt</a> · <a href="{prefix}impressum.html">Impressum</a> · <a href="{prefix}datenschutz.html">Datenschutz</a></span>
  </div>
</footer>"""


SITE = "https://speicherklar.de"

def head_meta(og_image=None, og_alt=""):
    """Icons für Browser und Homescreen, Web-App-Manifest und Vorschaubild für geteilte Links."""
    # Google-Suchergebnis: eigene Datei, Vielfaches von 48 px. favicon.ico liegt zusätzlich im Hauptordner.
    s = ('<link rel="icon" href="/favicon.ico" sizes="48x48">'
         '<link rel="icon" href="/favicon.svg" type="image/svg+xml">'
         '<link rel="icon" href="/img/favicon-96.png" sizes="96x96" type="image/png">'
         '<link rel="apple-touch-icon" href="/apple-touch-icon.png">'
         '<link rel="manifest" href="/site.webmanifest">'
         '<meta name="apple-mobile-web-app-title" content="Speicherklar">'
         '<meta property="og:site_name" content="Speicherklar">')
    if og_image:
        url = og_image if og_image.startswith("http") else SITE + "/" + og_image.lstrip("/")
        w, h = ("1200", "630")
        s += (f'<meta property="og:image" content="{url}"><meta property="og:image:width" content="{w}">'
              f'<meta property="og:image:height" content="{h}"><meta property="og:image:alt" content="{og_alt}">'
              '<meta name="twitter:card" content="summary_large_image">')
    return s
