"""Topic Clusters Kit workbook (asset 03).

Cluster Map: one row per page (pillar, cluster or supporting). Pillars: one row per topic with an automatic
Cluster Health Score. Fan Out Questions: the sub questions an AI answer or a curious reader would ask, checked
against your pages. Link Plan: every internal link task with anchor and URL checks.
"""
from openpyxl.styles import PatternFill, Font
from openpyxl.formatting.rule import CellIsRule, ColorScaleRule, FormulaRule
from openpyxl.chart import BarChart, Reference
from openpyxl.utils import get_column_letter as L
import kitlib as K

FIRST, LAST = 5, 504        # Cluster Map
P_FIRST, P_LAST = 5, 54     # Pillars
FO_FIRST, FO_LAST = 5, 304  # Fan Out Questions
LP_FIRST, LP_LAST = 5, 304  # Link Plan
S = 'Settings'
CM = "'Cluster Map'"
FO = "'Fan Out Questions'"

# Demo data: HireHive, a fictional HR software company for small businesses in India. Illustrative numbers only.
PILLARS = [
    # name, url, keyword, goal, target pages, owner, notes
    ('Employee onboarding', '/employee-onboarding/', 'employee onboarding', 'Sign ups', 10, 'Priya', 'Our strongest product fit'),
    ('Performance reviews', '/performance-reviews/', 'performance review', 'Leads', 8, 'Arjun', ''),
    ('Leave policy', '/leave-policy/', 'leave policy', 'Sign ups', 8, 'Priya', 'Many India specific questions'),
]
# pillar, role, title, url, keyword, subtopic, intent, vol, kd, value, aio, status, up, from_pillar, siblings, clicks, impressions, owner
PAGES = [
    ('Employee onboarding', 'Pillar', 'Employee Onboarding: The Complete Guide for Small Teams', '/employee-onboarding/', 'employee onboarding', 'What onboarding is and how to run it end to end', 'Informational', 6600, 52, 3, 'Yes', 'Live', '', '', 3, 410, 18200, 'Priya'),
    ('Employee onboarding', 'Cluster', 'Employee Onboarding Checklist (Free Download)', '/templates/onboarding-checklist/', 'employee onboarding checklist', 'What to do before day one and in week one', 'Transactional', 2900, 31, 3, 'No', 'Live', 'Yes', 'Yes', 2, 260, 5400, 'Priya'),
    ('Employee onboarding', 'Cluster', 'The Only Employee Onboarding Checklist You Need', '/blog/employee-onboarding-checklist/', 'employee onboarding checklist', 'Same checklist as a blog post', 'Informational', 2900, 31, 2, 'Yes', 'Live', 'Yes', 'No', 0, 35, 4100, 'Rohan'),
    ('Employee onboarding', 'Cluster', '30 60 90 Day Onboarding Plan Template', '/templates/30-60-90-day-plan/', '30 60 90 day plan', 'Goals for the first three months', 'Transactional', 4400, 38, 3, 'No', 'Live', 'Yes', 'Yes', 1, 300, 9800, 'Priya'),
    ('Employee onboarding', 'Cluster', 'Remote Onboarding: How to Welcome New Hires Online', '/blog/remote-onboarding/', 'remote onboarding', 'Onboarding staff who work from home', 'Informational', 1300, 29, 2, 'Yes', 'Live', 'Yes', 'Yes', 1, 60, 2600, 'Rohan'),
    ('Employee onboarding', 'Cluster', 'Onboarding vs Orientation: What Is the Difference?', '/blog/onboarding-vs-orientation/', 'onboarding vs orientation', 'Difference between the two', 'Informational', 880, 18, 1, 'Yes', 'Live', 'Yes', 'Yes', 0, 22, 3900, 'Rohan'),
    ('Employee onboarding', 'Cluster', 'Welcome Email to New Employee: 12 Templates', '/templates/welcome-email/', 'welcome email to new employee', 'What to send before day one', 'Transactional', 1900, 22, 2, 'No', 'Live', 'Yes', 'Yes', 2, 15, 2400, 'Priya'),
    ('Employee onboarding', 'Cluster', 'Employee Onboarding Software for Small Business', '/features/onboarding/', 'employee onboarding software', 'Tools that automate onboarding', 'Commercial', 1600, 55, 3, 'No', 'Planned', '', '', 0, None, None, 'Priya'),
    ('Employee onboarding', 'Supporting', 'Preboarding: What to Do Before Day One', '/blog/preboarding/', 'preboarding', 'Steps between offer letter and joining', 'Informational', 480, 12, 2, 'Yes', 'Planned', '', '', 0, None, None, 'Rohan'),
    ('Performance reviews', 'Pillar', 'Performance Reviews: A Practical Guide for Managers', '/performance-reviews/', 'performance review', 'How to plan, write and hold reviews', 'Informational', 5400, 48, 3, 'Yes', 'Live', '', '', 2, 180, 12500, 'Arjun'),
    ('Performance reviews', 'Cluster', 'Performance Review Phrases: 150 Examples', '/blog/performance-review-phrases/', 'performance review phrases', 'Wording for strengths and gaps', 'Informational', 3600, 27, 2, 'Yes', 'Live', 'Yes', 'Yes', 1, 140, 7100, 'Arjun'),
    ('Performance reviews', 'Cluster', 'Self Appraisal Examples for Employees', '/blog/self-appraisal-examples/', 'self appraisal examples', 'What employees write about themselves', 'Informational', 6600, 33, 2, 'Yes', 'Live', 'Yes', 'No', 1, 210, 15800, 'Arjun'),
    ('Performance reviews', 'Cluster', 'Performance Review Template (Excel and Word)', '/templates/performance-review/', 'performance review template', 'A ready review form', 'Transactional', 2400, 30, 3, 'No', 'Writing', '', '', 0, None, None, 'Arjun'),
    ('Performance reviews', 'Cluster', '360 Degree Feedback: How It Works', '/blog/360-degree-feedback/', '360 degree feedback', 'Feedback from peers and reports', 'Informational', 2900, 41, 2, 'Yes', 'Planned', '', '', 0, None, None, 'Arjun'),
    ('Performance reviews', 'Cluster', 'Performance Management Software Compared', '/compare/performance-software/', 'performance management software', 'Choosing a tool', 'Commercial', 1900, 58, 3, 'No', 'Planned', '', '', 0, None, None, 'Arjun'),
    ('Performance reviews', 'Supporting', 'How to Give Negative Feedback Kindly', '/blog/negative-feedback/', 'how to give negative feedback', 'Hard conversations', 'Informational', 1000, 20, 1, 'Yes', 'Live', 'No', 'No', 0, 30, 1900, 'Arjun'),
    ('Leave policy', 'Pillar', 'Leave Policy: How to Write One for Your Company', '/leave-policy/', 'leave policy', 'Writing and running a leave policy', 'Informational', 2900, 35, 3, 'Yes', 'Live', '', '', 2, 95, 6100, 'Priya'),
    ('Leave policy', 'Cluster', 'Leave Policy Template for Small Businesses', '/templates/leave-policy/', 'leave policy template', 'A ready policy to adapt', 'Transactional', 1600, 24, 3, 'No', 'Live', 'Yes', 'Yes', 1, 120, 3300, 'Priya'),
    ('Leave policy', 'Cluster', 'Types of Leave in India Explained', '/blog/types-of-leave-india/', 'types of leave in india', 'Casual, sick, earned and more', 'Informational', 2400, 26, 2, 'Yes', 'Live', 'Yes', 'Yes', 1, 70, 5200, 'Rohan'),
    ('Leave policy', 'Cluster', 'Earned Leave Rules and Encashment', '/blog/earned-leave-rules/', 'earned leave rules', 'Accrual, carry forward and encashment', 'Informational', 1300, 22, 2, 'Yes', 'Update', 'Yes', 'Yes', 1, 40, 2800, 'Rohan'),
    ('Leave policy', 'Cluster', 'Free Leave Tracker Spreadsheet', '/templates/leave-tracker/', 'leave tracker', 'Track balances for a small team', 'Transactional', 1900, 28, 3, 'No', 'Planned', '', '', 0, None, None, 'Priya'),
    ('Leave policy', 'Cluster', 'Leave Management Software for Small Teams', '/features/leave-management/', 'leave management software', 'Automating requests and approvals', 'Commercial', 1000, 50, 3, 'No', 'Planned', '', '', 0, None, None, 'Priya'),
    ('Leave policy', 'Supporting', 'Leave Application Email: 10 Samples', '/blog/leave-application-email/', 'leave application email', 'Wording employees can copy', 'Informational', 8100, 20, 1, 'Yes', 'Live', 'Yes', 'Yes', 0, 160, 21000, 'Rohan'),
]
# pillar, question, type, answered by url, depth
FANOUT = [
    ('Employee onboarding', 'What is employee onboarding?', 'Definition', '/employee-onboarding/', 'Full section'),
    ('Employee onboarding', 'How long should onboarding last?', 'How to', '/employee-onboarding/', 'Full section'),
    ('Employee onboarding', 'What should be on an onboarding checklist?', 'Examples or templates', '/templates/onboarding-checklist/', 'Full section'),
    ('Employee onboarding', 'What is a 30 60 90 day plan?', 'Definition', '/templates/30-60-90-day-plan/', 'Full section'),
    ('Employee onboarding', 'How do you onboard a remote employee?', 'How to', '/blog/remote-onboarding/', 'Full section'),
    ('Employee onboarding', 'What is the difference between onboarding and orientation?', 'Comparison', '/blog/onboarding-vs-orientation/', 'Full section'),
    ('Employee onboarding', 'Which documents do new employees submit in India?', 'Rules or compliance', '/employee-onboarding/', 'Short mention'),
    ('Employee onboarding', 'What is the best onboarding software for a small business?', 'Tools or software', '/features/onboarding/', 'Full section'),
    ('Employee onboarding', 'How much does onboarding cost per employee?', 'Cost or pricing', '', ''),
    ('Employee onboarding', 'How do you measure onboarding success?', 'How to', '', ''),
    ('Performance reviews', 'How often should performance reviews happen?', 'How to', '/performance-reviews/', 'Full section'),
    ('Performance reviews', 'What should I write in a self appraisal?', 'Examples or templates', '/blog/self-appraisal-examples/', 'Full section'),
    ('Performance reviews', 'What are good phrases for a performance review?', 'Examples or templates', '/blog/performance-review-phrases/', 'Full section'),
    ('Performance reviews', 'What is 360 degree feedback?', 'Definition', '/blog/360-degree-feedback/', 'Full section'),
    ('Performance reviews', 'How do you link reviews to salary hikes?', 'How to', '', ''),
    ('Performance reviews', 'What is the alternative to annual reviews?', 'Alternatives', '/performance-reviews/', 'Short mention'),
    ('Leave policy', 'What types of leave are there in India?', 'Rules or compliance', '/blog/types-of-leave-india/', 'Full section'),
    ('Leave policy', 'Can earned leave be encashed?', 'Rules or compliance', '/blog/earned-leave-rules/', 'Full section'),
    ('Leave policy', 'How do I write a leave policy?', 'How to', '/leave-policy/', 'Full section'),
    ('Leave policy', 'How do I track employee leave in Excel?', 'Tools or software', '/templates/leave-tracker/', 'Full section'),
    ('Leave policy', 'How do I write a leave application email?', 'Examples or templates', '/blog/leave-application-email/', 'Full section'),
    ('Leave policy', 'What is a comp off?', 'Definition', '', ''),
]
# from, to, anchor, type, placed
LINKS = [
    ('/blog/employee-onboarding-checklist/', '/employee-onboarding/', 'employee onboarding guide', 'Cluster to pillar', 'Yes'),
    ('/employee-onboarding/', '/blog/employee-onboarding-checklist/', 'click here', 'Pillar to cluster', 'No'),
    ('/employee-onboarding/', '/blog/preboarding/', 'preboarding steps', 'Pillar to cluster', 'No'),
    ('/blog/onboarding-vs-orientation/', '/blog/remote-onboarding/', 'remote onboarding tips', 'Cluster to cluster', 'No'),
    ('/blog/negative-feedback/', '/performance-reviews/', 'performance review guide for managers', 'Cluster to pillar', 'No'),
    ('/performance-reviews/', '/blog/negative-feedback/', 'read more', 'Pillar to cluster', 'No'),
    ('/performance-reviews/', '/blog/self-appraisal-examples/', 'self appraisal examples', 'Pillar to cluster', 'No'),
    ('/blog/performance-review-phrases/', '/blog/self-appraisal-examples/', 'self appraisal examples for employees', 'Cluster to cluster', 'No'),
    ('/blog/types-of-leave-india/', '/blog/earned-leave-rules/', 'earned leave rules and encashment', 'Cluster to cluster', 'Yes'),
    ('/leave-policy/', '/templates/leave-tracker/', 'leave tracker spreadsheet', 'Pillar to cluster', 'No'),
    ('/blog/remote-onboarding/', '/blog/remote-onboarding/', 'remote onboarding', 'Cluster to cluster', 'No'),
    ('/templates/welcome-email/', '/blog/preboarding/', 'what to do before a new employee joins your company on the very first day', 'Cluster to cluster', 'No'),
    ('/blog/leave-application-email/', '/leave-policy/', 'leave policy', 'Cluster to pillar', 'Yes'),
    ('/templates/30-60-90-day-plan/', '/templates/onboarding-checklist/', 'onboarding checklist', 'Cluster to cluster', 'Yes'),
    ('/blog/onboarding-vs-orientation/', '/employee-onboarding/', 'onboarding', 'Cluster to pillar', 'Yes'),
    ('/blog/welcome-emails/', '/employee-onboarding/', 'employee onboarding process', 'Cluster to pillar', 'No'),
]

