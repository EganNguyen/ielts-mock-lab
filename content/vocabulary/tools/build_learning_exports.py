import csv, json, re
from collections import Counter
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill, Border, Side
from openpyxl.utils import get_column_letter

ROOT = Path('/Users/tim2k/test/ielts-mock-lab')
DATA = json.loads((ROOT / 'content/vocabulary/ielts20-21-learning-vocabulary.json').read_text())
OUT = ROOT / 'content/vocabulary'
items = DATA['items']


def ref_text(item):
    p = item['primary']
    return f"{p['book']} · Test {p['test']} · {p['skill']} {p['section'].upper()} · {p['sectionTitle']}"


def qs(nums):
    nums = sorted(set(nums))
    if not nums:
        return ''
    return f"Q{nums[0]}" if len(nums) == 1 else f"Q{nums[0]}–{nums[-1]}"


rows = []
for item in items:
    s = item['sentence']
    rows.append({
        'term': item['term'],
        'ipa': item['ipa'],
        'pos': item['pos'],
        'meaning_en': item['meaningEn'],
        'meaning_vi': item['meaningVi'],
        'synonyms': '; '.join(item['synonyms']),
        'sentence': s['text'],
        'sentence_vi': s['translation'],
        'sentence_importance': s['importance'],
        'sentence_breakdown': ' | '.join(f"{p['text']} → {p['vi']} ({p['role']})" for p in s['breakdown']),
        'why_you_need_it': s['why'],
        'misunderstanding_risk': s['risk'],
        'book': item['primary']['book'],
        'test': item['primary']['test'],
        'skill': item['primary']['skill'],
        'section': item['primary']['section'].upper(),
        'section_title': item['primary']['sectionTitle'],
        'questions': qs(item['primary']['questions']),
        'answer_evidence': 'yes' if item['answers'] else 'no',
        'answer_links': len(item['answers']),
        'answer_relationships': '; '.join(sorted({tag for a in item['answers'] for tag in a.get('relevance', [])})),
    })

with (OUT / 'ielts20-21-learning-vocabulary.csv').open('w', newline='', encoding='utf-8-sig') as f:
    writer = csv.DictWriter(f, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)

# Anki: no correct answers, no answer evidence details that could reveal a key.
with (OUT / 'ielts20-21-learning-anki.csv').open('w', newline='', encoding='utf-8-sig') as f:
    writer = csv.writer(f)
    writer.writerow(['Front', 'Back', 'Tags'])
    for item in items:
        s = item['sentence']
        p = item['primary']
        front = f"{item['term']} {item['ipa']}<br><i>{item['pos']}</i>"
        breakdown = '<br>'.join(f"• {part['text']} — {part['vi']} ({part['role']})" for part in s['breakdown'])
        back = (
            f"<b>{item['meaningEn']}</b><br>{item['meaningVi']}<br><br>"
            f"<i>{s['text']}</i><br>{s['translation']}<br><br>{breakdown}<br><br>"
            f"<b>Why:</b> {s['why']}<br><b>Risk:</b> {s['risk']}<br><br>"
            f"<b>Synonyms:</b> {', '.join(item['synonyms'])}<br><br>"
            f"<small>{p['book']} · Test {p['test']} · {p['skill']} {p['section'].upper()} · {p['sectionTitle']} {qs(p['questions'])}</small>"
        )
        tags = ' '.join([
            p['book'].replace(' ', '').lower(), f"test{p['test']}", p['skill'].lower(),
            f"sentence-{s['importance'].lower()}", 'answer-evidence' if item['answers'] else 'sentence-only',
        ])
        writer.writerow([front, back, tags])

wb = Workbook()
head_fill = PatternFill('solid', fgColor='1F1F1F')
head_font = Font(color='FFFFFF', bold=True, size=11)
thin = Side(style='thin', color='D9D9D9')
border = Border(bottom=thin)

ws = wb.active
ws.title = 'Overview'
ws['A1'] = DATA['meta']['title']
ws['A1'].font = Font(bold=True, size=18)
summary = [
    ('Entries', DATA['meta']['totalItems']),
    ('Sections', DATA['meta']['totalSections']),
    ('Tests', DATA['meta']['totalTests']),
    ('Entries with answer evidence', DATA['meta']['answerItems']),
    ('Verified question links', DATA['meta']['answerReferences']),
]
r = 3
for label, value in summary:
    ws.cell(r, 1, label).font = Font(bold=True)
    ws.cell(r, 2, value)
    r += 1
r += 1
ws.cell(r, 1, 'Sentence importance').font = Font(bold=True, size=13)
r += 1
for value, count in DATA['meta']['sentenceImportance'].items():
    ws.cell(r, 1, value)
    ws.cell(r, 2, count)
    r += 1
r += 1
ws.cell(r, 1, 'Answer importance').font = Font(bold=True, size=13)
r += 1
for value, count in Counter(a['importance'] for i in items for a in i['answers']).items():
    ws.cell(r, 1, value)
    ws.cell(r, 2, count)
    r += 1
