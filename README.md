# TAPIS DIGITECH — Website

Production-ready static website for TAPIS DIGITECH, an enterprise AI & digital
transformation company. Multi-page, mobile-first, SEO-optimized and accessible.
No build step required — it is plain HTML/CSS/JS and runs anywhere.

## Quick start
- **View locally:** open `index.html` in a browser, or run a static server:
  ```bash
  python3 -m http.server 8080      # then visit http://localhost:8080
  ```
- **Deploy:** upload the whole folder to any static host (Netlify, Vercel,
  Cloudflare Pages, GitHub Pages, S3 + CloudFront, cPanel). No server runtime needed.

## Project structure
```
TAPIS-DIGITECH/
├── index.html · about.html · services.html · industries.html
├── solutions.html · case-studies.html · resources.html
├── careers.html · contact.html · search.html
├── blog/                       # blog index (index.html) + articles
├── authors/                    # author profile pages (EEAT)
├── assets/
│   ├── css/                    # style.css
│   ├── js/                     # main.js
│   ├── images/                 # content images, og-default.png
│   ├── icons/                  # Font Awesome CSS + subset webfonts
│   ├── fonts/                  # self-hosted Geist + Inter (woff2) + fonts.css
│   ├── documents/              # downloadable PDFs (company profile)
│   ├── logos/                  # brand logos
│   ├── favicons/               # favicon
│   └── videos/                 # (reserved)
├── sitemap.xml                 # sitemap index → pages / blog / images
├── sitemap-pages.xml · sitemap-blog.xml · sitemap-images.xml
├── robots.txt
├── manifest.webmanifest        # PWA / install metadata
├── browserconfig.xml           # Windows tiles
├── llms.txt · humans.txt       # machine + human credits
├── security.txt                # RFC 9116 (also in /.well-known/)
├── README.md · LICENSE
└── package_project.sh          # zips the project
```

## Before going live
1. Set your real domain in canonical/OG/sitemap URLs (currently `www.tapisdigitech.com`).
2. Replace placeholder phone, email and WhatsApp number.
3. Add your analytics container ID (GTM placeholder is in each `<head>`).
4. Connect the contact/newsletter forms to a real handler with server-side validation.
5. Replace illustrative case studies / testimonials / stats with verifiable, attributable proof.

## Notes
- All paths are relative, so the site works from any sub-path and over `file://`.
- Structured data (JSON-LD), Open Graph, Twitter cards and canonicals are per-page.
- Fonts and icons are self-hosted and subset for performance.
