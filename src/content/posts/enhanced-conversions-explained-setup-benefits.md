---
title: "Enhanced Conversions Explained: Setup and Benefits"
slug: "enhanced-conversions-explained-setup-benefits"
date: "2026-08-21T04:58:48"
updated: "2026-08-21T04:59:14"
author: "santajigade"
categories: ["google-ads"]
primaryCategory: "google-ads"
description: "Enhanced conversions explained: how the June 2026 unified setup works, real ROAS and CPA data, and the Consent Mode v2 mistake that silently breaks it."
focusKeyword: "Enhanced Conversions"
takeaways:
  - "Enhanced conversions sends hashed first-party data, such as an email, name, address or phone number, to Google using SHA-256 alongside your normal conversion tag."
  - "Since June 2026, enhanced conversions for web and enhanced conversions for leads use one unified on and off setting instead of two separate toggles."
  - "Enhanced conversions does not instantly boost performance; its real value is better tracking accuracy and attribution, which then feeds better Smart Bidding decisions."
  - "To set it up, open your conversion action settings in Google Ads, turn on enhanced conversions and accept the customer data terms."
  - "Configure Consent Mode v2 with ad_user_data set to granted, because without it your hashed data gets silently dropped."
image: "/wp-content/uploads/2026/08/Enhanced-Conversions.webp"
imageAlt: "Enhanced Conversions"
words: 1269
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
<span class="bx-meta-pill">Enhanced Conversions</span>
<span class="bx-meta-pill">Google Ads</span>
<span class="bx-meta-pill">2026</span>
</div>

<p class="bx-lede">Enhanced conversions explained simply: it's Google Ads' fix for the tracking gaps cookies, cross-device journeys, and privacy settings keep creating. You send hashed first-party data, like a customer's email, alongside your normal conversion tag, and Google matches it to close the gap between what actually happened and what your pixel could see.</p>

<p>Google Marketing Live 2026 changed how this works structurally. Enhanced conversions for web and enhanced conversions for leads used to be two separate setups. As of June 2026, they're unified into a single on/off toggle, and Google now accepts hashed data simultaneously from website tags, Data Manager, and API connections at once.</p>

<p>If you've had partial implementation, enhanced conversions for web running, leads tracking never configured, this update is worth revisiting. It closes exactly that kind of gap.</p>

<div class="bx-specs">
<div class="bx-spec"><div class="v">8%</div><div class="k">incremental ROAS lift on Search found across a 99-account study</div></div>
<div class="bx-spec"><div class="v">17.8%</div><div class="k">lower CPA documented versus pixel-only tracking</div></div>
<div class="bx-spec"><div class="v">30 days</div><div class="k">typical training period before impact shows in reporting</div></div>
</div>
<h2 id="what-it-is"><span class="bx-num">01</span>What Enhanced Conversions Actually Does</h2>
<div class="bx-rule"></div>
<p><a href="https://support.google.com/google-ads/answer/9888656?hl=en" target="_blank" rel="noopener">Google's own documentation</a> describes it precisely: enhanced conversions supplements your existing conversion tags by sending hashed first-party data, an email, name, address, or phone number, to Google using SHA-256, a secure one-way hashing algorithm, before it ever leaves your site.</p>

<p>OWOX's explainer frames the practical problem this solves: without enhanced conversions, a user who clicks an ad on their phone and completes a purchase later on desktop can look like two separate people to Google's system. Hashed first-party data lets Google recognize it's the same customer, closing that attribution gap.</p>

<h2 id="june-2026-change"><span class="bx-num">02</span>What Changed in June 2026</h2>
<div class="bx-rule"></div>
<p>Bizi Digital's coverage of Google Marketing Live 2026 calls this the end of a real gap in many accounts: enhanced conversions for web and enhanced conversions for leads used to be entirely separate setups, and it wasn't uncommon for an account to have web tracking live for over a year while the leads version sat completely unconfigured.</p>

