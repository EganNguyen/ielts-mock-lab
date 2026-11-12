import json, re, sys, unicodedata
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from entries import TESTS

ROOT = Path(__file__).resolve().parents[3]
BOOK_FILES = {
    ('IELTS 20', 1): 'ielts20-test1.json', ('IELTS 20', 2): 'ielts20-test2.json',
    ('IELTS 20', 3): 'ielts20-test3.json', ('IELTS 20', 4): 'ielts20-test4.json',
    ('IELTS 21', 1): 'cambridge21-test1.json', ('IELTS 21', 2): 'cambridge21-test2.json',
    ('IELTS 21', 3): 'cambridge21-test3.json', ('IELTS 21', 4): 'cambridge21-test4.json',
}
import eng_to_ipa as E2I

MANUAL_IPA = {
    'keen on': '/kiːn ɒn/', 'set lunch': '/set lʌntʃ/', 'calming effect': '/ˈkɑːmɪŋ ɪˈfekt/',
    'biologically dead': '/ˌbaɪəˈlɒdʒɪkli ded/', 'freight barge': '/freɪt bɑːdʒ/',
    'critically endangered': '/ˈkrɪtɪkli ɪnˈdeɪndʒəd/', 'widely held assumption': '/ˈwaɪdli held əˈsʌmpʃn/',
    'heightened sensitivity': '/ˈhaɪtnd ˌsensəˈtɪvəti/', 'precaution': '/prɪˈkɔːʃn/',
    'interpersonal skills': '/ˌɪntəˈpɜːsənl skɪlz/', 'brand ambassador': '/brænd æmˈbæsədə(r)/',
    'false assumption': '/fɔːls əˈsʌmpʃn/', 'free of charge': '/friː əv tʃɑːdʒ/',
    'inclusive design': '/ɪnˈkluːsɪv dɪˈzaɪn/', 'birds of prey': '/bɜːdz əv preɪ/',
    'fine motor skills': '/faɪn ˈməʊtə skɪlz/', 'spatial awareness': '/ˈspeɪʃl əˈweənəs/',
    'minimum wage': '/ˈmɪnɪməm weɪdʒ/', 'special effects': '/ˈspeʃl ɪˈfekts/',
    'genetic diversity': '/dʒəˈnetɪk daɪˈvɜːsəti/', 'sensory deprivation': '/ˈsensəri ˌdeprɪˈveɪʃn/',
    'all-inclusive': '/ˌɔːl ɪnˈkluːsɪv/', 'labour-intensive': '/ˈleɪbər ɪnˈtensɪv/',
    'medium of instruction': '/ˈmiːdiəm əv ɪnˈstrʌkʃn/', 'socio-economic': '/ˌsəʊsiəʊ ˌiːkəˈnɒmɪk/',
    'post-surgical': '/ˌpəʊst ˈsɜːdʒɪkl/', 'pain relief': '/peɪn rɪˈliːf/',
    'medical record': '/ˈmedɪkl ˈrekɔːd/', 'far-reaching': '/ˌfɑː ˈriːtʃɪŋ/',
    'second-hand': '/ˌsekənd ˈhænd/', 'out-of-town': '/ˌaʊt əv ˈtaʊn/',
    'financial set-back': '/faɪˈnænʃl ˈsetbæk/', 'rapid expansion': '/ˈræpɪd ɪkˈspænʃn/',
    'wellbeing': '/ˌwelˈbiːɪŋ/', 'midset': '', 'gore': '/ɡɔː(r)/', 'sceptre': '/ˈseptə(r)/',
    'dyspraxia': '/dɪsˈpræksiə/', 'sourdough': '/ˈsaʊədəʊ/', 'charcoal': '/ˈtʃɑːkəʊl/',
    'biogas': '/ˈbaɪəʊɡæs/', 'overtourism': '/ˌəʊvəˈtʊərɪzəm/', 'microplastic': '/ˈmaɪkrəʊplæstɪk/',
    'REM sleep': '/ˌɑːr iː ˈem sliːp/', 'disused': '/ˌdɪsˈjuːzd/', 'influencer': '/ˈɪnfluənsə/',
    'cursive': '/ˈkɜːsɪv/', 'solutionism': '/səˈluːʃənɪzəm/', 'locally sourced': '/ˈləʊkəli sɔːst/',
    'imprecisely': '/ˌɪmprɪˈsaɪsli/', 'hominin': '/ˈhɒmɪnɪn/', 'repurpose': '/ˌriːˈpɜːpəs/',
    'moveable': '/ˈmuːvəbl/', 'numeracy': '/ˈnjuːmərəsi/', 'multilingualism': '/ˌmʌltiˈlɪŋɡwəlɪzəm/',
}

