---
title: "Meta Robots Tag: Noindex, Nofollow and Follow Explained"
slug: "meta-robots-tags-explained-2"
date: "2026-08-09T05:34:18"
updated: "2026-08-09T08:35:17"
author: "santajigade"
categories: ["seo", "technical-seo"]
primaryCategory: "technical-seo"
description: "How the meta robots tag works, when to use noindex, nofollow and follow, with code examples and common mistakes that block pages from Google."
focusKeyword: "meta robots tag"
takeaways:
  - "A meta robots tag in the page head tells search engines whether to index that one page and whether to follow its links."
  - "Without any tag, Google defaults to index, follow, so you only need the tag to restrict something."
  - "Noindex does not stop crawling, and since 2019 Google treats nofollow as a hint rather than a strict rule."
  - "Never block a URL in robots.txt and noindex it at the same time, because Google cannot see a noindex on a page it cannot crawl."
  - "Use the X-Robots-Tag HTTP header for PDFs and other non-HTML files."
image: "/wp-content/uploads/2026/08/Meta-Robots-Tags.webp"
imageAlt: "Meta Robots Tags"
words: 1737
views: 63
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
<span class="bx-meta-pill">Meta Robots Tags</span>
<span class="bx-meta-pill">Indexing</span>
<span class="bx-meta-pill">2026</span>
</div>

<p class="bx-lede">Meta robots tags control something more specific than most site owners realize: not whether Google can visit a page, but whether it can include that page in search results and whether it should follow the links sitting on it. Get the directive wrong and you can accidentally deindex a page that took months to rank.</p>

<p>The confusion usually starts with terminology. Robots.txt, meta robots tags, and X-Robots-Tag all sound like the same thing, but they control different layers of how search engines interact with a page, and mixing them up is one of the most common technical SEO mistakes.</p>

<p>These directives operate at the individual URL level, sitting inside a page's head section rather than applying sitewide. That precision is exactly what makes them useful, and exactly what makes a single misplaced tag dangerous.</p>

<p>This guide breaks down every meta robots directive worth knowing, how index, noindex, follow, and nofollow actually behave, and the mistakes that quietly cost sites their rankings.</p>

<div class="bx-specs">
<div class="bx-spec"><div class="v">index, follow</div><div class="k">the default behavior when no meta robots tag is present at all</div></div>
<div class="bx-spec"><div class="v">2019</div><div class="k">the year Google began treating nofollow as a hint, not a strict directive</div></div>
<div class="bx-spec"><div class="v">2 waves</div><div class="k">Googlebot processes meta robots in: raw HTML first, then the rendered DOM</div></div>
</div>
<h2 id="what-is-meta-robots"><span class="bx-num">01</span>What Meta Robots Tags Actually Do</h2>
<div class="bx-rule"></div>
<p><a href="https://devendergupta.netlify.app/blog/meta-robots-tags/" target="_blank" rel="noopener">Devender Gupta's technical breakdown</a> defines it precisely: a meta robots tag is an HTML snippet placed in a document's head that tells search engines whether they can include the page in their index and whether they should follow its links, operating at the individual URL level rather than sitewide.</p>

<p><a href="https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/meta/name/robots" target="_blank" rel="noopener">MDN's official reference</a> notes this isn't part of any formal web specification, it's a de-facto standard for communicating with search bots, crawlers, and similar user agents, cooperatively honored by Google, Bing, and other major engines.</p>

<h2 id="index-vs-noindex"><span class="bx-num">02</span>Index vs Noindex: What Each Directive Controls</h2>
<div class="bx-rule"></div>
<p><a href="https://olibro.com/meta-robots-tag-index-noindex-follow-nofollow/" target="_blank" rel="noopener">Olibro's guide to meta robots directives</a> puts it simply: index tells search engines to include the page in results, while noindex hides it from view entirely. Without any such tag present, <a href="https://www.digitalapplied.com/blog/robots-txt-meta-robots-complete-seo-reference" target="_blank" rel="noopener">Digital Applied's complete SEO reference</a> confirms Google defaults to index, follow automatically.</p>

