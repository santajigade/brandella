"""Meta Description Kit workbook (asset 09).

Description Lab: one row per page (500 rows). You paste the title, the meta description, the snippet Google
really shows, the snippet controls and the Search Console numbers. The sheet measures length, duplicates,
boilerplate openings, keyword use, comma lists, facts, title repeats, years and CTR against your own site
average for the same position band, runs 13 weighted checks (1 = pass, 0.5 = partly, 0 = fix, blank = not
checked), gives a score, a grade, the fixes in priority order, a priority and an estimate of missed clicks,
and checks a proposed new description. Bulk Builder writes unique descriptions for many similar pages from
templates (Google recommends programmatic descriptions for large database driven sites). Test Log judges
changes fairly. Dashboard sums it all up.
"""
import datetime
from openpyxl.styles import PatternFill, Font, Alignment
from openpyxl.formatting.rule import CellIsRule, ColorScaleRule, FormulaRule
from openpyxl.chart import BarChart, Reference
from openpyxl.utils import get_column_letter as L
import kitlib as K

DL_FIRST, DL_LAST = 5, 504     # Description Lab
BB_FIRST, BB_LAST = 5, 204     # Bulk Builder
TS_FIRST, TS_LAST = 5, 204     # Test Log
S = 'Settings'
DL = "'Description Lab'"

(DATE, DMIN, DMAX, OPEN, SNIPMIN, COMMAS, WPC) = (f'{S}!$B${r}' for r in range(5, 12))
(MINIMP, CTRG, CTRL, BIGIMP, WAIT, WIN, POSMOVE) = (f'{S}!$B${r}' for r in range(13, 20))
(GA, GB, GC, REWRITE, SD1, SD2) = (f'{S}!$B${r}' for r in range(22, 28))
CHK_ROW = 31
YEARS = f'{S}!$K$5:$K$25'

PAGE_TYPES = [('Home', 'No'), ('Category', 'Yes'), ('Product or tour', 'Yes'), ('Article or guide', 'Yes'), ('Service', 'Yes'),
              ('Local landing', 'Yes'), ('Tool', 'Yes'), ('About or contact', 'No')]
BANDS = [(1, '1 to 3'), (4, '4 to 10'), (11, '11 to 20'), (21, '21 and beyond')]
SNIP = ['None', 'max-snippet', 'nosnippet']
TSTAT = ['Planned', 'Live', 'Reverted']

CHECKS = [
    ('Description present', 10, 'The page has a meta description.',
     'Write one or two sentences that summarise this page. Google says to write descriptions for your important pages first.'),
    ('Snippet allowed', 8, 'No nosnippet and no max-snippet below 50 characters (editable). nosnippet or max-snippet:0 = fix; a tight max-snippet = partly.',
     'Remove nosnippet unless you mean it. Google says a page must be eligible to show with a snippet to appear as a supporting link in AI Overviews and AI Mode.'),
    ('Unique description', 8, 'No other page uses the same description.', 'Give every page its own description. Google says identical descriptions on every page are not helpful.'),
    ('Not a keyword list', 6, 'Not a comma list (4 or more commas with fewer than 3 words between them, editable) and the keyword at most 2 times. Twice = partly. A list or 3 repeats = fix.',
     'Write a real summary. Google says long strings of keywords give people no clear idea of the page and are unlikely to be shown.'),
    ('Opening answers the search', 6, 'The first paragraph of the page answers the main question or says what the page offers (Yes or No).',
     'Google builds most snippets from page content. Open with 2 or 3 sentences that answer the search plainly.'),
    ('CTR vs your site average', 6, 'CTR is at least 80 percent of your own band average = pass, 50 to 79 percent = partly, below = fix. Needs 100 impressions.',
     'Rewrite the description around what searchers want: the answer, the facts and the reason to click. Then log it as a test.'),
    ('Keyword or topic named', 5, 'The focus keyword appears in the description = pass. Missing = partly.', 'Name the main topic naturally, once.'),
    ('Length', 5, '70 to 160 characters = pass (editable). Under 35 characters = fix. Otherwise partly.',
     'Google sets no limit and cuts snippets to fit the device, so put the most useful words first and aim for a full, specific summary.'),
    ('Specific facts', 5, 'The description contains at least one number (price, count, duration, date, size) = pass. None = partly.',
     'Add the facts searchers compare: price, duration, number of items, dates, author or opening hours.'),
    ('Not boilerplate', 5, 'No other page starts with the same 40 characters (editable). Not checked when the whole description is a duplicate.',
     'Start each description with what is special about that page, not with the same sentence about your company.'),
    ('Uses your description', 4, 'The snippet Google shows (pasted) uses your description = pass. Written from the page = partly. Blank = not checked.',
     'Snippets change with the query. If Google always writes its own, make the description a closer summary of the page.'),
    ('Adds to the title', 3, 'The description does not start with the whole title.', 'Use the description to add what the title cannot: facts, proof and the next step.'),
    ('Year is current', 3, 'If the description shows a year, it is the analysis year or later. Not checked when there is no year.',
     'Update the year only after a real update, and in the title and on the page too.'),
]
NCH = len(CHECKS)

# Bulk Builder templates: name, template, best for
TEMPLATES = [
    ('Trek or tour', '{name} in {place}: {number}, {fact1}. {fact2}. {offer}.', 'Tours, trips, courses and events with fixed facts'),
    ('Product', '{name}: {fact1} and {fact2}. {number}. {offer}.', 'Product pages from a catalogue'),
    ('Category', 'Browse {number} {name} in {place}: {fact1} and {fact2}. {offer}.', 'Category and listing pages'),
    ('Local', '{name} in {place}: {fact1}. {fact2}. {offer}.', 'Branch and service area pages'),
    ('Article byline', 'By {name}, updated {number}. {fact1}. {fact2}.', 'News and blog posts (Google suggests author and date)'),
    ('Facts only', '{name}. {fact1}. {fact2}. Price: {number}.', 'Pages where key facts say it all (Google says descriptions need not be sentences)'),
    ('Free tool', 'Free {name}: {fact1}. {fact2}. {offer}.', 'Calculators and tools'),
    ('Event', '{name} on {number} in {place}: {fact1}. {fact2}. {offer}.', 'Events and dated departures'),
]
TPL_ROW = CHK_ROW + NCH + 4