def clean(text):
    text = re.sub(r'\{\{\d+\}\}', '______', text)
    text = text.replace('•', '').replace('**', '').strip()
    text = re.sub(r'\s+', ' ', text)
    return text.strip('“”" ')

def ipa_for(term):
    if term in MANUAL_IPA:
        return MANUAL_IPA[term]
    words = re.findall(r"[A-Za-z]+", term)
    if not words:
        return ''
    parts = []
    for w in words:
        out = E2I.convert(w.lower())
        if '*' in out or not out:
            return ''
        out = out.strip('/')
        for a, b in [('ʤ','dʒ'),('ʧ','tʃ'),('ɛ','e'),('oʊ','əʊ'),('ɑr','ɑː'),('ɔr','ɔː'),('ər','ə'),('ɚ','ə'),('ɪr','ɪə'),('ʊr','ʊə')]:
            out = out.replace(a,b)
        parts.append(out)
    return '/' + ' '.join(parts) + '/'

def section_units(data):
    units = []
    for part in data['listening']:
        sid = f"l{part['number']}"
        for g in part['groups']:
            for b in g.get('body', []):
                units.append((sid, 'body', clean(b), f"{g['range'][0]}–{g['range'][1]}"))
            for q in part['questions']:
                if q['groupId'] != g['id']:
                    continue
                units.append((sid, 'question', clean(q.get('prompt', '')), str(q['number'])))
                for o in q.get('options', []) or []:
                    units.append((sid, 'option', clean(o), str(q['number'])))
            for o in g.get('sharedOptions', []) or []:
                units.append((sid, 'option', clean(o), f"{g['range'][0]}–{g['range'][1]}"))
        units.append((sid, 'source', clean(part.get('title','')), ''))
        for line in part.get('transcript', []):
            for s in re.split(r'(?<=[.!?])\s+', line['text']):
                if s.strip():
                    units.append((sid, 'source', clean(s), ''))
    for p in data['reading']:
        sid = f"r{p['number']}"
        units.append((sid, 'source', clean(p.get('title','')), ''))
        units.append((sid, 'source', clean(p.get('subtitle','')), ''))
        for g in p['groups']:
            for q in p['questions']:
                if q['groupId'] != g['id']:
                    continue
                units.append((sid, 'question', clean(q.get('prompt', '')), str(q['number'])))
                for o in q.get('options', []) or []:
                    units.append((sid, 'option', clean(o), str(q['number'])))
            for o in g.get('sharedOptions', []) or []:
                units.append((sid, 'option', clean(o), f"{g['range'][0]}–{g['range'][1]}"))
        for para in p['paragraphs']:
            for s in re.split(r'(?<=[.!?])\s+', para['text']):
                if s.strip():
                    units.append((sid, 'source', clean(s), ''))
    return units

