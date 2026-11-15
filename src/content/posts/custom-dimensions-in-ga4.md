---
title: "Custom Dimensions in GA4: 6 Simple Steps to Create Them"
slug: "custom-dimensions-in-ga4"
date: "2026-11-13T15:41:00"
updated: "2026-11-13T15:41:00"
author: "santajigade"
categories: ["paid-media", "paid-media-analytics"]
primaryCategory: "paid-media"
description: "Learn how to create custom dimensions in GA4 in 6 steps, choose the right scope, stay within quota limits and avoid the (not set) problem. Real screenshots."
focusKeyword: "custom dimensions in GA4"
image: "/images/covers/custom-dimensions-in-ga4.webp"
imageAlt: "Custom Dimensions in GA4: 6 Simple Steps to Create Them"
words: 2011
views: 0
format: "html"
---
<style>
@import url('https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600;700;800&display=swap');

#bx-article, #bx-article * { box-sizing: border-box; }
#bx-article {
  --bx-disp: 'Open Sans', sans-serif;
  --bx-body: 'Open Sans', sans-serif;
  --bx-green: #5DB92E;
  --bx-green-deep: #4a9e24;
  --bx-charcoal: #2b2b2b;
  --bx-charcoal-soft: #4a4a4a;
  --bx-dark: #20272C;
  font-family: var(--bx-body);
  font-weight: 400;
  font-size: 17px;
  line-height: 1.75;
  color: var(--bx-charcoal);
  max-width: 860px;
  margin: 0 auto;
  padding: 10px 18px 40px;
}
#bx-article a { color: var(--bx-green-deep); text-decoration: none; font-weight: 600; }
#bx-article a:hover { color: var(--bx-charcoal); }
#bx-article p { font-size: 17px; margin: 0 0 16px; }
#bx-article img, #bx-article svg { max-width: 100%; height: auto; }
#bx-article ul.bx-list { margin: 0 0 18px; padding-left: 22px; }
#bx-article ul.bx-list li { font-size: 17px; margin: 0 0 8px; }

.bx-pills { display: flex; flex-wrap: wrap; gap: 8px; margin: 18px 0 20px; }
.bx-pill {
  font-family: var(--bx-disp); font-size: 13px; font-weight: 700;
  color: var(--bx-green-deep); background: #eef8e6; border: 1px solid var(--bx-green);
  padding: 5px 14px; border-radius: 30px; letter-spacing: .3px;
}

.bx-lede {
  font-style: italic; font-size: 17px; color: var(--bx-charcoal-soft);
  border-left: 4px solid var(--bx-green); padding: 6px 20px; margin: 0 0 28px;
}

.bx-stats { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; margin: 22px 0 30px; }
.bx-stat { background: #fff; border: 1px solid #e6efe0; border-top: 4px solid var(--bx-green); border-radius: 10px; padding: 18px 16px; text-align: center; }
.bx-stat b { display: block; font-family: var(--bx-disp); font-weight: 800; font-size: 34px; color: var(--bx-charcoal); line-height: 1.1; }
.bx-stat span { display: block; font-size: 17px; color: var(--bx-charcoal-soft); margin-top: 6px; line-height: 1.4; }
@media (max-width: 640px) { .bx-stats { grid-template-columns: 1fr; } }

.bx-section-head { margin: 46px 0 18px; }
.bx-num {
  font-family: var(--bx-disp); font-weight: 800; font-size: 15px; color: var(--bx-green-deep);
  letter-spacing: 2px; display: block; margin-bottom: 4px;
}
#bx-article h2.bx-h2 {
  font-family: var(--bx-disp); font-weight: 700; font-size: 25px; color: var(--bx-charcoal);
  margin: 0 0 10px; line-height: 1.35;
}
.bx-rule { width: 64px; height: 4px; background: var(--bx-green); border-radius: 2px; }

h3.bx-h3 { font-family: var(--bx-disp); font-weight: 700; font-size: 20px; color: var(--bx-charcoal); margin: 26px 0 12px; }

