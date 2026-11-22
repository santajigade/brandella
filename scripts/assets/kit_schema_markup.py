"""Schema Markup Kit workbook (asset 11).

Schema Lab: one row per structured data block (500 rows). You paste the schema type, the format and the list
of properties in the markup, and record whether it matches the visible page, the Rich Results Test result,
the Search Console report, whether the page is blocked for Googlebot and when the values were last checked.
A Type Rules table on Settings holds Google's required and recommended properties for 17 types (with retired
rich results marked). The lab finds missing required and recommended properties, wrong types for the page and
self serving review markup, runs 11 weighted checks (1 = pass, 0.5 = partly, 0 = fix, blank = not checked) and
gives a score, grade, fixes in priority order, rich result eligibility and a priority. JSON-LD Builder writes
copy and paste JSON-LD for 9 types from plain form fields. Rollout Plan tracks markup per template.
"""
import datetime
import json
from openpyxl.styles import PatternFill, Font, Alignment
from openpyxl.formatting.rule import CellIsRule, ColorScaleRule, FormulaRule
from openpyxl.chart import BarChart, Reference
from openpyxl.utils import get_column_letter as L
import kitlib as K

SL_FIRST, SL_LAST = 5, 504      # Schema Lab
RP_FIRST, RP_LAST = 5, 104      # Rollout Plan
S = 'Settings'
SLS = "'Schema Lab'"

(DATE, COV1, COV2, FRESH1, FRESH2) = (f'{S}!$B${r}' for r in range(5, 10))
(GA, GB, GC) = (f'{S}!$B${r}' for r in range(11, 14))
CHK_ROW = 17
TR_FIRST = 33
TR_N = 22
TR_LAST = TR_FIRST + TR_N - 1
NREQ, NONE, NREC = 6, 3, 10
# Type Rules columns
TRC = {'type': 'A', 'feature': 'B', 'status': 'C', 'note': 'D', 'best': 'E'}
REQ_COLS = [L(6 + i) for i in range(NREQ)]            # F..K
ONE_COLS = [L(12 + i) for i in range(NONE)]           # L..N
REC_COLS = [L(15 + i) for i in range(NREC)]           # O..X
SELF_COL, CP_COL, CC_COL = 'Y', 'Z', 'AA'


def tr(col):
    return f'{S}!${col}${TR_FIRST}:${col}${TR_LAST}'


PAGE_TYPES = ['Home', 'Article or blog post', 'News article', 'Product page', 'Category page', 'Local business page', 'Event page',
              'Video page', 'Author profile', 'Forum thread', 'Review page', 'About page', 'FAQ or help page', 'How to guide', 'Fact check', 'Other']
ALL_BUT_HOME = ', '.join(p for p in PAGE_TYPES if p not in ('Home', 'Other'))
ART_REC = ['headline', 'image', 'datePublished', 'dateModified', 'author', 'author.name', 'author.url']
# type, Google result, status, note, best on, required, one of, recommended, self review check, conditional (if used, also required)
TYPES = [
    ('Article', 'Article: a better title, image and date in results', 'Supported', '', 'Article or blog post, News article, Video page, How to guide', [], [], ART_REC, 'No', None),
    ('BlogPosting', 'Article: a better title, image and date in results', 'Supported', 'A more specific Article type', 'Article or blog post, How to guide', [], [], ART_REC, 'No', None),
    ('NewsArticle', 'Article: a better title, image and date in results', 'Supported', 'A more specific Article type', 'News article, Article or blog post', [], [], ART_REC, 'No', None),
    ('Product', 'Product snippet: price, availability and ratings', 'Supported', 'Pages about one product only', 'Product page',
     ['name'], ['offers', 'review', 'aggregateRating'], ['aggregateRating', 'offers', 'review', 'offers.availability', 'offers.priceCurrency'], 'No', ('offers', 'offers.price')),
    ('Organization', 'Organization details: name, logo and facts Google can use', 'Supported', 'Home or about page', 'Home, About page',
     [], [], ['name', 'url', 'logo', 'sameAs', 'description', 'address', 'telephone', 'email', 'alternateName', 'contactPoint'], 'Yes', None),
    ('LocalBusiness', 'Local business details: address, hours and phone', 'Supported', 'Use the most specific subtype you can', 'Local business page, Home',
     ['name', 'address'], [], ['telephone', 'url', 'geo', 'openingHoursSpecification', 'priceRange', 'menu', 'servesCuisine', 'department'], 'Yes', None),
    ('BreadcrumbList', 'Breadcrumb trail in results', 'Supported', 'item is not required on the last crumb', ALL_BUT_HOME,
     ['itemListElement', 'item', 'name', 'position'], [], [], 'No', None),
    ('VideoObject', 'Video: thumbnail, date and key moments', 'Supported', '', 'Video page, Article or blog post, How to guide, Product page',
     ['name', 'thumbnailUrl', 'uploadDate'], [], ['description', 'duration', 'contentUrl', 'embedUrl', 'creator', 'interactionStatistic', 'expires', 'hasPart', 'regionsAllowed'], 'No', None),
    ('Event', 'Event: date, place and tickets', 'Supported', 'One page per event', 'Event page',
     ['name', 'startDate', 'location', 'location.address'], [], ['description', 'endDate', 'eventStatus', 'image', 'location.name', 'offers', 'organizer', 'performer', 'previousStartDate'], 'No', None),
    ('ProfilePage', 'Profile page: the person or organization behind content', 'Supported', 'Name the person in mainEntity', 'Author profile',
     ['mainEntity', 'mainEntity.name'], [], ['dateCreated', 'dateModified', 'mainEntity.alternateName', 'mainEntity.description', 'mainEntity.identifier', 'mainEntity.image', 'mainEntity.sameAs', 'mainEntity.interactionStatistic'], 'No', None),
    ('DiscussionForumPosting', 'Discussion forum: threads in forum results', 'Supported', '', 'Forum thread',
     ['author', 'author.name', 'datePublished'], ['text', 'image', 'video'], ['author.url', 'comment', 'commentCount', 'dateModified', 'headline', 'url', 'interactionStatistic', 'isPartOf', 'creativeWorkStatus', 'sharedContent'], 'No', None),
    ('Review', 'Review snippet: star rating', 'Supported', 'Reviews of other things, not your own business', 'Review page, Product page',
     ['author', 'itemReviewed', 'itemReviewed.name', 'reviewRating', 'reviewRating.ratingValue'], [], ['datePublished', 'reviewRating.bestRating', 'reviewRating.worstRating'], 'No', None),
    ('WebSite', 'Site name shown in results', 'Supported', 'Home page only', 'Home', ['name', 'url'], [], ['alternateName'], 'No', None),
    ('Person', 'No result of its own: used inside Article, ProfilePage and others', 'Supports other types', '', 'Author profile, About page, Article or blog post', [], [], [], 'No', None),
    ('FAQPage', 'FAQ rich result (retired)', 'Retired', 'Not shown in Google Search from 7 May 2026; docs removed June 2026', 'FAQ or help page', [], [], [], 'No', None),
    ('HowTo', 'How to rich result (retired)', 'Retired', 'Not shown on mobile from August 2023 or on desktop from September 2023', 'How to guide', [], [], [], 'No', None),
    ('ClaimReview', 'Fact check rich result (retired)', 'Retired', 'Phased out of Google Search in 2025', 'Fact check', [], [], [], 'No', None),
]
NTYPES = len(TYPES)
STATUSES = ['Supported', 'Supports other types', 'Retired']
FORMATS = ['JSON-LD', 'Microdata', 'RDFa']
MATCH = ['Yes', 'Partly', 'No']
RRT = ['Valid', 'Valid with warnings', 'Invalid', 'Not tested', 'Not supported by the test']
SCR = ['Valid', 'Warnings', 'Errors', 'Not shown']
RSTAT = ['Not started', 'In progress', 'Live', 'Validated']
AVAIL = ['InStock', 'OutOfStock', 'PreOrder', 'BackOrder', 'SoldOut']
EVSTAT = ['EventScheduled', 'EventCancelled', 'EventPostponed', 'EventRescheduled', 'EventMovedOnline']
ATTEND = ['OfflineEventAttendanceMode', 'OnlineEventAttendanceMode', 'MixedEventAttendanceMode']
LISTS = [('AC', 'Page type', PAGE_TYPES), ('AD', 'Format', FORMATS), ('AE', 'Matches?', MATCH), ('AF', 'Rich Results Test', RRT),
         ('AG', 'Search Console', SCR), ('AH', 'Yes/No', ['Yes', 'No']), ('AI', 'Rollout status', RSTAT), ('AJ', 'Availability', AVAIL),
         ('AK', 'Event status', EVSTAT), ('AL', 'Attendance', ATTEND), ('AM', 'Author type', ['Person', 'Organization']),
         ('AN', 'Article type', ['BlogPosting', 'Article', 'NewsArticle'])]
LREF = {name: f'{S}!${col}$6:${col}${5 + len(v)}' for col, name, v in LISTS}

CHECKS = [
    ('Type earns a Google result', 6, 'Supported or Supports other types = pass. A retired rich result (FAQPage, HowTo, ClaimReview) = partly. Unknown type = not checked.',
     'Google no longer shows this rich result. Accurate markup can stay, but spend your time on supported types.'),
    ('All required properties', 12, 'Every required property in Type Rules is in the markup, one of each either or group, and any property required when another is used (for example offers.price with offers). Not checked for retired types.',
     'Add the missing required properties. Google says items missing required properties are not eligible for rich results.'),
    ('Enough recommended properties', 6, 'Share of recommended properties present: 70 percent or more = pass, 40 percent or more = partly, less = fix (editable). Not checked when a type has none.',
     'Add the recommended properties you can fill with true, visible facts. Google says the more you provide, the higher quality the result.'),
    ('Matches the visible page', 12, 'Your check: every value in the markup is on the page and true (Yes), some values differ (Partly) or values are missing or wrong (No).',
     'Make every marked up value match what visitors see. Google says structured data must be a true representation of the page and that AI features need it to match the visible text.'),
    ('Not blocked for Googlebot', 8, 'The page is not blocked by robots.txt, noindex or a login (Yes = blocked = fix).',
     'Unblock the page. Google says not to block structured data pages with robots.txt, noindex or other access controls.'),
    ('Passes Rich Results Test', 8, 'Valid = pass, Valid with warnings = partly, Invalid or Not tested = fix, Not supported by the test or blank = not checked.',
     'Test the live URL in the Rich Results Test and fix every error. Warnings are usually missing recommended properties.'),
    ('Search Console status', 5, 'The matching enhancement report in Search Console: Valid = pass, Warnings = partly, Errors = fix, Not shown = not checked.',
     'Open the report, fix the items with errors and click Validate fix.'),
    ('Type fits the page', 6, 'The page type is in the Best on page types list for this schema type (Type Rules).',
     'Use the type that describes the main content of this page. For example, Product markup belongs on a page about one product, not a category page.'),
    ('No self serving reviews', 5, 'For Organization and LocalBusiness (editable in Type Rules): no review or aggregateRating in the markup. Not checked for other types.',
     'Remove review and aggregateRating from markup about your own business. Google does not show review stars for reviews a business controls about itself.'),
    ('JSON-LD format', 3, 'JSON-LD = pass. Microdata or RDFa = partly.', 'Microdata and RDFa work, but Google recommends JSON-LD because it is the easiest to add and maintain.'),
    ('Values up to date', 4, 'Days since you last checked the values against the page: up to 180 = pass, up to 365 = partly, older = fix (editable). Blank = not checked.',
     'Recheck prices, dates, hours and authors, and update the markup with the page. Google asks for up to date information.'),
]
NCH = len(CHECKS)

