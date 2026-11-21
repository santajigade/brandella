"""Title Tag Optimization Kit workbook (asset 08).

Title Lab: one row per page (500 rows). You paste the current title tag, the H1, the title Google really
shows and the Search Console numbers. The sheet measures length, duplicates, keyword position, keyword
repeats, the site name, years and CTR against your own site average for the same position band, runs 13
weighted checks (1 = pass, 0.5 = partly, 0 = fix, blank = not checked), gives a score, a grade, the fixes in
priority order, a priority and an estimate of missed clicks. It also checks a proposed new title.
Title Builder turns a keyword and an angle into titles from 10 patterns. Test Log judges title changes
fairly (before and after CTR, waiting time, position movement). Dashboard sums it all up.
"""
import datetime
from openpyxl.styles import PatternFill, Font, Alignment
from openpyxl.formatting.rule import CellIsRule, ColorScaleRule, FormulaRule
from openpyxl.chart import BarChart, Reference
from openpyxl.utils import get_column_letter as L
import kitlib as K

TL_FIRST, TL_LAST = 5, 504     # Title Lab
TB_FIRST, TB_LAST = 5, 104     # Title Builder
TS_FIRST, TS_LAST = 5, 204     # Test Log
S = 'Settings'
TL = "'Title Lab'"

(DATE, SITE, SEP, TMIN, TMAX, TLONG, NEAR, HALF) = (f'{S}!$B${r}' for r in range(5, 13))
(MINIMP, CTRG, CTRL, BIGIMP, WAIT, WIN, POSMOVE) = (f'{S}!$B${r}' for r in range(15, 22))
(GA, GB, GC, REWRITE, SD1, SD2) = (f'{S}!$B${r}' for r in range(24, 30))
CHK_ROW = 33
YEARS = f'{S}!$K$5:$K$25'
VAGUE = f'{S}!$I$5:$I$19'

# page type, use in the CTR averages? (home and about pages mostly get branded searches with a much higher CTR)
PAGE_TYPES = [('Home', 'No'), ('Category', 'Yes'), ('Product', 'Yes'), ('Article or guide', 'Yes'), ('Service', 'Yes'),
              ('Local landing', 'Yes'), ('Tool', 'Yes'), ('About or contact', 'No')]
VAGUE_LIST = ['home', 'homepage', 'welcome', 'untitled', 'untitled document', 'new page', 'index', 'products', 'product',
              'shop', 'blog', 'services', 'about', 'about us', 'contact']
BANDS = [(1, '1 to 3'), (4, '4 to 10'), (11, '11 to 20'), (21, '21 and beyond')]
TSTAT = ['Planned', 'Live', 'Reverted']

# name, weight, rule, how to fix (in weight order: this is the order of the fix list)
CHECKS = [
    ('Title present, not half empty', 10, 'A title exists and has at least 15 characters (editable) once the site name and separators are removed.',
     'Write a real title for this page. Google says a half empty title such as "| Site Name" makes it look for other text on the page.'),
    ('Keyword in title', 8, 'The focus keyword appears in the title tag.', 'Use the focus keyword, or its most natural phrasing, in the title.'),
    ('Unique title', 8, 'No other page in the Title Lab uses the same title.', 'Give every page its own title that says what that page alone offers.'),
    ('Title length', 6, '30 to 60 characters = pass. Under 30 or 61 to 70 = partly. Over 70 = fix. Bands are editable assumptions.',
     'Keep the main point in the first 60 characters. Very long titles are cut off and rewritten more often.'),
    ('No keyword stuffing', 6, 'The keyword appears once and the title has fewer than 3 commas. Twice = partly. 3 times or a comma list = fix.',
     'Say it once, naturally. Google warns that repeated keywords and keyword lists can look like spam.'),
    ('Specific, not vague', 6, 'The title without the site name is not a vague word (Home, Products, Blog) and has at least 3 words. 1 or 2 words = partly.',
     'Describe the page: what it is, for whom, and what makes it useful. Avoid titles like "Home" or "Profile".'),
    ('CTR vs your site average', 6, 'CTR is at least 80 percent of your own average CTR for pages in the same position band = pass. 50 to 79 percent = partly. Below = fix. Needs 100 impressions.',
     'Rewrite the title around what searchers want: a clearer promise, a number, a fresh angle. Then log it as a test.'),
    ('Keyword near the start', 5, 'The keyword begins within the first 25 characters (editable). Later = partly. Not checked when the keyword is missing.',
     'Move the topic to the front and put the angle and the site name after it.'),
    ('Year is current', 5, 'If the title shows a year, it is the analysis year or later. Not checked when there is no year.',
     'Update the year only when you really updated the content. Google lists an obsolete year as a common title problem.'),
    ('Matches the H1', 5, 'The H1 contains the focus keyword = pass. An H1 without it = partly. No H1 = fix.',
     'Make the H1 and the title describe the same topic. Google uses headings too when it builds title links.'),
    ('Shown as written', 5, 'The title Google shows (pasted from a search) equals your title = pass. Cut off = partly. Rewritten = fix. Blank = not checked.',
     'When Google rewrites a title, look at what it used instead (often the H1 or a shorter phrase) and close the gap.'),
    ('Site name once', 3, 'The site name appears exactly once = pass. Not at all = partly. Twice or more = fix.',
     'Add the site name once, at the start or end, after a simple separator such as a hyphen or colon.'),
    ('Clean separators', 3, 'No square brackets = pass. A pipe = partly. Square brackets = fix.',
     'Use one plain separator. In the Zyppy study, titles with brackets and pipes were rewritten more often than titles with dashes.'),
]
NCH = len(CHECKS)

# Title patterns for the Title Builder: name, pattern, best for
PATTERNS = [
    ('Keyword: angle', '{keyword}: {angle}', 'Guides, explainers, tools'),
    ('How to', 'How to {keyword}: {angle}', 'Step by step guides'),
    ('Keyword: number and proof', '{keyword}: {qualifier} {angle}', 'Lists and reviews based on your own tests'),
    ('Comparison', '{keyword}: Which Is Better for {angle}?', 'X vs Y pages'),
    ('Product with spec', '{keyword} with {angle} ({qualifier})', 'Product pages'),
    ('Category', '{keyword}: {angle} ({qualifier})', 'Category and collection pages'),
    ('Local', '{keyword} in {qualifier}: {angle}', 'Local landing pages'),
    ('Free tool', 'Free {keyword}: {angle}', 'Calculators and tools'),
    ('Dated guide', '{keyword} ({qualifier}): {angle}', 'Guides you really update every year'),
    ('Question', '{keyword}? {angle}', 'Question led articles'),
]
PAT_ROW = CHK_ROW + NCH + 4

