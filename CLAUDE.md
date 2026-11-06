# Brandella Journal (brandella.in) static site

Astro static site that replaced the WordPress install in November 2026. Owner: Santaji (non technical, wants short answers).

## Hard rules
- Never use em dash or en dash characters in any text written for the site.
- Every old WordPress URL must keep working: posts at `/<slug>/`, categories at `/category/<parent>/<child>/` (note `html_css` and `html_js` use underscores).
- `/tools/` belongs to the separate repo santajigade/brandella-tools. This site must never output anything under `/tools/`; rsync excludes it and never uses `--delete`.
- Never redirect an old post URL to the home page. Redirects for old slugs live in the generated block in `public/.htaccess`.

## Content
- Posts: `src/content/posts/<slug>.md`. Front matter keys: title, slug, date, updated, author, categories, primaryCategory, tags, description, focusKeyword, image, imageAlt, words, views, format.
- `format: html` means the body is raw HTML (migrated BX FORMAT posts with their own `<style>` and `<script>`), passed through untouched. New posts can use `format: md`.
- Categories and descriptions: `src/data/categories.json` (descriptions from `scripts/category_descriptions.py`).
- Re-running `python3 scripts/migrate_wxr.py export.xml` regenerates posts, pages, categories, `scripts/wp_images.txt` and the htaccess redirect block from a WordPress export.

## Build and deploy
- `npm run build` outputs `dist/`. Push to `main` runs `.github/workflows/deploy.yml` (rsync over SSH to Hostinger). Deploy is skipped until `HOST_FINGERPRINT` in the workflow and the `SSH_KEY` secret are set.
- `fetch-images.yml` (manual, one time) downloads images from the live WordPress site into `public/wp-content/uploads/`, makes card thumbnails in `public/thumbs/`, commits and redeploys.
- Logo and icons: `scripts/make_logo.py` then `scripts/make_icons.py`.
- Article pages auto load up to 6 next articles, each in a same origin iframe (`html.embed` mode hides site chrome), so BX scripts never clash.