<p>Noindex doesn't stop crawling on its own. Devender Gupta's breakdown, referenced above, explains Google continues visiting a noindexed page periodically to check whether the directive has changed, which is why removing thousands of pages via noindex takes real time to fully process.</p>

<div class="bx-note">
<span class="lbl">Noindex Eventually Becomes Noindex, Nofollow</span>
<p><a href="https://www.conductor.com/academy/meta-robots-tag/" target="_blank" rel="noopener">Conductor's 2026 meta robots guide</a> flags an important side effect: search engines significantly reduce re-crawling of a noindexed page over time, which functionally turns it into a noindex, nofollow situation, since links on a page that rarely gets crawled stop passing meaningful signal either.</p>
</div>
<h2 id="follow-vs-nofollow"><span class="bx-num">03</span>Follow vs Nofollow: What Changed in 2019</h2>
<div class="bx-rule"></div>
<p>Follow tells search engines to crawl and potentially index the pages a link points to. Nofollow tells them to skip that, historically preventing any link authority from passing through.</p>

<p>Devender Gupta's breakdown, referenced above, notes a shift worth knowing: since 2019, Google treats nofollow as a hint for crawling and indexing purposes rather than a strict directive. It usually still blocks PageRank transfer, but Google may still discover and follow the link if it finds the same URL referenced elsewhere.</p>

<h2 id="combinations"><span class="bx-num">04</span>Common Meta Robots Tag Combinations</h2>
<div class="bx-rule"></div>
<p>Index and follow behave independently, which means all four combinations are valid and each serves a distinct purpose. <a href="https://victorious.com/blog/noindex-meta-tag/" target="_blank" rel="noopener">Victorious' guide to noindex tags</a> offers a useful mental model: think of your site as connected rooms, where index or noindex controls whether a search engine can enter a room, and follow or nofollow controls whether it explores the doorways inside.</p>

<p>Olibro's guide, referenced above, ties each combination to real use cases: noindex, follow suits "thank you" pages you still want to pass discovery signal through, while index, nofollow fits pages you want visible in search but don't want passing authority onward, like user-generated content pages.</p>

<h2 id="additional-directives"><span class="bx-num">05</span>Additional Meta Robots Directives Worth Knowing</h2>
<div class="bx-rule"></div>
<p>Index, noindex, follow, and nofollow aren't the whole list. MDN's reference documents several more: noarchive prevents a cached version from appearing in results, nosnippet blocks any text snippet or video preview, and max-image-preview:large is essential for Google Discover eligibility specifically.</p>

<p><a href="https://searchroost.com/blog/meta-robots-tags-noindex-nofollow" target="_blank" rel="noopener">Search Roost's directive guide</a> adds unavailable_after, which schedules a page for automatic removal from search results at a specific date and time, useful for time-limited content like event pages or expiring promotions without needing a manual cleanup later.</p>
<h2 id="meta-robots-vs-robotstxt"><span class="bx-num">06</span>Meta Robots vs Robots.txt vs X-Robots-Tag</h2>
<div class="bx-rule"></div>
<p>This distinction causes more damage than any single directive mistake. <a href="https://irankly.com/en/blog/meta-robots-noindex-nofollow" target="_blank" rel="noopener">iRankly's guide</a> states it plainly: robots.txt controls crawling, meta robots controls indexing, and confusing the two is one of the most common points of failure in technical SEO setups.</p>

<p>Digital Applied's complete reference issues the critical warning directly: never combine disallow with noindex. If robots.txt blocks a URL, Googlebot cannot fetch the page and will never see the meta noindex tag inside it, so the URL can remain indexable indefinitely despite your intent to remove it.</p>

