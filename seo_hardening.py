#!/usr/bin/env python3
"""Apply safe, repeatable SEO hardening to TAPIS DIGITECH static HTML."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SKIP = {'.git', '.github', '__pycache__'}
files = [p for p in ROOT.rglob('*.html') if not any(part in SKIP for part in p.parts)]
changed = []

for path in files:
    text = path.read_text(encoding='utf-8')
    original = text
    rel = path.relative_to(ROOT).as_posix()

    # Internal site-search results should not become indexable landing pages.
    robots = ('noindex, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1'
              if rel == 'search.html' else
              'index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1')
    text = re.sub(r'<meta name="robots" content="[^"]*">',
                  f'<meta name="robots" content="{robots}">', text, count=1)

    # Consistent privacy-preserving referrer behavior.
    if 'name="referrer"' not in text:
        text = text.replace('</head>', '<meta name="referrer" content="strict-origin-when-cross-origin">\n</head>', 1)

    # Correct the root-level browserconfig reference without changing nested pages.
    depth = len(path.relative_to(ROOT).parts) - 1
    expected = '../' * depth + 'browserconfig.xml'
    if depth == 0:
        text = text.replace('href="../browserconfig.xml"', 'href="browserconfig.xml"')
    else:
        text = text.replace('href="browserconfig.xml"', f'href="{expected}"')

    # Never claim ownership of generic social-network homepages in Organization schema.
    text = text.replace(',"sameAs":["https://www.linkedin.com/","https://twitter.com/","https://www.facebook.com/"]', '')

    # Replace generator placeholders if they have leaked into generated HTML.
    text = text.replace('+91 12345 67890', '+91 97182 24996')
    text = text.replace('911234567890', '919718224996')

    if text != original:
        path.write_text(text, encoding='utf-8')
        changed.append(rel)

print(f'SEO hardening changed {len(changed)} HTML files')
for item in changed:
    print(item)