CUSTOM_EX = {
    'biologically dead': 'In 1957, the River Thames was declared biologically ______.',
    'critically endangered': 'The kākāpō is a nocturnal, flightless parrot that is critically endangered.',
    'nocturnal': 'The kākāpō is a nocturnal, flightless parrot.',
    'conservation': 'Conservationist Richard Henry led an effort to relocate several hundred of the birds.',
    'archaeological': 'The Bidcaster archaeological dig',
    'cope with': 'They are looking at corals that can cope well with the changed sea conditions.',
    'bargain': 'Save money on theatre tickets at bargaintickets.com.',
    'all-inclusive': 'The Level 1 course is all inclusive, plus a useful ______.',
    'stimulus': 'When you don’t have external sensory stimuli coming in, the brain tries to fill the void.',
    'budget': 'Trainees working on low-budget short films should expect ______.',
    'flourish': 'The kingdom of Mapungubwe flourished between the 11th and 13th century CE.',
    'repurpose': 'Demand for accommodation should be met by repurposing offices and factories.',
}

def find_unit(units, term):
    variants = {term.lower()}
    if term.endswith('e'):
        variants.add(term[:-1] + 'ing')
        variants.add(term[:-1] + 'ed')
    if term.endswith('y'):
        variants.add(term[:-1] + 'ies')
        variants.add(term[:-1] + 'ied')
    variants |= {v.replace('-', ' ') for v in variants}
    for kind in ('body', 'question', 'option', 'source'):
        for sid, k, text, q in units:
            if k != kind:
                continue
            low = text.lower()
            for v in variants:
                if ' ' in v:
                    if v in low:
                        return text, k, q
                elif re.search(r'\b' + re.escape(v) + r'(?:s|es|ed|d|ing|ly)?\b', low):
                    return text, k, q
    return None, None, None

def norm(term):
    return re.sub(r'[^a-z0-9]+', ' ', term.lower()).strip()

