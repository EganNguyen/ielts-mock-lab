import json, re
from pathlib import Path
from collections import Counter

ROOT = Path('/Users/tim2k/test/ielts-mock-lab')
SKEL = json.loads((ROOT / 'content/vocabulary/work/learning_skeleton.json').read_text())
BASE = json.loads((ROOT / 'content/vocabulary/ielts20-21-exam-vocabulary.json').read_text())
FILES = {
    ('IELTS 20', 1): 'ielts20-test1.json', ('IELTS 20', 2): 'ielts20-test2.json',
    ('IELTS 20', 3): 'ielts20-test3.json', ('IELTS 20', 4): 'ielts20-test4.json',
    ('IELTS 21', 1): 'cambridge21-test1.json', ('IELTS 21', 2): 'cambridge21-test2.json',
    ('IELTS 21', 3): 'cambridge21-test3.json', ('IELTS 21', 4): 'cambridge21-test4.json',
}
TESTS = {k: json.loads((ROOT / 'content/academic' / v).read_text()) for k, v in FILES.items()}


def clean(s):
    return re.sub(r'\s+', ' ', re.sub(r'\{\{\d+\}\}', '______', s)).strip()


def section_obj(book, test, sid):
    d = TESTS[(book, test)]
    if sid.startswith('l'):
        return d['listening'][int(sid[1]) - 1], 'Listening'
    return d['reading'][int(sid[1]) - 1], 'Reading'


def question_meta(book, test, sid, qnum):
    """Exact question text, options and stored key for one question."""
    sec, skill = section_obj(book, test, sid)
    q = next((x for x in sec['questions'] if x['number'] == qnum), None)
    if not q:
        return None
    group = next((g for g in sec['groups'] if g['id'] == q['groupId']), None)
    opts = q.get('options') or (group or {}).get('sharedOptions') or []
    question_text = q.get('prompt', '')
    blank_segment = question_text
    for b in (group or {}).get('body', []):
        if f'{{{{{qnum}}}}}' in b:
            question_text = clean(b)
            for part in re.split(r'\s+[—–]\s+|•', b):
                if f'{{{{{qnum}}}}}' in part:
                    blank_segment = clean(part)
                    # Narrow a summary paragraph to the sentence holding this blank.
                    for sentence in re.split(r'(?<=[.!?])\s+', part):
                        if f'{{{{{qnum}}}}}' in sentence:
                            blank_segment = clean(sentence)
                            break
                    break
            else:
                blank_segment = clean(b)
            break
    ans = str(q.get('answer', ''))
    ans_text = ans
    if re.fullmatch(r'[A-Z]', ans) and opts:
        idx = ord(ans) - 65
        if 0 <= idx < len(opts):
            ans_text = opts[idx]
    return {
        'question': question_text.strip(),
        'blankSegment': blank_segment.strip(),
        'options': opts,
        'answerRaw': ans,
        'answerText': ans_text,
        'questionNumber': qnum,
        'skill': skill,
        'sectionTitle': sec.get('title', ''),
        'groupInstructions': (group or {}).get('instructions', ''),
    }


def risk_for(pos, hint=''):
    if hint in {'verb', 'adjective', 'adverb', 'noun'}:
        pos = hint
    if pos == 'verb':
        return 'Reading the verb as weaker or stronger than it is can change who did what, or how completely it happened.'
    if pos == 'adjective':
        return 'Ignoring the adjective can make you miss the degree, attitude or contrast in the sentence.'
    if pos == 'adverb':
        return 'Ignoring the adverb can make you miss how strongly or in what way something happens.'
    return 'Missing the noun can make you lose the subject or object of the sentence and confuse it with a related idea.'


def _stem(word):
    for suffix in ('ations', 'ation', 'ments', 'ment', 'ings', 'ing', 'ions', 'ion',
                   'ives', 'ive', 'ies', 'ied', 'ers', 'er', 'es', 'ed', 's', 'ly'):
        if word.endswith(suffix) and len(word) - len(suffix) >= 4:
            return word[:-len(suffix)]
    return word


def _word_stems(text):
    return {_stem(w) for w in re.findall(r'[a-z]{3,}', text.lower())}


def mentions_term(term, synonyms, *texts):
    """True only when the item's wording is visibly present in the evidence chain."""
    hay = _word_stems(' '.join(texts))
    wanted = _word_stems(term)
    for synonym in synonyms:
        wanted |= _word_stems(synonym)
    return bool(hay & wanted)


