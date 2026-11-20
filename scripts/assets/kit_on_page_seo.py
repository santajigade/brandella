"""On-Page SEO Kit workbook (asset 07).

Page Audit: one row per page (500 rows). You type what you see on the page (title, description, H1,
first paragraph, images, links, indexing, structured data, Core Web Vitals, Search Console numbers).
The sheet measures lengths and duplicates, runs 19 weighted checks (1 = pass, 0.5 = partly, 0 = fix,
blank = not checked or not needed), gives a score from 0 to 100, a grade, the fixes in priority order
and a priority based on the page's position. Page Report turns one URL into a printable report.
Fix Plan tracks the work. Dashboard counts failures per check.
"""
import datetime
from openpyxl.styles import PatternFill, Font, Alignment
from openpyxl.formatting.rule import CellIsRule, ColorScaleRule, FormulaRule
from openpyxl.chart import BarChart, Reference
from openpyxl.utils import get_column_letter as L
import kitlib as K

PA_FIRST, PA_LAST = 5, 504   # Page Audit
FX_FIRST, FX_LAST = 5, 304   # Fix Plan
S = 'Settings'
PA = "'Page Audit'"

(DATE, TMIN, TMAX, DMIN, DMAX, ALTMIN, LINKS, URLMAX) = (f'{S}!$B${r}' for r in range(5, 13))
LCPG, INPG, CLSG, LCPP, INPP, CLSP = (f'{S}!$B${r}' for r in range(15, 21))
GA, GB, GC, REWORK, SD1, SD2 = (f'{S}!$B${r}' for r in range(23, 29))
CHK_ROW = 32   # first row of the check table on Settings

PAGE_TYPES = [('Home', 'No'), ('Category', 'No'), ('Product', 'No'), ('Article or guide', 'Yes'), ('Service', 'No'),
              ('Local landing', 'No'), ('Tool', 'No'), ('About or contact', 'No')]
CANON = ['Self', 'Other URL', 'Missing']
SDATA = ['Valid', 'Errors', 'None']
YNN = ['Yes', 'No', 'Not needed']
FSTAT = ['To do', 'In progress', 'Done']

# name (header), weight, rule, how to fix
CHECKS = [
    ('Indexable, self canonical', 10, 'Indexable is Yes and the canonical points to the page itself. Missing canonical = partly.',
     'Remove a noindex you did not mean, fix robots.txt blocks and point the canonical to this URL.'),
    ('Keyword in title', 8, 'The focus keyword appears in the title tag.', 'Put the focus keyword, or the closest natural phrasing, near the start of the title.'),
    ('Direct answer up top', 8, 'The first paragraph says plainly what the page answers or offers.',
     'Open with 2 or 3 sentences that answer the main question or say what the page offers, before any story.'),
    ('Original value', 8, 'The page shows first hand data, photos, tests, examples or experience.',
     'Add what only you have: your own photos, results, prices, tests, mistakes and customer questions.'),
    ('Internal links in', 8, 'Pages on your site that link to this page: good at 3 or more, partly at 1 or 2, fix at 0.',
     'Link to the page from related pages with descriptive anchor text. Every page you care about needs at least one.'),
    ('Keyword in H1', 6, 'An H1 exists and contains the focus keyword. H1 without the keyword = partly.', 'Write one clear main heading that names the topic.'),
    ('Keyword in first paragraph', 6, 'The focus keyword appears in the first paragraph.', 'Name the topic naturally in the first paragraph.'),
    ('Title length', 5, 'Title between 30 and 60 characters (editable). Outside the range = partly.',
     'Keep the title clear and specific. Long titles may be cut off; very short ones waste the space.'),
    ('Unique title', 5, 'No other audited page uses the same title.', 'Give every page its own title that describes that page.'),
    ('Meta description', 5, 'A description exists and is 70 to 160 characters (editable). Outside the range = partly.',
     'Write a specific summary of the page in 1 or 2 sentences. Google may still show other text from the page.'),
    ('Byline', 5, 'Articles and guides show the author. Not checked on other page types.', 'Show a named author with a link to an author page.'),
    ('Image alt text', 5, 'At least 90 percent of images have alt text (editable). 50 to 89 percent = partly.',
     'Describe each image in a short, specific alt text. Do not stuff keywords.'),
    ('Core Web Vitals', 5, 'LCP, INP and CLS all Good = pass, none Poor = partly, any Poor = fix. Blank = no data.',
     'Fix the worst metric first: image size and server speed for LCP, heavy scripts for INP, reserved space for CLS.'),
    ('Question headings', 4, 'Articles and guides have at least 1 heading phrased as a question. Not checked on other types.',
     'Turn the follow up questions readers ask into headings with a short answer under each.'),
    ('Structured data', 4, 'Valid = pass, None = partly, Errors = fix.', 'Add the structured data type that fits the page and fix every error in the Rich Results Test.'),
    ('Unique description', 3, 'No other audited page uses the same meta description.', 'Write a description for this page only.'),
    ('Readable URL', 3, 'The path has no ?, = or _ and is at most 75 characters (editable).', 'Use short words separated by hyphens. Never change a ranking URL without a 301 redirect.'),
    ('Descriptive anchors', 3, 'No generic link text such as click here or read more on the page.', 'Rewrite generic link text so it says what the linked page is about.'),
    ('Updated date', 3, 'Articles and guides show when they were last updated. Not checked on other types.', 'Show the date of the last real update near the top.'),
]
NCH = len(CHECKS)