<p>RelevantAudience's 2026 guide confirms the mechanics: starting in April 2026, Google began accepting user-provided data simultaneously from website tags, Data Manager, and API connections. By June 2026, that consolidated into one unified on/off toggle, removing the old choice between implementation methods entirely.</p>

<div class="bx-note">
<span class="lbl">Existing Users: No Action Needed</span>
<p>Google's own documentation is clear on migration: if you'd already accepted the customer data terms, you were automatically migrated to the unified setting with no extra steps. New users can now enable it at either the account level or for individual conversion actions.</p>
</div>
<h2 id="benefits"><span class="bx-num">03</span>The Real Benefits, Backed by Data</h2>
<div class="bx-rule"></div>
<p>Growth Minded Marketing's guide is honest about the expectation to set: enhanced conversions doesn't instantly boost campaign performance, its real value is improving tracking accuracy and attribution over time, which then feeds better decisions into Smart Bidding.</p>

<p>Bizi Digital's coverage cites a specific study worth noting: an analysis across 99 accounts found an 8% incremental ROAS lift on Search for advertisers using enhanced conversions. DataCops' implementation guide adds a documented 17.8% lower CPA compared to pixel-only tracking, with typical conversion recovery in the 20% to 40% range once hidden, previously untracked conversions get captured.</p>

<h2 id="setup"><span class="bx-num">04</span>How to Set It Up</h2>
<div class="bx-rule"></div>
<p>Growth Minded Marketing's step-by-step is straightforward: in Google Ads, go to your conversion action settings, expand the Enhanced Conversions section, check "Turn on enhanced conversions," then review and accept the customer data terms. Choose your implementation method, the Google tag, Google Tag Manager, or the API, and confirm the tag captures the right first-party fields.</p>

<p>Campaigns You Love's guide flags a detail that quietly breaks a lot of setups: enhanced conversions technically works without Consent Mode v2, but without the ad_user_data parameter set to "granted," Google silently drops the hashed data server-side with no warning. Your setup will look fine in Tag Assistant while functionally doing nothing.</p>

<div class="bx-code">
<div class="bx-code-label">Basic Enhanced Conversions Data Object (Google Tag)</div>
<pre>gtag('set', 'user_data', {
  email: 'user@example.com',
  phone_number: '+1234567890',
  address: {
    first_name: 'John',
    last_name: 'Doe',
    street: '1 Main St',
    city: 'Anytown',
    region: 'CA',
    postal_code: '12345',
    country: 'US'
  }
});

// Google automatically hashes this data with SHA-256
// before it leaves the browser. Never send plain-text
// data manually, always let the tag handle hashing.</pre>
</div>

<h2 id="checklist"><span class="bx-num">05</span>Implementation Checklist</h2>
<div class="bx-rule"></div>
<p>A short list to confirm before assuming your setup is actually working.</p>

<div class="bx-checklist">
<div class="bx-check-item"><div class="bx-check-icon"></div><p><strong>Turn on the unified toggle</strong> at either account or conversion-action level, no need to choose an implementation method anymore.</p></div>
<div class="bx-check-item"><div class="bx-check-icon"></div><p><strong>Configure Consent Mode v2 properly</strong>, without the ad_user_data parameter set to granted, your hashed data gets silently dropped.</p></div>
<div class="bx-check-item"><div class="bx-check-icon"></div><p><strong>Capture the right first-party fields</strong>, email and phone number matter most; address fields add further matching accuracy.</p></div>
<div class="bx-check-item"><div class="bx-check-icon"></div><p><strong>Wait the full 30-day training period</strong> before judging impact; don't make changes based on the first few days of data.</p></div>
<div class="bx-check-item"><div class="bx-check-icon"></div><p><strong>Set up enhanced conversions in GA4 separately</strong> too, Google Ads and GA4 configurations don't share automatically.</p></div>
</div>

