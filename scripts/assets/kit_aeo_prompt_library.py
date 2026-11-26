"""AEO Prompt Library Kit workbook (asset 19).

Prompt Library: one row per prompt (500 rows) with intent type, funnel stage, persona, where the prompt came from,
business value and the page that should answer it. The sheet spots branded prompts, then rolls up every test run:
runs, engines tested, mention rate, named first rate, cited rate, tone, wrong answers, runs naming a competitor,
the top competitor, a confidence check, a status, the next action, a priority score and a retest date.
Test Log: one row per run of a prompt in one AI engine (1,000 rows). You paste the brands the answer names, in order;
the sheet finds you, your position and each competitor, and checks the row for typing mistakes.
Share of Voice: mention rates by engine and by intent type for you and up to 5 competitors, on unbranded prompts only.
Fix Plan: problems found (wrong facts, absent, negative tone) with the source to fix, hours and a before and after result.
Prompt Builder: 20 editable prompt templates and 6 personas that write prompts from your category, audience and location.
Dashboard sums it all up.
"""
import datetime
from openpyxl.styles import PatternFill, Font, Alignment
from openpyxl.formatting.rule import CellIsRule, ColorScaleRule, FormulaRule
from openpyxl.chart import BarChart, Reference
from openpyxl.utils import get_column_letter as L
import kitlib as K

LB_FIRST, LB_LAST = 5, 504      # Prompt Library (500 rows)
LG_FIRST, LG_LAST = 5, 1004     # Test Log (1,000 rows)
FX_FIRST, FX_LAST = 5, 154      # Fix Plan (150 rows)
S = 'Settings'
LBS, LGS, FXS, PBS, SVS = "'Prompt Library'", "'Test Log'", "'Fix Plan'", "'Prompt Builder'", "'Share of Voice'"

RULES = [
    ('Your brand name', 'CalmDesk', '@'),
    ('Other way people write it (optional)', 'Calm Desk', '@'),
    ('Another name or product (optional)', None, '@'),
    ('Today (set it to the day you review the sheet)', datetime.date(2026, 11, 26), 'dd mmm yyyy'),
    ('Runs needed before you trust a prompt\'s rates', 10, '0'),
    ('Strong: mention rate at least', 0.6, '0%'),
    ('Mentioned sometimes: mention rate at least', 0.2, '0%'),
    ('Test each prompt again after (days)', 30, '0'),
    ('P1: work on it now when the score is at least', 65, '0'),
    ('P2: this month when at least', 45, '0'),
    ('P3: this quarter when at least (below = P4: later)', 25, '0'),
    ('Measure a fix this many days after it is done', 30, '0'),
    ('Fix hours available per week', 8, '0'),
]
(BRAND, ALIAS1, ALIAS2, DATE, MINRUNS, STRONG, SOME, RETEST, P1, P2, P3, MEASURE, HOURS) = (f'{S}!$B${r}' for r in range(5, 5 + len(RULES)))
COMPS = ['HelpHive', 'TicketNest', 'SupportLoop', 'DeskPilot', 'AnswerBay']
COMP = [f'{S}!$E${6 + k}' for k in range(5)]
WEIGHTS = [('Business value', 35), ('Visibility gap (1 minus mention rate)', 30), ('Unbranded prompt', 15), ('Wrong or partly wrong answers', 20)]
W_VAL, W_GAP, W_UNB, W_WRONG = (f'{S}!$E${r}' for r in range(15, 19))
INTENTS = [
    ('Recommendation', 'Asks which product or company to choose. The core test of AI visibility.'),
    ('Comparison', 'Puts brands side by side. Shows how engines describe your strengths.'),
    ('Alternatives', 'Asks for options other than a named brand, yours or a competitor\'s.'),
    ('Problem or how to', 'Describes a problem without naming a product. Tests if you are suggested as the fix.'),
    ('Pricing', 'Asks about cost or free options. Wrong prices are a common error.'),
    ('Brand facts', 'Asks what your brand is, does or costs. Tests accuracy.'),
    ('Reviews and trust', 'Asks whether you are good or safe. Tests tone.'),
    ('Local', 'Adds a city, region or country. Tests local visibility.'),
]
INT_FIRST = 23
FUNNEL = ['Learn', 'Compare', 'Buy', 'Use']
ORIGINS = ['Sales call', 'Support ticket', 'Search Console query', 'Bing grounding query', 'People also ask', 'Reddit or forum', 'Team idea', 'Prompt Builder']
ENGINES = ['ChatGPT', 'Gemini', 'Google AI Mode', 'Google AI Overview', 'Perplexity', 'Microsoft Copilot', 'Claude']
MODES = ['Logged out, fresh chat', 'Logged in, memory off', 'Logged in, memory on', 'Web search on', 'API call']
TONES = ['Positive', 'Neutral', 'Negative', 'Not mentioned']
FACTS = ['Correct', 'Partly wrong', 'Wrong', 'Not mentioned']
PROBLEMS = [
    ('Wrong fact', 3, 'Fix the fact where the engines read it: your own page first, then profiles, listings and old articles that repeat it. Retest the same prompt.'),
    ('Negative tone', 4, 'Find where the complaint comes from (reviews, forums, old articles). Fix the cause, reply in public and publish proof such as numbers or case studies.'),
    ('Absent: competitors win', 8, 'Publish the page that answers this prompt best, with proof, and earn mentions on the sites the engines cite for it.'),
    ('Absent: no brand named', 6, 'Write the clearest answer to this question on your site, with your own data, so engines have a source that names you.'),
    ('Mentioned, not cited', 3, 'Make the page you want cited easy to crawl (OAI-SearchBot, Bingbot, Googlebot) and the most complete answer on the topic.'),
    ('Outdated information', 2, 'Update the facts on your site and profiles, show a visible updated date and remove old pages that repeat the old facts.'),
]
PR_FIRST = 33
FIXSRC = ['Own website page', 'Help docs', 'Google Business Profile', 'Bing Places', 'Review sites', 'Wikipedia or Wikidata', 'Industry directories',
          'Press and partner sites', 'Comparison and list articles', 'Reddit or forums']
OWNERS = ['Ravi (content)', 'Neha (PR)', 'SEO', 'Developer', 'Support lead']
WEEKS = [f'Week {i}' for i in range(1, 9)]
ASTAT = ['To do', 'Doing', 'Done']
STATUSES = [
    ('Paused', 'Not active. Switch Active? to Yes to test it again.'),
    ('Not tested yet', 'Run it in each engine you track, in a fresh chat, and log every run on the Test Log.'),
    ('Too few runs: test more', 'AI answers change from run to run. Log more runs before you trust the rates.'),
    ('Wrong facts: fix the source', 'At least one answer gets your facts wrong. Add a row on the Fix Plan and fix the source first.'),
    ('Branded: negative tone', 'Answers about you lean negative. Find the source of the complaints and publish proof.'),
    ('Branded: accurate, protect it', 'Answers about you are accurate. Keep your pages and profiles current and retest monthly.'),
    ('Strong: protect it', 'You are named in most runs. Keep the target page fresh and watch for new competitors.'),
    ('Mentioned sometimes: build proof', 'You appear in some runs. Strengthen the target page and earn mentions on the sources the engines cite.'),
    ('Absent: competitors win', 'Competitors are named, you are not. Study which sources the engines cite and get on them.'),
    ('Absent: no brand named', 'No brand wins this prompt yet. Publish the clearest answer on the topic so you become the source.'),
]
ST_FIRST = 46
ST_RNG = f'{S}!$D${ST_FIRST}:$E${ST_FIRST + len(STATUSES) - 1}'

