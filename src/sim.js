/* Speicherklar Simulationskern – ohne DOM, im Browser und in Node lauffähig */
var REGIONS={"0":{n:"Sachsen, Thüringen-Ost, Sachsen-Anhalt-Süd",lat:51.2,lon:12.9,H:[22,44.7,84.9,133.1,168.5,180,175.4,150.9,104.5,60.7,31.1,20.3],Kd:[0.72,0.55,0.52,0.47,0.47,0.44,0.48,0.46,0.49,0.55,0.6,0.65]},
"1":{n:"Berlin, Brandenburg, Mecklenburg-Vorpommern",lat:52.8,lon:13.4,H:[19.7,40.8,79.8,127.6,164.5,175,167.2,146.4,101.4,53.3,24.4,15.6],Kd:[0.71,0.56,0.54,0.5,0.49,0.47,0.51,0.49,0.5,0.59,0.66,0.71]},
"2":{n:"Hamburg, Schleswig-Holstein, Bremen, Niedersachsen-Nord",lat:53.6,lon:9.6,H:[18.1,36.7,77.1,126.8,155.8,168.5,157,136.5,94.9,50.9,23,13.6],Kd:[0.7,0.57,0.55,0.47,0.5,0.47,0.54,0.51,0.52,0.59,0.66,0.71]},
"3":{n:"Hannover, Braunschweig, Magdeburg, Kassel",lat:52.0,lon:10.0,H:[20.2,40.1,81.7,127.9,159.9,171.5,161.3,143.6,99.7,54.6,26,16.3],Kd:[0.74,0.59,0.54,0.48,0.51,0.48,0.52,0.5,0.52,0.6,0.68,0.72]},
"4":{n:"Ruhrgebiet, Niederrhein, Münsterland, Westfalen",lat:51.6,lon:7.2,H:[22.4,42.8,83.5,125.7,158,167.7,161.6,139.5,99.6,55.9,30,17.6],Kd:[0.68,0.55,0.52,0.5,0.5,0.5,0.52,0.51,0.51,0.59,0.61,0.68]},
"5":{n:"Köln, Bonn, Aachen, Koblenz, Trier",lat:50.5,lon:7.0,H:[24.1,45.6,86.2,127.9,159.3,168.8,164.4,141.2,103.3,57.4,31.1,20.2],Kd:[0.71,0.56,0.53,0.5,0.51,0.49,0.52,0.52,0.51,0.6,0.63,0.68]},
"6":{n:"Rhein-Main, Pfalz, Saarland, Mannheim",lat:49.9,lon:8.4,H:[26.1,48.1,95.4,139.6,173.2,183.7,181.6,153.4,112.8,59.9,30,19.8],Kd:[0.67,0.53,0.47,0.44,0.45,0.43,0.44,0.45,0.45,0.59,0.67,0.72]},
"7":{n:"Stuttgart, Baden, Bodensee",lat:48.6,lon:9.0,H:[31.8,54,100.2,134.2,158.4,180.6,180.8,151.9,115,67.5,37.2,27.2],Kd:[0.65,0.5,0.46,0.46,0.5,0.43,0.44,0.45,0.45,0.54,0.59,0.6]},
"8":{n:"München, Augsburg, Allgäu, Oberbayern",lat:48.0,lon:11.2,H:[33.3,56.9,98.6,133.9,152,180.5,175,152.6,111.8,70,38,28.3],Kd:[0.61,0.48,0.47,0.46,0.49,0.43,0.42,0.42,0.45,0.51,0.59,0.59]},
"9":{n:"Nürnberg, Würzburg, Franken, Thüringen-Süd",lat:49.8,lon:11.0,H:[25,47.1,90.3,133.9,163.2,180.7,178.5,151.9,107.5,61.3,30.5,20.8],Kd:[0.71,0.55,0.49,0.47,0.49,0.45,0.46,0.47,0.49,0.57,0.64,0.69]}};

var MDAYS=[31,28,31,30,31,30,31,31,30,31,30,31];
var H0=[0.55,0.45,0.4,0.38,0.38,0.45,0.7,0.95,0.95,0.9,0.9,0.95,1.05,1.0,0.9,0.85,0.9,1.1,1.35,1.45,1.35,1.15,0.95,0.7];
var SIGMA=0.9, PR=0.789, ALBEDO=0.2, SUB=4, CIRC=0.75;
// Reflexionsverlust bei flachem Lichteinfall (Martin/Ruiz, a_r = 0.16)
function IAM(c){return (1-Math.exp(-c/0.16))/(1-Math.exp(-1/0.16));}
var D2R=Math.PI/180;

