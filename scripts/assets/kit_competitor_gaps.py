"""Competitor Gaps Kit workbook (asset 04).

Gap Finder: one row per keyword with your position and up to 4 competitor positions. The sheet sorts every
keyword into a gap type (Missing, Untapped, Weak, Shared, Strong, Unique, Open), scores the opportunity,
estimates the click upside, and writes the play. Competitors: estimated share of clicks, gap volume and AI
answer mentions per site. AI Answer Gaps: who AI answers mention and cite for your key prompts.
Action Plan: the target queue with owners and dates.
"""
from openpyxl.styles import PatternFill, Font, Alignment
from openpyxl.formatting.rule import CellIsRule, ColorScaleRule, FormulaRule
from openpyxl.chart import BarChart, Reference
from openpyxl.utils import get_column_letter as L
import kitlib as K

FIRST, LAST = 5, 504          # Gap Finder
AI_FIRST, AI_LAST = 5, 304    # AI Answer Gaps
AP_FIRST, AP_LAST = 5, 154    # Action Plan
S = 'Settings'
GF = "'Gap Finder'"
AG = "'AI Answer Gaps'"
CO = 'Competitors'

# Settings cell map
THR, WEAKGAP, ACTIVE = f'{S}!$B$5', f'{S}!$B$6', f'{S}!$B$7'
COMFY, EASEZERO, VOLFULL = f'{S}!$B$10', f'{S}!$B$11', f'{S}!$B$12'
WV, WE, WB, WP, WT = (f'{S}!$B${r}' for r in (15, 16, 17, 18, 19))
P1, P2 = f'{S}!$B$22', f'{S}!$B$23'
OPENPOS = f'{S}!$B$26'
CTR_RNG, CTR_BEYOND = f'{S}!$E$17:$E$26', f'{S}!$E$27'
PLAY_RNG = f'{S}!$D$11:$E$14'

# Demo: LedgerLeaf, a fictional invoicing and GST billing app for freelancers and small businesses in India.
# All competitors are fictional too. Volumes, difficulty and positions are illustrative, not real data.
SITES = [
    ('LedgerLeaf (you)', 'ledgerleaf.example', 'Your site', 'Our blog started in 2025. Strong on basics, thin on templates.'),
    ('BillNest', 'billnest.example', 'Business competitor', 'Big product with many feature pages and a help centre.'),
    ('InvoTrack', 'invotrack.example', 'Business competitor', 'Comparison and alternatives pages for every rival.'),
    ('TaxPal Guides', 'taxpalguides.example', 'Publisher or blog', 'Tax publisher. Deep GST rule explainers, updated often.'),
    ('FormFolio', 'formfolio.example', 'Template or marketplace site', 'Free downloadable formats in Excel and Word.'),
]
# keyword, topic, intent, volume, kd, value, you, c1, c2, c3, c4, aio
KW = [
    ('gst invoice format in excel', 'Templates', 'Transactional', 2400, 22, 3, None, 4, 7, 15, 2, 'No'),
    ('invoice generator for freelancers', 'Invoicing', 'Transactional', 1900, 45, 3, 14, 3, 6, None, None, 'No'),
    ('how to make an invoice', 'Invoicing', 'Informational', 6600, 48, 2, 9, 5, 12, 3, None, 'Yes'),
    ('proforma invoice meaning', 'Invoicing basics', 'Informational', 4400, 30, 1, None, None, 11, 4, None, 'Yes'),
    ('gst billing software for small business', 'Software', 'Commercial', 3600, 62, 3, None, 2, 5, None, None, 'No'),
    ('billnest alternatives', 'Software', 'Commercial', 390, 18, 3, None, None, 3, 9, None, 'No'),
    ('billnest login', 'Brand', 'Navigational', 2900, 10, 1, None, 1, None, None, None, 'No'),
    ('e invoice applicability limit', 'GST rules', 'Informational', 5400, 35, 2, 6, 8, 4, 2, None, 'Yes'),
    ('invoice vs bill difference', 'Invoicing basics', 'Informational', 1600, 20, 1, 2, 6, None, 4, 9, 'Yes'),
    ('freelancer invoice template', 'Templates', 'Transactional', 2900, 26, 3, 5, 8, None, None, 3, 'No'),
    ('recurring invoice software', 'Software', 'Commercial', 480, 33, 3, 4, None, None, None, None, 'No'),
    ('how to add gst to an invoice', 'GST rules', 'Informational', 1300, 24, 2, None, 6, None, 2, 8, 'Yes'),
    ('upi payment link for invoice', 'Payments', 'Transactional', 880, 19, 3, None, 3, 2, 7, 12, 'No'),
    ('payment reminder email template', 'Payments', 'Informational', 2400, 21, 2, 11, None, 4, None, 6, 'No'),
    ('hsn code list for services', 'GST rules', 'Informational', 8100, 52, 1, None, None, None, 1, None, 'Yes'),
    ('invoice number format', 'Invoicing basics', 'Informational', 1000, 15, 2, None, 7, 9, 5, 4, 'Yes'),
    ('credit note format under gst', 'Templates', 'Transactional', 1300, 28, 2, None, None, None, 6, 3, 'No'),
    ('invoicing app for small business india', 'Software', 'Commercial', 1000, 40, 3, 18, 2, 4, None, None, 'No'),
    ('how to get paid faster as a freelancer', 'Payments', 'Informational', 320, 12, 2, None, None, None, None, None, 'Yes'),
    ('tds on freelancer payments', 'GST rules', 'Informational', 1900, 38, 1, None, None, None, 3, None, 'Yes'),
    ('delivery challan format', 'Templates', 'Transactional', 3600, 25, 2, None, None, None, 9, 1, 'No'),
    ('invoice financing for msme', 'Payments', 'Commercial', 590, 47, 1, None, None, None, None, None, 'No'),
    ('quotation format in word', 'Templates', 'Transactional', 4400, 24, 2, 3, None, None, None, 1, 'No'),
    ('invotrack pricing', 'Brand', 'Navigational', 260, 8, 2, None, None, 1, None, None, 'No'),
    ('gst invoice rules for freelancers', 'GST rules', 'Informational', 720, 29, 3, 7, None, 5, 2, None, 'Yes'),
    ('multi currency invoice', 'Invoicing', 'Commercial', 210, 20, 3, None, 6, 11, None, None, 'No'),
    ('receipt vs invoice', 'Invoicing basics', 'Informational', 1300, 14, 1, 1, 4, None, 6, None, 'Yes'),
    ('export invoice format', 'Templates', 'Transactional', 1600, 30, 2, None, 10, None, 8, 5, 'No'),
]
URLS = {
    'invoice generator for freelancers': '/invoice-generator/',
    'how to make an invoice': '/blog/how-to-make-an-invoice/',
    'e invoice applicability limit': '/blog/e-invoicing-guide/',
    'invoice vs bill difference': '/blog/invoice-vs-bill/',
    'freelancer invoice template': '/templates/freelancer-invoice/',
    'recurring invoice software': '/features/recurring-invoices/',
    'payment reminder email template': '/blog/payment-reminder-emails/',
    'invoicing app for small business india': '/invoicing-app/',
    'quotation format in word': '/templates/quotation-format/',
    'gst invoice rules for freelancers': '/blog/gst-for-freelancers/',
    'receipt vs invoice': '/blog/receipt-vs-invoice/',
}
# prompt, topic, engine, date, shown, you mentioned, you cited, c1..c4 mentioned, most cited url
AI = [
    ('best invoicing app for freelancers in india', 'Software', 'ChatGPT', '2026-11-10', 'Yes', 'No', 'No', 'Yes', 'Yes', 'No', 'No', 'invotrack.example/compare/'),
    ('best invoicing app for freelancers in india', 'Software', 'Google AI Mode', '2026-11-10', 'Yes', 'Yes', 'No', 'Yes', 'Yes', 'No', 'No', 'billnest.example/'),
    ('gst invoice format in excel', 'Templates', 'Google AI Overview', '2026-11-10', 'Yes', 'No', 'No', 'No', 'No', 'Yes', 'Yes', 'formfolio.example/gst-invoice/'),
    ('how to make an invoice', 'Invoicing', 'Google AI Overview', '2026-11-10', 'Yes', 'Yes', 'Yes', 'Yes', 'No', 'Yes', 'No', 'taxpalguides.example/invoice-guide/'),
    ('e invoice applicability limit', 'GST rules', 'Google AI Overview', '2026-11-11', 'Yes', 'No', 'No', 'No', 'No', 'Yes', 'No', 'taxpalguides.example/e-invoice/'),
    ('e invoice applicability limit', 'GST rules', 'Perplexity', '2026-11-11', 'Yes', 'No', 'No', 'No', 'No', 'Yes', 'No', 'taxpalguides.example/e-invoice/'),
    ('billnest alternatives', 'Software', 'ChatGPT', '2026-11-11', 'Yes', 'Yes', 'No', 'Yes', 'Yes', 'No', 'No', 'invotrack.example/billnest-alternatives/'),
    ('how to get paid faster as a freelancer', 'Payments', 'Gemini', '2026-11-12', 'Yes', 'No', 'No', 'No', 'No', 'No', 'No', 'a freelancer forum thread'),
    ('upi payment link for invoice', 'Payments', 'Google AI Mode', '2026-11-12', 'Yes', 'No', 'No', 'Yes', 'Yes', 'No', 'No', 'billnest.example/upi-links/'),
    ('receipt vs invoice', 'Invoicing basics', 'Google AI Overview', '2026-11-12', 'Yes', 'Yes', 'Yes', 'No', 'No', 'Yes', 'No', 'ledgerleaf.example/blog/receipt-vs-invoice/'),
    ('freelancer invoice template', 'Templates', 'Google AI Overview', '2026-11-12', 'No', 'No', 'No', 'No', 'No', 'No', 'No', ''),
    ('gst invoice rules for freelancers', 'GST rules', 'Copilot', '2026-11-13', 'Yes', 'Yes', 'No', 'No', 'Yes', 'Yes', 'No', 'taxpalguides.example/freelancer-gst/'),
]
# keyword, decision, content type, target url, owner, due, status
PLAN = [
    ('gst invoice format in excel', 'Target', 'New page', '/templates/gst-invoice-format/', 'Meera', '2026-12-05', 'Brief'),
    ('upi payment link for invoice', 'Target', 'New page', '/features/upi-payment-links/', 'Dev', '2026-12-12', 'Not started'),
    ('invoice generator for freelancers', 'Target', 'Upgrade existing page', '/invoice-generator/', 'Dev', '2026-12-01', 'Writing'),
    ('how to make an invoice', 'Target', 'Upgrade existing page', '/blog/how-to-make-an-invoice/', 'Meera', '2026-12-15', 'Not started'),
    ('proforma invoice meaning', 'Monitor', 'Refresh', '', 'Meera', '', 'Not started'),
    ('billnest login', 'Skip', '', '', '', '', ''),
]