<h2 id="table"><span class="bx-num">06</span>Web vs Leads: What Changed</h2>
<div class="bx-rule"></div>
<p>A quick before-and-after for anyone who set this up before the unification.</p>

<div class="bx-table-wrap">
<table class="bx-table">
<thead>
<tr><th>Aspect</th><th>Before June 2026</th><th>After June 2026</th></tr>
</thead>
<tbody>
<tr><td>Web vs Leads setup</td><td>Two separate feature toggles</td><td>One unified on/off setting</td></tr>
<tr><td>Data sources</td><td>Choose one: tag, Data Manager, or API</td><td>All three accepted simultaneously</td></tr>
<tr><td>Offline conversions import</td><td>Via Google Ads API</td><td>Migrated to Data Manager API (June 15, 2026)</td></tr>
<tr><td>Existing accounts</td><td>N/A</td><td>Auto-migrated if data terms already accepted</td></tr>
</tbody>
</table>
</div>

<h2 id="score"><span class="bx-num">07</span>Is Your Setup Actually Working?</h2>
<div class="bx-rule"></div>
<p>Answer a few questions to check whether your enhanced conversions implementation is likely functioning correctly.</p>

<div class="bx-calc">
<div class="bx-calc-header"><h3>Is Your Setup Actually Working?</h3><p>Select the option that matches your current setup</p></div>
<div class="bx-calc-body">
<div class="bx-calc-factor"><div class="bx-calc-factor-top"><label>Consent Mode v2 status</label><span>35 pts</span></div>
<select class="bx-calc-select" data-weight="35" onchange="bxCalc()">
<option value="0">Not configured or unsure</option>
<option value="0.5">Configured, not fully verified</option>
<option value="1">Configured and verified with ad_user_data granted</option>
</select></div>
<div class="bx-calc-factor"><div class="bx-calc-factor-top"><label>Conversion action status in Google Ads</label><span>30 pts</span></div>
<select class="bx-calc-select" data-weight="30" onchange="bxCalc()">
<option value="0">Shows standard recording, no enhanced status</option>
<option value="0.5">Recently enabled, still in training</option>
<option value="1">Shows "Recording (enhanced conversions)"</option>
</select></div>
<div class="bx-calc-factor"><div class="bx-calc-factor-top"><label>GA4 enhanced conversions</label><span>20 pts</span></div>
<select class="bx-calc-select" data-weight="20" onchange="bxCalc()">
<option value="0">Not set up separately</option>
<option value="1">Configured in both Google Ads and GA4</option>
</select></div>
<div class="bx-calc-factor"><div class="bx-calc-factor-top"><label>Time since enabling</label><span>15 pts</span></div>
<select class="bx-calc-select" data-weight="15" onchange="bxCalc()">
<option value="0">Under 30 days</option>
<option value="1">Over 30 days</option>
</select></div>
<div class="bx-calc-gauge-wrap"><div class="bx-calc-gauge-track"><div class="bx-calc-gauge-fill" id="bxGaugeFill"><span id="bxGaugeScore">0%</span></div></div>
<div class="bx-calc-verdict" id="bxVerdict">Select an option for each factor to check your setup.</div></div>
</div>
</div>

<script>
function bxCalc(){var selects=document.querySelectorAll('.bx-calc-select');var total=0;selects.forEach(function(s){var weight=parseFloat(s.getAttribute('data-weight'));var value=parseFloat(s.value);total+=weight*value;});var pct=Math.round(total);document.getElementById('bxGaugeFill').style.width=pct+'%';document.getElementById('bxGaugeScore').innerText=pct+'%';var verdict=document.getElementById('bxVerdict');if(pct>=75){verdict.innerText="Looking solid. Your setup should be delivering accurate, matched conversion data.";}else if(pct>=40){verdict.innerText="Partially working. Check Consent Mode v2 first, that's the most common silent failure point.";}else{verdict.innerText="Likely not functioning correctly. Start with Consent Mode v2 and verify in the conversion action status column.";}}
</script>

