---
title: "Core Web Vitals for Single Page Applications: 5 Proven Fixes"
slug: "core-web-vitals-for-single-page-applications"
date: "2026-10-01T05:06:34"
updated: "2026-10-01T05:06:59"
author: "santajigade"
categories: ["core-web-vitals"]
primaryCategory: "core-web-vitals"
description: "Core Web Vitals for single page applications breaks differently than a static site. See why INP and LCP suffer after client side navigation, and how to fix it."
focusKeyword: "core web vitals single page applications"
image: "/wp-content/uploads/2026/10/Core-Web-Vitals.webp"
imageAlt: "Core Web Vitals"
words: 2106
views: 24
format: "html"
---
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<style>
@import url('https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600;700;800&display=swap');

#bx-article, #bx-article * { box-sizing: border-box; }
#bx-article {
  --bx-disp: 'Open Sans', sans-serif;
  --bx-body: 'Open Sans', sans-serif;
  --bx-green: #5DB92E;
  --bx-green-deep: #4a9e24;
  --bx-charcoal: #2b2b2b;
  --bx-charcoal-soft: #4a4a4a;
  --bx-dark: #20272C;
  font-family: var(--bx-body);
  font-weight: 400;
  font-size: 17px;
  line-height: 1.75;
  color: var(--bx-charcoal);
  max-width: 860px;
  margin: 0 auto;
  padding: 10px 18px 40px;
}
#bx-article a { color: var(--bx-green-deep); text-decoration: none; font-weight: 600; }
#bx-article a:hover { color: var(--bx-charcoal); }
#bx-article p { font-size: 17px; margin: 0 0 16px; }
#bx-article img, #bx-article svg { max-width: 100%; height: auto; }

.bx-pills { display: flex; flex-wrap: wrap; gap: 8px; margin: 18px 0 20px; }
.bx-pill {
  font-family: var(--bx-disp); font-size: 13px; font-weight: 700;
  color: var(--bx-green-deep); background: #eef8e6; border: 1px solid var(--bx-green);
  padding: 5px 14px; border-radius: 30px; letter-spacing: .3px;
}

.bx-lede {
  font-style: italic; font-size: 17px; color: var(--bx-charcoal-soft);
  border-left: 4px solid var(--bx-green); padding: 6px 20px; margin: 0 0 28px;
}

.bx-section-head { margin: 46px 0 18px; }
.bx-num {
  font-family: var(--bx-disp); font-weight: 800; font-size: 15px; color: var(--bx-green-deep);
  letter-spacing: 2px; display: block; margin-bottom: 4px;
}
#bx-article h2.bx-h2 {
  font-family: var(--bx-disp); font-weight: 700; font-size: 25px; color: var(--bx-charcoal);
  margin: 0 0 10px; line-height: 1.35;
}
.bx-rule { width: 64px; height: 4px; background: var(--bx-green); border-radius: 2px; }

h3.bx-h3 { font-family: var(--bx-disp); font-weight: 700; font-size: 20px; color: var(--bx-charcoal); margin: 26px 0 12px; }

