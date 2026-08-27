#!/usr/bin/env python3
"""Apply safe, repeatable SEO and contact-detail hardening to TAPIS DIGITECH static HTML."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SKIP = {'.git', '.github', '__pycache__'}
files = [p for p in ROOT.rglob('*.html') if not any(part in SKIP for part in p.parts)]
changed = []

DISPLAY_PHONE = '+91-7428996299'
WHATSAPP = '917428996299'
OLD_PHONE_PATTERNS = (
    '+91 12345 67890', '+91-12345-67890', '+91 12345-67890', '911234567890',
    '+91 97182 24996', '+91-9718224996', '+91-97182-24996', '+91 9718224996',
    '9718224996', '919718224996', '97182 24996'
)

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
    else:
        text = text.replace('href="browserconfig.xml"', f'href="{expected}"')

    text = text.replace(',"sameAs":["https://www.linkedin.com/","https://twitter.com/","https://www.facebook.com/"]', '')

    # Normalize all known old/placeholder phone representations to the verified business number.
    for old in OLD_PHONE_PATTERNS:
        text = text.replace(old, DISPLAY_PHONE)

    # Normalize all WhatsApp destinations to the verified number.
    text = re.sub(r'https://wa\.me/\d+', f'https://wa.me/{WHATSAPP}', text)

    # The floating call CTA must dial the verified business number directly.
    text = re.sub(
        r'(<a\s+class="fab fab-call"\s+)href="[^"]*"([^>]*)(>)',
        rf'\1href="tel:+{WHATSAPP}"\2 aria-label="Call TAPIS DIGITECH at {DISPLAY_PHONE}"\3',
        text,
        count=1,
    )
    text = re.sub(r'href="tel:\+?\d+"', f'href="tel:+{WHATSAPP}"', text)

    if text != original:
        path.write_text(text, encoding='utf-8')
        changed.append(rel)

print(f'SEO/contact hardening changed {len(changed)} HTML files')
for item in changed:
    print(item)
