"""Search Intent Kit workbook (asset 02).

Intent Audit: one row per query. The sheet reads signal words in the query, counts the result types you saw
in the top 10, works out the dominant intent and how clear it is, recommends the page type the SERP rewards,
checks your current page against it, and ranks the fixes.
"""
from openpyxl.styles import PatternFill, Font
from openpyxl.formatting.rule import CellIsRule, ColorScaleRule
from openpyxl.chart import BarChart, Reference
from openpyxl.utils import get_column_letter as L
import kitlib as K

FIRST, LAST = 5, 504          # Intent Audit rows
PF_FIRST, PF_LAST = 5, 154    # Page Fit Plan rows
SIG_FIRST, SIG_LAST = 5, 44   # Intent Signals word list rows
S = 'Settings'
IA = "'Intent Audit'"
SIG = "'Intent Signals'"

# Demo data: BrewNest, a fictional online coffee equipment and beans store in India with one roastery in Pune.
# Numbers are illustrative only. SERP counts = how many of the top 10 organic results are each page type.
# query, topic, volume, value, guides, lists, product, brand, localpack, aio, top format, angle, your url, your type, owner, status
DEMO = [
    ('best espresso machine for home', 'Espresso machines', 6600, 3, 2, 7, 1, 0, 'No', 'Yes', 'Best of list', 'Tested picks with prices in rupees', '/espresso-machines/', 'Category page', 'Nisha', 'Planned'),
    ('espresso machine price', 'Espresso machines', 5400, 3, 0, 2, 8, 0, 'No', 'No', 'Category page', 'Price filters and EMI options', '/espresso-machines/', 'Category page', 'Nisha', 'Live'),
    ('how does an espresso machine work', 'Espresso machines', 1300, 1, 8, 0, 0, 0, 'No', 'Yes', 'Definition or explainer', 'Simple diagram of pump and boiler', '', '', 'Kabir', 'Planned'),
    ('espresso machine vs coffee maker', 'Espresso machines', 880, 2, 3, 6, 1, 0, 'No', 'Yes', 'Comparison', 'Taste, cost and effort side by side', '/blog/espresso-vs-coffee-maker/', 'Comparison', 'Kabir', 'Live'),
    ('best coffee grinder for espresso', 'Grinders', 2400, 3, 1, 8, 1, 0, 'No', 'Yes', 'Best of list', 'Budget tiers and burr type', '/blog/best-coffee-grinders/', 'Best of list', 'Kabir', 'Live'),
    ('burr vs blade grinder', 'Grinders', 1600, 2, 4, 6, 0, 0, 'No', 'Yes', 'Comparison', 'Which grinder for which brew', '/blog/grinder-guide/', 'How to guide', 'Kabir', 'Rework'),
    ('buy coffee grinder online', 'Grinders', 1900, 3, 0, 1, 9, 0, 'No', 'No', 'Category page', 'Fast delivery and warranty', '/grinders/', 'Category page', 'Nisha', 'Live'),
    ('espresso grind size', 'Grinders', 2900, 2, 7, 1, 0, 0, 'No', 'Yes', 'How to guide', 'Grind size chart by brew method', '/blog/grinder-guide/', 'How to guide', 'Kabir', 'Live'),
    ('how to make cold brew at home', 'Brewing guides', 8100, 2, 9, 0, 0, 0, 'No', 'Yes', 'How to guide', 'Ratio, steeping time, no special gear', '/blog/cold-brew-guide/', 'How to guide', 'Kabir', 'Live'),
    ('french press vs pour over', 'Brewing guides', 1000, 2, 5, 5, 0, 0, 'No', 'Yes', 'Comparison', 'Taste and effort for beginners', '', '', 'Kabir', 'Planned'),
    ('aeropress recipe', 'Brewing guides', 2400, 2, 9, 0, 1, 0, 'No', 'Yes', 'How to guide', 'Championship style recipes', '/blog/aeropress-recipes/', 'List of ideas or tips', 'Kabir', 'Optimize'),
    ('moka pot how to use', 'Brewing guides', 1300, 2, 8, 0, 0, 0, 'No', 'Yes', 'Video', 'Step by step with video', '/blog/moka-pot-guide/', 'How to guide', 'Kabir', 'Optimize'),
    ('coffee to water ratio', 'Brewing guides', 3600, 1, 9, 0, 0, 0, 'No', 'Yes', 'Definition or explainer', 'Quick ratio table by method', '', '', 'Kabir', 'Planned'),
    ('what is crema', 'Brewing guides', 720, 1, 9, 0, 0, 0, 'No', 'Yes', 'Definition or explainer', 'One line answer, then detail', '', '', '', 'Planned'),
    ('best coffee beans in india', 'Coffee beans', 4400, 3, 1, 7, 2, 0, 'No', 'Yes', 'Best of list', 'Roaster and roast level picks', '/coffee-beans/', 'Category page', 'Nisha', 'Rework'),
    ('coffee beans subscription', 'Coffee beans', 1000, 3, 0, 4, 6, 0, 'No', 'No', 'Pricing or service page', 'Flexible delivery and pause anytime', '/subscription/', 'Pricing or service page', 'Nisha', 'Live'),
    ('arabica vs robusta', 'Coffee beans', 2900, 1, 6, 4, 0, 0, 'No', 'Yes', 'Comparison', 'Taste, caffeine and price', '/blog/arabica-vs-robusta/', 'Comparison', 'Kabir', 'Live'),
    ('light vs dark roast caffeine', 'Coffee beans', 1300, 1, 9, 1, 0, 0, 'No', 'Yes', 'Definition or explainer', 'Clear answer, myth busting', '', '', '', 'Planned'),
    ('buy arabica coffee beans online', 'Coffee beans', 1600, 3, 0, 1, 9, 0, 'No', 'No', 'Category page', 'Fresh roast date on every bag', '/coffee-beans/', 'Category page', 'Nisha', 'Live'),
    ('coffee roasters in pune', 'Local', 590, 2, 3, 2, 4, 1, 'Yes', 'No', 'Local or location page', 'Map pack plus local lists', '/pune-roastery/', 'Local or location page', 'Nisha', 'Live'),
    ('brewnest login', 'Brand', 260, 1, 0, 0, 0, 10, 'No', 'No', 'Login or account page', '', '/account/login/', 'Login or account page', 'Nisha', 'Live'),
    ('brewnest coupon code', 'Brand', 480, 2, 1, 0, 4, 5, 'No', 'No', 'Homepage or brand page', 'Current offers in one place', '', '', 'Nisha', 'Planned'),
    ('brewnest reviews', 'Brand', 320, 3, 0, 4, 0, 6, 'No', 'No', 'Review', 'Third party reviews and ratings', '/reviews/', 'Review', 'Nisha', 'Live'),
    ('espresso machine not heating', 'Troubleshooting', 590, 2, 6, 0, 0, 0, 'No', 'Yes', 'List of ideas or tips', 'Causes and owner tested fixes', '/support/espresso-not-heating/', 'How to guide', 'Kabir', 'Live'),
    ('how to descale an espresso machine', 'Troubleshooting', 1900, 2, 8, 0, 1, 0, 'No', 'Yes', 'How to guide', 'Vinegar or descaler, step by step', '/blog/descale-espresso-machine/', 'How to guide', 'Kabir', 'Live'),
    ('why is my espresso bitter', 'Troubleshooting', 880, 2, 8, 0, 0, 0, 'No', 'Yes', 'List of ideas or tips', 'Causes and quick fixes', '', '', 'Kabir', 'Planned'),
    ('which espresso machine should i buy if i drink two lattes a day and have a small kitchen', 'Espresso machines', 10, 3, 2, 6, 2, 0, 'No', 'Yes', 'Best of list', 'Compact picks for milk drinks', '', '', 'Nisha', 'Planned'),
    ('coffee cost per cup calculator', 'Brewing guides', 390, 2, 2, 0, 6, 0, 'No', 'No', 'Tool or calculator', 'Instant per cup cost', '', '', 'Kabir', 'Planned'),
    ('coffee gift hamper', 'Gifts', 1600, 3, 1, 5, 4, 0, 'No', 'No', 'Best of list', 'Picks under 2,000 rupees', '/gifts/', 'Category page', 'Nisha', 'Rework'),
    ('espresso machine emi', 'Espresso machines', 590, 3, 1, 0, 8, 1, 'No', 'No', 'Pricing or service page', 'No cost EMI explained', '/espresso-machines/', 'Category page', 'Nisha', 'Optimize'),
]
TOPICS = ['Espresso machines', 'Grinders', 'Brewing guides', 'Coffee beans', 'Troubleshooting', 'Local', 'Brand', 'Gifts']

