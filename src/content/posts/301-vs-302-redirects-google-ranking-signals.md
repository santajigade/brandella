---
title: "301 vs 302 Redirects: Which One Passes Ranking Signals"
slug: "301-vs-302-redirects-google-ranking-signals"
date: "2026-11-09T08:40:00+05:30"
author: "santajigade"
categories: ["seo", "technical-seo"]
primaryCategory: "technical-seo"
tags: ["redirects", "canonicalization", "technical SEO"]
description: "301 vs 302 redirects: Google's Gary Illyes says only a 301 passes ranking signals to the new URL. What that means and how to audit your redirects today."
focusKeyword: "301 vs 302 redirects"
takeaways:
  - "Google's Gary Illyes explained that a 301 redirect passes ranking signals to the new URL, while a 302 keeps the old URL in results."
  - "Google indexes a page whichever redirect type is used, but only a permanent redirect signals that the target should be canonical."
  - "Google treats 301 and 308 as permanent and 302, 303 and 307 as temporary, with 307 and 308 keeping POST data intact."
  - "Google prefers server side redirects and calls JavaScript redirects a last resort because they may never be seen if rendering fails."
  - "A 302 still suits genuinely temporary moves, but many platforms default to 302, so permanent moves often end up temporary by accident."
image: "/images/covers/301-vs-302-redirects-google-ranking-signals.webp"
imageAlt: "301 vs 302 redirects and Google ranking signals"
format: "md"
---

The 301 vs 302 redirects question comes up in almost every site migration, and Google has given a clear answer again. In a discussion between Google's Gary Illyes and Cherry Prommawin, reported by [Search Engine Journal](https://www.searchenginejournal.com/google-explains-how-redirects-affect-ranking-signals/595967/) on November 5, 2026, Illyes explained that a 301 passes ranking signals from the old URL to the new one, while a 302 does not.

That lines up with Google's official [redirects and Google Search documentation](https://developers.google.com/search/docs/crawling-indexing/301-redirects), which says a permanent redirect is a signal that the target should be canonical, while a temporary redirect is not.

This affects anyone who changes URLs: site migrations, HTTPS moves, slug changes, merged articles and retired product pages. Picking the wrong redirect type will not stop a page from being indexed, but it can decide which URL Google shows and where the signals end up.

## What Google said about 301 vs 302 redirects

According to Search Engine Journal's report of the conversation:

- Google will index a page whichever redirect type you use. The choice mainly affects which URL appears in results.
- Google groups similar pages into clusters and picks one canonical URL. Both 301 and 302 redirects help with that clustering, but only the 301 has a canonicalization effect.
- A 301 passes ranking signals to the new URL. With a 302, Illyes said, Google keeps the old URL in results and largely ignores the new one.
- 307 and 308 are the modern equivalents of 302 and 301. The key difference is that they keep submitted POST data, such as form data, intact during the redirect.
- Google prefers server side redirects over JavaScript or meta refresh redirects, which are slower and need the browser to do more work.

## How Google classifies each redirect type

Google's documentation sorts redirects into permanent and temporary. This table summarizes it.

| Redirect | Google treats it as | Shown in results |
|---|---|---|
| HTTP 301, 308 | Permanent | Usually the new URL |
| Meta refresh or HTTP refresh with 0 second delay | Permanent | Usually the new URL |
| JavaScript location redirect | Permanent, if Google renders it | Usually the new URL, but rendering can fail |
| HTTP 302, 303, 307 | Temporary | Usually the old URL |
| Meta refresh or HTTP refresh with a delay | Temporary | Usually the old URL |

Google says server side redirects are the most reliably understood, and calls JavaScript redirects a last resort because Google may never see them if rendering fails. Its advice is to use a permanent server side redirect, 301 or 308, whenever a URL change is lasting.

Google's guide to [consolidating duplicate URLs](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls) ranks redirects as the strongest canonical signal, ahead of rel canonical, with sitemap inclusion as a weak signal. That is why redirects are the right tool for retiring duplicate pages. Our [canonical tag explainer](/what-is-canonical-tag/) covers when a canonical tag is the better choice.

## When a 302 is still the right choice

None of this makes 302 a bad redirect. Google's documentation says temporary redirects suit short term situations, such as a service being briefly unavailable, because the original URL keeps its place in results.

Good uses include a temporary sale page, a page under maintenance, or a location or language redirect that should not replace the main URL. The mistake is using a 302 for a move you never plan to undo. Many platforms and plugins default to 302, so permanent moves often end up temporary by accident.

## How to audit your redirects today

These steps are Brandella's recommendations based on the guidance above.

1. **List every redirect.** Crawl your site with an SEO crawler and export all 3xx responses, or pull them from your server config or redirect plugin.
2. **Mark each as permanent or temporary.** Ask one question for each: will this old URL ever come back? If not, it should be a 301 or 308.
3. **Fix permanent moves sent as 302 or 307.** These are the ones most likely to leave the old URL in results and keep signals from moving. Change them at the server level. If you manage redirects in code, our [redirect manager in PHP](/redirect-manager-in-php/) guide shows one way to do it.
4. **Remove chains.** Point each old URL straight to its final destination instead of hopping through several redirects. Fewer hops also help crawling, as covered in [crawl budget explained](/crawl-budget-explained/).
5. **Replace JavaScript and delayed meta refresh redirects** with server side redirects where you can.
6. **Update internal links and sitemaps.** Link to the final URL directly and list only final URLs in your sitemap, so all signals point the same way.
7. **Check Search Console.** Use URL Inspection on a few old and new URLs to see which one Google picked as canonical.

## A note on old URLs showing up

Even with a correct 301, Google's documentation says it may sometimes still show the old URL as an alternate name for the canonical URL. It calls this normal after a domain move and says it typically fades over time. So do not panic and switch redirect types if an old URL appears for a while after a move.

The rule to remember is simple: permanent move, permanent redirect. Use 301 or 308 for lasting changes, keep 302 and 307 for genuinely temporary ones, and keep your [canonical tags](/canonical-tag-implementation-guide/) pointing at the same final URLs.
