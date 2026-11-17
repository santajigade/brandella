"""Shared helpers for the SEO and AEO asset kits (Excel workbooks).

Style rules: Arial everywhere, light yellow = cells you type in, light grey = formulas (do not edit),
dark header rows, frozen headers, filters, data validation dropdowns. No em or en dashes in any text.
"""
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.utils import get_column_letter

FONT = 'Arial'
GREEN = '6CC82A'
DEEP = '4F9D1A'
INK = '1F1F1F'
INPUT_FILL = PatternFill('solid', fgColor='FFF8E1')
FORMULA_FILL = PatternFill('solid', fgColor='F2F2F2')
HEAD_IN = PatternFill('solid', fgColor='2B2B2B')
HEAD_F = PatternFill('solid', fgColor='4F9D1A')
SOFT = PatternFill('solid', fgColor='EEF8E6')
thin = Side(style='thin', color='DDDDDD')
BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)


def f(size=10, bold=False, color=INK, italic=False):
    return Font(name=FONT, size=size, bold=bold, color=color, italic=italic)


def new_book():
    wb = Workbook()
    wb.remove(wb.active)
    return wb


def title_block(ws, title, subtitle, width_cols=8):
    ws['A1'] = title
    ws['A1'].font = f(16, True, DEEP)
    ws['A2'] = subtitle
    ws['A2'].font = f(10, False, '555555', True)
    ws.row_dimensions[1].height = 26


def header_row(ws, row, headers, formula_cols=(), widths=None):
    """headers: list of names. formula_cols: 1 based column numbers that hold formulas (green header)."""
    for i, h in enumerate(headers, start=1):
        c = ws.cell(row=row, column=i, value=h)
        c.font = f(10, True, 'FFFFFF')
        c.fill = HEAD_F if i in formula_cols else HEAD_IN
        c.alignment = Alignment(wrap_text=True, vertical='center')
        c.border = BORDER
        if widths:
            ws.column_dimensions[get_column_letter(i)].width = widths[i - 1]
    ws.row_dimensions[row].height = 34


def style_body(ws, first_row, last_row, ncols, formula_cols=(), number_formats=None, wrap_cols=()):
    number_formats = number_formats or {}
    for r in range(first_row, last_row + 1):
        for col in range(1, ncols + 1):
            c = ws.cell(row=r, column=col)
            c.font = f(10)
            c.border = BORDER
            c.fill = FORMULA_FILL if col in formula_cols else INPUT_FILL
            c.alignment = Alignment(vertical='top', wrap_text=col in wrap_cols)
            if col in number_formats:
                c.number_format = number_formats[col]


def dropdown(ws, rng, formula1, prompt=None):
    dv = DataValidation(type='list', formula1=formula1, allow_blank=True, showDropDown=False)
    if prompt:
        dv.promptTitle = 'Choose a value'
        dv.prompt = prompt
        dv.showInputMessage = True
    ws.add_data_validation(dv)
    dv.add(rng)


def whole_number(ws, rng, lo, hi, msg):
    dv = DataValidation(type='whole', operator='between', formula1=str(lo), formula2=str(hi), allow_blank=True)
    dv.error = msg
    dv.errorTitle = 'Check this value'
    dv.showErrorMessage = True
    ws.add_data_validation(dv)
    dv.add(rng)


def start_here(wb, title, intro, tabs, steps, url, legend_extra=None):
    ws = wb.create_sheet('Start Here', 0)
    ws.sheet_view.showGridLines = False
    ws.column_dimensions['A'].width = 4
    ws.column_dimensions['B'].width = 28
    ws.column_dimensions['C'].width = 90
    ws['B2'] = title
    ws['B2'].font = f(20, True, DEEP)
    ws['B3'] = 'A free resource from Brandella Journal. Free for personal and client work.'
    ws['B3'].font = f(10, False, '666666', True)
    ws['B4'] = url
    ws['B4'].hyperlink = url
    ws['B4'].font = f(10, False, '1A56A8')
    r = 6
    for p in intro:
        ws.cell(row=r, column=2, value=p).font = f(11)
        ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=3)
        ws.cell(row=r, column=2).alignment = Alignment(wrap_text=True, vertical='top')
        ws.row_dimensions[r].height = 32
        r += 1
    r += 1
    ws.cell(row=r, column=2, value='Colour legend').font = f(12, True)
    r += 1
    ws.cell(row=r, column=2, value='Light yellow cells').fill = INPUT_FILL
    ws.cell(row=r, column=3, value='You type or choose these. Dropdowns appear when you click the cell.')
    r += 1
    ws.cell(row=r, column=2, value='Light grey cells').fill = FORMULA_FILL
    ws.cell(row=r, column=3, value='Formulas. They calculate by themselves. Please do not type over them.')
    r += 1
    c = ws.cell(row=r, column=2, value='Green header')
    c.fill = HEAD_F
    c.font = f(10, True, 'FFFFFF')
    ws.cell(row=r, column=3, value='A column that calculates automatically.')
    r += 1
    for k, v in (legend_extra or []):
        ws.cell(row=r, column=2, value=k)
        ws.cell(row=r, column=3, value=v)
        r += 1
    r += 1
    ws.cell(row=r, column=2, value='Tabs in this workbook').font = f(12, True)
    r += 1
    for name, desc in tabs:
        ws.cell(row=r, column=2, value=name).font = f(10, True)
        ws.cell(row=r, column=3, value=desc)
        ws.cell(row=r, column=3).alignment = Alignment(wrap_text=True, vertical='top')
        r += 1
    r += 1
    ws.cell(row=r, column=2, value='How to use it').font = f(12, True)
    r += 1
    for i, s in enumerate(steps, 1):
        ws.cell(row=r, column=2, value=f'Step {i}').font = f(10, True, DEEP)
        ws.cell(row=r, column=3, value=s)
        ws.cell(row=r, column=3).alignment = Alignment(wrap_text=True, vertical='top')
        ws.row_dimensions[r].height = 30
        r += 1
    for row in ws.iter_rows(min_row=5, max_row=r, min_col=2, max_col=3):
        for c in row:
            if c.font.name != FONT:
                c.font = f(10, c.font.bold)
    return ws


