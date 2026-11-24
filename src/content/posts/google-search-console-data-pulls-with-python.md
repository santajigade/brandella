---
title: "Google Search Console Data Pulls With Python: 7 Steps to Complete Automated Reporting"
slug: "google-search-console-data-pulls-with-python"
date: "2026-08-25T07:52:31"
updated: "2026-08-25T07:52:59"
author: "santajigade"
categories: ["development", "python"]
primaryCategory: "development"
description: "Google search console data pulls with python replace manual CSV exports with a script that fetches queries, clicks, and impressions straight from the API."
focusKeyword: "Google Search Console Data Pulls"
takeaways:
  - "The Search Console interface caps most exports at 1,000 rows and keeps only about sixteen months of visible data."
  - "A service account must be added as a user on the Search Console property, or API requests return empty results."
  - "The API returns up to 25,000 rows per request, so the startRow parameter is used to paginate until an empty page returns."
  - "Pulling data with a three day delay avoids saving incomplete figures, since recent Search Console numbers are often revised."
  - "Appending daily pulls into one deduplicated archive, scheduled through GitHub Actions, builds history beyond the dashboard's window."
image: "/wp-content/uploads/2026/08/Google-Search-Console-Data-Pulls.webp"
imageAlt: "Google Search Console Data Pulls"
words: 2187
views: 41
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
.bx-stepper { display: flex; align-items: center; gap: 14px; margin-bottom: 22px; }
.bx-stepper button {
  width: 36px; height: 36px; border-radius: 50%; border: 1px solid #3a444b; background: #2c343a;
  color: #fff; font-size: 18px; cursor: pointer; font-family: var(--bx-disp);
}
.bx-stepper span { font-family: var(--bx-disp); font-weight: 700; font-size: 18px; min-width: 150px; text-align: center; }
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
    <span class="bx-pill">Search Console</span>
    <span class="bx-pill">Reporting Automation</span>
  </div>

  <p class="bx-lede">The Search Console interface caps most reports at a thousand rows and quietly ages data out after around sixteen months. Google search console data pulls with python remove both limits and turn a manual export habit into a running archive.</p>

  <p>A site with a few thousand ranking queries hits that thousand row wall almost immediately. Whatever did not fit in the export just never gets analyzed.</p>

  <p>The sixteen month window causes a quieter problem. Ask what changed since a redesign two years ago, and the interface simply cannot answer, because the data behind that point is already gone.</p>

  <p>Google search console data pulls with python solve both problems at once. A script does not care whether a query is row four or row forty thousand, and once it starts saving results daily, the sixteen month ceiling stops mattering.</p>

  <p>This guide authenticates against the Search Console API, pulls query and page performance data, works past the API's own row limit, and saves everything somewhere that outlives the dashboard's memory.</p>

  <p>None of it needs anything exotic. A Google Cloud project, a Python environment, and about forty lines of working code cover the whole thing.</p>

  <div class="bx-stats">
    <div class="bx-stat-card"><span class="bx-stat-num">1,000</span><span class="bx-stat-label">rows is the practical cap on most Search Console UI exports</span></div>
    <div class="bx-stat-card"><span class="bx-stat-num">~16 mo</span><span class="bx-stat-label">is roughly how far back the interface keeps data visible</span></div>
    <div class="bx-stat-card"><span class="bx-stat-num">25,000</span><span class="bx-stat-label">rows per request is the API's own limit, which this guide works around</span></div>
  </div>

  <div class="bx-section-head">
    <span class="bx-num">01</span>
    <h2 class="bx-h2" id="why-google-search-console-data-pulls-with-python-beat-manual-exports">Why Google Search Console Data Pulls With Python Beat Manual Exports</h2>
    <div class="bx-rule"></div>
  </div>

  <p>The Search Console dashboard is genuinely useful for a quick look. It becomes a poor research tool the moment you need more history or more rows than the interface is willing to show.</p>

  <p>Comparing this quarter to the same quarter two years ago is a common request that the UI simply cannot fulfill once the data has aged out of its visible window.</p>

  <p>Exporting by hand every week is also easy to forget. A missed week is not just a gap, it is a permanent gap, since that data is not sitting somewhere waiting to be pulled later.</p>

  <p>Pairing this with a wider <a href="/google-search-console-ai-powered-configuration/" target="_blank" rel="noopener">Search Console configuration</a> review is worth doing once the automated pulls are running, since a script surfaces patterns a manual glance at the dashboard tends to miss.</p>


  <div class="bx-section-head">
    <span class="bx-num">02</span>
    <h2 class="bx-h2" id="setting-up-google-cloud-access-for-the-search-console-api">Setting Up Google Cloud Access for the Search Console API</h2>
    <div class="bx-rule"></div>
  </div>

  <p>Before any Python runs, the Search Console API needs to be turned on for a <a href="https://cloud.google.com/apis" target="_blank" rel="noopener">Google Cloud project</a>, and something needs permission to use it.</p>

  <p>A service account is the cleanest option for a script that runs unattended, since it never depends on a personal login session expiring.</p>

  <ul class="bx-checklist">
    <li><b>Create a Google Cloud project:</b> or reuse an existing one, then enable the Search Console API from the API library.</li>
    <li><b>Create a service account:</b> under IAM and Admin, and download its JSON key file. Treat this file exactly like a password.</li>
    <li><b>Grant the service account access:</b> add its email address as a user in <a href="https://support.google.com/webmasters/answer/7687615" target="_blank" rel="noopener">Search Console</a>, under Settings and then Users and Permissions, with at least Restricted access.</li>
    <li><b>Keep the key file out of version control:</b> add it to <code>.gitignore</code> immediately, the same as any other credential.</li>
  </ul>

  <p>Skipping that third step is the most common reason a first script fails. The API call authenticates fine and then returns an empty result, because the account making the request was never actually added to the property.</p>

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