HEAD = ['Pillar', 'Page role', 'Page title', 'URL', 'Primary keyword', 'Subtopic or question it answers', 'Search intent',
        'Monthly volume', 'KD (0 to 100)', 'Business value (1 to 3)', 'AI Overview?', 'Status', 'Links up to pillar?',
        'Linked from pillar?', 'Sibling links in', 'Clicks (28 days)', 'Impressions (28 days)',
        'Pillar URL', 'Link health', 'Keyword overlap', 'Build score (0 to 100)', 'Build priority', 'CTR (28 days)',
        'Next action', 'Suggested anchor text', 'Owner', 'Publish or update date', 'Notes']
FCOLS = tuple(range(18, 26))
WIDTHS = [20, 11, 42, 34, 28, 32, 14, 10, 9, 10, 10, 10, 10, 10, 9, 10, 11, 24, 20, 22, 11, 10, 9, 34, 28, 10, 13, 26]


def settings_sheet(wb):
    ws = wb.create_sheet(S)
    ws.sheet_view.showGridLines = False
    K.title_block(ws, 'Settings', 'Every weight, threshold and list used by this workbook. Change a blue number and every score updates.')
    for c, w in zip('ABCDEFGHIJKLMNOP', [50, 13, 3, 24, 10, 3, 14, 15, 13, 9, 22, 18, 13, 16, 15, 3]):
        ws.column_dimensions[c].width = w
    rows = [
        (4, 'YOUR SITE', None, None),
        (5, 'Site stage', 'Growing site', None),
        (6, 'Comfortable keyword difficulty (auto)', '=VLOOKUP(B5,D5:E7,2,FALSE)', '0'),
        (7, 'Ease reaches zero this many KD points above comfortable', 40, '0'),
        (8, 'Volume that earns full volume points', 10000, '#,##0'),
        (10, 'BUILD SCORE WEIGHTS (any numbers, they are scaled)', None, None),
        (11, 'Volume weight', 35, '0'),
        (12, 'Ease weight', 25, '0'),
        (13, 'Business value weight', 40, '0'),
        (14, 'Total (auto)', '=SUM(B11:B13)', '0'),
        (16, 'BUILD PRIORITY', None, None),
        (17, 'P1 when build score is at least', 85, '0'),
        (18, 'P2 when build score is at least (below = P3)', 70, '0'),
        (20, 'CLUSTER HEALTH WEIGHTS', None, None),
        (21, 'Coverage (live cluster pages vs target)', 35, '0'),
        (22, 'Two way links (live cluster pages linked up and down)', 30, '0'),
        (23, 'Fan out coverage (questions answered)', 25, '0'),
        (24, 'No keyword overlap', 10, '0'),
        (25, 'Total (auto)', '=SUM(B21:B24)', '0'),
        (27, 'HEALTH BANDS', None, None),
        (28, 'Strong when health is at least', 75, '0'),
        (29, 'Growing when health is at least (below = Thin)', 50, '0'),
        (31, 'NEXT MOVE TRIGGERS', None, None),
        (32, 'Publish more pages when coverage is below', 0.5, '0%'),
        (33, 'Fix links when two way links are below', 0.8, '0%'),
        (34, 'Answer questions when fan out coverage is below', 0.7, '0%'),
        (36, 'LINK AND CTR CHECKS', None, None),
        (37, 'Minimum sibling links into each cluster page', 1, '0'),
        (38, 'Low CTR when below', 0.01, '0.0%'),
        (39, 'Only judge CTR from this many impressions', 100, '#,##0'),
        (40, 'Most words allowed in anchor text', 8, '0'),
    ]
    for r, label, val, fmt in rows:
        a = ws.cell(row=r, column=1, value=label)
        a.font = K.f(10, val is None, K.DEEP if val is None else K.INK)
        if val is not None:
            c = ws.cell(row=r, column=2, value=val)
            c.border = K.BORDER
            is_f = isinstance(val, str) and val.startswith('=')
            c.fill = K.FORMULA_FILL if is_f else K.INPUT_FILL
            c.font = K.f(10, True, K.INK if is_f or r == 5 else '0000FF')
            if fmt:
                c.number_format = fmt
    ws['A42'] = 'All weights and thresholds are starter assumptions chosen for this kit, not Google rules. Tune them to your site.'
    ws['A42'].font = K.f(9, False, '777777', True)
    ws['D4'] = 'COMFORTABLE KD BY SITE STAGE'
    ws['D4'].font = K.f(10, True, K.DEEP)
    for i, (k, v) in enumerate([('New site', 15), ('Growing site', 30), ('Established site', 50)]):
        ws.cell(row=5 + i, column=4, value=k).fill = K.INPUT_FILL
        c = ws.cell(row=5 + i, column=5, value=v)
        c.fill = K.INPUT_FILL
        c.font = K.f(10, False, '0000FF')
    ws['D10'] = 'GENERIC ANCHORS TO AVOID'
    ws['D10'].font = K.f(10, True, K.DEEP)
    generic = ['click here', 'read more', 'learn more', 'here', 'this page', 'this article', 'more', 'link', 'website',
               'see more', 'continue reading', 'this', 'check it out', 'find out more']
    for i in range(20):
        c = ws.cell(row=11 + i, column=4, value=generic[i] if i < len(generic) else None)
        c.fill = K.INPUT_FILL
        c.border = K.BORDER
    ws['G4'] = 'DROPDOWN LISTS'
    ws['G4'].font = K.f(10, True, K.DEEP)
    lists = {
        'G': ['Page role', 'Pillar', 'Cluster', 'Supporting'],
        'H': ['Intent', 'Informational', 'Commercial', 'Transactional', 'Navigational'],
        'I': ['Status', 'Planned', 'Writing', 'Live', 'Update', 'Merge'],
        'J': ['Yes/No', 'Yes', 'No'],
        'K': ['Question type', 'Definition', 'How to', 'Comparison', 'Cost or pricing', 'Problem or fix', 'Examples or templates', 'Tools or software', 'Rules or compliance', 'Alternatives'],
        'L': ['Link type', 'Cluster to pillar', 'Pillar to cluster', 'Cluster to cluster', 'Other'],
        'M': ['Goal', 'Leads', 'Sales', 'Sign ups', 'Authority'],
        'N': ['Site stage', 'New site', 'Growing site', 'Established site'],
        'O': ['Answer depth', 'Full section', 'Short mention'],
    }
    for c, vals in lists.items():
        for i, v in enumerate(vals):
            cell = ws[f'{c}{5 + i}']
            cell.value = v
            cell.font = K.f(9, i == 0, '555555')
    K.dropdown(ws, 'B5', f'{S}!$N$6:$N$8')
    return ws


