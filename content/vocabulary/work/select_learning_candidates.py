import json
C=json.load(open('content/vocabulary/work/new_candidates.json'))
BLOCK=set('chef cinema clay potter lonely chick parrot nest stressed housework supermarket avocado furniture coin detector pond keyboard frozen robot scientist climb cafe farmer prey flood sail swim sailing shampoo trainee prep podcast rubber candle massage silk beginner drill shelf cruise tourist souvenir boxing elderly tourism octopus nightmare decorate cabin snack fabric sheep bamboo cork wool hemp recycle squirrel toad gardener rhododendron cave hairdresser vegetable craft leather polynesian amazonian vietnamese african french hundred-mile-an-hour high-fructose'.split())
adv=[x for x in C if x['zipf']<=4.3 and x['term'] not in BLOCK]
mid=[x for x in C if 4.3<x['zipf']<=4.5 and x['term'] not in BLOCK]
extra_terms='depression facility transport survive escape danger trend advertising limit plastic strike manage cycle rent customer deliver ancient actor familiar perform independence launch temperature marine wave intelligence planet perspective stadium teach affected painting decade drawing protected introduction ocean detail aircraft extreme noise quiet external internal sugar literature diet pattern kingdom object'.split()
extra=[x for x in C if x['term'] in extra_terms]
sel=[]; seen=set()
for group in (adv,mid,extra):
    for x in sorted(group,key=lambda y:(-y['score'],y['zipf'],y['term'])):
        if x['term'] in seen: continue
        sel.append(x); seen.add(x['term'])
print('adv',len(adv),'mid',len(mid),'extra',len(extra),'selected',len(sel))
for x in sel: print(f"{x['term']}|{x['zipf']}|{x['book']}|{x['test']}|{x['section']}|{x['sentence']}")
json.dump(sel,open('content/vocabulary/work/selected_new.json','w'),ensure_ascii=False,indent=1)