def prompts_sheet(wb, prompts, url):
    ws = wb.create_sheet('AI Prompts')
    ws.sheet_view.showGridLines = False
    title_block(ws, 'AI prompts', 'Copy a prompt into ChatGPT, Claude or Gemini. Replace the parts in [square brackets]. Always check the output against real data.')
    header_row(ws, 4, ['#', 'Prompt name', 'Prompt (copy this)', 'Tip'], widths=[5, 30, 100, 40])
    for i, p in enumerate(prompts, 1):
        r = 4 + i
        ws.cell(row=r, column=1, value=i)
        ws.cell(row=r, column=2, value=p['t'])
        ws.cell(row=r, column=3, value=p['p'].strip())
        ws.cell(row=r, column=4, value=p.get('tip', ''))
        for col in range(1, 5):
            c = ws.cell(row=r, column=col)
            c.font = f(10, col == 2)
            c.alignment = Alignment(wrap_text=True, vertical='top')
            c.border = BORDER
        ws.row_dimensions[r].height = max(45, 15 * (p['p'].count('\n') + 2 + len(p['p']) // 110))
    ws.freeze_panes = 'A5'


def checklist_sheet(wb, items):
    ws = wb.create_sheet('Checklist')
    ws.sheet_view.showGridLines = False
    title_block(ws, 'Checklist', 'Choose Yes in column C when a step is done. Progress updates by itself.')
    header_row(ws, 4, ['#', 'Step', 'Done?'], formula_cols=(), widths=[5, 95, 12])
    n = len(items)
    for i, it in enumerate(items, 1):
        r = 4 + i
        ws.cell(row=r, column=1, value=i).font = f(10)
        c = ws.cell(row=r, column=2, value=it)
        c.font = f(10)
        c.alignment = Alignment(wrap_text=True)
        d = ws.cell(row=r, column=3, value='No')
        d.fill = INPUT_FILL
        d.font = f(10)
        for col in (1, 2, 3):
            ws.cell(row=r, column=col).border = BORDER
    dropdown(ws, f'C5:C{4 + n}', '"Yes,No"')
    pr = 6 + n
    ws.cell(row=pr, column=2, value='Progress').font = f(11, True)
    c = ws.cell(row=pr, column=3, value=f'=COUNTIF(C5:C{4 + n},"Yes")/{n}')
    c.number_format = '0%'
    c.font = f(12, True, DEEP)
    c.fill = FORMULA_FILL
    from openpyxl.formatting.rule import CellIsRule
    ws.conditional_formatting.add(f'C5:C{4 + n}', CellIsRule(operator='equal', formula=['"Yes"'], fill=PatternFill('solid', fgColor='D9F2C4')))


def sources_sheet(wb, sources, notes):
    ws = wb.create_sheet('Sources')
    ws.sheet_view.showGridLines = False
    title_block(ws, 'Sources and assumptions', 'Where the facts and default settings in this workbook come from.')
    header_row(ws, 4, ['Item', 'Detail', 'Link'], widths=[34, 80, 60])
    r = 5
    for t, d, u in notes + [(s['t'], 'Source', s['url']) for s in sources]:
        ws.cell(row=r, column=1, value=t).font = f(10, True)
        ws.cell(row=r, column=2, value=d).font = f(10)
        c = ws.cell(row=r, column=3, value=u)
        if u.startswith('http'):
            c.hyperlink = u
            c.font = f(10, False, '1A56A8')
        for col in (1, 2, 3):
            ws.cell(row=r, column=col).alignment = Alignment(wrap_text=True, vertical='top')
            ws.cell(row=r, column=col).border = BORDER
        r += 1
