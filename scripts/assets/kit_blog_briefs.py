"""Content Brief Kit workbook (asset 16, blog briefs).

Brief Pipeline: one row per planned article (500 rows) with focus keyword, intent, format, reader, goal, demand,
difficulty, business value, AI Overview check, competitor length, information gain, links, writer, due date and
status. The sheet works out title checks, duplicate focus keywords, a target length band, outline sections and
words, whether an answer first block is needed, an information gain check, brief completeness (11 fields), an
opportunity score (0 to 100), a priority, writing hours (assumption), due status and the next step.
Outline Bank: H2, H3 and FAQ sections for every brief. Brief Builder: pick an article and the full brief, outline
and pre hand over checks assemble themselves. Dashboard sums it all up.
"""
import datetime
from openpyxl.styles import PatternFill, Font, Alignment
from openpyxl.formatting.rule import CellIsRule, ColorScaleRule, FormulaRule
from openpyxl.chart import BarChart, Reference
from openpyxl.utils import get_column_letter as L
import kitlib as K

BP_FIRST, BP_LAST = 5, 504      # Brief Pipeline (500 rows)
OB_FIRST, OB_LAST = 5, 504      # Outline Bank (500 rows)
S = 'Settings'
BPS = "'Brief Pipeline'"
OBS = "'Outline Bank'"
BBS = "'Brief Builder'"
SEL = f'{BBS}!$C$5'

(DATE, FULL, P1, P2, P3, WPH, FACTOR, SOON, WEEKLY, TOL) = (f'{S}!$B${r}' for r in range(5, 15))
W_DEM, W_EASE, W_VAL, W_IG = (f'{S}!$G${r}' for r in range(6, 10))
FMT_RNG = f'{S}!$J$6:$M$14'
IG_RNG = f'{S}!$J$18:$K$24'

WEIGHTS = [('Demand (monthly searches)', 35), ('Ease (100 minus difficulty)', 20), ('Business value', 30), ('Information gain planned', 15)]
# format, min words, max words, research hours (all assumptions)
FORMATS = [('Guide', 1500, 3000, 4), ('How to', 1000, 2500, 3), ('List', 1000, 2500, 3), ('Comparison', 1200, 2500, 5),
           ('Review', 1200, 2500, 5), ('Template or tool', 600, 1500, 4), ('Glossary', 400, 1200, 1), ('Case study', 1000, 2000, 6),
           ('News', 400, 1000, 1)]
INFOGAIN = [('Original data or survey', 'Yes', 'Numbers you collected yourself: a survey, your product data, a test you ran'),
            ('First hand test or experience', 'Yes', 'You used the product, ran the process or visited the place, with photos or notes'),
            ('Expert quote or interview', 'Yes', 'A named expert answers questions the top results leave open'),
            ('Worked example with real numbers', 'Yes', 'A full example with real or clearly labelled illustrative numbers'),
            ('Free template or tool', 'Yes', 'Something the reader can download or use straight away'),
            ('Customer story', 'Yes', 'A real customer, with permission, and what changed for them'),
            ('None yet', 'No', 'The brief is not ready: find something the top results lack')]
INTENTS = ['Informational', 'Commercial', 'Transactional', 'Navigational']
FUNNEL = ['Awareness', 'Consideration', 'Decision']
STATUS = ['Idea', 'Briefed', 'Writing', 'Editing', 'Published']
WRITERS = ['Meera (writer)', 'Arjun (writer)', 'Freelance writer', 'SEO lead', 'Product marketer']
YNC = ['Yes', 'No', 'Not checked']
LEVELS = ['H2', 'H3', 'FAQ']
SECFMT = ['Paragraphs', 'Steps', 'Table', 'List', 'Checklist', 'Example', 'FAQ answer']

