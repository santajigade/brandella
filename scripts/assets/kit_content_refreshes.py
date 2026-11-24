"""Content Refresh Kit workbook (asset 15).

Content Inventory: one row per URL with Search Console clicks, impressions and position for a previous and a recent
period, plus dates, business value, time sensitivity and AI Overview checks (500 rows). The sheet works out the
changes, CTR, months since the last real update and whether a review is due, then diagnoses each page (ranking decay,
CTR decay, CTR decay under an AI Overview, demand decay, mixed decay, low traffic, growing, stable), suggests a
refresh type and action, flags URLs that share a main query, scores each page 0 to 100, sets a priority and estimates
hours and clicks recovered (labelled assumptions).
Refresh Queue: plan refreshes by week against writing hours, write a brief, apply the date rule and measure results
28 days later. Refresh Playbook explains each diagnosis. Dashboard sums it all up.
"""
import datetime
from openpyxl.styles import PatternFill, Font, Alignment
from openpyxl.formatting.rule import CellIsRule, ColorScaleRule, FormulaRule
from openpyxl.chart import BarChart, Reference
from openpyxl.utils import get_column_letter as L
import kitlib as K

CI_FIRST, CI_LAST = 5, 504     # Content Inventory (500 rows)
RQ_FIRST, RQ_LAST = 5, 104     # Refresh Queue (100 rows)
S = 'Settings'
CIS = "'Content Inventory'"
RQS = "'Refresh Queue'"

(DATE, PREV, RECENT, LOW, GROW, DECAY, IMPDROP, IMPSTAB, POSLOSS, FULL, P1, P2, P3, HOURS, MEASURE) = (f'{S}!$B${r}' for r in range(5, 20))
W_LOST, W_VALUE, W_POS, W_DUE = (f'{S}!$G${r}' for r in range(6, 10))
POS_RNG = f'{S}!$F$13:$G$17'
FRESH_RNG = f'{S}!$F$21:$G$23'
TYPE_RNG = f'{S}!$J$6:$N$14'

WEIGHTS = [('Clicks lost', 40), ('Business value', 25), ('Position band', 20), ('Review due', 15)]
POSBANDS = [(0, 0.5, 'Positions 1 to 3: protect'), (3.5, 1, 'Positions 4 to 10: most to gain'), (10.5, 0.8, 'Page two'),
            (20.5, 0.4, 'Positions 21 to 50'), (50.5, 0.1, 'Beyond 50')]
FRESH = [('Fast changing', 6), ('Yearly', 12), ('Evergreen', 24)]
# diagnosis, refresh type, hours, recovery share (assumption), what to do
TYPES = [
    ('Ranking decay', 'Full refresh', 6, 0.5, 'Full refresh: check today\'s top results, update facts, add missing subtopics and original examples, refresh internal links'),
    ('CTR decay', 'Snippet refresh', 1, 0.3, 'Snippet refresh: rewrite the title and meta description to match the intent better; check the visible date'),
    ('CTR decay (AI Overview)', 'Answer refresh', 3, 0.35, 'Answer refresh: put a clear 40 to 60 word answer near the top, add unique data and experience, tidy headings and FAQ'),
    ('Demand decay', 'Light refresh', 2, 0.15, 'Light refresh: update facts before the next season; check Google Trends and compare year over year'),
    ('Mixed decay', 'Diagnose queries', 1, 0, 'Diagnose: compare queries for this URL in Search Console to find which ones lost clicks'),
    ('Low traffic', 'Merge or improve', 4, 0.4, 'Review: merge into a stronger page with a 301, improve it, or leave it if it serves visitors'),
    ('Growing', 'Protect', 1, 0, 'Protect: leave the structure alone; fix facts only if they changed'),
    ('Stable', 'Monitor', 0, 0, 'Monitor: no action this cycle'),
    ('Stable, review due', 'Fact check', 1, 0, 'Fact check: confirm facts, prices and links; change the date only if the update is substantial'),
]
CTYPES = ['Guide', 'How to', 'List', 'Comparison', 'Review', 'Template or tool', 'Glossary', 'News or trends', 'Landing page']
SENS = ['Fast changing', 'Yearly', 'Evergreen']
YNC = ['Yes', 'No', 'Not checked']
OWNERS = ['Asha (writer)', 'Rahul (writer)', 'SEO', 'Editor', 'Product team']
WEEKS = [f'Week {i}' for i in range(1, 9)]

