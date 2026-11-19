---
title: "GPT-6.2 Astra and Sol: What Marketers Should Know"
slug: "gpt-6-2-astra-sol-marketers"
date: "2026-11-19T18:05:00+05:30"
author: "santajigade"
categories: ["artificial-intelligence"]
primaryCategory: "artificial-intelligence"
tags: ["OpenAI", "GPT-6.2", "ChatGPT", "AI models", "Prompt engineering"]
description: "GPT-6.2 Astra and Sol are OpenAI's new models for ChatGPT and the API. Pricing, the new prompting advice and what marketing teams should test first."
focusKeyword: "gpt-6.2 astra"
takeaways:
  - "OpenAI launched GPT-6.2 Astra, its frontier model, and GPT-6.2 Sol, a cheaper everyday model, in ChatGPT, Codex and the API."
  - "Astra API pricing is $8 input and $40 output per million tokens, 20% lower than GPT-6 Astra; Sol stays at $2 and $10."
  - "OpenAI says Astra is more concise by default, so old 'be concise' instructions may need a rewrite."
  - "The API now drops reasoning items if an app edits earlier conversation history, which can lower quality and raise token use."
  - "OpenAI highlights better slides, documents, spreadsheets and web layouts, which are the areas marketers should test first."
image: "/images/covers/gpt-6-2-astra-sol-marketers.webp"
imageAlt: "GPT-6.2 Astra and Sol models from OpenAI for marketers"
format: "md"
---

