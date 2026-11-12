"""Validate the exam-focused vocabulary pack against the 8 source tests."""
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROJECT = ROOT.parents[1]
DATA = json.loads((ROOT / 'ielts20-21-exam-vocabulary.json').read_text(encoding='utf-8'))
FILES = {
    ('IELTS 20', 1): 'ielts20-test1.json', ('IELTS 20', 2): 'ielts20-test2.json',
    ('IELTS 20', 3): 'ielts20-test3.json', ('IELTS 20', 4): 'ielts20-test4.json',
    ('IELTS 21', 1): 'cambridge21-test1.json', ('IELTS 21', 2): 'cambridge21-test2.json',
    ('IELTS 21', 3): 'cambridge21-test3.json', ('IELTS 21', 4): 'cambridge21-test4.json',
}
SOURCE = {}
for key, name in FILES.items():
    SOURCE[key] = json.loads((PROJECT / 'content/academic' / name).read_text(encoding='utf-8'))

errors = []
items = DATA['items']
sections = DATA['sections']

if len(items) != DATA['meta']['totalItems']:
    errors.append('meta totalItems does not match item count')
if len(sections) != 56:
    errors.append(f'expected 56 sections, found {len(sections)}')
if len({(s['book'], s['test']) for s in sections}) != 8:
    errors.append('expected 8 tests')

ids = [i['id'] for i in items]
terms = [i['term'].lower() for i in items]
for label, values in [('id', ids), ('term', terms)]:
    dupes = [v for v, n in Counter(values).items() if n > 1]
    if dupes:
        errors.append(f'duplicate {label}: {dupes[:5]}')


def section_text(book, test, sid):
    data = SOURCE[(book, test)]
    if sid.startswith('l'):
        part = data['listening'][int(sid[1]) - 1]
        text = [part.get('title', '')]
        for g in part['groups']:
            text += g.get('body', [])
            text += g.get('sharedOptions', [])
        for q in part['questions']:
            text.append(q.get('prompt', ''))
            text += q.get('options', []) or []
        text += [line['text'] for line in part.get('transcript', [])]
        return ' '.join(text)
    p = data['reading'][int(sid[1]) - 1]
    text = [p.get('title', ''), p.get('subtitle', '')]
    for g in p['groups']:
        text += g.get('sharedOptions', [])
    for q in p['questions']:
        text.append(q.get('prompt', ''))
        text += q.get('options', []) or []
    text += [para['text'] for para in p['paragraphs']]
    return ' '.join(text)


IRREGULAR = {'stimulus': 'stimuli', 'analysis': 'analyses', 'crisis': 'crises'}


def variants(word):
    out = {word, word + 's', word + 'es', word + 'ed', word + 'ing'}
    if word.endswith('e'):
        out |= {word[:-1] + 'ing', word[:-1] + 'ed'}
    if word.endswith('y'):
        out |= {word[:-1] + 'ies', word[:-1] + 'ied'}
    if word in IRREGULAR:
        out.add(IRREGULAR[word])
    return out


def key_words(term):
    return [w for w in re.findall(r'[a-z]+', term.lower()) if len(w) > 2]


def appears(term, text):
    text = re.sub(r'[^a-z0-9 ]', ' ', text.lower())
    words = key_words(term)
    return all(any(v in text for v in variants(w)) for w in words)

section_by_key = {(s['book'], s['test'], s['id']): s for s in sections}
for item in items:
    for field in ('term', 'ipa', 'pos', 'meaningEn', 'meaningVi', 'why', 'example', 'type'):
        if not item.get(field):
            errors.append(f"{item.get('id')}: missing {field}")
    if item['priority'] not in {'E', 'I', 'A'}:
        errors.append(f"{item['id']}: bad priority")
    if not item['ipa'].startswith('/') or not item['ipa'].endswith('/'):
        errors.append(f"{item['id']}: bad IPA {item['ipa']}")
    if not item['synonyms']:
        errors.append(f"{item['id']}: no synonyms")
    if not item['occurrences']:
        errors.append(f"{item['id']}: no occurrences")
    for occ in item['occurrences']:
        full_id = f"{occ['book'].lower().replace(' ', '')}-t{occ['test']}-{occ['section']}"
        key = (occ['book'], occ['test'], full_id)
        section = section_by_key.get(key)
        if not section:
            errors.append(f"{item['id']}: unknown section {key}")
            continue
        if occ['skill'] != section['skill']:
            errors.append(f"{item['id']}: skill mismatch in {key}")
        if occ['sectionTitle'] != section['title']:
            errors.append(f"{item['id']}: section title mismatch in {key}")
        if not occ['questions']:
            errors.append(f"{item['id']}: no question numbers in {key}")
        data = SOURCE[(occ['book'], occ['test'])]
        if occ['skill'] == 'Listening':
            valid_q = {q['number'] for q in data['listening'][int(occ['section'][1]) - 1]['questions']}
        else:
            valid_q = {q['number'] for q in data['reading'][int(occ['section'][1]) - 1]['questions']}
        for q in occ['questions']:
            if q not in valid_q:
                errors.append(f"{item['id']}: bad question {q} in {key}")
        text = section_text(occ['book'], occ['test'], occ['section'])
        if not appears(item['term'], text):
            errors.append(f"{item['id']}: term not found in {key}")

priority = Counter(i['priority'] for i in items)
total = len(items)
expected = {'E': 0.50, 'I': 0.35, 'A': 0.15}
for key, share in expected.items():
    actual = priority[key] / total
    if abs(actual - share) > 0.03:
        errors.append(f'priority {key}: {actual:.1%} differs from {share:.0%}')

print(f"Items: {total} | Sections: {len(sections)} | Tests: 8")
print("Priorities:", ', '.join(f"{k} {priority[k]} ({priority[k]/total:.0%})" for k in 'EIA'))
print("Skills:", DATA['meta']['skills'])
print("Cross-referenced items:", sum(1 for i in items if len(i['occurrences']) > 1))
print("Source-based examples:", sum(1 for i in items if i.get('exampleKind') == 'source'))

if errors:
    print(f"\nFAIL — {len(errors)} problem(s):")
    for error in errors[:40]:
        print(' -', error)
    sys.exit(1)
print("\nOK — every term is grounded in its source section and the pack has no missing fields.")