# Demo: Ledgerly, a fictional invoicing app for freelancers and small businesses (ledgerly.example). Illustrative numbers.
U = 'https://ledgerly.example'
# title, kw, secondary, intent, format, funnel, reader, goal, searches, kd, value, aio, comp words, infogain, ig detail,
# link to, links from, writer, due, status, published url, notes
ARTS = [
    ('How to make an invoice as a freelancer', 'how to make an invoice', 'invoice format, invoice number, what to include on an invoice', 'Informational', 'How to', 'Awareness',
     'Freelancers in India sending their first or second invoice', 'Make a correct invoice in 10 minutes; CTA: try the free invoice template',
     2400, 38, 3, 'Yes', 1850, 'Free template or tool', 'Free invoice template plus 3 filled examples from design, writing and consulting users',
     '/templates/invoice/, /blog/gst-invoice-rules/', '/blog/getting-paid-on-time/, /blog/freelance-pricing/', 'Meera (writer)', '2026-12-04', 'Briefed', '', 'Worked example in the guide'),
    ('GST invoice rules for small businesses', 'gst invoice rules', 'gst invoice format, gstin on invoice', 'Informational', 'Guide', 'Consideration',
     'Small business owners registered for GST', 'Understand what a GST invoice must show; CTA: GST ready invoices in Ledgerly',
     1300, 45, 3, 'Yes', 2600, 'Expert quote or interview', 'A chartered accountant answers the 5 questions our support team gets most',
     '/blog/how-to-make-an-invoice/', '/blog/invoice-numbering-rules/', 'Arjun (writer)', '2026-12-10', 'Idea', '', ''),
    ('Invoice vs bill: what is the difference?', 'invoice vs bill', 'bill vs invoice meaning', 'Informational', 'Comparison', 'Awareness',
     'New freelancers', 'Explain the difference in plain words', 900, 22, 1, 'Yes', 1100, 'None yet', '', '', '', '', '', 'Idea', '', 'Short topic: may fit as a FAQ instead'),
    ('Best invoicing software for freelancers in India', 'invoicing software for freelancers', 'free invoicing app, billing software', 'Commercial', 'Comparison', 'Decision',
     'Freelancers choosing a tool', 'Compare 6 tools honestly; CTA: start a Ledgerly trial', 1600, 52, 3, 'No', 3200, 'First hand test or experience',
     'We sent the same 3 invoices from every tool and timed each one', '/pricing/, /blog/how-to-make-an-invoice/', '/blog/getting-paid-on-time/', 'Arjun (writer)', '2026-11-20', 'Writing', '', ''),
    ('How to follow up on an unpaid invoice', 'unpaid invoice follow up', 'payment reminder email', 'Informational', 'How to', 'Consideration',
     'Freelancers with a late client', 'Get paid without losing the client; CTA: automatic reminders', 700, 18, 2, 'Yes', 1400, 'Worked example with real numbers',
     'Reminder timeline with 4 sample emails and what each one achieved for our users (illustrative)', '/blog/late-payment-fees/', '/blog/getting-paid-on-time/', 'Meera (writer)', '2026-11-28', 'Editing', '', ''),
    ('Payment terms explained: Net 15, Net 30 and more', 'payment terms', 'net 30 meaning, due on receipt', 'Informational', 'Guide', 'Awareness',
     'Freelancers and small agencies', 'Pick payment terms that get you paid sooner', 3600, 61, 2, 'Yes', 2200, 'Customer story',
     'Two agencies explain why they moved from Net 30 to Net 15', '/blog/how-to-make-an-invoice/', '/blog/unpaid-invoice-follow-up/', 'Freelance writer', '2026-12-18', 'Idea', '', ''),
    ('Free freelance invoice template', 'freelance invoice template', 'invoice template word, invoice template excel', 'Transactional', 'Template or tool', 'Decision',
     'Freelancers who want a template now', 'Download the template; CTA: send it from Ledgerly', 1900, 40, 3, 'No', 900, 'Free template or tool',
     'Template in 3 formats with a filled example', '/blog/how-to-make-an-invoice/', '/blog/how-to-make-an-invoice/', 'Meera (writer)', '2026-12-12', 'Idea', '', ''),
    ('How to make an invoice in Excel', 'how to make an invoice', 'invoice in excel', 'Informational', 'How to', 'Awareness',
     'Freelancers who use spreadsheets', 'Build a simple invoice sheet', 1000, 30, 2, 'Yes', 1500, 'Free template or tool', 'Excel file', '', '', 'Freelance writer', '2026-12-30', 'Idea', '', 'Same focus keyword as row 1: merge or retarget'),
    ('What is a proforma invoice?', 'proforma invoice', 'proforma invoice meaning', 'Informational', 'Glossary', 'Awareness',
     'Exporters and freelancers with foreign clients', 'Define it and show when to use it', 1200, 30, 1, 'Yes', 900, 'None yet', '', '/blog/how-to-make-an-invoice/', '', 'SEO lead', '2026-12-08', 'Idea', '', ''),
    ('Late payment fees: how to add them to invoices', 'late payment fees', 'late fee on invoice', 'Informational', 'How to', 'Consideration',
     'Freelancers with repeat late payers', 'Add fair late fees clients accept', 400, 15, 2, 'Yes', 1300, 'Expert quote or interview', 'A lawyer explains what to write in the contract',
     '/blog/unpaid-invoice-follow-up/', '/blog/payment-terms/', 'Arjun (writer)', '2026-12-20', 'Idea', '', ''),
    ('Invoicing app or spreadsheet: which is better?', 'invoice spreadsheet vs software', 'excel vs invoicing app', 'Commercial', 'Comparison', 'Decision',
     'Freelancers outgrowing spreadsheets', 'Show when an app saves time; CTA: free trial', 300, 12, 3, 'No', 1500, 'First hand test or experience',
     'Time taken for 20 invoices in a spreadsheet and in Ledgerly', '/pricing/', '/blog/how-to-make-an-invoice-in-excel/', 'Product marketer', '2026-12-15', 'Briefed', '', ''),
    ('Cash flow tips for freelancers', 'cash flow tips for freelancers', 'freelance cash flow', 'Informational', 'List', 'Awareness',
     'Freelancers with uneven income', 'Smooth monthly income; CTA: cash flow view', 1000, 48, 2, 'Yes', 2400, 'Original data or survey',
     'Survey of Ledgerly users on payment delays (run it before writing)', '/blog/payment-terms/', '', 'Freelance writer', '2027-01-08', 'Idea', '', ''),
    ('TDS on freelance income explained', 'tds on freelance income', 'tds for freelancers', 'Informational', 'Guide', 'Consideration',
     'Freelancers paid by Indian companies', 'Understand TDS deductions on invoices', 2900, 55, 2, 'Yes', 2800, 'Expert quote or interview', 'Chartered accountant review of every rule',
     '/blog/gst-invoice-rules/', '/blog/how-to-make-an-invoice/', 'Arjun (writer)', '2027-01-15', 'Idea', '', 'Fast changing rules: official sources only'),
    ('How to write a quote for a client', 'how to write a quote', 'quotation format', 'Informational', 'How to', 'Consideration',
     'Freelancers pricing a new project', 'Send clear quotes that turn into invoices', 600, 25, 2, 'No', 1300, 'Worked example with real numbers', 'Filled quote for a website project',
     '/blog/how-to-make-an-invoice/', '/blog/freelance-pricing/', 'Meera (writer)', '2026-12-22', 'Idea', '', ''),
    ('Getting paid on time: 12 habits', 'getting paid on time', 'how to get paid faster', 'Informational', 'List', 'Consideration',
     'Freelancers', 'Habits that cut late payments; CTA: reminders', 800, 35, 2, 'Yes', 1900, 'Customer story', 'Three users share the habit that worked best',
     '/blog/unpaid-invoice-follow-up/', '/blog/payment-terms/', 'Meera (writer)', '2026-11-10', 'Published', '/blog/getting-paid-on-time/', ''),
    ('Recurring invoices: when to use them', 'recurring invoices', 'retainer invoice', 'Commercial', 'How to', 'Decision',
     'Freelancers on retainers', 'Set up recurring billing; CTA: recurring invoices feature', 250, 10, 3, 'No', 1000, 'Worked example with real numbers', 'A retainer billed for 12 months',
     '/features/recurring/', '/blog/payment-terms/', 'Product marketer', '2026-12-05', 'Writing', '', ''),
    ('Invoice numbering rules', 'invoice numbering', 'invoice number format', 'Informational', 'How to', 'Awareness',
     'Small businesses', 'Number invoices correctly', 500, 20, 2, 'Yes', 1000, 'None yet', '', '', '', '', '', 'Idea', '', ''),
    ('Expense tracking for small business owners', 'expense tracking for small business', 'expense tracker', 'Commercial', 'Guide', 'Consideration',
     'Small business owners', 'Track expenses in 15 minutes a week; CTA: expense tracker', 1800, 58, 2, 'Yes', 2300, 'Free template or tool', 'Free expense tracker sheet',
     '/features/expenses/', '', 'Freelance writer', '2027-01-20', 'Idea', '', ''),
]
A1 = ARTS[0][0]
# article index, order, level, heading, question, points and entities, format, words, source
OUT = [
    (0, 1, 'H2', 'How to make an invoice in 6 steps', 'How do I make an invoice?', 'Answer first in 40 to 60 words, then the 6 steps: your details, client details, invoice number and date, items, tax, payment terms', 'Steps', 250, 'Our template and help docs'),
    (0, 2, 'H2', 'What to include on an invoice', 'What must an invoice include?', 'Business name and address, client details, invoice number, date, due date, description, amount, tax, payment details', 'Checklist', 300, 'Official GST portal for tax fields'),
    (0, 3, 'H3', 'Invoice numbering that stays in order', 'How should I number invoices?', 'Sequential numbers, one series per financial year, never reuse a number', 'Paragraphs', 150, 'Official GST rules'),
    (0, 4, 'H2', 'GST on freelance invoices', 'Do freelancers need GST on invoices?', 'GSTIN, when registration applies, link to the GST invoice rules post', 'Paragraphs', 250, 'Official GST portal'),
    (0, 5, 'H2', 'Three filled invoice examples', 'What does a good invoice look like?', 'Designer, writer and consultant examples with screenshots of the template', 'Example', 400, 'Our own examples (information gain)'),
    (0, 6, 'H2', 'Payment terms and due dates', 'What payment terms should I use?', 'Due on receipt, Net 15, Net 30, late fees; link to the payment terms guide', 'Table', 200, 'Our payment terms guide'),
    (0, 7, 'H2', 'Common invoice mistakes', 'What mistakes delay payment?', 'Missing due date, wrong client name, no payment details, vague descriptions', 'List', 200, 'Support tickets'),
    (0, 8, 'FAQ', 'How do I make an invoice for free?', 'How do I make an invoice for free?', 'Template, Word or Sheets, free plan', 'FAQ answer', 60, ''),
    (0, 9, 'FAQ', 'Can I make an invoice in Word or Excel?', 'Can I make an invoice in Word or Excel?', 'Yes, with a template; link to the Excel post', 'FAQ answer', 60, ''),
    (0, 10, 'FAQ', 'What is the difference between an invoice and a bill?', 'Invoice vs bill', 'One line answer and a link', 'FAQ answer', 60, ''),
    (1, 1, 'H2', 'What a GST invoice must show', 'What must a GST invoice include?', 'Every mandatory field as a checklist', 'Checklist', 500, 'Official GST portal'),
    (1, 2, 'H2', 'Tax invoice, bill of supply and other documents', 'Which document do I issue?', 'When to use each document', 'Table', 400, 'Official GST portal'),
    (1, 3, 'H2', 'GST invoice example', 'What does a GST invoice look like?', 'Annotated example invoice', 'Example', 400, 'Our template'),
    (1, 4, 'H2', 'Questions our accountant gets most', 'What do small businesses get wrong?', 'Expert answers to 5 support questions', 'FAQ answer', 600, 'Interview (information gain)'),
    (1, 5, 'H2', 'How long to keep invoices', 'How long must I keep GST invoices?', 'Record keeping rule with the official source', 'Paragraphs', 200, 'Official GST portal'),
    (3, 1, 'H2', 'The 6 invoicing tools we tested', 'Which invoicing software is best for freelancers?', 'Answer first: best for each need in one line', 'Table', 400, 'Our test'),
    (3, 2, 'H2', 'How we tested', 'How were the tools compared?', 'Same 3 invoices in every tool, timed, screenshots', 'Steps', 300, 'Our test (information gain)'),
    (3, 3, 'H2', 'Pricing compared', 'How much do invoicing apps cost?', 'Free plans, paid plans, limits; date checked', 'Table', 400, 'Each tool pricing page'),
    (3, 4, 'H2', 'Best free option', 'Is there a free invoicing app?', 'Free plans and their limits', 'Paragraphs', 300, 'Pricing pages'),
    (3, 5, 'H2', 'Which tool to pick for your situation', 'Which should I choose?', 'Decision table by need', 'Table', 400, ''),
    (3, 6, 'FAQ', 'Do I need software to send invoices?', 'Do I need invoicing software?', 'Honest answer: a template works at first', 'FAQ answer', 80, ''),
    (4, 1, 'H2', 'When to follow up on an unpaid invoice', 'When should I follow up?', 'Answer first, then a reminder timeline', 'Steps', 300, 'Our users (illustrative)'),
    (4, 2, 'H2', '4 follow up emails you can copy', 'What should a payment reminder say?', 'Friendly, firm, final, after due date', 'Example', 600, ''),
    (4, 3, 'H2', 'What to do if the client still does not pay', 'What if the client never pays?', 'Call, pause work, late fee, formal notice', 'List', 300, ''),
    (4, 4, 'FAQ', 'How many reminders should I send?', 'How many reminders?', 'Usually 3 or 4', 'FAQ answer', 60, ''),
    (10, 1, 'H2', 'Spreadsheet or app: the short answer', 'Is an invoicing app better than a spreadsheet?', 'Answer first: depends on invoice volume', 'Paragraphs', 200, 'Our test'),
    (10, 2, 'H2', 'Our 20 invoice test', 'How much time does an app save?', 'Timed test with screenshots', 'Table', 500, 'Our test (information gain)'),
    (10, 3, 'H2', 'When a spreadsheet is enough', 'When is a spreadsheet fine?', 'Low volume, one client', 'List', 300, ''),
    (14, 1, 'H2', '12 habits that get you paid on time', 'How do I get paid faster?', 'Answer first list', 'List', 900, ''),
    (14, 2, 'H2', 'What three freelancers changed', 'What works in practice?', 'Customer stories', 'Example', 600, 'Interviews'),
    (15, 1, 'H2', 'What a recurring invoice is', 'What is a recurring invoice?', 'Definition and when to use it', 'Paragraphs', 200, ''),
    (15, 2, 'H2', 'A retainer billed for 12 months', 'How does it work over a year?', 'Worked example with dates', 'Example', 400, 'Product data (illustrative)'),
    (15, 3, 'H2', 'How to set one up', 'How do I set up recurring billing?', 'Steps with screenshots', 'Steps', 300, 'Help docs'),
]

