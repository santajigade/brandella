"""Site Speed Wins Kit workbook (asset 14): a Core Web Vitals checklist that ranks fixes by impact and effort.

Templates: one row per page template and device with field data at the 75th percentile (LCP, INP, CLS, TTFB),
traffic, the LCP element and the four LCP subparts. The sheet rates every metric with Google's thresholds, gives
a speed score, finds the LCP subpart that is furthest over its ideal share, suggests the first fix and lists red flags.
Speed Wins: one row per fix (500 rows). Each fix comes from the Fix Library (38 fixes from web.dev guidance) or your
own list. The sheet looks up the metric, the template's current status, traffic and revenue weight, then works out
value, priority score, P1 to P4, a quadrant (quick win, big bet, small task, avoid for now), the date field data is
ready (shipped date plus the 28 day CrUX window) and whether the fix worked.
Sprint Plan turns wins into tickets with a weekly capacity check. Dashboard sums it all up.
"""
import datetime
from openpyxl.styles import PatternFill, Font, Alignment
from openpyxl.formatting.rule import CellIsRule, ColorScaleRule, FormulaRule
from openpyxl.chart import BarChart, Reference
from openpyxl.utils import get_column_letter as L
import kitlib as K

TP_FIRST, TP_LAST = 5, 104     # Templates (100 rows)
SW_FIRST, SW_LAST = 5, 504     # Speed Wins (500 rows)
FL_FIRST, FL_LAST = 5, 64      # Fix Library (60 rows)
SP_FIRST, SP_LAST = 5, 104     # Sprint Plan (100 rows)
S = 'Settings'
TPS = 'Templates'
SWS = "'Speed Wins'"
FLS = "'Fix Library'"

DATE, WINDOW, CAP, P1, P2, P3, QV, QE, REV, BLANKF = (f'{S}!$B${r}' for r in range(5, 15))
THR = f'{S}!$F$6:$H$10'
STAT_RNG = f'{S}!$F$14:$G$17'
IMP_RNG = f'{S}!$F$21:$G$23'
EFF_RNG = f'{S}!$F$27:$G$30'
CONF_RNG = f'{S}!$F$34:$G$36'
TRAF_RNG = f'{S}!$F$40:$G$43'
SUB_RNG = f'{S}!$K$6:$M$9'
G = {m: (f'{S}!$G${r}', f'{S}!$H${r}') for m, r in (('LCP', 6), ('INP', 7), ('CLS', 8), ('TTFB', 9), ('FCP', 10))}
IDEAL = {k: f'{S}!$L${r}' for k, r in (('ttfb', 6), ('delay', 7), ('dur', 8), ('render', 9))}

THRESHOLDS = [('LCP', 2.5, 4, 'seconds'), ('INP', 200, 500, 'milliseconds'), ('CLS', 0.1, 0.25, 'unitless score'),
              ('TTFB', 800, 1800, 'milliseconds (experimental in PageSpeed Insights)'), ('FCP', 1.8, 3, 'seconds (not a Core Web Vital)')]
STATUS = [('Good', 0.2), ('Needs improvement', 0.6), ('Poor', 1), ('No data', 0.5)]
IMPACT = [('High', 3), ('Medium', 2), ('Low', 1)]
EFFORT = [('S', 1, 'Under a day'), ('M', 2, 'A few days'), ('L', 3, 'One to two weeks'), ('XL', 5, 'A project')]
CONF = [('High', 1), ('Medium', 0.8), ('Low', 0.5)]
TRAFFIC = [(0, 0.2), (0.05, 0.5), (0.15, 0.8), (0.3, 1)]
SUBPARTS = [('Time to first byte', 0.4, 'Cache HTML on a CDN, remove redirects and speed up server work'),
            ('Resource load delay', 0.1, 'Put the LCP image in the initial HTML, add fetchpriority high and never lazy load it'),
            ('Resource load duration', 0.4, 'Compress the LCP image, use WebP or AVIF and serve responsive sizes from a CDN'),
            ('Element render delay', 0.1, 'Cut render blocking CSS and JavaScript, server render the main content, break up long tasks')]
DEVICES = ['Mobile', 'Desktop']
STATUSES = ['Idea', 'Planned', 'In progress', 'Shipped', 'Validated', 'Dropped']
OWNERS = ['Developer', 'SEO', 'Hosting or IT', 'Design', 'Marketing']
SOURCES = ['CrUX URL', 'CrUX origin', 'Search Console group', 'RUM', 'Lab only']
ELEMENTS = ['Image', 'Text', 'Video', 'Background image']
YNI = ['Yes', 'No', 'Not an image']
METHODS = ['CrUX field data (28 days)', 'Search Console Validate fix', 'PageSpeed Insights lab', 'RUM (web-vitals)', 'DevTools Performance panel', 'Manual check']
WEEKS = [f'Week {i}' for i in range(1, 9)]
METRICS = ['LCP', 'INP', 'CLS', 'TTFB', 'All']
VRES = ['Not started', 'Passed', 'Failed']

# id, metric, part, fix, how to check, impact, effort, source
FIXES = [
    ('SP01', 'LCP', 'Resource load delay', 'Put the LCP image in the initial HTML with src or srcset (not data-src or a JavaScript slider)', 'View source: the LCP image URL is in the HTML the server sends', 'High', 'S', 'web.dev Optimize LCP'),
    ('SP02', 'LCP', 'Resource load delay', 'Add fetchpriority="high" to the LCP image (one or two images at most)', 'DevTools Network: the LCP image has High priority and starts early', 'High', 'S', 'web.dev Optimize LCP'),
    ('SP03', 'LCP', 'Resource load delay', 'Remove loading="lazy" from the LCP image', 'Inspect the LCP img element', 'High', 'S', 'web.dev Optimize LCP'),
    ('SP04', 'LCP', 'Resource load delay', 'Preload the LCP image when CSS or JavaScript references it (background images)', 'A link rel="preload" with fetchpriority high in the head', 'High', 'S', 'web.dev Optimize LCP'),
    ('SP05', 'LCP', 'Resource load delay', 'Host the LCP image on the same origin or preconnect to its host', 'DevTools Network: no slow connection setup before the image', 'Medium', 'S', 'web.dev Optimize LCP'),
    ('SP06', 'LCP', 'Element render delay', 'Server render or prerender the main content instead of building it with client side JavaScript', 'View source shows the main text and LCP element', 'High', 'XL', 'web.dev Top Core Web Vitals'),
    ('SP07', 'LCP', 'Element render delay', 'Defer or remove synchronous JavaScript in the head', 'Lighthouse: no render blocking scripts', 'High', 'M', 'web.dev Optimize LCP'),
    ('SP08', 'LCP', 'Element render delay', 'Reduce render blocking CSS; inline only small critical CSS', 'Lighthouse render blocking resources audit', 'Medium', 'M', 'web.dev Optimize LCP'),
    ('SP09', 'LCP', 'Element render delay', 'Break up long main thread tasks during page load', 'DevTools Performance: no long tasks before LCP', 'Medium', 'L', 'web.dev Optimize LCP'),
    ('SP10', 'LCP', 'Resource load duration', 'Compress the LCP image and serve WebP or AVIF', 'Image bytes compared before and after', 'Medium', 'S', 'web.dev Optimize LCP'),
    ('SP11', 'LCP', 'Resource load duration', 'Serve responsive sizes with srcset and sizes', 'Phones download a phone sized image', 'Medium', 'M', 'web.dev Optimize LCP'),
    ('SP12', 'LCP', 'Resource load duration', 'Serve images from an image CDN', 'Image response headers show the CDN', 'Medium', 'M', 'web.dev Optimize LCP'),
    ('SP13', 'LCP', 'Element render delay', 'Use font-display swap or optional and preload the main web font (text LCP)', 'Text shows while the font loads', 'Medium', 'S', 'web.dev Optimize LCP'),
    ('SP14', 'TTFB', 'Time to first byte', 'Use a CDN and cache HTML at the edge, even for a short time', 'Response headers show a cache hit; TTFB drops in field data', 'High', 'M', 'web.dev Top Core Web Vitals'),
    ('SP15', 'TTFB', 'Time to first byte', 'Remove redirects on landing URLs (ads, emails, internal links)', 'Each landing URL answers 200 with no hop', 'Medium', 'S', 'web.dev Optimize LCP'),
    ('SP16', 'TTFB', 'Time to first byte', 'Stop unique URL parameters from bypassing the CDN cache', 'Cache hit ratio for URLs with tracking parameters', 'Medium', 'S', 'web.dev Optimize LCP'),
    ('SP17', 'TTFB', 'Time to first byte', 'Cache pages and slow database queries on the server', 'Server timing for uncached and cached requests', 'High', 'M', 'Kit suggestion'),
    ('SP18', 'All', 'Instant navigation', 'Make pages eligible for the back and forward cache (no Cache-Control: no-store, no unload handlers)', 'DevTools Application panel, Back forward cache test', 'Medium', 'M', 'web.dev Top Core Web Vitals'),
    ('SP19', 'All', 'Instant navigation', 'Prerender likely next pages with the Speculation Rules API', 'DevTools shows the page as prerendered', 'Medium', 'M', 'web.dev Top Core Web Vitals'),
    ('SP20', 'INP', 'Processing duration', 'Yield to the main thread in long tasks (scheduler.yield or setTimeout)', 'DevTools Performance: no task over 50 ms after a click', 'High', 'M', 'web.dev Top Core Web Vitals'),
    ('SP21', 'INP', 'Input delay', 'Remove unused JavaScript with code splitting and the DevTools Coverage panel', 'Less JavaScript downloaded and run at startup', 'High', 'L', 'web.dev Top Core Web Vitals'),
    ('SP22', 'INP', 'Input delay', 'Audit the tag manager and third party tags; remove tags nobody uses', 'Tag list before and after', 'High', 'S', 'web.dev Top Core Web Vitals'),
    ('SP23', 'INP', 'Processing duration', 'Show visual feedback first and defer non urgent work in event handlers', 'The click shows a response at once', 'Medium', 'M', 'web.dev Optimize INP'),
    ('SP24', 'INP', 'Presentation delay', 'Avoid layout thrashing (reading layout right after changing styles)', 'DevTools: no forced reflow warnings', 'Medium', 'M', 'web.dev Optimize INP'),
    ('SP25', 'INP', 'Presentation delay', 'Reduce DOM size; use content-visibility for long off screen sections', 'Lighthouse DOM size audit', 'Medium', 'L', 'web.dev Optimize INP'),
    ('SP26', 'INP', 'Input delay', 'Cut script evaluation during startup (load non critical scripts later)', 'DevTools: less scripting before the page is usable', 'Medium', 'L', 'web.dev Optimize INP'),
    ('SP27', 'INP', 'Processing duration', 'Use built in browser features instead of JavaScript copies of them', 'Smaller bundles, fewer handlers', 'Low', 'M', 'web.dev Top Core Web Vitals'),
    ('SP28', 'CLS', 'Layout shifts', 'Set width and height (or aspect-ratio) on every image and video', 'Crawl or Lighthouse: no unsized images', 'High', 'S', 'web.dev Top Core Web Vitals'),
    ('SP29', 'CLS', 'Layout shifts', 'Reserve space for ads, embeds and iframes with min-height', 'No shift when an ad loads', 'High', 'S', 'web.dev Top Core Web Vitals'),
    ('SP30', 'CLS', 'Layout shifts', 'Animate transform instead of top, left, margin or border', 'DevTools Rendering, Layout shift regions', 'Medium', 'S', 'web.dev Top Core Web Vitals'),
    ('SP31', 'CLS', 'Layout shifts', 'Show cookie and promo banners as overlays, never push content down after load', 'No shift when the banner appears', 'Medium', 'S', 'Kit suggestion'),
    ('SP32', 'CLS', 'Layout shifts', 'Match the fallback font size to the web font to reduce shifts when it swaps', 'No text jump when the font loads', 'Low', 'M', 'Kit suggestion'),
    ('SP33', 'INP', 'Measurement', 'Add real user monitoring with the web-vitals library to find slow interactions', 'Slowest interactions listed per page', 'Medium', 'M', 'web.dev Optimize INP'),
    ('SP34', 'All', 'AI crawlers', 'Serve the main content and links in the initial HTML so crawlers that do not run JavaScript can read it', 'View source or fetch the page without JavaScript', 'Medium', 'L', 'Vercel and MERJ study'),
    ('SP35', 'LCP', 'Resource load duration', 'Lazy load images below the fold so they do not compete with the LCP image', 'Below the fold images use loading="lazy"', 'Low', 'S', 'web.dev Optimize LCP'),
    ('SP36', 'INP', 'Input delay', 'Load chat widgets and video embeds only when the visitor asks for them (a facade)', 'Third party script runs after a click only', 'Medium', 'M', 'Kit suggestion'),
    ('SP37', 'LCP', 'Resource load duration', 'Self host web fonts and load only the weights you use', 'Fewer font files and hosts', 'Low', 'S', 'Kit suggestion'),
    ('SP38', 'LCP', 'Resource load duration', 'Turn on Brotli or gzip compression for HTML, CSS and JavaScript', 'Response headers show content-encoding', 'Medium', 'S', 'Kit suggestion'),
]
NFIX = len(FIXES)

