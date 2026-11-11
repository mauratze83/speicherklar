"""Gemeinsame Kopf- und Fußzeile für alle Seiten von speicherklar.de.

prefix: Pfad zur Website-Wurzel aus Sicht der Seite ("./" für Seiten im Hauptordner, "../" für ratgeber/).
active: "rechner" | "ratgeber" | "pro" | None – markiert den aktuellen Menüpunkt.
"""

IG = "https://www.instagram.com/speicherklar/"

# Reichweitenmessung mit Umami Cloud (ohne Cookies). Leer = kein Skript und kein Abschnitt in der Datenschutzerklärung.
UMAMI_ID = "f4570047-b7d7-42e7-944e-a06941b94082"
UMAMI_SRC = "https://cloud.umami.is/script.js"

def analytics():
    return f'<script defer src="{UMAMI_SRC}" data-website-id="{UMAMI_ID}" data-domains="speicherklar.de"></script>' if UMAMI_ID else ""

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
matchMedia('(min-width:721px)').addEventListener('change',function(m){if(m.matches)set(false)});})();</script>"""


def header(prefix="./", active=None):
    def item(href, label, key=None):
        cur = ' aria-current="page"' if key and key == active else ""
        return f'<a href="{href}"{cur}>{label}</a>'
    nav = "".join([
        item(f"{prefix}#rechner", "Rechner", "rechner"),
        item(f"{prefix}ratgeber/", "Ratgeber", "ratgeber"),
        item(f"{prefix}#annahmen", "Annahmen"),
        item(f"{prefix}pro/", "Angebots-Check", "pro"),
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


def footer(prefix="./"):
    return f"""<footer>
  <div class="wrap">
    <span>Speicherklar ist eine Schätzung, keine Anlagen- oder Finanzberatung. Für eine Kaufentscheidung hol dir Angebote von Fachbetrieben.</span>
    <span>Unabhängig: kein Geld von Herstellern oder Installateuren, keine Werbung. Der Rechenweg ist <a href="{prefix}methodik.html">offen</a>.</span>
    <span>Sonnendaten: PVGIS © Europäische Union, 2001–2026.</span>
    <span><a href="{IG}" target="_blank" rel="noopener">Instagram @speicherklar</a> · <a href="{prefix}methodik.html">Methodik</a> · <a href="{prefix}ueber-mich.html">Über mich</a> · <a href="{prefix}impressum.html">Impressum</a> · <a href="{prefix}datenschutz.html">Datenschutz</a></span>
  </div>
</footer>"""


SITE = "https://speicherklar.de"

def head_meta(og_image=None, og_alt=""):
    """Icons für Browser und Homescreen, Web-App-Manifest und Vorschaubild für geteilte Links."""
    s = ('<link rel="icon" href="/img/favicon-32.png" sizes="32x32" type="image/png">'
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