<h2 id="faq"><span class="bx-num">08</span>FAQs on Enhanced Conversions</h2>
<div class="bx-rule"></div>
<div class="bx-faq" id="bxFaq">
<button class="bx-q">What data does enhanced conversions actually send to Google?<span class="ic">+</span></button>
<div class="bx-a"><p>Hashed first-party data like email, phone number, name, and address, encrypted with SHA-256 before it leaves your website. Google never receives plain-text customer data.</p></div>
<button class="bx-q">What changed with the June 2026 update?<span class="ic">+</span></button>
<div class="bx-a"><p>Enhanced conversions for web and leads merged into a single on/off toggle, and Google now accepts data simultaneously from website tags, Data Manager, and API connections.</p></div>
<button class="bx-q">Why isn't my enhanced conversions data showing up?<span class="ic">+</span></button>
<div class="bx-a"><p>The most common cause is Consent Mode v2 not properly set to grant ad_user_data. Without it, Google silently drops the hashed data with no error message.</p></div>
<button class="bx-q">How long until I see the impact in my reports?<span class="ic">+</span></button>
<div class="bx-a"><p>Up to 30 days. Google needs that training period to calibrate matching before enhanced conversion data appears in your reporting.</p></div>
<button class="bx-q">Do I need to set this up separately in GA4?<span class="ic">+</span></button>
<div class="bx-a"><p>Yes. Enabling enhanced conversions in Google Ads doesn't automatically enable it in GA4, they require separate configuration.</p></div>
</div>

<div class="bx-related-box">
<h3>Related Articles</h3>
<ul>
<li><a href="/ga4-events-vs-conversions-difference/" target="_blank" rel="noopener">GA4 Events vs Conversions: The Difference Explained</a></li>
<li><a href="/meta-one-click-conversions-api-pixel-setup/" target="_blank" rel="noopener">Meta Conversions API: One-Click Pixel Setup</a></li>
<li><a href="/search-campaign-vs-performance-max/" target="_blank" rel="noopener">Search Campaign vs Performance Max</a></li>
</ul>
</div>

<div class="bx-learn">
<h3>What We Learn Today</h3>
<div class="bx-learn-grid">
<div class="bx-learn-card"><p>Enhanced conversions sends hashed first-party data to close tracking gaps</p></div>
<div class="bx-learn-card"><p>Web and leads versions unified into one toggle in June 2026</p></div>
<div class="bx-learn-card"><p>Studies show an 8% ROAS lift and 17.8% lower CPA</p></div>
<div class="bx-learn-card"><p>Consent Mode v2 is required or data gets silently dropped</p></div>
<div class="bx-learn-card"><p>Full impact takes up to 30 days of training to appear</p></div>
<div class="bx-learn-card"><p>GA4 and Google Ads need separate enhanced conversions setup</p></div>
</div>
</div>

<section class="bx-cta">
<h2 id="build-a-complete-measurement-foundation">Build a Complete Measurement Foundation</h2>
<p>Enhanced conversions works best alongside clean GA4 tracking and Meta's Conversions API. Explore both guides next.</p>
<div class="bx-actions">
<a class="bx-btn primary" href="/ga4-events-vs-conversions-difference/" target="_blank" rel="noopener">GA4 Events vs Conversions</a>
<a class="bx-btn ghost" href="/meta-one-click-conversions-api-pixel-setup/" target="_blank" rel="noopener">Meta Conversions API Setup</a>
</div>
</section>

</div>
<script>
(function(){var root=document.currentScript.parentNode.querySelector('.bmc-flow')||document;var qs=root.querySelectorAll('#bxFaq .bx-q');qs.forEach(function(q){q.addEventListener('click',function(){var a=q.nextElementSibling,open=q.classList.contains('on');qs.forEach(function(x){x.classList.remove('on');x.nextElementSibling.classList.remove('on');});if(!open){q.classList.add('on');a.classList.add('on');}});});})();
</script>
