---
title: "Reading Time Calculator for Blog Posts: Formula and JavaScript"
slug: "reading-time-calculator-blog-posts"
date: "2026-08-24T06:48:44"
updated: "2026-08-24T06:50:06"
author: "santajigade"
categories: ["development", "javascript"]
primaryCategory: "javascript"
description: "Reading time calculator for blog posts: the real word-count-to-WPM formula, why Medium uses 265 WPM, and working JavaScript to build your own."
focusKeyword: "reading time calculator"
takeaways:
  - "Reading time equals word count divided by words per minute, so a 1,000-word article at 200 WPM takes 5 minutes."
  - "Medium uses 265 WPM and Google's reference point is 200 WPM, while technical documentation should use about 150 WPM."
  - "Each image adds roughly 12-20 seconds of viewing time and complex tables can add 30-60+ seconds, so word count alone understates reading time."
  - "Estimates should be rounded up with Math.ceil and calculated from the live DOM so they stay accurate as content changes."
  - "Displaying reading time can increase engagement by around 30%, and Medium found posts of about 7 minutes earn the highest engagement."
image: "/wp-content/uploads/2026/08/reading-time-calculator.webp"
imageAlt: "reading time calculator"
words: 975
views: 43
format: "html"
---
<div class="bmc-flow">
<style>
@import url('https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600;700;800&display=swap');
.bmc-flow{--bx-green:#5DB92E;--bx-green-deep:#4a9e24;--bx-gold:#F4B41A;--bx-ink:#2b2b2b;--bx-steel:#5a6570;--bx-steel-2:#8a96a1;--bx-line:#E3EDE0;--bx-red:#c95d5d;--bx-blue:#6fa8dc;--bx-disp:'Open Sans',Arial,sans-serif;--bx-body:'Open Sans',system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif;font-family:var(--bx-body);font-weight:400;font-style:normal;color:var(--bx-ink);line-height:1.75;font-size:17px;max-width:920px;margin:0 auto;padding:0;-webkit-font-smoothing:antialiased;}
.bmc-flow *{box-sizing:border-box;}
.bmc-flow p{margin:0 0 14px;font-size:17px;}
.bmc-flow a{color:var(--bx-green-deep);text-decoration:none;font-weight:600;}
.bmc-flow a:hover{color:var(--bx-green);}
.bmc-flow strong{font-weight:700;}
.bmc-flow h2{font-family:var(--bx-disp);font-weight:700;font-size:26px;line-height:1.2;margin:36px 0 16px;color:var(--bx-ink);}
.bmc-flow h2 .bx-num{color:var(--bx-green);font-weight:800;margin-right:8px;}
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
.bmc-flow .bx-dyk{border-left:5px solid var(--bx-blue);background:#eef4fb;border-radius:0 10px 10px 0;padding:17px 20px;margin:20px 0 30px;}
.bmc-flow .bx-dyk .lbl{font-family:var(--bx-disp);text-transform:uppercase;letter-spacing:1px;font-size:17px;color:#3a6ea5;font-weight:700;display:flex;align-items:center;gap:8px;margin-bottom:6px;}
.bmc-flow .bx-dyk p{margin:0;font-size:17px;color:#2c4a6b;}
.bmc-flow .bx-checklist{display:flex;flex-direction:column;gap:10px;margin:20px 0 30px;}
.bmc-flow .bx-check-item{display:flex;gap:13px;background:#fff;border:1px solid var(--bx-line);border-left:4px solid var(--bx-green);border-radius:10px;padding:14px 17px;align-items:flex-start;}
.bmc-flow .bx-check-icon{width:22px;height:22px;border-radius:6px;background:var(--bx-green);flex-shrink:0;margin-top:2px;position:relative;}
.bmc-flow .bx-check-icon::after{content:"✓";position:absolute;top:-2px;left:5px;color:#fff;font-weight:800;font-size:13px;}
.bmc-flow .bx-check-item p{margin:0;font-size:17px;color:#3a3a3a;}
.bmc-flow .bx-check-item strong{color:var(--bx-ink);}
.bmc-flow .bx-table-wrap{overflow-x:auto;margin:20px 0 30px;}
.bmc-flow .bx-table{width:100%;border-collapse:collapse;font-size:17px;}
.bmc-flow .bx-table th{background:var(--bx-ink);color:#fff;padding:13px 16px;text-align:left;font-family:var(--bx-disp);font-weight:600;font-size:17px;}
.bmc-flow .bx-table td{padding:13px 16px;border-bottom:1px solid var(--bx-line);font-size:17px;}
.bmc-flow .bx-table tr:nth-child(even) td{background:#f7faf5;}
.bmc-flow .bx-code{background:#20272C;border-radius:14px;padding:20px 22px;margin:20px 0 30px;overflow-x:auto;}
.bmc-flow .bx-code pre{margin:0;font-family:'Courier New',monospace;font-size:14px;line-height:1.6;color:#c7e8b8;white-space:pre-wrap;word-break:break-word;}
.bmc-flow .bx-code-label{font-family:var(--bx-disp);color:var(--bx-steel-2);text-transform:uppercase;letter-spacing:1.2px;font-size:13px;margin-bottom:10px;font-weight:600;}
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
.bmc-flow .bx-calc-select,.bmc-flow .bx-calc-input{width:100%;padding:8px 10px;border-radius:8px;border:1px solid var(--bx-line);font-size:17px;color:#3a3a3a;font-family:var(--bx-body);background:#f7faf5;}
.bmc-flow .bx-calc-gauge-wrap{margin-top:20px;background:#f7faf5;border-radius:12px;padding:20px;text-align:center;}
.bmc-flow .bx-calc-gauge-track{background:#e8ece7;border-radius:20px;height:28px;overflow:hidden;margin-bottom:12px;}
.bmc-flow .bx-calc-gauge-fill{height:100%;background:linear-gradient(90deg,#c95d5d,#e2a52c,#5DB92E);border-radius:20px;width:0%;transition:width 0.4s ease;display:flex;align-items:center;justify-content:flex-end;padding-right:10px;}
.bmc-flow .bx-calc-gauge-fill span{color:#fff;font-weight:800;font-size:17px;}
.bmc-flow .bx-calc-verdict{font-size:17px;font-weight:700;color:var(--bx-ink);}
.bmc-flow .bx-faq{border:1px solid var(--bx-line);border-radius:12px;overflow:hidden;background:#fff;margin:20px 0 30px;}
.bmc-flow .bx-q{width:100%;text-align:left;background:#fff;border:0;border-top:1px solid var(--bx-line);padding:16px 17px;cursor:pointer;font-family:var(--bx-disp);font-weight:600;font-size:17px;color:var(--bx-ink);display:flex;justify-content:space-between;align-items:center;gap:12px;}
.bmc-flow .bx-faq .bx-q:first-child{border-top:0;}
.bmc-flow .bx-q .ic{color:var(--bx-green);font-weight:800;flex:0 0 auto;transition:transform .2s ease;font-size:20px;}
.bmc-flow .bx-q.on .ic{transform:rotate(45deg);}
.bmc-flow .bx-a{max-height:0;overflow:hidden;transition:max-height .3s ease;padding:0 17px;}
.bmc-flow .bx-a.on{max-height:360px;}
.bmc-flow .bx-a p{padding:2px 0 16px;margin:0;font-size:17px;color:var(--bx-steel);}
.bmc-flow .bx-cta{position:relative;overflow:hidden;border-radius:17px;margin:30px 0 8px;padding:36px 30px;color:#fff;background:radial-gradient(120% 160% at 12% 10%,rgba(244,180,26,.25),transparent 46%),linear-gradient(135deg,#5DB92E 0%,#3f9421 55%,#245214 100%);}
.bmc-flow .bx-cta h2{color:#fff!important;margin:0 0 8px;}
.bmc-flow .bx-cta p{color:rgba(255,255,255,.94)!important;max-width:560px;margin:0 0 20px;font-size:17px;}
.bmc-flow .bx-actions{display:flex;flex-wrap:wrap;gap:12px;}
.bmc-flow .bx-btn{display:inline-flex;align-items:center;gap:8px;font-family:var(--bx-disp);font-size:17px;font-weight:700;padding:12px 20px;border-radius:40px;text-decoration:none;border:0;}
.bmc-flow .bx-btn.primary{background:#fff;color:var(--bx-green-deep)!important;}
.bmc-flow .bx-btn.ghost{background:rgba(255,255,255,.12);color:#fff!important;border:1.5px solid rgba(255,255,255,.55);}
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
.bmc-flow .bx-ad-wrap{margin:40px 0;}
.bmc-flow .bx-ad-divider{display:flex;align-items:center;gap:12px;}
.bmc-flow .bx-ad-divider span{font-size:12px;color:#777;font-weight:600;letter-spacing:1px;text-transform:uppercase;}
.bmc-flow .bx-ad-line{flex:1;border-top:2px dotted #bdbdbd;}
</style>

<div class="bx-meta-row">
<span class="bx-meta-pill">SEO Tools</span>
<span class="bx-meta-pill">Reading Time</span>
<span class="bx-meta-pill">JavaScript</span>
<span class="bx-meta-pill">2026</span>
</div>

<p class="bx-lede">A reading time calculator for blog posts uses one simple formula: word count divided by reading speed in words per minute. Medium uses 265 WPM, Google's own reference standard is 200 WPM, and most implementations land somewhere in the 200-250 range for general web content.</p>

<p>Displaying <a href="https://dev.to/joebailey26/the-importance-of-read-time-for-blog-posts-and-how-to-automatically-generate-it-using-nodejs-1pmk">reading time </a>isn't just a nice-to-have. Research shows it can increase engagement by 30%, since readers can decide whether they have time to commit before they start.</p>

<p>Here's the exact formula, real working JavaScript, and the adjustments that make an estimate meaningfully more accurate than a bare word-count division.</p>

<div class="bx-specs">
<div class="bx-spec"><div class="v">238</div><div class="k">WPM average adult silent reading speed, based on a meta-analysis of 18,000+ participants</div></div>
<div class="bx-spec"><div class="v">30%</div><div class="k">engagement increase reported when reading time is displayed on blog posts</div></div>
<div class="bx-spec"><div class="v">7</div><div class="k">minutes, the read time Medium found achieves the highest engagement</div></div>
</div>
<h2 id="formula"><span class="bx-num">01</span>The Reading Time Formula</h2>
<div class="bx-rule"></div>
<p>The base formula behind every reading time calculator is straightforward: Reading Time = Word Count ÷ Words Per Minute. A 1,000-word article at 200 WPM comes out to 5 minutes.</p>

<p>The WPM value you pick matters more than it seems. Medium uses 265 WPM, general web standards range from 200-250, and Google's own reference point is 200 WPM. Technical or dense content should use a slower estimate, since research shows comprehension drops significantly above 300 WPM.</p>

<h2 id="basic-code"><span class="bx-num">02</span>Basic Working JavaScript</h2>
<div class="bx-rule"></div>
<p>Here's the simplest working version: grab the article text, split it into words, divide by WPM, and round up so a reader is never disappointed by an underestimate.</p>

<div class="bx-code">
<div class="bx-code-label">Basic Reading Time Calculator</div>
<pre>function calculateReadingTime(text, wpm = 238) {
  const words = text.trim().split(/\s+/).length;
  const minutes = Math.ceil(words / wpm);
  return minutes;
}

// Usage
const articleText = document.querySelector('.article-content').innerText;
const readTime = calculateReadingTime(articleText);
document.getElementById('reading-time').innerText = `${readTime} min read`;</pre>
</div>
<h2 id="images-accuracy"><span class="bx-num">03</span>Accounting for Images: The Part Most Calculators Skip</h2>
<div class="bx-rule"></div>
<p>Word count alone understates total engagement time for heavily illustrated content. Each image adds roughly 12-20 seconds of viewing time, decreasing slightly for each additional image as readers skim faster through a gallery. Complex tables or figures can add 30-60+ seconds for real comprehension.</p>

<div class="bx-code">
<div class="bx-code-label">Reading Time With Image Time Added</div>
<pre>function calculateReadingTimeWithImages(text, imageCount, wpm = 265) {
  const words = text.trim().split(/\s+/).length;
  const wordMinutes = words / wpm;

  // First image adds 12s, decreasing by 1s per image down to a 3s floor
  let imageSeconds = 0;
  for (let i = 0; i < imageCount; i++) {
    imageSeconds += Math.max(12 - i, 3);
  }

  const totalMinutes = wordMinutes + (imageSeconds / 60);
  return Math.ceil(totalMinutes);
}

// Example: 1,500 words, 5 images, 265 WPM ≈ 6-7 min read
const readTime = calculateReadingTimeWithImages(articleText, 5);</pre>
</div>

<h2 id="dom-scan"><span class="bx-num">04</span>Auto-Detecting Word Count and Images From the DOM</h2>
<div class="bx-rule"></div>
<p>Rather than hardcoding values, scan the actual rendered article container so the estimate updates automatically whenever content changes, no manual recalculation required.</p>

<div class="bx-code">
<div class="bx-code-label">Fully Automatic: Scan DOM for Words and Images</div>
<pre>function autoReadingTime(containerSelector, wpm = 238) {
  const container = document.querySelector(containerSelector);
  if (!container) return null;

  const text = container.innerText || container.textContent;
  const words = text.trim().split(/\s+/).filter(Boolean).length;
  const images = container.querySelectorAll('img').length;

  const wordMinutes = words / wpm;
  let imageSeconds = 0;
  for (let i = 0; i < images; i++) {
    imageSeconds += Math.max(12 - i, 3);
  }

  const totalMinutes = Math.ceil(wordMinutes + imageSeconds / 60);

  return {
    minutes: totalMinutes,
    words: words,
    images: images,
    label: totalMinutes < 1 ? 'Less than a minute' : `${totalMinutes} min read`
  };
}

const result = autoReadingTime('.article-content');
document.getElementById('reading-time').innerText = result.label;</pre>
</div>
<h2 id="table"><span class="bx-num">05</span>Reading Speed Reference by Content Type</h2>
<div class="bx-rule"></div>
<p>Different content types genuinely need different WPM assumptions for an accurate estimate.</p>

<div class="bx-table-wrap">
<table class="bx-table">
<thead>
<tr><th>Content Type</th><th>Recommended WPM</th><th>Why</th></tr>
</thead>
<tbody>
<tr><td>Technical documentation</td><td>150 WPM</td><td>Readers re-read sections, code needs careful parsing</td></tr>
<tr><td>Standard blog posts</td><td>200-238 WPM</td><td>General web reading speed, Google's own reference point</td></tr>
<tr><td>Casual/listicle content</td><td>250-300 WPM</td><td>Readers skim familiar, easy-to-scan content</td></tr>
<tr><td>Fiction/narrative</td><td>260 WPM</td><td>Faster natural flow than non-fiction analysis</td></tr>
</tbody>
</table>
</div>

<h2 id="interactive"><span class="bx-num">06</span>Try It: Reading Time Estimator</h2>
<div class="bx-rule"></div>
<p>Enter a word count and pick a reading speed to see the estimate update live.</p>

<div class="bx-calc">
<div class="bx-calc-header"><h3>Reading Time Estimator</h3><p>Enter your word count and select a reading speed</p></div>
<div class="bx-calc-body">
<div class="bx-calc-factor">
<div class="bx-calc-factor-top"><label>Word count</label></div>
<input type="number" class="bx-calc-input" id="bxWordCount" value="1500" min="0" oninput="bxReadCalc()">
</div>
<div class="bx-calc-factor">
<div class="bx-calc-factor-top"><label>Reading speed</label></div>
<select class="bx-calc-select" id="bxWpm" onchange="bxReadCalc()">
<option value="150">Slow / Technical (150 WPM)</option>
<option value="238" selected>Average Adult (238 WPM)</option>
<option value="265">Medium's Standard (265 WPM)</option>
<option value="300">Fast Skimmer (300 WPM)</option>
</select>
</div>
<div class="bx-calc-gauge-wrap">
<div class="bx-calc-verdict" id="bxReadVerdict">≈ 6 min read</div>
</div>
</div>
</div>

<script>
function bxReadCalc(){
  var words = parseFloat(document.getElementById('bxWordCount').value) || 0;
  var wpm = parseFloat(document.getElementById('bxWpm').value);
  var minutes = Math.ceil(words / wpm);
  var label = minutes < 1 ? 'Less than a minute' : '≈ ' + minutes + ' min read';
  document.getElementById('bxReadVerdict').innerText = label;
}
bxReadCalc();
</script>

<h2 id="checklist"><span class="bx-num">07</span>Implementation Best Practices</h2>
<div class="bx-rule"></div>
<p>A short list for getting reading time estimates right.</p>

<div class="bx-checklist">
<div class="bx-check-item"><div class="bx-check-icon"></div><p><strong>Round up, never down</strong>, an underestimate disappoints readers more than a slight overestimate.</p></div>
<div class="bx-check-item"><div class="bx-check-icon"></div><p><strong>Adjust WPM by content type</strong>, technical docs need 150 WPM, casual posts can use 250+.</p></div>
<div class="bx-check-item"><div class="bx-check-icon"></div><p><strong>Add time for images and tables</strong>, word count alone understates true engagement time on visual content.</p></div>
<div class="bx-check-item"><div class="bx-check-icon"></div><p><strong>Scan the live DOM, not static values</strong>, so the estimate stays accurate as content is edited.</p></div>
<div class="bx-check-item"><div class="bx-check-icon"></div><p><strong>Show it near the title</strong>, readers decide whether to commit before they start scrolling.</p></div>
</div>

<h2 id="faq"><span class="bx-num">08</span>Common Questions</h2>
<div class="bx-rule"></div>
<div class="bx-faq" id="bxFaq">
<button class="bx-q">What WPM should I use for my blog's reading time?<span class="ic">+</span></button>
<div class="bx-a"><p>200-250 WPM covers most general blog content. Use 150 WPM for technical documentation, and up to 265 WPM (Medium's standard) for casual, easy-to-read posts.</p></div>
<button class="bx-q">Does displaying reading time actually improve engagement?<span class="ic">+</span></button>
<div class="bx-a"><p>Yes. Research shows displaying reading time on blog posts can increase engagement by around 30%, since it helps readers commit with clear expectations upfront.</p></div>
<button class="bx-q">Should I round reading time up or down?<span class="ic">+</span></button>
<div class="bx-a"><p>Round up using Math.ceil(). Underestimating disappoints readers who expected a shorter read, while a small overestimate rarely causes a problem.</p></div>
<button class="bx-q">Do images actually affect reading time calculations?<span class="ic">+</span></button>
<div class="bx-a"><p>Yes, meaningfully. Each image adds roughly 12-20 seconds of viewing time, and ignoring this can noticeably understate true reading time on image-heavy posts.</p></div>
<button class="bx-q">What's the ideal blog post length for engagement?<span class="ic">+</span></button>
<div class="bx-a"><p>Research from Medium found posts around 7 minutes (roughly 1,855 words at 265 WPM) achieve the highest engagement, though this varies by content type and audience.</p></div>
</div>

<div class="bx-related-box">
<h3>Related Articles</h3>
<ul>
<li><a href="/auto-generate-table-of-contents-headings/" target="_blank" rel="noopener">How to Automatically Generate Table of Contents from Headings</a></li>
<li><a href="/how-to-detect-broken-links-javascript/" target="_blank" rel="noopener">How to Detect Broken Links Using JavaScript</a></li>
<li><a href="/25-seo-best-practices-in-2026-to-boost-rankings/" target="_blank" rel="noopener">25 SEO Best Practices in 2026 to Boost Rankings</a></li>
</ul>
</div>

<div class="bx-learn">
<h3>What We Learn Today</h3>
<div class="bx-learn-grid">
<div class="bx-learn-card"><p>Reading Time = Word Count ÷ Words Per Minute</p></div>
<div class="bx-learn-card"><p>WPM should vary by content type, not stay fixed</p></div>
<div class="bx-learn-card"><p>Images add real, measurable time beyond word count alone</p></div>
<div class="bx-learn-card"><p>Displaying reading time can lift engagement by around 30%</p></div>
<div class="bx-learn-card"><p>Always round up to avoid disappointing readers</p></div>
<div class="bx-learn-card"><p>Scanning the live DOM keeps estimates accurate as content changes</p></div>
</div>
</div>

<section class="bx-cta">
<h2 id="build-a-complete-content-ux-toolkit">Build a Complete Content UX Toolkit</h2>
<p>Reading time pairs well with table of contents generation for long-form content. Explore both guides next.</p>
<div class="bx-actions">
<a class="bx-btn primary" href="/auto-generate-table-of-contents-headings/" target="_blank" rel="noopener">Auto-Generate Table of Contents</a>
<a class="bx-btn ghost" href="/how-to-detect-broken-links-javascript/" target="_blank" rel="noopener">Detect Broken Links Using JavaScript</a>
</div>
</section>

</div>
<script>
(function(){var root=document.currentScript.parentNode.querySelector('.bmc-flow')||document;var qs=root.querySelectorAll('#bxFaq .bx-q');qs.forEach(function(q){q.addEventListener('click',function(){var a=q.nextElementSibling,open=q.classList.contains('on');qs.forEach(function(x){x.classList.remove('on');x.nextElementSibling.classList.remove('on');});if(!open){q.classList.add('on');a.classList.add('on');}});});})();
</script>