# Demo: CalmDesk, a fictional help desk app for small teams in India (calmdesk.example). Competitors are fictional too.
U = 'https://calmdesk.example'
PERSONAS = [
    ('Founder', 'I run a 6 person software startup and answer support myself.'),
    ('Support lead', 'I lead a support team of 4 at an online store.'),
    ('Ops manager', 'I manage operations for a 20 person company in Pune.'),
    ('Shop owner', 'I sell handmade products online and answer customer messages on WhatsApp.'),
    ('Agency owner', 'I run a small digital agency and look after support for 10 clients.'),
    ('IT admin', 'I look after software for a 50 person firm and need tools with single sign on.'),
]
# id, prompt, topic, intent, funnel, persona, origin, value, target page, active, notes
PROMPTS = [
    ('P01', 'What is the best help desk software for small teams?', 'Help desk software', 'Recommendation', 'Compare', 'Founder', 'Sales call', 3, '/', 'Yes', 'Worked example in the guide'),
    ('P02', 'Recommend 5 help desk tools for a small business in India.', 'Help desk software', 'Recommendation', 'Compare', 'Ops manager', 'Team idea', 3, '/in/', 'Yes', ''),
    ('P03', 'Which help desk software is easiest to set up for a small team?', 'Setup', 'Recommendation', 'Compare', 'Founder', 'Support ticket', 3, '/features/setup/', 'Yes', ''),
    ('P04', 'What are the best alternatives to HelpHive?', 'Alternatives', 'Alternatives', 'Compare', 'Support lead', 'Search Console query', 3, '/compare/helphive-alternatives/', 'Yes', ''),
    ('P05', 'Compare the top shared inbox tools for customer support by email.', 'Shared inbox', 'Comparison', 'Compare', 'Support lead', 'People also ask', 2, '/compare/shared-inbox-tools/', 'Yes', ''),
    ('P06', 'How can a small team manage customer support emails better?', 'Support email', 'Problem or how to', 'Learn', 'Founder', 'Reddit or forum', 2, '/guides/manage-support-emails/', 'Yes', ''),
    ('P07', 'How much does help desk software cost for a small team?', 'Pricing', 'Pricing', 'Compare', 'Founder', 'Sales call', 3, '/pricing/', 'Yes', ''),
    ('P08', 'Is there a free help desk for small teams?', 'Pricing', 'Pricing', 'Learn', 'Founder', 'Search Console query', 2, '/pricing/', 'Yes', ''),
    ('P09', 'What is CalmDesk?', 'Brand', 'Brand facts', 'Learn', 'Founder', 'Team idea', 2, '/about/', 'Yes', ''),
    ('P10', 'How much does CalmDesk cost?', 'Brand', 'Brand facts', 'Buy', 'Ops manager', 'Sales call', 3, '/pricing/', 'Yes', 'Old price still in an FAQ'),
    ('P11', 'Is CalmDesk good? What do users say?', 'Brand', 'Reviews and trust', 'Buy', 'Support lead', 'Team idea', 3, '/customers/', 'Yes', ''),
    ('P12', 'CalmDesk vs HelpHive: which is better for email support?', 'Brand', 'Comparison', 'Buy', 'Support lead', 'Sales call', 3, '/compare/calmdesk-vs-helphive/', 'Yes', ''),
    ('P13', 'Best help desk software companies in India', 'Help desk software', 'Local', 'Compare', 'Ops manager', 'Team idea', 2, '/in/', 'Yes', ''),
    ('P14', 'Which help desk has WhatsApp support built in?', 'WhatsApp', 'Recommendation', 'Compare', 'Shop owner', 'Support ticket', 3, '/features/whatsapp/', 'Yes', ''),
    ('P15', 'What tools help an online shop answer customer questions faster?', 'Online shops', 'Problem or how to', 'Learn', 'Shop owner', 'Reddit or forum', 2, '/guides/online-shop-support/', 'Yes', ''),
    ('P16', 'How do I set up a customer support knowledge base?', 'Knowledge base', 'Problem or how to', 'Learn', 'Support lead', 'People also ask', 1, '/guides/knowledge-base/', 'Yes', ''),
    ('P17', 'What are good alternatives to CalmDesk?', 'Brand', 'Alternatives', 'Use', 'Support lead', 'Team idea', 2, '/compare/', 'Yes', ''),
    ('P18', 'Which help desk software works best with Shopify?', 'Integrations', 'Recommendation', 'Compare', 'Shop owner', 'Sales call', 3, '/integrations/shopify/', 'Yes', ''),
    ('P19', 'Best ticketing system for a 3 person startup', 'Help desk software', 'Recommendation', 'Compare', 'Founder', 'Team idea', 2, '/', 'No', 'Paused: too close to P01'),
    ('P20', 'What is a shared inbox?', 'Shared inbox', 'Problem or how to', 'Learn', 'Support lead', 'People also ask', 1, '/guides/shared-inbox/', 'Yes', ''),
]
TEST_ENGINES = ['ChatGPT', 'Gemini', 'Perplexity', 'Google AI Mode']
RUN_DATES = ['2026-11-02', '2026-11-09', '2026-11-16']
# per prompt id: run pattern per test engine (3 runs), competitor indices that appear.
# C = named and your URL cited (positive), M = named (neutral), X = named, negative tone, W = named with a wrong fact,
# P = named with a partly wrong fact, N = not named.
RUNS = {
    'P01': (['MCN', 'NMN', 'CNM', 'NNM'], [0, 1, 2, 3]),
    'P02': (['NNN', 'NNM', 'MNN', 'NNN'], [0, 1, 4]),
    'P03': (['CMC', 'MMC', 'CCC', 'MCM'], [1, 2]),
    'P04': (['MNM', 'NNN', 'CMN', 'NNN'], [1, 2, 3, 4]),
    'P05': (['NNN', 'NNN', 'NMN', 'NNN'], [0, 2]),
    'P06': (['NNN', 'NNN', 'NNN', 'NNN'], [2]),
    'P07': (['MNM', 'NNM', 'MMN', 'NNN'], [0, 1, 3]),
    'P08': (['NNN', 'NMN', 'NNN', 'NNN'], [0, 4]),
    'P09': (['MMM', 'CMM', 'CMM', 'MMM'], []),
    'P10': (['WMW', 'WWM', 'CMM', 'MWM'], []),
    'P11': (['XMM', 'XXM', 'MCM', 'XMM'], []),
    'P12': (['CMM', 'MMM', 'CCM', 'MCM'], [0]),
    'P13': (['MNN', 'NNN', 'MMN', 'NMN'], [0, 1, 2, 4]),
    'P14': (['CCM', 'MCC', 'CCC', 'CMC'], [3]),
    'P15': (['NMN', 'NNN', 'NNM', 'NNN'], [0, 1]),
    'P16': (['NNN', 'NNN', 'NNN', 'NNN'], []),
    'P20': (['NNN', 'NNN', 'NNN', 'NNN'], []),
}
EXTRA_RUNS = [('2026-11-23', 'P17', 'ChatGPT', 'M', [0, 1, 3], 0), ('2026-11-23', 'P17', 'ChatGPT', 'M', [0, 1, 3], 1), ('2026-11-23', 'P17', 'ChatGPT', 'N', [0, 1, 3], 2)]
WRONG = {'W': 'Quotes the old price of 499 rupees per agent a month (it is 699 since April 2026)',
         'P': 'Says there is no free plan (there is a free plan for 2 agents)'}
# prompt id, problem, what the AI said, correct fact or goal, source to fix, owner, week, status, done on, before, after, wrong after
FIXES = [
    ('P10', 'Wrong fact', 'Old price of 499 rupees per agent a month', '699 rupees per agent a month since April 2026, free plan for 2 agents',
     'Own website page', 'Ravi (content)', 'Week 1', 'Done', '2026-11-12', None, None, None),
    ('P11', 'Negative tone', 'Setup is slow and support replies late', 'Show the 15 minute setup and the median first reply time, with customer quotes',
     'Review sites', 'Neha (PR)', 'Week 2', 'Doing', None, None, None, None),
    ('P02', 'Absent: competitors win', 'Lists HelpHive, TicketNest and AnswerBay', 'Be named in India focused lists of help desk tools',
     'Comparison and list articles', 'Neha (PR)', 'Week 2', 'To do', None, None, None, None),
    ('P05', 'Absent: competitors win', 'Lists HelpHive and SupportLoop', 'Publish an honest shared inbox comparison with real setup times',
     'Own website page', 'Ravi (content)', 'Week 3', 'To do', None, None, None, None),
    ('P13', 'Absent: competitors win', 'Lists four other companies', 'Appear in India company lists and directories',
     'Industry directories', 'Neha (PR)', None, 'Done', '2026-10-12', 0.08, 0.33, None),
    ('P07', 'Outdated information', 'Gives 2024 price ranges', 'Current price ranges with a visible updated date',
     'Own website page', 'Ravi (content)', None, 'Done', '2026-10-20', 0.25, 0.42, None),
]

LB_IN = ['Prompt ID', 'Prompt', 'Topic', 'Intent type', 'Funnel stage', 'Persona', 'Where the prompt came from', 'Business value (1 to 3)',
         'Target page', 'Active?', 'Notes']
LB_FH = ['Branded?', 'Runs', 'Engines tested', 'Runs that name you', 'Mention rate', 'Named first rate', 'Cited rate', 'Tone (-1 to 1)',
         'Wrong or partly wrong answers', 'Runs naming a competitor', 'Top competitor', 'Confidence', 'Last tested', 'Status', 'Next action',
         'Priority score (0 to 100)', 'Priority', 'Days since tested', 'Test again?', 'Rank (helper)']
LB_HID = [f'Competitor {k + 1} runs' for k in range(5)]
LB_HEAD = LB_IN + LB_FH + LB_HID
BC = {h: L(i + 1) for i, h in enumerate(LB_HEAD)}
LB_F = tuple(range(len(LB_IN) + 1, len(LB_HEAD) + 1))

LG_IN = ['Date', 'Prompt ID', 'Engine', 'Mode', 'Brands named in the answer (in order, commas)', 'Your URL cited?', 'Cited URL or source',
         'Tone about you', 'Facts about you', 'What it got wrong', 'Notes']
LG_FH = ['Prompt', 'Intent type', 'Branded prompt?', 'You named?', 'Your position', 'Brands named'] + \
        [f'Competitor {k + 1} named' for k in range(5)] + ['Competitors named', 'Run number', 'Data check']
LG_HEAD = LG_IN + LG_FH
GC = {h: L(i + 1) for i, h in enumerate(LG_HEAD)}
LG_F = tuple(range(len(LG_IN) + 1, len(LG_HEAD) + 1))
CF = [GC[f'Competitor {k + 1} named'] for k in range(5)]


def lg(h):
    c = GC.get(h, h)
    return f'{LGS}!${c}${LG_FIRST}:${c}${LG_LAST}'


def lb(h):
    c = BC.get(h, h)
    return f'{LBS}!${c}${LB_FIRST}:${c}${LB_LAST}'


def d(s):
    return datetime.date.fromisoformat(s) if s else None


def named(text):
    """Excel test: is your brand (or an alias) in text?"""
    return (f'OR(ISNUMBER(SEARCH({BRAND},{text})),AND({ALIAS1}<>"",ISNUMBER(SEARCH({ALIAS1},{text}))),'
            f'AND({ALIAS2}<>"",ISNUMBER(SEARCH({ALIAS2},{text}))))')


