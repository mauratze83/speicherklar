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
      html+='<span class="wheel'+(i===WHEELS-1?' red':'')+'" aria-hidden="true"><span class="strip">';
      for(var d=0;d<10;d++)html+="<span>"+d+"</span>";
      html+="</span></span>";
    }
    el.innerHTML=html+'<span class="unit">kWh / Jahr</span>';
    strips=el.querySelectorAll(".strip");
  })();
  function wheels(n){
    var s=String(Math.min(99999,Math.max(0,Math.round(n)))).padStart(WHEELS,"0");
    for(var i=0;i<WHEELS;i++)strips[i].style.transform="translateY("+(-(+s[i])*10)+"%)";
    $("wheels").setAttribute("aria-label",nf0.format(n)+" Kilowattstunden pro Jahr");
  }

  function euro(v){return (v<0?"−":"")+nf0.format(Math.abs(v))+" €";}

  function chart(res,p){
    var W=560,H=210,pl=50,pr=8,pt=12,pb=28,iw=W-pl-pr,ih=H-pt-pb;
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
      var col=s.net>=0?"var(--pos)":"var(--neg)",hgt=Math.max(1,Math.abs(y1-y0));
      svg+='<rect x="'+x+'" y="'+Math.min(y0,y1)+'" width="'+w+'" height="'+hgt+'" fill="'+col+'" rx="2" opacity="'+(s.cap===p.bat?1:0.55)+'"/>';
      if(s.cap===p.bat)svg+='<rect x="'+(x-3)+'" y="'+(Math.min(y0,y1)-3)+'" width="'+(w+6)+'" height="'+(hgt+6)+'" fill="none" stroke="var(--ink)" stroke-width="1.5" rx="3"/>';
      svg+='<text x="'+(x+w/2)+'" y="'+(H-10)+'" text-anchor="middle">'+s.cap+'</text>';
    });
    svg+='<text x="'+(W-pr)+'" y="'+(H-0.5)+'" text-anchor="end">kWh</text>';
    svg+='<text x="4" y="'+(pt-2)+'">€</text>';
    $("chart").innerHTML=svg;
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
    chart(res,p);
  }

  seg("aspect","aspect");
  seg("evtime","evTime");
  seg("eeg","eeg",function(){
    if(state.eeg==="reform"){state.prevFeed=$("feed").value;$("feed").value=0;}
    else $("feed").value=state.prevFeed&&+state.prevFeed>0?state.prevFeed:7.7;
  });

  var pending=null;
  $("inputs").addEventListener("input",function(){if(pending)cancelAnimationFrame(pending);pending=requestAnimationFrame(render);});
  $("inputs").addEventListener("submit",function(e){e.preventDefault();});
  render();

  // Bereiche weiter unten einmal einblenden
  try{
    if("IntersectionObserver" in window){
      document.documentElement.classList.add("js");
      var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add("in");io.unobserve(e.target);}});},{rootMargin:"0px 0px -80px 0px"});
      Array.prototype.forEach.call(document.querySelectorAll(".reveal"),function(el){io.observe(el);});
    }
  }catch(e){}
})();
