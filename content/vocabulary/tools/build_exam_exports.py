"""Build CSV, Anki and XLSX exports for the exam-focused vocabulary pack."""
import csv
import json
import re
from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

ROOT = Path(__file__).resolve().parent.parent
DATA = json.loads((ROOT / 'ielts20-21-exam-vocabulary.json').read_text(encoding='utf-8'))
ITEMS = DATA['items']
SECTIONS = {s['id']: s for s in DATA['sections']}
PRIORITY = {'E': 'Essential', 'I': 'Important', 'A': 'Advanced'}
TYPE = {'question': 'Question wording', 'paraphrase': 'Paraphrase signal', 'collocation': 'Collocation', 'distractor': 'Distractor trap', 'topic': 'Topic term'}


def section_label(occ):
    return f"{occ['skill']} {'Part' if occ['skill'] == 'Listening' else 'Passage'} {occ['section'][1:]}"


def fmt_qs(qs):
    qs = sorted(set(qs))
    if not qs:
        return ''
    if len(qs) == 1:
        return f"Q{qs[0]}"
    if all(b == a + 1 for a, b in zip(qs, qs[1:])):
        return f"Q{qs[0]}–{qs[-1]}"
    return ', '.join(f"Q{q}" for q in qs)


def also_in(item):
    return '; '.join(f"{o['book']} T{o['test']} {section_label(o)}" for o in item['occurrences'][1:])


def rows():
    for n, item in enumerate(ITEMS, start=1):
        p = item['primary']
        yield {
            'No.': n, 'Term': item['term'], 'IPA': item['ipa'], 'Part of speech': item['pos'],
            'Priority': PRIORITY[item['priority']], 'Skill': item['primary']['skill'],
            'Book': p['book'], 'Test': p['test'], 'Section': section_label(p),
            'Section title': p['sectionTitle'], 'Questions': fmt_qs(p['questions']),
            'Meaning (English)': item['meaningEn'], 'Meaning (Vietnamese)': item['meaningVi'],
            'Example': item['example'], 'Synonyms and paraphrases': '; '.join(item['synonyms']),
            'Why it helps': item['why'], 'Item type': TYPE.get(item['type'], item['type']),
            'Also appears in': also_in(item),
        }


# CSV
headers = list(next(rows()).keys())
with open(ROOT / 'ielts20-21-exam-vocabulary.csv', 'w', newline='', encoding='utf-8-sig') as f:
    wr = csv.DictWriter(f, fieldnames=headers)
    wr.writeheader()
    wr.writerows(rows())

# Anki
with open(ROOT / 'ielts20-21-exam-anki.csv', 'w', newline='', encoding='utf-8') as f:
    wr = csv.writer(f)
    wr.writerow(['Front', 'Back', 'Tags'])
    for item in ITEMS:
        p = item['primary']
        front = f"{item['term']}  {item['ipa']}".strip()
        back = (f"{PRIORITY[item['priority']]} · {p['skill']}\n"
                f"{item['meaningEn']}\n{item['meaningVi']}\n\n"
                f"“{item['example']}”\n\n"
                f"Paraphrases: {', '.join(item['synonyms'])}\n"
                f"Why: {item['why']}")
        tags = f"IELTS::{p['book'].replace(' ', '')}::T{p['test']}::{p['skill']}::{item['priority']}"
        wr.writerow([front, back, tags])

# XLSX
INK, LINE, WHITE = '111111', 'D3D7DC', 'FFFFFF'
RED, AMBER, BLUE = 'FBE7E4', 'FFF4D6', 'E8F0FD'
thin = Side(style='thin', color=LINE)
border = Border(left=thin, right=thin, top=thin, bottom=thin)
header_fill = PatternFill('solid', fgColor=INK)
header_font = Font(name='Calibri', size=10, bold=True, color=WHITE)
body = Font(name='Calibri', size=10, color=INK)
muted = Font(name='Calibri', size=10, color='555B61')

wb = Workbook()
ws = wb.active
ws.title = 'Overview'
ws.sheet_view.showGridLines = False
ws.column_dimensions['B'].width = 30
for col in 'CDE':
    ws.column_dimensions[col].width = 28
ws['B2'] = 'IELTS 20 & Cambridge IELTS 21'
ws['B2'].font = Font(name='Calibri', size=11, bold=True, color='555B61')
ws['B3'] = 'Exam-focused Listening & Reading vocabulary'
ws['B3'].font = Font(name='Calibri', size=24, bold=True)
ws['B4'] = f"{len(ITEMS)} words and phrases · {DATA['meta']['totalSections']} sections · 8 tests"
ws['B4'].font = Font(name='Calibri', size=12, color='555B61')
ws.merge_cells('B4:E4')

ws['B6'] = 'Selection principle'
ws['B6'].font = Font(name='Calibri', size=12, bold=True)
ws['B7'] = ('Only vocabulary that affects answer accuracy: question wording, paraphrase signals, collocations and distractors. '
            'This is not a complete glossary of every unfamiliar word. No answer keys are included.')