pip install google-api-python-client google-auth pandas</code></pre>
  </div>

  <p>The <a href="https://pypi.org/project/google-api-python-client/" target="_blank" rel="noopener"><code>google-api-python-client</code></a> package builds the actual API connection, <code>google-auth</code> handles the service account authentication, and <a href="https://pandas.pydata.org/" target="_blank" rel="noopener">pandas</a> holds the results once they come back.</p>

  <div class="bx-section-head">
    <span class="bx-num">04</span>
    <h2 class="bx-h2" id="authenticating-and-connecting-to-the-search-console-api">Authenticating and Connecting to the Search Console API</h2>
    <div class="bx-rule"></div>
  </div>

  <p>With the service account key in hand, connecting takes a few lines. This function builds a reusable client that every later script in this guide calls.</p>

  <div class="bx-code-wrap">
    <div class="bx-code-title">gsc_client.py</div>
    <pre><code><span class="tok-kw">from</span> google.oauth2 <span class="tok-kw">import</span> service_account
<span class="tok-kw">from</span> googleapiclient.discovery <span class="tok-kw">import</span> build

<span class="tok-fn">SCOPES</span> = [<span class="tok-str">"https://www.googleapis.com/auth/webmasters.readonly"</span>]
<span class="tok-fn">KEY_FILE</span> = <span class="tok-str">"service_account.json"</span>

<span class="tok-kw">def</span> <span class="tok-fn">get_gsc_service</span>():
    credentials = service_account.Credentials.from_service_account_file(
        KEY_FILE, scopes=SCOPES
    )
    <span class="tok-kw">return</span> build(<span class="tok-str">"searchconsole"</span>, <span class="tok-str">"v1"</span>, credentials=credentials)</code></pre>
  </div>

  <p>The read only scope is intentional. A reporting script has no reason to ever modify a property's settings, so limiting what the credential can do keeps the blast radius small if the key ever leaks.</p>

  <p>The full setup, including where each button lives inside the Google Cloud console, is also documented step by step on <a href="https://www.jcchouinard.com/google-search-console-api-with-python/" target="_blank" rel="noopener">jcchouinard.com</a> if a screenshot heavy walkthrough helps.</p>

  <div class="bx-section-head">
    <span class="bx-num">05</span>
    <h2 class="bx-h2" id="pulling-query-and-page-performance-data">Pulling Query and Page Performance Data</h2>
    <div class="bx-rule"></div>
  </div>

  <p>Every real implementation of google search console data pulls with python starts at the same endpoint. The <a href="https://developers.google.com/webmaster-tools/v1/searchanalytics/query" target="_blank" rel="noopener">searchanalytics.query</a> call accepts a date range and a list of dimensions, then returns clicks, impressions, position, and click through rate for each row.</p>

  <div class="bx-code-wrap">
    <div class="bx-code-title">pull_performance.py</div>
    <pre><code><span class="tok-kw">import</span> pandas <span class="tok-kw">as</span> pd
