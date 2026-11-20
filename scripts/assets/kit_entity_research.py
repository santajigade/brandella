"""Entity Research Kit workbook (asset 06).

Entity Map: one row per entity connected to a topic (500 rows). The sheet measures how often each entity
appears in the top results and in AI answers, scores its importance (0 to 100), sorts it into Main, Core,
Supporting or Peripheral, compares that with how well your page covers it and says what to do. It also
suggests the schema.org property (about or mentions) and builds a JSON-LD fragment with sameAs.
Topics: one row per topic or page with an importance weighted coverage score and a verdict.
AI Answer Check: the entities each AI answer names, matched against the map.
Brand Entity Audit: how clearly your own brand and authors are defined as entities.
Page Plan: one topic as a brief, with the top 12 entities and ready JSON-LD.
"""
import datetime
from openpyxl.styles import PatternFill, Font, Alignment
from openpyxl.formatting.rule import CellIsRule, ColorScaleRule, FormulaRule
from openpyxl.chart import BarChart, Reference
from openpyxl.utils import get_column_letter as L
import kitlib as K

MAP_FIRST, MAP_LAST = 5, 504     # Entity Map
TOP_FIRST, TOP_LAST = 5, 104     # Topics
AI_FIRST, AI_LAST = 5, 204       # AI Answer Check
S = 'Settings'
EM = "'Entity Map'"
TP = 'Topics'
AIS = "'AI Answer Check'"

CORE, SUPP, MINENT, STRONG, FILL = (f'{S}!$B${r}' for r in range(5, 10))
W1, W2, W3, W4, WT = (f'{S}!$B${r}' for r in range(12, 17))

TYPES = [('Person', 'Person'), ('Organization', 'Organization'), ('Brand or product', 'Product'), ('Place', 'Place'),
         ('Concept', 'Thing'), ('Event', 'Event'), ('Creative work', 'CreativeWork'), ('Other', 'Thing')]
ROLES = ['Main entity', 'Part or type of the main entity', 'Attribute or measure', 'Used with or related',
         'Person or organization behind it', 'Place', 'Alternative or comparison']
COVERAGE = ['None', 'Mentioned', 'Explained', 'Own section']
ENGINES = ['Google AI Overview', 'Google AI Mode', 'ChatGPT', 'Gemini', 'Perplexity', 'Copilot', 'Other']
STATUS = ['Done', 'Partly', 'Missing', 'Not relevant']
WIKI = 'https://en.wikipedia.org/wiki/'

# Demo: LeafLine Teas, a fictional online tea store in India. All counts, scores and AI answers are illustrative.
# topic, main entity, our page, results checked
TOPICS = [
    ('darjeeling first flush tea', 'Darjeeling tea', '/guides/darjeeling-first-flush/', 10),
    ('how to brew green tea', 'Green tea', '/guides/how-to-brew-green-tea/', 10),
    ('assam vs darjeeling tea', 'Assam tea and Darjeeling tea', '/guides/assam-vs-darjeeling/', 10),
    ('cold brew tea', 'Cold brew tea', '', 10),
]
# topic index, entity, type, role, results mentioning, PAA, reference url, coverage, salience
E = [
    (0, 'Darjeeling tea', 'Concept', 'Main entity', 10, 'Yes', WIKI + 'Darjeeling_tea', 'Own section', 0.41),
    (0, 'First flush', 'Concept', 'Part or type of the main entity', 10, 'Yes', '', 'Own section', 0.22),
    (0, 'Muscatel flavour', 'Concept', 'Attribute or measure', 6, 'Yes', '', 'None', None),
    (0, 'Water temperature', 'Concept', 'Attribute or measure', 8, 'Yes', '', 'Explained', 0.04),
    (0, 'Darjeeling', 'Place', 'Place', 8, 'No', WIKI + 'Darjeeling', 'Mentioned', 0.08),
    (0, 'Second flush', 'Concept', 'Part or type of the main entity', 6, 'Yes', '', 'Mentioned', 0.03),
    (0, 'Steeping time', 'Concept', 'Attribute or measure', 6, 'Yes', '', 'Explained', 0.03),
    (0, 'Camellia sinensis', 'Concept', 'Part or type of the main entity', 4, 'No', WIKI + 'Camellia_sinensis', 'Mentioned', 0.02),
    (0, 'Geographical indication', 'Concept', 'Used with or related', 4, 'No', WIKI + 'Geographical_indication', 'None', None),
    (0, 'Tea estate', 'Concept', 'Used with or related', 6, 'No', '', 'Explained', 0.05),
    (0, 'Black tea', 'Concept', 'Alternative or comparison', 4, 'No', WIKI + 'Black_tea', 'Mentioned', 0.01),
    (0, 'Leaf grade', 'Concept', 'Attribute or measure', 2, 'No', '', 'None', None),
    (1, 'Green tea', 'Concept', 'Main entity', 10, 'Yes', WIKI + 'Green_tea', 'Own section', None),
    (1, 'Water temperature', 'Concept', 'Attribute or measure', 10, 'Yes', '', 'Explained', None),
    (1, 'Steeping time', 'Concept', 'Attribute or measure', 10, 'Yes', '', 'Explained', None),
    (1, 'Bitterness', 'Concept', 'Attribute or measure', 8, 'Yes', '', 'None', None),
    (1, 'Matcha', 'Concept', 'Part or type of the main entity', 6, 'Yes', WIKI + 'Matcha', 'None', None),
    (1, 'Tea bag', 'Brand or product', 'Alternative or comparison', 6, 'Yes', '', 'None', None),
    (1, 'Loose leaf tea', 'Concept', 'Alternative or comparison', 8, 'No', '', 'None', None),
    (1, 'Sencha', 'Concept', 'Part or type of the main entity', 4, 'No', WIKI + 'Sencha', 'None', None),
    (1, 'Catechins', 'Concept', 'Attribute or measure', 4, 'No', WIKI + 'Catechin', 'None', None),
    (1, 'Kettle', 'Brand or product', 'Used with or related', 6, 'No', '', 'Mentioned', None),
    (1, 'Gaiwan', 'Brand or product', 'Used with or related', 2, 'No', WIKI + 'Gaiwan', 'None', None),
    (2, 'Assam tea', 'Concept', 'Main entity', 10, 'Yes', WIKI + 'Assam_tea', 'Own section', None),
    (2, 'Darjeeling tea', 'Concept', 'Main entity', 10, 'Yes', WIKI + 'Darjeeling_tea', 'Own section', None),
    (2, 'Caffeine', 'Concept', 'Attribute or measure', 8, 'Yes', WIKI + 'Caffeine', 'Explained', None),
    (2, 'Masala chai', 'Concept', 'Used with or related', 6, 'Yes', WIKI + 'Masala_chai', 'Explained', None),
    (2, 'CTC tea', 'Concept', 'Part or type of the main entity', 6, 'Yes', '', 'Mentioned', None),
    (2, 'Assam', 'Place', 'Place', 6, 'No', WIKI + 'Assam', 'Mentioned', None),
    (2, 'Malty flavour', 'Concept', 'Attribute or measure', 8, 'No', '', 'Explained', None),
    (2, 'Muscatel flavour', 'Concept', 'Attribute or measure', 6, 'No', '', 'Explained', None),
    (2, 'Price per 100 g', 'Concept', 'Attribute or measure', 6, 'No', '', 'Explained', None),
    (2, 'Camellia sinensis var. assamica', 'Concept', 'Part or type of the main entity', 4, 'No', '', 'None', None),
    (3, 'Cold brew tea', 'Concept', 'Main entity', 10, 'Yes', '', 'None', None),
    (3, 'Steeping time', 'Concept', 'Attribute or measure', 9, 'Yes', '', 'None', None),
    (3, 'Iced tea', 'Concept', 'Alternative or comparison', 6, 'No', WIKI + 'Iced_tea', 'None', None),
    (3, 'Oolong', 'Concept', 'Part or type of the main entity', 4, 'No', WIKI + 'Oolong', 'None', None),
]
# topic index, engine, date, shown, entities named (up to 8), brand named, page linked
AI = [
    (0, 'Google AI Overview', '2026-11-18', 'Yes', ['Darjeeling tea', 'First flush', 'Muscatel flavour', 'Darjeeling', 'Second flush', 'Spring harvest', 'Geographical indication'], 'No', 'No'),
    (0, 'ChatGPT', '2026-11-18', 'Yes', ['Darjeeling tea', 'First flush', 'Muscatel flavour', 'Steeping time', 'Water temperature', 'Camellia sinensis'], 'No', 'No'),
    (0, 'Perplexity', '2026-11-18', 'Yes', ['Darjeeling tea', 'First flush', 'Spring harvest', 'Tea estate', 'Muscatel flavour'], 'Yes', 'Yes'),
    (1, 'Google AI Overview', '2026-11-19', 'Yes', ['Green tea', 'Water temperature', 'Steeping time', 'Bitterness', 'Loose leaf tea', 'Tea bag'], 'No', 'No'),
    (1, 'ChatGPT', '2026-11-19', 'Yes', ['Green tea', 'Water temperature', 'Steeping time', 'Bitterness', 'Matcha', 'Sencha', 'Cold brewing'], 'No', 'No'),
    (2, 'Google AI Overview', '2026-11-19', 'Yes', ['Assam tea', 'Darjeeling tea', 'Malty flavour', 'Muscatel flavour', 'Caffeine', 'Masala chai'], 'No', 'No'),
    (2, 'Gemini', '2026-11-19', 'Yes', ['Assam tea', 'Darjeeling tea', 'Caffeine', 'CTC tea', 'Assam', 'Darjeeling'], 'Yes', 'No'),
]
# check, area, weight, demo status, evidence
BRAND = [
    ('One brand name, written the same way on the site, profiles and listings', 'Brand identity', 10, 'Done', 'LeafLine Teas everywhere'),
    ('Home or About page says clearly who you are, what you do and where', 'Brand identity', 8, 'Partly', 'About page has no founding year or address'),
    ('About page names the people behind the business, with history and contact details', 'Brand identity', 6, 'Partly', ''),
    ('Organization structured data on the home page or About page', 'Structured data', 10, 'Done', '/about/'),
    ('Organization markup includes name, url, logo and sameAs links to official profiles', 'Structured data', 8, 'Partly', 'sameAs missing'),
    ('Organization markup includes identifiers where relevant (for example vatID or iso6523Code)', 'Structured data', 4, 'Missing', ''),
    ('Logo file at least 112 x 112 px, crawlable, looks right on a white background', 'Structured data', 4, 'Done', '/img/logo.png'),
    ('Official social and directory profiles link back to the site and use the same name', 'Profiles', 6, 'Partly', '3 of 5 profiles'),
    ('Google Business Profile claimed and complete (if you serve customers in person)', 'Profiles', 8, 'Not relevant', 'Online only'),
    ('Every writer has an author page with a bio and real credentials', 'Authors', 8, 'Missing', ''),
    ('Visible byline on every article', 'Authors', 6, 'Done', ''),
    ('Article markup gives each author a type and a url (or sameAs), one author per field', 'Authors', 8, 'Missing', ''),
    ('Searched the brand name: knowledge panel shown and correct', 'Knowledge Graph', 4, 'Missing', 'No panel yet'),
    ('If a knowledge panel shows, it is claimed through Get verified on Google', 'Knowledge Graph', 4, 'Not relevant', ''),
    ('Independent sites mention the brand (press, partners, reviews)', 'Mentions', 6, 'Partly', '2 press mentions'),
    ('Brand named in AI answers for your main topics (see AI Answer Check)', 'AI answers', 6, 'Partly', '2 of 7 answers'),
]

