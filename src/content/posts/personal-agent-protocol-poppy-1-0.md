---
title: "Personal Agent Protocol 1.0: Poppy Goes Live on Shopify"
slug: "personal-agent-protocol-poppy-1-0"
date: "2026-11-16T07:40:00+05:30"
author: "santajigade"
categories: ["artificial-intelligence"]
primaryCategory: "artificial-intelligence"
tags: ["AI agents", "Personal Agent Protocol", "Sierra", "Meta Muse", "Shopify", "agentic commerce"]
description: "Personal Agent Protocol 1.0 (Poppy) is live on every Shopify store and in Meta's Muse agent. What it does, who backs it and what brands should do now."
focusKeyword: "personal agent protocol"
takeaways:
  - "Sierra released Personal Agent Protocol (Poppy) 1.0 on November 13, 2026, a standard for personal AI agents to deal with companies."
  - "Every Shopify store now publishes a Poppy file automatically, and Meta's Muse agent looks for Poppy first on every site it visits."
  - "Poppy builds on MCP, OpenAPI and UCP and uses OAuth, so customers control what their agent may do."
  - "More than 100 companies back it, and Mercury, Synchrony and Turkish Airlines are going live."
  - "Brands should map which customer tasks an agent could do, then test Sierra's implementation kit and validator."
image: "/images/covers/personal-agent-protocol-poppy-1-0.webp"
imageAlt: "Personal Agent Protocol Poppy 1.0 release"
format: "md"
---

The Personal Agent Protocol, nicknamed Poppy, reached version 1.0 on November 13, 2026. Customer service AI company Sierra announced the release in a post titled [Releasing Personal Agent Protocol 1.0](https://sierra.ai/blog/releasing-poppy), describing Poppy as a standard that lets personal agents "interact with companies through business agents, websites, and APIs".

Two partners make this more than a paper standard. Poppy is switched on for everyone who uses Muse, Meta's AI agent, and Shopify has enabled it for every merchant on its platform. Sierra says more than 100 companies now back the protocol.

For marketers and ecommerce teams, this matters because a growing share of visits may come from an agent acting for a customer rather than the customer in person. Poppy is one of the first attempts to give those agents a common, permission based way to talk to a business.

![Personal Agent Protocol 1.0 in numbers](/images/infographics/ig-personal-agent-protocol-poppy-1-0-1.webp)

## What the Personal Agent Protocol does

Sierra published a draft of Poppy the month before and named its first design partners: Meta, Genesys, Instinct, NiCE, Rocket, Shopify, Stripe and Walmart. Version 1.0 reflects about five weeks of testing against real websites, APIs and agents.

The protocol mostly builds on standards that already exist: MCP, OpenAPI and UCP. If MCP is new to you, our [beginner guide to the Model Context Protocol](/mcp-model-context-protocol-explained-beginners/) explains it in plain English. Authentication runs through OAuth, which Sierra says means "customers control what personal agents can and can't do" and can change that access over time.

Poppy covers the step before a purchase or a service request. It is how an agent identifies itself and learns what it may do on a site. Sierra says UCP "handles the shopping itself, like finding products, filling a cart, and checking out." Version 1.0 also gives companies more ways to give guidance to the visiting agent and to collect feedback from it.

## Shopify and Meta Muse make it large from day one

Every Shopify store now publishes a Poppy file automatically, so merchants do not need to build anything. Sierra notes Shopify powers businesses in more than 175 countries and every store already supports UCP by default.

The commerce extension was co-authored by Shopify. It connects to UCP Ask so a shopper's agent can talk directly to a store's agent. Agents can shop as a guest or sign in to a customer's account, and they must ask the customer before certain actions.

On the demand side, Sierra says Muse "automatically looks for Poppy first on every site it visits". That is significant because Muse is already a big source of agent traffic. In a September 2026 post, security firm HUMAN said that in its early observations [Muse accounted for an average of 72% of daily AI agent requests](https://www.humansecurity.com/learn/blog/meta-muse-agentic-traffic/), and that 84% of Muse requests targeted product and search pages. HUMAN sells agent traffic products, so treat those figures as one vendor's sample.

## Who is already using Poppy

Sierra says 60 new companies joined the design partner group, taking it past 100. Named examples include Affirm, Delta Air Lines, Intuit, Salesforce, Twilio, Wayfair and Zoom. Three companies are going live:

| Company | What a personal agent can do, per Sierra |
|---|---|
| Mercury | Check balances, review transactions, categorise spending, manage budgets and receipts, and start payments that pass the account's approval policy first |
| Synchrony | Work is underway to help customers find products while weighing affordability, financing and offers across more than 500,000 merchant locations |
| Turkish Airlines | Check fares, flight status and stopovers, look up bookings by reference and surname, and find business class upgrades that customers approve before paying |

The common thread is approval. In every example, the customer stays in the loop for money moving actions. That design choice answers some of the worries that led brands such as United to restrict agents, which we covered in our post on the [United Airlines AI agents ban](/united-airlines-ai-agents-ban/).

## Why this matters for marketers

Agents change who reads your site. When an agent compares products for someone, your page copy, structured data and policies are read by software that then summarises them for a person. Poppy adds a layer where you can tell that software what it is allowed to do and give it guidance.

It also sits next to the payment side of agentic commerce. OpenAI recently gave agents a way to pay, as explained in our article on [ChatGPT Wallet and AI agent purchases](/chatgpt-wallet-ai-agent-purchases/). Discovery, permission and payment are all being standardised at the same time, so stores that prepare early will be easier for agents to deal with.

Our view, not an official statement: Poppy is not yet a universal standard. It is backed by one vendor and its partners, and competing approaches may appear. But with Shopify and Muse on board, it is worth understanding now.

## What brands should do now

![Steps to prepare your site for personal AI agents](/images/infographics/ig-personal-agent-protocol-poppy-1-0-2.webp)

1. **If you are on Shopify, check your store.** Your store already publishes a Poppy file, so make sure your product data, shipping rules and return policy are accurate, because an agent may read them.
2. **List the tasks customers repeat.** Order status, bookings, returns and account questions are the tasks agents will try first. Decide which ones you are happy for an agent to do.
3. **Separate agent traffic in analytics.** Agent sessions can distort conversion and funnel numbers. Tools such as [Microsoft Clarity agentic analytics](/microsoft-clarity-agentic-analytics/) help you see what agents do on your pages.
4. **Read the spec before you build.** The [Poppy 1.0 specification](https://personalagentprotocol.org/docs/1.0/spec) explains roles and authentication. Hand it to your developers along with this article.
5. **Test with the official kit.** Sierra's [implementation kit for companies](https://personalagentprotocol.org/kit/company) walks through setup and includes a validator.
6. **Write a clear agent policy.** State in your terms which agent actions you allow and which need human confirmation, so customers and agents both know the rules.

## FAQ about the Personal Agent Protocol

### What is the Personal Agent Protocol?

It is a standard, also called Poppy, that lets a customer's personal AI agent identify itself to a company and learn what it may do through business agents, websites and APIs. Version 1.0 was released on November 13, 2026.

### Do Shopify merchants need to do anything?

Sierra says no extra implementation work is needed, because every Shopify store publishes a Poppy file automatically. Merchants should still keep product and policy information accurate.

### Is Poppy the same as UCP?

No. Sierra says UCP handles shopping tasks such as finding products, filling a cart and checking out, while Poppy handles the earlier step where an agent identifies itself and learns what it may do.

### Can an agent spend money without the customer?

In the examples Sierra gives, money moving actions need approval. Mercury payments pass the account's approval policy, and Turkish Airlines upgrades are approved by the customer before paying.