HEAD = ['Keyword', 'Topic', 'Search intent', 'Monthly volume', 'KD (0 to 100)', 'Business value (1 to 3)',
        'Your position', 'Your ranking URL', None, None, None, None, 'AI Overview shows?',
        'Competitors in top N', 'Best competitor position', 'Best competitor', 'Gap type', 'Positions to gain',
        'Opportunity score (0 to 100)', 'Priority', 'Recommended play', 'Your est. clicks now', 'Est. click upside',
        'Owner', 'Notes', 'Est. clicks C1', 'Est. clicks C2', 'Est. clicks C3', 'Est. clicks C4', 'Rank key (helper)']
FCOLS = tuple(range(14, 24)) + tuple(range(26, 31))
WIDTHS = [36, 16, 14, 10, 9, 10, 10, 34, 11, 11, 11, 11, 10, 11, 11, 16, 12, 10, 12, 9, 44, 10, 10, 10, 26, 9, 9, 9, 9, 10]
COMP_COLS = ['I', 'J', 'K', 'L']
EST_COLS = ['Z', 'AA', 'AB', 'AC']


def ctr(x):
    """Assumed CTR for a position cell or expression (blank or 0 = not ranking)."""
    return f'IF(N({x})<1,0,IF({x}<=10,INDEX({CTR_RNG},MAX(1,ROUND({x},0))),{CTR_BEYOND}))'


def gf(c):
    return f'{GF}!${c}${FIRST}:${c}${LAST}'


def ag(c):
    return f"{AG}!${c}${AI_FIRST}:${c}${AI_LAST}"