# Demo: BrewNest Coffee Roasters, a fictional roastery and cafe in Pune. Every page and number is illustrative.
U = 'https://brewnest.example'
# url, page type, schema type, format, properties, matches, RRT, SC, blocked, last checked, impressions, notes
P = [
    ('/', 'Home', 'Organization', 'JSON-LD', 'name, url, logo, sameAs, address, telephone, aggregateRating, review', 'Yes', 'Valid', 'Not shown', 'No', '2026-10-01', 12000, 'Reviews from the cafe widget'),
    ('/', 'Home', 'WebSite', 'JSON-LD', 'name, url, alternateName', 'Yes', '', '', 'No', '2026-10-01', 12000, ''),
    ('/blog/pour-over-coffee-guide/', 'Article or blog post', 'BlogPosting', 'JSON-LD', 'headline, image, datePublished, author', 'Yes', 'Valid', 'Valid', 'No', '2026-09-15', 9500, ''),
    ('/blog/pour-over-coffee-guide/', 'Article or blog post', 'BreadcrumbList', 'JSON-LD', 'itemListElement, item, name, position', 'Yes', 'Valid', 'Valid', 'No', '2026-09-15', 9500, ''),
    ('/blog/best-coffee-beans-india/', 'Article or blog post', 'BlogPosting', 'Microdata', 'headline, image, datePublished, dateModified, author, author.name', 'Partly', 'Valid with warnings', 'Valid', 'No', '2026-08-20', 15000, 'dateModified newer than the date on the page'),
    ('/shop/monsoon-malabar-250g/', 'Product page', 'Product', 'JSON-LD', 'name, image, description, brand, sku, offers, offers.price, offers.priceCurrency, offers.availability, aggregateRating', 'Yes', 'Valid', 'Valid', 'No', '2026-11-02', 6200, ''),
    ('/shop/kalimpong-light-roast/', 'Product page', 'Product', 'JSON-LD', 'name, image, description, brand, offers, offers.price, offers.priceCurrency', 'No', 'Valid', 'Warnings', 'No', '2026-03-10', 4200, 'Worked example: markup says Rs 499, page says Rs 549'),
    ('/shop/coorg-dark-roast/', 'Product page', 'Product', 'JSON-LD', 'name, image, description, brand', 'Yes', 'Invalid', 'Errors', 'No', '2026-11-02', 3100, 'Price block missing from the template'),
    ('/shop/', 'Category page', 'Product', 'JSON-LD', 'name, offers, offers.price, offers.priceCurrency', 'Partly', 'Valid', 'Valid', 'No', '2026-11-02', 18000, 'Theme adds Product markup to the category'),
    ('/cafe/koregaon-park/', 'Local business page', 'LocalBusiness', 'JSON-LD', 'name, address, telephone, url, geo, openingHoursSpecification, priceRange, menu, servesCuisine', 'Yes', 'Valid', 'Not shown', 'No', '2026-10-20', 2600, ''),
    ('/events/home-brewing-workshop/', 'Event page', 'Event', 'JSON-LD', 'name, startDate, endDate, location, location.name, image, description, offers', 'Yes', 'Invalid', 'Errors', 'No', '2026-11-10', 900, 'Venue address missing'),
    ('/videos/aeropress-recipe/', 'Video page', 'VideoObject', 'JSON-LD', 'name, description, thumbnailUrl, contentUrl, duration', 'Yes', 'Invalid', 'Errors', 'No', '2026-11-10', 1400, 'Upload date missing'),
    ('/help/faq/', 'FAQ or help page', 'FAQPage', 'JSON-LD', 'mainEntity', 'Yes', 'Not supported by the test', '', 'No', '2026-06-01', 2000, 'Rich result retired in 2026'),
    ('/blog/how-to-make-cold-brew/', 'How to guide', 'HowTo', 'JSON-LD', 'name, step, totalTime, supply', 'Yes', 'Not supported by the test', '', 'No', '2025-12-01', 5400, 'Rich result retired in 2023'),
    ('/team/anika-rao/', 'Author profile', 'ProfilePage', 'JSON-LD', 'mainEntity, mainEntity.name, mainEntity.image, mainEntity.sameAs, dateModified', 'Yes', 'Valid', '', 'Yes', '2026-11-01', 0, 'Team pages set to noindex by mistake'),
]
# Rollout plan: group, example url, pages, type, owner, status, target date, notes
PLAN = [
    ('Home page', '/', 1, 'Organization', 'Anika', 'Validated', '2026-10-01', 'Remove the review widget markup'),
    ('Home page', '/', 1, 'WebSite', 'Anika', 'Validated', '2026-10-01', ''),
    ('Blog post template', '/blog/pour-over-coffee-guide/', 64, 'BlogPosting', 'Dev team', 'Live', '2026-09-15', 'Add dateModified and author.url'),
    ('All pages except home', '/blog/pour-over-coffee-guide/', 139, 'BreadcrumbList', 'Dev team', 'Live', '2026-09-15', ''),
    ('Product template', '/shop/monsoon-malabar-250g/', 38, 'Product', 'Dev team', 'In progress', '2026-11-30', 'Fix the price block'),
    ('Cafe pages', '/cafe/koregaon-park/', 3, 'LocalBusiness', 'Anika', 'Validated', '2026-10-20', ''),
    ('Event pages', '/events/home-brewing-workshop/', 6, 'Event', 'Dev team', 'Not started', '2026-11-15', 'Add the venue address'),
    ('Video pages', '/videos/aeropress-recipe/', 12, 'VideoObject', 'Dev team', 'Not started', '2026-12-20', ''),
    ('Author pages', '/team/anika-rao/', 4, 'ProfilePage', 'Anika', 'In progress', '2026-12-10', 'Remove noindex first'),
    ('Help centre', '/help/faq/', 1, 'FAQPage', 'Anika', 'Not started', '2026-12-31', ''),
]

IN_HEAD = ['URL', 'Page type', 'Schema type', 'Format', 'Properties in the markup (comma list)', 'Matches the visible page?', 'Rich Results Test',
           'Search Console report', 'Blocked for Googlebot?', 'Values last checked', 'Impressions (28 days)', 'Notes']
MEAS_HEAD = ['Google result', 'Google status', 'Type fits the page?', 'Required properties', 'Required missing', 'Missing required (list)',
             'Recommended properties', 'Recommended present', 'Recommended coverage', 'Missing recommended (list)', 'Self serving review markup?', 'Days since checked']
OUT_HEAD = ['Score (0 to 100)', 'Grade', 'Fixes needed', 'Fixes in priority order', 'Rich result eligibility', 'Priority']
HELP_HEAD = (['Rule row (helper)', 'Normalized properties (helper)'] + [f'Required {i + 1} missing (helper)' for i in range(NREQ)] +
             ['Either or present (helper)', 'Conditional missing (helper)'] + [f'Recommended {i + 1} missing (helper)' for i in range(NREC)])
NIN, NME = len(IN_HEAD), len(MEAS_HEAD)
C0 = NIN + NME + 1
CK = [L(C0 + i) for i in range(NCH)]
SC = C0 + NCH
H0 = SC + len(OUT_HEAD)
HEAD = IN_HEAD + MEAS_HEAD + [c[0] for c in CHECKS] + OUT_HEAD + HELP_HEAD
F_COLS = tuple(range(NIN + 1, len(HEAD) + 1))
M = {h: L(i + 1) for i, h in enumerate(HEAD)}
PRIOS = ['Fix now: blocked for Googlebot', 'Fix now: markup does not match the page', 'Fix now: required properties missing', 'Fix now: invalid markup',
         'Fix now: self serving review markup', 'Fix: wrong type for this page', 'Low priority: rich result retired', 'Improve: add recommended properties',
         'Improve when you can', 'Healthy: monitor']


def sl(c):
    return f'{SLS}!${c}${SL_FIRST}:${c}${SL_LAST}'


def d(s):
    return datetime.date.fromisoformat(s) if s else None


