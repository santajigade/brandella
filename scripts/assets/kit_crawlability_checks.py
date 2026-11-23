"""Crawlability Checks Kit workbook (asset 13).

URL Checker: one row per URL (500 rows). You say whether the page should be indexed and add what your crawler
and Search Console report: status code, blocked by robots.txt, noindex, canonical, in the sitemap, sitemap
lastmod, last real change, internal links in, click depth, main content in the raw HTML and the Page indexing
status. The checker works out the indexability, the canonical target health and the lastmod gap, runs 13
weighted checks (1 = pass, 0.5 = partly, 0 = fix, blank = not checked), gives a score, grade, fixes in priority
order and a verdict that names the conflict (blocked, noindex, not 200, canonical elsewhere, orphan, not indexed
by Google, noindex hidden by robots.txt, unwanted URL indexed, sitemap clean up).
Robots.txt Review: paste robots.txt line by line; it splits every line into field and value, tracks the user agent
group, says whether Google supports the field and flags whole site blocks, blocked CSS or JavaScript, relative
sitemap URLs, rules outside a group and the Googlebot group trap. Sitemap Files checks each sitemap file against
Google's limits. AI Bot Access compares your policy for each search and AI bot with what robots.txt really does.
Monitoring Plan schedules the recurring checks. Dashboard sums it all up.
"""
import datetime
from openpyxl.styles import PatternFill, Font, Alignment
from openpyxl.formatting.rule import CellIsRule, ColorScaleRule, FormulaRule
from openpyxl.chart import BarChart, Reference
from openpyxl.utils import get_column_letter as L
import kitlib as K

UC_FIRST, UC_LAST = 5, 504      # URL Checker
RT_FIRST, RT_LAST = 8, 157      # Robots.txt Review (150 lines)
SF_FIRST, SF_LAST = 5, 54       # Sitemap Files
BA_FIRST, BA_LAST = 5, 44       # AI Bot Access
MP_FIRST, MP_LAST = 5, 44       # Monitoring Plan
S = 'Settings'
UCS = "'URL Checker'"
RTS = "'Robots.txt Review'"
SFS = "'Sitemap Files'"
BAS = "'AI Bot Access'"
MPS = "'Monitoring Plan'"

(DATE, DPASS, DFIX, BUMP, RSIZE, SMURL, SMMB, SMREAD, MSOON, GA, GB, GC) = (f'{S}!$B${r}' for r in range(5, 17))
CHK_ROW = 21
PT = f'{S}!$F$6:$F$20'
NOIDX = f'{S}!$H$6:$H$9'
GSC_RNG = f'{S}!$J$6:$K$19'
RES_RNG = f'{S}!$M$6:$M$20'
SUPP = f'{S}!$O$6:$O$9'

PAGE_TYPES = ['Home', 'Product or feature', 'Pricing', 'Blog post', 'Docs page', 'Category or tag', 'Search or filter',
              'Account or app', 'Landing page', 'About or legal', 'Other']
NOINDEX = ['No', 'Meta robots', 'X-Robots-Tag', 'Both']
GSC = [('Indexed', 'Yes'), ('Crawled, not indexed', 'No'), ('Discovered, not indexed', 'No'),
       ('Duplicate, Google chose another canonical', 'No'), ('Duplicate without user canonical', 'No'),
       ('Alternate with proper canonical', 'No'), ('Page with redirect', 'No'), ('Not found (404)', 'No'), ('Soft 404', 'No'),
       ('Server error (5xx)', 'No'), ('Blocked by robots.txt', 'No'), ('Excluded by noindex', 'No'), ('Unknown to Google', 'No'),
       ('Not checked', '')]
RESOURCES = ['.css', '.js', '/assets/', '/static/', '/_next/', '/wp-includes/', '/wp-content/themes/', '/fonts/']
SUPPORTED = ['user-agent', 'allow', 'disallow', 'sitemap']
BOT_TYPES = ['Search', 'AI search', 'AI training', 'User requested fetch', 'Control token']
POLICY = ['Allow', 'Block', 'Allow some paths']
SMTYPES = ['Sitemap index', 'URL sitemap', 'Image sitemap', 'Video sitemap', 'News sitemap']
SMGSC = ['Success', 'Has errors', "Couldn't fetch", 'Not submitted']
RESULTS = ['OK', 'Issue found', 'Not done']

CHECKS = [
    ('Not blocked by robots.txt', 10, 'Pages you want indexed: robots.txt allows Googlebot = pass, blocked = fix.',
     'Remove or narrow the Disallow rule (test it with a robots.txt tester). A blocked page can still be indexed without its content, so it never shows properly.'),
    ('No noindex', 10, 'Pages you want indexed: no noindex in meta robots or the X-Robots-Tag header = pass.',
     'Remove the noindex from the template, plugin or server header, then request indexing in URL Inspection.'),
    ('Returns 200', 9, 'Pages you want indexed: status code 200 = pass. Anything else = fix.',
     'Fix server errors, restore deleted pages you still want, or link and list the final URL instead of a redirect.'),
    ('Canonical points to itself', 7, 'Pages you want indexed: canonical is the page itself = pass, missing = partly, another URL = fix.',
     'Add a self referencing canonical. Google recommends one on the canonical page itself.'),
    ('Canonical target is live', 6, 'Pages that canonicalise to another URL: the target returns 200, is not noindex and not blocked = pass. Target not in the list = partly.',
     'Point the canonical at the live, indexable version of the page.'),
    ('Noindex can be seen', 6, 'Pages with noindex: not blocked by robots.txt = pass. Blocked = fix, because Google cannot crawl the page to see the noindex.',
     'Unblock the page in robots.txt so Google can read the noindex, or remove the noindex if you want it indexed.'),
    ('Sitemap lists only indexable URLs', 5, 'In the sitemap: the URL is indexable = pass, not indexable = fix. A page you want indexed that is missing from the sitemap = partly.',
     'List only 200, indexable, canonical URLs. Remove redirects, 404s, noindex and canonicalised URLs.'),
    ('lastmod is accurate', 2, 'In the sitemap with dates: lastmod in the future or older than the last real change = fix. lastmod more than the allowed days after the real change = partly.',
     'Set lastmod to the date the main content really changed. Google uses lastmod only if it is consistently and verifiably accurate.'),
    ('Linked internally', 7, 'Pages you want indexed: at least 1 internal link in = pass, 0 = fix.',
     'Link the page from its hub and 2 or 3 related pages. Google finds most new pages through links.'),
    ('Shallow click depth', 4, 'Pages you want indexed: 3 clicks or less = pass, 4 = partly, 5 or more or not reachable = fix (editable).',
     'Link to the page from a hub, category or menu near the home page.'),
    ('Content in the raw HTML', 4, 'Pages you want indexed: main content in the initial HTML = pass, only after JavaScript = partly.',
     'Render the main content on the server. Google renders JavaScript, but many AI crawlers do not run it.'),
    ('Unwanted URL kept out', 5, 'Pages you do not want indexed: Google reports it indexed = fix; still crawlable and indexable = partly; kept out = pass.',
     'Add noindex (and keep it crawlable), canonicalise it to the main version, or remove it. Do not rely on robots.txt alone.'),
    ('Google has indexed it', 6, 'Pages you want indexed with a Page indexing status: Indexed = pass, any other status = fix.',
     'Use URL Inspection to see why. Improve the content, link to it, fix duplicates and request indexing.'),
]
NCH = len(CHECKS)

