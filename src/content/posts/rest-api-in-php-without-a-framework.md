---
title: "REST API in PHP Without a Framework: Build It in 6 Steps"
slug: "rest-api-in-php-without-a-framework"
date: "2026-08-26T09:33:36"
updated: "2026-08-26T09:34:40"
author: "santajigade"
categories: ["development", "php"]
primaryCategory: "development"
description: "Build a rest api in php without a framework using a router, PDO models, bearer token auth, and consistent JSON error handling."
focusKeyword: "rest api in php"
takeaways:
  - "A small REST API in plain PHP needs only a front controller, a simple router, a database connection and clear HTTP verb rules."
  - "An .htaccess rewrite sends every request that is not a real file to index.php, which acts as the single entry point."
  - "Each method should return a consistent status code, such as 201 for a successful POST and 204 for a successful DELETE."
  - "Bearer tokens should be compared with hash_equals(), which runs in constant time and avoids leaking timing information."
  - "Error responses should return a random request ID instead of the raw exception message, keeping internal details out of the response."
image: "/wp-content/uploads/2026/08/rest-api-in-php.webp"
imageAlt: "rest api in php"
words: 1722
views: 56
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
    <span class="bx-pill">REST API</span>
    <span class="bx-pill">JSON</span>
  </div>

  <p class="bx-lede">Installing a full framework to serve a handful of JSON endpoints is a lot of weight for a small job. A REST API in PHP without a framework needs only a router, a database connection, and a clear idea of what each HTTP verb should do.</p>

  <div class="bx-section-head">
    <span class="bx-num">01</span>
    <h2 class="bx-h2" id="why-build-a-rest-api-in-php-without-a-framework">Why Build a REST API in PHP Without a Framework</h2>
    <div class="bx-rule"></div>
  </div>

  <p>A framework earns its weight on a large application with dozens of routes, middleware, and moving parts. Roy Fielding's original <a href="https://ics.uci.edu/~fielding/pubs/dissertation/top.htm" target="_blank" rel="noopener">REST dissertation</a> never mentions a framework at all, since the architecture itself is just a set of constraints over plain HTTP.</p>

  <p>A small internal tool, a mobile app backend with six endpoints, or a proof of concept rarely needs any of that structure.</p>

  <p>Plain PHP with a thin routing layer starts in minutes and stays easy to read months later, since nothing hides behind a framework's own conventions.</p>

  <p>Everything below is production usable code, not a toy example, built around the same HTTP rules a framework would enforce anyway.</p>


  <div class="bx-section-head">
    <span class="bx-num">02</span>
    <h2 class="bx-h2" id="setting-up-a-front-controller">Setting Up a Front Controller</h2>
    <div class="bx-rule"></div>
  </div>

  <p>Every request routes through a single PHP file, which keeps the routing logic in one place instead of scattered across separate files per endpoint.</p>

  <div class="bx-code-wrap">
    <div class="bx-code-title">.htaccess</div>
    <pre><code><span class="tok-sel">RewriteEngine</span> On
