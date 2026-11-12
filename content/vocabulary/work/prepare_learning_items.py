import json, re
from pathlib import Path
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import wordnet as wn
import eng_to_ipa as E2I

ROOT = Path('/Users/tim2k/test/ielts-mock-lab')
BASE = json.loads((ROOT / 'content/vocabulary/ielts20-21-exam-vocabulary.json').read_text())
NEW = json.loads((ROOT / 'content/vocabulary/work/selected_new.json').read_text())
FILES = {
    ('IELTS 20', 1): 'ielts20-test1.json', ('IELTS 20', 2): 'ielts20-test2.json',
    ('IELTS 20', 3): 'ielts20-test3.json', ('IELTS 20', 4): 'ielts20-test4.json',
    ('IELTS 21', 1): 'cambridge21-test1.json', ('IELTS 21', 2): 'cambridge21-test2.json',
    ('IELTS 21', 3): 'cambridge21-test3.json', ('IELTS 21', 4): 'cambridge21-test4.json',
}
TESTS = {k: json.loads((ROOT / 'content/academic' / v).read_text()) for k, v in FILES.items()}
POSMAP = {'N': 'noun', 'V': 'verb', 'J': 'adjective', 'R': 'adverb'}
WN_POS = {'noun': 'n', 'verb': 'v', 'adjective': 'a', 'adverb': 'r'}


def section_sentences(book, test, sid):
    d = TESTS[(book, test)]
    if sid.startswith('l'):
        part = d['listening'][int(sid[1]) - 1]
        out = []
        for line in part.get('transcript', []):
            out += sent_tokenize(line['text'])
        return out, part['title'], 'Listening', int(sid[1])
    p = d['reading'][int(sid[1]) - 1]
    out = []
    for para in p['paragraphs']:
        out += sent_tokenize(para['text'])
    return out, p['title'], 'Reading', int(sid[1])


def find_sentence(term, sentences):
    variants = {term.lower()}
    if term.endswith('e'):
        variants |= {term[:-1] + 'ing', term[:-1] + 'ed'}
    if term.endswith('y'):
        variants |= {term[:-1] + 'ies', term[:-1] + 'ied'}
    pats = [re.compile(r'\b' + re.escape(v) + r'(?:s|es|ed|d|ing|ly)?\b', re.I) for v in variants]
    hits = [s for s in sentences if any(p.search(s) for p in pats)]
    if not hits:
        return ''
    hits.sort(key=lambda s: (0 if 8 <= len(s.split()) <= 38 else 1, abs(len(s.split()) - 22)))
    return hits[0]


def clean(s):
    return re.sub(r'\s+', ' ', re.sub(r'\{\{\d+\}\}', '______', s)).strip()


def chunk(sentence):
    s = clean(sentence)
    parts = re.split(r'(?<=[;:])\s+|\s+—\s+', s)
    if len(parts) == 1 and len(s.split()) > 24:
        m = re.search(r'\s+(because|although|while|whereas|which|that|when|if|so that|but)\s+', s, re.I)
        if m and m.start() > 10:
            parts = [s[:m.start()].strip(), s[m.start():].strip()]
    if len(parts) == 1 and len(s.split()) > 18:
        words = s.split()
        cut = len(words) // 2
        parts = [' '.join(words[:cut]), ' '.join(words[cut:])]
    parts = [p.strip(' ,') for p in parts if len(p.split()) >= 3][:4] or [s]
    return parts


def ipa(term):
    parts = []
    for w in re.findall(r'[A-Za-z]+', term):
        out = E2I.convert(w.lower())
        if '*' in out or not out:
            return ''
        out = out.strip('/')
        for a, b in [('ʤ','dʒ'),('ʧ','tʃ'),('ɛ','e'),('oʊ','əʊ'),('ɑr','ɑː'),('ɔr','ɔː'),('ər','ə'),('ɚ','ə'),('ɪr','ɪə'),('ʊr','ʊə')]:
            out = out.replace(a, b)
        parts.append(out)
    return '/' + ' '.join(parts) + '/'


def definition_for(term, pos):
    p = WN_POS.get(pos, 'n')
    ss = wn.synsets(term, pos=p) or wn.synsets(term)
    if not ss:
        return '', []
    syns = []
    for s in ss[:2]:
        for l in s.lemmas():
            n = l.name().replace('_', ' ')
            if n.lower() != term.lower() and n.lower() not in syns:
                syns.append(n)
    return ss[0].definition(), syns[:4]


items = []
for base in BASE['items']:
    p = base['primary']
    sentences, title, skill, number = section_sentences(p['book'], p['test'], p['section'])
    sent = find_sentence(base['term'], sentences) or base['example']
    items.append({
        'id': f"{base['id']}-learn",
        'term': base['term'], 'ipa': base['ipa'], 'pos': base['pos'],
        'meaningEn': base['meaningEn'], 'meaningVi': base['meaningVi'], 'synonyms': base['synonyms'],
        'sentenceText': clean(sent), 'sentenceChunks': chunk(sent),
        'sentenceImportance': 'Essential' if base['priority'] == 'E' else ('Helpful' if base['priority'] == 'I' else 'Optional'),
        'book': p['book'], 'test': p['test'], 'skill': skill, 'section': p['section'],
        'sectionTitle': title, 'questions': p['questions'], 'source': 'exam',
        'why': base['why'], 'riskHint': base['pos'],
    })

seen = {i['term'].lower() for i in items}
for c in NEW:
    term = c['term']
    if term.lower() in seen:
        continue
    pos = ''
    for tok, tag in nltk.pos_tag(word_tokenize(c['sentence'])):
        if tok.lower().strip("'-") == term.lower():
            pos = POSMAP.get(tag[0], 'noun'); break
    pos = pos or 'noun'
    definition, syns = definition_for(term, pos)
    if not definition:
        definition = 'a key term used in this section'
    items.append({
        'id': re.sub(r'[^a-z0-9]+', '-', term.lower()).strip('-') + '-sentence',
        'term': term, 'ipa': ipa(term), 'pos': pos,
        'meaningEn': definition, 'meaningVi': '',
        'synonyms': syns or [term],
        'sentenceText': clean(c['sentence']), 'sentenceChunks': chunk(c['sentence']),
        'sentenceImportance': 'Essential' if c['inq'] else ('Helpful' if c['zipf'] < 3.9 else 'Optional'),
        'book': c['book'], 'test': c['test'], 'skill': c['skill'], 'section': c['section'],
        'sectionTitle': c['title'], 'questions': [], 'source': 'sentence',
        'why': '', 'riskHint': pos,
    })
    seen.add(term.lower())

# Group by test for translation agents.
outdir = ROOT / 'content/vocabulary/work/translate'
outdir.mkdir(parents=True, exist_ok=True)
for book, test in FILES:
    group = [i for i in items if i['book'] == book and i['test'] == test]
    (outdir / f"input-{book.lower().replace(' ', '')}-t{test}.json").write_text(json.dumps(group, ensure_ascii=False, indent=2))
    print(book, test, len(group))
(ROOT / 'content/vocabulary/work/learning_skeleton.json').write_text(json.dumps({'items': items}, ensure_ascii=False, indent=2))
print('TOTAL', len(items))
