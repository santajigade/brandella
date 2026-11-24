---
title: "Simple Rank Tracker in Python: Build a Complete SEO Tool in 7 Steps"
slug: "simple-rank-tracker-python"
date: "2026-08-25T07:48:44"
updated: "2026-08-25T07:49:04"
author: "santajigade"
categories: ["development", "python"]
primaryCategory: "development"
description: "Learn how to build a simple rank tracker in Python using a compliant SERP API, store keyword history, and chart movement over time."
focusKeyword: "Simple Rank Tracker"
takeaways:
  - "Manual rank checks are unreliable because Google personalizes results by location, device and history, even in incognito mode."
  - "Scraping Google results directly sits outside Google's terms of service, so a dedicated SERP API such as SerpApi is the sustainable choice."
  - "A missing position is real data, meaning the domain did not appear in the organic results returned for that search."
  - "Storing results in a growing history file turns single snapshots into a tracker that shows ranking movement over time."
  - "API costs grow with keywords, locations and check frequency, and weekly checks are a reasonable default for most sites."
image: "/wp-content/uploads/2026/08/Simple-Rank-Tracker.webp"
imageAlt: "Simple Rank Tracker"
words: 1872
views: 45
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
.bx-stepper { display: flex; align-items: center; gap: 14px; margin-bottom: 18px; flex-wrap: wrap; }
.bx-stepper button {
  width: 36px; height: 36px; border-radius: 50%; border: 1px solid #3a444b; background: #2c343a;
  color: #fff; font-size: 18px; cursor: pointer; font-family: var(--bx-disp);
}
.bx-stepper span { font-family: var(--bx-disp); font-weight: 700; font-size: 17px; min-width: 150px; text-align: center; }
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
    <span class="bx-pill">Rank Tracking</span>
    <span class="bx-pill">SERP API</span>
  </div>

  <p class="bx-lede">Typing forty keywords into an incognito window every Monday is not rank tracking, it is a chore that produces unreliable numbers. A simple rank tracker in python runs the same check the same way, every time, and remembers what it found.</p>

  <p>A client once tracked two hundred keywords by hand in a spreadsheet. Someone spent most of a Monday morning searching each one and writing down where the site landed.</p>

  <p>The numbers were never quite trustworthy. Personalization, location, and small mistakes in a long manual process all crept in somewhere along the way.</p>

  <p>A simple rank tracker in python fixes both problems at once. It checks every keyword the same way every time, and it never gets tired on keyword one hundred and eighty.</p>

  <p>This guide builds one using a proper SERP API rather than scraping Google directly, stores the results with history attached, and turns raw positions into a chart that actually shows movement.</p>

  <p>None of it needs a paid rank tracking platform. A SERP API key, a Python environment, and a place to store a growing CSV cover the whole build.</p>

  <div class="bx-stats">
    <div class="bx-stat-card"><span class="bx-stat-num">200+</span><span class="bx-stat-label">keywords a script checks in the time one manual search used to take</span></div>
    <div class="bx-stat-card"><span class="bx-stat-num">1 method</span><span class="bx-stat-label">stays reliable long term: a proper SERP API, not direct scraping</span></div>
    <div class="bx-stat-card"><span class="bx-stat-num">0</span><span class="bx-stat-label">personalization bias, since every check uses the same clean parameters</span></div>
  </div>

  <div class="bx-section-head">
    <span class="bx-num">01</span>
    <h2 class="bx-h2" id="why-a-simple-rank-tracker-in-python-beats-manual-checking">Why a Simple Rank Tracker in Python Beats Manual Checking</h2>
    <div class="bx-rule"></div>
  </div>

  <p>Manual rank checking has a quality problem before it even has a scale problem. Google personalizes results based on location, device, and search history, so the same query can return a different order for two different people.</p>

  <p>Incognito mode helps a little. It does not remove location signals or device differences, which means two people checking the same keyword in incognito can still see two different rankings.</p>

  <p>A script run with fixed parameters does not have that inconsistency. The same location, the same device setting, and the same query structure every single time make the resulting numbers actually comparable week to week.</p>

  <p>Comparing keyword rank against a broader <a href="/best-keyword-research-tools-compared/" target="_blank" rel="noopener">keyword research process</a> becomes far more useful once the tracking data behind it is this consistent.</p>


  <div class="bx-section-head">
    <span class="bx-num">02</span>
    <h2 class="bx-h2" id="choosing-a-compliant-way-to-check-rankings">Choosing a Compliant Way to Check Rankings</h2>
    <div class="bx-rule"></div>
  </div>

  <p>How a rank tracker actually gets its data matters more than most guides admit. Scraping Google's results pages directly sits outside <a href="https://policies.google.com/terms" target="_blank" rel="noopener">Google's terms of service</a>, and it tends to break the moment a CAPTCHA shows up.</p>

  <p>A dedicated SERP API is the sustainable choice. These services run the search on Google's behalf through infrastructure built for exactly this, and return clean, structured results instead of raw HTML to parse and hope holds together.</p>

  <div class="bx-table-wrap">
    <table class="bx-table">
      <thead>
        <tr><th>Method</th><th>Compliance</th><th>Reliability</th><th>Cost</th></tr>
      </thead>
      <tbody>
        <tr><td>Direct scraping of Google results</td><td>Outside Google's terms</td><td>Breaks often, blocked frequently</td><td>Free until it stops working</td></tr>
        <tr><td>Dedicated SERP API</td><td>Compliant, run through licensed infrastructure</td><td>Consistent, structured results</td><td>Usage based, this guide's approach</td></tr>
        <tr><td>Search Console average position</td><td>Fully compliant, official Google data</td><td>Aggregated, not a per search snapshot</td><td>Free with a verified property</td></tr>
      </tbody>
    </table>
  </div>

  <p>This guide builds around a SERP API, using <a href="https://serpapi.com/organic-results" target="_blank" rel="noopener">SerpApi</a> as the working example. The same pattern applies to comparable providers, since most return organic results in a similar structured shape.</p>

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

