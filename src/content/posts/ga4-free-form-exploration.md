---
title: "GA4 Free Form Exploration: 5 Easy Steps to Build Reports"
slug: "ga4-free-form-exploration"
date: "2026-11-13T15:42:00"
updated: "2026-11-13T15:42:00"
author: "santajigade"
categories: ["paid-media", "paid-media-analytics"]
primaryCategory: "paid-media"
description: "Build a GA4 free form exploration in 5 easy steps with real screenshots, fix the 2 month data limit, avoid sampling, and save 5 ready made report recipes."
focusKeyword: "GA4 free form exploration"
takeaways:
  - "A GA4 free form exploration works like a pivot table where you choose the rows, columns, metrics, filters and segments yourself."
  - "By default explorations only see 2 months of event data, so change Event data retention to 14 months under Admin."
  - "The longer retention setting is not retroactive, because the extra history only builds up from the day you switch it."
  - "An outbound click report uses Link domain and Link URL as rows, Event count as the value, and an Event name exactly matches click filter."
  - "Watch the limits: sampling past about 10 million events, the (other) row, data thresholds, and 200 explorations created per user."
image: "/images/covers/ga4-free-form-exploration.webp"
imageAlt: "GA4 Free Form Exploration: 5 Easy Steps to Build Reports"
words: 2026
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

<p>Hey there, and welcome! Today we are building a real custom report in GA4 together, click by click, using live data.</p>

<p class="bx-lede">Standard GA4 reports answer the questions Google expected you to ask. The moment you want something specific, like which external websites your readers click through to most, you hit a wall. A GA4 free form exploration removes that wall. It is a drag and drop table where you choose the rows, the numbers and the filters yourself.</p>

<p>Every screenshot here was captured from a live GA4 property for a technical blog. We will build an outbound click report from a blank canvas, so you can copy the exact same steps on your own site.</p>

<p>Along the way, you will also learn the one data setting to change today, the limits that quietly change your numbers, and five ready made report recipes.</p>

<div class="bx-section-head">
  <span class="bx-num">01</span>
  <h2 class="bx-h2" id="what-is-a-ga4-free-form-exploration">What Is a GA4 Free Form Exploration?</h2>
  <div class="bx-rule"></div>
</div>

<p>Explore is the custom analysis area of GA4, opened from the compass icon in the left menu. It offers several techniques, and free form is the one you will use most.</p>

<p>A GA4 free form exploration is essentially a pivot table. You drop dimensions into rows and columns, add metrics as values, and slice everything with filters or segments.</p>

<p><a href="https://piotrlitwa.com/articles/en/ga4-explorations-guide.html" target="_blank" rel="noopener">Piotr Litwa's explorations guide</a> describes free form as the workhorse for ad hoc questions, and estimates it should cover most of the explorations you build.</p>

<p>The screen has three columns. Variables on the left holds your building blocks, Settings in the middle decides how they are arranged, and the canvas on the right shows the result.</p>

<div class="bx-stats">
  <div class="bx-stat"><b>2</b><span>months of data by default</span></div>
  <div class="bx-stat"><b>14</b><span>months maximum on a standard property</span></div>
  <div class="bx-stat"><b>10M</b><span>events per query before sampling</span></div>
</div>


<div class="bx-section-head">
  <span class="bx-num">02</span>
  <h2 class="bx-h2" id="data-retention-for-ga4-free-form-exploration">Change This Setting Before Your First GA4 Free Form Exploration</h2>
  <div class="bx-rule"></div>
</div>

<p>Here is the surprise that catches almost everyone. By default, explorations can only see the last two months of event data.</p>

<p><a href="https://support.google.com/analytics/answer/7667196?hl=en" target="_blank" rel="noopener">Google's data retention help page</a> confirms you can choose 2 or 14 months on a standard property, and that this setting only affects explorations and funnel reports. Your standard reports are not limited this way.</p>

<ol class="bx-steps">
  <li>Open <b>Admin</b>.</li>
  <li>Under <b>Data collection and modification</b>, click <b>Data retention</b>.</li>
  <li>Change <b>Event data retention</b> to <b>14 months</b> and click <b>Save</b>.</li>
</ol>

<p>The change is not retroactive. <a href="https://www.analyticsmania.com/post/2-month-data-in-google-analytics-4" target="_blank" rel="noopener">Analytics Mania explains</a> that you still cannot select more than two months right away, because the longer history only builds up from the day you switch.</p>

<div class="bx-fact">
  <span class="bx-fact-label">Did You Know</span>
  <p>If a standard property grows large enough to be classed as Large, <a href="https://support.google.com/analytics/answer/7667196?hl=en" target="_blank" rel="noopener">Google automatically reduces event data retention to 2 months</a>, and older event data becomes inaccessible.</p>
