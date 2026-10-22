# Central Ohio Window Guide

Homeowner resource for smart shades and window treatments in Columbus and Central Ohio.
Static site in `public/`, deployed on Netlify (pushes to `main` auto-deploy).

Live at https://centralohiowindowguide.com

## Design (Oct 2026 editorial edition)
- Sister palette to olssonss.com: ivory `#faf7f0`, ink `#2e2a25`, gold `#b08d3c`; Cormorant Garamond + Jost.
- `style.css` holds every style; `site.js` builds the "In this guide" list, scroll reveals and reading bar.
- Article photos live in `public/images/editorial/` (Norman manufacturer photos); real install photos stay in `public/images/`.

## Adding a new article
Copy any article folder (e.g. `public/sunroom-window-treatments-ohio/`), keep the masthead/footer markup,
and change the kicker, h1, dek, hero photo, body and schema. Add it to `sitemap.xml`, `llms.txt` and the homepage index.
`tools/redesign.py` was the one-time converter from the old layout; don't re-run it on converted pages.
