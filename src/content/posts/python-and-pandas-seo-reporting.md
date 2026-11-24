---
title: "Python and Pandas for SEO Reporting: Automate Dashboards in 6 Steps"
slug: "python-and-pandas-seo-reporting"
date: "2026-08-25T07:46:37"
updated: "2026-08-25T07:47:15"
author: "santajigade"
categories: ["development", "python"]
primaryCategory: "development"
description: "Learn how to use python and pandas for SEO reporting to pull Search Console and GA4 data, merge it, and automate client dashboards."
focusKeyword: "Python and Pandas"
takeaways:
  - "Python and pandas can replace manual copying of Search Console and analytics data into monthly client reports."
  - "The Search Console API and Google's google-analytics-data client for GA4 together cover most of what a client report needs."
  - "Cleaning keys and filling missing values with fillna prevents blank cells from breaking merges and later calculations."
  - "Month over month change columns matter more to clients than raw totals, and a replace(0, 1) guard prevents division by zero."
  - "A GitHub Actions cron job can generate every report on the first day of each month, with credentials stored as secrets."
image: "/wp-content/uploads/2026/08/Python-and-Pandas.webp"
imageAlt: "Python and Pandas"
words: 1752
views: 42
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
    <span class="bx-pill">Pandas</span>
    <span class="bx-pill">SEO Reporting</span>
  </div>

  <p class="bx-lede">Copying numbers from Search Console into a slide deck every Monday morning is not reporting, it is data entry. Python and pandas for SEO reporting turns that same weekly task into a script that runs in minutes and never mistypes a cell.</p>

  <div class="bx-section-head">
    <span class="bx-num">01</span>
    <h2 class="bx-h2" id="why-python-and-pandas-for-seo-reporting-beats-the-manual-client-deck">Why Python and Pandas for SEO Reporting Beats the Manual Client Deck</h2>
    <div class="bx-rule"></div>
  </div>

  <p>An agency managing a dozen client accounts spends a real chunk of every month on reporting. Someone exports Search Console data, exports analytics data, and pastes both into a spreadsheet by hand.</p>

  <p>Then the same person builds a chart, writes a summary, and repeats the whole process for the next client. Nothing about that process changes month to month except the numbers.</p>

  <p>A script replaces the copying step entirely. It pulls the same two data sources, merges them, calculates the same comparisons, and writes the same report shape every time.</p>

  <p>The person who used to spend a day on reporting spends that day on the parts a script cannot do, reading the numbers and deciding what they mean for the client.</p>


  <div class="bx-section-head">
    <span class="bx-num">02</span>
    <h2 class="bx-h2" id="setting-up-your-python-environment">Setting Up Your Python Environment</h2>
    <div class="bx-rule"></div>
  </div>

  <p>Four libraries cover the whole pipeline in this guide, from pulling data to writing the finished report.</p>

  <div class="bx-code-wrap">
    <div class="bx-code-title">terminal</div>
    <pre><code><span class="tok-cm"># create an isolated environment so package versions don't clash</span>
python -m venv venv
<span class="tok-val">source</span> venv/bin/activate      <span class="tok-cm"># Windows: venv\Scripts\activate</span>

pip install pandas google-api-python-client google-analytics-data openpyxl matplotlib</code></pre>
  </div>

  <p>The <a href="https://pandas.pydata.org/docs/" target="_blank" rel="noopener"><code>pandas</code></a> library does the merging and math. <a href="https://github.com/googleapis/google-api-python-client" target="_blank" rel="noopener"><code>google-api-python-client</code></a> talks to Search Console, and <a href="https://pypi.org/project/google-analytics-data/" target="_blank" rel="noopener"><code>google-analytics-data</code></a> is Google's official client for pulling Google Analytics 4 data. <a href="https://openpyxl.readthedocs.io/en/stable/" target="_blank" rel="noopener"><code>openpyxl</code></a> writes a formatted spreadsheet, and <a href="https://matplotlib.org/stable/" target="_blank" rel="noopener"><code>matplotlib</code></a> draws the trend chart.</p>

  <p>All four are documented in full on the <a href="https://pypi.org/" target="_blank" rel="noopener">Python Package Index</a>, which is worth bookmarking before the first run in case a version pin needs checking later.</p>

  <div class="bx-section-head">
    <span class="bx-num">03</span>
    <h2 class="bx-h2" id="pulling-search-console-data">Pulling Search Console Data</h2>
    <div class="bx-rule"></div>
  </div>

  <p>The <a href="https://developers.google.com/webmaster-tools/search-console-api-original" target="_blank" rel="noopener">Search Console API</a> returns clicks, impressions, and average position for a date range, one row per query or page depending on the dimension requested.</p>

  <div class="bx-code-wrap">
    <div class="bx-code-title">gsc_pull.py</div>
    <pre><code><span class="tok-kw">from</span> google.oauth2 <span class="tok-kw">import</span> service_account