function rng(seed){return function(){seed|=0;seed=seed+0x6D2B79F5|0;var t=Math.imul(seed^seed>>>15,1|seed);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296;};}

// Tageswetter: je Monat auf Mittel 1 normiert, aufeinanderfolgende Tage korreliert
var WEATHER=(function(){var r=rng(20261108),out=[],z=0;function gauss(){return Math.sqrt(-2*Math.log(r()+1e-12))*Math.cos(2*Math.PI*r());}
  for(var m=0;m<12;m++){var arr=[],s=0;for(var d=0;d<MDAYS[m];d++){z=0.55*z+Math.sqrt(1-0.55*0.55)*gauss();var f=Math.min(2.6,Math.exp(SIGMA*z));arr.push(f);s+=f;}var mean=s/arr.length;for(var j=0;j<arr.length;j++)out.push(arr[j]/mean);}return out;})();

// Lastspitzen innerhalb der Stunde (5-Minuten-Schritte) und Tagesschwankung ±25 %
var STEPS=12;
var QW=(function(){var r=rng(4711),q=new Float64Array(8760*STEPS);for(var h=0;h<8760;h++){var w=[],s=0;for(var k=0;k<STEPS;k++){var v=0.12+6*Math.pow(r(),9);w.push(v);s+=v;}for(var k2=0;k2<STEPS;k2++)q[h*STEPS+k2]=w[k2]/s*STEPS;}return q;})();
var DAYLOAD=(function(){var r=rng(1337),a=[];for(var d=0;d<365;d++)a.push(0.75+0.5*r());var m=a.reduce(function(x,y){return x+y;},0)/365;return a.map(function(x){return x/m;});})();

/* Erzeugung: kWh je Stunde für eine Dachfläche. aspect: 0 = Süd, -90 = Ost, 90 = West */
function pvProfile(region,kwp,tilt,aspect){
  var R=REGIONS[region],phi=R.lat*D2R,out=new Float64Array(8760);
  var b=tilt*D2R,g=aspect*D2R;
  var nE=-Math.sin(b)*Math.sin(g),nN=-Math.sin(b)*Math.cos(g),nU=Math.cos(b);
  var skyF=(1+Math.cos(b))/2,gndF=ALBEDO*(1-Math.cos(b))/2;
  var n=0,idx=0;
  for(var m=0;m<12;m++){
    var Hday=R.H[m]/MDAYS[m];
    for(var d=0;d<MDAYS[m];d++,n++){
      var doy=n+1,f=WEATHER[n];
      var dec=23.45*D2R*Math.sin(2*Math.PI*(284+doy)/365);
      var B=2*Math.PI*(doy-81)/365,eot=9.87*Math.sin(2*B)-7.53*Math.cos(B)-1.5*Math.sin(B);
      var off=(doy>=87&&doy<300)?2:1;
      var kd=Math.min(1,Math.max(0.12,R.Kd[m]*(1.25-0.25*f)));
      var cz=[],ct=[],ia=[],sumW=0;
      for(var h=0;h<24;h++){
        var czs=0,cts=0,iamW=0;
        for(var s=0;s<SUB;s++){
          var t=h+(s+0.5)/SUB-off+R.lon/15+eot/60;
          var w=15*(t-12)*D2R;
          var cZ=Math.sin(phi)*Math.sin(dec)+Math.cos(phi)*Math.cos(dec)*Math.cos(w);
          if(cZ>0){
            var sE=-Math.cos(dec)*Math.sin(w),sN=Math.cos(phi)*Math.sin(dec)-Math.sin(phi)*Math.cos(dec)*Math.cos(w);
            var cth=Math.max(0,sE*nE+sN*nN+cZ*nU);
            czs+=cZ;cts+=cth;iamW+=cth*IAM(cth);
          }
        }
        cz.push(czs/SUB);ct.push(cts/SUB);sumW+=czs/SUB;
        ia.push(cts>0?iamW/cts:0);
      }
      var Hd=Hday*f;
      for(var h2=0;h2<24;h2++){
        var ghi=sumW>0?Hd*cz[h2]/sumW:0,beam=0,diff=ghi*kd;
        var bh=ghi*(1-kd);
        var circ=0;
        if(cz[h2]>0.06){beam=bh*ct[h2]/cz[h2]*ia[h2];var Ai=Math.min(0.6,(1-kd)*CIRC);circ=diff*Ai*ct[h2]/cz[h2]*ia[h2];diff*=1-Ai;}else diff+=bh;
        var gp=beam+circ+diff*skyF*0.95+ghi*gndF;
        out[idx++]=kwp*gp*PR;
      }
    }
  }
  return out;
}

