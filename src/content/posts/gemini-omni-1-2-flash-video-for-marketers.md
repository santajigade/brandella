---
title: "Gemini Omni 1.2 Flash Brings 15 Second AI Video for Marketers"
slug: "gemini-omni-1-2-flash-video-for-marketers"
date: "2026-11-07T09:48:00+05:30"
author: "santajigade"
categories: ["artificial-intelligence"]
primaryCategory: "artificial-intelligence"
tags: ["Gemini Omni", "AI video", "Google DeepMind"]
description: "Gemini Omni 1.2 Flash makes 15 second AI video clips at a 30% lower price. What changed, where it works, and how marketers should test it."
focusKeyword: "gemini omni 1.2 flash"
image: "/images/covers/gemini-omni-1-2-flash-video-for-marketers.webp"
imageAlt: "Gemini Omni 1.2 Flash AI video model for marketers"
format: "md"
---

Google released Gemini Omni 1.2 Flash on November 5, 2026, an update to its video generation and editing model. According to the [official Google announcement](https://blog.google/innovation-and-ai/technology/developers-tools/introducing-gemini-omni-1-2-flash/) by Anish Nangia, a product manager at Google DeepMind, the model can now generate and edit clips up to 15 seconds long, up from 10 seconds in Omni 1.1, and it costs 30% less.

This matters to anyone who makes short video for ads, social posts or product pages. Fifteen seconds is a common length for short form ad placements, and the model is now available in tools many marketing teams already touch, including Google Ads asset studio, Google Vids and the Gemini API.

Below is what actually changed, where you can use it, what it costs, and a simple way to test it before it goes anywhere near a live campaign.

## What is new in Gemini Omni 1.2 Flash

Google lists several improvements over Omni 1.1. The headline change is length: clips can run from 3 to 15 seconds, set in one second steps. The other changes are about control and consistency, which is usually where AI video falls apart for brand work.

| Area | Omni 1.2 Flash, per Google |
|---|---|
| Clip length | 3 to 15 seconds (Omni 1.1 topped out at 10 seconds) |
| Price | 30% lower than Omni 1.1, $0.07 per second for 720p via the API |
| References | Character, product and style images, motion clips up to 3 seconds, audio cues |
| Consistency | Less drift or morphing from first frame to last; faces, garments, packaging text and brand colors kept across angles |
| Editing | Multi-turn edits on the same clip, such as swapping a product or background, changing lighting or switching aspect ratio |
| Speech | More natural dialogue, clearer lip-sync and multi-speaker support |
| Camera | Continuous moves such as orbits, zoom-outs and FPV style flythroughs with fewer jump cuts |

Google also describes a draft first workflow: create at 360p or 720p, fix details with follow up edits instead of regenerating, then upscale the final clip to 1080p or 4K.

## Where marketers can use it

The announcement lists a wide set of surfaces. For marketing teams, these are the ones that matter most:

- **Google Ads asset studio:** Google says advertisers can scale video campaigns with the model inside asset studio.
- **Google Vids:** 15 second clips at no additional cost for people with a Google account or Workspace subscription.
- **Gemini app:** 15 second videos are rolling out to Google AI Ultra subscribers.
- **Flow:** for directing scenes and multi-turn edits.
- **Gemini API and Google AI Studio:** generally available, model ID `gemini-omni-1.2-flash`, with pricing on the [Gemini API pricing page](https://aistudio.google.com/docs/pricing#gemini-omni-1.2-flash).
- **Google Cloud:** an enterprise API, covered in the [Google Cloud announcement](https://cloud.google.com/blog/products/ai-machine-learning/gemini-omni-1-2-flash-generally-available).

If your team runs [Demand Gen campaigns](/demand-gen-campaigns-explained/) or YouTube heavy Performance Max, the asset studio route is the one to watch, because it puts generation next to the campaign itself.

## What Gemini Omni 1.2 Flash costs

Google gives one clear number: $0.07 per second for 720p video through the Gemini API. On that rate, a full 15 second 720p clip works out to about $1.05 per generation (our own arithmetic). The post does not list prices for 360p, 1080p or 4K, so check the pricing page before you budget for higher resolutions.

Remember that you rarely get a usable clip on the first try. Budget for several drafts and edits per finished asset, not one. Inside Google Vids, Google says 15 second clips come at no additional cost for eligible accounts, which makes it the cheapest place to experiment.

## Brand safety and AI labels

Google says every output carries an imperceptible [SynthID](https://deepmind.google/models/synthid/) watermark. That helps platforms identify AI content, but it does not do your disclosure work for you.

If you run ads, this links directly to a separate change this week. Google Ads now shows visible AI labels on ads in more regions when assets are marked as AI created or edited. We covered that in [Google Ads AI labels now show in California, South Korea and Vietnam](/google-ads-ai-labels-expand-california-korea-vietnam/). Any Omni clip you use in an ad should be labeled correctly in Google Ads.

Google is also open about limits. The announcement says work continues on fast sports action, rapid scene changes and complex physics, so avoid briefs that depend on those.

## What marketers should do now

This is our recommendation, not official Google guidance. Treat the model as a fast prototyping tool first and a production tool second.

1. **Pick one low risk use case.** Product showcase clips, background loops for social posts or concept boards for a video shoot are safer starting points than a hero brand ad.
2. **Build a reference pack.** Collect approved product shots, logo and color references, and one or two short motion clips. Google says the model now holds packaging text and brand colors across angles, so test that claim with your own assets.
3. **Draft cheap, upscale late.** Work at 360p or 720p, use multi-turn edits to fix problems, and only upscale clips that pass review.
4. **Create a review checklist.** Check product accuracy, on screen text, hands and faces, lip-sync and anything that could mislead a buyer. A clip that changes your product's look is a compliance risk, not just a quality issue.
5. **Label AI assets in Google Ads.** Mark them as AI created or edited in the asset library, especially for campaigns that target regions where labels show on the ad.
6. **Test against real footage.** Run AI clips against your existing creative in a controlled test and judge on conversions, not views. Our [creative video marketing ideas](/7-creative-video-marketing-ideas/) can help you plan variants.
7. **Write down usage rules.** Agree who can generate, who approves and where AI video is not allowed, for example testimonials or anything that shows real customers.

## How it fits the wider AI toolkit

Omni 1.2 Flash is one more step toward video becoming a routine asset rather than a special project. For most teams, the win is speed: more variants for testing, faster storyboards and cheaper versions for different aspect ratios.

The risk is the same as with text tools: volume without judgment. Use the model where it saves time and keep humans in charge of claims, accuracy and brand fit. If you are still mapping which tools belong in your stack, see our guide to [AI tools for marketers](/ai-tools-for-marketers/), and for the basics of how these models work, [large language models explained](/large-language-models-explained/).

Full model details are on the [Gemini Omni model page](https://deepmind.google/models/gemini-omni/).