<span class="tok-kw">from</span> gsc_client <span class="tok-kw">import</span> get_gsc_service

<span class="tok-kw">def</span> <span class="tok-fn">pull_search_data</span>(site_url: <span class="tok-fn">str</span>, start_date: <span class="tok-fn">str</span>, end_date: <span class="tok-fn">str</span>, row_limit: <span class="tok-fn">int</span> = <span class="tok-val">25000</span>) -> pd.DataFrame:
    service = <span class="tok-fn">get_gsc_service</span>()

    request = {
        <span class="tok-str">"startDate"</span>: start_date,
        <span class="tok-str">"endDate"</span>: end_date,
        <span class="tok-str">"dimensions"</span>: [<span class="tok-str">"query"</span>, <span class="tok-str">"page"</span>],
        <span class="tok-str">"rowLimit"</span>: row_limit,
    }

    response = service.searchanalytics().query(siteUrl=site_url, body=request).execute()
    rows = response.get(<span class="tok-str">"rows"</span>, [])

    records = [{
        <span class="tok-str">"query"</span>: row[<span class="tok-str">"keys"</span>][<span class="tok-val">0</span>],
        <span class="tok-str">"page"</span>: row[<span class="tok-str">"keys"</span>][<span class="tok-val">1</span>],
        <span class="tok-str">"clicks"</span>: row[<span class="tok-str">"clicks"</span>],
        <span class="tok-str">"impressions"</span>: row[<span class="tok-str">"impressions"</span>],
        <span class="tok-str">"ctr"</span>: row[<span class="tok-str">"ctr"</span>],
        <span class="tok-str">"position"</span>: row[<span class="tok-str">"position"</span>],
    } <span class="tok-kw">for</span> row <span class="tok-kw">in</span> rows]

    <span class="tok-kw">return</span> pd.DataFrame(records)</code></pre>
  </div>

  <p>Splitting queries from <a href="/branded-queries-filter-in-search-console/" target="_blank" rel="noopener">branded queries</a> becomes trivial once this data sits in a dataframe instead of an export you have to filter by hand every time.</p>

  <div class="bx-section-head">
    <span class="bx-num">06</span>
    <h2 class="bx-h2" id="working-past-the-25-000-row-limit-with-pagination">Working Past the 25,000 Row Limit With Pagination</h2>
    <div class="bx-rule"></div>
  </div>

  <p>A single request tops out at 25,000 rows, and a busy site can easily have more query and page combinations than that in a single month. The <code>startRow</code> parameter is how you keep going past it.</p>

  <div class="bx-code-wrap">
    <div class="bx-code-title">pull_all_rows.py</div>
    <pre><code><span class="tok-kw">import</span> time
<span class="tok-kw">import</span> pandas <span class="tok-kw">as</span> pd
<span class="tok-kw">from</span> gsc_client <span class="tok-kw">import</span> get_gsc_service

<span class="tok-fn">PAGE_SIZE</span> = <span class="tok-val">25000</span>