# Demo: TrekTrail, a fictional trek operator in Dehradun. Every page and number is illustrative.
# url, type, kw, title, description, opening answers, snippet control, max-snippet, snippet shown, impressions, clicks, position, proposed, notes
P = [
    ('https://trektrail.example/', 'Home', 'himalayan treks', 'TrekTrail: Small Group Himalayan Treks from Dehradun',
     'TrekTrail runs small group Himalayan treks from Dehradun: 24 routes, certified trek leaders and fixed departures every week from March to December.',
     'Yes', 'None', None, '', 7000, 1100, 2.0, '', ''),
    ('https://trektrail.example/treks-in-uttarakhand/', 'Category', 'treks in uttarakhand', 'Treks in Uttarakhand: 24 Routes for Every Level', '',
     'Yes', 'None', None, 'Compare 24 treks in Uttarakhand by days, altitude and difficulty, from easy 3 day walks to high passes for experienced trekkers.',
     26000, 520, 7.5, 'Compare 24 treks in Uttarakhand by days, altitude and difficulty, with prices from Rs 6,500 and weekly departures from Dehradun.', 'Template forgot this page'),
    ('https://trektrail.example/treks/kedarkantha/', 'Product or tour', 'kedarkantha trek', 'Kedarkantha Trek: 6 Day Snow Trek from Dehradun',
     'Kedarkantha trek in 6 days from Dehradun: snow summit at 3,800 m, stays and meals included. From Rs 9,500 with free date changes.',
     'Yes', 'None', None, 'Kedarkantha trek in 6 days from Dehradun: snow summit at 3,800 m, stays and meals included. From Rs 9,500 with free date changes.',
     40000, 2100, 4.2, '', ''),
    ('https://trektrail.example/treks/valley-of-flowers/', 'Product or tour', 'valley of flowers trek', 'Valley of Flowers Trek: 6 Days in the Monsoon Bloom',
     'Book your Himalayan trek with TrekTrail, the trusted operator in Dehradun. Valley of Flowers trek in July and August with Hemkund Sahib.',
     'Yes', 'None', None, '', 15000, 420, 6.4, 'Valley of Flowers trek in 6 days, July to mid September: 300 flower species, Hemkund Sahib day hike and stays included from Rs 12,000.', ''),
    ('https://trektrail.example/treks/brahmatal/', 'Product or tour', 'brahmatal trek', 'Brahmatal Trek: 6 Day Winter Trek with Lake Views',
     'Book your Himalayan trek with TrekTrail, the trusted operator in Dehradun. Brahmatal trek in winter with frozen lakes and summit views.',
     'Yes', 'None', None, '', 11000, 380, 5.1, '', 'Same opening as Valley of Flowers'),
    ('https://trektrail.example/blog/best-time-for-kedarkantha-trek/', 'Article or guide', 'best time for kedarkantha trek', 'Best Time for Kedarkantha Trek: Month by Month Guide',
     'Kedarkantha trek, best time for Kedarkantha trek, Kedarkantha in winter, Kedarkantha snow, Kedarkantha weather, Kedarkantha temperature',
     'No', 'None', None, 'Every December our trek leaders head up to Kedarkantha to check the trail. Here is what they have learned about the weather and the snow...',
     18000, 160, 5.8, 'Best time for Kedarkantha trek: December to April for snow and May for clear skies. Weather, crowds and what to pack for all 12 months.',
     'Worked example in the guide'),
    ('https://trektrail.example/blog/trek-packing-list/', 'Article or guide', 'trek packing list', 'Trek Packing List: 42 Items for a Himalayan Trek',
     'Our trek packing list has 42 items for 5 to 8 day Himalayan treks, from layers and rain gear to the first aid kit, with a printable checklist.',
     'Yes', 'None', None, 'Our trek packing list has 42 items for 5 to 8 day Himalayan treks, from layers and rain gear to the first aid kit, with a printable checklist.',
     9000, 700, 3.0, '', ''),
    ('https://trektrail.example/blog/prepare-for-high-altitude-trek/', 'Article or guide', 'prepare for a high altitude trek', 'How to Prepare for a High Altitude Trek: A Training Plan',
     'How to prepare for a high altitude trek: a simple training plan for stamina, strength and breathing, plus what to eat and how to acclimatise.',
     'Yes', 'None', None, '', 12000, 300, 9.1, '', ''),
    ('https://trektrail.example/blog/trekking-shoes-vs-hiking-boots/', 'Article or guide', 'trekking shoes vs hiking boots', 'Trekking Shoes vs Hiking Boots: Which Is Better?',
     'Trekking Shoes vs Hiking Boots: Which Is Better? We compare grip, ankle support, weight and price for 4 kinds of Himalayan trail.',
     'Yes', 'None', None, '', 5000, 70, 12.5, 'Trekking shoes vs hiking boots on 4 kinds of Himalayan trail: grip, ankle support, weight and price, and what our 12 trek leaders wear.', ''),
    ('https://trektrail.example/trek-operator-dehradun/', 'Local landing', 'trek operator in dehradun', 'Trek Operator in Dehradun: Visit Our Rajpur Road Office',
     'Visit our trek office on Rajpur Road, Dehradun, open 9 am to 7 pm every day. Talk to a trek leader, rent gear and book any of our 24 treks.',
     'Yes', 'None', None, '', 2500, 320, 1.9, '', ''),
    ('https://trektrail.example/tools/trek-cost-calculator/', 'Tool', 'trek cost calculator', 'Trek Cost Calculator: Budget Your Himalayan Trek',
     'Free trek cost calculator: add your trek, days, travel and gear to see the full cost of a Himalayan trek, with the extras most people forget.',
     'Yes', 'nosnippet', None, '', 3000, 30, 6.0, '', 'nosnippet left over from a template'),
    ('https://trektrail.example/blog/chopta-tungnath-trek/', 'Article or guide', 'chopta tungnath trek', 'Chopta Tungnath Trek: Route, Map and Best Time',
     'Chopta Tungnath trek guide for 2024: the 3.5 km route to Tungnath temple and Chandrashila, the best time to go and where to stay in Chopta.',
     'Yes', 'max-snippet', 30, '', 7000, 210, 8.0, 'Chopta Tungnath trek guide: the 3.5 km route to Tungnath temple and Chandrashila, the best time to go and where to stay in Chopta.', ''),
    ('https://trektrail.example/about/', 'About or contact', 'trektrail', 'About TrekTrail: Our Trek Leaders and Story', 'About us.',
     'Yes', 'None', None, '', 600, 90, 1.4, 'Meet the 12 certified trek leaders behind TrekTrail, see how we run small group treks from Dehradun and read our safety rules.', ''),
    ('https://trektrail.example/winter-treks/', 'Category', 'winter treks in india', 'Winter Treks in India: 9 Snow Treks for December to March',
     'Looking for the best winter treks in India? Our team has handpicked 9 snow treks in Uttarakhand and Himachal for December to March, with easy, moderate and hard options, small groups, certified trek leaders, stays and meals included and free date changes.',
     'Yes', 'None', None, '', 6000, 90, 14.0, '', ''),
]
TESTS = [
    (2, 'Kedarkantha trek with TrekTrail. Book now for the best prices and service.', None, '2026-09-01', 'Live', 36000, 1300, 4.3, 40000, 2100, 4.2, 'Added days, altitude, price and date change'),
    (7, 'Prepare for your trek with our guide.', None, '2026-11-10', 'Live', 11500, 280, 9.3, None, None, None, 'Too early to judge'),
    (9, 'Our trek office in Dehradun.', None, '2026-08-15', 'Live', 2300, 280, 2.0, 2500, 320, 1.9, 'Added address and hours'),
    (7, 'Prepare for a high altitude trek with a training plan.', 'How to prepare for a high altitude trek: a simple training plan for stamina, strength and breathing, plus what to eat and how to acclimatise.', '2026-07-01', 'Reverted', 12000, 300, 9.0, 11800, 300, 9.2, 'Kept for the record'),
    (5, None, 'Best time for Kedarkantha trek: December to April for snow and May for clear skies. Weather, crowds and what to pack for all 12 months.',
     '2026-11-28', 'Planned', 18000, 160, 5.8, None, None, None, 'From the worked example'),
]
# Bulk Builder demo: id or URL, template, name, fact1, fact2, number, place, offer
BUILD = [
    ('/treks/kedarkantha/', 'Trek or tour', 'Kedarkantha trek', 'snow summit at 3,800 m', 'Stays, meals and permits included', '6 days', 'Uttarakhand', 'From Rs 9,500 with free date changes'),
    ('/treks/brahmatal/', 'Trek or tour', 'Brahmatal trek', 'frozen lakes and views of Trishul', 'Small groups of up to 12', '6 days', 'Uttarakhand', 'From Rs 10,500 with free date changes'),
    ('/treks/har-ki-dun/', 'Trek or tour', 'Har Ki Dun trek', 'a valley trek past 300 year old villages', 'Best from April to June and September to November', '7 days', 'Uttarakhand', 'From Rs 11,000'),
    ('/treks/hampta-pass/', 'Trek or tour', 'Hampta Pass trek', 'a crossing from green Kullu to the deserts of Lahaul', 'Includes a visit to Chandratal lake', '5 days', 'Himachal', 'From Rs 9,900'),
    ('/treks/kuari-pass/', 'Trek or tour', 'Kuari Pass trek', 'views of Nanda Devi from the pass', '', '6 days', 'Uttarakhand', 'From Rs 9,500'),
    ('/gear/trekking-poles/', 'Product', 'Aluminium trekking poles', 'weigh 240 g each', 'fold to 38 cm', 'Rs 1,450 a pair', '', 'Free pickup at our Dehradun office'),
    ('/winter-treks/', 'Category', 'winter treks', 'easy, moderate and hard routes', 'small groups with certified leaders', '9', 'Uttarakhand and Himachal', 'Departures every week from December to March'),
    ('/blog/trek-packing-list/', 'Article byline', 'Asha Rawat', 'A packing list of 42 items for 5 to 8 day Himalayan treks', 'With a printable checklist', '12 Nov 2026', '', ''),
    ('/treks/dayara-bugyal/', 'Trek or tour', 'Dayara Bugyal trek', 'snow meadows at 3,400 m', 'Stays, meals and permits included', '5 days', 'Uttarakhand', 'From Rs 8,500 with free date changes'),
    ('/treks/kedarkantha-copy/', 'Trek or tour', 'Kedarkantha trek', 'snow summit at 3,800 m', 'Stays, meals and permits included', '6 days', 'Uttarakhand', 'From Rs 9,500 with free date changes'),
]