MANUAL_IPA.update({
    'deposit': '/dɪˈpɒzɪt/', 'solitude': '/ˈsɒlɪtjuːd/', 'sewage': '/ˈsuːɪdʒ/',
    'warehouse': '/ˈweəhaʊs/', 'initiative': '/ɪˈnɪʃətɪv/', 'nocturnal': '/nɒkˈtɜːnl/',
    'conservation': '/ˌkɒnsəˈveɪʃn/', 'reintroduce': '/ˌriːɪntrəˈdjuːs/',
    'prominent': '/ˈprɒmɪnənt/', 'vulnerable': '/ˈvʌlnərəbl/', 'methodology': '/ˌmeθəˈdɒlədʒi/',
    'carer': '/ˈkeərə/', 'responsibilities': '/rɪˌspɒnsəˈbɪlətiz/', 'cooperation': '/kəʊˌɒpəˈreɪʃn/',
    'outskirts': '/ˈaʊtskɜːts/', 'overuse': '/ˌəʊvəˈjuːz/', 'aquatic': '/əˈkwætɪk/',
    'legislation': '/ˌledʒɪsˈleɪʃn/', 'habitat': '/ˈhæbɪtæt/', 'neurological': '/ˌnjʊərəˈlɒdʒɪkl/',
    'emotion': '/ɪˈməʊʃn/', 'accuracy': '/ˈækjərəsi/', 'contract': '/ˈkɒntrækt/',
    'up-to-date': '/ˌʌp tə ˈdeɪt/', 'audience': '/ˈɔːdiəns/', 'interface': '/ˈɪntəfeɪs/',
    'alteration': '/ˌɔːltəˈreɪʃn/', 'reproduction': '/ˌriːprəˈdʌkʃn/', 'restoration': '/ˌrestəˈreɪʃn/',
    'inanimate': '/ɪnˈænɪmət/', 'personify': '/pəˈsɒnɪfaɪ/', 'accommodation': '/əˌkɒməˈdeɪʃn/',
    'exhibition': '/ˌeksɪˈbɪʃn/', 'dressing room': '/ˈdresɪŋ ruːm/', 'electrocute': '/ɪˈlektrəkjuːt/',
    'career': '/kəˈrɪə/', 'subject': '/ˈsʌbdʒɪkt/', 'quantity': '/ˈkwɒntəti/',
    'abstract': '/ˈæbstrækt/', 'mangrove': '/ˈmæŋɡrəʊv/', 'livestock': '/ˈlaɪvstɒk/',
    'widespread': '/ˈwaɪdspred/', 'herd': '/hɜːd/', 'toiletries': '/ˈtɔɪlətriːz/',
    'portfolio': '/pɔːtˈfəʊliəʊ/', 'continuity': '/ˌkɒntɪˈnjuːəti/', 'invasive': '/ɪnˈveɪsɪv/',
    'toxicity': '/tɒkˈsɪsəti/', 'cultivate': '/ˈkʌltɪveɪt/', 'philanthropic': '/ˌfɪlənˈθrɒpɪk/',
    'contemporary': '/kənˈtemprəri/', 'inheritance': '/ɪnˈherɪtəns/', 'compensate': '/ˈkɒmpenseɪt/',
    'processed': '/ˈprəʊsest/', 'herb': '/hɜːb/', 'ruins': '/ˈruːɪnz/', 'circular': '/ˈsɜːkjələ/',
    'budget': '/ˈbʌdʒɪt/', 'hunting': '/ˈhʌntɪŋ/', 'hearing': '/ˈhɪərɪŋ/', 'flourish': '/ˈflʌrɪʃ/',
    'uncertainty': '/ʌnˈsɜːtnti/', 'framework': '/ˈfreɪmwɜːk/', 'implement': '/ˈɪmplɪment/',
    'prejudice': '/ˈpredʒʊdɪs/', 'refund': '/ˈriːfʌnd/', 'permit': '/ˈpɜːmɪt/',
    'durable': '/ˈdjʊərəbl/', 'monitoring': '/ˈmɒnɪtərɪŋ/', 'fluctuation': '/ˌflʌktʃuˈeɪʃn/',
    'periphery': '/pəˈrɪfəri/', 'authenticity': '/ˌɔːθenˈtɪsəti/', 'survey': '/ˈsɜːveɪ/',
    'exhibitor': '/ɪɡˈzɪbɪtə/', 'deadline': '/ˈdedlaɪn/', 'communal': '/kəˈmjuːnl/',
    'decorative': '/ˈdekərətɪv/', 'investigate': '/ɪnˈvestɪɡeɪt/', 'hyacinth': '/ˈhaɪəsɪnθ/',
    'literacy': '/ˈlɪtərəsi/', 'accurate': '/ˈækjərət/', 'profitable': '/ˈprɒfɪtəbl/',
    'craftsmanship': '/ˈkrɑːftsmənʃɪp/',
})

