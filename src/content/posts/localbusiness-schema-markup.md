---
title: "LocalBusiness Schema Markup: 7 Essential Properties to Add"
slug: "localbusiness-schema-markup"
date: "2026-10-01T04:40:14"
updated: "2026-10-01T04:41:31"
author: "santajigade"
categories: ["local-seo"]
primaryCategory: "local-seo"
description: "LocalBusiness schema markup helps Google show your hours, ratings, and address in search. See the 7 properties that make it actually work."
focusKeyword: "LocalBusiness schema markup"
takeaways:
  - "LocalBusiness schema describes a physical business so search engines can read its name, address, hours and location."
  - "Your business name and address in the markup must match your signage and Google Business Profile exactly."
  - "Use the full PostalAddress structure and geo coordinates with at least five decimal places."
  - "Do not mark up reviews of your own business with aggregateRating; let your Google Business Profile carry the stars."
  - "Test the live URL in Google's Rich Results Test before and after publishing."
image: "/wp-content/uploads/2026/10/LocalBusiness-schema-markup.webp"
imageAlt: "LocalBusiness schema markup"
words: 2228
views: 20
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
  <span class="bx-pill">Local SEO</span>
</div>

<p>So your shop, clinic, or office shows up in search, but every competitor sitting above you has star ratings, opening hours, and a map pin baked right into the result, and you don't. Nine times out of ten that gap is structured data, and today we're going to close it properly.</p>

<p class="bx-lede"><em>Picture a customer searching for your service in your city. They scroll past five plain blue links and click the one listing with visible stars, hours, and an address right there in the snippet. A properly built LocalBusiness schema markup setup is usually the only real difference between those two listings.</em></p>

<div class="bx-section-head">
  <span class="bx-num">01</span>
  <h2 class="bx-h2" id="what-is-localbusiness-schema-markup-and-why-should-you-care">What Is LocalBusiness Schema Markup, and Why Should You Care</h2>
  <div class="bx-rule"></div>
</div>

<p><a href="https://schema.org/LocalBusiness">Schema.org defines LocalBusiness</a> as a type for "a particular physical business or branch of an organization," covering everything from restaurants and clinics to law firms and bowling alleys. It inherits properties from the broader Organization and Place types, which is why a single LocalBusiness block can carry contact details, geographic coordinates, and reviews all at once.</p>

<p>LocalBusiness schema markup is the vocabulary that turns a page full of plain text into something a search engine can actually parse into facts: this is the business name, this is the phone number, these are the hours. Without it, Google has to guess at those details from unstructured copy, and guesses are unreliable.</p>

<p>According to <a href="https://ahrefs.com/seo/glossary/local-business-schema">Ahrefs</a>, this markup exists specifically to help pages surface in Local Search results and in Google Maps, which is exactly where most local purchase decisions begin. Get the setup wrong and you are not disqualified, you simply miss out on the richer display other businesses are getting for free.</p>

<div class="bx-ad">
  <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-3931314195561246" data-ad-slot="4249015278" data-ad-format="auto" data-full-width-responsive="true"></ins>
  <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
</div>

<div class="bx-section-head">
  <span class="bx-num">02</span>
  <h2 class="bx-h2" id="the-properties-schema-org-actually-defines">The Properties Schema.org Actually Defines</h2>
  <div class="bx-rule"></div>
</div>

<p>Before touching any code, it helps to know what the standard actually asks for. From the base LocalBusiness type you get <code>openingHours</code>, <code>priceRange</code>, <code>paymentAccepted</code>, and <code>currenciesAccepted</code>. From the inherited Organization type you get <code>address</code>, <code>telephone</code>, <code>email</code>, <code>aggregateRating</code>, and <code>review</code>. From Place you inherit <code>geo</code>, <code>image</code>, <code>photo</code>, and the more detailed <code>openingHoursSpecification</code>.</p>

<p><a href="https://developers.google.com/search/docs/appearance/structured-data/local-business">Google's own structured data guidelines</a> are narrower than the full schema.org vocabulary. Google only strictly requires <code>name</code> and a complete <code>address</code> object with street, locality, region, postal code, and country. Everything else, telephone, a page specific <code>url</code>, opening hours, geo coordinates, and price range, is recommended rather than mandatory.</p>

<p>That distinction matters because plenty of guides treat the full schema.org property list as a checklist of requirements, when in reality Google is asking for the minimum needed to confirm identity and location, and leaving the rest to improve how the listing looks once it qualifies. Knowing this upfront keeps a LocalBusiness schema markup project from sprawling into properties nobody actually checks.</p>

<div class="bx-tip">
  <p class="bx-tip-label">Tip</p>
  <p>If you haven't added any structured data to your site yet, start with the broader concept before narrowing your LocalBusiness schema markup to local properties. Our guide on <a href="/what-is-schema-markup/">what schema markup is</a> covers the vocabulary and syntax options in plain terms.</p>
