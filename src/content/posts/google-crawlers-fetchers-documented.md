---
title: "Google Crawlers and Fetchers: 12 More Bots Now Documented"
slug: "google-crawlers-fetchers-documented"
date: "2026-11-26T17:40:00+05:30"
author: "santajigade"
categories: ["seo", "technical-seo"]
primaryCategory: "technical-seo"
tags: ["Google crawlers", "User-triggered fetchers", "robots.txt", "Server logs", "Googlebot"]
description: "Google crawlers and fetchers docs now list 12 more existing bots, including pageburst, GoogleDocs and PageSpeed Insights. Here is how to spot them in your logs."
focusKeyword: "google crawlers and fetchers"
takeaways:
  - "Google added 12 existing crawlers and user-triggered fetchers to its crawling documentation, with pages last updated on November 23, 2026."
  - "Six are special-case crawlers, such as pageburst for Google Ads and GoogleDocs for IMPORTHTML, and each one ignores robots.txt rules."
  - "Six are user-triggered fetchers, including PageSpeed Insights, Google-Apps-Script and GoogleImageProxy, which generally ignore robots.txt because a user asked for the fetch."
  - "APIs-Google moved from the special-case list to the user-triggered list."
  - "Use the user agent strings and Google's IP range JSON files to label this traffic in logs and firewall rules."
image: "/images/covers/google-crawlers-fetchers-documented.webp"
imageAlt: "Google crawlers and fetchers documentation update"
format: "md"
---