def settings_sheet(wb):
    ws = wb.create_sheet(S)
    ws.sheet_view.showGridLines = False
    K.title_block(ws, 'Settings', 'Your brand, competitors, rules, weights and lists. Change a blue value and every rate, status and priority updates.')
    for c, w in zip('ABCDEFGHIJKLMNOPQRS', [50, 18, 3, 40, 16, 70, 3, 18, 14, 22, 22, 20, 14, 26, 12, 10, 3, 3, 3]):
        ws.column_dimensions[c].width = w
    ws['A4'] = 'YOUR BRAND AND RULES'
    ws['A4'].font = K.f(10, True, K.DEEP)
    for i, (label, val, fmt) in enumerate(RULES):
        r = 5 + i
        ws.cell(row=r, column=1, value=label).font = K.f(10)
        c = ws.cell(row=r, column=2, value=val)
        c.border, c.fill, c.font, c.number_format = K.BORDER, K.INPUT_FILL, K.f(10, True, '0000FF'), fmt
    ws['A20'] = ('Mention rate = runs that name you / all runs of the prompt. Priority score = value weight x value / 3 + gap weight x '
                 '(1 minus mention rate) + unbranded weight x (1 for unbranded, 0.3 for branded) + wrong answer weight x (1 if any answer '
                 'was wrong). AI answers vary from run to run, so the kit reports how often you are named across many runs instead of a '
                 'rank. The run minimum, thresholds, weights and hours on this tab are assumptions of this kit for you to tune.')
    ws['A20'].font = K.f(9, False, '777777', True)
    ws['A20'].alignment = Alignment(wrap_text=True, vertical='top')
    ws.merge_cells('A20:B32')

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
    table(4, 5, 'COMPETITORS (up to 5, as AI answers write them)', ['#', 'Competitor'], [(f'Competitor {k + 1}', n) for k, n in enumerate(COMPS)], blue=(1,))
    table(4, 14, 'PRIORITY WEIGHTS (add up to 100)', ['Factor', 'Weight'], WEIGHTS)
    ws['D19'] = 'Total'
    ws['E19'] = '=SUM(E15:E18)'
    ws['E19'].fill, ws['E19'].font = K.FORMULA_FILL, K.f(10, True)
    table(4, INT_FIRST - 1, 'INTENT TYPES', ['Intent type', 'What it tests'], INTENTS, blue=())
    for i in range(len(INTENTS)):
        ws.merge_cells(start_row=INT_FIRST + i, start_column=5, end_row=INT_FIRST + i, end_column=6)
    table(4, PR_FIRST - 1, 'PROBLEMS, HOURS (assumptions) AND THE FIX', ['Problem', 'Hours', 'Suggested fix'], PROBLEMS, ['@', '0', '@'])
    table(4, ST_FIRST - 1, 'STATUS AND NEXT ACTION (prompt level)', ['Status', 'Next action'], STATUSES, blue=())
    for i in range(len(STATUSES)):
        ws.merge_cells(start_row=ST_FIRST + i, start_column=5, end_row=ST_FIRST + i, end_column=6)
    for r in list(range(INT_FIRST, INT_FIRST + 8)) + list(range(PR_FIRST, PR_FIRST + 6)) + list(range(ST_FIRST, ST_FIRST + len(STATUSES))):
        ws.row_dimensions[r].height = 30
    lists = [('H', 'Engine', ENGINES), ('I', 'Funnel stage', FUNNEL), ('J', 'Where it came from', ORIGINS), ('K', 'Mode', MODES),
             ('L', 'Tone about you', TONES), ('M', 'Facts about you', FACTS), ('N', 'Source to fix', FIXSRC), ('O', 'Owner', OWNERS), ('P', 'Week', WEEKS)]
    ws['H4'] = 'LISTS (used by the dropdowns)'
    ws['H4'].font = K.f(10, True, K.DEEP)
    for col, head, vals in lists:
        ws[f'{col}5'] = head
        ws[f'{col}5'].font = K.f(9, True, '555555')
        n = {'H': 10, 'O': 12}.get(col, len(vals))
        for i in range(n):
            c = ws[f'{col}{6 + i}']
            c.value = vals[i] if i < len(vals) else None
            c.fill, c.border, c.font = K.INPUT_FILL, K.BORDER, K.f(10)
    ws['H18'] = 'Action status'
    ws['H18'].font = K.f(9, True, '555555')
    for i, v in enumerate(ASTAT):
        c = ws[f'H{19 + i}']
        c.value, c.fill, c.border, c.font = v, K.INPUT_FILL, K.BORDER, K.f(10)
    return ws


def log_sheet(wb):
    ws = wb.create_sheet('Test Log')
    ws.sheet_view.showGridLines = False
    n_runs = sum(len(p) * 3 for p, _ in RUNS.values()) + len(EXTRA_RUNS)
    K.title_block(ws, 'Test log', f'One row per run of a prompt in one AI engine. Rows 5 to {4 + n_runs} are DEMO runs for CalmDesk, a fictional help desk app (illustrative). 1,000 rows ready.')
    ws['A2'].font = K.f(10, True, 'B45309')
    ws['A3'] = ('Use a fresh chat for every run. Paste the brands the answer names, in the order it names them, separated by commas. '
                'The grey columns find your brand, your position and each competitor by themselves.')
    ws['A3'].font = K.f(9, False, '666666', True)
    widths = [11, 9, 16, 20, 46, 10, 34, 12, 12, 34, 18, 40, 16, 11, 9, 9, 9] + [9] * 5 + [10, 8, 30]
    K.header_row(ws, 4, LG_HEAD, formula_cols=LG_F, widths=widths)
    rows = []
    for pid, (pats, comps) in RUNS.items():
        for ei, pat in enumerate(pats):
            for k, ch in enumerate(pat):
                rows.append((RUN_DATES[k], pid, TEST_ENGINES[ei], ch, comps, k + ei))
    rows.sort(key=lambda x: (x[0], x[1], TEST_ENGINES.index(x[2])))
    rows += EXTRA_RUNS
    pmap = {p[0]: p for p in PROMPTS}
    c = GC
    for r in range(LG_FIRST, LG_LAST + 1):
        i = r - LG_FIRST
        if i < len(rows):
            dt, pid, eng, ch, comps, rot = rows[i]
            names = [COMPS[k] for k in comps]
            if names:
                s = rot % len(names)
                names = names[s:] + names[:s]
                drop = (rot * 2 + len(pid)) % (len(names) + 2)
                if len(names) > 1 and drop < len(names):
                    names.pop(drop)
            if ch != 'N':
                names.insert(rot % (len(names) + 1), 'CalmDesk')
            cited = 'Yes' if ch == 'C' else 'No'
            url = U + pmap[pid][8] if ch == 'C' else None
            tone = {'C': 'Positive', 'M': 'Neutral', 'X': 'Negative', 'W': 'Neutral', 'P': 'Neutral', 'N': 'Not mentioned'}[ch]
            fact = {'W': 'Wrong', 'P': 'Partly wrong', 'N': 'Not mentioned'}.get(ch, 'Correct')
            vals = [d(dt), pid, eng, 'Logged out, fresh chat', ', '.join(names) or None, cited, url, tone, fact, WRONG.get(ch)]
            for col, v in enumerate(vals, 1):
                if v not in (None, ''):
                    ws.cell(row=r, column=col, value=v)
        e = f'B{r}=""'
        g = lambda h: f'{c[h]}{r}'
        m = f'MATCH(B{r},{lb("A")},0)'
        f = {}
        f['Prompt'] = f'=IF({e},"",IFERROR(INDEX({lb("B")},{m}),"Prompt ID not in the library"))'
        f['Intent type'] = f'=IF({e},"",IFERROR(INDEX({lb("D")},{m})&"",""))'
        f['Branded prompt?'] = f'=IF({e},"",IFERROR(INDEX({lb("Branded?")},{m}),""))'
        f['You named?'] = f'=IF({e},"",IF({named(f"E{r}")},"Yes","No"))'
        pos = (f'MIN(IFERROR(SEARCH({BRAND},E{r}),99999),IF({ALIAS1}="",99999,IFERROR(SEARCH({ALIAS1},E{r}),99999)),'
               f'IF({ALIAS2}="",99999,IFERROR(SEARCH({ALIAS2},E{r}),99999)))')
        f['Your position'] = f'=IF(OR({e},{g("You named?")}<>"Yes"),"",LEN(LEFT(E{r},{pos}))-LEN(SUBSTITUTE(LEFT(E{r},{pos}),",",""))+1)'
        f['Brands named'] = f'=IF({e},"",IF(TRIM(E{r})="",0,LEN(E{r})-LEN(SUBSTITUTE(E{r},",",""))+1))'
        for k in range(5):
            f[f'Competitor {k + 1} named'] = f'=IF({e},"",IF({COMP[k]}="",0,IF(ISNUMBER(SEARCH({COMP[k]},E{r})),1,0)))'
        f['Competitors named'] = f'=IF({e},"",SUM({CF[0]}{r}:{CF[-1]}{r}))'
        f['Run number'] = f'=IF({e},"",COUNTIFS($B${LG_FIRST}:B{r},B{r},$C${LG_FIRST}:C{r},C{r}))'
        yn = g('You named?')
        f['Data check'] = (f'=IF({e},"",IF(C{r}="","Choose the engine",IF(AND({yn}="Yes",H{r}="Not mentioned"),"You are named: set the tone",'
                           f'IF(AND({yn}="No",H{r}<>"Not mentioned",H{r}<>""),"You are not named: tone should be Not mentioned",'
                           f'IF(AND(F{r}="Yes",{yn}="No"),"Cited but not named: check the answer",IF(AND(OR(I{r}="Wrong",I{r}="Partly wrong"),J{r}=""),"Note what it got wrong","OK"))))))')
        for h, v in f.items():
            ws[f'{c[h]}{r}'] = v
    idx = lambda h: LG_HEAD.index(h) + 1
    K.style_body(ws, LG_FIRST, LG_LAST, len(LG_HEAD), formula_cols=LG_F, number_formats={1: 'dd mmm yyyy', idx('Your position'): '0', idx('Brands named'): '0'},
                 wrap_cols=(5, 7, 10, 11, idx('Prompt'), idx('Data check')))
    K.dropdown(ws, f'B{LG_FIRST}:B{LG_LAST}', lb('A'), 'Prompt IDs from the Prompt Library.')
    K.dropdown(ws, f'C{LG_FIRST}:C{LG_LAST}', f'{S}!$H$6:$H$15')
    K.dropdown(ws, f'D{LG_FIRST}:D{LG_LAST}', f'{S}!$K$6:$K$10')
    K.dropdown(ws, f'F{LG_FIRST}:F{LG_LAST}', '"Yes,No"', 'Yes when the answer links to one of your pages.')
    K.dropdown(ws, f'H{LG_FIRST}:H{LG_LAST}', f'{S}!$L$6:$L$9')
    K.dropdown(ws, f'I{LG_FIRST}:I{LG_LAST}', f'{S}!$M$6:$M$9')
    yc = c['You named?']
    ws.conditional_formatting.add(f'{yc}{LG_FIRST}:{yc}{LG_LAST}', CellIsRule(operator='equal', formula=['"Yes"'], fill=PatternFill('solid', fgColor='D9F2C4'), font=Font(name=K.FONT, bold=True, color='3D7F12')))
    ws.conditional_formatting.add(f'I{LG_FIRST}:I{LG_LAST}', FormulaRule(formula=[f'OR(I{LG_FIRST}="Wrong",I{LG_FIRST}="Partly wrong")'], fill=PatternFill('solid', fgColor='F8D7D3'), font=Font(name=K.FONT, bold=True, color='9B2C1F')))
    ws.conditional_formatting.add(f'H{LG_FIRST}:H{LG_LAST}', CellIsRule(operator='equal', formula=['"Negative"'], fill=PatternFill('solid', fgColor='FCE5CD'), font=Font(name=K.FONT, bold=True)))
    dc = c['Data check']
    ws.conditional_formatting.add(f'{dc}{LG_FIRST}:{dc}{LG_LAST}', FormulaRule(formula=[f'AND({dc}{LG_FIRST}<>"",{dc}{LG_FIRST}<>"OK")'], font=Font(name=K.FONT, bold=True, color='9B2C1F')))
    for cf in CF:
        ws.conditional_formatting.add(f'{cf}{LG_FIRST}:{cf}{LG_LAST}', CellIsRule(operator='equal', formula=['1'], fill=PatternFill('solid', fgColor='EEEEEE')))
    ws.freeze_panes = 'C5'
    ws.auto_filter.ref = f'A4:{L(len(LG_HEAD))}{LG_LAST}'
    return ws, rows


