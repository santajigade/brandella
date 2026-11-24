---
title: "OpenAI Perplexity Figures: What the Pretraining Post Means"
slug: "openai-perplexity-pretraining-limits"
date: "2026-11-24T17:41:00+05:30"
author: "santajigade"
categories: ["artificial-intelligence"]
primaryCategory: "artificial-intelligence"
tags: ["OpenAI", "AI models", "AI safety", "pretraining"]
description: "OpenAI perplexity figures for GPT-3.5 and GPT-4 are now public, with a call for common limits on AI development. What it says and what it means for marketers."
focusKeyword: "openai perplexity"
takeaways:
  - "On November 22, 2026 OpenAI Chief Scientist Jakub Pachocki published internal pretraining perplexity figures and proposed common limits on AI development."
  - "GPT-3.5 scored about 0.99 and GPT-4 about 0.91 on OpenAI's internal codebase dataset. Lower is better."
  - "Pachocki expects further transformative capabilities around 0.68 to 0.7, and says big pretraining advances could come as soon as 2027."
  - "The post proposes no numeric cap and names no labs. It asks frontier developers to agree shared evaluation and transparency norms."
  - "For marketers, the practical lesson is to expect faster model changes and keep AI workflows easy to retest."
image: "/images/covers/openai-perplexity-pretraining-limits.webp"
imageAlt: "OpenAI perplexity figures and proposed limits on AI development"
format: "md"
---

OpenAI perplexity figures are now public. On November 22, 2026, OpenAI Chief Scientist Jakub Pachocki published [Perplexity and Intelligence](https://openai.com/index/perplexity-and-intelligence/), a post that shares internal pretraining figures for past models and proposes "common limits" that AI developers would commit not to cross.

A quick note on the name: perplexity here is a measurement used in model training, not the AI search company Perplexity. The post uses log perplexity (cross entropy loss) on a held out dataset, and lower is better.

Most marketers will never track this metric. But the post says the next big jumps in model ability could arrive as soon as 2027, and that affects every team building content, ads or search work on top of AI tools.

![OpenAI perplexity figures from November 22 2026 post: GPT-3.5 about 0.99, GPT-4 about 0.91, below 0.8 transformative capabilities, about 0.68 to 0.7 next expected window](/images/infographics/ig-openai-perplexity-pretraining-limits-1.webp)

## The OpenAI perplexity figures in the post

All numbers are measured on OpenAI's held out internal codebase dataset, for a fixed snapshot. Pachocki gives these markers:

| Log perplexity | What the post links it to |
|---|---|
| About 0.99 | GPT-3.5, the basis for the original ChatGPT |
| About 0.91 | GPT-4, proficient at chain of thought reasoning |
| Below 0.8 | Transformative capabilities in cybersecurity and mathematics |
| About 0.76 | The model began resolving open math problems |
| About 0.68 to 0.7 | Where Pachocki expects further transformative capabilities |

For context, OpenAI's [2022 ChatGPT launch post](https://openai.com/index/chatgpt/) says ChatGPT was fine tuned from a model in the GPT-3.5 series, and [GPT-4](https://openai.com/index/gpt-4-research/) was announced on March 14, 2023.

A footnote says OpenAI's loss curve shows "a steep acceleration in 2026," mostly from research and compute, with a smaller part from automation. The post also argues that "smaller gains on perplexity will correspond to larger leaps in model intelligence."

## Why OpenAI shared the numbers

Pachocki writes: "As a first step, I provide more transparency into pretraining progress at OpenAI." He admits the choice had a cost: "Publishing our internal perplexity measurements took some consideration; it gives competitors a clearer picture of where we stand."

The post does not promise to publish these figures on a schedule. It says he hopes to see more transparency across the industry.

## The proposal for common limits

The core idea is a shared measure that every lab can track. Pachocki proposes "common limits, based on perplexity and other measurements, that developers are committed to not crossing" until the ability to understand and monitor AI behaviour reaches a concrete milestone. His example of that milestone is a successor to chain of thought monitors.

He wants an industry standard with a first limit on development, which could lead to a framework for setting later limits. He also says "frontier model developers should jointly endeavour to establish shared norms for how to evaluate such models," including red teaming and shared transparency standards, by the time those models are first used.

The post names no other labs, sets no numeric cap, and does not mention governments or regulation. It is a proposal from one company's chief scientist, not an agreement.

## The limits of the metric

Pachocki lists caveats himself. Labs use different datasets, so their numbers are hard to compare. "Perplexity does not directly correspond to a task we care about." Gains from chain of thought reasoning do not show up in perplexity, and nobody knows where the floor is.

So a lower number does not tell you which chatbot writes better ad copy or answers search queries more accurately. It is a research signal about raw model ability.

## What marketers should do now

These are Brandella's recommendations based on the post, not OpenAI guidance. If model ability keeps jumping, possibly faster from 2027, plans built around today's tools will need rechecking.

![Steps for marketers after the OpenAI perplexity post: keep a test set of real tasks, rerun it after model updates, avoid workflows tied to one model, keep human review, watch how people use AI assistants, review AI policy every quarter](/images/infographics/ig-openai-perplexity-pretraining-limits-2.webp)

1. Keep a small test set of your real tasks, such as five briefs, ten ad headlines and three support answers, with the outputs you consider good.
2. Rerun that test set whenever a major model update ships, like the recent [GPT-6.2 Astra and Sol release](/gpt-6-2-astra-sol-marketers/), and note what got better or worse.
3. Avoid building workflows that only work with one model. Keep prompts and instructions in documents you can move between tools.
4. Keep human review on anything published under your brand.
5. Watch how people use AI assistants to find information. Studies like [SparkToro's analysis of ChatGPT prompts](/how-americans-use-chatgpt-sparktoro-study/) show where search behaviour is heading.
6. Review your team's AI policy every quarter rather than once a year. Our list of [AI tools for marketers](/ai-tools-for-marketers/) is a starting point for that review.

## FAQ about OpenAI perplexity figures

### Is this about the company Perplexity?

No. Perplexity here is a training metric that measures how well a model predicts text. Lower numbers are better.

### Did OpenAI announce a new model?

No. The post shares past figures and a proposal. It mentions only GPT-3.5, GPT-4 and the original ChatGPT by name.

### Have other AI labs agreed to the limits?

The post names no other labs and reports no agreement. It is a proposal that asks frontier developers to work on shared norms.

### When could the next big jump happen?

Pachocki says a similar wave of pretraining advances could come "as soon as 2027," but gives no firm date.