<span class="tok-sel">RewriteCond</span> %{REQUEST_FILENAME} !<span class="tok-prop">-f</span>
<span class="tok-sel">RewriteRule</span> ^(.*)$ index.php [QSA,L]</code></pre>
  </div>

  <p>Every request that does not point at a real file gets forwarded to <code>index.php</code>, which becomes the single entry point the router below reads from. <a href="https://httpd.apache.org/docs/current/mod/mod_rewrite.html" target="_blank" rel="noopener">mod_rewrite</a> handles this on Apache, and Nginx uses an equivalent <code>try_files</code> directive in its own server block.</p>

  <div class="bx-section-head">
    <span class="bx-num">03</span>
    <h2 class="bx-h2" id="building-a-simple-router-class">Building a Simple Router Class</h2>
    <div class="bx-rule"></div>
  </div>

  <p>A router just needs to match a method and a path pattern against the current request, then call the matching handler.</p>

  <div class="bx-code-wrap">
    <div class="bx-code-title">Router.php</div>
    <pre><code><span class="tok-kw">final class</span> Router {
    <span class="tok-kw">private array</span> <span class="tok-val">$routes</span> = [];

    <span class="tok-kw">public function</span> <span class="tok-fn">add</span>(<span class="tok-kw">string</span> <span class="tok-val">$method</span>, <span class="tok-kw">string</span> <span class="tok-val">$pattern</span>, <span class="tok-kw">callable</span> <span class="tok-val">$handler</span>): <span class="tok-kw">void</span> {
        <span class="tok-val">$this</span>->routes[] = [<span class="tok-str">'method'</span> => <span class="tok-val">$method</span>, <span class="tok-str">'pattern'</span> => <span class="tok-val">$pattern</span>, <span class="tok-str">'handler'</span> => <span class="tok-val">$handler</span>];
    }

    <span class="tok-kw">public function</span> <span class="tok-fn">dispatch</span>(<span class="tok-kw">string</span> <span class="tok-val">$method</span>, <span class="tok-kw">string</span> <span class="tok-val">$path</span>): <span class="tok-kw">void</span> {
        <span class="tok-kw">foreach</span> (<span class="tok-val">$this</span>->routes <span class="tok-kw">as</span> <span class="tok-val">$route</span>) {
            <span class="tok-kw">if</span> (<span class="tok-val">$route</span>[<span class="tok-str">'method'</span>] !== <span class="tok-val">$method</span>) {
                <span class="tok-kw">continue</span>;
            }
            <span class="tok-val">$regex</span> = <span class="tok-str">'#^'</span> . preg_replace(<span class="tok-str">'/\{(\w+)\}/'</span>, <span class="tok-str">'(?P&lt;$1&gt;[^/]+)'</span>, <span class="tok-val">$route</span>[<span class="tok-str">'pattern'</span>]) . <span class="tok-str">'$#'</span>;
            <span class="tok-kw">if</span> (preg_match(<span class="tok-val">$regex</span>, <span class="tok-val">$path</span>, <span class="tok-val">$matches</span>)) {
                <span class="tok-val">$route</span>[<span class="tok-str">'handler'</span>](array_filter(<span class="tok-val">$matches</span>, <span class="tok-str">'is_string'</span>, ARRAY_FILTER_USE_KEY));
                <span class="tok-kw">return</span>;
            }
        }
        http_response_code(<span class="tok-val">404</span>);
        <span class="tok-fn">echo</span> json_encode([<span class="tok-str">'error'</span> => <span class="tok-str">'Route not found'</span>]);
    }
}</code></pre>
  </div>

  <p>Turning <code>{id}</code> style placeholders into a named regex group lets a single pattern like <code>/posts/{id}</code> match <code>/posts/42</code> and hand back <code>id</code> already extracted.</p>

  <div class="bx-section-head">
    <span class="bx-num">04</span>
    <h2 class="bx-h2" id="returning-proper-json-responses-and-status-codes">Returning Proper JSON Responses and Status Codes</h2>
    <div class="bx-rule"></div>
  </div>

  <p>A REST API's status code carries real meaning, and a client integrating against it depends on that meaning being consistent. The full list of codes and what each one is meant to signal comes from <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Status" target="_blank" rel="noopener">MDN's HTTP status reference</a>, which is worth keeping open while building any API.</p>

  <div class="bx-code-wrap">
    <div class="bx-code-title">respond.php</div>
    <pre><code><span class="tok-kw">function</span> <span class="tok-fn">json_response</span>(<span class="tok-kw">array</span> <span class="tok-val">$data</span>, <span class="tok-kw">int</span> <span class="tok-val">$status</span> = <span class="tok-val">200</span>): <span class="tok-kw">void</span> {
    http_response_code(<span class="tok-val">$status</span>);
    header(<span class="tok-str">'Content-Type: application/json'</span>);
    <span class="tok-fn">echo</span> json_encode(<span class="tok-val">$data</span>, JSON_UNESCAPED_SLASHES);
    <span class="tok-kw">exit</span>;
}</code></pre>
  </div>

  <div class="bx-table-wrap">
    <table class="bx-table">
      <thead><tr><th>HTTP Method</th><th>Action</th><th>Typical Status Code</th></tr></thead>
      <tbody>
        <tr><td>GET</td><td>Read one or many resources</td><td>200 on success, 404 if missing</td></tr>
        <tr><td>POST</td><td>Create a new resource</td><td>201 on success</td></tr>
        <tr><td>PUT</td><td>Replace an existing resource</td><td>200 on success</td></tr>
        <tr><td>DELETE</td><td>Remove a resource</td><td>204 on success</td></tr>
      </tbody>
    </table>
  </div>

  <div class="bx-section-head">
    <span class="bx-num">05</span>
    <h2 class="bx-h2" id="handling-get-post-put-and-delete-for-a-resource">Handling GET, POST, PUT, and DELETE for a Resource</h2>
    <div class="bx-rule"></div>
  </div>

  <p>Registering routes for a single resource follows the same shape regardless of how many resources the API eventually grows to cover, and every response still follows the same <a href="https://www.json.org/json-en.html" target="_blank" rel="noopener">JSON</a> structure a client already expects.</p>

  <div class="bx-code-wrap">
    <div class="bx-code-title">index.php</div>
    <pre><code><span class="tok-val">$router</span> = <span class="tok-kw">new</span> Router();

