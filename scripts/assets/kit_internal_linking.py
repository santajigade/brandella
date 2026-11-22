"""Internal Linking Kit workbook (asset 10).

Page Inventory: one row per page (500 rows). You add the page facts from a crawler and Search Console
(status, indexable, sitemap, click depth, impressions, clicks, position), a topic cluster and a business
priority. Link Map: one row per internal link (1,000 rows) with source, target, anchor, link type,
whether it is a real <a href> link and the rel value. The Link Map checks every link (target health,
generic or long anchors, crawlable, nofollow, self links, repeats) and the Page Inventory counts links
in and out for each page, runs 13 weighted checks (1 = pass, 0.5 = partly, 0 = fix, blank = not checked),
gives a score, grade, fixes in priority order, a priority and how many content links each page still
needs. Link Planner checks every new link before you add it. Dashboard sums it all up.
"""
import datetime
from openpyxl.styles import PatternFill, Font, Alignment
from openpyxl.formatting.rule import CellIsRule, ColorScaleRule, FormulaRule
from openpyxl.chart import BarChart, Reference
from openpyxl.utils import get_column_letter as L
import kitlib as K

PI_FIRST, PI_LAST = 5, 504      # Page Inventory
LM_FIRST, LM_LAST = 5, 1004     # Link Map
LP_FIRST, LP_LAST = 5, 204      # Link Planner
S = 'Settings'
PI = "'Page Inventory'"
LMS = "'Link Map'"

(DATE, DPASS, DFIX, GEN, MAXW, DOM1, DOM2, MINV, OUTMIN, RFIX) = (f'{S}!$B${r}' for r in range(5, 15))
(SD1, SD2, SDIMP, GA, GB, GC) = (f'{S}!$B${r}' for r in range(16, 22))
CHK_ROW = 25
PT_RNG = f'{S}!$F$6:$H$16'          # page types
PR_RNG = f'{S}!$F$20:$G$22'         # business priority targets
LT_RNG = f'{S}!$F$25:$G$34'         # link types
CL_RNG = f'{S}!$J$6:$K$25'          # clusters and hubs
GEN_RNG = f'{S}!$M$6:$M$30'         # generic anchors

PAGE_TYPES = [('Home', 'No', 'No'), ('Category', 'No', 'Yes'), ('Product', 'No', 'Yes'), ('Pillar or hub', 'Yes', 'Yes'), ('Article', 'Yes', 'Yes'),
              ('Service', 'No', 'Yes'), ('Tool', 'No', 'Yes'), ('Local', 'No', 'Yes'), ('About or contact', 'No', 'No')]
PRIORITIES = [('High', 5), ('Medium', 3), ('Low', 1)]
LINK_TYPES = [('Contextual', 'Yes'), ('Image in content', 'Yes'), ('Related box', 'No'), ('Navigation', 'No'),
              ('Breadcrumb', 'No'), ('Footer', 'No'), ('Sidebar', 'No'), ('Pagination', 'No')]
GENERIC = ['click here', 'read more', 'here', 'this', 'this page', 'this article', 'more', 'learn more', 'website', 'article',
           'link', 'see more', 'find out more', 'check it out', 'go', 'details', 'more info', 'view more', 'continue reading', 'this post']
RELS = ['follow', 'nofollow', 'sponsored', 'ugc']
PSTAT = ['Idea', 'Planned', 'Added', 'Rejected']
PLACE = ['Early in the body', 'In the body', 'List or table', 'Navigation or template']

CHECKS = [
    ('Not an orphan', 10, 'A live page has at least 1 internal link from another page. 0 = fix.',
     'Link to it from its hub and from 2 or 3 related pages. Google says every page you care about should have a link from at least one other page on your site.'),
    ('Enough content links in', 8, 'Content links in (from different pages) reach the target for its business priority (High 5, Medium 3, Low 1, editable) = pass. Half the target = partly. Less = fix.',
     'Add links from related articles, in the body text, with descriptive anchors. Use the Link Planner to check each new link.'),
    ('Shallow click depth', 7, 'Click depth from the home page (from your crawler) of 3 or less = pass, 5 or more = fix, 4 = partly. Blank = not checked.',
     'Link to the page from a hub or category that sits near the home page, or add it to a menu or hub list.'),
    ('Linked from its hub', 6, 'The hub page of its topic cluster (Settings) links to it. Not checked for the hub itself or pages with no cluster.',
     'Add the page to its hub page in a list or in the text, so the cluster is connected from the top.'),
    ('Links back to its hub', 3, 'The page links to its hub page. Missing = partly.', 'Add one natural link from the page to its hub, near the start or in the closing paragraph.'),
    ('Descriptive anchors', 6, 'Share of links in that use a generic anchor (Settings list, for example click here or read more): 0 = pass, up to 25 percent = partly, more = fix.',
     'Rewrite generic anchors so they say what the target page is about. Google says good anchor text is descriptive, reasonably concise and relevant.'),
    ('Anchor variety', 3, 'With 3 or more content links in, the most used content link anchor is at most 60 percent of them = pass, up to 80 percent = partly, more = fix. An assumption of this kit.',
     'Vary the anchors naturally: the topic, a question, a benefit. Do not force the exact keyword into every link.'),
    ('Crawlable links in', 5, 'Every link in is a real <a> element with an href (Link Map column E). Some not crawlable = partly, none crawlable = fix.',
     'Replace JavaScript buttons and onclick links with <a href="/url/"> links. Google can only reliably crawl <a> elements with an href.'),
    ('No broken links out', 7, 'The page links to no target with a 4xx or 5xx status.', 'Update each broken link to the right live page, or remove it.'),
    ('No redirected links out', 4, 'Links to targets that redirect (3xx): 0 = pass, 1 or 2 = partly, 3 or more = fix (editable).',
     'Point the link straight at the final URL. Google says to avoid long redirect chains, which hurt crawling.'),
    ('Followed internal links', 3, 'No link in uses rel nofollow. Any nofollow = partly.',
     'Remove nofollow from internal links. Google says to use nofollow only when you do not trust the source.'),
    ('Enough content links out', 4, 'For page types that need them (articles and hubs, editable): 3 or more content links out = pass, 1 or 2 = partly, 0 = fix.',
     'Link to the hub, to 1 or 2 sibling articles and to the product or service the article supports.'),
    ('In XML sitemap', 3, 'The page is in your XML sitemap = pass. Missing = partly.',
     'Add it to the sitemap. A sitemap helps discovery, but Google says it does not guarantee that pages are crawled or indexed, so links still matter.'),
]
NCH = len(CHECKS)

# Demo: LeafBox, a fictional indoor plant shop in Bengaluru. Every page, link and number is illustrative.
U = 'https://leafbox.example'
CLUSTERS = [('Shop', f'{U}/shop/'), ('Plant care', f'{U}/plant-care/'), ('Low light plants', f'{U}/low-light-plants/'),
            ('Pet safe plants', f'{U}/pet-safe-plants/')]
