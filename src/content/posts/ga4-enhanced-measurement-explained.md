---
title: "GA4 Enhanced Measurement Explained: 7 Essential Events"
slug: "ga4-enhanced-measurement-explained"
date: "2026-11-13T15:40:00"
updated: "2026-11-13T15:40:00"
author: "santajigade"
categories: ["paid-media", "paid-media-analytics"]
primaryCategory: "paid-media"
description: "GA4 enhanced measurement tracks scrolls, outbound clicks, downloads, searches, videos and forms automatically. See every setting with real screenshots."
focusKeyword: "GA4 enhanced measurement"
image: "/images/covers/ga4-enhanced-measurement-explained.webp"
imageAlt: "GA4 Enhanced Measurement Explained: 7 Essential Events"
words: 2051
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

<p>Hello and welcome back! Today we are opening up one of the most useful switches inside Google Analytics, the one most people never look at after setup day.</p>

<p class="bx-lede">You installed GA4, saw page views roll in, and moved on. But somewhere in your data stream settings sits a panel that is quietly tracking scrolls, outbound clicks, downloads, searches, videos and forms for you. If you have ever wondered what GA4 enhanced measurement actually records, which events you can trust, and which ones need a backup plan, this guide walks you through every toggle with real screenshots.</p>

<p>We captured every screenshot below from a live GA4 property for a technical blog, so you see exactly what your own screens will look like. No mockups, no guesswork.</p>

<p>By the end, you will know how to switch each option on or off, where the data lands in your reports, and the handful of gotchas that silently distort your numbers.</p>

<div class="bx-stats">
  <div class="bx-stat"><b>7</b><span>options in the settings panel</span></div>
  <div class="bx-stat"><b>10</b><span>automatic events across those options</span></div>
  <div class="bx-stat"><b>0</b><span>lines of code needed to start</span></div>
</div>

<div class="bx-section-head">
  <span class="bx-num">01</span>
  <h2 class="bx-h2" id="what-is-ga4-enhanced-measurement">What Is GA4 Enhanced Measurement?</h2>
  <div class="bx-rule"></div>
</div>

<p>GA4 enhanced measurement is a set of automatic events that Google Analytics collects from your website without any extra tagging. You switch options on in the interface, and the Google tag starts listening for those interactions.</p>

<p><a href="https://support.google.com/analytics/answer/9216061?hl=en" target="_blank" rel="noopener">Google's own help page on enhanced measurement events</a> describes it as a way to measure content interactions by enabling options in the interface, with no code changes required.</p>

<p>It lives inside your web data stream. Open <b>Admin</b>, then <b>Data streams</b> under Data collection and modification, and you will see your website stream listed.</p>

<div class="bx-shot">
<img src="/images/ga4/01-data-streams.webp" alt="GA4 Admin Data streams list showing the web stream where GA4 enhanced measurement is configured" width="800" height="468" loading="lazy">
</div>
<p class="bx-shot-caption">The Data streams page in GA4 Admin. Click your web stream to reach the GA4 enhanced measurement settings.</p>

<p>Click the stream and the Web stream details panel opens. The Enhanced measurement block sits right under Events, with a master switch and a row of icons showing what is currently being measured.</p>

<div class="bx-shot">
<img src="/images/ga4/02-web-stream-enhanced-measurement.webp" alt="GA4 web stream details panel with the GA4 enhanced measurement switch turned on and Page views, Scrolls and Outbound clicks listed" width="800" height="468" loading="lazy">
</div>
<p class="bx-shot-caption">Web stream details with the master switch on. The gear icon on the right opens the full list of options.</p>

<p>Notice the Measurement ID in that panel too. It starts with <code>G-</code> and is the same ID your Google tag uses on every page.</p>

<div class="bx-ad">
  <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-3931314195561246" data-ad-slot="4249015278" data-ad-format="auto" data-full-width-responsive="true"></ins>
  <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
</div>

<div class="bx-section-head">
  <span class="bx-num">02</span>
  <h2 class="bx-h2" id="how-to-turn-on-ga4-enhanced-measurement">How to Turn On GA4 Enhanced Measurement and Choose Events</h2>
  <div class="bx-rule"></div>
</div>

<p>New GA4 properties usually ship with the feature already on. Still, it is worth opening the settings once, because the defaults are not right for every website.</p>

<p>You need Editor access or higher at the property level to change these toggles, according to <a href="https://support.google.com/analytics/answer/9216061?hl=en" target="_blank" rel="noopener">Google's setup instructions</a>. Viewers can see the panel but cannot save changes.</p>