# Demo: BrightLedger, a fictional accounting software company (brightledger.example). Every URL and number is illustrative.
U = 'https://brightledger.example'
# url, type, want, status, redirects to, blocked, noindex, canonical, sitemap, lastmod, changed, links in, depth, raw html, gsc, impressions, notes
P = [
    ('/', 'Home', 'Yes', 200, '', 'No', 'No', '/', 'Yes', '2026-11-20', '2026-11-20', 180, 0, 'Yes', 'Indexed', 52000, ''),
    ('/pricing/', 'Pricing', 'Yes', 200, '', 'No', 'No', '/pricing/', 'Yes', '2026-11-02', '2026-11-02', 96, 1, 'Yes', 'Indexed', 18000, ''),
    ('/features/invoicing/', 'Product or feature', 'Yes', 200, '', 'No', 'No', '/features/invoicing/', 'Yes', '2026-10-15', '2026-11-12', 44, 1, 'Yes', 'Indexed', 9400, 'Page changed, lastmod did not'),
    ('/features/payroll/', 'Product or feature', 'Yes', 200, '', 'No', 'No', '/features/payroll/', 'Yes', '2026-11-21', '2026-09-30', 41, 1, 'Yes', 'Indexed', 6100, 'lastmod bumped by every deploy'),
    ('/features/expenses/', 'Product or feature', 'Yes', 200, '', 'No', 'No', '/features/expenses/', 'Yes', '2026-10-01', '2026-10-01', 22, 2, 'Yes', 'Duplicate, Google chose another canonical', 900, 'Near copy of /features/invoicing/'),
    ('/features/reports/', 'Product or feature', 'Yes', 503, '', 'No', 'No', '/features/reports/', 'Yes', '2026-11-05', '2026-11-05', 30, 2, 'Yes', 'Server error (5xx)', 3100, 'Times out under load'),
    ('/integrations/tally/', 'Landing page', 'Yes', 200, '', 'Yes', 'No', '/integrations/tally/', 'Yes', '2026-10-20', '2026-10-20', 12, 2, 'Yes', 'Blocked by robots.txt', 2300, 'Googlebot group blocks /integrations/'),
    ('/blog/', 'Category or tag', 'Yes', 200, '', 'No', 'No', '/blog/', 'Yes', '2026-11-18', '2026-11-18', 150, 1, 'Yes', 'Indexed', 4200, ''),
    ('/blog/gst-invoice-format/', 'Blog post', 'Yes', 200, '', 'No', 'No', '/blog/gst-invoice-format/', 'Yes', '2026-11-10', '2026-11-10', 14, 2, 'Yes', 'Indexed', 31000, ''),
    ('/blog/how-to-file-gst-returns/', 'Blog post', 'Yes', 200, '', 'No', 'No', '', 'Yes', '2026-09-12', '2026-09-12', 9, 2, 'Yes', 'Indexed', 12000, 'No canonical tag'),
    ('/blog/tds-rates-2026/', 'Blog post', 'Yes', 200, '', 'No', 'Meta robots', '/blog/tds-rates-2026/', 'Yes', '2026-11-18', '2026-11-18', 6, 2, 'Yes', 'Excluded by noindex', 0, 'Worked example: noindex left from the draft'),
    ('/blog/payroll-compliance-checklist/', 'Blog post', 'Yes', 200, '', 'No', 'No', '/blog/payroll-compliance-checklist/', 'No', '', '2026-11-05', 0, None, 'Yes', 'Discovered, not indexed', 0, 'Published without links or a sitemap entry'),
    ('/blog/invoice-vs-bill/', 'Blog post', 'Yes', 200, '', 'No', 'No', '/blog/invoice-vs-bill/', 'Yes', '2026-08-04', '2026-08-04', 1, 5, 'Yes', 'Indexed', 1400, 'Only linked from page 6 of the blog'),
    ('/docs/', 'Docs page', 'Yes', 200, '', 'No', 'No', '/docs/', 'Yes', '2026-11-15', '2026-11-15', 120, 1, 'No', 'Indexed', 7600, 'Docs are a JavaScript app'),
    ('/docs/api/authentication/', 'Docs page', 'Yes', 200, '', 'No', 'No', '/docs/api/authentication/', 'Yes', '2026-11-15', '2026-11-15', 8, 2, 'No', 'Crawled, not indexed', 0, ''),
    ('/docs/api/webhooks/', 'Docs page', 'Yes', 200, '', 'No', 'No', '/docs/api/webhooks', 'Yes', '2026-11-15', '2026-11-15', 8, 2, 'No', 'Alternate with proper canonical', 0, 'Canonical drops the trailing slash'),
    ('/docs/api/webhooks', 'Docs page', 'No', 301, '/docs/api/webhooks/', 'No', 'No', '', 'Yes', '2026-11-15', '2026-11-15', 3, 3, 'No', 'Page with redirect', 0, 'Old link format'),
    ('/old-pricing/', 'Pricing', 'No', 301, '/pricing/', 'No', 'No', '', 'Yes', '2025-04-01', '2025-04-01', 2, 3, 'Yes', 'Page with redirect', 0, 'Still in the pages sitemap'),
    ('/blog/old-gst-rates-2024/', 'Blog post', 'No', 404, '', 'No', 'No', '', 'Yes', '2024-07-01', '2024-07-01', 4, 3, 'Yes', 'Not found (404)', 0, 'Deleted, still in the blog sitemap'),
    ('/blog/tag/gst/', 'Category or tag', 'No', 200, '', 'No', 'Meta robots', '/blog/tag/gst/', 'No', '', '', 60, 2, 'Yes', 'Excluded by noindex', 0, 'Kept out on purpose'),
    ('/search?q=invoice', 'Search or filter', 'No', 200, '', 'No', 'No', '', 'No', '', '', 0, None, 'Yes', 'Indexed', 40, 'Googlebot group dropped the /search rule'),
    ('/features/invoicing/?sort=price', 'Search or filter', 'No', 200, '', 'No', 'No', '/features/invoicing/', 'No', '', '', 3, 2, 'Yes', 'Alternate with proper canonical', 0, ''),
    ('/app/dashboard/', 'Account or app', 'No', 302, '/login/', 'No', 'No', '', 'No', '', '', 2, 1, 'No', 'Page with redirect', 0, ''),
    ('/login/', 'Account or app', 'No', 200, '', 'No', 'Meta robots', '/login/', 'No', '', '', 180, 1, 'Yes', 'Excluded by noindex', 0, ''),
    ('/staging/new-homepage/', 'Other', 'No', 200, '', 'Yes', 'Meta robots', '/staging/new-homepage/', 'No', '', '', 1, 4, 'Yes', 'Blocked by robots.txt', 0, 'Blocked, so Google cannot see the noindex'),
    ('/about/', 'About or legal', 'Yes', 200, '', 'No', 'No', '/about/', 'Yes', '2026-06-10', '2026-06-10', 180, 1, 'Yes', 'Indexed', 900, ''),
    ('/contact/', 'About or legal', 'Yes', 200, '', 'No', 'No', '/contact/', 'Yes', '2026-06-10', '2026-06-10', 180, 1, 'Yes', 'Indexed', 600, ''),
]
ROBOTS = [
    '# BrightLedger robots.txt (demo)',
    'User-agent: *',
    'Disallow: /app/',
    'Disallow: /search',
    'Disallow: /*?sort=',
    'Disallow: /assets/js/',
    'Allow: /app/signup',
    'Crawl-delay: 5',
    '',
    'User-agent: Googlebot',
    'Noindex: /blog/tag/',
    'Disallow: /staging/',
    'Disallow: /integrations/',
    '',
    'User-agent: GPTBot',
    'User-agent: Google-Extended',
    'Disallow: /',
    '',
    'User-agent: PerplexityBot',
    'Disallow:',
    '',
    'Sitemap: https://brightledger.example/sitemap_index.xml',
    'Sitemap: /blog-sitemap.xml',
]
# url, type, status, urls, size MB, listed, submitted, gsc status, last read, discovered, notes
SITEMAPS = [
    ('/sitemap_index.xml', 'Sitemap index', 200, 4, 0.01, 'Yes', 'Yes', 'Success', '2026-11-21', None, 'Lists the 4 files below'),
    ('/sitemap-pages.xml', 'URL sitemap', 200, 140, 0.03, 'Yes', 'No', 'Not submitted', '2026-11-21', None, 'In the index'),
    ('/sitemap-blog.xml', 'URL sitemap', 200, 620, 0.15, 'Yes', 'No', 'Not submitted', '2026-11-20', None, 'In the index'),
    ('/sitemap-docs.xml', 'URL sitemap', 200, 52400, 11.2, 'Yes', 'Yes', 'Has errors', '2026-11-19', 50000, 'Docs generator puts every version in one file'),
    ('/blog-sitemap.xml', 'URL sitemap', 404, None, None, 'Yes', 'Yes', "Couldn't fetch", '2026-09-30', None, 'Old file, still named in robots.txt'),
    ('/sitemap-landing.xml', 'URL sitemap', 200, 38, 0.01, 'No', 'No', 'Not submitted', None, None, 'Made by the landing page tool, never linked'),
]
# token, company, type, what the vendor says, robots behaviour, policy, hits 30 days, error hits
BOTS = [
    ('Googlebot', 'Google', 'Search', 'Crawls for Google Search, including Discover and Search features. Blocking it removes you from Google Search and its AI features.', 'Google says its common crawlers always obey robots.txt rules when crawling automatically.', 'Allow', 18400, 0),
    ('Google-Extended', 'Google', 'Control token', 'Not a separate crawler: a robots.txt token that controls use for training future Gemini models and for grounding. Google says it does not affect inclusion or ranking in Google Search.', 'Control token read from robots.txt.', 'Block', None, None),
    ('GPTBot', 'OpenAI', 'AI training', 'OpenAI says disallowing GPTBot indicates content should not be used to train generative AI foundation models.', 'Controlled with robots.txt. OpenAI says changes take about 24 hours.', 'Block', 0, 0),
    ('OAI-SearchBot', 'OpenAI', 'AI search', 'OpenAI says sites opted out of OAI-SearchBot will not be shown in ChatGPT search answers.', 'Controlled with robots.txt.', 'Allow', 2100, 0),
    ('ChatGPT-User', 'OpenAI', 'User requested fetch', 'Visits pages when people ask ChatGPT to. Not used to crawl the web automatically.', 'OpenAI says robots.txt rules may not apply, because a user starts the visit.', 'Allow', 640, 0),
    ('ClaudeBot', 'Anthropic', 'AI training', 'Anthropic says it collects web content that could potentially contribute to training its models.', 'Anthropic says its bots honor robots.txt, including Crawl-delay.', 'Block', 3900, 0),
    ('Claude-SearchBot', 'Anthropic', 'AI search', 'Anthropic says it navigates the web to improve search result quality for users.', 'Anthropic says its bots honor robots.txt.', 'Allow', 520, 37),
    ('Claude-User', 'Anthropic', 'User requested fetch', 'Fetches pages when people ask Claude questions.', 'Anthropic says its bots honor robots.txt.', 'Allow', 210, 0),
    ('PerplexityBot', 'Perplexity', 'AI search', 'Perplexity says it surfaces and links websites in Perplexity search results and is not used to crawl content for AI foundation models.', 'Controlled with robots.txt. Perplexity says changes can take up to 24 hours.', 'Allow', 1300, 0),
    ('Perplexity-User', 'Perplexity', 'User requested fetch', 'Supports user actions in Perplexity. Not used for crawling or training.', 'Perplexity says it generally ignores robots.txt, because a user requested the fetch.', 'Block', 450, 0),
]
# task, where, every days, owner, last done, last result, notes
TASKS = [
    ('Compare robots.txt with last week\'s copy', 'robots.txt file; Search Console robots.txt report', 7, 'SEO', '2026-11-20', 'Issue found', 'Googlebot group added on 12 Nov'),
    ('Page indexing report: new reasons and spikes', 'Search Console, Pages', 7, 'SEO', '2026-11-18', 'Issue found', ''),
    ('Sitemaps report: status and discovered pages', 'Search Console, Sitemaps', 7, 'SEO', '2026-11-09', 'Issue found', ''),
    ('Crawl Stats: host status, response codes, response time', 'Search Console, Settings, Crawl stats', 30, 'Developer', '2026-10-15', 'OK', ''),
    ('Full crawl and refresh the URL Checker', 'Your crawler', 30, 'SEO', '2026-11-22', 'Issue found', ''),
    ('URL Inspection for new and updated key pages', 'Search Console, URL Inspection', 7, 'Content', '2026-11-21', 'OK', ''),
    ('Server or CDN logs for Googlebot and AI bots', 'Server or CDN logs', 30, 'Developer', '2026-10-01', 'OK', ''),
    ('CDN, firewall and bot protection rules', 'CDN or firewall dashboard', 30, 'Hosting or IT', None, '', 'Never reviewed'),
    ('AI bot documentation and new user agents', 'OpenAI, Anthropic, Perplexity and Google crawler pages', 90, 'SEO', '2026-09-01', 'OK', ''),
    ('JavaScript rendering spot check on each template', 'URL Inspection, View crawled page; view source', 90, 'Developer', '2026-10-10', 'Issue found', 'Docs app'),
    ('Canonical spot check on new templates', 'Crawler; URL Inspection', 30, 'SEO', '2026-11-01', 'OK', ''),
    ('Redirects and sitemap after content removals', 'Crawler; sitemap files', 30, 'Content', '2026-10-28', 'OK', ''),
]