<span class="tok-kw">from</span> googleapiclient.discovery <span class="tok-kw">import</span> build
<span class="tok-kw">import</span> pandas <span class="tok-kw">as</span> pd

SCOPES = [<span class="tok-str">'https://www.googleapis.com/auth/webmasters.readonly'</span>]
creds = service_account.Credentials.from_service_account_file(
    <span class="tok-str">'service_account.json'</span>, scopes=SCOPES
)
service = build(<span class="tok-str">'searchconsole'</span>, <span class="tok-str">'v1'</span>, credentials=creds)

<span class="tok-kw">def</span> <span class="tok-fn">get_gsc_data</span>(site_url, start_date, end_date):
    request = {
        <span class="tok-str">'startDate'</span>: start_date,
        <span class="tok-str">'endDate'</span>: end_date,
        <span class="tok-str">'dimensions'</span>: [<span class="tok-str">'query'</span>],
        <span class="tok-str">'rowLimit'</span>: 5000
    }
    response = service.searchanalytics().query(
        siteUrl=site_url, body=request
    ).execute()
    rows = response.get(<span class="tok-str">'rows'</span>, [])
    <span class="tok-kw">return</span> pd.DataFrame([{
        <span class="tok-str">'query'</span>: r[<span class="tok-str">'keys'</span>][0],
        <span class="tok-str">'clicks'</span>: r[<span class="tok-str">'clicks'</span>],
        <span class="tok-str">'impressions'</span>: r[<span class="tok-str">'impressions'</span>],
        <span class="tok-str">'position'</span>: <span class="tok-fn">round</span>(r[<span class="tok-str">'position'</span>], 1)
    } <span class="tok-kw">for</span> r <span class="tok-kw">in</span> rows])</code></pre>
  </div>

  <p>Running this once for the current month and again for the prior month gives two data frames ready to compare, which is exactly what the report needs.</p>

  <div class="bx-section-head">
    <span class="bx-num">04</span>
    <h2 class="bx-h2" id="pulling-google-analytics-4-data">Pulling Google Analytics 4 Data</h2>
    <div class="bx-rule"></div>
  </div>

  <p>Google's official <code>google-analytics-data</code> client wraps the <a href="https://developers.google.com/analytics/devguides/reporting/data/v1" target="_blank" rel="noopener">GA4 Data API</a> and returns sessions, users, and conversions in a similar shape to the Search Console pull.</p>

  <div class="bx-code-wrap">
    <div class="bx-code-title">ga4_pull.py</div>
    <pre><code><span class="tok-kw">from</span> google.analytics.data_v1beta <span class="tok-kw">import</span> BetaAnalyticsDataClient
<span class="tok-kw">from</span> google.analytics.data_v1beta.types <span class="tok-kw">import</span> RunReportRequest, DateRange, Dimension, Metric
<span class="tok-kw">import</span> pandas <span class="tok-kw">as</span> pd

client = BetaAnalyticsDataClient()

<span class="tok-kw">def</span> <span class="tok-fn">get_ga4_data</span>(property_id, start_date, end_date):
    request = RunReportRequest(
        property=<span class="tok-fn">f</span><span class="tok-str">'properties/{property_id}'</span>,
        dimensions=[Dimension(name=<span class="tok-str">'landingPage'</span>)],
        metrics=[Metric(name=<span class="tok-str">'sessions'</span>), Metric(name=<span class="tok-str">'conversions'</span>)],
        date_ranges=[DateRange(start_date=start_date, end_date=end_date)]
    )
    response = client.run_report(request)
    rows = []
    <span class="tok-kw">for</span> row <span class="tok-kw">in</span> response.rows:
        rows.append({
            <span class="tok-str">'landing_page'</span>: row.dimension_values[0].value,
            <span class="tok-str">'sessions'</span>: <span class="tok-fn">int</span>(row.metric_values[0].value),
            <span class="tok-str">'conversions'</span>: <span class="tok-fn">float</span>(row.metric_values[1].value)
        })
    <span class="tok-kw">return</span> pd.DataFrame(rows)</code></pre>
  </div>

  <p>The property ID and a service account with API access are the only setup pieces here, since the request shape stays the same across every client property.</p>

  <div class="bx-section-head">
    <span class="bx-num">05</span>
    <h2 class="bx-h2" id="merging-and-cleaning-the-data-with-pandas">Merging and Cleaning the Data With Pandas</h2>
    <div class="bx-rule"></div>
  </div>

  <p>Search Console rows and GA4 rows rarely line up on the same key out of the box, so a short cleaning step makes the merge reliable.</p>

  <div class="bx-code-wrap">
    <div class="bx-code-title">merge_data.py</div>
    <pre><code><span class="tok-kw">import</span> pandas <span class="tok-kw">as</span> pd

