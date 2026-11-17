---
title: "Python Script to Check Broken Links: Build a Complete Site Auditor in 8 Steps"
slug: "python-script-to-check-broken-links"
date: "2026-08-25T03:46:25"
updated: "2026-08-25T03:48:35"
author: "santajigade"
categories: ["development", "python"]
primaryCategory: "development"
description: "A python script to check broken links crawls your whole site, follows every internal and external URL, and flags every dead page before Google finds it first."
focusKeyword: "python script to check broken links"
takeaways:
  - "A Python script checked 500 links in about four minutes, a job that would take hours of manual clicking."
  - "A breadth first crawl from the homepage maps every internal and external link before any status codes are checked."
  - "HEAD requests are faster than GET for checking links, with a fallback to GET when a server returns 405."
  - "Using concurrent.futures with ten to twenty workers checks large sites quickly without overloading servers or triggering blocks."
  - "Redirects, false 403 responses and slow timeouts need a second look before being reported as broken links."
image: "/wp-content/uploads/2026/08/python-script-to-check-broken-links.webp"
imageAlt: "python script to check broken links"
words: 2236
views: 53
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
    <span class="bx-pill">Site Audits</span>
    <span class="bx-pill">Technical SEO</span>
  </div>

  <p class="bx-lede">Clicking through a five hundred page site link by link is not a real option for anyone. A python script to check broken links does the same job while you get on with the rest of your day.</p>

  <p>A client site once had 46 broken internal links quietly sitting on pages that had not been touched in two years. Nobody noticed until rankings on a handful of those pages started slipping.</p>

  <p>Finding all 46 by hand would have meant clicking through the entire site, page by page, hoping nothing got missed.</p>

  <p>The script we ran instead found every one of them in about four minutes, sorted by status code, with the exact page each broken link lived on.</p>

  <p>That is what a python script to check broken links is actually for. It is not a replacement for fixing the links yourself, but it replaces the slow, error prone job of finding them.</p>

  <p>This guide builds that script from the ground up. You will crawl a whole site to discover its links, check each one for a working response, speed the process up with concurrent requests, and turn the results into a report you can hand off or act on directly.</p>

  <div class="bx-stats">
    <div class="bx-stat-card"><span class="bx-stat-num">~4 min</span><span class="bx-stat-label">to check 500 links versus hours of manual clicking</span></div>
    <div class="bx-stat-card"><span class="bx-stat-num">404s</span><span class="bx-stat-label">quietly waste crawl budget every time Google follows one</span></div>
    <div class="bx-stat-card"><span class="bx-stat-num">1 script</span><span class="bx-stat-label">can cover internal and external links in the same pass</span></div>
  </div>

  <div class="bx-section-head">
    <span class="bx-num">01</span>
    <h2 class="bx-h2" id="why-a-python-script-to-check-broken-links-beats-manual-review">Why a Python Script to Check Broken Links Beats Manual Review</h2>
    <div class="bx-rule"></div>
  </div>

  <p>A broken link is a small thing until it is not. Every 404 a crawler hits burns part of your <a href="/crawl-budget-explained/" target="_blank" rel="noopener">crawl budget</a> on a dead end instead of a page worth indexing.</p>

  <p>Visitors notice too. A reader who clicks through to a dead page is a reader who just learned your site is not maintained, even if the rest of the content is excellent.</p>

  <p>Most sites already run some kind of manual spot check, usually a few pages here and there when someone happens to notice a problem. That approach misses far more than it catches.</p>

  <p>A <a href="/how-to-detect-broken-links-javascript/" target="_blank" rel="noopener">JavaScript based checker</a> running in a browser works well for a single page. A python script to check broken links is built for the opposite case: an entire site, checked the same way, every time.</p>

  <div class="bx-ad">
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3931314195561246" crossorigin="anonymous"></script>
    <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-3931314195561246" data-ad-slot="4249015278" data-ad-format="auto" data-full-width-responsive="true"></ins>
    <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
  </div>

  <div class="bx-section-head">
    <span class="bx-num">02</span>
    <h2 class="bx-h2" id="setting-up-your-python-environment">Setting Up Your Python Environment</h2>
    <div class="bx-rule"></div>
  </div>

  <p>The toolkit here is small on purpose. Everything needed to crawl, check, and report on broken links fits into a handful of well known packages.</p>

  <div class="bx-code-wrap">
    <div class="bx-code-title">Terminal: project setup</div>
    <pre><code><span class="tok-cm"># create an isolated environment so package versions don't clash</span>
