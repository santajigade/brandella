---
title: "How Google Crawls Websites: From Discovery to Indexing"
slug: "how-google-crawls-websites"
date: "2026-08-04T03:36:01"
updated: "2026-08-09T08:39:39"
author: "santajigade"
categories: ["seo", "technical-seo"]
primaryCategory: "seo"
description: "How Google Crawls Websites? Google indexes only 30-60% of a typical site's pages. Learn the full discovery-to-indexing pipeline, the two-wave rendering process."
focusKeyword: "How Google Crawls Websites"
takeaways:
  - "According to Google's John Mueller, Google indexes only 30 to 60% of a typical website's pages."
  - "Google's pipeline runs through discovery, crawling, rendering and indexing, and new links found during rendering can loop back into discovery."
  - "Discovery starts from previously crawled pages, known backlinks, submitted XML sitemaps and pages submitted manually through Search Console."
  - "Googlebot first reads the raw HTML without JavaScript, then runs a slower rendering pass, so heavy JavaScript without server-side rendering delays indexing."
  - "Crawled currently not indexed means a page failed the quality evaluation, while discovered currently not indexed means Google has not crawled it yet."
image: "/wp-content/uploads/2026/08/How-Google-Crawls-Websites.webp"
imageAlt: "How Google Crawls Websites"
words: 1147
views: 97
format: "html"
---
<div class="bgc-wrap">
<style>
.bgc-wrap{font-family:'Segoe UI', Arial, sans-serif;font-size:17px;line-height:1.75;color:#2e2e2e;max-width:100%;}
.bgc-wrap h2{font-size:25px;color:#2b2b2b;margin:36px 0 16px;font-weight:800;border-left:5px solid #5DB92E;padding-left:14px;}
.bgc-wrap h3{font-size:19px;color:#2b2b2b;margin:18px 0 10px;font-weight:700;}
.bgc-wrap p{margin:0 0 14px;font-size:17px;}
.bgc-wrap a{color:#3f9421;font-weight:600;text-decoration:none;}
.bgc-wrap a:hover{color:#2f7418;text-decoration:none;}
.bgc-wrap ul,.bgc-wrap ol{margin:0 0 16px;padding-left:22px;}
.bgc-wrap li{margin-bottom:8px;font-size:17px;}

.bgc-lede{font-size:20px;color:#333;font-style:italic;margin:0 0 18px;line-height:1.6;border-left:3px solid #5DB92E;padding-left:16px;}

.bgc-meta-row{display:flex;flex-wrap:wrap;gap:10px;margin:0 0 24px;}
.bgc-meta-pill{background:#eef8e8;color:#3f9421;border:1px solid #cdeabb;border-radius:20px;padding:6px 16px;font-size:13px;font-weight:700;text-transform:uppercase;letter-spacing:.5px;}

/* Stat cards */
.bgc-stat-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin:20px 0 30px;}
.bgc-stat-card{background:#f7faf5;border:1px solid #e3ede0;border-radius:12px;padding:22px 16px;text-align:center;}
.bgc-stat-num{font-size:32px;font-weight:800;color:#5DB92E;margin-bottom:6px;}
.bgc-stat-card p{margin:0;font-size:17px;color:#4a4a4a;}
@media(max-width:820px){.bgc-stat-grid{grid-template-columns:1fr;}}

/* Pipeline with loop-back */
.bgc-pipeline{margin:20px 0 30px;background:#fff;border:1px solid #e3ede0;border-radius:14px;padding:26px 20px;position:relative;}
.bgc-pipe-row{display:flex;align-items:center;gap:6px;flex-wrap:wrap;justify-content:center;}
.bgc-pipe-step{background:#f7faf5;border:2px solid #5DB92E;border-radius:10px;padding:14px 10px;text-align:center;font-size:13px;font-weight:700;color:#2b2b2b;flex:1;min-width:110px;}
.bgc-pipe-step .n{display:block;color:#5DB92E;font-size:11px;font-weight:800;margin-bottom:4px;}
.bgc-pipe-arrow{color:#5DB92E;font-weight:800;font-size:18px;}
.bgc-pipe-loop{text-align:center;font-size:12px;color:#7a7a7a;margin-top:14px;font-style:italic;}
@media(max-width:820px){.bgc-pipe-row{flex-direction:column;}}

/* Two-wave comparison */
.bgc-waves{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin:20px 0 30px;}
.bgc-wave-card{border-radius:12px;padding:20px;border:1px solid #e3ede0;}
.bgc-wave-card.first{background:#eef8e8;border-top:4px solid #5DB92E;}
.bgc-wave-card.second{background:#fff8ea;border-top:4px solid #e2a52c;}
.bgc-wave-card h3{margin:0 0 8px;font-size:16px;}
.bgc-wave-card p{margin:0;font-size:14px;color:#4a4a4a;}
@media(max-width:700px){.bgc-waves{grid-template-columns:1fr;}}

/* Table */
.bgc-table-wrap{overflow-x:auto;margin:20px 0 30px;}
.bgc-table{width:100%;border-collapse:collapse;font-size:17px;}
.bgc-table th{background:#2b2b2b;color:#fff;padding:13px 16px;text-align:left;font-weight:700;}
.bgc-table td{padding:13px 16px;border-bottom:1px solid #e3ede0;}
.bgc-table tr:nth-child(even) td{background:#f7faf5;}

/* Interactive tool */
.bgc-calc{border-radius:16px;overflow:hidden;border:1px solid #e3ede0;margin:20px 0 32px;}
.bgc-calc-header{background:#2b2b2b;color:#fff;padding:18px 22px;}
.bgc-calc-header h3{margin:0 0 4px;font-size:19px;color:#fff;}
.bgc-calc-header p{margin:0;font-size:14px;color:#c7d9c0;}
.bgc-calc-body{padding:22px;background:#fff;}
.bgc-calc-row{margin-bottom:14px;}
.bgc-calc-row label{font-size:15px;font-weight:700;color:#2b2b2b;display:block;margin-bottom:6px;}
.bgc-calc-row select{width:100%;padding:10px;border-radius:8px;border:1px solid #e3ede0;font-size:14px;color:#3a3a3a;font-family:'Segoe UI',Arial,sans-serif;background:#f7faf5;box-sizing:border-box;}
.bgc-calc-output{margin-top:8px;background:#f7faf5;border:1px solid #e3ede0;border-radius:10px;padding:16px 18px;font-size:15px;color:#2b2b2b;font-weight:700;text-align:center;}

/* FAQ */
.bgc-faq-item{margin-bottom:14px;}
.bgc-faq-q{background:#f2f5f0;border-radius:8px 8px 0 0;padding:14px 18px;font-weight:700;color:#2b2b2b;font-size:17px;}
.bgc-faq-a{background:#fff;border:1px solid #eef1ec;border-top:none;border-radius:0 0 8px 8px;padding:16px 18px;font-size:17px;color:#4a4a4a;}

/* Related */
.bgc-related-box{background:#f7faf5;border:1px solid #e3ede0;border-radius:12px;padding:22px;margin:20px 0 30px;}
.bgc-related-box h3{margin:0 0 12px;color:#2b2b2b;}
.bgc-related-box ul{margin:0;padding-left:20px;}
.bgc-related-box li{margin-bottom:10px;}
.bgc-related-box a{font-weight:600 !important;}

/* What we learn today - badge grid */
.bgc-learn{margin:26px 0 20px;}
.bgc-learn h3{font-size:20px;color:#2b2b2b;margin:0 0 18px;text-align:center;}
.bgc-learn-grid{display:grid;grid-template-columns:1fr 1fr;gap:12px;}
.bgc-learn-card{background:#fff;border:2px solid #cdeabb;border-radius:10px;padding:14px 16px;text-align:center;}
.bgc-learn-card p{margin:0;font-size:14px;color:#3a3a3a;font-weight:600;}
@media(max-width:820px){.bgc-learn-grid{grid-template-columns:1fr;}}
</style>

<div class="bgc-meta-row">
<span class="bgc-meta-pill">Technical SEO</span>
<span class="bgc-meta-pill">Crawling and Indexing</span>
<span class="bgc-meta-pill">Googlebot</span>
<span class="bgc-meta-pill">Search Console</span>
</div>

<p class="bgc-lede">Google indexes only 30 to 60% of a typical website's pages, according to Google's own John Mueller. The rest sit in some in-between state, crawled but excluded, discovered but never fetched, or fetched but never rendered properly. Understanding the actual pipeline between discovery and indexing explains exactly where most of that other 40 to 70% quietly gets lost.</p>

<p>Google crawls websites through a multi-stage pipeline: discovering URLs through links, sitemaps, and prior crawl history, fetching their content, rendering JavaScript-heavy pages in a headless browser, and finally evaluating that content for inclusion in the index. Crawling and indexing are related but genuinely separate processes.</p>
<p>We covered why Google sometimes skips pages entirely in our <a href="/crawl-budget-explained/" target="_blank" rel="noopener">crawl budget guide</a>. This article covers the full pipeline that budget gets spent moving through.</p>

<div class="bgc-stat-grid">
<div class="bgc-stat-card"><div class="bgc-stat-num">30-60%</div><p>of a typical site's pages actually make it into Google's index, per John Mueller</p></div>
<div class="bgc-stat-card"><div class="bgc-stat-num">2</div><p>separate waves handle indexing: a quick HTML pass, then a deferred rendering pass</p></div>
<div class="bgc-stat-card"><div class="bgc-stat-num">0</div><p>guarantee that crawling a page results in it actually being indexed</p></div>
</div>

<h2 id="the-full-pipeline-start-to-finish">The Full Pipeline, Start to Finish</h2>
<div class="bgc-pipeline">
<div class="bgc-pipe-row">
<div class="bgc-pipe-step"><span class="n">1</span>Discovery</div>
<div class="bgc-pipe-arrow">→</div>
<div class="bgc-pipe-step"><span class="n">2</span>Crawling / Fetching</div>
<div class="bgc-pipe-arrow">→</div>
<div class="bgc-pipe-step"><span class="n">3</span>Rendering</div>
<div class="bgc-pipe-arrow">→</div>
<div class="bgc-pipe-step"><span class="n">4</span>Indexing</div>
</div>
<p class="bgc-pipe-loop">The pipeline isn't strictly linear: new links found during rendering can trigger additional crawling, looping back to Stage 1.</p>
</div>

<h2 id="stage-1-how-google-discovers-a-url">Stage 1: How Google Discovers a URL</h2>
<p>According to <a href="https://fudugo.com/how-google-does-indexing-a-technical-deep-dive/" target="_blank" rel="noopener">Fudugo's technical deep dive into how Google does indexing</a>, discovery starts from seed URLs: previously crawled pages, known backlinks, submitted XML sitemaps, and pages manually submitted through Search Console.</p>

<p>According to <a href="https://www.incremys.com/en/resources/blog/seo-crawling" target="_blank" rel="noopener">Incremys' guide to understanding Google's site exploration</a>, a sitemap is a discovery and prioritization signal, not an "index now" button. Submitting one never forces crawling or indexing directly.</p>

<h2 id="stage-2-and-3-fetching-then-rendering">Stage 2 and 3: Fetching, Then Rendering</h2>
<p>Modern Googlebot processes pages in two distinct waves.</p>

<div class="bgc-waves">
<div class="bgc-wave-card first">
<h3>First Wave: Quick Crawl</h3>
<p>Googlebot extracts what it can directly from the raw HTML, links, metadata, and visible text, without executing any JavaScript yet.</p>
</div>
<div class="bgc-wave-card second">
<h3>Second Wave: Rendering</h3>
<p>A separate, more resource-intensive pass executes JavaScript in a headless browser to see the page the way a real visitor would.</p>
</div>
</div>

<p>According to <a href="https://seo-hacker.com/how-google-crawling-works/" target="_blank" rel="noopener">SEO Hacker's step-by-step guide to Google crawling</a>, rendering requires significant computational resources, which is why Google prioritizes which pages get rendered based on page importance and freshness requirements.</p>

<h2 id="stage-4-what-happens-during-indexing">Stage 4: What Happens During Indexing</h2>
<p>According to <a href="https://www.incremys.com/en/resources/blog/googlebot" target="_blank" rel="noopener">Incremys' 2026 guide to managing Googlebot</a>, indexing analyzes the fully rendered content to determine its topic and decide whether it earns a place in the index at all.</p>

<h2 id="why-crawling-doesn-t-guarantee-indexing">Why Crawling Doesn't Guarantee Indexing</h2>
<div class="bgc-table-wrap">
<table class="bgc-table">
<thead>
<tr><th>Search Console Status</th><th>What Actually Happened</th></tr>
</thead>
<tbody>
<tr><td>Crawled – currently not indexed</td><td>Passed discovery and fetch, failed the quality evaluation stage</td></tr>
<tr><td>Discovered – currently not indexed</td><td>Google knows the URL exists but hasn't crawled it yet</td></tr>
<tr><td>Excluded by noindex tag</td><td>Fetched successfully, then explicitly told not to index</td></tr>
<tr><td>Alternate page with proper canonical tag</td><td>Crawled, but a different URL was chosen as canonical</td></tr>
<tr><td>Page with redirect</td><td>Crawled, but authority passed to a different destination URL</td></tr>
</tbody>
</table>
</div>

<h2 id="crawl-to-index-diagnostic">Crawl-to-Index Diagnostic</h2>
<p>Select the Search Console status you're seeing to identify which pipeline stage is the actual problem.</p>

<div class="bgc-calc">
<div class="bgc-calc-header">
<h3>Crawl-to-Index Diagnostic</h3>
<p>Matches a Search Console status to the pipeline stage and likely fix</p>
</div>
<div class="bgc-calc-body">
<div class="bgc-calc-row">
<label>What status are you seeing in Search Console?</label>
<select id="bgcStatus" onchange="bgcDiagnose()">
<option value="discovered">Discovered – currently not indexed</option>
<option value="crawled">Crawled – currently not indexed</option>
<option value="noindex">Excluded by noindex tag</option>
<option value="canonical">Alternate page with proper canonical tag</option>
<option value="redirect">Page with redirect</option>
</select>
</div>
<div class="bgc-calc-output" id="bgcResult">Google knows this URL exists but hasn't crawled it yet. Usually a crawl budget or priority issue. Add strong internal links pointing to it.</div>
</div>
</div>

<script>
function bgcDiagnose(){
  var status = document.getElementById('bgcStatus').value;
  var out = document.getElementById('bgcResult');
  if(status === 'discovered'){
    out.innerText = "Google knows this URL exists but hasn't crawled it yet. Usually a crawl budget or priority issue. Add strong internal links pointing to it.";
  } else if(status === 'crawled'){
    out.innerText = "Google fetched and likely rendered the page, then judged the content not worth indexing. Focus on improving depth and uniqueness, not technical fixes.";
  } else if(status === 'noindex'){
    out.innerText = "Working as designed, if intentional. If not, check for an accidental noindex tag left over from staging or a plugin default.";
  } else if(status === 'canonical'){
    out.innerText = "Google chose a different URL as the canonical version. Confirm your canonical tags point where you actually intend them to.";
  } else if(status === 'redirect'){
    out.innerText = "The page redirects elsewhere and authority followed. Confirm this is intentional and the destination is the correct final URL.";
  }
}
</script><h2 id="why-understanding-crawling-and-indexing-together-matters">Why Understanding Crawling and Indexing Together Matters</h2>
<p>According to <a href="https://www.seo-kreativ.de/en/blog/crawling-indexing-google/" target="_blank" rel="noopener">SEO Kreativ's guide to crawling and indexing explained simply</a>, treating these as one combined process is a common mistake. Every page you want visible must be crawlable, renderable, and indexable, three distinct hurdles rather than one.</p>

<p>According to <a href="https://cyberraiden.wordpress.com/2026/03/26/google-search-explained-crawling-indexing-ranking-ai-features-limitations/" target="_blank" rel="noopener">a detailed explainer on how Google Search works</a>, crawling and indexing together form the foundation the entire ranking system depends on, powering everything from traditional results to AI Overviews and AI Mode.</p>

<h2 id="internal-linking-s-role-in-the-discovery-stage">Internal Linking's Role in the Discovery Stage</h2>
<p>According to Incremys' guide to SEO crawling referenced above, internal linking plays a dual role in both crawling and indexing outcomes: it aids discovery of new pages and clarifies the site's overall hierarchy for Google to interpret.</p>

<p>The deeper a page sits, meaning the more clicks required from an entry point to reach it, the harder it becomes to discover and the less frequently it gets revisited once it is crawled and indexed for the first time.</p>

<h2 id="what-slows-this-pipeline-down">What Slows This Pipeline Down</h2>
<p>According to <a href="https://viacon.io/blog/google-crawl-and-google-index/" target="_blank" rel="noopener">Viacon's beginner's guide to Google crawl versus index</a>, excessive JavaScript reliance without server-side rendering delays the second wave significantly, since the rendering queue is inherently slower than the initial HTML pass.</p>

<p>According to <a href="https://digitalstrategyforce.com/journal/how-does-google-crawl-and-index-your-website/" target="_blank" rel="noopener">Digital Strategy Force's guide to how Google crawls and indexes</a>, architectural clarity, every URL reachable, renderable, and unambiguous in its canonical identity, matters more to full indexing than content quality alone.</p><h2 id="faqs-on-how-google-crawls-websites">FAQs on How Google Crawls Websites</h2>

<div class="bgc-faq-item">
<div class="bgc-faq-q">Does submitting a sitemap guarantee Google will index my pages?</div>
<div class="bgc-faq-a">No. A sitemap is a discovery and prioritization signal for crawling and indexing, helping Google find URLs faster, but it never forces either process directly.</div>
</div>
<div class="bgc-faq-item">
<div class="bgc-faq-q">Why would Google crawl a page but not index it?</div>
<div class="bgc-faq-a">This typically means the page passed discovery and fetching but failed the quality evaluation stage, often due to thin content, duplication, or a mismatch with search intent.</div>
</div>
<div class="bgc-faq-item">
<div class="bgc-faq-q">What is the two-wave indexing process?</div>
<div class="bgc-faq-a">Google first extracts what it can from raw HTML without executing JavaScript, then runs a separate, more resource-intensive rendering pass later to see the fully executed page.</div>
</div>
<div class="bgc-faq-item">
<div class="bgc-faq-q">How long does crawling and indexing take for a new page?</div>
<div class="bgc-faq-a">It varies widely, from hours for established, high-authority sites to several weeks for new sites without existing authority or backlinks.</div>
</div>
<div class="bgc-faq-item">
<div class="bgc-faq-q">Can blocking CSS or JavaScript in robots.txt hurt crawling and indexing?</div>
<div class="bgc-faq-a">Yes. If critical resources needed to render the page correctly are blocked, Google may fail to see the page's actual content, which can degrade both evaluation and indexing.</div>
</div>
<div class="bgc-faq-item">
<div class="bgc-faq-q">What's the fastest way to diagnose a crawling and indexing problem?</div>
<div class="bgc-faq-a">Check the specific exclusion reason in Search Console's Coverage or Pages report. Each status maps to a distinct stage in the pipeline, pointing directly at where the process broke down.</div>
</div>

<div class="bgc-related-box">
<h3>Related Articles</h3>
<ul>
<li><a href="/crawl-budget-explained/" target="_blank" rel="noopener">Crawl Budget Explained: Why Google Might Be Ignoring Half Your Site</a></li>
<li><a href="/robots-txt-complete-guide/" target="_blank" rel="noopener">Robots.txt Explained: Complete Guide with Examples</a></li>
<li><a href="/what-is-x-robots-tag-when-to-use-it/" target="_blank" rel="noopener">What Is X-Robots-Tag? When Should You Use It?</a></li>
<li><a href="/build-xml-sitemap-generator-php/" target="_blank" rel="noopener">Build Your Own XML Sitemap Generator in PHP</a></li>
</ul>
</div>

<div class="bgc-learn">
<h3>What We Learn Today</h3>
<div class="bgc-learn-grid">
<div class="bgc-learn-card"><p>Only 30-60% of a typical site's pages actually get indexed</p></div>
<div class="bgc-learn-card"><p>Discovery starts from sitemaps, links, and Search Console submissions</p></div>
<div class="bgc-learn-card"><p>A sitemap signals priority; it never forces indexing directly</p></div>
<div class="bgc-learn-card"><p>Indexing runs in two waves: quick HTML pass, then deferred rendering</p></div>
<div class="bgc-learn-card"><p>Crawling and indexing are separate; one doesn't guarantee the other</p></div>
<div class="bgc-learn-card"><p>Search Console's exclusion reasons map directly to the pipeline stage</p></div>
</div>
</div>

</div>