# url, type, cluster, keyword, priority, status, indexable, sitemap, depth, impressions, clicks, position, notes
P = [
    ('/', 'Home', '', 'leafbox', 'High', 200, 'Yes', 'Yes', 0, 8000, 900, 2.1, ''),
    ('/shop/', 'Category', 'Shop', 'buy indoor plants online', 'High', 200, 'Yes', 'Yes', 1, 22000, 610, 8.4, ''),
    ('/shop/snake-plant/', 'Product', 'Shop', 'snake plant', 'High', 200, 'Yes', 'Yes', 2, 30000, 540, 9.2, ''),
    ('/shop/zz-plant/', 'Product', 'Shop', 'zz plant', 'High', 200, 'Yes', 'Yes', 2, 12000, 300, 7.5, ''),
    ('/shop/money-plant/', 'Product', 'Shop', 'money plant', 'Medium', 200, 'Yes', 'Yes', 2, 9000, 160, 12.3, ''),
    ('/shop/areca-palm/', 'Product', 'Shop', 'areca palm', 'Medium', 200, 'Yes', 'Yes', None, 1500, 20, 18.0, 'Crawler cannot reach it; Google found it in the sitemap'),
    ('/plant-care/', 'Pillar or hub', 'Plant care', 'indoor plant care', 'High', 200, 'Yes', 'Yes', 1, 14000, 350, 6.8, ''),
    ('/plant-care/how-often-to-water-indoor-plants/', 'Article', 'Plant care', 'how often to water indoor plants', 'Medium', 200, 'Yes', 'Yes', 2, 18000, 260, 7.9, ''),
    ('/plant-care/snake-plant-care/', 'Article', 'Plant care', 'snake plant care', 'High', 200, 'Yes', 'Yes', 4, 26000, 390, 6.2, 'Worked example in the guide'),
    ('/plant-care/yellow-leaves-on-plants/', 'Article', 'Plant care', 'yellow leaves on plants', 'Medium', 200, 'Yes', 'Yes', 3, 7000, 120, 11.0, ''),
    ('/plant-care/repotting-guide/', 'Article', 'Plant care', 'how to repot a plant', 'Low', 200, 'Yes', 'Yes', 5, 900, 10, 24.0, ''),
    ('/low-light-plants/', 'Pillar or hub', 'Low light plants', 'low light indoor plants', 'High', 200, 'Yes', 'Yes', 1, 16000, 420, 5.5, ''),
    ('/low-light-plants/best-plants-for-bedroom/', 'Article', 'Low light plants', 'best plants for bedroom', 'Medium', 200, 'Yes', 'Yes', 2, 11000, 330, 4.8, ''),
    ('/low-light-plants/plants-for-office-desk/', 'Article', 'Low light plants', 'plants for office desk', 'Medium', 200, 'Yes', 'Yes', 3, 5000, 90, 9.6, ''),
    ('/pet-safe-plants/', 'Pillar or hub', 'Pet safe plants', 'pet safe plants', 'High', 200, 'Yes', 'Yes', 1, 6000, 150, 7.0, ''),
    ('/pet-safe-plants/plants-safe-for-cats/', 'Article', 'Pet safe plants', 'plants safe for cats', 'High', 200, 'Yes', 'No', None, 4000, 60, 13.0, 'Published without links or a sitemap entry'),
    ('/zz-plant/', 'Product', 'Shop', 'zz plant', 'Low', 301, 'No', 'No', 2, None, None, None, 'Old URL, redirects to /shop/zz-plant/'),
    ('/blog/fertiliser-guide/', 'Article', 'Plant care', 'fertiliser for indoor plants', 'Low', 404, 'No', 'No', 2, None, None, None, 'Deleted in 2025'),
    ('/about/', 'About or contact', '', 'leafbox about', 'Low', 200, 'Yes', 'Yes', 1, 500, 30, 3.0, ''),
    ('/contact/', 'About or contact', '', 'leafbox contact', 'Low', 200, 'Yes', 'Yes', 1, 300, 20, 2.5, ''),
]
# source, target, anchor, type, a href, rel, notes
C, N, B, F = 'Contextual', 'Navigation', 'Breadcrumb', 'Footer'
LINKS = [
    ('/', '/shop/', 'Shop plants', N, 'Yes', 'follow', 'Menu (logged once, from the home page)'),
    ('/', '/plant-care/', 'Plant care', N, 'Yes', 'follow', 'Menu'),
    ('/', '/low-light-plants/', 'Low light plants', N, 'Yes', 'follow', 'Menu'),
    ('/', '/pet-safe-plants/', 'Pet safe plants', N, 'Yes', 'follow', 'Menu'),
    ('/', '/about/', 'About us', F, 'Yes', 'follow', ''),
    ('/', '/contact/', 'Contact', F, 'Yes', 'follow', ''),
    ('/', '/shop/snake-plant/', 'Snake plant', C, 'Yes', 'follow', 'Best sellers'),
    ('/', '/shop/zz-plant/', 'ZZ plant', C, 'Yes', 'follow', 'Best sellers'),
    ('/shop/', '/shop/snake-plant/', 'Snake plant', C, 'Yes', 'follow', ''),
    ('/shop/', '/shop/zz-plant/', 'ZZ plant', C, 'Yes', 'follow', ''),
    ('/shop/', '/shop/money-plant/', 'Money plant', C, 'Yes', 'follow', ''),
    ('/shop/', '/', 'Home', B, 'Yes', 'follow', ''),
    ('/shop/snake-plant/', '/shop/', 'Shop', B, 'Yes', 'follow', ''),
    ('/shop/snake-plant/', '/plant-care/snake-plant-care/', 'Read more', C, 'Yes', 'follow', ''),
    ('/shop/snake-plant/', '/zz-plant/', 'ZZ plant', C, 'Yes', 'follow', 'Old URL'),
    ('/shop/zz-plant/', '/shop/', 'Shop', B, 'Yes', 'follow', ''),
    ('/shop/zz-plant/', '/low-light-plants/', 'more low light plants', C, 'Yes', 'follow', ''),
    ('/shop/money-plant/', '/shop/', 'Shop', B, 'Yes', 'follow', ''),
    ('/shop/money-plant/', '/shop/money-plant/', 'Money plant', B, 'Yes', 'follow', 'Last breadcrumb item is a link'),
    ('/plant-care/', '/plant-care/how-often-to-water-indoor-plants/', 'how often to water indoor plants', C, 'Yes', 'follow', ''),
    ('/plant-care/', '/plant-care/yellow-leaves-on-plants/', 'why plant leaves turn yellow', C, 'Yes', 'follow', ''),
    ('/plant-care/', '/plant-care/repotting-guide/', 'repotting guide', C, 'Yes', 'follow', ''),
    ('/plant-care/', '/', 'Home', B, 'Yes', 'follow', ''),
    ('/plant-care/how-often-to-water-indoor-plants/', '/plant-care/', 'indoor plant care guide', C, 'Yes', 'follow', ''),
    ('/plant-care/how-often-to-water-indoor-plants/', '/plant-care/snake-plant-care/', 'click here', C, 'Yes', 'follow', ''),
    ('/plant-care/how-often-to-water-indoor-plants/', '/plant-care/yellow-leaves-on-plants/', 'yellow leaves caused by overwatering', C, 'Yes', 'follow', ''),
    ('/plant-care/how-often-to-water-indoor-plants/', '/shop/snake-plant/', 'snake plant', C, 'Yes', 'follow', ''),
    ('/plant-care/snake-plant-care/', '/plant-care/', 'indoor plant care', C, 'Yes', 'follow', ''),
    ('/plant-care/snake-plant-care/', '/zz-plant/', 'ZZ plant', C, 'Yes', 'follow', 'Old URL'),
    ('/plant-care/snake-plant-care/', '/shop/snake-plant/', 'buy a snake plant', C, 'Yes', 'follow', ''),
    ('/plant-care/snake-plant-care/', '/plant-care/how-often-to-water-indoor-plants/', 'how often to water', C, 'Yes', 'follow', ''),
    ('/plant-care/yellow-leaves-on-plants/', '/blog/fertiliser-guide/', 'fertiliser guide', C, 'Yes', 'follow', 'Deleted page'),
    ('/plant-care/yellow-leaves-on-plants/', '/plant-care/', 'plant care', C, 'Yes', 'follow', ''),
    ('/plant-care/yellow-leaves-on-plants/', '/plant-care/how-often-to-water-indoor-plants/', 'watering schedule', C, 'Yes', 'follow', ''),
    ('/plant-care/repotting-guide/', '/plant-care/', 'plant care hub', C, 'Yes', 'follow', ''),
    ('/low-light-plants/', '/low-light-plants/best-plants-for-bedroom/', 'best plants for the bedroom', C, 'Yes', 'follow', ''),
    ('/low-light-plants/', '/low-light-plants/plants-for-office-desk/', 'plants for an office desk', C, 'Yes', 'nofollow', 'Old plugin setting'),
    ('/low-light-plants/', '/shop/zz-plant/', 'ZZ plant', C, 'Yes', 'follow', ''),
    ('/low-light-plants/', '/shop/snake-plant/', 'snake plant', C, 'Yes', 'follow', ''),
    ('/low-light-plants/best-plants-for-bedroom/', '/low-light-plants/', 'low light indoor plants', C, 'Yes', 'follow', ''),
    ('/low-light-plants/best-plants-for-bedroom/', '/shop/snake-plant/', 'snake plant', C, 'Yes', 'follow', ''),
    ('/low-light-plants/best-plants-for-bedroom/', '/low-light-plants/plants-for-office-desk/', 'desk plants', C, 'No', 'follow', 'JavaScript button, no href'),
    ('/low-light-plants/plants-for-office-desk/', '/low-light-plants/', 'low light plants', C, 'Yes', 'follow', ''),
    ('/low-light-plants/plants-for-office-desk/', '/shop/zz-plant/', 'ZZ plant', C, 'Yes', 'follow', ''),
    ('/pet-safe-plants/', '/', 'Home', B, 'Yes', 'follow', ''),
    ('/pet-safe-plants/', '/low-light-plants/', 'low light plants', C, 'Yes', 'follow', ''),
    ('/about/', '/contact/', 'contact our plant team', C, 'Yes', 'follow', ''),
    ('/about/', '/blog/fertiliser-guide/', 'our fertiliser guide', C, 'Yes', 'follow', 'Deleted page'),
    ('/contact/', '/', 'Home', B, 'Yes', 'follow', ''),
    ('/shop/areca-palm/', '/shop/', 'Shop', B, 'Yes', 'follow', ''),
    ('/pet-safe-plants/plants-safe-for-cats/', '/pet-safe-plants/', 'pet safe plants', C, 'Yes', 'follow', ''),
    ('/plant-care/how-often-to-water-indoor-plants/', '/shop/snake-plant/', 'snake plant', C, 'Yes', 'follow', 'Second link to the same page'),
]
# source, target, anchor, placement, status, date added, notes
PLAN = [
    ('/plant-care/', '/plant-care/snake-plant-care/', 'snake plant care', 'List or table', 'Planned', None, 'Hub list: fixes Linked from its hub'),
    ('/low-light-plants/best-plants-for-bedroom/', '/plant-care/snake-plant-care/', 'how to care for a snake plant', 'In the body', 'Planned', None, ''),
    ('/pet-safe-plants/', '/pet-safe-plants/plants-safe-for-cats/', 'plants safe for cats', 'Early in the body', 'Planned', None, 'Fixes an orphan'),
    ('/plant-care/how-often-to-water-indoor-plants/', '/shop/snake-plant/', 'snake plant', 'In the body', 'Idea', None, ''),
    ('/shop/zz-plant/', '/zz-plant/', 'zz plant care', 'In the body', 'Idea', None, ''),
    ('/plant-care/yellow-leaves-on-plants/', '/plant-care/snake-plant-care/', 'click here', 'In the body', 'Idea', None, ''),
    ('/shop/', '/shop/areca-palm/', 'Areca palm', 'List or table', 'Added', '2026-11-18', 'Fixes an orphan'),
    ('/low-light-plants/', '/plant-care/repotting-guide/', 'how to repot a plant', 'In the body', 'Planned', None, 'Cuts click depth from 5 to 2'),
]