PAGE_TYPES = [
    ('How to guide', 'Informational'), ('Definition or explainer', 'Informational'), ('List of ideas or tips', 'Informational'),
    ('Video', 'Informational'), ('Forum or discussion', 'Informational'), ('Best of list', 'Commercial'),
    ('Comparison', 'Commercial'), ('Review', 'Commercial'), ('Alternatives page', 'Commercial'),
    ('Product page', 'Transactional'), ('Category page', 'Transactional'), ('Pricing or service page', 'Transactional'),
    ('Tool or calculator', 'Transactional'), ('Template or download', 'Transactional'), ('Local or location page', 'Transactional'),
    ('Homepage or brand page', 'Navigational'), ('Login or account page', 'Navigational'),
]
PT_FIRST = 5
PT_LAST = PT_FIRST + len(PAGE_TYPES) - 1   # Settings H5:I21

SIGNALS = {
    'B': ('Transactional signals', ['buy', 'order', 'price', 'prices', 'pricing', 'cost', 'cheap', 'cheapest', 'deal', 'deals', 'discount',
                                    'coupon', 'sale', 'shop', 'subscription', 'emi', 'for sale', 'quote', 'hire', 'book', 'download',
                                    'template', 'calculator', 'generator', 'free trial']),
    'C': ('Commercial signals', ['best', 'top', 'vs', 'versus', 'review', 'reviews', 'compare', 'comparison', 'alternative',
                                 'alternatives', 'worth it', 'pros and cons', 'rated', 'recommended', 'which', 'hamper', 'ideas for']),
    'D': ('Informational signals', ['how', 'what', 'why', 'when', 'who', 'guide', 'tutorial', 'tips', 'examples', 'meaning',
                                    'definition', 'is', 'does', 'can', 'ways', 'steps', 'learn', 'history', 'benefits', 'recipe',
                                    'explained', 'ratio', 'size', 'not working', 'not heating']),
    'E': ('Navigational signals (add your brands)', ['login', 'log in', 'sign in', 'sign up', 'account', 'app', 'contact',
                                                     'customer care', 'official', 'website', 'brewnest']),
    'F': ('Local signals (add your cities)', ['near me', 'nearby', 'open now', 'directions', 'showroom', 'store near', 'in pune', 'pune']),
}

HEAD = ['Query', 'Topic', 'Monthly Volume', 'Business Value (1 to 3)',
        'SERP: guides and articles', 'SERP: lists, reviews, comparisons', 'SERP: product, pricing, tool pages', 'SERP: brand, homepage, login',
        'Local pack?', 'AI Overview?', 'Top format seen', 'Content angle seen', 'Your URL', 'Your page type',
        'Words in query', 'Word signal intent', 'SERP intent', 'Dominant intent', 'Top type share', 'Intent clarity',
        'Secondary intents', 'Local intent?', 'Funnel stage', 'Recommended page type', 'Page fit', 'AI answer exposure',
        'Fix priority score (0 to 100)', 'Priority', 'Recommended action', 'Duplicate check', 'Owner', 'Status', 'Notes',
        'Helper: transactional words', 'Helper: commercial words', 'Helper: informational words', 'Helper: navigational words', 'Helper: local words']
