---
title: "What Is Total Blocking Time (TBT)? A Complete Guide for Website Owners"
slug: "what-is-total-blocking-time-tbt"
date: "2026-07-31T09:42:14"
updated: "2026-08-02T12:07:02"
author: "santajigade"
categories: ["digital-marketing"]
primaryCategory: "digital-marketing"
description: "TBT carries 30% weight in your Lighthouse score, more than any other metric. Learn what causes high TBT and how to calculate and fix it."
focusKeyword: "TBT"
image: "/wp-content/uploads/2026/07/TBT.webp"
imageAlt: "TBT"
words: 1350
views: 90
format: "html"
---
<div class="btbt-wrap">
<style>
.btbt-wrap{font-family:'Segoe UI', Arial, sans-serif;font-size:17px;line-height:1.75;color:#2e2e2e;max-width:100%;}
.btbt-wrap h2{font-size:25px;color:#2b2b2b;margin:36px 0 16px;font-weight:800;border-left:5px solid #5DB92E;padding-left:14px;}
.btbt-wrap h3{font-size:19px;color:#2b2b2b;margin:18px 0 10px;font-weight:700;}
.btbt-wrap p{margin:0 0 14px;font-size:17px;}
.btbt-wrap a{color:#3f9421;font-weight:600;text-decoration:none;}
.btbt-wrap a:hover{color:#2f7418;text-decoration:none;}
.btbt-wrap ul,.btbt-wrap ol{margin:0 0 16px;padding-left:22px;}
.btbt-wrap li{margin-bottom:8px;font-size:17px;}

.btbt-lede{font-size:20px;color:#333;font-style:italic;margin:0 0 18px;line-height:1.6;border-left:3px solid #5DB92E;padding-left:16px;}

.btbt-meta-row{display:flex;flex-wrap:wrap;gap:10px;margin:0 0 24px;}
.btbt-meta-pill{background:#eef8e8;color:#3f9421;border:1px solid #cdeabb;border-radius:20px;padding:6px 16px;font-size:13px;font-weight:700;text-transform:uppercase;letter-spacing:.5px;}

/* Stat cards */
.btbt-stat-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin:20px 0 30px;}
.btbt-stat-card{background:#f7faf5;border:1px solid #e3ede0;border-radius:12px;padding:22px 16px;text-align:center;}
.btbt-stat-num{font-size:32px;font-weight:800;color:#5DB92E;margin-bottom:6px;}
.btbt-stat-card p{margin:0;font-size:17px;color:#4a4a4a;}
@media(max-width:820px){.btbt-stat-grid{grid-template-columns:1fr;}}

/* NEW: Long task bar chart with threshold line */
.btbt-illo{margin:20px 0 30px;background:#fff;border:1px solid #e3ede0;border-radius:14px;padding:26px 22px;position:relative;}
.btbt-illo-bars{display:flex;align-items:flex-end;gap:16px;height:140px;position:relative;padding-top:20px;}
.btbt-illo-threshold{position:absolute;left:0;right:0;top:80px;border-top:2px dashed #c95d5d;}
.btbt-illo-threshold span{position:absolute;right:0;top:-18px;font-size:11px;color:#c95d5d;font-weight:800;}
.btbt-illo-bar{flex:1;border-radius:6px 6px 0 0;position:relative;display:flex;align-items:flex-start;justify-content:center;padding-top:6px;}
.btbt-illo-bar span{font-size:11px;color:#fff;font-weight:800;}
.btbt-illo-labels{display:flex;gap:16px;margin-top:8px;}
.btbt-illo-labels div{flex:1;text-align:center;font-size:11px;color:#7a7a7a;font-weight:700;}

/* Threshold meter */
.btbt-threshold-meter{display:flex;border-radius:10px;overflow:hidden;margin:20px 0 30px;height:50px;}
.btbt-th-seg{display:flex;align-items:center;justify-content:center;color:#fff;font-weight:800;font-size:14px;flex-direction:column;line-height:1.3;}
.btbt-th-good{background:#5DB92E;width:33%;}
.btbt-th-ok{background:#e2a52c;width:34%;}
.btbt-th-poor{background:#c95d5d;width:33%;}

/* Video embed */
.btbt-video-box{margin:20px 0 8px;border-radius:12px;overflow:hidden;border:1px solid #e3ede0;}
.btbt-video-wrap{position:relative;padding-bottom:56.25%;height:0;background:#000;}
.btbt-video-wrap iframe{position:absolute;top:0;left:0;width:100%;height:100%;border:0;}
.btbt-video-credit{font-size:14px;color:#7a7a7a;margin:8px 0 26px;text-align:center;}
.btbt-video-credit a{color:#5a5a5a;text-decoration:none;font-weight:600;}

/* Tabs */
.btbt-tabs{margin:20px 0 30px;}
.btbt-tab-buttons{display:flex;flex-wrap:wrap;gap:8px;border-bottom:2px solid #e3ede0;}
.btbt-tab-btn{background:#f2f5f0;border:none;border-radius:8px 8px 0 0;padding:12px 20px;font-size:17px;font-weight:700;color:#4a4a4a;cursor:pointer;font-family:'Segoe UI',Arial,sans-serif;}
.btbt-tab-btn.active{background:#5DB92E;color:#fff;}
.btbt-tab-panel{display:none;border:1px solid #e3ede0;border-top:none;border-radius:0 0 10px 10px;padding:20px;background:#fff;}
.btbt-tab-panel.active{display:block;}
.btbt-tab-panel p{margin:0 0 10px;}
.btbt-tab-panel p:last-child{margin-bottom:0;}

/* Table */
.btbt-table-wrap{overflow-x:auto;margin:20px 0 30px;}
.btbt-table{width:100%;border-collapse:collapse;font-size:17px;}
.btbt-table th{background:#2b2b2b;color:#fff;padding:13px 16px;text-align:left;font-weight:700;}
.btbt-table td{padding:13px 16px;border-bottom:1px solid #e3ede0;}
.btbt-table tr:nth-child(even) td{background:#f7faf5;}

/* Interactive calculator */
.btbt-calc{border-radius:16px;overflow:hidden;border:1px solid #e3ede0;margin:20px 0 32px;}
.btbt-calc-header{background:#2b2b2b;color:#fff;padding:18px 22px;}
.btbt-calc-header h3{margin:0 0 4px;font-size:19px;color:#fff;}
.btbt-calc-header p{margin:0;font-size:14px;color:#c7d9c0;}
.btbt-calc-body{padding:22px;background:#fff;}
.btbt-calc-row{display:flex;gap:14px;align-items:center;padding:10px 0;border-bottom:1px solid #f0f2f0;flex-wrap:wrap;}
.btbt-calc-row:last-of-type{border-bottom:none;}
.btbt-calc-row label{font-size:15px;font-weight:700;color:#2b2b2b;width:220px;flex-shrink:0;}
.btbt-calc-row input{flex:1;min-width:100px;padding:8px 10px;border-radius:8px;border:1px solid #e3ede0;font-size:14px;color:#3a3a3a;font-family:'Segoe UI',Arial,sans-serif;background:#f7faf5;}
.btbt-calc-btn{background:#5DB92E;color:#fff;border:none;padding:10px 20px;border-radius:8px;font-weight:700;font-size:15px;cursor:pointer;font-family:'Segoe UI',Arial,sans-serif;margin-top:8px;}
.btbt-calc-result{margin-top:18px;background:#f7faf5;border:1px solid #e3ede0;border-radius:10px;padding:18px;}
.btbt-calc-result-num{font-size:26px;font-weight:800;color:#3f9421;margin-bottom:4px;text-align:center;}
.btbt-calc-result p{margin:0;font-size:14px;color:#4a4a4a;text-align:center;}

/* FAQ */
.btbt-faq-item{margin-bottom:14px;}
.btbt-faq-q{background:#f2f5f0;border-radius:8px 8px 0 0;padding:14px 18px;font-weight:700;color:#2b2b2b;font-size:17px;}
.btbt-faq-a{background:#fff;border:1px solid #eef1ec;border-top:none;border-radius:0 0 8px 8px;padding:16px 18px;font-size:17px;color:#4a4a4a;}

/* Related */
.btbt-related-box{background:#f7faf5;border:1px solid #e3ede0;border-radius:12px;padding:22px;margin:20px 0 30px;}
.btbt-related-box h3{margin:0 0 12px;color:#2b2b2b;}
.btbt-related-box ul{margin:0;padding-left:20px;}
.btbt-related-box li{margin-bottom:10px;}
.btbt-related-box a{font-weight:600 !important;}

/* What we learn today - NEW: horizontal progress-track with milestone flags */
.btbt-learn{margin:26px 0 20px;}
.btbt-learn h3{font-size:20px;color:#2b2b2b;margin:0 0 18px;text-align:center;}
.btbt-learn-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;}
.btbt-learn-card{background:#f7faf5;border-left:4px solid #5DB92E;border-radius:0 8px 8px 0;padding:12px 16px;}
.btbt-learn-card p{margin:0;font-size:15px;color:#3a3a3a;}
@media(max-width:820px){.btbt-learn-grid{grid-template-columns:1fr;}}
</style>

<div class="btbt-meta-row">
<span class="btbt-meta-pill">Technical SEO</span>
<span class="btbt-meta-pill">TBT</span>
<span class="btbt-meta-pill">Page Speed</span>
<span class="btbt-meta-pill">Lighthouse</span>
</div>

<p class="btbt-lede">TBT carries more weight in your Lighthouse score than any other single metric, roughly 30%, yet most website owners have never heard of it. If your page looks fully loaded but clicks seem to do nothing for a moment, this is almost always the metric responsible, and it is measured in a genuinely simple, checkable way.</p>

<p>Total Blocking Time, or TBT, measures the total amount of time between First Contentful Paint and Time to Interactive during which the browser's main thread is blocked by tasks longer than 50 milliseconds, preventing it from responding to clicks, taps, or typing.</p>

<p>We covered the real-user counterpart to this metric in our <a href="/interaction-to-next-paint-inp-explained/" target="_blank" rel="noopener">INP guide</a>. TBT is the lab-based proxy for INP, useful specifically because INP is much harder to measure before a site is live.</p>

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


<div class="btbt-stat-grid">
<div class="btbt-stat-card"><div class="btbt-stat-num">30%</div><p>weight TBT carries in the overall Lighthouse performance score, the highest of any metric</p></div>
<div class="btbt-stat-card"><div class="btbt-stat-num">50ms</div><p>is the threshold a task must exceed before it starts counting toward this metric</p></div>
<div class="btbt-stat-card"><div class="btbt-stat-num">200ms</div><p>or less is Google's recommended target on average mobile hardware</p></div>
</div>

<h2 id="how-tbt-is-actually-calculated">How TBT Is Actually Calculated</h2>
<p>The formula is simpler than it sounds. For every long task, only the portion beyond the first 50 milliseconds counts.</p>

<div class="btbt-illo">
<div class="btbt-illo-bars">
<div class="btbt-illo-threshold"><span>50ms threshold</span></div>
<div class="btbt-illo-bar" style="height:100%;background:#c95d5d;"><span>250ms</span></div>
<div class="btbt-illo-bar" style="height:20%;background:#5DB92E;"><span>30ms</span></div>
<div class="btbt-illo-bar" style="height:35%;background:#e2a52c;"><span>60ms</span></div>
</div>
<div class="btbt-illo-labels">
<div>Task A → 200ms blocking</div>
<div>Task B → 0ms blocking</div>
<div>Task C → 10ms blocking</div>
</div>
</div>

<p>Adding those three contributions together, 200ms plus 0ms plus 10ms, produces a total blocking time of 210ms for this example page.</p>

<h2 id="tbt-thresholds-good-needs-improvement-and-poor">TBT Thresholds: Good, Needs Improvement, and Poor</h2>
<div class="btbt-threshold-meter">
<div class="btbt-th-seg btbt-th-good">Good<br>0-200ms</div>
<div class="btbt-th-seg btbt-th-ok">Needs Work<br>200-600ms</div>
<div class="btbt-th-seg btbt-th-poor">Poor<br>600ms+</div>
</div>

<div class="btbt-video-box">
<div class="btbt-video-wrap">
<iframe src="https://www.youtube.com/embed/lEdQn2cNffU" title="How to Fix Interaction to Next Paint (INP) and Total Blocking Time (TBT) with Brian Jackson" allowfullscreen loading="lazy"></iframe>
</div>
</div>
<p class="btbt-video-credit">Video: "How to Fix Interaction to Next Paint (INP) and Total Blocking Time (TBT) with Brian Jackson" featuring Brian Jackson of Perfmatters, via The Admin Bar — credit to the original creator, via <a href="https://www.youtube.com/watch?v=lEdQn2cNffU" target="_blank" rel="noopener">YouTube</a></p>

<h2 id="why-this-metric-is-not-a-core-web-vital">Why This Metric Is Not a Core Web Vital</h2>
<p>This is a genuinely important distinction. Tap through both to see how this metric relates to the official Core Web Vitals.</p>

<div class="btbt-tabs">
<div class="btbt-tab-buttons">
<button class="btbt-tab-btn active" onclick="btbtTab(event,'btbt-lab')">Lab Metric, Not Field Data</button>
<button class="btbt-tab-btn" onclick="btbtTab(event,'btbt-inp')">Its Relationship to INP</button>
</div>
<div id="btbt-lab" class="btbt-tab-panel active">
<p>According to <a href="https://web.dev/articles/tbt" target="_blank" rel="noopener">web.dev's official documentation</a>, this metric is a lab-only measurement calculated by Lighthouse during a simulated page load. It is not available in CrUX field data at all, unlike LCP, INP, and CLS.</p>
</div>
<div id="btbt-inp" class="btbt-tab-panel">
<p>A low reading here often correlates with a low INP, since both measure symptoms of the same underlying problem: a busy main thread. This makes it a useful early-warning signal before a site accumulates enough real traffic for INP field data to be meaningful.</p>
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

<h2 id="the-three-most-common-causes">The Three Most Common Causes</h2>
<div class="btbt-table-wrap">
<table class="btbt-table">
<thead>
<tr><th>Cause</th><th>Typical Impact</th></tr>
</thead>
<tbody>
<tr><td>Large JavaScript bundles</td><td>A single 500KB file can block the main thread for 1-2 seconds on mobile</td></tr>
<tr><td>Third-party scripts</td><td>Analytics, chat widgets, ad tags, and A/B testing tools frequently create long tasks</td></tr>
<tr><td>Unoptimized framework hydration</td><td>React, Vue, or Angular initial hydration can create 200ms+ long tasks on its own</td></tr>
</tbody>
</table>
</div>

<h2 id="tbt-long-task-calculator">TBT Long Task Calculator</h2>
<p>Enter the duration of up to four long tasks from your Lighthouse or DevTools performance trace to see the total.</p>

<div class="btbt-calc">
<div class="btbt-calc-header">
<h3>TBT Long Task Calculator</h3>
<p>Find task durations in Chrome DevTools' Performance panel, under the Main thread section</p>
</div>
<div class="btbt-calc-body">

<div class="btbt-calc-row">
<label>Task 1 Duration (ms)</label>
<input type="number" id="btbtTask1" value="250">
</div>
<div class="btbt-calc-row">
<label>Task 2 Duration (ms)</label>
<input type="number" id="btbtTask2" value="30">
</div>
<div class="btbt-calc-row">
<label>Task 3 Duration (ms)</label>
<input type="number" id="btbtTask3" value="60">
</div>
<div class="btbt-calc-row">
<label>Task 4 Duration (ms)</label>
<input type="number" id="btbtTask4" value="0">
</div>

<button class="btbt-calc-btn" onclick="btbtCalc()">Calculate My Total</button>

<div class="btbt-calc-result">
<div class="btbt-calc-result-num" id="btbtTotal">-- ms</div>
<p id="btbtVerdict">Enter your task durations above and click calculate.</p>
</div>

</div>
</div>

<script>
function btbtTab(evt, id){
  var panels = document.querySelectorAll('.btbt-tab-panel');
  var btns = document.querySelectorAll('.btbt-tab-btn');
  panels.forEach(function(p){p.classList.remove('active');});
  btns.forEach(function(b){b.classList.remove('active');});
  document.getElementById(id).classList.add('active');
  evt.currentTarget.classList.add('active');
}
function btbtCalc(){
  var tasks = [
    parseFloat(document.getElementById('btbtTask1').value) || 0,
    parseFloat(document.getElementById('btbtTask2').value) || 0,
    parseFloat(document.getElementById('btbtTask3').value) || 0,
    parseFloat(document.getElementById('btbtTask4').value) || 0
  ];
  var total = 0;
  tasks.forEach(function(t){
    if(t > 50){ total += (t - 50); }
  });
  document.getElementById('btbtTotal').innerText = total.toFixed(0) + ' ms';
  var verdict = document.getElementById('btbtVerdict');
  if(total <= 200){ verdict.innerText = "Good. These tasks alone keep you within the recommended range."; }
  else if(total <= 600){ verdict.innerText = "Needs improvement. Consider breaking up your largest task or deferring it."; }
  else { verdict.innerText = "Poor. Your largest tasks are likely making the page feel frozen after it loads."; }
}
</script>

<h2 id="how-to-fix-high-values-step-by-step">How to Fix High Values Step by Step</h2>
<p>According to <a href="https://www.pagespeedmatters.com/resources/glossary/total-blocking-time" target="_blank" rel="noopener">PageSpeed Matters' 2026 guide</a>, three strategies address the underlying cause directly: code-splitting so JavaScript loads on demand, breaking long tasks into smaller chunks using the scheduler.yield() API, and deferring non-critical scripts until after the user actually interacts.</p>

<p>According to <a href="https://last9.io/blog/total-blocking-time-tbt/" target="_blank" rel="noopener">Last9's guide to fixing this metric</a>, auditing third-party scripts specifically is often the fastest win, since tag managers, chat widgets, and marketing pixels frequently run unnecessary work on the main thread that the site owner never explicitly requested.</p>
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

<h2 id="why-mobile-devices-amplify-the-problem">Why Mobile Devices Amplify the Problem</h2>
<p>According to <a href="https://pagevitals.com/academy/total-blocking-time/" target="_blank" rel="noopener">PageVitals' guide for website owners</a>, mid-range phones amplify long tasks significantly, so a page that looks fine on desktop often turns out to be genuinely broken-feeling on mobile hardware.</p>

<p>Tracking deltas after every release matters more than watching the absolute number alone. A jump from 150ms to 350ms after a new tag deployment is worth investigating immediately, even if 350ms has not yet crossed into clearly poor territory.</p>

<h2 id="testing-tbt-with-real-tools">Testing TBT With Real Tools</h2>
<p>According to <a href="https://www.browserstack.com/guide/total-blocking-time-tbt" target="_blank" rel="noopener">BrowserStack's guide to minimizing TBT</a>, Lighthouse remains the most accessible way to measure it, either directly in Chrome DevTools' Lighthouse panel or through PageSpeed Insights, which runs Lighthouse automatically for any submitted URL.</p>

<p>For a more granular breakdown, Chrome DevTools' Performance panel shows every individual long task on the main thread, letting you identify exactly which script or function is responsible for a given block of blocking time, rather than relying on a single aggregated number.</p>

<p>According to <a href="https://signoz.io/guides/total-blocking-time/" target="_blank" rel="noopener">SigNoz's complete guide to TBT</a>, values below 200ms on mobile or 150ms on desktop indicate good responsiveness, with the desktop threshold being slightly stricter since desktop hardware is generally more capable.</p>

<h2 id="tbt-in-a-real-client-side-rendering-context">TBT in a Real Client-Side Rendering Context</h2>
<p>According to <a href="https://www.quattr.com/core-web-vitals/total-blocking-time-tbt" target="_blank" rel="noopener">Quattr's guide to measuring and reducing TBT</a>, single-page applications that render entirely client-side tend to show the highest values, since the browser has to download, parse, and execute a large JavaScript bundle before the page becomes interactive at all.</p>

<p>Server-side rendering or static generation avoids much of this problem by handing the browser ready-to-paint HTML upfront.</p>

<p>JavaScript in that scenario only needs to attach event handlers to already-visible content, a far smaller and faster task than building the entire page from scratch on the client.</p>

<h2 id="building-an-ongoing-monitoring-habit-for-tbt">Building an Ongoing Monitoring Habit for TBT</h2>
<p>A single audit rarely stays accurate for long. New marketing scripts, plugin updates, and growing content complexity can all quietly push a previously healthy TBT score back into problematic territory.</p>

<p>Checking Lighthouse scores as part of a pre-launch checklist for any significant site change, rather than only running a review after visitors start complaining, catches TBT regressions while they are still small and easy to isolate.</p>

<h2 id="faqs-on-total-blocking-time-tbt">FAQs on Total Blocking Time (TBT)</h2>

<div class="btbt-faq-item">
<div class="btbt-faq-q">What is a good TBT score?</div>
<div class="btbt-faq-a">Google recommends a TBT of 200 milliseconds or less on average mobile hardware. Between 200 and 600 milliseconds needs improvement, and anything above 600 milliseconds is considered poor.</div>
</div>
<div class="btbt-faq-item">
<div class="btbt-faq-q">Is TBT one of the official Core Web Vitals?</div>
<div class="btbt-faq-a">No. TBT is a lab-only metric measured by Lighthouse and other synthetic testing tools. It is not available in CrUX field data, unlike LCP, INP, and CLS.</div>
</div>
<div class="btbt-faq-item">
<div class="btbt-faq-q">What counts as a "long task"?</div>
<div class="btbt-faq-a">Any task running on the browser's main thread for longer than 50 milliseconds. Only the portion of the task beyond that 50 millisecond threshold counts toward the total.</div>
</div>
<div class="btbt-faq-item">
<div class="btbt-faq-q">What is the relationship between TBT and INP?</div>
<div class="btbt-faq-a">TBT serves as a lab-based proxy for INP, the real-user Core Web Vital that measures actual interaction responsiveness. A low reading on one often correlates with a low value on the other, since both point to main-thread congestion.</div>
</div>
<div class="btbt-faq-item">
<div class="btbt-faq-q">What is the single most common cause of a high score here?</div>
<div class="btbt-faq-a">Heavy JavaScript execution, whether from large first-party bundles or third-party scripts like analytics and chat widgets, is the most frequently cited cause across technical performance audits.</div>
</div>
<div class="btbt-faq-item">
<div class="btbt-faq-q">Why does this metric weigh so heavily in the Lighthouse score?</div>
<div class="btbt-faq-a">It accounts for roughly 30% of the overall Lighthouse performance score, more than any other individual metric, because it directly captures how frozen or unresponsive a page feels immediately after it appears to finish loading.</div>
</div>

<div class="btbt-related-box">
<h3>Related Articles</h3>
<ul>
<li><a href="/interaction-to-next-paint-inp-explained/" target="_blank" rel="noopener">Interaction to Next Paint (INP) Explained: Improve Website Responsiveness</a></li>
<li><a href="/what-is-ttfb-causes-testing-optimization/" target="_blank" rel="noopener">What Is Time to First Byte (TTFB)? Causes, Testing, and Optimization Guide</a></li>
<li><a href="/how-to-measure-core-web-vitals-tools-guide/" target="_blank" rel="noopener">How to Measure Core Web Vitals: PageSpeed Insights, Lighthouse, CrUX & Search Console</a></li>
<li><a href="/lazy-loading-images-explained-lcp-seo/" target="_blank" rel="noopener">Lazy Loading Images Explained: Best Practices That Improve LCP Without Hurting SEO</a></li>
</ul>
</div>

<div class="btbt-learn">
<h3>What We Learn Today</h3>
<div class="btbt-learn-grid">
<div class="btbt-learn-card"><p>TBT measures main-thread blocking time between FCP and TTI.</p></div>
<div class="btbt-learn-card"><p>Only the portion of a task beyond 50ms counts toward the total.</p></div>
<div class="btbt-learn-card"><p>Good is 200ms or less; poor is above 600ms.</p></div>
<div class="btbt-learn-card"><p>It carries 30% weight in Lighthouse, more than any other metric.</p></div>
<div class="btbt-learn-card"><p>It is a lab metric only; INP is the real-user equivalent.</p></div>
<div class="btbt-learn-card"><p>Large JS bundles and third-party scripts are the top causes.</p></div>
</div>
</div>

</div>
