---
title: "Nofollow vs Dofollow Links: Which External Links Help SEO"
slug: "nofollow-vs-dofollow-links"
date: "2026-10-01T04:49:08"
updated: "2026-11-13T11:30:00"
author: "santajigade"
categories: ["off-page-seo"]
primaryCategory: "off-page-seo"
description: "Dofollow vs nofollow external links explained with HTML examples, when to use each, and how to track outbound link clicks in GA4."
focusKeyword: "dofollow external links"
takeaways:
  - "A dofollow link is a normal link with no nofollow, sponsored or ugc value in its rel attribute."
  - "Since September 2019 Google treats nofollow, sponsored and ugc as hints rather than strict rules."
  - "Use rel=\"sponsored\" for paid or affiliate links and rel=\"ugc\" for links in comments and forums."
  - "A healthy backlink profile naturally mixes dofollow and nofollow links."
  - "GA4 can track outbound link clicks automatically through enhanced measurement."
image: "/wp-content/uploads/2026/10/nofollow-vs-dofollow-links.webp"
imageAlt: "nofollow vs dofollow links"
words: 2481
views: 19
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
  <span class="bx-pill">Off-Page SEO</span>
</div>

<p>Hey! If you have ever stared at a backlink report and wondered why some links seem to matter more than others, this guide is for you. We are going to clear up exactly what that tiny rel attribute in your code is doing to your rankings.</p>

<p class="bx-lede"><em>Picture this: a major publication mentions your brand, but buried in the link code is a single word that decides whether that mention quietly lifts your rankings or just sends a trickle of referral visitors. That word is the entire nofollow vs dofollow links debate, and most marketers still get it wrong because they are working from rules Google rewrote back in 2019.</em></p>

<div class="bx-section-head">
  <span class="bx-num">01</span>
  <h2 class="bx-h2" id="nofollow-vs-dofollow-links-what-each-one-actually-means">Nofollow vs Dofollow Links: What Each One Actually Means</h2>
  <div class="bx-rule"></div>
</div>

<p>A dofollow link is just an ordinary hyperlink. There is no special markup, no rel value, nothing extra. By default, every link on the web is dofollow unless a site owner deliberately adds an attribute to change that behavior.</p>

<p>A nofollow link carries <code>rel="nofollow"</code> in its anchor tag. It was originally designed as a flat instruction telling search engines not to pass any ranking credit, often called link equity, through that particular connection.</p>

<p>Here is a detail that trips people up: dofollow was never an official term Google invented. SEOs coined it as the natural opposite of nofollow, and it stuck, even though you will never find it in Google's own documentation.</p>

<p>Getting this terminology straight matters beyond trivia. When you brief a writer, a client or an outreach partner, the nofollow vs dofollow links distinction is usually the very first thing you need to agree on, since it decides how a placement gets valued, priced and reported later.</p>

<div class="bx-tip">
  <p class="bx-tip-label">Tip</p>
  <p>If you want a deeper refresher on how ranking value actually moves between pages before you dig into nofollow versus dofollow links, read our <a href="/link-equity-explained/">link equity explained</a> guide first.</p>
</div>

<div class="bx-section-head">
  <span class="bx-num">02</span>
  <h2 class="bx-h2" id="a-short-history-why-nofollow-was-invented-in-2005">A Short History: Why Nofollow Was Invented in 2005</h2>
  <div class="bx-rule"></div>
</div>

<p>The nofollow attribute was not part of Google's original plan for the web. It was introduced in 2005 as a joint effort among Google, Yahoo and the blogging platforms of the time, created specifically to fight a flood of comment spam.</p>

<p>Before nofollow existed, spammers would drop links in blog comments purely to harvest ranking credit, with zero intention of adding anything useful to the conversation. Attaching nofollow to comment links removed the financial incentive almost overnight.</p>

<p><a href="https://www.screamingfrog.co.uk/learn-seo/nofollow/">Screaming Frog</a> notes that this original 2005 use case, blocking spammy comment links, is still the closest thing to the attribute's original intent, even though its role has expanded dramatically since then.</p>

<div class="bx-fact">
  <span class="bx-fact-label">Did You Know</span>
  <p>The nofollow attribute has been part of the web's toolkit for roughly two decades, first appearing in 2005 purely as a spam prevention measure, according to <a href="https://www.screamingfrog.co.uk/learn-seo/nofollow/">Screaming Frog</a>.</p>
</div>


