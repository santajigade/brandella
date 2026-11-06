---
title: "Web Scraper for Competitor Content Audits: Build a Complete Python Tool in 9 Steps"
slug: "web-scraper-for-competitor-content-audits"
date: "2026-08-25T03:42:15"
updated: "2026-08-25T03:43:27"
author: "santajigade"
categories: ["development", "python"]
primaryCategory: "development"
description: "A practical web scraper for competitor content audits pulls titles, word counts, headings, and publish dates from rival pages so you can compare content at scale."
focusKeyword: "web scraper for competitor content audits"
image: "/wp-content/uploads/2026/08/web-scraper-for-competitor-content-audits.webp"
imageAlt: "web scraper for competitor content audits"
words: 2691
views: 43
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

.bx-tool { background: var(--bx-dark); border-radius: 14px; padding: 30px; margin: 26px 0 32px; color: #e8ede9; }
.bx-tool h3 { font-family: var(--bx-disp); color: #fff; font-size: 21px; margin: 0 0 6px; }
.bx-tool p.bx-tool-sub { color: #a9b4ac; font-size: 15px; margin: 0 0 20px; }
.bx-chip-row { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 18px; }
.bx-chip {
  font-family: var(--bx-disp); font-size: 14px; font-weight: 600; color: #cfd8d2;
  background: #2c343a; border: 1px solid #3a444b; padding: 8px 16px; border-radius: 30px; cursor: pointer;
}
.bx-chip.active { background: var(--bx-green); border-color: var(--bx-green); color: #12210a; }
.bx-stepper { display: flex; align-items: center; gap: 14px; margin-bottom: 22px; }
.bx-stepper button {
  width: 36px; height: 36px; border-radius: 50%; border: 1px solid #3a444b; background: #2c343a;
  color: #fff; font-size: 18px; cursor: pointer; font-family: var(--bx-disp);
}
.bx-stepper span { font-family: var(--bx-disp); font-weight: 700; font-size: 18px; min-width: 130px; text-align: center; }
.bx-tool-output { background: #171d21; border-radius: 10px; padding: 20px; display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
.bx-tool-output .bx-out-num { font-family: var(--bx-disp); font-weight: 800; font-size: 26px; color: var(--bx-green); display: block; }
.bx-tool-output .bx-out-label { font-size: 13px; color: #9aa79f; }
@media (max-width: 640px) { .bx-tool-output { grid-template-columns: 1fr; } }

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
    <span class="bx-pill">Web Scraping</span>
    <span class="bx-pill">Competitor Research</span>
  </div>

  <p class="bx-lede">Checking twenty competitor pages by hand means twenty open tabs, twenty word counts, and twenty chances to lose track of what you already reviewed. A web scraper for competitor content audits does the same job in the time it takes to make a coffee.</p>

  <p>A client once asked us to review how forty competitor blog posts compared to their own content on word count, heading structure, and publish dates. Doing that by hand would have meant a full day of copying numbers into a spreadsheet.</p>

  <p>The script we actually used finished the same forty pages in about ninety seconds, and it did not miss a single page or mistype a word count along the way.</p>

  <p>That is the real value of a web scraper for competitor content audits. It is not about replacing your judgment on what makes content good.</p>

  <p>It is about removing the copy and paste work so you can spend your time on the analysis instead of the data collection.</p>

  <p>This guide builds a complete, respectful scraper in Python. You will fetch pages politely, respect robots.txt, pull the metrics that actually matter for a content audit, crawl a whole competitor sitemap automatically, and turn the results into a report you can act on.</p>

  <div class="bx-stats">
    <div class="bx-stat-card"><span class="bx-stat-num">~90 sec</span><span class="bx-stat-label">to audit 40 competitor pages versus most of a working day by hand</span></div>
    <div class="bx-stat-card"><span class="bx-stat-num">6 metrics</span><span class="bx-stat-label">pulled automatically per page: title, word count, headings, links, images, schema</span></div>
    <div class="bx-stat-card"><span class="bx-stat-num">1 rule</span><span class="bx-stat-label">that matters most: always check robots.txt before you crawl anything</span></div>
  </div>

  <div class="bx-section-head">
    <span class="bx-num">01</span>
    <h2 class="bx-h2" id="why-a-web-scraper-for-competitor-content-audits-beats-manual-review">Why a Web Scraper for Competitor Content Audits Beats Manual Review</h2>
    <div class="bx-rule"></div>
  </div>

  <p>A proper <a href="/content-audit-explained-improve-rankings/" target="_blank" rel="noopener">content audit</a> looks at dozens or hundreds of pages across word count, heading structure, freshness, and media use. Reviewing that many pages by hand is slow, and slow work tends to get inconsistent.</p>

  <p>One page gets a careful word count. The next gets an estimate because you are tired of counting. That inconsistency quietly wrecks the comparison you are trying to make.</p>

  <p>A script treats every page the same way, every time. It counts words the same way on page one and page one hundred, and it never skips a field because it got bored.</p>

  <p><a href="https://www.searchenginejournal.com/" target="_blank" rel="noopener">Search Engine Journal</a> and <a href="https://searchengineland.com/" target="_blank" rel="noopener">Search Engine Land</a> both publish regular guidance on running content audits at scale, and consistency is the theme that comes up again and again.</p>

  <p>There is also a coverage argument. A person can realistically review twenty or thirty competitor pages in a sitting before quality drops.</p>

  <p>A script can work through an entire competitor sitemap, which might be five hundred pages, without losing accuracy on page four hundred and ninety nine.</p>

  <div class="bx-ad">
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3931314195561246" crossorigin="anonymous"></script>
    <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-3931314195561246" data-ad-slot="4249015278" data-ad-format="auto" data-full-width-responsive="true"></ins>
    <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
  </div>

  <div class="bx-section-head">
    <span class="bx-num">02</span>
    <h2 class="bx-h2" id="setting-up-your-python-scraping-environment">Setting Up Your Python Scraping Environment</h2>
    <div class="bx-rule"></div>
  </div>

  <p>Keep the toolkit small. You need a way to fetch pages, a way to parse the HTML, a place to hold results, and a retry layer for the occasional slow or failed request.</p>

  <div class="bx-code-wrap">
    <div class="bx-code-title">Terminal: project setup</div>
    <pre><code><span class="tok-cm"># create an isolated environment so package versions don't clash</span>
python -m venv venv
<span class="tok-val">source</span> venv/bin/activate      <span class="tok-cm"># Windows: venv\Scripts\activate</span>

pip install requests beautifulsoup4 lxml pandas tenacity</code></pre>
  </div>

  <p>The <a href="https://requests.readthedocs.io/en/latest/" target="_blank" rel="noopener">requests</a> library handles the HTTP calls, <a href="https://www.crummy.com/software/BeautifulSoup/bs4/doc/" target="_blank" rel="noopener">Beautiful Soup</a> parses the returned HTML, <code>lxml</code> makes that parsing fast, <code>pandas</code> holds and organizes the results, and <a href="https://pypi.org/project/tenacity/" target="_blank" rel="noopener">Tenacity</a> retries a request that fails without crashing the whole run.</p>

  <p>Set a clear <code>User-Agent</code> header before you send a single request. Many sites use it to identify who is visiting, and an honest, identifiable value is part of scraping politely rather than pretending to be a regular browser.</p>

  <div class="bx-code-wrap">
    <div class="bx-code-title">config.py</div>
    <pre><code><span class="tok-fn">HEADERS</span> = {
    <span class="tok-str">"User-Agent"</span>: <span class="tok-str">"BrandellaContentAuditBot/1.0 (contact: audits@example.com)"</span>
}
<span class="tok-fn">REQUEST_DELAY_SECONDS</span> = <span class="tok-val">1.5</span>
<span class="tok-fn">REQUEST_TIMEOUT</span> = <span class="tok-val">15</span></code></pre>
  </div>

  <div class="bx-section-head">
    <span class="bx-num">03</span>
    <h2 class="bx-h2" id="reading-robots-txt-before-you-crawl-a-single-page">Reading robots.txt Before You Crawl a Single Page</h2>
    <div class="bx-rule"></div>
  </div>

  <p>Every respectful web scraper for competitor content audits starts by checking what the site actually allows. The <a href="https://www.rfc-editor.org/rfc/rfc9309.html" target="_blank" rel="noopener">Robots Exclusion Protocol</a> is a published standard, and <code>robots.txt</code> is how a site tells automated tools which paths are off limits.</p>

  <p>Python's standard library already includes a parser for this, so there is no reason to skip the check.</p>

  <div class="bx-code-wrap">
    <div class="bx-code-title">robots_check.py</div>
    <pre><code><span class="tok-kw">from</span> urllib.robotparser <span class="tok-kw">import</span> RobotFileParser
<span class="tok-kw">from</span> urllib.parse <span class="tok-kw">import</span> urljoin

<span class="tok-kw">def</span> <span class="tok-fn">can_fetch</span>(base_url: <span class="tok-fn">str</span>, path: <span class="tok-fn">str</span>, user_agent: <span class="tok-fn">str</span> = <span class="tok-str">"*"</span>) -> <span class="tok-fn">bool</span>:
    parser = RobotFileParser()
    parser.set_url(urljoin(base_url, <span class="tok-str">"/robots.txt"</span>))
    parser.read()
    <span class="tok-kw">return</span> parser.can_fetch(user_agent, path)

<span class="tok-kw">if</span> __name__ == <span class="tok-str">"__main__"</span>:
    site = <span class="tok-str">"https://example.com"</span>
    target = <span class="tok-str">"https://example.com/blog/sample-post"</span>
    <span class="tok-kw">if</span> <span class="tok-fn">can_fetch</span>(site, target):
        <span class="tok-fn">print</span>(<span class="tok-str">"Allowed, proceed with the audit"</span>)
    <span class="tok-kw">else</span>:
        <span class="tok-fn">print</span>(<span class="tok-str">"Blocked by robots.txt, skip this path"</span>)</code></pre>
  </div>

  <p>Build this check into every audit script from the start rather than adding it later. A site that disallows crawling on certain paths, like login areas or internal search results, is telling you plainly where the boundary sits.</p>

  <ul class="bx-checklist">
    <li><b>Check robots.txt first:</b> run <code>can_fetch</code> before requesting any URL, not after you notice a problem.</li>
    <li><b>Identify yourself honestly:</b> use a real <code>User-Agent</code> string with a contact method, not a spoofed browser signature.</li>
    <li><b>Add real delays:</b> a second or two between requests protects the target site and your own IP address from getting flagged.</li>
    <li><b>Stay on public pages:</b> never attempt to scrape content behind a login wall or paywall for a competitor audit.</li>
    <li><b>Cache what you already fetched:</b> save responses locally so a rerun does not hit the same server twice for no reason.</li>
  </ul>

  <div class="bx-section-head">
    <span class="bx-num">04</span>
    <h2 class="bx-h2" id="building-the-core-scraper-function">Building the Core Scraper Function</h2>
    <div class="bx-rule"></div>
  </div>

  <p>With permission checked and headers set, the core function is short. It fetches a page, retries on a transient failure, and hands the HTML to BeautifulSoup for parsing.</p>

  <div class="bx-code-wrap">
    <div class="bx-code-title">scraper.py</div>
    <pre><code><span class="tok-kw">import</span> time
<span class="tok-kw">import</span> requests
<span class="tok-kw">from</span> bs4 <span class="tok-kw">import</span> BeautifulSoup
<span class="tok-kw">from</span> tenacity <span class="tok-kw">import</span> retry, wait_exponential, stop_after_attempt
<span class="tok-kw">from</span> config <span class="tok-kw">import</span> HEADERS, REQUEST_DELAY_SECONDS, REQUEST_TIMEOUT

<span class="tok-cm">@retry(wait=wait_exponential(multiplier=1, min=2, max=20), stop=stop_after_attempt(4))</span>
<span class="tok-kw">def</span> <span class="tok-fn">fetch_page</span>(url: <span class="tok-fn">str</span>) -> BeautifulSoup:
    response = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    time.sleep(REQUEST_DELAY_SECONDS)   <span class="tok-cm"># be polite between requests</span>
    <span class="tok-kw">return</span> BeautifulSoup(response.text, <span class="tok-str">"lxml"</span>)

<span class="tok-kw">def</span> <span class="tok-fn">extract_basics</span>(soup: BeautifulSoup, url: <span class="tok-fn">str</span>) -> <span class="tok-fn">dict</span>:
    title = soup.title.get_text(strip=<span class="tok-kw">True</span>) <span class="tok-kw">if</span> soup.title <span class="tok-kw">else</span> <span class="tok-str">""</span>
    meta_desc_tag = soup.find(<span class="tok-str">"meta"</span>, attrs={<span class="tok-str">"name"</span>: <span class="tok-str">"description"</span>})
    meta_description = meta_desc_tag[<span class="tok-str">"content"</span>] <span class="tok-kw">if</span> meta_desc_tag <span class="tok-kw">else</span> <span class="tok-str">""</span>
    h1 = soup.find(<span class="tok-str">"h1"</span>)
    body_text = soup.get_text(separator=<span class="tok-str">" "</span>, strip=<span class="tok-kw">True</span>)

    <span class="tok-kw">return</span> {
        <span class="tok-str">"url"</span>: url,
        <span class="tok-str">"title"</span>: title,
        <span class="tok-str">"meta_description"</span>: meta_description,
        <span class="tok-str">"h1"</span>: h1.get_text(strip=<span class="tok-kw">True</span>) <span class="tok-kw">if</span> h1 <span class="tok-kw">else</span> <span class="tok-str">""</span>,
        <span class="tok-str">"word_count"</span>: <span class="tok-fn">len</span>(body_text.split()),
    }</code></pre>
  </div>

  <p>The retry decorator matters more than it looks. A single competitor site will occasionally hand back a slow response or a brief server error, and without a retry layer that one failure can quietly drop a page from your whole audit.</p>

  <div class="bx-section-head">
    <span class="bx-num">05</span>
    <h2 class="bx-h2" id="extracting-the-metrics-that-actually-matter-for-the-audit">Extracting the Metrics That Actually Matter for the Audit</h2>
    <div class="bx-rule"></div>
  </div>

  <p>A web scraper for competitor content audits earns its real value once you look past word count alone. A content audit gets useful when you add heading structure, link counts, media presence, and whether the page carries schema markup.</p>

  <div class="bx-code-wrap">
    <div class="bx-code-title">metrics.py</div>
    <pre><code><span class="tok-kw">def</span> <span class="tok-fn">extract_content_metrics</span>(soup, url: <span class="tok-fn">str</span>, domain: <span class="tok-fn">str</span>) -> <span class="tok-fn">dict</span>:
    headings = {
        <span class="tok-str">"h1_count"</span>: <span class="tok-fn">len</span>(soup.find_all(<span class="tok-str">"h1"</span>)),
        <span class="tok-str">"h2_count"</span>: <span class="tok-fn">len</span>(soup.find_all(<span class="tok-str">"h2"</span>)),
        <span class="tok-str">"h3_count"</span>: <span class="tok-fn">len</span>(soup.find_all(<span class="tok-str">"h3"</span>)),
    }

    links = soup.find_all(<span class="tok-str">"a"</span>, href=<span class="tok-kw">True</span>)
    internal_links = [a <span class="tok-kw">for</span> a <span class="tok-kw">in</span> links <span class="tok-kw">if</span> domain <span class="tok-kw">in</span> a[<span class="tok-str">"href"</span>]]
    external_links = [a <span class="tok-kw">for</span> a <span class="tok-kw">in</span> links <span class="tok-kw">if</span> domain <span class="tok-kw">not</span> <span class="tok-kw">in</span> a[<span class="tok-str">"href"</span>] <span class="tok-kw">and</span> a[<span class="tok-str">"href"</span>].startswith(<span class="tok-str">"http"</span>)]

    schema_tags = soup.find_all(<span class="tok-str">"script"</span>, type=<span class="tok-str">"application/ld+json"</span>)

    <span class="tok-kw">return</span> {
        <span class="tok-str">"url"</span>: url,
        **headings,
        <span class="tok-str">"internal_link_count"</span>: <span class="tok-fn">len</span>(internal_links),
        <span class="tok-str">"external_link_count"</span>: <span class="tok-fn">len</span>(external_links),
        <span class="tok-str">"image_count"</span>: <span class="tok-fn">len</span>(soup.find_all(<span class="tok-str">"img"</span>)),
        <span class="tok-str">"has_schema_markup"</span>: <span class="tok-fn">len</span>(schema_tags) > <span class="tok-val">0</span>,
    }</code></pre>
  </div>

  <div class="bx-table-wrap">
    <table class="bx-table">
      <thead>
        <tr><th>Metric</th><th>What It Reveals</th><th>Why It Matters for the Audit</th></tr>
      </thead>
      <tbody>
        <tr><td>Word count</td><td>Depth of coverage on the topic</td><td>Flags thin pages that may need expanding</td></tr>
        <tr><td>Heading structure</td><td>How the page is organized</td><td>Reveals scannability and topic breakdown</td></tr>
        <tr><td>Internal and external links</td><td>How the page connects to other content</td><td>Shows linking patterns worth matching or beating</td></tr>
        <tr><td>Image count</td><td>How visual the page is</td><td>Highlights gaps in media richness</td></tr>
        <tr><td>Schema markup</td><td>Whether structured data is present</td><td>Signals technical SEO maturity</td></tr>
      </tbody>
    </table>
  </div>

  <div class="bx-section-head">
    <span class="bx-num">06</span>
    <h2 class="bx-h2" id="crawling-an-entire-competitor-sitemap-automatically">Crawling an Entire Competitor Sitemap Automatically</h2>
    <div class="bx-rule"></div>
  </div>

  <p>A single page tells you very little about a competitor's overall content strategy. The real value of a web scraper for competitor content audits shows up once you point it at their whole sitemap.</p>

  <p>Most sites publish one at a predictable path, so pulling every blog URL is usually a short step.</p>

  <div class="bx-code-wrap">
    <div class="bx-code-title">crawl_sitemap.py</div>
    <pre><code><span class="tok-kw">import</span> requests
<span class="tok-kw">import</span> pandas <span class="tok-kw">as</span> pd
<span class="tok-kw">from</span> bs4 <span class="tok-kw">import</span> BeautifulSoup
<span class="tok-kw">from</span> scraper <span class="tok-kw">import</span> fetch_page, extract_basics
<span class="tok-kw">from</span> metrics <span class="tok-kw">import</span> extract_content_metrics
<span class="tok-kw">from</span> config <span class="tok-kw">import</span> HEADERS

<span class="tok-kw">def</span> <span class="tok-fn">get_sitemap_urls</span>(sitemap_url: <span class="tok-fn">str</span>) -> <span class="tok-fn">list</span>:
    response = requests.get(sitemap_url, headers=HEADERS, timeout=<span class="tok-val">15</span>)
    soup = BeautifulSoup(response.text, <span class="tok-str">"xml"</span>)
    <span class="tok-kw">return</span> [loc.get_text() <span class="tok-kw">for</span> loc <span class="tok-kw">in</span> soup.find_all(<span class="tok-str">"loc"</span>)]

<span class="tok-kw">def</span> <span class="tok-fn">audit_competitor</span>(sitemap_url: <span class="tok-fn">str</span>, domain: <span class="tok-fn">str</span>, limit: <span class="tok-fn">int</span> = <span class="tok-val">50</span>) -> pd.DataFrame:
    urls = <span class="tok-fn">get_sitemap_urls</span>(sitemap_url)[:limit]
    rows = []

    <span class="tok-kw">for</span> url <span class="tok-kw">in</span> urls:
        <span class="tok-kw">try</span>:
            soup = <span class="tok-fn">fetch_page</span>(url)
            basics = <span class="tok-fn">extract_basics</span>(soup, url)
            metrics = <span class="tok-fn">extract_content_metrics</span>(soup, url, domain)
            rows.append({**basics, **metrics})
        <span class="tok-kw">except</span> Exception <span class="tok-kw">as</span> error:
            <span class="tok-fn">print</span>(<span class="tok-fn">f"Skipped {url}: {error}"</span>)

    <span class="tok-kw">return</span> pd.DataFrame(rows)

<span class="tok-kw">if</span> __name__ == <span class="tok-str">"__main__"</span>:
    df = <span class="tok-fn">audit_competitor</span>(<span class="tok-str">"https://competitor.com/sitemap.xml"</span>, <span class="tok-str">"competitor.com"</span>)
    df.to_csv(<span class="tok-str">"competitor_audit.csv"</span>, index=<span class="tok-kw">False</span>)
    <span class="tok-fn">print</span>(<span class="tok-fn">f"Audited {len(df)} pages"</span>)</code></pre>
  </div>

  <p>Notice the <code>try</code> and <code>except</code> block wrapped around every page. A single broken page should never take down a fifty page audit, so one failure gets logged and the crawl moves on.</p>

  <div class="bx-ad">
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3931314195561246" crossorigin="anonymous"></script>
    <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-3931314195561246" data-ad-slot="4249015278" data-ad-format="auto" data-full-width-responsive="true"></ins>
    <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
  </div>

  <div class="bx-section-head">
    <span class="bx-num">07</span>
    <h2 class="bx-h2" id="turning-raw-data-into-an-actual-content-audit-report">Turning Raw Data Into an Actual Content Audit Report</h2>
    <div class="bx-rule"></div>
  </div>

  <p>A CSV full of numbers is not a report yet. The last step is comparing what you found against your own content, or against the other competitors you audited.</p>

  <div class="bx-code-wrap">
    <div class="bx-code-title">report.py</div>
    <pre><code><span class="tok-kw">import</span> pandas <span class="tok-kw">as</span> pd

<span class="tok-kw">def</span> <span class="tok-fn">summarize_audit</span>(df: pd.DataFrame) -> pd.DataFrame:
    summary = pd.DataFrame({
        <span class="tok-str">"avg_word_count"</span>: [df[<span class="tok-str">"word_count"</span>].mean()],
        <span class="tok-str">"median_word_count"</span>: [df[<span class="tok-str">"word_count"</span>].median()],
        <span class="tok-str">"avg_h2_count"</span>: [df[<span class="tok-str">"h2_count"</span>].mean()],
        <span class="tok-str">"pct_with_schema"</span>: [df[<span class="tok-str">"has_schema_markup"</span>].mean() * <span class="tok-val">100</span>],
        <span class="tok-str">"pages_below_800_words"</span>: [(df[<span class="tok-str">"word_count"</span>] < <span class="tok-val">800</span>).sum()],
    })
    <span class="tok-kw">return</span> summary.round(<span class="tok-val">1</span>)

<span class="tok-kw">if</span> __name__ == <span class="tok-str">"__main__"</span>:
    df = pd.read_csv(<span class="tok-str">"competitor_audit.csv"</span>)
    <span class="tok-fn">print</span>(<span class="tok-fn">summarize_audit</span>(df))</code></pre>
  </div>

  <p>Numbers like these turn into decisions fast. If a competitor averages 1,800 words on their top ranking posts and your own average sits at 900, that is a specific, evidence backed gap to close rather than a vague feeling that your content should be longer.</p>

  <div class="bx-section-head">
    <span class="bx-num">08</span>
    <h2 class="bx-h2" id="handling-blocks-javascript-rendered-pages-and-other-failures">Handling Blocks, JavaScript Rendered Pages, and Other Failures</h2>
    <div class="bx-rule"></div>
  </div>

  <p>A web scraper for competitor content audits will eventually run into a page that fights back. Some sites block automated requests outright, and others render their content with JavaScript, so the HTML that <code>requests</code> receives is nearly empty.</p>

  <ul class="bx-checklist">
    <li><b>403 or 429 responses:</b> slow down further, respect a <code>Retry-After</code> header if one is present, and never retry aggressively against a site that is actively refusing you.</li>
    <li><b>Empty or near empty HTML:</b> if word count comes back near zero on a page you can see content on in a browser, the site likely renders with JavaScript and needs a headless browser instead.</li>
    <li><b>Encoding issues:</b> set <code>response.encoding</code> explicitly when special characters show up as garbled text.</li>
    <li><b>Timeouts:</b> a generous but finite timeout, paired with the retry decorator, keeps one slow server from stalling the whole audit.</li>
    <li><b>Sites that require JavaScript:</b> reach for <a href="https://playwright.dev/python/" target="_blank" rel="noopener">Playwright</a> instead of <code>requests</code>. It runs an actual browser engine and waits for the page to render before you read the HTML.</li>
  </ul>

  <div class="bx-code-wrap">
    <div class="bx-code-title">playwright_fallback.py</div>
    <pre><code><span class="tok-kw">from</span> playwright.sync_api <span class="tok-kw">import</span> sync_playwright

<span class="tok-kw">def</span> <span class="tok-fn">fetch_rendered_html</span>(url: <span class="tok-fn">str</span>) -> <span class="tok-fn">str</span>:
    <span class="tok-kw">with</span> sync_playwright() <span class="tok-kw">as</span> pw:
        browser = pw.chromium.launch(headless=<span class="tok-kw">True</span>)
        page = browser.new_page()
        page.goto(url, wait_until=<span class="tok-str">"networkidle"</span>)
        html = page.content()
        browser.close()
        <span class="tok-kw">return</span> html</code></pre>
  </div>

  <p>Reach for this only when you actually need it. A headless browser is slower and heavier than a plain request, so keep it as a fallback for JavaScript rendered pages rather than your default approach.</p>

  <p><a href="https://realpython.com/python-requests/" target="_blank" rel="noopener">Real Python's guide to the requests library</a> covers most of the timeout and error handling patterns worth knowing before you run a large crawl.</p>

  <div class="bx-ad">
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3931314195561246" crossorigin="anonymous"></script>
    <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-3931314195561246" data-ad-slot="4249015278" data-ad-format="auto" data-full-width-responsive="true"></ins>
    <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
  </div>

  <div class="bx-section-head">
    <span class="bx-num">09</span>
    <h2 class="bx-h2" id="legal-and-ethical-considerations-for-competitor-scraping">Legal and Ethical Considerations for Competitor Scraping</h2>
    <div class="bx-rule"></div>
  </div>

  <p>Scraping publicly visible pages for a <a href="/competitor-backlink-analysis/" target="_blank" rel="noopener">competitor analysis</a> sits in genuinely nuanced territory, and this guide is not legal advice. The details depend on your jurisdiction, the site's terms of service, and exactly what you collect.</p>

  <p>What is worth knowing is that courts have addressed this question directly. In <a href="https://en.wikipedia.org/wiki/HiQ_Labs_v._LinkedIn" target="_blank" rel="noopener">hiQ Labs v. LinkedIn</a>, a United States appeals court found that scraping data a site has made publicly accessible, without logging in, did not violate federal computer fraud law on its own.</p>

  <p>That ruling did not settle every question. A site's terms of service can still create separate contract obligations, and scraping personal data brings privacy rules like GDPR into play regardless of what a court decided about one specific statute.</p>

  <p>For a content audit built for internal strategy work, the practical guidance is simple. Stay on public pages, respect <code>robots.txt</code>, identify your bot honestly, keep request rates low, and never collect personal information you do not need.</p>

  <p>If you want data with a clearer license and none of this ambiguity, an official API is always the safer starting point, the same way it is for <a href="/best-keyword-research-tools-compared/" target="_blank" rel="noopener">keyword research tools</a> that offer one.</p>

  <div class="bx-tool">
    <h3>Crawl Delay and Duration Estimator</h3>
    <p class="bx-tool-sub">Pick a crawl pace and a page count to see roughly how long a polite audit takes.</p>
    <div class="bx-chip-row" id="bx-pace-chips">
      <button type="button" class="bx-chip active" data-delay="2" data-note="A safe default for most competitor audits">Polite, 2s delay</button>
      <button type="button" class="bx-chip" data-delay="1" data-note="Fine for smaller sites with light traffic">Standard, 1s delay</button>
      <button type="button" class="bx-chip" data-delay="0.5" data-note="Only use this on sites you know can handle it">Fast, 0.5s delay</button>
    </div>
    <div class="bx-stepper">
      <button type="button" id="bx-step-down" aria-label="Decrease page count">−</button>
      <span id="bx-step-value">50 pages</span>
      <button type="button" id="bx-step-up" aria-label="Increase page count">+</button>
    </div>
    <div class="bx-tool-output">
      <div><span class="bx-out-num" id="bx-out-time">1.7 min</span><span class="bx-out-label">Estimated total crawl time</span></div>
      <div><span class="bx-out-num" id="bx-out-rate">30</span><span class="bx-out-label" id="bx-out-note">Requests per minute</span></div>
    </div>
  </div>

  <div class="bx-section-head">
    <span class="bx-num">10</span>
    <h2 class="bx-h2" id="watch-web-scraping-with-python-and-beautifulsoup">Watch: Web Scraping With Python and BeautifulSoup</h2>
    <div class="bx-rule"></div>
  </div>

  <p>Watching the request and parse cycle run in real time makes it click faster than reading code alone. <a href="https://www.freecodecamp.org/" target="_blank" rel="noopener">freeCodeCamp.org</a>, a well known nonprofit coding education channel, published a full crash course covering exactly the <code>requests</code> and BeautifulSoup pattern used throughout this guide.</p>

  <div style="position:relative; padding-bottom:56.25%; height:0; overflow:hidden; border-radius:12px; margin:18px 0 8px;">
    <iframe src="https://www.youtube.com/embed/XVv6mJpFOb0" title="Web Scraping with Python, Beautiful Soup Crash Course by freeCodeCamp.org" style="position:absolute; top:0; left:0; width:100%; height:100%; border:0;" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen loading="lazy"></iframe>
  </div>
  <p style="font-size:14px; color:var(--bx-charcoal-soft); margin-top:6px;">Video credit: freeCodeCamp.org.</p>

  <p>The fundamentals in that video, fetching a page and walking its parsed tags, are the same fundamentals this entire pipeline builds on. Everything past that point is really just organizing what BeautifulSoup already gives you.</p>

  <svg width="100%" height="220" viewBox="0 0 800 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Diagram of a web scraper for competitor content audits moving from a sitemap through page fetching and parsing to a final audit report" style="margin:26px 0;">
    <rect width="800" height="220" fill="#f4faef" rx="12"/>
    <g font-family="Open Sans, sans-serif" font-size="14" fill="#2b2b2b">
      <rect x="20" y="85" width="130" height="60" rx="8" fill="#ffffff" stroke="#5DB92E" stroke-width="2"/>
      <text x="85" y="120" text-anchor="middle" font-weight="700">Sitemap URLs</text>

      <line x1="150" y1="115" x2="200" y2="115" stroke="#4a9e24" stroke-width="2" marker-end="url(#arrow)"/>

      <rect x="200" y="85" width="140" height="60" rx="8" fill="#ffffff" stroke="#5DB92E" stroke-width="2"/>
      <text x="270" y="120" text-anchor="middle" font-weight="700">Polite Fetch</text>

      <line x1="340" y1="115" x2="390" y2="115" stroke="#4a9e24" stroke-width="2" marker-end="url(#arrow)"/>

      <rect x="390" y="85" width="150" height="60" rx="8" fill="#ffffff" stroke="#5DB92E" stroke-width="2"/>
      <text x="465" y="112" text-anchor="middle" font-weight="700">BeautifulSoup</text>
      <text x="465" y="130" text-anchor="middle" font-weight="700">Parsing</text>

      <line x1="540" y1="115" x2="590" y2="115" stroke="#4a9e24" stroke-width="2" marker-end="url(#arrow)"/>

      <rect x="590" y="85" width="130" height="60" rx="8" fill="#ffffff" stroke="#5DB92E" stroke-width="2"/>
      <text x="655" y="120" text-anchor="middle" font-weight="700">Pandas Table</text>

      <line x1="720" y1="115" x2="760" y2="115" stroke="#4a9e24" stroke-width="2" marker-end="url(#arrow2)"/>
    </g>
    <defs>
      <marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto" markerUnits="strokeWidth">
        <path d="M0,0 L0,6 L9,3 z" fill="#4a9e24"/>
      </marker>
      <marker id="arrow2" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto" markerUnits="strokeWidth">
        <path d="M0,0 L0,6 L9,3 z" fill="#4a9e24"/>
      </marker>
    </defs>
  </svg>

  <div class="bx-related">
    <h3>Related Articles</h3>
    <ul>
      <li><a href="/content-audit-explained-improve-rankings/" target="_blank" rel="noopener">Content Audit Explained: Improve Rankings</a></li>
      <li><a href="/competitor-backlink-analysis/" target="_blank" rel="noopener">Competitor Backlink Analysis</a></li>
      <li><a href="/build-seo-audit-tool-javascript/" target="_blank" rel="noopener">Build an SEO Audit Tool With JavaScript</a></li>
      <li><a href="/screaming-frog-seo-spider-beginners-guide/" target="_blank" rel="noopener">Screaming Frog SEO Spider: Beginners Guide</a></li>
    </ul>
  </div>

  <div class="bx-faq">
    <h3 class="bx-h3">Frequently Asked Questions</h3>

    <div class="bx-faq-item">
      <button type="button" class="bx-faq-q">Is a web scraper for competitor content audits legal to use?</button>
      <div class="bx-faq-a"><p>Scraping publicly visible pages without logging in has generally held up in cases like hiQ Labs v. LinkedIn, but this is not legal advice, and terms of service and privacy laws can still apply. Stay on public content, respect robots.txt, and keep your request rate low.</p></div>
    </div>
    <div class="bx-faq-item">
      <button type="button" class="bx-faq-q">Do I need permission before scraping a competitor's website?</button>
      <div class="bx-faq-a"><p>You do not typically need explicit permission for publicly available pages, but checking robots.txt and following any stated crawling rules is the closest thing to asking politely. If a site clearly disallows a path, treat that as a firm no.</p></div>
    </div>
    <div class="bx-faq-item">
      <button type="button" class="bx-faq-q">What Python library should I use for a competitor content audit?</button>
      <div class="bx-faq-a"><p>Start with <code>requests</code> and <code>beautifulsoup4</code> for most sites. Reach for <code>Playwright</code> only when a page renders its content with JavaScript and the plain HTML comes back nearly empty.</p></div>
    </div>
    <div class="bx-faq-item">
      <button type="button" class="bx-faq-q">How do I avoid getting blocked while scraping competitor pages?</button>
      <div class="bx-faq-a"><p>Add real delays between requests, use an honest <code>User-Agent</code> header, respect robots.txt, and back off completely if you see repeated 403 or 429 responses. A slow, polite crawl rarely gets blocked.</p></div>
    </div>
    <div class="bx-faq-item">
      <button type="button" class="bx-faq-q">Can I scrape JavaScript heavy websites with requests and BeautifulSoup alone?</button>
      <div class="bx-faq-a"><p>Usually not. If the rendered content only appears after JavaScript runs, plain requests will return incomplete HTML, and you will need a headless browser tool like Playwright instead.</p></div>
    </div>
  </div>

  <div class="bx-learn">
    <h2 id="what-we-learn-today">What We Learn Today</h2>
    <div class="bx-learn-grid">
      <div class="bx-learn-card"><span class="bx-learn-num">1</span><div><h4>Automation removes inconsistency</h4><p>A web scraper for competitor content audits treats every page the same way, unlike a tired manual reviewer.</p></div></div>
      <div class="bx-learn-card"><span class="bx-learn-num">2</span><div><h4>robots.txt comes first</h4><p>Check permission before every crawl using Python's built in robot parser, not after something goes wrong.</p></div></div>
      <div class="bx-learn-card"><span class="bx-learn-num">3</span><div><h4>Word count alone is not enough</h4><p>Headings, links, images, and schema markup together tell the real content story.</p></div></div>
      <div class="bx-learn-card"><span class="bx-learn-num">4</span><div><h4>Sitemaps unlock full coverage</h4><p>Crawling a whole sitemap reveals patterns a handful of manually chosen pages cannot show.</p></div></div>
      <div class="bx-learn-card"><span class="bx-learn-num">5</span><div><h4>JavaScript needs a different tool</h4><p>Playwright picks up where plain requests calls stop working on rendered pages.</p></div></div>
      <div class="bx-learn-card"><span class="bx-learn-num">6</span><div><h4>Ethics is not optional</h4><p>Polite delays, honest identification, and public data only keep an audit sustainable and defensible.</p></div></div>
    </div>
  </div>

  <div class="bx-ad">
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3931314195561246" crossorigin="anonymous"></script>
    <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-3931314195561246" data-ad-slot="4249015278" data-ad-format="auto" data-full-width-responsive="true"></ins>
    <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
  </div>

  <div class="bx-cta">
    <h3>Ready to Build Your Own Content Audit Workflow?</h3>
    <p>Pair this web scraper for competitor content audits with a full audit process to turn competitor data into a real content plan.</p>
    <div class="bx-cta-btns">
      <a href="/content-audit-explained-improve-rankings/" target="_blank" rel="noopener">Read the Content Audit Guide</a>
      <a href="/build-seo-audit-tool-javascript/" target="_blank" rel="noopener" class="bx-cta-outline">Build More SEO Tools</a>
    </div>
  </div>

</div>

<script>
(function() {
  // FAQ accordion, single item open at a time
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

  // Crawl delay and duration estimator
  var chips = document.querySelectorAll('#bx-pace-chips .bx-chip');
  var stepValue = document.getElementById('bx-step-value');
  var outTime = document.getElementById('bx-out-time');
  var outRate = document.getElementById('bx-out-rate');
  var pages = 50;
  var delay = 2;

  function render() {
    stepValue.textContent = pages + ' pages';
    var totalSeconds = pages * delay;
    var minutes = totalSeconds / 60;
    outTime.textContent = minutes < 1 ? Math.round(totalSeconds) + ' sec' : minutes.toFixed(1) + ' min';
    outRate.textContent = Math.round(60 / delay);
  }

  chips.forEach(function(chip) {
    chip.addEventListener('click', function() {
      chips.forEach(function(c) { c.classList.remove('active'); });
      chip.classList.add('active');
      delay = parseFloat(chip.getAttribute('data-delay'));
      render();
    });
  });

  document.getElementById('bx-step-up').addEventListener('click', function() {
    pages = Math.min(pages + 10, 500);
    render();
  });
  document.getElementById('bx-step-down').addEventListener('click', function() {
    pages = Math.max(pages - 10, 10);
    render();
  });

  render();
})();
</script>