# Demo: UrbanRoots, a fictional plant shop and nursery in Pune. Every page, number and date is illustrative.
# url, type, kw, title, desc, h1, h1s, first para, words, q, imgs, noalt, links in, generic, indexable, canonical, sdata,
# byline, updated, direct, original, lcp, inp, cls, impressions, position
P = [
    ('https://urbanroots.example/', 'Home', 'indoor plants online in pune', 'UrbanRoots: Indoor Plants Online in Pune, Delivered in 24 Hours',
     'Buy healthy indoor plants online in Pune with pots, soil and care tips. Same day delivery in most areas and a 7 day plant guarantee.',
     'Indoor plants online in Pune, delivered in 24 hours', 1, 'Buy indoor plants online in Pune from our own nursery in Baner. Every plant is checked, potted and delivered within 24 hours.',
     900, 0, 24, 2, 120, 3, 'Yes', 'Self', 'Valid', 'Not needed', 'Not needed', 'Yes', 'Yes', 3.1, 180, 0.05, 18000, 3.2),
    ('https://urbanroots.example/indoor-plants/', 'Category', 'indoor plants', 'Indoor Plants: Buy Online at the Best Prices | UrbanRoots', '',
     'Indoor Plants', 1, 'Shop 140 indoor plants grown in our Pune nursery, from easy snake plants to statement fiddle leaf figs.',
     400, 0, 40, 12, 85, 0, 'Yes', 'Self', 'Valid', 'Not needed', 'Not needed', 'Yes', 'No', 2.2, 150, 0.02, 26000, 14.5),
    ('https://urbanroots.example/plants/snake-plant/', 'Product', 'snake plant', 'Snake Plant (Sansevieria) in a Ceramic Pot | UrbanRoots',
     'A hardy snake plant in a 6 inch ceramic pot, grown in our Pune nursery. Low light friendly, needs water every 2 to 3 weeks. Free care guide.',
     'Snake Plant in Ceramic Pot', 1, 'The snake plant is one of the easiest indoor plants to keep alive. This one is about 45 cm tall and comes in a 6 inch pot.',
     650, 2, 6, 0, 14, 0, 'Yes', 'Self', 'Valid', 'Not needed', 'Not needed', 'Yes', 'Yes', 2.0, 120, 0.01, 9000, 8.1),
    ('https://urbanroots.example/guides/how-to-repot-a-snake-plant/', 'Article or guide', 'how to repot a snake plant', 'How to Repot a Snake Plant: 7 Steps With Photos',
     'Repot your snake plant without damaging the roots: when to do it, which pot and soil to use, and 7 steps with photos from our nursery.',
     'Repotting Your Snake Plant', 1, 'Snake plants are tough, but they do outgrow their pots. Here is what we have learned from repotting hundreds of them in our nursery.',
     1700, 0, 8, 5, 0, 1, 'Yes', 'Self', 'None', 'Yes', 'No', 'No', 'Yes', 2.3, 130, 0.04, 5400, 7.0),
    ('https://urbanroots.example/guides/best-indoor-plants-for-low-light/', 'Article or guide', 'best indoor plants for low light',
     'Best Indoor Plants for Low Light: 12 We Grew in North Facing Rooms', 'The 12 best indoor plants for low light, tested for 6 months in north facing rooms in Pune, with how much light each one really needs.',
     '12 Best Indoor Plants for Low Light', 1, 'These are the best indoor plants for low light that survived 6 months in our north facing test rooms, ranked by how well they grew.',
     2600, 4, 14, 0, 9, 0, 'Yes', 'Self', 'Valid', 'Yes', 'Yes', 'Yes', 'Yes', 2.4, 160, 0.04, 22000, 5.6),
    ('https://urbanroots.example/guides/money-plant-care/', 'Article or guide', 'money plant care', 'Money Plant Care Guide',
     'Simple plant care tips from the UrbanRoots nursery team: light, water, soil and what to do when something goes wrong.',
     'Money Plant Care: Water, Light and Soil', 1, 'Money plant care is easy once you get the watering right. Here is the routine we use in our nursery.',
     1800, 3, 7, 1, 4, 1, 'Yes', 'Self', 'None', 'Yes', 'No', 'Yes', 'No', 3.0, 240, 0.12, 7200, 11.2),
    ('https://urbanroots.example/blog/yellow-leaves-on-plants/', 'Article or guide', 'why are my plant leaves turning yellow',
     'Why Are My Plant Leaves Turning Yellow? 9 Causes and Fixes', 'Simple plant care tips from the UrbanRoots nursery team: light, water, soil and what to do when something goes wrong.',
     'Why Are My Plant Leaves Turning Yellow?', 2, 'Yellow leaves usually mean too much water, but there are 8 other causes. Check the pattern on the leaf first.',
     2100, 9, 10, 0, 2, 0, 'Yes', 'Self', 'Valid', 'Yes', 'Yes', 'Yes', 'Yes', 2.1, 90, 0.03, 15000, 4.3),
    ('https://urbanroots.example/plant-nursery-in-pune/', 'Local landing', 'plant nursery in pune', 'Plant Nursery in Pune: Visit Our Baner Garden Centre',
     'Visit the UrbanRoots plant nursery in Baner, Pune: 600 plants, pots and soil, open every day from 8 am to 8 pm, with free parking.',
     'Plant nursery in Pune', 1, 'Our plant nursery in Pune is in Baner, 5 minutes from the highway, with 600 plants on display.',
     700, 0, 12, 4, 6, 2, 'Yes', 'Self', 'Valid', 'Not needed', 'Not needed', 'Yes', 'Yes', 4.6, 310, 0.3, 4100, 6.0),
    ('https://urbanroots.example/plant-delivery-pune/', 'Service', 'plant delivery in pune', 'Plant Delivery', '',
     '', 0, 'We deliver across the city every day, including Sundays.',
     300, 0, 3, 3, 1, 4, 'Yes', 'Self', 'None', 'Not needed', 'Not needed', 'No', 'No', 2.9, 210, 0.08, 3300, 18.0),
    ('https://urbanroots.example/guides/self-watering-pots/', 'Article or guide', 'self watering pots', 'Self Watering Pots: Do They Work? Our 3 Month Test',
     'We tested 5 self watering pots for 3 months with 20 plants. Here is which plants loved them, which rotted, and how to use one properly.',
     'Self Watering Pots: Do They Work?', 1, 'Self watering pots work well for thirsty plants and badly for succulents. Our 3 month test with 20 plants showed why.',
     1500, 2, 6, 0, 0, 0, 'Yes', 'Self', 'Valid', 'Yes', 'Yes', 'Yes', 'Yes', 2.3, 140, 0.05, 800, 24.0),
    ('https://urbanroots.example/about/', 'About or contact', 'urbanroots', 'About UrbanRoots: Our Pune Nursery and Team',
     'UrbanRoots grows indoor plants in Baner, Pune. Meet the team of 12 gardeners, see how we grow and pack plants, and find our address and hours.',
     'About UrbanRoots', 1, 'UrbanRoots started in 2019 as a small nursery in Baner, Pune, and now ships indoor plants across the city.',
     800, 0, 9, 0, 120, 0, 'Yes', 'Self', 'Valid', 'Not needed', 'Not needed', 'Yes', 'Yes', 2.0, 100, 0.02, 300, 1.2),
    ('https://urbanroots.example/tools/pot-size-calculator/', 'Tool', 'pot size calculator', 'Pot Size Calculator: Find the Right Pot for Any Plant',
     'Enter your plant and its current pot to get the right new pot size in inches and cm, with drainage and soil tips from our nursery.',
     'Pot Size Calculator', 1, 'Use this pot size calculator to find the right next pot for your plant in seconds.',
     500, 1, 2, 0, 7, 0, 'No', 'Self', 'None', 'Not needed', 'Not needed', 'Yes', 'Yes', 1.8, 110, 0.0, None, None),
]
# url index, fix (check name), owner, due, status, notes
FIXES = [
    (3, 'Internal links in', 'Meera', '2026-11-27', 'To do', 'Link from the snake plant product page and the low light guide'),
    (3, 'Direct answer up top', 'Meera', '2026-11-27', 'To do', 'Open with when to repot and the 3 signs'),
    (3, 'Image alt text', 'Kiran', '2026-11-25', 'In progress', '5 step photos have no alt text'),
    (3, 'Keyword in first paragraph', 'Meera', '2026-11-27', 'To do', ''),
    (8, 'Keyword in title', 'Kiran', '2026-11-24', 'To do', 'Title is only "Plant Delivery"'),
    (8, 'Meta description', 'Kiran', '2026-11-24', 'To do', ''),
    (8, 'Keyword in H1', 'Kiran', '2026-11-24', 'To do', 'No H1 on the page'),
    (11, 'Indexable, self canonical', 'Dev team', '2026-11-21', 'In progress', 'noindex left over from staging'),
    (1, 'Meta description', 'Kiran', '2026-11-28', 'To do', ''),
    (7, 'Core Web Vitals', 'Dev team', '2026-12-10', 'To do', 'Hero image is 2.4 MB, map embed shifts layout'),
    (5, 'Unique description', 'Meera', '2026-11-18', 'Done', 'Rewritten'),
    (6, 'Unique description', 'Meera', '2026-11-19', 'To do', 'Same description as the money plant guide'),
    (4, 'Byline', 'Meera', '2026-11-15', 'Done', 'Author box added'),
]

