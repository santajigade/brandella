---
title: "Meta Robots Tags Explained with HTML Code Examples"
slug: "meta-robots-tags-explained"
date: "2026-07-31T09:50:15"
updated: "2026-08-09T08:40:07"
author: "santajigade"
categories: ["seo", "technical-seo"]
primaryCategory: "seo"
description: "One misplaced meta robots tag has deindexed entire sites overnight. Learn every directive — noindex, nofollow, X-Robots-Tag with real HTML code."
focusKeyword: "meta robots"
image: "/wp-content/uploads/2026/07/meta-robots.webp"
imageAlt: "meta robots"
words: 1346
views: 113
format: "html"
---
<div class="bmr-wrap">
<style>
.bmr-wrap{font-family:'Segoe UI', Arial, sans-serif;font-size:17px;line-height:1.75;color:#2e2e2e;max-width:100%;}
.bmr-wrap h2{font-size:25px;color:#2b2b2b;margin:36px 0 16px;font-weight:800;border-left:5px solid #5DB92E;padding-left:14px;}
.bmr-wrap h3{font-size:19px;color:#2b2b2b;margin:18px 0 10px;font-weight:700;}
.bmr-wrap p{margin:0 0 14px;font-size:17px;}
.bmr-wrap a{color:#3f9421;font-weight:600;text-decoration:none;}
.bmr-wrap a:hover{color:#2f7418;text-decoration:none;}
.bmr-wrap ul,.bmr-wrap ol{margin:0 0 16px;padding-left:22px;}
.bmr-wrap li{margin-bottom:8px;font-size:17px;}

.bmr-lede{font-size:20px;color:#333;font-style:italic;margin:0 0 18px;line-height:1.6;border-left:3px solid #5DB92E;padding-left:16px;}

.bmr-meta-row{display:flex;flex-wrap:wrap;gap:10px;margin:0 0 24px;}
.bmr-meta-pill{background:#eef8e8;color:#3f9421;border:1px solid #cdeabb;border-radius:20px;padding:6px 16px;font-size:13px;font-weight:700;text-transform:uppercase;letter-spacing:.5px;}

/* Stat cards */
.bmr-stat-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin:20px 0 30px;}
.bmr-stat-card{background:#f7faf5;border:1px solid #e3ede0;border-radius:12px;padding:22px 16px;text-align:center;}
.bmr-stat-num{font-size:32px;font-weight:800;color:#5DB92E;margin-bottom:6px;}
.bmr-stat-card p{margin:0;font-size:17px;color:#4a4a4a;}
@media(max-width:820px){.bmr-stat-grid{grid-template-columns:1fr;}}

/* Code block */
.bmr-code-box{background:#1e1e1e;border-radius:12px;padding:20px 22px;margin:20px 0 10px;overflow-x:auto;}
.bmr-code-box pre{margin:0;font-family:'Consolas','Monaco',monospace;font-size:13.5px;line-height:1.65;color:#d4d4d4;white-space:pre;}
.bmr-code-box .k{color:#9cdcfe;}
.bmr-code-box .s{color:#ce9178;}
.bmr-code-box .c{color:#6a9955;}
.bmr-code-box .p{color:#dcdcaa;}
.bmr-code-caption{font-size:14px;color:#7a7a7a;margin:8px 0 26px;text-align:center;}

/* NEW: Directive matrix (2x2 grid) */
.bmr-matrix{display:grid;grid-template-columns:auto 1fr 1fr;gap:2px;margin:20px 0 30px;background:#e3ede0;border-radius:12px;overflow:hidden;}
.bmr-matrix-cell{background:#fff;padding:16px;text-align:center;}
.bmr-matrix-cell.head{background:#2b2b2b;color:#fff;font-weight:800;font-size:14px;}
.bmr-matrix-cell.label{background:#2b2b2b;color:#fff;font-weight:800;font-size:14px;display:flex;align-items:center;justify-content:center;}
.bmr-matrix-cell.good{background:#eef8e8;}
.bmr-matrix-cell.warn{background:#fff8ea;}
.bmr-matrix-cell.bad{background:#fdecec;}
.bmr-matrix-cell code{font-size:12px;font-family:'Consolas','Monaco',monospace;display:block;margin-bottom:6px;font-weight:700;}
.bmr-matrix-cell span{font-size:12px;color:#5a5a5a;}

/* Steps */
.bmr-steps{display:flex;flex-direction:column;gap:14px;margin:20px 0 30px;}
.bmr-step{display:flex;gap:16px;background:#fff;border:1px solid #e3ede0;border-radius:12px;padding:18px 20px;align-items:flex-start;}
.bmr-step-num{width:36px;height:36px;border-radius:50%;background:#5DB92E;color:#fff;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:17px;flex-shrink:0;}
.bmr-step h3{margin:0 0 6px;font-size:17px;}
.bmr-step p{margin:0;font-size:17px;color:#4a4a4a;}

/* Tabs */
.bmr-tabs{margin:20px 0 30px;}
.bmr-tab-buttons{display:flex;flex-wrap:wrap;gap:8px;border-bottom:2px solid #e3ede0;}
.bmr-tab-btn{background:#f2f5f0;border:none;border-radius:8px 8px 0 0;padding:12px 20px;font-size:16px;font-weight:700;color:#4a4a4a;cursor:pointer;font-family:'Segoe UI',Arial,sans-serif;}
.bmr-tab-btn.active{background:#5DB92E;color:#fff;}
.bmr-tab-panel{display:none;border:1px solid #e3ede0;border-top:none;border-radius:0 0 10px 10px;padding:20px;background:#fff;}
.bmr-tab-panel.active{display:block;}
.bmr-tab-panel p{margin:0 0 10px;}
.bmr-tab-panel p:last-child{margin-bottom:0;}

/* Table */
.bmr-table-wrap{overflow-x:auto;margin:20px 0 30px;}
.bmr-table{width:100%;border-collapse:collapse;font-size:16px;}
.bmr-table th{background:#2b2b2b;color:#fff;padding:12px 14px;text-align:left;font-weight:700;}
.bmr-table td{padding:12px 14px;border-bottom:1px solid #e3ede0;}
.bmr-table tr:nth-child(even) td{background:#f7faf5;}
.bmr-table code{font-family:'Consolas','Monaco',monospace;font-size:13px;background:#f2f5f0;padding:2px 6px;border-radius:4px;}

/* Interactive builder */
.bmr-calc{border-radius:16px;overflow:hidden;border:1px solid #e3ede0;margin:20px 0 32px;}
.bmr-calc-header{background:#2b2b2b;color:#fff;padding:18px 22px;}
.bmr-calc-header h3{margin:0 0 4px;font-size:19px;color:#fff;}
.bmr-calc-header p{margin:0;font-size:14px;color:#c7d9c0;}
.bmr-calc-body{padding:22px;background:#fff;}
.bmr-calc-row{display:flex;gap:14px;align-items:center;padding:10px 0;border-bottom:1px solid #f0f2f0;flex-wrap:wrap;}
.bmr-calc-row:last-of-type{border-bottom:none;}
.bmr-calc-row label{font-size:15px;font-weight:700;color:#2b2b2b;width:200px;flex-shrink:0;}
.bmr-calc-row select{flex:1;min-width:150px;padding:8px 10px;border-radius:8px;border:1px solid #e3ede0;font-size:14px;color:#3a3a3a;font-family:'Segoe UI',Arial,sans-serif;background:#f7faf5;}
.bmr-calc-check{display:flex;align-items:center;gap:8px;}
.bmr-calc-check input{width:16px;height:16px;accent-color:#5DB92E;}
.bmr-calc-output{margin-top:18px;background:#1e1e1e;border-radius:10px;padding:16px;font-family:'Consolas','Monaco',monospace;font-size:13px;color:#d4d4d4;word-break:break-word;}

/* FAQ */
.bmr-faq-item{margin-bottom:14px;}
.bmr-faq-q{background:#f2f5f0;border-radius:8px 8px 0 0;padding:14px 18px;font-weight:700;color:#2b2b2b;font-size:17px;}
.bmr-faq-a{background:#fff;border:1px solid #eef1ec;border-top:none;border-radius:0 0 8px 8px;padding:16px 18px;font-size:17px;color:#4a4a4a;}

/* Related */
.bmr-related-box{background:#f7faf5;border:1px solid #e3ede0;border-radius:12px;padding:22px;margin:20px 0 30px;}
.bmr-related-box h3{margin:0 0 12px;color:#2b2b2b;}
.bmr-related-box ul{margin:0;padding-left:20px;}
.bmr-related-box li{margin-bottom:10px;}
.bmr-related-box a{font-weight:600 !important;}

/* What we learn today - terminal log style, matches sibling schema article */
.bmr-learn{margin:26px 0 20px;background:#1e1e1e;border-radius:14px;padding:20px 22px;}
.bmr-learn h3{font-size:18px;color:#fff;margin:0 0 14px;font-family:'Consolas','Monaco',monospace;}
.bmr-learn-line{display:flex;gap:10px;padding:6px 0;font-family:'Consolas','Monaco',monospace;font-size:14px;}
.bmr-learn-line .ok{color:#5DB92E;}
.bmr-learn-line p{margin:0;color:#d4d4d4;}
</style>

<div class="bmr-meta-row">
<span class="bmr-meta-pill">Technical SEO</span>
<span class="bmr-meta-pill">Meta Robots Tag</span>
<span class="bmr-meta-pill">Noindex</span>
<span class="bmr-meta-pill">Crawling</span>
</div>

<p class="bmr-lede">One misplaced meta robots tag has deindexed entire websites overnight. It is one line of HTML, and it is also one of the easiest ways to accidentally tell Google to forget your site exists. Here is exactly how the tag works, every directive it supports, and the real code for each one.</p>

<p>A meta robots tag is an HTML element placed in a page's head section that tells search engine crawlers whether to index the page and whether to follow its links.</p>

<p>Unlike robots.txt, which blocks crawling entirely, the meta robots tag lets a page be crawled but controls what happens after.</p>

<p>We covered a closely related file in our <a href="/what-is-xml-sitemap-ai-search-era/" target="_blank" rel="noopener">XML sitemap guide</a>. Never include a page carrying a meta robots noindex tag in your sitemap, since the two signals directly contradict each other.</p>

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


<div class="bmr-stat-grid">
<div class="bmr-stat-card"><div class="bmr-stat-num">index, follow</div><p>is the default behavior Google assumes when no meta robots tag is present at all</p></div>
<div class="bmr-stat-card"><div class="bmr-stat-num">2019</div><p>the year Google began treating nofollow as a hint, not a strict directive</p></div>
<div class="bmr-stat-card"><div class="bmr-stat-num">1</div><p>rule above all others: Googlebot must crawl a page to ever see its meta robots tag</p></div>
</div>

<h2 id="basic-meta-robots-tag-syntax">Basic Meta Robots Tag Syntax</h2>
<p>Every meta robots tag follows the same structure, placed inside the page's head element.</p>

<div class="bmr-code-box">
<pre>&lt;head&gt;
  &lt;meta name=<span class="s">"robots"</span> content=<span class="s">"noindex, follow"</span> /&gt;
&lt;/head&gt;</pre>
</div>
<p class="bmr-code-caption">The basic meta robots tag structure, placed in the head section of any page</p>

<h2 id="the-four-core-directive-combinations">The Four Core Directive Combinations</h2>
<p>These four combinations cover the overwhelming majority of real-world use cases.</p>

<div class="bmr-matrix">
<div class="bmr-matrix-cell head"></div>
<div class="bmr-matrix-cell head">Follow</div>
<div class="bmr-matrix-cell head">Nofollow</div>

<div class="bmr-matrix-cell label">Index</div>
<div class="bmr-matrix-cell good"><code>index, follow</code><span>Default. No tag needed.</span></div>
<div class="bmr-matrix-cell warn"><code>index, nofollow</code><span>Show in results, don't pass link equity.</span></div>

<div class="bmr-matrix-cell label">Noindex</div>
<div class="bmr-matrix-cell warn"><code>noindex, follow</code><span>Hide page, still discover its links.</span></div>
<div class="bmr-matrix-cell bad"><code>noindex, nofollow</code><span>Fully hidden. No links passed at all.</span></div>
</div>

<h2 id="noindex-follow-thank-you-and-confirmation-pages">Noindex, Follow: Thank-You and Confirmation Pages</h2>
<div class="bmr-code-box">
<pre>&lt;meta name=<span class="s">"robots"</span> content=<span class="s">"noindex, follow"</span> /&gt;</pre>
</div>
<p class="bmr-code-caption">Keeps a page out of search results while still letting Google discover linked pages</p>

<h2 id="noindex-nofollow-admin-and-staging-pages">Noindex, Nofollow: Admin and Staging Pages</h2>
<div class="bmr-code-box">
<pre>&lt;meta name=<span class="s">"robots"</span> content=<span class="s">"noindex, nofollow"</span> /&gt;</pre>
</div>
<p class="bmr-code-caption">Fully hides a page from indexing and prevents any link equity from passing through it</p>

<h2 id="targeting-a-specific-crawler">Targeting a Specific Crawler</h2>
<p>According to <a href="https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/meta/name/robots" target="_blank" rel="noopener">MDN's official meta robots documentation</a>, replacing the name attribute lets a directive apply to one specific bot rather than every crawler.</p>

<div class="bmr-code-box">
<pre>&lt;meta name=<span class="s">"googlebot"</span> content=<span class="s">"noindex"</span> /&gt;
&lt;meta name=<span class="s">"bingbot"</span> content=<span class="s">"noindex"</span> /&gt;</pre>
</div>
<p class="bmr-code-caption">Applying noindex only to Google or Bing, leaving other crawlers unaffected</p>

<h2 id="additional-directives-noarchive-nosnippet-and-max-snippet">Additional Directives: Noarchive, Nosnippet, and Max-Snippet</h2>
<div class="bmr-table-wrap">
<table class="bmr-table">
<thead>
<tr><th>Directive</th><th>What It Does</th></tr>
</thead>
<tbody>
<tr><td><code>noarchive</code></td><td>Prevents Google from showing a cached version of the page</td></tr>
<tr><td><code>nosnippet</code></td><td>Blocks any text snippet or video preview in results</td></tr>
<tr><td><code>max-snippet:50</code></td><td>Limits the text snippet shown to 50 characters</td></tr>
<tr><td><code>max-image-preview:large</code></td><td>Controls the maximum size of an image preview shown</td></tr>
<tr><td><code>unavailable_after</code></td><td>Automatically removes a page from results after a set date</td></tr>
</tbody>
</table>
</div>

<div class="bmr-code-box">
<pre>&lt;meta name=<span class="s">"robots"</span> content=<span class="s">"noarchive, max-snippet:50"</span> /&gt;
&lt;meta name=<span class="s">"robots"</span> content=<span class="s">"unavailable_after: 2026-12-31T23:59:59+00:00"</span> /&gt;</pre>
</div>
<p class="bmr-code-caption">Combining multiple directives in one tag, and setting an automatic expiration date</p>

<h2 id="x-robots-tag-controlling-non-html-files">X-Robots-Tag: Controlling Non-HTML Files</h2>
<p>According to <a href="https://developers.google.com/search/docs/crawling-indexing/robots-meta-tag" target="_blank" rel="noopener">Google Search Central's official robots meta tag documentation</a>, the X-Robots-Tag HTTP header carries the same directives but applies to files where an HTML head tag is not possible, like PDFs or images.</p>

<div class="bmr-code-box">
<pre><span class="c"># Apache .htaccess example</span>
&lt;FilesMatch <span class="s">"\.pdf$"</span>&gt;
  Header set X-Robots-Tag <span class="s">"noindex, nofollow"</span>
&lt;/FilesMatch&gt;

<span class="c"># NGINX example</span>
location ~* \.pdf$ {
  add_header X-Robots-Tag <span class="s">"noindex"</span>;
}</pre>
</div>
<p class="bmr-code-caption">Applying noindex to every PDF file on a site through server configuration, not HTML</p>

<h2 id="the-one-mistake-that-breaks-everything">The One Mistake That Breaks Everything</h2>
<p>This single error causes more noindex failures than any other mistake combined. Tap through both scenarios.</p>

<div class="bmr-tabs">
<div class="bmr-tab-buttons">
<button class="bmr-tab-btn active" onclick="bmrTab(event,'bmr-wrong')">The Broken Setup</button>
<button class="bmr-tab-btn" onclick="bmrTab(event,'bmr-right')">The Correct Setup</button>
</div>
<div id="bmr-wrong" class="bmr-tab-panel active">
<p>According to <a href="https://www.digitalapplied.com/blog/robots-txt-meta-robots-complete-seo-reference" target="_blank" rel="noopener">DigitalApplied's complete SEO reference</a>, blocking a URL in robots.txt while also adding a meta robots noindex tag on that same page fails silently.</p>

<p>Googlebot cannot fetch the page, so it never sees the noindex directive at all, and the URL can still appear indexed with no description.</p>
</div>
<div id="bmr-right" class="bmr-tab-panel">
<p>Allow crawling in robots.txt, then apply the noindex meta tag on the page itself. This lets Googlebot actually fetch the page, read the directive, and remove it from the index correctly.</p>
</div>
</div>
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

<h2 id="meta-robots-directive-builder">Meta Robots Directive Builder</h2>
<p>Select your options below to generate the exact meta robots tag for your situation.</p>

<div class="bmr-calc">
<div class="bmr-calc-header">
<h3>Meta Robots Directive Builder</h3>
<p>Builds a copy-paste ready meta tag based on your selections</p>
</div>
<div class="bmr-calc-body">

<div class="bmr-calc-row">
<label>Indexing</label>
<select id="bmrIndex" onchange="bmrBuild()">
<option value="index">index</option>
<option value="noindex">noindex</option>
</select>
</div>
<div class="bmr-calc-row">
<label>Link Following</label>
<select id="bmrFollow" onchange="bmrBuild()">
<option value="follow">follow</option>
<option value="nofollow">nofollow</option>
</select>
</div>
<div class="bmr-calc-row">
<label class="bmr-calc-check"><input type="checkbox" id="bmrNoarchive" onchange="bmrBuild()"> Add noarchive</label>
</div>
<div class="bmr-calc-row">
<label class="bmr-calc-check"><input type="checkbox" id="bmrNosnippet" onchange="bmrBuild()"> Add nosnippet</label>
</div>

<div class="bmr-calc-output" id="bmrOutput">&lt;meta name="robots" content="index, follow" /&gt;</div>

</div>
</div>

<script>
function bmrTab(evt, id){
  var panels = document.querySelectorAll('.bmr-tab-panel');
  var btns = document.querySelectorAll('.bmr-tab-btn');
  panels.forEach(function(p){p.classList.remove('active');});
  btns.forEach(function(b){b.classList.remove('active');});
  document.getElementById(id).classList.add('active');
  evt.currentTarget.classList.add('active');
}
function bmrBuild(){
  var idx = document.getElementById('bmrIndex').value;
  var fol = document.getElementById('bmrFollow').value;
  var directives = [idx, fol];
  if(document.getElementById('bmrNoarchive').checked){ directives.push('noarchive'); }
  if(document.getElementById('bmrNosnippet').checked){ directives.push('nosnippet'); }
  var output = '<meta name="robots" content="' + directives.join(', ') + '" />';
  document.getElementById('bmrOutput').innerText = output;
}
</script>

<h2 id="common-meta-robots-mistakes">Common Meta Robots Mistakes</h2>
<div class="bmr-steps">
<div class="bmr-step">
<div class="bmr-step-num">1</div>
<div>
<h3>Blocking Crawling and Adding Noindex Together</h3>
<p>As covered above, this is the single most common failure. The noindex tag never gets seen if robots.txt already blocks the page.</p>
</div>
</div>
<div class="bmr-step">
<div class="bmr-step-num">2</div>
<div>
<h3>Injecting the Tag Only Through JavaScript</h3>
<p>According to <a href="https://devendergupta.netlify.app/blog/meta-robots-tags/" target="_blank" rel="noopener">Devender Gupta's guide to meta robots tags</a>, Googlebot processes the raw HTML first, then the rendered DOM after JavaScript executes, creating a delay before a JS-injected directive takes effect.</p>
</div>
</div>
<div class="bmr-step">
<div class="bmr-step-num">3</div>
<div>
<h3>Conflicting Signals Across Plugins and Templates</h3>
<p>According to <a href="https://usergrowth.io/academy/meta-robots-tag/" target="_blank" rel="noopener">User Growth's comprehensive guide to robots meta tags</a>, if one plugin outputs index and a hardcoded tag says noindex, Google follows the most restrictive instruction, which is noindex, but the conflict itself signals a messier setup worth cleaning up.</p>
</div>
</div>
</div>
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

<h2 id="meta-robots-tag-placement-rules-worth-remembering">Meta Robots Tag Placement Rules Worth Remembering</h2>
<p>According to <a href="https://www.conductor.com/academy/meta-robots-tag/" target="_blank" rel="noopener">Conductor's meta robots tag guide</a>, the tag should be placed once per page, inside the head section, and never referenced from a page that also carries an hreflang tag pointing to it, since hreflang signals a page should be indexed.</p>

<p>According to <a href="https://irankly.com/en/blog/meta-robots-noindex-nofollow" target="_blank" rel="noopener">iRankly's guide to meta robots directives</a>, avoiding noindex on paginated pages is another common recommendation, since search engines generally understand pagination well enough not to treat it as duplicate content requiring exclusion.</p>

<h2 id="meta-robots-tag-behavior-over-time">Meta Robots Tag Behavior Over Time</h2>
<p>According to <a href="https://searchroost.com/blog/meta-robots-tags-noindex-nofollow" target="_blank" rel="noopener">Search Roost's guide to meta robots directives</a>, Google continues crawling noindex pages periodically to check whether the directive has changed, rather than abandoning them permanently after the first noindex is detected.</p>

<p>Over an extended period, a persistently noindexed page's crawl frequency drops, and its outbound links effectively behave as nofollow in practice, even without an explicit nofollow directive ever being added.</p>

<h2 id="faqs-on-meta-robots-tags">FAQs on Meta Robots Tags</h2>

<div class="bmr-faq-item">
<div class="bmr-faq-q">What is the difference between the meta robots tag and robots.txt?</div>
<div class="bmr-faq-a">Robots.txt blocks crawling before a page is ever fetched. The meta robots tag lives inside the page itself, so a crawler must be able to fetch the page for the tag to have any effect at all.</div>
</div>
<div class="bmr-faq-item">
<div class="bmr-faq-q">What happens if I combine robots.txt disallow with a noindex meta tag?</div>
<div class="bmr-faq-a">It fails. Since the page is blocked from crawling, Googlebot never sees the noindex directive, and the URL can remain indexed without a description rather than being removed.</div>
</div>
<div class="bmr-faq-item">
<div class="bmr-faq-q">Is nofollow still a strict directive?</div>
<div class="bmr-faq-a">No. Since 2019, Google treats nofollow as a hint for crawling and indexing decisions rather than an absolute rule it always obeys.</div>
</div>
<div class="bmr-faq-item">
<div class="bmr-faq-q">What should I use for pages I cannot add an HTML meta tag to?</div>
<div class="bmr-faq-a">Use the X-Robots-Tag HTTP header instead, applied server-side through .htaccess or NGINX configuration, particularly for PDFs, images, and other non-HTML files.</div>
</div>
<div class="bmr-faq-item">
<div class="bmr-faq-q">What is the default behavior if no meta robots tag exists?</div>
<div class="bmr-faq-a">Index, follow. Google assumes a page can be indexed and its links can be followed unless a meta robots tag explicitly says otherwise.</div>
</div>
<div class="bmr-faq-item">
<div class="bmr-faq-q">How long does it take for a noindex tag to actually remove a page?</div>
<div class="bmr-faq-a">It varies, often hours to days, since Google must first crawl the page, process the directive, and then pass that signal to the indexer before the URL disappears from search results.</div>
</div>

<div class="bmr-related-box">
<h3>Related Articles</h3>
<ul>
<li><a href="/what-is-canonical-tag/" target="_blank" rel="noopener">What Is Canonicalization? Fixing Duplicate Content Before It Costs You Rankings</a></li>
<li><a href="/crawl-budget-explained/" target="_blank" rel="noopener">Crawl Budget Explained: Why Google Might Be Ignoring Half Your Site</a></li>
<li><a href="/what-is-xml-sitemap-ai-search-era/" target="_blank" rel="noopener">What Is an XML Sitemap, and Does It Still Matter in the AI Search Era?</a></li>
<li><a href="/how-to-add-schema-markup-json-ld/" target="_blank" rel="noopener">How to Add Schema Markup to Any Website (JSON-LD Examples)</a></li>
</ul>
</div>

<div class="bmr-learn">
<h3>&gt; what_we_learn_today.log</h3>
<div class="bmr-learn-line"><span class="ok">[OK]</span><p>Meta robots tags require crawling first; robots.txt blocks crawling entirely</p></div>
<div class="bmr-learn-line"><span class="ok">[OK]</span><p>Default behavior with no tag present is always index, follow</p></div>
<div class="bmr-learn-line"><span class="ok">[OK]</span><p>Never combine robots.txt disallow with a noindex tag on the same page</p></div>
<div class="bmr-learn-line"><span class="ok">[OK]</span><p>X-Robots-Tag handles PDFs, images, and other non-HTML files</p></div>
<div class="bmr-learn-line"><span class="ok">[OK]</span><p>Nofollow has been a hint, not a strict rule, since 2019</p></div>
<div class="bmr-learn-line"><span class="ok">[OK]</span><p>The most restrictive directive always wins when signals conflict</p></div>
</div>

</div>