# Demo: BrewBean, a fictional coffee equipment store (brewbean.example). All numbers are illustrative.
U = 'https://brewbean.example'
# template, device, url, visits, revenue, source, lcp, inp, cls, ttfb, element, in html, lazy, t, delay, dur, render, notes
TEMPLATES = [
    ('Home', 'Mobile', '/', 42000, 'No', 'CrUX URL', 2.1, 180, 0.04, 600, 'Image', 'Yes', 'No', 600, 150, 700, 650, 'Hero image compressed in October'),
    ('Product page', 'Mobile', '/grinders/burr-grinder-pro/', 96000, 'Yes', 'Search Console group', 3.6, 240, 0.18, 900, 'Image', 'No', 'Yes', 900, 1300, 600, 800, 'Gallery slider builds the first image with JavaScript'),
    ('Category page', 'Mobile', '/espresso-machines/', 61000, 'Yes', 'Search Console group', 2.9, 310, 0.08, 1100, 'Image', 'Yes', 'No', 1100, 250, 900, 650, 'Filters run heavy JavaScript'),
    ('Blog article', 'Mobile', '/blog/how-to-dial-in-espresso/', 38000, 'No', 'CrUX origin', 2.3, 160, 0.27, 500, 'Text', 'Not an image', 'Not an image', 500, 0, 0, 1800, 'Ad slots push text down'),
    ('Brew guide', 'Mobile', '/guides/pour-over/', 22000, 'No', 'CrUX URL', 4.6, 420, 0.05, 1900, 'Image', 'Yes', 'No', 1900, 400, 1500, 800, 'Old page builder, no HTML cache'),
    ('Cart and checkout', 'Mobile', '/cart/', 9500, 'Yes', 'RUM', 2.0, 560, 0.02, 700, 'Text', 'Not an image', 'Not an image', 700, 0, 0, 1300, 'Apply coupon click freezes the page'),
    ('Product page', 'Desktop', '/grinders/burr-grinder-pro/', 31000, 'Yes', 'Search Console group', 2.2, 120, 0.12, 500, 'Image', 'No', 'Yes', 500, 900, 400, 400, 'Sticky add to cart bar slides in with top'),
    ('Store locator', 'Mobile', '/stores/', 4000, 'No', 'Lab only', 3.1, 190, 0.03, 800, 'Background image', 'No', 'No', 800, 1200, 600, 500, 'Map background set in CSS'),
]
K_ = lambda t, dv: f'{t} ({dv})'
# fix id, description, template key, effort, confidence, owner, status, shipped, before, after, notes
WINS = [
    ('SP01', 'Render the first gallery image in HTML instead of the JavaScript slider', K_('Product page', 'Mobile'), 'S', 'High', 'Developer', 'Planned', None, 3.6, None, 'Worked example in the guide'),
    ('SP03', 'Remove loading="lazy" from the main product image', K_('Product page', 'Mobile'), 'S', 'High', 'Developer', 'In progress', None, 3.6, None, ''),
    ('SP02', 'Add fetchpriority="high" to the main product image', K_('Product page', 'Mobile'), 'S', 'High', 'Developer', 'Shipped', '2026-11-20', 3.6, None, 'Lab LCP fell to 2.9 s'),
    ('SP28', 'Set width and height on review photos and thumbnails', K_('Product page', 'Mobile'), 'S', 'High', 'Developer', 'Planned', None, 0.18, None, ''),
    ('SP22', 'Remove 6 unused marketing tags from the tag manager', K_('Product page', 'Mobile'), 'S', 'Medium', 'Marketing', 'Idea', None, 240, None, 'Check with the ads team first'),
    ('SP14', 'Cache brew guide HTML on the CDN for 10 minutes', K_('Brew guide', 'Mobile'), 'M', 'High', 'Hosting or IT', 'Planned', None, 1900, None, ''),
    ('SP06', 'Rebuild brew guides on the server rendered template', K_('Brew guide', 'Mobile'), 'XL', 'Medium', 'Developer', 'Idea', None, 4.6, None, ''),
    ('SP20', 'Yield in the Apply coupon handler and show a spinner first', K_('Cart and checkout', 'Mobile'), 'M', 'High', 'Developer', 'Planned', None, 560, None, 'Revenue page'),
    ('SP29', 'Reserve 280 px for each in article ad slot', K_('Blog article', 'Mobile'), 'S', 'High', 'Developer', 'Planned', None, 0.27, None, ''),
    ('SP13', 'font-display swap and preload the heading font', K_('Blog article', 'Mobile'), 'S', 'High', 'Developer', 'Idea', None, 2.3, None, 'LCP already good'),
    ('SP21', 'Split the filter JavaScript and load it on first use', K_('Category page', 'Mobile'), 'L', 'Medium', 'Developer', 'Idea', None, 310, None, ''),
    ('SP17', 'Cache category queries for 5 minutes', K_('Category page', 'Mobile'), 'M', 'High', 'Developer', 'Planned', None, 1100, None, ''),
    ('SP04', 'Preload the map background image', K_('Store locator', 'Mobile'), 'S', 'High', 'Developer', 'Idea', None, 3.1, None, 'Lab data only'),
    ('SP30', 'Slide the sticky add to cart bar with transform', K_('Product page', 'Desktop'), 'S', 'High', 'Developer', 'Planned', None, 0.12, None, ''),
    ('SP18', 'Remove the unload handler from the chat script', K_('Home', 'Mobile'), 'M', 'Medium', 'Developer', 'Idea', None, None, None, ''),
    ('SP10', 'Compress the home hero to AVIF', K_('Home', 'Mobile'), 'S', 'High', 'Design', 'Validated', '2026-10-10', 2.6, 2.1, ''),
    ('SP15', 'Remove the redirect on ad landing URLs for categories', K_('Category page', 'Mobile'), 'S', 'High', 'Marketing', 'Shipped', '2026-10-15', 1250, 1100, ''),
    ('SP31', 'Show the cookie banner as an overlay', K_('Blog article', 'Mobile'), 'S', 'Medium', 'Developer', 'Shipped', '2026-10-01', 0.27, 0.27, 'Shifts come from ads, not the banner'),
    ('SP36', 'Load the video player only when Play is tapped', K_('Brew guide', 'Mobile'), 'M', 'High', 'Developer', 'Planned', None, 420, None, ''),
]
# win number, week, done when, method, result
PLAN = [
    (1, 'Week 1', 'View source on 10 product pages shows the first gallery image with src and srcset', 'PageSpeed Insights lab', 'Not started'),
    (2, 'Week 1', 'No product image above the fold has loading="lazy"', 'Manual check', 'Passed'),
    (4, 'Week 1', 'Lighthouse finds no unsized images on 10 product pages', 'PageSpeed Insights lab', 'Not started'),
    (5, 'Week 1', '', 'Manual check', 'Not started'),
    (9, 'Week 2', 'No layout shift when ads load on 5 sample articles', 'DevTools Performance panel', 'Not started'),
    (6, 'Week 2', 'Cache hit on repeat requests; TTFB under 800 ms in RUM', None, 'Not started'),
    (12, 'Week 2', 'Category TTFB under 800 ms at p75 in RUM', 'RUM (web-vitals)', 'Not started'),
    (8, 'Week 3', 'Apply coupon responds in under 200 ms in RUM', 'RUM (web-vitals)', 'Not started'),
    (14, 'Week 3', 'No shift when the bar appears; CLS 0.1 or less in field data', 'CrUX field data (28 days)', 'Not started'),
    (19, 'Week 3', 'Video script loads only after a tap', 'Manual check', 'Not started'),
    (11, 'Week 4', 'Filter JavaScript loads on first use; INP 200 ms or less', 'RUM (web-vitals)', 'Not started'),
    (7, 'Week 4', 'Brew guides render on the server; LCP 2.5 s or less', 'CrUX field data (28 days)', 'Not started'),
]