IN_HEAD = ['URL', 'Page type', 'Focus keyword', 'Title tag', 'Meta description (paste)', 'H1', 'Number of H1s', 'First paragraph (paste)',
           'Approx. words', 'Question headings (count)', 'Images', 'Images without alt', 'Internal links pointing to it', 'Generic anchors on the page',
           'Indexable?', 'Canonical', 'Structured data (test result)', 'Byline shown?', 'Updated date shown?', 'Direct answer in first paragraph?',
           'Original value (data, photos, tests)?', 'LCP (s)', 'INP (ms)', 'CLS', 'Impressions (28 days)', 'Avg position', 'Notes']
MEAS_HEAD = ['URL path', 'Title characters', 'Description characters', 'Pages with this title', 'Pages with this description', 'Alt coverage', 'Core Web Vitals status']
OUT_HEAD = ['Score (0 to 100)', 'Grade', 'Fixes needed', 'Fixes in priority order', 'Priority', 'Fix value (helper)', 'Editorial (helper)']
NIN, NME = len(IN_HEAD), len(MEAS_HEAD)
C0 = NIN + NME + 1                      # first check column (35 = AI)
CK = [L(C0 + i) for i in range(NCH)]    # check column letters
SC = C0 + NCH                           # score column (54 = BB)
HEAD = IN_HEAD + MEAS_HEAD + [c[0] for c in CHECKS] + OUT_HEAD
F_COLS = tuple(range(NIN + 1, len(HEAD) + 1))


def pa(c):
    return f'{PA}!${c}${PA_FIRST}:${c}${PA_LAST}'


def d(s):
    return datetime.date.fromisoformat(s) if s else None


def settings_sheet(wb):
    ws = wb.create_sheet(S)
    ws.sheet_view.showGridLines = False
    K.title_block(ws, 'Settings', 'Every threshold, weight and list used by this workbook. Change a blue number and every score updates.')
    for c, w in zip('ABCDEFGHIJK', [44, 12, 62, 70, 3, 20, 10, 3, 12, 12, 12]):
        ws.column_dimensions[c].width = w
    rows = [
        (4, 'PAGE CHECKS', None, None),
        (5, 'Analysis date (set it to the day you audit)', datetime.date(2026, 11, 20), 'dd mmm yyyy'),
        (6, 'Title is short below (characters)', 30, '0'),
        (7, 'Title may be cut off above (characters)', 60, '0'),
        (8, 'Description is short below (characters)', 70, '0'),
        (9, 'Description may be cut off above (characters)', 160, '0'),
        (10, 'Image alt text coverage for a pass', 0.9, '0%'),
        (11, 'Internal links pointing to the page for a full pass', 3, '0'),
        (12, 'URL path is long above (characters)', 75, '0'),
        (14, 'CORE WEB VITALS (Google thresholds, field data)', None, None),
        (15, 'LCP Good at most (seconds)', 2.5, '0.0'),
        (16, 'INP Good at most (milliseconds)', 200, '0'),
        (17, 'CLS Good at most', 0.1, '0.00'),
        (18, 'LCP Poor above (seconds)', 4, '0.0'),
        (19, 'INP Poor above (milliseconds)', 500, '0'),
        (20, 'CLS Poor above', 0.25, '0.00'),
        (22, 'GRADES AND PRIORITY', None, None),
        (23, 'Grade A when the score is at least', 85, '0'),
        (24, 'Grade B when at least', 70, '0'),
        (25, 'Grade C when at least (below = D)', 55, '0'),
        (26, 'Rework the page when the score is below', 50, '0'),
        (27, 'Close to the top: average position from', 4, '0'),
        (28, 'Close to the top: average position up to', 20, '0'),
    ]
    for r, label, val, fmt in rows:
        a = ws.cell(row=r, column=1, value=label)
        a.font = K.f(10, val is None, K.DEEP if val is None else K.INK)
        if val is not None:
            c = ws.cell(row=r, column=2, value=val)
            c.border, c.fill = K.BORDER, K.INPUT_FILL
            c.font = K.f(10, True, '0000FF')
            c.number_format = fmt
    ws['C5'] = 'Length bands for titles and descriptions are assumptions of this kit: Google sets no fixed limit and cuts snippets to fit the device. Core Web Vitals bands are from Google Search Console help.'
    ws['C5'].font = K.f(9, False, '777777', True)
    ws['C5'].alignment = Alignment(wrap_text=True, vertical='top')
    ws.merge_cells('C5:D8')
    ws.cell(row=CHK_ROW - 2, column=1, value='THE 19 CHECKS (weights are editable; any numbers, they are scaled)').font = K.f(10, True, K.DEEP)
    K.header_row(ws, CHK_ROW - 1, ['Check', 'Weight', 'Rule in the workbook', 'How to fix'])
    for i, (name, w, rule, fix) in enumerate(CHECKS):
        r = CHK_ROW + i
        for col, v in enumerate([name, w, rule, fix], 1):
            c = ws.cell(row=r, column=col, value=v)
            c.border = K.BORDER
            c.font = K.f(10, col == 1, '0000FF' if col == 2 else K.INK)
            c.alignment = Alignment(wrap_text=True, vertical='top')
        ws.cell(row=r, column=2).fill = K.INPUT_FILL
        ws.row_dimensions[r].height = 30
    tr = CHK_ROW + NCH
    ws.cell(row=tr, column=1, value='Total weight (auto)').font = K.f(10, True)
    ws.cell(row=tr, column=2, value=f'=SUM(B{CHK_ROW}:B{tr - 1})').fill = K.FORMULA_FILL
    ws['F4'] = 'PAGE TYPES'
    ws['F4'].font = K.f(10, True, K.DEEP)
    ws['F5'], ws['G5'] = 'Page type', 'Editorial?'
    for c in ('F5', 'G5'):
        ws[c].font = K.f(9, True, '555555')
    for i, (t, ed) in enumerate(PAGE_TYPES):
        ws.cell(row=6 + i, column=6, value=t).fill = K.INPUT_FILL
        ws.cell(row=6 + i, column=7, value=ed).fill = K.INPUT_FILL
    ws.cell(row=6 + len(PAGE_TYPES), column=6, value='Editorial pages get the byline, updated date and question heading checks.').font = K.f(8, False, '777777', True)
    ws['I4'] = 'DROPDOWN LISTS'
    ws['I4'].font = K.f(10, True, K.DEEP)
    lists = {'I': ['Yes/No', 'Yes', 'No', 'Not needed'], 'J': ['Canonical'] + CANON, 'K': ['Structured data'] + SDATA, 'H': [None]}
    lists['L'] = ['Fix status'] + FSTAT
    for c, vals in lists.items():
        for i, v in enumerate(vals):
            if v is None:
                continue
            cell = ws[f'{c}{5 + i}']
            cell.value = v
            cell.font = K.f(9, i == 0, '555555')
    ws.column_dimensions['L'].width = 12
    return ws