# Demo: BrewNest, a fictional coffee gear shop and brewing blog in Bengaluru. Every page and number is illustrative.
# url, type, kw, title, h1, google shows, impressions, clicks, position, proposed, notes
P = [
    ('https://brewnest.example/', 'Home', 'specialty coffee gear', 'Home | BrewNest', 'Specialty coffee gear, delivered across India',
     'BrewNest: Specialty Coffee Gear Online in India', 9000, 1350, 1.8, 'BrewNest: Specialty Coffee Gear and Fresh Beans in India', 'Google already rewrites it'),
    ('https://brewnest.example/coffee-grinders/', 'Category', 'coffee grinders', 'Coffee Grinders: Manual and Electric Burr Grinders - BrewNest',
     'Coffee Grinders', 'Coffee Grinders: Manual and Electric Burr Grinders - BrewNest', 21000, 610, 7.9, '', ''),
    ('https://brewnest.example/hand-coffee-grinder/', 'Product', 'hand coffee grinder', 'BrewNest Hand Coffee Grinder with Ceramic Burrs and 40 Settings',
     'Hand Coffee Grinder with Ceramic Burrs', '', 6000, 260, 5.5, '', ''),
    ('https://brewnest.example/guides/pour-over-coffee-ratio/', 'Article or guide', 'pour over coffee ratio',
     'The Ultimate Guide to the Pour Over Coffee Ratio for Beginners and Experts in 2024 | BrewNest', 'Pour Over Coffee Ratio: Grams, Water and Time',
     'Pour Over Coffee Ratio: Grams, Water and Time', 12400, 150, 6.2,
     'Pour Over Coffee Ratio: Grams, Water and Time (With Chart)', 'Worked example in the guide'),
    ('https://brewnest.example/guides/french-press-ratio/', 'Article or guide', 'french press ratio', 'French Press Ratio: Grams of Coffee per Cup (Chart) - BrewNest',
     'French Press Ratio for 1 to 8 Cups', 'French Press Ratio: Grams of Coffee per Cup (Chart) - BrewNest', 8800, 620, 3.1, '', 'Title test won in October'),
    ('https://brewnest.example/guides/descale-coffee-machine/', 'Article or guide', 'descale a coffee machine', 'How to Descale a Coffee Machine With Vinegar or Citric Acid',
     'How to Descale a Coffee Machine', 'How to Descale a Coffee Machine With Vinegar or Citric Acid', 15000, 960, 4.6, '', 'New title live since 12 Nov'),
    ('https://brewnest.example/blog/best-coffee-beans-india/', 'Article or guide', 'best coffee beans in india', 'Best Coffee Beans in India 2025: 12 We Tasted - BrewNest',
     'The 12 Best Coffee Beans in India', '', 30000, 420, 9.8, 'Best Coffee Beans in India 2026: 12 We Tasted Blind', 'Content refreshed this month'),
    ('https://brewnest.example/guides/aeropress-recipe/', 'Article or guide', 'aeropress recipe', 'Coffee Brewing Guide - BrewNest', 'Our Favourite AeroPress Recipe',
     'AeroPress Recipe: Our Favourite 2 Minute Brew - BrewNest', 4200, 90, 8.6, 'AeroPress Recipe: Our 2 Minute Brew With 15 g of Coffee', 'Shares its title with the moka pot guide'),
    ('https://brewnest.example/guides/moka-pot/', 'Article or guide', 'how to use a moka pot', 'Coffee Brewing Guide - BrewNest', 'How to Use a Moka Pot',
     '', 3100, 75, 12.4, 'How to Use a Moka Pot: 6 Steps for Strong Coffee', ''),
    ('https://brewnest.example/coffee-beans/', 'Category', 'coffee beans', 'Coffee Beans, Buy Coffee Beans, Coffee Beans Online, Arabica Coffee Beans Best Price',
     'Coffee Beans', 'Coffee Beans: Buy Fresh Roasted Arabica Online', 18000, 290, 11.3, 'Coffee Beans: Fresh Roasted Arabica, Shipped in 48 Hours', ''),
    ('https://brewnest.example/coffee-roastery-bengaluru/', 'Local landing', 'coffee roastery in bengaluru', 'Coffee Roastery in Bengaluru: Visit Our Indiranagar Cafe - BrewNest',
     'Our coffee roastery in Bengaluru', '', 2600, 210, 3.4, '', ''),
    ('https://brewnest.example/tools/coffee-ratio-calculator/', 'Tool', 'coffee ratio calculator', 'Coffee Ratio Calculator: Grams of Coffee and Water for Any Brew',
     'Coffee Ratio Calculator', 'Coffee Ratio Calculator: Grams of Coffee and Water for Any Brew', 11000, 1580, 2.4, '', ''),
    ('https://brewnest.example/guides/espresso-grind-size/', 'Article or guide', 'espresso grind size', 'Espresso Grind Size Chart [Updated] - BrewNest',
     'Espresso Grind Size: A Simple Chart', 'Espresso Grind Size Chart - BrewNest', 5200, 240, 6.9, '', ''),
    ('https://brewnest.example/about/', 'About or contact', 'brewnest', 'About BrewNest - BrewNest', 'About BrewNest', '', 400, 60, 1.3, 'About BrewNest: Our Bengaluru Roastery and Team', ''),
]
# url index, old title, new title, date changed, status, impr before, clicks before, pos before, impr after, clicks after, pos after, notes
TESTS = [
    (4, 'French Press Ratio Guide - BrewNest', None, '2026-09-15', 'Live', 8200, 330, 3.3, 8800, 620, 3.1, 'Added grams per cup and the word Chart'),
    (5, 'Descaling Your Coffee Machine: A Complete Guide - BrewNest', None, '2026-11-12', 'Live', 14600, 700, 4.8, None, None, None, 'Too early to judge'),
    (2, 'Hand Coffee Grinder - BrewNest', None, '2026-08-20', 'Live', 5600, 240, 5.6, 6000, 260, 5.5, 'Added the burr and settings detail'),
    (11, 'Coffee Ratio Calculator - BrewNest', None, '2026-07-01', 'Live', 9000, 1050, 4.9, 11000, 1580, 2.4, 'Moved from 4.9 to 2.4: CTR change is not only the title'),
    (6, 'Best Coffee Beans in India: Our Top Picks', None, '2026-06-10', 'Reverted', 28000, 520, 9.5, 27000, 380, 9.9, 'Lost clicks, old title restored'),
    (3, None, 'Pour Over Coffee Ratio: Grams, Water and Time (With Chart)', '2026-11-28', 'Planned', 12400, 150, 6.2, None, None, None, 'From the worked example'),
]
# Title Builder demo rows: page type, pattern, keyword, angle, qualifier, add site name
BUILD = [
    ('Article or guide', 'Keyword: angle', 'Pour Over Coffee Ratio', 'Grams, Water and Time', '', 'No'),
    ('Article or guide', 'How to', 'Use a Moka Pot', '6 Steps for Strong Coffee', '', 'Yes'),
    ('Article or guide', 'Keyword: number and proof', 'Best Coffee Beans in India', 'We Tasted Blind', '12', 'No'),
    ('Article or guide', 'Comparison', 'Burr vs Blade Grinder', 'Pour Over', '', 'Yes'),
    ('Product', 'Product with spec', 'Hand Coffee Grinder', 'Ceramic Burrs', '40 Settings', 'No'),
    ('Category', 'Category', 'Coffee Grinders', 'Manual and Electric', '32 Models', 'Yes'),
    ('Local landing', 'Local', 'Coffee Roastery', 'Visit Our Indiranagar Cafe', 'Bengaluru', 'Yes'),
    ('Tool', 'Free tool', 'Coffee Ratio Calculator', 'Grams for Any Brew Method', '', 'No'),
    ('Article or guide', 'Dated guide', 'Coffee Subscription Prices in India', 'Every Plan Compared', '2026', 'No'),
    ('Article or guide', 'Question', 'Is a Burr Grinder Worth It', 'We Tested 6 for a Month', '', 'Yes'),
]

