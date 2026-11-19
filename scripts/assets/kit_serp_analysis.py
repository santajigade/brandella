"""SERP Analysis Kit workbook (asset 05).

SERP Log: one row per result on page one (500 rows). The sheet pulls the domain, works out page age,
counts weak signals (dated, no named author, no first hand experience, forum result, few links) and rates each
result Strong, Average or Beatable. Keywords: one row per keyword with SERP features; the sheet finds the
dominant format and site type, the implied intent, an Opportunity score and a verdict. Format Mix counts formats
and site types per keyword. AI Answer Check compares the links in AI answers with the organic top 10.
Page Plan turns one keyword into a brief.
"""
import datetime
from openpyxl.styles import PatternFill, Font, Alignment
from openpyxl.formatting.rule import CellIsRule, ColorScaleRule, FormulaRule
from openpyxl.chart import BarChart, Reference
from openpyxl.utils import get_column_letter as L
import kitlib as K

LOG_FIRST, LOG_LAST = 5, 504   # SERP Log
KW_FIRST, KW_LAST = 5, 104     # Keywords and Format Mix
AI_FIRST, AI_LAST = 5, 204     # AI Answer Check
S = 'Settings'
LG = "'SERP Log'"
KWS = 'Keywords'
FM = "'Format Mix'"

DATE, FRESH, LOWRD, BEAT, AVG, CLEAR, MULT, MINRES = (f'{S}!$B${r}' for r in range(5, 13))
W1, W2, W3, W4, W5, WT = (f'{S}!$B${r}' for r in range(15, 21))
GO, ANGLE = f'{S}!$B$23', f'{S}!$B$24'

FORMATS = [('Guide or how to', 'Informational'), ('Best of list', 'Commercial'), ('List post', 'Informational'),
           ('Comparison or review', 'Commercial'), ('Checklist or template', 'Informational'), ('Tool or calculator', 'Transactional'),
           ('Product page', 'Transactional'), ('Category page', 'Transactional'), ('Video', 'Informational'),
           ('Forum thread', 'Informational'), ('News', 'Informational'), ('Definition', 'Informational')]
SITE_TYPES = ['Brand or retailer', 'Publisher or blog', 'Specialist business', 'Forum or community', 'Video platform',
              'Marketplace or directory', 'Government or education']
FEATURES = ['AI Overview', 'Featured snippet', 'People also ask', 'Video results', 'Image results', 'Local pack', 'Product or shopping results']
ENGINES = ['Google AI Overview', 'Google AI Mode', 'ChatGPT', 'Gemini', 'Perplexity', 'Copilot', 'Other']