pip install google-search-results python-dotenv pandas</code></pre>
  </div>

  <p>The <a href="https://pypi.org/project/google-search-results/" target="_blank" rel="noopener"><code>google-search-results</code></a> package is SerpApi's official client, despite the slightly generic sounding name. <a href="https://pypi.org/project/python-dotenv/" target="_blank" rel="noopener"><code>python-dotenv</code></a> keeps the API key out of the code, and <a href="https://pandas.pydata.org/docs/" target="_blank" rel="noopener"><code>pandas</code></a> holds every result once it comes back.</p>

  <div class="bx-section-head">
    <span class="bx-num">04</span>
    <h2 class="bx-h2" id="checking-a-single-keyword-s-position">Checking a Single Keyword's Position</h2>
    <div class="bx-rule"></div>
  </div>

  <p>A single search returns a list of organic results, each with its own position. Finding your own domain in that list is the entire job.</p>

  <div class="bx-code-wrap">
    <div class="bx-code-title">rank_checker.py</div>
    <pre><code><span class="tok-kw">import</span> os
<span class="tok-kw">from</span> dotenv <span class="tok-kw">import</span> load_dotenv
<span class="tok-kw">from</span> serpapi <span class="tok-kw">import</span> GoogleSearch

load_dotenv()
<span class="tok-fn">API_KEY</span> = os.getenv(<span class="tok-str">"SERPAPI_KEY"</span>)