IN_HEAD = ['URL', 'Page type', 'Topic cluster', 'Focus keyword', 'Business priority', 'Status code', 'Indexable?', 'In XML sitemap?',
           'Click depth', 'Impressions (28 days)', 'Clicks (28 days)', 'Avg position', 'Notes']
MEAS_HEAD = ['Live page?', 'Hub URL', 'Is the hub?', 'Pages linking in', 'Content links in (pages)', 'Links in from same cluster',
             'Linked from hub?', 'Links to hub?', 'Not crawlable links in', 'Nofollow links in', 'Links in (all)', 'Generic anchors in',
             'Generic anchor share', 'Top anchor share', 'Pages linked out', 'Content links out (pages)', 'Broken links out',
             'Redirected links out', 'Content links in target', 'Content links to add']
OUT_HEAD = ['Score (0 to 100)', 'Grade', 'Fixes needed', 'Fixes in priority order', 'Priority', 'Opportunity (helper)']
NIN, NME = len(IN_HEAD), len(MEAS_HEAD)
C0 = NIN + NME + 1
CK = [L(C0 + i) for i in range(NCH)]
SC = C0 + NCH
HEAD = IN_HEAD + MEAS_HEAD + [c[0] for c in CHECKS] + OUT_HEAD
F_COLS = tuple(range(NIN + 1, len(HEAD) + 1))
M = {h: L(i + 1) for i, h in enumerate(HEAD)}

LM_IN = ['Source URL (page with the link)', 'Target URL (page linked to)', 'Anchor text (or image alt)', 'Link type', 'Real <a href> link?', 'rel', 'Notes']
LM_F = ['Source cluster', 'Target cluster', 'Same cluster?', 'Target status', 'Target health', 'Self link?', 'Counts as a content link?',
        'Anchor words', 'Generic anchor?', 'Anchor names the target topic?', 'Same anchor to this target (content links)', 'First link source to target (helper)',
        'First content link (helper)', 'Issues']
LMH = LM_IN + LM_F
LMC = {h: L(i + 1) for i, h in enumerate(LMH)}


def pi(c):
    return f'{PI}!${c}${PI_FIRST}:${c}${PI_LAST}'


def lm(c):
    return f'{LMS}!${c}${LM_FIRST}:${c}${LM_LAST}'


def d(s):
    return datetime.date.fromisoformat(s) if s else None


def settings_sheet(wb):
    ws = wb.create_sheet(S)
    ws.sheet_view.showGridLines = False
    K.title_block(ws, 'Settings', 'Every threshold, weight and list used by this workbook. Change a blue value and every score updates.')
    for c, w in zip('ABCDEFGHIJKLMNOPQRS', [52, 14, 62, 58, 3, 20, 16, 16, 3, 18, 44, 3, 20, 3, 8, 11, 10, 20, 3]):
        ws.column_dimensions[c].width = w
    rows = [
        (4, 'LINK RULES', None, None),
        (5, 'Analysis date (set it to the day you crawl)', datetime.date(2026, 11, 22), 'dd mmm yyyy'),
        (6, 'Click depth passes at or below', 3, '0'),
        (7, 'Click depth fails at or above', 5, '0'),
        (8, 'Generic anchors: partly up to this share of links in', 0.25, '0%'),
        (9, 'An anchor is too long above this many words', 10, '0'),
        (10, 'Anchor variety: the top anchor may be up to this share', 0.6, '0%'),
        (11, 'Anchor variety: partly up to this share', 0.8, '0%'),
        (12, 'Anchor variety is checked from this many links in', 3, '0'),
        (13, 'Content links out needed (articles and hubs)', 3, '0'),
        (14, 'Redirected links out fail at or above', 3, '0'),
        (15, 'OPPORTUNITY AND GRADES', None, None),
        (16, 'Close to the top: average position from', 4, '0'),
        (17, 'Close to the top: average position up to', 20, '0'),
        (18, 'Close to the top: at least this many impressions (28 days)', 500, '#,##0'),
        (19, 'Grade A when the score is at least', 85, '0'),
        (20, 'Grade B when at least', 70, '0'),
        (21, 'Grade C when at least (below = D)', 55, '0'),
    ]
    for r, label, val, fmt in rows:
        a = ws.cell(row=r, column=1, value=label)
        a.font = K.f(10, val is None, K.DEEP if val is None else K.INK)
        if val is not None:
            c = ws.cell(row=r, column=2, value=val)
            c.border, c.fill = K.BORDER, K.INPUT_FILL
            c.font = K.f(10, True, '0000FF')
            c.number_format = fmt
    ws['C5'] = ('Google says every page you care about should have a link from at least one other page, that there is no magical ideal number of links '
                'on a page, and that good anchor text is descriptive, reasonably concise and relevant. Every number on this tab (the 3 click depth, the '
                'content link targets by priority, the 25 percent generic share, the 10 word anchor, the 60 and 80 percent anchor variety, 3 content links '
                'out and the grade bands) is an assumption of this kit for you to tune.')
    ws['C5'].font = K.f(9, False, '777777', True)
    ws['C5'].alignment = Alignment(wrap_text=True, vertical='top')
    ws.merge_cells('C5:D12')
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
        ws.row_dimensions[r].height = 44
    tr = CHK_ROW + NCH
    ws.cell(row=tr, column=1, value='Total weight (auto)').font = K.f(10, True)
    ws.cell(row=tr, column=2, value=f'=SUM(B{CHK_ROW}:B{tr - 1})').fill = K.FORMULA_FILL

    def table(col, row, title, heads, vals, n):
        ws.cell(row=row - 1, column=col, value=title).font = K.f(10, True, K.DEEP)
        for j, h in enumerate(heads):
            ws.cell(row=row, column=col + j, value=h).font = K.f(9, True, '555555')
        for i in range(n):
            for j in range(len(heads)):
                v = vals[i][j] if i < len(vals) else None
                c = ws.cell(row=row + 1 + i, column=col + j, value=v)
                c.fill, c.border, c.font = K.INPUT_FILL, K.BORDER, K.f(10)
    table(6, 5, 'PAGE TYPES', ['Page type', 'Needs content links out?', 'Checks content links in?'], PAGE_TYPES, 11)
    table(6, 19, 'BUSINESS PRIORITY', ['Priority', 'Content links in target'], PRIORITIES, 3)
    ws['F23'] = 'Targets are assumptions: important pages deserve more links from related pages.'
    ws['F23'].font = K.f(8, False, '777777', True)
    table(6, 24, 'LINK TYPES', ['Link type', 'Counts as a content link?'], LINK_TYPES, 10)
    table(10, 5, 'TOPIC CLUSTERS AND HUB PAGES', ['Topic cluster', 'Hub URL'], CLUSTERS, 20)
    ws['M4'] = 'GENERIC ANCHORS'
    ws['M4'].font = K.f(10, True, K.DEEP)
    ws['M5'] = 'Anchor (any case)'
    ws['M5'].font = K.f(9, True, '555555')
    for i in range(25):
        c = ws.cell(row=6 + i, column=13, value=GENERIC[i] if i < len(GENERIC) else None)
        c.fill, c.border, c.font = K.INPUT_FILL, K.BORDER, K.f(10)
    ws['O4'] = 'LISTS'
    ws['O4'].font = K.f(10, True, K.DEEP)
    for col, vals in (('O', ['Yes/No', 'Yes', 'No']), ('P', ['rel'] + RELS), ('Q', ['Planner status'] + PSTAT), ('R', ['Placement'] + PLACE)):
        for i, v in enumerate(vals):
            c = ws[f'{col}{5 + i}']
            c.value = v
            c.font = K.f(9, i == 0, '555555')
    return ws