<div class="bx-section-head">
  <span class="bx-num">03</span>
  <h2 class="bx-h2" id="google-s-2019-announcement-changed-the-rules-completely">Google's 2019 Announcement Changed the Rules Completely</h2>
  <div class="bx-rule"></div>
</div>

<p>On September 10, 2019, Google published a post called <a href="https://developers.google.com/search/blog/2019/09/evolving-nofollow-new-ways-to-identify">Evolving nofollow</a>, and it reshaped how every SEO thinks about link attributes. Two brand new values arrived alongside nofollow: <code>rel="sponsored"</code> and <code>rel="ugc"</code>.</p>

<p>The bigger shift was philosophical. Google announced that starting March 1, 2020, nofollow, sponsored and ugc would all be treated as hints for crawling, indexing and ranking, not as absolute commands Google was forced to obey.</p>

<p>Google's own Danny Sullivan was blunt about it at the time, telling publishers through <a href="https://www.seroundtable.com/google-nofollow-link-attribute-change-sponsored-ugc-28196.html">Search Engine Roundtable</a>, "you literally don't have to change anything if you don't want." Nothing was mandatory, but the meaning of the attribute itself had quietly changed forever.</p>

<p>Gary Illyes later confirmed through <a href="https://www.searchenginejournal.com/meta-robots-nofollow-hint/325591/">Search Engine Journal</a> that even the meta robots nofollow tag was folded into this same hint based treatment, aligning every nofollow style signal under one consistent philosophy.</p>

<p>This hint based model is the single most misunderstood part of the nofollow vs dofollow links conversation. The old assumption was that nofollow completely blocked a page from being crawled or indexed, full stop. Google now reserves the right to crawl, index and even weigh that link if its systems decide the context is strong enough to justify it.</p>

<div class="bx-section-head">
  <span class="bx-num">04</span>
  <h2 class="bx-h2" id="nofollow-vs-sponsored-vs-ugc-when-to-use-each-attribute">Nofollow vs Sponsored vs UGC: When to Use Each Attribute</h2>
  <div class="bx-rule"></div>
</div>

<p>Now that three attributes exist, picking the right one matters for staying inside Google's link guidelines. <a href="https://yoast.com/outbound-link-sponsored-nofollow-ugc-attributes/">Yoast</a> frames the decision simply: match the attribute to why the link exists, not just whether you trust the destination.</p>

<p>Use <code>rel="sponsored"</code> for anything compensated: paid placements, affiliate links, advertorials. Use <code>rel="ugc"</code> for links your visitors create themselves, such as comments, forum posts and reviews. Reach for plain <code>rel="nofollow"</code> for everything else you simply do not want to vouch for.</p>

<table class="bx-table">
  <thead><tr style="background:#2b2b2b !important;"><th style="background:#2b2b2b !important; color:#ffffff !important;">Attribute</th><th style="background:#2b2b2b !important; color:#ffffff !important;">Typical use case</th><th style="background:#2b2b2b !important; color:#ffffff !important;">Passes link equity?</th></tr></thead>
  <tbody>
    <tr><td>No attribute (dofollow)</td><td>A genuine editorial endorsement</td><td>Yes, by default</td></tr>
    <tr><td><code>rel="nofollow"</code></td><td>Untrusted or unverified destinations</td><td>Treated only as a hint</td></tr>
    <tr><td><code>rel="sponsored"</code></td><td>Paid, affiliate or advertising links</td><td>Treated only as a hint</td></tr>
    <tr><td><code>rel="ugc"</code></td><td>Comments, forums and reviews</td><td>Treated only as a hint</td></tr>
  </tbody>
</table>

<p>Mislabeling matters more than it looks. Google's own <a href="https://developers.google.com/search/blog/2019/09/evolving-nofollow-new-ways-to-identify">guidance</a> still expects paid links to carry at least one blocking signal, and sites that leave sponsored placements as plain, unmarked dofollow links risk a manual action for unnatural linking rather than a quiet algorithmic shrug.</p>

<div class="bx-tip">
  <p class="bx-tip-label">Tip</p>
  <p>You can combine values, such as <code>rel="nofollow sponsored"</code>, since not every search engine supports the newer attributes yet. When in doubt, pair sponsored or ugc with nofollow for broader compatibility.</p>
</div>


<div class="bx-section-head">
  <span class="bx-num">05</span>
  <h2 class="bx-h2" id="do-dofollow-links-still-beat-nofollow-links-in-2026">Do Dofollow Links Still Beat Nofollow Links in 2026?</h2>
  <div class="bx-rule"></div>
</div>

