# TAPIS DIGITECH — Information & SEO Architecture

This document describes the enterprise architecture introduced in Sprint 1 and the
playbook for scaling the site to **300+ services, 200+ industries, 300+ solutions
and 1000+ blog articles** without thin content and without touching the approved
visual identity or top navigation.

> **Golden rule:** the approved design system (`assets/css/style.css` tokens) and
> the approved top navigation structure are not to be redesigned. Everything below
> *extends* them.

---

## 1. Directory structure

```
/                         core marketing pages (hand-authored, approved)
/services/<slug>.html     service detail pages       (generated)
/industries/<slug>.html   industry detail pages      (generated)
/solutions/<slug>.html    solution (outcome) pages   (generated)
/trust/<slug>.html        Trust Center               (generated)
/legal/<slug>.html        Privacy, Terms             (generated)
/blog/<slug>.html         articles + blog/index.html (hand-authored)
/authors/<slug>.html      author / EEAT pages        (hand-authored)
/tools/                   the page generator (NOT deployed)
```

`services.html`, `industries.html`, `solutions.html` remain the **hub** pages.
Each hub links down to its detail pages ("deep-dive" section) and each detail
page links back up via breadcrumbs — a clean hub-and-spoke topology.

## 2. The page generator (scalable foundation)

All new pages are produced by **`tools/build.py`**, the single source of truth for:

- the `<head>` (canonical, robots, Open Graph, Twitter, JSON-LD graph),
- the approved header navigation (with depth-aware relative paths + active state),
- the footer, floating CTAs and the closing CTA band.

Content lives in **`tools/content.py`** (services, industries, solutions),
**`tools/trust_content.py`** and **`tools/legal_content.py`**. To regenerate:

```bash
python3 tools/build.py
```

`tools/` is build-time only. The output is plain `.html` — no runtime/build step,
exactly like the rest of the site. (`tools/fix_existing.py` was a one-off used to
normalise footers/breadcrumbs on the hand-authored pages.)

### Adding a new page (no thin content)

1. Append a dict to the relevant registry in `tools/content.py`. Each dict already
   forces real substance: a unique `lead`, intro paragraphs, a 6-item capability
   grid, a 4-step process and **related links** (the internal-linking engine).
2. Run `python3 tools/build.py`.
3. Add the URL to `sitemap-pages.xml` and `llms.txt` (or extend the sitemap step).

Because every field is required, you cannot accidentally ship a 50-word stub.

## 3. Internal-linking engine (topical authority)

Every detail page renders a **related-content engine** (`.rel-grid` / `.rel-card`)
that creates the cross-links search engines use to understand topical clusters:

| Page type | Links out to |
|-----------|--------------|
| Service   | Industries it serves · Solutions it powers · Related articles |
| Industry  | Services for the sector · Outcomes · Related articles |
| Solution  | Services that deliver it · Industries · Related articles |
| Blog post | Related articles **+ related services/solutions/industries** |
| Author    | Articles by the author |

This realises the required flows: Service→Industry, Industry→Solution,
Solution→Blog, Blog→Service, Case Study→Solution, Author→Blog. Relationships are
declared once as slugs in `content.py`; the generator resolves names, icons,
descriptions and correct relative paths automatically, so links never rot.

## 4. SEO architecture

- **Canonical consistency** — every page sets a single absolute canonical that
  matches its real URL. The generator derives it from the file path.
- **URL consistency** — lowercase, hyphenated, descriptive slugs under predictable
  directories.
- **Breadcrumbs** — all pages use an accessible `<nav class="crumbs"
  aria-label="Breadcrumb">` *and* a matching `BreadcrumbList` JSON-LD trail.
- **Heading hierarchy** — exactly one `<h1>` per page; sections use `<h2>/<h3>`.
- **Entity consistency** — every page shares the same `#organization` and
  `#website` JSON-LD nodes (one Organization entity, referenced by `@id`).
- **Schema consistency** — service pages emit `Service`, blog posts `BlogPosting`,
  every page a `BreadcrumbList`. Add types in the generator, not by hand.
- **Machine files** — `sitemap-pages.xml`, `sitemap-blog.xml`, `llms.txt`,
  `robots.txt` are kept in sync with the page set.

## 5. Navigation experience

- Top navigation **structure and labels are unchanged** (approved).
- Dropdowns now work for **keyboard** (focus-within + `Escape`) and **touch**
  (first tap opens, outside tap/`Escape` closes), with `aria-haspopup`/
  `aria-expanded` managed in `assets/js/main.js`.
- **Active state** is set per page by the generator (`aria-current="page"`).
- The **footer** is now a real secondary nav: Company / Services (deep links) /
  Explore (incl. Trust Center) / Legal & Support — consistent on every page.

## 6. Enterprise trust foundation

`/trust/` is a hub with sub-navigation covering **Security, Responsible AI,
Technology Stack, Development Process, Quality Assurance**, plus `/legal/`
(Privacy, Terms). These describe our genuine *approach*. Anything requiring
verified facts — certifications, audit reports (SOC 2 / ISO 27001), sub-processor
lists, legal specifics — is rendered as a **clearly-marked `.ph-note` placeholder**
and must be replaced with verified information. **No certifications, awards,
partnerships, statistics or testimonials were invented.**

## 7. Performance & accessibility

- No render-blocking additions; fonts/icons remain self-hosted and subset.
- New components are CSS-only and reuse existing tokens; JS additions are tiny and
  guarded. `prefers-reduced-motion` is respected by the existing rules.
- Targets remain: Performance 95+, Accessibility 100, Best Practices 100, SEO 100.

## 8. Scaling roadmap (Sprint 2+)

1. Promote remaining industries/solutions from the homepage grid into full detail
   pages (one dict each).
2. Introduce blog **categories/tags** as generated archive pages and a
   `CollectionPage` schema; wire posts to category hubs.
3. Generate per-service **sub-service** pages (e.g. `services/ai-solutions/
   chatbots.html`) for the 300+ target, reusing the same generator with `depth=2`.
4. Replace illustrative case studies/testimonials/stats with verifiable proof and
   add `Review`/`CaseStudy` schema.
5. Add an XML sitemap auto-builder step to `tools/build.py`.