</div>

<div class="bx-section-head">
  <span class="bx-num">03</span>
  <h2 class="bx-h2" id="steps-1-and-2-name-address-phone-and-opening-hours">Steps 1 and 2: Name, Address, Phone and Opening Hours</h2>
  <div class="bx-rule"></div>
</div>

<p>Step one of a complete LocalBusiness schema markup setup is the identity block: <code>name</code>, <code>@type</code>, and the <code>address</code> object. The name should match what appears on your signage and your Google Business Profile exactly, no keyword stuffing, no extra city names appended. The address should use the full <code>PostalAddress</code> structure rather than a single text string, since each field, street address, locality, region, postal code, and country, maps to a distinct property Google can validate.</p>

<p>Step two adds <code>telephone</code> and opening hours. Use a single primary contact number in full international format, and express hours with the standard shorthand, for example <code>Mo-Fr 09:00-18:00</code>, rather than a sentence describing your schedule. If your hours genuinely vary by day, use <code>openingHoursSpecification</code> instead of the simpler <code>openingHours</code> property so each day gets its own entry.</p>

<p>Every one of these values needs to match what is published everywhere else your business appears online, your website footer, your Google Business Profile, and any directory listing. That matching is the entire idea behind NAP consistency, and it is worth reading in full if you haven't already: see our breakdown of <a href="/nap-consistency-hidden-local-seo-ranking-factor/">NAP consistency as a local SEO ranking factor</a>.</p>

<div class="bx-section-head">
  <span class="bx-num">04</span>
  <h2 class="bx-h2" id="steps-3-and-4-geo-coordinates-price-range-and-ratings">Steps 3 and 4: Geo Coordinates, Price Range and Ratings</h2>
  <div class="bx-rule"></div>
</div>

<p>Step three is <code>geo</code>, your latitude and longitude as a <code>GeoCoordinates</code> object. Google recommends at least five decimal places of precision, which is roughly the difference between pointing at your building and pointing at your entire block. You can pull exact coordinates from Google Maps itself by right clicking your pin.</p>

<p>Step four covers <code>priceRange</code> and, carefully, <code>aggregateRating</code>. Price range is a short symbolic string under a hundred characters, something like <code>$$</code>, and it exists to set expectations rather than list exact prices. This is also the point where a LocalBusiness schema markup setup starts looking complete rather than minimal. Ratings are where most local businesses get tripped up, so it deserves its own warning.</p>

<p><a href="https://www.brightlocal.com/learn/review-schema/">BrightLocal's review schema guide</a> explains that Google changed policy in 2019 so that reviews a business places about itself are no longer eligible for star display in search results. If the entity being reviewed controls the reviews describing itself, whether added directly or through an embedded widget, the star rating simply will not render. The workaround most sites use is marking up reviews of specific products or services instead of the business entity itself, which schema.org explicitly supports and Google still honors.</p>

<div class="bx-fact">
  <span class="bx-fact-label">Did You Know</span>
  <p>Whitespark's 2026 local search ranking factors report scores "website content marked up in schema" at 49 for local pack and map rankings, but 111 for conversion related signals, meaning structured data appears to do far more for turning searchers into customers than for moving you up the ranking itself. <a href="https://whitespark.ca/local-search-ranking-factors/">Whitespark</a> notes this pattern holds across their full 187 factor dataset.</p>
</div>

<div class="bx-ad">
  <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-3931314195561246" data-ad-slot="4249015278" data-ad-format="auto" data-full-width-responsive="true"></ins>
  <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
</div>

<div class="bx-section-head">
  <span class="bx-num">05</span>
  <h2 class="bx-h2" id="step-5-testing-validating-and-publishing-your-markup">Step 5: Testing, Validating and Publishing Your Markup</h2>
  <div class="bx-rule"></div>
</div>

<p>Step five, and the one skipped most often, is validation before you publish. Paste your finished code block into Google's Rich Results Test, available through Search Console help, and check it against a live URL rather than only a snippet, since some errors only surface once the page actually renders.</p>

<p><a href="https://support.google.com/webmasters/answer/7445569?hl=en">Google's own documentation for the tool</a> flags one gotcha worth remembering directly: the Rich Results Test quietly ignores comments written inside your structured data block during testing, which means a page that passes the test can still throw errors once it goes live, because that comment skipping behavior is not part of the actual <code>JSON-LD</code> standard. Strip every comment from the final code before you ship it, not just before you test it.</p>

<p>Once the test passes with no errors and no missing fields, publish the page, then recheck it again a few days later through the URL Inspection tool in Search Console to confirm Google actually read the markup the way you intended.</p>

