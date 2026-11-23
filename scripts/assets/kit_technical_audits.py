"""Technical SEO Audit Kit workbook (asset 12).

Audit Checks: a library of 61 technical checks in 13 areas (crawling, indexing, status codes, canonicals,
structure, sitemaps, JavaScript, mobile, page experience, HTTPS, structured data, international and AI search
readiness). You mark each check Pass, Warning, Fail, Not checked or Not applicable; every check carries a default
severity, so the workbook gives a severity weighted health score per area and for the whole site, and flags
failed checks that have no issue logged yet.
Issue Log: one row per issue found (500 rows). You add the check, the section, URLs affected, the section size,
impressions on the affected URLs, effort, owner, status and dates. The log works out severity, reach and traffic
factors, a priority score (0 to 100), a priority band (P1 to P4), the fix deadline from the severity and whether
the issue is on track, due soon, overdue or closed on time.
Fix Plan: turn issues into developer tickets with acceptance criteria, a week and a validation method, and check
each week against your fix capacity. Dashboard sums it all up.
"""
import datetime
from openpyxl.styles import PatternFill, Font, Alignment
from openpyxl.formatting.rule import CellIsRule, ColorScaleRule, FormulaRule
from openpyxl.chart import BarChart, Reference
from openpyxl.utils import get_column_letter as L
import kitlib as K

AC_FIRST, AC_LAST = 5, 104      # Audit Checks (100 rows)
IL_FIRST, IL_LAST = 5, 504      # Issue Log (500 rows)
FP_FIRST, FP_LAST = 5, 104      # Fix Plan (100 rows)
S = 'Settings'
ACS = "'Audit Checks'"
ILS = "'Issue Log'"
FPS = "'Fix Plan'"

(DATE, P1, P2, P3, CRIT, SOON, BLANKF, GA, GB, GC, CAP) = (f'{S}!$B${r}' for r in range(5, 16))
SEV_RNG = f'{S}!$F$6:$H$9'
EFF_RNG = f'{S}!$F$14:$G$17'
REACH_RNG = f'{S}!$F$22:$G$25'
TRAF_RNG = f'{S}!$F$30:$G$33'

AREAS = ['Crawling and robots.txt', 'Indexing and directives', 'Status codes and redirects', 'Canonicals and duplicates',
         'Site structure and links', 'XML sitemaps', 'JavaScript and rendering', 'Mobile', 'Page experience and speed',
         'HTTPS and security', 'Structured data', 'International', 'AI search readiness']
SEVERITY = [('Critical', 10, 7, 'Pages you need are out of Search or cannot be crawled'),
            ('High', 6, 14, 'Real loss of crawling, indexing or rankings on many URLs'),
            ('Medium', 3, 30, 'Waste, confusion or weaker signals'),
            ('Low', 1, 90, 'Hygiene and polish')]
EFFORT = [('S', 1, 'Under a day'), ('M', 2, 'A few days'), ('L', 3, 'One to two weeks'), ('XL', 5, 'A project')]
REACH = [(0, 0.2), (0.01, 0.4), (0.1, 0.7), (0.5, 1)]
TRAFFIC = [(0, 0.2), (100, 0.4), (1000, 0.7), (10000, 1)]
RESULTS = [('Pass', 1), ('Warning', 0.5), ('Fail', 0), ('Not checked', None), ('Not applicable', None)]
STATUSES = ['Open', 'In progress', 'Validating', 'Fixed', "Won't fix"]
OWNERS = ['SEO', 'Developer', 'Content', 'Hosting or IT', 'Design']
METHODS = ['Recrawl', 'URL Inspection', 'Search Console Validate fix', 'PageSpeed Insights', 'Rich Results Test', 'Server logs', 'Manual check']
WEEKS = [f'Week {i}' for i in range(1, 9)]
VRES = ['Not started', 'Passed', 'Failed']

