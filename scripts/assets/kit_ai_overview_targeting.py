"""AI Overview Optimization Kit workbook (asset 17, AI Overview targeting).

Query Tracker: one row per target query (500 rows) with demand, value, organic position, whether an AI Overview
shows, whether you are cited, sources cited, competitors cited, AI Mode check and Search Console numbers. The sheet
pulls the target page's readiness and eligibility from the Page Audit, works out fan out coverage, a status, the next
action, an opportunity score (0 to 100), a priority and when to check the results page again.
Page Audit: one row per page (300 rows) with 13 typed checks plus an automatic fan out check, three of them gates
(indexed, snippet allowed, crawlable). It scores readiness 0 to 100, names the biggest gap, counts fixes and hours.
Fan Out Map: the sub questions behind each query and whether the page covers them. Action Plan: fixes by week with
a before and after measure from the Search Console generative AI performance report. Dashboard sums it all up.
"""
import datetime
from openpyxl.styles import PatternFill, Font, Alignment
from openpyxl.formatting.rule import CellIsRule, ColorScaleRule, FormulaRule
from openpyxl.chart import BarChart, Reference
from openpyxl.utils import get_column_letter as L
import kitlib as K

QT_FIRST, QT_LAST = 5, 504     # Query Tracker (500 rows)
PA_FIRST, PA_LAST = 5, 304     # Page Audit (300 rows)
FO_FIRST, FO_LAST = 5, 504     # Fan Out Map (500 rows)
AP_FIRST, AP_LAST = 5, 154     # Action Plan (150 rows)
S = 'Settings'
QTS, PAS, FOS, APS = "'Query Tracker'", "'Page Audit'", "'Fan Out Map'", "'Action Plan'"

(DATE, FULL, RECHECK, P1, P2, P3, READY, FANOK, FANPART, MEASURE, HOURS) = (f'{S}!$B${r}' for r in range(5, 16))
W_DEM, W_VAL, W_AIO, W_POS, W_GAP = (f'{S}!$G${r}' for r in range(6, 11))
POS_RNG = f'{S}!$F$14:$G$19'
AIO_RNG = f'{S}!$F$23:$G$26'
CHK_FIRST = 6
CHK_RNG = f'{S}!$J${CHK_FIRST}:$N${CHK_FIRST + 13}'
ST_RNG = f'{S}!$J$24:$K$31'

WEIGHTS = [('Demand (monthly searches)', 30), ('Business value', 25), ('AI Overview shows', 15), ('Position band', 15), ('Readiness gap', 15)]
POSBANDS = [(0, 1, 'Positions 1 to 3'), (3.5, 0.9, 'Positions 4 to 10'), (10.5, 0.6, 'Page two'), (20.5, 0.3, 'Positions 21 to 50'), (50.5, 0.1, 'Beyond 50'), (999, 0.2, 'Not ranking (blank)')]
AIOF = [('Yes', 1), ('Sometimes', 0.6), ('Not checked', 0.5), ('No', 0.2)]
# check, weight, gate, hours to fix (assumption), how to fix.  Order = Page Audit columns.
CHECKS = [
    ('Indexed in Google', 10, 'Gate', 2, 'Run URL Inspection in Search Console. Fix noindex, canonical or quality problems, then request indexing.'),
    ('Snippet allowed', 8, 'Gate', 1, 'Remove nosnippet, a very low max-snippet or data-nosnippet from the text that answers the query.'),
    ('Googlebot can crawl it', 7, 'Gate', 2, 'Check robots.txt, CDN or firewall rules and login walls. Googlebot must reach the page.'),
    ('Answer first under a clear heading', 10, '', 1, 'Answer the main question in the first 40 to 60 words under a heading that names it.'),
    ('Headings match the sub questions', 7, '', 2, 'Turn the sub questions from the Fan Out Map into descriptive H2 and H3 headings.'),
    ('Original value (data, tests, experience)', 12, '', 6, 'Add something the top results lack: your own data, a test, photos, a worked example or expert input.'),
    ('Covers the fan out sub questions', 8, '', 4, 'Add sections for the sub questions marked No on the Fan Out Map, or link to pages that answer them.'),
    ('Key content is in text', 5, '', 2, 'Put important information in HTML text, not only in images, video or PDFs.'),
    ('Clear author and visible date', 6, '', 1, 'Show who wrote or reviewed it, their experience and a clear Published or Last updated date.'),
    ('Facts checked in the last 12 months', 6, '', 3, 'Check every number, price, rule and link against a current official source.'),
    ('Structured data matches the page', 5, '', 2, 'Make every structured data value match the visible text; fix errors in the Rich Results Test.'),
    ('Good page experience on mobile', 5, '', 6, 'Fix layout shifts, slow loading and intrusive pop ups; check Core Web Vitals in Search Console.'),
    ('Helpful images or video', 4, '', 3, 'Add original images or a short video that support the text, with descriptive alt text.'),
    ('Internal links from related pages', 7, '', 1, 'Link to the page from 2 or more related pages with descriptive anchor text.'),
]
CHK_NAMES = [c[0] for c in CHECKS]
STATUSES = [
    ('Check the results page', 'Search the query in a private window and record whether an AI Overview shows and who is cited.'),
    ('Fix eligibility first', 'The page is not indexed, blocks snippets or cannot be crawled. Fix the gate on the Page Audit before anything else.'),
    ('No AI Overview: classic SEO', 'No AI Overview shows. Work on the classic result: title, snippet and depth. Check again next cycle.'),
    ('Cited: protect and expand', 'You are cited. Keep facts current, cover the sub questions still marked No and add internal links.'),
    ('Ranks top 10, not cited: close the answer gap', 'Add a clear answer first, original value and headings that match the sub questions.'),
    ('Ranks 11 to 30: build depth and fan out coverage', 'Cover the sub questions with their own sections and add original value so the page appears for fan out searches.'),
    ('Not ranking: build a stronger page', 'Consider a dedicated page or a much deeper section. Check search intent first.'),
    ('Add a target page', 'Choose the page that should answer this query and audit it on the Page Audit.'),
]
INTENTS = ['Informational', 'Commercial', 'Transactional', 'Navigational']
AIO = ['Yes', 'Sometimes', 'No', 'Not checked']
YNC = ['Yes', 'No', 'Not checked']
YPN = ['Yes', 'Partly', 'No', 'Not checked']
SUBTYPE = ['Definition', 'How to', 'Comparison', 'Cost or price', 'Problem or fix', 'Example', 'Safety or risk', 'Next step']
FOUND = ['AI Overview text', 'AI Mode follow up', 'People also ask', 'Search Console query', 'Customer question', 'Related searches']
OWNERS = ['Nisha (editor)', 'Kabir (writer)', 'SEO', 'Developer', 'Plant expert']
WEEKS = [f'Week {i}' for i in range(1, 9)]
ASTAT = ['To do', 'Doing', 'Done']
PTYPES = ['Guide', 'List', 'How to', 'Product category', 'Product page', 'Comparison', 'FAQ page', 'Glossary']