def settings_sheet(wb):
    ws = wb.create_sheet(S)
    ws.sheet_view.showGridLines = False
    K.title_block(ws, 'Settings', 'Thresholds, check weights, the Type Rules table and lists. Change a blue value and every score updates.')
    widths = {'A': 46, 'B': 36, 'C': 18, 'D': 40, 'E': 40}
    for c in REQ_COLS + ONE_COLS + REC_COLS:
        widths[c] = 17
    widths.update({SELF_COL: 12, CP_COL: 12, CC_COL: 14, 'AB': 3})
    for col, name, v in LISTS:
        widths[col] = 22
    for c, w in widths.items():
        ws.column_dimensions[c].width = w
    rows = [
        (4, 'RULES', None, None),
        (5, 'Analysis date (set it to the day you check)', datetime.date(2026, 11, 22), 'dd mmm yyyy'),
        (6, 'Recommended properties: pass at or above this share', 0.7, '0%'),
        (7, 'Recommended properties: partly at or above this share', 0.4, '0%'),
        (8, 'Values up to date: pass up to this many days since checked', 180, '0'),
        (9, 'Values up to date: partly up to this many days', 365, '0'),
        (10, 'GRADES', None, None),
        (11, 'Grade A when the score is at least', 85, '0'),
        (12, 'Grade B when at least', 70, '0'),
        (13, 'Grade C when at least (below = D)', 55, '0'),
    ]
    for r, label, val, fmt in rows:
        a = ws.cell(row=r, column=1, value=label)
        a.font = K.f(10, val is None, K.DEEP if val is None else K.INK)
        if val is not None:
            c = ws.cell(row=r, column=2, value=val)
            c.border, c.fill = K.BORDER, K.INPUT_FILL
            c.font = K.f(10, True, '0000FF')
            c.number_format = fmt
    ws['D5'] = ('Required and recommended properties come from Google Search Central structured data docs (read November 2026). '
                'The 70 and 40 percent coverage bands, the 180 and 365 day freshness rule, the weights and the grade bands are assumptions of this kit. '
                'Google does not guarantee a rich result even when markup is correct.')
    ws['D5'].font = K.f(9, False, '777777', True)
    ws['D5'].alignment = Alignment(wrap_text=True, vertical='top')
    ws.merge_cells('D5:E13')
    ws.cell(row=CHK_ROW - 2, column=1, value='THE 11 CHECKS (weights are editable; any numbers, they are scaled)').font = K.f(10, True, K.DEEP)
    K.header_row(ws, CHK_ROW - 1, ['Check', 'Weight', 'Rule in the workbook', 'How to fix'])
    for i, (name, w, rule, fix) in enumerate(CHECKS):
        r = CHK_ROW + i
        for col, v in enumerate([name, w, rule, fix], 1):
            c = ws.cell(row=r, column=col, value=v)
            c.border = K.BORDER
            c.font = K.f(10, col == 1, '0000FF' if col == 2 else K.INK)
            c.alignment = Alignment(wrap_text=True, vertical='top')
        ws.cell(row=r, column=2).fill = K.INPUT_FILL
        ws.row_dimensions[r].height = 48
    tr_ = CHK_ROW + NCH
    ws.cell(row=tr_, column=1, value='Total weight (auto)').font = K.f(10, True)
    ws.cell(row=tr_, column=2, value=f'=SUM(B{CHK_ROW}:B{tr_ - 1})').fill = K.FORMULA_FILL
    ws.cell(row=TR_FIRST - 3, column=1, value='TYPE RULES (Google required and recommended properties; nested properties use a dot, for example author.name; add your own types in the empty rows)').font = K.f(10, True, K.DEEP)
    ws.cell(row=TR_FIRST - 2, column=6, value='Required').font = K.f(9, True, K.DEEP)
    ws.cell(row=TR_FIRST - 2, column=12, value='Required: at least one of').font = K.f(9, True, K.DEEP)
    ws.cell(row=TR_FIRST - 2, column=15, value='Recommended').font = K.f(9, True, K.DEEP)
    heads = (['Schema type', 'What Google can show', 'Google status', 'Note', 'Best on page types (comma list)'] + [f'Req {i + 1}' for i in range(NREQ)] +
             [f'One of {i + 1}' for i in range(NONE)] + [f'Rec {i + 1}' for i in range(NREC)] + ['Check self reviews?', 'If this is used', 'this is also required'])
    K.header_row(ws, TR_FIRST - 1, heads)
    for i in range(TR_N):
        r = TR_FIRST + i
        if i < NTYPES:
            t, feat, st, note, best, req, one, rec, selfc, cond = TYPES[i]
            vals = [t, feat, st, note, best] + (req + [None] * NREQ)[:NREQ] + (one + [None] * NONE)[:NONE] + (rec + [None] * NREC)[:NREC] + [selfc] + list(cond or (None, None))
        else:
            vals = [None] * len(heads)
        for j, v in enumerate(vals, 1):
            c = ws.cell(row=r, column=j, value=v)
            c.fill, c.border = K.INPUT_FILL, K.BORDER
            c.font = K.f(9, j == 1)
            c.alignment = Alignment(wrap_text=j in (2, 4, 5), vertical='top')
        ws.row_dimensions[r].height = 30
    K.dropdown(ws, f'C{TR_FIRST}:C{TR_LAST}', '"Supported,Supports other types,Retired"')
    ws.conditional_formatting.add(f'C{TR_FIRST}:C{TR_LAST}', CellIsRule(operator='equal', formula=['"Retired"'], fill=PatternFill('solid', fgColor='F8D7D3'), font=Font(name=K.FONT, bold=True, color='9B2C1F')))
    ws['AC4'] = 'LISTS'
    ws['AC4'].font = K.f(10, True, K.DEEP)
    for col, name, vals in LISTS:
        c = ws[f'{col}5']
        c.value = name
        c.font = K.f(9, True, '555555')
        for i, v in enumerate(vals):
            ws[f'{col}{6 + i}'] = v
            ws[f'{col}{6 + i}'].font = K.f(9)
    ws.freeze_panes = 'B4'
    return ws


