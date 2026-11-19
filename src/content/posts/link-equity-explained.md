---
title: "Link Equity Explained: How Authority Flows Through Your Website"
slug: "link-equity-explained"
date: "2026-08-09T05:30:05"
updated: "2026-08-09T08:35:35"
author: "santajigade"
categories: ["link-building", "seo"]
primaryCategory: "link-building"
description: "Link equity explained: how authority flows through internal and external links, what determines link value, and how to fix common equity leaks."
focusKeyword: "link equity"
takeaways:
  - "Link equity is the authority, trust and ranking power that passes from one page to another through a hyperlink, rooted in Google's 1998 PageRank algorithm."
  - "Equity divides among a page's dofollow outgoing links, so 5 links give each destination roughly 20% while 50 links give each roughly 2%."
  - "Links from authoritative, topically relevant sites pass more equity, and dofollow links pass equity while nofollow links do not by default."
  - "Under the Reasonable Surfer model, a contextual link in the first paragraph passes more equity than an identical link buried in a footer."
  - "Broken internal links are the most common equity leak, and in 2016 Google's Gary Illyes clarified that 301 and 302 redirects retain all PageRank."
image: "/wp-content/uploads/2026/08/link-equity.webp"
imageAlt: "link equity"
words: 1821
views: 91
format: "html"
---
<div class="bmc-flow">
<style>
@import url('https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600;700;800&display=swap');

.bmc-flow{
  --bx-green:#5DB92E;
  --bx-green-deep:#4a9e24;
  --bx-gold:#F4B41A;
  --bx-ink:#2b2b2b;
  --bx-steel:#5a6570;
  --bx-steel-2:#8a96a1;
  --bx-line:#E3EDE0;
  --bx-red:#c95d5d;
  --bx-blue:#6fa8dc;
  --bx-disp:'Open Sans',Arial,sans-serif;
  --bx-body:'Open Sans',system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif;
  font-family:var(--bx-body);font-weight:400;font-style:normal;color:var(--bx-ink);line-height:1.75;font-size:17px;
  max-width:920px;margin:0 auto;padding:0;-webkit-font-smoothing:antialiased;
}
.bmc-flow *{box-sizing:border-box;}
.bmc-flow p{margin:0 0 14px;font-size:17px;}
.bmc-flow a{color:var(--bx-green-deep);text-decoration:none;font-weight:600;}
.bmc-flow a:hover{text-decoration:none;color:var(--bx-green);}
.bmc-flow strong{font-weight:700;}

.bmc-flow h2{font-family:var(--bx-disp);font-weight:700;font-size:26px;line-height:1.2;margin:36px 0 16px;color:var(--bx-ink);}
.bmc-flow h2 .bx-num{color:var(--bx-green);font-weight:800;margin-right:8px;}
.bmc-flow h3{font-family:var(--bx-disp);font-weight:600;font-size:17px;margin:17px 0 10px;color:var(--bx-ink);}
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