def relevance_tags(term, synonyms, answer_text, question, support, options, paraphrasing):
    """Derive answer-relationship tags only from the verified question and evidence."""
    term_stems = _word_stems(term)
    synonym_stems = set()
    for synonym in synonyms:
        synonym_stems |= _word_stems(synonym)
    answer_stems = _word_stems(answer_text)
    question_stems = _word_stems(question)
    support_stems = _word_stems(support)
    tags = []
    if term_stems & answer_stems:
        tags.append('Correct Answer')
    if term_stems & support_stems:
        tags.append('Answer Evidence')
    question_has = bool(term_stems & question_stems)
    support_has = bool(term_stems & support_stems)
    if ((question_has and not support_has)
            or (support_has and (synonym_stems & question_stems))
            or (term_stems & _word_stems(paraphrasing))):
        tags.append('Paraphrase')
    for option in options:
        if option.strip() == answer_text.strip():
            continue
        if term_stems & _word_stems(option):
            tags.append('Distractor')
            break
    return tags


def answer_importance(sentence_importance):
    return 'Critical' if sentence_importance == 'Essential' else ('Helpful' if sentence_importance == 'Helpful' else 'Not relevant')


def why_for(term, meaning_en, section_title):
    return (f'“{term}” carries the core idea “{meaning_en}”. In this sentence from “{section_title}”, '
            f'it tells you exactly what is being claimed, compared or explained — without it you only get the topic.')


# Original answer-focused pack keeps every section where an item occurs.
BASE_REFS = {}
for b in BASE['items']:
    occ = b.get('occurrences') or ([b['primary']] if b.get('primary') else [])
    BASE_REFS[b['id']] = occ
    BASE_REFS['term:' + b['term'].lower()] = occ

# Direct translations authored by the eight per-test translation agents.
translations = {}
for p in sorted((ROOT / 'content/vocabulary/work/translate').glob('output-*.json')):
    for r in json.loads(p.read_text()):
        translations[r['id']] = r

# Answer evidence verified sentence by sentence against the book text.
LINKS = {}
for p in sorted((ROOT / 'content/vocabulary/work/answers').glob('answer-output-*.json')):
    payload = json.loads(p.read_text())
    LINKS.update(payload.get('links', {}))

items = []
for s in SKEL['items']:
    tr = translations.get(s['id'], {})
    meaning_vi = tr.get('meaningVi') or s.get('meaningVi') or ''
    translation = tr.get('translation') or ''
    breakdown = tr.get('breakdown') or [{'text': c, 'vi': '', 'role': 'part of the sentence'} for c in s['sentenceChunks']]

    refs = []
    if s['source'] == 'exam':
        refs = (s.get('references') or BASE_REFS.get(s['id'])
                or BASE_REFS.get('term:' + s['term'].lower()) or [
                    {'book': s['book'], 'test': s['test'], 'skill': s['skill'],
                     'section': s['section'], 'sectionTitle': s['sectionTitle'],
                     'questions': s['questions']}])

    answers = []
    seen = set()
    if s['source'] == 'exam':
        for ref in refs:
            for qn in ref.get('questions', []):
                key = f"{s['id']}|{ref['section']}|q{qn}"
                link = LINKS.get(key)
                if not link or key in seen:
                    continue
                meta = question_meta(ref['book'], ref['test'], ref['section'], qn)
                if not meta:
                    continue
                if not mentions_term(s['term'], s['synonyms'], meta['blankSegment'], link['support']):
                    continue
                seen.add(key)
                answers.append({
                    'book': ref['book'], 'test': ref['test'], 'skill': meta['skill'],
                    'section': ref['section'], 'sectionTitle': meta['sectionTitle'],
                    'questionNumber': qn, 'question': meta['question'], 'options': meta['options'],
                    'instructions': meta['groupInstructions'], 'support': link['support'],
                    'correctAnswer': meta['answerRaw'], 'correctAnswerText': meta['answerText'],
                    'connection': link['connection'], 'paraphrasing': link['paraphrasing'],
                    'why': s.get('why') or f'Understanding “{s["term"]}” is what connects the question wording to this line of the text.',
                    'mistake': 'When matching this question: ' + risk_for(s['pos'], s.get('riskHint', ''))[0].lower() + risk_for(s['pos'], s.get('riskHint', ''))[1:],
                    'importance': answer_importance(s['sentenceImportance']),
                    'relevance': relevance_tags(s['term'], s['synonyms'], meta['answerText'],
                                                meta['question'], link['support'], meta['options'],
                                                link['paraphrasing']),
                })

    items.append({
        'id': s['id'], 'term': s['term'], 'ipa': s['ipa'], 'pos': s['pos'],
        'meaningEn': s['meaningEn'], 'meaningVi': meaning_vi, 'synonyms': s['synonyms'],
        'sentence': {
            'text': s['sentenceText'], 'translation': translation, 'breakdown': breakdown,
            'why': why_for(s['term'], s['meaningEn'], s['sectionTitle']),
            'risk': risk_for(s['pos'], s.get('riskHint', '')),
            'importance': s['sentenceImportance'],
        },
        'answers': answers,
        'references': refs,
        'source': s['source'],
        'primary': {'book': s['book'], 'test': s['test'], 'skill': s['skill'], 'section': s['section'],
                    'sectionTitle': s['sectionTitle'], 'questions': s['questions']},
    })

