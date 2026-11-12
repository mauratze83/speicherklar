(function(){
  var nf0=new Intl.NumberFormat("de-DE",{maximumFractionDigits:0});
  var nf1=new Intl.NumberFormat("de-DE",{minimumFractionDigits:1,maximumFractionDigits:1});
  var nf2=new Intl.NumberFormat("de-DE",{minimumFractionDigits:2,maximumFractionDigits:2});
  var $=function(id){return document.getElementById(id);};
  var state={aspect:"0",evTime:"eve",eeg:"now",region:"4"};
  var ASPECT_NAME={"0":"Süd","-45":"Südost","45":"Südwest","ow":"Ost-West","-90":"Ost","90":"West"};

  function seg(id,key,after){
    var btns=document.querySelectorAll("#"+id+" button");
    Array.prototype.forEach.call(btns,function(btn){
      btn.addEventListener("click",function(){
        state[key]=btn.getAttribute("data-v");
        Array.prototype.forEach.call(btns,function(b){b.setAttribute("aria-pressed",String(b===btn));});
        if(after)after();
        render();
      });
    });
  }

  function regionFromPlz(){
    var v=$("plz").value.replace(/\D/g,"");
    if(v.length===5&&REGIONS[v[0]]){state.region=v[0];return true;}
    return false;
  }

  function roofs(){
    var kwp=+$("pv").value,tilt=+$("tilt").value;
    if(state.aspect==="ow")return [{kwp:kwp/2,tilt:tilt,aspect:-90},{kwp:kwp/2,tilt:tilt,aspect:90}];
    return [{kwp:kwp,tilt:tilt,aspect:+state.aspect}];
  }

  function read(){
    return {region:state.region,roofs:roofs(),cons:+$("cons").value,ev:+$("ev").value,evTime:state.evTime,
      bat:+$("bat").value,bprice:+$("bprice").value,life:+$("life").value,price:+$("price").value,
      feed:+$("feed").value,feedLimit:state.eeg==="reform"?0.5:0};
  }

  function outputs(p,plzOk){
    $("o-plz").textContent=plzOk?REGIONS[p.region].n:"5-stellige PLZ eingeben";
    $("o-plz").className=plzOk?"":"warn";
    $("o-tilt").textContent=$("tilt").value+"°";
    $("o-pv").textContent=nf1.format(+$("pv").value)+" kWp";
    $("o-cons").textContent=nf0.format(p.cons)+" kWh";
    $("o-ev").textContent=p.ev?nf0.format(p.ev)+" kWh":"kein E-Auto";
    $("o-bat").textContent=p.bat+" kWh";
    $("o-bprice").textContent=nf0.format(p.bprice)+" €/kWh";
    $("o-life").textContent=p.life+" Jahre";
    $("o-price").textContent=nf2.format(p.price)+" ct/kWh";
    $("o-feed").textContent=nf2.format(p.feed)+" ct/kWh";
    $("h-eeg").textContent=state.eeg==="reform"
      ?"Kabinettsentwurf: keine feste Vergütung nach der Übergangszeit, Einspeisung höchstens 50 % der Anlagenleistung. Noch nicht beschlossen."
      :"Gilt 20 Jahre ab Inbetriebnahme, für Anlagen ab August 2026 bis 10 kWp.";
  }

  // Zählerrollen: einmal aufbauen, danach nur die Ziffernstreifen verschieben
  var WHEELS=5,strips=[];
  (function buildWheels(){
    var el=$("wheels"),html="";
    for(var i=0;i<WHEELS;i++){
      html+='<span class="wheel" aria-hidden="true"><span class="strip">';
      for(var d=0;d<10;d++)html+="<span>"+d+"</span>";
      html+="</span></span>";
    }
    el.innerHTML=html+'<span class="unit">kWh / Jahr</span>';
    strips=el.querySelectorAll(".strip");
  })();
  // Die Rollen drehen erst, wenn der Zähler zu sehen ist (auf dem Handy liegt er weit unten)
  var wheelsSeen=!("IntersectionObserver" in window),wheelsVal=null;
  if(!wheelsSeen){
    try{
      var wio=new IntersectionObserver(function(es){if(!es[0].isIntersecting)return;wio.disconnect();wheelsSeen=true;
        var w=$("wheels");w.classList.add("roll");if(wheelsVal!==null)wheels(wheelsVal);setTimeout(function(){w.classList.remove("roll");},1400);},{threshold:0.6});
      wio.observe($("wheels"));
    }catch(e){wheelsSeen=true;}
  }
  function wheels(n){
    if(!wheelsSeen){wheelsVal=n;$("wheels").setAttribute("aria-label",nf0.format(n)+" Kilowattstunden pro Jahr");return;}
    var s=String(Math.min(99999,Math.max(0,Math.round(n)))).padStart(WHEELS,"0");
    for(var i=0;i<WHEELS;i++)strips[i].style.transform="translateY("+(-(+s[i])*10)+"%)";
    $("wheels").setAttribute("aria-label",nf0.format(n)+" Kilowattstunden pro Jahr");
  }

  function euro(v){return (v<0?"−":"")+nf0.format(Math.abs(v))+" €";}

  function chart(res,p){
    var W=560,H=210,pl=50,pr=8,pt=20,pb=28,iw=W-pl-pr,ih=H-pt-pb;
    var vals=res.sweep.map(function(s){return s.net;});
    var max=Math.max(0,Math.max.apply(null,vals)),min=Math.min(0,Math.min.apply(null,vals));
    var span=max-min||1;
    var step=Math.pow(10,Math.floor(Math.log10(span/4)));[1,2,2.5,5,10].some(function(m){if(span/(step*m)<=5){step*=m;return true;}return false;});
    var top=Math.ceil(max/step)*step,bot=Math.floor(min/step)*step;if(top===bot)top=bot+step;
    var y=function(v){return pt+(top-v)/(top-bot)*ih;};
    var bw=iw/15,svg="";
    for(var t=bot;t<=top+1e-9;t+=step){
      svg+='<line x1="'+pl+'" x2="'+(W-pr)+'" y1="'+y(t)+'" y2="'+y(t)+'" stroke="var(--line)" stroke-width="1"'+(Math.abs(t)<1e-9?'':' stroke-dasharray="2 3"')+'/>';
      svg+='<text x="'+(pl-6)+'" y="'+(y(t)+4)+'" text-anchor="end">'+(t<0?"−":"")+nf0.format(Math.abs(t))+'</text>';
    }
    res.sweep.forEach(function(s,i){
      var x=pl+i*bw+bw*0.18,w=bw*0.64,y0=y(0),y1=y(s.net);
      var isBest=s.cap===res.best.cap&&res.best.net>0;
      var col=s.net<0?"var(--neg)":isBest?"var(--sun)":"var(--c-imp)",hgt=Math.max(1,Math.abs(y1-y0));
      svg+='<rect x="'+x+'" y="'+Math.min(y0,y1)+'" width="'+w+'" height="'+hgt+'" fill="'+col+'" rx="2"'+(s.net<0?' opacity="0.75"':'')+'/>';
      if(isBest)svg+='<text class="best" x="'+Math.min(W-pr-30,Math.max(pl+30,x+w/2))+'" y="'+Math.max(10,y1-(s.cap===p.bat?8:5))+'" text-anchor="middle">+'+nf0.format(s.net)+' €</text>';
      if(s.cap===p.bat)svg+='<rect x="'+(x-3)+'" y="'+(Math.min(y0,y1)-3)+'" width="'+(w+6)+'" height="'+(hgt+6)+'" fill="none" stroke="var(--ink)" stroke-width="1.5" rx="3"/>';
      svg+='<text x="'+(x+w/2)+'" y="'+(H-10)+'" text-anchor="middle">'+s.cap+'</text>';
    });
    svg+='<text x="'+(W-pr)+'" y="'+(H-0.5)+'" text-anchor="end">kWh</text>';
    svg+='<text x="4" y="'+(pt-2)+'">€</text>';
    $("chart").innerHTML=svg;
  }


  // ---------- Tageskurve ----------
  // Kubische Bézierkurve wie --ease-out in CSS: cubic-bezier(0.23, 1, 0.32, 1)
  function bezier(x1,y1,x2,y2){return function(t){var lo=0,hi=1,m=t;for(var i=0;i<24;i++){m=(lo+hi)/2;var x=3*(1-m)*(1-m)*m*x1+3*(1-m)*m*m*x2+m*m*m;if(x<t)lo=m;else hi=m;}return 3*(1-m)*(1-m)*m*y1+3*(1-m)*m*m*y2+m*m*m;};}
  var EASE=bezier(0.23,1,0.32,1);
  var REDUCE=false;try{REDUCE=window.matchMedia("(prefers-reduced-motion: reduce)").matches;}catch(e){}
  var MONTH_NAME=["Januar","Februar","März","April","Mai","Juni","Juli","August","September","Oktober","November","Dezember"];
  var DAYBOX={l:40,t:22,w:500,h:190},DAYH=250,dayState={month:5,days:null,shown:null,anim:0,built:"",paths:null,line:null};
  $("daylegend").innerHTML=DRAW.legend();
  var rz=0;window.addEventListener("resize",function(){cancelAnimationFrame(rz);rz=requestAnimationFrame(function(){if(dayState.shown)dayFrame(dayState.shown);});});

  function dayTarget(){
    var d=dayState.days,st=DRAW.stack(d[dayState.month]);
    var ym=Math.max(DRAW.stack(d[5]).max,DRAW.stack(d[11]).max),step=DRAW.niceStep(ym,4);
    st.ymax=Math.ceil(ym/step)*step;return st;
  }
  function dayFrame(st){
    var svg=$("daychart"),W=Math.max(280,Math.round(svg.getBoundingClientRect().width||560));
    DAYBOX.w=W-DAYBOX.l-14;DAYBOX.h=W<480?170:190;svg.setAttribute("viewBox","0 0 "+W+" "+(DAYBOX.h+DAYBOX.t+30));
    var g=DRAW.dayGeometry(st,DAYBOX,st.ymax),key=W+"|"+st.ymax;
    if(dayState.built!==key){
      var s=DRAW.dayAxes(DAYBOX,st.ymax,g.x,g.y);
      g.areas.forEach(function(d,i){s+='<path class="area '+DRAW.LAYERS[i].cls+'" d="'+d+'"/>';});
      svg.innerHTML=s+'<path class="lline" d="'+g.load+'"/>';
      dayState.built=key;dayState.paths=svg.querySelectorAll("path.area");dayState.line=svg.querySelector("path.lline");
    }else{
      // Während der Überblendung nur die Flächen und die Lastlinie neu setzen, Achsen bleiben stehen
      g.areas.forEach(function(d,i){dayState.paths[i].setAttribute("d",d);});
      dayState.line.setAttribute("d",g.load);
    }
  }
  function lerpStack(a,b,t){
    var L=function(x,y){var o=[];for(var i=0;i<24;i++)o.push(x[i]+(y[i]-x[i])*t);return o;};
    return {layers:a.layers.map(function(la,i){return {bottom:L(la.bottom,b.layers[i].bottom),top:L(la.top,b.layers[i].top)};}),load:L(a.load,b.load),ymax:a.ymax+(b.ymax-a.ymax)*t};
  }
  function drawDay(){
    var target=dayTarget(),from=dayState.shown;
    cancelAnimationFrame(dayState.anim);
    if(!from||REDUCE){dayState.shown=target;dayFrame(target);}
    else{
      var t0=performance.now(),D=240;
      var step=function(now){var k=Math.min(1,(now-t0)/D),cur=lerpStack(from,target,EASE(k));dayState.shown=cur;dayFrame(cur);if(k<1)dayState.anim=requestAnimationFrame(step);};
      dayState.anim=requestAnimationFrame(step);
    }
    var m=dayState.days[dayState.month],sum=function(a){var s=0;for(var i=0;i<24;i++)s+=a[i];return s;};
    var imp=sum(m.imp),socMax=Math.max.apply(null,m.soc),full=-1;
    for(var h=0;h<24;h++)if(m.soc[h]>=0.95){full=h;break;}
    var name=MONTH_NAME[dayState.month];
    $("daysum").innerHTML=full>=0
      ?"Im "+name+" ist der Speicher im Schnitt gegen <b>"+(full+1)+" Uhr voll</b> und versorgt das Haus abends. Aus dem Netz kommen nur <b>"+nf1.format(imp)+" kWh am Tag</b>."
      :"Im "+name+" wird der Speicher im Schnitt nur zu <b>"+Math.round(socMax*100)+" % voll</b>. Aus dem Netz kommen <b>"+nf1.format(imp)+" kWh am Tag</b>, ein größerer Speicher ändert daran wenig.";
  }

  function render(){
    var plzOk=regionFromPlz();
    var p=read();outputs(p,plzOk);
    var res=evaluate(p),c=res.chosen,b=res.base;
    $("yield").textContent="Deine Anlage erzeugt rund "+nf0.format(Math.round(b.gen/10)*10)+" kWh im Jahr ("+nf0.format(b.gen/res.kwp)+" kWh je kWp, "+ASPECT_NAME[state.aspect]+", "+$("tilt").value+"°)."
      +(b.curt>20?" Durch die 50-%-Grenze gehen ohne Speicher etwa "+nf0.format(b.curt)+" kWh verloren.":"");
    wheels(c.extraSelf);
    $("meterfoot").textContent=p.feed>0
      ?"Solarstrom, der sonst für "+nf2.format(p.feed)+" ct ins Netz gegangen wäre und jetzt "+nf2.format(p.price)+" ct Netzstrom ersetzt."
      :"Solarstrom, der ohne Speicher unvergütet ins Netz gegangen wäre und jetzt "+nf2.format(p.price)+" ct Netzstrom ersetzt.";
    $("k-save").textContent=euro(c.save);
    $("k-pay").textContent=isFinite(c.payback)?nf1.format(c.payback)+" J.":"nie";
    $("k-cost").textContent="bei "+euro(c.cost)+" Anschaffung";
    $("k-net").textContent=(c.net>=0?"+":"")+euro(c.net);
    $("k-net").style.color=c.net>=0?"var(--pos)":"var(--neg)";
    $("k-netd").textContent="nach "+p.life+" Jahren";
    $("b-aut").textContent=Math.round(b.autarky*100)+" % → "+Math.round(c.r.autarky*100)+" %";
    $("b-ev").textContent=Math.round(b.selfRate*100)+" % → "+Math.round(c.r.selfRate*100)+" %";
    $("t-aut0").style.transform="scaleX("+b.autarky+")";$("t-aut1").style.transform="scaleX("+c.r.autarky+")";
    $("t-ev0").style.transform="scaleX("+b.selfRate+")";$("t-ev1").style.transform="scaleX("+c.r.selfRate+")";
    var v;
    if(c.net>=0)v='Mit '+p.bat+' kWh <span class="ok">rechnet sich der Speicher nach etwa '+nf1.format(c.payback)+' Jahren.</span>';
    else v='Mit '+p.bat+' kWh <span class="no">holt der Speicher seine Kosten in '+p.life+' Jahren nicht rein.</span>';
    if(res.best.cap!==p.bat)v+=res.best.net>0?' Am meisten bleibt bei '+res.best.cap+' kWh übrig.':' Bei diesen Preisen rechnet sich keine Größe.';
    else if(res.best.net>0)v+=' Das ist auch die wirtschaftlichste Größe.';
    $("verdict").innerHTML=v;
    $("sweepsum").innerHTML=res.best.net>0?"Mit deinen Werten bleibt am meisten bei <b>"+res.best.cap+"&nbsp;kWh</b>: +"+euro(res.best.net).replace(" €","&nbsp;€")+" nach "+p.life+" Jahren, bezahlt nach "+nf1.format(res.best.payback)+" Jahren.":"Mit deinen Werten rechnet sich keine Speichergröße.";
    chart(res,p);
    var okNet=c.net>=0&&isFinite(c.payback);
    $("rbar-main").textContent=p.bat+" kWh · "+(okNet?"bezahlt nach "+nf1.format(c.payback)+" J.":"rechnet sich nicht");
    $("rbar-sub").innerHTML=(c.net>=0?"+":"")+euro(c.net)+" nach "+p.life+" Jahren"+(res.best.net>0?" · <i>"+(res.best.cap===p.bat?"wirtschaftlichste Größe":"am meisten bleibt bei "+res.best.cap+" kWh")+"</i>":"");
    dayState.days=daySeries(res.gen,res.load,p.bat,res.fc);drawDay();
    // Übergabe an den Angebots-Check im Hash (wird nicht an einen Server gesendet)
    var q={plz:$("plz").value.replace(/\D/g,""),kwp:$("pv").value,aspect:state.aspect,tilt:$("tilt").value,cons:p.cons,ev:p.ev,evt:p.evTime,bat:p.bat,price:p.price,eeg:state.eeg,feed:p.feed,life:p.life};
    $("to-pro").href="pro/#"+Object.keys(q).map(function(k){return k+"="+encodeURIComponent(q[k]);}).join("&");
  }

  seg("aspect","aspect");
  seg("evtime","evTime");
  Array.prototype.forEach.call(document.querySelectorAll("#daymonth button"),function(btn){btn.addEventListener("click",function(){dayState.month=+btn.getAttribute("data-v");Array.prototype.forEach.call(document.querySelectorAll("#daymonth button"),function(x){x.setAttribute("aria-pressed",String(x===btn));});drawDay();});});
  seg("eeg","eeg",function(){
    if(state.eeg==="reform"){state.prevFeed=$("feed").value;$("feed").value=0;}
    else $("feed").value=state.prevFeed&&+state.prevFeed>0?state.prevFeed:7.7;
  });

  // Zählung ohne Cookies (Umami), nur wenn das Skript geladen ist; keine Eingabewerte
  function track(n){try{if(window.umami)window.umami.track(n);}catch(e){}}
  $("to-pro").addEventListener("click",function(){track("rechner-zu-pro");});
  var used=false;function markUsed(){if(!used){used=true;track("rechner-genutzt");}}
  $("inputs").addEventListener("change",markUsed);
  Array.prototype.forEach.call(document.querySelectorAll("#inputs .seg button"),function(b){b.addEventListener("click",markUsed);});

  // Tasten − und + neben dem Regler für die Speichergröße
  function stepBat(d){var el=$("bat"),v=Math.max(+el.min,Math.min(+el.max,+el.value+d));if(v===+el.value)return;el.value=v;
    el.dispatchEvent(new Event("input",{bubbles:true}));el.dispatchEvent(new Event("change",{bubbles:true}));}
  $("bat-minus").addEventListener("click",function(){stepBat(-1);});
  $("bat-plus").addEventListener("click",function(){stepBat(1);});

  // Ergebnisleiste am Handy: sichtbar, solange die Eingaben im Bild sind und das Ergebnis nicht
  (function(){
    var bar=$("rbar");if(!bar||!("IntersectionObserver" in window))return;
    var inForm=false,inRes=false;
    function upd(){var on=inForm&&!inRes;bar.classList.toggle("show",on);bar.setAttribute("aria-hidden",String(!on));bar.tabIndex=on?0:-1;}
    try{
      new IntersectionObserver(function(es){inForm=es[0].isIntersecting;upd();},{rootMargin:"-30% 0px -30% 0px"}).observe($("inputs"));
      new IntersectionObserver(function(es){inRes=es[0].isIntersecting;upd();},{rootMargin:"0px 0px -120px 0px"}).observe($("ergebnis"));
    }catch(e){}
  })();

  var pending=null;
  $("inputs").addEventListener("input",function(){if(pending)cancelAnimationFrame(pending);pending=requestAnimationFrame(render);});
  $("inputs").addEventListener("submit",function(e){e.preventDefault();});
  render();

  // ---------- Hausgrafik im Seitenkopf ----------
  (function(){
    var fig=$("scene");if(!fig)return;
    var p0=read(),days=dayProfile(p0,p0.bat),IDX={jul:6,nov:10};
    var sum=function(a){var s=0;for(var i=0;i<24;i++)s+=a[i];return s;};
    var data={};Object.keys(IDX).forEach(function(k){var m=days[IDX[k]];data[k]={gen:sum(m.gen),load:sum(m.load),imp:sum(m.imp),direct:sum(m.direct),charge:sum(m.charge),dis:sum(m.discharge),exp:sum(m.exp)};});
    var SUN={jul:[150,58],nov:[62,226]};
    var sunEl=fig.querySelector(".sun"),flows={direct:"f-direct",charge:"f-charge",dis:"f-dis",imp:"f-imp",exp:"f-exp"};
    var width=function(v){return v<0.05?0:Math.min(16,1.5+v*0.45);};
    var dots=[];
    function runDots(){
      if(REDUCE||!fig.animate)return;
      dots.forEach(function(el){el.remove();});dots=[];
      Object.keys(flows).forEach(function(k){
        var base=$(flows[k]);if(!base||parseFloat(base.style.strokeWidth)<1)return;
        var d=base.cloneNode();d.removeAttribute("id");d.setAttribute("class","flow dots");d.removeAttribute("style");d.removeAttribute("stroke-width");base.parentNode.appendChild(d);dots.push(d);
        var an=d.animate([{strokeDashoffset:30},{strokeDashoffset:0}],{duration:900,iterations:4,easing:"linear"});
        an.onfinish=function(){d.remove();};
      });
    }
    function show(season,animate){
      var v=data[season];fig.setAttribute("data-season",season);
      sunEl.style.transform="translate("+SUN[season][0]+"px,"+SUN[season][1]+"px)";
      Object.keys(flows).forEach(function(k){var el=$(flows[k]),w=width(v[k]);el.style.strokeWidth=w.toFixed(1)+"px";el.style.opacity=w?1:0;});
      $("sc-gen").textContent=nf1.format(v.gen);$("sc-load").textContent=nf1.format(v.load);$("sc-imp").textContent=nf1.format(v.imp);
      Array.prototype.forEach.call(document.querySelectorAll("#season button"),function(b){b.setAttribute("aria-pressed",String(b.getAttribute("data-v")===season));});
      if(animate)setTimeout(runDots,450);
    }
    $("sc-note").textContent="kWh pro Tag. Beispiel: "+nf1.format(p0.roofs.reduce(function(s,r){return s+r.kwp;},0))+" kWp Süd, "+nf0.format(p0.cons)+" kWh im Jahr, "+p0.bat+" kWh Speicher, "+REGIONS[p0.region].n.split(",")[0]+".";
    var touched=false;
    Array.prototype.forEach.call(document.querySelectorAll("#season button"),function(b){b.addEventListener("click",function(){touched=true;show(b.getAttribute("data-v"),true);});});
    // Startbild Juli; einmal nach dem Laden wechselt die Szene in den November, die Kernaussage der Seite
    fig.classList.add("no-trans");show("jul",false);void fig.offsetWidth;fig.classList.remove("no-trans");
    if(REDUCE){show("nov",false);return;}
    // Einblenden und Wechsel in den November erst, wenn die Grafik im Bild ist (auf dem Handy liegt sie unter dem Text)
    function start(){fig.classList.remove("wait");setTimeout(function(){if(!touched)show("nov",true);},1600);}
    if("IntersectionObserver" in window){
      try{
        fig.classList.add("wait");
        var sio=new IntersectionObserver(function(es){if(es[0].isIntersecting){sio.disconnect();start();}},{threshold:0.5});
        sio.observe(fig);
      }catch(e){start();}
    }else start();
  })();

  // Bereiche weiter unten einmal einblenden
  try{
    if("IntersectionObserver" in window){
      document.documentElement.classList.add("js");
      var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add("in");io.unobserve(e.target);}});},{rootMargin:"0px 0px -80px 0px"});
      Array.prototype.forEach.call(document.querySelectorAll(".reveal"),function(el){io.observe(el);});
    }
  }catch(e){}
})();

/* Pro-Box: Preis und Kauf nach Datum (Werte kommen beim Bauen aus src/pro-config.js) */
(function(){
  var b=document.getElementById("pricebox");if(!b)return;
  var today=new Date().toISOString().slice(0,10),pub=b.getAttribute("data-public"),intro=b.getAttribute("data-intro");
  if(intro&&today>intro){document.getElementById("pro-price").innerHTML=b.getAttribute("data-regular")+" € <small>einmalig</small>";document.getElementById("pro-intro").hidden=true;}
  if(pub&&today>=pub){document.getElementById("pro-buy").hidden=false;document.getElementById("pro-tag").textContent="Speicherklar Pro";}
})();
