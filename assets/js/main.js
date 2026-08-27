// TAPIS DIGITECH — interactions (production)
document.addEventListener('DOMContentLoaded', function () {
  var header = document.querySelector('.header');
  function onScroll(){
    if(header) header.classList.toggle('scrolled', window.scrollY > 12);
    var t=document.querySelector('.fab-top');
    if(t) t.classList.toggle('show', window.scrollY > 600);
  }
  window.addEventListener('scroll', onScroll, {passive:true});
  onScroll();

  // Mobile menu (accessible)
  var burger = document.querySelector('.burger');
  var menu = document.querySelector('.mobile-menu');
  if (burger && menu) {
    burger.addEventListener('click', function () {
      var open = menu.classList.toggle('open');
      burger.classList.toggle('open', open);
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
      burger.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
      document.body.style.overflow = open ? 'hidden' : '';
    });
    menu.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () {
        menu.classList.remove('open');
        burger.classList.remove('open');
        burger.setAttribute('aria-expanded','false');
        document.body.style.overflow = '';
      });
    });
  }

  // Back to top
  var topBtn = document.querySelector('.fab-top');
  if (topBtn) topBtn.addEventListener('click', function(){ window.scrollTo({top:0,behavior:'smooth'}); });

  // Scroll reveal — fail-open by design.
  var revealEls = Array.prototype.slice.call(document.querySelectorAll('.reveal'));
  function revealAll() {
    revealEls.forEach(function (el) {
      el.classList.add('in');
      el.style.opacity = '1';
      el.style.transform = 'none';
    });
  }

  if (revealEls.length) {
    if ('IntersectionObserver' in window) {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
          if (e.isIntersecting) {
            e.target.classList.add('in');
            e.target.style.opacity = '1';
            e.target.style.transform = 'none';
            io.unobserve(e.target);
          }
        });
      }, { threshold: 0.01, rootMargin: '0px 0px 180px 0px' });
      revealEls.forEach(function (el) { io.observe(el); });
      window.setTimeout(revealAll, 900);
    } else {
      revealAll();
    }
  }

  // Counters
  function animate(el) {
    var target = parseFloat(el.dataset.count), suffix = el.dataset.suffix || '', dur = 1400, start = null;
    function step(ts){
      if(!start) start=ts;
      var p=Math.min((ts-start)/dur,1);
      var e=1-Math.pow(1-p,3);
      el.textContent = Math.round(target*e)+suffix;
      if(p<1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }
  if ('IntersectionObserver' in window) {
    var cio = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { animate(e.target); cio.unobserve(e.target); }
      });
    }, { threshold: 0.5 });
    document.querySelectorAll('[data-count]').forEach(function (el) {
      el.textContent='0'+(el.dataset.suffix||'');
      cio.observe(el);
    });
  } else {
    document.querySelectorAll('[data-count]').forEach(function (el) { animate(el); });
  }

  // FAQ
  document.querySelectorAll('.faq-q').forEach(function (q) {
    q.setAttribute('tabindex','0');
    q.setAttribute('role','button');
    function toggle(){ q.parentElement.classList.toggle('open'); }
    q.addEventListener('click', toggle);
    q.addEventListener('keydown', function(e){ if(e.key==='Enter'||e.key===' '){ e.preventDefault(); toggle(); } });
  });

  // Testimonial slider
  document.addEventListener('click', function (e) {
    var nav = e.target.closest('[data-testi]');
    if (!nav) return;
    var track = document.getElementById('testiTrack');
    if (!track) return;
    var card = track.querySelector('.testi-card');
    var step = card ? card.offsetWidth + 24 : 340;
    track.scrollBy({ left: (nav.dataset.testi === 'next' ? step : -step), behavior: 'smooth' });
  });

  // Dropdown accessibility: ARIA, keyboard (Escape) and touch toggle.
  document.querySelectorAll('.has-drop').forEach(function (drop) {
    var trigger = drop.querySelector(':scope > a');
    var menu = drop.querySelector(':scope > .dropdown');
    if (!trigger || !menu) return;
    trigger.setAttribute('aria-haspopup', 'true');
    trigger.setAttribute('aria-expanded', 'false');
    function setOpen(open) {
      drop.classList.toggle('open', open);
      trigger.setAttribute('aria-expanded', open ? 'true' : 'false');
    }
    trigger.addEventListener('click', function (e) {
      if (window.matchMedia('(hover: none)').matches && !drop.classList.contains('open')) {
        e.preventDefault();
        document.querySelectorAll('.has-drop.open').forEach(function (d) { if (d !== drop) d.classList.remove('open'); });
        setOpen(true);
      }
    });
    drop.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') { setOpen(false); trigger.focus(); }
    });
    drop.addEventListener('focusout', function () {
      setTimeout(function () { if (!drop.contains(document.activeElement)) setOpen(false); }, 0);
    });
  });
  document.addEventListener('click', function (e) {
    if (!e.target.closest('.has-drop')) {
      document.querySelectorAll('.has-drop.open').forEach(function (d) {
        d.classList.remove('open');
        var t = d.querySelector(':scope > a');
        if (t) t.setAttribute('aria-expanded', 'false');
      });
    }
  });

  // Contact form: validation only. The form itself submits natively to contact.php.
  // This intentionally avoids competing submit handlers and fake client-side success states.
  var contactForm = document.querySelector('#contact-form form[data-validate]');
  if (contactForm) {
    contactForm.setAttribute('action', 'contact.php');
    contactForm.setAttribute('method', 'post');
    contactForm.querySelectorAll('input,textarea,select').forEach(function(inp){
      inp.addEventListener('input', function(){
        var fld=inp.closest('.field');
        if(fld) fld.classList.remove('invalid');
        var status=contactForm.querySelector('.form-status');
        if(status) status.textContent='';
      });
    });
    contactForm.addEventListener('submit', function(e){
      var ok=true;
      var hp=contactForm.querySelector('.hp input');
      if(hp && hp.value){ e.preventDefault(); return; }
      contactForm.querySelectorAll('[required]').forEach(function(inp){
        var valid=inp.value.trim().length>0;
        if(inp.type==='email') valid=valid && /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(inp.value);
        var field=inp.closest('.field');
        if(field) field.classList.toggle('invalid',!valid);
        if(!valid) ok=false;
      });
      if(!ok){
        e.preventDefault();
        var status=contactForm.querySelector('.form-status');
        if(status){ status.className='form-status bad'; status.textContent='Please review the highlighted fields and try again.'; }
        return;
      }
      var btn=contactForm.querySelector('button[type="submit"]');
      if(btn){ btn.disabled=true; btn.setAttribute('aria-busy','true'); btn.dataset.originalText=btn.textContent; btn.textContent='Sending…'; }
    });
  }

  // Display server response state after contact.php redirects back to contact.html.
  var params = new URLSearchParams(window.location.search);
  var responseState = params.get('sent') || params.get('error');
  if (responseState) {
    var status = document.querySelector('#contact-form .form-status');
    if (status) {
      if (responseState === 'sent') {
        status.className='form-status ok';
        status.textContent='Thank you. Your enquiry has been received. Our team will get back to you within one business day.';
      } else if (responseState === 'validation' || responseState === 'invalid') {
        status.className='form-status bad';
        status.textContent='We could not process the enquiry. Please review the form and try again.';
      } else if (responseState === 'mail') {
        status.className='form-status bad';
        status.textContent='We could not send the enquiry right now. Please contact us directly by email or WhatsApp.';
      }
      history.replaceState({}, document.title, window.location.pathname + window.location.hash);
      status.scrollIntoView({behavior:'smooth', block:'nearest'});
    }
  }
});