.bmc-flow .bx-steps{background:#20272C;border-radius:16px;padding:24px 20px;margin:20px 0 30px;}
.bmc-flow .bx-steps .dc-hint{font-size:17px;color:var(--bx-steel-2);text-transform:uppercase;letter-spacing:1.4px;font-family:var(--bx-disp);margin-bottom:14px;font-weight:600;}
.bmc-flow .bx-track{display:flex;flex-wrap:wrap;gap:8px;}
.bmc-flow .bx-step{flex:1 1 92px;min-width:88px;cursor:pointer;border:1px solid rgba(255,255,255,.16);border-radius:11px;padding:12px 8px;background:rgba(255,255,255,.04);color:#fff;text-align:center;transition:transform .14s ease,background .18s ease,border-color .18s ease;}
.bmc-flow .bx-step:hover{transform:translateY(-3px);background:rgba(93,185,46,.18);border-color:var(--bx-green);}
.bmc-flow .bx-step.on{background:var(--bx-green);border-color:var(--bx-green);}
.bmc-flow .bx-step .no{font-family:var(--bx-disp);font-weight:800;font-size:17px;color:var(--bx-gold)!important;line-height:1;}
.bmc-flow .bx-step.on .no{color:#fff!important;}
.bmc-flow .bx-step .lb{font-size:17px;text-transform:uppercase;letter-spacing:.4px;margin-top:5px;color:#fff!important;line-height:1.2;}
.bmc-flow .bx-stepdetail{margin-top:16px;background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.08);border-radius:11px;padding:15px 17px;min-height:84px;}
.bmc-flow .bx-stepdetail .dt-t{font-family:var(--bx-disp);letter-spacing:.4px;color:var(--bx-gold)!important;font-size:17px;margin:0 0 4px;font-weight:700;}
.bmc-flow .bx-stepdetail .dt-d{margin:0;font-size:17px;color:#E4E8EB!important;line-height:1.6;}

.bmc-flow .bx-table-wrap{overflow-x:auto;margin:20px 0 30px;}
.bmc-flow .bx-table{width:100%;border-collapse:collapse;font-size:17px;}
.bmc-flow .bx-table th{background:var(--bx-ink);color:#fff;padding:13px 16px;text-align:left;font-family:var(--bx-disp);font-weight:600;font-size:17px;}
.bmc-flow .bx-table td{padding:13px 16px;border-bottom:1px solid var(--bx-line);font-size:17px;}
.bmc-flow .bx-table tr:nth-child(even) td{background:#f7faf5;}

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
.bmc-flow .bx-q .ic{color:var(--bx-green);font-weight:800;flex:0 0 auto;transition:transform .2s ease;font-family:var(--bx-body);font-size:20px;}
.bmc-flow .bx-q.on .ic{transform:rotate(45deg);}
.bmc-flow .bx-a{max-height:0;overflow:hidden;transition:max-height .3s ease;padding:0 17px;}
.bmc-flow .bx-a.on{max-height:360px;}
.bmc-flow .bx-a p{padding:2px 0 16px;margin:0;font-size:17px;color:var(--bx-steel);}

.bmc-flow .bx-cta{position:relative;overflow:hidden;border-radius:17px;margin:30px 0 8px;padding:36px 30px;color:#fff;background:radial-gradient(120% 160% at 12% 10%,rgba(244,180,26,.25),transparent 46%),linear-gradient(135deg,#5DB92E 0%,#3f9421 55%,#245214 100%);}
.bmc-flow .bx-cta h2{color:#fff!important;margin:0 0 8px;}
.bmc-flow .bx-cta p{color:rgba(255,255,255,.94)!important;max-width:560px;margin:0 0 20px;font-size:17px;}
.bmc-flow .bx-actions{display:flex;flex-wrap:wrap;gap:12px;}
.bmc-flow .bx-btn{display:inline-flex;align-items:center;gap:8px;font-family:var(--bx-disp);font-size:17px;font-weight:700;padding:12px 20px;border-radius:40px;text-decoration:none;border:0;transition:transform .15s ease,box-shadow .15s ease;}
.bmc-flow .bx-btn.primary{background:#fff;color:var(--bx-green-deep)!important;}
.bmc-flow .bx-btn.ghost{background:rgba(255,255,255,.12);color:#fff!important;border:1.5px solid rgba(255,255,255,.55);}
.bmc-flow .bx-btn:hover{transform:translateY(-2px);box-shadow:0 10px 22px rgba(0,0,0,.18);}

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

.bmc-flow .bx-svgwrap{background:#f7faf5;border:1px solid var(--bx-line);border-radius:14px;padding:20px;margin:20px 0 30px;text-align:center;}
.bmc-flow .bx-svgwrap svg{max-width:100%;height:auto;}
.bmc-flow .bx-svgcap{font-size:17px;color:var(--bx-steel);margin-top:10px;}

.bmc-flow .bx-code{background:#20272C;border-radius:14px;padding:20px 22px;margin:20px 0 30px;overflow-x:auto;}
.bmc-flow .bx-code pre{margin:0;font-family:'Courier New',monospace;font-size:14px;line-height:1.6;color:#c7e8b8;white-space:pre-wrap;word-break:break-word;}
.bmc-flow .bx-code-label{font-family:var(--bx-disp);color:var(--bx-steel-2);text-transform:uppercase;letter-spacing:1.2px;font-size:13px;margin-bottom:10px;font-weight:600;}

.bmc-flow .bx-video-wrap{margin:20px 0 30px;border-radius:14px;overflow:hidden;border:1px solid var(--bx-line);}
.bmc-flow .bx-video-frame{position:relative;padding-bottom:56.25%;height:0;background:#000;}
.bmc-flow .bx-video-frame iframe{position:absolute;top:0;left:0;width:100%;height:100%;border:0;}
.bmc-flow .bx-video-cap{background:#f7faf5;padding:12px 17px;font-size:17px;color:var(--bx-steel);}

.bmc-flow .bx-ad-wrap{margin:40px 0;}
.bmc-flow .bx-ad-divider{display:flex;align-items:center;gap:12px;}
.bmc-flow .bx-ad-divider span{font-size:12px;color:#777;font-weight:600;letter-spacing:1px;text-transform:uppercase;}
.bmc-flow .bx-ad-line{flex:1;border-top:2px dotted #bdbdbd;}
@media(prefers-reduced-motion:reduce){.bmc-flow *{animation:none!important;transition:none!important;}}
</style>

<div class="bx-meta-row">
<span class="bx-meta-pill">Link Building</span>
<span class="bx-meta-pill">Link Equity</span>
<span class="bx-meta-pill">Internal Linking</span>
<span class="bx-meta-pill">2026</span>
</div>

<p class="bx-lede">Link equity explained simply: it's the authority that passes from one page to another every time a hyperlink connects them, and it's still the mechanism deciding which of your pages Google trusts enough to rank. The concept traces back to Google's original PageRank algorithm, published by Larry Page and Sergey Brin in 1998, and the core idea hasn't changed since.</p>

<p>Picture a page as a jug of water. Every link on that page pours out a portion of what it holds. The more links crowded onto the page, the smaller each individual pour becomes. <a href="https://www.domcop.com/blog/what-is-link-equity/" target="_blank" rel="noopener">DomCop's explainer</a> uses that exact analogy for how this authority distributes, and it explains a surprising number of ranking mysteries once you actually see it.</p>

<p>Link equity flows through both external backlinks and internal links, but most site owners only think about the external half. Internal linking is where you actually control the flow, and poor internal structure can waste authority that expensive backlinks worked hard to earn.</p>

<p>This guide breaks down how link equity moves through a site, what determines how much of it a given link passes, and the specific leaks that quietly waste authority most sites never notice.</p>

<div class="bx-specs">
<div class="bx-spec"><div class="v">1998</div><div class="k">the year Google's PageRank algorithm first formalized how link authority flows</div></div>
<div class="bx-spec"><div class="v">45-50</div><div class="k">links per page where traffic peaks before each additional link adds little value</div></div>
<div class="bx-spec"><div class="v">5-15</div><div class="k">broken internal links found on the average website, each one a silent equity leak</div></div>
</div>

<!-- OPENING ADSENSE CODE -->
<div class="bx-ad-wrap">
    <div class="bx-ad-divider" style="margin-bottom:20px;">
        <div class="bx-ad-line"></div>
        <span>Advertisement</span>
        <div class="bx-ad-line"></div>
    </div>
<ins class="adsbygoogle"
     style="display:block"
     data-ad-client="ca-pub-3931314195561246"
     data-ad-slot="4249015278"
     data-ad-format="auto"
     data-full-width-responsive="true"></ins>
<script>
     (adsbygoogle = window.adsbygoogle || []).push({});
</script>
    <div class="bx-ad-divider" style="margin-top:20px;">
        <div class="bx-ad-line"></div>
        <span>Advertisement</span>
        <div class="bx-ad-line"></div>
    </div>
</div>
<!-- CLOSING ADSENSE CODE -->

<h2 id="what-is-link-equity"><span class="bx-num">01</span>What Link Equity Actually Is</h2>
<div class="bx-rule"></div>
<p><a href="https://www.rhinorank.io/blog/link-equity-guide/" target="_blank" rel="noopener">Rhino Rank's 2026 guide</a> defines it precisely: link equity is the authority, trust, and ranking power that passes from one page to another through a hyperlink. When Page A links to Page B, a portion of Page A's accumulated value transfers to Page B, and search engines treat that as a vote of confidence.</p>

<p>The informal term "link juice" showed up as SEO shorthand in the early 2000s, and it stuck because it describes the mechanism well, authority flows through links the way liquid flows through pipes. Link equity is the cleaner, more technical term most SEO teams use for the same idea today.</p>

<h2 id="internal-flow"><span class="bx-num">02</span>How Link Equity Flows Through Internal Links</h2>
<div class="bx-rule"></div>
<p><a href="https://seoshouts.com/blog/link-equity/" target="_blank" rel="noopener">SEOShouts' breakdown of internal flow patterns</a> lays out the dilution principle clearly: equity divides among all dofollow outgoing links on a source page. A page with 5 outgoing links gives each destination roughly 20% of its equity. A page with 50 outgoing links gives each destination roughly 2%.</p>

<p>That single mechanic explains why a Zyppy study of 23 million links found traffic peaking at 45 to 50 links per page, SEOShouts' analysis notes. Beyond that threshold, each individual link passes so little equity it barely registers for the destination page.</p>

<div class="bx-note">
<span class="lbl">Your Strongest Pages Should Link Deliberately</span>
<p><a href="https://cloud22.com/link-equity-for-seo" target="_blank" rel="noopener">Cloud22's walkthrough of the concept</a> puts it well: a page that receives external backlinks and then links to other internal pages can amplify authority across your entire site structure. Category pages, product pages, and pillar content often rank well precisely because they sit at the center of many internal pathways.</p>
</div>

<!-- OPENING ADSENSE CODE -->
<div class="bx-ad-wrap">
    <div class="bx-ad-divider" style="margin-bottom:20px;">
        <div class="bx-ad-line"></div>
        <span>Advertisement</span>
        <div class="bx-ad-line"></div>
    </div>
<ins class="adsbygoogle"
     style="display:block"
     data-ad-client="ca-pub-3931314195561246"
     data-ad-slot="4249015278"
     data-ad-format="auto"
     data-full-width-responsive="true"></ins>
<script>
     (adsbygoogle = window.adsbygoogle || []).push({});
</script>
    <div class="bx-ad-divider" style="margin-top:20px;">
        <div class="bx-ad-line"></div>
        <span>Advertisement</span>
        <div class="bx-ad-line"></div>
    </div>
</div>
<!-- CLOSING ADSENSE CODE -->

<h2 id="what-determines-value"><span class="bx-num">03</span>What Determines How Much Equity a Link Passes</h2>
<div class="bx-rule"></div>
<p><a href="https://pielab.io/link-equity/" target="_blank" rel="noopener">Pielab's guide</a> identifies the factor most people overlook first: not all links pass value the same way. Links from authoritative, topically relevant websites typically transfer more equity than links from low-quality or unrelated sources.</p>

<p>Link type matters just as much as source quality. <a href="/nofollow-vs-dofollow-links/">Dofollow links</a> pass equity normally, the standard type used in backlink building. Nofollow links, by contrast, instruct search engines not to consider them for ranking purposes, so they don't pass meaningful equity even when they still drive referral traffic, a distinction <a href="https://linksthatrank.com/blog/link-equity/" target="_blank" rel="noopener">LinksThatRank's guide</a> emphasizes when auditing which backlinks are actually worth pursuing.</p>

<h2 id="reasonable-surfer"><span class="bx-num">04</span>The Reasonable Surfer Model: Why Placement Matters</h2>
<div class="bx-rule"></div>
<p>SEOShouts' analysis, referenced above, points to a refinement Google made to the original PageRank concept: the Reasonable Surfer model assigns more weight to links users are actually likely to click. A contextual link sitting in the first paragraph of body content passes more equity than an identical link buried in a footer.</p>

<p><a href="https://www.clickrank.ai/page-rank-algorithm/" target="_blank" rel="noopener">ClickRank's PageRank guide</a> reinforces the same principle from a different angle: links placed prominently within main content usually carry more weight than links hidden in sidebars or navigation, since editorial context signals genuine relevance rather than a boilerplate placement.</p>

<div class="bx-svgwrap">
<svg viewBox="0 0 700 240" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Diagram showing how link equity divides among outgoing links: a page with five links passes roughly twenty percent equity to each destination, while a page with fifty links passes only about two percent to each">
<rect x="20" y="30" width="180" height="55" rx="10" fill="#20272C"/>
<text x="110" y="55" text-anchor="middle" fill="#fff" font-family="Open Sans" font-size="12" font-weight="700">Page A</text>
<text x="110" y="72" text-anchor="middle" fill="#c7d9c0" font-family="Open Sans" font-size="10">5 outgoing links</text>

<line x1="200" y1="45" x2="290" y2="35" stroke="#5DB92E" stroke-width="2"/>
<line x1="200" y1="55" x2="290" y2="70" stroke="#5DB92E" stroke-width="2"/>
<line x1="200" y1="65" x2="290" y2="105" stroke="#5DB92E" stroke-width="2"/>

<rect x="295" y="20" width="120" height="30" rx="6" fill="#eef8e8" stroke="#cdeabb"/>
<text x="355" y="40" text-anchor="middle" fill="#3f9421" font-family="Open Sans" font-size="10" font-weight="700">~20% each</text>

<rect x="20" y="130" width="180" height="55" rx="10" fill="#20272C"/>
<text x="110" y="155" text-anchor="middle" fill="#fff" font-family="Open Sans" font-size="12" font-weight="700">Page B</text>
<text x="110" y="172" text-anchor="middle" fill="#c7d9c0" font-family="Open Sans" font-size="10">50 outgoing links</text>

<line x1="200" y1="145" x2="290" y2="140" stroke="#c95d5d" stroke-width="1.5"/>
<line x1="200" y1="155" x2="290" y2="165" stroke="#c95d5d" stroke-width="1.5"/>
<line x1="200" y1="165" x2="290" y2="195" stroke="#c95d5d" stroke-width="1.5"/>

<rect x="295" y="130" width="120" height="30" rx="6" fill="#fdecec" stroke="#e6b3b3"/>
<text x="355" y="150" text-anchor="middle" fill="#a33" font-family="Open Sans" font-size="10" font-weight="700">~2% each</text>
</svg>
<p class="bx-svgcap">The dilution principle: fewer, well-chosen outgoing links pass meaningfully more equity to each destination page.</p>
</div>

<h2 id="video"><span class="bx-num">05</span>Watch: Understanding Link Equity for SEO</h2>
<div class="bx-rule"></div>
<p>For a walkthrough of these fundamentals and why the concept remains one of the most influential ranking factors, this explainer covers the mechanics well.</p>

<div class="bx-video-wrap">
<div class="bx-video-frame">
<iframe src="https://www.youtube.com/embed/s8Cmqll8d4o" title="Understanding Link Equity For SEO" allowfullscreen></iframe>
</div>
<div class="bx-video-cap">"Understanding Link Equity For SEO" — Joe Hall. Source: YouTube.</div>
</div>

<h2 id="equity-leaks"><span class="bx-num">06</span>Common Link Equity Leaks Worth Fixing</h2>
<div class="bx-rule"></div>
<p>SEOShouts' guide, referenced above, calls these equity leaks: pages or links that waste authority instead of routing it productively. Every site has them, and finding the leaks is often faster than building new backlinks to compensate.</p>

<p>Broken internal links are the most common leak. Semrush's analysis of 10 million pages found the average website carries 5 to 15 broken internal links, and each one sends equity into a dead end. The source page still spends one of its link slots on that broken link, reducing what flows to working destinations, while the broken page itself receives nothing useful.</p>

<!-- OPENING ADSENSE CODE -->
<div class="bx-ad-wrap">
    <div class="bx-ad-divider" style="margin-bottom:20px;">
        <div class="bx-ad-line"></div>
        <span>Advertisement</span>
        <div class="bx-ad-line"></div>
    </div>
<ins class="adsbygoogle"
     style="display:block"
     data-ad-client="ca-pub-3931314195561246"
     data-ad-slot="4249015278"
     data-ad-format="auto"
     data-full-width-responsive="true"></ins>
<script>
     (adsbygoogle = window.adsbygoogle || []).push({});
</script>
    <div class="bx-ad-divider" style="margin-top:20px;">
        <div class="bx-ad-line"></div>
        <span>Advertisement</span>
        <div class="bx-ad-line"></div>
    </div>
</div>
<!-- CLOSING ADSENSE CODE -->

<h2 id="redirects"><span class="bx-num">07</span>How 301 Redirects Pass Link Equity</h2>
<div class="bx-rule"></div>
<p><a href="https://www.practicalecommerce.com/the-right-way-to-pass-pagerank" target="_blank" rel="noopener">Practical Ecommerce's technical SEO reference</a> traces the history of this specific question: in 2013, Google's then-webspam lead Matt Cutts confirmed 301 redirects pass most PageRank to a destination page, though not necessarily all of it. In 2016, Google's Gary Illyes clarified that 301 and 302 redirects retain all PageRank.</p>

<p>The same reference adds an important caveat worth remembering: Google has repeatedly stated that 301 redirects may pass little to no link equity for anything other than genuine 1:1 URL replacements, like a redesign or a platform migration, rather than arbitrary redirect chains.</p>

<h2 id="link-types-table"><span class="bx-num">08</span>Link Types and How They Handle Equity</h2>
<div class="bx-rule"></div>
<p>Different link mechanisms handle equity in genuinely different ways, which matters when auditing a site's overall structure.</p>

<div class="bx-table-wrap">
<table class="bx-table">
<thead>
<tr><th>Link Type</th><th>Passes Equity?</th><th>Notes</th></tr>
</thead>
<tbody>
<tr><td>Dofollow link</td><td>Yes</td><td>Standard equity-passing link, the default unless marked otherwise</td></tr>
<tr><td>Nofollow link</td><td>No (by default)</td><td>Can still drive referral traffic without passing ranking value</td></tr>
<tr><td>301 redirect</td><td>Mostly yes</td><td>Retains most or all equity for genuine 1:1 URL replacements</td></tr>
<tr><td>Broken internal link</td><td>No</td><td>Equity vanishes; the link slot is wasted entirely</td></tr>
<tr><td>Canonical tag</td><td>Consolidates, doesn't transfer</td><td>Signals which duplicate version should hold the equity</td></tr>
</tbody>
</table>
</div>

<h2 id="code"><span class="bx-num">09</span>Finding and Fixing Broken Internal Links</h2>
<div class="bx-rule"></div>
<p>Here's a practical command-line approach to surfacing broken internal links, plus the correct redirect pattern to recover the lost equity.</p>

<div class="bx-code">
<div class="bx-code-label">Finding Broken Internal Links (Screaming Frog CLI example)</div>
<pre># Crawl a site and export all internal links returning 4xx/5xx
screamingfrogseospider --crawl https://example.com \
  --headless --save-crawl \
  --export-tabs "Internal:All" \
  --output-folder ./audit

# Then filter the export for Status Code >= 400
# Each broken URL found is a link equity leak</pre>
</div>

<div class="bx-code">
<div class="bx-code-label">Correct 301 Redirect Pattern (.htaccess)</div>
<pre># Redirect a broken/removed page to its closest live equivalent
Redirect 301 /old-broken-page/ https://example.com/closest-live-page/

# Avoid redirect chains: point directly to the FINAL destination,
# not to another redirect. Each hop in a chain can dilute equity.</pre>
</div>

<h2 id="checklist"><span class="bx-num">10</span>Best Practices Checklist to Preserve Authority</h2>
<div class="bx-rule"></div>
<p>A disciplined approach to preserving and directing this authority beats hoping it distributes itself well.</p>

<div class="bx-checklist">
<div class="bx-check-item"><div class="bx-check-icon"></div><p><strong>Audit for broken internal links regularly</strong>, each one is a silent equity leak that's often faster to fix than earning a new backlink.</p></div>
<div class="bx-check-item"><div class="bx-check-icon"></div><p><strong>Keep outgoing links per page reasonable</strong>, staying well under the 45-50 range where each link's equity share starts to matter little.</p></div>
<div class="bx-check-item"><div class="bx-check-icon"></div><p><strong>Place important links in body content</strong>, not footers or sidebars, since Google's Reasonable Surfer model weights click-likely placements higher.</p></div>
<div class="bx-check-item"><div class="bx-check-icon"></div><p><strong>Link deliberately from high-authority pages</strong> to the pages you most want to rank, rather than distributing links evenly.</p></div>
<div class="bx-check-item"><div class="bx-check-icon"></div><p><strong>Avoid redirect chains</strong>, point 301s directly at the final destination URL to minimize equity loss along the way.</p></div>
</div>

<h2 id="stepper"><span class="bx-num">11</span>Priority Workflow Stepper</h2>
<div class="bx-rule"></div>
<p>Five steps cover a practical optimization workflow. Tap each one for the specific action.</p>

<div class="bx-steps" id="bxSteps">
  <div class="dc-hint">Tap a factor &darr;</div>
  <div class="bx-track" role="group" aria-label="Link equity optimization priority workflow steps">
    <div class="bx-step on" data-t="Audit for Broken Links" data-d="Crawl your site and identify every internal link returning a 4xx or 5xx status. Each one is wasted equity."><div class="no">1</div><div class="lb">Audit</div></div>
    <div class="bx-step" data-t="Fix Redirect Chains" data-d="Find any 301 redirects pointing to other redirects instead of the final destination, and correct them directly."><div class="no">2</div><div class="lb">Redirects</div></div>
    <div class="bx-step" data-t="Trim Excessive Outgoing Links" data-d="Review pages with 50+ outgoing links. Each additional link dilutes the equity every other link on that page passes."><div class="no">3</div><div class="lb">Trim</div></div>
    <div class="bx-step" data-t="Link From Strong Pages" data-d="Identify your highest-authority pages and add deliberate, contextual links to priority pages you want to rank."><div class="no">4</div><div class="lb">Link Deliberately</div></div>
    <div class="bx-step" data-t="Prioritize Placement" data-d="Move important links into body content where users are likely to click, away from footers and low-visibility navigation."><div class="no">5</div><div class="lb">Placement</div></div>
  </div>
  <div class="bx-stepdetail" aria-live="polite">
    <p class="dt-t" id="bxStepT">Audit for Broken Links</p>
    <p class="dt-d" id="bxStepD">Crawl your site and identify every internal link returning a 4xx or 5xx status. Each one is wasted equity.</p>
  </div>
</div>

<h2 id="score"><span class="bx-num">12</span>Link Equity Health Score</h2>
<div class="bx-rule"></div>
<p>Score your site against the factors that determine how efficiently authority flows through it.</p>

<div class="bx-calc">
<div class="bx-calc-header">
<h3>Authority Flow Health Score</h3>
<p>Select the option that matches your current site setup</p>
</div>
<div class="bx-calc-body">

<div class="bx-calc-factor">
<div class="bx-calc-factor-top"><label>Broken internal links</label><span>30 pts</span></div>
<select class="bx-calc-select" data-weight="30" onchange="bxCalc()">
<option value="0">Never audited, likely several present</option>
<option value="0.5">Audited once, some remain</option>
<option value="1">Regularly audited and fixed</option>
</select>
</div>

<div class="bx-calc-factor">
<div class="bx-calc-factor-top"><label>Outgoing links per page</label><span>25 pts</span></div>
<select class="bx-calc-select" data-weight="25" onchange="bxCalc()">
<option value="0">Many pages exceed 50+ outgoing links</option>
<option value="0.5">Some pages run high, most reasonable</option>
<option value="1">Consistently well under the dilution threshold</option>
</select>
</div>

<div class="bx-calc-factor">
<div class="bx-calc-factor-top"><label>Redirect chain hygiene</label><span>25 pts</span></div>
<select class="bx-calc-select" data-weight="25" onchange="bxCalc()">
<option value="0">Redirect chains exist, never audited</option>
<option value="0.5">Some chains, partially cleaned up</option>
<option value="1">All redirects point directly to final destinations</option>
</select>
</div>

<div class="bx-calc-factor">
<div class="bx-calc-factor-top"><label>Strategic internal linking</label><span>20 pts</span></div>
<select class="bx-calc-select" data-weight="20" onchange="bxCalc()">
<option value="0">Links distributed randomly, no strategy</option>
<option value="0.5">Some deliberate linking to priority pages</option>
<option value="1">High-authority pages consistently link to priority content</option>
</select>
</div>

<div class="bx-calc-gauge-wrap">
<div class="bx-calc-gauge-track"><div class="bx-calc-gauge-fill" id="bxGaugeFill"><span id="bxGaugeScore">0%</span></div></div>
<div class="bx-calc-verdict" id="bxVerdict">Select an option for each factor to calculate your score.</div>
</div>

</div>
</div>

<script>
function bxCalc(){
  var selects = document.querySelectorAll('.bx-calc-select');
  var total = 0;
  selects.forEach(function(s){
    var weight = parseFloat(s.getAttribute('data-weight'));
    var value = parseFloat(s.value);
    total += weight * value;
  });
  var pct = Math.round(total);
  document.getElementById('bxGaugeFill').style.width = pct + '%';
  document.getElementById('bxGaugeScore').innerText = pct + '%';
  var verdict = document.getElementById('bxVerdict');
  if(pct >= 80){ verdict.innerText = "Strong link equity flow. Keep auditing regularly to maintain it."; }
  else if(pct >= 50){ verdict.innerText = "Decent baseline. A broken-link audit is usually the fastest next win."; }
  else if(pct > 0){ verdict.innerText = "Significant equity leaks likely. Start with a full internal link audit."; }
  else { verdict.innerText = "Select an option for each factor to calculate your score."; }
}

(function(){
  var root=document.currentScript.parentNode.querySelector('.bmc-flow')||document.querySelector('.bmc-flow');
  var steps=root.querySelectorAll('#bxSteps .bx-step'),
      sT=root.querySelector('#bxStepT'),sD=root.querySelector('#bxStepD');
  steps.forEach(function(s){s.addEventListener('click',function(){
    steps.forEach(function(x){x.classList.remove('on');}); s.classList.add('on');
    sT.textContent=s.getAttribute('data-t'); sD.textContent=s.getAttribute('data-d');
  });});
})();
</script>

<h2 id="faq"><span class="bx-num">13</span>FAQs on Link Equity</h2>
<div class="bx-rule"></div>

<div class="bx-faq" id="bxFaq">
  <button class="bx-q">What is link equity in simple terms?<span class="ic">+</span></button>
  <div class="bx-a"><p>The authority and ranking value that passes from one page to another through a hyperlink, sometimes called "link juice." It's the mechanism behind why backlinks influence rankings.</p></div>
  <button class="bx-q">Does a page lose its own authority when it links out?<span class="ic">+</span></button>
  <div class="bx-a"><p>No. The page keeps its own authority, but the equity it can pass gets divided among all the pages it links to, so more outgoing links means less equity per link.</p></div>
  <button class="bx-q">Do nofollow links pass any ranking authority?<span class="ic">+</span></button>
  <div class="bx-a"><p>By default, no. Nofollow links instruct search engines not to consider them for ranking purposes, though they can still drive referral traffic.</p></div>
  <button class="bx-q">Do 301 redirects pass full authority to the new page?<span class="ic">+</span></button>
  <div class="bx-a"><p>Mostly, for genuine 1:1 URL replacements. Google has confirmed redirects retain most or all PageRank in that scenario, though redirect chains can dilute it further.</p></div>
  <button class="bx-q">How many links per page is too many before value dilutes?<span class="ic">+</span></button>
  <div class="bx-a"><p>A large-scale study found traffic peaking around 45 to 50 links per page. Beyond that, each additional link's equity share becomes negligible.</p></div>
</div>

<div class="bx-related-box">
<h3>Related Articles</h3>
<ul>
<li><a href="/anchor-text-optimization-best-practices/" target="_blank" rel="noopener">Anchor Text Optimization: Best Practices for Better Rankings</a></li>
<li><a href="/competitor-backlink-analysis/" target="_blank" rel="noopener">Competitor Backlink Analysis: Step-by-Step Guide</a></li>
<li><a href="/digital-pr-vs-traditional-link-building/" target="_blank" rel="noopener">Digital PR vs Traditional Link Building</a></li>
<li><a href="/what-is-off-page-seo-complete-beginners-guide/" target="_blank" rel="noopener">What Is Off-Page SEO? Complete Beginner's Guide</a></li>
</ul>
</div>

<div class="bx-learn">
<h3>What We Learn Today</h3>
<div class="bx-learn-grid">
<div class="bx-learn-card"><p>Link equity traces back to Google's original 1998 PageRank algorithm</p></div>
<div class="bx-learn-card"><p>Equity divides among all outgoing dofollow links on a page</p></div>
<div class="bx-learn-card"><p>Link placement in body content passes more equity than footers</p></div>
<div class="bx-learn-card"><p>Broken internal links are silent, common equity leaks</p></div>
<div class="bx-learn-card"><p>301 redirects retain most equity for genuine 1:1 replacements</p></div>
<div class="bx-learn-card"><p>Traffic peaks around 45-50 links per page before dilution sets in</p></div>
</div>
</div>

<!-- CTA -->
<section class="bx-cta">
  <h2 id="build-a-complete-off-page-seo-foundation">Build a Complete Off-Page SEO Foundation</h2>
  <p>Link equity works hand in hand with anchor text and backlink strategy. Explore our anchor text and competitor backlink guides next.</p>
  <div class="bx-actions">
    <a class="bx-btn primary" href="/anchor-text-optimization-best-practices/" target="_blank" rel="noopener">Anchor Text Optimization</a>
    <a class="bx-btn ghost" href="/competitor-backlink-analysis/" target="_blank" rel="noopener">Competitor Backlink Analysis</a>
  </div>
</section>

</div><!-- /.bmc-flow -->

<script>
(function(){
  var root=document.currentScript.parentNode.querySelector('.bmc-flow')||document;
  var qs=root.querySelectorAll('#bxFaq .bx-q');
  qs.forEach(function(q){q.addEventListener('click',function(){
    var a=q.nextElementSibling, open=q.classList.contains('on');
    qs.forEach(function(x){x.classList.remove('on');x.nextElementSibling.classList.remove('on');});
    if(!open){q.classList.add('on');a.classList.add('on');}
  });});
})();
</script>
