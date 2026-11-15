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


def footer(prefix="./"):
    return video_overlay(prefix) + f"""<footer>
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
