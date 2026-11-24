---
title: "Cross Domain Tracking in GA4: Complete Setup Guide"
slug: "cross-domain-tracking-ga4-setup-guide"
date: "2026-08-22T10:13:02"
updated: "2026-08-22T10:14:24"
author: "santajigade"
categories: ["technical-seo"]
primaryCategory: "technical-seo"
description: "Cross domain tracking in GA4, fully explained: exact setup steps, the _gl parameter, common failure points, and the referral exclusion step people skip."
focusKeyword: "Cross domain tracking"
takeaways:
  - "Without cross domain tracking, a visitor moving between separate root domains gets new cookies and IDs, so GA4 counts them as a new user."
  - "GA4 passes identifiers between domains through the _gl URL parameter, whose timestamp invalidates after roughly two minutes by design."
  - "Subdomains are handled automatically, but www and non-www versions and every other domain in the journey must be listed separately."
  - "The native setup only works on link clicks, so form submissions and server-side redirects need extra custom handling."
  - "Add your own domains to the Unwanted Referrals list and force HTTPS throughout, because HTTPS to HTTP downgrades strip the _gl parameter."
image: "/wp-content/uploads/2026/08/Cross-domain-tracking.webp"
imageAlt: "Cross domain tracking"
words: 1395
views: 69
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
.bmc-flow .bx-faq{display:flex;flex-direction:column;gap:14px;margin:20px 0 30px;}
.bmc-flow .bx-faq-item{background:#fff;border:1px solid var(--bx-line);border-radius:12px;padding:18px 20px;}
.bmc-flow .bx-faq-item .fq{font-family:var(--bx-disp);font-weight:700;font-size:17px;color:var(--bx-ink);margin:0 0 8px;}
.bmc-flow .bx-faq-item .fa{margin:0;font-size:17px;color:var(--bx-steel);}
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
<span class="bx-meta-pill">Cross Domain Tracking</span>
<span class="bx-meta-pill">GA4</span>
<span class="bx-meta-pill">2026</span>
</div>

<p class="bx-lede">Cross domain tracking in GA4 is what stops a real customer from looking like two different people in your reports. Without it, someone browsing your main site, then clicking through to checkout.yoursite-payments.com, gets counted as a brand-new visitor the moment the domain changes, and the campaign that actually brought them disappears entirely.</p>

<p>GA4 uses first-party cookies by default, which only work on the single domain that set them. Cross domain tracking passes an identifier between domains through a URL parameter, so the second domain can pick up exactly where the first one left off.</p>

<p>The setup itself is simpler than it used to be in Universal Analytics. Getting it fully correct, especially across cookie consent, redirects, and third-party checkout tools, is where most implementations quietly break.</p>

<div class="bx-specs">
<div class="bx-spec"><div class="v">30-50%</div><div class="k">inflation in new users and sessions typically seen when this is misconfigured</div></div>
<div class="bx-spec"><div class="v">~2 min</div><div class="k">window before the _gl parameter's timestamp invalidates, by design</div></div>
<div class="bx-spec"><div class="v">100</div><div class="k">domain conditions you can configure per data stream in GA4</div></div>
</div>
<h2 id="what-it-is"><span class="bx-num">01</span>Cross Domain Tracking Explained</h2>
<div class="bx-rule"></div>
<p><a href="https://support.google.com/analytics/answer/10071811?hl=en" target="_blank" rel="noopener">Google's own documentation</a> defines it plainly: cross-domain measurement allows activity to be accurately attributed to a single user as they move across domains. Without it, a single visitor to different root domains gets assigned new cookies and new IDs on each one.</p>

<p><a href="https://refact.co/insights/digital-product/ga4-cross-domain-measurement-guide" target="_blank" rel="noopener">Refact's guide</a> adds the mechanism behind it: GA4 passes tracking details through a URL parameter called _gl. When someone clicks from Domain A to Domain B, that parameter carries the identifiers needed so the second domain continues the same session instead of starting fresh.</p>

<h2 id="when-needed"><span class="bx-num">02</span>When You Actually Need Cross Domain Tracking</h2>
<div class="bx-rule"></div>
<p><a href="https://analytics-tips.com/en/cross-domain-tracking-in-ga4-when-it-is-needed-and-how-to-set-it-up" target="_blank" rel="noopener">Analytics-Tips' guide</a> offers the clearest decision rule available: one brand, one strategy, one sales funnel means one GA4 property with properly configured cross-domain tracking. Different businesses or independent teams should stay as two separate properties without it.</p>

<p><a href="https://zeo.org/resources/blog/cross-domain-tracking-in-ga4-a-comprehensive-guide" target="_blank" rel="noopener">Zeo's guide</a> adds a detail worth confirming first: GA4 handles subdomains automatically. You don't need cross domain tracking for something like blog.yoursite.com to shop.yoursite.com, only for genuinely separate root domains.</p>

<div class="bx-dyk">
<span class="lbl">🔎 Did you know?</span>
<p><a href="https://www.analyticsmania.com/post/google-analytics-4-cross-domain-tracking-not-working/" target="_blank" rel="noopener">Analytics Mania's guide</a> notes when cross-domain tracking fails, session data often splits in a way that inflates "New User" and "Session" counts by 30% to 50%, depending on how many visitors move between your domains. It's rarely a subtle problem once it's broken.</p>
</div>
<h2 id="prerequisites"><span class="bx-num">03</span>Before You Start: What You Need</h2>
<div class="bx-rule"></div><p><a href="https://devrix.com/tutorial/cross-domain-tracking-ga4/" target="_blank" rel="noopener">Devrix's March 2026 guide</a> lists the requirements clearly: all domains must send data to the same GA4 Measurement ID, you need Editor-level admin access across every domain involved, and a clear understanding of your current URL parameters so the _gl tag doesn't conflict with existing query strings.</p>

<p><a href="https://www.analyticsmania.com/post/cross-domain-tracking-in-google-analytics-4/" target="_blank" rel="noopener">Analytics Mania's setup guide</a> adds one important limitation: this native solution works when users navigate between domains by clicking a link. It won't work for form submissions or server-side redirects without additional custom handling.</p>

<h2 id="setup"><span class="bx-num">04</span>Step-by-Step Setup in GA4</h2>
<div class="bx-rule"></div>
<p><a href="https://markanamedia.com/blog/ga4-cross-domain-tracking-setup/" target="_blank" rel="noopener">Markana Media's May 2026 guide</a> walks through the exact path: go to Admin, select your web data stream, scroll to Configure Tag Settings, then click Configure Your Domains under Cross-Domain Measurement. Add every domain in the user journey, without the protocol and without trailing slashes.</p>

<p>The same guide flags a detail people miss constantly: GA4 won't automatically assume www and non-www versions are the same domain. If your journey includes www.yoursite.com, yoursite.com, and checkout.yoursite.com, list each variation separately.</p>

<div class="bx-table-wrap">
<table class="bx-table">
<thead>
<tr><th>Step</th><th>Where</th><th>What To Do</th></tr>
</thead>
<tbody>
<tr><td>1. Open Data Streams</td><td>Admin → Property → Data Streams</td><td>Select your primary web data stream</td></tr>
<tr><td>2. Configure Tag Settings</td><td>Bottom of the web stream details page</td><td>Click "Configure tag settings"</td></tr>
<tr><td>3. Add domains</td><td>"Configure your domains"</td><td>List every domain, no protocol, no trailing slash</td></tr>
<tr><td>4. Test</td><td>Browser address bar / DebugView</td><td>Click through and confirm the _gl parameter appears</td></tr>
</tbody>
</table>
</div>

<h2 id="gl-parameter"><span class="bx-num">05</span>Verifying the _gl Parameter</h2>
<div class="bx-rule"></div>
<p><a href="https://krmdigital.uk/blog/cross-domain-tracking/" target="_blank" rel="noopener">KRM Digital's guide</a> gives the simplest confirmation method: click a link from your first domain to your second, then check the destination URL. A parameter starting with <code>?_gl=</code> or <code>&_gl=</code> followed by a character string means it's working.</p>

<p><a href="https://accs-net.com/glossary/cross-domain-tracking/" target="_blank" rel="noopener">ACCS-Net's guide</a> adds an important, easy-to-miss detail: the timestamp inside _gl invalidates after roughly two minutes. That's by design, so users can't bookmark a decorated URL and accidentally impersonate another visitor's client ID later.</p>

<h2 id="code"><span class="bx-num">06</span>GTM Linker Configuration Example</h2>
<div class="bx-rule"></div>
<p>For teams managing this through Google Tag Manager instead of the native GA4 admin panel, here's the linker parameter structure.</p>

<div class="bx-code">
<div class="bx-code-label">GTM Google Tag: Linker Parameter</div>
<pre>// In your Google tag configuration in GTM
// Configuration Parameter: linker
// Value:

{
  "domains": ["example.com", "checkout-example.com"],
  "url_position": "fragment"
}

// Note: setting the linker parameter this way overrides
// any domains configured in the GA4 Admin interface.
// Choose one method, not both, to avoid conflicts.</pre>
</div>

<h2 id="common-issues"><span class="bx-num">07</span>Common Reasons It Breaks</h2>
<div class="bx-rule"></div>
<p>Markana Media's guide, referenced above, describes a real client case: a "URL beautification" script stripped all query parameters from links, silently removing the _gl parameter and breaking funnel tracking for two months before anyone noticed.</p>

<p>ACCS-Net's guide, referenced above, flags mixed protocols as another common failure point. Browsers strip query parameters on HTTPS-to-HTTP downgrades, so any link in the chain going from secure to non-secure will drop the _gl parameter mid-flow. Forcing HTTPS everywhere in the journey avoids this entirely.</p>

<div class="bx-note">
<span class="lbl">Don't Forget Unwanted Referrals</span>
<p><a href="https://www.ficilcom.jp/en/blog/ga4-cross-domain-tracking" target="_blank" rel="noopener">Ficilcom's guide</a> makes a point worth acting on directly: after configuring cross-domain tracking, register each domain in the "List Unwanted Referrals" setting too. Skipping this step means GA4 still logs a self-referral between your own domains, muddying the exact attribution picture you just fixed.</p>
</div>

<h2 id="checklist"><span class="bx-num">08</span>Setup Checklist</h2>
<div class="bx-rule"></div>
<p>Confirm each of these before considering the setup complete.</p>

<div class="bx-checklist">
<div class="bx-check-item"><div class="bx-check-icon"></div><p><strong>Same Measurement ID everywhere.</strong> All domains must send data to the identical GA4 property.</p></div>
<div class="bx-check-item"><div class="bx-check-icon"></div><p><strong>List every domain variant.</strong> www, non-www, and any subdomain used in the journey need separate entries.</p></div>
<div class="bx-check-item"><div class="bx-check-icon"></div><p><strong>Add domains to unwanted referrals</strong> to prevent self-referral pollution in your reports.</p></div>
<div class="bx-check-item"><div class="bx-check-icon"></div><p><strong>Force HTTPS across the entire journey</strong> to avoid the _gl parameter getting stripped mid-flow.</p></div>
<div class="bx-check-item"><div class="bx-check-icon"></div><p><strong>Test with a real click-through</strong>, not just a page reload, and confirm _gl appears in DebugView.</p></div>
</div>

<h2 id="score"><span class="bx-num">09</span>Is Your Setup Actually Working?</h2>
<div class="bx-rule"></div>
<p>Answer a few quick questions to check your current implementation.</p>

<div class="bx-calc">
<div class="bx-calc-header"><h3>Is Your Setup Actually Working?</h3><p>Select the option that matches your property</p></div>
<div class="bx-calc-body">
<div class="bx-calc-factor"><div class="bx-calc-factor-top"><label>_gl parameter appears on click-through</label><span>30 pts</span></div>
<select class="bx-calc-select" data-weight="30" onchange="bxCalc()">
<option value="0">Haven't checked</option>
<option value="0.5">Checked once, unclear result</option>
<option value="1">Confirmed present and valid</option>
</select></div>
<div class="bx-calc-factor"><div class="bx-calc-factor-top"><label>Domain list completeness</label><span>25 pts</span></div>
<select class="bx-calc-select" data-weight="25" onchange="bxCalc()">
<option value="0">Only added one domain variant</option>
<option value="1">All www/non-www/subdomain variants listed</option>
</select></div>
<div class="bx-calc-factor"><div class="bx-calc-factor-top"><label>Unwanted referrals configured?</label><span>25 pts</span></div>
<select class="bx-calc-select" data-weight="25" onchange="bxCalc()">
<option value="0">Not set up</option>
<option value="1">Domains added to the exclusion list</option>
</select></div>
<div class="bx-calc-factor"><div class="bx-calc-factor-top"><label>HTTPS consistency across the journey</label><span>20 pts</span></div>
<select class="bx-calc-select" data-weight="20" onchange="bxCalc()">
<option value="0">Mixed HTTP/HTTPS somewhere</option>
<option value="1">HTTPS enforced throughout</option>
</select></div>
<div class="bx-calc-gauge-wrap"><div class="bx-calc-gauge-track"><div class="bx-calc-gauge-fill" id="bxGaugeFill"><span id="bxGaugeScore">0%</span></div></div>
<div class="bx-calc-verdict" id="bxVerdict">Select an option for each factor to check your setup.</div></div>
</div>
</div>

<script>
function bxCalc(){var selects=document.querySelectorAll('.bx-calc-select');var total=0;selects.forEach(function(s){var weight=parseFloat(s.getAttribute('data-weight'));var value=parseFloat(s.value);total+=weight*value;});var pct=Math.round(total);document.getElementById('bxGaugeFill').style.width=pct+'%';document.getElementById('bxGaugeScore').innerText=pct+'%';var verdict=document.getElementById('bxVerdict');if(pct>=75){verdict.innerText="Looking solid. Your cross domain tracking setup should be capturing the full journey correctly.";}else if(pct>=40){verdict.innerText="Partially working. Check your domain list and unwanted referrals next.";}else{verdict.innerText="Likely broken or incomplete. Start by verifying the _gl parameter on a real click-through.";}}
</script>

<h2 id="faq"><span class="bx-num">10</span>Common Questions</h2>
<div class="bx-rule"></div>

<div class="bx-faq">
<div class="bx-faq-item">
<p class="fq">Do I need cross domain tracking for subdomains?</p>
<p class="fa">No. GA4 automatically handles subdomains using the same cookie domain. Cross domain tracking is only needed for genuinely separate root domains, like example.com to a third-party checkout.com.</p>
</div>
<div class="bx-faq-item">
<p class="fq">Does cross domain tracking work with form submissions?</p>
<p class="fa">Not natively. The native setup relies on link clicks to append the _gl parameter. Form submissions and server-side redirects need additional custom handling to pass the client ID.</p>
</div>
<div class="bx-faq-item">
<p class="fq">Why does GA4 still show a self-referral after I set this up?</p>
<p class="fa">You likely haven't added the domains to the Unwanted Referrals list. Cross-domain configuration and the referral exclusion list are two separate settings, both are needed.</p>
</div>
<div class="bx-faq-item">
<p class="fq">Can I track a single session across two different GA4 properties?</p>
<p class="fa">No. Cross domain tracking only works within a single GA4 property and Measurement ID. Two separate properties cannot share one continuous session.</p>
</div>
<div class="bx-faq-item">
<p class="fq">Why did my tracking break after a developer added a URL cleanup script?</p>
<p class="fa">Scripts that strip query parameters for "clean" URLs often remove the _gl parameter along with everything else, silently breaking cross-domain session continuity without any visible error.</p>
</div>
</div>

<div class="bx-related-box">
<h3>Related Articles</h3>
<ul>
<li><a href="/how-to-detect-filter-bot-traffic-ga4/" target="_blank" rel="noopener">How to Detect and Filter Bot Traffic in GA4</a></li>
<li><a href="/referral-spam-explained-keep-analytics-clean/" target="_blank" rel="noopener">Referral Spam Explained: How to Keep Analytics Data Clean</a></li>
<li><a href="/ga4-custom-event-tracking-google-tag-manager/" target="_blank" rel="noopener">GA4 Custom Event Tracking with Google Tag Manager</a></li>
</ul>
</div>

<div class="bx-learn">
<h3>What We Learn Today</h3>
<div class="bx-learn-grid">
<div class="bx-learn-card"><p>Without it, cross-domain visitors look like brand new users</p></div>
<div class="bx-learn-card"><p>GA4 handles subdomains automatically, no setup needed there</p></div>
<div class="bx-learn-card"><p>The _gl parameter carries identity between domains via link clicks</p></div>
<div class="bx-learn-card"><p>Always list www, non-www, and subdomain variants separately</p></div>
<div class="bx-learn-card"><p>Add domains to unwanted referrals to prevent self-referral noise</p></div>
<div class="bx-learn-card"><p>Mixed HTTP/HTTPS in the journey silently strips the _gl parameter</p></div>
</div>
</div>

<section class="bx-cta">
<h2 id="build-a-complete-clean-data-measurement-stack">Build a Complete Clean-Data Measurement Stack</h2>
<p>Cross domain tracking pairs directly with clean bot filtering and referral spam control. Explore both guides next.</p>
<div class="bx-actions">
<a class="bx-btn primary" href="/how-to-detect-filter-bot-traffic-ga4/" target="_blank" rel="noopener">Detect and Filter Bot Traffic in GA4</a>
<a class="bx-btn ghost" href="/referral-spam-explained-keep-analytics-clean/" target="_blank" rel="noopener">Referral Spam Explained</a>
</div>
</section>

</div>