</div>

<div class="bx-section-head">
  <span class="bx-num">03</span>
  <h2 class="bx-h2" id="build-a-ga4-free-form-exploration-in-5-steps">How to Build a GA4 Free Form Exploration in 5 Steps</h2>
  <div class="bx-rule"></div>
</div>

<p>Our goal is simple: a table showing which external domains and URLs visitors clicked, ranked by clicks. GA4 already sends this data automatically through outbound click tracking.</p>

<h3 class="bx-h3">Step 1: Start a blank free form</h3>

<p>Click <b>Explore</b> in the left menu, then click the <b>Free form</b> template. GA4 opens a new exploration with a sample table of cities and devices.</p>

<p>Click the <b>Exploration name</b> field at the top of the Variables column and give it a clear name, such as "Outbound link clicks". Explorations are saved automatically as you work.</p>

<h3 class="bx-h3">Step 2: Import the dimensions you need</h3>

<p>Click the <b>plus icon</b> next to Dimensions. A picker opens with every dimension available in the property, grouped by category.</p>

<p>Search for "link" and tick <b>Link domain</b>, <b>Link URL</b> and <b>Outbound</b>. These are predefined, so no custom setup is needed.</p>

<div class="bx-shot">
<img src="/images/ga4/09-explore-link-dimensions.webp" alt="GA4 free form exploration dimension picker with Link domain, Link URL and Outbound ticked" width="800" height="468" loading="lazy">
</div>
<p class="bx-shot-caption">The dimension picker with the three Link dimensions selected. Click Confirm to add them to the Variables column.</p>

<p>Click <b>Confirm</b>. The new dimensions appear in the Variables column, ready to use.</p>

<h3 class="bx-h3">Step 3: Set rows and values</h3>

<p>In the Settings column, remove the default <b>City</b> row by hovering over it and clicking the small cross. Then add <b>Link domain</b> and <b>Link URL</b> as rows.</p>

<p>Remove <b>Device category</b> from Columns, so the table stays simple. Under Values, swap <b>Active users</b> for <b>Event count</b>.</p>

<div class="bx-tip">
  <p class="bx-tip-label">Tip</p>
  <p>You can also drag a dimension straight from the Variables column into Rows. Double clicking it works too and adds it to Rows instantly.</p>
</div>

<h3 class="bx-h3">Step 4: Filter to outbound clicks only</h3>

<p>Without a filter, Link URL picks up values from several events, including file downloads. Scroll to <b>Filters</b>, click the drop zone and choose <b>Event name</b>.</p>

<p>Set the condition to <b>exactly matches</b>, type <code>click</code>, and click <b>Apply</b>.</p>

<div class="bx-shot">
<img src="/images/ga4/10-explore-filter-event-name-click.webp" alt="GA4 free form exploration filter panel with Event name exactly matches click before applying" width="800" height="468" loading="lazy">
</div>
<p class="bx-shot-caption">The filter set to Event name exactly matches click. Before applying it, the table still shows mixed rows with a large (not set) total.</p>

<h3 class="bx-h3">Step 5: Read and sort the result</h3>

<p>The table now lists every outbound domain and URL with its click count. Click the <b>Event count</b> header to sort from highest to lowest.</p>

<div class="bx-shot">
<img src="/images/ga4/11-explore-outbound-clicks-by-link-url.webp" alt="Finished GA4 free form exploration showing outbound clicks by link domain and link URL with a total of 201 events" width="800" height="468" loading="lazy">
</div>
<p class="bx-shot-caption">The finished report. 201 outbound clicks across domains like abb.com, analog.com and api.whatsapp.com.</p>

<p>Want a chart instead of a table? The <b>Visualization</b> icons in the Settings column switch the same data to a donut, line, bar, scatter or geo map view in one click.</p>

<p>For a report like this one, the table usually works best, because long URLs are hard to read on a chart. A bar chart of Link domain alone, without Link URL, is a nice visual for a monthly slide.</p>

<p>Notice the total of 201. It matches the <code>click</code> event count in the standard Events report for the same 28 days, which is a quick way to confirm your filter is correct.</p>


<div class="bx-section-head">
  <span class="bx-num">04</span>
  <h2 class="bx-h2" id="ga4-free-form-exploration-recipe-builder">Plan Your Next GA4 Free Form Exploration</h2>
  <div class="bx-rule"></div>
</div>

<p>Once you have built one report, the same pattern works for almost any question. The builder below gives you the exact settings for common marketing questions.</p>

