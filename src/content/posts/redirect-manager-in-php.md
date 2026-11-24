---
title: "Redirect Manager in PHP: Manage 301s at Scale in 5 Steps"
slug: "redirect-manager-in-php"
date: "2026-08-25T12:22:15"
updated: "2026-08-25T12:23:09"
author: "santajigade"
categories: ["development", "php"]
primaryCategory: "development"
description: "Build a redirect manager in PHP backed by MySQL to handle thousands of 301s, with wildcard matching, chain detection, and hit logging."
focusKeyword: "Redirect Manager in PHP"
takeaways:
  - "Apache reads .htaccess from top to bottom on every request, so thousands of redirect rules add real overhead to each page load."
  - "A database table with a unique index on source_path keeps lookups fast and stops one old URL mapping to two destinations."
  - "The redirect check should run before any template or heavy code loads, with the status code passed from the database."
  - "Exact path matches should be checked first, with regex rules used only as a fallback to protect performance."
  - "Checking for redirect chains before saving a rule and reviewing zero hit redirects quarterly keeps the table clean."
image: "/wp-content/uploads/2026/08/Redirect-Manager-in-PHP.webp"
imageAlt: "Redirect Manager in PHP"
words: 1439
views: 40
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

.bx-stats { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; margin: 22px 0 30px; }
.bx-stat-card { background: #f4faef; border: 1px solid #dff0d3; border-radius: 10px; padding: 20px 14px; text-align: center; }
.bx-stat-num { font-family: var(--bx-disp); font-weight: 800; font-size: 30px; color: var(--bx-green-deep); display: block; line-height: 1.1; }
.bx-stat-label { font-size: 14px; color: var(--bx-charcoal-soft); margin-top: 6px; display: block; }
@media (max-width: 640px) { .bx-stats { grid-template-columns: 1fr; } }

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

.bx-table-wrap { overflow-x: auto; margin: 20px 0 30px; border-radius: 10px; }
table.bx-table { width: 100%; border-collapse: collapse; font-size: 17px; min-width: 620px; }
table.bx-table thead tr { background: var(--bx-charcoal) !important; }
table.bx-table thead th { color: #fff !important; font-family: var(--bx-disp); font-weight: 700; text-align: left; padding: 13px 14px; font-size: 17px; }
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

.bx-faq { margin: 20px 0 30px; }
.bx-faq-item { border-bottom: 1px solid #e3e3e3; }
.bx-faq-q {
  width: 100%; text-align: left; background: none; border: none; cursor: pointer;
  font-family: var(--bx-disp); font-weight: 700; font-size: 17px; color: var(--bx-charcoal);
  padding: 18px 34px 18px 4px; position: relative;
}
.bx-faq-q::after {
  content: "+"; position: absolute; right: 4px; top: 50%; transform: translateY(-50%);
  color: var(--bx-green-deep); font-size: 22px; font-weight: 400; transition: transform .25s ease;
}
.bx-faq-item.open .bx-faq-q::after { transform: translateY(-50%) rotate(45deg); }
.bx-faq-a { max-height: 0; overflow: hidden; transition: max-height .3s ease; }
.bx-faq-a p { padding: 0 4px 18px; margin: 0; font-size: 17px; color: var(--bx-charcoal-soft); }

.bx-related { background: #eef8e6; border-radius: 12px; padding: 26px 26px 10px; margin: 34px 0; }
.bx-related h3 { font-family: var(--bx-disp); font-size: 19px; color: var(--bx-charcoal); margin: 0 0 16px; }
.bx-related ul { list-style: none; margin: 0; padding: 0; display: grid; grid-template-columns: 1fr 1fr; gap: 10px 20px; }
.bx-related li { font-size: 17px; padding-bottom: 16px; border-bottom: 1px dashed #cfe8bd; }
@media (max-width: 640px) { .bx-related ul { grid-template-columns: 1fr; } }

.bx-learn { margin: 40px 0 10px; }
.bx-learn h2 { font-family: var(--bx-disp); font-size: 24px; color: var(--bx-charcoal); margin-bottom: 20px; }
.bx-learn-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
.bx-learn-card {
  border: 1px solid #e3efdc; border-radius: 12px; padding: 20px; background: #fff;
  display: flex; gap: 14px; align-items: flex-start;
}
.bx-learn-num {
  flex-shrink: 0; width: 34px; height: 34px; border-radius: 50%; background: var(--bx-charcoal);
  color: var(--bx-green); font-family: var(--bx-disp); font-weight: 800; font-size: 15px;
  display: flex; align-items: center; justify-content: center;
}
.bx-learn-card h4 { margin: 0 0 6px; font-family: var(--bx-disp); font-size: 16px; color: var(--bx-charcoal); }
.bx-learn-card p { margin: 0; font-size: 17px; color: var(--bx-charcoal-soft); }
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
    <span class="bx-pill">Development</span>
    <span class="bx-pill">PHP</span>
    <span class="bx-pill">301 Redirects</span>
    <span class="bx-pill">MySQL</span>
  </div>

  <p class="bx-lede">A site migration that generates three thousand old URLs does not belong in a growing .htaccess file, since every added rule slows down every single request on the server. A redirect manager in PHP moves that lookup into a database where it belongs.</p>

  <div class="bx-section-head">
    <span class="bx-num">01</span>
    <h2 class="bx-h2" id="why-a-redirect-manager-in-php-beats-a-giant-htaccess-file">Why a Redirect Manager in PHP Beats a Giant htaccess File</h2>
    <div class="bx-rule"></div>
  </div>

  <p>Apache reads an .htaccess file from top to bottom on every request, checking each rule in order until one matches.</p>

  <p>A file with a few dozen redirect rules barely registers. A file with several thousand rules, built up after two or three site migrations, adds real overhead to every page load.</p>

  <p>It also becomes almost impossible to search, edit safely, or hand off to someone else on the team without breaking something.</p>

  <p>A small PHP script backed by an indexed database table replaces all of that with a single fast lookup, no matter how many redirects the table holds.</p>


  <div class="bx-section-head">
    <span class="bx-num">02</span>
    <h2 class="bx-h2" id="designing-the-redirect-database-table">Designing the Redirect Database Table</h2>
    <div class="bx-rule"></div>
  </div>

  <p>A single table covers most sites, as long as the source path column is indexed for fast lookups.</p>

  <div class="bx-code-wrap">
    <div class="bx-code-title">redirects.sql</div>
    <pre><code><span class="tok-kw">CREATE TABLE</span> redirects (
    id <span class="tok-kw">INT</span> <span class="tok-kw">AUTO_INCREMENT PRIMARY KEY</span>,
    source_path <span class="tok-kw">VARCHAR</span>(<span class="tok-val">500</span>) <span class="tok-kw">NOT NULL</span>,
    destination_url <span class="tok-kw">VARCHAR</span>(<span class="tok-val">500</span>) <span class="tok-kw">NOT NULL</span>,
    status_code <span class="tok-kw">SMALLINT</span> <span class="tok-kw">DEFAULT</span> <span class="tok-val">301</span>,
    is_regex <span class="tok-kw">BOOLEAN</span> <span class="tok-kw">DEFAULT</span> <span class="tok-val">0</span>,
    hit_count <span class="tok-kw">INT</span> <span class="tok-kw">DEFAULT</span> <span class="tok-val">0</span>,
    created_at <span class="tok-kw">TIMESTAMP</span> <span class="tok-kw">DEFAULT CURRENT_TIMESTAMP</span>,
    <span class="tok-kw">UNIQUE KEY</span> idx_source (source_path)
);</code></pre>
  </div>

  <p>The unique key on <code>source_path</code> does double duty. It keeps the lookup fast and stops the same old URL from ever being mapped to two different destinations by mistake. <a href="https://dev.mysql.com/doc/refman/8.4/en/mysql-indexes.html" target="_blank" rel="noopener">MySQL's own indexing guide</a> explains why this matters more as a table grows past a few thousand rows.</p>

  <div class="bx-section-head">
    <span class="bx-num">03</span>
    <h2 class="bx-h2" id="setting-up-pdo-and-the-redirect-lookup-function">Setting Up PDO and the Redirect Lookup Function</h2>
    <div class="bx-rule"></div>
  </div>

  <p><a href="https://www.php.net/manual/en/book.pdo.php" target="_blank" rel="noopener">PDO</a> with prepared statements keeps the lookup safe from injection, even though the only input here is the requested path itself.</p>

  <div class="bx-code-wrap">
    <div class="bx-code-title">redirect_lookup.php</div>
    <pre><code><span class="tok-val">$pdo</span> = <span class="tok-kw">new</span> PDO(
    <span class="tok-str">'mysql:host=localhost;dbname=brandella;charset=utf8mb4'</span>,
    getenv(<span class="tok-str">'DB_USER'</span>), getenv(<span class="tok-str">'DB_PASS'</span>)
);
<span class="tok-val">$pdo</span>->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

<span class="tok-kw">function</span> <span class="tok-fn">find_redirect</span>(PDO <span class="tok-val">$pdo</span>, <span class="tok-val">$path</span>) {
    <span class="tok-val">$stmt</span> = <span class="tok-val">$pdo</span>->prepare(
        <span class="tok-str">'SELECT * FROM redirects WHERE source_path = ? AND is_regex = 0 LIMIT 1'</span>
    );
    <span class="tok-val">$stmt</span>->execute([<span class="tok-val">$path</span>]);
    <span class="tok-kw">return</span> <span class="tok-val">$stmt</span>->fetch(PDO::FETCH_ASSOC);
}</code></pre>
  </div>

  <p>This function only checks exact matches for now. The next two sections add wildcard and regex support on top of it.</p>

  <div class="bx-section-head">
    <span class="bx-num">04</span>
    <h2 class="bx-h2" id="handling-the-request-before-anything-else-loads">Handling the Request Before Anything Else Loads</h2>
    <div class="bx-rule"></div>
  </div>

  <p>The redirect check needs to run as early as possible in the request lifecycle, before the page template or any heavy application code loads.</p>

  <div class="bx-code-wrap">
    <div class="bx-code-title">index.php</div>
    <pre><code><span class="tok-val">$path</span> = parse_url(<span class="tok-val">$_SERVER</span>[<span class="tok-str">'REQUEST_URI'</span>], PHP_URL_PATH);
<span class="tok-val">$redirect</span> = find_redirect(<span class="tok-val">$pdo</span>, <span class="tok-val">$path</span>);

<span class="tok-kw">if</span> (<span class="tok-val">$redirect</span>) {
    log_redirect_hit(<span class="tok-val">$pdo</span>, <span class="tok-val">$redirect</span>[<span class="tok-str">'id'</span>]);
    header(<span class="tok-str">'Location: '</span> . <span class="tok-val">$redirect</span>[<span class="tok-str">'destination_url'</span>], <span class="tok-val">true</span>, <span class="tok-val">$redirect</span>[<span class="tok-str">'status_code'</span>]);
    <span class="tok-kw">exit</span>;
}</code></pre>
  </div>

  <p>Passing the status code from the database into <code>header()</code> means the same function handles both a <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/301" target="_blank" rel="noopener">301 permanent move</a> and a <a href="https://httpwg.org/specs/rfc9110.html#status.302" target="_blank" rel="noopener">302 temporary redirect</a> without any extra branching.</p>

  <div class="bx-section-head">
    <span class="bx-num">05</span>
    <h2 class="bx-h2" id="supporting-wildcard-and-regex-redirects">Supporting Wildcard and Regex Redirects</h2>
    <div class="bx-rule"></div>
  </div>

  <p>Not every redirect maps one old URL to one new URL. A whole folder of old product pages often needs to collapse into a single category page.</p>

  <div class="bx-code-wrap">
    <div class="bx-code-title">regex_lookup.php</div>
    <pre><code><span class="tok-kw">function</span> <span class="tok-fn">find_regex_redirect</span>(PDO <span class="tok-val">$pdo</span>, <span class="tok-val">$path</span>) {
    <span class="tok-val">$stmt</span> = <span class="tok-val">$pdo</span>->query(
        <span class="tok-str">'SELECT * FROM redirects WHERE is_regex = 1'</span>
    );
    <span class="tok-kw">foreach</span> (<span class="tok-val">$stmt</span> <span class="tok-kw">as</span> <span class="tok-val">$rule</span>) {
        <span class="tok-kw">if</span> (preg_match(<span class="tok-val">$rule</span>[<span class="tok-str">'source_path'</span>], <span class="tok-val">$path</span>, <span class="tok-val">$matches</span>)) {
            <span class="tok-kw">return</span> [
                <span class="tok-str">'id'</span> => <span class="tok-val">$rule</span>[<span class="tok-str">'id'</span>],
                <span class="tok-str">'destination_url'</span> => preg_replace(<span class="tok-val">$rule</span>[<span class="tok-str">'source_path'</span>], <span class="tok-val">$rule</span>[<span class="tok-str">'destination_url'</span>], <span class="tok-val">$path</span>),
                <span class="tok-str">'status_code'</span> => <span class="tok-val">$rule</span>[<span class="tok-str">'status_code'</span>]
            ];
        }
    }
    <span class="tok-kw">return</span> <span class="tok-val">null</span>;
}</code></pre>
  </div>

  <p>Regex rules are checked only after the exact match table lookup fails, since scanning every regex row on every single request would erase the speed advantage the exact match index provides.</p>

  <div class="bx-table-wrap">
    <table class="bx-table">
      <thead><tr><th>Matching Strategy</th><th>Speed</th><th>Best For</th></tr></thead>
      <tbody>
        <tr><td>Exact path lookup</td><td>Fastest, uses the index directly</td><td>Individual page moves</td></tr>
        <tr><td>Wildcard prefix match</td><td>Fast, small candidate set</td><td>Whole folders moving together</td></tr>
        <tr><td>Regex pattern match</td><td>Slower, checked as a fallback</td><td>Complex URL structure changes</td></tr>
      </tbody>
    </table>
  </div>

  <div class="bx-section-head">
    <span class="bx-num">06</span>
    <h2 class="bx-h2" id="detecting-and-preventing-redirect-chains">Detecting and Preventing Redirect Chains</h2>
    <div class="bx-rule"></div>
  </div>

  <p>A chain forms when one redirect points at a URL that is itself another redirect, and <a href="https://developers.google.com/search/docs/crawling-indexing/301-redirects" target="_blank" rel="noopener">Google's own redirect guidance</a> flags long chains as a real crawl efficiency problem.</p>

  <div class="bx-code-wrap">
    <div class="bx-code-title">chain_check.php</div>
    <pre><code><span class="tok-kw">function</span> <span class="tok-fn">creates_chain</span>(PDO <span class="tok-val">$pdo</span>, <span class="tok-val">$destination</span>) {
    <span class="tok-val">$path</span> = parse_url(<span class="tok-val">$destination</span>, PHP_URL_PATH);
    <span class="tok-val">$stmt</span> = <span class="tok-val">$pdo</span>->prepare(<span class="tok-str">'SELECT id FROM redirects WHERE source_path = ?'</span>);
    <span class="tok-val">$stmt</span>->execute([<span class="tok-val">$path</span>]);
    <span class="tok-kw">return</span> <span class="tok-val">$stmt</span>->fetch() !== <span class="tok-val">false</span>;
}</code></pre>
  </div>

  <p>Running this check before saving a new redirect catches the chain at creation time, which is far easier than untangling one after it has been live for months.</p>

  <div class="bx-section-head">
    <span class="bx-num">07</span>
    <h2 class="bx-h2" id="logging-hits-and-finding-unused-redirects">Logging Hits and Finding Unused Redirects</h2>
    <div class="bx-rule"></div>
  </div>

  <p>Not every redirect stays useful forever. Some stop receiving any traffic once old backlinks and bookmarks age out, a pattern <a href="https://www.searchenginejournal.com/redirects-seo/" target="_blank" rel="noopener">Search Engine Journal's redirect guide</a> covers in more depth from the SEO side of things.</p>

  <div class="bx-code-wrap">
    <div class="bx-code-title">log_redirect_hit.php</div>
    <pre><code><span class="tok-kw">function</span> <span class="tok-fn">log_redirect_hit</span>(PDO <span class="tok-val">$pdo</span>, <span class="tok-val">$id</span>) {
    <span class="tok-val">$stmt</span> = <span class="tok-val">$pdo</span>->prepare(
        <span class="tok-str">'UPDATE redirects SET hit_count = hit_count + 1 WHERE id = ?'</span>
    );
    <span class="tok-val">$stmt</span>->execute([<span class="tok-val">$id</span>]);
}</code></pre>
  </div>

  <p>A quarterly query for rows where <code>hit_count</code> stayed at zero surfaces redirects nobody is actually using anymore, safe candidates for cleanup. This kind of ongoing maintenance is exactly what a redirect manager in PHP makes practical at a scale .htaccess never could.</p>

  <ul class="bx-checklist">
    <li><b>Index the source_path column:</b> without it, the lookup falls back to a full table scan on every single request.</li>
    <li><b>Check exact matches before regex:</b> keeping the fast path first protects performance as the table grows into the thousands.</li>
    <li><b>Block chains at creation time:</b> a check before saving a new redirect is far cheaper than an audit months later.</li>
    <li><b>Review zero hit redirects quarterly:</b> a smaller, cleaner table stays easier to reason about than one that only grows.</li>
    <li><b>Cache the lookup where traffic is heavy:</b> a high traffic site can front the database check with a fast in memory cache layer like <a href="https://redis.io/docs/latest/" target="_blank" rel="noopener">Redis</a>.</li>
  </ul>


  <div class="bx-section-head">
    <span class="bx-num">08</span>
    <h2 class="bx-h2" id="watch-fetching-data-from-mysql-in-php">Watch: Fetching Data From MySQL in PHP</h2>
    <div class="bx-rule"></div>
  </div>

  <p>Traversy Media, referenced earlier in this series for a working PHP contact form, also covers the database fetching pattern that a redirect lookup builds directly on.</p>

  <div style="position:relative; padding-bottom:56.25%; height:0; overflow:hidden; border-radius:12px; margin:18px 0 8px;">
    <iframe src="https://www.youtube.com/embed/IYlDJ2K3MGk" title="PHP Front To Back, Fetching Data With MySQLi" style="position:absolute; top:0; left:0; width:100%; height:100%; border:0;" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen loading="lazy"></iframe>
  </div>
  <p style="font-size:14px; color:var(--bx-charcoal-soft); margin-top:6px;">Video credit: Traversy Media.</p>

  <p>Swapping the query shown in the video for the prepared statement lookup in this guide is the entire difference between a demo and a production ready redirect manager in PHP.</p>

  <svg width="100%" height="220" viewBox="0 0 800 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Diagram of a redirect manager in PHP moving an incoming request through exact match, wildcard, and regex lookups before either a 301 redirect or a normal page load" style="margin:26px 0;">
    <rect width="800" height="220" fill="#f4faef" rx="12"/>
    <g font-family="Open Sans, sans-serif" font-size="13" fill="#2b2b2b">
      <rect x="15" y="85" width="120" height="55" rx="8" fill="#ffffff" stroke="#5DB92E" stroke-width="2"/>
      <text x="75" y="117" text-anchor="middle" font-weight="700">Incoming Path</text>

      <line x1="135" y1="112" x2="175" y2="112" stroke="#4a9e24" stroke-width="2" marker-end="url(#arrow)"/>

      <rect x="175" y="85" width="130" height="55" rx="8" fill="#ffffff" stroke="#5DB92E" stroke-width="2"/>
      <text x="240" y="117" text-anchor="middle" font-weight="700">Exact Match</text>

      <line x1="305" y1="112" x2="345" y2="112" stroke="#4a9e24" stroke-width="2" marker-end="url(#arrow)"/>

      <rect x="345" y="85" width="130" height="55" rx="8" fill="#ffffff" stroke="#5DB92E" stroke-width="2"/>
      <text x="410" y="117" text-anchor="middle" font-weight="700">Regex Lookup</text>

      <line x1="475" y1="112" x2="515" y2="112" stroke="#4a9e24" stroke-width="2" marker-end="url(#arrow)"/>

      <rect x="515" y="85" width="120" height="55" rx="8" fill="#2b2b2b" stroke="#5DB92E" stroke-width="2"/>
      <text x="575" y="117" text-anchor="middle" font-weight="700" fill="#5DB92E">301 Redirect</text>

      <line x1="475" y1="140" x2="475" y2="170" stroke="#4a9e24" stroke-width="2" marker-end="url(#arrow)"/>
      <rect x="395" y="170" width="160" height="45" rx="8" fill="#ffffff" stroke="#5DB92E" stroke-width="2"/>
      <text x="475" y="197" text-anchor="middle" font-weight="700">Normal Page Load</text>
    </g>
    <defs>
      <marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto" markerUnits="strokeWidth">
        <path d="M0,0 L0,6 L9,3 z" fill="#4a9e24"/>
      </marker>
    </defs>
  </svg>

    <div class="bx-faq">
    <h3 class="bx-h3">Frequently Asked Questions</h3>

    <div class="bx-faq-item">
      <button type="button" class="bx-faq-q">How many redirects can a database backed system realistically handle?</button>
      <div class="bx-faq-a"><p>Well into the hundreds of thousands, since an indexed exact match lookup stays fast regardless of table size, unlike a growing .htaccess file that Apache reads line by line. Watching crawl stats in <a href="https://search.google.com/search-console/about" target="_blank" rel="noopener">Search Console</a> is a good way to confirm the migration went smoothly.</p></div>
    </div>
    <div class="bx-faq-item">
      <button type="button" class="bx-faq-q">Why build a redirect manager in PHP instead of just using .htaccess?</button>
      <div class="bx-faq-a"><p>Performance at scale, easier editing through an admin interface, built in chain detection, and hit logging that shows which redirects are still actually needed.</p></div>
    </div>
    <div class="bx-faq-item">
      <button type="button" class="bx-faq-q">Should every redirect use a 301 status code?</button>
      <div class="bx-faq-a"><p>Only permanent moves should. A temporary change, like a seasonal page, is a better fit for a 302, which the status_code column in this design already supports.</p></div>
    </div>
    <div class="bx-faq-item">
      <button type="button" class="bx-faq-q">What happens if two rules could both match the same path?</button>
      <div class="bx-faq-a"><p>The exact match table always takes priority in this design, and regex rules are only checked once the exact match lookup comes back empty.</p></div>
    </div>
    <div class="bx-faq-item">
      <button type="button" class="bx-faq-q">How often should redirect chains be audited?</button>
      <div class="bx-faq-a"><p>Checking at creation time, as shown in this guide, prevents most chains before they exist, so a full audit is really only needed after a large migration.</p></div>
    </div>
  </div>

  <div class="bx-learn">
    <h2 id="what-we-learn-today">What We Learn Today</h2>
    <div class="bx-learn-grid">
      <div class="bx-learn-card"><span class="bx-learn-num">1</span><div><h4>htaccess does not scale forever</h4><p>Thousands of rules read line by line add real overhead to every request.</p></div></div>
      <div class="bx-learn-card"><span class="bx-learn-num">2</span><div><h4>An index makes the lookup fast</h4><p>A unique key on source_path keeps performance flat as the table grows.</p></div></div>
      <div class="bx-learn-card"><span class="bx-learn-num">3</span><div><h4>Exact match should run first</h4><p>Checking regex rules only as a fallback protects the fast path.</p></div></div>
      <div class="bx-learn-card"><span class="bx-learn-num">4</span><div><h4>Chains are easiest to stop early</h4><p>A check at creation time beats untangling a chain months later.</p></div></div>
      <div class="bx-learn-card"><span class="bx-learn-num">5</span><div><h4>Hit counts reveal dead weight</h4><p>Zero hit redirects are safe, low risk candidates for cleanup.</p></div></div>
      <div class="bx-learn-card"><span class="bx-learn-num">6</span><div><h4>Status codes should match intent</h4><p>301 for permanent moves, 302 for anything meant to be temporary.</p></div></div>
    </div>
  </div>


  <div class="bx-cta">
    <h3>Ready to Take Redirects Out of htaccess?</h3>
    <p>Pair a redirect manager in PHP with a wider toolkit to keep every site migration clean and every old URL accounted for.</p>
    <div class="bx-cta-btns">
      <a href="/screaming-frog-seo-spider-beginners-guide/" target="_blank" rel="noopener">Read the Screaming Frog Guide</a>
      <a href="/best-keyword-research-tools-compared/" target="_blank" rel="noopener" class="bx-cta-outline">Compare Keyword Tools</a>
    </div>
  </div>

</div>

<script>
(function() {
  var items = document.querySelectorAll('.bx-faq-item');
  items.forEach(function(item) {
    var q = item.querySelector('.bx-faq-q');
    var a = item.querySelector('.bx-faq-a');
    q.addEventListener('click', function() {
      var isOpen = item.classList.contains('open');
      items.forEach(function(other) {
        other.classList.remove('open');
        other.querySelector('.bx-faq-a').style.maxHeight = null;
      });
      if (!isOpen) {
        item.classList.add('open');
        a.style.maxHeight = a.scrollHeight + 'px';
      }
    });
  });
})();
</script>
