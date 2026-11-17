---
title: "Ask AdMob and Agent Skills: Google's AI Tools for App Ads"
slug: "ask-admob-gemini-agent-skills"
date: "2026-11-17T07:30:00+05:30"
author: "santajigade"
categories: ["artificial-intelligence"]
primaryCategory: "artificial-intelligence"
tags: ["AdMob", "AI agents", "Gemini", "app monetization", "MCP"]
description: "Ask AdMob, a Gemini assistant, enters testing while new AdMob agent skills let coding tools like Claude Code add app ads. What is live now and what comes next."
focusKeyword: "ask admob"
takeaways:
  - "Google announced Ask AdMob, a Gemini built assistant inside AdMob accounts, with testing starting over the next few months."
  - "AdMob agent skills are available now and let coding assistants such as Claude Code, Codex and Cursor add and check ad code."
  - "An AdMob MCP server is in early testing and should reach more developers in early 2027."
  - "Google says every recommendation and change needs developer approval before it is applied."
  - "Legacy Android Mobile Ads SDK versions face deprecation and sunset dates from June 30, 2027."
image: "/images/covers/ask-admob-gemini-agent-skills.webp"
imageAlt: "Ask AdMob Gemini assistant and AdMob agent skills"
format: "md"
---

Ask AdMob is a new Gemini built assistant that Google is bringing to AdMob, its ad network for mobile apps. Google announced it on November 16, 2026, together with AdMob agent skills that let AI coding assistants add ads to apps, and an MCP server that lets agents work with AdMob accounts.

The announcement came in a [Google Keyword blog post](https://blog.google/products/publisher-connections/new-google-admob-tools/) by Naomi Ben-Ayoun, General Manager of AdMob, as reported by [PPC Land](https://ppc.land/google-to-test-gemini-agent-that-flags-admob-setup-errors/) and [The Next Web](https://thenextweb.com/news/google-admob-ai-agents-claude-code-codex-ask-admob). Only one part is available today: the agent skills. The rest is in testing.

For app publishers and the marketers who run their monetisation, this is a clear sign that ad setup is moving from manual menus to AI agents that suggest and make changes, with a human approving each one.

![Infographic showing the status of Ask AdMob, agent skills and the AdMob MCP server](/images/infographics/ig-ask-admob-gemini-agent-skills-1.webp)

## What Ask AdMob will do

Ask AdMob is a chat assistant inside the AdMob account. According to The Next Web, it will flag setup problems, suggest ad networks that could earn more, catch pricing typos and let developers set brand safety rules in plain language.

Google says testing starts "over the next few months." PPC Land reports that the ability for Ask AdMob to act on a publisher's behalf comes later in 2027, and that every recommendation needs approval before it is applied.

## AdMob agent skills: available now

Agent skills are ready made instructions that teach an AI coding assistant how to do a specific AdMob task correctly. Google's [agent skills documentation](https://developers.google.com/admob/android/next-gen/agent-skills) for Android lists six skills, according to PPC Land:

| Skill | What it helps with |
|---|---|
| get-started | Setting up AdMob in an app |
| banner | Adding banner ads |
| interstitial | Adding full screen interstitial ads |
| rewarded | Adding rewarded ads |
| Android migration to Next-Gen | Moving to the newer Google Mobile Ads SDK |
| validate | Checking an app for setup errors before launch |

The supported coding assistants named in the coverage are Antigravity, Claude Code, Codex and Cursor. PPC Land reports the install command in the documentation is `npx skills add google/skills/skills/ads`.

## The AdMob MCP server and what it means

The third piece is an MCP server, which is still in early testing. MCP is the open standard that lets AI tools connect to outside systems, and our [MCP explainer for beginners](/mcp-model-context-protocol-explained-beginners/) covers how it works.

According to PPC Land, the AdMob MCP server is meant to read account data, create ad units and manage mediation settings, with approval before updates reach production. It should expand to more developers in early 2027.

This follows a wider pattern of companies publishing guidance for AI coding tools, similar to the [Modern Web Guidance 1.0 project for AI coding agents](/modern-web-guidance-ai-coding-agents/) that we covered last week.

## SDK deadlines app teams should note

The announcement also came with timelines for older SDKs. PPC Land reports these dates:

- Legacy Android SDK v23: sunset on June 30, 2027.
- Legacy Android SDK v24 and v25: deprecation on June 30, 2027 and sunset on June 30, 2028.
- The GMA Next-Gen SDK v1.x.x was released on April 14, 2026.

If your app still runs an older SDK, the migration skill is the practical reason to try agent skills now rather than later.

## What app publishers should do now

These are Brandella's recommendations, not official Google guidance.

![Checklist of five steps for app publishers preparing for Ask AdMob](/images/infographics/ig-ask-admob-gemini-agent-skills-2.webp)

1. **Check your SDK version.** Find which Google Mobile Ads SDK each app uses and note the June 30, 2027 dates.
2. **Try the validate skill on a test branch.** Let your coding assistant run it and review every change in code review, as you would for a human developer. Our list of [common AI web development mistakes](/ai-web-development-mistakes-chrome-top-10/) is a good reminder of what to watch for.
3. **Write down your brand safety rules.** Ask AdMob will accept rules in plain language, so prepare a short, clear list of categories you want blocked.
4. **Set approval owners.** Decide who on your team approves AI suggested changes to ad units and mediation before the tools arrive.
5. **Track revenue per user before and after.** Keep a baseline so you can measure whether AI suggestions actually help.

## Why AI agents in ad platforms need guardrails

An agent that can change ad settings can also make costly mistakes. Google's approval step for every change is the main guardrail, and teams should not switch it off even when it becomes possible.

If you are new to the idea, our guide on [what an AI agent is](/what-is-an-ai-agent/) explains the basics. The short version: agents are useful for repetitive setup work, while pricing and strategy decisions still need a person.

## FAQ about Ask AdMob

### Is Ask AdMob available now?

No. Google says testing starts over the next few months. Only the agent skills are available today.

### Which coding tools work with AdMob agent skills?

The coverage names Antigravity, Claude Code, Codex and Cursor.

### Can Ask AdMob change my account without permission?

Google says every recommendation needs approval before it is applied, including the actions planned for 2027.

### When will the AdMob MCP server open to more developers?

It is in early testing and should expand to more developers in early 2027.
