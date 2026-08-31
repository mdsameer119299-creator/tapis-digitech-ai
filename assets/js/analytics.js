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
  // with zero HTML changes required.
  function classifyCtaEvent(anchor) {
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

  document.addEventListener('click', function (e) {
    var anchor = e.target.closest('a');
    if (!anchor) { return; }
    var href = anchor.getAttribute('href') || '';
    var commonParams = {
      page_location: window.location.href,
      page_title: document.title
    };

    if (href.indexOf('tel:') === 0) {
      tdxTrack('phone_click', commonParams);
      return;
    }
    if (href.indexOf('mailto:') === 0) {
      tdxTrack('email_click', commonParams);
      return;
    }
    if (href.indexOf('wa.me/') !== -1 || href.indexOf('api.whatsapp.com') !== -1) {
      tdxTrack('whatsapp_click', commonParams);
      return;
    }

    var ctaEvent = classifyCtaEvent(anchor);
    if (ctaEvent) {
      var params = Object.assign({}, commonParams, {
        cta_location: (anchor.closest('header') && 'header') ||
          (anchor.closest('footer') && 'footer') ||
          (anchor.closest('.cta-band, .tdx-cta') && 'cta_band') ||
          'body'
      });
      tdxTrack(ctaEvent, params);
    }
  }, true);

  // ---- Future-tools event helper (see docs/PHASE_B_SEO_AUDIT.md Part 15) --
  // Not wired to any page yet -- no tool exists in the repo at this phase.
  // When a tool ships, it calls these directly, e.g.:
  //   window.tdxTrackTool('start', 'ai_roi_calculator');
  window.tdxTrackTool = function (stage, toolName, extraParams) {
    var eventName = 'tool_' + stage; // tool_start | tool_complete | tool_result_view | tool_cta_click
    tdxTrack(eventName, Object.assign({ tool_name: toolName }, extraParams || {}));
  };
})();
