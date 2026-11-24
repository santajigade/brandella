---
title: "Large Scale XML Sitemaps in PHP: Streaming, Sharding & Index Files"
slug: "large-scale-xml-sitemaps-php-index-files"
date: "2026-08-24T06:46:56"
updated: "2026-08-24T06:47:22"
author: "santajigade"
categories: ["php"]
primaryCategory: "php"
description: "Large scale XML sitemaps in PHP: XMLWriter streaming, unbuffered PDO generators, automatic 50k-URL sharding, and sitemap index file generation."
focusKeyword: "Large Scale XML Sitemaps"
takeaways:
  - "The Sitemaps protocol limits each file to 50,000 URLs and 50MB uncompressed, and gzip compression does not raise that 50MB cap."
  - "PHP's XMLWriter streams elements straight to a file, keeping memory flat, unlike building a DOMDocument for the whole sitemap in memory."
  - "PDO's MySQL driver buffers full result sets by default, so disable buffered queries and wrap the cursor in a generator that yields one row at a time."
  - "The generator should shard automatically into a new file every 50,000 URLs, with one sitemap index file submitted to Search Console and robots.txt."
  - "Only indexable, published pages belong in the source query, because listing noindexed or unpublished pages wastes crawl budget."
image: "/wp-content/uploads/2026/08/Large-Scale-XML-Sitemap.webp"
imageAlt: "Large Scale XML Sitemaps"
words: 1599
views: 56
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
.bmc-flow .bx-tip{position:relative;overflow:hidden;border-radius:14px;margin:20px 0 30px;padding:20px 22px 20px 62px;background:linear-gradient(135deg,#fff8e6 0%,#fff2d1 100%);border:1px solid #f4d98a;}
.bmc-flow .bx-tip::before{content:"💡";position:absolute;left:16px;top:18px;font-size:24px;line-height:1;}
.bmc-flow .bx-tip .lbl{font-family:var(--bx-disp);text-transform:uppercase;letter-spacing:1px;font-size:16px;color:#a5750b;font-weight:800;display:block;margin-bottom:6px;}
.bmc-flow .bx-tip p{margin:0;font-size:17px;color:#6b4f0e;}
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
.bmc-flow .bx-code pre{margin:0;font-family:'Courier New',monospace;font-size:14px;line-height:1.7;white-space:pre-wrap;word-break:break-word;color:#e6e6e6;}
.bmc-flow .bx-code-label{font-family:var(--bx-disp);color:var(--bx-steel-2);text-transform:uppercase;letter-spacing:1.2px;font-size:13px;margin-bottom:10px;font-weight:600;}
.bmc-flow .tok-com{color:#7a8a7a;font-style:italic;}
.bmc-flow .tok-sel{color:#8fd97f;}
.bmc-flow .tok-prop{color:#6fc6e8;}
.bmc-flow .tok-val{color:#f4b45a;}
.bmc-flow .tok-str{color:#e8c96a;}
.bmc-flow .tok-kw{color:#c992e8;}
.bmc-flow .tok-fn{color:#79b8f2;}
.bmc-flow .tok-num{color:#f4915a;}
.bmc-flow .tok-var{color:#f18aa8;}
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
<span class="bx-meta-pill">XML Sitemaps</span>
<span class="bx-meta-pill">PHP</span>
<span class="bx-meta-pill">2026</span>
</div>

<p class="bx-lede">An XML sitemap for a large site in PHP hits a wall that small-site tutorials never mention: the 50,000 URL and 50MB-uncompressed limits defined in the Sitemaps protocol. Once a site crosses that line, building one flat sitemap file isn't just wrong, it can produce a file search engines silently reject or truncate.</p>

<h2 id="large-scale-xml-sitemap-php-basics"><span class="bx-num">01</span>Large Scale XML Sitemaps in PHP: Why the Approach Changes</h2>
<div class="bx-rule"></div>
<p><a href="https://www.sitemaps.org/protocol.html" target="_blank" rel="noopener">The official Sitemaps protocol</a> is explicit: each sitemap file must contain no more than 50,000 URLs and must be no larger than 50MB uncompressed. Cross either limit, and you need multiple sitemap files referenced by a single sitemap index file instead of one giant document.</p>

<p>The second wall is memory, not the URL protocol. <a href="https://www.jasminedirectory.com/blog/xml-sitemaps-advanced-strategies-for-large-directories/" target="_blank" rel="noopener">Jasmine Directory's guide</a> is direct about the fix: use XMLWriter for streaming generation and PDO with unbuffered queries, and avoid loading entire result sets into arrays. Stream everything, don't build the whole document in memory first.</p>

<div class="bx-specs">
<div class="bx-spec"><div class="v">50,000</div><div class="k">maximum URLs allowed per individual sitemap file under the protocol</div></div>
<div class="bx-spec"><div class="v">50MB</div><div class="k">maximum uncompressed file size per sitemap, gzip doesn't change this cap</div></div>
<div class="bx-spec"><div class="v">50,000</div><div class="k">maximum sitemap files a single index file may reference</div></div>
</div>
<h2 id="xmlwriter-streaming"><span class="bx-num">02</span>Streaming a Sitemap File With XMLWriter</h2>
<div class="bx-rule"></div>
<p>Instead of building a DOM object in memory and serializing it at the end, PHP's XMLWriter class writes elements incrementally, directly to a file or output stream, keeping memory usage flat regardless of how many URLs you write.</p>

<div class="bx-code">
<div class="bx-code-label">Streaming a Single Sitemap File (Memory-Flat)</div>
<pre><span class="tok-kw">function</span> <span class="tok-fn">writeSitemapFile</span>(<span class="tok-var">$filePath</span>, <span class="tok-var">$urlGenerator</span>) {
  <span class="tok-var">$writer</span> = <span class="tok-kw">new</span> <span class="tok-fn">XMLWriter</span>();
  <span class="tok-var">$writer</span>-&gt;<span class="tok-fn">openUri</span>(<span class="tok-var">$filePath</span>);
  <span class="tok-var">$writer</span>-&gt;<span class="tok-fn">startDocument</span>(<span class="tok-str">'1.0'</span>, <span class="tok-str">'UTF-8'</span>);
  <span class="tok-var">$writer</span>-&gt;<span class="tok-fn">startElement</span>(<span class="tok-str">'urlset'</span>);
  <span class="tok-var">$writer</span>-&gt;<span class="tok-fn">writeAttribute</span>(<span class="tok-str">'xmlns'</span>, <span class="tok-str">'http://www.sitemaps.org/schemas/sitemap/0.9'</span>);

  <span class="tok-com">// $urlGenerator is a PHP generator, one row is held in memory at a time</span>
  <span class="tok-kw">foreach</span> (<span class="tok-var">$urlGenerator</span> <span class="tok-kw">as</span> <span class="tok-var">$row</span>) {
    <span class="tok-var">$writer</span>-&gt;<span class="tok-fn">startElement</span>(<span class="tok-str">'url'</span>);
    <span class="tok-var">$writer</span>-&gt;<span class="tok-fn">writeElement</span>(<span class="tok-str">'loc'</span>, <span class="tok-var">$row</span>[<span class="tok-str">'url'</span>]);
    <span class="tok-var">$writer</span>-&gt;<span class="tok-fn">writeElement</span>(<span class="tok-str">'lastmod'</span>, <span class="tok-var">$row</span>[<span class="tok-str">'updated_at'</span>]);
    <span class="tok-var">$writer</span>-&gt;<span class="tok-fn">endElement</span>(); <span class="tok-com">// </url></span>
  }

  <span class="tok-var">$writer</span>-&gt;<span class="tok-fn">endElement</span>(); <span class="tok-com">// </urlset></span>
  <span class="tok-var">$writer</span>-&gt;<span class="tok-fn">endDocument</span>();
  <span class="tok-var">$writer</span>-&gt;<span class="tok-fn">flush</span>();
}</pre>
</div>

<h2 id="unbuffered-pdo"><span class="bx-num">03</span>Feeding It From an Unbuffered PDO Query</h2>
<div class="bx-rule"></div>
<p>The writer above expects a generator, not an array. PDO's MySQL driver buffers full result sets in memory by default, defeating the point of streaming. Disabling buffered queries and wrapping the cursor in a PHP generator keeps only one row in memory at any time, regardless of table size.</p>

<div class="bx-code">
<div class="bx-code-label">Unbuffered PDO Query as a Generator</div>
<pre><span class="tok-var">$pdo</span>-&gt;<span class="tok-fn">setAttribute</span>(PDO::MYSQL_ATTR_USE_BUFFERED_QUERY, <span class="tok-val">false</span>);

<span class="tok-kw">function</span> <span class="tok-fn">fetchIndexableUrls</span>(<span class="tok-var">$pdo</span>) {
  <span class="tok-var">$stmt</span> = <span class="tok-var">$pdo</span>-&gt;<span class="tok-fn">query</span>(
    <span class="tok-str">'SELECT url, updated_at FROM pages WHERE noindex = 0 ORDER BY id'</span>
  );

  <span class="tok-com">// yield hands over one row and pauses, this is the memory-saving part</span>
  <span class="tok-kw">while</span> (<span class="tok-var">$row</span> = <span class="tok-var">$stmt</span>-&gt;<span class="tok-fn">fetch</span>(PDO::FETCH_ASSOC)) {
    <span class="tok-kw">yield</span> <span class="tok-var">$row</span>;
  }
}

<span class="tok-fn">writeSitemapFile</span>(<span class="tok-str">'sitemaps/sitemap-1.xml'</span>, <span class="tok-fn">fetchIndexableUrls</span>(<span class="tok-var">$pdo</span>));</pre>
</div>

<div class="bx-tip">
<span class="lbl">Quick Tip</span>
<p>Only indexable, published pages belong in the query. Unpublish a page and forget to exclude it here, and you're actively asking search engines to crawl and index content you no longer want in results, which wastes crawl budget on exactly the pages that matter least.</p>
</div>
<h2 id="sharding"><span class="bx-num">04</span>Sharding Into Multiple Files at the 50,000 Mark</h2>
<div class="bx-rule"></div>
<p>Once total URLs exceed 50,000, the generator needs to close the current file and open a new one automatically, rather than one script writing a single oversized file that violates the protocol.</p>

<div class="bx-code">
<div class="bx-code-label">Automatic Sharding at the URL Limit</div>
<pre><span class="tok-kw">function</span> <span class="tok-fn">generateShardedSitemaps</span>(<span class="tok-var">$urlGenerator</span>, <span class="tok-var">$outputDir</span>, <span class="tok-var">$limitPerFile</span> = <span class="tok-num">50000</span>) {
  <span class="tok-var">$fileIndex</span> = <span class="tok-num">1</span>;
  <span class="tok-var">$count</span> = <span class="tok-num">0</span>;
  <span class="tok-var">$writer</span> = <span class="tok-val">null</span>;
  <span class="tok-var">$generatedFiles</span> = [];

  <span class="tok-kw">foreach</span> (<span class="tok-var">$urlGenerator</span> <span class="tok-kw">as</span> <span class="tok-var">$row</span>) {
    <span class="tok-kw">if</span> (<span class="tok-var">$count</span> % <span class="tok-var">$limitPerFile</span> === <span class="tok-num">0</span>) {
      <span class="tok-kw">if</span> (<span class="tok-var">$writer</span>) {
        <span class="tok-var">$writer</span>-&gt;<span class="tok-fn">endElement</span>();
        <span class="tok-var">$writer</span>-&gt;<span class="tok-fn">endDocument</span>();
        <span class="tok-var">$writer</span>-&gt;<span class="tok-fn">flush</span>();
      }
      <span class="tok-var">$fileName</span> = <span class="tok-str">"sitemap-{$fileIndex}.xml"</span>;
      <span class="tok-var">$generatedFiles</span>[] = <span class="tok-var">$fileName</span>;
      <span class="tok-var">$writer</span> = <span class="tok-kw">new</span> <span class="tok-fn">XMLWriter</span>();
      <span class="tok-var">$writer</span>-&gt;<span class="tok-fn">openUri</span>(<span class="tok-var">$outputDir</span> . <span class="tok-str">'/'</span> . <span class="tok-var">$fileName</span>);
      <span class="tok-var">$writer</span>-&gt;<span class="tok-fn">startDocument</span>(<span class="tok-str">'1.0'</span>, <span class="tok-str">'UTF-8'</span>);
      <span class="tok-var">$writer</span>-&gt;<span class="tok-fn">startElement</span>(<span class="tok-str">'urlset'</span>);
      <span class="tok-var">$writer</span>-&gt;<span class="tok-fn">writeAttribute</span>(<span class="tok-str">'xmlns'</span>, <span class="tok-str">'http://www.sitemaps.org/schemas/sitemap/0.9'</span>);
      <span class="tok-var">$fileIndex</span>++;
    }

    <span class="tok-var">$writer</span>-&gt;<span class="tok-fn">startElement</span>(<span class="tok-str">'url'</span>);
    <span class="tok-var">$writer</span>-&gt;<span class="tok-fn">writeElement</span>(<span class="tok-str">'loc'</span>, <span class="tok-var">$row</span>[<span class="tok-str">'url'</span>]);
    <span class="tok-var">$writer</span>-&gt;<span class="tok-fn">writeElement</span>(<span class="tok-str">'lastmod'</span>, <span class="tok-var">$row</span>[<span class="tok-str">'updated_at'</span>]);
    <span class="tok-var">$writer</span>-&gt;<span class="tok-fn">endElement</span>();

    <span class="tok-var">$count</span>++;
  }

  <span class="tok-kw">if</span> (<span class="tok-var">$writer</span>) {
    <span class="tok-var">$writer</span>-&gt;<span class="tok-fn">endElement</span>();
    <span class="tok-var">$writer</span>-&gt;<span class="tok-fn">endDocument</span>();
    <span class="tok-var">$writer</span>-&gt;<span class="tok-fn">flush</span>();
  }

  <span class="tok-kw">return</span> <span class="tok-var">$generatedFiles</span>;
}</pre>
</div>

<h2 id="sitemap-index"><span class="bx-num">05</span>Building the Sitemap Index File</h2>
<div class="bx-rule"></div>
<p>Once URLs are split across multiple files, a single sitemap index file lists each one. This is the only file you submit to Search Console and reference in robots.txt, search engines follow it to discover the rest.</p>

<div class="bx-code">
<div class="bx-code-label">Generating the Sitemap Index File</div>
<pre><span class="tok-kw">function</span> <span class="tok-fn">writeSitemapIndex</span>(<span class="tok-var">$generatedFiles</span>, <span class="tok-var">$baseUrl</span>, <span class="tok-var">$outputPath</span>) {
  <span class="tok-var">$writer</span> = <span class="tok-kw">new</span> <span class="tok-fn">XMLWriter</span>();
  <span class="tok-var">$writer</span>-&gt;<span class="tok-fn">openUri</span>(<span class="tok-var">$outputPath</span> . <span class="tok-str">'/sitemap-index.xml'</span>);
  <span class="tok-var">$writer</span>-&gt;<span class="tok-fn">startDocument</span>(<span class="tok-str">'1.0'</span>, <span class="tok-str">'UTF-8'</span>);
  <span class="tok-var">$writer</span>-&gt;<span class="tok-fn">startElement</span>(<span class="tok-str">'sitemapindex'</span>);
  <span class="tok-var">$writer</span>-&gt;<span class="tok-fn">writeAttribute</span>(<span class="tok-str">'xmlns'</span>, <span class="tok-str">'http://www.sitemaps.org/schemas/sitemap/0.9'</span>);

  <span class="tok-kw">foreach</span> (<span class="tok-var">$generatedFiles</span> <span class="tok-kw">as</span> <span class="tok-var">$fileName</span>) {
    <span class="tok-var">$writer</span>-&gt;<span class="tok-fn">startElement</span>(<span class="tok-str">'sitemap'</span>);
    <span class="tok-var">$writer</span>-&gt;<span class="tok-fn">writeElement</span>(<span class="tok-str">'loc'</span>, <span class="tok-var">$baseUrl</span> . <span class="tok-str">'/'</span> . <span class="tok-var">$fileName</span>);
    <span class="tok-var">$writer</span>-&gt;<span class="tok-fn">writeElement</span>(<span class="tok-str">'lastmod'</span>, <span class="tok-fn">date</span>(<span class="tok-str">'c'</span>));
    <span class="tok-var">$writer</span>-&gt;<span class="tok-fn">endElement</span>();
  }

  <span class="tok-var">$writer</span>-&gt;<span class="tok-fn">endElement</span>();
  <span class="tok-var">$writer</span>-&gt;<span class="tok-fn">endDocument</span>();
  <span class="tok-var">$writer</span>-&gt;<span class="tok-fn">flush</span>();
}</pre>
</div>

<div class="bx-dyk">
<span class="lbl">🔎 Did you know?</span>
<p>A documented real-world case handled 60 million URLs across 20 languages in PHP and Laravel. The team's original approach kept every processed item in memory until hitting the 50,000 limit, which meant items sat in RAM the whole time. Switching to write-and-stream in small batches, opening and closing the sitemap file as needed, was what actually made the process viable at that scale.</p>
</div>
<h2 id="gzip"><span class="bx-num">06</span>Gzip Compression Without Blowing Up Memory</h2>
<div class="bx-rule"></div>
<p><a href="https://lettercounter.org/blog/xml-sitemap-url-limits/" target="_blank" rel="noopener">Letter Counter's guide</a> notes gzip compression can reduce actual transfer size by 70-90% without affecting how the 50MB limit is calculated, since the cap applies to the uncompressed content. For large sitemaps, compress the already-written file rather than trying to gzip inline during the write loop.</p>

<div class="bx-code">
<div class="bx-code-label">Gzip Compress an Already-Written Sitemap File</div>
<pre><span class="tok-kw">function</span> <span class="tok-fn">gzipSitemapFile</span>(<span class="tok-var">$filePath</span>) {
  <span class="tok-var">$gzPath</span> = <span class="tok-var">$filePath</span> . <span class="tok-str">'.gz'</span>;
  <span class="tok-var">$source</span> = <span class="tok-fn">fopen</span>(<span class="tok-var">$filePath</span>, <span class="tok-str">'rb'</span>);
  <span class="tok-var">$dest</span> = <span class="tok-fn">gzopen</span>(<span class="tok-var">$gzPath</span>, <span class="tok-str">'wb9'</span>);

  <span class="tok-kw">while</span> (!<span class="tok-fn">feof</span>(<span class="tok-var">$source</span>)) {
    <span class="tok-fn">gzwrite</span>(<span class="tok-var">$dest</span>, <span class="tok-fn">fread</span>(<span class="tok-var">$source</span>, <span class="tok-num">1048576</span>)); <span class="tok-com">// 1MB chunks</span>
  }

  <span class="tok-fn">fclose</span>(<span class="tok-var">$source</span>);
  <span class="tok-fn">gzclose</span>(<span class="tok-var">$dest</span>);
}</pre>
</div>

<h2 id="table"><span class="bx-num">07</span>Buffered vs Streaming Approach Compared</h2>
<div class="bx-rule"></div>
<p>A quick reference for why the streaming approach matters as URL counts grow.</p>

<div class="bx-table-wrap">
<table class="bx-table">
<thead>
<tr><th>Factor</th><th>Buffered (fetchAll + DOMDocument)</th><th>Streaming (Generator + XMLWriter)</th></tr>
</thead>
<tbody>
<tr><td>Memory usage at 1M URLs</td><td>Scales with total URL count</td><td>Stays flat regardless of total count</td></tr>
<tr><td>Risk of memory limit crash</td><td>High on large sites</td><td>Effectively eliminated</td></tr>
<tr><td>Code complexity</td><td>Simpler to write initially</td><td>Slightly more setup, generators + sharding</td></tr>
<tr><td>Suitable site size</td><td>Small sites, under a few thousand URLs</td><td>Any size, including tens of millions</td></tr>
</tbody>
</table>
</div>

<h2 id="checklist"><span class="bx-num">08</span>Implementation Checklist</h2>
<div class="bx-rule"></div>
<p>A short list to confirm before deploying a large-scale sitemap generator.</p>

<div class="bx-checklist">
<div class="bx-check-item"><div class="bx-check-icon"></div><p><strong>Use XMLWriter, not DOMDocument</strong>, for anything beyond a few thousand URLs, to keep memory flat.</p></div>
<div class="bx-check-item"><div class="bx-check-icon"></div><p><strong>Disable PDO query buffering</strong>, wrap the cursor in a generator so only one row loads at a time.</p></div>
<div class="bx-check-item"><div class="bx-check-icon"></div><p><strong>Shard automatically at 50,000 URLs</strong>, don't rely on manual file splitting.</p></div>
<div class="bx-check-item"><div class="bx-check-icon"></div><p><strong>Generate a sitemap index file</strong>, this is the single file you submit and reference in robots.txt.</p></div>
<div class="bx-check-item"><div class="bx-check-icon"></div><p><strong>Exclude noindexed and unpublished content</strong> from the source query, don't waste crawl budget on it.</p></div>
</div>

<h2 id="faq"><span class="bx-num">09</span>Common Questions</h2>
<div class="bx-rule"></div>
<div class="bx-faq" id="bxFaq">
<button class="bx-q">What happens if my sitemap exceeds 50,000 URLs?<span class="ic">+</span></button>
<div class="bx-a"><p>It violates the Sitemaps protocol and may be rejected or truncated by search engines. Split URLs across multiple files, each under the 50,000 limit, and reference them all from a single sitemap index file.</p></div>
<button class="bx-q">Does gzip compression let me exceed the 50MB sitemap limit?<span class="ic">+</span></button>
<div class="bx-a"><p>No. The 50MB cap applies to the uncompressed file size, regardless of how small the compressed version ends up being. Gzip saves bandwidth, it doesn't raise the limit.</p></div>
<button class="bx-q">Why does my sitemap generator run out of memory on a large site?<span class="ic">+</span></button>
<div class="bx-a"><p>Usually because the entire URL set is loaded into an array or DOMDocument before writing. Switch to a PHP generator feeding an XMLWriter stream to keep memory usage flat regardless of total URL count.</p></div>
<button class="bx-q">Should I submit individual sitemap files or the index file to Google?<span class="ic">+</span></button>
<div class="bx-a"><p>Submit the sitemap index file. Search engines follow it to discover and crawl each individual sitemap file automatically, so you only need to reference one URL in Search Console and robots.txt.</p></div>
<button class="bx-q">Can PDO's default settings handle streaming a million-row query?<span class="ic">+</span></button>
<div class="bx-a"><p>Not by default. MySQL's PDO driver buffers full result sets in memory. Disable this with PDO::MYSQL_ATTR_USE_BUFFERED_QUERY set to false, and wrap the fetch loop in a generator using yield.</p></div>
</div>

<div class="bx-related-box">
<h3>Related Articles</h3>
<ul>
<li><a href="/build-xml-sitemap-generator-php/" target="_blank" rel="noopener">How to Build an XML Sitemap Generator in PHP</a></li>
<li><a href="/html-sitemap-vs-xml-sitemap-difference/" target="_blank" rel="noopener">HTML Sitemap vs XML Sitemap: The Difference</a></li>
<li><a href="/dynamic-meta-tags-php/" target="_blank" rel="noopener">How to Create Dynamic Meta Tags in PHP</a></li>
</ul>
</div>

<div class="bx-learn">
<h3>What We Learn Today</h3>
<div class="bx-learn-grid">
<div class="bx-learn-card"><p>The protocol caps every sitemap at 50,000 URLs and 50MB uncompressed</p></div>
<div class="bx-learn-card"><p>XMLWriter streams output instead of building a DOM in memory</p></div>
<div class="bx-learn-card"><p>Unbuffered PDO queries plus generators keep memory flat at any scale</p></div>
<div class="bx-learn-card"><p>Sharding must happen automatically once the URL count crosses the limit</p></div>
<div class="bx-learn-card"><p>A sitemap index file is the single file you submit and reference</p></div>
<div class="bx-learn-card"><p>Gzip cuts transfer size but never changes the uncompressed size limit</p></div>
</div>
</div>

<section class="bx-cta">
<h2 id="build-a-complete-php-technical-seo-toolkit">Build a Complete PHP Technical SEO Toolkit</h2>
<p>Large-scale sitemap generation pairs naturally with dynamic meta tags and sitemap type comparisons. Explore both guides next.</p>
<div class="bx-actions">
<a class="bx-btn primary" href="/dynamic-meta-tags-php/" target="_blank" rel="noopener">Dynamic Meta Tags in PHP</a>
<a class="bx-btn ghost" href="/html-sitemap-vs-xml-sitemap-difference/" target="_blank" rel="noopener">HTML Sitemap vs XML Sitemap</a>
</div>
</section>

</div>
<script>
(function(){var root=document.currentScript.parentNode.querySelector('.bmc-flow')||document;var qs=root.querySelectorAll('#bxFaq .bx-q');qs.forEach(function(q){q.addEventListener('click',function(){var a=q.nextElementSibling,open=q.classList.contains('on');qs.forEach(function(x){x.classList.remove('on');x.nextElementSibling.classList.remove('on');});if(!open){q.classList.add('on');a.classList.add('on');}});});})();
</script>