# Demo: Roamly, a fictional travel planning app with a blog (roamly.example). All numbers are illustrative.
U = 'https://roamly.example'
# url, title, type, topic, main query, published, updated, cP, cR, iP, iR, posP, posR, conv, value, sens, aio, cited, owner, notes
PAGES = [
    ('/blog/schengen-visa-checklist/', 'Schengen visa checklist for Indian travellers', 'Guide', 'Visas', 'schengen visa checklist', '2024-03-10', '2025-01-15', 4200, 2300, 98000, 61000, 3.2, 7.8, 46, 3, 'Fast changing', 'Yes', 'No', 'Asha (writer)', 'Worked example in the guide'),
    ('/blog/best-time-to-visit-bali/', 'Best time to visit Bali, month by month', 'Guide', 'Destinations', 'best time to visit bali', '2023-07-01', '2024-08-01', 3100, 1700, 120000, 118000, 4.1, 4.3, 12, 2, 'Yearly', 'Yes', 'No', 'Rahul (writer)', ''),
    ('/blog/travel-insurance-explained/', 'Travel insurance explained', 'Guide', 'Insurance', 'travel insurance explained', '2024-05-01', '2026-02-01', 2600, 2750, 54000, 57000, 5.0, 4.7, 31, 3, 'Yearly', 'Yes', 'Yes', 'Asha (writer)', ''),
    ('/blog/how-to-plan-a-road-trip/', 'How to plan a road trip in 9 steps', 'How to', 'Planning', 'road trip planning', '2022-11-01', '2023-06-10', 1900, 1150, 76000, 52000, 6.5, 6.9, 20, 2, 'Evergreen', 'No', 'Not checked', 'Rahul (writer)', ''),
    ('/blog/packing-list-for-ladakh/', 'Packing list for Ladakh', 'List', 'Destinations', 'ladakh packing list', '2024-04-01', '2026-09-15', 1400, 600, 40000, 22000, 4.4, 9.6, 3, 2, 'Yearly', 'No', 'No', 'Rahul (writer)', 'Refreshed in September, see Refresh Queue'),
    ('/blog/cheap-flights-tips/', '21 tips to find cheap flights', 'List', 'Flights', 'cheap flights tips', '2023-01-10', '2024-01-10', 2200, 1500, 150000, 146000, 7.2, 7.5, 9, 2, 'Yearly', 'Yes', 'No', 'Asha (writer)', ''),
    ('/blog/roamly-vs-tripit/', 'Roamly vs TripIt: which trip planner is better?', 'Comparison', 'Product', 'roamly vs tripit', '2025-02-01', '2025-02-01', 900, 820, 9800, 9500, 2.1, 2.4, 54, 3, 'Yearly', 'No', 'Not checked', 'Product team', 'Competitor changed pricing in 2026'),
    ('/blog/kerala-itinerary-7-days/', 'Kerala itinerary for 7 days', 'Guide', 'Destinations', 'kerala itinerary 7 days', '2024-09-01', '2024-09-01', 800, 1050, 21000, 28000, 8.1, 6.2, 6, 2, 'Yearly', 'No', 'No', 'Rahul (writer)', ''),
    ('/blog/what-is-visa-on-arrival/', 'What is visa on arrival?', 'Glossary', 'Visas', 'what is visa on arrival', '2023-05-01', '2023-05-01', 60, 35, 3000, 2500, 18.0, 22.0, 0, 1, 'Evergreen', 'Yes', 'No', 'SEO', ''),
    ('/blog/digital-nomad-visa-countries/', 'Digital nomad visa countries', 'List', 'Visas', 'digital nomad visa countries', '2024-01-15', '2024-07-01', 2800, 1300, 88000, 70000, 4.8, 8.9, 15, 3, 'Fast changing', 'Yes', 'No', 'Asha (writer)', ''),
    ('/blog/japan-rail-pass-guide/', 'Japan Rail Pass guide', 'Guide', 'Destinations', 'japan rail pass', '2023-08-10', '2025-09-01', 1600, 1250, 39000, 38000, 3.9, 4.1, 8, 2, 'Yearly', 'No', 'Not checked', 'Rahul (writer)', 'Title rewritten on 10 Nov, see Refresh Queue'),
    ('/blog/group-trip-budget-template/', 'Group trip budget template', 'Template or tool', 'Planning', 'group trip budget template', '2024-06-01', '2025-11-01', 1200, 1350, 18000, 19500, 3.0, 2.8, 88, 3, 'Evergreen', 'No', 'Not checked', 'Product team', ''),
    ('/blog/solo-travel-safety-tips/', 'Solo travel safety tips', 'List', 'Planning', 'solo travel safety tips', '2022-03-01', '2023-02-01', 1300, 1000, 45000, 41000, 6.0, 7.1, 4, 1, 'Evergreen', 'Not checked', 'Not checked', 'Asha (writer)', ''),
    ('/blog/goa-vs-pondicherry/', 'Goa vs Pondicherry for a long weekend', 'Comparison', 'Destinations', 'goa vs pondicherry', '2024-02-01', '2024-02-01', 700, 300, 15000, 9000, 5.5, 11.2, 2, 1, 'Yearly', 'No', 'No', 'Rahul (writer)', ''),
    ('/blog/international-driving-permit-india/', 'International driving permit from India', 'Guide', 'Visas', 'international driving permit india', '2024-10-01', '2025-10-20', 1100, 1080, 26000, 25500, 2.5, 2.6, 5, 2, 'Fast changing', 'Yes', 'Yes', 'Asha (writer)', ''),
    ('/blog/how-to-use-roamly-offline/', 'How to use Roamly offline', 'How to', 'Product', 'roamly offline', '2025-06-01', '2025-06-01', 300, 280, 4100, 4000, 1.8, 1.9, 12, 3, 'Evergreen', 'No', 'Not checked', 'Product team', ''),
    ('/blog/weekend-getaways-from-pune/', '10 weekend getaways from Pune', 'List', 'Destinations', 'weekend getaways from pune', '2021-10-10', '2022-05-01', 450, 120, 30000, 14000, 9.5, 16.8, 0, 1, 'Yearly', 'No', 'No', 'Rahul (writer)', ''),
    ('/blog/travel-trends-2025/', 'Travel trends 2025', 'News or trends', 'Planning', 'travel trends 2025', '2025-01-05', '2025-01-05', 500, 90, 22000, 5000, 6.0, 7.5, 0, 1, 'Fast changing', 'No', 'No', 'SEO', 'Dated topic: consider a 2026 piece'),
    ('/blog/best-travel-credit-cards-india/', 'Best travel credit cards in India', 'Comparison', 'Money', 'best travel credit cards india', '2024-08-01', '2025-03-01', 1900, 1200, 47000, 44000, 5.1, 6.0, 0, 2, 'Fast changing', 'Yes', 'No', 'Editor', ''),
    ('/blog/passport-renewal-steps/', 'Passport renewal in 6 steps', 'How to', 'Visas', 'passport renewal steps', '2023-11-01', '2023-11-01', 950, 520, 33000, 21000, 6.8, 10.4, 3, 2, 'Fast changing', 'No', 'No', 'Asha (writer)', ''),
    ('/blog/travel-photography-tips/', 'Travel photography tips for phones', 'List', 'Planning', 'travel photography tips', '2022-06-01', '2022-06-01', 40, 25, 4000, 3500, 24.0, 31.0, 0, 1, 'Evergreen', 'No', 'No', 'SEO', ''),
    ('/blog/monsoon-treks-maharashtra/', 'Monsoon treks in Maharashtra', 'Guide', 'Destinations', 'monsoon treks maharashtra', '2024-06-15', '2025-06-01', 1500, 400, 25000, 8000, 5.0, 5.5, 1, 1, 'Yearly', 'No', 'No', 'Rahul (writer)', 'Seasonal: compare year over year'),
    ('/blog/visa-free-countries-for-indians/', 'Visa free countries for Indians', 'List', 'Visas', 'visa free countries for indians', '2024-02-10', '2026-10-06', 5200, 5600, 140000, 150000, 2.2, 2.0, 40, 3, 'Fast changing', 'Yes', 'Yes', 'Asha (writer)', 'Refreshed in October, see Refresh Queue'),
    ('/blog/europe-trip-cost/', 'How much does a Europe trip cost?', 'Guide', 'Money', 'europe trip cost', '2023-04-01', '2024-04-01', 1700, 900, 52000, 37000, 5.8, 9.4, 14, 3, 'Fast changing', 'Yes', 'No', 'Editor', ''),
    ('/features/trip-planner/', 'Roamly trip planner', 'Landing page', 'Product', 'trip planner app', '2024-01-01', '2026-06-01', 650, 700, 8000, 8300, 3.5, 3.4, 140, 3, 'Evergreen', 'No', 'Not checked', 'Product team', ''),
    ('/blog/airport-lounge-access-guide/', 'Airport lounge access guide', 'Guide', 'Flights', 'airport lounge access', '2024-07-01', '2024-07-01', 880, 610, 21000, 20000, 4.2, 4.4, 2, 1, 'Yearly', 'Yes', 'No', 'Asha (writer)', ''),
    ('/blog/hidden-gems-rajasthan/', 'Hidden gems in Rajasthan', 'List', 'Destinations', 'hidden gems rajasthan', '2023-09-01', '2023-09-01', 120, 70, 6000, 5200, 12.5, 14.0, 0, 1, 'Evergreen', 'Not checked', 'Not checked', 'Rahul (writer)', ''),
    ('/blog/best-travel-apps/', 'Best travel apps for 2026', 'List', 'Product', 'best travel apps', '2023-03-01', '2025-03-01', 2100, 1650, 61000, 58000, 3.6, 3.9, 25, 3, 'Yearly', 'Yes', 'No', 'Product team', ''),
    ('/blog/schengen-visa-appointment/', 'How to get a Schengen visa appointment', 'How to', 'Visas', 'schengen visa checklist', '2024-03-15', '2024-03-15', 1300, 780, 36000, 33000, 6.2, 8.0, 6, 2, 'Fast changing', 'Yes', 'No', 'Asha (writer)', 'Overlaps with the Schengen checklist'),
    ('/blog/road-trip-checklist/', 'Road trip checklist', 'List', 'Planning', 'road trip planning', '2023-10-01', '2023-10-01', 90, 60, 7000, 6500, 14.0, 15.5, 0, 2, 'Evergreen', 'No', 'No', 'Rahul (writer)', 'Overlaps with the road trip guide'),
]
# url, week, override, owner, refreshed on, what changed, substantial, clicks 28d before, after
QUEUE = [
    ('/blog/schengen-visa-checklist/', 'Week 1', None, 'Asha (writer)', None, '', None, None, None),
    ('/blog/best-time-to-visit-bali/', 'Week 1', None, 'Rahul (writer)', None, '', None, None, None),
    ('/blog/digital-nomad-visa-countries/', 'Week 1', None, 'Asha (writer)', None, '', None, None, None),
    ('/blog/cheap-flights-tips/', 'Week 2', None, 'Asha (writer)', None, '', None, None, None),
    ('/blog/schengen-visa-appointment/', 'Week 2', 'Merge or improve', 'Asha (writer)', None, 'Merge into the Schengen checklist and 301 redirect', None, None, None),
    ('/blog/europe-trip-cost/', 'Week 3', None, 'Editor', None, '', None, None, None),
    ('/blog/travel-trends-2025/', 'Week 3', None, 'SEO', None, '', None, None, None),
    ('/blog/visa-free-countries-for-indians/', None, None, 'Asha (writer)', '2026-10-06', 'Added 3 countries, updated 5 rules, new FAQ', 'Yes', 1650, 1980),
    ('/blog/japan-rail-pass-guide/', None, 'Snippet refresh', 'Rahul (writer)', '2026-11-10', 'New title and meta description only', 'No', 410, None),
    ('/blog/packing-list-for-ladakh/', None, None, 'Rahul (writer)', '2026-09-15', 'Rewrote gear section, added winter list', 'Yes', 260, 245),
]

