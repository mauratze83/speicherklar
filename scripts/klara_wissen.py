"""Erzeugt das Wissen für Klara (KI-Hilfe) aus den Quellen der Website: worker-klara/wissen.js.

Läuft am Ende von build.py. Ändert sich eine Quelle (Artikel, Methodik, Eingabefelder, Preise, Politik),
ändert sich wissen.js mit, und der Workflow „Klara“ veröffentlicht den Worker neu.
Ohne Quelländerung entsteht keine Änderung (keine Zeitstempel in der Datei).

Aufruf einzeln: python3 scripts/klara_wissen.py
"""
import datetime, html, json, pathlib, re, sys
from html.parser import HTMLParser

ROOT = pathlib.Path(__file__).resolve().parent.parent
S = ROOT / "src"
OUT = ROOT / "worker-klara" / "wissen.js"
SITE = "https://speicherklar.de/"
MAX_TOKENS = 60000  # grobe Obergrenze fürs Wissen; Haiku 5.5 kostet über 100.000 Tokens Prompt das Fünffache


class Text(HTMLParser):
    """HTML → lesbarer Text: Absätze, Listen, Tabellenzeilen mit |, Links mit Adresse. script/style/svg fallen weg."""
    SKIP = {"script", "style", "svg", "noscript"}
    BLOCK = {"p", "div", "section", "article", "h1", "h2", "h3", "h4", "li", "tr", "table", "ul", "ol", "details", "summary", "fieldset", "legend", "br", "figure", "figcaption"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out, self.skip, self.href = [], 0, []

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP: self.skip += 1; return
        if self.skip: return
        a = dict(attrs)
        if tag in ("h1", "h2", "h3", "h4"): self.out.append("\n\n" + "#" * int(tag[1]) + " ")
        elif tag == "li": self.out.append("\n- ")
        elif tag == "tr": self.out.append("\n| ")
        elif tag in ("td", "th"): pass
        elif tag in self.BLOCK: self.out.append("\n")
        if tag == "a": self.href.append(a.get("href") or "")

    def handle_endtag(self, tag):
        if tag in self.SKIP: self.skip -= 1; return
        if self.skip: return
        if tag in ("td", "th"): self.out.append(" | ")
        elif tag == "a" and self.href:
            h = self.href.pop()
            if h.startswith("http") and "speicherklar.de" not in h: self.out.append(f" ({h})")
        elif tag in self.BLOCK: self.out.append("\n")

    def handle_data(self, d):
        if not self.skip: self.out.append(d)

    def text(self):
        t = "".join(self.out)
        t = re.sub(r"[ \t\r\f\v]+", " ", t)
        t = re.sub(r" *\n *", "\n", t)
        t = re.sub(r"\|\s*\n", "|\n", t)
        return re.sub(r"\n{3,}", "\n\n", t).strip()


def txt(h):
    p = Text(); p.feed(h); return p.text()


def strip_tags(h):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", h))).strip()


# Einheiten der Regler im kostenlosen Rechner (die Anzeige kommt aus ui.js, nicht aus dem HTML)
UNITS = {"tilt": "°", "pv": "kWp", "cons": "kWh/Jahr", "hp": "kWh/Jahr", "ev": "kWh/Jahr", "bat": "kWh",
         "bprice": "€/kWh nutzbar", "life": "Jahre", "price": "ct/kWh", "feed": "ct/kWh"}


def felder(body, units):
    """Eingabefelder: Name, Art, Bereich, Startwert, Hinweis."""
    out = []
    for block in re.split(r'<div class="field', body)[1:]:
        block = block.split("</div></div>")[0] if "stepper" not in block else block
        lab = re.search(r'<label for="([^"]+)">(.*?)</label>', block, re.S)
        flab = re.search(r'class="flabel"[^>]*>(.*?)</span>', block, re.S)
        name = strip_tags(lab.group(2)) if lab else (strip_tags(flab.group(1)) if flab else None)
        if not name: continue
        fid = lab.group(1) if lab else ""
        line = f"- {name}"
        inp = re.search(r'<input[^>]*id="' + re.escape(fid) + r'"[^>]*>', block) if fid else None
        if inp:
            a = dict(re.findall(r'(\w[\w-]*)="([^"]*)"', inp.group(0)))
            u = units.get(fid) or ""
            if not u:
                m = re.search(r'<span>([^<]+)</span>', block[inp.end():inp.end() + 80])
                u = m.group(1) if m else ""
            if a.get("type") == "range":
                line += f" (Regler {a.get('min')} bis {a.get('max')} {u}, Startwert {a.get('value')} {u})"
            elif a.get("type") == "number":
                line += f" (Zahl in {u}" + (f", {a.get('min')} bis {a.get('max')}" if a.get("min") else "") + ")"
            elif fid in ("plz", "f-plz"):
                line += " (Postleitzahl; der kostenlose Rechner nutzt die erste Ziffer als Region, Speicherklar Pro die ersten zwei)"
        segs = re.findall(r'<button type="button" data-v="[^"]*" aria-pressed="(true|false)">(.*?)</button>', block)
        if segs:
            line += ". Auswahl: " + ", ".join(strip_tags(b) + (" (Start)" if p == "true" else "") for p, b in segs)
        hints = [strip_tags(h) for h in re.findall(r'<span class="hint"[^>]*>(.*?)</span>', block, re.S) if strip_tags(h)]
        if hints: line += ". Hinweis auf der Seite: " + " ".join(hints)
        out.append(line)
    return "\n".join(out)


# Was die Ergebniswerte bedeuten (die Werte selbst rechnet ui.js im Browser, im HTML stehen nur Platzhalter)
ERGEBNIS = """# Was der Rechner anzeigt (rechts bzw. unter den Eingaben, Abschnitt #ergebnis)
- Urteil oben: ein Satz, ob sich der gewählte Speicher bei deinen Werten rechnet.
- Zusätzlich selbst genutzt durch den Speicher (Zählerrolle): Solarstrom in kWh pro Jahr, den du dank Speicher selbst nutzt statt einzuspeisen.
- Ersparnis pro Jahr: was der Speicher pro Jahr gegenüber derselben Anlage ohne Speicher spart (weniger Netzstrom gekauft minus entgangene Einspeisevergütung).
- Amortisation: nach wie vielen Jahren die Ersparnis den Speicherpreis wieder eingespielt hat. Darunter steht der Speicherpreis (Größe mal Preis je kWh).
- Bilanz nach Lebensdauer: Ersparnis über die gewählte Lebensdauer minus Speicherpreis. Plus heißt: Am Ende bleibt Geld übrig.
- Autarkie: Anteil deines Verbrauchs, der vom eigenen Dach kommt, ohne und mit Speicher. Eigenverbrauch: Anteil des Solarstroms, der im Haus bleibt.
- Ein typischer Tag mit deinem Speicher: Tagesverlauf im Juni und im Dezember (Erzeugung, Verbrauch, Laden, Entladen).
- Welche Größe rechnet sich am besten?: Bilanz für jede Größe von 1 bis 15 kWh. Bernstein ist die beste Größe (größte Bilanz), umrandet deine Wahl. Am Handy zeigt eine Leiste unten Größe, Amortisation und Bilanz.
- Knopf „Angebot prüfen“: führt zu Speicherklar Pro, die Werte aus dem Rechner werden übernommen.
Nicht im Modell: Notstrom, Verschattung, Alterung des Speichers, dynamische Stromtarife, die 60-%-Grenze und Stunden mit negativen Preisen aus dem Solarspitzengesetz (im Modus „EEG heute“)."""

DACH_PRO = "- Dachfläche(n): je Fläche Leistung in kWp, Ausrichtung, Neigung und optional „Höchstens“ (so viel kWp passen maximal aufs Dach). Mit „+ Dachfläche hinzufügen“ trägst du weitere Flächen ein, z. B. Ost und West getrennt.\n- Verbrauch nach Monaten (optional): statt Jahreswert zwölf Monatswerte, z. B. aus dem Zählerportal."


def politik():
    raw = (S / "klara-politik.md").read_text()
    raw = re.sub(r"<!--.*?-->", "", raw, flags=re.S)
    out = []
    for part in raw.split("\n## ")[1:]:
        lines = part.strip().split("\n")
        e = {"thema": lines[0].strip()}
        rest = []
        for l in lines[1:]:
            m = re.match(r"- (Stand|Status|Quelle|Prüfen bis): (.*)", l)
            if m: e[{"Stand": "stand", "Status": "status", "Quelle": "quelle", "Prüfen bis": "pruefenBis"}[m.group(1)]] = m.group(2).strip()
            elif l.strip(): rest.append(l.strip())
        e["text"] = " ".join(rest)
        for k in ("stand", "status", "quelle", "pruefenBis"):
            assert k in e, f"klara-politik.md: {e['thema']} ohne {k}"
        out.append(e)
    heute = datetime.date.today().isoformat()
    for e in out:
        if e["pruefenBis"] < heute:
            print(f"WARNUNG: Klara-Politik „{e['thema']}“ abgelaufen (Prüfen bis {e['pruefenBis']}), Klara nutzt den Eintrag nicht mehr")
    return out


def build():
    sys.path.insert(0, str(S))
    import articles as A

    body = (S / "body.html").read_text()
    pro = (S / "pro-body.html").read_text()
    cfg = (S / "pro-config.js").read_text()
    cv = lambda k: re.search(k + r'\s*:\s*"?([^",\n]*)"?', cfg).group(1).strip()
    de = lambda d: ".".join(reversed(d.split("-")))
    def abschnitt(h, i):
        a = h.rfind("<", 0, h.find(f'id="{i}"'))
        return txt(h[a:].split("</section>")[0])
    annahmen = abschnitt(body, "annahmen")
    lead = abschnitt(body, "unabhaengig") if 'id="unabhaengig"' in body else ""

    teile = []
    teile.append(f"""# Speicherklar in Kürze
Speicherklar (speicherklar.de) ist ein kostenloser Stromspeicher-Rechner für Leute, die eine PV-Anlage erst planen. Betreiber ist Manuel Maurer (Krefeld), privat und unabhängig: keine Provision, keine Werbung, keine Partner-Installateure, Ergebnis ohne Anmeldung, Rechenweg offen auf GitHub. Speicherklar finanziert sich nur über Speicherklar Pro, deshalb darf auch ein kleinerer Speicher rauskommen. Leitsatz: „Verkäufer rechnen mit Juli. Ich rechne mit November.“ Kontakt: kontakt@speicherklar.de, Instagram @speicherklar.

{lead}

# Speicherklar Pro
Speicherklar Pro ist der Angebots-Check unter {SITE}pro/: Du trägst das Angebot deines Installateurs ein (Anlage, Speichergröße, Preise, Dach, Verbrauch). Vor dem Kauf gibt es kostenlos eine erste Einschätzung, als Ampel: grün, gelb oder rot, in vier Punkten (Speichergröße, Größe der PV-Anlage, Speicherpreis je kWh, Preis der PV-Anlage je kWp). Mit Speicherklar Pro bekommst du den vollständigen PDF-Bericht: ob der Speicher zu groß ist, die Ersparnis bei passender Größe, welche PV-Anlage und welcher Speicher am besten zusammenpassen (Empfehlung der PV-Anlagengröße) und Fragen an den Installateur. Speicherklar Pro rechnet mit genaueren Sonnendaten je zweistelligem PLZ-Gebiet. Musterbericht: {SITE}pro/musterbericht.pdf
Preis: {cv('price')} € einmalig bis {de(cv('introUntil'))}, danach {cv('regularPrice')} €. Kein Abo, keine automatische Verlängerung. Kaufen kann jeder ab {de(cv('publicFrom'))}. Der Zugang gilt {cv('accessDays')} Tage ab der ersten Freischaltung, in der Zeit beliebig viele Angebote, auf bis zu drei Geräten. PDF-Berichte bleiben dauerhaft beim Käufer. Verlängerung auf Mail-Anfrage kostenlos. Bezahlung über Stripe, der Lizenzschlüssel kommt auf der Seite und per Mail.
Preise nie als Streichpreis nennen, sondern „{cv('price')} € bis {de(cv('introUntil'))}, danach {cv('regularPrice')} €“.""")

    teile.append("# Eingabefelder im kostenlosen Rechner (Startseite, Abschnitt #rechner)\n" + felder(body.split('id="ergebnis"')[0], UNITS))
    teile.append(ERGEBNIS)
    teile.append("# Annahmen des Rechners (Startseite, Abschnitt #annahmen)\n" + annahmen)
    teile.append(f"# Eingabefelder in Speicherklar Pro ({SITE}pro/)\n" + felder(pro.split('id="teaser"')[0], {}).replace(
        "Speicherklar Pro die ersten zwei). Hinweis auf der Seite: „Höchstens“", "Speicherklar Pro die ersten zwei)\n" + DACH_PRO + " Hinweis auf der Seite: „Höchstens“"))
    teile.append(f"# Methodik ({SITE}methodik.html)\n" + txt((S / "methodik.html").read_text()))

    sg = (S / "so-gehts.html").read_text()
    sg = re.sub(r"\{\{[A-Z_]+\}\}", "", sg)
    import ast
    src = (ROOT / "build_articles.py").read_text()
    m = re.search(r"SG_FAQ = (\[.*?\n\])", src, re.S)
    faq = ast.literal_eval(m.group(1)) if m else []
    teile.append(f"# So funktioniert Speicherklar ({SITE}so-gehts/)\n" + txt(sg) + "\n" + "\n".join(f"Frage: {q}\nAntwort: {a}" for q, a in faq))

    pfade = ["", "#rechner", "#annahmen", "pro/", "pro/musterbericht.pdf", "so-gehts/", "ratgeber/", "methodik.html", "ueber-mich.html", "kontakt.html", "datenschutz.html"]
    pfade += [f"methodik.html#{i}" for i in re.findall(r'<h2[^>]*id="([a-z0-9-]+)"', (S / "methodik.html").read_text())]
    art = [f"# Ratgeber-Artikel\nAlle Zahlen in den Artikeln sind mit dem Simulationskern src/sim.js gerechnet. Annahmen, wenn nicht anders genannt: {strip_tags(A.BEISPIEL)}"]
    for a in A.ARTICLES:
        url = f"ratgeber/{a['slug']}.html"; pfade.append(url)
        stand = a.get("updated") or a.get("date")
        faqs = "\n".join(f"Frage: {q}\nAntwort: {x}" for q, x in a.get("faq", []))
        art.append(f"## {a['title']}\nAdresse: {SITE}{url} (Stand {de(stand)})\nKurz: {strip_tags(a.get('lead', a.get('desc', '')))}\n{txt(a['body'])}\n{faqs}".strip())
    teile.append("\n\n".join(art))

    wissen = "\n\n".join(teile)
    wissen = wissen.replace("—", "-")
    pol = politik()
    tok = (len(wissen) + len(json.dumps(pol, ensure_ascii=False))) / 3.2
    assert tok < MAX_TOKENS, f"Klara-Wissen zu groß: rund {int(tok)} Tokens (Grenze {MAX_TOKENS})"
    pfade = sorted(set(pfade))

    js = ("// Erzeugt von scripts/klara_wissen.py (läuft in build.py). Nicht von Hand ändern.\n"
          f"// Rund {int(tok / 1000)}k Tokens.\n"
          f"export const WISSEN = {json.dumps(wissen, ensure_ascii=False)};\n"
          f"export const POLITIK = {json.dumps(pol, ensure_ascii=False, indent=1)};\n"
          f"export const PFADE = {json.dumps(pfade, ensure_ascii=False)};\n")
    OUT.parent.mkdir(exist_ok=True)
    old = OUT.read_text() if OUT.exists() else ""
    if js != old: OUT.write_text(js)
    print(f"Klara-Wissen: rund {int(tok / 1000)}k Tokens, {len(pol)} Politik-Einträge, {len(pfade)} Seiten" + ("" if js != old else " (unverändert)"))


if __name__ == "__main__":
    build()