Google has added 12 crawlers and fetchers to its official list of Google crawlers and fetchers. The [special-case crawlers page](https://developers.google.com/crawling/docs/crawlers-fetchers/google-special-case-crawlers) and the [user-triggered fetchers page](https://developers.google.com/crawling/docs/crawlers-fetchers/google-user-triggered-fetchers) both show "last updated 2026-11-23 UTC", and the [crawling documentation changelog](https://developers.google.com/crawling/docs/changelog) records the change.

None of these bots are new. [PPC Land](https://ppc.land/google-documents-12-existing-bots-that-ignore-robots-txt/), which reported the update first, quotes Google calling them clients that are "not new" and says Google documented them because they are high volume and people had asked about them.

If you run a website, some of these user agents are probably already in your server logs. Until now you couldn't match them to a Google product in Google's own docs, so some got blocked as unknown bots and some got mistaken for Googlebot.

![Google crawlers and fetchers update: 6 special-case crawlers added, 6 user-triggered fetchers added, 1 fetcher moved, pages updated November 23, 2026](/images/infographics/ig-google-crawlers-fetchers-documented-1.webp)

## The six new special-case crawlers

Special-case crawlers do one job for one Google product. Google says they "may ignore robots.txt rules and so they operate from a different IP range than the common crawlers." Each of the six new entries says it ignores robots.txt rules.

| Crawler | What it does |
|---|---|
| Google-analytics-postbacks | Sends Google Analytics attribution postback requests to ad network endpoints when conversion events happen |
| Google-Calendar-Importer | Fetches and refreshes external .ics calendar feeds that Google Calendar users subscribe to |
| GoogleDocs | Powers Google Sheets functions such as IMPORTHTML that fetch data from a URL the user enters |
| Google-Edu | Verifies institutional domains for Google Workspace for Education applications |
| pageburst | Renders web pages for Google Ads quality, landing page safety and page understanding |
| PlayStore-Google | Fetches and validates the URLs developers submit in Google Play Store app listings |

pageburst matters most for advertisers. Google says it ignores robots.txt and is also unaffected by crawling preferences. It sends a desktop user agent and a mobile one, and both contain the token "pageburst". AdsBot, AdsBot Mobile Web, Google-Safety and Mediapartners-Google are still on the same page. For background on how Google Ads rates landing pages, see our [Google Ads Quality Score guide](/google-ads-quality-score-explained/).

## The six new user-triggered fetchers

User-triggered fetchers run because a person did something, like opening an email or running a test. Google's rule for the whole group is: "Because the fetch was requested by a user, these fetchers generally ignore robots.txt rules."

| Fetcher | When it visits your site |
|---|---|
| AppEngine-Google | An app on the App Engine Standard Environment requests your URL through the URL Fetch service |
| Google-Apps-Script | A user's script calls UrlFetchApp to fetch an external URL or API |
| Google-Cloud-Tasks | Cloud Tasks dispatches a queued HTTP request or scheduled webhook to an endpoint |
| GoogleImageProxy | Someone opens an email or document with an image embedded from your site, for example in Gmail |
| Google Web Preview | Someone shares your URL in a product such as Google Classroom and a link preview is built |
| PageSpeed Insights (Chrome-Lighthouse) | Someone runs a PageSpeed Insights audit on your page |

The PageSpeed Insights entry clears up a common log question. Its mobile and desktop user agents end in "Chrome-Lighthouse", so a burst of those hits usually means somebody, maybe your own team or an agency, has been [testing your Core Web Vitals](/how-to-measure-core-web-vitals-tools-guide/).

## APIs-Google moved lists

APIs-Google is no longer on the special-case crawlers page. It now appears with the user-triggered fetchers, where Google says it "delivers webhook push notifications configured by developers in Google Cloud and Google Workspace APIs, such as Pub/Sub push subscriptions and Google Drive resource change notifications." PPC Land also reports that its user agent string was corrected to include a semicolon.

If you filter logs or firewall rules on the exact old APIs-Google string, check the current one on the user-triggered fetchers page and update your rule.

## How to verify Google crawlers and fetchers in your logs

Don't trust a user agent alone, because anyone can fake one. Google publishes separate IP range files for each group:

- special-crawlers.json for special-case crawlers
- user-triggered-fetchers.json, user-triggered-fetchers-google.json and user-triggered-agents.json for user-triggered fetchers

Reverse DNS helps too. Special-case crawlers resolve to hosts like rate-limited-proxy-\*\*\*-\*\*\*-\*\*\*-\*\*\*.google.com. User-triggered fetchers resolve to \*\*\*-\*\*\*-\*\*\*-\*\*\*.gae.googleusercontent.com or google-proxy-\*\*\*-\*\*\*-\*\*\*-\*\*\*.google.com. We covered why a reverse DNS check can be too weak on its own in [our post on verifying Googlebot](/verify-googlebot-reverse-dns-google-cloud/).

## What site owners should do now

![Checklist for the Google crawlers and fetchers update: search logs for the new names, label them, check IP ranges, review firewall blocks, update the APIs-Google rule](/images/infographics/ig-google-crawlers-fetchers-documented-2.webp)

These are our recommendations, not instructions from Google.

1. Search the last 30 days of server logs for the 12 names in the tables above. Our [Python log file analysis guide](/python-log-file-analysis-googlebot-crawl-behavior/) shows how to group hits by user agent.
2. Label each one by product (Ads, Analytics, Workspace, Play, PageSpeed) so your crawl reports stop lumping them in with Googlebot.
3. Check the source IPs against the matching JSON file before you treat any hit as genuine.
4. Review your WAF and bot rules. If you block pageburst or GoogleImageProxy as unknown bots, ad landing page checks or email images may break.
5. Don't try to manage these bots with robots.txt. Google says they ignore it, so use server rules if you really need to limit one. Our [robots.txt guide](/robots-txt-complete-guide/) explains what the file can and cannot control.
6. Update any rule that matches the old APIs-Google string.

## FAQ about Google crawlers and fetchers

### Are these new Google bots?

No. Google calls them existing clients. The November 23, 2026 update only documents them.

### Can I block pageburst with robots.txt?

No. Google says pageburst ignores robots.txt rules and is unaffected by crawling preferences.

### Do these fetchers affect my rankings?

Google does not say they do. They serve products such as Ads, Analytics, Sheets and PageSpeed Insights, not Google Search indexing.

### Where do I find the IP ranges?

On the special-case crawlers and user-triggered fetchers pages, which link to special-crawlers.json and the three user-triggered JSON files.