def lab_sheet(wb):
    ws = wb.create_sheet('Schema Lab')
    ws.sheet_view.showGridLines = False
    K.title_block(ws, 'Schema lab', f'Rows 5 to {4 + len(P)} hold DEMO data for BrewNest, a fictional coffee roastery (illustrative pages and numbers). Select the yellow demo cells and press Delete to start your own. Grey formula columns stay.')
    ws['A2'].font = K.f(10, True, 'B45309')
    ws['A3'] = ('One row per structured data block (a page with Article and BreadcrumbList markup gets 2 rows). List the property names in the markup, '
                'separated by commas, with a dot for nested ones (author.name, offers.price). 500 rows ready.')
    ws['A3'].font = K.f(9, False, '666666', True)
    widths = ([38, 18, 18, 10, 46, 10, 14, 11, 9, 11, 10, 30] + [30, 12, 8, 9, 8, 30, 10, 10, 10, 34, 9, 8] +
              [9] * NCH + [9, 7, 7, 52, 32, 34] + [8] * len(HELP_HEAD))
    K.header_row(ws, 4, HEAD, formula_cols=F_COLS, widths=widths)
    for i, col in enumerate(CK):
        c = ws[f'{col}3']
        c.value = f'={S}!$B${CHK_ROW + i}'
        c.font, c.fill, c.alignment = K.f(9, True, K.DEEP), K.SOFT, Alignment(horizontal='center')
    ws[f'{CK[0]}2'] = 'Check weights (from Settings)'
    ws[f'{CK[0]}2'].font = K.f(9, True, K.DEEP)
    m = M
    for r in range(SL_FIRST, SL_LAST + 1):
        i = r - SL_FIRST
        if i < len(P):
            row = list(P[i])
            row[0] = U + row[0]
            row[9] = d(row[9])
            for col, v in enumerate(row, 1):
                if v not in (None, ''):
                    ws.cell(row=r, column=col, value=v)
        e = f'A{r}=""'
        g = lambda h: f'{m[h]}{r}'
        rr, nrm = g('Rule row (helper)'), g('Normalized properties (helper)')
        ix = lambda col: f'INDEX({tr(col)},{rr})'
        pres = lambda p: f'OR(ISNUMBER(SEARCH(","&{p}&",",{nrm})),ISNUMBER(SEARCH(","&{p}&".",{nrm})))'
        f = {}
        f['Rule row (helper)'] = f'=IF(OR({e},C{r}=""),"",IFERROR(MATCH(TRIM(C{r}),{tr("A")},0),""))'
        f['Normalized properties (helper)'] = f'=IF({e},"",","&SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(LOWER(E{r})," ",""),";",","),CHAR(10),",")&",")'
        for k, col in enumerate(REQ_COLS):
            f[f'Required {k + 1} missing (helper)'] = f'=IF({rr}="","",IF({ix(col)}="","",IF({pres(ix(col))},"",{ix(col)})))'
        f['Either or present (helper)'] = f'=IF({rr}="","",IF({ix(ONE_COLS[0])}="","",' + '+'.join(f'IF({ix(c)}="",0,IF({pres(ix(c))},1,0))' for c in ONE_COLS) + '))'
        f['Conditional missing (helper)'] = f'=IF({rr}="","",IF({ix(CP_COL)}="","",IF(AND({pres(ix(CP_COL))},NOT({pres(ix(CC_COL))})),{ix(CC_COL)},"")))'
        for k, col in enumerate(REC_COLS):
            f[f'Recommended {k + 1} missing (helper)'] = f'=IF({rr}="","",IF({ix(col)}="","",IF({pres(ix(col))},"",{ix(col)})))'
        f['Google result'] = f'=IF({e},"",IF({rr}="","Unknown type: check the spelling or add it to Type Rules",{ix("B")}))'
        f['Google status'] = f'=IF(OR({e},{rr}=""),"",{ix("C")})'
        f['Type fits the page?'] = f'=IF(OR({e},{rr}="",B{r}=""),"",IF(ISNUMBER(SEARCH(", "&B{r}&",",", "&{ix("E")}&",")),"Yes","No"))'
        rq1, rqN = g('Required 1 missing (helper)'), g(f'Required {NREQ} missing (helper)')
        eo, cm = g('Either or present (helper)'), g('Conditional missing (helper)')
        nreq = '+'.join(f'IF({ix(c)}="",0,1)' for c in REQ_COLS)
        f['Required properties'] = f'=IF(OR({e},{rr}=""),"",{nreq}+IF({ix(ONE_COLS[0])}="",0,1)+IF({cm}="",IF(AND({ix(CP_COL)}<>"",{pres(ix(CP_COL))}),1,0),1))'
        f['Required missing'] = f'=IF(OR({e},{rr}=""),"",COUNTIF({rq1}:{rqN},"?*")+IF({eo}=0,1,0)+IF({cm}="",0,1))'
        onelist = '_xlfn.TEXTJOIN(", ",TRUE,' + ','.join(ix(c) for c in ONE_COLS) + ')'
        f['Missing required (list)'] = f'=IF(OR({e},{rr}=""),"",_xlfn.TEXTJOIN(", ",TRUE,{rq1}:{rqN},IF({eo}=0,"one of "&{onelist},""),{cm}))'
        nrec = '+'.join(f'IF({ix(c)}="",0,1)' for c in REC_COLS)
        rc1, rcN = g('Recommended 1 missing (helper)'), g(f'Recommended {NREC} missing (helper)')
        f['Recommended properties'] = f'=IF(OR({e},{rr}=""),"",{nrec})'
        rt = g('Recommended properties')
        f['Recommended present'] = f'=IF(OR({e},{rr}=""),"",{rt}-COUNTIF({rc1}:{rcN},"?*"))'
        f['Recommended coverage'] = f'=IF(OR({e},{rr}="",N({rt})=0),"",{g("Recommended present")}/{rt})'
        f['Missing recommended (list)'] = f'=IF(OR({e},{rr}=""),"",_xlfn.TEXTJOIN(", ",TRUE,{rc1}:{rcN}))'
        f['Self serving review markup?'] = f'=IF(OR({e},{rr}=""),"",IF({ix(SELF_COL)}<>"Yes","",IF(OR({pres(chr(34) + "review" + chr(34))},{pres(chr(34) + "aggregaterating" + chr(34))}),"Yes","No")))'
        f['Days since checked'] = f'=IF(OR({e},J{r}=""),"",{DATE}-J{r})'
        st = g('Google status')
        t = {}
        t['Type earns a Google result'] = f'=IF(OR({e},{st}=""),"",IF({st}="Retired",0.5,1))'
        t['All required properties'] = f'=IF(OR({e},{st}="",{st}="Retired"),"",IF({g("Required missing")}=0,1,0))'
        cov = g('Recommended coverage')
        t['Enough recommended properties'] = f'=IF(OR({e},{cov}="",{st}="Retired"),"",IF({cov}>={COV1},1,IF({cov}>={COV2},0.5,0)))'
        t['Matches the visible page'] = f'=IF(OR({e},F{r}=""),"",IF(F{r}="Yes",1,IF(F{r}="Partly",0.5,0)))'
        t['Not blocked for Googlebot'] = f'=IF(OR({e},I{r}=""),"",IF(I{r}="Yes",0,1))'
        t['Passes Rich Results Test'] = f'=IF(OR({e},G{r}="",G{r}="Not supported by the test"),"",IF(G{r}="Valid",1,IF(G{r}="Valid with warnings",0.5,0)))'
        t['Search Console status'] = f'=IF(OR({e},H{r}="",H{r}="Not shown"),"",IF(H{r}="Valid",1,IF(H{r}="Warnings",0.5,0)))'
        t['Type fits the page'] = f'=IF(OR({e},{g("Type fits the page?")}=""),"",IF({g("Type fits the page?")}="Yes",1,0))'
        t['No self serving reviews'] = f'=IF(OR({e},{g("Self serving review markup?")}=""),"",IF({g("Self serving review markup?")}="Yes",0,1))'
        t['JSON-LD format'] = f'=IF(OR({e},D{r}=""),"",IF(D{r}="JSON-LD",1,0.5))'
        ds = g('Days since checked')
        t['Values up to date'] = f'=IF(OR({e},{ds}=""),"",IF({ds}<={FRESH1},1,IF({ds}<={FRESH2},0.5,0)))'
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
        rm, fit, srv = g('Required missing'), g('Type fits the page?'), g('Self serving review markup?')
        ws[g('Rich result eligibility')] = (
            f'=IF({e},"",IF({rr}="","Unknown type",IF({st}="Retired","No: Google retired this rich result",IF({st}="Supports other types","No result of its own: supports other markup",'
            f'IF(I{r}="Yes","No: blocked for Googlebot",IF(N({rm})>0,"No: required properties missing",IF(F{r}="No","No: does not match the page",'
            f'IF({fit}="No","No: wrong type for this page",IF(G{r}="Invalid","No: invalid in the Rich Results Test",IF({srv}="Yes","Details only: no review stars for self serving reviews",'
            f'IF(OR(G{r}="Valid",G{r}="Valid with warnings"),"Eligible (Google does not guarantee it)","Test it in the Rich Results Test")))))))))))')
        ws[g('Priority')] = (
            f'=IF(OR({e},{sc}{r}=""),"",IF(I{r}="Yes","{PRIOS[0]}",IF(F{r}="No","{PRIOS[1]}",IF(AND({st}<>"Retired",N({rm})>0),"{PRIOS[2]}",'
            f'IF(G{r}="Invalid","{PRIOS[3]}",IF({srv}="Yes","{PRIOS[4]}",IF({fit}="No","{PRIOS[5]}",IF({st}="Retired","{PRIOS[6]}",'
            f'IF(AND({cov}<>"",N({cov})<{COV1}),"{PRIOS[7]}",IF({sc}{r}>={GA},"{PRIOS[9]}","{PRIOS[8]}"))))))))))')
    nf = {10: 'dd mmm yyyy', 11: '#,##0', NIN + 9: '0%', NIN + 12: '0', SC: '0'}
    K.style_body(ws, SL_FIRST, SL_LAST, len(HEAD), formula_cols=F_COLS, number_formats=nf, wrap_cols=(5, 12, NIN + 1, NIN + 6, NIN + 10, SC + 3, SC + 4))
    ws.freeze_panes = 'B5'
    ws.auto_filter.ref = f'A4:{L(H0 - 1)}{SL_LAST}'
    K.dropdown(ws, f'B{SL_FIRST}:B{SL_LAST}', LREF['Page type'])
    K.dropdown(ws, f'C{SL_FIRST}:C{SL_LAST}', f'{S}!$A${TR_FIRST}:$A${TR_LAST}', 'Types and their rules live on Settings. Add your own in the empty rows.')
    K.dropdown(ws, f'D{SL_FIRST}:D{SL_LAST}', LREF['Format'])
    K.dropdown(ws, f'F{SL_FIRST}:F{SL_LAST}', LREF['Matches?'], 'Compare every value in the markup with what visitors see on the page.')
    K.dropdown(ws, f'G{SL_FIRST}:G{SL_LAST}', LREF['Rich Results Test'])
    K.dropdown(ws, f'H{SL_FIRST}:H{SL_LAST}', LREF['Search Console'])
    K.dropdown(ws, f'I{SL_FIRST}:I{SL_LAST}', LREF['Yes/No'], 'Yes if robots.txt, noindex or a login blocks Googlebot.')
    chk = f'{CK[0]}{SL_FIRST}:{CK[-1]}{SL_LAST}'
    ws.conditional_formatting.add(chk, CellIsRule(operator='equal', formula=['1'], fill=PatternFill('solid', fgColor='D9F2C4')))
    ws.conditional_formatting.add(chk, CellIsRule(operator='equal', formula=['0.5'], fill=PatternFill('solid', fgColor='FFF4CC')))
    ws.conditional_formatting.add(chk, FormulaRule(formula=[f'AND(ISNUMBER({CK[0]}{SL_FIRST}),{CK[0]}{SL_FIRST}=0)'], fill=PatternFill('solid', fgColor='F8D7D3'), font=Font(name=K.FONT, bold=True, color='9B2C1F')))
    scol = L(SC)
    ws.conditional_formatting.add(f'{scol}{SL_FIRST}:{scol}{SL_LAST}', ColorScaleRule(start_type='num', start_value=30, start_color='F8D7D3', mid_type='num', mid_value=70, mid_color='FFF4CC', end_type='num', end_value=100, end_color='B7E4A0'))
    gcol = f'{L(SC + 1)}{SL_FIRST}:{L(SC + 1)}{SL_LAST}'
    for val, col in (('A', '9BE07A'), ('B', 'D9F2C4'), ('C', 'FFF4CC'), ('D', 'F8D7D3')):
        ws.conditional_formatting.add(gcol, CellIsRule(operator='equal', formula=[f'"{val}"'], fill=PatternFill('solid', fgColor=col), font=Font(name=K.FONT, bold=True)))
    el = L(SC + 4)
    ws.conditional_formatting.add(f'{el}{SL_FIRST}:{el}{SL_LAST}', FormulaRule(formula=[f'LEFT({el}{SL_FIRST},8)="Eligible"'], fill=PatternFill('solid', fgColor='D9F2C4'), font=Font(name=K.FONT, bold=True)))
    ws.conditional_formatting.add(f'{el}{SL_FIRST}:{el}{SL_LAST}', FormulaRule(formula=[f'LEFT({el}{SL_FIRST},3)="No:"'], fill=PatternFill('solid', fgColor='F8D7D3')))
    pc = L(SC + 5)
    pr = f'{pc}{SL_FIRST}:{pc}{SL_LAST}'
    for start, n, fill, fc in (('Fix now', 7, '9B2C1F', 'FFFFFF'), ('Fix:', 4, 'F8D7D3', '9B2C1F'), ('Low', 3, 'EEEEEE', '555555'), ('Improve:', 8, 'FFF4CC', '1F1F1F'), ('Healthy', 7, 'D9F2C4', '1F1F1F')):
        ws.conditional_formatting.add(pr, FormulaRule(formula=[f'LEFT({pc}{SL_FIRST},{n})="{start}"'], fill=PatternFill('solid', fgColor=fill), font=Font(name=K.FONT, bold=True, color=fc)))
    st = m['Google status']
    ws.conditional_formatting.add(f'{st}{SL_FIRST}:{st}{SL_LAST}', CellIsRule(operator='equal', formula=['"Retired"'], font=Font(name=K.FONT, bold=True, color='9B2C1F')))
    mr = m['Missing required (list)']
    ws.conditional_formatting.add(f'{mr}{SL_FIRST}:{mr}{SL_LAST}', FormulaRule(formula=[f'{mr}{SL_FIRST}<>""'], font=Font(name=K.FONT, bold=True, color='9B2C1F')))
    for j in range(H0, len(HEAD) + 1):
        ws.column_dimensions[L(j)].hidden = True
    return ws


# ---------- JSON-LD Builder ----------
def lit(s):
    return '"' + s.replace('"', '""') + '"'


def esc(ref):
    return f'SUBSTITUTE(SUBSTITUTE(TRIM({ref}),"\\","\\\\"),"""","\\""")'


def p_str(key, ref):
    return f'IF(TRIM({ref})="","",{lit(f", {chr(34)}{key}{chr(34)}: {chr(34)}")}&{esc(ref)}&{lit(chr(34))})'


def p_num(key, ref):
    return f'IF(TRIM({ref})="","",{lit(f", {chr(34)}{key}{chr(34)}: ")}&SUBSTITUTE(TRIM({ref}),",","."))'


def p_enum(key, ref):
    return f'IF(TRIM({ref})="","",{lit(f", {chr(34)}{key}{chr(34)}: {chr(34)}https://schema.org/")}&TRIM({ref})&{lit(chr(34))})'


def p_list(key, ref):
    return (f'IF(TRIM({ref})="","",{lit(f", {chr(34)}{key}{chr(34)}: [{chr(34)}")}&SUBSTITUTE(SUBSTITUTE(TRIM({ref})," ",""),",",{lit(chr(34) + "," + chr(34))})'
            f'&{lit(chr(34) + "]")})')


def p_list_words(key, ref):
    """Comma list of words that may contain spaces (for example day names)."""
    return (f'IF(TRIM({ref})="","",{lit(f", {chr(34)}{key}{chr(34)}: [{chr(34)}")}&SUBSTITUTE(SUBSTITUTE(TRIM({ref}),", ",","),",",{lit(chr(34) + ", " + chr(34))})'
            f'&{lit(chr(34) + "]")})')


def p_obj(key, typ, cond, parts):
    inner = '&'.join(parts) if parts else '""'
    return f'IF({cond},{lit(f", {chr(34)}{key}{chr(34)}: {{{chr(34)}@type{chr(34)}: {chr(34)}{typ}{chr(34)}")}&{inner}&"}}","")'


def wrap(typ_expr, parts):
    return (f'={lit("<script type=" + chr(34) + "application/ld+json" + chr(34) + ">{" + chr(34) + "@context" + chr(34) + ": " + chr(34) + "https://schema.org" + chr(34) + ", " + chr(34) + "@type" + chr(34) + ": " + chr(34))}'
            f'&{typ_expr}&{lit(chr(34))}&' + '&'.join(parts) + f'&{lit("}</script>")}')


