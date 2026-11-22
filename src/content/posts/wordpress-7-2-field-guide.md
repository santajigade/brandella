---
title: "WordPress 7.2 Field Guide: What Site Owners Should Check"
slug: "wordpress-7-2-field-guide"
date: "2026-11-22T07:05:00+05:30"
author: "santajigade"
categories: ["development", "php"]
primaryCategory: "php"
tags: ["WordPress 7.2", "WordPress", "random redirect", "Secrets API", "WordPress release"]
description: "WordPress 7.2 is due December 8, 2026. The field guide lists a new /random/ redirect, database and jQuery changes, and the Secrets API was pulled late."
focusKeyword: "wordpress 7.2"
takeaways:
  - "WordPress 7.2 is scheduled for December 8, 2026, the last major release of the year."
  - "The field guide counts more than 440 Core Trac tickets, 21 new hooks and 2,947 changed files since 7.1.4."
  - "A new /random/ endpoint redirects visitors to a random published post; the wp_enable_random_content_redirect filter turns it off."
  - "The planned Secrets API was removed from 7.2 on November 17, and jQuery 4 is not included."
image: "/images/covers/wordpress-7-2-field-guide.webp"
imageAlt: "WordPress 7.2 field guide and release checklist"
format: "md"
---

WordPress 7.2 is scheduled for release on December 8, 2026, according to the [WordPress 7.2 release page](https://make.wordpress.org/core/7-2/) on Make WordPress Core, which calls it the final major release of 2026. Release Candidate 1 shipped on November 17, and on November 20 release coordinator David Baumwald published the [WordPress 7.2 Field Guide](https://make.wordpress.org/core/2026/11/20/wordpress-7-2-field-guide/), the developer summary of what changes.

If you run WordPress sites for clients, this is the document to read before the update lands on your hosts. A few changes touch URLs, redirects and database settings, which is where SEO and plugin trouble usually starts.

The scale is large. The guide counts "more than 440 Core Trac tickets", about 150 of them enhancements and over 260 bug fixes, plus about 700 Gutenberg enhancements and nearly 500 Gutenberg bug fixes.

![WordPress 7.2 by the numbers from the field guide](/images/infographics/ig-wordpress-7-2-field-guide-1.webp)

## WordPress 7.2 release dates

| Milestone | Date |
|---|---|
| Beta 1 | October 20, 2026 |
| Release Candidate 1 | November 17, 2026 |
| Field Guide published | November 20, 2026 |
| Dry run and 24 hour code freeze | December 7, 2026 |
| WordPress 7.2 release | December 8, 2026 |

More release candidates are listed between RC1 and the dry run. The release page says enhancement patches will not be committed after the posted dates, so what is in the field guide is close to final.

## The new /random/ redirect

The change most likely to surprise site owners is under the Rewrite API. The field guide says "WordPress 7.2 introduces a new `/random/` endpoint that redirects visitors to a randomly selected published post." It works across eligible post types, taxonomies and author archives, and the random URL base can be changed in Permalink Settings.

Developers get three controls: a new `randomable` argument in `register_post_type()` to opt a custom post type in or out, a `wp_enable_random_content_redirect` filter to switch the feature off, and a `wp_is_random_content_query()` helper.

[Search Engine Journal](https://www.searchenginejournal.com/wordpress-7-2-seo-ai-changes/597616/), citing the original developer note, reports that the redirect is a 302, is on by default with no dashboard switch, and sends `X-Robots-Tag: noindex, follow` on the redirect response only. It also reports that the random pick does not skip posts an SEO plugin has set to noindex, and that sites behind a page cache or CDN may see a cached 404 at `/random/` until caches are purged. If you want a refresher on how temporary redirects are treated, read our explainer on [301 vs 302 redirects](/301-vs-302-redirects-google-ranking-signals/).

## Other WordPress 7.2 changes worth knowing

- Database: `NO_BACKSLASH_ESCAPES` joins the incompatible SQL modes that WordPress disables by default through `wpdb::set_sql_mode()`.
- jQuery: jQuery Migrate moves to 3.6.0. WordPress 7.2 does not include jQuery 4, which is tentatively targeted for 7.3.
- Media: client-side media processing works in Chromium 137 and later, while Firefox and Safari fall back to server-side processing.
- Admin: the admin bar and menu switch from Dashicons glyphs to SVG icons.
- Blocks: a new `textShadow` block support arrives with Light and Strong presets.
- REST API: the comments `status` parameter is now an array, and revision metadata is limited to registered revision meta.
- Sitemaps: Trac [ticket 65593](https://core.trac.wordpress.org/ticket/65593) removes the XSLT stylesheet from core sitemaps, which Chrome 158 already stopped rendering. Our post on the [Chrome 158 XSLT removal](/chrome-158-xslt-xml-sitemaps/) explains why that is cosmetic.

The [Roadmap to 7.2](https://make.wordpress.org/core/2026/09/18/roadmap-to-7-2/) also lists Ipsum, a minimal new default theme, and a suggestion mode for Notes in the editor.

## What was cut late

The Secrets API, a planned way to store credentials such as API keys, was removed from 7.2 on November 17, according to Search Engine Journal. It reports design questions and a finding that the capability checks were never enforced. Its developer note had been published on November 11, so anyone who built against it from the beta should check their code.

Collaborative editing is also not part of 7.2, the roadmap says.

## What to do now before WordPress 7.2

![What to do now before updating to WordPress 7.2](/images/infographics/ig-wordpress-7-2-field-guide-2.webp)

These are our recommendations for agencies and site owners.

1. Make sure every site is on 7.1.5 first. That release fixed a batch of security issues, covered in our [WordPress 7.1.5 security release](/wordpress-7-1-5-security-release/) post.
2. Test RC builds on a staging copy, never on production, with your real theme and plugins.
3. Decide whether you want `/random/`. If not, add the `wp_enable_random_content_redirect` filter in a must-use plugin before the update. Check that no existing page already uses the slug `random`.
4. Purge your page cache and CDN after updating, then load `/random/` to confirm it behaves as you expect.
5. Ask plugin vendors about the database change and the jQuery Migrate update, especially for older form, slider and page builder plugins.
6. If your code used the Secrets API from the betas, remove that dependency.
7. After the release, keep auto updates and security monitoring on. Our post on [Gootloader SEO poisoning](/gootloader-seo-poisoning-fbi-wordpress/) shows why unpatched WordPress sites are a target.

## FAQ about WordPress 7.2

### When is WordPress 7.2 released?

The official schedule lists December 8, 2026, after a dry run and 24 hour code freeze on December 7.

### Can I turn off the /random/ redirect?

Yes. The field guide names the `wp_enable_random_content_redirect` filter for disabling it. Custom post types can opt out with the `randomable` argument.

### Is the Secrets API in WordPress 7.2?

No. Search Engine Journal reports it was removed on November 17, 2026, during the release candidate phase.

### Does WordPress 7.2 include jQuery 4?

No. The field guide says jQuery 4 is not included and is tentatively targeted for WordPress 7.3.
