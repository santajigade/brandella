---
title: "How to Detect Broken Links Using JavaScript"
slug: "how-to-detect-broken-links-javascript"
date: "2026-08-23T15:26:57"
updated: "2026-08-23T15:28:50"
author: "santajigade"
categories: ["development", "javascript"]
primaryCategory: "javascript"
description: "Detect broken links using JavaScript: real HEAD-request code for browser console, full page scanning, and Node.js sitemap checks with timeout handling."
focusKeyword: "detect broken links"
takeaways:
  - "Detecting broken links in JavaScript means looping through page links, sending a HEAD request to each, and flagging any 400+ status code."
  - "HEAD requests fetch only response headers, making bulk checks fast, and native Fetch works in modern browsers and Node.js 18+."
  - "Add a timeout with AbortController and fall back to a GET request when a server returns 405 or 403 for HEAD."
  - "Deduplicate links with a Set and filter out mailto: and anchor-only links before checking to avoid wasted requests."
  - "A Node.js script can check every URL in sitemap.xml for whole-site audits, while JavaScript-rendered SPAs need a headless browser like Playwright."
image: "/wp-content/uploads/2026/08/detect-broken-links.webp"
imageAlt: "detect broken links"
words: 1095
views: 75
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
.bmc-flow .bx-code pre{margin:0;font-family:'Courier New',monospace;font-size:14px;line-height:1.6;color:#c7e8b8;white-space:pre-wrap;word-break:break-word;}
.bmc-flow .bx-code-label{font-family:var(--bx-disp);color:var(--bx-steel-2);text-transform:uppercase;letter-spacing:1.2px;font-size:13px;margin-bottom:10px;font-weight:600;}
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
<span class="bx-meta-pill">Broken Links</span>
<span class="bx-meta-pill">JavaScript</span>
<span class="bx-meta-pill">2026</span>
</div>
<h2 id="detect-broken-links-using-javascript">Detect broken links using JavaScript</h2>
<p class="bx-lede">Detect broken links using JavaScript comes down to one core technique: looping through every link on a page, sending a HEAD request to each URL, and flagging anything that returns a 400+ status code. Broken links quietly hurt user experience and SEO, and most sites have more of them than owners realize.</p>

<p>The Fetch API makes this genuinely simple in modern browsers and Node.js 18+. HEAD requests fetch only the response headers, not the full page body, making bulk link checks fast and bandwidth-light.</p>

<p>Here's the working code for a browser console snippet, a full page scanner with timeout handling, and a Node.js script for checking an entire sitemap.</p>

<div class="bx-specs">
<div class="bx-spec"><div class="v">HEAD</div><div class="k">the fastest HTTP method for checking link status without downloading full content</div></div>
<div class="bx-spec"><div class="v">400+</div><div class="k">status code threshold typically used to flag a link as broken</div></div>
<div class="bx-spec"><div class="v">18+</div><div class="k">Node.js version required for native Fetch API support without extra libraries</div></div>
</div>
<h2 id="quick-snippet"><span class="bx-num">01</span>Quick DevTools Console Snippet</h2>
<div class="bx-rule"></div>
<p>Paste this directly into your browser's console while on any page to check every link instantly, then watch the Network tab for 404s or failed requests.</p>

<div class="bx-code">
<div class="bx-code-label">Console Snippet: Check All Links on Current Page</div>
<pre>document.querySelectorAll('a[href]:not([href=""])').forEach(anchor => {
  fetch(anchor.href, { method: 'HEAD' })
    .then(res => {
      if (res.status >= 400) {
        console.warn('Broken link:', anchor.href, 'Status:', res.status);
      }
    })
    .catch(err => {
      console.error('Failed to fetch:', anchor.href, err);
    });
});</pre>
</div>

<h2 id="full-scanner"><span class="bx-num">02</span>Full Page Scanner With Timeout and Fallback</h2>
<div class="bx-rule"></div>
<p>Some servers reject HEAD requests entirely or return inconsistent statuses. This version adds a timeout via AbortController and automatically falls back to a GET request when a server responds with 405 or 403.</p>

<div class="bx-code">
<div class="bx-code-label">Full Broken Link Checker (Browser or Node.js 18+)</div>
<pre>async function checkLink(url, timeout = 10000) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeout);

  try {
    let res = await fetch(url, {
      method: 'HEAD',
      signal: controller.signal,
      redirect: 'follow'
    });

    // Some servers reject HEAD, fall back to GET
    if (res.status === 405 || res.status === 403) {
      res = await fetch(url, {
        method: 'GET',
        signal: controller.signal,
        redirect: 'follow'
      });
    }

    clearTimeout(timer);
    return {
      url,
      status: res.status,
      ok: res.ok,
      redirected: res.redirected,
      finalUrl: res.url
    };
  } catch (err) {
    clearTimeout(timer);
    return {
      url,
      status: 0,
      ok: false,
      error: err.name === 'AbortError' ? 'timeout' : err.message
    };
  }
}

