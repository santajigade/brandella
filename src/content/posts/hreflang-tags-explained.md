---
title: "Hreflang Tags Explained: 5 Essential Rules for Global SEO"
slug: "hreflang-tags-explained"
date: "2026-10-01T04:21:30"
updated: "2026-10-01T04:38:55"
author: "santajigade"
categories: ["technical-seo"]
primaryCategory: "technical-seo"
description: "Hreflang tags tell Google which language and country version of a page to show. Learn the 5 rules that stop the wrong page ranking in the wrong market."
focusKeyword: "hreflang tags"
takeaways:
  - "Hreflang tags tell search engines which language and country each version of a page is meant for."
  - "Every hreflang link must be confirmed by a return tag on the other page, or Google ignores the pair."
  - "Use x-default for the version shown when no language or country annotation matches the visitor."
  - "You can add hreflang in the HTML head, in HTTP headers or in the XML sitemap; Google treats all three equally."
  - "Use a crawler to audit hreflang regularly, especially after adding locales, renaming pages or migrating."
image: "/wp-content/uploads/2026/10/hreflang-tags.webp"
imageAlt: "hreflang tags"
words: 1842
views: 22
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
  <span class="bx-pill">Technical SEO</span>
</div>

<p>Hey! If you run a site in more than one language or ship separate pages for different countries, you have probably typed a block of link tags into your head section and hoped for the best. This one is for you.</p>

<p class="bx-lede"><em>Picture this: your French page outranks your English page in France, except it is showing up for searchers in Canada instead, and your support inbox is full of confused messages. That mismatch is usually not a translation problem. It is a hreflang tags problem, and it is one of the most common ways international sites quietly lose traffic.</em></p>

<div class="bx-section-head">
  <span class="bx-num">01</span>
  <h2 class="bx-h2" id="what-hreflang-tags-actually-do">What Hreflang Tags Actually Do</h2>
  <div class="bx-rule"></div>
</div>

<p>Hreflang tags are a small piece of markup that tell search engines which language and which country a page is meant for. According to <a href="https://developers.google.com/search/docs/specialty/international/localized-versions">Google's own documentation</a>, the annotation exists so Google can point a searcher in Tokyo to the Japanese version of a page and a searcher in Madrid to the Spanish one, even when both pages are technically duplicates of each other.</p>

<p>Without hreflang tags, search engines are left guessing. They might index only one language, show the wrong country version in search results, or treat your localized pages as duplicate content competing against each other. That last outcome is the quiet killer, because it dilutes ranking signals across pages that should be working together.</p>


<p>Per <a href="https://en.wikipedia.org/wiki/Hreflang">Wikipedia's overview of the attribute</a>, hreflang covers three real world scenarios: the same country with different languages, different countries with the same language, and different countries with different languages. Most sites only plan for one of these and miss the other two.</p>

<p>The scale of the problem is bigger than most teams expect. An audit of 374,756 domains found that 67 percent of sites using hreflang tags carried at least one unresolved error, meaning broken international targeting is closer to the norm than the exception. If your site has never been audited for this specifically, assume there is at least one mismatched pair somewhere in your clusters.</p>

<div class="bx-tip">
  <p class="bx-tip-label">Tip</p>
  <p>Before you touch this setup, make sure your <a href="/what-is-canonical-tag/">canonical tags</a> are already correct for every locale. Hreflang built on top of a broken canonical setup just scales the confusion.</p>
</div>

<div class="bx-section-head">
  <span class="bx-num">02</span>
  <h2 class="bx-h2" id="the-rule-nobody-reads-twice-return-tags-must-confirm">The Rule Nobody Reads Twice: Return Tags Must Confirm</h2>
  <div class="bx-rule"></div>
</div>

<p>This is the part of international SEO that trips up even experienced teams. Google states it plainly: if page A points to page B as an alternate, page B must point back to page A, or the whole pair is ignored. One direction is not enough.</p>

<p><a href="https://ahrefs.com/blog/hreflang-tags/">Ahrefs compares this to confirming a relationship status</a>, a declaration only counts once both sides agree. A page that lists five language versions but is not listed back on all five is effectively invisible to the system, even though the markup looks complete on the page you are staring at.</p>

<p>This return tag requirement is also why mismatches are so easy to create at scale. Add a new regional page, forget to update the other four, and you have broken a cluster that was working fine yesterday.</p>