<span class="tok-kw">def</span> <span class="tok-fn">build_report_frame</span>(gsc_df, ga4_df):
    gsc_df[<span class="tok-str">'query'</span>] = gsc_df[<span class="tok-str">'query'</span>].<span class="tok-fn">str</span>.strip().<span class="tok-fn">str</span>.lower()
    combined = pd.concat([gsc_df], ignore_index=<span class="tok-val">True</span>)
    combined[<span class="tok-str">'clicks'</span>] = combined[<span class="tok-str">'clicks'</span>].fillna(0).astype(<span class="tok-fn">int</span>)
    combined[<span class="tok-str">'impressions'</span>] = combined[<span class="tok-str">'impressions'</span>].fillna(0).astype(<span class="tok-fn">int</span>)
    <span class="tok-kw">return</span> combined.sort_values(<span class="tok-str">'clicks'</span>, ascending=<span class="tok-val">False</span>)</code></pre>
  </div>

  <p><code>fillna</code> matters here because a query that had impressions but zero clicks sometimes comes back missing entirely rather than as a literal zero, and an uncaught blank cell breaks every calculation after it.</p>

  <div class="bx-section-head">
    <span class="bx-num">06</span>
    <h2 class="bx-h2" id="calculating-month-over-month-change">Calculating Month Over Month Change</h2>
    <div class="bx-rule"></div>
  </div>

  <p>Clients care less about the raw numbers than about the direction they moved, so the report needs a comparison column, not just two tables side by side.</p>

  <div class="bx-code-wrap">
    <div class="bx-code-title">compare_periods.py</div>
    <pre><code><span class="tok-kw">import</span> pandas <span class="tok-kw">as</span> pd

<span class="tok-kw">def</span> <span class="tok-fn">compare_periods</span>(current_df, previous_df, key, metric):
    merged = current_df.merge(
        previous_df, on=key, suffixes=(<span class="tok-str">'_now'</span>, <span class="tok-str">'_prev'</span>), how=<span class="tok-str">'outer'</span>
    ).fillna(0)
    merged[<span class="tok-fn">f</span><span class="tok-str">'{metric}_change'</span>] = merged[<span class="tok-fn">f</span><span class="tok-str">'{metric}_now'</span>] - merged[<span class="tok-fn">f</span><span class="tok-str">'{metric}_prev'</span>]
    merged[<span class="tok-fn">f</span><span class="tok-str">'{metric}_pct_change'</span>] = (
        merged[<span class="tok-fn">f</span><span class="tok-str">'{metric}_change'</span>] / merged[<span class="tok-fn">f</span><span class="tok-str">'{metric}_prev'</span>].<span class="tok-fn">replace</span>(0, 1) * 100
    ).<span class="tok-fn">round</span>(1)
    <span class="tok-kw">return</span> merged.sort_values(<span class="tok-fn">f</span><span class="tok-str">'{metric}_change'</span>, ascending=<span class="tok-val">False</span>)</code></pre>
  </div>

  <p>The <code>replace(0, 1)</code> guard stops a division by zero from crashing the script the first time a query shows up with no prior month history at all.</p>

  <div class="bx-table-wrap">
    <table class="bx-table">
      <thead><tr><th>Report Element</th><th>Data Source</th><th>What It Shows the Client</th></tr></thead>
      <tbody>
        <tr><td>Clicks and impressions trend</td><td>Search Console API</td><td>Whether visibility grew or shrank this month</td></tr>
        <tr><td>Top movers table</td><td>Search Console + pandas merge</td><td>Which queries gained or lost the most clicks</td></tr>
        <tr><td>Landing page sessions</td><td>GA4 Data API</td><td>Which pages carried the organic traffic</td></tr>
        <tr><td>Conversion summary</td><td>GA4 Data API</td><td>Whether the traffic actually converted</td></tr>
      </tbody>
    </table>
  </div>

  <div class="bx-section-head">
    <span class="bx-num">07</span>
    <h2 class="bx-h2" id="writing-the-client-ready-report">Writing the Client Ready Report</h2>
    <div class="bx-rule"></div>
  </div>

  <p>A finished pandas data frame can become a formatted spreadsheet in a few lines, complete with a chart the client can open without any setup on their end. <a href="https://www.searchenginejournal.com/seo-reporting/" target="_blank" rel="noopener">Search Engine Journal's guide to SEO reporting</a> covers what most clients actually want to see in a report, which is worth checking against the layout a script produces.</p>

  <div class="bx-code-wrap">
    <div class="bx-code-title">build_report.py</div>
    <pre><code><span class="tok-kw">import</span> pandas <span class="tok-kw">as</span> pd
