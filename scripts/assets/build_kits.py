"""Build the downloadable kits for the SEO and AEO Growth Assets library.

For every asset YAML with `kit: true` and a matching kit_<slug>.py module this writes, into
public/resources/seo-aeo-assets/kits/:
  brandella-<slug>-template.xlsx   Excel workbook (formulas recalculated with LibreOffice)
  brandella-<slug>-guide.pdf       Full guide
  brandella-<slug>-checklist.pdf   Printable checklist
  brandella-<slug>-ai-prompts.md   Prompt pack
  brandella-<slug>-kit.zip         All of the above
plus brandella-seo-aeo-assets-all-kits.zip and a preview JSON per asset in src/data/seo-assets/previews/.

Run from the repo root:  python3 scripts/assets/build_kits.py
Needs: openpyxl, pyyaml, playwright (chromium), LibreOffice (soffice) for recalculation.
"""
import importlib, json, os, re, subprocess, sys, zipfile, html, datetime
from pathlib import Path
import yaml
from openpyxl import load_workbook

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).parent))
DATA = ROOT / 'src/data/seo-assets'
OUT = ROOT / 'public/resources/seo-aeo-assets/kits'
PREV = DATA / 'previews'
SITE = 'https://brandella.in'
RECALC = os.environ.get('RECALC', str(Path(__file__).parent / 'recalc.py'))

index = json.loads((DATA / 'index.json').read_text())
meta = {a['slug']: a for a in index['assets']}


def page_url(slug):
    return f'{SITE}/resources/seo-aeo-assets/{slug}/'


def abs_links(s):
    return re.sub(r'href="/', f'href="{SITE}/', s)


def recalc(path):
    out = subprocess.run([sys.executable, RECALC, str(path), '90'], capture_output=True, text=True)
    res = json.loads(out.stdout[out.stdout.find('{'):]) if '{' in out.stdout else {'error': out.stderr}
    if res.get('status') != 'success' or res.get('total_errors'):
        raise SystemExit(f'Recalc problem in {path}: {res}')
    return res


PDF_CSS = """
@page { size: A4; margin: 18mm 16mm 20mm; }
body { font-family: 'Open Sans', Arial, sans-serif; color: #1f1f1f; font-size: 10.5pt; line-height: 1.55; }
h1 { font-size: 26pt; line-height: 1.15; margin: 0 0 10px; }
h2 { font-size: 15pt; margin: 22px 0 8px; color: #1f1f1f; border-bottom: 2px solid #6cc82a; padding-bottom: 4px; page-break-after: avoid; }
h3 { font-size: 12pt; margin: 14px 0 6px; page-break-after: avoid; }
a { color: #3d7f12; text-decoration: none; }
.cover { height: 250mm; display: flex; flex-direction: column; justify-content: center; page-break-after: always; }
.brand { font-size: 14pt; font-weight: 700; color: #555; } .brand span { color: #6cc82a; }
.kicker { display: inline-block; background: #eef8e6; color: #3d7f12; font-weight: 700; font-size: 9pt; letter-spacing: .5px; text-transform: uppercase; padding: 4px 10px; border-radius: 12px; margin: 30px 0 14px; }
.lead { font-size: 12.5pt; color: #444; max-width: 150mm; }
.meta { margin-top: 30px; color: #666; font-size: 9.5pt; }
table { width: 100%; border-collapse: collapse; margin: 8px 0 12px; font-size: 9.5pt; page-break-inside: avoid; }
th { background: #2b2b2b; color: #fff; text-align: left; padding: 6px 8px; }
td { border-bottom: 1px solid #e3e3e3; padding: 6px 8px; vertical-align: top; }
.box { border: 1px solid #d6edc4; background: #f6faf1; border-radius: 8px; padding: 10px 14px; margin: 10px 0; page-break-inside: avoid; }
.prompt { border: 1px solid #e3e3e3; border-radius: 6px; margin: 8px 0; page-break-inside: avoid; }
.prompt b { display: block; background: #f5f5f5; padding: 5px 10px; font-size: 10pt; }
.prompt pre { margin: 0; padding: 8px 10px; white-space: pre-wrap; font-family: Consolas, monospace; font-size: 9pt; }
ol.steps li { margin-bottom: 6px; }
.check li { list-style: none; margin: 0 0 7px -20px; } .check li::before { content: ""; display: inline-block; width: 11px; height: 11px; border: 1.5px solid #4f9d1a; border-radius: 2px; margin-right: 9px; vertical-align: -1px; }
.faq b { display: block; margin-top: 8px; }
.foot { margin-top: 24px; font-size: 9pt; color: #777; }
"""