/* Verbrauch: kWh je Stunde. monthly (optional, 12 Werte) ersetzt die Standard-Saisonkurve */
function loadProfile(cons,ev,evTime,monthly){
  var load=new Float64Array(8760),h0sum=H0.reduce(function(a,b){return a+b;},0);
  var evHours=evTime==="day"?[10,11,12,13,14,15]:[18,19,20,21,22],evDaily=(ev||0)/365;
  var mtot=[];
  if(monthly&&monthly.length===12){var ms=monthly.reduce(function(a,b){return a+b;},0);for(var i=0;i<12;i++)mtot.push(cons*monthly[i]/ms);}
  else{var seas=[],ss=0;for(var m=0;m<12;m++){var v=1+0.2*Math.cos(2*Math.PI*m/12);seas.push(v);ss+=v*MDAYS[m];}for(var m1=0;m1<12;m1++)mtot.push(cons*seas[m1]*MDAYS[m1]/ss);}
  var day=0,idx=0;
  for(var m2=0;m2<12;m2++){var dl=mtot[m2]/MDAYS[m2];
    for(var d=0;d<MDAYS[m2];d++,day++)for(var h=0;h<24;h++)
      load[idx++]=dl*DAYLOAD[day]*H0[h]/h0sum+(evHours.indexOf(h)>=0?evDaily/evHours.length:0);}
  return load;
}

/* Energiefluss mit Speicher. feedCap: max. Einspeiseleistung in kW (Infinity = keine Grenze) */
function runBattery(gen,load,cap,feedCap){
  var soc=0,eta=Math.sqrt(0.88),pmax=Math.min(cap*0.5,5)/STEPS,stby=cap>0?0.025/STEPS:0;
  var fcap=(feedCap||Infinity)/STEPS,feed=0,grid=0,curt=0,G=0,Ld=0;
  for(var i=0,n=8760*STEPS;i<n;i++){
    var h=(i/STEPS)|0,gq=gen[h]/STEPS,lq=load[h]*QW[i]/STEPS;
    var s=gq-lq-stby;G+=gq;Ld+=lq;
    if(s>=0){var c=cap>0?Math.min(s,pmax,(cap-soc)/eta):0;soc+=c*eta;var ex=s-c,fe=Math.min(ex,fcap);feed+=fe;curt+=ex-fe;}
    else{var need=-s,dis=cap>0?Math.min(need,pmax,soc*eta):0;soc-=dis/eta;grid+=need-dis;}
  }
  return {feed:feed,grid:grid,curt:curt,gen:G,load:Ld,autarky:1-grid/Ld,selfRate:G>0?(G-feed-curt)/G:0};
}

/* p: {region, roofs:[{kwp,tilt,aspect}], cons, ev, evTime, monthly, bat, bprice, life, price, feed, feedLimit} */
function evaluate(p){
  var gen=new Float64Array(8760),kwpTot=0;
  p.roofs.forEach(function(r){var g=pvProfile(p.region,r.kwp,r.tilt,r.aspect);for(var i=0;i<8760;i++)gen[i]+=g[i];kwpTot+=r.kwp;});
  var load=loadProfile(p.cons,p.ev,p.evTime,p.monthly);
  var fc=p.feedLimit?kwpTot*p.feedLimit:Infinity;
  var base=runBattery(gen,load,0,fc);
  function forCap(cap){
    var r=runBattery(gen,load,cap,fc);
    var save=(base.grid-r.grid)*p.price/100-(base.feed-r.feed)*p.feed/100;
    var cost=cap*p.bprice;
    return {cap:cap,r:r,save:save,cost:cost,payback:save>0?cost/save:Infinity,net:save*p.life-cost,extraSelf:base.grid-r.grid};
  }
  var sweep=[];for(var c=1;c<=15;c++)sweep.push(forCap(c));
  var best=sweep.reduce(function(a,b){return b.net>a.net?b:a;});
  return {gen:gen,kwp:kwpTot,base:base,chosen:sweep[p.bat-1],best:best,sweep:sweep,
    // Kosten der PV-Anlage ohne Speicher (Stromrechnung mit PV): für spätere Pro-Auswertung
    pvValue:(p.cons+(p.ev||0)-base.grid)*p.price/100+base.feed*p.feed/100};
}

if(typeof module!=="undefined")module.exports={REGIONS:REGIONS,pvProfile:pvProfile,loadProfile:loadProfile,runBattery:runBattery,evaluate:evaluate};