def library_sheet(wb):
    ws = wb.create_sheet('Prompt Library')
    ws.sheet_view.showGridLines = False
    K.title_block(ws, 'Prompt library', f'One row per prompt a real customer might ask an AI assistant. Rows 5 to {4 + len(PROMPTS)} are DEMO prompts for CalmDesk, a fictional help desk app (illustrative). 500 rows ready.')
    ws['A2'].font = K.f(10, True, 'B45309')
    ws['A3'] = ('Give every prompt a short ID (P01, P02 ...) and log each run on the Test Log. Mix branded and unbranded prompts, every intent '
                'type and every funnel stage. The grey columns roll up all runs of the prompt.')
    ws['A3'].font = K.f(9, False, '666666', True)
    widths = [8, 44, 16, 16, 9, 13, 16, 9, 30, 7, 22, 10, 7, 8, 8, 9, 9, 8, 8, 9, 9, 12, 16, 11, 30, 46, 10, 14, 8, 12, 8] + [6] * 5
    K.header_row(ws, 4, LB_HEAD, formula_cols=LB_F, widths=widths)
    c = BC
    for r in range(LB_FIRST, LB_LAST + 1):
        i = r - LB_FIRST
        if i < len(PROMPTS):
            p = PROMPTS[i]
            for col, v in enumerate(p, 1):
                if col == 9 and v:
                    v = U + v
                if v not in (None, ''):
                    ws.cell(row=r, column=col, value=v)
        e = f'A{r}=""'
        g = lambda h: f'{c[h]}{r}'
        ids = lg('B')
        f = {}
        f['Branded?'] = f'=IF({e},"",IF({named(f"B{r}")},"Branded","Unbranded"))'
        f['Runs'] = f'=IF({e},"",COUNTIF({ids},A{r}))'
        f['Engines tested'] = '=IF({},"",{})'.format(e, '+'.join(f'IF(COUNTIFS({ids},A{r},{lg("C")},{S}!$H${6 + k})>0,1,0)' for k in range(len(ENGINES))))
        f['Runs that name you'] = f'=IF({e},"",COUNTIFS({ids},A{r},{lg("You named?")},"Yes"))'
        runs = g('Runs')
        f['Mention rate'] = f'=IF(OR({e},N({runs})=0),"",{g("Runs that name you")}/{runs})'
        f['Named first rate'] = f'=IF(OR({e},N({runs})=0),"",COUNTIFS({ids},A{r},{lg("Your position")},1)/{runs})'
        f['Cited rate'] = f'=IF(OR({e},N({runs})=0),"",COUNTIFS({ids},A{r},{lg("F")},"Yes")/{runs})'
        yes = g('Runs that name you')
        f['Tone (-1 to 1)'] = f'=IF(OR({e},N({yes})=0),"",(COUNTIFS({ids},A{r},{lg("H")},"Positive")-COUNTIFS({ids},A{r},{lg("H")},"Negative"))/{yes})'
        f['Wrong or partly wrong answers'] = f'=IF({e},"",COUNTIFS({ids},A{r},{lg("I")},"Wrong")+COUNTIFS({ids},A{r},{lg("I")},"Partly wrong"))'
        f['Runs naming a competitor'] = f'=IF({e},"",COUNTIFS({ids},A{r},{lg("Competitors named")},">0"))'
        for k in range(5):
            f[LB_HID[k]] = f'=IF({e},"",SUMIF({ids},A{r},{lg(CF[k])}))'
        hr = f'{c[LB_HID[0]]}{r}:{c[LB_HID[-1]]}{r}'
        f['Top competitor'] = f'=IF({e},"",IF(MAX({hr})=0,"None named",INDEX({S}!$E$6:$E$10,MATCH(MAX({hr}),{hr},0))))'
        f['Confidence'] = f'=IF({e},"",IF(N({runs})>={MINRUNS},"Enough runs","Need "&({MINRUNS}-N({runs}))&" more"))'
        f['Last tested'] = f'=IF(OR({e},N({runs})=0),"",_xlfn.MAXIFS({lg("A")},{ids},A{r}))'
        mr, wr, br = g('Mention rate'), g('Wrong or partly wrong answers'), g('Branded?')
        f['Status'] = (f'=IF({e},"",IF(J{r}="No","Paused",IF(N({runs})=0,"Not tested yet",IF({runs}<{MINRUNS},"Too few runs: test more",'
                       f'IF({wr}>0,"Wrong facts: fix the source",IF({br}="Branded",IF(N({g("Tone (-1 to 1)")})<0,"Branded: negative tone","Branded: accurate, protect it"),'
                       f'IF({mr}>={STRONG},"Strong: protect it",IF({mr}>={SOME},"Mentioned sometimes: build proof",'
                       f'IF(N({g("Runs naming a competitor")})>0,"Absent: competitors win","Absent: no brand named")))))))))')
        stv = g('Status')
        f['Next action'] = f'=IF({e},"",IFERROR(VLOOKUP({stv},{ST_RNG},2,FALSE),""))'
        f['Priority score (0 to 100)'] = (f'=IF({e},"",ROUND({W_VAL}*IF(H{r}="",2,H{r})/3+{W_GAP}*(1-N({mr}))+{W_UNB}*IF({br}="Unbranded",1,0.3)'
                                          f'+{W_WRONG}*IF(N({wr})>0,1,0),0))')
        ps = g('Priority score (0 to 100)')
        f['Priority'] = (f'=IF({e},"",IF({stv}="Paused","Paused",IF(LEFT({stv},5)="Wrong","P1: fix facts",IF(OR({stv}="Not tested yet",LEFT({stv},3)="Too"),"Test first",'
                         f'IF(OR(LEFT({stv},6)="Strong",{stv}="Branded: accurate, protect it"),"Protect",'
                         f'IF({ps}>={P1},"P1: now",IF({ps}>={P2},"P2: this month",IF({ps}>={P3},"P3: this quarter","P4: later"))))))))')
        lt = g('Last tested')
        f['Days since tested'] = f'=IF(OR({e},{lt}=""),"",{DATE}-{lt})'
        ds = g('Days since tested')
        f['Test again?'] = f'=IF({e},"",IF(J{r}="No","No: paused",IF({lt}="","Yes: never tested",IF({ds}>={RETEST},"Yes","In "&({RETEST}-{ds})&" days"))))'
        pv = g('Priority')
        f['Rank (helper)'] = (f'=IF(OR({e},{pv}="Protect",{pv}="Paused",{pv}="Test first"),"",IF({pv}="P1: fix facts",100,0)+{ps}-ROW()/100000)')
        for h, v in f.items():
            ws[f'{c[h]}{r}'] = v
    idx = lambda h: LB_HEAD.index(h) + 1
    nf = {idx('Runs'): '0', idx('Engines tested'): '0', idx('Mention rate'): '0%', idx('Named first rate'): '0%', idx('Cited rate'): '0%',
          idx('Tone (-1 to 1)'): '0.00', idx('Last tested'): 'dd mmm yyyy', idx('Priority score (0 to 100)'): '0', idx('Days since tested'): '0',
          idx('Rank (helper)'): '0.00000'}
    K.style_body(ws, LB_FIRST, LB_LAST, len(LB_HEAD), formula_cols=LB_F, number_formats=nf, wrap_cols=(2, 9, 11, idx('Status'), idx('Next action')))
    K.dropdown(ws, f'D{LB_FIRST}:D{LB_LAST}', f'{S}!$D${INT_FIRST}:$D${INT_FIRST + 7}')
    K.dropdown(ws, f'E{LB_FIRST}:E{LB_LAST}', f'{S}!$I$6:$I$9')
    K.dropdown(ws, f'F{LB_FIRST}:F{LB_LAST}', f'{PBS}!$B$38:$B$43', 'Personas from the Prompt Builder tab.')
    K.dropdown(ws, f'G{LB_FIRST}:G{LB_LAST}', f'{S}!$J$6:$J$13')
    K.dropdown(ws, f'H{LB_FIRST}:H{LB_LAST}', '"1,2,3"', '3 close to a sale or lead, 2 builds trust, 1 loosely related.')
    K.dropdown(ws, f'J{LB_FIRST}:J{LB_LAST}', '"Yes,No"')
    mc = c['Mention rate']
    ws.conditional_formatting.add(f'{mc}{LB_FIRST}:{mc}{LB_LAST}', ColorScaleRule(start_type='num', start_value=0, start_color='F8D7D3', mid_type='num', mid_value=0.3, mid_color='FFF4CC', end_type='num', end_value=1, end_color='8BC34A'))
    sc = c['Status']
    for start, fill, fc in (('Wro', '9B2C1F', 'FFFFFF'), ('Str', 'B7E4A0', '1F1F1F'), ('Bra', 'EEF8E6', '3D7F12'), ('Men', 'FFF4CC', '1F1F1F'),
                            ('Abs', 'F8D7D3', '9B2C1F'), ('Too', 'FCE5CD', '1F1F1F'), ('Not', 'FCE5CD', '1F1F1F'), ('Pau', 'EEEEEE', '555555')):
        ws.conditional_formatting.add(f'{sc}{LB_FIRST}:{sc}{LB_LAST}', FormulaRule(formula=[f'LEFT({sc}{LB_FIRST},3)="{start}"'], fill=PatternFill('solid', fgColor=fill), font=Font(name=K.FONT, bold=True, color=fc)))
    ws.conditional_formatting.add(f'{sc}{LB_FIRST}:{sc}{LB_LAST}', CellIsRule(operator='equal', formula=['"Branded: negative tone"'], fill=PatternFill('solid', fgColor='F8D7D3'), font=Font(name=K.FONT, bold=True, color='9B2C1F')))
    pc = c['Priority']
    for start, fill, fc in (('P1', '9B2C1F', 'FFFFFF'), ('P2', 'F8D7D3', '9B2C1F'), ('P3', 'FFF4CC', '1F1F1F'), ('P4', 'EEEEEE', '555555'),
                            ('Pr', 'B7E4A0', '1F1F1F'), ('Te', 'FCE5CD', '1F1F1F')):
        ws.conditional_formatting.add(f'{pc}{LB_FIRST}:{pc}{LB_LAST}', FormulaRule(formula=[f'LEFT({pc}{LB_FIRST},2)="{start}"'], fill=PatternFill('solid', fgColor=fill), font=Font(name=K.FONT, bold=True, color=fc)))
    cc = c['Confidence']
    ws.conditional_formatting.add(f'{cc}{LB_FIRST}:{cc}{LB_LAST}', FormulaRule(formula=[f'LEFT({cc}{LB_FIRST},4)="Need"'], font=Font(name=K.FONT, bold=True, color='B45309')))
    ta = c['Test again?']
    ws.conditional_formatting.add(f'{ta}{LB_FIRST}:{ta}{LB_LAST}', FormulaRule(formula=[f'LEFT({ta}{LB_FIRST},3)="Yes"'], font=Font(name=K.FONT, bold=True, color='9B2C1F')))
    for h in LB_HID + ['Rank (helper)']:
        ws.column_dimensions[c[h]].hidden = True
    for r in range(LB_FIRST, LB_FIRST + len(PROMPTS)):
        ws.row_dimensions[r].height = 32
    ws.freeze_panes = 'C5'
    ws.auto_filter.ref = f'A4:{c["Test again?"]}{LB_LAST}'
    return ws