# id, area index, check, how to test, pass rule, default severity
CHECKS = [
    ('TA01', 0, 'robots.txt answers with 200 (or 404), never 5xx', 'Open /robots.txt; Search Console robots.txt report', 'Status 200. A 4xx means no rules; a 5xx makes Google stop crawling for the first 12 hours', 'Critical'),
    ('TA02', 0, 'No page you want in Search is blocked by robots.txt', 'robots.txt tester on key URLs of every template', 'Every important URL allowed for Googlebot', 'Critical'),
    ('TA03', 0, 'CSS, JavaScript and images needed to render are not blocked', 'URL Inspection, View crawled page, More info', 'No blocked page resources', 'High'),
    ('TA04', 0, 'robots.txt is under 500 KiB and uses only fields Google supports', 'File size; read every line', 'Under 500 KiB; only user-agent, allow, disallow and sitemap matter to Google', 'Low'),
    ('TA05', 0, 'A Googlebot group, if you have one, repeats every rule it needs', 'Read the groups in robots.txt', 'Google obeys only the most specific group, so the * rules do not apply to it', 'High'),
    ('TA06', 0, 'CDN, firewall and bot protection let Googlebot through', 'Crawl Stats report host status; CDN or firewall logs', 'No blocks, challenges or 403 spikes for Googlebot', 'Critical'),
    ('TA07', 0, 'Server answers crawlers without 5xx or 429 errors', 'Crawl Stats report, By response', 'Server errors close to zero', 'High'),
    ('TA08', 1, 'No noindex on pages you want indexed', 'Crawl: meta robots and X-Robots-Tag', 'Zero', 'Critical'),
    ('TA09', 1, 'Noindex pages are not blocked by robots.txt', 'Compare noindex URLs with robots.txt rules', 'Google can crawl every page that carries a noindex', 'Medium'),
    ('TA10', 1, 'Important pages show as indexed', 'Page indexing report; URL Inspection', 'Every important canonical page indexed', 'High'),
    ('TA11', 1, 'Crawled and Discovered currently not indexed pages reviewed', 'Page indexing report, Why pages are not indexed', 'Reviewed with a plan to improve, merge or remove', 'Medium'),
    ('TA12', 1, 'No soft 404s: empty or error pages do not return 200', 'Page indexing report, Soft 404; crawl for thin pages', 'Zero soft 404 pages', 'Medium'),
    ('TA13', 1, 'Staging, test and internal search pages stay out of the index', 'Crawl; site: searches; Page indexing report', 'None indexed', 'High'),
    ('TA14', 2, 'Important pages return 200', 'Crawl', 'Every important URL returns 200', 'Critical'),
    ('TA15', 2, 'Removed pages return 404 or 410', 'Crawl old URLs', 'Not 200, and not a redirect to the home page', 'Medium'),
    ('TA16', 2, 'Permanent moves use 301 or 308', 'Crawl redirects', 'No 302 or 307 for permanent moves', 'Medium'),
    ('TA17', 2, 'Internal links point to the final URL (no redirect chains)', 'Crawl: links to redirects and chains', 'No internal links to redirects; no chains', 'Medium'),
    ('TA18', 2, 'No redirect loops or redirect errors', 'Crawl; Page indexing report, Redirect error', 'Zero', 'High'),
    ('TA19', 2, 'No internal links to 4xx pages', 'Crawl: broken internal links', 'Zero', 'Medium'),
    ('TA20', 2, 'The custom 404 page returns a real 404 status', 'Open a made up URL and check the status', 'Status 404', 'Medium'),
    ('TA21', 3, 'Every indexable page has a self referencing canonical', 'Crawl: canonical column', 'All indexable pages', 'Medium'),
    ('TA22', 3, 'Canonicals point to live, indexable URLs', 'Crawl: canonical target status', 'No canonical to a redirect, 404 or noindex page', 'High'),
    ('TA23', 3, 'Canonical, sitemap and internal links name the same URL', 'Compare crawl, sitemap and canonicals', 'One URL per page everywhere', 'Medium'),
    ('TA24', 3, 'One version of the site: http, www and trailing slash variants redirect', 'Open all 4 host variants and a no slash URL', 'All variants 301 to the one version', 'High'),
    ('TA25', 3, 'Parameter and filter URLs are canonicalised or kept out of the crawl', 'Crawl URLs with ?', 'No indexable duplicates from parameters', 'Medium'),
    ('TA26', 3, 'Google selected canonical matches yours on key pages', 'URL Inspection: user declared vs Google selected', 'They match', 'Medium'),
    ('TA27', 4, 'No orphan pages among important pages', 'Crawl compared with sitemap and analytics', 'Every important page has at least one internal link', 'High'),
    ('TA28', 4, 'Important pages within 3 clicks of the home page', 'Crawl depth', '3 clicks or less (an assumption, not a Google rule)', 'Medium'),
    ('TA29', 4, 'Links are real <a href> elements', 'Crawl with and without JavaScript', 'No links that only work with onclick or buttons', 'High'),
    ('TA30', 4, 'Hub and category pages link to every page in their section', 'Crawl: links from hubs', 'Every section page linked from its hub', 'Low'),
    ('TA31', 4, 'Paginated lists use crawlable links to each page', 'Crawl category pages', 'Page 2 onward reachable through <a href> links', 'Low'),
    ('TA32', 5, 'Sitemap submitted and read successfully', 'Search Console Sitemaps report', 'Status Success', 'High'),
    ('TA33', 5, 'Sitemaps list only 200, indexable, canonical URLs', 'Crawl the sitemap URLs', 'Zero redirects, 404s, noindex or canonicalised URLs', 'Medium'),
    ('TA34', 5, 'Each sitemap file has at most 50,000 URLs and 50 MB uncompressed', 'File check', 'Within both limits; use a sitemap index above them', 'Medium'),
    ('TA35', 5, 'lastmod matches real content changes', 'Compare lastmod with real update dates', 'Accurate, not bumped on every build', 'Low'),
    ('TA36', 5, 'Sitemap listed in robots.txt with an absolute URL', 'Read robots.txt', 'Sitemap: https://... line present', 'Low'),
    ('TA37', 6, 'Main content and links appear in the rendered HTML Google sees', 'URL Inspection, View crawled page, HTML', 'Content and links present', 'High'),
    ('TA38', 6, 'Key content and meta tags are in the initial HTML', 'View source compared with the rendered page', 'Main text, title, description and links without JavaScript', 'Medium'),
    ('TA39', 6, 'App routes return real status codes or noindex for errors', 'Open a bad route in a single page app', 'A 404 status, or noindex on error views', 'Medium'),
    ('TA40', 6, 'No primary content that loads only after a click, swipe or typing', 'Manual review of tabs, carousels and load more', 'Primary content loads without interaction', 'Medium'),
    ('TA41', 7, 'Mobile has the same content, headings, structured data and meta as desktop', 'Compare mobile and desktop versions', 'Equivalent on both', 'High'),
    ('TA42', 7, 'Viewport set and text readable without zooming', 'Lighthouse; a real phone', 'Viewport meta present; no horizontal scroll', 'Medium'),
    ('TA43', 7, 'No pop ups that hide the main content on mobile', 'Manual check on a phone', 'Content visible on arrival', 'Low'),
    ('TA44', 8, 'LCP is good: 2.5 seconds or less at the 75th percentile', 'Search Console Core Web Vitals; PageSpeed Insights field data', 'Good for each template', 'High'),
    ('TA45', 8, 'INP is good: 200 ms or less at the 75th percentile', 'Search Console Core Web Vitals; PageSpeed Insights field data', 'Good for each template', 'High'),
    ('TA46', 8, 'CLS is good: 0.1 or less at the 75th percentile', 'Search Console Core Web Vitals; PageSpeed Insights field data', 'Good for each template', 'Medium'),
    ('TA47', 8, 'Images are sized, compressed and lazy loaded below the fold', 'Lighthouse; crawl image sizes', 'No oversized images; hero image not lazy loaded', 'Low'),
    ('TA48', 8, 'Server response time is fast for crawlers and people', 'Crawl Stats average response time; PageSpeed Insights', 'Within your Settings target (an assumption)', 'Medium'),
    ('TA49', 9, 'Every page is served over HTTPS with a valid certificate', 'Crawl; browser check', 'All pages HTTPS; certificate valid', 'High'),
    ('TA50', 9, 'No mixed content (http files on https pages)', 'Crawl; browser console', 'Zero', 'Medium'),
    ('TA51', 9, 'http URLs redirect to https with a 301', 'Open http versions of key URLs', '301 to the https URL', 'High'),
    ('TA52', 9, 'No security issues or manual actions', 'Search Console Security issues and Manual actions', 'None reported', 'Critical'),
    ('TA53', 10, 'Structured data passes the Rich Results Test', 'Rich Results Test on each template', 'No errors', 'Medium'),
    ('TA54', 10, 'Structured data matches the visible text on the page', 'Compare markup with the page', 'Every marked up value is visible', 'Medium'),
    ('TA55', 10, 'Organization and site name markup on the home page', 'Rich Results Test or Schema Markup Validator', 'Present with name, url and logo', 'Low'),
    ('TA56', 11, 'hreflang tags have return links and valid codes', 'hreflang checker; crawl', 'Every alternate links back', 'Medium'),
    ('TA57', 11, 'Each language version canonicalises to itself', 'Crawl canonicals per language', 'Self canonical per language', 'Medium'),
    ('TA58', 12, 'Snippets are allowed on pages you want in AI features', 'Crawl meta robots: nosnippet, max-snippet, data-nosnippet', 'No unwanted nosnippet or max-snippet:0', 'High'),
    ('TA59', 12, 'AI bot policy decided and robots.txt matches it', 'Read robots.txt for GPTBot, OAI-SearchBot, ClaudeBot, Claude-SearchBot, PerplexityBot, Google-Extended', 'Every bot allowed or blocked on purpose', 'Medium'),
    ('TA60', 12, 'Important content is available as text, not only in images or video', 'Manual review of key templates', 'Key facts in HTML text', 'Medium'),
    ('TA61', 12, 'Server logs show search and AI bots get 200 on key pages', 'Server or CDN logs', 'No 403 or 5xx for bots you allow', 'Low'),
]
NCHK = len(CHECKS)
# Demo results for TrailNest (illustrative): id -> (result, evidence)
DEMO_RESULTS = {
    'TA06': ('Fail', 'Bot fight rule from 14 Nov challenges Googlebot on /trail-guides/'),
    'TA08': ('Fail', '46 new product pages carry noindex from the staging template'),
    'TA12': ('Warning', 'Empty filter pages return 200'),
    'TA17': ('Warning', '620 pages link to http or no slash URLs'),
    'TA20': ('Fail', '/this-page-does-not-exist/ returns 200'),
    'TA22': ('Fail', '212 colour variants canonicalise to 404 parents'),
    'TA24': ('Fail', 'http://www version returns 200 instead of a redirect'),
    'TA27': ('Fail', '38 trail guides have no internal links'),
    'TA31': ('Warning', 'Load more button, no page links'),
    'TA33': ('Warning', '95 redirected or 404 URLs in the product sitemap'),
    'TA38': ('Warning', 'Store locator text loads with JavaScript only'),
    'TA44': ('Warning', 'Product template LCP 3.4 s on mobile (needs improvement)'),
    'TA45': ('Not checked', ''),
    'TA55': ('Warning', 'Logo and sameAs missing'),
    'TA56': ('Not applicable', 'One language only'),
    'TA57': ('Not applicable', 'One language only'),
    'TA58': ('Warning', 'Fix shipped for max-snippet:0, waiting to validate'),
    'TA61': ('Not checked', ''),
}

