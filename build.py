#!/usr/bin/env python3
"""
TAPIS DIGITECH — static page generator (scalable foundation)
============================================================
Single source of truth for the shared <head>, header navigation and footer.
New Services / Solutions / Industries / Trust / Legal pages are generated from
small content definitions so every page stays 100% consistent with the approved
design and navigation. No build step is required at runtime — this script simply
emits plain .html files into the project, exactly like the hand-written pages.

USAGE
-----
    python3 tools/build.py            # regenerate every page defined in pages/*.py-less registry below

To add a new page (e.g. a 4th service), append a dict to the relevant registry
list at the bottom of this file and re-run. See ARCHITECTURE.md for the full
playbook on scaling to 300+ service / 200+ industry / 300+ solution pages.
"""

import os
import json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOMAIN = "https://www.tapisdigitech.com/"
OG_IMAGE = DOMAIN + "assets/images/og-default.png"
PHONE = "+91-7428996299"
WA = "917428996299"
YEAR = 2026

# ----------------------------------------------------------------------------
# Primary navigation (single source of truth). label, href (root-relative),
# optional dropdown of (icon, label, href) and an `id` used for active state.
# ----------------------------------------------------------------------------
NAV = [
    {"id": "home", "label": "Home", "href": "index.html"},
    {"id": "about", "label": "About Us", "href": "about.html"},
    # NOTE: top-nav dropdown destinations are the APPROVED anchors into the
    # Services hub (services.html#…). Dedicated detail pages live under
    # /services/ and are linked from the hub, footer and related-content engine.
    {"id": "services", "label": "Services", "href": "services.html", "drop": [
        ("fa-solid fa-brain", "AI Solutions", "services.html#ai"),
        ("fa-solid fa-code", "Software Development", "services.html#software"),
        ("fa-solid fa-bullhorn", "Digital Marketing", "services.html#marketing"),
        ("fa-solid fa-pen-nib", "Branding & Design", "services.html#design"),
        ("fa-solid fa-cloud", "Cloud & IT Services", "services.html#cloud"),
    ]},
    {"id": "industries", "label": "Industries", "href": "industries.html"},
    {"id": "solutions", "label": "Solutions", "href": "solutions.html"},
    {"id": "case-studies", "label": "Case Studies", "href": "case-studies.html"},
    {"id": "resources", "label": "Resources", "href": "resources.html", "drop": [
        ("fa-solid fa-newspaper", "Blog & Articles", "blog/index.html"),
        ("fa-solid fa-book-open", "Guides & Ebooks", "resources.html#guides"),
        ("fa-solid fa-video", "Webinars", "resources.html#webinars"),
        ("fa-solid fa-circle-question", "FAQs", "resources.html#faq"),
    ]},
    {"id": "careers", "label": "Careers", "href": "careers.html"},
]


def rel(href, depth):
    """Make a root-relative href correct for a page nested `depth` levels deep."""
    if href.startswith(("http", "#", "mailto:", "tel:")):
        return href
    return ("../" * depth) + href