IN_HEAD = ['URL', 'Page type', 'Should be indexed?', 'Status code', 'Redirects to', 'Blocked by robots.txt?', 'Noindex', 'Canonical URL',
           'In XML sitemap?', 'Sitemap lastmod', 'Last real content change', 'Internal links in', 'Click depth',
           'Main content in raw HTML?', 'Search Console status', 'Impressions (28 days)', 'Notes']
MEAS_HEAD = ['Parameter URL?', 'Canonical state', 'Canonical target status', 'Canonical target indexable?', 'Indexability',
             'lastmod gap (days)', 'Google says indexed?']
OUT_HEAD = ['Score (0 to 100)', 'Grade', 'Fixes needed', 'Fixes in priority order', 'Verdict']
NIN, NME = len(IN_HEAD), len(MEAS_HEAD)
C0 = NIN + NME + 1
CK = [L(C0 + i) for i in range(NCH)]
SC = C0 + NCH
HEAD = IN_HEAD + MEAS_HEAD + [c[0] for c in CHECKS] + OUT_HEAD
F_COLS = tuple(range(NIN + 1, len(HEAD) + 1))
M = {h: L(i + 1) for i, h in enumerate(HEAD)}
CKM = {c[0]: CK[i] for i, c in enumerate(CHECKS)}
VERDICTS = ['Fix now: blocked by robots.txt', 'Fix now: noindex on a page you want', 'Fix now: not returning 200',
            'Fix: canonical points elsewhere', 'Link it: orphan page', 'Investigate: Google has not indexed it',
            'Conflict: noindex hidden by robots.txt', 'Clean up: indexed but you do not want it', 'Clean up: remove from the sitemap',
            'Fix: canonical target not live', 'Decide: still open to indexing', 'Healthy', 'Improve when you can', 'OK: kept out as planned']


def uc(c):
    return f'{UCS}!${c}${UC_FIRST}:${c}${UC_LAST}'


def rt(c):
    return f'{RTS}!${c}${RT_FIRST}:${c}${RT_LAST}'


def d(s):
    return datetime.date.fromisoformat(s) if s else None


def settings_sheet(wb):
    ws = wb.create_sheet(S)
    ws.sheet_view.showGridLines = False
    K.title_block(ws, 'Settings', 'Every threshold, weight and list used by this workbook. Change a blue value and every check updates.')
    for c, w in zip('ABCDEFGHIJKLMNOPQRSTU', [54, 14, 62, 58, 3, 20, 3, 14, 3, 36, 12, 3, 20, 3, 14, 3, 20, 14, 16, 14, 14]):
        ws.column_dimensions[c].width = w
    rows = [
        (4, 'RULES', None, None),
        (5, 'Audit date (set it to the day you crawl)', datetime.date(2026, 11, 23), 'dd mmm yyyy'),
        (6, 'Click depth passes at or below', 3, '0'),
        (7, 'Click depth fails at or above', 5, '0'),
        (8, 'lastmod may be later than the real change by up to (days)', 7, '0'),
        (9, 'robots.txt size limit (bytes, Google: 500 KiB)', 512000, '#,##0'),
        (10, 'Sitemap file limit: URLs (Google: 50,000)', 50000, '#,##0'),
        (11, 'Sitemap file limit: MB uncompressed (Google: 50 MB)', 50, '0'),
        (12, 'Warn when Google last read a sitemap more than this many days ago', 14, '0'),
        (13, 'Monitoring: due soon within (days)', 3, '0'),
        (14, 'Grade A when the score is at least', 85, '0'),
        (15, 'Grade B when at least', 70, '0'),
        (16, 'Grade C when at least (below = D)', 55, '0'),
    ]
    for r, label, val, fmt in rows:
        a = ws.cell(row=r, column=1, value=label)
        a.font = K.f(10, val is None, K.DEEP if val is None else K.INK)
        if val is not None:
            c = ws.cell(row=r, column=2, value=val)
            c.border, c.fill = K.BORDER, K.INPUT_FILL
            c.font = K.f(10, True, '0000FF')
            c.number_format = fmt
    ws['C5'] = ('The robots.txt and sitemap limits come from Google documentation. The click depth rule, the 7 day lastmod allowance, the 14 day '
                'sitemap warning, the check weights and the grade bands are assumptions of this kit for you to tune.')
    ws['C5'].font = K.f(9, False, '777777', True)
    ws['C5'].alignment = Alignment(wrap_text=True, vertical='top')
    ws.merge_cells('C5:D9')
    ws.cell(row=CHK_ROW - 2, column=1, value='THE 13 URL CHECKS (weights are editable; any numbers, they are scaled)').font = K.f(10, True, K.DEEP)
    K.header_row(ws, CHK_ROW - 1, ['Check', 'Weight', 'Rule in the workbook', 'How to fix'])
    for i, (name, w, rule, fix) in enumerate(CHECKS):
        r = CHK_ROW + i
        for col, v in enumerate([name, w, rule, fix], 1):
            c = ws.cell(row=r, column=col, value=v)
            c.border = K.BORDER
            c.font = K.f(10, col == 1, '0000FF' if col == 2 else K.INK)
            c.alignment = Alignment(wrap_text=True, vertical='top')
        ws.cell(row=r, column=2).fill = K.INPUT_FILL
        ws.row_dimensions[r].height = 44
    tr = CHK_ROW + NCH
    ws.cell(row=tr, column=1, value='Total weight (auto)').font = K.f(10, True)
    ws.cell(row=tr, column=2, value=f'=SUM(B{CHK_ROW}:B{tr - 1})').fill = K.FORMULA_FILL

    def lst(col, title, head, vals, n, row=4):
        ws[f'{col}{row}'] = title
        ws[f'{col}{row}'].font = K.f(10, True, K.DEEP)
        ws[f'{col}{row + 1}'] = head
        ws[f'{col}{row + 1}'].font = K.f(9, True, '555555')
        for i in range(n):
            c = ws[f'{col}{row + 2 + i}']
            c.value = vals[i] if i < len(vals) else None
            c.fill, c.border, c.font = K.INPUT_FILL, K.BORDER, K.f(10)
    lst('F', 'PAGE TYPES', 'Page type', PAGE_TYPES, 15)
    lst('H', 'NOINDEX', 'Where', NOINDEX, 4)
    ws['J4'] = 'SEARCH CONSOLE STATUS'
    ws['J4'].font = K.f(10, True, K.DEEP)
    ws['J5'], ws['K5'] = 'Status (closest Page indexing reason)', 'Counts as indexed?'
    for c in ('J5', 'K5'):
        ws[c].font = K.f(9, True, '555555')
    for i, (s, v) in enumerate(GSC):
        for col, val in (('J', s), ('K', v)):
            c = ws[f'{col}{6 + i}']
            c.value = val if val != '' else None
            c.fill, c.border, c.font = K.INPUT_FILL, K.BORDER, K.f(10)
    lst('M', 'FILES ROBOTS.TXT SHOULD NOT BLOCK', 'Path contains', RESOURCES, 15)
    lst('O', 'FIELDS GOOGLE SUPPORTS', 'Field', SUPPORTED, 4)
    lst('Q', 'BOT TYPES', 'Type', BOT_TYPES, 5)
    lists = [('R', 'Policy', POLICY), ('S', 'Sitemap type', SMTYPES), ('T', 'Sitemap status', SMGSC), ('U', 'Task result', RESULTS)]
    for col, head, vals in lists:
        ws[f'{col}5'] = head
        ws[f'{col}5'].font = K.f(9, True, '555555')
        for i, v in enumerate(vals):
            ws[f'{col}{6 + i}'] = v
            ws[f'{col}{6 + i}'].font = K.f(9)
    ws['R4'] = 'LISTS'
    ws['R4'].font = K.f(10, True, K.DEEP)
    ws['O12'] = 'Yes/No'
    ws['O12'].font = K.f(9, True, '555555')
    ws['O13'], ws['O14'] = 'Yes', 'No'
    return ws


