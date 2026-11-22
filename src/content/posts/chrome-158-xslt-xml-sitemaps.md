---
title: "Chrome 158 XSLT Removal: Why XML Sitemaps Look Broken"
slug: "chrome-158-xslt-xml-sitemaps"
date: "2026-11-22T07:00:00+05:30"
author: "santajigade"
categories: ["seo", "technical-seo"]
primaryCategory: "technical-seo"
tags: ["Chrome 158", "XSLT", "XML sitemaps", "WordPress sitemaps", "Technical SEO"]
description: "Chrome 158 XSLT removal means styled XML sitemaps now show as raw code. Why the file still works for crawlers, which plugins are affected and what to do."
focusKeyword: "chrome 158 xslt"
takeaways:
  - "Chrome 158, released November 17, 2026, stopped running XSLT for most users, so styled XML sitemaps now show raw XML."
  - "Chrome removed XSLT for security reasons; it says only about 0.02% of page loads use it."
  - "The sitemap file itself is unchanged. Crawlers read the XML, not the stylesheet."
  - "WordPress core, Yoast, Rank Math and AIOSEO sitemaps are affected in different ways; check Search Console before changing anything."
image: "/images/covers/chrome-158-xslt-xml-sitemaps.webp"
imageAlt: "Chrome 158 XSLT removal and unstyled XML sitemaps"
format: "md"
---

The Chrome 158 XSLT removal is why your XML sitemap suddenly looks like a wall of code. Google's Chrome team planned to remove XSLT "from version 158 (November 17, 2026)", according to its developer guide [Removing XSLT for a more secure browser](https://developer.chrome.com/docs/web-platform/deprecating-xslt). From that release, XSLT stops working on Chrome Stable for everyone except sites in an origin trial and companies using an enterprise policy.

Most XML sitemaps made by WordPress and SEO plugins ship with an XSLT stylesheet that turns the XML into a readable table in the browser. In Chrome 158 that step is skipped. You see raw tags plus a warning, and clients start emailing that the sitemap is broken.

It isn't. The XML is the same file it was last week. Only the browser view changed, and that matters for how you answer clients and what you fix.

![Chrome 158 XSLT removal: key dates and numbers from Chrome](/images/infographics/ig-chrome-158-xslt-xml-sitemaps-1.webp)

## Why Chrome removed XSLT

Chrome's guide says keeping XSLT 1.0 in browsers "presents a significant and unnecessary security risk". The feature runs on [libxslt](https://github.com/GNOME/libxslt), which Chrome describes as one of several complex, aging C and C++ codebases prone to memory safety bugs. The guide cites CVE-2025-7425 and CVE-2022-22834 as examples.

Usage is tiny. Chrome's [usage data](https://chromestatus.com/metrics/feature/timeline/popularity/79) puts XSLT at about 0.02% of page loads, and pages using the XSLT processing instruction at under 0.001%. The guide also says Firefox and WebKit have indicated plans to remove XSLT from their engines.

Two things are not going away. Chrome says "we won't be removing XML from the browser", and CSS stylesheets attached to raw XML with `type="text/css"` keep working.

## The Chrome 158 XSLT timeline

| Chrome version | Date | What happened |
|---|---|---|
| Chrome 143 | December 2, 2025 | Official deprecation, warnings in console and Lighthouse |
| Chrome 146 | March 10, 2026 | Enterprise policy available for testing |
| Chrome 152 | August 25, 2026 | Origin trial opens to keep XSLT past removal |
| Chrome 158 | November 17, 2026 | XSLT stops working on Stable for most users |
| Chrome 176 | August 17, 2027 | Origin trial and enterprise policy end, XSLT off for everyone |

So for most sites the visual change is permanent. The origin trial only buys time until August 2027.

## Does this hurt crawling or rankings?