TP_IN = ['Template', 'Device', 'Example URL', 'Monthly visits', 'Revenue page?', 'Data source', 'LCP p75 (s)', 'INP p75 (ms)',
         'CLS p75', 'TTFB p75 (ms)', 'LCP element', 'LCP image in initial HTML?', 'LCP image lazy loaded?', 'LCP part: TTFB (ms)',
         'LCP part: load delay (ms)', 'LCP part: load duration (ms)', 'LCP part: render delay (ms)', 'Notes']
TP_FH = ['Key (template and device)', 'Traffic share', 'LCP status', 'INP status', 'CLS status', 'TTFB status', 'Worst status',
         'Core Web Vitals', 'LCP score', 'INP score', 'CLS score', 'Speed score (0 to 100)', 'LCP breakdown total (ms)',
         'TTFB share', 'Load delay share', 'Load duration share', 'Render delay share', 'Biggest LCP gap', 'First fix to try',
         'Red flags', 'Open wins', 'Wins shipped or validated']
TP_HEAD = TP_IN + TP_FH
TC = {h: L(i + 1) for i, h in enumerate(TP_HEAD)}
TP_F = tuple(range(len(TP_IN) + 1, len(TP_HEAD) + 1))

SW_IN = ['Win ID', 'Fix ID', 'Fix or task (your words)', 'Template and device', 'Effort', 'Confidence', 'Owner', 'Status',
         'Shipped on', 'Before (p75)', 'After (p75, field)', 'Notes']
SW_FH = ['Metric', 'Library fix', 'Expected impact', 'Metric status now', 'Status factor', 'Traffic share', 'Traffic factor',
         'Revenue factor', 'Impact points', 'Effort points', 'Confidence factor', 'Value (0 to 100)', 'Priority score',
         'Priority', 'Quadrant', 'Good threshold', 'Change (before minus after)', 'Improvement', 'Field data ready on',
         'Result', 'Rank (helper)']
SW_HEAD = SW_IN + SW_FH
WC = {h: L(i + 1) for i, h in enumerate(SW_HEAD)}
SW_F = tuple(range(len(SW_IN) + 1, len(SW_HEAD) + 1))


def tp(h):
    c = TC[h]
    return f'{TPS}!${c}${TP_FIRST}:${c}${TP_LAST}'


def sw(h):
    c = WC.get(h, h)
    return f'{SWS}!${c}${SW_FIRST}:${c}${SW_LAST}'


def fl(c):
    return f'{FLS}!${c}${FL_FIRST}:${c}${FL_LAST}'


def d(s):
    return datetime.date.fromisoformat(s) if s else None


def settings_sheet(wb):
    ws = wb.create_sheet(S)
    ws.sheet_view.showGridLines = False
    K.title_block(ws, 'Settings', 'Every threshold, weight and list used by this workbook. Change a blue value and every status, score and priority updates.')
    for c, w in zip('ABCDEFGHIJKLMNOPQRSTUVW', [50, 14, 3, 3, 3, 20, 12, 14, 30, 3, 24, 10, 60, 3, 10, 13, 15, 20, 18, 14, 28, 10, 9]):
        ws.column_dimensions[c].width = w
    rows = [
        (4, 'DATES, CAPACITY AND PRIORITY RULES', None, None),
        (5, 'Today (set it to the day you review the sheet)', datetime.date(2026, 11, 24), 'dd mmm yyyy'),
        (6, 'Field data window in days (CrUX uses 28 days)', 28, '0'),
        (7, 'Fix capacity per week (effort points)', 5, '0'),
        (8, 'P1: do now when the priority score is at least', 30, '0'),
        (9, 'P2: this sprint when at least', 12, '0'),
        (10, 'P3: plan it when at least (below = P4: later)', 5, '0'),
        (11, 'Quick win or big bet: value at least', 30, '0'),
        (12, 'Quick win: effort points at most', 2, '0'),
        (13, 'Revenue page factor (Revenue page? = Yes)', 1.5, '0.0'),
        (14, 'Traffic factor when monthly visits are blank', 0.4, '0.0'),
    ]
    for r, label, val, fmt in rows:
        a = ws.cell(row=r, column=1, value=label)
        a.font = K.f(10, val is None, K.DEEP if val is None else K.INK)
        if val is not None:
            c = ws.cell(row=r, column=2, value=val)
            c.border, c.fill = K.BORDER, K.INPUT_FILL
            c.font = K.f(10, True, '0000FF')
            c.number_format = fmt
    ws['A16'] = ('Value = 100 x impact points / 3 x status factor x traffic factor x revenue factor x confidence factor, '
                 'capped at 100. Priority score = value / effort points. The Core Web Vitals thresholds come from Google '
                 '(PageSpeed Insights and web.dev). The ideal LCP shares come from web.dev and are guidelines, not rules. '
                 'Every other weight, band and factor on this tab is an assumption of this kit for you to tune.')
    ws['A16'].font = K.f(9, False, '777777', True)
    ws['A16'].alignment = Alignment(wrap_text=True, vertical='top')
    ws.merge_cells('A16:B24')

    def table(col, row, title, heads, vals, fmts=None, blue=(1,)):
        ws.cell(row=row - 1, column=col, value=title).font = K.f(10, True, K.DEEP)
        for j, h in enumerate(heads):
            ws.cell(row=row, column=col + j, value=h).font = K.f(9, True, '555555')
        for i, v in enumerate(vals):
            for j in range(len(heads)):
                c = ws.cell(row=row + 1 + i, column=col + j, value=v[j])
                c.fill, c.border, c.font = K.INPUT_FILL, K.BORDER, K.f(10, j in blue, '0000FF' if j in blue else K.INK)
                c.alignment = Alignment(wrap_text=True, vertical='top')
                if fmts and fmts[j]:
                    c.number_format = fmts[j]
    table(6, 5, 'CORE WEB VITALS THRESHOLDS (75th percentile)', ['Metric', 'Good up to', 'Poor above', 'Unit'], THRESHOLDS, blue=(1, 2))
    table(6, 13, 'STATUS FACTOR', ['Status', 'Factor'], STATUS, ['@', '0.0'])
    table(6, 20, 'EXPECTED IMPACT', ['Impact', 'Points'], IMPACT)
    table(6, 26, 'EFFORT', ['Effort', 'Points', 'Meaning'], EFFORT)
    table(6, 33, 'CONFIDENCE', ['Confidence', 'Factor'], CONF, ['@', '0.0'])
    table(6, 39, 'TRAFFIC (share of all visits in the Templates tab)', ['At least', 'Factor'], TRAFFIC, ['0%', '0.0'])
    ws['F45'] = 'Keep the At least values in rising order: the lookup uses them as bands.'
    ws['F45'].font = K.f(8, False, '777777', True)
    table(11, 5, 'LCP SUBPARTS (ideal share of LCP time, web.dev)', ['Subpart', 'Ideal share', 'First fix to try'], SUBPARTS, ['@', '0%', '@'])
    for r in range(6, 10):
        ws.row_dimensions[r].height = 30
    lists = [('O', 'Device', DEVICES), ('P', 'Status', STATUSES), ('Q', 'Owner', OWNERS), ('R', 'Data source', SOURCES),
             ('S', 'LCP element', ELEMENTS), ('T', 'Yes or No', YNI), ('U', 'Validation method', METHODS), ('V', 'Week', WEEKS),
             ('W', 'Metric', METRICS)]
    ws['O13'] = 'LISTS (used by the dropdowns)'
    ws['O13'].font = K.f(10, True, K.DEEP)
    for col, head, vals in lists:
        ws[f'{col}14'] = head
        ws[f'{col}14'].font = K.f(9, True, '555555')
        n = 10 if col in 'QR' else len(vals)
        for i in range(n):
            c = ws[f'{col}{15 + i}']
            c.value = vals[i] if i < len(vals) else None
            c.fill, c.border, c.font = K.INPUT_FILL, K.BORDER, K.f(10)
    ws['O27'] = 'Validation results: Not started, Passed, Failed'
    for i, v in enumerate(VRES):
        c = ws[f'O{28 + i}']
        c.value, c.fill, c.border = v, K.INPUT_FILL, K.BORDER
    return ws


def mscore(v, m):
    g, p = G[m]
    return f'IF({v}="","",IF({v}<={g},100,IF({v}<={p},ROUND(50+50*({p}-{v})/({p}-{g}),1),ROUND(MAX(0,50-50*({v}-{p})/{p}),1))))'


def mstatus(v, m):
    g, p = G[m]
    return f'IF({v}="","No data",IF({v}<={g},"Good",IF({v}<={p},"Needs improvement","Poor")))'


