---
title: "How to Fix \"Discovered Currently Not Indexed\" Pages: The Complete 2026 Guide"
slug: "discovered-currently-not-indexed-fix"
date: "2026-08-09T05:05:48"
updated: "2026-08-09T08:36:46"
author: "santajigade"
categories: ["google-search-console", "seo"]
primaryCategory: "google-search-console"
description: "Discovered - currently not indexed doesn't mean rejection. Learn the real causes, how to diagnose them, and the structural fixes that actually work."
focusKeyword: "Discovered Currently Not Indexed"
takeaways:
  - "\"Discovered, currently not indexed\" means Google knows the URL exists but has not crawled it yet."
  - "Common causes are a slow site, low site or page priority for Google, and a stretched crawl budget."
  - "It is different from \"Crawled, currently not indexed\", where Google fetched the page and chose not to index it."
  - "Fix the cause first by adding internal links from strong pages, improving content depth and cleaning up the sitemap."
  - "Request indexing only after fixing the cause; manual requests are limited to roughly 10 to 15 URLs a day."
image: "/wp-content/uploads/2026/08/Discovered-Currently-Not-Indexed.webp"
imageAlt: "Discovered Currently Not Indexed"
words: 1724
views: 87
format: "html"
---
<div class="bmc-flow">
<style>
@import url('https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600;700;800&display=swap');

.bmc-flow{
  --bx-green:#5DB92E;
  --bx-green-deep:#4a9e24;
  --bx-gold:#F4B41A;
  --bx-ink:#2b2b2b;
  --bx-steel:#5a6570;
  --bx-steel-2:#8a96a1;
  --bx-line:#E3EDE0;
  --bx-red:#c95d5d;
  --bx-blue:#6fa8dc;
  --bx-disp:'Open Sans',Arial,sans-serif;
  --bx-body:'Open Sans',system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif;
  font-family:var(--bx-body);font-weight:400;font-style:normal;color:var(--bx-ink);line-height:1.75;font-size:17px;
  max-width:920px;margin:0 auto;padding:0;-webkit-font-smoothing:antialiased;
}
.bmc-flow *{box-sizing:border-box;}
.bmc-flow p{margin:0 0 14px;font-size:17px;}
.bmc-flow a{color:var(--bx-green-deep);text-decoration:none;font-weight:600;}
.bmc-flow a:hover{text-decoration:none;color:var(--bx-green);}
.bmc-flow strong{font-weight:700;}

.bmc-flow h2{font-family:var(--bx-disp);font-weight:700;font-size:26px;line-height:1.2;margin:36px 0 16px;color:var(--bx-ink);}
.bmc-flow h2 .bx-num{color:var(--bx-green);font-weight:800;margin-right:8px;}
.bmc-flow h3{font-family:var(--bx-disp);font-weight:600;font-size:17px;margin:17px 0 10px;color:var(--bx-ink);}
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

