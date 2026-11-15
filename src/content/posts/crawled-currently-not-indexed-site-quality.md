---
title: "Crawled Currently Not Indexed: Google Points to Site Quality"
slug: "crawled-currently-not-indexed-site-quality"
date: "2026-11-12T07:15:00+05:30"
author: "santajigade"
categories: ["seo", "google-search-console"]
primaryCategory: "google-search-console"
tags: ["Google Search Console", "indexing", "crawled currently not indexed", "John Mueller", "site quality"]
description: "Crawled currently not indexed pages are usually a site quality signal, says Google's John Mueller, and shrinking the site will not fix it. What to do now."
focusKeyword: "crawled currently not indexed"
takeaways:
  - "John Mueller says many crawled or discovered currently not indexed pages usually signal that Google's quality systems are unconvinced about the site."
  - "Mueller said just making the site smaller by noindexing or deleting pages does not significantly raise the site's overall quality."
  - "Discovered currently not indexed means Google found but has not crawled the URL, while crawled means Google fetched it and declined indexing."
  - "Google's crawl budget guide is written mainly for large sites with 1 million or more unique pages, so smaller sites rarely face crawl budget issues."
  - "Site owners should rule out technical causes first, then improve or merge weak pages before pruning, and expect recovery over weeks or months."
image: "/images/covers/crawled-currently-not-indexed-site-quality.webp"
imageAlt: "Crawled currently not indexed pages in Google Search Console"
format: "md"
---

If a large share of your pages show as crawled currently not indexed or discovered currently not indexed in Google Search Console, Google's John Mueller says the cause is usually not technical. In a Bluesky reply around November 10, 2026, he wrote: "Usually this is a sign that Google's quality systems are unconvinced about your site."

The exchange was reported on November 11 by [Search Engine Roundtable](https://www.seroundtable.com/google-crawled-discovered-currently-not-indexed-42507.html), with a link to [Mueller's Bluesky post](https://bsky.app/profile/johnmu.com/post/3mzycywr5vs26). It answered a site owner who asked whether to noindex those pages, redirect them to indexed pages, or simply wait.

Mueller's key point was that pruning alone does not help: "Just making the site smaller doesn't significantly raise the overall quality of the site." That matters for anyone planning a mass noindex or delete project during Google's [November 2026 core update](/google-november-2026-core-update/).

![Crawled currently not indexed: what Mueller said vs common fixes](/images/infographics/ig-crawled-currently-not-indexed-site-quality-1.webp)

## What John Mueller said about crawled currently not indexed pages

The question came from a user named Toren Ajk. According to Search Engine Roundtable, he followed up by asking whether "building more trust signals is more important than optimizing the crawl budget."

Mueller replied: "I think those are very distinct things." He explained that if only a tiny number of a site's pages are indexed, it points either to a severe technical issue, such as crawl budget, which would be noticeable at that scale, or to Google not being convinced about the site overall.

## Crawled vs discovered: what the two statuses mean

Both statuses mean Google knows the URL but chose not to index it. The difference is how far Google got.

| Status | What happened | Usual first check |
|---|---|---|
| Discovered, currently not indexed | Google found the URL but has not crawled it yet | Internal links, crawl capacity, server speed |
| Crawled, currently not indexed | Google crawled the page and decided not to index it | Content value, duplication, overall site quality |

The table reflects general Search Console definitions plus Mueller's comments. For a deep fix list on the first status, see our guide on [how to fix Discovered currently not indexed pages](/discovered-currently-not-indexed-fix/).

## Why pruning alone will not fix it

Many site owners react to a long not indexed list by noindexing or deleting those URLs. Mueller's reply suggests that removes the symptom without changing how Google judges the site.

Search Engine Roundtable's Barry Schwartz added his own reading: if Google crawled a page and still did not index it, Google does not consider that page worth including. Removing weak pages can still be sensible housekeeping, but the remaining pages have to be convincing on their own.

Google's guide to [creating helpful, reliable, people-first content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content) is the best yardstick. It asks questions such as "Does the content provide original information, reporting, research, or analysis?" and "Is the content produced well, or does it appear sloppy or hastily produced?" Run your unindexed pages through those questions honestly before deciding what to keep.

## How to tell a technical problem from a quality problem

Mueller drew a clear line between the two. A severe technical issue is usually obvious at scale, so check that first and rule it out quickly.

- Open the [Crawl Stats report](/understanding-crawl-stats-report/) and look for server errors, slow response times or a sudden drop in crawl requests.
- Inspect a sample of affected URLs with the URL Inspection tool and confirm they return 200, are not blocked and have the right canonical.
- If crawling looks healthy and Google is fetching the pages, the problem is very likely quality, not [crawl budget](/crawl-budget-explained/).

Google's own [crawl budget guide](https://developers.google.com/crawling/docs/crawl-budget) says it is written mainly for large sites with 1 million or more unique pages, medium sites with 10,000 or more pages that change daily, and sites with a large portion of URLs marked Discovered, currently not indexed. Google adds that "These are not exact thresholds." If your site is a few hundred or a few thousand pages, crawl budget is rarely the real issue.

## What to do now if many pages are not indexed

![Crawled currently not indexed checklist: five steps to take](/images/infographics/ig-crawled-currently-not-indexed-site-quality-2.webp)

These steps are Brandella's recommendations based on Mueller's comments, not official Google instructions.

1. **Measure the share.** Export the Page indexing report and calculate what percentage of your submitted URLs are indexed. A few unindexed pages is normal; a majority is a site level signal.
2. **Rule out technical causes first.** Use the checks above. Fix server errors, soft 404s and wrong canonicals before touching content.
3. **Sample and grade the pages.** Read 20 unindexed URLs. Are they thin, near duplicates, auto generated or outdated? Note patterns by template or folder.
4. **Improve or merge, then prune.** Rewrite pages that can become the best answer, merge overlapping ones with redirects, and only then noindex what has no value.
5. **Strengthen the pages that are indexed.** Add internal links from your best performing pages, show real expertise and keep facts current. Track progress in the [Search Console performance report](/search-console-performance-report/).

## How long recovery takes

Mueller did not give a timeline, and Google rarely does. Quality reassessment is gradual, so expect weeks or months, not days, and avoid judging changes while the November core update is still rolling out.

The takeaway is simple: a long crawled currently not indexed list is feedback about the whole site. Fixing it means making the site more useful, not just smaller.
