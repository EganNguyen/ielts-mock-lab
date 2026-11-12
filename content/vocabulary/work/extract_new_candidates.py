import json, re, glob
from collections import Counter, defaultdict
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from wordfreq import zipf_frequency

ROOT = '/Users/tim2k/test/ielts-mock-lab'
FILES = sorted(glob.glob(ROOT + '/content/academic/ielts20-test*.json')) + sorted(glob.glob(ROOT + '/content/academic/cambridge21-test*.json'))
EXIST = json.load(open(ROOT + '/content/vocabulary/ielts20-21-exam-vocabulary.json'))
existing = {i['term'].lower() for i in EXIST['items']}
STOP = set(stopwords.words('english')) | {'also','would','could','should','might','must','may','one','two','three','first','second','third','many','much','more','most','some','such','other','another','however','therefore','because','while','where','which','whose','what','when','why','how','than','then','there','their','they','these','those','this','that','with','from','into','over','under','about','after','before','between','during','through','within','without','against','around','across','along','among','upon','onto','off','out','up','down','only','even','just','very','well','make','made','used','using','use','can','will','would','could','should','has','have','had','was','were','are','is','be','been','being','not','for','and','but','or','if','as','at','by','in','on','to','of','a','an','the','it','its','we','you','he','she','i','our','your','his','her','them','us','me','my','do','does','did','say','says','said','also','than','more','most','less','least','new','old','good','bad','big','small','high','low','long','short','few','many','much','such','own','same','different','important','possible','available','necessary','often','sometimes','usually','always','never','still','yet','already','both','each','every','either','neither','not','no','yes'}
LM = WordNetLemmatizer()
POSMAP = {'N':'n','V':'v','J':'a','R':'r'}

def clean(s):
    return re.sub(r'\s+',' ',re.sub(r'\{\{\d+\}\}','______',s)).strip()

def section_units(book, test):
    data = json.load(open(f"{ROOT}/content/academic/{'ielts20' if book=='IELTS 20' else 'cambridge21'}-test{test}.json"))
    out = {}
    for part in data['listening']:
        sid=f"l{part['number']}"
        src=[]
        for line in part.get('transcript',[]):
            src += sent_tokenize(line['text'])
        qtext=[]
        for g in part['groups']:
            qtext += [clean(b) for b in g.get('body',[])]
            qtext += [clean(o) for o in g.get('sharedOptions',[])]
        for q in part['questions']:
            qtext.append(clean(q.get('prompt','')))
            qtext += [clean(o) for o in q.get('options',[])]
        out[sid]={'skill':'Listening','title':part['title'],'source':src,'questions':qtext,'qnums':None}
    for p in data['reading']:
        sid=f"r{p['number']}"
        src=[]
        for para in p['paragraphs']:
            src += sent_tokenize(para['text'])
        qtext=[]
        for g in p['groups']:
            qtext += [clean(o) for o in g.get('sharedOptions',[])]
        for q in p['questions']:
            qtext.append(clean(q.get('prompt','')))
            qtext += [clean(o) for o in q.get('options',[])]
        out[sid]={'skill':'Reading','title':p['title'],'source':src,'questions':qtext,'qnums':None}
    return out

candidates=[]
for book,test in [('IELTS 20',i) for i in range(1,5)] + [('IELTS 21',i) for i in range(1,5)]:
    for sid, sec in section_units(book,test).items():
        counts=Counter(); sentence_for={}
        qtext=' '.join(sec['questions']).lower()
        for sent in sec['source']:
            for tok,tag in nltk.pos_tag(word_tokenize(sent)):
                if not re.fullmatch(r"[A-Za-z][A-Za-z'-]+",tok): continue
                if tag in ('NNP','NNPS'): continue
                low=tok.lower().strip("'-")
                if low in STOP or len(low)<4: continue
                p=POSMAP.get(tag[0])
                if not p: continue
                lemma=LM.lemmatize(low,p)
                if lemma in existing or len(lemma)<4: continue
                z=zipf_frequency(lemma,'en')
                if z < 2.0 or z > 5.25: continue
                counts[lemma]+=1
                if lemma not in sentence_for or (12 <= len(sent.split()) <= 38 and len(sent) > len(sentence_for[lemma])):
                    sentence_for[lemma]=sent
        for term,count in counts.items():
            inq = term in qtext
            z=zipf_frequency(term,'en')
            score = (5 if inq else 0) + (2 if z < 4.8 else 0) + min(count,3)*0.6 + (0.8 if len(term)>=8 else 0)
            candidates.append({'term':term,'book':book,'test':test,'section':sid,'skill':sec['skill'],'title':sec['title'],'count':count,'zipf':round(z,2),'inq':inq,'sentence':clean(sentence_for[term]),'score':round(score,2)})
# choose top per section, globally dedupe
bysec=defaultdict(list)
for c in candidates: bysec[(c['book'],c['test'],c['section'])].append(c)
chosen=[]; seen=set()
for key in sorted(bysec):
    rows=sorted(bysec[key],key=lambda x:(-x['score'],-x['count'],x['term']))
    n=0
    for r in rows:
        if r['term'] in seen: continue
        chosen.append(r); seen.add(r['term']); n+=1
        if n>=8: break
json.dump(chosen,open(ROOT+'/content/vocabulary/work/new_candidates.json','w'),ensure_ascii=False,indent=1)
print('sections',len(bysec),'candidates',len(candidates),'chosen',len(chosen))
for c in chosen[:20]: print(c['term'],c['zipf'],c['book'],c['test'],c['section'],'|',c['sentence'][:100])