IN_HEAD = ['URL', 'Page type', 'Focus keyword', 'Title tag', 'Meta description (paste)', 'Opening answers the search?', 'Snippet control',
           'max-snippet value', 'Snippet Google shows (paste, optional)', 'Impressions (28 days)', 'Clicks (28 days)', 'Avg position',
           'Proposed new description', 'Notes']
MEAS_HEAD = ['Characters', 'Words', 'Pages with this description', 'Pages with the same opening', 'Keyword count', 'Commas',
             'Has a number?', 'Repeats the title?', 'Year in description', 'Position band', 'CTR', 'Band average CTR', 'CTR vs band', 'Google snippet']
OUT_HEAD = ['Score (0 to 100)', 'Grade', 'Fixes needed', 'Fixes in priority order', 'Priority', 'Missed clicks (estimate)',
            'Proposed characters', 'Proposed description check', 'Opportunity (helper)', 'In CTR average (helper)']
NIN, NME = len(IN_HEAD), len(MEAS_HEAD)
C0 = NIN + NME + 1
CK = [L(C0 + i) for i in range(NCH)]
SC = C0 + NCH
HEAD = IN_HEAD + MEAS_HEAD + [c[0] for c in CHECKS] + OUT_HEAD
F_COLS = tuple(range(NIN + 1, len(HEAD) + 1))
M = {h: L(i + 1) for i, h in enumerate(HEAD)}


def dl(c):
    return f'{DL}!${c}${DL_FIRST}:${c}${DL_LAST}'


def d(s):
    return datetime.date.fromisoformat(s) if s else None


def settings_sheet(wb):
    ws = wb.create_sheet(S)
    ws.sheet_view.showGridLines = False
    K.title_block(ws, 'Settings', 'Every threshold, weight, list and template used by this workbook. Change a blue value and every score updates.')
    for c, w in zip('ABCDEFGHIJKLMNO', [50, 14, 64, 58, 3, 14, 16, 3, 3, 3, 10, 3, 10, 13, 11]):
        ws.column_dimensions[c].width = w
    rows = [
        (4, 'DESCRIPTION RULES', None, None),
        (5, 'Analysis date (set it to the day you check)', datetime.date(2026, 11, 21), 'dd mmm yyyy'),
        (6, 'Description is short below (characters)', 70, '0'),
        (7, 'Description may be cut off above (characters)', 160, '0'),
        (8, 'Same opening: compare the first characters', 40, '0'),
        (9, 'max-snippet below this many characters is too tight', 50, '0'),
        (10, 'A keyword list has at least this many commas', 4, '0'),
        (11, 'and fewer words than this between commas, on average', 3, '0'),
        (12, 'CTR RULES (compared with your own Search Console data)', None, None),
        (13, 'Minimum impressions before CTR is judged', 100, '#,##0'),
        (14, 'CTR is fine at or above this share of the band average', 0.8, '0%'),
        (15, 'CTR is low below this share of the band average', 0.5, '0%'),
        (16, 'High impressions (for Rewrite first)', 1000, '#,##0'),
        (17, 'Description test: days to wait before judging', 28, '0'),
        (18, 'Description test: a win or loss needs a CTR change of at least', 0.1, '0%'),
        (19, 'Description test: fair only if the position moved by at most', 2, '0.0'),
        (21, 'GRADES AND PRIORITY', None, None),
        (22, 'Grade A when the score is at least', 85, '0'),
        (23, 'Grade B when at least', 70, '0'),
        (24, 'Grade C when at least (below = D)', 55, '0'),
        (25, 'Rewrite the description when the score is below', 50, '0'),
        (26, 'Close to the top: average position from', 4, '0'),
        (27, 'Close to the top: average position up to', 20, '0'),
    ]
    for r, label, val, fmt in rows:
        a = ws.cell(row=r, column=1, value=label)
        a.font = K.f(10, val is None, K.DEEP if val is None else K.INK)
        if val is not None:
            c = ws.cell(row=r, column=2, value=val)
            c.border, c.fill = K.BORDER, K.INPUT_FILL
            c.font = K.f(10, True, '0000FF')
            c.number_format = fmt
    ws['C5'] = ('Google says there is no limit on the length of a meta description and that snippets are truncated as needed, typically to fit the device width. '
                'The 70 and 160 character band, the 40 character opening, the 50 character max-snippet and the 4 comma rule are assumptions of this kit. '
                'CTR is judged against your own pages in the same position band, never against an outside benchmark.')
    ws['C5'].font = K.f(9, False, '777777', True)
    ws['C5'].alignment = Alignment(wrap_text=True, vertical='top')
    ws.merge_cells('C5:D10')
    ws.cell(row=CHK_ROW - 2, column=1, value='THE 13 CHECKS (weights are editable; any numbers, they are scaled)').font = K.f(10, True, K.DEEP)
    K.header_row(ws, CHK_ROW - 1, ['Check', 'Weight', 'Rule in the workbook', 'How to fix'])
    for i, (name, w, rule, fix) in enumerate(CHECKS):
        r = CHK_ROW + i
        for col, v in enumerate([name, w, rule, fix], 1):
            c = ws.cell(row=r, column=col, value=v)
            c.border = K.BORDER
            c.font = K.f(10, col == 1, '0000FF' if col == 2 else K.INK)
            c.alignment = Alignment(wrap_text=True, vertical='top')
        ws.cell(row=r, column=2).fill = K.INPUT_FILL
        ws.row_dimensions[r].height = 42
    tr = CHK_ROW + NCH
    ws.cell(row=tr, column=1, value='Total weight (auto)').font = K.f(10, True)
    ws.cell(row=tr, column=2, value=f'=SUM(B{CHK_ROW}:B{tr - 1})').fill = K.FORMULA_FILL
    ws.cell(row=TPL_ROW - 2, column=1, value='BULK BUILDER TEMPLATES ({name}, {fact1}, {fact2}, {number}, {place} and {offer} are filled in; add your own in the empty rows)').font = K.f(10, True, K.DEEP)
    K.header_row(ws, TPL_ROW - 1, ['Template name', 'Template', 'Best for', 'Example from the demo'])
    ex = {}
    for j, b in enumerate(BUILD):
        ex.setdefault(b[1], j)
    for i in range(15):
        r = TPL_ROW + i
        vals = list(TEMPLATES[i]) if i < len(TEMPLATES) else ['', '', '']
        for col, v in enumerate(vals, 1):
            ws.cell(row=r, column=col, value=v or None)
        if i < len(TEMPLATES) and TEMPLATES[i][0] in ex:
            ws.cell(row=r, column=4, value=f"='Bulk Builder'!I{BB_FIRST + ex[TEMPLATES[i][0]]}")
        for col in range(1, 5):
            c = ws.cell(row=r, column=col)
            c.border = K.BORDER
            c.fill = K.FORMULA_FILL if col == 4 else K.INPUT_FILL
            c.font = K.f(10, col == 1, '0000FF' if col == 2 else K.INK)
            c.alignment = Alignment(wrap_text=True, vertical='top')
        ws.row_dimensions[r].height = 30
    ws['F4'] = 'POSITION BANDS'
    ws['F4'].font = K.f(10, True, K.DEEP)
    ws['F5'], ws['G5'] = 'From position', 'Band name'
    for c in ('F5', 'G5'):
        ws[c].font = K.f(9, True, '555555')
    for i, (start, name) in enumerate(BANDS):
        for col, v in ((6, start), (7, name)):
            c = ws.cell(row=6 + i, column=col, value=v)
            c.fill, c.border = K.INPUT_FILL, K.BORDER
    ws['F11'] = 'PAGE TYPES'
    ws['F11'].font = K.f(10, True, K.DEEP)
    ws['F12'], ws['G12'] = 'Page type', 'In CTR averages?'
    for c in ('F12', 'G12'):
        ws[c].font = K.f(9, True, '555555')
    for i, (t, use) in enumerate(PAGE_TYPES):
        for col, v in ((6, t), (7, use)):
            c = ws.cell(row=13 + i, column=col, value=v)
            c.fill, c.border = K.INPUT_FILL, K.BORDER
    ws.cell(row=13 + len(PAGE_TYPES), column=6, value='Home and about pages mostly get brand searches, so their CTR is left out of the averages and not judged.').font = K.f(8, False, '777777', True)
    ws['K4'] = 'YEARS'
    ws['K4'].font = K.f(10, True, K.DEEP)
    for i in range(21):
        c = ws.cell(row=5 + i, column=11, value=2015 + i)
        c.fill, c.border = K.INPUT_FILL, K.BORDER
    ws['M4'] = 'LISTS'
    ws['M4'].font = K.f(10, True, K.DEEP)
    for col, vals in (('M', ['Yes/No', 'Yes', 'No']), ('N', ['Snippet control'] + SNIP), ('O', ['Test status'] + TSTAT)):
        for i, v in enumerate(vals):
            c = ws[f'{col}{5 + i}']
            c.value = v
            c.font = K.f(9, i == 0, '555555')
    return ws