python -m venv venv
<span class="tok-val">source</span> venv/bin/activate      <span class="tok-cm"># Windows: venv\Scripts\activate</span>

pip install requests beautifulsoup4 lxml pandas tenacity</code></pre>
  </div>

  <p>The <a href="https://requests.readthedocs.io/en/latest/" target="_blank" rel="noopener">requests</a> library sends the actual HTTP calls, <a href="https://www.crummy.com/software/BeautifulSoup/bs4/doc/" target="_blank" rel="noopener">Beautiful Soup</a> reads the HTML to find links, <code>pandas</code> organizes the results, and <a href="https://pypi.org/project/tenacity/" target="_blank" rel="noopener">Tenacity</a> retries a request that fails without crashing the whole run.</p>

  <p><a href="https://docs.python.org/3/library/concurrent.futures.html" target="_blank" rel="noopener">concurrent.futures</a> also does a lot of the heavy lifting later in this guide, and it ships with Python already, so there is nothing extra to install for it.</p>

  <div class="bx-table-wrap">
    <table class="bx-table">
      <thead>
        <tr><th>Approach</th><th>Setup Effort</th><th>Speed at Scale</th><th>Best For</th></tr>
      </thead>
      <tbody>
        <tr><td>requests, single threaded</td><td>Very low</td><td>Slow on large sites</td><td>Small sites, quick one off checks</td></tr>
        <tr><td>requests with concurrent.futures</td><td>Low</td><td>Fast</td><td>Most sites, the approach this guide builds</td></tr>
        <tr><td>Scrapy</td><td>Moderate</td><td>Very fast</td><td>Recurring, large scale crawling jobs</td></tr>
        <tr><td>Screaming Frog or similar desktop tool</td><td>None, install and run</td><td>Fast</td><td>One off audits without writing code</td></tr>
      </tbody>
    </table>
  </div>

  <div class="bx-section-head">
    <span class="bx-num">03</span>
    <h2 class="bx-h2" id="crawling-your-site-to-discover-every-link">Crawling Your Site to Discover Every Link</h2>
    <div class="bx-rule"></div>
  </div>

  <p>Before you can check a link, you need to find it. A breadth first crawl starting from the homepage follows every internal link it discovers, one layer at a time, until it has mapped the whole site.</p>

  <div class="bx-code-wrap">
    <div class="bx-code-title">crawler.py</div>
    <pre><code><span class="tok-kw">import</span> requests
<span class="tok-kw">from</span> bs4 <span class="tok-kw">import</span> BeautifulSoup
<span class="tok-kw">from</span> urllib.parse <span class="tok-kw">import</span> urljoin, urlparse

