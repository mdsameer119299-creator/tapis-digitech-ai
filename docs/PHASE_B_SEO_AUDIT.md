# Phase B — SEO, Analytics, Indexation & Technical Quality Audit

**Repository:** mdsameer119299-creator/tapis-digitech-ai
**Branch:** `phase-b-seo-analytics` (created from `seo-responsive-lead-gen-2026-08` at commit `d442cb0`, the tip of Phase A)
**Audit date:** 2026-08-31
**Scope:** 50 published HTML files (49 indexable + `search.html`, which is intentionally `noindex`)
**Method:** every claim in this document was produced by a script reading the actual repository files in this session (BeautifulSoup-based metadata extraction, regex/XML parsing, a live PHP server, and a real headless Chromium browser via Playwright) — nothing below is inferred or assumed. Where a number could not be verified this way (Search Console indexation counts, Lighthouse/PageSpeed scores, real-world GTM/GA4 behavior), this document says so explicitly instead of guessing.

Per the standing project rule, this phase does not touch homepage layout, visual identity, animations, or color. Every fix below is metadata, configuration, dead-code removal, or a verified accessibility/technical bug — nothing changes what a visitor sees on the homepage, and the two logo edits (below) were pixel-verified to render identically at their real on-page size.

---

## 1. Executive Summary

The codebase was, on inspection, in materially better shape than a "cold" audit usually finds: across all 50 pages there is zero missing/empty/generic `alt` text (96 images checked), zero pages with more or fewer than one `<h1>`, zero JSON-LD parse errors, zero fake `AggregateRating`/review schema, zero generic ("click here") anchor text, and a robots.txt / `.htaccess` / canonical-tag chain that is fully self-consistent (https + `www.tapisdigitech.com`, enforced by a real 301 redirect, matching every page's canonical tag and the generator scripts' `DOMAIN` constant). Phase A's trust fixes (fabricated case studies removed, stale testimonial note removed, no fake ratings) were verified still in place and were not touched.

Real problems found and fixed directly in this phase: one keyword-stuffed title/description matching the explicitly-banned pattern; zero Open Graph/Twitter Card tags on all seven Global Markets country pages; two blog posts that existed on disk with correct metadata and were already in the sitemap, but were invisible in `blog/index.html`'s own grid and JSON-LD (a real discoverability bug); eight indexable pages (the Trust Center hub and legal pages) missing from `sitemap-pages.xml`; a dead, inert fake-GTM-ID HTML comment duplicated across 35 pages; no analytics/conversion-tracking architecture at all; and a mobile burger-menu tap target that measured 36×28px against best-practice's ~44×44px. A logo asset (`logo-light.png`, loaded on all 50 pages) was serving at 1774×887px for a 200×100px display slot; it has been safely re-encoded to 400×200px (retina-sharp, visually identical, verified by screenshot) cutting its weight from 230KB to 35.7KB.

One real bug was introduced and then caught by this phase's own testing before delivery: an early version of the `analytics.js` script-tag injection in `seo_hardening.py` used a substring guard that coincidentally matched text inside its own explanatory HTML comment, which would have silently prevented `index.html`/`search.html` from ever receiving the analytics tag once CI restored them from `main`. The CI-restore idempotency simulation (mandated by this project's testing checklist) caught it; it's fixed and now verified idempotent across three consecutive runs with byte-identical output.

No Search Console data, Lighthouse score, or real GTM/GA4 behavior is claimed anywhere in this document — this sandbox cannot reach Google's services, and inventing those numbers was explicitly prohibited.

## 2. Site Inventory (Part 1)

50 HTML files, all under one Apache vhost (`tapisdigitech.com`), no subdomains, no CMS — hand-authored plus five Python generator scripts (`build.py`, `content.py`, `home_rebuild.py`, `legal_content.py`, `trust_content.py`) at the repo root. Breakdown by section:

