---
title: "ChatGPT Ads Target CPA and Target CPC: What Changes November 9"
slug: "chatgpt-ads-target-cpa-target-cpc"
date: "2026-11-08T09:45:00+05:30"
author: "santajigade"
categories: ["paid-media", "ppc-strategy"]
primaryCategory: "ppc-strategy"
tags: ["ChatGPT Ads", "OpenAI", "Target CPA", "Target CPC", "bidding"]
description: "ChatGPT Ads Target CPA and Target CPC launch in Ads Manager on November 9, and Max Bid and Max CPC retire on January 1, 2027. What changes and what to do."
focusKeyword: "chatgpt ads target cpa"
image: "/images/covers/chatgpt-ads-target-cpa-target-cpc.webp"
imageAlt: "ChatGPT Ads Target CPA and Target CPC bidding change"
format: "md"
---

ChatGPT Ads Target CPA and Target CPC bidding arrive in OpenAI's Ads Manager on Monday, November 9, 2026. According to an email OpenAI sent to advertisers, first reported by [Search Engine Roundtable](https://www.seroundtable.com/openai-updates-chatgpt-ads-bidding-options-42470.html), the two new cost targets will replace the older Max Bid and Max CPC options, which retire on January 1, 2027.

The change affects every advertiser running conversion or click campaigns in ChatGPT. Existing campaigns are not switched off on November 9, but they will need to move to the new strategies before the old ones are retired.

This is a meaningful shift in how you control cost. Max Bid and Max CPC were caps on what you would pay. The new options are averages that the system aims for, which means individual auctions can cost more or less than the number you enter.

## What OpenAI is changing in ChatGPT Ads bidding

Based on the advertiser email as reported by Search Engine Roundtable, there are three changes. OpenAI's wording was that "starting Monday, November 9, you can optionally choose a cost target in Ads Manager."

| Campaign type | Old option | New option | What the new option does |
|---|---|---|---|
| Conversion campaigns | Max Bid | Target CPA | You set an average cost per conversion and the system adjusts bids toward it |
| Click campaigns | Max CPC | Target CPC | You set an average cost per click; single auctions can go above or below it |
| Automatic bidding | Maximize results | Intelligent bidding | Same automatic bid and delivery adjustment under a new name |

New conversion campaigns get Target CPA and new click campaigns get Target CPC. Existing Max Bid and Max CPC campaigns keep running until you switch them, up to the January 1, 2027 retirement date.

## Key dates for advertisers

| Date | What happens |
|---|---|
| November 9, 2026 | Target CPA and Target CPC become available in Ads Manager |
| November 9 to December 31, 2026 | Old and new options exist side by side; existing campaigns keep running |
| January 1, 2027 | Max Bid and Max CPC are retired |

OpenAI also publishes a help article on [bidding strategies and how pricing works in ChatGPT Ads](https://help.openai.com/en/articles/20001634-bidding-strategies-and-how-pricing-works-in-chatgpt-ads). We could not load it during this run, so check it in your own account before you make changes, in case details differ by market.

## Why ChatGPT Ads Target CPA is not the same as a cap

If you have run Google Ads, this model will feel familiar. Google's own [Target CPA documentation](https://support.google.com/google-ads/answer/6268632?hl=en) says plainly that "some conversions may cost more than your target and some may cost less", because the system aims for an average, not a ceiling.

The same logic applies to Target CPC in ChatGPT Ads. Unlike Max CPC, which capped each bid, the new option lets the system bid above or below your target in individual auctions. For advertisers who used Max CPC as a hard safety limit, that is the biggest practical change.

There is also a delivery risk on the other side. OpenAI warned advertisers that overly restrictive targets or weak conversion signals can limit delivery and leave budget unspent. A target set too low does not save money; it can simply stop your ads from showing.

We covered how this model works in Google Ads when Google changed its rules for advertisers [beating their Target CPA](/google-ads-bidding-change-target-cpa/). Much of that thinking carries over.

## Conversion tracking matters more now

Target CPA only works as well as the conversion data behind it. OpenAI's advice in the email was to confirm that your Pixel or Conversions API sends the selected event to the linked data source, and to use Event Quality Score warnings to find and fix gaps.

OpenAI's developer guide to [ChatGPT Ads conversion tracking](https://developers.openai.com/ads/conversion-tracking) explains the two options. The Measurement Pixel runs in the browser, the Conversions API runs on your server, and you can use both if you send the same event name and event ID through each channel so the same action is not counted twice.

The guide also says only standard events, such as `order_created` for purchases or `lead_created` for leads, can drive conversion optimization. Custom events like `quote_requested` can be tracked, but they will not train the bidding. If your key action is set up as a custom event today, that is the first thing to fix.

## What advertisers should do now

Here is the checklist we suggest. These are Brandella's recommendations based on OpenAI's guidance, not official OpenAI steps.

1. **List every campaign by bid type.** Mark which ones use Max Bid and which use Max CPC, so you know exactly what must move before January 1, 2027.
2. **Pull recent actual CPA and CPC.** OpenAI recommends basing targets on recent actual results. Use the last few weeks of real numbers, not the cap you used to enter.
3. **Check your conversion event.** Confirm it is a standard event, that it fires on the Pixel or Conversions API, and that it is linked to the right data source.
4. **Fix Event Quality Score warnings.** Work through them before switching a conversion campaign to Target CPA.
5. **Set up deduplication if you use both channels.** Match the event ID between the Pixel and the server event.
6. **Move one campaign first.** Switch a single campaign on or after November 9, watch delivery and cost for a week or two, then migrate the rest.
7. **Watch for underspend.** If spend drops sharply after the switch, your target is probably too tight. Loosen it in small steps.
8. **Do not leave it to the last week of December.** Migrating early gives the system time to learn before the old options disappear.

If you report ChatGPT Ads alongside other channels, add average CPA and CPC against target to your [paid media reporting dashboard](/paid-media-reporting-dashboard/) so you can spot drift quickly.

## How this fits the wider ChatGPT Ads picture

Moving from bid caps to cost targets brings ChatGPT Ads closer to the Target CPA model Google Ads advertisers already know, with the system adjusting bids auction by auction. In our view it gives OpenAI's system more room to find conversions, and gives advertisers less direct control over single auctions.

If you are still deciding how much budget ChatGPT deserves compared with search, our comparison of [ChatGPT Ads vs Google Search Ads](/chatgpt-ads-vs-google-search-ads/) covers the strategic side. For accounts that already optimize toward revenue, our guide to [value based bidding](/value-based-bidding-google-ads-explained/) explains why clean conversion data is the foundation for any target based strategy.

The short version: check your tracking this week, set realistic targets from real data, and start moving campaigns from November 9 rather than waiting for January.
