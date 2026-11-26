"""Featured Snippet Kit workbook (asset 18, featured snippets).

Snippet Tracker: one row per query (500 rows). You record the organic position, whether a featured snippet shows,
who holds it, the format Google shows, the holder domain, the AI Overview and Search Console numbers. The sheet
recommends a format, shows the target length, pulls snippet controls from the Page Check and the answer score from
the Answer Builder, then sets a status, a next action, an opportunity score, a priority and a recheck date.
Answer Builder: paste a draft answer block (paragraph, list items one per line, or a table size). It counts words,
characters, sentences and items, checks length against the format, the heading, the key term, the format Google
shows and HTML, scores the block 0 to 100 and names the top fix.
Page Check: snippet controls (nosnippet, max-snippet, data-nosnippet, indexing) and five page checks.
Action Plan: fixes by week with hours, how to fix and a before and after result (holder and clicks).
Dashboard sums it all up with three charts.
"""
import datetime
from openpyxl.styles import PatternFill, Font, Alignment
from openpyxl.formatting.rule import CellIsRule, ColorScaleRule, FormulaRule
from openpyxl.chart import BarChart, Reference
from openpyxl.utils import get_column_letter as L
import kitlib as K

QT_FIRST, QT_LAST = 5, 504     # Snippet Tracker (500 rows)
AB_FIRST, AB_LAST = 5, 304     # Answer Builder (300 rows)
PG_FIRST, PG_LAST = 5, 204     # Page Check (200 rows)
AP_FIRST, AP_LAST = 5, 154     # Action Plan (150 rows)
S = 'Settings'
QTS, ABS, PGS, APS = "'Snippet Tracker'", "'Answer Builder'", "'Page Check'", "'Action Plan'"

RULES = [
    ('Today (set it to the day you review the sheet)', datetime.date(2026, 11, 26), 'dd mmm yyyy'),
    ('Monthly searches that earn full demand marks', 5000, '#,##0'),
    ('Check each results page again after (days)', 30, '0'),
    ('P1: work on it now when the score is at least', 70, '0'),
    ('P2: this month when at least', 50, '0'),
    ('P3: this quarter when at least (below = P4: later)', 30, '0'),
    ('Answer is ready when its score is at least', 80, '0'),
    ('Measure results this many days after a fix', 28, '0'),
    ('Fix hours available per week', 10, '0'),
    ('Warn when max-snippet is below (characters)', 320, '0'),
    ('Most sentences in a paragraph answer', 3, '0'),
    ('Most words per list item (average)', 12, '0'),
    ('Most columns in a table answer', 3, '0'),
]
(DATE, FULL, RECHECK, P1, P2, P3, READY, MEASURE, HOURS, MAXSNIP, MAXSENT, MAXITEM, MAXCOLS) = (f'{S}!$B${r}' for r in range(5, 5 + len(RULES)))

FORMATS = ['Paragraph', 'Ordered list', 'Unordered list', 'Table']
SHOWN = FORMATS + ['Video', 'None']
# format, min, max, unit, guidance (assumptions from public studies, see Sources)
FMT = [
    ('Paragraph', 40, 55, 'words', '2 to 3 sentences, about 40 to 55 words, under about 320 characters'),
    ('Ordered list', 4, 8, 'items', '4 to 8 steps, one short step per line, as an HTML ol list'),
    ('Unordered list', 4, 8, 'items', '4 to 8 short items, one per line, as an HTML ul list'),
    ('Table', 3, 5, 'rows', '3 to 5 rows and 2 to 3 short columns, as an HTML table'),
]
FMT_RNG = f'{S}!$D$6:$H$9'
QTYPES = [('Definition', 'Paragraph'), ('How to', 'Ordered list'), ('List or best', 'Unordered list'), ('Comparison', 'Table'),
          ('Number or amount', 'Paragraph'), ('Price or specs', 'Table'), ('Yes or no', 'Paragraph'), ('Why or cause', 'Paragraph'),
          ('Other', 'Paragraph')]
QTYPE_RNG = f'{S}!$D$13:$E$21'
WEIGHTS = [('Demand (monthly searches)', 30), ('Business value', 25), ('Position band', 20), ('Snippet shows', 15), ('Answer gap', 10)]
W_DEM, W_VAL, W_POS, W_SNIP, W_GAP = (f'{S}!$E${r}' for r in range(25, 30))
POSBANDS = [(0, 1, 'Positions 1 to 5'), (5.5, 0.7, 'Positions 6 to 10'), (10.5, 0.35, 'Positions 11 to 20'), (20.5, 0.15, 'Positions 21 to 50'), (50.5, 0.05, 'Beyond 50')]
POS_RNG = f'{S}!$D$34:$E$38'
SNIPF = [('Yes', 1), ('Not checked', 0.5), ('No', 0.2)]
SNIP_RNG = f'{S}!$D$43:$E$45'
# answer check, weight, what it tests
CHECKS = [
    ('Length fits the format', 25, 'Words for a paragraph, items for a list, rows for a table, compared with the format table. Full points in range, half points within 25 percent of it.'),
    ('Heading states the question', 10, 'A heading right above the block that ends with a question mark or contains the key term.'),
    ('Key term early', 10, 'The key term appears in the first 150 characters of the answer (half points if it appears later).'),
    ('Answer comes right after the heading', 15, 'Typed: Yes, Partly or No. No intro, no story, the answer first.'),
    ('Short sentences or items', 10, 'Paragraph: at most the set number of sentences. List: short items on average. Table: at most the set number of columns.'),
    ('Matches the format Google shows', 20, 'Same format as the snippet shown now, or the recommended format when none shows. Half points for the other kind of list.'),
    ('Built with HTML tags', 10, 'Typed: Yes when the block is real text in p, ol, ul or table tags, not an image or a script.'),
]
CHK_FIRST = 6
CW = [f'{S}!$K${CHK_FIRST + k}' for k in range(len(CHECKS))]
STATUSES = [
    ('Add a target page', 'Choose the page that should answer this query and add it to the Page Check.'),
    ('Check the results page', 'Search the query in a private window. Record the snippet, who holds it, the format and the AI Overview.'),
    ('Fix snippet controls first', 'The page blocks snippets (nosnippet, data-nosnippet on the answer) or is not indexed. Fix it on the Page Check before anything else.'),
    ('Held: protect it', 'You hold the snippet. Keep the answer block, the facts and the date current, and check it every month.'),
    ('No snippet, AI Overview shows: aim for a citation', 'No featured snippet, but an AI Overview shows. Keep a clear answer block and depth so the page can be cited.'),
    ('No snippet: classic SEO', 'No featured snippet shows. Work on the title, description and depth. Check again next cycle.'),
    ('Not top 10: rank first', 'Nearly every featured snippet comes from a page in the top 10. Improve the page and its links before polishing the answer.'),
    ('Top 5: win it with a better answer block', 'You are close. Match the format Google shows, answer right under a question heading and fit the target length.'),
    ('Ranks 6 to 10: sharpen the answer and climb', 'Write a tight answer block now, then add depth and internal links to move into the top 5.'),
]
ST_RNG = f'{S}!$J$19:$K$27'
FIXES = [
    ('Write an answer block under a question heading', 1, 'Add a heading that asks the query, then answer it in the first sentence or list right below.'),
    ('Trim or expand the answer to the target length', 0.5, 'Use the Answer Builder. Cut extra words or add the missing detail until the length fits.'),
    ('Change the answer to a numbered list', 1, 'Turn the steps into an HTML ol list, one short step per line, in order.'),
    ('Change the answer to a bulleted list', 1, 'Turn the items into an HTML ul list, one short item per line.'),
    ('Add an HTML table', 2, 'Build a real HTML table with a header row, 3 to 5 rows and 2 to 3 short columns.'),
    ('Put the key term in the first sentence', 0.5, 'Start the answer with the subject of the query, in the words people search.'),
    ('Fix snippet controls (nosnippet, max-snippet, data-nosnippet)', 1, 'Remove nosnippet, raise or remove a low max-snippet and remove data-nosnippet from the answer.'),
    ('Get the page indexed', 2, 'Run URL Inspection in Search Console. Fix noindex, canonical or quality problems, then request indexing.'),
    ('Improve the page to rank top 5', 8, 'Add depth the top results lack, original examples and internal links from related pages.'),
    ('Refresh facts and the visible date', 2, 'Check every number and rule against a current source and update the Last updated date.'),
    ('Add a short how to video with chapters', 6, 'Record the steps, add chapters and a transcript, and embed it near the answer.'),
    ('Add internal links with the query as anchor', 1, 'Link to the page from 2 or more related pages using descriptive anchor text.'),
]
FIX_FIRST = 32
FIX_RNG_NAME = f'{S}!$J${FIX_FIRST}:$J${FIX_FIRST + len(FIXES) - 1}'
YNC = ['Yes', 'No', 'Not checked']
YPN = ['Yes', 'Partly', 'No']
HOLDER = ['You', 'Competitor', 'Not checked']
AIO = ['Yes', 'Sometimes', 'No', 'Not checked']
OWNERS = ['Tara (editor)', 'Dev (writer)', 'SEO', 'Developer', 'Barista expert']
WEEKS = [f'Week {i}' for i in range(1, 9)]
ASTAT = ['To do', 'Doing', 'Done']
BSTAT = ['Draft', 'Approved', 'Live']
BEFORE = ['You', 'Competitor', 'No snippet']

