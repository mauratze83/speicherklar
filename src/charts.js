/* Erzeugt die Artikelgrafiken aus dem Simulationsmodell.
   Aufruf (von build_articles.py): node src/charts.js < specs.json > charts.json
   specs.json: {"base": {...Standardparameter...}, "charts": {"<slug>": {kind, title, caption, ...}}}
   kind "sweep": series:[{label, p:{Abweichungen}}]  -> Gewinn nach Lebensdauer je Speichergröße 1–12 kWh
   kind "day":   p:{...}, cap:<kWh>, months:[5,11]   -> Durchschnittstag je Monat (0 = Januar) */
var S = require("./sim.js"), D = require("./draw.js");
var MONTHS = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"];

function merge(base, over) { var o = JSON.parse(JSON.stringify(base)); Object.keys(over || {}).forEach(function (k) { o[k] = over[k]; }); return o; }
function nets(p) { return S.evaluate(p).sweep.slice(0, 12).map(function (s) { return Math.round(s.net); }); }

var input = JSON.parse(require("fs").readFileSync(0, "utf8")), out = {};
Object.keys(input.charts).forEach(function (slug) {
  var c = input.charts[slug], html, spark, facts = {};
  if (c.kind === "sweep") {
    var series = c.series.map(function (se) { var v = nets(merge(input.base, se.p)); return { label: se.label, values: v }; });
    html = D.sweepChart(series);
    spark = D.spark(series[0].values);
    facts = series.map(function (se) { var m = Math.max.apply(null, se.values); return { label: se.label, best: m > 0 ? se.values.indexOf(m) + 1 : null, net: m }; });
  } else if (c.kind === "day") {
    var p = merge(input.base, c.p), days = S.dayProfile(p, c.cap);
    html = D.dayChart(c.months.map(function (m) { return days[m]; }), c.months.map(function (m) { return MONTHS[m]; }));
    spark = D.spark(nets(p));
  } else throw new Error("Unbekannte Grafik: " + c.kind);
  out[slug] = { html: html, spark: spark, facts: facts };
});
process.stdout.write(JSON.stringify(out));
