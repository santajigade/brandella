---
title: "Auto Highlight Current Heading Scrolling (Scrollspy)"
slug: "auto-highlight-current-heading-scrolling"
date: "2026-08-23T15:22:05"
updated: "2026-08-23T15:23:55"
author: "santajigade"
categories: ["technical-seo"]
primaryCategory: "technical-seo"
description: "Auto highlight current heading scrolling: real IntersectionObserver code, the short last-section fix, and fixed-header offset handling."
focusKeyword: "highlight current heading scrolling"
takeaways:
  - "Scrollspy highlights the table of contents link for the section currently visible, and IntersectionObserver does this more efficiently than scroll listeners."
  - "A rootMargin bottom value of -70% means only headings in the top 30% of the viewport count as active."
  - "The last heading on a page is often too short to cross the threshold, so a scroll-position check near the page bottom should force-activate it."
  - "A fixed header can be handled by adding a negative top rootMargin equal to the header's height."
  - "The script should only toggle an active class, with all visual styling kept in CSS."
image: "/wp-content/uploads/2026/08/highlight-current-heading-scrolling.webp"
imageAlt: "highlight current heading scrolling"
words: 1410
views: 70
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
<span class="bx-meta-pill">Technical SEO</span>
<span class="bx-meta-pill">Scrollspy</span>
<span class="bx-meta-pill">JavaScript</span>
<span class="bx-meta-pill">2026</span>
</div>

<p class="bx-lede">Auto highlighting the current heading while scrolling, often called "scrollspy," works by watching which section is currently visible in the viewport and marking the matching table of contents link as active. The modern, efficient way to do this uses IntersectionObserver rather than a scroll event listener.</p>

<p><a href="https://www.andrewgilliland.dev/articles/intersection-observer-api/" target="_blank" rel="noopener">Andrew Gilliland's guide</a> on the Intersection Observer API explains the core mechanism: an IntersectionObserver watches one or more elements and fires a callback whenever their intersection with a root element, the viewport by default, crosses a threshold you define. Scroll listeners, by contrast, fire dozens of times per second and force expensive layout recalculations if not carefully throttled.</p>

<div class="bx-dyk">
<span class="lbl">🔎 Did you know?</span>
<p>The term "ScrollSpy" actually originated with the Bootstrap framework, which used it for a jQuery-based navigation mechanism that watched scroll position and updated active links. Modern implementations swap Bootstrap's original scroll-math approach for IntersectionObserver, but the name has stuck across the JavaScript ecosystem.</p>
</div>

<p>This pattern works best paired with a <a href="/auto-generate-table-of-contents-headings/" target="_blank" rel="noopener">table of contents generated from your page's actual headings</a>, since scrollspy highlighting has nothing to highlight without a linked navigation list already in place.</p>

<p>Here's the working code for basic highlighting, handling the tricky edge case of short sections near the bottom of a page, and a version that accounts for a fixed header.</p>

<div class="bx-specs">
<div class="bx-spec"><div class="v">0</div><div class="k">scroll event listeners needed when using IntersectionObserver instead</div></div>
<div class="bx-spec"><div class="v">-70%</div><div class="k">typical rootMargin offset used to trigger highlighting before a section reaches page center</div></div>
<div class="bx-spec"><div class="v">1</div><div class="k">active class applied at a time, removed from all others on every intersection change</div></div>
</div>

<!-- OPENING ADSENSE CODE -->
<div class="bx-ad-wrap">
<div class="bx-ad-divider" style="margin-bottom:20px;"><div class="bx-ad-line"></div><span>Advertisement</span><div class="bx-ad-line"></div></div>
<ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-3931314195561246" data-ad-slot="4249015278" data-ad-format="auto" data-full-width-responsive="true"></ins>
<script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
<div class="bx-ad-divider" style="margin-top:20px;"><div class="bx-ad-line"></div><span>Advertisement</span><div class="bx-ad-line"></div></div>
</div>
<!-- CLOSING ADSENSE CODE -->

<h2 id="basic-highlight"><span class="bx-num">01</span>Basic Scroll Highlighting With IntersectionObserver</h2>
<div class="bx-rule"></div>
<p>The core pattern: observe every heading in the content, and whenever one crosses the intersection threshold, remove the active class from all table of contents links and add it to the one matching that heading's ID.</p>

