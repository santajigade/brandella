---
title: "What Is Speed Index? Understanding One of Google's Key Performance Metrics"
slug: "what-is-speed-index-google-performance"
date: "2026-07-31T09:45:44"
updated: "2026-08-09T08:40:08"
author: "santajigade"
categories: ["core-web-vitals", "seo"]
primaryCategory: "seo"
description: "Speed Index measures how quickly a page fills in visually, not a single moment like FCP. Learn the formula, thresholds, and what actually improves it."
focusKeyword: "Speed Index"
takeaways:
  - "Speed Index measures how quickly above-the-fold content becomes visually complete, calculated from video frames captured during the whole load."
  - "Google treats 3.4 seconds or less as good on mobile, 3.4-5.8s as needing work and above 5.8s as poor."
  - "Speed Index carries 10% weight in the Lighthouse performance score and is lab only, never part of CrUX field data."
  - "Pages that render meaningful content steadily score better than pages that stay blank and show everything at once, even with the same total load time."
  - "Render-blocking CSS and JavaScript, heavy above-the-fold images and web fonts that block text rendering are common causes of a poor score."
image: "/wp-content/uploads/2026/07/Speed-Index.webp"
imageAlt: "Speed Index"
words: 1294
views: 58
format: "html"
---
<div class="bspx-wrap">
<style>
.bspx-wrap{font-family:'Segoe UI', Arial, sans-serif;font-size:17px;line-height:1.75;color:#2e2e2e;max-width:100%;}
.bspx-wrap h2{font-size:25px;color:#2b2b2b;margin:36px 0 16px;font-weight:800;border-left:5px solid #5DB92E;padding-left:14px;}
.bspx-wrap h3{font-size:19px;color:#2b2b2b;margin:18px 0 10px;font-weight:700;}
.bspx-wrap p{margin:0 0 14px;font-size:17px;}
.bspx-wrap a{color:#3f9421;font-weight:600;text-decoration:none;}
.bspx-wrap a:hover{color:#2f7418;text-decoration:none;}
.bspx-wrap ul,.bspx-wrap ol{margin:0 0 16px;padding-left:22px;}
.bspx-wrap li{margin-bottom:8px;font-size:17px;}

.bspx-lede{font-size:20px;color:#333;font-style:italic;margin:0 0 18px;line-height:1.6;border-left:3px solid #5DB92E;padding-left:16px;}

.bspx-meta-row{display:flex;flex-wrap:wrap;gap:10px;margin:0 0 24px;}
.bspx-meta-pill{background:#eef8e8;color:#3f9421;border:1px solid #cdeabb;border-radius:20px;padding:6px 16px;font-size:13px;font-weight:700;text-transform:uppercase;letter-spacing:.5px;}

/* Stat cards */
.bspx-stat-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin:20px 0 30px;}
.bspx-stat-card{background:#f7faf5;border:1px solid #e3ede0;border-radius:12px;padding:22px 16px;text-align:center;}
.bspx-stat-num{font-size:32px;font-weight:800;color:#5DB92E;margin-bottom:6px;}
.bspx-stat-card p{margin:0;font-size:17px;color:#4a4a4a;}
@media(max-width:820px){.bspx-stat-grid{grid-template-columns:1fr;}}

/* NEW: Filmstrip visual */
.bspx-filmstrip{margin:20px 0 30px;background:#1e1e1e;border-radius:14px;padding:20px;overflow-x:auto;}
.bspx-film-row{display:flex;gap:6px;}
.bspx-frame{flex-shrink:0;width:90px;height:110px;background:#fff;border-radius:4px;position:relative;overflow:hidden;}
.bspx-frame-fill{position:absolute;bottom:0;left:0;right:0;background:#5DB92E;}
.bspx-frame-label{position:absolute;bottom:4px;left:0;right:0;text-align:center;font-size:10px;color:#2b2b2b;font-weight:800;background:rgba(255,255,255,0.85);}
.bspx-frame-time{text-align:center;font-size:11px;color:#8a8a8a;margin-top:6px;}

/* Threshold meter */
.bspx-threshold{display:flex;border-radius:10px;overflow:hidden;margin:20px 0 30px;height:50px;}
.bspx-th-seg{display:flex;align-items:center;justify-content:center;color:#fff;font-weight:800;font-size:13px;flex-direction:column;line-height:1.3;}
.bspx-th-good{background:#5DB92E;width:45%;}
.bspx-th-ok{background:#e2a52c;width:25%;}
.bspx-th-poor{background:#c95d5d;width:30%;}

/* Tabs */
.bspx-tabs{margin:20px 0 30px;}
.bspx-tab-buttons{display:flex;flex-wrap:wrap;gap:8px;border-bottom:2px solid #e3ede0;}
.bspx-tab-btn{background:#f2f5f0;border:none;border-radius:8px 8px 0 0;padding:12px 20px;font-size:17px;font-weight:700;color:#4a4a4a;cursor:pointer;font-family:'Segoe UI',Arial,sans-serif;}
.bspx-tab-btn.active{background:#5DB92E;color:#fff;}
.bspx-tab-panel{display:none;border:1px solid #e3ede0;border-top:none;border-radius:0 0 10px 10px;padding:20px;background:#fff;}
.bspx-tab-panel.active{display:block;}
.bspx-tab-panel p{margin:0 0 10px;}
.bspx-tab-panel p:last-child{margin-bottom:0;}

/* Table */
.bspx-table-wrap{overflow-x:auto;margin:20px 0 30px;}
.bspx-table{width:100%;border-collapse:collapse;font-size:17px;}
.bspx-table th{background:#2b2b2b;color:#fff;padding:13px 16px;text-align:left;font-weight:700;}
.bspx-table td{padding:13px 16px;border-bottom:1px solid #e3ede0;}
.bspx-table tr:nth-child(even) td{background:#f7faf5;}

/* Interactive calculator */
.bspx-calc{border-radius:16px;overflow:hidden;border:1px solid #e3ede0;margin:20px 0 32px;}
.bspx-calc-header{background:#2b2b2b;color:#fff;padding:18px 22px;}
.bspx-calc-header h3{margin:0 0 4px;font-size:19px;color:#fff;}
.bspx-calc-header p{margin:0;font-size:14px;color:#c7d9c0;}
.bspx-calc-body{padding:22px;background:#fff;}
.bspx-calc-row{display:flex;gap:14px;align-items:center;padding:10px 0;border-bottom:1px solid #f0f2f0;flex-wrap:wrap;}
.bspx-calc-row:last-of-type{border-bottom:none;}
.bspx-calc-row label{font-size:15px;font-weight:700;color:#2b2b2b;width:230px;flex-shrink:0;}
.bspx-calc-row input{flex:1;min-width:100px;padding:8px 10px;border-radius:8px;border:1px solid #e3ede0;font-size:14px;color:#3a3a3a;font-family:'Segoe UI',Arial,sans-serif;background:#f7faf5;}
.bspx-calc-btn{background:#5DB92E;color:#fff;border:none;padding:10px 20px;border-radius:8px;font-weight:700;font-size:15px;cursor:pointer;font-family:'Segoe UI',Arial,sans-serif;margin-top:8px;}
.bspx-calc-result{margin-top:18px;background:#f7faf5;border:1px solid #e3ede0;border-radius:10px;padding:18px;}
.bspx-calc-result-num{font-size:26px;font-weight:800;color:#3f9421;margin-bottom:4px;text-align:center;}
.bspx-calc-result p{margin:0;font-size:14px;color:#4a4a4a;text-align:center;}

/* FAQ */
.bspx-faq-item{margin-bottom:14px;}
.bspx-faq-q{background:#f2f5f0;border-radius:8px 8px 0 0;padding:14px 18px;font-weight:700;color:#2b2b2b;font-size:17px;}
.bspx-faq-a{background:#fff;border:1px solid #eef1ec;border-top:none;border-radius:0 0 8px 8px;padding:16px 18px;font-size:17px;color:#4a4a4a;}

/* Related */
.bspx-related-box{background:#f7faf5;border:1px solid #e3ede0;border-radius:12px;padding:22px;margin:20px 0 30px;}
.bspx-related-box h3{margin:0 0 12px;color:#2b2b2b;}
.bspx-related-box ul{margin:0;padding-left:20px;}
.bspx-related-box li{margin-bottom:10px;}
.bspx-related-box a{font-weight:600 !important;}

/* What we learn today - NEW: percentage progress bars, one per takeaway */
.bspx-learn{margin:26px 0 20px;}
.bspx-learn h3{font-size:20px;color:#2b2b2b;margin:0 0 18px;text-align:center;}
.bspx-learn-grid{display:flex;flex-direction:column;gap:12px;}
.bspx-learn-row{display:flex;align-items:center;gap:14px;}
.bspx-learn-pct{width:44px;flex-shrink:0;font-weight:800;color:#3f9421;font-size:14px;text-align:right;}
.bspx-learn-track{flex:1;background:#f0f2f0;border-radius:20px;height:10px;overflow:hidden;}
.bspx-learn-fill{height:100%;background:#5DB92E;border-radius:20px;}
.bspx-learn-text{flex-shrink:0;width:60%;font-size:15px;color:#3a3a3a;}
@media(max-width:820px){.bspx-learn-row{flex-wrap:wrap;}.bspx-learn-text{width:100%;order:3;}}
</style>

<div class="bspx-meta-row">
<span class="bspx-meta-pill">Technical SEO</span>
<span class="bspx-meta-pill">Speed Index</span>
<span class="bspx-meta-pill">Lighthouse</span>
<span class="bspx-meta-pill">Page Speed</span>
</div>

<p class="bspx-lede">Two pages can share the exact same First Contentful Paint and the exact same Largest Contentful Paint, and still feel completely different to load. One fills in steadily and predictably. The other sits mostly blank, then dumps everything onto the screen at once. Speed Index is the metric built specifically to tell these two experiences apart.</p>

<p>Speed Index measures how quickly the visible, above-the-fold content of a page becomes visually complete during load, expressed in seconds.</p>

<p>Unlike FCP or LCP, it does not mark a single moment in time. It is a calculated score built from comparing video frames captured throughout the entire loading process.</p>

<p>We covered the metrics this one complements in our guides to <a href="/what-is-first-contentful-paint-fcp/" target="_blank" rel="noopener">FCP</a> and <a href="/what-is-largest-contentful-paint-lcp/" target="_blank" rel="noopener">LCP</a>. Speed Index looks at the whole visual journey between those two milestones, not just a single point along the way.</p>

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


<div class="bspx-stat-grid">
<div class="bspx-stat-card"><div class="bspx-stat-num">3.4s</div><p>or less is Google's "good" Speed Index threshold on mobile devices</p></div>
<div class="bspx-stat-card"><div class="bspx-stat-num">10%</div><p>weight this metric carries in the overall Lighthouse performance score</p></div>
<div class="bspx-stat-card"><div class="bspx-stat-num">1.3s</div><p>or less is the desktop threshold needed for a subscore above 90</p></div>
</div>

<h2 id="how-speed-index-is-actually-calculated">How Speed Index Is Actually Calculated</h2>
<p>According to <a href="https://developer.chrome.com/docs/lighthouse/performance/speed-index" target="_blank" rel="noopener">Chrome for Developers' official Speed Index documentation</a>, Lighthouse captures a video of the page loading, computes the visual progression between frames, then uses the Speedline Node.js module to generate the final score.</p>

<div class="bspx-filmstrip">
<div class="bspx-film-row">
<div class="bspx-frame"><div class="bspx-frame-fill" style="height:5%;background:#c95d5d;"></div><div class="bspx-frame-label">10%</div></div>
<div class="bspx-frame"><div class="bspx-frame-fill" style="height:35%;background:#e2a52c;"></div><div class="bspx-frame-label">40%</div></div>
<div class="bspx-frame"><div class="bspx-frame-fill" style="height:70%;background:#8ec96a;"></div><div class="bspx-frame-label">75%</div></div>
<div class="bspx-frame"><div class="bspx-frame-fill" style="height:100%;background:#5DB92E;"></div><div class="bspx-frame-label">100%</div></div>
</div>
<div class="bspx-film-row">
<div class="bspx-frame-time" style="width:90px;">0.5s</div>
<div class="bspx-frame-time" style="width:90px;">1.2s</div>
<div class="bspx-frame-time" style="width:90px;">2.0s</div>
<div class="bspx-frame-time" style="width:90px;">2.8s</div>
</div>
</div>

<h2 id="speed-index-thresholds-good-needs-improvement-and-poor">Speed Index Thresholds: Good, Needs Improvement, and Poor</h2>
<div class="bspx-threshold">
<div class="bspx-th-seg bspx-th-good">Good<br>0-3.4s (mobile)</div>
<div class="bspx-th-seg bspx-th-ok">Needs Work<br>3.4-5.8s</div>
<div class="bspx-th-seg bspx-th-poor">Poor<br>5.8s+</div>
</div>

<h2 id="why-this-metric-is-not-available-in-field-data">Why This Metric Is Not Available in Field Data</h2>
<p>This is a genuinely important limitation to understand. Tap through both perspectives.</p>

<div class="bspx-tabs">
<div class="bspx-tab-buttons">
<button class="bspx-tab-btn active" onclick="bspxTab(event,'bspx-lab')">Lab-Only Measurement</button>
<button class="bspx-tab-btn" onclick="bspxTab(event,'bspx-why')">Why It Can't Scale to Real Users</button>
</div>
<div id="bspx-lab" class="bspx-tab-panel active">
<p>According to <a href="https://www.debugbear.com/docs/metrics/speed-index" target="_blank" rel="noopener">DebugBear's guide to measuring Speed Index</a>, this metric is reported by Lighthouse and other synthetic testing tools, never as part of CrUX real-user field data.</p>
</div>
<div id="bspx-why" class="bspx-tab-panel">
<p>Calculating it requires capturing and comparing screenshots throughout the entire load, an expensive operation that is simply not practical to run silently on millions of real visitor devices the way Google collects LCP or CLS data.</p>
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

<h2 id="speed-index-vs-other-lighthouse-metrics">Speed Index vs. Other Lighthouse Metrics</h2>
<div class="bspx-table-wrap">
<table class="bspx-table">
<thead>
<tr><th>Metric</th><th>What It Marks</th><th>Lighthouse Weight</th></tr>
</thead>
<tbody>
<tr><td>FCP</td><td>A single moment: first content appears</td><td>10%</td></tr>
<tr><td>LCP</td><td>A single moment: largest element appears</td><td>25%</td></tr>
<tr><td>Speed Index</td><td>A calculated score across the entire visual load</td><td>10%</td></tr>
<tr><td>TBT</td><td>Total main-thread blocking after FCP</td><td>30%</td></tr>
<tr><td>CLS</td><td>Visual stability throughout the page's lifespan</td><td>25%</td></tr>
</tbody>
</table>
</div>

<h2 id="speed-index-completeness-estimator">Speed Index Completeness Estimator</h2>
<p>Enter the approximate visual completeness percentage of your page at three points during load to estimate how your Speed Index behaves.</p>

<div class="bspx-calc">
<div class="bspx-calc-header">
<h3>Speed Index Completeness Estimator</h3>
<p>Based on the same interval-weighted formula Lighthouse uses internally</p>
</div>
<div class="bspx-calc-body">

<div class="bspx-calc-row">
<label>Completeness at 1 second (%)</label>
<input type="number" id="bspxT1" min="0" max="100" value="20">
</div>
<div class="bspx-calc-row">
<label>Completeness at 2 seconds (%)</label>
<input type="number" id="bspxT2" min="0" max="100" value="55">
</div>
<div class="bspx-calc-row">
<label>Completeness at 3 seconds (%)</label>
<input type="number" id="bspxT3" min="0" max="100" value="90">
</div>

<button class="bspx-calc-btn" onclick="bspxCalc()">Estimate My Score</button>

<div class="bspx-calc-result">
<div class="bspx-calc-result-num" id="bspxTotal">-- s</div>
<p id="bspxVerdict">Enter your completeness percentages above and click estimate.</p>
</div>

</div>
</div>

<script>
function bspxTab(evt, id){
  var panels = document.querySelectorAll('.bspx-tab-panel');
  var btns = document.querySelectorAll('.bspx-tab-btn');
  panels.forEach(function(p){p.classList.remove('active');});
  btns.forEach(function(b){b.classList.remove('active');});
  document.getElementById(id).classList.add('active');
  evt.currentTarget.classList.add('active');
}
function bspxCalc(){
  var t1 = parseFloat(document.getElementById('bspxT1').value) || 0;
  var t2 = parseFloat(document.getElementById('bspxT2').value) || 0;
  var t3 = parseFloat(document.getElementById('bspxT3').value) || 0;
  var interval = 1;
  var estimate = interval*(1-t1/100) + interval*(1-t2/100) + interval*(1-t3/100);
  document.getElementById('bspxTotal').innerText = estimate.toFixed(2) + ' s (approx.)';
  var verdict = document.getElementById('bspxVerdict');
  if(estimate <= 1.5){ verdict.innerText = "Excellent visual progression. Your page fills in quickly across each interval."; }
  else if(estimate <= 2.2){ verdict.innerText = "Reasonable, but there's room to fill in content earlier in the timeline."; }
  else { verdict.innerText = "Slow visual progression. Content is likely staying hidden too long before appearing."; }
}
</script>
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

<h2 id="what-actually-improves-speed-index">What Actually Improves Speed Index</h2>
<p>According to <a href="https://nitropack.io/blog/google-page-speed-index/" target="_blank" rel="noopener">NitroPack's guide to reducing Speed Index</a>, the core techniques involve reducing JavaScript execution time, minimizing main-thread work, and managing the impact of third-party scripts, the same fixes that help several other loading metrics simultaneously.</p>

<p>According to <a href="https://migratelab.com/resources/lighthouse-performance-metrics-explained-how-to-improve" target="_blank" rel="noopener">MigrateLab's complete Lighthouse metrics guide</a>, each metric follows a log-normal scoring curve, meaning early improvements move the needle far more than chasing the last few tenths of a second once a page is already reasonably fast.</p>

<h2 id="why-progressive-rendering-matters-more-than-raw-speed">Why Progressive Rendering Matters More Than Raw Speed</h2>
<p>According to <a href="https://requestmetrics.com/web-performance/understanding-lighthouse-speed-index/" target="_blank" rel="noopener">Request Metrics' guide to understanding Lighthouse Speed Index</a>, this metric specifically rewards pages that paint meaningful chunks steadily and punishes pages that download everything first before rendering much of anything.</p>

<p>A page that shows 80% of its content almost instantly, then slowly finishes the remaining 20%, scores better than a page that sits blank and then reveals everything at once, even if both pages technically finish loading at the same total time.</p>

<h2 id="common-causes-of-a-poor-score">Common Causes of a Poor Score</h2>
<p>According to <a href="https://gtmetrix.com/speed-index.html" target="_blank" rel="noopener">GTmetrix's guide to Speed Index</a>, render-blocking resources are among the most frequent causes, since CSS and synchronous JavaScript loaded before visible content directly delays every frame comparison Lighthouse captures.</p>

<p>According to <a href="https://nestify.io/blog/speed-index-for-page-speed/" target="_blank" rel="noopener">Nestify's guide to Speed Index for page speed</a>, heavy above-the-fold images without proper compression or modern formats also contribute significantly, since the browser has to finish downloading and decoding them before the visible portion of the page can register as complete.</p>

<p>A third common cause is web fonts that block text rendering until they finish loading.</p>

<p>If custom fonts are not preloaded or given a fallback strategy, the visible page can sit with invisible text for a noticeable stretch, delaying visual completeness even though the underlying HTML has technically already arrived.</p>

<h2 id="interpreting-a-speed-index-result-in-context">Interpreting a Speed Index Result in Context</h2>
<p>A single number in isolation tells you less than comparing it against your own site's history or a direct competitor running the same type of page.</p>

<p>According to <a href="https://unlighthouse.dev/glossary/speed-index" target="_blank" rel="noopener">Unlighthouse's guide to Lighthouse Speed Index</a>, the Lighthouse Score Calculator lets you see exactly how a given value translates into its 10% contribution toward your overall performance score.</p>

<p>Tracking this number across releases, rather than checking it once and moving on, reveals whether a new feature or added script quietly regressed the visual loading experience, even when other metrics appear unaffected.</p>

<h2 id="setting-up-a-repeatable-testing-process">Setting Up a Repeatable Testing Process</h2>
<p>Running a single test and drawing conclusions from it is a common mistake. Network conditions, server load, and even minor CPU throttling variance can shift a single test result by a meaningful margin without anything on the site actually changing.</p>

<p>A more reliable approach runs the same test three to five times and takes the median result, or uses a monitoring tool that automates this repetition on a schedule. This turns a noisy single measurement into a dependable trend line worth acting on.</p>

<h2 id="faqs-on-speed-index">FAQs on Speed Index</h2>

<div class="bspx-faq-item">
<div class="bspx-faq-q">What is a good Speed Index score?</div>
<div class="bspx-faq-a">Google considers 3.4 seconds or less good on mobile devices, and 1.3 seconds or less good on desktop. Values roughly between the good threshold and 5.8 seconds need improvement, with anything higher considered poor.</div>
</div>
<div class="bspx-faq-item">
<div class="bspx-faq-q">Is Speed Index a Core Web Vital?</div>
<div class="bspx-faq-a">No. It is one of five metrics in the Lighthouse performance score but is not one of the three official Core Web Vitals, LCP, INP, and CLS, that Google uses directly for search ranking evaluation.</div>
</div>
<div class="bspx-faq-item">
<div class="bspx-faq-q">Why isn't Speed Index available in Google Search Console or CrUX?</div>
<div class="bspx-faq-a">Calculating it requires capturing and analyzing video frames throughout a page's entire load, which is too resource-intensive to run at scale across millions of real user devices, unlike simpler timestamp-based metrics.</div>
</div>
<div class="bspx-faq-item">
<div class="bspx-faq-q">How is Speed Index different from First Contentful Paint?</div>
<div class="bspx-faq-a">FCP marks a single moment when the first content appears. Speed Index is a calculated score covering the entire visual loading process, rewarding pages that fill in steadily rather than all at once.</div>
</div>
<div class="bspx-faq-item">
<div class="bspx-faq-q">What tools can measure Speed Index?</div>
<div class="bspx-faq-a">Lighthouse, accessible through Chrome DevTools or PageSpeed Insights, and WebPageTest both report this metric, since WebPageTest originally introduced the underlying concept.</div>
</div>
<div class="bspx-faq-item">
<div class="bspx-faq-q">Does fixing Speed Index also help other metrics?</div>
<div class="bspx-faq-a">Generally yes. Reducing JavaScript execution time and minimizing main-thread work, the primary fixes for this metric, also tend to improve LCP, TBT, and overall perceived performance simultaneously.</div>
</div>

<div class="bspx-related-box">
<h3>Related Articles</h3>
<ul>
<li><a href="/what-is-first-contentful-paint-fcp/" target="_blank" rel="noopener">What Is First Contentful Paint (FCP)? How It Affects SEO and User Experience</a></li>
<li><a href="/what-is-largest-contentful-paint-lcp/" target="_blank" rel="noopener">What Is Largest Contentful Paint (LCP)? How to Diagnose and Fix It</a></li>
<li><a href="/what-is-total-blocking-time-tbt/" target="_blank" rel="noopener">What Is Total Blocking Time (TBT)? A Complete Guide for Website Owners</a></li>
<li><a href="/how-to-measure-core-web-vitals-tools-guide/" target="_blank" rel="noopener">How to Measure Core Web Vitals: PageSpeed Insights, Lighthouse, CrUX & Search Console</a></li>
</ul>
</div>

<div class="bspx-learn">
<h3>What We Learn Today</h3>
<div class="bspx-learn-grid">
<div class="bspx-learn-row"><span class="bspx-learn-pct">100%</span><div class="bspx-learn-track"><div class="bspx-learn-fill" style="width:100%;"></div></div><span class="bspx-learn-text">Speed Index measures the entire visual load, not one moment</span></div>
<div class="bspx-learn-row"><span class="bspx-learn-pct">10%</span><div class="bspx-learn-track"><div class="bspx-learn-fill" style="width:10%;"></div></div><span class="bspx-learn-text">Its weight in the Lighthouse performance score</span></div>
<div class="bspx-learn-row"><span class="bspx-learn-pct">3.4s</span><div class="bspx-learn-track"><div class="bspx-learn-fill" style="width:40%;"></div></div><span class="bspx-learn-text">The good threshold on mobile devices</span></div>
<div class="bspx-learn-row"><span class="bspx-learn-pct">0%</span><div class="bspx-learn-track"><div class="bspx-learn-fill" style="width:0%;"></div></div><span class="bspx-learn-text">Presence in CrUX field data, it is lab-only</span></div>
<div class="bspx-learn-row"><span class="bspx-learn-pct">80%</span><div class="bspx-learn-track"><div class="bspx-learn-fill" style="width:80%;"></div></div><span class="bspx-learn-text">Early visual progress matters more than final total time</span></div>
<div class="bspx-learn-row"><span class="bspx-learn-pct">100%</span><div class="bspx-learn-track"><div class="bspx-learn-fill" style="width:100%;"></div></div><span class="bspx-learn-text">JS and main-thread fixes improve this metric alongside others</span></div>
</div>
</div>

</div>