# Demo: BrewNest, a fictional home coffee gear shop with a brewing guides section (brewnest.example). Illustrative numbers.
U = 'https://brewnest.example'
Y, N_, NC, P_ = 'Yes', 'No', 'Not checked', 'Partly'
# url, title, indexed, nosnippet, max-snippet, data-nosnippet, html text, question headings, html lists, date+author, facts, notes
PAGES = [
    ('/guides/cold-brew-coffee/', 'How to make cold brew coffee at home', Y, N_, None, N_, Y, Y, Y, Y, Y, 'Worked example in the guide'),
    ('/guides/french-press-ratio/', 'French press coffee ratio and recipe', Y, N_, None, N_, Y, P_, Y, Y, P_, ''),
    ('/guides/flat-white/', 'What is a flat white?', Y, N_, None, N_, Y, Y, Y, P_, Y, ''),
    ('/guides/best-grinders-for-beginners/', 'Best coffee grinders for beginners', Y, N_, None, N_, Y, P_, Y, Y, N_, 'Prices need a refresh'),
    ('/guides/pour-over-vs-french-press/', 'Pour over vs French press', Y, N_, None, N_, Y, Y, Y, Y, Y, ''),
    ('/guides/descale-coffee-machine/', 'How to descale a coffee machine', Y, N_, None, N_, Y, Y, Y, Y, Y, 'Holds the snippet'),
    ('/guides/sour-espresso/', 'Why is my espresso sour?', Y, N_, None, N_, Y, N_, P_, N_, Y, ''),
    ('/guides/caffeine-in-coffee-drinks/', 'Caffeine in coffee drinks', Y, N_, None, Y, Y, Y, Y, Y, Y, 'Theme wraps the article body in data-nosnippet'),
    ('/guides/coffee-ratio-chart/', 'Coffee to water ratio chart', Y, N_, 120, N_, P_, Y, Y, Y, Y, 'SEO plugin sets max-snippet:120'),
    ('/products/burr-grinders/', 'Burr coffee grinders', Y, N_, None, N_, Y, N_, N_, NC, Y, 'Product category page'),
]
# query, page index (None = no page), topic, query type, searches, value, position, snippet shows, holder, format shown,
# holder domain, aio, cited in aio, clicks, impressions, checked
QUERIES = [
    ('how to make cold brew coffee', 0, 'Cold brew', 'How to', 6600, 2, 3.4, Y, 'Competitor', 'Ordered list', 'coffeemag.example', 'Sometimes', N_, 410, 21000, '2026-11-20'),
    ('how long to steep cold brew', 0, 'Cold brew', 'Number or amount', 2400, 2, 2.1, Y, 'You', 'Paragraph', 'brewnest.example', N_, NC, 380, 9800, '2026-11-20'),
    ('french press coffee ratio', 1, 'French press', 'Number or amount', 3600, 2, 4.8, Y, 'Competitor', 'Table', 'beanblog.example', Y, N_, 260, 15000, '2026-11-21'),
    ('what is a flat white', 2, 'Espresso drinks', 'Definition', 9900, 1, 7.2, Y, 'Competitor', 'Paragraph', 'cafeguide.example', Y, N_, 190, 33000, '2026-11-21'),
    ('best coffee grinder for beginners', 3, 'Grinders', 'List or best', 2900, 3, 8.5, Y, 'Competitor', 'Unordered list', 'gearreview.example', 'Sometimes', N_, 120, 12000, '2026-11-22'),
    ('pour over vs french press', 4, 'Brewing methods', 'Comparison', 1900, 2, 5.0, Y, 'Competitor', 'Table', 'coffeemag.example', Y, Y, 150, 8200, '2026-11-22'),
    ('how to descale a coffee machine', 5, 'Cleaning', 'How to', 4400, 2, 1.6, Y, 'You', 'Ordered list', 'brewnest.example', N_, NC, 900, 19000, '2026-11-19'),
    ('why is my espresso sour', 6, 'Espresso drinks', 'Why or cause', 1300, 2, 12.0, Y, 'Competitor', 'Paragraph', 'beanblog.example', Y, N_, 30, 4100, '2026-11-23'),
    ('how much caffeine in espresso', 7, 'Caffeine', 'Number or amount', 8100, 1, 6.1, Y, 'Competitor', 'Paragraph', 'healthsite.example', Y, N_, 210, 30000, '2026-11-18'),
    ('coffee to water ratio chart', 8, 'Ratios', 'Comparison', 1600, 2, 3.0, Y, 'Competitor', 'Table', 'coffeemag.example', N_, NC, 140, 7000, '2026-11-23'),
    ('burr vs blade grinder', 3, 'Grinders', 'Comparison', 1000, 3, 9.6, N_, '', 'None', '', Y, N_, 40, 3900, '2026-11-22'),
    ('burr grinder', 9, 'Grinders', 'Other', 5400, 3, 14.0, N_, '', 'None', '', N_, NC, 60, 9000, '2026-11-22'),
    ('how to clean a french press', 1, 'Cleaning', 'How to', 1300, 1, 22.0, Y, 'Competitor', 'Ordered list', 'cleanhome.example', 'Sometimes', N_, 5, 1900, '2026-11-23'),
    ('is cold brew stronger than coffee', 0, 'Cold brew', 'Yes or no', 1600, 2, 6.8, Y, 'Competitor', 'Paragraph', 'cafeguide.example', Y, N_, 70, 6400, '2026-11-20'),
    ('aeropress recipe', None, 'Brewing methods', 'How to', 2400, 2, None, NC, '', '', '', NC, NC, None, None, ''),
    ('moka pot vs espresso machine', 4, 'Brewing methods', 'Comparison', 880, 2, None, NC, '', '', '', NC, NC, None, None, ''),
]
# query index, key term, format, heading, answer text (lines), table rows, table cols, right after heading, html, status
ANSWERS = [
    (0, 'cold brew', 'Ordered list', 'How to make cold brew coffee at home', [
        'Grind 100 g of coffee beans coarse, like rough sand.',
        'Add the grounds to a jar with 1 litre of cold water.',
        'Stir gently so all the grounds are wet.',
        'Cover and steep in the fridge for 12 to 18 hours.',
        'Strain through a paper filter or a fine mesh sieve.',
        'Dilute the cold brew concentrate 1 to 1 with water or milk.',
        'Serve over ice and keep the rest chilled for up to a week.'], None, None, Y, Y, 'Approved'),
    (3, 'flat white', 'Paragraph', 'What is a flat white?', [
        'Many people ask us about this drink in the shop. A flat white is an espresso drink made with a double shot of espresso and '
        'steamed milk that has a thin layer of velvety microfoam. It is smaller than a latte, usually 150 to 180 ml, so the coffee '
        'tastes stronger. It started in Australia and New Zealand. Baristas pour it with latte art on top.'], None, None, P_, Y, 'Draft'),
    (2, 'french press', 'Table', 'French press coffee ratio chart', [
        'Cups | Coffee | Water', '1 cup | 15 g | 250 ml', '2 cups | 30 g | 500 ml', '3 cups | 45 g | 750 ml', '4 cups | 60 g | 1 litre'], 5, 3, Y, Y, 'Live'),
    (4, 'coffee grinder', 'Unordered list', 'Best coffee grinder for beginners', [
        'Manual burr grinder: cheap, quiet and consistent for one or two cups',
        'Entry level electric burr grinder: fast, with 15 or more grind settings',
        'Flat burr grinder: very even grind for pour over and espresso',
        'Blade grinder: only if your budget is very tight',
        'Look for: easy cleaning, a clear grind scale and a 1 year warranty'], None, None, Y, Y, 'Live'),
    (5, 'pour over', 'Table', 'Pour over vs French press: key differences', [
        'Feature | Pour over | French press', 'Taste | Clean, bright | Full, heavy', 'Grind | Medium fine | Coarse',
        'Brew time | 3 to 4 minutes | 4 minutes', 'Filter | Paper | Metal mesh', 'Effort | Hands on | Easy', 'Best for | One cup | Sharing'], 7, 3, Y, Y, 'Draft'),
    (8, 'caffeine', 'Paragraph', 'How much caffeine is in espresso?', [
        'A single shot of espresso (about 30 ml) usually has about 60 to 75 mg of caffeine, and a double shot about 120 to 150 mg. '
        'The exact amount depends on the beans, the roast and the shot size. Per ml, espresso has more caffeine than drip coffee, '
        'but a full mug of drip coffee often has more in total.'], None, None, Y, Y, 'Live'),
    (13, 'cold brew', 'Paragraph', 'Is cold brew stronger than regular coffee?', [
        'Cold brew concentrate is stronger than regular coffee, but most people dilute it 1 to 1 with water or milk. '
        'Once diluted, a glass of cold brew has about the same caffeine as a cup of hot drip coffee. It tastes smoother '
        'and less acidic because the coffee never touches hot water.'], None, None, Y, Y, 'Draft'),
    (7, 'sour', 'Unordered list', 'Why is my espresso sour?', [
        'The grind is too coarse', 'The shot runs too fast', 'The water is too cool', 'The beans are roasted too light'], None, None, N_, Y, 'Draft'),
]
# query index, fix index, owner, week, status, done on, holder before, holder after, clicks before, clicks after
ACTIONS = [
    (8, 6, 'Developer', 'Week 1', 'Done', '2026-11-14', 'Competitor', None, 190, None),
    (0, 5, 'Dev (writer)', 'Week 1', 'To do', None, 'Competitor', None, None, None),
    (3, 1, 'Dev (writer)', 'Week 1', 'Doing', None, 'Competitor', None, None, None),
    (7, 0, 'Dev (writer)', 'Week 2', 'To do', None, 'Competitor', None, None, None),
    (9, 6, 'Developer', 'Week 2', 'To do', None, 'Competitor', None, None, None),
    (6, 9, 'Tara (editor)', None, 'Done', '2026-10-10', 'You', 'You', 800, 900),
    (1, 0, 'Dev (writer)', None, 'Done', '2026-10-05', 'Competitor', 'You', 210, 380),
    (4, 8, 'SEO', 'Week 3', 'To do', None, 'Competitor', None, None, None),
]
FLAT_WHITE_TRIMMED = ('A flat white is an espresso drink made with a double shot of espresso and steamed milk that has a thin layer of velvety '
                      'microfoam. It is smaller than a latte, usually 150 to 180 ml, so the coffee tastes stronger.')
