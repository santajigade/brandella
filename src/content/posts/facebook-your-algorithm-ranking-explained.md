---
title: "Facebook Your Algorithm: How Meta Ranks Interests People Choose"
slug: "facebook-your-algorithm-ranking-explained"
date: "2026-11-12T18:15:00+05:30"
author: "santajigade"
categories: ["social"]
primaryCategory: "social"
tags: ["Facebook", "Meta", "Your Algorithm", "Feed ranking", "Reels"]
description: "Meta explains how Facebook Your Algorithm turns typed interests into Feed and Reels ranking. What the new engineering post means for creators and brands."
focusKeyword: "facebook your algorithm"
takeaways:
  - "Facebook Your Algorithm, launched October 13, 2026, lets people type topics they want more or less of in Feed and Reels."
  - "An Engineering at Meta post on November 10, 2026 explained how chosen interests are retrieved, boosted, balanced and filtered."
  - "New interests get temporary extra weight and a daily cap per interest, after which normal engagement signals decide ranking."
  - "Topics marked Not interested in are filtered at several stages, including an LLM reranker and the on device cache."
  - "Requests for less AI generated or suggestive content use separate quality demotion signals, while named creators are filtered out directly."
image: "/images/covers/facebook-your-algorithm-ranking-explained.webp"
imageAlt: "Facebook Your Algorithm interest controls shaping Feed and Reels ranking"
format: "md"
---

Facebook Your Algorithm lets people type the topics they want more or less of, and Meta has now explained in detail how those choices flow into Feed and Reels ranking. The explanation came in an Engineering at Meta post published on November 10, 2026, about a month after the feature launched.

The post, [Your Algorithm: Giving People More Ways to Personalize Facebook Recommendations](https://engineering.fb.com/2026/11/10/ml-applications/your-algorithm-giving-people-more-ways-to-personalize-facebook-recommendations/), is written by eight Meta engineers. It covers how interests are retrieved, boosted, balanced and filtered, and where large language models fit in. [Social Media Today](https://www.socialmediatoday.com/news/meta-publishes-explainer-on-your-algorithm-controls/874460/) highlighted it on November 11.

For brands, publishers and creators on Facebook, this is rare insight into how a user's stated preference beats or blends with engagement signals. It also shows how fast a user can now remove your topic, or your page, from their feed.

![Facebook Your Algorithm: what happens when people add or remove interests](/images/infographics/ig-facebook-your-algorithm-ranking-explained-1.webp)

## What Facebook Your Algorithm is

Meta introduced the tools on [October 13, 2026](https://about.fb.com/news/2026/10/introducing-your-algorithm-facebook/), describing them as "a dedicated space to tell us exactly what you're into." People reach it from the three dot menu on any post.

According to the engineering post, the page has three parts:

- **Lately summary:** a one sentence description of what the person has been watching recently.
- **Interested in:** a list prefilled with interests Meta inferred from past activity.
- **Not interested in:** topics the person marked as uninteresting, or content they have hidden or X'd out.

People can add interests in plain language, move them between lists or remove them. Changes apply to both Feed and Reels. Meta says the page and the ranking system read from the same preference store, so what people see on the page is what ranking actually uses.

## How chosen interests change ranking

Each interest a person adds drives four retrieval sources. Two find matching content directly, through search and clusters of related topics. Two extend reach through the content graph and similarity between items. Candidates that pass a relevance check against the interest then get a boost in late stage ranking.

New interests get extra weight for a limited time so people notice the change. After that, Meta relies on how people actually engage with that content.

Balance is a stated goal. The system spaces out recommendations for the same interest and caps each interest's daily contribution. The post puts it this way: "A new interest should show up, not take over."

| Signal | What Meta says happens |
| --- | --- |
| New interest added | Temporary extra weight, plus an extra fetch for fresh matching content |
| After the boost period | Normal engagement signals decide ranking |
| Many posts on one interest | Spaced out, with a daily cap per interest |
| Topic added to Not interested in | Filtered during ranking, by an LLM reranker and from the on device cache |
| Request to see less of a creator | That creator's content is filtered out directly |
| Request for less AI or suggestive content | Handled by separate quality demotion signals |

## How Not interested in works

Removal is stricter than addition. Meta filters at several stages: an embedding comparison removes candidates too close to the listed topic, demotion rules push down near matches, and after ranking a fine tuned LLM reranker reviews the final list. On the device, cached content that matches the topic is dropped before it is shown.

Requests about quality, such as seeing less AI generated or sexually suggestive content, are handled by dedicated demotion signals rather than topic matching. Social Media Today notes Meta's point that this can reduce AI generated content in feeds but will not eliminate it. When a person names a specific creator, that creator's content is filtered out directly.

## Where LLMs fit in

Meta uses LLMs at four points. One turns interest signals into readable topic names and writes the Lately summary. A smaller model checks that each phrase a person adds is a coherent topic, spots duplicates and maps it to a clean name. A fine tuned model reranks results to remove recently excluded topics. Another LLM acts as a judge to grade outputs during evaluation. The post shares no figures on adoption or engagement impact.

## What brands and creators should do now

![What brands and creators should do now about Facebook Your Algorithm](/images/infographics/ig-facebook-your-algorithm-ranking-explained-2.webp)

These steps are Brandella recommendations based on Meta's description, not official Meta advice.

1. **Make your topic obvious.** Interests are matched by topic, so posts with a clear, consistent subject are easier to retrieve for people who chose that interest. Mixed, vague posts are harder to match.
2. **Earn the second look.** The boost for a new interest is temporary. After that, engagement decides. Content that gets saves, shares and comments will keep its place.
3. **Avoid being the reason someone opts out.** Repetitive or low quality posting can lead people to add your topic or your page to Not interested in, and Meta filters those requests at several stages.
4. **Label AI content honestly.** Meta handles requests for less AI content through quality demotion. Do not rely on unlabelled AI images to carry your reach.
5. **Watch reach by format.** Changes apply to both Feed and Reels, so compare organic reach on each and review your [social media KPIs](/social-media-kpis-every-marketer-should-track/) monthly.
6. **Keep paid separate in your analysis.** The post is about organic recommendations. For paid reach, keep your [Meta Advantage Plus setup](/meta-advantage-plus-campaigns/) and creative testing on their own track.

## What this means for Facebook marketing

The direction is clear: people get more direct control, and Meta is building ranking around what they say they want, not only what they click. That rewards brands with a clear niche and loyal followers, and it punishes accounts that rely on reach from people who never asked for them.

If you are reviewing your plan for next year, our look at [Facebook marketing in 2026](/facebook-marketing-2026-whats-working/) covers the basics that still work. Add one new question to that plan: would someone who typed your topic into Your Algorithm be glad they saw your post?
