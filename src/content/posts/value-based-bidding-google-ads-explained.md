---
title: "Value Based Bidding in Google Ads Explained"
slug: "value-based-bidding-google-ads-explained"
date: "2026-08-21T05:00:54"
updated: "2026-08-21T05:01:14"
author: "santajigade"
categories: ["google-ads"]
primaryCategory: "google-ads"
description: "Value based bidding in Google Ads explained: how tROAS differs from tCPA, the June 2026 rename, and the August 17 change to budget-limited campaigns."
focusKeyword: "Value Based Bidding"
takeaways:
  - "Value based bidding tells Google Ads what each conversion is worth, so the algorithm chases the most valuable conversions instead of the largest number of them."
  - "Starting June 2026, Google renamed its strategies to simply Target CPA and Target ROAS, and says the underlying bidding behavior is unchanged."
  - "Demand Gen campaigns need at least 50 conversions with value in the past 35 days, including a minimum of 10 in the past 7 days."
  - "Assign a distinct value to each conversion action, such as $500 for a booked demo, $200 for a free trial and $15 for a content download."
  - "Set your initial Target ROAS roughly 20% below your historical ROAS, so a 500% history means starting the target at 400%."
image: "/wp-content/uploads/2026/08/Value-Based-Bidding.webp"
imageAlt: "Value Based Bidding"
words: 1444
views: 71
format: "html"
---
<div class="bmc-flow">
<style>
@import url('https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600;700;800&display=swap');
.bmc-flow{--bx-green:#5DB92E;--bx-green-deep:#4a9e24;--bx-gold:#F4B41A;--bx-ink:#2b2b2b;--bx-steel:#5a6570;--bx-steel-2:#8a96a1;--bx-line:#E3EDE0;--bx-red:#c95d5d;--bx-disp:'Open Sans',Arial,sans-serif;--bx-body:'Open Sans',system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif;font-family:var(--bx-body);font-weight:400;font-style:normal;color:var(--bx-ink);line-height:1.75;font-size:17px;max-width:920px;margin:0 auto;padding:0;-webkit-font-smoothing:antialiased;}
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
<span class="bx-meta-pill">Paid Media</span>
<span class="bx-meta-pill">Value Based Bidding</span>
<span class="bx-meta-pill">Google Ads</span>
<span class="bx-meta-pill">2026</span>
</div>

<p class="bx-lede">Value based bidding in Google Ads means telling the algorithm what each conversion is actually worth to your business, not just how many conversions you want. Instead of "get me conversions at $80 each," you're saying "find me the conversions worth the most, and here's exactly what each type is worth."</p>

<p>The distinction matters more than it sounds. Target CPA treats a $15 newsletter signup and a $5,000 closed deal as equally worth chasing, as long as both cost roughly the same to acquire. Value based bidding tells Google to chase the deal.</p>

<p>2026 also brought real structural changes to how this works. Target CPA and Target ROAS got their standalone names back in June, and a bigger behavioral change lands August 17: budget-limited campaigns stop quietly overperforming their stated targets.</p>

<div class="bx-specs">
<div class="bx-spec"><div class="v">14%</div><div class="k">increase in conversion value documented when shifting from tCPA to tROAS</div></div>
<div class="bx-spec"><div class="v">30+</div><div class="k">conversions in 30 days typically needed before a value-based strategy can perform well</div></div>
<div class="bx-spec"><div class="v">Aug 17</div><div class="k">2026 date budget-limited tCPA/tROAS campaigns stop over-delivering past target</div></div>
</div>
<h2 id="what-it-is"><span class="bx-num">01</span>What Value Based Bidding Actually Does</h2>
<div class="bx-rule"></div>
<p><a href="https://support.google.com/google-ads/answer/15099424?hl=en" target="_blank" rel="noopener">Google's own documentation</a> defines it as a subset of Smart Bidding that optimizes campaigns based on the value a conversion brings to your business, either maximizing conversion value within budget or hitting a specific Target ROAS. That's different from conversion-based bidding, which chases volume regardless of what each conversion is actually worth.</p>

<p>CustomerLabs' guide illustrates the gap plainly: with tCPA, Google will happily bid the same $10 for a $100 signup and a $500 purchase, since both cost the same to acquire. Value based bidding is what teaches the algorithm to tell those two conversions apart.</p>

<h2 id="june-2026-rename"><span class="bx-num">02</span>The June 2026 Naming Change</h2>
<div class="bx-rule"></div>
<p>Google's own Help Center confirms the update directly: starting June 2026, "Maximize conversions with a Target CPA" reverted to simply "Target CPA," and "Maximize conversion value with a Target ROAS" became "Target ROAS." Google states plainly that the underlying bidding behavior is unchanged, this is a labeling fix, not a mechanism change.</p>

<p>Kick Ads' coverage adds useful context for why this matters visually rather than functionally: a campaign labeled "Target CPA" now signals at a glance that it's running to a target, without needing to open bid settings to confirm it.</p>

<div class="bx-note">
<span class="lbl">The August 17 Change Is the One That Actually Affects Performance</span>
<p>JumpFly's coverage flags the real behavioral shift: starting August 17, 2026, budget-limited campaigns using tCPA or tROAS get pulled closer to their literal stated target instead of quietly overperforming it. A campaign set to a $25 tCPA that's been delivering $14 conversions will get steered toward $25, not left alone at $14. Google will not adjust your targets automatically, that's a manual review you need to make yourself.</p>
</div>
<h2 id="setup-requirements"><span class="bx-num">03</span>What You Need Before Switching to Value Based Bidding</h2>
<div class="bx-rule"></div>
<p>Google's requirements are specific. For Demand Gen campaigns, you need at least 50 conversions with value in the past 35 days, including a minimum of 10 in the past 7 days, or 100 conversions with value across all Demand Gen campaigns in 35 days. For Search and Shopping value-based experiments, you need at least two unique, non-zero conversion values already being tracked.</p>

<p>Groas' 2026 Smart Bidding guide adds the practical baseline most sources converge on: aim for 30+ conversions in the last 30 days before switching, with 50+ being meaningfully more reliable. Below that, the algorithm doesn't have enough signal to learn what actually predicts value.</p>

<h2 id="setting-values"><span class="bx-num">04</span>How to Assign Conversion Values Correctly</h2>
<div class="bx-rule"></div>
<p>BrainmineTech's 2026 playbook gives a concrete example worth modeling your own account on: a SaaS company might assign $500 to a booked demo, $200 to a free trial activation, and $15 to a content download, each conversion action carrying a distinct, deliberate value rather than a flat number.</p>

<p>DeanLong's guide points to where this can go further: beyond simple revenue values, a Profit bidding approach imports the dynamic Cost of Goods Sold for each sale and bids toward actual profit margin instead of raw revenue, a more advanced setup worth growing into once basic value tracking is solid.</p>

<h2 id="troas-setup"><span class="bx-num">05</span>Setting Your Initial Target ROAS</h2>
<div class="bx-rule"></div>
<p>Google's own guidance for Demand Gen campaigns transitioning to tROAS is specific: review your campaign's actual ROAS (conversion value divided by cost) over the previous month, then set your initial target roughly 20% lower than that number. If your historical ROAS is 500%, start the target at 400% to give the campaign room to adjust during the switch.</p>

<p>Groas' guide reinforces why patience matters here: don't make bid or creative changes during the first 14 days after switching to value-based bidding. That window is when Google's AI model is training on the new signal, and interrupting it resets the calibration.</p>

<h2 id="table"><span class="bx-num">06</span>Value Based Bidding vs Conversion-Based Bidding</h2>
<div class="bx-rule"></div>
<p>A side-by-side of the core mechanical differences.</p>

<div class="bx-table-wrap">
<table class="bx-table">
<thead>
<tr><th>Factor</th><th>Target CPA / Max Conversions</th><th>Target ROAS / Max Conversion Value</th></tr>
</thead>
<tbody>
<tr><td>Optimizes for</td><td>Number of conversions</td><td>Total conversion value</td></tr>
<tr><td>Treats all conversions as</td><td>Equal, regardless of worth</td><td>Different, weighted by assigned value</td></tr>
<tr><td>Data needed</td><td>30+ conversions in 30 days</td><td>30-50+ conversions with value data</td></tr>
<tr><td>Best for</td><td>Lead gen with similar-value leads</td><td>E-commerce, variable-value conversions</td></tr>
<tr><td>June 2026 label</td><td>Target CPA (was "Maximize Conversions with target CPA")</td><td>Target ROAS (was "Maximize conversion value with target ROAS")</td></tr>
</tbody>
</table>
</div>

<h2 id="code"><span class="bx-num">07</span>Example Conversion Value Setup</h2>
<div class="bx-rule"></div>
<p>Here's what assigning distinct, deliberate conversion values looks like in practice, following the SaaS example above.</p>

<div class="bx-code">
<div class="bx-code-label">Conversion Action Values (Example)</div>
<pre>Conversion Action          |  Assigned Value  |  Why
----------------------------------------------------------
Demo booked                |  $500             |  High-intent, sales-ready lead
Free trial started         |  $200             |  Mid-funnel, needs nurturing
Content download (gated)   |  $15              |  Early-funnel, low intent signal
Newsletter signup          |  $5               |  Lowest intent, brand awareness only

// In Google Ads: Tools > Conversions > [Action] > Value
// Set "Use different values for each conversion" and
// enter these amounts per action.</pre>
</div>

<h2 id="checklist"><span class="bx-num">08</span>Implementation Checklist</h2>
<div class="bx-rule"></div>
<p>A short list before flipping the switch.</p>

<div class="bx-checklist">
<div class="bx-check-item"><div class="bx-check-icon"></div><p><strong>Confirm you have 30+ conversions</strong> in the last 30 days before attempting a value-based strategy.</p></div>
<div class="bx-check-item"><div class="bx-check-icon"></div><p><strong>Assign at least two distinct, non-zero conversion values</strong>, a flat single value defeats the purpose.</p></div>
<div class="bx-check-item"><div class="bx-check-icon"></div><p><strong>Set your initial tROAS 20% below your historical average</strong> to give the campaign room to adjust.</p></div>
<div class="bx-check-item"><div class="bx-check-icon"></div><p><strong>Don't touch bids or creative for 14 days</strong> after switching; let the model finish training.</p></div>
<div class="bx-check-item"><div class="bx-check-icon"></div><p><strong>Review budget-limited campaigns before August 17, 2026</strong>, overdelivering tCPA/tROAS campaigns will shift toward their literal stated target.</p></div>
</div>

<h2 id="score"><span class="bx-num">09</span>Are You Ready for Value Based Bidding?</h2>
<div class="bx-rule"></div>
<p>Answer a few questions about your account to check readiness.</p>

<div class="bx-calc">
<div class="bx-calc-header"><h3>Are You Ready for Value Based Bidding?</h3><p>Select the option that matches your account</p></div>
<div class="bx-calc-body">
<div class="bx-calc-factor"><div class="bx-calc-factor-top"><label>Monthly conversion volume</label><span>30 pts</span></div>
<select class="bx-calc-select" data-weight="30" onchange="bxCalc()">
<option value="0">Under 15 conversions</option>
<option value="0.5">15-30 conversions</option>
<option value="1">30+ conversions</option>
</select></div>
<div class="bx-calc-factor"><div class="bx-calc-factor-top"><label>Conversion value variability</label><span>30 pts</span></div>
<select class="bx-calc-select" data-weight="30" onchange="bxCalc()">
<option value="0">All conversions worth roughly the same</option>
<option value="0.5">Some variation</option>
<option value="1">Significant variation in value per conversion</option>
</select></div>
<div class="bx-calc-factor"><div class="bx-calc-factor-top"><label>Conversion value tracking accuracy</label><span>25 pts</span></div>
<select class="bx-calc-select" data-weight="25" onchange="bxCalc()">
<option value="0">Not tracking distinct values yet</option>
<option value="0.5">Tracking, not fully verified</option>
<option value="1">Accurate, verified value tracking in place</option>
</select></div>
<div class="bx-calc-factor"><div class="bx-calc-factor-top"><label>Budget flexibility</label><span>15 pts</span></div>
<select class="bx-calc-select" data-weight="15" onchange="bxCalc()">
<option value="0">Tightly budget-constrained</option>
<option value="1">Some flexibility to let the algorithm optimize</option>
</select></div>
<div class="bx-calc-gauge-wrap"><div class="bx-calc-gauge-track"><div class="bx-calc-gauge-fill" id="bxGaugeFill"><span id="bxGaugeScore">0%</span></div></div>
<div class="bx-calc-verdict" id="bxVerdict">Select an option for each factor to check readiness.</div></div>
</div>
</div>

<script>
function bxCalc(){var selects=document.querySelectorAll('.bx-calc-select');var total=0;selects.forEach(function(s){var weight=parseFloat(s.getAttribute('data-weight'));var value=parseFloat(s.value);total+=weight*value;});var pct=Math.round(total);document.getElementById('bxGaugeFill').style.width=pct+'%';document.getElementById('bxGaugeScore').innerText=pct+'%';var verdict=document.getElementById('bxVerdict');if(pct>=70){verdict.innerText="Ready. You have the data and value variability to make value-based bidding worthwhile.";}else if(pct>=40){verdict.innerText="Close. Build a bit more conversion volume or value tracking accuracy first.";}else{verdict.innerText="Not yet. Focus on accumulating conversions and accurate value tracking before switching.";}}
</script>

<h2 id="faq"><span class="bx-num">10</span>FAQs on Value Based Bidding</h2>
<div class="bx-rule"></div>
<div class="bx-faq" id="bxFaq">
<button class="bx-q">What's the difference between tCPA and tROAS?<span class="ic">+</span></button>
<div class="bx-a"><p>tCPA optimizes for conversion volume at a target cost. tROAS optimizes for total conversion value at a target return, treating conversions as worth different amounts.</p></div>
<button class="bx-q">Did the June 2026 rename change how bidding actually works?<span class="ic">+</span></button>
<div class="bx-a"><p>No. Google confirmed the rename from "Maximize Conversions with Target CPA" back to "Target CPA" (and the ROAS equivalent) was cosmetic only. The underlying algorithm is unchanged.</p></div>
<button class="bx-q">What is the August 17, 2026 bidding change?<span class="ic">+</span></button>
<div class="bx-a"><p>Budget-limited tCPA and tROAS campaigns will be steered to perform closer to their literal stated target instead of quietly overperforming it. Google won't adjust your targets automatically.</p></div>
<button class="bx-q">How many conversions do I need before switching to value based bidding?<span class="ic">+</span></button>
<div class="bx-a"><p>At least 30 in the last 30 days for Search and Shopping, with 50+ conversions with value data typically required for Demand Gen campaigns.</p></div>
<button class="bx-q">Can I set a negative conversion value?<span class="ic">+</span></button>
<div class="bx-a"><p>Not currently. Google Ads doesn't support negative conversion values as of 2026's documentation.</p></div>
</div>

<div class="bx-related-box">
<h3>Related Articles</h3>
<ul>
<li><a href="/enhanced-conversions-explained-setup-benefits/" target="_blank" rel="noopener">Enhanced Conversions Explained: Setup and Benefits</a></li>
<li><a href="/search-campaign-vs-performance-max/" target="_blank" rel="noopener">Search Campaign vs Performance Max</a></li>
<li><a href="/google-ads-bidding-change-target-cpa/" target="_blank" rel="noopener">Google Ads Bidding Change: Target CPA</a></li>
</ul>
</div>

<div class="bx-learn">
<h3>What We Learn Today</h3>
<div class="bx-learn-grid">
<div class="bx-learn-card"><p>Value based bidding optimizes for conversion worth, not just count</p></div>
<div class="bx-learn-card"><p>June 2026 renamed tCPA/tROAS back, with no behavior change</p></div>
<div class="bx-learn-card"><p>August 17 change stops budget-limited campaigns overdelivering</p></div>
<div class="bx-learn-card"><p>Need 30+ conversions and distinct values before switching</p></div>
<div class="bx-learn-card"><p>Set initial tROAS 20% below historical average</p></div>
<div class="bx-learn-card"><p>Don't touch bids for 14 days after switching strategies</p></div>
</div>
</div>

<section class="bx-cta">
<h2 id="build-a-complete-measurement-and-bidding-foundation">Build a Complete Measurement and Bidding Foundation</h2>
<p>Value based bidding depends on accurate conversion tracking. Explore our enhanced conversions and Performance Max guides next.</p>
<div class="bx-actions">
<a class="bx-btn primary" href="/enhanced-conversions-explained-setup-benefits/" target="_blank" rel="noopener">Enhanced Conversions Setup</a>
<a class="bx-btn ghost" href="/search-campaign-vs-performance-max/" target="_blank" rel="noopener">Search Campaign vs Performance Max</a>
</div>
</section>

</div>
<script>
(function(){var root=document.currentScript.parentNode.querySelector('.bmc-flow')||document;var qs=root.querySelectorAll('#bxFaq .bx-q');qs.forEach(function(q){q.addEventListener('click',function(){var a=q.nextElementSibling,open=q.classList.contains('on');qs.forEach(function(x){x.classList.remove('on');x.nextElementSibling.classList.remove('on');});if(!open){q.classList.add('on');a.classList.add('on');}});});})();
</script>