r += 1
ws.cell(r, 1, 'Answer relationships').font = Font(bold=True, size=13)
r += 1
for value, count in Counter(t for i in items for a in i['answers'] for t in a.get('relevance', [])).items():
    ws.cell(r, 1, value)
    ws.cell(r, 2, count)
    r += 1
r += 1
ws.cell(r, 1, 'No answer keys are included in this workbook or the CSV/Anki exports.').font = Font(italic=True, color='7F1D1D')
ws.column_dimensions['A'].width = 38
ws.column_dimensions['B'].width = 22

cols = [
    ('Term', 'term', 22), ('IPA', 'ipa', 16), ('POS', 'pos', 8),
    ('English meaning', 'meaning_en', 42), ('Vietnamese meaning', 'meaning_vi', 34),
    ('Synonyms', 'synonyms', 40), ('Original sentence', 'sentence', 70),
    ('Vietnamese translation', 'sentence_vi', 70), ('Sentence importance', 'sentence_importance', 14),
    ('Sentence breakdown', 'sentence_breakdown', 80), ('Why you need it', 'why_you_need_it', 55),
    ('Misunderstanding risk', 'misunderstanding_risk', 55), ('Book', 'book', 10),
    ('Test', 'test', 6), ('Skill', 'skill', 10), ('Section', 'section', 8),
    ('Section title', 'section_title', 36), ('Questions', 'questions', 10),
    ('Answer evidence', 'answer_evidence', 10), ('Answer links', 'answer_links', 8),
    ('Answer relationships', 'answer_relationships', 34),
]
ws = wb.create_sheet('Entries')
for c, (title, _, width) in enumerate(cols, 1):
    cell = ws.cell(1, c, title)
    cell.fill = head_fill
    cell.font = head_font
    cell.alignment = Alignment(vertical='center')
    ws.column_dimensions[get_column_letter(c)].width = width
for r, row in enumerate(rows, 2):
    for c, (_, key, _) in enumerate(cols, 1):
        cell = ws.cell(r, c, row[key])
        cell.alignment = Alignment(vertical='top', wrap_text=True)
        cell.border = border
ws.freeze_panes = 'A2'
ws.auto_filter.ref = ws.dimensions

ws = wb.create_sheet('Answers')
acols = [
    ('Term', 20), ('Book', 10), ('Test', 6), ('Skill', 10), ('Section', 8),
    ('Section title', 34), ('Question', 10), ('Exact question', 55),
    ('Supporting sentence (verbatim)', 75), ('Vocabulary connection', 55),
    ('Paraphrasing', 50), ('Why it matters', 45), ('Potential mistake', 45),
    ('Answer importance', 14), ('Answer relationships', 32),
]
for c, (title, width) in enumerate(acols, 1):
    cell = ws.cell(1, c, title)
    cell.fill = head_fill
    cell.font = head_font
    cell.alignment = Alignment(vertical='center')
    ws.column_dimensions[get_column_letter(c)].width = width
r = 2
for item in items:
    for a in item['answers']:
        values = [
            item['term'], a['book'], a['test'], a['skill'], a['section'].upper(),
            a['sectionTitle'], f"Q{a['questionNumber']}", a['question'], a['support'],
            a['connection'], a['paraphrasing'], a['why'], a['mistake'], a['importance'],
            ', '.join(a.get('relevance', [])),
        ]
        for c, value in enumerate(values, 1):
            cell = ws.cell(r, c, value)
            cell.alignment = Alignment(vertical='top', wrap_text=True)
            cell.border = border
        r += 1
ws.freeze_panes = 'A2'
ws.auto_filter.ref = ws.dimensions

ws = wb.create_sheet('Sections')
for c, (title, width) in enumerate([('Book', 10), ('Test', 6), ('Skill', 10), ('Section', 8), ('Title', 42), ('Entries', 9), ('With answers', 12)], 1):
    cell = ws.cell(1, c, title)
    cell.fill = head_fill
    cell.font = head_font
    ws.column_dimensions[get_column_letter(c)].width = width
secs = {}
for item in items:
    p = item['primary']
    key = (p['book'], p['test'], p['skill'], p['section'])
    sec = secs.setdefault(key, {'title': p['sectionTitle'], 'n': 0, 'a': 0})
    sec['n'] += 1
    sec['a'] += 1 if item['answers'] else 0
for r, ((book, test, skill, section), sec) in enumerate(sorted(secs.items()), 2):
    for c, value in enumerate([book, test, skill, section.upper(), sec['title'], sec['n'], sec['a']], 1):
        cell = ws.cell(r, c, value)
        cell.border = border
ws.freeze_panes = 'A2'

wb.save(OUT / 'ielts20-21-learning-vocabulary.xlsx')
print('wrote', len(rows), 'entries and', sum(len(i['answers']) for i in items), 'answer links')
