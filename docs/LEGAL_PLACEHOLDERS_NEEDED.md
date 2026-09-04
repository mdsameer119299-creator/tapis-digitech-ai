# Legal Page Placeholders — Business Input Required

This document catalogs every placeholder or incomplete section currently on
`privacy-policy.html` and `terms.html`. None of the underlying legal facts
(dates, jurisdiction, sub-processor list) can be safely invented, so this is
a checklist of exactly what the business owner (and, ideally, a qualified
legal professional) needs to supply before either page can be published as
a binding policy rather than a template.

Both pages already carry a visible, honest disclosure (`<div class="ph-note">`)
telling visitors the document is a template pending legal review — that
disclosure is intentional and should stay in place until the items below are
resolved, not be quietly removed.

## privacy-policy.html

| Location | Placeholder | What's needed |
|---|---|---|
| "Status" section | `Last updated: [DATE]. Effective: [DATE].` | Real effective/last-updated dates, set once the policy has actually been reviewed and approved. |
| "Status" section | `Placeholder —` legal-review notice | Sign-off from a qualified legal professional for the applicable jurisdiction(s) (e.g. India's DPDP Act, GDPR, CCPA), then this notice can be removed. |
| "Sharing & processors" section | "A complete list of sub-processors should be maintained and linked from the Trust Center." | The actual list of third-party processors currently in use (hosting provider, analytics, email/SMTP delivery, etc.) so it can be published and linked from `trust.html`. |

## terms.html

| Location | Placeholder | What's needed |
|---|---|---|
| "Status" section | `Last updated: [DATE].` | Real last-updated date, set once the terms have actually been reviewed and approved. |
| "Status" section | `Placeholder —` legal-review notice | Same legal sign-off as above; then this notice can be removed. |
| "Governing law" section | `governed by the laws of [JURISDICTION]. ... courts of [JURISDICTION]` | The business's chosen governing law and forum (this is a legal/business decision — e.g. India, given the registered address on the Organization schema is New Delhi — but it must be confirmed by the business owner, not inferred from a mailing address). |

## Explicitly not done here

Per the governing instructions for this remediation, none of the above were
filled in with invented values — including using the New Delhi address
already present in the site's structured data as a stand-in for a governing
-law jurisdiction. A mailing address is not the same thing as a deliberate
choice of governing law, so that field is left for the business owner to
decide.

## security.html / trust.html

These pages already handle the equivalent placeholder honestly: their
"Certifications & formal assurance" sections explicitly disclose that no
certification (ISO 27001, SOC 2, etc.) is currently held, and that nothing
on the page should be read as a current certification unless listed with
evidence. No fabricated certification claims were found on `main`, and no
change was needed there.
