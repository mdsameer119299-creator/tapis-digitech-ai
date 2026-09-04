/*!
 * TAPIS DIGITECH LAB — Website SEO Audit page glue.
 * Wires the shared TDXAuditEngine to this page's form/loading/error/report
 * elements. No mock or fabricated data lives in this file -- with no
 * backend connected yet, every submission ends in the honest "not
 * available yet" error state below, never a fake report.
 */
document.addEventListener('DOMContentLoaded', function () {
  var TOOL_NAME = 'website_seo_audit';
  var engine = window.TDXAuditEngine;
  if (!engine) { return; }

  var form = document.getElementById('ft-audit-form');
  var input = document.getElementById('ft-audit-url');
  var errEl = document.getElementById('ft-audit-url-err');
  var submitBtn = document.getElementById('ft-audit-submit');
  var loadingEl = document.getElementById('ft-audit-loading');
  var errorPanel = document.getElementById('ft-audit-error');
  var errorMsgEl = document.getElementById('ft-audit-error-msg');
  var reportEl = document.getElementById('ft-audit-report');
  var reportBody = document.getElementById('ft-audit-report-body');
  var ctaBtn = document.getElementById('ft-audit-report-cta');

  if (!form || !input) { return; }

  if (ctaBtn && engine.AuditCTA) { engine.AuditCTA.wire(ctaBtn, TOOL_NAME); }

  function setInvalid(message) {
    var field = input.closest('.field');
    if (field) { field.classList.add('invalid'); }
    input.setAttribute('aria-invalid', 'true');
    if (errEl) { errEl.textContent = message; }
  }

  function clearInvalid() {
    var field = input.closest('.field');
    if (field) { field.classList.remove('invalid'); }
    input.setAttribute('aria-invalid', 'false');
  }

  input.addEventListener('input', clearInvalid);

  form.addEventListener('submit', function (e) {
    e.preventDefault();

    var result = engine.AuditInput.validate(input.value);
    if (!result.valid) {
      setInvalid(result.reason);
      input.focus();
      return;
    }
    clearInvalid();

    if (errorPanel) { errorPanel.classList.remove('on'); }
    if (reportEl) { reportEl.classList.remove('on'); }
    if (loadingEl) { loadingEl.classList.add('on'); }
    if (submitBtn) { submitBtn.disabled = true; submitBtn.textContent = 'Analyzing…'; }

    if (window.tdxTrackTool) { window.tdxTrackTool('start', TOOL_NAME, { target_url_host: safeHost(result.normalized) }); }

    engine.AuditFetcher.run(result.normalized).then(function (report) {
      if (loadingEl) { loadingEl.classList.remove('on'); }
      if (submitBtn) { submitBtn.disabled = false; submitBtn.textContent = 'Analyze Website'; }
      if (window.tdxTrackTool) { window.tdxTrackTool('complete', TOOL_NAME, { target_url_host: safeHost(result.normalized), score: report.overallScore }); }
      if (reportBody) { engine.AuditReport.render(reportBody, report); }
      if (reportEl) { reportEl.classList.add('on'); reportEl.scrollIntoView({ behavior: 'smooth', block: 'start' }); }
      if (window.tdxTrackTool) { window.tdxTrackTool('result_view', TOOL_NAME, { target_url_host: safeHost(result.normalized) }); }
    }).catch(function (err) {
      if (loadingEl) { loadingEl.classList.remove('on'); }
      if (submitBtn) { submitBtn.disabled = false; submitBtn.textContent = 'Analyze Website'; }
      if (errorMsgEl) { errorMsgEl.textContent = (err && err.message) || 'Something went wrong. Please try again.'; }
      if (errorPanel) { errorPanel.classList.add('on'); errorPanel.focus(); }
    });
  });

  // Only used for analytics params -- never shown to the visitor, never
  // sent anywhere but the in-page dataLayer, and deliberately just the
  // hostname (no path/query) to avoid pushing a visitor-typed full URL
  // into analytics.
  function safeHost(u) {
    try { return new URL(u).hostname; } catch (e) { return undefined; }
  }
});
