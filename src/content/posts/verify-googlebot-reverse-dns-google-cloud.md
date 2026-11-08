---
title: "Verify Googlebot Properly: Google Cloud VMs Can Pass Weak Checks"
slug: "verify-googlebot-reverse-dns-google-cloud"
date: "2026-11-08T17:55:00+05:30"
author: "santajigade"
categories: ["seo", "technical-seo"]
primaryCategory: "technical-seo"
tags: ["Googlebot", "reverse DNS", "bot verification", "log file analysis"]
description: "How to verify Googlebot without being fooled: loose reverse DNS checks let Google Cloud VMs pass as Google's crawler. What changed and how to fix your setup."
focusKeyword: "verify googlebot"
image: "/images/covers/verify-googlebot-reverse-dns-google-cloud.webp"
imageAlt: "Reverse DNS check to verify Googlebot in server logs"
format: "md"
---

If your server, firewall or log tool tries to verify Googlebot with a reverse DNS lookup, it may be trusting far more machines than Google's crawler. This week, developers of open source bot verification tools patched a gap where any server rented on Google Cloud could pass as a verified Googlebot.

The problem comes from how the check is written, not from a change at Google. Google's own [guide to verifying Google crawlers and fetchers](https://developers.google.com/crawling/docs/crawlers-fetchers/verify-google-requests?hl=en) lists three accepted domains, and one of them, googleusercontent.com, is also used for ordinary Google Cloud machines.

This matters to SEOs, developers and site owners who whitelist Googlebot in a firewall, exclude it from rate limits, or analyse crawl behaviour from logs. A loose rule can let scrapers through the front door with a Googlebot badge, and it can quietly pollute your crawl data.

## What happened this week

On November 6, 2026, the maintainers of the Ruby bot detection library agentry merged [pull request #43](https://github.com/levups/agentry/pull/43), titled "A Google Cloud VM no longer passes as a verified Googlebot." According to the pull request, its reverse DNS check had accepted any hostname under googleusercontent.com, and every Google Cloud VM gets a name in that domain.

That meant anyone could rent a VM, send a Googlebot user agent and be treated as Google's crawler. The fix now accepts only googlebot.com and google.com in the reverse DNS step, and covers Google's user triggered fetchers through the published IP ranges instead.

The same pattern has been flagged elsewhere. An issue in the spiderhead log tool is titled "[Log bot verification accepts Google Cloud VMs (*.bc.googleusercontent.com) as Googlebot](https://github.com/PavloSEO/spiderhead/issues/1532)." If two separate tools made the same mistake, many custom scripts and server rules probably did too.

## Why googleusercontent.com is the weak spot

Google's manual method has four steps: run a reverse DNS lookup on the IP, confirm the hostname ends in googlebot.com, google.com or googleusercontent.com, run a forward lookup on that hostname, and confirm it returns the original IP.

The forward lookup stops simple spoofing, because a faker cannot make Google's DNS point to their own IP. But it does not help when the IP genuinely belongs to a Google Cloud customer. That machine passes both lookups honestly, it just is not a Google crawler.

The detailed table in Google's guide is more precise than the short rule:

| Crawler type | Reverse DNS pattern Google lists | Follows robots.txt |
|---|---|---|
| Common crawlers, such as Googlebot | crawl-\*\*\*-\*\*\*-\*\*\*-\*\*\*.googlebot.com or geo-crawl-\*\*\*-\*\*\*-\*\*\*-\*\*\*.geo.googlebot.com | Yes, for automatic crawls |
| Special case crawlers, such as AdsBot | rate-limited-proxy-\*\*\*-\*\*\*-\*\*\*-\*\*\*.google.com | May or may not |
| User triggered fetchers | \*\*\*-\*\*\*-\*\*\*-\*\*\*.gae.googleusercontent.com or google-proxy-\*\*\*-\*\*\*-\*\*\*-\*\*\*.google.com | No, a user requested the fetch |

So the real Googlebot always resolves to googlebot.com. Google also notes that IPs from its user triggered fetchers list may appear when a site running on Google Cloud fetches content such as RSS feeds because one of its users asked for it. None of that is Googlebot crawling your site for Search.

## Why fake Googlebot traffic is growing

Google's Gary Illyes recently said that AI has made bot impersonation worse. As [reported by Relevant Audience](https://www.relevantaudience.com/seo/gary-illyes-ai-scraping-fake-googlebot-verification/), citing his podcast interview, Illyes said anyone can fake a Googlebot user agent in about 30 seconds and that his honeypots logged such requests from IP addresses unrelated to Google.

He also described robots.txt as a suggestion rather than an enforceable rule and pointed to network level tools such as a web application firewall. That makes the quality of your verification rule more important, because it is often the only thing deciding who gets special treatment.

We covered the cost side of this earlier in [AI bot traffic is exploding](/ai-bot-traffic-is-exploding/). A broken Googlebot check makes that problem worse, because the bots you most want to slow down can claim the one identity you never block.

## How to verify Googlebot correctly

This is Brandella's recommended setup based on Google's documentation. Adjust it to your stack.

1. **Match Googlebot to googlebot.com only.** If a request claims to be Googlebot, the reverse DNS hostname should end in googlebot.com. Do not accept googleusercontent.com for this check.
2. **Always do the forward lookup.** Resolve the hostname again and confirm it returns the same IP. Skipping this step lets anyone with control of their own reverse DNS pass.
3. **Prefer Google's IP range files at scale.** Google publishes JSON files for each group, including [common-crawlers.json](https://developers.google.com/static/crawling/ipranges/common-crawlers.json) for Googlebot. Matching against these avoids DNS lookups on every request. Refresh them on a schedule.
4. **Treat fetcher ranges separately.** If you want to allow user triggered fetchers, match them against their own JSON files, and do not give them the same treatment as Googlebot.
5. **Audit your rules today.** Search your firewall, CDN rules, server config and log scripts for "googleusercontent". Any rule that trusts the whole domain as Googlebot needs fixing.

A minimal Python version of the strict check looks like this:

```python
import socket

def is_googlebot(ip):
    try:
        host = socket.gethostbyaddr(ip)[0]
        if not host.endswith(".googlebot.com"):
            return False
        return ip in socket.gethostbyname_ex(host)[2]
    except OSError:
        return False
```

Cache the result per IP, since DNS lookups on every hit will slow your server down.

## Check your crawl data for fake Googlebot visits

If your old rule was loose, your past crawl reports may include fake visits. Rerun the analysis with the strict check and compare request counts.

Our tutorial on [Python log file analysis for Googlebot crawl behaviour](/python-log-file-analysis-googlebot-crawl-behavior/) shows how to group requests by user agent and status code, and it is easy to add the verification function above to that script. Compare the verified totals with the [Search Console Crawl Stats report](/understanding-crawl-stats-report/), which only counts real Google crawling.

A big gap between "claims to be Googlebot" and "verified Googlebot" tells you how much scraper traffic was hiding behind the name. If the real crawl volume is lower than you thought, our guide to [crawl budget](/crawl-budget-explained/) explains what to prioritise.

## The bottom line for site owners

Nothing changed in how Google crawls. What changed is that more people noticed a common shortcut in verification code. If you check only that a hostname ends in a Google domain, tighten it so Googlebot must resolve to googlebot.com, and use Google's published IP ranges for everything else.