<p>Mostly yes, but the gap is smaller and blurrier than most people assume. <a href="https://searchengineland.com/google-doesnt-pass-pagerank-on-nofollow-links-heres-why-you-still-see-them-in-gsc-320636">Search Engine Land</a> confirmed that Google still does not pass PageRank through nofollow links, even though they appear in your Search Console link report for transparency.</p>

<p>John Mueller explained that Google shows nofollow links in that report simply because "it's still a link on the web, and users may be using those to reach your website," which is a traffic signal, not a ranking signal.</p>

<p><a href="https://ahrefs.com/blog/nofollow-ugc-sponsored/">Ahrefs</a> research found that about 10.6 percent of backlinks pointing to large sites already carry a nofollow attribute, and Ahrefs analyst Patrick Stox noted that even giants like Wikipedia, Forbes and CNN routinely nofollow their outbound links.</p>

<p>That means a nofollow link from a site with real traffic and trust can still send visitors, build brand recognition and occasionally get picked up elsewhere as a genuine dofollow citation, even without passing direct ranking credit itself.</p>

<p>In practical terms, this is why experienced link builders stopped treating the nofollow vs dofollow links question as a simple yes or no filter. A nofollow mention on a page your audience actually reads will usually outperform a dofollow link buried in a low quality directory nobody visits.</p>

<p>Many digital PR and guest posting negotiations still hinge entirely on whether a mention will be follow or no follow, but fixating on that single checkbox misses the bigger picture. A relevant mention on a site with an engaged, active audience often delivers more qualified traffic than a technically followed link sitting on a page with almost no real readership, regardless of which rel attribute ends up in the final markup.</p>

<div class="bx-fact">
  <span class="bx-fact-label">Did You Know</span>
  <p>According to <a href="https://ahrefs.com/blog/nofollow-ugc-sponsored/">Ahrefs</a>, roughly 10.6 percent of all backlinks to large websites are nofollow, while the newer sponsored and ugc attributes combined still appear on well under one percent of links.</p>
</div>


<div class="bx-section-head">
  <span class="bx-num">06</span>
  <h2 class="bx-h2" id="common-mistakes-with-nofollow-vs-dofollow-links">Common Mistakes With Nofollow vs Dofollow Links</h2>
  <div class="bx-rule"></div>
</div>

<p>Most of the confusion around nofollow vs dofollow links comes down to a handful of repeated mistakes, and nearly all of them are easy to fix once you can spot them.</p>

<p><a href="https://learn.g2.com/google-link-guidelines?hsLang=en">G2's own breakdown</a> of Google's link guidelines points out that many site owners still assume nofollow equals worthless, when in reality a nofollow mention from an authoritative publisher can still drive meaningful referral traffic and brand lift.</p>

<div class="bx-checklist">
  <li><b>Assuming every nofollow link is a waste of outreach time.</b> Judge a placement by its traffic and audience fit too, not only the rel attribute.</li>
  <li><b>Leaving every guest post link as plain dofollow.</b> Read our <a href="/guest-blogging-for-seo-best-practices/">guest blogging best practices</a> guide, since most guest posts should carry sponsored or ugc depending on how the placement was earned.</li>
  <li><b>Never auditing your own outbound links.</b> Use a crawler to find pages where comments or widgets are quietly leaking dofollow links to untrusted destinations.</li>
  <li><b>Ignoring toxic backlinks pointing back at you.</b> Review our <a href="/how-to-identify-remove-toxic-backlinks-safely/">guide on identifying and removing toxic backlinks</a> so a bad neighborhood of links does not drag your profile down.</li>
  <li><b>Forgetting to disclose paid placements at all.</b> Any compensated link needs sponsored or nofollow, full stop, regardless of how the relationship is framed elsewhere.</li>
</div>


<div class="bx-section-head">
  <span class="bx-num">07</span>
  <h2 class="bx-h2" id="how-to-check-if-an-external-link-is-dofollow-or-nofollow">How to Check if an External Link Is Dofollow or Nofollow</h2>
  <div class="bx-rule"></div>
</div>

<p>There is no such thing as a <code>rel="dofollow"</code> attribute. A dofollow external link is simply a normal link with no <code>nofollow</code>, <code>sponsored</code> or <code>ugc</code> value in its <code>rel</code> attribute. So checking a link means looking for what is missing, not for a dofollow label.</p>

<pre><code>&lt;!-- Dofollow external link (passes link signals) --&gt;
&lt;a href="https://example.com/guide/"&gt;helpful guide&lt;/a&gt;