def cm(c):
    return f'{CM}!${c}${FIRST}:${c}${LAST}'


def fo(c):
    return f'{FO}!${c}${FO_FIRST}:${c}${FO_LAST}'


def live_count(url_cell):
    """Pages in Cluster Map with this URL that are live (Live or Update)."""
    return f'(COUNTIFS({cm("D")},{url_cell},{cm("L")},"Live")+COUNTIFS({cm("D")},{url_cell},{cm("L")},"Update"))'


def cluster_sheet(wb):
    ws = wb.create_sheet('Cluster Map')
    ws.sheet_view.showGridLines = False
    K.title_block(ws, 'Cluster map', 'Rows 5 to 27 hold DEMO data for HireHive, a fictional HR software company (illustrative numbers). Select the yellow demo cells and press Delete to start your own map. Grey formula columns stay.')
    ws['A2'].font = K.f(10, True, 'B45309')
    ws['A3'] = 'One row per page. Add each pillar on the Pillars tab first, then list its pillar page, cluster pages and supporting pages here. 500 rows ready.'
    ws['A3'].font = K.f(9, False, '666666', True)
    K.header_row(ws, 4, HEAD, formula_cols=FCOLS, widths=WIDTHS)
    for r in range(FIRST, LAST + 1):
        i = r - FIRST
        if i < len(PAGES):
            d = PAGES[i]
            for c, v in zip(list(range(1, 18)) + [26], d):
                if v is not None and v != '':
                    ws.cell(row=r, column=c, value=v)
        live = f'OR(L{r}="Live",L{r}="Update")'
        ws.cell(row=r, column=18, value=f'=IF(C{r}="","",IF(B{r}="Pillar",D{r},IFERROR(VLOOKUP(A{r},Pillars!$A${P_FIRST}:$B${P_LAST},2,FALSE),"Add pillar on Pillars tab")))')
        ws.cell(row=r, column=19, value=(
            f'=IF(C{r}="","",IF(B{r}="Pillar","Pillar hub",IF(NOT({live}),"Link when live",'
            f'IF(AND(M{r}="Yes",N{r}="Yes"),IF(N(O{r})>={S}!$B$37,"OK","Add sibling links"),'
            f'IF(AND(M{r}<>"Yes",N{r}<>"Yes",N(O{r})=0),"Orphan risk",IF(M{r}<>"Yes","Add link up to pillar","Add link from pillar"))))))'))
        ws.cell(row=r, column=20, value=f'=IF(E{r}="","",IF(COUNTIF($E${FIRST}:$E${LAST},E{r})>1,"Same keyword as another page","OK"))')
        ws.cell(row=r, column=21, value=(
            f'=IF(C{r}="","",ROUND(100*({S}!$B$11*MIN(1,LOG10(N(H{r})+1)/LOG10({S}!$B$8+1))'
            f'+{S}!$B$12*IF(N(I{r})<={S}!$B$6,1,MAX(0,1-(N(I{r})-{S}!$B$6)/{S}!$B$7))'
            f'+{S}!$B$13*N(J{r})/3)/{S}!$B$14,0))'))
        ws.cell(row=r, column=22, value=f'=IF(U{r}="","",IF(U{r}>={S}!$B$17,"P1",IF(U{r}>={S}!$B$18,"P2","P3")))')
        ws.cell(row=r, column=23, value=f'=IF(N(Q{r})>0,N(P{r})/Q{r},"")')
        ws.cell(row=r, column=24, value=(
            f'=IF(C{r}="","",IF(L{r}="Planned","Brief and write ("&V{r}&")",IF(L{r}="Writing","Finish, then link both ways",'
            f'IF(L{r}="Merge","Merge into the stronger page and 301 redirect",IF(L{r}="Update","Refresh facts, examples and links",'
            f'IF(T{r}="Same keyword as another page","Fix overlap: one page per keyword",'
            f'IF(AND(S{r}<>"OK",S{r}<>"Pillar hub"),S{r},'
            f'IF(N(Q{r})>={S}!$B$39,IF(N(P{r})/Q{r}<{S}!$B$38,"Rewrite title and intro (low CTR)","Monitor monthly"),"Monitor monthly"))))))))'))
        ws.cell(row=r, column=25, value=f'=IF(C{r}="","",IF(E{r}="",C{r},E{r}))')
    K.style_body(ws, FIRST, LAST, len(HEAD), formula_cols=FCOLS,
                 number_formats={8: '#,##0', 16: '#,##0', 17: '#,##0', 21: '0', 23: '0.0%', 27: 'dd mmm yyyy'}, wrap_cols=(3, 6, 24, 28))
    ws.freeze_panes = 'D5'
    ws.auto_filter.ref = f'A4:{L(len(HEAD))}{LAST}'
    K.dropdown(ws, f'A{FIRST}:A{LAST}', f'Pillars!$A${P_FIRST}:$A${P_LAST}', 'Pick a pillar from the Pillars tab')
    K.dropdown(ws, f'B{FIRST}:B{LAST}', f'{S}!$G$6:$G$8')
    K.dropdown(ws, f'G{FIRST}:G{LAST}', f'{S}!$H$6:$H$9')
    K.dropdown(ws, f'J{FIRST}:J{LAST}', '"1,2,3"', '3 = close to a sale or lead, 2 = builds trust, 1 = loosely related')
    K.dropdown(ws, f'K{FIRST}:K{LAST}', f'{S}!$J$6:$J$7')
    K.dropdown(ws, f'L{FIRST}:L{LAST}', f'{S}!$I$6:$I$10')
    K.dropdown(ws, f'M{FIRST}:N{LAST}', f'{S}!$J$6:$J$7')
    K.whole_number(ws, f'I{FIRST}:I{LAST}', 0, 100, 'Keyword difficulty must be between 0 and 100.')
    K.whole_number(ws, f'O{FIRST}:O{LAST}', 0, 500, 'Number of links from other pages in the same cluster.')
    s_rng = f'S{FIRST}:S{LAST}'
    ws.conditional_formatting.add(s_rng, CellIsRule(operator='equal', formula=['"OK"'], fill=PatternFill('solid', fgColor='D9F2C4')))
    ws.conditional_formatting.add(s_rng, CellIsRule(operator='equal', formula=['"Orphan risk"'], fill=PatternFill('solid', fgColor='F8D7D3'), font=Font(name=K.FONT, bold=True, color='9B2C1F')))
    ws.conditional_formatting.add(s_rng, FormulaRule(formula=[f'LEFT(S{FIRST},4)="Add "'], fill=PatternFill('solid', fgColor='FFE8B3')))
    ws.conditional_formatting.add(f'T{FIRST}:T{LAST}', CellIsRule(operator='equal', formula=['"Same keyword as another page"'], font=Font(name=K.FONT, bold=True, color='C0392B'), fill=PatternFill('solid', fgColor='F8D7D3')))
    v_rng = f'V{FIRST}:V{LAST}'
    ws.conditional_formatting.add(v_rng, CellIsRule(operator='equal', formula=['"P1"'], fill=PatternFill('solid', fgColor='9BE07A'), font=Font(name=K.FONT, bold=True)))
    ws.conditional_formatting.add(v_rng, CellIsRule(operator='equal', formula=['"P2"'], fill=PatternFill('solid', fgColor='D9F2C4')))
    ws.conditional_formatting.add(v_rng, CellIsRule(operator='equal', formula=['"P3"'], fill=PatternFill('solid', fgColor='FFE8B3')))
    ws.conditional_formatting.add(f'U{FIRST}:U{LAST}', ColorScaleRule(start_type='num', start_value=0, start_color='F8D7D3', mid_type='num', mid_value=50, mid_color='FFF4CC', end_type='num', end_value=100, end_color='B7E4A0'))
    ws.conditional_formatting.add(f'B{FIRST}:B{LAST}', CellIsRule(operator='equal', formula=['"Pillar"'], font=Font(name=K.FONT, bold=True, color=K.DEEP)))
    return ws