# block: key, title, type (fixed string or field id), fields (id, label, note, demo, list), parts builder, missing rules
BLOCKS = [
    ('article', 'Article or blog post', 'type', [
        ('type', '@type', 'BlogPosting, Article or NewsArticle', 'BlogPosting', 'Article type'),
        ('headline', 'headline', 'Recommended. The title of the article', 'Pour over coffee guide: ratios, grind size and timing', None),
        ('image', 'image (one or more URLs, comma separated)', 'Recommended. Crawlable, indexable image URLs', 'https://brewnest.example/img/pour-over-16x9.jpg, https://brewnest.example/img/pour-over-1x1.jpg', None),
        ('datePublished', 'datePublished', 'Recommended. ISO 8601, with time zone', '2026-09-15T08:00:00+05:30', None),
        ('dateModified', 'dateModified', 'Recommended. Only change it after a real update', '2026-11-02T09:30:00+05:30', None),
        ('authorType', 'author @type', 'Person or Organization', 'Person', 'Author type'),
        ('authorName', 'author.name', 'Recommended. As shown on the page', 'Anika Rao', None),
        ('authorUrl', 'author.url', 'Recommended. Profile page of the author', 'https://brewnest.example/team/anika-rao/', None),
    ], 'article'),
    ('product', 'Product (product snippet)', 'Product', [
        ('name', 'name', 'Required', 'Monsoon Malabar coffee beans 250 g', None),
        ('image', 'image (comma separated URLs)', 'Optional extra', 'https://brewnest.example/img/monsoon-malabar.jpg', None),
        ('description', 'description', 'Optional extra', 'Medium roast, low acidity, notes of cocoa and spice.', None),
        ('sku', 'sku', 'Optional extra', 'BN-MM-250', None),
        ('brand', 'brand.name', 'Optional extra', 'BrewNest', None),
        ('price', 'offers.price', 'Required inside offers. Number only', 549, None),
        ('currency', 'offers.priceCurrency', 'Recommended. ISO 4217 code', 'INR', None),
        ('avail', 'offers.availability', 'Recommended', 'InStock', 'Availability'),
        ('offerUrl', 'offers.url', 'Optional extra', 'https://brewnest.example/shop/monsoon-malabar-250g/', None),
        ('rating', 'aggregateRating.ratingValue', 'Optional. Only real reviews shown on the page', 4.6, None),
        ('count', 'aggregateRating.reviewCount', 'Needed with a rating', 38, None),
    ], 'product'),
    ('org', 'Organization (home or about page)', 'Organization', [
        ('name', 'name', 'Recommended', 'BrewNest Coffee Roasters', None),
        ('alt', 'alternateName', 'Recommended', 'BrewNest', None),
        ('url', 'url', 'Recommended', 'https://brewnest.example/', None),
        ('logo', 'logo', 'Recommended. Image URL', 'https://brewnest.example/img/logo-512.png', None),
        ('desc', 'description', 'Recommended', 'Specialty coffee roastery and cafe in Pune, roasting Indian estate coffees since 2019.', None),
        ('email', 'email', 'Recommended', 'hello@brewnest.example', None),
        ('tel', 'telephone', 'Recommended. With country code', '+91-20-5555-0101', None),
        ('street', 'address.streetAddress', 'Recommended', '12 Lane 5, Koregaon Park', None),
        ('city', 'address.addressLocality', 'Recommended', 'Pune', None),
        ('region', 'address.addressRegion', 'Recommended', 'Maharashtra', None),
        ('zip', 'address.postalCode', 'Recommended', '411001', None),
        ('country', 'address.addressCountry', 'Recommended. 2 letter code', 'IN', None),
        ('sameas', 'sameAs (comma separated URLs)', 'Recommended. Your official profiles', 'https://www.instagram.com/brewnest.example, https://www.youtube.com/@brewnest.example', None),
    ], 'org'),
    ('local', 'LocalBusiness (one location page)', 'type', [
        ('type', '@type', 'LocalBusiness or a subtype, for example CafeOrCoffeeShop', 'CafeOrCoffeeShop', None),
        ('name', 'name', 'Required', 'BrewNest Cafe Koregaon Park', None),
        ('url', 'url', 'Recommended', 'https://brewnest.example/cafe/koregaon-park/', None),
        ('tel', 'telephone', 'Recommended', '+91-20-5555-0102', None),
        ('image', 'image (comma separated URLs)', 'Optional extra', 'https://brewnest.example/img/cafe-kp.jpg', None),
        ('price', 'priceRange', 'Recommended', 'Rs 200 to 600', None),
        ('street', 'address.streetAddress', 'Required (address)', '12 Lane 5, Koregaon Park', None),
        ('city', 'address.addressLocality', 'Required (address)', 'Pune', None),
        ('region', 'address.addressRegion', 'Recommended', 'Maharashtra', None),
        ('zip', 'address.postalCode', 'Recommended', '411001', None),
        ('country', 'address.addressCountry', 'Recommended', 'IN', None),
        ('lat', 'geo.latitude', 'Recommended. Number', 18.5362, None),
        ('lng', 'geo.longitude', 'Recommended. Number', 73.8939, None),
        ('days1', 'Opening hours 1: days (comma separated)', 'Recommended', 'Monday, Tuesday, Wednesday, Thursday, Friday', None),
        ('open1', 'Opening hours 1: opens (HH:MM)', '', '08:00', None),
        ('close1', 'Opening hours 1: closes (HH:MM)', '', '21:00', None),
        ('days2', 'Opening hours 2: days', 'Optional', 'Saturday, Sunday', None),
        ('open2', 'Opening hours 2: opens', '', '09:00', None),
        ('close2', 'Opening hours 2: closes', '', '22:00', None),
        ('menu', 'menu (URL)', 'Recommended for food places', 'https://brewnest.example/cafe/menu/', None),
        ('cuisine', 'servesCuisine', 'Recommended for food places', 'Coffee, Bakery', None),
    ], 'local'),
    ('crumbs', 'BreadcrumbList', 'BreadcrumbList', [
        (f'{k}{i}', f'Crumb {i}: {"name" if k == "n" else "URL"}', ('Required' if k == 'n' else 'Required, except on the last crumb') if i <= 2 else 'Optional', v, None)
        for i, (nm, url) in enumerate([('Home', 'https://brewnest.example/'), ('Blog', 'https://brewnest.example/blog/'), ('Pour over coffee guide', ''), ('', ''), ('', '')], 1)
        for k, v in (('n', nm), ('u', url))
    ], 'crumbs'),
    ('video', 'VideoObject', 'VideoObject', [
        ('name', 'name', 'Required', 'AeroPress recipe in 3 minutes', None),
        ('desc', 'description', 'Recommended', 'Our head roaster shows a simple AeroPress recipe for one cup.', None),
        ('thumb', 'thumbnailUrl (comma separated URLs)', 'Required', 'https://brewnest.example/img/aeropress-thumb.jpg', None),
        ('upload', 'uploadDate', 'Required. ISO 8601 with time zone', '2026-11-05T10:00:00+05:30', None),
        ('dur', 'duration', 'Recommended. ISO 8601, for example PT3M10S', 'PT3M10S', None),
        ('content', 'contentUrl', 'Recommended. The video file', 'https://brewnest.example/video/aeropress.mp4', None),
        ('embed', 'embedUrl', 'Recommended. The player', 'https://brewnest.example/embed/aeropress', None),
    ], 'video'),
    ('event', 'Event', 'Event', [
        ('name', 'name', 'Required', 'Home brewing workshop: pour over and AeroPress', None),
        ('desc', 'description', 'Recommended', 'A 2 hour hands on class for beginners. Beans and gear provided.', None),
        ('image', 'image (comma separated URLs)', 'Recommended', 'https://brewnest.example/img/workshop.jpg', None),
        ('start', 'startDate', 'Required. ISO 8601 with time zone', '2026-12-13T10:00:00+05:30', None),
        ('end', 'endDate', 'Recommended', '2026-12-13T12:00:00+05:30', None),
        ('status', 'eventStatus', 'Recommended', 'EventScheduled', 'Event status'),
        ('mode', 'eventAttendanceMode', 'Optional extra', 'OfflineEventAttendanceMode', 'Attendance'),
        ('venue', 'location.name', 'Recommended', 'BrewNest Cafe Koregaon Park', None),
        ('street', 'location.address.streetAddress', 'Required (location.address)', '12 Lane 5, Koregaon Park', None),
        ('city', 'location.address.addressLocality', 'Required (location.address)', 'Pune', None),
        ('zip', 'location.address.postalCode', 'Recommended', '411001', None),
        ('country', 'location.address.addressCountry', 'Recommended', 'IN', None),
        ('price', 'offers.price', 'Recommended. Number', 1500, None),
        ('currency', 'offers.priceCurrency', 'Recommended', 'INR', None),
        ('ourl', 'offers.url', 'Recommended', 'https://brewnest.example/events/home-brewing-workshop/', None),
        ('avail', 'offers.availability', 'Recommended', 'InStock', 'Availability'),
        ('org', 'organizer.name', 'Recommended', 'BrewNest Coffee Roasters', None),
        ('orgurl', 'organizer.url', 'Recommended', 'https://brewnest.example/', None),
    ], 'event'),
    ('profile', 'ProfilePage (author page)', 'ProfilePage', [
        ('name', 'mainEntity.name (Person)', 'Required', 'Anika Rao', None),
        ('alt', 'mainEntity.alternateName', 'Recommended. A handle', 'anikabrews', None),
        ('desc', 'mainEntity.description', 'Recommended', 'Head roaster at BrewNest. Q grader with 9 years in specialty coffee.', None),
        ('image', 'mainEntity.image', 'Recommended', 'https://brewnest.example/img/anika.jpg', None),
        ('sameas', 'mainEntity.sameAs (comma separated URLs)', 'Recommended', 'https://www.linkedin.com/in/anika-rao-example', None),
        ('created', 'dateCreated', 'Recommended', '2024-02-01T09:00:00+05:30', None),
        ('modified', 'dateModified', 'Recommended', '2026-11-01T09:00:00+05:30', None),
    ], 'profile'),
    ('website', 'WebSite (site name, home page only)', 'WebSite', [
        ('name', 'name', 'Required. Your preferred site name', 'BrewNest Coffee Roasters', None),
        ('alt', 'alternateName', 'Recommended. Another name people use', 'BrewNest', None),
        ('url', 'url', 'Required. Your home page', 'https://brewnest.example/', None),
    ], 'website'),
]
BUILD_OUT = {}   # block key -> (output cell, check cell)


