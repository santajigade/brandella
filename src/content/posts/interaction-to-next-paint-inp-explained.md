---
title: "Interaction to Next Paint (INP) Explained: Improve Website Responsiveness and Pass Core Web Vitals"
slug: "interaction-to-next-paint-inp-explained"
date: "2026-07-29T02:59:49"
updated: "2026-08-09T08:40:10"
author: "santajigade"
categories: ["core-web-vitals", "seo"]
primaryCategory: "seo"
description: "Discover what Interaction to Next Paint (INP) is, how Google measures responsiveness, common causes of poor INP scores, and proven ways to optimize website performance"
focusKeyword: "Interaction to Next Paint"
takeaways:
  - "Interaction to Next Paint measures how long a page takes to visually respond after a click, tap or key press, reporting the worst or near-worst interaction."
  - "INP replaced First Input Delay as a Core Web Vital on March 12, 2024, and roughly 43% of websites fail its 200ms good threshold."
  - "Every INP score has three phases: input delay, processing time and presentation delay, each fixed by breaking up long tasks, lightening handlers or simplifying visual updates."
  - "Long JavaScript tasks over 50 milliseconds, too many third-party scripts, non-essential work in click handlers and large DOM size are common causes of poor INP."
  - "Debouncing does not fix slow click handlers and a CDN does not improve INP, because INP measures runtime responsiveness after the page has loaded."
