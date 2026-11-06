---
title: "Build Your Own XML Sitemap Generator in PHP"
slug: "build-xml-sitemap-generator-php"
date: "2026-07-31T09:53:02"
updated: "2026-08-09T08:40:06"
author: "santajigade"
categories: ["seo", "technical-seo"]
primaryCategory: "seo"
description: "Build a working PHP sitemap generator in four versions array-based, directory scanner, database-driven, and sitemap-index for 50,000+ URLs."
focusKeyword: "sitemap generator"
image: "/wp-content/uploads/2026/07/sitemap-generator.webp"
imageAlt: "sitemap generator"
words: 1824
views: 103
format: "html"
---
<div class="bsg-wrap">
<style>
.bsg-wrap{font-family:'Segoe UI', Arial, sans-serif;font-size:17px;line-height:1.75;color:#2e2e2e;max-width:100%;}
.bsg-wrap h2{font-size:25px;color:#2b2b2b;margin:36px 0 16px;font-weight:800;border-left:5px solid #5DB92E;padding-left:14px;}
.bsg-wrap h3{font-size:19px;color:#2b2b2b;margin:18px 0 10px;font-weight:700;}
.bsg-wrap p{margin:0 0 14px;font-size:17px;}
.bsg-wrap a{color:#3f9421;font-weight:600;text-decoration:none;}
.bsg-wrap a:hover{color:#2f7418;text-decoration:none;}
.bsg-wrap ul,.bsg-wrap ol{margin:0 0 16px;padding-left:22px;}
.bsg-wrap li{margin-bottom:8px;font-size:17px;}

.bsg-lede{font-size:20px;color:#333;font-style:italic;margin:0 0 18px;line-height:1.6;border-left:3px solid #5DB92E;padding-left:16px;}

.bsg-meta-row{display:flex;flex-wrap:wrap;gap:10px;margin:0 0 24px;}
.bsg-meta-pill{background:#eef8e8;color:#3f9421;border:1px solid #cdeabb;border-radius:20px;padding:6px 16px;font-size:13px;font-weight:700;text-transform:uppercase;letter-spacing:.5px;}

/* Stat cards */
.bsg-stat-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin:20px 0 30px;}
.bsg-stat-card{background:#f7faf5;border:1px solid #e3ede0;border-radius:12px;padding:22px 16px;text-align:center;}
.bsg-stat-num{font-size:32px;font-weight:800;color:#5DB92E;margin-bottom:6px;}
.bsg-stat-card p{margin:0;font-size:17px;color:#4a4a4a;}
@media(max-width:820px){.bsg-stat-grid{grid-template-columns:1fr;}}

/* Pipeline illustration */
.bsg-pipeline{margin:20px 0 30px;background:#fff;border:1px solid #e3ede0;border-radius:14px;padding:24px 18px;}
.bsg-pipe-row{display:flex;align-items:center;gap:6px;flex-wrap:wrap;justify-content:center;}
.bsg-pipe-step{background:#f7faf5;border:2px solid #5DB92E;border-radius:10px;padding:12px 10px;text-align:center;font-size:13px;font-weight:700;color:#2b2b2b;flex:1;min-width:110px;}
.bsg-pipe-step .n{display:block;color:#5DB92E;font-size:11px;font-weight:800;margin-bottom:4px;}
.bsg-pipe-arrow{color:#5DB92E;font-weight:800;font-size:18px;}
@media(max-width:820px){.bsg-pipe-row{flex-direction:column;}}

/* Code block */
.bsg-code-box{background:#1e1e1e;border-radius:12px;padding:20px 22px;margin:20px 0 10px;overflow-x:auto;}
.bsg-code-box pre{margin:0;font-family:'Consolas','Monaco',monospace;font-size:13px;line-height:1.6;color:#d4d4d4;white-space:pre;}
.bsg-code-box .k{color:#c586c0;}
.bsg-code-box .s{color:#ce9178;}
.bsg-code-box .c{color:#6a9955;}
.bsg-code-box .v{color:#9cdcfe;}
.bsg-code-box .f{color:#dcdcaa;}
.bsg-code-caption{font-size:14px;color:#7a7a7a;margin:8px 0 26px;text-align:center;}

/* Steps */
.bsg-steps{display:flex;flex-direction:column;gap:14px;margin:20px 0 30px;}
.bsg-step{display:flex;gap:16px;background:#fff;border:1px solid #e3ede0;border-radius:12px;padding:18px 20px;align-items:flex-start;}
.bsg-step-num{width:36px;height:36px;border-radius:50%;background:#5DB92E;color:#fff;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:17px;flex-shrink:0;}
.bsg-step h3{margin:0 0 6px;font-size:17px;}
.bsg-step p{margin:0;font-size:17px;color:#4a4a4a;}

/* Tabs */
.bsg-tabs{margin:20px 0 30px;}
.bsg-tab-buttons{display:flex;flex-wrap:wrap;gap:8px;border-bottom:2px solid #e3ede0;}
.bsg-tab-btn{background:#f2f5f0;border:none;border-radius:8px 8px 0 0;padding:12px 20px;font-size:16px;font-weight:700;color:#4a4a4a;cursor:pointer;font-family:'Segoe UI',Arial,sans-serif;}
.bsg-tab-btn.active{background:#5DB92E;color:#fff;}
.bsg-tab-panel{display:none;border:1px solid #e3ede0;border-top:none;border-radius:0 0 10px 10px;padding:20px;background:#fff;}
.bsg-tab-panel.active{display:block;}
.bsg-tab-panel p{margin:0 0 10px;}
.bsg-tab-panel p:last-child{margin-bottom:0;}

/* Table */
.bsg-table-wrap{overflow-x:auto;margin:20px 0 30px;}
.bsg-table{width:100%;border-collapse:collapse;font-size:16px;}
.bsg-table th{background:#2b2b2b;color:#fff;padding:12px 14px;text-align:left;font-weight:700;}
.bsg-table td{padding:12px 14px;border-bottom:1px solid #e3ede0;}
.bsg-table tr:nth-child(even) td{background:#f7faf5;}
.bsg-table code{font-family:'Consolas','Monaco',monospace;font-size:13px;background:#f2f5f0;padding:2px 6px;border-radius:4px;}

/* Interactive tool */
.bsg-calc{border-radius:16px;overflow:hidden;border:1px solid #e3ede0;margin:20px 0 32px;}
.bsg-calc-header{background:#2b2b2b;color:#fff;padding:18px 22px;}
.bsg-calc-header h3{margin:0 0 4px;font-size:19px;color:#fff;}
.bsg-calc-header p{margin:0;font-size:14px;color:#c7d9c0;}
.bsg-calc-body{padding:22px;background:#fff;}
.bsg-calc-row{margin-bottom:14px;}
.bsg-calc-row label{font-size:15px;font-weight:700;color:#2b2b2b;display:block;margin-bottom:6px;}
.bsg-calc-row textarea,.bsg-calc-row select{width:100%;padding:10px;border-radius:8px;border:1px solid #e3ede0;font-size:14px;color:#3a3a3a;font-family:'Consolas','Monaco',monospace;background:#f7faf5;box-sizing:border-box;}
.bsg-calc-row textarea{min-height:90px;}
.bsg-calc-btn{background:#5DB92E;color:#fff;border:none;padding:10px 20px;border-radius:8px;font-weight:700;font-size:15px;cursor:pointer;font-family:'Segoe UI',Arial,sans-serif;margin-top:4px;}
.bsg-calc-output{margin-top:18px;background:#1e1e1e;border-radius:10px;padding:16px;font-family:'Consolas','Monaco',monospace;font-size:12px;color:#d4d4d4;white-space:pre-wrap;word-break:break-word;max-height:280px;overflow-y:auto;}

/* FAQ */
.bsg-faq-item{margin-bottom:14px;}
.bsg-faq-q{background:#f2f5f0;border-radius:8px 8px 0 0;padding:14px 18px;font-weight:700;color:#2b2b2b;font-size:17px;}
.bsg-faq-a{background:#fff;border:1px solid #eef1ec;border-top:none;border-radius:0 0 8px 8px;padding:16px 18px;font-size:17px;color:#4a4a4a;}

/* Related */
.bsg-related-box{background:#f7faf5;border:1px solid #e3ede0;border-radius:12px;padding:22px;margin:20px 0 30px;}
.bsg-related-box h3{margin:0 0 12px;color:#2b2b2b;}
.bsg-related-box ul{margin:0;padding-left:20px;}
.bsg-related-box li{margin-bottom:10px;}
.bsg-related-box a{font-weight:600 !important;}

/* What we learn today - terminal log style, matches sibling code articles */
.bsg-learn{margin:26px 0 20px;background:#1e1e1e;border-radius:14px;padding:20px 22px;}
.bsg-learn h3{font-size:18px;color:#fff;margin:0 0 14px;font-family:'Consolas','Monaco',monospace;}
.bsg-learn-line{display:flex;gap:10px;padding:6px 0;font-family:'Consolas','Monaco',monospace;font-size:14px;}
.bsg-learn-line .ok{color:#5DB92E;}
.bsg-learn-line p{margin:0;color:#d4d4d4;}
</style>

<div class="bsg-meta-row">
<span class="bsg-meta-pill">Technical SEO</span>
<span class="bsg-meta-pill">Sitemap Generator</span>
<span class="bsg-meta-pill">PHP</span>
<span class="bsg-meta-pill">XML</span>
</div>

<p class="bsg-lede">Most sitemap plugins are black boxes. You install one, hope it catches every URL correctly, and rarely look at what it actually outputs. Building your own PHP sitemap generator takes about thirty minutes and gives you full control over exactly which pages get included, how often they update, and what happens once you cross 50,000 URLs.</p>

<p>A sitemap generator built in PHP reads a list of URLs, either from an array, a directory scan, or a database query, then outputs valid XML following the <a href="https://www.sitemaps.org/protocol.html" target="_blank" rel="noopener">official sitemaps.org protocol</a> that search engines expect.</p>

<p>This guide walks through four working sitemap generator versions, from a basic static script to a database-driven generator that handles sitemap indexes automatically.</p>

<p>We covered why this file matters in our <a href="/what-is-xml-sitemap-ai-search-era/" target="_blank" rel="noopener">XML sitemap guide</a>. This article is the hands-on build: real, complete PHP code you can run today.</p>

<!-- OPENING ADSENSE CODE -->
<div style="margin:40px 0;">
    <div style="display:flex;align-items:center;gap:12px;margin-bottom:20px;">
        <div style="flex:1;border-top:2px dotted #bdbdbd;"></div>
        <span style="font-size:12px;color:#777;font-weight:600;letter-spacing:1px;text-transform:uppercase;">
            Advertisement
        </span>
        <div style="flex:1;border-top:2px dotted #bdbdbd;"></div>
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
    <div style="display:flex;align-items:center;gap:12px;margin-top:20px;">
        <div style="flex:1;border-top:2px dotted #bdbdbd;"></div>
        <span style="font-size:12px;color:#777;font-weight:600;letter-spacing:1px;text-transform:uppercase;">
            Advertisement
        </span>
        <div style="flex:1;border-top:2px dotted #bdbdbd;"></div>
    </div>
</div>
<!-- CLOSING ADSENSE CODE -->


<div class="bsg-stat-grid">
<div class="bsg-stat-card"><div class="bsg-stat-num">50,000</div><p>maximum URLs allowed in a single sitemap file per the sitemaps.org protocol</p></div>
<div class="bsg-stat-card"><div class="bsg-stat-num">50MB</div><p>maximum uncompressed file size per sitemap file before splitting is required</p></div>
<div class="bsg-stat-card"><div class="bsg-stat-num">4</div><p>working sitemap generator versions covered, from basic to fully automated</p></div>
</div>

<h2 id="how-this-sitemap-generator-pipeline-works">How This Sitemap Generator Pipeline Works</h2>
<div class="bsg-pipeline">
<div class="bsg-pipe-row">
<div class="bsg-pipe-step"><span class="n">STEP 1</span>Collect URLs</div>
<div class="bsg-pipe-arrow">→</div>
<div class="bsg-pipe-step"><span class="n">STEP 2</span>Build XML with DOMDocument</div>
<div class="bsg-pipe-arrow">→</div>
<div class="bsg-pipe-step"><span class="n">STEP 3</span>Split if Over 50,000</div>
<div class="bsg-pipe-arrow">→</div>
<div class="bsg-pipe-step"><span class="n">STEP 4</span>Save and Automate</div>
</div>
</div>

<h2 id="version-1-a-basic-sitemap-generator-from-an-array">Version 1: A Basic Sitemap Generator From an Array</h2>
<p>This is the simplest working sitemap generator version, using PHP's built-in <a href="https://www.php.net/manual/en/class.domdocument.php" target="_blank" rel="noopener">DOMDocument class</a> rather than string concatenation, since DOMDocument automatically escapes special characters correctly.</p>

<div class="bsg-code-box">
<pre><span class="k">&lt;?php</span>
<span class="f">header</span>(<span class="s">'Content-Type: application/xml; charset=utf-8'</span>);

<span class="v">$baseUrl</span> = <span class="s">'https://www.brandella.in'</span>;

<span class="v">$urls</span> = [
    [<span class="s">'loc'</span> =&gt; <span class="s">'/'</span>, <span class="s">'lastmod'</span> =&gt; <span class="s">'2026-07-30'</span>, <span class="s">'changefreq'</span> =&gt; <span class="s">'daily'</span>, <span class="s">'priority'</span> =&gt; <span class="s">'1.0'</span>],
    [<span class="s">'loc'</span> =&gt; <span class="s">'/blog/'</span>, <span class="s">'lastmod'</span> =&gt; <span class="s">'2026-07-29'</span>, <span class="s">'changefreq'</span> =&gt; <span class="s">'daily'</span>, <span class="s">'priority'</span> =&gt; <span class="s">'0.9'</span>],
    [<span class="s">'loc'</span> =&gt; <span class="s">'/about/'</span>, <span class="s">'lastmod'</span> =&gt; <span class="s">'2026-06-15'</span>, <span class="s">'changefreq'</span> =&gt; <span class="s">'monthly'</span>, <span class="s">'priority'</span> =&gt; <span class="s">'0.6'</span>],
];

<span class="v">$xml</span> = <span class="k">new</span> <span class="f">DOMDocument</span>(<span class="s">'1.0'</span>, <span class="s">'UTF-8'</span>);
<span class="v">$xml</span>-&gt;formatOutput = <span class="k">true</span>;

<span class="v">$urlset</span> = <span class="v">$xml</span>-&gt;<span class="f">createElement</span>(<span class="s">'urlset'</span>);
<span class="v">$urlset</span>-&gt;<span class="f">setAttribute</span>(<span class="s">'xmlns'</span>, <span class="s">'http://www.sitemaps.org/schemas/sitemap/0.9'</span>);
<span class="v">$xml</span>-&gt;<span class="f">appendChild</span>(<span class="v">$urlset</span>);

<span class="k">foreach</span> (<span class="v">$urls</span> <span class="k">as</span> <span class="v">$entry</span>) {
    <span class="v">$urlNode</span> = <span class="v">$xml</span>-&gt;<span class="f">createElement</span>(<span class="s">'url'</span>);
    <span class="v">$urlNode</span>-&gt;<span class="f">appendChild</span>(<span class="v">$xml</span>-&gt;<span class="f">createElement</span>(<span class="s">'loc'</span>, <span class="v">$baseUrl</span> . <span class="v">$entry</span>[<span class="s">'loc'</span>]));
    <span class="v">$urlNode</span>-&gt;<span class="f">appendChild</span>(<span class="v">$xml</span>-&gt;<span class="f">createElement</span>(<span class="s">'lastmod'</span>, <span class="v">$entry</span>[<span class="s">'lastmod'</span>]));
    <span class="v">$urlNode</span>-&gt;<span class="f">appendChild</span>(<span class="v">$xml</span>-&gt;<span class="f">createElement</span>(<span class="s">'changefreq'</span>, <span class="v">$entry</span>[<span class="s">'changefreq'</span>]));
    <span class="v">$urlNode</span>-&gt;<span class="f">appendChild</span>(<span class="v">$xml</span>-&gt;<span class="f">createElement</span>(<span class="s">'priority'</span>, <span class="v">$entry</span>[<span class="s">'priority'</span>]));
    <span class="v">$urlset</span>-&gt;<span class="f">appendChild</span>(<span class="v">$urlNode</span>);
}

<span class="k">echo</span> <span class="v">$xml</span>-&gt;<span class="f">saveXML</span>();</pre>
</div>
<p class="bsg-code-caption">Save as sitemap.php and visit it directly in a browser to see valid XML output</p>
<!-- OPENING ADSENSE CODE -->
<div style="margin:40px 0;">
    <div style="display:flex;align-items:center;gap:12px;margin-bottom:20px;">
        <div style="flex:1;border-top:2px dotted #bdbdbd;"></div>
        <span style="font-size:12px;color:#777;font-weight:600;letter-spacing:1px;text-transform:uppercase;">
            Advertisement
        </span>
        <div style="flex:1;border-top:2px dotted #bdbdbd;"></div>
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
    <div style="display:flex;align-items:center;gap:12px;margin-top:20px;">
        <div style="flex:1;border-top:2px dotted #bdbdbd;"></div>
        <span style="font-size:12px;color:#777;font-weight:600;letter-spacing:1px;text-transform:uppercase;">
            Advertisement
        </span>
        <div style="flex:1;border-top:2px dotted #bdbdbd;"></div>
    </div>
</div>
<!-- CLOSING ADSENSE CODE -->

<h2 id="version-2-scanning-a-directory-automatically">Version 2: Scanning a Directory Automatically</h2>
<p>For static sites, scanning a folder of HTML files with PHP's <a href="https://www.php.net/manual/en/class.recursivedirectoryiterator.php" target="_blank" rel="noopener">RecursiveDirectoryIterator</a> removes the need to maintain a URL list by hand entirely.</p>

<div class="bsg-code-box">
<pre><span class="k">&lt;?php</span>
<span class="k">function</span> <span class="f">scanDirectory</span>(<span class="v">$dir</span>, <span class="v">$extension</span> = <span class="s">'html'</span>) {
    <span class="v">$urls</span> = [];
    <span class="v">$files</span> = <span class="k">new</span> <span class="f">RecursiveIteratorIterator</span>(
        <span class="k">new</span> <span class="f">RecursiveDirectoryIterator</span>(<span class="v">$dir</span>, <span class="f">RecursiveDirectoryIterator</span>::SKIP_DOTS)
    );

    <span class="k">foreach</span> (<span class="v">$files</span> <span class="k">as</span> <span class="v">$file</span>) {
        <span class="k">if</span> (<span class="v">$file</span>-&gt;<span class="f">getExtension</span>() === <span class="v">$extension</span>) {
            <span class="v">$relativePath</span> = <span class="f">str_replace</span>(<span class="v">$dir</span>, <span class="s">''</span>, <span class="v">$file</span>-&gt;<span class="f">getPathname</span>());
            <span class="v">$urls</span>[] = [
                <span class="s">'loc'</span> =&gt; <span class="f">str_replace</span>(<span class="s">'\\'</span>, <span class="s">'/'</span>, <span class="v">$relativePath</span>),
                <span class="s">'lastmod'</span> =&gt; <span class="f">date</span>(<span class="s">'Y-m-d'</span>, <span class="v">$file</span>-&gt;<span class="f">getMTime</span>()),
                <span class="s">'changefreq'</span> =&gt; <span class="s">'weekly'</span>,
                <span class="s">'priority'</span> =&gt; <span class="s">'0.5'</span>
            ];
        }
    }
    <span class="k">return</span> <span class="v">$urls</span>;
}

<span class="v">$urls</span> = <span class="f">scanDirectory</span>(<span class="f">__DIR__</span> . <span class="s">'/public'</span>);</pre>
</div>
<p class="bsg-code-caption">Automatically finds every HTML file, using the file's own modified date for lastmod</p>

<h2 id="version-3-pulling-urls-from-a-database">Version 3: Pulling URLs From a Database</h2>
<p>For dynamic sites built on a CMS or custom database, querying published content directly through <a href="https://www.php.net/manual/en/book.pdo.php" target="_blank" rel="noopener">PHP's PDO extension</a> keeps the sitemap perfectly in sync with what actually exists.</p>

<div class="bsg-code-box">
<pre><span class="k">&lt;?php</span>
<span class="v">$pdo</span> = <span class="k">new</span> <span class="f">PDO</span>(<span class="s">'mysql:host=localhost;dbname=brandella;charset=utf8mb4'</span>, <span class="s">'db_user'</span>, <span class="s">'db_password'</span>);
<span class="v">$stmt</span> = <span class="v">$pdo</span>-&gt;<span class="f">query</span>(<span class="s">"SELECT slug, updated_at FROM posts WHERE status = 'published'"</span>);

<span class="v">$urls</span> = [];
<span class="k">while</span> (<span class="v">$row</span> = <span class="v">$stmt</span>-&gt;<span class="f">fetch</span>(<span class="f">PDO</span>::FETCH_ASSOC)) {
    <span class="v">$urls</span>[] = [
        <span class="s">'loc'</span> =&gt; <span class="s">'/'</span> . <span class="v">$row</span>[<span class="s">'slug'</span>] . <span class="s">'/'</span>,
        <span class="s">'lastmod'</span> =&gt; <span class="f">date</span>(<span class="s">'Y-m-d'</span>, <span class="f">strtotime</span>(<span class="v">$row</span>[<span class="s">'updated_at'</span>])),
        <span class="s">'changefreq'</span> =&gt; <span class="s">'weekly'</span>,
        <span class="s">'priority'</span> =&gt; <span class="s">'0.7'</span>
    ];
}</pre>
</div>
<p class="bsg-code-caption">Replace the query with whatever table structure your own CMS or app actually uses</p>
<!-- OPENING ADSENSE CODE -->
<div style="margin:40px 0;">
    <div style="display:flex;align-items:center;gap:12px;margin-bottom:20px;">
        <div style="flex:1;border-top:2px dotted #bdbdbd;"></div>
        <span style="font-size:12px;color:#777;font-weight:600;letter-spacing:1px;text-transform:uppercase;">
            Advertisement
        </span>
        <div style="flex:1;border-top:2px dotted #bdbdbd;"></div>
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
    <div style="display:flex;align-items:center;gap:12px;margin-top:20px;">
        <div style="flex:1;border-top:2px dotted #bdbdbd;"></div>
        <span style="font-size:12px;color:#777;font-weight:600;letter-spacing:1px;text-transform:uppercase;">
            Advertisement
        </span>
        <div style="flex:1;border-top:2px dotted #bdbdbd;"></div>
    </div>
</div>
<!-- CLOSING ADSENSE CODE -->

<h2 id="handling-more-than-50-000-urls">Handling More Than 50,000 URLs</h2>
<p>The sitemaps.org protocol caps a single file at 50,000 URLs. Larger sites need a sitemap index file pointing to multiple chunked sitemaps.</p>

<div class="bsg-tabs">
<div class="bsg-tab-buttons">
<button class="bsg-tab-btn active" onclick="bsgTab(event,'bsg-small')">Under 50,000 URLs</button>
<button class="bsg-tab-btn" onclick="bsgTab(event,'bsg-large')">Over 50,000 URLs</button>
</div>
<div id="bsg-small" class="bsg-tab-panel active">
<p>A single sitemap.xml file, exactly like Version 1 above, is all that's needed. No index file is required.</p>
</div>
<div id="bsg-large" class="bsg-tab-panel">
<p>Split the URL array into chunks of 50,000 using PHP's array_chunk function, generate one sitemap file per chunk, then build a sitemap index file listing each chunked file's location.</p>
</div>
</div>

<div class="bsg-code-box">
<pre><span class="k">&lt;?php</span>
<span class="v">$chunks</span> = <span class="f">array_chunk</span>(<span class="v">$allUrls</span>, <span class="s">50000</span>);

<span class="v">$indexXml</span> = <span class="k">new</span> <span class="f">DOMDocument</span>(<span class="s">'1.0'</span>, <span class="s">'UTF-8'</span>);
<span class="v">$indexXml</span>-&gt;formatOutput = <span class="k">true</span>;
<span class="v">$sitemapindex</span> = <span class="v">$indexXml</span>-&gt;<span class="f">createElement</span>(<span class="s">'sitemapindex'</span>);
<span class="v">$sitemapindex</span>-&gt;<span class="f">setAttribute</span>(<span class="s">'xmlns'</span>, <span class="s">'http://www.sitemaps.org/schemas/sitemap/0.9'</span>);
<span class="v">$indexXml</span>-&gt;<span class="f">appendChild</span>(<span class="v">$sitemapindex</span>);

<span class="k">foreach</span> (<span class="v">$chunks</span> <span class="k">as</span> <span class="v">$i</span> =&gt; <span class="v">$chunk</span>) {
    <span class="f">file_put_contents</span>(<span class="s">"sitemap-"</span> . (<span class="v">$i</span> + <span class="s">1</span>) . <span class="s">".xml"</span>, <span class="f">buildSitemapXml</span>(<span class="v">$chunk</span>));

    <span class="v">$sitemap</span> = <span class="v">$indexXml</span>-&gt;<span class="f">createElement</span>(<span class="s">'sitemap'</span>);
    <span class="v">$sitemap</span>-&gt;<span class="f">appendChild</span>(<span class="v">$indexXml</span>-&gt;<span class="f">createElement</span>(<span class="s">'loc'</span>, <span class="v">$baseUrl</span> . <span class="s">"/sitemap-"</span> . (<span class="v">$i</span> + <span class="s">1</span>) . <span class="s">".xml"</span>));
    <span class="v">$sitemap</span>-&gt;<span class="f">appendChild</span>(<span class="v">$indexXml</span>-&gt;<span class="f">createElement</span>(<span class="s">'lastmod'</span>, <span class="f">date</span>(<span class="s">'Y-m-d'</span>)));
    <span class="v">$sitemapindex</span>-&gt;<span class="f">appendChild</span>(<span class="v">$sitemap</span>);
}

<span class="f">file_put_contents</span>(<span class="s">'sitemap-index.xml'</span>, <span class="v">$indexXml</span>-&gt;<span class="f">saveXML</span>());</pre>
</div>
<p class="bsg-code-caption">Wrap the Version 1 logic in a buildSitemapXml() function, then call it once per chunk here</p>

<h2 id="automating-generation-with-cron">Automating Generation With CRON</h2>
<div class="bsg-steps">
<div class="bsg-step">
<div class="bsg-step-num">1</div>
<div>
<h3>Save the Script to Write a File, Not Just Echo</h3>
<p>Change the final line from <code>echo $xml->saveXML();</code> to <code>file_put_contents('sitemap.xml', $xml->saveXML());</code> so running the script regenerates the actual file on disk.</p>
</div>
</div>
<div class="bsg-step">
<div class="bsg-step-num">2</div>
<div>
<h3>Add a CRON Job</h3>
<p>A daily cron entry like <code>0 2 * * * php /path/to/sitemap-generator.php</code> regenerates the sitemap automatically every night at 2am.</p>
</div>
</div>
<div class="bsg-step">
<div class="bsg-step-num">3</div>
<div>
<h3>Reference It in robots.txt</h3>
<p>Add <code>Sitemap: https://www.brandella.in/sitemap.xml</code> to your robots.txt file so crawlers can discover the generated file automatically.</p>
</div>
</div>
</div>

<h2 id="live-xml-sitemap-preview-builder">Live XML Sitemap Preview Builder</h2>
<p>Paste URLs, one per line, to see the exact XML this script would generate.</p>

<div class="bsg-calc">
<div class="bsg-calc-header">
<h3>Live XML Sitemap Preview Builder</h3>
<p>Mirrors the output of the PHP script above, without needing to run PHP</p>
</div>
<div class="bsg-calc-body">

<div class="bsg-calc-row">
<label>Base URL</label>
<textarea id="bsgBase" style="min-height:auto;">https://www.example.com</textarea>
</div>
<div class="bsg-calc-row">
<label>Paths (one per line)</label>
<textarea id="bsgPaths">/
/blog/
/about/</textarea>
</div>
<div class="bsg-calc-row">
<label>Change Frequency</label>
<select id="bsgFreq">
<option value="daily">daily</option>
<option value="weekly" selected>weekly</option>
<option value="monthly">monthly</option>
</select>
</div>

<button class="bsg-calc-btn" onclick="bsgBuild()">Generate Sitemap XML</button>

<div class="bsg-calc-output" id="bsgOutput">Your generated sitemap.xml will appear here.</div>

</div>
</div>

<script>
function bsgTab(evt, id){
  var panels = document.querySelectorAll('.bsg-tab-panel');
  var btns = document.querySelectorAll('.bsg-tab-btn');
  panels.forEach(function(p){p.classList.remove('active');});
  btns.forEach(function(b){b.classList.remove('active');});
  document.getElementById(id).classList.add('active');
  evt.currentTarget.classList.add('active');
}
function bsgBuild(){
  var base = document.getElementById('bsgBase').value.trim().replace(/\/$/, '');
  var paths = document.getElementById('bsgPaths').value.split('\n').map(function(p){return p.trim();}).filter(Boolean);
  var freq = document.getElementById('bsgFreq').value;
  var today = new Date().toISOString().slice(0,10);
  var xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n';
  paths.forEach(function(p){
    var full = base + (p.startsWith('/') ? p : '/' + p);
    xml += '  <url>\n    <loc>' + full + '</loc>\n    <lastmod>' + today + '</lastmod>\n    <changefreq>' + freq + '</changefreq>\n  </url>\n';
  });
  xml += '</urlset>';
  document.getElementById('bsgOutput').innerText = xml;
}
</script>

<h2 id="validating-your-sitemap-generator-s-output">Validating Your Sitemap Generator's Output</h2>
<p>Before relying on any sitemap generator in production, confirm the output actually validates.</p>

<p>According to <a href="https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap" target="_blank" rel="noopener">Google Search Central's guide to building a sitemap</a>, submitting the file through Search Console's Sitemaps report is the most reliable way to confirm Google can parse it without errors.</p>

<p>A quick manual check works too: open the generated file directly in a browser.</p>

<p>A well-formed sitemap generator produces XML the browser renders as a structured tree, while a broken one shows a parsing error at the exact line where the invalid character or malformed tag sits.</p>

<h2 id="when-to-choose-a-custom-generator-over-a-plugin">When to Choose a Custom Generator Over a Plugin</h2>
<p>According to <a href="https://yoast.com/developer-blog/xml-sitemap-php-script/" target="_blank" rel="noopener">Yoast's developer blog on building a custom sitemap script</a>, a hand-built sitemap generator makes the most sense when a site has an unusual content structure, like large volumes of downloadable files, that generic plugins do not handle well by default.</p>

<p>For a standard WordPress blog with no unusual content types, an established plugin usually remains the more practical choice, since it also handles edge cases like taxonomy pages and media attachments without any custom code required.</p>

<h2 id="performance-considerations-for-large-sites">Performance Considerations for Large Sites</h2>
<p>A sitemap generator scanning tens of thousands of database rows or files can consume significant memory if not handled carefully.</p>

<p>According to <a href="https://github.com/msbatal/PHP-Sitemap-Generator" target="_blank" rel="noopener">an open-source PHP sitemap generator reference implementation</a>, generation time scales directly with site size, so very large catalogs benefit from batching database queries rather than loading every URL into memory at once.</p>

<p>According to <a href="https://www.php.net/manual/en/function.array-chunk.php" target="_blank" rel="noopener">PHP's own documentation for array_chunk</a>, this same batching function is what splits URLs into manageable groups for both memory efficiency and the 50,000 URL sitemap limit.</p>

<p>Running the sitemap generator as a scheduled background job, rather than triggering it from a live page request, keeps this resource usage isolated from actual visitor traffic.</p>

<h2 id="common-mistakes-when-building-a-sitemap-generator">Common Mistakes When Building a Sitemap Generator</h2>
<div class="bsg-table-wrap">
<table class="bsg-table">
<thead>
<tr><th>Mistake</th><th>Why It Matters</th></tr>
</thead>
<tbody>
<tr><td>Using string concatenation instead of DOMDocument</td><td>Special characters in URLs can break XML validity</td></tr>
<tr><td>Including noindexed or redirected URLs</td><td>Sends contradictory signals about which pages matter</td></tr>
<tr><td>Forgetting the 50,000 URL limit</td><td>Large sites need a sitemap index, not one giant file</td></tr>
<tr><td>Never automating regeneration</td><td>A stale sitemap missing new content defeats its purpose</td></tr>
<tr><td>Not referencing the file in robots.txt</td><td>Makes discovery slower for crawlers checking that file first</td></tr>
</tbody>
</table>
</div>

<h2 id="faqs-on-building-a-php-sitemap-generator">FAQs on Building a PHP Sitemap Generator</h2>

<div class="bsg-faq-item">
<div class="bsg-faq-q">Do I need a framework to build a sitemap generator in PHP?</div>
<div class="bsg-faq-a">No. Plain PHP with the built-in DOMDocument class handles this entirely, without any external library or framework dependency for a basic sitemap generator.</div>
</div>
<div class="bsg-faq-item">
<div class="bsg-faq-q">Why use DOMDocument instead of just writing the XML as a string?</div>
<div class="bsg-faq-a">DOMDocument automatically escapes special characters like ampersands and quotes correctly. Manual string concatenation can silently produce invalid XML if a URL or title contains such characters.</div>
</div>
<div class="bsg-faq-item">
<div class="bsg-faq-q">How do I handle a site with more than 50,000 pages?</div>
<div class="bsg-faq-a">Split the URL list into chunks of 50,000 using array_chunk, generate one sitemap file per chunk, and create a sitemap index file that references each chunked file's location.</div>
</div>
<div class="bsg-faq-item">
<div class="bsg-faq-q">Should the sitemap generator run on every page load?</div>
<div class="bsg-faq-a">No. Generate the file periodically through a CRON job and serve the static result, rather than regenerating it dynamically on every single request, which wastes server resources.</div>
</div>
<div class="bsg-faq-item">
<div class="bsg-faq-q">Can this same sitemap generator approach work for WordPress or other CMS platforms?</div>
<div class="bsg-faq-a">Yes, by adapting the database query in Version 3 to match your CMS's actual table structure, such as WordPress's wp_posts table, instead of a custom posts table.</div>
</div>
<div class="bsg-faq-item">
<div class="bsg-faq-q">How do I test that the generated sitemap is valid?</div>
<div class="bsg-faq-a">Open the file directly in a browser to confirm it renders as XML without errors, then submit it through Google Search Console's Sitemaps report to confirm Google can parse it correctly.</div>
</div>

<div class="bsg-related-box">
<h3>Related Articles</h3>
<ul>
<li><a href="/what-is-xml-sitemap-ai-search-era/" target="_blank" rel="noopener">What Is an XML Sitemap, and Does It Still Matter in the AI Search Era?</a></li>
<li><a href="/how-to-add-schema-markup-json-ld/" target="_blank" rel="noopener">How to Add Schema Markup to Any Website (JSON-LD Examples)</a></li>
<li><a href="/meta-robots-tags-explained/" target="_blank" rel="noopener">Meta Robots Tags Explained with HTML Code Examples</a></li>
<li><a href="/crawl-budget-explained/" target="_blank" rel="noopener">Crawl Budget Explained: Why Google Might Be Ignoring Half Your Site</a></li>
</ul>
</div>

<div class="bsg-learn">
<h3>&gt; what_we_learn_today.log</h3>
<div class="bsg-learn-line"><span class="ok">[OK]</span><p>DOMDocument builds valid XML more safely than manual string concatenation</p></div>
<div class="bsg-learn-line"><span class="ok">[OK]</span><p>A directory scanner removes the need to maintain a URL list by hand</p></div>
<div class="bsg-learn-line"><span class="ok">[OK]</span><p>Database-driven generation keeps dynamic sites perfectly in sync</p></div>
<div class="bsg-learn-line"><span class="ok">[OK]</span><p>50,000 URLs per file is the hard limit; use a sitemap index beyond that</p></div>
<div class="bsg-learn-line"><span class="ok">[OK]</span><p>CRON automation keeps the file fresh without manual regeneration</p></div>
<div class="bsg-learn-line"><span class="ok">[OK]</span><p>Always validate output before relying on it for production traffic</p></div>
</div>

</div>
