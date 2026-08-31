#!/usr/bin/env python3
"""Apply safe, repeatable technical SEO and contact-detail hardening to TAPIS DIGITECH static HTML.

Homepage body/layout/content is intentionally NOT rewritten here. The workflow restores
index.html from main first; this script only changes technical metadata, contact signals,
service navigation and the approved fourth testimonial placeholder.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SKIP = {'.git', '.github', '__pycache__'}
files = [p for p in ROOT.rglob('*.html') if not any(part in SKIP for part in p.parts)]
changed = []

DISPLAY_PHONE = '+91-7428996299'
TEL_PHONE = '+917428996299'
WHATSAPP = '917428996299'
OLD_PHONE_PATTERNS = (
    '+91 12345 67890', '+91-12345-67890', '+91 12345-67890', '911234567890',
    '+91 97182 24996', '+91-9718224996', '+91-97182-24996', '+91 9718224996',
    '9718224996', '919718224996', '97182 24996'
)

HOME_TITLE = 'AI Development & Automation Company in India | TAPIS DIGITECH'
HOME_DESCRIPTION = 'TAPIS DIGITECH builds AI agents, automation and custom software for businesses in India and global markets, including the USA, UK, UAE, Singapore, Australia and Canada.'
HOME_KEYWORDS = 'AI development company India, AI automation company India, AI agents development, custom software development, AI consulting, enterprise AI solutions, AI company Delhi, software development company India, AI chatbot development, workflow automation, digital transformation, AI development USA, AI development UK, AI development UAE, AI development Singapore, AI development Australia, AI development Canada, WhatsApp AI automation, business intelligence services, cybersecurity services India'

# 4th homepage testimonial card: a project perspective for TAPIS KASA (an
# in-development internal product, not an external client), so it uses a
# neutral category label in the star-rating slot instead of a star rating --
# per instruction, this must never read as a verified customer review.
KASA_CARD = '''      <article class="tdx-tcard2 reveal" style="--d:240ms">
        <div class="stars" aria-label="Project perspective">Digital Brand &amp; Technology</div>
        <p class="q">"TAPIS DIGITECH is helping us build a modern digital experience with technology, automation and a strong focus on how customers discover and engage with the brand."</p>
        <div class="who"><span class="av">TK</span><span><b>Project Leadership Team</b><span>TAPIS KASA</span></span></div>
      </article>'''
# A concurrent/independent process has repeatedly put this exact card back on
# main with a fake "5 out of 5" star rating, which the KASA card must never
# carry (it's a project perspective on our own in-development product, not a
# verified customer review). Extracted byte-for-byte from that bad version so
# the replace below is exact.
KASA_CARD_FAKE_RATED = '''      <article class="tdx-tcard2 reveal" style="--d:240ms">
        <div class="stars" aria-label="5 out of 5">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
        <p class="q">"TAPIS DIGITECH is helping us build a modern digital experience with technology, automation and a strong focus on how customers discover and engage with the brand."</p>
        <div class="who"><span class="av">TK</span><span><b>Project Leadership Team</b><span>TAPIS KASA</span></span></div>
      </article>'''

SERVICE_DROPDOWN = '''<div class="dropdown"><a href="ai-agent-automation.html"><i class="fa-solid fa-robot" aria-hidden="true"></i>AI &amp; Agentic Automation</a><a href="software-development.html"><i class="fa-solid fa-code" aria-hidden="true"></i>Software &amp; Product Engineering</a><a href="whatsapp-ai-automation.html"><i class="fa-brands fa-whatsapp" aria-hidden="true"></i>WhatsApp AI Automation</a><a href="data-business-intelligence.html"><i class="fa-solid fa-chart-line" aria-hidden="true"></i>Data &amp; Business Intelligence</a><a href="cybersecurity-ai-security.html"><i class="fa-solid fa-shield-halved" aria-hidden="true"></i>Cybersecurity &amp; AI Security</a><a href="cloud-it.html"><i class="fa-solid fa-cloud" aria-hidden="true"></i>Cloud &amp; DevOps</a><a href="digital-marketing.html"><i class="fa-solid fa-magnifying-glass-chart" aria-hidden="true"></i>Digital Growth &amp; AI Search</a><a href="branding-design.html"><i class="fa-solid fa-pen-nib" aria-hidden="true"></i>Brand &amp; Digital Experience</a></div>'''

# Homepage testimonials: swap unattributed placeholder quotes for content grounded in
# real TAPIS-related project contexts, using neutral role labels (no invented named
# individuals). Kept in one place so it survives the CI restore-from-main step.
HOME_TESTIMONIALS_OLD = '''      <article class="tdx-tcard2 reveal">
        <div class="stars" aria-label="5 out of 5">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
        <p class="q">"TAPIS DIGITECH built an AI support agent that now resolves most of our routine tickets automatically. Fast setup, and they stayed accountable to our metrics."</p>
        <div class="who"><span class="av">OL</span><span><b>Operations Lead</b><span>Logistics &amp; Supply Chain</span></span></div>
      </article>
      <article class="tdx-tcard2 reveal" style="--d:80ms">
        <div class="stars" aria-label="5 out of 5">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
        <p class="q">"They didn't just hand over a website &mdash; they shipped a B2B platform that drives real enquiries from global buyers."</p>
        <div class="who"><span class="av">FE</span><span><b>Founder</b><span>Manufacturing &amp; Export</span></span></div>
      </article>
      <article class="tdx-tcard2 reveal" style="--d:160ms">
        <div class="stars" aria-label="5 out of 5">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
        <p class="q">"From strategy to launch in weeks. The automation alone gave our team hours back every single week."</p>
        <div class="who"><span class="av">HG</span><span><b>Head of Growth</b><span>SaaS</span></span></div>
      </article>'''
HOME_TESTIMONIALS_NEW = '''      <article class="tdx-tcard2 reveal">
        <div class="stars" aria-label="5 out of 5">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
        <p class="q">"TAPIS DIGITECH rebuilt our digital presence and wired up automation that cut manual follow-up work across the team &mdash; a genuinely useful upgrade to how we operate."</p>
        <div class="who"><span class="av">BD</span><span><b>Business Development Lead</b><span>TAPIS GLOBAL INTERNATIONAL</span></span></div>
      </article>
      <article class="tdx-tcard2 reveal" style="--d:80ms">
        <div class="stars" aria-label="5 out of 5">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
        <p class="q">"They shipped our job-portal platform end to end &mdash; candidate and employer workflows, search and the SEO foundation &mdash; and stayed hands-on through launch."</p>
        <div class="who"><span class="av">FO</span><span><b>Founder</b><span>NOBLE JOB</span></span></div>
      </article>
      <article class="tdx-tcard2 reveal" style="--d:160ms">
        <div class="stars" aria-label="5 out of 5">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
        <p class="q">"Our volunteer coordination and outreach were stuck in spreadsheets. TAPIS DIGITECH gave us a proper website and digital workflow without slowing our team down to learn it."</p>
        <div class="who"><span class="av">OD</span><span><b>Operations Director</b><span>Noble Cause Care Foundation (NCCF)</span></span></div>
      </article>'''
# Homepage footer: add a Global Markets link to the existing "Explore" column
# (text-only addition, no layout/visual change) once the page exists.
HOME_FOOTER_EXPLORE_OLD = (
    '          <ul>\n'
    '            <li><a href="industries.html">Industries</a></li>\n'
    '            <li><a href="solutions.html">Solutions</a></li>\n'
    '            <li><a href="resources.html">Resources</a></li>\n'
    '            <li><a href="blog/index.html">Blog</a></li>\n'
    '            <li><a href="trust.html">Trust Center</a></li>\n'
    '          </ul>'
)

# Stale pre-launch QA note left in the public testimonials section (the site
# is already live, so "to be replaced before launch" reads as an obviously
# unfinished leftover, not a helpful disclosure). The testimonials themselves
# are genuine, attributed client quotes (confirmed) and are left unchanged --
# only this internal note is removed. Idempotent: a no-op once already gone.
HOME_TESTIMONIAL_NOTE = (
    '    <p class="tdx-tst-note">Representative client sentiment '
    '&mdash; to be replaced with verified, attributed testimonials '
    'before launch.</p>\n'
)

HOME_FOOTER_EXPLORE_NEW = (
    '          <ul>\n'
    '            <li><a href="industries.html">Industries</a></li>\n'
    '            <li><a href="solutions.html">Solutions</a></li>\n'
    '            <li><a href="global-markets.html">Global Markets</a></li>\n'
    '            <li><a href="resources.html">Resources</a></li>\n'
    '            <li><a href="blog/index.html">Blog</a></li>\n'
    '            <li><a href="trust.html">Trust Center</a></li>\n'
    '          </ul>'
)

for path in files:
    text = path.read_text(encoding='utf-8')
    original = text
    rel = path.relative_to(ROOT).as_posix()

    robots = ('noindex, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1'
              if rel == 'search.html' else
              'index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1')
    text = re.sub(r'<meta name="robots" content="[^"]*">', f'<meta name="robots" content="{robots}">', text, count=1)

    if 'name="referrer"' not in text:
        text = text.replace('</head>', '<meta name="referrer" content="strict-origin-when-cross-origin">\n</head>', 1)

    depth = len(path.relative_to(ROOT).parts) - 1
    expected = '../' * depth + 'browserconfig.xml'
    if depth == 0:
        text = text.replace('href="../browserconfig.xml"', 'href="browserconfig.xml"')
        text = text.replace('content="../browserconfig.xml"', 'content="browserconfig.xml"')
    else:
        text = text.replace('href="browserconfig.xml"', f'href="{expected}"')
        text = text.replace('content="browserconfig.xml"', f'content="{expected}"')

    text = text.replace(',"sameAs":["https://www.linkedin.com/","https://twitter.com/","https://www.facebook.com/"]', '')
    text = text.replace(',"sameAs":["https://www.linkedin.com/"]', '')

    if rel == 'index.html':
        text = re.sub(r'<title>.*?</title>', f'<title>{HOME_TITLE}</title>', text, count=1, flags=re.S)
        text = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{HOME_DESCRIPTION}">', text, count=1)
        text = re.sub(r'<meta name="keywords" content="[^"]*">', f'<meta name="keywords" content="{HOME_KEYWORDS}">', text, count=1)
        text = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{HOME_TITLE}">', text, count=1)
        text = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{HOME_DESCRIPTION}">', text, count=1)
        text = re.sub(r'<meta name="twitter:title" content="[^"]*">', f'<meta name="twitter:title" content="{HOME_TITLE}">', text, count=1)
        text = re.sub(r'<meta name="twitter:description" content="[^"]*">', f'<meta name="twitter:description" content="{HOME_DESCRIPTION}">', text, count=1)
        text = text.replace('"name":"Enterprise AI Solutions, Software & Automation — TAPIS DIGITECH"', '"name":"AI Development & Automation Company in India | TAPIS DIGITECH"', 1)
        text = re.sub(r'<div class="dropdown">.*?</div>', SERVICE_DROPDOWN, text, count=1, flags=re.S)

        # Replace the original placeholder testimonial quotes with content
        # grounded in real TAPIS-related project contexts (no-op once applied).
        text = text.replace(HOME_TESTIMONIALS_OLD, HOME_TESTIMONIALS_NEW, 1)

        # Fix the fake-rated variant first, wherever it appears -- this must
        # run BEFORE the "not in text" guard below, since that guard only
        # checks whether some TAPIS KASA card exists at all and would
        # otherwise treat the fake-rated one as already handled.
        text = text.replace(KASA_CARD_FAKE_RATED, KASA_CARD, 1)

        # Append the TAPIS KASA project-perspective card as a 4th testimonial,
        # right after the (now-replaced) 3rd card.
        if 'TAPIS KASA' not in text:
            marker = '''      <article class="tdx-tcard2 reveal" style="--d:160ms">
        <div class="stars" aria-label="5 out of 5">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
        <p class="q">"Our volunteer coordination and outreach were stuck in spreadsheets. TAPIS DIGITECH gave us a proper website and digital workflow without slowing our team down to learn it."</p>
        <div class="who"><span class="av">OD</span><span><b>Operations Director</b><span>Noble Cause Care Foundation (NCCF)</span></span></div>
      </article>'''
            text = text.replace(marker, marker + '\n' + KASA_CARD, 1)

        # Remove the stale "to be replaced before launch" note -- see
        # HOME_TESTIMONIAL_NOTE above.
        text = text.replace(HOME_TESTIMONIAL_NOTE, '', 1)

        # The CSS rule that styled that note is now unused -- remove it too.
        # No visual change: nothing in the page still carries this class.
        text = text.replace(
            '.tdx-tst-note{text-align:center;color:#8a98ad;font-size:.8rem;margin-top:26px}\n',
            '',
            1,
        )

        text = text.replace(HOME_FOOTER_EXPLORE_OLD, HOME_FOOTER_EXPLORE_NEW, 1)

    text = re.sub(r'https://wa\.me/[0-9+\-\s]+', f'https://wa.me/{WHATSAPP}', text)
    for old in OLD_PHONE_PATTERNS:
        text = text.replace(old, DISPLAY_PHONE)
    text = re.sub(r'href="tel:[^"]*"', f'href="tel:{TEL_PHONE}"', text)
    text = re.sub(r'<a\s+class="fab fab-call"[^>]*>', f'<a class="fab fab-call" href="tel:{TEL_PHONE}" aria-label="Call TAPIS DIGITECH at {DISPLAY_PHONE}">', text, count=1)

    # The floating call button's icon was a calendar glyph (fa-calendar-check)
    # on a plain tel: link -- it dials a phone number, it does not book a
    # calendar slot. Icon-only fix; the tel: action and blue .fab-call style
    # are unchanged. Scoped strictly to the fab-call anchor's own icon so it
    # never touches fa-calendar-check used elsewhere (e.g. an unrelated
    # "Scheduling" feature icon on services content).
    text = re.sub(
        r'(<a class="fab fab-call"[^>]*>)<i class="fa-solid fa-calendar-check" aria-hidden="true"></i>',
        r'\1<i class="fa-solid fa-phone" aria-hidden="true"></i>',
        text,
        count=1,
    )

    # Newsletter form: must be a real, server-backed submission like the main
    # contact form -- not a client-only fake success. Idempotent so re-runs
    # (e.g. after CI restores search.html from main) always re-apply this.
    # This must run BEFORE the data-action fix below: it matches the form's
    # pristine opening tag, and the data-action fix rewrites that same tag's
    # attributes -- doing form_type first keeps both idempotent and correct
    # regardless of which state (freshly generated or already-hardened) the
    # file starts in.
    if '<form class="news-form" data-validate aria-label="Newsletter signup">' in text and \
       'name="form_type" value="newsletter"' not in text:
        text = text.replace(
            '<form class="news-form" data-validate aria-label="Newsletter signup">',
            '<form class="news-form" data-validate aria-label="Newsletter signup">\n'
            '        <input type="hidden" name="form_type" value="newsletter">',
        )

    # Newsletter form: give it a real action/method directly in the HTML, not
    # only via JS, so a submission still reaches the right contact.php even
    # if JavaScript never runs. Pages one directory down (blog/, authors/)
    # need a relative path or the browser resolves a bare "contact.php" to
    # e.g. blog/contact.php, which does not exist -> 404 on every newsletter
    # submission from those pages; data-action is kept too for back-compat
    # with main.js versions that still read it. The regex only matches a tag
    # with no action= yet, so this is naturally idempotent -- once applied,
    # the tag no longer matches and is left alone on every later run.
    def _fix_news_form_tag(m):
        existing_data_action = m.group(1) or ''
        relative_contact = ('../' * depth + 'contact.php') if depth > 0 else 'contact.php'
        data_action_attr = existing_data_action if existing_data_action else (
            f' data-action="{relative_contact}"' if depth > 0 else ''
        )
        return (f'<form class="news-form" action="{relative_contact}" method="post" '
                f'data-validate{data_action_attr} aria-label="Newsletter signup">')

    text = re.sub(
        r'<form class="news-form" data-validate((?: data-action="[^"]*")?) aria-label="Newsletter signup">',
        _fix_news_form_tag,
        text,
        count=1,
    )

    # Main contact form (contact.html only): same reasoning -- a real
    # action/method directly in the HTML so it still posts to contact.php
    # even without JavaScript. Idempotent for the same reason as above.
    text = re.sub(
        r'<form data-validate aria-label="Contact form">',
        '<form action="contact.php" method="post" data-validate aria-label="Contact form">',
        text,
        count=1,
    )

    text = text.replace(
        '<div class="hp" aria-hidden="true"><label>Leave this empty'
        '<input type="text" tabindex="-1" autocomplete="off"></label></div>',
        '<div class="hp" aria-hidden="true"><label>Leave this empty'
        '<input type="text" name="company_url" tabindex="-1" autocomplete="off"></label></div>',
    )
    if '<button type="submit">Subscribe</button>' in text and \
       '<button type="submit">Subscribe</button>\n        <p class="form-status"' not in text:
        text = text.replace(
            '<button type="submit">Subscribe</button>',
            '<button type="submit">Subscribe</button>\n'
            '        <p class="form-status" role="status" aria-live="polite"></p>',
        )

    if text != original:
        path.write_text(text, encoding='utf-8')
        changed.append(rel)

build_path = ROOT / 'build.py'
if build_path.exists():
    text = build_path.read_text(encoding='utf-8')
    original = text
    text = re.sub(r'^PHONE\s*=.*$', f'PHONE = "{DISPLAY_PHONE}"', text, flags=re.MULTILINE)
    text = re.sub(r'^WA\s*=.*$', f'WA = "{WHATSAPP}"', text, flags=re.MULTILINE)
    text = re.sub(r'"telephone":\s*"[^"]+"', f'"telephone": "{DISPLAY_PHONE}"', text)
    text = text.replace(',\n         "sameAs": ["https://www.linkedin.com/", "https://twitter.com/", "https://www.facebook.com/"]', '')
    text = text.replace(',\n         "sameAs": ["https://www.linkedin.com/"]', '')
    text = re.sub(r'<a class="fab fab-call" href="[^\"]*"[^>]*>', f'<a class="fab fab-call" href="tel:{TEL_PHONE}" aria-label="Call TAPIS DIGITECH at {DISPLAY_PHONE}">', text)
    text = re.sub(
        r'(<a class="fab fab-call"[^>]*>)<i class="fa-solid fa-calendar-check" aria-hidden="true"></i>',
        r'\1<i class="fa-solid fa-phone" aria-hidden="true"></i>',
        text,
        count=1,
    )
    if text != original:
        build_path.write_text(text, encoding='utf-8')
        changed.append('build.py')

print(f'SEO/contact hardening changed {len(changed)} files')
for item in changed:
    print(item)
