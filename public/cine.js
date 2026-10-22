/* Scroll-driven cinematic hero + horizontal install reel */
(function(){
'use strict';
var d=document,w=window;
var reduce=w.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
function clamp(v,a,b){return Math.max(a,Math.min(b,v));}
function lerp(a,b,t){return a+(b-a)*t;}
function sm(e0,e1,x){var t=clamp((x-e0)/(e1-e0),0,1);return t*t*(3-2*t);}
function fmt(t){var h=Math.floor(t),m=Math.floor((t-h)*60/5)*5;var ap=h>=12?'pm':'am';return (h%12||12)+':'+(m<10?'0':'')+m+' '+ap;}

/* ---------- Cinematic hero ---------- */
var cine=d.querySelector('.cine');
if(cine&&!reduce){
  cine.classList.add('live');
  var pin=cine.querySelector('.cine-pin'),A=cine.querySelector('.cine-a'),Aimg=A.querySelector('img'),B=cine.querySelector('.cine-b'),cv=cine.querySelector('.cine-canvas');
  var fabs=cine.querySelectorAll('.cine-fab'),tints=cine.querySelectorAll('.cine-tint'),room=cine.querySelector('.cine-room'),lamps=cine.querySelector('.cine-lamps'),glare=cine.querySelector('.cine-glare');
  var veil=cine.querySelector('.cine-veil'),chip=cine.querySelector('.cine-chip'),clock=chip.querySelector('b'),state=chip.querySelector('span');
  var T=[].slice.call(cine.querySelectorAll('.cine-t')),rail=cine.querySelector('.cine-rail i'),dots=cine.querySelectorAll('.cine-dots b'),cue=cine.querySelector('.cine-cue');
  var R=[[-1,-1,.14,.22],[.27,.33,.52,.58],[.6,.66,.78,.84],[.86,.92,2,3]];
  var mh=0;
  function layout(){
    var m=d.querySelector('.masthead');mh=m?m.offsetHeight:0;d.documentElement.style.setProperty('--mh',mh+'px');
    var W=pin.clientWidth,H=pin.clientHeight,s=Math.max(W/1300,H/735)*1.02,cw=1300*s,ch=735*s;
    var left=clamp(W/2-.516*cw,W-cw,0),top=clamp(H*.46-.36*ch,H-ch,0);
    cv.style.width=cw+'px';cv.style.height=ch+'px';cv.style.left=left+'px';cv.style.top=top+'px';
  }
  var last=-1,ticking=false;
  function frame(){
    ticking=false;
    var r=cine.getBoundingClientRect(),span=cine.offsetHeight-pin.offsetHeight,p=clamp(-r.top/(span||1),0,1);
    if(Math.abs(p-last)<.0005)return;last=p;
    // layer A: arched room, slow push-in, then dissolve
    var a=1-sm(.17,.3,p);A.style.opacity=a;Aimg.style.transform='scale('+(1+.12*sm(0,.3,p)).toFixed(4)+')';
    // layer B: bedroom, shades lower and the day turns to night
    var b=sm(.17,.3,p);B.style.opacity=b;B.style.transform='scale('+(1.06-.06*sm(.17,.4,p)+.05*sm(.86,1,p)).toFixed(4)+')';
    var cov=sm(.33,.66,p),t=lerp(13.5,21.8,sm(.3,.84,p));
    var sun=sm(6,9,t)*(1-sm(15.5,20,t)),night=1-sm(5.5,7.5,t)*(1-sm(19.5,21.5,t)),gold=sm(16,18,t)*(1-sm(19.2,20.4,t));
    var pct=(cov*100).toFixed(2)+'%';for(var i=0;i<fabs.length;i++)fabs[i].style.height=pct;
    var gt='rgba(14,20,38,'+(night*.9).toFixed(3)+')';for(i=0;i<tints.length;i++)tints[i].style.background='linear-gradient('+gt+','+gt+'),rgba(255,160,80,'+(gold*.3).toFixed(3)+')';
    var day=sun*(1-cov),lampLvl=clamp((1-sun)*1.1,0,1),amb=Math.max(day,lampLvl*.32);
    room.style.opacity=(.82*Math.pow(1-amb,1.5)).toFixed(3);
    lamps.style.opacity=(lampLvl*(.6+.4*(1-day))).toFixed(3);
    glare.style.opacity=(sun*(1-cov)*.8).toFixed(3);
    chip.style.opacity=sm(.27,.33,p)*(1-sm(.84,.9,p));
    clock.textContent=fmt(t);
    state.textContent=cov<.02?'Shades open':cov>.98?'Shades closed':'Shades lowering '+Math.round(cov*100)+'%';
    // copy chapters
    T.forEach(function(el,k){var q=R[k],v=(q[0]<0?1:sm(q[0],q[1],p))*(1-sm(q[2],q[3],p));
      el.style.opacity=v.toFixed(3);var dir=(q[0]<0||p>=q[1])?-1:1;el.style.transform='translateY('+((1-v)*26*dir).toFixed(1)+'px)';
      el.style.visibility=v<.01?'hidden':'visible';el.classList.toggle('on',v>.5);});
    veil.style.opacity=(.55+.25*sm(.86,.95,p)).toFixed(3);
    rail.style.transform='scaleY('+p.toFixed(4)+')';
    var ch=p<.25?0:p<.59?1:p<.85?2:3;for(i=0;i<dots.length;i++)dots[i].classList.toggle('on',i===ch);
    if(cue)cue.style.opacity=(1-sm(.02,.08,p)).toFixed(3);
  }
  function req(){if(!ticking){ticking=true;requestAnimationFrame(frame);}}
  w.addEventListener('scroll',req,{passive:true});
  w.addEventListener('resize',function(){layout();last=-1;req();});
  layout();frame();
  // dots jump to chapter
  [].forEach.call(dots,function(dt,i){dt.addEventListener('click',function(){var span=cine.offsetHeight-pin.offsetHeight,top=cine.getBoundingClientRect().top+w.scrollY;w.scrollTo({top:top+span*[0,.42,.72,.95][i],behavior:'smooth'});});});
}

/* ---------- Install reel ---------- */
var reel=d.querySelector('.reel');
if(reel){
  var track=reel.querySelector('.reel-track'),rpin=reel.querySelector('.reel-pin'),bar=reel.querySelector('.reel-bar i');
  var vids=[].slice.call(reel.querySelectorAll('video'));
  var desktop=function(){return w.innerWidth>860&&!reduce;};
  function size(){
    if(desktop()){var extra=track.scrollWidth-rpin.clientWidth;reel.style.height=(rpin.offsetHeight+Math.max(0,extra))+'px';reel.classList.add('pinned');}
    else{reel.style.height='';reel.classList.remove('pinned');track.style.transform='';}
  }
  function move(){
    if(!desktop())return;
    var r=reel.getBoundingClientRect(),span=reel.offsetHeight-rpin.offsetHeight,p=clamp(-r.top/(span||1),0,1);
    var extra=track.scrollWidth-rpin.clientWidth;track.style.transform='translate3d('+(-extra*p).toFixed(1)+'px,0,0)';
    if(bar)bar.style.transform='scaleX('+p.toFixed(4)+')';
  }
  w.addEventListener('scroll',function(){requestAnimationFrame(move);},{passive:true});
  w.addEventListener('resize',function(){size();move();});
  w.addEventListener('load',function(){size();move();});
  size();move();
  if('IntersectionObserver' in w){
    var io=new IntersectionObserver(function(es){es.forEach(function(e){var v=e.target;
      if(e.isIntersecting&&e.intersectionRatio>.5){if(v.preload!=='auto')v.preload='auto';var pr=v.play();if(pr&&pr.catch)pr.catch(function(){});}
      else v.pause();});},{threshold:[0,.5,.8]});
    vids.forEach(function(v){io.observe(v);});
  }
  if(!desktop()&&track){track.addEventListener('scroll',function(){if(bar)bar.style.transform='scaleX('+(track.scrollLeft/Math.max(1,track.scrollWidth-track.clientWidth)).toFixed(4)+')';},{passive:true});}
}
})();