# Demo: TrailNest, a fictional outdoor gear store (trailnest.example). All issues and numbers are illustrative.
U = 'https://trailnest.example'
# check, issue, example URL, section, affected, section size, impressions, sev override, effort, owner, status, found, fixed, notes
ISSUES = [
    ('TA06', 'Bot protection challenges Googlebot on trail guides since the CDN rule change', '/trail-guides/kedarkantha-trek/', 'Trail guides', 310, 310, 41000, None, 'S', 'Hosting or IT', 'In progress', '2026-11-17', None, 'Crawl Stats shows 403 spike from 14 Nov'),
    ('TA08', 'Noindex left on new product pages from the staging template', '/gear/tents/alpine-2p/', 'Products', 46, 1450, 0, None, 'S', 'Developer', 'Open', '2026-11-18', None, 'New pages, no impressions yet'),
    ('TA44', 'Product template LCP is 3.4 s at p75 on mobile', '/gear/backpacks/ridge-45/', 'Products', 1450, 1450, 96000, None, 'L', 'Developer', 'Open', '2026-11-03', None, 'Hero image not preloaded'),
    ('TA17', 'Internal links to http and no slash URLs create 2 hop redirect chains', '/blog/layering-guide/', 'Whole site', 620, 4200, 18500, None, 'M', 'Developer', 'Open', '2026-11-10', None, ''),
    ('TA22', 'Colour variant canonicals point to discontinued parents that now 404', '/gear/jackets/storm-shell-red/', 'Products', 212, 1450, 7800, None, 'M', 'Developer', 'Open', '2026-11-12', None, 'Worked example in the guide'),
    ('TA27', 'Trail guides with no internal links since the blog redesign', '/trail-guides/hampta-pass/', 'Trail guides', 38, 310, 2400, None, 'S', 'Content', 'Open', '2026-11-12', None, ''),
    ('TA12', 'Empty filter pages (0 products) return 200: soft 404', '/gear/tents/?brand=none', 'Filter pages', 380, 2100, 300, None, 'M', 'Developer', 'Open', '2026-11-10', None, ''),
    ('TA38', 'Store locator text and addresses load only with JavaScript', '/stores/pune/', 'Store pages', 24, 24, 600, None, 'L', 'Developer', 'Open', '2026-11-10', None, ''),
    ('TA33', 'Sitemap lists redirected and 404 URLs', '/sitemap-products.xml', 'Sitemaps', 95, 3650, None, None, 'S', 'Developer', 'Open', '2026-11-10', None, 'Impressions not relevant'),
    ('TA50', 'Mixed content: blog images loaded over http', '/blog/monsoon-trek-checklist/', 'Blog', 140, 520, 9000, None, 'S', 'Developer', 'Fixed', '2026-11-03', '2026-11-12', ''),
    ('TA58', 'max-snippet:0 set by an old plugin on gear guides', '/blog/how-to-choose-a-sleeping-bag/', 'Gear guides', 64, 310, 22000, None, 'S', 'SEO', 'Validating', '2026-11-14', None, 'Blocks text snippets, so no AI Overview links'),
    ('TA59', 'robots.txt blocked OAI-SearchBot by mistake (copied block list)', '/robots.txt', 'Whole site', 4200, 4200, None, None, 'S', 'SEO', 'Fixed', '2026-10-20', '2026-11-21', 'Policy: allow AI search, block training'),
    ('TA55', 'Organization markup missing logo and sameAs', '/', 'Home', 1, 1, 30000, None, 'S', 'SEO', 'Open', '2026-11-10', None, ''),
    ('TA31', 'Category pagination uses a Load more button without page links', '/gear/tents/', 'Category pages', 85, 85, 14000, None, 'M', 'Developer', 'Open', '2026-11-10', None, ''),
    ('TA20', 'Custom 404 page returns 200', '/this-page-does-not-exist/', 'Whole site', None, None, None, 'High', 'S', 'Developer', 'Open', '2026-11-10', None, 'Raised to High: every mistyped URL becomes a soft 404'),
]
# issue number, week, done when, method, result
PLAN = [
    (1, 'Week 1', 'Verified Googlebot gets 200 on 20 sample trail guides in URL Inspection; no 403 in Crawl Stats for 7 days', 'URL Inspection', 'Not started'),
    (2, 'Week 1', 'All 46 pages have no noindex; URL Inspection says indexing allowed', 'URL Inspection', 'Not started'),
    (6, 'Week 1', 'Each guide linked from its region hub and 2 related guides; recrawl shows 0 orphans', 'Recrawl', 'Not started'),
    (11, 'Week 1', 'max-snippet:0 gone from all 64 guides', 'Recrawl', 'Passed'),
    (5, 'Week 2', 'Each variant canonicalises to a live colour page or to itself; 0 canonicals to 404', 'Recrawl', 'Not started'),
    (3, 'Week 2', '', 'PageSpeed Insights', 'Not started'),
    (7, 'Week 2', 'Filter pages with 0 products return 404 or noindex', 'Recrawl', 'Not started'),
    (8, 'Week 2', 'Store address and hours in the initial HTML', 'Manual check', 'Not started'),
    (15, 'Week 3', 'A made up URL returns status 404 with the custom page', None, 'Not started'),
    (4, None, 'All internal links point to https URLs with a trailing slash', 'Recrawl', 'Not started'),
]

AC_HEAD = ['ID', 'Area', 'Check', 'How to test', 'Pass rule', 'Default severity', 'Result', 'Evidence or notes',
           'Weight', 'Result score', 'Points earned', 'Points possible', 'Issues logged', 'Open issues', 'Status']
AC_F = tuple(range(9, 16))
IL_IN = ['Issue ID', 'Check ID', 'Issue found', 'Example URL', 'Section or template', 'URLs affected', 'URLs in the section',
         'Impressions on affected URLs (28 days)', 'Severity override (blank = default)', 'Effort', 'Owner', 'Status',
         'Found on', 'Fixed on', 'Notes']
IL_FH = ['Area', 'Check', 'Severity', 'Severity weight', 'Share of section affected', 'Reach factor', 'Traffic factor',
         'Effort points', 'Priority score (0 to 100)', 'Priority', 'Fix within (days)', 'Due date', 'Days open',
         'Deadline status', 'How to retest', 'Rank (helper)']
IL_HEAD = IL_IN + IL_FH
IC = {h: L(i + 1) for i, h in enumerate(IL_HEAD)}
IL_F = tuple(range(len(IL_IN) + 1, len(IL_HEAD) + 1))


def ac(c):
    return f'{ACS}!${c}${AC_FIRST}:${c}${AC_LAST}'


def il(c):
    return f'{ILS}!${c}${IL_FIRST}:${c}${IL_LAST}'


def d(s):
    return datetime.date.fromisoformat(s) if s else None


def settings_sheet(wb):
    ws = wb.create_sheet(S)
    ws.sheet_view.showGridLines = False
    K.title_block(ws, 'Settings', 'Every rule, weight and list used by this workbook. Change a blue value and every score and priority updates.')
    for c, w in zip('ABCDEFGHIJKLMNOPQRS', [52, 14, 3, 3, 3, 16, 12, 14, 50, 3, 28, 3, 16, 10, 14, 18, 28, 10, 14]):
        ws.column_dimensions[c].width = w
    rows = [
        (4, 'AUDIT AND PRIORITY RULES', None, None),
        (5, 'Audit date (set it to the day you audit)', datetime.date(2026, 11, 23), 'dd mmm yyyy'),
        (6, 'P1: fix now when the priority score is at least', 40, '0'),
        (7, 'P2: this sprint when at least', 15, '0'),
        (8, 'P3: plan it when at least (below = P4: backlog)', 6, '0'),
        (9, 'Critical issues are always P1 (Yes or No)', 'Yes', '@'),
        (10, 'Due soon: warn this many days before the due date', 7, '0'),
        (11, 'Factor used when reach or traffic is blank', 0.4, '0.0'),
        (12, 'Health grade A when the score is at least', 90, '0'),
        (13, 'Health grade B when at least', 75, '0'),
        (14, 'Health grade C when at least (below = D)', 60, '0'),
        (15, 'Fix capacity per week (effort points)', 8, '0'),
    ]
    for r, label, val, fmt in rows:
        a = ws.cell(row=r, column=1, value=label)
        a.font = K.f(10, val is None, K.DEEP if val is None else K.INK)
        if val is not None:
            c = ws.cell(row=r, column=2, value=val)
            c.border, c.fill = K.BORDER, K.INPUT_FILL
            c.font = K.f(10, True, '0000FF')
            c.number_format = fmt
    K.dropdown(ws, 'B9', '"Yes,No"')
    ws['A17'] = ('Priority score = 10 x severity weight x the average of the reach and traffic factors / effort points, '
                 'rounded. A Critical issue on every URL of a busy section that takes under a day scores 100. Every weight, '
                 'band, deadline and threshold on this tab is an assumption of this kit for you to tune; Google publishes no '
                 'severity scale.')
    ws['A17'].font = K.f(9, False, '777777', True)
    ws['A17'].alignment = Alignment(wrap_text=True, vertical='top')
    ws.merge_cells('A17:B24')

    def table(col, row, title, heads, vals, fmts=None):
        ws.cell(row=row - 1, column=col, value=title).font = K.f(10, True, K.DEEP)
        for j, h in enumerate(heads):
            ws.cell(row=row, column=col + j, value=h).font = K.f(9, True, '555555')
        for i, v in enumerate(vals):
            for j in range(len(heads)):
                c = ws.cell(row=row + 1 + i, column=col + j, value=v[j])
                c.fill, c.border, c.font = K.INPUT_FILL, K.BORDER, K.f(10, j == 1, '0000FF' if j == 1 else K.INK)
                if fmts and fmts[j]:
                    c.number_format = fmts[j]
    table(6, 5, 'SEVERITY', ['Severity', 'Weight', 'Fix within (days)', 'Meaning'], SEVERITY)
    table(6, 13, 'EFFORT', ['Effort', 'Points', 'Meaning'], EFFORT)
    table(6, 21, 'REACH (share of the section affected)', ['At least', 'Factor'], REACH, ['0%', '0.0'])
    table(6, 29, 'TRAFFIC (impressions on affected URLs, 28 days)', ['At least', 'Factor'], TRAFFIC, ['#,##0', '0.0'])
    ws['F35'] = 'Keep the At least values in rising order: the lookups use them as bands.'
    ws['F35'].font = K.f(8, False, '777777', True)
    ws['K4'] = 'LISTS'
    ws['K4'].font = K.f(10, True, K.DEEP)
    lists = [('K', 'Area', AREAS), ('M', 'Result', [r for r, _ in RESULTS]), ('N', 'Score', [s for _, s in RESULTS]),
             ('O', 'Status', STATUSES), ('P', 'Owner', OWNERS), ('Q', 'Validation method', METHODS), ('R', 'Week', WEEKS),
             ('S', 'Validation result', VRES)]
    for col, head, vals in lists:
        ws[f'{col}5'] = head
        ws[f'{col}5'].font = K.f(9, True, '555555')
        n = 15 if col in 'KP' else len(vals)
        for i in range(n):
            c = ws[f'{col}{6 + i}']
            c.value = vals[i] if i < len(vals) else None
            c.fill, c.border, c.font = K.INPUT_FILL, K.BORDER, K.f(10)
    ws['K22'] = 'Results score Pass 1, Warning 0.5 and Fail 0. Not checked and Not applicable are left out of the score.'
    ws['K22'].font = K.f(8, False, '777777', True)
    return ws