# Demo: Sproutly, a fictional indoor plant and gardening shop with a guides section (sproutly.example). Illustrative numbers.
U = 'https://sproutly.example'
# url, title, type, main query, 13 typed checks (order of CHECKS without the fan out check), ai impressions, search impressions, audited, notes
YP, PT, NO, NC = 'Yes', 'Partly', 'No', 'Not checked'
PAGES = [
    ('/guides/succulent-watering/', 'How often to water succulents', 'Guide', 'how often to water succulents', [YP, YP, YP, NO, PT, NO, YP, PT, YP, YP, YP, YP, PT], 9200, 41000, '2026-11-18', 'Worked example in the guide'),
    ('/guides/monstera-care/', 'Monstera care guide', 'Guide', 'monstera care', [YP, YP, YP, YP, YP, YP, YP, YP, YP, YP, YP, YP, YP], 21000, 72000, '2026-11-18', 'Cited for the main query'),
    ('/guides/repotting-plants/', 'How to repot a plant', 'How to', 'how to repot a plant', [YP, YP, YP, YP, NO, PT, YP, NO, PT, YP, PT, YP, YP], 2100, 30000, '2026-11-19', ''),
    ('/guides/best-low-light-plants/', 'Best low light indoor plants', 'List', 'best low light plants', [YP, YP, YP, YP, YP, PT, YP, YP, PT, YP, YP, YP, YP], 7400, 58000, '2026-11-19', 'Answer first added in October'),
    ('/guides/fungus-gnats/', 'How to get rid of fungus gnats', 'How to', 'how to get rid of fungus gnats', [YP, YP, YP, YP, YP, YP, YP, YP, YP, YP, PT, YP, YP], 12500, 39000, '2026-11-20', ''),
    ('/guides/potting-mix-guide/', 'Potting mix explained', 'Guide', 'potting mix for indoor plants', [YP, YP, YP, PT, PT, NO, YP, NO, NO, NO, YP, NO, PT], 600, 21000, '2026-11-20', ''),
    ('/products/self-watering-pots/', 'Self watering pots', 'Product category', 'self watering pots', [YP, YP, YP, NO, NO, NO, PT, NO, NC, YP, PT, YP, YP], 300, 26000, '2026-11-21', 'Product category page'),
    ('/guides/yellow-leaves/', 'Why are my plant leaves turning yellow?', 'Guide', 'why are my plant leaves turning yellow', [YP, NO, YP, YP, YP, YP, YP, YP, YP, YP, YP, YP, YP], 0, 64000, '2026-11-21', 'nosnippet added by mistake in a theme update'),
    ('/guides/balcony-vegetable-garden/', 'Balcony vegetable garden for beginners', 'Guide', 'balcony vegetable garden', [YP, YP, YP, PT, NO, PT, YP, PT, YP, NC, NO, YP, NO], 400, 12000, '2026-11-22', ''),
    ('/guides/pet-safe-plants/', 'Pet safe houseplants', 'List', 'pet safe houseplants', [YP, YP, YP, YP, PT, NO, YP, YP, NO, YP, YP, YP, PT], 1800, 24000, '2026-11-22', 'Needs a vet reviewed source list'),
]
# query, page index, topic, intent, searches, value, position, aio, cited, sources, competitors, ai mode, clicks, impressions, checked
QUERIES = [
    ('how often to water succulents', 0, 'Succulents', 'Informational', 4400, 2, 4.2, 'Yes', 'No', 7, 'Two gardening magazines, a university extension page', 'No', 610, 38000, '2026-11-18'),
    ('succulent watering schedule', 0, 'Succulents', 'Informational', 900, 2, 6.5, 'Yes', 'No', 6, 'A forum thread, a plant shop', 'Not checked', 70, 6100, '2026-11-18'),
    ('monstera care', 1, 'Monstera', 'Informational', 6600, 2, 8.1, 'Yes', 'Yes', 9, 'Two plant blogs, a magazine', 'Yes', 980, 52000, '2026-11-18'),
    ('how to repot a plant', 2, 'Repotting', 'Informational', 2900, 2, 12.4, 'Yes', 'No', 8, 'A video, two plant blogs', 'No', 140, 19000, '2026-11-19'),
    ('best low light plants', 3, 'Low light', 'Commercial', 5400, 3, 5.3, 'Sometimes', 'No', 6, 'Two magazines, a plant shop', 'Not checked', 890, 41000, '2026-11-19'),
    ('low light plants for bedroom', 3, 'Low light', 'Commercial', 1300, 3, 9.0, 'Yes', 'No', 7, 'A home decor site, a plant shop', 'No', 120, 12000, '2026-11-19'),
    ('how to get rid of fungus gnats', 4, 'Pests', 'Informational', 3600, 2, 3.1, 'Yes', 'Yes', 8, 'A university extension page, a pest control site', 'Yes', 720, 30000, '2026-11-20'),
    ('potting mix for indoor plants', 5, 'Soil', 'Commercial', 1600, 3, 15.2, 'No', 'No', 0, '', 'Not checked', 90, 14000, '2026-11-20'),
    ('self watering pots', 6, 'Pots', 'Transactional', 2400, 3, 7.7, 'No', 'No', 0, '', 'Not checked', 410, 21000, '2026-11-21'),
    ('do self watering pots work', 6, 'Pots', 'Informational', 700, 3, 18.5, 'Yes', 'No', 6, 'A review site, a forum thread', 'No', 15, 4800, '2026-11-21'),
    ('why are my plant leaves turning yellow', 7, 'Plant problems', 'Informational', 8100, 2, 6.0, 'Yes', 'No', 8, 'Two plant blogs, a university extension page', 'No', 1200, 58000, '2026-11-21'),
    ('yellow leaves on monstera', 7, 'Plant problems', 'Informational', 1000, 2, 11.0, 'Yes', 'No', 7, 'Two plant blogs', 'No', 60, 6000, '2026-11-21'),
    ('balcony vegetable garden', 8, 'Edibles', 'Informational', 1900, 2, 24.0, 'Yes', 'No', 7, 'A magazine, a government horticulture page', 'No', 40, 7800, '2026-11-22'),
    ('easy vegetables to grow in pots', 8, 'Edibles', 'Informational', 2400, 2, 31.0, 'Yes', 'No', 9, 'Three gardening sites', 'No', 10, 4200, '2026-11-22'),
    ('pet safe houseplants', 9, 'Pets', 'Commercial', 2200, 3, 4.8, 'Yes', 'No', 8, 'An animal welfare charity, a vet clinic', 'No', 420, 20000, '2026-11-22'),
    ('are snake plants safe for cats', 9, 'Pets', 'Informational', 1500, 2, None, 'Not checked', 'Not checked', None, '', 'Not checked', 0, 0, ''),
    ('how to water a monstera', 1, 'Monstera', 'Informational', 1200, 2, 5.5, 'Yes', 'No', 6, 'Two plant blogs', 'No', 160, 9000, '2026-11-18'),
    ('best soil for succulents', 5, 'Soil', 'Commercial', 1100, 3, 9.8, 'Sometimes', 'No', 5, 'A plant shop, a forum thread', 'Not checked', 85, 7000, '2026-11-20'),
]
# query index, sub question, type, found in, covered, heading on the page
FANOUT = [
    (0, 'How often to water succulents in summer', 'How to', 'AI Overview text', 'Yes', 'Watering in summer'),
    (0, 'How often to water succulents in winter', 'How to', 'AI Overview text', 'Yes', 'Watering in winter'),
    (0, 'How to tell if a succulent needs water', 'Problem or fix', 'People also ask', 'Partly', 'Signs of thirst'),
    (0, 'Signs of overwatering succulents', 'Problem or fix', 'People also ask', 'No', ''),
    (0, 'Best way to water succulents indoors', 'How to', 'AI Mode follow up', 'No', ''),
    (0, 'Do succulents need drainage holes', 'Problem or fix', 'Customer question', 'No', ''),
    (1, 'Watering schedule by season', 'Example', 'Search Console query', 'No', ''),
    (1, 'Watering schedule for small pots', 'Example', 'Customer question', 'Yes', 'Small pots'),
    (2, 'How much light does a monstera need', 'How to', 'AI Overview text', 'Yes', 'Light'),
    (2, 'How often to water a monstera', 'How to', 'People also ask', 'Yes', 'Watering'),
    (2, 'Why is my monstera not splitting', 'Problem or fix', 'People also ask', 'Yes', 'Leaf splits'),
    (2, 'Monstera soil mix', 'How to', 'AI Mode follow up', 'Partly', 'Soil'),
    (3, 'When to repot a plant', 'How to', 'AI Overview text', 'Yes', 'When to repot'),
    (3, 'What size pot to choose', 'How to', 'People also ask', 'No', ''),
    (3, 'Should you water after repotting', 'Next step', 'People also ask', 'No', ''),
    (3, 'How to repot without killing the plant', 'Safety or risk', 'AI Mode follow up', 'Partly', 'Steps'),
    (4, 'Best low light plants for beginners', 'Comparison', 'AI Overview text', 'Yes', 'Easy picks'),
    (4, 'Low light plants that are pet safe', 'Safety or risk', 'People also ask', 'Partly', 'Notes'),
    (4, 'Can plants grow without sunlight', 'Definition', 'People also ask', 'Yes', 'What low light means'),
    (6, 'What causes fungus gnats', 'Definition', 'AI Overview text', 'Yes', 'Why they appear'),
    (6, 'Do sticky traps work for fungus gnats', 'Comparison', 'People also ask', 'Yes', 'Traps'),
    (6, 'How long to get rid of fungus gnats', 'How to', 'AI Mode follow up', 'Yes', 'How long it takes'),
    (10, 'Yellow leaves from overwatering', 'Problem or fix', 'AI Overview text', 'Yes', 'Too much water'),
    (10, 'Yellow leaves from too little light', 'Problem or fix', 'People also ask', 'Yes', 'Light'),
    (10, 'Should I cut off yellow leaves', 'Next step', 'People also ask', 'Yes', 'Pruning'),
    (10, 'Yellow leaves from nutrient deficiency', 'Problem or fix', 'AI Mode follow up', 'Partly', 'Feeding'),
    (12, 'Best vegetables for a balcony', 'Comparison', 'AI Overview text', 'Partly', 'What to grow'),
    (12, 'How much sun a balcony garden needs', 'How to', 'People also ask', 'No', ''),
    (12, 'Container size for vegetables', 'How to', 'AI Mode follow up', 'No', ''),
    (14, 'Which houseplants are toxic to cats', 'Safety or risk', 'AI Overview text', 'Partly', 'Plants to avoid'),
    (14, 'Pet safe plants for low light', 'Comparison', 'People also ask', 'Yes', 'Low light picks'),
    (14, 'What to do if a pet eats a plant', 'Next step', 'Customer question', 'No', ''),
]
# page index, fix (check name), owner, week, status, done on, ai impr before, after, cited before, after
ACTIONS = [
    (0, 'Answer first under a clear heading', 'Kabir (writer)', 'Week 1', 'To do', None, None, None, 'No', None),
    (0, 'Original value (data, tests, experience)', 'Plant expert', 'Week 2', 'To do', None, None, None, 'No', None),
    (7, 'Snippet allowed', 'Developer', 'Week 1', 'Done', '2026-11-12', 0, None, 'No', None),
    (4, 'Facts checked in the last 12 months', 'Nisha (editor)', None, 'Done', '2026-10-01', 5200, 6900, 'Yes', 'Yes'),
    (3, 'Answer first under a clear heading', 'Kabir (writer)', None, 'Done', '2026-10-15', 3100, 4800, 'No', 'Yes'),
    (2, 'Headings match the sub questions', 'Kabir (writer)', 'Week 2', 'Doing', None, None, None, 'No', None),
    (8, 'Covers the fan out sub questions', 'Kabir (writer)', 'Week 3', 'To do', None, None, None, 'No', None),
    (5, 'Internal links from related pages', 'SEO', None, 'Done', '2026-10-20', 900, 870, 'No', 'No'),
]