<p>X-Robots-Tag solves a different problem entirely. Google's own <a href="https://developers.google.com/search/docs/crawling-indexing/robots-meta-tag" target="_blank" rel="noopener">Search Central documentation on robots meta directives</a> confirms it carries the same values as meta robots but works as an HTTP header, making it the right choice for non-HTML files like PDFs and images where editing a head section isn't possible.</p>

<div class="bx-svgwrap">
<svg viewBox="0 0 700 240" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Diagram showing that robots.txt controls crawling access while meta robots tags control indexing decisions, and blocking a URL in robots.txt prevents Google from ever seeing a noindex tag on that page">
<rect x="20" y="30" width="200" height="60" rx="10" fill="#20272C"/>
<text x="120" y="55" text-anchor="middle" fill="#fff" font-family="Open Sans" font-size="13" font-weight="700">robots.txt</text>
<text x="120" y="73" text-anchor="middle" fill="#c7d9c0" font-family="Open Sans" font-size="11">Controls crawling</text>

<rect x="20" y="150" width="200" height="60" rx="10" fill="#f7faf5" stroke="#cdeabb"/>
<text x="120" y="175" text-anchor="middle" fill="#2b2b2b" font-family="Open Sans" font-size="13" font-weight="700">Meta Robots Tag</text>
<text x="120" y="193" text-anchor="middle" fill="#5a6570" font-family="Open Sans" font-size="11">Controls indexing</text>

<line x1="220" y1="60" x2="480" y2="60" stroke="#c95d5d" stroke-width="2" stroke-dasharray="5,5"/>
<text x="350" y="45" text-anchor="middle" fill="#a33" font-family="Open Sans" font-size="11" font-weight="700">If disallowed, page is never fetched</text>

<line x1="220" y1="180" x2="480" y2="180" stroke="#5DB92E" stroke-width="3"/>
<polygon points="480,174 494,180 480,186" fill="#5DB92E"/>

<rect x="500" y="30" width="180" height="60" rx="10" fill="#fdecec" stroke="#e6b3b3"/>
<text x="590" y="55" text-anchor="middle" fill="#a33" font-family="Open Sans" font-size="12" font-weight="700">Noindex Tag</text>
<text x="590" y="73" text-anchor="middle" fill="#a33" font-family="Open Sans" font-size="11" font-weight="600">Never seen by Google</text>

<rect x="500" y="150" width="180" height="60" rx="10" fill="#eef8e8" stroke="#cdeabb"/>
<text x="590" y="175" text-anchor="middle" fill="#3f9421" font-family="Open Sans" font-size="12" font-weight="700">Noindex Tag</text>
<text x="590" y="193" text-anchor="middle" fill="#3f9421" font-family="Open Sans" font-size="11" font-weight="600">Seen and honored</text>
</svg>
<p class="bx-svgcap">Allow crawling first, then apply noindex — never combine disallow with noindex on the same URL.</p>
</div>

<h2 id="video"><span class="bx-num">07</span>Watch: Noindex vs Disallow Explained by Google</h2>
<div class="bx-rule"></div>
<p>For a walkthrough of the exact mistake covered above, mixing a robots.txt disallow with a page-level noindex tag, this video breaks down troubleshooting the "Excluded by noindex tag" status directly inside Search Console.</p>

<div class="bx-video-wrap">
<div class="bx-video-frame">
<iframe src="https://www.youtube.com/embed/quY-u3odBtY" title="How to Fix Excluded by 'noindex' tag - Search Console Page Indexing" allowfullscreen></iframe>
</div>
<div class="bx-video-cap">"How to Fix Excluded by 'noindex' Tag - Search Console Page Indexing" — RankYa. Source: YouTube.</div>
</div>