BP_IN = ['Working title', 'Focus keyword', 'Secondary keywords', 'Search intent', 'Format', 'Funnel stage', 'Reader (who it is for)',
         'Goal and call to action', 'Monthly searches', 'Keyword difficulty (0 to 100)', 'Business value (1 to 3)', 'AI Overview on the results page?',
         'Top 3 average words', 'Information gain', 'Information gain detail', 'Must link to (internal)', 'Ask for links from', 'Writer',
         'Due date', 'Status', 'Published URL', 'Notes']
BP_FH = ['Title length', 'Keyword in title?', 'Keyword planned twice?', 'Target words (a guide)', 'Outline sections', 'Outline words planned',
         'Answer first block?', 'Information gain check', 'Brief fields done (of 11)', 'Brief complete', 'Opportunity score (0 to 100)',
         'Priority', 'Hours to write (assumption)', 'Days to due', 'Due status', 'Next step', 'Rank (helper)']
BP_HEAD = BP_IN + BP_FH
CC = {h: L(i + 1) for i, h in enumerate(BP_HEAD)}
BP_F = tuple(range(len(BP_IN) + 1, len(BP_HEAD) + 1))
OB_IN = ['Article (working title)', 'Order', 'Level', 'Heading', 'Question it answers', 'Points and entities to cover', 'Section format', 'Words planned', 'Source to use', 'Notes']
OB_FH = ['Heading length', 'Question heading?', 'Article in pipeline?', 'Builder order (helper)']
OB_HEAD = OB_IN + OB_FH


def bp(h):
    c = CC.get(h, h)
    return f'{BPS}!${c}${BP_FIRST}:${c}${BP_LAST}'


def ob(c):
    return f'{OBS}!${c}${OB_FIRST}:${c}${OB_LAST}'


def d(s):
    return datetime.date.fromisoformat(s) if s else None


def settings_sheet(wb):
    ws = wb.create_sheet(S)
    ws.sheet_view.showGridLines = False
    K.title_block(ws, 'Settings', 'Every rule, weight and list used by this workbook. Change a blue value and every score, length and priority updates.')
    for c, w in zip('ABCDEFGHIJKLMNOPQRSTUVW', [52, 16, 3, 3, 3, 28, 10, 3, 3, 30, 12, 12, 14, 3, 3, 16, 18, 18, 18, 12, 10, 14, 3]):
        ws.column_dimensions[c].width = w
    rows = [
        (4, 'RULES', None, None),
        (5, 'Today (set it to the day you review the sheet)', datetime.date(2026, 11, 25), 'dd mmm yyyy'),
        (6, 'Monthly searches that earn full demand marks', 2000, '#,##0'),
        (7, 'P1: brief now when the score is at least', 70, '0'),
        (8, 'P2: next when at least', 50, '0'),
        (9, 'P3: later when at least (below = P4: park it)', 30, '0'),
        (10, 'Words a writer drafts per hour (assumption)', 500, '0'),
        (11, 'Target length factor vs the top 3 average', 1, '0.00'),
        (12, 'Due soon: days before the due date', 7, '0'),
        (13, 'Writing hours per week for each writer', 15, '0'),
        (14, 'Outline words may differ from the target by', 0.2, '0%'),
    ]
    for r, label, val, fmt in rows:
        a = ws.cell(row=r, column=1, value=label)
        a.font = K.f(10, val is None, K.DEEP if val is None else K.INK)
        if val is not None:
            c = ws.cell(row=r, column=2, value=val)
            c.border, c.fill = K.BORDER, K.INPUT_FILL
            c.font = K.f(10, True, '0000FF')
            c.number_format = fmt
    ws['A16'] = ('Opportunity score = demand weight x MIN(1, searches / full marks) + ease weight x (100 minus difficulty) / 100 '
                 '+ business value weight x value / 3 + information gain weight (when the type counts). Target words = the top 3 average '
                 'x the factor, rounded to 100 and kept inside the band for the format; with no average, the middle of the band. '
                 'Google says it has no preferred word count, so the target is a guide for the writer, not a rule. Every rule, weight, '
                 'band and hour on this tab is an assumption of this kit for you to tune.')
    ws['A16'].font = K.f(9, False, '777777', True)
    ws['A16'].alignment = Alignment(wrap_text=True, vertical='top')
    ws.merge_cells('A16:B27')

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
    table(10, 5, 'FORMAT BANDS (assumptions: words and research hours)', ['Format', 'Min words', 'Max words', 'Research hours'], FORMATS, ['@', '#,##0', '#,##0', '0'], blue=(1, 2, 3))
    table(10, 17, 'INFORMATION GAIN TYPES', ['Type', 'Counts?', 'What it means'], INFOGAIN, blue=(1,))
    ws.merge_cells('L17:N17')
    for i in range(len(INFOGAIN)):
        ws.merge_cells(start_row=18 + i, start_column=12, end_row=18 + i, end_column=14)
        ws.row_dimensions[18 + i].height = 28
    lists = [('P', 'Search intent', INTENTS), ('Q', 'Funnel stage', FUNNEL), ('R', 'Status', STATUS), ('S', 'Writer', WRITERS),
             ('T', 'Yes, No', YNC), ('U', 'Level', LEVELS), ('V', 'Section format', SECFMT)]
    ws['P4'] = 'LISTS (used by the dropdowns)'
    ws['P4'].font = K.f(10, True, K.DEEP)
    for col, head, vals in lists:
        ws[f'{col}5'] = head
        ws[f'{col}5'].font = K.f(9, True, '555555')
        n = 12 if col == 'S' else len(vals)
        for i in range(n):
            c = ws[f'{col}{6 + i}']
            c.value = vals[i] if i < len(vals) else None
            c.fill, c.border, c.font = K.INPUT_FILL, K.BORDER, K.f(10)
    return ws


