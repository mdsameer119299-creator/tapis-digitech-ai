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
  // The previous implementation depended entirely on IntersectionObserver.
  // If JS was delayed, cached, blocked, or an observer callback failed,
  // .reveal elements could remain opacity:0 and make whole pages look blank.
  var revealEls = Array.prototype.slice.call(document.querySelectorAll('.reveal'));
  function revealAll() {
    revealEls.forEach(function (el) {
      el.classList.add('in');
      // Hard visibility fallback so content can never remain hidden.
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

      // Safety net: even if the observer is unavailable or the page was
      // restored from cache in an odd state, reveal everything shortly after load.
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

  // Forms: validation, honeypot, states (client-side; pair with server validation in production)
  document.querySelectorAll('form[data-validate]').forEach(function (f) {
    f.setAttribute('novalidate','');
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      var ok = true;
      var hp = f.querySelector('.hp input');
      if (hp && hp.value) { return; }
      f.querySelectorAll('[required]').forEach(function (inp) {
        var field = inp.closest('.field');
        var valid = inp.value.trim().length > 0;
        if (inp.type === 'email') valid = valid && /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(inp.value);
        if (field) field.classList.toggle('invalid', !valid);
        if (!valid) ok = false;
      });
      var status = f.querySelector('.form-status');
      if (!ok) {
        if (status){ status.className='form-status bad'; status.textContent='Please correct the highlighted fields.'; }
        return;
      }
      var btn = f.querySelector('button[type=submit],button:not([type])');
      if (btn){
        var t=btn.textContent;
        btn.textContent='Sending…';
        btn.disabled=true;
        setTimeout(function(){
          btn.textContent=t;
          btn.disabled=false;
          f.reset();
          if(status){ status.className='form-status ok'; status.textContent='Thank you! Your message has been received. We’ll reply within one business day.'; }
        }, 1200);
      }
    });
    f.querySelectorAll('input,textarea,select').forEach(function(inp){
      inp.addEventListener('input', function(){ var fld=inp.closest('.field'); if(fld) fld.classList.remove('invalid'); });
    });
  });

  // Real Hostinger/PHP contact submission. This listener runs after the legacy
  // client-side validator above; when the contact form is valid, submit the
  // native form so contact.php receives the lead instead of using fake success.
  var serverContactForm = document.querySelector('#contact-form form[data-validate]');
  if (serverContactForm) {
    serverContactForm.setAttribute('action', 'contact.php');
    serverContactForm.setAttribute('method', 'post');
    serverContactForm.addEventListener('submit', function () {
      var valid = true;
      serverContactForm.querySelectorAll('[required]').forEach(function (inp) {
        if (!inp.value.trim()) valid = false;
        if (inp.type === 'email' && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(inp.value)) valid = false;
      });
      var hp = serverContactForm.querySelector('.hp input');
      if (hp && hp.value) valid = false;
      if (!valid) return;
      window.setTimeout(function () {
        serverContactForm.removeAttribute('data-validate');
        HTMLFormElement.prototype.submit.call(serverContactForm);
      }, 0);
    });
  }
});