MAP_HEAD = ['Topic', 'Entity', 'Entity type', 'Role', 'Top results that mention it', 'In People also ask or related searches?',
            'Reference URL for sameAs (Wikipedia, Wikidata or official site)', 'Our coverage', 'Salience (optional, 0 to 1)', 'Notes',
            'Results checked', 'SERP share', 'AI answers checked', 'AI answers naming it', 'AI share', 'Importance (0 to 100)', 'Tier',
            'Coverage points', 'Coverage needed', 'Gap', 'Next action', 'Schema property', 'sameAs check', 'Salience check',
            'Earned (helper)', 'Possible (helper)', 'Gap weight (helper)', 'Rank in topic', 'Key (helper)', 'Row (helper)', 'Gap key (helper)', 'JSON-LD fragment']
MAP_F = tuple(range(11, 33))
TOP_HEAD = ['Topic or keyword', 'Main entity', 'Our page URL', 'Top results checked', 'Notes', 'Entities mapped', 'Main and core entities',
            'Main and core covered', 'Coverage score', 'Critical gaps', 'All gaps', 'Missing reference URLs', 'AI answers checked',
            'Brand named in AI answers', 'Biggest gap', 'Verdict', 'Next step']
TOP_F = tuple(range(6, 18))


def em(c):
    return f'{EM}!${c}${MAP_FIRST}:${c}${MAP_LAST}'


def tp(c):
    return f'{TP}!${c}${TOP_FIRST}:${c}${TOP_LAST}'


def ai(c):
    return f'{AIS}!${c}${AI_FIRST}:${c}${AI_LAST}'


def d(s):
    return datetime.date.fromisoformat(s) if s else None


def verdict_rules(ws, rng, first):
    ws.conditional_formatting.add(rng, FormulaRule(formula=[f'LEFT({first},6)="Strong"'], fill=PatternFill('solid', fgColor='9BE07A'), font=Font(name=K.FONT, bold=True)))
    ws.conditional_formatting.add(rng, FormulaRule(formula=[f'LEFT({first},4)="Fill"'], fill=PatternFill('solid', fgColor='FFF4CC')))
    ws.conditional_formatting.add(rng, FormulaRule(formula=[f'LEFT({first},4)="Thin"'], fill=PatternFill('solid', fgColor='F8D7D3'), font=Font(name=K.FONT, bold=True, color='9B2C1F')))