def inventory_sheet(wb):
    ws = wb.create_sheet('Page Inventory')
    ws.sheet_view.showGridLines = False
    K.title_block(ws, 'Page inventory', f'Rows 5 to {4 + len(P)} hold DEMO data for LeafBox, a fictional plant shop (illustrative pages and numbers). Select the yellow demo cells and press Delete to start your own. Grey formula columns stay.')
    ws['A2'].font = K.f(10, True, 'B45309')
    ws['A3'] = 'One row per page. Add status, indexable, sitemap and click depth from your crawler, and Search Console numbers for 28 days. Every link count comes from the Link Map tab. 500 rows ready.'
    ws['A3'].font = K.f(9, False, '666666', True)
    widths = ([44, 14, 16, 28, 10, 8, 9, 9, 8, 11, 9, 8, 30] + [7, 30, 7, 8, 9, 9, 9, 8, 9, 9, 8, 8, 9, 9, 8, 9, 8, 9, 9, 9] +
              [9] * NCH + [9, 7, 7, 56, 34, 8])
    K.header_row(ws, 4, HEAD, formula_cols=F_COLS, widths=widths)
    for i, col in enumerate(CK):
        c = ws[f'{col}3']
        c.value = f'={S}!$B${CHK_ROW + i}'
        c.font, c.fill, c.alignment = K.f(9, True, K.DEEP), K.SOFT, Alignment(horizontal='center')
    ws[f'{CK[0]}2'] = 'Check weights (from Settings)'
    ws[f'{CK[0]}2'].font = K.f(9, True, K.DEEP)
    m = M
    LA, LB, LCc, LE, LF = lm('A'), lm('B'), lm('C'), lm('E'), lm('F')
    lc = lambda h: lm(LMC[h])
    for r in range(PI_FIRST, PI_LAST + 1):
        i = r - PI_FIRST
        if i < len(P):
            row = list(P[i])
            row[0] = U + row[0]
            for col, v in enumerate(row, 1):
                if v not in (None, ''):
                    ws.cell(row=r, column=col, value=v)
        e = f'A{r}=""'
        g = lambda h: f'{m[h]}{r}'
        A = f'A{r}'
        f = {}
        f['Live page?'] = f'=IF({e},"",IF(AND(N(F{r})=200,G{r}<>"No"),"Yes","No"))'
        f['Hub URL'] = f'=IF(OR({e},C{r}=""),"",IFERROR(VLOOKUP(C{r},{CL_RNG},2,FALSE),""))'
        hub = g('Hub URL')
        f['Is the hub?'] = f'=IF(OR({e},{hub}=""),"",IF({hub}={A},"Yes","No"))'
        nself = f'{lc("Self link?")},"No"'
        f['Pages linking in'] = f'=IF({e},"",COUNTIFS({LB},{A},{lc("First link source to target (helper)")},1,{nself}))'
        f['Content links in (pages)'] = f'=IF({e},"",COUNTIFS({LB},{A},{lc("First content link (helper)")},1,{nself}))'
        f['Links in from same cluster'] = f'=IF({e},"",COUNTIFS({LB},{A},{lc("First link source to target (helper)")},1,{nself},{lc("Same cluster?")},"Yes"))'
        ish = g('Is the hub?')
        f['Linked from hub?'] = f'=IF(OR({e},{hub}="",{ish}="Yes"),"",IF(COUNTIFS({LA},{hub},{LB},{A})>0,"Yes","No"))'
        f['Links to hub?'] = f'=IF(OR({e},{hub}="",{ish}="Yes"),"",IF(COUNTIFS({LA},{A},{LB},{hub})>0,"Yes","No"))'
        f['Not crawlable links in'] = f'=IF({e},"",COUNTIFS({LB},{A},{LE},"No",{nself}))'
        f['Nofollow links in'] = f'=IF({e},"",COUNTIFS({LB},{A},{LF},"nofollow",{nself}))'
        f['Links in (all)'] = f'=IF({e},"",COUNTIFS({LB},{A},{nself}))'
        f['Generic anchors in'] = f'=IF({e},"",COUNTIFS({LB},{A},{lc("Generic anchor?")},"Yes",{nself}))'
        lin = g('Links in (all)')
        f['Generic anchor share'] = f'=IF(OR({e},N({lin})=0),"",{g("Generic anchors in")}/{lin})'
        ctl = f'COUNTIFS({LB},{A},{nself},{lc("Counts as a content link?")},"Yes")'
        f['Top anchor share'] = f'=IF(OR({e},{ctl}=0),"",_xlfn.MAXIFS({lc("Same anchor to this target (content links)")},{LB},{A},{nself},{lc("Counts as a content link?")},"Yes")/{ctl})'
        f['Pages linked out'] = f'=IF({e},"",COUNTIFS({LA},{A},{lc("First link source to target (helper)")},1,{nself}))'
        f['Content links out (pages)'] = f'=IF({e},"",COUNTIFS({LA},{A},{lc("First content link (helper)")},1,{nself}))'
        f['Broken links out'] = f'=IF({e},"",COUNTIFS({LA},{A},{lc("Target health")},"Broken"))'
        f['Redirected links out'] = f'=IF({e},"",COUNTIFS({LA},{A},{lc("Target health")},"Redirect"))'
        f['Content links in target'] = f'=IF({e},"",IF(IFERROR(VLOOKUP(B{r},{PT_RNG},3,FALSE),"Yes")="No",0,IFERROR(VLOOKUP(E{r},{PR_RNG},2,FALSE),0)))'
        live = g('Live page?')
        cin, tgt = g('Content links in (pages)'), g('Content links in target')
        f['Content links to add'] = f'=IF(OR({e},{live}<>"Yes"),"",MAX(0,{tgt}-{cin}))'
        ok = f'OR({e},{live}<>"Yes")'
        t = {}
        t['Not an orphan'] = f'=IF({ok},"",IF({g("Pages linking in")}>=1,1,0))'
        t['Enough content links in'] = f'=IF(OR({ok},N({tgt})=0),"",IF({cin}>={tgt},1,IF({cin}>={tgt}/2,0.5,0)))'
        t['Shallow click depth'] = f'=IF(OR({ok},I{r}=""),"",IF(I{r}<={DPASS},1,IF(I{r}>={DFIX},0,0.5)))'
        t['Linked from its hub'] = f'=IF(OR({ok},{g("Linked from hub?")}=""),"",IF({g("Linked from hub?")}="Yes",1,0))'
        t['Links back to its hub'] = f'=IF(OR({ok},{g("Links to hub?")}=""),"",IF({g("Links to hub?")}="Yes",1,0.5))'
        gs = g('Generic anchor share')
        t['Descriptive anchors'] = f'=IF(OR({ok},{gs}=""),"",IF({gs}=0,1,IF({gs}<={GEN},0.5,0)))'
        ts = g('Top anchor share')
        t['Anchor variety'] = f'=IF(OR({ok},{ts}="",{ctl}<{MINV}),"",IF({ts}<={DOM1},1,IF({ts}<={DOM2},0.5,0)))'
        nc = g('Not crawlable links in')
        t['Crawlable links in'] = f'=IF(OR({ok},N({lin})=0),"",IF({nc}=0,1,IF({nc}<{lin},0.5,0)))'
        t['No broken links out'] = f'=IF({ok},"",IF({g("Broken links out")}=0,1,0))'
        ro = g('Redirected links out')
        t['No redirected links out'] = f'=IF({ok},"",IF({ro}=0,1,IF({ro}<{RFIX},0.5,0)))'
        t['Followed internal links'] = f'=IF(OR({ok},N({lin})=0),"",IF({g("Nofollow links in")}=0,1,0.5))'
        need = f'IFERROR(VLOOKUP(B{r},{PT_RNG},2,FALSE),"No")'
        co = g('Content links out (pages)')
        t['Enough content links out'] = f'=IF(OR({ok},{need}<>"Yes"),"",IF({co}>={OUTMIN},1,IF({co}>=1,0.5,0)))'
        t['In XML sitemap'] = f'=IF(OR({ok},H{r}=""),"",IF(H{r}="Yes",1,0.5))'
        for h, v in list(f.items()) + list(t.items()):
            ws[f'{m[h]}{r}'] = v
        rng = f'{CK[0]}{r}:{CK[-1]}{r}'
        w = f'${CK[0]}$3:${CK[-1]}$3'
        sc = m['Score (0 to 100)']
        ws[f'{sc}{r}'] = f'=IF({ok},"",IFERROR(ROUND(100*SUMPRODUCT({w},{rng})/SUMPRODUCT({w}*ISNUMBER({rng})),0),""))'
        ws[g('Grade')] = f'=IF(OR({e},{sc}{r}=""),"",IF({sc}{r}>={GA},"A",IF({sc}{r}>={GB},"B",IF({sc}{r}>={GC},"C","D"))))'
        ws[g('Fixes needed')] = f'=IF({ok},"",COUNTIF({rng},0)+COUNTIF({rng},0.5))'
        parts = ','.join(f'IF({c}{r}=0,{c}$4,IF({c}{r}=0.5,{c}$4&" (partly)",""))' for c in CK)
        ws[g('Fixes in priority order')] = f'=IF({ok},"",_xlfn.TEXTJOIN("; ",TRUE,{parts}))'
        orph = f'{m["Not an orphan"]}{r}'
        deep = f'{m["Shallow click depth"]}{r}'
        add = g('Content links to add')
        ws[g('Priority')] = (
            f'=IF({e},"",IF({live}<>"Yes",IF(N({g("Pages linking in")})>0,"Fix links: page not live, repoint links","Not live: no action"),'
            f'IF({orph}=0,"Fix now: orphan page",IF({g("Broken links out")}>0,"Fix now: broken links on this page",'
            f'IF(AND(N(L{r})>={SD1},N(L{r})<={SD2},N(J{r})>={SDIMP},N({add})>0),"Boost: add links, close to the top",'
            f'IF(AND(ISNUMBER({deep}),{deep}=0),"Restructure: page is too deep",IF({sc}{r}>={GA},"Healthy: monitor","Improve when you can")))))))')
        ws[g('Opportunity (helper)')] = f'=IF(OR({e},N({add})=0),"",N(J{r})+1+ROW()/100000)'
    nf = {10: '#,##0', 11: '#,##0', 12: '0.0', NIN + 13: '0%', NIN + 14: '0%', SC: '0', SC + 5: '0.00000'}
    K.style_body(ws, PI_FIRST, PI_LAST, len(HEAD), formula_cols=F_COLS, number_formats=nf, wrap_cols=(13, SC + 3))
    ws.freeze_panes = 'B5'
    ws.auto_filter.ref = f'A4:{L(len(HEAD))}{PI_LAST}'
    K.dropdown(ws, f'B{PI_FIRST}:B{PI_LAST}', f'{S}!$F$6:$F$16')
    K.dropdown(ws, f'C{PI_FIRST}:C{PI_LAST}', f'{S}!$J$6:$J$25', 'Clusters and their hub pages live on Settings.')
    K.dropdown(ws, f'E{PI_FIRST}:E{PI_LAST}', f'{S}!$F$20:$F$22')
    K.whole_number(ws, f'F{PI_FIRST}:F{PI_LAST}', 100, 599, 'HTTP status code, for example 200, 301 or 404.')
    for col in 'GH':
        K.dropdown(ws, f'{col}{PI_FIRST}:{col}{PI_LAST}', f'{S}!$O$6:$O$7')
    K.whole_number(ws, f'I{PI_FIRST}:I{PI_LAST}', 0, 50, 'Click depth from the home page (0 = home). Leave blank if the crawler cannot reach the page.')
    chk = f'{CK[0]}{PI_FIRST}:{CK[-1]}{PI_LAST}'
    ws.conditional_formatting.add(chk, CellIsRule(operator='equal', formula=['1'], fill=PatternFill('solid', fgColor='D9F2C4')))
    ws.conditional_formatting.add(chk, CellIsRule(operator='equal', formula=['0.5'], fill=PatternFill('solid', fgColor='FFF4CC')))
    ws.conditional_formatting.add(chk, FormulaRule(formula=[f'AND(ISNUMBER({CK[0]}{PI_FIRST}),{CK[0]}{PI_FIRST}=0)'], fill=PatternFill('solid', fgColor='F8D7D3'), font=Font(name=K.FONT, bold=True, color='9B2C1F')))
    scol = L(SC)
    ws.conditional_formatting.add(f'{scol}{PI_FIRST}:{scol}{PI_LAST}', ColorScaleRule(start_type='num', start_value=30, start_color='F8D7D3', mid_type='num', mid_value=70, mid_color='FFF4CC', end_type='num', end_value=100, end_color='B7E4A0'))
    gcol = f'{L(SC + 1)}{PI_FIRST}:{L(SC + 1)}{PI_LAST}'
    for val, col in (('A', '9BE07A'), ('B', 'D9F2C4'), ('C', 'FFF4CC'), ('D', 'F8D7D3')):
        ws.conditional_formatting.add(gcol, CellIsRule(operator='equal', formula=[f'"{val}"'], fill=PatternFill('solid', fgColor=col), font=Font(name=K.FONT, bold=True)))
    pc = L(SC + 4)
    pr = f'{pc}{PI_FIRST}:{pc}{PI_LAST}'
    for start, n, fill, fc in (('Fix now', 7, '9B2C1F', 'FFFFFF'), ('Fix links', 9, 'F8D7D3', '9B2C1F'), ('Boost', 5, 'FCE4D6', '9B2C1F'), ('Restructure', 11, 'FFF4CC', '1F1F1F'), ('Healthy', 7, 'D9F2C4', '1F1F1F')):
        ws.conditional_formatting.add(pr, FormulaRule(formula=[f'LEFT({pc}{PI_FIRST},{n})="{start}"'], fill=PatternFill('solid', fgColor=fill), font=Font(name=K.FONT, bold=True, color=fc)))
    ad = m['Content links to add']
    ws.conditional_formatting.add(f'{ad}{PI_FIRST}:{ad}{PI_LAST}', CellIsRule(operator='greaterThan', formula=['0'], font=Font(name=K.FONT, bold=True, color='B45309')))
    ws.column_dimensions[L(SC + 5)].hidden = True
    return ws