CUSTOM_EX.update({
    'resistant': 'Growers look for elm trees that are resistant to Dutch elm disease.',
    'restoration': 'Coral reef restoration is a major conservation goal.',
    'personify': 'People often personify machines, treating them as if they were human.',
    'dyspraxia': 'Children with dyspraxia may find handwriting especially difficult.',
    'mangrove': 'Mangroves are coastal trees that can help protect shorelines.',
    'predation': 'Some species are threatened by predation from introduced animals.',
    'amass': 'The sisters amassed a large collection of French paintings.',
    'philanthropic': 'The sisters used part of their wealth for philanthropic purposes.',
    'contemporary': 'The collection includes contemporary French art from the same period.',
    'inheritance': 'Gwendoline came into her inheritance in 1907.',
    'sensory deprivation': 'Sensory deprivation can affect how the brain works.',
    'fraud': 'The project was designed to prevent food fraud.',
    'REM sleep': 'REM sleep is one of the two main types of sleep.',
    'archaeology': 'Archaeology can reveal how people lived in the past.',
    'refund': 'The booking policy explains when a refund is available.',
    'semi-synthetic': 'The speakers compare natural, synthetic and semi-synthetic fabrics.',
    'periphery': 'New housing is spreading towards the periphery of the city.',
    'exhibitor': 'Exhibitors can claim discounts on popular brands.',
    'discount': 'The exhibition offers discounts to exhibiting companies.',
    'medium of instruction': 'The medium of instruction is the language used to teach subjects.',
    'craftsmanship': 'The book celebrates the craftsmanship of globe makers.',
    'inheritance': 'The sisters received a large inheritance from their family.',
    'refrigeration': 'Refrigeration allows food to be kept cold for longer.',
    'flourish': 'The kingdom of Mapungubwe flourished for several centuries.',
    'calming effect': 'Heather values pottery’s calming effect.',
    'essential': 'Some tools are essential items for a potter.',
    'apron': 'Visitors should put on their aprons before starting.',
    'dementia': 'Dementia is one of the health risks linked to loneliness.',
    'cardiovascular': 'Cardiovascular disease affects the heart and blood vessels.',
    'methodology': 'The writer describes the study’s methodology.',
    'interpersonal skills': 'Volunteers need strong interpersonal skills.',
    'flexibility': 'Flexibility is one of the requirements for festival volunteers.',
    'manageable': 'The writer recommends setting manageable aims.',
    'subjective': 'Umpires make a subjective assessment of the strike zone.',
    'perceived': 'The perceived area may differ from its measured size.',
    'rental': 'The table compares furniture rental companies.',
    'archaeological': 'The talk describes an archaeological dig at Bidcaster.',
    'outline': 'The outline of fields was visible on the other side of the river.',
    'informative': 'Eighteenth-century programmes were more informative.',
    'inclusive design': 'Inclusive design removes barriers for a wide range of users.',
    'accommodation': 'The notes begin with advice on accommodation.',
    'dressing room': 'The stadium tour includes a dressing room tour.',
    'fine motor skills': 'Handwriting practice can improve fine motor skills.',
    'spatial awareness': 'Learning to write may improve spatial awareness.',
    'minimum wage': 'Trainees on low-budget films may not receive a minimum wage.',
    'special effects': 'Trainees may work on makeup for special effects.',
    'continuity': 'Continuity requires checking details between scenes.',
    'invasive': 'The lecture discusses invasive species such as the lionfish.',
    'microplastic': 'Microplastics are a form of ocean pollution.',
    'toxicity': 'The article discusses metal toxicity in the ocean.',
    'synthetic': 'Synthetic rubber is made by chemical processes.',
    'overtourism': 'Overtourism can damage popular cities.',
    'perception': 'The cruise industry faces problems of perception.',
    'framework': 'The summary refers to a framework for AI.',
    'prejudice': 'AI systems can reproduce social prejudice.',
    'locally sourced': 'Street food is popular partly because it is locally sourced.',
    'native': 'Invasive species can eat native species.',
    'repair': 'The item is being collected after repair.',
    'deadline': 'The students are worried about meeting the deadline.',
    'communal': 'The design includes communal vegetable plots.',
    'moveable': 'Moveable internal walls can change the layout.',
    'multilingualism': 'The passage examines multilingualism in Indian schools.',
})


