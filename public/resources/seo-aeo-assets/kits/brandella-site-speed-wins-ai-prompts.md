# Site Speed Wins: AI prompt pack

From Brandella Journal, free to use. Full guide: https://brandella.in/resources/seo-aeo-assets/site-speed-wins/

Replace the parts in [square brackets] before you paste a prompt into ChatGPT, Claude or Gemini. Always check the output against real data.

## 1. Explain a PageSpeed Insights report

```
Here is a PageSpeed Insights report for [URL] on [mobile or desktop]: [paste field data and the main diagnostics]
Explain in plain language which Core Web Vitals pass or fail at the 75th percentile, what is causing each failure,
and the 3 fixes most likely to help. Do not invent numbers that are not in the report.
```

## 2. Read the LCP breakdown

```
My LCP element is [image, text or video] and the LCP breakdown is: time to first byte [ms], resource load delay [ms],
resource load duration [ms], element render delay [ms]. Compare each part with the guideline shares
(about 40%, under 10%, about 40%, under 10%), name the part that is furthest over, and list the fixes for that part.
```

## 3. Make the LCP image discoverable

```
Here is the HTML for my page header and hero area: [paste HTML]
Find out whether the LCP image is in the initial HTML, lazy loaded, set as a CSS background or built by JavaScript.
Rewrite the markup so the image is discoverable early with fetchpriority high, without lazy loading.
```

## 4. Find render blocking resources

```
Here is the head section of my page: [paste head]. List every stylesheet and script that blocks rendering,
say which ones can use defer or async, which CSS could be inlined because it is small, and what to load later.
```

## 5. TTFB and caching plan

```
My site runs on [CMS or framework] with [hosting or CDN]. TTFB at p75 is [ms] on [template].
Suggest a caching plan: which pages can be cached at the edge and for how long, what must never be cached,
and how to stop URL parameters like utm tags from bypassing the cache.
```

## 6. Find long tasks behind a slow INP

```
This is a DevTools Performance trace summary (or my own notes) for the interaction "[click or tap]" on [page]: [paste]
Split the delay into input delay, processing duration and presentation delay. Point to the long tasks
(over 50 ms) and suggest where to yield to the main thread.
```

## 7. Break up a long event handler

```
Here is my event handler code: [paste JavaScript]. It runs when a user [action] and makes INP slow.
Rewrite it so the visual update happens first and non urgent work runs after yielding to the main thread.
Keep the behaviour the same and explain each change.
```

## 8. Tag manager clean up

```
Here is the list of tags in my tag manager with what each one does: [paste list]
Group them into keep, review and remove. Flag tags that fire on every page but are needed only on some pages,
and tags that could load after the page is interactive.
```

## 9. Third party script audit

```
These third party scripts load on [template]: [paste list with sizes if known]. For each one, say whether it can
be removed, delayed until interaction (a facade), loaded later, or must stay. Note the likely effect on INP and LCP.
```

## 10. Find layout shift causes

```
CLS on [template] is [value] at p75. The page has [ads, embeds, banners, web fonts, images without sizes].
List the most likely causes of layout shifts in order, how to confirm each in DevTools, and the fix for each.
```

## 11. Reserve space for ads and embeds

```
My [ad slot, video embed or widget] loads after the page and pushes content down. Its usual sizes are [sizes].
Write the CSS that reserves space for it on mobile and desktop without leaving large empty gaps.
```

## 12. Image optimization plan

```
Here is a list of the largest images on [template] with file type, size in KB and displayed width: [paste list]
Suggest the right format (WebP or AVIF), target file size, srcset widths and which images should be lazy loaded.
```

## 13. Web font plan

```
My site loads these fonts: [paste font families, weights and hosts]. Suggest how to cut the number of files,
which font to preload, the font-display value to use and how to reduce layout shifts when the font swaps.
```

## 14. Back and forward cache check

```
Chrome says my page is not eligible for the back and forward cache for these reasons: [paste reasons].
Explain each reason in plain words and what a developer must change to fix it.
```

## 15. Server rendering decision

```
My [template] builds its main content with client side JavaScript using [framework]. Explain the trade offs of
server rendering, static generation and prerendering for this page, the likely effect on LCP, and how to make the
main text and links visible in the initial HTML for crawlers that do not run JavaScript.
```

## 16. Estimate effort for a fix list

```
Here are speed fixes for my site: [paste fixes]. Our stack is [stack] and our team is [team size].
Give each fix an effort of S (under a day), M (a few days), L (one to two weeks) or XL (a project),
and a one line reason. Flag any fix that needs design or business approval.
```

## 17. Explain speed work to a manager

```
Write a short update for my manager about our site speed work. Data: [paste dashboard numbers].
Explain in plain language what passed, what failed, what we shipped, what we are waiting to measure and what is next.
No jargon without a one line explanation.
```

## 18. Workflow 1 of 5: brief the assistant

```
You are my web performance assistant. My site: [site and business]. Stack: [CMS, framework, hosting, CDN].
Main templates: [list]. Goal: pass Core Web Vitals on mobile for the templates with the most visits.
Confirm you understand, then wait for the next step.
```

## 19. Workflow 2 of 5: read the data

```
Here is p75 field data per template and device: [paste table with LCP, INP, CLS, TTFB and visits].
Rate each metric as good, needs improvement or poor (LCP 2.5 s and 4 s, INP 200 and 500 ms, CLS 0.1 and 0.25),
and rank the templates by how much traffic is affected.
```

## 20. Workflow 3 of 5: find causes

```
For the worst three templates, here are the LCP breakdowns and diagnostics: [paste].
Name the main cause for each failing metric, using the LCP parts, long tasks and layout shift sources.
```

## 21. Workflow 4 of 5: pick fixes

```
Pick the fixes for these causes from this list of fix IDs: [paste Fix Library IDs and names].
For each fix give the template, effort (S, M, L or XL) and confidence (High, Medium or Low), and say why.
```

## 22. Workflow 5 of 5: tickets for Excel

```
Turn the fixes into a table I can paste into my Speed Wins tab, with these columns separated by tabs:
Fix ID, Fix or task, Template and device, Effort, Confidence, Owner. Then write acceptance criteria for each fix
that a developer can test, and say which validation method to use.
```