def audit_sheet(wb):
    ws = wb.create_sheet('Page Audit')
    ws.sheet_view.showGridLines = False
    K.title_block(ws, 'Page audit', f'Rows 5 to {4 + len(P)} hold DEMO data for UrbanRoots, a fictional plant shop in Pune (illustrative pages and numbers). Select the yellow demo cells and press Delete to start your own. Grey formula columns stay.')
    ws['A2'].font = K.f(10, True, 'B45309')
    ws['A3'] = 'One row per page. Type what you see on the live page (view source for the title, description and canonical). Row 3 above the checks shows each check weight from Settings. 500 rows ready.'
    ws['A3'].font = K.f(9, False, '666666', True)
    widths = ([44, 14, 26, 44, 50, 32, 7, 50, 8, 8, 7, 8, 9, 9, 9, 10, 10, 9, 9, 10, 10, 7, 7, 7, 10, 8, 18] +
              [30, 7, 7, 8, 8, 8, 11] + [9] * NCH + [9, 7, 7, 60, 26, 9, 8])
    K.header_row(ws, 4, HEAD, formula_cols=F_COLS, widths=widths)
    for i, col in enumerate(CK):
        c = ws[f'{col}3']
        c.value = f'={S}!$B${CHK_ROW + i}'
        c.font, c.fill, c.alignment = K.f(9, True, K.DEEP), K.SOFT, Alignment(horizontal='center')
    ws[f'{CK[0]}2'] = 'Check weights (from Settings)'
    ws[f'{CK[0]}2'].font = K.f(9, True, K.DEEP)
    m = {h: L(i + 1) for i, h in enumerate(HEAD)}
    for r in range(PA_FIRST, PA_LAST + 1):
        i = r - PA_FIRST
        if i < len(P):
            for col, v in enumerate(P[i], 1):
                if v not in (None, ''):
                    ws.cell(row=r, column=col, value=v)
        e = f'A{r}=""'
        ed = f'{m["Editorial (helper)"]}{r}'
        s = f'IF(ISNUMBER(FIND("//",A{r})),MID(A{r},FIND("//",A{r})+2,500),A{r})'
        f = {}
        f['URL path'] = f'=IF({e},"",IF(ISNUMBER(FIND("/",{s})),MID({s},FIND("/",{s}),500),"/"))'
        f['Title characters'] = f'=IF({e},"",LEN(D{r}))'
        f['Description characters'] = f'=IF({e},"",LEN(E{r}))'
        f['Pages with this title'] = f'=IF(OR({e},D{r}=""),"",SUMPRODUCT(--($D${PA_FIRST}:$D${PA_LAST}=D{r})))'
        f['Pages with this description'] = f'=IF(OR({e},E{r}=""),"",SUMPRODUCT(--($E${PA_FIRST}:$E${PA_LAST}=E{r})))'
        f['Alt coverage'] = f'=IF(OR({e},K{r}=""),"",IF(N(K{r})=0,1,MAX(0,1-N(L{r})/K{r})))'
        f['Core Web Vitals status'] = (
            f'=IF({e},"",IF(COUNT(V{r}:X{r})<3,"No data",IF(OR(V{r}>{LCPP},W{r}>{INPP},X{r}>{CLSP}),"Poor",'
            f'IF(AND(V{r}<={LCPG},W{r}<={INPG},X{r}<={CLSG}),"Good","Needs improvement"))))')
        kw = f'OR({e},C{r}="")'
        t = {}
        t['Indexable, self canonical'] = f'=IF(OR({e},O{r}=""),"",IF(O{r}<>"Yes",0,IF(P{r}="Self",1,IF(P{r}="Missing",0.5,0))))'
        t['Keyword in title'] = f'=IF({kw},"",IF(ISNUMBER(SEARCH(C{r},D{r})),1,0))'
        t['Direct answer up top'] = f'=IF(OR({e},T{r}=""),"",IF(T{r}="Yes",1,0))'
        t['Original value'] = f'=IF(OR({e},U{r}=""),"",IF(U{r}="Yes",1,0))'
        t['Internal links in'] = f'=IF(OR({e},M{r}=""),"",IF(N(M{r})>={LINKS},1,IF(N(M{r})>=1,0.5,0)))'
        t['Keyword in H1'] = f'=IF({kw},"",IF(OR(N(G{r})=0,F{r}=""),0,IF(ISNUMBER(SEARCH(C{r},F{r})),1,0.5)))'
        t['Keyword in first paragraph'] = f'=IF(OR({kw},H{r}=""),"",IF(ISNUMBER(SEARCH(C{r},H{r})),1,0))'
        t['Title length'] = f'=IF({e},"",IF(D{r}="",0,IF(AND(LEN(D{r})>={TMIN},LEN(D{r})<={TMAX}),1,0.5)))'
        t['Unique title'] = f'=IF(OR({e},D{r}=""),"",IF({m["Pages with this title"]}{r}>1,0,1))'
        t['Meta description'] = f'=IF({e},"",IF(E{r}="",0,IF(AND(LEN(E{r})>={DMIN},LEN(E{r})<={DMAX}),1,0.5)))'
        t['Byline'] = f'=IF(OR({e},{ed}<>"Yes",R{r}=""),"",IF(R{r}="Yes",1,0))'
        t['Image alt text'] = f'=IF(OR({e},K{r}=""),"",IF({m["Alt coverage"]}{r}>={ALTMIN},1,IF({m["Alt coverage"]}{r}>=0.5,0.5,0)))'
        cw = f'{m["Core Web Vitals status"]}{r}'
        t['Core Web Vitals'] = f'=IF(OR({e},{cw}="No data"),"",IF({cw}="Good",1,IF({cw}="Poor",0,0.5)))'
        t['Question headings'] = f'=IF(OR({e},{ed}<>"Yes",J{r}=""),"",IF(N(J{r})>=1,1,0))'
        t['Structured data'] = f'=IF(OR({e},Q{r}=""),"",IF(Q{r}="Valid",1,IF(Q{r}="None",0.5,0)))'
        t['Unique description'] = f'=IF(OR({e},E{r}=""),"",IF({m["Pages with this description"]}{r}>1,0,1))'
        up = f'{m["URL path"]}{r}'
        t['Readable URL'] = f'=IF({e},"",IF(OR(ISNUMBER(FIND("?",{up})),ISNUMBER(FIND("=",{up})),ISNUMBER(FIND("_",{up})),LEN({up})>{URLMAX}),0,1))'
        t['Descriptive anchors'] = f'=IF(OR({e},N{r}=""),"",IF(N(N{r})=0,1,0))'
        t['Updated date'] = f'=IF(OR({e},{ed}<>"Yes",S{r}=""),"",IF(S{r}="Yes",1,0))'
        for h, v in list(f.items()) + list(t.items()):
            ws[f'{m[h]}{r}'] = v
        rng = f'{CK[0]}{r}:{CK[-1]}{r}'
        w = f'${CK[0]}$3:${CK[-1]}$3'
        sc = m['Score (0 to 100)']
        ws[f'{sc}{r}'] = f'=IF({e},"",IFERROR(ROUND(100*SUMPRODUCT({w},{rng})/SUMPRODUCT({w}*ISNUMBER({rng})),0),""))'
        ws[f'{m["Grade"]}{r}'] = f'=IF(OR({e},{sc}{r}=""),"",IF({sc}{r}>={GA},"A",IF({sc}{r}>={GB},"B",IF({sc}{r}>={GC},"C","D"))))'
        ws[f'{m["Fixes needed"]}{r}'] = f'=IF({e},"",COUNTIF({rng},0)+COUNTIF({rng},0.5))'
        parts = ','.join(f'IF({c}{r}=0,{c}$4,IF({c}{r}=0.5,{c}$4&" (partly)",""))' for c in CK)
        ws[f'{m["Fixes in priority order"]}{r}'] = f'=IF({e},"",_xlfn.TEXTJOIN("; ",TRUE,{parts}))'
        z = f'Z{r}'
        ws[f'{m["Priority"]}{r}'] = (
            f'=IF(OR({e},{sc}{r}=""),"",IF({CK[0]}{r}=0,"Blocked: fix indexing first",IF({sc}{r}>={GA},"Healthy: monitor",IF(AND(N({z})>=1,N({z})<{SD1}),"Protect: fix carefully",'
            f'IF(AND(N({z})>={SD1},N({z})<={SD2}),"Fix first: close to the top",IF({sc}{r}<{REWORK},"Rework the page","Improve when you can"))))))')
        ws[f'{m["Fix value (helper)"]}{r}'] = f'=IF(OR({e},{sc}{r}=""),"",ROUND(N(Y{r})*(100-{sc}{r})/100,0))'
        ws[f'{m["Editorial (helper)"]}{r}'] = f'=IF({e},"",IFERROR(VLOOKUP(B{r},{S}!$F$6:$G${5 + len(PAGE_TYPES)},2,FALSE),"No"))'
    nf = {9: '#,##0', 22: '0.0', 23: '0', 24: '0.00', 25: '#,##0', 26: '0.0', NIN + 6: '0%', SC: '0', SC + 5: '#,##0'}
    K.style_body(ws, PA_FIRST, PA_LAST, len(HEAD), formula_cols=F_COLS, number_formats=nf, wrap_cols=(4, 5, 8, SC + 3))
    ws.freeze_panes = 'B5'
    ws.auto_filter.ref = f'A4:{L(len(HEAD))}{PA_LAST}'
    K.dropdown(ws, f'B{PA_FIRST}:B{PA_LAST}', f'{S}!$F$6:$F${5 + len(PAGE_TYPES)}')
    K.whole_number(ws, f'G{PA_FIRST}:G{PA_LAST}', 0, 20, 'Number of H1 headings on the page.')
    for c in 'OTU':
        K.dropdown(ws, f'{c}{PA_FIRST}:{c}{PA_LAST}', f'{S}!$I$6:$I$7')
    for c in 'RS':
        K.dropdown(ws, f'{c}{PA_FIRST}:{c}{PA_LAST}', f'{S}!$I$6:$I$8')
    K.dropdown(ws, f'P{PA_FIRST}:P{PA_LAST}', f'{S}!$J$6:$J$8')
    K.dropdown(ws, f'Q{PA_FIRST}:Q{PA_LAST}', f'{S}!$K$6:$K$8')
    chk = f'{CK[0]}{PA_FIRST}:{CK[-1]}{PA_LAST}'
    ws.conditional_formatting.add(chk, CellIsRule(operator='equal', formula=['1'], fill=PatternFill('solid', fgColor='D9F2C4')))
    ws.conditional_formatting.add(chk, CellIsRule(operator='equal', formula=['0.5'], fill=PatternFill('solid', fgColor='FFF4CC')))
    ws.conditional_formatting.add(chk, FormulaRule(formula=[f'AND(ISNUMBER({CK[0]}{PA_FIRST}),{CK[0]}{PA_FIRST}=0)'], fill=PatternFill('solid', fgColor='F8D7D3'), font=Font(name=K.FONT, bold=True, color='9B2C1F')))
    scol = L(SC)
    ws.conditional_formatting.add(f'{scol}{PA_FIRST}:{scol}{PA_LAST}', ColorScaleRule(start_type='num', start_value=30, start_color='F8D7D3', mid_type='num', mid_value=70, mid_color='FFF4CC', end_type='num', end_value=100, end_color='B7E4A0'))
    g = f'{L(SC + 1)}{PA_FIRST}:{L(SC + 1)}{PA_LAST}'
    for val, col in (('A', '9BE07A'), ('B', 'D9F2C4'), ('C', 'FFF4CC'), ('D', 'F8D7D3')):
        ws.conditional_formatting.add(g, CellIsRule(operator='equal', formula=[f'"{val}"'], fill=PatternFill('solid', fgColor=col), font=Font(name=K.FONT, bold=True)))
    pr = f'{L(SC + 4)}{PA_FIRST}:{L(SC + 4)}{PA_LAST}'
    ws.conditional_formatting.add(pr, FormulaRule(formula=[f'LEFT({L(SC + 4)}{PA_FIRST},9)="Fix first"'], fill=PatternFill('solid', fgColor='F8D7D3'), font=Font(name=K.FONT, bold=True, color='9B2C1F')))
    ws.conditional_formatting.add(pr, FormulaRule(formula=[f'LEFT({L(SC + 4)}{PA_FIRST},7)="Blocked"'], fill=PatternFill('solid', fgColor='9B2C1F'), font=Font(name=K.FONT, bold=True, color='FFFFFF')))
    ws.conditional_formatting.add(pr, FormulaRule(formula=[f'LEFT({L(SC + 4)}{PA_FIRST},6)="Rework"'], fill=PatternFill('solid', fgColor='FCE4D6'), font=Font(name=K.FONT, bold=True)))
    ws.conditional_formatting.add(pr, FormulaRule(formula=[f'LEFT({L(SC + 4)}{PA_FIRST},7)="Healthy"'], fill=PatternFill('solid', fgColor='D9F2C4')))
    for col, rule in ((m['Title characters'], f'OR({m["Title characters"]}{PA_FIRST}<{TMIN},{m["Title characters"]}{PA_FIRST}>{TMAX})'),
                      (m['Description characters'], f'OR({m["Description characters"]}{PA_FIRST}<{DMIN},{m["Description characters"]}{PA_FIRST}>{DMAX})')):
        ws.conditional_formatting.add(f'{col}{PA_FIRST}:{col}{PA_LAST}', FormulaRule(formula=[f'AND($A{PA_FIRST}<>"",{rule})'], font=Font(name=K.FONT, bold=True, color='B45309')))
    cwc = m['Core Web Vitals status']
    ws.conditional_formatting.add(f'{cwc}{PA_FIRST}:{cwc}{PA_LAST}', CellIsRule(operator='equal', formula=['"Poor"'], font=Font(name=K.FONT, bold=True, color='9B2C1F')))
    ws.conditional_formatting.add(f'{cwc}{PA_FIRST}:{cwc}{PA_LAST}', CellIsRule(operator='equal', formula=['"Good"'], font=Font(name=K.FONT, bold=True, color=K.DEEP)))
    return m


