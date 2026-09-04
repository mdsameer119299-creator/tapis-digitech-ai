# Production Deployment Alignment

## What's wrong

Production (`https://www.tapisdigitech.com/`) is not serving `main`. Content
fingerprinting against a dozen independent, page-specific markers (exact
robots.txt text, hero-stat labels, testimonial names, footer heading level,
CSS custom-property values, Font Awesome subset size, presence/absence of
Phase D accessibility fixes, and more) matches production to
`origin/seo-responsive-lead-gen-2026-08` at its tip, not to `main`.

That branch diverged from `main`'s lineage before Phase A began. It has
never received Phase A's trust-content corrections, Phase B's SEO/analytics
work, Phase C's conversion work, or Phase D's performance/accessibility
fixes — it evolved independently, picking up its own SEO-hardening
auto-commits and its own contact-form/SMTP fixes along the way.

## Why: there is no deployment pipeline in this repository

This was confirmed by inspecting the repository directly, not assumed:

- No `vercel.json`, `netlify.toml`, `.vercel/`, or any other
  platform-deploy config file exists anywhere in the repo.
- The only GitHub Actions workflow (`.github/workflows/seo-hardening.yml`)
  triggers exclusively on pushes to `seo-responsive-lead-gen-2026-08`. It
  restores `index.html`/`search.html` from `origin/main`, reruns
  `seo_hardening.py`, and commits the result back to that same branch. It
  does not build, deploy, or touch any hosting platform — it is a content
  script, not a deploy step.
- `.htaccess`'s own header comment says: *"production Apache hardening for
  Hostinger — keep this file in the project root (public_html) when
  deploying."* Apache + `public_html` is Hostinger's shared-hosting
  convention, not a platform with a git-based CI/CD pipeline by default.
- `README.md` describes deployment as "upload the whole folder to any
  static host" — a manual step.
- `package_project.sh` exists specifically to zip the project for manual
  upload; there is no equivalent script that pushes to any hosting API.

**Conclusion: deployment to production is a manual, human-driven upload to
Hostinger** (via FTP or the Hostinger File Manager), not something the
repository's own configuration controls. There is no repo-side file this
task can safely edit to make production start serving `main` — creating a
`vercel.json` or similar would be inventing infrastructure that doesn't
exist and has no evidence of ever being used, which the governing
instructions for this task explicitly prohibit.

## What actually needs to happen (requires the business owner / a human with hosting access)

One of the following, depending on how the live site is actually
configured in Hostinger's hPanel (this repo cannot confirm which, since
hPanel configuration isn't stored in git):

1. **If Hostinger's "Git" auto-deploy feature is enabled** (hPanel →
   Websites → your site → Advanced → Git): its configured source branch is
   almost certainly still `seo-responsive-lead-gen-2026-08`. Someone with
   hPanel access needs to repoint it at `main` (or whatever branch is
   intended to be the production source of truth going forward) and trigger
   a fresh deploy.
2. **If deployment is plain FTP/File Manager upload**: someone needs to
   download the current `main` branch (e.g. via GitHub's "Download ZIP", or
   `package_project.sh` run against a `main` checkout) and upload it to
   `public_html`, replacing the currently-live files.

Either path is an operational action outside this repository and outside
what this environment has credentials or access to perform. No DNS change,
no hosting migration, and no new deployment architecture is being proposed
here — the existing Hostinger destination is very likely still correct;
only the *source* it's pulling from (or was last uploaded from) needs
correcting.

## After the fix

Once whichever of the above is done, production should be re-verified
against `main`'s current tip using the same content-fingerprinting
technique that diagnosed this issue in the first place (see the
"Production Alignment Report" for the specific markers to check), since
"deploy succeeded" messages from a hosting panel are not, on their own,
evidence that the public domain is serving the new code.
