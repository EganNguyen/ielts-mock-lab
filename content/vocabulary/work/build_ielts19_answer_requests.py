import json, re
from pathlib import Path

ROOT = Path('/Users/tim2k/test/ielts-mock-lab')
SKEL = json.loads((ROOT / 'content/vocabulary/work/ielts19_skeleton.json').read_text())
TESTS = {t: json.loads((ROOT / f'content/academic/ielts19-test{t}.json').read_text()) for t in range(1, 5)}
OUT = ROOT / 'content/vocabulary/work/answers'


def clean(s):
    return re.sub(r'\s+', ' ', re.sub(r'\{\{\d+\}\}', '______', s)).strip()


for test in range(1, 5):
    d = TESTS[test]
    sections = {}
    items = []
    for it in SKEL['items']:
        if it['test'] != test or not it['questions']:
            continue
        mine = []
        for ref in it['references']:
            sid = ref['section']
            sec = d['listening'][int(sid[1]) - 1] if sid.startswith('l') else d['reading'][int(sid[1]) - 1]
            text = '\n'.join(x['text'] for x in sec.get('transcript', [])) if sid.startswith('l') else '\n\n'.join(p['text'] for p in sec['paragraphs'])
            if sid not in sections:
                sections[sid] = {'skill': ref['skill'], 'title': sec.get('title', ''), 'text': text}
            for qn in ref['questions']:
                q = next((x for x in sec['questions'] if x['number'] == qn), None)
                if not q:
                    continue
                g = next((x for x in sec['groups'] if x['id'] == q['groupId']), None)
                opts = q.get('options') or (g or {}).get('sharedOptions') or []
                ans = str(q.get('answer', ''))
                at = ans
                if re.fullmatch(r'[A-Z]', ans) and opts and ord(ans) - 65 < len(opts):
                    at = opts[ord(ans) - 65]
                question = q.get('prompt', '')
                for b in (g or {}).get('body', []):
                    if f'{{{{{qn}}}}}' in b:
                        question = clean(b)
                        break
                mine.append({
                    'key': f"{it['id']}|{sid}|q{qn}", 'section': sid, 'skill': ref['skill'],
                    'sectionTitle': sec.get('title', ''), 'questionNumber': qn, 'question': question,
                    'options': opts, 'instructions': (g or {}).get('instructions', ''), 'answerText': at,
                })
        if mine:
            items.append({'id': it['id'], 'term': it['term'], 'meaningEn': it['meaningEn'],
                          'pos': it['pos'], 'synonyms': it['synonyms'], 'refs': mine})
    payload = {'book': 'IELTS 19', 'test': test, 'tag': f'ielts19-t{test}',
               'note': 'Sections contain the complete transcript/passage text. Support must be copied verbatim from here.',
               'sections': sections, 'items': items}
    (OUT / f'request-ielts19-t{test}.json').write_text(json.dumps(payload, ensure_ascii=False, indent=1))
    print('test', test, len(items), 'items', sum(len(i['refs']) for i in items), 'refs')
