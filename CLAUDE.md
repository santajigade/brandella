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