# Demo: TrailNest, a fictional online trekking gear store in India. Every site, number and date is illustrative.
# keyword, volume, kd, country/device, date, your pos, your url, your RD, 7 features
KEYWORDS = [
    ('best trekking shoes for beginners', 2900, 34, 'India, mobile', '2026-11-18', 18, '/blog/best-trekking-shoes/', 12, ['Yes', 'No', 'Yes', 'Yes', 'Yes', 'No', 'Yes']),
    ('kedarkantha trek packing list', 1900, 18, 'India, mobile', '2026-11-18', None, '', 12, ['Yes', 'Yes', 'Yes', 'Yes', 'No', 'No', 'No']),
    ('how to choose a trekking backpack', 1300, 26, 'India, mobile', '2026-11-18', 9, '/blog/choose-trekking-backpack/', 12, ['Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'No', 'Yes']),
    ('trekking pole height chart', 720, 12, 'India, mobile', '2026-11-19', None, '', 12, ['Yes', 'Yes', 'Yes', 'No', 'Yes', 'No', 'No']),
    ('waterproof jacket for trekking', 3600, 48, 'India, mobile', '2026-11-19', 24, '/rain-jackets/', 8, ['No', 'No', 'Yes', 'No', 'Yes', 'No', 'Yes']),
]
SITE = 'https://'
# kw index, pos, url, title, site type, format, angle, words, updated, author, first hand, rich, rd, ai linked
R = [
    (0, 1, 'trailtested.example/best-trekking-shoes/', 'Best Trekking Shoes for Beginners (Tested on 12 Treks)', 'Publisher or blog', 'Best of list', 'Lab and field tested picks', 4200, '2026-09-01', 'Yes', 'Yes', 'Yes', 310, 'Yes'),
    (0, 2, 'gearlane.example/trekking-shoes/', 'Trekking Shoes: Buy Online', 'Brand or retailer', 'Category page', 'Big range with filters', 600, '2026-10-01', 'No', 'No', 'Yes', 140, 'No'),
    (0, 3, 'hikeindia.example/best-trekking-shoes-india/', '9 Best Trekking Shoes in India Under 5,000', 'Publisher or blog', 'Best of list', 'Budget picks in rupees', 2800, '2025-04-10', 'No', 'No', 'No', 22, 'Yes'),
    (0, 4, 'videohub.example/watch?v=trek-shoes', 'Trekking Shoes for Beginners: What to Buy', 'Video platform', 'Video', 'Buying guide on camera', None, '2025-12-01', 'Yes', 'Yes', 'No', None, 'No'),
    (0, 5, 'trekkersforum.example/t/first-trekking-shoes', 'First trekking shoes, what worked for you?', 'Forum or community', 'Forum thread', 'Beginners share what worked', 1100, '2024-08-01', 'No', 'Yes', 'No', 4, 'Yes'),
    (0, 6, 'shoereviewhub.example/trekking/', 'Top 10 Trekking Shoes', 'Publisher or blog', 'Best of list', 'Generic top 10', 1900, '2024-02-11', 'No', 'No', 'Yes', 18, 'No'),
    (0, 7, 'bigmart.example/trekking-shoes/', 'Trekking Shoes at Lowest Prices', 'Marketplace or directory', 'Category page', 'Lowest prices', 300, '2026-11-01', 'No', 'No', 'Yes', 900, 'No'),
    (0, 8, 'mountainmiles.example/blog/trekking-shoes-guide/', 'Trekking Shoes Guide: Pick by Trek Type', 'Publisher or blog', 'Best of list', 'Shoes by trek type', 2400, '2025-08-20', 'Yes', 'Yes', 'No', 24, 'Yes'),
    (0, 9, 'lifestylemag.example/best-hiking-shoes/', 'Stylish Hiking Shoes We Love', 'Publisher or blog', 'Best of list', 'Style led picks', 1500, '2023-11-30', 'No', 'No', 'No', 60, 'No'),
    (0, 10, 'snowtrails.example/blog/choosing-trekking-shoes/', 'How to Choose Trekking Shoes: Fit and Break In', 'Specialist business', 'Guide or how to', 'Fit and break in tips', 2000, '2025-06-02', 'Yes', 'Yes', 'No', 54, 'No'),
    (1, 1, 'trekhimalaya.example/kedarkantha-packing-list/', 'Kedarkantha Trek Packing List: What to Carry', 'Specialist business', 'Checklist or template', 'Trek leader list by day', 2100, '2025-12-10', 'Yes', 'Yes', 'No', 38, 'Yes'),
    (1, 2, 'mountainmiles.example/blog/kedarkantha-what-to-pack/', 'What to Pack for Kedarkantha', 'Publisher or blog', 'Checklist or template', 'Winter layering focus', 1600, '2024-01-15', 'No', 'No', 'No', 12, 'No'),
    (1, 3, 'trekkersforum.example/t/kedarkantha-packing', 'Kedarkantha packing, what did you carry?', 'Forum or community', 'Forum thread', 'Real trekkers share kit lists', 900, '2025-02-01', 'No', 'Yes', 'No', 3, 'No'),
    (1, 4, 'videohub.example/watch?v=kk-pack', 'Kedarkantha Packing Walkthrough', 'Video platform', 'Video', 'Packing on camera', None, '2024-11-20', 'Yes', 'Yes', 'No', None, 'No'),
    (1, 5, 'snowtrails.example/kedarkantha-trek-guide/', 'Kedarkantha Trek Guide: Route, Cost and Kit', 'Specialist business', 'Guide or how to', 'Full trek guide, short kit section', 3500, '2026-02-10', 'Yes', 'Yes', 'No', 54, 'Yes'),
    (1, 6, 'travelnotes.example/kedarkantha-checklist/', 'Kedarkantha Checklist (Printable)', 'Publisher or blog', 'Checklist or template', 'Printable checklist', 1200, '2023-09-05', 'No', 'No', 'No', 5, 'No'),
    (1, 7, 'himalayanhikes.example/packing-list-for-winter-treks/', 'Packing List for Winter Treks', 'Specialist business', 'Checklist or template', 'Generic winter trek list', 1800, '2024-06-12', 'No', 'No', 'No', 22, 'No'),
    (1, 8, 'backpackbuzz.example/kedarkantha-trek/', 'Kedarkantha in December: Trip Report and Kit', 'Publisher or blog', 'Checklist or template', 'Trip report with kit list', 2600, '2025-03-18', 'No', 'Yes', 'No', 9, 'No'),
    (1, 9, 'gearlane.example/kedarkantha-kit/', 'Shop the Kedarkantha Kit', 'Brand or retailer', 'Category page', 'Shop the whole kit', 400, '2026-08-01', 'No', 'No', 'Yes', 15, 'No'),
    (1, 10, 'trekkersforum.example/t/kedarkantha-december', 'Kedarkantha in December, how cold?', 'Forum or community', 'Forum thread', 'Weather and conditions', 700, '2024-12-02', 'No', 'Yes', 'No', 2, 'No'),
    (2, 1, 'trailtested.example/how-to-choose-a-backpack/', 'How to Choose a Backpack for Trekking', 'Publisher or blog', 'Guide or how to', 'Fit, volume and frame explained', 3800, '2026-05-01', 'Yes', 'Yes', 'No', 220, 'Yes'),
    (2, 2, 'gearlane.example/expert-advice/backpacks/', 'Backpacks: Expert Advice', 'Brand or retailer', 'Guide or how to', 'Retailer expert advice', 2500, '2026-01-15', 'Yes', 'Yes', 'No', 140, 'Yes'),
    (2, 3, 'videohub.example/watch?v=pack-fit', 'How to Fit a Trekking Backpack', 'Video platform', 'Video', 'Fitting a pack on camera', None, '2025-09-10', 'Yes', 'Yes', 'No', None, 'No'),
    (2, 4, 'hikeindia.example/trekking-backpack-guide/', 'Trekking Backpack Guide: Litres by Trek Length', 'Publisher or blog', 'Guide or how to', 'Litres by trek length', 2200, '2025-02-01', 'Yes', 'No', 'No', 25, 'Yes'),
    (2, 5, 'bigmart.example/backpacks/', 'Backpacks Online', 'Marketplace or directory', 'Category page', 'Shop backpacks', 300, '2026-11-10', 'No', 'No', 'Yes', 900, 'No'),
    (2, 6, 'travelnotes.example/backpack-tips/', '15 Backpack Tips for Trekkers', 'Publisher or blog', 'List post', '15 quick tips', 1300, '2023-07-01', 'No', 'No', 'No', 6, 'No'),
    (2, 7, 'gearlane.example/p/trail-45l/', 'Trail 45L Trekking Backpack', 'Brand or retailer', 'Product page', 'One 45 litre pack', 500, '2026-07-01', 'No', 'No', 'Yes', 20, 'No'),
    (2, 8, 'mountainmiles.example/blog/backpack-guide/', 'Backpack Guide for Women Trekkers', 'Publisher or blog', 'Guide or how to', 'Women specific fit', 2100, '2025-11-25', 'Yes', 'Yes', 'No', 30, 'No'),
    (2, 9, 'trailnest.example/blog/choose-trekking-backpack/', 'How to Choose a Trekking Backpack (Sizing Chart)', 'Brand or retailer', 'Guide or how to', 'Our sizing chart', 1800, '2025-05-01', 'Yes', 'Yes', 'No', 12, 'No'),
    (2, 10, 'trekkersforum.example/t/which-backpack', 'Which backpack for a 6 day trek?', 'Forum or community', 'Forum thread', 'Litre debates', 800, '2024-05-05', 'No', 'Yes', 'No', 3, 'No'),
    (3, 1, 'trailtested.example/trekking-pole-length/', 'Trekking Pole Height Chart and How to Adjust', 'Publisher or blog', 'Guide or how to', 'Chart plus adjusting tips', 1400, '2024-10-01', 'Yes', 'Yes', 'No', 45, 'Yes'),
    (3, 2, 'polecalc.example/', 'Trekking Pole Length Calculator', 'Specialist business', 'Tool or calculator', 'Enter height, get length', 150, '2023-05-01', 'No', 'No', 'No', 8, 'No'),
    (3, 3, 'trekkersforum.example/t/pole-height', 'Pole height for downhill?', 'Forum or community', 'Forum thread', 'Downhill vs uphill length', 600, '2024-03-03', 'No', 'Yes', 'No', 2, 'Yes'),
    (3, 4, 'gearlane.example/expert-advice/poles/', 'Trekking Poles: Expert Advice', 'Brand or retailer', 'Guide or how to', 'Retailer advice', 1600, '2025-01-20', 'Yes', 'Yes', 'No', 140, 'No'),
    (3, 5, 'bigmart.example/trekking-poles/', 'Trekking Poles Online', 'Marketplace or directory', 'Category page', 'Shop poles', 200, '2026-10-01', 'No', 'No', 'Yes', 900, 'No'),
    (3, 6, 'hikeindia.example/pole-height-chart/', 'Pole Height Chart (Printable)', 'Publisher or blog', 'Guide or how to', 'Printable chart', 900, '2023-12-12', 'No', 'No', 'No', 7, 'No'),
    (3, 7, 'sizeguides.example/trekking-poles/', 'Trekking Pole Size Chart', 'Publisher or blog', 'Tool or calculator', 'Size chart table', 500, '2024-07-07', 'No', 'No', 'No', 11, 'No'),
    (3, 8, 'videohub.example/watch?v=pole-height', 'Setting Your Pole Height', 'Video platform', 'Video', 'Setting pole height', None, '2024-09-09', 'Yes', 'Yes', 'No', None, 'No'),
    (3, 9, 'askoutdoors.example/q/pole-length', 'What length trekking pole for my height?', 'Forum or community', 'Forum thread', 'Short Q and A', 400, '2022-10-10', 'No', 'No', 'No', 1, 'No'),
    (3, 10, 'gearlane.example/p/carbon-pole/', 'Carbon Trekking Pole', 'Brand or retailer', 'Product page', 'Carbon pole', 400, '2026-06-01', 'No', 'No', 'Yes', 20, 'No'),
    (4, 1, 'gearlane.example/waterproof-jackets/', 'Waterproof Jackets for Trekking', 'Brand or retailer', 'Category page', 'Big range', 500, '2026-11-01', 'No', 'No', 'Yes', 140, 'No'),
    (4, 2, 'bigmart.example/rain-jackets/', 'Rain Jackets: Up to 60 Percent Off', 'Marketplace or directory', 'Category page', 'Discounts', 300, '2026-11-12', 'No', 'No', 'Yes', 900, 'No'),
    (4, 3, 'alpinewear.example/jackets/waterproof/', 'Waterproof Jackets', 'Brand or retailer', 'Category page', 'Premium brand range', 400, '2026-10-20', 'No', 'No', 'Yes', 260, 'No'),
    (4, 4, 'trailtested.example/best-rain-jackets/', 'Best Rain Jackets, Tested in the Monsoon', 'Publisher or blog', 'Best of list', 'Tested in heavy rain', 3900, '2026-08-15', 'Yes', 'Yes', 'Yes', 310, 'No'),
    (4, 5, 'shopzone.example/trekking-jackets/', 'Trekking Jackets', 'Marketplace or directory', 'Category page', 'Wide choice', 250, '2026-11-05', 'No', 'No', 'Yes', 700, 'No'),
    (4, 6, 'alpinewear.example/p/storm-shell/', 'Storm Shell Waterproof Jacket', 'Brand or retailer', 'Product page', 'Flagship jacket', 600, '2026-09-01', 'No', 'No', 'Yes', 260, 'No'),
    (4, 7, 'hikeindia.example/best-waterproof-jackets/', 'Best Waterproof Jackets in India', 'Publisher or blog', 'Best of list', 'Budget picks', 2100, '2025-06-01', 'Yes', 'No', 'No', 25, 'No'),
    (4, 8, 'sportsdepot.example/jackets/rain/', 'Rain Jackets for Men and Women', 'Brand or retailer', 'Category page', 'Sports chain range', 350, '2026-10-30', 'No', 'No', 'Yes', 480, 'No'),
    (4, 9, 'gearlane.example/p/monsoon-pro/', 'Monsoon Pro Jacket', 'Brand or retailer', 'Product page', 'Best seller', 500, '2026-07-15', 'No', 'No', 'Yes', 140, 'No'),
    (4, 10, 'fashionhub.example/rain-jackets-men/', 'Rain Jackets for Men', 'Marketplace or directory', 'Category page', 'Fashion range', 200, '2026-11-11', 'No', 'No', 'Yes', 350, 'No'),
]
# keyword index, engine, date, shown, 5 linked urls (paths without https://), you linked
AI = [
    (1, 'Google AI Overview', '2026-11-18', 'Yes', ['trekhimalaya.example/kedarkantha-packing-list/', 'snowtrails.example/kedarkantha-trek-guide/', 'trekguideindia.example/kedarkantha/', 'weatherhills.example/kedarkantha-winter/', 'campfirediaries.example/kedarkantha-kit/'], 'No'),
    (1, 'ChatGPT', '2026-11-18', 'Yes', ['trekguideindia.example/kedarkantha/', 'campfirediaries.example/kedarkantha-kit/', 'weatherhills.example/kedarkantha-winter/', '', ''], 'No'),
    (0, 'Google AI Overview', '2026-11-18', 'Yes', ['trailtested.example/best-trekking-shoes/', 'hikeindia.example/best-trekking-shoes-india/', 'trekkersforum.example/t/first-trekking-shoes', 'footcareclinic.example/hiking-blisters/', ''], 'No'),
    (0, 'Google AI Mode', '2026-11-18', 'Yes', ['trailtested.example/best-trekking-shoes/', 'mountainmiles.example/blog/trekking-shoes-guide/', 'footcareclinic.example/hiking-blisters/', 'shoefitlab.example/trekking-fit/', 'trekguideindia.example/gear/'], 'No'),
    (2, 'Google AI Overview', '2026-11-18', 'Yes', ['trailtested.example/how-to-choose-a-backpack/', 'gearlane.example/expert-advice/backpacks/', 'hikeindia.example/trekking-backpack-guide/', '', ''], 'No'),
    (3, 'Google AI Overview', '2026-11-19', 'Yes', ['trailtested.example/trekking-pole-length/', 'trekkersforum.example/t/pole-height', 'physiotrek.example/pole-technique/', 'mountainschool.example/poles/', ''], 'No'),
    (4, 'Google AI Overview', '2026-11-19', 'No', ['', '', '', '', ''], 'No'),
]

LOG_HEAD = ['Keyword', 'Position', 'URL', 'Title shown', 'Site type', 'Page format', 'Main angle', 'Approx. words', 'Last updated',
            'Named author?', 'First hand experience?', 'Rich attributes?', 'Referring domains', 'Linked in AI answer?', 'Notes',
            'Domain', 'Age (months)', 'Keyword in title?', 'Weak signals (0 to 5)', 'Weak spots', 'Result strength', 'Results from this domain', 'Key (helper)']
LOG_F = tuple(range(16, 24))
KW_HEAD = ['Keyword', 'Monthly volume', 'KD (0 to 100)', 'Country and device', 'Date checked', 'Your position', 'Your URL',
           'Your referring domains'] + FEATURES + [
           'Results logged', 'Dominant format', 'Format share', 'Format clarity', 'Implied intent', 'Dominant site type',
           'Beatable results', 'Link reachable share', 'Dated share', 'Forum share', 'SERP features (of 7)', 'Results linked in AI answers',
           'Opportunity score (0 to 100)', 'Verdict', 'Format to build', 'Feature plays', 'Your status', 'Notes']
KW_F = tuple(range(16, 32))


def lg(c):
    return f'{LG}!${c}${LOG_FIRST}:${c}${LOG_LAST}'


def kw(c):
    return f'{KWS}!${c}${KW_FIRST}:${c}${KW_LAST}'


def d(s):
    return datetime.date.fromisoformat(s) if s else None


def settings_sheet(wb):
    ws = wb.create_sheet(S)
    ws.sheet_view.showGridLines = False
    K.title_block(ws, 'Settings', 'Every threshold, weight and list used by this workbook. Change a blue number and every score updates.')
    for c, w in zip('ABCDEFGHI', [56, 14, 3, 24, 16, 3, 26, 10, 20]):
        ws.column_dimensions[c].width = w
    rows = [
        (4, 'RESULT CHECKS', None, None),
        (5, 'Analysis date (set it to the day you log the results)', datetime.date(2026, 11, 19), 'dd mmm yyyy'),
        (6, 'Dated when the last update is older than (months)', 12, '0'),
        (7, 'Few links when referring domains are below', 20, '0'),
        (8, 'Beatable when weak signals are at least', 3, '0'),
        (9, 'Average when weak signals are at least (below = Strong)', 2, '0'),
        (10, 'Clear format when the dominant format has at least this share', 0.5, '0%'),
        (11, 'Link reachable when a result has at most your referring domains times', 2, '0.0'),
        (12, 'Minimum results logged before a keyword gets a score', 5, '0'),
        (14, 'OPPORTUNITY SCORE WEIGHTS (any numbers, they are scaled)', None, None),
        (15, 'Beatable results share', 35, '0'),
        (16, 'Link reachable share', 25, '0'),
        (17, 'Dated results share', 15, '0'),
        (18, 'Forum and community results share', 10, '0'),
        (19, 'Room for organic results (fewer SERP features)', 15, '0'),
        (20, 'Total (auto)', '=SUM(B15:B19)', '0'),
        (22, 'VERDICT', None, None),
        (23, 'Go when the opportunity score is at least', 55, '0'),
        (24, 'Go with a strong angle when at least (below = Hard)', 35, '0'),
    ]
    for r, label, val, fmt in rows:
        a = ws.cell(row=r, column=1, value=label)
        a.font = K.f(10, val is None, K.DEEP if val is None else K.INK)
        if val is not None:
            c = ws.cell(row=r, column=2, value=val)
            c.border = K.BORDER
            is_f = isinstance(val, str) and val.startswith('=')
            c.fill = K.FORMULA_FILL if is_f else K.INPUT_FILL
            c.font = K.f(10, True, K.INK if is_f else '0000FF')
            if fmt:
                c.number_format = fmt
    ws['A26'] = ('All thresholds and weights are starter assumptions chosen for this kit, not Google rules. The weak signals are practical '
                 'hints that a page may be easier to beat; Google does not publish a list like this. Tune them to your niche.')
    ws['A26'].font = K.f(9, False, '777777', True)
    ws['A26'].alignment = Alignment(wrap_text=True)
    ws.row_dimensions[26].height = 42
    ws['D4'] = 'PAGE FORMAT AND IMPLIED INTENT'
    ws['D4'].font = K.f(10, True, K.DEEP)
    for i, (fmt, intent) in enumerate(FORMATS):
        ws.cell(row=5 + i, column=4, value=fmt).fill = K.INPUT_FILL
        ws.cell(row=5 + i, column=5, value=intent).fill = K.INPUT_FILL
    ws['G4'] = 'DROPDOWN LISTS'
    ws['G4'].font = K.f(10, True, K.DEEP)
    lists = {'G': ['Site type'] + SITE_TYPES, 'H': ['Yes/No', 'Yes', 'No'], 'I': ['AI engine'] + ENGINES}
    for c, vals in lists.items():
        for i, v in enumerate(vals):
            cell = ws[f'{c}{5 + i}']
            cell.value = v
            cell.font = K.f(9, i == 0, '555555')
    return ws


def log_sheet(wb):
    ws = wb.create_sheet('SERP Log')
    ws.sheet_view.showGridLines = False
    K.title_block(ws, 'SERP log', 'Rows 5 to 54 hold DEMO data for TrailNest, a fictional trekking gear store: 5 keywords x 10 results (illustrative sites and numbers). Select the yellow demo cells and press Delete to start your own. Grey formula columns stay.')
    ws['A2'].font = K.f(10, True, 'B45309')
    ws['A3'] = 'One row per organic result on page one. Add the keyword on the Keywords tab first. Look at each page itself, not only the snippet. 500 rows ready.'
    ws['A3'].font = K.f(9, False, '666666', True)
    K.header_row(ws, 4, LOG_HEAD, formula_cols=LOG_F,
                 widths=[30, 8, 40, 40, 20, 18, 28, 9, 12, 9, 10, 9, 10, 10, 20, 24, 9, 10, 10, 40, 11, 10, 10])
    for r in range(LOG_FIRST, LOG_LAST + 1):
        i = r - LOG_FIRST
        if i < len(R):
            k, pos, url, title, st, fmt, angle, words, upd, au, fh, rich, rd, ai = R[i]
            vals = [KEYWORDS[k][0], pos, SITE + url, title, st, fmt, angle, words, d(upd), au, fh, rich, rd, ai]
            for c, v in enumerate(vals, 1):
                if v is not None:
                    ws.cell(row=r, column=c, value=v)
        s = f'IF(ISNUMBER(FIND("//",C{r})),MID(C{r},FIND("//",C{r})+2,300),C{r})'
        ws.cell(row=r, column=16, value=f'=IF(C{r}="","",SUBSTITUTE(LOWER(LEFT({s},FIND("/",{s}&"/")-1)),"www.",""))')
        ws.cell(row=r, column=17, value=f'=IF(I{r}="","",MAX(0,ROUND(({DATE}-I{r})/30.44,0)))')
        ws.cell(row=r, column=18, value=f'=IF(OR(A{r}="",D{r}=""),"",IF(ISNUMBER(SEARCH(A{r},D{r})),"Yes","No"))')
        dated = f'N(Q{r})>{FRESH}'
        few = f'AND(M{r}<>"",N(M{r})<{LOWRD})'
        ws.cell(row=r, column=19, value=(
            f'=IF(C{r}="","",({dated})*1+(J{r}<>"Yes")*1+(K{r}<>"Yes")*1+(E{r}="Forum or community")*1+({few})*1)'))
        ws.cell(row=r, column=20, value=(
            f'=IF(C{r}="","",_xlfn.TEXTJOIN(", ",TRUE,IF({dated},"dated",""),IF(J{r}<>"Yes","no named author",""),'
            f'IF(K{r}<>"Yes","no first hand experience",""),IF(E{r}="Forum or community","forum result",""),IF({few},"few links","")))'))
        ws.cell(row=r, column=21, value=f'=IF(C{r}="","",IF(S{r}>={BEAT},"Beatable",IF(S{r}>={AVG},"Average","Strong")))')
        ws.cell(row=r, column=22, value=f'=IF(P{r}="","",COUNTIFS($A${LOG_FIRST}:$A${LOG_LAST},A{r},$P${LOG_FIRST}:$P${LOG_LAST},P{r}))')
        ws.cell(row=r, column=23, value=f'=IF(A{r}="","",A{r}&"|"&B{r})')
    K.style_body(ws, LOG_FIRST, LOG_LAST, len(LOG_HEAD), formula_cols=LOG_F,
                 number_formats={8: '#,##0', 9: 'dd mmm yyyy', 13: '#,##0', 17: '0'}, wrap_cols=(4, 7, 20))
    ws.freeze_panes = 'C5'
    ws.auto_filter.ref = f'A4:{L(len(LOG_HEAD))}{LOG_LAST}'
    K.dropdown(ws, f'A{LOG_FIRST}:A{LOG_LAST}', kw('A'), 'Pick a keyword from the Keywords tab')
    K.whole_number(ws, f'B{LOG_FIRST}:B{LOG_LAST}', 1, 20, 'Position on page one or two (1 to 20).')
    K.dropdown(ws, f'E{LOG_FIRST}:E{LOG_LAST}', f'{S}!$G$6:$G${5 + len(SITE_TYPES)}')
    K.dropdown(ws, f'F{LOG_FIRST}:F{LOG_LAST}', f'{S}!$D$5:$D${4 + len(FORMATS)}')
    K.dropdown(ws, f'J{LOG_FIRST}:L{LOG_LAST}', f'{S}!$H$6:$H$7')
    K.dropdown(ws, f'N{LOG_FIRST}:N{LOG_LAST}', f'{S}!$H$6:$H$7')
    u = f'U{LOG_FIRST}:U{LOG_LAST}'
    ws.conditional_formatting.add(u, CellIsRule(operator='equal', formula=['"Beatable"'], fill=PatternFill('solid', fgColor='9BE07A'), font=Font(name=K.FONT, bold=True)))
    ws.conditional_formatting.add(u, CellIsRule(operator='equal', formula=['"Average"'], fill=PatternFill('solid', fgColor='FFF4CC')))
    ws.conditional_formatting.add(u, CellIsRule(operator='equal', formula=['"Strong"'], fill=PatternFill('solid', fgColor='F8D7D3'), font=Font(name=K.FONT, bold=True, color='9B2C1F')))
    ws.conditional_formatting.add(f'S{LOG_FIRST}:S{LOG_LAST}', ColorScaleRule(start_type='num', start_value=0, start_color='F8D7D3', mid_type='num', mid_value=2, mid_color='FFF4CC', end_type='num', end_value=5, end_color='B7E4A0'))
    ws.conditional_formatting.add(f'V{LOG_FIRST}:V{LOG_LAST}', CellIsRule(operator='greaterThan', formula=['1'], font=Font(name=K.FONT, bold=True, color='B45309')))
    ws.conditional_formatting.add(f'C{LOG_FIRST}:C{LOG_LAST}', FormulaRule(formula=[f'ISNUMBER(SEARCH("trailnest",C{LOG_FIRST}))'], font=Font(name=K.FONT, bold=True, color=K.DEEP)))
    return ws


def mix_sheet(wb):
    ws = wb.create_sheet('Format Mix')
    ws.sheet_view.showGridLines = False
    K.title_block(ws, 'Format mix', 'How many logged results of each page format and site type appear for each keyword. Everything here is automatic.')
    nf, ns = len(FORMATS), len(SITE_TYPES)
    head = ['Keyword'] + [f for f, _ in FORMATS] + ['Results', 'Top count', 'Dominant format'] + SITE_TYPES + ['Top site count', 'Dominant site type']
    K.header_row(ws, 4, head, formula_cols=tuple(range(1, len(head) + 1)), widths=[32] + [10] * nf + [8, 8, 20] + [11] * ns + [8, 22])
    fc0, fc1 = 2, 1 + nf                    # format count columns
    res, top, dom = 2 + nf, 3 + nf, 4 + nf
    sc0, sc1 = 5 + nf, 4 + nf + ns
    stop, sdom = 5 + nf + ns, 6 + nf + ns
    for r in range(KW_FIRST, KW_LAST + 1):
        ws.cell(row=r, column=1, value=f'=IF({KWS}!A{r}="","",{KWS}!A{r})')
        for c in range(fc0, fc1 + 1):
            ws.cell(row=r, column=c, value=f'=IF($A{r}="","",COUNTIFS({lg("A")},$A{r},{lg("F")},{L(c)}$4))')
        ws.cell(row=r, column=res, value=f'=IF($A{r}="","",COUNTIF({lg("A")},$A{r}))')
        fr = f'{L(fc0)}{r}:{L(fc1)}{r}'
        ws.cell(row=r, column=top, value=f'=IF($A{r}="","",MAX({fr}))')
        ws.cell(row=r, column=dom, value=f'=IF(OR($A{r}="",N({L(top)}{r})=0),"",INDEX(${L(fc0)}$4:${L(fc1)}$4,MATCH({L(top)}{r},{fr},0)))')
        for c in range(sc0, sc1 + 1):
            ws.cell(row=r, column=c, value=f'=IF($A{r}="","",COUNTIFS({lg("A")},$A{r},{lg("E")},{L(c)}$4))')
        sr = f'{L(sc0)}{r}:{L(sc1)}{r}'
        ws.cell(row=r, column=stop, value=f'=IF($A{r}="","",MAX({sr}))')
        ws.cell(row=r, column=sdom, value=f'=IF(OR($A{r}="",N({L(stop)}{r})=0),"",INDEX(${L(sc0)}$4:${L(sc1)}$4,MATCH({L(stop)}{r},{sr},0)))')
    K.style_body(ws, KW_FIRST, KW_LAST, len(head), formula_cols=tuple(range(1, len(head) + 1)))
    ws.conditional_formatting.add(f'{L(fc0)}{KW_FIRST}:{L(fc1)}{KW_LAST}', ColorScaleRule(start_type='num', start_value=0, start_color='FFFFFF', end_type='num', end_value=8, end_color='6CC82A'))
    ws.conditional_formatting.add(f'{L(sc0)}{KW_FIRST}:{L(sc1)}{KW_LAST}', ColorScaleRule(start_type='num', start_value=0, start_color='FFFFFF', end_type='num', end_value=8, end_color='8DB4E2'))
    ws.freeze_panes = 'B5'
    return {'dom': L(dom), 'top': L(top), 'sdom': L(sdom)}


def keywords_sheet(wb, mix):
    ws = wb.create_sheet(KWS)
    ws.sheet_view.showGridLines = False
    K.title_block(ws, 'Keywords and verdicts', 'One row per keyword you analyse. Type the yellow cells and mark the SERP features you saw. Grey columns summarise the SERP Log and give a verdict.')
    widths = [32, 10, 9, 14, 12, 9, 28, 10] + [10] * 7 + [9, 20, 9, 10, 13, 20, 10, 11, 9, 9, 9, 10, 11, 22, 26, 60, 14, 24]
    K.header_row(ws, 4, KW_HEAD, formula_cols=KW_F, widths=widths)
    play = [('I', 'Answer the main question early and add first hand detail the AI answer cannot'),
            ('J', 'Put a short, direct answer right under a question heading'),
            ('K', 'Answer the People also ask questions in clear sections'),
            ('L', 'Add a short original video'),
            ('M', 'Use original photos with descriptive alt text'),
            ('N', 'Strengthen your Business Profile for local results'),
            ('O', 'Add product details, prices and Product structured data')]
    for r in range(KW_FIRST, KW_LAST + 1):
        i = r - KW_FIRST
        if i < len(KEYWORDS):
            k = KEYWORDS[i]
            vals = [k[0], k[1], k[2], k[3], d(k[4]), k[5], k[6], k[7]] + k[8]
            for c, v in enumerate(vals, 1):
                if v not in (None, ''):
                    ws.cell(row=r, column=c, value=v)
        a = f'$A{r}'
        ws.cell(row=r, column=16, value=f'=IF(A{r}="","",COUNTIF({lg("A")},{a}))')
        ws.cell(row=r, column=17, value=f'=IF(A{r}="","",{FM}!{mix["dom"]}{r})')
        ws.cell(row=r, column=18, value=f'=IF(OR(A{r}="",N(P{r})=0),"",{FM}!{mix["top"]}{r}/P{r})')
        ws.cell(row=r, column=19, value=f'=IF(R{r}="","",IF(R{r}>={CLEAR},"Clear","Mixed"))')
        ws.cell(row=r, column=20, value=f'=IF(Q{r}="","",IFERROR(VLOOKUP(Q{r},{S}!$D$5:$E${4 + len(FORMATS)},2,FALSE),""))')
        ws.cell(row=r, column=21, value=f'=IF(A{r}="","",{FM}!{mix["sdom"]}{r})')
        ws.cell(row=r, column=22, value=f'=IF(A{r}="","",COUNTIFS({lg("A")},{a},{lg("U")},"Beatable"))')
        ws.cell(row=r, column=23, value=(
            f'=IF(OR(A{r}="",N(P{r})=0),"",IFERROR(COUNTIFS({lg("A")},{a},{lg("M")},"<="&N(H{r})*{MULT})/COUNTIFS({lg("A")},{a},{lg("M")},"<>"),0))'))
        ws.cell(row=r, column=24, value=f'=IF(OR(A{r}="",N(P{r})=0),"",COUNTIFS({lg("A")},{a},{lg("Q")},">"&{FRESH})/P{r})')
        ws.cell(row=r, column=25, value=f'=IF(OR(A{r}="",N(P{r})=0),"",COUNTIFS({lg("A")},{a},{lg("E")},"Forum or community")/P{r})')
        ws.cell(row=r, column=26, value=f'=IF(A{r}="","",COUNTIF(I{r}:O{r},"Yes"))')
        ws.cell(row=r, column=27, value=f'=IF(A{r}="","",COUNTIFS({lg("A")},{a},{lg("N")},"Yes"))')
        ws.cell(row=r, column=28, value=(
            f'=IF(OR(A{r}="",N(P{r})<{MINRES}),"",ROUND(100*({W1}*V{r}/P{r}+{W2}*W{r}+{W3}*X{r}+{W4}*Y{r}+{W5}*(1-Z{r}/7))/{WT},0))'))
        ws.cell(row=r, column=29, value=(
            f'=IF(A{r}="","",IF(N(P{r})<{MINRES},"Log at least "&{MINRES}&" results",IF(AB{r}>={GO},"Go",'
            f'IF(AB{r}>={ANGLE},"Go with a strong angle","Hard: pick a narrower keyword"))))'))
        ws.cell(row=r, column=30, value=f'=IF(OR(A{r}="",Q{r}=""),"",IF(S{r}="Clear",Q{r},"Mixed: lead with "&Q{r}&", test others"))')
        parts = ','.join(f'IF({c}{r}="Yes","{t}","")' for c, t in play)
        ws.cell(row=r, column=31, value=f'=IF(A{r}="","",_xlfn.TEXTJOIN(". ",TRUE,{parts}))')
        ws.cell(row=r, column=32, value=f'=IF(A{r}="","",IF(N(F{r})=0,"Not ranking",IF(F{r}<=3,"Top 3",IF(F{r}<=10,"Page one","Beyond page one"))))')
    K.style_body(ws, KW_FIRST, KW_LAST, len(KW_HEAD), formula_cols=KW_F,
                 number_formats={2: '#,##0', 5: 'dd mmm yyyy', 8: '#,##0', 18: '0%', 23: '0%', 24: '0%', 25: '0%', 28: '0'}, wrap_cols=(30, 31, 33))
    ws.freeze_panes = 'B5'
    ws.auto_filter.ref = f'A4:{L(len(KW_HEAD))}{KW_LAST}'
    K.dropdown(ws, f'I{KW_FIRST}:O{KW_LAST}', f'{S}!$H$6:$H$7')
    K.whole_number(ws, f'C{KW_FIRST}:C{KW_LAST}', 0, 100, 'Keyword difficulty must be between 0 and 100.')
    v = f'AC{KW_FIRST}:AC{KW_LAST}'
    ws.conditional_formatting.add(v, CellIsRule(operator='equal', formula=['"Go"'], fill=PatternFill('solid', fgColor='9BE07A'), font=Font(name=K.FONT, bold=True)))
    ws.conditional_formatting.add(v, CellIsRule(operator='equal', formula=['"Go with a strong angle"'], fill=PatternFill('solid', fgColor='FFF4CC')))
    ws.conditional_formatting.add(v, FormulaRule(formula=[f'LEFT(AC{KW_FIRST},4)="Hard"'], fill=PatternFill('solid', fgColor='F8D7D3'), font=Font(name=K.FONT, bold=True, color='9B2C1F')))
    ws.conditional_formatting.add(f'AB{KW_FIRST}:AB{KW_LAST}', ColorScaleRule(start_type='num', start_value=0, start_color='F8D7D3', mid_type='num', mid_value=50, mid_color='FFF4CC', end_type='num', end_value=100, end_color='B7E4A0'))
    ws.conditional_formatting.add(f'I{KW_FIRST}:O{KW_LAST}', CellIsRule(operator='equal', formula=['"Yes"'], fill=PatternFill('solid', fgColor='DCEBFF')))
    return ws


def ai_sheet(wb):
    ws = wb.create_sheet('AI Answer Check')
    ws.sheet_view.showGridLines = False
    K.title_block(ws, 'AI answer check', 'For each keyword, record the pages an AI answer links to. Paste each URL exactly as in the SERP Log. The sheet shows how many come from your organic top 10.')
    head = ['Keyword', 'AI engine', 'Date checked', 'AI answer shown?', 'Linked URL 1', 'Linked URL 2', 'Linked URL 3', 'Linked URL 4', 'Linked URL 5',
            'You linked?', 'Notes', 'Links logged', 'Also in your SERP Log', 'Overlap share', 'From outside the log', 'What it tells you']
    fc = (12, 13, 14, 15, 16)
    K.header_row(ws, 4, head, formula_cols=fc, widths=[32, 18, 12, 10, 30, 30, 30, 30, 30, 9, 20, 9, 11, 9, 11, 56])
    for r in range(AI_FIRST, AI_LAST + 1):
        i = r - AI_FIRST
        if i < len(AI):
            k, eng, dt, shown, urls, you = AI[i]
            vals = [KEYWORDS[k][0], eng, d(dt), shown] + [SITE + u if u else None for u in urls] + [you]
            for c, v in enumerate(vals, 1):
                if v is not None:
                    ws.cell(row=r, column=c, value=v)
        ws.cell(row=r, column=12, value=f'=IF(A{r}="","",COUNTA(E{r}:I{r}))')
        inlog = '+'.join(f'IF({c}{r}="",0,MIN(1,COUNTIFS({lg("A")},$A{r},{lg("C")},{c}{r})))' for c in 'EFGHI')
        ws.cell(row=r, column=13, value=f'=IF(A{r}="","",{inlog})')
        ws.cell(row=r, column=14, value=f'=IF(OR(A{r}="",N(L{r})=0),"",M{r}/L{r})')
        ws.cell(row=r, column=15, value=f'=IF(A{r}="","",L{r}-M{r})')
        ws.cell(row=r, column=16, value=(
            f'=IF(A{r}="","",IF(D{r}<>"Yes","No AI answer: compete in the classic results",IF(L{r}=0,"Add the linked URLs",'
            f'IF(N{r}>=0.6,"Mostly links the top results: win the organic page first",'
            f'IF(N{r}>=0.3,"Mixed: some links come from outside the top results","Links pages outside the top results: a separate opportunity")))))'))
    K.style_body(ws, AI_FIRST, AI_LAST, len(head), formula_cols=fc, number_formats={3: 'dd mmm yyyy', 14: '0%'}, wrap_cols=(16,))
    K.dropdown(ws, f'A{AI_FIRST}:A{AI_LAST}', kw('A'))
    K.dropdown(ws, f'B{AI_FIRST}:B{AI_LAST}', f'{S}!$I$6:$I${5 + len(ENGINES)}')
    K.dropdown(ws, f'D{AI_FIRST}:D{AI_LAST}', f'{S}!$H$6:$H$7')
    K.dropdown(ws, f'J{AI_FIRST}:J{AI_LAST}', f'{S}!$H$6:$H$7')
    p = f'P{AI_FIRST}:P{AI_LAST}'
    ws.conditional_formatting.add(p, FormulaRule(formula=[f'LEFT(P{AI_FIRST},5)="Links"'], fill=PatternFill('solid', fgColor='9BE07A'), font=Font(name=K.FONT, bold=True)))
    ws.conditional_formatting.add(p, FormulaRule(formula=[f'LEFT(P{AI_FIRST},5)="Mixed"'], fill=PatternFill('solid', fgColor='FFF4CC')))
    ws.conditional_formatting.add(p, FormulaRule(formula=[f'LEFT(P{AI_FIRST},6)="Mostly"'], fill=PatternFill('solid', fgColor='DCEBFF')))
    ws.freeze_panes = 'B5'
    return ws


def plan_sheet(wb):
    ws = wb.create_sheet('Page Plan')
    ws.sheet_view.showGridLines = False
    for c, w in zip('ABCDEFGHIJ', [34, 40, 22, 18, 26, 9, 12, 11, 40, 10]):
        ws.column_dimensions[c].width = w
    K.title_block(ws, 'Page plan', 'Choose a keyword in the yellow cell. The summary and the page one table fill in by themselves. Then write your brief in the yellow boxes below.')
    ws['A4'] = 'Keyword'
    ws['A4'].font = K.f(11, True)
    ws['B4'] = KEYWORDS[1][0]
    ws['B4'].fill = K.INPUT_FILL
    ws['B4'].font = K.f(11, True)
    ws['B4'].border = K.BORDER
    K.dropdown(ws, 'B4', kw('A'), 'Pick a keyword from the Keywords tab')
    m = f'MATCH($B$4,{kw("A")},0)'
    items = [('Monthly volume', 'B', '#,##0'), ('KD (0 to 100)', 'C', '0'), ('Your status', 'AF', None), ('Results logged', 'P', '0'),
             ('Dominant format', 'Q', None), ('Format clarity', 'S', None), ('Implied intent', 'T', None), ('Dominant site type', 'U', None),
             ('Beatable results', 'V', '0'), ('Link reachable share', 'W', '0%'), ('Dated share', 'X', '0%'), ('SERP features (of 7)', 'Z', '0'),
             ('Opportunity score', 'AB', '0'), ('Verdict', 'AC', None), ('Format to build', 'AD', None), ('Feature plays', 'AE', None)]
    ws['A6'] = 'SERP SUMMARY'
    ws['A6'].font = K.f(10, True, K.DEEP)
    for i, (label, col, fmt) in enumerate(items):
        r = 7 + i
        ws.cell(row=r, column=1, value=label).font = K.f(10)
        c = ws.cell(row=r, column=2, value=f'=IFERROR(INDEX({kw(col)},{m}),"")')
        c.fill = K.FORMULA_FILL
        c.border = K.BORDER
        c.font = K.f(10, label in ('Verdict', 'Opportunity score'))
        c.alignment = Alignment(wrap_text=True, vertical='top')
        if fmt:
            c.number_format = fmt
    r = 7 + len(items)
    ws.cell(row=r, column=1, value='Typical length of logged results (context only)').font = K.f(10)
    c = ws.cell(row=r, column=2, value=f'=IFERROR(ROUND(AVERAGEIFS({lg("H")},{lg("A")},$B$4),-2),"")')
    c.fill, c.border, c.number_format = K.FORMULA_FILL, K.BORDER, '#,##0'
    ws.row_dimensions[7 + len(items) - 1].height = 60
    top = r + 2
    ws.cell(row=top - 1, column=1, value='PAGE ONE AT A GLANCE (from the SERP Log)').font = K.f(10, True, K.DEEP)
    K.header_row(ws, top, ['Position', 'URL', 'Domain', 'Page format', 'Main angle', 'Words', 'Updated', 'Strength', 'Weak spots', 'In AI answer?'],
                 formula_cols=tuple(range(1, 11)))
    cols = {2: 'C', 3: 'P', 4: 'F', 5: 'G', 6: 'H', 7: 'I', 8: 'U', 9: 'T', 10: 'N'}
    for p in range(1, 11):
        rr = top + p
        ws.cell(row=rr, column=1, value=p)
        mm = f'MATCH($B$4&"|"&$A{rr},{lg("W")},0)'
        for c, col in cols.items():
            ws.cell(row=rr, column=c, value=f'=IFERROR(INDEX({lg(col)},{mm})&"","")' if col not in ('H', 'I') else f'=IFERROR(IF(INDEX({lg(col)},{mm})="","",INDEX({lg(col)},{mm})),"")')
        for c in range(1, 11):
            cell = ws.cell(row=rr, column=c)
            cell.fill = K.FORMULA_FILL
            cell.border = K.BORDER
            cell.font = K.f(9)
            cell.alignment = Alignment(wrap_text=c in (2, 5, 9), vertical='top')
        ws.cell(row=rr, column=6).number_format = '#,##0'
        ws.cell(row=rr, column=7).number_format = 'mmm yyyy'
    h = f'H{top + 1}:H{top + 10}'
    ws.conditional_formatting.add(h, CellIsRule(operator='equal', formula=['"Beatable"'], fill=PatternFill('solid', fgColor='9BE07A'), font=Font(name=K.FONT, bold=True)))
    ws.conditional_formatting.add(h, CellIsRule(operator='equal', formula=['"Strong"'], fill=PatternFill('solid', fgColor='F8D7D3')))
    b0 = top + 13
    ws.cell(row=b0 - 1, column=1, value='YOUR BRIEF (type here)').font = K.f(10, True, K.DEEP)
    brief = [
        ('Our angle in one sentence', 'A day by day packing list from our own trek leaders, with weights and what to rent instead of buy.'),
        ('Original value only we can add', 'Photos of a real packed bag, total pack weight, what our customers forgot most often.'),
        ('Questions the page must answer', 'How cold does it get in December? Which shoes? Can I rent gear in Sankri? How heavy should my bag be?'),
        ('Format we will build', 'Checklist or template, with a printable version'),
        ('Target URL', '/guides/kedarkantha-packing-list/'),
        ('Pages that will link to it', '/trekking-backpacks/, /blog/winter-trek-layering/'),
        ('Owner and due date', 'Asha, 10 December 2026'),
    ]
    for i, (k, v) in enumerate(brief):
        rr = b0 + i
        ws.cell(row=rr, column=1, value=k).font = K.f(10, True)
        c = ws.cell(row=rr, column=2, value=v)
        c.fill = K.INPUT_FILL
        c.border = K.BORDER
        c.alignment = Alignment(wrap_text=True, vertical='top')
        ws.merge_cells(start_row=rr, start_column=2, end_row=rr, end_column=6)
        ws.row_dimensions[rr].height = 32
    return ws


def dashboard_sheet(wb):
    ws = wb.create_sheet('Dashboard')
    ws.sheet_view.showGridLines = False
    K.title_block(ws, 'Dashboard', 'Everything here calculates from the other tabs. Nothing to type.')
    for c, w in zip('ABCDEFGH', [44, 12, 3, 34, 9, 26, 3, 3]):
        ws.column_dimensions[c].width = w
    kpis = [
        ('Keywords analysed', f'=COUNTA({kw("A")})', '0'),
        ('Results logged', f'=COUNTA({lg("C")})', '0'),
        ('Verdict: Go', f'=COUNTIF({kw("AC")},"Go")', '0'),
        ('Verdict: Go with a strong angle', f'=COUNTIF({kw("AC")},"Go with a strong angle")', '0'),
        ('Verdict: Hard', f'=COUNTIF({kw("AC")},"Hard*")', '0'),
        ('Average opportunity score', f'=IFERROR(ROUND(AVERAGE({kw("AB")}),0),0)', '0'),
        ('Share of results rated Beatable', f'=IFERROR(COUNTIF({lg("U")},"Beatable")/COUNTA({lg("C")}),0)', '0%'),
        ('Keywords with an AI Overview', f'=COUNTIF({kw("I")},"Yes")', '0'),
        ('AI answer links from outside your log', f"=SUM('AI Answer Check'!$O${AI_FIRST}:$O${AI_LAST})", '0'),
        ('Keywords with a clear format', f'=COUNTIF({kw("S")},"Clear")', '0'),
    ]
    ws['A4'] = 'KEY NUMBERS'
    ws['A4'].font = K.f(10, True, K.DEEP)
    for i, (label, fml, fmt) in enumerate(kpis):
        r = 5 + i
        ws.cell(row=r, column=1, value=label).font = K.f(10)
        c = ws.cell(row=r, column=2, value=fml)
        c.number_format = fmt
        c.font = K.f(11, True)
        c.fill = K.FORMULA_FILL
        c.border = K.BORDER
    for j, h in enumerate(['Keyword', 'Score', 'Verdict']):
        c = ws.cell(row=4, column=4 + j, value=h)
        c.font = K.f(10, True, 'FFFFFF')
        c.fill = K.HEAD_F
    for i in range(15):
        r = 5 + i
        kr = KW_FIRST + i
        ws.cell(row=r, column=4, value=f'=IF({KWS}!A{kr}="","",{KWS}!A{kr})')
        ws.cell(row=r, column=5, value=f'=IF({KWS}!A{kr}="","",{KWS}!AB{kr})')
        ws.cell(row=r, column=6, value=f'=IF({KWS}!A{kr}="","",{KWS}!AC{kr})')
        for cc in (4, 5, 6):
            ws.cell(row=r, column=cc).border = K.BORDER
            ws.cell(row=r, column=cc).font = K.f(10, cc == 4)
            ws.cell(row=r, column=cc).fill = K.FORMULA_FILL
    v = 'F5:F19'
    ws.conditional_formatting.add(v, CellIsRule(operator='equal', formula=['"Go"'], fill=PatternFill('solid', fgColor='9BE07A'), font=Font(name=K.FONT, bold=True)))
    ws.conditional_formatting.add(v, CellIsRule(operator='equal', formula=['"Go with a strong angle"'], fill=PatternFill('solid', fgColor='FFF4CC')))
    ws.conditional_formatting.add(v, FormulaRule(formula=['LEFT(F5,4)="Hard"'], fill=PatternFill('solid', fgColor='F8D7D3')))
    top = 22
    for j, h in enumerate(['Page format', 'Results']):
        c = ws.cell(row=top, column=1 + j, value=h)
        c.font = K.f(10, True, 'FFFFFF')
        c.fill = K.HEAD_F
    for i, (fmt, _) in enumerate(FORMATS):
        r = top + 1 + i
        ws.cell(row=r, column=1, value=fmt).border = K.BORDER
        c = ws.cell(row=r, column=2, value=f'=COUNTIF({lg("F")},A{r})')
        c.border = K.BORDER
        c.fill = K.FORMULA_FILL

    def bar(title, ytitle, cat_col, val_col, r1, r2, anchor, color, horiz):
        ch = BarChart()
        ch.type = 'bar' if horiz else 'col'
        ch.title = title
        ch.y_axis.title = ytitle
        ch.add_data(Reference(ws, min_col=val_col, min_row=r1, max_row=r2), titles_from_data=False)
        ch.set_categories(Reference(ws, min_col=cat_col, min_row=r1, max_row=r2))
        ch.legend = None
        ch.height, ch.width = 7.5, 16
        ch.roundedCorners = False
        ch.x_axis.delete = False
        ch.y_axis.delete = False
        ch.title.overlay = False
        ch.y_axis.title.overlay = False
        ch.series[0].graphicalProperties.solidFill = color
        ws.add_chart(ch, anchor)
        return ch
    c1 = bar('Opportunity score by keyword', 'Score', 4, 5, 5, 5 + len(KEYWORDS) - 1, 'H4', K.GREEN, True)
    c1.y_axis.scaling.min = 0
    c1.y_axis.scaling.max = 100
    bar('Page formats across all logged results', 'Results', 1, 2, top + 1, top + len(FORMATS), 'H21', '2B2B2B', False)
    return ws


def build(path, asset, url):
    wb = K.new_book()
    log_sheet(wb)
    mix = mix_sheet(wb)
    keywords_sheet(wb, mix)
    dashboard_sheet(wb)
    ai_sheet(wb)
    plan_sheet(wb)
    settings_sheet(wb)
    K.prompts_sheet(wb, asset['prompts'], url)
    K.checklist_sheet(wb, list(asset['checklist']))
    K.sources_sheet(wb, asset['sources'], [
        ('Demo data', 'TrailNest and every site in the demo are fictional (.example domains). All volumes, difficulty scores, positions, referring domains, dates and AI answers are illustrative, not real data.', ''),
        ('Weak signals', 'Dated page, no named author, no first hand experience, forum result and few referring domains are practical hints chosen for this kit that a result may be easier to beat. They are not a Google list. Google says it looks at meaning, relevance, quality, usability and context.', ''),
        ('Opportunity score', 'Weighted mix of the share of Beatable results, the share of results whose referring domains are within reach of yours, the share of dated results, the share of forum results and the room left by SERP features. Weights and bands live on Settings and are assumptions to tune.', ''),
        ('SERP features', 'Feature names follow the Visual Elements gallery of Google Search where possible (for example the related questions group, also called People also ask).', ''),
        ('Typical length', 'Shown for context only. Google says there is no ideal page length.', ''),
        ('AI answers', 'AI answers vary by user, location, wording and date. Record what you saw, date it and recheck monthly.', ''),
    ])
    K.start_here(
        wb, 'SERP Analysis Kit',
        [
            'This workbook breaks down page one for any keyword: what formats and sites rank, how fresh and how strong each result is, which SERP features and AI answers crowd the page, and whether the keyword is worth going after. Every keyword gets an Opportunity score, a verdict and the format to build.',
            'It ships with demo data for a fictional trekking gear store (5 keywords, 50 results, 7 AI answer checks) so you can see every formula working. Clear the yellow demo cells when you are ready.',
        ],
        [
            ('SERP Log', 'One row per result with 500 ready rows: position, URL, site type, format, angle, update date, author, first hand experience and links, plus automatic domain, age, weak signals, weak spots and strength.'),
            ('Keywords', 'One row per keyword with SERP features, plus automatic dominant format and site type, implied intent, opportunity score, verdict, format to build and feature plays.'),
            ('Format Mix', 'Counts of page formats and site types per keyword, the source of the dominant format.'),
            ('Dashboard', 'Key numbers, scores and verdicts for every keyword, a format count and two charts.'),
            ('AI Answer Check', 'The pages AI answers link to, compared with your logged organic results.'),
            ('Page Plan', 'Pick a keyword to see its SERP summary and page one at a glance, then write your brief.'),
            ('Settings', 'Analysis date, thresholds, score weights, verdict bands, format to intent table and dropdown lists.'),
            ('AI Prompts', 'Prompts for ChatGPT, Claude or Gemini to read a SERP, find angles, brief pages and compare AI answers.'),
            ('Checklist', 'The full process as a tick list with automatic progress.'),
            ('Sources', 'Where facts come from and which numbers are assumptions.'),
        ],
        [
            'Look at the demo on every tab, the Dashboard and the Page Plan to see how it works, then clear the yellow demo cells.',
            'On Settings, set the analysis date to the day you check the results.',
            'Add each keyword on the Keywords tab with volume, difficulty, your position and the SERP features you see.',
            'Search the keyword in a clean browser for your target country and device. Log each page one result on the SERP Log, opening each page.',
            'Check the AI Overview, AI Mode or an AI assistant for the keyword and paste the linked URLs on AI Answer Check.',
            'Read the verdict, dominant format and feature plays on Keywords, then open Page Plan and write your brief.',
            'Recheck important keywords every quarter, because page one changes.',
        ],
        url,
    )
    order = ['Start Here', 'SERP Log', 'Keywords', 'Dashboard', 'Format Mix', 'AI Answer Check', 'Page Plan', 'Settings', 'AI Prompts', 'Checklist', 'Sources']
    wb._sheets = [wb[n] for n in order]
    wb.active = 0
    for ws in wb.worksheets:
        ws.sheet_properties.tabColor = K.GREEN if ws.title in ('Start Here', 'SERP Log', 'Keywords', 'Dashboard', 'Page Plan') else 'A6EF39'
    wb.save(path)


PREVIEW = {'sheet': 'SERP Log', 'header_row': 4, 'rows': 10, 'cols': [1, 2, 16, 5, 6, 10, 11, 13, 17, 19, 20, 21],
           'formula_idx': [2, 8, 9, 10, 11]}


def check(wb):
    """Assert the worked examples used in the guide."""
    k = wb[KWS]
    # Worked example: kedarkantha trek packing list (row 6)
    assert k['P6'].value == 10, k['P6'].value
    assert k['Q6'].value == 'Checklist or template' and abs(k['R6'].value - 0.5) < 1e-9 and k['S6'].value == 'Clear', (k['Q6'].value, k['R6'].value)
    assert k['T6'].value == 'Informational', k['T6'].value
    assert k['V6'].value == 7, k['V6'].value
    assert abs(k['W6'].value - 7 / 9) < 1e-9, k['W6'].value
    assert abs(k['X6'].value - 0.7) < 1e-9, k['X6'].value
    assert abs(k['Y6'].value - 0.2) < 1e-9, k['Y6'].value
    assert k['Z6'].value == 4, k['Z6'].value
    assert k['AB6'].value == 63 and k['AC6'].value == 'Go', (k['AB6'].value, k['AC6'].value)
    # The other verdicts
    assert k['AC9'].value.startswith('Hard'), (k['AB9'].value, k['AC9'].value)
    assert k['AC5'].value == 'Go with a strong angle' and k['AB5'].value == 39, (k['AB5'].value, k['AC5'].value)
    assert k['AC7'].value.startswith('Hard') and k['AF7'].value == 'Page one', (k['AB7'].value, k['AF7'].value)
    assert k['AB8'].value == 55 and k['AC8'].value == 'Go', k['AB8'].value
    assert k['S8'].value == 'Mixed' and k['AD8'].value.startswith('Mixed: lead with'), (k['S8'].value, k['AD8'].value)
    g = wb['SERP Log']
    assert g['P15'].value == 'trekhimalaya.example', g['P15'].value
    assert g['S15'].value == 0 and g['U15'].value == 'Strong', (g['S15'].value, g['U15'].value)
    assert g['S16'].value == 4 and g['U16'].value == 'Beatable', (g['S16'].value, g['U16'].value)
    assert g['T16'].value == 'dated, no named author, no first hand experience, few links', g['T16'].value
    a = wb['AI Answer Check']
    assert a['L5'].value == 5 and a['M5'].value == 2 and a['O5'].value == 3, (a['L5'].value, a['M5'].value)
    assert a['P5'].value.startswith('Mixed'), a['P5'].value
    assert a['M6'].value == 0 and a['P6'].value.startswith('Links pages outside'), a['P6'].value
    assert a['P11'].value.startswith('No AI answer'), a['P11'].value
    p = wb['Page Plan']
    assert p['B20'].value == 'Go', p['B20'].value