<ol class="bx-steps">
  <li>Go to <b>Admin</b> and open <b>Data streams</b>.</li>
  <li>Click your <b>Web</b> stream to open the stream details.</li>
  <li>Make sure the <b>Enhanced measurement</b> switch is on.</li>
  <li>Click the <b>gear icon</b> to open the individual options.</li>
  <li>Switch each option on or off, then click <b>Save</b>.</li>
</ol>

<p>Here is what the full options panel looks like once you click the gear. Each option has its own switch and a short description of what it captures.</p>

<div class="bx-shot">
<img src="/images/ga4/03-outbound-clicks-toggle.webp" alt="GA4 enhanced measurement options panel listing Page views, Scrolls, Outbound clicks, Site search, Form interactions, Video engagement and File downloads with their toggles" width="800" height="468" loading="lazy">
</div>
<p class="bx-shot-caption">The individual options panel. Page views has a locked switch, while every other option can be turned off on its own.</p>

<p>Look closely at the Page views row. Its switch is greyed out, because page views are the base of every GA4 property. You can only fine tune them through the advanced settings link underneath.</p>

<div class="bx-tip">
  <p class="bx-tip-label">Tip</p>
  <p>If you just installed GA4 and want a tour of the core metrics these events feed into, read our <a href="https://brandella.in/google-analytics-4-metrics-explained-beginners/">beginner guide to GA4 metrics</a> first.</p>
</div>

<div class="bx-section-head">
  <span class="bx-num">03</span>
  <h2 class="bx-h2" id="the-7-ga4-enhanced-measurement-options">The 7 GA4 Enhanced Measurement Options and Their Events</h2>
  <div class="bx-rule"></div>
</div>

<p>The settings panel shows seven options, but some of them send more than one event. <a href="https://www.semrush.com/blog/google-analytics-4-events/" target="_blank" rel="noopener">Semrush's guide to GA4 events</a> also counts seven switches you can turn on or off with one click.</p>

<p>The table below maps each option to the event names you will actually see in your reports, plus the moment each one fires.</p>

<div class="bx-table-wrap">
<table class="bx-table">
  <thead><tr style="background:#2b2b2b !important;"><th style="background:#2b2b2b !important; color:#ffffff !important;">Option in panel</th><th style="background:#2b2b2b !important; color:#ffffff !important;">Event name</th><th style="background:#2b2b2b !important; color:#ffffff !important;">When it fires</th></tr></thead>
  <tbody>
    <tr><td>Page views</td><td><code>page_view</code></td><td>Each page load, plus browser history changes if left on</td></tr>
    <tr><td>Scrolls</td><td><code>scroll</code></td><td>Once per page, when a visitor reaches roughly 90% of the page</td></tr>
    <tr><td>Outbound clicks</td><td><code>click</code></td><td>A click on a link that leads to another domain</td></tr>
    <tr><td>Site search</td><td><code>view_search_results</code></td><td>A page loads with a search query parameter in the URL</td></tr>
    <tr><td>Form interactions</td><td><code>form_start</code>, <code>form_submit</code></td><td>First interaction with a form in a session, and the submit</td></tr>
    <tr><td>Video engagement</td><td><code>video_start</code>, <code>video_progress</code>, <code>video_complete</code></td><td>Embedded YouTube plays, progress points and completion</td></tr>
    <tr><td>File downloads</td><td><code>file_download</code></td><td>A click on a link to a common document, archive, audio or video file</td></tr>
  </tbody>
</table>
</div>

<p>Add them up and you get ten automatic event names from seven switches. That matches the breakdown in <a href="https://measureschool.com/google-analytics-4-enhanced-measurement/" target="_blank" rel="noopener">Measureschool's enhanced measurement walkthrough</a>, which also lists the extra parameters each event carries.</p>

<p>Those parameters matter. An outbound <code>click</code>, for example, carries the destination as <code>link_url</code>, the domain as <code>link_domain</code> and an <code>outbound</code> flag set to true.</p>

<div class="bx-code-wrap">
  <div class="bx-code-title">outboundClickEvent.txt</div>
  <pre><code><span class="tok-cm">// Simplified view of one automatic outbound click</span>
event_name:   <span class="tok-str">click</span>
link_url:     <span class="tok-str">https://www.example.com/datasheet</span>
link_domain:  <span class="tok-str">example.com</span>
link_text:    <span class="tok-str">Read the datasheet</span>
outbound:     <span class="tok-val">true</span></code></pre>
</div>

