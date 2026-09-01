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
    // Escape closes the mobile menu (it previously had no keyboard way to
    // dismiss it) and returns focus to the burger button so keyboard users
    // land back where they started rather than losing their place.
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && menu.classList.contains('open')) {
        menu.classList.remove('open');
        burger.classList.remove('open');
        burger.setAttribute('aria-expanded', 'false');
        burger.setAttribute('aria-label', 'Open menu');
        document.body.style.overflow = '';
        burger.focus();
      }
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

  // Lead forms: both the contact form and the newsletter signup post to the
  // real Hostinger/PHP handler and only ever show a "received" state after
  // the server actually confirms it -- never on a fixed timer. (main.js has
  // twice regressed to a client-only fake setTimeout success on this
  // branch; if you are re-merging this file from main or elsewhere, keep
  // this block intact.)
  //
  // The raw HTML already carries a real action/method (see contact.html and
  // the news-form markup) so a submission still reaches contact.php even if
  // this script never runs. When it does run, submission is upgraded to a
  // real fetch() POST so the page can show a "Sending..." state, disable the
  // button, and display the server's actual response without a full reload.
  document.querySelectorAll('.news-form').forEach(function (f) {
    // Back-compat: data-action (relative path fix for subdirectory pages)
    // still wins if present; otherwise trust whatever real action the HTML
    // already has, falling back to 'contact.php' only as a last resort.
    var realAction = f.getAttribute('data-action') || f.getAttribute('action') || 'contact.php';
    f.setAttribute('action', realAction);
    f.setAttribute('method', 'post');
  });
  var contactFormEl = document.querySelector('#contact-form form');
  if (contactFormEl && !contactFormEl.getAttribute('action')) {
    contactFormEl.setAttribute('action', 'contact.php');
    contactFormEl.setAttribute('method', 'post');
  }

  // Client-side validation only (for any form still marked data-validate
  // with no server endpoint configured -- not the contact/newsletter forms,
  // handled separately below).
  document.querySelectorAll('form[data-validate]').forEach(function (f) {
    if (f.classList.contains('news-form') || f.closest('#contact-form')) { return; }
    f.setAttribute('novalidate','');
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      var ok = true;
      var hp = f.querySelector('.hp input');
      if (hp && hp.value) { return; }
      f.querySelectorAll('[required]').forEach(function (inp) {
        var field = inp.closest('.field'); var valid = inp.value.trim().length > 0;
        if (inp.type === 'email') valid = valid && /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(inp.value);
        if (field) field.classList.toggle('invalid', !valid);
        inp.setAttribute('aria-invalid', valid ? 'false' : 'true');
        if (!valid) ok = false;
      });
      var status = f.querySelector('.form-status');
      if (!ok) { if (status){ status.className='form-status bad'; status.textContent='Please correct the highlighted fields.'; } return; }
      if (status){ status.className='form-status bad'; status.textContent='This form is not connected to a server endpoint yet.'; }
    });
    f.querySelectorAll('input,textarea,select').forEach(function(inp){
      inp.addEventListener('input', function(){ var fld=inp.closest('.field'); if(fld) fld.classList.remove('invalid'); inp.setAttribute('aria-invalid', 'false'); });
    });
  });

  // Real submission handler for the contact form and every newsletter form:
  // validate -> disable button + show "Sending..." -> real POST via fetch()
  // -> wait for and parse the actual server response -> show success ONLY
  // if the server reports success, otherwise show a real error. No network
  // call is ever assumed to succeed, and no message is shown before the
  // response arrives.
  document.querySelectorAll('#contact-form form, .news-form').forEach(function (f) {
    f.setAttribute('novalidate','');
    f.querySelectorAll('input,textarea,select').forEach(function(inp){
      inp.addEventListener('input', function(){ var fld=inp.closest('.field'); if(fld) fld.classList.remove('invalid'); inp.setAttribute('aria-invalid', 'false'); });
    });

    // Track the first meaningful interaction with the main contact form (not
    // the newsletter form -- a single-email field has no meaningful "start"
    // stage distinct from submit). Fires once per page load, on first focus
    // into any field, before the visitor has necessarily filled anything in.
    // No field values or personal data are ever included -- only which form
    // and which page, matching contact_form_submit/generate_lead's existing
    // no-PII rule.
    if (f.closest('#contact-form')) {
      var contactFormStartTracked = false;
      f.addEventListener('focusin', function () {
        if (contactFormStartTracked) { return; }
        contactFormStartTracked = true;
        if (window.tdxTrack) {
          window.tdxTrack('contact_form_start', {
            form_name: 'contact',
            page_path: window.location.pathname
          });
        }
      });
    }
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      if (f.dataset.submitting === '1') { return; } // guard against double-submit

      var ok = true;
      f.querySelectorAll('[required]').forEach(function (inp) {
        var field = inp.closest('.field'); var valid = inp.value.trim().length > 0;
        if (inp.type === 'email') valid = valid && /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(inp.value);
        if (field) field.classList.toggle('invalid', !valid);
        inp.setAttribute('aria-invalid', valid ? 'false' : 'true');
        if (!valid) ok = false;
      });
      var status = f.querySelector('.form-status');
      if (!ok) {
        if (status){ status.className='form-status bad'; status.textContent='Please correct the highlighted fields.'; }
        return;
      }

      var btn = f.querySelector('button[type="submit"]');
      var originalBtnHTML = btn ? btn.innerHTML : '';
      f.dataset.submitting = '1';
      if (btn) { btn.disabled = true; btn.innerHTML = 'Sending&hellip;'; }
      if (status) { status.className = 'form-status'; status.textContent = ''; }

      fetch(f.getAttribute('action'), {
        method: 'POST',
        body: new FormData(f),
        headers: { 'X-TDX-Ajax': '1' },
        credentials: 'same-origin'
      })
        .then(function (res) {
          return res.json().then(function (data) { return { ok: res.ok, data: data }; });
        })
        .then(function (result) {
          var data = result.data || {};
          if (result.ok && data.success) {
            if (status) { status.className = 'form-status ok'; status.textContent = data.message || 'Thank you! Your submission has been received.'; }
            // Fire the conversion event only now -- after the server has
            // actually confirmed success, never optimistically. See
            // assets/js/analytics.js; a no-op if that file hasn't loaded.
            if (window.tdxTrack) {
              var isContactForm = !!f.closest('#contact-form');
              var commonParams = { page_location: window.location.href, page_title: document.title };
              if (isContactForm) {
                window.tdxTrack('contact_form_submit', commonParams);
                window.tdxTrack('generate_lead', Object.assign({ lead_source: 'contact_form' }, commonParams));
              } else {
                window.tdxTrack('newsletter_signup', commonParams);
              }
            }
            f.reset();
          } else {
            if (status) { status.className = 'form-status bad'; status.textContent = data.message || 'Sorry, something went wrong. Please try again or contact us directly.'; }
          }
        })
        .catch(function () {
          // Network failure, server unreachable, or a non-JSON response --
          // never shown as success, since the server never confirmed it.
          if (status) { status.className = 'form-status bad'; status.textContent = "Sorry, we couldn't reach the server. Please check your connection and try again, or contact hello@tapisdigitech.com directly."; }
        })
        .finally(function () {
          f.dataset.submitting = '0';
          if (btn) { btn.disabled = false; btn.innerHTML = originalBtnHTML; }
        });
    });
  });

  // No-JS fallback only: if this script never ran (blocked, failed to load,
  // or errored earlier in the file), the form above still submits natively
  // via its real action/method, contact.php redirects back with a query
  // param, and -- if main.js loads successfully on that next page load --
  // this shows the same real, server-confirmed result.
  var params = new URLSearchParams(window.location.search);
  var contactStatus = document.querySelector('#contact-form .form-status');
  if (contactStatus && params.get('sent') === '1') {
    contactStatus.className = 'form-status ok';
    contactStatus.textContent = 'Thank you! Your message has been received. We’ll reply within one business day.';
    history.replaceState({}, document.title, window.location.pathname);
  } else if (contactStatus && params.get('error')) {
    contactStatus.className = 'form-status bad';
    contactStatus.textContent = 'We could not send your message. Please try again or contact hello@tapisdigitech.com.';
    history.replaceState({}, document.title, window.location.pathname);
  }
  var newsStatus = document.querySelector('.news-form .form-status');
  if (newsStatus && params.get('subscribed') === '1') {
    newsStatus.className = 'form-status ok';
    newsStatus.textContent = 'Thanks — you’re subscribed.';
    history.replaceState({}, document.title, window.location.pathname);
  } else if (newsStatus && params.get('sub_error')) {
    newsStatus.className = 'form-status bad';
    newsStatus.textContent = 'We could not subscribe you. Please try again or email hello@tapisdigitech.com.';
    history.replaceState({}, document.title, window.location.pathname);
  }
});
