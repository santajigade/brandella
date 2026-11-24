---
title: "Google Ads Negative Keywords: 7 Essential Tips"
slug: "google-ads-negative-keywords"
date: "2026-10-08T11:49:30"
updated: "2026-10-08T11:50:01"
author: "santajigade"
categories: ["google-ads"]
primaryCategory: "google-ads"
description: "Learn how Google Ads negative keywords actually work in 2026: match types, shared lists, campaign vs ad group placement, and real Performance Max limits."
focusKeyword: "Google Ads negative keywords"
takeaways:
  - "Negative keywords stop your ads showing for chosen searches and can be set at account, campaign or ad group level."
  - "Broad match negatives block queries containing all the words in any order, phrase match requires the same order, and exact match blocks only that search."
  - "Shared negative keyword lists apply one set of exclusions across many campaigns, with common starting terms like 'free', 'jobs', 'DIY' and 'refund'."
  - "Review the search terms report weekly or biweekly for irrelevant queries, and avoid negatives that conflict with keywords you are actively bidding on."
  - "In Performance Max, account level negatives apply automatically, campaign negatives were raised from 100 to 10,000, and negatives only cover Search and Shopping inventory."
image: "/wp-content/uploads/2026/10/Google-Ads-negative-keywords.webp"
imageAlt: "Google Ads negative keywords"
words: 2190
views: 12
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
</style>

<div id="bx-article">

<div class="bx-pills">
  <span class="bx-pill">Paid Media</span>
  <span class="bx-pill">Google Ads</span>
</div>

<p>Hey! If your Google Ads account has ever burned through budget on clicks that were never going to turn into a sale, this one is for you.</p>

<p class="bx-lede"><em>Picture this. Your campaign looks healthy, impressions keep climbing, clicks keep rolling in, but sales barely move. Open the search terms report and you will usually find the real story: people searching for things you do not sell, cannot afford, or were never going to buy from you anyway. Google Ads negative keywords exist to close exactly that gap, and getting them right is one of the fastest ways to make an existing budget perform better without spending anything extra.</em></p>

<div class="bx-section-head">
  <span class="bx-num">01</span>
  <h2 class="bx-h2" id="what-are-google-ads-negative-keywords">What Are Google Ads Negative Keywords?</h2>
  <div class="bx-rule"></div>
</div>

<p>Google Ads negative keywords are terms and phrases you add to a campaign or ad group specifically so your ad will not show when someone searches for them. Think of them as a filter sitting between the keywords you are actively bidding on and the live auction, catching searches that are close enough to trigger a match but wrong enough to waste the click.</p>

<p>A plumbing company bidding on "drain cleaning" does not want to show up for "how to unclog a drain yourself." Negative keywords are how you teach the system that distinction without touching a single bid.</p>

<p>They can live at three levels inside an account: the whole account, a single campaign, or one ad group, and each level solves a different problem, covered shortly.</p>

<div class="bx-section-head">
  <span class="bx-num">02</span>
  <h2 class="bx-h2" id="negative-keyword-match-types-broad-phrase-and-exact">Negative Keyword Match Types: Broad, Phrase, and Exact</h2>
  <div class="bx-rule"></div>
</div>

<p>Setting up Google Ads negative keywords correctly starts with match type, since broad, phrase, and exact behave differently and change how much traffic gets blocked. Broad match is the default: it blocks a search only when every word in your negative appears somewhere in the query, in any order, per <a href="https://support.google.com/google-ads/answer/12437241">Google's own Ads Help documentation</a>.</p>

<p>Phrase match tightens that by requiring the words to appear in the same order, though extra words can still surround them. Exact match is the strictest of the three, blocking only that specific search with nothing added before or after it, as the table below shows.</p>

<p>Getting this right partly comes down to understanding <a href="/how-google-ads-auction-works/">how the Google Ads auction actually decides which ads are even eligible to compete</a> for a given search, since a well placed negative removes you from that competition entirely rather than just lowering your rank in it.</p>