def templates_sheet(wb):
    ws = wb.create_sheet(TPS)
    ws.sheet_view.showGridLines = False
    K.title_block(ws, 'Templates', f'One row per page template and device. Rows 5 to {4 + len(TEMPLATES)} are DEMO data for BrewBean, a fictional coffee equipment store (illustrative numbers). Replace them with your own; 100 rows ready.')
    ws['A2'].font = K.f(10, True, 'B45309')
    ws['A3'] = ('Field data (p75) comes from PageSpeed Insights, the Search Console Core Web Vitals report or your RUM. '
                'The LCP parts come from the PageSpeed Insights LCP breakdown or the DevTools Performance panel.')
    ws['A3'].font = K.f(9, False, '666666', True)
    widths = [18, 9, 30, 11, 9, 15, 8, 8, 7, 9, 12, 11, 10, 9, 9, 9, 9, 28,
              26, 9, 13, 13, 13, 13, 13, 9, 7, 7, 7, 9, 10, 8, 8, 8, 8, 20, 44, 40, 7, 9]
    K.header_row(ws, 4, TP_HEAD, formula_cols=TP_F, widths=widths)
    c = TC
    for r in range(TP_FIRST, TP_LAST + 1):
        i = r - TP_FIRST
        if i < len(TEMPLATES):
            row = list(TEMPLATES[i])
            row[2] = U + row[2]
            for col, v in enumerate(row, 1):
                if v not in (None, ''):
                    ws.cell(row=r, column=col, value=v)
        e = f'A{r}=""'
        g = lambda h: f'{c[h]}{r}'
        f = {}
        f['Key (template and device)'] = f'=IF({e},"",A{r}&" ("&IF(B{r}="","All devices",B{r})&")")'
        f['Traffic share'] = f'=IF(OR({e},N(D{r})=0),"",D{r}/SUM($D${TP_FIRST}:$D${TP_LAST}))'
        f['LCP status'] = f'=IF({e},"",{mstatus(f"G{r}", "LCP")})'
        f['INP status'] = f'=IF({e},"",{mstatus(f"H{r}", "INP")})'
        f['CLS status'] = f'=IF({e},"",{mstatus(f"I{r}", "CLS")})'
        f['TTFB status'] = f'=IF({e},"",{mstatus(f"J{r}", "TTFB")})'
        st = [g('LCP status'), g('INP status'), g('CLS status')]
        f['Worst status'] = (f'=IF({e},"",IF(OR({st[0]}="Poor",{st[1]}="Poor",{st[2]}="Poor"),"Poor",'
                             f'IF(OR({st[0]}="Needs improvement",{st[1]}="Needs improvement",{st[2]}="Needs improvement"),"Needs improvement",'
                             f'IF(AND({st[0]}="No data",{st[1]}="No data",{st[2]}="No data"),"No data","Good"))))')
        f['Core Web Vitals'] = (f'=IF({e},"",IF(OR({st[0]}="Poor",{st[0]}="Needs improvement",{st[1]}="Poor",{st[1]}="Needs improvement",{st[2]}="Poor",{st[2]}="Needs improvement"),"Failed",'
                                f'IF(OR({st[0]}="No data",{st[2]}="No data"),"Incomplete data","Passed")))')
        f['LCP score'] = f'=IF({e},"",{mscore(f"G{r}", "LCP")})'
        f['INP score'] = f'=IF({e},"",{mscore(f"H{r}", "INP")})'
        f['CLS score'] = f'=IF({e},"",{mscore(f"I{r}", "CLS")})'
        f['Speed score (0 to 100)'] = f'=IF({e},"",IFERROR(ROUND(AVERAGE({g("LCP score")}:{g("CLS score")}),0),""))'
        f['LCP breakdown total (ms)'] = f'=IF(OR({e},SUM(N{r}:Q{r})=0),"",SUM(N{r}:Q{r}))'
        tot = g('LCP breakdown total (ms)')
        for h, col in (('TTFB share', 'N'), ('Load delay share', 'O'), ('Load duration share', 'P'), ('Render delay share', 'Q')):
            f[h] = f'=IF({tot}="","",N({col}{r})/{tot})'
        gt, gd, gu, gr = (f'({g(h)}-{IDEAL[k]})' for h, k in (('TTFB share', 'ttfb'), ('Load delay share', 'delay'),
                                                              ('Load duration share', 'dur'), ('Render delay share', 'render')))
        mx = f'MAX({gt},{gd},{gu},{gr})'
        f['Biggest LCP gap'] = (f'=IF({tot}="","",IF({gd}={mx},"Resource load delay",IF({gr}={mx},"Element render delay",'
                                f'IF({gt}={mx},"Time to first byte","Resource load duration"))))')
        f['First fix to try'] = f'=IF({g("Biggest LCP gap")}="","",IFERROR(VLOOKUP({g("Biggest LCP gap")},{SUB_RNG},3,FALSE),""))'
        flags = (f'IF(M{r}="Yes","LCP image is lazy loaded. ","")&IF(L{r}="No","LCP image is not in the initial HTML. ","")'
                 f'&IF({g("TTFB status")}="Poor","TTFB is poor. ","")&IF({g("INP status")}="Poor","INP is poor. ","")'
                 f'&IF({g("CLS status")}="Poor","CLS is poor. ","")&IF(F{r}="Lab only","Lab data only: confirm with field data. ","")')
        f['Red flags'] = f'=IF({e},"",IF({flags}="","None",TRIM({flags})))'
        key = g('Key (template and device)')
        f['Open wins'] = f'=IF({e},"",COUNTIFS({sw("D")},{key},{sw("C")},"<>",{sw("H")},"<>Shipped",{sw("H")},"<>Validated",{sw("H")},"<>Dropped"))'
        f['Wins shipped or validated'] = f'=IF({e},"",COUNTIFS({sw("D")},{key},{sw("H")},"Shipped")+COUNTIFS({sw("D")},{key},{sw("H")},"Validated"))'
        for h, v in f.items():
            ws[f'{c[h]}{r}'] = v
    nf = {4: '#,##0', 7: '0.0', 8: '0', 9: '0.00', 10: '#,##0', 14: '#,##0', 15: '#,##0', 16: '#,##0', 17: '#,##0'}
    for h in ('Traffic share', 'TTFB share', 'Load delay share', 'Load duration share', 'Render delay share'):
        nf[TP_HEAD.index(h) + 1] = '0%'
    for h in ('LCP score', 'INP score', 'CLS score', 'Speed score (0 to 100)'):
        nf[TP_HEAD.index(h) + 1] = '0'
    nf[TP_HEAD.index('LCP breakdown total (ms)') + 1] = '#,##0'
    K.style_body(ws, TP_FIRST, TP_LAST, len(TP_HEAD), formula_cols=TP_F, number_formats=nf,
                 wrap_cols=(3, 18, TP_HEAD.index('First fix to try') + 1, TP_HEAD.index('Red flags') + 1))
    K.dropdown(ws, f'B{TP_FIRST}:B{TP_LAST}', f'{S}!$O$15:$O$16')
    K.dropdown(ws, f'E{TP_FIRST}:E{TP_LAST}', '"Yes,No"', 'Yes for pages that sell or capture leads.')
    K.dropdown(ws, f'F{TP_FIRST}:F{TP_LAST}', f'{S}!$R$15:$R$24')
    K.dropdown(ws, f'K{TP_FIRST}:K{TP_LAST}', f'{S}!$S$15:$S$18')
    K.dropdown(ws, f'L{TP_FIRST}:M{TP_LAST}', f'{S}!$T$15:$T$17')
    for h in ('LCP status', 'INP status', 'CLS status', 'TTFB status', 'Worst status'):
        col = c[h]
        rng = f'{col}{TP_FIRST}:{col}{TP_LAST}'
        for val, fill in (('Good', 'D9F2C4'), ('Needs improvement', 'FFF4CC'), ('Poor', 'F8D7D3')):
            ws.conditional_formatting.add(rng, CellIsRule(operator='equal', formula=[f'"{val}"'], fill=PatternFill('solid', fgColor=fill), font=Font(name=K.FONT, bold=val == 'Poor')))
    cw = c['Core Web Vitals']
    ws.conditional_formatting.add(f'{cw}{TP_FIRST}:{cw}{TP_LAST}', CellIsRule(operator='equal', formula=['"Passed"'], fill=PatternFill('solid', fgColor='B7E4A0'), font=Font(name=K.FONT, bold=True)))
    ws.conditional_formatting.add(f'{cw}{TP_FIRST}:{cw}{TP_LAST}', CellIsRule(operator='equal', formula=['"Failed"'], fill=PatternFill('solid', fgColor='9B2C1F'), font=Font(name=K.FONT, bold=True, color='FFFFFF')))
    sc = c['Speed score (0 to 100)']
    ws.conditional_formatting.add(f'{sc}{TP_FIRST}:{sc}{TP_LAST}', ColorScaleRule(start_type='num', start_value=40, start_color='F8D7D3', mid_type='num', mid_value=75, mid_color='FFF4CC', end_type='num', end_value=100, end_color='B7E4A0'))
    for r in range(TP_FIRST, TP_FIRST + len(TEMPLATES)):
        ws.row_dimensions[r].height = 42
    ws.freeze_panes = 'C5'
    ws.auto_filter.ref = f'A4:{L(len(TP_HEAD))}{TP_LAST}'
    return ws