DOMAINS = ['coffeemag.example', 'beanblog.example', 'cafeguide.example', 'gearreview.example', 'healthsite.example', 'cleanhome.example', 'brewnest.example']

QT_IN = ['Query', 'Target URL', 'Topic', 'Query type', 'Monthly searches', 'Business value (1 to 3)', 'Organic position',
         'Featured snippet shows?', 'Who holds it?', 'Format shown', 'Holder domain', 'AI Overview shows?', 'Cited in the AI Overview?',
         'Clicks (28 days)', 'Impressions (28 days)', 'Date checked', 'Notes']
QT_FH = ['CTR', 'Recommended format', 'Target length', 'Snippet controls', 'Answer score (0 to 100)', 'Answer verdict', 'Status',
         'Next action', 'Opportunity score (0 to 100)', 'Priority', 'Days since checked', 'Check again?', 'Rank (helper)']
QT_HEAD = QT_IN + QT_FH
QC = {h: L(i + 1) for i, h in enumerate(QT_HEAD)}
QT_F = tuple(range(len(QT_IN) + 1, len(QT_HEAD) + 1))

AB_IN = ['Query', 'Key term', 'Answer format', 'Heading above the answer', 'Answer text (lists and tables: one item or row per line)',
         'Table rows', 'Table columns', 'Answer comes right after the heading?', 'Built with HTML tags?', 'Status', 'Notes']
AB_FH = ['Target URL', 'Format shown', 'Recommended format', 'Words', 'Characters', 'Sentences (approx.)', 'Lines or items',
         'Words per item', 'Length measured', 'Target range', 'Length fit', 'Answer score (0 to 100)', 'Verdict', 'Top fix']
GAPS = [f'Gap: {i + 1}' for i in range(len(CHECKS))]
AB_HEAD = AB_IN + AB_FH + GAPS
AC = {h: L(i + 1) for i, h in enumerate(AB_HEAD)}
AB_F = tuple(range(len(AB_IN) + 1, len(AB_HEAD) + 1))

PG_IN = ['URL', 'Page title', 'Indexed in Google?', 'Robots nosnippet?', 'max-snippet value (blank = not set)', 'data-nosnippet on the answer?',
         'Answer is HTML text (not an image)?', 'Question headings (H2 or H3)?', 'Lists and tables use HTML tags?', 'Visible date and author?',
         'Facts checked in the last 12 months?', 'Notes']
PG_FH = ['Snippet controls', 'Page score (0 to 100)', 'Queries targeting this page', 'Snippets showing', 'Snippets you hold', 'Win rate', 'Next step']
PG_HEAD = PG_IN + PG_FH
PGC = {h: L(i + 1) for i, h in enumerate(PG_HEAD)}
PG_F = tuple(range(len(PG_IN) + 1, len(PG_HEAD) + 1))


def qt(h):
    c = QC.get(h, h)
    return f'{QTS}!${c}${QT_FIRST}:${c}${QT_LAST}'


def ab(h):
    c = AC.get(h, h)
    return f'{ABS}!${c}${AB_FIRST}:${c}${AB_LAST}'


def pg(h):
    c = PGC.get(h, h)
    return f'{PGS}!${c}${PG_FIRST}:${c}${PG_LAST}'


def d(s):
    return datetime.date.fromisoformat(s) if s else None


def settings_sheet(wb):
    ws = wb.create_sheet(S)
    ws.sheet_view.showGridLines = False
    K.title_block(ws, 'Settings', 'Every rule, weight, length and list used by this workbook. Change a blue value and every score, status and priority updates.')
    for c, w in zip('ABCDEFGHIJKLMNOPQRSTUV', [50, 14, 3, 30, 10, 10, 9, 52, 3, 50, 10, 60, 3, 16, 18, 16, 16, 18, 16, 12, 10, 14]):
        ws.column_dimensions[c].width = w
    ws['A4'] = 'RULES'
    ws['A4'].font = K.f(10, True, K.DEEP)
    for i, (label, val, fmt) in enumerate(RULES):
        r = 5 + i
        ws.cell(row=r, column=1, value=label).font = K.f(10)
        c = ws.cell(row=r, column=2, value=val)
        c.border, c.fill, c.font, c.number_format = K.BORDER, K.INPUT_FILL, K.f(10, True, '0000FF'), fmt
    ws['A20'] = ('Opportunity score = demand weight x MIN(1, searches / full marks) + value weight x value / 3 + position weight x '
                 'position band factor + snippet weight x snippet factor + gap weight x (1 minus answer score / 100). Answer score = the '
                 'sum of each answer check weight x its points (1, 0.5 or 0). Google does not publish snippet lengths: the format '
                 'lengths, weights, bands, factors and hours on this tab are assumptions of this kit, based on the public studies on '
                 'the Sources tab. Tune them to what you see in your own results.')
    ws['A20'].font = K.f(9, False, '777777', True)
    ws['A20'].alignment = Alignment(wrap_text=True, vertical='top')
    ws.merge_cells('A20:B34')

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
    table(4, 5, 'ANSWER FORMATS AND TARGET LENGTHS (assumptions)', ['Format', 'Min', 'Max', 'Unit', 'Guidance'], FMT, ['@', '0', '0', '@', '@'], blue=(1, 2))
    table(4, 12, 'QUERY TYPE TO FORMAT (when no snippet shows yet)', ['Query type', 'Format'], QTYPES, blue=(1,))
    table(4, 24, 'OPPORTUNITY WEIGHTS (add up to 100)', ['Factor', 'Weight'], WEIGHTS)
    ws['D30'] = 'Total'
    ws['E30'] = '=SUM(E25:E29)'
    ws['E30'].fill, ws['E30'].font = K.FORMULA_FILL, K.f(10, True)
    table(4, 33, 'POSITION BAND (organic position)', ['At least', 'Factor', 'Meaning'], POSBANDS, ['0.0', '0.00', '@'])
    table(4, 42, 'SNIPPET FACTOR', ['Snippet shows?', 'Factor'], SNIPF, ['@', '0.0'])
    table(10, 5, 'ANSWER CHECKS (weights add up to 100)', ['Check', 'Weight', 'What it tests'], CHECKS, ['@', '0', '@'])
    ws['J13'] = 'Total weight'
    ws['K13'] = f'=SUM(K{CHK_FIRST}:K{CHK_FIRST + len(CHECKS) - 1})'
    ws['K13'].fill, ws['K13'].font = K.FORMULA_FILL, K.f(10, True)
    table(10, 18, 'STATUS AND NEXT ACTION (query level)', ['Status', 'Next action'], STATUSES, blue=())
    table(10, FIX_FIRST - 1, 'FIXES, HOURS (assumptions) AND HOW TO FIX', ['Fix', 'Hours', 'How to fix'], FIXES, ['@', '0.0', '@'])
    for r in list(range(6, 13)) + list(range(19, 28)) + list(range(FIX_FIRST, FIX_FIRST + len(FIXES))):
        ws.row_dimensions[r].height = 30
    lists = [('N', 'Format shown', SHOWN), ('O', 'Query type', [q[0] for q in QTYPES]), ('P', 'Yes, No, Not checked', YNC),
             ('Q', 'Yes, Partly, No', YPN), ('R', 'Who holds it?', HOLDER), ('S', 'AI Overview shows?', AIO), ('T', 'Owner', OWNERS),
             ('U', 'Week', WEEKS), ('V', 'Holder before or after', BEFORE)]
    ws['N4'] = 'LISTS (used by the dropdowns)'
    ws['N4'].font = K.f(10, True, K.DEEP)
    for col, head, vals in lists:
        ws[f'{col}5'] = head
        ws[f'{col}5'].font = K.f(9, True, '555555')
        n = 12 if col == 'T' else len(vals)
        for i in range(n):
            c = ws[f'{col}{6 + i}']
            c.value = vals[i] if i < len(vals) else None
            c.fill, c.border, c.font = K.INPUT_FILL, K.BORDER, K.f(10)
    for col, head, vals in (('N', 'Answer format', FORMATS), ('O', 'Action status', ASTAT), ('P', 'Answer status', BSTAT)):
        ws[f'{col}20'] = head
        ws[f'{col}20'].font = K.f(9, True, '555555')
        for i, v in enumerate(vals):
            c = ws[f'{col}{21 + i}']
            c.value, c.fill, c.border, c.font = v, K.INPUT_FILL, K.BORDER, K.f(10)
    return ws


def val(cell):
    return f'IF({cell}="Yes",1,IF({cell}="Partly",0.5,0))'


