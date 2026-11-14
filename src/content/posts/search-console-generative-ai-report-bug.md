---
title: "Search Console Generative AI Report Bug: Nov 9 to 11 Data Low"
slug: "search-console-generative-ai-report-bug"
date: "2026-11-14T07:30:00+05:30"
author: "santajigade"
categories: ["seo", "google-search-console"]
primaryCategory: "google-search-console"
tags: ["Search Console", "Generative AI performance report", "data anomaly", "AI Overviews"]
description: "Google confirmed a Search Console generative AI report bug that cut impressions for November 9 to 11, 2026. What it affects and how to report around it."
focusKeyword: "search console generative ai report bug"
image: "/images/covers/search-console-generative-ai-report-bug.webp"
imageAlt: "Search Console generative AI report bug November 2026"
format: "md"
---

Google has confirmed a Search Console generative AI report bug that lowered impressions for November 9 to 11, 2026. The note on Google's official [data anomalies in Search Console](https://support.google.com/webmasters/answer/6211453?hl=en#zippy=%2Cperformance-reports-search-results-discover-google-news) page reads: "A logging error caused a decrease in impressions on the Generative AI performance report in Search." Google adds that "This issue affects data logging only."

In plain words, your pages did not lose visibility in AI features because of this bug. The report simply recorded fewer impressions than really happened on those three days. [Search Engine Roundtable reported the issue](https://www.seroundtable.com/google-generative-ai-performance-report-data-bug-42527.html) on November 12 and noted that the report now shows an annotation for the affected dates.

The timing makes it more than a small footnote. The [Google November 2026 core update](/google-november-2026-core-update/) started rolling out on November 10, right inside the bug window. Anyone reading AI visibility trends this week needs to keep both events apart before drawing any conclusion.

![Search Console generative AI report bug: affected dates and what Google confirmed](/images/infographics/ig-search-console-generative-ai-report-bug-1.webp)

## What the Search Console generative AI report bug affects

Google's note is short, so it helps to be precise about what it does and does not say. Here is the confirmed scope, taken from the data anomalies page:

| Question | What Google has said |
|---|---|
| Which report | Generative AI performance report in Search |
| Which dates | November 9 to 11, 2026 |
| Which metric | A decrease in impressions |
| Real search performance | Not affected, "data logging only" |
| Data restored | Not stated yet for this incident |

For context, Google's help page for the [Generative AI performance report (Search)](https://support.google.com/webmasters/answer/16984139) says it shows impressions for links to your site in AI Overviews and AI Mode, grouped by page, country, date or device. Note that multiple links from one site in a single AI result count as one impression in the chart.

Google has not said anything about clicks for this incident, so do not assume either way. It has also not said whether the missing impressions will be filled back in. If you need exact numbers for those days, wait for an update on the anomalies page before reporting them.

## This is not the first logging error in this report

The same page lists an earlier problem in the same report. For August 13 to 17, 2026, Google logged the identical wording: a logging error "caused a decrease in impressions on the Generative AI performance report in Search."

That August case had a happier ending. An update dated August 21 says the missing data was restored and that "The Performance report now shows complete metrics." Google also listed a separate August 13 error that dropped Discover clicks and impressions, which also lowered reported impressions for generative AI features in Discover.

Two logging errors in about three months is worth noting. The report is still young, and its numbers should be read as a guide to trends rather than a precise count. We would treat any single day of unusual data with care until it has been checked against the anomalies page.

## Why the core update overlap matters

The November core update began on November 10, and core updates take time to roll out fully. So rankings can move at the same time as the report under-counts impressions. A drop on November 10 or 11 could be the bug, the update, or both.

The safest approach is to separate the two signals. The bug only touches the generative AI report, so your regular [Search Console performance report](/search-console-performance-report/) is the better place to judge core update movement in classic web results. If the regular report looks stable but the AI report dips only on November 9 to 11, the logging error is the likely cause.

If you also track visits in analytics, Google's new guidance on how to [identify Google Search traffic](/identify-google-search-traffic-referer/) helps you check whether real visits from Google changed on those days. Analytics will not split AI features from regular results, but it gives you a second source that the logging error cannot touch.

## What SEO teams should do now

This is our own checklist, not an official Google process. It keeps your reporting honest without wasting time chasing a bug.

![Checklist for handling the Search Console generative AI report bug](/images/infographics/ig-search-console-generative-ai-report-bug-2.webp)

1. **Annotate November 9 to 11 in every report.** Add a note to your dashboards, client decks and Looker Studio pages so nobody reads the dip as a real loss.
2. **Exclude the window from comparisons.** When you compare week over week or month over month for AI impressions, compare periods that do not include November 9 to 11, or call out the gap clearly.
3. **Use the regular performance report for core update checks.** Judge ranking changes from the standard web search data, ideally after the rollout finishes. Filters such as the [device filter with multi-select](/search-console-device-filter-multi-select/) and the [branded vs non-branded filter](/branded-queries-filter-in-search-console/) help you see where any real change sits.
4. **Do not change content because of these three days.** A logging error is not a quality signal. Pausing, rewriting or deleting pages based on a known bug can cause real damage.
5. **Recheck the anomalies page next week.** In August, Google restored the data four days after the window ended. If it does the same here, refresh any exported numbers before final monthly reporting.
6. **Save a raw export now.** Export the generative AI report for early November. If Google restores data later, you can compare before and after and show stakeholders exactly what changed.

## How to explain the gap to clients and managers

Many people outside SEO now watch AI visibility closely, so a sudden dip can trigger worried messages. Keep the explanation short: Google confirmed a logging error, the affected days are November 9 to 11, and Google says real search performance was not affected.

Link them to the official anomalies page so they can read it themselves. Then show them the regular performance report for the same days. A clear, sourced note sent early usually prevents a long thread later, especially during a core update week.

For monthly reports, add one line in the methods or notes section. Something like "AI impressions for November 9 to 11 are under-reported due to a confirmed Google logging error" is enough.

## What we still do not know

Google has not said whether the November data will be restored, and it has not explained what caused the error. It has also not given any figure for how large the drop was. Until Google updates the page, any estimate of the missing impressions is a guess.

We will watch the data anomalies page and update this article if Google adds a fix or restore note. In the meantime, treat the AI report as useful for direction, keep the bug window out of your conclusions, and judge the core update on the data that was logged correctly.