def library_sheet(wb):
    ws = wb.create_sheet('Fix Library')
    ws.sheet_view.showGridLines = False
    K.title_block(ws, 'Fix library', f'{NCHK_TEXT}. Expected impact and typical effort are starting assumptions: change them to fit your site. Add your own fixes in the empty rows with a new ID.')
    head = ['Fix ID', 'Metric', 'Part or area', 'Fix', 'How to check it worked', 'Expected impact', 'Typical effort', 'Source', 'Wins logged', 'Open wins']
    K.header_row(ws, 4, head, formula_cols=(9, 10), widths=[8, 8, 20, 62, 46, 10, 9, 24, 8, 8])
    for r in range(FL_FIRST, FL_LAST + 1):
        i = r - FL_FIRST
        if i < NFIX:
            for col, v in enumerate(FIXES[i], 1):
                ws.cell(row=r, column=col, value=v)
        ws[f'I{r}'] = f'=IF(A{r}="","",COUNTIFS({sw("B")},A{r},{sw("C")},"<>"))'
        ws[f'J{r}'] = f'=IF(A{r}="","",COUNTIFS({sw("B")},A{r},{sw("C")},"<>",{sw("H")},"<>Shipped",{sw("H")},"<>Validated",{sw("H")},"<>Dropped"))'
    K.style_body(ws, FL_FIRST, FL_LAST, len(head), formula_cols=(9, 10), wrap_cols=(3, 4, 5, 8))
    K.dropdown(ws, f'B{FL_FIRST}:B{FL_LAST}', f'{S}!$W$15:$W$19')
    K.dropdown(ws, f'F{FL_FIRST}:F{FL_LAST}', f'{S}!$F$21:$F$23')
    K.dropdown(ws, f'G{FL_FIRST}:G{FL_LAST}', f'{S}!$F$27:$F$30')
    for r in range(FL_FIRST, FL_FIRST + NFIX):
        ws.row_dimensions[r].height = 30
    rng = f'F{FL_FIRST}:F{FL_LAST}'
    ws.conditional_formatting.add(rng, CellIsRule(operator='equal', formula=['"High"'], fill=PatternFill('solid', fgColor='D9F2C4'), font=Font(name=K.FONT, bold=True)))
    ws.freeze_panes = 'E5'
    ws.auto_filter.ref = f'A4:J{FL_LAST}'
    return ws


NCHK_TEXT = f'{NFIX} proven fixes for LCP, INP, CLS and TTFB, mostly from Google\'s web.dev guidance'


def wins_sheet(wb):
    ws = wb.create_sheet('Speed Wins')
    ws.sheet_view.showGridLines = False
    K.title_block(ws, 'Speed wins', f'One row per fix. Rows 5 to {4 + len(WINS)} are DEMO wins for BrewBean (illustrative). To start your own, delete the yellow demo cells from column B to L; keep the Win IDs in column A. 500 rows ready.')
    ws['A2'].font = K.f(10, True, 'B45309')
    ws['A3'] = ('Pick a Fix ID from the Fix Library (or leave it blank for your own task), the template and device, effort and confidence. '
                'Sort by Priority score and work P1 first. Before and After use the unit of the metric (LCP seconds, INP and TTFB milliseconds, CLS score).')
    ws['A3'].font = K.f(9, False, '666666', True)
    widths = [8, 7, 44, 26, 7, 10, 13, 11, 11, 9, 9, 28, 7, 40, 9, 16, 8, 8, 8, 8, 8, 8, 9, 9, 9, 14, 13, 9, 10, 10, 12, 30, 9]
    K.header_row(ws, 4, SW_HEAD, formula_cols=SW_F, widths=widths)
    c = WC
    lib = f'{fl("A")}:{FLS}!$G${FL_LAST}'
    for r in range(SW_FIRST, SW_LAST + 1):
        i = r - SW_FIRST
        if i < len(WINS):
            fid, desc, key, eff, conf, own, st, shp, bef, aft, note = WINS[i]
            for col, v in zip(range(2, 13), [fid, desc, key, eff, conf, own, st, d(shp), bef, aft, note]):
                if v not in (None, ''):
                    ws.cell(row=r, column=col, value=v)
        ws[f'A{r}'] = f'SW-{i + 1:03d}'
        e = f'C{r}=""'
        g = lambda h: f'{c[h]}{r}'
        tm = f'MATCH(D{r},{tp("Key (template and device)")},0)'
        tget = lambda h: f'INDEX({tp(h)},{tm})'
        f = {}
        f['Metric'] = f'=IF({e},"",IF(B{r}="","All",IFERROR(VLOOKUP(B{r},{lib},2,FALSE),"Fix ID not found")))'
        f['Library fix'] = f'=IF(OR({e},B{r}=""),"",IFERROR(VLOOKUP(B{r},{lib},4,FALSE),""))'
        f['Expected impact'] = f'=IF({e},"",IF(B{r}="","Medium",IFERROR(VLOOKUP(B{r},{lib},6,FALSE),"Medium")))'
        m = g('Metric')
        f['Metric status now'] = (f'=IF({e},"",IF(ISNA({tm}),"Template not found",IF({m}="LCP",{tget("LCP status")},IF({m}="INP",{tget("INP status")},'
                                  f'IF({m}="CLS",{tget("CLS status")},IF({m}="TTFB",{tget("TTFB status")},{tget("Worst status")}))))))')
        f['Status factor'] = f'=IF({e},"",IFERROR(VLOOKUP({g("Metric status now")},{STAT_RNG},2,FALSE),0.5))'
        f['Traffic share'] = f'=IF({e},"",IFERROR(IF({tget("Traffic share")}="","",{tget("Traffic share")}),""))'
        f['Traffic factor'] = f'=IF({e},"",IF({g("Traffic share")}="",{BLANKF},VLOOKUP({g("Traffic share")},{TRAF_RNG},2,TRUE)))'
        f['Revenue factor'] = f'=IF({e},"",IFERROR(IF({tget("Revenue page?")}="Yes",{REV},1),1))'
        f['Impact points'] = f'=IF({e},"",IFERROR(VLOOKUP({g("Expected impact")},{IMP_RNG},2,FALSE),2))'
        f['Effort points'] = f'=IF({e},"",IFERROR(VLOOKUP(E{r},{EFF_RNG},2,FALSE),2))'
        f['Confidence factor'] = f'=IF({e},"",IFERROR(VLOOKUP(F{r},{CONF_RNG},2,FALSE),0.8))'
        f['Value (0 to 100)'] = (f'=IF({e},"",MIN(100,ROUND(100*{g("Impact points")}/3*{g("Status factor")}*{g("Traffic factor")}'
                                 f'*{g("Revenue factor")}*{g("Confidence factor")},0)))')
        val = g('Value (0 to 100)')
        f['Priority score'] = f'=IF({e},"",ROUND({val}/{g("Effort points")},0))'
        sc = g('Priority score')
        f['Priority'] = (f'=IF({e},"",IF(H{r}="Dropped","Dropped",IF(H{r}="Validated","Validated",IF(H{r}="Shipped","Shipped",'
                         f'IF({sc}>={P1},"P1: do now",IF({sc}>={P2},"P2: this sprint",IF({sc}>={P3},"P3: plan it","P4: later")))))))')
        ep = g('Effort points')
        f['Quadrant'] = (f'=IF({e},"",IF({val}>={QV},IF({ep}<={QE},"Quick win","Big bet"),IF({ep}<={QE},"Small task","Avoid for now")))')
        f['Good threshold'] = f'=IF(OR({e},{m}="All"),"",IFERROR(VLOOKUP({m},{THR},2,FALSE),""))'
        f['Change (before minus after)'] = f'=IF(OR({e},J{r}="",K{r}=""),"",J{r}-K{r})'
        ch = g('Change (before minus after)')
        f['Improvement'] = f'=IF(OR({ch}="",N(J{r})=0),"",{ch}/J{r})'
        f['Field data ready on'] = f'=IF(OR({e},I{r}=""),"",I{r}+{WINDOW})'
        rd = g('Field data ready on')
        gt = g('Good threshold')
        f['Result'] = (f'=IF({e},"",IF(H{r}="Dropped","Dropped",IF(I{r}="","Not shipped yet",IF({DATE}<{rd},"Wait for field data: "&({rd}-{DATE})&" days left",'
                       f'IF(K{r}="","Add the After value",IF(AND({gt}<>"",K{r}<={gt}),"Now good",IF(K{r}<J{r},"Improved, not good yet","No improvement: investigate")))))))')
        f['Rank (helper)'] = f'=IF(OR({e},H{r}="Shipped",H{r}="Validated",H{r}="Dropped"),"",{sc}+{val}/1000-ROW()/10000000)'
        for h, v in f.items():
            ws[f'{c[h]}{r}'] = v
    nf = {9: 'dd mmm yyyy', 10: '0.00', 11: '0.00'}
    idx = lambda h: SW_HEAD.index(h) + 1
    nf.update({idx('Traffic share'): '0%', idx('Status factor'): '0.0', idx('Traffic factor'): '0.0', idx('Revenue factor'): '0.0',
               idx('Confidence factor'): '0.0', idx('Value (0 to 100)'): '0', idx('Priority score'): '0', idx('Improvement'): '0%',
               idx('Field data ready on'): 'dd mmm yyyy', idx('Change (before minus after)'): '0.00', idx('Rank (helper)'): '0.000000'})
    K.style_body(ws, SW_FIRST, SW_LAST, len(SW_HEAD), formula_cols=SW_F, number_formats=nf,
                 wrap_cols=(3, 4, 12, idx('Library fix'), idx('Result')))
    K.dropdown(ws, f'B{SW_FIRST}:B{SW_LAST}', fl('A'), 'Fix IDs live on the Fix Library tab. Leave blank for your own task.')
    K.dropdown(ws, f'D{SW_FIRST}:D{SW_LAST}', tp('Key (template and device)'), 'Templates and devices from the Templates tab.')
    K.dropdown(ws, f'E{SW_FIRST}:E{SW_LAST}', f'{S}!$F$27:$F$30', 'S under a day, M a few days, L one to two weeks, XL a project.')
    K.dropdown(ws, f'F{SW_FIRST}:F{SW_LAST}', f'{S}!$F$34:$F$36')
    K.dropdown(ws, f'G{SW_FIRST}:G{SW_LAST}', f'{S}!$Q$15:$Q$24')
    K.dropdown(ws, f'H{SW_FIRST}:H{SW_LAST}', f'{S}!$P$15:$P$20')
    pc = c['Priority']
    pr = f'{pc}{SW_FIRST}:{pc}{SW_LAST}'
    for start, fill, fc in (('P1', '9B2C1F', 'FFFFFF'), ('P2', 'F8D7D3', '9B2C1F'), ('P3', 'FFF4CC', '1F1F1F'), ('P4', 'EEEEEE', '555555'), ('Va', 'D9F2C4', '1F1F1F'), ('Sh', 'EEF8E6', '3D7F12')):
        ws.conditional_formatting.add(pr, FormulaRule(formula=[f'LEFT({pc}{SW_FIRST},2)="{start}"'], fill=PatternFill('solid', fgColor=fill), font=Font(name=K.FONT, bold=True, color=fc)))
    qc = c['Quadrant']
    qr = f'{qc}{SW_FIRST}:{qc}{SW_LAST}'
    for val, fill in (('Quick win', 'B7E4A0'), ('Big bet', 'CFE2F3'), ('Small task', 'FFF4CC'), ('Avoid for now', 'EEEEEE')):
        ws.conditional_formatting.add(qr, CellIsRule(operator='equal', formula=[f'"{val}"'], fill=PatternFill('solid', fgColor=fill), font=Font(name=K.FONT, bold=val == 'Quick win')))
    rc = c['Result']
    rr = f'{rc}{SW_FIRST}:{rc}{SW_LAST}'
    ws.conditional_formatting.add(rr, CellIsRule(operator='equal', formula=['"Now good"'], fill=PatternFill('solid', fgColor='B7E4A0'), font=Font(name=K.FONT, bold=True)))
    ws.conditional_formatting.add(rr, FormulaRule(formula=[f'LEFT({rc}{SW_FIRST},2)="No"'], fill=PatternFill('solid', fgColor='F8D7D3'), font=Font(name=K.FONT, bold=True, color='9B2C1F')))
    ws.conditional_formatting.add(rr, FormulaRule(formula=[f'OR(LEFT({rc}{SW_FIRST},4)="Wait",LEFT({rc}{SW_FIRST},3)="Add",LEFT({rc}{SW_FIRST},8)="Improved")'], fill=PatternFill('solid', fgColor='FFF4CC')))
    vc = c['Value (0 to 100)']
    ws.conditional_formatting.add(f'{vc}{SW_FIRST}:{vc}{SW_LAST}', ColorScaleRule(start_type='num', start_value=0, start_color='FFFFFF', end_type='num', end_value=90, end_color='8BC34A'))
    ws.column_dimensions[c['Rank (helper)']].hidden = True
    for r in range(SW_FIRST, SW_FIRST + len(WINS)):
        ws.row_dimensions[r].height = 30
    ws.freeze_panes = 'D5'
    ws.auto_filter.ref = f'A4:{L(len(SW_HEAD))}{SW_LAST}'
    return ws