<h2 id="combinations-table"><span class="bx-num">08</span>Meta Robots Directive Combinations at a Glance</h2>
<div class="bx-rule"></div>
<p><a href="https://usergrowth.io/academy/meta-robots-tag/" target="_blank" rel="noopener">User Growth's comprehensive guide</a> to robots meta tags and Victorious' room analogy both map onto the same practical set of use cases.</p>

<div class="bx-table-wrap">
<table class="bx-table">
<thead>
<tr><th>Directive</th><th>Effect</th><th>Typical Use Case</th></tr>
</thead>
<tbody>
<tr><td>index, follow</td><td>Default; page indexed, links passed</td><td>Standard content pages (no tag needed)</td></tr>
<tr><td>noindex, follow</td><td>Page hidden, links still discoverable</td><td>Thank-you pages, internal search results</td></tr>
<tr><td>index, nofollow</td><td>Page indexed, links don't pass authority</td><td>User-generated content, affiliate-heavy pages</td></tr>
<tr><td>noindex, nofollow</td><td>Page hidden, links not passed (same as "none")</td><td>Admin pages, staging sites, cart/checkout</td></tr>
</tbody>
</table>
</div>

<h2 id="code"><span class="bx-num">09</span>Meta Robots and X-Robots-Tag Code Examples</h2>
<div class="bx-rule"></div>
<p>Here are the exact tag formats for the most common scenarios, plus the server-side equivalents for non-HTML files.</p>

<div class="bx-code">
<div class="bx-code-label">Meta Robots Tag (in the HTML head)</div>
<pre>&lt;!-- Standard noindex, follow --&gt;
&lt;meta name="robots" content="noindex, follow"&gt;

&lt;!-- Fully hidden, no link equity passed --&gt;
&lt;meta name="robots" content="noindex, nofollow"&gt;

&lt;!-- Target Googlebot specifically --&gt;
&lt;meta name="googlebot" content="noindex"&gt;

&lt;!-- Schedule automatic removal --&gt;
&lt;meta name="robots" content="unavailable_after: 2026-12-31T23:59:59+00:00"&gt;</pre>
</div>

<div class="bx-code">
<div class="bx-code-label">X-Robots-Tag for Non-HTML Files (.htaccess)</div>
<pre># Apply noindex to all PDF files
&lt;FilesMatch "\.pdf$"&gt;
  Header set X-Robots-Tag "noindex, nofollow"
&lt;/FilesMatch&gt;

# Apply noindex to image file types sitewide
&lt;Files ~ "\.(png|jpe?g|gif)$"&gt;
  Header set X-Robots-Tag "noindex"
&lt;/Files&gt;</pre>
</div>

<h2 id="checklist"><span class="bx-num">10</span>Meta Robots Implementation Checklist</h2>
<div class="bx-rule"></div>
<p>A disciplined process prevents the accidental deindexing that meta robots mistakes are most known for.</p>

<div class="bx-checklist">
<div class="bx-check-item"><div class="bx-check-icon"></div><p><strong>Never combine disallow with noindex</strong> on the same URL; allow crawling first, then apply noindex.</p></div>
<div class="bx-check-item"><div class="bx-check-icon"></div><p><strong>Check for conflicting signals</strong>, a noindex tag alongside a self-referencing canonical sends mixed instructions.</p></div>
<div class="bx-check-item"><div class="bx-check-icon"></div><p><strong>Don't noindex paginated pages</strong>, Google handles pagination differently and won't treat it as duplicate content.</p></div>
<div class="bx-check-item"><div class="bx-check-icon"></div><p><strong>Exclude noindexed pages from your XML sitemap</strong>, since the sitemap signals which pages should be indexed.</p></div>
<div class="bx-check-item"><div class="bx-check-icon"></div><p><strong>Watch for JavaScript-injected tags</strong>, a directive added after hydration can delay or silently fail to take effect.</p></div>
</div>

<h2 id="stepper"><span class="bx-num">11</span>Priority Decision Workflow</h2>
<div class="bx-rule"></div>
<p>Five questions cover most meta robots decisions. Tap each one for guidance.</p>