<div class="bx-ad">
  <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-3931314195561246" data-ad-slot="4249015278" data-ad-format="auto" data-full-width-responsive="true"></ins>
  <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
</div>

<div class="bx-section-head">
  <span class="bx-num">04</span>
  <h2 class="bx-h2" id="which-ga4-enhanced-measurement-events-to-trust">Which GA4 Enhanced Measurement Events You Can Trust</h2>
  <div class="bx-rule"></div>
</div>

<p>Not every option works equally well on every site. Some are rock solid, others depend on how your site is built.</p>

<p>Use the picker below to check each option. It shows the events, the key parameters, how reliable it tends to be, and what to do when it falls short.</p>

<div class="bx-tool" id="emTool">
  <p class="bx-tool-title">Enhanced Measurement Trust Checker</p>
  <p class="bx-tool-sub">Pick an option to see what it records and whether you should rely on it.</p>
  <div class="bx-chips" id="emChips"></div>
  <div class="bx-panel" id="emPanel"></div>
</div>

<p>The pattern is clear. Page views, outbound clicks and file downloads work well on most sites right away, while forms and videos need a closer look.</p>

<p><a href="https://www.analyticsmania.com/post/google-analytics-4-tutorial/" target="_blank" rel="noopener">Analytics Mania's GA4 tutorial</a> warns that the automatic form events can fire incorrectly or miss submissions, and suggests custom form tracking through GTM when forms matter to your business.</p>

<div class="bx-fact">
  <span class="bx-fact-label">Did You Know</span>
  <p>Video engagement only works for embedded YouTube players with the JavaScript API enabled. <a href="https://measureschool.com/google-analytics-4-enhanced-measurement/" target="_blank" rel="noopener">Measureschool points out</a> that videos hosted on other platforms need a Tag Manager setup instead.</p>
</div>

<p>If your YouTube embeds do not show any <code>video_start</code> events, check the embed URL. It should include the <code>enablejsapi=1</code> parameter.</p>

<div class="bx-code-wrap">
  <div class="bx-code-title">youtubeEmbed.html</div>
  <pre><code>&lt;<span class="tok-kw">iframe</span> <span class="tok-prop">width</span>=<span class="tok-str">"560"</span> <span class="tok-prop">height</span>=<span class="tok-str">"315"</span>
  <span class="tok-prop">src</span>=<span class="tok-str">"https://www.youtube.com/embed/VIDEO_ID?enablejsapi=1"</span>
  <span class="tok-prop">title</span>=<span class="tok-str">"Product demo"</span> <span class="tok-prop">allowfullscreen</span>&gt;&lt;/<span class="tok-kw">iframe</span>&gt;</code></pre>
</div>

<div class="bx-section-head">
  <span class="bx-num">05</span>
  <h2 class="bx-h2" id="where-to-find-ga4-enhanced-measurement-data">Where to Find GA4 Enhanced Measurement Data in Reports</h2>
  <div class="bx-rule"></div>
</div>

<p>All of these events land in the same place: <b>Reports</b>, then <b>Engagement</b>, then <b>Events</b>. The event names appear exactly as they are written, underscores and all.</p>

<p>Type a word into the table search box to narrow the list. Here we searched for "click" on the live property.</p>

<div class="bx-shot">
<img src="/images/ga4/05-events-report-click-event.webp" alt="GA4 Events report filtered to click events showing click_outbound, ad_click and the automatic click event from GA4 enhanced measurement" width="800" height="468" loading="lazy">
</div>
<p class="bx-shot-caption">The Events report filtered to "click". The plain <code>click</code> row is the automatic outbound click event.</p>

<p>Notice there are three rows. Only the plain <code>click</code> row comes from the automatic feature. The other two are custom events this site added separately, which is a good reminder to know which events you created yourself.</p>

<p>For context, the same property logged 3,132 <code>file_download</code> events and 1,998 <code>scroll</code> events over the same 28 days, all without a single line of custom code.</p>

<p>Click any event name to open its detail report. You get a trend line, a country breakdown and a card showing parameter values from the last 30 minutes.</p>

<div class="bx-shot">
<img src="/images/ga4/06-click-event-detail.webp" alt="GA4 event detail report for the automatic click event showing event count, total users and a realtime parameter card" width="800" height="468" loading="lazy">
</div>
<p class="bx-shot-caption">The detail report for the <code>click</code> event. The card on the right shows parameter values in near real time.</p>