def sov_sheet(wb):
    ws = wb.create_sheet('Share of Voice')
    ws.sheet_view.showGridLines = False
    K.title_block(ws, 'Share of voice', 'How often each brand is named, on UNBRANDED prompts only, so prompts that already name you do not inflate your numbers.')
    for col, w in zip('ABCDEFGHI', [24, 9, 12, 12, 12, 12, 12, 12, 3]):
        ws.column_dimensions[col].width = w
    heads = ['Engine', 'Runs', '=' + BRAND] + [f'={x}' for x in COMP]

    def block(top, title, label, items, crit_col):
        ws.cell(row=top - 1, column=1, value=title).font = K.f(10, True, K.DEEP)
        for j, h in enumerate([label] + heads[1:]):
            cell = ws.cell(row=top, column=1 + j, value=h)
            cell.font, cell.fill = K.f(10, True, 'FFFFFF'), K.HEAD_F
        for i, it in enumerate(items):
            r = top + 1 + i
            ws.cell(row=r, column=1, value=it)
            base = f'{lg(crit_col)},$A{r},{lg("Branded prompt?")},"Unbranded"'
            ws.cell(row=r, column=2, value=f'=COUNTIFS({base})')
            ws.cell(row=r, column=3, value=f'=IF(B{r}=0,"",COUNTIFS({base},{lg("You named?")},"Yes")/B{r})')
            for k in range(5):
                ws.cell(row=r, column=4 + k, value=f'=IF(OR(B{r}=0,{COMP[k]}=""),"",SUMIFS({lg(CF[k])},{base})/B{r})')
            for cc in range(1, 9):
                cell = ws.cell(row=r, column=cc)
                cell.border, cell.font = K.BORDER, K.f(10, cc == 1)
                cell.fill = K.FORMULA_FILL if cc > 1 else PatternFill(fill_type=None)
                if cc > 2:
                    cell.number_format = '0%'
        rng = f'C{top + 1}:H{top + len(items)}'
        ws.conditional_formatting.add(rng, ColorScaleRule(start_type='num', start_value=0, start_color='FFFFFF', end_type='num', end_value=1, end_color='8BC34A'))
        return top + 1, top + len(items)
    e1, e2 = block(5, 'MENTION RATE BY ENGINE (share of unbranded runs that name each brand)', 'Engine', ENGINES, 'C')
    i1, i2 = block(e2 + 4, 'MENTION RATE BY INTENT TYPE (unbranded runs)', 'Intent type', [x[0] for x in INTENTS], 'Intent type')
    t = i2 + 4
    ws.cell(row=t - 1, column=1, value='SHARE OF VOICE (all unbranded runs)').font = K.f(10, True, K.DEEP)
    for j, h in enumerate(['Brand', 'Mentions', 'Share of voice', 'Mention rate']):
        cell = ws.cell(row=t, column=1 + j, value=h)
        cell.font, cell.fill = K.f(10, True, 'FFFFFF'), K.HEAD_F
    unb = f'{lg("Branded prompt?")},"Unbranded"'
    ws.cell(row=t + 1, column=1, value=f'={BRAND}')
    ws.cell(row=t + 1, column=2, value=f'=COUNTIFS({unb},{lg("You named?")},"Yes")')
    for k in range(5):
        ws.cell(row=t + 2 + k, column=1, value=f'=IF({COMP[k]}="","",{COMP[k]})')
        ws.cell(row=t + 2 + k, column=2, value=f'=SUMIFS({lg(CF[k])},{unb})')
    for r in range(t + 1, t + 7):
        ws.cell(row=r, column=3, value=f'=IF(SUM($B${t + 1}:$B${t + 6})=0,"",B{r}/SUM($B${t + 1}:$B${t + 6}))').number_format = '0%'
        ws.cell(row=r, column=4, value=f'=IF(COUNTIFS({unb})=0,"",B{r}/COUNTIFS({unb}))').number_format = '0%'
        for cc in range(1, 5):
            cell = ws.cell(row=r, column=cc)
            cell.border, cell.font = K.BORDER, K.f(10, cc == 1)
            if cc > 1:
                cell.fill = K.FORMULA_FILL
    ws['F' + str(t)] = 'Share of voice = a brand\'s mentions / all mentions of the 6 tracked brands.'
    ws['F' + str(t)].font = K.f(9, False, '777777', True)
    ch = BarChart()
    ch.type = 'bar'
    ch.title = 'Share of voice (unbranded prompts)'
    ch.add_data(Reference(ws, min_col=3, min_row=t + 1, max_row=t + 6), titles_from_data=False)
    ch.set_categories(Reference(ws, min_col=1, min_row=t + 1, max_row=t + 6))
    ch.legend = None
    ch.height, ch.width = 8, 16
    ch.x_axis.delete = False
    ch.y_axis.delete = False
    ch.y_axis.numFmt = '0%'
    ch.title.overlay = False
    ch.series[0].graphicalProperties.solidFill = K.GREEN
    ws.add_chart(ch, f'J{e1 - 1}')
    return ws, (e1, e2, i1, i2, t)