QT_IN = ['Query', 'Target URL', 'Topic', 'Search intent', 'Monthly searches', 'Business value (1 to 3)', 'Organic position',
         'AI Overview shows?', 'Cited in the AI Overview?', 'Sources cited in the overview', 'Who is cited instead', 'AI Mode cites you?',
         'Clicks (28 days)', 'Impressions (28 days)', 'Date checked', 'Notes']
QT_FH = ['CTR', 'Page readiness (0 to 100)', 'Page eligibility', 'Fan out sub questions', 'Fan out coverage', 'Status', 'Next action',
         'Opportunity score (0 to 100)', 'Priority', 'Days since checked', 'Check again?', 'Rank (helper)']
QT_HEAD = QT_IN + QT_FH
QC = {h: L(i + 1) for i, h in enumerate(QT_HEAD)}
QT_F = tuple(range(len(QT_IN) + 1, len(QT_HEAD) + 1))
TYPED = [c for c in CHK_NAMES if c != 'Covers the fan out sub questions']
PA_IN = ['URL', 'Page title', 'Page type', 'Main query'] + TYPED + ['AI feature impressions (28 days)', 'Search impressions (28 days)', 'Last audited', 'Notes']
PA_FH = ['Fan out sub questions', 'Fan out coverage', 'Covers the fan out sub questions', 'Eligibility', 'Readiness score (0 to 100)',
         'Readiness', 'Biggest gap', 'Fixes left', 'Hours to fix (assumption)', 'AI share of impressions', 'Queries targeting this page']
GAPS = [f'Gap: {i + 1}' for i in range(len(CHECKS))]
PA_HEAD = PA_IN + PA_FH + GAPS
PC = {h: L(i + 1) for i, h in enumerate(PA_HEAD)}
PA_F = tuple(range(len(PA_IN) + 1, len(PA_HEAD) + 1))
CHK_COL = {name: PC[name] for name in CHK_NAMES}


def qt(h):
    c = QC.get(h, h)
    return f'{QTS}!${c}${QT_FIRST}:${c}${QT_LAST}'


def pa(h):
    c = PC.get(h, h)
    return f'{PAS}!${c}${PA_FIRST}:${c}${PA_LAST}'


def fo(c):
    return f'{FOS}!${c}${FO_FIRST}:${c}${FO_LAST}'


def d(s):
    return datetime.date.fromisoformat(s) if s else None


def settings_sheet(wb):
    ws = wb.create_sheet(S)
    ws.sheet_view.showGridLines = False
    K.title_block(ws, 'Settings', 'Every rule, weight and list used by this workbook. Change a blue value and every score, status and priority updates.')
    for c, w in zip('ABCDEFGHIJKLMNOPQRSTUVW', [52, 16, 3, 3, 3, 26, 10, 22, 3, 42, 9, 8, 9, 70, 3, 16, 22, 18, 16, 12, 10, 16, 10]):
        ws.column_dimensions[c].width = w
    rows = [
        (4, 'RULES', None, None),
        (5, 'Today (set it to the day you review the sheet)', datetime.date(2026, 11, 25), 'dd mmm yyyy'),
        (6, 'Monthly searches that earn full demand marks', 5000, '#,##0'),
        (7, 'Check each results page again after (days)', 30, '0'),
        (8, 'P1: work on it now when the score is at least', 70, '0'),
        (9, 'P2: this month when at least', 50, '0'),
        (10, 'P3: this quarter when at least (below = P4: later)', 30, '0'),
        (11, 'Ready: readiness score at least', 80, '0'),
        (12, 'Fan out check is Yes when coverage is at least', 0.8, '0%'),
        (13, 'Fan out check is Partly when coverage is at least', 0.5, '0%'),
        (14, 'Measure results this many days after a fix', 28, '0'),
        (15, 'Fix hours available per week', 10, '0'),
    ]
    for r, label, val, fmt in rows:
        a = ws.cell(row=r, column=1, value=label)
        a.font = K.f(10, val is None, K.DEEP if val is None else K.INK)
        if val is not None:
            c = ws.cell(row=r, column=2, value=val)
            c.border, c.fill = K.BORDER, K.INPUT_FILL
            c.font = K.f(10, True, '0000FF')
            c.number_format = fmt
    ws['A17'] = ('Readiness score = the sum of each check weight x its value (Yes 1, Partly 0.5, No or Not checked 0). Opportunity score = '
                 'demand weight x MIN(1, searches / full marks) + value weight x value / 3 + AI Overview weight x AI Overview factor + position '
                 'weight x position band factor + gap weight x (1 minus readiness / 100). Google says there are no extra requirements and no '
                 'special optimizations for AI Overviews or AI Mode, so these checks are ordinary SEO basics, weighted for answer pages. Every '
                 'weight, band, factor and hour on this tab is an assumption of this kit for you to tune.')
    ws['A17'].font = K.f(9, False, '777777', True)
    ws['A17'].alignment = Alignment(wrap_text=True, vertical='top')
    ws.merge_cells('A17:B30')

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
    table(6, 5, 'OPPORTUNITY WEIGHTS (add up to 100)', ['Factor', 'Weight'], WEIGHTS)
    ws['F11'] = 'Total'
    ws['G11'] = '=SUM(G6:G10)'
    ws['G11'].fill, ws['G11'].font = K.FORMULA_FILL, K.f(10, True)
    table(6, 13, 'POSITION BAND (organic position)', ['At least', 'Factor', 'Meaning'], POSBANDS, ['0.0', '0.0', '@'])
    table(6, 22, 'AI OVERVIEW FACTOR', ['AI Overview shows?', 'Factor'], AIOF, ['@', '0.0'])
    table(10, 5, 'PAGE CHECKS (weights add up to 100; hours are assumptions)', ['Check', 'Weight', 'Gate?', 'Hours', 'How to fix'], CHECKS, ['@', '0', '@', '0', '@'], blue=(1, 3))
    ws['K20'] = '=SUM(K6:K19)'
    ws['J20'] = 'Total weight'
    ws['K20'].fill, ws['K20'].font = K.FORMULA_FILL, K.f(10, True)
    for r in range(6, 20):
        ws.row_dimensions[r].height = 30
    table(10, 23, 'STATUS AND NEXT ACTION (query level)', ['Status', 'Next action'], STATUSES, blue=())
    for i in range(len(STATUSES)):
        ws.merge_cells(start_row=24 + i, start_column=11, end_row=24 + i, end_column=14)
        ws.row_dimensions[24 + i].height = 30
    ws.merge_cells('K23:N23')
    lists = [('P', 'Search intent', INTENTS), ('Q', 'AI Overview shows?', AIO), ('R', 'Yes, No, Not checked', YNC), ('S', 'Yes, Partly, No', YPN),
             ('T', 'Sub question type', SUBTYPE), ('U', 'Found in', FOUND), ('V', 'Owner', OWNERS), ('W', 'Week', WEEKS)]
    ws['P33'] = 'LISTS (used by the dropdowns)'
    ws['P33'].font = K.f(10, True, K.DEEP)
    for col, head, vals in lists:
        ws[f'{col}34'] = head
        ws[f'{col}34'].font = K.f(9, True, '555555')
        n = 12 if col in 'V' else len(vals)
        for i in range(n):
            c = ws[f'{col}{35 + i}']
            c.value = vals[i] if i < len(vals) else None
            c.fill, c.border, c.font = K.INPUT_FILL, K.BORDER, K.f(10)
    ws['P48'] = 'Action status'
    ws['P48'].font = K.f(9, True, '555555')
    for i, v in enumerate(ASTAT):
        c = ws[f'P{49 + i}']
        c.value, c.fill, c.border, c.font = v, K.INPUT_FILL, K.BORDER, K.f(10)
    ws['Q48'] = 'Page type'
    ws['Q48'].font = K.f(9, True, '555555')
    for i, v in enumerate(PTYPES):
        c = ws[f'Q{49 + i}']
        c.value, c.fill, c.border, c.font = v, K.INPUT_FILL, K.BORDER, K.f(10)
    return ws


def val(cell):
    return f'IF({cell}="Yes",1,IF({cell}="Partly",0.5,0))'


