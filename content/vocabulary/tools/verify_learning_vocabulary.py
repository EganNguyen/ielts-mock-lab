import json, re, sys
from collections import Counter
from pathlib import Path

ROOT = Path('/Users/tim2k/test/ielts-mock-lab')
DATA = json.loads((ROOT / 'content/vocabulary/ielts20-21-learning-vocabulary.json').read_text())
FILES = {
    ('IELTS 20', 1): 'ielts20-test1.json', ('IELTS 20', 2): 'ielts20-test2.json',
    ('IELTS 20', 3): 'ielts20-test3.json', ('IELTS 20', 4): 'ielts20-test4.json',
    ('IELTS 21', 1): 'cambridge21-test1.json', ('IELTS 21', 2): 'cambridge21-test2.json',
    ('IELTS 21', 3): 'cambridge21-test3.json', ('IELTS 21', 4): 'cambridge21-test4.json',
}
TESTS = {k: json.loads((ROOT / 'content/academic' / v).read_text()) for k, v in FILES.items()}
errors = []
warnings = []


def norm(s):
    s = s.replace('\u2019', "'").replace('\u2018', "'").replace('\u201c', '"').replace('\u201d', '"')
    s = s.replace('\u2013', '-').replace('\u2014', '-')
    return re.sub(r'\s+', ' ', s).strip().lower()


def section_text(book, test, sid, skill):
    d = TESTS[(book, test)]
    sec = d['listening'][int(sid[1]) - 1] if sid.startswith('l') else d['reading'][int(sid[1]) - 1]
    if skill == 'Listening':
        return '\n'.join(x['text'] for x in sec.get('transcript', []))
    return '\n'.join(p['text'] for p in sec['paragraphs'])


items = DATA['items']
if DATA['meta']['totalItems'] != len(items):
    errors.append(f"meta totalItems {DATA['meta']['totalItems']} != {len(items)}")

ids = [i['id'] for i in items]
terms = [i['term'].lower() for i in items]
if len(set(ids)) != len(ids):
    errors.append(f'duplicate ids: {[k for k, v in Counter(ids).items() if v > 1][:10]}')
if len(set(terms)) != len(terms):
    errors.append(f'duplicate terms: {[k for k, v in Counter(terms).items() if v > 1][:10]}')

sections = set()
for item in items:
    tag = item['id']
    for field in ('term', 'ipa', 'pos', 'meaningEn', 'meaningVi'):
        if not str(item.get(field, '')).strip():
            errors.append(f'{tag}: empty {field}')
    if not item['synonyms']:
        errors.append(f'{tag}: no synonyms')
    sentence = item['sentence']
    for field in ('text', 'translation', 'why', 'risk'):
        if not str(sentence.get(field, '')).strip():
            errors.append(f'{tag}: empty sentence.{field}')
    if sentence.get('importance') not in {'Essential', 'Helpful', 'Optional'}:
        errors.append(f'{tag}: bad sentence importance {sentence.get("importance")}')
    if not sentence['breakdown']:
        errors.append(f'{tag}: empty breakdown')
    for part in sentence['breakdown']:
        if not part.get('text', '').strip() or not part.get('vi', '').strip() or not part.get('role', '').strip():
            errors.append(f'{tag}: incomplete breakdown part')
    primary = item['primary']
    sections.add((primary['book'], primary['test'], primary['section']))
    if item['source'] == 'exam' and not item['answers']:
        warnings.append(f'{tag}: no verified answer link')
    if item['source'] == 'sentence' and item['answers']:
        errors.append(f'{tag}: sentence-only item has answers')
    for ref in item['references']:
        if ref['book'] != primary['book'] or ref['test'] != primary['test']:
            continue
    for answer in item['answers']:
        for field in ('question', 'support', 'correctAnswer', 'connection', 'paraphrasing', 'why', 'mistake'):
            if not str(answer.get(field, '')).strip():
                errors.append(f"{tag} Q{answer.get('questionNumber')}: empty {field}")
        if answer.get('importance') not in {'Critical', 'Helpful', 'Not relevant'}:
            errors.append(f"{tag} Q{answer.get('questionNumber')}: bad answer importance")
        bad_tags = set(answer.get('relevance', [])) - {'Correct Answer', 'Answer Evidence', 'Paraphrase', 'Distractor'}
        if bad_tags:
            errors.append(f"{tag} Q{answer.get('questionNumber')}: bad relevance tags {bad_tags}")
        text = norm(section_text(answer['book'], answer['test'], answer['section'], answer['skill']))
        if norm(answer['support']) not in text:
            errors.append(f"{tag} Q{answer['questionNumber']}: support is not verbatim in {answer['book']} T{answer['test']} {answer['section']}")

answer_items = sum(1 for i in items if i['answers'])
answer_refs = sum(len(i['answers']) for i in items)
if DATA['meta']['answerItems'] != answer_items:
    errors.append('meta answerItems mismatch')
if DATA['meta']['answerReferences'] != answer_refs:
    errors.append('meta answerReferences mismatch')
if DATA['meta']['totalSections'] != len(sections):
    errors.append('meta totalSections mismatch')

print('items', len(items))
print('sections', len(sections))
print('sentence importance', dict(Counter(i['sentence']['importance'] for i in items)))
print('answer items', answer_items, 'answer refs', answer_refs)
print('answer importance', dict(Counter(a['importance'] for i in items for a in i['answers'])))
print('answer relationships', dict(Counter(t for i in items for a in i['answers'] for t in a['relevance'])))
print('skills', dict(Counter(i['primary']['skill'] for i in items)))
print('warning: items with no answer link', len(warnings))
if errors:
    print('\nERRORS', len(errors))
    for e in errors[:60]:
        print(' -', e)
    sys.exit(1)
print('\nPASS: all structural, translation and verbatim-evidence checks passed.')