&lt;!-- Nofollow external link --&gt;
&lt;a href="https://example.com/guide/" rel="nofollow"&gt;helpful guide&lt;/a&gt;

&lt;!-- Paid or affiliate link --&gt;
&lt;a href="https://example.com/product/" rel="sponsored"&gt;product&lt;/a&gt;</code></pre>

<p>Four quick ways to check any page:</p>

<div class="bx-checklist">
  <li><b>Inspect the link.</b> Right click the link in Chrome, choose Inspect and read the <code>rel</code> value in the highlighted HTML.</li>
  <li><b>View page source.</b> Press Ctrl+U, then Ctrl+F for <code>rel="</code> to see every link attribute on the page.</li>
  <li><b>Use a browser extension.</b> SEO extensions that highlight nofollow links mark them in a different colour so you can scan a whole page in seconds.</li>
  <li><b>Crawl the whole site.</b> A crawler like <a href="/screaming-frog-seo-spider-beginners-guide/">Screaming Frog SEO Spider</a> lists every outbound link with its rel value, which is the fastest way to audit hundreds of pages.</li>
</div>

<div class="bx-tip">
  <p class="bx-tip-label">Tip</p>
  <p>Keep editorial dofollow external links for sources you genuinely trust and cite, such as official documentation and original research. Add <code>rel="sponsored"</code> to anything paid and <code>rel="ugc"</code> to links in comments or forums.</p>
</div>

<div class="bx-section-head">
  <span class="bx-num">08</span>
  <h2 class="bx-h2" id="how-to-track-outbound-link-clicks-in-ga4">How to Track Outbound Link Clicks in GA4</h2>
  <div class="bx-rule"></div>
</div>

<p>Knowing which external links readers actually click tells you which sources they trust and where your content sends traffic. GA4 can track outbound link clicks without any code.</p>

<table class="bx-table">
  <thead><tr style="background:#2b2b2b !important;"><th style="background:#2b2b2b !important; color:#ffffff !important;">Step</th><th style="background:#2b2b2b !important; color:#ffffff !important;">What to do</th></tr></thead>
  <tbody>
    <tr><td>1. Turn on enhanced measurement</td><td>In GA4 go to Admin, Data streams, choose your web stream and make sure Outbound clicks is switched on.</td></tr>
    <tr><td>2. Know the event</td><td>GA4 records each outbound click as a <code>click</code> event with the parameters <code>link_url</code>, <code>link_domain</code> and <code>outbound</code> set to true.</td></tr>
    <tr><td>3. Register the dimensions</td><td>Under Admin, Custom definitions, create event scoped dimensions for <code>link_url</code> and <code>link_domain</code> so they appear in reports.</td></tr>
    <tr><td>4. Build the report</td><td>In Explore, create a free form exploration, filter Event name to <code>click</code> and break it down by Link URL or Link domain.</td></tr>
  </tbody>
</table>

<p>If you need more control, such as tracking clicks only on sponsored links, use <a href="/gtm-data-layer-explained/">Google Tag Manager</a> with a Just Links trigger and a condition on the click URL. Our guide to <a href="/ga4-custom-event-tracking-google-tag-manager/">GA4 custom event tracking with GTM</a> walks through the setup.</p>


<div class="bx-section-head">
  <span class="bx-num">09</span>
  <h2 class="bx-h2" id="building-a-balanced-nofollow-vs-dofollow-link-profile">Building a Balanced Nofollow vs Dofollow Link Profile</h2>
  <div class="bx-rule"></div>
</div>

<p>A natural backlink profile rarely sits at one hundred percent dofollow. Real websites earn a messy mix of editorial mentions, forum chatter, sponsored placements and the occasional spammy comment link, and that mix is exactly what Google expects to see.</p>

<p>Start by auditing what you already have. Our <a href="/how-to-analyze-your-backlink-profile/">guide on analyzing your backlink profile</a> walks through pulling a full link export and sorting it by attribute, source quality and anchor text distribution.</p>

<p>From there, focus future outreach on relevance and traffic rather than chasing dofollow status alone. A well placed nofollow mention on a site your actual customers read is worth more than a dofollow link buried on a page nobody visits.</p>

<p>Revisit our earlier point on how links are built in the first place by checking <a href="/what-is-link-building/">what link building actually involves</a> if any of these terms still feel unfamiliar, since nofollow vs dofollow links only make sense once the basics of link building click.</p>