def fix_sheet(wb):
    ws = wb.create_sheet('Fix Plan')
    ws.sheet_view.showGridLines = False
    K.title_block(ws, 'Fix plan', 'One row per problem you found. Pick the prompt and the problem; the prompt, current rate, fix and hours fill in. Retest the prompt after the fix.')
    head = ['Prompt ID', 'Problem', 'What the AI said', 'The correct fact or goal', 'Source to fix', 'Owner', 'Week', 'Status', 'Done on',
            'Mention rate before', 'Mention rate after', 'Wrong answers in the retest', 'Prompt', 'Mention rate now', 'Suggested fix', 'Hours (assumption)', 'Measure on', 'Change', 'Result']
    fc = tuple(range(13, 20))
    K.header_row(ws, 4, head, formula_cols=fc, widths=[8, 20, 30, 34, 20, 14, 9, 9, 11, 10, 10, 10, 36, 10, 52, 9, 11, 9, 34])
    for r in range(FX_FIRST, FX_LAST + 1):
        i = r - FX_FIRST
        if i < len(FIXES):
            for col, v in enumerate(FIXES[i], 1):
                if col == 9:
                    v = d(v)
                if v not in (None, ''):
                    ws.cell(row=r, column=col, value=v)
        e = f'A{r}=""'
        m = f'MATCH(A{r},{lb("A")},0)'
        pr = f'MATCH(B{r},{S}!$D${PR_FIRST}:$D${PR_FIRST + 5},0)'
        ws[f'M{r}'] = f'=IF({e},"",IFERROR(INDEX({lb("B")},{m}),"Prompt ID not in the library"))'
        ws[f'N{r}'] = f'=IF({e},"",IFERROR(INDEX({lb("Mention rate")},{m}),""))'
        ws[f'O{r}'] = f'=IF(OR({e},B{r}=""),"",IFERROR(INDEX({S}!$F${PR_FIRST}:$F${PR_FIRST + 5},{pr}),""))'
        ws[f'P{r}'] = f'=IF(OR({e},B{r}=""),"",IFERROR(INDEX({S}!$E${PR_FIRST}:$E${PR_FIRST + 5},{pr}),0))'
        ws[f'Q{r}'] = f'=IF(OR({e},I{r}=""),"",I{r}+{MEASURE})'
        ws[f'R{r}'] = f'=IF(OR({e},J{r}="",K{r}=""),"",K{r}-J{r})'
        ws[f'S{r}'] = (f'=IF({e},"",IF(H{r}<>"Done","Not done yet",IF(I{r}="","Add the done date",IF({DATE}<Q{r},"Wait: "&(Q{r}-{DATE})&" days left",'
                       f'IF(B{r}="Wrong fact",IF(L{r}="","Retest and count wrong answers",IF(L{r}=0,"Fixed: facts now correct","Still wrong in "&L{r}&" runs: fix more sources")),'
                       f'IF(R{r}="","Retest and add the rate after",IF(R{r}>=0.1,"Up "&TEXT(R{r}*100,"0")&" points: keep going",IF(R{r}>-0.1,"Flat: give it another cycle","Down: check what changed"))))))))')
    K.style_body(ws, FX_FIRST, FX_LAST, len(head), formula_cols=fc, number_formats={9: 'dd mmm yyyy', 10: '0%', 11: '0%', 12: '0', 14: '0%', 16: '0', 17: 'dd mmm yyyy', 18: '0%'},
                 wrap_cols=(2, 3, 4, 5, 13, 15, 19))
    for r in range(FX_FIRST, FX_FIRST + len(FIXES)):
        ws.row_dimensions[r].height = 45
    K.dropdown(ws, f'A{FX_FIRST}:A{FX_LAST}', lb('A'), 'Prompt IDs from the Prompt Library.')
    K.dropdown(ws, f'B{FX_FIRST}:B{FX_LAST}', f'{S}!$D${PR_FIRST}:$D${PR_FIRST + 5}')
    K.dropdown(ws, f'E{FX_FIRST}:E{FX_LAST}', f'{S}!$N$6:$N$15')
    K.dropdown(ws, f'F{FX_FIRST}:F{FX_LAST}', f'{S}!$O$6:$O$17')
    K.dropdown(ws, f'G{FX_FIRST}:G{FX_LAST}', f'{S}!$P$6:$P$13')
    K.dropdown(ws, f'H{FX_FIRST}:H{FX_LAST}', f'{S}!$H$19:$H$21')
    t = f'S{FX_FIRST}:S{FX_LAST}'
    ws.conditional_formatting.add(t, FormulaRule(formula=[f'OR(LEFT(S{FX_FIRST},2)="Up",LEFT(S{FX_FIRST},5)="Fixed")'], fill=PatternFill('solid', fgColor='B7E4A0'), font=Font(name=K.FONT, bold=True)))
    ws.conditional_formatting.add(t, FormulaRule(formula=[f'OR(LEFT(S{FX_FIRST},4)="Down",LEFT(S{FX_FIRST},5)="Still")'], fill=PatternFill('solid', fgColor='F8D7D3'), font=Font(name=K.FONT, bold=True, color='9B2C1F')))
    ws.conditional_formatting.add(t, FormulaRule(formula=[f'OR(LEFT(S{FX_FIRST},4)="Wait",LEFT(S{FX_FIRST},4)="Flat",LEFT(S{FX_FIRST},6)="Retest")'], fill=PatternFill('solid', fgColor='FFF4CC')))
    ws['U4'] = 'WEEKLY FIX HOURS'
    ws['U4'].font = K.f(10, True, K.DEEP)
    for j, h in enumerate(['Week', 'Hours planned', 'Capacity', 'Status']):
        cc = ws.cell(row=5, column=21 + j, value=h)
        cc.font, cc.fill = K.f(10, True, 'FFFFFF'), K.HEAD_F
    for i in range(len(WEEKS)):
        r = 6 + i
        ws.cell(row=r, column=21, value=f'={S}!P{6 + i}')
        ws.cell(row=r, column=22, value=f'=SUMIF($G${FX_FIRST}:$G${FX_LAST},U{r},$P${FX_FIRST}:$P${FX_LAST})')
        ws.cell(row=r, column=23, value=f'={HOURS}')
        ws.cell(row=r, column=24, value=f'=IF(V{r}=0,"Free",IF(V{r}>W{r},"Over capacity by "&(V{r}-W{r})&" hours","OK"))')
        for cc in range(21, 25):
            cell = ws.cell(row=r, column=cc)
            cell.border, cell.fill, cell.font = K.BORDER, K.FORMULA_FILL, K.f(10)
    for col, w in zip(['T', 'U', 'V', 'W', 'X'], [3, 12, 10, 9, 24]):
        ws.column_dimensions[col].width = w
    ws.conditional_formatting.add('X6:X13', FormulaRule(formula=['LEFT(X6,4)="Over"'], fill=PatternFill('solid', fgColor='F8D7D3'), font=Font(name=K.FONT, bold=True, color='9B2C1F')))
    ws.freeze_panes = 'B5'
    ws.auto_filter.ref = f'A4:S{FX_LAST}'
    return ws


TEMPLATES = [
    ('Recommendation', 'What is the best [category] for [audience]?'),
    ('Recommendation', 'Recommend 5 [category] options for [audience] in [location].'),
    ('Recommendation', 'Which [category] is easiest to set up for [audience]?'),
    ('Recommendation', 'I run [audience]. Which [category] should I choose and why?'),
    ('Comparison', '[brand] vs [competitor]: which is better for [use case]?'),
    ('Comparison', 'Compare the top [category] tools for [use case].'),
    ('Comparison', 'Is [brand] or [competitor] cheaper for [audience]?'),
    ('Alternatives', 'What are the best alternatives to [competitor]?'),
    ('Alternatives', 'What are good alternatives to [brand]?'),
    ('Problem or how to', 'How can [audience] handle [use case] better?'),
    ('Problem or how to', 'What tools help [audience] with [use case]?'),
    ('Pricing', 'How much does [category] cost for [audience]?'),
    ('Pricing', 'Is there a free [category] for [audience]?'),
    ('Brand facts', 'What is [brand] and who is it for?'),
    ('Brand facts', 'How much does [brand] cost?'),
    ('Brand facts', 'Does [brand] work for [use case]?'),
    ('Reviews and trust', 'Is [brand] good? What do users say?'),
    ('Reviews and trust', 'What are the downsides of [brand]?'),
    ('Local', 'Best [category] companies in [location]'),
    ('Local', 'Which [category] has support in [location]?'),
]
PB_INPUTS = [('Category (how buyers name it)', 'help desk software'), ('Audience', 'small teams'), ('Location', 'India'),
             ('Main competitor', None), ('Use case', 'customer support by email')]