<table class="bx-table">
  <thead><tr style="background:#2b2b2b !important;"><th style="background:#2b2b2b !important; color:#ffffff !important;">Match Type</th><th style="background:#2b2b2b !important; color:#ffffff !important;">Written As</th><th style="background:#2b2b2b !important; color:#ffffff !important;">Blocks This Search</th><th style="background:#2b2b2b !important; color:#ffffff !important;">Still Shows For</th></tr></thead>
  <tbody>
    <tr><td>Broad match</td><td>running shoes</td><td>blue running shoes, shoes running</td><td>running shoe, blue tennis shoes</td></tr>
    <tr><td>Phrase match</td><td>"running shoes"</td><td>blue running shoes</td><td>shoes running</td></tr>
    <tr><td>Exact match</td><td>[running shoes]</td><td>running shoes (only)</td><td>blue running shoes</td></tr>
  </tbody>
</table>


<div class="bx-section-head">
  <span class="bx-num">03</span>
  <h2 class="bx-h2" id="negative-keyword-lists-that-work-across-every-campaign">Negative Keyword Lists That Work Across Every Campaign</h2>
  <div class="bx-rule"></div>
</div>

<p>Typing the same Google Ads negative keywords into ten different campaigns, one at a time, is exactly the kind of busywork negative keyword lists were built to remove. A negative keyword list is a single reusable set of exclusions you can apply to as many campaigns as you want, and updating the list once updates every campaign that uses it, per <a href="https://support.google.com/google-ads/answer/2453983">Google's documentation on negative keyword lists</a>.</p>

<p>Google also offers a separate, account wide layer called account level negative keywords, set once in Account Settings, that automatically apply to all eligible Search and Shopping inventory without being attached to any single campaign. Independent consultant Nils Rooijmans documented this option rolling out, noting it supports broad, exact, or phrase match like any other negative, per <a href="https://nilsrooijmans.com/daily/performance-max-account-level-negative-keywords-are-here">his write up on account level exclusions</a>.</p>

<p>A good shared list usually covers terms that have nothing to do with your business at all: "free," "jobs," "DIY," and "refund" are common starting points, saved once and reused everywhere rather than rebuilt per campaign.</p>

<div class="bx-tip">
  <p class="bx-tip-label">Tip</p>
  <p>Start one shared negative keyword list with universal exclusions like "free," "jobs," "DIY," and "refund," then apply it to every campaign in the account before you build anything more specific. It pairs well with the broader checklist in our <a href="/25-google-ads-optimization-tips/">Google Ads optimization tips guide</a>.</p>
</div>

<div class="bx-section-head">
  <span class="bx-num">04</span>
  <h2 class="bx-h2" id="campaign-level-negatives-vs-ad-group-level-negatives">Campaign Level Negatives vs Ad Group Level Negatives</h2>
  <div class="bx-rule"></div>
</div>

<p>Negative keywords also differ by where you place them. A campaign level negative blocks a search across every ad group in that campaign, while an ad group level negative only blocks it for that one ad group, leaving the rest untouched.</p>

<p>This matters most when a campaign is split into tightly themed ad groups by product line. If one ad group targets "wedding photography" and another targets "newborn photography," adding "wedding" as an ad group level negative on the newborn ad group stops wedding searches from leaking in, without touching the wedding ad group at all.</p>

<p>A practical way to think about Google Ads negative keywords is as layers, broadest to narrowest: a shared list first, campaign level negatives second, and ad group level negatives last, so overlapping match types never trigger the wrong ad group.</p>

<p>A common proactive habit is adding the exact match version of every ad group's own keywords as negatives on every other ad group in that campaign, which keeps tightly related ad groups from quietly stealing each other's traffic.</p>

<div class="bx-tip">
  <p class="bx-tip-label">Tip</p>
  <p>Add the exact match version of each ad group's own keywords as a negative on every sibling ad group in the same campaign, so one tightly targeted ad never steals clicks from another.</p>
</div>


<div class="bx-section-head">
  <span class="bx-num">05</span>
  <h2 class="bx-h2" id="using-the-search-terms-report-to-find-new-negatives">Using the Search Terms Report to Find New Negatives</h2>
  <div class="bx-rule"></div>
</div>

<p>The search terms report shows the real, literal queries that triggered your ads, different from the keywords you actually bid on. It is the best place to find your next negative, because it shows exactly what Google already decided was a close enough match.</p>

<p>A weekly or biweekly pass through this report, sorted by cost or by clicks with zero conversions, usually surfaces the worst offenders fast. Anything irrelevant or clearly a different intent than your offer is a candidate for exclusion.</p>

