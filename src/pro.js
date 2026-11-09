/* Speicherklar Pro – Angebots-Check. Reine Rechnung ohne DOM, im Browser (nach sim.js und markt.js) und in Node lauffähig.

   PRO.check(o) mit
   o = { region, roofs:[{kwp,tilt,aspect}], cons, monthly (optional, 12 Werte), ev, evTime, hp,
         price (ct/kWh), feed (ct/kWh), feedLimit (0 oder 0.5), eeg ("now"|"reform"), life (Jahre),
         cap (kWh laut Angebot), capKind ("nutzbar"|"brutto"|"unklar"), pow (kW, 0 = unbekannt),
         total (€ Gesamtpreis, 0 = unbekannt), store (€ Aufpreis Speicher, 0 = unbekannt), model (Text) } */
var PRO = (function () {
  var S = typeof require !== "undefined" ? require("./sim.js") : { profiles: profiles, runBattery: runBattery, daySeries: daySeries, REGIONS: REGIONS };
  var M = typeof require !== "undefined" ? require("./markt.js") : MARKT;

  var FIX = 0.3;        // Anteil des Speicherpreises, der nicht mit der Größe sinkt (Wechselrichter, Montage, Anschluss)
  var BRUTTO = 0.9;     // nutzbarer Anteil, wenn das Angebot brutto angibt
  var MAXCAP = 20;

  function clone(o) { return JSON.parse(JSON.stringify(o)); }

  // Nutzbare Kapazität und Ladeleistung des Angebots
  function usable(o) { return o.capKind === "brutto" ? o.cap * BRUTTO : o.cap; }
  function power(o, c, cap) {
    var offered = o.pow > 0 ? o.pow : Math.min(cap * 0.5, 5);
    if (Math.abs(c - cap) < 1e-9) return offered;
    return Math.min(offered, Math.max(2.5, c * 0.5));
  }

  // Speicherpreis: aus dem Angebot oder geschätzt
  function storePrice(o, cap) {
    if (o.store > 0) return { v: o.store, est: false };
    return { v: Math.round(cap * perKwhBand(cap).mid / 50) * 50, est: true };
  }
  function perKwhBand(cap) {
    var B = M.SPEICHER, add = cap < B.kleinBis ? B.kleinAufschlag : 0;
    return { lo: B.lo + add, hi: B.hi + add, mid: B.mitte + add };
  }
  function costFor(c, cap, sp) { return c <= 0 ? 0 : sp * (FIX + (1 - FIX) * c / cap); }

  // Energiebilanz für alle Größen 0..20 plus die angebotene Größe (unabhängig von Preisen)
  function energy(o, cap) {
    var pr = S.profiles(o), caps = [];
    for (var c = 0; c <= MAXCAP; c++) caps.push(c);
    if (caps.indexOf(cap) < 0) caps.push(cap);
    caps.sort(function (a, b) { return a - b; });
    var runs = caps.map(function (c) { return { cap: c, r: S.runBattery(pr.gen, pr.load, c, pr.fc, c > 0 ? power(o, c, cap) : 0) }; });
    return { pr: pr, runs: runs };
  }

  // Wirtschaftlichkeit für gegebene Preise auf Basis einer Energiebilanz
  function econ(en, o, cap, sp) {
    var base = en.runs[0].r, life = o.life;
    var rows = en.runs.map(function (x) {
      var save = (base.grid - x.r.grid) * o.price / 100 - (base.feed - x.r.feed) * o.feed / 100;
      var cost = costFor(x.cap, cap, sp);
      return { cap: x.cap, r: x.r, save: save, cost: cost, net: save * life - cost, payback: save > 0 && x.cap > 0 ? cost / save : Infinity, extra: base.grid - x.r.grid };
    });
    var ints = rows.filter(function (r) { return Math.abs(r.cap - Math.round(r.cap)) < 1e-9; });
    var best = ints.reduce(function (a, b) { return b.net > a.net + 1e-6 ? b : a; });
    var offer = rows.filter(function (r) { return Math.abs(r.cap - cap) < 1e-9; })[0];
    var tol = Math.max(250, 0.05 * sp);
    // Empfehlung: kleinste Größe ab 1 kWh, die fast so viel bringt wie die beste
    var rec = best.cap === 0 ? best : ints.filter(function (r) { return r.cap >= 1 && r.net >= best.net - tol; })[0];
    var verdict;
    if (best.cap === 0 && offer.net < 0) verdict = "nolohn";
    else if (offer.net >= best.net - tol) verdict = "passt";
    else verdict = offer.cap > best.cap ? "gross" : "klein";
    return { rows: rows, ints: ints, best: best, offer: offer, rec: rec, tol: tol, verdict: verdict };
  }

  function pvBand(kwp) { for (var i = 0; i < M.PV.length; i++) if (kwp <= M.PV[i][0]) return { lo: M.PV[i][1], hi: M.PV[i][2] }; }
  function rate(v, lo, hi) { return v < lo ? "guenstig" : v <= hi ? "ueblich" : v <= hi * 1.15 ? "hoch" : "teuer"; }

  function scenarios(o, cap, sp, baseEn, baseEc) {
    var list = [{ name: "Deine Eingaben", o: o, en: baseEn }];
    var alt = clone(o);
    if (o.eeg === "reform") { alt.eeg = "now"; alt.feed = 7.7; alt.feedLimit = 0; list.push({ name: "EEG heute (7,7 ct Vergütung)", o: alt }); }
    else { alt.eeg = "reform"; alt.feed = 0; alt.feedLimit = 0.5; list.push({ name: "EEG-Reform 2027 (keine Vergütung, 50-%-Grenze)", o: alt }); }
    var lo = clone(o); lo.price = o.price - 5; list.push({ name: "Strom 5 ct billiger", o: lo, en: baseEn });
    var hi = clone(o); hi.price = o.price + 5; list.push({ name: "Strom 5 ct teurer", o: hi, en: baseEn });
    var l10 = clone(o); l10.life = 10; list.push({ name: "Speicher hält nur 10 Jahre", o: l10, en: baseEn });
    var l20 = clone(o); l20.life = 20; list.push({ name: "Speicher hält 20 Jahre", o: l20, en: baseEn });
    if (!(o.ev > 0)) { var e = clone(o); e.ev = 2500; e.evTime = "eve"; list.push({ name: "Später E-Auto (2.500 kWh, lädt abends)", o: e }); }
    if (!(o.hp > 0)) { var w = clone(o); w.hp = 3500; list.push({ name: "Später Wärmepumpe (3.500 kWh)", o: w }); }
    return list.map(function (s) {
      var en = s.en || energy(s.o, cap), ec = s.en === baseEn && s.o === o ? baseEc : econ(en, s.o, cap, sp);
      return { name: s.name, best: ec.best.cap, offerNet: ec.offer.net, recNet: ec.rec.net, verdict: ec.verdict, rec: ec.rec.cap };
    });
  }

  function questions(o, r) {
    var q = [], nf = function (v) { return Math.round(v).toLocaleString("de-DE"); };
    if (r.storeEst) q.push(["Was kostet dieselbe Anlage ohne Speicher?", "Erst damit lässt sich der Speicher allein bewerten. Viele Angebote nennen nur den Gesamtpreis."]);
    if (o.capKind !== "nutzbar") q.push(["Wie viel Kapazität ist nutzbar, nicht nur brutto?", "Der Bericht rechnet mit " + r.capText + ". Nutzbar ist meist 90–100 % der Bruttoangabe."]);
    if (r.verdict === "gross") q.push(["Gibt es dasselbe System mit " + r.rec.cap + " kWh, und was kostet es dann?", "Nach dieser Rechnung bringt " + r.rec.cap + " kWh fast denselben Nutzen. Frag nach dem genauen Preisunterschied."]);
    if (r.verdict === "gross" || r.verdict === "klein") q.push(["Ist der Speicher modular, und was kostet später ein weiteres Modul?", "Dann kannst du klein anfangen und nachrüsten, wenn sich dein Verbrauch ändert, etwa durch E-Auto oder Wärmepumpe."]);
    if (r.verdict === "nolohn") q.push(["Was kostet die Anlage ohne Speicher, und lässt sich ein Speicher später nachrüsten?", "Bei diesen Preisen holt kein Speicher seine Kosten herein. Ein Wechselrichter, der später einen Speicher aufnehmen kann, hält dir die Option offen."]);
    if (!(o.pow > 0)) q.push(["Mit wie viel kW lädt und entlädt der Speicher?", "Der Bericht nimmt die halbe Kapazität pro Stunde an, höchstens 5 kW. Ist die Leistung kleiner, deckt der Speicher abendliche Spitzen schlechter."]);
    else if (o.pow < r.cap * 0.3) q.push(["Reicht die Lade- und Entladeleistung von " + String(o.pow).replace(".", ",") + " kW?", "Im Verhältnis zur Größe ist sie klein. An sonnigen Tagen wird der Speicher dann nicht voll, und Lastspitzen kommen aus dem Netz."]);
    if (r.storeRate === "hoch" || r.storeRate === "teuer") q.push(["Wie setzt sich der Speicherpreis zusammen?", "Mit " + nf(r.storePerKwh) + " € je kWh liegt er über der üblichen Spanne von " + nf(r.storeBand.lo) + "–" + nf(r.storeBand.hi) + " €. Frag nach Speicher, Wechselrichter, Montage und Zählerschrank einzeln."]);
    if (r.pvRate === "hoch" || r.pvRate === "teuer") q.push(["Was ist im PV-Preis enthalten?", "Mit " + nf(r.pvPerKwp) + " € je kWp liegt die Anlage über der üblichen Spanne. Gerüst, Zählerschrank, Anmeldung und Optimierer erklären einen Teil davon, aber nicht beliebig viel."]);
    q.push(["Welche Garantie gibt es auf die Restkapazität?", "Üblich sind 10 Jahre mit mindestens 60–80 % Restkapazität. Wichtig ist, was bei weniger passiert und wer dann zahlt."]);
    q.push(["Sind Smart Meter und Steuerbox im Angebot, und wer zahlt den Messstellenbetrieb?", "Neue Anlagen ohne diese Technik dürfen nach dem Solarspitzengesetz nur 60 % ihrer Leistung einspeisen. Die jährlichen Messkosten gehören in die Rechnung."]);
    q.push(["Ist Notstrom oder Ersatzstrom enthalten, und was kostet er extra?", "Nicht jeder braucht ihn. Wenn er im Preis steckt, sollte er auch zu deinem Bedarf passen."]);
    return q;
  }

  function check(o) {
    var cap = usable(o), sp = storePrice(o, cap);
    var en = energy(o, cap), ec = econ(en, o, cap, sp.v);
    var kwp = o.roofs.reduce(function (s, r) { return s + r.kwp; }, 0);
    var band = perKwhBand(cap), perKwh = sp.v / cap;
    var pv = o.total > 0 ? o.total - sp.v : 0, pb = pvBand(kwp);
    var res = {
      cap: cap, capText: (Math.round(cap * 10) / 10).toLocaleString("de-DE") + " kWh nutzbar", kwp: kwp,
      gen: en.runs[0].r.gen, load: en.runs[0].r.load, base: en.runs[0].r,
      store: sp.v, storeEst: sp.est, storePerKwh: perKwh, storeBand: band, storeRate: sp.est ? null : rate(perKwh, band.lo, band.hi),
      pv: pv, pvPerKwp: pv > 0 ? pv / kwp : 0, pvBand: pb, pvRate: pv > 0 && kwp > 0 ? rate(pv / kwp, pb.lo, pb.hi) : null,
      rows: ec.rows, best: ec.best, offer: ec.offer, rec: ec.rec, tol: ec.tol, verdict: ec.verdict
    };
    // Grenznutzen: was jede weitere kWh im Jahr noch bringt
    res.marginal = ec.ints.slice(1).map(function (r, i) { return { cap: r.cap, add: r.save - ec.ints[i].save }; });
    res.days = S.daySeries(en.pr.gen, en.pr.load, cap, en.pr.fc, power(o, cap, cap));
    res.scen = scenarios(o, cap, sp.v, en, ec);
    res.robust = res.scen.every(function (s) { return s.verdict === res.verdict; });
    res.questions = questions(o, res);
    return res;
  }

  // Kostenlose Vorschau: nur die Einordnung, keine Zahlen
  function teaser(r) { return { verdict: r.verdict, storeRate: r.storeRate, pvRate: r.pvRate, storeEst: r.storeEst }; }

  return { check: check, teaser: teaser, usable: usable, FIX: FIX, BRUTTO: BRUTTO, MAXCAP: MAXCAP };
})();
if (typeof module !== "undefined") module.exports = PRO;