def esc(s):
    return html.escape(str(s))


def guide_html(slug, a):
    m = meta[slug]
    date = datetime.date.fromisoformat(str(a['updated'])).strftime('%d %B %Y')
    parts = [f'<div class="cover"><div class="brand">Brandella <span>Journal</span></div>'
             f'<div class="kicker">Free SEO and AEO Growth Asset {m["n"]:02d} of 36</div>'
             f'<h1>{esc(a["h1"])}</h1><p class="lead">{esc(a["description"])}</p>'
             f'<p class="meta">Updated {date}<br>Online version and downloads: <a href="{page_url(slug)}">{page_url(slug)}</a><br>'
             f'Free for personal and client work. By Santaji Gadepatil, Founder of Brandella Journal.</p></div>']
    parts.append('<h2>What is in this kit</h2><table><tr><th>Item</th><th>What it is</th></tr>' +
                 ''.join(f'<tr><td><b>{esc(k["t"])}</b></td><td>{esc(k["d"])}</td></tr>' for k in a.get('kitContents', [])) + '</table>')
    parts.append(''.join(f'<p>{p}</p>' for p in a['intro']))
    nm = ' '.join(w if w.isupper() else w.lower() for w in m['name'].split())
    parts.append(f'<h2>How to use this {esc(nm)} kit</h2><ol class="steps">' +
                 ''.join(f'<li><b>{esc(s["t"])}.</b> {s["d"]}</li>' for s in a['steps']) + '</ol>')
    for s in a.get('sections', []):
        body = s['html'].replace('class="ra-sheet-wrap"', '').replace('class="ra-sheet"', '')
        parts.append(f'<h2>{esc(s["h"])}</h2>{body}')
    parts.append('<h2>AI prompts</h2><p>Replace the parts in [square brackets]. Always check the output against real data.</p>' +
                 ''.join(f'<div class="prompt"><b>{i}. {esc(p["t"])}</b><pre>{esc(p["p"].strip())}</pre></div>' for i, p in enumerate(a['prompts'], 1)))
    parts.append('<h2>Checklist</h2><ul class="check">' + ''.join(f'<li>{esc(c)}</li>' for c in a['checklist']) + '</ul>')
    parts.append('<h2>Frequently asked questions</h2><div class="faq">' + ''.join(f'<b>{esc(f["q"])}</b><p>{f["a"]}</p>' for f in a['faq']) + '</div>')
    parts.append('<h2>Sources</h2><ul>' + ''.join(f'<li><a href="{esc(s["url"])}">{esc(s["t"])}</a><br><span style="color:#777;font-size:9pt">{esc(s["url"])}</span></li>' for s in a['sources']) + '</ul>')
    parts.append(f'<p class="foot">More free templates, checklists and prompts: {SITE}/resources/seo-aeo-assets/</p>')
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{PDF_CSS}</style></head><body>{abs_links("".join(parts))}</body></html>'


def checklist_html(slug, a):
    m = meta[slug]
    items = ''.join(f'<li>{esc(c)}</li>' for c in a['checklist'])
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>{PDF_CSS} body{{font-size:11pt}} .check li{{margin-bottom:11px}}</style></head><body>'
            f'<div class="brand">Brandella <span>Journal</span></div><h1 style="font-size:20pt;margin-top:10px">{esc(m["name"])} checklist</h1>'
            f'<p style="color:#666">Project: ______________________________ &nbsp; Date: ______________</p>'
            f'<ul class="check">{items}</ul><p class="foot">Full kit and guide: {page_url(slug)}</p></body></html>')


def prompts_md(slug, a):
    lines = [f'# {meta[slug]["name"]}: AI prompt pack', '', f'From Brandella Journal, free to use. Full guide: {page_url(slug)}', '',
             'Replace the parts in [square brackets] before you paste a prompt into ChatGPT, Claude or Gemini. Always check the output against real data.', '']
    for i, p in enumerate(a['prompts'], 1):
        lines += [f'## {i}. {p["t"]}', '', '```', p['p'].strip(), '```', '']
    return '\n'.join(lines)