def settings_sheet(wb):
    ws = wb.create_sheet(S)
    ws.sheet_view.showGridLines = False
    K.title_block(ws, 'Settings', 'Every threshold, weight and list used by this workbook. Change a blue number and every score updates.')
    for c, w in zip('ABCDEFGHIJK', [58, 12, 3, 20, 16, 3, 32, 14, 9, 20, 14]):
        ws.column_dimensions[c].width = w
    rows = [
        (4, 'TIERS AND VERDICTS', None, None),
        (5, 'Core entity when importance is at least', 55, '0'),
        (6, 'Supporting entity when importance is at least (below = Peripheral)', 30, '0'),
        (7, 'Minimum entities mapped before a topic gets a coverage score', 5, '0'),
        (8, 'Strong entity coverage when the coverage score is at least', 0.8, '0%'),
        (9, 'Fill the gaps when at least (below = Thin)', 0.5, '0%'),
        (11, 'IMPORTANCE WEIGHTS (any numbers, they are scaled)', None, None),
        (12, 'Share of top results that mention the entity', 45, '0'),
        (13, 'Share of AI answers that name the entity', 30, '0'),
        (14, 'Appears in People also ask or related searches', 15, '0'),
        (15, 'Has a reference URL (a well defined, known entity)', 10, '0'),
        (16, 'Total (auto)', '=SUM(B12:B15)', '0'),
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
    notes = [
        (18, 'Coverage needed by tier: Main entity needs its Own section, Core needs Explained, Supporting needs Mentioned, Peripheral is optional.'),
        (19, 'When a topic has no AI answers logged yet, the AI weight is left out and the other weights are scaled up.'),
        (20, 'All thresholds and weights are starter assumptions chosen for this kit, not Google rules. Tune them to your niche.'),
    ]
    for r, t in notes:
        ws.cell(row=r, column=1, value=t).font = K.f(9, False, '777777', True)
        ws.cell(row=r, column=1).alignment = Alignment(wrap_text=True)
        ws.row_dimensions[r].height = 28
    ws['D4'] = 'ENTITY TYPE AND SCHEMA.ORG TYPE'
    ws['D4'].font = K.f(10, True, K.DEEP)
    for i, (t, st) in enumerate(TYPES):
        ws.cell(row=5 + i, column=4, value=t).fill = K.INPUT_FILL
        ws.cell(row=5 + i, column=5, value=st).fill = K.INPUT_FILL
    ws['G4'] = 'DROPDOWN LISTS'
    ws['G4'].font = K.f(10, True, K.DEEP)
    lists = {'G': ['Role'] + ROLES, 'H': ['Coverage'] + COVERAGE, 'I': ['Yes/No', 'Yes', 'No'], 'J': ['AI engine'] + ENGINES, 'K': ['Status'] + STATUS}
    for c, vals in lists.items():
        for i, v in enumerate(vals):
            cell = ws[f'{c}{5 + i}']
            cell.value = v
            cell.font = K.f(9, i == 0, '555555')
    return ws


def map_sheet(wb):
    ws = wb.create_sheet('Entity Map')
    ws.sheet_view.showGridLines = False
    K.title_block(ws, 'Entity map', f'Rows 5 to {4 + len(E)} hold DEMO data for LeafLine Teas, a fictional tea store: 4 topics, {len(E)} entities (illustrative counts). Select the yellow demo cells and press Delete to start your own. Grey formula columns stay.')
    ws['A2'].font = K.f(10, True, 'B45309')
    ws['A3'] = 'One row per entity (person, place, thing or idea) connected to a topic. Add the topic on the Topics tab first. Count how many of the top results mention each entity. 500 rows ready.'
    ws['A3'].font = K.f(9, False, '666666', True)
    widths = [28, 26, 16, 24, 10, 11, 38, 12, 10, 18, 8, 8, 8, 8, 8, 10, 11, 8, 8, 13, 46, 10, 18, 22, 8, 8, 8, 8, 10, 6, 10, 50]
    K.header_row(ws, 4, MAP_HEAD, formula_cols=MAP_F, widths=widths)
    cov = f'{S}!$H$6:$H$9'
    for r in range(MAP_FIRST, MAP_LAST + 1):
        i = r - MAP_FIRST
        if i < len(E):
            t, name, typ, role, n, paa, url, c, sal = E[i]
            for col, v in enumerate([TOPICS[t][0], name, typ, role, n, paa, url, c, sal], 1):
                if v not in (None, ''):
                    ws.cell(row=r, column=col, value=v)
        b = f'B{r}=""'
        ws.cell(row=r, column=11, value=f'=IF(A{r}="","",IFERROR(INDEX({tp("D")},MATCH(A{r},{tp("A")},0)),""))')
        ws.cell(row=r, column=12, value=f'=IF(OR({b},N(K{r})=0),"",MIN(1,N(E{r})/K{r}))')
        ws.cell(row=r, column=13, value=f'=IF(A{r}="","",COUNTIFS({ai("A")},A{r},{ai("D")},"Yes"))')
        named = '+'.join(f'COUNTIFS({ai("A")},$A{r},{ai("D")},"Yes",{ai(c)},$B{r})' for c in 'EFGHIJKL')
        ws.cell(row=r, column=14, value=f'=IF({b},"",{named})')
        ws.cell(row=r, column=15, value=f'=IF(OR({b},N(M{r})=0),"",MIN(1,N{r}/M{r}))')
        num = f'{W1}*N(L{r})+IF(N(M{r})>0,{W2}*N(O{r}),0)+{W3}*(F{r}="Yes")+{W4}*(G{r}<>"")'
        den = f'({WT}-IF(N(M{r})>0,0,{W2}))'
        ws.cell(row=r, column=16, value=f'=IF({b},"",IF(D{r}="Main entity",100,ROUND(100*({num})/{den},0)))')
        ws.cell(row=r, column=17, value=f'=IF({b},"",IF(D{r}="Main entity","Main",IF(P{r}>={CORE},"Core",IF(P{r}>={SUPP},"Supporting","Peripheral"))))')
        ws.cell(row=r, column=18, value=f'=IF({b},"",IFERROR(MATCH(H{r},{cov},0)-1,0))')
        ws.cell(row=r, column=19, value=f'=IF({b},"",IF(Q{r}="Main",3,IF(Q{r}="Core",2,IF(Q{r}="Supporting",1,0))))')
        ws.cell(row=r, column=20, value=(
            f'=IF({b},"",IF(S{r}=0,"Optional",IF(R{r}>=S{r},"Covered",IF(AND(R{r}=0,OR(Q{r}="Main",Q{r}="Core")),"Critical gap",IF(R{r}=0,"Gap","Partly covered")))))'))
        ws.cell(row=r, column=21, value=(
            f'=IF({b},"",IF(T{r}="Covered","Keep it accurate and up to date",'
            f'IF(Q{r}="Main","Make it the clear subject: name it in the title, H1 and first paragraph and give it its own section",'
            f'IF(AND(Q{r}="Core",R{r}=0),"Add a section that explains what it is and how it connects to the main entity",'
            f'IF(Q{r}="Core","Explain it properly, not just a passing mention",'
            f'IF(Q{r}="Supporting","Mention it where it fits, with a link if you have a page on it","Optional: include only if it helps the reader"))))))'))
        ws.cell(row=r, column=22, value=f'=IF({b},"",IF(Q{r}="Main",IF(R{r}>=1,"about",""),IF(AND(R{r}>=1,OR(Q{r}="Core",Q{r}="Supporting")),"mentions","")))')
        ws.cell(row=r, column=23, value=f'=IF({b},"",IF(Q{r}="Peripheral","",IF(G{r}<>"","Has reference URL","Find a reference URL")))')
        ws.cell(row=r, column=24, value=(
            f'=IF(OR({b},I{r}=""),"",IF(D{r}<>"Main entity","",IF(I{r}>=_xlfn.MAXIFS($I${MAP_FIRST}:$I${MAP_LAST},$A${MAP_FIRST}:$A${MAP_LAST},A{r}),'
            f'"Most salient entity: good","Another entity is more salient: tighten the focus")))'))
        ws.cell(row=r, column=25, value=f'=IF({b},"",IF(S{r}>0,P{r}*MIN(1,R{r}/S{r}),0))')
        ws.cell(row=r, column=26, value=f'=IF({b},"",IF(S{r}>0,P{r},0))')
        ws.cell(row=r, column=27, value=f'=IF({b},"",IF(OR(T{r}="Covered",T{r}="Optional"),0,P{r}))')
        ws.cell(row=r, column=28, value=(
            f'=IF({b},"",COUNTIFS($A${MAP_FIRST}:$A${MAP_LAST},A{r},$P${MAP_FIRST}:$P${MAP_LAST},">"&P{r})'
            f'+COUNTIFS($A${MAP_FIRST}:$A${MAP_LAST},A{r},$P${MAP_FIRST}:$P${MAP_LAST},P{r},$AD${MAP_FIRST}:$AD${MAP_LAST},"<"&AD{r})+1)'))
        ws.cell(row=r, column=29, value=f'=IF({b},"",A{r}&"|"&AB{r})')
        ws.cell(row=r, column=30, value=f'=ROW()')
        ws.cell(row=r, column=31, value=f'=IF({b},"",A{r}&"|"&AA{r})')
        st = f'IFERROR(VLOOKUP(C{r},{S}!$D$5:$E${4 + len(TYPES)},2,FALSE),"Thing")'
        nm = f'SUBSTITUTE(B{r},CHAR(34),"")'
        ws.cell(row=r, column=32, value=(
            f'=IF({b},"","{{""@type"":"""&{st}&""",""name"":"""&{nm}&""""&IF(G{r}<>"",",""sameAs"":"""&G{r}&"""","")&"}}")'))
    K.style_body(ws, MAP_FIRST, MAP_LAST, len(MAP_HEAD), formula_cols=MAP_F,
                 number_formats={9: '0.00', 12: '0%', 15: '0%', 16: '0', 25: '0.0'}, wrap_cols=(2, 21))
    ws.freeze_panes = 'C5'
    ws.auto_filter.ref = f'A4:{L(len(MAP_HEAD))}{MAP_LAST}'
    K.dropdown(ws, f'A{MAP_FIRST}:A{MAP_LAST}', tp('A'), 'Pick a topic from the Topics tab')
    K.dropdown(ws, f'C{MAP_FIRST}:C{MAP_LAST}', f'{S}!$D$5:$D${4 + len(TYPES)}')
    K.dropdown(ws, f'D{MAP_FIRST}:D{MAP_LAST}', f'{S}!$G$6:$G${5 + len(ROLES)}')
    K.whole_number(ws, f'E{MAP_FIRST}:E{MAP_LAST}', 0, 20, 'How many of the top results mention this entity (0 to 20).')
    K.dropdown(ws, f'F{MAP_FIRST}:F{MAP_LAST}', f'{S}!$I$6:$I$7')
    K.dropdown(ws, f'H{MAP_FIRST}:H{MAP_LAST}', f'{S}!$H$6:$H$9')
    q = f'Q{MAP_FIRST}:Q{MAP_LAST}'
    for val, col, bold in (('Main', '6CC82A', True), ('Core', '9BE07A', True), ('Supporting', 'DCEBFF', False), ('Peripheral', 'F2F2F2', False)):
        ws.conditional_formatting.add(q, CellIsRule(operator='equal', formula=[f'"{val}"'], fill=PatternFill('solid', fgColor=col), font=Font(name=K.FONT, bold=bold)))
    t = f'T{MAP_FIRST}:T{MAP_LAST}'
    ws.conditional_formatting.add(t, CellIsRule(operator='equal', formula=['"Critical gap"'], fill=PatternFill('solid', fgColor='F8D7D3'), font=Font(name=K.FONT, bold=True, color='9B2C1F')))
    ws.conditional_formatting.add(t, CellIsRule(operator='equal', formula=['"Gap"'], fill=PatternFill('solid', fgColor='FCE4D6')))
    ws.conditional_formatting.add(t, CellIsRule(operator='equal', formula=['"Partly covered"'], fill=PatternFill('solid', fgColor='FFF4CC')))
    ws.conditional_formatting.add(t, CellIsRule(operator='equal', formula=['"Covered"'], fill=PatternFill('solid', fgColor='D9F2C4')))
    ws.conditional_formatting.add(f'P{MAP_FIRST}:P{MAP_LAST}', ColorScaleRule(start_type='num', start_value=0, start_color='FFFFFF', end_type='num', end_value=100, end_color='6CC82A'))
    ws.conditional_formatting.add(f'W{MAP_FIRST}:W{MAP_LAST}', CellIsRule(operator='equal', formula=['"Find a reference URL"'], font=Font(name=K.FONT, bold=True, color='B45309')))
    ws.conditional_formatting.add(f'X{MAP_FIRST}:X{MAP_LAST}', FormulaRule(formula=[f'LEFT(X{MAP_FIRST},7)="Another"'], font=Font(name=K.FONT, bold=True, color='9B2C1F')))
    return ws


def topics_sheet(wb):
    ws = wb.create_sheet(TP)
    ws.sheet_view.showGridLines = False
    K.title_block(ws, 'Topics and coverage', 'One row per topic or page. Type the yellow cells. Grey columns summarise the Entity Map and the AI Answer Check and give a verdict.')
    K.header_row(ws, 4, TOP_HEAD, formula_cols=TOP_F, widths=[30, 24, 30, 9, 18, 9, 9, 9, 9, 8, 8, 10, 9, 10, 22, 30, 52])
    for r in range(TOP_FIRST, TOP_LAST + 1):
        i = r - TOP_FIRST
        if i < len(TOPICS):
            for col, v in enumerate(TOPICS[i], 1):
                if v not in (None, ''):
                    ws.cell(row=r, column=col, value=v)
        a = f'$A{r}'
        e = f'A{r}=""'
        ws.cell(row=r, column=6, value=f'=IF({e},"",COUNTIF({em("A")},{a}))')
        ws.cell(row=r, column=7, value=f'=IF({e},"",COUNTIFS({em("A")},{a},{em("Q")},"Main")+COUNTIFS({em("A")},{a},{em("Q")},"Core"))')
        ws.cell(row=r, column=8, value=(
            f'=IF({e},"",COUNTIFS({em("A")},{a},{em("Q")},"Main",{em("T")},"Covered")+COUNTIFS({em("A")},{a},{em("Q")},"Core",{em("T")},"Covered"))'))
        ws.cell(row=r, column=9, value=(
            f'=IF(OR({e},N(F{r})<{MINENT}),"",IFERROR(SUMIFS({em("Y")},{em("A")},{a})/SUMIFS({em("Z")},{em("A")},{a}),""))'))
        ws.cell(row=r, column=10, value=f'=IF({e},"",COUNTIFS({em("A")},{a},{em("T")},"Critical gap"))')
        ws.cell(row=r, column=11, value=(
            f'=IF({e},"",COUNTIFS({em("A")},{a},{em("T")},"Critical gap")+COUNTIFS({em("A")},{a},{em("T")},"Gap")+COUNTIFS({em("A")},{a},{em("T")},"Partly covered"))'))
        ws.cell(row=r, column=12, value=f'=IF({e},"",COUNTIFS({em("A")},{a},{em("W")},"Find a reference URL"))')
        ws.cell(row=r, column=13, value=f'=IF({e},"",COUNTIFS({ai("A")},{a},{ai("D")},"Yes"))')
        ws.cell(row=r, column=14, value=f'=IF(OR({e},N(M{r})=0),"",COUNTIFS({ai("A")},{a},{ai("D")},"Yes",{ai("M")},"Yes")/M{r})')
        mx = f'_xlfn.MAXIFS({em("AA")},{em("A")},{a})'
        ws.cell(row=r, column=15, value=f'=IF(OR({e},N(F{r})=0),"",IF({mx}=0,"None",IFERROR(INDEX({em("B")},MATCH({a}&"|"&{mx},{em("AE")},0)),"")))')
        ws.cell(row=r, column=16, value=(
            f'=IF({e},"",IF(N(F{r})<{MINENT},"Map at least "&{MINENT}&" entities",IF(I{r}>={STRONG},"Strong entity coverage",'
            f'IF(I{r}>={FILL},"Fill the gaps","Thin: rebuild around the core entities"))))'))
        ws.cell(row=r, column=17, value=(
            f'=IF({e},"",IF(N(F{r})<{MINENT},"Check the top results and AI answers and map more entities",'
            f'IF(J{r}>0,"Start with the biggest gap: "&O{r}&". "&J{r}&" critical gap(s) in total",'
            f'IF(K{r}>0,"Close the remaining "&K{r}&" gap(s), starting with "&O{r},'
            f'IF(L{r}>0,"Add reference URLs for "&L{r}&" entities and mark them up",'
            f'IF(AND(N(M{r})>0,N(N{r})<0.5),"Coverage is strong: now earn mentions so AI answers name your brand","Keep it fresh and recheck every quarter"))))))'))
    K.style_body(ws, TOP_FIRST, TOP_LAST, len(TOP_HEAD), formula_cols=TOP_F, number_formats={9: '0%', 14: '0%'}, wrap_cols=(16, 17))
    ws.freeze_panes = 'B5'
    ws.auto_filter.ref = f'A4:{L(len(TOP_HEAD))}{TOP_LAST}'
    K.whole_number(ws, f'D{TOP_FIRST}:D{TOP_LAST}', 1, 20, 'How many top results you checked (usually 10).')
    verdict_rules(ws, f'P{TOP_FIRST}:P{TOP_LAST}', f'P{TOP_FIRST}')
    ws.conditional_formatting.add(f'I{TOP_FIRST}:I{TOP_LAST}', ColorScaleRule(start_type='num', start_value=0, start_color='F8D7D3', mid_type='num', mid_value=0.5, mid_color='FFF4CC', end_type='num', end_value=1, end_color='B7E4A0'))
    ws.conditional_formatting.add(f'J{TOP_FIRST}:J{TOP_LAST}', CellIsRule(operator='greaterThan', formula=['0'], font=Font(name=K.FONT, bold=True, color='9B2C1F')))
    return ws


def ai_sheet(wb):
    ws = wb.create_sheet('AI Answer Check')
    ws.sheet_view.showGridLines = False
    K.title_block(ws, 'AI answer check', 'Ask the topic in an AI Overview, AI Mode or an assistant. Type the entities the answer names, spelled exactly as in your Entity Map. The map counts them by itself.')
    head = ['Topic', 'AI engine', 'Date checked', 'AI answer shown?'] + [f'Entity named {i}' for i in range(1, 9)] + [
        'Your brand named?', 'Your page linked?', 'Notes', 'Entities named', 'Already in your map', 'Explained on your page', 'New to your map', 'What it tells you']
    fc = (16, 17, 18, 19, 20)
    K.header_row(ws, 4, head, formula_cols=fc, widths=[28, 18, 12, 9] + [17] * 8 + [9, 9, 16, 9, 9, 10, 9, 52])
    for r in range(AI_FIRST, AI_LAST + 1):
        i = r - AI_FIRST
        if i < len(AI):
            t, eng, dt, shown, names, brand, linked = AI[i]
            names = names + [None] * (8 - len(names))
            for col, v in enumerate([TOPICS[t][0], eng, d(dt), shown] + names + [brand, linked], 1):
                if v not in (None, ''):
                    ws.cell(row=r, column=col, value=v)
        e = f'A{r}=""'
        ws.cell(row=r, column=16, value=f'=IF({e},"",COUNTA(E{r}:L{r}))')
        inmap = '+'.join(f'IF({c}{r}="",0,MIN(1,COUNTIFS({em("A")},$A{r},{em("B")},{c}{r})))' for c in 'EFGHIJKL')
        ws.cell(row=r, column=17, value=f'=IF({e},"",{inmap})')
        expl = '+'.join(f'IF({c}{r}="",0,MIN(1,COUNTIFS({em("A")},$A{r},{em("B")},{c}{r},{em("R")},">=2")))' for c in 'EFGHIJKL')
        ws.cell(row=r, column=18, value=f'=IF({e},"",{expl})')
        ws.cell(row=r, column=19, value=f'=IF({e},"",P{r}-Q{r})')
        ws.cell(row=r, column=20, value=(
            f'=IF({e},"",IF(D{r}<>"Yes","No AI answer for this topic yet",IF(P{r}=0,"Type the entities the answer names",'
            f'IF(S{r}>0,"Add the "&S{r}&" new entity(ies) to your Entity Map",'
            f'IF(Q{r}>R{r},"The answer names "&(Q{r}-R{r})&" entity(ies) your page does not explain yet",'
            f'IF(M{r}<>"Yes","Your page covers these entities: now earn a mention of your brand","Covered and named: keep the page fresh"))))))'))
    K.style_body(ws, AI_FIRST, AI_LAST, len(head), formula_cols=fc, number_formats={3: 'dd mmm yyyy'}, wrap_cols=(20,))
    K.dropdown(ws, f'A{AI_FIRST}:A{AI_LAST}', tp('A'))
    K.dropdown(ws, f'B{AI_FIRST}:B{AI_LAST}', f'{S}!$J$6:$J${5 + len(ENGINES)}')
    for c in 'DMN':
        K.dropdown(ws, f'{c}{AI_FIRST}:{c}{AI_LAST}', f'{S}!$I$6:$I$7')
    p = f'T{AI_FIRST}:T{AI_LAST}'
    ws.conditional_formatting.add(p, FormulaRule(formula=[f'LEFT(T{AI_FIRST},3)="Add"'], fill=PatternFill('solid', fgColor='FCE4D6'), font=Font(name=K.FONT, bold=True)))
    ws.conditional_formatting.add(p, FormulaRule(formula=[f'LEFT(T{AI_FIRST},10)="The answer"'], fill=PatternFill('solid', fgColor='FFF4CC')))
    ws.conditional_formatting.add(p, FormulaRule(formula=[f'LEFT(T{AI_FIRST},7)="Covered"'], fill=PatternFill('solid', fgColor='9BE07A')))
    ws.freeze_panes = 'B5'
    return ws


def brand_sheet(wb):
    ws = wb.create_sheet('Brand Entity Audit')
    ws.sheet_view.showGridLines = False
    K.title_block(ws, 'Brand entity audit', 'How clearly your own business and your authors are defined as entities. Choose a status for each check. Weights are editable.')
    head = ['Check', 'Area', 'Weight', 'Status', 'Evidence or URL', 'Owner', 'Due date', 'Points earned', 'Points possible', 'Priority']
    K.header_row(ws, 6, head, formula_cols=(8, 9, 10), widths=[70, 16, 8, 12, 30, 12, 12, 9, 9, 12])
    ws['A4'] = 'Brand entity score'
    ws['A4'].font = K.f(12, True)
    n = len(BRAND)
    first, last = 7, 7 + n - 1 + 10
    c = ws['C4']
    c.value = f'=IFERROR(SUM(H{first}:H{last})/SUM(I{first}:I{last}),0)'
    c.number_format = '0%'
    c.font = K.f(14, True, K.DEEP)
    c.fill = K.FORMULA_FILL
    ws['D4'] = f'=IF(C4>=0.8,"Well defined",IF(C4>=0.5,"Partly defined","Weak: start with the Fix first rows"))'
    ws['D4'].font = K.f(11, True)
    owners = ['Asha', 'Asha', 'Ravi', 'Ravi', 'Ravi', 'Ravi', 'Ravi', 'Asha', '', 'Asha', 'Asha', 'Ravi', 'Asha', '', 'Asha', 'Asha']
    for i in range(last - first + 1):
        r = first + i
        if i < n:
            chk, area, w, st, ev = BRAND[i]
            for col, v in enumerate([chk, area, w, st, ev, owners[i]], 1):
                if v not in (None, ''):
                    ws.cell(row=r, column=col, value=v)
            if st in ('Missing', 'Partly'):
                ws.cell(row=r, column=7, value=datetime.date(2026, 12, 15 if w >= 8 else 31))
        ws.cell(row=r, column=8, value=f'=IF(OR(A{r}="",D{r}="",D{r}="Not relevant"),0,N(C{r})*IF(D{r}="Done",1,IF(D{r}="Partly",0.5,0)))')
        ws.cell(row=r, column=9, value=f'=IF(OR(A{r}="",D{r}="",D{r}="Not relevant"),0,N(C{r}))')
        ws.cell(row=r, column=10, value=f'=IF(OR(A{r}="",D{r}=""),"",IF(D{r}="Not relevant","",IF(D{r}="Done","Done",IF(AND(D{r}="Missing",N(C{r})>=8),"Fix first","Next"))))')
    K.style_body(ws, first, last, len(head), formula_cols=(8, 9, 10), number_formats={7: 'dd mmm yyyy', 8: '0.0'}, wrap_cols=(1, 5))
    K.dropdown(ws, f'D{first}:D{last}', f'{S}!$K$6:$K$9')
    j = f'J{first}:J{last}'
    ws.conditional_formatting.add(j, CellIsRule(operator='equal', formula=['"Fix first"'], fill=PatternFill('solid', fgColor='F8D7D3'), font=Font(name=K.FONT, bold=True, color='9B2C1F')))
    ws.conditional_formatting.add(j, CellIsRule(operator='equal', formula=['"Next"'], fill=PatternFill('solid', fgColor='FFF4CC')))
    ws.conditional_formatting.add(j, CellIsRule(operator='equal', formula=['"Done"'], fill=PatternFill('solid', fgColor='D9F2C4')))
    ws.freeze_panes = 'A7'
    return ws, first, last


def plan_sheet(wb):
    ws = wb.create_sheet('Page Plan')
    ws.sheet_view.showGridLines = False
    for c, w in zip('ABCDEFGHIJK', [30, 30, 16, 12, 10, 12, 14, 52, 36, 11, 10]):
        ws.column_dimensions[c].width = w
    K.title_block(ws, 'Page plan', 'Choose a topic in the yellow cell. The summary, the top 12 entities and the JSON-LD fill in by themselves. Then write your brief below.')
    ws['A4'] = 'Topic'
    ws['A4'].font = K.f(11, True)
    ws['B4'] = TOPICS[0][0]
    ws['B4'].fill = K.INPUT_FILL
    ws['B4'].font = K.f(11, True)
    ws['B4'].border = K.BORDER
    K.dropdown(ws, 'B4', tp('A'), 'Pick a topic from the Topics tab')
    m = f'MATCH($B$4,{tp("A")},0)'
    items = [('Main entity', 'B', None), ('Our page URL', 'C', None), ('Entities mapped', 'F', '0'), ('Main and core entities', 'G', '0'),
             ('Main and core covered', 'H', '0'), ('Coverage score', 'I', '0%'), ('Critical gaps', 'J', '0'), ('Missing reference URLs', 'L', '0'),
             ('Brand named in AI answers', 'N', '0%'), ('Biggest gap', 'O', None), ('Verdict', 'P', None), ('Next step', 'Q', None)]
    ws['A6'] = 'TOPIC SUMMARY'
    ws['A6'].font = K.f(10, True, K.DEEP)
    for i, (label, col, fmt) in enumerate(items):
        r = 7 + i
        ws.cell(row=r, column=1, value=label).font = K.f(10)
        c = ws.cell(row=r, column=2, value=f'=IFERROR(INDEX({tp(col)},{m})&"","")' if fmt is None else f'=IFERROR(INDEX({tp(col)},{m}),"")')
        c.fill, c.border = K.FORMULA_FILL, K.BORDER
        c.font = K.f(10, label in ('Verdict', 'Coverage score'))
        c.alignment = Alignment(wrap_text=True, vertical='top')
        if fmt:
            c.number_format = fmt
        ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=4)
    top = 7 + len(items) + 2
    ws.cell(row=top - 1, column=1, value='TOP 12 ENTITIES BY IMPORTANCE (from the Entity Map)').font = K.f(10, True, K.DEEP)
    heads = ['Rank', 'Entity', 'Type', 'Tier', 'Importance', 'Our coverage', 'Gap', 'Next action', 'Reference URL', 'Schema property', 'JSON-LD (helper)']
    K.header_row(ws, top, heads, formula_cols=tuple(range(1, 12)))
    cols = {2: 'B', 3: 'C', 4: 'Q', 5: 'P', 6: 'H', 7: 'T', 8: 'U', 9: 'G', 10: 'V', 11: 'AF'}
    for p in range(1, 13):
        rr = top + p
        ws.cell(row=rr, column=1, value=p)
        mm = f'MATCH($B$4&"|"&$A{rr},{em("AC")},0)'
        for c, col in cols.items():
            ws.cell(row=rr, column=c, value=f'=IFERROR(INDEX({em(col)},{mm}),"")' if col == 'P' else f'=IFERROR(INDEX({em(col)},{mm})&"","")')
        for c in range(1, 12):
            cell = ws.cell(row=rr, column=c)
            cell.fill, cell.border, cell.font = K.FORMULA_FILL, K.BORDER, K.f(9)
            cell.alignment = Alignment(wrap_text=c in (2, 8, 9), vertical='top')
    g = f'G{top + 1}:G{top + 12}'
    ws.conditional_formatting.add(g, CellIsRule(operator='equal', formula=['"Critical gap"'], fill=PatternFill('solid', fgColor='F8D7D3'), font=Font(name=K.FONT, bold=True)))
    ws.conditional_formatting.add(g, CellIsRule(operator='equal', formula=['"Covered"'], fill=PatternFill('solid', fgColor='D9F2C4')))
    ws.conditional_formatting.add(g, CellIsRule(operator='equal', formula=['"Partly covered"'], fill=PatternFill('solid', fgColor='FFF4CC')))
    r1, r2 = top + 1, top + 12
    j = top + 14
    ws.cell(row=j, column=1, value='JSON-LD FOR THE PAGE (copy, replace the headline, test it)').font = K.f(10, True, K.DEEP)
    ws.cell(row=j + 1, column=1, value='Headline for the markup').font = K.f(10, True)
    h = ws.cell(row=j + 1, column=2, value='Darjeeling First Flush Tea: Taste, Harvest and How to Brew It')
    h.fill, h.border = K.INPUT_FILL, K.BORDER
    ws.merge_cells(start_row=j + 1, start_column=2, end_row=j + 1, end_column=8)
    about = f'_xlfn.TEXTJOIN(",",TRUE,IF(J{r1}="about",K{r1},""),' + ','.join(f'IF(J{x}="about",K{x},"")' for x in range(r1 + 1, r2 + 1)) + ')'
    ment = f'_xlfn.TEXTJOIN(",",TRUE,' + ','.join(f'IF(J{x}="mentions",K{x},"")' for x in range(r1, r2 + 1)) + ')'
    ws.cell(row=j + 2, column=1, value='JSON-LD').font = K.f(10, True)
    out = ws.cell(row=j + 2, column=2, value=(
        f'=IF($B$4="","",'
        f'"<script type=""application/ld+json"">{{""@context"":""https://schema.org"",""@type"":""Article"",""headline"":"""&SUBSTITUTE(B{j + 1},CHAR(34),"")&""",'
        f'""about"":["&{about}&"],""mentions"":["&{ment}&"]}}</script>")'))
    out.fill, out.border, out.font = K.FORMULA_FILL, K.BORDER, K.f(9)
    out.alignment = Alignment(wrap_text=True, vertical='top')
    ws.merge_cells(start_row=j + 2, start_column=2, end_row=j + 2, end_column=8)
    ws.row_dimensions[j + 2].height = 150
    ws.cell(row=j + 3, column=2, value='about and mentions are schema.org properties, not a Google rich result. Add the other Article properties you use, then check the code with the Schema Markup Validator or the Rich Results Test.').font = K.f(9, False, '777777', True)
    b0 = j + 6
    ws.cell(row=b0 - 1, column=1, value='YOUR BRIEF (type here)').font = K.f(10, True, K.DEEP)
    brief = [
        ('What the page is about, in one sentence', 'Darjeeling first flush tea: what it is, when it is picked, how it tastes and how to brew it.'),
        ('Entities to add or explain', 'Muscatel flavour (own section with tasting notes), Darjeeling as a place (explain the region), spring harvest.'),
        ('Original detail only we can add', 'Our own tasting notes from 6 estates, photos of the dry leaf and the cup, the water temperatures we tested.'),
        ('Questions the page must answer', 'When is first flush picked? How is it different from second flush? Why is it so light? How hot should the water be?'),
        ('Internal links to and from', '/guides/assam-vs-darjeeling/, /shop/darjeeling-tea/'),
        ('Owner and due date', 'Asha, 10 December 2026'),
    ]
    for i, (k, v) in enumerate(brief):
        rr = b0 + i
        ws.cell(row=rr, column=1, value=k).font = K.f(10, True)
        c = ws.cell(row=rr, column=2, value=v)
        c.fill, c.border = K.INPUT_FILL, K.BORDER
        c.alignment = Alignment(wrap_text=True, vertical='top')
        ws.merge_cells(start_row=rr, start_column=2, end_row=rr, end_column=8)
        ws.row_dimensions[rr].height = 32
    return ws, top, j + 2