def builder_sheet(wb):
    ws = wb.create_sheet('Prompt Builder')
    ws.sheet_view.showGridLines = False
    K.title_block(ws, 'Prompt builder', 'Fill the yellow cells. 20 templates and 6 personas write prompts for you. Copy the ones that sound like your buyers into the Prompt Library.')
    for col, w in zip('ABCDEF', [6, 30, 52, 66, 12, 12]):
        ws.column_dimensions[col].width = w
    ws['B4'] = 'YOUR INPUTS'
    ws['B4'].font = K.f(10, True, K.DEEP)
    for i, (label, v) in enumerate(PB_INPUTS):
        r = 5 + i
        ws.cell(row=r, column=2, value=label).font = K.f(10)
        c = ws.cell(row=r, column=3, value=v if v else f'={COMP[0]}')
        c.border, c.font = K.BORDER, K.f(10, True, '0000FF')
        c.fill = K.INPUT_FILL
    ws['B10'] = 'Brand (from Settings)'
    ws['C10'] = f'={BRAND}'
    ws['C10'].fill, ws['C10'].border = K.FORMULA_FILL, K.BORDER
    ws['D5'] = 'Placeholders: [category] [audience] [location] [competitor] [use case] [brand]. Edit any template in column C; the prompt rewrites itself.'
    ws['D5'].font = K.f(9, False, '777777', True)
    ws['D5'].alignment = Alignment(wrap_text=True)
    ws.merge_cells('D5:F7')
    top = 12
    K.header_row(ws, top, ['#', 'Intent type', 'Template (edit me)', 'Prompt', 'Branded?', 'In library?'], formula_cols=(4, 5, 6))
    for i, (intent, tpl) in enumerate(TEMPLATES):
        r = top + 1 + i
        ws.cell(row=r, column=1, value=i + 1)
        ws.cell(row=r, column=2, value=intent)
        ws.cell(row=r, column=3, value=tpl)
        sub = f'C{r}'
        for ph, ref in (('[category]', '$C$5'), ('[audience]', '$C$6'), ('[location]', '$C$7'), ('[competitor]', '$C$8'), ('[use case]', '$C$9'), ('[brand]', '$C$10')):
            sub = f'SUBSTITUTE({sub},"{ph}",{ref})'
        ws.cell(row=r, column=4, value=f'=IF(C{r}="","",{sub})')
        ws.cell(row=r, column=5, value=f'=IF(D{r}="","",IF({named(f"D{r}")},"Branded","Unbranded"))')
        ws.cell(row=r, column=6, value=f'=IF(D{r}="","",IF(COUNTIF({lb("B")},D{r})>0,"Yes","No"))')
        for cc in range(1, 7):
            cell = ws.cell(row=r, column=cc)
            cell.border, cell.font = K.BORDER, K.f(10)
            cell.alignment = Alignment(wrap_text=True, vertical='top')
            cell.fill = K.INPUT_FILL if cc in (2, 3) else K.FORMULA_FILL
        ws.row_dimensions[r].height = 30
    K.dropdown(ws, f'B{top + 1}:B{top + len(TEMPLATES)}', f'{S}!$D${INT_FIRST}:$D${INT_FIRST + 7}')
    pt = 37
    ws.cell(row=pt - 1, column=2, value='PERSONA PROMPTS (a template with real context, the way people actually ask AI assistants)').font = K.f(10, True, K.DEEP)
    K.header_row(ws, pt, ['', 'Persona', 'Context (edit me)', 'Persona prompt', 'Template #', ''], formula_cols=(4,))
    for i, (name, ctx) in enumerate(PERSONAS):
        r = pt + 1 + i
        ws.cell(row=r, column=2, value=name)
        ws.cell(row=r, column=3, value=ctx)
        ws.cell(row=r, column=5, value=[1, 3, 2, 11, 6, 4][i])
        ws.cell(row=r, column=4, value=f'=IF(OR(C{r}="",E{r}=""),"",C{r}&" "&IFERROR(INDEX($D${top + 1}:$D${top + len(TEMPLATES)},E{r}),""))')
        for cc in range(2, 6):
            cell = ws.cell(row=r, column=cc)
            cell.border, cell.font = K.BORDER, K.f(10)
            cell.alignment = Alignment(wrap_text=True, vertical='top')
            cell.fill = K.FORMULA_FILL if cc == 4 else K.INPUT_FILL
        ws.row_dimensions[r].height = 42
    K.whole_number(ws, f'E{pt + 1}:E{pt + 6}', 1, len(TEMPLATES), 'A template number from 1 to 20.')
    ws.conditional_formatting.add(f'F{top + 1}:F{top + len(TEMPLATES)}', CellIsRule(operator='equal', formula=['"Yes"'], fill=PatternFill('solid', fgColor='D9F2C4'), font=Font(name=K.FONT, bold=True, color='3D7F12')))
    ws.freeze_panes = 'A13'
    return ws


def chart(ws, title, ytitle, cat_col, val_cols, r1, r2, anchor, colors, horiz, h=7.5, w=16, pct=False):
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
    if pct:
        ch.y_axis.numFmt = '0%'
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


def dashboard_sheet(wb, sov_rows):
    e1, e2, i1, i2, t = sov_rows
    ws = wb.create_sheet('Dashboard')
    ws.sheet_view.showGridLines = False
    K.title_block(ws, 'Dashboard', 'Everything here calculates from the other tabs. Nothing to type.')
    for col, w in zip('ABCDEFGHIJ', [50, 13, 3, 8, 44, 30, 8, 14, 10, 3]):
        ws.column_dimensions[col].width = w
    unb = f'{lg("Branded prompt?")},"Unbranded"'
    FXH, FXS_ = f'{FXS}!$H${FX_FIRST}:$H${FX_LAST}', f'{FXS}!$S${FX_FIRST}:$S${FX_LAST}'
    kpis = [
        ('Prompts in the library', f'=COUNTIF({lb("A")},"?*")', '0'),
        ('Active prompts', f'=COUNTIF({lb("J")},"Yes")', '0'),
        ('Prompts tested at least once', f'=COUNTIF({lb("Runs")},">0")', '0'),
        ('Prompts with enough runs to trust', f'=COUNTIF({lb("Confidence")},"Enough runs")', '0'),
        ('Test runs logged', f'=COUNTIF({lg("B")},"?*")', '0'),
        ('Engines covered', '=' + '+'.join(f'IF(COUNTIF({lg("C")},{S}!$H${6 + k})>0,1,0)' for k in range(len(ENGINES))), '0'),
        ('Mention rate, unbranded prompts', f'=IFERROR(COUNTIFS({unb},{lg("You named?")},"Yes")/COUNTIFS({unb}),"")', '0%'),
        ('Named first, unbranded prompts', f'=IFERROR(COUNTIFS({unb},{lg("Your position")},1)/COUNTIFS({unb}),"")', '0%'),
        ('Your URL cited (all runs)', f'=IFERROR(COUNTIF({lg("F")},"Yes")/B9,"")', '0%'),
        ('Prompts where you are strong', f'=COUNTIF({lb("Status")},"Strong*")', '0'),
        ('Prompts where you are mentioned sometimes', f'=COUNTIF({lb("Status")},"Mentioned*")', '0'),
        ('Prompts where you are absent', f'=COUNTIF({lb("Status")},"Absent*")', '0'),
        ('Prompts with wrong facts about you', f'=COUNTIF({lb("Status")},"Wrong*")', '0'),
        ('Wrong or partly wrong answers (runs)', f'=COUNTIF({lg("I")},"Wrong")+COUNTIF({lg("I")},"Partly wrong")', '0'),
        ('Average tone when named (-1 to 1)', f'=IFERROR((COUNTIF({lg("H")},"Positive")-COUNTIF({lg("H")},"Negative"))/COUNTIF({lg("You named?")},"Yes"),"")', '0.00'),
        ('Your share of voice, unbranded prompts', f"={SVS}!C{t + 1}", '0%'),
        ('Top competitor by share of voice', f"=INDEX({SVS}!$A${t + 2}:$A${t + 6},MATCH(MAX({SVS}!$C${t + 2}:$C${t + 6}),{SVS}!$C${t + 2}:$C${t + 6},0))", '@'),
        ('Top competitor share of voice', f"=MAX({SVS}!$C${t + 2}:$C${t + 6})", '0%'),
        ('Fixes open (To do or Doing)', f'=COUNTIF({FXH},"To do")+COUNTIF({FXH},"Doing")', '0'),
        ('Fixes that worked (up or fixed)', f'=COUNTIF({FXS_},"Up*")+COUNTIF({FXS_},"Fixed*")', '0'),
    ]
    ws['A4'] = 'KEY NUMBERS'
    ws['A4'].font = K.f(10, True, K.DEEP)
    for i, (label, fml, fmt) in enumerate(kpis):
        r = 5 + i
        ws.cell(row=r, column=1, value=label).font = K.f(10)
        cell = ws.cell(row=r, column=2, value=fml)
        cell.number_format, cell.font, cell.fill, cell.border = fmt, K.f(11, True), K.FORMULA_FILL, K.BORDER
        cell.alignment = Alignment(horizontal='right')
    ws['D4'] = 'TOP 10 PROMPTS TO WORK ON (wrong facts first, then priority score)'
    ws['D4'].font = K.f(10, True, K.DEEP)
    heads = ['ID', 'Prompt', 'Status', 'Mention', 'Priority', 'Top rival']
    cols = ['A', 'B', 'Status', 'Mention rate', 'Priority', 'Top competitor']
    head_cells(ws, 5, 4, heads)
    rk = lb('Rank (helper)')
    for k in range(1, 11):
        r = 5 + k
        mt = f'MATCH(LARGE({rk},{k}),{rk},0)'
        for j, col in enumerate(cols):
            cell = ws.cell(row=r, column=4 + j, value=f'=IFERROR(INDEX({lb(col)},{mt}),"")')
            cell.border, cell.fill, cell.font = K.BORDER, K.FORMULA_FILL, K.f(9, j == 1)
            cell.alignment = Alignment(wrap_text=j in (1, 2, 4), vertical='top')
            cell.number_format = {3: '0%'}.get(j, '@')
        ws.row_dimensions[r].height = 30
    top = 28
    ws.cell(row=top - 1, column=1, value='PROMPTS BY STATUS').font = K.f(10, True, K.DEEP)
    head_cells(ws, top, 1, ['Status', 'Prompts'])
    for i in range(len(STATUSES)):
        r = top + 1 + i
        ws.cell(row=r, column=1, value=f'={S}!D{ST_FIRST + i}')
        ws.cell(row=r, column=2, value=f'=COUNTIF({lb("Status")},A{r})')
        for cc in (1, 2):
            cell = ws.cell(row=r, column=cc)
            cell.border, cell.fill, cell.font = K.BORDER, K.FORMULA_FILL, K.f(10, cc == 1)
    t2 = top + len(STATUSES) + 4
    ws.cell(row=t2 - 1, column=1, value='YOUR MENTION RATE BY ENGINE (unbranded prompts)').font = K.f(10, True, K.DEEP)
    head_cells(ws, t2, 1, ['Engine', 'Mention rate'])
    for i in range(len(ENGINES)):
        r = t2 + 1 + i
        ws.cell(row=r, column=1, value=f'={SVS}!A{e1 + i}').border = K.BORDER
        cell = ws.cell(row=r, column=2, value=f'=IF({SVS}!C{e1 + i}="",0,{SVS}!C{e1 + i})')
        cell.border, cell.fill, cell.number_format = K.BORDER, K.FORMULA_FILL, '0%'
    chart(ws, 'Prompts by status', 'Prompts', 1, [2], top + 1, top + len(STATUSES), 'D18', ['E07A5F'], True, h=9, w=18)
    chart(ws, 'Your mention rate by engine', 'Mention rate', 1, [2], t2 + 1, t2 + len(ENGINES), 'D37', [K.GREEN], False, w=18, pct=True)
    return ws