<p>It also estimates whether your date range is likely to trigger sampling, based on how many events your property records per day.</p>

<div class="bx-tool" id="ffTool">
  <p class="bx-tool-title">Free Form Recipe Builder</p>
  <p class="bx-tool-sub">Pick a question to get the rows, values and filter to use.</p>
  <div class="bx-chips" id="ffChips"></div>
  <div class="bx-panel" id="ffPanel"></div>
  <div class="bx-grid2" style="margin-top:18px">
    <div class="bx-field"><label for="ffDaily">Events per day in your property</label><input id="ffDaily" type="number" min="0" value="5000"></div>
    <div class="bx-field"><label for="ffDays">Days in your date range</label><input id="ffDays" type="number" min="1" max="430" value="28"></div>
  </div>
  <div class="bx-panel">
    <h4 id="ffSampleHead">Sampling check</h4>
    <div class="bx-gauge"><b id="ffBar"></b></div>
    <p id="ffSample"></p>
  </div>
</div>

<p>The sampling check uses the threshold from <a href="https://clickport.io/blog/ga4-data-sampling" target="_blank" rel="noopener">Clickport's breakdown of GA4 sampling</a>, which explains that a standard property samples once a query passes about 10 million events for the date range.</p>

<p>Most small and medium sites never get close. Large ecommerce or media sites can, especially across a full year.</p>

<div class="bx-section-head">
  <span class="bx-num">05</span>
  <h2 class="bx-h2" id="segments-filters-and-sharing">Segments, Filters and Sharing Explained</h2>
  <div class="bx-rule"></div>
</div>

<p>Filters and segments look similar, but they behave differently. Mixing them up is a common reason two tabs show different totals.</p>

<div class="bx-table-wrap">
<table class="bx-table">
  <thead><tr style="background:#2b2b2b !important;"><th style="background:#2b2b2b !important; color:#ffffff !important;">Feature</th><th style="background:#2b2b2b !important; color:#ffffff !important;">What it does</th><th style="background:#2b2b2b !important; color:#ffffff !important;">Best for</th></tr></thead>
  <tbody>
    <tr><td>Filter</td><td>Limits the rows in this one tab</td><td>Showing only one event, page or country</td></tr>
    <tr><td>Segment</td><td>Defines a group of users, sessions or events you can reuse</td><td>Comparing groups side by side, such as mobile versus desktop</td></tr>
    <tr><td>Segment comparison</td><td>Adds a column per segment in the same table</td><td>Quick before and after or audience comparisons</td></tr>
  </tbody>
</table>
</div>

<p><a href="https://www.stackmatix.com/blog/ga4-explorations-guide" target="_blank" rel="noopener">Stackmatix's explorations guide</a> calls confusing a filter for a segment a classic reason an exploration looks fine in one tab and wrong in another.</p>

<p>Explorations are private by default. Use the share icon at the top of the canvas to share a read only copy with colleagues who have access to the property.</p>

<div class="bx-tip">
  <p class="bx-tip-label">Tip</p>
  <p>Add a second tab with the plus button next to the tab name. You can keep a filtered version and an unfiltered version of the same report side by side.</p>
</div>


<div class="bx-section-head">
  <span class="bx-num">06</span>
  <h2 class="bx-h2" id="ga4-free-form-exploration-limits">GA4 Free Form Exploration Limits to Know</h2>
  <div class="bx-rule"></div>
</div>

<p>Explorations query raw event data, which makes them powerful but also subject to a few limits. Knowing them stops you from trusting a number that is quietly estimated.</p>

<h3 class="bx-h3">Sampling on very large queries</h3>

<p>When sampling kicks in, a shield icon at the top right of the canvas turns yellow. Hover over it to see what percentage of data GA4 used.</p>

<p>The fix is usually a shorter date range. Run two smaller explorations instead of one huge one, then combine the results.</p>

<h3 class="bx-h3">The (other) row</h3>

<p>A dimension with thousands of unique values, such as a full page path or URL, can push smaller rows into a single "(other)" line. Stackmatix notes this is a cardinality limit, not classic sampling.</p>

<h3 class="bx-h3">Data thresholds</h3>

<p>When Google signals is active, GA4 may hide rows with very small numbers to protect user privacy. Your totals will look lower than the standard reports on small segments.</p>

<p><a href="https://www.relevantaudience.com/analytics/ga4-explorations-guide/" target="_blank" rel="noopener">Relevant Audience's guide to explorations</a> covers how sampling and thresholds change the numbers you see, and when an exploration beats a standard report.</p>

<h3 class="bx-h3">A cap on saved explorations</h3>