def checks_sheet(wb):
    ws = wb.create_sheet('Audit Checks')
    ws.sheet_view.showGridLines = False
    K.title_block(ws, 'Audit checks', f'{NCHK} technical checks in {len(AREAS)} areas. Column G holds DEMO results for TrailNest, a fictional outdoor gear store. Choose your own result for every check; add your own checks in the empty rows.')
    ws['A2'].font = K.f(10, True, 'B45309')
    ws['A3'] = 'Pass = fine, Warning = partly, Fail = fix. Every Warning and Fail should have at least one row on the Issue Log; the Status column tells you when one is missing.'
    ws['A3'].font = K.f(9, False, '666666', True)
    K.header_row(ws, 4, AC_HEAD, formula_cols=AC_F, widths=[7, 22, 46, 36, 40, 10, 12, 40, 8, 8, 8, 8, 8, 8, 30])
    for r in range(AC_FIRST, AC_LAST + 1):
        i = r - AC_FIRST
        if i < NCHK:
            cid, ai, chk, how, rule, sev = CHECKS[i]
            res, ev = DEMO_RESULTS.get(cid, ('Pass', ''))
            for col, v in enumerate([cid, AREAS[ai], chk, how, rule, sev, res, ev], 1):
                if v not in (None, ''):
                    ws.cell(row=r, column=col, value=v)
        e = f'OR(A{r}="",C{r}="")'
        scored = f'OR(G{r}="Pass",G{r}="Warning",G{r}="Fail")'
        ws[f'I{r}'] = f'=IF({e},"",IFERROR(VLOOKUP(F{r},{SEV_RNG},2,FALSE),0))'
        ws[f'J{r}'] = f'=IF(OR({e},NOT({scored})),"",VLOOKUP(G{r},{S}!$M$6:$N$10,2,FALSE))'
        ws[f'K{r}'] = f'=IF(J{r}="","",I{r}*J{r})'
        ws[f'L{r}'] = f'=IF(J{r}="","",I{r})'
        ws[f'M{r}'] = f'=IF({e},"",COUNTIF({il("B")},A{r}))'
        opn = f'COUNTIFS({il("B")},A{r},{il("L")},"<>Fixed",{il("L")},"<>Won\'t fix",{il("C")},"<>")'
        ws[f'N{r}'] = f'=IF({e},"",{opn})'
        ws[f'O{r}'] = (f'=IF({e},"",IF(OR(G{r}="",G{r}="Not checked"),"Not checked yet",IF(G{r}="Not applicable","Not applicable",'
                       f'IF(G{r}="Pass",IF(N{r}>0,"Pass, but issues are open: recheck","OK"),IF(M{r}=0,"Log an issue","Issue logged")))))')
    K.style_body(ws, AC_FIRST, AC_LAST, len(AC_HEAD), formula_cols=AC_F, wrap_cols=(3, 4, 5, 8, 15))
    K.dropdown(ws, f'B{AC_FIRST}:B{AC_LAST}', f'{S}!$K$6:$K$20')
    K.dropdown(ws, f'F{AC_FIRST}:F{AC_LAST}', f'{S}!$F$6:$F$9')
    K.dropdown(ws, f'G{AC_FIRST}:G{AC_LAST}', f'{S}!$M$6:$M$10', 'Pass, Warning, Fail, Not checked or Not applicable')
    g = f'G{AC_FIRST}:G{AC_LAST}'
    for val, col in (('Pass', 'D9F2C4'), ('Warning', 'FFF4CC'), ('Fail', 'F8D7D3')):
        ws.conditional_formatting.add(g, CellIsRule(operator='equal', formula=[f'"{val}"'], fill=PatternFill('solid', fgColor=col), font=Font(name=K.FONT, bold=True)))
    o = f'O{AC_FIRST}:O{AC_LAST}'
    ws.conditional_formatting.add(o, CellIsRule(operator='equal', formula=['"Log an issue"'], fill=PatternFill('solid', fgColor='9B2C1F'), font=Font(name=K.FONT, bold=True, color='FFFFFF')))
    ws.conditional_formatting.add(o, FormulaRule(formula=[f'LEFT(O{AC_FIRST},4)="Pass"'], fill=PatternFill('solid', fgColor='FFF4CC')))
    ws.conditional_formatting.add(o, CellIsRule(operator='equal', formula=['"OK"'], fill=PatternFill('solid', fgColor='D9F2C4')))
    sv = f'F{AC_FIRST}:F{AC_LAST}'
    ws.conditional_formatting.add(sv, CellIsRule(operator='equal', formula=['"Critical"'], font=Font(name=K.FONT, bold=True, color='9B2C1F')))
    for r in range(AC_FIRST, AC_FIRST + NCHK):
        ws.row_dimensions[r].height = 30
    ws.freeze_panes = 'D5'
    ws.auto_filter.ref = f'A4:O{AC_LAST}'
    return ws