<div class="bx-section-head">
  <span class="bx-num">03</span>
  <h2 class="bx-h2" id="what-the-x-default-value-is-for-and-isn-t">What the x default Value Is For (and Isn't)</h2>
  <div class="bx-rule"></div>
</div>

<p>Alongside language and country codes, hreflang tags support one special value: <code>x-default</code>. Google describes it as the version shown when none of your other annotations match a visitor's browser settings, think of a language picker page or a global homepage that serves everyone before they choose a locale.</p>

<p><code>x-default</code> is not meant for your biggest market's homepage or your most heavily optimized page. It is meant for the fallback a visitor sees when nothing else fits, which is a narrower job than most teams assign it.</p>

<div class="bx-fact">
  <span class="bx-fact-label">Did You Know</span>
  <p>An audit of over 374,000 domains by <a href="https://ahrefs.com/blog/hreflang-study">Ahrefs</a> found that 56.3 percent of sites using hreflang tags were missing an <code>x-default</code> fallback entirely, making it the single most common gap in real world implementations.</p>
</div>


<div class="bx-section-head">
  <span class="bx-num">04</span>
  <h2 class="bx-h2" id="three-ways-to-add-hreflang">Three Ways to Add Hreflang</h2>
  <div class="bx-rule"></div>
</div>

<p>There are three accepted places to declare hreflang tags, and Google treats them as functionally equal. You pick based on your site's shape, not based on which one ranks better.</p>

<p>The first is a <code>link</code> element inside the HTML head of each page, the most common choice for small to mid sized sites because it is easy to template. The second is an HTTP header, which matters for files that have no head section at all, like PDFs. The third is an XML sitemap entry, which <a href="https://www.screamingfrog.co.uk/seo-spider/tutorials/how-to-audit-hreflang/">Screaming Frog recommends</a> for large multilingual catalogs, since one sitemap file can describe hundreds of language clusters without bloating every page's markup.</p>

<p>If your site already maintains a sitemap for crawling, our guide on the difference between an <a href="/html-sitemap-vs-xml-sitemap-difference/">HTML sitemap and an XML sitemap</a> is a useful companion read before you decide where this annotation should live.</p>

<div class="bx-tip">
  <p class="bx-tip-label">Tip</p>
  <p>Pick one method and stick to it. Google explicitly says there is no ranking benefit to declaring hreflang tags in the sitemap and the HTML head at the same time, you just double your chances of the two copies drifting out of sync.</p>
</div>

<div class="bx-section-head">
  <span class="bx-num">05</span>
  <h2 class="bx-h2" id="5-mistakes-that-break-international-seo">5 Mistakes That Break International SEO</h2>
  <div class="bx-rule"></div>
</div>

<p>Now the part you came for. These five mistakes show up again and again in audits, and they are the reason this markup has a reputation for being fragile.</p>

<p>A study of 20,000 multilingual sites by <a href="https://www.semrush.com/blog/the-most-common-hreflang-mistakes-infographic/">Semrush</a> found that 58 percent had hreflang conflicts somewhere in their source code, and missing self references showed up in 96 percent of the sites that had any source code conflict at all. These are not rare edge cases, they are the default state of most multilingual sites that have never been audited.</p>

<div class="bx-checklist">
  <li><b>Missing return tags.</b> A page lists its alternates but is not listed back by all of them. Audit every cluster as a group, not one page at a time, so a one sided link cannot hide.</li>
  <li><b>Wrong language or region codes.</b> Teams write <code>en-UK</code> when the correct region code is <code>GB</code>, or reverse the order and write the country before the language. Codes must follow <a href="https://www.w3.org/International/articles/bcp47/">the BCP 47 language tag standard</a>, language first, region second.</li>
  <li><b>Pointing to a redirect or a non canonical URL.</b> If the target URL 301s somewhere else or is not the canonical version of that page, Google ignores the pair. Check your <a href="/http-status-codes-for-seo-explained/">HTTP status codes</a> for every hreflang target before you assume the setup works.</li>
  <li><b>No <code>x-default</code> fallback.</b> Visitors whose language does not match any listed version land on whatever the server guesses, often the wrong country entirely.</li>
  <li><b>Mixing methods inconsistently.</b> Declaring hreflang tags in both the sitemap and the page head with different values creates a direct conflict that search engines have to resolve on their own, usually by ignoring both.</li>
</div>

<p>As Helen Pollitt, Head of SEO at Getty Images, put it in a <a href="https://www.searchenginejournal.com/ask-an-seo-what-are-the-most-common-hreflang-mistakes/556455/">Search Engine Journal interview</a>, getting hreflang tags right matters because "search engines being confused over which version of a page to show" is exactly the outcome you are trying to avoid.</p>


<div class="bx-section-head">
  <span class="bx-num">06</span>
  <h2 class="bx-h2" id="auditing-your-hreflang-setup-without-guessing">Auditing Your Hreflang Setup Without Guessing</h2>
  <div class="bx-rule"></div>
</div>

<p>You cannot eyeball every pair across a hundred pages and trust what you see. A crawler is the only realistic way to confirm every pair actually links back correctly.</p>

<p>Tools built for this job flag the same handful of problems every time: broken or redirected targets, missing reciprocal links, duplicate language codes pointing at more than one URL, and annotations that contradict a <a href="/meta-robots-tags-explained-2/">noindex directive</a> on the target page. Run that check after every content migration, not just once at launch, since a single URL change can quietly snap a whole cluster.</p>

<p>It also helps to confirm your <a href="https://searchengineland.com/guide/international-seo">overall international site structure</a> before you fix individual tags, since this annotation layered on top of an inconsistent folder or subdomain structure tend to break again the next time someone reorganizes the site.</p>


<div class="bx-section-head">
  <span class="bx-num">07</span>
  <h2 class="bx-h2" id="keeping-your-hreflang-setup-healthy-long-term">Keeping Your Hreflang Setup Healthy Long Term</h2>
  <div class="bx-rule"></div>
</div>

<p>Hreflang tags are not a set it and forget it task. Every new locale, every page rename, and every migration is a chance to break a reciprocal link that was fine the week before.</p>

<p>Build a habit of treating language clusters as a single unit. When one page in the group moves or redirects, update every other member of that cluster in the same change, not as a follow up ticket that might get skipped.</p>

<p>Keep a simple reference sheet of your valid language and region codes so nobody on the team has to remember whether it is <code>pt-BR</code> or <code>br-PT</code>. Small clerical slips are the most common reason these tags fail, far more often than anything structurally complicated.</p>

<div class="bx-tip">
  <p class="bx-tip-label">Tip</p>
  <p>Re run a full hreflang tags audit on a schedule, quarterly at minimum, and immediately after any domain or URL structure change.</p>
</div>


<div class="bx-faq">
  <div class="bx-faq-item open">
    <button class="bx-faq-q"><span class="bx-faq-num">1</span>What are hreflang tags used for?</button>
    <div class="bx-faq-a"><p>Hreflang tags tell search engines which language and country a page targets, so the right localized version shows up for each searcher instead of search engines guessing or treating translated pages as duplicates.</p></div>
  </div>
  <div class="bx-faq-item open">
    <button class="bx-faq-q"><span class="bx-faq-num">2</span>Do hreflang tags need to point both ways?</button>
    <div class="bx-faq-a"><p>Yes. Google's documentation states that if two pages do not both point to each other, the annotation is ignored entirely. Every page in a language cluster must list every other page, and vice versa.</p></div>
  </div>
  <div class="bx-faq-item open">
    <button class="bx-faq-q"><span class="bx-faq-num">3</span>What happens if I skip the x default value?</button>
    <div class="bx-faq-a"><p>Visitors whose browser language does not match any of your listed hreflang tags get routed based on the server's own guess, which often lands them on the wrong country version. Ahrefs found over half of sites studied skip this fallback entirely.</p></div>
  </div>
  <div class="bx-faq-item open">
    <button class="bx-faq-q"><span class="bx-faq-num">4</span>Should hreflang tags go in the sitemap or the page head?</button>
    <div class="bx-faq-a"><p>Either works, Google treats them as equal. Small sites usually find HTML head tags easier to maintain, while large multilingual catalogs often prefer sitemap entries so one file can cover many pages without bloating every page's source code.</p></div>
  </div>
  <div class="bx-faq-item open">
    <button class="bx-faq-q"><span class="bx-faq-num">5</span>Why do hreflang tags keep breaking after I fix them?</button>
    <div class="bx-faq-a"><p>Usually because a related page in the cluster moved, redirected, or changed its canonical tag without every other version being updated at the same time. Treat the whole cluster as one unit whenever any page in it changes.</p></div>
  </div>
</div>

<div class="bx-learn">
  <h2 id="learn-today">Learn Today</h2>
  <div class="bx-learn-grid">
    <div class="bx-learn-card"><span class="bx-learn-num">1</span><div><h4>Hreflang</h4><p>An HTML annotation that tells search engines the language and region a page targets.</p></div></div>
    <div class="bx-learn-card"><span class="bx-learn-num">2</span><div><h4>X Default</h4><p>A fallback hreflang value shown when no listed language or region matches the visitor.</p></div></div>
    <div class="bx-learn-card"><span class="bx-learn-num">3</span><div><h4>Return Tag</h4><p>The reciprocal hreflang link that a target page must send back to confirm a pairing.</p></div></div>
    <div class="bx-learn-card"><span class="bx-learn-num">4</span><div><h4>BCP 47</h4><p>The standard combining ISO language and region codes used to format hreflang values correctly.</p></div></div>
    <div class="bx-learn-card"><span class="bx-learn-num">5</span><div><h4>Language Cluster</h4><p>The full set of localized versions of one page that must all reference each other.</p></div></div>
    <div class="bx-learn-card"><span class="bx-learn-num">6</span><div><h4>Canonical Conflict</h4><p>When a hreflang target is not the canonical version of a page, causing the signal to be ignored.</p></div></div>
  </div>
</div>

<div class="bx-cta">
  <h3>Get Your International Site Speaking the Right Language to Google</h3>
  <p>Explore more Brandella Journal guides on SEO and digital marketing.</p>
  <div class="bx-cta-btns">
    <a href="/">Browse All Guides</a>
    <a class="bx-cta-outline" href="/what-is-canonical-tag/">Check Your Canonical Tags Next</a>
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
