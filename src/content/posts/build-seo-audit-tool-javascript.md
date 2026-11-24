---
title: "Build an SEO Audit Tool Using JavaScript: Complete Guide"
slug: "build-seo-audit-tool-javascript"
date: "2026-08-23T13:53:49"
updated: "2026-08-24T02:56:27"
author: "santajigade"
categories: ["javascript"]
primaryCategory: "javascript"
description: "Build an SEO audit tool using JavaScript: real, runnable checks for title, meta, headings, alt text, and canonical tags, with scoring and a bookmarklet."
focusKeyword: "SEO Audit Tool"
takeaways:
  - "A JavaScript SEO audit tool runs rule-based DOM checks for title, meta description, heading hierarchy, image alt text and canonical tags, then scores the results."
  - "Titles should stay within 50-60 characters and meta descriptions within 150-160 characters to avoid truncation in search results."
  - "The heading check flags a missing single H1 and skipped levels when opening a section, but not when closing a subsection, which the W3C allows."
  - "Wrapping the audit in a self-executing function lets it run as a bookmarklet on any page with one click."
  - "A DOM-based tool checks one page at a time and cannot see HTTP headers or status codes, unlike full crawlers such as Screaming Frog."
image: "/wp-content/uploads/2026/08/SEO-Audit-Tool.webp"
imageAlt: "SEO Audit Tool"
words: 1681
views: 59
format: "html"
---
<div class="bmc-flow">
<style>
@import url('https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600;700;800&display=swap');
.bmc-flow{--bx-green:#5DB92E;--bx-green-deep:#4a9e24;--bx-gold:#F4B41A;--bx-ink:#2b2b2b;--bx-steel:#5a6570;--bx-steel-2:#8a96a1;--bx-line:#E3EDE0;--bx-red:#c95d5d;--bx-blue:#6fa8dc;--bx-disp:'Open Sans',Arial,sans-serif;--bx-body:'Open Sans',system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif;font-family:var(--bx-body);font-weight:400;font-style:normal;color:var(--bx-ink);line-height:1.75;font-size:17px;max-width:920px;margin:0 auto;padding:0;-webkit-font-smoothing:antialiased;}
.bmc-flow *{box-sizing:border-box;}
.bmc-flow p{margin:0 0 14px;font-size:17px;}
.bmc-flow a{color:var(--bx-green-deep);text-decoration:none;font-weight:600;}
.bmc-flow a:hover{color:var(--bx-green);}
.bmc-flow strong{font-weight:700;}
.bmc-flow h2{font-family:var(--bx-disp);font-weight:700;font-size:26px;line-height:1.2;margin:36px 0 16px;color:var(--bx-ink);}
.bmc-flow h2 .bx-num{color:var(--bx-green);font-weight:800;margin-right:8px;}
.bmc-flow .bx-rule{height:4px;width:56px;background:var(--bx-green);border-radius:2px;margin:0 0 16px;}
.bmc-flow .bx-meta-row{display:flex;flex-wrap:wrap;gap:10px;margin:0 0 24px;}
.bmc-flow .bx-meta-pill{background:#eef8e8;color:#3f9421;border:1px solid #cdeabb;border-radius:20px;padding:6px 16px;font-size:17px;font-weight:700;text-transform:uppercase;letter-spacing:.5px;}
.bmc-flow .bx-lede{font-size:17px;color:#333;font-style:italic;margin:0 0 17px;line-height:1.6;border-left:3px solid var(--bx-green);padding-left:16px;}
.bmc-flow .bx-specs{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin:20px 0 30px;}
.bmc-flow .bx-spec{background:#f7faf5;border:1px solid var(--bx-line);border-radius:12px;padding:22px 16px;text-align:center;}
.bmc-flow .bx-spec .v{font-family:var(--bx-disp);font-weight:800;font-size:32px;color:var(--bx-green-deep);margin-bottom:6px;}
.bmc-flow .bx-spec .k{font-size:17px;color:#4a4a4a;}
@media(max-width:700px){.bmc-flow .bx-specs{grid-template-columns:1fr;}}
.bmc-flow .bx-note{border-left:5px solid var(--bx-red);background:#fdecec;border-radius:0 10px 10px 0;padding:17px 20px;margin:20px 0 30px;}
.bmc-flow .bx-note .lbl{font-family:var(--bx-disp);text-transform:uppercase;letter-spacing:1px;font-size:17px;color:#a33;font-weight:700;display:block;margin-bottom:4px;}
.bmc-flow .bx-note p{margin:0;font-size:17px;color:#7a3a3a;}
.bmc-flow .bx-dyk{border-left:5px solid var(--bx-blue);background:#eef4fb;border-radius:0 10px 10px 0;padding:17px 20px;margin:20px 0 30px;}
.bmc-flow .bx-dyk .lbl{font-family:var(--bx-disp);text-transform:uppercase;letter-spacing:1px;font-size:17px;color:#3a6ea5;font-weight:700;display:flex;align-items:center;gap:8px;margin-bottom:6px;}
.bmc-flow .bx-dyk p{margin:0;font-size:17px;color:#2c4a6b;}
.bmc-flow .bx-tip{position:relative;overflow:hidden;border-radius:14px;margin:20px 0 30px;padding:20px 22px 20px 62px;background:linear-gradient(135deg,#fff8e6 0%,#fff2d1 100%);border:1px solid #f4d98a;}
.bmc-flow .bx-tip::before{content:"💡";position:absolute;left:16px;top:18px;font-size:24px;line-height:1;}
.bmc-flow .bx-tip .lbl{font-family:var(--bx-disp);text-transform:uppercase;letter-spacing:1px;font-size:16px;color:#a5750b;font-weight:800;display:block;margin-bottom:6px;}
.bmc-flow .bx-tip p{margin:0;font-size:17px;color:#6b4f0e;}
.bmc-flow .bx-checklist{display:flex;flex-direction:column;gap:10px;margin:20px 0 30px;}
.bmc-flow .bx-check-item{display:flex;gap:13px;background:#fff;border:1px solid var(--bx-line);border-left:4px solid var(--bx-green);border-radius:10px;padding:14px 17px;align-items:flex-start;}
.bmc-flow .bx-check-icon{width:22px;height:22px;border-radius:6px;background:var(--bx-green);flex-shrink:0;margin-top:2px;position:relative;}
.bmc-flow .bx-check-icon::after{content:"✓";position:absolute;top:-2px;left:5px;color:#fff;font-weight:800;font-size:13px;}
.bmc-flow .bx-check-item p{margin:0;font-size:17px;color:#3a3a3a;}
.bmc-flow .bx-check-item strong{color:var(--bx-ink);}
.bmc-flow .bx-table-wrap{overflow-x:auto;margin:20px 0 30px;}
.bmc-flow .bx-table{width:100%;border-collapse:collapse;font-size:17px;}
.bmc-flow .bx-table th{background:var(--bx-ink);color:#fff;padding:13px 16px;text-align:left;font-family:var(--bx-disp);font-weight:600;font-size:17px;}
.bmc-flow .bx-table td{padding:13px 16px;border-bottom:1px solid var(--bx-line);font-size:17px;}
.bmc-flow .bx-table tr:nth-child(even) td{background:#f7faf5;}
.bmc-flow .bx-code{background:#20272C;border-radius:14px;padding:20px 22px;margin:20px 0 30px;overflow-x:auto;}
.bmc-flow .bx-code pre{margin:0;font-family:'Courier New',monospace;font-size:14px;line-height:1.7;white-space:pre-wrap;word-break:break-word;color:#e6e6e6;}
.bmc-flow .bx-code-label{font-family:var(--bx-disp);color:var(--bx-steel-2);text-transform:uppercase;letter-spacing:1.2px;font-size:13px;margin-bottom:10px;font-weight:600;}
.bmc-flow .tok-com{color:#7a8a7a;font-style:italic;}
.bmc-flow .tok-sel{color:#8fd97f;}
.bmc-flow .tok-prop{color:#6fc6e8;}
.bmc-flow .tok-val{color:#f4b45a;}
.bmc-flow .tok-str{color:#e8c96a;}
.bmc-flow .tok-kw{color:#c992e8;}
.bmc-flow .tok-fn{color:#79b8f2;}
.bmc-flow .tok-num{color:#f4915a;}
.bmc-flow .bx-calc{border-radius:16px;overflow:hidden;border:1px solid var(--bx-line);margin:20px 0 30px;}
.bmc-flow .bx-calc-header{background:#20272C;color:#fff;padding:17px 22px;}
.bmc-flow .bx-calc-header h3{margin:0 0 4px;font-size:17px;color:#fff;font-family:var(--bx-disp);}
.bmc-flow .bx-calc-header p{margin:0;font-size:17px;color:#c7d9c0;}
.bmc-flow .bx-calc-body{padding:22px;background:#fff;}
.bmc-flow .bx-calc-factor{padding:12px 0;border-bottom:1px solid #f0f2f0;}
.bmc-flow .bx-calc-factor:last-of-type{border-bottom:none;}
.bmc-flow .bx-calc-factor-top{display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;}
.bmc-flow .bx-calc-factor-top label{font-size:17px;font-weight:700;color:var(--bx-ink);}
.bmc-flow .bx-calc-factor-top span{font-size:17px;font-weight:800;color:#3f9421;background:#eef8e8;padding:2px 8px;border-radius:10px;}
.bmc-flow .bx-calc-select,.bmc-flow .bx-calc-input{width:100%;padding:8px 10px;border-radius:8px;border:1px solid var(--bx-line);font-size:17px;color:#3a3a3a;font-family:var(--bx-body);background:#f7faf5;}
.bmc-flow .bx-calc-gauge-wrap{margin-top:20px;background:#f7faf5;border-radius:12px;padding:20px;text-align:center;}
.bmc-flow .bx-calc-gauge-track{background:#e8ece7;border-radius:20px;height:28px;overflow:hidden;margin-bottom:12px;}
.bmc-flow .bx-calc-gauge-fill{height:100%;background:linear-gradient(90deg,#c95d5d,#e2a52c,#5DB92E);border-radius:20px;width:0%;transition:width 0.4s ease;display:flex;align-items:center;justify-content:flex-end;padding-right:10px;}
.bmc-flow .bx-calc-gauge-fill span{color:#fff;font-weight:800;font-size:17px;}
.bmc-flow .bx-calc-verdict{font-size:17px;font-weight:700;color:var(--bx-ink);}
.bmc-flow .bx-faq{border:1px solid var(--bx-line);border-radius:12px;overflow:hidden;background:#fff;margin:20px 0 30px;}
.bmc-flow .bx-q{width:100%;text-align:left;background:#fff;border:0;border-top:1px solid var(--bx-line);padding:16px 17px;cursor:pointer;font-family:var(--bx-disp);font-weight:600;font-size:17px;color:var(--bx-ink);display:flex;justify-content:space-between;align-items:center;gap:12px;}
.bmc-flow .bx-faq .bx-q:first-child{border-top:0;}
.bmc-flow .bx-q .ic{color:var(--bx-green);font-weight:800;flex:0 0 auto;transition:transform .2s ease;font-size:20px;}
.bmc-flow .bx-q.on .ic{transform:rotate(45deg);}
.bmc-flow .bx-a{max-height:0;overflow:hidden;transition:max-height .3s ease;padding:0 17px;}
.bmc-flow .bx-a.on{max-height:360px;}
.bmc-flow .bx-a p{padding:2px 0 16px;margin:0;font-size:17px;color:var(--bx-steel);}
.bmc-flow .bx-cta{position:relative;overflow:hidden;border-radius:17px;margin:30px 0 8px;padding:36px 30px;color:#fff;background:radial-gradient(120% 160% at 12% 10%,rgba(244,180,26,.25),transparent 46%),linear-gradient(135deg,#5DB92E 0%,#3f9421 55%,#245214 100%);}
.bmc-flow .bx-cta h2{color:#fff!important;margin:0 0 8px;}
.bmc-flow .bx-cta p{color:rgba(255,255,255,.94)!important;max-width:560px;margin:0 0 20px;font-size:17px;}
.bmc-flow .bx-actions{display:flex;flex-wrap:wrap;gap:12px;}
.bmc-flow .bx-btn{display:inline-flex;align-items:center;gap:8px;font-family:var(--bx-disp);font-size:17px;font-weight:700;padding:12px 20px;border-radius:40px;text-decoration:none;border:0;}
.bmc-flow .bx-btn.primary{background:#fff;color:var(--bx-green-deep)!important;}
.bmc-flow .bx-btn.ghost{background:rgba(255,255,255,.12);color:#fff!important;border:1.5px solid rgba(255,255,255,.55);}
.bmc-flow .bx-related-box{background:#f7faf5;border:1px solid var(--bx-line);border-radius:12px;padding:22px;margin:20px 0 30px;}
.bmc-flow .bx-related-box h3{margin:0 0 12px;color:var(--bx-ink);font-size:17px;}
.bmc-flow .bx-related-box ul{margin:0;padding-left:20px;}
.bmc-flow .bx-related-box li{margin-bottom:10px;font-size:17px;}
.bmc-flow .bx-learn{margin:26px 0 20px;}
.bmc-flow .bx-learn h3{font-size:17px;color:var(--bx-ink);margin:0 0 17px;text-align:center;font-family:var(--bx-disp);}
.bmc-flow .bx-learn-grid{display:grid;grid-template-columns:1fr 1fr;gap:12px;}
.bmc-flow .bx-learn-card{background:#fff;border:2px solid #cdeabb;border-radius:10px;padding:14px 16px;text-align:center;}
.bmc-flow .bx-learn-card p{margin:0;font-size:17px;color:#3a3a3a;font-weight:600;}
@media(max-width:820px){.bmc-flow .bx-learn-grid{grid-template-columns:1fr;}}
.bmc-flow .bx-ad-wrap{margin:40px 0;}
.bmc-flow .bx-ad-divider{display:flex;align-items:center;gap:12px;}
.bmc-flow .bx-ad-divider span{font-size:12px;color:#777;font-weight:600;letter-spacing:1px;text-transform:uppercase;}
.bmc-flow .bx-ad-line{flex:1;border-top:2px dotted #bdbdbd;}
</style>

<div class="bx-meta-row">
<span class="bx-meta-pill">Technical SEO</span>
<span class="bx-meta-pill">SEO Audit Tool</span>
<span class="bx-meta-pill">JavaScript</span>
<span class="bx-meta-pill">2026</span>
</div>

<p class="bx-lede">Building an SEO audit tool using JavaScript means writing rule-based checks against the DOM, title length, meta description, heading hierarchy, missing alt text, canonical presence, then scoring the results. It's genuinely simpler than it sounds. A handful of focused check functions and a scoring pass cover the checks that matter most for a real page.</p>

<h2 id="seo-audit-tool-basics"><span class="bx-num">01</span>Building an SEO Audit Tool Using JavaScript: The Core Approach</h2>
<div class="bx-rule"></div>
<p><a href="https://localseoaudittool.com/" target="_blank" rel="noopener">One reference audit platform</a> bundles well over 100 checks across technical, on-page, and structured-data categories. A useful DIY tool doesn't need all of them. Focus on the checks with the biggest, most reliably measurable impact: title and meta length, heading hierarchy, image alt coverage, and canonical presence.</p>

<p>Each check follows the same shape: query the relevant DOM elements, evaluate them against a known-good threshold, and return a structured result with a pass/fail status and a human-readable message.</p>

<div class="bx-specs">
<div class="bx-spec"><div class="v">50-60</div><div class="k">characters, the recommended title tag length before search engines truncate it</div></div>
<div class="bx-spec"><div class="v">150-160</div><div class="k">characters, the safe range for meta descriptions before SERP truncation</div></div>
<div class="bx-spec"><div class="v">5</div><div class="k">core checks cover most of what a lightweight audit tool actually needs</div></div>
</div>
<h2 id="title-meta-checks"><span class="bx-num">02</span>Checking Title and Meta Description</h2>
<div class="bx-rule"></div>
<p><a href="https://www.siteguru.co/free-seo-tools/onpage-seo-check" target="_blank" rel="noopener">SiteGuru's on-page checker</a> treats these two as foundational: does the page have a title and description, and are they within the length range search engines display without truncating.</p>

<div class="bx-code">
<div class="bx-code-label">Title and Meta Description Checks</div>
<pre><span class="tok-kw">function</span> <span class="tok-fn">checkTitle</span>() {
  <span class="tok-kw">const</span> title = document.<span class="tok-fn">querySelector</span>(<span class="tok-str">'title'</span>)?.textContent?.<span class="tok-fn">trim</span>() || <span class="tok-str">''</span>;
  <span class="tok-kw">const</span> length = title.length;

  <span class="tok-kw">if</span> (!title) {
    <span class="tok-kw">return</span> { check: <span class="tok-str">'Title Tag'</span>, status: <span class="tok-str">'fail'</span>, message: <span class="tok-str">'Missing title tag entirely'</span> };
  }
  <span class="tok-kw">if</span> (length &lt; <span class="tok-num">30</span>) {
    <span class="tok-kw">return</span> { check: <span class="tok-str">'Title Tag'</span>, status: <span class="tok-str">'warn'</span>, message: <span class="tok-str">`Title is only ${length} chars, likely too short`</span> };
  }
  <span class="tok-kw">if</span> (length &gt; <span class="tok-num">60</span>) {
    <span class="tok-kw">return</span> { check: <span class="tok-str">'Title Tag'</span>, status: <span class="tok-str">'warn'</span>, message: <span class="tok-str">`Title is ${length} chars, may get truncated`</span> };
  }
  <span class="tok-kw">return</span> { check: <span class="tok-str">'Title Tag'</span>, status: <span class="tok-str">'pass'</span>, message: <span class="tok-str">`Title length OK (${length} chars)`</span> };
}

<span class="tok-kw">function</span> <span class="tok-fn">checkMetaDescription</span>() {
  <span class="tok-kw">const</span> meta = document.<span class="tok-fn">querySelector</span>(<span class="tok-str">'meta[name="description"]'</span>);
  <span class="tok-kw">const</span> content = meta?.<span class="tok-fn">getAttribute</span>(<span class="tok-str">'content'</span>)?.<span class="tok-fn">trim</span>() || <span class="tok-str">''</span>;
  <span class="tok-kw">const</span> length = content.length;

  <span class="tok-kw">if</span> (!content) {
    <span class="tok-kw">return</span> { check: <span class="tok-str">'Meta Description'</span>, status: <span class="tok-str">'fail'</span>, message: <span class="tok-str">'Missing meta description'</span> };
  }
  <span class="tok-kw">if</span> (length &lt; <span class="tok-num">70</span> || length &gt; <span class="tok-num">160</span>) {
    <span class="tok-kw">return</span> { check: <span class="tok-str">'Meta Description'</span>, status: <span class="tok-str">'warn'</span>, message: <span class="tok-str">`Description is ${length} chars, outside 70-160 range`</span> };
  }
  <span class="tok-kw">return</span> { check: <span class="tok-str">'Meta Description'</span>, status: <span class="tok-str">'pass'</span>, message: <span class="tok-str">`Description length OK (${length} chars)`</span> };
}</pre>
</div>
<h2 id="heading-check"><span class="bx-num">03</span>Checking Heading Hierarchy</h2>
<div class="bx-rule"></div>
<p>This connects directly to the rules covered in our <a href="/html-heading-structure-best-practices/" target="_blank" rel="noopener">heading structure best practices guide</a>: one H1, and no skipped levels when opening a new section.</p>

<div class="bx-code">
<div class="bx-code-label">Heading Hierarchy Check</div>
<pre><span class="tok-kw">function</span> <span class="tok-fn">checkHeadings</span>() {
  <span class="tok-kw">const</span> h1s = document.<span class="tok-fn">querySelectorAll</span>(<span class="tok-str">'h1'</span>);
  <span class="tok-kw">const</span> issues = [];

  <span class="tok-kw">if</span> (h1s.length === <span class="tok-num">0</span>) {
    issues.<span class="tok-fn">push</span>(<span class="tok-str">'No H1 found on page'</span>);
  } <span class="tok-kw">else</span> <span class="tok-kw">if</span> (h1s.length &gt; <span class="tok-num">1</span>) {
    issues.<span class="tok-fn">push</span>(<span class="tok-str">`Multiple H1 tags found (${h1s.length})`</span>);
  }

  <span class="tok-com">// Check for skipped levels when opening a new section</span>
  <span class="tok-kw">const</span> allHeadings = [...document.<span class="tok-fn">querySelectorAll</span>(<span class="tok-str">'h1, h2, h3, h4, h5, h6'</span>)];
  <span class="tok-kw">let</span> lastLevel = <span class="tok-num">0</span>;

  allHeadings.<span class="tok-fn">forEach</span>(heading => {
    <span class="tok-kw">const</span> level = <span class="tok-fn">parseInt</span>(heading.tagName[<span class="tok-num">1</span>]);
    <span class="tok-kw">if</span> (lastLevel &gt; <span class="tok-num">0</span> && level &gt; lastLevel + <span class="tok-num">1</span>) {
      issues.<span class="tok-fn">push</span>(<span class="tok-str">`Skipped from H${lastLevel} to H${level}: "${heading.textContent.trim().slice(0, 40)}"`</span>);
    }
    lastLevel = level;
  });

  <span class="tok-kw">return</span> {
    check: <span class="tok-str">'Heading Structure'</span>,
    status: issues.length === <span class="tok-num">0</span> ? <span class="tok-str">'pass'</span> : <span class="tok-str">'fail'</span>,
    message: issues.length === <span class="tok-num">0</span> ? <span class="tok-str">'Heading hierarchy looks clean'</span> : issues.<span class="tok-fn">join</span>(<span class="tok-str">'; '</span>)
  };
}</pre>
</div>

<div class="bx-tip">
<span class="lbl">Quick Tip</span>
<p>Watch out for skipped levels when closing a subsection, that's actually valid per the W3C. An H4 closing a deep subsection can validly be followed by an H2 opening a new one. The check above only flags a jump when opening, tightening this rule further would produce false positives on perfectly correct pages.</p>
</div>

<h2 id="images-canonical-check"><span class="bx-num">04</span>Checking Images and Canonical Tag</h2>
<div class="bx-rule"></div>
<p><a href="https://wellows.com/blog/audit-checklist/" target="_blank" rel="noopener">Wellows' 2026 audit checklist</a> flags missing alt text as one of the most common, easily fixable issues on real sites. The canonical check confirms exactly one canonical tag exists, echoing the failure mode covered in our <a href="/canonical-tag-implementation-guide/" target="_blank" rel="noopener">canonical tag implementation guide</a>.</p>

<div class="bx-code">
<div class="bx-code-label">Image Alt Text and Canonical Tag Checks</div>
<pre><span class="tok-kw">function</span> <span class="tok-fn">checkImageAltText</span>() {
  <span class="tok-kw">const</span> images = [...document.<span class="tok-fn">querySelectorAll</span>(<span class="tok-str">'img'</span>)];
  <span class="tok-kw">const</span> missingAlt = images.<span class="tok-fn">filter</span>(img => !img.<span class="tok-fn">getAttribute</span>(<span class="tok-str">'alt'</span>));

  <span class="tok-kw">return</span> {
    check: <span class="tok-str">'Image Alt Text'</span>,
    status: missingAlt.length === <span class="tok-num">0</span> ? <span class="tok-str">'pass'</span> : <span class="tok-str">'warn'</span>,
    message: missingAlt.length === <span class="tok-num">0</span>
      ? <span class="tok-str">`All ${images.length} images have alt text`</span>
      : <span class="tok-str">`${missingAlt.length} of ${images.length} images missing alt text`</span>
  };
}

<span class="tok-kw">function</span> <span class="tok-fn">checkCanonical</span>() {
  <span class="tok-kw">const</span> canonicals = document.<span class="tok-fn">querySelectorAll</span>(<span class="tok-str">'link[rel="canonical"]'</span>);

  <span class="tok-kw">if</span> (canonicals.length === <span class="tok-num">0</span>) {
    <span class="tok-kw">return</span> { check: <span class="tok-str">'Canonical Tag'</span>, status: <span class="tok-str">'fail'</span>, message: <span class="tok-str">'No canonical tag found'</span> };
  }
  <span class="tok-kw">if</span> (canonicals.length &gt; <span class="tok-num">1</span>) {
    <span class="tok-kw">return</span> { check: <span class="tok-str">'Canonical Tag'</span>, status: <span class="tok-str">'fail'</span>, message: <span class="tok-str">`${canonicals.length} canonical tags found, should be exactly 1`</span> };
  }
  <span class="tok-kw">return</span> { check: <span class="tok-str">'Canonical Tag'</span>, status: <span class="tok-str">'pass'</span>, message: <span class="tok-str">'Single canonical tag present'</span> };
}</pre>
</div>
<h2 id="running-scoring"><span class="bx-num">05</span>Running All Checks and Scoring the Result</h2>
<div class="bx-rule"></div>
<p>Combine every check into one runner function that returns a structured report with a numeric score, weighting a failed check more heavily than a warning.</p>

<div class="bx-code">
<div class="bx-code-label">Full Audit Runner With Scoring</div>
<pre><span class="tok-kw">function</span> <span class="tok-fn">runSeoAudit</span>() {
  <span class="tok-kw">const</span> results = [
    <span class="tok-fn">checkTitle</span>(),
    <span class="tok-fn">checkMetaDescription</span>(),
    <span class="tok-fn">checkHeadings</span>(),
    <span class="tok-fn">checkImageAltText</span>(),
    <span class="tok-fn">checkCanonical</span>()
  ];

  <span class="tok-kw">let</span> score = <span class="tok-num">100</span>;
  results.<span class="tok-fn">forEach</span>(result => {
    <span class="tok-kw">if</span> (result.status === <span class="tok-str">'fail'</span>) score -= <span class="tok-num">20</span>;
    <span class="tok-kw">if</span> (result.status === <span class="tok-str">'warn'</span>) score -= <span class="tok-num">10</span>;
  });

  <span class="tok-kw">return</span> {
    score: Math.<span class="tok-fn">max</span>(<span class="tok-num">0</span>, score),
    results: results
  };
}

<span class="tok-com">// Run it and log a readable report</span>
<span class="tok-kw">const</span> audit = <span class="tok-fn">runSeoAudit</span>();
console.<span class="tok-fn">log</span>(<span class="tok-str">`SEO Score: ${audit.score}/100`</span>);
console.<span class="tok-fn">table</span>(audit.results);</pre>
</div>

<h2 id="bookmarklet"><span class="bx-num">06</span>Turning It Into a Bookmarklet</h2>
<div class="bx-rule"></div>
<p>Wrapping the audit in a self-executing function and minifying it into a bookmarklet lets you run it on any page with one click, without opening DevTools manually.</p>

<div class="bx-code">
<div class="bx-code-label">Bookmarklet Wrapper (Paste as a Bookmark URL)</div>
<pre>javascript:(<span class="tok-kw">function</span>(){
  <span class="tok-com">// ...paste the checkTitle, checkMetaDescription, checkHeadings,</span>
  <span class="tok-com">// checkImageAltText, checkCanonical, and runSeoAudit functions here...</span>
  <span class="tok-kw">const</span> audit = <span class="tok-fn">runSeoAudit</span>();
  <span class="tok-kw">let</span> report = <span class="tok-str">`SEO Score: ${audit.score}/100\n\n`</span>;
  audit.results.<span class="tok-fn">forEach</span>(r => {
    report += <span class="tok-str">`${r.status.toUpperCase()}: ${r.check} — ${r.message}\n`</span>;
  });
  alert(report);
})();</pre>
</div>

<h2 id="table"><span class="bx-num">07</span>Client-Side Checks vs Full Crawlers</h2>
<div class="bx-rule"></div>
<p>A DIY DOM-based tool has real limits worth understanding before relying on it.</p>

<div class="bx-table-wrap">
<table class="bx-table">
<thead>
<tr><th>Factor</th><th>DOM-Based JS Tool (this guide)</th><th>Full Crawler (Screaming Frog, Ahrefs)</th></tr>
</thead>
<tbody>
<tr><td>Scope</td><td>One page at a time, current DOM only</td><td>Entire site, hundreds of thousands of URLs</td></tr>
<tr><td>Setup cost</td><td>None, runs in any browser console</td><td>Software install or paid subscription</td></tr>
<tr><td>Server-side signals</td><td>Can't see HTTP headers, status codes</td><td>Full access to headers, redirects, response codes</td></tr>
<tr><td>Best use case</td><td>Quick spot-checks, learning, CI integration</td><td>Comprehensive audits, migrations, ongoing monitoring</td></tr>
</tbody>
</table>
</div>

<h2 id="checklist"><span class="bx-num">08</span>Extending the Tool</h2>
<div class="bx-rule"></div>
<p>A short list of natural next checks to add once the basics are working.</p>

<div class="bx-checklist">
<div class="bx-check-item"><div class="bx-check-icon"></div><p><strong>Add an Open Graph tag check</strong>, confirming og:title, og:description, and og:image are all present.</p></div>
<div class="bx-check-item"><div class="bx-check-icon"></div><p><strong>Check for structured data</strong>, scanning for at least one script[type="application/ld+json"] block.</p></div>
<div class="bx-check-item"><div class="bx-check-icon"></div><p><strong>Verify hreflang consistency</strong>, on multilingual pages, for return tags on every language variant.</p></div>
<div class="bx-check-item"><div class="bx-check-icon"></div><p><strong>Wrap it as a Node.js script</strong> using a headless browser like Puppeteer for JavaScript-rendered pages and batch URLs.</p></div>
<div class="bx-check-item"><div class="bx-check-icon"></div><p><strong>Export results as JSON</strong>, making the tool usable in a CI pipeline as an automated regression check.</p></div>
</div>

<h2 id="score"><span class="bx-num">09</span>Try It: Sample Audit Score Preview</h2>
<div class="bx-rule"></div>
<p>Select realistic values to see how the scoring logic above would grade a page.</p>

<div class="bx-calc">
<div class="bx-calc-header"><h3>Sample Audit Score Preview</h3><p>Select the option that matches your page</p></div>
<div class="bx-calc-body">
<div class="bx-calc-factor"><div class="bx-calc-factor-top"><label>Title tag</label></div>
<select class="bx-calc-select" id="bxTitle" onchange="bxAuditCalc()">
<option value="0">Missing entirely</option>
<option value="10">Present but wrong length</option>
<option value="20" selected>Present, 50-60 characters</option>
</select></div>
<div class="bx-calc-factor"><div class="bx-calc-factor-top"><label>Meta description</label></div>
<select class="bx-calc-select" id="bxMeta" onchange="bxAuditCalc()">
<option value="0">Missing entirely</option>
<option value="10">Present but wrong length</option>
<option value="20" selected>Present, 70-160 characters</option>
</select></div>
<div class="bx-calc-factor"><div class="bx-calc-factor-top"><label>Heading structure</label></div>
<select class="bx-calc-select" id="bxHeading" onchange="bxAuditCalc()">
<option value="0">Multiple H1s or skipped levels</option>
<option value="20" selected>Single H1, clean hierarchy</option>
</select></div>
<div class="bx-calc-factor"><div class="bx-calc-factor-top"><label>Image alt text</label></div>
<select class="bx-calc-select" id="bxAlt" onchange="bxAuditCalc()">
<option value="10">Some images missing alt text</option>
<option value="20" selected>All images have alt text</option>
</select></div>
<div class="bx-calc-factor"><div class="bx-calc-factor-top"><label>Canonical tag</label></div>
<select class="bx-calc-select" id="bxCanonical" onchange="bxAuditCalc()">
<option value="0">Missing or duplicated</option>
<option value="20" selected>Exactly one present</option>
</select></div>
<div class="bx-calc-gauge-wrap"><div class="bx-calc-gauge-track"><div class="bx-calc-gauge-fill" id="bxGaugeFill"><span id="bxGaugeScore">100%</span></div></div>
<div class="bx-calc-verdict" id="bxVerdict">Score reflects the exact logic in runSeoAudit() above.</div></div>
</div>
</div>

<script>
function bxAuditCalc(){
  var score = parseInt(document.getElementById('bxTitle').value)
    + parseInt(document.getElementById('bxMeta').value)
    + parseInt(document.getElementById('bxHeading').value)
    + parseInt(document.getElementById('bxAlt').value)
    + parseInt(document.getElementById('bxCanonical').value);
  document.getElementById('bxGaugeFill').style.width = score + '%';
  document.getElementById('bxGaugeScore').innerText = score + '/100';
  var verdict = document.getElementById('bxVerdict');
  if(score >= 90){verdict.innerText = "Strong. Only minor issues, if any, remain.";}
  else if(score >= 60){verdict.innerText = "Moderate. A few checks need real attention.";}
  else{verdict.innerText = "Weak. Multiple core checks are failing right now.";}
}
bxAuditCalc();
</script>

<h2 id="faq"><span class="bx-num">10</span>Common Questions</h2>
<div class="bx-rule"></div>
<div class="bx-faq" id="bxFaq">
<button class="bx-q">Can a client-side JavaScript audit tool see everything a full crawler sees?<span class="ic">+</span></button>
<div class="bx-a"><p>No. A DOM-based tool only sees the current rendered page, it can't check HTTP status codes, response headers, or crawl an entire site. It's best for quick spot-checks, not comprehensive site audits.</p></div>
<button class="bx-q">Why does the heading check allow some skipped levels but not others?<span class="ic">+</span></button>
<div class="bx-a"><p>Per W3C guidance, skipping is only a problem when opening a new section, like jumping from H2 straight to H4. It's valid when closing a subsection, so a strict "never skip" rule would create false positives.</p></div>
<button class="bx-q">Can I run this audit tool against a live URL, not just the current page?<span class="ic">+</span></button>
<div class="bx-a"><p>Not directly from a browser console due to CORS restrictions. For auditing other URLs, wrap the same check functions in a Node.js script using a headless browser like Puppeteer.</p></div>
<button class="bx-q">What's the fastest way to run these checks without writing code each time?<span class="ic">+</span></button>
<div class="bx-a"><p>Save the combined script as a bookmarklet. Once set up, clicking the bookmark runs the full audit against whatever page you're currently viewing, with no DevTools required.</p></div>
<button class="bx-q">Should I use a DIY tool instead of a commercial SEO audit platform?<span class="ic">+</span></button>
<div class="bx-a"><p>For learning, quick checks, or CI integration, yes. For comprehensive, site-wide audits covering hundreds of pages, HTTP-level signals, and ongoing monitoring, a dedicated crawler tool remains more practical.</p></div>
</div>

<div class="bx-related-box">
<h3>Related Articles</h3>
<ul>
<li><a href="/html-heading-structure-best-practices/" target="_blank" rel="noopener">HTML Heading Structure Best Practices (H1-H6)</a></li>
<li><a href="/canonical-tag-implementation-guide/" target="_blank" rel="noopener">Canonical Tag Implementation Guide</a></li>
<li><a href="/how-to-detect-broken-links-javascript/" target="_blank" rel="noopener">How to Detect Broken Links Using JavaScript</a></li>
</ul>
</div>

<div class="bx-learn">
<h3>What We Learn Today</h3>
<div class="bx-learn-grid">
<div class="bx-learn-card"><p>Five focused checks cover most of what a lightweight audit needs</p></div>
<div class="bx-learn-card"><p>Each check returns a structured pass/warn/fail result</p></div>
<div class="bx-learn-card"><p>Heading checks should only flag skips when opening, not closing</p></div>
<div class="bx-learn-card"><p>A weighted score combines all checks into one number</p></div>
<div class="bx-learn-card"><p>Bookmarklets make the tool usable on any page instantly</p></div>
<div class="bx-learn-card"><p>DOM tools complement, but don't replace, full site crawlers</p></div>
</div>
</div>

<section class="bx-cta">
<h2 id="build-a-complete-technical-seo-toolkit">Build a Complete Technical SEO Toolkit</h2>
<p>This audit tool pairs naturally with the heading structure and canonical guides its checks are based on. Explore both next.</p>
<div class="bx-actions">
<a class="bx-btn primary" href="/html-heading-structure-best-practices/" target="_blank" rel="noopener">HTML Heading Structure Best Practices</a>
<a class="bx-btn ghost" href="/canonical-tag-implementation-guide/" target="_blank" rel="noopener">Canonical Tag Implementation Guide</a>
</div>
</section>

</div>
<script>
(function(){var root=document.currentScript.parentNode.querySelector('.bmc-flow')||document;var qs=root.querySelectorAll('#bxFaq .bx-q');qs.forEach(function(q){q.addEventListener('click',function(){var a=q.nextElementSibling,open=q.classList.contains('on');qs.forEach(function(x){x.classList.remove('on');x.nextElementSibling.classList.remove('on');});if(!open){q.classList.add('on');a.classList.add('on');}});});})();
</script>
