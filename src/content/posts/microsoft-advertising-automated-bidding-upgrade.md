---
title: "Microsoft Advertising Automated Bidding Gets a Big Upgrade"
slug: "microsoft-advertising-automated-bidding-upgrade"
date: "2026-11-19T07:20:00+05:30"
author: "santajigade"
categories: ["paid-media", "ppc-strategy"]
primaryCategory: "ppc-strategy"
tags: ["Microsoft Advertising", "Bing Ads", "Smart bidding", "Target ROAS", "Target CPA"]
description: "Microsoft Advertising automated bidding gets rebuilt prediction models that react faster to target changes. What changed, the claims and what to check now."
focusKeyword: "microsoft advertising automated bidding"
takeaways:
  - "Microsoft calls the rebuilt prediction models behind its automated bidding its biggest bidding model upgrade in a decade."
  - "Microsoft says bids now adjust nearly twice as fast after a CPA or ROAS target change and budgets pace more evenly."
  - "Internal data claims about 10% more conversion value per click for Maximize Conversion Value or Target ROAS at similar ROAS."
  - "The upgrade rolls out automatically to more accounts over time, with more bidding updates planned for 2027."
  - "Microsoft advises against Maximum CPC caps and suggests changing targets in 15% steps."
image: "/images/covers/microsoft-advertising-automated-bidding-upgrade.webp"
imageAlt: "Microsoft Advertising automated bidding upgrade"
format: "md"
---

