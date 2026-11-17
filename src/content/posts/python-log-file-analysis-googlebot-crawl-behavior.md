---
title: "Python Log File Analysis: 8 Proven Steps to Decode Googlebot Crawl Behavior"
slug: "python-log-file-analysis-googlebot-crawl-behavior"
date: "2026-08-25T07:50:34"
updated: "2026-08-25T07:51:00"
author: "santajigade"
categories: ["development", "python"]
primaryCategory: "development"
description: "Python log file analysis turns raw server logs into a clear picture of how Googlebot actually crawls your site, no sampling, no guessing, just real requests."
focusKeyword: "python log file analysis"
takeaways:
  - "Server logs record every request Googlebot makes, while Search Console crawl stats only show an aggregated summary."
  - "Python's built in re module and pandas are enough to parse standard Apache combined format log lines into structured data."
  - "A Googlebot user agent string proves nothing, so requests must be verified with a forward confirmed reverse DNS lookup."
  - "Running DNS verification once per unique IP, not per log line, avoids repeating the same lookups thousands of times."
  - "Grouping verified requests by status code and parameter URLs shows where crawl budget is being wasted on non indexable pages."
image: "/wp-content/uploads/2026/08/Python-Log-File-Analysis.webp"
imageAlt: "Python Log File Analysis"
words: 2081
views: 48
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
table.bx-table thead tr { background: var(--bx-charcoal); }
table.bx-table thead th { color: #fff; font-family: var(--bx-disp); font-weight: 700; text-align: left; padding: 13px 14px; font-size: 17px; }
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
    <span class="bx-pill">Python</span>
    <span class="bx-pill">Log Files</span>
    <span class="bx-pill">Technical SEO</span>
  </div>

  <p class="bx-lede">Search Console shows a sampled, aggregated version of how Google sees your site. Server logs show every single request, exactly as it happened. Python log file analysis is how you read that second, more honest record.</p>

  <p>A site we reviewed once looked completely healthy in Search Console. Crawl stats were steady, nothing alarming in the charts.</p>

  <p>The raw log files told a different story. Roughly sixty percent of Googlebot's requests that month went to filtered category URLs with parameters attached, not to the actual product pages anyone wanted ranked.</p>

  <p>No dashboard surfaced that pattern on its own. Only the logs, read line by line through python log file analysis, showed exactly where the crawl budget was actually going.</p>

  <p>Python log file analysis is what makes reading thousands or millions of those lines practical. This guide parses raw server logs, separates genuine Googlebot requests from spoofed ones, and turns the result into a clear picture of real crawl behavior.</p>

  <p>Nothing here needs a paid log analyzer. A folder of log files and a Python environment cover the whole thing.</p>

  <div class="bx-stats">
    <div class="bx-stat-card"><span class="bx-stat-num">100%</span><span class="bx-stat-label">of requests appear in raw logs, versus a sampled view in most dashboards</span></div>
    <div class="bx-stat-card"><span class="bx-stat-num">2 checks</span><span class="bx-stat-label">confirm a request is genuinely Googlebot, not just a spoofed user agent</span></div>
    <div class="bx-stat-card"><span class="bx-stat-num">1 file</span><span class="bx-stat-label">type covers most hosts: the standard combined access log format</span></div>
  </div>

  <div class="bx-section-head">
    <span class="bx-num">01</span>
    <h2 class="bx-h2" id="why-python-log-file-analysis-reveals-what-search-console-cannot">Why Python Log File Analysis Reveals What Search Console Cannot</h2>
    <div class="bx-rule"></div>
  </div>

  <p>The <a href="/understanding-crawl-stats-report/" target="_blank" rel="noopener">crawl stats report</a> in Search Console is a genuinely useful summary. It is still a summary, built from aggregated numbers rather than the individual requests behind them.</p>

  <p>A server log has no such filter. Every request Googlebot ever made to your server sits there, one line at a time, with a timestamp, a path, and a status code attached.</p>

  <p>That level of detail is what makes it possible to answer specific questions a dashboard was never built to answer. Which exact pages get crawled daily, and which have not been touched in months.</p>

  <p>Whether Googlebot is spending its visits on real content or burning through <a href="/crawl-budget-explained/" target="_blank" rel="noopener">crawl budget</a> on filtered, parameterized, or duplicate URLs is a question only python log file analysis can answer with certainty.</p>

  <div class="bx-ad">
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3931314195561246" crossorigin="anonymous"></script>
    <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-3931314195561246" data-ad-slot="4249015278" data-ad-format="auto" data-full-width-responsive="true"></ins>
    <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
  </div>

  <div class="bx-section-head">
    <span class="bx-num">02</span>
    <h2 class="bx-h2" id="getting-your-server-log-files">Getting Your Server Log Files</h2>
    <div class="bx-rule"></div>
  </div>

  <p>Where log files live depends entirely on the hosting setup. Shared hosting often exposes them through a control panel, a VPS usually keeps them in a predictable system folder, and sites behind a CDN need an export from that provider instead.</p>

  <div class="bx-table-wrap">
    <table class="bx-table">
      <thead>
        <tr><th>Format</th><th>Common Source</th><th>Key Fields</th></tr>
      </thead>
      <tbody>
        <tr><td>Apache Combined Log Format</td><td>Apache, most shared hosting</td><td>IP, timestamp, request, status, bytes, referrer, user agent</td></tr>
        <tr><td>Nginx access log</td><td>Nginx servers</td><td>Same core fields, slightly different default layout</td></tr>
        <tr><td>CDN or edge logs</td><td>Cloudflare, Fastly, and similar</td><td>Often JSON, with extra edge and cache fields included</td></tr>
        <tr><td>Custom application logs</td><td>Some frameworks and platforms</td><td>Varies widely, always worth checking the format first</td></tr>
      </tbody>
    </table>
  </div>

  <p>The examples in this guide use the <a href="https://httpd.apache.org/docs/2.4/logs.html" target="_blank" rel="noopener">Apache combined log format</a>, since it covers the large majority of sites and is close enough to the <a href="https://nginx.org/en/docs/http/ngx_http_log_module.html" target="_blank" rel="noopener">Nginx default format</a> that the parsing logic adapts easily.</p>

  <div class="bx-section-head">
    <span class="bx-num">03</span>
    <h2 class="bx-h2" id="setting-up-your-python-environment">Setting Up Your Python Environment</h2>
    <div class="bx-rule"></div>
  </div>

  <div class="bx-code-wrap">
    <div class="bx-code-title">Terminal: project setup</div>
    <pre><code><span class="tok-cm"># create an isolated environment so package versions don't clash</span>
python -m venv venv
<span class="tok-val">source</span> venv/bin/activate      <span class="tok-cm"># Windows: venv\Scripts\activate</span>

pip install pandas</code></pre>
  </div>

  <p>That is genuinely the whole list. Parsing a standard combined log line only needs Python's built in <a href="https://docs.python.org/3/library/re.html" target="_blank" rel="noopener">re</a> module, and <a href="https://pandas.pydata.org/" target="_blank" rel="noopener">pandas</a> is enough to hold and analyze everything that comes out of it.</p>

  <div class="bx-section-head">
    <span class="bx-num">04</span>
    <h2 class="bx-h2" id="parsing-raw-log-lines-into-structured-data">Parsing Raw Log Lines Into Structured Data</h2>
    <div class="bx-rule"></div>
  </div>

  <p>A single combined format log line looks dense at first glance, but it breaks down into the same handful of fields every time. A regular expression captures all of them in one pass.</p>

  <div class="bx-code-wrap">
    <div class="bx-code-title">log_parser.py</div>
    <pre><code><span class="tok-kw">import</span> re
<span class="tok-kw">import</span> pandas <span class="tok-kw">as</span> pd

<span class="tok-fn">LOG_PATTERN</span> = re.compile(
    <span class="tok-str">r'(?P&lt;ip&gt;\S+) \S+ \S+ \[(?P&lt;timestamp&gt;.+?)\] '</span>
    <span class="tok-str">r'"(?P&lt;method&gt;\S+) (?P&lt;path&gt;\S+) \S+" '</span>
    <span class="tok-str">r'(?P&lt;status&gt;\d+) (?P&lt;bytes&gt;\S+) '</span>
    <span class="tok-str">r'"(?P&lt;referrer&gt;.*?)" "(?P&lt;user_agent&gt;.*?)"'</span>
)

<span class="tok-kw">def</span> <span class="tok-fn">parse_log_file</span>(file_path: <span class="tok-fn">str</span>) -> pd.DataFrame:
    records = []

    <span class="tok-kw">with</span> <span class="tok-fn">open</span>(file_path, <span class="tok-str">"r"</span>, encoding=<span class="tok-str">"utf-8"</span>, errors=<span class="tok-str">"ignore"</span>) <span class="tok-kw">as</span> f:
        <span class="tok-kw">for</span> line <span class="tok-kw">in</span> f:
            match = LOG_PATTERN.match(line)
            <span class="tok-kw">if</span> match:
                records.append(match.groupdict())

    df = pd.DataFrame(records)
    df[<span class="tok-str">"status"</span>] = df[<span class="tok-str">"status"</span>].astype(<span class="tok-fn">int</span>)
    <span class="tok-kw">return</span> df</code></pre>
  </div>

  <p>Lines that do not match the pattern are simply skipped rather than crashing the whole run. A stray malformed line in a multi million row file should never take down the entire analysis.</p>

  <div class="bx-section-head">
    <span class="bx-num">05</span>
    <h2 class="bx-h2" id="filtering-for-googlebot-requests">Filtering for Googlebot Requests</h2>
    <div class="bx-rule"></div>
  </div>

  <p>With the log parsed into a dataframe, the next stage of python log file analysis is isolating Googlebot's own requests with a simple filter on the user agent string.</p>

  <div class="bx-code-wrap">
    <div class="bx-code-title">filter_bots.py</div>
    <pre><code><span class="tok-kw">def</span> <span class="tok-fn">filter_googlebot_claims</span>(df: pd.DataFrame) -> pd.DataFrame:
    <span class="tok-kw">return</span> df[df[<span class="tok-str">"user_agent"</span>].str.contains(<span class="tok-str">"Googlebot"</span>, case=<span class="tok-kw">False</span>, na=<span class="tok-kw">False</span>)]</code></pre>
  </div>

  <p>Call this step a filter for requests that claim to be Googlebot, not a filter for confirmed Googlebot. That distinction matters more than it sounds, and it is the entire subject of the next section.</p>

  <div class="bx-section-head">
    <span class="bx-num">06</span>
    <h2 class="bx-h2" id="verifying-real-googlebot-with-reverse-dns">Verifying Real Googlebot With Reverse DNS</h2>
    <div class="bx-rule"></div>
  </div>

  <p>Anyone can send a request with <code>Googlebot</code> typed into the user agent header. The string alone proves nothing, and <a href="https://searchengineland.com/guide/what-is-googlebot-fraud" target="_blank" rel="noopener">fake Googlebot traffic</a> claiming to be the real crawler is common enough to have its own name.</p>

  <p><a href="https://developers.google.com/crawling/docs/crawlers-fetchers/verify-google-requests" target="_blank" rel="noopener">Google's own documentation</a> describes the fix for genuine python log file analysis: a forward confirmed reverse DNS lookup. Look up the hostname behind the request's IP address, confirm it ends in <code>googlebot.com</code> or <code>google.com</code>, then look that hostname back up and confirm it resolves to the same original IP.</p>

  <div class="bx-code-wrap">
    <div class="bx-code-title">verify_googlebot.py</div>
    <pre><code><span class="tok-kw">import</span> socket

<span class="tok-fn">VALID_SUFFIXES</span> = (<span class="tok-str">".googlebot.com"</span>, <span class="tok-str">".google.com"</span>)

<span class="tok-kw">def</span> <span class="tok-fn">is_verified_googlebot</span>(ip_address: <span class="tok-fn">str</span>) -> <span class="tok-fn">bool</span>:
    <span class="tok-kw">try</span>:
        hostname, _, _ = socket.gethostbyaddr(ip_address)
    <span class="tok-kw">except</span> socket.herror:
        <span class="tok-kw">return</span> <span class="tok-kw">False</span>

    <span class="tok-kw">if</span> <span class="tok-kw">not</span> hostname.endswith(VALID_SUFFIXES):
        <span class="tok-kw">return</span> <span class="tok-kw">False</span>

    <span class="tok-kw">try</span>:
        forward_ip = socket.gethostbyname(hostname)
    <span class="tok-kw">except</span> socket.gaierror:
        <span class="tok-kw">return</span> <span class="tok-kw">False</span>

    <span class="tok-kw">return</span> forward_ip == ip_address</code></pre>
  </div>

  <p>Run this once per unique IP rather than once per log line. A busy site might see the same Googlebot IP thousands of times in a single day, and there is no reason to repeat the same two DNS lookups that many times.</p>

  <div class="bx-code-wrap">
    <div class="bx-code-title">apply_verification.py</div>
    <pre><code><span class="tok-kw">def</span> <span class="tok-fn">apply_verification</span>(df: pd.DataFrame) -> pd.DataFrame:
    unique_ips = df[<span class="tok-str">"ip"</span>].unique()
    verification = {ip: <span class="tok-fn">is_verified_googlebot</span>(ip) <span class="tok-kw">for</span> ip <span class="tok-kw">in</span> unique_ips}

    df[<span class="tok-str">"is_verified"</span>] = df[<span class="tok-str">"ip"</span>].map(verification)
    <span class="tok-kw">return</span> df</code></pre>
  </div>

  <p>Anything that fails this check but still claims to be Googlebot in its user agent is worth a second look. That combination is one of the more reliable signals of a spoofed crawler or a scraper hiding behind a familiar name, a pattern <a href="/how-google-crawls-websites/" target="_blank" rel="noopener">how Googlebot actually crawls the web</a> covers in more depth.</p>

  <div class="bx-ad">
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3931314195561246" crossorigin="anonymous"></script>
    <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-3931314195561246" data-ad-slot="4249015278" data-ad-format="auto" data-full-width-responsive="true"></ins>
    <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
  </div>

  <div class="bx-section-head">
    <span class="bx-num">07</span>
    <h2 class="bx-h2" id="analyzing-crawl-frequency-and-patterns">Analyzing Crawl Frequency and Patterns</h2>
    <div class="bx-rule"></div>
  </div>

  <p>Once verified Googlebot rows are isolated, grouping by path and by day turns raw requests into an actual picture of crawl behavior.</p>

  <div class="bx-code-wrap">
    <div class="bx-code-title">analyze_frequency.py</div>
    <pre><code><span class="tok-kw">def</span> <span class="tok-fn">crawl_frequency_by_path</span>(df: pd.DataFrame) -> pd.DataFrame:
    verified = df[df[<span class="tok-str">"is_verified"</span>]]
    counts = verified.groupby(<span class="tok-str">"path"</span>).size().reset_index(name=<span class="tok-str">"crawl_count"</span>)
    <span class="tok-kw">return</span> counts.sort_values(<span class="tok-str">"crawl_count"</span>, ascending=<span class="tok-kw">False</span>)

<span class="tok-kw">def</span> <span class="tok-fn">crawl_volume_by_day</span>(df: pd.DataFrame) -> pd.DataFrame:
    verified = df[df[<span class="tok-str">"is_verified"</span>]].copy()
    verified[<span class="tok-str">"date"</span>] = pd.to_datetime(
        verified[<span class="tok-str">"timestamp"</span>], format=<span class="tok-str">"%d/%b/%Y:%H:%M:%S %z"</span>
    ).dt.date
    <span class="tok-kw">return</span> verified.groupby(<span class="tok-str">"date"</span>).size().reset_index(name=<span class="tok-str">"requests"</span>)</code></pre>
  </div>

  <p>The most crawled paths often line up with what you would expect, the homepage and top category pages. The genuinely useful part is what shows up unexpectedly high, or what important pages barely show up at all.</p>

  <div class="bx-section-head">
    <span class="bx-num">08</span>
    <h2 class="bx-h2" id="finding-wasted-crawl-budget">Finding Wasted Crawl Budget</h2>
    <div class="bx-rule"></div>
  </div>

  <p>Grouping verified requests by status code shows exactly where crawl budget is going, and how much of it is going somewhere other than a real, indexable page.</p>

  <div class="bx-code-wrap">
    <div class="bx-code-title">wasted_budget.py</div>
    <pre><code><span class="tok-kw">def</span> <span class="tok-fn">status_code_breakdown</span>(df: pd.DataFrame) -> pd.DataFrame:
    verified = df[df[<span class="tok-str">"is_verified"</span>]]
    breakdown = verified[<span class="tok-str">"status"</span>].value_counts(normalize=<span class="tok-kw">True</span>) * <span class="tok-val">100</span>
    <span class="tok-kw">return</span> breakdown.round(<span class="tok-val">1</span>)

<span class="tok-kw">def</span> <span class="tok-fn">parameter_url_share</span>(df: pd.DataFrame) -> <span class="tok-fn">float</span>:
    verified = df[df[<span class="tok-str">"is_verified"</span>]]
    has_params = verified[<span class="tok-str">"path"</span>].str.contains(<span class="tok-str">r"\?"</span>, regex=<span class="tok-kw">True</span>)
    <span class="tok-kw">return</span> <span class="tok-fn">round</span>(has_params.mean() * <span class="tok-val">100</span>, <span class="tok-val">1</span>)</code></pre>
  </div>

  <p>A high share of 404s, redirects, or parameter heavy URLs in that breakdown is the exact signal that sent us digging in the anecdote at the start of this guide. The fix always starts with seeing the number first.</p>

  <div class="bx-section-head">
    <span class="bx-num">09</span>
    <h2 class="bx-h2" id="turning-log-data-into-a-recurring-crawl-report">Turning Log Data Into a Recurring Crawl Report</h2>
    <div class="bx-rule"></div>
  </div>

  <p>Logs rotate and get deleted on most hosts after a set number of days, so a one time run of python log file analysis only captures a narrow window. Running it on a schedule keeps a longer history than the server itself ever holds onto.</p>

  <div class="bx-code-wrap">
    <div class="bx-code-title">run_report.py</div>
    <pre><code><span class="tok-kw">import</span> pandas <span class="tok-kw">as</span> pd
<span class="tok-kw">from</span> log_parser <span class="tok-kw">import</span> parse_log_file
<span class="tok-kw">from</span> filter_bots <span class="tok-kw">import</span> filter_googlebot_claims
<span class="tok-kw">from</span> verify_googlebot <span class="tok-kw">import</span> apply_verification

<span class="tok-kw">def</span> <span class="tok-fn">run</span>(log_file: <span class="tok-fn">str</span>):
    df = <span class="tok-fn">parse_log_file</span>(log_file)
    bots = <span class="tok-fn">filter_googlebot_claims</span>(df)
    verified = <span class="tok-fn">apply_verification</span>(bots)

    summary = pd.DataFrame({
        <span class="tok-str">"total_claimed_googlebot"</span>: [<span class="tok-fn">len</span>(bots)],
        <span class="tok-str">"verified_googlebot"</span>: [verified[<span class="tok-str">"is_verified"</span>].sum()],
        <span class="tok-str">"unverified_claims"</span>: [(<span class="tok-kw">not</span> verified[<span class="tok-str">"is_verified"</span>]).sum()],
    })
    summary.to_csv(<span class="tok-str">"crawl_verification_summary.csv"</span>, index=<span class="tok-kw">False</span>)
    <span class="tok-fn">print</span>(summary)

<span class="tok-kw">if</span> __name__ == <span class="tok-str">"__main__"</span>:
    <span class="tok-fn">run</span>(<span class="tok-str">"access.log"</span>)</code></pre>
  </div>

  <p>Scheduling this weekly through <a href="https://docs.github.com/en/actions" target="_blank" rel="noopener">GitHub Actions</a>, the same way earlier automation guides in this series do, keeps a running archive of crawl behavior long after the raw log itself has been rotated away.</p>

  <ul class="bx-checklist">
    <li><b>Confirm the log format first:</b> check a few sample lines before trusting any parser against a new host.</li>
    <li><b>Always verify, never trust the user agent alone:</b> the reverse DNS check is not optional if the analysis will inform real decisions.</li>
    <li><b>Cache DNS results per IP:</b> avoid repeating the same lookup thousands of times across one log file.</li>
    <li><b>Watch parameter and redirect heavy paths:</b> these are the most common source of wasted crawl budget.</li>
    <li><b>Archive summaries before logs rotate:</b> most hosts do not keep raw logs longer than a few weeks.</li>
  </ul>

  <div class="bx-section-head">
    <span class="bx-num">10</span>
    <h2 class="bx-h2" id="watch-how-googlebot-actually-crawls-and-renders-pages">Watch: How Googlebot Actually Crawls and Renders Pages</h2>
    <div class="bx-rule"></div>
  </div>

  <p>Martin Splitt, a Google Search Central developer advocate who works directly on crawling and rendering, explains the mechanics of how Googlebot processes a page once it has been requested, which is exactly what shows up as a single line in the logs this guide parses.</p>

  <div style="position:relative; padding-bottom:56.25%; height:0; overflow:hidden; border-radius:12px; margin:18px 0 8px;">
    <iframe src="https://www.youtube.com/embed/2snXeMR6jRU" title="How Does Googlebot Render Web Pages, by Martin Splitt of Google Search Central" style="position:absolute; top:0; left:0; width:100%; height:100%; border:0;" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen loading="lazy"></iframe>
  </div>
  <p style="font-size:14px; color:var(--bx-charcoal-soft); margin-top:6px;">Video credit: Martin Splitt, Google Search Central.</p>

  <p>Seeing what happens after the request lands helps explain why a single crawl in the logs does not always mean a page updates in search results right away.</p>

  <svg width="100%" height="220" viewBox="0 0 800 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Diagram of python log file analysis moving from raw server logs through Googlebot verification to a crawl frequency report" style="margin:26px 0;">
    <rect width="800" height="220" fill="#f4faef" rx="12"/>
    <g font-family="Open Sans, sans-serif" font-size="14" fill="#2b2b2b">
      <rect x="20" y="85" width="130" height="60" rx="8" fill="#ffffff" stroke="#5DB92E" stroke-width="2"/>
      <text x="85" y="120" text-anchor="middle" font-weight="700">Raw Log Files</text>

      <line x1="150" y1="115" x2="200" y2="115" stroke="#4a9e24" stroke-width="2" marker-end="url(#arrow)"/>

      <rect x="200" y="85" width="140" height="60" rx="8" fill="#ffffff" stroke="#5DB92E" stroke-width="2"/>
      <text x="270" y="120" text-anchor="middle" font-weight="700">Regex Parsing</text>

      <line x1="340" y1="115" x2="390" y2="115" stroke="#4a9e24" stroke-width="2" marker-end="url(#arrow)"/>

      <rect x="390" y="85" width="150" height="60" rx="8" fill="#ffffff" stroke="#5DB92E" stroke-width="2"/>
      <text x="465" y="112" text-anchor="middle" font-weight="700">Reverse DNS</text>
      <text x="465" y="130" text-anchor="middle" font-weight="700">Verification</text>

      <line x1="540" y1="115" x2="590" y2="115" stroke="#4a9e24" stroke-width="2" marker-end="url(#arrow)"/>

      <rect x="590" y="85" width="170" height="60" rx="8" fill="#2b2b2b" stroke="#5DB92E" stroke-width="2"/>
      <text x="675" y="120" text-anchor="middle" font-weight="700" fill="#5DB92E">Crawl Frequency Report</text>
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
      <button type="button" class="bx-faq-q">Can I trust the user agent header alone to identify Googlebot?</button>
      <div class="bx-faq-a"><p>No. The user agent string is trivial to fake, so any serious analysis needs a reverse DNS check to confirm a request is genuinely coming from Google's own IP ranges.</p></div>
    </div>
    <div class="bx-faq-item">
      <button type="button" class="bx-faq-q">Where do I get my server's raw log files?</button>
      <div class="bx-faq-a"><p>It depends on the host. Shared hosting usually exposes logs through a control panel, a VPS keeps them in a standard system folder, and sites behind a CDN need to export them from that provider instead.</p></div>
    </div>
    <div class="bx-faq-item">
      <button type="button" class="bx-faq-q">How much log history is enough for meaningful python log file analysis?</button>
      <div class="bx-faq-a"><p>Two to four weeks is usually enough to spot real patterns rather than a single unusual day. Archiving weekly summaries over time builds a much longer picture than any one export can.</p></div>
    </div>
    <div class="bx-faq-item">
      <button type="button" class="bx-faq-q">Does log file analysis replace the Search Console crawl stats report?</button>
      <div class="bx-faq-a"><p>No, the two complement each other. Search Console is a fast, convenient summary, while raw logs give the exact request level detail needed to investigate anything the summary only hints at.</p></div>
    </div>
    <div class="bx-faq-item">
      <button type="button" class="bx-faq-q">Do I need advanced Python experience to follow this guide?</button>
      <div class="bx-faq-a"><p>Basic comfort with Python and <a href="/python-and-pandas-seo-reporting/">pandas</a> is enough. The regular expression for parsing is the most complex single piece, and it can be copied and reused as is once a log format is confirmed.</p></div>
    </div>
  </div>

  <div class="bx-learn">
    <h2 id="what-we-learn-today">What We Learn Today</h2>
    <div class="bx-learn-grid">
      <div class="bx-learn-card"><span class="bx-learn-num">1</span><div><h4>Logs show ground truth</h4><p>Python log file analysis works from every actual request, not a sampled summary.</p></div></div>
      <div class="bx-learn-card"><span class="bx-learn-num">2</span><div><h4>Format comes before parsing</h4><p>Confirming the log format first avoids building a parser against the wrong pattern.</p></div></div>
      <div class="bx-learn-card"><span class="bx-learn-num">3</span><div><h4>User agent is just a claim</h4><p>Only a forward confirmed reverse DNS check actually verifies a request as real Googlebot.</p></div></div>
      <div class="bx-learn-card"><span class="bx-learn-num">4</span><div><h4>Frequency reveals priorities</h4><p>Grouping by path shows exactly which pages Google actually bothers to revisit.</p></div></div>
      <div class="bx-learn-card"><span class="bx-learn-num">5</span><div><h4>Status codes expose waste</h4><p>A high share of 404s or parameter URLs points straight at wasted crawl budget.</p></div></div>
      <div class="bx-learn-card"><span class="bx-learn-num">6</span><div><h4>Logs disappear fast</h4><p>Scheduling regular runs preserves history the server itself will not keep for long.</p></div></div>
    </div>
  </div>

  <div class="bx-ad">
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3931314195561246" crossorigin="anonymous"></script>
    <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-3931314195561246" data-ad-slot="4249015278" data-ad-format="auto" data-full-width-responsive="true"></ins>
    <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
  </div>

  <div class="bx-cta">
    <h3>Ready to See What Googlebot Is Really Doing?</h3>
    <p>Pair python log file analysis with a full crawl budget review to find exactly where Google's attention is going on your site. <a href="https://realpython.com/regex-python/" target="_blank" rel="noopener">Real Python's guide to regular expressions</a> is a good next stop for adapting the parser to a custom log format.</p>
    <div class="bx-cta-btns">
      <a href="/crawl-budget-explained/" target="_blank" rel="noopener">Read the Crawl Budget Guide</a>
      <a href="/understanding-crawl-stats-report/" target="_blank" rel="noopener" class="bx-cta-outline">Explore Crawl Stats Report</a>
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