def linkmap_sheet(wb):
    ws = wb.create_sheet('Link Map')
    ws.sheet_view.showGridLines = False
    K.title_block(ws, 'Link map', f'One row per internal link. Rows 5 to {4 + len(LINKS)} are DEMO links for LeafBox. Paste the internal links export from your crawler (source, target, anchor) and choose the link type. 1,000 rows ready.')
    ws['A2'].font = K.f(10, True, 'B45309')
    ws['A3'] = 'Tip: menu, footer and sidebar links repeat on every page. Log them once, from the home page, or paste the full export; repeats of the same source and target are counted once.'
    ws['A3'].font = K.f(9, False, '666666', True)
    nin = len(LM_IN)
    fc = tuple(range(nin + 1, len(LMH) + 1))
    K.header_row(ws, 4, LMH, formula_cols=fc, widths=[40, 40, 30, 14, 9, 9, 26, 14, 14, 8, 8, 12, 7, 9, 7, 9, 9, 9, 9, 9, 44])
    c = LMC
    for r in range(LM_FIRST, LM_LAST + 1):
        i = r - LM_FIRST
        if i < len(LINKS):
            row = list(LINKS[i])
            row[0], row[1] = U + row[0], U + row[1]
            for col, v in enumerate(row, 1):
                if v not in (None, ''):
                    ws.cell(row=r, column=col, value=v)
        e = f'OR(A{r}="",B{r}="")'
        g = lambda h: f'{c[h]}{r}'
        f = {}
        f['Source cluster'] = f'=IF({e},"",IFERROR(""&VLOOKUP(A{r},{pi("A")}:{PI}!$C${PI_LAST},3,FALSE),"Not in inventory"))'
        f['Target cluster'] = f'=IF({e},"",IFERROR(""&VLOOKUP(B{r},{pi("A")}:{PI}!$C${PI_LAST},3,FALSE),"Not in inventory"))'
        sc_, tc_ = g('Source cluster'), g('Target cluster')
        f['Same cluster?'] = f'=IF(OR({e},{sc_}="",{tc_}="",{sc_}="Not in inventory"),"",IF({sc_}={tc_},"Yes","No"))'
        f['Target status'] = f'=IF({e},"",IFERROR(VLOOKUP(B{r},{pi("A")}:{PI}!$F${PI_LAST},6,FALSE),"Not in inventory"))'
        ts = g('Target status')
        idx = f'IFERROR(VLOOKUP(B{r},{pi("A")}:{PI}!$G${PI_LAST},7,FALSE),"")'
        f['Target health'] = (f'=IF({e},"",IF({ts}="Not in inventory","Not in inventory",IF(N({ts})=0,"Unknown",IF({ts}>=400,"Broken",'
                              f'IF({ts}>=300,"Redirect",IF({idx}="No","Not indexable","OK"))))))')
        f['Self link?'] = f'=IF({e},"",IF(A{r}=B{r},"Yes","No"))'
        f['Counts as a content link?'] = f'=IF({e},"",IFERROR(VLOOKUP(D{r},{LT_RNG},2,FALSE),"No"))'
        f['Anchor words'] = f'=IF(OR({e},TRIM(C{r})=""),"",LEN(TRIM(C{r}))-LEN(SUBSTITUTE(TRIM(C{r})," ",""))+1)'
        f['Generic anchor?'] = f'=IF(OR({e},TRIM(C{r})=""),"",IF(COUNTIF({GEN_RNG},TRIM(C{r}))>0,"Yes","No"))'
        kw = f'IFERROR(""&VLOOKUP(B{r},{pi("A")}:{PI}!$D${PI_LAST},4,FALSE),"")'
        f['Anchor names the target topic?'] = f'=IF(OR({e},TRIM(C{r})="",{kw}=""),"",IF(ISNUMBER(SEARCH({kw},C{r})),"Yes","No"))'
        cl = c['Counts as a content link?']
        f['Same anchor to this target (content links)'] = (f'=IF(OR({e},TRIM(C{r})="",{cl}{r}<>"Yes"),"",COUNTIFS($B${LM_FIRST}:$B${LM_LAST},B{r},$C${LM_FIRST}:$C${LM_LAST},C{r},'
                                                         f'${c["Self link?"]}${LM_FIRST}:${c["Self link?"]}${LM_LAST},"No",${cl}${LM_FIRST}:${cl}${LM_LAST},"Yes"))')
        f['First link source to target (helper)'] = f'=IF({e},"",IF(COUNTIFS($A$4:A{r - 1},A{r},$B$4:B{r - 1},B{r})=0,1,0))'
        cc = c['Counts as a content link?']
        f['First content link (helper)'] = f'=IF(OR({e},{g("Counts as a content link?")}<>"Yes"),"",IF(COUNTIFS($A$4:A{r - 1},A{r},$B$4:B{r - 1},B{r},${cc}$4:{cc}{r - 1},"Yes")=0,1,0))'
        th, aw, ga, sl, fr = g('Target health'), g('Anchor words'), g('Generic anchor?'), g('Self link?'), g('First link source to target (helper)')
        issues = (f'_xlfn.TEXTJOIN("; ",TRUE,IF({th}="Broken","broken target",""),IF({th}="Redirect","redirected target: link the final URL",""),'
                  f'IF({th}="Not indexable","target is noindex",""),IF({th}="Not in inventory","target not in inventory",""),IF(TRIM(C{r})="","empty anchor",""),'
                  f'IF({ga}="Yes","generic anchor",""),IF(N({aw})>{MAXW},"long anchor",""),IF(E{r}="No","not a crawlable link",""),'
                  f'IF(F{r}="nofollow","nofollow on an internal link",""),IF({sl}="Yes","links to itself",""),IF({fr}=0,"repeat link (counted once)",""))')
        f['Issues'] = f'=IF({e},"",IF({issues}="","OK",{issues}))'
        for h, v in f.items():
            ws[f'{c[h]}{r}'] = v
    K.style_body(ws, LM_FIRST, LM_LAST, len(LMH), formula_cols=fc, wrap_cols=(3, 7, len(LMH)))
    K.dropdown(ws, f'A{LM_FIRST}:A{LM_LAST}', pi('A'))
    K.dropdown(ws, f'B{LM_FIRST}:B{LM_LAST}', pi('A'))
    K.dropdown(ws, f'D{LM_FIRST}:D{LM_LAST}', f'{S}!$F$25:$F$34')
    K.dropdown(ws, f'E{LM_FIRST}:E{LM_LAST}', f'{S}!$O$6:$O$7', 'Yes = an <a> element with an href. No = a JavaScript button or onclick link.')
    K.dropdown(ws, f'F{LM_FIRST}:F{LM_LAST}', f'{S}!$P$6:$P$9')
    iss = c['Issues']
    rng = f'{iss}{LM_FIRST}:{iss}{LM_LAST}'
    ws.conditional_formatting.add(rng, CellIsRule(operator='equal', formula=['"OK"'], fill=PatternFill('solid', fgColor='D9F2C4')))
    ws.conditional_formatting.add(rng, FormulaRule(formula=[f'OR(ISNUMBER(SEARCH("broken",{iss}{LM_FIRST})),ISNUMBER(SEARCH("crawlable",{iss}{LM_FIRST})))'], fill=PatternFill('solid', fgColor='F8D7D3'), font=Font(name=K.FONT, bold=True, color='9B2C1F')))
    ws.conditional_formatting.add(rng, FormulaRule(formula=[f'AND({iss}{LM_FIRST}<>"",{iss}{LM_FIRST}<>"OK")'], fill=PatternFill('solid', fgColor='FFF4CC')))
    th = c['Target health']
    ws.conditional_formatting.add(f'{th}{LM_FIRST}:{th}{LM_LAST}', FormulaRule(formula=[f'AND({th}{LM_FIRST}<>"",{th}{LM_FIRST}<>"OK")'], font=Font(name=K.FONT, bold=True, color='9B2C1F')))
    for h in ('First link source to target (helper)', 'First content link (helper)'):
        ws.column_dimensions[c[h]].hidden = True
    ws.freeze_panes = 'C5'
    ws.auto_filter.ref = f'A4:{L(len(LMH))}{LM_LAST}'
    return ws