<div class="bx-tip">
  <p class="bx-tip-label">Tip</p>
  <p>If you are implementing this through <code>JSON-LD</code> for the first time, walk through our dedicated guide on <a href="/how-to-add-schema-markup-json-ld/">adding schema markup with <code>JSON-LD</code></a> before you write your first script tag, it covers placement and formatting mistakes this article doesn't repeat.</p>
</div>

<div class="bx-section-head">
  <span class="bx-num">06</span>
  <h2 class="bx-h2" id="how-this-connects-back-to-nap-and-your-business-profile">How This Connects Back to NAP and Your Business Profile</h2>
  <div class="bx-rule"></div>
</div>

<p>A complete LocalBusiness schema markup setup does not exist in isolation. <a href="https://www.searchenginejournal.com/how-to-use-schema-for-local-seo-a-complete-guide/294973/">Search Engine Journal's guide to local schema</a> describes structured data as acting like a translator, turning your website's content into a format search engines can classify quickly, and notes that it helps Google associate your site with your Google Business Profile even when that profile listing is incomplete or unclaimed.</p>

<p>That alignment only works if the facts actually agree. If your schema lists one phone number, your Google Business Profile lists a second, and an old directory listing lists a third, you have given Google three conflicting answers to the same question and no reason to trust any of them fully. Before you publish new markup, it's worth confirming your Google Business Profile itself is complete and accurate; our <a href="/google-my-business-profile-complete-guide-beginners/">Google Business Profile setup guide</a> walks through that from scratch.</p>

<p>Reviews deserve the same discipline. If you're actively trying to grow your review count as part of this process, our guide on <a href="/how-to-get-more-google-reviews/">getting more Google reviews</a> pairs naturally with the aggregateRating properties covered in step four above.</p>

<div class="bx-ad">
  <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-3931314195561246" data-ad-slot="4249015278" data-ad-format="auto" data-full-width-responsive="true"></ins>
  <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
</div>

<div class="bx-section-head">
  <span class="bx-num">07</span>
  <h2 class="bx-h2" id="common-mistakes-that-undo-a-good-setup">Common Mistakes That Undo a Good Setup</h2>
  <div class="bx-rule"></div>
</div>

<p>Most broken LocalBusiness schema markup implementations aren't caused by complicated properties, they're caused by small, avoidable slips that nobody catches before publishing.</p>

<div class="bx-checklist">
  <li><b>Marking up reviews of the business itself.</b> Switch the <code>itemReviewed</code> target to a specific product or service instead, or drop aggregateRating entirely and let your Google Business Profile carry the stars.</li>
  <li><b>Mismatched NAP details across platforms.</b> Audit your website footer, schema, Google Business Profile, and top directory listings in one sitting and correct every inconsistency you find.</li>
  <li><b>Using a plain text address instead of a PostalAddress object.</b> Google cannot reliably parse a single string the way it parses discrete street, city, region, and postal code fields.</li>
  <li><b>Leaving <code>JSON-LD</code> comments in the published file.</b> They pass casual testing but are not part of the actual <code>JSON-LD</code> standard and risk breaking in production.</li>
  <li><b>Forgetting to retest after a redesign.</b> A template change or plugin update can silently strip your script tag, so a page that validated six months ago is not guaranteed to validate today.</li>
</div>

<p>None of these mistakes are difficult to fix once you know to look for them, which is really the whole point of treating LocalBusiness schema markup as a maintenance task rather than a one time project.</p>

<div class="bx-ad">
  <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-3931314195561246" data-ad-slot="4249015278" data-ad-format="auto" data-full-width-responsive="true"></ins>
  <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
</div>

<div class="bx-fact">
  <span class="bx-fact-label">Did You Know</span>
  <p>Businesses that earn a spot in Google's local pack see roughly 126 percent more traffic and 93 percent more calls, clicks, and direction requests than businesses ranked four through ten, and about 42 percent of searchers click a local pack result for local queries, according to data covered by <a href="https://searchengineland.com/guide/google-local-pack">Search Engine Land</a>.</p>
</div>

<p>That gap is exactly what a complete, accurate LocalBusiness schema markup setup is working toward, not a guaranteed ranking boost on its own, but a better looking, more trustworthy listing once you've already earned visibility through the other signals that actually move rankings.</p>

<h2 style="font-family:var(--bx-disp);font-weight:700;color:var(--bx-dark);" id="properties-at-a-glance">Properties at a Glance</h2>