def report_sheet(wb, m):
    ws = wb.create_sheet('Page Report')
    ws.sheet_view.showGridLines = False
    for c, w in zip('ABCDEF', [30, 12, 44, 56, 60, 3]):
        ws.column_dimensions[c].width = w
    K.title_block(ws, 'Page report', 'Choose a URL in the yellow cell. Every check, its result, what was measured and how to fix it fill in by themselves. Print it or send it to the writer or developer.')
    ws['A4'] = 'URL'
    ws['A4'].font = K.f(11, True)
    ws['B4'] = P[3][0]
    ws['B4'].fill, ws['B4'].font, ws['B4'].border = K.INPUT_FILL, K.f(11, True), K.BORDER
    ws.merge_cells('B4:D4')
    K.dropdown(ws, 'B4', pa('A'), 'Pick a URL from the Page Audit tab')
    mt = f'MATCH($B$4,{pa("A")},0)'

    def get(col, text=True):
        return f'IFERROR(INDEX({pa(col)},{mt}){"&" + chr(34) * 2 if text else ""},"")'
    items = [('Page type', 'B', None), ('Focus keyword', 'C', None), ('Score (0 to 100)', m['Score (0 to 100)'], '0'), ('Grade', m['Grade'], None),
             ('Fixes needed', m['Fixes needed'], '0'), ('Priority', m['Priority'], None), ('Impressions (28 days)', 'Y', '#,##0'), ('Avg position', 'Z', '0.0'),
             ('Fixes in priority order', m['Fixes in priority order'], None)]
    for i, (label, col, fmt) in enumerate(items):
        r = 6 + i
        ws.cell(row=r, column=1, value=label).font = K.f(10)
        c = ws.cell(row=r, column=2, value='=' + get(col, fmt is None))
        c.fill, c.border, c.font = K.FORMULA_FILL, K.BORDER, K.f(10, label in ('Score (0 to 100)', 'Grade', 'Priority'))
        c.alignment = Alignment(wrap_text=True, vertical='top')
        if fmt:
            c.number_format = fmt
        ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=4)
    ws.row_dimensions[14].height = 48
    top = 17
    ws.cell(row=top - 1, column=1, value='THE 19 CHECKS FOR THIS PAGE').font = K.f(10, True, K.DEEP)
    K.header_row(ws, top, ['Check', 'Result', 'What was measured', 'Rule', 'How to fix'], formula_cols=(1, 2, 3, 4, 5))
    meas = {
        'Indexable, self canonical': f'"Indexable: "&{get("O")}&", canonical: "&{get("P")}',
        'Keyword in title': get('D'),
        'Direct answer up top': get('T'),
        'Original value': get('U'),
        'Internal links in': get('M') + '&" pages link to it"',
        'Keyword in H1': f'{get("G")}&" H1: "&{get("F")}',
        'Keyword in first paragraph': f'LEFT({get("H")},140)',
        'Title length': get(m['Title characters']) + '&" characters"',
        'Unique title': get(m['Pages with this title']) + '&" page(s) use this title"',
        'Meta description': get(m['Description characters']) + '&" characters"',
        'Byline': get('R'),
        'Image alt text': f'{get("L")}&" of "&{get("K")}&" images without alt"',
        'Core Web Vitals': f'{get(m["Core Web Vitals status"])}&" (LCP "&{get("V")}&" s, INP "&{get("W")}&" ms, CLS "&{get("X")}&")"',
        'Question headings': get('J'),
        'Structured data': get('Q'),
        'Unique description': get(m['Pages with this description']) + '&" page(s) use this description"',
        'Readable URL': get(m['URL path']),
        'Descriptive anchors': get('N') + '&" generic anchors"',
        'Updated date': get('S'),
    }
    for i, (name, w, rule, fix) in enumerate(CHECKS):
        r = top + 1 + i
        ws.cell(row=r, column=1, value=f'={S}!A{CHK_ROW + i}')
        v = f'IFERROR(INDEX({pa(CK[i])},{mt}),"")'
        ws.cell(row=r, column=2, value=f'=IF($B$4="","",IF({v}="","Not checked",IF({v}=1,"OK",IF({v}=0.5,"Partly","Fix"))))')
        ws.cell(row=r, column=3, value=f'=IF($B$4="","",{meas[name]})')
        ws.cell(row=r, column=4, value=f'={S}!C{CHK_ROW + i}')
        ws.cell(row=r, column=5, value=f'=IF(B{r}="OK","",{S}!D{CHK_ROW + i})')
        for c in range(1, 6):
            cell = ws.cell(row=r, column=c)
            cell.fill, cell.border, cell.font = K.FORMULA_FILL, K.BORDER, K.f(9, c == 1)
            cell.alignment = Alignment(wrap_text=True, vertical='top')
        ws.row_dimensions[r].height = 40
    b = f'B{top + 1}:B{top + NCH}'
    ws.conditional_formatting.add(b, CellIsRule(operator='equal', formula=['"OK"'], fill=PatternFill('solid', fgColor='D9F2C4'), font=Font(name=K.FONT, bold=True)))
    ws.conditional_formatting.add(b, CellIsRule(operator='equal', formula=['"Partly"'], fill=PatternFill('solid', fgColor='FFF4CC'), font=Font(name=K.FONT, bold=True)))
    ws.conditional_formatting.add(b, CellIsRule(operator='equal', formula=['"Fix"'], fill=PatternFill('solid', fgColor='F8D7D3'), font=Font(name=K.FONT, bold=True, color='9B2C1F')))
    return ws, top


