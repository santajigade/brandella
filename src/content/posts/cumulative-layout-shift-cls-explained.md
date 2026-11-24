---
title: "Cumulative Layout Shift (CLS) Explained: Fix Unexpected Layout Shifts for Better SEO"
slug: "cumulative-layout-shift-cls-explained"
date: "2026-07-29T02:57:44"
updated: "2026-08-09T08:40:11"
author: "santajigade"
categories: ["core-web-vitals", "seo"]
primaryCategory: "seo"
description: "Learn what Cumulative Layout Shift (CLS) is, why it matters for Core Web Vitals, what causes unexpected layout shifts, and how to fix CLS issues"
focusKeyword: "Cumulative Layout Shift"
takeaways:
  - "Cumulative Layout Shift (CLS) measures how much visible content unexpectedly moves while a page loads."
  - "A CLS score of 0.1 or less is good, 0.1 to 0.25 needs improvement and above 0.25 is poor."
  - "Images without width and height attributes are the most common cause of layout shifts."
  - "Reserve space for ads, embeds and late loading banners so they cannot push content down."
  - "Test CLS on mobile as well as desktop, because shifts usually look worse on small screens."
image: "/wp-content/uploads/2026/07/Cumulative-Layout-Shift.webp"
imageAlt: "Cumulative Layout Shift"
words: 1696
views: 116
format: "html"
---
<div class="bcl-wrap">
<style>
.bcl-wrap{font-family:'Segoe UI', Arial, sans-serif;font-size:17px;line-height:1.75;color:#2e2e2e;max-width:100%;}
.bcl-wrap h2{font-size:25px;color:#2b2b2b;margin:36px 0 16px;font-weight:800;border-left:5px solid #5DB92E;padding-left:14px;}
.bcl-wrap h3{font-size:19px;color:#2b2b2b;margin:18px 0 10px;font-weight:700;}
.bcl-wrap p{margin:0 0 14px;font-size:17px;}
.bcl-wrap a{color:#3f9421;font-weight:600;text-decoration:none;}
.bcl-wrap a:hover{color:#2f7418;text-decoration:none;}
.bcl-wrap ul,.bcl-wrap ol{margin:0 0 16px;padding-left:22px;}
.bcl-wrap li{margin-bottom:8px;font-size:17px;}

.bcl-lede{font-size:20px;color:#333;font-style:italic;margin:0 0 18px;line-height:1.6;border-left:3px solid #5DB92E;padding-left:16px;}

.bcl-meta-row{display:flex;flex-wrap:wrap;gap:10px;margin:0 0 24px;}
.bcl-meta-pill{background:#eef8e8;color:#3f9421;border:1px solid #cdeabb;border-radius:20px;padding:6px 16px;font-size:13px;font-weight:700;text-transform:uppercase;letter-spacing:.5px;}

/* Stat cards */
.bcl-stat-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin:20px 0 30px;}
.bcl-stat-card{background:#f7faf5;border:1px solid #e3ede0;border-radius:12px;padding:22px 16px;text-align:center;}
.bcl-stat-num{font-size:32px;font-weight:800;color:#5DB92E;margin-bottom:6px;}
.bcl-stat-card p{margin:0;font-size:17px;color:#4a4a4a;}
@media(max-width:820px){.bcl-stat-grid{grid-template-columns:1fr;}}

/* Layout shift before/after illustration */
.bcl-illo{margin:20px 0 30px;background:#fff;border:1px solid #e3ede0;border-radius:14px;padding:24px 22px;display:grid;grid-template-columns:1fr 1fr;gap:20px;}
.bcl-illo-col{text-align:center;}
.bcl-illo-label{font-size:13px;font-weight:800;color:#7a7a7a;text-transform:uppercase;letter-spacing:.5px;margin-bottom:10px;}
.bcl-illo-page{border:1px solid #e3ede0;border-radius:8px;padding:14px;background:#f7faf5;}
.bcl-illo-bar{height:8px;border-radius:3px;background:#e8ece7;margin-bottom:8px;}
.bcl-illo-bar.short{width:60%;}
.bcl-illo-btn{display:inline-block;background:#5DB92E;color:#fff;font-size:12px;font-weight:700;padding:6px 14px;border-radius:5px;margin-top:6px;}
.bcl-illo-gap{height:24px;background:repeating-linear-gradient(45deg,#faf0da,#faf0da 4px,#fff8ea 4px,#fff8ea 8px);border-radius:4px;margin:8px 0;font-size:10px;color:#b5771e;display:flex;align-items:center;justify-content:center;}
@media(max-width:820px){.bcl-illo{grid-template-columns:1fr;}}

/* Threshold meter */
.bcl-threshold{display:flex;border-radius:10px;overflow:hidden;margin:20px 0 30px;height:50px;}
.bcl-th-seg{display:flex;align-items:center;justify-content:center;color:#fff;font-weight:800;font-size:14px;flex-direction:column;line-height:1.3;}
.bcl-th-good{background:#5DB92E;width:40%;}
.bcl-th-ok{background:#e2a52c;width:35%;}
.bcl-th-poor{background:#c95d5d;width:25%;}

/* Numbered factors */
.bcl-factors{display:flex;flex-direction:column;gap:14px;margin:20px 0 30px;}
.bcl-factor{display:flex;gap:16px;background:#fff;border:1px solid #e3ede0;border-radius:12px;padding:18px 20px;align-items:flex-start;}
.bcl-factor-num{width:36px;height:36px;border-radius:50%;background:#5DB92E;color:#fff;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:17px;flex-shrink:0;}
.bcl-factor h3{margin:0 0 6px;font-size:17px;}
.bcl-factor p{margin:0;font-size:17px;color:#4a4a4a;}

/* Tabs */
.bcl-tabs{margin:20px 0 30px;}
.bcl-tab-buttons{display:flex;flex-wrap:wrap;gap:8px;border-bottom:2px solid #e3ede0;}
.bcl-tab-btn{background:#f2f5f0;border:none;border-radius:8px 8px 0 0;padding:12px 20px;font-size:17px;font-weight:700;color:#4a4a4a;cursor:pointer;font-family:'Segoe UI',Arial,sans-serif;}
.bcl-tab-btn.active{background:#5DB92E;color:#fff;}
.bcl-tab-panel{display:none;border:1px solid #e3ede0;border-top:none;border-radius:0 0 10px 10px;padding:20px;background:#fff;}
.bcl-tab-panel.active{display:block;}
.bcl-tab-panel p{margin:0 0 10px;}
.bcl-tab-panel p:last-child{margin-bottom:0;}

/* Table */
.bcl-table-wrap{overflow-x:auto;margin:20px 0 30px;}
.bcl-table{width:100%;border-collapse:collapse;font-size:17px;}
.bcl-table th{background:#2b2b2b;color:#fff;padding:13px 16px;text-align:left;font-weight:700;}
.bcl-table td{padding:13px 16px;border-bottom:1px solid #e3ede0;}
.bcl-table tr:nth-child(even) td{background:#f7faf5;}

/* Interactive checklist widget */
.bcl-check{border-radius:14px;overflow:hidden;border:1px solid #e3ede0;margin:20px 0 32px;}
.bcl-check-header{background:#2b2b2b;color:#fff;padding:16px 22px;font-weight:700;font-size:17px;}
.bcl-check-body{padding:22px;background:#fff;}
.bcl-check-item{display:flex;align-items:flex-start;gap:12px;padding:10px 0;border-bottom:1px solid #f0f2f0;cursor:pointer;}
.bcl-check-item:last-of-type{border-bottom:none;}
.bcl-check-item input{margin-top:4px;width:18px;height:18px;accent-color:#5DB92E;flex-shrink:0;}
.bcl-check-item span{font-size:17px;color:#3a3a3a;}
.bcl-check-result{margin-top:16px;background:#f7faf5;border:1px solid #e3ede0;border-radius:10px;padding:16px 18px;font-size:17px;font-weight:700;color:#2b2b2b;text-align:center;}

/* FAQ */
.bcl-faq-item{margin-bottom:14px;}
.bcl-faq-q{background:#f2f5f0;border-radius:8px 8px 0 0;padding:14px 18px;font-weight:700;color:#2b2b2b;font-size:17px;}
.bcl-faq-a{background:#fff;border:1px solid #eef1ec;border-top:none;border-radius:0 0 8px 8px;padding:16px 18px;font-size:17px;color:#4a4a4a;}

/* Related */
.bcl-related-box{background:#f7faf5;border:1px solid #e3ede0;border-radius:12px;padding:22px;margin:20px 0 30px;}
.bcl-related-box h3{margin:0 0 12px;color:#2b2b2b;}
.bcl-related-box ul{margin:0;padding-left:20px;}
.bcl-related-box li{margin-bottom:10px;}
.bcl-related-box a{font-weight:600 !important;}

/* What we learn today - 23rd distinct style: stacked ribbon cards with corner fold effect */
.bcl-learn{margin:26px 0 20px;}
.bcl-learn h3{font-size:20px;color:#2b2b2b;margin:0 0 18px;text-align:center;}
.bcl-learn-grid{display:grid;grid-template-columns:1fr 1fr;gap:14px;}
.bcl-learn-card{position:relative;background:#f7faf5;border:1px solid #e3ede0;border-radius:0 10px 10px 10px;padding:16px 18px 16px 20px;}
.bcl-learn-card::before{content:'';position:absolute;top:0;left:0;width:0;height:0;border-style:solid;border-width:0 16px 16px 0;border-color:transparent #5DB92E transparent transparent;}
.bcl-learn-card p{margin:0;font-size:15px;color:#3a3a3a;font-weight:600;padding-top:6px;}
@media(max-width:820px){.bcl-learn-grid{grid-template-columns:1fr;}}
</style>

<div class="bcl-meta-row">
<span class="bcl-meta-pill">Technical SEO</span>
<span class="bcl-meta-pill">CLS</span>
<span class="bcl-meta-pill">Core Web Vitals</span>
<span class="bcl-meta-pill">Visual Stability</span>
</div>

<p class="bcl-lede">A visitor reaches for the "Submit" button on a lead form. A late-loading promo banner shoves it down half a second before the tap lands, and they hit a blank space instead, or worse, an ad. That single moment is what Cumulative Layout Shift measures, and it is quietly costing sites real conversions, not just Core Web Vitals points.</p>

<p>Cumulative Layout Shift measures how much visible content moves unexpectedly during a page's entire lifespan, not just while it loads. Every unplanned jump, whether from a late image, an injected banner, or a font swap, adds to the score.</p>

<p>We covered CLS alongside LCP and INP in our <a href="/core-web-vitals-2026/" target="_blank" rel="noopener">Core Web Vitals overview</a>, and went deep on the other two in our <a href="/what-is-largest-contentful-paint-lcp/" target="_blank" rel="noopener">LCP guide</a> and <a href="/interaction-to-next-paint-inp-explained/" target="_blank" rel="noopener">INP guide</a>. This article completes the set.</p>

<div class="bcl-stat-grid">
<div class="bcl-stat-card"><div class="bcl-stat-num">0.1</div><p>or lower is a good CLS score, measured at the 75th percentile of page visits</p></div>
<div class="bcl-stat-card"><div class="bcl-stat-num">62%</div><p>of mobile pages still ship at least one image with no reserved dimensions</p></div>
<div class="bcl-stat-card"><div class="bcl-stat-num">8-14%</div><p>typical bounce rate reduction reported after fixing a site from poor to good CLS</p></div>
</div>

<h2 id="what-a-layout-shift-actually-looks-like">What a Layout Shift Actually Looks Like</h2>
<p>Picture the same page loading two different ways.</p>

<div class="bcl-illo">
<div class="bcl-illo-col">
<div class="bcl-illo-label">Unstable Layout</div>
<div class="bcl-illo-page">
<div class="bcl-illo-bar"></div>
<div class="bcl-illo-bar short"></div>
<div class="bcl-illo-btn">Submit</div>
<div class="bcl-illo-gap">banner loads here ↑</div>
</div>
</div>
<div class="bcl-illo-col">
<div class="bcl-illo-label">Stable Layout</div>
<div class="bcl-illo-page">
<div class="bcl-illo-gap">space reserved ↓</div>
<div class="bcl-illo-bar"></div>
<div class="bcl-illo-bar short"></div>
<div class="bcl-illo-btn">Submit</div>
</div>
</div>
</div>

<h2 id="cls-thresholds-good-needs-improvement-and-poor">CLS Thresholds: Good, Needs Improvement, and Poor</h2>
<div class="bcl-threshold">
<div class="bcl-th-seg bcl-th-good">Good<br>0-0.1</div>
<div class="bcl-th-seg bcl-th-ok">Needs Work<br>0.1-0.25</div>
<div class="bcl-th-seg bcl-th-poor">Poor<br>0.25+</div>
</div>

<h2 id="how-a-cls-score-is-actually-calculated">How a CLS Score Is Actually Calculated</h2>
<p>CLS is unitless, which confuses a lot of people the first time they see it.</p>

<p>According to <a href="https://parachutedesign.ca/blog/cumulative-layout-shift-cls/" target="_blank" rel="noopener">Parachute Design's 2026 CLS guide</a>, the browser calculates each individual shift by multiplying two components: impact fraction, how much of the viewport was affected, and distance fraction, how far the elements actually moved.</p>

<p>These individual shift scores accumulate within session windows, groups of rapid shifts occurring within one second of each other, capped at five seconds total. The single highest-scoring session window becomes your page's CLS value, not a simple sum of every shift that ever happened.</p>

<h2 id="five-common-causes-of-poor-cls">Five Common Causes of Poor CLS</h2>
<div class="bcl-factors">
<div class="bcl-factor">
<div class="bcl-factor-num">1</div>
<div>
<h3>Images Without Width and Height Attributes</h3>
<p>According to <a href="https://sproutsagesolutions.com/cumulative-layout-shift-fix/" target="_blank" rel="noopener">Sprout Sage Solutions' 2026 CLS guide</a>, this is the single biggest CLS offender. Without explicit dimensions, the browser has no way to reserve space before the image finishes loading.</p>
</div>
</div>
<div class="bcl-factor">
<div class="bcl-factor-num">2</div>
<div>
<h3>Ads and Embeds With No Reserved Space</h3>
<p>Dynamic ad slots and third-party embeds that inject content after the initial layout renders are a frequent, hard-to-predict source of shifting, especially on ad-supported pages.</p>
</div>
</div>
<div class="bcl-factor">
<div class="bcl-factor-num">3</div>
<div>
<h3>Web Fonts Swapping Late</h3>
<p>According to <a href="https://logoswebdesigns.com/blog/how-to-fix-cumulative-layout-shift-2026/" target="_blank" rel="noopener">Logos Web Designs' 2026 CLS guide</a>, only about 11% of pages preload their web fonts, and a late font swap can noticeably resize text and push surrounding content.</p>
</div>
</div>
<div class="bcl-factor">
<div class="bcl-factor-num">4</div>
<div>
<h3>Cookie Banners and Injected Notices</h3>
<p>A consent banner that appears at the top of the viewport after the page has already rendered pushes everything below it down, a shift many sites never test for since it happens so early.</p>
</div>
</div>
<div class="bcl-factor">
<div class="bcl-factor-num">5</div>
<div>
<h3>Animating the Wrong CSS Properties</h3>
<p>Animating properties like top, left, width, or height triggers layout recalculation and counts toward CLS. Animating transform and opacity instead avoids this entirely.</p>
</div>
</div>
</div>

<h2 id="expected-vs-unexpected-shifts-what-actually-counts">Expected vs. Unexpected Shifts: What Actually Counts</h2>
<p>Not every layout change counts against your CLS score. Tap through both categories to see the distinction.</p>

<div class="bcl-tabs">
<div class="bcl-tab-buttons">
<button class="bcl-tab-btn active" onclick="bclTab(event,'bcl-unexpected')">Unexpected Shifts (Count)</button>
<button class="bcl-tab-btn" onclick="bclTab(event,'bcl-expected')">Expected Shifts (Excluded)</button>
</div>
<div id="bcl-unexpected" class="bcl-tab-panel active">
<p>A late-loading image pushing text down, a banner injecting itself above existing content, or a font swap resizing a headline are all unexpected shifts, since the user did nothing to trigger them.</p>
</div>
<div id="bcl-expected" class="bcl-tab-panel">
<p>According to Parachute Design's guide referenced above, any shift occurring within 500 milliseconds of user input is excluded from CLS calculations. Clicking an accordion to expand it, or tapping a button that intentionally reveals more content, does not count against your score.</p>
</div>
</div>
<h2 id="how-cls-is-measured-across-impact-and-distance">How CLS Is Measured Across Impact and Distance</h2>
<div class="bcl-table-wrap">
<table class="bcl-table">
<thead>
<tr><th>Factor</th><th>What It Measures</th><th>Example</th></tr>
</thead>
<tbody>
<tr><td>Impact fraction</td><td>How much of the viewport was affected by the shift</td><td>A banner covering half the visible screen scores higher than a small icon</td></tr>
<tr><td>Distance fraction</td><td>How far the shifted elements actually moved</td><td>Content moving 300px scores higher than content moving 20px</td></tr>
<tr><td>Session window</td><td>Groups rapid shifts within 1 second, capped at 5 seconds</td><td>Several small shifts in quick succession combine into one window score</td></tr>
</tbody>
</table>
</div>

<div class="bcl-check">
<div class="bcl-check-header">Quick Check: Is Your Site Likely Failing CLS?</div>
<div class="bcl-check-body">
<label class="bcl-check-item"><input type="checkbox" onchange="bclCheck()"><span>Some images on my site do not have explicit width and height set.</span></label>
<label class="bcl-check-item"><input type="checkbox" onchange="bclCheck()"><span>I run ads, embeds, or a cookie banner that could inject content late.</span></label>
<label class="bcl-check-item"><input type="checkbox" onchange="bclCheck()"><span>I have noticed text or buttons jump slightly while a page is loading.</span></label>
<label class="bcl-check-item"><input type="checkbox" onchange="bclCheck()"><span>I have not checked my CLS score in Search Console or PageSpeed Insights recently.</span></label>
<div id="bcl-check-result" class="bcl-check-result">Check the boxes that apply to see how likely CLS is a problem for you.</div>
</div>
</div>

<script>
function bclTab(evt, id){
  var panels = document.querySelectorAll('.bcl-tab-panel');
  var btns = document.querySelectorAll('.bcl-tab-btn');
  panels.forEach(function(p){p.classList.remove('active');});
  btns.forEach(function(b){b.classList.remove('active');});
  document.getElementById(id).classList.add('active');
  evt.currentTarget.classList.add('active');
}
function bclCheck(){
  var boxes = document.querySelectorAll('.bcl-check-item input');
  var count = 0;
  boxes.forEach(function(b){ if(b.checked) count++; });
  var msg = "Check the boxes that apply to see how likely CLS is a problem for you.";
  if(count >= 3){ msg = "High likelihood. Start by adding width and height to every image this week."; }
  else if(count == 2){ msg = "Worth a quick audit. Check your CLS score in PageSpeed Insights soon."; }
  else if(count == 1){ msg = "Probably in decent shape, but a periodic check is still worthwhile."; }
  document.getElementById('bcl-check-result').innerText = msg;
}
</script>

<h2 id="how-to-fix-the-most-common-cls-problems">How to Fix the Most Common CLS Problems</h2>
<p>Start with images, since they are the most common and easiest fix. Add explicit width and height attributes, or a CSS aspect-ratio value, to every image, ad slot, and embed on the page so the browser reserves the correct space before content arrives.</p>

<p>For fonts, according to <a href="https://logoswebdesigns.com/blog/how-to-fix-cumulative-layout-shift-2026/" target="_blank" rel="noopener">Logos Web Designs' guide</a>, using font-display: optional rather than swap, paired with size-adjust overrides, can eliminate font-swap shifts entirely rather than just reducing them.</p>

<p>For ads, embeds, and cookie banners, reserve a fixed-height container in the layout from the very first paint, even before the actual content has loaded into it.</p>

<p>According to <a href="https://www.corewebvitals.io/core-web-vitals/largest-contentful-paint" target="_blank" rel="noopener">CoreWebVitals.io's broader Core Web Vitals reference</a>, this same reserve-space principle applies across all dynamic content types, not just images, so nothing needs to move once it arrives.</p>

<h2 id="common-cls-mistakes-that-undo-good-fixes">Common CLS Mistakes That Undo Good Fixes</h2>
<p>The most common mistake is fixing images but ignoring third-party embeds and ad slots, which often cause the largest individual shifts on a page even when every first-party image is properly sized.</p>

<p>A second mistake, according to <a href="https://ondigitals.com/cumulative-layout-shift/" target="_blank" rel="noopener">OnDigitals' 2026 CLS guide</a>, is relying only on the PageSpeed Insights score without investigating which specific element is actually shifting, since the number alone can hide the real underlying issue on pages with complex, dynamic content.</p>

<p>A third mistake is treating a "good" CLS score as permanent. According to <a href="https://techmarg.in/blog/eliminating-layout-shifts-a-deep-dive-into-cumulative-layout-shift-cls/" target="_blank" rel="noopener">TechMarg's deep dive into CLS</a>, new content additions, plugin updates, or design changes can quietly reintroduce shifts that were fixed months earlier, so periodic rechecks matter as much as the initial fix.</p>

<h2 id="why-cls-still-matters-alongside-lcp-and-inp">Why CLS Still Matters Alongside LCP and INP</h2>
<p>A page that loads fast and responds instantly can still feel broken if content keeps jumping around underneath the visitor's cursor.</p>

<p>Google treats all three Core Web Vitals as one connected page experience signal, the same way it treats <a href="/what-is-schema-markup/" target="_blank" rel="noopener">schema markup</a> and <a href="/crawl-budget-explained/" target="_blank" rel="noopener">crawl budget</a> as pieces of one larger technical health picture, not isolated boxes to check off separately.</p>
<h2 id="why-cls-damages-conversions-more-than-it-damages-rankings">Why CLS Damages Conversions More Than It Damages Rankings</h2>
<p>The SEO impact of CLS is real but modest. The conversion impact is often larger and more immediate, since a shifting layout directly interferes with the moment a visitor decides to act.</p>

<p>According to <a href="https://whitelabelseoservice.com/cls-optimization-guide/" target="_blank" rel="noopener">White Label SEO Service's CLS optimization guide</a>, visitors who abandon a form mid-completion or click the wrong button because of a layout shift rarely come back to try again.</p>

<p>The lost conversion happens instantly, while the ranking penalty, if any, unfolds far more gradually.</p>

<p>This is especially costly on high-intent pages like checkout flows, lead forms, and pricing pages, where a single misplaced tap can end a conversion that would otherwise have completed successfully.</p>

<h2 id="testing-for-cls-on-mobile-not-just-desktop">Testing for CLS on Mobile, Not Just Desktop</h2>
<p>Layout shifts often show up more severely on mobile, since smaller viewports mean the same absolute pixel movement represents a larger share of what the user can actually see.</p>

<p>According to <a href="https://ondigitals.com/cumulative-layout-shift/" target="_blank" rel="noopener">OnDigitals' CLS guide</a>, ads, embeds, and review widgets that arrive after the first paint create disproportionately large shifts on mobile screens compared to how the same elements behave on a wider desktop layout.</p>

<p>Testing exclusively on a desktop browser during development is a common reason CLS problems go unnoticed until real mobile users start experiencing them, since the visual proportions genuinely differ between the two environments.</p>

<h2 id="faqs-on-cumulative-layout-shift-cls">FAQs on Cumulative Layout Shift (CLS)</h2>

<div class="bcl-faq-item">
<div class="bcl-faq-q">What is a good CLS score?</div>
<div class="bcl-faq-a">Google considers a CLS of 0.1 or lower, at the 75th percentile of page visits, to be good. Between 0.1 and 0.25 needs improvement, and anything above 0.25 is considered poor.</div>
</div>
<div class="bcl-faq-item">
<div class="bcl-faq-q">Does clicking a button that changes the layout count against my CLS score?</div>
<div class="bcl-faq-a">No, as long as the shift happens within 500 milliseconds of the user's input. Google excludes these expected, user-triggered shifts from the CLS calculation entirely.</div>
</div>
<div class="bcl-faq-item">
<div class="bcl-faq-q">What is the single biggest cause of poor CLS?</div>
<div class="bcl-faq-a">Images without explicit width and height attributes are the most commonly cited cause, since the browser has no way to reserve the correct amount of space before the image finishes loading.</div>
</div>
<div class="bcl-faq-item">
<div class="bcl-faq-q">How is CLS different from LCP and INP?</div>
<div class="bcl-faq-a">LCP measures loading speed and INP measures responsiveness to interaction. CLS measures visual stability, specifically how much visible content moves unexpectedly, whether during loading or later in a session.</div>
</div>
<div class="bcl-faq-item">
<div class="bcl-faq-q">Can ads and third-party embeds hurt my CLS score?</div>
<div class="bcl-faq-a">Yes, significantly. Ads, embeds, and injected banners that load after the initial layout renders are among the most common and hardest-to-predict sources of poor CLS, especially on ad-supported pages.</div>
</div>
<div class="bcl-faq-item">
<div class="bcl-faq-q">Does fixing CLS actually improve conversions, not just SEO?</div>
<div class="bcl-faq-a">Yes. Reported case studies commonly show bounce rate reductions of 8 to 14% and conversion rate increases after moving a page from a poor CLS score to a good one, independent of any ranking benefit.</div>
</div>

<div class="bcl-related-box">
<h3>Related Articles</h3>
<ul>
<li><a href="/core-web-vitals-2026/" target="_blank" rel="noopener">Core Web Vitals in 2026: What Actually Changed and What Still Matters</a></li>
<li><a href="/what-is-largest-contentful-paint-lcp/" target="_blank" rel="noopener">What Is Largest Contentful Paint (LCP)? How to Diagnose and Fix It</a></li>
<li><a href="/interaction-to-next-paint-inp-explained/" target="_blank" rel="noopener">Interaction to Next Paint (INP) Explained: Improve Website Responsiveness</a></li>
<li><a href="/crawl-budget-explained/" target="_blank" rel="noopener">Crawl Budget Explained: Why Google Might Be Ignoring Half Your Site</a></li>
</ul>
</div>

<div class="bcl-learn">
<h3>What We Learn Today</h3>
<div class="bcl-learn-grid">
<div class="bcl-learn-card"><p>CLS measures unexpected visual movement, not just during loading but the whole visit.</p></div>
<div class="bcl-learn-card"><p>A good CLS score is 0.1 or lower, measured at the 75th percentile of visits.</p></div>
<div class="bcl-learn-card"><p>Unsized images are the single biggest, most common cause of poor CLS.</p></div>
<div class="bcl-learn-card"><p>Shifts within 500ms of user input are excluded from the score entirely.</p></div>
<div class="bcl-learn-card"><p>Reserving space for ads, embeds, and fonts prevents most shifts before they happen.</p></div>
<div class="bcl-learn-card"><p>Fixing CLS improves conversions directly, not just search rankings.</p></div>
</div>
</div>

</div>
