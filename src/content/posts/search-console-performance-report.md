---
title: "Search Console Performance Report: 5 Essential Metrics"
slug: "search-console-performance-report"
date: "2026-10-01T05:15:52"
updated: "2026-10-01T05:16:13"
author: "santajigade"
categories: ["google-search-console"]
primaryCategory: "google-search-console"
description: "A search console performance report turns a spreadsheet of queries into a clear action list. See the 5 metrics that actually tell you what to fix."
focusKeyword: "search console performance report"
takeaways:
  - "The Performance report is built on four metrics: clicks, impressions, click through rate and average position, which only tell the full story together."
  - "The quickest wins are queries with an average position between four and fifteen, since Google already trusts the page but it has not reached the top three."
  - "Ignore queries with fewer than fifty impressions across a ninety day window, because smaller samples are too noisy to act on with confidence."
  - "Ahrefs found position one click through rate fell by roughly 34.5 percent when an AI Overview appeared, so lower CTR does not always mean weaker content."
  - "Search Console keeps only sixteen months of data with a lag of about two to three days, so export your data monthly to keep a longer archive."
image: "/wp-content/uploads/2026/10/search-console-performance-report.webp"
imageAlt: "search console performance report"
words: 2168
views: 17
format: "html"
---
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
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
.tok-sel { color: #9ece6a; }
.tok-prop{ color: #7fdbca; }

.bx-shot { margin: 18px 0 28px; border-radius: 10px; overflow: hidden; box-shadow: 0 2px 10px rgba(0,0,0,.15); }
.bx-shot img { display: block; width: 100%; }
.bx-shot-caption { font-size: 14px; color: var(--bx-charcoal-soft); text-align: center; margin: 8px 0 0; font-style: italic; }

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
table.bx-table tbody td { padding: 12px 14px; font-size: 17px; border-bottom: 1px solid #e7f2dd; }
table.bx-table tbody tr:nth-child(odd) { background: #f4faef; }
table.bx-table tbody tr:nth-child(even) { background: #ffffff; }

.bx-checklist { list-style: none; margin: 18px 0 28px; padding: 0; display: grid; gap: 12px; }
.bx-checklist li {
  background: #fff; border: 1px solid #e9e9e9; border-left: 4px solid var(--bx-green);
  border-radius: 8px; padding: 14px 16px 14px 44px; position: relative; font-size: 17px;
}
.bx-checklist li::before {
  content: "✓"; position: absolute; left: 14px; top: 13px; color: var(--bx-green-deep); font-weight: 800; font-size: 17px;
}
.bx-checklist b { color: var(--bx-charcoal); }

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

.bx-ad { text-align: center; margin: 34px 0; padding: 18px 0; border-top: 1px dashed #cfcfcf; border-bottom: 1px dashed #cfcfcf; }
</style>

<div id="bx-article">

<div class="bx-pills">
  <span class="bx-pill">SEO</span>
  <span class="bx-pill">Google Search Console</span>
</div>

<p>Hey! If you have ever stared at a spreadsheet of queries in Search Console and thought "okay, now what do I actually do with this," this one is for you. We are going to turn that raw table into a short list of pages you can fix this week.</p>

<p class="bx-lede"><em>Picture this: a page you wrote months ago is sitting on page two of Google, quietly collecting thousands of impressions and almost no clicks. You would never notice it by scrolling your own site. But a Search Console Performance Report would show it to you in about thirty seconds, if you know where to look.</em></p>

<div class="bx-section-head">
  <span class="bx-num">01</span>
  <h2 class="bx-h2" id="what-a-search-console-performance-report-actually-shows-you">What a Search Console Performance Report Actually Shows You</h2>
  <div class="bx-rule"></div>
</div>

<p>Open Search Console and click Performance in the left sidebar, and you land on the Search results view. This is the only place Google hands you real data about how people found your site in organic search, straight from its own logs rather than a third party estimate.</p>

<p>The Search Console Performance Report is built around one table and one chart, both of which respond live to whatever filters and date range you set at the top of the page. Every row in that table represents either a query, a page, a country, a device, or a search appearance type, depending on which tab you have selected.</p>

<p>Before you dig into the technique in this guide, it helps to have your property configured properly so the data you are reading is complete and accurate. Our <a href="/google-search-console-ai-powered-configuration/">guide to setting up Search Console</a> walks through verification and sitemap submission if you have not done that yet.</p>

<div class="bx-tip">
  <p class="bx-tip-label">Tip</p>
  <p>Set your date range to the last twenty eight days for day to day monitoring, but switch to three or six months whenever you are hunting for quick wins. A short window hides patterns that only show up over time.</p>
</div>

<div class="bx-ad">
  <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-3931314195561246" data-ad-slot="4249015278" data-ad-format="auto" data-full-width-responsive="true"></ins>
  <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
</div>

<div class="bx-section-head">
  <span class="bx-num">02</span>
  <h2 class="bx-h2" id="the-four-metrics-behind-every-number">The Four Metrics Behind Every Number</h2>
  <div class="bx-rule"></div>
</div>

<p>Every row in the Performance report reduces down to four measurements, and Google defines them precisely rather than leaving them open to interpretation. Clicks are, in Google's own words, how often someone clicked a link from Google to your site. Impressions count how often a link to your site was seen in results, even if nobody scrolled far enough to notice it, according to <a href="https://support.google.com/webmasters/answer/7042828?hl=en">Search Console Help</a>.</p>

<p>Click through rate is simply clicks divided by impressions, expressed as a percentage, and average position is where your link typically sat on the results page, counted from the top down. None of these four numbers tells the full story on its own, which is exactly why the Search Console Performance Report pairs them together in one view.</p>

<table class="bx-table">
  <thead><tr style="background:#2b2b2b !important;"><th style="background:#2b2b2b !important; color:#ffffff !important;">Metric</th><th style="background:#2b2b2b !important; color:#ffffff !important;">What It Measures</th><th style="background:#2b2b2b !important; color:#ffffff !important;">What To Watch For</th></tr></thead>
  <tbody>
    <tr><td>Clicks</td><td>Visits that started from a Google result</td><td>Flat clicks despite rising impressions</td></tr>
    <tr><td>Impressions</td><td>Times your link appeared, even unscrolled</td><td>High volume with little traffic to show</td></tr>
    <tr><td>Click through rate</td><td>Clicks as a share of impressions</td><td>A rate far below the average for that position</td></tr>
    <tr><td>Position</td><td>Average rank across all matching queries</td><td>Pages hovering just below the first page</td></tr>
  </tbody>
</table>

<div class="bx-fact">
  <span class="bx-fact-label">Did You Know</span>
  <p>An analysis of roughly four million Google results found the top ranking page captures about 27.6 percent of all clicks for its query, and the top three results combine for over half of them, according to <a href="https://backlinko.com/google-ctr-stats">Backlinko</a>.</p>
</div>

<div class="bx-section-head">
  <span class="bx-num">03</span>
  <h2 class="bx-h2" id="why-a-good-position-does-not-always-mean-clicks">Why a Good Position Does Not Always Mean Clicks</h2>
  <div class="bx-rule"></div>
</div>

<p>It is tempting to treat position as the only metric that matters, but click through rate can swing wildly between two pages sitting at the same spot. A benchmark study cited by <a href="https://www.semrush.com/blog/google-search-console-keywords">Semrush</a> puts average click through rate near 39.8 percent at position one, dropping to 18.7 percent at position two and 10.2 percent at position three, and the same research notes that only about 0.63 percent of searchers ever click something on page two at all.</p>

<p>The landscape has also shifted recently because of AI generated summaries appearing above the organic results. Ahrefs analyzed three hundred thousand keywords and found position one click through rate fell by roughly 34.5 percent when an AI Overview appeared on the page, and a separate study of seven hundred thousand keywords by Amsive found informational queries without a brand name lost around 20 percent of their clicks, as reported by <a href="https://searchengineland.com/google-ai-overviews-hurt-click-through-rates-454428">Search Engine Land</a>.</p>

<p>That shift matters for how you read your own Search Console Performance Report. A page that used to convert impressions into clicks reliably at position three might now show a lower click through rate simply because an AI summary sits above it, not because your content got worse.</p>

<div class="bx-ad">
  <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-3931314195561246" data-ad-slot="4249015278" data-ad-format="auto" data-full-width-responsive="true"></ins>
  <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
</div>

<div class="bx-section-head">
  <span class="bx-num">04</span>
  <h2 class="bx-h2" id="the-position-four-to-fifteen-opportunity">The Position Four to Fifteen Opportunity</h2>
  <div class="bx-rule"></div>
</div>

<p>Here is the actual quick win technique at the center of this guide. Open the Queries tab in your Search Console Performance Report, sort the table by impressions from highest to lowest, and scan for rows with an average position somewhere between four and fifteen. Those queries already rank, Google already trusts the page enough to show it often, but it has not quite broken into the top three where most of the clicks land.</p>

<p><a href="https://www.searchenginejournal.com/python-seo-striking-distance/423009/">Search Engine Journal</a> describes this group as striking distance keywords, originally defined as positions four through twenty, though the article notes the range is meant to be adjusted rather than treated as a fixed rule. A more recent playbook from <a href="https://www.gscwizard.com/learn/playbooks/striking-distance.html">GSC Wizard</a> narrows the practical sweet spot to positions five through fifteen, arguing that pushing a page from position fifteen to position three is a far easier lift than pushing it from position five.</p>

<p>That same playbook recommends ignoring any query with fewer than fifty impressions across a ninety day window, since smaller samples are too noisy to act on with confidence. One worked example it cites shows a query sitting at a 1.3 percent click through rate despite thirty four hundred impressions in ninety days, which is exactly the kind of row worth your time.</p>

<p>Once you have your short list, cross check the surviving queries against your existing keyword research to confirm search intent before you touch the page. Our <a href="/best-keyword-research-tools-compared/">comparison of keyword research tools</a> is a useful second opinion if a query looks promising but unfamiliar.</p>

<div class="bx-tip">
  <p class="bx-tip-label">Tip</p>
  <p>For each query in the four to fifteen range, open the matching page and check whether that exact phrase actually appears in the title tag, the first paragraph, and at least one heading. A Search Console Performance Report full of near misses, where the keyword is implied but never written out, is one of the easiest fixes you will find all month.</p>
</div>

<div class="bx-section-head">
  <span class="bx-num">05</span>
  <h2 class="bx-h2" id="stacking-query-page-country-and-device-filters">Stacking Query, Page, Country, and Device Filters</h2>
  <div class="bx-rule"></div>
</div>

<p>The dimension tabs along the top of the Search Console Performance Report, covering queries, pages, countries, devices, search appearance, and dates, are not meant to be used one at a time. According to <a href="https://support.google.com/webmasters/answer/17011259?hl=en">Search Console Help</a>, you can apply several filters together so the table only shows rows that match every condition at once.</p>

<p>A practical combination for the four to fifteen technique looks like this: filter to a single page, add a country filter for your main market, then switch to the Queries tab to see exactly which search terms are dragging that page's average position down. Flip to the Devices tab afterward, since a page that performs fine on desktop but badly on mobile often has a technical cause rather than a content one.</p>

<p>Before you act on any list of queries, filter out your own brand terms so they do not crowd out the generic opportunities you are actually looking for. Search Console has a built in way to do this, which our <a href="/branded-queries-filter-in-search-console/">guide to the branded queries filter</a> explains step by step, and a similar manual approach using combined filters is described by <a href="https://resignal.com/blog/how-to-find-seo-quick-wins-in-google-search-console-low-ctr-keywords/">Resignal</a>, which recommends a wide six month window when exporting data to spot topic patterns across many queries at once.</p>

<div class="bx-ad">
  <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-3931314195561246" data-ad-slot="4249015278" data-ad-format="auto" data-full-width-responsive="true"></ins>
  <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
</div>

<div class="bx-section-head">
  <span class="bx-num">06</span>
  <h2 class="bx-h2" id="common-mistakes-people-make-reading-the-report">Common Mistakes People Make Reading the Report</h2>
  <div class="bx-rule"></div>
</div>

<p>Most of the confusion around this report comes from treating it like a ranking tracker instead of a log of real search behavior. It is neither wrong nor broken when a number looks odd, it is usually just being measured differently than you expect.</p>

<p>If a page is missing from the Search Console Performance Report entirely, that is an indexing question, not a performance question, and pulling it apart with filters will not help. Our <a href="/url-inspection-tool-diagnose-indexing-problems/">walkthrough of the URL Inspection tool</a> is the right next step for that specific problem.</p>

<div class="bx-checklist">
  <li><b>Judging a page by total clicks alone.</b> Compare click through rate against the typical rate for that position before calling a page a failure.</li>
  <li><b>Acting on a query with only a handful of impressions.</b> Wait for a larger sample, roughly fifty impressions or more, before you change anything.</li>
  <li><b>Comparing data across two different date ranges that are different lengths.</b> Always compare periods of equal length, such as this month against last month.</li>
  <li><b>Forgetting that average position is an average.</b> A page can show position six while actually ranking first for one query and twentieth for another.</li>
  <li><b>Chasing every dip in the chart.</b> Short term wiggles are normal; a real trend needs several weeks to confirm itself.</li>
</div>

<div class="bx-ad">
  <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-3931314195561246" data-ad-slot="4249015278" data-ad-format="auto" data-full-width-responsive="true"></ins>
  <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
</div>

<div class="bx-section-head">
  <span class="bx-num">07</span>
  <h2 class="bx-h2" id="what-the-data-will-not-tell-you">What the Data Will Not Tell You</h2>
  <div class="bx-rule"></div>
</div>

<p>A Search Console Performance Report is honest but incomplete, and knowing its edges saves you from chasing phantom problems. Google retains this data for only sixteen months, after which older rows are permanently removed from the interface, as noted by <a href="https://seotesting.com/google-search-console/data-limitations/">SEO Testing</a>.</p>

<p>The numbers you see are also not instant. Search Console itself warns of a lag between when activity happens and when it shows up in your account, and in practice that gap typically runs about two to three days, per the same source and Google's own <a href="https://support.google.com/webmasters/answer/96568?hl=en">About Search Console data</a> documentation. Rows for very rare, low volume queries are also omitted from the table to protect searcher privacy, which mostly affects long tail terms rather than the mid volume rows this guide focuses on.</p>

<p>Pair the Performance report with your crawl data for a fuller picture, since a page can look fine in one and still have a problem the other would catch. Our <a href="/understanding-crawl-stats-report/">guide to the Crawl Stats report</a> covers the crawling side of that equation.</p>

<div class="bx-tip">
  <p class="bx-tip-label">Tip</p>
  <p>Export your Performance report data on a regular schedule, monthly works well, so you keep a running archive beyond the sixteen month window Search Console itself retains.</p>
</div>

<div class="bx-faq">
  <div class="bx-faq-item open">
    <button class="bx-faq-q"><span class="bx-faq-num">1</span>What is a Search Console Performance Report used for?</button>
    <div class="bx-faq-a"><p>It shows real data on how your site appeared and performed in Google Search results, broken down by query, page, country, device, and date, so you can see which pages earn clicks and which ones only earn impressions.</p></div>
  </div>
  <div class="bx-faq-item open">
    <button class="bx-faq-q"><span class="bx-faq-num">2</span>Why does my average position look higher than where I actually rank?</button>
    <div class="bx-faq-a"><p>Average position is calculated across every query and every search where your page appeared, so a page ranking first for a rare query and twentieth for a common one will show a blended middle number rather than either extreme.</p></div>
  </div>
  <div class="bx-faq-item open">
    <button class="bx-faq-q"><span class="bx-faq-num">3</span>How far back does Search Console data go?</button>
    <div class="bx-faq-a"><p>The Performance report keeps roughly sixteen months of history. Anything older than that is deleted from the interface, so it is worth exporting your data periodically if you want a longer archive.</p></div>
  </div>
  <div class="bx-faq-item open">
    <button class="bx-faq-q"><span class="bx-faq-num">4</span>What counts as a good quick win in the four to fifteen position range?</button>
    <div class="bx-faq-a"><p>Look for queries with at least fifty impressions over a recent ninety day stretch, an average position between four and fifteen, and a click through rate noticeably below what similar positions typically earn. Those are the rows most likely to respond to a focused edit.</p></div>
  </div>
  <div class="bx-faq-item open">
    <button class="bx-faq-q"><span class="bx-faq-num">5</span>Why is my click through rate lower than it used to be at the same position?</button>
    <div class="bx-faq-a"><p>Features like AI generated summaries now sit above organic results for many informational queries and absorb a share of clicks that used to go to the top ranking pages, so a lower click through rate does not always mean your content declined.</p></div>
  </div>
</div>

<div class="bx-learn">
  <h2 id="learn-today">Learn Today</h2>
  <div class="bx-learn-grid">
    <div class="bx-learn-card"><span class="bx-learn-num">1</span><div><h4>Impression</h4><p>A count of how often your link was shown in a search result, whether or not anyone noticed it.</p></div></div>
    <div class="bx-learn-card"><span class="bx-learn-num">2</span><div><h4>Click Through Rate</h4><p>Clicks divided by impressions, shown as a percentage, for a query, page, or any other dimension.</p></div></div>
    <div class="bx-learn-card"><span class="bx-learn-num">3</span><div><h4>Average Position</h4><p>The typical rank of your link across every matching search, counted from the top of the results down.</p></div></div>
    <div class="bx-learn-card"><span class="bx-learn-num">4</span><div><h4>Striking Distance Keyword</h4><p>A query ranking close enough to the first page that a small content edit can realistically push it higher.</p></div></div>
    <div class="bx-learn-card"><span class="bx-learn-num">5</span><div><h4>Search Appearance</h4><p>A dimension showing which special result types, such as rich results, your pages qualified for.</p></div></div>
    <div class="bx-learn-card"><span class="bx-learn-num">6</span><div><h4>AI Overview</h4><p>A generated summary Google can place above organic results for some queries, which can change click patterns.</p></div></div>
  </div>
</div>

<div class="bx-cta">
  <h3>Turn Your Performance Report Into a To Do List</h3>
  <p>Explore more Brandella Journal guides on SEO and digital marketing.</p>
  <div class="bx-cta-btns">
    <a href="/">Browse All Guides</a>
    <a class="bx-cta-outline" href="/google-search-console-ai-powered-configuration/">Set Up Search Console Properly</a>
  </div>
</div>

</div>

<script>
document.querySelectorAll('.bx-faq-item').forEach(function(item){
  var q = item.querySelector('.bx-faq-q');
  var a = item.querySelector('.bx-faq-a');
  a.style.maxHeight = a.scrollHeight + 'px';
  q.addEventListener('click', function(){
    var isOpen = item.classList.contains('open');
    if (isOpen) {
      item.classList.remove('open');
      a.style.maxHeight = '0px';
    } else {
      item.classList.add('open');
      a.style.maxHeight = a.scrollHeight + 'px';
    }
  });
});
</script>
