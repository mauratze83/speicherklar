// Aktualisiert die preisabhängigen Felder in numbers.json. Aufruf: node gen/update.js <ct> [--check]
var fs=require("fs"),path=require("path");
var S=require(path.resolve(process.env.SPEICHERKLAR_SITE||path.join(__dirname,"../../speicherklar-site"),"src/sim.js"));
var price=+process.argv[2],check=process.argv.includes("--check");
var D=JSON.parse(fs.readFileSync(__dirname+"/../numbers.json","utf8"));
function P(o){var p={region:"4",roofs:[{kwp:9,tilt:35,aspect:0}],cons:4500,ev:0,evTime:"eve",bat:8,bprice:500,life:15,price:price,feed:7.7,feedLimit:0};for(var k in o)p[k]=o[k];return p;}
var OW=[{kwp:4.5,tilt:35,aspect:-90},{kwp:4.5,tilt:35,aspect:90}];
var V={sued_heute:P({}),sued_reform:P({feed:0,feedLimit:0.5}),ow_heute:P({roofs:OW}),ow_reform:P({roofs:OW,feed:0,feedLimit:0.5}),
  sued_6kWp:P({roofs:[{kwp:6,tilt:35,aspect:0}]}),sued_12kWp:P({roofs:[{kwp:12,tilt:35,aspect:0}]})};
var r1=function(v){return Math.round(v*10)/10;},diff=0;
Object.keys(V).forEach(function(k){
  var p=V[k],e=S.evaluate(p),aut=function(r){return Math.round((1-r.grid/p.cons)*100);};
  var row=function(s){return [s.cap,Math.round(s.save),r1(s.payback),Math.round(s.net),aut(s.r)];};
  var n={best:e.best.cap,bestNet:Math.round(e.best.net),bestPay:r1(e.best.payback),bestSave:Math.round(e.best.save),
    s8:{save:Math.round(e.sweep[7].save),pay:r1(e.sweep[7].payback),net:Math.round(e.sweep[7].net),aut:aut(e.sweep[7].r)},sweep:e.sweep.map(row)};
  var o=D[k];
  ["best","bestNet","bestPay","bestSave"].forEach(function(f){if(o[f]!==n[f]){diff++;if(check)console.log(k,f,o[f],n[f]);}});
  ["save","pay","net"].forEach(function(f){if(o.s8[f]!==n.s8[f]){diff++;if(check)console.log(k,"s8."+f,o.s8[f],n.s8[f]);}});
  n.sweep.forEach(function(r,i){[1,2,3].forEach(function(j){if(o.sweep[i][j]!==r[j]){diff++;if(check)console.log(k,"sweep",i+1,j,o.sweep[i][j],r[j]);}});});
  if(!check){o.best=n.best;o.bestNet=n.bestNet;o.bestPay=n.bestPay;o.bestSave=n.bestSave;["save","pay","net"].forEach(function(f){o.s8[f]=n.s8[f];});
    o.sweep.forEach(function(r,i){r[1]=n.sweep[i][1];r[2]=n.sweep[i][2];r[3]=n.sweep[i][3];});}
});
if(check)console.log("Abweichungen:",diff);
else{D.price=price;fs.writeFileSync(__dirname+"/../numbers.json",JSON.stringify(D));console.log("ok",price);}
