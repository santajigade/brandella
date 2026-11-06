# Daily news playbook (Brandella Journal)

The scheduled task runs twice a day and publishes 5 news articles a day: 3 in the morning run, 2 in the evening run. Follow every step. Quality beats count: publish fewer rather than publish something thin, wrong or duplicated.

## 1. Setup
- `npm ci` and `pip install --break-system-packages pyyaml pillow` if missing.
- `git pull --rebase` first. Today's date and time: use IST (Asia/Kolkata).

## 2. Find stories (last 48 hours, prefer last 24)
Scan what competitors are covering, then go to the primary source:
- Competitor news desks (topic ideas only): searchengineland.com, searchenginejournal.com, seroundtable.com, marketingland style trade press.
- Primary sources (always read and link the official one): Google Search Central blog (developers.google.com/search/blog), Google Search Status Dashboard, blog.google, Google Ads announcements (support.google.com/google-ads/announcements and blog.google/products/ads-commerce), Microsoft Advertising blog, Bing Webmaster blog, Meta newsroom and Meta for Business, LinkedIn Marketing blog, YouTube official blog, TikTok newsroom, OpenAI, Anthropic, Google DeepMind and Perplexity announcements.

Pick the stories (3 or 2, see above) that matter to marketers, spread across different sections (SEO, Paid Media, Content, Social, Digital Marketing, Artificial Intelligence, Development). At most 2 per section per run.

Duplicate check before writing each story:
- `python3 scripts/list_posts.py recent 40` and `python3 scripts/list_posts.py find <key words>`.
- Skip a story already covered unless there is genuinely new information; then write a clearly different follow up angle and link the earlier post.

## 3. Rules for using competitor sites
- Use them only to discover what is newsworthy. Never copy, closely paraphrase or follow the structure of their article.
- Every fact must come from a source you opened in this run, preferably the official announcement. If a detail only exists in one trade outlet's original reporting, link and credit that outlet in the sentence.
- No invented numbers, quotes, dates or rollout details. If something is unconfirmed, say so plainly.

## 4. Write the article
File: `src/content/posts/<slug>.md`, Markdown, front matter exactly like this:

```yaml
---
title: "Google March Core Update Starts Rolling Out: What to Check"
slug: "google-march-core-update-rolling-out"
date: "2026-11-07T09:30:00+05:30"
author: "santajigade"
categories: ["seo", "technical-seo"]
primaryCategory: "technical-seo"
tags: ["Google core update"]
description: "120 to 160 characters, includes the focus keyword, says what happened and why it matters."
focusKeyword: "google march core update"
image: "/images/covers/google-march-core-update-rolling-out.webp"
imageAlt: "Google March core update rollout"
format: "md"
---
```

- `categories`: the top section slug plus at most one subcategory slug from `src/data/categories.json` (for example `["paid-media", "google-ads"]`). `primaryCategory` is the most specific one.
- `author`: `ankush-guleria` when `digital-marketing` is in categories, otherwise `santajigade`.
- `date`: now in IST with `+05:30`.
- Title: focus keyword first, 45 to 65 characters, factual, no clickbait.
- Slug: short, lowercase, contains the focus keyword, max 60 characters.

Body (800 to 1,200 words, plain clear English):
- Intro of 2 or 3 short paragraphs: what happened, who it affects, why it matters. Focus keyword in the first paragraph.
- 4 to 6 story specific `##` headings (never Conclusion, Summary, Final Thoughts, Overview). The focus keyword in at least one heading.
- Always include a practical section such as "What advertisers should do now" or "How to check if your site was hit", with steps or a checklist. This is Brandella's own angle and the main value over competitors.
- A table where it genuinely helps (old vs new, dates, who is affected).
- Paragraphs of 2 or 3 sentences. No H1 in the body.
- Links inside sentences, no Sources or References section:
  - 3 to 6 external links, always including the official announcement.
  - 3 to 5 internal links to existing Brandella articles that genuinely relate (find them with `list_posts.py`). Use relative links like `/crawl-budget-explained/`.
- Absolutely no em dash or en dash characters anywhere. Hyphens inside words are fine.

## 5. Cover image
`python3 scripts/make_cover.py <slug> "<short headline, max about 70 chars>" "<primary category name>" "<top section name>"`
Then look at `public/images/covers/<slug>.webp` with the Read tool. Shorten the headline if it wraps badly.

## 6. Check, build, publish
- `python3 scripts/check_post.py <slug1> <slug2> ...` must print OK for every post. Fix every FAIL; read the warnings and fix them where sensible.
- `grep -P "[\x{2013}\x{2014}]" src/content/posts/<slug>.md` must print nothing.
- `npm run build` must pass, and `dist/<slug>/index.html` must exist for each post.
- Commit only the new posts and covers: `git add src/content/posts/<slugs>.md public/images/covers/<slugs>.webp`, message `news: <N> articles <YYYY-MM-DD HH:MM IST>`, then `git pull --rebase` and `git push`.
- Wait for the Deploy to Hostinger run (`gh run list -R santajigade/brandella -L 1`) and confirm it succeeded. If it fails, read the log and fix.

Never edit old posts, the theme, `.htaccess`, workflows or anything under `/tools/` in a news run. If a post cannot pass the checks, leave it out and publish the rest.