<div class="bx-tip">
  <p class="bx-tip-label">Tip</p>
  <p>Parameters like <code>link_url</code> are collected but do not show as report dimensions until you register them. Our guide to <a href="https://brandella.in/custom-dimensions-in-ga4/">custom dimensions in GA4</a> shows the exact steps.</p>
</div>

<div class="bx-ad">
  <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-3931314195561246" data-ad-slot="4249015278" data-ad-format="auto" data-full-width-responsive="true"></ins>
  <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
</div>

<div class="bx-section-head">
  <span class="bx-num">06</span>
  <h2 class="bx-h2" id="ga4-enhanced-measurement-settings-worth-changing">GA4 Enhanced Measurement Settings Worth Changing</h2>
  <div class="bx-rule"></div>
</div>

<p>A few advanced settings fix most of the common data problems. They take minutes to adjust and pay off for years.</p>

<h3 class="bx-h3">Tell GA4 which domains are yours</h3>

<p>Outbound clicks only make sense if GA4 knows where your website ends. If you run a blog and a shop on different domains, both need to be listed, or every click between them counts as outbound.</p>

<p>That list lives in the Google tag settings under <b>Configure your domains</b>. The panel itself explains that it controls which links do not trigger outbound click events.</p>

<div class="bx-shot">
<img src="/images/ga4/04-configure-your-domains.webp" alt="Configure your domains screen in the Google tag settings, which decides which links GA4 enhanced measurement treats as outbound" width="800" height="468" loading="lazy">
</div>
<p class="bx-shot-caption">The Configure your domains screen. Any domain listed here stops counting as an outbound destination.</p>

<p>This same list powers cross domain measurement, so it is worth setting up carefully. Our <a href="https://brandella.in/cross-domain-tracking-ga4-setup-guide/">cross domain tracking guide for GA4</a> covers the full setup.</p>

<h3 class="bx-h3">Add your own site search parameter</h3>

<p>Site search looks for a few common query parameters in the URL. <a href="https://www.lovesdata.com/blog/enhanced-measurement/" target="_blank" rel="noopener">Loves Data's enhanced measurement guide</a> lists defaults like <code>q</code>, <code>s</code>, <code>search</code> and <code>query</code>.</p>

<p>If your search page uses something else, open <b>Show advanced settings</b> under Site search and add your parameter name. You can add several, separated by commas.</p>

<h3 class="bx-h3">Turn off what you already track elsewhere</h3>

<p>Running the same tracking in two places doubles your counts. <a href="https://measureschool.com/google-analytics-4-enhanced-measurement/" target="_blank" rel="noopener">Measureschool recommends</a> disabling an option in GA4 whenever Tag Manager already tracks that same interaction.</p>

<p>This happens most with scroll depth and outbound clicks. If you built custom versions like the ones in our <a href="https://brandella.in/track-scroll-depth-gtm/">scroll depth tracking guide</a>, switch the automatic one off.</p>

<div class="bx-section-head">
  <span class="bx-num">07</span>
  <h2 class="bx-h2" id="ga4-enhanced-measurement-audit-checklist">A 10 Minute GA4 Enhanced Measurement Audit</h2>
  <div class="bx-rule"></div>
</div>

<p>Run through this list once on every property you manage. It catches the problems that quietly inflate or hide your numbers.</p>

<ul class="bx-checklist">
  <li><b>Master switch is on.</b> Open your web stream and confirm the main GA4 enhanced measurement toggle is active.</li>
  <li><b>Only useful options are enabled.</b> Turn off forms or videos if your site does not use them, so the event list stays clean.</li>
  <li><b>No double tracking.</b> Compare your Tag Manager tags against the panel and disable any overlap.</li>
  <li><b>All your domains are listed.</b> Check Configure your domains so internal links never count as outbound.</li>
  <li><b>Search parameter matches your site.</b> Run a test search and check the URL for the parameter name.</li>
  <li><b>YouTube embeds use the JS API.</b> Look for <code>enablejsapi=1</code> in every embed URL.</li>
  <li><b>Key parameters are registered.</b> Register <code>link_url</code>, <code>file_name</code> or <code>search_term</code> as custom dimensions if you report on them.</li>
</ul>

<p>Once your GA4 enhanced measurement setup passes this audit, you have a reliable base layer of behaviour data. Anything beyond it, like button clicks or ecommerce, can then be added with Tag Manager.</p>