def block_formula(kind, c):
    if kind == 'article':
        parts = [p_str('headline', c['headline']), p_list('image', c['image']), p_str('datePublished', c['datePublished']), p_str('dateModified', c['dateModified']),
                 f'IF(TRIM({c["authorName"]})="","",{lit(", " + chr(34) + "author" + chr(34) + ": [{" + chr(34) + "@type" + chr(34) + ": " + chr(34))}&IF(TRIM({c["authorType"]})="","Person",TRIM({c["authorType"]}))&{lit(chr(34))}'
                 f'&{p_str("name", c["authorName"])}&{p_str("url", c["authorUrl"])}&"}}]")']
        typ = f'IF(TRIM({c["type"]})="","BlogPosting",TRIM({c["type"]}))'
        miss = [(f'TRIM({c["headline"]})=""', 'headline (recommended)'), (f'TRIM({c["image"]})=""', 'image (recommended)'),
                (f'TRIM({c["datePublished"]})=""', 'datePublished (recommended)'), (f'TRIM({c["authorName"]})=""', 'author.name (recommended)')]
    elif kind == 'product':
        offer = p_obj('offers', 'Offer', f'TRIM({c["price"]})<>""', [p_num('price', c['price']), p_str('priceCurrency', c['currency']), p_enum('availability', c['avail']), p_str('url', c['offerUrl'])])
        rating = p_obj('aggregateRating', 'AggregateRating', f'AND(TRIM({c["rating"]})<>"",TRIM({c["count"]})<>"")', [p_num('ratingValue', c['rating']), p_num('reviewCount', c['count'])])
        brand = p_obj('brand', 'Brand', f'TRIM({c["brand"]})<>""', [p_str('name', c['brand'])])
        parts = [p_str('name', c['name']), p_list('image', c['image']), p_str('description', c['description']), p_str('sku', c['sku']), brand, offer, rating]
        typ = lit('Product')
        miss = [(f'TRIM({c["name"]})=""', 'name'), (f'AND(TRIM({c["price"]})="",OR(TRIM({c["rating"]})="",TRIM({c["count"]})=""))', 'offers.price or a rating with reviewCount'),
                (f'AND(TRIM({c["rating"]})<>"",TRIM({c["count"]})="")', 'reviewCount for the rating')]
    elif kind == 'org':
        addr = p_obj('address', 'PostalAddress', f'TRIM({c["street"]}&{c["city"]})<>""', [p_str('streetAddress', c['street']), p_str('addressLocality', c['city']),
                                                                                          p_str('addressRegion', c['region']), p_str('postalCode', c['zip']), p_str('addressCountry', c['country'])])
        parts = [p_str('name', c['name']), p_str('alternateName', c['alt']), p_str('url', c['url']), p_str('logo', c['logo']), p_str('description', c['desc']),
                 p_str('email', c['email']), p_str('telephone', c['tel']), addr, p_list('sameAs', c['sameas'])]
        typ = lit('Organization')
        miss = [(f'TRIM({c["name"]})=""', 'name (recommended)'), (f'TRIM({c["url"]})=""', 'url (recommended)'), (f'TRIM({c["logo"]})=""', 'logo (recommended)')]
    elif kind == 'local':
        addr = p_obj('address', 'PostalAddress', f'TRIM({c["street"]}&{c["city"]})<>""', [p_str('streetAddress', c['street']), p_str('addressLocality', c['city']),
                                                                                          p_str('addressRegion', c['region']), p_str('postalCode', c['zip']), p_str('addressCountry', c['country'])])
        geo = p_obj('geo', 'GeoCoordinates', f'AND(TRIM({c["lat"]})<>"",TRIM({c["lng"]})<>"")', [p_num('latitude', c['lat']), p_num('longitude', c['lng'])])

        def spec(dd, o, cl):
            return (f'"{{"&{lit(chr(34) + "@type" + chr(34) + ": " + chr(34) + "OpeningHoursSpecification" + chr(34))}&{p_list_words("dayOfWeek", dd)}'
                    f'&{p_str("opens", o)}&{p_str("closes", cl)}&"}}"')
        hours = (f'IF(TRIM({c["days1"]})="","",{lit(", " + chr(34) + "openingHoursSpecification" + chr(34) + ": [")}&{spec(c["days1"], c["open1"], c["close1"])}'
                 f'&IF(TRIM({c["days2"]})="","",", "&{spec(c["days2"], c["open2"], c["close2"])})&"]")')
        parts = [p_str('name', c['name']), p_str('url', c['url']), p_str('telephone', c['tel']), p_list('image', c['image']), p_str('priceRange', c['price']),
                 addr, geo, hours, p_str('menu', c['menu']), p_str('servesCuisine', c['cuisine'])]
        typ = f'IF(TRIM({c["type"]})="","LocalBusiness",TRIM({c["type"]}))'
        miss = [(f'TRIM({c["name"]})=""', 'name'), (f'TRIM({c["street"]}&{c["city"]})=""', 'address')]
    elif kind == 'crumbs':
        items = []
        for i in range(1, 6):
            n, u = c[f'n{i}'], c[f'u{i}']
            item = (f'"{{"&{lit(chr(34) + "@type" + chr(34) + ": " + chr(34) + "ListItem" + chr(34) + ", " + chr(34) + "position" + chr(34) + ": " + str(i))}'
                    f'&{p_str("name", n)}&{p_str("item", u)}&"}}"')
            items.append(item if i == 1 else f'IF(TRIM({n})="","",", "&{item})')
        parts = [f'{lit(", " + chr(34) + "itemListElement" + chr(34) + ": [")}&' + '&'.join(items) + '&"]"']
        typ = lit('BreadcrumbList')
        miss = [(f'TRIM({c["n1"]})=""', 'crumb 1 name'), (f'TRIM({c["n2"]})=""', 'at least 2 crumbs')]
        for i in range(1, 5):
            miss.append((f'AND(TRIM({c[f"n{i + 1}"]})<>"",TRIM({c[f"u{i}"]})="")', f'crumb {i} URL'))
    elif kind == 'video':
        parts = [p_str('name', c['name']), p_str('description', c['desc']), p_list('thumbnailUrl', c['thumb']), p_str('uploadDate', c['upload']),
                 p_str('duration', c['dur']), p_str('contentUrl', c['content']), p_str('embedUrl', c['embed'])]
        typ = lit('VideoObject')
        miss = [(f'TRIM({c["name"]})=""', 'name'), (f'TRIM({c["thumb"]})=""', 'thumbnailUrl'), (f'TRIM({c["upload"]})=""', 'uploadDate')]
    elif kind == 'event':
        addr = p_obj('address', 'PostalAddress', f'TRIM({c["street"]}&{c["city"]})<>""', [p_str('streetAddress', c['street']), p_str('addressLocality', c['city']),
                                                                                          p_str('postalCode', c['zip']), p_str('addressCountry', c['country'])])
        loc = p_obj('location', 'Place', f'TRIM({c["venue"]}&{c["street"]}&{c["city"]})<>""', [p_str('name', c['venue']), addr])
        offer = p_obj('offers', 'Offer', f'TRIM({c["price"]}&{c["ourl"]})<>""', [p_num('price', c['price']), p_str('priceCurrency', c['currency']), p_str('url', c['ourl']), p_enum('availability', c['avail'])])
        org = p_obj('organizer', 'Organization', f'TRIM({c["org"]})<>""', [p_str('name', c['org']), p_str('url', c['orgurl'])])
        parts = [p_str('name', c['name']), p_str('description', c['desc']), p_list('image', c['image']), p_str('startDate', c['start']), p_str('endDate', c['end']),
                 p_enum('eventStatus', c['status']), p_enum('eventAttendanceMode', c['mode']), loc, offer, org]
        typ = lit('Event')
        miss = [(f'TRIM({c["name"]})=""', 'name'), (f'TRIM({c["start"]})=""', 'startDate'), (f'TRIM({c["street"]}&{c["city"]})=""', 'location.address')]
    elif kind == 'profile':
        person = p_obj('mainEntity', 'Person', f'TRIM({c["name"]}&{c["alt"]})<>""', [p_str('name', c['name']), p_str('alternateName', c['alt']), p_str('description', c['desc']),
                                                                                    p_str('image', c['image']), p_list('sameAs', c['sameas'])])
        parts = [p_str('dateCreated', c['created']), p_str('dateModified', c['modified']), person]
        typ = lit('ProfilePage')
        miss = [(f'TRIM({c["name"]}&{c["alt"]})=""', 'mainEntity.name')]
    else:
        parts = [p_str('name', c['name']), p_str('alternateName', c['alt']), p_str('url', c['url'])]
        typ = lit('WebSite')
        miss = [(f'TRIM({c["name"]})=""', 'name'), (f'TRIM({c["url"]})=""', 'url')]
    out = wrap(typ, parts)
    chk = '_xlfn.TEXTJOIN(", ",TRUE,' + ','.join(f'IF({cond},"{txt}","")' for cond, txt in miss) + ')'
    check = f'=IF({chk}="","Ready to paste. Then test the page in the Rich Results Test.","Missing: "&{chk})'
    return out, check


def builder_sheet(wb):
    ws = wb.create_sheet('JSON-LD Builder')
    ws.sheet_view.showGridLines = False
    K.title_block(ws, 'JSON-LD builder', 'Fill the yellow fields. Grey cells build JSON-LD you can copy and paste into the page head or body. Empty optional fields are left out by themselves.')
    ws['A3'] = ('Copy the grey output cell (one line, ready to paste), then check the live page in the Rich Results Test. Only mark up facts that visitors can see on the page. '
                'Demo values are for the fictional BrewNest.')
    ws['A3'].font = K.f(9, False, '666666', True)
    for c, w in zip('ABCDE', [42, 52, 40, 3, 100]):
        ws.column_dimensions[c].width = w
    r = 5
    for key, title, _, fields, kind in BLOCKS:
        ws.cell(row=r, column=1, value=title.upper()).font = K.f(11, True, K.DEEP)
        for j, h in enumerate(['Property', 'Your value', 'Note'], 1):
            c = ws.cell(row=r + 1, column=j, value=h)
            c.font, c.fill, c.border = K.f(10, True, 'FFFFFF'), K.HEAD_IN, K.BORDER
        c = ws.cell(row=r + 1, column=5, value='JSON-LD output (copy this cell)')
        c.font, c.fill, c.border = K.f(10, True, 'FFFFFF'), K.HEAD_F, K.BORDER
        refs = {}
        fr = r + 2
        for i, (fid, label, note, demo, lst) in enumerate(fields):
            rr = fr + i
            ws.cell(row=rr, column=1, value=label).font = K.f(10, 'Required' in note)
            v = ws.cell(row=rr, column=2, value=demo if demo != '' else None)
            v.fill, v.border, v.font = K.INPUT_FILL, K.BORDER, K.f(10)
            v.alignment = Alignment(wrap_text=True, vertical='top')
            if isinstance(demo, str):
                v.number_format = '@'
            if lst:
                K.dropdown(ws, f'B{rr}', LREF[lst])
            n = ws.cell(row=rr, column=3, value=note)
            n.font = K.f(9, False, '9B2C1F' if note.startswith('Required') else '666666', True)
            ws.cell(row=rr, column=1).border = K.BORDER
            n.border = K.BORDER
            refs[fid] = f'$B${rr}'
        lr = fr + len(fields) - 1
        out, check = block_formula(kind, refs)
        o = ws.cell(row=fr, column=5, value=out)
        o.fill, o.font, o.alignment, o.border = K.FORMULA_FILL, Font(name='Consolas', size=9), Alignment(wrap_text=True, vertical='top'), K.BORDER
        ws.merge_cells(start_row=fr, start_column=5, end_row=lr, end_column=5)
        cr = lr + 1
        ws.cell(row=cr, column=1, value='Check').font = K.f(10, True)
        ck = ws.cell(row=cr, column=2, value=check)
        ck.fill, ck.font, ck.border = K.FORMULA_FILL, K.f(10, True), K.BORDER
        ws.merge_cells(start_row=cr, start_column=2, end_row=cr, end_column=3)
        ws.conditional_formatting.add(f'B{cr}', FormulaRule(formula=[f'LEFT(B{cr},5)="Ready"'], fill=PatternFill('solid', fgColor='D9F2C4')))
        ws.conditional_formatting.add(f'B{cr}', FormulaRule(formula=[f'LEFT(B{cr},7)="Missing"'], fill=PatternFill('solid', fgColor='F8D7D3'), font=Font(name=K.FONT, bold=True, color='9B2C1F')))
        BUILD_OUT[key] = (f'E{fr}', f'B{cr}')
        r = cr + 3
    return ws