def page_sheet(wb):
    ws = wb.create_sheet('Page Check')
    ws.sheet_view.showGridLines = False
    K.title_block(ws, 'Page check', f'One row per page that targets a snippet. Rows 5 to {4 + len(PAGES)} are DEMO pages for BrewNest, a fictional coffee gear shop (illustrative). 200 rows ready.')
    ws['A2'].font = K.f(10, True, 'B45309')
    ws['A3'] = ('Snippet controls first: a robots nosnippet rule, max-snippet:0 or data-nosnippet on the answer keeps the text out of '
                'featured snippets. View the page source or use URL Inspection in Search Console to check.')
    ws['A3'].font = K.f(9, False, '666666', True)
    K.header_row(ws, 4, PG_HEAD, formula_cols=PG_F, widths=[38, 32, 11, 11, 12, 13, 12, 12, 12, 11, 12, 30, 30, 10, 10, 10, 10, 9, 48])
    for r in range(PG_FIRST, PG_LAST + 1):
        i = r - PG_FIRST
        if i < len(PAGES):
            p = PAGES[i]
            for col, v in enumerate([U + p[0]] + list(p[1:]), 1):
                if v not in (None, ''):
                    ws.cell(row=r, column=col, value=v)
        e = f'A{r}=""'
        ws[f'M{r}'] = (f'=IF({e},"",IF(C{r}="No","Blocked: not indexed",IF(OR(D{r}="Yes",AND(E{r}<>"",N(E{r})=0)),"Blocked: nosnippet",'
                       f'IF(F{r}="Yes","Blocked: data-nosnippet on the answer",IF(AND(N(E{r})>0,N(E{r})<{MAXSNIP}),"Risk: max-snippet "&E{r}&" is low",'
                       f'IF(OR(C{r}="Not checked",C{r}="",D{r}="Not checked",D{r}="",F{r}="Not checked",F{r}=""),"Check the controls","Allowed"))))))')
        ws[f'N{r}'] = '=IF({},"",ROUND(20*({}),0))'.format(e, '+'.join(val(f'{c}{r}') for c in 'GHIJK'))
        ws[f'O{r}'] = f'=IF({e},"",COUNTIF({qt("B")},A{r}))'
        ws[f'P{r}'] = f'=IF({e},"",COUNTIFS({qt("B")},A{r},{qt("H")},"Yes"))'
        ws[f'Q{r}'] = f'=IF({e},"",COUNTIFS({qt("B")},A{r},{qt("H")},"Yes",{qt("I")},"You"))'
        ws[f'R{r}'] = f'=IF(OR({e},N(P{r})=0),"",Q{r}/P{r})'
        ws[f'S{r}'] = (f'=IF({e},"",IF(LEFT(M{r},7)="Blocked","Fix the controls: "&MID(M{r},10,60),IF(LEFT(M{r},4)="Risk","Raise or remove max-snippet",'
                       f'IF(M{r}="Check the controls","Check robots meta, max-snippet and data-nosnippet",IF(G{r}<>"Yes","Put the answer in HTML text",'
                       f'IF(I{r}<>"Yes","Use real HTML lists and tables",IF(H{r}<>"Yes","Add question headings",IF(K{r}<>"Yes","Check the facts",'
                       f'IF(J{r}<>"Yes","Show a date and author","Page is snippet ready")))))))))')
    K.style_body(ws, PG_FIRST, PG_LAST, len(PG_HEAD), formula_cols=PG_F, number_formats={5: '0', 14: '0', 15: '0', 16: '0', 17: '0', 18: '0%'},
                 wrap_cols=(1, 2, 12, 13, 19))
    for col in 'CDF':
        K.dropdown(ws, f'{col}{PG_FIRST}:{col}{PG_LAST}', f'{S}!$P$6:$P$8')
    K.dropdown(ws, f'G{PG_FIRST}:K{PG_LAST}', f'{S}!$Q$6:$Q$8', 'Yes, Partly or No.')
    K.whole_number(ws, f'E{PG_FIRST}:E{PG_LAST}', -1, 100000, 'A number of characters. -1 lets Google choose; 0 works like nosnippet.')
    rng = f'G{PG_FIRST}:K{PG_LAST}'
    for txt, fill, fc in (('Yes', 'D9F2C4', '3D7F12'), ('Partly', 'FFF4CC', '1F1F1F'), ('No', 'F8D7D3', '9B2C1F')):
        ws.conditional_formatting.add(rng, CellIsRule(operator='equal', formula=[f'"{txt}"'], fill=PatternFill('solid', fgColor=fill), font=Font(name=K.FONT, color=fc)))
    m = f'M{PG_FIRST}:M{PG_LAST}'
    ws.conditional_formatting.add(m, FormulaRule(formula=[f'LEFT(M{PG_FIRST},7)="Blocked"'], fill=PatternFill('solid', fgColor='9B2C1F'), font=Font(name=K.FONT, bold=True, color='FFFFFF')))
    ws.conditional_formatting.add(m, FormulaRule(formula=[f'LEFT(M{PG_FIRST},4)="Risk"'], fill=PatternFill('solid', fgColor='FCE5CD'), font=Font(name=K.FONT, bold=True)))
    ws.conditional_formatting.add(m, CellIsRule(operator='equal', formula=['"Allowed"'], fill=PatternFill('solid', fgColor='D9F2C4'), font=Font(name=K.FONT, bold=True, color='3D7F12')))
    ws.conditional_formatting.add(f'N{PG_FIRST}:N{PG_LAST}', ColorScaleRule(start_type='num', start_value=0, start_color='F8D7D3', mid_type='num', mid_value=60, mid_color='FFF4CC', end_type='num', end_value=100, end_color='8BC34A'))
    for r in range(PG_FIRST, PG_FIRST + len(PAGES)):
        ws.row_dimensions[r].height = 30
    ws.freeze_panes = 'B5'
    ws.auto_filter.ref = f'A4:S{PG_LAST}'
    return ws


