---
title: "Python Keyword Research Automation: 7 Proven Ways to Query SEO APIs at Scale"
slug: "python-keyword-research-automation"
date: "2026-08-25T03:40:05"
updated: "2026-08-25T03:41:08"
author: "santajigade"
categories: ["development", "python"]
primaryCategory: "development"
description: "Python keyword research automation pulls live search volume, related terms, and keyword clusters from the Google Ads and DataForSEO APIs, no manual exports required."
focusKeyword: "python keyword research automation"
image: "/wp-content/uploads/2026/08/python-keyword-research-automation.webp"
imageAlt: "python keyword research automation"
words: 2990
views: 57
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

/* Meta pills */
.bx-pills { display: flex; flex-wrap: wrap; gap: 8px; margin: 18px 0 20px; }
.bx-pill {
  font-family: var(--bx-disp); font-size: 13px; font-weight: 700;
  color: var(--bx-green-deep); background: #eef8e6; border: 1px solid var(--bx-green);
  padding: 5px 14px; border-radius: 30px; letter-spacing: .3px;
}

/* Lede */
.bx-lede {
  font-style: italic; font-size: 17px; color: var(--bx-charcoal-soft);
  border-left: 4px solid var(--bx-green); padding: 6px 20px; margin: 0 0 28px;
}

/* Numbered H2 */
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

