/*!
 * TAPIS DIGITECH LAB — reusable audit-tool engine.
 *
 * Shared, small, framework-free building blocks any /free-tools/ audit can
 * reuse: validating what the visitor typed, abstracting how a report is
 * fetched (so swapping in a real backend later touches ONE function), and
 * rendering a report consistently. Intentionally not over-built -- there is
 * no plugin system, no state manager, just five plain objects.
 *
 * IMPORTANT: AuditFetcher.endpoint is null by default and MUST stay null in
 * every tool until a real, security-reviewed backend exists for it (see
 * docs/FREE_TOOLS_SECURITY_ARCHITECTURE.md). With no endpoint configured,
 * run() always resolves to a NOT_AVAILABLE error -- it never fabricates a
 * report. This file contains no mock or sample data of any kind; a preview
 * of the finished report UI lives only in the separate, unlinked
 * _dev-preview.html file, which never ships this engine live data.
 */
window.TDXAuditEngine = (function () {
  'use strict';

  // ---------------------------------------------------------------------
  // AuditInput -- validates/normalises what the visitor typed. Purely
  // client-side shape checking (is this a plausible http/https URL) --
  // NOT a security control. Real SSRF/abuse protections belong entirely
  // server-side in the backend that doesn't exist yet.
  // ---------------------------------------------------------------------
  var AuditInput = {
    normalize: function (raw) {
      var v = (raw || '').trim();
      if (!v) { return ''; }
      if (!/^https?:\/\//i.test(v)) { v = 'https://' + v; }
      return v;
    },
    validate: function (raw) {
      var v = AuditInput.normalize(raw);
      if (!v) {
        return { valid: false, reason: 'Enter a website address to analyze.', normalized: '' };
      }
      var parsed;
      try { parsed = new URL(v); } catch (e) {
        return { valid: false, reason: 'That doesn’t look like a valid website address.', normalized: v };
      }
      if (parsed.protocol !== 'http:' && parsed.protocol !== 'https:') {
        return { valid: false, reason: 'Only http:// and https:// addresses are supported.', normalized: v };
      }
      // A bare host needs at least one dot (contact.php's own SMTP host
      // checks aside, this is just "does this look like a real domain",
      // not a security boundary).
      if (parsed.hostname.indexOf('.') === -1) {
        return { valid: false, reason: 'Enter a full website address, e.g. https://example.com.', normalized: v };
      }
      return { valid: true, reason: '', normalized: v };
    }
  };

  // ---------------------------------------------------------------------
  // AuditFetcher -- abstracts "how do we get a report for this URL".
  // Today: no endpoint exists, so every call resolves NOT_AVAILABLE.
  // Tomorrow: set AuditFetcher.endpoint to the real backend path and this
  // function's fetch() call is the only thing that changes -- callers
  // (the page-specific scripts) never change.
  // ---------------------------------------------------------------------
  var AuditFetcher = {
    endpoint: null,
    run: function (targetUrl) {
      return new Promise(function (resolve, reject) {
        if (!AuditFetcher.endpoint) {
          reject({
            code: 'NOT_AVAILABLE',
            message: 'This tool’s analysis engine isn’t connected yet. We’re building it securely -- check back soon, or talk to us directly in the meantime.'
          });
          return;
        }
        fetch(AuditFetcher.endpoint, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ url: targetUrl })
        }).then(function (res) {
          if (!res.ok) {
            reject({ code: 'BACKEND_ERROR', message: 'The audit couldn’t be completed. Please try again in a moment.' });
            return;
          }
          return res.json();
        }).then(function (data) {
          if (data) { resolve(data); }
        }).catch(function () {
          reject({ code: 'NETWORK_ERROR', message: 'We couldn’t reach the audit engine. Check your connection and try again.' });
        });
      });
    }
  };

  // ---------------------------------------------------------------------
  // AuditReport -- renders a report object into a container. Expected
  // shape (all fields required unless noted):
  // {
  //   target: 'https://example.com/',
  //   overallScore: 78,                       // 0-100
  //   categories: [{ key, label, score }],     // 0-100 each
  //   findings: [{
  //     category, severity: 'critical'|'high'|'medium'|'low'|'passed',
  //     title, evidence, recommendation
  //   }]
  // }
  // ---------------------------------------------------------------------
  var SEVERITY_ORDER = ['critical', 'high', 'medium', 'low', 'passed'];
  var SEVERITY_LABEL = { critical: 'Critical Issues', high: 'Needs Attention', medium: 'Worth Reviewing', low: 'Minor Notes', passed: 'What’s Working' };
  var SEVERITY_ICON = { critical: '🔴', high: '⚠️', medium: '⚠️', low: 'ℹ️', passed: '✓' };

  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  var AuditReport = {
    render: function (containerEl, report) {
      if (!containerEl || !report) { return; }
      var html = '';

      html += '<div class="ft-score-head">'
        + '<div><div class="ft-score-num">' + esc(report.overallScore) + '<small>/100</small></div></div>'
        + '<div><div style="font-family:var(--font-head);font-weight:600;margin-bottom:4px">Your Website SEO Score</div>'
        + '<div class="ft-score-target">' + esc(report.target) + '</div></div>'
        + '</div>';

      if (report.categories && report.categories.length) {
        html += '<div class="ft-cat-grid">';
        report.categories.forEach(function (c) {
          html += '<div class="ft-cat-card"><b>' + esc(c.score) + '</b><span>' + esc(c.label) + '</span>'
            + '<div class="ft-cat-bar"><i style="width:' + Math.max(0, Math.min(100, c.score)) + '%"></i></div></div>';
        });
        html += '</div>';
      }

      var byCategory = {};
      (report.findings || []).forEach(function (f) {
        var sev = SEVERITY_ORDER.indexOf(f.severity) === -1 ? 'low' : f.severity;
        (byCategory[sev] = byCategory[sev] || []).push(f);
      });

      SEVERITY_ORDER.forEach(function (sev) {
        var items = byCategory[sev];
        if (!items || !items.length) { return; }
        html += '<div class="ft-findings-group"><h3>' + SEVERITY_ICON[sev] + ' ' + SEVERITY_LABEL[sev] + ' (' + items.length + ')</h3>';
        items.forEach(function (f) {
          html += '<div class="ft-finding sev-' + sev + '">'
            + '<span class="ft-sev sev-' + sev + '">' + esc(f.severity) + '</span>'
            + '<h4>' + esc(f.title) + '</h4>'
            + (f.evidence ? '<p class="ft-evidence">' + esc(f.evidence) + '</p>' : '')
            + (f.recommendation ? '<p><b>Fix:</b> ' + esc(f.recommendation) + '</p>' : '')
            + '</div>';
        });
        html += '</div>';
      });

      containerEl.innerHTML = html;
    }
  };

  // ---------------------------------------------------------------------
  // AuditCTA -- the report's "want us to fix this" hand-off. Kept tiny on
  // purpose: it just wires a click on an existing CTA element to the
  // shared tool-analytics contract. The CTA markup itself lives in the
  // page (reusing .btn/.btn-primary), not generated here.
  // ---------------------------------------------------------------------
  var AuditCTA = {
    wire: function (ctaEl, toolName) {
      if (!ctaEl) { return; }
      ctaEl.addEventListener('click', function () {
        if (window.tdxTrackTool) { window.tdxTrackTool('cta_click', toolName); }
      });
    }
  };

  return { AuditInput: AuditInput, AuditFetcher: AuditFetcher, AuditReport: AuditReport, AuditCTA: AuditCTA };
})();
