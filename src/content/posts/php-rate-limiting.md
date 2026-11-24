---
title: "PHP Rate Limiting: Protect Your API in 5 Steps"
slug: "php-rate-limiting"
date: "2026-08-26T09:36:08"
updated: "2026-08-26T09:36:44"
author: "santajigade"
categories: ["development", "php"]
primaryCategory: "development"
description: "PHP rate limiting protects your API from abuse. Learn token bucket and sliding window algorithms using Redis to block traffic spikes before they cause damage."
focusKeyword: "php rate limiting"
takeaways:
  - "A single unbounded caller can exhaust database connections and memory, slowing an API down for every other user."
  - "Redis gives every server in a cluster the same shared view of request counts, which flat file counters cannot do."
  - "A token bucket allows short bursts while enforcing a steady average rate, avoiding the fixed window's boundary burst problem."
  - "Rejected requests should return status 429 with a Retry-After header so well behaved clients know when to try again."
  - "Key limits by API key or user ID rather than IP address, and give login and password reset routes stricter limits."
image: "/wp-content/uploads/2026/08/php-rate-limiting.webp"
imageAlt: "php rate limiting"
words: 1594
views: 61
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
    <span class="bx-pill">Rate Limiting</span>
    <span class="bx-pill">Redis</span>
  </div>

  <p class="bx-lede">One script running in a loop can generate more traffic in a minute than a hundred real visitors send in a day. PHP rate limiting is what keeps that one script from taking down an endpoint everyone else still needs to use.</p>

  <div class="bx-section-head">
    <span class="bx-num">01</span>
    <h2 class="bx-h2" id="why-php-rate-limiting-matters-for-every-public-endpoint">Why PHP Rate Limiting Matters for Every Public Endpoint</h2>
    <div class="bx-rule"></div>
  </div>

  <p>An API with no limit at all treats every caller the same, whether it is a real user or a script hammering the same route in a tight loop.</p>

  <p>That single unbounded caller can exhaust database connections, fill up server memory, or simply push everyone else's requests to the back of the queue.</p>

  <p>A flat file counter per IP address, the kind used earlier in this series for a contact form, works fine at small scale but does not survive across multiple servers.</p>

  <p>Redis solves that gap. It gives every server in a cluster the same shared view of how many requests a caller has already made.</p>

  <p>Cloudflare's own <a href="https://www.cloudflare.com/learning/bots/what-is-rate-limiting/" target="_blank" rel="noopener">rate limiting documentation</a> makes a similar point about shared state: a centralized store is what makes php rate limiting meaningful once traffic crosses more than one server.</p>


  <div class="bx-section-head">
    <span class="bx-num">02</span>
    <h2 class="bx-h2" id="choosing-between-fixed-window-sliding-window-and-token-bucket">Choosing Between Fixed Window, Sliding Window, and Token Bucket</h2>
    <div class="bx-rule"></div>
  </div>

  <p>Three algorithms cover almost every real world rate limiting need, and each makes a different tradeoff between simplicity and smoothness.</p>

  <div class="bx-table-wrap">
    <table class="bx-table">
      <thead><tr><th>Algorithm</th><th>Behavior</th><th>Weakness</th></tr></thead>
      <tbody>
        <tr><td>Fixed window</td><td>Counts requests in fixed time blocks</td><td>Allows a burst right at the window boundary</td></tr>
        <tr><td>Sliding window</td><td>Counts requests in a rolling time frame</td><td>Slightly more storage and computation</td></tr>
        <tr><td>Token bucket</td><td>Refills tokens at a steady rate over time</td><td>More setup, but smooths bursts naturally</td></tr>
      </tbody>
    </table>
  </div>

  <p>Token bucket is the closest match to how most APIs actually want to behave, allowing a short burst while still enforcing a steady average rate.</p>

  <p><a href="https://owasp.org/API-Security/editions/2023/en/0xa4-unrestricted-resource-consumption/" target="_blank" rel="noopener">OWASP's API Security Top 10</a> lists unrestricted resource consumption as a leading risk, and picking the right algorithm here is a direct mitigation for that exact threat category, which is why php rate limiting counts as a core defensive control rather than an optional nice to have.</p>

  <div class="bx-section-head">
    <span class="bx-num">03</span>
    <h2 class="bx-h2" id="setting-up-redis-for-rate-limit-storage">Setting Up Redis for Rate Limit Storage</h2>
    <div class="bx-rule"></div>
  </div>

  <p>PHP talks to Redis through the <a href="https://github.com/phpredis/phpredis" target="_blank" rel="noopener"><code>phpredis</code></a> extension, which wraps the Redis commands used below in plain PHP method calls.</p>

  <div class="bx-code-wrap">
    <div class="bx-code-title">redis_connect.php</div>
    <pre><code><span class="tok-val">$redis</span> = <span class="tok-kw">new</span> Redis();