def pipeline_sheet(wb):
    ws = wb.create_sheet('Brief Pipeline')
    ws.sheet_view.showGridLines = False
    K.title_block(ws, 'Brief pipeline', f'One row per planned article. Rows 5 to {4 + len(ARTS)} are DEMO briefs for Ledgerly, a fictional invoicing app (illustrative numbers). Replace them with your own; 500 rows ready.')
    ws['A2'].font = K.f(10, True, 'B45309')
    ws['A3'] = ('Add the idea, focus keyword and judgement on the left. Grey columns check the brief and score it. Sort by Opportunity score, '
                'then open the Brief Builder tab to get the full brief for one article.')
    ws['A3'].font = K.f(9, False, '666666', True)
    widths = [36, 24, 26, 13, 13, 13, 28, 34, 10, 10, 9, 11, 10, 22, 34, 28, 28, 15, 11, 10, 22, 26,
              7, 9, 18, 10, 8, 9, 34, 26, 8, 8, 10, 22, 9, 9, 18, 44, 8]
    K.header_row(ws, 4, BP_HEAD, formula_cols=BP_F, widths=widths)
    c = CC
    obA, obH = ob('A'), ob('H')
    for r in range(BP_FIRST, BP_LAST + 1):
        i = r - BP_FIRST
        if i < len(ARTS):
            row = list(ARTS[i])
            row[18] = d(row[18])
            if row[20]:
                row[20] = U + row[20]
            for col, v in enumerate(row, 1):
                if v not in (None, ''):
                    ws.cell(row=r, column=col, value=v)
        e = f'A{r}=""'
        g = lambda h: f'{c[h]}{r}'
        f = {}
        f['Title length'] = f'=IF({e},"",LEN(A{r}))'
        f['Keyword in title?'] = f'=IF(OR({e},B{r}=""),"",IF(ISNUMBER(SEARCH(B{r},A{r})),"Yes","No: add it near the start"))'
        f['Keyword planned twice?'] = (f'=IF(OR({e},B{r}=""),"",IF(COUNTIF($B${BP_FIRST}:$B${BP_LAST},B{r})=1,"No",'
                                       f'IF(COUNTIF($B${BP_FIRST}:B{r},B{r})=1,"Yes: a later row repeats it","Yes: an earlier row has it")))')
        lo = f'IFERROR(VLOOKUP(E{r},{FMT_RNG},2,FALSE),800)'
        hi = f'IFERROR(VLOOKUP(E{r},{FMT_RNG},3,FALSE),2000)'
        f['Target words (a guide)'] = f'=IF({e},"",IF(N(M{r})>0,MIN({hi},MAX({lo},ROUND(M{r}*{FACTOR},-2))),ROUND(({lo}+{hi})/2,-2)))'
        f['Outline sections'] = f'=IF({e},"",COUNTIF({obA},A{r}))'
        f['Outline words planned'] = f'=IF({e},"",SUMIF({obA},A{r},{obH}))'
        f['Answer first block?'] = (f'=IF({e},"",IF(OR(L{r}="Yes",D{r}="Informational"),"Yes: answer the main question in the first 40 to 60 words",'
                                    f'"Optional: open with the main benefit"))')
        igc = f'IFERROR(VLOOKUP(N{r},{IG_RNG},2,FALSE),"No")'
        f['Information gain check'] = f'=IF({e},"",IF(N{r}="","Choose an information gain type",IF({igc}="Yes","OK","Add something the top results lack")))'
        secs = g('Outline sections')
        f['Brief fields done (of 11)'] = (f'=IF({e},"",(A{r}<>"")+(B{r}<>"")+(D{r}<>"")+(E{r}<>"")+(G{r}<>"")+(H{r}<>"")'
                                          f'+({g("Information gain check")}="OK")+(P{r}<>"")+(R{r}<>"")+(S{r}<>"")+(N({secs})>=3))')
        f['Brief complete'] = f'=IF({e},"",{g("Brief fields done (of 11)")}/11)'
        f['Opportunity score (0 to 100)'] = (f'=IF({e},"",ROUND({W_DEM}*MIN(1,N(I{r})/{FULL})+{W_EASE}*(100-IF(J{r}="",50,J{r}))/100'
                                             f'+{W_VAL}*IF(K{r}="",2,K{r})/3+{W_IG}*IF({igc}="Yes",1,0),0))')
        sc = g('Opportunity score (0 to 100)')
        f['Priority'] = (f'=IF({e},"",IF(T{r}="Published","Published",IF({g("Keyword planned twice?")}="Yes: an earlier row has it","Rethink: keyword planned twice",'
                         f'IF({sc}>={P1},"P1: brief now",IF({sc}>={P2},"P2: next",IF({sc}>={P3},"P3: later","P4: park it"))))))')
        f['Hours to write (assumption)'] = f'=IF({e},"",ROUND(IFERROR(VLOOKUP(E{r},{FMT_RNG},4,FALSE),3)+{g("Target words (a guide)")}/{WPH},1))'
        f['Days to due'] = f'=IF(OR({e},S{r}=""),"",S{r}-{DATE})'
        dd = g('Days to due')
        f['Due status'] = (f'=IF({e},"",IF(T{r}="Published","Published",IF(S{r}="","No date",IF({dd}<0,"Overdue by "&(-{dd})&" days",'
                           f'IF({dd}<={SOON},"Due in "&{dd}&" days","On track")))))')
        done = g('Brief fields done (of 11)')
        f['Next step'] = (f'=IF({e},"",IF({g("Priority")}="Rethink: keyword planned twice","Merge with the earlier brief or choose a different focus keyword",'
                          f'IF(T{r}="Published","Ask for links from the pages listed, then check Search Console after 28 days",'
                          f'IF(T{r}="Editing","Final checks: facts, sources, title, links, then publish",'
                          f'IF(T{r}="Writing","Editor reviews facts, sources and the information gain",'
                          f'IF(T{r}="Briefed","Writer drafts from the Brief Builder",'
                          f'IF({done}<11,"Finish the brief: "&(11-{done})&" of 11 fields missing","Brief ready: set the status to Briefed and send it")))))))')
        f['Rank (helper)'] = f'=IF(OR({e},T{r}="Published"),"",{sc}+N(I{r})/10000000-ROW()/100000000)'
        for h, v in f.items():
            ws[f'{c[h]}{r}'] = v
    idx = lambda h: BP_HEAD.index(h) + 1
    nf = {9: '#,##0', 10: '0', 11: '0', 13: '#,##0', 19: 'dd mmm yyyy'}
    nf.update({idx('Title length'): '0', idx('Target words (a guide)'): '#,##0', idx('Outline sections'): '0', idx('Outline words planned'): '#,##0',
               idx('Brief fields done (of 11)'): '0', idx('Brief complete'): '0%', idx('Opportunity score (0 to 100)'): '0',
               idx('Hours to write (assumption)'): '0.0', idx('Days to due'): '0', idx('Rank (helper)'): '0.000000'})
    K.style_body(ws, BP_FIRST, BP_LAST, len(BP_HEAD), formula_cols=BP_F, number_formats=nf,
                 wrap_cols=(1, 3, 7, 8, 15, 16, 17, 22, idx('Answer first block?'), idx('Information gain check'), idx('Next step')))
    K.dropdown(ws, f'D{BP_FIRST}:D{BP_LAST}', f'{S}!$P$6:$P$9', 'What the searcher wants: learn, compare, buy or find a site.')
    K.dropdown(ws, f'E{BP_FIRST}:E{BP_LAST}', f'{S}!$J$6:$J$14')
    K.dropdown(ws, f'F{BP_FIRST}:F{BP_LAST}', f'{S}!$Q$6:$Q$8')
    K.dropdown(ws, f'K{BP_FIRST}:K{BP_LAST}', '"1,2,3"', '3 close to a sale or lead, 2 builds trust, 1 loosely related.')
    K.dropdown(ws, f'L{BP_FIRST}:L{BP_LAST}', f'{S}!$T$6:$T$8', 'Search the focus keyword in a private window.')
    K.dropdown(ws, f'N{BP_FIRST}:N{BP_LAST}', f'{S}!$J$18:$J$24', 'What will this article offer that the top results do not?')
    K.dropdown(ws, f'R{BP_FIRST}:R{BP_LAST}', f'{S}!$S$6:$S$17')
    K.dropdown(ws, f'T{BP_FIRST}:T{BP_LAST}', f'{S}!$R$6:$R$10')
    for col in 'IM':
        K.whole_number(ws, f'{col}{BP_FIRST}:{col}{BP_LAST}', 0, 100000000, 'A whole number.')
    K.whole_number(ws, f'J{BP_FIRST}:J{BP_LAST}', 0, 100, 'Keyword difficulty from your keyword tool, 0 to 100.')
    pc = c['Priority']
    pr = f'{pc}{BP_FIRST}:{pc}{BP_LAST}'
    for start, fill, fc in (('P1', '9B2C1F', 'FFFFFF'), ('P2', 'F8D7D3', '9B2C1F'), ('P3', 'FFF4CC', '1F1F1F'), ('P4', 'EEEEEE', '555555'),
                            ('Re', 'FCE5CD', '9B2C1F'), ('Pu', 'B7E4A0', '1F1F1F')):
        ws.conditional_formatting.add(pr, FormulaRule(formula=[f'LEFT({pc}{BP_FIRST},2)="{start}"'], fill=PatternFill('solid', fgColor=fill), font=Font(name=K.FONT, bold=True, color=fc)))
    sc = c['Opportunity score (0 to 100)']
    ws.conditional_formatting.add(f'{sc}{BP_FIRST}:{sc}{BP_LAST}', ColorScaleRule(start_type='num', start_value=0, start_color='FFFFFF', mid_type='num', mid_value=50, mid_color='FFF4CC', end_type='num', end_value=100, end_color='8BC34A'))
    bc = c['Brief complete']
    ws.conditional_formatting.add(f'{bc}{BP_FIRST}:{bc}{BP_LAST}', ColorScaleRule(start_type='num', start_value=0, start_color='F8D7D3', mid_type='num', mid_value=0.7, mid_color='FFF4CC', end_type='num', end_value=1, end_color='B7E4A0'))
    for h, start in (('Keyword in title?', 'No'), ('Keyword planned twice?', 'Yes'), ('Information gain check', 'Ch'), ('Information gain check', 'Ad'), ('Due status', 'Ov')):
        col = c[h]
        ws.conditional_formatting.add(f'{col}{BP_FIRST}:{col}{BP_LAST}', FormulaRule(formula=[f'LEFT({col}{BP_FIRST},2)="{start[:2]}"'], fill=PatternFill('solid', fgColor='F8D7D3'), font=Font(name=K.FONT, bold=True, color='9B2C1F')))
    tl = c['Title length']
    ws.conditional_formatting.add(f'{tl}{BP_FIRST}:{tl}{BP_LAST}', CellIsRule(operator='greaterThan', formula=['60'], font=Font(name=K.FONT, bold=True, color='9B2C1F')))
    ws.column_dimensions[c['Rank (helper)']].hidden = True
    for r in range(BP_FIRST, BP_FIRST + len(ARTS)):
        ws.row_dimensions[r].height = 45
    ws.freeze_panes = 'C5'
    ws.auto_filter.ref = f'A4:{L(len(BP_HEAD))}{BP_LAST}'
    return ws