def checker_sheet(wb):
    ws = wb.create_sheet('URL Checker')
    ws.sheet_view.showGridLines = False
    K.title_block(ws, 'URL checker', f'Rows 5 to {4 + len(P)} hold DEMO data for BrightLedger, a fictional accounting software company (illustrative URLs and numbers). Select the yellow demo cells and press Delete to start your own. Grey formula columns stay.')
    ws['A2'].font = K.f(10, True, 'B45309')
    ws['A3'] = 'One row per URL: your important pages plus the URLs you want kept out (filters, search, tags, redirects, staging). Say if each should be indexed, then add crawler and Search Console facts. 500 rows ready.'
    ws['A3'].font = K.f(9, False, '666666', True)
    widths = ([46, 16, 9, 8, 30, 9, 11, 34, 9, 11, 11, 8, 7, 10, 26, 10, 30] + [8, 10, 9, 9, 22, 8, 9] + [9] * NCH + [9, 7, 7, 52, 36])
    K.header_row(ws, 4, HEAD, formula_cols=F_COLS, widths=widths)
    for i, col in enumerate(CK):
        c = ws[f'{col}3']
        c.value = f'={S}!$B${CHK_ROW + i}'
        c.font, c.fill, c.alignment = K.f(9, True, K.DEEP), K.SOFT, Alignment(horizontal='center')
    ws[f'{CK[0]}2'] = 'Check weights (from Settings)'
    ws[f'{CK[0]}2'].font = K.f(9, True, K.DEEP)
    m = M
    tbl = f'$A${UC_FIRST}:$G${UC_LAST}'
    for r in range(UC_FIRST, UC_LAST + 1):
        i = r - UC_FIRST
        if i < len(P):
            row = list(P[i])
            row[0] = U + row[0]
            if row[4]:
                row[4] = U + row[4]
            if row[7]:
                row[7] = U + row[7]
            row[9], row[10] = d(row[9]), d(row[10])
            for col, v in enumerate(row, 1):
                if v not in (None, ''):
                    ws.cell(row=r, column=col, value=v)
        e = f'A{r}=""'
        g = lambda h: f'{m[h]}{r}'
        f = {}
        f['Parameter URL?'] = f'=IF({e},"",IF(ISNUMBER(FIND("?",A{r})),"Yes","No"))'
        f['Canonical state'] = f'=IF({e},"",IF(TRIM(H{r})="","Missing",IF(TRIM(H{r})=A{r},"Self","Other URL")))'
        cs = g('Canonical state')
        f['Canonical target status'] = f'=IF(OR({e},{cs}<>"Other URL"),"",IFERROR(VLOOKUP(TRIM(H{r}),{tbl},4,FALSE),"Not in list"))'
        cts = g('Canonical target status')
        f['Canonical target indexable?'] = (f'=IF(OR({e},{cs}<>"Other URL"),"",IF({cts}="Not in list","Unknown",IF(AND(N({cts})=200,'
                                            f'IFERROR(VLOOKUP(TRIM(H{r}),{tbl},7,FALSE),"No")="No",IFERROR(VLOOKUP(TRIM(H{r}),{tbl},6,FALSE),"No")<>"Yes"),"Yes","No")))')
        noi = f'OR(G{r}="Meta robots",G{r}="X-Robots-Tag",G{r}="Both")'
        f['Indexability'] = (f'=IF({e},"",IF(F{r}="Yes","Blocked by robots.txt",IF(N(D{r})=0,"No status yet",IF(D{r}>=500,"Server error",'
                             f'IF(D{r}>=400,"Not found or error",IF(D{r}>=300,"Redirect",IF({noi},"Noindex",IF({cs}="Other URL","Canonicalised to another URL","Indexable"))))))))')
        f['lastmod gap (days)'] = f'=IF(OR({e},J{r}="",K{r}=""),"",J{r}-K{r})'
        f['Google says indexed?'] = f'=IF(OR({e},O{r}="",O{r}="Not checked"),"",IFERROR(""&VLOOKUP(O{r},{GSC_RNG},2,FALSE),""))'
        idx, gap, gsi = g('Indexability'), g('lastmod gap (days)'), g('Google says indexed?')
        want, nowant = f'C{r}="Yes"', f'C{r}="No"'
        t = {}
        t['Not blocked by robots.txt'] = f'=IF(OR({e},NOT({want}),F{r}=""),"",IF(F{r}="Yes",0,1))'
        t['No noindex'] = f'=IF(OR({e},NOT({want}),G{r}=""),"",IF({noi},0,1))'
        t['Returns 200'] = f'=IF(OR({e},NOT({want}),N(D{r})=0),"",IF(D{r}=200,1,0))'
        t['Canonical points to itself'] = f'=IF(OR({e},NOT({want})),"",IF({cs}="Self",1,IF({cs}="Missing",0.5,0)))'
        t['Canonical target is live'] = f'=IF(OR({e},{cs}<>"Other URL"),"",IF({g("Canonical target indexable?")}="Yes",1,IF({g("Canonical target indexable?")}="Unknown",0.5,0)))'
        t['Noindex can be seen'] = f'=IF(OR({e},NOT({noi})),"",IF(F{r}="Yes",0,1))'
        t['Sitemap lists only indexable URLs'] = f'=IF(OR({e},I{r}=""),"",IF(I{r}="Yes",IF({idx}="Indexable",1,0),IF({want},0.5,"")))'
        t['lastmod is accurate'] = (f'=IF(OR({e},I{r}<>"Yes",J{r}=""),"",IF(J{r}>{DATE},0,IF({gap}="","",IF({gap}<0,0,IF({gap}>{BUMP},0.5,1)))))')
        t['Linked internally'] = f'=IF(OR({e},NOT({want})),"",IF(N(L{r})>=1,1,0))'
        t['Shallow click depth'] = f'=IF(OR({e},NOT({want})),"",IF(M{r}="",0,IF(M{r}<={DPASS},1,IF(M{r}>={DFIX},0,0.5))))'
        t['Content in the raw HTML'] = f'=IF(OR({e},NOT({want}),N{r}=""),"",IF(N{r}="Yes",1,0.5))'
        t['Unwanted URL kept out'] = f'=IF(OR({e},NOT({nowant})),"",IF({gsi}="Yes",0,IF({idx}="Indexable",0.5,1)))'
        t['Google has indexed it'] = f'=IF(OR({e},NOT({want}),{gsi}=""),"",IF({gsi}="Yes",1,0))'
        for h, v in list(f.items()) + list(t.items()):
            ws[f'{m[h]}{r}'] = v
        rng = f'{CK[0]}{r}:{CK[-1]}{r}'
        w = f'${CK[0]}$3:${CK[-1]}$3'
        sc = m['Score (0 to 100)']
        ws[f'{sc}{r}'] = f'=IF({e},"",IFERROR(ROUND(100*SUMPRODUCT({w},{rng})/SUMPRODUCT({w}*ISNUMBER({rng})),0),""))'
        ws[g('Grade')] = f'=IF(OR({e},{sc}{r}=""),"",IF({sc}{r}>={GA},"A",IF({sc}{r}>={GB},"B",IF({sc}{r}>={GC},"C","D"))))'
        ws[g('Fixes needed')] = f'=IF({e},"",COUNTIF({rng},0)+COUNTIF({rng},0.5))'
        parts = ','.join(f'IF({c}{r}=0,{c}$4,IF({c}{r}=0.5,{c}$4&" (partly)",""))' for c in CK)
        ws[g('Fixes in priority order')] = f'=IF({e},"",_xlfn.TEXTJOIN("; ",TRUE,{parts}))'
        k = lambda name: f'{CKM[name]}{r}'
        z = lambda name: f'AND(ISNUMBER({k(name)}),{k(name)}=0)'
        ws[g('Verdict')] = (
            f'=IF({e},"",IF(C{r}="","Choose Should be indexed?",IF({want},'
            f'IF({z("Not blocked by robots.txt")},"Fix now: blocked by robots.txt",IF({z("No noindex")},"Fix now: noindex on a page you want",'
            f'IF({z("Returns 200")},"Fix now: not returning 200",IF({z("Canonical points to itself")},"Fix: canonical points elsewhere",'
            f'IF({z("Linked internally")},"Link it: orphan page",IF({z("Google has indexed it")},"Investigate: Google has not indexed it",'
            f'IF(N({sc}{r})>={GA},"Healthy","Improve when you can"))))))),'
            f'IF({z("Noindex can be seen")},"Conflict: noindex hidden by robots.txt",IF({z("Unwanted URL kept out")},"Clean up: indexed but you do not want it",'
            f'IF({z("Sitemap lists only indexable URLs")},"Clean up: remove from the sitemap",IF({z("Canonical target is live")},"Fix: canonical target not live",'
            f'IF(AND(ISNUMBER({k("Unwanted URL kept out")}),{k("Unwanted URL kept out")}=0.5),"Decide: still open to indexing","OK: kept out as planned"))))))))')
    nf = {4: '0', 10: 'dd mmm yyyy', 11: 'dd mmm yyyy', 16: '#,##0', SC: '0'}
    K.style_body(ws, UC_FIRST, UC_LAST, len(HEAD), formula_cols=F_COLS, number_formats=nf, wrap_cols=(17, SC + 3, SC + 4))
    ws.freeze_panes = 'B5'
    ws.auto_filter.ref = f'A4:{L(len(HEAD))}{UC_LAST}'
    yn = f'{S}!$O$13:$O$14'
    K.dropdown(ws, f'B{UC_FIRST}:B{UC_LAST}', PT)
    for col in 'CFIN':
        K.dropdown(ws, f'{col}{UC_FIRST}:{col}{UC_LAST}', yn)
    K.dropdown(ws, f'G{UC_FIRST}:G{UC_LAST}', NOIDX, 'No, Meta robots, X-Robots-Tag or Both')
    K.dropdown(ws, f'O{UC_FIRST}:O{UC_LAST}', f'{S}!$J$6:$J$19', 'Pick the closest reason from the Page indexing report or URL Inspection.')
    K.whole_number(ws, f'D{UC_FIRST}:D{UC_LAST}', 100, 599, 'HTTP status code, for example 200, 301, 404 or 503.')
    K.whole_number(ws, f'M{UC_FIRST}:M{UC_LAST}', 0, 50, 'Clicks from the home page (0 = home). Leave blank if the crawler cannot reach the page.')
    chk = f'{CK[0]}{UC_FIRST}:{CK[-1]}{UC_LAST}'
    ws.conditional_formatting.add(chk, CellIsRule(operator='equal', formula=['1'], fill=PatternFill('solid', fgColor='D9F2C4')))
    ws.conditional_formatting.add(chk, CellIsRule(operator='equal', formula=['0.5'], fill=PatternFill('solid', fgColor='FFF4CC')))
    ws.conditional_formatting.add(chk, FormulaRule(formula=[f'AND(ISNUMBER({CK[0]}{UC_FIRST}),{CK[0]}{UC_FIRST}=0)'], fill=PatternFill('solid', fgColor='F8D7D3'), font=Font(name=K.FONT, bold=True, color='9B2C1F')))
    scol = L(SC)
    ws.conditional_formatting.add(f'{scol}{UC_FIRST}:{scol}{UC_LAST}', ColorScaleRule(start_type='num', start_value=30, start_color='F8D7D3', mid_type='num', mid_value=70, mid_color='FFF4CC', end_type='num', end_value=100, end_color='B7E4A0'))
    gcol = f'{L(SC + 1)}{UC_FIRST}:{L(SC + 1)}{UC_LAST}'
    for val, col in (('A', '9BE07A'), ('B', 'D9F2C4'), ('C', 'FFF4CC'), ('D', 'F8D7D3')):
        ws.conditional_formatting.add(gcol, CellIsRule(operator='equal', formula=[f'"{val}"'], fill=PatternFill('solid', fgColor=col), font=Font(name=K.FONT, bold=True)))
    vc = L(SC + 4)
    vr = f'{vc}{UC_FIRST}:{vc}{UC_LAST}'
    for start, n, fill, fc in (('Fix now', 7, '9B2C1F', 'FFFFFF'), ('Conflict', 8, '9B2C1F', 'FFFFFF'), ('Fix:', 4, 'F8D7D3', '9B2C1F'), ('Clean up', 8, 'FCE4D6', '9B2C1F'),
                               ('Link it', 7, 'FCE4D6', '9B2C1F'), ('Investigate', 11, 'FFF4CC', '1F1F1F'), ('Decide', 6, 'FFF4CC', '1F1F1F'), ('Healthy', 7, 'D9F2C4', '1F1F1F'), ('OK:', 3, 'D9F2C4', '1F1F1F')):
        ws.conditional_formatting.add(vr, FormulaRule(formula=[f'LEFT({vc}{UC_FIRST},{n})="{start}"'], fill=PatternFill('solid', fgColor=fill), font=Font(name=K.FONT, bold=True, color=fc)))
    ix = m['Indexability']
    ws.conditional_formatting.add(f'{ix}{UC_FIRST}:{ix}{UC_LAST}', FormulaRule(formula=[f'AND({ix}{UC_FIRST}<>"",{ix}{UC_FIRST}<>"Indexable")'], font=Font(name=K.FONT, bold=True, color='9B2C1F')))
    return ws