def lab_sheet(wb):
    ws = wb.create_sheet('Description Lab')
    ws.sheet_view.showGridLines = False
    K.title_block(ws, 'Description lab', f'Rows 5 to {4 + len(P)} hold DEMO data for TrekTrail, a fictional trek operator (illustrative pages and numbers). Select the yellow demo cells and press Delete to start your own. Grey formula columns stay.')
    ws['A2'].font = K.f(10, True, 'B45309')
    ws['A3'] = 'One row per page. Paste the title and meta description from the page source, the snippet control from the robots meta tag, and (optional) the snippet Google shows in a real search. Add Search Console numbers for the last 28 days. 500 rows ready.'
    ws['A3'].font = K.f(9, False, '666666', True)
    widths = ([40, 14, 24, 36, 56, 10, 11, 8, 50, 10, 9, 8, 56, 26] + [8, 7, 9, 9, 8, 7, 8, 8, 8, 11, 8, 9, 8, 13] +
              [9] * NCH + [9, 7, 7, 56, 30, 10, 9, 34, 8, 8])
    K.header_row(ws, 4, HEAD, formula_cols=F_COLS, widths=widths)
    for i, col in enumerate(CK):
        c = ws[f'{col}3']
        c.value = f'={S}!$B${CHK_ROW + i}'
        c.font, c.fill, c.alignment = K.f(9, True, K.DEEP), K.SOFT, Alignment(horizontal='center')
    ws[f'{CK[0]}2'] = 'Check weights (from Settings)'
    ws[f'{CK[0]}2'].font = K.f(9, True, K.DEEP)
    m = M
    for r in range(DL_FIRST, DL_LAST + 1):
        i = r - DL_FIRST
        if i < len(P):
            for col, v in enumerate(P[i], 1):
                if v not in (None, ''):
                    ws.cell(row=r, column=col, value=v)
        e = f'A{r}=""'
        g = lambda h: f'{m[h]}{r}'
        E, C, Dt, Mp = f'E{r}', f'C{r}', f'D{r}', f'M{r}'
        f = {}
        f['Characters'] = f'=IF({e},"",LEN({E}))'
        f['Words'] = f'=IF(OR({e},TRIM({E})=""),"",LEN(TRIM({E}))-LEN(SUBSTITUTE(TRIM({E})," ",""))+1)'
        f['Pages with this description'] = f'=IF(OR({e},{E}=""),"",SUMPRODUCT(--($E${DL_FIRST}:$E${DL_LAST}={E})))'
        f['Pages with the same opening'] = (f'=IF(OR({e},LEN({E})<{OPEN}),"",SUMPRODUCT(--(LEFT($E${DL_FIRST}:$E${DL_LAST},{OPEN})=LEFT({E},{OPEN}))))')
        f['Keyword count'] = f'=IF(OR({e},{C}="",{E}=""),"",(LEN({E})-LEN(SUBSTITUTE(LOWER({E}),LOWER({C}),"")))/LEN({C}))'
        f['Commas'] = f'=IF(OR({e},{E}=""),"",LEN({E})-LEN(SUBSTITUTE({E},",","")))'
        digits = '+'.join(f'ISNUMBER(FIND("{n}",{E}))' for n in range(10))
        f['Has a number?'] = f'=IF(OR({e},{E}=""),"",IF(({digits})>0,"Yes","No"))'
        f['Repeats the title?'] = f'=IF(OR({e},{E}="",{Dt}=""),"",IF(LEFT({E},LEN(TRIM({Dt})))=TRIM({Dt}),"Yes","No"))'
        yr = f'SUMPRODUCT(MAX(ISNUMBER(SEARCH({YEARS},{E}))*{YEARS}))'
        f['Year in description'] = f'=IF(OR({e},{E}=""),"",IF({yr}=0,"",{yr}))'
        f['Position band'] = f'=IF(OR({e},N(L{r})=0),"",LOOKUP(L{r},{S}!$F$6:$F$9,{S}!$G$6:$G$9))'
        f['CTR'] = f'=IF(OR({e},N(J{r})=0,K{r}=""),"",K{r}/J{r})'
        band, ctr = g('Position band'), g('CTR')
        bc = '$' + m['Position band']
        hc = '$' + m['In CTR average (helper)']
        hr = f'{hc}${DL_FIRST}:{hc}${DL_LAST},"Yes"'
        f['Band average CTR'] = (f'=IF(OR({ctr}="",{band}=""),"",IFERROR(SUMIFS($K${DL_FIRST}:$K${DL_LAST},{bc}${DL_FIRST}:{bc}${DL_LAST},{band},$J${DL_FIRST}:$J${DL_LAST},">="&{MINIMP},{hr})'
                                 f'/SUMIFS($J${DL_FIRST}:$J${DL_LAST},{bc}${DL_FIRST}:{bc}${DL_LAST},{band},$J${DL_FIRST}:$J${DL_LAST},">="&{MINIMP},{hr}),""))')
        bav = g('Band average CTR')
        f['CTR vs band'] = f'=IF({g("In CTR average (helper)")}<>"Yes","",IF(OR({ctr}="",{bav}="",N(J{r})<{MINIMP}),"",IF({bav}=0,"",{ctr}/{bav})))'
        stem = f'TRIM(SUBSTITUTE(SUBSTITUTE(I{r},"...",""),"…",""))'
        f['Google snippet'] = (f'=IF(OR({e},I{r}=""),"",IF({E}="","Written from the page",IF(OR(ISNUMBER(FIND(LEFT({stem},40),{E})),'
                               f'ISNUMBER(FIND(LEFT({E},40),{stem}))),"Uses your description","Written from the page")))')
        kwc, cm, num, rep, yv, rat, gs = (g(h) for h in ('Keyword count', 'Commas', 'Has a number?', 'Repeats the title?', 'Year in description', 'CTR vs band', 'Google snippet'))
        t = {}
        t['Description present'] = f'=IF({e},"",IF(TRIM({E})="",0,1))'
        t['Snippet allowed'] = (f'=IF(OR({e},G{r}=""),"",IF(G{r}="nosnippet",0,IF(G{r}="max-snippet",IF(H{r}="",1,IF(N(H{r})=-1,1,'
                                f'IF(N(H{r})=0,0,IF(N(H{r})<{SNIPMIN},0.5,1)))),1)))')
        t['Unique description'] = f'=IF(OR({e},{E}=""),"",IF({g("Pages with this description")}>1,0,1))'
        wd = g('Words')
        t['Not a keyword list'] = f'=IF(OR({e},{E}=""),"",IF(OR(AND(N({cm})>={COMMAS},N({wd})/(N({cm})+1)<{WPC}),N({kwc})>=3),0,IF(N({kwc})=2,0.5,1)))'
        t['Opening answers the search'] = f'=IF(OR({e},F{r}=""),"",IF(F{r}="Yes",1,0))'
        t['CTR vs your site average'] = f'=IF(OR({e},{rat}=""),"",IF({rat}>={CTRG},1,IF({rat}>={CTRL},0.5,0)))'
        t['Keyword or topic named'] = f'=IF(OR({e},{C}="",{E}=""),"",IF(N({kwc})>=1,1,0.5))'
        t['Length'] = f'=IF(OR({e},{E}=""),"",IF(LEN({E})<{DMIN}/2,0,IF(AND(LEN({E})>={DMIN},LEN({E})<={DMAX}),1,0.5)))'
        t['Specific facts'] = f'=IF(OR({e},{E}=""),"",IF({num}="Yes",1,0.5))'
        t['Not boilerplate'] = f'=IF(OR({e},{g("Pages with the same opening")}="",N({g("Pages with this description")})>1),"",IF({g("Pages with the same opening")}>1,0,1))'
        t['Uses your description'] = f'=IF(OR({e},{gs}=""),"",IF({gs}="Uses your description",1,0.5))'
        t['Adds to the title'] = f'=IF(OR({e},{rep}=""),"",IF({rep}="Yes",0,1))'
        t['Year is current'] = f'=IF(OR({e},{yv}=""),"",IF({yv}>=YEAR({DATE}),1,0))'
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
        z = f'L{r}'
        ctrchk = f'{m["CTR vs your site average"]}{r}'
        snip = f'{m["Snippet allowed"]}{r}'
        ws[g('Priority')] = (
            f'=IF(OR({e},{sc}{r}=""),"",IF(AND(ISNUMBER({snip}),{snip}=0),"Fix now: snippet blocked",IF({CK[0]}{r}=0,"Fix now: missing description",'
            f'IF(AND(ISNUMBER({ctrchk}),{ctrchk}=0,N(J{r})>={BIGIMP}),"Rewrite first: low CTR, high impressions",IF({sc}{r}>={GA},"Healthy: monitor",'
            f'IF(AND(N({z})>=1,N({z})<{SD1}),"Protect: test carefully",IF(AND(N({z})>={SD1},N({z})<={SD2}),"Fix first: close to the top",'
            f'IF({sc}{r}<{REWRITE},"Rewrite the description","Improve when you can"))))))))')
        ws[g('Missed clicks (estimate)')] = f'=IF(OR({e},{rat}=""),"",IF({rat}>=1,0,ROUND(J{r}*({bav}-{ctr}),0)))'
        ws[g('Proposed characters')] = f'=IF(OR({e},{Mp}=""),"",LEN({Mp}))'
        pyr = f'SUMPRODUCT(MAX(ISNUMBER(SEARCH({YEARS},{Mp}))*{YEARS}))'
        pdig = '+'.join(f'ISNUMBER(FIND("{n}",{Mp}))' for n in range(10))
        issues = (f'_xlfn.TEXTJOIN("; ",TRUE,IF(LEN({Mp})>{DMAX},"may be cut off",""),IF(LEN({Mp})<{DMIN},"short",""),'
                  f'IF({C}="","",IF(ISNUMBER(SEARCH({C},{Mp})),"","topic not named")),'
                  f'IF(SUMPRODUCT(--($E${DL_FIRST}:$E${DL_LAST}={Mp}))-IF({E}={Mp},1,0)>0,"same as another page",""),'
                  f'IF(AND(LEN({Mp})-LEN(SUBSTITUTE({Mp},",",""))>={COMMAS},(LEN(TRIM({Mp}))-LEN(SUBSTITUTE(TRIM({Mp})," ",""))+1)/(LEN({Mp})-LEN(SUBSTITUTE({Mp},",",""))+1)<{WPC}),"reads like a list",""),'
                  f'IF(AND({Dt}<>"",LEFT({Mp},LEN(TRIM({Dt})))=TRIM({Dt})),"repeats the title",""),'
                  f'IF(({pdig})=0,"add a fact or number",""),IF(AND({pyr}>0,{pyr}<YEAR({DATE})),"old year",""))')
        ws[g('Proposed description check')] = f'=IF(OR({e},{Mp}=""),"",IF({issues}="","Ready to test",{issues}))'
        mc = g('Missed clicks (estimate)')
        ws[g('Opportunity (helper)')] = f'=IF(OR({e},N({mc})=0),"",{mc}+ROW()/100000)'
        ws[g('In CTR average (helper)')] = f'=IF({e},"",IFERROR(VLOOKUP(B{r},{S}!$F$13:$G${12 + len(PAGE_TYPES)},2,FALSE),"Yes"))'
    nf = {8: '0', 10: '#,##0', 11: '#,##0', 12: '0.0', NIN + 11: '0.0%', NIN + 12: '0.0%', NIN + 13: '0%', SC: '0', SC + 5: '#,##0', SC + 8: '0.00000'}
    K.style_body(ws, DL_FIRST, DL_LAST, len(HEAD), formula_cols=F_COLS, number_formats=nf, wrap_cols=(4, 5, 9, 13, SC + 3, SC + 7))
    ws.freeze_panes = 'B5'
    ws.auto_filter.ref = f'A4:{L(len(HEAD))}{DL_LAST}'
    K.dropdown(ws, f'B{DL_FIRST}:B{DL_LAST}', f'{S}!$F$13:$F${12 + len(PAGE_TYPES)}')
    K.dropdown(ws, f'F{DL_FIRST}:F{DL_LAST}', f'{S}!$M$6:$M$7')
    K.dropdown(ws, f'G{DL_FIRST}:G{DL_LAST}', f'{S}!$N$6:$N$8', 'From the robots meta tag. None = no snippet rule.')
    K.whole_number(ws, f'H{DL_FIRST}:H{DL_LAST}', -1, 5000, 'max-snippet value in characters: -1 = no limit, 0 = no snippet.')
    chk = f'{CK[0]}{DL_FIRST}:{CK[-1]}{DL_LAST}'
    ws.conditional_formatting.add(chk, CellIsRule(operator='equal', formula=['1'], fill=PatternFill('solid', fgColor='D9F2C4')))
    ws.conditional_formatting.add(chk, CellIsRule(operator='equal', formula=['0.5'], fill=PatternFill('solid', fgColor='FFF4CC')))
    ws.conditional_formatting.add(chk, FormulaRule(formula=[f'AND(ISNUMBER({CK[0]}{DL_FIRST}),{CK[0]}{DL_FIRST}=0)'], fill=PatternFill('solid', fgColor='F8D7D3'), font=Font(name=K.FONT, bold=True, color='9B2C1F')))
    scol = L(SC)
    ws.conditional_formatting.add(f'{scol}{DL_FIRST}:{scol}{DL_LAST}', ColorScaleRule(start_type='num', start_value=30, start_color='F8D7D3', mid_type='num', mid_value=70, mid_color='FFF4CC', end_type='num', end_value=100, end_color='B7E4A0'))
    gcol = f'{L(SC + 1)}{DL_FIRST}:{L(SC + 1)}{DL_LAST}'
    for val, col in (('A', '9BE07A'), ('B', 'D9F2C4'), ('C', 'FFF4CC'), ('D', 'F8D7D3')):
        ws.conditional_formatting.add(gcol, CellIsRule(operator='equal', formula=[f'"{val}"'], fill=PatternFill('solid', fgColor=col), font=Font(name=K.FONT, bold=True)))
    pc = L(SC + 4)
    pr = f'{pc}{DL_FIRST}:{pc}{DL_LAST}'
    for start, n, fill, fc in (('Fix now', 7, '9B2C1F', 'FFFFFF'), ('Rewrite first', 13, 'F8D7D3', '9B2C1F'), ('Fix first', 9, 'FCE4D6', '9B2C1F'), ('Healthy', 7, 'D9F2C4', '1F1F1F')):
        ws.conditional_formatting.add(pr, FormulaRule(formula=[f'LEFT({pc}{DL_FIRST},{n})="{start}"'], fill=PatternFill('solid', fgColor=fill), font=Font(name=K.FONT, bold=True, color=fc)))
    ch = m['Characters']
    ws.conditional_formatting.add(f'{ch}{DL_FIRST}:{ch}{DL_LAST}', FormulaRule(formula=[f'AND($A{DL_FIRST}<>"",OR({ch}{DL_FIRST}<{DMIN},{ch}{DL_FIRST}>{DMAX}))'], font=Font(name=K.FONT, bold=True, color='B45309')))
    pcc = m['Proposed description check']
    ws.conditional_formatting.add(f'{pcc}{DL_FIRST}:{pcc}{DL_LAST}', CellIsRule(operator='equal', formula=['"Ready to test"'], fill=PatternFill('solid', fgColor='D9F2C4'), font=Font(name=K.FONT, bold=True)))
    ws.conditional_formatting.add(f'{pcc}{DL_FIRST}:{pcc}{DL_LAST}', FormulaRule(formula=[f'AND({pcc}{DL_FIRST}<>"",{pcc}{DL_FIRST}<>"Ready to test")'], fill=PatternFill('solid', fgColor='FFF4CC')))
    ws.column_dimensions[L(SC + 8)].hidden = True
    ws.column_dimensions[L(SC + 9)].hidden = True
    return ws