.bx-code-wrap { margin: 18px 0 26px; border-radius: 10px; overflow: hidden; background: #1e1e2e; box-shadow: 0 2px 10px rgba(0,0,0,.15); }
.bx-code-title {
  background: #171724; color: #a9adc1; font-family: 'Courier New', monospace; font-size: 13px;
  padding: 10px 16px; border-bottom: 1px solid #2f2f45; letter-spacing: .3px;
}
.bx-code-wrap pre { margin: 0; padding: 18px 20px; overflow-x: auto; }
.bx-code-wrap code { font-family: 'Courier New', Consolas, monospace; font-size: 16px; line-height: 1.65; color: #e4e4f0; white-space: pre; }
.tok-kw { color: #c792ea; }
.tok-fn { color: #82aaff; }
.tok-str { color: #f5d76e; }
.tok-val { color: #f78c50; }
.tok-cm  { color: #7c7f93; font-style: italic; }
.tok-prop{ color: #7fdbca; }

.bx-shot { margin: 18px 0 8px; border-radius: 10px; overflow: hidden; box-shadow: 0 2px 10px rgba(0,0,0,.15); border: 1px solid #e6efe0; }
.bx-shot img { display: block; width: 100%; }
.bx-shot-caption { font-size: 14px; color: var(--bx-charcoal-soft); text-align: center; margin: 8px 0 26px; font-style: italic; }

.bx-tip { background: #eef8e6; border-left: 4px solid var(--bx-green); border-radius: 8px; padding: 16px 20px; margin: 20px 0 26px; }
.bx-tip-label {
  display: flex; align-items: center; gap: 8px; font-family: var(--bx-disp); font-weight: 800;
  font-size: 14px; letter-spacing: 1.2px; color: var(--bx-green-deep); text-transform: uppercase; margin: 0 0 6px;
}
.bx-tip-label::before { content: ""; width: 8px; height: 8px; border-radius: 50%; background: var(--bx-green); display: inline-block; }
.bx-tip p { margin: 0; font-size: 17px; color: var(--bx-charcoal); }

.bx-fact { background: #eef8e6; border: 1px solid #d9edcd; border-radius: 10px; padding: 16px 20px 16px 60px; margin: 20px 0 26px; position: relative; }
.bx-fact::before {
  content: "?"; position: absolute; left: 16px; top: 18px; width: 28px; height: 28px; border-radius: 50%;
  background: var(--bx-charcoal); color: var(--bx-green); font-family: var(--bx-disp); font-weight: 800; font-size: 15px;
  display: flex; align-items: center; justify-content: center;
}
.bx-fact-label {
  display: block; font-family: var(--bx-disp); font-weight: 800; font-size: 14px;
  letter-spacing: 1.2px; color: var(--bx-charcoal-soft); text-transform: uppercase; margin: 0 0 4px;
}
.bx-fact p { margin: 0; font-size: 17px; color: var(--bx-charcoal); }

.bx-table-wrap { overflow-x: auto; margin: 20px 0 30px; border-radius: 10px; }
table.bx-table { width: 100%; border-collapse: collapse; font-size: 17px; min-width: 620px; }
table.bx-table thead tr { background: #2b2b2b !important; }
table.bx-table thead th { background: #2b2b2b !important; color: #ffffff !important; font-family: var(--bx-disp); font-weight: 700; text-align: left; padding: 13px 14px; font-size: 17px; }
table.bx-table tbody td { padding: 12px 14px; font-size: 17px; border-bottom: 1px solid #e7f2dd; vertical-align: top; }
table.bx-table tbody tr:nth-child(odd) { background: #f4faef; }
table.bx-table tbody tr:nth-child(even) { background: #ffffff; }

.bx-checklist { list-style: none; margin: 18px 0 28px; padding: 0; display: grid; gap: 12px; }
.bx-checklist li {
  background: #fff; border: 1px solid #e9e9e9; border-left: 4px solid var(--bx-green);
  border-radius: 8px; padding: 14px 16px 14px 44px; position: relative; font-size: 17px;
}
.bx-checklist li::before {
  content: "\2713"; position: absolute; left: 14px; top: 13px; color: var(--bx-green-deep); font-weight: 800; font-size: 17px;
}
.bx-checklist b { color: var(--bx-charcoal); }

.bx-steps { list-style: none; counter-reset: bxstep; margin: 18px 0 28px; padding: 0; display: grid; gap: 12px; }
.bx-steps li { counter-increment: bxstep; position: relative; padding: 14px 16px 14px 62px; background: #fbfefa; border: 1px solid #e3efdc; border-radius: 10px; font-size: 17px; }
.bx-steps li::before { content: counter(bxstep); position: absolute; left: 16px; top: 13px; width: 30px; height: 30px; border-radius: 50%; background: var(--bx-charcoal); color: var(--bx-green); font-family: var(--bx-disp); font-weight: 800; font-size: 15px; display: flex; align-items: center; justify-content: center; }

/* Dark interactive tool panel */
.bx-tool { background: var(--bx-dark); color: #e9eef1; border-radius: 14px; padding: 26px 24px; margin: 24px 0 32px; }
.bx-tool-title { font-family: var(--bx-disp); font-weight: 800; font-size: 20px; color: #fff; margin: 0 0 4px; }
.bx-tool-sub { font-size: 17px; color: #b9c4cb; margin: 0 0 18px; }
.bx-chips { display: flex; flex-wrap: wrap; gap: 8px; margin: 0 0 18px; }
.bx-chip { font-family: var(--bx-disp); font-weight: 700; font-size: 15px; background: #2c353c; color: #dfe7ec; border: 1px solid #3b4750; border-radius: 30px; padding: 8px 16px; cursor: pointer; transition: all .15s ease; }
.bx-chip:hover { border-color: var(--bx-green); }
.bx-chip.on { background: var(--bx-green); color: #fff; border-color: var(--bx-green); }
.bx-panel { background: #2a3238; border: 1px solid #36424a; border-radius: 12px; padding: 18px 20px; }
.bx-panel h4 { font-family: var(--bx-disp); font-size: 17px; color: #fff; margin: 0 0 8px; }
.bx-panel p { color: #d3dce1 !important; font-size: 17px; margin: 0 0 10px !important; }
.bx-panel code { background: #1b2126; color: #9fe07a; padding: 2px 7px; border-radius: 5px; font-size: 15px; }
.bx-kv { display: grid; grid-template-columns: 170px 1fr; gap: 8px 14px; margin: 10px 0 0; font-size: 17px; }
.bx-kv dt { color: #8fa0aa; font-weight: 700; }
.bx-kv dd { margin: 0; color: #eef3f6; }
.bx-badge { display: inline-block; font-weight: 800; font-size: 14px; padding: 3px 12px; border-radius: 20px; letter-spacing: .4px; }
.bx-badge.good { background: #5DB92E; color: #fff; }
.bx-badge.warn { background: #e8a33d; color: #1d1d1d; }
.bx-badge.bad { background: #d9534f; color: #fff; }
.bx-field { margin: 0 0 14px; }
.bx-field label { display: block; font-weight: 700; font-size: 15px; color: #b9c4cb; margin: 0 0 6px; }
.bx-field input, .bx-field select { width: 100%; background: #2a3238; color: #fff; border: 1px solid #3b4750; border-radius: 8px; padding: 10px 12px; font-family: var(--bx-body); font-size: 17px; }
.bx-field input:focus, .bx-field select:focus { outline: none; border-color: var(--bx-green); }
.bx-grid2 { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
.bx-gauge { height: 14px; background: #1b2126; border-radius: 10px; overflow: hidden; margin: 10px 0 6px; }
.bx-gauge b { display: block; height: 100%; width: 0; background: var(--bx-green); border-radius: 10px; transition: width .3s ease, background .3s ease; }
.bx-out { list-style: none; margin: 10px 0 0; padding: 0; }
.bx-out li { font-size: 17px; color: #d3dce1; padding: 7px 0 7px 26px; position: relative; border-bottom: 1px dashed #3b4750; }
.bx-out li:last-child { border-bottom: 0; }
.bx-out li::before { position: absolute; left: 0; top: 7px; font-weight: 800; }
.bx-out li.ok::before { content: "\2713"; color: #7fd14a; }
.bx-out li.no::before { content: "\2717"; color: #ff7b72; }
.bx-out li.wn::before { content: "!"; color: #e8a33d; left: 5px; }
@media (max-width: 640px) { .bx-grid2 { grid-template-columns: 1fr; } .bx-kv { grid-template-columns: 1fr; } }

.bx-faq { margin: 20px 0 30px; display: grid; gap: 12px; }
.bx-faq-item {
  border: 1px solid #e6efe0; border-radius: 12px; background: #fff;
  transition: border-color .2s ease, box-shadow .2s ease;
}
.bx-faq-item.open { border-color: var(--bx-green); box-shadow: 0 2px 12px rgba(93,185,46,.1); }
.bx-faq-q {
  width: 100%; text-align: left; background: none; border: none; cursor: pointer;
  display: flex; align-items: center; gap: 14px;
  font-family: var(--bx-disp); font-weight: 700; font-size: 17px; color: var(--bx-charcoal);
  padding: 16px 44px 16px 16px; position: relative;
}
.bx-faq-num {
  flex-shrink: 0; width: 30px; height: 30px; border-radius: 50%; background: var(--bx-green);
  color: #fff; font-family: var(--bx-disp); font-weight: 800; font-size: 13px;
  display: flex; align-items: center; justify-content: center;
}
.bx-faq-q::after {
  content: "+"; position: absolute; right: 16px; top: 50%; transform: translateY(-50%);
  color: var(--bx-green-deep); font-size: 22px; font-weight: 400; transition: transform .25s ease;
}
.bx-faq-item.open .bx-faq-q::after { transform: translateY(-50%) rotate(45deg); }
.bx-faq-a { max-height: 0; overflow: hidden; transition: max-height .3s ease; }
.bx-faq-a p {
  margin: 0 16px 16px 60px; padding: 2px 0 2px 16px; font-size: 17px; color: var(--bx-charcoal-soft);
  border-left: 3px solid #d9edcd;
}

.bx-related { margin: 34px 0; }
.bx-related h3 {
  font-family: var(--bx-disp); font-size: 19px; color: var(--bx-charcoal); margin: 0 0 16px;
  display: flex; align-items: center; gap: 10px;
}
.bx-related h3::before {
  content: ""; width: 22px; height: 4px; background: var(--bx-green); border-radius: 2px; display: inline-block;
}
.bx-related-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
.bx-related-card {
  display: flex; align-items: center; gap: 12px; background: #fff;
  border: 1px solid #e6efe0; border-left: 4px solid var(--bx-green); border-radius: 10px;
  padding: 15px 16px; transition: box-shadow .2s ease, border-color .2s ease;
}
.bx-related-card:hover { border-color: var(--bx-green); box-shadow: 0 2px 12px rgba(93,185,46,.12); }
.bx-related-title { font-family: var(--bx-disp); font-weight: 700; font-size: 15px; color: var(--bx-charcoal); line-height: 1.4; }
.bx-related-arrow { margin-left: auto; color: var(--bx-green-deep); font-size: 18px; flex-shrink: 0; }
@media (max-width: 640px) { .bx-related-grid { grid-template-columns: 1fr; } }

.bx-learn { margin: 34px 0 8px; }
.bx-learn h2 { font-family: var(--bx-disp); font-size: 22px; color: var(--bx-charcoal); margin-bottom: 14px; }
.bx-learn-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
.bx-learn-card {
  border: 1px solid #e3efdc; border-radius: 10px; padding: 12px 14px 12px 18px; background: #fbfefa;
  display: flex; gap: 10px; align-items: flex-start; position: relative; overflow: hidden;
}
.bx-learn-card::before { content: ""; position: absolute; left: 0; top: 0; bottom: 0; width: 4px; background: var(--bx-green); }
.bx-learn-num {
  flex-shrink: 0; width: 28px; height: 28px; border-radius: 50%; background: var(--bx-green);
  color: #fff; font-family: var(--bx-disp); font-weight: 800; font-size: 13px;
  display: flex; align-items: center; justify-content: center;
}
.bx-learn-card h4 { margin: 0 0 3px; font-family: var(--bx-disp); font-size: 15px; color: var(--bx-charcoal); }
.bx-learn-card p { margin: 0; font-size: 15px; line-height: 1.5; color: var(--bx-charcoal-soft); }
@media (max-width: 640px) { .bx-learn-grid { grid-template-columns: 1fr; } }

.bx-cta {
  background: linear-gradient(120deg, var(--bx-green) 0%, var(--bx-green-deep) 100%);
  border-radius: 14px; padding: 38px 32px; text-align: center; margin: 40px 0 20px; color: #fff;
}
.bx-cta h3 { font-family: var(--bx-disp); font-size: 24px; margin: 0 0 10px; color: #fff; }
.bx-cta p { color: #eafbe0; margin: 0 0 22px; font-size: 17px; }
.bx-cta-btns { display: flex; flex-wrap: wrap; gap: 12px; justify-content: center; }
.bx-cta-btns a {
  background: #fff; color: var(--bx-green-deep) !important; font-family: var(--bx-disp); font-weight: 700;
  padding: 12px 26px; border-radius: 30px; font-size: 15px;
}
.bx-cta-btns a.bx-cta-outline { background: transparent; color: #fff !important; border: 2px solid #fff; }

.bx-author {
  margin: 40px 0 20px; background: #fff; border: 1px solid #e6efe0; border-left: 4px solid var(--bx-green);
  border-radius: 12px; padding: 24px; display: flex; gap: 20px; align-items: flex-start;
}
.bx-author-photo { width: 84px; height: 84px; border-radius: 50%; object-fit: cover; flex-shrink: 0; border: 3px solid #eef8e6; }
.bx-author-label {
  font-family: var(--bx-disp); font-weight: 800; font-size: 12px; letter-spacing: 1.2px;
  color: var(--bx-green-deep); text-transform: uppercase; margin: 0 0 4px;
}
.bx-author-name { font-family: var(--bx-disp); font-size: 19px; margin: 0 0 4px; }
.bx-author-name a { color: var(--bx-charcoal); }
.bx-author-role { font-size: 14px; color: var(--bx-charcoal-soft); margin: 0 0 10px; font-weight: 600; }
.bx-author-bio { font-size: 15px; color: var(--bx-charcoal-soft); margin: 0 0 14px; line-height: 1.6; }
.bx-author-links { display: flex; gap: 10px; flex-wrap: wrap; }
.bx-author-links a {
  font-size: 13px; font-weight: 700; background: #eef8e6; color: var(--bx-green-deep) !important;
  padding: 8px 16px; border-radius: 30px;
}
.bx-author-links a:hover { background: var(--bx-green); color: #fff !important; }
@media (max-width: 640px) {
  .bx-author { flex-direction: column; align-items: center; text-align: center; }
  .bx-author-links { justify-content: center; }
}

.bx-ad { text-align: center; margin: 34px 0; padding: 18px 0; border-top: 1px dashed #cfcfcf; border-bottom: 1px dashed #cfcfcf; }
</style>

<div id="bx-article">
<div class="bx-pills">
  <span class="bx-pill">Paid Media Analytics</span>
  <span class="bx-pill">GA4</span>
</div>

<p>Hi everyone! Today's lesson fixes one of the most common GA4 frustrations: data you know you are sending, but can never find in a report.</p>

<p class="bx-lede">You added a parameter to an event, checked DebugView, and there it was. Then you opened your reports a day later and found nothing. The data was never lost. GA4 simply needs you to register it first, and that is exactly what custom dimensions in GA4 are for. Let's walk through it with real screenshots from a live property.</p>

<p>Every screenshot in this guide comes from a working GA4 property for a technical blog. You will see the same screens and the same buttons when you follow along.</p>

<p>We will cover the three scopes, the exact steps to create a dimension, the limits you need to plan around, and the mistakes that leave you staring at "(not set)".</p>

<div class="bx-section-head">
  <span class="bx-num">01</span>
  <h2 class="bx-h2" id="what-are-custom-dimensions-in-ga4">What Are Custom Dimensions in GA4?</h2>
  <div class="bx-rule"></div>
</div>

<p>Every GA4 event can carry extra details called parameters. A download event might carry a brochure name, and a signup event might carry a plan type.</p>

<p>GA4 collects those parameters, but most of them stay hidden from reports until you tell GA4 to treat them as a dimension. Custom dimensions in GA4 are that bridge between a raw parameter and a column you can actually report on.</p>

<p><a href="https://support.google.com/analytics/answer/10075209?hl=en" target="_blank" rel="noopener">Google's help article on custom dimensions and metrics</a> explains that event scope dimensions report on custom event parameters, while user scope dimensions report on custom user properties.</p>

<p>Think of it this way. The parameter is the raw data you send. The custom dimension is the reporting label that makes it usable.</p>

<h3 class="bx-h3">Custom dimensions versus custom metrics</h3>

<p>The same Custom definitions page also creates custom metrics. The difference is simple: a dimension describes something, while a metric counts or measures it.</p>

<p>A brochure name is a dimension, because you group rows by it. A file size in kilobytes or a quoted order value is a metric, because you add it up or average it.</p>

<p>Most marketers start with custom dimensions in GA4 and only add metrics later, once they know which numbers they want to total in reports.</p>

<div class="bx-stats">
  <div class="bx-stat"><b>50</b><span>event scope dimensions per standard property</span></div>
  <div class="bx-stat"><b>25</b><span>user scope dimensions per standard property</span></div>
  <div class="bx-stat"><b>10</b><span>item scope dimensions per standard property</span></div>
</div>

<div class="bx-ad">
  <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-3931314195561246" data-ad-slot="4249015278" data-ad-format="auto" data-full-width-responsive="true"></ins>
  <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
</div>

<div class="bx-section-head">
  <span class="bx-num">02</span>
  <h2 class="bx-h2" id="scopes-for-custom-dimensions-in-ga4">Event, User and Item Scope for GA4 Dimensions</h2>
  <div class="bx-rule"></div>
</div>

<p>Scope decides what a value describes. Pick the wrong one and your reports will slice data in ways that make no sense.</p>

<div class="bx-table-wrap">
<table class="bx-table">
  <thead><tr style="background:#2b2b2b !important;"><th style="background:#2b2b2b !important; color:#ffffff !important;">Scope</th><th style="background:#2b2b2b !important; color:#ffffff !important;">Describes</th><th style="background:#2b2b2b !important; color:#ffffff !important;">Good example</th><th style="background:#2b2b2b !important; color:#ffffff !important;">Standard limit</th></tr></thead>
  <tbody>
    <tr><td>Event</td><td>One single action</td><td>Brochure name on a download</td><td>50</td></tr>
    <tr><td>User</td><td>The person, across sessions</td><td>Customer type, such as distributor</td><td>25</td></tr>
    <tr><td>Item</td><td>A product inside an ecommerce event</td><td>Product colour or supplier</td><td>10</td></tr>
  </tbody>
</table>
</div>

<p>Most dimensions belong in event scope. <a href="https://www.relevantaudience.com/analytics/ga4-custom-dimensions/" target="_blank" rel="noopener">Relevant Audience's guide to scopes and quotas</a> calls choosing the wrong scope the most common design mistake, and notes that scope cannot be changed after you save.</p>

<p>User scope values come from user properties. Once set, GA4 applies them to that visitor's later events too, which is why they suit stable traits rather than one off actions.</p>

<div class="bx-fact">
  <span class="bx-fact-label">Did You Know</span>
  <p>A GA4 360 property raises the limits to 125 event scope, 100 user scope and 25 item scope dimensions, according to <a href="https://support.google.com/analytics/answer/10075209?hl=en" target="_blank" rel="noopener">Google's own limits table</a>.</p>
</div>

<div class="bx-section-head">
  <span class="bx-num">03</span>
  <h2 class="bx-h2" id="how-to-create-custom-dimensions-in-ga4">How to Create Custom Dimensions in GA4 in 6 Steps</h2>
  <div class="bx-rule"></div>
</div>

<p>The whole process takes about two minutes once the parameter is already being sent. Here is the path, step by step.</p>

<ol class="bx-steps">
  <li>Click <b>Admin</b> at the bottom left of GA4.</li>
  <li>Under <b>Data display</b>, open <b>Custom definitions</b>.</li>
  <li>Stay on the <b>Custom dimensions</b> tab and click <b>Create custom dimension</b>.</li>
  <li>Enter a clear <b>Dimension name</b> and an optional description.</li>
  <li>Choose the <b>Scope</b>, then pick or type the exact <b>Event parameter</b> name.</li>
  <li>Click <b>Save</b>, then wait for new data to arrive.</li>
</ol>

<p>Here is the Custom definitions page on our live property. Notice it already holds six dimensions that a WordPress plugin created automatically.</p>

<div class="bx-shot">
<img src="/images/ga4/07-custom-definitions.webp" alt="GA4 Custom definitions page listing custom dimensions in GA4 that were created by the Site Kit plugin" width="800" height="468" loading="lazy">
</div>
<p class="bx-shot-caption">The Custom definitions page. The six rows here were added by Google Site Kit, a reminder to check what already exists before adding more.</p>

<p>Plugins like Site Kit quietly use part of your quota. Always review this list first, so you know how many slots you really have left.</p>

<p>Clicking <b>Create custom dimension</b> opens the form on the right. Here it is filled in for the <code>link_url</code> parameter that outbound clicks send.</p>

<div class="bx-shot">
<img src="/images/ga4/08-create-link-url-custom-dimension.webp" alt="New custom dimension form in GA4 with Link URL as the name, Event as the scope and link_url as the event parameter" width="800" height="468" loading="lazy">
</div>
<p class="bx-shot-caption">The new custom dimension form, filled in for <code>link_url</code>. The parameter dropdown suggests names GA4 has already received.</p>

<p>Before you click Save, though, there is one check that saves quota. We actually closed this form without saving, and the next section shows why.</p>

<div class="bx-tip">
  <p class="bx-tip-label">Tip</p>
  <p>The parameter name must match exactly, including letter case. <code>Link_URL</code> and <code>link_url</code> are two different parameters to GA4.</p>
</div>

<div class="bx-ad">
  <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-3931314195561246" data-ad-slot="4249015278" data-ad-format="auto" data-full-width-responsive="true"></ins>
  <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
</div>

<div class="bx-section-head">
  <span class="bx-num">04</span>
  <h2 class="bx-h2" id="check-a-parameter-before-registering">Check a Parameter Before You Register It</h2>
  <div class="bx-rule"></div>
</div>

<p>GA4 already ships with hundreds of predefined dimensions. Many common parameters, including <code>link_url</code>, are already available as built in dimensions in Explore, so registering them again just burns a slot.</p>

<p>You can see this inside an exploration. Searching for "link" in the dimension picker shows five predefined Link dimensions plus Outbound, with zero custom ones needed.</p>

<div class="bx-shot">
<img src="/images/ga4/09-explore-link-dimensions.webp" alt="GA4 Explore dimension picker showing predefined Link domain, Link URL and Outbound dimensions that do not need custom dimensions in GA4" width="800" height="468" loading="lazy">
</div>
<p class="bx-shot-caption">The Explore dimension picker. Link URL is predefined, so there is no need to register it as a custom dimension for explorations.</p>

<p>Use the planner below before you create anything. It checks the name, flags parameters GA4 already covers, warns about values that change too often, and shows how much quota you have left.</p>

<div class="bx-tool" id="cdTool">
  <p class="bx-tool-title">Custom Dimension Planner</p>
  <p class="bx-tool-sub">Type a parameter name and see if it is worth registering.</p>
  <div class="bx-grid2">
    <div class="bx-field"><label for="cdName">Event parameter name</label><input id="cdName" type="text" value="product_line" autocomplete="off"></div>
    <div class="bx-field"><label for="cdScope">Scope</label><select id="cdScope"><option value="50">Event</option><option value="25">User</option><option value="10">Item</option></select></div>
    <div class="bx-field"><label for="cdUnique">Different values per day</label><select id="cdUnique"><option value="low">Under 100</option><option value="mid">100 to 500</option><option value="high">More than 500</option></select></div>
    <div class="bx-field"><label for="cdUsed">Dimensions already used in this scope</label><input id="cdUsed" type="number" min="0" max="125" value="6"></div>
  </div>
  <div class="bx-panel">
    <h4 id="cdVerdict">Checking</h4>
    <div class="bx-gauge"><b id="cdBar"></b></div>
    <p id="cdQuota" style="font-size:15px !important"></p>
    <ul class="bx-out" id="cdOut"></ul>
  </div>
</div>

<p>The planner flags high cardinality for a reason. <a href="https://www.stackmatix.com/blog/ga4-custom-dimensions" target="_blank" rel="noopener">Stackmatix's GA4 custom dimensions guide</a> explains how dimensions with too many unique values push rows into an "(other)" bucket in your reports.</p>

<div class="bx-section-head">
  <span class="bx-num">05</span>
  <h2 class="bx-h2" id="send-parameters-for-custom-dimensions-in-ga4">Send the Parameter, Then Register It</h2>
  <div class="bx-rule"></div>
</div>

<p>A dimension is only a label. Something on your website still has to send the parameter with each event.</p>

<p>Here is a real example. A brochure download event sends two custom parameters, and a user property marks the visitor as a distributor.</p>

<div class="bx-code-wrap">
  <div class="bx-code-title">brochureDownload.js</div>
  <pre><code><span class="tok-cm">// Event parameters, register as Event scope</span>
<span class="tok-fn">gtag</span>(<span class="tok-str">'event'</span>, <span class="tok-str">'download_brochure'</span>, {
  <span class="tok-prop">brochure_name</span>: <span class="tok-str">'Flow Meters 2026'</span>,
  <span class="tok-prop">product_line</span>: <span class="tok-str">'flow'</span>
});

<span class="tok-cm">// User property, register as User scope</span>
<span class="tok-fn">gtag</span>(<span class="tok-str">'set'</span>, <span class="tok-str">'user_properties'</span>, {
  <span class="tok-prop">customer_type</span>: <span class="tok-str">'distributor'</span>
});</code></pre>
</div>

<h3 class="bx-h3">Pick a naming convention and stick to it</h3>

<p>Lowercase names with underscores, like <code>product_line</code>, match the style Google uses for its own parameters. They are also easier to read in DebugView and harder to mistype.</p>

<p>Write the convention down for your team before anyone adds new tracking. A shared list of approved custom dimensions in GA4, with the parameter name, scope and owner for each one, prevents duplicates and keeps your quota under control.</p>

<p>You would then create two event scope dimensions, one for <code>brochure_name</code> and one for <code>product_line</code>, plus one user scope dimension for <code>customer_type</code>.</p>

<p>If you use Tag Manager instead of gtag, the logic is the same. Our guide to <a href="https://brandella.in/ga4-custom-event-tracking-google-tag-manager/">custom event tracking with Google Tag Manager</a> shows how to add parameters inside a GA4 event tag.</p>

<p>Keep collection limits in mind too. <a href="https://www.relevantaudience.com/analytics/ga4-custom-dimensions/" target="_blank" rel="noopener">Relevant Audience lists</a> a 40 character cap on parameter names, a 100 character cap on most values, and a maximum of 25 parameters per event.</p>

<div class="bx-tip">
  <p class="bx-tip-label">Tip</p>
  <p>Confirm the parameter in DebugView before you register anything. If it is not arriving there, no custom dimension will fix it.</p>
</div>

<div class="bx-ad">
  <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-3931314195561246" data-ad-slot="4249015278" data-ad-format="auto" data-full-width-responsive="true"></ins>
  <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
</div>

<div class="bx-section-head">
  <span class="bx-num">06</span>
  <h2 class="bx-h2" id="common-mistakes-with-custom-dimensions-in-ga4">Common Mistakes With Custom Dimensions in GA4</h2>
  <div class="bx-rule"></div>
</div>

<p>Most problems with custom dimensions in GA4 come down to timing, naming or quota. Here are the ones we see most often.</p>

<h3 class="bx-h3">Expecting old data to appear</h3>

<p>Registration is not retroactive. Relevant Audience notes that Google says a new dimension becomes usable 24 to 48 hours after it is created, and that earlier events are not reprocessed.</p>

<p><a href="https://optimizesmart.com/blog/google-analytics-4-data-delays-guidelines/" target="_blank" rel="noopener">Optimize Smart's guide to GA4 data delays</a> adds that you may see "(not set)" for a new custom dimension during its first 24 hours. That is normal, not a broken setup.</p>

<h3 class="bx-h3">Registering everything just in case</h3>

<p>Fifty slots sound generous until a few plugins and old experiments take half of them. Register only what you will actually report on.</p>

<p>If you hit the limit, you can archive old dimensions. <a href="https://measureschool.com/ga4-custom-dimensions/" target="_blank" rel="noopener">Measureschool's guide</a> shows the archive prompt warning that it cannot be undone, and Relevant Audience adds that you must wait 48 hours before reusing freed slots.</p>

<h3 class="bx-h3">Using values that are too unique</h3>

<p>Session IDs, timestamps and full user agent strings make terrible dimensions. They create so many unique values that GA4 groups most of them into "(other)".</p>

<h3 class="bx-h3">Mistyping the parameter name</h3>

<p>A dimension pointing at a parameter that is never sent stays empty forever. Copy the name straight from DebugView rather than typing it from memory.</p>

<h3 class="bx-h3">Sending personal information</h3>

<p>Never pass email addresses, phone numbers or full names as parameters. Google Analytics policies do not allow personally identifiable information, and a single careless form field can put your whole property at risk.</p>

<p>Use an internal ID or a broad category instead. "Distributor" or "returning buyer" tells you everything you need for reporting, without exposing who the person actually is.</p>

<div class="bx-section-head">
  <span class="bx-num">07</span>
  <h2 class="bx-h2" id="where-to-use-custom-dimensions-in-ga4">Where Your New GA4 Dimensions Show Up in Reports</h2>
  <div class="bx-rule"></div>
</div>

<p>Once data flows in, custom dimensions in GA4 appear in three main places. Each one suits a different kind of question.</p>

<ul class="bx-checklist">
  <li><b>Standard reports.</b> Add the dimension as a secondary dimension, or customize a report so it shows by default.</li>
  <li><b>Explorations.</b> Import it into the Variables panel and use it as a row, column or filter. Our <a href="https://brandella.in/ga4-free-form-exploration/">GA4 free form exploration guide</a> shows this step by step.</li>
  <li><b>Audiences.</b> Build an audience such as every visitor whose customer type is distributor.</li>
  <li><b>Looker Studio.</b> Registered dimensions appear in the GA4 connector, ready for dashboards.</li>
</ul>

<p><a href="https://www.analyticsmania.com/post/a-guide-to-custom-dimensions-in-google-analytics-4/" target="_blank" rel="noopener">Analytics Mania's custom dimensions guide</a> walks through each of these report locations in more detail if you want to go deeper.</p>

<p>If your parameters come from the automatic events covered in our <a href="https://brandella.in/ga4-enhanced-measurement-explained/">GA4 enhanced measurement guide</a>, check the predefined list first. Many of them are already there.</p>

<div class="bx-ad">
  <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-3931314195561246" data-ad-slot="4249015278" data-ad-format="auto" data-full-width-responsive="true"></ins>
  <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
</div>

<h2 class="bx-h2" id="faq" style="margin-top:40px">Frequently Asked Questions</h2>

<div class="bx-faq">
  <div class="bx-faq-item open">
    <button class="bx-faq-q"><span class="bx-faq-num">1</span>How long do custom dimensions take to show data?</button>
    <div class="bx-faq-a"><p>Usually 24 to 48 hours after you create them and new events arrive. Data collected before you registered the dimension will not appear.</p></div>
  </div>
  <div class="bx-faq-item open">
    <button class="bx-faq-q"><span class="bx-faq-num">2</span>Can I change the scope after saving?</button>
    <div class="bx-faq-a"><p>No. The scope and the event parameter are locked once saved. You need to archive the dimension and create a new one with the right settings.</p></div>
  </div>
  <div class="bx-faq-item open">
    <button class="bx-faq-q"><span class="bx-faq-num">3</span>How many custom dimensions in GA4 can I create?</button>
    <div class="bx-faq-a"><p>A standard property allows 50 event scope, 25 user scope and 10 item scope dimensions, plus 50 custom metrics.</p></div>
  </div>
  <div class="bx-faq-item open">
    <button class="bx-faq-q"><span class="bx-faq-num">4</span>Why does my dimension show (not set)?</button>
    <div class="bx-faq-a"><p>Either the data is still processing, the parameter name does not match exactly, or that particular event simply did not send the parameter.</p></div>
  </div>
  <div class="bx-faq-item open">
    <button class="bx-faq-q"><span class="bx-faq-num">5</span>Do I need to register link_url for outbound clicks?</button>
    <div class="bx-faq-a"><p>Not for explorations, where Link URL is already a predefined dimension. Check the predefined list in your reports before using a custom slot.</p></div>
  </div>
</div>

<div class="bx-learn">
  <h2 id="learn-today">What We Learn Today</h2>
  <div class="bx-learn-grid">
    <div class="bx-learn-card"><span class="bx-learn-num">1</span><div><h4>Parameter vs Dimension</h4><p>Parameters are raw data. Dimensions are the labels that make them reportable.</p></div></div>
    <div class="bx-learn-card"><span class="bx-learn-num">2</span><div><h4>Three Scopes</h4><p>Event for actions, User for people, Item for products in ecommerce.</p></div></div>
    <div class="bx-learn-card"><span class="bx-learn-num">3</span><div><h4>Quota Limits</h4><p>Standard properties get 50 event, 25 user and 10 item dimensions.</p></div></div>
    <div class="bx-learn-card"><span class="bx-learn-num">4</span><div><h4>Check Predefined First</h4><p>Many parameters, like Link URL, already exist as built in dimensions.</p></div></div>
    <div class="bx-learn-card"><span class="bx-learn-num">5</span><div><h4>Not Retroactive</h4><p>Only events after registration fill the dimension, after 24 to 48 hours.</p></div></div>
    <div class="bx-learn-card"><span class="bx-learn-num">6</span><div><h4>Avoid Unique Values</h4><p>IDs and timestamps flood reports with an (other) row.</p></div></div>
  </div>
</div>

<div class="bx-cta">
  <h3>Turn Your Parameters Into Insights</h3>
  <p>Your custom dimensions in GA4 are ready. Put them to work in a free form exploration and answer questions standard reports cannot.</p>
  <div class="bx-cta-btns">
    <a href="https://brandella.in/ga4-free-form-exploration/">Build a Free Form Report</a>
    <a class="bx-cta-outline" href="https://brandella.in/ga4-enhanced-measurement-explained/">Review Automatic Events</a>
  </div>
</div>

</div>

<script>
document.querySelectorAll('#bx-article .bx-faq-item').forEach(function(item){
  var q = item.querySelector('.bx-faq-q');
  var a = item.querySelector('.bx-faq-a');
  a.style.maxHeight = a.scrollHeight + 'px';
  q.addEventListener('click', function(){
    var isOpen = item.classList.contains('open');
    if (isOpen) { item.classList.remove('open'); a.style.maxHeight = '0px'; }
    else { item.classList.add('open'); a.style.maxHeight = a.scrollHeight + 'px'; }
  });
});
</script>
<script>
(function(){
  var PRE = ['link_url','link_text','link_domain','link_classes','link_id','outbound','file_name','file_extension','search_term','video_title','video_url','video_provider','percent_scrolled','page_location','page_referrer','page_title'];
  var $ = function(id){ return document.getElementById(id); };
  function run(){
    var n = $('cdName').value.trim(), lim = +$('cdScope').value, used = Math.max(0, +$('cdUsed').value || 0), u = $('cdUnique').value;
    var out = [], bad = 0, warn = 0;
    function add(c, t){ out.push('<li class="' + c + '">' + t + '</li>'); if (c === 'no') bad++; if (c === 'wn') warn++; }
    if (!n) add('no', 'Enter a parameter name.');
    else {
      add(n.length <= 40 ? 'ok' : 'no', 'Length is ' + n.length + ' characters (40 maximum).');
      add(/^[A-Za-z][A-Za-z0-9_]*$/.test(n) ? 'ok' : 'no', 'Starts with a letter and uses only letters, numbers and underscores.');
      add(/^(google_|ga_|firebase_)/i.test(n) ? 'no' : 'ok', 'Does not use a reserved prefix such as google_ or ga_.');
      if (PRE.indexOf(n.toLowerCase()) > -1) add('wn', 'GA4 already offers this as a predefined dimension. You may not need a custom slot.');
      else add('ok', 'Not on the common predefined list.');
      if (n !== n.toLowerCase()) add('wn', 'Contains capitals. Make sure the name matches what your site sends, letter for letter.');
    }
    if (u === 'high') add('wn', 'Many different values. Expect an (other) row in reports.');
    else if (u === 'mid') add('ok', 'Moderate variety. Fine for most reports.');
    else add('ok', 'Low variety. Ideal for reporting.');
    var left = Math.max(0, lim - used), pct = Math.min(100, used / lim * 100);
    if (left === 0) add('no', 'No free slots left in this scope. Archive an old dimension first.');
    var bar = $('cdBar'); bar.style.width = pct + '%'; bar.style.background = pct > 85 ? '#d9534f' : pct > 60 ? '#e8a33d' : '#5DB92E';
    $('cdQuota').textContent = used + ' of ' + lim + ' slots used. After this one, ' + Math.max(0, left - 1) + ' will be left.';
    $('cdVerdict').innerHTML = bad ? 'Fix before registering <span class="bx-badge bad">Not ready</span>' : warn ? 'Register with care <span class="bx-badge warn">Review</span>' : 'Good to register <span class="bx-badge good">Ready</span>';
    $('cdOut').innerHTML = out.join('');
  }
  ['cdName','cdUsed'].forEach(function(id){ $(id).addEventListener('input', run); });
  ['cdScope','cdUnique'].forEach(function(id){ $(id).addEventListener('change', run); });
  run();
})();
</script>