def outline_sheet(wb):
    ws = wb.create_sheet('Outline Bank')
    ws.sheet_view.showGridLines = False
    K.title_block(ws, 'Outline bank', 'One row per section (H2, H3 or FAQ) for every brief. Choose the article from the dropdown and give each section an order number. The Brief Builder shows the outline for one article.')
    ws['A3'] = 'Write headings as the questions or tasks readers really have. Each section should answer one question well and say where the facts come from.'
    ws['A3'].font = K.f(9, False, '666666', True)
    K.header_row(ws, 4, OB_HEAD, formula_cols=(11, 12, 13, 14), widths=[34, 7, 7, 40, 34, 52, 13, 9, 28, 20, 9, 10, 11, 10])
    for r in range(OB_FIRST, OB_LAST + 1):
        i = r - OB_FIRST
        if i < len(OUT):
            a, o, lv, hd, q, pts, fm, w, src = OUT[i]
            for col, v in enumerate([ARTS[a][0], o, lv, hd, q, pts, fm, w, src], 1):
                if v not in (None, ''):
                    ws.cell(row=r, column=col, value=v)
        e = f'A{r}=""'
        ws[f'K{r}'] = f'=IF(D{r}="","",LEN(D{r}))'
        ws[f'L{r}'] = f'=IF(D{r}="","",IF(RIGHT(TRIM(D{r}),1)="?","Yes","No"))'
        ws[f'M{r}'] = f'=IF({e},"",IF(COUNTIF({bp("A")},A{r})>0,"Yes","No: check the title"))'
        ws[f'N{r}'] = f'=IF(OR({e},A{r}<>{SEL}),"",N(B{r})+ROW()/100000)'
    K.style_body(ws, OB_FIRST, OB_LAST, len(OB_HEAD), formula_cols=(11, 12, 13, 14), number_formats={8: '#,##0', 14: '0.00000'}, wrap_cols=(1, 4, 5, 6, 9, 10))
    K.dropdown(ws, f'A{OB_FIRST}:A{OB_LAST}', bp('A'), 'Working titles from the Brief Pipeline.')
    K.dropdown(ws, f'C{OB_FIRST}:C{OB_LAST}', f'{S}!$U$6:$U$8')
    K.dropdown(ws, f'G{OB_FIRST}:G{OB_LAST}', f'{S}!$V$6:$V$12')
    K.whole_number(ws, f'B{OB_FIRST}:B{OB_LAST}', 1, 200, 'Order of the section in the article: 1, 2, 3 and so on.')
    K.whole_number(ws, f'H{OB_FIRST}:H{OB_LAST}', 0, 20000, 'Planned words for this section.')
    ws.conditional_formatting.add(f'M{OB_FIRST}:M{OB_LAST}', FormulaRule(formula=[f'LEFT(M{OB_FIRST},2)="No"'], fill=PatternFill('solid', fgColor='F8D7D3'), font=Font(name=K.FONT, bold=True, color='9B2C1F')))
    ws.conditional_formatting.add(f'C{OB_FIRST}:C{OB_LAST}', CellIsRule(operator='equal', formula=['"H2"'], font=Font(name=K.FONT, bold=True, color=K.DEEP)))
    ws.column_dimensions['N'].hidden = True
    for r in range(OB_FIRST, OB_FIRST + len(OUT)):
        ws.row_dimensions[r].height = 32
    ws.freeze_panes = 'B5'
    ws.auto_filter.ref = f'A4:M{OB_LAST}'
    return ws


OUT_ROWS = 25