def builder_sheet(wb):
    ws = wb.create_sheet('Bulk Builder')
    ws.sheet_view.showGridLines = False
    K.title_block(ws, 'Bulk builder', 'For many similar pages (products, tours, listings): pick a template and fill the facts. Each row builds a unique description with a length check and a duplicate check. Templates live on Settings.')
    head = ['URL or ID', 'Template', 'Name', 'Fact 1', 'Fact 2', 'Number (price, count, days, date)', 'Place or audience', 'Offer or next step',
            'Built description', 'Characters', 'Fit', 'Duplicate in this list?', 'Same opening as another row?']
    fc = (9, 10, 11, 12, 13)
    K.header_row(ws, 4, head, formula_cols=fc, widths=[26, 16, 26, 32, 32, 14, 18, 30, 64, 9, 14, 11, 12])
    tpl_rng = f'{S}!$A${TPL_ROW}:$B${TPL_ROW + 14}'
    for r in range(BB_FIRST, BB_LAST + 1):
        i = r - BB_FIRST
        if i < len(BUILD):
            for col, v in enumerate(BUILD[i], 1):
                if v not in (None, ''):
                    ws.cell(row=r, column=col, value=v)
        e = f'OR(B{r}="",C{r}="")'
        tpl = f'IFERROR(VLOOKUP(B{r},{tpl_rng},2,FALSE),"")'
        fill = tpl
        for ph, col in (('name', 'C'), ('fact1', 'D'), ('fact2', 'E'), ('number', 'F'), ('place', 'G'), ('offer', 'H')):
            fill = f'SUBSTITUTE({fill},"{{{ph}}}",{col}{r})'
        clean = fill
        for a, b in ((' .', '.'), (' ,', ','), (', .', '.'), (',.', '.'), (': .', '.'), (':.', '.'), ('..', '.'), ('. .', '.'), (' in :', ':'), (' in .', '.'), ('Price: .', '')):
            clean = f'SUBSTITUTE({clean},"{a}","{b}")'
        clean = f'TRIM(SUBSTITUTE(SUBSTITUTE({clean},"  "," "),"..","."))'
        ws.cell(row=r, column=9, value=f'=IF(OR({e},{tpl}=""),"",UPPER(LEFT({clean},1))&MID({clean},2,500))')
        ws.cell(row=r, column=10, value=f'=IF(I{r}="","",LEN(I{r}))')
        ws.cell(row=r, column=11, value=f'=IF(I{r}="","",IF(J{r}>{DMAX},"May be cut off",IF(J{r}<{DMIN},"Short","Fits")))')
        ws.cell(row=r, column=12, value=f'=IF(I{r}="","",IF(SUMPRODUCT(--($I${BB_FIRST}:$I${BB_LAST}=I{r}))>1,"Yes","No"))')
        ws.cell(row=r, column=13, value=f'=IF(OR(I{r}="",LEN(I{r})<{OPEN}),"",IF(SUMPRODUCT(--(LEFT($I${BB_FIRST}:$I${BB_LAST},{OPEN})=LEFT(I{r},{OPEN})))>1,"Yes","No"))')
    K.style_body(ws, BB_FIRST, BB_LAST, len(head), formula_cols=fc, wrap_cols=(4, 5, 8, 9))
    K.dropdown(ws, f'B{BB_FIRST}:B{BB_LAST}', f'{S}!$A${TPL_ROW}:$A${TPL_ROW + 14}')
    k = f'K{BB_FIRST}:K{BB_LAST}'
    ws.conditional_formatting.add(k, CellIsRule(operator='equal', formula=['"Fits"'], fill=PatternFill('solid', fgColor='D9F2C4'), font=Font(name=K.FONT, bold=True)))
    ws.conditional_formatting.add(k, FormulaRule(formula=[f'AND(K{BB_FIRST}<>"",K{BB_FIRST}<>"Fits")'], fill=PatternFill('solid', fgColor='FFF4CC')))
    for col in 'LM':
        ws.conditional_formatting.add(f'{col}{BB_FIRST}:{col}{BB_LAST}', CellIsRule(operator='equal', formula=['"Yes"'], fill=PatternFill('solid', fgColor='F8D7D3'), font=Font(name=K.FONT, bold=True, color='9B2C1F')))
    ws.freeze_panes = 'B5'
    return ws