FCOLS = tuple(range(15, 31)) + tuple(range(34, 39))
WIDTHS = [36, 17, 11, 11, 11, 11, 11, 11, 9, 10, 20, 28, 30, 20, 8, 14, 14, 14, 10, 13, 18, 9, 13, 20, 13, 12, 12, 10, 46, 13, 10, 12, 26, 11, 11, 11, 11, 11]


def settings_sheet(wb):
    ws = wb.create_sheet(S)
    ws.sheet_view.showGridLines = False
    K.title_block(ws, 'Settings', 'Every threshold, weight and lookup table used by the Intent Audit. Change a blue number and the whole workbook updates.')
    for col, w in zip('ABCDEFGHIJKLMN', [50, 12, 3, 24, 14, 24, 3, 26, 16, 3, 16, 10, 14, 3]):
        ws.column_dimensions[col].width = w
    rows = [
        (4, 'INTENT CLARITY', None, None),
        (5, 'Clear when the top result type holds at least', 0.7, '0%'),
        (6, 'Mostly clear when it holds at least (below this = Mixed)', 0.55, '0%'),
        (7, 'Show a secondary intent when its share is at least', 0.3, '0%'),
        (8, 'Long conversational query from this many words', 8, '0'),
        (9, 'Volume that earns full volume points', 20000, '#,##0'),
        (11, 'FIX PRIORITY WEIGHTS (any numbers, they are scaled)', None, None),
        (12, 'Volume weight', 30, '0'),
        (13, 'Business value weight', 30, '0'),
        (14, 'Page fit gap weight', 40, '0'),
        (15, 'Total weight (auto)', '=SUM(B12:B14)', '0'),
        (17, 'PRIORITY THRESHOLDS', None, None),
        (18, 'Fix now when score is at least', 70, '0'),
        (19, 'Next when score is at least', 50, '0'),
        (20, 'Later when score is at least (below = Monitor)', 30, '0'),
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
    ws['A22'] = 'All thresholds and weights are starter assumptions chosen for this kit, not Google numbers. Tune them to your market.'
    ws['A22'].font = K.f(9, False, '777777', True)

    def table(r0, col, title, head, data, fmts=None):
        ws.cell(row=r0, column=col, value=title).font = K.f(10, True, K.DEEP)
        rr = r0 + 1
        if head:
            for j, h in enumerate(head):
                c = ws.cell(row=rr, column=col + j, value=h)
                c.font = K.f(9, True, 'FFFFFF')
                c.fill = K.HEAD_IN
            rr += 1
        for i, row in enumerate(data):
            for j, v in enumerate(row):
                c = ws.cell(row=rr + i, column=col + j, value=v)
                c.fill = K.INPUT_FILL
                c.border = K.BORDER
                c.font = K.f(10, False, '0000FF' if isinstance(v, (int, float)) else K.INK)
                if fmts and j in fmts:
                    c.number_format = fmts[j]
        return rr

    # D4: page fit gap (rows 5 to 9)
    table(4, 4, 'PAGE FIT GAP (0 to 1)', None, [('No page yet', 0.8), ('Mismatch', 1), ('Close', 0.5), ('Match', 0.1), ('Choose your page type', 0.5)], {1: '0.0'})
    # D11: confidence by clarity (rows 12 to 15)
    table(11, 4, 'CONFIDENCE BY CLARITY', None, [('Clear', 1), ('Mostly clear', 0.85), ('Mixed', 0.7), ('No SERP data', 0.6)], {1: '0.00'})
    # D17: intent defaults (header row 18, data 19 to 23)
    table(17, 4, 'INTENT DEFAULTS', ['Intent', 'Funnel stage', 'Default page type'], [
        ('Informational', 'Awareness', 'How to guide'), ('Commercial', 'Consideration', 'Best of list'),
        ('Transactional', 'Decision', 'Product page'), ('Navigational', 'Retention', 'Homepage or brand page'),
        ('Unclear', '', 'Check the SERP')])
    # H4: page types (rows 5 to 21)
    ws.cell(row=4, column=8, value='PAGE TYPE').font = K.f(10, True, K.DEEP)
    ws.cell(row=4, column=9, value='INTENT FAMILY').font = K.f(10, True, K.DEEP)
    for i, (pt, fam) in enumerate(PAGE_TYPES):
        for j, v in enumerate((pt, fam)):
            c = ws.cell(row=PT_FIRST + i, column=8 + j, value=v)
            c.fill = K.INPUT_FILL
            c.border = K.BORDER
    ws.cell(row=PT_LAST + 2, column=8, value='Add your own page types at the end of this list').font = K.f(9, False, '777777', True)
    # Dropdown lists
    ws['K4'] = 'DROPDOWN LISTS'
    ws['K4'].font = K.f(10, True, K.DEEP)
    lists = {
        'K': ['Intent', 'Informational', 'Commercial', 'Transactional', 'Navigational'],
        'L': ['Yes/No', 'Yes', 'No'],
        'M': ['Status', 'Planned', 'In progress', 'Live', 'Optimize', 'Rework', 'Done'],
    }
    for col, vals in lists.items():
        for i, v in enumerate(vals):
            c = ws[f'{col}{5 + i}']
            c.value = v
            c.font = K.f(9, i == 0, '555555')
    return ws


def signals_sheet(wb):
    ws = wb.create_sheet('Intent Signals')
    ws.sheet_view.showGridLines = False
    K.title_block(ws, 'Intent signal words', 'Words that hint at intent. The Intent Audit matches them as whole words. Add your brand names and cities. Order of checks: navigational, transactional, commercial, informational.')
    ws.column_dimensions['A'].width = 4
    for col in 'BCDEF':
        ws.column_dimensions[col].width = 24
    for col, (head, words) in SIGNALS.items():
        c = ws[f'{col}4']
        c.value = head
        c.font = K.f(10, True, 'FFFFFF')
        c.fill = K.HEAD_IN
        c.alignment = K.Alignment(wrap_text=True)
        for i in range(SIG_LAST - SIG_FIRST + 1):
            cell = ws[f'{col}{SIG_FIRST + i}']
            cell.value = words[i] if i < len(words) else None
            cell.fill = K.INPUT_FILL
            cell.border = K.BORDER
            cell.font = K.f(10)
    ws.row_dimensions[4].height = 30
    # Reference: Google rater guideline intents vs the 4 type model
    ws.column_dimensions['H'].width = 22
    ws.column_dimensions['I'].width = 50
    ws.column_dimensions['J'].width = 30
    ws['H3'] = 'HOW THE FOUR TYPES MAP TO GOOGLE RATER GUIDELINE INTENTS'
    ws['H3'].font = K.f(10, True, K.DEEP)
    for j, h in enumerate(['Rater guideline intent', 'What the searcher wants', 'Closest type in this workbook']):
        c = ws.cell(row=4, column=8 + j, value=h)
        c.font = K.f(10, True, 'FFFFFF')
        c.fill = K.HEAD_F
        c.alignment = K.Alignment(wrap_text=True, vertical='center')
    ref = [
        ('Know', 'Find information or explore a topic', 'Informational'),
        ('Know Simple', 'A specific answer that fits in 1 or 2 sentences or a short list', 'Informational (high AI answer exposure)'),
        ('Do', 'Accomplish a goal or do something, such as buy, download or use a tool', 'Transactional'),
        ('Website', 'Reach a specific website or page', 'Navigational'),
        ('Visit in person', 'Find a business or a category of businesses nearby', 'Local intent flag plus Transactional'),
        ('Multiple intents', 'Many queries have more than one reasonable intent', 'Secondary intents column'),
    ]
    for i, row in enumerate(ref):
        for j, v in enumerate(row):
            c = ws.cell(row=5 + i, column=8 + j, value=v)
            c.font = K.f(10, j == 0)
            c.border = K.BORDER
            c.alignment = K.Alignment(wrap_text=True, vertical='top')
    ws['H12'] = 'Source: Google General Guidelines for Search Quality Evaluators (September 2025), section 12.7.'
    ws['H12'].font = K.f(9, False, '777777', True)
    return ws


def audit_sheet(wb):
    ws = wb.create_sheet('Intent Audit')
    ws.sheet_view.showGridLines = False
    K.title_block(ws, 'Search intent audit', 'Rows 5 to 34 hold DEMO data for BrewNest, a fictional coffee store (illustrative numbers). Select the yellow demo cells and press Delete to start your own audit. Grey formula columns stay.')
    ws['A2'].font = K.f(10, True, 'B45309')
    ws['A3'] = 'Search each query in a private window. Count the top 10 organic results by type in columns E to H, then pick the format that dominates. 500 rows ready.'
    ws['A3'].font = K.f(9, False, '666666', True)
    K.header_row(ws, 4, HEAD, formula_cols=FCOLS, widths=WIDTHS)
    T = lambda r: f'SUM($E{r}:$H{r})'
    sig = {34: 'B', 35: 'C', 36: 'D', 37: 'E', 38: 'F'}
    for r in range(FIRST, LAST + 1):
        i = r - FIRST
        if i < len(DEMO):
            d = DEMO[i]
            for col, v in zip(list(range(1, 15)) + [31, 32], d):
                if v is not None and v != '':
                    ws.cell(row=r, column=col, value=v)
        q = f'" "&SUBSTITUTE(SUBSTITUTE(LOWER(TRIM($A{r})),"?",""),",","")&" "'
        for col, sc in sig.items():
            rng = f'{SIG}!${sc}${SIG_FIRST}:${sc}${SIG_LAST}'
            ws.cell(row=r, column=col, value=f'=IF($A{r}="","",SUMPRODUCT(({rng}<>"")*ISNUMBER(SEARCH(" "&{rng}&" ",{q}))))')
        ws.cell(row=r, column=15, value=f'=IF(A{r}="","",LEN(TRIM(A{r}))-LEN(SUBSTITUTE(TRIM(A{r})," ",""))+1)')
        ws.cell(row=r, column=16, value=f'=IF(A{r}="","",IF(AK{r}>0,"Navigational",IF(AH{r}>0,"Transactional",IF(AI{r}>0,"Commercial",IF(AJ{r}>0,"Informational","Unclear")))))')
        ws.cell(row=r, column=17, value=f'=IF(OR(A{r}="",{T(r)}=0),"",CHOOSE(MATCH(MAX(E{r}:H{r}),E{r}:H{r},0),"Informational","Commercial","Transactional","Navigational"))')
        ws.cell(row=r, column=18, value=f'=IF(A{r}="","",IF(Q{r}<>"",Q{r},P{r}))')
        ws.cell(row=r, column=19, value=f'=IF(OR(A{r}="",{T(r)}=0),"",MAX(E{r}:H{r})/{T(r)})')
        ws.cell(row=r, column=20, value=f'=IF(A{r}="","",IF({T(r)}=0,"No SERP data",IF(S{r}>={S}!$B$5,"Clear",IF(S{r}>={S}!$B$6,"Mostly clear","Mixed"))))')
        parts = ','.join(f'IF(AND(R{r}<>"{n}",{c}{r}/{T(r)}>={S}!$B$7),"{n}","")' for c, n in zip('EFGH', ['Informational', 'Commercial', 'Transactional', 'Navigational']))
        tj = f'_xlfn.TEXTJOIN(", ",TRUE,{parts})'
        ws.cell(row=r, column=21, value=f'=IF(OR(A{r}="",{T(r)}=0),"",IF({tj}="","None",{tj}))')
        ws.cell(row=r, column=22, value=f'=IF(A{r}="","",IF(OR(I{r}="Yes",N(AL{r})>0),"Yes","No"))')
        ws.cell(row=r, column=23, value=f'=IF(A{r}="","",IFERROR(VLOOKUP(R{r},{S}!$D$19:$F$23,2,FALSE),""))')
        ws.cell(row=r, column=24, value=f'=IF(A{r}="","",IF(K{r}<>"",K{r},IFERROR(VLOOKUP(R{r},{S}!$D$19:$F$23,3,FALSE),"Check the SERP")))')
        fam = lambda x: f'IFERROR(VLOOKUP({x},{S}!$H${PT_FIRST}:$I${PT_LAST + 10},2,FALSE),"")'
        ws.cell(row=r, column=25, value=f'=IF(A{r}="","",IF(M{r}="","No page yet",IF(N{r}="","Choose your page type",IF(N{r}=X{r},"Match",IF({fam(f"N{r}")}={fam(f"X{r}")},"Close","Mismatch")))))')
        ws.cell(row=r, column=26, value=f'=IF(A{r}="","",IF(J{r}="Yes",IF(R{r}="Informational","High","Medium"),IF(R{r}="Informational","Medium","Low")))')
        ws.cell(row=r, column=27, value=(
            f'=IF(A{r}="","",ROUND(MIN(100,100*({S}!$B$12*MIN(1,LOG10(N(C{r})+1)/LOG10({S}!$B$9+1))'
            f'+{S}!$B$13*N(D{r})/3+{S}!$B$14*IFERROR(VLOOKUP(Y{r},{S}!$D$5:$E$9,2,FALSE),0.5))/{S}!$B$15'
            f'*IFERROR(VLOOKUP(T{r},{S}!$D$12:$E$15,2,FALSE),1)),0))'))
        ws.cell(row=r, column=28, value=f'=IF(AA{r}="","",IF(AA{r}>={S}!$B$18,"Fix now",IF(AA{r}>={S}!$B$19,"Next",IF(AA{r}>={S}!$B$20,"Later","Monitor"))))')
        base = (f'IF(Y{r}="Mismatch","Rebuild as "&LOWER(X{r})&". The SERP rewards "&LOWER(R{r})&" pages.",'
                f'IF(Y{r}="No page yet","Create a "&LOWER(X{r})&" for this query.",'
                f'IF(Y{r}="Close","Reshape into a "&LOWER(X{r})&" and match the angle.",'
                f'IF(Y{r}="Choose your page type","Pick your page type to check the fit.",'
                f'IF(R{r}="Navigational","Keep the brand page clear and fast.",'
                f'IF(Z{r}="High","Fit is right. Add an answer first block plus depth AI cannot give.","Fit is right. Beat the top pages on depth and angle."))))))')
        mixed = (f'IF(T{r}="Mixed",IF(U{r}<>"None"," Mixed SERP: cover "&LOWER(U{r})&" needs in their own section."," Mixed SERP: study the top 10 again before you build."),"")')
        local = f'IF(V{r}="Yes"," Local intent: link your location page and Business Profile.","")'
        longq = f'IF(N(O{r})>={S}!$B$8," Long conversational query: answer it in a FAQ or section.","")'
        ws.cell(row=r, column=29, value=f'=IF(A{r}="","",{base}&{mixed}&{local}&{longq})')
        ws.cell(row=r, column=30, value=f'=IF(A{r}="","",IF(COUNTIF($A${FIRST}:$A${LAST},A{r})>1,"Duplicate query","OK"))')
    K.style_body(ws, FIRST, LAST, len(HEAD), formula_cols=FCOLS, number_formats={3: '#,##0', 19: '0%', 27: '0'}, wrap_cols=(12, 21, 29, 33))
    ws.freeze_panes = 'B5'
    ws.auto_filter.ref = f'A4:{L(len(HEAD))}{LAST}'
    K.dropdown(ws, f'D{FIRST}:D{LAST}', '"1,2,3"', '3 = close to a sale or lead, 2 = builds trust, 1 = loosely related')
    K.dropdown(ws, f'I{FIRST}:J{LAST}', f'{S}!$L$6:$L$7')
    K.dropdown(ws, f'K{FIRST}:K{LAST}', f'{S}!$H${PT_FIRST}:$H${PT_LAST + 10}', 'The format most top 10 results share')
    K.dropdown(ws, f'N{FIRST}:N{LAST}', f'{S}!$H${PT_FIRST}:$H${PT_LAST + 10}', 'What your page is today')
    K.dropdown(ws, f'AF{FIRST}:AF{LAST}', f'{S}!$M$6:$M$11')
    K.whole_number(ws, f'E{FIRST}:H{LAST}', 0, 10, 'Count of top 10 results, from 0 to 10.')
    red = PatternFill('solid', fgColor='F8D7D3')
    ws.conditional_formatting.add(f'Y{FIRST}:Y{LAST}', CellIsRule(operator='equal', formula=['"Mismatch"'], fill=red, font=Font(name=K.FONT, bold=True, color='9B2C1F')))
    ws.conditional_formatting.add(f'Y{FIRST}:Y{LAST}', CellIsRule(operator='equal', formula=['"Close"'], fill=PatternFill('solid', fgColor='FFE8B3')))
    ws.conditional_formatting.add(f'Y{FIRST}:Y{LAST}', CellIsRule(operator='equal', formula=['"Match"'], fill=PatternFill('solid', fgColor='D9F2C4')))
    ws.conditional_formatting.add(f'Y{FIRST}:Y{LAST}', CellIsRule(operator='equal', formula=['"No page yet"'], fill=PatternFill('solid', fgColor='DCEBFF')))
    ws.conditional_formatting.add(f'T{FIRST}:T{LAST}', CellIsRule(operator='equal', formula=['"Mixed"'], fill=PatternFill('solid', fgColor='FFE8B3')))
    ws.conditional_formatting.add(f'Z{FIRST}:Z{LAST}', CellIsRule(operator='equal', formula=['"High"'], fill=PatternFill('solid', fgColor='DCEBFF'), font=Font(name=K.FONT, bold=True)))
    pr = f'AB{FIRST}:AB{LAST}'
    ws.conditional_formatting.add(pr, CellIsRule(operator='equal', formula=['"Fix now"'], fill=PatternFill('solid', fgColor='9BE07A'), font=Font(name=K.FONT, bold=True)))
    ws.conditional_formatting.add(pr, CellIsRule(operator='equal', formula=['"Next"'], fill=PatternFill('solid', fgColor='D9F2C4')))
    ws.conditional_formatting.add(pr, CellIsRule(operator='equal', formula=['"Later"'], fill=PatternFill('solid', fgColor='FFF4CC')))
    ws.conditional_formatting.add(f'AA{FIRST}:AA{LAST}', ColorScaleRule(start_type='num', start_value=0, start_color='F8D7D3', mid_type='num', mid_value=50, mid_color='FFF4CC', end_type='num', end_value=100, end_color='B7E4A0'))
    ws.conditional_formatting.add(f'AD{FIRST}:AD{LAST}', CellIsRule(operator='equal', formula=['"Duplicate query"'], font=Font(name=K.FONT, bold=True, color='C0392B')))
    return ws


def col(c):
    return f'{IA}!${c}${FIRST}:${c}${LAST}'


def dashboard_sheet(wb):
    ws = wb.create_sheet('Dashboard')
    ws.sheet_view.showGridLines = False
    K.title_block(ws, 'Dashboard', 'Everything here calculates from the Intent Audit. Type your topic names in the yellow cells of the topic table.')
    for c, w in zip('ABCDEFGHIJ', [40, 13, 3, 24, 11, 12, 12, 3, 3, 3]):
        ws.column_dimensions[c].width = w
    A = col('A')
    kpis = [
        ('Queries audited', f'=COUNTA({A})', '0'),                                          # B5
        ('Total monthly search volume', f'=SUM({col("C")})', '#,##0'),                      # B6
        ('Queries with SERP data', f'=SUMPRODUCT(({A}<>"")*({col("T")}<>"No SERP data"))', '0'),  # B7
        ('Clear intent', f'=COUNTIF({col("T")},"Clear")', '0'),                            # B8
        ('Mostly clear intent', f'=COUNTIF({col("T")},"Mostly clear")', '0'),              # B9
        ('Mixed intent', f'=COUNTIF({col("T")},"Mixed")', '0'),                            # B10
        ('Pages that mismatch the SERP (queries)', f'=COUNTIF({col("Y")},"Mismatch")', '0'),   # B11
        ('Search volume on mismatched queries', f'=SUMIF({col("Y")},"Mismatch",{col("C")})', '#,##0'),  # B12
        ('Queries with no page yet', f'=COUNTIF({col("Y")},"No page yet")', '0'),          # B13
        ('Fix now', f'=COUNTIF({col("AB")},"Fix now")', '0'),                              # B14
        ('Share with an AI Overview', f'=IFERROR(COUNTIF({col("J")},"Yes")/B5,0)', '0%'),  # B15
        ('High AI answer exposure', f'=COUNTIF({col("Z")},"High")', '0'),                  # B16
        ('Long conversational queries', f'=COUNTIF({col("O")},">="&Settings!$B$8)', '0'),  # B17
        ('Queries with local intent', f'=COUNTIF({col("V")},"Yes")', '0'),                 # B18
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

    def mini(r0, head, labels, formulas):
        for j, h in enumerate(head):
            c = ws.cell(row=r0, column=4 + j, value=h)
            c.font = K.f(10, True, 'FFFFFF')
            c.fill = K.HEAD_F
        for i, lab in enumerate(labels):
            r = r0 + 1 + i
            ws.cell(row=r, column=4, value=lab)
            for j, fm in enumerate(formulas):
                c = ws.cell(row=r, column=5 + j, value=fm(r))
                c.number_format = '#,##0'
            for cc in range(4, 4 + len(head)):
                ws.cell(row=r, column=cc).border = K.BORDER
                ws.cell(row=r, column=cc).font = K.f(10)

    mini(4, ['Dominant intent', 'Queries', 'Volume', 'Mismatches'], ['Informational', 'Commercial', 'Transactional', 'Navigational', 'Unclear'], [
        lambda r: f'=COUNTIF({col("R")},D{r})', lambda r: f'=SUMIF({col("R")},D{r},{col("C")})',
        lambda r: f'=COUNTIFS({col("R")},D{r},{col("Y")},"Mismatch")'])
    mini(11, ['Page fit', 'Queries', 'Volume'], ['Match', 'Close', 'Mismatch', 'No page yet', 'Choose your page type'], [
        lambda r: f'=COUNTIF({col("Y")},D{r})', lambda r: f'=SUMIF({col("Y")},D{r},{col("C")})'])
    # Topic table
    top = 21
    K.header_row(ws, top, ['Topic (type names)', 'Queries', None, 'Volume', 'Informational', 'Commercial', 'Transactional', 'Navigational', 'Mismatches', 'Fix now'],
                 formula_cols=(2, 4, 5, 6, 7, 8, 9, 10))
    ws.cell(row=top, column=3).fill = PatternFill(fill_type=None)
    for cc, w in zip('HIJ', [13, 11, 9]):
        ws.column_dimensions[cc].width = w
    for i in range(20):
        r = top + 1 + i
        a = ws.cell(row=r, column=1, value=TOPICS[i] if i < len(TOPICS) else None)
        a.fill = K.INPUT_FILL
        ws.cell(row=r, column=2, value=f'=IF(A{r}="","",COUNTIF({col("B")},A{r}))')
        ws.cell(row=r, column=4, value=f'=IF(A{r}="","",SUMIF({col("B")},A{r},{col("C")}))').number_format = '#,##0'
        for cc, it in zip(range(5, 9), ['Informational', 'Commercial', 'Transactional', 'Navigational']):
            ws.cell(row=r, column=cc, value=f'=IF(A{r}="","",COUNTIFS({col("B")},A{r},{col("R")},"{it}"))')
        ws.cell(row=r, column=9, value=f'=IF(A{r}="","",COUNTIFS({col("B")},A{r},{col("Y")},"Mismatch"))')
        ws.cell(row=r, column=10, value=f'=IF(A{r}="","",COUNTIFS({col("B")},A{r},{col("AB")},"Fix now"))')
        for cc in range(1, 11):
            if cc == 3:
                continue
            c = ws.cell(row=r, column=cc)
            c.border = K.BORDER
            c.font = K.f(10)
            if cc > 1:
                c.fill = K.FORMULA_FILL

    def bar(title, ytitle, data_rows, anchor, color):
        ch = BarChart()
        ch.type = 'bar'
        ch.title = title
        ch.y_axis.title = ytitle
        ch.add_data(Reference(ws, min_col=5, min_row=data_rows[0], max_row=data_rows[1]), titles_from_data=False)
        ch.set_categories(Reference(ws, min_col=4, min_row=data_rows[0], max_row=data_rows[1]))
        ch.legend = None
        ch.height, ch.width = 6.5, 13
        ch.roundedCorners = False
        ch.x_axis.delete = False
        ch.y_axis.delete = False
        ch.title.overlay = False
        ch.y_axis.title.overlay = False
        ch.series[0].graphicalProperties.solidFill = color
        ws.add_chart(ch, anchor)

    bar('Queries by dominant intent', 'Queries', (5, 9), 'L4', K.GREEN)
    bar('Queries by page fit', 'Queries', (12, 16), 'L19', '2B2B2B')
    return ws


def page_fit_sheet(wb):
    ws = wb.create_sheet('Page Fit Plan')
    ws.sheet_view.showGridLines = False
    K.title_block(ws, 'Page fit plan', 'One row per URL. Grey columns count the queries you mapped to that URL on the Intent Audit and flag pages that try to serve more than one intent. DEMO rows are for the fictional BrewNest.')
    head = ['URL', 'Page type today', 'Queries mapped', 'Volume mapped', 'Informational', 'Commercial', 'Transactional', 'Navigational',
            'Intents on this URL', 'Mismatched queries', 'Top query by volume', 'Verdict', 'Planned fix', 'Owner', 'Due date', 'Status']
    fc = tuple(range(3, 13))
    K.header_row(ws, 4, head, formula_cols=fc, widths=[34, 22, 10, 11, 12, 12, 12, 12, 10, 11, 34, 44, 36, 10, 12, 12])
    urls = []
    for d in DEMO:
        if d[12] and d[12] not in [u for u, _ in urls]:
            urls.append((d[12], d[13]))
    plans = {'/espresso-machines/': 'Keep as category page. Build a separate best espresso machines guide and link both ways.',
             '/blog/grinder-guide/': 'Split: keep grind size guide, move burr vs blade into its own comparison.',
             '/coffee-beans/': 'Keep as category page. Publish a best coffee beans list that links to products.',
             '/gifts/': 'Add a curated gift guide section above the product grid.'}
    for r in range(PF_FIRST, PF_LAST + 1):
        i = r - PF_FIRST
        if i < len(urls):
            ws.cell(row=r, column=1, value=urls[i][0])
            ws.cell(row=r, column=2, value=urls[i][1])
            if urls[i][0] in plans:
                ws.cell(row=r, column=13, value=plans[urls[i][0]])
                ws.cell(row=r, column=16, value='Planned')
        u = f'A{r}'
        ws.cell(row=r, column=3, value=f'=IF({u}="","",COUNTIF({col("M")},{u}))')
        ws.cell(row=r, column=4, value=f'=IF({u}="","",SUMIF({col("M")},{u},{col("C")}))')
        for cc, it in zip(range(5, 9), ['Informational', 'Commercial', 'Transactional', 'Navigational']):
            ws.cell(row=r, column=cc, value=f'=IF({u}="","",COUNTIFS({col("M")},{u},{col("R")},"{it}"))')
        ws.cell(row=r, column=9, value=f'=IF({u}="","",(E{r}>0)+(F{r}>0)+(G{r}>0)+(H{r}>0))')
        ws.cell(row=r, column=10, value=f'=IF({u}="","",COUNTIFS({col("M")},{u},{col("Y")},"Mismatch"))')
        ws.cell(row=r, column=11, value=(
            f'=IF({u}="","",IFERROR(INDEX({IA}!$A$1:$A${LAST},SUMPRODUCT(MAX(({col("M")}={u})*'
            f'({col("C")}=_xlfn.MAXIFS({col("C")},{col("M")},{u}))*ROW({col("M")})))),""))'))
        ws.cell(row=r, column=12, value=(
            f'=IF({u}="","",IF(N(C{r})=0,"No queries mapped yet",IF(I{r}>1,"Split or add sections: "&I{r}&" intents share this URL",'
            f'IF(J{r}>0,"Rebuild the format to match the SERP","Fit OK. Improve depth and angle"))))'))
    K.style_body(ws, PF_FIRST, PF_LAST, len(head), formula_cols=fc, number_formats={4: '#,##0', 15: 'dd mmm yyyy'}, wrap_cols=(11, 12, 13))
    K.dropdown(ws, f'B{PF_FIRST}:B{PF_LAST}', f'{S}!$H${PT_FIRST}:$H${PT_LAST + 10}')
    K.dropdown(ws, f'P{PF_FIRST}:P{PF_LAST}', f'{S}!$M$6:$M$11')
    from openpyxl.formatting.rule import FormulaRule
    ws.conditional_formatting.add(f'L{PF_FIRST}:L{PF_LAST}', FormulaRule(formula=[f'LEFT(L{PF_FIRST},5)="Split"'], fill=PatternFill('solid', fgColor='FFE8B3'), font=Font(name=K.FONT, bold=True)))
    ws.conditional_formatting.add(f'L{PF_FIRST}:L{PF_LAST}', FormulaRule(formula=[f'LEFT(L{PF_FIRST},7)="Rebuild"'], fill=PatternFill('solid', fgColor='F8D7D3'), font=Font(name=K.FONT, bold=True)))
    ws.freeze_panes = 'B5'
    ws.auto_filter.ref = f'A4:P{PF_LAST}'
    return ws


def build(path, asset, url):
    wb = K.new_book()
    audit_sheet(wb)
    dashboard_sheet(wb)
    page_fit_sheet(wb)
    signals_sheet(wb)
    settings_sheet(wb)
    K.prompts_sheet(wb, asset['prompts'], url)
    K.checklist_sheet(wb, list(asset['checklist']))
    K.sources_sheet(wb, asset['sources'], [
        ('Demo data', 'Rows 5 to 34 of Intent Audit and the demo rows of Page Fit Plan describe BrewNest, a fictional company. All volumes, SERP counts and pages are illustrative, not real data.', ''),
        ('Intent types', 'The four types (informational, commercial, transactional, navigational) are the common SEO model. The Intent Signals tab shows how they map to the Know, Know Simple, Do, Website and Visit in person intents in Google\'s rater guidelines.', ''),
        ('Clarity thresholds, weights, fit gap values', 'Editable assumptions chosen for this kit (Settings). They are not Google numbers. Tune them after your first audit.', ''),
        ('SERP intent', 'The type with the most top 10 results wins. Ties go to the leftmost column (guides, then lists, then product pages, then brand pages). When no SERP data is entered, the sheet falls back to signal words.', ''),
        ('Fix priority score', 'Weighted mix of volume (log scaled), business value and the page fit gap, multiplied by a confidence factor for intent clarity. Weights live on Settings.', ''),
    ])
    K.start_here(
        wb, 'Search Intent Kit',
        [
            'This workbook tells you what each query really wants and whether your page gives it. Count what ranks, and it works out the dominant intent, how clear it is, the page type Google rewards, and whether your page matches.',
            'It ships with 30 demo queries for a fictional coffee store so you can see every formula, the Page Fit Plan and the dashboard working. Clear the yellow demo cells when you are ready.',
        ],
        [
            ('Intent Audit', 'Your main sheet with 500 ready rows: SERP counts, AI Overview, top format, your page, plus 16 automatic columns from dominant intent to recommended action.'),
            ('Dashboard', 'Key numbers, intent and page fit tables, a topic table and two charts.'),
            ('Page Fit Plan', 'One row per URL. Flags pages that try to serve several intents at once and plans the fix.'),
            ('Intent Signals', 'Editable signal word lists (add your brand and cities) and how the four types map to Google rater guideline intents.'),
            ('Settings', 'Clarity thresholds, score weights, page types and their intent family, defaults and dropdown lists.'),
            ('AI Prompts', 'Prompts for ChatGPT, Claude or Gemini to classify intent, read SERPs, plan fan out questions and fix mismatches.'),
            ('Checklist', 'The full process as a tick list with automatic progress.'),
            ('Sources', 'Where facts come from and which numbers are assumptions.'),
        ],
        [
            'Look at the demo rows on Intent Audit, Page Fit Plan and Dashboard to see how it works, then clear the yellow demo cells.',
            'Add your brand names and cities on the Intent Signals tab.',
            'Paste your queries into column A with topic, volume and a business value from 1 to 3.',
            'Search each important query in a private window. Count the top 10 results by type (columns E to H) and note the local pack and AI Overview.',
            'Choose the top format you saw and note the angle the winners share.',
            'Add your ranking or target URL and choose what your page is today. The sheet shows Match, Close, Mismatch or No page yet.',
            'Sort by Fix priority score, then use Page Fit Plan to split pages that serve several intents.',
        ],
        url,
    )
    order = ['Start Here', 'Intent Audit', 'Dashboard', 'Page Fit Plan', 'Intent Signals', 'Settings', 'AI Prompts', 'Checklist', 'Sources']
    wb._sheets = [wb[n] for n in order]
    wb.active = 0
    for ws in wb.worksheets:
        ws.sheet_properties.tabColor = K.GREEN if ws.title in ('Start Here', 'Intent Audit', 'Dashboard') else 'A6EF39'
    wb.save(path)


PREVIEW = {'sheet': 'Intent Audit', 'header_row': 4, 'rows': 10, 'cols': [1, 3, 5, 6, 7, 8, 18, 20, 24, 25, 27, 28],
           'formula_idx': [6, 7, 8, 9, 10, 11]}


def check(wb):
    """Assert the worked examples used in the guide."""
    ws = wb['Intent Audit']
    # Worked example 1: best espresso machine for home (row 5)
    assert ws['P5'].value == 'Commercial', ws['P5'].value
    assert ws['Q5'].value == 'Commercial', ws['Q5'].value
    assert abs(ws['S5'].value - 0.7) < 1e-9, ws['S5'].value
    assert ws['T5'].value == 'Clear', ws['T5'].value
    assert ws['U5'].value == 'None', ws['U5'].value
    assert ws['X5'].value == 'Best of list', ws['X5'].value
    assert ws['Y5'].value == 'Mismatch', ws['Y5'].value
    assert ws['Z5'].value == 'Medium', ws['Z5'].value
    assert ws['AA5'].value == 97, ws['AA5'].value
    assert ws['AB5'].value == 'Fix now', ws['AB5'].value
    assert ws['AC5'].value.startswith('Rebuild as best of list. The SERP rewards commercial pages.'), ws['AC5'].value
    # Worked example 2: french press vs pour over (row 14), a 5 and 5 split
    assert ws['R14'].value == 'Informational', ws['R14'].value
    assert ws['T14'].value == 'Mixed', ws['T14'].value
    assert ws['U14'].value == 'Commercial', ws['U14'].value
    assert ws['Y14'].value == 'No page yet', ws['Y14'].value
    assert ws['AA14'].value == 51, ws['AA14'].value
    assert ws['AB14'].value == 'Next', ws['AB14'].value
    # Close fit and long query signal
    assert ws['Y15'].value == 'Close', ws['Y15'].value          # aeropress recipe: list vs how to guide
    assert ws['O31'].value >= 8 and 'Long conversational' in ws['AC31'].value
    assert ws['V24'].value == 'Yes'                              # coffee roasters in pune: local intent
    assert ws['P25'].value == 'Navigational'                     # brewnest login
    d = wb['Dashboard']
    assert d['B5'].value == len(DEMO), d['B5'].value
    pf = wb['Page Fit Plan']
    assert pf['A5'].value == '/espresso-machines/' and pf['C5'].value == 3 and pf['I5'].value == 2, (pf['C5'].value, pf['I5'].value)
    assert pf['L5'].value.startswith('Split'), pf['L5'].value
    assert pf['K5'].value == 'best espresso machine for home', pf['K5'].value