<div class="bx-steps" id="bxSteps">
  <div class="dc-hint">Tap a factor &darr;</div>
  <div class="bx-track" role="group" aria-label="Meta robots tags priority decision workflow steps">
    <div class="bx-step on" data-t="Should It Appear in Search?" data-d="If yes, use index (or omit the tag entirely). If no, use noindex. This is the core question every page needs answered."><div class="no">1</div><div class="lb">Index?</div></div>
    <div class="bx-step" data-t="Should Links Pass Authority?" data-d="If the page's outbound links should count, use follow. If not, like on user-generated content, use nofollow."><div class="no">2</div><div class="lb">Follow?</div></div>
    <div class="bx-step" data-t="Is This HTML or a File?" data-d="For HTML pages, use a meta robots tag in the head. For PDFs, images, or other files, use X-Robots-Tag instead."><div class="no">3</div><div class="lb">Format</div></div>
    <div class="bx-step" data-t="Check Crawl Access First" data-d="Confirm robots.txt isn't blocking the page. A disallowed page will never let Google see a noindex tag."><div class="no">4</div><div class="lb">Crawlable?</div></div>
    <div class="bx-step" data-t="Verify With URL Inspection" data-d="After deploying, check Search Console's URL Inspection tool to confirm Google is reading the directive as intended."><div class="no">5</div><div class="lb">Verify</div></div>
  </div>
  <div class="bx-stepdetail" aria-live="polite">
    <p class="dt-t" id="bxStepT">Should It Appear in Search?</p>
    <p class="dt-d" id="bxStepD">If yes, use index (or omit the tag entirely). If no, use noindex. This is the core question every page needs answered.</p>
  </div>
</div>

<h2 id="score"><span class="bx-num">12</span>Which Directive Should You Use Score</h2>
<div class="bx-rule"></div>
<p>Answer a few questions about the page you're configuring to see the recommended meta robots directive.</p>

<div class="bx-calc">
<div class="bx-calc-header">
<h3>Which Meta Robots Directive Fits This Page</h3>
<p>Select the option that matches your page's purpose</p>
</div>
<div class="bx-calc-body">

<div class="bx-calc-factor">
<div class="bx-calc-factor-top"><label>Should this page appear in search results?</label><span>40 pts</span></div>
<select class="bx-calc-select" data-weight="40" onchange="bxCalc()">
<option value="0">No, keep it out of search entirely</option>
<option value="0.5">Unsure</option>
<option value="1">Yes, it should be discoverable</option>
</select>
</div>

<div class="bx-calc-factor">
<div class="bx-calc-factor-top"><label>Should its links pass authority?</label><span>35 pts</span></div>
<select class="bx-calc-select" data-weight="35" onchange="bxCalc()">
<option value="0">No, don't pass link equity</option>
<option value="0.5">Unsure</option>
<option value="1">Yes, links should count normally</option>
</select>
</div>

<div class="bx-calc-factor">
<div class="bx-calc-factor-top"><label>Is it sensitive or admin-only content?</label><span>25 pts</span></div>
<select class="bx-calc-select" data-weight="25" onchange="bxCalc()">
<option value="1">Yes, staging, admin, or checkout page</option>
<option value="0.5">Somewhat sensitive</option>
<option value="0">No, standard public content</option>
</select>
</div>

<div class="bx-calc-gauge-wrap">
<div class="bx-calc-gauge-track"><div class="bx-calc-gauge-fill" id="bxGaugeFill"><span id="bxGaugeScore">0%</span></div></div>
<div class="bx-calc-verdict" id="bxVerdict">Select an option for each factor to see the recommended directive.</div>
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
  if(pct >= 70){ verdict.innerText = "Use index, follow: standard public content, or simply omit the tag."; }
  else if(pct >= 40){ verdict.innerText = "Consider noindex, follow or index, nofollow depending on which signal matters more."; }
  else { verdict.innerText = "Use noindex, nofollow: this page should stay out of search entirely."; }
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