def issues_sheet(wb):
    ws = wb.create_sheet('Issue Log')
    ws.sheet_view.showGridLines = False
    K.title_block(ws, 'Issue log', f'One row per issue. Rows 5 to {4 + len(ISSUES)} are DEMO issues for TrailNest (illustrative numbers). To start your own, delete the yellow demo cells from column B to O; keep the Issue IDs in column A (they stay fixed when you sort). 500 rows ready.')
    ws['A2'].font = K.f(10, True, 'B45309')
    ws['A3'] = 'Add the check ID, the section or template, URLs affected out of the URLs in that section, and impressions from Search Console for 28 days. Sort by Priority score; work P1 first.'
    ws['A3'].font = K.f(9, False, '666666', True)
    widths = [9, 8, 44, 36, 16, 10, 10, 12, 12, 7, 13, 11, 11, 11, 30, 22, 40, 9, 8, 9, 8, 8, 7, 10, 16, 8, 11, 8, 18, 34, 8]
    K.header_row(ws, 4, IL_HEAD, formula_cols=IL_F, widths=widths)
    c = IC
    chk_tbl = f'{ac("A")}:{ACS}!$F${AC_LAST}'
    for r in range(IL_FIRST, IL_LAST + 1):
        i = r - IL_FIRST
        if i < len(ISSUES):
            row = list(ISSUES[i])
            row[2] = U + row[2]
            row[11], row[12] = d(row[11]), d(row[12])
            for col, v in enumerate(row, 2):
                if v not in (None, ''):
                    ws.cell(row=r, column=col, value=v)
        e = f'C{r}=""'
        closed = f'OR(L{r}="Fixed",L{r}="Won\'t fix")'
        g = lambda h: f'{c[h]}{r}'
        f = {}
        ws[f'A{r}'] = f'ISS-{i + 1:03d}'
        f['Area'] = f'=IF(OR({e},B{r}=""),"",IFERROR(VLOOKUP(B{r},{chk_tbl},2,FALSE),"Check ID not found"))'
        f['Check'] = f'=IF(OR({e},B{r}=""),"",IFERROR(VLOOKUP(B{r},{chk_tbl},3,FALSE),""))'
        f['Severity'] = f'=IF({e},"",IF(I{r}<>"",I{r},IFERROR(VLOOKUP(B{r},{chk_tbl},6,FALSE),"Medium")))'
        sev = g('Severity')
        f['Severity weight'] = f'=IF({e},"",IFERROR(VLOOKUP({sev},{SEV_RNG},2,FALSE),0))'
        f['Share of section affected'] = f'=IF(OR({e},N(F{r})=0,N(G{r})=0),"",MIN(1,F{r}/G{r}))'
        sh = g('Share of section affected')
        f['Reach factor'] = f'=IF({e},"",IF({sh}="",{BLANKF},VLOOKUP({sh},{REACH_RNG},2,TRUE)))'
        f['Traffic factor'] = f'=IF({e},"",IF(H{r}="",{BLANKF},VLOOKUP(N(H{r}),{TRAF_RNG},2,TRUE)))'
        f['Effort points'] = f'=IF({e},"",IFERROR(VLOOKUP(J{r},{EFF_RNG},2,FALSE),2))'
        f['Priority score (0 to 100)'] = f'=IF({e},"",MIN(100,ROUND(10*{g("Severity weight")}*({g("Reach factor")}+{g("Traffic factor")})/2/{g("Effort points")},0)))'
        sc = g('Priority score (0 to 100)')
        f['Priority'] = (f'=IF({e},"",IF({closed},"Closed",IF(L{r}="Validating","Validating",IF(OR(AND({sev}="Critical",{CRIT}="Yes"),{sc}>={P1}),"P1: fix now",'
                         f'IF({sc}>={P2},"P2: this sprint",IF({sc}>={P3},"P3: plan it","P4: backlog"))))))')
        f['Fix within (days)'] = f'=IF({e},"",IFERROR(VLOOKUP({sev},{SEV_RNG},3,FALSE),30))'
        f['Due date'] = f'=IF(OR({e},M{r}=""),"",M{r}+{g("Fix within (days)")})'
        due = g('Due date')
        f['Days open'] = f'=IF(OR({e},M{r}=""),"",IF(N{r}<>"",N{r}-M{r},{DATE}-M{r}))'
        f['Deadline status'] = (f'=IF({e},"",IF({closed},IF(OR(N{r}="",{due}=""),"Closed",IF(N{r}<={due},"Closed on time","Closed late")),'
                                f'IF(L{r}="Validating","Validating",IF(M{r}="","Add a found date",IF({DATE}>{due},"Overdue by "&({DATE}-{due})&" days",'
                                f'IF({due}-{DATE}<={SOON},"Due soon","On track"))))))')
        f['How to retest'] = f'=IF(OR({e},B{r}=""),"",IFERROR(VLOOKUP(B{r},{chk_tbl},4,FALSE),""))'
        f['Rank (helper)'] = f'=IF(OR({e},{closed},L{r}="Validating"),"",{sc}+ROW()/100000)'
        for h, v in f.items():
            ws[f'{c[h]}{r}'] = v
    nf = {6: '#,##0', 7: '#,##0', 8: '#,##0', 13: 'dd mmm yyyy', 14: 'dd mmm yyyy', 20: '0%', 21: '0.0', 22: '0.0', 24: '0',
          27: 'dd mmm yyyy', 28: '0', 31: '0.00000'}
    K.style_body(ws, IL_FIRST, IL_LAST, len(IL_HEAD), formula_cols=IL_F, number_formats=nf, wrap_cols=(3, 15, 17, 30))
    K.dropdown(ws, f'B{IL_FIRST}:B{IL_LAST}', ac('A'), 'The check IDs live on the Audit Checks tab.')
    K.dropdown(ws, f'I{IL_FIRST}:I{IL_LAST}', f'{S}!$F$6:$F$9', 'Leave blank to use the default severity of the check.')
    K.dropdown(ws, f'J{IL_FIRST}:J{IL_LAST}', f'{S}!$F$14:$F$17', 'S under a day, M a few days, L one to two weeks, XL a project.')
    K.dropdown(ws, f'K{IL_FIRST}:K{IL_LAST}', f'{S}!$P$6:$P$20')
    K.dropdown(ws, f'L{IL_FIRST}:L{IL_LAST}', f'{S}!$O$6:$O$10')
    for col in 'FGH':
        K.whole_number(ws, f'{col}{IL_FIRST}:{col}{IL_LAST}', 0, 100000000, 'A whole number.')
    scl = c['Priority score (0 to 100)']
    ws.conditional_formatting.add(f'{scl}{IL_FIRST}:{scl}{IL_LAST}', ColorScaleRule(start_type='num', start_value=0, start_color='FFFFFF', mid_type='num', mid_value=20, mid_color='FFF4CC', end_type='num', end_value=60, end_color='E07A5F'))
    pc = c['Priority']
    pr = f'{pc}{IL_FIRST}:{pc}{IL_LAST}'
    for start, fill, fc in (('P1', '9B2C1F', 'FFFFFF'), ('P2', 'F8D7D3', '9B2C1F'), ('P3', 'FFF4CC', '1F1F1F'), ('P4', 'EEEEEE', '555555'), ('Cl', 'D9F2C4', '1F1F1F'), ('Va', 'EEF8E6', '3D7F12')):
        ws.conditional_formatting.add(pr, FormulaRule(formula=[f'LEFT({pc}{IL_FIRST},2)="{start}"'], fill=PatternFill('solid', fgColor=fill), font=Font(name=K.FONT, bold=True, color=fc)))
    dc = c['Deadline status']
    dr = f'{dc}{IL_FIRST}:{dc}{IL_LAST}'
    ws.conditional_formatting.add(dr, FormulaRule(formula=[f'OR(LEFT({dc}{IL_FIRST},7)="Overdue",{dc}{IL_FIRST}="Closed late")'], fill=PatternFill('solid', fgColor='F8D7D3'), font=Font(name=K.FONT, bold=True, color='9B2C1F')))
    ws.conditional_formatting.add(dr, CellIsRule(operator='equal', formula=['"Due soon"'], fill=PatternFill('solid', fgColor='FFF4CC'), font=Font(name=K.FONT, bold=True)))
    ws.conditional_formatting.add(dr, CellIsRule(operator='equal', formula=['"Closed on time"'], fill=PatternFill('solid', fgColor='D9F2C4')))
    sv = c['Severity']
    ws.conditional_formatting.add(f'{sv}{IL_FIRST}:{sv}{IL_LAST}', CellIsRule(operator='equal', formula=['"Critical"'], font=Font(name=K.FONT, bold=True, color='9B2C1F')))
    ws.column_dimensions[c['Rank (helper)']].hidden = True
    ws.freeze_panes = 'D5'
    ws.auto_filter.ref = f'A4:{L(len(IL_HEAD))}{IL_LAST}'
    return ws


