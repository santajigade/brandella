---
title: "Robots.txt Explained: Complete Guide with Examples"
slug: "robots-txt-complete-guide"
date: "2026-08-04T03:29:42"
updated: "2026-08-09T08:39:40"
author: "santajigade"
categories: ["seo", "technical-seo"]
primaryCategory: "seo"
description: "One misplaced line in robots.txt can hide your entire site. Learn the 4 core directives, AI crawler rules, wildcards, and a rule tester tool for 2026."
focusKeyword: "robots.txt"
image: "/wp-content/uploads/2026/08/robots.txt.webp"
imageAlt: "robots.txt"
words: 1248
views: 109
format: "html"
---
<div class="brt-wrap">
<style>
.brt-wrap{font-family:'Segoe UI', Arial, sans-serif;font-size:17px;line-height:1.75;color:#2e2e2e;max-width:100%;}
.brt-wrap h2{font-size:25px;color:#2b2b2b;margin:36px 0 16px;font-weight:800;border-left:5px solid #5DB92E;padding-left:14px;}
.brt-wrap h3{font-size:19px;color:#2b2b2b;margin:18px 0 10px;font-weight:700;}
.brt-wrap p{margin:0 0 14px;font-size:17px;}
.brt-wrap a{color:#3f9421;font-weight:600;text-decoration:none;}
.brt-wrap a:hover{color:#2f7418;text-decoration:none;}
.brt-wrap ul,.brt-wrap ol{margin:0 0 16px;padding-left:22px;}
.brt-wrap li{margin-bottom:8px;font-size:17px;}

.brt-lede{font-size:20px;color:#333;font-style:italic;margin:0 0 18px;line-height:1.6;border-left:3px solid #5DB92E;padding-left:16px;}

.brt-meta-row{display:flex;flex-wrap:wrap;gap:10px;margin:0 0 24px;}
.brt-meta-pill{background:#eef8e8;color:#3f9421;border:1px solid #cdeabb;border-radius:20px;padding:6px 16px;font-size:13px;font-weight:700;text-transform:uppercase;letter-spacing:.5px;}

/* Stat cards */
.brt-stat-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin:20px 0 30px;}
.brt-stat-card{background:#f7faf5;border:1px solid #e3ede0;border-radius:12px;padding:22px 16px;text-align:center;}
.brt-stat-num{font-size:32px;font-weight:800;color:#5DB92E;margin-bottom:6px;}
.brt-stat-card p{margin:0;font-size:17px;color:#4a4a4a;}
@media(max-width:820px){.brt-stat-grid{grid-template-columns:1fr;}}

/* Warning callout */
.brt-warning{margin:20px 0 30px;background:#fdecec;border-left:5px solid #c95d5d;border-radius:0 10px 10px 0;padding:18px 20px;}
.brt-warning strong{color:#a33;display:block;margin-bottom:4px;}
.brt-warning p{margin:0;color:#7a3a3a;}

/* Code block */
.brt-code-box{background:#1e1e1e;border-radius:12px;padding:20px 22px;margin:20px 0 10px;overflow-x:auto;}
.brt-code-box pre{margin:0;font-family:'Consolas','Monaco',monospace;font-size:13px;line-height:1.65;color:#d4d4d4;white-space:pre;}
.brt-code-box .k{color:#9cdcfe;}
.brt-code-box .v{color:#ce9178;}
.brt-code-box .c{color:#6a9955;}
.brt-code-caption{font-size:14px;color:#7a7a7a;margin:8px 0 26px;text-align:center;}

/* Tabs */
.brt-tabs{margin:20px 0 30px;}
.brt-tab-buttons{display:flex;flex-wrap:wrap;gap:8px;border-bottom:2px solid #e3ede0;}
.brt-tab-btn{background:#f2f5f0;border:none;border-radius:8px 8px 0 0;padding:12px 20px;font-size:16px;font-weight:700;color:#4a4a4a;cursor:pointer;font-family:'Segoe UI',Arial,sans-serif;}
.brt-tab-btn.active{background:#5DB92E;color:#fff;}
.brt-tab-panel{display:none;border:1px solid #e3ede0;border-top:none;border-radius:0 0 10px 10px;padding:20px;background:#fff;}
.brt-tab-panel.active{display:block;}
.brt-tab-panel p{margin:0 0 10px;}
.brt-tab-panel p:last-child{margin-bottom:0;}

/* Table */
.brt-table-wrap{overflow-x:auto;margin:20px 0 30px;}
.brt-table{width:100%;border-collapse:collapse;font-size:16px;}
.brt-table th{background:#2b2b2b;color:#fff;padding:12px 14px;text-align:left;font-weight:700;}
.brt-table td{padding:12px 14px;border-bottom:1px solid #e3ede0;}
.brt-table tr:nth-child(even) td{background:#f7faf5;}
.brt-table code{font-family:'Consolas','Monaco',monospace;font-size:13px;background:#f2f5f0;padding:2px 6px;border-radius:4px;}

/* Interactive tool */
.brt-calc{border-radius:16px;overflow:hidden;border:1px solid #e3ede0;margin:20px 0 32px;}
.brt-calc-header{background:#2b2b2b;color:#fff;padding:18px 22px;}
.brt-calc-header h3{margin:0 0 4px;font-size:19px;color:#fff;}
.brt-calc-header p{margin:0;font-size:14px;color:#c7d9c0;}
.brt-calc-body{padding:22px;background:#fff;}
.brt-calc-row{margin-bottom:14px;}
.brt-calc-row label{font-size:15px;font-weight:700;color:#2b2b2b;display:block;margin-bottom:6px;}
.brt-calc-row input{width:100%;padding:10px;border-radius:8px;border:1px solid #e3ede0;font-size:15px;color:#3a3a3a;font-family:'Consolas','Monaco',monospace;background:#f7faf5;box-sizing:border-box;}
.brt-calc-btn{background:#5DB92E;color:#fff;border:none;padding:10px 20px;border-radius:8px;font-weight:700;font-size:15px;cursor:pointer;font-family:'Segoe UI',Arial,sans-serif;margin-top:4px;}
.brt-calc-output{margin-top:16px;border-radius:10px;padding:16px 18px;font-size:15px;font-weight:700;text-align:center;}
.brt-calc-output.match{background:#fdecec;color:#a33;}
.brt-calc-output.nomatch{background:#eef8e8;color:#2b6b1f;}
.brt-calc-output.neutral{background:#f7faf5;color:#2b2b2b;}

/* FAQ */
.brt-faq-item{margin-bottom:14px;}
.brt-faq-q{background:#f2f5f0;border-radius:8px 8px 0 0;padding:14px 18px;font-weight:700;color:#2b2b2b;font-size:17px;}
.brt-faq-a{background:#fff;border:1px solid #eef1ec;border-top:none;border-radius:0 0 8px 8px;padding:16px 18px;font-size:17px;color:#4a4a4a;}

/* Related */
.brt-related-box{background:#f7faf5;border:1px solid #e3ede0;border-radius:12px;padding:22px;margin:20px 0 30px;}
.brt-related-box h3{margin:0 0 12px;color:#2b2b2b;}
.brt-related-box ul{margin:0;padding-left:20px;}
.brt-related-box li{margin-bottom:10px;}
.brt-related-box a{font-weight:600 !important;}

/* What we learn today - terminal log style */
.brt-learn{margin:26px 0 20px;background:#1e1e1e;border-radius:14px;padding:20px 22px;}
.brt-learn h3{font-size:18px;color:#fff;margin:0 0 14px;font-family:'Consolas','Monaco',monospace;}
.brt-learn-line{display:flex;gap:10px;padding:6px 0;font-family:'Consolas','Monaco',monospace;font-size:14px;}
.brt-learn-line .ok{color:#5DB92E;}
.brt-learn-line p{margin:0;color:#d4d4d4;}
</style>

<div class="brt-meta-row">
<span class="brt-meta-pill">Technical SEO</span>
<span class="brt-meta-pill">Robots.txt</span>
<span class="brt-meta-pill">Crawling</span>
<span class="brt-meta-pill">AI Crawlers</span>
</div>

<p class="brt-lede">A single misplaced line in robots.txt can hide your entire site from Google. It is one of the smallest, oldest files on the web, plain text, four main directives, and it still controls billions of dollars of traffic every single day. This guide covers the full syntax, real AI crawler rules for 2026, and the one mistake that quietly de-indexes sites.</p>

<p>Robots.txt is a plain-text file placed at the root of a website that tells search engine crawlers and AI bots which URLs they are allowed or not allowed to access.</p>

<p>It follows the Robots Exclusion Protocol, formalized as RFC 9309, a standard respected by Google, Bing, and most major AI crawlers.</p>

<!-- OPENING ADSENSE CODE -->
<div style="margin:40px 0;">
    <div style="display:flex;align-items:center;gap:12px;margin-bottom:20px;">
        <div style="flex:1;border-top:2px dotted #bdbdbd;"></div>
        <span style="font-size:12px;color:#777;font-weight:600;letter-spacing:1px;text-transform:uppercase;">
            Advertisement
        </span>
        <div style="flex:1;border-top:2px dotted #bdbdbd;"></div>
    </div>
<ins class="adsbygoogle"
     style="display:block"
     data-ad-client="ca-pub-3931314195561246"
     data-ad-slot="4249015278"
     data-ad-format="auto"
     data-full-width-responsive="true"></ins>
<script>
     (adsbygoogle = window.adsbygoogle || []).push({});
</script>
    <div style="display:flex;align-items:center;gap:12px;margin-top:20px;">
        <div style="flex:1;border-top:2px dotted #bdbdbd;"></div>
        <span style="font-size:12px;color:#777;font-weight:600;letter-spacing:1px;text-transform:uppercase;">
            Advertisement
        </span>
        <div style="flex:1;border-top:2px dotted #bdbdbd;"></div>
    </div>
</div>
<!-- CLOSING ADSENSE CODE -->

<p>We covered the page-level counterpart to this file in our <a href="/meta-robots-tags-explained/" target="_blank" rel="noopener">meta robots tags guide</a>. Robots.txt blocks crawling before a page is ever fetched; meta robots tags control indexing after it already has been.</p>

<div class="brt-stat-grid">
<div class="brt-stat-card"><div class="brt-stat-num">500KB</div><p>is Google's documented size limit for a robots.txt file; content beyond it is ignored</p></div>
<div class="brt-stat-card"><div class="brt-stat-num">4</div><p>core directives cover nearly everything: User-agent, Disallow, Allow, Sitemap</p></div>
<div class="brt-stat-card"><div class="brt-stat-num">2022</div><p>the year the Robots Exclusion Protocol became an official standard, RFC 9309</p></div>
</div>

<h2 id="basic-robots-txt-syntax">Basic Robots.txt Syntax</h2>
<div class="brt-code-box">
<pre><span class="k">User-agent:</span> <span class="v">*</span>
<span class="k">Disallow:</span> <span class="v">/admin/</span>
<span class="k">Disallow:</span> <span class="v">/cart/</span>
<span class="k">Allow:</span> <span class="v">/admin/public/</span>

<span class="k">Sitemap:</span> <span class="v">https://www.example.com/sitemap.xml</span></pre>
</div>
<p class="brt-code-caption">Must live at exactly yoursite.com/robots.txt; a file at /blog/robots.txt is simply ignored</p>

<div class="brt-warning">
<strong>Critical Distinction</strong>
<p>Disallow is not noindex. Blocking a URL in robots.txt only stops crawling. If other sites link to that URL, it can still appear in search results, just without a title or description, since Google never fetched the page to read a noindex tag.</p>
</div>

<h2 id="the-four-core-directives">The Four Core Directives</h2>
<div class="brt-table-wrap">
<table class="brt-table">
<thead>
<tr><th>Directive</th><th>What It Does</th></tr>
</thead>
<tbody>
<tr><td><code>User-agent</code></td><td>Specifies which crawler the following rules apply to</td></tr>
<tr><td><code>Disallow</code></td><td>Blocks crawling of a specific path; empty value means allow everything</td></tr>
<tr><td><code>Allow</code></td><td>Creates an exception inside a broader Disallow rule</td></tr>
<tr><td><code>Sitemap</code></td><td>Points crawlers to your sitemap location; can appear anywhere, applies globally</td></tr>
</tbody>
</table>
</div>

<h2 id="wildcard-patterns-for-precise-matching">Wildcard Patterns for Precise Matching</h2>
<p>According to <a href="https://ixieverse.com/blog/robots-txt-setup-analysis/" target="_blank" rel="noopener">Ixieverse's complete robots.txt setup guide</a>, combining the asterisk and dollar sign builds precise patterns matching specific URL structures rather than entire directories.</p>

<div class="brt-code-box">
<pre><span class="c"># Block every PDF file across the entire site</span>
<span class="k">Disallow:</span> <span class="v">/*.pdf$</span>

<span class="c"># Block any URL containing a query string starting with ?sort=</span>
<span class="k">Disallow:</span> <span class="v">/*?sort=</span>

<span class="c"># Block an entire path and everything beneath it</span>
<span class="k">Disallow:</span> <span class="v">/search</span></pre>
</div>
<p class="brt-code-caption">The dollar sign anchors the match to the end of the URL; without it, the pattern matches anywhere</p>

<h2 id="blocking-or-allowing-ai-crawlers-in-2026">Blocking or Allowing AI Crawlers in 2026</h2>
<p>According to <a href="https://toolsdock.io/blog/robots-txt-complete-guide" target="_blank" rel="noopener">ToolsDock's complete 2026 robots.txt guide</a>, every major AI company now runs its own crawler, some for training data, some for real-time browsing, and some for both.</p>

<div class="brt-code-box">
<pre><span class="c"># Allow Google and Bing as normal</span>
<span class="k">User-agent:</span> <span class="v">Googlebot</span>
<span class="k">Allow:</span> <span class="v">/</span>

<span class="c"># Block OpenAI's training crawler specifically</span>
<span class="k">User-agent:</span> <span class="v">GPTBot</span>
<span class="k">Disallow:</span> <span class="v">/</span>

<span class="c"># Allow Anthropic's on-demand fetch bot, block its training crawler</span>
<span class="k">User-agent:</span> <span class="v">Claude-User</span>
<span class="k">Allow:</span> <span class="v">/</span>
<span class="k">User-agent:</span> <span class="v">ClaudeBot</span>
<span class="k">Disallow:</span> <span class="v">/</span></pre>
</div>
<p class="brt-code-caption">Different bots from the same company often serve different purposes; block selectively, not all at once</p>
<!-- OPENING ADSENSE CODE -->
<div style="margin:40px 0;">
    <div style="display:flex;align-items:center;gap:12px;margin-bottom:20px;">
        <div style="flex:1;border-top:2px dotted #bdbdbd;"></div>
        <span style="font-size:12px;color:#777;font-weight:600;letter-spacing:1px;text-transform:uppercase;">
            Advertisement
        </span>
        <div style="flex:1;border-top:2px dotted #bdbdbd;"></div>
    </div>
<ins class="adsbygoogle"
     style="display:block"
     data-ad-client="ca-pub-3931314195561246"
     data-ad-slot="4249015278"
     data-ad-format="auto"
     data-full-width-responsive="true"></ins>
<script>
     (adsbygoogle = window.adsbygoogle || []).push({});
</script>
    <div style="display:flex;align-items:center;gap:12px;margin-top:20px;">
        <div style="flex:1;border-top:2px dotted #bdbdbd;"></div>
        <span style="font-size:12px;color:#777;font-weight:600;letter-spacing:1px;text-transform:uppercase;">
            Advertisement
        </span>
        <div style="flex:1;border-top:2px dotted #bdbdbd;"></div>
    </div>
</div>
<!-- CLOSING ADSENSE CODE -->
<h2 id="should-you-block-ai-crawlers-entirely">Should You Block AI Crawlers Entirely?</h2>
<p>This depends entirely on your goals. Tap through both perspectives.</p>

<div class="brt-tabs">
<div class="brt-tab-buttons">
<button class="brt-tab-btn active" onclick="brtTab(event,'brt-block')">Reasons to Block</button>
<button class="brt-tab-btn" onclick="brtTab(event,'brt-allow')">Reasons to Allow</button>
</div>
<div id="brt-block" class="brt-tab-panel active">
<p>Concerns about content being used for AI training without compensation, or protecting a paywalled business model, are valid reasons some publishers block AI training crawlers specifically.</p>
</div>
<div id="brt-allow" class="brt-tab-panel">
<p>Blocking search-oriented AI crawlers reduces visibility in ChatGPT, Perplexity, and AI Overviews, channels increasingly driving real referral traffic for many sites.</p>
</div>
</div>

<h2 id="robots-txt-rule-tester">Robots.txt Rule Tester</h2>
<p>Enter a Disallow pattern and a URL path to see if the rule would block it.</p>

<div class="brt-calc">
<div class="brt-calc-header">
<h3>Robots.txt Rule Tester</h3>
<p>Supports basic wildcard (*) and end-anchor ($) matching</p>
</div>
<div class="brt-calc-body">
<div class="brt-calc-row">
<label>Disallow Pattern</label>
<input type="text" id="brtPattern" value="/*.pdf$">
</div>
<div class="brt-calc-row">
<label>Test URL Path</label>
<input type="text" id="brtUrl" value="/downloads/guide.pdf">
</div>
<button class="brt-calc-btn" onclick="brtTest()">Test Rule</button>
<div class="brt-calc-output neutral" id="brtResult">Enter a pattern and URL, then click Test Rule.</div>
</div>
</div>

<script>
function brtTab(evt, id){
  var panels = document.querySelectorAll('.brt-tab-panel');
  var btns = document.querySelectorAll('.brt-tab-btn');
  panels.forEach(function(p){p.classList.remove('active');});
  btns.forEach(function(b){b.classList.remove('active');});
  document.getElementById(id).classList.add('active');
  evt.currentTarget.classList.add('active');
}
function brtTest(){
  var pattern = document.getElementById('brtPattern').value;
  var url = document.getElementById('brtUrl').value;
  var anchored = pattern.endsWith('$');
  var base = anchored ? pattern.slice(0, -1) : pattern;
  var escaped = base.replace(/[.+^${}()|[\]\\]/g, '\\$&').replace(/\*/g, '.*');
  var regex = new RegExp('^' + escaped + (anchored ? '$' : ''));
  var output = document.getElementById('brtResult');
  if(regex.test(url)){
    output.className = 'brt-calc-output match';
    output.innerText = 'BLOCKED: This pattern matches the URL and would prevent crawling.';
  } else {
    output.className = 'brt-calc-output nomatch';
    output.innerText = 'ALLOWED: This pattern does not match; the URL would still be crawled.';
  }
}
</script>

<h2 id="robots-txt-and-crawl-budget">Robots.txt and Crawl Budget</h2>
<p>According to <a href="https://www.conductor.com/academy/robotstxt/" target="_blank" rel="noopener">Conductor's guide to robots.txt essential rules</a>, one incorrect rule can block major sections of a site from search engines and AI bots simultaneously, making careful review essential before any change goes live.</p>

<p>Directives only apply to the exact domain and protocol where the file is hosted, meaning http and https versions of the same site need matching files if both are technically reachable.</p>

<h2 id="how-robots-txt-groups-and-multiple-user-agents-work">How Robots.txt Groups and Multiple User-Agents Work</h2>
<p>According to <a href="https://instarankseo.com/blog/robots-txt-seo-guide" target="_blank" rel="noopener">InstarankSEO's complete 2026 robots.txt guide</a>, a crawler looks for its specific User-agent block first, and falls back to the wildcard block only if no matching specific entry exists.</p>

<p>Multiple user-agents can also share the exact same set of rules, listed as consecutive User-agent lines followed by one shared block of directives, avoiding the need to repeat identical rules for each bot separately.</p>

<h2 id="common-mistakes-that-break-robots-txt">Common Mistakes That Break Robots.txt</h2>
<div class="brt-table-wrap">
<table class="brt-table">
<thead>
<tr><th>Mistake</th><th>What Happens</th></tr>
</thead>
<tbody>
<tr><td><code>Disallow: /</code> left in from staging</td><td>Blocks the entire live site from every crawler</td></tr>
<tr><td>Blocking CSS or JS directories</td><td>Google can't render the page properly to evaluate it</td></tr>
<tr><td>Using robots.txt to hide indexed pages</td><td>Doesn't remove them; use noindex on the page instead</td></tr>
<tr><td>File placed anywhere but the root</td><td>Ignored entirely; must be at yoursite.com/robots.txt exactly</td></tr>
<tr><td>Relying on Crawl-delay for Googlebot</td><td>Google ignores this directive completely</td></tr>
</tbody>
</table>
</div>

<h2 id="testing-your-robots-txt-before-deploying">Testing Your Robots.txt Before Deploying</h2>
<p>According to <a href="https://seranking.com/blog/guide-robots-txt/" target="_blank" rel="noopener">SE Ranking's robots.txt syntax and setup guide</a>, a bot can technically choose not to obey the file at all, though major search engines and reputable AI crawlers do respect it in practice.</p>

<p>According to <a href="https://dominatetools.com/blog/robots-txt-syntax-guide/" target="_blank" rel="noopener">DominateTools' complete 2026 reference guide</a>, testing changes in Google Search Console's report before deploying catches accidental blocks before they affect live crawling.</p>

<p>According to <a href="https://fieldari.com/en/blog/robots-txt-complete-guide-with-examples" target="_blank" rel="noopener">Fieldari's guide to examples, rules, and mistakes</a>, the gap between what this file does and what it doesn't do is exactly where even experienced developers trip up, making a test pass before publishing a genuinely worthwhile habit.</p>

<p>According to <a href="https://validatehtml.com/robots-txt-syntax" target="_blank" rel="noopener">ValidateHTML's complete syntax reference</a>, running the final file through a dedicated syntax checker catches typos and malformed directives a quick manual read-through can easily miss.</p>
<!-- OPENING ADSENSE CODE -->
<div style="margin:40px 0;">
    <div style="display:flex;align-items:center;gap:12px;margin-bottom:20px;">
        <div style="flex:1;border-top:2px dotted #bdbdbd;"></div>
        <span style="font-size:12px;color:#777;font-weight:600;letter-spacing:1px;text-transform:uppercase;">
            Advertisement
        </span>
        <div style="flex:1;border-top:2px dotted #bdbdbd;"></div>
    </div>
<ins class="adsbygoogle"
     style="display:block"
     data-ad-client="ca-pub-3931314195561246"
     data-ad-slot="4249015278"
     data-ad-format="auto"
     data-full-width-responsive="true"></ins>
<script>
     (adsbygoogle = window.adsbygoogle || []).push({});
</script>
    <div style="display:flex;align-items:center;gap:12px;margin-top:20px;">
        <div style="flex:1;border-top:2px dotted #bdbdbd;"></div>
        <span style="font-size:12px;color:#777;font-weight:600;letter-spacing:1px;text-transform:uppercase;">
            Advertisement
        </span>
        <div style="flex:1;border-top:2px dotted #bdbdbd;"></div>
    </div>
</div>
<!-- CLOSING ADSENSE CODE -->
<h2 id="faqs-on-robots-txt">FAQs on Robots.txt</h2>

<div class="brt-faq-item">
<div class="brt-faq-q">Does robots.txt prevent a page from being indexed?</div>
<div class="brt-faq-a">No. It only prevents crawling. A blocked page can still appear in search results without a description if other sites link to it. Use a noindex meta tag to actually prevent indexing.</div>
</div>
<div class="brt-faq-item">
<div class="brt-faq-q">Where must the robots.txt file be located?</div>
<div class="brt-faq-a">At the exact root of the domain, such as https://www.example.com/robots.txt. A file placed in any subfolder is ignored entirely by crawlers.</div>
</div>
<div class="brt-faq-item">
<div class="brt-faq-q">Is robots.txt case-sensitive?</div>
<div class="brt-faq-a">Path values are case-sensitive, so Disallow: /Admin/ differs from Disallow: /admin/. Directive names themselves, like User-agent and Disallow, are case-insensitive.</div>
</div>
<div class="brt-faq-item">
<div class="brt-faq-q">Can I block specific AI crawlers while allowing Google?</div>
<div class="brt-faq-a">Yes. Create a separate User-agent block for each bot you want to treat differently, such as disallowing GPTBot while allowing Googlebot full access.</div>
</div>
<div class="brt-faq-item">
<div class="brt-faq-q">Does Google support the Crawl-delay directive?</div>
<div class="brt-faq-a">No. Googlebot ignores Crawl-delay entirely, though some other crawlers, including Bingbot, do honor it.</div>
</div>
<div class="brt-faq-item">
<div class="brt-faq-q">What's the maximum size for a robots.txt file?</div>
<div class="brt-faq-a">Google's documented limit is 500 kilobytes. Content beyond that limit is ignored, though most legitimate sites stay well under 1 kilobyte in practice.</div>
</div>

<div class="brt-related-box">
<h3>Related Articles</h3>
<ul>
<li><a href="/meta-robots-tags-explained/" target="_blank" rel="noopener">Meta Robots Tags Explained with HTML Code Examples</a></li>
<li><a href="/crawl-budget-explained/" target="_blank" rel="noopener">Crawl Budget Explained: Why Google Might Be Ignoring Half Your Site</a></li>
<li><a href="/build-xml-sitemap-generator-php/" target="_blank" rel="noopener">Build Your Own XML Sitemap Generator in PHP</a></li>
<li><a href="/what-is-xml-sitemap-ai-search-era/" target="_blank" rel="noopener">What Is an XML Sitemap, and Does It Still Matter in the AI Search Era?</a></li>
</ul>
</div>

<div class="brt-learn">
<h3>&gt; what_we_learn_today.log</h3>
<div class="brt-learn-line"><span class="ok">[OK]</span><p>Robots.txt controls crawling; it never guarantees a page stays out of the index</p></div>
<div class="brt-learn-line"><span class="ok">[OK]</span><p>Four directives cover almost everything: User-agent, Disallow, Allow, Sitemap</p></div>
<div class="brt-learn-line"><span class="ok">[OK]</span><p>The file must live at the exact domain root, nowhere else</p></div>
<div class="brt-learn-line"><span class="ok">[OK]</span><p>Wildcard and end-anchor patterns allow precise, targeted rules</p></div>
<div class="brt-learn-line"><span class="ok">[OK]</span><p>Different AI crawlers can be allowed or blocked selectively per bot</p></div>
<div class="brt-learn-line"><span class="ok">[OK]</span><p>Always test changes before deploying; one bad line can block an entire site</p></div>
</div>

</div>