async function checkAllLinks() {
  const links = [...new Set(
    Array.from(document.querySelectorAll('a[href]'))
      .map(a => a.href)
      .filter(href => href.startsWith('http'))
  )];

  const results = await Promise.all(links.map(url => checkLink(url)));
  const broken = results.filter(r => !r.ok);

  console.table(broken);
  return broken;
}

checkAllLinks();</pre>
</div>
<h2 id="deduplication"><span class="bx-num">03</span>Deduplicating Links Before Checking</h2>
<div class="bx-rule"></div>
<p>Most pages contain repeated links, a link to the homepage often appears in the header, footer, and nav simultaneously. Checking each duplicate wastes requests. A native JavaScript Set removes duplicates automatically and lets you filter out mailto: and anchor-only links in the same pass.</p>

<div class="bx-code">
<div class="bx-code-label">Deduplicate and Filter Links Before Checking</div>
<pre>const allLinkHrefs = Array.from(document.querySelectorAll('a[href]')).map(a => a.href);

const validHrefs = [...new Set(allLinkHrefs)].filter(href =>
  href &&
  !href.startsWith('mailto:') &&
  !href.includes('#')
);

console.log(`Checking ${validHrefs.length} unique links...`);</pre>
</div>

<h2 id="node-sitemap"><span class="bx-num">04</span>Node.js Script for Checking a Full Sitemap</h2>
<div class="bx-rule"></div>
<p>For checking an entire site rather than a single page, fetch the sitemap.xml, extract every URL, then loop through and check each one. This runs well as a scheduled script or CI job.</p>

<div class="bx-code">
<div class="bx-code-label">Node.js: Check Every URL in a Sitemap</div>
<pre>import { parseStringPromise } from 'xml2js';

async function checkSitemap(sitemapUrl) {
  const response = await fetch(sitemapUrl);
  const xmlData = await response.text();
  const result = await parseStringPromise(xmlData);
  const urls = result.urlset.url.map(entry => entry.loc[0]);

  const broken = [];

  for (const url of urls) {
    try {
      const res = await fetch(url, { method: 'HEAD' });
      if (res.status >= 400) {
        broken.push({ url, status: res.status });
      }
    } catch (error) {
      broken.push({ url, status: 0, error: error.message });
    }
  }

  console.log(`Checked ${urls.length} URLs, found ${broken.length} broken.`);
  return broken;
}

checkSitemap('https://example.com/sitemap.xml');</pre>
</div>
<h2 id="table"><span class="bx-num">05</span>Approach Comparison</h2>
<div class="bx-rule"></div>
<p>A quick reference for choosing the right approach based on your situation.</p>

<div class="bx-table-wrap">
<table class="bx-table">
<thead>
<tr><th>Approach</th><th>Best For</th><th>Limitation</th></tr>
</thead>
<tbody>
<tr><td>Browser console snippet</td><td>Quick, one-off checks on a live page</td><td>Manual, doesn't scale across many pages</td></tr>
<tr><td>Full scanner with fallback</td><td>Single-page audits with retry logic</td><td>Still limited to one page at a time</td></tr>
<tr><td>Node.js sitemap script</td><td>Whole-site checks, CI/CD, scheduled jobs</td><td>Requires server-side execution environment</td></tr>
<tr><td>Headless browser (Playwright)</td><td>SPAs where links are JS-rendered after load</td><td>Heavier setup, slower per-page execution</td></tr>
</tbody>
</table>
</div>

<h2 id="checklist"><span class="bx-num">06</span>Practical Notes Before Running These Scripts</h2>
<div class="bx-rule"></div>
<p>A few things worth checking before running any of the above at scale.</p>