<span class="tok-kw">def</span> <span class="tok-fn">check_rank</span>(keyword: <span class="tok-fn">str</span>, target_domain: <span class="tok-fn">str</span>, location: <span class="tok-fn">str</span> = <span class="tok-str">"United States"</span>) -> <span class="tok-fn">dict</span>:
    params = {
        <span class="tok-str">"engine"</span>: <span class="tok-str">"google"</span>,
        <span class="tok-str">"q"</span>: keyword,
        <span class="tok-str">"location"</span>: location,
        <span class="tok-str">"api_key"</span>: API_KEY,
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    organic = results.get(<span class="tok-str">"organic_results"</span>, [])

    <span class="tok-kw">for</span> result <span class="tok-kw">in</span> organic:
        <span class="tok-kw">if</span> target_domain <span class="tok-kw">in</span> result.get(<span class="tok-str">"link"</span>, <span class="tok-str">""</span>):
            <span class="tok-kw">return</span> {<span class="tok-str">"keyword"</span>: keyword, <span class="tok-str">"position"</span>: result.get(<span class="tok-str">"position"</span>), <span class="tok-str">"url"</span>: result.get(<span class="tok-str">"link"</span>)}

    <span class="tok-kw">return</span> {<span class="tok-str">"keyword"</span>: keyword, <span class="tok-str">"position"</span>: <span class="tok-kw">None</span>, <span class="tok-str">"url"</span>: <span class="tok-kw">None</span>}</code></pre>
  </div>

  <p>A <code>None</code> position is not an error, it is real information. The domain genuinely did not appear in the organic results the API returned for that search.</p>

  <div class="bx-section-head">
    <span class="bx-num">05</span>
    <h2 class="bx-h2" id="tracking-multiple-keywords-and-locations">Tracking Multiple Keywords and Locations</h2>
    <div class="bx-rule"></div>
  </div>

  <p>A real tracker checks a whole list, and often needs to check it against more than one location if the business serves more than one market.</p>

  <div class="bx-code-wrap">
    <div class="bx-code-title">batch_check.py</div>
    <pre><code><span class="tok-kw">import</span> time
<span class="tok-kw">import</span> pandas <span class="tok-kw">as</span> pd
<span class="tok-kw">from</span> rank_checker <span class="tok-kw">import</span> check_rank

<span class="tok-fn">KEYWORDS</span> = [<span class="tok-str">"python for seo"</span>, <span class="tok-str">"rank tracker api"</span>, <span class="tok-str">"seo automation tools"</span>]
<span class="tok-fn">LOCATIONS</span> = [<span class="tok-str">"United States"</span>, <span class="tok-str">"United Kingdom"</span>]
<span class="tok-fn">TARGET_DOMAIN</span> = <span class="tok-str">"brandella.in"</span>

<span class="tok-kw">def</span> <span class="tok-fn">run_batch</span>() -> pd.DataFrame:
    rows = []

    <span class="tok-kw">for</span> location <span class="tok-kw">in</span> LOCATIONS:
        <span class="tok-kw">for</span> keyword <span class="tok-kw">in</span> KEYWORDS:
            result = <span class="tok-fn">check_rank</span>(keyword, TARGET_DOMAIN, location)
            result[<span class="tok-str">"location"</span>] = location
            rows.append(result)
            time.sleep(<span class="tok-val">1</span>)   <span class="tok-cm"># stay well under API rate limits</span>

    <span class="tok-kw">return</span> pd.DataFrame(rows)</code></pre>
  </div>

  <p>The one second pause between calls, using Python's own <a href="https://docs.python.org/3/library/time.html#time.sleep" target="_blank" rel="noopener"><code>time.sleep()</code></a>, is not strictly required by every provider, but it keeps a large batch well behaved and avoids tripping a rate limit partway through a run.</p>


  <div class="bx-section-head">
    <span class="bx-num">06</span>
    <h2 class="bx-h2" id="storing-rank-history-over-time">Storing Rank History Over Time</h2>
    <div class="bx-rule"></div>
  </div>

  <p>A single day of positions is a snapshot. History is what actually makes a simple rank tracker in python worth running, since movement only means something when you can see it against what came before.</p>

  <div class="bx-code-wrap">
    <div class="bx-code-title">append_history.py</div>
    <pre><code><span class="tok-kw">import</span> os
<span class="tok-kw">from</span> datetime <span class="tok-kw">import</span> date
<span class="tok-kw">import</span> pandas <span class="tok-kw">as</span> pd

<span class="tok-fn">HISTORY_PATH</span> = <span class="tok-str">"data/rank_history.csv"</span>

<span class="tok-kw">def</span> <span class="tok-fn">append_history</span>(df: pd.DataFrame):
    df[<span class="tok-str">"checked_on"</span>] = date.today().isoformat()

    <span class="tok-kw">if</span> os.path.exists(HISTORY_PATH):
        existing = pd.read_csv(HISTORY_PATH)
        combined = pd.concat([existing, df]).drop_duplicates(
            subset=[<span class="tok-str">"keyword"</span>, <span class="tok-str">"location"</span>, <span class="tok-str">"checked_on"</span>]
        )
    <span class="tok-kw">else</span>:
        combined = df

    combined.to_csv(HISTORY_PATH, index=<span class="tok-kw">False</span>)</code></pre>
  </div>

  <p>Running this daily or weekly through <a href="https://docs.github.com/en/actions" target="_blank" rel="noopener">GitHub Actions</a>, the same scheduling pattern used across the rest of this series, is what turns a one time check into an actual tracker.</p>

  <div class="bx-section-head">
    <span class="bx-num">07</span>
    <h2 class="bx-h2" id="visualizing-rank-movement">Visualizing Rank Movement</h2>
    <div class="bx-rule"></div>
  </div>

  <p>A table of numbers is accurate but hard to read at a glance. A simple line chart, built with <a href="https://matplotlib.org/stable/" target="_blank" rel="noopener">matplotlib</a>, makes movement obvious in a way a spreadsheet full of positions never quite does.</p>

  <div class="bx-code-wrap">
    <div class="bx-code-title">plot_history.py</div>
    <pre><code><span class="tok-kw">import</span> pandas <span class="tok-kw">as</span> pd
<span class="tok-kw">import</span> matplotlib.pyplot <span class="tok-kw">as</span> plt

<span class="tok-kw">def</span> <span class="tok-fn">plot_keyword_history</span>(history_path: <span class="tok-fn">str</span>, keyword: <span class="tok-fn">str</span>):
    df = pd.read_csv(history_path)
    subset = df[df[<span class="tok-str">"keyword"</span>] == keyword].sort_values(<span class="tok-str">"checked_on"</span>)

    plt.plot(subset[<span class="tok-str">"checked_on"</span>], subset[<span class="tok-str">"position"</span>], marker=<span class="tok-str">"o"</span>)
    plt.gca().invert_yaxis()   <span class="tok-cm"># position 1 should sit at the top</span>
    plt.title(<span class="tok-fn">f"Ranking history: {keyword}"</span>)
    plt.xlabel(<span class="tok-str">"Date checked"</span>)
    plt.ylabel(<span class="tok-str">"Position"</span>)
    plt.xticks(rotation=<span class="tok-val">45</span>)
    plt.tight_layout()
    plt.savefig(<span class="tok-fn">f"charts/{keyword.replace(' ', '_')}.png"</span>)</code></pre>
  </div>

  <p>Inverting the axis is a small detail that matters a lot. Without it, a page climbing from position ten to position one draws a line heading downward, which reads backward to anyone glancing at the chart.</p>

  <div class="bx-section-head">
    <span class="bx-num">08</span>
    <h2 class="bx-h2" id="handling-no-rank-results-volatility-and-api-costs">Handling No Rank Results, Volatility, and API Costs</h2>
    <div class="bx-rule"></div>
  </div>

  <p>A working script still needs a few judgment calls built in, or the numbers it produces will mislead more than they inform. <a href="https://www.searchenginejournal.com/rank-tracking/" target="_blank" rel="noopener">Search Engine Journal's guide to rank tracking</a> covers several of these same pitfalls from a broader, tool agnostic angle worth reading alongside a simple rank tracker in python.</p>

  <ul class="bx-checklist">
    <li><b>Not ranked is a real answer:</b> treat a missing position as data, not a bug, and record it as such rather than skipping the row.</li>
    <li><b>Single day swings are common:</b> positions naturally move a spot or two day to day. Look at a multi day trend before reacting to any one number.</li>
    <li><b>API calls cost money at scale:</b> a large keyword list checked daily across several locations adds up fast. Budget for it before committing to a schedule.</li>
    <li><b>Location genuinely changes results:</b> never assume a national average position reflects what a searcher in a specific city actually sees.</li>
    <li><b>Keep the target domain check flexible:</b> match on domain, not full URL, so a page that changes its path does not silently vanish from tracking.</li>
  </ul>

  <div class="bx-tool">
    <h3>Monthly SERP API Cost Estimator</h3>
    <p class="bx-tool-sub">Estimate the monthly call volume for a tracking schedule, based on keywords, locations, and check frequency.</p>
    <div class="bx-stepper">
      <button type="button" id="bx-kw-down" aria-label="Decrease keyword count">−</button>
      <span id="bx-kw-value">100 keywords</span>
      <button type="button" id="bx-kw-up" aria-label="Increase keyword count">+</button>
    </div>
    <div class="bx-stepper">
      <button type="button" id="bx-freq-down" aria-label="Decrease checks per week">−</button>
      <span id="bx-freq-value">1 check per week</span>
      <button type="button" id="bx-freq-up" aria-label="Increase checks per week">+</button>
    </div>
    <div class="bx-tool-output">
      <div><span class="bx-out-num" id="bx-out-calls">400</span><span class="bx-out-label">Estimated API calls per month</span></div>
      <div><span class="bx-out-num" id="bx-out-runs">4</span><span class="bx-out-label">Tracking runs per month</span></div>
    </div>
  </div>

  <div class="bx-section-head">
    <span class="bx-num">09</span>
    <h2 class="bx-h2" id="watch-a-quick-tour-of-a-serp-api-in-practice">Watch: A Quick Tour of a SERP API in Practice</h2>
    <div class="bx-rule"></div>
  </div>

  <p>SerpApi, the company whose API this guide builds around, published an official walkthrough of the same search endpoint and response structure used in the code above.</p>

  <div style="position:relative; padding-bottom:56.25%; height:0; overflow:hidden; border-radius:12px; margin:18px 0 8px;">
    <iframe src="https://www.youtube.com/embed/ViZ5WvDbzKY" title="Web Search API, A Quick Tour of SerpApi" style="position:absolute; top:0; left:0; width:100%; height:100%; border:0;" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen loading="lazy"></iframe>
  </div>
  <p style="font-size:14px; color:var(--bx-charcoal-soft); margin-top:6px;">Video credit: SerpApi, LLC.</p>

  <p>Seeing the raw response structure in the video makes it clear why parsing <code>organic_results</code> in Python is as simple as the code in this guide shows it to be.</p>

  <svg width="100%" height="220" viewBox="0 0 800 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Diagram of a simple rank tracker in python moving from a SERP API request through position matching to a stored history chart" style="margin:26px 0;">
    <rect width="800" height="220" fill="#f4faef" rx="12"/>
    <g font-family="Open Sans, sans-serif" font-size="14" fill="#2b2b2b">
      <rect x="20" y="85" width="130" height="60" rx="8" fill="#ffffff" stroke="#5DB92E" stroke-width="2"/>
      <text x="85" y="112" text-anchor="middle" font-weight="700">Keyword List</text>
      <text x="85" y="130" text-anchor="middle" font-weight="700">and Locations</text>

      <line x1="150" y1="115" x2="200" y2="115" stroke="#4a9e24" stroke-width="2" marker-end="url(#arrow)"/>

      <rect x="200" y="85" width="140" height="60" rx="8" fill="#ffffff" stroke="#5DB92E" stroke-width="2"/>
      <text x="270" y="120" text-anchor="middle" font-weight="700">SERP API Call</text>

      <line x1="340" y1="115" x2="390" y2="115" stroke="#4a9e24" stroke-width="2" marker-end="url(#arrow)"/>

      <rect x="390" y="85" width="150" height="60" rx="8" fill="#ffffff" stroke="#5DB92E" stroke-width="2"/>
      <text x="465" y="120" text-anchor="middle" font-weight="700">Position Match</text>

      <line x1="540" y1="115" x2="590" y2="115" stroke="#4a9e24" stroke-width="2" marker-end="url(#arrow)"/>

      <rect x="590" y="85" width="170" height="60" rx="8" fill="#2b2b2b" stroke="#5DB92E" stroke-width="2"/>
      <text x="675" y="120" text-anchor="middle" font-weight="700" fill="#5DB92E">History Chart</text>
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
      <button type="button" class="bx-faq-q">Is it legal to scrape Google search results for rank tracking?</button>
      <div class="bx-faq-a"><p>Directly scraping Google's results pages falls outside Google's terms of service and tends to get blocked quickly. A licensed SERP API runs the same search through infrastructure built for exactly this, which is the compliant and durable approach.</p></div>
    </div>
    <div class="bx-faq-item">
      <button type="button" class="bx-faq-q">How accurate is a simple rank tracker in python compared to paid platforms?</button>
      <div class="bx-faq-a"><p>Just as accurate for the core number, since both pull from the same kind of SERP API data underneath. Paid platforms mostly add convenience features like dashboards and alerts on top of the same raw check.</p></div>
    </div>
    <div class="bx-faq-item">
      <button type="button" class="bx-faq-q">How often should I check keyword rankings?</button>
      <div class="bx-faq-a"><p>Weekly is a reasonable default for most sites. Daily checks make sense for a small set of high value keywords, but running the full list daily usually costs more than the extra detail is worth.</p></div>
    </div>
    <div class="bx-faq-item">
      <button type="button" class="bx-faq-q">Can I track rankings for different cities or countries?</button>
      <div class="bx-faq-a"><p>Yes. Most SERP APIs accept a location parameter, and looping the same keyword across several locations is exactly what the batch checking example in this guide does.</p></div>
    </div>
    <div class="bx-faq-item">
      <button type="button" class="bx-faq-q">What does a not ranked or no position result actually mean?</button>
      <div class="bx-faq-a"><p>It means the target domain did not appear anywhere in the organic results the API returned for that search, typically the first page or two. It is a real result worth recording, not something to filter out.</p></div>
    </div>
  </div>

  <div class="bx-learn">
    <h2 id="what-we-learn-today">What We Learn Today</h2>
    <div class="bx-learn-grid">
      <div class="bx-learn-card"><span class="bx-learn-num">1</span><div><h4>Manual checks are inconsistent</h4><p>Personalization and location make hand checked rankings hard to compare over time.</p></div></div>
      <div class="bx-learn-card"><span class="bx-learn-num">2</span><div><h4>Method matters more than speed</h4><p>A compliant SERP API beats direct scraping on reliability, not just on legality.</p></div></div>
      <div class="bx-learn-card"><span class="bx-learn-num">3</span><div><h4>Position matching is simple</h4><p>Finding a domain inside organic results is a short loop, not complex logic.</p></div></div>
      <div class="bx-learn-card"><span class="bx-learn-num">4</span><div><h4>History is the actual product</h4><p>A single check is a snapshot. Stored history is what makes movement visible.</p></div></div>
      <div class="bx-learn-card"><span class="bx-learn-num">5</span><div><h4>Charts beat spreadsheets</h4><p>An inverted line chart makes rank movement obvious at a glance.</p></div></div>
      <div class="bx-learn-card"><span class="bx-learn-num">6</span><div><h4>Cost scales with ambition</h4><p>More keywords, more locations, and more frequency all add up in API calls.</p></div></div>
    </div>
  </div>


  <div class="bx-cta">
    <h3>Ready to Track Rankings on Your Own Terms?</h3>
    <p>Pair a simple rank tracker in python with a wider SEO toolkit to see the full picture behind every ranking change.</p>
    <div class="bx-cta-btns">
      <a href="/best-keyword-research-tools-compared/" target="_blank" rel="noopener">Compare Keyword Tools</a>
      <a href="/10-best-free-seo-tools-every-marketer-should-use/" target="_blank" rel="noopener" class="bx-cta-outline">Explore Free SEO Tools</a>
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

  var kwValue = document.getElementById('bx-kw-value');
  var freqValue = document.getElementById('bx-freq-value');
  var outCalls = document.getElementById('bx-out-calls');
  var outRuns = document.getElementById('bx-out-runs');
  var keywords = 100;
  var checksPerWeek = 1;

  function render() {
    kwValue.textContent = keywords + ' keywords';
    freqValue.textContent = checksPerWeek + (checksPerWeek === 1 ? ' check per week' : ' checks per week');
    var runsPerMonth = checksPerWeek * 4;
    outRuns.textContent = runsPerMonth;
    outCalls.textContent = (keywords * runsPerMonth).toLocaleString();
  }

  document.getElementById('bx-kw-up').addEventListener('click', function() {
    keywords = Math.min(keywords + 25, 1000);
    render();
  });
  document.getElementById('bx-kw-down').addEventListener('click', function() {
    keywords = Math.max(keywords - 25, 25);
    render();
  });
  document.getElementById('bx-freq-up').addEventListener('click', function() {
    checksPerWeek = Math.min(checksPerWeek + 1, 7);
    render();
  });
  document.getElementById('bx-freq-down').addEventListener('click', function() {
    checksPerWeek = Math.max(checksPerWeek - 1, 1);
    render();
  });

  render();
})();
</script>