<span class="tok-kw">def</span> <span class="tok-fn">pull_all_rows</span>(site_url: <span class="tok-fn">str</span>, start_date: <span class="tok-fn">str</span>, end_date: <span class="tok-fn">str</span>) -> pd.DataFrame:
    service = <span class="tok-fn">get_gsc_service</span>()
    all_rows = []
    start_row = <span class="tok-val">0</span>

    <span class="tok-kw">while</span> <span class="tok-kw">True</span>:
        request = {
            <span class="tok-str">"startDate"</span>: start_date,
            <span class="tok-str">"endDate"</span>: end_date,
            <span class="tok-str">"dimensions"</span>: [<span class="tok-str">"query"</span>, <span class="tok-str">"page"</span>],
            <span class="tok-str">"rowLimit"</span>: PAGE_SIZE,
            <span class="tok-str">"startRow"</span>: start_row,
        }
        response = service.searchanalytics().query(siteUrl=site_url, body=request).execute()
        rows = response.get(<span class="tok-str">"rows"</span>, [])

        <span class="tok-kw">if</span> <span class="tok-kw">not</span> rows:
            <span class="tok-kw">break</span>

        all_rows.extend(rows)
        start_row += PAGE_SIZE
        time.sleep(<span class="tok-val">1</span>)   <span class="tok-cm"># stay well under the daily quota</span>

    <span class="tok-kw">return</span> pd.DataFrame(all_rows)</code></pre>
  </div>

  <p>The loop stops the moment a page comes back empty, which is the API's own signal that there is nothing left to fetch. That is a cleaner stopping condition than guessing at a total row count in advance.</p>


  <div class="bx-section-head">
    <span class="bx-num">07</span>
    <h2 class="bx-h2" id="automating-multiple-properties-and-date-ranges">Automating Multiple Properties and Date Ranges</h2>
    <div class="bx-rule"></div>
  </div>

  <p>Most agencies and multi site owners are not pulling data for one property. The same function works for many, as long as the service account has been added to each one.</p>

  <div class="bx-code-wrap">
    <div class="bx-code-title">multi_property.py</div>
    <pre><code><span class="tok-kw">from</span> datetime <span class="tok-kw">import</span> date, timedelta
<span class="tok-kw">from</span> pull_all_rows <span class="tok-kw">import</span> pull_all_rows

<span class="tok-fn">SITES</span> = [
    <span class="tok-str">"https://brandella.in/"</span>,
    <span class="tok-str">"sc-domain:example-client.com"</span>,
]

<span class="tok-kw">def</span> <span class="tok-fn">run_daily_pull</span>():
    yesterday = (date.today() - timedelta(days=<span class="tok-val">3</span>)).isoformat()

    <span class="tok-kw">for</span> site <span class="tok-kw">in</span> SITES:
        df = <span class="tok-fn">pull_all_rows</span>(site, yesterday, yesterday)
        df[<span class="tok-str">"site"</span>] = site
        df[<span class="tok-str">"pull_date"</span>] = yesterday
        df.to_csv(<span class="tok-fn">f"data/{site.replace('/', '_')}_{yesterday}.csv"</span>, index=<span class="tok-kw">False</span>)</code></pre>
  </div>

  <p>Notice the three day offset in the date calculation. Search Console data is not final the moment a click happens, and pulling too close to today usually returns partial numbers that revise upward later.</p>

  <div class="bx-tool">
    <h3>Pagination Request Estimator</h3>
    <p class="bx-tool-sub">Estimate how many paginated API calls a pull needs, based on the API's 25,000 row limit per request.</p>
    <div class="bx-stepper">
      <button type="button" id="bx-step-down" aria-label="Decrease expected row count">−</button>
      <span id="bx-step-value">50,000 rows</span>
      <button type="button" id="bx-step-up" aria-label="Increase expected row count">+</button>
    </div>
    <div class="bx-tool-output">
      <div><span class="bx-out-num" id="bx-out-calls">2</span><span class="bx-out-label">Paginated requests needed</span></div>
      <div><span class="bx-out-num" id="bx-out-time">~2 sec</span><span class="bx-out-label">Estimated pull time at a 1 second delay</span></div>
    </div>
  </div>

  <div class="bx-section-head">
    <span class="bx-num">08</span>
    <h2 class="bx-h2" id="storing-results-beyond-the-dashboard-s-memory">Storing Results Beyond the Dashboard's Memory</h2>
    <div class="bx-rule"></div>
  </div>

  <p>Saving each day to its own CSV works, but it makes trend analysis harder than it needs to be. Once google search console data pulls with python are running daily, appending every pull into one growing table is usually the better long term shape. Our guide to <a href="/python-and-pandas-seo-reporting/">Python and Pandas SEO reporting</a> shows how to turn that table into a reusable dashboard.</p>

  <div class="bx-code-wrap">
    <div class="bx-code-title">append_to_archive.py</div>
    <pre><code><span class="tok-kw">import</span> os