def fix_sheet(wb, m):
    ws = wb.create_sheet('Fix Plan')
    ws.sheet_view.showGridLines = False
    K.title_block(ws, 'Fix plan', 'One row per fix. Pick the URL and the check, give it an owner and a due date, and update the status. Grey columns show the page score, the weight and whether it is late.')
    head = ['URL', 'Fix (check)', 'Owner', 'Due date', 'Status', 'Notes', 'Page score now', 'Page priority', 'Check weight', 'Check result now', 'Days left', 'Flag']
    fc = (7, 8, 9, 10, 11, 12)
    K.header_row(ws, 4, head, formula_cols=fc, widths=[44, 26, 12, 12, 12, 40, 9, 24, 8, 10, 8, 18])
    for r in range(FX_FIRST, FX_LAST + 1):
        i = r - FX_FIRST
        if i < len(FIXES):
            u, chk, own, due, st, note = FIXES[i]
            for col, v in enumerate([P[u][0], chk, own, d(due), st, note], 1):
                if v not in (None, ''):
                    ws.cell(row=r, column=col, value=v)
        e = f'A{r}=""'
        mt = f'MATCH(A{r},{pa("A")},0)'
        ws.cell(row=r, column=7, value=f'=IF({e},"",IFERROR(INDEX({pa(m["Score (0 to 100)"])},{mt}),""))')
        ws.cell(row=r, column=8, value=f'=IF({e},"",IFERROR(INDEX({pa(m["Priority"])},{mt}),""))')
        ws.cell(row=r, column=9, value=f'=IF(B{r}="","",IFERROR(VLOOKUP(B{r},{S}!$A${CHK_ROW}:$B${CHK_ROW + NCH - 1},2,FALSE),""))')
        res = f'INDEX({PA}!${CK[0]}${PA_FIRST}:${CK[-1]}${PA_LAST},{mt},MATCH(B{r},{PA}!${CK[0]}$4:${CK[-1]}$4,0))'
        ws.cell(row=r, column=10, value=f'=IF(OR({e},B{r}=""),"",IFERROR(IF({res}="","Not checked",IF({res}=1,"OK",IF({res}=0.5,"Partly","Fix"))),""))')
        ws.cell(row=r, column=11, value=f'=IF(OR({e},D{r}=""),"",D{r}-{DATE})')
        ws.cell(row=r, column=12, value=(
            f'=IF({e},"",IF(E{r}="Done",IF(J{r}="OK","Done and verified","Done: recheck the page"),IF(D{r}="","Add a due date",'
            f'IF(K{r}<0,"Overdue",IF(K{r}<=7,"Due this week","On track")))))'))
    K.style_body(ws, FX_FIRST, FX_LAST, len(head), formula_cols=fc, number_formats={4: 'dd mmm yyyy', 7: '0', 11: '0'}, wrap_cols=(6, 8))
    K.dropdown(ws, f'A{FX_FIRST}:A{FX_LAST}', pa('A'))
    K.dropdown(ws, f'B{FX_FIRST}:B{FX_LAST}', f'{S}!$A${CHK_ROW}:$A${CHK_ROW + NCH - 1}')
    K.dropdown(ws, f'E{FX_FIRST}:E{FX_LAST}', f'{S}!$L$6:$L$8')
    fl = f'L{FX_FIRST}:L{FX_LAST}'
    ws.conditional_formatting.add(fl, CellIsRule(operator='equal', formula=['"Overdue"'], fill=PatternFill('solid', fgColor='F8D7D3'), font=Font(name=K.FONT, bold=True, color='9B2C1F')))
    ws.conditional_formatting.add(fl, CellIsRule(operator='equal', formula=['"Due this week"'], fill=PatternFill('solid', fgColor='FFF4CC')))
    ws.conditional_formatting.add(fl, FormulaRule(formula=[f'LEFT(L{FX_FIRST},4)="Done"'], fill=PatternFill('solid', fgColor='D9F2C4')))
    ws.freeze_panes = 'B5'
    ws.auto_filter.ref = f'A4:L{FX_LAST}'
    return ws