CI_IN = ['URL', 'Title', 'Content type', 'Topic', 'Main query', 'Published', 'Last substantial update', 'Clicks (previous)',
         'Clicks (recent)', 'Impressions (previous)', 'Impressions (recent)', 'Position (previous)', 'Position (recent)',
         'Conversions (recent)', 'Business value (1 to 3)', 'Time sensitivity', 'AI Overview on main query?',
         'Cited in AI answers?', 'Owner', 'Notes']
CI_FH = ['Click change', 'Click change %', 'Impression change %', 'Positions lost', 'CTR (previous)', 'CTR (recent)',
         'CTR change', 'Months since update', 'Review due?', 'Diagnosis', 'Refresh type', 'What to do', 'Query overlap',
         'Clicks lost', 'Refresh score (0 to 100)', 'Priority', 'Hours (assumption)', 'Est. clicks recovered (assumption)',
         'Clicks recovered per hour', 'In refresh queue?', 'Rank (helper)']
CI_HEAD = CI_IN + CI_FH
CC = {h: L(i + 1) for i, h in enumerate(CI_HEAD)}
CI_F = tuple(range(len(CI_IN) + 1, len(CI_HEAD) + 1))
DECAYS = ['Ranking decay', 'CTR decay', 'CTR decay (AI Overview)', 'Demand decay', 'Mixed decay']


def ci(h):
    c = CC.get(h, h)
    return f'{CIS}!${c}${CI_FIRST}:${c}${CI_LAST}'


def d(s):
    return datetime.date.fromisoformat(s) if s else None


def settings_sheet(wb):
    ws = wb.create_sheet(S)
    ws.sheet_view.showGridLines = False
    K.title_block(ws, 'Settings', 'Every rule, weight and list used by this workbook. Change a blue value and every diagnosis, score and priority updates.')
    for c, w in zip('ABCDEFGHIJKLMNOPQRSTU', [52, 16, 3, 3, 3, 18, 10, 30, 3, 22, 17, 8, 10, 70, 3, 16, 14, 12, 16, 10, 3]):
        ws.column_dimensions[c].width = w
    rows = [
        (4, 'PERIODS AND DIAGNOSIS RULES', None, None),
        (5, 'Today (set it to the day you review the sheet)', datetime.date(2026, 11, 24), 'dd mmm yyyy'),
        (6, 'Previous period (label only)', '21 May to 18 Aug 2026', '@'),
        (7, 'Recent period (label only)', '19 Aug to 16 Nov 2026', '@'),
        (8, 'Low traffic: fewer clicks than this in both periods', 100, '#,##0'),
        (9, 'Growing: clicks up by at least', 0.1, '0%'),
        (10, 'Decay: clicks down by at least', 0.2, '0%'),
        (11, 'Impressions drop: down by at least', 0.2, '0%'),
        (12, 'Impressions stable: down by less than', 0.15, '0%'),
        (13, 'Ranking drop: positions lost at least', 2, '0.0'),
        (14, 'Clicks lost that earn full marks', 2000, '#,##0'),
        (15, 'P1: refresh now when the score is at least', 70, '0'),
        (16, 'P2: this month when at least', 50, '0'),
        (17, 'P3: this quarter when at least (below = P4: later)', 30, '0'),
        (18, 'Writing hours per week', 12, '0'),
        (19, 'Measure results this many days after a refresh', 28, '0'),
    ]
    for r, label, val, fmt in rows:
        a = ws.cell(row=r, column=1, value=label)
        a.font = K.f(10, val is None, K.DEEP if val is None else K.INK)
        if val is not None:
            c = ws.cell(row=r, column=2, value=val)
            c.border, c.fill = K.BORDER, K.INPUT_FILL
            c.font = K.f(10, True, '0000FF')
            c.number_format = fmt
    ws['A21'] = ('Refresh score = clicks lost weight x MIN(1, clicks lost / full marks) + business value weight x value / 3 '
                 '+ position weight x position band factor + review weight (when a review is due). Compare periods of the '
                 'same length; for seasonal pages compare the same months a year earlier. Every rule, weight, hour and '
                 'recovery share on this tab is an assumption of this kit for you to tune; Google publishes no such numbers.')
    ws['A21'].font = K.f(9, False, '777777', True)
    ws['A21'].alignment = Alignment(wrap_text=True, vertical='top')
    ws.merge_cells('A21:B30')

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
    table(6, 5, 'SCORE WEIGHTS (add up to 100)', ['Factor', 'Weight'], WEIGHTS)
    ws['F10'] = 'Total'
    ws['G10'] = '=SUM(G6:G9)'
    ws['G10'].fill, ws['G10'].font = K.FORMULA_FILL, K.f(10, True)
    table(6, 12, 'POSITION BAND (recent average position)', ['At least', 'Factor', 'Meaning'], POSBANDS, ['0.0', '0.0', '@'])
    table(6, 20, 'REVIEW AFTER (months since the last real update)', ['Time sensitivity', 'Months'], FRESH)
    table(10, 5, 'DIAGNOSIS TO REFRESH TYPE (hours and recovery are assumptions)', ['Diagnosis', 'Refresh type', 'Hours', 'Recovery share', 'What to do'], TYPES, ['@', '@', '0', '0%', '@'], blue=(2, 3))
    for r in range(6, 15):
        ws.row_dimensions[r].height = 30
    ws['J16'] = 'Recovery share = the share of lost clicks a refresh of that type might win back. A starting assumption only: replace it with your own results from the Refresh Queue.'
    ws['J16'].font = K.f(8, False, '777777', True)
    ws.merge_cells('J16:N17')
    ws['J16'].alignment = Alignment(wrap_text=True, vertical='top')
    lists = [('P', 'Content type', CTYPES), ('Q', 'Time sensitivity', SENS), ('R', 'Yes, No, Not checked', YNC),
             ('S', 'Owner', OWNERS), ('T', 'Week', WEEKS)]
    ws['P19'] = 'LISTS (used by the dropdowns)'
    ws['P19'].font = K.f(10, True, K.DEEP)
    for col, head, vals in lists:
        ws[f'{col}20'] = head
        ws[f'{col}20'].font = K.f(9, True, '555555')
        n = 12 if col in 'PS' else len(vals)
        for i in range(n):
            c = ws[f'{col}{21 + i}']
            c.value = vals[i] if i < len(vals) else None
            c.fill, c.border, c.font = K.INPUT_FILL, K.BORDER, K.f(10)
    return ws


