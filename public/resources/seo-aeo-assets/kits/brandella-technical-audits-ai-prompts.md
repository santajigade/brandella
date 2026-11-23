# Technical Audits: AI prompt pack

From Brandella Journal, free to use. Full guide: https://brandella.in/resources/seo-aeo-assets/technical-audits/

Replace the parts in [square brackets] before you paste a prompt into ChatGPT, Claude or Gemini. Always check the output against real data.

## 1. Explain a Search Console report

```
Here is a screenshot description or export of my Search Console [Page indexing / Crawl Stats / Core Web Vitals] report: [paste].
Explain in plain words what it shows, which numbers are normal, which are a problem, and what I should check first on my site.
```

## 2. Read a crawl export

```
Here is a crawl export with URL, status code, indexability, canonical, meta robots and click depth: [paste up to 200 rows].
Group the problems by type, count the URLs in each group and tell me which 5 groups matter most for Google and why.
```

## 3. Diagnose an indexing drop

```
My indexed pages dropped from [number] to [number] between [date] and [date]. Recent changes: [releases, plugin updates, CDN or firewall changes].
List the 8 most likely technical causes in order, how to confirm each one, and which Search Console report shows it.
```

## 4. Review my robots.txt

```
Here is my robots.txt: [paste]. My important sections are [list]. Check it against Google's rules: supported fields, the most specific group
rule, blocked CSS or JavaScript, blocked important sections and the sitemap line. Also list every AI bot it names and what each rule does.
```

## 5. Redirect map check

```
Here is my redirect list (old URL, new URL, status code): [paste]. Find chains, loops, temporary redirects used for permanent moves and
redirects to the home page. Give me a clean one hop map.
```

## 6. Canonical conflicts

```
Here are URLs with their canonical, sitemap status and the internal link URL most pages use: [paste]. Find every page where these do not
agree, and tell me which URL should win for each and why.
```

## 7. Soft 404 finder

```
Here are URLs that return 200 with their title, word count and main text start: [paste]. Which look like empty, error or thin pages that
Google could treat as soft 404s? Suggest 404, 410, noindex, redirect or improve for each.
```

## 8. JavaScript rendering gap

```
Here is the raw HTML of my page [URL]: [paste view source] and here is the text of the rendered page: [paste]. List the content, links and meta
tags that only exist after JavaScript runs, and rate how much each matters for Google and for AI crawlers that do not run JavaScript.
```

## 9. Core Web Vitals plan

```
My [template] pages have LCP [x] s, INP [y] ms and CLS [z] at the 75th percentile on mobile. The page uses [CMS, theme, main scripts, hero image].
Give me the 6 most likely causes and fixes in order of impact, with how a developer can confirm each one.
```

## 10. Size an issue

```
Issue: [describe]. It appears on [URL pattern]. My site has [number] URLs in that section and these Search Console numbers: [paste].
Estimate how many URLs are affected, how much traffic is at risk, and the effort to fix (S, M, L or XL) with your reasoning.
```

## 11. Write a developer ticket

```
Write a developer ticket for this SEO issue: [issue, example URL, URLs affected, severity]. Include a short title, what is wrong, why it matters
in one sentence, the exact change needed, acceptance criteria that can be tested, and how to validate after release.
```

## 12. Explain an issue to a manager

```
Explain this technical SEO issue to a non technical manager in 5 sentences: [issue]. Say what it costs if we wait, what the fix involves and
how long it takes. No jargon.
```

## 13. Bot protection check

```
Our CDN or firewall is [provider] with these bot rules: [paste or describe]. Our Crawl Stats report shows [paste numbers]. Could these rules be
blocking or challenging Googlebot or AI search bots? Tell me what to check in the logs and how to allow verified crawlers safely.
```

## 14. AI bot policy

```
Our goals: [for example be cited in AI search, but not used for model training]. Here is our robots.txt: [paste]. For GPTBot, OAI-SearchBot,
ChatGPT-User, ClaudeBot, Claude-SearchBot, Claude-User, PerplexityBot, Perplexity-User and Google-Extended, say what each one is for and
whether our current rules match our goals. Only use what the vendors' own documentation says, and tell me to check it.
```

## 15. Snippet controls audit

```
Here are the meta robots and X-Robots-Tag values found on my pages: [paste URL and value]. Which ones limit snippets (nosnippet, max-snippet,
data-nosnippet) or indexing, and which pages should I change so they can appear in search snippets and AI features?
```

## 16. Migration risk review

```
We plan to [migrate domain / change CMS / change URL structure] on [date]. Here is our plan: [paste]. List the technical SEO risks, the checks to run
before, on the day and after launch, and what to monitor for 4 weeks.
```

## 17. Monthly audit summary

```
Here are this month's audit numbers: health score [x] (last month [y]), area scores [paste], open issues by priority [paste], overdue [n].
Write a short monthly summary for the team: what improved, what got worse, the 3 priorities for next month.
```

## 18. Workflow 1 of 5: brief the assistant

```
You are my technical SEO auditor. My site: [domain], built on [CMS or framework], [number] URLs, main templates: [list]. Hosting and CDN: [details].
Severity rules: Critical blocks crawling or indexing of important pages, High hurts many URLs, Medium is waste or weak signals, Low is hygiene.
Confirm, then wait for my audit results.
```

## 19. Workflow 2 of 5: explain the failing checks

```
Here are my failed and warning checks with the evidence I found: [paste check ID, check, result, evidence]. For each one, explain in plain words what is
wrong, the most likely cause on my platform, and what I should confirm before I log it.
```

## 20. Workflow 3 of 5: size each issue

```
Here are the section sizes and 28 day impressions for my templates: [paste]. For each issue you explained, estimate URLs affected, the section, the
effort (S, M, L or XL) and the owner (SEO, Developer, Content, Hosting or IT). Show your reasoning briefly.
```

## 21. Workflow 4 of 5: pressure test

```
Review your list. Remove false alarms, merge issues that share one root cause, and flag anything where the fix could break something else.
Tell me which 3 issues you are least sure about and how to confirm them.
```

## 22. Workflow 5 of 5: rows for Excel

```
Turn the final list into rows with tabs between columns for my Issue Log: Check ID, Issue found, Example URL, Section or template, URLs affected,
URLs in the section, Impressions (28 days), Severity override (blank unless needed), Effort, Owner, Status (Open), Found on ([today's date]).
```