def builder_sheet(wb):
    ws = wb.create_sheet('Brief Builder')
    ws.sheet_view.showGridLines = False
    K.title_block(ws, 'Brief builder', 'Choose an article in the yellow cell. The whole brief, the outline and the hand over checks fill in by themselves. Copy them to your writer.')
    for col, w in zip('ABCDEFGHI', [3, 30, 16, 40, 38, 52, 13, 9, 28]):
        ws.column_dimensions[col].width = w
    ws['B5'] = 'Article'
    ws['B5'].font = K.f(11, True)
    c = ws['C5']
    c.value = A1
    c.fill, c.border, c.font = K.INPUT_FILL, K.BORDER, K.f(11, True, '0000FF')
    ws.merge_cells('C5:F5')
    K.dropdown(ws, 'C5', bp('A'), 'Pick a working title from the Brief Pipeline.')
    m = f'MATCH($C$5,{bp("A")},0)'
    get = lambda h: f'IFERROR(""&INDEX({bp(h)},{m}),"")'
    num = lambda h: f'IFERROR(INDEX({bp(h)},{m}),"")'
    fields = [
        ('Focus keyword', get('Focus keyword'), '@'),
        ('Secondary keywords', get('Secondary keywords'), '@'),
        ('Search intent and format', f'IFERROR(INDEX({bp("Search intent")},{m})&", "&INDEX({bp("Format")},{m}),"")', '@'),
        ('Reader', get('Reader (who it is for)'), '@'),
        ('Goal and call to action', get('Goal and call to action'), '@'),
        ('Target length (a guide)', f'IFERROR("About "&TEXT(INDEX({bp("Target words (a guide)")},{m}),"#,##0")&" words. Cover the topic fully; do not pad.","")', '@'),
        ('Answer first', get('Answer first block?'), '@'),
        ('Information gain', f'IFERROR(INDEX({bp("Information gain")},{m})&": "&INDEX({bp("Information gain detail")},{m}),"")', '@'),
        ('Must link to', get('Must link to (internal)'), '@'),
        ('Ask for links from', get('Ask for links from'), '@'),
        ('Writer and due date', f'IFERROR(INDEX({bp("Writer")},{m})&", due "&TEXT(INDEX({bp("Due date")},{m}),"dd mmm yyyy"),"")', '@'),
        ('Priority and score', f'IFERROR(INDEX({bp("Priority")},{m})&" (score "&INDEX({bp("Opportunity score (0 to 100)")},{m})&")","")', '@'),
        ('Brief complete', num('Brief complete'), '0%'),
        ('Next step', get('Next step'), '@'),
    ]
    for i, (lab, fml, fmt) in enumerate(fields):
        r = 7 + i
        ws.cell(row=r, column=2, value=lab).font = K.f(10, True)
        cell = ws.cell(row=r, column=3, value='=' + fml)
        cell.fill, cell.border, cell.font, cell.number_format = K.FORMULA_FILL, K.BORDER, K.f(10), fmt
        cell.alignment = Alignment(wrap_text=True, vertical='top', horizontal='left')
        ws.merge_cells(start_row=r, start_column=3, end_row=r, end_column=6)
        ws.row_dimensions[r].height = 30
    r0 = 7 + len(fields) + 1      # 22
    ws.cell(row=r0, column=2, value='Brief text (copy to the writer)').font = K.f(11, True, K.DEEP)
    t = (f'=IF(ISNA({m}),"Choose an article in C5","BRIEF: "&$C$5&CHAR(10)&"Focus keyword: "&C7&". Also cover: "&C8&"."&CHAR(10)'
         f'&"Intent and format: "&C9&". Reader: "&C10&"."&CHAR(10)&"Goal: "&C11&"."&CHAR(10)&"Length: "&C12&CHAR(10)'
         f'&"Answer first: "&C13&"."&CHAR(10)&"Information gain: "&C14&"."&CHAR(10)&"Link to: "&C15&". We will ask for links from: "&C16&"."&CHAR(10)'
         f'&"Rules: every fact from an official or primary source, linked in the sentence. Show who wrote it and their experience. '
         f'If AI helps with the draft, a person checks every fact, the title, the meta description and the alt text."&CHAR(10)&"Writer and deadline: "&C17&".")')
    cell = ws.cell(row=r0 + 1, column=2, value=t)
    cell.fill, cell.border, cell.font = K.FORMULA_FILL, K.BORDER, K.f(10)
    cell.alignment = Alignment(wrap_text=True, vertical='top')
    ws.merge_cells(start_row=r0 + 1, start_column=2, end_row=r0 + 9, end_column=6)
    o0 = r0 + 11     # 33
    ws.cell(row=o0 - 1, column=2, value='OUTLINE (from the Outline Bank, in order)').font = K.f(11, True, K.DEEP)
    heads = ['#', 'Level', 'Heading', 'Question it answers', 'Points and entities to cover', 'Format', 'Words', 'Source to use']
    for j, h in enumerate(heads):
        cc = ws.cell(row=o0, column=2 + j, value=h)
        cc.font, cc.fill = K.f(10, True, 'FFFFFF'), K.HEAD_F
        cc.border = K.BORDER
    helper = ob('N')
    for k in range(1, OUT_ROWS + 1):
        r = o0 + k
        mt = f'MATCH(SMALL({helper},{k}),{helper},0)'
        ws.cell(row=r, column=2, value=f'=IF(COUNT({helper})<{k},"",{k})')
        for j, col in enumerate('CDEFGHI'):
            src = 'CDEFGHI'[j]
            mapc = {'C': 'C', 'D': 'D', 'E': 'E', 'F': 'F', 'G': 'G', 'H': 'H', 'I': 'I'}[col]
            cell = ws.cell(row=r, column=3 + j, value=f'=IF(COUNT({helper})<{k},"",IFERROR(INDEX({ob(mapc)},{mt})&"",""))' if col != 'H'
                           else f'=IF(COUNT({helper})<{k},"",IFERROR(INDEX({ob("H")},{mt}),""))')
        for cc in range(2, 10):
            cell = ws.cell(row=r, column=cc)
            cell.fill, cell.border, cell.font = K.FORMULA_FILL, K.BORDER, K.f(9, cc == 4)
            cell.alignment = Alignment(wrap_text=True, vertical='top')
        ws.cell(row=r, column=8).number_format = '#,##0'
    tr = o0 + OUT_ROWS + 1
    ws.cell(row=tr, column=7, value='Total words').font = K.f(10, True)
    cell = ws.cell(row=tr, column=8, value=f'=SUM(H{o0 + 1}:H{o0 + OUT_ROWS})')
    cell.fill, cell.font, cell.number_format = K.FORMULA_FILL, K.f(10, True), '#,##0'
    ws.conditional_formatting.add(f'C{o0 + 1}:C{o0 + OUT_ROWS}', CellIsRule(operator='equal', formula=['"H2"'], font=Font(name=K.FONT, bold=True, color=K.DEEP)))
    q0 = tr + 2
    ws.cell(row=q0, column=2, value='BEFORE YOU HAND IT OVER (automatic checks)').font = K.f(11, True, K.DEEP)
    for j, h in enumerate(['Check', 'Result']):
        cc = ws.cell(row=q0 + 1, column=2 + j, value=h)
        cc.font, cc.fill = K.f(10, True, 'FFFFFF'), K.HEAD_F
    tw = f'INDEX({bp("Target words (a guide)")},{m})'
    checks = [
        ('Focus keyword in the title', f'=IFERROR(IF(INDEX({bp("Keyword in title?")},{m})="Yes","OK","Fix: add the focus keyword"),"")'),
        ('Title 60 characters or fewer', f'=IFERROR(IF(INDEX({bp("Title length")},{m})<=60,"OK","Fix: shorten the title"),"")'),
        ('Focus keyword not planned twice', f'=IFERROR(IF(LEFT(INDEX({bp("Keyword planned twice?")},{m}),2)="No","OK",IF(INDEX({bp("Keyword planned twice?")},{m})="Yes: a later row repeats it","OK: keep this one, retarget the later row","Fix: one page per focus keyword")),"")'),
        ('Information gain chosen', f'=IFERROR(IF(INDEX({bp("Information gain check")},{m})="OK","OK","Fix: add something the top results lack"),"")'),
        ('At least 3 outline sections', f'=IF(COUNT({helper})>=3,"OK","Fix: add sections in the Outline Bank")'),
        ('Outline words close to the target', f'=IFERROR(IF(ABS(H{tr}-{tw})<={TOL}*{tw},"OK","Check: outline has "&TEXT(H{tr},"#,##0")&" words, target "&TEXT({tw},"#,##0")),"")'),
        ('Every section has a question', f'=IF(COUNT({helper})=0,"",IF(COUNTIF(E{o0 + 1}:E{o0 + OUT_ROWS},"?*")>=COUNT({helper}),"OK","Fix: add the question each section answers"))'),
        ('Internal links listed', f'=IFERROR(IF(INDEX({bp("Must link to (internal)")},{m})<>"","OK","Fix: add pages to link to"),"")'),
        ('Writer and due date set', f'=IFERROR(IF(AND(INDEX({bp("Writer")},{m})<>"",INDEX({bp("Due date")},{m})<>""),"OK","Fix: add a writer and a date"),"")'),
    ]
    for i, (lab, fml) in enumerate(checks):
        r = q0 + 2 + i
        ws.cell(row=r, column=2, value=lab).border = K.BORDER
        cell = ws.cell(row=r, column=3, value=fml)
        cell.fill, cell.border, cell.font = K.FORMULA_FILL, K.BORDER, K.f(10, True)
        ws.merge_cells(start_row=r, start_column=3, end_row=r, end_column=5)
    rng = f'C{q0 + 2}:C{q0 + 1 + len(checks)}'
    ws.conditional_formatting.add(rng, CellIsRule(operator='equal', formula=['"OK"'], fill=PatternFill('solid', fgColor='D9F2C4'), font=Font(name=K.FONT, bold=True, color='3D7F12')))
    ws.conditional_formatting.add(rng, FormulaRule(formula=[f'OR(LEFT(C{q0 + 2},3)="Fix",LEFT(C{q0 + 2},5)="Check")'], fill=PatternFill('solid', fgColor='F8D7D3'), font=Font(name=K.FONT, bold=True, color='9B2C1F')))
    return ws, o0, tr, q0


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