<div class="bx-code">
<div class="bx-code-label">Basic Scrollspy Highlighting</div>
<pre>function highlightActiveHeading(contentSelector, tocSelector) {
  const headings = document.querySelectorAll(`${contentSelector} h2, ${contentSelector} h3`);
  const tocLinks = document.querySelectorAll(`${tocSelector} a`);

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        tocLinks.forEach(link => link.classList.remove('active'));

        const activeLink = document.querySelector(
          `${tocSelector} a[href="#${entry.target.id}"]`
        );
        if (activeLink) activeLink.classList.add('active');
      }
    });
  }, {
    rootMargin: '0px 0px -70% 0px'
  });

  headings.forEach(heading => observer.observe(heading));
}

highlightActiveHeading('.article-content', '#toc');</pre>
</div>

<h2 id="why-rootmargin"><span class="bx-num">02</span>Why the rootMargin Value Matters</h2>
<div class="bx-rule"></div>
<p>The rootMargin option shrinks the effective viewport used for intersection detection. Andrew Gilliland's guide, referenced above, explains it directly: a bottom value of "-70% 0px" shrinks the bottom of the detection zone by 70%, so only headings in the top 30% of the viewport are considered active, which makes the highlight feel like it tracks where a reader is actually looking.</p>

<p>Without this adjustment, a heading barely peeking into view at the bottom of the screen would trigger highlighting prematurely, well before a reader has actually scrolled to that section.</p>

<div class="bx-note" style="border-left-color:#4a9e24;background:#eef8e8;">
<span class="lbl" style="color:#3f9421;">💡 Quick Tip</span>
<p style="color:#2e5c1a;">Start with -70% and adjust from there by watching your actual page in DevTools. A value that feels right on a short blog post can feel too aggressive on a dense documentation page with many closely-spaced headings, so treat it as a tunable setting, not a fixed constant.</p>
</div>

<!-- OPENING ADSENSE CODE -->
<div class="bx-ad-wrap">
<div class="bx-ad-divider" style="margin-bottom:20px;"><div class="bx-ad-line"></div><span>Advertisement</span><div class="bx-ad-line"></div></div>
<ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-3931314195561246" data-ad-slot="4249015278" data-ad-format="auto" data-full-width-responsive="true"></ins>
<script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
<div class="bx-ad-divider" style="margin-top:20px;"><div class="bx-ad-line"></div><span>Advertisement</span><div class="bx-ad-line"></div></div>
</div>
<!-- CLOSING ADSENSE CODE -->

<h2 id="last-section"><span class="bx-num">03</span>Handling the Short Last Section Edge Case</h2>
<div class="bx-rule"></div>
<p><a href="https://benfrain.com/building-a-table-of-contents-with-active-indicator-using-javascript-intersection-observers/" target="_blank" rel="noopener">Ben Frain's writeup</a> on building a table of contents with the Intersection Observer API documents this exact edge case: when a heading tag stops intersecting the viewport at the bottom versus the top, the correct behavior differs. A common bug is that the final heading on a page is often too short to ever cross a 70% rootMargin threshold, since there isn't enough content below it to push the viewport that far. This version explicitly checks for scroll position near the bottom of the page and force-activates the last heading.</p>

<div class="bx-code">
<div class="bx-code-label">Scrollspy With Last-Section Fix</div>
<pre>function highlightActiveHeadingSafe(contentSelector, tocSelector) {
  const headings = Array.from(
    document.querySelectorAll(`${contentSelector} h2, ${contentSelector} h3`)
  );
  const tocLinks = document.querySelectorAll(`${tocSelector} a`);

  function setActive(id) {
    tocLinks.forEach(link => link.classList.remove('active'));
    const activeLink = document.querySelector(`${tocSelector} a[href="#${id}"]`);
    if (activeLink) activeLink.classList.add('active');
  }

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        setActive(entry.target.id);
      }
    });
  }, { rootMargin: '0px 0px -70% 0px' });

  headings.forEach(heading => observer.observe(heading));

  // Force-activate the last heading when the page is scrolled to the bottom
  window.addEventListener('scroll', () => {
    const scrolledToBottom =
      window.innerHeight + window.scrollY >= document.body.scrollHeight - 10;

    if (scrolledToBottom && headings.length) {
      setActive(headings[headings.length - 1].id);
    }
  }, { passive: true });
}</pre>
</div>