<span class="tok-kw">import</span> matplotlib.pyplot <span class="tok-kw">as</span> plt

<span class="tok-kw">def</span> <span class="tok-fn">write_excel_report</span>(report_df, client_name, output_path):
    <span class="tok-kw">with</span> pd.ExcelWriter(output_path, engine=<span class="tok-str">'openpyxl'</span>) <span class="tok-kw">as</span> writer:
        report_df.to_excel(writer, sheet_name=<span class="tok-str">'Query Performance'</span>, index=<span class="tok-val">False</span>)

<span class="tok-kw">def</span> <span class="tok-fn">save_trend_chart</span>(monthly_totals, output_path):
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(monthly_totals[<span class="tok-str">'month'</span>], monthly_totals[<span class="tok-str">'clicks'</span>], marker=<span class="tok-str">'o'</span>, color=<span class="tok-str">'#4a9e24'</span>)
    ax.set_title(<span class="tok-str">'Organic Clicks by Month'</span>)
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)</code></pre>
  </div>

  <p>Every client gets the exact same file structure, so opening last month's report and this month's report side by side always feels familiar rather than like a new document to learn.</p>

  <div class="bx-tool">
    <h3>Reporting Time Saved Calculator</h3>
    <p class="bx-tool-sub">Estimate the hours reclaimed each month by automating client reports with python and pandas for SEO reporting.</p>
    <div class="bx-stepper">
      <button type="button" id="bx-client-down" aria-label="Decrease client count">−</button>
      <span id="bx-client-value">10 clients</span>
      <button type="button" id="bx-client-up" aria-label="Increase client count">+</button>
    </div>
    <div class="bx-stepper">
      <button type="button" id="bx-hours-down" aria-label="Decrease hours per report">−</button>
      <span id="bx-hours-value">2 hours per report</span>
      <button type="button" id="bx-hours-up" aria-label="Increase hours per report">+</button>
    </div>
    <div class="bx-tool-output">
      <div><span class="bx-out-num" id="bx-out-hours">20</span><span class="bx-out-label">Hours saved per month</span></div>
      <div><span class="bx-out-num" id="bx-out-days">2.5</span><span class="bx-out-label">Working days reclaimed</span></div>
    </div>
  </div>


  <div class="bx-section-head">
    <span class="bx-num">08</span>
    <h2 class="bx-h2" id="scheduling-the-report-to-run-automatically">Scheduling the Report to Run Automatically</h2>
    <div class="bx-rule"></div>
  </div>

  <p>A script that still needs someone to remember to run it every month has only solved half the problem, so scheduling through <a href="https://docs.github.com/en/actions" target="_blank" rel="noopener">GitHub Actions</a> closes the loop.</p>

  <div class="bx-code-wrap">
    <div class="bx-code-title">.github/workflows/seo_report.yml</div>
    <pre><code><span class="tok-sel">name</span>: <span class="tok-str">Monthly SEO Report</span>
<span class="tok-sel">on</span>:
  <span class="tok-sel">schedule</span>:
    <span class="tok-prop">-</span> <span class="tok-str">cron: '0 6 1 * *'</span>