def plan_sheet(wb):
    ws = wb.create_sheet('Fix Plan')
    ws.sheet_view.showGridLines = False
    K.title_block(ws, 'Fix plan', 'Turn issues into developer tickets. Pick an Issue ID, a week, what done looks like and how you will validate it. The ticket text writes itself; the table on the right checks each week against your capacity.')
    head = ['Issue ID', 'Week', 'Done when (acceptance criteria)', 'Validation method', 'Validation result', 'Check', 'Severity',
            'Priority', 'Owner', 'URLs affected', 'Effort points', 'Ticket text (copy into your tracker)', 'Next step']
    fc = tuple(range(6, 14))
    K.header_row(ws, 4, head, formula_cols=fc, widths=[10, 10, 44, 20, 13, 34, 10, 14, 13, 9, 8, 70, 30])
    idx = lambda r: f'MATCH(A{r},{il("A")},0)'
    get = lambda col, r: f'INDEX({il(col)},{idx(r)})'
    for r in range(FP_FIRST, FP_LAST + 1):
        i = r - FP_FIRST
        if i < len(PLAN):
            n, wk, done, meth, res = PLAN[i]
            for col, v in enumerate([f'ISS-{n:03d}', wk, done, meth, res], 1):
                if v not in (None, ''):
                    ws.cell(row=r, column=col, value=v)
        e = f'A{r}=""'
        ok = f'ISNUMBER({idx(r)})'
        ws[f'F{r}'] = f'=IF({e},"",IF({ok},{get(IC["Check"], r)},"Issue ID not found"))'
        ws[f'G{r}'] = f'=IF(OR({e},NOT({ok})),"",{get(IC["Severity"], r)})'
        ws[f'H{r}'] = f'=IF(OR({e},NOT({ok})),"",{get(IC["Priority"], r)})'
        ws[f'I{r}'] = f'=IF(OR({e},NOT({ok})),"",""&{get("K", r)})'
        ws[f'J{r}'] = f'=IF(OR({e},NOT({ok})),"",N({get("F", r)}))'
        ws[f'K{r}'] = f'=IF(OR({e},NOT({ok})),"",{get(IC["Effort points"], r)})'
        ws[f'L{r}'] = (f'=IF(OR({e},NOT({ok})),"","["&G{r}&", "&LEFT(H{r},2)&"] "&{get("C", r)}&". Check: "&F{r}&". "&IF(J{r}>0,TEXT(J{r},"#,##0")&" URLs affected, for example ","Example: ")&{get("D", r)}'
                       f'&". Owner: "&IF(I{r}="","(not set)",I{r})&". Done when: "&IF(C{r}="","(add acceptance criteria)",C{r})&". Validate with: "&IF(D{r}="","(choose a method)",D{r})&".")')
        st = get('L', r)
        ws[f'M{r}'] = (f'=IF({e},"",IF(NOT({ok}),"Fix the Issue ID",IF(E{r}="Passed",IF(OR({st}="Fixed",{st}="Won\'t fix"),"Done","Passed: mark the issue Fixed"),'
                       f'IF(E{r}="Failed","Failed: reopen and fix again",IF(C{r}="","Write the acceptance criteria",IF(B{r}="","Schedule it in a week",'
                       f'IF(D{r}="","Choose how to validate","Ready for development")))))))')
    K.style_body(ws, FP_FIRST, FP_LAST, len(head), formula_cols=fc, number_formats={10: '#,##0'}, wrap_cols=(3, 6, 12, 13))
    for r in range(FP_FIRST, FP_FIRST + len(PLAN)):
        ws.row_dimensions[r].height = 58
    K.dropdown(ws, f'A{FP_FIRST}:A{FP_LAST}', il('A'))
    K.dropdown(ws, f'B{FP_FIRST}:B{FP_LAST}', f'{S}!$R$6:$R$13')
    K.dropdown(ws, f'D{FP_FIRST}:D{FP_LAST}', f'{S}!$Q$6:$Q$12')
    K.dropdown(ws, f'E{FP_FIRST}:E{FP_LAST}', f'{S}!$S$6:$S$8')
    m = f'M{FP_FIRST}:M{FP_LAST}'
    ws.conditional_formatting.add(m, CellIsRule(operator='equal', formula=['"Ready for development"'], fill=PatternFill('solid', fgColor='D9F2C4'), font=Font(name=K.FONT, bold=True)))
    ws.conditional_formatting.add(m, FormulaRule(formula=[f'OR(LEFT(M{FP_FIRST},6)="Failed",LEFT(M{FP_FIRST},3)="Fix")'], fill=PatternFill('solid', fgColor='F8D7D3'), font=Font(name=K.FONT, bold=True, color='9B2C1F')))
    ws.conditional_formatting.add(m, FormulaRule(formula=[f'OR(LEFT(M{FP_FIRST},5)="Write",LEFT(M{FP_FIRST},8)="Schedule",LEFT(M{FP_FIRST},6)="Choose",LEFT(M{FP_FIRST},6)="Passed")'], fill=PatternFill('solid', fgColor='FFF4CC')))
    # capacity table
    ws['O4'] = 'WEEKLY CAPACITY'
    ws['O4'].font = K.f(10, True, K.DEEP)
    for j, h in enumerate(['Week', 'Effort planned', 'Capacity', 'Status']):
        cc = ws.cell(row=5, column=15 + j, value=h)
        cc.font, cc.fill = K.f(10, True, 'FFFFFF'), K.HEAD_F
    for i in range(len(WEEKS)):
        r = 6 + i
        ws.cell(row=r, column=15, value=f'={S}!R{6 + i}')
        ws.cell(row=r, column=16, value=f'=SUMIF($B${FP_FIRST}:$B${FP_LAST},O{r},$K${FP_FIRST}:$K${FP_LAST})')
        ws.cell(row=r, column=17, value=f'={CAP}')
        ws.cell(row=r, column=18, value=f'=IF(P{r}=0,"Free",IF(P{r}>Q{r},"Over capacity by "&(P{r}-Q{r}),"OK"))')
        for cc in range(15, 19):
            cell = ws.cell(row=r, column=cc)
            cell.border, cell.fill, cell.font = K.BORDER, K.FORMULA_FILL, K.f(10)
    r = 6 + len(WEEKS)
    ws.cell(row=r, column=15, value='Not scheduled').font = K.f(10, True)
    ws.cell(row=r, column=16, value=f'=SUMIFS($K${FP_FIRST}:$K${FP_LAST},$A${FP_FIRST}:$A${FP_LAST},"<>",$B${FP_FIRST}:$B${FP_LAST},"")').fill = K.FORMULA_FILL
    for col, w in zip('NOPQR', [3, 14, 10, 9, 22]):
        ws.column_dimensions[col].width = w
    ws.conditional_formatting.add('R6:R13', FormulaRule(formula=['LEFT(R6,4)="Over"'], fill=PatternFill('solid', fgColor='F8D7D3'), font=Font(name=K.FONT, bold=True, color='9B2C1F')))
    ws.freeze_panes = 'B5'
    ws.auto_filter.ref = f'A4:M{FP_LAST}'
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
    for col, w in zip('ABCDEFGHIJK', [46, 12, 3, 10, 40, 16, 9, 7, 16, 18, 3]):
        ws.column_dimensions[col].width = w
    c = IC
    opn = f'{il("L")},"<>Fixed",{il("L")},"<>Won\'t fix",{il("C")},"<>"'
    kpis = [
        ('Technical health score (0 to 100)', f'=IFERROR(ROUND(100*SUM({ac("K")})/SUM({ac("L")}),0),0)', '0'),
        ('Health grade', f'=IF(B5>={GA},"A",IF(B5>={GB},"B",IF(B5>={GC},"C","D")))', '@'),
        ('Checks with a result (of all checks)', f'=COUNTIF({ac("J")},">=0")&" of "&COUNTA({ac("C")})', '@'),
        ('Checks failed', f'=COUNTIF({ac("G")},"Fail")', '0'),
        ('Checks with a warning', f'=COUNTIF({ac("G")},"Warning")', '0'),
        ('Checks not done yet', f'=COUNTIF({ac("O")},"Not checked yet")', '0'),
        ('Failed or warning checks with no issue logged', f'=COUNTIF({ac("O")},"Log an issue")', '0'),
        ('Open issues', f'=COUNTIFS({opn})', '0'),
        ('Open Critical issues', f'=COUNTIFS({opn},{il(c["Severity"])},"Critical")', '0'),
        ('P1 issues to fix now', f'=COUNTIF({il(c["Priority"])},"P1*")', '0'),
        ('Overdue issues', f'=COUNTIF({il(c["Deadline status"])},"Overdue*")', '0'),
        ('Due within the warning window', f'=COUNTIF({il(c["Deadline status"])},"Due soon")', '0'),
        ('URLs affected by open issues', f'=SUMIFS({il("F")},{opn})', '#,##0'),
        ('Impressions on URLs with open issues (28 days)', f'=SUMIFS({il("H")},{opn})', '#,##0'),
        ('Issues closed', f'=COUNTIF({il("L")},"Fixed")+COUNTIF({il("L")},"Won\'t fix")', '0'),
        ('Closed on time (share of closed with dates)', f'=IFERROR(COUNTIF({il(c["Deadline status"])},"Closed on time")/(COUNTIF({il(c["Deadline status"])},"Closed on time")+COUNTIF({il(c["Deadline status"])},"Closed late")),"")', '0%'),
        ('Open effort (effort points)', f'=SUMIFS({il(c["Effort points"])},{opn})', '0'),
        ('Weeks of work at your capacity', f'=IFERROR(ROUND(B21/{CAP},1),"")', '0.0'),
    ]
    ws['A4'] = 'KEY NUMBERS'
    ws['A4'].font = K.f(10, True, K.DEEP)
    for i, (label, fml, fmt) in enumerate(kpis):
        r = 5 + i
        ws.cell(row=r, column=1, value=label).font = K.f(10)
        cell = ws.cell(row=r, column=2, value=fml)
        cell.number_format, cell.font, cell.fill, cell.border = fmt, K.f(11, True), K.FORMULA_FILL, K.BORDER
        cell.alignment = Alignment(horizontal='right')
    ws['D4'] = 'TOP 10 OPEN ISSUES (highest priority score first)'
    ws['D4'].font = K.f(10, True, K.DEEP)
    heads = ['Issue ID', 'Issue', 'Section', 'URLs', 'Score', 'Priority', 'Deadline']
    cols = ['A', 'C', 'E', 'F', c['Priority score (0 to 100)'], c['Priority'], c['Deadline status']]
    for j, h in enumerate(heads):
        cell = ws.cell(row=5, column=4 + j, value=h)
        cell.font, cell.fill = K.f(10, True, 'FFFFFF'), K.HEAD_F
    rk = il(c['Rank (helper)'])
    for k in range(1, 11):
        r = 5 + k
        mt = f'MATCH(LARGE({rk},{k}),{rk},0)'
        for j, col in enumerate(cols):
            cell = ws.cell(row=r, column=4 + j, value=f'=IFERROR(INDEX({il(col)},{mt}),"")')
            cell.border, cell.fill, cell.font = K.BORDER, K.FORMULA_FILL, K.f(9, j == 0)
            cell.alignment = Alignment(wrap_text=j == 1, vertical='top')
            cell.number_format = ['@', '@', '@', '#,##0', '0', '@', '@'][j]
        ws.row_dimensions[r].height = 26
    top = 26
    ws.cell(row=top - 1, column=1, value='HEALTH BY AREA').font = K.f(10, True, K.DEEP)
    for j, h in enumerate(['Area', 'Health score', 'Checks scored', 'Failed', 'Warnings', 'Open issues']):
        cell = ws.cell(row=top, column=1 + j if j == 0 else 1 + j, value=h)
        cell.font, cell.fill = K.f(10, True, 'FFFFFF'), K.HEAD_F
    for i in range(len(AREAS)):
        r = top + 1 + i
        ws.cell(row=r, column=1, value=f'={S}!K{6 + i}')
        ws.cell(row=r, column=2, value=f'=IFERROR(ROUND(100*SUMIF({ac("B")},A{r},{ac("K")})/SUMIF({ac("B")},A{r},{ac("L")}),0),"")')
        ws.cell(row=r, column=3, value=f'=COUNTIFS({ac("B")},A{r},{ac("J")},">=0")')
        ws.cell(row=r, column=4, value=f'=COUNTIFS({ac("B")},A{r},{ac("G")},"Fail")')
        ws.cell(row=r, column=5, value=f'=COUNTIFS({ac("B")},A{r},{ac("G")},"Warning")')
        ws.cell(row=r, column=6, value=f'=COUNTIFS({il(c["Area"])},A{r},{opn})')
        for cc in range(1, 7):
            cell = ws.cell(row=r, column=cc)
            cell.border, cell.fill, cell.font = K.BORDER, K.FORMULA_FILL, K.f(10, cc == 2)
    last = top + len(AREAS)
    ws.conditional_formatting.add(f'B{top + 1}:B{last}', ColorScaleRule(start_type='num', start_value=40, start_color='F8D7D3', mid_type='num', mid_value=75, mid_color='FFF4CC', end_type='num', end_value=100, end_color='B7E4A0'))
    t2 = last + 4
    ws.cell(row=t2 - 1, column=1, value='ISSUES BY SEVERITY').font = K.f(10, True, K.DEEP)
    for j, h in enumerate(['Severity', 'Open', 'Validating', 'Closed']):
        cell = ws.cell(row=t2, column=1 + j, value=h)
        cell.font, cell.fill = K.f(10, True, 'FFFFFF'), K.HEAD_F
    for i, (sv, *_r) in enumerate(SEVERITY):
        r = t2 + 1 + i
        ws.cell(row=r, column=1, value=f'={S}!F{6 + i}')
        ws.cell(row=r, column=2, value=f'=COUNTIFS({il(c["Severity"])},A{r},{il("L")},"Open")+COUNTIFS({il(c["Severity"])},A{r},{il("L")},"In progress")')
        ws.cell(row=r, column=3, value=f'=COUNTIFS({il(c["Severity"])},A{r},{il("L")},"Validating")')
        ws.cell(row=r, column=4, value=f'=COUNTIFS({il(c["Severity"])},A{r},{il("L")},"Fixed")+COUNTIFS({il(c["Severity"])},A{r},{il("L")},"Won\'t fix")')
        for cc in range(1, 5):
            cell = ws.cell(row=r, column=cc)
            cell.border, cell.fill = K.BORDER, K.FORMULA_FILL
    t3 = t2 + 8
    ws.cell(row=t3 - 1, column=1, value='OPEN ISSUES BY PRIORITY').font = K.f(10, True, K.DEEP)
    for j, h in enumerate(['Priority', 'Issues']):
        cell = ws.cell(row=t3, column=1 + j, value=h)
        cell.font, cell.fill = K.f(10, True, 'FFFFFF'), K.HEAD_F
    for i, p in enumerate(['P1: fix now', 'P2: this sprint', 'P3: plan it', 'P4: backlog', 'Validating']):
        r = t3 + 1 + i
        ws.cell(row=r, column=1, value=p).border = K.BORDER
        cell = ws.cell(row=r, column=2, value=f'=COUNTIF({il(c["Priority"])},A{r})')
        cell.border, cell.fill = K.BORDER, K.FORMULA_FILL
    c1 = chart(ws, 'Health score by area', 'Score', 1, [2], top + 1, last, 'H17', [K.GREEN], True, False, h=10, w=17)
    c1.y_axis.scaling.min = 0
    c1.y_axis.scaling.max = 100
    chart(ws, 'Issues by severity', 'Issues', 1, [2, 3, 4], t2 + 1, t2 + 4, 'H38', ['E07A5F', 'F2C94C', K.GREEN], False, True, stacked=True, w=17)
    return ws, top, t2, t3