<p>The biggest takeaway from this whole nofollow vs dofollow links discussion is simple: stop optimizing for the attribute itself and start optimizing for relevance, trust and traffic, since those are the qualities Google's own hint based systems are quietly rewarding anyway.</p>

<p>Set a recurring reminder to pull a fresh link export every quarter rather than once a year. Attributes drift as platforms update their templates, partners swap plugins and old sponsored deals quietly lose their disclosure tags, so treat this audit as ongoing maintenance, not a one time project you finish and forget.</p>

<div class="bx-faq">
  <div class="bx-faq-item open">
    <button class="bx-faq-q"><span class="bx-faq-num">1</span>What is the real difference between nofollow vs dofollow links?</button>
    <div class="bx-faq-a"><p>A dofollow link is a plain hyperlink with no rel attribute, so it was built to pass full ranking credit. A nofollow link carries <code>rel="nofollow"</code>, which Google now treats as a hint rather than a hard block when deciding how much weight, if any, to give it.</p></div>
  </div>
  <div class="bx-faq-item open">
    <button class="bx-faq-q"><span class="bx-faq-num">2</span>Do nofollow links help SEO rankings at all in 2026?</button>
    <div class="bx-faq-a"><p>They rarely pass direct ranking credit, since Google confirmed through Search Engine Land that PageRank still is not transferred through nofollow links. They can still help indirectly through referral traffic, brand exposure and occasionally inspiring a genuine dofollow citation elsewhere.</p></div>
  </div>
  <div class="bx-faq-item open">
    <button class="bx-faq-q"><span class="bx-faq-num">3</span>Should I use sponsored or nofollow for affiliate links?</button>
    <div class="bx-faq-a"><p>Google's own guidance asks site owners to use <code>rel="sponsored"</code> for affiliate and paid links specifically, since that attribute identifies the commercial relationship directly. Pairing it with nofollow is fine for extra compatibility across older systems.</p></div>
  </div>
  <div class="bx-faq-item open">
    <button class="bx-faq-q"><span class="bx-faq-num">4</span>How can I check whether a link is nofollow or dofollow?</button>
    <div class="bx-faq-a"><p>View the page source or inspect the anchor tag for a rel attribute, or run a proper crawl with a tool like Screaming Frog, which flags every nofollow, sponsored and ugc link across an entire site in one pass.</p></div>
  </div>
  <div class="bx-faq-item open">
    <button class="bx-faq-q"><span class="bx-faq-num">5</span>What is a healthy ratio of nofollow vs dofollow links?</button>
    <div class="bx-faq-a"><p>There is no single magic number, but Ahrefs data shows large, trusted sites naturally sit around ten percent nofollow. A profile that is either entirely dofollow or almost entirely nofollow tends to look unnatural to Google rather than ideal.</p></div>
  </div>
</div>

<div class="bx-learn">
  <h2 id="learn-today">Learn Today</h2>
  <div class="bx-learn-grid">
    <div class="bx-learn-card"><span class="bx-learn-num">1</span><div><h4>Nofollow Attribute</h4><p>An HTML rel value telling search engines to treat a link as a hint rather than a guaranteed endorsement.</p></div></div>
    <div class="bx-learn-card"><span class="bx-learn-num">2</span><div><h4>Dofollow Link</h4><p>The informal name for an ordinary link with no blocking attribute, so it can pass full link equity.</p></div></div>
    <div class="bx-learn-card"><span class="bx-learn-num">3</span><div><h4>Rel Sponsored</h4><p>The attribute Google asks site owners to apply to paid, affiliate or advertising links.</p></div></div>
    <div class="bx-learn-card"><span class="bx-learn-num">4</span><div><h4>Rel UGC</h4><p>Short for user generated content, applied to links left in comments, forums and reviews.</p></div></div>
    <div class="bx-learn-card"><span class="bx-learn-num">5</span><div><h4>Link Equity</h4><p>The ranking value one page passes to another through a hyperlink between them.</p></div></div>
    <div class="bx-learn-card"><span class="bx-learn-num">6</span><div><h4>Anchor Text</h4><p>The clickable, visible words wrapped inside a hyperlink.</p></div></div>
  </div>
</div>

<div class="bx-cta">
  <h3>Ready to Audit Your Own Link Profile?</h3>
  <p>Explore more Brandella Journal guides on SEO and digital marketing.</p>
  <div class="bx-cta-btns">
    <a href="/">Browse All Guides</a>
    <a class="bx-cta-outline" href="/what-is-off-page-seo-complete-beginners-guide/">See the Off Page SEO Beginners Guide</a>
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