def pillars_sheet(wb):
    ws = wb.create_sheet('Pillars')
    ws.sheet_view.showGridLines = False
    K.title_block(ws, 'Pillars and cluster health', 'One row per pillar topic. Type the yellow cells. Grey columns score each cluster from the Cluster Map and Fan Out Questions tabs.')
    head = ['Pillar name', 'Pillar URL', 'Pillar keyword', 'Business goal', 'Target cluster pages', 'Owner',
            'Pages in map', 'Live cluster pages', 'Coverage', 'Two way links', 'Keyword overlaps', 'Fan out coverage',
            'Combined volume', 'Clicks (28 days)', 'Cluster health (0 to 100)', 'Health band', 'Next move', 'Notes']
    fc = tuple(range(7, 18))
    K.header_row(ws, 4, head, formula_cols=fc, widths=[22, 26, 22, 13, 11, 10, 9, 10, 10, 10, 10, 10, 11, 10, 11, 11, 36, 28])
    nonp = f'{cm("B")},"<>Pillar"'
    for r in range(P_FIRST, P_LAST + 1):
        i = r - P_FIRST
        if i < len(PILLARS):
            for c, v in zip((1, 2, 3, 4, 5, 6, 18), PILLARS[i]):
                if v != '':
                    ws.cell(row=r, column=c, value=v)
        a = f'$A{r}'
        lc = (f'(COUNTIFS({cm("A")},{a},{nonp},{cm("L")},"Live")+COUNTIFS({cm("A")},{a},{nonp},{cm("L")},"Update"))')
        tw = (f'(COUNTIFS({cm("A")},{a},{nonp},{cm("L")},"Live",{cm("M")},"Yes",{cm("N")},"Yes")'
              f'+COUNTIFS({cm("A")},{a},{nonp},{cm("L")},"Update",{cm("M")},"Yes",{cm("N")},"Yes"))')
        ws.cell(row=r, column=7, value=f'=IF(A{r}="","",COUNTIF({cm("A")},{a}))')
        ws.cell(row=r, column=8, value=f'=IF(A{r}="","",{lc})')
        ws.cell(row=r, column=9, value=f'=IF(A{r}="","",IF(N(E{r})>0,MIN(1,H{r}/E{r}),0))')
        ws.cell(row=r, column=10, value=f'=IF(A{r}="","",IF(N(H{r})=0,0,{tw}/H{r}))')
        ws.cell(row=r, column=11, value=f'=IF(A{r}="","",COUNTIFS({cm("A")},{a},{cm("T")},"Same keyword as another page"))')
        ws.cell(row=r, column=12, value=f'=IF(A{r}="","",IFERROR(COUNTIFS({fo("A")},{a},{fo("F")},"Covered")/COUNTIFS({fo("A")},{a},{fo("B")},"<>"),0))')
        ws.cell(row=r, column=13, value=f'=IF(A{r}="","",SUMIF({cm("A")},{a},{cm("H")}))')
        ws.cell(row=r, column=14, value=f'=IF(A{r}="","",SUMIF({cm("A")},{a},{cm("P")}))')
        ws.cell(row=r, column=15, value=(
            f'=IF(A{r}="","",ROUND(100*({S}!$B$21*I{r}+{S}!$B$22*J{r}+{S}!$B$23*L{r}'
            f'+{S}!$B$24*MAX(0,1-K{r}/MAX(1,G{r})))/{S}!$B$25,0))'))
        ws.cell(row=r, column=16, value=f'=IF(A{r}="","",IF(O{r}>={S}!$B$28,"Strong",IF(O{r}>={S}!$B$29,"Growing","Thin")))')
        ws.cell(row=r, column=17, value=(
            f'=IF(A{r}="","",IF(N(G{r})=0,"Add pages to the Cluster Map",IF(I{r}<{S}!$B$32,"Publish more cluster pages",'
            f'IF(J{r}<{S}!$B$33,"Fix missing links up and down",IF(L{r}<{S}!$B$34,"Answer the open fan out questions",'
            f'IF(K{r}>0,"Resolve keyword overlaps","Refresh and expand the strongest pages"))))))'))
    K.style_body(ws, P_FIRST, P_LAST, len(head), formula_cols=fc,
                 number_formats={5: '0', 9: '0%', 10: '0%', 12: '0%', 13: '#,##0', 14: '#,##0', 15: '0'}, wrap_cols=(17, 18))
    K.dropdown(ws, f'D{P_FIRST}:D{P_LAST}', f'{S}!$M$6:$M$9')
    K.whole_number(ws, f'E{P_FIRST}:E{P_LAST}', 1, 200, 'How many cluster pages this pillar should have.')
    band = f'P{P_FIRST}:P{P_LAST}'
    ws.conditional_formatting.add(band, CellIsRule(operator='equal', formula=['"Strong"'], fill=PatternFill('solid', fgColor='9BE07A'), font=Font(name=K.FONT, bold=True)))
    ws.conditional_formatting.add(band, CellIsRule(operator='equal', formula=['"Growing"'], fill=PatternFill('solid', fgColor='FFF4CC')))
    ws.conditional_formatting.add(band, CellIsRule(operator='equal', formula=['"Thin"'], fill=PatternFill('solid', fgColor='F8D7D3')))
    ws.conditional_formatting.add(f'O{P_FIRST}:O{P_LAST}', ColorScaleRule(start_type='num', start_value=0, start_color='F8D7D3', mid_type='num', mid_value=50, mid_color='FFF4CC', end_type='num', end_value=100, end_color='B7E4A0'))
    ws.freeze_panes = 'B5'
    return ws


