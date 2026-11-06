---
title: "Google Ads Audience Signals Explained: Signals vs Targeting"
slug: "google-ads-audience-signals-explained"
date: "2026-08-21T05:06:25"
updated: "2026-08-21T05:08:17"
author: "santajigade"
categories: ["google-ads"]
primaryCategory: "google-ads"
description: "Google Ads audience signals explained simply: how they differ from targeting, how PMax vs Demand Gen treat them, and the March 2026 Lookalike change."
focusKeyword: "Audience Signals"
image: "/wp-content/uploads/2026/08/Audience-Signals.webp"
imageAlt: "Audience Signals"
words: 1088
views: 65
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
<span class="bx-meta-pill">Audience Signals</span>
<span class="bx-meta-pill">Google Ads</span>
<span class="bx-meta-pill">2026</span>
</div>

<p class="bx-lede">Audience signals are hints, not orders. You tell Google's AI who your best customers tend to look like. The algorithm takes that hint and goes looking for more people like them, even ones outside your original list.</p>

<p>Think of it like giving someone directions to your house. You mention the neighborhood and a landmark. They still find their own way there.</p>

<p>That's the shift worth understanding in 2026. Keywords used to be the main lever. Now, audience signals are just as important, sometimes more.</p>

<div class="bx-specs">
<div class="bx-spec"><div class="v">45%</div><div class="k">of all Google Ads conversions now come through Performance Max, where signals matter most</div></div>
<div class="bx-spec"><div class="v">2 weeks</div><div class="k">typical time for Google's AI to fully integrate a new audience signal</div></div>
<div class="bx-spec"><div class="v">7</div><div class="k">core audience segment types available across Google Ads in 2026</div></div>
</div>

<!-- OPENING ADSENSE CODE -->
<div class="bx-ad-wrap">
<div class="bx-ad-divider" style="margin-bottom:20px;"><div class="bx-ad-line"></div><span>Advertisement</span><div class="bx-ad-line"></div></div>
<ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-3931314195561246" data-ad-slot="4249015278" data-ad-format="auto" data-full-width-responsive="true"></ins>
<script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
<div class="bx-ad-divider" style="margin-top:20px;"><div class="bx-ad-line"></div><span>Advertisement</span><div class="bx-ad-line"></div></div>
</div>
<!-- CLOSING ADSENSE CODE -->

<h2 id="signals-vs-targeting"><span class="bx-num">01</span>Audience Signals vs Audience Targeting</h2>
<div class="bx-rule"></div>
<p>These two terms get mixed up constantly. They mean very different things.</p>

<p>Targeting is a wall. "Only show my ads to these people." Nobody outside that group sees your ad.</p>

<p>Signals are a nudge. "Here's who I think converts best." Google can still show ads to people outside that group if it finds a good reason to.</p>

<p>Mind Over Maze's guide sums it up in one line worth remembering: targeting locks you in, signals give the AI room to explore.</p>

<h2 id="quick-visual"><span class="bx-num">02</span>The Simple Version</h2>
<div class="bx-rule"></div>
<div class="bx-dyk">
<span class="lbl">🔎 Did you know?</span>
<p>In a Demand Gen campaign with "optimized targeting" turned off, audience signals behave more like real targeting. Search Engine Land's reporting confirms this: turn that setting off, and your ads only show to the audience you picked, even if it underperforms.</p>
</div>

<p>That's the opposite of how <a href="https://www.searchenginejournal.com/google-performance-max/498283/">Performance Max </a>works. In PMax, there's no way to turn signals into a hard wall. The AI always keeps some freedom to look elsewhere.</p>

<!-- OPENING ADSENSE CODE -->
<div class="bx-ad-wrap">
<div class="bx-ad-divider" style="margin-bottom:20px;"><div class="bx-ad-line"></div><span>Advertisement</span><div class="bx-ad-line"></div></div>
<ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-3931314195561246" data-ad-slot="4249015278" data-ad-format="auto" data-full-width-responsive="true"></ins>
<script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
<div class="bx-ad-divider" style="margin-top:20px;"><div class="bx-ad-line"></div><span>Advertisement</span><div class="bx-ad-line"></div></div>
</div>
<!-- CLOSING ADSENSE CODE -->

<h2 id="types"><span class="bx-num">03</span>The Signal Types You Can Actually Use</h2>
<div class="bx-rule"></div>
<p>ClickedOn's 2026 guide breaks the main options down clearly. Each one fits a different stage of the funnel.</p>

<ul style="margin:0 0 20px 20px; padding:0;">
<li style="margin-bottom:8px;"><strong>Affinity segments</strong> — long-term interests, good for top-of-funnel awareness.</li>
<li style="margin-bottom:8px;"><strong>In-Market segments</strong> — people actively researching a purchase right now.</li>
<li style="margin-bottom:8px;"><strong>Custom segments</strong> — built from keywords, URLs, or apps you specify.</li>
<li style="margin-bottom:8px;"><strong>Customer Match</strong> — your own first-party customer data, uploaded directly.</li>
<li style="margin-bottom:8px;"><strong>Detailed demographics</strong> — age, income, parental status, and similar filters.</li>
<li style="margin-bottom:0;"><strong>Life events</strong> — recent moves, graduations, marriages, and other big life changes.</li>
</ul>