<p>Go further than a one by one read, and build a pivot table instead: each search term as a row, a count of ad groups it appears in as the value. A term spread across many ad groups is usually a sign your Google Ads negative keywords need to move up a level, from an ad group into the campaign or the shared list.</p>


<div class="bx-section-head">
  <span class="bx-num">06</span>
  <h2 class="bx-h2" id="the-costly-mistakes-most-advertisers-make-with-negatives">The Costly Mistakes Most Advertisers Make With Negatives</h2>
  <div class="bx-rule"></div>
</div>

<p>Negative keywords are simple in concept and easy to get wrong in practice, and the mistakes almost always cost money quietly rather than obviously.</p>

<p>The most damaging mistake is a direct conflict between a negative keyword and a keyword you are actively bidding on. PPC blog Karooya points out that adding a negative which matches one of your own bidded terms will quietly block that keyword from showing, often with no clear warning in the interface, per its <a href="https://www.karooya.com/blog/common-negative-keyword-mistakes/">rundown of common negative keyword mistakes</a>.</p>

<p>Over blocking is the second most common mistake with Google Ads negative keywords. A broad match negative added casually can remove far more legitimate traffic than intended, so test a phrase or exact match version first on anything you are not completely sure about.</p>

<p>A string of irrelevant clicks does not just waste spend either. It drags down the click through rate on that ad group, which can quietly pull down your <a href="/google-ads-quality-score-explained/">Quality Score</a> over time, making every future click in that ad group more expensive than it needs to be.</p>

<div class="bx-checklist">
  <li><b>Over blocking with broad match negatives.</b> A single broad negative can silently remove far more traffic than intended, so test a narrower phrase or exact match version first.</li>
  <li><b>Conflicting positive and negative keywords.</b> Adding a negative that matches a term you are actively bidding on will quietly stop that ad from ever showing again.</li>
  <li><b>Negatives added at the wrong level.</b> A term that belongs on one ad group ends up on the whole campaign, blocking traffic other ad groups still needed.</li>
  <li><b>Shared lists nobody reviews again.</b> A list built once and never revisited keeps blocking the same handful of terms while new wasteful searches pile up unseen.</li>
  <li><b>Assuming Performance Max behaves like Search.</b> Negative keyword lists and ad group level exclusions that work in Search campaigns do not automatically carry over to Performance Max.</li>
</div>

<div class="bx-section-head">
  <span class="bx-num">07</span>
  <h2 class="bx-h2" id="google-ads-negative-keywords-and-performance-max">Google Ads Negative Keywords and Performance Max</h2>
  <div class="bx-rule"></div>
</div>

<p>Performance Max is where negative keyword support genuinely differs from Search, and it is worth understanding exactly where the limits sit rather than assuming it behaves identically.</p>

<p>Account level negative keywords, set once in Account Settings, automatically apply to Performance Max the same way they apply to Search and Shopping, which is currently the most reliable way to block a term across every Performance Max campaign in the account at once, per <a href="https://support.google.com/google-ads/answer/15726455">Google's help page on negative keywords in Performance Max</a>.</p>

<p>Campaign specific negatives in Performance Max had a real, documented limitation worth knowing about. They originally required contacting a Google representative and were capped at only 100 terms per campaign, until Google raised that cap to 10,000, matching Search campaigns, after advertisers pushed back on the original limit, as reported by <a href="https://ppc.land/google-raises-negative-keywords-limit-to-10-000-for-performance-max-campaigns/">PPC Land</a>.</p>

<p>Negative keyword lists, the shared sets that work so well across Search campaigns, remain a newer and uneven part of the picture. Search Engine Land reported advertisers seeing list options appear inside Performance Max settings while Google's own help documentation had not yet confirmed full support everywhere, a feature rolling out unevenly rather than all at once, per its <a href="https://searchengineland.com/google-tests-negative-keyword-lists-pmax-459116">coverage of negative keyword lists being tested in Performance Max</a>.</p>

<p>One real limitation has not changed: Performance Max negative keywords, at every level, only apply to Search and Shopping inventory inside that campaign, not to Display, video, or other automated placements, so a negative alone will never fully stop an unwanted placement outside those two inventory types.</p>

<p>If you are deciding how much manual control you actually need, compare <a href="/search-campaign-vs-performance-max/">Search campaigns against Performance Max</a> before committing budget. Our <a href="/how-to-optimize-performance-max-campaign-step-by-step/">step by step guide to optimizing a Performance Max campaign</a> covers where negatives fit alongside audience signals and asset groups.</p>

