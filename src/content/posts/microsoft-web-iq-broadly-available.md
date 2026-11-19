---
title: "Microsoft Web IQ Opens to All: What Publishers Control"
slug: "microsoft-web-iq-broadly-available"
date: "2026-11-19T07:30:00+05:30"
author: "santajigade"
categories: ["artificial-intelligence"]
primaryCategory: "artificial-intelligence"
tags: ["Microsoft Web IQ", "Bing", "AI agents", "AI grounding", "Bingbot"]
description: "Microsoft Web IQ, the Bing based grounding service for AI agents, is now open to all Azure customers. What it does and how publishers control their content."
focusKeyword: "microsoft web iq"
takeaways:
  - "Microsoft Web IQ, a grounding service that feeds web results to AI agents, is now available to all Azure customers with lower pricing."
  - "Web IQ draws on Microsoft's own index crawled by Bingbot, and Microsoft says every result links to its original source."
  - "Sites that disallow Bingbot in robots.txt are not in the index Web IQ uses, but that also removes them from Bing."
  - "A page level ai-grounding meta tag or header lets publishers allow, limit or block use of content in generated answers."
  - "The DisallowExtended option keeps content out of third party grounding services such as Web IQ while allowing Microsoft's own experiences."
image: "/images/covers/microsoft-web-iq-broadly-available.webp"
imageAlt: "Microsoft Web IQ broadly available for AI agents"
format: "md"
---