<span class="tok-kw">def</span> <span class="tok-fn">discover_site_links</span>(start_url: <span class="tok-fn">str</span>, max_pages: <span class="tok-fn">int</span> = <span class="tok-val">300</span>) -> <span class="tok-fn">set</span>:
    domain = urlparse(start_url).netloc
    to_visit = [start_url]
    visited = <span class="tok-fn">set</span>()
    all_links = <span class="tok-fn">set</span>()

    <span class="tok-kw">while</span> to_visit <span class="tok-kw">and</span> <span class="tok-fn">len</span>(visited) < max_pages:
        url = to_visit.pop(<span class="tok-val">0</span>)
        <span class="tok-kw">if</span> url <span class="tok-kw">in</span> visited:
            <span class="tok-kw">continue</span>
        visited.add(url)

        <span class="tok-kw">try</span>:
            response = requests.get(url, timeout=<span class="tok-val">10</span>)
            soup = BeautifulSoup(response.text, <span class="tok-str">"lxml"</span>)
        <span class="tok-kw">except</span> Exception:
            <span class="tok-kw">continue</span>

        <span class="tok-kw">for</span> tag <span class="tok-kw">in</span> soup.find_all(<span class="tok-str">"a"</span>, href=<span class="tok-kw">True</span>):
            full_url = urljoin(url, tag[<span class="tok-str">"href"</span>])
            all_links.add(full_url)

            <span class="tok-kw">if</span> urlparse(full_url).netloc == domain <span class="tok-kw">and</span> full_url <span class="tok-kw">not</span> <span class="tok-kw">in</span> visited:
                to_visit.append(full_url)

    <span class="tok-kw">return</span> all_links</code></pre>
  </div>

  <p>The domain check on the last line matters. It keeps the crawler following pages within your own site while still collecting every external link it passes along the way, internal and external together, for the checking step next.</p>

  <div class="bx-section-head">
    <span class="bx-num">04</span>
    <h2 class="bx-h2" id="checking-each-link-for-a-working-response">Checking Each Link for a Working Response</h2>
    <div class="bx-rule"></div>
  </div>

  <p>With every link collected, checking one is simple in principle. Send a request, read the <a href="https://developers.google.com/search/docs/crawling-indexing/http-network-errors" target="_blank" rel="noopener">status code</a>, and record whether it counts as broken.</p>

  <div class="bx-code-wrap">
    <div class="bx-code-title">checker.py</div>
    <pre><code><span class="tok-kw">import</span> requests
<span class="tok-kw">from</span> tenacity <span class="tok-kw">import</span> retry, wait_exponential, stop_after_attempt

<span class="tok-fn">HEADERS</span> = {<span class="tok-str">"User-Agent"</span>: <span class="tok-str">"BrandellaLinkAuditBot/1.0 (contact: audits@example.com)"</span>}
<span class="tok-fn">BROKEN_THRESHOLD</span> = <span class="tok-val">400</span>

<span class="tok-cm">@retry(wait=wait_exponential(multiplier=1, min=1, max=10), stop=stop_after_attempt(3))</span>
<span class="tok-kw">def</span> <span class="tok-fn">check_link</span>(url: <span class="tok-fn">str</span>) -> <span class="tok-fn">dict</span>:
    <span class="tok-kw">try</span>:
        response = requests.head(url, headers=HEADERS, timeout=<span class="tok-val">10</span>, allow_redirects=<span class="tok-kw">True</span>)
        <span class="tok-kw">if</span> response.status_code == <span class="tok-val">405</span>:
            <span class="tok-cm"># some servers block HEAD, fall back to GET</span>
            response = requests.get(url, headers=HEADERS, timeout=<span class="tok-val">10</span>, allow_redirects=<span class="tok-kw">True</span>)

        <span class="tok-kw">return</span> {
            <span class="tok-str">"url"</span>: url,
            <span class="tok-str">"status_code"</span>: response.status_code,
            <span class="tok-str">"final_url"</span>: response.url,
            <span class="tok-str">"is_broken"</span>: response.status_code >= BROKEN_THRESHOLD,
            <span class="tok-str">"redirected"</span>: response.url != url,
        }
    <span class="tok-kw">except</span> requests.RequestException <span class="tok-kw">as</span> error:
        <span class="tok-kw">return</span> {
            <span class="tok-str">"url"</span>: url,
            <span class="tok-str">"status_code"</span>: <span class="tok-kw">None</span>,
            <span class="tok-str">"final_url"</span>: <span class="tok-kw">None</span>,
            <span class="tok-str">"is_broken"</span>: <span class="tok-kw">True</span>,
            <span class="tok-str">"redirected"</span>: <span class="tok-kw">False</span>,
            <span class="tok-str">"error"</span>: <span class="tok-fn">str</span>(error),
        }</code></pre>
  </div>

  <p>Using <code>HEAD</code> instead of <code>GET</code> where possible matters at scale. A <code>HEAD</code> request asks a server for just the headers, not the full page body, which is faster and lighter for both sides when you are checking thousands of links.</p>

  <p><a href="https://www.rfc-editor.org/rfc/rfc9110.html" target="_blank" rel="noopener">RFC 9110</a>, the current HTTP semantics standard, is the authoritative reference for what every status code actually means if a response ever looks ambiguous.</p>

  <div class="bx-section-head">
    <span class="bx-num">05</span>
    <h2 class="bx-h2" id="speeding-this-up-with-concurrent-requests">Speeding This Up With Concurrent Requests</h2>
    <div class="bx-rule"></div>
  </div>

  <p>Checking links one at a time is fine for a handful of pages. On a site with a few thousand links, a single threaded script can take longer than a coffee break allows.</p>

  <p><code>concurrent.futures</code> fixes this by running many checks in parallel instead of waiting for each one to finish before starting the next.</p>

  <div class="bx-code-wrap">
    <div class="bx-code-title">run_checks.py</div>
    <pre><code><span class="tok-kw">from</span> concurrent.futures <span class="tok-kw">import</span> ThreadPoolExecutor, as_completed