IN_HEAD = ['URL', 'Page type', 'Focus keyword', 'Current title tag', 'H1', 'Title Google shows (paste, optional)', 'Impressions (28 days)',
           'Clicks (28 days)', 'Avg position', 'Proposed new title', 'Notes']
MEAS_HEAD = ['Characters', 'Words', 'Title without site name', 'Pages with this title', 'Keyword starts at character', 'Keyword count',
             'Site name count', 'Year in title', 'Position band', 'CTR', 'Band average CTR', 'CTR vs band', 'Google shows it']
OUT_HEAD = ['Score (0 to 100)', 'Grade', 'Fixes needed', 'Fixes in priority order', 'Priority', 'Missed clicks (estimate)',
            'Proposed characters', 'Proposed title check', 'Opportunity (helper)', 'In CTR average (helper)']
NIN, NME = len(IN_HEAD), len(MEAS_HEAD)
C0 = NIN + NME + 1
CK = [L(C0 + i) for i in range(NCH)]
SC = C0 + NCH
HEAD = IN_HEAD + MEAS_HEAD + [c[0] for c in CHECKS] + OUT_HEAD
F_COLS = tuple(range(NIN + 1, len(HEAD) + 1))
M = {h: L(i + 1) for i, h in enumerate(HEAD)}


def tl(c):
    return f'{TL}!${c}${TL_FIRST}:${c}${TL_LAST}'


def d(s):
    return datetime.date.fromisoformat(s) if s else None