def inventory_sheet(wb):
    ws = wb.create_sheet('Content Inventory')
    ws.sheet_view.showGridLines = False
    K.title_block(ws, 'Content inventory', f'One row per URL. Rows 5 to {4 + len(PAGES)} are DEMO pages for Roamly, a fictional travel planning app (illustrative numbers). Replace them with your own; 500 rows ready.')
    ws['A2'].font = K.f(10, True, 'B45309')
    ws['A3'] = ('Export pages from the Search Console Performance report twice: the previous period and the recent period '
                '(same length). Paste clicks, impressions and position. Sort by Refresh score and work P1 first.')
    ws['A3'].font = K.f(9, False, '666666', True)
    widths = [36, 34, 13, 12, 26, 11, 11, 9, 9, 11, 11, 8, 8, 9, 9, 12, 10, 10, 13, 26,
              8, 8, 9, 8, 7, 7, 7, 8, 8, 18, 14, 50, 26, 8, 9, 14, 7, 10, 9, 8, 9]
    K.header_row(ws, 4, CI_HEAD, formula_cols=CI_F, widths=widths)
    c = CC
    qa = f'{RQS}!$A${RQ_FIRST}:$A${RQ_LAST}'
    for r in range(CI_FIRST, CI_LAST + 1):
        i = r - CI_FIRST
        if i < len(PAGES):
            row = list(PAGES[i])
            row[0] = U + row[0]
            row[5], row[6] = d(row[5]), d(row[6])
            for col, v in enumerate(row, 1):
                if v not in (None, ''):
                    ws.cell(row=r, column=col, value=v)
        e = f'A{r}=""'
        g = lambda h: f'{c[h]}{r}'
        f = {}
        f['Click change'] = f'=IF({e},"",N(I{r})-N(H{r}))'
        f['Click change %'] = f'=IF(OR({e},N(H{r})=0),"",(N(I{r})-H{r})/H{r})'
        f['Impression change %'] = f'=IF(OR({e},N(J{r})=0),"",(N(K{r})-J{r})/J{r})'
        f['Positions lost'] = f'=IF(OR({e},L{r}="",M{r}=""),"",M{r}-L{r})'
        f['CTR (previous)'] = f'=IF(OR({e},N(J{r})=0),"",N(H{r})/J{r})'
        f['CTR (recent)'] = f'=IF(OR({e},N(K{r})=0),"",N(I{r})/K{r})'
        f['CTR change'] = f'=IF(OR({g("CTR (previous)")}="",{g("CTR (recent)")}=""),"",{g("CTR (recent)")}-{g("CTR (previous)")})'
        f['Months since update'] = f'=IF(OR({e},AND(F{r}="",G{r}="")),"",ROUND(({DATE}-IF(G{r}<>"",G{r},F{r}))/30.44,1))'
        mo = g('Months since update')
        f['Review due?'] = f'=IF({e},"",IF({mo}="","Add a date",IF({mo}>=IFERROR(VLOOKUP(P{r},{FRESH_RNG},2,FALSE),12),"Yes","No")))'
        cc, ic, pl, due = g('Click change %'), g('Impression change %'), g('Positions lost'), g('Review due?')
        f['Diagnosis'] = (f'=IF({e},"",IF(AND(N(H{r})<{LOW},N(I{r})<{LOW}),"Low traffic",IF({cc}="","New or no previous data",'
                          f'IF({cc}>={GROW},"Growing",IF(AND({ic}<>"",{pl}<>"",{ic}<=-{IMPDROP},{pl}>={POSLOSS}),"Ranking decay",'
                          f'IF(AND({cc}<=-{DECAY},{ic}<>"",{ic}>-{IMPSTAB}),IF(Q{r}="Yes","CTR decay (AI Overview)","CTR decay"),'
                          f'IF(AND({ic}<>"",{ic}<=-{IMPDROP}),"Demand decay",IF({cc}<=-{DECAY},"Mixed decay",'
                          f'IF({due}="Yes","Stable, review due","Stable")))))))))')
        dg = g('Diagnosis')
        f['Refresh type'] = f'=IF({e},"",IFERROR(VLOOKUP({dg},{TYPE_RNG},2,FALSE),"Monitor"))'
        f['What to do'] = f'=IF({e},"",IFERROR(VLOOKUP({dg},{TYPE_RNG},5,FALSE),"Add clicks for both periods"))'
        f['Query overlap'] = f'=IF(OR({e},E{r}=""),"",IF(COUNTIF($E${CI_FIRST}:$E${CI_LAST},E{r})>1,"Shares its main query with "&(COUNTIF($E${CI_FIRST}:$E${CI_LAST},E{r})-1)&" other URL","Unique"))'
        f['Clicks lost'] = f'=IF({e},"",MAX(0,N(H{r})-N(I{r})))'
        pos = f'IF(M{r}="",0.5,VLOOKUP(M{r},{POS_RNG},2,TRUE))'
        f['Refresh score (0 to 100)'] = (f'=IF({e},"",ROUND({W_LOST}*MIN(1,{g("Clicks lost")}/{FULL})+{W_VALUE}*IF(O{r}="",2,O{r})/3'
                                         f'+{W_POS}*{pos}+{W_DUE}*IF({due}="Yes",1,0),0))')
        sc = g('Refresh score (0 to 100)')
        tpv = g('Refresh type')
        f['Priority'] = (f'=IF({e},"",IF(OR({tpv}="Monitor",{tpv}="Protect"),"Monitor",IF({sc}>={P1},"P1: refresh now",'
                         f'IF({sc}>={P2},"P2: this month",IF({sc}>={P3},"P3: this quarter","P4: later")))))')
        f['Hours (assumption)'] = f'=IF({e},"",IFERROR(VLOOKUP({dg},{TYPE_RNG},3,FALSE),0))'
        f['Est. clicks recovered (assumption)'] = f'=IF({e},"",ROUND({g("Clicks lost")}*IFERROR(VLOOKUP({dg},{TYPE_RNG},4,FALSE),0),0))'
        hr = g('Hours (assumption)')
        f['Clicks recovered per hour'] = f'=IF(OR({e},N({hr})=0),"",ROUND({g("Est. clicks recovered (assumption)")}/{hr},0))'
        f['In refresh queue?'] = f'=IF({e},"",IF(COUNTIF({qa},A{r})>0,"Yes","No"))'
        f['Rank (helper)'] = f'=IF(OR({e},{g("Priority")}="Monitor"),"",{sc}+{g("Est. clicks recovered (assumption)")}/100000-ROW()/10000000)'
        for h, v in f.items():
            ws[f'{c[h]}{r}'] = v
    idx = lambda h: CI_HEAD.index(h) + 1
    nf = {6: 'dd mmm yyyy', 7: 'dd mmm yyyy', 8: '#,##0', 9: '#,##0', 10: '#,##0', 11: '#,##0', 12: '0.0', 13: '0.0', 14: '#,##0'}
    nf.update({idx('Click change'): '#,##0', idx('Click change %'): '0%', idx('Impression change %'): '0%', idx('Positions lost'): '0.0',
               idx('CTR (previous)'): '0.0%', idx('CTR (recent)'): '0.0%', idx('CTR change'): '0.0%', idx('Months since update'): '0.0',
               idx('Clicks lost'): '#,##0', idx('Refresh score (0 to 100)'): '0', idx('Hours (assumption)'): '0',
               idx('Est. clicks recovered (assumption)'): '#,##0', idx('Clicks recovered per hour'): '#,##0', idx('Rank (helper)'): '0.000000'})
    K.style_body(ws, CI_FIRST, CI_LAST, len(CI_HEAD), formula_cols=CI_F, number_formats=nf,
                 wrap_cols=(1, 2, 20, idx('What to do'), idx('Query overlap')))
    K.dropdown(ws, f'C{CI_FIRST}:C{CI_LAST}', f'{S}!$P$21:$P$32')
    K.dropdown(ws, f'O{CI_FIRST}:O{CI_LAST}', '"1,2,3"', '3 close to a sale or lead, 2 builds trust, 1 loosely related.')
    K.dropdown(ws, f'P{CI_FIRST}:P{CI_LAST}', f'{S}!$Q$21:$Q$23', 'How fast the facts on this page go out of date.')
    K.dropdown(ws, f'Q{CI_FIRST}:R{CI_LAST}', f'{S}!$R$21:$R$23')
    K.dropdown(ws, f'S{CI_FIRST}:S{CI_LAST}', f'{S}!$S$21:$S$32')
    for col in 'HIJKN':
        K.whole_number(ws, f'{col}{CI_FIRST}:{col}{CI_LAST}', 0, 1000000000, 'A whole number.')
    dc = c['Diagnosis']
    dr = f'{dc}{CI_FIRST}:{dc}{CI_LAST}'
    for txt, fill, fc in (('Ranking decay', '9B2C1F', 'FFFFFF'), ('CTR decay', 'F8D7D3', '9B2C1F'), ('Demand decay', 'FFF4CC', '1F1F1F'),
                          ('Mixed decay', 'FCE5CD', '1F1F1F'), ('Low traffic', 'EEEEEE', '555555'), ('Growing', 'B7E4A0', '1F1F1F'), ('Stable', 'EEF8E6', '3D7F12')):
        ws.conditional_formatting.add(dr, FormulaRule(formula=[f'LEFT({dc}{CI_FIRST},{len(txt)})="{txt}"'], fill=PatternFill('solid', fgColor=fill), font=Font(name=K.FONT, bold=True, color=fc)))
    pc = c['Priority']
    pr = f'{pc}{CI_FIRST}:{pc}{CI_LAST}'
    for start, fill, fc in (('P1', '9B2C1F', 'FFFFFF'), ('P2', 'F8D7D3', '9B2C1F'), ('P3', 'FFF4CC', '1F1F1F'), ('P4', 'EEEEEE', '555555'), ('Mo', 'EEF8E6', '3D7F12')):
        ws.conditional_formatting.add(pr, FormulaRule(formula=[f'LEFT({pc}{CI_FIRST},2)="{start}"'], fill=PatternFill('solid', fgColor=fill), font=Font(name=K.FONT, bold=True, color=fc)))
    for h in ('Click change %', 'Impression change %'):
        col = c[h]
        ws.conditional_formatting.add(f'{col}{CI_FIRST}:{col}{CI_LAST}', ColorScaleRule(start_type='num', start_value=-0.5, start_color='E07A5F', mid_type='num', mid_value=0, mid_color='FFFFFF', end_type='num', end_value=0.5, end_color='8BC34A'))
    sc = c['Refresh score (0 to 100)']
    ws.conditional_formatting.add(f'{sc}{CI_FIRST}:{sc}{CI_LAST}', ColorScaleRule(start_type='num', start_value=0, start_color='FFFFFF', mid_type='num', mid_value=50, mid_color='FFF4CC', end_type='num', end_value=100, end_color='E07A5F'))
    oc = c['Query overlap']
    ws.conditional_formatting.add(f'{oc}{CI_FIRST}:{oc}{CI_LAST}', FormulaRule(formula=[f'LEFT({oc}{CI_FIRST},6)="Shares"'], fill=PatternFill('solid', fgColor='FFF4CC'), font=Font(name=K.FONT, bold=True)))
    rv = c['Review due?']
    ws.conditional_formatting.add(f'{rv}{CI_FIRST}:{rv}{CI_LAST}', CellIsRule(operator='equal', formula=['"Yes"'], font=Font(name=K.FONT, bold=True, color='9B2C1F')))
    ws.column_dimensions[c['Rank (helper)']].hidden = True
    for r in range(CI_FIRST, CI_FIRST + len(PAGES)):
        ws.row_dimensions[r].height = 30
    ws.freeze_panes = 'C5'
    ws.auto_filter.ref = f'A4:{L(len(CI_HEAD))}{CI_LAST}'
    return ws