image: "/wp-content/uploads/2026/07/Interaction-to-Next-Paint.webp"
imageAlt: "Interaction to Next Paint"
words: 1750
views: 322
format: "html"
---
<div class="bin-wrap">
<style>
.bin-wrap{font-family:'Segoe UI', Arial, sans-serif;font-size:17px;line-height:1.75;color:#2e2e2e;max-width:100%;}
.bin-wrap h2{font-size:25px;color:#2b2b2b;margin:36px 0 16px;font-weight:800;border-left:5px solid #5DB92E;padding-left:14px;}
.bin-wrap h3{font-size:19px;color:#2b2b2b;margin:18px 0 10px;font-weight:700;}
.bin-wrap p{margin:0 0 14px;font-size:17px;}
.bin-wrap a{color:#3f9421;font-weight:600;text-decoration:none;}
.bin-wrap a:hover{color:#2f7418;text-decoration:none;}
.bin-wrap ul,.bin-wrap ol{margin:0 0 16px;padding-left:22px;}
.bin-wrap li{margin-bottom:8px;font-size:17px;}

.bin-lede{font-size:20px;color:#333;font-style:italic;margin:0 0 18px;line-height:1.6;border-left:3px solid #5DB92E;padding-left:16px;}

.bin-meta-row{display:flex;flex-wrap:wrap;gap:10px;margin:0 0 24px;}
.bin-meta-pill{background:#eef8e8;color:#3f9421;border:1px solid #cdeabb;border-radius:20px;padding:6px 16px;font-size:13px;font-weight:700;text-transform:uppercase;letter-spacing:.5px;}

/* Stat cards */
.bin-stat-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin:20px 0 30px;}
.bin-stat-card{background:#f7faf5;border:1px solid #e3ede0;border-radius:12px;padding:22px 16px;text-align:center;}
.bin-stat-num{font-size:32px;font-weight:800;color:#5DB92E;margin-bottom:6px;}
.bin-stat-card p{margin:0;font-size:17px;color:#4a4a4a;}
@media(max-width:820px){.bin-stat-grid{grid-template-columns:1fr;}}

/* Interaction timeline illustration */
.bin-illo{margin:20px 0 30px;background:#fff;border:1px solid #e3ede0;border-radius:14px;padding:26px 22px;}
.bin-illo-row{display:flex;align-items:center;gap:4px;margin-bottom:14px;}
.bin-illo-seg{flex:1;text-align:center;border-radius:8px;padding:12px 6px;font-size:13px;font-weight:700;color:#fff;}
.bin-illo-seg.a{background:#c95d5d;flex:2;}
.bin-illo-seg.b{background:#e2a52c;flex:3;}
.bin-illo-seg.c{background:#5DB92E;flex:1;}
.bin-illo-caption{display:flex;justify-content:space-between;font-size:12px;color:#7a7a7a;}

/* Threshold meter */
.bin-threshold{display:flex;border-radius:10px;overflow:hidden;margin:20px 0 30px;height:50px;}
.bin-th-seg{display:flex;align-items:center;justify-content:center;color:#fff;font-weight:800;font-size:14px;flex-direction:column;line-height:1.3;}
.bin-th-good{background:#5DB92E;width:40%;}
.bin-th-ok{background:#e2a52c;width:30%;}
.bin-th-poor{background:#c95d5d;width:30%;}

/* Numbered factors */
.bin-factors{display:flex;flex-direction:column;gap:14px;margin:20px 0 30px;}
.bin-factor{display:flex;gap:16px;background:#fff;border:1px solid #e3ede0;border-radius:12px;padding:18px 20px;align-items:flex-start;}
.bin-factor-num{width:36px;height:36px;border-radius:50%;background:#5DB92E;color:#fff;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:17px;flex-shrink:0;}
.bin-factor h3{margin:0 0 6px;font-size:17px;}
.bin-factor p{margin:0;font-size:17px;color:#4a4a4a;}

/* Tabs */
.bin-tabs{margin:20px 0 30px;}
.bin-tab-buttons{display:flex;flex-wrap:wrap;gap:8px;border-bottom:2px solid #e3ede0;}
.bin-tab-btn{background:#f2f5f0;border:none;border-radius:8px 8px 0 0;padding:12px 20px;font-size:17px;font-weight:700;color:#4a4a4a;cursor:pointer;font-family:'Segoe UI',Arial,sans-serif;}
.bin-tab-btn.active{background:#5DB92E;color:#fff;}
.bin-tab-panel{display:none;border:1px solid #e3ede0;border-top:none;border-radius:0 0 10px 10px;padding:20px;background:#fff;}
.bin-tab-panel.active{display:block;}
.bin-tab-panel p{margin:0 0 10px;}
.bin-tab-panel p:last-child{margin-bottom:0;}

/* Table */
.bin-table-wrap{overflow-x:auto;margin:20px 0 30px;}
.bin-table{width:100%;border-collapse:collapse;font-size:17px;}
.bin-table th{background:#2b2b2b;color:#fff;padding:13px 16px;text-align:left;font-weight:700;}
.bin-table td{padding:13px 16px;border-bottom:1px solid #e3ede0;}
.bin-table tr:nth-child(even) td{background:#f7faf5;}

/* Interactive checklist widget */
.bin-check{border-radius:14px;overflow:hidden;border:1px solid #e3ede0;margin:20px 0 32px;}
.bin-check-header{background:#2b2b2b;color:#fff;padding:16px 22px;font-weight:700;font-size:17px;}
.bin-check-body{padding:22px;background:#fff;}
.bin-check-item{display:flex;align-items:flex-start;gap:12px;padding:10px 0;border-bottom:1px solid #f0f2f0;cursor:pointer;}
.bin-check-item:last-of-type{border-bottom:none;}
.bin-check-item input{margin-top:4px;width:18px;height:18px;accent-color:#5DB92E;flex-shrink:0;}
.bin-check-item span{font-size:17px;color:#3a3a3a;}
.bin-check-result{margin-top:16px;background:#f7faf5;border:1px solid #e3ede0;border-radius:10px;padding:16px 18px;font-size:17px;font-weight:700;color:#2b2b2b;text-align:center;}

/* FAQ */
.bin-faq-item{margin-bottom:14px;}
.bin-faq-q{background:#f2f5f0;border-radius:8px 8px 0 0;padding:14px 18px;font-weight:700;color:#2b2b2b;font-size:17px;}
.bin-faq-a{background:#fff;border:1px solid #eef1ec;border-top:none;border-radius:0 0 8px 8px;padding:16px 18px;font-size:17px;color:#4a4a4a;}

/* Related */
.bin-related-box{background:#f7faf5;border:1px solid #e3ede0;border-radius:12px;padding:22px;margin:20px 0 30px;}
.bin-related-box h3{margin:0 0 12px;color:#2b2b2b;}
.bin-related-box ul{margin:0;padding-left:20px;}
.bin-related-box li{margin-bottom:10px;}
.bin-related-box a{font-weight:600 !important;}

/* What we learn today - 22nd distinct style: horizontal scoreboard strip */
.bin-learn{margin:26px 0 20px;background:#2b2b2b;border-radius:14px;padding:8px;}
.bin-learn h3{font-size:20px;color:#fff;margin:0;padding:14px 16px 18px;text-align:center;}
.bin-learn-strip{display:grid;grid-template-columns:repeat(2,1fr);gap:8px;}
.bin-learn-cell{background:#3a3a3a;border-radius:8px;padding:14px 16px;}
.bin-learn-cell p{margin:0;font-size:14px;color:#e8e8e8;font-weight:600;}
.bin-learn-cell b{color:#7fd44f;}
@media(max-width:820px){.bin-learn-strip{grid-template-columns:1fr;}}
</style>

<div class="bin-meta-row">
<span class="bin-meta-pill">Technical SEO</span>
<span class="bin-meta-pill">INP</span>
<span class="bin-meta-pill">Core Web Vitals</span>
<span class="bin-meta-pill">Responsiveness</span>
</div>

<p class="bin-lede">Interaction to Next Paint fails on roughly 43% of websites, more than LCP or CLS, making it the single most commonly failed Core Web Vital in 2026. A site can pass every other performance check and still feel broken if a menu, filter, or "Add to Cart" button takes half a second to respond. This is what INP measures, why so many sites suddenly started failing it, and how to fix it.</p>

<p>Interaction to Next Paint measures how long a page takes to visually respond after someone clicks, taps, or presses a key.</p>

<p>The browser tracks every interaction throughout a visit and reports the worst one, or near-worst on pages with many interactions, as the page's INP score.</p>

<p>We covered INP alongside LCP and CLS in our <a href="/core-web-vitals-2026/" target="_blank" rel="noopener">Core Web Vitals overview</a>, and went deep on the loading metric in our <a href="/what-is-largest-contentful-paint-lcp/" target="_blank" rel="noopener">LCP guide</a>. This article does the same for INP specifically.</p>

<div class="bin-stat-grid">
<div class="bin-stat-card"><div class="bin-stat-num">43%</div><p>of websites still fail the 200ms INP threshold, the most commonly failed Core Web Vital</p></div>
<div class="bin-stat-card"><div class="bin-stat-num">200ms</div><p>is the "good" INP threshold Google measures, at the 75th percentile of real visits</p></div>
<div class="bin-stat-card"><div class="bin-stat-num">20+</div><p>third-party scripts a typical page-builder site can load before any of its own code runs</p></div>
</div>

<h2 id="what-interaction-to-next-paint-actually-measures">What Interaction to Next Paint Actually Measures</h2>
<p>Every INP score breaks into three phases that happen between a click and the next visual update.</p>

<div class="bin-illo">
<div class="bin-illo-row">
<div class="bin-illo-seg a">Input Delay</div>
<div class="bin-illo-seg b">Processing Time</div>
<div class="bin-illo-seg c">Presentation Delay</div>
</div>
<div class="bin-illo-caption"><span>Click happens</span><span>Next frame paints</span></div>
</div>

<h2 id="why-inp-replaced-first-input-delay-in-2024">Why INP Replaced First Input Delay in 2024</h2>
<p>Google announced on March 12, 2024 that INP officially replaced First Input Delay as a Core Web Vital.</p>

<p>According to <a href="https://parachutedesign.ca/blog/interaction-to-next-paint-inp/" target="_blank" rel="noopener">Parachute Design's 2026 INP guide</a>, FID only measured the delay before the browser started handling the very first interaction. It ignored all processing time and rendering work that happened after that initial moment.</p>

<p>A site could score well on FID yet still feel sluggish on every interaction after the first click.</p>

<p>According to <a href="https://logoswebdesigns.com/blog/how-to-fix-inp-interaction-to-next-paint-2026/" target="_blank" rel="noopener">Logos Web Designs' 2026 INP guide</a>, this is exactly why sites built on WordPress, Webflow, and Wix that scored "good" under FID now commonly score "poor" on INP without a single code change.</p>

<h2 id="inp-thresholds-good-needs-improvement-and-poor">INP Thresholds: Good, Needs Improvement, and Poor</h2>
<div class="bin-threshold">
<div class="bin-th-seg bin-th-good">Good<br>0-200ms</div>
<div class="bin-th-seg bin-th-ok">Needs Work<br>200-500ms</div>
<div class="bin-th-seg bin-th-poor">Poor<br>500ms+</div>
</div>

<h2 id="five-common-causes-of-poor-inp">Five Common Causes of Poor INP</h2>
<div class="bin-factors">
<div class="bin-factor">
<div class="bin-factor-num">1</div>
<div>
<h3>Long JavaScript Tasks Blocking the Main Thread</h3>
<p>Any script running longer than 50 milliseconds blocks the browser from responding to input until it finishes, directly adding to processing time.</p>
</div>
</div>
<div class="bin-factor">
<div class="bin-factor-num">2</div>
<div>
<h3>Too Many Third-Party Scripts</h3>
<p>According to Logos Web Designs' guide referenced above, a typical page-builder site with a form plugin and a tag manager can load 20 or more third-party scripts before any first-party code runs, each one competing for the main thread.</p>
</div>
</div>
<div class="bin-factor">
<div class="bin-factor-num">3</div>
<div>
<h3>Non-Essential Work Inside Click Handlers</h3>
<p>According to <a href="https://www.sitepoint.com/core-web-vitals-2026-fix-interaction-to-next-paint/" target="_blank" rel="noopener">SitePoint's 2026 INP fixing guide</a>, event handlers often run analytics logging or state synchronization that has nothing to do with the visible response, delaying the paint the user is actually waiting for.</p>
</div>
</div>
<div class="bin-factor">
<div class="bin-factor-num">4</div>
<div>
<h3>Large DOM Size</h3>
<p>Pages with an excessive number of DOM elements take longer for the browser to recalculate styles and layout after any interaction, even a simple one.</p>
</div>
</div>
<div class="bin-factor">
<div class="bin-factor-num">5</div>
<div>
<h3>Rendering Heavy Visual Updates Synchronously</h3>
<p>Complex animations or large content updates triggered directly by a click can hold up the presentation delay phase, the final step before the next frame paints.</p>
</div>
</div>
</div>
<h2 id="debouncing-vs-throttling-which-fix-applies-to-your-interaction">Debouncing vs. Throttling: Which Fix Applies to Your Interaction</h2>
<p>These two techniques get confused constantly, and using the wrong one wastes effort. Tap through both to see which applies to your situation.</p>

<div class="bin-tabs">
<div class="bin-tab-buttons">
<button class="bin-tab-btn active" onclick="binTab(event,'bin-debounce')">Debouncing</button>
<button class="bin-tab-btn" onclick="binTab(event,'bin-throttle')">Throttling</button>
</div>
<div id="bin-debounce" class="bin-tab-panel active">
<p>According to <a href="https://www.sitepoint.com/core-web-vitals-2026-fix-interaction-to-next-paint/" target="_blank" rel="noopener">SitePoint's guide</a>, debouncing delays execution until rapid-fire events stop, making it effective for search inputs where processing should only happen once the user pauses typing.</p>

<p>It does not help click-driven INP at all, since a click is a single discrete event, not a rapid stream.</p>
</div>
<div id="bin-throttle" class="bin-tab-panel">
<p>Throttling limits execution to a fixed interval, suiting scroll or resize-driven updates where some responsiveness during the event stream is still needed.</p>

<p>Neither technique fixes a slow click handler. The real fix for clicks is reducing the actual work inside the handler, not delaying when it fires.</p>
</div>
</div>

<h2 id="how-to-measure-and-diagnose-your-own-inp-score">How to Measure and Diagnose Your Own INP Score</h2>
<p>Start with Google Search Console's Core Web Vitals report, which groups URLs by Good, Needs Improvement, and Poor status separately for mobile and desktop.</p>

<p>According to <a href="https://www.linkgraph.com/blog/interaction-to-next-paint-optimization/" target="_blank" rel="noopener">LinkGraph's INP optimization guide</a>, Google reports the P75 value, meaning the score at which 75% of your visitors experience that number or better. A P75 INP of 250 milliseconds means a quarter of visitors experience something worse than that.</p>

<p>If your site does not have enough traffic for field data to appear, according to <a href="https://wp-rocket.me/google-core-web-vitals-wordpress/interaction-to-next-paint-insight/" target="_blank" rel="noopener">WP Rocket's guide to the INP insight</a>, Real User Monitoring through the open-source web-vitals JavaScript library fills the gap and can even identify which specific interaction is causing the slowdown.</p>

<h2 id="fixing-inp-step-by-step">Fixing INP Step by Step</h2>
<div class="bin-table-wrap">
<table class="bin-table">
<thead>
<tr><th>INP Phase</th><th>What Causes Delay Here</th><th>Fix</th></tr>
</thead>
<tbody>
<tr><td>Input delay</td><td>Main thread busy with unrelated work</td><td>Break up long tasks, defer non-critical scripts</td></tr>
<tr><td>Processing time</td><td>Heavy logic inside the event handler</td><td>Move non-visual work out of the handler's synchronous path</td></tr>
<tr><td>Presentation delay</td><td>Complex rendering or large DOM updates</td><td>Simplify the visual update, reduce DOM size</td></tr>
</tbody>
</table>
</div>

<div class="bin-check">
<div class="bin-check-header">Quick Check: Is Your Site Likely Failing INP?</div>
<div class="bin-check-body">
<label class="bin-check-item"><input type="checkbox" onchange="binCheck()"><span>My site uses a page builder, form plugin, and tag manager together.</span></label>
<label class="bin-check-item"><input type="checkbox" onchange="binCheck()"><span>Menus, filters, or buttons feel slightly delayed when I click them myself.</span></label>
<label class="bin-check-item"><input type="checkbox" onchange="binCheck()"><span>I have not checked the INP section of my Search Console Core Web Vitals report.</span></label>
<label class="bin-check-item"><input type="checkbox" onchange="binCheck()"><span>My other Core Web Vitals (LCP, CLS) are already in good shape.</span></label>
<div id="bin-check-result" class="bin-check-result">Check the boxes that apply to see how likely INP is your bottleneck.</div>
</div>
</div>

<script>
function binTab(evt, id){
  var panels = document.querySelectorAll('.bin-tab-panel');
  var btns = document.querySelectorAll('.bin-tab-btn');
  panels.forEach(function(p){p.classList.remove('active');});
  btns.forEach(function(b){b.classList.remove('active');});
  document.getElementById(id).classList.add('active');
  evt.currentTarget.classList.add('active');
}
function binCheck(){
  var boxes = document.querySelectorAll('.bin-check-item input');
  var count = 0;
  boxes.forEach(function(b){ if(b.checked) count++; });
  var msg = "Check the boxes that apply to see how likely INP is your bottleneck.";
  if(count >= 3){ msg = "High likelihood. Audit your third-party scripts and event handlers first."; }
  else if(count == 2){ msg = "Worth checking. Pull your P75 INP data from Search Console this week."; }
  else if(count == 1){ msg = "Probably fine for now, but keep an eye on it as you add new scripts."; }
  document.getElementById('bin-check-result').innerText = msg;
}
</script>
<h2 id="why-mobile-devices-struggle-more-with-responsiveness">Why Mobile Devices Struggle More With Responsiveness</h2>
<p>Mobile processors are significantly less powerful than desktop chips, which means the exact same JavaScript workload takes noticeably longer to execute on a phone than on a laptop.</p>

<p>This gap widens further on lower-end devices, which make up a meaningful share of real traffic in many markets.</p>

<p>A script that runs in 40 milliseconds on a flagship phone can easily take 150 milliseconds or more on a budget device, pushing a page from comfortably passing into failing territory without any change to the code itself.</p>

<p>This is one reason field data, gathered from real devices, tells a more honest story than a lab test run on a single development machine.</p>

<p>Testing exclusively on a fast device gives a misleadingly optimistic picture of how the majority of visitors actually experience a page.</p>

<h2 id="building-responsiveness-into-new-features-from-the-start">Building Responsiveness Into New Features From the Start</h2>
<p>The cheapest way to keep a page responsive is designing new features with responsiveness in mind from the beginning, rather than retrofitting fixes after a feature ships and users start complaining.</p>

<p>Before adding a new interactive element, a reasonable question to ask is what work actually needs to happen synchronously to update the screen.</p>

<p>What can be deferred to run afterward without the user noticing any delay is the second question. Analytics calls, background data syncing, and non-visual logging are common candidates for deferral, since none of them need to block the visual response a user is waiting to see.</p>

<h2 id="common-inp-mistakes-that-waste-optimization-effort">Common INP Mistakes That Waste Optimization Effort</h2>
<p>The most common mistake is over-optimizing rare interactions.</p>

<p>According to <a href="https://www.rollin.ca/resources/how-to-fix-inp-interaction-to-next-paint-optimization-guide/" target="_blank" rel="noopener">Rollin's INP optimization guide</a>, INP reports approximately the worst interaction, so fixing the most common interaction paths on a page improves overall experience more effectively than chasing an edge case a handful of users ever trigger.</p>

<p>A second mistake is assuming a CDN fixes INP the way it fixes LCP. According to LinkGraph's guide referenced above, CDNs primarily help loading performance, since INP measures runtime responsiveness that happens well after the page has already loaded.</p>

<p>A third mistake, according to <a href="https://www.egochi.com/interaction-to-next-paint/" target="_blank" rel="noopener">Egochi's guide to fixing INP</a>, is treating INP as a one-time fix rather than an ongoing discipline. Every new script, plugin, or feature added after the initial fix can quietly reintroduce the same responsiveness problems.</p>

<h2 id="why-inp-matters-alongside-the-rest-of-your-technical-seo">Why INP Matters Alongside the Rest of Your Technical SEO</h2>
<p>A page that responds instantly to clicks also tends to sit on a leaner, better-maintained codebase overall, the same discipline behind clean <a href="/what-is-schema-markup/" target="_blank" rel="noopener">schema markup</a> and efficient <a href="/crawl-budget-explained/" target="_blank" rel="noopener">crawl budget</a> usage. Google treats page experience as one connected signal, not three isolated checkboxes.</p>

<h2 id="faqs-on-interaction-to-next-paint-inp">FAQs on Interaction to Next Paint (INP)</h2>

<div class="bin-faq-item">
<div class="bin-faq-q">What is a good INP score?</div>
<div class="bin-faq-a">Google considers an INP of 200 milliseconds or less, at the 75th percentile of real visits, to be good. Between 200 and 500 milliseconds needs improvement, and anything above 500 milliseconds is poor.</div>
</div>
<div class="bin-faq-item">
<div class="bin-faq-q">Why did my site suddenly start failing Core Web Vitals after passing before?</div>
<div class="bin-faq-a">This usually happens because INP replaced First Input Delay in March 2024. Sites that scored well under the old metric can score poorly under INP without any code changes, since INP measures every interaction, not just the first one.</div>
</div>
<div class="bin-faq-item">
<div class="bin-faq-q">Does a CDN help improve INP?</div>
<div class="bin-faq-a">Not directly. CDNs primarily improve loading metrics like LCP and TTFB. INP measures runtime responsiveness after the page has already loaded, so CDN improvements have limited impact on it.</div>
</div>
<div class="bin-faq-item">
<div class="bin-faq-q">Should I debounce my click handlers to improve INP?</div>
<div class="bin-faq-a">No. Debouncing only helps with rapid-fire events like typing. Clicks are single, discrete events, so debouncing a click handler does not improve its INP. The fix is reducing the work the handler performs, not delaying it.</div>
</div>
<div class="bin-faq-item">
<div class="bin-faq-q">Why does INP fail more often than LCP or CLS?</div>
<div class="bin-faq-a">INP depends on runtime JavaScript efficiency across every interaction throughout a visit, which is structurally harder to control than a single loading or layout stability measurement, making it the most commonly failed Core Web Vital in 2026.</div>
</div>
<div class="bin-faq-item">
<div class="bin-faq-q">Can I check INP without much website traffic?</div>
<div class="bin-faq-a">Yes. Search Console requires sufficient traffic for field data to appear, but Real User Monitoring through the open-source web-vitals JavaScript library can measure INP directly, even on lower-traffic sites.</div>
</div>

<div class="bin-related-box">
<h3>Related Articles</h3>
<ul>
<li><a href="/core-web-vitals-2026/" target="_blank" rel="noopener">Core Web Vitals in 2026: What Actually Changed and What Still Matters</a></li>
<li><a href="/what-is-largest-contentful-paint-lcp/" target="_blank" rel="noopener">What Is Largest Contentful Paint (LCP)? How to Diagnose and Fix It</a></li>
<li><a href="/crawl-budget-explained/" target="_blank" rel="noopener">Crawl Budget Explained: Why Google Might Be Ignoring Half Your Site</a></li>
<li><a href="/what-is-schema-markup/" target="_blank" rel="noopener">What Is Schema Markup? A Complete Guide for SEO and AI Search in 2026</a></li>
</ul>
</div>

<div class="bin-learn">
<h3>What We Learn Today</h3>
<div class="bin-learn-strip">
<div class="bin-learn-cell"><p><b>200ms</b> is the good INP threshold, measured at the 75th percentile</p></div>
<div class="bin-learn-cell"><p><b>43%</b> of sites still fail INP, more than any other Core Web Vital</p></div>
<div class="bin-learn-cell"><p><b>2024</b> is when INP officially replaced First Input Delay</p></div>
<div class="bin-learn-cell"><p><b>3 phases</b> make up every INP score: input delay, processing, presentation</p></div>
<div class="bin-learn-cell"><p><b>Scripts</b> especially third-party ones, are the most common root cause</p></div>
<div class="bin-learn-cell"><p><b>Ongoing</b> discipline is required, not a one-time fix</p></div>
</div>
</div>

</div>