def dashboard_sheet(wb, brand_first, brand_last):
    ws = wb.create_sheet('Dashboard')
    ws.sheet_view.showGridLines = False
    K.title_block(ws, 'Dashboard', 'Everything here calculates from the other tabs. Nothing to type.')
    for c, w in zip('ABCDEFGH', [44, 12, 3, 30, 10, 30, 3, 3]):
        ws.column_dimensions[c].width = w
    kpis = [
        ('Topics mapped', f'=COUNTA({tp("A")})', '0'),
        ('Entities mapped', f'=COUNTA({em("B")})', '0'),
        ('Main and core entities', f'=COUNTIF({em("Q")},"Main")+COUNTIF({em("Q")},"Core")', '0'),
        ('Critical gaps', f'=COUNTIF({em("T")},"Critical gap")', '0'),
        ('All gaps (critical, gap, partly covered)', f'=COUNTIF({em("T")},"Critical gap")+COUNTIF({em("T")},"Gap")+COUNTIF({em("T")},"Partly covered")', '0'),
        ('Average coverage score', f'=IFERROR(AVERAGE({tp("I")}),0)', '0%'),
        ('Entities that need a reference URL', f'=COUNTIF({em("W")},"Find a reference URL")', '0'),
        ('AI answers checked', f'=COUNTIF({ai("D")},"Yes")', '0'),
        ('Entities named by AI but not in your map', f'=SUM({ai("S")})', '0'),
        ('AI answers that name your brand', f'=IFERROR(COUNTIFS({ai("D")},"Yes",{ai("M")},"Yes")/COUNTIF({ai("D")},"Yes"),0)', '0%'),
        ('Brand entity score', "='Brand Entity Audit'!C4", '0%'),
    ]
    ws['A4'] = 'KEY NUMBERS'
    ws['A4'].font = K.f(10, True, K.DEEP)
    for i, (label, fml, fmt) in enumerate(kpis):
        r = 5 + i
        ws.cell(row=r, column=1, value=label).font = K.f(10)
        c = ws.cell(row=r, column=2, value=fml)
        c.number_format, c.font, c.fill, c.border = fmt, K.f(11, True), K.FORMULA_FILL, K.BORDER
    for j, h in enumerate(['Topic', 'Coverage', 'Verdict']):
        c = ws.cell(row=4, column=4 + j, value=h)
        c.font, c.fill = K.f(10, True, 'FFFFFF'), K.HEAD_F
    for i in range(15):
        r = 5 + i
        kr = TOP_FIRST + i
        ws.cell(row=r, column=4, value=f'=IF({TP}!A{kr}="","",{TP}!A{kr})')
        ws.cell(row=r, column=5, value=f'=IF({TP}!A{kr}="","",IF({TP}!I{kr}="",0,{TP}!I{kr}))')
        ws.cell(row=r, column=6, value=f'=IF({TP}!A{kr}="","",{TP}!P{kr})')
        for cc in (4, 5, 6):
            cell = ws.cell(row=r, column=cc)
            cell.border, cell.font, cell.fill = K.BORDER, K.f(10, cc == 4), K.FORMULA_FILL
        ws.cell(row=r, column=5).number_format = '0%'
    verdict_rules(ws, 'F5:F19', 'F5')
    top = 22
    for j, h in enumerate(['Tier', 'Entities', 'With a gap']):
        c = ws.cell(row=top, column=1 + j, value=h)
        c.font, c.fill = K.f(10, True, 'FFFFFF'), K.HEAD_F
    for i, t in enumerate(['Main', 'Core', 'Supporting', 'Peripheral']):
        r = top + 1 + i
        ws.cell(row=r, column=1, value=t).border = K.BORDER
        c = ws.cell(row=r, column=2, value=f'=COUNTIF({em("Q")},A{r})')
        c.border, c.fill = K.BORDER, K.FORMULA_FILL
        c = ws.cell(row=r, column=3, value=(
            f'=COUNTIFS({em("Q")},A{r},{em("T")},"Critical gap")+COUNTIFS({em("Q")},A{r},{em("T")},"Gap")+COUNTIFS({em("Q")},A{r},{em("T")},"Partly covered")'))
        c.border, c.fill = K.BORDER, K.FORMULA_FILL

    def bar(title, ytitle, cat_col, val_cols, r1, r2, anchor, colors, horiz, titles=False):
        ch = BarChart()
        ch.type = 'bar' if horiz else 'col'
        ch.title = title
        ch.y_axis.title = ytitle
        for vc in val_cols:
            ch.add_data(Reference(ws, min_col=vc, min_row=r1 - (1 if titles else 0), max_row=r2), titles_from_data=titles)
        ch.set_categories(Reference(ws, min_col=cat_col, min_row=r1, max_row=r2))
        if not titles:
            ch.legend = None
        ch.height, ch.width = 7.5, 16
        ch.x_axis.delete = False
        ch.y_axis.delete = False
        ch.title.overlay = False
        ch.y_axis.title.overlay = False
        for s, col in zip(ch.series, colors):
            s.graphicalProperties.solidFill = col
        ws.add_chart(ch, anchor)
        return ch
    c1 = bar('Entity coverage score by topic', 'Coverage', 4, [5], 5, 5 + len(TOPICS) - 1, 'H4', [K.GREEN], True)
    c1.y_axis.scaling.min = 0
    c1.y_axis.scaling.max = 1
    c1.y_axis.numFmt = '0%'
    bar('Entities and gaps by tier', 'Entities', 1, [2, 3], top + 1, top + 4, 'H21', ['2B2B2B', 'E07A5F'], False, titles=True)
    return ws