def robots_sheet(wb):
    ws = wb.create_sheet('Robots.txt Review')
    ws.sheet_view.showGridLines = False
    K.title_block(ws, 'Robots.txt review', 'Paste your robots.txt into column A, one line per row (blank lines and comments are fine). Rows below hold the DEMO file for BrightLedger. 150 rows ready.')
    ws['A2'].font = K.f(10, True, 'B45309')
    ws['A3'] = 'Google obeys only one group per crawler: the most specific user agent that matches. User agent groups and the * group are not combined, so a Googlebot group must repeat every rule Googlebot needs.'
    ws['A3'].font = K.f(9, False, '666666', True)
    ws['A4'], ws['A5'] = 'robots.txt URL', 'File size in bytes (from your browser or server)'
    ws['B4'], ws['B5'] = f'{U}/robots.txt', 642
    for c in ('A4', 'A5'):
        ws[c].font = K.f(10, True)
    for c in ('B4', 'B5'):
        ws[c].fill, ws[c].border, ws[c].font = K.INPUT_FILL, K.BORDER, K.f(10)
    ws['C5'] = f'=IF(B5="","Add the file size",IF(B5>{RSIZE},"Over the limit: Google ignores everything after 500 KiB","Under the 500 KiB limit"))'
    ws['C5'].fill, ws['C5'].font = K.FORMULA_FILL, K.f(10, True)
    head = ['robots.txt line (paste)', 'Line', 'Line without comment', 'Field', 'Value', 'Group (user agents)', 'Last field (helper)',
            'Google supports it?', 'Flags', 'Severity']
    K.header_row(ws, 7, head, formula_cols=tuple(range(2, 11)), widths=[46, 6, 34, 12, 40, 26, 8, 34, 64, 10])
    D_, E_, F_ = rt('D'), rt('E'), rt('F')
    for r in range(RT_FIRST, RT_LAST + 1):
        i = r - RT_FIRST
        if i < len(ROBOTS) and ROBOTS[i]:
            ws.cell(row=r, column=1, value=ROBOTS[i])
        first = r == RT_FIRST
        ws[f'B{r}'] = f'=IF(A{r}="","",ROW()-{RT_FIRST - 1})'
        ws[f'C{r}'] = f'=IF(TRIM(A{r})="","",TRIM(IF(ISNUMBER(FIND("#",A{r})),LEFT(A{r},FIND("#",A{r})-1),A{r})))'
        ws[f'D{r}'] = f'=IF(C{r}="","",IF(ISNUMBER(FIND(":",C{r})),LOWER(TRIM(LEFT(C{r},FIND(":",C{r})-1))),"(no colon)"))'
        ws[f'E{r}'] = f'=IF(OR(C{r}="",NOT(ISNUMBER(FIND(":",C{r})))),"",TRIM(MID(C{r},FIND(":",C{r})+1,2000)))'
        if first:
            ws[f'G{r}'] = f'=IF(D{r}<>"",D{r},"")'
            ws[f'F{r}'] = f'=IF(D{r}="user-agent",E{r},"")'
        else:
            ws[f'G{r}'] = f'=IF(D{r}<>"",D{r},G{r - 1})'
            ws[f'F{r}'] = f'=IF(D{r}="user-agent",IF(G{r - 1}="user-agent",F{r - 1}&", "&E{r},E{r}),F{r - 1})'
        ws[f'H{r}'] = (f'=IF(D{r}="","",IF(COUNTIF({SUPP},D{r})>0,"Yes",IF(D{r}="crawl-delay","No: Google ignores crawl-delay",'
                       f'IF(D{r}="noindex","No: noindex is not a robots.txt rule","No: unknown field, ignored"))))')
        rule = f'OR(D{r}="allow",D{r}="disallow")'
        res = f'SUMPRODUCT(({S}!$M$6:$M$20<>"")*ISNUMBER(SEARCH({S}!$M$6:$M$20,E{r})))>0'
        star = f'OR(F{r}="*",LEFT(F{r},2)="*,",ISNUMBER(SEARCH(", ~*",F{r})))'
        flags = (f'_xlfn.TEXTJOIN("; ",TRUE,'
                 f'IF(AND(D{r}="disallow",E{r}="/"),IF(OR({star},ISNUMBER(SEARCH("googlebot",F{r}))),"blocks the whole site for "&F{r},"blocks these bots completely: check your AI bot policy"),""),'
                 f'IF(AND(D{r}="disallow",E{r}<>"",{res}),"may block CSS, JavaScript or fonts needed to render pages",""),'
                 f'IF(AND({rule},E{r}<>"",LEFT(E{r},1)<>"/",LEFT(E{r},1)<>"*"),"path should start with / or *",""),'
                 f'IF(AND({rule},F{r}=""),"rule before any user-agent line",""),'
                 f'IF(AND(D{r}="sitemap",LEFT(LOWER(E{r}),4)<>"http"),"sitemap URL must be absolute (https://...)",""),'
                 f'IF(AND(D{r}="user-agent",LOWER(E{r})="googlebot",COUNTIFS({D_},"user-agent",{E_},"~*")>0),"Googlebot group: Googlebot now ignores every * rule, so repeat the ones it needs",""),'
                 f'IF(AND(D{r}="disallow",E{r}=""),"empty disallow: this group may crawl everything",""),'
                 f'IF(AND(D{r}="user-agent",E{r}<>"*",COUNTIF({BAS}!$A${BA_FIRST}:$A${BA_LAST},E{r})>0),"names a search or AI bot: see AI Bot Access",""))')
        ws[f'I{r}'] = f'=IF(D{r}="","",{flags})'
        ws[f'J{r}'] = (f'=IF(D{r}="","",IF(OR(ISNUMBER(SEARCH("whole site",I{r})),ISNUMBER(SEARCH("Googlebot group",I{r}))),"High",'
                       f'IF(OR(ISNUMBER(SEARCH("CSS",I{r})),ISNUMBER(SEARCH("absolute",I{r})),ISNUMBER(SEARCH("should start",I{r})),ISNUMBER(SEARCH("before any",I{r}))),"Medium",'
                       f'IF(H{r}<>"Yes","Low",IF(I{r}<>"","Info","OK")))))')
    K.style_body(ws, RT_FIRST, RT_LAST, len(head), formula_cols=tuple(range(2, 11)), wrap_cols=(9,))
    ws.column_dimensions['G'].hidden = True
    jr = f'J{RT_FIRST}:J{RT_LAST}'
    for val, fill, fc in (('High', '9B2C1F', 'FFFFFF'), ('Medium', 'F8D7D3', '9B2C1F'), ('Low', 'FFF4CC', '1F1F1F'), ('Info', 'EEF8E6', '3D7F12'), ('OK', 'D9F2C4', '1F1F1F')):
        ws.conditional_formatting.add(jr, CellIsRule(operator='equal', formula=[f'"{val}"'], fill=PatternFill('solid', fgColor=fill), font=Font(name=K.FONT, bold=True, color=fc)))
    ws.conditional_formatting.add(f'H{RT_FIRST}:H{RT_LAST}', FormulaRule(formula=[f'LEFT(H{RT_FIRST},2)="No"'], font=Font(name=K.FONT, bold=True, color='B45309')))
    ws.freeze_panes = 'B8'
    return ws


