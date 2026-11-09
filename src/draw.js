/* Speicherklar Diagramme – reine Funktionen, die SVG-Text liefern. Laufen im Browser (Rechner) und in Node (Artikel-Build).
   Farben kommen aus den CSS-Variablen der Seite, damit helles und dunkles Design stimmen. */

var DRAW = (function () {
  var NF0 = function (v) { return Math.round(v).toLocaleString("de-DE"); };
  var NF1 = function (v) { return (Math.round(v * 10) / 10).toLocaleString("de-DE", { minimumFractionDigits: 1, maximumFractionDigits: 1 }); };

  // Reihenfolge der gestapelten Flächen: alles unterhalb der Verbrauchslinie versorgt das Haus, darüber der Überschuss
  var LAYERS = [
    { k: "direct", label: "Direkt genutzt", cls: "l-direct" },
    { k: "discharge", label: "Aus dem Speicher", cls: "l-dis" },
    { k: "imp", label: "Aus dem Netz", cls: "l-imp" },
    { k: "charge", label: "In den Speicher", cls: "l-charge" },
    { k: "exp", label: "Eingespeist", cls: "l-exp" }
  ];

  function stack(m) {
    var tops = [], acc = new Array(24).fill(0);
    LAYERS.forEach(function (L) {
      var bottom = acc.slice();
      for (var h = 0; h < 24; h++) acc[h] += m[L.k][h];
      tops.push({ bottom: bottom, top: acc.slice() });
    });
    return { layers: tops, load: Array.prototype.slice.call(m.load), max: Math.max.apply(null, acc.concat(Array.prototype.slice.call(m.load))) };
  }

  function niceStep(span, n) {
    var s = Math.pow(10, Math.floor(Math.log10(span / n)));
    [1, 2, 2.5, 5, 10].some(function (k) { if (span / (s * k) <= n) { s *= k; return true; } return false; });
    return s;
  }

  // Geometrie für den Tageschart; st = Ergebnis von stack(), ymax fest vorgeben, damit Juni und Dezember vergleichbar sind
  function dayGeometry(st, box, ymax) {
    var x = function (h) { return box.l + (box.w * h) / 24; };
    var y = function (v) { return box.t + box.h * (1 - v / ymax); };
    var pts = function (arr) { var s = ""; for (var h = 0; h < 24; h++) s += (h ? "L" : "") + x(h + 0.5).toFixed(1) + "," + y(arr[h]).toFixed(1); return s; };
    var area = function (b, t) {
      var s = "M" + x(0).toFixed(1) + "," + y(t[0]).toFixed(1) + "L" + pts(t);
      s += "L" + x(24).toFixed(1) + "," + y(t[23]).toFixed(1) + "L" + x(24).toFixed(1) + "," + y(b[23]).toFixed(1);
      for (var h = 23; h >= 0; h--) s += "L" + x(h + 0.5).toFixed(1) + "," + y(b[h]).toFixed(1);
      return s + "L" + x(0).toFixed(1) + "," + y(b[0]).toFixed(1) + "Z";
    };
    return {
      areas: st.layers.map(function (L) { return area(L.bottom, L.top); }),
      load: "M" + x(0).toFixed(1) + "," + y(st.load[0]).toFixed(1) + "L" + pts(st.load) + "L" + x(24).toFixed(1) + "," + y(st.load[23]).toFixed(1),
      x: x, y: y
    };
  }

  function dayAxes(box, ymax, x, y) {
    var s = "", step = niceStep(ymax, 4);
    for (var v = 0; v <= ymax + 1e-9; v += step) {
      s += '<line class="grid' + (v === 0 ? " zero" : "") + '" x1="' + box.l + '" x2="' + (box.l + box.w) + '" y1="' + y(v).toFixed(1) + '" y2="' + y(v).toFixed(1) + '"/>';
      s += '<text class="ax" x="' + (box.l - 8) + '" y="' + (y(v) + 4).toFixed(1) + '" text-anchor="end">' + NF1(v).replace(",0", "") + "</text>";
    }
    [0, 6, 12, 18, 24].forEach(function (h) {
      s += '<text class="ax" x="' + x(h).toFixed(1) + '" y="' + (box.t + box.h + 18) + '" text-anchor="' + (h === 0 ? "start" : h === 24 ? "end" : "middle") + '">' + h + (h === 24 ? " Uhr" : "") + "</text>";
    });
    s += '<text class="ax" x="' + (box.l - 8) + '" y="' + (box.t - 8) + '" text-anchor="end">kW</text>';
    return s;
  }

  function legend() {
    return '<div class="clegend">' + LAYERS.map(function (L) { return '<span><i class="sw ' + L.cls + '"></i>' + L.label + "</span>"; }).join("") +
      '<span><i class="sw l-load"></i>Verbrauch</span></div>';
  }

  function daySvgInner(m, box, ymax) {
    var st = stack(m), g = dayGeometry(st, box, ymax);
    return dayAxes(box, ymax, g.x, g.y) +
      g.areas.map(function (d, i) { return '<path class="area ' + LAYERS[i].cls + '" d="' + d + '"/>'; }).join("") +
      '<path class="lline" d="' + g.load + '"/>';
  }

  // Statischer Tageschart (Artikel): mehrere Monate nebeneinander, gleiche Skala
  function dayChart(months, titles) {
    var W = 340, H = 230, box = { l: 40, t: 24, w: 288, h: 168 };
    var ymax = 0; months.forEach(function (m) { ymax = Math.max(ymax, stack(m).max); });
    ymax = Math.ceil(ymax / niceStep(ymax, 4)) * niceStep(ymax, 4);
    var panels = months.map(function (m, i) {
      return '<div class="cpanel"><div class="ctitle">' + titles[i] + '</div><svg viewBox="0 0 ' + W + " " + H + '" role="img" aria-label="Tagesverlauf ' + titles[i] + '">' + daySvgInner(m, box, ymax) + "</svg></div>";
    }).join("");
    return '<div class="cpanels">' + panels + "</div>" + legend();
  }

  // Liniendiagramm: Gewinn/Verlust nach Lebensdauer je Speichergröße für mehrere Szenarien.
  // W = Breite des Zeichenbereichs; die Artikel bekommen eine breite und eine schmale Fassung (Handy).
  function sweepSvg(series, W) {
    var H = W < 500 ? 280 : 300, box = { l: 80, t: 26, w: W - 80 - 14, h: H - 26 - 50 }, caps = series[0].values.length;
    var all = []; series.forEach(function (s) { all = all.concat(s.values); });
    var max = Math.max(0, Math.max.apply(null, all)), min = Math.min(0, Math.min.apply(null, all));
    var step = niceStep(max - min || 1, 5), top = Math.ceil(max / step) * step, bot = Math.floor(min / step) * step;
    if (top === bot) top = bot + step;
    var x = function (i) { return box.l + (box.w * i) / (caps - 1); };
    var y = function (v) { return box.t + (box.h * (top - v)) / (top - bot); };
    var s = "";
    for (var v = bot; v <= top + 1e-9; v += step) {
      s += '<line class="grid' + (Math.abs(v) < 1e-9 ? " zero" : "") + '" x1="' + box.l + '" x2="' + (box.l + box.w) + '" y1="' + y(v).toFixed(1) + '" y2="' + y(v).toFixed(1) + '"/>';
      s += '<text class="ax" x="' + (box.l - 8) + '" y="' + (y(v) + 4).toFixed(1) + '" text-anchor="end">' + (v < 0 ? "−" : v > 0 ? "+" : "") + NF0(Math.abs(v)) + " €</text>";
    }
    for (var i = 0; i < caps; i++) if (W >= 500 || i % 2 === 0 || i === caps - 1) s += '<text class="ax" x="' + x(i).toFixed(1) + '" y="' + (box.t + box.h + 20) + '" text-anchor="middle">' + (i + 1) + "</text>";
    s += '<text class="ax" x="' + (box.l + box.w) + '" y="' + (H - 6) + '" text-anchor="end">Speichergröße in kWh</text>';
    var bests = series.map(function (se) {
      var bi = se.values.indexOf(Math.max.apply(null, se.values));
      return se.values[bi] > 0 ? { i: bi, x: x(bi), y: y(se.values[bi]) } : null;
    });
    var placed = [];
    series.forEach(function (se, k) {
      var d = se.values.map(function (v, i) { return (i ? "L" : "M") + x(i).toFixed(1) + "," + y(v).toFixed(1); }).join("");
      s += '<path class="sline s' + k + '" pathLength="1" d="' + d + '"/>';
    });
    // Punkte und Beschriftungen nach allen Linien, damit nichts verdeckt wird; Beschriftung unter den Punkt, wenn oben besetzt
    bests.forEach(function (b, k) {
      if (!b) return;
      var hit = function (ly) {
        return placed.some(function (p) { return Math.abs(p.x - b.x) < 44 && Math.abs(p.y - ly) < 15; }) ||
          bests.some(function (o, j) { return o && j !== k && Math.abs(o.x - b.x) < 30 && ly - 12 < o.y + 6 && ly + 2 > o.y - 6; });
      };
      var ly = b.y - 11;
      if (hit(ly)) ly = b.y + 22;
      if (hit(ly)) { ly = b.y + 4; }
      var lx = b.x, anchor = "middle";
      if (ly === b.y + 4) { lx = b.x + 10; anchor = "start"; }
      placed.push({ x: lx, y: ly });
      s += '<circle class="sdot s' + k + '" cx="' + b.x.toFixed(1) + '" cy="' + b.y.toFixed(1) + '" r="5"/>';
      s += '<text class="slabel s' + k + '" x="' + lx.toFixed(1) + '" y="' + ly.toFixed(1) + '" text-anchor="' + anchor + '">' + (b.i + 1) + " kWh</text>";
    });
    return '<svg viewBox="0 0 ' + W + " " + H + '" role="img" aria-label="Gewinn nach Lebensdauer je Speichergröße">' + s + "</svg>";
  }
  function sweepChart(series) {
    var leg = '<div class="clegend">' + series.map(function (se, k) { return '<span><i class="sw sl s' + k + '"></i>' + se.label + "</span>"; }).join("") + "</div>";
    return '<div class="c-wide">' + sweepSvg(series, 640) + '</div><div class="c-narrow">' + sweepSvg(series, 380) + "</div>" + leg;
  }

  // Mini-Grafik für Ratgeber-Karten (nur Form, keine Achsen)
  function spark(values) {
    var W = 120, H = 36, n = values.length, max = Math.max.apply(null, values.map(Math.abs)) || 1, bw = W / n;
    var mid = values.some(function (v) { return v < 0; }) ? H * 0.62 : H;
    var s = "";
    values.forEach(function (v, i) {
      var h = (Math.abs(v) / max) * (v >= 0 ? mid : H - mid) * 0.95;
      s += '<rect class="' + (v >= 0 ? "sp-pos" : "sp-neg") + '" x="' + (i * bw + 1).toFixed(1) + '" y="' + (v >= 0 ? mid - h : mid).toFixed(1) + '" width="' + (bw - 2).toFixed(1) + '" height="' + Math.max(1, h).toFixed(1) + '" rx="1.5"/>';
    });
    return '<svg class="spark" viewBox="0 0 ' + W + " " + H + '" aria-hidden="true">' + s + "</svg>";
  }

  return { LAYERS: LAYERS, stack: stack, dayGeometry: dayGeometry, dayAxes: dayAxes, legend: legend, niceStep: niceStep, dayChart: dayChart, sweepChart: sweepChart, spark: spark, NF1: NF1 };
})();

if (typeof module !== "undefined") module.exports = DRAW;
