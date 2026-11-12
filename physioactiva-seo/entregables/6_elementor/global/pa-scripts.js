/* Physio Activa — JS global: animación reveal + acordeón FAQ (idéntico al de las plantillas). */
(function(){
  function safe(fn,n){try{fn()}catch(e){console.warn(n,e)}}
  function initReveal(){
    var els=document.querySelectorAll('.pa-home .reveal');
    if(!('IntersectionObserver'in window)){els.forEach(function(e){e.classList.add('in')});return;}
    var io=new IntersectionObserver(function(en){en.forEach(function(x){if(x.isIntersecting){x.target.classList.add('in');io.unobserve(x.target);}})},{threshold:0.05});
    els.forEach(function(e){io.observe(e)});
    setTimeout(function(){els.forEach(function(e){e.classList.add('in')})},6000);
  }
  function initFAQ(){
    var list=document.querySelectorAll('.pa-home .faq');
    list.forEach(function(d){
      var ans=d.querySelector('.ans'),btn=d.querySelector('button');
      if(d.classList.contains('open')&&ans)ans.style.maxHeight=ans.scrollHeight+'px';
      btn.addEventListener('click',function(){
        var open=d.classList.contains('open');
        list.forEach(function(x){x.classList.remove('open');var a=x.querySelector('.ans');if(a)a.style.maxHeight=null;});
        if(!open){d.classList.add('open');if(ans)ans.style.maxHeight=ans.scrollHeight+'px';}
      });
    });
  }
  function boot(){var r=document.querySelector('.pa-home');if(r)r.classList.add('is-js');safe(initReveal,'reveal');safe(initFAQ,'faq');}
  if(document.readyState!=='loading'){boot();}else{document.addEventListener('DOMContentLoaded',boot);}
})();