<div class="bx-fact">
  <span class="bx-fact-label">Did You Know</span>
  <p>Performance Max campaigns could hold only 100 negative keywords each, added through a Google representative, until Google raised the limit to 10,000 per campaign in March 2025 to match Search campaigns. <a href="https://www.searchenginejournal.com/google-pmax-negative-keyword-limit-increase/542336/">Search Engine Journal</a> reported the change after advertisers said the original cap felt too restrictive for real campaign management.</p>
</div>


<div class="bx-faq">
  <div class="bx-faq-item open">
    <button class="bx-faq-q"><span class="bx-faq-num">1</span>What are Google Ads negative keywords, exactly?</button>
    <div class="bx-faq-a"><p>Google Ads negative keywords are terms you add to an account, campaign, or ad group so your ad will not show for searches containing them, which stops wasted spend on clicks that were never going to convert.</p></div>
  </div>
  <div class="bx-faq-item open">
    <button class="bx-faq-q"><span class="bx-faq-num">2</span>What is the difference between broad, phrase, and exact negative match types?</button>
    <div class="bx-faq-a"><p>Broad match blocks a search when every word in the negative appears anywhere in the query, phrase match requires the same order, and exact match only blocks that specific search with nothing added before or after it.</p></div>
  </div>
  <div class="bx-faq-item open">
    <button class="bx-faq-q"><span class="bx-faq-num">3</span>Can I share the same negative keyword list across multiple campaigns?</button>
    <div class="bx-faq-a"><p>Yes. A negative keyword list is built once and applied to as many campaigns as you want, and updating it in one place updates it everywhere, far faster than editing each campaign separately.</p></div>
  </div>
  <div class="bx-faq-item open">
    <button class="bx-faq-q"><span class="bx-faq-num">4</span>Should negative keywords go at the campaign level or the ad group level?</button>
    <div class="bx-faq-a"><p>Use the campaign level for terms that should never trigger any ad group in that campaign, and the ad group level when you only want to stop one specific ad group from showing while leaving the rest of the campaign untouched.</p></div>
  </div>
  <div class="bx-faq-item open">
    <button class="bx-faq-q"><span class="bx-faq-num">5</span>Do negative keywords work the same way in Performance Max campaigns?</button>
    <div class="bx-faq-a"><p>Not entirely. Account level negatives apply to Performance Max automatically, campaign specific negatives in Performance Max only apply to Search and Shopping inventory, and negative keyword list support inside Performance Max is still rolling out unevenly.</p></div>
  </div>
</div>

<div class="bx-learn">
  <h2 id="learn-today">Learn Today</h2>
  <div class="bx-learn-grid">
    <div class="bx-learn-card"><span class="bx-learn-num">1</span><div><h4>Negative Keyword</h4><p>A term you exclude so your ad will not show for searches containing it.</p></div></div>
    <div class="bx-learn-card"><span class="bx-learn-num">2</span><div><h4>Match Type</h4><p>The setting, broad, phrase, or exact, that controls how closely a search must match a negative keyword.</p></div></div>
    <div class="bx-learn-card"><span class="bx-learn-num">3</span><div><h4>Negative Keyword List</h4><p>A shared set of exclusions you can apply to several campaigns at once.</p></div></div>
    <div class="bx-learn-card"><span class="bx-learn-num">4</span><div><h4>Search Terms Report</h4><p>The report showing the actual queries that triggered your ads.</p></div></div>
    <div class="bx-learn-card"><span class="bx-learn-num">5</span><div><h4>Account Level Negative</h4><p>An exclusion set once that applies automatically across every eligible campaign, Performance Max included.</p></div></div>
    <div class="bx-learn-card"><span class="bx-learn-num">6</span><div><h4>Performance Max</h4><p>A goal based campaign type that uses automation across Google's full ad inventory.</p></div></div>
  </div>
</div>

<div class="bx-cta">
  <h3>Stop Paying for Clicks That Were Never Going to Convert</h3>
  <p>Explore more Brandella Journal guides on SEO and digital marketing.</p>
  <div class="bx-cta-btns">
    <a href="/">Browse All Guides</a>
    <a class="bx-cta-outline" href="/google-ads-success-3-key-factors/">See What Actually Drives Google Ads Success</a>
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