def audit_sheet(wb):
    ws = wb.create_sheet('Page Audit')
    ws.sheet_view.showGridLines = False
    K.title_block(ws, 'Page audit', f'One row per page. Rows 5 to {4 + len(PAGES)} are DEMO pages for Sproutly, a fictional plant shop (illustrative numbers). Replace them with your own; 300 rows ready.')
    ws['A2'].font = K.f(10, True, 'B45309')
    ws['A3'] = ('Answer each check with Yes, Partly, No or Not checked. The first three are gates: a No there means the page cannot be shown '
                'in AI features with a snippet. AI feature impressions come from the Search Console generative AI performance report.')
    ws['A3'].font = K.f(9, False, '666666', True)
    widths = [36, 30, 13, 28] + [11] * len(TYPED) + [11, 11, 11, 24] + [9, 9, 11, 22, 10, 13, 30, 8, 9, 10, 9] + [6] * len(GAPS)
    K.header_row(ws, 4, PA_HEAD, formula_cols=PA_F, widths=widths)
    c = PC
    fq_url = fo('H')
    gap_cols = [c[g] for g in GAPS]
    for r in range(PA_FIRST, PA_LAST + 1):
        i = r - PA_FIRST
        if i < len(PAGES):
            url, title, typ, q, checks, aii, si, aud, notes = PAGES[i]
            for col, v in enumerate([U + url, title, typ, q] + checks + [aii, si, d(aud), notes], 1):
                if v not in (None, ''):
                    ws.cell(row=r, column=col, value=v)
        e = f'A{r}=""'
        g = lambda h: f'{c[h]}{r}'
        f = {}
        f['Fan out sub questions'] = f'=IF({e},"",COUNTIF({fq_url},A{r}))'
        n = g('Fan out sub questions')
        f['Fan out coverage'] = f'=IF(OR({e},N({n})=0),"",SUMIF({fq_url},A{r},{fo("I")})/{n})'
        cov = g('Fan out coverage')
        f['Covers the fan out sub questions'] = f'=IF({e},"",IF({cov}="","Not checked",IF({cov}>={FANOK},"Yes",IF({cov}>={FANPART},"Partly","No"))))'
        g1, g2, g3 = (CHK_COL[CHK_NAMES[k]] + str(r) for k in range(3))
        f['Eligibility'] = (f'=IF({e},"",IF(OR({g1}="No",{g2}="No",{g3}="No"),"Not eligible",'
                            f'IF(AND({g1}="Yes",{g2}="Yes",{g3}="Yes"),"Eligible","Check the gates")))')
        parts = '+'.join(f'{S}!$K${CHK_FIRST + k}*{val(CHK_COL[name] + str(r))}' for k, name in enumerate(CHK_NAMES))
        f['Readiness score (0 to 100)'] = f'=IF({e},"",ROUND({parts},0))'
        sc = g('Readiness score (0 to 100)')
        f['Readiness'] = (f'=IF({e},"",IF({g("Eligibility")}="Not eligible","Blocked",IF({sc}>={READY},"Ready",IF({sc}>=60,"Nearly ready",'
                          f'IF({sc}>=40,"Needs work","Weak")))))')
        grng = f'{gap_cols[0]}{r}:{gap_cols[-1]}{r}'
        f['Biggest gap'] = f'=IF({e},"",IF(MAX({grng})=0,"None: protect the page",INDEX({S}!$J${CHK_FIRST}:$J${CHK_FIRST + 13},MATCH(MAX({grng}),{grng},0))))'
        f['Fixes left'] = f'=IF({e},"",COUNTIF({grng},">0"))'
        f['Hours to fix (assumption)'] = '=IF({},"",{})'.format(e, '+'.join(f'IF({gc}{r}>0,{S}!$M${CHK_FIRST + k},0)' for k, gc in enumerate(gap_cols)))
        ai_c, si_c = c['AI feature impressions (28 days)'], c['Search impressions (28 days)']
        f['AI share of impressions'] = f'=IF(OR({e},N({si_c}{r})=0),"",N({ai_c}{r})/{si_c}{r})'
        f['Queries targeting this page'] = f'=IF({e},"",COUNTIF({qt("B")},A{r}))'
        for k, name in enumerate(CHK_NAMES):
            f[GAPS[k]] = f'=IF({e},"",{S}!$K${CHK_FIRST + k}*(1-{val(CHK_COL[name] + str(r))}))'
        for h, v in f.items():
            ws[f'{c[h]}{r}'] = v
    idx = lambda h: PA_HEAD.index(h) + 1
    nf = {idx('AI feature impressions (28 days)'): '#,##0', idx('Search impressions (28 days)'): '#,##0', idx('Last audited'): 'dd mmm yyyy',
          idx('Fan out sub questions'): '0', idx('Fan out coverage'): '0%', idx('Readiness score (0 to 100)'): '0', idx('Fixes left'): '0',
          idx('Hours to fix (assumption)'): '0', idx('AI share of impressions'): '0.0%', idx('Queries targeting this page'): '0'}
    for gname in GAPS:
        nf[idx(gname)] = '0.0'
    K.style_body(ws, PA_FIRST, PA_LAST, len(PA_HEAD), formula_cols=PA_F, number_formats=nf,
                 wrap_cols=(1, 2, 4, idx('Notes'), idx('Biggest gap')))
    first_chk, last_chk = L(5), L(4 + len(TYPED))
    K.dropdown(ws, f'{first_chk}{PA_FIRST}:{last_chk}{PA_LAST}', f'{S}!$S$35:$S$38', 'Yes, Partly, No or Not checked.')
    K.dropdown(ws, f'C{PA_FIRST}:C{PA_LAST}', f'{S}!$Q$49:$Q$56')
    for col in (ai_c, si_c):
        K.whole_number(ws, f'{col}{PA_FIRST}:{col}{PA_LAST}', 0, 1000000000, 'A whole number from Search Console.')
    chk_rng = f'{first_chk}{PA_FIRST}:{last_chk}{PA_LAST}'
    for txt, fill, fc in (('Yes', 'D9F2C4', '3D7F12'), ('Partly', 'FFF4CC', '1F1F1F'), ('No', 'F8D7D3', '9B2C1F')):
        ws.conditional_formatting.add(chk_rng, CellIsRule(operator='equal', formula=[f'"{txt}"'], fill=PatternFill('solid', fgColor=fill), font=Font(name=K.FONT, color=fc)))
    fc_ = c['Covers the fan out sub questions']
    for txt, fill, fcol in (('Yes', 'D9F2C4', '3D7F12'), ('Partly', 'FFF4CC', '1F1F1F'), ('No', 'F8D7D3', '9B2C1F')):
        ws.conditional_formatting.add(f'{fc_}{PA_FIRST}:{fc_}{PA_LAST}', CellIsRule(operator='equal', formula=[f'"{txt}"'], fill=PatternFill('solid', fgColor=fill), font=Font(name=K.FONT, bold=True, color=fcol)))
    rc = c['Readiness']
    for txt, fill, fcol in (('Blocked', '9B2C1F', 'FFFFFF'), ('Weak', 'F8D7D3', '9B2C1F'), ('Needs work', 'FCE5CD', '1F1F1F'), ('Nearly ready', 'FFF4CC', '1F1F1F'), ('Ready', 'B7E4A0', '1F1F1F')):
        ws.conditional_formatting.add(f'{rc}{PA_FIRST}:{rc}{PA_LAST}', CellIsRule(operator='equal', formula=[f'"{txt}"'], fill=PatternFill('solid', fgColor=fill), font=Font(name=K.FONT, bold=True, color=fcol)))
    ec = c['Eligibility']
    ws.conditional_formatting.add(f'{ec}{PA_FIRST}:{ec}{PA_LAST}', CellIsRule(operator='equal', formula=['"Not eligible"'], fill=PatternFill('solid', fgColor='9B2C1F'), font=Font(name=K.FONT, bold=True, color='FFFFFF')))
    sc = c['Readiness score (0 to 100)']
    ws.conditional_formatting.add(f'{sc}{PA_FIRST}:{sc}{PA_LAST}', ColorScaleRule(start_type='num', start_value=0, start_color='F8D7D3', mid_type='num', mid_value=60, mid_color='FFF4CC', end_type='num', end_value=100, end_color='8BC34A'))
    for gc in gap_cols:
        ws.column_dimensions[gc].hidden = True
    for r in range(PA_FIRST, PA_FIRST + len(PAGES)):
        ws.row_dimensions[r].height = 30
    ws.freeze_panes = 'B5'
    ws.auto_filter.ref = f'A4:{c["Queries targeting this page"]}{PA_LAST}'
    return ws