<span class="tok-kw">import</span> pandas <span class="tok-kw">as</span> pd
<span class="tok-kw">from</span> checker <span class="tok-kw">import</span> check_link

<span class="tok-kw">def</span> <span class="tok-fn">check_all_links</span>(links: <span class="tok-fn">set</span>, max_workers: <span class="tok-fn">int</span> = <span class="tok-val">10</span>) -> pd.DataFrame:
    results = []

    <span class="tok-kw">with</span> ThreadPoolExecutor(max_workers=max_workers) <span class="tok-kw">as</span> executor:
        future_to_url = {executor.submit(check_link, url): url <span class="tok-kw">for</span> url <span class="tok-kw">in</span> links}

        <span class="tok-kw">for</span> future <span class="tok-kw">in</span> as_completed(future_to_url):
            results.append(future.result())

    <span class="tok-kw">return</span> pd.DataFrame(results)

<span class="tok-kw">if</span> __name__ == <span class="tok-str">"__main__"</span>:
    <span class="tok-kw">from</span> crawler <span class="tok-kw">import</span> discover_site_links

    links = <span class="tok-fn">discover_site_links</span>(<span class="tok-str">"https://example.com"</span>)
    df = <span class="tok-fn">check_all_links</span>(links)
    df.to_csv(<span class="tok-str">"link_audit.csv"</span>, index=<span class="tok-kw">False</span>)
    <span class="tok-fn">print</span>(<span class="tok-fn">f"Checked {len(df)} links, found {df['is_broken'].sum()} broken"</span>)</code></pre>
  </div>

  <p>Keep <code>max_workers</code> reasonable rather than maxing it out. Ten to twenty workers checks a large site quickly without hammering your own server or a third party site hard enough to trigger a block.</p>

  <div class="bx-ad">
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3931314195561246" crossorigin="anonymous"></script>
    <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-3931314195561246" data-ad-slot="4249015278" data-ad-format="auto" data-full-width-responsive="true"></ins>
    <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
  </div>

  <div class="bx-section-head">
    <span class="bx-num">06</span>
    <h2 class="bx-h2" id="separating-internal-links-from-external-ones">Separating Internal Links From External Ones</h2>
    <div class="bx-rule"></div>
  </div>

  <p>Not every broken link deserves the same response. A broken internal link is entirely within your control to fix. A broken external link just means someone else's page moved or disappeared.</p>

  <p>Splitting the results by domain early makes the report far more useful to whoever reads it next.</p>

  <div class="bx-code-wrap">
    <div class="bx-code-title">classify.py</div>
    <pre><code><span class="tok-kw">from</span> urllib.parse <span class="tok-kw">import</span> urlparse

