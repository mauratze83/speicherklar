/* Marktspannen für den Preis-Check in Speicherklar Pro.
   Ein- bis zweimal im Jahr prüfen und STAND anpassen. Werte inkl. Montage, brutto (Privatkunden, 0 % MwSt. auf PV seit 2023). */
var MARKT = {
  STAND: "Juli 2026",
  QUELLEN: [
    "42watt Magazin, Photovoltaik Kosten 2026 (Juli 2026), u. a. nach Fraunhofer ISE",
    "ADAC, Stromspeicher für PV-Anlage (August 2026)",
    "Verbraucherzentrale: 300–700 €/kWh für Speicher inkl. Einbau"
  ],
  // PV ohne Speicher, €/kWp nach Anlagengröße: [bis kWp, untere Grenze, obere Grenze]
  PV: [[5, 1335, 1800], [10, 1100, 1400], [15, 970, 1200], [99, 900, 1100]],
  // Speicher inkl. Einbau, € je kWh nutzbar. Kleine Speicher kosten je kWh mehr.
  SPEICHER: { lo: 350, hi: 700, kleinBis: 6, kleinAufschlag: 100, mitte: 525 }
};
if (typeof module !== "undefined") module.exports = MARKT;