def tracker_sheet(wb):
    ws = wb.create_sheet('Query Tracker')
    ws.sheet_view.showGridLines = False
    K.title_block(ws, 'Query tracker', f'One row per query you want AI Overviews to cite you for. Rows 5 to {4 + len(QUERIES)} are DEMO queries for Sproutly, a fictional plant shop (illustrative numbers). 500 rows ready.')
    ws['A2'].font = K.f(10, True, 'B45309')
    ws['A3'] = ('Search each query in a private window. Record whether an AI Overview shows, whether your page is linked in it, how many sources '
                'it cites and who. Clicks and impressions come from the Search Console Performance report filtered by query.')
    ws['A3'].font = K.f(9, False, '666666', True)
    widths = [32, 36, 13, 13, 10, 9, 9, 11, 11, 9, 32, 11, 9, 11, 11, 22, 7, 10, 13, 9, 9, 34, 48, 10, 18, 8, 12, 8]
    K.header_row(ws, 4, QT_HEAD, formula_cols=QT_F, widths=widths)
    c = QC
    for r in range(QT_FIRST, QT_LAST + 1):
        i = r - QT_FIRST
        if i < len(QUERIES):
            q, pi, topic, intent, srch, value, pos, aio, cited, srcs, comp, aim, clk, imp, chk = QUERIES[i]
            for col, v in enumerate([q, U + PAGES[pi][0], topic, intent, srch, value, pos, aio, cited, srcs, comp, aim, clk, imp, d(chk)], 1):
                if v not in (None, ''):
                    ws.cell(row=r, column=col, value=v)
        e = f'A{r}=""'
        g = lambda h: f'{c[h]}{r}'
        m = f'MATCH(B{r},{pa("A")},0)'
        f = {}
        f['CTR'] = f'=IF(OR({e},N(N{r})=0),"",N(M{r})/N{r})'
        f['Page readiness (0 to 100)'] = f'=IF(OR({e},B{r}=""),"",IFERROR(INDEX({pa("Readiness score (0 to 100)")},{m}),"Audit the page"))'
        f['Page eligibility'] = f'=IF(OR({e},B{r}=""),"",IFERROR(INDEX({pa("Eligibility")},{m}),"Audit the page"))'
        f['Fan out sub questions'] = f'=IF({e},"",COUNTIF({fo("A")},A{r}))'
        fn = g('Fan out sub questions')
        f['Fan out coverage'] = f'=IF(OR({e},N({fn})=0),"",SUMIF({fo("A")},A{r},{fo("I")})/{fn})'
        el = g('Page eligibility')
        f['Status'] = (f'=IF({e},"",IF(B{r}="","Add a target page",IF(OR(H{r}="",H{r}="Not checked"),"Check the results page",'
                       f'IF({el}="Not eligible","Fix eligibility first",IF(H{r}="No","No AI Overview: classic SEO",IF(I{r}="Yes","Cited: protect and expand",'
                       f'IF(AND(G{r}<>"",G{r}<=10),"Ranks top 10, not cited: close the answer gap",IF(AND(G{r}<>"",G{r}<=30),"Ranks 11 to 30: build depth and fan out coverage",'
                       f'"Not ranking: build a stronger page"))))))))')
        stv = g('Status')
        f['Next action'] = f'=IF({e},"",IFERROR(VLOOKUP({stv},{ST_RNG},2,FALSE),""))'
        rd = g('Page readiness (0 to 100)')
        pos = f'IF(G{r}="",0.2,VLOOKUP(G{r},{POS_RNG},2,TRUE))'
        f['Opportunity score (0 to 100)'] = (f'=IF({e},"",ROUND({W_DEM}*MIN(1,N(E{r})/{FULL})+{W_VAL}*IF(F{r}="",2,F{r})/3'
                                             f'+{W_AIO}*IFERROR(VLOOKUP(IF(H{r}="","Not checked",H{r}),{AIO_RNG},2,FALSE),0.5)+{W_POS}*{pos}'
                                             f'+{W_GAP}*(1-IF(ISNUMBER({rd}),{rd},0)/100),0))')
        osc = g('Opportunity score (0 to 100)')
        f['Priority'] = (f'=IF({e},"",IF({stv}="Fix eligibility first","P1: fix eligibility",IF(LEFT({stv},5)="Cited","Protect",'
                         f'IF(LEFT({stv},5)="No AI","Classic SEO",IF(OR({stv}="Check the results page",{stv}="Add a target page"),"Check first",'
                         f'IF({osc}>={P1},"P1: now",IF({osc}>={P2},"P2: this month",IF({osc}>={P3},"P3: this quarter","P4: later"))))))))')
        f['Days since checked'] = f'=IF(OR({e},O{r}=""),"",{DATE}-O{r})'
        ds = g('Days since checked')
        f['Check again?'] = f'=IF({e},"",IF(O{r}="","Yes: never checked",IF({ds}>={RECHECK},"Yes","In "&({RECHECK}-{ds})&" days")))'
        pv = g('Priority')
        f['Rank (helper)'] = (f'=IF(OR({e},{pv}="Protect",{pv}="Classic SEO",{pv}="Check first"),"",IF({pv}="P1: fix eligibility",100,0)'
                              f'+{osc}+N(E{r})/10000000-ROW()/100000000)')
        for h, v in f.items():
            ws[f'{c[h]}{r}'] = v
    idx = lambda h: QT_HEAD.index(h) + 1
    nf = {5: '#,##0', 7: '0.0', 10: '0', 13: '#,##0', 14: '#,##0', 15: 'dd mmm yyyy', idx('CTR'): '0.0%', idx('Page readiness (0 to 100)'): '0',
          idx('Fan out sub questions'): '0', idx('Fan out coverage'): '0%', idx('Opportunity score (0 to 100)'): '0', idx('Days since checked'): '0',
          idx('Rank (helper)'): '0.000000'}
    K.style_body(ws, QT_FIRST, QT_LAST, len(QT_HEAD), formula_cols=QT_F, number_formats=nf, wrap_cols=(1, 2, 11, 16, idx('Status'), idx('Next action')))
    K.dropdown(ws, f'B{QT_FIRST}:B{QT_LAST}', pa('A'), 'URLs from the Page Audit tab.')
    K.dropdown(ws, f'D{QT_FIRST}:D{QT_LAST}', f'{S}!$P$35:$P$38')
    K.dropdown(ws, f'F{QT_FIRST}:F{QT_LAST}', '"1,2,3"', '3 close to a sale or lead, 2 builds trust, 1 loosely related.')
    K.dropdown(ws, f'H{QT_FIRST}:H{QT_LAST}', f'{S}!$Q$35:$Q$38', 'Search the query in a private window. Sometimes = it shows on some checks only.')
    K.dropdown(ws, f'I{QT_FIRST}:I{QT_LAST}', f'{S}!$R$35:$R$37', 'Yes only when a link to your page shows inside the AI Overview.')
    K.dropdown(ws, f'L{QT_FIRST}:L{QT_LAST}', f'{S}!$R$35:$R$37')
    for col in 'EJMN':
        K.whole_number(ws, f'{col}{QT_FIRST}:{col}{QT_LAST}', 0, 1000000000, 'A whole number.')
    pc = c['Priority']
    pr = f'{pc}{QT_FIRST}:{pc}{QT_LAST}'
    for start, fill, fc in (('P1', '9B2C1F', 'FFFFFF'), ('P2', 'F8D7D3', '9B2C1F'), ('P3', 'FFF4CC', '1F1F1F'), ('P4', 'EEEEEE', '555555'),
                            ('Pr', 'B7E4A0', '1F1F1F'), ('Cl', 'EEF8E6', '3D7F12'), ('Ch', 'FCE5CD', '1F1F1F')):
        ws.conditional_formatting.add(pr, FormulaRule(formula=[f'LEFT({pc}{QT_FIRST},2)="{start}"'], fill=PatternFill('solid', fgColor=fill), font=Font(name=K.FONT, bold=True, color=fc)))
    sc = c['Status']
    for start, fill, fc in (('Fix', '9B2C1F', 'FFFFFF'), ('Cit', 'B7E4A0', '1F1F1F'), ('Ran', 'FFF4CC', '1F1F1F'), ('Not', 'F8D7D3', '9B2C1F'), ('Che', 'FCE5CD', '1F1F1F')):
        ws.conditional_formatting.add(f'{sc}{QT_FIRST}:{sc}{QT_LAST}', FormulaRule(formula=[f'LEFT({sc}{QT_FIRST},3)="{start}"'], fill=PatternFill('solid', fgColor=fill), font=Font(name=K.FONT, bold=True, color=fc)))
    for col, colr in (('I', None),):
        ws.conditional_formatting.add(f'I{QT_FIRST}:I{QT_LAST}', CellIsRule(operator='equal', formula=['"Yes"'], fill=PatternFill('solid', fgColor='D9F2C4'), font=Font(name=K.FONT, bold=True, color='3D7F12')))
    osc = c['Opportunity score (0 to 100)']
    ws.conditional_formatting.add(f'{osc}{QT_FIRST}:{osc}{QT_LAST}', ColorScaleRule(start_type='num', start_value=0, start_color='FFFFFF', mid_type='num', mid_value=50, mid_color='FFF4CC', end_type='num', end_value=100, end_color='E07A5F'))
    ca = c['Check again?']
    ws.conditional_formatting.add(f'{ca}{QT_FIRST}:{ca}{QT_LAST}', FormulaRule(formula=[f'LEFT({ca}{QT_FIRST},3)="Yes"'], font=Font(name=K.FONT, bold=True, color='9B2C1F')))
    ws.column_dimensions[c['Rank (helper)']].hidden = True
    for r in range(QT_FIRST, QT_FIRST + len(QUERIES)):
        ws.row_dimensions[r].height = 42
    ws.freeze_panes = 'B5'
    ws.auto_filter.ref = f'A4:{L(len(QT_HEAD))}{QT_LAST}'
    return ws