def fanout_sheet(wb):
    ws = wb.create_sheet('Fan Out Questions')
    ws.sheet_view.showGridLines = False
    K.title_block(ws, 'Fan out questions', 'The follow up questions a reader, or an AI answer that runs several related searches, would ask about each pillar. Map each one to the page that answers it.')
    head = ['Pillar', 'Question', 'Question type', 'Answered by URL', 'Answer depth', 'Coverage', 'Suggested fix', 'Notes']
    K.header_row(ws, 4, head, formula_cols=(6, 7), widths=[22, 56, 20, 34, 14, 18, 52, 26])
    for r in range(FO_FIRST, FO_LAST + 1):
        i = r - FO_FIRST
        if i < len(FANOUT):
            for c, v in enumerate(FANOUT[i], 1):
                if v:
                    ws.cell(row=r, column=c, value=v)
        ws.cell(row=r, column=6, value=(
            f'=IF(B{r}="","",IF(D{r}="","Gap",IF({live_count(f"D{r}")}>0,IF(E{r}="Short mention","Thin answer","Covered"),'
            f'IF(COUNTIF({cm("D")},D{r})>0,"Planned","URL not in Cluster Map"))))'))
        ws.cell(row=r, column=7, value=(
            f'=IF(F{r}="","",IF(F{r}="Gap","Answer it in a section of the pillar, or plan a cluster page if it needs a full guide",'
            f'IF(F{r}="Thin answer","Expand the short mention into a full, self contained answer",'
            f'IF(F{r}="Planned","Add this question to the brief of the planned page",'
            f'IF(F{r}="URL not in Cluster Map","Add the page to the Cluster Map or fix the URL","Keep the answer accurate and current")))))'))
    K.style_body(ws, FO_FIRST, FO_LAST, len(head), formula_cols=(6, 7), wrap_cols=(2, 7, 8))
    K.dropdown(ws, f'A{FO_FIRST}:A{FO_LAST}', f'Pillars!$A${P_FIRST}:$A${P_LAST}')
    K.dropdown(ws, f'C{FO_FIRST}:C{FO_LAST}', f'{S}!$K$6:$K$14')
    K.dropdown(ws, f'E{FO_FIRST}:E{FO_LAST}', f'{S}!$O$6:$O$7')
    rng = f'F{FO_FIRST}:F{FO_LAST}'
    ws.conditional_formatting.add(rng, CellIsRule(operator='equal', formula=['"Covered"'], fill=PatternFill('solid', fgColor='D9F2C4')))
    ws.conditional_formatting.add(rng, CellIsRule(operator='equal', formula=['"Gap"'], fill=PatternFill('solid', fgColor='F8D7D3'), font=Font(name=K.FONT, bold=True, color='9B2C1F')))
    ws.conditional_formatting.add(rng, CellIsRule(operator='equal', formula=['"Thin answer"'], fill=PatternFill('solid', fgColor='FFE8B3')))
    ws.conditional_formatting.add(rng, CellIsRule(operator='equal', formula=['"Planned"'], fill=PatternFill('solid', fgColor='DCEBFF')))
    ws.freeze_panes = 'C5'
    ws.auto_filter.ref = f'A4:H{FO_LAST}'
    return ws


