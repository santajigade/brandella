---
title: "How to Lazy Load Images Using Native JavaScript"
slug: "lazy-load-images-native-javascript"
date: "2026-08-02T09:09:24"
updated: "2026-08-09T08:39:47"
author: "santajigade"
categories: ["core-web-vitals", "seo"]
primaryCategory: "seo"
description: "Lazy load images with native JavaScript — the one-attribute method, full IntersectionObserver code, and CSS background image handling, with real examples."
focusKeyword: "lazy load images"
takeaways:
  - "The native loading=\"lazy\" attribute lazy loads images with one HTML attribute and is supported by about 95% of global browser traffic."
  - "The IntersectionObserver API gives full control, such as a 200px rootMargin that loads images just before they scroll into view."
  - "CSS background images ignore the native loading attribute, so they need IntersectionObserver to add a class that applies the background image."
  - "Never lazy load the LCP or hero image, because it delays the largest paint by 200-500ms; use fetchpriority=\"high\" instead."
  - "Always set width and height on lazy loaded images to prevent layout shift, then test with Lighthouse and on a real mobile connection."
image: "/wp-content/uploads/2026/08/lazy-load-images.webp"
imageAlt: "lazy load images"
words: 1423
views: 84
format: "html"
---
<div class="bnl-wrap">
<style>
.bnl-wrap{font-family:'Segoe UI', Arial, sans-serif;font-size:17px;line-height:1.75;color:#2e2e2e;max-width:100%;}
.bnl-wrap h2{font-size:25px;color:#2b2b2b;margin:36px 0 16px;font-weight:800;border-left:5px solid #5DB92E;padding-left:14px;}
.bnl-wrap h3{font-size:19px;color:#2b2b2b;margin:18px 0 10px;font-weight:700;}
.bnl-wrap p{margin:0 0 14px;font-size:17px;}
.bnl-wrap a{color:#3f9421;font-weight:600;text-decoration:none;}
.bnl-wrap a:hover{color:#2f7418;text-decoration:none;}
.bnl-wrap ul,.bnl-wrap ol{margin:0 0 16px;padding-left:22px;}
.bnl-wrap li{margin-bottom:8px;font-size:17px;}

.bnl-lede{font-size:20px;color:#333;font-style:italic;margin:0 0 18px;line-height:1.6;border-left:3px solid #5DB92E;padding-left:16px;}

.bnl-meta-row{display:flex;flex-wrap:wrap;gap:10px;margin:0 0 24px;}
.bnl-meta-pill{background:#eef8e8;color:#3f9421;border:1px solid #cdeabb;border-radius:20px;padding:6px 16px;font-size:13px;font-weight:700;text-transform:uppercase;letter-spacing:.5px;}

/* Stat cards */
.bnl-stat-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin:20px 0 30px;}
.bnl-stat-card{background:#f7faf5;border:1px solid #e3ede0;border-radius:12px;padding:22px 16px;text-align:center;}
.bnl-stat-num{font-size:32px;font-weight:800;color:#5DB92E;margin-bottom:6px;}
.bnl-stat-card p{margin:0;font-size:17px;color:#4a4a4a;}
@media(max-width:820px){.bnl-stat-grid{grid-template-columns:1fr;}}

/* Browser support bar */
.bnl-support{margin:20px 0 30px;background:#fff;border:1px solid #e3ede0;border-radius:14px;padding:22px;}
.bnl-support-track{display:flex;height:32px;border-radius:8px;overflow:hidden;margin-bottom:14px;}
.bnl-support-seg{display:flex;align-items:center;justify-content:center;color:#fff;font-size:12px;font-weight:800;}
.bnl-support-legend{display:flex;flex-wrap:wrap;gap:16px;font-size:13px;color:#4a4a4a;}
.bnl-support-legend span{display:flex;align-items:center;gap:6px;}
.bnl-support-dot{width:10px;height:10px;border-radius:50%;}

/* Warning callout */
.bnl-warning{margin:20px 0 30px;background:#fff8ea;border-left:5px solid #e2a52c;border-radius:0 10px 10px 0;padding:18px 20px;}
.bnl-warning strong{color:#8a6416;display:block;margin-bottom:4px;}
.bnl-warning p{margin:0;color:#5a4a2a;}

/* Code block */
.bnl-code-box{background:#1e1e1e;border-radius:12px;padding:20px 22px;margin:20px 0 10px;overflow-x:auto;}
.bnl-code-box pre{margin:0;font-family:'Consolas','Monaco',monospace;font-size:13px;line-height:1.6;color:#d4d4d4;white-space:pre;}
.bnl-code-box .k{color:#c586c0;}
.bnl-code-box .s{color:#ce9178;}
.bnl-code-box .c{color:#6a9955;}
.bnl-code-box .v{color:#9cdcfe;}
.bnl-code-box .f{color:#dcdcaa;}
.bnl-code-caption{font-size:14px;color:#7a7a7a;margin:8px 0 26px;text-align:center;}

/* Tabs */
.bnl-tabs{margin:20px 0 30px;}
.bnl-tab-buttons{display:flex;flex-wrap:wrap;gap:8px;border-bottom:2px solid #e3ede0;}
.bnl-tab-btn{background:#f2f5f0;border:none;border-radius:8px 8px 0 0;padding:12px 20px;font-size:16px;font-weight:700;color:#4a4a4a;cursor:pointer;font-family:'Segoe UI',Arial,sans-serif;}
.bnl-tab-btn.active{background:#5DB92E;color:#fff;}
.bnl-tab-panel{display:none;border:1px solid #e3ede0;border-top:none;border-radius:0 0 10px 10px;padding:20px;background:#fff;}
.bnl-tab-panel.active{display:block;}
.bnl-tab-panel p{margin:0 0 10px;}
.bnl-tab-panel p:last-child{margin-bottom:0;}

/* Table */
.bnl-table-wrap{overflow-x:auto;margin:20px 0 30px;}
.bnl-table{width:100%;border-collapse:collapse;font-size:16px;}
.bnl-table th{background:#2b2b2b;color:#fff;padding:12px 14px;text-align:left;font-weight:700;}
.bnl-table td{padding:12px 14px;border-bottom:1px solid #e3ede0;}
.bnl-table tr:nth-child(even) td{background:#f7faf5;}
.bnl-table code{font-family:'Consolas','Monaco',monospace;font-size:13px;background:#f2f5f0;padding:2px 6px;border-radius:4px;}

/* Interactive tool */
.bnl-calc{border-radius:16px;overflow:hidden;border:1px solid #e3ede0;margin:20px 0 32px;}
.bnl-calc-header{background:#2b2b2b;color:#fff;padding:18px 22px;}
.bnl-calc-header h3{margin:0 0 4px;font-size:19px;color:#fff;}
.bnl-calc-header p{margin:0;font-size:14px;color:#c7d9c0;}
.bnl-calc-body{padding:22px;background:#fff;}
.bnl-calc-row{margin-bottom:14px;}
.bnl-calc-row label{font-size:15px;font-weight:700;color:#2b2b2b;display:block;margin-bottom:6px;}
.bnl-calc-row select{width:100%;padding:10px;border-radius:8px;border:1px solid #e3ede0;font-size:14px;color:#3a3a3a;font-family:'Segoe UI',Arial,sans-serif;background:#f7faf5;box-sizing:border-box;}
.bnl-calc-output{margin-top:8px;background:#f7faf5;border:1px solid #e3ede0;border-radius:10px;padding:16px 18px;font-size:15px;color:#2b2b2b;font-weight:600;}

/* FAQ */
.bnl-faq-item{margin-bottom:14px;}
.bnl-faq-q{background:#f2f5f0;border-radius:8px 8px 0 0;padding:14px 18px;font-weight:700;color:#2b2b2b;font-size:17px;}
.bnl-faq-a{background:#fff;border:1px solid #eef1ec;border-top:none;border-radius:0 0 8px 8px;padding:16px 18px;font-size:17px;color:#4a4a4a;}

/* Related */
.bnl-related-box{background:#f7faf5;border:1px solid #e3ede0;border-radius:12px;padding:22px;margin:20px 0 30px;}
.bnl-related-box h3{margin:0 0 12px;color:#2b2b2b;}
.bnl-related-box ul{margin:0;padding-left:20px;}
.bnl-related-box li{margin-bottom:10px;}
.bnl-related-box a{font-weight:600 !important;}

/* What we learn today - terminal log style */
.bnl-learn{margin:26px 0 20px;background:#1e1e1e;border-radius:14px;padding:20px 22px;}
.bnl-learn h3{font-size:18px;color:#fff;margin:0 0 14px;font-family:'Consolas','Monaco',monospace;}
.bnl-learn-line{display:flex;gap:10px;padding:6px 0;font-family:'Consolas','Monaco',monospace;font-size:14px;}
.bnl-learn-line .ok{color:#5DB92E;}
.bnl-learn-line p{margin:0;color:#d4d4d4;}
</style>

<div class="bnl-meta-row">
<span class="bnl-meta-pill">Technical SEO</span>
<span class="bnl-meta-pill">Lazy Load Images</span>
<span class="bnl-meta-pill">JavaScript</span>
<span class="bnl-meta-pill">Performance</span>
</div>

<p class="bnl-lede">A product page with 60 photos does not need to download all 60 the moment someone lands on it. Visitors typically see three or four before scrolling. Native JavaScript can lazy load images with a single HTML attribute, or with full custom control through the IntersectionObserver API, and this guide gives you working code for both.</p>

<p>Lazy loading images with native JavaScript means deferring image downloads until they are actually close to entering the viewport, using either the browser's built-in <code>loading="lazy"</code> attribute or the IntersectionObserver API for cases the native attribute cannot handle, like CSS background images.</p>

<p>We covered the strategy and SEO implications in our <a href="/lazy-loading-images-explained-lcp-seo/" target="_blank" rel="noopener">lazy loading images guide</a>. This article is the implementation half: the actual code, working today, in three different approaches.</p>

<div class="bnl-stat-grid">
<div class="bnl-stat-card"><div class="bnl-stat-num">95%</div><p>of global browser traffic supports the native loading="lazy" attribute directly</p></div>
<div class="bnl-stat-card"><div class="bnl-stat-num">1</div><p>HTML attribute is all that's needed for the simplest lazy load images implementation</p></div>
<div class="bnl-stat-card"><div class="bnl-stat-num">0</div><p>times you should ever lazy load your page's LCP or hero image</p></div>
</div>

<h2 id="browser-support-why-native-alone-is-usually-enough">Browser Support: Why Native Alone Is Usually Enough</h2>
<div class="bnl-support">
<div class="bnl-support-track">
<div class="bnl-support-seg" style="width:95%;background:#5DB92E;">95% Native Support</div>
<div class="bnl-support-seg" style="width:1.5%;background:#e2a52c;"></div>
<div class="bnl-support-seg" style="width:3.5%;background:#c95d5d;">3.5%</div>
</div>
<div class="bnl-support-legend">
<span><span class="bnl-support-dot" style="background:#5DB92E;"></span>Supports loading="lazy" natively</span>
<span><span class="bnl-support-dot" style="background:#e2a52c;"></span>IntersectionObserver only, older Safari</span>
<span><span class="bnl-support-dot" style="background:#c95d5d;"></span>Neither supported, legacy browsers</span>
</div>
</div>

<h2 id="method-1-native-lazy-loading-in-one-attribute">Method 1: Native Lazy Loading in One Attribute</h2>
<p>This is the simplest way to lazy load images, requiring no JavaScript at all for the majority of visitors.</p>

<div class="bnl-code-box">
<pre>&lt;img src=<span class="s">"product-photo.jpg"</span>
     width=<span class="s">"600"</span> height=<span class="s">"400"</span>
     loading=<span class="s">"lazy"</span>
     alt=<span class="s">"Blue ceramic coffee mug on wooden table"</span>&gt;</pre>
</div>
<p class="bnl-code-caption">width and height are required to prevent layout shift once the image actually loads</p>

<div class="bnl-warning">
<strong>Critical Warning</strong>
<p>Never add loading="lazy" to your LCP or hero image. Doing so delays the browser's largest paint by 200-500ms and is flagged directly by Lighthouse as a performance anti-pattern.</p>
</div>

<h2 id="method-2-intersectionobserver-for-full-control">Method 2: IntersectionObserver for Full Control</h2>
<p>According to <a href="https://www.debugbear.com/blog/lazy-load-background-images-intersection-observer" target="_blank" rel="noopener">DebugBear's guide to lazy loading with IntersectionObserver</a>, this native browser API detects viewport intersection without the performance cost of manual scroll event listeners.</p>

<div class="bnl-code-box">
<pre><span class="k">const</span> <span class="v">lazyImages</span> = <span class="v">document</span>.<span class="f">querySelectorAll</span>(<span class="s">'img[data-src]'</span>);

<span class="k">const</span> <span class="v">imageObserver</span> = <span class="k">new</span> <span class="f">IntersectionObserver</span>((<span class="v">entries</span>, <span class="v">observer</span>) =&gt; {
  <span class="v">entries</span>.<span class="f">forEach</span>((<span class="v">entry</span>) =&gt; {
    <span class="k">if</span> (<span class="v">entry</span>.<span class="v">isIntersecting</span>) {
      <span class="k">const</span> <span class="v">img</span> = <span class="v">entry</span>.<span class="v">target</span>;
      <span class="v">img</span>.<span class="v">src</span> = <span class="v">img</span>.<span class="v">dataset</span>.<span class="v">src</span>;
      <span class="v">img</span>.<span class="f">removeAttribute</span>(<span class="s">'data-src'</span>);
      <span class="v">observer</span>.<span class="f">unobserve</span>(<span class="v">img</span>);
    }
  });
}, { <span class="v">rootMargin</span>: <span class="s">'200px 0px'</span> });

<span class="v">lazyImages</span>.<span class="f">forEach</span>((<span class="v">img</span>) =&gt; <span class="v">imageObserver</span>.<span class="f">observe</span>(<span class="v">img</span>));</pre>
</div>
<p class="bnl-code-caption">rootMargin loads images 200px before they reach the visible viewport, avoiding a visible pop-in</p>

<div class="bnl-code-box">
<pre>&lt;img data-src=<span class="s">"product-photo.jpg"</span>
     src=<span class="s">"placeholder-tiny.jpg"</span>
     width=<span class="s">"600"</span> height=<span class="s">"400"</span>
     alt=<span class="s">"Blue ceramic coffee mug on wooden table"</span>&gt;</pre>
</div>
<p class="bnl-code-caption">Matching HTML: the real image URL sits in data-src until the observer swaps it in</p>

<h2 id="method-3-lazy-loading-css-background-images">Method 3: Lazy Loading CSS Background Images</h2>
<p>According to <a href="https://www.pagespeedmatters.com/resources/glossary/lazy-loading" target="_blank" rel="noopener">PageSpeed Matters' complete 2026 lazy loading guide</a>, the native loading attribute does not apply to CSS background images at all, since they are not standard img elements.</p>

<div class="bnl-code-box">
<pre><span class="v">document</span>.<span class="f">querySelectorAll</span>(<span class="s">'.lazy-bg'</span>).<span class="f">forEach</span>((<span class="v">el</span>) =&gt; {
  <span class="k">const</span> <span class="v">bgObserver</span> = <span class="k">new</span> <span class="f">IntersectionObserver</span>((<span class="v">entries</span>) =&gt; {
    <span class="v">entries</span>.<span class="f">forEach</span>((<span class="v">entry</span>) =&gt; {
      <span class="k">if</span> (<span class="v">entry</span>.<span class="v">isIntersecting</span>) {
        <span class="v">entry</span>.<span class="v">target</span>.<span class="v">classList</span>.<span class="f">add</span>(<span class="s">'bg-loaded'</span>);
        <span class="v">entry</span>.<span class="f">unobserve</span>?.(<span class="v">entry</span>.<span class="v">target</span>) ?? <span class="v">bgObserver</span>.<span class="f">unobserve</span>(<span class="v">entry</span>.<span class="v">target</span>);
      }
    });
  });
  <span class="v">bgObserver</span>.<span class="f">observe</span>(<span class="v">el</span>);
});</pre>
</div>
<p class="bnl-code-caption">Adds a class that triggers the actual background-image URL, defined separately in CSS</p>

<div class="bnl-code-box">
<pre><span class="c">/* CSS: background-image only applies once .bg-loaded is added */</span>
.lazy-bg.bg-loaded {
  background-image: url(<span class="s">'hero-banner.jpg'</span>);
}</pre>
</div>
<p class="bnl-code-caption">The class-swap pattern for background images referenced above</p>
<h2 id="should-you-use-a-feature-detection-fallback">Should You Use a Feature-Detection Fallback?</h2>
<p>For most sites, no. Tap through both scenarios to see why.</p>

<div class="bnl-tabs">
<div class="bnl-tab-buttons">
<button class="bnl-tab-btn active" onclick="bnlTab(event,'bnl-simple')">Native Alone Is Fine</button>
<button class="bnl-tab-btn" onclick="bnlTab(event,'bnl-fallback')">When a Fallback Helps</button>
</div>
<div id="bnl-simple" class="bnl-tab-panel active">
<p>According to <a href="https://pagespeedchecklist.com/lazy-load-images" target="_blank" rel="noopener">PageSpeed Checklist's guide to native lazy image loading</a>, roughly 95% of traffic already supports loading="lazy" natively, making a JavaScript fallback unnecessary complexity for most general-audience sites.</p>
</div>
<div id="bnl-fallback" class="bnl-tab-panel">
<p>A site with a meaningful share of older Safari traffic can detect support and apply IntersectionObserver only where native support is missing, avoiding unnecessary JavaScript execution everywhere else.</p>
</div>
</div>

<div class="bnl-code-box">
<pre><span class="k">if</span> (<span class="s">'loading'</span> <span class="k">in</span> <span class="f">HTMLImageElement</span>.<span class="v">prototype</span>) {
  <span class="c">// Native lazy loading is supported, do nothing extra</span>
} <span class="k">else</span> <span class="k">if</span> (<span class="s">'IntersectionObserver'</span> <span class="k">in</span> <span class="v">window</span>) {
  <span class="c">// Fall back to the IntersectionObserver pattern from Method 2</span>
}</pre>
</div>
<p class="bnl-code-caption">Feature detection: only runs the JavaScript fallback where native support is actually missing</p>

<h2 id="lazy-load-decision-helper">Lazy Load Decision Helper</h2>
<p>Select the type of image to get the right technique for it.</p>

<div class="bnl-calc">
<div class="bnl-calc-header">
<h3>Lazy Load Decision Helper</h3>
<p>Not every image should be lazy loaded the same way, or at all</p>
</div>
<div class="bnl-calc-body">
<div class="bnl-calc-row">
<label>What type of image is this?</label>
<select id="bnlType" onchange="bnlDecide()">
<option value="hero">Above-the-fold hero / LCP image</option>
<option value="content">Below-the-fold content image</option>
<option value="bg">CSS background image</option>
<option value="iframe">Embedded video or map iframe</option>
</select>
</div>
<div class="bnl-calc-output" id="bnlResult">Do NOT lazy load this. Use fetchpriority="high" instead to speed it up.</div>
</div>
</div>

<script>
function bnlTab(evt, id){
  var panels = document.querySelectorAll('.bnl-tab-panel');
  var btns = document.querySelectorAll('.bnl-tab-btn');
  panels.forEach(function(p){p.classList.remove('active');});
  btns.forEach(function(b){b.classList.remove('active');});
  document.getElementById(id).classList.add('active');
  evt.currentTarget.classList.add('active');
}
function bnlDecide(){
  var type = document.getElementById('bnlType').value;
  var out = document.getElementById('bnlResult');
  if(type === 'hero'){
    out.innerText = 'Do NOT lazy load this. Use fetchpriority="high" instead to speed it up.';
  } else if(type === 'content'){
    out.innerText = 'Use Method 1: native loading="lazy" on the img tag.';
  } else if(type === 'bg'){
    out.innerText = 'Use Method 3: IntersectionObserver with a CSS class-swap pattern.';
  } else if(type === 'iframe'){
    out.innerText = 'Use a facade pattern: show a thumbnail, load the real iframe only on click.';
  }
}
</script>

<h2 id="why-you-d-choose-intersectionobserver-over-native">Why You'd Choose IntersectionObserver Over Native</h2>
<p>According to <a href="https://medium.com/fasal-engineering/image-lazy-loading-using-browsers-intersection-observer-api-a-step-by-step-guide-with-examples-b1a867614e8" target="_blank" rel="noopener">Fasal Engineering's step-by-step guide to IntersectionObserver</a>, the API uses the browser's compositor thread for intersection calculations, avoiding the main-thread cost that manual scroll event listeners used to require before this became possible to lazy load images natively at all.</p>

<p>According to <a href="https://deanhume.com/lazy-loading-images-using-intersection-observer/" target="_blank" rel="noopener">Dean Hume's guide to lazy loading images using Intersection Observer</a>, a graceful fallback for browsers lacking IntersectionObserver support simply loads all images immediately, rather than leaving them permanently hidden.</p>

<h2 id="real-world-impact-of-lazy-loading-images-correctly">Real-World Impact of Lazy Loading Images Correctly</h2>
<p>According to <a href="https://vitalsfixer.com/blog/lazy-loading-guide" target="_blank" rel="noopener">VitalsFixer's complete native lazy loading guide</a>, a typical product page loading 60 images upfront, when only 3 or 4 are ever seen without scrolling, wastes significant bandwidth that lazy loading images correctly eliminates entirely.</p>
<h2 id="preventing-layout-shift-from-lazy-loaded-images">Preventing Layout Shift From Lazy-Loaded Images</h2>
<div class="bnl-table-wrap">
<table class="bnl-table">
<thead>
<tr><th>Rule</th><th>Why It Matters</th></tr>
</thead>
<tbody>
<tr><td>Always set width and height</td><td>Reserves space before the image loads, preventing CLS</td></tr>
<tr><td>Never lazy load the LCP element</td><td>Adds 200-500ms delay to your largest paint metric</td></tr>
<tr><td>Use a low-quality placeholder for Method 2</td><td>Avoids a jarring blank-to-image pop-in effect</td></tr>
<tr><td>Add fetchpriority="high" to hero images</td><td>Tells the browser to fetch it before other resources</td></tr>
<tr><td>Test with Lighthouse after implementation</td><td>Flags any accidental lazy loading of above-fold content</td></tr>
</tbody>
</table>
</div>

<h2 id="testing-your-lazy-loading-setup">Testing Your Lazy Loading Setup</h2>
<p>According to <a href="https://web.dev/articles/browser-level-image-lazy-loading" target="_blank" rel="noopener">web.dev's official guide to browser-level image lazy loading</a>, running Lighthouse after implementation confirms two things at once: that below-fold images are correctly deferred, and that no above-fold or LCP image was accidentally caught by the same loading="lazy" attribute.</p>

<p>According to <a href="https://divotion.com/blog/lazy-load-images-with-the-intersection-obersver-api" target="_blank" rel="noopener">Divotion's guide to lazy loading images with IntersectionObserver</a>, testing on an actual mobile connection, not just desktop Chrome DevTools throttling, catches real-world lazy loading images behavior that a fast local connection can mask entirely.</p>

<h2 id="faqs-on-lazy-loading-images-with-native-javascript">FAQs on Lazy Loading Images With Native JavaScript</h2>

<div class="bnl-faq-item">
<div class="bnl-faq-q">Do I need a library to lazy load images?</div>
<div class="bnl-faq-a">No. The native loading="lazy" attribute and the IntersectionObserver API are both built into modern browsers, requiring no external JavaScript library for either approach.</div>
</div>
<div class="bnl-faq-item">
<div class="bnl-faq-q">When should I use IntersectionObserver instead of the native attribute?</div>
<div class="bnl-faq-a">Use IntersectionObserver for CSS background images, custom loading animations, or when you need more control than the native attribute provides, such as a specific rootMargin buffer distance.</div>
</div>
<div class="bnl-faq-item">
<div class="bnl-faq-q">Should I lazy load my hero image?</div>
<div class="bnl-faq-a">No. Never lazy load an image that is the page's LCP element. Doing so delays the largest paint and is directly flagged by Lighthouse as a performance mistake.</div>
</div>
<div class="bnl-faq-item">
<div class="bnl-faq-q">Do lazy-loaded images still need alt text?</div>
<div class="bnl-faq-a">Yes. Lazy loading is unrelated to image SEO. Every image still needs descriptive, keyword-natural alt text regardless of whether it loads immediately or later.</div>
</div>
<div class="bnl-faq-item">
<div class="bnl-faq-q">Why do my lazy-loaded images cause layout shift?</div>
<div class="bnl-faq-a">This happens when width and height attributes are missing. Without them, the browser cannot reserve space for the image before it loads, causing surrounding content to jump once it appears.</div>
</div>
<div class="bnl-faq-item">
<div class="bnl-faq-q">Can I lazy load iframes the same way as images?</div>
<div class="bnl-faq-a">The native loading="lazy" attribute also works on iframe elements directly. For heavy embeds like YouTube or Google Maps, a facade pattern showing a thumbnail until clicked often saves even more bandwidth.</div>
</div>

<div class="bnl-related-box">
<h3>Related Articles</h3>
<ul>
<li><a href="/lazy-loading-images-explained-lcp-seo/" target="_blank" rel="noopener">Lazy Loading Images Explained: Best Practices That Improve LCP Without Hurting SEO</a></li>
<li><a href="/what-is-largest-contentful-paint-lcp/" target="_blank" rel="noopener">What Is Largest Contentful Paint (LCP)? How to Diagnose and Fix It</a></li>
<li><a href="/cumulative-layout-shift-cls-explained/" target="_blank" rel="noopener">Cumulative Layout Shift (CLS) Explained</a></li>
<li><a href="/how-to-measure-core-web-vitals-tools-guide/" target="_blank" rel="noopener">How to Measure Core Web Vitals: PageSpeed Insights, Lighthouse, CrUX & Search Console</a></li>
</ul>
</div>

<div class="bnl-learn">
<h3>&gt; what_we_learn_today.log</h3>
<div class="bnl-learn-line"><span class="ok">[OK]</span><p>Native loading="lazy" covers roughly 95% of traffic with one HTML attribute</p></div>
<div class="bnl-learn-line"><span class="ok">[OK]</span><p>IntersectionObserver handles CSS backgrounds and custom control needs</p></div>
<div class="bnl-learn-line"><span class="ok">[OK]</span><p>Never lazy load the LCP or hero image; it delays your biggest paint metric</p></div>
<div class="bnl-learn-line"><span class="ok">[OK]</span><p>width and height attributes prevent layout shift once images load</p></div>
<div class="bnl-learn-line"><span class="ok">[OK]</span><p>A feature-detection fallback is optional, useful mainly for older Safari</p></div>
<div class="bnl-learn-line"><span class="ok">[OK]</span><p>Lazy-loaded images still need full, descriptive alt text</p></div>
</div>

</div>
