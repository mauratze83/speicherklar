"""Schreibt die freigegebenen Bewertungen aus der Antwort des Workers nach src/bewertungen.json.
Aufruf: python3 scripts/bewertungen.py antwort.json   (läuft im Workflow "Bewertungen", nicht von Hand nötig)
Prüft jeden Eintrag noch einmal, damit nichts Unerwartetes auf die Seite kommt."""
import json, pathlib, re, sys

OUT = pathlib.Path(__file__).resolve().parent.parent / "src" / "bewertungen.json"
data = json.loads(pathlib.Path(sys.argv[1]).read_text())
rows = []
for r in data.get("reviews", []):
    rid, stars, text, name, date = r.get("rid"), r.get("stars"), r.get("text"), r.get("name") or "", r.get("date")
    assert re.fullmatch(r"[0-9a-f]{12}", str(rid)), f"rid: {rid}"
    assert isinstance(stars, int) and 1 <= stars <= 5, f"Sterne: {stars}"
    assert isinstance(text, str) and 20 <= len(text) <= 1000, "Text"
    assert isinstance(name, str) and len(name) <= 40, "Name"
    assert re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(date)), f"Datum: {date}"
    rows.append({"rid": rid, "stars": stars, "text": text, "name": name, "date": date})
rows.sort(key=lambda x: (x["date"], x["rid"]), reverse=True)
OUT.write_text(json.dumps({"bewertungen": rows}, ensure_ascii=False, indent=1) + "\n")
print(len(rows), "freigegebene Bewertungen")
