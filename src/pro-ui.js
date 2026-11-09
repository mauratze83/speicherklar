/* Speicherklar Pro – Seite: Eingabe, kostenlose Einordnung, Freischaltung, Bericht. Braucht sim.js, draw.js, markt.js, pro.js, pro-config.js. */
(function () {
  var C = PRO_CONFIG, $ = function (id) { return document.getElementById(id); };
  var nf0 = new Intl.NumberFormat("de-DE", { maximumFractionDigits: 0 });
  var nf1 = new Intl.NumberFormat("de-DE", { minimumFractionDigits: 1, maximumFractionDigits: 1 });
  var nf2 = new Intl.NumberFormat("de-DE", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  var euro = function (v) { return (v < -0.5 ? "−" : "") + nf0.format(Math.abs(Math.round(v))) + " €"; };
  var signed = function (v) { return (v >= 0.5 ? "+" : "") + euro(v); };
  var kwp = function (v) { return nf1.format(v).replace(",0", "") + " kWp"; };
  var kwh = function (v) { return (Math.abs(v - Math.round(v)) < 0.05 ? nf0.format(Math.round(v)) : nf1.format(v)) + " kWh"; };
  var esc = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); };
  var MONTHS = ["Jan", "Feb", "Mär", "Apr", "Mai", "Jun", "Jul", "Aug", "Sep", "Okt", "Nov", "Dez"];
  var ASPECTS = [["0", "Süd"], ["-45", "Südost"], ["45", "Südwest"], ["-90", "Ost"], ["90", "West"], ["-135", "Nordost"], ["135", "Nordwest"], ["180", "Nord"]];
  var ASPECT_NAME = {}; ASPECTS.forEach(function (a) { ASPECT_NAME[a[0]] = a[1]; });
  var KEY_IN = "sk-pro-eingabe", KEY_LIC = "sk-pro-lizenz";
  var state = { capKind: "nutzbar", evTime: "eve", eeg: "now", roofs: [], monthly: null, result: null, input: null, unlocked: false };

  function store(k, v) { try { if (v === null) localStorage.removeItem(k); else localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} }
  function load(k) { try { return JSON.parse(localStorage.getItem(k)); } catch (e) { return null; } }
  function track(n) { try { if (window.umami) window.umami.track(n); } catch (e) {} }
  function num(id) { var v = $(id).value.replace(",", "."); return v === "" ? 0 : +v; }

  // ---------- Schaltergruppen ----------
  function seg(id, key, after) {
    var btns = document.querySelectorAll("#" + id + " button");
    Array.prototype.forEach.call(btns, function (b) {
      b.addEventListener("click", function () { setSeg(id, key, b.getAttribute("data-v")); if (after) after(); });
    });
  }
  function setSeg(id, key, v) {
    state[key] = v;
    Array.prototype.forEach.call(document.querySelectorAll("#" + id + " button"), function (b) { b.setAttribute("aria-pressed", String(b.getAttribute("data-v") === v)); });
  }

  // ---------- Dachflächen ----------
  function drawRoofs() {
    var html = state.roofs.map(function (r, i) {
      var opts = ASPECTS.map(function (a) { return '<option value="' + a[0] + '"' + (String(r.aspect) === a[0] ? " selected" : "") + ">" + a[1] + "</option>"; }).join("");
      return '<div class="roof" data-i="' + i + '"><div class="roofhead"><span class="flabel">Dachfläche ' + (i + 1) + "</span>" +
        (state.roofs.length > 1 ? '<button type="button" class="linkbtn rm" data-rm="' + i + '" aria-label="Dachfläche ' + (i + 1) + ' entfernen">entfernen</button>' : "") + "</div>" +
        '<div class="roofgrid">' +
        '<label>Leistung<span class="unitin"><input class="in" type="number" min="0.5" max="50" step="0.01" inputmode="decimal" data-k="kwp" value="' + r.kwp + '"><span>kWp</span></span></label>' +
        "<label>Ausrichtung<select class=\"in\" data-k=\"aspect\">" + opts + "</select></label>" +
        '<label>Neigung<span class="unitin"><input class="in" type="number" min="0" max="90" step="1" inputmode="numeric" data-k="tilt" value="' + r.tilt + '"><span>°</span></span></label>' +
        '<label>Höchstens<span class="unitin"><input class="in" type="number" min="0" max="60" step="0.01" inputmode="decimal" data-k="max" placeholder="optional" value="' + (r.max > 0 ? r.max : "") + '"><span>kWp</span></span></label>' +
        "</div></div>";
    }).join("");
    $("roofs").innerHTML = html;
  }
  $("roofs").addEventListener("input", function (e) {
    var k = e.target.getAttribute("data-k"); if (!k) return;
    var i = +e.target.closest(".roof").getAttribute("data-i");
    state.roofs[i][k] = k === "aspect" ? +e.target.value : +String(e.target.value).replace(",", ".");
  });
  $("roofs").addEventListener("click", function (e) {
    var i = e.target.getAttribute("data-rm"); if (i === null) return;
    state.roofs.splice(+i, 1); drawRoofs();
  });
  $("add-roof").addEventListener("click", function () { state.roofs.push({ kwp: 3, aspect: 0, tilt: 30 }); drawRoofs(); });

  // ---------- Monatswerte ----------
  function drawMonths() {
    $("months").innerHTML = MONTHS.map(function (m, i) {
      return '<label>' + m + '<input class="in" type="number" min="0" max="5000" step="1" inputmode="numeric" data-m="' + i + '" value="' + (state.monthly ? state.monthly[i] : "") + '"></label>';
    }).join("") + '<p class="hint">Haushaltsstrom ohne E-Auto und Wärmepumpe. Die Summe ersetzt den Jahreswert.</p>';
  }
  $("tog-month").addEventListener("click", function () {
    var open = $("months").hidden;
    $("months").hidden = !open; this.setAttribute("aria-expanded", String(open));
    this.textContent = open ? "Nur Jahreswert verwenden" : "Verbrauch nach Monaten eingeben";
    if (open) { if (!state.monthly) state.monthly = new Array(12).fill(""); drawMonths(); } else state.monthly = null;
  });
  $("months").addEventListener("input", function (e) {
    var m = e.target.getAttribute("data-m"); if (m === null) return;
    state.monthly[+m] = e.target.value;
    var s = state.monthly.reduce(function (a, b) { return a + (+b || 0); }, 0);
    if (s > 0) $("f-cons").value = Math.round(s);
  });

  // Sonnendaten: zweistelliges PLZ-Gebiet (PLZ2, aus PVGIS), sonst die Großregion aus dem kostenlosen Rechner
  function regionOf(plz) {
    plz = String(plz || "").replace(/\D/g, ""); if (plz.length !== 5) return null;
    var a = typeof PLZ2 !== "undefined" && PLZ2[plz.slice(0, 2)];
    if (a) return { lat: a.lat, lon: a.lon, H: a.H, Kd: a.Kd, n: a.n, area: "PLZ-Gebiet " + plz.slice(0, 2) };
    var R = REGIONS[plz[0]]; return R ? { lat: R.lat, lon: R.lon, H: R.H, Kd: R.Kd, n: R.n, area: "PLZ-Region " + plz[0] } : null;
  }
  $("f-plz").addEventListener("input", function () {
    var r = regionOf(this.value);
    var empty = !this.value.trim();
    $("o-plz").textContent = r ? r.area + ": " + r.n : empty ? "für die Sonnendaten" : "5-stellige PLZ";
    $("o-plz").className = r || empty ? "" : "warn";
  });

  seg("capkind", "capKind"); seg("evtime", "evTime");
  seg("eeg", "eeg", function () {
    if (state.eeg === "reform") { state.prevFeed = $("f-feed").value; $("f-feed").value = 0; }
    else $("f-feed").value = state.prevFeed && +state.prevFeed > 0 ? state.prevFeed : 7.7;
  });

  // ---------- Eingaben lesen, speichern, vorbefüllen ----------
  function read() {
    var monthly = null;
    if (state.monthly) { var m = state.monthly.map(function (v) { return +v || 0; }); if (m.every(function (v) { return v > 0; })) monthly = m; }
    return {
      model: $("f-model").value.trim().slice(0, 60), cap: num("f-cap"), capKind: state.capKind, pow: num("f-pow"),
      total: num("f-total"), store: num("f-store"), plz: $("f-plz").value.trim(), region: regionOf($("f-plz").value),
      roofs: state.roofs.map(function (r) { return { kwp: +r.kwp || 0, aspect: +r.aspect, tilt: +r.tilt || 0, max: +r.max > +r.kwp ? +r.max : 0 }; }),
      cons: num("f-cons"), monthly: monthly, ev: num("f-ev"), evTime: state.evTime, hp: num("f-hp"),
      price: num("f-price"), eeg: state.eeg, feed: num("f-feed"), feedLimit: state.eeg === "reform" ? 0.5 : 0, life: num("f-life") || 15
    };
  }
  function validate(o) {
    if (!(o.cap >= 1)) return ["f-cap", "Bitte gib die Speicherkapazität aus dem Angebot ein."];
    if (!o.region) return ["f-plz", "Bitte gib eine 5-stellige Postleitzahl ein."];
    if (!o.roofs.length || o.roofs.some(function (r) { return !(r.kwp > 0); })) return ["roofs", "Bitte gib für jede Dachfläche die Leistung in kWp ein."];
    if (!(o.cons >= 500)) return ["f-cons", "Bitte gib deinen Haushaltsstrom pro Jahr ein (mindestens 500 kWh)."];
    if (!(o.price >= 10)) return ["f-price", "Bitte gib deinen Strompreis in ct/kWh ein."];
    if (o.store > 0 && o.total > 0 && o.store >= o.total) return ["f-store", "Der Speicheranteil ist größer als der Gesamtpreis. Bitte prüf die beiden Werte."];
    return null;
  }
  function fill(o) {
    $("f-model").value = o.model || ""; $("f-cap").value = o.cap || ""; $("f-pow").value = o.pow || "";
    $("f-total").value = o.total || ""; $("f-store").value = o.store || ""; $("f-plz").value = o.plz || "";
    $("f-cons").value = o.cons || ""; $("f-ev").value = o.ev || ""; $("f-hp").value = o.hp || "";
    $("f-price").value = o.price || ""; $("f-feed").value = o.feed != null ? o.feed : 7.7; $("f-life").value = o.life || 15;
    setSeg("capkind", "capKind", o.capKind || "nutzbar"); setSeg("evtime", "evTime", o.evTime || "eve"); setSeg("eeg", "eeg", o.eeg || "now");
    state.roofs = (o.roofs && o.roofs.length ? o.roofs : [{ kwp: 9, aspect: 0, tilt: 35 }]).map(function (r) { return { kwp: r.kwp, aspect: r.aspect, tilt: r.tilt, max: r.max || "" }; });
    drawRoofs();
    if (o.monthly) { state.monthly = o.monthly.slice(); $("months").hidden = false; $("tog-month").setAttribute("aria-expanded", "true"); $("tog-month").textContent = "Nur Jahreswert verwenden"; drawMonths(); }
    $("f-plz").dispatchEvent(new Event("input"));
  }
  // Übergabe aus dem kostenlosen Rechner: speicherklar.de/pro/#plz=…&kwp=… (Hash, geht nicht an einen Server)
  function fromHash() {
    var h = location.hash.slice(1); if (!/plz=|kwp=/.test(h)) return null;
    var q = {}; h.split("&").forEach(function (kv) { var p = kv.split("="); q[p[0]] = decodeURIComponent(p[1] || ""); });
    var kwp = +q.kwp || 9, tilt = +q.tilt || 35;
    var roofs = q.aspect === "ow" ? [{ kwp: kwp / 2, aspect: -90, tilt: tilt }, { kwp: kwp / 2, aspect: 90, tilt: tilt }] : [{ kwp: kwp, aspect: +q.aspect || 0, tilt: tilt }];
    history.replaceState(null, "", location.pathname + location.search);
    return { plz: q.plz || "", roofs: roofs, cons: +q.cons || 4500, ev: +q.ev || 0, evTime: q.evt === "day" ? "day" : "eve", cap: +q.bat || "",
      price: +q.price || 33, eeg: q.eeg === "reform" ? "reform" : "now", feed: q.feed != null ? +q.feed : 7.7, life: +q.life || 15 };
  }

  // ---------- Kostenlose Einordnung ----------
  var VERDICT = {
    passt: ["ok", "Größe passt", "Die Speichergröße passt zu deinem Haushalt."],
    gross: ["warn", "Eher zu groß", "Der Speicher ist größer, als es sich für deinen Haushalt rechnet."],
    klein: ["warn", "Eher zu klein", "Ein etwas größerer Speicher würde sich für deinen Haushalt besser rechnen."],
    nolohn: ["bad", "Rechnet sich nicht", "Bei diesem Preis holt kein Speicher seine Kosten herein."]
  };
  var PVSIZE = {
    passt: ["ok", "Größe passt", "Die Größe der PV-Anlage passt."],
    offen: ["ok", "Passt, mehr könnte sich lohnen", "Mehr Leistung würde sich lohnen, falls dein Dach Platz hat.", "Trag ein, wie viel kWp maximal aufs Dach passen."],
    mehr: ["warn", "Größer lohnt sich", "Eine größere PV-Anlage würde sich lohnen."],
    weniger: ["warn", "Kleiner reicht", "Eine kleinere PV-Anlage würde fast genauso viel bringen."]
  };
  var RATE = { guenstig: ["ok", "günstig"], ueblich: ["ok", "üblich"], hoch: ["warn", "eher hoch"], teuer: ["bad", "teuer"] };
  function amp(cls, k, v, d) { return '<div class="amp ' + cls + '"><span class="dot" aria-hidden="true"></span><div><div class="k">' + k + '</div><div class="v">' + v + "</div>" + (d ? '<div class="d">' + d + "</div>" : "") + "</div></div>"; }
  function amps(t, o) {
    var v = VERDICT[t.verdict], s = "";
    s += amp(v[0], "Speichergröße", v[1]);
    var pz = PVSIZE[t.pvSize]; s += amp(pz[0], "Größe der PV-Anlage", pz[1], pz[3]);
    s += t.storeRate ? amp(RATE[t.storeRate][0], "Speicherpreis je kWh", RATE[t.storeRate][1]) : amp("na", "Speicherpreis je kWh", "nicht prüfbar", "Dafür fehlt der Preis des Speichers allein.");
    s += t.pvRate ? amp(RATE[t.pvRate][0], "Preis der PV-Anlage je kWp", RATE[t.pvRate][1]) : amp("na", "Preis der PV-Anlage je kWp", "nicht prüfbar", o.total > 0 ? "Dafür fehlt der Preis des Speichers allein." : "Dafür fehlt der Gesamtpreis.");
    return s;
  }
  function showTeaser() {
    var r = state.result, t = PRO.teaser(r);
    $("t-empty").hidden = true; $("t-res").hidden = false;
    $("t-verdict").innerHTML = VERDICT[t.verdict][2] + " " + PVSIZE[t.pvSize][2];
    $("t-amps").innerHTML = amps(t, state.input);
  }

  function runCheck(scroll) {
    var o = read(), err = validate(o);
    $("formerr").textContent = err ? err[1] : "";
    if (err) { var el = $(err[0]); if (el && el.focus) el.focus(); return; }
    store(KEY_IN, o);
    var btn = $("go"); btn.disabled = true; btn.textContent = "Rechne…";
    setTimeout(function () {
      state.input = o; state.result = PRO.check(o);
      btn.disabled = false; btn.textContent = "Angebot prüfen";
      showTeaser(); track("pro-geprueft");
      if (state.unlocked) { renderReport(); if (scroll) $("report-wrap").scrollIntoView({ behavior: "smooth" }); }
      else if (scroll) $("teaser").scrollIntoView({ behavior: "smooth", block: "start" });
    }, 30);
  }
  $("offer").addEventListener("submit", function (e) { e.preventDefault(); runCheck(true); });

  // ---------- Kauf ----------
  function today() { return new Date().toISOString().slice(0, 10); }
  function dateDe(iso) { var p = iso.split("-"); return p[2] + "." + p[1] + "." + p[0]; }
  function setupBuy() {
    var vorab = /[?&]vorab=1/.test(location.search) || load("sk-pro-vorab");
    if (/[?&]vorab=1/.test(location.search)) store("sk-pro-vorab", true);
    var open = C.checkoutUrl && C.organizationId && (!C.publicFrom || today() >= C.publicFrom || vorab);
    var intro = C.introUntil && today() <= C.introUntil;
    var price = intro ? C.price : C.regularPrice;
    $("b-price").innerHTML = price + " € <small>einmalig</small>";
    var note = [];
    if (intro) note.push("Einführungspreis bis " + dateDe(C.introUntil) + ", danach " + C.regularPrice + " €.");
    if (open) {
      $("b-btn").href = C.checkoutUrl; $("b-btn").textContent = "Bericht freischalten · " + price + " €";
      $("b-btn").addEventListener("click", function () { track("pro-kauf-klick"); });
      note.push("Bezahlung über Polar. Den Lizenzschlüssel bekommst du per Mail, dann hier eingeben.");
      if (C.publicFrom && today() < C.publicFrom) note.push("Vorab-Zugang für die Warteliste.");
    } else {
      $("b-btn").removeAttribute("href"); $("b-btn").classList.remove("btn-on"); $("b-btn").setAttribute("aria-disabled", "true");
      $("b-btn").textContent = C.publicFrom ? "Kauf ab " + dateDe(C.publicFrom) : "Kauf startet bald";
      note.push('Trag dich auf der <a href="../#pro">Warteliste</a> ein, dann bekommst du den Vorab-Zugang.');
    }
    $("b-note").innerHTML = note.join(" ");
  }

  // ---------- Freischaltung (Polar-Lizenzschlüssel, öffentliche Prüfung ohne Server) ----------
  var LICENSE = {
    api: function () { return C.sandbox ? "https://sandbox-api.polar.sh" : "https://api.polar.sh"; },
    verify: function (key) {
      if (/^(localhost|127\.0\.0\.1)$/.test(location.hostname) && key === "DEV-SPEICHERKLAR") return Promise.resolve({ ok: true });
      if (!C.organizationId) return Promise.resolve({ ok: false, msg: "Der Verkauf ist noch nicht gestartet." });
      var body = { key: key, organization_id: C.organizationId };
      if (C.benefitId) body.benefit_id = C.benefitId;
      return fetch(this.api() + "/v1/customer-portal/license-keys/validate", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) })
        .then(function (r) {
          if (r.ok) return r.json().then(function (j) { return j.status === "granted" ? { ok: true } : { ok: false, msg: "Dieser Schlüssel ist nicht mehr gültig." }; });
          if (r.status === 404) return { ok: false, msg: "Diesen Schlüssel kennen wir nicht. Bitte kopier ihn genau aus der Kaufbestätigung." };
          return { ok: false, net: true, msg: "Die Prüfung hat gerade nicht geklappt. Bitte versuch es gleich noch einmal." };
        }, function () { return { ok: false, net: true, msg: "Keine Verbindung zur Prüfung. Bitte versuch es gleich noch einmal." }; });
    }
  };
  function unlock() {
    state.unlocked = true; $("buy").hidden = true; $("keybox").hidden = true; $("teaser").classList.add("unlocked");
    if (state.result) renderReport();
  }
  $("keyform").addEventListener("submit", function (e) {
    e.preventDefault();
    var key = $("f-key").value.trim(), msg = $("keymsg"), btn = $("keybtn");
    if (key.length < 6) { msg.textContent = "Bitte gib den Schlüssel aus der Kaufbestätigung ein."; msg.className = "wait-msg err"; return; }
    btn.disabled = true; btn.textContent = "Prüfe…";
    LICENSE.verify(key).then(function (res) {
      btn.disabled = false; btn.textContent = "Freischalten";
      if (res.ok) { store(KEY_LIC, { key: key, at: Date.now() }); msg.textContent = ""; track("pro-freigeschaltet"); unlock(); $("report-wrap").scrollIntoView({ behavior: "smooth" }); }
      else { msg.textContent = res.msg; msg.className = "wait-msg err"; }
    });
  });
  // Gespeicherten Schlüssel nachprüfen: offline bleibt freigeschaltet, nur ein ausdrücklich ungültiger Schlüssel sperrt
  function restoreLicense() {
    var lic = load(KEY_LIC); if (!lic || !lic.key) return;
    unlock();
    if (Date.now() - (lic.at || 0) > 7 * 864e5) LICENSE.verify(lic.key).then(function (res) {
      if (res.ok) store(KEY_LIC, { key: lic.key, at: Date.now() });
      else if (!res.net) { store(KEY_LIC, null); location.reload(); }
    });
  }

  // ---------- Bericht ----------
  function sizeChart(r) {
    var rows = r.rows.filter(function (x) { return Math.abs(x.cap - Math.round(x.cap)) < 1e-9 || Math.abs(x.cap - r.cap) < 1e-9; });
    var W = 640, H = 260, box = { l: 70, t: 22, w: W - 70 - 12, h: H - 22 - 46 };
    var vals = rows.map(function (x) { return x.net; }), max = Math.max(0, Math.max.apply(null, vals)), min = Math.min(0, Math.min.apply(null, vals));
    var step = DRAW.niceStep(max - min || 1, 5), top = Math.ceil(max / step) * step, bot = Math.floor(min / step) * step; if (top === bot) top = bot + step;
    var X = function (c) { return box.l + box.w * c / PRO.MAXCAP; }, Y = function (v) { return box.t + box.h * (top - v) / (top - bot); };
    var s = "";
    for (var v = bot; v <= top + 1e-9; v += step) {
      s += '<line class="grid' + (Math.abs(v) < 1e-9 ? " zero" : "") + '" x1="' + box.l + '" x2="' + (box.l + box.w) + '" y1="' + Y(v).toFixed(1) + '" y2="' + Y(v).toFixed(1) + '"/>';
      s += '<text class="ax" x="' + (box.l - 8) + '" y="' + (Y(v) + 4).toFixed(1) + '" text-anchor="end">' + (v < 0 ? "−" : v > 0 ? "+" : "") + nf0.format(Math.abs(v)) + " €</text>";
    }
    for (var c = 0; c <= PRO.MAXCAP; c += 2) s += '<text class="ax" x="' + X(c).toFixed(1) + '" y="' + (box.t + box.h + 18) + '" text-anchor="middle">' + c + "</text>";
    s += '<text class="ax" x="' + (box.l + box.w) + '" y="' + (H - 4) + '" text-anchor="end">Speichergröße in kWh (nutzbar)</text>';
    var tolTop = Y(r.best.net), tolBot = Y(r.best.net - r.tol);
    s += '<rect class="tolband" x="' + box.l + '" width="' + box.w + '" y="' + tolTop.toFixed(1) + '" height="' + Math.max(1, tolBot - tolTop).toFixed(1) + '"/>';
    var ints = rows.filter(function (x) { return Math.abs(x.cap - Math.round(x.cap)) < 1e-9; });
    s += '<path class="sline s0" d="' + ints.map(function (x, i) { return (i ? "L" : "M") + X(x.cap).toFixed(1) + "," + Y(x.net).toFixed(1); }).join("") + '"/>';
    function mark(x, cls, label, below) {
      var px = X(x.cap), py = Y(x.net), ly = below ? py + 20 : py - 10;
      var anchor = px < box.l + 40 ? "start" : px > box.l + box.w - 40 ? "end" : "middle";
      return '<circle class="mk ' + cls + '" cx="' + px.toFixed(1) + '" cy="' + py.toFixed(1) + '" r="6"/><text class="mklabel ' + cls + '" x="' + px.toFixed(1) + '" y="' + ly.toFixed(1) + '" text-anchor="' + anchor + '">' + label + "</text>";
    }
    var same = Math.abs(r.rec.cap - r.cap) < 0.5;
    if (!same && r.rec.cap > 0) s += mark(r.rec, "rec", "Empfehlung " + kwh(r.rec.cap), r.offer.net > r.rec.net && Math.abs(r.offer.cap - r.rec.cap) < 8);
    s += mark(r.offer, "off", "Angebot " + kwh(r.cap), !same && r.offer.net < r.rec.net && Math.abs(r.offer.cap - r.rec.cap) < 8);
    return '<svg class="rchart" viewBox="0 0 ' + W + " " + H + '" role="img" aria-label="Bilanz nach Lebensdauer je Speichergröße">' + s + "</svg>" +
      '<div class="clegend"><span><i class="sw sl s0"></i>Bilanz nach ' + state.input.life + ' Jahren</span><span><i class="sw tolsw"></i>fast so gut wie die beste Größe</span><span><i class="sw dotoff"></i>Angebot</span>' + (same ? "" : '<span><i class="sw dotrec"></i>Empfehlung</span>') + "</div>";
  }

  function pvChart(r, curName, altName) {
    var A = r.pvSize.rows, B = r.pvAlt.rows, W = 640, H = 270, box = { l: 74, t: 24, w: W - 74 - 14, h: H - 24 - 50 };
    var all = A.concat(B).map(function (x) { return x.total; }), max = Math.max(0, Math.max.apply(null, all)), min = Math.min(0, Math.min.apply(null, all));
    var step = DRAW.niceStep(max - min || 1, 5), top = Math.ceil(max / step) * step, bot = Math.floor(min / step) * step; if (top === bot) top = bot + step;
    var k0 = A[0].K, k1 = A[A.length - 1].K, X = function (k) { return box.l + box.w * (k - k0) / ((k1 - k0) || 1); }, Y = function (v) { return box.t + box.h * (top - v) / (top - bot); };
    var s = "";
    for (var v = bot; v <= top + 1e-9; v += step) {
      s += '<line class="grid' + (Math.abs(v) < 1e-9 ? " zero" : "") + '" x1="' + box.l + '" x2="' + (box.l + box.w) + '" y1="' + Y(v).toFixed(1) + '" y2="' + Y(v).toFixed(1) + '"/>';
      s += '<text class="ax" x="' + (box.l - 8) + '" y="' + (Y(v) + 4).toFixed(1) + '" text-anchor="end">' + (v < 0 ? "−" : v > 0 ? "+" : "") + nf0.format(Math.abs(v)) + " €</text>";
    }
    var tstep = DRAW.niceStep(k1 - k0 || 1, 6);
    for (var k = Math.ceil(k0 / tstep) * tstep; k <= k1 + 1e-9; k += tstep) s += '<text class="ax" x="' + X(k).toFixed(1) + '" y="' + (box.t + box.h + 18) + '" text-anchor="middle">' + nf1.format(k).replace(",0", "") + "</text>";
    s += '<text class="ax" x="' + (box.l + box.w) + '" y="' + (H - 4) + '" text-anchor="end">PV-Leistung in kWp, jeweils mit passendem Speicher</text>';
    var line = function (rows, cls) { return '<path class="sline ' + cls + '" d="' + rows.map(function (x, i) { return (i ? "L" : "M") + X(x.K).toFixed(1) + "," + Y(x.total).toFixed(1); }).join("") + '"/>'; };
    s += line(B, "s2 alt") + line(A, "s0");
    var mk = function (x, cls, label, below) {
      var px = X(x.K), py = Y(x.total), anchor = px < box.l + 50 ? "start" : px > box.l + box.w - 50 ? "end" : "middle";
      return '<circle class="mk ' + cls + '" cx="' + px.toFixed(1) + '" cy="' + py.toFixed(1) + '" r="6"/><text class="mklabel ' + cls + '" x="' + px.toFixed(1) + '" y="' + (below ? py + 20 : py - 10).toFixed(1) + '" text-anchor="' + anchor + '">' + label + "</text>";
    };
    var bo = r.pvSize.best, of = r.pvSize.offer;
    if (bo !== of) s += mk(bo, "rec", "beste " + kwp(bo.K), false);
    s += mk(of, "off", "Angebot " + kwp(of.K), bo !== of && Math.abs(X(bo.K) - X(of.K)) < 120);
    return '<svg class="rchart" viewBox="0 0 ' + W + " " + H + '" role="img" aria-label="Bilanz je PV-Größe mit passendem Speicher">' + s + "</svg>" +
      '<div class="clegend"><span><i class="sw sl s0"></i>' + curName + ' (deine Annahme)</span><span><i class="sw sl s2"></i>' + altName + '</span><span><i class="sw dotoff"></i>Angebot</span>' + (bo !== of ? '<span><i class="sw dotrec"></i>beste Größe</span>' : "") + "</div>";
  }

  function dayText(m, name) {
    var socMax = Math.max.apply(null, m.soc), full = -1, imp = 0;
    for (var h = 0; h < 24; h++) { imp += m.imp[h]; if (full < 0 && m.soc[h] >= 0.95) full = h; }
    return full >= 0 ? "Im " + name + " ist der Speicher im Schnitt gegen " + (full + 1) + " Uhr voll. Aus dem Netz kommen " + nf1.format(imp) + " kWh am Tag."
      : "Im " + name + " erreicht der Speicher im Schnitt höchstens " + Math.round(socMax * 100) + " % Füllstand" + (socMax >= 0.8 ? ", an sonnigen Tagen wird er voll, an trüben nicht" : "") + ". Aus dem Netz kommen " + nf1.format(imp) + " kWh am Tag.";
  }

  function renderReport() {
    var r = state.result, o = state.input, life = o.life, same = Math.abs(r.rec.cap - r.cap) < 0.5;
    var v = VERDICT[r.verdict], t = PRO.teaser(r), off = r.offer, rec = r.rec;
    var stand = new Date().toLocaleDateString("de-DE", { day: "2-digit", month: "2-digit", year: "numeric" });
    var roofsTxt = o.roofs.map(function (x) { return nf1.format(x.kwp) + " kWp " + ASPECT_NAME[String(x.aspect)] + " " + x.tilt + "°"; }).join(", ");
    var h = "";

    h += '<header class="rhead"><div class="eyebrow">Speicherklar Pro · Angebots-Check · ' + stand + "</div>" +
      "<h1>" + (o.model ? esc(o.model) + ", " : "") + kwp(r.kwp) + " und " + kwh(r.cap) + " Speicher</h1>" +
      '<p class="rmeta">' + roofsTxt + " · " + o.region.area + " (" + o.region.n + ") · " + nf0.format(o.cons) + " kWh Haushalt" +
      (o.ev ? " · " + nf0.format(o.ev) + " kWh E-Auto" : "") + (o.hp ? " · " + nf0.format(o.hp) + " kWh Wärmepumpe" : "") + "</p></header>";

    // 1 Ergebnis
    h += '<section class="rsec"><h2><span>1</span>Ergebnis auf einen Blick</h2>';
    var lead = v[2] + " ";
    if (r.verdict === "gross") lead += "Mit " + kwh(rec.cap) + " statt " + kwh(r.cap) + " zahlst du geschätzt " + euro(off.cost - rec.cost) + " weniger und hast nach " + life + " Jahren " + (rec.net >= off.net ? euro(rec.net - off.net) + " mehr übrig." : "fast gleich viel übrig.");
    else if (r.verdict === "klein") lead += "Mit " + kwh(rec.cap) + " statt " + kwh(r.cap) + " hättest du nach " + life + " Jahren rund " + euro(rec.net - off.net) + " mehr übrig, bei geschätzt " + euro(rec.cost - off.cost) + " höherem Preis.";
    else if (r.verdict === "passt") lead += off.net >= 0 ? "Der Speicher holt seine Kosten nach etwa " + nf1.format(off.payback) + " Jahren herein." : "";
    else lead += "Nach " + life + " Jahren fehlen beim Angebot rund " + euro(-off.net) + ". Ohne Speicher stehst du wirtschaftlich besser da.";
    var pv = r.pvSize, pvo = pv.offer, pvr = pv.rec;
    if (pv.verdict === "mehr") lead += " Bei der PV-Anlage lohnt sich mehr Leistung: Mit " + kwp(pvr.K) + " statt " + kwp(pv.Ko) + " blieben nach " + PRO.PVLIFE + " Jahren rund " + euro(pvr.total - pvo.total) + " mehr übrig, dann am besten mit " + kwh(pvr.bestCap) + " Speicher.";
    else if (pv.verdict === "weniger") lead += " Bei der PV-Anlage reichen " + kwp(pvr.K) + " statt " + kwp(pv.Ko) + ": fast dasselbe Ergebnis bei geschätzt " + euro(pvo.pvCost - pvr.pvCost) + " weniger Anschaffung.";
    else if (pv.verdict === "offen") lead += " Die PV-Anlage passt. Jedes weitere kWp würde sich lohnen, wenn dein Dach Platz hat.";
    else lead += " Die Größe der PV-Anlage passt.";
    h += '<p class="rlead">' + lead + "</p>";
    h += '<div class="amps">' + amps(t, o) + "</div>";
    var cols = same || r.verdict === "nolohn" ? [["Angebot · " + kwh(r.cap), off]] : [["Angebot · " + kwh(r.cap), off], ["Empfehlung · " + kwh(rec.cap), rec]];
    var row = function (label, f, note) { return "<tr><td>" + label + (note ? " <small>" + note + "</small>" : "") + "</td>" + cols.map(function (c) { return '<td class="num">' + f(c[1]) + "</td>"; }).join("") + "</tr>"; };
    h += '<div class="tablewrap"><table class="rtab"><thead><tr><th></th>' + cols.map(function (c) { return "<th>" + c[0] + "</th>"; }).join("") + "</tr></thead><tbody>" +
      row("Preis Speicher", function (x) { return euro(x.cost) + (x === off && !r.storeEst ? "" : "*"); }) +
      row("Zusätzlich selbst genutzt", function (x) { return nf0.format(x.extra) + " kWh/Jahr"; }) +
      row("Ersparnis pro Jahr", function (x) { return euro(x.save); }) +
      row("Amortisation", function (x) { return isFinite(x.payback) ? nf1.format(x.payback) + " Jahre" : "nie"; }) +
      row("Bilanz nach " + life + " Jahren", function (x) { return '<b class="' + (x.net >= 0 ? "pos" : "neg") + '">' + signed(x.net) + "</b>"; }) +
      row("Autarkie", function (x) { return Math.round(r.base.autarky * 100) + " % → " + Math.round(x.r.autarky * 100) + " %"; }, "ohne → mit Speicher") +
      "</tbody></table></div>";
    h += '<p class="fine">* geschätzt: ' + (r.storeEst ? "Speicherpreis aus der Marktspanne, weil das Angebot ihn nicht einzeln nennt. " : "") +
      "Für andere Größen zählt " + Math.round(PRO.FIX * 100) + " % des Speicherpreises als fester Anteil (Wechselrichter, Montage), der Rest wächst mit der Kapazität.</p></section>";

    // 2 Größe
    var mc = r.store * (1 - PRO.FIX) / r.cap, lastWorth = 0;
    r.marginal.forEach(function (m) { if (m.add * life >= mc) lastWorth = m.cap; });
    h += '<section class="rsec"><h2><span>2</span>Welche Speichergröße passt</h2>';
    h += "<p>Die Linie zeigt für jede Speichergröße, was nach " + life + " Jahren übrig bleibt: Ersparnis minus Anschaffung. Im grauen Band liegen Größen, die höchstens " + euro(r.tol) + " schlechter abschneiden als die beste. Die Empfehlung ist die kleinste Größe in diesem Band, weil ein kleinerer Speicher weniger Geld bindet.</p>";
    h += '<div class="chartwrap">' + sizeChart(r) + "</div>";
    h += "<p>Jede zusätzliche kWh kostet bei diesem Angebot etwa <b>" + euro(mc) + "</b>. Damit sie sich in " + life + " Jahren bezahlt macht, muss sie <b>" + euro(mc / life) + " im Jahr</b> sparen. " +
      (lastWorth > 0 ? "Das schafft jede kWh bis " + lastWorth + " kWh, danach bringt eine weitere kWh weniger, als sie kostet." : "Das schafft schon die erste kWh nicht.") + "</p>";
    var upto = Math.min(PRO.MAXCAP, Math.max(Math.ceil(r.cap), r.best.cap) + 2);
    h += '<div class="tablewrap"><table class="rtab mtab"><thead><tr><th>Größe</th><th>Ersparnis/Jahr</th><th>diese kWh bringt</th><th>Bilanz nach ' + life + " J.</th></tr></thead><tbody>";
    r.rows.filter(function (x) { return x.cap >= 1 && x.cap <= upto && (Math.abs(x.cap - Math.round(x.cap)) < 1e-9); }).forEach(function (x) {
      var m = r.marginal.filter(function (y) { return y.cap === x.cap; })[0];
      var isOff = Math.abs(x.cap - r.cap) < 0.5, isRec = x.cap === rec.cap;
      h += "<tr" + (isOff ? ' class="hl-off"' : isRec ? ' class="hl-rec"' : "") + "><td>" + x.cap + " kWh" + (isOff ? " <small>≈ Angebot</small>" : isRec ? " <small>Empfehlung</small>" : "") + '</td><td class="num">' + euro(x.save) + '</td><td class="num">' + (m ? "+" + euro(m.add) + "/Jahr" : "") + '</td><td class="num ' + (x.net >= 0 ? "pos" : "neg") + '">' + signed(x.net) + "</td></tr>";
    });
    h += "</tbody></table></div></section>";

    // 3 PV-Größe und beste Kombination
    var curName = o.eeg === "reform" ? "EEG-Reform 2027" : "EEG heute", altName = o.eeg === "reform" ? "EEG heute" : "EEG-Reform 2027", pa = r.pvAlt;
    h += '<section class="rsec"><h2><span>3</span>Passt die Größe der PV-Anlage?</h2>';
    h += "<p>Hier rechnet der Bericht PV-Anlage und Speicher zusammen: für jede Anlagengröße mit dem jeweils passenden Speicher. Die PV-Anlage zählt über " + PRO.PVLIFE + " Jahre, so lange läuft die EEG-Vergütung, der Speicher über " + life + " Jahre. " +
      (pv.maxGiven ? "Größer als " + kwp(pv.Kmax) + " geht nicht, so viel passt laut deinen Angaben aufs Dach." : "Wie viel aufs Dach passt, hast du nicht angegeben. Deshalb prüft der Bericht nur kleinere Anlagen als im Angebot.") + "</p>";
    h += '<div class="chartwrap">' + pvChart(r, curName, altName) + "</div>";
    h += "<p>Beste Kombination mit deinen Annahmen (" + curName + "): <b>" + kwp(pv.best.K) + " und " + kwh(pv.best.bestCap) + " Speicher</b>, Bilanz <b>" + signed(pv.best.total) + "</b>. Das Angebot mit " + kwp(pv.Ko) + " kommt mit passendem Speicher auf " + signed(pvo.total) + ". " +
      "Mit " + altName + " wäre es " + kwp(pa.best.K) + " und " + kwh(pa.best.bestCap) + " Speicher" + (Math.abs(pa.best.K - pv.best.K) >= 2 ? ". Die Einspeiseregeln ändern also die richtige Größe deutlich, und welche gilt, hängt vom Tag der Inbetriebnahme ab." : ". Die richtige Größe hängt hier kaum von den Einspeiseregeln ab.") + "</p>";
    var pick = pv.rows.filter(function (x, i, a) { return x === pv.best || x === pv.rec || x.isOffer || i === 0 || i === a.length - 1 || i % Math.max(1, Math.ceil(a.length / 6)) === 0; });
    h += '<div class="tablewrap"><table class="rtab"><thead><tr><th>PV-Leistung</th><th>Erzeugung/Jahr</th><th>PV allein, ' + PRO.PVLIFE + ' J.</th><th>passender Speicher</th><th>zusammen</th></tr></thead><tbody>';
    pick.forEach(function (x) {
      var tag = x.isOffer ? " <small>Angebot</small>" : x === pv.best ? " <small>beste</small>" : x === pv.rec && pv.verdict !== "passt" && pv.verdict !== "offen" ? " <small>Empfehlung</small>" : "";
      h += "<tr" + (x.isOffer ? ' class="hl-off"' : x === pv.best ? ' class="hl-rec"' : "") + "><td>" + kwp(x.K) + tag + '</td><td class="num">' + nf0.format(Math.round(x.gen / 10) * 10) + ' kWh</td><td class="num ' + (x.pvNet >= 0 ? "pos" : "neg") + '">' + signed(x.pvNet) + '</td><td class="num">' + (x.bestCap ? x.bestCap + " kWh" : "keiner") + '</td><td class="num"><b class="' + (x.total >= 0 ? "pos" : "neg") + '">' + signed(x.total) + "</b></td></tr>";
    });
    h += "</tbody></table></div>";
    h += '<p class="fine">' + (r.pvPriceEst ? "PV-Preis geschätzt, weil das Angebot den Speicher nicht einzeln nennt oder der Gesamtpreis fehlt. " : "") + "Preis für andere Größen: " + Math.round(PRO.FIX_PV * 100) + " % des PV-Preises fest (Gerüst, Zählerschrank, Anmeldung), der Rest je kWp. Vergütung nach EEG für Inbetriebnahme bis 31.01.2027: 7,70 ct bis 10 kWp, 6,66 ct für den Teil bis 40 kWp, anteilig gemittelt.</p></section>";

    // 4 Jahreszeiten
    h += '<section class="rsec"><h2><span>4</span>November gegen Juli</h2>';
    h += "<p>Ein durchschnittlicher Tag mit deinem Speicher (" + kwh(r.cap) + "). Im Sommer reicht der Überschuss meist, um ihn zu füllen, im Winter fehlt er. Ein größerer Speicher hilft im Winter deshalb kaum.</p>";
    h += DRAW.dayChart([r.days[6], r.days[10]], ["Juli", "November"]);
    h += "<p>" + dayText(r.days[6], "Juli") + " " + dayText(r.days[10], "November") + "</p></section>";

    // 4 Preise
    h += '<section class="rsec"><h2><span>5</span>Preis-Check</h2>';
    if (r.storeEst) h += "<p>Das Angebot nennt den Speicher nicht einzeln. Der Bericht rechnet mit geschätzten <b>" + euro(r.store) + "</b> (" + euro(r.store / r.cap) + " je kWh, Mitte der Marktspanne). Frag nach dem Preis ohne Speicher, dann wird der Check genau.</p>";
    else h += "<p>Speicher: <b>" + euro(r.storePerKwh) + " je kWh</b> nutzbar. Üblich sind " + nf0.format(r.storeBand.lo) + "–" + nf0.format(r.storeBand.hi) + " € je kWh inklusive Einbau" + (r.cap < MARKT.SPEICHER.kleinBis ? ", bei kleinen Speichern etwas mehr" : "") + ". Einordnung: <b>" + RATE[r.storeRate][1] + "</b>.</p>";
    if (r.pvRate) h += "<p>PV-Anlage ohne Speicher: <b>" + euro(r.pv) + "</b>, also <b>" + euro(r.pvPerKwp) + " je kWp</b>. Für " + nf1.format(r.kwp) + " kWp sind " + nf0.format(r.pvBand.lo) + "–" + nf0.format(r.pvBand.hi) + " € je kWp üblich. Einordnung: <b>" + RATE[r.pvRate][1] + "</b>." + (r.storeEst ? " Weil der Speicherpreis geschätzt ist, ist auch dieser Wert nur ein Anhaltspunkt." : "") + "</p>";
    else h += "<p>Für den Preis der PV-Anlage fehlt der Gesamtpreis im Angebot.</p>";
    h += '<p class="fine">Marktspannen Stand ' + MARKT.STAND + ": " + MARKT.QUELLEN.join("; ") + ". Teurer kann berechtigt sein, etwa bei schwieriger Montage, neuem Zählerschrank oder Notstrom. Dann sollte das im Angebot stehen.</p></section>";

    // 5 Szenarien
    var same5 = r.scen.filter(function (s) { return s.verdict === r.verdict; }).length;
    h += '<section class="rsec"><h2><span>6</span>Wie stabil ist das Ergebnis?</h2>';
    h += "<p>Niemand weiß, wie sich Strompreis und Regeln entwickeln. Deshalb rechnet der Bericht dein Angebot mit veränderten Annahmen nach. In <b>" + same5 + " von " + r.scen.length + "</b> Fällen bleibt die Einordnung gleich" + (same5 === r.scen.length ? ". Das Ergebnis ist robust." : ". Wo sie sich ändert, lohnt ein zweiter Blick.") + "</p>";
    h += '<div class="tablewrap"><table class="rtab"><thead><tr><th>Annahme</th><th>beste Größe</th><th>Bilanz Angebot</th><th>Einordnung</th></tr></thead><tbody>';
    r.scen.forEach(function (s, i) {
      h += "<tr" + (i === 0 ? ' class="hl-base"' : "") + "><td>" + s.name + '</td><td class="num">' + (s.best ? s.best + " kWh" : "ohne") + '</td><td class="num ' + (s.offerNet >= 0 ? "pos" : "neg") + '">' + signed(s.offerNet) + "</td><td>" + VERDICT[s.verdict][1] + "</td></tr>";
    });
    h += "</tbody></table></div></section>";

    // 6 Fragen
    h += '<section class="rsec"><h2><span>7</span>Fragen an deinen Installateur</h2><p>Zum Ausdrucken und Mitnehmen. Die ersten Fragen ergeben sich direkt aus deinem Angebot.</p><ol class="qs">';
    r.questions.forEach(function (q) { h += "<li><b>" + q[0] + "</b><span>" + q[1] + "</span></li>"; });
    h += "</ol></section>";

    // 7 Annahmen
    h += '<section class="rsec"><h2><span>8</span>Annahmen und Grenzen</h2><div class="tablewrap"><table class="rtab"><tbody>' +
      "<tr><td>Deine Eingaben</td><td>" + kwh(o.cap) + " " + (o.capKind === "brutto" ? "brutto, gerechnet mit " + Math.round(PRO.BRUTTO * 100) + " % nutzbar" : o.capKind === "unklar" ? "(Art nicht angegeben, gerechnet als nutzbar)" : "nutzbar") +
      (o.pow ? ", " + nf1.format(o.pow) + " kW Leistung" : ", Leistung nicht angegeben (gerechnet: halbe Kapazität pro Stunde, höchstens 5 kW)") +
      "; Strompreis " + nf2.format(o.price) + " ct/kWh; " + (o.eeg === "reform" ? "EEG-Reform 2027 (keine Vergütung, Einspeisung höchstens 50 %)" : "Einspeisevergütung " + nf2.format(o.feed) + " ct/kWh") + "; Lebensdauer " + life + " Jahre" + (o.monthly ? "; Verbrauch nach Monaten" : "") + "</td></tr>" +
      "<tr><td>Rechnung</td><td>Jahressimulation in 5-Minuten-Schritten mit Sonnendaten PVGIS-SARAH3 2014–2023 für " + o.region.area + " (Mittelpunkt " + nf2.format(o.region.lat) + "° N, " + nf2.format(o.region.lon) + "° O), Standardlastprofil H0" + (o.hp ? ", Wärmepumpe nach Heizmonaten verteilt" : "") + ". Speicher mit 88 % Wirkungsgrad je Zyklus und 25 W Standby. Erzeugung im Jahr: " + nf0.format(Math.round(r.gen / 10) * 10) + " kWh, Verbrauch: " + nf0.format(Math.round(r.load / 10) * 10) + " kWh.</td></tr>" +
      "<tr><td>Ort</td><td>Mittelpunkt des PLZ-Gebiets aus den Postleitzahlen von GeoNames (geonames.org, CC BY 4.0). Innerhalb eines Gebiets ändert sich die Sonneneinstrahlung im Monatsmittel nur wenig.</td></tr>" +
      "<tr><td>PV-Anlage</td><td>Rechenzeitraum " + PRO.PVLIFE + " Jahre. Wert = selbst genutzter Solarstrom zum Strompreis plus Einspeisung zur Vergütung. Größere Anlagen nutzen die zusätzliche Dachfläche, kleinere verkleinern alle Dachflächen gleichmäßig.</td></tr>" +
      "<tr><td>Andere Größen</td><td>" + Math.round(PRO.FIX * 100) + " % des Speicherpreises als fester Anteil. Ladeleistung wie im Angebot, bei kleineren Größen höchstens halbe Kapazität pro Stunde, mindestens 2,5 kW.</td></tr>" +
      "<tr><td>Nicht drin</td><td>Verschattung, Alterung des Akkus, steigende Strompreise, Zinsen, dynamische Tarife, Notstrom. Strompreis und Lebensdauer prüft Abschnitt 6.</td></tr>" +
      '</tbody></table></div><p class="fine">Dieser Bericht ist eine Rechnung mit deinen Angaben und keine Anlagen-, Rechts- oder Finanzberatung. Er ersetzt nicht die Planung durch einen Fachbetrieb. Erstellt mit Speicherklar Pro, speicherklar.de.</p></section>';

    $("report").innerHTML = h;
    $("report-wrap").hidden = false;
  }

  $("print").addEventListener("click", function () { track("pro-pdf"); window.print(); });
  $("edit").addEventListener("click", function () { $("offer").scrollIntoView({ behavior: "smooth" }); });
  window.addEventListener("beforeprint", function () { document.title = "Speicherklar Angebots-Check " + (state.input && state.input.model ? state.input.model : ""); });

  // ---------- Start ----------
  var start = fromHash() || load(KEY_IN) || { roofs: [{ kwp: 9, aspect: 0, tilt: 35 }], cons: 4500, price: 33, feed: 7.7, life: 15 };
  fill(start);
  setupBuy();
  restoreLicense();
  if (start.cap) runCheck(false);
})();
