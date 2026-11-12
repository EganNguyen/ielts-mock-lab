import json, re
from pathlib import Path
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import wordnet as wn
import eng_to_ipa as E2I

ROOT = Path('/Users/tim2k/test/ielts-mock-lab')
C = json.loads((ROOT / 'content/vocabulary/work/ielts19_candidates.json').read_text())
TESTS = {t: json.loads((ROOT / f'content/academic/ielts19-test{t}.json').read_text()) for t in range(1, 5)}
POSMAP = {'N': 'noun', 'V': 'verb', 'J': 'adjective', 'R': 'adverb'}
WN_POS = {'noun': 'n', 'verb': 'v', 'adjective': 'a', 'adverb': 'r'}


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
        for a, b in [('ʤ', 'dʒ'), ('ʧ', 'tʃ'), ('ɛ', 'e'), ('oʊ', 'əʊ'), ('ɑr', 'ɑː'), ('ɔr', 'ɔː'), ('ər', 'ə'), ('ɚ', 'ə'), ('ɪr', 'ɪə'), ('ʊr', 'ʊə')]:
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


def refs_for(term, test, sid):
    d = TESTS[test]
    sec = d['listening'][int(sid[1]) - 1] if sid.startswith('l') else d['reading'][int(sid[1]) - 1]
    LM = nltk.stem.WordNetLemmatizer()
    stem = LM.lemmatize(term.lower())
    out = []
    for q in sec['questions']:
        text = ' '.join([q.get('prompt', '')] + q.get('options', [])).lower()
        toks = {LM.lemmatize(t) for t in re.findall(r'[a-z]+', text)}
        if stem in toks:
            out.append(q['number'])
    group_of = {q['number']: q.get('groupId') for q in sec['questions']}
    for g in sec.get('groups', []):
        for line in g.get('body', []):
            for part in re.split(r'\s+[—–]\s+|•', line):
                m = re.search(r'\{\{(\d+)\}\}', part)
                if not m:
                    continue
                n = int(m.group(1))
                if group_of.get(n) != g['id']:
                    continue
                toks = {LM.lemmatize(t) for t in re.findall(r'[a-z]+', part.lower())}
                if stem in toks and n not in out:
                    out.append(n)
    return sorted(out)


items = []
for c in C:
    term = c['term']
    pos = ''
    for tok, tag in nltk.pos_tag(word_tokenize(c['sentence'])):
        if tok.lower().strip("'-") == term.lower():
            pos = POSMAP.get(tag[0], 'noun')
            break
    pos = pos or 'noun'
    definition, syns = definition_for(term, pos)
    refs = refs_for(term, c['test'], c['section'])
    inq = bool(refs)
    importance = 'Essential' if (inq and c['zipf'] <= 4.5) else ('Helpful' if (inq or c['zipf'] <= 3.5) else 'Optional')
    items.append({
        'id': re.sub(r'[^a-z0-9]+', '-', term.lower()).strip('-') + '-i19',
        'term': term, 'ipa': ipa(term), 'pos': pos,
        'meaningEn': definition or 'a key term used in this section',
        'meaningVi': '', 'synonyms': syns or [term],
        'sentenceText': clean(c['sentence']), 'sentenceChunks': chunk(c['sentence']),
        'sentenceImportance': importance,
        'book': 'IELTS 19', 'test': c['test'], 'skill': c['skill'], 'section': c['section'],
        'sectionTitle': c['title'], 'questions': refs,
        'source': 'exam' if refs else 'sentence', 'why': '', 'riskHint': pos,
        'references': [{'book': 'IELTS 19', 'test': c['test'], 'skill': c['skill'],
                        'section': c['section'], 'sectionTitle': c['title'], 'questions': refs}] if refs else [],
    })

# Hand-checked removals: proper names, duplicates and a typo duplicate.
DROP = {'gary-i19', 'descartes-i19', 'specie-i19', 'ecosystems-i19',
        'microplastics-i19', 'math-i19', 'recycle-i19'}
items = [i for i in items if i['id'] not in DROP]
FIXES = json.loads((ROOT / 'content/vocabulary/work/ielts19_sense_fixes.json').read_text())
for item in items:
    fix = FIXES.get(item['id'])
    if fix:
        item.update(fix)

outdir = ROOT / 'content/vocabulary/work/translate'
for t in range(1, 5):
    group = [i for i in items if i['test'] == t]
    (outdir / f'input-ielts19-t{t}.json').write_text(json.dumps(group, ensure_ascii=False, indent=2))
    print('test', t, len(group), 'with refs', sum(1 for i in group if i['questions']))
(ROOT / 'content/vocabulary/work/ielts19_skeleton.json').write_text(json.dumps({'items': items}, ensure_ascii=False, indent=2))
print('TOTAL', len(items), 'with refs', sum(1 for i in items if i['questions']))
print('importance', {k: sum(1 for i in items if i['sentenceImportance'] == k) for k in ('Essential', 'Helpful', 'Optional')})
print('empty ipa', sum(1 for i in items if not i['ipa']))