<h2 id="faq"><span class="bx-num">13</span>FAQs on Meta Robots Tags</h2>
<div class="bx-rule"></div>

<div class="bx-faq" id="bxFaq">
  <button class="bx-q">What's the default if I don't add a meta robots tag at all?<span class="ic">+</span></button>
  <div class="bx-a"><p>index, follow. Google indexes the page and passes link equity through its links by default, with no tag required.</p></div>
  <button class="bx-q">Does noindex stop Google from crawling a page?<span class="ic">+</span></button>
  <div class="bx-a"><p>No. Noindex only removes the page from search results. Google continues crawling it periodically to check whether the directive has changed.</p></div>
  <button class="bx-q">Can I combine robots.txt disallow with a noindex tag?<span class="ic">+</span></button>
  <div class="bx-a"><p>No, and this is one of the most common technical SEO mistakes. If robots.txt blocks the page, Google never fetches it and never sees the noindex tag inside.</p></div>
  <button class="bx-q">Is nofollow still a strict directive in 2026?<span class="ic">+</span></button>
  <div class="bx-a"><p>No. Since 2019, Google treats nofollow as a hint rather than an absolute rule, though it usually still prevents link equity from passing.</p></div>
  <button class="bx-q">When should I use X-Robots-Tag instead of a meta robots tag?<span class="ic">+</span></button>
  <div class="bx-a"><p>For non-HTML files like PDFs, images, or videos, where you can't add an HTML head tag. X-Robots-Tag applies the same directives via an HTTP header.</p></div>
</div>

<div class="bx-related-box">
<h3>Related Articles</h3>
<ul>
<li><a href="/url-inspection-tool-diagnose-indexing-problems/" target="_blank" rel="noopener">How to Use the URL Inspection Tool to Diagnose Indexing Problems</a></li>
<li><a href="/how-to-test-mobile-friendliness-website/" target="_blank" rel="noopener">How to Test Mobile Friendliness of a Website</a></li>
<li><a href="/webp-vs-avif-image-format-seo/" target="_blank" rel="noopener">WebP vs AVIF: Which Image Format Is Better for SEO?</a></li>
<li><a href="/what-is-off-page-seo-complete-beginners-guide/" target="_blank" rel="noopener">What Is Off-Page SEO? Complete Beginner's Guide</a></li>
</ul>
</div>

<div class="bx-learn">
<h3>What We Learn Today</h3>
<div class="bx-learn-grid">
<div class="bx-learn-card"><p>The default behavior without any tag is index, follow</p></div>
<div class="bx-learn-card"><p>Noindex hides a page but doesn't stop Google from crawling it</p></div>
<div class="bx-learn-card"><p>Nofollow has been a hint, not a strict rule, since 2019</p></div>
<div class="bx-learn-card"><p>Never combine robots.txt disallow with a noindex tag</p></div>
<div class="bx-learn-card"><p>X-Robots-Tag handles non-HTML files meta tags can't reach</p></div>
<div class="bx-learn-card"><p>Conflicting canonical and noindex signals cause unpredictable results</p></div>
</div>
</div>

<!-- CTA -->
<section class="bx-cta">
  <h2 id="build-a-complete-technical-seo-foundation">Build a Complete Technical SEO Foundation</h2>
  <p>Directives pair directly with indexing diagnostics. Explore our URL Inspection tool guide next to verify your directives are working.</p>
  <div class="bx-actions">
    <a class="bx-btn primary" href="/url-inspection-tool-diagnose-indexing-problems/" target="_blank" rel="noopener">Diagnose Indexing Problems</a>
    <a class="bx-btn ghost" href="/how-to-test-mobile-friendliness-website/" target="_blank" rel="noopener">Test Mobile Friendliness</a>
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