def dashboard_sheet(wb, m):
    ws = wb.create_sheet('Dashboard')
    ws.sheet_view.showGridLines = False
    K.title_block(ws, 'Dashboard', 'Everything here calculates from the other tabs. Nothing to type.')
    for c, w in zip('ABCDEFGH', [40, 12, 3, 46, 9, 9, 26, 3]):
        ws.column_dimensions[c].width = w
    sc, gr, pr = m['Score (0 to 100)'], m['Grade'], m['Priority']
    kpis = [
        ('Pages audited', f'=COUNTA({pa("A")})', '0'),
        ('Average score', f'=IFERROR(ROUND(AVERAGE({pa(sc)}),0),0)', '0'),
        ('Grade A pages', f'=COUNTIF({pa(gr)},"A")', '0'),
        ('Grade B pages', f'=COUNTIF({pa(gr)},"B")', '0'),
        ('Grade C pages', f'=COUNTIF({pa(gr)},"C")', '0'),
        ('Grade D pages', f'=COUNTIF({pa(gr)},"D")', '0'),
        ('Fix first: close to the top', f'=COUNTIF({pa(pr)},"Fix first*")', '0'),
        ('Pages nobody links to (orphans)', f'=COUNTIFS({pa("A")},"<>",{pa("M")},0)', '0'),
        ('Pages that are not indexable', f'=COUNTIF({pa("O")},"No")', '0'),
        ('Pages with Good Core Web Vitals', f'=IFERROR(COUNTIF({pa(m["Core Web Vitals status"])},"Good")/(COUNTA({pa("A")})-COUNTIF({pa(m["Core Web Vitals status"])},"No data")),0)', '0%'),
        ('Open fixes on Fix Plan', f"=COUNTIFS('Fix Plan'!$A${FX_FIRST}:$A${FX_LAST},\"<>\",'Fix Plan'!$E${FX_FIRST}:$E${FX_LAST},\"<>Done\")", '0'),
        ('Overdue fixes', f"=COUNTIF('Fix Plan'!$L${FX_FIRST}:$L${FX_LAST},\"Overdue\")", '0'),
    ]
    ws['A4'] = 'KEY NUMBERS'
    ws['A4'].font = K.f(10, True, K.DEEP)
    for i, (label, fml, fmt) in enumerate(kpis):
        r = 5 + i
        ws.cell(row=r, column=1, value=label).font = K.f(10)
        c = ws.cell(row=r, column=2, value=fml)
        c.number_format, c.font, c.fill, c.border = fmt, K.f(11, True), K.FORMULA_FILL, K.BORDER
    for j, h in enumerate(['URL path', 'Score', 'Grade', 'Priority']):
        c = ws.cell(row=4, column=4 + j, value=h)
        c.font, c.fill = K.f(10, True, 'FFFFFF'), K.HEAD_F
    for i in range(15):
        r = 5 + i
        pr_ = PA_FIRST + i
        ws.cell(row=r, column=4, value=f"=IF({PA}!A{pr_}=\"\",\"\",{PA}!{m['URL path']}{pr_})")
        ws.cell(row=r, column=5, value=f"=IF({PA}!A{pr_}=\"\",\"\",{PA}!{sc}{pr_})")
        ws.cell(row=r, column=6, value=f"=IF({PA}!A{pr_}=\"\",\"\",{PA}!{gr}{pr_})")
        ws.cell(row=r, column=7, value=f"=IF({PA}!A{pr_}=\"\",\"\",{PA}!{pr}{pr_})")
        for cc in (4, 5, 6, 7):
            cell = ws.cell(row=r, column=cc)
            cell.border, cell.font, cell.fill = K.BORDER, K.f(9, cc == 4), K.FORMULA_FILL
    ws.conditional_formatting.add('G5:G19', FormulaRule(formula=['LEFT(G5,9)="Fix first"'], fill=PatternFill('solid', fgColor='F8D7D3'), font=Font(name=K.FONT, bold=True)))
    ws.conditional_formatting.add('E5:E19', ColorScaleRule(start_type='num', start_value=30, start_color='F8D7D3', mid_type='num', mid_value=70, mid_color='FFF4CC', end_type='num', end_value=100, end_color='B7E4A0'))
    top = 22
    for j, h in enumerate(['Check', 'Pages to fix', 'Partly']):
        c = ws.cell(row=top, column=1 + j, value=h)
        c.font, c.fill = K.f(10, True, 'FFFFFF'), K.HEAD_F
    for i, col in enumerate(CK):
        r = top + 1 + i
        ws.cell(row=r, column=1, value=f'={S}!A{CHK_ROW + i}').border = K.BORDER
        c = ws.cell(row=r, column=2, value=f'=COUNTIF({pa(col)},0)')
        c.border, c.fill = K.BORDER, K.FORMULA_FILL
        c = ws.cell(row=r, column=3, value=f'=COUNTIF({pa(col)},0.5)')
        c.border, c.fill = K.BORDER, K.FORMULA_FILL
    ws.conditional_formatting.add(f'B{top + 1}:B{top + NCH}', ColorScaleRule(start_type='num', start_value=0, start_color='FFFFFF', end_type='num', end_value=6, end_color='E07A5F'))

    def chart(title, ytitle, cat_col, val_cols, r1, r2, anchor, colors, horiz, titles, h=7.5, stacked=False):
        ch = BarChart()
        ch.type = 'bar' if horiz else 'col'
        ch.title = title
        ch.y_axis.title = ytitle
        for vc in val_cols:
            ch.add_data(Reference(ws, min_col=vc, min_row=r1 - (1 if titles else 0), max_row=r2), titles_from_data=titles)
        ch.set_categories(Reference(ws, min_col=cat_col, min_row=r1, max_row=r2))
        if not titles:
            ch.legend = None
        if stacked:
            ch.grouping = 'stacked'
            ch.overlap = 100
        ch.height, ch.width = h, 16
        ch.x_axis.delete = False
        ch.y_axis.delete = False
        ch.title.overlay = False
        ch.y_axis.title.overlay = False
        for s, col in zip(ch.series, colors):
            s.graphicalProperties.solidFill = col
        ws.add_chart(ch, anchor)
        return ch
    c1 = chart('Score by page', 'Score', 4, [5], 5, 5 + len(P) - 1, 'I4', [K.GREEN], True, False)
    c1.y_axis.scaling.min = 0
    c1.y_axis.scaling.max = 100
    chart('Pages failing each check', 'Pages', 1, [2, 3], top + 1, top + NCH, 'I21', ['E07A5F', 'F2C94C'], True, True, h=11, stacked=True)
    return ws