def links_sheet(wb):
    ws = wb.create_sheet('Link Plan')
    ws.sheet_view.showGridLines = False
    K.title_block(ws, 'Internal link plan', 'One row per link you will add. The grey columns check the anchor text and both URLs against the Cluster Map before you place the link.')
    head = ['From URL', 'To URL', 'Anchor text', 'Link type', 'Placed?', 'Anchor words', 'Anchor check', 'URL check', 'Status', 'Owner', 'Notes']
    fc = (6, 7, 8, 9)
    K.header_row(ws, 4, head, formula_cols=fc, widths=[34, 34, 40, 18, 9, 9, 20, 24, 18, 10, 28])
    for r in range(LP_FIRST, LP_LAST + 1):
        i = r - LP_FIRST
        if i < len(LINKS):
            for c, v in enumerate(LINKS[i], 1):
                ws.cell(row=r, column=c, value=v)
        ws.cell(row=r, column=6, value=f'=IF(TRIM(C{r})="","",LEN(TRIM(C{r}))-LEN(SUBSTITUTE(TRIM(C{r})," ",""))+1)')
        ws.cell(row=r, column=7, value=(
            f'=IF(TRIM(C{r})="","",IF(COUNTIF({S}!$D$11:$D$30,TRIM(C{r}))>0,"Generic, rewrite",'
            f'IF(F{r}>{S}!$B$40,"Too long, tighten",IF(F{r}<2,"One word, add context","OK"))))'))
        ws.cell(row=r, column=8, value=(
            f'=IF(OR(A{r}="",B{r}=""),"",IF(A{r}=B{r},"Self link, remove",IF(COUNTIF({cm("D")},A{r})=0,"From URL not in Cluster Map",'
            f'IF(COUNTIF({cm("D")},B{r})=0,"To URL not in Cluster Map",IF({live_count(f"B{r}")}=0,"Target not live yet","OK")))))'))
        ws.cell(row=r, column=9, value=(
            f'=IF(A{r}="","",IF(E{r}="Yes",IF(G{r}="OK","Done","Done, but fix the anchor"),'
            f'IF(G{r}<>"OK","Fix first",IF(H{r}="OK","Ready to place",IF(H{r}="Target not live yet","Wait for target","Fix first")))))'))
    K.style_body(ws, LP_FIRST, LP_LAST, len(head), formula_cols=fc, wrap_cols=(3, 11))
    K.dropdown(ws, f'D{LP_FIRST}:D{LP_LAST}', f'{S}!$L$6:$L$9')
    K.dropdown(ws, f'E{LP_FIRST}:E{LP_LAST}', f'{S}!$J$6:$J$7')
    st = f'I{LP_FIRST}:I{LP_LAST}'
    ws.conditional_formatting.add(st, CellIsRule(operator='equal', formula=['"Ready to place"'], fill=PatternFill('solid', fgColor='9BE07A'), font=Font(name=K.FONT, bold=True)))
    ws.conditional_formatting.add(st, CellIsRule(operator='equal', formula=['"Done"'], fill=PatternFill('solid', fgColor='D9F2C4')))
    ws.conditional_formatting.add(st, CellIsRule(operator='equal', formula=['"Fix first"'], fill=PatternFill('solid', fgColor='F8D7D3')))
    ws.conditional_formatting.add(st, FormulaRule(formula=[f'LEFT(I{LP_FIRST},6)="Done, "'], fill=PatternFill('solid', fgColor='FFE8B3')))
    ws.conditional_formatting.add(f'G{LP_FIRST}:G{LP_LAST}', FormulaRule(formula=[f'AND(G{LP_FIRST}<>"",G{LP_FIRST}<>"OK")'], font=Font(name=K.FONT, bold=True, color='C0392B')))
    ws.freeze_panes = 'C5'
    ws.auto_filter.ref = f'A4:K{LP_LAST}'
    return ws


