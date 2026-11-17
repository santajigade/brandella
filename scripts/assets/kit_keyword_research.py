"""Keyword Research Kit workbook (asset 01)."""
from openpyxl.styles import Alignment, PatternFill
from openpyxl.formatting.rule import CellIsRule, ColorScaleRule, FormulaRule
from openpyxl.chart import BarChart, Reference
from openpyxl.styles import Font
import kitlib as K

FIRST, LAST = 5, 504  # Keywords data rows
PM_FIRST, PM_LAST = 5, 154

# Demo data: InvoiceEase, a fictional invoicing app for freelancers and small businesses in India.
# Numbers are illustrative only.
# kw, cluster, intent, funnel, vol, kd, cpc, trend, aio, serp, value, rank, cur_url, target, owner, status
DEMO = [
    ('invoice template for freelancers', 'Invoice templates', 'Commercial', 'Consider', 2400, 28, 0.6, 'Stable', 'No', 'Images, People Also Ask', 3, 14, '/templates/freelance-invoice/', '/templates/freelance-invoice/', 'Asha', 'In progress'),
    ('free invoice template word', 'Invoice templates', 'Transactional', 'Decision', 5400, 41, 0.4, 'Stable', 'No', 'Images', 3, None, '', '/templates/invoice-word/', 'Asha', 'Planned'),
    ('invoice format in excel', 'Invoice templates', 'Transactional', 'Decision', 6600, 35, 0.3, 'Rising', 'No', 'Images, Video', 3, 22, '/templates/excel-invoice/', '/templates/excel-invoice/', 'Asha', 'In progress'),
    ('simple invoice format', 'Invoice templates', 'Transactional', 'Decision', 3600, 30, 0.3, 'Stable', 'No', 'Images', 2, None, '', '/templates/simple-invoice/', 'Asha', 'Planned'),
    ('proforma invoice format', 'Invoice templates', 'Informational', 'Awareness', 4400, 26, 0.5, 'Stable', 'Yes', 'AI Overview, People Also Ask', 2, 9, '/guides/proforma-invoice/', '/guides/proforma-invoice/', 'Ravi', 'Live'),
    ('invoice template for consultants', 'Invoice templates', 'Commercial', 'Consider', 720, 18, 0.7, 'Rising', 'No', 'People Also Ask', 3, None, '', '/templates/freelance-invoice/', 'Asha', 'Planned'),
    ('gst invoice format', 'GST invoicing', 'Informational', 'Awareness', 9900, 45, 0.6, 'Stable', 'Yes', 'AI Overview, People Also Ask, Images', 3, 31, '/guides/gst-invoice/', '/guides/gst-invoice/', 'Ravi', 'Rework'),
    ('what is e invoicing under gst', 'GST invoicing', 'Informational', 'Awareness', 2900, 38, 0.8, 'Rising', 'Yes', 'AI Overview, People Also Ask, Video', 2, None, '', '/guides/e-invoicing-gst/', 'Ravi', 'Planned'),
    ('gst invoice rules for freelancers', 'GST invoicing', 'Informational', 'Awareness', 880, 22, 0.9, 'Rising', 'Yes', 'AI Overview, People Also Ask', 3, None, '', '/guides/gst-invoice/', 'Ravi', 'Planned'),
    ('hsn code for software services', 'GST invoicing', 'Informational', 'Awareness', 1900, 25, 0.4, 'Stable', 'Yes', 'AI Overview', 1, None, '', '', '', 'Skip'),
    ('gst invoice generator online', 'GST invoicing', 'Transactional', 'Decision', 1300, 33, 1.2, 'Rising', 'No', 'Ads', 3, 18, '/tools/gst-invoice-generator/', '/tools/gst-invoice-generator/', 'Meera', 'Optimize'),
    ('tax invoice vs bill of supply', 'GST invoicing', 'Informational', 'Awareness', 1000, 20, 0.3, 'Stable', 'Yes', 'AI Overview, Featured snippet', 2, 6, '/guides/tax-invoice-vs-bill-of-supply/', '/guides/tax-invoice-vs-bill-of-supply/', 'Ravi', 'Live'),
    ('best invoicing software for small business', 'Invoicing software', 'Commercial', 'Consider', 3600, 62, 4.5, 'Stable', 'Yes', 'AI Overview, Ads, People Also Ask', 3, None, '', '/compare/best-invoicing-software/', 'Meera', 'Planned'),
    ('invoicing software for freelancers', 'Invoicing software', 'Commercial', 'Consider', 1600, 48, 3.8, 'Rising', 'No', 'Ads, People Also Ask', 3, 12, '/freelancers/', '/freelancers/', 'Meera', 'Optimize'),
    ('free invoicing app', 'Invoicing software', 'Transactional', 'Decision', 2400, 52, 2.9, 'Rising', 'No', 'Ads, App pack', 3, None, '', '/', 'Meera', 'Planned'),
    ('invoicing app alternatives', 'Invoicing software', 'Commercial', 'Consider', 390, 21, 3.2, 'Stable', 'No', 'People Also Ask', 3, None, '', '/compare/invoicing-app-alternatives/', 'Meera', 'Planned'),
    ('invoicing software with gst', 'Invoicing software', 'Commercial', 'Consider', 1000, 44, 3.5, 'Stable', 'No', 'Ads', 3, 25, '/features/gst/', '/features/gst/', 'Meera', 'Rework'),
    ('recurring invoice software', 'Invoicing software', 'Commercial', 'Consider', 590, 29, 4.1, 'Stable', 'No', 'People Also Ask', 3, None, '', '/features/recurring-invoices/', 'Meera', 'Planned'),
    ('how to write an invoice', 'Getting paid', 'Informational', 'Awareness', 8100, 47, 0.5, 'Stable', 'Yes', 'AI Overview, Video, People Also Ask', 2, 15, '/guides/how-to-write-an-invoice/', '/guides/how-to-write-an-invoice/', 'Ravi', 'Optimize'),
    ('payment reminder email template', 'Getting paid', 'Informational', 'Consider', 2900, 24, 0.6, 'Stable', 'Yes', 'AI Overview, People Also Ask', 2, 4, '/templates/payment-reminder-email/', '/templates/payment-reminder-email/', 'Asha', 'Live'),
    ('how to ask for payment politely', 'Getting paid', 'Informational', 'Awareness', 1300, 15, 0.2, 'Rising', 'Yes', 'AI Overview, People Also Ask', 2, None, '', '/templates/payment-reminder-email/', 'Asha', 'Planned'),
    ('late payment fee clause', 'Getting paid', 'Informational', 'Awareness', 720, 19, 0.7, 'Stable', 'Yes', 'AI Overview', 2, None, '', '/guides/late-payment-fees/', 'Ravi', 'Planned'),
    ('upi payment link for invoice', 'Getting paid', 'Transactional', 'Decision', 1600, 27, 1.1, 'Rising', 'No', 'People Also Ask', 3, None, '', '/features/upi-payments/', 'Meera', 'Planned'),
    ('what is net 30 payment terms', 'Getting paid', 'Informational', 'Awareness', 1900, 23, 0.4, 'Stable', 'Yes', 'AI Overview, Featured snippet', 1, 11, '/guides/payment-terms/', '/guides/payment-terms/', 'Ravi', 'Optimize'),
    ('how to track freelance income', 'Freelancer finance', 'Informational', 'Awareness', 590, 16, 0.6, 'Rising', 'Yes', 'AI Overview, People Also Ask', 2, None, '', '/guides/track-freelance-income/', 'Ravi', 'Planned'),
    ('freelancer tax calculator india', 'Freelancer finance', 'Transactional', 'Decision', 1300, 31, 0.9, 'Rising', 'No', 'Tools', 2, None, '', '/tools/freelancer-tax-calculator/', 'Meera', 'Planned'),
    ('expense tracker for freelancers', 'Freelancer finance', 'Commercial', 'Consider', 880, 36, 2.2, 'Stable', 'No', 'Ads, App pack', 2, 28, '/features/expenses/', '/features/expenses/', 'Meera', 'Rework'),
    ('how much to charge as a freelancer', 'Freelancer finance', 'Informational', 'Awareness', 2400, 34, 0.5, 'Stable', 'Yes', 'AI Overview, People Also Ask, Discussions', 1, None, '', '', '', 'Skip'),
    ('invoiceease login', 'Brand', 'Navigational', 'Retention', 260, 2, 0, 'Stable', 'No', 'Sitelinks', 1, 1, '/login/', '/login/', 'Meera', 'Live'),
    ('freelance invoice checklist', 'Getting paid', 'Informational', 'Awareness', 320, 10, 0.4, 'Stable', 'Yes', 'AI Overview', 2, None, '', '/guides/how-to-write-an-invoice/', 'Ravi', 'Planned'),
]
CLUSTERS = ['Invoice templates', 'GST invoicing', 'Invoicing software', 'Getting paid', 'Freelancer finance', 'Brand']