<span class="tok-val">$router</span>->add(<span class="tok-str">'GET'</span>, <span class="tok-str">'/posts'</span>, <span class="tok-kw">fn</span>() => json_response(get_all_posts(<span class="tok-val">$pdo</span>)));
<span class="tok-val">$router</span>->add(<span class="tok-str">'GET'</span>, <span class="tok-str">'/posts/{id}'</span>, <span class="tok-kw">fn</span>(<span class="tok-val">$p</span>) => json_response(get_post(<span class="tok-val">$pdo</span>, (<span class="tok-kw">int</span>) <span class="tok-val">$p</span>[<span class="tok-str">'id'</span>])));
<span class="tok-val">$router</span>->add(<span class="tok-str">'POST'</span>, <span class="tok-str">'/posts'</span>, <span class="tok-kw">fn</span>() => json_response(create_post(<span class="tok-val">$pdo</span>, get_json_body()), <span class="tok-val">201</span>));
<span class="tok-val">$router</span>->add(<span class="tok-str">'PUT'</span>, <span class="tok-str">'/posts/{id}'</span>, <span class="tok-kw">fn</span>(<span class="tok-val">$p</span>) => json_response(update_post(<span class="tok-val">$pdo</span>, (<span class="tok-kw">int</span>) <span class="tok-val">$p</span>[<span class="tok-str">'id'</span>], get_json_body())));
<span class="tok-val">$router</span>->add(<span class="tok-str">'DELETE'</span>, <span class="tok-str">'/posts/{id}'</span>, <span class="tok-kw">fn</span>(<span class="tok-val">$p</span>) => json_response(delete_post(<span class="tok-val">$pdo</span>, (<span class="tok-kw">int</span>) <span class="tok-val">$p</span>[<span class="tok-str">'id'</span>]), <span class="tok-val">204</span>));