def answer_sheet(wb):
    ws = wb.create_sheet('Answer Builder')
    ws.sheet_view.showGridLines = False
    K.title_block(ws, 'Answer builder', f'Paste the answer block you plan to publish. Rows 5 to {4 + len(ANSWERS)} are DEMO answers for BrewNest (fictional). 300 rows ready.')
    ws['A2'].font = K.f(10, True, 'B45309')
    ws['A3'] = ('Lists: one item per line (Alt+Enter in Excel, Ctrl+Enter in Google Sheets). Tables: type the rows and columns, and paste the '
                'rows if you like. The sheet counts words, sentences and items, checks the length and format, and scores the block.')
    ws['A3'].font = K.f(9, False, '666666', True)
    widths = [30, 14, 14, 30, 62, 8, 8, 12, 10, 10, 20, 34, 13, 13, 8, 9, 9, 8, 8, 9, 13, 12, 10, 13, 40] + [6] * len(GAPS)
    K.header_row(ws, 4, AB_HEAD, formula_cols=AB_F, widths=widths)
    c = AC
    fmt = lambda col: f'VLOOKUP(C{{r}},{FMT_RNG},{col},FALSE)'
    for r in range(AB_FIRST, AB_LAST + 1):
        i = r - AB_FIRST
        if i < len(ANSWERS):
            qi, key, fm, hd, lines, rows, cols, direct, html, st = ANSWERS[i]
            for col, v in enumerate([QUERIES[qi][0], key, fm, hd, '\n'.join(lines), rows, cols, direct, html, st], 1):
                if v not in (None, ''):
                    ws.cell(row=r, column=col, value=v)
        e = f'A{r}=""'
        g = lambda h: f'{c[h]}{r}'
        m = f'MATCH(A{r},{qt("A")},0)'
        txt = f'TRIM(SUBSTITUTE(E{r},CHAR(10)," "))'
        f = {}
        f['Target URL'] = f'=IF({e},"",IFERROR(INDEX({qt("B")},{m})&"","Query not in the tracker"))'
        f['Format shown'] = f'=IF({e},"",IFERROR(INDEX({qt("J")},{m})&"",""))'
        f['Recommended format'] = f'=IF({e},"",IFERROR(INDEX({qt("Recommended format")},{m})&"",""))'
        f['Words'] = f'=IF({e},"",IF({txt}="",0,LEN({txt})-LEN(SUBSTITUTE({txt}," ",""))+1))'
        f['Characters'] = f'=IF({e},"",LEN({txt}))'
        f['Sentences (approx.)'] = (f'=IF({e},"",IF({txt}="",0,(LEN({txt})-LEN(SUBSTITUTE({txt},". ","")))/2+(LEN({txt})-LEN(SUBSTITUTE({txt},"? ","")))/2'
                                    f'+(LEN({txt})-LEN(SUBSTITUTE({txt},"! ","")))/2+IF(OR(RIGHT({txt},1)=".",RIGHT({txt},1)="?",RIGHT({txt},1)="!"),1,0)))')
        f['Lines or items'] = f'=IF({e},"",IF(TRIM(E{r})="",0,LEN(TRIM(E{r}))-LEN(SUBSTITUTE(TRIM(E{r}),CHAR(10),""))+1))'
        f['Words per item'] = f'=IF(OR({e},N({g("Lines or items")})=0),"",{g("Words")}/{g("Lines or items")})'
        f['Length measured'] = (f'=IF(OR({e},C{r}=""),"",IF(C{r}="Paragraph",{g("Words")},IF(C{r}="Table",IF(F{r}="",{g("Lines or items")},F{r}),'
                                f'{g("Lines or items")})))')
        f['Target range'] = f'=IF(OR({e},C{r}=""),"",IFERROR({fmt(2).format(r=r)}&" to "&{fmt(3).format(r=r)}&" "&{fmt(4).format(r=r)},""))'
        lm = g('Length measured')
        lo, hi = fmt(2).format(r=r), fmt(3).format(r=r)
        f['Length fit'] = (f'=IF(OR({e},C{r}=""),"",IFERROR(IF({lm}<{lo},"Too short",IF({lm}>{hi},"Too long","In range")),""))')
        target = f'IF(OR({g("Format shown")}="Paragraph",{g("Format shown")}="Ordered list",{g("Format shown")}="Unordered list",{g("Format shown")}="Table"),{g("Format shown")},{g("Recommended format")})'
        pts = {}
        pts[0] = f'IFERROR(IF(AND({lm}>={lo},{lm}<={hi}),1,IF(AND({lm}>={lo}*0.75,{lm}<={hi}*1.25),0.5,0)),0)'
        pts[1] = f'IF(D{r}="",0,IF(OR(RIGHT(TRIM(D{r}),1)="?",AND(B{r}<>"",ISNUMBER(SEARCH(B{r},D{r})))),1,0.5))'
        pts[2] = f'IF(OR(B{r}="",E{r}=""),0,IF(ISNUMBER(SEARCH(B{r},LEFT({txt},150))),1,IF(ISNUMBER(SEARCH(B{r},E{r})),0.5,0)))'
        pts[3] = val(f'H{r}')
        pts[4] = (f'IF(C{r}="Paragraph",IF({g("Sentences (approx.)")}<={MAXSENT},1,IF({g("Sentences (approx.)")}<={MAXSENT}+1,0.5,0)),'
                  f'IF(C{r}="Table",IF(N(G{r})=0,0.5,IF(G{r}<={MAXCOLS},1,0.5)),IF(N({g("Words per item")})=0,0,IF({g("Words per item")}<={MAXITEM},1,IF({g("Words per item")}<={MAXITEM}*1.5,0.5,0)))))')
        pts[5] = f'IF(C{r}={target},1,IF(AND(ISNUMBER(SEARCH("list",C{r})),ISNUMBER(SEARCH("list",{target}))),0.5,0))'
        pts[6] = f'IF(I{r}="Yes",1,0)'
        for k in range(len(CHECKS)):
            f[GAPS[k]] = f'=IF(OR({e},C{r}=""),"",{CW[k]}*(1-{pts[k]}))'
        gr = f'{c[GAPS[0]]}{r}:{c[GAPS[-1]]}{r}'
        f['Answer score (0 to 100)'] = f'=IF(OR({e},C{r}=""),"",ROUND({S}!$K$13-SUM({gr}),0))'
        sc = g('Answer score (0 to 100)')
        f['Verdict'] = (f'=IF({e},"",IF(C{r}="","Choose a format",IF(AND(E{r}="",C{r}<>"Table"),"Write the answer",IF({sc}>={READY},"Ready to publish",'
                        f'IF({sc}>=60,"Nearly ready","Needs work")))))')
        f['Top fix'] = (f'=IF(OR({e},C{r}=""),"",IF(MAX({gr})=0,"None: publish it",INDEX({S}!$J${CHK_FIRST}:$J${CHK_FIRST + len(CHECKS) - 1},MATCH(MAX({gr}),{gr},0))'
                        f'&IF(INDEX({S}!$J${CHK_FIRST}:$J${CHK_FIRST + len(CHECKS) - 1},MATCH(MAX({gr}),{gr},0))="Length fits the format",": "&LOWER({g("Length fit")})&", aim for "&{g("Target range")},"")'
                        f'&IF(INDEX({S}!$J${CHK_FIRST}:$J${CHK_FIRST + len(CHECKS) - 1},MATCH(MAX({gr}),{gr},0))="Matches the format Google shows",": use "&LOWER({target}),"")))')
        for h, v in f.items():
            ws[f'{c[h]}{r}'] = v
    idx = lambda h: AB_HEAD.index(h) + 1
    nf = {6: '0', 7: '0', idx('Words'): '0', idx('Characters'): '0', idx('Sentences (approx.)'): '0', idx('Lines or items'): '0',
          idx('Words per item'): '0.0', idx('Length measured'): '0', idx('Answer score (0 to 100)'): '0'}
    for gname in GAPS:
        nf[idx(gname)] = '0.0'
    K.style_body(ws, AB_FIRST, AB_LAST, len(AB_HEAD), formula_cols=AB_F, number_formats=nf, wrap_cols=(1, 4, 5, 11, idx('Target URL'), idx('Top fix')))
    K.dropdown(ws, f'A{AB_FIRST}:A{AB_LAST}', qt('A'), 'Queries from the Snippet Tracker.')
    K.dropdown(ws, f'C{AB_FIRST}:C{AB_LAST}', f'{S}!$N$21:$N$24', 'Paragraph, Ordered list, Unordered list or Table.')
    K.dropdown(ws, f'H{AB_FIRST}:H{AB_LAST}', f'{S}!$Q$6:$Q$8')
    K.dropdown(ws, f'I{AB_FIRST}:I{AB_LAST}', '"Yes,No"')
    K.dropdown(ws, f'J{AB_FIRST}:J{AB_LAST}', f'{S}!$P$21:$P$23')
    for col in 'FG':
        K.whole_number(ws, f'{col}{AB_FIRST}:{col}{AB_LAST}', 0, 500, 'A whole number.')
    sc = c['Answer score (0 to 100)']
    ws.conditional_formatting.add(f'{sc}{AB_FIRST}:{sc}{AB_LAST}', ColorScaleRule(start_type='num', start_value=0, start_color='F8D7D3', mid_type='num', mid_value=60, mid_color='FFF4CC', end_type='num', end_value=100, end_color='8BC34A'))
    lf = c['Length fit']
    ws.conditional_formatting.add(f'{lf}{AB_FIRST}:{lf}{AB_LAST}', CellIsRule(operator='equal', formula=['"In range"'], fill=PatternFill('solid', fgColor='D9F2C4'), font=Font(name=K.FONT, bold=True, color='3D7F12')))
    ws.conditional_formatting.add(f'{lf}{AB_FIRST}:{lf}{AB_LAST}', FormulaRule(formula=[f'LEFT({lf}{AB_FIRST},3)="Too"'], fill=PatternFill('solid', fgColor='FCE5CD'), font=Font(name=K.FONT, bold=True)))
    vc = c['Verdict']
    for txt, fill, fcol in (('Ready to publish', 'B7E4A0', '1F1F1F'), ('Nearly ready', 'FFF4CC', '1F1F1F'), ('Needs work', 'F8D7D3', '9B2C1F')):
        ws.conditional_formatting.add(f'{vc}{AB_FIRST}:{vc}{AB_LAST}', CellIsRule(operator='equal', formula=[f'"{txt}"'], fill=PatternFill('solid', fgColor=fill), font=Font(name=K.FONT, bold=True, color=fcol)))
    for gc in GAPS:
        ws.column_dimensions[c[gc]].hidden = True
    for r in range(AB_FIRST, AB_FIRST + len(ANSWERS)):
        ws.row_dimensions[r].height = 120
    ws.freeze_panes = 'B5'
    ws.auto_filter.ref = f'A4:{c["Top fix"]}{AB_LAST}'
    return ws


