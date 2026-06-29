import os, re, json, glob
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
html=[f for f in glob.glob("**/*.html",recursive=True) if not f.startswith("tools")]
DOMAIN="https://www.tapisdigitech.com/"
errors=[]; warn=[]
href_re=re.compile(r'(?:href|src)="([^"]+)"')
ld_re=re.compile(r'<script type="application/ld\+json">(.*?)</script>', re.S)
script_re=re.compile(r'<script\b[^>]*>.*?</script>', re.S)
h1_re=re.compile(r'<h1[ >]')
def expected_canonical(f):
    if f=="index.html": return DOMAIN
    return DOMAIN+f
for f in html:
    raw=open(f,encoding="utf-8").read()
    s=script_re.sub("", raw)            # ignore links inside JS
    d=os.path.dirname(f)
    for link in href_re.findall(s):
        if link.startswith(("http://","https://","mailto:","tel:","#","data:","javascript:")): continue
        path=link.split("#")[0].split("?")[0]
        if not path: continue
        if not os.path.exists(os.path.normpath(os.path.join(d,path))):
            errors.append(f"[BROKEN LINK] {f} -> {link}")
    for m in ld_re.findall(raw):
        try:
            g=json.loads(m)
            types=[n.get("@type") for n in g.get("@graph",[])] if isinstance(g,dict) else []
            if "page-hero" in raw and "BreadcrumbList" not in str(types) and f not in ("index.html",):
                warn.append(f"[NO BREADCRUMB SCHEMA] {f}")
        except Exception as e: errors.append(f"[BAD JSON-LD] {f}: {e}")
    if len(h1_re.findall(raw))!=1: errors.append(f"[H1 COUNT={len(h1_re.findall(raw))}] {f}")
    cm=re.search(r'<link rel="canonical" href="([^"]+)"', raw)
    if not cm: errors.append(f"[NO CANONICAL] {f}")
    elif cm.group(1)!=expected_canonical(f): errors.append(f"[CANONICAL MISMATCH] {f}: {cm.group(1)} != {expected_canonical(f)}")
    # visible breadcrumb accessibility on inner pages
    if "page-hero" in raw and 'class="crumbs"' in raw and 'aria-label="Breadcrumb"' not in raw:
        warn.append(f"[CRUMBS NOT NAV] {f}")
    if re.search(r'<a href="#">(Privacy Policy|Terms|Security)', raw):
        errors.append(f"[DEAD FOOTER LINK] {f}")
    if "&copy; 2024" in raw: errors.append(f"[STALE YEAR] {f}")
print(f"Scanned {len(html)} files | ERRORS={len(errors)} WARNINGS={len(warn)}")
for e in errors: print("  ",e)
for w in warn: print("  ",w)