<p>Each user can only create a limited number of explorations per property. <a href="https://analytify.io/google-analytics-limits/" target="_blank" rel="noopener">Analytify's GA4 limits table</a> lists 200 created per user and 500 shared per property, so delete test reports you no longer need.</p>

<div class="bx-section-head">
  <span class="bx-num">07</span>
  <h2 class="bx-h2" id="five-ga4-free-form-exploration-recipes">Five GA4 Free Form Exploration Recipes to Save</h2>
  <div class="bx-rule"></div>
</div>

<p>Build each of these once and keep it. Together they answer most of the questions marketers ask every month.</p>

<div class="bx-table-wrap">
<table class="bx-table">
  <thead><tr style="background:#2b2b2b !important;"><th style="background:#2b2b2b !important; color:#ffffff !important;">Report</th><th style="background:#2b2b2b !important; color:#ffffff !important;">Rows</th><th style="background:#2b2b2b !important; color:#ffffff !important;">Values</th><th style="background:#2b2b2b !important; color:#ffffff !important;">Filter</th></tr></thead>
  <tbody>
    <tr><td>Outbound clicks</td><td>Link domain, Link URL</td><td>Event count</td><td>Event name is click</td></tr>
    <tr><td>File downloads</td><td>File name, Page path</td><td>Event count</td><td>Event name is file_download</td></tr>
    <tr><td>Site search terms</td><td>Search term</td><td>Event count, Total users</td><td>Event name is view_search_results</td></tr>
    <tr><td>Landing page quality</td><td>Landing page</td><td>Sessions, Engagement rate, Key events</td><td>None</td></tr>
    <tr><td>Campaign by device</td><td>Session campaign</td><td>Sessions, Key events</td><td>Columns: Device category</td></tr>
  </tbody>
</table>
</div>

<p>The first three rely on automatic events. Our <a href="https://brandella.in/ga4-enhanced-measurement-explained/">GA4 enhanced measurement guide</a> shows how to make sure those events are switched on.</p>

<p>If you want to report on a parameter that is not predefined, register it first. Our step by step guide to <a href="https://brandella.in/custom-dimensions-in-ga4/">custom dimensions in GA4</a> covers that in a few minutes.</p>

<p>Campaign reports work best when your links carry clean tags. Our <a href="https://brandella.in/utm-parameters-explained/">UTM parameters guide</a> explains how to set them up consistently.</p>

<p>Once these five are saved, your monthly reporting becomes a matter of opening Explore and changing the date range. That is the real payoff of learning the GA4 free form exploration properly.</p>


<h2 class="bx-h2" id="faq" style="margin-top:40px">Frequently Asked Questions</h2>

<div class="bx-faq">
  <div class="bx-faq-item open">
    <button class="bx-faq-q"><span class="bx-faq-num">1</span>Why can I only see two months of data in Explore?</button>
    <div class="bx-faq-a"><p>Your event data retention is set to the default of 2 months. Change it to 14 months under Admin, Data retention. Older data will not come back, but history builds from that day.</p></div>
  </div>
  <div class="bx-faq-item open">
    <button class="bx-faq-q"><span class="bx-faq-num">2</span>Is a GA4 free form exploration saved automatically?</button>
    <div class="bx-faq-a"><p>Yes. Every change is saved as you work, and the exploration appears in the list on the Explore page next time.</p></div>
  </div>
  <div class="bx-faq-item open">
    <button class="bx-faq-q"><span class="bx-faq-num">3</span>Why does my exploration total differ from standard reports?</button>
    <div class="bx-faq-a"><p>Common causes are sampling on large queries, data thresholds on small segments, a filter you forgot about, or a date range that reaches past your retention period.</p></div>
  </div>
  <div class="bx-faq-item open">
    <button class="bx-faq-q"><span class="bx-faq-num">4</span>Can I export a free form table?</button>
    <div class="bx-faq-a"><p>Yes. Use the download icon at the top of the canvas to export to Google Sheets, CSV, TSV or PDF.</p></div>
  </div>
  <div class="bx-faq-item open">
    <button class="bx-faq-q"><span class="bx-faq-num">5</span>Do I need custom dimensions to build explorations?</button>
    <div class="bx-faq-a"><p>Only for parameters that are not predefined. Common ones like Link URL, File name and Search term are already available.</p></div>
  </div>
</div>