<span class="tok-kw">import</span> pandas <span class="tok-kw">as</span> pd

<span class="tok-fn">ARCHIVE_PATH</span> = <span class="tok-str">"data/gsc_archive.csv"</span>

<span class="tok-kw">def</span> <span class="tok-fn">append_to_archive</span>(new_df: pd.DataFrame):
    <span class="tok-kw">if</span> os.path.exists(ARCHIVE_PATH):
        existing = pd.read_csv(ARCHIVE_PATH)
        combined = pd.concat([existing, new_df]).drop_duplicates(
            subset=[<span class="tok-str">"site"</span>, <span class="tok-str">"pull_date"</span>, <span class="tok-str">"query"</span>, <span class="tok-str">"page"</span>]
        )
    <span class="tok-kw">else</span>:
        combined = new_df

    combined.to_csv(ARCHIVE_PATH, index=<span class="tok-kw">False</span>)</code></pre>
  </div>

  <p>The <code>drop_duplicates</code> call matters more than it looks. A script that reruns after a partial failure should never double count a day it already saved successfully.</p>

  <div class="bx-code-wrap">
    <div class="bx-code-title">.github/workflows/gsc_pull.yml</div>
    <pre><code><span class="tok-prop">name</span>: <span class="tok-val">Daily Search Console Pull</span>
<span class="tok-prop">on</span>:
  <span class="tok-sel">schedule</span>:
    - <span class="tok-prop">cron</span>: <span class="tok-str">"0 8 * * *"</span>   <span class="tok-cm"># every day at 08:00 UTC</span>
  <span class="tok-sel">workflow_dispatch</span>: {}