HEAD = ['Keyword', 'Cluster or Topic', 'Search Intent', 'Funnel Stage', 'Monthly Volume', 'KD (0 to 100)', 'CPC', 'Trend',
        'AI Overview on SERP?', 'Other SERP Features', 'Business Value (1 to 3)', 'Current Rank', 'Current URL',
        'Opportunity Score (0 to 100)', 'Priority', 'Est. Monthly Clicks', 'Recommended Action', 'AI Search Angle',
        'Target URL', 'Keywords on Target URL', 'Duplicate Check', 'Owner', 'Status', 'Notes']
FCOLS = (14, 15, 16, 17, 18, 20, 21)
WIDTHS = [34, 20, 15, 13, 12, 10, 8, 10, 12, 26, 12, 10, 30, 14, 10, 12, 26, 34, 32, 12, 15, 10, 12, 30]

S = 'Settings'


def settings_sheet(wb):
    ws = wb.create_sheet(S)
    ws.sheet_view.showGridLines = False
    K.title_block(ws, 'Settings', 'Change these to fit your site. Every score and estimate in the workbook updates by itself.')
    for col, w in zip('ABCDEFGHIJKLMNOP', [40, 18, 3, 26, 12, 3, 14, 12, 3, 16, 14, 12, 14, 8, 18, 18]):
        ws.column_dimensions[col].width = w
    rows = [
        (4, 'YOUR SITE', None, None),
        (5, 'Site stage', 'Growing site', None),
        (6, 'Comfortable keyword difficulty (auto)', '=VLOOKUP(B5,D5:E7,2,FALSE)', None),
        (7, 'Volume that earns full volume points', 50000, '#,##0'),
        (8, 'Target position for click estimate', 3, '0'),
        (9, 'Click loss when an AI Overview shows', 0.4, '0%'),
        (10, 'Ease reaches zero this many KD points above comfortable', 40, '0'),
        (11, 'SCORE WEIGHTS (any numbers, they are scaled)', None, None),
        (12, 'Volume weight', 30, '0'),
        (13, 'Ease weight (difficulty vs your site)', 25, '0'),
        (14, 'Business value weight', 30, '0'),
        (15, 'Intent fit weight', 15, '0'),
        (16, 'Total weight (auto)', '=SUM(B12:B15)', '0'),
        (18, 'PRIORITY THRESHOLDS', None, None),
        (19, 'P1 when score is at least', 85, '0'),
        (20, 'P2 when score is at least', 70, '0'),
        (21, 'P3 when score is at least', 55, '0'),
    ]
    for r, label, val, fmt in rows:
        a = ws.cell(row=r, column=1, value=label)
        a.font = K.f(10, val is None, K.DEEP if val is None else K.INK)
        if val is not None:
            c = ws.cell(row=r, column=2, value=val)
            c.font = K.f(10, True)
            c.border = K.BORDER
            c.fill = K.FORMULA_FILL if isinstance(val, str) and val.startswith('=') else K.INPUT_FILL
            if fmt:
                c.number_format = fmt
    ws['B9'].comment = None
    # Lookup tables
    ws['D4'] = 'COMFORTABLE KD BY SITE STAGE'
    ws['D4'].font = K.f(10, True, K.DEEP)
    for i, (k, v) in enumerate([('New site', 15), ('Growing site', 30), ('Established site', 50)]):
        ws.cell(row=5 + i, column=4, value=k).fill = K.INPUT_FILL
        ws.cell(row=5 + i, column=5, value=v).fill = K.INPUT_FILL
    ws['D10'] = 'INTENT FIT (0 to 1)'
    ws['D10'].font = K.f(10, True, K.DEEP)
    for i, (k, v) in enumerate([('Transactional', 1), ('Commercial', 0.9), ('Informational', 0.6), ('Navigational', 0.2)]):
        ws.cell(row=11 + i, column=4, value=k).fill = K.INPUT_FILL
        c = ws.cell(row=11 + i, column=5, value=v)
        c.fill = K.INPUT_FILL
        c.number_format = '0.0'
    ws['G4'] = 'CTR BY POSITION (starter)'
    ws['G4'].font = K.f(10, True, K.DEEP)
    ctr = [0.28, 0.15, 0.10, 0.07, 0.05, 0.04, 0.03, 0.025, 0.02, 0.018, 0.012, 0.011, 0.01, 0.009, 0.008, 0.007, 0.007, 0.006, 0.006, 0.005]
    for i, v in enumerate(ctr):
        ws.cell(row=5 + i, column=7, value=i + 1).fill = K.INPUT_FILL
        c = ws.cell(row=5 + i, column=8, value=v)
        c.fill = K.INPUT_FILL
        c.number_format = '0.0%'
    ws['G26'] = 'Starter assumptions only, not a benchmark.'
    ws['G27'] = 'Replace them with your own average CTR by'
    ws['G28'] = 'position from Search Console.'
    for c in ('G26', 'G27', 'G28'):
        ws[c].font = K.f(9, False, '777777', True)
    # Dropdown lists
    ws['J4'] = 'DROPDOWN LISTS'
    ws['J4'].font = K.f(10, True, K.DEEP)
    lists = {
        'J': ['Intent', 'Transactional', 'Commercial', 'Informational', 'Navigational'],
        'K': ['Funnel', 'Awareness', 'Consider', 'Decision', 'Retention'],
        'L': ['Trend', 'Rising', 'Stable', 'Falling'],
        'M': ['Status', 'Planned', 'In progress', 'Live', 'Optimize', 'Rework', 'Skip'],
        'N': ['Yes/No', 'Yes', 'No'],
        'O': ['Content type', 'Guide', 'Template', 'Tool', 'Comparison', 'Landing page', 'Feature page', 'Product page'],
        'P': ['Site stage', 'New site', 'Growing site', 'Established site'],
    }
    for col, vals in lists.items():
        for i, v in enumerate(vals):
            c = ws[f'{col}{5 + i}']
            c.value = v
            c.font = K.f(9, i == 0, '555555')
    K.dropdown(ws, 'B5', f"{S}!$P$6:$P$8")
    for r in (5, 7, 8, 9, 10, 12, 13, 14, 15, 19, 20, 21):
        ws.cell(row=r, column=2).font = K.f(10, True, '0000FF')
    return ws