def build(path, asset, url):
    wb = K.new_book()
    map_sheet(wb)
    topics_sheet(wb)
    ai_sheet(wb)
    _, bf, bl = brand_sheet(wb)
    plan_sheet(wb)
    dashboard_sheet(wb, bf, bl)
    settings_sheet(wb)
    K.prompts_sheet(wb, asset['prompts'], url)
    K.checklist_sheet(wb, list(asset['checklist']))
    K.sources_sheet(wb, asset['sources'], [
        ('Demo data', 'LeafLine Teas is fictional. All counts of results, AI answers, coverage levels, salience scores and audit statuses are illustrative, not real data. Wikipedia links are given only as examples of reference URLs.', ''),
        ('Importance score', 'Weighted mix of the share of top results that mention an entity, the share of AI answers that name it, whether it appears in People also ask or related searches and whether it has a reference URL. Weights and tier bands live on Settings and are assumptions to tune.', ''),
        ('Coverage score', 'Importance weighted share of the coverage each entity needs (Main: own section, Core: explained, Supporting: mentioned). An assumption of this kit, not a Google metric.', ''),
        ('Salience', 'Optional. The Google Cloud Natural Language API returns a salience score from 0 to 1 for each entity in a text. It is a separate Cloud product: Google Search does not say it uses it. Use it only as a second opinion on what your text is mainly about.', ''),
        ('about and mentions', 'schema.org defines about as the subject matter of a work and mentions as a reference that the work is not necessarily about. They are not a Google rich result.', ''),
        ('AI answers', 'AI answers vary by user, location, wording and date. Record what you saw, date it and recheck monthly.', ''),
    ])
    K.start_here(
        wb, 'Entity Research Kit',
        [
            'This workbook maps the entities (people, places, things and ideas) that search engines and AI answers connect to your topic, scores how important each one is, checks how well your page covers it and tells you what to add. It also audits how clearly your own brand and authors are defined, and writes about and mentions JSON-LD for the page.',
            f'It ships with demo data for a fictional tea store (4 topics, {len(E)} entities, {len(AI)} AI answer checks) so you can see every formula working. Clear the yellow demo cells when you are ready.',
        ],
        [
            ('Entity Map', 'One row per entity with 500 ready rows: type, role, how many top results mention it, People also ask, reference URL and your coverage, plus automatic importance, tier, gap, next action, schema property and JSON-LD fragment.'),
            ('Topics', 'One row per topic or page with automatic coverage score, critical gaps, biggest gap, AI brand mentions, verdict and next step.'),
            ('Dashboard', 'Key numbers, coverage and verdict for every topic, and two charts.'),
            ('AI Answer Check', 'The entities each AI answer names, matched against your map, with new entities flagged.'),
            ('Brand Entity Audit', '16 checks for your brand and authors: consistent name, Organization markup, sameAs, author pages, knowledge panel, mentions.'),
            ('Page Plan', 'Pick a topic to see its summary, the top 12 entities, ready JSON-LD and a brief to fill in.'),
            ('Settings', 'Tier bands, verdict bands, importance weights, entity type to schema.org type table and dropdown lists.'),
            ('AI Prompts', 'Prompts for ChatGPT, Claude or Gemini to find, group, check and write about entities.'),
            ('Checklist', 'The full process as a tick list with automatic progress.'),
            ('Sources', 'Where facts come from and which numbers are assumptions.'),
        ],
        [
            'Look at the demo on every tab, the Dashboard and the Page Plan to see how it works, then clear the yellow demo cells.',
            'Add each topic or page on the Topics tab with its main entity and how many top results you checked.',
            'Open the top results for the topic. On the Entity Map, add every entity they keep naming, with type, role and how many results mention it.',
            'Ask the topic in AI Overviews, AI Mode or an assistant and type the entities each answer names on AI Answer Check.',
            'Mark how well your page covers each entity. Read the tier, gap and next action, and the verdict on Topics.',
            'Open Page Plan, write the brief, add the missing entities to the page and paste the JSON-LD after testing it.',
            'Work through the Brand Entity Audit, then recheck important topics every quarter.',
        ],
        url,
    )
    order = ['Start Here', 'Entity Map', 'Topics', 'Dashboard', 'AI Answer Check', 'Brand Entity Audit', 'Page Plan', 'Settings', 'AI Prompts', 'Checklist', 'Sources']
    wb._sheets = [wb[n] for n in order]
    wb.active = 0
    for ws in wb.worksheets:
        ws.sheet_properties.tabColor = K.GREEN if ws.title in ('Start Here', 'Entity Map', 'Topics', 'Dashboard', 'Page Plan') else 'A6EF39'
    wb.save(path)


