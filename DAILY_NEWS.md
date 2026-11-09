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

## Google quality rules (apply to every post)
These follow Google Search Central guidance: helpful people-first content, E-E-A-T, the spam policies (scaled content abuse, site reputation abuse) and Google News best practices.
- People first: write for marketers who need to act, not for keywords. Ask: would a reader bookmark or share this? If not, do not publish it.
- Add original value every time: practical steps, a checklist, a comparison table, or a clear explanation of what changed vs before. Never just restate the announcement.
- One story, one article. No near-duplicate pages on the same news, no keyword variants of the same post, no doorway pages.
- Accuracy and trust: facts only from sources you opened, official source linked in the first part of the post, dates and numbers exactly as published, say clearly when something is unconfirmed or a test.
- Honest titles: the title must match the content. No clickbait, no fake urgency, no ALL CAPS, no exaggerated claims.
- Keywords used naturally. No keyword stuffing, no hidden text, no lists of keywords.
- Links: only relevant links. No paid, swapped or irrelevant links; external links only to trustworthy sites.
- Expertise signals: the real author from the rules above (never invent an author), publish date in front matter, and a short note in the text when advice is our recommendation rather than an official statement.
- YMYL caution: no financial, legal or health advice beyond the marketing topic.
- Slow down rather than lower quality: if fewer good stories exist today, publish fewer.

## Self review before publishing
Read each finished post once as an editor and fix it if any answer is no:
1. Does the intro say clearly what happened, when, and who it affects?
2. Is every fact traceable to a linked or opened source?
3. Does the practical section give steps a reader can do today?
4. Is it clearly different from the competitor article that inspired the topic and from our own older posts?
5. Does the title promise exactly what the post delivers?

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

## 5b. In-article infographics (1 or 2 per post)
Santaji asked for related infographics between the paragraphs of every article.
- Write a JSON spec in the scratchpad (not in the repo) and run `python3 scripts/make_infographic.py <spec.json>`. Types: `stats` (2 to 4 key numbers), `compare` (before vs now or feature table, 2 to 6 rows), `steps` (the "what to do now" checklist, 3 to 7 short steps). See the script header for the keys. Name them `<slug>-1`, `<slug>-2`.
- Good default: one `stats` or `compare` graphic right after the intro (before the first `##`), and one `steps` graphic at the start of the practical section.
- Only facts that are already in the article and come from a source opened in this run. Put the source in the `source` line, or "Brandella recommendations" for our own advice. No dashes.
- Insert as Markdown with descriptive alt text (at least 10 characters): `![Alt text describing the graphic](/images/infographics/<slug>-1.webp)`.
- Look at every graphic with the Read tool; fix text that wraps badly or overflows.
- Commit them with the post: also `git add public/images/infographics/<slug>-*.webp`.
- Never use stock photos, photos of real people, or images copied from other sites.

## 6. Check, build, publish
- `python3 scripts/check_post.py <slug1> <slug2> ...` must print OK for every post. Fix every FAIL; read the warnings and fix them where sensible.
- `grep -P "[\x{2013}\x{2014}]" src/content/posts/<slug>.md` must print nothing.
- `npm run build` must pass, and `dist/<slug>/index.html` must exist for each post.
- Commit only the new posts, covers and infographics: `git add src/content/posts/<slugs>.md public/images/covers/<slugs>.webp public/images/infographics/<slug>-*.webp`, message `news: <N> articles <YYYY-MM-DD HH:MM IST>`, then `git pull --rebase` and `git push`.
- Wait for the Deploy to Hostinger run (`gh run list -R santajigade/brandella -L 1`) and confirm it succeeded. If it fails, read the log and fix.

Never edit old posts, the theme, `.htaccess`, workflows or anything under `/tools/` in a news run. If a post cannot pass the checks, leave it out and publish the rest.