<span class="tok-val">$redis</span>->connect(<span class="tok-str">'127.0.0.1'</span>, <span class="tok-val">6379</span>);
<span class="tok-val">$redis</span>->setOption(Redis::OPT_PREFIX, <span class="tok-str">'ratelimit:'</span>);</code></pre>
  </div>

  <p>Setting a key prefix keeps rate limit keys clearly separated from anything else the same Redis instance might store for other parts of the application.</p>

  <p><a href="https://redis.io/docs/latest/commands/" target="_blank" rel="noopener">Redis's own command reference</a> covers every method used below in full detail, and the <a href="https://pecl.php.net/package/redis" target="_blank" rel="noopener">PECL extension page</a> lists the installation steps for whichever operating system is running the server.</p>

  <div class="bx-section-head">
    <span class="bx-num">04</span>
    <h2 class="bx-h2" id="implementing-a-token-bucket-limiter">Implementing a Token Bucket Limiter</h2>
    <div class="bx-rule"></div>
  </div>

  <p>Each caller gets a bucket that refills at a fixed rate, and a request only succeeds if a token is available to spend.</p>

  <div class="bx-code-wrap">
    <div class="bx-code-title">TokenBucket.php</div>
    <pre><code><span class="tok-kw">final class</span> TokenBucket {
    <span class="tok-kw">public function</span> <span class="tok-fn">__construct</span>(
        <span class="tok-kw">private</span> Redis <span class="tok-val">$redis</span>,
        <span class="tok-kw">private int</span> <span class="tok-val">$capacity</span> = <span class="tok-val">10</span>,
        <span class="tok-kw">private float</span> <span class="tok-val">$refillPerSecond</span> = <span class="tok-val">0.5</span>
    ) {}

    <span class="tok-kw">public function</span> <span class="tok-fn">allow</span>(<span class="tok-kw">string</span> <span class="tok-val">$key</span>): <span class="tok-kw">bool</span> {
        <span class="tok-val">$now</span> = microtime(<span class="tok-val">true</span>);
        <span class="tok-val">$state</span> = <span class="tok-val">$this</span>->redis->get(<span class="tok-val">$key</span>);
        [<span class="tok-val">$tokens</span>, <span class="tok-val">$lastRefill</span>] = <span class="tok-val">$state</span> ? explode(<span class="tok-str">'|'</span>, <span class="tok-val">$state</span>) : [<span class="tok-val">$this</span>->capacity, <span class="tok-val">$now</span>];

        <span class="tok-val">$elapsed</span> = <span class="tok-val">$now</span> - (<span class="tok-kw">float</span>) <span class="tok-val">$lastRefill</span>;
        <span class="tok-val">$tokens</span> = <span class="tok-fn">min</span>(<span class="tok-val">$this</span>->capacity, (<span class="tok-kw">float</span>) <span class="tok-val">$tokens</span> + <span class="tok-val">$elapsed</span> * <span class="tok-val">$this</span>->refillPerSecond);

        <span class="tok-kw">if</span> (<span class="tok-val">$tokens</span> < <span class="tok-val">1</span>) {
            <span class="tok-val">$this</span>->redis->setex(<span class="tok-val">$key</span>, <span class="tok-val">3600</span>, <span class="tok-fn">sprintf</span>(<span class="tok-str">'%f|%f'</span>, <span class="tok-val">$tokens</span>, <span class="tok-val">$now</span>));
            <span class="tok-kw">return</span> <span class="tok-val">false</span>;
        }

        <span class="tok-val">$this</span>->redis->setex(<span class="tok-val">$key</span>, <span class="tok-val">3600</span>, <span class="tok-fn">sprintf</span>(<span class="tok-str">'%f|%f'</span>, <span class="tok-val">$tokens</span> - <span class="tok-val">1</span>, <span class="tok-val">$now</span>));
        <span class="tok-kw">return</span> <span class="tok-val">true</span>;
    }
}</code></pre>
  </div>

  <p>Storing the token count and the last refill time together in one string keeps the read and write a single round trip to Redis instead of two separate calls that could race against each other.</p>

  <p>The <a href="https://www.php.net/manual/en/function.microtime.php" target="_blank" rel="noopener">php.net manual for microtime()</a> explains the float mode used here, which keeps the elapsed time calculation precise enough for sub second refill rates.</p>

  <div class="bx-section-head">
    <span class="bx-num">05</span>
    <h2 class="bx-h2" id="implementing-a-sliding-window-limiter">Implementing a Sliding Window Limiter</h2>
    <div class="bx-rule"></div>
  </div>

  <p>A sliding window counts requests inside a rolling time frame rather than resetting sharply at a fixed boundary, which avoids the fixed window's burst problem.</p>

  <div class="bx-code-wrap">
    <div class="bx-code-title">sliding_window.php</div>
    <pre><code><span class="tok-kw">function</span> <span class="tok-fn">allow_sliding</span>(Redis <span class="tok-val">$redis</span>, <span class="tok-kw">string</span> <span class="tok-val">$key</span>, <span class="tok-kw">int</span> <span class="tok-val">$limit</span>, <span class="tok-kw">int</span> <span class="tok-val">$windowSeconds</span>): <span class="tok-kw">bool</span> {
    <span class="tok-val">$now</span> = microtime(<span class="tok-val">true</span>);
    <span class="tok-val">$redis</span>->zRemRangeByScore(<span class="tok-val">$key</span>, <span class="tok-val">0</span>, <span class="tok-val">$now</span> - <span class="tok-val">$windowSeconds</span>);

    <span class="tok-kw">if</span> (<span class="tok-val">$redis</span>->zCard(<span class="tok-val">$key</span>) >= <span class="tok-val">$limit</span>) {
        <span class="tok-kw">return</span> <span class="tok-val">false</span>;
    }

    <span class="tok-val">$redis</span>->zAdd(<span class="tok-val">$key</span>, <span class="tok-val">$now</span>, uniqid(<span class="tok-str">''</span>, <span class="tok-val">true</span>));
    <span class="tok-val">$redis</span>->expire(<span class="tok-val">$key</span>, <span class="tok-val">$windowSeconds</span>);
    <span class="tok-kw">return</span> <span class="tok-val">true</span>;
}</code></pre>
  </div>

  <p>A Redis sorted set stores one entry per request, scored by timestamp, so trimming entries older than the window is a single command instead of scanning a whole list.</p>

  <div class="bx-section-head">
    <span class="bx-num">06</span>
    <h2 class="bx-h2" id="returning-proper-rate-limit-headers-and-status-codes">Returning Proper Rate Limit Headers and Status Codes</h2>
    <div class="bx-rule"></div>
  </div>

  <p>A rejected request should tell the caller exactly what happened and when it is safe to try again, not just fail with a plain error.</p>

  <div class="bx-code-wrap">
    <div class="bx-code-title">respond_limited.php</div>
    <pre><code><span class="tok-kw">if</span> (!<span class="tok-val">$bucket</span>->allow(<span class="tok-val">$apiKey</span>)) {
    header(<span class="tok-str">'Retry-After: 2'</span>);
    header(<span class="tok-str">'X-RateLimit-Limit: 10'</span>);
    http_response_code(<span class="tok-val">429</span>);
    <span class="tok-fn">echo</span> json_encode([<span class="tok-str">'error'</span> => <span class="tok-str">'Too many requests'</span>]);
    <span class="tok-kw">exit</span>;
}</code></pre>
  </div>

  <p>Status <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429" target="_blank" rel="noopener">429</a> is the standard code for this situation, and a well behaved client library already knows to back off and retry after seeing it.</p>

  <p><a href="https://www.rfc-editor.org/rfc/rfc6585" target="_blank" rel="noopener">RFC 6585</a> is the document that formally defines status 429, and it specifically recommends sending a Retry-After header so automated clients know exactly when it is safe to try again.</p>

  <div class="bx-section-head">
    <span class="bx-num">07</span>
    <h2 class="bx-h2" id="applying-different-limits-per-endpoint-or-user-tier">Applying Different Limits Per Endpoint or User Tier</h2>
    <div class="bx-rule"></div>
  </div>

  <p>Not every route deserves the same limit. A search endpoint might tolerate heavy use, while a password reset endpoint should stay tight regardless of who is calling it.</p>

  <div class="bx-code-wrap">
    <div class="bx-code-title">tier_limits.php</div>
    <pre><code><span class="tok-val">$limits</span> = [
    <span class="tok-str">'free'</span> => <span class="tok-kw">new</span> TokenBucket(<span class="tok-val">$redis</span>, capacity: <span class="tok-val">10</span>, refillPerSecond: <span class="tok-val">0.2</span>),
    <span class="tok-str">'pro'</span> => <span class="tok-kw">new</span> TokenBucket(<span class="tok-val">$redis</span>, capacity: <span class="tok-val">100</span>, refillPerSecond: <span class="tok-val">2.0</span>),
];