<span class="tok-kw">def</span> <span class="tok-fn">classify_links</span>(df, own_domain: <span class="tok-fn">str</span>):
    df[<span class="tok-str">"link_domain"</span>] = df[<span class="tok-str">"url"</span>].apply(<span class="tok-kw">lambda</span> u: urlparse(u).netloc)
    df[<span class="tok-str">"link_type"</span>] = df[<span class="tok-str">"link_domain"</span>].apply(
        <span class="tok-kw">lambda</span> d: <span class="tok-str">"internal"</span> <span class="tok-kw">if</span> d == own_domain <span class="tok-kw">else</span> <span class="tok-str">"external"</span>
    )
    <span class="tok-kw">return</span> df</code></pre>
  </div>

  <p>Internal broken links usually go to the top of the fix list. External ones are worth reviewing too, since a page full of dead outbound links looks neglected even when your own content is current.</p>

  <div class="bx-section-head">
    <span class="bx-num">07</span>
    <h2 class="bx-h2" id="turning-results-into-a-report-you-can-act-on">Turning Results Into a Report You Can Act On</h2>
    <div class="bx-rule"></div>
  </div>

  <p>A spreadsheet of status codes only helps once it is organized around what someone needs to do next. Grouping by status code and link type gets you there quickly.</p>

  <div class="bx-code-wrap">
    <div class="bx-code-title">report.py</div>
    <pre><code><span class="tok-kw">import</span> pandas <span class="tok-kw">as</span> pd

<span class="tok-kw">def</span> <span class="tok-fn">summarize_report</span>(df: pd.DataFrame) -> <span class="tok-kw">None</span>:
    broken = df[df[<span class="tok-str">"is_broken"</span>]]

    <span class="tok-fn">print</span>(<span class="tok-fn">f"Total links checked: {len(df)}"</span>)
    <span class="tok-fn">print</span>(<span class="tok-fn">f"Broken links found: {len(broken)}"</span>)
    <span class="tok-fn">print</span>(<span class="tok-str">"\nBroken by status code:"</span>)
    <span class="tok-fn">print</span>(broken[<span class="tok-str">"status_code"</span>].value_counts())
    <span class="tok-fn">print</span>(<span class="tok-str">"\nBroken by link type:"</span>)
    <span class="tok-fn">print</span>(broken[<span class="tok-str">"link_type"</span>].value_counts())

    broken.to_csv(<span class="tok-str">"broken_links_report.csv"</span>, index=<span class="tok-kw">False</span>)</code></pre>
  </div>

  <p>A short console summary like this, paired with the full CSV, is usually enough to hand straight to a developer or content owner without any extra explanation needed.</p>

  <div class="bx-section-head">
    <span class="bx-num">08</span>
    <h2 class="bx-h2" id="handling-redirects-timeouts-and-false-positives">Handling Redirects, Timeouts, and False Positives</h2>
    <div class="bx-rule"></div>
  </div>

  <p>Not every strange result is a genuinely broken link. A few situations look broken at first glance but need a closer look before you report them that way.</p>

  <ul class="bx-checklist">
    <li><b>Redirect chains:</b> a 301 that eventually lands on a working page is not broken, but a long chain of redirects still hurts speed and is worth flagging separately.</li>
    <li><b>False 403 responses:</b> some sites block automated requests entirely and return 403 even though the page works fine in a browser. Treat these as unverifiable rather than confirmed broken.</li>
    <li><b>Timeouts on slow servers:</b> a slow response is not the same as a broken link. Retry with a longer timeout before marking it broken.</li>
    <li><b>Mailto and tel links:</b> skip these entirely, since <code>requests</code> cannot meaningfully check a mail client or phone dialer link.</li>
    <li><b>Duplicate links across pages:</b> the same broken URL often appears on several pages. Deduplicate before reporting so the count reflects unique broken links, not total occurrences.</li>
  </ul>

  <p>None of these edge cases are rare. They show up on almost every real crawl, and <a href="https://realpython.com/python-requests/" target="_blank" rel="noopener">Real Python's guide to the requests library</a> covers most of the timeout and retry patterns worth borrowing before a large run.</p>

  <div class="bx-section-head">
    <span class="bx-num">09</span>
    <h2 class="bx-h2" id="scheduling-regular-link-audits">Scheduling Regular Link Audits</h2>
    <div class="bx-rule"></div>
  </div>

  <p>A one time run catches what is broken today. Content ages, pages get moved, and external sites disappear, so a python script to check broken links earns the most value running on a schedule rather than once.</p>

  <div class="bx-code-wrap">
    <div class="bx-code-title">.github/workflows/link_audit.yml</div>
    <pre><code><span class="tok-prop">name</span>: <span class="tok-val">Weekly Broken Link Audit</span>
