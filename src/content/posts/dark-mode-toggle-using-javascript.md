---
title: "Dark Mode Toggle Using JavaScript: Complete Implementation Guide"
slug: "dark-mode-toggle-using-javascript"
date: "2026-08-24T06:39:49"
updated: "2026-08-24T06:40:11"
author: "santajigade"
categories: ["javascript"]
primaryCategory: "javascript"
description: "Dark mode toggle using JavaScript: real code for the preference cascade, preventing the flash of wrong theme, and syncing with live OS changes."
focusKeyword: "Dark Mode Toggle"
image: "/wp-content/uploads/2026/08/Dark-Mode-Toggle.webp"
imageAlt: "Dark Mode Toggle"
words: 1086
views: 58
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
<span class="bx-meta-pill">Dark Mode</span>
<span class="bx-meta-pill">JavaScript</span>
<span class="bx-meta-pill">2026</span>
</div>

<p class="bx-lede">A dark mode toggle using JavaScript needs to solve three things at once: read the user's saved preference, respect their OS setting when no preference exists yet, and apply the theme before the page actually renders to avoid a jarring flash of the wrong color scheme.</p>

<h2 id="dark-mode-toggle-basics"><span class="bx-num">01</span>Dark Mode Toggle Using JavaScript: The Core Pattern</h2>
<div class="bx-rule"></div>
<p>The pattern practitioners call the "preference cascade" checks three sources in order: localStorage first, since it reflects an explicit user choice, then the prefers-color-scheme media query as a fallback, then a default light theme if neither applies.</p>

<p>Getting the initial page load right matters more than the toggle button itself. Applying the theme class before the page renders prevents what's commonly called FOUC, a flash of unstyled or incorrectly themed content that briefly shows the wrong colors before JavaScript corrects it.</p>

<div class="bx-specs">
<div class="bx-spec"><div class="v">3</div><div class="k">sources checked in order: localStorage, then OS preference, then default</div></div>
<div class="bx-spec"><div class="v">1</div><div class="k">inline script needed in the head to prevent a flash of the wrong theme</div></div>
<div class="bx-spec"><div class="v">0</div><div class="k">external libraries required for a complete vanilla JS implementation</div></div>
</div>

<!-- OPENING ADSENSE CODE -->
<div class="bx-ad-wrap">
<div class="bx-ad-divider" style="margin-bottom:20px;"><div class="bx-ad-line"></div><span>Advertisement</span><div class="bx-ad-line"></div></div>
<ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-3931314195561246" data-ad-slot="4249015278" data-ad-format="auto" data-full-width-responsive="true"></ins>
<script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
<div class="bx-ad-divider" style="margin-top:20px;"><div class="bx-ad-line"></div><span>Advertisement</span><div class="bx-ad-line"></div></div>
</div>
<!-- CLOSING ADSENSE CODE -->

<h2 id="prevent-flash"><span class="bx-num">02</span>Preventing the Flash of Wrong Theme</h2>
<div class="bx-rule"></div>
<p><a href="https://dev.to/wrux/super-simple-light-dark-mode-switch-38nl" target="_blank" rel="noopener">Callum's guide on DEV Community</a> gets the ordering right: this inline script needs to sit at the very top of the head, executed as early as possible, before any CSS or content renders.</p>

<div class="bx-code">
<div class="bx-code-label">Inline Head Script: Prevent Flash of Wrong Theme</div>
<pre>&lt;script&gt;
  document.documentElement.classList.toggle(
    'dark',
    localStorage.theme === 'dark' ||
    (!('theme' in localStorage) &&
      window.matchMedia('(prefers-color-scheme: dark)').matches)
  );
&lt;/script&gt;</pre>
</div>

<div class="bx-dyk">
<span class="lbl">🔎 Did you know?</span>
<p><a href="https://olliewilliams.xyz/blog/dark-mode/" target="_blank" rel="noopener">Ollie Williams' guide</a> highlights a simpler native option many implementations skip: setting a meta tag with name="color-scheme" and content="light dark" lets the browser handle native form controls, scrollbars, and other built-in UI elements automatically, without any custom CSS needed for those specific pieces.</p>
</div>

<!-- OPENING ADSENSE CODE -->
<div class="bx-ad-wrap">
<div class="bx-ad-divider" style="margin-bottom:20px;"><div class="bx-ad-line"></div><span>Advertisement</span><div class="bx-ad-line"></div></div>
<ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-3931314195561246" data-ad-slot="4249015278" data-ad-format="auto" data-full-width-responsive="true"></ins>
<script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
<div class="bx-ad-divider" style="margin-top:20px;"><div class="bx-ad-line"></div><span>Advertisement</span><div class="bx-ad-line"></div></div>
</div>
<!-- CLOSING ADSENSE CODE -->