.bmc-flow .bx-checklist{display:flex;flex-direction:column;gap:10px;margin:20px 0 30px;}
.bmc-flow .bx-check-item{display:flex;gap:13px;background:#fff;border:1px solid var(--bx-line);border-left:4px solid var(--bx-green);border-radius:10px;padding:14px 17px;align-items:flex-start;}
.bmc-flow .bx-check-icon{width:22px;height:22px;border-radius:6px;background:var(--bx-green);flex-shrink:0;margin-top:2px;position:relative;}
.bmc-flow .bx-check-icon::after{content:"✓";position:absolute;top:-2px;left:5px;color:#fff;font-weight:800;font-size:13px;}
.bmc-flow .bx-check-item p{margin:0;font-size:17px;color:#3a3a3a;}
.bmc-flow .bx-check-item strong{color:var(--bx-ink);}

.bmc-flow .bx-steps{background:#20272C;border-radius:16px;padding:24px 20px;margin:20px 0 30px;}
.bmc-flow .bx-steps .dc-hint{font-size:17px;color:var(--bx-steel-2);text-transform:uppercase;letter-spacing:1.4px;font-family:var(--bx-disp);margin-bottom:14px;font-weight:600;}
.bmc-flow .bx-track{display:flex;flex-wrap:wrap;gap:8px;}
.bmc-flow .bx-step{flex:1 1 92px;min-width:88px;cursor:pointer;border:1px solid rgba(255,255,255,.16);border-radius:11px;padding:12px 8px;background:rgba(255,255,255,.04);color:#fff;text-align:center;transition:transform .14s ease,background .18s ease,border-color .18s ease;}
.bmc-flow .bx-step:hover{transform:translateY(-3px);background:rgba(93,185,46,.18);border-color:var(--bx-green);}
.bmc-flow .bx-step.on{background:var(--bx-green);border-color:var(--bx-green);}
.bmc-flow .bx-step .no{font-family:var(--bx-disp);font-weight:800;font-size:17px;color:var(--bx-gold)!important;line-height:1;}
.bmc-flow .bx-step.on .no{color:#fff!important;}
.bmc-flow .bx-step .lb{font-size:17px;text-transform:uppercase;letter-spacing:.4px;margin-top:5px;color:#fff!important;line-height:1.2;}
.bmc-flow .bx-stepdetail{margin-top:16px;background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.08);border-radius:11px;padding:15px 17px;min-height:84px;}
.bmc-flow .bx-stepdetail .dt-t{font-family:var(--bx-disp);letter-spacing:.4px;color:var(--bx-gold)!important;font-size:17px;margin:0 0 4px;font-weight:700;}
.bmc-flow .bx-stepdetail .dt-d{margin:0;font-size:17px;color:#E4E8EB!important;line-height:1.6;}

.bmc-flow .bx-table-wrap{overflow-x:auto;margin:20px 0 30px;}
.bmc-flow .bx-table{width:100%;border-collapse:collapse;font-size:17px;}
.bmc-flow .bx-table th{background:var(--bx-ink);color:#fff;padding:13px 16px;text-align:left;font-family:var(--bx-disp);font-weight:600;font-size:17px;}
.bmc-flow .bx-table td{padding:13px 16px;border-bottom:1px solid var(--bx-line);font-size:17px;}
.bmc-flow .bx-table tr:nth-child(even) td{background:#f7faf5;}

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
.bmc-flow .bx-calc-select{width:100%;padding:8px 10px;border-radius:8px;border:1px solid var(--bx-line);font-size:17px;color:#3a3a3a;font-family:var(--bx-body);background:#f7faf5;}
.bmc-flow .bx-calc-gauge-wrap{margin-top:20px;background:#f7faf5;border-radius:12px;padding:20px;text-align:center;}
.bmc-flow .bx-calc-gauge-track{background:#e8ece7;border-radius:20px;height:28px;overflow:hidden;margin-bottom:12px;}
.bmc-flow .bx-calc-gauge-fill{height:100%;background:linear-gradient(90deg,#c95d5d,#e2a52c,#5DB92E);border-radius:20px;width:0%;transition:width 0.4s ease;display:flex;align-items:center;justify-content:flex-end;padding-right:10px;}
.bmc-flow .bx-calc-gauge-fill span{color:#fff;font-weight:800;font-size:17px;}
.bmc-flow .bx-calc-verdict{font-size:17px;font-weight:700;color:var(--bx-ink);}

.bmc-flow .bx-faq{border:1px solid var(--bx-line);border-radius:12px;overflow:hidden;background:#fff;margin:20px 0 30px;}
.bmc-flow .bx-q{width:100%;text-align:left;background:#fff;border:0;border-top:1px solid var(--bx-line);padding:16px 17px;cursor:pointer;font-family:var(--bx-disp);font-weight:600;font-size:17px;color:var(--bx-ink);display:flex;justify-content:space-between;align-items:center;gap:12px;}
.bmc-flow .bx-faq .bx-q:first-child{border-top:0;}
.bmc-flow .bx-q .ic{color:var(--bx-green);font-weight:800;flex:0 0 auto;transition:transform .2s ease;font-family:var(--bx-body);font-size:20px;}
.bmc-flow .bx-q.on .ic{transform:rotate(45deg);}
.bmc-flow .bx-a{max-height:0;overflow:hidden;transition:max-height .3s ease;padding:0 17px;}
.bmc-flow .bx-a.on{max-height:360px;}
.bmc-flow .bx-a p{padding:2px 0 16px;margin:0;font-size:17px;color:var(--bx-steel);}

.bmc-flow .bx-cta{position:relative;overflow:hidden;border-radius:17px;margin:30px 0 8px;padding:36px 30px;color:#fff;background:radial-gradient(120% 160% at 12% 10%,rgba(244,180,26,.25),transparent 46%),linear-gradient(135deg,#5DB92E 0%,#3f9421 55%,#245214 100%);}
.bmc-flow .bx-cta h2{color:#fff!important;margin:0 0 8px;}
.bmc-flow .bx-cta p{color:rgba(255,255,255,.94)!important;max-width:560px;margin:0 0 20px;font-size:17px;}
.bmc-flow .bx-actions{display:flex;flex-wrap:wrap;gap:12px;}
.bmc-flow .bx-btn{display:inline-flex;align-items:center;gap:8px;font-family:var(--bx-disp);font-size:17px;font-weight:700;padding:12px 20px;border-radius:40px;text-decoration:none;border:0;transition:transform .15s ease,box-shadow .15s ease;}
.bmc-flow .bx-btn.primary{background:#fff;color:var(--bx-green-deep)!important;}
.bmc-flow .bx-btn.ghost{background:rgba(255,255,255,.12);color:#fff!important;border:1.5px solid rgba(255,255,255,.55);}
.bmc-flow .bx-btn:hover{transform:translateY(-2px);box-shadow:0 10px 22px rgba(0,0,0,.18);}

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

.bmc-flow .bx-svgwrap{background:#f7faf5;border:1px solid var(--bx-line);border-radius:14px;padding:20px;margin:20px 0 30px;text-align:center;}
.bmc-flow .bx-svgwrap svg{max-width:100%;height:auto;}
.bmc-flow .bx-svgcap{font-size:17px;color:var(--bx-steel);margin-top:10px;}

.bmc-flow .bx-code{background:#20272C;border-radius:14px;padding:20px 22px;margin:20px 0 30px;overflow-x:auto;}
.bmc-flow .bx-code pre{margin:0;font-family:'Courier New',monospace;font-size:14px;line-height:1.6;color:#c7e8b8;white-space:pre-wrap;word-break:break-word;}
.bmc-flow .bx-code-label{font-family:var(--bx-disp);color:var(--bx-steel-2);text-transform:uppercase;letter-spacing:1.2px;font-size:13px;margin-bottom:10px;font-weight:600;}

.bmc-flow .bx-video-wrap{margin:20px 0 30px;border-radius:14px;overflow:hidden;border:1px solid var(--bx-line);}
.bmc-flow .bx-video-frame{position:relative;padding-bottom:56.25%;height:0;background:#000;}
.bmc-flow .bx-video-frame iframe{position:absolute;top:0;left:0;width:100%;height:100%;border:0;}
.bmc-flow .bx-video-cap{background:#f7faf5;padding:12px 17px;font-size:17px;color:var(--bx-steel);}

.bmc-flow .bx-ad-wrap{margin:40px 0;}
.bmc-flow .bx-ad-divider{display:flex;align-items:center;gap:12px;}
.bmc-flow .bx-ad-divider span{font-size:12px;color:#777;font-weight:600;letter-spacing:1px;text-transform:uppercase;}
.bmc-flow .bx-ad-line{flex:1;border-top:2px dotted #bdbdbd;}
@media(prefers-reduced-motion:reduce){.bmc-flow *{animation:none!important;transition:none!important;}}
</style>

<div class="bx-meta-row">
<span class="bx-meta-pill">Technical SEO</span>
<span class="bx-meta-pill">Indexing</span>
<span class="bx-meta-pill">Google Search Console</span>
<span class="bx-meta-pill">2026</span>
</div>

<p class="bx-lede">Discovered - currently not indexed means Google knows your page exists but hasn't crawled it yet. It's not a penalty and not a rejection, it's a priority queue delay, and the fix has almost nothing to do with clicking "Request Indexing" over and over.</p>

<p>Most site owners panic the moment they see this status and immediately hammer the Request Indexing button. That instinct treats the symptom instead of the cause. If a page sits in this state for weeks, something structural, weak internal links, crawl budget competition, or thin content, is telling Google this page isn't worth prioritizing yet.</p>

<p>The pages affected usually show no last crawl date at all in Search Console, which is the clearest signal that Googlebot hasn't visited yet. That's different from a page Google crawled and rejected, and the fix for each is completely different.</p>

<p>This guide breaks down why discovered - currently not indexed happens, how to diagnose the real cause, and the specific structural fixes that actually move a discovered - currently not indexed page out of this queue.</p>

<div class="bx-specs">
<div class="bx-spec"><div class="v">10-15</div><div class="k">manual indexing requests typically allowed per day in Search Console</div></div>
<div class="bx-spec"><div class="v">4</div><div class="k">core reasons pages get stuck: slow site, low priority, page priority, crawl budget</div></div>
<div class="bx-spec"><div class="v">No date</div><div class="k">last crawl date shown for these URLs, confirming Googlebot hasn't visited yet</div></div>
</div>
<h2 id="what-it-means"><span class="bx-num">01</span>What "Discovered - Currently Not Indexed" Actually Means</h2>
<div class="bx-rule"></div>
<p><a href="https://www.onely.com/blog/how-to-fix-discovered-currently-not-indexed-in-google-search-console/" target="_blank" rel="noopener">Onely's March 2026 guide</a> defines it precisely: the status means Google knows the URL exists but has not crawled it yet. The page may have been found through internal links or an XML sitemap, but Google hasn't fetched it, so it can't be indexed. In Search Console, these URLs usually show no last crawl date at all.</p>

<p>Onely's guide is careful to note what this doesn't mean: it does not automatically signal the page is low quality or permanently excluded. The most common causes are weak internal discovery, low crawl priority, duplicate or low-value URL patterns, and server or crawl-efficiency constraints.</p>

<h2 id="why-happens"><span class="bx-num">02</span>Why This Happens: The Real Causes</h2>
<div class="bx-rule"></div>
<p><a href="https://ziptie.dev/blog/how-to-fix-discovered-currently-not-indexed/" target="_blank" rel="noopener">ZipTie's March 2026 breakdown</a> lists four specific reasons pages land here: the website is slow, the entire site isn't a priority for Google, the specific page isn't a priority within the site, or crawl budget is simply stretched thin across too many URLs.</p>

<p><a href="https://www.searchenginejournal.com/fixing-discovered-currently-not-indexed/491432/" target="_blank" rel="noopener">Search Engine Journal's coverage</a> of Google's own statements adds important nuance from John Mueller directly: Googlers have repeatedly said there's no crawl budget in the exact way SEOs imagine it, but Google does have finite capacity, and it tends to index pages that demonstrate real value while declining to prioritize others.</p>

<div class="bx-note">
<span class="lbl">More Pages Isn't Automatically Better</span>
<p>Search Engine Journal's coverage documents Mueller's direct response to a large e-commerce site asking whether deindexing millions of duplicate product pages would help: the real question isn't page count, it's whether the remaining pages actually improve quality. Trimming volume without improving substance doesn't move the needle.</p>
</div>
<h2 id="discovered-vs-crawled"><span class="bx-num">03</span>Discovered vs Crawled - Currently Not Indexed</h2>
<div class="bx-rule"></div>
<p>Onely's guide, referenced above, draws the line that matters most for diagnosis: discovered means Google has not fetched the page at all. Crawled means Google fetched it and still declined to index it, a fundamentally different, quality-driven decision rather than a queue position.</p>

<p><a href="https://www.masterseotool.com/blog/discovered-currently-not-indexed/" target="_blank" rel="noopener">MasterSEOTool's 2026 guide</a> reinforces why this distinction changes your entire approach: if a page is discovered but not indexed, Google hasn't evaluated the content yet, it simply hasn't allocated crawl resources. There's no content judgment to reverse, only a priority problem to solve.</p>

<h2 id="assess-severity"><span class="bx-num">04</span>Step 1: Assess the Severity Before Acting</h2>
<div class="bx-rule"></div>
<p>Onely's guide, referenced above, recommends a specific sequence before touching anything: confirm the URL is genuinely still not indexed, check the scale of the issue across your site, sample a representative set of affected URLs, and match the pattern to a likely diagnosis before prioritizing by business importance.</p>

<p>A handful of affected pages is a different problem than thousands. <a href="https://ahrefs.com/blog/discovered-currently-not-indexed/" target="_blank" rel="noopener">Ahrefs' guide to the status</a> notes that for a small number of URLs, requesting indexing directly through Search Console is often the fastest fix. For a large-scale pattern, the underlying cause needs solving first.</p>

<h2 id="video"><span class="bx-num">05</span>Watch: Fixing Discovered, Currently Not Indexed</h2>
<div class="bx-rule"></div>
<p>For a step-by-step walkthrough of diagnosing and fixing this exact status in Search Console, this explainer covers the practical workflow directly.</p>

<div class="bx-video-wrap">
<div class="bx-video-frame">
<iframe src="https://www.youtube.com/embed/kyM0XaLnRd4" title="Discovered, Currently Not Indexed: How to Fix It (Google Search Console)" allowfullscreen></iframe>
</div>
<div class="bx-video-cap">"Discovered, Currently Not Indexed: How to Fix It (Google Search Console)" — Ryan Robinson. Source: YouTube.</div>
</div>

<h2 id="fix-crawl-budget"><span class="bx-num">06</span>Step 2: Fix Crawl Budget and Internal Linking</h2>
<div class="bx-rule"></div>
<p><a href="https://www.easyguideshub.com/2026/07/how-to-solve-indexing-issues-in-2026-az.html" target="_blank" rel="noopener">EasyGuidesHub's 2026 A-Z guide</a> is direct about the fix: to resolve persistent indexation issues, improve the underlying content depth, fix technical errors, and update internal links before requesting re-indexing again. Resubmitting a sitemap alone doesn't guarantee indexing of pages Google has already deprioritized.</p>

<p><a href="https://www.semrush.com/blog/internal-linking-mistakes/" target="_blank" rel="noopener">Semrush's internal linking guide</a> identifies orphan pages, pages with zero internal links pointing to them, as a common structural cause. Fixing broken links and connecting priority pages to your site's stronger, more established pages directly signals importance to Google's crawler.</p>

<div class="bx-svgwrap">
<svg viewBox="0 0 700 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Diagram showing the discovered currently not indexed diagnostic path: check internal links, crawl depth, sitemap quality, and content differentiation before requesting indexing again">
<rect x="20" y="30" width="660" height="50" rx="10" fill="#20272C"/>
<text x="350" y="60" text-anchor="middle" fill="#fff" font-family="Open Sans" font-size="13" font-weight="700">Page Status: Discovered - Currently Not Indexed</text>

<rect x="20" y="110" width="150" height="70" rx="10" fill="#f7faf5" stroke="#cdeabb"/>
<text x="95" y="140" text-anchor="middle" fill="#2b2b2b" font-family="Open Sans" font-size="12" font-weight="700">Internal</text>
<text x="95" y="158" text-anchor="middle" fill="#2b2b2b" font-family="Open Sans" font-size="12" font-weight="700">Links</text>

<rect x="185" y="110" width="150" height="70" rx="10" fill="#f7faf5" stroke="#cdeabb"/>
<text x="260" y="140" text-anchor="middle" fill="#2b2b2b" font-family="Open Sans" font-size="12" font-weight="700">Crawl</text>
<text x="260" y="158" text-anchor="middle" fill="#2b2b2b" font-family="Open Sans" font-size="12" font-weight="700">Depth</text>

<rect x="350" y="110" width="150" height="70" rx="10" fill="#f7faf5" stroke="#cdeabb"/>
<text x="425" y="140" text-anchor="middle" fill="#2b2b2b" font-family="Open Sans" font-size="12" font-weight="700">Sitemap</text>
<text x="425" y="158" text-anchor="middle" fill="#2b2b2b" font-family="Open Sans" font-size="12" font-weight="700">Quality</text>

<rect x="515" y="110" width="150" height="70" rx="10" fill="#f7faf5" stroke="#cdeabb"/>
<text x="590" y="140" text-anchor="middle" fill="#2b2b2b" font-family="Open Sans" font-size="12" font-weight="700">Content</text>
<text x="590" y="158" text-anchor="middle" fill="#2b2b2b" font-family="Open Sans" font-size="12" font-weight="700">Differentiation</text>

<line x1="350" y1="80" x2="95" y2="110" stroke="#5DB92E" stroke-width="2"/>
<line x1="350" y1="80" x2="260" y2="110" stroke="#5DB92E" stroke-width="2"/>
<line x1="350" y1="80" x2="425" y2="110" stroke="#5DB92E" stroke-width="2"/>
<line x1="350" y1="80" x2="590" y2="110" stroke="#5DB92E" stroke-width="2"/>
</svg>
<p class="bx-svgcap">Check all four structural factors before requesting indexing again — repeated requests without fixing the cause rarely work.</p>
</div>

<h2 id="when-request-indexing"><span class="bx-num">07</span>When Request Indexing Actually Helps</h2>
<div class="bx-rule"></div>
<p>Ahrefs' guide, referenced above, notes there's an unofficial daily limit on manual submissions, typically 10 to 15 URLs per day, and confirms Google offers a batch Indexing API for submitting multiple URLs at once for eligible content types.</p>

<p><a href="https://www.ryrob.com/discovered-currently-not-indexed-fix/" target="_blank" rel="noopener">Ryan Robinson's guide</a>, matching the video above, frames the right sequence clearly: request indexing works best after structural fixes are made, not as a substitute for them. Repeating the request on an unchanged page rarely produces a different outcome.</p>
<h2 id="cause-fix-table"><span class="bx-num">08</span>Cause vs Fix Reference Table</h2>
<div class="bx-rule"></div>
<p>Different root causes call for entirely different fixes, which is why diagnosis has to come before action.</p>

<div class="bx-table-wrap">
<table class="bx-table">
<thead>
<tr><th>Likely Cause</th><th>Signal to Check</th><th>Primary Fix</th></tr>
</thead>
<tbody>
<tr><td>Weak internal linking</td><td>Orphan pages, few internal links pointing in</td><td>Link from established, relevant pages</td></tr>
<tr><td>Crawl budget competition</td><td>Large site, many low-value URLs</td><td>Trim thin/duplicate pages, prioritize sitemap</td></tr>
<tr><td>Slow site performance</td><td>Poor Core Web Vitals, slow server response</td><td>Improve page speed and server capacity</td></tr>
<tr><td>Low page priority</td><td>Thin, generic, or commodity content</td><td>Add genuine depth and differentiation</td></tr>
</tbody>
</table>
</div>

<h2 id="code"><span class="bx-num">09</span>Checking Sitemap Priority and Orphan Pages</h2>
<div class="bx-rule"></div>
<p>Here's a practical way to flag orphan pages and confirm your sitemap reflects genuine priority rather than every URL treated equally.</p>

<div class="bx-code">
<div class="bx-code-label">XML Sitemap with Priority Signals</div>
<pre>&lt;url&gt;
  &lt;loc&gt;https://example.com/high-priority-page/&lt;/loc&gt;
  &lt;lastmod&gt;2026-08-01&lt;/lastmod&gt;
  &lt;priority&gt;0.9&lt;/priority&gt;
&lt;/url&gt;
&lt;url&gt;
  &lt;loc&gt;https://example.com/low-priority-page/&lt;/loc&gt;
  &lt;lastmod&gt;2025-02-14&lt;/lastmod&gt;
  &lt;priority&gt;0.3&lt;/priority&gt;
&lt;/url&gt;

# Only include indexable, canonical URLs in your sitemap.
# Remove noindexed, redirected, or duplicate URLs entirely.</pre>
</div>

<div class="bx-code">
<div class="bx-code-label">Finding Orphan Pages (Screaming Frog CLI)</div>
<pre># Crawl the site and cross-reference against the sitemap
screamingfrogseospider --crawl https://example.com \
  --headless --save-crawl \
  --export-tabs "Internal:All,Sitemaps:URLs in Sitemap" \
  --output-folder ./orphan-audit

# Any sitemap URL with zero internal inlinks is an orphan page</pre>
</div>

<h2 id="checklist"><span class="bx-num">10</span>Step-by-Step Fix Checklist</h2>
<div class="bx-rule"></div>
<p>A structural approach resolves discovered - currently not indexed far more reliably than repeated manual requests.</p>

<div class="bx-checklist">
<div class="bx-check-item"><div class="bx-check-icon"></div><p><strong>Confirm the page truly has no last crawl date</strong> in Search Console before assuming a discovery problem.</p></div>
<div class="bx-check-item"><div class="bx-check-icon"></div><p><strong>Add internal links from established, relevant pages</strong>, orphan pages send a low-priority signal.</p></div>
<div class="bx-check-item"><div class="bx-check-icon"></div><p><strong>Clean up your XML sitemap</strong>, removing noindexed, redirected, or duplicate URLs entirely.</p></div>
<div class="bx-check-item"><div class="bx-check-icon"></div><p><strong>Improve page speed and server response</strong> if crawl capacity looks like a bottleneck.</p></div>
<div class="bx-check-item"><div class="bx-check-icon"></div><p><strong>Only request indexing after fixing the cause</strong>, and reserve it for genuinely important URLs given the daily limit.</p></div>
</div>

<h2 id="stepper"><span class="bx-num">11</span>Priority Diagnostic Workflow</h2>
<div class="bx-rule"></div>
<p>Five steps cover a complete diagnostic and fix process. Tap each one for the specific action.</p>

<div class="bx-steps" id="bxSteps">
  <div class="dc-hint">Tap a factor &darr;</div>
  <div class="bx-track" role="group" aria-label="Discovered currently not indexed priority workflow steps">
    <div class="bx-step on" data-t="Assess Severity" data-d="Confirm the URL is still not indexed, check how many pages are affected, and sample a representative set before acting."><div class="no">1</div><div class="lb">Assess</div></div>
    <div class="bx-step" data-t="Check Internal Links" data-d="Look for orphan pages with no internal links pointing to them. Link priority pages from established, relevant content."><div class="no">2</div><div class="lb">Internal Links</div></div>
    <div class="bx-step" data-t="Audit the Sitemap" data-d="Remove noindexed, redirected, or duplicate URLs from your sitemap. A clean sitemap signals genuine priority."><div class="no">3</div><div class="lb">Sitemap</div></div>
    <div class="bx-step" data-t="Improve Crawl Efficiency" data-d="For large sites, trim thin or duplicate pages competing for the same limited crawl budget."><div class="no">4</div><div class="lb">Crawl Budget</div></div>
    <div class="bx-step" data-t="Request Indexing Last" data-d="Only after structural fixes are made, request indexing for your highest-priority URLs, respecting the daily submission limit."><div class="no">5</div><div class="lb">Request</div></div>
  </div>
  <div class="bx-stepdetail" aria-live="polite">
    <p class="dt-t" id="bxStepT">Assess Severity</p>
    <p class="dt-d" id="bxStepD">Confirm the URL is still not indexed, check how many pages are affected, and sample a representative set before acting.</p>
  </div>
</div>

<h2 id="score"><span class="bx-num">12</span>Indexing Priority Score</h2>
<div class="bx-rule"></div>
<p>Score a specific stuck page against the factors that determine whether Google is likely to prioritize crawling it soon.</p>

<div class="bx-calc">
<div class="bx-calc-header">
<h3>Indexing Priority Score</h3>
<p>Select the option that matches the page you're diagnosing</p>
</div>
<div class="bx-calc-body">

<div class="bx-calc-factor">
<div class="bx-calc-factor-top"><label>Internal link count</label><span>30 pts</span></div>
<select class="bx-calc-select" data-weight="30" onchange="bxCalc()">
<option value="0">Orphan page, zero internal links</option>
<option value="0.5">A few internal links exist</option>
<option value="1">Well-linked from established pages</option>
</select>
</div>

<div class="bx-calc-factor">
<div class="bx-calc-factor-top"><label>Content differentiation</label><span>25 pts</span></div>
<select class="bx-calc-select" data-weight="25" onchange="bxCalc()">
<option value="0">Thin or commodity content, similar to others</option>
<option value="0.5">Somewhat unique</option>
<option value="1">Substantive, clearly differentiated content</option>
</select>
</div>

<div class="bx-calc-factor">
<div class="bx-calc-factor-top"><label>Site crawl budget pressure</label><span>25 pts</span></div>
<select class="bx-calc-select" data-weight="25" onchange="bxCalc()">
<option value="0">Large site, many competing low-value URLs</option>
<option value="0.5">Moderate site size</option>
<option value="1">Small site, minimal crawl budget competition</option>
</select>
</div>

<div class="bx-calc-factor">
<div class="bx-calc-factor-top"><label>Site speed and server response</label><span>20 pts</span></div>
<select class="bx-calc-select" data-weight="20" onchange="bxCalc()">
<option value="0">Slow load times, server strain evident</option>
<option value="0.5">Average performance</option>
<option value="1">Fast, healthy Core Web Vitals</option>
</select>
</div>

<div class="bx-calc-gauge-wrap">
<div class="bx-calc-gauge-track"><div class="bx-calc-gauge-fill" id="bxGaugeFill"><span id="bxGaugeScore">0%</span></div></div>
<div class="bx-calc-verdict" id="bxVerdict">Select an option for each factor to calculate your score.</div>
</div>

</div>
</div>

<script>
function bxCalc(){
  var selects = document.querySelectorAll('.bx-calc-select');
  var total = 0;
  selects.forEach(function(s){
    var weight = parseFloat(s.getAttribute('data-weight'));
    var value = parseFloat(s.value);
    total += weight * value;
  });
  var pct = Math.round(total);
  document.getElementById('bxGaugeFill').style.width = pct + '%';
  document.getElementById('bxGaugeScore').innerText = pct + '%';
  var verdict = document.getElementById('bxVerdict');
  if(pct >= 80){ verdict.innerText = "Strong candidate for a fast fix. Request indexing after any remaining small gaps are closed."; }
  else if(pct >= 50){ verdict.innerText = "Moderate priority. Fix internal linking and content depth before requesting indexing."; }
  else if(pct > 0){ verdict.innerText = "Significant structural issues. Focus on internal links and crawl budget before anything else."; }
  else { verdict.innerText = "Select an option for each factor to calculate your score."; }
}

(function(){
  var root=document.currentScript.parentNode.querySelector('.bmc-flow')||document.querySelector('.bmc-flow');
  var steps=root.querySelectorAll('#bxSteps .bx-step'),
      sT=root.querySelector('#bxStepT'),sD=root.querySelector('#bxStepD');
  steps.forEach(function(s){s.addEventListener('click',function(){
    steps.forEach(function(x){x.classList.remove('on');}); s.classList.add('on');
    sT.textContent=s.getAttribute('data-t'); sD.textContent=s.getAttribute('data-d');
  });});
})();
</script>

<h2 id="faq"><span class="bx-num">13</span>FAQs on Discovered Currently Not Indexed</h2>
<div class="bx-rule"></div>

<div class="bx-faq" id="bxFaq">
  <button class="bx-q">Does "discovered - currently not indexed" mean my page will never rank?<span class="ic">+</span></button>
  <div class="bx-a"><p>No. It means Google hasn't crawled the page yet, not that it's been rejected. Google simply hasn't allocated crawl resources to it yet.</p></div>
  <button class="bx-q">How is this different from "crawled - currently not indexed"?<span class="ic">+</span></button>
  <div class="bx-a"><p>Discovered means Google hasn't fetched the page at all. Crawled means Google fetched it and made a deliberate decision not to index it, a quality-based judgment rather than a queue delay.</p></div>
  <button class="bx-q">Should I keep clicking Request Indexing?<span class="ic">+</span></button>
  <div class="bx-a"><p>No. Repeating the request without fixing the underlying cause, weak internal links, crawl budget, or thin content, rarely produces a different result.</p></div>
  <button class="bx-q">How many pages can I request indexing for per day?<span class="ic">+</span></button>
  <div class="bx-a"><p>There's no officially published limit, but practitioners typically see 10 to 15 manual requests allowed per day before hitting a quota wall.</p></div>
  <button class="bx-q">Is crawl budget a real thing or just an SEO myth?<span class="ic">+</span></button>
  <div class="bx-a"><p>Google has said there's no crawl budget in the exact way SEOs often describe it, but Google does have finite crawling capacity and prioritizes pages that demonstrate genuine value.</p></div>
</div>

<div class="bx-related-box">
<h3>Related Articles</h3>
<ul>
<li><a href="/url-inspection-tool-diagnose-indexing-problems/" target="_blank" rel="noopener">How to Use the URL Inspection Tool to Diagnose Indexing Problems</a></li>
<li><a href="/meta-robots-tags-explained-2/" target="_blank" rel="noopener">Meta Robots Tags Explained: Index, Noindex, Follow, Nofollow, and More</a></li>
<li><a href="/link-equity-explained/" target="_blank" rel="noopener">Link Equity Explained: How Authority Flows Through Your Website</a></li>
<li><a href="/how-to-test-mobile-friendliness-website/" target="_blank" rel="noopener">How to Test Mobile Friendliness of a Website</a></li>
</ul>
</div>

<div class="bx-learn">
<h3>What We Learn Today</h3>
<div class="bx-learn-grid">
<div class="bx-learn-card"><p>Discovered means Google hasn't crawled the page yet at all</p></div>
<div class="bx-learn-card"><p>It's a priority delay, not a quality rejection or penalty</p></div>
<div class="bx-learn-card"><p>Weak internal linking is one of the most common root causes</p></div>
<div class="bx-learn-card"><p>Crawled vs discovered need completely different diagnostic approaches</p></div>
<div class="bx-learn-card"><p>Fix the structural cause before repeating indexing requests</p></div>
<div class="bx-learn-card"><p>Clean sitemaps and strong internal links speed up crawl priority</p></div>
</div>
</div>

<!-- CTA -->
<section class="bx-cta">
  <h2 id="build-a-complete-technical-seo-foundation">Build a Complete Technical SEO Foundation</h2>
  <p>Fixing indexing issues pairs directly with the URL Inspection tool and meta robots directives. Explore both guides next.</p>
  <div class="bx-actions">
    <a class="bx-btn primary" href="/url-inspection-tool-diagnose-indexing-problems/" target="_blank" rel="noopener">URL Inspection Tool Guide</a>
    <a class="bx-btn ghost" href="/meta-robots-tags-explained-2/" target="_blank" rel="noopener">Meta Robots Tags Explained</a>
  </div>
</section>

</div><!-- /.bmc-flow -->

<script>
(function(){
  var root=document.currentScript.parentNode.querySelector('.bmc-flow')||document;
  var qs=root.querySelectorAll('#bxFaq .bx-q');
  qs.forEach(function(q){q.addEventListener('click',function(){
    var a=q.nextElementSibling, open=q.classList.contains('on');
    qs.forEach(function(x){x.classList.remove('on');x.nextElementSibling.classList.remove('on');});
    if(!open){q.classList.add('on');a.classList.add('on');}
  });});
})();
</script>