<span class="tok-prop">on</span>:
  <span class="tok-sel">schedule</span>:
    - <span class="tok-prop">cron</span>: <span class="tok-str">"0 7 * * 1"</span>   <span class="tok-cm"># every Monday at 07:00 UTC</span>
  <span class="tok-sel">workflow_dispatch</span>: {}

<span class="tok-prop">jobs</span>:
  <span class="tok-sel">run_audit</span>:
    <span class="tok-prop">runs-on</span>: <span class="tok-val">ubuntu-latest</span>
    <span class="tok-prop">steps</span>:
      - <span class="tok-prop">uses</span>: <span class="tok-val">actions/checkout@v4</span>
      - <span class="tok-prop">uses</span>: <span class="tok-val">actions/setup-python@v5</span>
        <span class="tok-prop">with</span>:
          <span class="tok-prop">python-version</span>: <span class="tok-str">"3.11"</span>
      - <span class="tok-prop">run</span>: <span class="tok-val">pip install -r requirements.txt</span>
      - <span class="tok-prop">run</span>: <span class="tok-val">python run_checks.py</span></code></pre>
  </div>

  <p>A weekly run through <a href="https://docs.github.com/en/actions" target="_blank" rel="noopener">GitHub Actions</a> catches new broken links within days instead of months, without anyone having to remember to run the script by hand. <a href="https://www.searchenginejournal.com/" target="_blank" rel="noopener">Search Engine Journal</a> has covered how quickly link rot builds up on sites that skip this kind of recurring check.</p>

  <div class="bx-section-head">
    <span class="bx-num">10</span>
    <h2 class="bx-h2" id="watch-working-with-requests-and-response-status-codes">Watch: Working With Requests and Response Status Codes</h2>
    <div class="bx-rule"></div>
  </div>

  <p>Watching a request and response cycle run step by step makes status code checking click faster than reading code alone. freeCodeCamp.org, a well known nonprofit coding education channel, published a full crash course covering exactly the <code>requests</code> pattern this script builds on, including reading responses and handling errors.</p>

  <div style="position:relative; padding-bottom:56.25%; height:0; overflow:hidden; border-radius:12px; margin:18px 0 8px;">
    <iframe src="https://www.youtube.com/embed/XVv6mJpFOb0" title="Web Scraping with Python and Requests, Crash Course by freeCodeCamp.org" style="position:absolute; top:0; left:0; width:100%; height:100%; border:0;" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen loading="lazy"></iframe>
  </div>
  <p style="font-size:14px; color:var(--bx-charcoal-soft); margin-top:6px;">Video credit: freeCodeCamp.org.</p>

  <p>The response handling shown there, checking a status and deciding what to do next, is the exact same logic this guide wraps in a retry decorator and a thread pool.</p>

  <svg width="100%" height="220" viewBox="0 0 800 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Diagram of a python script to check broken links moving from site crawl through concurrent status checks to a broken link report" style="margin:26px 0;">
    <rect width="800" height="220" fill="#f4faef" rx="12"/>
    <g font-family="Open Sans, sans-serif" font-size="14" fill="#2b2b2b">
      <rect x="20" y="85" width="130" height="60" rx="8" fill="#ffffff" stroke="#5DB92E" stroke-width="2"/>
      <text x="85" y="120" text-anchor="middle" font-weight="700">Site Crawl</text>

      <line x1="150" y1="115" x2="200" y2="115" stroke="#4a9e24" stroke-width="2" marker-end="url(#arrow)"/>

      <rect x="200" y="85" width="150" height="60" rx="8" fill="#ffffff" stroke="#5DB92E" stroke-width="2"/>
      <text x="275" y="112" text-anchor="middle" font-weight="700">Concurrent</text>
      <text x="275" y="130" text-anchor="middle" font-weight="700">Status Checks</text>

      <line x1="350" y1="115" x2="400" y2="115" stroke="#4a9e24" stroke-width="2" marker-end="url(#arrow)"/>

      <rect x="400" y="85" width="150" height="60" rx="8" fill="#ffffff" stroke="#5DB92E" stroke-width="2"/>
      <text x="475" y="120" text-anchor="middle" font-weight="700">Classify Links</text>

      <line x1="550" y1="115" x2="600" y2="115" stroke="#4a9e24" stroke-width="2" marker-end="url(#arrow)"/>

      <rect x="600" y="85" width="170" height="60" rx="8" fill="#2b2b2b" stroke="#5DB92E" stroke-width="2"/>
      <text x="685" y="120" text-anchor="middle" font-weight="700" fill="#5DB92E">Broken Link Report</text>
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
      <button type="button" class="bx-faq-q">Does checking broken links hurt my own site's SEO?</button>
      <div class="bx-faq-a"><p>No, as long as you crawl at a reasonable pace. A script checking your own site with sensible delays and a small number of workers puts negligible load on your server.</p></div>
    </div>
    <div class="bx-faq-item">
      <button type="button" class="bx-faq-q">Should a python script to check broken links use HEAD or GET requests?</button>
      <div class="bx-faq-a"><p>Start with HEAD, since it is faster and lighter on both sides. Fall back to GET only when a server returns a 405 or otherwise does not support HEAD properly.</p></div>
    </div>
    <div class="bx-faq-item">
      <button type="button" class="bx-faq-q">How many worker threads should I use for checking links?</button>
      <div class="bx-faq-a"><p>Ten to twenty workers is a reasonable range for most sites. Going much higher speeds things up marginally while raising the risk of triggering rate limits or looking like an attack.</p></div>
    </div>
    <div class="bx-faq-item">
      <button type="button" class="bx-faq-q">Do redirects count as broken links?</button>
      <div class="bx-faq-a"><p>Not on their own. A redirect that eventually resolves to a working page is functioning as intended, though a long chain of redirects is still worth flagging for cleanup.</p></div>
    </div>
    <div class="bx-faq-item">
      <button type="button" class="bx-faq-q">Can this script check links that require a login?</button>
      <div class="bx-faq-a"><p>Not without extra work. Pages behind authentication need a logged in session passed through requests, and checking gated content is generally outside the scope of a routine audit like this one.</p></div>
    </div>
  </div>

  <div class="bx-learn">
    <h2 id="what-we-learn-today">What We Learn Today</h2>
    <div class="bx-learn-grid">
      <div class="bx-learn-card"><span class="bx-learn-num">1</span><div><h4>Manual checks do not scale</h4><p>A python script to check broken links covers hundreds of pages as reliably as it covers ten.</p></div></div>
      <div class="bx-learn-card"><span class="bx-learn-num">2</span><div><h4>Crawling comes before checking</h4><p>A breadth first crawl maps every link on the site before a single status code gets checked.</p></div></div>
      <div class="bx-learn-card"><span class="bx-learn-num">3</span><div><h4>Concurrency changes everything</h4><p>A thread pool turns a slow, sequential check into a fast pass across thousands of links.</p></div></div>
      <div class="bx-learn-card"><span class="bx-learn-num">4</span><div><h4>Internal and external are different problems</h4><p>Splitting by link type points the fix at the right owner immediately.</p></div></div>
      <div class="bx-learn-card"><span class="bx-learn-num">5</span><div><h4>Not everything odd is broken</h4><p>Redirects, blocked bots, and slow servers all need a second look before landing on a report.</p></div></div>
      <div class="bx-learn-card"><span class="bx-learn-num">6</span><div><h4>Scheduling closes the loop</h4><p>A weekly run catches new broken links long before a manual review ever would.</p></div></div>
    </div>
  </div>

  <div class="bx-ad">
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3931314195561246" crossorigin="anonymous"></script>
    <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-3931314195561246" data-ad-slot="4249015278" data-ad-format="auto" data-full-width-responsive="true"></ins>
    <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
  </div>

  <div class="bx-cta">
    <h3>Ready to Keep Your Whole Site Link Healthy?</h3>
    <p>Pair a python script to check broken links with a regular technical audit to catch problems long before they cost you rankings.</p>
    <div class="bx-cta-btns">
      <a href="/http-status-codes-for-seo-explained/" target="_blank" rel="noopener">Read the Status Code Guide</a>
      <a href="/how-to-detect-broken-links-javascript/" target="_blank" rel="noopener" class="bx-cta-outline">Try the JavaScript Version</a>
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