def keywords_sheet(wb):
    ws = wb.create_sheet('Keywords')
    ws.sheet_view.showGridLines = False
    K.title_block(ws, 'Keyword research sheet', 'Rows 5 to 34 hold DEMO data for InvoiceEase, a fictional invoicing app (illustrative numbers). Select the yellow cells in those rows and press Delete to start your own list. Grey formula columns stay.')
    ws['A2'].font = K.f(10, True, 'B45309')
    ws['A3'] = 'Yellow = you type. Grey with green header = calculates by itself. 500 rows ready. Tune scoring on the Settings tab.'
    ws['A3'].font = K.f(9, False, '666666', True)
    K.header_row(ws, 4, HEAD, formula_cols=FCOLS, widths=WIDTHS)
    for r in range(FIRST, LAST + 1):
        i = r - FIRST
        if i < len(DEMO):
            d = DEMO[i]
            vals = {1: d[0], 2: d[1], 3: d[2], 4: d[3], 5: d[4], 6: d[5], 7: d[6], 8: d[7], 9: d[8], 10: d[9], 11: d[10],
                    12: d[11], 13: d[12] or None, 19: d[13] or None, 22: d[14] or None, 23: d[15]}
            for col, v in vals.items():
                if v is not None and v != '':
                    ws.cell(row=r, column=col, value=v)
        ws.cell(row=r, column=14, value=(
            f'=IF(A{r}="","",ROUND(MIN(100,100*({S}!$B$12*MIN(1,LOG10(N(E{r})+1)/LOG10({S}!$B$7+1))'
            f'+{S}!$B$13*IF(N(F{r})<={S}!$B$6,1,MAX(0,1-(N(F{r})-{S}!$B$6)/{S}!$B$10))'
            f'+{S}!$B$14*N(K{r})/3'
            f'+{S}!$B$15*IFERROR(VLOOKUP(C{r},{S}!$D$11:$E$14,2,FALSE),0.5))/{S}!$B$16'
            f'*IF(H{r}="Rising",1.05,IF(H{r}="Falling",0.95,1))),0))'))
        ws.cell(row=r, column=15, value=f'=IF(N{r}="","",IF(N{r}>={S}!$B$19,"P1",IF(N{r}>={S}!$B$20,"P2",IF(N{r}>={S}!$B$21,"P3","Skip"))))')
        ws.cell(row=r, column=16, value=f'=IF(A{r}="","",ROUND(N(E{r})*IFERROR(VLOOKUP({S}!$B$8,{S}!$G$5:$H$24,2,FALSE),0)*IF(I{r}="Yes",1-{S}!$B$9,1),0))')
        ws.cell(row=r, column=17, value=f'=IF(A{r}="","",IF(L{r}="","Create new page",IF(L{r}<=3,"Protect and refresh",IF(L{r}<=10,"Optimize to reach top 3",IF(L{r}<=20,"Improve page two ranking","Rework page or create new")))))')
        ws.cell(row=r, column=18, value=f'=IF(A{r}="","",IF(I{r}="Yes","Answer first block plus FAQ, aim to be cited",IF(C{r}="Informational","Clear definition and steps, easy to quote",IF(C{r}="Navigational","Brand page, no new content needed","Strong offer page with proof and comparisons"))))')
        ws.cell(row=r, column=20, value=f'=IF(S{r}="","",COUNTIF($S${FIRST}:$S${LAST},S{r}))')
        ws.cell(row=r, column=21, value=f'=IF(A{r}="","",IF(COUNTIF($A${FIRST}:$A${LAST},A{r})>1,"Duplicate keyword","OK"))')
    K.style_body(ws, FIRST, LAST, len(HEAD), formula_cols=FCOLS,
                 number_formats={5: '#,##0', 7: '0.00', 14: '0', 16: '#,##0'}, wrap_cols=(10, 17, 18, 24))
    ws.freeze_panes = 'B5'
    ws.auto_filter.ref = f'A4:X{LAST}'
    K.dropdown(ws, f'C{FIRST}:C{LAST}', f'{S}!$J$6:$J$9', 'Transactional, Commercial, Informational or Navigational')
    K.dropdown(ws, f'D{FIRST}:D{LAST}', f'{S}!$K$6:$K$9')
    K.dropdown(ws, f'H{FIRST}:H{LAST}', f'{S}!$L$6:$L$8')
    K.dropdown(ws, f'I{FIRST}:I{LAST}', f'{S}!$N$6:$N$7', 'Search the keyword. Is there an AI Overview at the top?')
    K.dropdown(ws, f'K{FIRST}:K{LAST}', '"1,2,3"', '3 = close to a sale or lead, 2 = builds trust, 1 = loosely related')
    K.dropdown(ws, f'W{FIRST}:W{LAST}', f'{S}!$M$6:$M$11')
    K.whole_number(ws, f'F{FIRST}:F{LAST}', 0, 100, 'Keyword difficulty must be between 0 and 100.')
    K.whole_number(ws, f'L{FIRST}:L{LAST}', 1, 200, 'Use the rank number, or leave blank if not ranking.')
    rng = f'O{FIRST}:O{LAST}'
    ws.conditional_formatting.add(rng, CellIsRule(operator='equal', formula=['"P1"'], fill=PatternFill('solid', fgColor='9BE07A'), font=Font(name=K.FONT, bold=True)))
    ws.conditional_formatting.add(rng, CellIsRule(operator='equal', formula=['"P2"'], fill=PatternFill('solid', fgColor='D9F2C4')))
    ws.conditional_formatting.add(rng, CellIsRule(operator='equal', formula=['"P3"'], fill=PatternFill('solid', fgColor='FFE8B3')))
    ws.conditional_formatting.add(rng, CellIsRule(operator='equal', formula=['"Skip"'], fill=PatternFill('solid', fgColor='E5E5E5')))
    ws.conditional_formatting.add(f'N{FIRST}:N{LAST}', ColorScaleRule(start_type='num', start_value=0, start_color='F8D7D3', mid_type='num', mid_value=50, mid_color='FFF4CC', end_type='num', end_value=100, end_color='B7E4A0'))
    ws.conditional_formatting.add(f'I{FIRST}:I{LAST}', CellIsRule(operator='equal', formula=['"Yes"'], fill=PatternFill('solid', fgColor='DCEBFF')))
    ws.conditional_formatting.add(f'U{FIRST}:U{LAST}', CellIsRule(operator='equal', formula=['"Duplicate keyword"'], font=Font(name=K.FONT, bold=True, color='C0392B')))
    return ws