<p>First Pier's data found In-Market segments deliver a 10% CTR lift over Affinity segments in direct comparisons. That's a useful default for mid-funnel campaigns.</p>

<h2 id="pmax-vs-demandgen"><span class="bx-num">04</span>How Signals Work Differently in PMax vs Demand Gen</h2>
<div class="bx-rule"></div>
<p>This is the part that trips up a lot of advertisers. Same word, different behavior.</p>

<div class="bx-table-wrap">
<table class="bx-table">
<thead>
<tr><th>Behavior</th><th>Performance Max</th><th>Demand Gen</th></tr>
</thead>
<tbody>
<tr><td>Can signals become a hard limit?</td><td>No, never</td><td>Yes, with optimized targeting off</td></tr>
<tr><td>Applied at what level?</td><td>Asset group</td><td>Ad group / campaign</td></tr>
<tr><td>Lookalike-style expansion?</td><td>Built in automatically</td><td>Lookalike Segments, opt-in</td></tr>
<tr><td>Reporting detail</td><td>Limited channel visibility</td><td>Placement and segment-level detail</td></tr>
</tbody>
</table>
</div>

<p>Groas' comparison guide puts it simply: PMax groups assets and lets Google assemble them. Demand Gen lets you build distinct creative for distinct audiences within the same campaign.</p>

<h2 id="march-2026-change"><span class="bx-num">05</span>What Changed in March 2026</h2>
<div class="bx-rule"></div>
<p>Demand Gen's Lookalike Segments got a quiet but important update. The "reach" slider used to be a hard constraint.</p>

<p>Now it's just a signal strength control. ALM Corp's coverage confirms Google added a "signal" tag next to Lookalike segments in the Audience Reporting table, marking exactly which ones now work this new way.</p>

<div class="bx-note">
<span class="lbl">This Only Affects Demand Gen</span>
<p>ALM Corp's report is specific: this change applies only to Lookalike Segments inside Demand Gen campaigns. Video campaigns, Display & Video 360, Search, Shopping, and Performance Max are unaffected.</p>
</div>

<h2 id="setup-tips"><span class="bx-num">06</span>Getting Signals Right the First Time</h2>
<div class="bx-rule"></div>
<p>Sarah Stemen's 2026 guide reframes the whole job simply: you're not targeting users anymore, you're training the algorithm.</p>

<div class="bx-checklist">
<div class="bx-check-item"><div class="bx-check-icon"></div><p><strong>Start with first-party data.</strong> Customer lists and site visitors give Google the cleanest starting signal.</p></div>
<div class="bx-check-item"><div class="bx-check-icon"></div><p><strong>Don't overload one asset group.</strong> Multiple signals confuse the AI rather than sharpening it.</p></div>
<div class="bx-check-item"><div class="bx-check-icon"></div><p><strong>Give it two full weeks.</strong> Google's own documentation says signals take up to 14 days to fully integrate.</p></div>
<div class="bx-check-item"><div class="bx-check-icon"></div><p><strong>Check new lists after 24-72 hours.</strong> That's the window before audience size populates accurately.</p></div>
<div class="bx-check-item"><div class="bx-check-icon"></div><p><strong>Require click attribution</strong> for conversions where possible, this removes noisy view-through data.</p></div>
</div>

<h2 id="score"><span class="bx-num">07</span>Are Your Audience Signals Set Up Well?</h2>
<div class="bx-rule"></div>
<p>Answer a few quick questions to check your current setup.</p>

<div class="bx-calc">
<div class="bx-calc-header"><h3>Are Your Audience Signals Set Up Well?</h3><p>Select the option that matches your account</p></div>
<div class="bx-calc-body">
<div class="bx-calc-factor"><div class="bx-calc-factor-top"><label>First-party data quality</label><span>30 pts</span></div>
<select class="bx-calc-select" data-weight="30" onchange="bxCalc()">
<option value="0">No customer list uploaded</option>
<option value="0.5">Small or outdated list</option>
<option value="1">Fresh, sizable customer list uploaded</option>
</select></div>
<div class="bx-calc-factor"><div class="bx-calc-factor-top"><label>Signal count per asset group</label><span>25 pts</span></div>
<select class="bx-calc-select" data-weight="25" onchange="bxCalc()">
<option value="0">Many overlapping signals in one group</option>
<option value="1">One clear, focused signal per group</option>
</select></div>
<div class="bx-calc-factor"><div class="bx-calc-factor-top"><label>Time since last signal change</label><span>25 pts</span></div>
<select class="bx-calc-select" data-weight="25" onchange="bxCalc()">
<option value="0">Changed in the last few days</option>
<option value="1">Stable for 2+ weeks</option>
</select></div>
<div class="bx-calc-factor"><div class="bx-calc-factor-top"><label>Conversion attribution setup</label><span>20 pts</span></div>
<select class="bx-calc-select" data-weight="20" onchange="bxCalc()">
<option value="0">Includes noisy view-through data</option>
<option value="1">Click-based attribution required</option>
</select></div>
<div class="bx-calc-gauge-wrap"><div class="bx-calc-gauge-track"><div class="bx-calc-gauge-fill" id="bxGaugeFill"><span id="bxGaugeScore">0%</span></div></div>
<div class="bx-calc-verdict" id="bxVerdict">Select an option for each factor to check your setup.</div></div>
</div>
</div>