def planner_sheet(wb):
    ws = wb.create_sheet('Link Planner')
    ws.sheet_view.showGridLines = False
    K.title_block(ws, 'Link planner', 'Plan each new internal link here before you add it. The verdict checks the target, the anchor and whether the link already exists. Mark it Added when it is live, then add it to the Link Map.')
    head = ['Source URL (add the link here)', 'Target URL (link to)', 'Proposed anchor', 'Placement', 'Status', 'Date added', 'Notes',
            'Source cluster', 'Target cluster', 'Same cluster?', 'Target health', 'Already linked?', 'Anchor words', 'Generic anchor?',
            'Anchor names the target topic?', 'Source impressions (donor strength)', 'Target still needs (content links)', 'Verdict']
    fc = tuple(range(8, 19))
    K.header_row(ws, 4, head, formula_cols=fc, widths=[40, 40, 30, 18, 10, 12, 30, 14, 14, 8, 12, 9, 8, 9, 10, 11, 10, 40])
    inv = f'{pi("A")}:{PI}!${L(len(HEAD))}${PI_LAST}'
    col_of = lambda h: list(M).index(h) + 1
    for r in range(LP_FIRST, LP_LAST + 1):
        i = r - LP_FIRST
        if i < len(PLAN):
            sx, tx, an, pl, st, dt, nt = PLAN[i]
            for col, v in enumerate([U + sx, U + tx, an, pl, st, d(dt), nt], 1):
                if v not in (None, ''):
                    ws.cell(row=r, column=col, value=v)
        e = f'OR(A{r}="",B{r}="")'
        ws.cell(row=r, column=8, value=f'=IF({e},"",IFERROR(""&VLOOKUP(A{r},{inv},3,FALSE),"Not in inventory"))')
        ws.cell(row=r, column=9, value=f'=IF({e},"",IFERROR(""&VLOOKUP(B{r},{inv},3,FALSE),"Not in inventory"))')
        ws.cell(row=r, column=10, value=f'=IF(OR({e},H{r}="",I{r}="",H{r}="Not in inventory"),"",IF(H{r}=I{r},"Yes","No"))')
        st = f'IFERROR(VLOOKUP(B{r},{inv},6,FALSE),"")'
        ix = f'IFERROR(VLOOKUP(B{r},{inv},7,FALSE),"")'
        ws.cell(row=r, column=11, value=f'=IF({e},"",IF({st}="","Not in inventory",IF(N({st})>=400,"Broken",IF(N({st})>=300,"Redirect",IF({ix}="No","Not indexable","OK")))))')
        ws.cell(row=r, column=12, value=f'=IF({e},"",IF(COUNTIFS({lm("A")},A{r},{lm("B")},B{r})>0,"Yes","No"))')
        ws.cell(row=r, column=13, value=f'=IF(OR({e},TRIM(C{r})=""),"",LEN(TRIM(C{r}))-LEN(SUBSTITUTE(TRIM(C{r})," ",""))+1)')
        ws.cell(row=r, column=14, value=f'=IF(OR({e},TRIM(C{r})=""),"",IF(COUNTIF({GEN_RNG},TRIM(C{r}))>0,"Yes","No"))')
        kw = f'IFERROR(""&VLOOKUP(B{r},{inv},4,FALSE),"")'
        ws.cell(row=r, column=15, value=f'=IF(OR({e},TRIM(C{r})="",{kw}=""),"",IF(ISNUMBER(SEARCH({kw},C{r})),"Yes","No"))')
        ws.cell(row=r, column=16, value=f'=IF({e},"",IFERROR(N(VLOOKUP(A{r},{inv},10,FALSE)),0))')
        ws.cell(row=r, column=17, value=f'=IF({e},"",IFERROR(VLOOKUP(B{r},{inv},{col_of("Content links to add")},FALSE),""))')
        ws.cell(row=r, column=18, value=(
            f'=IF({e},"",IF(E{r}="Rejected","Rejected",IF(E{r}="Added","Added: add it to the Link Map and recheck after the next crawl",'
            f'IF(A{r}=B{r},"Same page: pick another target",IF(K{r}<>"OK","Target not live: link the final URL",'
            f'IF(L{r}="Yes","Already linked: skip or improve the anchor",IF(TRIM(C{r})="","Write an anchor",IF(N{r}="Yes","Rewrite the anchor: generic",'
            f'IF(N(M{r})>{MAXW},"Shorten the anchor","Ready to add")))))))))'))
    K.style_body(ws, LP_FIRST, LP_LAST, len(head), formula_cols=fc, number_formats={6: 'dd mmm yyyy', 16: '#,##0'}, wrap_cols=(3, 7, 18))
    K.dropdown(ws, f'A{LP_FIRST}:A{LP_LAST}', pi('A'))
    K.dropdown(ws, f'B{LP_FIRST}:B{LP_LAST}', pi('A'))
    K.dropdown(ws, f'D{LP_FIRST}:D{LP_LAST}', f'{S}!$R$6:$R$9')
    K.dropdown(ws, f'E{LP_FIRST}:E{LP_LAST}', f'{S}!$Q$6:$Q$9')
    v = f'R{LP_FIRST}:R{LP_LAST}'
    ws.conditional_formatting.add(v, CellIsRule(operator='equal', formula=['"Ready to add"'], fill=PatternFill('solid', fgColor='D9F2C4'), font=Font(name=K.FONT, bold=True)))
    ws.conditional_formatting.add(v, FormulaRule(formula=[f'LEFT(R{LP_FIRST},5)="Added"'], fill=PatternFill('solid', fgColor='EEF8E6')))
    ws.conditional_formatting.add(v, FormulaRule(formula=[f'OR(LEFT(R{LP_FIRST},6)="Target",LEFT(R{LP_FIRST},7)="Rewrite",LEFT(R{LP_FIRST},4)="Same")'], fill=PatternFill('solid', fgColor='F8D7D3'), font=Font(name=K.FONT, bold=True, color='9B2C1F')))
    ws.conditional_formatting.add(v, FormulaRule(formula=[f'LEFT(R{LP_FIRST},7)="Already"'], fill=PatternFill('solid', fgColor='FFF4CC')))
    ws.freeze_panes = 'C5'
    ws.auto_filter.ref = f'A4:R{LP_LAST}'
    return ws