<span class="tok-sel">jobs</span>:
  <span class="tok-sel">build_report</span>:
    <span class="tok-prop">runs</span><span class="tok-val">-on</span>: <span class="tok-str">ubuntu-latest</span>
    <span class="tok-sel">steps</span>:
      <span class="tok-prop">-</span> <span class="tok-str">uses: actions/checkout@v4</span>
      <span class="tok-prop">-</span> <span class="tok-str">run: pip install -r requirements.txt</span>
      <span class="tok-prop">-</span> <span class="tok-str">run: python build_report.py</span></code></pre>
  </div>

  <p>The cron entry runs on the first day of every month, so each client report is already sitting in the output folder before anyone thinks to ask for it.</p>

  <ul class="bx-checklist">
    <li><b>Store credentials as secrets:</b> the service account JSON and property IDs belong in GitHub Actions secrets, never committed to the repository.</li>
    <li><b>Keep one config file per client:</b> a small YAML or JSON file per client keeps the same script reusable across every account.</li>
    <li><b>Log failures loudly:</b> a report that silently fails to generate is worse than one that never existed, since nobody notices until a client asks.</li>
    <li><b>Version the output folder:</b> keeping a dated copy of every report makes it trivial to compare against any past month, not just the previous one.</li>
    <li><b>Review before sending:</b> automation builds the report, but a quick human glance before it reaches a client catches the occasional odd number an API returned.</li>
  </ul>

  <div class="bx-section-head">
    <span class="bx-num">09</span>
    <h2 class="bx-h2" id="watch-python-for-seo-in-practice">Watch: Python for SEO in Practice</h2>
    <div class="bx-rule"></div>
  </div>

  <p>JC Chouinard, whose Search Console API examples this series has referenced before, has also spoken publicly about applying Python across everyday SEO reporting work.</p>

  <div style="position:relative; padding-bottom:56.25%; height:0; overflow:hidden; border-radius:12px; margin:18px 0 8px;">
    <iframe src="https://www.youtube.com/embed/HB-KD0ATsGg" title="Jean-Christophe Chouinard on Python for SEO" style="position:absolute; top:0; left:0; width:100%; height:100%; border:0;" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen loading="lazy"></iframe>
  </div>
  <p style="font-size:14px; color:var(--bx-charcoal-soft); margin-top:6px;">Video credit: JC Chouinard.</p>

  <p>The same merge and compare pattern shown in this guide extends easily to a third data source, like a rank tracking export, once the two API pulls above feel familiar.</p>

  <svg width="100%" height="220" viewBox="0 0 800 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Diagram of python and pandas for SEO reporting moving from Search Console and GA4 APIs through a pandas merge to a finished client report" style="margin:26px 0;">
    <rect width="800" height="220" fill="#f4faef" rx="12"/>
    <g font-family="Open Sans, sans-serif" font-size="13" fill="#2b2b2b">
      <rect x="20" y="70" width="140" height="45" rx="8" fill="#ffffff" stroke="#5DB92E" stroke-width="2"/>
      <text x="90" y="97" text-anchor="middle" font-weight="700">Search Console API</text>

      <rect x="20" y="130" width="140" height="45" rx="8" fill="#ffffff" stroke="#5DB92E" stroke-width="2"/>
      <text x="90" y="157" text-anchor="middle" font-weight="700">GA4 Data API</text>

      <line x1="160" y1="92" x2="230" y2="105" stroke="#4a9e24" stroke-width="2" marker-end="url(#arrow)"/>
      <line x1="160" y1="152" x2="230" y2="118" stroke="#4a9e24" stroke-width="2" marker-end="url(#arrow)"/>

      <rect x="230" y="85" width="150" height="60" rx="8" fill="#ffffff" stroke="#5DB92E" stroke-width="2"/>
      <text x="305" y="112" text-anchor="middle" font-weight="700">Pandas Merge</text>
      <text x="305" y="130" text-anchor="middle" font-weight="700">and Compare</text>

      <line x1="380" y1="115" x2="430" y2="115" stroke="#4a9e24" stroke-width="2" marker-end="url(#arrow)"/>

      <rect x="430" y="85" width="150" height="60" rx="8" fill="#ffffff" stroke="#5DB92E" stroke-width="2"/>
      <text x="505" y="112" text-anchor="middle" font-weight="700">Excel Report</text>
      <text x="505" y="130" text-anchor="middle" font-weight="700">and Chart</text>

      <line x1="580" y1="115" x2="630" y2="115" stroke="#4a9e24" stroke-width="2" marker-end="url(#arrow)"/>

      <rect x="630" y="85" width="150" height="60" rx="8" fill="#2b2b2b" stroke="#5DB92E" stroke-width="2"/>
      <text x="705" y="120" text-anchor="middle" font-weight="700" fill="#5DB92E">Client Delivery</text>
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
      <button type="button" class="bx-faq-q">Do I need paid API access for Search Console and GA4?</button>
      <div class="bx-faq-a"><p>No. Both the Search Console API and the GA4 Data API are free to use within their standard quotas, which comfortably cover a typical agency reporting workload.</p></div>
    </div>
    <div class="bx-faq-item">
      <button type="button" class="bx-faq-q">Why use python and pandas for seo reporting instead of a dashboard tool?</button>
      <div class="bx-faq-a"><p>A dashboard tool works well for live exploration, but a scripted report gives full control over layout, wording, and exactly which metrics reach the client, with no subscription cost per seat.</p></div>
    </div>
    <div class="bx-faq-item">
      <button type="button" class="bx-faq-q">Can this same script handle more than one client?</button>
      <div class="bx-faq-a"><p>Yes. Looping the pull and merge functions across a list of client site URLs and property IDs is the most common way agencies scale this exact setup.</p></div>
    </div>
    <div class="bx-faq-item">
      <button type="button" class="bx-faq-q">What happens if an API call fails partway through?</button>
      <div class="bx-faq-a"><p>Wrapping each API call in a try block and logging the client name on failure keeps one broken pull from stopping every other client's report that same run.</p></div>
    </div>
    <div class="bx-faq-item">
      <button type="button" class="bx-faq-q">Is Excel the only output format this approach supports?</button>
      <div class="bx-faq-a"><p>No. The same data frame can just as easily become a PDF, an HTML email body, or a slide, since pandas is only responsible for the numbers, not the final file format.</p></div>
    </div>
  </div>

  <div class="bx-learn">
    <h2 id="what-we-learn-today">What We Learn Today</h2>
    <div class="bx-learn-grid">
      <div class="bx-learn-card"><span class="bx-learn-num">1</span><div><h4>Manual reporting does not scale</h4><p>Copying numbers by hand caps how many clients one person can realistically report on.</p></div></div>
      <div class="bx-learn-card"><span class="bx-learn-num">2</span><div><h4>Two APIs cover most reports</h4><p>Search Console and GA4 together answer most of what a client wants to know.</p></div></div>
      <div class="bx-learn-card"><span class="bx-learn-num">3</span><div><h4>Merging needs cleaning first</h4><p>Mismatched keys and missing values break a merge before it even runs.</p></div></div>
      <div class="bx-learn-card"><span class="bx-learn-num">4</span><div><h4>Change matters more than totals</h4><p>Clients respond to direction and movement, not a single raw number.</p></div></div>
      <div class="bx-learn-card"><span class="bx-learn-num">5</span><div><h4>The output format is flexible</h4><p>The same data frame can become a spreadsheet, a PDF, or an email body.</p></div></div>
      <div class="bx-learn-card"><span class="bx-learn-num">6</span><div><h4>Scheduling closes the loop</h4><p>A report nobody has to remember to run is the actual automation win.</p></div></div>
    </div>
  </div>


  <div class="bx-cta">
    <h3>Ready to Automate Your Client Reporting?</h3>
    <p>Pair python and pandas for SEO reporting with a wider toolkit to keep every client dashboard current without the manual work.</p>
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

  var clients = 10;
  var hours = 2;
  var clientVal = document.getElementById('bx-client-value');
  var hoursVal = document.getElementById('bx-hours-value');
  var outHours = document.getElementById('bx-out-hours');
  var outDays = document.getElementById('bx-out-days');

  function render() {
    clientVal.textContent = clients + ' client' + (clients === 1 ? '' : 's');
    hoursVal.textContent = hours + ' hour' + (hours === 1 ? '' : 's') + ' per report';
    var totalHours = clients * hours;
    outHours.textContent = totalHours;
    outDays.textContent = (totalHours / 8).toFixed(1);
  }

  document.getElementById('bx-client-up').addEventListener('click', function() {
    if (clients < 100) clients += 5;
    render();
  });
  document.getElementById('bx-client-down').addEventListener('click', function() {
    if (clients > 5) clients -= 5;
    render();
  });
  document.getElementById('bx-hours-up').addEventListener('click', function() {
    if (hours < 8) hours += 1;
    render();
  });
  document.getElementById('bx-hours-down').addEventListener('click', function() {
    if (hours > 1) hours -= 1;
    render();
  });

  render();
})();
</script>
