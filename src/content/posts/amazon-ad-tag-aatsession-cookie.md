---
title: "Amazon Ad Tag Adds aatSession First-Party Cookie"
slug: "amazon-ad-tag-aatsession-cookie"
date: "2026-11-16T08:00:00+05:30"
author: "santajigade"
categories: ["paid-media", "paid-media-analytics"]
primaryCategory: "paid-media-analytics"
tags: ["Amazon Ads", "Amazon Ad Tag", "first-party cookies", "conversion tracking", "consent"]
description: "The Amazon Ad Tag now sets a first-party aatSession cookie on North American advertiser sites. What it does, how consent works and how to turn it off."
focusKeyword: "amazon ad tag"
takeaways:
  - "Amazon's release notes, dated November 16, 2026, say the Amazon Ad Tag now sets a first-party aatSession cookie in North America."
  - "The cookie links a visitor's events for conversion measurement, and advertisers can turn it off with one line of code."
  - "Per PPC Land, the cookie lasts 30 days after the last page view and only works when consent signals allow it."
  - "Advertisers should update cookie policies and consent banners and decide whether to keep or disable the cookie."
image: "/images/covers/amazon-ad-tag-aatsession-cookie.webp"
imageAlt: "Amazon Ad Tag aatSession first-party cookie"
format: "md"
---

The Amazon Ad Tag now drops a new first-party cookie on advertiser websites. In its [Amazon Ads release notes](https://advertising.amazon.com/API/docs/en-us/release-notes/index#amazon-ad-tag-adds-a-first-party-session-identifier-cookie), in an entry dated November 16, 2026, Amazon says: "In North America, the Amazon Ad Tag now sets a first-party aatSession cookie".

According to the same note, the cookie links a visitor's events for conversion measurement, and advertisers can switch it off with a single line of code. The change happens automatically for sites that already run the tag, so there is no new setup to trigger it.

That makes it a task for two teams at once. Paid media teams get better connected conversion data, while whoever owns privacy and the cookie banner now has a new cookie to list, explain and control.

![Amazon Ad Tag aatSession cookie at a glance](/images/infographics/ig-amazon-ad-tag-aatsession-cookie-1.webp)

## What the Amazon Ad Tag cookie does

The release note links to the session identifier section of Amazon's [Ads Data Manager guide for the Amazon Ad Tag](https://advertising.amazon.com/API/docs/en-us/guides/ads-data-manager/data-sources/amazon-ad-tag/validate-and-share#session-identifier). The finer details below come from [PPC Land's review of that guide](https://ppc.land/amazon-ad-tag-adds-a-30-day-first-party-cookie-to-advertiser-websites/), which first spotted the entry on November 14.

| Detail | What it means |
|---|---|
| Cookie name | aatSession |
| Type | First-party, set on the advertiser's own domain |
| Purpose | Holds a session identifier that links a visitor's events |
| Lifetime | 30 days after the visitor's last page view, extended by each new page view (per PPC Land) |
| Region | North America only; no country list is given (per PPC Land) |
| Consent | Set, read and sent only when consent signals allow it, including TCF, GPP or the Amazon Consent Signal (per PPC Land) |
| Opt out | One line of code in the base tag |

In plain terms, Amazon can now tie a visitor's page views, add to carts and purchases together on your site more reliably. Because the cookie is first-party, it is less exposed to browser limits on third-party cookies. Our explainer on [first-party data and privacy](/data-privacy-and-first-party-data/) covers why advertisers are moving in this direction.

## How to turn off the aatSession cookie

PPC Land reports that the guide gives this opt out line, which goes in the base code on every page, before the first event:

```js
amzn("disableAATSessionCookie", true);
```

Adding it deletes any existing aatSession cookie and stops new ones from being set. One detail is easy to miss: per PPC Land, passing `false` does not turn the cookie back on. To re enable it, you must remove the line completely.

If you load the Amazon Ad Tag through Google Tag Manager, make sure the line runs before any event fires, otherwise the cookie may be set on the first hit. Our list of [common GTM mistakes that break tracking](/common-gtm-mistakes-tracking/) shows how firing order problems usually creep in.

## Consent: what changes for your banner

Amazon's design ties the cookie to consent signals, which is good news. If your consent platform already passes TCF or GPP signals, or you use the Amazon Consent Signal, the cookie should respect those choices.

Still, your cookie policy is now out of date if it lists every cookie by name. Add aatSession, its purpose and its 30 day lifetime. If you are building or reviewing your setup, our guide to [Consent Mode v2 for website owners](/consent-mode-v2-explained-website-owners/) explains how consent signals flow into ad tags in general.

This is our recommendation, not legal advice. If you are unsure what your local privacy rules require, ask your privacy or legal team.

## What advertisers should do now

![Checklist for the Amazon Ad Tag aatSession cookie](/images/infographics/ig-amazon-ad-tag-aatsession-cookie-2.webp)

1. **Confirm where the tag runs.** List every site in North America that uses the Amazon Ad Tag, including landing pages built by agencies.
2. **Check for the cookie.** Open your site in a browser, accept consent and look for aatSession in the developer tools cookie list.
3. **Test the no consent path.** Reject consent and confirm the cookie is not set. If it appears, fix how your consent platform passes signals.
4. **Update your cookie policy.** Add the cookie name, purpose and lifetime so the page matches what the site sets.
5. **Decide keep or disable.** Most advertisers will keep it for better measurement. If your policy bars new cookies without review, add the opt out line until the review is done.
6. **Watch your conversion reports.** Compare Amazon conversion numbers for a few weeks before and after, so you know whether linked sessions change what you see.
7. **Tell finance and the agency.** If reported conversions shift, everyone should know why before budgets for the holiday season are judged on them.

## Why this matters beyond one cookie

Amazon's ad business is already under close watch, as seen in our coverage of the [Amazon Ads FTC lawsuit details](/amazon-ads-ftc-lawsuit-auction-surcharges/). Changes that quietly add data collection to advertiser sites deserve a careful look, even when they are useful. A first-party session cookie gives Amazon better linked signals from your site, which is the stated goal of conversion measurement.

For advertisers, the trade off is simple. Better linked data usually means better optimisation, but only if consent is handled properly. Get the banner and the policy right first, then enjoy the cleaner numbers.

## FAQ about the Amazon Ad Tag cookie

### What is the aatSession cookie?

It is a first-party cookie that the Amazon Ad Tag now sets on advertiser websites in North America. Amazon says it links a visitor's events for conversion measurement.

### How long does the aatSession cookie last?

PPC Land reports it expires 30 days after the visitor's last page view, and each new page view extends it.

### Can I stop the Amazon Ad Tag from setting it?

Yes. Amazon says one line of code turns it off. PPC Land reports the line is `amzn("disableAATSessionCookie", true);` placed in the base code on every page before the first event.

### Does the cookie respect user consent?

Per PPC Land's reading of the guide, it is only set, read and sent when consent signals allow it, including TCF, GPP or the Amazon Consent Signal.
