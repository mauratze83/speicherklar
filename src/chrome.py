"""Gemeinsame Kopf- und Fußzeile für alle Seiten von speicherklar.de.

prefix: Pfad zur Website-Wurzel aus Sicht der Seite ("./" für Seiten im Hauptordner, "../" für ratgeber/).
active: "rechner" | "ratgeber" | None – markiert den aktuellen Menüpunkt.
"""

IG = "https://www.instagram.com/speicherklar/"

LOGO = ('<svg width="26" height="26" viewBox="0 0 26 26" aria-hidden="true">'
        '<rect x="5" y="4" width="16" height="20" rx="2.5" fill="none" stroke="currentColor" stroke-width="2"/>'
        '<rect x="10" y="1.5" width="6" height="3" rx="1" fill="currentColor"/>'
        '<rect x="8" y="14" width="10" height="7" rx="1" fill="var(--sun)"/></svg>')


def header(prefix="./", active=None):
    def item(href, label, key=None):
        cur = ' aria-current="page"' if key and key == active else ""
        return f'<a href="{href}"{cur}>{label}</a>'
    nav = "".join([
        item(f"{prefix}#rechner", "Rechner", "rechner"),
        item(f"{prefix}ratgeber/", "Ratgeber", "ratgeber"),
        item(f"{prefix}#annahmen", "Annahmen"),
        item(f"{prefix}#pro", "Pro"),
        f'<a href="{IG}" target="_blank" rel="noopener">Instagram</a>',
    ])
    return f"""<header class="top">
  <div class="wrap">
    <a class="brand" href="{prefix}" aria-label="Speicherklar, zur Startseite">
      {LOGO}
      Speicherklar
    </a>
    <nav aria-label="Seitenbereiche">{nav}</nav>
  </div>
</header>"""


def footer(prefix="./"):
    return f"""<footer>
  <div class="wrap">
    <span>Speicherklar ist eine Schätzung, keine Anlagen- oder Finanzberatung. Für eine Kaufentscheidung hol dir Angebote von Fachbetrieben.</span>
    <span>Sonnendaten: PVGIS © Europäische Union, 2001–2026.</span>
    <span><a href="{IG}" target="_blank" rel="noopener">Instagram @speicherklar</a> · <a href="{prefix}impressum.html">Impressum</a> · <a href="{prefix}datenschutz.html">Datenschutz</a></span>
  </div>
</footer>"""
