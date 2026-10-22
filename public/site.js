(function(){
  var d=document;
  var reduce=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Masthead shadow + reading progress
  var mh=d.querySelector('.masthead'),bar=d.querySelector('.progress'),prose=d.querySelector('.prose');
  function onScroll(){
    var y=window.scrollY||0;
    if(mh)mh.classList.toggle('scrolled',y>8);
    if(bar&&prose){var r=prose.getBoundingClientRect(),h=prose.offsetHeight-window.innerHeight*.6;
      var p=Math.min(1,Math.max(0,-r.top/(h>0?h:1)));bar.style.width=(p*100)+'%';}
  }
  window.addEventListener('scroll',onScroll,{passive:true});onScroll();

  // Contents list from article headings
  var toc=d.querySelector('.toc ol');
  if(toc&&prose){
    var hs=prose.querySelectorAll(':scope > h2'),links=[];
    hs.forEach(function(h,i){
      if(!h.id)h.id=(h.textContent||'').toLowerCase().replace(/&/g,'and').replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'')||('s'+i);
      var li=d.createElement('li'),a=d.createElement('a');a.href='#'+h.id;a.textContent=h.textContent;li.appendChild(a);toc.appendChild(li);links.push([h,a]);
    });
    if(!links.length){var t=d.querySelector('.toc');if(t)t.remove();}
    if('IntersectionObserver' in window&&links.length){
      var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){links.forEach(function(l){l[1].classList.toggle('on',l[0]===e.target)})}})},{rootMargin:'-20% 0px -70% 0px'});
      links.forEach(function(l){io.observe(l[0])});
    }
  }

  // Scroll reveals
  var els=d.querySelectorAll('.rv,.story-hero');
  if(reduce||!('IntersectionObserver' in window)){els.forEach(function(e){e.classList.add('is-in')});return;}
  var ro=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('is-in');ro.unobserve(e.target)}})},{rootMargin:'0px 0px -8% 0px',threshold:.06});
  els.forEach(function(e){ro.observe(e)});
})();
