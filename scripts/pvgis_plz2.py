"""Sonnendaten je zweistelligem PLZ-Gebiet für Speicherklar Pro.

Holt die Postleitzahlen von GeoNames (CC BY 4.0), bildet je PLZ-Gebiet (erste zwei Ziffern) den Mittelpunkt
und fragt dafür bei PVGIS die Monatsmittel 2014–2023 (SARAH3) ab: Globalstrahlung horizontal H(h)_m und Diffusanteil Kd.
Gegenprobe: derselbe Abruf für den Mittelpunkt der bisherigen Region 4 muss die Werte aus src/sim.js ergeben.

Aufruf: python3 scripts/pvgis_plz2.py [--neu = alles neu bei PVGIS abfragen]   (läuft per GitHub Actions, siehe .github/workflows/sonnendaten.yml)
Ergebnis: src/plz2.json
"""
import io, json, time, urllib.request, zipfile, datetime, collections, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
# Großkunden-Postleitzahlen (Behörden, Firmen) taugen nicht als Gebietsname
NO_PLACE = re.compile(r"GmbH|\bAG\b|\bSE\b|\bKG\b|[Aa]mt\b|Bank|Post|Versand|Logistik|Service|Agentur|Niederlassung|Verwaltung|Versicherung|Inkasso|Bundes|Elektronik|Electronic")
GEONAMES = "https://download.geonames.org/export/zip/DE.zip"
PVGIS = ("https://re.jrc.ec.europa.eu/api/v5_3/MRcalc?lat={lat:.3f}&lon={lon:.3f}&raddatabase=PVGIS-SARAH3"
         "&startyear=2014&endyear=2023&horirrad=1&d2g=1&outputformat=json")


def get(url, tries=5):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "speicherklar.de Sonnendaten-Skript"})
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read()
        except Exception as e:  # PVGIS antwortet bei Last gelegentlich mit 429/5xx
            print(f"  Versuch {i + 1} fehlgeschlagen: {e}", file=sys.stderr)
            time.sleep(2 * (i + 1))
    raise RuntimeError(f"Abruf fehlgeschlagen: {url}")


def areas_from_geonames(raw):
    """DE.txt: Land, PLZ, Ort, Bundesland, Kürzel, Kreis…, Breite (Spalte 10), Länge (Spalte 11)."""
    text = zipfile.ZipFile(io.BytesIO(raw)).read("DE.txt").decode("utf-8")
    codes = {}
    for line in text.splitlines():
        f = line.split("\t")
        if len(f) < 11 or not re.fullmatch(r"\d{5}", f[1]) or not f[9]:
            continue
        codes.setdefault(f[1], []).append((f[2], float(f[9]), float(f[10])))
    groups = collections.defaultdict(list)
    for code, rows in codes.items():
        lat = sum(r[1] for r in rows) / len(rows)
        lon = sum(r[2] for r in rows) / len(rows)
        groups[code[:2]].append((rows[0][0], lat, lon))
    out = {}
    for k, rows in sorted(groups.items()):
        # Name: die zwei Orte mit den meisten Postleitzahlen im Gebiet. Ein zweiter Name zählt nur mit mindestens
        # 3 Postleitzahlen, sonst wäre es oft eine Großkunden-PLZ (Behörde, Firma) statt eines Orts.
        common = [(n, c) for n, c in collections.Counter(r[0] for r in rows).most_common() if not NO_PLACE.search(n)][:2]
        names = [common[0][0]] + [n for n, c in common[1:] if c >= 3]
        out[k] = {"n": ", ".join(names), "lat": round(sum(r[1] for r in rows) / len(rows), 3),
                  "lon": round(sum(r[2] for r in rows) / len(rows), 3), "codes": len(rows)}
    return out


def monthly(lat, lon):
    data = json.loads(get(PVGIS.format(lat=lat, lon=lon)))
    H, K = [[] for _ in range(12)], [[] for _ in range(12)]
    for row in data["outputs"]["monthly"]:
        H[row["month"] - 1].append(row["H(h)_m"])
        K[row["month"] - 1].append(row["Kd"])
    return [round(sum(x) / len(x), 1) for x in H], [round(sum(x) / len(x), 2) for x in K]


def main():
    areas = areas_from_geonames(get(GEONAMES))
    print(f"{len(areas)} PLZ-Gebiete aus GeoNames")

    # Gegenprobe gegen Region 4 aus sim.js
    sim = (ROOT / "src/sim.js").read_text()
    m = re.search(r'"4":\{n:"[^"]*",lat:([\d.]+),lon:([\d.]+),H:\[([^\]]+)\],Kd:\[([^\]]+)\]', sim)
    lat4, lon4 = float(m.group(1)), float(m.group(2))
    h_old = [float(x) for x in m.group(3).split(",")]
    h_new, k_new = monthly(lat4, lon4)
    dev = abs(sum(h_new) - sum(h_old)) / sum(h_old)
    print(f"Gegenprobe Region 4: Jahressumme alt {sum(h_old):.1f}, neu {sum(h_new):.1f}, Abweichung {dev:.2%}")
    if dev > 0.02:
        sys.exit("Gegenprobe weicht mehr als 2 % ab – Abruf passt nicht zu den bisherigen Daten, nichts geschrieben.")

    # Vorhandene Werte wiederverwenden, wenn der Mittelpunkt gleich geblieben ist
    old_file = ROOT / "src/plz2.json"
    old = json.loads(old_file.read_text())["gebiete"] if old_file.exists() else {}
    for i, (k, a) in enumerate(areas.items()):
        o = old.get(k)
        if o and o["lat"] == a["lat"] and o["lon"] == a["lon"] and "--neu" not in sys.argv:
            a["H"], a["Kd"] = o["H"], o["Kd"]
            continue
        a["H"], a["Kd"] = monthly(a["lat"], a["lon"])
        print(f"{k} {a['n']:<40} {sum(a['H']):7.1f} kWh/m²")
        time.sleep(0.3)

    out = {"stand": datetime.date.today().isoformat(),
           "quelle": "PVGIS-SARAH3 Monatsmittel 2014–2023 © Europäische Union; Postleitzahlen: GeoNames, CC BY 4.0",
           "gegenprobe": {"region": "4", "alt": round(sum(h_old), 1), "neu": round(sum(h_new), 1)},
           "gebiete": areas}
    (ROOT / "src/plz2.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))
    print("src/plz2.json geschrieben")


if __name__ == "__main__":
    main()