def plan_sheet(wb):
    ws = wb.create_sheet('Sprint Plan')
    ws.sheet_view.showGridLines = False
    K.title_block(ws, 'Sprint plan', 'Turn wins into developer tickets. Pick a Win ID, a week, what done looks like and how you will validate it. The ticket text writes itself; the table on the right checks each week against your capacity.')
    head = ['Win ID', 'Week', 'Done when (acceptance criteria)', 'Validation method', 'Validation result', 'Fix', 'Template and device',
            'Metric', 'Priority', 'Owner', 'Effort points', 'Ticket text (copy into your tracker)', 'Next step']
    fc = tuple(range(6, 14))
    K.header_row(ws, 4, head, formula_cols=fc, widths=[9, 9, 42, 22, 12, 36, 22, 7, 14, 12, 8, 72, 30])
    idx = lambda r: f'MATCH(A{r},{sw("A")},0)'
    get = lambda h, r: f'INDEX({sw(h)},{idx(r)})'
    for r in range(SP_FIRST, SP_LAST + 1):
        i = r - SP_FIRST
        if i < len(PLAN):
            n, wk, done, meth, res = PLAN[i]
            for col, v in enumerate([f'SW-{n:03d}', wk, done, meth, res], 1):
                if v not in (None, ''):
                    ws.cell(row=r, column=col, value=v)
        e = f'A{r}=""'
        ok = f'ISNUMBER({idx(r)})'
        no = f'OR({e},NOT({ok}))'
        ws[f'F{r}'] = f'=IF({e},"",IF({ok},""&{get("C", r)},"Win ID not found"))'
        ws[f'G{r}'] = f'=IF({no},"",""&{get("D", r)})'
        ws[f'H{r}'] = f'=IF({no},"",{get(WC["Metric"], r)})'
        ws[f'I{r}'] = f'=IF({no},"",{get(WC["Priority"], r)})'
        ws[f'J{r}'] = f'=IF({no},"",""&{get("G", r)})'
        ws[f'K{r}'] = f'=IF({no},"",{get(WC["Effort points"], r)})'
        lib = get(WC['Library fix'], r)
        ws[f'L{r}'] = (f'=IF({no},"","["&H{r}&", "&LEFT(I{r},2)&", "&{get(WC["Quadrant"], r)}&"] "&F{r}&" on "&G{r}&". "'
                       f'&IF({lib}="","","Library fix: "&{lib}&". ")&"Metric now: "&{get(WC["Metric status now"], r)}&". Owner: "&IF(J{r}="","(not set)",J{r})'
                       f'&". Done when: "&IF(C{r}="","(add acceptance criteria)",C{r})&". Validate with: "&IF(D{r}="","(choose a method)",D{r})&".")')
        st = get('H', r)
        ws[f'M{r}'] = (f'=IF({e},"",IF(NOT({ok}),"Fix the Win ID",IF(E{r}="Passed",IF(OR({st}="Shipped",{st}="Validated"),"Done","Passed: mark the win Shipped"),'
                       f'IF(E{r}="Failed","Failed: reopen and fix again",IF(C{r}="","Write the acceptance criteria",IF(B{r}="","Schedule it in a week",'
                       f'IF(D{r}="","Choose how to validate","Ready for development")))))))')
    K.style_body(ws, SP_FIRST, SP_LAST, len(head), formula_cols=fc, wrap_cols=(3, 6, 7, 12, 13))
    for r in range(SP_FIRST, SP_FIRST + len(PLAN)):
        ws.row_dimensions[r].height = 60
    K.dropdown(ws, f'A{SP_FIRST}:A{SP_LAST}', sw('A'))
    K.dropdown(ws, f'B{SP_FIRST}:B{SP_LAST}', f'{S}!$V$15:$V$22')
    K.dropdown(ws, f'D{SP_FIRST}:D{SP_LAST}', f'{S}!$U$15:$U$20')
    K.dropdown(ws, f'E{SP_FIRST}:E{SP_LAST}', f'{S}!$O$28:$O$30')
    m = f'M{SP_FIRST}:M{SP_LAST}'
    ws.conditional_formatting.add(m, CellIsRule(operator='equal', formula=['"Ready for development"'], fill=PatternFill('solid', fgColor='D9F2C4'), font=Font(name=K.FONT, bold=True)))
    ws.conditional_formatting.add(m, FormulaRule(formula=[f'OR(LEFT(M{SP_FIRST},6)="Failed",LEFT(M{SP_FIRST},3)="Fix")'], fill=PatternFill('solid', fgColor='F8D7D3'), font=Font(name=K.FONT, bold=True, color='9B2C1F')))
    ws.conditional_formatting.add(m, FormulaRule(formula=[f'OR(LEFT(M{SP_FIRST},5)="Write",LEFT(M{SP_FIRST},8)="Schedule",LEFT(M{SP_FIRST},6)="Choose",LEFT(M{SP_FIRST},6)="Passed")'], fill=PatternFill('solid', fgColor='FFF4CC')))
    ws['O4'] = 'WEEKLY CAPACITY'
    ws['O4'].font = K.f(10, True, K.DEEP)
    for j, h in enumerate(['Week', 'Effort planned', 'Capacity', 'Status']):
        cc = ws.cell(row=5, column=15 + j, value=h)
        cc.font, cc.fill = K.f(10, True, 'FFFFFF'), K.HEAD_F
    for i in range(len(WEEKS)):
        r = 6 + i
        ws.cell(row=r, column=15, value=f'={S}!V{15 + i}')
        ws.cell(row=r, column=16, value=f'=SUMIF($B${SP_FIRST}:$B${SP_LAST},O{r},$K${SP_FIRST}:$K${SP_LAST})')
        ws.cell(row=r, column=17, value=f'={CAP}')
        ws.cell(row=r, column=18, value=f'=IF(P{r}=0,"Free",IF(P{r}>Q{r},"Over capacity by "&(P{r}-Q{r}),"OK"))')
        for cc in range(15, 19):
            cell = ws.cell(row=r, column=cc)
            cell.border, cell.fill, cell.font = K.BORDER, K.FORMULA_FILL, K.f(10)
    r = 6 + len(WEEKS)
    ws.cell(row=r, column=15, value='Not scheduled').font = K.f(10, True)
    ws.cell(row=r, column=16, value=f'=SUMIFS($K${SP_FIRST}:$K${SP_LAST},$A${SP_FIRST}:$A${SP_LAST},"<>",$B${SP_FIRST}:$B${SP_LAST},"")').fill = K.FORMULA_FILL
    for col, w in zip('NOPQR', [3, 14, 10, 9, 22]):
        ws.column_dimensions[col].width = w
    ws.conditional_formatting.add('R6:R13', FormulaRule(formula=['LEFT(R6,4)="Over"'], fill=PatternFill('solid', fgColor='F8D7D3'), font=Font(name=K.FONT, bold=True, color='9B2C1F')))
    ws.freeze_panes = 'B5'
    ws.auto_filter.ref = f'A4:M{SP_LAST}'
    return ws


