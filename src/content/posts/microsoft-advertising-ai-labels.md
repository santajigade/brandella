---
title: "Microsoft Advertising AI Labels: Declare AI Images and Video"
slug: "microsoft-advertising-ai-labels"
date: "2026-11-21T22:00:00+05:30"
author: "santajigade"
categories: ["paid-media", "display-advertising"]
primaryCategory: "display-advertising"
tags: ["Microsoft Advertising", "AI labels", "AI-generated ads", "ad transparency", "Bing Ads"]
description: "Microsoft Advertising AI labels are now generally available: declare AI images and video, add a visible watermark and check detection signals. What to do."
focusKeyword: "microsoft advertising ai labels"
takeaways:
  - "Microsoft says its AI content transparency controls are now generally available for declaring AI-generated images and video in ads."
  - "You can ask for a visible AI watermark where supported, across Product, Multimedia, Audience, Display, Video and Performance Max assets."
  - "In the Campaign Management API a label cannot be cleared once set, so declare carefully."
  - "Microsoft's AI detection signal is a reference only; advertisers stay responsible for their own declarations and local disclosure laws."
image: "/images/covers/microsoft-advertising-ai-labels.webp"
imageAlt: "Microsoft Advertising AI labels for AI-generated ad images and video"
format: "md"
---

Microsoft Advertising AI labels are now live for every advertiser. In its [November 2026 product roundup](https://about.ads.microsoft.com/en/blog/post/november-2026/put-ai-to-work-engaging-customers-in-more-places-whats-new-in-microsoft-advertising-this-november), published on November 19, Microsoft wrote: "AI content transparency controls are now generally available in Microsoft Advertising." The controls let you declare AI-generated image and video content and manage visible labels on supported ad formats.

This matters to anyone who builds ad creative with AI image or video tools and runs it on Bing, the Microsoft Audience Network or Performance Max on Microsoft. Microsoft gives one reason for the feature directly: "Governments are also passing laws that may require labels on some AI-generated content."

[Search Engine Roundtable](https://www.seroundtable.com/bing-ads-made-with-ai-label-42579.html) reported on November 20 that the visible label appears in the corner of the image and reads "Made with AI". Microsoft's own post calls them AI labels and says watermark size and placement can vary by ad format, placement and serving environment.

![Microsoft Advertising AI labels: three controls and the supported ad formats](/images/infographics/ig-microsoft-advertising-ai-labels-1.webp)

## What the Microsoft Advertising AI labels controls do

Microsoft lists three capabilities.

1. Declare AI-generated image and video content. You mark whether an asset includes AI-generated content and, where supported, choose a visible watermark.
2. Manage declarations at scale. You can update one asset or many in the Ads Studio Library, or use the Microsoft Advertising APIs and product feeds.
3. Check Microsoft's AI detection signals. Microsoft offers these "as a helpful reference for supported assets", but you still decide on and remain responsible for your own declarations.

Supported formats are Product Ads, Multimedia Ads, Audience Ads, Display Ads, Video Ads and assets in Performance Max campaigns. The post's example image also shows AI labels in Text Ads with Image Extensions. Microsoft notes that available controls may vary by ad format and workflow.

## The declaration values, explained

The [AI transparency guide on Microsoft Learn](https://learn.microsoft.com/en-us/advertising/guides/ai-transparency?view=bingads-13) shows how this works underneath. Each image or video asset in the Campaign Management API has a property called `AdvertiserAILabel`, and the same idea exists in hotel property feeds and Microsoft Merchant Center product offers.

| Value | What it means |
| --- | --- |
| `AIWithVisibleWatermark` | The asset contains AI-generated content and you request a visible AI watermark where supported |
| `AIContent` | The asset contains AI-generated content, but no visible watermark is requested |
| `NoAIContent` | You declare the asset does not contain AI-generated content |

Two details are easy to miss. `AIWithVisibleWatermark` asks Microsoft to add a watermark; it does not mean the file already has one. And in the Campaign Management API, "After a label has been set, it cannot be cleared." Setting `NoAIContent` later is a new declaration, not a way to remove the label. Merchant Center works differently: there an omitted or empty `advertiser_ai_label` attribute clears the declaration to null, and the field only works when the OfferAdvertiserAILabel store pilot is enabled.

The guide also opens with a note that "Not everyone has this feature yet", even though the blog post calls the controls generally available. If you don't see the option in your account or API version, that may be why.

## How the AI detection signal fits in

Microsoft also exposes a read-only property, `SystemAIDetectionSignal`. It can return `MicrosoftAIGenerated` (the asset was made with Microsoft AI), `AISignatureDetected` (an AI-content signature was found) or `NoSignalDetected`.

The last value is the one to be careful with. Microsoft's guide says plainly that `NoSignalDetected` "does not establish that the asset contains no AI-generated content." An image you edited with a tool that leaves no signature can still be AI content. Treat the signal as a second opinion.

This is the same direction Google has taken. We covered how [Google Ads AI labels expanded to California, South Korea and Vietnam](/google-ads-ai-labels-expand-california-korea-vietnam/) and why [an AI label will not save an ad that breaks the impersonation policy](/google-ads-ai-impersonation-policy/). Labels are about disclosure, and the normal ad policies still apply.

## What advertisers should do now

The following steps are Brandella's recommendations, not an official Microsoft checklist.

![What to do now about Microsoft Advertising AI labels: five steps](/images/infographics/ig-microsoft-advertising-ai-labels-2.webp)

1. List every image and video asset in your Ads Studio Library that came from an AI tool, including product shots retouched with generative fill and backgrounds made by AI.
2. Decide on a policy per brand: which AI assets get `AIWithVisibleWatermark` and which get `AIContent`. Base it on the disclosure laws in the countries you target, since Microsoft says you remain "responsible for making sure your ads follow local laws and disclosure rules."
3. Check Microsoft's detection signal against your list. Where Microsoft flags an asset you thought was clean, find out why before you declare.
4. Declare carefully the first time. Because API labels cannot be cleared, test on a few assets before you bulk update through the API or Ads Studio Library.
5. For Shopping, add the `advertiser_ai_label` attribute to your product feed if your store is in the pilot, and remember that a full Content API update replaces the whole offer.

If you also run Performance Max on Google, it helps to keep one AI asset register for both platforms. Our guide to [Performance Max visual guidelines](/performance-max-visual-guidelines/) covers how Google lets you steer AI-made images, and the [Microsoft Advertising automated bidding upgrade](/microsoft-advertising-automated-bidding-upgrade/) from the same week is worth reading if you manage Microsoft campaigns.

## FAQ about Microsoft Advertising AI labels

### Is the Made with AI label automatic?

Microsoft's post does not say labels are added automatically. You declare AI content yourself and can request a visible watermark where supported. Microsoft's detection signal is offered as a reference only.

### Which ad formats support AI labels?

Microsoft lists Product Ads, Multimedia Ads, Audience Ads, Display Ads, Video Ads and Performance Max assets. Its example image also shows labels on Text Ads with Image Extensions. Controls may vary by format and workflow.

### Can I remove an AI label after setting it?

Not through the Campaign Management API, where a label cannot be cleared once set. In Merchant Center product feeds, an empty or omitted attribute clears the declaration to null.

### Does Microsoft say which countries require AI labels?

No. The post says governments are passing laws that may require labels, and that advertisers decide whether their content needs one. Check the rules in each market you target.