items = []
sections = []
for (book, test), secmap in TESTS.items():
    data = json.loads((ROOT / 'content/academic' / BOOK_FILES[(book, test)]).read_text())
    units = section_units(data)
    meta = {
        'l1': (1, 'Listening', data['listening'][0]['title']),
        'l2': (2, 'Listening', data['listening'][1]['title']),
        'l3': (3, 'Listening', data['listening'][2]['title']),
        'l4': (4, 'Listening', data['listening'][3]['title']),
        'r1': (1, 'Reading', data['reading'][0]['title']),
        'r2': (2, 'Reading', data['reading'][1]['title']),
        'r3': (3, 'Reading', data['reading'][2]['title']),
    }
    for sid_raw, entries in secmap.items():
        sid = sid_raw.lower()
        num, skill, title = meta[sid]
        section = {
            'id': f"{book.lower().replace(' ', '')}-t{test}-{sid}",
            'book': book, 'test': test, 'skill': skill, 'number': num, 'title': title,
            'itemIds': [],
        }
        sections.append(section)
        for e in entries:
            text, kind, q = find_unit(units, e['t'])
            example = e['ex'] or CUSTOM_EX.get(e['t']) or text
            if not example:
                print('NO EXAMPLE', book, test, sid, e['t'])
                example = e['en']
            example = clean(example)
            if len(example) > 260:
                example = example[:257].rsplit(' ', 1)[0] + '…'
            items.append({
                'term': e['t'], 'pos': e['p'], 'priority': e['pri'],
                'meaningEn': e['en'], 'meaningVi': e['vi'],
                'synonyms': [x.strip() for x in e['syn'].split(';') if x.strip()],
                'why': e['why'], 'type': e['typ'],
                'example': example, 'exampleKind': kind or 'custom',
                'ipa': e['ipa'] or ipa_for(e['t']),
                'occurrence': {
                    'book': book, 'test': test, 'skill': skill, 'section': sid,
                    'sectionTitle': title, 'questions': e['q'],
                },
            })

# Merge duplicate terms across sections/tests.
merged = {}
order = []
for item in items:
    key = norm(item['term'])
    if key not in merged:
        merged[key] = item
        order.append(key)
    else:
        base = merged[key]
        if 'occurrences' not in base:
            base['occurrences'] = [base.pop('occurrence')]
        base['occurrences'].append(item['occurrence'])
        base['skills'] = sorted({o['skill'] for o in base['occurrences']})
        rank = {'E': 3, 'I': 2, 'A': 1}
        if rank[item['priority']] > rank[base['priority']]:
            base['priority'] = item['priority']
        if not base.get('ipa') and item.get('ipa'):
            base['ipa'] = item['ipa']

for key in order:
    base = merged[key]
    if 'occurrences' not in base:
        base['occurrences'] = [base.pop('occurrence')]
    seen = set(); uniq = []
    for o in base['occurrences']:
        key = (o['book'], o['test'], o['skill'], o['section'], tuple(o['questions']))
        if key not in seen:
            seen.add(key); uniq.append(o)
    base['occurrences'] = uniq
    base['skills'] = sorted({o['skill'] for o in base['occurrences']})
    base['skill'] = 'Both' if len(base['skills']) > 1 else base['skills'][0]
    base['id'] = re.sub(r'[^a-z0-9]+', '-', base['term'].lower()).strip('-')
    base['primary'] = base['occurrences'][0]

# assign items to their primary section
sec_by_id = {s['id']: s for s in sections}
for key in order:
    item = merged[key]
    p = item['primary']
    sid = f"{p['book'].lower().replace(' ', '')}-t{p['test']}-{p['section']}"
    sec_by_id[sid]['itemIds'].append(item['id'])

out_items = [merged[k] for k in order]
out = {
    'meta': {
        'title': 'IELTS 20 & 21 — Exam-focused Listening and Reading Vocabulary',
        'description': 'Key words, phrases and paraphrase signals selected from the eight IELTS 20 and Cambridge IELTS 21 Academic tests.',
        'totalItems': len(out_items),
        'totalSections': len(sections),
        'totalTests': 8,
        'priorities': {p: sum(1 for i in out_items if i['priority'] == p) for p in ('E', 'I', 'A')},
        'skills': {s: sum(1 for i in out_items if i['primary']['skill'] == s) for s in ('Listening', 'Reading')},
    },
    'sections': sections,
    'items': out_items,
}
Path(ROOT / 'content/vocabulary/ielts20-21-exam-vocabulary.json').write_text(json.dumps(out, ensure_ascii=False, indent=2))
print('items', len(out_items), 'sections', len(sections), 'raw', len(items))
print('priorities', out['meta']['priorities'])
print('skills', out['meta']['skills'])
print('no ipa', [i['term'] for i in out_items if not i['ipa']])
print('source examples', sum(1 for i in out_items if i['exampleKind'] == 'source'))