Microsoft Advertising automated bidding is getting what the company calls its "biggest upgrade to bidding models in a decade." In a [blog post dated November 18, 2026](https://about.ads.microsoft.com/en/blog/post/november-2026/building-the-next-generation-of-automated-bidding-at-microsoft-advertising), Principal Product Manager Carlo Buchmann says Microsoft rebuilt the model that predicts whether a click will turn into a sale and how much that sale is worth.

The change affects every advertiser who uses conversion based bid strategies on Microsoft Search and the Microsoft Audience Network, such as Target CPA, Target ROAS, Maximize Conversions and Maximize Conversion Value. There is no opt in. Microsoft says the updates roll out automatically to more accounts over time, and that this is only the first stage, with more improvements planned for 2027.

Why it matters: when the model under your bids changes, results can shift even if you touch nothing. Knowing what Microsoft promises, and what it recommends, helps you separate a real problem from normal recalibration.

![Microsoft Advertising automated bidding upgrade: Microsoft internal performance claims](/images/infographics/ig-microsoft-advertising-automated-bidding-upgrade-1.webp)

## What changed in Microsoft Advertising automated bidding

Microsoft says the new prediction model uses new user signals and a better way of valuing conversions. It lists three practical improvements:

- **More consistent performance:** bids hit CPA and ROAS targets more consistently without cutting conversion volume or value.
- **Faster optimization:** bids adjust nearly twice as quickly after you change a CPA or ROAS target.
- **More predictable delivery:** budgets pace more evenly through the day, and campaigns reach full budget faster.

The faster reaction to target changes is the part most account managers will notice first. In the past, a target change often meant waiting days before you could judge it.

## The performance claims, and how to read them

Microsoft shares three numbers from its own internal data. These are Microsoft's averages, not guarantees for any single account.

| Scenario | Microsoft's claim | Data period |
| --- | --- | --- |
| Maximize Conversion Value or Target ROAS | About 10% more conversion value per click at similar ROAS | August 2026, Search and Audience Network |
| Search campaigns moving from Target CPA to Target ROAS | About 8% more conversion value on average at similar ROAS | August to September 2026 |
| Moving from Enhanced CPC to Maximize Conversions with a Target CPA | About 18% more conversions at a similar cost per action | June to July 2026 |

Microsoft adds that the biggest value gains come when advertisers optimize on actual transaction values, such as purchase revenue. If you still pass a flat value for every conversion, value based bidding has little to learn from.

## Microsoft's own advice on bid strategy choice

The post includes clear setup guidance. Microsoft recommends [Universal Event Tracking (UET)](https://help.ads.microsoft.com/#apex/ads/en/56913/2) as the main conversion tracking method, with the [Conversions API](https://help.ads.microsoft.com/#apex/ads/en/60239/2) for added coverage and offline conversion import as another option.

For strategy choice, it gives a simple rule. With at least five account level conversions, start with a conversion based strategy instead of Enhanced CPC, because account history informs all campaigns. With fewer than five, start with Enhanced CPC to build history, then move to Maximize Conversions with a Target CPA or Maximize Conversion Value with a Target ROAS.

Two more points stand out. Microsoft says "Keeping a Maximum CPC set on your campaigns is not recommended," because caps conflict with CPA or ROAS targets and can stop you reaching goals even when the cap sits above your average CPC. It also describes targets as directional guides for the balance between volume and efficiency, not strict limits.

## What advertisers should do now

![Microsoft Advertising automated bidding upgrade: steps for advertisers](/images/infographics/ig-microsoft-advertising-automated-bidding-upgrade-2.webp)

Here is a practical checklist built from Microsoft's guidance plus our own experience running campaigns on both Google and Microsoft. Where a point is our recommendation rather than Microsoft's, we say so.

1. **Audit conversion tracking first.** Confirm UET fires on every key action and that purchase revenue is passed as a real value. Better models still need good inputs. If you use Google Tag Manager, our guide to [GA4 events vs conversions](/ga4-events-vs-conversions-difference/) helps you decide what to count.
2. **Mark a change date in your reports.** Our recommendation: add an annotation or note for November 18, 2026, so you can compare before and after periods fairly.
3. **Review Maximum CPC caps.** Microsoft says to avoid them on CPA or ROAS strategies. If a cap exists only out of habit, plan to remove it and use budgets, targets and conversion value rules instead.
4. **Change targets in 15% steps.** Microsoft suggests this increment and a review after one conversion cycle. Large CPA increases or ROAS decreases can cause short term volatility.
5. **Judge with enough data.** Microsoft points to about 30 conversions in 30 days and evaluation one to two conversion cycles after major changes.
6. **Evaluate at the right level.** Look at campaign or portfolio results using conversions and CPA or ROAS, not keyword level CPC. The new [bid strategy reports in the Microsoft Advertising interface](/microsoft-advertising-interface-update/) that compare target and actual results are useful here.
7. **Test Target ROAS if you track revenue.** Our recommendation: pick one Search campaign with steady volume and real revenue values, and test the switch from Target CPA, since that is where Microsoft reports an average 8% value gain.

If you manage Google Ads too, keep the platforms separate in your analysis. Our [Google Ads optimization tips](/25-google-ads-optimization-tips/) and the guide on [search campaigns vs Performance Max](/search-campaign-vs-performance-max/) cover the Google side.

## Open questions about the rollout

Microsoft Advertising liaison Navah Hopkins answered follow up questions on LinkedIn, as [Search Engine Journal reported](https://www.searchenginejournal.com/microsoft-rolls-out-its-biggest-bidding-upgrade-in-a-decade/597963/). Still, Microsoft does not say which accounts get the new models first, or how long the full rollout will take. The post also does not publish an exact list of every affected bid strategy, so treat the strategies named above as the ones Microsoft discusses rather than a complete list.

Microsoft asks for feedback through its feedback portal, in product feedback and support. If you see sharp swings that do not settle after one or two conversion cycles, raise a support ticket with dates and campaign IDs.

## FAQ about Microsoft Advertising automated bidding

### Do I need to turn on the new Microsoft bidding models?

No. Microsoft says the updates roll out automatically to more accounts over time. There is no opt in step mentioned in the announcement.

### Will my CPA or ROAS change right away?

It might shift while the model recalibrates. Microsoft recommends judging results after one to two conversion cycles and with about 30 conversions in 30 days.

### Should I remove Maximum CPC caps?

Microsoft says keeping a Maximum CPC on campaigns is not recommended because it conflicts with CPA and ROAS targets. Review each cap and remove it unless you have a strong business reason.

### Is Enhanced CPC still useful?

Yes, as a starting point. Microsoft suggests Enhanced CPC for accounts with fewer than five conversions, then a move to a conversion based strategy once history builds.