- **Core/company:** `index.html`, `about.html`, `contact.html`, `careers.html`, `search.html` (noindex)
- **Services (8):** `services.html` hub + `ai-agent-automation.html`, `whatsapp-ai-automation.html`, `data-business-intelligence.html`, `cybersecurity-ai-security.html`, `software-development.html`, `digital-marketing.html`, `branding-design.html`, `cloud-it.html`
- **Industries (5):** `industries.html` hub + `healthcare.html`, `retail-ecommerce.html`, `finance.html` (+ industries hub covers remaining verticals in-page)
- **Solutions (4):** `solutions.html` hub + `reduce-support-costs.html`, `automate-operations.html`, `increase-revenue.html`
- **Global Markets (8):** `global-markets.html` hub + 7 country pages (India, USA, UK, UAE, Singapore, Australia, Canada)
- **Proof/trust:** `case-studies.html`, `resources.html`
- **Trust Center hub (6, added to sitemap this phase):** `trust.html`, `security.html`, `responsible-ai.html`, `technology-stack.html`, `development-process.html`, `quality-assurance.html`
- **Legal (2):** `privacy-policy.html`, `terms.html`
- **Blog (6):** `blog/index.html` + 5 posts
- **Author bios (3):** `authors/priya-sharma.html`, `authors/rahul-mehta.html`, `authors/sneha-nair.html`

Every one of the 50 files was machine-checked for: URL, title, meta description, canonical, robots directive, H1/H2 count, JSON-LD `@type` list, internal/outbound link counts, image alt coverage, and generic-anchor count. The full per-file JSON is not included here (it would be a ~50-entry dump with little narrative value); findings below are the aggregated results.

## 3. Title & Meta Description Audit (Part 2)

**Finding (fixed):** `ai-development-india.html` had a 91-character, keyword-stuffed title — `"AI Development Company in India — Delhi NCR, Mumbai, Bengaluru & Pan-India | TAPIS DIGITECH"` — matching the exact banned pattern shape ("Best X Y Z | Brand"), and a 197-character meta description listing six cities in a row. Replaced with a 59-character natural title, `"AI Development for Businesses Across India | TAPIS DIGITECH"`, and a 128-character description that mentions the country and two representative cities without stuffing. Verified it does not duplicate or collide with the homepage title/description or with any other country page's title.

**Checked, no other violations found:** all other 49 titles are unique (zero duplicates), all fall in the 25–70 character range, none use the banned "Best AI Development Company AI Agency..." pattern, and all descriptions are unique and under 160 characters. This was a single, isolated violation, not a site-wide pattern.

## 4. Canonical URL Audit (Part 3)

Canonical domain was **not guessed** — it was read from three independent, agreeing sources: the generator scripts' `DOMAIN = "https://www.tapisdigitech.com/"` constant (`build.py`, `content.py`, `audit.py`), and the live `.htaccess`, which 301-redirects any non-HTTPS or non-`www` request to `https://www.tapisdigitech.com` and additionally redirects `/index.html` to `/`. All 50 pages' `<link rel="canonical">` tags were checked programmatically: **100% use `https://www.tapisdigitech.com`, zero use a bare domain or `http://`, zero point to a different URL than the page's own address, zero duplicates.** No index.html-duplication issue exists because the `.htaccess` rule and the homepage's canonical tag agree (`/`, not `/index.html`). No trailing-slash inconsistency was found — non-homepage pages consistently use the `.html` extension in both their canonical tag and every internal link to them, so there is no parallel clean-URL path creating a duplicate.

**Recommendation only (no code change):** the `.htaccess` redirect chain was not modified, since this is DNS/deployment-adjacent territory this phase does not touch, and it was already correct.

## 5. robots.txt Audit (Part 4)

```
User-agent: *
Allow: /
Sitemap: https://www.tapisdigitech.com/sitemap.xml
```

Clean. No `Disallow` rules at all (nothing is blocked, including CSS/JS — verified no `/assets/` block exists), and it correctly points at the sitemap index. No changes made or needed.

## 6. Sitemap Audit (Part 5)

**Finding (fixed):** `sitemap-pages.xml` was missing 8 real, indexable, correctly-canonicalized pages that exist in the repo and are linked from the site: `trust.html`, `security.html`, `responsible-ai.html`, `technology-stack.html`, `development-process.html`, `quality-assurance.html`, `privacy-policy.html`, `terms.html`. All eight were added with sensible `priority`/`changefreq` values (0.5/monthly for the Trust Center pages, 0.3/yearly for the two legal pages, matching the existing convention for similar page types) and `lastmod` set to today's date. `sitemap.xml`'s `<lastmod>` for the `sitemap-pages.xml` entry was bumped to match.