<span class="tok-prop">jobs</span>:
  <span class="tok-sel">pull_data</span>:
    <span class="tok-prop">runs-on</span>: <span class="tok-val">ubuntu-latest</span>
    <span class="tok-prop">steps</span>:
      - <span class="tok-prop">uses</span>: <span class="tok-val">actions/checkout@v4</span>
      - <span class="tok-prop">uses</span>: <span class="tok-val">actions/setup-python@v5</span>
        <span class="tok-prop">with</span>:
          <span class="tok-prop">python-version</span>: <span class="tok-str">"3.11"</span>
      - <span class="tok-prop">run</span>: <span class="tok-val">pip install -r requirements.txt</span>
      - <span class="tok-prop">run</span>: <span class="tok-val">python multi_property.py</span></code></pre>
  </div>

  <p>A daily run through <a href="https://docs.github.com/en/actions" target="_blank" rel="noopener">GitHub Actions</a> means the archive keeps growing on its own, well past whatever window the Search Console interface happens to keep visible.</p>

  <div class="bx-section-head">
    <span class="bx-num">09</span>
    <h2 class="bx-h2" id="handling-quotas-data-lag-and-other-edge-cases">Handling Quotas, Data Lag, and Other Edge Cases</h2>
    <div class="bx-rule"></div>
  </div>

  <p>A few details separate a script that runs once from one that keeps running reliably every day without someone checking on it.</p>

  <ul class="bx-checklist">
    <li><b>Daily quota limits:</b> the API enforces a per project request quota. Spread large historical backfills across several days rather than requesting years of data in one run.</li>
    <li><b>Data freshness lag:</b> figures for the last two to three days are often incomplete. Pull with a delay, as shown in the multi property example above.</li>
    <li><b>Empty rows on new properties:</b> a property added recently may return nothing for older date ranges, which is expected rather than a bug in the script.</li>
    <li><b>Zero click, zero impression noise:</b> some low volume queries add little analytical value. Filter these out after the pull rather than during it, so the raw archive stays complete.</li>
    <li><b>Service account access changes:</b> if someone removes the service account from a property's user list, the script fails quietly with an empty result rather than a clear error.</li>
  </ul>

  <p>None of these are difficult to handle once you know to expect them. They are simply the parts that a first script, written in an afternoon, tends to miss. <a href="https://www.searchenginejournal.com/" target="_blank" rel="noopener">Search Engine Journal</a> has covered similar lag and quota issues across other Google reporting APIs, and the same patience pays off here too.</p>

  <div class="bx-section-head">
    <span class="bx-num">10</span>
    <h2 class="bx-h2" id="watch-connecting-to-the-search-console-api-with-python">Watch: Connecting to the Search Console API With Python</h2>
    <div class="bx-rule"></div>
  </div>

  <p>JC Chouinard, a Python and SEO practitioner whose tutorials at jcchouinard.com are widely referenced in the technical SEO community, published a walkthrough covering exactly the authentication step this guide starts with.</p>

  <div style="position:relative; padding-bottom:56.25%; height:0; overflow:hidden; border-radius:12px; margin:18px 0 8px;">
    <iframe src="https://www.youtube.com/embed/-uy4L4P1Ujs" title="Google Search Console API With Python, Get API Keys by JC Chouinard" style="position:absolute; top:0; left:0; width:100%; height:100%; border:0;" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen loading="lazy"></iframe>
  </div>
  <p style="font-size:14px; color:var(--bx-charcoal-soft); margin-top:6px;">Video credit: JC Chouinard, jcchouinard.com.</p>

  <p>The credential setup shown there is the same service account pattern used throughout this guide, just walked through one click at a time inside the Google Cloud console.</p>

  <svg width="100%" height="220" viewBox="0 0 800 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Diagram of google search console data pulls with python moving from service account authentication through paginated API requests to a stored archive" style="margin:26px 0;">
    <rect width="800" height="220" fill="#f4faef" rx="12"/>
    <g font-family="Open Sans, sans-serif" font-size="14" fill="#2b2b2b">
      <rect x="20" y="85" width="140" height="60" rx="8" fill="#ffffff" stroke="#5DB92E" stroke-width="2"/>
      <text x="90" y="112" text-anchor="middle" font-weight="700">Service Account</text>
      <text x="90" y="130" text-anchor="middle" font-weight="700">Auth</text>

      <line x1="160" y1="115" x2="210" y2="115" stroke="#4a9e24" stroke-width="2" marker-end="url(#arrow)"/>

      <rect x="210" y="85" width="150" height="60" rx="8" fill="#ffffff" stroke="#5DB92E" stroke-width="2"/>
      <text x="285" y="112" text-anchor="middle" font-weight="700">Paginated</text>
      <text x="285" y="130" text-anchor="middle" font-weight="700">searchanalytics.query</text>

      <line x1="360" y1="115" x2="410" y2="115" stroke="#4a9e24" stroke-width="2" marker-end="url(#arrow)"/>

      <rect x="410" y="85" width="140" height="60" rx="8" fill="#ffffff" stroke="#5DB92E" stroke-width="2"/>
      <text x="480" y="120" text-anchor="middle" font-weight="700">Pandas Dataframe</text>

      <line x1="550" y1="115" x2="600" y2="115" stroke="#4a9e24" stroke-width="2" marker-end="url(#arrow)"/>

      <rect x="600" y="85" width="170" height="60" rx="8" fill="#2b2b2b" stroke="#5DB92E" stroke-width="2"/>
      <text x="685" y="120" text-anchor="middle" font-weight="700" fill="#5DB92E">Growing CSV Archive</text>
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
      <button type="button" class="bx-faq-q">Do I need a Google Ads account to use the Search Console API?</button>
      <div class="bx-faq-a"><p>No. The Search Console API only needs a verified Search Console property and a Google Cloud project with the API enabled. It has no connection to Google Ads at all.</p></div>
    </div>
    <div class="bx-faq-item">
      <button type="button" class="bx-faq-q">Why does my script return an empty result with no error?</button>
      <div class="bx-faq-a"><p>This almost always means the service account was never added as a user on the Search Console property. Add its email address under Settings and Users and Permissions, and the same request will start returning rows.</p></div>
    </div>
    <div class="bx-faq-item">
      <button type="button" class="bx-faq-q">How do google search console data pulls with python handle the row limit?</button>
      <div class="bx-faq-a"><p>By paginating with the startRow parameter. Each request returns up to 25,000 rows, and looping with an increasing startRow value until an empty response comes back collects everything available.</p></div>
    </div>
    <div class="bx-faq-item">
      <button type="button" class="bx-faq-q">How far back can I pull historical Search Console data?</button>
      <div class="bx-faq-a"><p>The API generally exposes a similar window to what the interface shows, roughly sixteen months. The value of automating the pull is capturing new data going forward so future gaps never happen again.</p></div>
    </div>
    <div class="bx-faq-item">
      <button type="button" class="bx-faq-q">Should I use OAuth or a service account for this?</button>
      <div class="bx-faq-a"><p>A service account is usually better for anything scheduled and unattended, since it never expires the way a personal OAuth session can. OAuth makes more sense for a script you run interactively yourself.</p></div>
    </div>
  </div>

  <div class="bx-learn">
    <h2 id="what-we-learn-today">What We Learn Today</h2>
    <div class="bx-learn-grid">
      <div class="bx-learn-card"><span class="bx-learn-num">1</span><div><h4>The UI has real limits</h4><p>Row caps and a rolling history window make manual exports a poor long term data source.</p></div></div>
      <div class="bx-learn-card"><span class="bx-learn-num">2</span><div><h4>Access setup comes first</h4><p>The service account must be added to the property, or every later request comes back empty.</p></div></div>
      <div class="bx-learn-card"><span class="bx-learn-num">3</span><div><h4>Pagination is not optional</h4><p>The 25,000 row cap per request means most real pulls need a loop, not a single call.</p></div></div>
      <div class="bx-learn-card"><span class="bx-learn-num">4</span><div><h4>Data lag is real</h4><p>Pulling with a few days of delay avoids saving numbers that have not finished settling.</p></div></div>
      <div class="bx-learn-card"><span class="bx-learn-num">5</span><div><h4>Archiving beats exporting again</h4><p>Appending daily pulls into one deduplicated table builds history the dashboard cannot offer.</p></div></div>
      <div class="bx-learn-card"><span class="bx-learn-num">6</span><div><h4>Scheduling makes it durable</h4><p>A daily GitHub Actions run keeps the archive current without anyone remembering to click export.</p></div></div>
    </div>
  </div>


  <div class="bx-cta">
    <h3>Ready to Stop Losing Search Console History?</h3>
    <p>Pair google search console data pulls with python and a broader reporting workflow to keep every metric that matters within reach.</p>
    <div class="bx-cta-btns">
      <a href="/google-search-console-ai-powered-configuration/" target="_blank" rel="noopener">Read the GSC Configuration Guide</a>
      <a href="/google-analytics-4-metrics-explained-beginners/" target="_blank" rel="noopener" class="bx-cta-outline">Explore GA4 Metrics</a>
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

  var stepValue = document.getElementById('bx-step-value');
  var outCalls = document.getElementById('bx-out-calls');
  var outTime = document.getElementById('bx-out-time');
  var rows = 50000;
  var pageSize = 25000;
  var delaySeconds = 1;

  function render() {
    stepValue.textContent = rows.toLocaleString() + ' rows';
    var calls = Math.max(1, Math.ceil(rows / pageSize));
    outCalls.textContent = calls;
    var totalSeconds = calls * delaySeconds;
    outTime.textContent = totalSeconds < 60 ? ('~' + totalSeconds + ' sec') : ('~' + (totalSeconds / 60).toFixed(1) + ' min');
  }

  document.getElementById('bx-step-up').addEventListener('click', function() {
    rows = Math.min(rows + 25000, 1000000);
    render();
  });
  document.getElementById('bx-step-down').addEventListener('click', function() {
    rows = Math.max(rows - 25000, 25000);
    render();
  });

  render();
})();
</script>
