---
title: "Cross-Origin Storage API: Chrome's Plan to Share Big Files"
slug: "cross-origin-storage-api-chrome"
date: "2026-11-15T18:35:00+05:30"
author: "santajigade"
categories: ["development", "javascript"]
primaryCategory: "javascript"
tags: ["Chrome", "web performance", "JavaScript", "browser AI"]
description: "The Cross-Origin Storage API proposal lets sites share large files like AI models and Wasm by hash. How it works, its status and what web teams should do."
focusKeyword: "cross-origin storage api"
takeaways:
  - "Chrome introduced the Cross-Origin Storage API proposal on November 10, 2026, as an early stage WICG proposal, not a shipped standard."
  - "Files are stored and found by their cryptographic hash, so one copy of a large file can be reused across sites."
  - "Main use cases are browser AI models, Wasm modules, shared libraries, game engines and large web fonts."
  - "A Hugging Face test showed a 177 MB Whisper model download duplicated on a second origin without shared storage."
  - "You can test it today with a polyfill extension, but production sites should keep normal caching as the default."
image: "/images/covers/cross-origin-storage-api-chrome.webp"
imageAlt: "Cross-Origin Storage API proposal in Chrome"
format: "md"
---

The Cross-Origin Storage API is a new browser proposal that would let different websites share one stored copy of a large file, such as an AI model or a WebAssembly module. Thomas Steiner of the Chrome team introduced it on the [Chrome for Developers blog](https://developer.chrome.com/blog/introducing-cross-origin-storage?hl=en) on November 10, 2026, and Search Engine Roundtable flagged the post in its November 13 daily recap.

Today, browsers partition their cache by site. If two websites use the same 100 MB model, a visitor downloads and stores it twice. The proposal tries to fix that without reopening the privacy problems that cache partitioning was built to solve.

It is not shipping in Chrome yet. But for teams that build AI features into web pages, it is worth understanding now, because it could change how fast those features load for first time visitors.

![Cross-Origin Storage API at a glance: status, how it works and main use cases](/images/infographics/ig-cross-origin-storage-api-chrome-1.webp)

## What the Cross-Origin Storage API does

The idea is content addressing. Instead of asking for a file by URL, a page asks for it by its cryptographic hash, such as a SHA-256 value. If the browser already holds a file with that hash, and the page is allowed to see it, the page gets it without a network request.

The [WICG draft specification](https://wicg.github.io/cross-origin-storage/), dated November 3, 2026, defines one entry point: `navigator.crossOriginStorage.getFileHandle(hash, options)`. The hash has an algorithm and a lowercase hex value, and SHA-1 is rejected. With `create: true` a page can write a new file, and the browser checks that the bytes match the hash before saving.

The Chrome post also lists planned integrations for HTML attributes, a CSS function, JavaScript import attributes and a `fetch()` request option.

## Why Chrome is proposing it now

Large files are becoming normal on the web. The Chrome post names AI models such as Gemma or Llama variants as a major motivation, along with Wasm modules from tools like Flutter, shared JavaScript libraries, game engine runtimes such as Godot and Unity, and large icon or emoji fonts.

A June 2026 [Hugging Face guest post](https://huggingface.co/blog/cross-origin-storage) shows the cost. Loading the Whisper tiny.en model on a second origin duplicated 177 MB of download and storage. The shared ONNX Runtime Wasm file it uses is 4,733 kB, and two different models depend on it, so shared storage would keep only one copy.

| Today | With Cross-Origin Storage |
| --- | --- |
| Each site downloads its own copy of a model | A file stored once can be reused by permitted sites |
| Files requested by URL | Files requested by hash |
| Cache partitioned per site | Sharing limited to named origins or popular public files |

## How privacy is protected

The spec is careful here, because shared storage could reveal which sites a person visited. Global sharing to all sites only works for hashes on a Public Hash List, a popularity based allowlist. Otherwise sharing is limited to same site origins or a list of named origins, and a file server can restrict which origins may be named.

Browsers may also randomly hide global results to make probing unreliable, and entries do not store the source URL. Access is controlled by a `cross-origin-storage` Permissions Policy feature that defaults to the same origin. No user permission prompt is defined, and users should be able to view and delete entries in browser settings.

## What web teams should do now

![What web teams should do now about the Cross-Origin Storage API](/images/infographics/ig-cross-origin-storage-api-chrome-2.webp)

These steps are Brandella recommendations, not official Chrome guidance.

1. **Do not ship it to production yet.** It is an early stage proposal with an Intent to Prototype, and Mozilla and WebKit have only been asked for standards positions.
2. **Measure your heavy files.** List every file over a few megabytes your pages load, such as models, Wasm and fonts. These are the candidates if the API ships.
3. **Try the polyfill.** The Chrome post says a polyfill extension is available for Chrome, Firefox and Safari. Test it on a staging site, not on visitors.
4. **Test with Transformers.js.** If you run browser AI, the Hugging Face post shows an experimental flag, `env.experimental_useCrossOriginStorage = true`, which falls back to the normal Cache API when the API is missing.
5. **Keep normal caching strong.** Good cache headers still matter most. Our guide to [browser caching for speed and SEO](/browser-caching-explained-website-speed-seo/) covers the basics.
6. **Watch page experience.** Big downloads hurt loading and responsiveness, so track [Core Web Vitals in 2026](/core-web-vitals-2026/) on pages with AI features.

Heavy work in the browser also blocks the main thread, so pair any model loading with [JavaScript Web Workers](/javascript-web-workers/). If your team is new to models, start with [large language models explained](/large-language-models-explained/).

## Who is already experimenting

The Chrome post lists experimental, typically opt in, interest from Emscripten, Flutter, Transformers.js, WebLLM, wllama, Nuxt.js, a Prompt API polyfill and Prebid.js. The spec editors are Thomas Steiner and François Beaufort of Google and Christian Liebel of Thinktecture.

A W3C TAG design review is underway and cross browser tests are in progress. None of that means the API will ship as written, so treat today's method names as subject to change.

## FAQ about the Cross-Origin Storage API

### Can I use the Cross-Origin Storage API in Chrome today?

Not natively. It is an early stage proposal. You can test it with the polyfill extension the Chrome team links in its post.

### Is this the same as the HTTP cache?

No. The HTTP cache is partitioned by site and keyed by URL. Cross-Origin Storage finds files by hash and only shares them under the rules in the spec.

### Does it affect SEO?

Not directly. It could make pages with large AI or Wasm files load faster for returning visitors across sites, which helps user experience, but it is not a ranking signal.

### Could sites use it to track people?

The spec addresses that risk with the Public Hash List, origin limits, random hiding of global results and no stored source URLs.