<span class="tok-val">$bucket</span> = <span class="tok-val">$limits</span>[<span class="tok-val">$user</span>[<span class="tok-str">'tier'</span>]] ?? <span class="tok-val">$limits</span>[<span class="tok-str">'free'</span>];</code></pre>
  </div>

  <p>Keying the bucket lookup by API key rather than IP address also means a shared office network never accidentally hits one caller's limit on another caller's behalf.</p>

  <ul class="bx-checklist">
    <li><b>Key limits by API key or user ID:</b> IP based limiting punishes everyone behind the same router or proxy for one caller's traffic, a mistake basic php rate limiting setups make constantly.</li>
    <li><b>Always return Retry-After:</b> a well built client can back off automatically instead of hammering the endpoint again immediately.</li>
    <li><b>Set an expiry on every Redis key:</b> a limiter that never expires its own state slowly fills memory with stale entries.</li>
    <li><b>Log rejected requests separately:</b> a spike in 429 responses is often the first sign of abuse worth investigating further.</li>
    <li><b>Tighten limits on sensitive endpoints:</b> login and password reset routes deserve a stricter limit than a general read endpoint.</li>
  </ul>


  <div class="bx-section-head">
    <span class="bx-num">08</span>
    <h2 class="bx-h2" id="testing-the-limiter-under-load">Testing the Limiter Under Load</h2>
    <div class="bx-rule"></div>
  </div>

  <p>A limiter that has never actually been pushed past its limit in a test is a limiter nobody can be fully sure works correctly.</p>

  <div class="bx-code-wrap">
    <div class="bx-code-title">terminal</div>
    <pre><code><span class="tok-cm"># fire 20 rapid requests and count how many get rejected</span>