def rollout_sheet(wb):
    ws = wb.create_sheet('Rollout Plan')
    ws.sheet_view.showGridLines = False
    K.title_block(ws, 'Rollout plan', 'Structured data is added per template, not per page. One row per template and schema type. The plan shows what Google needs and the next step.')
    head = ['Template or page group', 'Example URL', 'Pages using it', 'Schema type', 'Owner', 'Status', 'Target date', 'Notes',
            'What Google can show', 'Google status', 'Required properties', 'Recommended properties', 'Days to target', 'Next step']
    fc = tuple(range(9, 15))
    K.header_row(ws, 4, head, formula_cols=fc, widths=[26, 36, 9, 18, 12, 12, 12, 30, 34, 14, 40, 52, 9, 52])
    for r in range(RP_FIRST, RP_LAST + 1):
        i = r - RP_FIRST
        if i < len(PLAN):
            g_, u, n, t, o, st, dt, nt = PLAN[i]
            for col, v in enumerate([g_, U + u, n, t, o, st, d(dt), nt], 1):
                if v not in (None, ''):
                    ws.cell(row=r, column=col, value=v)
        e = f'OR(A{r}="",D{r}="")'
        rr = f'MATCH(TRIM(D{r}),{tr("A")},0)'
        ix = lambda col: f'INDEX({tr(col)},{rr})'
        ws.cell(row=r, column=9, value=f'=IF({e},"",IFERROR({ix("B")},"Unknown type"))')
        ws.cell(row=r, column=10, value=f'=IF({e},"",IFERROR({ix("C")},""))')
        req = ','.join(ix(c) for c in REQ_COLS)
        one = ','.join(ix(c) for c in ONE_COLS)
        ws.cell(row=r, column=11, value=f'=IF({e},"",IFERROR(_xlfn.TEXTJOIN(", ",TRUE,{req},IF({ix(ONE_COLS[0])}="","","one of "&_xlfn.TEXTJOIN(" or ",TRUE,{one})),IF({ix(CC_COL)}="","",{ix(CC_COL)}&" (with "&{ix(CP_COL)}&")")),""))')
        rec = ','.join(ix(c) for c in REC_COLS)
        ws.cell(row=r, column=12, value=f'=IF({e},"",IFERROR(_xlfn.TEXTJOIN(", ",TRUE,{rec}),""))')
        ws.cell(row=r, column=13, value=f'=IF(OR({e},G{r}=""),"",G{r}-{DATE})')
        late = f'IF(AND(N(M{r})<0,F{r}<>"Live",F{r}<>"Validated",J{r}<>"Retired"),"Late: ","")'
        ws.cell(row=r, column=14, value=(
            f'=IF({e},"",{late}&IF(J{r}="Retired","Skip: Google retired this rich result. Keep existing markup only if it is accurate",'
            f'IF(F{r}="Not started","Build it in the JSON-LD Builder or your CMS template, with the required properties",'
            f'IF(F{r}="In progress","Test a sample URL in the Rich Results Test before release",'
            f'IF(F{r}="Live","Check the Search Console report after Google recrawls, then mark Validated",'
            f'IF(F{r}="Validated","Monitor the report monthly and recheck values after template changes","Choose a status"))))))'))
    K.style_body(ws, RP_FIRST, RP_LAST, len(head), formula_cols=fc, number_formats={3: '#,##0', 7: 'dd mmm yyyy', 13: '0'}, wrap_cols=(8, 9, 11, 12, 14))
    K.dropdown(ws, f'D{RP_FIRST}:D{RP_LAST}', f'{S}!$A${TR_FIRST}:$A${TR_LAST}')
    K.dropdown(ws, f'F{RP_FIRST}:F{RP_LAST}', LREF['Rollout status'])
    n = f'N{RP_FIRST}:N{RP_LAST}'
    ws.conditional_formatting.add(n, FormulaRule(formula=[f'LEFT(N{RP_FIRST},4)="Late"'], fill=PatternFill('solid', fgColor='F8D7D3'), font=Font(name=K.FONT, bold=True, color='9B2C1F')))
    ws.conditional_formatting.add(n, FormulaRule(formula=[f'LEFT(N{RP_FIRST},4)="Skip"'], fill=PatternFill('solid', fgColor='EEEEEE')))
    ws.conditional_formatting.add(f'F{RP_FIRST}:F{RP_LAST}', CellIsRule(operator='equal', formula=['"Validated"'], fill=PatternFill('solid', fgColor='D9F2C4'), font=Font(name=K.FONT, bold=True)))
    ws.freeze_panes = 'B5'
    ws.auto_filter.ref = f'A4:N{RP_LAST}'
    return ws


def chart(ws, title, ytitle, cat_col, val_cols, r1, r2, anchor, colors, horiz, titles, h=7.5, stacked=False):
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
    ch.height, ch.width = h, 17
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
    for c, w in zip('ABCDEFG', [46, 12, 3, 24, 10, 11, 11]):
        ws.column_dimensions[c].width = w
    m = M
    sc, pr, el = m['Score (0 to 100)'], m['Priority'], m['Rich result eligibility']
    kpis = [
        ('Markup blocks checked', f'=COUNTA({sl("A")})', '0'),
        ('Pages with markup', f'=SUMPRODUCT(({sl("A")}<>"")/COUNTIF({sl("A")},{sl("A")}&""))', '0'),
        ('Average markup score', f'=IFERROR(ROUND(AVERAGE({sl(sc)}),0),0)', '0'),
        ('Blocks eligible for a rich result', f'=COUNTIF({sl(el)},"Eligible*")', '0'),
        ('Blocks missing required properties', f'=COUNTIF({sl(m["All required properties"])},0)', '0'),
        ('Blocks that do not fully match the page', f'=COUNTIF({sl("F")},"No")+COUNTIF({sl("F")},"Partly")', '0'),
        ('Pages blocked for Googlebot', f'=COUNTIF({sl("I")},"Yes")', '0'),
        ('Invalid in the Rich Results Test', f'=COUNTIF({sl("G")},"Invalid")', '0'),
        ('Not tested yet', f'=COUNTIF({sl("G")},"Not tested")', '0'),
        ('Retired rich result types still in use', f'=COUNTIF({sl(m["Google status"])},"Retired")', '0'),
        ('Self serving review markup', f'=COUNTIF({sl(m["Self serving review markup?"])},"Yes")', '0'),
        ('Wrong type for the page', f'=COUNTIF({sl(m["Type fits the page?"])},"No")', '0'),
        ('Not in JSON-LD', f'=COUNTIF({sl("D")},"Microdata")+COUNTIF({sl("D")},"RDFa")', '0'),
        ('Values not checked for over 180 days', f'=COUNTIF({sl(m["Days since checked"])},">"&{FRESH1})', '0'),
        ('Templates validated (Rollout Plan)', f"=COUNTIF('Rollout Plan'!$F${RP_FIRST}:$F${RP_LAST},\"Validated\")&\" of \"&COUNTA('Rollout Plan'!$A${RP_FIRST}:$A${RP_LAST})", '@'),
    ]
    ws['A4'] = 'KEY NUMBERS'
    ws['A4'].font = K.f(10, True, K.DEEP)
    for i, (label, fml, fmt) in enumerate(kpis):
        r = 5 + i
        ws.cell(row=r, column=1, value=label).font = K.f(10)
        c = ws.cell(row=r, column=2, value=fml)
        c.number_format, c.font, c.fill, c.border = fmt, K.f(11, True), K.FORMULA_FILL, K.BORDER
        c.alignment = Alignment(horizontal='right')
    ws['D4'] = 'BY SCHEMA TYPE'
    ws['D4'].font = K.f(10, True, K.DEEP)
    for j, h in enumerate(['Schema type', 'Blocks', 'Avg score', 'Eligible']):
        c = ws.cell(row=5, column=4 + j, value=h)
        c.font, c.fill = K.f(10, True, 'FFFFFF'), K.HEAD_F
    for i in range(NTYPES):
        r = 6 + i
        ws.cell(row=r, column=4, value=f'={S}!A{TR_FIRST + i}')
        ws.cell(row=r, column=5, value=f'=COUNTIF({sl("C")},D{r})')
        ws.cell(row=r, column=6, value=f'=IF(E{r}=0,"",ROUND(AVERAGEIF({sl("C")},D{r},{sl(sc)}),0))')
        ws.cell(row=r, column=7, value=f'=COUNTIFS({sl("C")},D{r},{sl(el)},"Eligible*")')
        for cc in range(4, 8):
            ws.cell(row=r, column=cc).border, ws.cell(row=r, column=cc).fill = K.BORDER, K.FORMULA_FILL
    top = 26
    ws.cell(row=top - 1, column=1, value='MARKUP BLOCKS BY PRIORITY').font = K.f(10, True, K.DEEP)
    for j, h in enumerate(['Priority', 'Blocks']):
        c = ws.cell(row=top, column=1 + j, value=h)
        c.font, c.fill = K.f(10, True, 'FFFFFF'), K.HEAD_F
    for i, p in enumerate(PRIOS):
        r = top + 1 + i
        ws.cell(row=r, column=1, value=p).border = K.BORDER
        c = ws.cell(row=r, column=2, value=f'=COUNTIF({sl(pr)},A{r})')
        c.border, c.fill = K.BORDER, K.FORMULA_FILL
    t2 = top + len(PRIOS) + 3
    ws.cell(row=t2 - 1, column=1, value='BLOCKS FAILING EACH CHECK').font = K.f(10, True, K.DEEP)
    for j, h in enumerate(['Check', 'Blocks to fix', 'Partly']):
        c = ws.cell(row=t2, column=1 + j, value=h)
        c.font, c.fill = K.f(10, True, 'FFFFFF'), K.HEAD_F
    for i, col in enumerate(CK):
        r = t2 + 1 + i
        ws.cell(row=r, column=1, value=f'={S}!A{CHK_ROW + i}').border = K.BORDER
        for cc, val in ((2, 0), (3, 0.5)):
            c = ws.cell(row=r, column=cc, value=f'=COUNTIF({sl(col)},{val})')
            c.border, c.fill = K.BORDER, K.FORMULA_FILL
    ws.conditional_formatting.add(f'B{t2 + 1}:B{t2 + NCH}', ColorScaleRule(start_type='num', start_value=0, start_color='FFFFFF', end_type='num', end_value=5, end_color='E07A5F'))
    chart(ws, 'Markup blocks by priority', 'Blocks', 1, [2], top + 1, top + len(PRIOS), 'I4', [K.GREEN], True, False, h=9)
    chart(ws, 'Blocks failing each check', 'Blocks', 1, [2, 3], t2 + 1, t2 + NCH, 'I24', ['E07A5F', 'F2C94C'], True, True, h=10, stacked=True)
    return ws