def sitemaps_sheet(wb):
    ws = wb.create_sheet('Sitemap Files')
    ws.sheet_view.showGridLines = False
    K.title_block(ws, 'Sitemap files', 'One row per sitemap file. Rows below hold DEMO files for BrightLedger. Add status, URL count and size from the file, and status and last read from the Search Console Sitemaps report.')
    ws['A2'].font = K.f(10, True, 'B45309')
    ws['A3'] = 'Google limits each sitemap to 50,000 URLs or 50 MB uncompressed and says to use absolute URLs. The URL Checker tells you which listed URLs are not indexable.'
    ws['A3'].font = K.f(9, False, '666666', True)
    head = ['Sitemap URL', 'Type', 'Status code', 'URLs listed', 'Size (MB, uncompressed)', 'Listed in robots.txt or an index?',
            'Submitted in Search Console?', 'Search Console status', 'Last read by Google', 'Discovered pages (Search Console)', 'Notes',
            'Absolute URL?', 'Within URL limit?', 'Within size limit?', 'Days since Google read it', 'Issues', 'Verdict']
    fc = tuple(range(12, 18))
    K.header_row(ws, 4, head, formula_cols=fc, widths=[42, 14, 8, 10, 10, 12, 12, 16, 12, 12, 34, 9, 9, 9, 9, 50, 40])
    for r in range(SF_FIRST, SF_LAST + 1):
        i = r - SF_FIRST
        if i < len(SITEMAPS):
            row = list(SITEMAPS[i])
            row[0] = U + row[0]
            row[8] = d(row[8])
            for col, v in enumerate(row, 1):
                if v not in (None, ''):
                    ws.cell(row=r, column=col, value=v)
        e = f'A{r}=""'
        ws[f'L{r}'] = f'=IF({e},"",IF(LEFT(LOWER(A{r}),4)="http","Yes","No"))'
        ws[f'M{r}'] = f'=IF(OR({e},D{r}=""),"",IF(D{r}<={SMURL},"Yes","No"))'
        ws[f'N{r}'] = f'=IF(OR({e},E{r}=""),"",IF(E{r}<={SMMB},"Yes","No"))'
        ws[f'O{r}'] = f'=IF(OR({e},I{r}=""),"",{DATE}-I{r})'
        iss = (f'_xlfn.TEXTJOIN("; ",TRUE,IF(AND(C{r}<>"",N(C{r})<>200),"returns "&C{r},""),IF(L{r}="No","not an absolute URL",""),'
               f'IF(M{r}="No","over "&TEXT({SMURL},"#,##0")&" URLs",""),IF(N{r}="No","over "&{SMMB}&" MB",""),'
               f'IF(OR(H{r}="Has errors",H{r}="Couldn\'t fetch"),"Search Console: "&H{r},""),'
               f'IF(AND(F{r}="No",G{r}<>"Yes"),"Google may never find it",""),IF(AND(O{r}<>"",N(O{r})>{SMREAD}),"not read for "&O{r}&" days",""))')
        ws[f'P{r}'] = f'=IF({e},"",IF({iss}="","OK",{iss}))'
        ws[f'Q{r}'] = (f'=IF({e},"",IF(AND(C{r}<>"",N(C{r})<>200),"Fix now: file not reachable (remove it from robots.txt and Search Console if it is gone)",'
                       f'IF(OR(M{r}="No",N{r}="No"),"Split it and list the parts in a sitemap index",IF(OR(H{r}="Has errors",H{r}="Couldn\'t fetch"),"Open the Sitemaps report and fix the errors",'
                       f'IF(AND(F{r}="No",G{r}<>"Yes"),"Add it to robots.txt, a sitemap index or Search Console",IF(AND(O{r}<>"",N(O{r})>{SMREAD}),"Check why Google stopped reading it","OK"))))))')
    K.style_body(ws, SF_FIRST, SF_LAST, len(head), formula_cols=fc, number_formats={4: '#,##0', 5: '0.00', 9: 'dd mmm yyyy', 10: '#,##0'}, wrap_cols=(11, 16, 17))
    yn = f'{S}!$O$13:$O$14'
    K.dropdown(ws, f'B{SF_FIRST}:B{SF_LAST}', f'{S}!$S$6:$S$10')
    K.dropdown(ws, f'F{SF_FIRST}:F{SF_LAST}', yn)
    K.dropdown(ws, f'G{SF_FIRST}:G{SF_LAST}', yn)
    K.dropdown(ws, f'H{SF_FIRST}:H{SF_LAST}', f'{S}!$T$6:$T$9')
    q = f'Q{SF_FIRST}:Q{SF_LAST}'
    ws.conditional_formatting.add(q, CellIsRule(operator='equal', formula=['"OK"'], fill=PatternFill('solid', fgColor='D9F2C4')))
    ws.conditional_formatting.add(q, FormulaRule(formula=[f'LEFT(Q{SF_FIRST},7)="Fix now"'], fill=PatternFill('solid', fgColor='9B2C1F'), font=Font(name=K.FONT, bold=True, color='FFFFFF')))
    ws.conditional_formatting.add(q, FormulaRule(formula=[f'AND(Q{SF_FIRST}<>"",Q{SF_FIRST}<>"OK",LEFT(Q{SF_FIRST},7)<>"Fix now")'], fill=PatternFill('solid', fgColor='FFF4CC'), font=Font(name=K.FONT, bold=True)))
    ws.freeze_panes = 'B5'
    ws.auto_filter.ref = f'A4:Q{SF_LAST}'
    return ws


def bots_sheet(wb):
    ws = wb.create_sheet('AI Bot Access')
    ws.sheet_view.showGridLines = False
    K.title_block(ws, 'Search and AI bot access', 'Decide a policy for each bot, then see whether your robots.txt (Robots.txt Review tab) really does it. The bot facts come from each vendor\'s own crawler page (see Sources); check them again every quarter.')
    ws['A3'] = 'Training bots, AI search bots and user requested fetchers are different. Blocking an AI search bot can remove you from that AI search; user requested fetchers may not follow robots.txt at all.'
    ws['A3'].font = K.f(9, False, '666666', True)
    head = ['Bot token (user agent)', 'Company', 'Type', 'What the vendor says', 'robots.txt behaviour (vendor)', 'Your policy',
            'Hits in your logs (30 days)', 'Hits with 403 or 5xx', 'Named in your robots.txt?', 'Blocked from the whole site?', 'Verdict', 'Lines for robots.txt']
    fc = (9, 10, 11, 12)
    K.header_row(ws, 4, head, formula_cols=fc, widths=[18, 11, 16, 56, 40, 12, 10, 10, 14, 12, 46, 24])
    for r in range(BA_FIRST, BA_LAST + 1):
        i = r - BA_FIRST
        if i < len(BOTS):
            for col, v in enumerate(BOTS[i], 1):
                if v not in (None, ''):
                    ws.cell(row=r, column=col, value=v)
        e = f'A{r}=""'
        ws[f'I{r}'] = f'=IF({e},"",IF(COUNTIFS({rt("D")},"user-agent",{rt("E")},A{r})>0,"Own group","No: uses the * group"))'
        own = f'COUNTIFS({rt("D")},"disallow",{rt("E")},"/",{rt("F")},"*"&A{r}&"*")'
        allg = f'COUNTIFS({rt("D")},"disallow",{rt("E")},"/",{rt("F")},"~*")'
        ws[f'J{r}'] = f'=IF({e},"",IF(I{r}="Own group",IF({own}>0,"Yes","No"),IF({allg}>0,"Yes","No")))'
        ufetch = f'C{r}="User requested fetch"'
        ws[f'K{r}'] = (f'=IF({e},"",IF(F{r}="","Choose a policy",IF(F{r}="Allow some paths","Check the paths for this group on Robots.txt Review",'
                       f'IF(F{r}="Block",IF(J{r}="Yes",IF({ufetch},"Blocked, but this fetcher may ignore robots.txt: use server rules if you must","OK: blocked as planned"),'
                       f'IF({ufetch},"Not blocked, and robots.txt may not stop it: use server or firewall rules if you must","Mismatch: not blocked yet, add the lines on the right")),'
                       f'IF(J{r}="Yes","Mismatch: you block a bot you want",IF(N(H{r})>0,"Check: "&H{r}&" blocked or failed hits in your logs","OK: allowed as planned"))))))')
        ws[f'L{r}'] = f'=IF(OR({e},F{r}<>"Block",J{r}="Yes"),"","User-agent: "&A{r}&CHAR(10)&"Disallow: /")'
    K.style_body(ws, BA_FIRST, BA_LAST, len(head), formula_cols=fc, number_formats={7: '#,##0', 8: '#,##0'}, wrap_cols=(4, 5, 11, 12))
    for r in range(BA_FIRST, BA_FIRST + len(BOTS)):
        ws.row_dimensions[r].height = 58
    K.dropdown(ws, f'C{BA_FIRST}:C{BA_LAST}', f'{S}!$Q$6:$Q$10')
    K.dropdown(ws, f'F{BA_FIRST}:F{BA_LAST}', f'{S}!$R$6:$R$8')
    k = f'K{BA_FIRST}:K{BA_LAST}'
    ws.conditional_formatting.add(k, FormulaRule(formula=[f'LEFT(K{BA_FIRST},2)="OK"'], fill=PatternFill('solid', fgColor='D9F2C4')))
    ws.conditional_formatting.add(k, FormulaRule(formula=[f'LEFT(K{BA_FIRST},8)="Mismatch"'], fill=PatternFill('solid', fgColor='9B2C1F'), font=Font(name=K.FONT, bold=True, color='FFFFFF')))
    ws.conditional_formatting.add(k, FormulaRule(formula=[f'OR(LEFT(K{BA_FIRST},5)="Check",LEFT(K{BA_FIRST},3)="Not",LEFT(K{BA_FIRST},7)="Blocked")'], fill=PatternFill('solid', fgColor='FFF4CC'), font=Font(name=K.FONT, bold=True)))
    ws.freeze_panes = 'B5'
    return ws


