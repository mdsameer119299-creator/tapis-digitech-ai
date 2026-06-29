import re, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
import build

ROOT = build.ROOT
root_files = ["index.html","about.html","services.html","industries.html","solutions.html",
              "case-studies.html","resources.html","careers.html","contact.html","search.html"]
sub_files = ["blog/index.html","blog/ai-agents-customer-support.html",
             "blog/business-automation-before-hiring.html","blog/cloud-migration-guide.html",
             "authors/priya-sharma.html","authors/rahul-mehta.html","authors/sneha-nair.html"]

def footer_only(depth):
    full = build.footer(depth)
    a = full.index('<footer class="footer">')
    b = full.index('</footer>') + len('</footer>')
    return full[a:b]

FOOT0 = footer_only(0)
FOOT1 = footer_only(1)
foot_re = re.compile(r'<footer class="footer">.*?</footer>', re.S)
# convert single-line div.crumbs to nav.crumbs (accessible)
crumb_re = re.compile(r'<div class="crumbs">(.*?)</div>')

def process(rel, depth):
    p = os.path.join(ROOT, rel)
    s = open(p, encoding="utf-8").read()
    orig = s
    foot = FOOT0 if depth == 0 else FOOT1
    s2, n = foot_re.subn(lambda m: foot, s)
    s = s2
    s, nc = crumb_re.subn(lambda m: '<nav class="crumbs" aria-label="Breadcrumb">%s</nav>' % m.group(1), s)
    if s != orig:
        open(p, "w", encoding="utf-8").write(s)
    print(f"{rel}: footer={n} crumbs->nav={nc}")

for f in root_files: process(f, 0)
for f in sub_files: process(f, 1)