def build(path, asset, url):
    wb = K.new_book()
    m = audit_sheet(wb)
    report_sheet(wb, m)
    fix_sheet(wb, m)
    dashboard_sheet(wb, m)
    settings_sheet(wb)
    K.prompts_sheet(wb, asset['prompts'], url)
    K.checklist_sheet(wb, list(asset['checklist']))
    K.sources_sheet(wb, asset['sources'], [
        ('Demo data', 'UrbanRoots and every page in the demo are fictional (.example domain). All titles, counts, Core Web Vitals, impressions and positions are illustrative, not real data.', ''),
        ('Score', 'Weighted share of the 19 checks a page passes (pass 1, partly 0.5, fix 0). Checks that do not apply or have no data are left out. Weights, grade bands and priority rules live on Settings and are assumptions to tune.', ''),
        ('Title and description lengths', 'The 30 to 60 and 70 to 160 character bands are assumptions of this kit. Google says there is no limit on meta description length and that snippets are truncated as needed, typically to fit the device width.', ''),
        ('Core Web Vitals', 'Good, Needs improvement and Poor bands for LCP, INP and CLS follow the Search Console Core Web Vitals report, which uses field data from real users. A page status is its worst metric.', ''),
        ('Internal links', 'Google says every page you care about should have a link from at least one other page on your site. The full pass at 3 links is an assumption.', ''),
        ('Word count', 'Shown for context only. It is not scored: Google says content length alone does not matter for ranking.', ''),
    ])
    K.start_here(
        wb, 'On Page SEO Kit',
        [
            'This workbook audits every page on your site against 19 on page checks that matter for Google and for AI answers: indexing, titles, descriptions, headings, the first paragraph, original value, internal links, images, structured data, authorship and Core Web Vitals. Each page gets a score, a grade, its fixes in priority order and a priority based on where it ranks.',
            f'It ships with demo data for a fictional plant shop ({len(P)} pages and {len(FIXES)} fixes) so you can see every check working. Clear the yellow demo cells when you are ready.',
        ],
        [
            ('Page Audit', 'One row per page with 500 ready rows: what you see on the page plus 7 automatic measures, 19 automatic checks, score, grade, fixes and priority.'),
            ('Page Report', 'Pick a URL to get a one page report: every check, the result, what was measured, the rule and how to fix it.'),
            ('Fix Plan', 'Track each fix with an owner, due date and status. It shows the page score, the check result now and overdue fixes.'),
            ('Dashboard', 'Key numbers, score and priority for every page, pages failing each check and two charts.'),
            ('Settings', 'Analysis date, length bands, Core Web Vitals thresholds, grade and priority rules, the 19 check weights with rules and fixes, page types and lists.'),
            ('AI Prompts', 'Prompts for ChatGPT, Claude or Gemini to write titles, descriptions, direct answers, headings, alt text and fix plans.'),
            ('Checklist', 'The on page SEO checklist as a tick list with automatic progress.'),
            ('Sources', 'Where facts come from and which numbers are assumptions.'),
        ],
        [
            'Look at the demo on Page Audit, Page Report and the Dashboard to see how it works, then clear the yellow demo cells.',
            'On Settings, set the analysis date. Change the weights only if your site needs it.',
            'Add your most important pages on Page Audit. Open each live page and its source and fill in the yellow cells.',
            'Add impressions and average position from Search Console and Core Web Vitals from PageSpeed Insights where you have them.',
            'Sort by Priority. Open each Fix first page on Page Report and read the fixes in order.',
            'Add each fix to the Fix Plan with an owner and a due date. After a fix, update the page row and check the result turns OK.',
            'Re audit important pages every quarter and after every redesign.',
        ],
        url,
    )
    order = ['Start Here', 'Page Audit', 'Page Report', 'Fix Plan', 'Dashboard', 'Settings', 'AI Prompts', 'Checklist', 'Sources']
    wb._sheets = [wb[n] for n in order]
    wb.active = 0
    for ws in wb.worksheets:
        ws.sheet_properties.tabColor = K.GREEN if ws.title in ('Start Here', 'Page Audit', 'Page Report', 'Fix Plan', 'Dashboard') else 'A6EF39'
    wb.save(path)


PREVIEW = {'sheet': 'Page Audit', 'header_row': 4, 'rows': 12, 'cols': [28, 2, 29, 30, 34, C0, C0 + 1, C0 + 4, SC, SC + 1, SC + 2, SC + 4],
           'formula_idx': [0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]}


def check(wb):
    """Assert the worked examples used in the guide."""
    a = wb['Page Audit']
    col = {h: L(i + 1) for i, h in enumerate(HEAD)}
    v = lambda h, r: a[f'{col[h]}{r}'].value
    r = 8   # the repotting guide
    assert v('URL path', r) == '/guides/how-to-repot-a-snake-plant/', v('URL path', r)
    assert v('Title characters', r) == 47 and v('Keyword in title', r) == 1 and v('Title length', r) == 1, v('Title characters', r)
    assert v('Keyword in H1', r) == 0.5 and v('Keyword in first paragraph', r) == 0, (v('Keyword in H1', r), v('Keyword in first paragraph', r))
    assert v('Internal links in', r) == 0 and v('Direct answer up top', r) == 0, v('Internal links in', r)
    assert abs(v('Alt coverage', r) - 0.375) < 1e-9 and v('Image alt text', r) == 0, v('Alt coverage', r)
    assert v('Core Web Vitals status', r) == 'Good' and v('Structured data', r) == 0.5 and v('Updated date', r) == 0, v('Core Web Vitals status', r)
    assert v('Question headings', r) == 0, v('Question headings', r)
    assert v('Score (0 to 100)', r) == 60 and v('Grade', r) == 'C', v('Score (0 to 100)', r)
    assert v('Fixes needed', r) == 9, v('Fixes needed', r)
    assert v('Priority', r) == 'Fix first: close to the top', v('Priority', r)
    assert v('Fixes in priority order', r).startswith('Direct answer up top; Internal links in; Keyword in H1 (partly); Keyword in first paragraph'), v('Fixes in priority order', r)
    # other pages used in the guide
    assert v('Grade', 9) == 'A' and v('Priority', 9) == 'Healthy: monitor', (v('Score (0 to 100)', 9), v('Priority', 9))
    assert v('Pages with this description', 10) == 2 and v('Unique description', 11) == 0, v('Pages with this description', 10)
    assert v('Core Web Vitals status', 12) == 'Poor' and v('Core Web Vitals', 12) == 0, v('Core Web Vitals status', 12)
    assert v('Indexable, self canonical', 16) == 0 and v('Priority', 16).startswith('Blocked'), v('Priority', 16)
    assert v('Grade', 6) == 'B' and v('Priority', 6) == 'Fix first: close to the top', v('Score (0 to 100)', 6)
    assert v('Grade', 13) == 'D' and v('Priority', 13) == 'Fix first: close to the top', (v('Score (0 to 100)', 13), v('Priority', 13))
    assert v('Byline', 5) is None and v('Editorial (helper)', 5) == 'No', v('Byline', 5)
    p = wb['Page Report']
    assert p['B8'].value == 60 and p['B20'].value == 'Fix' and p['B21'].value == 'OK', (p['B8'].value, p['B20'].value, p['B21'].value)
    f = wb['Fix Plan']
    assert f['L15'].value == 'Done: recheck the page' and f['J15'].value == 'Fix', (f['L15'].value, f['J15'].value)
    assert f['L16'].value == 'Overdue', f['L16'].value
    assert f['L17'].value == 'Done and verified', f['L17'].value