PREVIEW = {'sheet': 'Entity Map', 'header_row': 4, 'rows': 12, 'cols': [2, 3, 4, 5, 6, 8, 12, 15, 16, 17, 20, 21],
           'formula_idx': [6, 7, 8, 9, 10, 11]}


def check(wb):
    """Assert the worked examples used in the guide."""
    m = wb['Entity Map']
    # Topic 1: darjeeling first flush tea (rows 5 to 16)
    assert m['P5'].value == 100 and m['Q5'].value == 'Main' and m['T5'].value == 'Covered', (m['P5'].value, m['T5'].value)
    assert m['M5'].value == 3, m['M5'].value
    assert m['N7'].value == 3 and abs(m['L7'].value - 0.6) < 1e-9, (m['N7'].value, m['L7'].value)
    assert m['P7'].value == 72 and m['Q7'].value == 'Core' and m['T7'].value == 'Critical gap', (m['P7'].value, m['T7'].value)
    assert m['P6'].value == 90 and m['T6'].value == 'Covered', m['P6'].value
    assert m['P9'].value == 56 and m['Q9'].value == 'Core' and m['T9'].value == 'Partly covered', (m['P9'].value, m['T9'].value)
    assert m['P13'].value == 38 and m['T13'].value == 'Gap', (m['P13'].value, m['T13'].value)
    assert m['P15'].value == 28 and m['Q15'].value == 'Peripheral' and m['T15'].value == 'Optional', m['P15'].value
    assert m['V5'].value == 'about' and m['V6'].value == 'mentions' and not m['V7'].value, (m['V5'].value, m['V7'].value)
    assert m['X5'].value.startswith('Most salient'), m['X5'].value
    assert m['AF5'].value == '{"@type":"Thing","name":"Darjeeling tea","sameAs":"https://en.wikipedia.org/wiki/Darjeeling_tea"}', m['AF5'].value
    t = wb[TP]
    assert t['F5'].value == 12 and t['J5'].value == 1 and t['K5'].value == 3, (t['F5'].value, t['J5'].value, t['K5'].value)
    assert abs(t['I5'].value - 458 / 596) < 1e-9, t['I5'].value
    assert t['O5'].value == 'Muscatel flavour' and t['P5'].value == 'Fill the gaps', (t['O5'].value, t['P5'].value)
    assert abs(t['N5'].value - 1 / 3) < 1e-9, t['N5'].value
    assert t['P6'].value.startswith('Thin') and t['J6'].value == 3 and t['O6'].value == 'Bitterness', (t['I6'].value, t['J6'].value, t['O6'].value)
    assert t['P7'].value == 'Strong entity coverage', (t['I7'].value, t['P7'].value)
    assert t['P8'].value.startswith('Map at least'), t['P8'].value
    assert not m['V38'].value, m['V38'].value
    a = wb['AI Answer Check']
    assert a['P5'].value == 7 and a['Q5'].value == 6 and a['S5'].value == 1, (a['P5'].value, a['Q5'].value)
    assert a['T5'].value.startswith('Add the 1 new'), a['T5'].value
    p = wb['Page Plan']
    assert p['B17'].value == 'Fill the gaps', p['B17'].value
    js = [c.value for row in p.iter_rows() for c in row if isinstance(c.value, str) and c.value.startswith('<script')]
    assert js and '"about":[{"@type":"Thing","name":"Darjeeling tea"' in js[0] and '"mentions":[{' in js[0] and 'Muscatel' not in js[0], js
    b = wb['Brand Entity Audit']
    assert 0.3 < b['C4'].value < 0.7, b['C4'].value