def chart(ws, title, ytitle, cat_col, val_cols, r1, r2, anchor, colors, horiz, titles, h=7.5, stacked=False, w=16):
    ch = BarChart()
    ch.type = 'bar' if horiz else 'col'
    ch.title = title
    ch.y_axis.title = ytitle
    for vc in val_cols:
        ch.add_data(Reference(ws, min_col=vc, min_row=r1 - (1 if titles else 0), max_row=r2), titles_from_data=titles)
    ch.set_categories(Reference(ws, min_col=cat_col, min_row=r1, max_row=r2))
    if not titles:
        ch.legend = None
    else:
        ch.legend.overlay = False
    if stacked:
        ch.grouping = 'stacked'
        ch.overlap = 100
    ch.height, ch.width = h, w
    ch.roundedCorners = False
    ch.x_axis.delete = False
    ch.y_axis.delete = False
    ch.title.overlay = False
    ch.y_axis.title.overlay = False
    for s, col in zip(ch.series, colors):
        s.graphicalProperties.solidFill = col
    ws.add_chart(ch, anchor)
    return ch


def dashboard_sheet(wb):
    ws = wb.create_sheet('Dashboard')
    ws.sheet_view.showGridLines = False
    K.title_block(ws, 'Dashboard', 'Everything here calculates from the other tabs. Nothing to type.')
    for col, w in zip('ABCDEFGHIJKL', [48, 12, 3, 9, 42, 24, 8, 8, 15, 14, 26, 3]):
        ws.column_dimensions[col].width = w
    opn = f'{sw("C")},"<>",{sw("H")},"<>Shipped",{sw("H")},"<>Validated",{sw("H")},"<>Dropped"'
    tk = tp('Key (template and device)')
    kpis = [
        ('Template and device rows measured', f'=COUNTIF({tk},"?*")', '0'),
        ('Rows passing Core Web Vitals', f'=COUNTIF({tp("Core Web Vitals")},"Passed")', '0'),
        ('Share of visits on passing rows', f'=IFERROR(SUMIF({tp("Core Web Vitals")},"Passed",{tp("Monthly visits")})/SUM({tp("Monthly visits")}),0)', '0%'),
        ('Rows with a poor LCP', f'=COUNTIF({tp("LCP status")},"Poor")', '0'),
        ('Rows with a poor INP', f'=COUNTIF({tp("INP status")},"Poor")', '0'),
        ('Rows with a poor CLS', f'=COUNTIF({tp("CLS status")},"Poor")', '0'),
        ('Average speed score (weighted by visits)', f'=IFERROR(ROUND(SUMPRODUCT({tp("Speed score (0 to 100)")},{tp("Monthly visits")})/SUMIF({tp("Speed score (0 to 100)")},">=0",{tp("Monthly visits")}),0),"")', '0'),
        ('Open wins', f'=COUNTIFS({opn})', '0'),
        ('P1 wins to do now', f'=COUNTIF({sw(WC["Priority"])},"P1*")', '0'),
        ('Open quick wins', f'=COUNTIFS({opn},{sw(WC["Quadrant"])},"Quick win")', '0'),
        ('Shipped, waiting for field data', f'=COUNTIF({sw(WC["Result"])},"Wait*")', '0'),
        ('Fixes now good', f'=COUNTIF({sw(WC["Result"])},"Now good")', '0'),
        ('Fixes improved but not good yet', f'=COUNTIF({sw(WC["Result"])},"Improved*")', '0'),
        ('Fixes with no improvement', f'=COUNTIF({sw(WC["Result"])},"No improvement*")', '0'),
        ('Open effort (effort points)', f'=SUMIFS({sw(WC["Effort points"])},{opn})', '0'),
        ('Weeks of work at your capacity', f'=IFERROR(ROUND(B19/{CAP},1),"")', '0.0'),
    ]
    ws['A4'] = 'KEY NUMBERS'
    ws['A4'].font = K.f(10, True, K.DEEP)
    for i, (label, fml, fmt) in enumerate(kpis):
        r = 5 + i
        ws.cell(row=r, column=1, value=label).font = K.f(10)
        cell = ws.cell(row=r, column=2, value=fml)
        cell.number_format, cell.font, cell.fill, cell.border = fmt, K.f(11, True), K.FORMULA_FILL, K.BORDER
        cell.alignment = Alignment(horizontal='right')
    ws['D4'] = 'TOP 10 OPEN WINS (highest priority score first)'
    ws['D4'].font = K.f(10, True, K.DEEP)
    heads = ['Win ID', 'Fix', 'Template and device', 'Metric', 'Score', 'Priority', 'Quadrant']
    cols = ['A', 'C', 'D', WC['Metric'], WC['Priority score'], WC['Priority'], WC['Quadrant']]
    for j, h in enumerate(heads):
        cell = ws.cell(row=5, column=4 + j, value=h)
        cell.font, cell.fill = K.f(10, True, 'FFFFFF'), K.HEAD_F
    rk = sw(WC['Rank (helper)'])
    for k in range(1, 11):
        r = 5 + k
        mt = f'MATCH(LARGE({rk},{k}),{rk},0)'
        for j, col in enumerate(cols):
            cell = ws.cell(row=r, column=4 + j, value=f'=IFERROR(INDEX({sw(col)},{mt}),"")')
            cell.border, cell.fill, cell.font = K.BORDER, K.FORMULA_FILL, K.f(9, j == 0)
            cell.alignment = Alignment(wrap_text=j in (1, 2), vertical='top')
            cell.number_format = '0' if j == 4 else '@'
        ws.row_dimensions[r].height = 26
    top = 24
    ws.cell(row=top - 1, column=1, value='TEMPLATES (first 12 rows of the Templates tab)').font = K.f(10, True, K.DEEP)
    th = ['Template and device', 'Speed score', 'LCP', 'INP', 'CLS', 'Core Web Vitals', 'Open wins']
    tcols = ['Key (template and device)', 'Speed score (0 to 100)', 'LCP status', 'INP status', 'CLS status', 'Core Web Vitals', 'Open wins']
    for j, h in enumerate(th):
        cell = ws.cell(row=top, column=1 + j if j < 2 else 2 + j, value=h)
        cell.font, cell.fill = K.f(10, True, 'FFFFFF'), K.HEAD_F
    for i in range(12):
        r = top + 1 + i
        for j, h in enumerate(tcols):
            col = 1 + j if j < 2 else 2 + j
            cell = ws.cell(row=r, column=col, value=f'={TPS}!{TC[h]}{TP_FIRST + i}')
            cell.border, cell.fill, cell.font = K.BORDER, K.FORMULA_FILL, K.f(10, j < 2)
    last = top + 12
    for col in 'DEFG':
        rng = f'{col}{top + 1}:{col}{last}'
        for val, fill in (('Good', 'D9F2C4'), ('Needs improvement', 'FFF4CC'), ('Poor', 'F8D7D3'), ('Passed', 'B7E4A0'), ('Failed', 'F8D7D3')):
            ws.conditional_formatting.add(rng, CellIsRule(operator='equal', formula=[f'"{val}"'], fill=PatternFill('solid', fgColor=fill)))
    ws.conditional_formatting.add(f'B{top + 1}:B{last}', ColorScaleRule(start_type='num', start_value=40, start_color='F8D7D3', mid_type='num', mid_value=75, mid_color='FFF4CC', end_type='num', end_value=100, end_color='B7E4A0'))
    t2 = last + 4
    ws.cell(row=t2 - 1, column=1, value='OPEN WINS BY QUADRANT').font = K.f(10, True, K.DEEP)
    for j, h in enumerate(['Quadrant', 'Open wins', 'Effort points']):
        cell = ws.cell(row=t2, column=1 + j if j == 0 else 1 + j, value=h)
        cell.font, cell.fill = K.f(10, True, 'FFFFFF'), K.HEAD_F
    for i, q in enumerate(['Quick win', 'Big bet', 'Small task', 'Avoid for now']):
        r = t2 + 1 + i
        ws.cell(row=r, column=1, value=q).border = K.BORDER
        for col, fml in ((2, f'=COUNTIFS({opn},{sw(WC["Quadrant"])},A{r})'), (3, f'=SUMIFS({sw(WC["Effort points"])},{opn},{sw(WC["Quadrant"])},A{r})')):
            cell = ws.cell(row=r, column=col, value=fml)
            cell.border, cell.fill = K.BORDER, K.FORMULA_FILL
    t3 = t2 + 8
    ws.cell(row=t3 - 1, column=1, value='OPEN WINS BY METRIC').font = K.f(10, True, K.DEEP)
    for j, h in enumerate(['Metric', 'Open wins', 'P1 wins']):
        cell = ws.cell(row=t3, column=1 + j, value=h)
        cell.font, cell.fill = K.f(10, True, 'FFFFFF'), K.HEAD_F
    for i, mt in enumerate(METRICS):
        r = t3 + 1 + i
        ws.cell(row=r, column=1, value=mt).border = K.BORDER
        for col, fml in ((2, f'=COUNTIFS({opn},{sw(WC["Metric"])},A{r})'), (3, f'=COUNTIFS({sw(WC["Metric"])},A{r},{sw(WC["Priority"])},"P1*")')):
            cell = ws.cell(row=r, column=col, value=fml)
            cell.border, cell.fill = K.BORDER, K.FORMULA_FILL
    c1 = chart(ws, 'Speed score by template and device', 'Score', 1, [2], top + 1, top + len(TEMPLATES), 'I17', [K.GREEN], True, False, h=9, w=17)
    c1.y_axis.scaling.min = 0
    c1.y_axis.scaling.max = 100
    chart(ws, 'Open wins by quadrant', 'Wins', 1, [2], t2 + 1, t2 + 4, 'I36', ['4F9D1A'], False, False, w=17)
    return ws, top, t2, t3