.bx-code-wrap { margin: 18px 0 26px; border-radius: 10px; overflow: hidden; background: #1e1e2e; box-shadow: 0 2px 10px rgba(0,0,0,.15); }
.bx-code-title {
  background: #171724; color: #a9adc1; font-family: 'Courier New', monospace; font-size: 13px;
  padding: 10px 16px; border-bottom: 1px solid #2f2f45; letter-spacing: .3px;
}
.bx-code-wrap pre { margin: 0; padding: 18px 20px; overflow-x: auto; }
.bx-code-wrap code { font-family: 'Courier New', Consolas, monospace; font-size: 16px; line-height: 1.65; color: #e4e4f0; white-space: pre; }
.tok-kw { color: #c792ea; }
.tok-fn { color: #82aaff; }
.tok-str { color: #f5d76e; }
.tok-val { color: #f78c50; }
.tok-cm  { color: #7c7f93; font-style: italic; }
.tok-sel { color: #9ece6a; }
.tok-prop{ color: #7fdbca; }

.bx-shot { margin: 18px 0 28px; border-radius: 10px; overflow: hidden; box-shadow: 0 2px 10px rgba(0,0,0,.15); }
.bx-shot img { display: block; width: 100%; }
.bx-shot-caption { font-size: 14px; color: var(--bx-charcoal-soft); text-align: center; margin: 8px 0 0; font-style: italic; }

.bx-tip { background: #eef8e6; border-left: 4px solid var(--bx-green); border-radius: 8px; padding: 16px 20px; margin: 20px 0 26px; }
.bx-tip-label {
  display: flex; align-items: center; gap: 8px; font-family: var(--bx-disp); font-weight: 800;
  font-size: 14px; letter-spacing: 1.2px; color: var(--bx-green-deep); text-transform: uppercase; margin: 0 0 6px;
}
.bx-tip-label::before { content: ""; width: 8px; height: 8px; border-radius: 50%; background: var(--bx-green); display: inline-block; }
.bx-tip p { margin: 0; font-size: 17px; color: var(--bx-charcoal); }

.bx-fact { background: #eef8e6; border: 1px solid #d9edcd; border-radius: 10px; padding: 16px 20px 16px 60px; margin: 20px 0 26px; position: relative; }
.bx-fact::before {
  content: "?"; position: absolute; left: 16px; top: 18px; width: 28px; height: 28px; border-radius: 50%;
  background: var(--bx-charcoal); color: var(--bx-green); font-family: var(--bx-disp); font-weight: 800; font-size: 15px;
  display: flex; align-items: center; justify-content: center;
}
.bx-fact-label {
  display: block; font-family: var(--bx-disp); font-weight: 800; font-size: 14px;
  letter-spacing: 1.2px; color: var(--bx-charcoal-soft); text-transform: uppercase; margin: 0 0 4px;
}
.bx-fact p { margin: 0; font-size: 17px; color: var(--bx-charcoal); }

.bx-table-wrap { overflow-x: auto; margin: 20px 0 30px; border-radius: 10px; }
table.bx-table { width: 100%; border-collapse: collapse; font-size: 17px; min-width: 620px; }
table.bx-table thead tr { background: #2b2b2b !important; }
table.bx-table thead th { background: #2b2b2b !important; color: #ffffff !important; font-family: var(--bx-disp); font-weight: 700; text-align: left; padding: 13px 14px; font-size: 17px; }
table.bx-table tbody td { padding: 12px 14px; font-size: 17px; border-bottom: 1px solid #e7f2dd; }
table.bx-table tbody tr:nth-child(odd) { background: #f4faef; }
table.bx-table tbody tr:nth-child(even) { background: #ffffff; }

.bx-checklist { list-style: none; margin: 18px 0 28px; padding: 0; display: grid; gap: 12px; }
.bx-checklist li {
  background: #fff; border: 1px solid #e9e9e9; border-left: 4px solid var(--bx-green);
  border-radius: 8px; padding: 14px 16px 14px 44px; position: relative; font-size: 17px;
}
.bx-checklist li::before {
  content: "✓"; position: absolute; left: 14px; top: 13px; color: var(--bx-green-deep); font-weight: 800; font-size: 17px;
}
.bx-checklist b { color: var(--bx-charcoal); }

.bx-faq { margin: 20px 0 30px; display: grid; gap: 12px; }
.bx-faq-item {
  border: 1px solid #e6efe0; border-radius: 12px; background: #fff;
  transition: border-color .2s ease, box-shadow .2s ease;
}
.bx-faq-item.open { border-color: var(--bx-green); box-shadow: 0 2px 12px rgba(93,185,46,.1); }
.bx-faq-q {
  width: 100%; text-align: left; background: none; border: none; cursor: pointer;
  display: flex; align-items: center; gap: 14px;
  font-family: var(--bx-disp); font-weight: 700; font-size: 17px; color: var(--bx-charcoal);
  padding: 16px 44px 16px 16px; position: relative;
}
.bx-faq-num {
  flex-shrink: 0; width: 30px; height: 30px; border-radius: 50%; background: var(--bx-green);
  color: #fff; font-family: var(--bx-disp); font-weight: 800; font-size: 13px;
  display: flex; align-items: center; justify-content: center;
}
.bx-faq-q::after {
  content: "+"; position: absolute; right: 16px; top: 50%; transform: translateY(-50%);
  color: var(--bx-green-deep); font-size: 22px; font-weight: 400; transition: transform .25s ease;
}
.bx-faq-item.open .bx-faq-q::after { transform: translateY(-50%) rotate(45deg); }
.bx-faq-a { max-height: 0; overflow: hidden; transition: max-height .3s ease; }
.bx-faq-a p {
  margin: 0 16px 16px 60px; padding: 2px 0 2px 16px; font-size: 17px; color: var(--bx-charcoal-soft);
  border-left: 3px solid #d9edcd;
}

.bx-related { margin: 34px 0; }
.bx-related h3 {
  font-family: var(--bx-disp); font-size: 19px; color: var(--bx-charcoal); margin: 0 0 16px;
  display: flex; align-items: center; gap: 10px;
}
.bx-related h3::before {
  content: ""; width: 22px; height: 4px; background: var(--bx-green); border-radius: 2px; display: inline-block;
}
.bx-related-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
.bx-related-card {
  display: flex; align-items: center; gap: 12px; background: #fff;
  border: 1px solid #e6efe0; border-left: 4px solid var(--bx-green); border-radius: 10px;
  padding: 15px 16px; transition: box-shadow .2s ease, border-color .2s ease;
}
.bx-related-card:hover { border-color: var(--bx-green); box-shadow: 0 2px 12px rgba(93,185,46,.12); }
.bx-related-title { font-family: var(--bx-disp); font-weight: 700; font-size: 15px; color: var(--bx-charcoal); line-height: 1.4; }
.bx-related-arrow { margin-left: auto; color: var(--bx-green-deep); font-size: 18px; flex-shrink: 0; }
@media (max-width: 640px) { .bx-related-grid { grid-template-columns: 1fr; } }

.bx-learn { margin: 34px 0 8px; }
.bx-learn h2 { font-family: var(--bx-disp); font-size: 22px; color: var(--bx-charcoal); margin-bottom: 14px; }
.bx-learn-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
.bx-learn-card {
  border: 1px solid #e3efdc; border-radius: 10px; padding: 12px 14px 12px 18px; background: #fbfefa;
  display: flex; gap: 10px; align-items: flex-start; position: relative; overflow: hidden;
}
.bx-learn-card::before { content: ""; position: absolute; left: 0; top: 0; bottom: 0; width: 4px; background: var(--bx-green); }
.bx-learn-num {
  flex-shrink: 0; width: 28px; height: 28px; border-radius: 50%; background: var(--bx-green);
  color: #fff; font-family: var(--bx-disp); font-weight: 800; font-size: 13px;
  display: flex; align-items: center; justify-content: center;
}
.bx-learn-card h4 { margin: 0 0 3px; font-family: var(--bx-disp); font-size: 15px; color: var(--bx-charcoal); }
.bx-learn-card p { margin: 0; font-size: 15px; line-height: 1.5; color: var(--bx-charcoal-soft); }
@media (max-width: 640px) { .bx-learn-grid { grid-template-columns: 1fr; } }

.bx-cta {
  background: linear-gradient(120deg, var(--bx-green) 0%, var(--bx-green-deep) 100%);
  border-radius: 14px; padding: 38px 32px; text-align: center; margin: 40px 0 20px; color: #fff;
}
.bx-cta h3 { font-family: var(--bx-disp); font-size: 24px; margin: 0 0 10px; color: #fff; }
.bx-cta p { color: #eafbe0; margin: 0 0 22px; font-size: 17px; }
.bx-cta-btns { display: flex; flex-wrap: wrap; gap: 12px; justify-content: center; }
.bx-cta-btns a {
  background: #fff; color: var(--bx-green-deep) !important; font-family: var(--bx-disp); font-weight: 700;
  padding: 12px 26px; border-radius: 30px; font-size: 15px;
}
.bx-cta-btns a.bx-cta-outline { background: transparent; color: #fff !important; border: 2px solid #fff; }

.bx-ad { text-align: center; margin: 34px 0; padding: 18px 0; border-top: 1px dashed #cfcfcf; border-bottom: 1px dashed #cfcfcf; }
</style>

<div id="bx-article">

<div class="bx-pills">
  <span class="bx-pill">SEO</span>
  <span class="bx-pill">Core Web Vitals</span>
</div>

<p>Hey! If your React or Vue app looks fast in a lab test but real visitors keep complaining that tapping around feels sluggish, you are not imagining things, and this one is for you.</p>

<p class="bx-lede"><em>Picture this: you ship a shiny new app, Lighthouse hands you a green score on the homepage, and then real users start clicking through routes and everything suddenly feels heavy. That gap between a lab score and real user frustration is exactly where Core Web Vitals for single page applications gets complicated, and it is worth understanding before your team spends another sprint chasing the wrong number.</em></p>

<div class="bx-section-head">
  <span class="bx-num">01</span>
  <h2 class="bx-h2" id="why-core-web-vitals-for-single-page-applications-is-a-different-proble">Why Core Web Vitals for single page applications is a different problem</h2>
  <div class="bx-rule"></div>
</div>

<p>Most Core Web Vitals advice assumes a traditional page load: the browser requests a document, the server streams HTML, and the page settles. A single page app built with React, Vue, or Angular works differently. One bundle boots up once, then quietly rewrites the DOM every time someone clicks a link, and the browser never fires another full navigation.</p>

<p>That architecture is useful for app like interfaces, but it breaks an assumption baked into the original metrics: that a page load and a page view are the same event. Google's own engineering team has said plainly that single page apps have "never been fully supported" by these metrics, since the browser has no clean signal for where one screen ends and the next begins.</p>

<p>In practice this shows up as two pain points: Interaction to Next Paint getting worse the deeper someone navigates, and Largest Contentful Paint looking fine on the first load but meaningless on every route after that. This guide on Core Web Vitals for single page applications walks through why both happen and which fixes actually move the needle.</p>

<div class="bx-ad">
  <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-3931314195561246" data-ad-slot="4249015278" data-ad-format="auto" data-full-width-responsive="true"></ins>
  <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
</div>

<div class="bx-section-head">
  <span class="bx-num">02</span>
  <h2 class="bx-h2" id="the-inp-problem-heavy-javascript-on-every-route-change">The INP problem: heavy JavaScript on every route change</h2>
  <div class="bx-rule"></div>
</div>

<p>Interaction to Next Paint measures how long the browser stays frozen after someone taps, clicks, or types, until the next frame paints. On a server rendered site that mostly means keeping handlers light. In a single page app it is bigger, since one click on a nav link can trigger route matching, data fetching, component teardown, a fresh render pass, and rehydration, all on the same main thread.</p>

<p><a href="https://vercel.com/blog/improving-interaction-to-next-paint-with-react-18-and-suspense">Vercel's own engineering team documented</a> this clearly while working on <code>nextjs.org</code> itself: before they adopted React 18's selective hydration with Suspense, loading a full page of JavaScript before any component could respond to input was pushing Total Blocking Time to 430 milliseconds. After moving to Suspense boundaries that let the browser do other work while hydration finished in the background, that figure dropped to 80 milliseconds, and the resulting INP came in at a comfortably good 48 milliseconds.</p>

<p>That is the lesson for anyone chasing <a href="/interaction-to-next-paint-inp-explained/">a better INP score</a> inside a framework heavy app: the problem is rarely one slow function, it is the sheer amount of synchronous work a route change asks of the main thread in one burst.</p>

<div class="bx-tip">
  <p class="bx-tip-label">Tip</p>
  <p>Record a DevTools trace while clicking through your busiest in app routes, and look for long tasks over 50 milliseconds right after the click. That trace tells you more about real INP than any lab score.</p>
</div>

<div class="bx-section-head">
  <span class="bx-num">03</span>
  <h2 class="bx-h2" id="the-lcp-problem-content-that-only-appears-after-the-bundle-loads">The LCP problem: content that only appears after the bundle loads</h2>
  <div class="bx-rule"></div>
</div>

<p>Largest Contentful Paint measures how soon the biggest visible element shows up on screen, and a passing score needs under 2.5 seconds. Client rendered apps tend to fail this quietly: the server sends back a near empty HTML shell, the browser has to download, parse, and execute the JavaScript bundle before a single word of real content exists, and only then does the framework build the DOM and paint something meaningful.</p>

<p>Google's own documentation on client rendering spells out why this hurts: unlike HTML streamed from a server, which the browser's preload scanner can act on immediately, resources referenced inside JavaScript generated markup stay invisible to that scanner until the script runs. Images, fonts, and hero content effectively queue up behind the entire bundle instead of loading in parallel with it.</p>

<p>This is why <a href="/what-is-largest-contentful-paint-lcp/">LCP guidance written for ordinary pages</a> can feel incomplete for a single page app. A static site worries about image compression and font loading; a client rendered app solves those problems while also racing a JavaScript bundle just to get content on the canvas.</p>

<div class="bx-fact">
  <span class="bx-fact-label">Did You Know</span>
  <p>Astro's 2023 Web Framework Performance Report, built on real Chrome User Experience Report data, found that only roughly one in four Next.js sites and one in five Nuxt sites passed the overall Core Web Vitals assessment, while the industry wide INP pass rate sat at 60.9 percent. <a href="https://astro.build/blog/2023-web-framework-performance-report/">Astro</a> credited the gap to how much client side JavaScript these architectures ship by default.</p>
</div>

<div class="bx-ad">
  <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-3931314195561246" data-ad-slot="4249015278" data-ad-format="auto" data-full-width-responsive="true"></ins>
  <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
</div>

<div class="bx-section-head">
  <span class="bx-num">04</span>
  <h2 class="bx-h2" id="soft-navigations-why-your-field-data-never-showed-the-real-picture">Soft navigations: why your field data never showed the real picture</h2>
  <div class="bx-rule"></div>
</div>

<p>Here is the part most teams never realize: the Chrome User Experience Report, the real world dataset behind the ranking signal, historically only measured the first hard page load of a session. Every route change afterward, no matter how slow, was invisible to that field data, because the browser never recorded a traditional navigation event for it.</p>

<p><a href="https://developer.chrome.com/docs/web-platform/soft-navigations-experiment">Chrome engineers call these in app transitions soft navigations</a>, and they built a dedicated detection system to finally close the gap. A soft navigation now has to meet three conditions: a real user interaction kicked it off, the visible URL changed, and the browser actually painted something new as a result. Chrome 151 shipped standardized APIs for this, including <code>PerformanceSoftNavigation</code> and a new <code>InteractionContentfulPaint</code> entry that lets LCP be measured per route instead of only once per session.</p>

<p>For anyone building a RUM dashboard, this matters enormously. As <a href="https://www.debugbear.com/blog/soft-navigations">DebugBear's breakdown of the feature</a> puts it, every metric effectively resets at each soft navigation: LCP and CLS start fresh, INP measures delay from that point forward, and Time to First Byte reports as zero. Tools opt into this with <code>reportSoftNavs: true</code> inside Google's <code>web-vitals</code> library, version six and above, rather than aggregating an entire session into one misleading number.</p>

<p>Google's performance team is careful to say neither architecture is inherently superior. <a href="https://web.dev/articles/vitals-spa-faq">Web.dev's own FAQ on SPA architecture</a> states that single page apps and traditional multi page sites "are both capable of delivering high quality experiences to users," and that switching frameworks purely to chase a score is the wrong motivation.</p>

<div class="bx-section-head">
  <span class="bx-num">05</span>
  <h2 class="bx-h2" id="fix-one-and-two-code-splitting-and-route-based-lazy-loading">Fix one and two: code splitting and route based lazy loading</h2>
  <div class="bx-rule"></div>
</div>

<p>The single highest leverage fix for both INP and LCP is also the simplest: stop shipping the entire app in one JavaScript file. <a href="https://web.dev/articles/reduce-javascript-payloads-with-code-splitting">Web.dev's guidance on reducing JavaScript payloads</a> recommends splitting a bundle along route boundaries, so a visitor landing on the homepage only downloads code the homepage actually needs, not the checkout flow or every modal in the product.</p>

<p>In React this usually means pairing <code>React.lazy</code> with <code>Suspense</code> around each route component. Angular ships route level code splitting as a framework default, and Vue Router supports the same pattern with dynamic imports. A smaller initial bundle means a faster first LCP, and smaller per route chunks mean less code competing for the main thread when INP is measured.</p>

<div class="bx-tip">
  <p class="bx-tip-label">Tip</p>
  <p>Run your production bundle through your framework's bundle analyzer first. Teams are often surprised to find one unused charting library accounting for a third of the JavaScript shipped on every route.</p>
</div>

<div class="bx-section-head">
  <span class="bx-num">06</span>
  <h2 class="bx-h2" id="fix-three-and-four-hybrid-rendering-and-lighter-route-transitions">Fix three and four: hybrid rendering and lighter route transitions</h2>
  <div class="bx-rule"></div>
</div>

<p>The second major fix tackles LCP directly by removing the wait for JavaScript on first load. <a href="https://nextjs.org/learn/seo/rendering-strategies">Next.js documentation on rendering strategies</a> lays out the tradeoffs: static generation builds HTML at build time, server rendering builds it fresh per request, and both ship real content in the first response instead of an empty shell. A hybrid setup, where marketing pages use static rendering while a logged in dashboard stays client rendered, gets speed benefits where they matter most.</p>

<p><a href="https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics">Google's documentation on JavaScript heavy sites</a> backs this up from the crawling side too: Googlebot queues a page, runs it through a headless browser, and only then discovers links added by client rendered content, a two wave indexing cycle that can lag the initial crawl noticeably. Server or static rendering sidesteps that delay.</p>

<p>The fourth fix lives inside the route transition itself: reduce how much synchronous work a single click triggers. Defer analytics and non critical widgets until after the next paint, break large render functions into smaller chunks the browser can interrupt, and use CSS transitions instead of JavaScript animation. Every millisecond trimmed there is a millisecond INP improves.</p>

<div class="bx-ad">
  <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-3931314195561246" data-ad-slot="4249015278" data-ad-format="auto" data-full-width-responsive="true"></ins>
  <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
</div>

<div class="bx-section-head">
  <span class="bx-num">07</span>
  <h2 class="bx-h2" id="fix-five-measure-it-properly-then-avoid-these-common-mistakes">Fix five: measure it properly, then avoid these common mistakes</h2>
  <div class="bx-rule"></div>
</div>

<p>None of the previous four fixes mean much if the measurement itself is broken, which brings us to the fifth and final fix: instrument your app with a library that actually understands soft navigations. Using a current release of Google's <code>web-vitals</code> library with soft navigation reporting on, pointed at <a href="/how-to-measure-core-web-vitals-tools-guide/">a proper measurement setup</a>, is the only reliable way to see how individual routes perform rather than one blended session average.</p>

<p><a href="https://www.smashingmagazine.com/2024/04/monitor-optimize-google-core-web-vitals/">Smashing Magazine's field guide to monitoring Core Web Vitals</a> is a useful reminder of the thresholds above: LCP under 2.5 seconds, INP under 200 milliseconds, and CLS under 0.1. Chasing Core Web Vitals for single page applications without those numbers in front of you is just guessing.</p>

<div class="bx-checklist">
  <li><b>Measuring only the homepage.</b> Instrument every meaningful route, not just the landing page, since that is where soft navigation problems actually live.</li>
  <li><b>Shipping one giant bundle.</b> Split code by route so a visitor never downloads screens they have not opened yet.</li>
  <li><b>Blocking the main thread on every click.</b> Defer non essential work until after the next paint instead of running it synchronously inside the click handler.</li>
  <li><b>Ignoring soft navigations in RUM tools.</b> Turn on soft navigation reporting so route level data does not get averaged into one misleading session score.</li>
  <li><b>Assuming a rewrite is the only option.</b> A hybrid rendering setup, not a full framework migration, usually solves most of the pain.</li>
</div>

<div class="bx-ad">
  <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-3931314195561246" data-ad-slot="4249015278" data-ad-format="auto" data-full-width-responsive="true"></ins>
  <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
</div>

<div class="bx-faq">
  <div class="bx-faq-item open">
    <button class="bx-faq-q"><span class="bx-faq-num">1</span>What is Core Web Vitals for single page applications, exactly?</button>
    <div class="bx-faq-a"><p>It refers to the specific challenges of measuring and improving LCP, INP, and CLS inside apps built with React, Vue, or Angular, where one JavaScript bundle handles most page changes instead of the browser loading a fresh document each time.</p></div>
  </div>
  <div class="bx-faq-item open">
    <button class="bx-faq-q"><span class="bx-faq-num">2</span>Why does INP get worse specifically after someone navigates inside the app?</button>
    <div class="bx-faq-a"><p>Each route change can trigger data fetching, component teardown, and a fresh render pass on the main thread in response to a single click, so the browser stays busy longer before it can paint the next frame, which is exactly what INP measures.</p></div>
  </div>
  <div class="bx-faq-item open">
    <button class="bx-faq-q"><span class="bx-faq-num">3</span>Does client rendering always hurt Largest Contentful Paint?</button>
    <div class="bx-faq-a"><p>Not always, but it usually adds a delay, since the preload scanner cannot discover images or text buried inside JavaScript generated markup the way it can with HTML streamed from a server.</p></div>
  </div>
  <div class="bx-faq-item open">
    <button class="bx-faq-q"><span class="bx-faq-num">4</span>What is a soft navigation and why does it matter here?</button>
    <div class="bx-faq-a"><p>A soft navigation is an in app route change, triggered by a user interaction, that updates the URL and visible content without a full page reload. Field data historically ignored these, so Chrome built dedicated APIs so tools can measure each one.</p></div>
  </div>
  <div class="bx-faq-item open">
    <button class="bx-faq-q"><span class="bx-faq-num">5</span>Can server side rendering or static generation fix this on its own?</button>
    <div class="bx-faq-a"><p>It solves most of the first load LCP problem by shipping real content immediately, but it will not fix a heavy route transition by itself, which is why pairing it with code splitting matters for the full picture.</p></div>
  </div>
</div>

<div class="bx-learn">
  <h2 id="learn-today">Learn Today</h2>
  <div class="bx-learn-grid">
    <div class="bx-learn-card"><span class="bx-learn-num">1</span><div><h4>INP</h4><p>Interaction to Next Paint, the Core Web Vitals metric that measures how long a page stays unresponsive after a user interaction.</p></div></div>
    <div class="bx-learn-card"><span class="bx-learn-num">2</span><div><h4>LCP</h4><p>Largest Contentful Paint, the time it takes for the biggest visible element on a screen to actually render.</p></div></div>
    <div class="bx-learn-card"><span class="bx-learn-num">3</span><div><h4>Soft Navigation</h4><p>A route change inside a single page app that updates the URL and content without a full browser page reload.</p></div></div>
    <div class="bx-learn-card"><span class="bx-learn-num">4</span><div><h4>Code Splitting</h4><p>Breaking one large JavaScript bundle into smaller pieces that load only when a specific route or feature is needed.</p></div></div>
    <div class="bx-learn-card"><span class="bx-learn-num">5</span><div><h4>Hydration</h4><p>The process where a framework attaches event handlers and interactivity to HTML that already exists on the page.</p></div></div>
    <div class="bx-learn-card"><span class="bx-learn-num">6</span><div><h4>Hybrid Rendering</h4><p>Using server rendering or static generation for some pages and client rendering for others within the same app.</p></div></div>
  </div>
</div>

<div class="bx-cta">
  <h3>Get Core Web Vitals for single page applications right</h3>
  <p>Explore more Brandella Journal guides on SEO and digital marketing.</p>
  <div class="bx-cta-btns">
    <a href="/">Browse All Guides</a>
    <a class="bx-cta-outline" href="/how-to-measure-core-web-vitals-tools-guide/">See the Measurement Guide</a>
  </div>
</div>

</div>

<script>
document.querySelectorAll('.bx-faq-item').forEach(function(item){
  var q = item.querySelector('.bx-faq-q');
  var a = item.querySelector('.bx-faq-a');
  a.style.maxHeight = a.scrollHeight + 'px';
  q.addEventListener('click', function(){
    var isOpen = item.classList.contains('open');
    if (isOpen) {
      item.classList.remove('open');
      a.style.maxHeight = '0px';
    } else {
      item.classList.add('open');
      a.style.maxHeight = a.scrollHeight + 'px';
    }
  });
});
</script>