def tracker_sheet(wb):
    ws = wb.create_sheet('Snippet Tracker')
    ws.sheet_view.showGridLines = False
    K.title_block(ws, 'Snippet tracker', f'One row per query you want a featured snippet for. Rows 5 to {4 + len(QUERIES)} are DEMO queries for BrewNest, a fictional coffee gear shop (illustrative numbers). 500 rows ready.')
    ws['A2'].font = K.f(10, True, 'B45309')
    ws['A3'] = ('Search each query in a private window. Record whether a featured snippet shows, who holds it, its format and domain, and '
                'whether an AI Overview shows. Position, clicks and impressions come from the Search Console Performance report.')
    ws['A3'].font = K.f(9, False, '666666', True)
    widths = [32, 38, 14, 15, 10, 9, 9, 11, 11, 13, 20, 11, 11, 9, 11, 11, 22, 7, 13, 30, 22, 10, 14, 34, 48, 10, 20, 8, 12, 8]
    K.header_row(ws, 4, QT_HEAD, formula_cols=QT_F, widths=widths)
    c = QC
    for r in range(QT_FIRST, QT_LAST + 1):
        i = r - QT_FIRST
        if i < len(QUERIES):
            q, pi, topic, qtype, srch, value, pos, shows, holder, shown, dom, aio, cited, clk, imp, chk = QUERIES[i]
            url = U + PAGES[pi][0] if pi is not None else None
            for col, v in enumerate([q, url, topic, qtype, srch, value, pos, shows, holder, shown, dom, aio, cited, clk, imp, d(chk)], 1):
                if v not in (None, ''):
                    ws.cell(row=r, column=col, value=v)
        e = f'A{r}=""'
        g = lambda h: f'{c[h]}{r}'
        f = {}
        f['CTR'] = f'=IF(OR({e},N(O{r})=0),"",N(N{r})/O{r})'
        f['Recommended format'] = (f'=IF({e},"",IF(OR(J{r}="Paragraph",J{r}="Ordered list",J{r}="Unordered list",J{r}="Table"),J{r},'
                                   f'IFERROR(VLOOKUP(D{r},{QTYPE_RNG},2,FALSE),"Paragraph")))')
        f['Target length'] = f'=IF({e},"",IFERROR(VLOOKUP({g("Recommended format")},{FMT_RNG},5,FALSE),"")&IF(J{r}="Video",". A video shows: add a short video with chapters too",""))'
        f['Snippet controls'] = f'=IF(OR({e},B{r}=""),"",IFERROR(INDEX({pg("Snippet controls")},MATCH(B{r},{pg("A")},0)),"Add the page to the Page Check"))'
        f['Answer score (0 to 100)'] = f'=IF({e},"",IFERROR(INDEX({ab("Answer score (0 to 100)")},MATCH(A{r},{ab("A")},0)),"No answer yet"))'
        f['Answer verdict'] = f'=IF({e},"",IFERROR(INDEX({ab("Verdict")},MATCH(A{r},{ab("A")},0)),"Draft one on the Answer Builder"))'
        ctl = g('Snippet controls')
        f['Status'] = (f'=IF({e},"",IF(B{r}="","Add a target page",IF(OR(H{r}="",H{r}="Not checked"),"Check the results page",'
                       f'IF(LEFT({ctl},7)="Blocked","Fix snippet controls first",IF(AND(H{r}="Yes",I{r}="You"),"Held: protect it",'
                       f'IF(AND(H{r}="No",OR(L{r}="Yes",L{r}="Sometimes")),"No snippet, AI Overview shows: aim for a citation",IF(H{r}="No","No snippet: classic SEO",'
                       f'IF(OR(G{r}="",G{r}>10),"Not top 10: rank first",IF(G{r}<=5,"Top 5: win it with a better answer block","Ranks 6 to 10: sharpen the answer and climb")))))))))')
        stv = g('Status')
        f['Next action'] = f'=IF({e},"",IFERROR(VLOOKUP({stv},{ST_RNG},2,FALSE),""))'
        asc = g('Answer score (0 to 100)')
        pos = f'IF(G{r}="",0.05,VLOOKUP(G{r},{POS_RNG},2,TRUE))'
        f['Opportunity score (0 to 100)'] = (f'=IF({e},"",ROUND({W_DEM}*MIN(1,N(E{r})/{FULL})+{W_VAL}*IF(F{r}="",2,F{r})/3+{W_POS}*{pos}'
                                             f'+{W_SNIP}*IFERROR(VLOOKUP(IF(H{r}="","Not checked",H{r}),{SNIP_RNG},2,FALSE),0.5)'
                                             f'+{W_GAP}*(1-IF(ISNUMBER({asc}),{asc},0)/100),0))')
        osc = g('Opportunity score (0 to 100)')
        f['Priority'] = (f'=IF({e},"",IF({stv}="Fix snippet controls first","P1: fix controls",IF(LEFT({stv},4)="Held","Protect",'
                         f'IF({stv}="No snippet: classic SEO","Classic SEO",IF(LEFT({stv},10)="No snippet","AI citation",'
                         f'IF(OR({stv}="Check the results page",{stv}="Add a target page"),"Check first",'
                         f'IF({osc}>={P1},"P1: now",IF({osc}>={P2},"P2: this month",IF({osc}>={P3},"P3: this quarter","P4: later")))))))))')
        f['Days since checked'] = f'=IF(OR({e},P{r}=""),"",{DATE}-P{r})'
        ds = g('Days since checked')
        f['Check again?'] = f'=IF({e},"",IF(P{r}="","Yes: never checked",IF({ds}>={RECHECK},"Yes","In "&({RECHECK}-{ds})&" days")))'
        pv = g('Priority')
        f['Rank (helper)'] = (f'=IF(OR({e},{pv}="Protect",{pv}="Classic SEO",{pv}="AI citation",{pv}="Check first"),"",IF({pv}="P1: fix controls",100,0)'
                              f'+{osc}+N(E{r})/10000000-ROW()/100000000)')
        for h, v in f.items():
            ws[f'{c[h]}{r}'] = v
    idx = lambda h: QT_HEAD.index(h) + 1
    nf = {5: '#,##0', 7: '0.0', 14: '#,##0', 15: '#,##0', 16: 'dd mmm yyyy', idx('CTR'): '0.0%', idx('Answer score (0 to 100)'): '0',
          idx('Opportunity score (0 to 100)'): '0', idx('Days since checked'): '0', idx('Rank (helper)'): '0.000000'}
    K.style_body(ws, QT_FIRST, QT_LAST, len(QT_HEAD), formula_cols=QT_F, number_formats=nf,
                 wrap_cols=(1, 2, 17, idx('Target length'), idx('Snippet controls'), idx('Status'), idx('Next action'), idx('Answer verdict')))
    K.dropdown(ws, f'B{QT_FIRST}:B{QT_LAST}', pg('A'), 'URLs from the Page Check tab.')
    K.dropdown(ws, f'D{QT_FIRST}:D{QT_LAST}', f'{S}!$O$6:$O$14')
    K.dropdown(ws, f'F{QT_FIRST}:F{QT_LAST}', '"1,2,3"', '3 close to a sale or lead, 2 builds trust, 1 loosely related.')
    K.dropdown(ws, f'H{QT_FIRST}:H{QT_LAST}', f'{S}!$P$6:$P$8', 'Is there a featured snippet box at the top for this query?')
    K.dropdown(ws, f'I{QT_FIRST}:I{QT_LAST}', f'{S}!$R$6:$R$8', 'You when the snippet links to your page.')
    K.dropdown(ws, f'J{QT_FIRST}:J{QT_LAST}', f'{S}!$N$6:$N$11')
    K.dropdown(ws, f'L{QT_FIRST}:L{QT_LAST}', f'{S}!$S$6:$S$9')
    K.dropdown(ws, f'M{QT_FIRST}:M{QT_LAST}', f'{S}!$P$6:$P$8')
    for col in 'ENO':
        K.whole_number(ws, f'{col}{QT_FIRST}:{col}{QT_LAST}', 0, 1000000000, 'A whole number.')
    pc = c['Priority']
    pr = f'{pc}{QT_FIRST}:{pc}{QT_LAST}'
    for start, fill, fc in (('P1', '9B2C1F', 'FFFFFF'), ('P2', 'F8D7D3', '9B2C1F'), ('P3', 'FFF4CC', '1F1F1F'), ('P4', 'EEEEEE', '555555'),
                            ('Pr', 'B7E4A0', '1F1F1F'), ('Cl', 'EEF8E6', '3D7F12'), ('AI', 'DCEBFF', '1F1F1F'), ('Ch', 'FCE5CD', '1F1F1F')):
        ws.conditional_formatting.add(pr, FormulaRule(formula=[f'LEFT({pc}{QT_FIRST},2)="{start}"'], fill=PatternFill('solid', fgColor=fill), font=Font(name=K.FONT, bold=True, color=fc)))
    sc = c['Status']
    for start, fill, fc in (('Fix', '9B2C1F', 'FFFFFF'), ('Hel', 'B7E4A0', '1F1F1F'), ('Top', 'FFF4CC', '1F1F1F'), ('Ran', 'FFF4CC', '1F1F1F'),
                            ('Not', 'F8D7D3', '9B2C1F'), ('Che', 'FCE5CD', '1F1F1F'), ('Add', 'FCE5CD', '1F1F1F')):
        ws.conditional_formatting.add(f'{sc}{QT_FIRST}:{sc}{QT_LAST}', FormulaRule(formula=[f'LEFT({sc}{QT_FIRST},3)="{start}"'], fill=PatternFill('solid', fgColor=fill), font=Font(name=K.FONT, bold=True, color=fc)))
    ws.conditional_formatting.add(f'I{QT_FIRST}:I{QT_LAST}', CellIsRule(operator='equal', formula=['"You"'], fill=PatternFill('solid', fgColor='D9F2C4'), font=Font(name=K.FONT, bold=True, color='3D7F12')))
    ws.conditional_formatting.add(f'H{QT_FIRST}:H{QT_LAST}', CellIsRule(operator='equal', formula=['"Yes"'], fill=PatternFill('solid', fgColor='DCEBFF')))
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


def action_sheet(wb):
    ws = wb.create_sheet('Action Plan')
    ws.sheet_view.showGridLines = False
    K.title_block(ws, 'Action plan', 'Plan fixes by week. Pick a query and a fix; the page, hours and how to fix fill in. After a fix, record who holds the snippet and the clicks for 28 days before and after.')
    head = ['Query', 'Fix', 'Owner', 'Week', 'Status', 'Done on', 'Snippet holder before', 'Snippet holder after', 'Clicks 28 days before',
            'Clicks 28 days after', 'Target URL', 'Hours (assumption)', 'How to fix', 'Measure on', 'Click change', 'Result']
    fc = tuple(range(11, 17))
    K.header_row(ws, 4, head, formula_cols=fc, widths=[30, 34, 14, 9, 9, 11, 12, 12, 10, 10, 34, 9, 52, 11, 9, 34])
    for r in range(AP_FIRST, AP_LAST + 1):
        i = r - AP_FIRST
        if i < len(ACTIONS):
            qi, fi, own, wk, st, done, hb, ha, cb, ca = ACTIONS[i]
            for col, v in enumerate([QUERIES[qi][0], FIXES[fi][0], own, wk, st, d(done), hb, ha, cb, ca], 1):
                if v not in (None, ''):
                    ws.cell(row=r, column=col, value=v)
        e = f'A{r}=""'
        fx = f'MATCH(B{r},{FIX_RNG_NAME},0)'
        ws[f'K{r}'] = f'=IF({e},"",IFERROR(INDEX({qt("B")},MATCH(A{r},{qt("A")},0))&"","Query not in the tracker"))'
        ws[f'L{r}'] = f'=IF(OR({e},B{r}=""),"",IFERROR(INDEX({S}!$K${FIX_FIRST}:$K${FIX_FIRST + len(FIXES) - 1},{fx}),0))'
        ws[f'M{r}'] = f'=IF(OR({e},B{r}=""),"",IFERROR(INDEX({S}!$L${FIX_FIRST}:$L${FIX_FIRST + len(FIXES) - 1},{fx}),""))'
        ws[f'N{r}'] = f'=IF(OR({e},F{r}=""),"",F{r}+{MEASURE})'
        ws[f'O{r}'] = f'=IF(OR({e},N(I{r})=0,J{r}=""),"",(J{r}-I{r})/I{r})'
        ws[f'P{r}'] = (f'=IF({e},"",IF(E{r}<>"Done","Not done yet",IF(F{r}="","Add the done date",IF({DATE}<N{r},"Wait: "&(N{r}-{DATE})&" days left",'
                       f'IF(H{r}="","Add the holder after",IF(AND(G{r}<>"You",H{r}="You"),"Won the snippet: keep it fresh",IF(AND(G{r}="You",H{r}<>"You"),"Lost the snippet: compare with the new holder",'
                       f'IF(O{r}="","Add clicks after",IF(O{r}>=0.1,"Up "&TEXT(O{r},"0%")&": keep going",IF(O{r}>-0.1,"Flat: give it another cycle","Down: check the results page"))))))))))')
    K.style_body(ws, AP_FIRST, AP_LAST, len(head), formula_cols=fc, number_formats={6: 'dd mmm yyyy', 9: '#,##0', 10: '#,##0', 12: '0.0', 14: 'dd mmm yyyy', 15: '0%'},
                 wrap_cols=(1, 2, 11, 13, 16))
    for r in range(AP_FIRST, AP_FIRST + len(ACTIONS)):
        ws.row_dimensions[r].height = 45
    K.dropdown(ws, f'A{AP_FIRST}:A{AP_LAST}', qt('A'), 'Queries from the Snippet Tracker.')
    K.dropdown(ws, f'B{AP_FIRST}:B{AP_LAST}', FIX_RNG_NAME, 'Fixes from the Settings tab.')
    K.dropdown(ws, f'C{AP_FIRST}:C{AP_LAST}', f'{S}!$T$6:$T$17')
    K.dropdown(ws, f'D{AP_FIRST}:D{AP_LAST}', f'{S}!$U$6:$U$13')
    K.dropdown(ws, f'E{AP_FIRST}:E{AP_LAST}', f'{S}!$O$21:$O$23')
    K.dropdown(ws, f'G{AP_FIRST}:H{AP_LAST}', f'{S}!$V$6:$V$8')
    t = f'P{AP_FIRST}:P{AP_LAST}'
    ws.conditional_formatting.add(t, FormulaRule(formula=[f'OR(LEFT(P{AP_FIRST},2)="Up",LEFT(P{AP_FIRST},3)="Won")'], fill=PatternFill('solid', fgColor='B7E4A0'), font=Font(name=K.FONT, bold=True)))
    ws.conditional_formatting.add(t, FormulaRule(formula=[f'OR(LEFT(P{AP_FIRST},4)="Down",LEFT(P{AP_FIRST},4)="Lost")'], fill=PatternFill('solid', fgColor='F8D7D3'), font=Font(name=K.FONT, bold=True, color='9B2C1F')))
    ws.conditional_formatting.add(t, FormulaRule(formula=[f'OR(LEFT(P{AP_FIRST},4)="Wait",LEFT(P{AP_FIRST},4)="Flat",LEFT(P{AP_FIRST},3)="Add")'], fill=PatternFill('solid', fgColor='FFF4CC')))
    ws['R4'] = 'WEEKLY FIX HOURS'
    ws['R4'].font = K.f(10, True, K.DEEP)
    for j, h in enumerate(['Week', 'Hours planned', 'Capacity', 'Status']):
        cc = ws.cell(row=5, column=18 + j, value=h)
        cc.font, cc.fill = K.f(10, True, 'FFFFFF'), K.HEAD_F
    for i in range(len(WEEKS)):
        r = 6 + i
        ws.cell(row=r, column=18, value=f'={S}!U{6 + i}')
        ws.cell(row=r, column=19, value=f'=SUMIF($D${AP_FIRST}:$D${AP_LAST},R{r},$L${AP_FIRST}:$L${AP_LAST})').number_format = '0.0'
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