<span class="tok-val">$router</span>->dispatch(<span class="tok-val">$_SERVER</span>[<span class="tok-str">'REQUEST_METHOD'</span>], parse_url(<span class="tok-val">$_SERVER</span>[<span class="tok-str">'REQUEST_URI'</span>], PHP_URL_PATH));</code></pre>
  </div>

  <p>Five lines wire up a complete resource, and adding a second resource means five more lines rather than a new controller class and configuration file.</p>

  <div class="bx-section-head">
    <span class="bx-num">06</span>
    <h2 class="bx-h2" id="connecting-routes-to-a-pdo-backed-model">Connecting Routes to a PDO Backed Model</h2>
    <div class="bx-rule"></div>
  </div>

  <p>The handler functions referenced above stay small, since each one wraps a single <a href="https://www.php.net/manual/en/book.pdo.php" target="_blank" rel="noopener">PDO</a> prepared statement.</p>

  <div class="bx-code-wrap">
    <div class="bx-code-title">posts_model.php</div>
    <pre><code><span class="tok-kw">function</span> <span class="tok-fn">get_post</span>(PDO <span class="tok-val">$pdo</span>, <span class="tok-kw">int</span> <span class="tok-val">$id</span>): <span class="tok-kw">array</span> {
    <span class="tok-val">$stmt</span> = <span class="tok-val">$pdo</span>->prepare(<span class="tok-str">'SELECT id, title, body FROM posts WHERE id = ?'</span>);
    <span class="tok-val">$stmt</span>->execute([<span class="tok-val">$id</span>]);
    <span class="tok-val">$post</span> = <span class="tok-val">$stmt</span>->fetch(PDO::FETCH_ASSOC);

    <span class="tok-kw">if</span> (!<span class="tok-val">$post</span>) {
        json_response([<span class="tok-str">'error'</span> => <span class="tok-str">'Post not found'</span>], <span class="tok-val">404</span>);
    }
    <span class="tok-kw">return</span> <span class="tok-val">$post</span>;
}</code></pre>
  </div>

  <p>Calling <code>json_response</code> directly from inside the model and letting it <code>exit</code> keeps the missing resource case short, without an extra layer of exceptions just to bubble a 404 upward.</p>

  <div class="bx-section-head">
    <span class="bx-num">07</span>
    <h2 class="bx-h2" id="authenticating-requests-with-a-bearer-token">Authenticating Requests With a Bearer Token</h2>
    <div class="bx-rule"></div>
  </div>

  <p>A write endpoint left open to anyone is a real risk the moment the API is reachable from outside a local network. The <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Authentication" target="_blank" rel="noopener">Bearer scheme</a> is a standard HTTP authentication pattern, not something specific to this guide.</p>

  <div class="bx-code-wrap">
    <div class="bx-code-title">auth_middleware.php</div>
    <pre><code><span class="tok-kw">function</span> <span class="tok-fn">require_bearer_token</span>(): <span class="tok-kw">void</span> {
    <span class="tok-val">$header</span> = <span class="tok-val">$_SERVER</span>[<span class="tok-str">'HTTP_AUTHORIZATION'</span>] ?? <span class="tok-str">''</span>;

    <span class="tok-kw">if</span> (!preg_match(<span class="tok-str">'/^Bearer\s+(.+)$/'</span>, <span class="tok-val">$header</span>, <span class="tok-val">$matches</span>)) {
        json_response([<span class="tok-str">'error'</span> => <span class="tok-str">'Missing or malformed token'</span>], <span class="tok-val">401</span>);
    }
    <span class="tok-kw">if</span> (!hash_equals(getenv(<span class="tok-str">'API_TOKEN'</span>), <span class="tok-val">$matches</span>[<span class="tok-val">1</span>])) {
        json_response([<span class="tok-str">'error'</span> => <span class="tok-str">'Invalid token'</span>], <span class="tok-val">403</span>);
    }
}</code></pre>
  </div>

  <p><a href="https://www.php.net/manual/en/function.hash-equals.php" target="_blank" rel="noopener"><code>hash_equals()</code></a> compares strings in constant time, which matters here since a plain <code>===</code> comparison can leak timing information about how much of the token matched. <a href="https://www.rfc-editor.org/rfc/rfc6750" target="_blank" rel="noopener">RFC 6750</a> defines the Bearer token scheme this pattern follows.</p>

  <div class="bx-section-head">
    <span class="bx-num">08</span>
    <h2 class="bx-h2" id="handling-errors-with-a-consistent-json-format">Handling Errors With a Consistent JSON Format</h2>
    <div class="bx-rule"></div>
  </div>

  <p>A client integrating against the API should be able to parse every error the same way, regardless of which endpoint produced it.</p>

  <div class="bx-code-wrap">
    <div class="bx-code-title">error_handler.php</div>
    <pre><code>set_exception_handler(<span class="tok-kw">function</span> (Throwable <span class="tok-val">$e</span>) {
    json_response([
        <span class="tok-str">'error'</span> => <span class="tok-str">'Server error'</span>,
        <span class="tok-str">'request_id'</span> => bin2hex(random_bytes(<span class="tok-val">8</span>))
    ], <span class="tok-val">500</span>);
});</code></pre>
  </div>

  <p>Returning a random <code>request_id</code> instead of the raw exception message keeps internal details out of the response while still giving support a value to search server logs for.</p>

  <ul class="bx-checklist">
    <li><b>Validate the request body before touching the database:</b> the JSON decoding and validation rules from earlier in this series apply directly here.</li>
    <li><b>Return the right status code, not just 200:</b> a client relies on the code as much as the body to know what happened.</li>
    <li><b>Never echo a raw exception message:</b> it can leak file paths, query fragments, or other internal details to a caller.</li>
    <li><b>Rate limit write endpoints:</b> the same IP based limiter used for a contact form works just as well in front of a POST route.</li>
    <li><b>Check requests against the <a href="https://owasp.org/API-Security/editions/2023/en/0x00-header/" target="_blank" rel="noopener">OWASP API Security Top 10</a>:</b> broken authentication and excessive data exposure are the two most common issues in a hand rolled API.</li>
    <li><b>Version the API in the URL path:</b> a prefix like /v1/posts leaves room to change the response shape later without breaking existing clients.</li>
  </ul>


  <div class="bx-section-head">
    <span class="bx-num">09</span>
    <h2 class="bx-h2" id="testing-the-api-with-curl">Testing the API With curl</h2>
    <div class="bx-rule"></div>
  </div>

  <p>A quick command line request using <a href="https://curl.se/docs/manual.html" target="_blank" rel="noopener">curl</a> confirms the whole chain works before any client application gets involved.</p>

  <div class="bx-code-wrap">
    <div class="bx-code-title">terminal</div>
    <pre><code><span class="tok-cm"># create a post</span>