def queue_sheet(wb):
    ws = wb.create_sheet('Refresh Queue')
    ws.sheet_view.showGridLines = False
    K.title_block(ws, 'Refresh queue', 'Plan refreshes by week. Pick a URL from the Content Inventory, a week and a writer. The brief writes itself. After the refresh, add the date, whether the change was substantial and clicks for 28 days before and after.')
    head = ['URL', 'Week', 'Refresh type override (blank = suggested)', 'Owner', 'Refreshed on', 'What changed', 'Substantial change?',
            'Clicks 28 days before', 'Clicks 28 days after', 'Title', 'Diagnosis', 'Refresh type', 'Hours', 'Priority', 'Main query',
            'Brief (copy to the writer)', 'Date rule', 'Measure on', 'Click change', 'Result']
    fc = tuple(range(10, 21))
    K.header_row(ws, 4, head, formula_cols=fc, widths=[34, 9, 16, 14, 11, 30, 11, 9, 9, 28, 16, 14, 7, 14, 22, 70, 30, 11, 9, 28])
    idx = lambda r: f'MATCH(A{r},{ci("A")},0)'
    get = lambda h, r: f'INDEX({ci(h)},{idx(r)})'
    tcol = f'{S}!$K$6:$K$14'
    for r in range(RQ_FIRST, RQ_LAST + 1):
        i = r - RQ_FIRST
        if i < len(QUEUE):
            url, wk, ov, own, done, what, subst, bef, aft = QUEUE[i]
            for col, v in enumerate([U + url, wk, ov, own, d(done), what, subst, bef, aft], 1):
                if v not in (None, ''):
                    ws.cell(row=r, column=col, value=v)
        e = f'A{r}=""'
        ok = f'ISNUMBER({idx(r)})'
        no = f'OR({e},NOT({ok}))'
        ws[f'J{r}'] = f'=IF({e},"",IF({ok},""&{get("B", r)},"URL not in the Content Inventory"))'
        ws[f'K{r}'] = f'=IF({no},"",{get("Diagnosis", r)})'
        ws[f'L{r}'] = f'=IF({no},"",IF(C{r}<>"",C{r},{get("Refresh type", r)}))'
        ws[f'M{r}'] = f'=IF({no},"",IFERROR(INDEX({S}!$L$6:$L$14,MATCH(L{r},{tcol},0)),0))'
        ws[f'N{r}'] = f'=IF({no},"",{get("Priority", r)})'
        ws[f'O{r}'] = f'=IF({no},"",""&{get("E", r)})'
        act = f'IFERROR(INDEX({S}!$N$6:$N$14,MATCH(L{r},{tcol},0)),"")'
        ovl = get('Query overlap', r)
        ws[f'P{r}'] = (f'=IF({no},"","Refresh: "&J{r}&" ("&A{r}&"). Diagnosis: "&K{r}&". Main query: "&O{r}&". Do: "&{act}&". "'
                       f'&IF({get("Q", r)}="Yes","An AI Overview shows for the main query: answer it clearly near the top and add what a summary cannot. ","")'
                       f'&IF(LEFT({ovl},6)="Shares",{ovl}&": merge the pages or give each a clearly different intent. ","")'
                       f'&"Keep the URL and add links from 2 related pages.")')
        ws[f'Q{r}'] = (f'=IF({e},"",IF(G{r}="Yes","Update the visible Last updated date and dateModified",IF(G{r}="No","Keep the old date: the change is not substantial",'
                       f'"Decide whether the change is substantial")))')
        ws[f'R{r}'] = f'=IF(OR({e},E{r}=""),"",E{r}+{MEASURE})'
        ws[f'S{r}'] = f'=IF(OR({e},N(H{r})=0,I{r}=""),"",(I{r}-H{r})/H{r})'
        ws[f'T{r}'] = (f'=IF({e},"",IF(E{r}="","Not refreshed yet",IF({DATE}<R{r},"Wait: "&(R{r}-{DATE})&" days left",IF(I{r}="","Add clicks after",'
                       f'IF(S{r}="","Add clicks before",IF(S{r}>=0.1,"Up "&TEXT(S{r},"0%")&": keep going",IF(S{r}>-0.1,"Flat: check rankings by query","Still falling: diagnose again")))))))')
    K.style_body(ws, RQ_FIRST, RQ_LAST, len(head), formula_cols=fc, number_formats={5: 'dd mmm yyyy', 8: '#,##0', 9: '#,##0', 18: 'dd mmm yyyy', 19: '0%'},
                 wrap_cols=(1, 6, 10, 16, 17, 20))
    for r in range(RQ_FIRST, RQ_FIRST + len(QUEUE)):
        ws.row_dimensions[r].height = 75
    K.dropdown(ws, f'A{RQ_FIRST}:A{RQ_LAST}', ci('A'), 'URLs from the Content Inventory.')
    K.dropdown(ws, f'B{RQ_FIRST}:B{RQ_LAST}', f'{S}!$T$21:$T$28')
    K.dropdown(ws, f'C{RQ_FIRST}:C{RQ_LAST}', tcol)
    K.dropdown(ws, f'D{RQ_FIRST}:D{RQ_LAST}', f'{S}!$S$21:$S$32')
    K.dropdown(ws, f'G{RQ_FIRST}:G{RQ_LAST}', '"Yes,No"', 'Yes only when the content really changed, not just the date.')
    t = f'T{RQ_FIRST}:T{RQ_LAST}'
    ws.conditional_formatting.add(t, FormulaRule(formula=[f'LEFT(T{RQ_FIRST},2)="Up"'], fill=PatternFill('solid', fgColor='B7E4A0'), font=Font(name=K.FONT, bold=True)))
    ws.conditional_formatting.add(t, FormulaRule(formula=[f'LEFT(T{RQ_FIRST},5)="Still"'], fill=PatternFill('solid', fgColor='F8D7D3'), font=Font(name=K.FONT, bold=True, color='9B2C1F')))
    ws.conditional_formatting.add(t, FormulaRule(formula=[f'OR(LEFT(T{RQ_FIRST},4)="Wait",LEFT(T{RQ_FIRST},4)="Flat",LEFT(T{RQ_FIRST},3)="Add")'], fill=PatternFill('solid', fgColor='FFF4CC')))
    q = f'Q{RQ_FIRST}:Q{RQ_LAST}'
    ws.conditional_formatting.add(q, FormulaRule(formula=[f'LEFT(Q{RQ_FIRST},4)="Keep"'], font=Font(name=K.FONT, bold=True, color='9B2C1F')))
    ws['V4'] = 'WEEKLY WRITING HOURS'
    ws['V4'].font = K.f(10, True, K.DEEP)
    for j, h in enumerate(['Week', 'Hours planned', 'Capacity', 'Status']):
        cc = ws.cell(row=5, column=22 + j, value=h)
        cc.font, cc.fill = K.f(10, True, 'FFFFFF'), K.HEAD_F
    for i in range(len(WEEKS)):
        r = 6 + i
        ws.cell(row=r, column=22, value=f'={S}!T{21 + i}')
        ws.cell(row=r, column=23, value=f'=SUMIF($B${RQ_FIRST}:$B${RQ_LAST},V{r},$M${RQ_FIRST}:$M${RQ_LAST})')
        ws.cell(row=r, column=24, value=f'={HOURS}')
        ws.cell(row=r, column=25, value=f'=IF(W{r}=0,"Free",IF(W{r}>X{r},"Over capacity by "&(W{r}-X{r})&" hours","OK"))')
        for cc in range(22, 26):
            cell = ws.cell(row=r, column=cc)
            cell.border, cell.fill, cell.font = K.BORDER, K.FORMULA_FILL, K.f(10)
    for col, w in zip('UVWXY', [3, 12, 10, 9, 24]):
        ws.column_dimensions[col].width = w
    ws.conditional_formatting.add('Y6:Y13', FormulaRule(formula=['LEFT(Y6,4)="Over"'], fill=PatternFill('solid', fgColor='F8D7D3'), font=Font(name=K.FONT, bold=True, color='9B2C1F')))
    ws.freeze_panes = 'B5'
    ws.auto_filter.ref = f'A4:T{RQ_LAST}'
    return ws