<p><a href="https://analytify.io/ga4-enhanced-measurement/" target="_blank" rel="noopener">Analytify's complete guide</a> makes the same point: the feature captures key actions with no extra code, which frees your custom tracking budget for the interactions that are unique to your business.</p>

<div class="bx-ad">
  <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-3931314195561246" data-ad-slot="4249015278" data-ad-format="auto" data-full-width-responsive="true"></ins>
  <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
</div>

<h2 class="bx-h2" id="faq" style="margin-top:40px">Frequently Asked Questions</h2>

<div class="bx-faq">
  <div class="bx-faq-item open">
    <button class="bx-faq-q"><span class="bx-faq-num">1</span>Is GA4 enhanced measurement on by default?</button>
    <div class="bx-faq-a"><p>For most new web data streams, yes. It is still worth opening the gear icon once to check which individual options are switched on for your site.</p></div>
  </div>
  <div class="bx-faq-item open">
    <button class="bx-faq-q"><span class="bx-faq-num">2</span>Do I need Google Tag Manager to use it?</button>
    <div class="bx-faq-a"><p>No. GA4 enhanced measurement works with the standard Google tag alone. Tag Manager only becomes useful when you need tracking the automatic events do not cover.</p></div>
  </div>
  <div class="bx-faq-item open">
    <button class="bx-faq-q"><span class="bx-faq-num">3</span>Why are my form events wrong?</button>
    <div class="bx-faq-a"><p>The automatic form events rely on standard HTML form behaviour. Forms built with JavaScript, popups or AJAX often confuse them, so custom tracking is safer for important forms.</p></div>
  </div>
  <div class="bx-faq-item open">
    <button class="bx-faq-q"><span class="bx-faq-num">4</span>Can I change the 90% scroll threshold?</button>
    <div class="bx-faq-a"><p>Not inside GA4. The automatic <code>scroll</code> event fires once at roughly 90%. For 25%, 50% and 75% points, use a Tag Manager scroll depth trigger and turn the automatic option off.</p></div>
  </div>
  <div class="bx-faq-item open">
    <button class="bx-faq-q"><span class="bx-faq-num">5</span>Does turning an option off delete old data?</button>
    <div class="bx-faq-a"><p>No. Switching an option off only stops new events from being collected. Events already recorded stay in your reports.</p></div>
  </div>
</div>

<div class="bx-learn">
  <h2 id="learn-today">What We Learn Today</h2>
  <div class="bx-learn-grid">
    <div class="bx-learn-card"><span class="bx-learn-num">1</span><div><h4>Seven Switches</h4><p>The settings panel has seven options that send ten automatic events.</p></div></div>
    <div class="bx-learn-card"><span class="bx-learn-num">2</span><div><h4>Web Stream Setting</h4><p>Everything lives under Admin, Data streams, then your web stream.</p></div></div>
    <div class="bx-learn-card"><span class="bx-learn-num">3</span><div><h4>Trust Levels Vary</h4><p>Page views, outbound clicks and downloads are reliable. Forms and video need checks.</p></div></div>
    <div class="bx-learn-card"><span class="bx-learn-num">4</span><div><h4>Your Domain List</h4><p>Configure your domains decides which clicks count as outbound.</p></div></div>
    <div class="bx-learn-card"><span class="bx-learn-num">5</span><div><h4>Avoid Double Counts</h4><p>Disable any option you already track with Tag Manager.</p></div></div>
    <div class="bx-learn-card"><span class="bx-learn-num">6</span><div><h4>Register Parameters</h4><p>Values like the link URL need a custom dimension before they appear in reports.</p></div></div>
  </div>
</div>

<div class="bx-related">
  <h3>Related Articles</h3>
  <div class="bx-related-grid">
    <a class="bx-related-card" href="https://brandella.in/custom-dimensions-in-ga4/"><div class="bx-related-title">Custom Dimensions in GA4: Step by Step</div><span class="bx-related-arrow">&rarr;</span></a>
    <a class="bx-related-card" href="https://brandella.in/track-outbound-link-clicks-gtm/"><div class="bx-related-title">Track Outbound Link Clicks With GTM</div><span class="bx-related-arrow">&rarr;</span></a>
    <a class="bx-related-card" href="https://brandella.in/track-pdf-downloads-ga4/"><div class="bx-related-title">Track PDF Downloads in GA4</div><span class="bx-related-arrow">&rarr;</span></a>
    <a class="bx-related-card" href="https://brandella.in/ga4-events-vs-conversions-difference/"><div class="bx-related-title">GA4 Events vs Conversions Explained</div><span class="bx-related-arrow">&rarr;</span></a>
  </div>
