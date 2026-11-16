---
title: "Google Merchant Center Outage on November 6: What to Check Now"
slug: "google-merchant-center-outage-november-6"
date: "2026-11-08T17:45:00+05:30"
author: "santajigade"
categories: ["paid-media", "google-ads"]
primaryCategory: "google-ads"
tags: ["Google Merchant Center", "Shopping ads", "Merchant API", "product feeds"]
description: "The Google Merchant Center outage on November 6 hit Merchant API and feeds for 8.5 hours. What happened and a checklist to confirm your products are fine."
focusKeyword: "google merchant center outage"
takeaways:
  - "A Google Merchant Center outage on November 6, 2026 affected Merchant Center, the Merchant API and Feeds from 04:30 UTC to 13:00 UTC."
  - "The eight and a half hour window ran from 10:00 AM to 6:30 PM IST for online stores in India."
  - "Google posted only one 'investigating' update and gave no cause or confirmation of whether any product data was lost or delayed."
  - "Stores that changed prices, stock or feeds that day should check the Needs attention tab, View history and approved product counts."
  - "Advertisers should compare Shopping and Performance Max results for November 6 and 7 and avoid big bid or budget changes based on those days."
image: "/images/covers/google-merchant-center-outage-november-6.webp"
imageAlt: "Google Merchant Center outage status check for product feeds"
format: "md"
---

A Google Merchant Center outage on November 6, 2026 affected three connected services at once: Merchant Center itself, the Merchant API and Feeds. Google's [Merchant Center Status Dashboard](https://merchants.google.com/status/incidents/t9PYzTMMb6MzqB3zAuES) lists the incident as starting at 04:30 UTC and ending at 13:00 UTC, a window of eight and a half hours.

For online stores in India, that window ran from 10:00 AM to 6:30 PM IST, which is most of a working day. Anyone who uploaded new products, changed prices or pushed promotions through a feed or the API that day should not assume everything landed correctly.

The timing matters. Retailers are loading holiday prices and sale products right now, and Shopping ads and Performance Max campaigns depend on product data being accurate. A short checkup today is cheaper than discovering a stale price after a sale starts.

## What Google confirmed about the Google Merchant Center outage

The official record is brief. At 10:26 AM UTC, Google posted one update on the status dashboard: "We're investigating reports of an issue with Merchant API, Merchant Center, and Feeds. We will provide more information shortly."

No further update or cause appears on the incident page. The dashboard only shows that the incident ended at 13:00 UTC. The [Merchant API incident history](https://merchants.google.com/status/products/75f9XJD2BcWpo77rMTzT/history) lists the same event with a duration of 8 hours and 30 minutes, and it is the only Merchant API incident listed for October and November.

[Search Engine Roundtable reported](https://www.seroundtable.com/google-confirms-issues-with-merchant-center-42473.html) the problem the same morning and noted forum complaints that Merchant Center accounts were loading slowly and failing to show data on the overview and other pages. Google has not said publicly whether any product data was lost or delayed, so treat that as unconfirmed.

| Detail | What the official dashboard shows |
|---|---|
| Date | November 6, 2026 |
| Start | 04:30 UTC (10:00 AM IST) |
| End | 13:00 UTC (6:30 PM IST) |
| Duration | 8 hours, 30 minutes |
| Services affected | Merchant API, Merchant Center, Feeds |
| Cause given | None |
| Official updates | One "investigating" message at 10:26 AM UTC |

## Who should pay attention

Not every store needs to act. If you did not touch your product data on November 6 and your feed runs on a weekly schedule, the risk is low.

These groups should run the checks below:

- Stores with daily or hourly scheduled feed fetches that ran during the window.
- Developers and platforms that push product updates through the Merchant API, especially if errors were not retried.
- Retailers that changed prices, stock status or sale prices for holiday campaigns that day.
- Agencies managing many accounts, where one missed update can repeat across clients.
- Advertisers who saw unusual drops in Shopping or Performance Max impressions on November 6 or 7.

## How to check your products after the Merchant Center outage

This is Brandella's recommended checklist, not an official Google procedure.

1. **Open the Needs attention tab.** In Merchant Center, go to Products and click Needs attention in the upper menu. Google's [help page on the Needs attention tab](https://support.google.com/merchants/answer/12476548?hl=en) explains that the summary cards show the issues with the biggest impact and how many products each one affects.
2. **Use View history.** Next to the Show all fixes button, click View history. It shows each product's latest status and status history, and you can filter by time period. Set it to cover November 5 to November 8 and look for products that changed status during the outage.
3. **Compare product counts.** Note how many products are approved today and compare it with the number before November 6. A sudden drop is the clearest sign that something went wrong.
4. **Spot check prices and availability.** Pick ten products you changed recently and compare the price and stock status in Merchant Center with your live product pages. Mismatches can lead to disapprovals.
5. **Refetch your feed.** If your primary feed ran during the window, trigger a manual fetch now rather than waiting for the next schedule.
6. **Review API logs.** If you use the Merchant API, search your logs for failed or timed out calls between 04:30 and 13:00 UTC on November 6 and resend those updates.
7. **Download the issue list.** The Needs attention view can be downloaded, which gives you a record to share with your developer or client.

## What to check in Google Ads reporting

An outage in product data can show up in campaign numbers a day later. Open your Shopping and Performance Max campaigns and compare November 6 and 7 against the same weekdays in the previous two weeks.

Look at impressions, clicks and conversions for product based campaigns separately from Search. If you already keep a [paid media reporting dashboard](/paid-media-reporting-dashboard/), add a note for November 6 so nobody misreads a dip later. A drop that recovers by November 8 is likely linked to the incident, while a drop that continues points to a feed or policy problem you need to fix.

Avoid making big bid or budget changes based only on those two days. In our experience a two day dip is too short to judge a campaign, and our guide on [how to optimize a Performance Max campaign](/how-to-optimize-performance-max-campaign-step-by-step/) explains why short dips are a poor basis for restructuring.

## How to protect your feeds before Black Friday

The bigger lesson is that the holiday season is a bad time to find out your product data has no safety net. A few habits reduce the damage of the next incident.

- **Bookmark the status dashboard.** Check the [Merchant Center Status Dashboard](https://merchants.google.com/status/incidents/t9PYzTMMb6MzqB3zAuES) whenever Merchant Center feels slow, before you start debugging your own feed.
- **Build retries into API updates.** Failed calls should be logged and resent automatically, not silently dropped.
- **Schedule feeds outside your peak update time.** If you change prices in the morning, schedule a second fetch later in the day.
- **Keep a before and after count.** A daily note of approved product totals makes problems obvious in seconds.
- **Track product revenue in GA4.** Clean [GA4 ecommerce events](/ga4-ecommerce-events-examples/) let you see whether sales from product listings dropped, even when ad reporting is delayed.

If you are still deciding how much budget to put into product campaigns this season, our comparison of [Search campaigns vs Performance Max](/search-campaign-vs-performance-max/) covers when each one fits.

## What happens next

Google has not published a cause or a follow up note, and it may never do so for an incident of this size.

For now, the practical step is simple: confirm your product counts and recent price changes, refetch anything that ran during the window, and move on with holiday planning knowing your data is clean.
