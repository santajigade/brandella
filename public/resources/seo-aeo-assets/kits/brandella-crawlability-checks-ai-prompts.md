# Crawlability Checks: AI prompt pack

From Brandella Journal, free to use. Full guide: https://brandella.in/resources/seo-aeo-assets/crawlability-checks/

Replace the parts in [square brackets] before you paste a prompt into ChatGPT, Claude or Gemini. Always check the output against real data.

## 1. Explain my robots.txt

```
Here is my robots.txt: [paste]. For each group, list the user agents and the rules. Then tell me, for Googlebot, Bingbot, GPTBot,
OAI-SearchBot, ClaudeBot and PerplexityBot, which group each one follows and what it may not crawl. Remember that only the most
specific matching group applies.
```

## 2. Test URLs against robots.txt

```
Here is my robots.txt: [paste] and these URLs: [paste list]. For Googlebot, say whether each URL is allowed or blocked and which rule
decides it. Use the longest matching path, and the least restrictive rule when an allow and a disallow are the same length.
```

## 3. Write robots.txt for my policy

```
My site: [domain]. Keep these out of crawling: [paths]. Bot policy: allow search and AI search bots, block AI training bots
[or your policy]. Write a clean robots.txt with only user-agent, allow, disallow and sitemap lines, and explain each group.
```

## 4. Find the Googlebot group trap

```
Here is my robots.txt: [paste]. Does any named group (for example Googlebot) lose rules that only exist in the * group? List the
rules each named group is missing and give me corrected groups.
```

## 5. Clean my sitemap

```
Here are the URLs in my sitemap with status code, noindex and canonical: [paste]. List every URL that should not be in the sitemap and
why, and any important URL from this list of pages I want indexed that is missing: [paste].
```

## 6. Fix lastmod logic

```
My CMS sets lastmod like this: [describe]. Here are 20 URLs with lastmod and the real last content change: [paste]. Is our lastmod
accurate? Write the rule a developer should implement so lastmod only changes when the main content changes.
```

## 7. Split a large sitemap

```
My sitemap [name] has [number] URLs and is [size] MB. Here is our URL structure: [describe]. Propose how to split it into files under
50,000 URLs and 50 MB, how to name them and what the sitemap index should look like.
```

## 8. Explain a Page indexing reason

```
Search Console shows [reason, for example Crawled, currently not indexed] for these URLs: [paste with page type and a short summary].
Explain what the reason means, the 5 most likely causes for pages like these, and what to check in URL Inspection.
```

## 9. Crawled or discovered but not indexed

```
These pages are not indexed: [paste URL, title, word count, internal links in, impressions]. Which look like a content quality problem,
which like a discovery problem and which like duplicates? Suggest improve, merge, link, noindex or remove for each.
```

## 10. Noindex, canonical or robots.txt?

```
I want to handle these URL types: [paste list, for example filter URLs, internal search, tag pages, print versions, old campaign pages].
For each, should I use noindex, a canonical, a 404 or 410, a redirect, or a robots.txt disallow? Explain each choice in one line.
```

## 11. Parameter URL plan

```
My site creates URLs with these parameters: [paste examples with ?sort=, ?color=, ?page= and so on]. Which create real unique content,
which are duplicates and which waste crawling? Give me a rule per parameter.
```

## 12. Canonical conflicts

```
Here are URLs with their canonical, status code, sitemap status and how internal links point to them: [paste]. Find every conflict
and tell me which URL should be the canonical for each group.
```

## 13. JavaScript content check

```
Here is the raw HTML of [URL]: [paste view source] and the visible text of the rendered page: [paste]. Which important content, links,
title or meta tags exist only after JavaScript? What should be server rendered first?
```

## 14. AI bot policy

```
Our goals: [for example appear and be cited in AI search, but not be used for training]. Explain the difference between search bots,
training bots and user requested fetchers for OpenAI, Anthropic, Perplexity and Google, and which robots.txt tokens match our goals.
Tell me to confirm every token on each vendor's own crawler page.
```

## 15. Read bot traffic in my logs

```
Here is a summary of my server logs for 30 days: user agent, hits, status codes and top paths: [paste]. Which bots get errors, which
crawl pages they should not, and which important sections they never reach? Remind me to verify bots by IP or reverse DNS.
```

## 16. CDN and firewall check

```
Our CDN or firewall is [provider] with these bot settings: [describe]. Our logs show [403 or challenge counts by user agent]. Could we
be blocking Googlebot or AI search bots we want? What should we change and how do we test it safely?
```

## 17. Migration crawl checks

```
We are moving from [old setup] to [new setup] on [date]. Write the crawlability checks for before launch, launch day and the first
4 weeks: robots.txt, sitemaps, redirects, canonicals, noindex, status codes and Search Console reports.
```

## 18. Workflow 1 of 5: brief the assistant

```
You are my crawlability reviewer. My site: [domain] on [CMS or framework]. URL types I want indexed: [list]. URL types I want kept out:
[list]. Bot policy: [policy]. Only use Google's robots.txt rules: one group per crawler, longest path wins. Confirm, then wait.
```

## 19. Workflow 2 of 5: robots.txt

```
Here is my robots.txt: [paste]. For Googlebot and each bot in my policy, give the group it follows and its effective rules.
List every rule that conflicts with my lists of URLs to index and to keep out.
```

## 20. Workflow 3 of 5: the URL Checker rows

```
Here are my URL Checker rows with URL, should be indexed, indexability, Search Console status, fixes and verdict: [paste]. Group the
problems by root cause (one robots rule, one template, one plugin) and rank the groups by how many important URLs they affect.
```

## 21. Workflow 4 of 5: pressure test

```
For each fix you suggest, tell me what else it could change. Would a robots.txt edit block anything I want indexed? Would a noindex hit
pages that get traffic? Remove or adjust any risky fix.
```

## 22. Workflow 5 of 5: the change list

```
Give me the final change list: the full corrected robots.txt, the sitemap changes, and one row per remaining fix with tabs between
columns: URL or pattern, Problem, Fix, Owner (SEO, Developer, Content or Hosting), How to validate.
```