</div>

<div class="bx-cta">
  <h3>Ready to Go Beyond the Defaults?</h3>
  <p>Now that your automatic events are set up properly, learn how to turn its hidden parameters into reports you can actually use.</p>
  <div class="bx-cta-btns">
    <a href="https://brandella.in/custom-dimensions-in-ga4/">Create Custom Dimensions</a>
    <a class="bx-cta-outline" href="https://brandella.in/ga4-free-form-exploration/">Build a Free Form Report</a>
  </div>
</div>

<div class="bx-author">
  <img class="bx-author-photo" src="https://brandella.in/wp-content/uploads/2026/10/santaji-gadepatil.webp" alt="Santaji Gade">
  <div>
    <p class="bx-author-label">Written By</p>
    <h3 class="bx-author-name"><a href="https://brandella.in/author/santajigade/">Santaji Gade</a></h3>
    <p class="bx-author-role">Marketing Manager at <a href="https://www.kobold.com/" target="_blank" rel="noopener">KOBOLD</a> and Founder at <a href="https://brandella.in/" target="_blank" rel="noopener">Brandella</a></p>
    <p class="bx-author-bio">Santaji brings 25 years of hands on experience in SEO, Google Ads, PPC, and digital marketing. He has helped businesses across industries build lasting organic visibility and run profitable paid campaigns, and he shares that practical, real world experience through Brandella Journal to help marketers and business owners grow their search presence.</p>
    <div class="bx-author-links">
      <a href="https://www.linkedin.com/in/santaji-gadepatil6680/" target="_blank" rel="noopener">Connect on LinkedIn</a>
      <a href="https://brandella.in/author/santajigade/">View All Articles</a>
    </div>
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
  var D = {
    'Page views': {ev:'page_view', p:'page_location, page_referrer, page_title', t:'good', tl:'Reliable', n:'Fires on every page load. Leave the browser history option on for single page apps, or switch it off if it creates duplicate views.'},
    'Scrolls': {ev:'scroll', p:'No extra parameters, it fires once near 90 percent', t:'warn', tl:'Limited', n:'Only one fixed threshold. Use a Tag Manager scroll depth trigger if you need 25, 50 and 75 percent points.'},
    'Outbound clicks': {ev:'click', p:'link_url, link_domain, link_text, outbound', t:'good', tl:'Reliable', n:'Works well once every domain you own is listed under Configure your domains.'},
    'Site search': {ev:'view_search_results', p:'search_term', t:'good', tl:'Reliable if URL based', n:'Needs the search term in the URL. Add your own parameter name under advanced settings if it is not a common one.'},
    'Form interactions': {ev:'form_start, form_submit', p:'form_id, form_name, form_destination', t:'bad', tl:'Often unreliable', n:'Struggles with JavaScript, popup and AJAX forms. Track important forms with Tag Manager instead.'},
    'Video engagement': {ev:'video_start, video_progress, video_complete', p:'video_title, video_url, video_percent', t:'warn', tl:'YouTube only', n:'Only embedded YouTube players with enablejsapi=1. Other players need custom tracking.'},
    'File downloads': {ev:'file_download', p:'file_name, file_extension, link_url, link_text', t:'good', tl:'Reliable', n:'Covers common document, archive and media extensions. Custom file types need a Tag Manager trigger.'}
  };
  var chips = document.getElementById('emChips'), panel = document.getElementById('emPanel');
  function show(k){
    var d = D[k];
    chips.querySelectorAll('.bx-chip').forEach(function(c){ c.classList.toggle('on', c.textContent === k); });
    panel.innerHTML = '<h4>' + k + ' <span class="bx-badge ' + d.t + '">' + d.tl + '</span></h4>' +
      '<dl class="bx-kv"><dt>Event name</dt><dd><code>' + d.ev + '</code></dd><dt>Key parameters</dt><dd>' + d.p + '</dd></dl>' +
      '<p style="margin-top:12px !important">' + d.n + '</p>';
  }
  Object.keys(D).forEach(function(k){
    var b = document.createElement('button'); b.className = 'bx-chip'; b.type = 'button'; b.textContent = k;
    b.addEventListener('click', function(){ show(k); }); chips.appendChild(b);
  });
  show('Outbound clicks');
})();
</script>