<h2 id="toggle-function"><span class="bx-num">03</span>The Toggle Button Function</h2>
<div class="bx-rule"></div>
<p>Once the initial theme is set correctly, the toggle itself just needs to flip the class and save the new preference. <a href="https://whitep4nth3r.com/blog/best-light-dark-mode-theme-toggle-javascript/" target="_blank" rel="noopener">whitep4nth3r's guide</a> calls this the "preference cascade" in action, with the stored user preference always taking priority once it exists.</p>

<div class="bx-code">
<div class="bx-code-label">Full Toggle Implementation With Persistence</div>
<pre>function getInitialTheme() {
  const saved = localStorage.getItem('theme');
  if (saved) return saved;

  return window.matchMedia('(prefers-color-scheme: dark)').matches
    ? 'dark'
    : 'light';
}

function applyTheme(theme) {
  document.documentElement.classList.toggle('dark', theme === 'dark');
  localStorage.setItem('theme', theme);
}

// Set initial theme on page load
applyTheme(getInitialTheme());

// Wire up the toggle button
document.getElementById('theme-toggle').addEventListener('click', () => {
  const isDark = document.documentElement.classList.contains('dark');
  applyTheme(isDark ? 'light' : 'dark');
});</pre>
</div>

<h2 id="css-variables"><span class="bx-num">04</span>Pairing the Toggle With CSS Custom Properties</h2>
<div class="bx-rule"></div>
<p>The JavaScript only manages one class, all actual color values should live in CSS custom properties. This keeps the toggle logic simple and makes adding a third theme, or adjusting colors later, a CSS-only change.</p>

<div class="bx-code">
<div class="bx-code-label">CSS Custom Properties for Theming</div>
<pre>:root {
  --bg-color: #ffffff;
  --text-color: #1a1a1a;
  --border-color: #e0e0e0;
  color-scheme: light dark;
}

html.dark {
  --bg-color: #1a1a1a;
  --text-color: #f0f0f0;
  --border-color: #3a3a3a;
}

body {
  background-color: var(--bg-color);
  color: var(--text-color);
  transition: background-color 0.2s ease, color 0.2s ease;
}</pre>
</div>

<!-- OPENING ADSENSE CODE -->
<div class="bx-ad-wrap">
<div class="bx-ad-divider" style="margin-bottom:20px;"><div class="bx-ad-line"></div><span>Advertisement</span><div class="bx-ad-line"></div></div>
<ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-3931314195561246" data-ad-slot="4249015278" data-ad-format="auto" data-full-width-responsive="true"></ins>
<script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
<div class="bx-ad-divider" style="margin-top:20px;"><div class="bx-ad-line"></div><span>Advertisement</span><div class="bx-ad-line"></div></div>
</div>
<!-- CLOSING ADSENSE CODE -->

<h2 id="listening-os-changes"><span class="bx-num">05</span>Listening for Live OS Theme Changes</h2>
<div class="bx-rule"></div>
<p>Some users switch their OS theme while your site is still open. <a href="https://dev.to/abbeyperini/dark-mode-toggle-and-prefers-color-scheme-4f3m" target="_blank" rel="noopener">Abbey Perini's guide</a> covers listening for this properly, but only when the user hasn't explicitly overridden the setting themselves, otherwise a manual choice would get silently overwritten.</p>

<div class="bx-code">
<div class="bx-code-label">Respond to Live OS Preference Changes</div>
<pre>const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');

mediaQuery.addEventListener('change', (e) => {
  // Only respond to OS changes if the user hasn't set an explicit preference
  if (!localStorage.getItem('theme')) {
    applyTheme(e.matches ? 'dark' : 'light');
  }
});</pre>
</div>

<p>💡 Quick Tip: test this behavior using Chrome DevTools' Rendering panel, which lets you emulate prefers-color-scheme without actually changing your OS settings, making it far faster to verify both branches of the logic.</p>

<h2 id="table"><span class="bx-num">06</span>Storage Approach Comparison</h2>
<div class="bx-rule"></div>
<p>A quick reference for the different ways to persist a theme preference.</p>

<div class="bx-table-wrap">
<table class="bx-table">
<thead>
<tr><th>Storage Method</th><th>Persists Across</th><th>Best For</th></tr>
</thead>
<tbody>
<tr><td>localStorage</td><td>Sessions, same browser only</td><td>Most sites, no backend required</td></tr>
<tr><td>Cookie + server-side</td><td>Devices, if tied to a user account</td><td>Logged-in apps wanting cross-device sync</td></tr>
<tr><td>prefers-color-scheme only</td><td>Nothing explicit, follows OS always</td><td>Simple sites with no manual override needed</td></tr>
</tbody>
</table>
</div>

<h2 id="checklist"><span class="bx-num">07</span>Implementation Checklist</h2>
<div class="bx-rule"></div>
<p>A short list to confirm before shipping a dark mode toggle to production.</p>

