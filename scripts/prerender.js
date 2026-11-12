// Rechnet das Standard-Beispiel der Startseite mit src/sim.js vor, damit das Ergebnis auch ohne
// JavaScript im HTML steht (Suchmaschinen- und KI-Crawler führen meist kein JavaScript aus).
// Aufruf aus build.py: node scripts/prerender.js '<JSON der Startwerte>'  → JSON mit fertigen Texten.
// Die Texte entsprechen render() in src/ui.js; ui.js überschreibt sie beim Laden.
const sim = require("../src/sim.js");
const d = JSON.parse(process.argv[2]);
const nf0 = new Intl.NumberFormat("de-DE", { maximumFractionDigits: 0 });
const nf1 = new Intl.NumberFormat("de-DE", { minimumFractionDigits: 1, maximumFractionDigits: 1 });
const nf2 = new Intl.NumberFormat("de-DE", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
const euro = v => (v < 0 ? "−" : "") + nf0.format(Math.abs(v)) + " €";
const p = { region: d.region, roofs: [{ kwp: d.pv, tilt: d.tilt, aspect: 0 }], cons: d.cons, ev: d.ev, evTime: "eve",
  bat: d.bat, bprice: d.bprice, life: d.life, price: d.price, feed: d.feed, feedLimit: 0 };
const res = sim.evaluate(p), c = res.chosen, best = res.best;
let v = c.net >= 0
  ? `Mit ${p.bat} kWh <span class="ok">rechnet sich der Speicher nach etwa ${nf1.format(c.payback)} Jahren.</span>`
  : `Mit ${p.bat} kWh <span class="no">holt der Speicher seine Kosten in ${p.life} Jahren nicht rein.</span>`;
if (best.cap !== p.bat) v += best.net > 0 ? ` Am meisten bleibt bei ${best.cap} kWh übrig.` : " Bei diesen Preisen rechnet sich keine Größe.";
else if (best.net > 0) v += " Das ist auch die wirtschaftlichste Größe.";
const sweep = best.net > 0
  ? `Am meisten bleibt bei <b>${best.cap}&nbsp;kWh</b>: ${(best.net >= 0 ? "+" : "") + euro(best.net).replace(" €", "&nbsp;€")} nach ${p.life} Jahren, bezahlt nach ${nf1.format(best.payback)} Jahren.`
  : "Bei diesen Preisen rechnet sich keine Speichergröße.";
console.log(JSON.stringify({
  verdict: v,
  save: euro(c.save),
  pay: isFinite(c.payback) ? nf1.format(c.payback) + " J." : "nie",
  cost: "bei " + euro(c.cost) + " Anschaffung",
  net: (c.net >= 0 ? "+" : "") + euro(c.net), netPos: c.net >= 0,
  netd: "nach " + p.life + " Jahren",
  sweep,
  // Ein Satz für die Beschreibung des Beispiels (Startseite, llms.txt), mit allen Annahmen
  example: `Beispiel: ${sim.REGIONS[d.region].n.split(",")[0]}, ${Number.isInteger(d.pv) ? nf0.format(d.pv) : nf1.format(d.pv)} kWp Süd, ${d.tilt}° Neigung, ${nf0.format(d.cons)} kWh Verbrauch im Jahr, `
    + `Speicher ${nf0.format(d.bprice)} €/kWh, Strompreis ${nf2.format(d.price)} ct, Einspeisung ${nf2.format(d.feed)} ct, ${d.life} Jahre.`,
  best: { cap: best.cap, net: Math.round(best.net), payback: Math.round(best.payback * 10) / 10, save: Math.round(best.save) },
}));
