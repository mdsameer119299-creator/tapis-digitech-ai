#!/usr/bin/env python3
"""Apply safe, repeatable technical SEO and contact-detail hardening to TAPIS DIGITECH static HTML.

Homepage body/layout/content is intentionally NOT rewritten here. The workflow restores
index.html from main first; this script only changes technical metadata, contact signals,
and the approved fourth testimonial placeholder.
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
HOME_DESCRIPTION = 'TAPIS DIGITECH builds AI agents, automation and custom software for businesses in India and global markets, including the USA, UK, UAE, Singapore and Australia.'
HOME_KEYWORDS = 'AI development company India, AI automation company India, AI agents development, custom software development, AI consulting, enterprise AI solutions, AI company Delhi, software development company India, AI chatbot development, workflow automation, digital transformation, AI development USA, AI development UK, AI development UAE, AI development Singapore, AI development Australia'

KASA_CARD = '''      <article class="tdx-tcard2 reveal" style="--d:240ms">
        <div class="stars" aria-label="5 out of 5">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
        <p class="q">"TAPIS DIGITECH is helping us build a modern digital experience with technology, automation and a strong focus on how customers discover and engage with the brand."</p>
        <div class="who"><span class="av">TK</span><span><b>Project Leadership Team</b><span>TAPIS KASA</span></span></div>
      </article>'''

for path in files:
    text = path.read_text(encoding='utf-8')
    original = text
    rel = path.relative_to(ROOT).as_posix()

    robots = ('noindex, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1'
              if rel == 'search.html' else
              'index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1')
    text = re.sub(r'<meta name="robots" content="[^"]*">',
                  f'<meta name="robots" content="{robots}">', text, count=1)

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

    # Remove generic placeholder social URLs from structured data only.
    # The visible footer social icons/markup are left untouched.
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

        if 'TAPIS KASA' not in text:
            marker = '''      <article class="tdx-tcard2 reveal" style="--d:160ms">
        <div class="stars" aria-label="5 out of 5">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
        <p class="q">"From strategy to launch in weeks. The automation alone gave our team hours back every single week."</p>
        <div class="who"><span class="av">HG</span><span><b>Head of Growth</b><span>SaaS</span></span></div>
      </article>'''
            text = text.replace(marker, marker + '\n' + KASA_CARD, 1)

    text = re.sub(r'https://wa\.me/[0-9+\-\s]+', f'https://wa.me/{WHATSAPP}', text)
    for old in OLD_PHONE_PATTERNS:
        text = text.replace(old, DISPLAY_PHONE)
    text = re.sub(r'href="tel:[^"]*"', f'href="tel:{TEL_PHONE}"', text)
    text = re.sub(r'<a\s+class="fab fab-call"[^>]*>', f'<a class="fab fab-call" href="tel:{TEL_PHONE}" aria-label="Call TAPIS DIGITECH at {DISPLAY_PHONE}">', text, count=1)

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
    if text != original:
        build_path.write_text(text, encoding='utf-8')
        changed.append('build.py')

print(f'SEO/contact hardening changed {len(changed)} files')
for item in changed:
    print(item)