The stylesheet was only ever a display layer for people. A crawler fetching your sitemap reads the `<loc>` and `<lastmod>` entries in the XML itself. [Search Engine Journal](https://www.searchenginejournal.com/your-wordpress-sitemap-isnt-broken-chrome-158-has-dropped-xslt/597549/), which first looked at the WordPress impact, puts it plainly: "Search engines do not use XSLT."

That fits how sitemaps work. If you want proof for a client, open the Sitemaps report in Google Search Console and check that the status still reads Success. We cover what sitemaps do for discovery in [what an XML sitemap is in the AI search era](/what-is-xml-sitemap-ai-search-era/).

## Which WordPress sitemaps are affected

Search Engine Journal's Dan Taylor checked the main WordPress setups. His findings, with the official links:

| Sitemap source | URL | Status in Chrome 158 |
|---|---|---|
| WordPress core | `/wp-sitemap.xml` | Raw XML; [Trac ticket 65593](https://core.trac.wordpress.org/ticket/65593) removes the XSLT in WordPress 7.2 |
| Yoast SEO | `/sitemap_index.xml` | Version 28.9 swaps XSLT for pure CSS; it was still a release candidate on November 17 ([release notes](https://yoast.com/release-notes/)) |
| Rank Math | plugin sitemap | Raw XML; users raised it in a [support thread](https://wordpress.org/support/topic/xslt-deprecation-warning-on-rank-math-xml-sitemap-in-google-chrome/) on November 4 |
| All in One SEO | plugin sitemap | Raw XML, no alternative stylesheet announced |

Rank Math users should also keep the plugin current for security reasons; see our roundup of [Rank Math vulnerabilities in 2026](/rank-math-vulnerabilities-2026/). WordPress 7.2 itself is due on December 8, and we explain the rest of that release in the [WordPress 7.2 field guide](/wordpress-7-2-field-guide/).

## What to do now

![What to do now about Chrome 158 and XML sitemaps](/images/infographics/ig-chrome-158-xslt-xml-sitemaps-2.webp)

1. Don't edit or regenerate a sitemap just because it looks unstyled. The file crawlers read has not changed.
2. Check Search Console. Open Indexing, then Sitemaps, and confirm each submitted sitemap still shows Success and a recent read date.
3. Brief clients and colleagues before they find it themselves. One line works: Chrome 158 stopped styling XML in the browser, and search engines never used the styling.
4. Update plugins when fixes ship. Watch for Yoast 28.9 and WordPress 7.2, and check your SEO plugin's changelog.
5. Give people an HTML sitemap if they need a readable page. Our guide to [HTML sitemap vs XML sitemap](/html-sitemap-vs-xml-sitemap-difference/) explains when that helps.
6. If you built your own styled sitemap or feed, move the transform to the server. Chrome recommends server-side XSLT that sends HTML, a JavaScript library such as SaxonJS, or a WASM polyfill. For RSS and Atom feeds, it suggests linking them from your HTML pages with `<link rel="alternate" type="application/rss+xml">`. If you generate sitemaps in code, our [PHP sitemap generator tutorial](/build-xml-sitemap-generator-php/) shows the plain XML you actually need.
7. For WordPress core sitemaps, Search Engine Journal suggests a small must-use plugin that returns false for the `wp_sitemaps_stylesheet_url` and `wp_sitemaps_stylesheet_index_url` filters to stop the warnings. It notes WordPress 7.2 deprecates both filters, so remove that file after you update.

This is our recommendation, not an official Google statement: treat the change as cosmetic for SEO and spend the time on real sitemap problems, such as missing URLs or wrong `lastmod` dates.

## FAQ about the Chrome 158 XSLT change

### Is my XML sitemap broken in Chrome 158?

No. Chrome no longer applies the XSLT stylesheet, so you see raw XML instead of a table. The file and its URLs are unchanged.

### Will Google stop reading my sitemap?

Nothing in Chrome's announcement affects how crawlers fetch sitemaps. Check the Sitemaps report in Search Console, where the status should still read Success.

### Can I bring the styled view back?

For your own sites, Chrome points to server-side transforms, JavaScript libraries or a polyfill. The origin trial and enterprise policy only work until Chrome 176 on August 17, 2027.

### Are Firefox and Safari removing XSLT too?

Chrome's guide says the Firefox and WebKit projects have indicated plans to remove XSLT. It gives no dates for those browsers.