Microsoft Web IQ is now available to all Azure customers. In a [Bing blog post dated November 17, 2026](https://blogs.bing.com/webiq/2026/11/web-iq-is-now-broadly-available-build-better-agents-that-keep-up-with-the-world/), Jordi Ribas, President of Search and AI at Microsoft, says the grounding service for AI agents is open more widely and comes "with new, lower pricing."

Web IQ was [first announced in June 2026](https://blogs.bing.com/search/2026/6/Announcing-Microsoft-Web-IQ/) as "a search engine for AI systems." Instead of showing ten blue links to a person, it returns focused passages of web evidence that an AI agent can use to answer a question.

This matters to marketers and publishers because any company can now plug Bing's index into its own chatbot or agent. Your pages can end up as evidence inside answers on apps you have never heard of, and Microsoft has published controls that decide whether that happens.

![Microsoft Web IQ broadly available: key numbers Microsoft shared](/images/infographics/ig-microsoft-web-iq-broadly-available-1.webp)

## What Microsoft Web IQ is and what is new

Microsoft describes Web IQ as grounding: giving an AI model current facts from the web so its answers are not limited to training data. The June post says it returns passages and structured evidence objects rather than whole documents, with the idea of "fewer tokens in, better answers out, lower cost per call."

The November update adds several pieces:

- **Web IQ Auto**, now the default, which handles multi step retrieval in one call across web, image, video, news, weather and places sources.
- **Auto Advanced**, which checks results, refines queries and fetches more when the first results are not enough.
- **Knowledge domains** for weather, places (more than 207 million businesses and places) and commerce, which is in private preview with more than 40 billion structured offers.
- **Enterprise features** such as Web IQ Scopes, which limit grounding to approved sites or exclude sources, and Zero Query Logging for Azure managed customers in regulated industries.

Microsoft also says Web IQ identifies health questions and prioritizes clinically relevant, credible sources.

## The benchmark claims, and their limits

Microsoft published scores on FreshSearch, a benchmark it has open sourced, on a 0 to 100 scale. Web IQ Auto scored 87.5 and Web IQ web scored 81.2. Microsoft lists Parallel at 82.4, Exa 3.0 Auto at 73.5 and Perplexity at 57.9.

In a test of 500 product category queries, Microsoft says its commerce solution returned 57% more matched products than the next closest competitor. It also quotes customer Genspark saying voice assistant response time dropped from 6 seconds to 0.6 seconds.

Treat these as vendor numbers. The benchmark code is on GitHub, but the tests were run by Microsoft, so independent results may differ.

## How Microsoft Web IQ uses publisher content

For site owners, this is the important section. Microsoft says Web IQ runs on its own index and that "every result links to its original source." Bingbot is the crawler for Bing Search, Copilot and Web IQ alike.

Microsoft lists three separate controls:

| Control | What it decides | How to set it |
| --- | --- | --- |
| Crawling | Whether Bingbot can fetch pages | robots.txt |
| Indexing | Whether pages appear in the Search index | noindex |
| Grounding | Whether content can inform AI generated answers | Page level meta tag or HTTP header |

The blog states that "Bingbot does not crawl sites that publishers disallow, so that content is not in the index Web IQ draws on." Blocking Bingbot is a blunt tool, though. It also removes you from Bing Search.

The finer option is the grounding preference Microsoft explained in its [October 30 post on training and grounding preferences](https://blogs.bing.com/search/2026/10/your-content-your-choice-clearer-preferences-for-training-and-grounding/). On a page you can add a meta tag such as `<meta name="Bingbot" content="ai-grounding:disallow">` or the matching `X-Robots-Tag` header. There are three values:

- **Allow** (the default): content can inform generated responses.
- **DisallowExtended**: grounding is limited to Microsoft operated experiences such as Copilot and Microsoft 365. Third party grounding services such as Web IQ are excluded.
- **Disallow**: content is not used for generated responses.

Microsoft notes there is no site wide robots.txt rule for grounding, only page level settings, and none of the options affects Bing search eligibility. New preferences take effect from February 1, 2027 as Microsoft crawls.

## What publishers and marketers should do now

![Microsoft Web IQ: steps for publishers to set content preferences](/images/infographics/ig-microsoft-web-iq-broadly-available-2.webp)

Most brands want to be cited by AI agents, so the default is often fine. The point is to make the choice on purpose. These steps combine Microsoft's documentation with Brandella recommendations.

1. **Check Bingbot access.** Open your robots.txt and confirm you are not blocking Bingbot by accident. Our [robots.txt guide](/robots-txt-complete-guide/) explains the rules.
2. **Verify real Bingbot traffic.** Use Microsoft's Bingbot verification method before you trust user agent strings in your logs.
3. **Decide per section.** Our recommendation: keep product, service and help pages on Allow so agents can recommend you, and consider DisallowExtended or Disallow only for paid or premium content.
4. **Set page level tags with care.** Use the meta tag or `X-Robots-Tag` header. Our guide to [X-Robots-Tag](/what-is-x-robots-tag-when-to-use-it/) shows where headers fit.
5. **Prompt a recrawl.** Microsoft says preferences apply only after a recrawl and that IndexNow may prompt one but does not guarantee it. See [IndexNow explained](/indexnow-explained-can-it-help-google-index-faster/).
6. **Watch Bing Webmaster Tools.** The [Bing Webmaster Tools guide](/bing-webmaster-tools-complete-guide/) covers setup. Microsoft says temporary grounding preferences open there on December 15, 2026 for pages on sites that use NoArchive or NoCache.

If you are also preparing for Google's agent traffic, read our note on [Google-Agent traffic and how to allow AI agents](/google-agent-traffic-allow-guide/).

## FAQ about Microsoft Web IQ

### What is Microsoft Web IQ?

It is a Microsoft grounding service, built on Bing's index, that gives AI systems and agents current web evidence such as passages, news, images and places data.

### Can I block Web IQ without leaving Bing Search?

Yes, at page level. Microsoft's DisallowExtended grounding value excludes third party grounding services such as Web IQ while keeping your search eligibility.

### Does Web IQ link back to my site?

Microsoft says every Web IQ result links to its original source. Whether an agent shows that link to its users depends on the app that uses it.

### Is there a site wide setting for grounding?

No. Microsoft says grounding preferences are page level only, set with a meta tag or HTTP header. Training preferences can be set in robots.txt.