def build(path, asset, url):
    wb = K.new_book()
    templates_sheet(wb)
    wins_sheet(wb)
    library_sheet(wb)
    plan_sheet(wb)
    dashboard_sheet(wb)
    settings_sheet(wb)
    K.prompts_sheet(wb, asset['prompts'], url)
    K.checklist_sheet(wb, list(asset['checklist']))
    K.sources_sheet(wb, asset['sources'], [
        ('Demo data', 'BrewBean and every URL in the demo are fictional (.example domain). All visits, timings, scores and dates are illustrative, not real data.', ''),
        ('Core Web Vitals thresholds', 'Good at the 75th percentile: LCP 2.5 s or less, INP 200 ms or less, CLS 0.1 or less. Poor: LCP over 4 s, INP over 500 ms, CLS over 0.25. PageSpeed Insights also rates TTFB (good up to 800 ms, poor over 1,800 ms, experimental) and FCP.', 'https://developers.google.com/speed/docs/insights/v5/about'),
        ('Field data window', 'PageSpeed Insights shows Chrome UX Report field data over the previous 28 day collection period, so a fix needs about 28 days before field data fully reflects it.', 'https://developers.google.com/speed/docs/insights/v5/about'),
        ('LCP subparts', 'web.dev splits LCP into time to first byte (about 40 percent of LCP time), resource load delay (under 10 percent), resource load duration (about 40 percent) and element render delay (under 10 percent). These are guidelines.', 'https://web.dev/articles/optimize-lcp'),
        ('Impact, effort and value', 'Expected impact, typical effort, status factors, traffic bands, the revenue factor, confidence and the P1 to P4 thresholds are assumptions of this kit. Tune them on Settings and Fix Library.', ''),
        ('AI crawlers and JavaScript', 'A Vercel and MERJ study (December 2024) found that none of the major AI crawlers it measured rendered JavaScript. Behaviour may change; check your own logs.', 'https://vercel.com/blog/the-rise-of-the-ai-crawler'),
    ])
    K.start_here(
        wb, 'Site Speed Wins Kit',
        [
            'This workbook is a Core Web Vitals checklist that turns into a plan. Add your page templates with field data, and it rates LCP, INP, CLS and TTFB with Google\'s thresholds, finds which part of LCP is slow and suggests the first fix to try.',
            f'Every fix goes on the Speed Wins tab, which ranks it by impact, effort, traffic and confidence, sorts it into quick wins and big bets, and tells you when field data is ready to prove it worked. A library of {NFIX} proven fixes and a worked demo for a fictional coffee equipment store are included.',
        ],
        [
            ('Templates', 'One row per template and device: field data, traffic, LCP element and the four LCP parts. Statuses, speed score, biggest LCP gap, first fix and red flags.'),
            ('Speed Wins', 'One row per fix, 500 rows ready. Value, priority score, P1 to P4, quadrant, field data date and result.'),
            ('Fix Library', f'{NFIX} fixes for LCP, INP, CLS and TTFB with how to check them, expected impact and typical effort.'),
            ('Sprint Plan', 'Developer tickets with acceptance criteria, week and validation method, plus a weekly capacity check.'),
            ('Dashboard', '16 key numbers, top 10 open wins, template table, wins by quadrant and by metric, with two charts.'),
            ('Settings', 'Thresholds, ideal LCP shares, impact, effort, confidence, traffic bands, priority rules and lists.'),
            ('AI Prompts', 'Prompts for ChatGPT, Claude or Gemini to read PageSpeed reports, find causes and write tickets.'),
            ('Checklist', 'The site speed checklist as a tick list with automatic progress.'),
            ('Sources', 'Where facts come from and which numbers are assumptions.'),
        ],
        [
            'Look at the demo on Templates, Speed Wins, Sprint Plan and the Dashboard. Then clear the yellow demo cells on Templates, Speed Wins (keep the Win IDs) and Sprint Plan.',
            'On Settings, set today\'s date and your weekly capacity. Leave the Google thresholds as they are.',
            'List your main templates (home, product, category, article, checkout) per device. Add p75 field data from PageSpeed Insights or Search Console, monthly visits and the LCP breakdown.',
            'Read the Biggest LCP gap, First fix to try and Red flags columns. Add matching fixes from the Fix Library on Speed Wins.',
            'Choose effort and confidence for every win. Sort by Priority score and put P1 quick wins on the Sprint Plan first.',
            'When a fix ships, add the Shipped on date and the Before value. After 28 days, add the After value from field data and read the Result.',
            'Review every month and after every big release. Move metrics from Poor to Good one template at a time.',
        ],
        url,
    )
    order = ['Start Here', 'Templates', 'Speed Wins', 'Fix Library', 'Sprint Plan', 'Dashboard', 'Settings', 'AI Prompts', 'Checklist', 'Sources']
    wb._sheets = [wb[n] for n in order]
    wb.active = 0
    for ws in wb.worksheets:
        ws.sheet_properties.tabColor = K.GREEN if ws.title in order[:6] else 'A6EF39'
    wb.save(path)


PREVIEW = {'sheet': 'Speed Wins', 'header_row': 4, 'rows': 12,
           'cols': [1, 3, 4, len(SW_IN) + 1, len(SW_IN) + 4, len(SW_IN) + 12, len(SW_IN) + 14, len(SW_IN) + 15],
           'formula_idx': [3, 4, 5, 6, 7]}


def check(wb):
    """Assert the worked examples used in the guide."""
    t = wb['Templates']
    tv = lambda h, r: t[f'{TC[h]}{r}'].value
    r = 6   # Product page (Mobile)
    assert tv('Key (template and device)', r) == 'Product page (Mobile)'
    assert abs(tv('Traffic share', r) - 96000 / 303500) < 1e-9
    assert tv('LCP status', r) == 'Needs improvement' and tv('INP status', r) == 'Needs improvement' and tv('CLS status', r) == 'Needs improvement'
    assert tv('Core Web Vitals', r) == 'Failed' and tv('Speed score (0 to 100)', r) == 77, tv('Speed score (0 to 100)', r)
    assert tv('LCP breakdown total (ms)', r) == 3600 and abs(tv('Load delay share', r) - 1300 / 3600) < 1e-9
    assert tv('Biggest LCP gap', r) == 'Resource load delay', tv('Biggest LCP gap', r)
    assert tv('Red flags', r) == 'LCP image is lazy loaded. LCP image is not in the initial HTML.', tv('Red flags', r)
    assert tv('Open wins', r) == 4 and tv('Wins shipped or validated', r) == 1, (tv('Open wins', r), tv('Wins shipped or validated', r))
    assert tv('Core Web Vitals', 5) == 'Passed' and tv('Speed score (0 to 100)', 5) == 100
    assert tv('Biggest LCP gap', 8) == 'Element render delay' and tv('CLS status', 8) == 'Poor'
    assert tv('Biggest LCP gap', 9) == 'Element render delay' and tv('TTFB status', 9) == 'Poor', tv('Biggest LCP gap', 9)
    assert tv('Red flags', 12) == 'LCP image is not in the initial HTML. Lab data only: confirm with field data.', tv('Red flags', 12)
    w = wb['Speed Wins']
    v = lambda h, r: w[f'{WC[h]}{r}'].value
    r = 5   # SW-001
    assert w[f'A{r}'].value == 'SW-001' and v('Metric', r) == 'LCP' and v('Metric status now', r) == 'Needs improvement'
    assert v('Status factor', r) == 0.6 and v('Traffic factor', r) == 1 and v('Revenue factor', r) == 1.5 and v('Impact points', r) == 3
    assert v('Value (0 to 100)', r) == 90 and v('Priority score', r) == 90 and v('Priority', r) == 'P1: do now' and v('Quadrant', r) == 'Quick win', v('Value (0 to 100)', r)
    exp = {}
    for rr in range(SW_FIRST, SW_FIRST + len(WINS)):
        exp[w[f'A{rr}'].value] = (v('Value (0 to 100)', rr), v('Priority score', rr), v('Priority', rr), v('Quadrant', rr), v('Result', rr))
    assert exp['SW-003'][2] == 'Shipped' and exp['SW-003'][4] == 'Wait for field data: 24 days left', exp['SW-003']
    assert exp['SW-006'][:4] == (50, 25, 'P2: this sprint', 'Quick win'), exp['SW-006']
    assert exp['SW-007'][:4] == (40, 8, 'P3: plan it', 'Big bet'), exp['SW-007']
    assert exp['SW-008'][:4] == (30, 15, 'P2: this sprint', 'Quick win'), exp['SW-008']
    assert exp['SW-009'][:3] == (50, 50, 'P1: do now'), exp['SW-009']
    assert exp['SW-010'][3] == 'Small task' and exp['SW-010'][2] == 'P3: plan it', exp['SW-010']
    assert exp['SW-016'][4] == 'Now good' and exp['SW-017'][4] == 'Improved, not good yet' and exp['SW-018'][4] == 'No improvement: investigate', (exp['SW-016'], exp['SW-017'], exp['SW-018'])
    assert exp['SW-015'][2] == 'P4: later', exp['SW-015']
    d = wb['Dashboard']
    vals = {d.cell(row=r, column=1).value: d.cell(row=r, column=2).value for r in range(5, 21)}
    assert vals['Template and device rows measured'] == 8 and vals['Rows passing Core Web Vitals'] == 1, vals
    assert vals['Open wins'] == 15 and vals['Shipped, waiting for field data'] == 1 and vals['Fixes now good'] == 1, vals
    assert d['D6'].value == 'SW-001', d['D6'].value
    p = wb['Sprint Plan']
    assert p['M5'].value == 'Ready for development' and p['M6'].value == 'Passed: mark the win Shipped' and p['M8'].value == 'Write the acceptance criteria', (p['M6'].value, p['M8'].value)
    assert p['M10'].value == 'Choose how to validate'
    assert p['P6'].value == 4 and p['P7'].value == 5 and p['P9'].value == 8 and p['R9'].value == 'Over capacity by 3', (p['P6'].value, p['P7'].value, p['P8'].value, p['P9'].value, p['R9'].value)
    return exp, vals