<div class="bx-checklist">
<div class="bx-check-item"><div class="bx-check-icon"></div><p><strong>Inline the initial theme script in the head</strong>, applying it after first paint causes a visible flash.</p></div>
<div class="bx-check-item"><div class="bx-check-icon"></div><p><strong>Check localStorage before OS preference</strong>, an explicit user choice should always win.</p></div>
<div class="bx-check-item"><div class="bx-check-icon"></div><p><strong>Keep all colors in CSS custom properties</strong>, never hardcode colors that need to change per theme.</p></div>
<div class="bx-check-item"><div class="bx-check-icon"></div><p><strong>Set color-scheme in CSS</strong>, this helps native browser UI like scrollbars and form controls match automatically.</p></div>
<div class="bx-check-item"><div class="bx-check-icon"></div><p><strong>Only listen for OS changes when no explicit choice exists</strong>, otherwise a manual toggle gets silently overridden.</p></div>
</div>

<h2 id="faq"><span class="bx-num">08</span>Common Questions</h2>
<div class="bx-rule"></div>
<div class="bx-faq" id="bxFaq">
<button class="bx-q">Why does my dark mode toggle briefly show the wrong theme on load?<span class="ic">+</span></button>
<div class="bx-a"><p>This is the flash of wrong theme (FOUC) problem. It happens when the theme is applied after the page renders. Fix it by inlining a small script at the very top of the head that runs before first paint.</p></div>
<button class="bx-q">Should I check localStorage or OS preference first?<span class="ic">+</span></button>
<div class="bx-a"><p>Check localStorage first. If the user has explicitly chosen a theme before, that choice should always take priority over their current OS-level setting.</p></div>
<button class="bx-q">Do I need JavaScript for dark mode, or can CSS alone handle it?<span class="ic">+</span></button>
<div class="bx-a"><p>CSS alone with prefers-color-scheme works if you only want to follow the OS setting. JavaScript is needed if you want to let users manually override that setting and remember their choice.</p></div>
<button class="bx-q">What does the color-scheme CSS property actually do?<span class="ic">+</span></button>
<div class="bx-a"><p>It tells the browser to automatically theme native UI elements, like scrollbars, form inputs, and date pickers, to match the current color scheme without needing custom CSS for each one.</p></div>
<button class="bx-q">How do I test dark mode without changing my OS settings?<span class="ic">+</span></button>
<div class="bx-a"><p>Chrome DevTools has a Rendering panel that lets you emulate prefers-color-scheme directly in the browser, letting you test both light and dark branches without touching your actual system settings.</p></div>
</div>

<div class="bx-related-box">
<h3>Related Articles</h3>
<ul>
<li><a href="/auto-highlight-current-heading-scrolling/" target="_blank" rel="noopener">Auto Highlight Current Heading While Scrolling</a></li>
<li><a href="/auto-generate-table-of-contents-headings/" target="_blank" rel="noopener">How to Automatically Generate Table of Contents from Headings</a></li>
<li><a href="/how-to-detect-broken-links-javascript/" target="_blank" rel="noopener">How to Detect Broken Links Using JavaScript</a></li>
</ul>
</div>

<div class="bx-learn">
<h3>What We Learn Today</h3>
<div class="bx-learn-grid">
<div class="bx-learn-card"><p>Check localStorage, then OS preference, then default</p></div>
<div class="bx-learn-card"><p>Inline the initial theme script to prevent a visible flash</p></div>
<div class="bx-learn-card"><p>Keep colors in CSS custom properties, not JavaScript</p></div>
<div class="bx-learn-card"><p>Set color-scheme so native browser UI matches automatically</p></div>
<div class="bx-learn-card"><p>Only auto-follow OS changes when no explicit choice exists</p></div>
<div class="bx-learn-card"><p>DevTools can emulate prefers-color-scheme for easier testing</p></div>
</div>
</div>

<section class="bx-cta">
<h2 id="build-a-complete-front-end-javascript-toolkit">Build a Complete Front-End JavaScript Toolkit</h2>
<p>Dark mode pairs well with other content UX features like scrollspy highlighting and auto-generated navigation. Explore both guides next.</p>
<div class="bx-actions">
<a class="bx-btn primary" href="/auto-highlight-current-heading-scrolling/" target="_blank" rel="noopener">Auto Highlight Current Heading</a>
<a class="bx-btn ghost" href="/auto-generate-table-of-contents-headings/" target="_blank" rel="noopener">Auto-Generate Table of Contents</a>
</div>
</section>

</div>
<script>
(function(){var root=document.currentScript.parentNode.querySelector('.bmc-flow')||document;var qs=root.querySelectorAll('#bxFaq .bx-q');qs.forEach(function(q){q.addEventListener('click',function(){var a=q.nextElementSibling,open=q.classList.contains('on');qs.forEach(function(x){x.classList.remove('on');x.nextElementSibling.classList.remove('on');});if(!open){q.classList.add('on');a.classList.add('on');}});});})();
</script>