def fanout_sheet(wb):
    ws = wb.create_sheet('Fan Out Map')
    ws.sheet_view.showGridLines = False
    K.title_block(ws, 'Fan out map', 'AI Overviews and AI Mode may run several related searches across subtopics. List the sub questions behind each query and mark whether your page covers them.')
    ws['A3'] = 'Find sub questions in the AI Overview text, AI Mode follow ups, People also ask, related searches, Search Console queries and customer questions.'
    ws['A3'].font = K.f(9, False, '666666', True)
    head = ['Main query', 'Sub question', 'Type', 'Found in', 'Covered on the page?', 'Heading on the page', 'Notes', 'Target URL', 'Points', 'Action', 'Query in tracker?']
    K.header_row(ws, 4, head, formula_cols=(8, 9, 10, 11), widths=[32, 42, 15, 19, 12, 24, 22, 36, 7, 48, 11])
    for r in range(FO_FIRST, FO_LAST + 1):
        i = r - FO_FIRST
        if i < len(FANOUT):
            qi, sq, typ, found, cov, hd = FANOUT[i]
            for col, v in enumerate([QUERIES[qi][0], sq, typ, found, cov, hd], 1):
                if v not in (None, ''):
                    ws.cell(row=r, column=col, value=v)
        e = f'A{r}=""'
        m = f'MATCH(A{r},{qt("A")},0)'
        ws[f'H{r}'] = f'=IF({e},"",IFERROR(INDEX({qt("B")},{m})&"",""))'
        ws[f'I{r}'] = f'=IF(OR({e},B{r}=""),"",IF(E{r}="Yes",1,IF(E{r}="Partly",0.5,0)))'
        ws[f'J{r}'] = (f'=IF(OR({e},B{r}=""),"",IF(E{r}="Yes","Covered: keep it current",IF(E{r}="Partly","Expand the section"&IF(F{r}<>""," "&F{r},"")&" so it answers this fully",'
                       f'IF(E{r}="No","Add a section that answers: "&B{r},"Check the page"))))')
        ws[f'K{r}'] = f'=IF({e},"",IF(ISNUMBER({m}),"Yes","No: add the query"))'
    K.style_body(ws, FO_FIRST, FO_LAST, len(head), formula_cols=(8, 9, 10, 11), number_formats={9: '0.0'}, wrap_cols=(1, 2, 6, 7, 8, 10))
    K.dropdown(ws, f'A{FO_FIRST}:A{FO_LAST}', qt('A'), 'Queries from the Query Tracker.')
    K.dropdown(ws, f'C{FO_FIRST}:C{FO_LAST}', f'{S}!$T$35:$T$42')
    K.dropdown(ws, f'D{FO_FIRST}:D{FO_LAST}', f'{S}!$U$35:$U$40')
    K.dropdown(ws, f'E{FO_FIRST}:E{FO_LAST}', f'{S}!$S$35:$S$38')
    for txt, fill, fc in (('Yes', 'D9F2C4', '3D7F12'), ('Partly', 'FFF4CC', '1F1F1F'), ('No', 'F8D7D3', '9B2C1F')):
        ws.conditional_formatting.add(f'E{FO_FIRST}:E{FO_LAST}', CellIsRule(operator='equal', formula=[f'"{txt}"'], fill=PatternFill('solid', fgColor=fill), font=Font(name=K.FONT, bold=True, color=fc)))
    ws.conditional_formatting.add(f'K{FO_FIRST}:K{FO_LAST}', FormulaRule(formula=[f'LEFT(K{FO_FIRST},2)="No"'], fill=PatternFill('solid', fgColor='F8D7D3'), font=Font(name=K.FONT, bold=True, color='9B2C1F')))
    for r in range(FO_FIRST, FO_FIRST + len(FANOUT)):
        ws.row_dimensions[r].height = 30
    ws.freeze_panes = 'C5'
    ws.auto_filter.ref = f'A4:K{FO_LAST}'
    return ws


def action_sheet(wb):
    ws = wb.create_sheet('Action Plan')
    ws.sheet_view.showGridLines = False
    K.title_block(ws, 'Action plan', 'Plan fixes by week. Pick a page and a fix; the hours and the how to fix text fill in. After a fix, add the date and AI feature impressions for 28 days before and after, from the Search Console generative AI performance report.')
    head = ['Page URL', 'Fix', 'Owner', 'Week', 'Status', 'Done on', 'AI impressions 28 days before', 'AI impressions 28 days after',
            'Cited before?', 'Cited after?', 'Page title', 'Hours (assumption)', 'How to fix', 'Measure on', 'Impression change', 'Result']
    fc = tuple(range(11, 17))
    K.header_row(ws, 4, head, formula_cols=fc, widths=[34, 30, 15, 9, 9, 11, 11, 11, 9, 9, 28, 9, 54, 11, 10, 30])
    chk = f'{S}!$J${CHK_FIRST}:$J${CHK_FIRST + 13}'
    for r in range(AP_FIRST, AP_LAST + 1):
        i = r - AP_FIRST
        if i < len(ACTIONS):
            pi, fix, own, wk, st, done, bef, aft, cb, ca = ACTIONS[i]
            for col, v in enumerate([U + PAGES[pi][0], fix, own, wk, st, d(done), bef, aft, cb, ca], 1):
                if v not in (None, ''):
                    ws.cell(row=r, column=col, value=v)
        e = f'A{r}=""'
        ws[f'K{r}'] = f'=IF({e},"",IFERROR(INDEX({pa("B")},MATCH(A{r},{pa("A")},0))&"","URL not on the Page Audit"))'
        ws[f'L{r}'] = f'=IF(OR({e},B{r}=""),"",IFERROR(INDEX({S}!$M${CHK_FIRST}:$M${CHK_FIRST + 13},MATCH(B{r},{chk},0)),0))'
        ws[f'M{r}'] = f'=IF(OR({e},B{r}=""),"",IFERROR(INDEX({S}!$N${CHK_FIRST}:$N${CHK_FIRST + 13},MATCH(B{r},{chk},0)),""))'
        ws[f'N{r}'] = f'=IF(OR({e},F{r}=""),"",F{r}+{MEASURE})'
        ws[f'O{r}'] = f'=IF(OR({e},N(G{r})=0,H{r}=""),"",(H{r}-G{r})/G{r})'
        ws[f'P{r}'] = (f'=IF({e},"",IF(E{r}<>"Done","Not done yet",IF(F{r}="","Add the done date",IF({DATE}<N{r},"Wait: "&(N{r}-{DATE})&" days left",'
                       f'IF(H{r}="","Add impressions after",IF(AND(I{r}="No",J{r}="Yes"),"Now cited: keep going",IF(O{r}="",IF(N(H{r})>0,"Up: new AI impressions","Flat: give it another cycle"),'
                       f'IF(O{r}>=0.1,"Up "&TEXT(O{r},"0%")&": keep going",IF(O{r}>-0.1,"Flat: give it another cycle","Down: audit the page again")))))))))')
    K.style_body(ws, AP_FIRST, AP_LAST, len(head), formula_cols=fc, number_formats={6: 'dd mmm yyyy', 7: '#,##0', 8: '#,##0', 12: '0', 14: 'dd mmm yyyy', 15: '0%'},
                 wrap_cols=(1, 2, 11, 13, 16))
    for r in range(AP_FIRST, AP_FIRST + len(ACTIONS)):
        ws.row_dimensions[r].height = 45
    K.dropdown(ws, f'A{AP_FIRST}:A{AP_LAST}', pa('A'), 'URLs from the Page Audit.')
    K.dropdown(ws, f'B{AP_FIRST}:B{AP_LAST}', chk, 'The checks from the Page Audit.')
    K.dropdown(ws, f'C{AP_FIRST}:C{AP_LAST}', f'{S}!$V$35:$V$46')
    K.dropdown(ws, f'D{AP_FIRST}:D{AP_LAST}', f'{S}!$W$35:$W$42')
    K.dropdown(ws, f'E{AP_FIRST}:E{AP_LAST}', f'{S}!$P$49:$P$51')
    K.dropdown(ws, f'I{AP_FIRST}:J{AP_LAST}', '"Yes,No"')
    t = f'P{AP_FIRST}:P{AP_LAST}'
    ws.conditional_formatting.add(t, FormulaRule(formula=[f'OR(LEFT(P{AP_FIRST},2)="Up",LEFT(P{AP_FIRST},3)="Now")'], fill=PatternFill('solid', fgColor='B7E4A0'), font=Font(name=K.FONT, bold=True)))
    ws.conditional_formatting.add(t, FormulaRule(formula=[f'LEFT(P{AP_FIRST},4)="Down"'], fill=PatternFill('solid', fgColor='F8D7D3'), font=Font(name=K.FONT, bold=True, color='9B2C1F')))
    ws.conditional_formatting.add(t, FormulaRule(formula=[f'OR(LEFT(P{AP_FIRST},4)="Wait",LEFT(P{AP_FIRST},4)="Flat",LEFT(P{AP_FIRST},3)="Add")'], fill=PatternFill('solid', fgColor='FFF4CC')))
    ws['R4'] = 'WEEKLY FIX HOURS'
    ws['R4'].font = K.f(10, True, K.DEEP)
    for j, h in enumerate(['Week', 'Hours planned', 'Capacity', 'Status']):
        cc = ws.cell(row=5, column=18 + j, value=h)
        cc.font, cc.fill = K.f(10, True, 'FFFFFF'), K.HEAD_F
    for i in range(len(WEEKS)):
        r = 6 + i
        ws.cell(row=r, column=18, value=f'={S}!W{35 + i}')
        ws.cell(row=r, column=19, value=f'=SUMIF($D${AP_FIRST}:$D${AP_LAST},R{r},$L${AP_FIRST}:$L${AP_LAST})')
        ws.cell(row=r, column=20, value=f'={HOURS}')
        ws.cell(row=r, column=21, value=f'=IF(S{r}=0,"Free",IF(S{r}>T{r},"Over capacity by "&(S{r}-T{r})&" hours","OK"))')
        for cc in range(18, 22):
            cell = ws.cell(row=r, column=cc)
            cell.border, cell.fill, cell.font = K.BORDER, K.FORMULA_FILL, K.f(10)
    for col, w in zip('QRSTU', [3, 12, 10, 9, 24]):
        ws.column_dimensions[col].width = w
    ws.conditional_formatting.add('U6:U13', FormulaRule(formula=['LEFT(U6,4)="Over"'], fill=PatternFill('solid', fgColor='F8D7D3'), font=Font(name=K.FONT, bold=True, color='9B2C1F')))
    ws.freeze_panes = 'B5'
    ws.auto_filter.ref = f'A4:P{AP_LAST}'
    return ws


