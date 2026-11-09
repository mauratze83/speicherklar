var assert=require("assert"),S=require("../src/sim.js"),P=require("../src/pro.js");
var base={region:"4",roofs:[{kwp:9,tilt:35,aspect:0}],cons:4500,ev:0,evTime:"eve",hp:0,price:33,feed:7.7,feedLimit:0,eeg:"now",life:15,
  cap:10,capKind:"nutzbar",pow:5,total:19000,store:6500,model:"Test"};
function run(name,over){var o=Object.assign({},base,over||{});var t=Date.now(),r=P.check(o);
  console.log(name.padEnd(28),"verdict",r.verdict.padEnd(7),"best",String(r.best.cap).padStart(2),"rec",String(r.rec.cap).padStart(2),
   "offerNet",Math.round(r.offer.net),"bestNet",Math.round(r.best.net),"€/kWh",Math.round(r.storePerKwh),r.storeRate,"pv €/kWp",Math.round(r.pvPerKwp),r.pvRate,"robust",r.robust,(Date.now()-t)+"ms");
  return r;}
var r=run("10 kWh, 650 €/kWh");
run("15 kWh teuer",{cap:15,store:11000});
run("5 kWh günstig",{cap:5,store:2200});
run("brutto 10.24, ohne Preis",{cap:10.24,capKind:"brutto",store:0,pow:0});
run("Reform",{eeg:"reform",feed:0,feedLimit:0.5});
run("E-Auto + WP",{ev:3000,hp:4000,cap:12,store:7000});
run("Mehrere Dächer",{roofs:[{kwp:6,tilt:30,aspect:-90},{kwp:6,tilt:30,aspect:90},{kwp:2,tilt:10,aspect:0}],total:24000});
run("billig 3 kWh",{cap:3,store:1500});
r.scen.forEach(function(s){console.log("  ",s.name.padEnd(48),s.verdict,s.best,Math.round(s.offerNet));});
r.questions.forEach(function(q){console.log("  ?",q[0]);});
// Regression: kostenloser Rechner liefert dieselben Werte wie vorher
var p={region:"4",roofs:[{kwp:9,tilt:35,aspect:0}],cons:4500,ev:0,evTime:"eve",bat:8,bprice:500,life:15,price:33,feed:7.7,feedLimit:0};
var e=S.evaluate(p);console.log("free calc save",e.chosen.save.toFixed(4),"best",e.best.cap);
// Pro-Zeile für 8 kWh ohne Wärmepumpe muss mit dem kostenlosen Rechner übereinstimmen, wenn Leistung gleich
var r8=P.check(Object.assign({},base,{cap:8,pow:4,store:4000}));
var row=r8.rows.filter(function(x){return x.cap===8;})[0];
assert(Math.abs(row.save-e.chosen.save)<1e-6,"Abweichung zum kostenlosen Rechner "+row.save+" vs "+e.chosen.save);
console.log("OK");
// PV-Größe
var A=require("../src/plz2.json").gebiete["47"];
function pvrun(name,over){var o=Object.assign({},base,{region:A},over||{});var t=Date.now(),r=P.check(o),v=r.pvSize;
  console.log(name.padEnd(30),"PV",v.verdict.padEnd(7),"Angebot",v.Ko,"kWp",Math.round(v.offer.total),"| beste",v.best.K,"kWp +",v.best.bestCap,"kWh",Math.round(v.best.total),"| Empf.",v.rec.K,"| alt beste",r.pvAlt.best.K,"+",r.pvAlt.best.bestCap,"|",Date.now()-t,"ms");return r;}
pvrun("Dach max 15, EEG heute",{roofs:[{kwp:9,tilt:35,aspect:0,max:15}]});
pvrun("Dach max 15, Reform",{roofs:[{kwp:9,tilt:35,aspect:0,max:15}],eeg:"reform",feed:0,feedLimit:0.5});
pvrun("ohne Max, EEG heute");
pvrun("Ost-West max 8+8",{roofs:[{kwp:5,tilt:30,aspect:-90,max:8},{kwp:5,tilt:30,aspect:90,max:8}],total:21000});
assert(Math.abs(P.tariff({feed:7.7},12)-7.527)<0.01,"Mischsatz 12 kWp");
var rr=P.check(Object.assign({},base,{region:A}));assert(rr.pvSize.offer.bestCap===rr.best.cap||rr.best.cap>15,"Speicher im Raster = Speicher-Optimum");
console.log("PV OK");