def settings_sheet(wb):
    ws = wb.create_sheet(S)
    ws.sheet_view.showGridLines = False
    K.title_block(ws, 'Settings', 'Every threshold, weight, list and pattern used by this workbook. Change a blue value and every score updates.')
    for c, w in zip('ABCDEFGHIJKLMN', [50, 14, 60, 60, 3, 14, 16, 3, 20, 3, 10, 3, 12, 12]):
        ws.column_dimensions[c].width = w
    rows = [
        (4, 'TITLE RULES', None, None),
        (5, 'Analysis date (set it to the day you check)', datetime.date(2026, 11, 21), 'dd mmm yyyy'),
        (6, 'Site name (exactly as it appears in your titles)', 'BrewNest', '@'),
        (7, 'Separator the Title Builder puts before the site name', ' - ', '@'),
        (8, 'Title is short below (characters)', 30, '0'),
        (9, 'Title may be cut off above (characters)', 60, '0'),
        (10, 'Title is very long above (characters)', 70, '0'),
        (11, 'Keyword is near the start when it begins by character', 25, '0'),
        (12, 'Half empty: fewer characters than this without the site name', 15, '0'),
        (14, 'CTR RULES (compared with your own Search Console data)', None, None),
        (15, 'Minimum impressions before CTR is judged', 100, '#,##0'),
        (16, 'CTR is fine at or above this share of the band average', 0.8, '0%'),
        (17, 'CTR is low below this share of the band average', 0.5, '0%'),
        (18, 'High impressions (for Rewrite first)', 1000, '#,##0'),
        (19, 'Title test: days to wait before judging', 28, '0'),
        (20, 'Title test: a win or loss needs a CTR change of at least', 0.1, '0%'),
        (21, 'Title test: fair only if the position moved by at most', 2, '0.0'),
        (23, 'GRADES AND PRIORITY', None, None),
        (24, 'Grade A when the score is at least', 85, '0'),
        (25, 'Grade B when at least', 70, '0'),
        (26, 'Grade C when at least (below = D)', 55, '0'),
        (27, 'Rewrite the title when the score is below', 50, '0'),
        (28, 'Close to the top: average position from', 4, '0'),
        (29, 'Close to the top: average position up to', 20, '0'),
    ]
    for r, label, val, fmt in rows:
        a = ws.cell(row=r, column=1, value=label)
        a.font = K.f(10, val is None, K.DEEP if val is None else K.INK)
        if val is not None:
            c = ws.cell(row=r, column=2, value=val)
            c.border, c.fill = K.BORDER, K.INPUT_FILL
            c.font = K.f(10, True, '0000FF')
            c.number_format = fmt
    ws['C5'] = ('Google sets no character limit for titles and cuts title links to fit the device. The 30, 60 and 70 character bands are assumptions '
                'of this kit, informed by the Zyppy title rewrite study (51 to 60 characters were rewritten least, over 70 almost always). '
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
    ws.cell(row=PAT_ROW - 2, column=1, value='TITLE PATTERNS for the Title Builder ({keyword}, {angle} and {qualifier} are filled in; add your own in the empty rows)').font = K.f(10, True, K.DEEP)
    K.header_row(ws, PAT_ROW - 1, ['Pattern name', 'Pattern', 'Best for', 'Example from the demo'])
    ex = {b[1]: b for b in BUILD}
    for i in range(15):
        r = PAT_ROW + i
        vals = list(PATTERNS[i]) if i < len(PATTERNS) else ['', '', '']
        for col, v in enumerate(vals, 1):
            ws.cell(row=r, column=col, value=v or None)
        if i < len(PATTERNS) and PATTERNS[i][0] in ex:
            j = BUILD.index(ex[PATTERNS[i][0]])
            ws.cell(row=r, column=4, value=f"='Title Builder'!G{TB_FIRST + j}")
        for col in range(1, 5):
            c = ws.cell(row=r, column=col)
            c.border = K.BORDER
            c.fill = K.FORMULA_FILL if col == 4 else K.INPUT_FILL
            c.font = K.f(10, col == 1, '0000FF' if col == 2 else K.INK)
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
    ws['I4'] = 'VAGUE TITLES'
    ws['I4'].font = K.f(10, True, K.DEEP)
    for i, t in enumerate(VAGUE_LIST):
        c = ws.cell(row=5 + i, column=9, value=t)
        c.fill, c.border = K.INPUT_FILL, K.BORDER
    ws['K4'] = 'YEARS'
    ws['K4'].font = K.f(10, True, K.DEEP)
    for i in range(21):
        c = ws.cell(row=5 + i, column=11, value=2015 + i)
        c.fill, c.border = K.INPUT_FILL, K.BORDER
    ws['M4'] = 'LISTS'
    ws['M4'].font = K.f(10, True, K.DEEP)
    for col, vals in (('M', ['Yes/No', 'Yes', 'No']), ('N', ['Test status'] + TSTAT)):
        for i, v in enumerate(vals):
            c = ws[f'{col}{5 + i}']
            c.value = v
            c.font = K.f(9, i == 0, '555555')
    return ws


def lab_sheet(wb):
    ws = wb.create_sheet('Title Lab')
    ws.sheet_view.showGridLines = False
    K.title_block(ws, 'Title lab', f'Rows 5 to {4 + len(P)} hold DEMO data for BrewNest, a fictional coffee gear shop (illustrative titles and numbers). Select the yellow demo cells and press Delete to start your own. Grey formula columns stay.')
    ws['A2'].font = K.f(10, True, 'B45309')
    ws['A3'] = 'One row per page. Paste the title from the page source, the H1, and (optional) the title Google shows in a real search. Add Search Console numbers for the last 28 days. 500 rows ready.'
    ws['A3'].font = K.f(9, False, '666666', True)
    widths = ([42, 14, 24, 48, 34, 44, 10, 9, 8, 46, 26] + [8, 7, 32, 8, 9, 8, 8, 7, 11, 8, 9, 8, 11] +
              [9] * NCH + [9, 7, 7, 56, 30, 10, 9, 34, 8, 8])
    K.header_row(ws, 4, HEAD, formula_cols=F_COLS, widths=widths)
    for i, col in enumerate(CK):
        c = ws[f'{col}3']
        c.value = f'={S}!$B${CHK_ROW + i}'
        c.font, c.fill, c.alignment = K.f(9, True, K.DEEP), K.SOFT, Alignment(horizontal='center')
    ws[f'{CK[0]}2'] = 'Check weights (from Settings)'
    ws[f'{CK[0]}2'].font = K.f(9, True, K.DEEP)
    m = M
    for r in range(TL_FIRST, TL_LAST + 1):
        i = r - TL_FIRST
        if i < len(P):
            for col, v in enumerate(P[i], 1):
                if v not in (None, ''):
                    ws.cell(row=r, column=col, value=v)
        e = f'A{r}=""'
        g = lambda h: f'{m[h]}{r}'
        D, C, J = f'D{r}', f'C{r}', f'J{r}'
        f = {}
        f['Characters'] = f'=IF({e},"",LEN({D}))'
        f['Words'] = f'=IF(OR({e},TRIM({D})=""),"",LEN(TRIM({D}))-LEN(SUBSTITUTE(TRIM({D})," ",""))+1)'
        core = f'TRIM(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE({D},{SITE},"")," | "," ")," - "," "),"|"," "),": "," "))'
        f['Title without site name'] = f'=IF(OR({e},{D}=""),"",IF({SITE}="",TRIM({D}),{core}))'
        f['Pages with this title'] = f'=IF(OR({e},{D}=""),"",SUMPRODUCT(--($D${TL_FIRST}:$D${TL_LAST}={D})))'
        f['Keyword starts at character'] = f'=IF(OR({e},{C}="",{D}=""),"",IFERROR(SEARCH({C},{D}),0))'
        f['Keyword count'] = f'=IF(OR({e},{C}="",{D}=""),"",(LEN({D})-LEN(SUBSTITUTE(LOWER({D}),LOWER({C}),"")))/LEN({C}))'
        f['Site name count'] = f'=IF(OR({e},{SITE}="",{D}=""),"",(LEN({D})-LEN(SUBSTITUTE(LOWER({D}),LOWER({SITE}),"")))/LEN({SITE}))'
        yr = f'SUMPRODUCT(MAX(ISNUMBER(SEARCH({YEARS},{D}))*{YEARS}))'
        f['Year in title'] = f'=IF(OR({e},{D}=""),"",IF({yr}=0,"",{yr}))'
        f['Position band'] = f'=IF(OR({e},N(I{r})=0),"",LOOKUP(I{r},{S}!$F$6:$F$9,{S}!$G$6:$G$9))'
        f['CTR'] = f'=IF(OR({e},N(G{r})=0,H{r}=""),"",H{r}/G{r})'
        band, ctr = g('Position band'), g('CTR')
        bc = f'$' + m['Position band']
        hc = '$' + m['In CTR average (helper)']
        hr = f'{hc}${TL_FIRST}:{hc}${TL_LAST},"Yes"'
        f['Band average CTR'] = (f'=IF(OR({ctr}="",{band}=""),"",IFERROR(SUMIFS($H${TL_FIRST}:$H${TL_LAST},{bc}${TL_FIRST}:{bc}${TL_LAST},{band},$G${TL_FIRST}:$G${TL_LAST},">="&{MINIMP},{hr})'
                                 f'/SUMIFS($G${TL_FIRST}:$G${TL_LAST},{bc}${TL_FIRST}:{bc}${TL_LAST},{band},$G${TL_FIRST}:$G${TL_LAST},">="&{MINIMP},{hr}),""))')
        bav = g('Band average CTR')
        f['CTR vs band'] = f'=IF({g("In CTR average (helper)")}<>"Yes","",IF(OR({ctr}="",{bav}="",N(G{r})<{MINIMP}),"",IF({bav}=0,"",{ctr}/{bav})))'
        stem = f'TRIM(SUBSTITUTE(SUBSTITUTE(F{r},"...",""),"…",""))'
        f['Google shows it'] = (f'=IF(OR({e},F{r}="",{D}=""),"",IF(TRIM(F{r})=TRIM({D}),"As written",IF(AND(LEN({stem})>0,LEN({stem})<LEN(TRIM({D})),'
                                f'LEFT(TRIM({D}),LEN({stem}))={stem}),"Cut off","Rewritten")))')
        kwpos, kwc, sn, yv, rat, gs = (g(h) for h in ('Keyword starts at character', 'Keyword count', 'Site name count', 'Year in title', 'CTR vs band', 'Google shows it'))
        commas = f'(LEN({D})-LEN(SUBSTITUTE({D},",","")))'
        cr = g('Title without site name')
        t = {}
        t['Title present, not half empty'] = f'=IF({e},"",IF(OR({D}="",LEN({cr})<{HALF}),0,1))'
        t['Keyword in title'] = f'=IF(OR({e},{C}=""),"",IF(N({kwpos})>0,1,0))'
        t['Unique title'] = f'=IF(OR({e},{D}=""),"",IF({g("Pages with this title")}>1,0,1))'
        t['Title length'] = f'=IF({e},"",IF({D}="",0,IF(LEN({D})>{TLONG},0,IF(AND(LEN({D})>={TMIN},LEN({D})<={TMAX}),1,0.5))))'
        t['No keyword stuffing'] = f'=IF(OR({e},{D}=""),"",IF(OR(N({kwc})>=3,{commas}>=3),0,IF(N({kwc})=2,0.5,1)))'
        t['Specific, not vague'] = (f'=IF(OR({e},{D}=""),"",IF(COUNTIF({VAGUE},{cr})>0,0,'
                                    f'IF(LEN(TRIM({cr}))-LEN(SUBSTITUTE(TRIM({cr})," ",""))+1<3,0.5,1)))')
        t['CTR vs your site average'] = f'=IF(OR({e},{rat}=""),"",IF({rat}>={CTRG},1,IF({rat}>={CTRL},0.5,0)))'
        t['Keyword near the start'] = f'=IF(OR({e},N({kwpos})=0),"",IF({kwpos}<={NEAR},1,0.5))'
        t['Year is current'] = f'=IF(OR({e},{yv}=""),"",IF({yv}>=YEAR({DATE}),1,0))'
        t['Matches the H1'] = f'=IF(OR({e},{C}=""),"",IF(E{r}="",0,IF(ISNUMBER(SEARCH({C},E{r})),1,0.5)))'
        t['Shown as written'] = f'=IF(OR({e},{gs}=""),"",IF({gs}="As written",1,IF({gs}="Cut off",0.5,0)))'
        t['Site name once'] = f'=IF(OR({e},{sn}=""),"",IF({sn}=1,1,IF({sn}=0,0.5,0)))'
        t['Clean separators'] = f'=IF(OR({e},{D}=""),"",IF(ISNUMBER(FIND("[",{D})),0,IF(ISNUMBER(FIND("|",{D})),0.5,1)))'
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
        z = f'I{r}'
        ctrchk = f'{m["CTR vs your site average"]}{r}'
        ws[g('Priority')] = (
            f'=IF(OR({e},{sc}{r}=""),"",IF({CK[0]}{r}=0,"Fix now: missing or half empty",IF({m["No keyword stuffing"]}{r}=0,"Fix now: keyword stuffing",'
            f'IF(AND(ISNUMBER({ctrchk}),{ctrchk}=0,N(G{r})>={BIGIMP}),"Rewrite first: low CTR, high impressions",IF({sc}{r}>={GA},"Healthy: monitor",'
            f'IF(AND(N({z})>=1,N({z})<{SD1}),"Protect: test carefully",IF(AND(N({z})>={SD1},N({z})<={SD2}),"Fix first: close to the top",'
            f'IF({sc}{r}<{REWRITE},"Rewrite the title","Improve when you can"))))))))')
        ws[g('Missed clicks (estimate)')] = f'=IF(OR({e},{rat}=""),"",IF({rat}>=1,0,ROUND(G{r}*({bav}-{ctr}),0)))'
        ws[g('Proposed characters')] = f'=IF(OR({e},{J}=""),"",LEN({J}))'
        pyr = f'SUMPRODUCT(MAX(ISNUMBER(SEARCH({YEARS},{J}))*{YEARS}))'
        issues = (f'_xlfn.TEXTJOIN("; ",TRUE,IF(LEN({J})>{TMAX},"may be cut off",""),IF(LEN({J})<{TMIN},"short",""),'
                  f'IF({C}="","",IF(ISNUMBER(SEARCH({C},{J})),IF(SEARCH({C},{J})>{NEAR},"keyword late",""),"no keyword")),'
                  f'IF(SUMPRODUCT(--($D${TL_FIRST}:$D${TL_LAST}={J}))-IF({D}={J},1,0)>0,"same as another page",""),'
                  f'IF(ISNUMBER(FIND("[",{J})),"brackets",""),IF(AND({pyr}>0,{pyr}<YEAR({DATE})),"old year",""))')
        ws[g('Proposed title check')] = f'=IF(OR({e},{J}=""),"",IF({issues}="","Ready to test",{issues}))'
        mc = g('Missed clicks (estimate)')
        ws[g('Opportunity (helper)')] = f'=IF(OR({e},N({mc})=0),"",{mc}+ROW()/100000)'
        ws[g('In CTR average (helper)')] = f'=IF({e},"",IFERROR(VLOOKUP(B{r},{S}!$F$13:$G${12 + len(PAGE_TYPES)},2,FALSE),"Yes"))'
    nf = {7: '#,##0', 8: '#,##0', 9: '0.0', NIN + 10: '0.0%', NIN + 11: '0.0%', NIN + 12: '0%', SC: '0', SC + 5: '#,##0', SC + 8: '0.00000'}
    K.style_body(ws, TL_FIRST, TL_LAST, len(HEAD), formula_cols=F_COLS, number_formats=nf, wrap_cols=(4, 6, 10, NIN + 3, SC + 3, SC + 7))
    ws.freeze_panes = 'B5'
    ws.auto_filter.ref = f'A4:{L(len(HEAD))}{TL_LAST}'
    K.dropdown(ws, f'B{TL_FIRST}:B{TL_LAST}', f'{S}!$F$13:$F${12 + len(PAGE_TYPES)}')
    chk = f'{CK[0]}{TL_FIRST}:{CK[-1]}{TL_LAST}'
    ws.conditional_formatting.add(chk, CellIsRule(operator='equal', formula=['1'], fill=PatternFill('solid', fgColor='D9F2C4')))
    ws.conditional_formatting.add(chk, CellIsRule(operator='equal', formula=['0.5'], fill=PatternFill('solid', fgColor='FFF4CC')))
    ws.conditional_formatting.add(chk, FormulaRule(formula=[f'AND(ISNUMBER({CK[0]}{TL_FIRST}),{CK[0]}{TL_FIRST}=0)'], fill=PatternFill('solid', fgColor='F8D7D3'), font=Font(name=K.FONT, bold=True, color='9B2C1F')))
    scol = L(SC)
    ws.conditional_formatting.add(f'{scol}{TL_FIRST}:{scol}{TL_LAST}', ColorScaleRule(start_type='num', start_value=30, start_color='F8D7D3', mid_type='num', mid_value=70, mid_color='FFF4CC', end_type='num', end_value=100, end_color='B7E4A0'))
    gcol = f'{L(SC + 1)}{TL_FIRST}:{L(SC + 1)}{TL_LAST}'
    for val, col in (('A', '9BE07A'), ('B', 'D9F2C4'), ('C', 'FFF4CC'), ('D', 'F8D7D3')):
        ws.conditional_formatting.add(gcol, CellIsRule(operator='equal', formula=[f'"{val}"'], fill=PatternFill('solid', fgColor=col), font=Font(name=K.FONT, bold=True)))
    pc = L(SC + 4)
    pr = f'{pc}{TL_FIRST}:{pc}{TL_LAST}'
    for start, n, fill, fc in (('Fix now', 7, '9B2C1F', 'FFFFFF'), ('Rewrite first', 13, 'F8D7D3', '9B2C1F'), ('Fix first', 9, 'FCE4D6', '9B2C1F'), ('Healthy', 7, 'D9F2C4', '1F1F1F')):
        ws.conditional_formatting.add(pr, FormulaRule(formula=[f'LEFT({pc}{TL_FIRST},{n})="{start}"'], fill=PatternFill('solid', fgColor=fill), font=Font(name=K.FONT, bold=True, color=fc)))
    ch = m['Characters']
    ws.conditional_formatting.add(f'{ch}{TL_FIRST}:{ch}{TL_LAST}', FormulaRule(formula=[f'AND($A{TL_FIRST}<>"",OR({ch}{TL_FIRST}<{TMIN},{ch}{TL_FIRST}>{TMAX}))'], font=Font(name=K.FONT, bold=True, color='B45309')))
    gsc = m['Google shows it']
    ws.conditional_formatting.add(f'{gsc}{TL_FIRST}:{gsc}{TL_LAST}', CellIsRule(operator='equal', formula=['"Rewritten"'], font=Font(name=K.FONT, bold=True, color='9B2C1F')))
    pcc = m['Proposed title check']
    ws.conditional_formatting.add(f'{pcc}{TL_FIRST}:{pcc}{TL_LAST}', CellIsRule(operator='equal', formula=['"Ready to test"'], fill=PatternFill('solid', fgColor='D9F2C4'), font=Font(name=K.FONT, bold=True)))
    ws.conditional_formatting.add(f'{pcc}{TL_FIRST}:{pcc}{TL_LAST}', FormulaRule(formula=[f'AND({pcc}{TL_FIRST}<>"",{pcc}{TL_FIRST}<>"Ready to test")'], fill=PatternFill('solid', fgColor='FFF4CC')))
    ws.column_dimensions[L(SC + 8)].hidden = True
    ws.column_dimensions[L(SC + 9)].hidden = True
    return ws


def builder_sheet(wb):
    ws = wb.create_sheet('Title Builder')
    ws.sheet_view.showGridLines = False
    K.title_block(ws, 'Title builder', 'Pick a pattern, type the keyword, the angle and a qualifier (a number, a year or a place). The title, its length and a fit check build themselves. Patterns live on Settings.')
    head = ['Page type', 'Pattern', 'Keyword (as it should read)', 'Angle or benefit', 'Qualifier (number, year, place)', 'Add site name?',
            'Built title', 'Characters', 'Fit', 'Keyword near the start?']
    fc = (7, 8, 9, 10)
    K.header_row(ws, 4, head, formula_cols=fc, widths=[16, 24, 32, 32, 16, 10, 62, 9, 14, 12])
    pat_rng = f'{S}!$A${PAT_ROW}:$B${PAT_ROW + 14}'
    for r in range(TB_FIRST, TB_LAST + 1):
        i = r - TB_FIRST
        if i < len(BUILD):
            for col, v in enumerate(BUILD[i], 1):
                if v not in (None, ''):
                    ws.cell(row=r, column=col, value=v)
        e = f'OR(B{r}="",C{r}="")'
        pat = f'IFERROR(VLOOKUP(B{r},{pat_rng},2,FALSE),"")'
        fill = f'SUBSTITUTE(SUBSTITUTE(SUBSTITUTE({pat},"{{keyword}}",C{r}),"{{angle}}",D{r}),"{{qualifier}}",E{r})'
        clean = f'TRIM(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE({fill},"()",""),"( )","")," :",":"))'
        full = f'IF(F{r}="Yes",{clean}&{SEP}&{SITE},{clean})'
        ws.cell(row=r, column=7, value=f'=IF(OR({e},{pat}=""),"",UPPER(LEFT({full},1))&MID({full},2,500))')
        ws.cell(row=r, column=8, value=f'=IF(G{r}="","",LEN(G{r}))')
        ws.cell(row=r, column=9, value=f'=IF(G{r}="","",IF(H{r}>{TLONG},"Too long",IF(H{r}>{TMAX},"May be cut off",IF(H{r}<{TMIN},"Short","Fits"))))')
        ws.cell(row=r, column=10, value=f'=IF(G{r}="","",IF(IFERROR(SEARCH(C{r},G{r}),999)<={NEAR},"Yes","No"))')
    K.style_body(ws, TB_FIRST, TB_LAST, len(head), formula_cols=fc, wrap_cols=(7,))
    K.dropdown(ws, f'A{TB_FIRST}:A{TB_LAST}', f'{S}!$F$13:$F${12 + len(PAGE_TYPES)}')
    K.dropdown(ws, f'B{TB_FIRST}:B{TB_LAST}', f'{S}!$A${PAT_ROW}:$A${PAT_ROW + 14}')
    K.dropdown(ws, f'F{TB_FIRST}:F{TB_LAST}', f'{S}!$M$6:$M$7')
    rng = f'I{TB_FIRST}:I{TB_LAST}'
    ws.conditional_formatting.add(rng, CellIsRule(operator='equal', formula=['"Fits"'], fill=PatternFill('solid', fgColor='D9F2C4'), font=Font(name=K.FONT, bold=True)))
    ws.conditional_formatting.add(rng, CellIsRule(operator='equal', formula=['"May be cut off"'], fill=PatternFill('solid', fgColor='FFF4CC')))
    ws.conditional_formatting.add(rng, CellIsRule(operator='equal', formula=['"Too long"'], fill=PatternFill('solid', fgColor='F8D7D3'), font=Font(name=K.FONT, bold=True, color='9B2C1F')))
    ws.freeze_panes = 'A5'
    return ws


def test_sheet(wb):
    ws = wb.create_sheet('Test Log')
    ws.sheet_view.showGridLines = False
    K.title_block(ws, 'Title test log', 'Log every title change with the Search Console numbers for 28 days before and 28 days after. The verdict waits long enough and warns you when the position moved too, because then CTR changes for other reasons.')
    head = ['URL', 'Old title', 'New title', 'Date changed', 'Status', 'Impressions before', 'Clicks before', 'Position before',
            'Impressions after', 'Clicks after', 'Position after', 'Notes', 'CTR before', 'CTR after', 'CTR change', 'Position change',
            'Days live', 'New title characters', 'Verdict']
    fc = tuple(range(13, 20))
    K.header_row(ws, 4, head, formula_cols=fc, widths=[40, 40, 40, 12, 10, 11, 9, 9, 11, 9, 9, 34, 9, 9, 9, 9, 8, 10, 34])
    for r in range(TS_FIRST, TS_LAST + 1):
        i = r - TS_FIRST
        if i < len(TESTS):
            u, old, new, dt, st, ib, cb, pb, ia, ca, pa, note = TESTS[i]
            vals = [P[u][0], old if old else None, new if new else None, d(dt), st, ib, cb, pb, ia, ca, pa, note]
            for col, v in enumerate(vals, 1):
                if v not in (None, ''):
                    ws.cell(row=r, column=col, value=v)
            if not old:
                ws.cell(row=r, column=2, value=f"=IFERROR(INDEX({tl('D')},MATCH(A{r},{tl('A')},0)),\"\")")
            if not new:
                ws.cell(row=r, column=3, value=f"=IFERROR(INDEX({tl('D')},MATCH(A{r},{tl('A')},0)),\"\")")
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
            f'IF(ABS(N(P{r}))>{POSMOVE},"Position moved: not a fair test",IF(O{r}>={WIN},"Win: keep the new title",'
            f'IF(O{r}<=-{WIN},"Loss: revert or try again","No clear change"))))))))'))
    K.style_body(ws, TS_FIRST, TS_LAST, len(head), formula_cols=fc,
                 number_formats={4: 'dd mmm yyyy', 6: '#,##0', 7: '#,##0', 8: '0.0', 9: '#,##0', 10: '#,##0', 11: '0.0', 13: '0.0%', 14: '0.0%', 15: '+0%;-0%;0%', 16: '+0.0;-0.0;0.0', 17: '0'},
                 wrap_cols=(2, 3, 12, 19))
    for i in range(len(TESTS)):
        for col in (2, 3):
            c = ws.cell(row=TS_FIRST + i, column=col)
            if isinstance(c.value, str) and c.value.startswith('='):
                c.fill = K.FORMULA_FILL
    K.dropdown(ws, f'A{TS_FIRST}:A{TS_LAST}', tl('A'))
    K.dropdown(ws, f'E{TS_FIRST}:E{TS_LAST}', f'{S}!$N$6:$N$8')
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
    for c, w in zip('ABCDEFGHIJ', [40, 12, 3, 44, 26, 9, 9, 11, 30, 3]):
        ws.column_dimensions[c].width = w
    m = M
    sc, gr, pr = m['Score (0 to 100)'], m['Grade'], m['Priority']
    kpis = [
        ('Pages checked', f'=COUNTA({tl("A")})', '0'),
        ('Average score', f'=IFERROR(ROUND(AVERAGE({tl(sc)}),0),0)', '0'),
        ('Grade A or B pages', f'=COUNTIF({tl(gr)},"A")+COUNTIF({tl(gr)},"B")', '0'),
        ('Grade C or D pages', f'=COUNTIF({tl(gr)},"C")+COUNTIF({tl(gr)},"D")', '0'),
        ('Missing or half empty titles', f'=COUNTIF({tl(CK[0])},0)', '0'),
        ('Pages sharing a title', f'=COUNTIF({tl(m["Pages with this title"])},">1")', '0'),
        ('Titles over the cut off length', f'=COUNTIF({tl(m["Characters"])},">"&{TMAX})', '0'),
        ('Focus keyword missing from the title', f'=COUNTIF({tl(m["Keyword in title"])},0)', '0'),
        ('Titles with an old year', f'=COUNTIF({tl(m["Year is current"])},0)', '0'),
        ('Titles Google rewrites (of those you pasted)', f'=COUNTIF({tl(m["Google shows it"])},"Rewritten")', '0'),
        ('Rewrite first: low CTR, high impressions', f'=COUNTIF({tl(pr)},"Rewrite first*")', '0'),
        ('Missed clicks per 28 days (estimate)', f'=SUM({tl(m["Missed clicks (estimate)"])})', '#,##0'),
        ('Title tests won', f"=COUNTIF('Test Log'!$S${TS_FIRST}:$S${TS_LAST},\"Win*\")", '0'),
        ('Title tests waiting', f"=COUNTIF('Test Log'!$S${TS_FIRST}:$S${TS_LAST},\"Too early*\")+COUNTIF('Test Log'!$S${TS_FIRST}:$S${TS_LAST},\"Not live*\")", '0'),
    ]
    ws['A4'] = 'KEY NUMBERS'
    ws['A4'].font = K.f(10, True, K.DEEP)
    for i, (label, fml, fmt) in enumerate(kpis):
        r = 5 + i
        ws.cell(row=r, column=1, value=label).font = K.f(10)
        c = ws.cell(row=r, column=2, value=fml)
        c.number_format, c.font, c.fill, c.border = fmt, K.f(11, True), K.FORMULA_FILL, K.BORDER
    # top click opportunities
    ws['D4'] = 'BIGGEST CLICK OPPORTUNITIES (CTR below your own band average)'
    ws['D4'].font = K.f(10, True, K.DEEP)
    for j, h in enumerate(['URL', 'Focus keyword', 'CTR', 'Band avg', 'Missed clicks', 'Priority']):
        c = ws.cell(row=5, column=4 + j, value=h)
        c.font, c.fill = K.f(10, True, 'FFFFFF'), K.HEAD_F
    op = tl(m['Opportunity (helper)'])
    for k in range(1, 11):
        r = 5 + k
        mt = f'MATCH(LARGE({op},{k}),{op},0)'
        for j, col in enumerate(['A', 'C', m['CTR'], m['Band average CTR'], m['Missed clicks (estimate)'], pr]):
            c = ws.cell(row=r, column=4 + j, value=f'=IFERROR(INDEX({tl(col)},{mt}),"")')
            c.border, c.fill, c.font = K.BORDER, K.FORMULA_FILL, K.f(9, j == 0)
            c.number_format = ['@', '@', '0.0%', '0.0%', '#,##0', '@'][j]
    # CTR by band
    top = 22
    ws.cell(row=top - 1, column=1, value='YOUR CTR BY POSITION BAND (pages in the averages with enough impressions)').font = K.f(10, True, K.DEEP)
    for j, h in enumerate(['Position band', 'Pages', 'Impressions', 'Clicks', 'CTR']):
        c = ws.cell(row=top, column=1 + j, value=h)
        c.font, c.fill = K.f(10, True, 'FFFFFF'), K.HEAD_F
    bcol = tl(m['Position band'])
    for i in range(len(BANDS)):
        r = top + 1 + i
        ws.cell(row=r, column=1, value=f'={S}!G{6 + i}')
        crit = f'{tl("G")},">="&{MINIMP},{tl(m["In CTR average (helper)"])},"Yes"'
        ws.cell(row=r, column=2, value=f'=COUNTIFS({bcol},A{r},{crit})')
        ws.cell(row=r, column=3, value=f'=SUMIFS({tl("G")},{bcol},A{r},{crit})')
        ws.cell(row=r, column=4, value=f'=SUMIFS({tl("H")},{bcol},A{r},{crit})')
        ws.cell(row=r, column=5, value=f'=IF(C{r}=0,0,D{r}/C{r})')
        for cc, fmt in ((1, '@'), (2, '0'), (3, '#,##0'), (4, '#,##0'), (5, '0.0%')):
            cell = ws.cell(row=r, column=cc)
            cell.border, cell.fill, cell.number_format = K.BORDER, K.FORMULA_FILL, fmt
    # failing each check
    t2 = top + len(BANDS) + 3
    for j, h in enumerate(['Check', 'Pages to fix', 'Partly']):
        c = ws.cell(row=t2, column=1 + j, value=h)
        c.font, c.fill = K.f(10, True, 'FFFFFF'), K.HEAD_F
    for i, col in enumerate(CK):
        r = t2 + 1 + i
        ws.cell(row=r, column=1, value=f'={S}!A{CHK_ROW + i}').border = K.BORDER
        for cc, val in ((2, 0), (3, 0.5)):
            c = ws.cell(row=r, column=cc, value=f'=COUNTIF({tl(col)},{val})')
            c.border, c.fill = K.BORDER, K.FORMULA_FILL
    ws.conditional_formatting.add(f'B{t2 + 1}:B{t2 + NCH}', ColorScaleRule(start_type='num', start_value=0, start_color='FFFFFF', end_type='num', end_value=6, end_color='E07A5F'))
    c1 = chart(ws, 'Your CTR by position band', 'CTR', 1, [5], top + 1, top + len(BANDS), 'K4', [K.GREEN], False, False, pct=True)
    c1.y_axis.scaling.min = 0
    chart(ws, 'Pages failing each check', 'Pages', 1, [2, 3], t2 + 1, t2 + NCH, 'K21', ['E07A5F', 'F2C94C'], True, True, h=11, stacked=True)
    return ws, top, t2


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
        ('Demo data', 'BrewNest and every page in the demo are fictional (.example domain). All titles, impressions, clicks, positions and test results are illustrative, not real data.', ''),
        ('Score', 'Weighted share of the 13 checks a title passes (pass 1, partly 0.5, fix 0). Checks without data are left out. Weights, grade bands and priority rules live on Settings and are assumptions to tune.', ''),
        ('Length bands', 'Google says there is no limit on the length of a title element and that title links are shortened to fit the device width. The 30, 60 and 70 character bands are assumptions of this kit.', ''),
        ('Rewrite studies', 'Zyppy (early 2022, 80,959 titles on 2,370 sites) found Google rewrote 61.6 percent of titles; 51 to 60 characters were rewritten least and over 70 characters 99.9 percent of the time; brackets 77.6 percent, pipes 41 percent of the time versus 19.7 percent for dashes. A 2025 study published on Search Engine Land reported 76 percent. Methods differ, so treat both as signals, not rules.', 'https://zyppy.com/seo/google-title-rewrites/'),
        ('CTR comparison', 'CTR is compared with the average CTR of your own pages in the same position band (pages with at least 100 impressions), never with an outside benchmark. Missed clicks = impressions x (band average CTR minus page CTR): an estimate, not a promise.', ''),
        ('Title tests', 'Search Console data is compared for 28 days before and after a change. A test is called fair only when the average position moved by 2 or less, because position changes CTR on its own. Both numbers are assumptions you can change.', ''),
    ])
    K.start_here(
        wb, 'Title Tag Optimization Kit',
        [
            'This workbook checks every title tag on your site against 13 rules that matter for Google and for AI search: a real, specific title, the keyword near the start, a sensible length, no stuffing, unique titles, a current year, a match with the H1, clean separators and whether Google shows your title as written. It compares each page CTR with your own average for the same position band, so you know which titles cost you clicks.',
            f'It ships with demo data for a fictional coffee gear shop ({len(P)} pages, {len(BUILD)} built titles and {len(TESTS)} title tests) so you can see every check working. Clear the yellow demo cells when you are ready.',
        ],
        [
            ('Title Lab', 'One row per page with 500 ready rows: current title, H1, the title Google shows and Search Console numbers, plus 13 measures, 13 checks, score, grade, fixes, priority, missed clicks and a check of your proposed title.'),
            ('Title Builder', 'Build new titles from 10 patterns (keyword, angle, qualifier, optional site name) with length and fit checks.'),
            ('Test Log', 'Log each title change with 28 days before and after. The verdict waits, compares CTR and warns when the position moved too.'),
            ('Dashboard', 'Key numbers, the 10 biggest click opportunities, your CTR by position band and pages failing each check, with two charts.'),
            ('Settings', 'Analysis date, site name, length bands, CTR rules, grades, the 13 check weights with rules and fixes, title patterns and lists.'),
            ('AI Prompts', 'Prompts for ChatGPT, Claude or Gemini to write, test and fix titles.'),
            ('Checklist', 'The title tag checklist as a tick list with automatic progress.'),
            ('Sources', 'Where facts come from and which numbers are assumptions.'),
        ],
        [
            'Look at the demo on Title Lab, Test Log and the Dashboard, then clear the yellow demo cells.',
            'On Settings, set the analysis date and type your site name exactly as it appears in your titles.',
            'Export pages from Search Console (Performance, Pages, last 28 days) and add URL, impressions, clicks and position to Title Lab.',
            'Paste each page title from the page source, the H1, the focus keyword and, for important pages, the title Google shows in a real search.',
            'Sort by Priority. Start with Fix now, then Rewrite first and Fix first. Write a proposed title until it says Ready to test.',
            'Use the Title Builder for new pages or full rewrites. Copy the best title into the Proposed column.',
            'Change one title at a time, log it on Test Log, and judge it after 28 days. Keep the winners, revert the losers.',
        ],
        url,
    )
    order = ['Start Here', 'Title Lab', 'Title Builder', 'Test Log', 'Dashboard', 'Settings', 'AI Prompts', 'Checklist', 'Sources']
    wb._sheets = [wb[n] for n in order]
    wb.active = 0
    for ws in wb.worksheets:
        ws.sheet_properties.tabColor = K.GREEN if ws.title in order[:5] else 'A6EF39'
    wb.save(path)


