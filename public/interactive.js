/* Central Ohio Window Guide — interactive modules
   [data-studio]  Light Studio: drag a shade, change fabric and time of day, play a smart-home day
   [data-rooms]   Which treatment fits your room
   [data-motor]   Motorize it, or keep it manual?
   .float-cta     Floating installer pill */
(function(){
'use strict';
var d=document;
var reduce=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
function el(tag,cls,html){var e=d.createElement(tag);if(cls)e.className=cls;if(html!=null)e.innerHTML=html;return e;}
function clamp(v,a,b){return Math.max(a,Math.min(b,v));}
function lerp(a,b,t){return a+(b-a)*t;}
function smooth(e0,e1,x){var t=clamp((x-e0)/(e1-e0),0,1);return t*t*(3-2*t);}
function track(name,p){try{if(window.gtag)gtag('event',name,p||{});}catch(e){}}

/* ================= LIGHT STUDIO ================= */
var PANES=[[430,577],[595,744],[761,907]],W=1300,H=735,TOP=111,BOT=393;
var FABRICS={
  sheer:{n:'Sheer',d:'Soft, filtered light with the view still there.',tr:.72,glare:.6,view:.75,pday:.3,pnight:.05},
  filter:{n:'Light-filtering',d:'Glows with daylight, hides the view, keeps daytime privacy.',tr:.42,glare:.32,view:.12,pday:.92,pnight:.72},
  solar:{n:'Solar 3%',d:'Cuts glare and heat while you keep the view outside.',tr:.24,glare:.12,view:.62,pday:.6,pnight:.08},
  blackout:{n:'Blackout',d:'Room-darkening for bedrooms, nurseries and media rooms.',tr:0,glare:0,view:0,pday:1,pnight:1}
};
var SCHEDULE=[[5,1,'Sleeping in the dark'],[6.75,0,'6:45 am  Shades rise slowly to wake you'],[13,.72,'1:00 pm  West sun: shades lower to cut glare'],[17.5,0,'5:30 pm  Golden hour: open for the view'],[20.5,1,'8:30 pm  Sunset: close for privacy']];
function fmtTime(t){var h=Math.floor(t),m=Math.round((t-h)*60/5)*5;if(m===60){h++;m=0;}var ap=h>=12&&h<24?'pm':'am',hh=h%12||12;return hh+':'+(m<10?'0':'')+m+' '+ap;}
function sunAt(t){return smooth(6,9,t)*(1-smooth(15.5,20,t)*.999);}
function goldAt(t){return smooth(16,18,t)*(1-smooth(19.2,20.4,t))+smooth(6,7,t)*(1-smooth(7.2,8.6,t))*.6;}
function nightAt(t){return 1-smooth(5.5,7.5,t)*(1-smooth(19.5,21.5,t));}
function schedTarget(t){var c=1,l=0;for(var i=0;i<SCHEDULE.length;i++){if(t>=SCHEDULE[i][0]){c=SCHEDULE[i][1];l=i;}}return[c,l];}

function Studio(root){
  var compact=root.hasAttribute('data-compact');
  var S={cov:.35,fab:'blackout',t:14,auto:false,touched:false};
  root.classList.add('studio');
  var scene=el('div','st-scene');scene.setAttribute('role','img');scene.setAttribute('aria-label','Bedroom with three motorized roller shades; the shade position, fabric and time of day are adjustable.');
  var img=el('img','st-img');img.src='/images/editorial/studio-bedroom-open.webp';img.alt='';img.width=W;img.height=H;img.loading='lazy';
  var cv=el('div','st-canvas');scene.appendChild(cv);cv.appendChild(img);
  var panes=[],tints=[],fabs=[];
  PANES.forEach(function(p){
    var pane=el('div','st-pane');pane.style.left=(p[0]/W*100)+'%';pane.style.width=((p[1]-p[0])/W*100)+'%';pane.style.top=(TOP/H*100)+'%';pane.style.height=((BOT-TOP)/H*100)+'%';
    var tint=el('div','st-tint'),fab=el('div','st-fabric'),hem=el('i','st-hem');fab.appendChild(hem);
    pane.appendChild(tint);pane.appendChild(fab);cv.appendChild(pane);panes.push(pane);tints.push(tint);fabs.push(fab);
  });
  var room=el('div','st-room'),glare=el('div','st-glare'),lamps=el('div','st-lamps'),grab=el('div','st-grab','<span>Drag</span>');
  cv.appendChild(room);cv.appendChild(glare);cv.appendChild(lamps);cv.appendChild(grab);
  grab.style.left=((PANES[1][0]+PANES[1][1])/2/W*100)+'%';
  var chip=el('div','st-chip','<b class="st-clock">2:00 pm</b><span class="st-day">Daylight 0%</span>');scene.appendChild(chip);
  var credit=el('p','st-credit','Photo: Norman Window Fashions, adapted for this demo');

  var panel=el('div','st-panel');
  var fabWrap=el('div','st-fabs');
  Object.keys(FABRICS).forEach(function(k){var b=el('button','st-fab'+(k===S.fab?' on':''),'<span class="sw sw-'+k+'"></span>'+FABRICS[k].n);b.type='button';b.dataset.f=k;fabWrap.appendChild(b);});
  var fabDesc=el('p','st-fdesc',FABRICS[S.fab].d);
  var covRow=el('label','st-row','<span>Shade position</span>');var cov=el('input');cov.type='range';cov.min=0;cov.max=100;cov.value=35;cov.setAttribute('aria-label','Shade position, percent lowered');covRow.appendChild(cov);
  var timeRow=el('label','st-row','<span>Time of day</span>');var tim=el('input');tim.type='range';tim.min=5;tim.max=23;tim.step=.05;tim.value=14;tim.setAttribute('aria-label','Time of day');timeRow.appendChild(tim);
  var meters=el('div','st-meters');
  var M={};[['glare','Glare'],['privacy','Privacy'],['view','View']].forEach(function(m){var r=el('div','st-meter','<span>'+m[1]+'</span><div class="bar"><i></i></div><b></b>');meters.appendChild(r);M[m[0]]=r;});
  var play=el('button','st-play','<span class="ic">&#9654;</span><span class="tx">Play a smart-home day</span>');play.type='button';
  var log=el('ol','st-log');SCHEDULE.forEach(function(s){log.appendChild(el('li','',s[2]));});

  var h=el('div','st-head');
  panel.appendChild(el('p','st-label','Fabric'));panel.appendChild(fabWrap);panel.appendChild(fabDesc);
  panel.appendChild(covRow);panel.appendChild(timeRow);panel.appendChild(meters);panel.appendChild(play);panel.appendChild(log);
  var stage=el('div','st-stage');stage.appendChild(scene);stage.appendChild(credit);
  root.appendChild(stage);root.appendChild(panel);

  function label(v,a,b){return v<a?'Low':v<b?'Medium':'High';}
  function render(){
    var f=FABRICS[S.fab],c=S.cov,t=S.t,sun=sunAt(t),gold=goldAt(t),night=nightAt(t);
    var pct=(c*100).toFixed(2)+'%';
    fabs.forEach(function(x){x.style.height=pct;x.className='st-fabric f-'+S.fab;});
    var gt='rgba(14,20,38,'+(night*.9).toFixed(3)+')';
    tints.forEach(function(x){x.style.background='linear-gradient(180deg,'+gt+','+gt+'),rgba(255,160,80,'+(gold*.28).toFixed(3)+')';x.style.backgroundBlendMode='normal';});
    var exposure=(1-c)+c*f.tr,day=sun*exposure,lamp=night>.35||sun<.35?1:0;
    var lampLvl=clamp((1-sun)*1.1,0,1);
    var ambient=Math.max(day,lampLvl*.32);
    var dark=.8*Math.pow(1-ambient,1.5);
    var warm=gold*.6+lampLvl*.35;
    room.style.opacity=dark.toFixed(3);
    room.style.background='linear-gradient(180deg,rgba('+Math.round(lerp(20,70,warm))+','+Math.round(lerp(26,44,warm))+','+Math.round(lerp(46,30,warm))+',1),rgba('+Math.round(lerp(12,40,warm))+','+Math.round(lerp(14,26,warm))+','+Math.round(lerp(24,18,warm))+',1))';
    var gl=sun*((1-c)+c*f.glare);
    glare.style.opacity=(gl*.85).toFixed(3);
    glare.style.setProperty('--warm',(gold).toFixed(3));
    lamps.style.opacity=(lampLvl*(.55+.45*(1-day))).toFixed(3);
    grab.style.top=((TOP+(BOT-TOP)*c)/H*100)+'%';
    var priv=c*lerp(f.pday,f.pnight,night)+(1-c)*0;
    if(night<.3)priv=Math.max(priv,c*f.pday);
    var view=(1-c)+c*f.view;
    setM('glare',gl,label(gl,.28,.62));setM('privacy',priv,label(priv,.3,.7));setM('view',view,view>.7?'Clear':view>.3?'Soft':'Hidden');
    chip.querySelector('.st-clock').textContent=fmtTime(t);
    chip.querySelector('.st-day').textContent='Daylight in room '+Math.round(day*100)+'%';
    cov.value=Math.round(c*100);tim.value=t;
    cov.style.setProperty('--p',(c*100)+'%');tim.style.setProperty('--p',((t-5)/18*100)+'%');
    scene.classList.toggle('is-night',night>.6);
  }
  function setM(k,v,txt){M[k].querySelector('i').style.width=Math.round(clamp(v,0,1)*100)+'%';M[k].querySelector('b').textContent=txt;}
  function stopAuto(){if(S.auto){S.auto=false;root.classList.remove('playing');play.querySelector('.tx').textContent='Play a smart-home day';play.querySelector('.ic').innerHTML='&#9654;';}}
  function touch(){if(!S.touched){S.touched=true;track('studio_interact');}}

  fabWrap.addEventListener('click',function(e){var b=e.target.closest('.st-fab');if(!b)return;S.fab=b.dataset.f;fabWrap.querySelectorAll('.st-fab').forEach(function(x){x.classList.toggle('on',x===b);});fabDesc.textContent=FABRICS[S.fab].d;touch();render();});
  cov.addEventListener('input',function(){stopAuto();S.paused=false;touch();S.cov=cov.value/100;render();});
  tim.addEventListener('input',function(){stopAuto();S.paused=false;touch();S.t=+tim.value;render();});

  // drag the shade directly
  var dragging=false;
  function fromPointer(e){var r=cv.getBoundingClientRect(),y=(e.clientY-r.top)/r.height*H;S.cov=clamp((y-TOP)/(BOT-TOP),0,1);render();}
  scene.addEventListener('pointerdown',function(e){var r=cv.getBoundingClientRect(),x=(e.clientX-r.left)/r.width*W;if(x<PANES[0][0]-30||x>PANES[2][1]+30)return;dragging=true;stopAuto();touch();scene.setPointerCapture(e.pointerId);scene.classList.add('dragging');fromPointer(e);e.preventDefault();});
  scene.addEventListener('pointermove',function(e){if(dragging)fromPointer(e);});
  function end(){dragging=false;scene.classList.remove('dragging');}
  scene.addEventListener('pointerup',end);scene.addEventListener('pointercancel',end);

  // play a day
  var last=0,lastLog=-1;
  function step(ts){
    if(!S.auto)return;
    var dt=last?Math.min(.05,(ts-last)/1000):0;last=ts;
    S.t+=dt*(18/16);
    var tg=schedTarget(S.t);
    S.cov+=clamp(tg[0]-S.cov,-dt*.55,dt*.55);
    if(tg[1]!==lastLog){lastLog=tg[1];log.querySelectorAll('li').forEach(function(li,i){li.classList.toggle('on',i===tg[1]);li.classList.toggle('done',i<tg[1]);});}
    if(S.t>=23){S.t=23;render();stopAuto();return;}
    render();requestAnimationFrame(step);
  }
  play.addEventListener('click',function(){
    if(S.auto){stopAuto();S.paused=true;return;}
    touch();track('studio_play_day');
    if(!S.paused||S.t>=22.9){S.t=5.2;S.cov=1;}
    S.paused=false;
    S.auto=true;last=0;lastLog=-1;root.classList.add('playing');play.querySelector('.tx').textContent='Pause';play.querySelector('.ic').innerHTML='&#10074;&#10074;';
    if(reduce){S.t=14;S.auto=false;render();return;}
    requestAnimationFrame(step);
  });

  // scroll-linked intro: the shade lowers as the section scrolls into view, until someone touches it
  if(!reduce&&!compact){
    window.addEventListener('scroll',function(){
      if(S.touched||S.auto)return;var r=root.getBoundingClientRect(),vh=window.innerHeight;
      var p=clamp((vh-r.top)/(vh*.9),0,1);S.cov=lerp(0,.62,p);render();
    },{passive:true});
  }
  render();
}

/* ================= ROOM FINDER ================= */
var ROOMS=[
  {k:'Bedroom',img:'norman-portrait-honeycomb-cellular-shades-bedroom-15.webp',pick:'Blackout cellular shades',why:'Honeycomb cells insulate against Ohio winters, and a blackout fabric darkens the room for sleep. Go cordless, or motorize so they close on a schedule.',price:'$175 to $750 per window',link:'/child-pet-safe-cordless-window-treatments/',lt:'Child- and pet-safe options'},
  {k:'Great room',img:'norman-woodlore-composite-plantation-shutters-great-room-36.webp',pick:'Motorized roller or solar shades',why:'Tall and two-story windows can\'t be reached by hand. Group every shade into one scene so the whole wall moves together.',price:'$450 to $1,300 per window',link:'/smart-home-window-automation-central-ohio/',lt:'Smart home automation guide'},
  {k:'Sunroom',img:'norman-perfectsheer-shades-living-room-89.webp',pick:'Solar shades, often motorized',why:'Glass on three sides means glare and heat. A 3 to 5 percent openness cuts both while keeping the view of the yard.',price:'$175 to $650 per window, manual',link:'/sunroom-window-treatments-ohio/',lt:'Sunroom guide'},
  {k:'Kitchen',img:'norman-centerpiece-roman-shades-dining-room-27.webp',pick:'Roller shades or faux wood blinds',why:'Moisture-resistant materials that wipe clean. Keep the fabric consistent with the open living area so it reads as one space.',price:'$125 to $650 per window',link:'/shades-vs-blinds-vs-shutters-ohio/',lt:'Shades vs. blinds vs. shutters'},
  {k:'Front rooms',img:'norman-woodlore-composite-plantation-shutters-living-room-31.webp',pick:'Plantation shutters',why:'The look from the street matters here. Shutters give a clean, consistent exterior and add to resale value.',price:'$275 to $1,600 per window',link:'/plantation-shutters-cost-columbus-ohio/',lt:'Shutter cost guide'},
  {k:'Home office',img:'norman-soluna-roller-shades-home-office-90.webp',pick:'Light-filtering or solar roller shades',why:'Stop afternoon screen glare without killing the daylight. A schedule can lower them at 2 pm every weekday.',price:'$175 to $650 per window',link:'/motorized-shades-cost-central-ohio/',lt:'Full cost guide'}
];
function Rooms(root){
  root.classList.add('rooms');
  var tabs=el('div','rm-tabs');tabs.setAttribute('role','tablist');
  var stage=el('div','rm-stage'),ph=el('div','rm-ph'),card=el('div','rm-card');
  ROOMS.forEach(function(r,i){var b=el('button','rm-tab'+(i===0?' on':''),r.k);b.type='button';b.setAttribute('role','tab');b.dataset.i=i;tabs.appendChild(b);
    var im=el('img');im.src='/images/editorial/'+r.img;im.alt=r.k+' window treatments (manufacturer photo)';im.loading='lazy';im.width=1300;im.height=735;if(i===0)im.className='on';ph.appendChild(im);});
  stage.appendChild(ph);stage.appendChild(card);root.appendChild(tabs);root.appendChild(stage);
  function show(i){var r=ROOMS[i];
    tabs.querySelectorAll('.rm-tab').forEach(function(b,j){b.classList.toggle('on',j===i);b.setAttribute('aria-selected',j===i);});
    ph.querySelectorAll('img').forEach(function(m,j){m.classList.toggle('on',j===i);});
    card.classList.remove('in');void card.offsetWidth;
    card.innerHTML='<p class="rm-k">Best for the '+r.k.toLowerCase()+'</p><h3>'+r.pick+'</h3><p>'+r.why+'</p><p class="rm-price"><span>Typical installed</span>'+r.price+'</p><a class="rm-link" href="'+r.link+'">'+r.lt+' &rarr;</a>';
    card.classList.add('in');}
  tabs.addEventListener('click',function(e){var b=e.target.closest('.rm-tab');if(b){show(+b.dataset.i);track('room_finder',{room:ROOMS[+b.dataset.i].k});}});
  show(0);
}

/* ================= MOTORIZE IT? ================= */
function Motor(root){
  root.classList.add('motor');
  root.innerHTML=
   '<div class="mo-in">'+
   '<label class="mo-f"><span>Windows in the project <b class="v-w">12</b></span><input type="range" min="1" max="40" value="12" class="i-w"></label>'+
   '<label class="mo-f"><span>Out of easy reach (tall, behind furniture) <b class="v-r">3</b></span><input type="range" min="0" max="12" value="3" class="i-r"></label>'+
   '<div class="mo-f"><span>How often you adjust them</span><div class="mo-chips" data-k="use"><button type="button" data-v="0">Rarely</button><button type="button" data-v="1" class="on">Daily</button><button type="button" data-v="2">Several times a day</button></div></div>'+
   '<div class="mo-f mo-tg"><button type="button" class="tg" data-k="kids" aria-pressed="false"><i></i>Kids or pets at home</button><button type="button" class="tg" data-k="smart" aria-pressed="false"><i></i>Use Alexa, Google or Apple Home</button></div>'+
   '</div><div class="mo-out"><p class="mo-k">Our take</p><h3 class="mo-verdict"></h3><p class="mo-why"></p><div class="mo-opts"></div><p class="mo-fine">Budget ranges use typical 2026 Central Ohio installed prices: cordless shades $175 to $750 per window, motorized $450 to $1,300. A free measurement sets the real number.</p></div>';
  var S={w:12,r:3,use:1,kids:false,smart:false};
  function money(n){n=Math.round(n/50)*50;return '$'+n.toLocaleString('en-US');}
  function render(){
    S.r=Math.min(S.r,S.w);root.querySelector('.i-r').max=Math.min(12,S.w);
    root.querySelector('.v-w').textContent=S.w;root.querySelector('.v-r').textContent=S.r;var iw=root.querySelector('.i-w'),ir=root.querySelector('.i-r');iw.style.setProperty('--p',((S.w-1)/39*100)+'%');ir.value=S.r;ir.style.setProperty('--p',(S.r/(+ir.max||1)*100)+'%');
    var score=S.r*2+S.use*2+(S.kids?2:0)+(S.smart?3:0);
    var mix=Math.max(S.r,Math.round(S.w*(S.use===2?.4:S.use===1?.25:0)));if(S.smart||S.use===2)mix=Math.max(mix,Math.ceil(S.w*.3));mix=Math.min(mix,S.w);
    var opts=[
      {k:'manual',n:'All cordless',lo:S.w*175,hi:S.w*750},
      {k:'mix',n:'Motorize '+mix+', cordless the rest',lo:mix*450+(S.w-mix)*175,hi:mix*1300+(S.w-mix)*750},
      {k:'all',n:'Motorize all '+S.w,lo:S.w*450,hi:S.w*1300}];
    var pick=score>=13&&(S.smart||S.use===2)?'all':(S.r>0||score>=6)?'mix':'manual';
    if(pick==='mix'&&mix===0)pick='manual';
    var V={manual:['Keep it manual, go cordless','Nothing is out of reach and you rarely adjust them. Cordless shades are safe, clean-looking and the budget pick.'],
      mix:['Motorize where it counts','Motorize the '+(mix===1?'one window':mix+' windows')+' you can\'t reach or use most, and go cordless everywhere else. It is the most common way Central Ohio homeowners stay on budget.'],
      all:['Motorize the whole house','You adjust them often'+(S.smart?' and already run a smart home':'')+'. Whole-house scenes and schedules are where motorization pays off every single day.']};
    root.querySelector('.mo-verdict').textContent=V[pick][0];
    root.querySelector('.mo-why').textContent=V[pick][1]+(S.kids?' With kids or pets, every option here is cord-free.':'');
    var maxHi=opts[2].hi;
    root.querySelector('.mo-opts').innerHTML=opts.filter(function(o){return !(o.k==='mix'&&(mix===0||mix===S.w));}).map(function(o){
      return '<div class="mo-opt'+(o.k===pick?' on':'')+'"><div class="t"><span>'+o.n+'</span><b>'+money(o.lo)+' to '+money(o.hi)+'</b></div><div class="bar"><i style="left:'+(o.lo/maxHi*100)+'%;width:'+((o.hi-o.lo)/maxHi*100)+'%"></i></div></div>';}).join('');
  }
  root.addEventListener('input',function(e){if(e.target.classList.contains('i-w'))S.w=+e.target.value;if(e.target.classList.contains('i-r'))S.r=+e.target.value;render();});
  root.addEventListener('click',function(e){var c=e.target.closest('.mo-chips button');if(c){c.parentNode.querySelectorAll('button').forEach(function(b){b.classList.toggle('on',b===c);});S.use=+c.dataset.v;render();}
    var t=e.target.closest('.tg');if(t){var k=t.dataset.k;S[k]=!S[k];t.setAttribute('aria-pressed',S[k]);t.classList.toggle('on',S[k]);render();}
    if(c||t)track('motorize_tool');});
  render();
}

/* ================= FLOATING CTA ================= */
function floatCta(){
  var f=el('div','float-cta','<span class="fc-dot"></span><span class="fc-t">Questions? A real person answers.</span><a href="tel:+16149070976" class="fc-call" aria-label="Call Olsson Smart Shades">(614) 907-0976</a><a href="https://olssonss.com/quote" class="fc-go">Free consultation &rarr;</a>');
  f.setAttribute('aria-label','Contact the local installer');d.body.appendChild(f);
  var foot=d.querySelector('.foot');
  var mods=[].slice.call(d.querySelectorAll('.studio,.motor,.rooms,.calc,.cine,.reel'));
  function on(){var y=window.scrollY,vh=window.innerHeight,show=y>vh*.9;if(foot&&foot.getBoundingClientRect().top<vh)show=false;
    mods.forEach(function(m){var r=m.getBoundingClientRect();if(r.top<vh-60&&r.bottom>vh*.35)show=false;});f.classList.toggle('show',show);}
  window.addEventListener('scroll',on,{passive:true});on();
}

function init(){
  d.querySelectorAll('[data-studio]').forEach(function(n){try{Studio(n);}catch(e){}});
  d.querySelectorAll('[data-rooms]').forEach(function(n){try{Rooms(n);}catch(e){}});
  d.querySelectorAll('[data-motor]').forEach(function(n){try{Motor(n);}catch(e){}});
  floatCta();
}
if(d.readyState==='loading')d.addEventListener('DOMContentLoaded',init);else init();
})();