def dashboard_sheet(wb):
    ws = wb.create_sheet('Dashboard')
    ws.sheet_view.showGridLines = False
    K.title_block(ws, 'Dashboard', 'Everything here calculates from the Keywords tab. Type your cluster names in the yellow cells of the cluster table.')
    for col, w in zip('ABCDEFGH', [36, 14, 3, 30, 12, 14, 14, 36]):
        ws.column_dimensions[col].width = w
    R = f'Keywords!$A${FIRST}:$A${LAST}'
    col = lambda c: f'Keywords!${c}${FIRST}:${c}${LAST}'
    kpis = [
        ('Keywords tracked', f'=COUNTA({R})', '0'),
        ('Total monthly search volume', f'=SUM({col("E")})', '#,##0'),
        ('Est. monthly clicks at target position', f'=SUM({col("P")})', '#,##0'),
        ('P1 keywords', f'=COUNTIF({col("O")},"P1")', '0'),
        ('P2 keywords', f'=COUNTIF({col("O")},"P2")', '0'),
        ('P3 keywords', f'=COUNTIF({col("O")},"P3")', '0'),
        ('Skip', f'=COUNTIF({col("O")},"Skip")', '0'),
        ('Keywords with an AI Overview', f'=COUNTIF({col("I")},"Yes")', '0'),
        ('Share with an AI Overview', '=IFERROR(B12/B5,0)', '0%'),
        ('Not ranking yet', f'=SUMPRODUCT(({R}<>"")*({col("L")}=""))', '0'),
        ('Ranking 1 to 3', f'=COUNTIFS({col("L")},">=1",{col("L")},"<=3")', '0'),
        ('Ranking 4 to 10', f'=COUNTIFS({col("L")},">=4",{col("L")},"<=10")', '0'),
        ('Ranking 11 to 20', f'=COUNTIFS({col("L")},">=11",{col("L")},"<=20")', '0'),
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
    # Intent table
    for cc, h in zip(range(4, 8), ['Search intent', 'Keywords', 'Volume', 'Est. clicks']):
        c = ws.cell(row=4, column=cc, value=h)
        c.font = K.f(10, True, 'FFFFFF')
        c.fill = K.HEAD_F
    for i, it in enumerate(['Transactional', 'Commercial', 'Informational', 'Navigational']):
        r = 5 + i
        ws.cell(row=r, column=4, value=it)
        ws.cell(row=r, column=5, value=f'=COUNTIF({col("C")},D{r})')
        ws.cell(row=r, column=6, value=f'=SUMIF({col("C")},D{r},{col("E")})').number_format = '#,##0'
        ws.cell(row=r, column=7, value=f'=SUMIF({col("C")},D{r},{col("P")})').number_format = '#,##0'
        for cc in range(4, 8):
            ws.cell(row=r, column=cc).border = K.BORDER
            ws.cell(row=r, column=cc).font = K.f(10)
    # Action table
    ws['D11'] = 'Recommended action'
    ws['E11'] = 'Keywords'
    for c in ('D11', 'E11'):
        ws[c].font = K.f(10, True, 'FFFFFF')
        ws[c].fill = K.HEAD_F
    for i, a in enumerate(['Create new page', 'Protect and refresh', 'Optimize to reach top 3', 'Improve page two ranking', 'Rework page or create new']):
        r = 12 + i
        ws.cell(row=r, column=4, value=a).font = K.f(10)
        ws.cell(row=r, column=5, value=f'=COUNTIF({col("Q")},D{r})').font = K.f(10)
        ws.cell(row=r, column=4).border = K.BORDER
        ws.cell(row=r, column=5).border = K.BORDER
    # Cluster table
    top = 20
    K.header_row(ws, top, ['Cluster (type names)', 'Keywords', None, 'Volume', 'Est. clicks', 'Avg score', 'P1 keywords', 'Top keyword by score'], formula_cols=(2, 4, 5, 6, 7, 8))
    ws.cell(row=top, column=3).fill = PatternFill(fill_type=None)
    for i in range(20):
        r = top + 1 + i
        a = ws.cell(row=r, column=1, value=CLUSTERS[i] if i < len(CLUSTERS) else None)
        a.fill = K.INPUT_FILL
        ws.cell(row=r, column=2, value=f'=IF(A{r}="","",COUNTIF({col("B")},A{r}))')
        ws.cell(row=r, column=4, value=f'=IF(A{r}="","",SUMIF({col("B")},A{r},{col("E")}))').number_format = '#,##0'
        ws.cell(row=r, column=5, value=f'=IF(A{r}="","",SUMIF({col("B")},A{r},{col("P")}))').number_format = '#,##0'
        ws.cell(row=r, column=6, value=f'=IF(A{r}="","",IFERROR(AVERAGEIF({col("B")},A{r},{col("N")}),""))').number_format = '0'
        ws.cell(row=r, column=7, value=f'=IF(A{r}="","",COUNTIFS({col("B")},A{r},{col("O")},"P1"))')
        ws.cell(row=r, column=8, value=(
            f'=IF(A{r}="","",IFERROR(INDEX(Keywords!$A$1:$A${LAST},SUMPRODUCT(MAX(({col("B")}=A{r})*'
            f'({col("N")}=_xlfn.MAXIFS({col("N")},{col("B")},A{r}))*ROW({col("B")})))),""))'))
        for cc in range(1, 9):
            if cc == 3:
                continue
            c = ws.cell(row=r, column=cc)
            c.border = K.BORDER
            c.font = K.f(10)
            if cc > 1:
                c.fill = K.FORMULA_FILL
    # Chart: keywords by priority
    ch = BarChart()
    ch.type = 'col'
    ch.title = 'Keywords by priority'
    ch.y_axis.title = 'Keywords'
    ch.add_data(Reference(ws, min_col=2, min_row=8, max_row=11), titles_from_data=False)
    ch.set_categories(Reference(ws, min_col=1, min_row=8, max_row=11))
    ch.legend = None
    ch.height, ch.width = 7, 12
    ch.roundedCorners = False
    ch.x_axis.delete = False
    ch.y_axis.delete = False
    ch.title.overlay = False
    ch.y_axis.title.overlay = False
    ch.series[0].graphicalProperties.solidFill = K.GREEN
    ws.add_chart(ch, 'J4')
    return ws


def page_map_sheet(wb):
    ws = wb.create_sheet('Page Map')
    ws.sheet_view.showGridLines = False
    K.title_block(ws, 'Page map', 'One row per page. The grey columns pull totals from the Keywords tab using the Target URL. DEMO rows are for the fictional InvoiceEase.')
    head = ['Target URL', 'Page Title', 'Primary Keyword', 'Content Type', 'Keywords Mapped', 'Combined Volume', 'Est. Monthly Clicks', 'Best Opportunity Score', 'Status', 'Publish or Update Date', 'Notes']
    fc = (5, 6, 7, 8)
    K.header_row(ws, 4, head, formula_cols=fc, widths=[36, 40, 34, 14, 11, 12, 12, 13, 12, 14, 30])
    pages = {}
    for d in DEMO:
        if d[13]:
            pages.setdefault(d[13], []).append(d)
    ctype = lambda u: ('Template' if '/templates/' in u else 'Guide' if '/guides/' in u else 'Tool' if '/tools/' in u else
                       'Comparison' if '/compare/' in u else 'Feature page' if '/features/' in u else 'Product page' if 'login' in u else 'Landing page')
    rows = []
    for url, ks in pages.items():
        prim = max(ks, key=lambda x: x[4])
        small = {'for', 'in', 'to', 'of', 'a', 'an', 'as', 'vs', 'with', 'under', 'and'}
        acr = {'gst': 'GST', 'upi': 'UPI', 'hsn': 'HSN'}
        words = prim[0].split()
        title = ' '.join(acr.get(w, w if (i and w in small) else w.capitalize()) for i, w in enumerate(words))
        rows.append((url, title, prim[0], ctype(url), prim[15]))
    for r in range(PM_FIRST, PM_LAST + 1):
        i = r - PM_FIRST
        if i < len(rows):
            for col, v in zip((1, 2, 3, 4, 9), rows[i]):
                ws.cell(row=r, column=col, value=v)
        ws.cell(row=r, column=5, value=f'=IF(A{r}="","",COUNTIF(Keywords!$S${FIRST}:$S${LAST},A{r}))')
        ws.cell(row=r, column=6, value=f'=IF(A{r}="","",SUMIF(Keywords!$S${FIRST}:$S${LAST},A{r},Keywords!$E${FIRST}:$E${LAST}))')
        ws.cell(row=r, column=7, value=f'=IF(A{r}="","",SUMIF(Keywords!$S${FIRST}:$S${LAST},A{r},Keywords!$P${FIRST}:$P${LAST}))')
        ws.cell(row=r, column=8, value=f'=IF(A{r}="","",_xlfn.MAXIFS(Keywords!$N${FIRST}:$N${LAST},Keywords!$S${FIRST}:$S${LAST},A{r}))')
    K.style_body(ws, PM_FIRST, PM_LAST, len(head), formula_cols=fc, number_formats={6: '#,##0', 7: '#,##0', 8: '0', 10: 'dd mmm yyyy'})
    K.dropdown(ws, f'D{PM_FIRST}:D{PM_LAST}', f'{S}!$O$6:$O$12')
    K.dropdown(ws, f'I{PM_FIRST}:I{PM_LAST}', f'{S}!$M$6:$M$11')
    ws.freeze_panes = 'B5'
    ws.auto_filter.ref = f'A4:K{PM_LAST}'
    return ws


def build(path, asset, url):
    wb = K.new_book()
    keywords_sheet(wb)
    dashboard_sheet(wb)
    page_map_sheet(wb)
    settings_sheet(wb)
    K.prompts_sheet(wb, asset['prompts'], url)
    K.checklist_sheet(wb, [c for c in asset['checklist']])
    K.sources_sheet(wb, asset['sources'], [
        ('Demo data', 'Rows 5 to 34 of Keywords and the demo rows of Page Map describe InvoiceEase, a fictional company. All volumes, difficulty scores, CPCs and ranks are illustrative, not real data.', ''),
        ('CTR by position (Settings)', 'Starter assumptions only. Replace with your own average CTR by position from the Google Search Console Performance report.', ''),
        ('Click loss with an AI Overview (Settings, default 40%)', 'An editable assumption. Public studies report very different drops depending on method and sample, so pick a value that matches your own Search Console data.', ''),
        ('Opportunity Score', 'Weighted mix of volume (log scaled), ease (difficulty compared with what your site stage can win), business value and intent fit, adjusted 5% up for rising and 5% down for falling trends. Weights live on Settings.', ''),
    ])
    K.start_here(
        wb, 'Keyword Research Kit',
        [
            'This workbook turns a raw keyword list into a ranked, page by page plan. Paste keywords, choose a few dropdowns, and it scores every keyword, estimates clicks, flags AI Overviews and tells you what to do next.',
            'It ships with 30 rows of demo data for a fictional invoicing app so you can see every formula and the dashboard working. Clear the yellow demo cells when you are ready.',
        ],
        [
            ('Keywords', 'Your master list with 500 ready rows: intent, funnel, volume, difficulty, AI Overview check, business value, rank, plus automatic score, priority, click estimate, action and AI search angle.'),
            ('Dashboard', 'Key numbers, intent and action summaries, a cluster table and a priority chart, all calculated from Keywords.'),
            ('Page Map', 'One row per page so every keyword has a home and no two pages compete.'),
            ('Settings', 'Your site stage, score weights, priority thresholds, CTR curve and dropdown lists.'),
            ('AI Prompts', 'Prompts for ChatGPT, Claude or Gemini to expand, classify, cluster and check keywords.'),
            ('Checklist', 'The full process as a tick list with automatic progress.'),
            ('Sources', 'Where facts come from and which numbers are assumptions.'),
        ],
        [
            'Open Settings and choose your site stage. Leave the weights as they are for your first run.',
            'Look at the demo rows on Keywords and the Dashboard to see how it works, then clear the yellow demo cells.',
            'Paste your seed and expanded keywords into column A. Add volume, difficulty and CPC from one data source.',
            'Choose intent, funnel stage, trend, AI Overview (search the keyword to check) and business value for each row.',
            'Add your current rank and URL from Search Console where you already rank.',
            'Sort or filter by Opportunity Score and Priority. Give every keyword you will target a Target URL.',
            'Fill the Page Map with one row per page, then work through the Recommended Action column.',
        ],
        url,
    )
    order = ['Start Here', 'Keywords', 'Dashboard', 'Page Map', 'Settings', 'AI Prompts', 'Checklist', 'Sources']
    wb._sheets = [wb[n] for n in order]
    wb.active = 0
    for ws in wb.worksheets:
        ws.sheet_properties.tabColor = K.GREEN if ws.title in ('Start Here', 'Keywords', 'Dashboard') else 'A6EF39'
    wb.save(path)


PREVIEW = {'sheet': 'Keywords', 'header_row': 4, 'rows': 10, 'cols': [1, 3, 5, 6, 9, 11, 12, 14, 15, 16, 17], 'formula_idx': [7, 8, 9, 10]}


def check(wb):
    """Sanity checks on recalculated values (fail the build if the logic breaks)."""
    ws = wb['Keywords']
    assert ws['N5'].value == 90, ws['N5'].value          # worked example in the guide
    assert ws['O5'].value == 'P1'
    assert ws['Q5'].value == 'Improve page two ranking'
    d = wb['Dashboard']
    assert d['B5'].value == len(DEMO)
    pm = wb['Page Map']
    assert pm['E5'].value >= 1