<script>
function bxCalc(){var selects=document.querySelectorAll('.bx-calc-select');var total=0;selects.forEach(function(s){var weight=parseFloat(s.getAttribute('data-weight'));var value=parseFloat(s.value);total+=weight*value;});var pct=Math.round(total);document.getElementById('bxGaugeFill').style.width=pct+'%';document.getElementById('bxGaugeScore').innerText=pct+'%';var verdict=document.getElementById('bxVerdict');if(pct>=70){verdict.innerText="Solid setup. Your signals should be training the algorithm effectively.";}else if(pct>=40){verdict.innerText="Getting there. Clean up your data quality or give it more time to settle.";}else{verdict.innerText="Needs work. Start with a clean first-party list and one focused signal per group.";}}
</script>

<h2 id="faq"><span class="bx-num">08</span>Common Questions</h2>
<div class="bx-rule"></div>
<div class="bx-faq" id="bxFaq">
<button class="bx-q">Are audience signals the same as targeting?<span class="ic">+</span></button>
<div class="bx-a"><p>No. Targeting restricts who sees your ad. Signals suggest who to prioritize, but Google can still show ads to people outside that group.</p></div>
<button class="bx-q">Can I force Performance Max to stay within my audience signal?<span class="ic">+</span></button>
<div class="bx-a"><p>No. PMax always keeps some freedom to expand beyond your signal if it finds conversions elsewhere. Only Demand Gen lets you lock this down.</p></div>
<button class="bx-q">What changed with Demand Gen Lookalike Segments in March 2026?<span class="ic">+</span></button>
<div class="bx-a"><p>The reach slider stopped being a hard limit and became a signal strength control instead. Google now marks affected segments with a "signal" tag.</p></div>
<button class="bx-q">How long before I see results from a new audience signal?<span class="ic">+</span></button>
<div class="bx-a"><p>Up to two weeks for Google's models to fully integrate it. New audience lists take 24 to 72 hours just to populate accurately.</p></div>
<button class="bx-q">Should I add multiple audience signals to one asset group?<span class="ic">+</span></button>
<div class="bx-a"><p>Keep it focused. Too many overlapping signals in one group makes it harder for the algorithm to identify a clear pattern.</p></div>
</div>

<div class="bx-related-box">
<h3>Related Articles</h3>
<ul>
<li><a href="/demand-gen-campaigns-explained/" target="_blank" rel="noopener">Demand Gen Campaigns Explained</a></li>
<li><a href="/search-campaign-vs-performance-max/" target="_blank" rel="noopener">Search Campaign vs Performance Max</a></li>
<li><a href="/value-based-bidding-google-ads-explained/" target="_blank" rel="noopener">Value Based Bidding in Google Ads Explained</a></li>
</ul>
</div>

<div class="bx-learn">
<h3>What We Learn Today</h3>
<div class="bx-learn-grid">
<div class="bx-learn-card"><p>Audience signals are suggestions, not hard rules</p></div>
<div class="bx-learn-card"><p>PMax can never be locked to a signal, only Demand Gen can</p></div>
<div class="bx-learn-card"><p>In-Market segments beat Affinity by 10% CTR in tests</p></div>
<div class="bx-learn-card"><p>March 2026 turned Demand Gen's reach slider into a soft signal</p></div>
<div class="bx-learn-card"><p>New signals take up to 2 weeks to fully train</p></div>
<div class="bx-learn-card"><p>First-party data remains the cleanest starting signal</p></div>
</div>
</div>

<section class="bx-cta">
<h2 id="build-a-complete-google-ads-targeting-strategy">Build a Complete Google Ads Targeting Strategy</h2>
<p>Audience signals work best alongside Demand Gen and value-based bidding. Explore both guides next.</p>
<div class="bx-actions">
<a class="bx-btn primary" href="/demand-gen-campaigns-explained/" target="_blank" rel="noopener">Demand Gen Campaigns Explained</a>
<a class="bx-btn ghost" href="/value-based-bidding-google-ads-explained/" target="_blank" rel="noopener">Value Based Bidding Explained</a>
</div>
</section>

</div>
<script>
(function(){var root=document.currentScript.parentNode.querySelector('.bmc-flow')||document;var qs=root.querySelectorAll('#bxFaq .bx-q');qs.forEach(function(q){q.addEventListener('click',function(){var a=q.nextElementSibling,open=q.classList.contains('on');qs.forEach(function(x){x.classList.remove('on');x.nextElementSibling.classList.remove('on');});if(!open){q.classList.add('on');a.classList.add('on');}});});})();
</script>