def monitor_sheet(wb):
    ws = wb.create_sheet('Monitoring Plan')
    ws.sheet_view.showGridLines = False
    K.title_block(ws, 'Monitoring plan', 'Crawlability breaks quietly after releases, plugin updates and CDN changes. Keep these checks on a schedule: type the date you last did each one and the status updates.')
    head = ['Task', 'Where to check', 'Every (days)', 'Owner', 'Last done', 'Last result', 'Notes', 'Next due', 'Days until due', 'Status']
    fc = (8, 9, 10)
    K.header_row(ws, 4, head, formula_cols=fc, widths=[46, 44, 9, 13, 12, 12, 30, 12, 9, 24])
    for r in range(MP_FIRST, MP_LAST + 1):
        i = r - MP_FIRST
        if i < len(TASKS):
            row = list(TASKS[i])
            row[4] = d(row[4])
            for col, v in enumerate(row, 1):
                if v not in (None, ''):
                    ws.cell(row=r, column=col, value=v)
        e = f'A{r}=""'
        ws[f'H{r}'] = f'=IF(OR({e},E{r}="",C{r}=""),"",E{r}+C{r})'
        ws[f'I{r}'] = f'=IF(H{r}="","",H{r}-{DATE})'
        ws[f'J{r}'] = (f'=IF({e},"",IF(E{r}="","Never done: do it now",IF(I{r}<0,"Overdue by "&(-I{r})&" days",IF(I{r}<={MSOON},"Due soon",'
                       f'IF(F{r}="Issue found","Done: follow up the issue","OK")))))')
    K.style_body(ws, MP_FIRST, MP_LAST, len(head), formula_cols=fc, number_formats={5: 'dd mmm yyyy', 8: 'dd mmm yyyy'}, wrap_cols=(1, 2, 7))
    K.dropdown(ws, f'F{MP_FIRST}:F{MP_LAST}', f'{S}!$U$6:$U$8')
    K.whole_number(ws, f'C{MP_FIRST}:C{MP_LAST}', 1, 400, 'How often, in days.')
    j = f'J{MP_FIRST}:J{MP_LAST}'
    ws.conditional_formatting.add(j, FormulaRule(formula=[f'OR(LEFT(J{MP_FIRST},7)="Overdue",LEFT(J{MP_FIRST},5)="Never")'], fill=PatternFill('solid', fgColor='F8D7D3'), font=Font(name=K.FONT, bold=True, color='9B2C1F')))
    ws.conditional_formatting.add(j, CellIsRule(operator='equal', formula=['"Due soon"'], fill=PatternFill('solid', fgColor='FFF4CC'), font=Font(name=K.FONT, bold=True)))
    ws.conditional_formatting.add(j, CellIsRule(operator='equal', formula=['"OK"'], fill=PatternFill('solid', fgColor='D9F2C4')))
    ws.freeze_panes = 'B5'
    return ws


def chart(ws, title, ytitle, cat_col, val_cols, r1, r2, anchor, colors, horiz, titles, h=7.5, stacked=False, w=17):
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
    for col, w in zip('ABCDEFGH', [52, 12, 3, 44, 10, 3, 3, 3]):
        ws.column_dimensions[col].width = w
    m = M
    want = f'{uc("C")},"Yes"'
    v = uc(m['Verdict'])
    kpis = [
        ('URLs checked', f'=COUNTA({uc("A")})', '0'),
        ('URLs you want indexed', f'=COUNTIF({uc("C")},"Yes")', '0'),
        ('Wanted URLs that are indexable now', f'=COUNTIFS({want},{uc(m["Indexability"])},"Indexable")', '0'),
        ('Wanted URLs blocked by robots.txt', f'=COUNTIFS({want},{uc("F")},"Yes")', '0'),
        ('Wanted URLs with noindex', f'=COUNTIFS({want},{uc(m["No noindex"])},0)', '0'),
        ('Wanted URLs not returning 200', f'=COUNTIFS({want},{uc(m["Returns 200"])},0)', '0'),
        ('Wanted URLs whose canonical points elsewhere', f'=COUNTIFS({want},{uc(m["Canonical points to itself"])},0)', '0'),
        ('Wanted URLs with no internal links (orphans)', f'=COUNTIFS({want},{uc(m["Linked internally"])},0)', '0'),
        ('Wanted URLs Google has not indexed', f'=COUNTIFS({want},{uc(m["Google has indexed it"])},0)', '0'),
        ('Unwanted URLs that Google has indexed', f'=COUNTIF({uc(m["Unwanted URL kept out"])},0)', '0'),
        ('Noindex pages hidden by robots.txt', f'=COUNTIF({uc(m["Noindex can be seen"])},0)', '0'),
        ('Sitemap URLs that are not indexable', f'=COUNTIF({uc(m["Sitemap lists only indexable URLs"])},0)', '0'),
        ('Average URL score', f'=IFERROR(ROUND(AVERAGE({uc(m["Score (0 to 100)"])}),0),0)', '0'),
        ('robots.txt lines Google ignores', f'=COUNTIF({rt("H")},"No*")', '0'),
        ('robots.txt High and Medium flags', f'=COUNTIF({rt("J")},"High")+COUNTIF({rt("J")},"Medium")', '0'),
        ('robots.txt size', f"={RTS}!C5", '@'),
        ('Sitemap files with problems', f"=COUNTIFS({SFS}!$Q${SF_FIRST}:$Q${SF_LAST},\"<>OK\",{SFS}!$A${SF_FIRST}:$A${SF_LAST},\"<>\")", '0'),
        ('Bot policy mismatches', f"=COUNTIF({BAS}!$K${BA_FIRST}:$K${BA_LAST},\"Mismatch*\")", '0'),
        ('Monitoring tasks overdue or never done', f"=COUNTIF({MPS}!$J${MP_FIRST}:$J${MP_LAST},\"Overdue*\")+COUNTIF({MPS}!$J${MP_FIRST}:$J${MP_LAST},\"Never*\")", '0'),
    ]
    ws['A4'] = 'KEY NUMBERS'
    ws['A4'].font = K.f(10, True, K.DEEP)
    for i, (label, fml, fmt) in enumerate(kpis):
        r = 5 + i
        ws.cell(row=r, column=1, value=label).font = K.f(10)
        c = ws.cell(row=r, column=2, value=fml)
        c.number_format, c.font, c.fill, c.border = fmt, K.f(11, True), K.FORMULA_FILL, K.BORDER
        c.alignment = Alignment(horizontal='right', wrap_text=fmt == '@')
    ws['D4'] = 'URLS BY VERDICT'
    ws['D4'].font = K.f(10, True, K.DEEP)
    for j, h in enumerate(['Verdict', 'URLs']):
        c = ws.cell(row=5, column=4 + j, value=h)
        c.font, c.fill = K.f(10, True, 'FFFFFF'), K.HEAD_F
    for i, vd in enumerate(VERDICTS):
        r = 6 + i
        ws.cell(row=r, column=4, value=vd).border = K.BORDER
        c = ws.cell(row=r, column=5, value=f'=COUNTIF({v},D{r})')
        c.border, c.fill = K.BORDER, K.FORMULA_FILL
    vlast = 5 + len(VERDICTS)
    ws.conditional_formatting.add(f'E6:E{vlast}', ColorScaleRule(start_type='num', start_value=0, start_color='FFFFFF', end_type='num', end_value=5, end_color='E07A5F'))
    t2 = 28
    ws.cell(row=t2 - 1, column=1, value='URLS FAILING EACH CHECK').font = K.f(10, True, K.DEEP)
    for j, h in enumerate(['Check', 'Fix', 'Partly']):
        c = ws.cell(row=t2, column=1 + j, value=h)
        c.font, c.fill = K.f(10, True, 'FFFFFF'), K.HEAD_F
    for i, col in enumerate(CK):
        r = t2 + 1 + i
        ws.cell(row=r, column=1, value=f'={S}!A{CHK_ROW + i}').border = K.BORDER
        for cc, val in ((2, 0), (3, 0.5)):
            c = ws.cell(row=r, column=cc, value=f'=COUNTIF({uc(col)},{val})')
            c.border, c.fill = K.BORDER, K.FORMULA_FILL
    chart(ws, 'URLs by verdict', 'URLs', 4, [5], 6, vlast, 'G4', ['E07A5F'], True, False, h=10)
    chart(ws, 'URLs failing each check', 'URLs', 1, [2, 3], t2 + 1, t2 + NCH, 'G25', ['E07A5F', 'F2C94C'], True, True, h=10, stacked=True)
    return ws, t2