def head_cells(ws, row, col, heads):
    for j, h in enumerate(heads):
        cell = ws.cell(row=row, column=col + j, value=h)
        cell.font, cell.fill = K.f(10, True, 'FFFFFF'), K.HEAD_F


def dashboard_sheet(wb):
    ws = wb.create_sheet('Dashboard')
    ws.sheet_view.showGridLines = False
    K.title_block(ws, 'Dashboard', 'Everything here calculates from the other tabs. Only the holder domains (yellow) are typed.')
    for col, w in zip('ABCDEFGHIJ', [50, 13, 3, 34, 34, 8, 12, 14, 12, 3]):
        ws.column_dimensions[col].width = w
    sh, ho, ai = qt('H'), qt('I'), qt('L')
    APE = f'{APS}!$E${AP_FIRST}:$E${AP_LAST}'
    kpis = [
        ('Queries tracked', f'=COUNTIF({qt("A")},"?*")', '0'),
        ('Queries where a featured snippet shows', f'=COUNTIF({sh},"Yes")', '0'),
        ('Snippets you hold', f'=COUNTIFS({sh},"Yes",{ho},"You")', '0'),
        ('Win rate (held / snippets showing)', '=IFERROR(B7/B6,"")', '0%'),
        ('Snippets held by others', '=B6-B7', '0'),
        ('Queries with no featured snippet', f'=COUNTIF({sh},"No")', '0'),
        ('Queries with an AI Overview (Yes or Sometimes)', f'=COUNTIF({ai},"Yes")+COUNTIF({ai},"Sometimes")', '0'),
        ('Snippet and AI Overview on the same page', f'=COUNTIFS({sh},"Yes",{ai},"Yes")+COUNTIFS({sh},"Yes",{ai},"Sometimes")', '0'),
        ('Cited in the AI Overview', f'=COUNTIF({qt("M")},"Yes")', '0'),
        ('P1 queries (including control fixes)', f'=COUNTIF({qt("Priority")},"P1*")', '0'),
        ('Queries to check again', f'=COUNTIF({qt("Check again?")},"Yes*")', '0'),
        ('Answer blocks drafted', f'=COUNTIF({ab("A")},"?*")', '0'),
        ('Answer blocks ready to publish', f'=COUNTIF({ab("Verdict")},"Ready to publish")', '0'),
        ('Average answer score', f'=IFERROR(AVERAGE({ab("Answer score (0 to 100)")}),"")', '0'),
        ('Pages checked', f'=COUNTIF({pg("A")},"?*")', '0'),
        ('Pages blocked by snippet controls', f'=COUNTIF({pg("Snippet controls")},"Blocked*")', '0'),
        ('Fixes open (To do or Doing)', f'=COUNTIF({APE},"To do")+COUNTIF({APE},"Doing")', '0'),
        ('Snippets won after a fix', f'=COUNTIF({APS}!$P${AP_FIRST}:$P${AP_LAST},"Won*")', '0'),
    ]
    ws['A4'] = 'KEY NUMBERS'
    ws['A4'].font = K.f(10, True, K.DEEP)
    for i, (label, fml, fmt) in enumerate(kpis):
        r = 5 + i
        ws.cell(row=r, column=1, value=label).font = K.f(10)
        cell = ws.cell(row=r, column=2, value=fml)
        cell.number_format, cell.font, cell.fill, cell.border = fmt, K.f(11, True), K.FORMULA_FILL, K.BORDER
        cell.alignment = Alignment(horizontal='right')
    ws['D4'] = 'TOP 10 QUERIES TO WORK ON (control fixes first, then opportunity score)'
    ws['D4'].font = K.f(10, True, K.DEEP)
    heads = ['Query', 'Status', 'Score', 'Priority', 'Format', 'Answer']
    cols = ['A', 'Status', 'Opportunity score (0 to 100)', 'Priority', 'Recommended format', 'Answer score (0 to 100)']
    head_cells(ws, 5, 4, heads)
    rk = qt('Rank (helper)')
    for k in range(1, 11):
        r = 5 + k
        mt = f'MATCH(LARGE({rk},{k}),{rk},0)'
        for j, col in enumerate(cols):
            cell = ws.cell(row=r, column=4 + j, value=f'=IFERROR(INDEX({qt(col)},{mt}),"")')
            cell.border, cell.fill, cell.font = K.BORDER, K.FORMULA_FILL, K.f(9, j == 0)
            cell.alignment = Alignment(wrap_text=j in (0, 1, 3, 4), vertical='top')
            cell.number_format = {2: '0', 5: '0'}.get(j, '@')
        ws.row_dimensions[r].height = 30
    top = 27
    ws.cell(row=top - 1, column=1, value='QUERIES BY STATUS').font = K.f(10, True, K.DEEP)
    head_cells(ws, top, 1, ['Status', 'Queries'])
    for i in range(len(STATUSES)):
        r = top + 1 + i
        ws.cell(row=r, column=1, value=f'={S}!J{19 + i}')
        ws.cell(row=r, column=2, value=f'=COUNTIF({qt("Status")},A{r})')
        for cc in (1, 2):
            cell = ws.cell(row=r, column=cc)
            cell.border, cell.fill, cell.font = K.BORDER, K.FORMULA_FILL, K.f(10, cc == 1)
    t2 = top + len(STATUSES) + 4
    ws.cell(row=t2 - 1, column=1, value='FORMAT OF THE SNIPPETS SHOWING').font = K.f(10, True, K.DEEP)
    head_cells(ws, t2, 1, ['Format shown', 'Snippets'])
    for i, fm in enumerate(SHOWN[:5]):
        r = t2 + 1 + i
        ws.cell(row=r, column=1, value=fm).border = K.BORDER
        cell = ws.cell(row=r, column=2, value=f'=COUNTIFS({qt("J")},A{r},{sh},"Yes")')
        cell.border, cell.fill = K.BORDER, K.FORMULA_FILL
    g0 = t2 + 9
    ws.cell(row=g0 - 1, column=1, value='WHO HOLDS THE SNIPPETS (type the domains you see)').font = K.f(10, True, K.DEEP)
    head_cells(ws, g0, 1, ['Holder domain', 'Snippets held'])
    for k in range(12):
        r = g0 + 1 + k
        a = ws.cell(row=r, column=1, value=DOMAINS[k] if k < len(DOMAINS) else None)
        a.border, a.fill = K.BORDER, K.INPUT_FILL
        cell = ws.cell(row=r, column=2, value=f'=IF(A{r}="","",COUNTIFS({qt("K")},A{r},{sh},"Yes"))')
        cell.border, cell.fill = K.BORDER, K.FORMULA_FILL
    chart(ws, 'Queries by status', 'Queries', 1, [2], top + 1, top + len(STATUSES), 'D18', ['E07A5F'], True, h=9, w=18)
    chart(ws, 'Format of the snippets showing', 'Snippets', 1, [2], t2 + 1, t2 + 5, 'D37', [K.GREEN], False, w=18)
    chart(ws, 'Who holds the snippets', 'Snippets', 1, [2], g0 + 1, g0 + len(DOMAINS), 'D53', ['F4B860'], True, h=9, w=18)
    return ws