<span class="tok-kw">for</span> i <span class="tok-kw">in</span> {1..20}; <span class="tok-kw">do</span>
  curl -s -o /dev/null -w <span class="tok-str">"%{http_code}\n"</span> https://api.example.com/search
<span class="tok-kw">done</span> | sort | uniq -c</code></pre>
  </div>

  <p>Seeing a mix of <code>200</code> and <code>429</code> responses in that output confirms the bucket is enforcing its limit rather than silently allowing everything through.</p>

  <svg width="100%" height="220" viewBox="0 0 800 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Diagram of php rate limiting moving an incoming request through a Redis backed token bucket check before either a 429 rejection or a normal response" style="margin:26px 0;">
    <rect width="800" height="220" fill="#f4faef" rx="12"/>
    <g font-family="Open Sans, sans-serif" font-size="13" fill="#2b2b2b">
      <rect x="15" y="85" width="115" height="55" rx="8" fill="#ffffff" stroke="#5DB92E" stroke-width="2"/>
      <text x="72" y="117" text-anchor="middle" font-weight="700">API Request</text>

      <line x1="130" y1="112" x2="170" y2="112" stroke="#4a9e24" stroke-width="2" marker-end="url(#arrow)"/>

      <rect x="170" y="85" width="140" height="55" rx="8" fill="#ffffff" stroke="#5DB92E" stroke-width="2"/>
      <text x="240" y="117" text-anchor="middle" font-weight="700">Redis Token Check</text>

      <line x1="310" y1="112" x2="350" y2="112" stroke="#4a9e24" stroke-width="2" marker-end="url(#arrow)"/>

      <rect x="350" y="85" width="115" height="55" rx="8" fill="#2b2b2b" stroke="#5DB92E" stroke-width="2"/>
      <text x="407" y="117" text-anchor="middle" font-weight="700" fill="#5DB92E">200 Response</text>

      <line x1="240" y1="140" x2="240" y2="170" stroke="#4a9e24" stroke-width="2" marker-end="url(#arrow)"/>
      <rect x="165" y="170" width="150" height="45" rx="8" fill="#ffffff" stroke="#5DB92E" stroke-width="2"/>
      <text x="240" y="197" text-anchor="middle" font-weight="700">429 Too Many</text>
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
      <button type="button" class="bx-faq-q">Is Redis required for PHP rate limiting, or can a database work instead?</button>
      <div class="bx-faq-a"><p>A database can work but is slower for this purpose. Redis keeps everything in memory and supports the atomic operations a limiter needs, which is why it is the common choice.</p></div>
    </div>
    <div class="bx-faq-item">
      <button type="button" class="bx-faq-q">Why is php rate limiting better with a token bucket than a simple counter?</button>
      <div class="bx-faq-a"><p>A simple counter resets sharply at a fixed boundary, allowing a burst right at that edge. A token bucket refills gradually, which smooths traffic more naturally.</p></div>
    </div>
    <div class="bx-faq-item">
      <button type="button" class="bx-faq-q">Should rate limiting happen in PHP or at the web server level?</button>
      <div class="bx-faq-a"><p>Both have a place. A web server or reverse proxy can block obvious floods early, while PHP level limiting allows finer control per user, per endpoint, or per API key.</p></div>
    </div>
    <div class="bx-faq-item">
      <button type="button" class="bx-faq-q">What happens to a legitimate user who hits the limit by accident?</button>
      <div class="bx-faq-a"><p>They receive a 429 response with a Retry-After header telling them exactly how long to wait, so a well built client can recover automatically without any manual intervention.</p></div>
    </div>
    <div class="bx-faq-item">
      <button type="button" class="bx-faq-q">Does rate limiting protect against every kind of API abuse?</button>
      <div class="bx-faq-a"><p>No. It protects against volume based abuse specifically. Authentication, input validation, and authorization checks still need to run independently to cover other kinds of misuse.</p></div>
    </div>
  </div>

  <div class="bx-learn">
    <h2 id="what-we-learn-today">What We Learn Today</h2>
    <div class="bx-learn-grid">
      <div class="bx-learn-card"><span class="bx-learn-num">1</span><div><h4>One caller can affect everyone</h4><p>Unbounded traffic from a single source degrades an API for all users.</p></div></div>
      <div class="bx-learn-card"><span class="bx-learn-num">2</span><div><h4>Redis enables shared state</h4><p>Multiple servers can enforce the same limit without stepping on each other.</p></div></div>
      <div class="bx-learn-card"><span class="bx-learn-num">3</span><div><h4>Token bucket smooths bursts</h4><p>A gradual refill avoids the sharp edge a fixed window creates.</p></div></div>
      <div class="bx-learn-card"><span class="bx-learn-num">4</span><div><h4>429 has a specific meaning</h4><p>Clients already know to back off and retry after seeing this code.</p></div></div>
      <div class="bx-learn-card"><span class="bx-learn-num">5</span><div><h4>Limits should vary by endpoint</h4><p>A login route deserves a tighter limit than a general search route.</p></div></div>
      <div class="bx-learn-card"><span class="bx-learn-num">6</span><div><h4>Testing under load confirms it works</h4><p>A limiter never pushed past its limit is one nobody has verified.</p></div></div>
    </div>
  </div>


  <div class="bx-cta">
    <h3>Ready to Protect Your API From Abuse?</h3>
    <p>Pair php rate limiting with a wider security minded workflow to keep every endpoint fast and available for real users.</p>
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

    item.classList.add('open');
    a.style.maxHeight = a.scrollHeight + 'px';

    q.addEventListener('click', function() {
      var isOpen = item.classList.contains('open');
      if (isOpen) {
        item.classList.remove('open');
        a.style.maxHeight = null;
      } else {
        item.classList.add('open');
        a.style.maxHeight = a.scrollHeight + 'px';
      }
    });
  });
})();
</script>
