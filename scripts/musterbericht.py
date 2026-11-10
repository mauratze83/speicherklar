"""Erzeugt pro/musterbericht.pdf: den echten Pro-Bericht für ein erfundenes Musterangebot.

Aufruf (nach build.py, braucht Playwright): python3 scripts/musterbericht.py
Neu erzeugen, wenn sich pro.js, pro-ui.js, sim.js oder die Standardwerte ändern.
"""
import json, pathlib, subprocess, sys, time, socket

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "pro" / "musterbericht.pdf"

# Musterangebot (erfunden): gleiche Werte wie der Artikel "PV-Angebot prüfen" und test/pro.test.js
MUSTER = {
    "model": "Musterangebot (Beispiel)", "cap": 10, "capKind": "nutzbar", "pow": 5,
    "total": 19000, "store": 6500, "plz": "47051",
    "roofs": [{"kwp": 9, "aspect": 0, "tilt": 35, "max": 15}],
    "cons": 4500, "ev": 0, "evTime": "eve", "hp": 0,
    "price": 33, "eeg": "now", "feed": 7.7, "life": 15,
}


def free_port():
    s = socket.socket(); s.bind(("127.0.0.1", 0)); p = s.getsockname()[1]; s.close(); return p


def main():
    from playwright.sync_api import sync_playwright
    port = free_port()
    srv = subprocess.Popen([sys.executable, "-m", "http.server", str(port), "--bind", "127.0.0.1"], cwd=ROOT,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        time.sleep(0.8)
        with sync_playwright() as p:
            b = p.chromium.launch()
            page = b.new_page(locale="de-DE")
            init = (f"localStorage.setItem('sk-pro-eingabe', {json.dumps(json.dumps(MUSTER))});"
                    "localStorage.setItem('sk-pro-lizenz', JSON.stringify({key:'MUSTER',email:'',at:Date.now()}));")
            page.add_init_script(init)
            # Lizenzprüfung nur in diesem Testbrowser beantworten; die Seite selbst kennt keinen Testschlüssel
            page.route("**/validate", lambda r: r.fulfill(status=200, content_type="application/json", body='{"ok":true,"email":""}'))
            page.goto(f"http://127.0.0.1:{port}/pro/?vorab=1")
            page.wait_for_selector("#report-wrap:not([hidden]) #report section", timeout=60000)
            page.wait_for_timeout(1500)
            page.emulate_media(media="print")
            page.pdf(path=str(OUT), format="A4", print_background=True, prefer_css_page_size=True)
            b.close()
    finally:
        srv.terminate()
    print("Musterbericht:", OUT.relative_to(ROOT), OUT.stat().st_size // 1024, "KB")


if __name__ == "__main__":
    main()