def build(path, asset, url):
    wb = K.new_book()
    checks_sheet(wb)
    issues_sheet(wb)
    plan_sheet(wb)
    dashboard_sheet(wb)
    settings_sheet(wb)
    K.prompts_sheet(wb, asset['prompts'], url)
    K.checklist_sheet(wb, list(asset['checklist']))
    K.sources_sheet(wb, asset['sources'], [
        ('Demo data', 'TrailNest and every URL in the demo are fictional (.example domain). All results, issues, URL counts, impressions and dates are illustrative, not real data.', ''),
        ('Severity, deadlines and priority score', 'Severity weights (10, 6, 3, 1), fix deadlines (7, 14, 30, 90 days), reach and traffic bands, effort points and the P1 to P4 thresholds are assumptions of this kit. Google publishes no severity scale. Tune them on Settings.', ''),
        ('Minimum requirements', 'Google lists three technical requirements: Googlebot is not blocked, the page works (Google receives an HTTP 200) and the page has indexable content. Meeting them does not guarantee indexing.', 'https://developers.google.com/search/docs/essentials/technical'),
        ('robots.txt', 'Google enforces a 500 KiB size limit, supports user-agent, allow, disallow and sitemap (crawl-delay is not supported), caches the file for up to 24 hours and obeys only the most specific matching group.', 'https://developers.google.com/crawling/docs/robots-txt/robots-txt-spec'),
        ('Status codes', 'Google follows up to 10 redirect hops; 301 and 308 are strong signals, 302 and 307 weak; 4xx URLs are not indexed; 5xx and 429 slow crawling and persistent errors drop URLs.', 'https://developers.google.com/crawling/docs/troubleshooting/http-status-codes'),
        ('Core Web Vitals', 'Good at the 75th percentile: LCP 2.5 s or less, INP 200 ms or less, CLS 0.1 or less. Poor: LCP over 4 s, INP over 500 ms, CLS over 0.25.', 'https://web.dev/articles/defining-core-web-vitals-thresholds'),
        ('AI crawlers and JavaScript', 'A Vercel and MERJ study (December 2024) found that none of the major AI crawlers it measured rendered JavaScript. Behaviour may change; test your own logs.', 'https://vercel.com/blog/the-rise-of-the-ai-crawler'),
    ])
    K.start_here(
        wb, 'Technical SEO Audit Kit',
        [
            f'This workbook runs a full technical SEO audit: {NCHK} checks in {len(AREAS)} areas, from robots.txt, indexing and status codes to canonicals, JavaScript, Core Web Vitals, HTTPS and AI search readiness. Each check has a default severity, so you get a health score per area and for the site.',
            f'Every problem you find goes on the Issue Log, which scores it by severity, reach, traffic and effort, sets a deadline and turns it into a developer ticket on the Fix Plan. It ships with a worked demo for a fictional outdoor gear store ({len(ISSUES)} issues) so you can see every formula working.',
        ],
        [
            ('Audit Checks', f'{NCHK} checks with how to test, the pass rule and a default severity. Choose Pass, Warning, Fail, Not checked or Not applicable. Flags failures with no issue logged.'),
            ('Issue Log', 'One row per issue, 500 rows ready. Severity, reach and traffic factors, priority score, P1 to P4, deadline, days open and deadline status.'),
            ('Fix Plan', 'Developer tickets with acceptance criteria, week and validation method, plus a weekly capacity check.'),
            ('Dashboard', 'Health score and grade, 18 key numbers, top 10 open issues, health by area and issues by severity, with two charts.'),
            ('Settings', 'Audit date, priority rules, severity weights and deadlines, effort points, reach and traffic bands, owners and lists.'),
            ('AI Prompts', 'Prompts for ChatGPT, Claude or Gemini to read crawl exports, explain issues and write tickets.'),
            ('Checklist', 'The technical audit checklist as a tick list with automatic progress.'),
            ('Sources', 'Where facts come from and which numbers are assumptions.'),
        ],
        [
            'Look at the demo on Audit Checks, Issue Log, Fix Plan and the Dashboard. Then clear the demo results in columns G and H of Audit Checks, the yellow demo cells in columns B to O of the Issue Log (keep the Issue IDs) and the Fix Plan.',
            'On Settings, set the audit date, your owners and your weekly fix capacity. Check the severity weights and deadlines.',
            'Crawl your site and open Search Console (Page indexing, Crawl Stats, Core Web Vitals, Sitemaps). Work through every check and choose a result.',
            'For every Fail or Warning, add a row on the Issue Log: check ID, section, URLs affected, URLs in the section, impressions, effort and owner.',
            'Sort the Issue Log by Priority score. Put P1 and P2 issues on the Fix Plan with acceptance criteria and a validation method.',
            'Copy the ticket text into your tracker. Mark issues Validating when the fix ships and Fixed when validation passes.',
            'Repeat the audit every month or after every release, and compare the health score on the Dashboard.',
        ],
        url,
    )
    order = ['Start Here', 'Audit Checks', 'Issue Log', 'Fix Plan', 'Dashboard', 'Settings', 'AI Prompts', 'Checklist', 'Sources']
    wb._sheets = [wb[n] for n in order]
    wb.active = 0
    for ws in wb.worksheets:
        ws.sheet_properties.tabColor = K.GREEN if ws.title in order[:5] else 'A6EF39'
    wb.save(path)