<div class="bx-checklist">
<div class="bx-check-item"><div class="bx-check-icon"></div><p><strong>Watch for CORS restrictions</strong> when checking cross-origin links directly from a browser console.</p></div>
<div class="bx-check-item"><div class="bx-check-icon"></div><p><strong>Always set a timeout</strong>, unresponsive servers can otherwise hang a batch check indefinitely.</p></div>
<div class="bx-check-item"><div class="bx-check-icon"></div><p><strong>Fall back to GET when HEAD is rejected</strong>, some servers return 403 or 405 for HEAD requests specifically.</p></div>
<div class="bx-check-item"><div class="bx-check-icon"></div><p><strong>Deduplicate links first</strong>, checking the same URL five times wastes requests and time.</p></div>
<div class="bx-check-item"><div class="bx-check-icon"></div><p><strong>For SPAs, use a headless browser</strong> instead of static HTML parsing, since JS-injected links won't appear otherwise.</p></div>
</div>

<h2 id="faq"><span class="bx-num">07</span>Common Questions</h2>
<div class="bx-rule"></div>
<div class="bx-faq" id="bxFaq">
<button class="bx-q">Why use a HEAD request instead of GET to check links?<span class="ic">+</span></button>
<div class="bx-a"><p>HEAD requests return only the response headers, not the full page body, making them faster and far less bandwidth-intensive for bulk link checking.</p></div>
<button class="bx-q">What if a server rejects HEAD requests?<span class="ic">+</span></button>
<div class="bx-a"><p>Some servers return 403 or 405 for HEAD requests specifically. The fix is falling back to a GET request only when that happens, rather than using GET for every check.</p></div>
<button class="bx-q">Can this detect links added by JavaScript on single-page apps?<span class="ic">+</span></button>
<div class="bx-a"><p>Not with static HTML parsing alone. For SPAs where navigation items are injected after page load, a headless browser tool like Playwright is needed to capture JS-rendered links.</p></div>
<button class="bx-q">Will checking links from the browser console hit CORS issues?<span class="ic">+</span></button>
<div class="bx-a"><p>It can, for cross-origin requests where the target server doesn't allow it. Server-side Node.js scripts avoid this limitation entirely since CORS is a browser-enforced restriction.</p></div>
<button class="bx-q">How do I check an entire website instead of one page?<span class="ic">+</span></button>
<div class="bx-a"><p>Fetch your sitemap.xml, parse out every URL listed, then loop through and check each one with a HEAD request, ideally as a scheduled Node.js script or CI job.</p></div>
</div>

<div class="bx-related-box">
<h3>Related Articles</h3>
<ul>
<li><a href="/what-is-canonical-tag/" target="_blank" rel="noopener">What Is a Canonical Tag?</a></li>
<li><a href="/canonical-tag-implementation-guide/" target="_blank" rel="noopener">Canonical Tag Implementation Guide</a></li>
<li><a href="/robots-txt-complete-guide/" target="_blank" rel="noopener">Robots.txt Complete Guide</a></li>
</ul>
</div>

<div class="bx-learn">
<h3>What We Learn Today</h3>
<div class="bx-learn-grid">
<div class="bx-learn-card"><p>HEAD requests check status without downloading full content</p></div>
<div class="bx-learn-card"><p>AbortController adds timeout protection to prevent hanging checks</p></div>
<div class="bx-learn-card"><p>Fall back to GET only when a server rejects HEAD specifically</p></div>
<div class="bx-learn-card"><p>Deduplicating links with a Set avoids wasted repeat requests</p></div>
<div class="bx-learn-card"><p>Sitemap-based checking scales to whole-site audits</p></div>
<div class="bx-learn-card"><p>SPAs need a headless browser to capture JS-rendered links</p></div>
</div>
</div>

<section class="bx-cta">
<h2 id="build-a-complete-technical-seo-toolkit">Build a Complete Technical SEO Toolkit</h2>
<p>Broken link detection pairs well with canonical tags and robots directives. Explore both guides next.</p>
<div class="bx-actions">
<a class="bx-btn primary" href="/canonical-tag-implementation-guide/" target="_blank" rel="noopener">Canonical Tag Implementation Guide</a>
<a class="bx-btn ghost" href="/robots-txt-complete-guide/" target="_blank" rel="noopener">Robots.txt Complete Guide</a>
</div>
</section>

</div>
<script>
(function(){var root=document.currentScript.parentNode.querySelector('.bmc-flow')||document;var qs=root.querySelectorAll('#bxFaq .bx-q');qs.forEach(function(q){q.addEventListener('click',function(){var a=q.nextElementSibling,open=q.classList.contains('on');qs.forEach(function(x){x.classList.remove('on');x.nextElementSibling.classList.remove('on');});if(!open){q.classList.add('on');a.classList.add('on');}});});})();
</script>