def dashboard_sheet(wb):
    ws = wb.create_sheet('Dashboard')
    ws.sheet_view.showGridLines = False
    K.title_block(ws, 'Dashboard', 'Everything here calculates from the other tabs. Nothing to type.')
    for col, w in zip('ABCDEFGHIJK', [46, 12, 3, 38, 24, 8, 16, 12, 15, 16, 3]):
        ws.column_dimensions[col].width = w
    st, pr = bp('Status'), bp('Priority')
    open_ = f'{st},"<>Published",{bp("A")},"?*"'
    kpis = [
        ('Articles in the pipeline', f'=COUNTIF({bp("A")},"?*")', '0'),
        ('Ideas', f'=COUNTIF({st},"Idea")', '0'),
        ('Briefed', f'=COUNTIF({st},"Briefed")', '0'),
        ('Writing', f'=COUNTIF({st},"Writing")', '0'),
        ('Editing', f'=COUNTIF({st},"Editing")', '0'),
        ('Published', f'=COUNTIF({st},"Published")', '0'),
        ('Briefs 100% complete', f'=COUNTIF({bp("Brief complete")},1)', '0'),
        ('Briefs with no information gain yet', f'=COUNTIF({bp("Information gain check")},"<>OK")-COUNTBLANK({bp("Information gain check")})', '0'),
        ('Rows that repeat a focus keyword', f'=COUNTIF({bp("Keyword planned twice?")},"Yes: an earlier*")', '0'),
        ('P1 briefs to write now', f'=COUNTIF({pr},"P1*")', '0'),
        ('Overdue articles', f'=COUNTIF({bp("Due status")},"Overdue*")', '0'),
        ('Due in the next 7 days', f'=COUNTIF({bp("Due status")},"Due in*")', '0'),
        ('Results pages with an AI Overview', f'=COUNTIF({bp("L")},"Yes")', '0'),
        ('Words planned, not yet published', f'=SUMIFS({bp("Target words (a guide)")},{open_})', '#,##0'),
        ('Writing hours planned (assumption)', f'=SUMIFS({bp("Hours to write (assumption)")},{open_})', '0.0'),
        ('Average opportunity score', f'=IFERROR(AVERAGE({bp("Opportunity score (0 to 100)")}),"")', '0'),
    ]
    ws['A4'] = 'KEY NUMBERS'
    ws['A4'].font = K.f(10, True, K.DEEP)
    for i, (label, fml, fmt) in enumerate(kpis):
        r = 5 + i
        ws.cell(row=r, column=1, value=label).font = K.f(10)
        cell = ws.cell(row=r, column=2, value=fml)
        cell.number_format, cell.font, cell.fill, cell.border = fmt, K.f(11, True), K.FORMULA_FILL, K.BORDER
        cell.alignment = Alignment(horizontal='right')
    ws['D4'] = 'TOP 10 BRIEFS (highest opportunity score, not yet published)'
    ws['D4'].font = K.f(10, True, K.DEEP)
    heads = ['Working title', 'Focus keyword', 'Score', 'Priority', 'Status', 'Writer', 'Due status']
    cols = ['A', 'B', 'Opportunity score (0 to 100)', 'Priority', 'Status', 'Writer', 'Due status']
    for j, h in enumerate(heads):
        cell = ws.cell(row=5, column=4 + j, value=h)
        cell.font, cell.fill = K.f(10, True, 'FFFFFF'), K.HEAD_F
    rk = bp('Rank (helper)')
    for k in range(1, 11):
        r = 5 + k
        mt = f'MATCH(LARGE({rk},{k}),{rk},0)'
        for j, col in enumerate(cols):
            cell = ws.cell(row=r, column=4 + j, value=f'=IFERROR(INDEX({bp(col)},{mt}),"")')
            cell.border, cell.fill, cell.font = K.BORDER, K.FORMULA_FILL, K.f(9, j == 0)
            cell.alignment = Alignment(wrap_text=j in (0, 1, 3), vertical='top')
            cell.number_format = '0' if j == 2 else '@'
        ws.row_dimensions[r].height = 28
    top = 24
    ws.cell(row=top - 1, column=1, value='PIPELINE BY STATUS').font = K.f(10, True, K.DEEP)
    for j, h in enumerate(['Status', 'Articles', '', 'Words planned']):
        if h:
            cell = ws.cell(row=top, column=1 + j, value=h)
            cell.font, cell.fill = K.f(10, True, 'FFFFFF'), K.HEAD_F
    for i in range(len(STATUS)):
        r = top + 1 + i
        ws.cell(row=r, column=1, value=f'={S}!R{6 + i}')
        ws.cell(row=r, column=2, value=f'=COUNTIF({st},A{r})')
        ws.cell(row=r, column=4, value=f'=SUMIF({st},A{r},{bp("Target words (a guide)")})')
        for cc in (1, 2, 4):
            cell = ws.cell(row=r, column=cc)
            cell.border, cell.fill, cell.font = K.BORDER, K.FORMULA_FILL, K.f(10, cc == 1)
        ws.cell(row=r, column=4).number_format = '#,##0'
    w0 = top + len(STATUS) + 4
    ws.cell(row=w0 - 1, column=1, value='WRITER LOAD (open articles; hours are assumptions)').font = K.f(10, True, K.DEEP)
    for j, h in enumerate(['Writer', 'Open articles', '', 'Hours planned', 'Weeks of work', 'Status']):
        if h:
            cell = ws.cell(row=w0, column=1 + j, value=h)
            cell.font, cell.fill = K.f(10, True, 'FFFFFF'), K.HEAD_F
    for i in range(len(WRITERS)):
        r = w0 + 1 + i
        ws.cell(row=r, column=1, value=f'={S}!S{6 + i}')
        ws.cell(row=r, column=2, value=f'=COUNTIFS({bp("Writer")},A{r},{st},"<>Published")')
        ws.cell(row=r, column=4, value=f'=SUMIFS({bp("Hours to write (assumption)")},{bp("Writer")},A{r},{st},"<>Published")')
        ws.cell(row=r, column=5, value=f'=IF({WEEKLY}=0,"",ROUND(D{r}/{WEEKLY},1))')
        ws.cell(row=r, column=6, value=f'=IF(B{r}=0,"Free",IF(E{r}>4,"Heavy: more than 4 weeks","OK"))')
        for cc in (1, 2, 4, 5, 6):
            cell = ws.cell(row=r, column=cc)
            cell.border, cell.fill, cell.font = K.BORDER, K.FORMULA_FILL, K.f(10, cc == 1)
        ws.cell(row=r, column=4).number_format = '0.0'
        ws.cell(row=r, column=5).number_format = '0.0'
    ws.conditional_formatting.add(f'F{w0 + 1}:F{w0 + len(WRITERS)}', FormulaRule(formula=[f'LEFT(F{w0 + 1},5)="Heavy"'], fill=PatternFill('solid', fgColor='F8D7D3'), font=Font(name=K.FONT, bold=True, color='9B2C1F')))
    chart(ws, 'Articles by status', 'Articles', 1, [2], top + 1, top + len(STATUS), 'H18', [K.GREEN], False, w=15)
    chart(ws, 'Writing hours planned by writer', 'Hours (assumption)', 1, [4], w0 + 1, w0 + len(WRITERS), 'H34', ['E07A5F'], True, w=15)
    return ws, top, w0