PLAYBOOK = [
    ('Ranking decay', 'Impressions and position fell together. Competitors improved, facts went stale, or the page no longer matches what searchers want.',
     'In Search Console, filter by this URL and compare queries: which ones lost position? Search the main query and read today\'s top results.',
     'Update facts, add the subtopics the top results cover and you do not, add original examples, data or experience, improve the opening answer, refresh internal links.',
     'Do not change the URL. Do not cut sections that still rank for other queries.'),
    ('CTR decay', 'Impressions held but clicks fell. A new results feature, a weaker title than competitors or an old date in the snippet.',
     'Search the main query in a private window. Compare your title and description with the top results.',
     'Rewrite the title and meta description around the main intent. Show a clear visible date when you truly update the page.',
     'Do not add a new year to the title without updating the content.'),
    ('CTR decay (AI Overview)', 'An AI Overview answers part of the query on the results page, so fewer people click.',
     'Is your page linked inside the AI Overview? What does the overview leave out?',
     'Put a clear, self contained answer near the top, then add depth the summary cannot give: steps, examples, tables, first hand experience. Keep headings and FAQs clear.',
     'Do not shrink the page to a short answer only. Do not chase the overview with keyword stuffing.'),
    ('Demand decay', 'Fewer people search the topic. Often seasonal, sometimes a fading trend.',
     'Check Google Trends and compare the same months a year earlier in Search Console.',
     'Light refresh of facts before the next season. Move effort to growing topics.',
     'Do not rewrite a page that still ranks well just because the season ended.'),
    ('Mixed decay', 'Clicks fell without a clear pattern in impressions or position.',
     'Break the page down by query and by country or device. Check for a tracking or migration change.',
     'Fix the specific queries that lost clicks; treat them as ranking or CTR decay.',
     'Do not start a full rewrite before you know which queries dropped.'),
    ('Low traffic', 'Few clicks in both periods. The page may be thin, overlap another page or serve a small audience.',
     'Does it bring links, conversions or help visitors? Does another page cover the same query?',
     'Merge into a stronger page with a 301 redirect, improve it, or leave it if it is useful.',
     'Do not delete pages in bulk to look fresh. Google says that does not help rankings.'),
    ('Growing', 'Clicks are rising.', 'Which queries grew? Is the page close to the top 3 for them?',
     'Protect it: small fact updates only, and add internal links to it from related pages.',
     'Do not restructure a growing page.'),
    ('Stable, review due', 'Traffic is steady but the last real update is older than the review window for this kind of content.',
     'Check facts, prices, screenshots, links and rules that may have changed.',
     'Fix what is out of date. Update the visible date only if the change is substantial.',
     'Do not change the date when the content has not really changed.'),
]


def playbook_sheet(wb):
    ws = wb.create_sheet('Refresh Playbook')
    ws.sheet_view.showGridLines = False
    K.title_block(ws, 'Refresh playbook', 'What each diagnosis on the Content Inventory usually means and how to refresh the page. Edit it to match your own process.')
    K.header_row(ws, 4, ['Diagnosis', 'What it usually means', 'Check first', 'What to change', 'What not to do', 'Pages now'], formula_cols=(6,), widths=[22, 44, 44, 54, 40, 9])
    for i, row in enumerate(PLAYBOOK):
        r = 5 + i
        for col, v in enumerate(row, 1):
            ws.cell(row=r, column=col, value=v)
        ws.cell(row=r, column=6, value=f'=COUNTIF({ci("Diagnosis")},A{r})')
        ws.row_dimensions[r].height = 78
    K.style_body(ws, 5, 4 + len(PLAYBOOK), 6, formula_cols=(6,), wrap_cols=(1, 2, 3, 4, 5))
    for r in range(5, 5 + len(PLAYBOOK)):
        ws.cell(row=r, column=1).font = K.f(10, True)
    r0 = 7 + len(PLAYBOOK)
    ws.cell(row=r0, column=1, value='EVERY REFRESH, WHATEVER THE TYPE').font = K.f(10, True, K.DEEP)
    steps = ['Keep the same URL.', 'Read today\'s top results and AI answers for the main query before you write.',
             'Check every fact, price, rule, screenshot and outbound link.', 'Answer the main question clearly near the top.',
             'Add something the top results lack: examples, data, steps or first hand experience.',
             'Add or update internal links from 2 related pages.', 'Update the visible date and dateModified only for a substantial change.',
             'Request indexing in Search Console for important pages.', 'Log the refresh on the Refresh Queue and measure after 28 days.']
    for i, s in enumerate(steps):
        ws.cell(row=r0 + 1 + i, column=1, value=i + 1).font = K.f(10, True, K.DEEP)
        c = ws.cell(row=r0 + 1 + i, column=2, value=s)
        c.font = K.f(10)
        ws.merge_cells(start_row=r0 + 1 + i, start_column=2, end_row=r0 + 1 + i, end_column=4)
    ws.freeze_panes = 'B5'
    return ws