<div class="bx-learn">
  <h2 id="learn-today">What We Learn Today</h2>
  <div class="bx-learn-grid">
    <div class="bx-learn-card"><span class="bx-learn-num">1</span><div><h4>A Pivot Table</h4><p>Free form lets you choose rows, columns, values and filters yourself.</p></div></div>
    <div class="bx-learn-card"><span class="bx-learn-num">2</span><div><h4>Fix Retention First</h4><p>Switch event data retention to 14 months before you need history.</p></div></div>
    <div class="bx-learn-card"><span class="bx-learn-num">3</span><div><h4>Import Variables</h4><p>Dimensions and metrics must be added to Variables before use.</p></div></div>
    <div class="bx-learn-card"><span class="bx-learn-num">4</span><div><h4>Filter vs Segment</h4><p>Filters trim one tab. Segments define reusable groups to compare.</p></div></div>
    <div class="bx-learn-card"><span class="bx-learn-num">5</span><div><h4>Check the Shield</h4><p>A yellow shield icon means the result is sampled.</p></div></div>
    <div class="bx-learn-card"><span class="bx-learn-num">6</span><div><h4>Cross Check Totals</h4><p>Compare your total with the standard Events report to confirm filters.</p></div></div>
  </div>
</div>

<div class="bx-cta">
  <h3>Build Reports That Answer Real Questions</h3>
  <p>You now know how to build, filter and trust a GA4 free form exploration. Next, make sure the data feeding it is complete.</p>
  <div class="bx-cta-btns">
    <a href="https://brandella.in/ga4-enhanced-measurement-explained/">Check Automatic Events</a>
    <a class="bx-cta-outline" href="https://brandella.in/custom-dimensions-in-ga4/">Add Custom Dimensions</a>
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
  var R = {
    'Top outbound links': {rows:'Link domain, Link URL', cols:'None', vals:'Event count', filt:'Event name exactly matches click', viz:'Table'},
    'Most downloaded files': {rows:'File name', cols:'None', vals:'Event count, Total users', filt:'Event name exactly matches file_download', viz:'Table'},
    'What visitors search for': {rows:'Search term', cols:'None', vals:'Event count', filt:'Event name exactly matches view_search_results', viz:'Table'},
    'Best landing pages': {rows:'Landing page', cols:'None', vals:'Sessions, Engagement rate, Key events', filt:'None', viz:'Table'},
    'Traffic trend by channel': {rows:'Date', cols:'Session default channel group', vals:'Sessions', filt:'None', viz:'Line chart'},
    'Mobile versus desktop': {rows:'Page title', cols:'Device category', vals:'Views, Engagement rate', filt:'None', viz:'Table'}
  };
  var $ = function(id){ return document.getElementById(id); };
  var chips = $('ffChips'), panel = $('ffPanel');
  function show(k){
    var r = R[k];
    chips.querySelectorAll('.bx-chip').forEach(function(c){ c.classList.toggle('on', c.textContent === k); });
    panel.innerHTML = '<h4>' + k + '</h4><dl class="bx-kv"><dt>Rows</dt><dd>' + r.rows + '</dd><dt>Columns</dt><dd>' + r.cols + '</dd><dt>Values</dt><dd>' + r.vals + '</dd><dt>Filter</dt><dd>' + r.filt + '</dd><dt>Visualization</dt><dd>' + r.viz + '</dd></dl>';
  }
  Object.keys(R).forEach(function(k){
    var b = document.createElement('button'); b.className = 'bx-chip'; b.type = 'button'; b.textContent = k;
    b.addEventListener('click', function(){ show(k); }); chips.appendChild(b);
  });
  function sample(){
    var d = Math.max(0, +$('ffDaily').value || 0), n = Math.max(1, +$('ffDays').value || 1), tot = d * n, lim = 10000000;
    var pct = Math.min(100, tot / lim * 100), bar = $('ffBar');
    bar.style.width = pct + '%'; bar.style.background = pct >= 100 ? '#d9534f' : pct > 70 ? '#e8a33d' : '#5DB92E';
    var badge = pct >= 100 ? '<span class="bx-badge bad">Likely sampled</span>' : pct > 70 ? '<span class="bx-badge warn">Close to limit</span>' : '<span class="bx-badge good">Unsampled</span>';
    $('ffSampleHead').innerHTML = 'Sampling check ' + badge;
    var txt = 'About ' + tot.toLocaleString() + ' events in this range, ' + pct.toFixed(1) + '% of the 10 million threshold.';
    if (pct >= 100) txt += ' Try about ' + Math.max(1, Math.floor(lim / Math.max(d, 1))) + ' days or fewer per query.';
    $('ffSample').textContent = txt;
  }
  ['ffDaily','ffDays'].forEach(function(id){ $(id).addEventListener('input', sample); });
  show('Top outbound links'); sample();
})();
</script>