def test_sheet(wb):
    ws = wb.create_sheet('Test Log')
    ws.sheet_view.showGridLines = False
    K.title_block(ws, 'Description test log', 'Log every description change with the Search Console numbers for 28 days before and 28 days after. The verdict waits long enough and warns you when the position moved too.')
    head = ['URL', 'Old description', 'New description', 'Date changed', 'Status', 'Impressions before', 'Clicks before', 'Position before',
            'Impressions after', 'Clicks after', 'Position after', 'Notes', 'CTR before', 'CTR after', 'CTR change', 'Position change',
            'Days live', 'New description characters', 'Verdict']
    fc = tuple(range(13, 20))
    K.header_row(ws, 4, head, formula_cols=fc, widths=[40, 44, 44, 12, 10, 11, 9, 9, 11, 9, 9, 32, 9, 9, 9, 9, 8, 11, 34])
    for r in range(TS_FIRST, TS_LAST + 1):
        i = r - TS_FIRST
        if i < len(TESTS):
            u, old, new, dt, st, ib, cb, pb, ia, ca, pa, note = TESTS[i]
            vals = [P[u][0], old, new, d(dt), st, ib, cb, pb, ia, ca, pa, note]
            for col, v in enumerate(vals, 1):
                if v not in (None, ''):
                    ws.cell(row=r, column=col, value=v)
            for col, val in ((2, old), (3, new)):
                if not val:
                    c = ws.cell(row=r, column=col, value=f"=IFERROR(INDEX({dl('E')},MATCH(A{r},{dl('A')},0)),\"\")")
        e = f'A{r}=""'
        ws.cell(row=r, column=13, value=f'=IF(OR({e},N(F{r})=0),"",G{r}/F{r})')
        ws.cell(row=r, column=14, value=f'=IF(OR({e},N(I{r})=0),"",J{r}/I{r})')
        ws.cell(row=r, column=15, value=f'=IF(OR(M{r}="",N{r}="",N(M{r})=0),"",N{r}/M{r}-1)')
        ws.cell(row=r, column=16, value=f'=IF(OR({e},H{r}="",K{r}=""),"",K{r}-H{r})')
        ws.cell(row=r, column=17, value=f'=IF(OR({e},D{r}=""),"",{DATE}-D{r})')
        ws.cell(row=r, column=18, value=f'=IF(OR({e},C{r}=""),"",LEN(C{r}))')
        ws.cell(row=r, column=19, value=(
            f'=IF({e},"",IF(E{r}="Reverted","Reverted",IF(OR(E{r}="Planned",D{r}="",N(Q{r})<0),"Not live yet",'
            f'IF(Q{r}<{WAIT},"Too early: wait "&({WAIT}-Q{r})&" more days",IF(O{r}="","Add the after numbers",'
            f'IF(ABS(N(P{r}))>{POSMOVE},"Position moved: not a fair test",IF(O{r}>={WIN},"Win: keep the new description",'
            f'IF(O{r}<=-{WIN},"Loss: revert or try again","No clear change"))))))))'))
    K.style_body(ws, TS_FIRST, TS_LAST, len(head), formula_cols=fc,
                 number_formats={4: 'dd mmm yyyy', 6: '#,##0', 7: '#,##0', 8: '0.0', 9: '#,##0', 10: '#,##0', 11: '0.0', 13: '0.0%', 14: '0.0%', 15: '+0%;-0%;0%', 16: '+0.0;-0.0;0.0', 17: '0'},
                 wrap_cols=(2, 3, 12, 19))
    for i in range(len(TESTS)):
        for col in (2, 3):
            c = ws.cell(row=TS_FIRST + i, column=col)
            if isinstance(c.value, str) and c.value.startswith('='):
                c.fill = K.FORMULA_FILL
    K.dropdown(ws, f'A{TS_FIRST}:A{TS_LAST}', dl('A'))
    K.dropdown(ws, f'E{TS_FIRST}:E{TS_LAST}', f'{S}!$O$6:$O$8')
    v = f'S{TS_FIRST}:S{TS_LAST}'
    ws.conditional_formatting.add(v, FormulaRule(formula=[f'LEFT(S{TS_FIRST},3)="Win"'], fill=PatternFill('solid', fgColor='D9F2C4'), font=Font(name=K.FONT, bold=True)))
    ws.conditional_formatting.add(v, FormulaRule(formula=[f'LEFT(S{TS_FIRST},4)="Loss"'], fill=PatternFill('solid', fgColor='F8D7D3'), font=Font(name=K.FONT, bold=True, color='9B2C1F')))
    ws.conditional_formatting.add(v, FormulaRule(formula=[f'LEFT(S{TS_FIRST},8)="Position"'], fill=PatternFill('solid', fgColor='FFF4CC')))
    ws.freeze_panes = 'B5'
    ws.auto_filter.ref = f'A4:S{TS_LAST}'
    return ws