def build(path, asset, url):
    wb = K.new_book()
    library_sheet(wb)
    _, rows = log_sheet(wb)
    _, sov_rows = sov_sheet(wb)
    fix_sheet(wb)
    builder_sheet(wb)
    dashboard_sheet(wb, sov_rows)
    settings_sheet(wb)
    K.prompts_sheet(wb, asset['prompts'], url)
    K.checklist_sheet(wb, list(asset['checklist']))
    K.sources_sheet(wb, asset['sources'], [
        ('Demo data', 'CalmDesk, its competitors (HelpHive, TicketNest, SupportLoop, DeskPilot, AnswerBay), every URL and every answer in the demo are fictional. Runs, rates and dates are illustrative, not real data.', ''),
        ('Run minimum, thresholds, weights and hours', 'The 10 run minimum, the 60 and 20 percent thresholds, the priority weights and the hours per fix are assumptions of this kit. Tune them on Settings.', ''),
        ('Why rates, not ranks', 'A SparkToro and Gumshoe study (January 2026, 2,961 runs of 12 prompts in ChatGPT, Claude and Google AI) found less than a 1 in 100 chance of the same brand list twice, and recommends visibility percentage across many runs over ranking position.', 'https://sparktoro.com/blog/new-research-ais-are-highly-inconsistent-when-recommending-brands-or-products-marketers-should-take-care-when-tracking-ai-visibility/'),
        ('Intent matters', 'A Conductor study (14,000 API calls, 4 engines, 7 intent types) found consistency varies by intent type and recommends tracking by intent and engine separately.', 'https://www.conductor.com/academy/ai-recommendation-consistency-analysis/'),
        ('Platform data', 'Bing Webmaster Tools reports AI citations and grounding queries for Copilot and Bing AI summaries; Search Console reports impressions in AI Overviews and AI Mode; ChatGPT adds utm_source=chatgpt.com to referral links.', 'https://blogs.bing.com/webmaster/February-2026/Introducing-AI-Performance-in-Bing-Webmaster-Tools-Public-Preview'),
    ])
    K.start_here(
        wb, 'AEO Prompt Library Kit',
        [
            'This workbook tests how AI assistants see your brand. You keep a library of the prompts real buyers ask, run each one several times in ChatGPT, Gemini, Perplexity, Google AI Mode or any engine you choose, and log what each answer says.',
            f'The sheet turns the runs into mention rates, named first rates, cited rates, tone, wrong answers and share of voice against 5 competitors, then gives every prompt a status, a next action and a priority. A worked demo for a fictional help desk app ({len(PROMPTS)} prompts, {len(rows)} runs, {len(FIXES)} fixes) shows every formula working.',
        ],
        [
            ('Prompt Library', 'One row per prompt, 500 rows ready. Intent, funnel, persona, origin, value, target page, plus runs, engines, mention, first, cited and tone rates, wrong answers, top competitor, status, priority and retest date.'),
            ('Test Log', 'One row per run, 1,000 rows ready. Paste the brands named in order; the sheet finds you, your position and each competitor and checks the row.'),
            ('Share of Voice', 'Mention rates by engine and by intent type for you and 5 competitors, and share of voice with a chart. Unbranded prompts only.'),
            ('Fix Plan', 'Wrong facts, absent prompts and negative tone with the source to fix, hours, a weekly hours check and a before and after result.'),
            ('Prompt Builder', '20 editable templates across 8 intent types and 6 personas that write prompts from your category, audience and location.'),
            ('Dashboard', '20 key numbers, the top 10 prompts to work on, prompts by status and your mention rate by engine, with charts.'),
            ('Settings', 'Your brand and aliases, 5 competitors, rules, priority weights, intent types, problems and fixes, statuses and lists.'),
            ('AI Prompts', 'Prompts for ChatGPT, Claude or Gemini to build the library, read answers, find sources and plan fixes.'),
            ('Checklist', 'The whole testing process as a tick list with automatic progress.'),
            ('Sources', 'Where facts come from and which numbers are assumptions.'),
        ],
        [
            'Look at the demo on every tab. Then clear the yellow demo cells on Prompt Library, Test Log and Fix Plan.',
            'On Settings, type your brand, the other ways people write it and up to 5 competitors. Set today\'s date.',
            'Use the Prompt Builder and your own sales, support and Search Console questions to write 30 to 100 prompts in the Prompt Library.',
            'Run each prompt in a fresh chat in every engine you track, at least 3 times each. Log every run on the Test Log.',
            'Read the Prompt Library statuses and the Share of Voice tab. Check the Data check column for typing mistakes.',
            'Add wrong facts, absent prompts and negative tone to the Fix Plan, within your weekly hours.',
            'Retest every prompt monthly. After a fix, add the mention rate before and after. The Result column reads it.',
        ],
        url,
    )
    order = ['Start Here', 'Prompt Library', 'Test Log', 'Share of Voice', 'Fix Plan', 'Prompt Builder', 'Dashboard', 'Settings', 'AI Prompts', 'Checklist', 'Sources']
    wb._sheets = [wb[n] for n in order]
    wb.active = 0
    for ws in wb.worksheets:
        ws.sheet_properties.tabColor = K.GREEN if ws.title in order[:7] else 'A6EF39'
    wb.save(path)


PREVIEW = {'sheet': 'Prompt Library', 'header_row': 4, 'rows': 12,
           'cols': [1, 2, 4, len(LB_IN) + 1, len(LB_IN) + 2, len(LB_IN) + 5, len(LB_IN) + 14, len(LB_IN) + 17],
           'formula_idx': [3, 4, 5, 6, 7]}


def values(wb):
    lbw, fx = wb['Prompt Library'], wb['Fix Plan']
    out = {}
    for i in range(len(PROMPTS)):
        r = LB_FIRST + i
        out[('p', PROMPTS[i][0])] = {h: lbw[f'{BC[h]}{r}'].value for h in LB_HEAD}
    for i in range(len(FIXES)):
        r = FX_FIRST + i
        out[('fx', i)] = {k: fx[f'{k}{r}'].value for k in 'MNOPQRS'}
    return out


def check(wb):
    """Assert the worked examples used in the guide."""
    v = values(wb)
    p1 = v[('p', 'P01')]
    assert p1['Branded?'] == 'Unbranded' and p1['Runs'] == 12 and p1['Engines tested'] == 4, (p1['Runs'], p1['Engines tested'])
    assert p1['Runs that name you'] == 6 and abs(p1['Mention rate'] - 0.5) < 1e-9, p1['Runs that name you']
    assert p1['Status'] == 'Mentioned sometimes: build proof' and p1['Top competitor'] == 'HelpHive', (p1['Status'], p1['Top competitor'])
    assert p1['Priority score (0 to 100)'] == 65 and p1['Priority'] == 'P1: now', p1['Priority score (0 to 100)']
    assert p1['Days since tested'] == 10 and p1['Test again?'] == 'In 20 days'
    assert abs(p1['Named first rate'] - 1 / 12) < 1e-9 and abs(p1['Cited rate'] - 2 / 12) < 1e-9 and abs(p1['Tone (-1 to 1)'] - 1 / 3) < 1e-9
    assert v[('p', 'P11')]['Tone (-1 to 1)'] == -0.25 and v[('p', 'P10')]['Runs that name you'] == 12
    sv = wb['Share of Voice']
    sov = {sv.cell(row=r, column=1).value: (sv.cell(row=r, column=2).value, sv.cell(row=r, column=3).value) for r in range(29, 35)}
    assert sov['CalmDesk'][0] == 49 and round(sov['CalmDesk'][1], 2) == 0.15 and round(sov['TicketNest'][1], 2) == 0.21 and round(sov['HelpHive'][1], 2) == 0.20, sov
    eng = {sv.cell(row=r, column=1).value: sv.cell(row=r, column=3).value for r in range(6, 13)}
    assert round(eng['Perplexity'], 2) == 0.44 and round(eng['Google AI Mode'], 2) == 0.21, eng
    p10 = v[('p', 'P10')]
    assert p10['Branded?'] == 'Branded' and p10['Wrong or partly wrong answers'] == 5 and p10['Status'] == 'Wrong facts: fix the source' and p10['Priority'] == 'P1: fix facts'
    assert v[('p', 'P11')]['Status'] == 'Branded: negative tone', v[('p', 'P11')]['Status']
    assert v[('p', 'P03')]['Status'] == 'Strong: protect it' and v[('p', 'P09')]['Status'] == 'Branded: accurate, protect it'
    assert v[('p', 'P02')]['Status'] == 'Absent: competitors win' and v[('p', 'P16')]['Status'] == 'Absent: no brand named'
    assert v[('p', 'P17')]['Status'] == 'Too few runs: test more' and v[('p', 'P17')]['Confidence'] == 'Need 7 more'
    assert v[('p', 'P18')]['Status'] == 'Not tested yet' and v[('p', 'P19')]['Status'] == 'Paused'
    assert v[('fx', 0)]['S'] == 'Wait: 16 days left' and v[('fx', 4)]['S'] == 'Up 25 points: keep going' and v[('fx', 5)]['S'] == 'Up 17 points: keep going', (v[('fx', 0)]['S'], v[('fx', 4)]['S'])
    f = wb['Fix Plan']
    assert f['V6'].value == 3 and f['V7'].value == 12 and f['X7'].value == 'Over capacity by 4 hours', (f['V6'].value, f['V7'].value, f['X7'].value)
    lgw = wb['Test Log']
    for r in range(LG_FIRST, LG_FIRST + 200):
        if lgw[f'B{r}'].value is None:
            break
        assert lgw[f'{GC["Data check"]}{r}'].value == 'OK', (r, lgw[f'{GC["Data check"]}{r}'].value)
    dsh = wb['Dashboard']
    k = {dsh.cell(row=r, column=1).value: dsh.cell(row=r, column=2).value for r in range(5, 25)}
    assert k['Prompts in the library'] == len(PROMPTS) and k['Engines covered'] == 4, k
    assert k['Test runs logged'] == 207 and round(k['Mention rate, unbranded prompts'], 2) == 0.31 and k['Top competitor by share of voice'] == 'TicketNest', k
    s = wb['Settings']
    assert s['E19'].value == 100
    return v
