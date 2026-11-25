---
title: "Google Generative AI Controls: New Guide to AI Opt Outs"
slug: "google-generative-ai-controls"
date: "2026-11-25T07:10:00+05:30"
author: "santajigade"
categories: ["artificial-intelligence"]
primaryCategory: "artificial-intelligence"
tags: ["Google-Extended", "AI Overviews", "AI Mode", "robots.txt", "Search Console"]
description: "A new guide to Google generative AI controls, published November 24, 2026, explains training, grounding, Google-Extended and AI Overviews opt outs."
focusKeyword: "google generative ai controls"
takeaways:
  - "Google published two new pages on November 24, 2026: one on generative AI controls and one on attribution in AI Overviews and AI Mode."
  - "Google separates model training from grounding, which looks up fresh content from the Search index when answering."
  - "The Search generative AI control in Search Console handles AI Overviews, AI Mode and Discover but does not affect model training."
  - "Google-Extended in robots.txt limits training and grounding for other Google AI products and is not a Search ranking signal."
  - "Google intends to support a shared machine-readable AI training preference signal in early 2027."
image: "/images/covers/google-generative-ai-controls.webp"
imageAlt: "Google generative AI controls guide for site owners"
format: "md"
---

Google has published a single guide to its Google generative AI controls, explaining how content it crawls is used to train models and to answer questions in AI features, and which settings site owners can change. The [documentation changelog](https://developers.google.com/search/updates) lists it on November 24, 2026 as "Added documentation about generative AI controls and attribution."

Two pages went live. [Control how your content is used for generative AI at Google](https://developers.google.com/search/docs/fundamentals/gen-ai-controls) covers the settings. [Attribution and factuality in Search generative AI features](https://developers.google.com/search/docs/fundamentals/gen-ai-attribution-factuality) explains how AI Overviews and AI Mode pick and link sources.

For publishers and brands, the guide sets out what each control does and how to stay in Search while opting out of AI uses, or the other way round.

![Google generative AI controls compared: Search generative AI control, Google-Extended, GoogleOther, snippet rules and noindex](/images/infographics/ig-google-generative-ai-controls-1.webp)

## Training vs grounding: the split that matters

Google describes two separate uses of web content.

Model training teaches foundation models such as Gemini general patterns, reasoning and world knowledge before they are deployed. That training feeds the Gemini app and Search generative AI features, including AI Overviews, AI Mode and generative AI features in Discover.

Grounding, also called RAG, means looking up fresh information from the Google Search index when answering a prompt. Google says it does this "to improve the factuality, accuracy, and relevancy of responses and link to supporting web pages." Grounding happens after a model is trained and is independent of training.

That is why each control below covers a different use.

## The Google generative AI controls, one by one

| Control | What it manages | Where you set it |
|---|---|---|
| Search generative AI control | Grounding and display, including links, in AI Overviews, AI Mode and Discover. Does not affect model training | Search Console settings |
| Google-Extended | Training and grounding for certain commercially available Google generative AI products | robots.txt |
| GoogleOther | Google's generic crawler for non-Search uses, such as one-off research crawls | robots.txt |
| nosnippet, data-nosnippet, max-snippet | Snippets and previews, including in AI Overviews and AI Mode | Page HTML or X-Robots-Tag header |
| noindex | Keeps a page out of Search, including generative AI features | Page HTML or X-Robots-Tag header |

Google says the Search generative AI control "isn't used as a ranking or inclusion signal for other parts of Google Search." It says the same of Google-Extended, which is not a ranking signal and does not affect a site's inclusion in Search. Opting out of AI uses should not, by Google's account, hurt your normal rankings.

Google also says nosnippet and max-snippet can stop content from being used as a direct input for AI Overviews and AI Mode. If you are new to these rules, our guides to the [robots meta tag](/meta-robots-tags-explained-2/) and the [X-Robots-Tag header](/what-is-x-robots-tag-when-to-use-it/) cover the syntax.

## Common setups Google describes

The guide lists seven example setups. The ones most sites will care about:

- To stay in Search and allow training but skip AI features, set the Search generative AI control to "Exclude my site's links and content from Search generative AI features" and do not disallow Google-Extended.
- To stay in Search and AI Overviews but limit other AI products, disallow Google-Extended in [robots.txt](/robots-txt-complete-guide/).
- To opt out of both, use the Search generative AI control and disallow Google-Extended.
- For paywalled content, add paywalled structured data with data-nosnippet or max-snippet.

Looking further out, Google writes that it "intends to support the shared machine-readable training preference signal (with `user-agent: __usage_ai-training`) in early 2027."

## How AI Overviews choose which sites to link

The attribution page sets out four steps. The model starts with ranked results from the Search index, and Google says "snippets from these articles are provided to the model as a basis for the overview." It may then run related searches, which Google calls "query fan-out," to cover other parts of the question. It writes the answer, cites and links the pages that support it, and shows them as inline links, source cards and carousels.

Google says this runs on "a customized Gemini model integrated directly with Google's core web ranking, information retrieval, and quality systems." Claims are checked against web results, data feeds and the Knowledge Graph. Sensitive Your Money or Your Life topics and thin breaking news coverage face a higher bar.

If your content is credited to the wrong source, Google points to the Feedback link under the AI response. A copy of your content on another site can be reported under the DMCA.

## What site owners should do now

![Five steps to review your Google generative AI controls](/images/infographics/ig-google-generative-ai-controls-2.webp)

These steps are our recommendations based on Google's two pages:

1. Decide your goal first: full AI visibility, Search only, or a mix. Then pick the matching setup from Google's list.
2. Check your robots.txt for a Google-Extended rule and confirm it matches that decision.
3. Open Search Console settings and check the Search generative AI control. Google says your site must be included there to be linked in these features.
4. Use data-nosnippet on passages you do not want quoted, instead of removing the whole page.
5. Track the effect in the Generative AI performance report in Search Console, keeping in mind the [low data bug from November 9 to 11](/search-console-generative-ai-report-bug/).

## FAQ about Google generative AI controls

### Does blocking Google-Extended hurt my Google rankings?

Google says Google-Extended is not used as a ranking signal in Search and does not affect a site's inclusion in Search.

### Can I stay in Search but leave AI Overviews and AI Mode?

Yes. Google says you can set the Search generative AI control in Search Console to exclude your site's links and content from Search generative AI features.

### Does the Search Console control stop model training?

No. Google says the Search generative AI control does not affect generative AI model training.

### When will Google support the shared AI training signal?

Google says it intends to support the shared machine-readable training preference signal in early 2027.