def chart(ws, title, ytitle, cat_col, val_cols, r1, r2, anchor, colors, horiz, h=7.5, w=16):
    ch = BarChart()
    ch.type = 'bar' if horiz else 'col'
    ch.title = title
    ch.y_axis.title = ytitle
    for vc in val_cols:
        ch.add_data(Reference(ws, min_col=vc, min_row=r1, max_row=r2), titles_from_data=False)
    ch.set_categories(Reference(ws, min_col=cat_col, min_row=r1, max_row=r2))
    ch.legend = None
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
    for col, w in zip('ABCDEFGHIJK', [50, 13, 3, 34, 30, 8, 9, 14, 13, 3, 3]):
        ws.column_dimensions[col].width = w
    aio = qt('H')
    kpis = [
        ('Queries tracked', f'=COUNTIF({qt("A")},"?*")', '0'),
        ('Queries with an AI Overview (Yes or Sometimes)', f'=COUNTIF({aio},"Yes")+COUNTIF({aio},"Sometimes")', '0'),
        ('Queries where you are cited in the AI Overview', f'=COUNTIF({qt("I")},"Yes")', '0'),
        ('Citation rate (cited / AI Overview queries)', '=IFERROR(B7/B6,"")', '0%'),
        ('Queries where AI Mode cites you', f'=COUNTIF({qt("L")},"Yes")', '0'),
        ('P1 queries (including eligibility fixes)', f'=COUNTIF({qt("Priority")},"P1*")', '0'),
        ('Queries to check again', f'=COUNTIF({qt("Check again?")},"Yes*")', '0'),
        ('Pages audited', f'=COUNTIF({pa("A")},"?*")', '0'),
        ('Pages not eligible (a gate is No)', f'=COUNTIF({pa("Eligibility")},"Not eligible")', '0'),
        ('Average readiness score', f'=IFERROR(AVERAGE({pa("Readiness score (0 to 100)")}),"")', '0'),
        ('Pages ready (score at least the Ready threshold)', f'=COUNTIF({pa("Readiness")},"Ready")', '0'),
        ('AI feature impressions, 28 days', f'=SUM({pa("AI feature impressions (28 days)")})', '#,##0'),
        ('AI share of search impressions', f'=IFERROR(B16/SUM({pa("Search impressions (28 days)")}),"")', '0.0%'),
        ('Fan out sub questions mapped', f'=COUNTIF({fo("B")},"?*")', '0'),
        ('Fan out coverage (all queries)', f'=IFERROR(SUM({fo("I")})/B18,"")', '0%'),
        ('Fixes open (To do or Doing)', f'=COUNTIF({APS}!$E${AP_FIRST}:$E${AP_LAST},"To do")+COUNTIF({APS}!$E${AP_FIRST}:$E${AP_LAST},"Doing")', '0'),
        ('Fixes done', f'=COUNTIF({APS}!$E${AP_FIRST}:$E${AP_LAST},"Done")', '0'),
        ('Fixes that led to a new citation or more AI impressions', f'=COUNTIF({APS}!$P${AP_FIRST}:$P${AP_LAST},"Now*")+COUNTIF({APS}!$P${AP_FIRST}:$P${AP_LAST},"Up*")', '0'),
    ]
    ws['A4'] = 'KEY NUMBERS'
    ws['A4'].font = K.f(10, True, K.DEEP)
    for i, (label, fml, fmt) in enumerate(kpis):
        r = 5 + i
        ws.cell(row=r, column=1, value=label).font = K.f(10)
        cell = ws.cell(row=r, column=2, value=fml)
        cell.number_format, cell.font, cell.fill, cell.border = fmt, K.f(11, True), K.FORMULA_FILL, K.BORDER
        cell.alignment = Alignment(horizontal='right')
    ws['D4'] = 'TOP 10 QUERIES TO WORK ON (eligibility fixes first, then opportunity score)'
    ws['D4'].font = K.f(10, True, K.DEEP)
    heads = ['Query', 'Status', 'Score', 'Readiness', 'Priority', 'Fan out']
    cols = ['A', 'Status', 'Opportunity score (0 to 100)', 'Page readiness (0 to 100)', 'Priority', 'Fan out coverage']
    for j, h in enumerate(heads):
        cell = ws.cell(row=5, column=4 + j, value=h)
        cell.font, cell.fill = K.f(10, True, 'FFFFFF'), K.HEAD_F
    rk = qt('Rank (helper)')
    for k in range(1, 11):
        r = 5 + k
        mt = f'MATCH(LARGE({rk},{k}),{rk},0)'
        for j, col in enumerate(cols):
            cell = ws.cell(row=r, column=4 + j, value=f'=IFERROR(INDEX({qt(col)},{mt}),"")')
            cell.border, cell.fill, cell.font = K.BORDER, K.FORMULA_FILL, K.f(9, j == 0)
            cell.alignment = Alignment(wrap_text=j in (0, 1, 4), vertical='top')
            cell.number_format = {2: '0', 3: '0', 5: '0%'}.get(j, '@')
        ws.row_dimensions[r].height = 30
    top = 27
    ws.cell(row=top - 1, column=1, value='QUERIES BY STATUS').font = K.f(10, True, K.DEEP)
    for j, h in enumerate(['Status', 'Queries']):
        cell = ws.cell(row=top, column=1 + j, value=h)
        cell.font, cell.fill = K.f(10, True, 'FFFFFF'), K.HEAD_F
    for i in range(len(STATUSES)):
        r = top + 1 + i
        ws.cell(row=r, column=1, value=f'={S}!J{24 + i}')
        ws.cell(row=r, column=2, value=f'=COUNTIF({qt("Status")},A{r})')
        for cc in (1, 2):
            cell = ws.cell(row=r, column=cc)
            cell.border, cell.fill, cell.font = K.BORDER, K.FORMULA_FILL, K.f(10, cc == 1)
    t2 = top + len(STATUSES) + 4
    ws.cell(row=t2 - 1, column=1, value='PAGES BY READINESS').font = K.f(10, True, K.DEEP)
    for j, h in enumerate(['Readiness', 'Pages']):
        cell = ws.cell(row=t2, column=1 + j, value=h)
        cell.font, cell.fill = K.f(10, True, 'FFFFFF'), K.HEAD_F
    for i, p in enumerate(['Ready', 'Nearly ready', 'Needs work', 'Weak', 'Blocked']):
        r = t2 + 1 + i
        ws.cell(row=r, column=1, value=p).border = K.BORDER
        cell = ws.cell(row=r, column=2, value=f'=COUNTIF({pa("Readiness")},A{r})')
        cell.border, cell.fill = K.BORDER, K.FORMULA_FILL
    g0 = t2 + 9
    ws.cell(row=g0 - 1, column=1, value='MOST COMMON GAPS (pages where the check is not Yes)').font = K.f(10, True, K.DEEP)
    for j, h in enumerate(['Check', 'Pages']):
        cell = ws.cell(row=g0, column=1 + j, value=h)
        cell.font, cell.fill = K.f(10, True, 'FFFFFF'), K.HEAD_F
    for k, name in enumerate(CHK_NAMES):
        r = g0 + 1 + k
        ws.cell(row=r, column=1, value=f'={S}!J{CHK_FIRST + k}').border = K.BORDER
        cell = ws.cell(row=r, column=2, value=f'=COUNTIF({pa(GAPS[k])},">0")')
        cell.border, cell.fill = K.BORDER, K.FORMULA_FILL
    chart(ws, 'Queries by status', 'Queries', 1, [2], top + 1, top + len(STATUSES), 'D18', ['E07A5F'], True, h=9, w=18)
    chart(ws, 'Pages by readiness', 'Pages', 1, [2], t2 + 1, t2 + 5, 'D37', [K.GREEN], False, w=18)
    chart(ws, 'Most common gaps', 'Pages', 1, [2], g0 + 1, g0 + len(CHK_NAMES), 'D53', ['F4B860'], True, h=10, w=18)
    return ws, top, t2, g0