def build(path, asset, url):
    wb = K.new_book()
    checker_sheet(wb)
    robots_sheet(wb)
    sitemaps_sheet(wb)
    bots_sheet(wb)
    dashboard_sheet(wb)
    monitor_sheet(wb)
    settings_sheet(wb)
    K.prompts_sheet(wb, asset['prompts'], url)
    K.checklist_sheet(wb, list(asset['checklist']))
    K.sources_sheet(wb, asset['sources'], [
        ('Demo data', 'BrightLedger and every URL in the demo are fictional (.example domain). All statuses, dates, links, log hits and impressions are illustrative, not real data.', ''),
        ('Score and verdicts', 'Weighted share of the 13 checks a URL passes (pass 1, partly 0.5, fix 0). Checks that do not apply are left out. Weights, the click depth rule, the lastmod allowance and the grade bands are assumptions to tune on Settings.', ''),
        ('robots.txt rules', 'Google supports user-agent, allow, disallow and sitemap (crawl-delay is not supported), enforces a 500 KiB limit, obeys only the most specific matching group and does not combine user agent groups with the * group.', 'https://developers.google.com/crawling/docs/robots-txt/robots-txt-spec'),
        ('Sitemap rules', 'Google limits a sitemap to 50 MB uncompressed or 50,000 URLs, asks for absolute URLs, ignores priority and changefreq and uses lastmod only if it is consistently and verifiably accurate.', 'https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap'),
        ('Canonicals and noindex', 'Google: redirects and rel canonical are strong canonical signals, sitemaps a weak one; do not use robots.txt for canonicalisation, and a URL disallowed in robots.txt may still be indexed without its content.', 'https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls'),
        ('Google-Extended', 'Google says Google-Extended has no separate user agent, controls use for Gemini training and grounding, and does not affect inclusion or ranking in Google Search.', 'https://developers.google.com/crawling/docs/crawlers-fetchers/google-common-crawlers'),
        ('Anthropic bots', 'ClaudeBot, Claude-SearchBot and Claude-User purposes and robots.txt behaviour, from Anthropic\'s help centre.', 'https://support.claude.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler'),
        ('Perplexity bots', 'PerplexityBot and Perplexity-User purposes and robots.txt behaviour, from Perplexity\'s crawler documentation.', 'https://docs.perplexity.ai/guides/perplexitybot'),
        ('AI crawlers and JavaScript', 'A Vercel and MERJ study (December 2024) found that none of the major AI crawlers it measured rendered JavaScript. Test your own logs; behaviour may change.', 'https://vercel.com/blog/the-rise-of-the-ai-crawler'),
    ])
    K.start_here(
        wb, 'Crawlability Checks Kit',
        [
            'This workbook checks whether search engines and AI bots can crawl and index the pages you want, and keep out the ones you do not: robots.txt, noindex, status codes, canonicals, XML sitemaps, internal links, click depth, JavaScript and the Search Console Page indexing status, all in one place.',
            f'It ships with demo data for a fictional accounting software company ({len(P)} URLs, a {len(ROBOTS)} line robots.txt, {len(SITEMAPS)} sitemap files and {len(BOTS)} bots) so you can see every check and verdict working. Clear the yellow demo cells when you are ready.',
        ],
        [
            ('URL Checker', 'One row per URL, 500 rows ready: 17 inputs, 7 measures, 13 weighted checks, score, grade, fixes in priority order and a verdict that names the conflict.'),
            ('Robots.txt Review', 'Paste robots.txt line by line. Splits each line, tracks the user agent group, says what Google ignores and flags risky rules.'),
            ('Sitemap Files', 'Checks each sitemap file: status, absolute URL, 50,000 URLs and 50 MB limits, Search Console status and when Google last read it.'),
            ('AI Bot Access', 'Your policy for Googlebot, Google-Extended and the OpenAI, Anthropic and Perplexity bots, compared with what your robots.txt really does.'),
            ('Dashboard', '19 key numbers, URLs by verdict and URLs failing each check, with two charts.'),
            ('Monitoring Plan', 'Recurring crawlability checks with next due dates and overdue warnings.'),
            ('Settings', 'Audit date, thresholds, the 13 check weights with rules and fixes, page types, Search Console statuses and lists.'),
            ('AI Prompts', 'Prompts for ChatGPT, Claude or Gemini to read robots.txt, sitemaps and Page indexing exports.'),
            ('Checklist', 'The crawlability checklist as a tick list with automatic progress.'),
            ('Sources', 'Where facts come from and which numbers are assumptions.'),
        ],
        [
            'Look at the demo on every tab, then clear the yellow demo cells. On Settings, set the audit date.',
            'List your URLs on the URL Checker: important pages from every template plus the URLs you want kept out. Choose Should be indexed? for each.',
            'Crawl the site and add status, robots.txt block, noindex, canonical, sitemap, lastmod, internal links and click depth. Add the Search Console Page indexing status from URL Inspection or the report.',
            'Paste your robots.txt into Robots.txt Review and your sitemap files into Sitemap Files.',
            'On AI Bot Access, choose Allow or Block for each bot and add log hits if you have them.',
            'Sort the URL Checker by Verdict. Fix every Fix now and Conflict row first, then canonicals, orphans and sitemap clean up.',
            'Keep the Monitoring Plan dates current and recheck after every release.',
        ],
        url,
    )
    order = ['Start Here', 'URL Checker', 'Robots.txt Review', 'Sitemap Files', 'AI Bot Access', 'Dashboard', 'Monitoring Plan', 'Settings', 'AI Prompts', 'Checklist', 'Sources']
    wb._sheets = [wb[n] for n in order]
    wb.active = 0
    for ws in wb.worksheets:
        ws.sheet_properties.tabColor = K.GREEN if ws.title in order[:7] else 'A6EF39'
    wb.save(path)


PREVIEW = {'sheet': 'URL Checker', 'header_row': 4, 'rows': 12,
           'cols': [1, 3, 4, NIN + 5, SC, SC + 1, SC + 2, SC + 4],
           'formula_idx': [3, 4, 5, 6, 7]}


def check(wb):
    """Assert the worked examples used in the guide."""
    a = wb['URL Checker']
    v = lambda h, r: a[f'{M[h]}{r}'].value
    r = 15   # /blog/tds-rates-2026/
    assert a[f'A{r}'].value.endswith('/blog/tds-rates-2026/')
    assert v('Indexability', r) == 'Noindex' and v('No noindex', r) == 0 and v('Sitemap lists only indexable URLs', r) == 0, v('Indexability', r)
    assert v('Google has indexed it', r) == 0 and v('Noindex can be seen', r) == 1 and v('Canonical target is live', r) is None
    assert v('Score (0 to 100)', r) == 70 and v('Grade', r) == 'B' and v('Fixes needed', r) == 3, v('Score (0 to 100)', r)
    assert v('Fixes in priority order', r) == 'No noindex; Sitemap lists only indexable URLs; Google has indexed it', v('Fixes in priority order', r)
    assert v('Verdict', r) == 'Fix now: noindex on a page you want', v('Verdict', r)
    exp = {5: 'Healthy', 7: 'Healthy', 8: 'Healthy', 9: 'Investigate: Google has not indexed it',
           10: 'Fix now: not returning 200', 11: 'Fix now: blocked by robots.txt', 14: 'Healthy', 16: 'Link it: orphan page',
           19: 'Investigate: Google has not indexed it', 20: 'Fix: canonical points elsewhere', 21: 'Clean up: remove from the sitemap',
           22: 'Clean up: remove from the sitemap', 23: 'Clean up: remove from the sitemap', 24: 'OK: kept out as planned',
           25: 'Clean up: indexed but you do not want it', 26: 'OK: kept out as planned', 27: 'OK: kept out as planned',
           28: 'OK: kept out as planned', 29: 'Conflict: noindex hidden by robots.txt', 30: 'Healthy'}
    for rr, x in exp.items():
        assert v('Verdict', rr) == x, (rr, a[f'A{rr}'].value, v('Verdict', rr), v('Fixes in priority order', rr))
    assert v('lastmod is accurate', 7) == 0 and v('lastmod is accurate', 8) == 0.5 and v('lastmod gap (days)', 8) == 52, v('lastmod gap (days)', 8)
    assert v('Canonical target status', 20) == 301 and v('Canonical target is live', 20) == 0, v('Canonical target status', 20)
    assert v('Canonical target is live', 26) == 1 and v('Shallow click depth', 17) == 0 and v('Content in the raw HTML', 18) == 0.5
    rv = wb['Robots.txt Review']
    rows = {rv[f'C{r}'].value: (rv[f'F{r}'].value, rv[f'H{r}'].value, rv[f'I{r}'].value, rv[f'J{r}'].value) for r in range(RT_FIRST, RT_FIRST + len(ROBOTS)) if rv[f'C{r}'].value}
    assert rows['User-agent: Googlebot'][3] == 'High' and 'Googlebot group' in rows['User-agent: Googlebot'][2], rows['User-agent: Googlebot']
    assert rows['Crawl-delay: 5'][1] == 'No: Google ignores crawl-delay' and rows['Noindex: /blog/tag/'][3] == 'Low', rows['Noindex: /blog/tag/']
    assert rows['Disallow: /assets/js/'][3] == 'Medium' and rows['Sitemap: /blog-sitemap.xml'][3] == 'Medium', rows['Disallow: /assets/js/']
    assert rows['Disallow: /'][0] == 'GPTBot, Google-Extended' and rows['Disallow: /'][3] == 'Info', rows['Disallow: /']
    assert rows['Disallow: /app/'][3] == 'OK' and rows['Disallow:'][3] == 'Info', rows['Disallow:']
    sf = wb['Sitemap Files']
    sv = [sf[f'Q{r}'].value for r in range(SF_FIRST, SF_FIRST + len(SITEMAPS))]
    assert sv[0] == 'OK' and sv[1] == 'OK' and sv[3] == 'Split it and list the parts in a sitemap index' and sv[4].startswith('Fix now'), sv
    assert sv[5] == 'Add it to robots.txt, a sitemap index or Search Console', sv
    ba = wb['AI Bot Access']
    bv = {ba[f'A{r}'].value: (ba[f'I{r}'].value, ba[f'J{r}'].value, ba[f'K{r}'].value) for r in range(BA_FIRST, BA_FIRST + len(BOTS))}
    assert bv['GPTBot'] == ('Own group', 'Yes', 'OK: blocked as planned') and bv['Google-Extended'][2] == 'OK: blocked as planned', bv
    assert bv['ClaudeBot'] == ('No: uses the * group', 'No', 'Mismatch: not blocked yet, add the lines on the right'), bv['ClaudeBot']
    assert bv['Claude-SearchBot'][2] == 'Check: 37 blocked or failed hits in your logs' and bv['Perplexity-User'][2].startswith('Not blocked'), bv
    assert bv['Googlebot'][2] == 'OK: allowed as planned' and bv['PerplexityBot'] == ('Own group', 'No', 'OK: allowed as planned'), bv
    dsh = wb['Dashboard']
    vals = {dsh.cell(row=r, column=1).value: dsh.cell(row=r, column=2).value for r in range(5, 24)}
    assert vals['URLs checked'] == 27 and vals['URLs you want indexed'] == 18, vals
    assert vals['Wanted URLs blocked by robots.txt'] == 1 and vals['Wanted URLs with noindex'] == 1 and vals['Wanted URLs not returning 200'] == 1, vals
    assert vals['Unwanted URLs that Google has indexed'] == 1 and vals['Noindex pages hidden by robots.txt'] == 1 and vals['Sitemap URLs that are not indexable'] == 7, vals
    assert vals['Wanted URLs Google has not indexed'] == 7 and vals['Bot policy mismatches'] == 1, vals
    mp = wb['Monitoring Plan']
    assert mp['J7'].value == 'Overdue by 7 days' and mp['J12'].value == 'Never done: do it now', (mp['J7'].value, mp['J12'].value)