def chart(ws, title, ytitle, cat_col, val_cols, r1, r2, anchor, colors, horiz, titles, h=7.5, stacked=False, pct=False):
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
    if pct:
        ch.y_axis.numFmt = '0%'
    ch.height, ch.width = h, 16
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
    for c, w in zip('ABCDEFGHIJ', [42, 12, 3, 44, 26, 9, 9, 11, 30, 3]):
        ws.column_dimensions[c].width = w
    m = M
    sc, gr, pr = m['Score (0 to 100)'], m['Grade'], m['Priority']
    kpis = [
        ('Pages checked', f'=COUNTA({dl("A")})', '0'),
        ('Average score', f'=IFERROR(ROUND(AVERAGE({dl(sc)}),0),0)', '0'),
        ('Grade A or B pages', f'=COUNTIF({dl(gr)},"A")+COUNTIF({dl(gr)},"B")', '0'),
        ('Grade C or D pages', f'=COUNTIF({dl(gr)},"C")+COUNTIF({dl(gr)},"D")', '0'),
        ('Pages with no meta description', f'=COUNTIF({dl(CK[0])},0)', '0'),
        ('Pages with snippets blocked or too tight', f'=COUNTIF({dl(m["Snippet allowed"])},0)+COUNTIF({dl(m["Snippet allowed"])},0.5)', '0'),
        ('Pages sharing a description', f'=COUNTIF({dl(m["Pages with this description"])},">1")', '0'),
        ('Pages with a boilerplate opening', f'=COUNTIF({dl(m["Not boilerplate"])},0)', '0'),
        ('Keyword lists', f'=COUNTIF({dl(m["Not a keyword list"])},0)', '0'),
        ('Descriptions outside the length band', f'=COUNTIF({dl(m["Length"])},0.5)', '0'),
        ('Snippets written from the page (of those you pasted)', f'=COUNTIF({dl(m["Google snippet"])},"Written*")', '0'),
        ('Rewrite first: low CTR, high impressions', f'=COUNTIF({dl(pr)},"Rewrite first*")', '0'),
        ('Missed clicks per 28 days (estimate)', f'=SUM({dl(m["Missed clicks (estimate)"])})', '#,##0'),
        ('Description tests won', f"=COUNTIF('Test Log'!$S${TS_FIRST}:$S${TS_LAST},\"Win*\")", '0'),
        ('Bulk Builder rows that are duplicates', f"=COUNTIF('Bulk Builder'!$L${BB_FIRST}:$L${BB_LAST},\"Yes\")", '0'),
    ]
    ws['A4'] = 'KEY NUMBERS'
    ws['A4'].font = K.f(10, True, K.DEEP)
    for i, (label, fml, fmt) in enumerate(kpis):
        r = 5 + i
        ws.cell(row=r, column=1, value=label).font = K.f(10)
        c = ws.cell(row=r, column=2, value=fml)
        c.number_format, c.font, c.fill, c.border = fmt, K.f(11, True), K.FORMULA_FILL, K.BORDER
    ws['D4'] = 'BIGGEST CLICK OPPORTUNITIES (CTR below your own band average)'
    ws['D4'].font = K.f(10, True, K.DEEP)
    for j, h in enumerate(['URL', 'Focus keyword', 'CTR', 'Band avg', 'Missed clicks', 'Priority']):
        c = ws.cell(row=5, column=4 + j, value=h)
        c.font, c.fill = K.f(10, True, 'FFFFFF'), K.HEAD_F
    op = dl(m['Opportunity (helper)'])
    for k in range(1, 11):
        r = 5 + k
        mt = f'MATCH(LARGE({op},{k}),{op},0)'
        for j, col in enumerate(['A', 'C', m['CTR'], m['Band average CTR'], m['Missed clicks (estimate)'], pr]):
            c = ws.cell(row=r, column=4 + j, value=f'=IFERROR(INDEX({dl(col)},{mt}),"")')
            c.border, c.fill, c.font = K.BORDER, K.FORMULA_FILL, K.f(9, j == 0)
            c.number_format = ['@', '@', '0.0%', '0.0%', '#,##0', '@'][j]
    top = 23
    ws.cell(row=top - 1, column=1, value='YOUR CTR BY POSITION BAND (pages in the averages with enough impressions)').font = K.f(10, True, K.DEEP)
    for j, h in enumerate(['Position band', 'Pages', 'Impressions', 'Clicks', 'CTR']):
        c = ws.cell(row=top, column=1 + j, value=h)
        c.font, c.fill = K.f(10, True, 'FFFFFF'), K.HEAD_F
    bcol = dl(m['Position band'])
    for i in range(len(BANDS)):
        r = top + 1 + i
        ws.cell(row=r, column=1, value=f'={S}!G{6 + i}')
        crit = f'{dl("J")},">="&{MINIMP},{dl(m["In CTR average (helper)"])},"Yes"'
        ws.cell(row=r, column=2, value=f'=COUNTIFS({bcol},A{r},{crit})')
        ws.cell(row=r, column=3, value=f'=SUMIFS({dl("J")},{bcol},A{r},{crit})')
        ws.cell(row=r, column=4, value=f'=SUMIFS({dl("K")},{bcol},A{r},{crit})')
        ws.cell(row=r, column=5, value=f'=IF(C{r}=0,0,D{r}/C{r})')
        for cc, fmt in ((1, '@'), (2, '0'), (3, '#,##0'), (4, '#,##0'), (5, '0.0%')):
            cell = ws.cell(row=r, column=cc)
            cell.border, cell.fill, cell.number_format = K.BORDER, K.FORMULA_FILL, fmt
    t2 = top + len(BANDS) + 3
    for j, h in enumerate(['Check', 'Pages to fix', 'Partly']):
        c = ws.cell(row=t2, column=1 + j, value=h)
        c.font, c.fill = K.f(10, True, 'FFFFFF'), K.HEAD_F
    for i, col in enumerate(CK):
        r = t2 + 1 + i
        ws.cell(row=r, column=1, value=f'={S}!A{CHK_ROW + i}').border = K.BORDER
        for cc, val in ((2, 0), (3, 0.5)):
            c = ws.cell(row=r, column=cc, value=f'=COUNTIF({dl(col)},{val})')
            c.border, c.fill = K.BORDER, K.FORMULA_FILL
    ws.conditional_formatting.add(f'B{t2 + 1}:B{t2 + NCH}', ColorScaleRule(start_type='num', start_value=0, start_color='FFFFFF', end_type='num', end_value=6, end_color='E07A5F'))
    c1 = chart(ws, 'Your CTR by position band', 'CTR', 1, [5], top + 1, top + len(BANDS), 'K4', [K.GREEN], False, False, pct=True)
    c1.y_axis.scaling.min = 0
    chart(ws, 'Pages failing each check', 'Pages', 1, [2, 3], t2 + 1, t2 + NCH, 'K21', ['E07A5F', 'F2C94C'], True, True, h=11, stacked=True)
    return ws