PREVIEW = {'sheet': 'Title Lab', 'header_row': 4, 'rows': 12,
           'cols': [3, 4, NIN + 1, NIN + 13, SC, SC + 1, SC + 2, SC + 5, SC + 4],
           'formula_idx': [2, 3, 4, 5, 6, 7, 8]}


def check(wb):
    """Assert the worked examples used in the guide."""
    a = wb['Title Lab']
    v = lambda h, r: a[f'{M[h]}{r}'].value
    r = 8   # the pour over coffee ratio guide
    assert v('Characters', r) == 93 and v('Keyword starts at character', r) == 27 and v('Year in title', r) == 2024, (v('Characters', r), v('Keyword starts at character', r))
    assert v('Position band', r) == '4 to 10' and abs(v('CTR', r) - 150 / 12400) < 1e-9, v('CTR', r)
    assert abs(v('Band average CTR', r) - 2730 / 93800) < 1e-9 and round(v('CTR vs band', r), 2) == 0.42, v('Band average CTR', r)
    assert v('Google shows it', r) == 'Rewritten' and v('Missed clicks (estimate)', r) == 211, v('Missed clicks (estimate)', r)
    assert v('Title length', r) == 0 and v('Keyword near the start', r) == 0.5 and v('Clean separators', r) == 0.5 and v('Year is current', r) == 0, r
    assert v('Score (0 to 100)', r) == 66 and v('Grade', r) == 'C' and v('Fixes needed', r) == 6, v('Score (0 to 100)', r)
    assert v('Priority', r) == 'Rewrite first: low CTR, high impressions', v('Priority', r)
    assert v('Fixes in priority order', r) == ('Title length; CTR vs your site average; Keyword near the start (partly); Year is current; '
                                              'Shown as written; Clean separators (partly)'), v('Fixes in priority order', r)
    assert v('Proposed characters', r) == 58 and v('Proposed title check', r) == 'Ready to test', v('Proposed title check', r)
    # other pages used in the guide
    assert v('Title without site name', 5) == 'Home' and v('Score (0 to 100)', 5) == 44 and v('Priority', 5).startswith('Fix now'), v('Score (0 to 100)', 5)
    assert v('CTR vs band', 5) is None, v('CTR vs band', 5)
    assert v('Score (0 to 100)', 11) == 85 and v('Priority', 11).startswith('Rewrite first') and v('Missed clicks (estimate)', 11) == 453, v('Score (0 to 100)', 11)
    assert v('Pages with this title', 12) == 2 and v('Unique title', 13) == 0, v('Pages with this title', 12)
    assert v('Keyword count', 14) == 4 and v('Priority', 14) == 'Fix now: keyword stuffing', v('Priority', 14)
    assert v('Clean separators', 17) == 0 and v('Google shows it', 17) == 'Rewritten', v('Clean separators', 17)
    d = wb['Dashboard']
    assert d['B16'].value == 1115 and d['B5'].value == 14, d['B16'].value
    assert abs(d['E23'].value - 2410 / 22400) < 1e-9 and d['C24'].value == 93800, (d['E23'].value, d['C24'].value)
    t = wb['Test Log']
    assert t['S5'].value == 'Win: keep the new title' and round(t['O5'].value, 2) == 0.75, (t['S5'].value, t['O5'].value)
    assert t['S6'].value == 'Too early: wait 19 more days' and t['S7'].value == 'No clear change', (t['S6'].value, t['S7'].value)
    assert t['S8'].value == 'Position moved: not a fair test' and t['S10'].value == 'Not live yet', t['S8'].value
    b = wb['Title Builder']
    assert b['G5'].value == 'Pour Over Coffee Ratio: Grams, Water and Time' and b['H5'].value == 45, b['G5'].value
    assert b['I8'].value == 'May be cut off' and b['G6'].value.endswith(' - BrewNest'), (b['I8'].value, b['G6'].value)