def build(path, asset, url):
    wb = K.new_book()
    lab_sheet(wb)
    builder_sheet(wb)
    rollout_sheet(wb)
    dashboard_sheet(wb)
    settings_sheet(wb)
    K.prompts_sheet(wb, asset['prompts'], url)
    K.checklist_sheet(wb, list(asset['checklist']))
    K.sources_sheet(wb, asset['sources'], [
        ('Demo data', 'BrewNest and every page in the demo are fictional (.example domain). All markup, test results, dates, prices and impressions are illustrative, not real data.', ''),
        ('Score', 'Weighted share of the 11 checks a markup block passes (pass 1, partly 0.5, fix 0). Checks without data are left out. Weights, coverage bands, the freshness rule and grade bands live on Settings and are assumptions to tune.', ''),
        ('Type Rules', 'Required and recommended properties per type are taken from the Google Search Central structured data docs for each feature (read November 2026). Google changes these docs, so check the doc for a type before a big rollout. Person has no rich result of its own.', 'https://developers.google.com/search/docs/appearance/structured-data/search-gallery'),
        ('Retired rich results', 'FAQ rich results stopped appearing in Google Search on 7 May 2026 and the documentation was removed in June 2026. How to rich results stopped on mobile in August 2023 and on desktop in September 2023. ClaimReview was among the features Google phased out in 2025.', 'https://developers.google.com/search/updates'),
        ('AI features', 'Google says there is no special schema.org structured data needed to appear in AI Overviews or AI Mode, and lists making sure structured data matches the visible text as a best practice.', 'https://developers.google.com/search/docs/appearance/ai-features'),
        ('Eligibility', 'Eligible means the block meets the checks in this workbook. Google does not guarantee that structured data will show up in search results, even when it is correct.', 'https://developers.google.com/search/docs/appearance/structured-data/sd-policies'),
    ])
    K.start_here(
        wb, 'Schema Markup Kit',
        [
            'This workbook audits every structured data block on your site against Google rules: the required and recommended properties for 17 types, whether the markup matches the visible page, the Rich Results Test, Search Console, blocked pages, wrong types, self serving reviews, JSON-LD and stale values. It also flags retired rich results such as FAQ and How to, so you stop spending time on them.',
            f'The JSON-LD Builder writes copy and paste markup for 9 types from plain form fields. It ships with demo data for a fictional coffee roastery ({len(P)} markup blocks and {len(PLAN)} rollout rows) so you can see every check working.',
        ],
        [
            ('Schema Lab', 'One row per markup block with 500 ready rows: type, format, properties, matches page, test results, blocked, last checked, plus 12 measures, 11 checks, score, grade, fixes, eligibility and priority.'),
            ('JSON-LD Builder', 'Fill plain fields and copy ready JSON-LD for Article or BlogPosting, Product, Organization, LocalBusiness, BreadcrumbList, VideoObject, Event, ProfilePage and WebSite.'),
            ('Rollout Plan', 'One row per template and type: what Google can show, required and recommended properties, status, target date and the next step.'),
            ('Dashboard', 'Key numbers, results by schema type, blocks by priority and blocks failing each check, with two charts.'),
            ('Settings', 'Analysis date, coverage and freshness rules, the 11 check weights with rules and fixes, the Type Rules table and lists.'),
            ('AI Prompts', 'Prompts for ChatGPT, Claude or Gemini to write, audit and fix structured data.'),
            ('Checklist', 'The schema markup checklist as a tick list with automatic progress.'),
            ('Sources', 'Where facts come from and which numbers are assumptions.'),
        ],
        [
            'Look at the demo on Schema Lab, JSON-LD Builder, Rollout Plan and the Dashboard, then clear the yellow demo cells.',
            'On Settings, set the analysis date. Check the Type Rules for the types you use, and add any type you need in the empty rows.',
            'List your page templates on Rollout Plan with the schema type each one needs.',
            'For each template, test one live URL in the Rich Results Test. Add a Schema Lab row per markup block with the property names from the test or the page source.',
            'Compare each marked up value with the visible page, choose Matches, and add the test result, the Search Console report and whether the page is blocked.',
            'Sort by Priority. Fix blocked pages, mismatches and missing required properties first. Build new markup on the JSON-LD Builder.',
            'After release, check the Search Console reports, update the Rollout Plan and recheck values after every template change.',
        ],
        url,
    )
    order = ['Start Here', 'Schema Lab', 'JSON-LD Builder', 'Rollout Plan', 'Dashboard', 'Settings', 'AI Prompts', 'Checklist', 'Sources']
    wb._sheets = [wb[n] for n in order]
    wb.active = 0
    for ws in wb.worksheets:
        ws.sheet_properties.tabColor = K.GREEN if ws.title in order[:5] else 'A6EF39'
    wb.save(path)


PREVIEW = {'sheet': 'Schema Lab', 'header_row': 4, 'rows': 12,
           'cols': [1, 3, NIN + 6, NIN + 8, SC, SC + 1, SC + 4, SC + 5],
           'formula_idx': [2, 3, 4, 5, 6, 7]}


def check(wb):
    """Assert the worked examples used in the guide and that every builder output is valid JSON."""
    a = wb['Schema Lab']
    v = lambda h, r: a[f'{M[h]}{r}'].value
    r = 11   # kalimpong light roast
    assert a[f'A{r}'].value.endswith('/shop/kalimpong-light-roast/')
    assert v('Required missing', r) == 0 and v('Required properties', r) == 3 and v('Recommended present', r) == 2 and abs(v('Recommended coverage', r) - 0.4) < 1e-9, (v('Required properties', r), v('Recommended present', r))
    assert v('Missing recommended (list)', r) == 'aggregateRating, review, offers.availability', v('Missing recommended (list)', r)
    assert v('Days since checked', r) == 257 and v('Score (0 to 100)', r) == 72 and v('Grade', r) == 'B' and v('Fixes needed', r) == 4, (v('Days since checked', r), v('Score (0 to 100)', r))
    assert v('Fixes in priority order', r) == 'Enough recommended properties (partly); Matches the visible page; Search Console status (partly); Values up to date (partly)', v('Fixes in priority order', r)
    assert v('Priority', r) == 'Fix now: markup does not match the page' and v('Rich result eligibility', r) == 'No: does not match the page', v('Priority', r)
    assert v('Missing required (list)', 12) == 'one of offers, review, aggregateRating' and v('Priority', 12) == 'Fix now: required properties missing', v('Missing required (list)', 12)
    assert v('Type fits the page?', 13) == 'No' and v('Priority', 13) == 'Fix: wrong type for this page', v('Priority', 13)
    assert v('Self serving review markup?', 5) == 'Yes' and v('Priority', 5) == 'Fix now: self serving review markup', v('Priority', 5)
    assert v('Rich result eligibility', 5) == 'Details only: no review stars for self serving reviews', v('Rich result eligibility', 5)
    assert v('Missing required (list)', 15) == 'location.address' and v('Missing required (list)', 16) == 'uploadDate', (v('Missing required (list)', 15), v('Missing required (list)', 16))
    assert v('Priority', 17) == 'Low priority: rich result retired' and v('Priority', 18) == 'Low priority: rich result retired' and v('All required properties', 17) is None, v('Priority', 17)
    assert v('Priority', 19) == 'Fix now: blocked for Googlebot', v('Priority', 19)
    assert v('Priority', 10) == 'Healthy: monitor' and v('Rich result eligibility', 10) == 'Eligible (Google does not guarantee it)', v('Priority', 10)
    assert v('Missing recommended (list)', 7) == 'dateModified, author.name, author.url' and v('Priority', 7) == 'Improve: add recommended properties', (v('Missing recommended (list)', 7), v('Priority', 7))
    assert v('Google result', 6) == 'Site name shown in results' and v('Required missing', 6) == 0
    d = wb['Dashboard']
    kp = {d.cell(row=r, column=1).value: d.cell(row=r, column=2).value for r in range(5, 20)}
    assert kp['Markup blocks checked'] == 15 and kp['Pages with markup'] == 13 and kp['Retired rich result types still in use'] == 2, kp
    assert kp['Blocks missing required properties'] == 3 and kp['Pages blocked for Googlebot'] == 1, kp
    b = wb['JSON-LD Builder']
    for key, (oc, cc) in BUILD_OUT.items():
        s = b[oc].value
        assert s.startswith('<script type="application/ld+json">') and s.endswith('</script>'), (key, s[:80])
        data = json.loads(s[len('<script type="application/ld+json">'):-len('</script>')])
        assert data['@context'] == 'https://schema.org', key
        assert b[cc].value.startswith('Ready to paste'), (key, b[cc].value)
        if key == 'product':
            assert data['offers']['price'] == 549 and data['offers']['availability'] == 'https://schema.org/InStock' and data['aggregateRating']['reviewCount'] == 38, data
        if key == 'crumbs':
            assert len(data['itemListElement']) == 3 and 'item' not in data['itemListElement'][2], data
        if key == 'local':
            assert data['@type'] == 'CafeOrCoffeeShop' and data['openingHoursSpecification'][1]['dayOfWeek'] == ['Saturday', 'Sunday'], data
        if key == 'event':
            assert data['location']['address']['addressLocality'] == 'Pune' and data['eventStatus'] == 'https://schema.org/EventScheduled', data
        if key == 'article':
            assert data['author'][0]['name'] == 'Anika Rao' and len(data['image']) == 2, data