<h2 id="fixed-header"><span class="bx-num">04</span>Accounting for a Fixed Header</h2>
<div class="bx-rule"></div>
<p><a href="https://blog.maximeheckel.com/posts/scrollspy-demystified/" target="_blank" rel="noopener">Maxime Heckel's deep-dive</a> on scrollspy implementation covers this directly: the Intersection Observer API's rootMargin option adds margins around the viewport before computing intersection, so a fixed header can be accounted for by adding a negative top margin equal to the header's height, making the intersection end earlier by that same amount.</p>

<div class="bx-code">
<div class="bx-code-label">Scrollspy Adjusted for a Fixed Header</div>
<pre>function highlightWithFixedHeader(contentSelector, tocSelector, headerHeight = 80) {
  const headings = document.querySelectorAll(`${contentSelector} h2, ${contentSelector} h3`);
  const tocLinks = document.querySelectorAll(`${tocSelector} a`);

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        tocLinks.forEach(link => link.classList.remove('active'));
        const activeLink = document.querySelector(
          `${tocSelector} a[href="#${entry.target.id}"]`
        );
        if (activeLink) activeLink.classList.add('active');
      }
    });
  }, {
    // Offset the top by the header height, bottom by 70% as before
    rootMargin: `-${headerHeight}px 0px -70% 0px`
  });

  headings.forEach(heading => observer.observe(heading));
}

highlightWithFixedHeader('.article-content', '#toc', 80);</pre>
</div>

<!-- OPENING ADSENSE CODE -->
<div class="bx-ad-wrap">
<div class="bx-ad-divider" style="margin-bottom:20px;"><div class="bx-ad-line"></div><span>Advertisement</span><div class="bx-ad-line"></div></div>
<ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-3931314195561246" data-ad-slot="4249015278" data-ad-format="auto" data-full-width-responsive="true"></ins>
<script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
<div class="bx-ad-divider" style="margin-top:20px;"><div class="bx-ad-line"></div><span>Advertisement</span><div class="bx-ad-line"></div></div>
</div>
<!-- CLOSING ADSENSE CODE -->

<h2 id="css-example"><span class="bx-num">05</span>Styling the Active State</h2>
<div class="bx-rule"></div>
<p>The JavaScript only toggles a class, actual visual styling belongs in CSS. A simple, effective active-link style just needs a color and weight change, plus a smooth transition.</p>

<p>If your active links are pointing at broken or renamed anchor IDs, they'll silently fail to highlight at all, so it's worth periodically running a <a href="/how-to-detect-broken-links-javascript/" target="_blank" rel="noopener">broken link check across your site</a> to catch stale anchors before they quietly break navigation.</p>

<div class="bx-code">
<div class="bx-code-label">Basic Active-Link CSS</div>
<pre>#toc a {
  display: block;
  padding: 4px 0;
  color: #5a6570;
  text-decoration: none;
  transition: color 0.2s ease, font-weight 0.2s ease;
}

#toc a.active {
  color: #4a9e24;
  font-weight: 700;
  border-left: 2px solid #4a9e24;
  padding-left: 8px;
}</pre>
</div>

<h2 id="table"><span class="bx-num">06</span>Approach Comparison</h2>
<div class="bx-rule"></div>
<p>A quick reference comparing scroll listeners to IntersectionObserver.</p>

<div class="bx-table-wrap">
<table class="bx-table">
<thead>
<tr><th>Approach</th><th>Performance</th><th>Complexity</th></tr>
</thead>
<tbody>
<tr><td>Scroll event listener</td><td>Fires constantly, needs manual throttling</td><td>Simple but easy to get wrong</td></tr>
<tr><td>IntersectionObserver</td><td>Async, off main thread, efficient by default</td><td>Slightly more setup, no throttling needed</td></tr>
<tr><td>Scroll listener + requestAnimationFrame</td><td>Better than raw scroll, still main-thread work</td><td>Moderate, manual frame management</td></tr>
</tbody>
</table>
</div>

<h2 id="checklist"><span class="bx-num">07</span>Practical Notes Before Shipping</h2>
<div class="bx-rule"></div>
<p>A few things worth checking before this goes into production.</p>