def chart(ws, title, ytitle, cat_col, val_cols, r1, r2, anchor, colors, horiz, titles, h=7.5, w=16):
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
    for col, w in zip('ABCDEFGHIJK', [50, 14, 3, 40, 22, 9, 9, 15, 11, 10, 3]):
        ws.column_dimensions[col].width = w
    dg = ci('Diagnosis')
    decay = '+'.join(f'COUNTIF({dg},"{x}")' for x in DECAYS)
    pr = ci('Priority')
    kpis = [
        ('URLs tracked', f'=COUNTIF({ci("A")},"?*")', '0'),
        ('Clicks, previous period', f'=SUM({ci("H")})', '#,##0'),
        ('Clicks, recent period', f'=SUM({ci("I")})', '#,##0'),
        ('Change in clicks', f'=IFERROR(B7/B6-1,"")', '0%'),
        ('Clicks lost on pages that fell', f'=SUM({ci("Clicks lost")})', '#,##0'),
        ('Pages in decay', f'={decay}', '0'),
        ('P1 pages to refresh now', f'=COUNTIF({pr},"P1*")', '0'),
        ('P2 pages for this month', f'=COUNTIF({pr},"P2*")', '0'),
        ('Pages with a review due', f'=COUNTIF({ci("Review due?")},"Yes")', '0'),
        ('CTR decay under an AI Overview', f'=COUNTIF({dg},"CTR decay (AI Overview)")', '0'),
        ('URLs sharing a main query', f'=COUNTIF({ci("Query overlap")},"Shares*")', '0'),
        ('Hours for P1 and P2 pages (assumption)', f'=SUMIF({pr},"P1*",{ci("Hours (assumption)")})+SUMIF({pr},"P2*",{ci("Hours (assumption)")})', '0'),
        ('Clicks P1 and P2 refreshes might win back (assumption)', f'=SUMIF({pr},"P1*",{ci("Est. clicks recovered (assumption)")})+SUMIF({pr},"P2*",{ci("Est. clicks recovered (assumption)")})', '#,##0'),
        ('Pages in the refresh queue', f'=COUNTIF({RQS}!$A${RQ_FIRST}:$A${RQ_LAST},"?*")', '0'),
        ('Refreshed, waiting to measure', f'=COUNTIF({RQS}!$T${RQ_FIRST}:$T${RQ_LAST},"Wait*")', '0'),
        ('Refreshed and up', f'=COUNTIF({RQS}!$T${RQ_FIRST}:$T${RQ_LAST},"Up*")', '0'),
        ('Refreshed and flat or still falling', f'=COUNTIF({RQS}!$T${RQ_FIRST}:$T${RQ_LAST},"Flat*")+COUNTIF({RQS}!$T${RQ_FIRST}:$T${RQ_LAST},"Still*")', '0'),
    ]
    ws['A4'] = 'KEY NUMBERS'
    ws['A4'].font = K.f(10, True, K.DEEP)
    for i, (label, fml, fmt) in enumerate(kpis):
        r = 5 + i
        ws.cell(row=r, column=1, value=label).font = K.f(10)
        cell = ws.cell(row=r, column=2, value=fml)
        cell.number_format, cell.font, cell.fill, cell.border = fmt, K.f(11, True), K.FORMULA_FILL, K.BORDER
        cell.alignment = Alignment(horizontal='right')
    ws['D4'] = 'TOP 10 REFRESH CANDIDATES (highest refresh score first)'
    ws['D4'].font = K.f(10, True, K.DEEP)
    heads = ['Title', 'Diagnosis', 'Score', 'Lost', 'Priority', 'Refresh type', 'Queued?']
    cols = ['B', 'Diagnosis', 'Refresh score (0 to 100)', 'Clicks lost', 'Priority', 'Refresh type', 'In refresh queue?']
    for j, h in enumerate(heads):
        cell = ws.cell(row=5, column=4 + j, value=h)
        cell.font, cell.fill = K.f(10, True, 'FFFFFF'), K.HEAD_F
    rk = ci('Rank (helper)')
    for k in range(1, 11):
        r = 5 + k
        mt = f'MATCH(LARGE({rk},{k}),{rk},0)'
        for j, col in enumerate(cols):
            cell = ws.cell(row=r, column=4 + j, value=f'=IFERROR(INDEX({ci(col)},{mt}),"")')
            cell.border, cell.fill, cell.font = K.BORDER, K.FORMULA_FILL, K.f(9, j == 0)
            cell.alignment = Alignment(wrap_text=j in (0, 1), vertical='top')
            cell.number_format = {2: '0', 3: '#,##0'}.get(j, '@')
        ws.row_dimensions[r].height = 26
    top = 25
    ws.cell(row=top - 1, column=1, value='PAGES BY DIAGNOSIS').font = K.f(10, True, K.DEEP)
    for j, h in enumerate(['Diagnosis', 'Pages', 'Clicks lost', 'Hours (assumption)']):
        cell = ws.cell(row=top, column=1 + j if j < 2 else 2 + j, value=h)
        cell.font, cell.fill = K.f(10, True, 'FFFFFF'), K.HEAD_F
    for i in range(len(TYPES)):
        r = top + 1 + i
        ws.cell(row=r, column=1, value=f'={S}!J{6 + i}')
        ws.cell(row=r, column=2, value=f'=COUNTIF({dg},A{r})')
        ws.cell(row=r, column=4, value=f'=SUMIF({dg},A{r},{ci("Clicks lost")})')
        ws.cell(row=r, column=5, value=f'=SUMIF({dg},A{r},{ci("Hours (assumption)")})')
        for cc in (1, 2, 4, 5):
            cell = ws.cell(row=r, column=cc)
            cell.border, cell.fill, cell.font = K.BORDER, K.FORMULA_FILL, K.f(10, cc == 1)
            if cc == 4:
                cell.number_format = '#,##0'
    last = top + len(TYPES)
    t2 = last + 4
    ws.cell(row=t2 - 1, column=1, value='PAGES BY PRIORITY').font = K.f(10, True, K.DEEP)
    for j, h in enumerate(['Priority', 'Pages']):
        cell = ws.cell(row=t2, column=1 + j, value=h)
        cell.font, cell.fill = K.f(10, True, 'FFFFFF'), K.HEAD_F
    for i, p in enumerate(['P1: refresh now', 'P2: this month', 'P3: this quarter', 'P4: later', 'Monitor']):
        r = t2 + 1 + i
        ws.cell(row=r, column=1, value=p).border = K.BORDER
        cell = ws.cell(row=r, column=2, value=f'=COUNTIF({pr},A{r})')
        cell.border, cell.fill = K.BORDER, K.FORMULA_FILL
    chart(ws, 'Clicks lost by diagnosis', 'Clicks lost', 1, [4], top + 1, last, 'G17', ['E07A5F'], True, False, h=9, w=17)
    chart(ws, 'Pages by priority', 'Pages', 1, [2], t2 + 1, t2 + 5, 'G36', [K.GREEN], False, False, w=17)
    return ws, top, t2