curl <span class="tok-prop">-X</span> POST https://api.example.com/posts \
  <span class="tok-prop">-H</span> <span class="tok-str">"Authorization: Bearer your_token_here"</span> \
  <span class="tok-prop">-H</span> <span class="tok-str">"Content-Type: application/json"</span> \
  <span class="tok-prop">-d</span> <span class="tok-str">'{"title":"Hello","body":"First post"}'</span></code></pre>
  </div>

  <p>A successful call returns status 201 along with the newly created row, confirming the router, the model, and the authentication check all worked together correctly.</p>

  <div class="bx-section-head">
    <span class="bx-num">10</span>
    <h2 class="bx-h2" id="watch-building-a-php-rest-api-from-scratch">Watch: Building a PHP REST API From Scratch</h2>
    <div class="bx-rule"></div>
  </div>

  <p>Dave Hollingworth builds a working REST API using plain, object oriented PHP and MySQL, which follows a very similar shape to the router and model pattern in this guide.</p>

  <div style="position:relative; padding-bottom:56.25%; height:0; overflow:hidden; border-radius:12px; margin:18px 0 8px;">
    <iframe src="https://www.youtube.com/embed/X51KOJKrofU" title="Create a PHP REST API, Write a RESTful API from Scratch" style="position:absolute; top:0; left:0; width:100%; height:100%; border:0;" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen loading="lazy"></iframe>
  </div>
  <p style="font-size:14px; color:var(--bx-charcoal-soft); margin-top:6px;">Video credit: Dave Hollingworth.</p>

  <p>Swapping the video's approach for the named route parameters and bearer token check in this guide is a natural next step once the base pattern feels familiar.</p>

  <svg width="100%" height="220" viewBox="0 0 800 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Diagram of a rest api in php without a framework moving a request through the router, authentication check, and model before returning a JSON response" style="margin:26px 0;">
    <rect width="800" height="220" fill="#f4faef" rx="12"/>
    <g font-family="Open Sans, sans-serif" font-size="13" fill="#2b2b2b">
      <rect x="15" y="85" width="115" height="55" rx="8" fill="#ffffff" stroke="#5DB92E" stroke-width="2"/>
      <text x="72" y="117" text-anchor="middle" font-weight="700">HTTP Request</text>

      <line x1="130" y1="112" x2="170" y2="112" stroke="#4a9e24" stroke-width="2" marker-end="url(#arrow)"/>

      <rect x="170" y="85" width="115" height="55" rx="8" fill="#ffffff" stroke="#5DB92E" stroke-width="2"/>
      <text x="227" y="117" text-anchor="middle" font-weight="700">Router</text>

      <line x1="285" y1="112" x2="325" y2="112" stroke="#4a9e24" stroke-width="2" marker-end="url(#arrow)"/>

      <rect x="325" y="85" width="130" height="55" rx="8" fill="#ffffff" stroke="#5DB92E" stroke-width="2"/>
      <text x="390" y="117" text-anchor="middle" font-weight="700">Bearer Auth</text>

      <line x1="455" y1="112" x2="495" y2="112" stroke="#4a9e24" stroke-width="2" marker-end="url(#arrow)"/>

      <rect x="495" y="85" width="115" height="55" rx="8" fill="#ffffff" stroke="#5DB92E" stroke-width="2"/>
      <text x="552" y="117" text-anchor="middle" font-weight="700">PDO Model</text>

      <line x1="610" y1="112" x2="650" y2="112" stroke="#4a9e24" stroke-width="2" marker-end="url(#arrow)"/>

      <rect x="650" y="85" width="135" height="55" rx="8" fill="#2b2b2b" stroke="#5DB92E" stroke-width="2"/>
      <text x="717" y="117" text-anchor="middle" font-weight="700" fill="#5DB92E">JSON Response</text>
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
      <button type="button" class="bx-faq-q">Is it actually a good idea to skip a framework for a real project?</button>
      <div class="bx-faq-a"><p>For a small, focused API it often is. Once the number of resources and business rules grows large, the structure a framework provides usually becomes worth the added weight.</p></div>
    </div>
    <div class="bx-faq-item">
      <button type="button" class="bx-faq-q">Why build a REST API in PHP without a framework instead of using one from the start?</button>
      <div class="bx-faq-a"><p>Faster setup, fewer dependencies to keep updated, and a codebase where every line of routing and request handling is visible instead of hidden behind configuration.</p></div>
    </div>
    <div class="bx-faq-item">
      <button type="button" class="bx-faq-q">Is a bearer token enough security for a production API?</button>
      <div class="bx-faq-a"><p>It is a reasonable baseline for a server to server integration, though a public facing API serving many users usually needs a fuller OAuth style flow eventually.</p></div>
    </div>
    <div class="bx-faq-item">
      <button type="button" class="bx-faq-q">Should every response include a status code even when nothing went wrong?</button>
      <div class="bx-faq-a"><p>Yes. Always setting an explicit status code, even 200, avoids relying on PHP's default, which can vary depending on what already ran earlier in the request.</p></div>
    </div>
    <div class="bx-faq-item">
      <button type="button" class="bx-faq-q">How do I add a second resource to this same API?</button>
      <div class="bx-faq-a"><p>Add a new model file with its own functions and register a matching set of routes, following the exact same five line pattern used for posts in this guide.</p></div>
    </div>
  </div>

  <div class="bx-learn">
    <h2 id="what-we-learn-today">What We Learn Today</h2>
    <div class="bx-learn-grid">
      <div class="bx-learn-card"><span class="bx-learn-num">1</span><div><h4>A front controller centralizes routing</h4><p>Every request passes through one file instead of many scattered endpoints.</p></div></div>
      <div class="bx-learn-card"><span class="bx-learn-num">2</span><div><h4>Status codes carry real meaning</h4><p>Clients depend on the code, not just the response body, to know what happened.</p></div></div>
      <div class="bx-learn-card"><span class="bx-learn-num">3</span><div><h4>Route registration stays short</h4><p>Five lines wire up a full resource without any generated boilerplate.</p></div></div>
      <div class="bx-learn-card"><span class="bx-learn-num">4</span><div><h4>Bearer tokens need constant time checks</h4><p>hash_equals prevents a timing attack a plain comparison would allow.</p></div></div>
      <div class="bx-learn-card"><span class="bx-learn-num">5</span><div><h4>Errors should never leak internals</h4><p>A request ID beats a raw exception message in every response.</p></div></div>
      <div class="bx-learn-card"><span class="bx-learn-num">6</span><div><h4>curl confirms the whole chain</h4><p>A single command line request tests routing, auth, and the model together.</p></div></div>
    </div>
  </div>


  <div class="bx-cta">
    <h3>Ready to Ship a Lightweight PHP API?</h3>
    <p>Pair a rest api in php without a framework with a wider development workflow to keep every endpoint fast, secure, and easy to extend.</p>
    <div class="bx-cta-btns">
      <a href="/10-best-free-seo-tools-every-marketer-should-use/" target="_blank" rel="noopener">Explore Free SEO Tools</a>
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