def build(path, asset, url):
    wb = K.new_book()
    tracker_sheet(wb)
    answer_sheet(wb)
    page_sheet(wb)
    action_sheet(wb)
    dashboard_sheet(wb)
    settings_sheet(wb)
    K.prompts_sheet(wb, asset['prompts'], url)
    K.checklist_sheet(wb, list(asset['checklist']))
    K.sources_sheet(wb, asset['sources'], [
        ('Demo data', 'BrewNest, every URL, domain and query in the demo are fictional (.example domains). Searches, positions, holders, clicks and dates are illustrative, not real data.', ''),
        ('Target lengths, weights, bands, factors and hours', 'Google publishes no snippet lengths. The format lengths on Settings are assumptions of this kit based on public studies (Semrush 2020, Portent 2021). The weights, bands, factors and hours are assumptions too. Tune them on Settings.', ''),
        ('You cannot mark a page as a featured snippet', 'Google says its systems decide whether a page would make a good featured snippet. The kit improves your odds; it cannot guarantee a snippet.', 'https://developers.google.com/search/docs/appearance/featured-snippets'),
        ('Opting out', 'Google says nosnippet blocks all snippets, text marked with data-nosnippet will not appear in featured snippets, and a lower max-snippet makes a featured snippet less likely.', 'https://developers.google.com/search/docs/appearance/featured-snippets'),
        ('Snippets in the AI era', 'An Ahrefs study of 1 million US desktop results pages found featured snippets on 5.53 percent of results pages in June 2025, down from 15.41 percent in January, while AI Overviews grew from 3.93 to 27.43 percent.', 'https://ahrefs.com/blog/how-serp-features-have-evolved-in-the-ai-era/'),
        ('Snippets come from the top 10', 'Ahrefs (2017, 2 million snippets) found 99.58 percent of featured pages already ranked in the top 10, and 30.9 percent ranked first.', 'https://ahrefs.com/blog/featured-snippets-study/'),
    ])
    K.start_here(
        wb, 'Featured Snippet Kit',
        [
            'This workbook shows which of your queries show a featured snippet, who holds it and in what format, and what to fix first. Every query gets a recommended format, a target length, a status, a next action, an opportunity score and a priority.',
            f'The Answer Builder checks the answer block you plan to publish: words, sentences, items, length, heading, key term and format, with a score and the top fix. The Page Check catches snippet controls that block you. A worked demo for a fictional coffee gear shop ({len(QUERIES)} queries, {len(ANSWERS)} answers, {len(PAGES)} pages) shows every formula working.',
        ],
        [
            ('Snippet Tracker', 'One row per query, 500 rows ready. Snippet, holder, format, AI Overview, recommended format and length, controls, answer score, status, next action, score, priority and recheck dates.'),
            ('Answer Builder', 'Paste a draft answer block. Word, sentence and item counts, length fit, 7 checks, an answer score and the top fix. 300 rows ready.'),
            ('Page Check', 'Snippet controls (indexing, nosnippet, max-snippet, data-nosnippet), five page checks, snippets held and the next step per page.'),
            ('Action Plan', 'Fixes by week with hours, how to fix, a weekly hours check and a before and after result: holder and clicks.'),
            ('Dashboard', '18 key numbers, the top 10 queries to work on, queries by status, snippet formats and who holds the snippets, with three charts.'),
            ('Settings', 'Target lengths per format, query type to format, opportunity weights, position bands, answer check weights, statuses, fixes, rules and lists.'),
            ('AI Prompts', 'Prompts for ChatGPT, Claude or Gemini to draft, trim and test answer blocks and compare them with the current snippet.'),
            ('Checklist', 'The featured snippet process as a tick list with automatic progress.'),
            ('Sources', 'Where facts come from and which numbers are assumptions.'),
        ],
        [
            'Look at the demo on every tab. Then clear the yellow demo cells on Snippet Tracker, Answer Builder, Page Check and Action Plan.',
            'On Settings, set today\'s date, the searches that earn full marks and your fix hours per week. Check the target lengths.',
            'Add each target page to the Page Check and answer the controls first: indexed, nosnippet, max-snippet and data-nosnippet.',
            'Add your queries to the Snippet Tracker with position from Search Console. Search each one and record the snippet, holder, format and AI Overview.',
            'For each top query, draft the answer block on the Answer Builder in the recommended format until it is Ready to publish.',
            'Sort the tracker by priority. Add the top fixes to the Action Plan, within your weekly hours.',
            'After each fix, wait 28 days, then record who holds the snippet and the clicks before and after. The Result column reads it.',
        ],
        url,
    )
    order = ['Start Here', 'Snippet Tracker', 'Answer Builder', 'Page Check', 'Action Plan', 'Dashboard', 'Settings', 'AI Prompts', 'Checklist', 'Sources']
    wb._sheets = [wb[n] for n in order]
    wb.active = 0
    for ws in wb.worksheets:
        ws.sheet_properties.tabColor = K.GREEN if ws.title in order[:6] else 'A6EF39'
    wb.save(path)


PREVIEW = {'sheet': 'Snippet Tracker', 'header_row': 4, 'rows': 12,
           'cols': [1, 7, 8, 9, 10, len(QT_IN) + 2, len(QT_IN) + 7, len(QT_IN) + 9, len(QT_IN) + 10],
           'formula_idx': [5, 6, 7, 8]}


def values(wb):
    """Read the recalculated demo values (used by check() and to write the guide)."""
    q, a, p, ap = wb['Snippet Tracker'], wb['Answer Builder'], wb['Page Check'], wb['Action Plan']
    out = {}
    for i in range(len(QUERIES)):
        r = QT_FIRST + i
        out[('q', i)] = {h: q[f'{QC[h]}{r}'].value for h in QT_HEAD}
    for i in range(len(ANSWERS)):
        r = AB_FIRST + i
        out[('a', i)] = {h: a[f'{AC[h]}{r}'].value for h in AB_HEAD}
    for i in range(len(PAGES)):
        r = PG_FIRST + i
        out[('p', i)] = {h: p[f'{PGC[h]}{r}'].value for h in PG_HEAD}
    for i in range(len(ACTIONS)):
        r = AP_FIRST + i
        out[('ap', i)] = {k: ap[f'{k}{r}'].value for k in 'KLMNOP'}
    return out


def check(wb):
    """Assert the worked examples used in the guide."""
    v = values(wb)
    a0 = v[('a', 0)]   # cold brew ordered list
    assert a0['Words'] == 76 and a0['Lines or items'] == 7 and a0['Length fit'] == 'In range', (a0['Words'], a0['Lines or items'], a0['Length fit'])
    assert a0['Answer score (0 to 100)'] == 95 and a0['Verdict'] == 'Ready to publish' and a0['Top fix'] == 'Key term early', (a0['Answer score (0 to 100)'], a0['Top fix'])
    a1 = v[('a', 1)]   # flat white paragraph
    assert a1['Words'] == 66 and a1['Sentences (approx.)'] == 5 and a1['Length fit'] == 'Too long', (a1['Words'], a1['Sentences (approx.)'], a1['Length fit'])
    assert a1['Answer score (0 to 100)'] == 70 and a1['Verdict'] == 'Nearly ready', a1['Answer score (0 to 100)']
    trimmed = FLAT_WHITE_TRIMMED.split()
    assert len(trimmed) == 41 and FLAT_WHITE_TRIMMED in ANSWERS[1][4][0], len(trimmed)
    assert a1['Top fix'] == 'Length fits the format: too long, aim for 40 to 55 words', a1['Top fix']
    a4 = v[('a', 4)]   # pour over table with 7 rows
    assert a4['Length fit'] == 'Too long' and a4['Answer score (0 to 100)'] == 75, (a4['Length fit'], a4['Answer score (0 to 100)'])
    a7 = v[('a', 7)]   # sour espresso list where Google shows a paragraph
    assert a7['Top fix'] == 'Matches the format Google shows: use paragraph', a7['Top fix']
    q0 = v[('q', 0)]
    assert q0['Recommended format'] == 'Ordered list' and q0['Snippet controls'] == 'Allowed' and q0['Answer score (0 to 100)'] == 95
    assert q0['Status'] == 'Top 5: win it with a better answer block' and q0['Opportunity score (0 to 100)'] == 82 and q0['Priority'] == 'P1: now', (q0['Status'], q0['Opportunity score (0 to 100)'])
    assert q0['Days since checked'] == 6 and q0['Check again?'] == 'In 24 days'
    q3 = v[('q', 3)]
    assert q3['Status'] == 'Ranks 6 to 10: sharpen the answer and climb' and q3['Opportunity score (0 to 100)'] == 70 and q3['Priority'] == 'P1: now', (q3['Opportunity score (0 to 100)'],)
    assert v[('q', 8)]['Status'] == 'Fix snippet controls first' and v[('q', 8)]['Priority'] == 'P1: fix controls'
    assert v[('q', 1)]['Status'] == 'Held: protect it' and v[('q', 1)]['Priority'] == 'Protect'
    assert v[('q', 9)]['Snippet controls'] == 'Risk: max-snippet 120 is low' and v[('q', 9)]['Status'] == 'Top 5: win it with a better answer block'
    assert v[('q', 10)]['Status'] == 'No snippet, AI Overview shows: aim for a citation' and v[('q', 11)]['Status'] == 'No snippet: classic SEO'
    assert v[('q', 12)]['Status'] == 'Not top 10: rank first' and v[('q', 14)]['Status'] == 'Add a target page' and v[('q', 15)]['Status'] == 'Check the results page'
    assert v[('p', 7)]['Snippet controls'] == 'Blocked: data-nosnippet on the answer'
    ap = v[('ap', 0)]
    assert ap['P'] == 'Wait: 16 days left', ap['P']
    assert v[('ap', 5)]['P'] == 'Up 13%: keep going' and v[('ap', 6)]['P'] == 'Won the snippet: keep it fresh', (v[('ap', 5)]['P'], v[('ap', 6)]['P'])
    a = wb['Action Plan']
    assert a['S6'].value == 2 and a['S7'].value == 2 and a['S8'].value == 8, (a['S6'].value, a['S7'].value, a['S8'].value)
    dsh = wb['Dashboard']
    k = {dsh.cell(row=r, column=1).value: dsh.cell(row=r, column=2).value for r in range(5, 23)}
    assert k['Queries tracked'] == len(QUERIES) and k['Snippets you hold'] == 2 and k['Queries where a featured snippet shows'] == 12, k
    assert dsh['D6'].value == 'how much caffeine in espresso' and dsh['D7'].value == 'how to make cold brew coffee', (dsh['D6'].value, dsh['D7'].value)
    s = wb['Settings']
    assert s['K13'].value == 100 and s['E30'].value == 100
    return v