def build(path, asset, url):
    wb = K.new_book()
    inventory_sheet(wb)
    queue_sheet(wb)
    playbook_sheet(wb)
    dashboard_sheet(wb)
    settings_sheet(wb)
    K.prompts_sheet(wb, asset['prompts'], url)
    K.checklist_sheet(wb, list(asset['checklist']))
    K.sources_sheet(wb, asset['sources'], [
        ('Demo data', 'Roamly and every URL in the demo are fictional (.example domain). All clicks, impressions, positions, conversions and dates are illustrative, not real data.', ''),
        ('Diagnosis rules, weights, hours and recovery', 'The decay thresholds, score weights, position bands, review windows, hours per refresh type and recovery shares are assumptions of this kit. Google publishes no such numbers. Tune them on Settings and replace the recovery shares with your own results.', ''),
        ('Dates', 'Google asks whether you change the date of pages to make them seem fresh when the content has not substantially changed, and says adding or removing lots of content to seem fresh will not help rankings.', 'https://developers.google.com/search/docs/fundamentals/creating-helpful-content'),
        ('Byline dates', 'Google recommends a visible date labelled Published or Last updated, matching datePublished and dateModified in Article structured data.', 'https://developers.google.com/search/docs/appearance/publication-dates'),
        ('AI assistants and freshness', 'An Ahrefs study of about 17 million citations (July 2025) found URLs cited by AI assistants were on average 25.7 percent fresher than organic search results, with ChatGPT showing the strongest preference and Google AI Overviews the least.', 'https://ahrefs.com/blog/do-ai-assistants-prefer-to-cite-fresh-content/'),
    ])
    K.start_here(
        wb, 'Content Refresh Kit',
        [
            'This workbook finds the pages that are losing traffic, explains why, and tells you which to refresh first. Paste Search Console data for two periods and every URL gets a diagnosis: ranking decay, CTR decay, CTR decay under an AI Overview, demand decay, low traffic, growing or stable.',
            f'Each page gets a refresh type, a score from 0 to 100, a priority, an hours estimate and a brief for the writer. The Refresh Queue plans the work by week and measures the result 28 days later. A worked demo for a fictional travel app ({len(PAGES)} pages, {len(QUEUE)} refreshes) shows every formula working.',
        ],
        [
            ('Content Inventory', 'One row per URL, 500 rows ready. Changes, CTR, months since update, review due, diagnosis, refresh type, query overlap, score, priority, hours and clicks recovered.'),
            ('Refresh Queue', 'Plan refreshes by week, get a brief for the writer, apply the date rule and measure results, with a weekly hours check.'),
            ('Refresh Playbook', 'What each diagnosis means, what to check, what to change and what not to do, plus the steps for every refresh.'),
            ('Dashboard', '17 key numbers, top 10 refresh candidates, pages by diagnosis and by priority, with two charts.'),
            ('Settings', 'Diagnosis rules, score weights, position bands, review windows, refresh types with hours and recovery assumptions, and lists.'),
            ('AI Prompts', 'Prompts for ChatGPT, Claude or Gemini to diagnose pages, compare with top results and draft refreshes.'),
            ('Checklist', 'The content refresh process as a tick list with automatic progress.'),
            ('Sources', 'Where facts come from and which numbers are assumptions.'),
        ],
        [
            'Look at the demo on Content Inventory, Refresh Queue and the Dashboard. Then clear the yellow demo cells on Content Inventory and Refresh Queue.',
            'On Settings, set today\'s date, the two period labels, your writing hours per week and the clicks lost that earn full marks (about the monthly clicks of a strong page on your site).',
            'In Search Console, export pages for the previous and the recent period (same length). Paste clicks, impressions and position, plus the dates, type and main query.',
            'Choose business value, time sensitivity and whether an AI Overview shows for the main query.',
            'Sort by Refresh score. Read the Diagnosis, What to do and Query overlap columns for the top pages.',
            'Add P1 and P2 pages to the Refresh Queue, give the brief to the writer and keep the weekly hours within capacity.',
            'After each refresh, fill the date, whether the change was substantial and clicks 28 days before and after. Repeat every month or quarter.',
        ],
        url,
    )
    order = ['Start Here', 'Content Inventory', 'Refresh Queue', 'Refresh Playbook', 'Dashboard', 'Settings', 'AI Prompts', 'Checklist', 'Sources']
    wb._sheets = [wb[n] for n in order]
    wb.active = 0
    for ws in wb.worksheets:
        ws.sheet_properties.tabColor = K.GREEN if ws.title in order[:5] else 'A6EF39'
    wb.save(path)


PREVIEW = {'sheet': 'Content Inventory', 'header_row': 4, 'rows': 12,
           'cols': [2, 8, 9, len(CI_IN) + 1, len(CI_IN) + 10, len(CI_IN) + 11, len(CI_IN) + 15, len(CI_IN) + 16],
           'formula_idx': [3, 4, 5, 6, 7]}


def check(wb):
    """Assert the worked examples used in the guide."""
    a = wb['Content Inventory']
    v = lambda h, r: a[f'{CC[h]}{r}'].value
    out = {}
    for r in range(CI_FIRST, CI_FIRST + len(PAGES)):
        out[r - CI_FIRST + 1] = (v('Diagnosis', r), v('Refresh score (0 to 100)', r), v('Priority', r), v('Refresh type', r), v('Review due?', r), v('Query overlap', r), v('Est. clicks recovered (assumption)', r))
    r = 5   # Schengen visa checklist
    assert v('Click change', r) == -1900 and abs(v('Click change %', r) - (-1900 / 4200)) < 1e-9
    assert abs(v('Impression change %', r) - (-37000 / 98000)) < 1e-9 and abs(v('Positions lost', r) - 4.6) < 1e-9
    assert v('Months since update', r) == 22.3 and v('Review due?', r) == 'Yes', v('Months since update', r)
    assert v('Diagnosis', r) == 'Ranking decay' and v('Refresh type', r) == 'Full refresh'
    assert v('Refresh score (0 to 100)', r) == 98 and v('Priority', r) == 'P1: refresh now', v('Refresh score (0 to 100)', r)
    assert v('Est. clicks recovered (assumption)', r) == 950 and v('Clicks recovered per hour', r) == 158
    assert v('Query overlap', r) == 'Shares its main query with 1 other URL'
    assert out[2][0] == 'CTR decay (AI Overview)' and out[4][0] == 'Demand decay' and out[8][0] == 'Growing' and out[9][0] == 'Low traffic', (out[2], out[4], out[8], out[9])
    assert out[11][0] == 'CTR decay' and out[11][1] == 59 and out[11][2] == 'P2: this month', out[11]
    assert out[7][0] == 'Stable, review due' and out[7][3] == 'Fact check', out[7]
    assert out[12][2] == 'Monitor' and out[23][0] == 'Stable' and out[23][4] == 'No', (out[12], out[23])
    q = wb['Refresh Queue']
    assert q['T5'].value == 'Not refreshed yet' and q['L9'].value == 'Merge or improve' and q['M9'].value == 4
    assert q['T12'].value == 'Up 20%: keep going' and q['T13'].value == 'Wait: 14 days left' and q['T14'].value == 'Flat: check rankings by query', (q['T12'].value, q['T13'].value, q['T14'].value)
    assert q['Q12'].value.startswith('Update the visible') and q['Q13'].value.startswith('Keep the old date')
    assert q['W6'].value == 15 and q['Y6'].value == 'Over capacity by 3 hours' and q['W7'].value == 7 and q['W8'].value == 8, (q['W6'].value, q['W7'].value, q['W8'].value)
    dsh = wb['Dashboard']
    vals = {dsh.cell(row=r, column=1).value: dsh.cell(row=r, column=2).value for r in range(5, 22)}
    assert vals['URLs tracked'] == len(PAGES) and dsh['D6'].value == PAGES[0][1], (vals, dsh['D6'].value)
    return out, vals