def build(path, asset, url):
    wb = K.new_book()
    tracker_sheet(wb)
    audit_sheet(wb)
    fanout_sheet(wb)
    action_sheet(wb)
    dashboard_sheet(wb)
    settings_sheet(wb)
    K.prompts_sheet(wb, asset['prompts'], url)
    K.checklist_sheet(wb, list(asset['checklist']))
    K.sources_sheet(wb, asset['sources'], [
        ('Demo data', 'Sproutly, every URL and every query in the demo are fictional (.example domain). Searches, positions, citations, impressions and dates are illustrative, not real data.', ''),
        ('Weights, bands, factors and hours', 'The check weights, opportunity weights, position bands, AI Overview factors, fan out thresholds, hours per fix and the 40 to 60 word answer first habit are assumptions of this kit. Google publishes no such numbers. Tune them on Settings.', ''),
        ('No special requirements', 'Google says there are no additional requirements to appear in AI Overviews or AI Mode, nor other special optimizations necessary. A page must be indexed and eligible to be shown with a snippet.', 'https://developers.google.com/search/docs/appearance/ai-features'),
        ('Query fan out', 'Google says AI Overviews and AI Mode may use a query fan out technique, issuing multiple related searches across subtopics and data sources.', 'https://developers.google.com/search/docs/appearance/ai-features'),
        ('Generative AI performance report', 'Search Console reports impressions of links to your site in AI Overviews and AI Mode, by page, country, device and date. Google says it rolled out to all websites worldwide as of 31 August 2026.', 'https://support.google.com/webmasters/answer/16984139'),
        ('Citations and rankings', 'An Ahrefs study (March 2026, 863,000 keyword results pages, about 4 million AI Overview URLs) found 37.9 percent of cited URLs also ranked in the top 10, down from about 76 percent in July 2025.', 'https://ahrefs.com/blog/ai-overview-citations-top-10/'),
    ])
    K.start_here(
        wb, 'AI Overview Optimization Kit',
        [
            'This workbook shows which of your queries show an AI Overview, where you are cited and where you are not, and which pages to fix first. Every query gets a status, a next action, an opportunity score and a priority.',
            f'Every page gets a readiness score from 14 checks, three of them gates (indexed, snippet allowed, crawlable), plus its biggest gap and hours to fix. The Fan Out Map lists the sub questions behind each query, and the Action Plan measures each fix 28 days later. A worked demo for a fictional plant shop ({len(QUERIES)} queries, {len(PAGES)} pages, {len(FANOUT)} sub questions) shows every formula working.',
        ],
        [
            ('Query Tracker', 'One row per query, 500 rows ready. AI Overview and citation checks, page readiness and eligibility, fan out coverage, status, next action, score, priority and recheck dates.'),
            ('Page Audit', 'One row per page, 300 rows ready. 14 checks, gates, readiness score, biggest gap, fixes left, hours and AI share of impressions.'),
            ('Fan Out Map', 'The sub questions behind each query, where you found them and whether the page covers them, with an action for each gap.'),
            ('Action Plan', 'Fixes by week with hours, how to fix, a weekly hours check and a before and after result from Search Console.'),
            ('Dashboard', '18 key numbers, the top 10 queries to work on, queries by status, pages by readiness and the most common gaps, with three charts.'),
            ('Settings', 'Check weights and gates, opportunity weights, position bands, AI Overview factors, status actions, rules and lists.'),
            ('AI Prompts', 'Prompts for ChatGPT, Claude or Gemini to map sub questions, rewrite answers and compare your page with cited sources.'),
            ('Checklist', 'The AI Overview optimization process as a tick list with automatic progress.'),
            ('Sources', 'Where facts come from and which numbers are assumptions.'),
        ],
        [
            'Look at the demo on every tab. Then clear the yellow demo cells on Query Tracker, Page Audit, Fan Out Map and Action Plan.',
            'On Settings, set today\'s date, the searches that earn full marks and your fix hours per week. Check the weights.',
            'Add each page you want cited to the Page Audit and answer the 13 typed checks. Start with the three gates.',
            'Add your target queries to the Query Tracker. Search each one in a private window and record the AI Overview, citation and sources.',
            'For each priority query, list 4 to 8 sub questions on the Fan Out Map and mark whether the page covers them.',
            'Sort the Query Tracker by priority. Add the biggest gaps of the top pages to the Action Plan, within your weekly hours.',
            'After each fix, wait 28 days, then add AI feature impressions before and after from Search Console and check the citation again.',
        ],
        url,
    )
    order = ['Start Here', 'Query Tracker', 'Page Audit', 'Fan Out Map', 'Action Plan', 'Dashboard', 'Settings', 'AI Prompts', 'Checklist', 'Sources']
    wb._sheets = [wb[n] for n in order]
    wb.active = 0
    for ws in wb.worksheets:
        ws.sheet_properties.tabColor = K.GREEN if ws.title in order[:6] else 'A6EF39'
    wb.save(path)


PREVIEW = {'sheet': 'Query Tracker', 'header_row': 4, 'rows': 12,
           'cols': [1, 7, 8, 9, len(QT_IN) + 2, len(QT_IN) + 6, len(QT_IN) + 8, len(QT_IN) + 9],
           'formula_idx': [4, 5, 6, 7]}


def check(wb):
    """Assert the worked examples used in the guide."""
    p = wb['Page Audit']
    pv = lambda h, r: p[f'{PC[h]}{r}'].value
    r = 5   # succulent watering page
    assert pv('Fan out sub questions', r) == 8 and abs(pv('Fan out coverage', r) - 3.5 / 8) < 1e-9, (pv('Fan out sub questions', r), pv('Fan out coverage', r))
    assert pv('Covers the fan out sub questions', r) == 'No' and pv('Eligibility', r) == 'Eligible'
    assert pv('Readiness score (0 to 100)', r) == 60 and pv('Readiness', r) == 'Nearly ready', pv('Readiness score (0 to 100)', r)
    assert pv('Biggest gap', r) == 'Original value (data, tests, experience)' and pv('Fixes left', r) == 6 and pv('Hours to fix (assumption)', r) == 15, (pv('Biggest gap', r), pv('Fixes left', r), pv('Hours to fix (assumption)', r))
    assert abs(pv('AI share of impressions', r) - 9200 / 41000) < 1e-9 and pv('Queries targeting this page', r) == 2
    assert pv('Readiness score (0 to 100)', 6) == 100 and pv('Readiness', 6) == 'Ready' and pv('Biggest gap', 6) == 'None: protect the page', (pv('Readiness score (0 to 100)', 6), pv('Biggest gap', 6))
    assert pv('Eligibility', 12) == 'Not eligible' and pv('Readiness', 12) == 'Blocked'
    q = wb['Query Tracker']
    qv = lambda h, r: q[f'{QC[h]}{r}'].value
    r = 5   # how often to water succulents
    assert qv('Page readiness (0 to 100)', r) == 60 and qv('Fan out sub questions', r) == 6 and abs(qv('Fan out coverage', r) - 2.5 / 6) < 1e-9
    assert qv('Status', r) == 'Ranks top 10, not cited: close the answer gap', qv('Status', r)
    assert qv('Opportunity score (0 to 100)', r) == 78 and qv('Priority', r) == 'P1: now', qv('Opportunity score (0 to 100)', r)
    assert qv('Days since checked', r) == 7 and qv('Check again?', r) == 'In 23 days'
    assert qv('Status', 15) == 'Fix eligibility first' and qv('Priority', 15) == 'P1: fix eligibility', (qv('Status', 15), qv('Priority', 15))
    assert qv('Status', 7) == 'Cited: protect and expand' and qv('Priority', 7) == 'Protect'
    assert qv('Status', 12) == 'No AI Overview: classic SEO' and qv('Status', 20) == 'Check the results page' and qv('Check again?', 20) == 'Yes: never checked'
    assert qv('Status', 8) == 'Ranks 11 to 30: build depth and fan out coverage' and qv('Status', 18) == 'Not ranking: build a stronger page', (qv('Status', 8), qv('Status', 18))
    a = wb['Action Plan']
    assert a['L5'].value == 1 and a['P5'].value == 'Not done yet' and a['P7'].value == 'Wait: 15 days left', (a['L5'].value, a['P7'].value)
    assert a['P8'].value == 'Up 33%: keep going' and a['P9'].value == 'Now cited: keep going' and a['P12'].value == 'Flat: give it another cycle', (a['P8'].value, a['P9'].value, a['P12'].value)
    assert a['S6'].value == 2 and a['S7'].value == 8 and a['U7'].value == 'OK', (a['S6'].value, a['S7'].value)
    dsh = wb['Dashboard']
    vals = {dsh.cell(row=r, column=1).value: dsh.cell(row=r, column=2).value for r in range(5, 23)}
    assert vals['Queries tracked'] == len(QUERIES) and vals['Queries where you are cited in the AI Overview'] == 2, vals
    assert dsh['D6'].value == 'why are my plant leaves turning yellow' and dsh['D7'].value == 'yellow leaves on monstera' and dsh['D8'].value == 'best low light plants', (dsh['D6'].value, dsh['D7'].value, dsh['D8'].value)
    s = wb['Settings']
    assert s['K20'].value == 100 and s['G11'].value == 100
    return vals
