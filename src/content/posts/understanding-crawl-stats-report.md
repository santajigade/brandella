---
title: "Understanding Google Search Console Crawl Stats Report: A Simple Guide"
slug: "understanding-crawl-stats-report"
date: "2026-08-09T05:02:04"
updated: "2026-08-09T08:37:11"
author: "santajigade"
categories: ["google-search-console", "seo"]
primaryCategory: "google-search-console"
description: "Understanding the Crawl Stats report in Google Search Console, explained simply. See what the numbers mean and what to check first."
focusKeyword: "Crawl Stats report"
takeaways:
  - "The Crawl Stats report in Search Console shows how often Google crawls your site and how your server responds."
  - "You find it under Settings, then Crawling, then Open Report, not in the main menu."
  - "Check host status first; green means your server is reliable enough for Google to crawl smoothly."
  - "Watch for sudden spikes or drops in crawl requests and a rising average response time."
  - "Google says sites with fewer than 1,000 pages usually do not need to worry about crawl budget."
image: "/wp-content/uploads/2026/08/Crawl-Stats-report.webp"
imageAlt: "Crawl Stats report"
words: 1570
views: 80
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

.bmc-flow .bx-tip{border-left:5px solid var(--bx-green);background:#eef8e8;border-radius:0 10px 10px 0;padding:17px 20px;margin:20px 0 30px;}
.bmc-flow .bx-tip .lbl{font-family:var(--bx-disp);text-transform:uppercase;letter-spacing:1px;font-size:17px;color:#3f9421;font-weight:700;display:flex;align-items:center;gap:8px;margin-bottom:8px;}
.bmc-flow .bx-tip ul{margin:0;padding-left:20px;}
.bmc-flow .bx-tip li{font-size:17px;color:#2f5a1c;margin-bottom:6px;}
.bmc-flow .bx-tip li:last-child{margin-bottom:0;}

.bmc-flow .bx-dyk{border-left:5px solid var(--bx-blue);background:#eef4fb;border-radius:0 10px 10px 0;padding:17px 20px;margin:20px 0 30px;}
.bmc-flow .bx-dyk .lbl{font-family:var(--bx-disp);text-transform:uppercase;letter-spacing:1px;font-size:17px;color:#3a6ea5;font-weight:700;display:flex;align-items:center;gap:8px;margin-bottom:6px;}
.bmc-flow .bx-dyk p{margin:0;font-size:17px;color:#2c4a6b;}

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
<span class="bx-meta-pill">Technical SEO</span>
<span class="bx-meta-pill">Google Search Console</span>
<span class="bx-meta-pill">Crawl Stats</span>
<span class="bx-meta-pill">2026</span>
</div>

<p class="bx-lede">The Crawl Stats report is one of those Google Search Console features that sounds scary but really isn't. Once you know what to look for, it's just Google telling you: "here's how I've been visiting your website lately, and here's how well your server handled it."</p>

<p>Most people never open this report. It's tucked away in Settings, not on the main menu, so it's easy to miss. But if you run a bigger site, or you're chasing down a weird indexing problem, this is where you'll find real clues, not guesses.</p>

<p>In plain words: it shows you how many times Google visited your site, how much data it downloaded, how fast your server answered, and whether anything went wrong along the way.</p>

<p>Let's walk through it together, piece by piece, in plain language, no jargon left unexplained.</p>

<div class="bx-specs">
<div class="bx-spec"><div class="v">90 days</div><div class="k">how far back the Crawl Stats report shows you data</div></div>
<div class="bx-spec"><div class="v">1,000+</div><div class="k">pages is roughly when Google says this report starts being genuinely useful</div></div>
<div class="bx-spec"><div class="v">3</div><div class="k">main things to watch: crawl requests, response time, and host status</div></div>
</div>
<h2 id="what-is-it"><span class="bx-num">01</span>So, What Is the Crawl Stats Report?</h2>
<div class="bx-rule"></div>
<p>Here's the simplest way to put it. Google's own <a href="https://support.google.com/webmasters/answer/9679690?hl=en" target="_blank" rel="noopener">Search Console Help page</a> says the Crawl Stats report shows statistics about Google's crawling history on your website, how many requests were made, what your server replied with, and any availability problems Google ran into.</p>

<p>Think of "crawling" as Google's robot, called Googlebot, walking through your website page by page, clicking links, downloading files, and taking notes. The Crawl Stats report is basically Googlebot's diary from the last 90 days.</p>

<div class="bx-dyk">
<span class="lbl">🔎 Did you know?</span>
<p>Google's own help page says if your site has fewer than a thousand pages, you probably don't need to worry about this report at all. It's really built with bigger, busier sites in mind, ones where Google has to make choices about what to crawl and when.</p>
</div>

<h2 id="where-to-find"><span class="bx-num">02</span>Where Do You Actually Find It?</h2>
<div class="bx-rule"></div>
<p>This is the part people get stuck on. <a href="https://neilpatel.com/blog/google-search-console-crawl-stats/" target="_blank" rel="noopener">Neil Patel's guide</a> points out it's not sitting in the main left-hand menu like most reports. You'll find it under Settings, then a section called Crawling, then a link that says "Open Report" next to Crawl stats.</p>

<p><a href="https://rightblogger.com/blog/crawl-stats-report" target="_blank" rel="noopener">RightBlogger's 2026 guide</a> adds one thing worth knowing before you go looking: this report only shows up for root-level properties. That means your whole domain (like example.com), not a sub-folder property like example.com/blog/. If you only verified a subfolder in Search Console, you simply won't see this report.</p>
<h2 id="the-main-numbers"><span class="bx-num">03</span>The Main Numbers You'll See</h2>
<div class="bx-rule"></div>
<p>When the report opens, you'll see a chart and a handful of numbers. <a href="https://nkyseo.com/crawl-stats-report/" target="_blank" rel="noopener">Nkyseo's 2026 walkthrough</a> breaks it down nicely: total crawl requests tells you how active Google has been on your site, and average response time tells you how fast your server felt from Google's side.</p>

<p><a href="https://devendergupta.netlify.app/blog/google-search-console-crawl-stats/" target="_blank" rel="noopener">Devender Gupta's guide</a> adds a third dimension worth knowing: every single "fetch" Google makes gets sorted by response code (like 200 for success or 404 for not found), file type (HTML, images, JS, CSS), and the purpose of the crawl (discovering something new versus refreshing something old).</p>

<div class="bx-tip">
<span class="lbl">💡 Quick tip</span>
<ul>
<li>Total crawl requests includes both successful AND failed visits, so a high number isn't automatically good.</li>
<li>Watch for sudden spikes or drops more than the exact numbers themselves.</li>
<li>Compare this week to last week, not just one single day.</li>
</ul>
</div>

<h2 id="host-status"><span class="bx-num">04</span>What "Host Status" Means (and Why Green Matters)</h2>
<div class="bx-rule"></div>
<p>Host status is basically Google's report card on whether your server is reliable enough to crawl smoothly. Google's official documentation says the goal is simple: you want to see green. If it's red, click in and you'll see exactly what's wrong, robots.txt availability, DNS problems, or the server just not responding fast enough.</p>

<p>You don't need to memorize every technical term here. Just remember: green means "all good," red means "something's blocking Google, go look closer."</p>

<h2 id="video"><span class="bx-num">05</span>Watch: Google Explains the Crawl Stats Report</h2>
<div class="bx-rule"></div>
<p>This one's straight from Google itself. Search Advocate Daniel Waisberg walks through every section of the report and explains what the data actually means for your site.</p>

<div class="bx-video-wrap">
<div class="bx-video-frame">
<iframe src="https://www.youtube.com/embed/x_GoMrl6_u0" title="Crawl Budget and the Crawl Stats Report - Google Search Console Training" allowfullscreen></iframe>
</div>
<div class="bx-video-cap">"Crawl Budget and the Crawl Stats Report" — Daniel Waisberg, Google Search Console Training. Source: YouTube.</div>
</div>

<h2 id="common-problems"><span class="bx-num">06</span>What Problems Can This Report Actually Reveal?</h2>
<div class="bx-rule"></div>
<p><a href="https://www.siteguru.co/seo-academy/google-search-console-crawl-stats-report" target="_blank" rel="noopener">SiteGuru's guide</a> puts it in plain, useful questions you can actually answer once you're in the report: is Google spending its time on the pages that matter to your business, or is a chunk of that effort going to waste on 404 pages and errors instead?</p>

<p><a href="https://entail.ai/resources/seo/googles-crawl-stats-report-guide" target="_blank" rel="noopener">Entail AI's guide</a> adds one more thing to watch for: if Google notices lots of your pages don't seem valuable, it may quietly crawl your site less. That drop in crawling often shows up right around the same time pages start getting stuck in "crawled – not indexed" or "discovered – not indexed" status.</p>

<div class="bx-dyk">
<span class="lbl">🔎 Did you know?</span>
<p><a href="https://edwardbate.com/resources/google-search-console-crawl-stats-guide/" target="_blank" rel="noopener">Edward Bate's guide</a> notes that "crawl budget" genuinely isn't something 95% of websites need to worry about, especially if you're under about 1,000 to 10,000 pages. It only becomes a real concern for very large sites.</p>
</div>
<h2 id="table"><span class="bx-num">07</span>A Simple Cheat Sheet for the Report</h2>
<div class="bx-rule"></div>
<p>Here's a quick reference so you don't have to remember everything at once.</p>

<div class="bx-table-wrap">
<table class="bx-table">
<thead>
<tr><th>What You See</th><th>What It Means</th><th>What To Do</th></tr>
</thead>
<tbody>
<tr><td>Total crawl requests</td><td>How often Google visited your site</td><td>Watch for big spikes or sudden drops</td></tr>
<tr><td>Total download size</td><td>How much data Google downloaded</td><td>A steady climb is normal; a huge jump isn't</td></tr>
<tr><td>Average response time</td><td>How fast your server answered Google</td><td>Slower times can hurt crawling and indexing</td></tr>
<tr><td>Host status</td><td>Overall server health and availability</td><td>Green is good; red needs a closer look</td></tr>
<tr><td>By response code</td><td>How many pages returned 200, 404, 301, etc.</td><td>Lots of 404s means wasted crawl effort</td></tr>
</tbody>
</table>
</div>

<h2 id="checklist"><span class="bx-num">08</span>What to Check First (Your Simple Starting Checklist)</h2>
<div class="bx-rule"></div>
<p>You don't need to analyze every chart at once. Start here.</p>

<div class="bx-checklist">
<div class="bx-check-item"><div class="bx-check-icon"></div><p><strong>Check your host status first.</strong> If it's green, you can relax a little and move on to the details.</p></div>
<div class="bx-check-item"><div class="bx-check-icon"></div><p><strong>Look for sudden spikes or drops</strong> in crawl requests. That's usually a bigger clue than the exact number itself.</p></div>
<div class="bx-check-item"><div class="bx-check-icon"></div><p><strong>See if response times are climbing.</strong> A slower server can quietly hurt how much Google crawls.</p></div>
<div class="bx-check-item"><div class="bx-check-icon"></div><p><strong>Check the response code breakdown</strong> for a high share of 404s or errors, that's wasted crawl effort.</p></div>
<div class="bx-check-item"><div class="bx-check-icon"></div><p><strong>Line up any weird pattern with a recent change</strong>, like a migration, a plugin update, or new content batch.</p></div>
</div>

<h2 id="stepper"><span class="bx-num">09</span>A Simple Step-by-Step Walkthrough</h2>
<div class="bx-rule"></div>
<p>Here's the order I'd check things in, one step at a time. Tap each one for a plain explanation.</p>

<div class="bx-steps" id="bxSteps">
  <div class="dc-hint">Tap a step &darr;</div>
  <div class="bx-track" role="group" aria-label="Crawl Stats report simple walkthrough steps">
    <div class="bx-step on" data-t="Open the Report" data-d="Go to Settings, then Crawling, then click Open Report next to Crawl stats. Remember, this only works on root-level properties."><div class="no">1</div><div class="lb">Open It</div></div>
    <div class="bx-step" data-t="Check Host Status" data-d="Look at the top summary. Green means healthy. Red means something is blocking Google, click in to see what."><div class="no">2</div><div class="lb">Host Status</div></div>
    <div class="bx-step" data-t="Scan the Trend Line" data-d="Look at the crawl requests chart over the last 90 days. Are you seeing a steady pattern, or a strange spike or cliff?"><div class="no">3</div><div class="lb">Trend Line</div></div>
    <div class="bx-step" data-t="Check Response Codes" data-d="See how many crawls returned 200 versus 404 or other errors. A high error share means wasted crawl time."><div class="no">4</div><div class="lb">Response Codes</div></div>
    <div class="bx-step" data-t="Match It to a Change" data-d="If something looks off, check what changed around that date, a migration, new content, or a site update."><div class="no">5</div><div class="lb">Find the Cause</div></div>
  </div>
  <div class="bx-stepdetail" aria-live="polite">
    <p class="dt-t" id="bxStepT">Open the Report</p>
    <p class="dt-d" id="bxStepD">Go to Settings, then Crawling, then click Open Report next to Crawl stats. Remember, this only works on root-level properties.</p>
  </div>
</div>

<h2 id="score"><span class="bx-num">10</span>Quick Crawl Health Check</h2>
<div class="bx-rule"></div>
<p>Answer a few simple questions about what you're seeing in your report to get a quick read on how healthy things look.</p>

<div class="bx-calc">
<div class="bx-calc-header">
<h3>Quick Crawl Health Check</h3>
<p>Select the option that matches what you see in your report</p>
</div>
<div class="bx-calc-body">

<div class="bx-calc-factor">
<div class="bx-calc-factor-top"><label>Host status</label><span>35 pts</span></div>
<select class="bx-calc-select" data-weight="35" onchange="bxCalc()">
<option value="0">Red, showing errors</option>
<option value="0.5">Not sure / never checked</option>
<option value="1">Green</option>
</select>
</div>

<div class="bx-calc-factor">
<div class="bx-calc-factor-top"><label>Crawl request trend</label><span>25 pts</span></div>
<select class="bx-calc-select" data-weight="25" onchange="bxCalc()">
<option value="0">Sharp, unexplained drop recently</option>
<option value="0.5">Some ups and downs, nothing extreme</option>
<option value="1">Fairly steady over the last 90 days</option>
</select>
</div>

<div class="bx-calc-factor">
<div class="bx-calc-factor-top"><label>Response codes</label><span>25 pts</span></div>
<select class="bx-calc-select" data-weight="25" onchange="bxCalc()">
<option value="0">Lots of 404s or errors</option>
<option value="0.5">A small, normal share of errors</option>
<option value="1">Mostly 200s, very few errors</option>
</select>
</div>

<div class="bx-calc-factor">
<div class="bx-calc-factor-top"><label>Average response time</label><span>15 pts</span></div>
<select class="bx-calc-select" data-weight="15" onchange="bxCalc()">
<option value="0">Slow or climbing steadily</option>
<option value="0.5">Average, not great not terrible</option>
<option value="1">Fast and consistent</option>
</select>
</div>

<div class="bx-calc-gauge-wrap">
<div class="bx-calc-gauge-track"><div class="bx-calc-gauge-fill" id="bxGaugeFill"><span id="bxGaugeScore">0%</span></div></div>
<div class="bx-calc-verdict" id="bxVerdict">Answer each question to see your quick health check.</div>
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
  if(pct >= 80){ verdict.innerText = "Looking healthy! Just keep an eye on it every so often."; }
  else if(pct >= 50){ verdict.innerText = "Mostly okay, but worth digging into the weaker spots."; }
  else if(pct > 0){ verdict.innerText = "A few things need attention. Start with host status and error codes."; }
  else { verdict.innerText = "Answer each question to see your quick health check."; }
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

<h2 id="faq"><span class="bx-num">11</span>Common Questions About the Crawl Stats Report</h2>
<div class="bx-rule"></div>

<div class="bx-faq" id="bxFaq">
  <button class="bx-q">Do I really need to check this report?<span class="ic">+</span></button>
  <div class="bx-a"><p>Not really, if your site is small. Google itself says sites under 1,000 pages usually don't need to worry about this level of detail.</p></div>
  <button class="bx-q">Why can't I find the Crawl Stats report in my account?<span class="ic">+</span></button>
  <div class="bx-a"><p>It's only available for root-level properties (your whole domain), not for a subfolder property. Also, check under Settings, not the main menu.</p></div>
  <button class="bx-q">What does a red host status actually mean?<span class="ic">+</span></button>
  <div class="bx-a"><p>It means Google ran into a problem crawling your site, like DNS issues, robots.txt trouble, or your server not responding well enough.</p></div>
  <button class="bx-q">Does more crawling always mean better SEO?<span class="ic">+</span></button>
  <div class="bx-a"><p>Not automatically. More crawling can be a good sign, but it can also mean Google is wasting time on error pages. Look at what's being crawled, not just how much.</p></div>
  <button class="bx-q">How far back does the data go?<span class="ic">+</span></button>
  <div class="bx-a"><p>The report shows data for the last 90 days, so you can spot patterns over time instead of judging from a single day.</p></div>
</div>

<div class="bx-related-box">
<h3>Related Articles</h3>
<ul>
<li><a href="/url-inspection-tool-diagnose-indexing-problems/" target="_blank" rel="noopener">How to Use the URL Inspection Tool to Diagnose Indexing Problems</a></li>
<li><a href="/discovered-currently-not-indexed-fix/" target="_blank" rel="noopener">How to Fix "Discovered – Currently Not Indexed" Pages</a></li>
<li><a href="/meta-robots-tags-explained-2/" target="_blank" rel="noopener">Meta Robots Tags Explained: Index, Noindex, Follow, Nofollow, and More</a></li>
<li><a href="/how-to-test-mobile-friendliness-website/" target="_blank" rel="noopener">How to Test Mobile Friendliness of a Website</a></li>
</ul>
</div>

<div class="bx-learn">
<h3>What We Learn Today</h3>
<div class="bx-learn-grid">
<div class="bx-learn-card"><p>The Crawl Stats report shows Google's last 90 days of visits</p></div>
<div class="bx-learn-card"><p>It's hidden under Settings, not the main menu</p></div>
<div class="bx-learn-card"><p>Only available for root-level properties, not subfolders</p></div>
<div class="bx-learn-card"><p>Host status green means healthy, red means investigate</p></div>
<div class="bx-learn-card"><p>Sites under 1,000 pages rarely need to worry about this report</p></div>
<div class="bx-learn-card"><p>Watch trends and patterns, not single numbers in isolation</p></div>
</div>
</div>

<!-- CTA -->
<section class="bx-cta">
  <h2 id="build-a-complete-technical-seo-foundation">Build a Complete Technical SEO Foundation</h2>
  <p>Crawl Stats pairs perfectly with the URL Inspection tool and fixing indexing issues. Explore both guides next.</p>
  <div class="bx-actions">
    <a class="bx-btn primary" href="/url-inspection-tool-diagnose-indexing-problems/" target="_blank" rel="noopener">URL Inspection Tool Guide</a>
    <a class="bx-btn ghost" href="/discovered-currently-not-indexed-fix/" target="_blank" rel="noopener">Fix Discovered Not Indexed</a>
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