PREVIEW = {'sheet': 'Issue Log', 'header_row': 4, 'rows': 12,
           'cols': [1, 2, len(IL_IN) + 1, 6, len(IL_IN) + 3, len(IL_IN) + 9, len(IL_IN) + 10, len(IL_IN) + 14],
           'formula_idx': [2, 4, 5, 6, 7]}


def check(wb):
    """Assert the worked examples used in the guide."""
    a = wb['Issue Log']
    v = lambda h, r: a[f'{IC[h]}{r}'].value
    r = 9   # ISS-005 colour variant canonicals
    assert a[f'A{r}'].value == 'ISS-005'
    assert v('Severity', r) == 'High' and v('Severity weight', r) == 6, v('Severity', r)
    assert abs(v('Share of section affected', r) - 212 / 1450) < 1e-9 and v('Reach factor', r) == 0.7 and v('Traffic factor', r) == 0.7
    assert v('Effort points', r) == 2 and v('Priority score (0 to 100)', r) == 21 and v('Priority', r) == 'P2: this sprint', v('Priority score (0 to 100)', r)
    assert v('Due date', r).date() == datetime.date(2026, 11, 26) and v('Deadline status', r) == 'Due soon' and v('Days open', r) == 11, v('Deadline status', r)
    exp = {5: (100, 'P1: fix now'), 6: (30, 'P1: fix now'), 7: (20, 'P2: this sprint'), 8: (13, 'P3: plan it'), 10: (42, 'P1: fix now'),
           11: (8, 'P3: plan it'), 12: (7, 'P3: plan it'), 13: (12, 'P3: plan it'), 15: (51, 'Validating'), 17: (10, 'P3: plan it'),
           18: (5, 'P4: backlog'), 19: (24, 'P2: this sprint')}
    for rr, (sc, pr) in exp.items():
        assert v('Priority score (0 to 100)', rr) == sc and v('Priority', rr) == pr, (rr, v('Priority score (0 to 100)', rr), v('Priority', rr))
    assert v('Deadline status', 7) == 'Overdue by 6 days', v('Deadline status', 7)
    assert v('Deadline status', 14) == 'Closed on time' and v('Deadline status', 16) == 'Closed late', (v('Deadline status', 14), v('Deadline status', 16))
    assert v('Severity', 19) == 'High' and v('Reach factor', 19) == 0.4
    ch = wb['Audit Checks']
    stat = {ch[f'A{r}'].value: ch[f'O{r}'].value for r in range(AC_FIRST, AC_FIRST + NCHK)}
    assert stat['TA24'] == 'Log an issue' and stat['TA06'] == 'Issue logged' and stat['TA59'] == 'OK' and stat['TA50'] == 'OK', stat
    assert stat['TA45'] == 'Not checked yet' and stat['TA56'] == 'Not applicable'
    dsh = wb['Dashboard']
    vals = {dsh.cell(row=r, column=1).value: dsh.cell(row=r, column=2).value for r in range(5, 23)}
    assert vals['Technical health score (0 to 100)'] == 78 and vals['Health grade'] == 'B', vals
    assert vals['Checks failed'] == 6 and vals['Checks with a warning'] == 8 and vals['Failed or warning checks with no issue logged'] == 1, vals
    assert vals['Open issues'] == 13 and vals['P1 issues to fix now'] == 3 and vals['Overdue issues'] == 1, vals
    assert dsh['D6'].value == 'ISS-001' and dsh['D7'].value == 'ISS-006', (dsh['D6'].value, dsh['D7'].value)
    fp = wb['Fix Plan']
    assert fp['M5'].value == 'Ready for development' and fp['M8'].value == 'Passed: mark the issue Fixed' and fp['M10'].value == 'Write the acceptance criteria', (fp['M8'].value, fp['M10'].value)
    assert fp['M13'].value == 'Choose how to validate' and fp['M14'].value == 'Schedule it in a week'
    assert fp['P6'].value == 4 and fp['P7'].value == 10 and fp['R7'].value == 'Over capacity by 2', (fp['P6'].value, fp['P7'].value, fp['R7'].value)