ws['B7'].alignment = Alignment(wrap_text=True, vertical='top')
ws.merge_cells('B7:E9')

ws['B11'] = 'Priority mix'
ws['B11'].font = Font(name='Calibri', size=12, bold=True)
row = 12
for key in 'EIA':
    count = DATA['meta']['priorities'][key]
    ws[f'B{row}'] = PRIORITY[key]
    ws[f'B{row}'].font = Font(name='Calibri', size=11, bold=True)
    ws[f'C{row}'] = count
    ws[f'D{row}'] = f'{count / len(ITEMS):.0%}'
    row += 1

ws['B17'] = 'Skills'
ws['B17'].font = Font(name='Calibri', size=12, bold=True)
ws['B18'] = 'Listening'
ws['C18'] = DATA['meta']['skills']['Listening']
ws['B19'] = 'Reading'
ws['C19'] = DATA['meta']['skills']['Reading']

ws['B22'] = 'How to use'
ws['B22'].font = Font(name='Calibri', size=12, bold=True)
tips = [
    'Filter by skill, priority, test or search term in the web page at /vocabulary/.',
    'Open an item to see the Vietnamese meaning, test example, paraphrases and why it matters.',
    'Items repeated across tests are shown once, with an “Also appears in” cross-reference.',
    'Use the Vocabulary sheet to sort by Book, Test or Priority; use By section for revision.',
]
for i, tip in enumerate(tips):
    ws[f'B{23+i}'] = f'•  {tip}'
    ws[f'B{23+i}'].alignment = Alignment(wrap_text=True, vertical='top')
    ws.merge_cells(f'B{23+i}:E{23+i}')

ws['B29'] = 'Source and copyright'
ws['B29'].font = Font(name='Calibri', size=12, bold=True)
ws['B30'] = ('IELTS 20 Academic and Cambridge IELTS 21 Academic, © Cambridge University Press & Assessment and Qunyan Press. '
             'Private study only; do not redistribute. Definitions, Vietnamese glosses and priority labels are study aids.')
ws['B30'].alignment = Alignment(wrap_text=True, vertical='top')
ws.merge_cells('B30:E33')

ws = wb.create_sheet('Vocabulary')
cols = ['No.', 'Term', 'IPA', 'Part of speech', 'Priority', 'Skill', 'Book', 'Test', 'Section', 'Questions',
        'Meaning (English)', 'Meaning (Vietnamese)', 'Example', 'Synonyms and paraphrases', 'Why it helps', 'Also appears in']
widths = [5, 22, 24, 12, 11, 10, 11, 6, 18, 9, 42, 34, 62, 38, 60, 34]
for i, (h, w) in enumerate(zip(cols, widths), start=1):
    c = ws.cell(row=1, column=i, value=h)
    c.font = header_font
    c.fill = header_fill
    c.border = border
    c.alignment = Alignment(horizontal='left', vertical='center')
    ws.column_dimensions[get_column_letter(i)].width = w
ws.row_dimensions[1].height = 30
for i, item in enumerate(rows(), start=2):
    values = [item[c] for c in cols]
    for j, value in enumerate(values, start=1):
        c = ws.cell(row=i, column=j, value=value)
        c.font = body
        c.border = border
        c.alignment = Alignment(vertical='top', wrap_text=j in (11, 12, 13, 14, 15, 16))
    fill = {'Essential': RED, 'Important': AMBER, 'Advanced': BLUE}[item['Priority']]
    ws.cell(row=i, column=5).fill = PatternFill('solid', fgColor=fill)
ws.freeze_panes = 'B2'
ws.auto_filter.ref = f'A1:P{len(ITEMS)+1}'
ws.sheet_view.zoomScale = 90

ws = wb.create_sheet('By section')
cols = ['Book', 'Test', 'Skill', 'Section', 'Section title', 'Items', 'Terms']
widths = [11, 6, 10, 18, 46, 7, 120]
for i, (h, w) in enumerate(zip(cols, widths), start=1):
    c = ws.cell(row=1, column=i, value=h)
    c.font = header_font
    c.fill = header_fill
    c.border = border
    ws.column_dimensions[get_column_letter(i)].width = w
by_id = {i['id']: i for i in ITEMS}
for r, section in enumerate(DATA['sections'], start=2):
    terms = [by_id[x]['term'] for x in section['itemIds']]
    values = [section['book'], section['test'], section['skill'], section_label({'skill': section['skill'], 'section': section['id'][-2:]}),
              section['title'], len(terms), ', '.join(terms)]
    for j, value in enumerate(values, start=1):
        c = ws.cell(row=r, column=j, value=value)
        c.font = body
        c.border = border
        c.alignment = Alignment(vertical='top', wrap_text=j in (4, 5, 7))
ws.freeze_panes = 'A2'
ws.auto_filter.ref = f'A1:G{len(DATA["sections"])+1}'

wb.save(ROOT / 'ielts20-21-exam-vocabulary.xlsx')
print('wrote CSV, Anki CSV and XLSX')