def preview(slug, xlsx, spec):
    wb = load_workbook(xlsx, data_only=True)
    ws = wb[spec['sheet']]
    heads = [ws.cell(row=spec['header_row'], column=c).value for c in spec['cols']]
    rows = []
    for r in range(spec['header_row'] + 1, spec['header_row'] + 1 + spec['rows']):
        row = []
        for c in spec['cols']:
            v = ws.cell(row=r, column=c).value
            if isinstance(v, float) and v.is_integer():
                v = int(v)
            row.append('' if v is None else v)
        rows.append(row)
    PREV.mkdir(parents=True, exist_ok=True)
    (PREV / f'{slug}.json').write_text(json.dumps({'sheet': spec['sheet'], 'columns': heads, 'rows': rows, 'formulaCols': spec.get('formula_idx', [])}, indent=1))
    return wb


def main():
    from playwright.sync_api import sync_playwright
    OUT.mkdir(parents=True, exist_ok=True)
    built = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page()
        for path in sorted(DATA.glob('*.yaml')):
            slug = path.stem
            a = yaml.safe_load(path.read_text())
            if not a.get('kit'):
                continue
            mod = importlib.import_module('kit_' + slug.replace('-', '_'))
            base = OUT / f'brandella-{slug}'
            xlsx = Path(f'{base}-template.xlsx')
            mod.build(str(xlsx), a, page_url(slug))
            print(slug, 'recalc', recalc(xlsx).get('total_formulas'), 'formulas')
            wb = preview(slug, xlsx, mod.PREVIEW)
            if hasattr(mod, 'check'):
                mod.check(wb)
            for kind, htmlfn in (('guide', guide_html), ('checklist', checklist_html)):
                page.set_content(htmlfn(slug, a), wait_until='load')
                page.pdf(path=f'{base}-{kind}.pdf', format='A4', print_background=True,
                         display_header_footer=kind == 'guide', header_template='<span></span>',
                         footer_template='<div style="font-size:8px;color:#888;width:100%;text-align:center">Brandella Journal &middot; brandella.in &middot; page <span class="pageNumber"></span> of <span class="totalPages"></span></div>',
                         margin={'top': '16mm', 'bottom': '18mm', 'left': '14mm', 'right': '14mm'})
            Path(f'{base}-ai-prompts.md').write_text(prompts_md(slug, a))
            readme = (f'{meta[slug]["name"]} kit from Brandella Journal\n\nFiles:\n'
                      f'  brandella-{slug}-template.xlsx   Excel workbook (also opens in Google Sheets)\n'
                      f'  brandella-{slug}-guide.pdf       Full guide\n'
                      f'  brandella-{slug}-checklist.pdf   Printable checklist\n'
                      f'  brandella-{slug}-ai-prompts.md   AI prompt pack\n\n'
                      f'Start with the "Start Here" tab in the workbook.\nOnline version: {page_url(slug)}\n'
                      'Free for personal and client work.\n')
            files = [f'{base}-template.xlsx', f'{base}-guide.pdf', f'{base}-checklist.pdf', f'{base}-ai-prompts.md']
            with zipfile.ZipFile(f'{base}-kit.zip', 'w', zipfile.ZIP_DEFLATED) as z:
                for fp in files:
                    z.write(fp, f'brandella-{slug}-kit/{Path(fp).name}')
                z.writestr(f'brandella-{slug}-kit/README.txt', readme)
            built.append((meta[slug], files, readme))
        browser.close()
    built.sort(key=lambda x: x[0]['n'])
    lines = ['Brandella Journal: free SEO and AEO Growth Assets', '', f'{len(built)} of 36 kits included. New kits are added regularly at {SITE}/resources/seo-aeo-assets/', '']
    with zipfile.ZipFile(OUT / 'brandella-seo-aeo-assets-all-kits.zip', 'w', zipfile.ZIP_DEFLATED) as z:
        for m, files, readme in built:
            folder = f'brandella-seo-aeo-assets/{m["n"]:02d}-{m["slug"]}'
            for fp in files:
                z.write(fp, f'{folder}/{Path(fp).name}')
            z.writestr(f'{folder}/README.txt', readme)
            lines.append(f'{m["n"]:02d}  {m["name"]}  ({page_url(m["slug"])})')
        lines += ['', 'Free for personal and client work.']
        z.writestr('brandella-seo-aeo-assets/INDEX.txt', '\n'.join(lines) + '\n')
    (DATA / 'previews' / '_kits.json').write_text(json.dumps({m['slug']: True for m, _, _ in built}))
    print('built', [m['slug'] for m, _, _ in built])


if __name__ == '__main__':
    main()