def head(depth, title, description, canonical_path, schema_graph, og_type="website"):
    p = "../" * depth
    canonical = DOMAIN + canonical_path
    full_title = f"{title} — TAPIS DIGITECH"
    schema = json.dumps({"@context": "https://schema.org", "@graph": schema_graph},
                        separators=(",", ":"), ensure_ascii=False)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{full_title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">
<meta name="theme-color" content="#0a1124">
<meta name="author" content="TAPIS DIGITECH">
<meta name="format-detection" content="telephone=no">
<!-- Open Graph -->
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="TAPIS DIGITECH">
<meta property="og:locale" content="en_US">
<meta property="og:title" content="{full_title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{OG_IMAGE}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="TAPIS DIGITECH — Enterprise AI &amp; Digital Transformation">
<!-- Twitter -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{full_title}">
<meta name="twitter:description" content="{description}">
<meta name="twitter:image" content="{OG_IMAGE}">
<link rel="icon" type="image/png" href="{p}assets/favicons/favicon.png">
<link rel="apple-touch-icon" href="{p}assets/favicons/favicon.png">
<link rel="manifest" href="{p}manifest.webmanifest">
<meta name="msapplication-config" content="{p}browserconfig.xml">
<link rel="preload" as="font" type="font/woff2" href="{p}assets/fonts/geist-sans-latin-600-normal.woff2" crossorigin>
<link rel="preload" as="font" type="font/woff2" href="{p}assets/fonts/inter-latin-400-normal.woff2" crossorigin>
<link rel="stylesheet" href="{p}assets/fonts/fonts.css">
<link rel="stylesheet" href="{p}assets/icons/all.min.css">
<link rel="stylesheet" href="{p}assets/css/style.css">
<script type="application/ld+json">{schema}</script>
<script>document.documentElement.classList.add('js');</script>
<!-- Google Tag Manager / GA4 placeholder — add your container ID before deploy
<script>(function(w,d,s,l,i){{...GTM snippet...}})(window,document,'script','dataLayer','GTM-XXXXXXX');</script>
-->
</head>
<body>
<a class="skip-link" href="#main">Skip to main content</a>
"""


def header(depth, active):
    p = "../" * depth
    items = []
    for n in NAV:
        is_active = (n["id"] == active)
        if "drop" in n:
            cls = "has-drop active" if is_active else "has-drop"
            aria = ' aria-current="page"' if is_active else ""
            links = "".join(
                f'<a href="{rel(h, depth)}"><i class="{ic}" aria-hidden="true"></i>{lb}</a>'
                for ic, lb, h in n["drop"]
            )
            items.append(
                f'<li class="{cls}"><a href="{rel(n["href"], depth)}"{aria}>{n["label"]} '
                f'<i class="fa-solid fa-chevron-down" aria-hidden="true"></i></a>'
                f'<div class="dropdown">{links}</div></li>'
            )
        else:
            cls = ' class="active"' if is_active else ""
            aria = ' aria-current="page"' if is_active else ""
            items.append(f'<li{cls}><a href="{rel(n["href"], depth)}"{aria}>{n["label"]}</a></li>')
    nav_links = "".join(items)
    mob = "".join(
        f'<a href="{rel(n["href"], depth)}">{n["label"]}</a>' for n in NAV
    )
    return f"""<header class="header">
  <div class="container nav">
    <a class="brand" href="{p}index.html" aria-label="TAPIS DIGITECH home"><img src="{p}assets/logos/logo-light.png" alt="TAPIS DIGITECH — Digital Solutions, Growth, Success" title="TAPIS DIGITECH — Enterprise AI &amp; Digital Transformation" width="200" height="100" fetchpriority="high" decoding="async"></a>
    <nav class="nav-links-wrap" aria-label="Primary">
      <ul class="nav-links">{nav_links}</ul>
    </nav>
    <div class="nav-cta">
      <a href="{p}contact.html" class="btn btn-primary">Contact Us</a>
      <button class="burger" aria-label="Open menu" aria-expanded="false" aria-controls="mobileMenu"><span></span><span></span><span></span></button>
    </div>
  </div>
  <nav class="mobile-menu" id="mobileMenu" aria-label="Mobile">{mob}<a href="{p}contact.html" class="btn btn-primary">Contact Us</a></nav>
</header>
<main id="main">
"""


def breadcrumb(depth, trail):
    """trail = list of (label, href_or_None). Last item is the current page."""
    parts = []
    for label, href in trail:
        if href is None:
            parts.append(f"<span>{label}</span>")
        else:
            parts.append(f'<a href="{rel(href, depth)}">{label}</a>')
    return '<nav class="crumbs" aria-label="Breadcrumb">' + " / ".join(parts) + "</nav>"


def breadcrumb_schema(trail):
    items = []
    for i, (label, href) in enumerate(trail, 1):
        url = DOMAIN + (href if href else "")
        item = {"@type": "ListItem", "position": i, "name": label}
        if href is not None:
            item["item"] = DOMAIN + href
        items.append(item)
    return {"@type": "BreadcrumbList", "itemListElement": items}


def cta_band(depth):
    p = "../" * depth
    return f"""<section class="cta-band">
    <div class="container">
      <div class="cta-inner reveal">
        <div>
          <span class="eyebrow">Ready to Transform Your Business?</span>
          <h2>Let's Build Something Amazing with AI</h2>
          <p>Book a free consultation and discover how AI and automation can take your business to the next level.</p>
        </div>
        <div class="cta-right">
          <a href="{p}contact.html" class="btn btn-primary">Book Free Consultation <i class="fa-solid fa-arrow-right"></i></a>
          <div class="cta-call"><i class="fa-solid fa-phone"></i> Or call us directly: <b>{PHONE}</b></div>
        </div>
        <svg class="cta-brain" viewBox="0 0 200 200" fill="none" xmlns="http://www.w3.org/2000/svg">
          <g stroke="#3ba3ee" stroke-width="1.2" opacity="0.9">
            <circle cx="100" cy="100" r="60"/><circle cx="100" cy="100" r="40"/>
            <path d="M40 100h120M100 40v120M58 58l84 84M142 58l-84 84"/>
            <circle cx="100" cy="100" r="6" fill="#3ba3ee"/>
            <circle cx="40" cy="100" r="4" fill="#3ba3ee"/><circle cx="160" cy="100" r="4" fill="#3ba3ee"/>
            <circle cx="100" cy="40" r="4" fill="#3ba3ee"/><circle cx="100" cy="160" r="4" fill="#3ba3ee"/>
            <circle cx="58" cy="58" r="4" fill="#3ba3ee"/><circle cx="142" cy="142" r="4" fill="#3ba3ee"/>
            <circle cx="142" cy="58" r="4" fill="#3ba3ee"/><circle cx="58" cy="142" r="4" fill="#3ba3ee"/>
          </g>
        </svg>
      </div>
    </div>
  </section>
"""


def footer(depth):
    p = "../" * depth
    def L(href):
        return rel(href, depth)
    return f"""</main>
<div class="float-ctas">
  <a class="fab fab-wa" href="https://wa.me/{WA}" target="_blank" rel="noopener" aria-label="Chat on WhatsApp"><i class="fa-brands fa-whatsapp" aria-hidden="true"></i></a>
  <a class="fab fab-call" href="tel:+917428996299" aria-label="Call TAPIS DIGITECH at +91-7428996299"><i class="fa-solid fa-phone" aria-hidden="true"></i></a>
  <button class="fab fab-top" type="button" aria-label="Back to top"><i class="fa-solid fa-arrow-up" aria-hidden="true"></i></button>
</div>
<footer class="footer">
  <div class="container">
    <div class="foot-top">
      <div class="foot-brand">
        <img src="{p}assets/logos/logo-light.png" alt="TAPIS DIGITECH logo" title="TAPIS DIGITECH" width="200" height="100" loading="lazy" decoding="async">
        <p>An enterprise AI &amp; digital transformation company. We design, build and scale intelligent technology that helps ambitious businesses grow faster.</p>
        <div class="socials">
          <a href="#" aria-label="TAPIS DIGITECH on Facebook"><i class="fa-brands fa-facebook-f" aria-hidden="true"></i></a>
          <a href="#" aria-label="TAPIS DIGITECH on LinkedIn"><i class="fa-brands fa-linkedin-in" aria-hidden="true"></i></a>
          <a href="#" aria-label="TAPIS DIGITECH on X"><i class="fa-brands fa-x-twitter" aria-hidden="true"></i></a>
          <a href="#" aria-label="TAPIS DIGITECH on Instagram"><i class="fa-brands fa-instagram" aria-hidden="true"></i></a>
          <a href="#" aria-label="TAPIS DIGITECH on YouTube"><i class="fa-brands fa-youtube" aria-hidden="true"></i></a>
        </div>
      </div>
      <div class="foot-cols">
        <div class="foot-col">
          <h3>Company</h3>
          <ul>
            <li><a href="{L('about.html')}">About Us</a></li>
            <li><a href="{L('about.html#team')}">Our Team</a></li>
            <li><a href="{L('careers.html')}">Careers</a></li>
            <li><a href="{L('case-studies.html')}">Case Studies</a></li>
            <li><a href="{L('contact.html')}">Contact Us</a></li>
          </ul>
        </div>
        <div class="foot-col">
          <h3>Services</h3>
          <ul>
            <li><a href="{L('services/ai-solutions.html')}">AI Solutions</a></li>
            <li><a href="{L('services/software-development.html')}">Software Development</a></li>
            <li><a href="{L('services/digital-marketing.html')}">Digital Marketing</a></li>
            <li><a href="{L('services/branding-design.html')}">Branding &amp; Design</a></li>
            <li><a href="{L('services/cloud-it.html')}">Cloud &amp; IT Services</a></li>
          </ul>
        </div>
        <div class="foot-col">
          <h3>Explore</h3>
          <ul>
            <li><a href="{L('industries.html')}">Industries</a></li>
            <li><a href="{L('solutions.html')}">Solutions</a></li>
            <li><a href="{L('resources.html')}">Resources</a></li>
            <li><a href="{L('blog/index.html')}">Blog</a></li>
            <li><a href="{L('trust/index.html')}">Trust Center</a></li>
          </ul>
        </div>
        <div class="foot-col">
          <h3>Legal &amp; Support</h3>
          <ul>
            <li><a href="{L('legal/privacy-policy.html')}">Privacy Policy</a></li>
            <li><a href="{L('legal/terms.html')}">Terms &amp; Conditions</a></li>
            <li><a href="{L('trust/security.html')}">Security</a></li>
            <li><a href="{L('contact.html')}">Support</a></li>
            <li><a href="{L('sitemap.xml')}">Sitemap</a></li>
          </ul>
        </div>
      </div>
    </div>

    <div class="foot-mid">
      <div class="news">
        <h3>Subscribe to our newsletter</h3>
        <p>Get the latest on AI, automation and digital transformation — straight to your inbox.</p>
      </div>
      <form class="news-form" data-validate aria-label="Newsletter signup">
        <div class="hp" aria-hidden="true"><label>Leave this empty<input type="text" tabindex="-1" autocomplete="off"></label></div>
        <label class="sr-only" for="news-email">Email address</label>
        <input id="news-email" name="email" type="email" placeholder="Enter your email" required autocomplete="email">
        <button type="submit">Subscribe</button>
      </form>
    </div>

    <div class="foot-contact">
      <div class="fc-item"><i class="fa-solid fa-location-dot"></i><div><b>Head Office</b><span>New Delhi, India</span></div></div>
      <div class="fc-item"><i class="fa-solid fa-phone"></i><div><b>Call Us</b><span>{PHONE}</span></div></div>
      <div class="fc-item"><i class="fa-solid fa-envelope"></i><div><b>Email Us</b><span>hello@tapisdigitech.com</span></div></div>
      <div class="fc-item"><i class="fa-solid fa-clock"></i><div><b>Working Hours</b><span>Mon–Sat, 9:00 AM – 7:00 PM IST</span></div></div>
    </div>

    <div class="foot-bottom">
      <small>&copy; {YEAR} Tapis Digitech. All Rights Reserved.</small>
      <div class="foot-badges">
        <div class="foot-badge"><i class="fa-solid fa-shield-halved"></i><span><b>Secure by Design</b>Built-in security</span></div>
        <div class="foot-badge"><i class="fa-solid fa-user-check"></i><span><b>Human-in-the-Loop</b>Accountable AI</span></div>
        <div class="foot-badge"><i class="fa-solid fa-layer-group"></i><span><b>Enterprise-Grade</b>Engineering</span></div>
      </div>
      <div class="made">Made with <span class="heart">&hearts;</span> in India</div>
    </div>
  </div>
</footer>
<script src="{p}assets/js/analytics.js"></script>
<script src="{p}assets/js/main.js"></script>
</body>
</html>"""


# Reusable Organization graph nodes shared by every page (entity consistency).
def org_nodes():
    return [
        {"@type": "Organization", "@id": DOMAIN + "#organization", "name": "TAPIS DIGITECH",
         "url": DOMAIN, "logo": DOMAIN + "assets/logos/logo-light.png",
         "description": "Enterprise AI & digital transformation company building AI solutions, custom software and automation.",
         "address": {"@type": "PostalAddress", "addressLocality": "New Delhi", "addressCountry": "IN"},
         "contactPoint": {"@type": "ContactPoint", "telephone": "+91-7428996299", "contactType": "sales", "areaServed": "Worldwide"}},
        {"@type": "WebSite", "@id": DOMAIN + "#website", "url": DOMAIN, "name": "TAPIS DIGITECH",
         "publisher": {"@id": DOMAIN + "#organization"},
         "potentialAction": {"@type": "SearchAction",
                              "target": {"@type": "EntryPoint", "urlTemplate": DOMAIN + "search.html?q={search_term_string}"},
                              "query-input": "required name=search_term_string"}},
    ]


def write(path, html):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote", path)


def page(path, depth, active, title, description, trail, body, extra_schema=None):
    """Assemble and write a complete page."""
    graph = org_nodes() + [breadcrumb_schema(trail)] + (extra_schema or [])
    html = (
        head(depth, title, description, path, graph)
        + header(depth, active)
        + body
        + cta_band(depth)
        + footer(depth)
    )
    write(path, html)


# Content registries are imported from tools/content.py to keep this file focused.
if __name__ == "__main__":
    import content
    content.build(globals())
    print("Done. All generated pages are up to date.")