def build(path, asset, url):
    wb = K.new_book()
    pipeline_sheet(wb)
    outline_sheet(wb)
    builder_sheet(wb)
    dashboard_sheet(wb)
    settings_sheet(wb)
    K.prompts_sheet(wb, asset['prompts'], url)
    K.checklist_sheet(wb, list(asset['checklist']))
    K.sources_sheet(wb, asset['sources'], [
        ('Demo data', 'Ledgerly, every URL and every article in the demo are fictional (.example domain). Searches, difficulty, word counts and dates are illustrative, not real data.', ''),
        ('Weights, bands and hours', 'Score weights, length bands per format, research hours, words per hour and the 40 to 60 word answer first habit are assumptions of this kit. Tune them on Settings.', ''),
        ('Word count', 'Google says it has no preferred word count, so the target length is only a guide for the writer.', 'https://developers.google.com/search/docs/fundamentals/creating-helpful-content'),
        ('Information gain', 'Google asks whether content provides original information, reporting, research or analysis, and substantial value compared with other pages in search results.', 'https://developers.google.com/search/docs/fundamentals/creating-helpful-content'),
        ('AI assisted drafts', 'Google says to fact check and review all AI generated content before publishing, including titles, meta descriptions, structured data and alt text, and warns that many pages without added value may be scaled content abuse.', 'https://developers.google.com/search/docs/fundamentals/using-gen-ai-content'),
    ])
    K.start_here(
        wb, 'Content Brief Kit',
        [
            'This workbook turns article ideas into briefs a writer can follow. Each row in the Brief Pipeline gets a target length band, an answer first rule, an information gain check, a completeness score, an opportunity score, a priority, writing hours and the next step.',
            f'The Outline Bank holds the H2, H3 and FAQ sections for every brief, and the Brief Builder assembles the full brief, the outline and nine hand over checks for one article. A worked demo for a fictional invoicing app ({len(ARTS)} briefs, {len(OUT)} outline sections) shows every formula working.',
        ],
        [
            ('Brief Pipeline', 'One row per article, 500 rows ready. Title checks, duplicate keywords, target words, outline totals, answer first, information gain, completeness, score, priority, hours, due status, next step.'),
            ('Outline Bank', 'H2, H3 and FAQ sections for every brief, with the question each one answers, points and entities, format, words and source.'),
            ('Brief Builder', 'Pick one article: the brief, a copy ready brief text, the ordered outline and nine automatic checks.'),
            ('Dashboard', '16 key numbers, the top 10 briefs, pipeline by status and writer load, with two charts.'),
            ('Settings', 'Score weights, length bands and research hours per format, information gain types, rules and lists.'),
            ('AI Prompts', 'Prompts for ChatGPT, Claude or Gemini to research, outline, check and improve briefs.'),
            ('Checklist', 'The brief process as a tick list with automatic progress.'),
            ('Sources', 'Where facts come from and which numbers are assumptions.'),
        ],
        [
            'Look at the demo on Brief Pipeline, Outline Bank, Brief Builder and Dashboard. Then clear the yellow demo cells on Brief Pipeline and Outline Bank.',
            'On Settings, set today\'s date, the searches that earn full marks (a strong keyword for your site), words per hour and the format bands.',
            'Add each idea with its focus keyword, intent, format, reader and goal. Add searches and difficulty from your keyword tool.',
            'Search each focus keyword: note whether an AI Overview shows and the average length of the top 3 results.',
            'Choose the information gain: what this article will offer that the top results do not.',
            'Write the outline in the Outline Bank, one row per section, with the question it answers and the source to use.',
            'Open the Brief Builder, choose the article, fix anything the checks flag, then copy the brief text to the writer and set the status to Briefed.',
        ],
        url,
    )
    order = ['Start Here', 'Brief Pipeline', 'Outline Bank', 'Brief Builder', 'Dashboard', 'Settings', 'AI Prompts', 'Checklist', 'Sources']
    wb._sheets = [wb[n] for n in order]
    wb.active = 0
    for ws in wb.worksheets:
        ws.sheet_properties.tabColor = K.GREEN if ws.title in order[:5] else 'A6EF39'
    wb.save(path)


PREVIEW = {'sheet': 'Brief Pipeline', 'header_row': 4, 'rows': 12,
           'cols': [1, 2, 5, 14, len(BP_IN) + 4, len(BP_IN) + 10, len(BP_IN) + 11, len(BP_IN) + 12],
           'formula_idx': [4, 5, 6, 7]}


def check(wb):
    """Assert the worked examples used in the guide."""
    a = wb['Brief Pipeline']
    v = lambda h, r: a[f'{CC[h]}{r}'].value
    r = 5   # How to make an invoice as a freelancer
    assert v('Keyword in title?', r) == 'Yes' and v('Title length', r) == 38, v('Title length', r)
    assert v('Keyword planned twice?', r) == 'Yes: a later row repeats it'
    assert v('Target words (a guide)', r) == 1900 and v('Outline sections', r) == 10 and v('Outline words planned', r) == 1930, (v('Target words (a guide)', r), v('Outline words planned', r))
    assert v('Information gain check', r) == 'OK' and v('Brief fields done (of 11)', r) == 11 and v('Brief complete', r) == 1
    assert v('Opportunity score (0 to 100)', r) == 92 and v('Priority', r) == 'P1: brief now', v('Opportunity score (0 to 100)', r)
    assert abs(v('Hours to write (assumption)', r) - 6.8) < 1e-9 and v('Days to due', r) == 9 and v('Due status', r) == 'On track'
    assert v('Next step', r) == 'Writer drafts from the Brief Builder'
    r = 7   # Invoice vs bill
    assert v('Target words (a guide)', r) == 1200 and v('Brief fields done (of 11)', r) == 6, (v('Target words (a guide)', r), v('Brief fields done (of 11)', r))
    assert v('Opportunity score (0 to 100)', r) == 41 and v('Priority', r) == 'P3: later', v('Opportunity score (0 to 100)', r)
    assert v('Information gain check', r) == 'Add something the top results lack'
    assert v('Next step', r) == 'Finish the brief: 5 of 11 fields missing', v('Next step', r)
    r = 12  # Excel invoice: duplicate keyword
    assert v('Keyword planned twice?', r) == 'Yes: an earlier row has it' and v('Priority', r) == 'Rethink: keyword planned twice'
    assert v('Due status', 8) == 'Overdue by 5 days' and v('Due status', 9) == 'Due in 3 days', (v('Due status', 8), v('Due status', 9))
    assert v('Priority', 19) == 'Published'
    b = wb['Brief Builder']
    assert b['C7'].value == 'how to make an invoice' and b['C12'].value.startswith('About 1,900 words'), (b['C7'].value, b['C12'].value)
    assert b['D34'].value == 'How to make an invoice in 6 steps' and b['D43'].value == 'What is the difference between an invoice and a bill?', (b['D34'].value, b['D43'].value)
    assert b['B44'].value in (None, '') and b['H59'].value == 1930, (b['B44'].value, b['H59'].value)
    res = [b.cell(row=r, column=3).value for r in range(63, 72)]
    assert all(str(x).startswith('OK') for x in res) and res[2].startswith('OK: keep'), res
    assert b['B23'].value.startswith('BRIEF: How to make an invoice as a freelancer')
    dsh = wb['Dashboard']
    vals = {dsh.cell(row=r, column=1).value: dsh.cell(row=r, column=2).value for r in range(5, 21)}
    assert vals['Articles in the pipeline'] == len(ARTS) and vals['Rows that repeat a focus keyword'] == 1 and vals['Overdue articles'] == 1, vals
    assert dsh['D6'].value == A1, dsh['D6'].value
    return vals