def dashboard_sheet(wb):
    ws = wb.create_sheet('Dashboard')
    ws.sheet_view.showGridLines = False
    K.title_block(ws, 'Dashboard', 'Everything here calculates from the other tabs. Nothing to type.')
    for c, w in zip('ABCDEFGHIJ', [40, 13, 3, 22, 11, 10, 10, 10, 10, 34]):
        ws.column_dimensions[c].width = w
    C = cm('C')
    lp = lambda c: f"'Link Plan'!${c}${LP_FIRST}:${c}${LP_LAST}"
    kpis = [
        ('Pillars', f'=COUNTA(Pillars!$A${P_FIRST}:$A${P_LAST})', '0'),                         # B5
        ('Pages in the cluster map', f'=COUNTA({C})', '0'),                                     # B6
        ('Live pages (Live or Update)', f'=COUNTIF({cm("L")},"Live")+COUNTIF({cm("L")},"Update")', '0'),  # B7
        ('Planned or being written', f'=COUNTIF({cm("L")},"Planned")+COUNTIF({cm("L")},"Writing")', '0'),  # B8
        ('Live cluster pages with two way links', f'=COUNTIF({cm("S")},"OK")+COUNTIF({cm("S")},"Add sibling links")', '0'),  # B9
        ('Orphan risk pages', f'=COUNTIF({cm("S")},"Orphan risk")', '0'),                      # B10
        ('Pages sharing a primary keyword', f'=COUNTIF({cm("T")},"Same keyword as another page")', '0'),  # B11
        ('Fan out questions listed', f'=COUNTA({fo("B")})', '0'),                              # B12
        ('Fan out gaps', f'=COUNTIF({fo("F")},"Gap")', '0'),                                   # B13
        ('Thin answers', f'=COUNTIF({fo("F")},"Thin answer")', '0'),                           # B14
        ('Links ready to place', f'=COUNTIF({lp("I")},"Ready to place")', '0'),                # B15
        ('Link tasks to fix first', f'=COUNTIF({lp("I")},"Fix first")', '0'),                  # B16
        ('Low CTR pages to rewrite', f'=COUNTIF({cm("X")},"Rewrite title and intro (low CTR)")', '0'),  # B17
        ('Average cluster health', f'=IFERROR(AVERAGE(Pillars!$O${P_FIRST}:$O${P_LAST}),0)', '0'),  # B18
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
    # Status table
    for j, h in enumerate(['Page status', 'Pages', 'Volume']):
        c = ws.cell(row=4, column=4 + j, value=h)
        c.font = K.f(10, True, 'FFFFFF')
        c.fill = K.HEAD_F
    for i, st in enumerate(['Planned', 'Writing', 'Live', 'Update', 'Merge']):
        r = 5 + i
        ws.cell(row=r, column=4, value=st)
        ws.cell(row=r, column=5, value=f'=COUNTIF({cm("L")},D{r})')
        ws.cell(row=r, column=6, value=f'=SUMIF({cm("L")},D{r},{cm("H")})').number_format = '#,##0'
        for cc in (4, 5, 6):
            ws.cell(row=r, column=cc).border = K.BORDER
            ws.cell(row=r, column=cc).font = K.f(10)
    # Pillar health table (mirrors Pillars)
    top = 21
    K.header_row(ws, top, ['Pillar', 'Health', None, 'Band', 'Coverage', 'Links', 'Fan out', 'Live pages', 'Overlaps', 'Next move'], formula_cols=tuple(range(1, 11)))
    ws.cell(row=top, column=3).fill = PatternFill(fill_type=None)
    for i in range(15):
        r = top + 1 + i
        pr = P_FIRST + i
        cells = {1: f'=IF(Pillars!A{pr}="","",Pillars!A{pr})', 2: f'=IF(Pillars!A{pr}="","",Pillars!O{pr})',
                 4: f'=IF(Pillars!A{pr}="","",Pillars!P{pr})', 5: f'=IF(Pillars!A{pr}="","",Pillars!I{pr})',
                 6: f'=IF(Pillars!A{pr}="","",Pillars!J{pr})', 7: f'=IF(Pillars!A{pr}="","",Pillars!L{pr})',
                 8: f'=IF(Pillars!A{pr}="","",Pillars!H{pr})', 9: f'=IF(Pillars!A{pr}="","",Pillars!K{pr})',
                 10: f'=IF(Pillars!A{pr}="","",Pillars!Q{pr})'}
        for cc, fm in cells.items():
            c = ws.cell(row=r, column=cc, value=fm)
            c.border = K.BORDER
            c.font = K.f(10, cc == 1)
            c.fill = K.FORMULA_FILL
            if cc in (5, 6, 7):
                c.number_format = '0%'
        ws.cell(row=r, column=10).alignment = K.Alignment(wrap_text=True)
    ch = BarChart()
    ch.type = 'bar'
    ch.title = 'Cluster health by pillar (0 to 100)'
    ch.y_axis.title = 'Health'
    ch.add_data(Reference(ws, min_col=2, min_row=top + 1, max_row=top + len(PILLARS) + 2), titles_from_data=False)
    ch.set_categories(Reference(ws, min_col=1, min_row=top + 1, max_row=top + len(PILLARS) + 2))
    ch.legend = None
    ch.height, ch.width = 7, 14
    ch.roundedCorners = False
    ch.x_axis.delete = False
    ch.y_axis.delete = False
    ch.y_axis.scaling.min = 0
    ch.y_axis.scaling.max = 100
    ch.title.overlay = False
    ch.y_axis.title.overlay = False
    ch.series[0].graphicalProperties.solidFill = K.GREEN
    ws.add_chart(ch, 'L4')
    ch2 = BarChart()
    ch2.type = 'col'
    ch2.title = 'Pages by status'
    ch2.y_axis.title = 'Pages'
    ch2.add_data(Reference(ws, min_col=5, min_row=5, max_row=9), titles_from_data=False)
    ch2.set_categories(Reference(ws, min_col=4, min_row=5, max_row=9))
    ch2.legend = None
    ch2.height, ch2.width = 7, 14
    ch2.roundedCorners = False
    ch2.x_axis.delete = False
    ch2.y_axis.delete = False
    ch2.title.overlay = False
    ch2.y_axis.title.overlay = False
    ch2.series[0].graphicalProperties.solidFill = '2B2B2B'
    ws.add_chart(ch2, 'L20')
    return ws


def build(path, asset, url):
    wb = K.new_book()
    cluster_sheet(wb)
    pillars_sheet(wb)
    dashboard_sheet(wb)
    fanout_sheet(wb)
    links_sheet(wb)
    settings_sheet(wb)
    K.prompts_sheet(wb, asset['prompts'], url)
    K.checklist_sheet(wb, list(asset['checklist']))
    K.sources_sheet(wb, asset['sources'], [
        ('Demo data', 'The demo rows on Cluster Map, Pillars, Fan Out Questions and Link Plan describe HireHive, a fictional company. All volumes, difficulty scores, clicks and impressions are illustrative, not real data.', ''),
        ('Cluster health score', 'Weighted mix of coverage (live cluster pages vs your target), two way links between pillar and cluster pages, fan out questions answered, and freedom from keyword overlap. Weights and bands live on Settings and are assumptions to tune.', ''),
        ('Build score', 'Weighted mix of volume (log scaled), ease (difficulty compared with what your site stage can win) and business value. Same method as the Keyword Research Kit.', ''),
        ('Fan out questions', 'Google says AI Overviews and AI Mode may run several related searches across subtopics (query fan out). This tab helps you check that your cluster answers those follow up questions. It does not predict what Google will run.', ''),
        ('Live pages', 'Pages with status Live or Update count as live for coverage, links and fan out checks.', ''),
    ])
    K.start_here(
        wb, 'Topic Clusters Kit',
        [
            'This workbook plans and audits topic clusters: a pillar page, the cluster pages around it, the links between them and the follow up questions they must answer. Every pillar gets a Cluster Health Score and a clear next move.',
            'It ships with demo data for a fictional HR software company (3 pillars, 23 pages, 22 questions, 16 link tasks) so you can see every check working. Clear the yellow demo cells when you are ready.',
        ],
        [
            ('Cluster Map', 'One row per page with 500 ready rows: pillar, role, keyword, intent, status and links, plus automatic link health, overlap check, build score, next action and anchor text.'),
            ('Pillars', 'One row per pillar with target size, coverage, two way links, fan out coverage, overlaps, health score, band and next move.'),
            ('Dashboard', 'Key numbers, status table, a pillar health table and two charts.'),
            ('Fan Out Questions', 'Follow up questions for each pillar, checked against your live and planned pages to show gaps and thin answers.'),
            ('Link Plan', 'Every internal link task with automatic anchor text and URL checks.'),
            ('Settings', 'Site stage, score weights, health bands, triggers, generic anchor list and dropdown lists.'),
            ('AI Prompts', 'Prompts for ChatGPT, Claude or Gemini to map clusters, mine questions, brief pages and plan links.'),
            ('Checklist', 'The full process as a tick list with automatic progress.'),
            ('Sources', 'Where facts come from and which numbers are assumptions.'),
        ],
        [
            'Look at the demo rows on every tab and the Dashboard to see how it works, then clear the yellow demo cells.',
            'Open Settings and choose your site stage. Leave the weights as they are for your first run.',
            'Add 1 to 5 pillar topics on the Pillars tab with their URL, keyword, goal and a target number of cluster pages.',
            'List every page for each pillar on the Cluster Map: the pillar page, cluster pages and supporting pages, live or planned.',
            'Mark the links that exist today (up to the pillar, from the pillar, sibling links) and add Search Console clicks and impressions.',
            'Add the follow up questions for each pillar on Fan Out Questions and the page that answers each one.',
            'Work through the Next move on Pillars, the Next action on Cluster Map and the Link Plan, then review monthly.',
        ],
        url,
    )
    order = ['Start Here', 'Cluster Map', 'Pillars', 'Dashboard', 'Fan Out Questions', 'Link Plan', 'Settings', 'AI Prompts', 'Checklist', 'Sources']
    wb._sheets = [wb[n] for n in order]
    wb.active = 0
    for ws in wb.worksheets:
        ws.sheet_properties.tabColor = K.GREEN if ws.title in ('Start Here', 'Cluster Map', 'Pillars', 'Dashboard') else 'A6EF39'
    wb.save(path)


PREVIEW = {'sheet': 'Cluster Map', 'header_row': 4, 'rows': 10, 'cols': [1, 2, 5, 8, 12, 13, 14, 19, 20, 21, 24],
           'formula_idx': [7, 8, 9, 10]}


def check(wb):
    """Assert the worked examples used in the guide."""
    p = wb['Pillars']
    # Worked example: Employee onboarding pillar (row 5)
    assert p['G5'].value == 9, p['G5'].value
    assert p['H5'].value == 6, p['H5'].value
    assert abs(p['I5'].value - 0.6) < 1e-9, p['I5'].value
    assert abs(p['J5'].value - 5 / 6) < 1e-9, p['J5'].value
    assert p['K5'].value == 2, p['K5'].value
    assert abs(p['L5'].value - 0.6) < 1e-9, p['L5'].value
    assert p['O5'].value == 69, p['O5'].value
    assert p['P5'].value == 'Growing', p['P5'].value
    assert p['Q5'].value == 'Answer the open fan out questions', p['Q5'].value
    # Performance reviews is thin, Leave policy counts Update pages as live
    assert p['P6'].value == 'Thin' and p['Q6'].value == 'Publish more cluster pages', (p['O6'].value, p['Q6'].value)
    assert p['H7'].value == 4, p['H7'].value
    c = wb['Cluster Map']
    # Build score example: Employee Onboarding Software (row 12)
    assert c['U12'].value == 77, c['U12'].value
    assert c['V12'].value == 'P2', c['V12'].value
    assert c['X12'].value == 'Brief and write (P2)', c['X12'].value
    assert c['U25'].value == 94 and c['V25'].value == 'P1', c['U25'].value
    assert c['T6'].value == 'Same keyword as another page', c['T6'].value
    assert c['X7'].value == 'Fix overlap: one page per keyword', c['X7'].value
    assert c['S7'].value == 'Add link from pillar', c['S7'].value
    assert c['S20'].value == 'Orphan risk', c['S20'].value
    assert c['X11'].value == 'Rewrite title and intro (low CTR)', c['X11'].value
    f = wb['Fan Out Questions']
    assert [f[f'F{r}'].value for r in range(5, 15)].count('Covered') == 6
    assert f['F11'].value == 'Thin answer' and f['F12'].value == 'Planned' and f['F13'].value == 'Gap'
    lp = wb['Link Plan']
    assert lp['G6'].value == 'Generic, rewrite', lp['G6'].value
    assert lp['H15'].value == 'Self link, remove', lp['H15'].value
    assert lp['G16'].value == 'Too long, tighten' and lp['I16'].value == 'Fix first', lp['G16'].value
    assert lp['I7'].value == 'Wait for target', lp['I7'].value
    assert lp['H20'].value == 'From URL not in Cluster Map', lp['H20'].value
    d = wb['Dashboard']
    assert d['B6'].value == len(PAGES), d['B6'].value
