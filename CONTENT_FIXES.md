# Content fixes queue (posts Google crawled but did not index)

Source: Search Console "Crawled - currently not indexed" export, 2026-11-17. One item per day (Santaji, 2026-11-17). A scheduled task takes the first unchecked item, does it, ticks it and adds the date.

Rules for every item: follow `SEO_CHECKLIST.md`, keep the slug and URL, never use em or en dashes (also remove any in the old text), research current facts with web search and link official sources inside sentences, add `takeaways` and an FAQ section, update `updated` and `words`, add one contextual link to the post from an older related post, run `npm run build`.

- [x] Merge `https-migration-seo-impact` into `migrate-from-http-to-https` (301 in the manual block of `public/.htaccess`). Done 2026-11-17.
- [x] Add internal links to `python-and-pandas-seo-reporting` and `copy-to-clipboard-button-javascript`. Done 2026-11-17.
- [ ] Expand `ai-for-seo-artificial-intelligence` (809 words, thin) into a complete, current guide of about 2,000 words: what AI does for SEO in 2026 (research, content briefs, technical audits, AI Overviews and AI Mode), practical workflows with example prompts, risks and Google's guidance on AI generated content, a tools table. Check it does not duplicate other AI SEO posts (`python3 scripts/list_posts.py find ai seo`); give it a distinct angle.
- [ ] Expand `understanding-digital-marketing` (939 words, overlaps `digital-marketing-tips-2026`) into a definitive beginner guide of about 2,000 words: what digital marketing is, each channel with a table (what it is, best for, key KPI, starting budget), how channels work together in a funnel, AI's role in 2026, a 90 day starter plan. Keep it clearly different from the tips post (definition and overview, not tips) and link to it.
- [ ] Refresh `ai-in-ppc-should-advertisers-be-worried` (November 2025, 1,144 words) for 2026: current Google Ads AI features (AI Max, Performance Max reporting, AI Overviews ads), what advertisers still control, a practical checklist, and sources. About 1,800 words.