/* Stat strip */
.bx-stats { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; margin: 22px 0 30px; }
.bx-stat-card { background: #f4faef; border: 1px solid #dff0d3; border-radius: 10px; padding: 20px 14px; text-align: center; }
.bx-stat-num { font-family: var(--bx-disp); font-weight: 800; font-size: 30px; color: var(--bx-green-deep); display: block; line-height: 1.1; }
.bx-stat-label { font-size: 14px; color: var(--bx-charcoal-soft); margin-top: 6px; display: block; }
@media (max-width: 640px) { .bx-stats { grid-template-columns: 1fr; } }

/* Code blocks */
.bx-code-wrap { margin: 18px 0 26px; border-radius: 10px; overflow: hidden; background: #1e1e2e; box-shadow: 0 2px 10px rgba(0,0,0,.15); }
.bx-code-title {
  background: #171724; color: #a9adc1; font-family: 'Courier New', monospace; font-size: 13px;
  padding: 10px 16px; border-bottom: 1px solid #2f2f45; letter-spacing: .3px;
}
.bx-code-wrap pre { margin: 0; padding: 18px 20px; overflow-x: auto; }
.bx-code-wrap code { font-family: 'Courier New', Consolas, monospace; font-size: 16px; line-height: 1.65; color: #e4e4f0; white-space: pre; }
.tok-kw { color: #c792ea; } /* keywords - purple */
.tok-fn { color: #82aaff; } /* functions - blue */
.tok-str { color: #f5d76e; } /* strings - yellow/gold */
.tok-val { color: #f78c50; } /* values - orange */
.tok-cm  { color: #7c7f93; font-style: italic; } /* comments grey italic */
.tok-sel { color: #9ece6a; } /* selectors - green */
.tok-prop{ color: #7fdbca; } /* properties - cyan */

/* Comparison / decision table */
.bx-table-wrap { overflow-x: auto; margin: 20px 0 30px; border-radius: 10px; }
table.bx-table { width: 100%; border-collapse: collapse; font-size: 17px; min-width: 620px; }
table.bx-table thead tr { background: var(--bx-charcoal); }
table.bx-table thead th { color: #fff; font-family: var(--bx-disp); font-weight: 700; text-align: left; padding: 13px 14px; font-size: 17px; }
table.bx-table tbody td { padding: 12px 14px; font-size: 17px; border-bottom: 1px solid #e7f2dd; }
table.bx-table tbody tr:nth-child(odd) { background: #f4faef; }
table.bx-table tbody tr:nth-child(even) { background: #ffffff; }

/* Checklist */
.bx-checklist { list-style: none; margin: 18px 0 28px; padding: 0; display: grid; gap: 12px; }
.bx-checklist li {
  background: #fff; border: 1px solid #e9e9e9; border-left: 4px solid var(--bx-green);
  border-radius: 8px; padding: 14px 16px 14px 44px; position: relative; font-size: 17px;
}
.bx-checklist li::before {
  content: "✓"; position: absolute; left: 14px; top: 13px; color: var(--bx-green-deep); font-weight: 800; font-size: 17px;
}
.bx-checklist b { color: var(--bx-charcoal); }

/* Dark interactive tool */
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
.bx-stepper span { font-family: var(--bx-disp); font-weight: 700; font-size: 18px; min-width: 110px; text-align: center; }
.bx-tool-output { background: #171d21; border-radius: 10px; padding: 20px; display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
.bx-tool-output .bx-out-num { font-family: var(--bx-disp); font-weight: 800; font-size: 26px; color: var(--bx-green); display: block; }
.bx-tool-output .bx-out-label { font-size: 13px; color: #9aa79f; }
@media (max-width: 640px) { .bx-tool-output { grid-template-columns: 1fr; } }

/* FAQ accordion */
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

/* Related articles */
.bx-related { background: #eef8e6; border-radius: 12px; padding: 26px 26px 10px; margin: 34px 0; }
.bx-related h3 { font-family: var(--bx-disp); font-size: 19px; color: var(--bx-charcoal); margin: 0 0 16px; }
.bx-related ul { list-style: none; margin: 0; padding: 0; display: grid; grid-template-columns: 1fr 1fr; gap: 10px 20px; }
.bx-related li { font-size: 17px; padding-bottom: 16px; border-bottom: 1px dashed #cfe8bd; }
@media (max-width: 640px) { .bx-related ul { grid-template-columns: 1fr; } }

/* What We Learn Today */
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

/* CTA */
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

/* Ad wrapper: dashed divider only, no text label */
.bx-ad { text-align: center; margin: 34px 0; padding: 18px 0; border-top: 1px dashed #cfcfcf; border-bottom: 1px dashed #cfcfcf; }
</style>

<div id="bx-article">

  <div class="bx-pills">
    <span class="bx-pill">Development</span>
    <span class="bx-pill">Python</span>
    <span class="bx-pill">SEO APIs</span>
    <span class="bx-pill">Automation</span>
  </div>

  <p class="bx-lede">Most SEO teams still build keyword lists by hand, one browser tab and one export at a time. Python keyword research automation replaces that slow loop with a script that runs in seconds and scales to thousands of terms.</p>

  <p>The first time I automated a client's keyword list with a script instead of a spreadsheet, it pulled 4,800 keyword variants with search volume, CPC, and competition data in under two minutes.</p>

  <p>The equivalent manual export from Google Keyword Planner, cleaned and deduplicated by hand, had taken our team most of a working day the week before.</p>

  <p>That gap is the whole case for python keyword research automation. It is not about replacing strategic judgment, since a script cannot decide which keywords fit your <a href="/content-calendar-planning/">content plan</a> or your business.</p>

  <p>What it does remove is the part that is repetitive and prone to errors: logging into an API, paging through results, merging data from more than one source, and running the same query again next month without starting from zero.</p>

  <p>This guide is a working build, not a theory piece. You will set up a Python environment and authenticate against two different keyword APIs.</p>

  <p>From there you will pull and merge live search volume data, cluster the results into topics, and schedule the whole pipeline to run on its own. Along the way we will cover the failure modes that actually show up in production, including rate limits, quota errors, and mismatched locales.</p>

  <div class="bx-stats">
    <div class="bx-stat-card"><span class="bx-stat-num">~20 min</span><span class="bx-stat-label">versus a full day for a 5,000 keyword manual export and cleanup</span></div>
    <div class="bx-stat-card"><span class="bx-stat-num">10K+</span><span class="bx-stat-label">keywords a single script can process per run without manual pagination</span></div>
    <div class="bx-stat-card"><span class="bx-stat-num">2 APIs</span><span class="bx-stat-label">minimum you'll want to blend for reliable volume and competition data</span></div>
  </div>

  <div class="bx-section-head">
    <span class="bx-num">01</span>
    <h2 class="bx-h2" id="why-python-keyword-research-automation-beats-manual-spreadsheets">Why Python Keyword Research Automation Beats Manual Spreadsheets</h2>
    <div class="bx-rule"></div>
  </div>

  <p>Manual keyword research has a ceiling. A person can comfortably review a few hundred terms before quality starts to drop.</p>

  <p>Fatigue sets in, formatting gets inconsistent, and duplicate or near duplicate keywords slip through. Manual work also does not refresh itself, so last quarter's volume numbers sit untouched until someone remembers to export them again.</p>

  <p>A script has none of those limits. Once the authentication and request logic are written, running it again next month costs almost nothing.</p>

  <p>This matters even more once you are trying to align keyword targeting with <a href="/what-is-search-intent-practical-guide/" target="_blank" rel="noopener">search intent</a> across a large site. That kind of classification is far easier to apply consistently when you are working with one structured dataframe instead of a scattered set of CSV exports from different tools.</p>

  <p>There is also a data quality argument. Ahrefs, Semrush, DataForSEO, and Google's own Keyword Planner rarely agree exactly on volume for the same term, because each pulls from different sample sizes and methods.</p>

  <p>Ahrefs' own study comparing Search Console and Keyword Planner volumes puts that gap in concrete numbers. Blending two or three sources programmatically, then averaging or flagging outliers, is realistic in Python. Doing the same thing by hand across multiple browser tabs is not, as <a href="https://ahrefs.com/blog/gsc-gkp-search-volume-study/" target="_blank" rel="noopener">Ahrefs' comparison of Search Console and Keyword Planner data</a> makes clear.</p>

  <div class="bx-ad">
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3931314195561246" crossorigin="anonymous"></script>
    <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-3931314195561246" data-ad-slot="4249015278" data-ad-format="auto" data-full-width-responsive="true"></ins>
    <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
  </div>

  <div class="bx-section-head">
    <span class="bx-num">02</span>
    <h2 class="bx-h2" id="setting-up-your-python-environment-for-seo-api-calls">Setting Up Your Python Environment for SEO API Calls</h2>
    <div class="bx-rule"></div>
  </div>

  <p>Every python keyword research automation project starts with the same small, reproducible environment. You need an HTTP client, a place to hold results, a way to keep API keys out of your codebase, and a retry layer for the moments when an endpoint throttles you partway through a run.</p>

  <div class="bx-code-wrap">
    <div class="bx-code-title">Terminal: project setup</div>
    <pre><code><span class="tok-cm"># create an isolated environment so package versions don't clash</span>
python -m venv venv
<span class="tok-val">source</span> venv/bin/activate      <span class="tok-cm"># Windows: venv\Scripts\activate</span>

pip install requests pandas python-dotenv tenacity google-ads gspread</code></pre>
  </div>

  <p>Store credentials in a <code>.env</code> file and load them with <code>python-dotenv</code>. Never hardcode API keys into a script you might commit to a public repository.</p>

  <div class="bx-code-wrap">
    <div class="bx-code-title">.env</div>
    <pre><code><span class="tok-prop">DATAFORSEO_LOGIN</span>=<span class="tok-str">your_login</span>
<span class="tok-prop">DATAFORSEO_PASSWORD</span>=<span class="tok-str">your_password</span>
<span class="tok-prop">GOOGLE_ADS_DEVELOPER_TOKEN</span>=<span class="tok-str">your_dev_token</span>
<span class="tok-prop">GOOGLE_ADS_CLIENT_ID</span>=<span class="tok-str">your_client_id</span>
<span class="tok-prop">GOOGLE_ADS_CLIENT_SECRET</span>=<span class="tok-str">your_client_secret</span>
<span class="tok-prop">GOOGLE_ADS_REFRESH_TOKEN</span>=<span class="tok-str">your_refresh_token</span>
<span class="tok-prop">GOOGLE_ADS_CUSTOMER_ID</span>=<span class="tok-str">1234567890</span></code></pre>
  </div>

  <div class="bx-code-wrap">
    <div class="bx-code-title">config.py</div>
    <pre><code><span class="tok-kw">import</span> os
<span class="tok-kw">from</span> dotenv <span class="tok-kw">import</span> load_dotenv

load_dotenv()

<span class="tok-fn">DATAFORSEO_LOGIN</span> = os.getenv(<span class="tok-str">"DATAFORSEO_LOGIN"</span>)
<span class="tok-fn">DATAFORSEO_PASSWORD</span> = os.getenv(<span class="tok-str">"DATAFORSEO_PASSWORD"</span>)

<span class="tok-kw">if</span> <span class="tok-kw">not</span> DATAFORSEO_LOGIN:
    <span class="tok-kw">raise</span> <span class="tok-fn">EnvironmentError</span>(<span class="tok-str">"Missing DATAFORSEO_LOGIN in .env"</span>)</code></pre>
  </div>

  <p>This structure matters. A dedicated <code>config.py</code> that fails loudly when a credential is missing saves you from a much worse failure mode: a script that silently sends empty auth headers and returns a generic 401 three modules deep into a pipeline.</p>

  <div class="bx-section-head">
    <span class="bx-num">03</span>
    <h2 class="bx-h2" id="choosing-the-right-keyword-data-api-for-your-python-pipeline">Choosing the Right Keyword Data API for Your Python Pipeline</h2>
    <div class="bx-rule"></div>
  </div>

  <p>Every keyword API trades off differently on cost, setup complexity, and freshness. Before writing a single request for python keyword research automation, decide which one actually fits the job.</p>

  <p>Pulling seed keyword volume for a content calendar has very different requirements than continuously monitoring competitor rankings. For a broader look at the tools themselves, read our <a href="/best-keyword-research-tools-compared/" target="_blank" rel="noopener">comparison of the best keyword research tools</a>. Here is how the four most commonly scripted APIs stack up for Python automation specifically.</p>

  <div class="bx-table-wrap">
    <table class="bx-table">
      <thead>
        <tr><th>API</th><th>Auth Method</th><th>Free Tier</th><th>Best For</th></tr>
      </thead>
      <tbody>
        <tr><td><strong>Google Ads API</strong> (Keyword Planner)</td><td>OAuth2 plus developer token</td><td>Free with an active Google Ads account</td><td>Google sourced volume and Keyword Ideas expansion</td></tr>
        <tr><td><strong>DataForSEO Labs / Keywords Data</strong></td><td>HTTP Basic Auth</td><td>Pay as you go, with no monthly minimum on most endpoints</td><td>Bulk volume, related keywords, clustering based on real search results</td></tr>
        <tr><td><strong>Semrush API</strong></td><td>API key (purchased units)</td><td>None. Units are bought separately from the subscription</td><td>Competitor keyword gaps, difficulty scoring</td></tr>
        <tr><td><strong>Keywords Everywhere API</strong></td><td>API key (credit packs)</td><td>Small free credit allowance</td><td>Lightweight volume lookups, browser and script parity</td></tr>
      </tbody>
    </table>
  </div>

  <p>For most teams, the practical answer is to combine two APIs. Use the Google Ads API for authoritative search volume and keyword ideas sourced directly from Google, and use DataForSEO for the bulk keyword expansion and clustering data that Google's own API does not expose.</p>

  <p>That pairing is what the rest of this walkthrough uses.</p>

  <div class="bx-section-head">
    <span class="bx-num">04</span>
    <h2 class="bx-h2" id="pulling-search-volume-data-with-the-dataforseo-api">Pulling Search Volume Data with the DataForSEO API</h2>
    <div class="bx-rule"></div>
  </div>

  <p>The first practical step in python keyword research automation is pulling real search volume, not theoretical seed terms. DataForSEO's <a href="https://docs.dataforseo.com/v3/keywords-data-overview/" target="_blank" rel="noopener">Keywords Data endpoints</a> accept a list of seed terms and return monthly search volume, CPC, and competition in a single request.</p>

  <p>For lists under 1,000 keywords per call, no pagination is required.</p>

  <div class="bx-code-wrap">
    <div class="bx-code-title">dataforseo_volume.py</div>
    <pre><code><span class="tok-kw">import</span> base64
<span class="tok-kw">import</span> requests
<span class="tok-kw">import</span> pandas <span class="tok-kw">as</span> pd
<span class="tok-kw">from</span> tenacity <span class="tok-kw">import</span> retry, wait_exponential, stop_after_attempt
<span class="tok-kw">from</span> config <span class="tok-kw">import</span> DATAFORSEO_LOGIN, DATAFORSEO_PASSWORD

<span class="tok-fn">API_URL</span> = <span class="tok-str">"https://api.dataforseo.com/v3/keywords_data/google_ads/search_volume/live"</span>

<span class="tok-kw">def</span> <span class="tok-fn">_auth_header</span>():
    token = base64.b64encode(
        <span class="tok-fn">f"{DATAFORSEO_LOGIN}:{DATAFORSEO_PASSWORD}"</span>.encode()
    ).decode()
    <span class="tok-kw">return</span> {<span class="tok-str">"Authorization"</span>: <span class="tok-fn">f"Basic {token}"</span>, <span class="tok-str">"Content-Type"</span>: <span class="tok-str">"application/json"</span>}

<span class="tok-cm">@retry(wait=wait_exponential(multiplier=1, min=2, max=30), stop=stop_after_attempt(5))</span>
<span class="tok-kw">def</span> <span class="tok-fn">get_search_volume</span>(keywords: <span class="tok-fn">list</span>, location_code: <span class="tok-fn">int</span> = <span class="tok-val">2840</span>, language_code: <span class="tok-fn">str</span> = <span class="tok-str">"en"</span>):
    <span class="tok-str">"""Fetch search volume for up to 1000 keywords in one call."""</span>
    payload = [{
        <span class="tok-str">"keywords"</span>: keywords,
        <span class="tok-str">"location_code"</span>: location_code,
        <span class="tok-str">"language_code"</span>: language_code,
    }]
    response = requests.post(API_URL, json=payload, headers=_auth_header(), timeout=<span class="tok-val">30</span>)
    response.raise_for_status()
    data = response.json()

    rows = []
    <span class="tok-kw">for</span> task <span class="tok-kw">in</span> data.get(<span class="tok-str">"tasks"</span>, []):
        <span class="tok-kw">for</span> item <span class="tok-kw">in</span> (task.get(<span class="tok-str">"result"</span>) <span class="tok-kw">or</span> []):
            rows.append({
                <span class="tok-str">"keyword"</span>: item.get(<span class="tok-str">"keyword"</span>),
                <span class="tok-str">"search_volume"</span>: item.get(<span class="tok-str">"search_volume"</span>),
                <span class="tok-str">"cpc"</span>: item.get(<span class="tok-str">"cpc"</span>),
                <span class="tok-str">"competition"</span>: item.get(<span class="tok-str">"competition"</span>),
            })
    <span class="tok-kw">return</span> pd.DataFrame(rows)

<span class="tok-kw">if</span> __name__ == <span class="tok-str">"__main__"</span>:
    seeds = [<span class="tok-str">"python for seo"</span>, <span class="tok-str">"keyword research api"</span>, <span class="tok-str">"seo automation tools"</span>]
    df = <span class="tok-fn">get_search_volume</span>(seeds)
    df.to_csv(<span class="tok-str">"volume_report.csv"</span>, index=<span class="tok-kw">False</span>)
    <span class="tok-fn">print</span>(df.sort_values(<span class="tok-str">"search_volume"</span>, ascending=<span class="tok-kw">False</span>))</code></pre>
  </div>

  <p>The <code>@retry</code> decorator from <a href="https://pypi.org/project/tenacity/" target="_blank" rel="noopener">Tenacity</a> is doing real work here, not just decoration. DataForSEO, like most SEO APIs, will occasionally return a 429 or a brief 500 under load.</p>

  <p>Exponential backoff is the difference between a script that fails cleanly on a genuine outage and one that fails on a blip that would have resolved itself two seconds later.</p>

  <div class="bx-section-head">
    <span class="bx-num">05</span>
    <h2 class="bx-h2" id="expanding-seed-keywords-with-the-google-ads-api">Expanding Seed Keywords with the Google Ads API</h2>
    <div class="bx-rule"></div>
  </div>

  <p>The Google Ads API's <code>KeywordPlanIdeaService</code> is the closest thing to raw Keyword Planner data you can script against. Setup is heavier than DataForSEO.</p>

  <p>You need a developer token approved on a Google Ads manager account, plus an OAuth2 refresh token. In exchange, the data comes straight from Google.</p>

  <div class="bx-code-wrap">
    <div class="bx-code-title">google_ads.yaml</div>
    <pre><code><span class="tok-prop">developer_token</span>: <span class="tok-str">"YOUR_DEV_TOKEN"</span>
<span class="tok-prop">client_id</span>: <span class="tok-str">"YOUR_CLIENT_ID"</span>
<span class="tok-prop">client_secret</span>: <span class="tok-str">"YOUR_CLIENT_SECRET"</span>
<span class="tok-prop">refresh_token</span>: <span class="tok-str">"YOUR_REFRESH_TOKEN"</span>
<span class="tok-prop">login_customer_id</span>: <span class="tok-str">"1234567890"</span></code></pre>
  </div>

  <div class="bx-code-wrap">
    <div class="bx-code-title">keyword_ideas.py</div>
    <pre><code><span class="tok-kw">from</span> google.ads.googleads.client <span class="tok-kw">import</span> GoogleAdsClient

<span class="tok-kw">def</span> <span class="tok-fn">generate_keyword_ideas</span>(customer_id: <span class="tok-fn">str</span>, seed_keywords: <span class="tok-fn">list</span>, page_url: <span class="tok-fn">str</span> = <span class="tok-kw">None</span>):
    client = GoogleAdsClient.load_from_storage(<span class="tok-str">"google_ads.yaml"</span>)
    keyword_plan_idea_service = client.get_service(<span class="tok-str">"KeywordPlanIdeaService"</span>)

    request = client.get_type(<span class="tok-str">"GenerateKeywordIdeasRequest"</span>)
    request.customer_id = customer_id
    request.language = <span class="tok-str">"languageConstants/1000"</span>   <span class="tok-cm"># English</span>
    request.geo_target_constants.append(<span class="tok-str">"geoTargetConstants/2840"</span>)  <span class="tok-cm"># US</span>
    request.keyword_plan_network = (
        client.enums.KeywordPlanNetworkEnum.GOOGLE_SEARCH
    )
    request.keyword_seed.keywords.extend(seed_keywords)

    results = keyword_plan_idea_service.generate_keyword_ideas(request=request)

    ideas = []
    <span class="tok-kw">for</span> result <span class="tok-kw">in</span> results:
        metrics = result.keyword_idea_metrics
        ideas.append({
            <span class="tok-str">"keyword"</span>: result.text,
            <span class="tok-str">"avg_monthly_searches"</span>: metrics.avg_monthly_searches,
            <span class="tok-str">"competition"</span>: metrics.competition.name,
        })
    <span class="tok-kw">return</span> ideas</code></pre>
  </div>

  <p>Two setup details trip people up every time. First, <code>login_customer_id</code> must be the manager account, not the client account, if you are accessing data through an agency's MCC structure.</p>

  <p>Second, the refresh token has to be generated with the exact OAuth scope that <a href="https://developers.google.com/identity/protocols/oauth2" target="_blank" rel="noopener">Google's OAuth2 documentation</a> specifies for Ads API access. A token generated for a different Google API scope will authenticate, but it will fail silently on every call to the Ads API.</p>

  <div class="bx-ad">
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3931314195561246" crossorigin="anonymous"></script>
    <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-3931314195561246" data-ad-slot="4249015278" data-ad-format="auto" data-full-width-responsive="true"></ins>
    <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
  </div>

  <div class="bx-section-head">
    <span class="bx-num">06</span>
    <h2 class="bx-h2" id="clustering-thousands-of-keywords-automatically-in-python">Clustering Thousands of Keywords Automatically in Python</h2>
    <div class="bx-rule"></div>
  </div>

  <p>Raw volume data is not a content plan. It is a spreadsheet with thousands of rows until it gets grouped into topics someone can actually write against.</p>

  <p>This is where python keyword research automation earns its keep a second time. Clustering by hand past a few hundred rows is genuinely impractical, but a script can group thousands of keywords by similarity in seconds.</p>

  <p>A lightweight approach uses term frequency vectors and cosine similarity. It needs no external embedding API, which keeps the pipeline free to run:</p>

  <div class="bx-code-wrap">
    <div class="bx-code-title">cluster_keywords.py</div>
    <pre><code><span class="tok-kw">from</span> sklearn.feature_extraction.text <span class="tok-kw">import</span> TfidfVectorizer
<span class="tok-kw">from</span> sklearn.cluster <span class="tok-kw">import</span> KMeans
<span class="tok-kw">import</span> pandas <span class="tok-kw">as</span> pd

<span class="tok-kw">def</span> <span class="tok-fn">cluster_keywords</span>(df: pd.DataFrame, n_clusters: <span class="tok-fn">int</span> = <span class="tok-val">12</span>):
    vectorizer = TfidfVectorizer(stop_words=<span class="tok-str">"english"</span>, ngram_range=(<span class="tok-val">1</span>, <span class="tok-val">2</span>))
    vectors = vectorizer.fit_transform(df[<span class="tok-str">"keyword"</span>])

    model = KMeans(n_clusters=n_clusters, random_state=<span class="tok-val">42</span>, n_init=<span class="tok-str">"auto"</span>)
    df[<span class="tok-str">"cluster"</span>] = model.fit_predict(vectors)

    <span class="tok-cm"># label each cluster with its highest volume keyword</span>
    labels = (
        df.sort_values(<span class="tok-str">"search_volume"</span>, ascending=<span class="tok-kw">False</span>)
          .groupby(<span class="tok-str">"cluster"</span>)[<span class="tok-str">"keyword"</span>]
          .first()
          .to_dict()
    )
    df[<span class="tok-str">"cluster_label"</span>] = df[<span class="tok-str">"cluster"</span>].map(labels)
    <span class="tok-kw">return</span> df</code></pre>
  </div>

  <p>Set <code>n_clusters</code> conservatively at first. Clustering too aggressively fragments closely related terms across separate topics, which defeats the point.</p>

  <p>A good starting rule is one cluster for every 15 to 25 keywords in your input set, then adjust by hand once you see the output. Once clusters are labeled, feeding them into a proper <a href="/how-to-build-topic-clusters-that-rank/" target="_blank" rel="noopener">topic cluster structure</a> is a much shorter step than starting from an unsorted keyword list.</p>

  <div class="bx-section-head">
    <span class="bx-num">07</span>
    <h2 class="bx-h2" id="scheduling-the-pipeline-and-storing-results-automatically">Scheduling the Pipeline and Storing Results Automatically</h2>
    <div class="bx-rule"></div>
  </div>

  <p>A script you run manually once is only a proof of concept, not python keyword research automation. A script that runs itself on a schedule and writes results somewhere your team actually looks, that is the real deliverable.</p>

  <p>Two practical options exist here. Use a cron job on a server you control, or use a <a href="https://docs.github.com/en/actions" target="_blank" rel="noopener">GitHub Actions</a> workflow if your code already lives in a repository.</p>

  <div class="bx-code-wrap">
    <div class="bx-code-title">.github/workflows/keyword_report.yml</div>
    <pre><code><span class="tok-prop">name</span>: <span class="tok-val">Weekly Keyword Report</span>
<span class="tok-prop">on</span>:
  <span class="tok-sel">schedule</span>:
    - <span class="tok-prop">cron</span>: <span class="tok-str">"0 6 * * 1"</span>   <span class="tok-cm"># every Monday at 06:00 UTC</span>
  <span class="tok-sel">workflow_dispatch</span>: {}

<span class="tok-prop">jobs</span>:
  <span class="tok-sel">run_report</span>:
    <span class="tok-prop">runs-on</span>: <span class="tok-val">ubuntu-latest</span>
    <span class="tok-prop">steps</span>:
      - <span class="tok-prop">uses</span>: <span class="tok-val">actions/checkout@v4</span>
      - <span class="tok-prop">uses</span>: <span class="tok-val">actions/setup-python@v5</span>
        <span class="tok-prop">with</span>:
          <span class="tok-prop">python-version</span>: <span class="tok-str">"3.11"</span>
      - <span class="tok-prop">run</span>: <span class="tok-val">pip install -r requirements.txt</span>
      - <span class="tok-prop">run</span>: <span class="tok-val">python run_pipeline.py</span>
        <span class="tok-prop">env</span>:
          <span class="tok-prop">DATAFORSEO_LOGIN</span>: <span class="tok-val">${{ secrets.DATAFORSEO_LOGIN }}</span>
          <span class="tok-prop">DATAFORSEO_PASSWORD</span>: <span class="tok-val">${{ secrets.DATAFORSEO_PASSWORD }}</span></code></pre>
  </div>

  <p>For storage, writing straight to Google Sheets with <code>gspread</code> keeps results visible to teammates who are not developers, without building a dashboard:</p>

  <div class="bx-code-wrap">
    <div class="bx-code-title">write_to_sheets.py</div>
    <pre><code><span class="tok-kw">import</span> gspread
<span class="tok-kw">import</span> pandas <span class="tok-kw">as</span> pd

<span class="tok-kw">def</span> <span class="tok-fn">push_to_sheet</span>(df: pd.DataFrame, sheet_id: <span class="tok-fn">str</span>, worksheet_name: <span class="tok-fn">str</span> = <span class="tok-str">"Keywords"</span>):
    gc = gspread.service_account(filename=<span class="tok-str">"service_account.json"</span>)
    sheet = gc.open_by_key(sheet_id)
    <span class="tok-kw">try</span>:
        ws = sheet.worksheet(worksheet_name)
    <span class="tok-kw">except</span> gspread.WorksheetNotFound:
        ws = sheet.add_worksheet(title=worksheet_name, rows=<span class="tok-str">"2000"</span>, cols=<span class="tok-str">"10"</span>)

    ws.clear()
    ws.update([df.columns.values.tolist()] + df.values.tolist())</code></pre>
  </div>

  <div class="bx-section-head">
    <span class="bx-num">08</span>
    <h2 class="bx-h2" id="handling-rate-limits-quota-errors-and-other-edge-cases">Handling Rate Limits, Quota Errors, and Other Edge Cases</h2>
    <div class="bx-rule"></div>
  </div>

  <p>Every python keyword research automation pipeline that runs unattended will eventually meet an edge case a manual workflow would have caught by eye. Build for these before they show up in an early morning scheduled run with nobody watching.</p>

  <ul class="bx-checklist">
    <li><b>Rate limit responses (429):</b> back off exponentially and cap total retries. Do not loop indefinitely against an API that is actively throttling you.</li>
    <li><b>Keywords with zero volume:</b> DataForSEO and Google Ads both return <code>None</code> or <code>0</code> for terms that get very little search traffic. Filter or flag these rather than treating them as errors.</li>
    <li><b>Locale and currency mismatches:</b> a <code>location_code</code> or <code>language_code</code> set incorrectly returns data that looks valid but is wrong. It will not throw an error, so validate outputs against a known baseline keyword.</li>
    <li><b>Duplicate keywords across sources:</b> normalize casing and whitespace before merging DataForSEO and Google Ads results, or you will count the same term twice under two different labels.</li>
    <li><b>API quota running out partway through:</b> log progress to disk as you go, so a failed run at keyword 8,000 of 10,000 does not force a full restart from zero.</li>
  </ul>

  <p>None of these are exotic. They are the same categories of failure covered in <a href="https://realpython.com/python-requests/" target="_blank" rel="noopener">Real Python's guide to the requests library</a>, and building error handling for them up front is far cheaper than debugging a silent data quality issue three weeks later.</p>

  <div class="bx-ad">
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3931314195561246" crossorigin="anonymous"></script>
    <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-3931314195561246" data-ad-slot="4249015278" data-ad-format="auto" data-full-width-responsive="true"></ins>
    <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
  </div>

  <div class="bx-section-head">
    <span class="bx-num">09</span>
    <h2 class="bx-h2" id="api-key-security-and-compliance-considerations">API Key Security and Compliance Considerations</h2>
    <div class="bx-rule"></div>
  </div>

  <p>Two things get overlooked once a pipeline works: where the credentials live, and whether the method of collection is actually allowed. Neither is optional to think through.</p>

  <p>Keep every credential in environment variables or a secrets manager, never in a script committed to version control. Add <code>.env</code> to <code>.gitignore</code> on day one, not after a key leaks.</p>

  <p>If the pipeline runs in CI, store credentials as encrypted repository secrets, as shown in the GitHub Actions example above, rather than pasting them into workflow files directly.</p>

  <p>On compliance, everything in this guide queries official, documented APIs: Google Ads, DataForSEO, Semrush, and Keywords Everywhere. Each is governed by its own terms of service and rate limits that are meant to be respected, not routed around.</p>

  <p>That is a meaningfully different activity from scraping Google's live search results pages directly, which sits outside Google's terms and carries its own risk. <a href="https://searchengineland.com/" target="_blank" rel="noopener">Search Engine Land</a> and <a href="https://searchenginejournal.com/" target="_blank" rel="noopener">Search Engine Journal</a> have both covered enforcement actions against tools that scrape rather than query approved endpoints, a good reminder to build python keyword research automation on official APIs, not around them.</p>

  <div class="bx-tool">
    <h3>API Cost &amp; Quota Estimator</h3>
    <p class="bx-tool-sub">Pick a provider and a monthly keyword volume to see roughly what the automation costs to run.</p>
    <div class="bx-chip-row" id="bx-provider-chips">
      <button type="button" class="bx-chip active" data-cost="0.0" data-note="Free with an active Ads account, no per keyword fee">Google Ads API</button>
      <button type="button" class="bx-chip" data-cost="0.0006" data-note="Pay as you go, roughly $0.06 per 100 keyword volume lookups">DataForSEO</button>
      <button type="button" class="bx-chip" data-cost="0.0025" data-note="Units consumed from a purchased Semrush API package">Semrush API</button>
      <button type="button" class="bx-chip" data-cost="0.0008" data-note="Credit pack pricing, similar to a light DataForSEO run">Keywords Everywhere</button>
    </div>
    <div class="bx-stepper">
      <button type="button" id="bx-step-down" aria-label="Decrease keyword volume">−</button>
      <span id="bx-step-value">5,000 keywords</span>
      <button type="button" id="bx-step-up" aria-label="Increase keyword volume">+</button>
    </div>
    <div class="bx-tool-output">
      <div><span class="bx-out-num" id="bx-out-cost">$0.00</span><span class="bx-out-label">Estimated cost per run</span></div>
      <div><span class="bx-out-num" id="bx-out-note"></span><span class="bx-out-label" id="bx-out-note-label">Pricing basis</span></div>
    </div>
  </div>

  <div class="bx-section-head">
    <span class="bx-num">10</span>
    <h2 class="bx-h2" id="watch-building-a-keyword-research-tool-in-python">Watch: Building a Keyword Research Tool in Python</h2>
    <div class="bx-rule"></div>
  </div>

  <p>Seeing python keyword research automation run outside a code editor helps it click. For a walkthrough of querying Google's keyword data directly from a script, JC Chouinard covers the request and response structure end to end in this video.</p>

  <p>He is a Python and SEO practitioner whose scripts and tutorials at jcchouinard.com are widely referenced in the technical SEO community.</p>

  <div style="position:relative; padding-bottom:56.25%; height:0; overflow:hidden; border-radius:12px; margin:18px 0 8px;">
    <iframe src="https://www.youtube.com/embed/0bjfWoFtaYg" title="How To Use Google Keyword Research using Python Tutorial by JC Chouinard" style="position:absolute; top:0; left:0; width:100%; height:100%; border:0;" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen loading="lazy"></iframe>
  </div>
  <p style="font-size:14px; color:var(--bx-charcoal-soft); margin-top:6px;">Video credit: JC Chouinard, jcchouinard.com.</p>

  <p>The core logic in the video maps closely to the DataForSEO and Google Ads examples above. Authenticate, send seed keywords, then parse the JSON response into rows you can actually work with in <a href="https://pandas.pydata.org/" target="_blank" rel="noopener">pandas</a>.</p>

  <svg width="100%" height="220" viewBox="0 0 800 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Diagram of a python keyword research automation pipeline moving from seed keywords through API calls to clustered keyword output" style="margin:26px 0;">
    <rect width="800" height="220" fill="#f4faef" rx="12"/>
    <g font-family="Open Sans, sans-serif" font-size="14" fill="#2b2b2b">
      <rect x="30" y="85" width="140" height="60" rx="8" fill="#ffffff" stroke="#5DB92E" stroke-width="2"/>
      <text x="100" y="120" text-anchor="middle" font-weight="700">Seed Keywords</text>

      <line x1="170" y1="115" x2="220" y2="115" stroke="#4a9e24" stroke-width="2" marker-end="url(#arrow)"/>

      <rect x="220" y="85" width="150" height="60" rx="8" fill="#ffffff" stroke="#5DB92E" stroke-width="2"/>
      <text x="295" y="112" text-anchor="middle" font-weight="700">Google Ads +</text>
      <text x="295" y="130" text-anchor="middle" font-weight="700">DataForSEO APIs</text>

      <line x1="370" y1="115" x2="420" y2="115" stroke="#4a9e24" stroke-width="2" marker-end="url(#arrow)"/>

      <rect x="420" y="85" width="140" height="60" rx="8" fill="#ffffff" stroke="#5DB92E" stroke-width="2"/>
      <text x="490" y="120" text-anchor="middle" font-weight="700">Merged Dataframe</text>

      <line x1="560" y1="115" x2="610" y2="115" stroke="#4a9e24" stroke-width="2" marker-end="url(#arrow)"/>

      <rect x="610" y="85" width="160" height="60" rx="8" fill="#2b2b2b" stroke="#5DB92E" stroke-width="2"/>
      <text x="690" y="112" text-anchor="middle" font-weight="700" fill="#5DB92E">Clustered Topics</text>
      <text x="690" y="130" text-anchor="middle" font-size="12" fill="#e8ede9">+ Google Sheet</text>
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
      <button type="button" class="bx-faq-q">Can I automate keyword research in Python without a Google Ads account?</button>
      <div class="bx-faq-a"><p>Yes. DataForSEO, Semrush, and Keywords Everywhere all offer keyword volume and related keyword endpoints that do not require a Google Ads account. Only the Google Ads API's Keyword Planner data specifically requires one, since it is tied to that platform.</p></div>
    </div>
    <div class="bx-faq-item">
      <button type="button" class="bx-faq-q">Which Python library is best for calling SEO keyword APIs?</button>
      <div class="bx-faq-a"><p>The standard <code>requests</code> library covers most of what python keyword research automation needs for DataForSEO, Semrush, and Keywords Everywhere, with no extra dependency. For the Google Ads API specifically, Google's official <code>google-ads</code> Python client handles the more complex OAuth2 flow and the request objects built on protobuf for you.</p></div>
    </div>
    <div class="bx-faq-item">
      <button type="button" class="bx-faq-q">Is scraping Google Keyword Planner instead of using the API legal?</button>
      <div class="bx-faq-a"><p>Scraping Google's interfaces directly falls outside Google's terms of service and risks getting your account or IP address blocked. Querying the official Google Ads API with an approved developer token is the compliant path, and it is the one used throughout this guide.</p></div>
    </div>
    <div class="bx-faq-item">
      <button type="button" class="bx-faq-q">How much does python keyword research automation cost to run monthly?</button>
      <div class="bx-faq-a"><p>It depends entirely on which API and volume you choose. The Google Ads API is free with an active account, while DataForSEO and Keywords Everywhere typically run a few dollars per few thousand keywords. Use the cost estimator earlier in this article to model your own volume.</p></div>
    </div>
    <div class="bx-faq-item">
      <button type="button" class="bx-faq-q">Can I cluster keywords without machine learning experience?</button>
      <div class="bx-faq-a"><p>Yes. The term frequency and KMeans approach shown above uses functions already included in <code>scikit-learn</code>, and it requires no prior machine learning background to run. You are calling two functions, not designing a model from scratch.</p></div>
    </div>
  </div>

  <div class="bx-learn">
    <h2 id="what-we-learn-today">What We Learn Today</h2>
    <div class="bx-learn-grid">
      <div class="bx-learn-card"><span class="bx-learn-num">1</span><div><h4>Automation removes the ceiling</h4><p>Python keyword research automation scales past the few hundred terms a person can review manually in a session.</p></div></div>
      <div class="bx-learn-card"><span class="bx-learn-num">2</span><div><h4>Environment setup matters</h4><p>A <code>.env</code> file, retry logic, and a config module that fails loudly prevent silent failures down the line.</p></div></div>
      <div class="bx-learn-card"><span class="bx-learn-num">3</span><div><h4>No single API is complete</h4><p>Blending Google Ads and DataForSEO data covers gaps neither source fills alone.</p></div></div>
      <div class="bx-learn-card"><span class="bx-learn-num">4</span><div><h4>Clustering turns data into a plan</h4><p>Term frequency vectors and KMeans group thousands of keywords into usable topics in seconds.</p></div></div>
      <div class="bx-learn-card"><span class="bx-learn-num">5</span><div><h4>Scheduling makes it real</h4><p>Cron jobs and GitHub Actions turn a single script into a pipeline that runs itself weekly.</p></div></div>
      <div class="bx-learn-card"><span class="bx-learn-num">6</span><div><h4>Compliance isn't optional</h4><p>Official APIs, secured credentials, and respected rate limits keep the pipeline sustainable long term.</p></div></div>
    </div>
  </div>

  <div class="bx-ad">
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3931314195561246" crossorigin="anonymous"></script>
    <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-3931314195561246" data-ad-slot="4249015278" data-ad-format="auto" data-full-width-responsive="true"></ins>
    <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
  </div>

  <div class="bx-cta">
    <h3>Ready to Build Your Own SEO Automation Stack?</h3>
    <p>Explore more practical technical guides and tool comparisons to keep expanding your python keyword research automation toolkit.</p>
    <div class="bx-cta-btns">
      <a href="/best-keyword-research-tools-compared/" target="_blank" rel="noopener">Compare Keyword Tools</a>
      <a href="/build-ai-chatbot-openai-api/" target="_blank" rel="noopener" class="bx-cta-outline">Build With the OpenAI API</a>
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

  // Cost estimator tool
  var chips = document.querySelectorAll('#bx-provider-chips .bx-chip');
  var stepValue = document.getElementById('bx-step-value');
  var outCost = document.getElementById('bx-out-cost');
  var outNote = document.getElementById('bx-out-note');
  var outNoteLabel = document.getElementById('bx-out-note-label');
  var volume = 5000;
  var activeCost = 0.0;
  var activeNote = "Free with an active Ads account, no per keyword fee";

  function render() {
    stepValue.textContent = volume.toLocaleString() + ' keywords';
    var cost = (volume * activeCost);
    outCost.textContent = '$' + cost.toFixed(2);
    outNote.textContent = activeCost === 0 ? 'Free tier' : ('$' + activeCost.toFixed(4) + '/kw');
    outNoteLabel.textContent = activeNote;
  }

  chips.forEach(function(chip) {
    chip.addEventListener('click', function() {
      chips.forEach(function(c) { c.classList.remove('active'); });
      chip.classList.add('active');
      activeCost = parseFloat(chip.getAttribute('data-cost'));
      activeNote = chip.getAttribute('data-note');
      render();
    });
  });

  document.getElementById('bx-step-up').addEventListener('click', function() {
    volume = Math.min(volume + 1000, 50000);
    render();
  });
  document.getElementById('bx-step-down').addEventListener('click', function() {
    volume = Math.max(volume - 1000, 1000);
    render();
  });

  render();
})();
</script>