OpenAI has released two new models, GPT-6.2 Astra and GPT-6.2 Sol. In its [launch post](https://openai.com/index/introducing-gpt-6-2-astra-sol/), OpenAI describes Astra as its frontier model for the hardest projects and Sol as the efficient, versatile model for everyday work. Both are available now in ChatGPT, Codex and the API, and [Search Engine Journal](https://www.searchenginejournal.com/openai-gpt-6-2-astra-prompting-guidance/597877/) dated the launch to November 17, 2026.

The release affects two groups of marketers. Teams that use ChatGPT for slides, reports and briefs will see a model that OpenAI says writes "more direct" output with "less filler". Teams that build tools on the API, such as content workflows, chatbots or reporting scripts, get new pricing and a set of migration rules that can quietly change cost and quality.

The key point: GPT-6.2 Astra is not just a faster model. OpenAI changed how it prefers to be prompted, so prompts written for older models may now work worse.

![GPT-6.2 Astra and Sol API pricing per million tokens](/images/infographics/ig-gpt-6-2-astra-sol-marketers-1.webp)

## GPT-6.2 Astra and Sol at a glance

| | GPT-6.2 Astra | GPT-6.2 Sol |
|---|---|---|
| Role | Frontier model for the hardest work | Efficient model for everyday work |
| API input (per 1M tokens) | $8 | $2 |
| Cached input | $0.40 | $0.10 |
| Output | $40 | $10 |
| Price change | Input and output 20% lower than GPT-6 Astra, cached input 60% cheaper | Same as GPT-6.1 Sol |
| API name | `gpt-6.2-astra` | `gpt-6.2-sol` |

In ChatGPT, OpenAI says both models are available to Plus, Pro, Enterprise and Edu users in ChatGPT Work and Codex. Enterprise and Edu users get the faster Ultrafast mode once a workspace admin enables it.

## What OpenAI says Astra does better for marketing work

The launch post lists several improvements that map directly to marketing tasks:

- **Slides:** Astra can match a supplied template's layout, colours and typography, and OpenAI says slide titles state the main takeaway.
- **Documents and spreadsheets:** output follows the conventions of fields like sales and finance, with more direct writing.
- **Web and visual design:** better visual reasoning for layouts and imagery, including turning a written brief into an interactive browser experience.

OpenAI also published benchmark claims. On GDPval v2, Astra is up 6.2 points from GPT-6 Astra while using 22% fewer output tokens, and Sol is up 5.3 points from GPT-6.1 Sol. These are OpenAI's own figures. As with any launch benchmark, test on your real tasks before you switch a workflow. For context on the competition, see our look at [Claude Fable 5.2 for marketers](/claude-fable-5-2-marketers/), which OpenAI uses as a comparison point in several of its benchmark claims.

## The new GPT-6.2 Astra prompting rules

OpenAI's [GPT-6.2 model guide](https://developers.openai.com/api/docs/guides/latest-model?model=gpt-6.2-astra) is where the practical changes live. Four points matter most for marketing teams:

1. **Shorter by default.** Astra is "more concise and direct by default than earlier models". If your system prompt says "be concise", revisit it, or you may get answers that are too thin for long form content.
2. **Reasoning effort.** OpenAI suggests starting new integrations at `medium`. If you currently use `none` or `minimal`, use `low` instead.
3. **Do not edit history.** From GPT-6.2, the Responses API drops reasoning items when an app edits earlier conversation history, switches to certain other models, or changes the end user or organization. OpenAI warns this can lower answer quality and make the model spend more tokens repeating work.
4. **Append, do not rewrite.** To add new instructions mid conversation, OpenAI suggests appending a developer message rather than editing the original. Reusable instructions should go in a `developer` message as the first item in the input so they can be cached.

The guide also says that for long autonomous tasks, the model should stop only for big scope changes, blockers, needed decisions or irreversible actions, and state its assumptions. If you use agents for research or reporting, check that this matches how much freedom you want them to have. Our [prompt engineering guide for marketers](/prompt-engineering-marketing-professionals/) explains how to structure the system and developer parts of a prompt.

## What changes for API costs

Cost now depends heavily on caching. Cached input on Astra costs $0.40 per million tokens against $8 for fresh input, so a stable prompt prefix saves real money. OpenAI's guide says to keep the prefix unchanged between requests to preserve reasoning and keep earlier input eligible for caching. Teams migrating from GPT-5.5 or earlier should also replace `prompt_cache_retention` with `prompt_cache_options.ttl` set to `"30m"`.

Some older parameters are gone. OpenAI says to omit `temperature`, `top_p` and `logprobs` style settings from requests, and tool calling now requires the Responses API. If a developer built your chatbot with the older Chat Completions pattern, like the one in our [OpenAI API chatbot tutorial](/build-ai-chatbot-openai-api/), check these settings before switching the model name.

## What marketing teams should do now

![What marketing teams should do now with GPT-6.2 Astra and Sol](/images/infographics/ig-gpt-6-2-astra-sol-marketers-2.webp)

These steps are Brandella's recommendations, based on OpenAI's launch post and model guide.

1. **Pick three real tasks** you do every week, such as a campaign report, a slide deck and a blog brief, and run them on both Astra and Sol.
2. **Compare length and quality.** If Astra's answers are too short, remove old "be concise" lines and say the length you need.
3. **Default to Sol for routine work.** Its API output costs $10 per million tokens against $40 for Astra, so save Astra for the hardest jobs.
4. **Audit your API code** for edits to earlier messages, and move to appending developer messages instead.
5. **Remove unsupported parameters** like `temperature` and `top_p` before changing the model name.
6. **Keep a fixed prompt prefix** so caching cuts your input bill.
7. **Fact check every output** before publishing. A new model still needs a human editor, especially for figures and claims.

## FAQ about GPT-6.2 Astra

### What is the difference between GPT-6.2 Astra and Sol?
Astra is OpenAI's frontier model for the most demanding tasks. Sol is the efficient model for everyday work at a lower price, $2 input and $10 output per million tokens.

### Is GPT-6.2 Astra available in ChatGPT?
Yes. OpenAI says both models are available to Plus, Pro, Enterprise and Edu users in ChatGPT Work and Codex.

### Why are my old prompts giving shorter answers?
OpenAI says Astra is more concise and direct by default, so instructions written to shorten older models can now cut too much.

### Does GPT-6.2 cost more than GPT-6?
No. OpenAI says Astra input and output prices are 20% lower than GPT-6 Astra, and Sol prices match GPT-6.1 Sol.