def settings_sheet(wb):
    ws = wb.create_sheet(S)
    ws.sheet_view.showGridLines = False
    K.title_block(ws, 'Settings', 'Every threshold, weight and list used by this workbook. Change a blue number and every score updates.')
    for c, w in zip('ABCDEFGHIJKLMN', [52, 14, 3, 26, 44, 3, 16, 22, 26, 22, 18, 14, 3, 3]):
        ws.column_dimensions[c].width = w
    rows = [
        (4, 'GAP RULES', None, None),
        (5, 'A site "ranks" when its position is at or above (top N)', 20, '0'),
        (6, 'Weak when the best competitor is at least this many positions ahead', 5, '0'),
        (7, 'Active competitors (auto, from the Competitors tab)', f'=COUNTA({CO}!$A$6:$A$9)', '0'),
        (9, 'YOUR SITE', None, None),
        (10, 'Comfortable keyword difficulty (auto from the site stage in E4)', '=VLOOKUP(E4,D5:E7,2,FALSE)', '0'),
        (11, 'Ease reaches zero this many KD points above comfortable', 40, '0'),
        (12, 'Volume that earns full volume points', 10000, '#,##0'),
        (14, 'OPPORTUNITY SCORE WEIGHTS (any numbers, they are scaled)', None, None),
        (15, 'Volume weight', 30, '0'),
        (16, 'Ease weight', 20, '0'),
        (17, 'Business value weight', 30, '0'),
        (18, 'Competitor proof weight (share of competitors ranking)', 20, '0'),
        (19, 'Total (auto)', '=SUM(B15:B18)', '0'),
        (21, 'PRIORITY', None, None),
        (22, 'P1 when opportunity score is at least', 85, '0'),
        (23, 'P2 when opportunity score is at least (below = P3)', 70, '0'),
        (25, 'UPSIDE ESTIMATE', None, None),
        (26, 'Target position for keywords no competitor ranks for', 5, '0'),
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
    ws['A29'] = ('All weights, thresholds and click through rates here are starter assumptions chosen for this kit, '
                 'not Google rules or published benchmarks. Replace the CTR table with your own Search Console average CTR by position when you can.')
    ws['A29'].font = K.f(9, False, '777777', True)
    ws['A29'].alignment = Alignment(wrap_text=True)
    ws.row_dimensions[29].height = 40
    # Site stage
    ws['D4'] = 'SITE STAGE'
    ws['D4'].font = K.f(10, True, K.DEEP)
    ws['E4'] = 'Growing site'
    ws['E4'].fill = K.INPUT_FILL
    ws['E4'].font = K.f(10, True)
    ws['E4'].border = K.BORDER
    for i, (k, v) in enumerate([('New site', 15), ('Growing site', 30), ('Established site', 50)]):
        ws.cell(row=5 + i, column=4, value=k).fill = K.INPUT_FILL
        c = ws.cell(row=5 + i, column=5, value=v)
        c.fill = K.INPUT_FILL
        c.font = K.f(10, False, '0000FF')
    # Intent to play
    ws['D10'] = 'NEW PAGE FORMAT BY INTENT'
    ws['D10'].font = K.f(10, True, K.DEEP)
    plays = [('Informational', 'page: a guide more useful than the top result'),
             ('Commercial', 'page: an honest comparison or best of list'),
             ('Transactional', 'page: a product, tool or template page'),
             ('Navigational', 'page only if it is your own brand term')]
    for i, (k, v) in enumerate(plays):
        ws.cell(row=11 + i, column=4, value=k).fill = K.INPUT_FILL
        ws.cell(row=11 + i, column=5, value=v).fill = K.INPUT_FILL
    # CTR table
    ws['D16'] = 'ASSUMED CTR BY POSITION (edit)'
    ws['D16'].font = K.f(10, True, K.DEEP)
    for i, v in enumerate([0.25, 0.15, 0.10, 0.07, 0.05, 0.04, 0.03, 0.025, 0.02, 0.015]):
        ws.cell(row=17 + i, column=4, value=f'Position {i + 1}')
        c = ws.cell(row=17 + i, column=5, value=v)
        c.number_format = '0.0%'
        c.fill = K.INPUT_FILL
        c.font = K.f(10, False, '0000FF')
    ws['D27'] = 'Position 11 to N'
    ws['E27'] = 0.005
    ws['E27'].number_format = '0.0%'
    ws['E27'].fill = K.INPUT_FILL
    ws['E27'].font = K.f(10, False, '0000FF')
    ws['G4'] = 'DROPDOWN LISTS'
    ws['G4'].font = K.f(10, True, K.DEEP)
    lists = {
        'G': ['Intent', 'Informational', 'Commercial', 'Transactional', 'Navigational'],
        'H': ['Site type', 'Your site', 'Business competitor', 'Publisher or blog', 'Template or marketplace site', 'Forum or community', 'Review or directory site', 'Other'],
        'I': ['AI engine', 'Google AI Overview', 'Google AI Mode', 'ChatGPT', 'Gemini', 'Perplexity', 'Copilot', 'Other'],
        'J': ['Yes/No', 'Yes', 'No'],
        'K': ['Decision', 'Target', 'Monitor', 'Skip'],
        'L': ['Content type', 'New page', 'Upgrade existing page', 'Refresh', 'Merge'],
        'M': ['Status', 'Not started', 'Brief', 'Writing', 'Published', 'Measuring'],
        'N': ['Site stage', 'New site', 'Growing site', 'Established site'],
    }
    for c, vals in lists.items():
        ws.column_dimensions[c].width = max(ws.column_dimensions[c].width or 0, 18)
        for i, v in enumerate(vals):
            cell = ws[f'{c}{5 + i}']
            cell.value = v
            cell.font = K.f(9, i == 0, '555555')
    K.dropdown(ws, 'E4', f'{S}!$N$6:$N$8')
    return ws


def competitors_sheet(wb):
    ws = wb.create_sheet(CO)
    ws.sheet_view.showGridLines = False
    K.title_block(ws, 'Competitors', 'Row 5 is your site. Rows 6 to 9 are up to 4 search competitors: the sites that rank for your keywords, not only the companies you sell against.')
    head = ['Site name', 'Domain', 'Site type', 'Why they win (your notes)', 'Keywords in top N', 'Keywords in top 3',
            'Est. monthly clicks', 'Est. share of clicks', 'Keywords where they beat you', 'Gap volume (they rank, you do not)',
            'AI answers mentioning them', 'AI mention rate']
    fc = tuple(range(5, 13))
    K.header_row(ws, 4, head, formula_cols=fc, widths=[22, 24, 24, 46, 11, 10, 11, 11, 12, 13, 12, 11])
    shown = f'COUNTIF({ag("E")},"Yes")'
    for i, site in enumerate(SITES):
        r = 5 + i
        for c, v in enumerate(site, 1):
            ws.cell(row=r, column=c, value=v)
        col = 'G' if i == 0 else COMP_COLS[i - 1]
        est = 'V' if i == 0 else EST_COLS[i - 1]
        rng = gf(col)
        ws.cell(row=r, column=5, value=f'=IF(A{r}="","",COUNTIFS({rng},">0",{rng},"<="&{THR}))')
        ws.cell(row=r, column=6, value=f'=IF(A{r}="","",COUNTIFS({rng},">0",{rng},"<=3"))')
        ws.cell(row=r, column=7, value=f'=IF(A{r}="","",SUM({gf(est)}))')
        tot = '+'.join(f'SUM({gf(c)})' for c in ['V'] + EST_COLS)
        ws.cell(row=r, column=8, value=f'=IF(A{r}="","",IFERROR(G{r}/({tot}),0))')
        g = gf('G')
        if i == 0:
            ws.cell(row=r, column=9, value='n/a')
            ws.cell(row=r, column=10, value='n/a')
            ws.cell(row=r, column=11, value=f'=IF(A{r}="","",COUNTIFS({ag("E")},"Yes",{ag("F")},"Yes"))')
        else:
            ws.cell(row=r, column=9, value=(f'=IF(A{r}="","",SUMPRODUCT(({rng}>0)*({rng}<={THR})*((({g}=0)+({g}>{rng}))>0)))'))
            ws.cell(row=r, column=10, value=(f'=IF(A{r}="","",SUMPRODUCT(({rng}>0)*({rng}<={THR})*((({g}=0)+({g}>{THR}))>0)*{gf("D")}))'))
            ws.cell(row=r, column=11, value=f'=IF(A{r}="","",COUNTIFS({ag("E")},"Yes",{ag(L(7 + i))},"Yes"))')
        ws.cell(row=r, column=12, value=f'=IF(A{r}="","",IFERROR(K{r}/{shown},0))')
    K.style_body(ws, 5, 9, len(head), formula_cols=fc, number_formats={7: '#,##0', 8: '0%', 10: '#,##0', 12: '0%'}, wrap_cols=(4,))
    for c in range(1, 5):
        ws.cell(row=5, column=c).font = K.f(10, True, K.DEEP)
    K.dropdown(ws, 'C5:C9', f'{S}!$H$6:$H$12')
    ws['A11'] = ('Est. clicks use the assumed CTR by position on Settings, so treat them as a way to compare sites, not as real traffic. '
                 'Gap volume is the monthly volume of keywords where this competitor ranks in the top N and you do not.')
    ws['A11'].font = K.f(9, False, '666666', True)
    ws.merge_cells('A11:L11')
    ws['A11'].alignment = Alignment(wrap_text=True)
    ws.row_dimensions[11].height = 30
    ws.conditional_formatting.add('H5:H9', ColorScaleRule(start_type='num', start_value=0, start_color='FFFFFF', end_type='max', end_color='9BE07A'))
    ws.freeze_panes = 'B5'
    return ws


def gap_sheet(wb):
    ws = wb.create_sheet('Gap Finder')
    ws.sheet_view.showGridLines = False
    K.title_block(ws, 'Gap finder', 'Rows 5 to 32 hold DEMO data for LedgerLeaf, a fictional invoicing app, and 4 fictional competitors (illustrative numbers). Select the yellow demo cells and press Delete to start your own. Grey formula columns stay.')
    ws['A2'].font = K.f(10, True, 'B45309')
    ws['A3'] = 'One row per keyword. Leave a position blank when the site does not rank in your keyword tool. Positions can be decimals (Search Console average position). 500 rows ready.'
    ws['A3'].font = K.f(9, False, '666666', True)
    K.header_row(ws, 4, [h or '' for h in HEAD], formula_cols=FCOLS, widths=WIDTHS)
    for j, c in enumerate(COMP_COLS):
        ws[f'{c}4'] = f'={CO}!A{6 + j}&" position"'
    for r in range(FIRST, LAST + 1):
        i = r - FIRST
        if i < len(KW):
            for c, v in zip([1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13], KW[i]):
                if v is not None:
                    ws.cell(row=r, column=c, value=v)
            if KW[i][0] in URLS:
                ws.cell(row=r, column=8, value=URLS[KW[i][0]])
        rngc = f'I{r}:L{r}'
        you_rank = f'AND(N(G{r})>0,N(G{r})<={THR})'
        ws.cell(row=r, column=14, value=f'=IF(A{r}="","",COUNTIFS({rngc},">0",{rngc},"<="&{THR}))')
        ws.cell(row=r, column=15, value=f'=IF(A{r}="","",IF(COUNT({rngc})=0,"",MIN({rngc})))')
        ws.cell(row=r, column=16, value=f'=IF(O{r}="","",INDEX({CO}!$A$6:$A$9,MATCH(O{r},{rngc},0)))')
        ws.cell(row=r, column=17, value=(
            f'=IF(A{r}="","",IF(NOT({you_rank}),IF(N{r}=0,"Open",IF(N{r}>={ACTIVE},"Missing","Untapped")),'
            f'IF(N{r}=0,"Unique",IF(G{r}<O{r},"Strong",IF(G{r}-O{r}>={WEAKGAP},"Weak","Shared")))))'))
        ws.cell(row=r, column=18, value=f'=IF(OR(Q{r}="Weak",Q{r}="Shared"),ROUND(G{r}-O{r},0),"")')
        ws.cell(row=r, column=19, value=(
            f'=IF(A{r}="","",ROUND(100*({WV}*MIN(1,LOG10(N(D{r})+1)/LOG10({VOLFULL}+1))'
            f'+{WE}*IF(N(E{r})<={COMFY},1,MAX(0,1-(N(E{r})-{COMFY})/{EASEZERO}))'
            f'+{WB}*N(F{r})/3+{WP}*N{r}/MAX(1,{ACTIVE}))/{WT},0))'))
        ws.cell(row=r, column=20, value=(
            f'=IF(A{r}="","",IF(OR(Q{r}="Strong",Q{r}="Unique"),"Defend",IF(N(F{r})<=1,"Monitor",IF(S{r}>={P1},"P1",IF(S{r}>={P2},"P2","P3")))))'))
        page = f'IF(H{r}="","your ranking page",H{r})'
        ws.cell(row=r, column=21, value=(
            f'=IF(A{r}="","",IF(Q{r}="Strong","Defend: keep it the best answer and refresh it",'
            f'IF(Q{r}="Unique","Protect and expand: only you rank here",'
            f'IF(N(F{r})<=1,"Monitor: low business value",'
            f'IF(Q{r}="Open","Validate demand first: no one in your set ranks",'
            f'IF(Q{r}="Weak","Upgrade "&{page}&" to close a gap of "&R{r}&" positions",'
            f'IF(Q{r}="Shared","Refresh "&{page}&" and add internal links",'
            f'IF(H{r}<>"","Rework "&H{r}&" for this keyword",'
            f'IF(C{r}="Navigational","Usually skip: people want another brand",'
            f'"New "&IFERROR(VLOOKUP(C{r},{PLAY_RNG},2,FALSE),"page"))))))))))'))
        ws.cell(row=r, column=22, value=f'=IF(A{r}="","",ROUND(N(D{r})*{ctr(f"G{r}")},0))')
        tgt = f'IF(O{r}="",{OPENPOS},MAX(1,MIN(10,O{r})))'
        ws.cell(row=r, column=23, value=(
            f'=IF(A{r}="","",IF(T{r}="Defend",0,MAX(0,ROUND(N(D{r})*{ctr(tgt)}-V{r},0))))'))
        for c, e in zip(COMP_COLS, EST_COLS):
            ws[f'{e}{r}'] = f'=IF(A{r}="","",ROUND(N(D{r})*{ctr(f"{c}{r}")},0))'
        ws[f'AD{r}'] = (f'=IF(OR(T{r}="P1",T{r}="P2",T{r}="P3"),IF(C{r}="Navigational","",S{r}+MIN(W{r},99999)/100000+(1000-ROW())/100000000),"")')
    K.style_body(ws, FIRST, LAST, len(HEAD), formula_cols=FCOLS,
                 number_formats={4: '#,##0', 7: '0.0', 9: '0.0', 10: '0.0', 11: '0.0', 12: '0.0', 15: '0.0', 19: '0', 22: '#,##0', 23: '#,##0', 30: '0.000'},
                 wrap_cols=(1, 21, 25))
    for c in COMP_COLS:
        ws[f'{c}4'].font = K.f(10, True, 'FFFFFF')
    ws.freeze_panes = 'B5'
    ws.auto_filter.ref = f'A4:{L(len(HEAD))}{LAST}'
    K.dropdown(ws, f'C{FIRST}:C{LAST}', f'{S}!$G$6:$G$9')
    K.dropdown(ws, f'F{FIRST}:F{LAST}', '"1,2,3"', '3 = close to a sale or lead, 2 = builds trust, 1 = loosely related')
    K.dropdown(ws, f'M{FIRST}:M{LAST}', f'{S}!$J$6:$J$7')
    K.whole_number(ws, f'E{FIRST}:E{LAST}', 0, 100, 'Keyword difficulty must be between 0 and 100.')
    q = f'Q{FIRST}:Q{LAST}'
    for val, fill, bold in [('Missing', 'F8D7D3', True), ('Untapped', 'FFE8B3', False), ('Weak', 'FCE4C4', True),
                            ('Shared', 'DCEBFF', False), ('Strong', 'D9F2C4', True), ('Unique', '9BE07A', True), ('Open', 'EFEFEF', False)]:
        ws.conditional_formatting.add(q, CellIsRule(operator='equal', formula=[f'"{val}"'], fill=PatternFill('solid', fgColor=fill), font=Font(name=K.FONT, bold=bold)))
    t = f'T{FIRST}:T{LAST}'
    ws.conditional_formatting.add(t, CellIsRule(operator='equal', formula=['"P1"'], fill=PatternFill('solid', fgColor='9BE07A'), font=Font(name=K.FONT, bold=True)))
    ws.conditional_formatting.add(t, CellIsRule(operator='equal', formula=['"P2"'], fill=PatternFill('solid', fgColor='D9F2C4')))
    ws.conditional_formatting.add(t, CellIsRule(operator='equal', formula=['"P3"'], fill=PatternFill('solid', fgColor='FFE8B3')))
    ws.conditional_formatting.add(t, CellIsRule(operator='equal', formula=['"Defend"'], fill=PatternFill('solid', fgColor='DCEBFF')))
    ws.conditional_formatting.add(t, CellIsRule(operator='equal', formula=['"Monitor"'], font=Font(name=K.FONT, color='888888', italic=True)))
    ws.conditional_formatting.add(f'S{FIRST}:S{LAST}', ColorScaleRule(start_type='num', start_value=0, start_color='F8D7D3', mid_type='num', mid_value=60, mid_color='FFF4CC', end_type='num', end_value=100, end_color='B7E4A0'))
    ws.conditional_formatting.add(f'G{FIRST}:L{LAST}', CellIsRule(operator='between', formula=['1', '3'], font=Font(name=K.FONT, bold=True, color=K.DEEP)))
    ws.conditional_formatting.add(f'U{FIRST}:U{LAST}', FormulaRule(formula=[f'LEFT(U{FIRST},7)="Monitor"'], font=Font(name=K.FONT, color='888888', italic=True)))
    return ws


def ai_sheet(wb):
    ws = wb.create_sheet('AI Answer Gaps')
    ws.sheet_view.showGridLines = False
    K.title_block(ws, 'AI answer gaps', 'Ask your key questions in AI Overviews, AI Mode and AI assistants. Record who is mentioned and who is linked. Answers change often, so date every check.')
    head = ['Prompt or query', 'Topic', 'AI engine', 'Date checked', 'AI answer shown?', 'You mentioned?', 'You linked or cited?',
            None, None, None, None, 'Most cited source', 'Competitors mentioned', 'Status', 'Next step', 'Notes']
    fc = (13, 14, 15)
    K.header_row(ws, 4, [h or '' for h in head], formula_cols=fc, widths=[40, 16, 18, 12, 10, 11, 11, 11, 11, 11, 11, 34, 12, 20, 50, 24])
    for j in range(4):
        ws.cell(row=4, column=8 + j, value=f'={CO}!A{6 + j}&" mentioned?"').font = K.f(10, True, 'FFFFFF')
    import datetime
    for r in range(AI_FIRST, AI_LAST + 1):
        i = r - AI_FIRST
        if i < len(AI):
            for c, v in enumerate(AI[i], 1):
                if v:
                    ws.cell(row=r, column=c, value=datetime.date.fromisoformat(v) if c == 4 else v)
        ws.cell(row=r, column=13, value=f'=IF(A{r}="","",COUNTIF(H{r}:K{r},"Yes"))')
        ws.cell(row=r, column=14, value=(
            f'=IF(A{r}="","",IF(E{r}<>"Yes","No AI answer",IF(G{r}="Yes","Cited",IF(F{r}="Yes","Mentioned, not linked",'
            f'IF(M{r}>0,"Competitor only","Nobody in your set")))))'))
        ws.cell(row=r, column=15, value=(
            f'=IF(N{r}="","",IF(N{r}="Cited","Keep the cited page accurate, current and easy to quote",'
            f'IF(N{r}="Mentioned, not linked","Make your page the clearest, most complete source for this answer",'
            f'IF(N{r}="Competitor only","Study the cited page, then publish a more useful first hand answer",'
            f'IF(N{r}="Nobody in your set","Open topic: publish a clear answer page and build mentions","Track it as a classic search keyword")))))'))
    K.style_body(ws, AI_FIRST, AI_LAST, len(head), formula_cols=fc, number_formats={4: 'dd mmm yyyy'}, wrap_cols=(1, 12, 15, 16))
    K.dropdown(ws, f'C{AI_FIRST}:C{AI_LAST}', f'{S}!$I$6:$I$12')
    K.dropdown(ws, f'E{AI_FIRST}:K{AI_LAST}', f'{S}!$J$6:$J$7')
    n = f'N{AI_FIRST}:N{AI_LAST}'
    ws.conditional_formatting.add(n, CellIsRule(operator='equal', formula=['"Cited"'], fill=PatternFill('solid', fgColor='9BE07A'), font=Font(name=K.FONT, bold=True)))
    ws.conditional_formatting.add(n, CellIsRule(operator='equal', formula=['"Mentioned, not linked"'], fill=PatternFill('solid', fgColor='D9F2C4')))
    ws.conditional_formatting.add(n, CellIsRule(operator='equal', formula=['"Competitor only"'], fill=PatternFill('solid', fgColor='F8D7D3'), font=Font(name=K.FONT, bold=True, color='9B2C1F')))
    ws.conditional_formatting.add(n, CellIsRule(operator='equal', formula=['"Nobody in your set"'], fill=PatternFill('solid', fgColor='FFE8B3')))
    ws.freeze_panes = 'B5'
    ws.auto_filter.ref = f'A4:P{AI_LAST}'
    return ws


def plan_sheet(wb):
    ws = wb.create_sheet('Action Plan')
    ws.sheet_view.showGridLines = False
    K.title_block(ws, 'Action plan', 'Your target queue. Pick a keyword from the Gap Finder, decide Target, Monitor or Skip, and give every target an owner and a date. Grey columns pull the facts from the Gap Finder.')
    head = ['Keyword', 'Decision', 'Content type', 'Target URL', 'Owner', 'Due date', 'Status',
            'Gap type', 'Opportunity score', 'Priority', 'Best competitor', 'Est. click upside', 'Recommended play', 'Check', 'Notes']
    fc = tuple(range(8, 15))
    K.header_row(ws, 4, head, formula_cols=fc, widths=[36, 11, 20, 32, 10, 12, 12, 11, 11, 9, 16, 11, 44, 26, 24])
    import datetime
    for r in range(AP_FIRST, AP_LAST + 1):
        i = r - AP_FIRST
        if i < len(PLAN):
            for c, v in enumerate(PLAN[i], 1):
                if v:
                    ws.cell(row=r, column=c, value=datetime.date.fromisoformat(v) if c == 6 else v)
        lk = lambda col: f'IFERROR(INDEX({gf(col)},MATCH($A{r},{gf("A")},0)),"")'
        ws.cell(row=r, column=8, value=f'=IF(A{r}="","",IFERROR(INDEX({gf("Q")},MATCH($A{r},{gf("A")},0)),"Not in Gap Finder"))')
        ws.cell(row=r, column=9, value=f'=IF(A{r}="","",{lk("S")})')
        ws.cell(row=r, column=10, value=f'=IF(A{r}="","",{lk("T")})')
        ws.cell(row=r, column=11, value=f'=IF(A{r}="","",{lk("P")})')
        ws.cell(row=r, column=12, value=f'=IF(A{r}="","",{lk("W")})')
        ws.cell(row=r, column=13, value=f'=IF(A{r}="","",{lk("U")})')
        ws.cell(row=r, column=14, value=(
            f'=IF(A{r}="","",IF(H{r}="Not in Gap Finder","Add the keyword to the Gap Finder",IF(B{r}<>"Target","",'
            f'IF(OR(E{r}="",F{r}=""),"Add an owner and a due date",IF(AND(F{r}<TODAY(),G{r}<>"Published",G{r}<>"Measuring"),"Overdue","On track")))))'))
    K.style_body(ws, AP_FIRST, AP_LAST, len(head), formula_cols=fc, number_formats={6: 'dd mmm yyyy', 9: '0', 12: '#,##0'}, wrap_cols=(13, 15))
    K.dropdown(ws, f'A{AP_FIRST}:A{AP_LAST}', gf('A'), 'Pick a keyword from the Gap Finder')
    K.dropdown(ws, f'B{AP_FIRST}:B{AP_LAST}', f'{S}!$K$6:$K$8')
    K.dropdown(ws, f'C{AP_FIRST}:C{AP_LAST}', f'{S}!$L$6:$L$9')
    K.dropdown(ws, f'G{AP_FIRST}:G{AP_LAST}', f'{S}!$M$6:$M$10')
    b = f'B{AP_FIRST}:B{AP_LAST}'
    ws.conditional_formatting.add(b, CellIsRule(operator='equal', formula=['"Target"'], fill=PatternFill('solid', fgColor='9BE07A'), font=Font(name=K.FONT, bold=True)))
    ws.conditional_formatting.add(b, CellIsRule(operator='equal', formula=['"Skip"'], font=Font(name=K.FONT, color='888888', italic=True)))
    nn = f'N{AP_FIRST}:N{AP_LAST}'
    ws.conditional_formatting.add(nn, CellIsRule(operator='equal', formula=['"Overdue"'], fill=PatternFill('solid', fgColor='F8D7D3'), font=Font(name=K.FONT, bold=True, color='9B2C1F')))
    ws.conditional_formatting.add(nn, CellIsRule(operator='equal', formula=['"On track"'], fill=PatternFill('solid', fgColor='D9F2C4')))
    ws.freeze_panes = 'B5'
    return ws


GAP_TYPES = ['Missing', 'Untapped', 'Weak', 'Shared', 'Strong', 'Unique', 'Open']


def dashboard_sheet(wb):
    ws = wb.create_sheet('Dashboard')
    ws.sheet_view.showGridLines = False
    K.title_block(ws, 'Dashboard', 'Everything here calculates from the other tabs. Nothing to type.')
    for c, w in zip('ABCDEFGHIJK', [40, 12, 3, 20, 10, 12, 12, 3, 3, 3, 3]):
        ws.column_dimensions[c].width = w
    kpis = [
        ('Keywords analysed', f'=COUNTA({gf("A")})', '0'),                                   # B5
        ('Missing (every competitor ranks, you do not)', f'=COUNTIF({gf("Q")},"Missing")', '0'),  # B6
        ('Untapped (some competitors rank, you do not)', f'=COUNTIF({gf("Q")},"Untapped")', '0'),  # B7
        ('Weak (you trail by many positions)', f'=COUNTIF({gf("Q")},"Weak")', '0'),             # B8
        ('Strong or unique (defend)', f'=COUNTIF({gf("Q")},"Strong")+COUNTIF({gf("Q")},"Unique")', '0'),  # B9
        ('P1 opportunities', f'=COUNTIF({gf("T")},"P1")', '0'),                                  # B10
        ('Est. monthly click upside (P1 and P2)', f'=SUMIF({gf("T")},"P1",{gf("W")})+SUMIF({gf("T")},"P2",{gf("W")})', '#,##0'),  # B11
        ('Your est. share of clicks', f'={CO}!H5', '0%'),                                       # B12
        ('AI answers checked (answer shown)', f'=COUNTIF({ag("E")},"Yes")', '0'),              # B13
        ('AI answers that cite you', f'=COUNTIF({ag("N")},"Cited")', '0'),                      # B14
        ('AI answers where only competitors appear', f'=COUNTIF({ag("N")},"Competitor only")', '0'),  # B15
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
    # gap type table
    for j, h in enumerate(['Gap type', 'Keywords', 'Volume', 'Click upside']):
        c = ws.cell(row=4, column=4 + j, value=h)
        c.font = K.f(10, True, 'FFFFFF')
        c.fill = K.HEAD_F
    for i, gt in enumerate(GAP_TYPES):
        r = 5 + i
        ws.cell(row=r, column=4, value=gt)
        ws.cell(row=r, column=5, value=f'=COUNTIF({gf("Q")},D{r})')
        ws.cell(row=r, column=6, value=f'=SUMIF({gf("Q")},D{r},{gf("D")})').number_format = '#,##0'
        ws.cell(row=r, column=7, value=f'=SUMIF({gf("Q")},D{r},{gf("W")})').number_format = '#,##0'
        for cc in (4, 5, 6, 7):
            ws.cell(row=r, column=cc).border = K.BORDER
            ws.cell(row=r, column=cc).font = K.f(10)
    # share of clicks table
    for j, h in enumerate(['Site', 'Share of clicks']):
        c = ws.cell(row=13, column=4 + j, value=h)
        c.font = K.f(10, True, 'FFFFFF')
        c.fill = K.HEAD_F
    for i in range(5):
        r = 14 + i
        ws.cell(row=r, column=4, value=f'=IF({CO}!A{5 + i}="","",{CO}!A{5 + i})')
        ws.cell(row=r, column=5, value=f'=IF({CO}!A{5 + i}="",0,{CO}!H{5 + i})').number_format = '0%'
        for cc in (4, 5):
            ws.cell(row=r, column=cc).border = K.BORDER
            ws.cell(row=r, column=cc).font = K.f(10)
    # Top 10
    top = 22
    ws.cell(row=top - 1, column=1, value='TOP 10 OPPORTUNITIES (P1 to P3, not navigational, sorted by score then upside)').font = K.f(10, True, K.DEEP)
    K.header_row(ws, top, ['Keyword', 'Score', None, 'Gap type', 'Priority', 'Upside', 'Best competitor'], formula_cols=tuple(range(1, 8)))
    ws.cell(row=top, column=3).fill = PatternFill(fill_type=None)
    ws.column_dimensions['G'].width = 16
    for k in range(1, 11):
        r = top + k
        m = f'MATCH(LARGE({gf("AD")},{k}),{gf("AD")},0)'
        cells = {1: f'=IFERROR(INDEX({gf("A")},{m}),"")', 2: f'=IFERROR(INDEX({gf("S")},{m}),"")',
                 4: f'=IFERROR(INDEX({gf("Q")},{m}),"")', 5: f'=IFERROR(INDEX({gf("T")},{m}),"")',
                 6: f'=IFERROR(INDEX({gf("W")},{m}),"")', 7: f'=IFERROR(INDEX({gf("P")},{m}),"")'}
        for cc, fm in cells.items():
            c = ws.cell(row=r, column=cc, value=fm)
            c.border = K.BORDER
            c.font = K.f(10, cc == 1)
            c.fill = K.FORMULA_FILL
            if cc == 6:
                c.number_format = '#,##0'

    def bar(title, ytitle, cat_col, val_col, r1, r2, anchor, color, horiz=False):
        ch = BarChart()
        ch.type = 'bar' if horiz else 'col'
        ch.title = title
        ch.y_axis.title = ytitle
        ch.add_data(Reference(ws, min_col=val_col, min_row=r1, max_row=r2), titles_from_data=False)
        ch.set_categories(Reference(ws, min_col=cat_col, min_row=r1, max_row=r2))
        ch.legend = None
        ch.height, ch.width = 7, 15
        ch.roundedCorners = False
        ch.x_axis.delete = False
        ch.y_axis.delete = False
        ch.title.overlay = False
        ch.y_axis.title.overlay = False
        ch.series[0].graphicalProperties.solidFill = color
        ws.add_chart(ch, anchor)
        return ch
    bar('Keywords by gap type', 'Keywords', 4, 5, 5, 11, 'I4', K.GREEN)
    c2 = bar('Estimated share of clicks by site', 'Share', 4, 5, 14, 18, 'I20', '2B2B2B', horiz=True)
    c2.y_axis.number_format = '0%'
    return ws


def build(path, asset, url):
    wb = K.new_book()
    gap_sheet(wb)
    competitors_sheet(wb)
    dashboard_sheet(wb)
    ai_sheet(wb)
    plan_sheet(wb)
    settings_sheet(wb)
    K.prompts_sheet(wb, asset['prompts'], url)
    K.checklist_sheet(wb, list(asset['checklist']))
    K.sources_sheet(wb, asset['sources'], [
        ('Demo data', 'LedgerLeaf and all 4 competitors are fictional. Every volume, difficulty score, position and AI answer in the demo is illustrative, not real data.', ''),
        ('Gap types', 'Missing, Weak, Strong, Untapped, Unique and Shared follow the common keyword gap categories used by tools such as Semrush Keyword Gap, adapted to a top N ranking threshold you set. Open is added for keywords nobody in your set ranks for.', ''),
        ('Opportunity score', 'Weighted mix of volume (log scaled), ease (difficulty compared with what your site stage can win), business value and competitor proof (share of competitors ranking). Weights live on Settings and are assumptions to tune.', ''),
        ('Assumed CTR by position', 'Starter numbers chosen for this kit so that estimated clicks and share of clicks can be compared between sites. They are not a published benchmark. Replace them with your own Search Console average CTR by position.', ''),
        ('AI answer checks', 'AI answers vary by user, location, wording and date. Record what you saw, date it and recheck monthly. Google says AI Overviews and AI Mode may show a wider and more diverse set of links than classic results.', ''),
    ])
    K.start_here(
        wb, 'Competitor Gaps Kit',
        [
            'This workbook finds the keywords and AI answers your search competitors win and you do not, sorts every keyword into a gap type, scores the opportunity, estimates the click upside and writes the next play.',
            'It ships with demo data for a fictional invoicing app and 4 fictional competitors (28 keywords, 12 AI answer checks, 6 planned actions) so you can see every formula working. Clear the yellow demo cells when you are ready.',
        ],
        [
            ('Gap Finder', 'One row per keyword with 500 ready rows: your position and up to 4 competitor positions, plus automatic gap type, opportunity score, priority, play and click upside.'),
            ('Competitors', 'Your site and up to 4 competitors with keywords in the top N, estimated share of clicks, gap volume and AI answer mentions.'),
            ('Dashboard', 'Key numbers, gap type table, share of clicks, a top 10 opportunity list and two charts.'),
            ('AI Answer Gaps', 'Prompts checked in AI Overviews, AI Mode and AI assistants: who is mentioned, who is cited and what to do next.'),
            ('Action Plan', 'The target queue: decision, content type, owner, due date and status, with facts pulled from the Gap Finder.'),
            ('Settings', 'Ranking threshold, weak gap, site stage, score weights, priority bands, assumed CTR by position and dropdown lists.'),
            ('AI Prompts', 'Prompts for ChatGPT, Claude or Gemini to find competitors, explain gaps, plan pages and test AI answers.'),
            ('Checklist', 'The full process as a tick list with automatic progress.'),
            ('Sources', 'Where facts come from and which numbers are assumptions.'),
        ],
        [
            'Look at the demo rows and the Dashboard to see how it works, then clear the yellow demo cells.',
            'On Competitors, add your site in row 5 and up to 4 search competitors in rows 6 to 9.',
            'Export the ranking keywords for each site from one SEO tool and paste keyword, volume, difficulty and each position into the Gap Finder.',
            'Give each keyword an intent and a business value from 1 to 3. Mark whether an AI Overview shows.',
            'Check your 10 to 30 most important questions in AI Overviews, AI Mode and AI assistants, and log them on AI Answer Gaps.',
            'Read the Dashboard top 10, then move the best gaps to the Action Plan with an owner and a date.',
            'Publish or upgrade the pages, then refresh positions and AI checks every month.',
        ],
        url,
    )
    order = ['Start Here', 'Gap Finder', 'Competitors', 'Dashboard', 'AI Answer Gaps', 'Action Plan', 'Settings', 'AI Prompts', 'Checklist', 'Sources']
    wb._sheets = [wb[n] for n in order]
    wb.active = 0
    for ws in wb.worksheets:
        ws.sheet_properties.tabColor = K.GREEN if ws.title in ('Start Here', 'Gap Finder', 'Competitors', 'Dashboard') else 'A6EF39'
    wb.save(path)


PREVIEW = {'sheet': 'Gap Finder', 'header_row': 4, 'rows': 10, 'cols': [1, 4, 5, 7, 9, 10, 11, 12, 17, 19, 20, 21],
           'formula_idx': [8, 9, 10, 11]}


def check(wb):
    """Assert the worked examples used in the guide."""
    g = wb['Gap Finder']
    # Example 1: gst invoice format in excel (row 5) is Missing, P1
    assert g['N5'].value == 4 and g['O5'].value == 2 and g['P5'].value == 'FormFolio', (g['N5'].value, g['O5'].value, g['P5'].value)
    assert g['Q5'].value == 'Missing', g['Q5'].value
    assert g['S5'].value == 95 and g['T5'].value == 'P1', (g['S5'].value, g['T5'].value)
    assert g['W5'].value == 360, g['W5'].value
    assert g['U5'].value == 'New page: a product, tool or template page', g['U5'].value
    # Example 2: invoice generator for freelancers (row 6) is Weak, P2
    assert g['Q6'].value == 'Weak' and g['R6'].value == 11, (g['Q6'].value, g['R6'].value)
    assert g['S6'].value == 77 and g['T6'].value == 'P2', (g['S6'].value, g['T6'].value)
    assert g['V6'].value == 10 and g['W6'].value == 180, (g['V6'].value, g['W6'].value)
    # Other gap types in the demo
    assert g['Q12'].value == 'Shared' and g['Q13'].value == 'Strong' and g['Q15'].value == 'Unique', (g['Q12'].value, g['Q13'].value, g['Q15'].value)
    assert g['Q23'].value == 'Open' and g['Q8'].value == 'Untapped', (g['Q23'].value, g['Q8'].value)
    assert g['U11'].value == 'Monitor: low business value' and g['T11'].value == 'Monitor', g['U11'].value
    assert g['U6'].value == 'Upgrade /invoice-generator/ to close a gap of 11 positions', g['U6'].value
    assert abs(c_share := wb['Competitors']['H5'].value - 0.118) < 0.001, wb['Competitors']['H5'].value
    assert g['U28'].value == 'Usually skip: people want another brand', g['U28'].value
    c = wb['Competitors']
    assert c['E5'].value == 11, c['E5'].value
    d = wb['Dashboard']
    assert d['B5'].value == len(KW), d['B5'].value
    assert d['A23'].value == 'gst invoice format in excel', d['A23'].value
    a = wb['AI Answer Gaps']
    assert a['N5'].value == 'Competitor only' and a['N6'].value == 'Mentioned, not linked' and a['N8'].value == 'Cited', (a['N5'].value, a['N6'].value, a['N8'].value)
    assert a['N15'].value == 'No AI answer' and a['N12'].value == 'Nobody in your set', (a['N15'].value, a['N12'].value)