**Verified after the fix:** `sitemap-pages.xml` now has exactly 43 URLs and `sitemap-blog.xml` has 6, for 49 total — which is exactly the count of indexable pages on the site (50 files minus `search.html`, which is correctly *not* in any sitemap because it's `noindex`). That is a 1:1 match between "pages that should be indexed" and "pages listed in the sitemap," with zero gaps and zero extras.

**Checked, no changes needed:** `sitemap-blog.xml` already listed all 6 blog files including the two posts added to `blog/index.html`'s grid in this phase — I initially assumed these might be missing there too and confirmed by reading the file that they were not; no edit was made. `sitemap-images.xml` is valid XML and lists images only for the homepage (2 images) — it is not broken, but it is minimal; see the P2 recommendation below. Every `<loc>` in all three sub-sitemaps uses the same `https://www.tapisdigitech.com` absolute-URL form as the canonical tags (verified programmatically, zero mismatches), and there are zero duplicate `<loc>` entries in any sitemap.

**KEEP:** all 49 URLs now in `sitemap-pages.xml` + `sitemap-blog.xml` — every one resolves to a real 200-status file in the repo with `index, follow` robots and a self-referential canonical.
**REMOVE:** none identified — `search.html` was already correctly excluded.
**INVESTIGATE:** none outstanding. (See Section 8 for the Global Markets thin-content question, which is a content-strategy question, not a sitemap-inclusion question — none of those 7 pages are proposed for removal from the sitemap.)

## 7. Indexation Classification (Part 6)

The user-supplied Search Console snapshot (~63 indexed / ~64 not-indexed, from before this phase) is the only real indexation data available, and it is **not** re-derived, extended, or second-guessed here — this sandbox has no Search Console access. What follows is a structural classification of the 50 on-disk pages by what *should* happen to them, for the user to cross-reference against Search Console directly:

- **A — Keep & actively index (high confidence):** homepage, `services.html` + 8 service pages, `industries.html` + 3 industry pages, `solutions.html` + 3 solution pages, `about.html`, `contact.html`, `case-studies.html`, `careers.html`, `resources.html`, `blog/index.html` + 5 posts. These have unique, substantial content, clean metadata, and real internal link equity (7–8 inbound links on average for the older blog posts).
- **B — Keep & index, monitor (structurally sound, thinner content):** the Trust Center hub pages (`trust.html`, `security.html`, `responsible-ai.html`, `technology-stack.html`, `development-process.html`, `quality-assurance.html`) and the 2 legal pages — legitimate, necessary pages, but not content Google will rank competitively; their value is trust/compliance signaling and internal linking, not organic acquisition. No action needed beyond the sitemap fix already made.
- **C — Keep, but review as a group before expecting inclusion (Global Markets country pages):** all 7 `ai-development-<country>.html` pages. See Section 8 — these are correctly indexable and non-duplicate, but thin and templated enough that Search Console may reasonably treat them as low-priority. Recommendation only: no page in this group is proposed for removal.
- **D — Utility, correctly excluded:** `search.html` (`noindex`, zero inbound internal links — reached only via the on-site search box, exactly as intended).
- **E — Remove from index:** none identified. Nothing in the current 50-page inventory looks like a candidate for deletion or deindexing.

No page was auto-deleted or had its robots directive changed as part of this classification — this section is documentation only, per the instruction not to force non-indexed pages into Google or invent Search Console data.

## 8. Thin/Duplicate Content Audit — Global Markets (Part 7)

**Word counts (main content area, machine-counted):** India 200, UK 181, USA 174, Singapore 165, UAE 164, Australia 160, Canada 159. All seven sit in a narrow 159–200 word band.

**Duplicate-content check (5-word shingle Jaccard similarity, all 21 pairs computed):** the highest similarity between any two country pages is **0.076** (UK↔Canada) — meaning even the most similar pair shares under 8% of their five-word phrase sets. These are not literal or near-duplicate pages; each has genuinely distinct body copy. For comparison, this is well below any reasonable duplicate-content threshold.

**The actual risk is structural, not textual:** all seven pages follow an identical H1/H2/CTA template and sit in the same narrow word-count band, which is the classic "programmatic SEO" shape search engines watch for even when the prose itself differs. Combined with each page having exactly one inbound link (from `global-markets.html`) and no unique supporting content (no country-specific case study, pricing note, or client example), this is a legitimate consolidation candidate — but which of the three options below is right depends on business priorities this audit can't determine:

- Enrich each page with country-specific substance (a local case study, timezone/engagement-model detail, local compliance notes) to justify seven separate URLs, or
- Consolidate to a single `/global-markets.html` with country sections instead of seven thin standalone pages, or
- Leave as-is if the seven pages are intentionally covering different search queries the business considers each worth targeting independently.

**No page in this group was deleted, merged, or deindexed.** This is a Section 19/P1 recommendation only.

## 9. Heading Structure Audit (Part 8)

Every one of the 50 pages has **exactly one** `<h1>` (machine-verified, zero exceptions) and a sensible H2 count (ranging 2–8 depending on page length/type). No heading-hierarchy restructuring was needed or performed — this was already clean, and no visual/layout change was made anywhere to "improve" heading tags.

## 10. Image SEO Audit (Part 9)

96 `<img>` tags across the site; **zero missing `alt`, zero empty `alt=""` where the image isn't decorative, zero generic (`"image"`, `"photo"`) alt text, and zero keyword-stuffed alt text** matching the banned pattern. This was fully clean before this phase and required no fixes.

**Performance finding (fixed):** `assets/logos/logo-light.png` — the header/footer logo loaded on all 50 pages — was a 1774×887px, 230KB RGBA PNG displayed everywhere at 200×100px (every `<img>` tag specifies `width="200" height="100"`; verified across all 50 files). It has been re-encoded at 400×200px (2× the largest actual display size, for retina sharpness) using high-quality Lanczos resampling, reducing it to 35.7KB — an 84% reduction, shipped on every single page. This was verified two ways before being applied: a Playwright screenshot of the rendered header comparing before/after (visually identical — the icon's line weight and proportions are unchanged, only invisible excess pixel data was removed), and confirming the live-served file matches the optimized bytes via a local PHP server.

**Documented, not changed — three unused image assets:** `assets/logos/logo-color.png` (324KB), `assets/logos/logo-head.png` (80KB), and `assets/images/tapis-global-logo.png` (692KB) have **zero references** anywhere in the repo's HTML, CSS, or JS (verified by exhaustive grep across all three file types, including background-image CSS rules). `tapis-global-logo.png` was very likely intended for the Tapis Global case-study card before Phase A rewrote that card as text-only honest copy with no logo image. Since these files are never requested by a real visitor, they cost nothing in page-load performance — they're dead repository weight, not a live-site problem — so removing them is a judgment call (they may be intentionally kept for future re-use) and is left as a P2 recommendation rather than deleted.

`og-default.png` (1200×630, 148KB) is used correctly at its actual Open Graph/Twitter-Card display size and is not oversized for its purpose.

## 11. Structured Data Audit (Part 10)

All 50 pages' JSON-LD blocks parse without error (verified via `json.loads` on every `<script type="application/ld+json">` block found). Types in use: `Organization`, `ProfessionalService`, `ImageObject`, `WebSite`, `BreadcrumbList`, and (blog) `BlogPosting`/`Blog`. **Zero pages carry `AggregateRating`, `Review`, or any rating/award schema** — this was the direct target of Phase A's trust cleanup and remains true after this phase's edits; the two new `blog/index.html` `BlogPosting` entries added for the two newly-visible blog posts use only verifiable fields (headline, description, dates, URL, and `author: {"@type":"Organization","name":"TAPIS DIGITECH"}`, since no individual author is known for those two posts) and add no rating of any kind.

## 12. Internal Linking Map (Part 11)

Built a full inbound-link graph from the 50 pages' actual `<a href>` tags (resolving relative paths). Results:

- **Zero broken internal links.** An initial automated pass flagged 9 "broken" links, all of which turned out to be false positives — external LinkedIn/Twitter/WhatsApp share URLs that embed the site's own canonical URL as a query parameter (e.g. `https://www.linkedin.com/sharing/share-offsite/?url=https://www.tapisdigitech.com/...`), which a naive substring check misclassified. Manually confirmed these are legitimate external share links; the real broken-internal-link count is zero.
- **One true orphan:** `search.html`, which is intentional (noindex utility page, reached via the search box UI, not meant to be link-discoverable).
- **Weakly-linked pages (exactly 1 inbound link):** the 7 Global Markets country pages (all linked once, from `global-markets.html`), the 3 author bio pages (linked from their own posts), and — **before this phase's fix, this would have been zero inbound links (a true orphan)** — the two new blog posts, which now have exactly 1 inbound link each from `blog/index.html`'s grid.
- **Finding (documented, not force-fixed):** the three *older* blog posts are richly cross-linked — 7–8 inbound links each, from relevant service/industry pages and their author's bio page (e.g. `blog/cloud-migration-guide.html` is linked from `cloud-it.html`, `finance.html`, `software-development.html`, and `authors/sneha-nair.html`). The two new posts only have their `blog/index.html` grid link. Adding matching contextual links from relevant service/industry pages would bring them in line with their peers, but choosing *which* pages should link to them is an editorial call about topical relevance, not a mechanical fix — left as a P2 recommendation rather than added here, in keeping with the instruction not to add unnatural link volume.
- **Zero generic anchor text** ("click here", "read more" used as the entire link text) found anywhere.

## 13. Analytics Architecture (Parts 12–13)

**Confirmed before building anything:** there was no real GA4 or GTM implementation anywhere in the repository — only a dead, non-executing HTML comment (see below). No Measurement ID or Container ID has been invented anywhere in this codebase; every ID field defaults to an empty string and the site is fully functional with analytics unconfigured (verified: `assets/js/analytics.js` was checked with `node --check`, and a live-browser test loaded every page with no console errors and no network requests to any Google domain when `GTM_CONTAINER_ID` is empty).

**Architecture built, GTM-first per your stated preference:**

- New file `assets/js/analytics.js`, loaded on all 50 pages (and in `build.py`'s template, so future generated pages get it automatically), immediately before `main.js`.
- `window.TDX_ANALYTICS_CONFIG.GTM_CONTAINER_ID` — a single string, empty by default. **This is the only thing that needs to be set to go live.**
- The GTM bootstrap snippet only executes `if (gtmId)` — with the ID unset, zero external requests are made and the file only sets up `window.dataLayer` and the tracking helpers described below.
- GA4 itself is **not** hard-coded anywhere in this codebase, by design — per your stated preference, GA4 is configured as a tag *inside* GTM once a container exists, so there is exactly one place (`GTM_CONTAINER_ID`) to fill in, and no risk of double-counting from two independent GA4 snippets.

**Exact setup steps (to go live, when ready):**
1. Create a GTM container in Google Tag Manager; note its ID (format `GTM-XXXXXXX`).
2. Inside that GTM container, add a GA4 Configuration tag with your GA4 Measurement ID, triggered on "All Pages".
3. In `assets/js/analytics.js`, set `GTM_CONTAINER_ID: 'GTM-XXXXXXX'` (the real ID).
4. Deploy. Verify using GTM's own Preview mode (Tag Assistant), which will show the container loading and the events described in Section 14 firing as `dataLayer` pushes.
5. Do **not** also add a separate `gtag('config', 'G-XXXXXXX')` snippet anywhere — GA4 should be configured only inside GTM, to avoid double-counting page views.

## 14. Conversion Event Architecture (Part 14)

Implemented in `assets/js/analytics.js` via a single delegated click listener (so it keeps working with any dynamically-added content) plus a hook in `main.js`'s existing form-submission handler:

| Event | Fires on | Params |
|---|---|---|
| `phone_click` | any `tel:` link | `page_location`, `page_title` |
| `email_click` | any `mailto:` link | `page_location`, `page_title` |
| `whatsapp_click` | any `wa.me`/`api.whatsapp.com` link | `page_location`, `page_title` |
| `book_consultation_click` | CTA text matching "book/consultation/discovery call/schedule a demo" | `page_location`, `page_title`, `cta_location` |
| `get_quote_click` | CTA text matching "quote/proposal/estimate" | `page_location`, `page_title`, `cta_location` |
| `contact_page_cta_click` | any `.btn` on `contact.html` not already classified above | `page_location`, `page_title`, `cta_location` |
| `contact_form_submit` + `generate_lead` | contact form's genuine server-confirmed success (never optimistic) | `page_location`, `page_title`, `lead_source: 'contact_form'` |
| `newsletter_signup` | newsletter form's genuine server-confirmed success | `page_location`, `page_title` |

`cta_location` is derived from DOM position (`header`/`footer`/`.cta-band`/`body`), not hard-coded per page. **No password, PII, or form message content is ever sent** — verified by reading the actual event-construction code and by a live end-to-end test (Section 17) inspecting `window.dataLayer` after a real submission, which contained only the fields listed above.

## 15. Future Tools Event Architecture (Part 15)

Reserved, not built: `window.tdxTrackTool(stage, toolName, extraParams)` in `assets/js/analytics.js`, which will emit `tool_start`, `tool_complete`, `tool_result_view`, or `tool_cta_click` (from `stage`) with a `tool_name` param (e.g. `ai_roi_calculator`, `ai_readiness_assessment`, `website_cost_calculator`) plus whatever extra params a future tool needs. No calculator or tool was built in this phase — this is purely the naming contract so Phase C's tools can call one existing function instead of inventing their own event schema.

## 16. Forms Audit (Part 16)

Re-verified end-to-end with a live PHP server and a real headless-Chromium browser, specifically to confirm the new analytics hook introduces no regression:

- **Real failure path** (SMTP unconfigured in this sandbox, exactly as it would be misconfigured in a real outage): `contact.php` correctly returns a failure JSON, the UI shows *"Sorry, we couldn't send your enquiry..."*, and — critically — **`window.dataLayer` stayed empty**. No false `contact_form_submit`/`generate_lead` event fired on failure, confirming the analytics hook correctly inherits the "never claim success without genuine server confirmation" gate already built into `contact.php` and `main.js`.
- **Success path** (server response mocked to a genuine-shaped success JSON, since this sandbox has no real SMTP credentials): the UI showed the correct thank-you message, the form fields were reset, and `window.dataLayer` received exactly two events — `contact_form_submit` and `generate_lead` — with only `page_location`/`page_title`/`lead_source`, no name/email/message content.
- **Newsletter form**, same success test: fired exactly one `newsletter_signup` event, correct confirmation message shown.
- **Zero console errors** in either path, on either form.
- Client-side validation (required-field highlighting), the honeypot field (`company_url`, off-screen/`tabindex="-1"`, unrelated to and unaffected by the analytics change), and the "Sending..." disabled-button state were all exercised and behaved as before — nothing in the existing backend or validation logic was touched in this phase.

## 17. Performance Audit (Part 17)

**Explicitly not chased for its own sake, per your instruction:** no animation was removed or throttled, no library was swapped, and no change here was made "to raise a Lighthouse number" — every change below is tied to a concrete, verified byte-count or tap-target measurement.

- **JS:** `main.js` 14.5KB, `analytics.js` 5KB (new, this phase). No external JS dependency of any kind — verified zero `<script src="https://...">` pointing off-domain anywhere in the codebase.
- **CSS:** one file, `assets/css/style.css`, 57.8KB — a moderate size for a 50-page site with this much shared component styling; not flagged as a problem.
- **Images — fixed:** `logo-light.png` re-encoded from 1774×887 (230KB) to 400×200 (35.7KB), see Section 10. This is the single highest-impact fix available, since the file loads on all 50 pages.
- **Images — documented, not changed:** three unused logo/case-study assets totaling ~1.1MB of dead repository weight (Section 10) — no live-page performance impact since they're never requested, but worth cleaning up. `og-default.png` (148KB, 1200×630) is correctly sized for its Open Graph/Twitter-Card purpose.
- **What this audit cannot verify:** an actual Lighthouse/PageSpeed score, real-world Core Web Vitals, or server response-time/TTFB on the live Hostinger deployment. Nothing in this document should be read as a Lighthouse score claim — none was run, because this sandbox has no access to the live site or to Google's PageSpeed API.

## 18. Mobile SEO/UX Audit (Part 18)

Tested with a real headless Chromium browser at two mobile viewports (iPhone SE 375×667, iPhone 14 390×844) across `index.html`, `contact.html`, `services.html`, `ai-development-india.html`, and `case-studies.html`:

- **Viewport meta tag:** present and correct (`width=device-width, initial-scale=1, viewport-fit=cover`) on all 50 pages — verified, zero exceptions.
- **Horizontal overflow:** zero — `document.documentElement.scrollWidth` matched `clientWidth` exactly on every page/viewport combination tested.
- **Mobile navigation:** the hamburger menu opens/closes correctly (`aria-expanded` toggles, `#mobileMenu` becomes visible), and its 9 links each have an ample tap target (measured 327×61.5px).
- **Finding (fixed):** the hamburger button itself measured **36×28px** — below the ~44×44px minimum tap-target size recommended by WCAG 2.5.5 and both Apple's and Google's mobile guidelines. Fixed by increasing its CSS padding (`6px` → `14px 10px`), which changes only the invisible clickable hit-area, not the icon's visual appearance — verified with a before/after screenshot comparison (pixel-identical icon, larger surrounding tap zone) and a live re-test confirming the menu still opens correctly and now measures 44×44px. This only affects the mobile burger (the rule lives inside the same media query that already hides it above 900px width) — desktop layout is untouched.
- **Forms on mobile:** the contact form's required fields and submit button (277×53px) are comfortably tappable at 375px width; no overlap or cramping observed. (One form field measured under 36px tall in the raw scan — this was the intentionally off-screen honeypot field, `x: -9970px`, which real visitors never see; not a bug.)
- **Zero console errors** on any page/viewport combination tested.

No layout was changed to "improve" a mobile score — the only code change in this section is the single-property tap-target padding fix above, which is a genuine accessibility bug fix, not a redesign.

## 19. Priority Summary (Part 20)

**P0 — none found.** No indexing damage, no duplicate/broken canonical, no broken tracking, and no trust/security regression was present at the start of this phase or introduced by it. (The `seo_hardening.py` guard bug described in the Executive Summary would have become a real P0 — silently missing analytics on 2 of 50 pages, forever, on every future deploy — but it was caught and fixed before this branch was ever pushed, so it is listed here as a caught-and-resolved issue, not an open one.)

**P1 — high-impact, implemented this phase:**
- Keyword-stuffed title/description on `ai-development-india.html` (Section 3)
- Missing OG/Twitter tags on all 7 Global Markets pages (Section 3/10)
- Two orphaned blog posts invisible in `blog/index.html`'s grid and schema (Section 12)
- 8 pages missing from `sitemap-pages.xml` (Section 6)
- Oversized sitewide logo asset, 230KB→35.7KB across all 50 pages (Section 10/17)
- Mobile burger-menu tap target below accessibility minimum (Section 18)
- Dead fake-GTM-ID comment on 35 pages, replaced with a pointer to the real config (Section 13)
- No analytics/conversion-tracking architecture at all — now built safe-by-default (Sections 13–14)

**P1 — high-impact, recommendation only (business judgment required):**
- Global Markets thin/templated content — enrich, consolidate, or leave as-is (Section 8)

**P2 — useful, not urgent, recommendation only:**
- Cross-link the two new blog posts from relevant service/industry pages, matching the older posts' linking pattern (Section 12)
- Remove or repurpose 3 unused image assets (~1.1MB dead weight: `logo-color.png`, `logo-head.png`, `tapis-global-logo.png`) (Section 10)
- Expand `sitemap-images.xml` beyond the homepage's 2 images, if richer image search visibility is a goal (Section 6)

---

## 20. Known Limitations

This sandbox cannot: query Google Search Console (the ~63/~64 indexed/not-indexed figures are exactly what you supplied, unchanged and unextended); run a real Lighthouse or PageSpeed Insights audit against the live site; verify actual GTM/GA4 behavior without a real, live Container ID; or confirm how Hostinger's production environment (as opposed to this session's local PHP server) actually serves the site. Every fix in this document was verified against the repository's own files and a local simulation of the CI pipeline, not against the live tapisdigitech.com deployment.

## 21. Phase C Readiness

The foundation this phase set up — a working, safe-by-default analytics config and a documented event contract — is what Phase C's planned tools (ROI calculator, AI-readiness assessment, etc.) need before they can report usage. Recommended before starting Phase C: decide on the Global Markets consolidation question (Section 8), since new Tools-hub pages will add more entries to the same internal-linking structure being discussed there, and get a real `GTM_CONTAINER_ID` configured and verified in GTM Preview mode so Phase C's `tool_start`/`tool_complete` events land somewhere real from day one instead of only in the in-memory `dataLayer`.