<div class="bx-checklist">
<div class="bx-check-item"><div class="bx-check-icon"></div><p><strong>Use IntersectionObserver over scroll listeners</strong>, it avoids constant recalculation and runs more efficiently.</p></div>
<div class="bx-check-item"><div class="bx-check-icon"></div><p><strong>Tune the rootMargin to your layout</strong>, the right offset depends on your header height and desired trigger point.</p></div>
<div class="bx-check-item"><div class="bx-check-icon"></div><p><strong>Handle the short last-section edge case</strong>, otherwise the final heading may never get highlighted.</p></div>
<div class="bx-check-item"><div class="bx-check-icon"></div><p><strong>Keep styling in CSS, not JavaScript</strong>, the script should only toggle a class.</p></div>
<div class="bx-check-item"><div class="bx-check-icon"></div><p><strong>Test with a fixed header if you have one</strong>, headings can scroll underneath it before appearing visually active.</p></div>
</div>

<h2 id="faq"><span class="bx-num">08</span>Common Questions</h2>
<div class="bx-rule"></div>
<div class="bx-faq" id="bxFaq">
<button class="bx-q">Why use IntersectionObserver instead of a scroll event listener?<span class="ic">+</span></button>
<div class="bx-a"><p>IntersectionObserver runs asynchronously off the main thread and doesn't require manual throttling, making it significantly more efficient than a scroll listener that fires dozens of times per second.</p></div>
<button class="bx-q">Why does the last heading on my page never get highlighted?<span class="ic">+</span></button>
<div class="bx-a"><p>A short final section often doesn't have enough content below it to cross the rootMargin threshold. A scroll-to-bottom check that force-activates the last heading fixes this.</p></div>
<button class="bx-q">What does the rootMargin option actually control?<span class="ic">+</span></button>
<div class="bx-a"><p>It shrinks the effective viewport used for intersection detection, letting you control exactly when a heading is considered "in view" relative to the actual visible screen area.</p></div>
<button class="bx-q">Do I need to adjust anything for a sticky header?<span class="ic">+</span></button>
<div class="bx-a"><p>Yes. Offset the top rootMargin value by your header's pixel height, otherwise headings will appear active while still partially hidden underneath the fixed header.</p></div>
<button class="bx-q">Should the active state styling live in JavaScript or CSS?<span class="ic">+</span></button>
<div class="bx-a"><p>CSS. The JavaScript should only add or remove a class name; all visual styling, colors, transitions, and borders belong in your stylesheet.</p></div>
</div>

<div class="bx-related-box">
<h3>Related Articles</h3>
<ul>
<li><a href="/auto-generate-table-of-contents-headings/" target="_blank" rel="noopener">How to Automatically Generate Table of Contents from Headings</a></li>
<li><a href="/how-to-detect-broken-links-javascript/" target="_blank" rel="noopener">How to Detect Broken Links Using JavaScript</a></li>
<li><a href="/canonical-tag-implementation-guide/" target="_blank" rel="noopener">Canonical Tag Implementation Guide</a></li>
</ul>
</div>

<div class="bx-learn">
<h3>What We Learn Today</h3>
<div class="bx-learn-grid">
<div class="bx-learn-card"><p>IntersectionObserver beats scroll listeners for performance</p></div>
<div class="bx-learn-card"><p>rootMargin controls exactly when a heading counts as active</p></div>
<div class="bx-learn-card"><p>Short last sections need a manual scroll-to-bottom fix</p></div>
<div class="bx-learn-card"><p>Fixed headers require offsetting the top rootMargin value</p></div>
<div class="bx-learn-card"><p>JavaScript should only toggle classes, not apply styles directly</p></div>
<div class="bx-learn-card"><p>One active class should be applied at a time, removed from all others first</p></div>
</div>
</div>

<section class="bx-cta">
<h2 id="build-a-complete-content-navigation-toolkit">Build a Complete Content Navigation Toolkit</h2>
<p>Scrollspy highlighting pairs directly with table of contents generation for long-form content. Explore both guides next.</p>
<div class="bx-actions">
<a class="bx-btn primary" href="/auto-generate-table-of-contents-headings/" target="_blank" rel="noopener">Auto-Generate Table of Contents</a>
<a class="bx-btn ghost" href="/how-to-detect-broken-links-javascript/" target="_blank" rel="noopener">Detect Broken Links Using JavaScript</a>
</div>
</section>

</div>
<script>
(function(){var root=document.currentScript.parentNode.querySelector('.bmc-flow')||document;var qs=root.querySelectorAll('#bxFaq .bx-q');qs.forEach(function(q){q.addEventListener('click',function(){var a=q.nextElementSibling,open=q.classList.contains('on');qs.forEach(function(x){x.classList.remove('on');x.nextElementSibling.classList.remove('on');});if(!open){q.classList.add('on');a.classList.add('on');}});});})();
</script>