sections = {(i['primary']['book'], i['primary']['test'], i['primary']['section']) for i in items}

# Final hand-checked clean-up of extraction artefacts and morphology duplicates.
DROP_IDS = {'carers-sentence', 'influencers-sentence', 'microplastics-sentence',
            'hunt-sentence', 'collect-sentence'}
FIXES = {
    'specie-sentence': {
        'id': 'species-sentence', 'term': 'species', 'ipa': '/ˈspiːʃiːz/',
        'meaningEn': 'a group of living organisms that share common characteristics and can breed together',
        'meaningVi': 'loài', 'synonyms': ['kind', 'type', 'breed'],
    },
    'prehistory-sentence': {'ipa': '/ˌpriːˈhɪstəri/'},
    'saiga-sentence': {'ipa': '/ˈsaɪɡə/'},
    'knotweed-sentence': {'ipa': '/ˈnɒtwiːd/'},
    'lionfish-sentence': {'ipa': '/ˈlaɪənfɪʃ/'},
    'minimise-sentence': {'ipa': '/ˈmɪnɪmaɪz/'},
    'civilisation-sentence': {'ipa': '/ˌsɪvəlaɪˈzeɪʃn/'},
    'expose-sentence': {
        'pos': 'verb',
        'meaningEn': 'to put someone or something in a situation where they are affected by something harmful',
        'synonyms': ['subject to', 'leave open to', 'make vulnerable to'],
    },
    'collect-sentence': {
        'pos': 'verb',
        'meaningEn': 'to gather things together over time',
        'synonyms': ['gather', 'accumulate', 'assemble'],
    },
    'ocean-sentence': {
        'pos': 'noun',
        'meaningEn': 'a very large area of sea',
        'synonyms': ['sea', 'the deep', 'waters'],
    },
    'riverside-sentence': {
        'pos': 'adjective', 'meaningEn': 'on or beside a river',
        'synonyms': ['river-side', 'beside the river', 'along the river'],
    },
    'sanctuary-sentence': {
        'pos': 'noun', 'meaningEn': 'a place where birds or animals are protected',
        'synonyms': ['refuge', 'reserve', 'safe haven'],
    },
    'non-inclusive-sentence': {
        'pos': 'adjective',
        'meaningEn': 'not designed for all users, especially people with disabilities',
        'synonyms': ['exclusionary', 'not accessible', 'restrictive'],
    },
    'schoolchildren-sentence': {
        'pos': 'noun', 'meaningEn': 'children who go to school',
        'synonyms': ['pupils', 'students', 'learners'],
    },
    'knotweed-sentence': {
        'ipa': '/ˈnɒtwiːd/', 'pos': 'noun',
        'meaningEn': 'a fast-growing plant that spreads quickly and is hard to control',
        'synonyms': ['Japanese knotweed', 'invasive plant', 'weed'],
    },
    'thick-sentence': {
        'pos': 'adjective', 'meaningEn': 'dense and difficult to see through',
        'synonyms': ['dense', 'heavy', 'opaque'],
    },
    'behaviour-sentence': {
        'meaningEn': 'the way a person, animal or thing acts',
        'synonyms': ['conduct', 'manner', 'way of acting'],
    },
}
items = [i for i in items if i['id'] not in DROP_IDS]
for item in items:
    fix = FIXES.get(item['id'])
    if fix:
        item.update(fix)

# Sense/POS corrections from the two-pass semantic audit.
SENSE_FIXES = json.loads((ROOT / 'content/vocabulary/work/sense_fixes.json').read_text())
for item in items:
    fix = SENSE_FIXES.get(item['id'])
    if fix:
        item.update(fix)
sections = {(i['primary']['book'], i['primary']['test'], i['primary']['section']) for i in items}
out = {
    'meta': {
        'title': 'IELTS 20 & 21 — Sentence & Answer Vocabulary',
        'totalItems': len(items),
        'totalTests': 8,
        'totalSections': len(sections),
        'sentenceImportance': dict(Counter(i['sentence']['importance'] for i in items)),
        'answerItems': sum(1 for i in items if i['answers']),
        'answerReferences': sum(len(i['answers']) for i in items),
        'skills': dict(Counter(i['primary']['skill'] for i in items)),
    },
    'items': items,
}
(ROOT / 'content/vocabulary/ielts20-21-learning-vocabulary.json').write_text(
    json.dumps(out, ensure_ascii=False, indent=2))
print('items', len(items), 'answer items', out['meta']['answerItems'], 'refs', out['meta']['answerReferences'])
print('sections', len(sections), 'importance', out['meta']['sentenceImportance'])
print('missing translations', sum(1 for i in items if not i['sentence']['translation']))
print('missing VI meanings', sum(1 for i in items if not i['meaningVi']))
