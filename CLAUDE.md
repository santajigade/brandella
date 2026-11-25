# Brandella Journal (brandella.in) static site

Astro static site that replaced the WordPress install in November 2026. Owner: Santaji (non technical, wants short answers).

## Hard rules
- Never use em dash or en dash characters in any text written for the site.
- Every old WordPress URL must keep working: posts at `/<slug>/`, categories at `/category/<parent>/<child>/` (note `html_css` and `html_js` use underscores).
- `/tools/` belongs to the separate repo santajigade/brandella-tools. This site must never output anything under `/tools/`; rsync excludes it and never uses `--delete`.
- Never redirect an old post URL to the home page. Redirects for old slugs live in the generated block in `public/.htaccess`.

## Content
- Every article (news or evergreen, new or updated) must follow `SEO_CHECKLIST.md`.
- Posts: `src/content/posts/<slug>.md`. Front matter keys: title, slug, date, updated, author, categories, primaryCategory, tags, description, focusKeyword, image, imageAlt, words, views, format.
- `format: html` means the body is raw HTML (migrated BX FORMAT posts with their own `<style>` and `<script>`), passed through untouched. New posts can use `format: md`.
- Categories and descriptions: `src/data/categories.json` (descriptions from `scripts/category_descriptions.py`).
- Re-running `python3 scripts/migrate_wxr.py export.xml` regenerates posts, pages, categories, `scripts/wp_images.txt` and the htaccess redirect block from a WordPress export.

## Build and deploy
- `npm run build` outputs `dist/`. Push to `main` runs `.github/workflows/deploy.yml` (rsync over SSH to Hostinger). Deploy is skipped until `HOST_FINGERPRINT` in the workflow and the `SSH_KEY` secret are set.
- `fetch-images.yml` (manual, one time) downloads images from the live WordPress site into `public/wp-content/uploads/`, makes card thumbnails in `public/thumbs/`, commits and redeploys.
- Logo and icons: `scripts/make_logo.py` then `scripts/make_icons.py`.
- Article pages auto load up to 6 next articles, each in a same origin iframe (`html.embed` mode hides site chrome), so BX scripts never clash.

## Daily news
- Scheduled runs publish news posts by following `DAILY_NEWS.md` (Markdown posts, `format: md`, covers from `scripts/make_cover.py`, checks with `scripts/check_post.py`, duplicate checks with `scripts/list_posts.py`).

## Push alerts (same tool as topabcnews.com)
- Max 1 notification per day. `.github/workflows/push.yml` runs at 11:45 IST and sends the best post from the last 24 hours (`scripts/send_push.mjs`, category priority inside). Manual run: Actions > Daily push notification (mode `init` only sets up keys).
- Browser side: `public/push.js` (click only prompt: margin bell on wide screens plus footer "Daily alerts" link, nothing auto opens, close remembered in localStorage `brj_push_off`; never in embed iframes), `public/sw.js`, `public/api/subscribe.php` (the only PHP allowed by `.htaccess`).
- Subscribers and VAPID keys live on the server outside the web root: `domains/brandella.in/push-data/`. Never commit them.

## Newsletter signup
- `src/components/Newsletter.astro` (banner on every article, hidden in embed iframes) posts to `public/api/newsletter.php`.
- Emails are saved to `domains/brandella.in/newsletter-data/subscribers.csv` on the server, outside the web root (columns: email, subscribed_at_ist, page). Santaji downloads it from Hostinger File Manager and opens it in Excel. Never commit it.
- Only `subscribe.php` and `newsletter.php` may run PHP (`public/.htaccess` and `public/api/.htaccess`).

## Free SEO and AEO assets library
- `/resources/` and `/resources/seo-aeo-assets/` (hub of 36 assets). `src/data/seo-assets/index.json` lists all 36; an asset goes live when `src/data/seo-assets/<slug>.yaml` exists, otherwise its card shows "Coming soon". Never link to an asset page that is not live.
- Pages: `src/pages/resources/`; loader `src/lib/assets.ts`; styles `src/styles/assets.css` (`ra-` prefix).
- Every asset is a FULL KIT (Santaji, 2026-11-17: simple templates are "no use"). Quality bar = `keyword-research.yaml` + `scripts/assets/kit_keyword_research.py`:
  - `time` (shown as "Time to use") must be plain: "About 2 hours to set up, then about 1 hour a month to update" or "About 10 minutes for each page" (Santaji, 2026-11-24).
  - YAML with `kit: true`, `tabs` (workbook tab count shown on the download card, default 8), `kitContents`, long AI era guide in `sections` (reference tables, worked example, column guide, 30 day plan, mistakes), 7 steps, 20+ prompts incl. a chained workflow, 12 to 16 checklist items, 6 FAQs, real sources (official Google docs first, every fact from a source you opened). No em or en dashes.
  - `scripts/assets/kit_<slug_with_underscores>.py` with `build(path, asset, url)`, `PREVIEW` and `check(wb)`: a multi tab Excel workbook (Start Here, main sheet with 500 formula rows and dropdowns, Dashboard, a planning tab, Settings, AI Prompts, Checklist, Sources) with a worked demo for a fictional company. Use `scripts/assets/kitlib.py`. Only Excel 2007 era functions plus `_xlfn.MAXIFS/MINIFS/IFS/SWITCH/TEXTJOIN`.
  - Build: `RECALC=<xlsx skill>/scripts/recalc.py python3 scripts/assets/build_kits.py` (needs LibreOffice, openpyxl, pyyaml, Playwright). It writes the workbook, PDF guide, PDF checklist, prompts .md, the kit ZIP and the all kits ZIP into `public/resources/seo-aeo-assets/kits/` and a preview JSON into `src/data/seo-assets/previews/`. Zero formula errors required. Commit the generated files.
- Release pace (Santaji, 2026-11-17): only 2 new kits per day, so the library does not look like scaled content. A scheduled task does this Monday to Friday at 14:13 IST (Santaji, 2026-11-25).

## Pinterest
- New posts reach Pinterest automatically from `/rss.xml` (each item carries its cover image).
- Older posts: `python3 scripts/make_pins.py --start YYYY-MM-DD` makes 1000x1500 pins in `public/pins/<slug>.jpg` and bulk upload CSVs in `pinterest/` (4 pins a day, 56 rows per file because Pinterest only accepts publish dates within 14 days). Boards: SEO Tips and Strategies, Google Ads and PPC, AI in Marketing, Digital Marketing and Content, Web Development Tips. The 50 newest posts (already in the feed) are skipped.

