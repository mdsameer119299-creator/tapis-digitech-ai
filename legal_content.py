# -*- coding: utf-8 -*-
"""
TAPIS DIGITECH — Legal pages (Privacy Policy, Terms).
These are clearly-marked TEMPLATES for legal review. They fix the previously
dead footer links and give the site a complete legal scaffold. They are NOT
legal advice and must be reviewed by a qualified professional before relying
on them.
"""


def build_legal(g, page_hero, content_sections, ph):
    depth = 1

    def crumbs(name):
        return g["breadcrumb"](depth, [("Home", "index.html"), (name, None)])

    review_note = ph("This document is a template provided for completeness. Have it reviewed and adapted by a qualified legal professional for your jurisdiction (e.g. India's DPDP Act, GDPR, CCPA) before publishing as binding. Replace bracketed items with your verified business details.")

    # ---- Privacy Policy ----
    path = "legal/privacy-policy.html"
    trail = [("Home", ""), ("Privacy Policy", path)]
    body = page_hero(crumbs("Privacy Policy"), "Privacy Policy",
                     "How TAPIS DIGITECH collects, uses and protects personal information.")
    body += content_sections([
        ("Status", review_note + '<p style="margin-top:14px"><em>Last updated: [DATE]. Effective: [DATE].</em></p>'),
        ("Who we are", "<p>TAPIS DIGITECH (\"we\", \"us\") operates this website and provides AI, software, marketing, design and cloud services. For privacy questions, contact us at <strong>hello@tapisdigitech.com</strong> or the address in our footer.</p>"),
        ("Information we collect", "<p>We collect information you provide directly (such as your name, email, phone and message when you use our contact or newsletter forms), and limited technical information collected automatically (such as device, browser and usage data via analytics, where enabled).</p>"),
        ("How we use information", "<p>We use information to respond to enquiries, provide and improve our services, send communications you have requested, and meet legal obligations. We do not sell your personal information.</p>"),
        ("Legal bases", "<p>Where applicable, we process personal data on the bases of your consent, performance of a contract, our legitimate interests, and compliance with law. You may withdraw consent at any time.</p>"),
        ("Sharing &amp; processors", "<p>We share data only with service providers who help us operate (for example hosting, analytics and email delivery), under appropriate agreements. " + "</p>" + ph("A complete list of sub-processors should be maintained and linked from the Trust Center.")),
        ("Data retention &amp; security", "<p>We keep personal data only as long as necessary for the purposes above, then delete or anonymise it. We apply the security measures described in our <a href=\"../trust/security.html\">Trust Center</a>.</p>"),
        ("Your rights", "<p>Depending on your location you may have rights to access, correct, delete, port or object to processing of your personal data. To exercise these, contact us using the details above.</p>"),
        ("International transfers", "<p>If we transfer data across borders, we use appropriate safeguards consistent with applicable law.</p>"),
        ("Changes", "<p>We may update this policy; material changes will be reflected by the \"last updated\" date above.</p>"),
    ])
    g["page"](path, depth, None, "Privacy Policy", "How TAPIS DIGITECH collects, uses, shares and protects personal information, and the privacy rights available to you.", trail, body)

    # ---- Terms ----
    path = "legal/terms.html"
    trail = [("Home", ""), ("Terms & Conditions", path)]
    body = page_hero(crumbs("Terms &amp; Conditions"), "Terms &amp; Conditions",
                     "The terms that govern your use of the TAPIS DIGITECH website.")
    body += content_sections([
        ("Status", review_note + '<p style="margin-top:14px"><em>Last updated: [DATE].</em></p>'),
        ("Acceptance of terms", "<p>By accessing this website you agree to these terms. If you do not agree, please do not use the site.</p>"),
        ("Use of the site", "<p>You may use this site for lawful purposes only. You agree not to misuse it, attempt to disrupt it, or infringe the rights of others.</p>"),
        ("Intellectual property", "<p>The content, branding and design on this site are owned by TAPIS DIGITECH or its licensors and are protected by law. You may not reproduce them without permission.</p>"),
        ("Services", "<p>Information about our services on this site is general; specific engagements are governed by separate written agreements.</p>"),
        ("Disclaimers", "<p>The site is provided \"as is\" without warranties of any kind to the extent permitted by law. We work to keep information accurate but do not guarantee it is always complete or current.</p>"),
        ("Limitation of liability", "<p>To the maximum extent permitted by law, TAPIS DIGITECH is not liable for indirect or consequential losses arising from use of this site.</p>"),
        ("Governing law", "<p>These terms are governed by the laws of [JURISDICTION]. Disputes are subject to the courts of [JURISDICTION].</p>"),
        ("Contact", "<p>Questions about these terms? Email <strong>hello@tapisdigitech.com</strong>.</p>"),
    ])
    g["page"](path, depth, None, "Terms & Conditions", "The terms and conditions governing use of the TAPIS DIGITECH website, including IP, disclaimers and liability.", trail, body)