def chart(ws, title, ytitle, cat_col, val_cols, r1, r2, anchor, colors, horiz, titles, h=7.5, stacked=False):
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


DEPTHS = [('0 (home)', '=0', 0), ('1 click', '=1', 1), ('2 clicks', '=2', 2), ('3 clicks', '=3', 3), ('4 clicks', '=4', 4), ('5 or more', '>=5', 5)]


def dashboard_sheet(wb):
    ws = wb.create_sheet('Dashboard')
    ws.sheet_view.showGridLines = False
    K.title_block(ws, 'Dashboard', 'Everything here calculates from the other tabs. Nothing to type.')
    for c, w in zip('ABCDEFGHIJ', [44, 12, 3, 46, 22, 9, 9, 9, 34, 3]):
        ws.column_dimensions[c].width = w
    m = M
    sc, pr, live = m['Score (0 to 100)'], m['Priority'], m['Live page?']
    lmc = LMC
    kpis = [
        ('Pages in the inventory', f'=COUNTA({pi("A")})', '0'),
        ('Live pages (200 and indexable)', f'=COUNTIF({pi(live)},"Yes")', '0'),
        ('Average link score (live pages)', f'=IFERROR(ROUND(AVERAGE({pi(sc)}),0),0)', '0'),
        ('Orphan pages (no links in)', f'=COUNTIF({pi(m["Not an orphan"])},0)', '0'),
        ('Live pages the crawler cannot reach (no click depth)', f'=COUNTIFS({pi(live)},"Yes",{pi("I")},"")', '0'),
        ('Pages deeper than the click depth rule', f'=COUNTIFS({pi(live)},"Yes",{pi("I")},">"&{DPASS})', '0'),
        ('Internal links logged', f'=COUNTIF({lm(lmc["Self link?"])},"No")', '#,##0'),
        ('Links to broken pages', f'=COUNTIF({lm(lmc["Target health"])},"Broken")', '0'),
        ('Links to redirects', f'=COUNTIF({lm(lmc["Target health"])},"Redirect")', '0'),
        ('Links with a generic anchor', f'=COUNTIF({lm(lmc["Generic anchor?"])},"Yes")', '0'),
        ('Links that are not crawlable', f'=COUNTIF({lm("E")},"No")', '0'),
        ('Internal links with nofollow', f'=COUNTIF({lm("F")},"nofollow")', '0'),
        ('Pages linked from their hub (of those checked)', f'=COUNTIF({pi(m["Linked from hub?"])},"Yes")&" of "&(COUNTIF({pi(m["Linked from hub?"])},"Yes")+COUNTIF({pi(m["Linked from hub?"])},"No"))', '@'),
        ('Boost pages: close to the top, need links', f'=COUNTIF({pi(pr)},"Boost*")', '0'),
        ('Content links still to add (all live pages)', f'=SUM({pi(m["Content links to add"])})', '0'),
        ('Planned links ready to add', f"=COUNTIF('Link Planner'!$R${LP_FIRST}:$R${LP_LAST},\"Ready to add\")", '0'),
    ]
    ws['A4'] = 'KEY NUMBERS'
    ws['A4'].font = K.f(10, True, K.DEEP)
    for i, (label, fml, fmt) in enumerate(kpis):
        r = 5 + i
        ws.cell(row=r, column=1, value=label).font = K.f(10)
        c = ws.cell(row=r, column=2, value=fml)
        c.number_format, c.font, c.fill, c.border = fmt, K.f(11, True), K.FORMULA_FILL, K.BORDER
        c.alignment = Alignment(horizontal='right')
    ws['D4'] = 'PAGES THAT NEED LINKS MOST (biggest search demand first)'
    ws['D4'].font = K.f(10, True, K.DEEP)
    for j, h in enumerate(['URL', 'Focus keyword', 'Impressions', 'Links in', 'Links to add', 'Priority']):
        c = ws.cell(row=5, column=4 + j, value=h)
        c.font, c.fill = K.f(10, True, 'FFFFFF'), K.HEAD_F
    op = pi(m['Opportunity (helper)'])
    for k in range(1, 11):
        r = 5 + k
        mt = f'MATCH(LARGE({op},{k}),{op},0)'
        for j, col in enumerate(['A', 'D', 'J', m['Content links in (pages)'], m['Content links to add'], pr]):
            c = ws.cell(row=r, column=4 + j, value=f'=IFERROR(INDEX({pi(col)},{mt}),"")')
            c.border, c.fill, c.font = K.BORDER, K.FORMULA_FILL, K.f(9, j == 0)
            c.number_format = ['@', '@', '#,##0', '0', '0', '@'][j]
    top = 24
    ws.cell(row=top - 1, column=1, value='LIVE PAGES BY CLICK DEPTH').font = K.f(10, True, K.DEEP)
    for j, h in enumerate(['Click depth', 'Pages']):
        c = ws.cell(row=top, column=1 + j, value=h)
        c.font, c.fill = K.f(10, True, 'FFFFFF'), K.HEAD_F
    for i, (name, crit, _) in enumerate(DEPTHS):
        r = top + 1 + i
        ws.cell(row=r, column=1, value=name).border = K.BORDER
        c = ws.cell(row=r, column=2, value=f'=COUNTIFS({pi(live)},"Yes",{pi("I")},"{crit}")')
        c.border, c.fill = K.BORDER, K.FORMULA_FILL
    r = top + 1 + len(DEPTHS)
    ws.cell(row=r, column=1, value='Not reachable').border = K.BORDER
    c = ws.cell(row=r, column=2, value=f'=COUNTIFS({pi(live)},"Yes",{pi("I")},"")')
    c.border, c.fill = K.BORDER, K.FORMULA_FILL
    ct = r + 3
    ws.cell(row=ct - 1, column=1, value='TOPIC CLUSTERS').font = K.f(10, True, K.DEEP)
    for j, h in enumerate(['Cluster', 'Live pages', 'Avg content links in', 'Linked from hub', 'Orphans']):
        c = ws.cell(row=ct, column=1 + j, value=h)
        c.font, c.fill = K.f(10, True, 'FFFFFF'), K.HEAD_F
    for i in range(len(CLUSTERS) + 4):
        r = ct + 1 + i
        ws.cell(row=r, column=1, value=f'=IF({S}!J{6 + i}="","",{S}!J{6 + i})')
        ws.cell(row=r, column=2, value=f'=IF(A{r}="","",COUNTIFS({pi("C")},A{r},{pi(live)},"Yes"))')
        ws.cell(row=r, column=3, value=f'=IF(OR(A{r}="",N(B{r})=0),"",AVERAGEIFS({pi(m["Content links in (pages)"])},{pi("C")},A{r},{pi(live)},"Yes"))')
        ws.cell(row=r, column=4, value=f'=IF(A{r}="","",COUNTIFS({pi("C")},A{r},{pi(m["Linked from hub?"])},"Yes")&" of "&COUNTIFS({pi("C")},A{r},{pi(m["Is the hub?"])},"No",{pi(live)},"Yes"))')
        ws.cell(row=r, column=5, value=f'=IF(A{r}="","",COUNTIFS({pi("C")},A{r},{pi(m["Not an orphan"])},0))')
        for cc, fmt in ((1, '@'), (2, '0'), (3, '0.0'), (4, '@'), (5, '0')):
            cell = ws.cell(row=r, column=cc)
            cell.border, cell.fill, cell.number_format = K.BORDER, K.FORMULA_FILL, fmt
    t2 = ct + len(CLUSTERS) + 7
    for j, h in enumerate(['Check', 'Pages to fix', 'Partly']):
        c = ws.cell(row=t2, column=1 + j, value=h)
        c.font, c.fill = K.f(10, True, 'FFFFFF'), K.HEAD_F
    ws.cell(row=t2 - 1, column=1, value='PAGES FAILING EACH CHECK').font = K.f(10, True, K.DEEP)
    for i, col in enumerate(CK):
        r = t2 + 1 + i
        ws.cell(row=r, column=1, value=f'={S}!A{CHK_ROW + i}').border = K.BORDER
        for cc, val in ((2, 0), (3, 0.5)):
            c = ws.cell(row=r, column=cc, value=f'=COUNTIF({pi(col)},{val})')
            c.border, c.fill = K.BORDER, K.FORMULA_FILL
    ws.conditional_formatting.add(f'B{t2 + 1}:B{t2 + NCH}', ColorScaleRule(start_type='num', start_value=0, start_color='FFFFFF', end_type='num', end_value=6, end_color='E07A5F'))
    c1 = chart(ws, 'Live pages by click depth', 'Pages', 1, [2], top + 1, top + len(DEPTHS) + 1, 'D19', [K.GREEN], False, False)
    c1.y_axis.scaling.min = 0
    chart(ws, 'Pages failing each check', 'Pages', 1, [2, 3], t2 + 1, t2 + NCH, 'D36', ['E07A5F', 'F2C94C'], True, True, h=11, stacked=True)
    return ws, top, ct, t2