<table class="bx-table">
  <thead><tr style="background:#2b2b2b !important;"><th style="background:#2b2b2b !important; color:#ffffff !important;">Property</th><th style="background:#2b2b2b !important; color:#ffffff !important;">Required by Google</th><th style="background:#2b2b2b !important; color:#ffffff !important;">Notes</th></tr></thead>
  <tbody>
    <tr><td><code>name</code></td><td>Yes</td><td>Must match signage and your Google Business Profile</td></tr>
    <tr><td><code>address</code></td><td>Yes</td><td>Use the full PostalAddress object, not plain text</td></tr>
    <tr><td><code>telephone</code></td><td>Recommended</td><td>One primary number, full international format</td></tr>
    <tr><td><code>openingHours</code></td><td>Recommended</td><td>Use openingHoursSpecification if hours vary by day</td></tr>
    <tr><td><code>geo</code></td><td>Recommended</td><td>Five decimal places of precision or more</td></tr>
    <tr><td><code>priceRange</code></td><td>Recommended</td><td>Short symbolic string, under 100 characters</td></tr>
    <tr><td><code>aggregateRating</code></td><td>Conditional</td><td>Only for reviews of products or services, not the business itself</td></tr>
  </tbody>
</table>

<div class="bx-faq">
  <div class="bx-faq-item open">
    <button class="bx-faq-q"><span class="bx-faq-num">1</span>Is LocalBusiness schema markup a confirmed Google ranking factor</button>
    <div class="bx-faq-a"><p>Not directly. Whitespark's 2026 ranking factors report scores schema markup relatively low for local pack and map rankings, but much higher for conversion signals, meaning it tends to help searchers act on a listing more than it moves the listing itself upward.</p></div>
  </div>
  <div class="bx-faq-item open">
    <button class="bx-faq-q"><span class="bx-faq-num">2</span>Can I add star ratings for my own business using aggregateRating</button>
    <div class="bx-faq-a"><p>No, not for the business entity itself. Google stopped displaying star ratings from reviews a business places about itself back in 2019. You can still mark up reviews of specific products or services you offer, which remains fully supported.</p></div>
  </div>
  <div class="bx-faq-item open">
    <button class="bx-faq-q"><span class="bx-faq-num">3</span>Do I need every property schema.org lists for LocalBusiness</button>
    <div class="bx-faq-a"><p>No. Schema.org defines a large vocabulary, but Google only strictly requires name and a complete address object for a valid LocalBusiness schema markup entry. Telephone, hours, geo coordinates, and price range are recommended because they improve how your listing displays, not because they're mandatory for eligibility.</p></div>
  </div>
  <div class="bx-faq-item open">
    <button class="bx-faq-q"><span class="bx-faq-num">4</span>How does LocalBusiness schema markup relate to NAP consistency</button>
    <div class="bx-faq-a"><p>Your schema's name, address, and phone values need to match what appears on your Google Business Profile and other directory listings exactly. Mismatched details across sources make it harder for Google to confidently associate your website with your physical business.</p></div>
  </div>
  <div class="bx-faq-item open">
    <button class="bx-faq-q"><span class="bx-faq-num">5</span>How do I check that my markup is actually working</button>
    <div class="bx-faq-a"><p>Run your published page through Google's Rich Results Test and confirm there are no errors or missing fields, then recheck the live URL in Search Console's URL Inspection tool a few days after publishing to confirm Google read it the way you intended.</p></div>
  </div>
</div>

<div class="bx-learn">
  <h2 id="learn-today">Learn Today</h2>
  <div class="bx-learn-grid">
    <div class="bx-learn-card"><span class="bx-learn-num">1</span><div><h4>LocalBusiness Schema</h4><p>A schema.org type used to describe a physical business location to search engines in a structured, machine readable format.</p></div></div>
    <div class="bx-learn-card"><span class="bx-learn-num">2</span><div><h4>PostalAddress Object</h4><p>A structured address format breaking a location into street, locality, region, postal code, and country fields.</p></div></div>
    <div class="bx-learn-card"><span class="bx-learn-num">3</span><div><h4>GeoCoordinates</h4><p>Latitude and longitude values that pinpoint a business location for maps and local search features.</p></div></div>
    <div class="bx-learn-card"><span class="bx-learn-num">4</span><div><h4>AggregateRating</h4><p>A schema property summarizing an average rating across multiple reviews, subject to Google's self review restrictions.</p></div></div>
    <div class="bx-learn-card"><span class="bx-learn-num">5</span><div><h4>Rich Results Test</h4><p>Google's free tool for validating that a page's structured data is error free before and after publishing.</p></div></div>
    <div class="bx-learn-card"><span class="bx-learn-num">6</span><div><h4>NAP Consistency</h4><p>Keeping a business's name, address, and phone number identical across a website, schema markup, and online listings.</p></div></div>
  </div>
</div>

<div class="bx-cta">
  <h3>Ready to Give Your Listing the Details It's Missing</h3>
  <p>A complete LocalBusiness schema markup setup takes an afternoon, not a redesign. Explore more Brandella Journal guides on SEO and digital marketing.</p>
  <div class="bx-cta-btns">
    <a href="/">Browse All Guides</a>
    <a class="bx-cta-outline" href="/how-to-rank-higher-on-google-maps-2026/">Rank Higher on Google Maps</a>
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