def build(path, asset, url):
    wb = K.new_book()
    lab_sheet(wb)
    builder_sheet(wb)
    test_sheet(wb)
    dashboard_sheet(wb)
    settings_sheet(wb)
    K.prompts_sheet(wb, asset['prompts'], url)
    K.checklist_sheet(wb, list(asset['checklist']))
    K.sources_sheet(wb, asset['sources'], [
        ('Demo data', 'TrekTrail and every page in the demo are fictional (.example domain). All descriptions, prices, impressions, clicks, positions and test results are illustrative, not real data.', ''),
        ('Score', 'Weighted share of the 13 checks a description passes (pass 1, partly 0.5, fix 0). Checks without data are left out. Weights, grade bands and priority rules live on Settings and are assumptions to tune.', ''),
        ('Length band', 'Google says there is no limit on meta description length and that snippets are truncated to fit the device. The 70 to 160 character band is an assumption of this kit. An Ahrefs study (2020, 20,000 keywords) found that keeping descriptions within length limits barely changed how often Google rewrote them.', 'https://ahrefs.com/blog/meta-description-study/'),
        ('Snippet controls', 'nosnippet stops Google showing a snippet, max-snippet sets a maximum length in characters, data-nosnippet hides parts of a page. Google says a page must be indexed and eligible to show with a snippet to be a supporting link in AI Overviews and AI Mode. The 50 character limit for a tight max-snippet is an assumption.', ''),
        ('CTR comparison', 'CTR is compared with the average CTR of your own pages in the same position band (pages with at least 100 impressions; home and about pages excluded), never with an outside benchmark. Missed clicks = impressions x (band average CTR minus page CTR): an estimate, not a promise.', ''),
        ('Description tests', 'Search Console data is compared for 28 days before and after a change. A test is called fair only when the average position moved by 2 or less. Both numbers are assumptions you can change.', ''),
    ])
    K.start_here(
        wb, 'Meta Description Kit',
        [
            'This workbook checks every meta description on your site against 13 rules that matter for Google and for AI search: a description that exists and is unique, snippets that are allowed, no keyword lists or boilerplate openings, real facts, a page opening that answers the search, and whether Google uses your description at all. It compares each page CTR with your own average for the same position band, so you know which descriptions cost you clicks.',
            f'It ships with demo data for a fictional trek operator ({len(P)} pages, {len(BUILD)} bulk built descriptions and {len(TESTS)} tests) so you can see every check working. Clear the yellow demo cells when you are ready.',
        ],
        [
            ('Description Lab', 'One row per page with 500 ready rows: title, description, snippet controls, the snippet Google shows and Search Console numbers, plus 14 measures, 13 checks, score, grade, fixes, priority, missed clicks and a check of your proposed description.'),
            ('Bulk Builder', 'Write unique descriptions for many similar pages from 8 templates, with length, duplicate and same opening checks.'),
            ('Test Log', 'Log each change with 28 days before and after. The verdict waits, compares CTR and warns when the position moved too.'),
            ('Dashboard', 'Key numbers, the 10 biggest click opportunities, your CTR by position band and pages failing each check, with two charts.'),
            ('Settings', 'Analysis date, length band, opening length, snippet and list rules, CTR rules, grades, the 13 check weights with rules and fixes, templates and lists.'),
            ('AI Prompts', 'Prompts for ChatGPT, Claude or Gemini to write, fix, scale and test meta descriptions.'),
            ('Checklist', 'The meta description checklist as a tick list with automatic progress.'),
            ('Sources', 'Where facts come from and which numbers are assumptions.'),
        ],
        [
            'Look at the demo on Description Lab, Bulk Builder, Test Log and the Dashboard, then clear the yellow demo cells.',
            'On Settings, set the analysis date. Change the bands and weights only if your site needs it.',
            'Export pages from Search Console (Performance, Pages, last 28 days) and add URL, impressions, clicks and position.',
            'Paste each title and meta description from the page source, the snippet control from the robots meta tag and, for key pages, the snippet Google shows.',
            'Sort by Priority. Start with Fix now, then Rewrite first and Fix first. Write a proposed description until it says Ready to test.',
            'For many similar pages, build descriptions on Bulk Builder and copy them into your CMS or import file.',
            'Change one description at a time on important pages, log it on Test Log and judge it after 28 days.',
        ],
        url,
    )
    order = ['Start Here', 'Description Lab', 'Bulk Builder', 'Test Log', 'Dashboard', 'Settings', 'AI Prompts', 'Checklist', 'Sources']
    wb._sheets = [wb[n] for n in order]
    wb.active = 0
    for ws in wb.worksheets:
        ws.sheet_properties.tabColor = K.GREEN if ws.title in order[:5] else 'A6EF39'
    wb.save(path)


PREVIEW = {'sheet': 'Description Lab', 'header_row': 4, 'rows': 12,
           'cols': [3, 5, NIN + 1, SC, SC + 1, SC + 2, SC + 5, SC + 4],
           'formula_idx': [2, 3, 4, 5, 6, 7]}


def check(wb):
    """Assert the worked examples used in the guide."""
    a = wb['Description Lab']
    v = lambda h, r: a[f'{M[h]}{r}'].value
    r = 10   # best time for kedarkantha trek
    assert v('Characters', r) == 135 and v('Commas', r) == 5 and v('Words', r) == 16 and v('Has a number?', r) == 'No', (v('Characters', r), v('Words', r))
    assert v('Not a keyword list', r) == 0 and v('Opening answers the search', r) == 0 and v('Google snippet', r) == 'Written from the page', r
    assert v('Position band', r) == '4 to 10' and abs(v('Band average CTR', r) - 4120 / 132000) < 1e-9, v('Band average CTR', r)
    assert round(v('CTR vs band', r), 2) == 0.28 and v('Missed clicks (estimate)', r) == 402, v('Missed clicks (estimate)', r)
    assert v('Score (0 to 100)', r) == 68 and v('Grade', r) == 'C' and v('Fixes needed', r) == 5, v('Score (0 to 100)', r)
    assert v('Priority', r) == 'Rewrite first: low CTR, high impressions', v('Priority', r)
    assert v('Fixes in priority order', r) == ('Not a keyword list; Opening answers the search; CTR vs your site average; '
                                              'Specific facts (partly); Uses your description (partly)'), v('Fixes in priority order', r)
    assert v('Proposed characters', r) == 135 and v('Proposed description check', r) == 'Ready to test', v('Proposed description check', r)
    # other pages used in the guide
    assert v('Description present', 6) == 0 and v('Priority', 6) == 'Fix now: missing description' and v('Missed clicks (estimate)', 6) == 292, v('Priority', 6)
    assert v('Pages with the same opening', 8) == 2 and v('Not boilerplate', 9) == 0, v('Pages with the same opening', 8)
    assert v('Repeats the title?', 13) == 'Yes' and v('Adds to the title', 13) == 0 and v('Proposed description check', 13) == 'Ready to test', v('Repeats the title?', 13)
    assert v('Snippet allowed', 15) == 0 and v('Priority', 15) == 'Fix now: snippet blocked' and v('Score (0 to 100)', 15) == 75, v('Priority', 15)
    assert v('Snippet allowed', 16) == 0.5 and v('Year is current', 16) == 0, v('Snippet allowed', 16)
    assert v('Length', 17) == 0 and v('CTR vs band', 17) is None, v('Length', 17)
    assert v('Not a keyword list', 18) == 1 and v('Length', 18) == 0.5 and v('Characters', 18) == 255, v('Not a keyword list', 18)
    d = wb['Dashboard']
    assert d['B17'].value == 990 and d['B5'].value == 14 and d['C25'].value == 132000, (d['B17'].value, d['C25'].value)
    t = wb['Test Log']
    assert t['S5'].value == 'Win: keep the new description' and round(t['O5'].value, 2) == 0.45, (t['S5'].value, t['O5'].value)
    assert t['S6'].value == 'Too early: wait 17 more days' and t['S7'].value == 'No clear change' and t['S9'].value == 'Not live yet', (t['S6'].value, t['S7'].value)
    b = wb['Bulk Builder']
    assert b['I5'].value == ('Kedarkantha trek in Uttarakhand: 6 days, snow summit at 3,800 m. Stays, meals and permits included. '
                             'From Rs 9,500 with free date changes.') and b['J5'].value == 137, b['I5'].value
    assert b['I9'].value == 'Kuari Pass trek in Uttarakhand: 6 days, views of Nanda Devi from the pass. From Rs 9,500.', b['I9'].value
    assert b['K11'].value == 'May be cut off' and b['L14'].value == 'Yes' and b['L6'].value == 'No', (b['K11'].value, b['L14'].value)
    for r in range(BB_FIRST, BB_FIRST + len(BUILD)):
        assert '{' not in b[f'I{r}'].value and '..' not in b[f'I{r}'].value, b[f'I{r}'].value
