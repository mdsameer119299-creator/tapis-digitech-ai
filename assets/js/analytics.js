/*!
 * TAPIS DIGITECH — analytics configuration and conversion event tracking.
 *
 * SAFE BY DESIGN: this file works correctly whether or not real analytics
 * IDs are configured. With GTM_CONTAINER_ID left empty, no analytics script
 * ever loads, no network request is made, and no console error is produced
 * -- every event still pushes to window.dataLayer (a harmless in-memory
 * array) so nothing needs to change here once a real ID is added later.
 *
 * ---------------------------------------------------------------------
 * TO ENABLE GOOGLE TAG MANAGER / GA4: set GTM_CONTAINER_ID below to your
 * real container ID (looks like "GTM-XXXXXXX") and nothing else in this
 * file needs to change. See docs/PHASE_B_SEO_AUDIT.md for full setup
 * instructions (creating the GTM container, configuring GA4 inside it,
 * and publishing).
 * ---------------------------------------------------------------------
 */
window.TDX_ANALYTICS_CONFIG = window.TDX_ANALYTICS_CONFIG || {
  // Fill this in once a real GTM container exists, e.g. 'GTM-ABCD123'.
  // Leave it exactly '' (empty string) until then.
  GTM_CONTAINER_ID: ''
};

(function () {
  'use strict';

  window.dataLayer = window.dataLayer || [];

  // Central event helper. Every conversion event in this file (and any
  // future one) goes through this single function, so there is one place
  // that guarantees events never throw and never send sensitive data.
  // Usage: window.tdxTrack('whatsapp_click', { cta_location: 'header' });
  function tdxTrack(eventName, params) {
    try {
      var payload = { event: eventName };
      if (params) {
        for (var key in params) {
          if (Object.prototype.hasOwnProperty.call(params, key) && params[key] !== undefined && params[key] !== null) {
            payload[key] = params[key];
          }
        }
      }
      window.dataLayer.push(payload);
    } catch (e) {
      // Analytics must never break the page.
    }
  }
  window.tdxTrack = tdxTrack;

  // ---- GTM bootstrap (only runs if a real container ID is configured) ----
  var gtmId = window.TDX_ANALYTICS_CONFIG.GTM_CONTAINER_ID;
  if (gtmId) {
    (function (w, d, s, l, i) {
      w[l] = w[l] || [];
      w[l].push({ 'gtm.start': new Date().getTime(), event: 'gtm.js' });
      var f = d.getElementsByTagName(s)[0], j = d.createElement(s), dl = l !== 'dataLayer' ? '&l=' + l : '';
      j.async = true;
      j.src = 'https://www.googletagmanager.com/gtm.js?id=' + i + dl;
      if (f && f.parentNode) { f.parentNode.insertBefore(j, f); }
    })(window, document, 'script', 'dataLayer', gtmId);
  }

  // ---- Conversion event delegation -----------------------------------
  // Uses one delegated click listener on <body> rather than per-element
  // handlers, so it works for every current and future link on every page
  // with zero HTML changes required for the URL-pattern-based events
  // (tel:/mailto:/wa.me) below.
  //
  // For everything else, CTA classification prefers an explicit
  // data-track-cta="<event_name>" attribute on the link over guessing from
  // its visible text. This is the scalable path: adding or renaming a CTA
  // just means setting/copying its data-track-cta attribute, and it can
  // never silently stop being tracked because someone edited the button
  // copy. The old text-pattern matching is kept as a fallback ONLY for
  // links that don't yet carry the attribute, so nothing that already
  // worked (book_consultation_click / get_quote_click / contact_page_cta_click)
  // stops firing while pages are migrated over incrementally.
  function classifyCtaEvent(anchor) {
    if (anchor.dataset && anchor.dataset.trackCta) {
      return anchor.dataset.trackCta;
    }
    var text = (anchor.textContent || '').trim().toLowerCase();
    var onContactPage = /\/contact\.html$/.test(window.location.pathname) || window.location.pathname === '/contact.html';
    if (/book.*consult|consultation|discovery call|schedule a demo/.test(text)) {
      return 'book_consultation_click';
    }
    if (/quote|proposal|estimate/.test(text)) {
      return 'get_quote_click';
    }
    if (onContactPage && anchor.matches('.btn, [class*="btn-"]')) {
      return 'contact_page_cta_click';
    }
    return null;
  }

  // Where on the page a click happened, for the cta_location param. An
  // explicit data-cta-location on the element always wins; otherwise this
  // falls back to DOM position, including a floating-widget check for the
  // sticky WhatsApp/Call buttons (assets in .float-ctas).
  function classifyCtaLocation(anchor) {
    if (anchor.dataset && anchor.dataset.ctaLocation) {
      return anchor.dataset.ctaLocation;
    }
    if (anchor.closest('.float-ctas')) { return 'floating'; }
    if (anchor.closest('header')) { return 'header'; }
    if (anchor.closest('footer')) { return 'footer'; }
    if (anchor.closest('.cta-band, .tdx-cta, .tdx-final')) { return 'cta_band'; }
    if (anchor.closest('.tdx-hero, section.hero')) { return 'hero'; }
    if (anchor.closest('.afx-sec')) { return 'automation_flow'; }
    if (anchor.closest('.tdx-prodcard')) { return 'products'; }
    if (anchor.closest('section.sec.alt')) { return 'outcomes'; }
    return 'body';
  }

  document.addEventListener('click', function (e) {
    var anchor = e.target.closest('a');
    if (!anchor) { return; }
    var href = anchor.getAttribute('href') || '';
    var commonParams = {
      page_location: window.location.href,
      page_title: document.title,
      page_path: window.location.pathname
    };

    if (href.indexOf('tel:') === 0) {
      tdxTrack('phone_click', Object.assign({}, commonParams, { cta_location: classifyCtaLocation(anchor) }));
      return;
    }
    if (href.indexOf('mailto:') === 0) {
      tdxTrack('email_click', Object.assign({}, commonParams, { cta_location: classifyCtaLocation(anchor) }));
      return;
    }
    if (href.indexOf('wa.me/') !== -1 || href.indexOf('api.whatsapp.com') !== -1) {
      tdxTrack('whatsapp_click', Object.assign({}, commonParams, { cta_location: classifyCtaLocation(anchor) }));
      return;
    }

    var ctaEvent = classifyCtaEvent(anchor);
    if (ctaEvent) {
      var params = Object.assign({}, commonParams, {
        cta_name: (anchor.dataset && anchor.dataset.ctaName) || (anchor.textContent || '').trim(),
        cta_location: classifyCtaLocation(anchor),
        service: (anchor.dataset && anchor.dataset.service) || document.body.dataset.service || undefined
      });
      tdxTrack(ctaEvent, params);
    }
  }, true);

  // ---- service_page_view -----------------------------------------------
  // Fires once per page load, only on pages explicitly marked as an
  // individual service page via <body data-page-type="service"
  // data-service="...">. Deliberately does NOT fire on the services hub
  // (data-page-type="service_hub") or on industry/solution/blog pages --
  // this event answers "which specific service is generating interest",
  // not "did someone view a page in the services section broadly".
  if (document.body && document.body.dataset.pageType === 'service') {
    tdxTrack('service_page_view', {
      service: document.body.dataset.service || undefined,
      page_path: window.location.pathname,
      page_title: document.title
    });
  }

  // ---- Future-tools event helper (see docs/PHASE_B_SEO_AUDIT.md Part 15) --
  // Not wired to any page yet -- no tool exists in the repo at this phase.
  // When a tool ships, it calls these directly, e.g.:
  //   window.tdxTrackTool('start', 'ai_roi_calculator');
  window.tdxTrackTool = function (stage, toolName, extraParams) {
    var eventName = 'tool_' + stage; // tool_start | tool_complete | tool_result_view | tool_cta_click
    tdxTrack(eventName, Object.assign({ tool_name: toolName }, extraParams || {}));
  };
})();