def build(path, asset, url):
    wb = K.new_book()
    inventory_sheet(wb)
    linkmap_sheet(wb)
    planner_sheet(wb)
    dashboard_sheet(wb)
    settings_sheet(wb)
    K.prompts_sheet(wb, asset['prompts'], url)
    K.checklist_sheet(wb, list(asset['checklist']))
    K.sources_sheet(wb, asset['sources'], [
        ('Demo data', 'LeafBox and every page in the demo are fictional (.example domain). All pages, links, status codes, click depths, impressions, clicks and positions are illustrative, not real data.', ''),
        ('Score', 'Weighted share of the 13 checks a page passes (pass 1, partly 0.5, fix 0). Checks without data are left out. Weights, targets, grade bands and priority rules live on Settings and are assumptions to tune.', ''),
        ('Crawlable links', 'Google says it can generally only crawl a link if it is an <a> element with an href attribute, and that links added with JavaScript are fine when they use that markup.', 'https://developers.google.com/search/docs/crawling-indexing/links-crawlable'),
        ('Orphan pages', 'Google says every page you care about should have a link from at least one other page on your site, and that there is no magical ideal number of links on a page.', 'https://developers.google.com/search/docs/crawling-indexing/links-crawlable'),
        ('Click depth', 'The 3 click rule is an assumption of this kit, in line with common SEO advice (for example Ahrefs: keep every page within three clicks of the homepage). Google gives no fixed number.', 'https://ahrefs.com/blog/internal-links-for-seo/'),
        ('Search Console Links report', 'The Top linked pages table for internal links is a sample, limited to 1,000 rows in the report, and groups pages by canonical URL. Use a crawler for a full link map.', 'https://support.google.com/webmasters/answer/9049606'),
    ])
    K.start_here(
        wb, 'Internal Linking Kit',
        [
            'This workbook maps every internal link on your site and checks every page against 13 rules that matter for Google and for AI search: no orphan pages, enough links in from related pages, a shallow click depth, links from and to the topic hub, descriptive and varied anchors, real crawlable links, no broken or redirected links and no internal nofollow.',
            f'It ships with demo data for a fictional plant shop ({len(P)} pages, {len(LINKS)} links and {len(PLAN)} planned links) so you can see every check working. Clear the yellow demo cells when you are ready.',
        ],
        [
            ('Page Inventory', 'One row per page with 500 ready rows: status, indexable, sitemap, click depth and Search Console numbers, plus 20 link measures, 13 checks, score, grade, fixes, priority and the content links each page still needs.'),
            ('Link Map', 'One row per internal link with 1,000 ready rows. Checks the target, the anchor, crawlability, rel and repeats for every link.'),
            ('Link Planner', 'Plan new links. The verdict checks the target is live, the link is new and the anchor is descriptive.'),
            ('Dashboard', 'Key numbers, the pages that need links most, click depth, topic clusters and pages failing each check, with two charts.'),
            ('Settings', 'Analysis date, link rules, the 13 check weights with rules and fixes, page types, priority targets, link types, clusters with hub pages, generic anchors and lists.'),
            ('AI Prompts', 'Prompts for ChatGPT, Claude or Gemini to find link ideas, write anchors and plan clusters.'),
            ('Checklist', 'The internal linking checklist as a tick list with automatic progress.'),
            ('Sources', 'Where facts come from and which numbers are assumptions.'),
        ],
        [
            'Look at the demo on Page Inventory, Link Map, Link Planner and the Dashboard, then clear the yellow demo cells.',
            'On Settings, set the analysis date, your topic clusters with their hub page URL and your page types.',
            'Crawl your site (any crawler) and paste URL, status code, indexable, in sitemap and click depth into Page Inventory. Add Search Console impressions, clicks and position for 28 days.',
            'Paste the internal links export (source, target, anchor) into Link Map and choose the link type, a href and rel.',
            'Sort Page Inventory by Priority: fix orphans and broken links first, then repoint links to redirects, then Boost pages close to the top.',
            'Plan each new link on Link Planner until it says Ready to add, add it on the site and mark it Added.',
            'Crawl again after a few weeks and compare the score, orphans and click depth on the Dashboard.',
        ],
        url,
    )
    order = ['Start Here', 'Page Inventory', 'Link Map', 'Link Planner', 'Dashboard', 'Settings', 'AI Prompts', 'Checklist', 'Sources']
    wb._sheets = [wb[n] for n in order]
    wb.active = 0
    for ws in wb.worksheets:
        ws.sheet_properties.tabColor = K.GREEN if ws.title in order[:5] else 'A6EF39'
    wb.save(path)


PREVIEW = {'sheet': 'Page Inventory', 'header_row': 4, 'rows': 12,
           'cols': [1, 2, NIN + 4, NIN + 5, SC, SC + 1, SC + 2, SC + 4],
           'formula_idx': [2, 3, 4, 5, 6, 7]}


def check(wb):
    """Assert the worked examples used in the guide."""
    a = wb['Page Inventory']
    v = lambda h, r: a[f'{M[h]}{r}'].value
    r = 13   # snake plant care
    assert a[f'A{r}'].value.endswith('/plant-care/snake-plant-care/')
    assert v('Pages linking in', r) == 2 and v('Content links in (pages)', r) == 2 and v('Generic anchor share', r) == 1, v('Pages linking in', r)
    assert v('Linked from hub?', r) == 'No' and v('Links to hub?', r) == 'Yes' and v('Redirected links out', r) == 1, v('Linked from hub?', r)
    assert v('Content links out (pages)', r) == 4 and v('Content links to add', r) == 3 and v('Anchor variety', r) is None, v('Content links out (pages)', r)
    assert v('Score (0 to 100)', r) == 61 and v('Grade', r) == 'C' and v('Fixes needed', r) == 5, v('Score (0 to 100)', r)
    assert v('Fixes in priority order', r) == ('Enough content links in; Shallow click depth (partly); Linked from its hub; Descriptive anchors; '
                                              'No redirected links out (partly)'), v('Fixes in priority order', r)
    assert v('Priority', r) == 'Boost: add links, close to the top', v('Priority', r)
    assert v('Priority', 10) == 'Fix now: orphan page' and v('Priority', 20) == 'Fix now: orphan page', (v('Priority', 10), v('Priority', 20))
    assert v('In XML sitemap', 20) == 0.5
    assert v('Priority', 21) == 'Fix links: page not live, repoint links' and v('Pages linking in', 21) == 2, v('Priority', 21)
    assert v('Priority', 22) == 'Fix links: page not live, repoint links' and v('Score (0 to 100)', 22) is None, v('Priority', 22)
    assert v('Priority', 14) == 'Fix now: broken links on this page' and v('Priority', 23) == 'Fix now: broken links on this page', v('Priority', 14)
    assert v('Shallow click depth', 15) == 0 and v('Priority', 15) == 'Restructure: page is too deep', v('Priority', 15)
    assert v('Crawlable links in', 18) == 0.5 and v('Followed internal links', 18) == 0.5, v('Crawlable links in', 18)
    assert v('Pages linking in', 7) == 6 and v('Links in (all)', 7) == 7, (v('Pages linking in', 7), v('Links in (all)', 7))
    lmap = wb['Link Map']
    c = LMC
    assert lmap[f'{c["Issues"]}18'].value == 'generic anchor' and lmap[f'{c["Issues"]}19'].value == 'redirected target: link the final URL', lmap[f'{c["Issues"]}18'].value
    assert lmap[f'{c["Issues"]}36'].value == 'broken target' and lmap[f'{c["Issues"]}46'].value == 'not a crawlable link', lmap[f'{c["Issues"]}46'].value
    assert lmap[f'{c["Issues"]}23'].value == 'links to itself' and lmap[f'{c["Issues"]}56'].value == 'repeat link (counted once)', lmap[f'{c["Issues"]}23'].value
    p = wb['Link Planner']
    exp = ['Ready to add', 'Ready to add', 'Ready to add', 'Already linked: skip or improve the anchor', 'Target not live: link the final URL',
           'Rewrite the anchor: generic', 'Added: add it to the Link Map and recheck after the next crawl', 'Ready to add']
    for i, x in enumerate(exp):
        assert p[f'R{LP_FIRST + i}'].value == x, (i, p[f'R{LP_FIRST + i}'].value)
    d = wb['Dashboard']
    vals = {d.cell(row=r, column=1).value: d.cell(row=r, column=2).value for r in range(5, 21)}
    assert vals['Orphan pages (no links in)'] == 2 and vals['Links to broken pages'] == 2 and vals['Links to redirects'] == 2, vals
    assert vals['Links with a generic anchor'] == 2 and vals['Live pages (200 and indexable)'] == 18, vals
    assert d['D6'].value.endswith('/shop/snake-plant/') is False and d['D6'].value.endswith('/plant-care/snake-plant-care/'), d['D6'].value
