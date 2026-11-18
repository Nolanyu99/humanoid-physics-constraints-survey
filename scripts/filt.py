import json, re, sys, os
sys.stdout.reconfigure(encoding='utf8')
D = json.load(open('ss_pool.json', encoding='utf8')); pool = D['pool']
read = set(x[:-4] for x in os.listdir('txt'))
read |= {'2510.02252','2510.26236','2509.26633'}
out = []
for k, e in pool.items():
    if e['arxiv'] in read: continue
    s = (e['title'] + ' ' + e['abstract'])
    hum = re.search(r'humanoid|\bG1\b|\bH1\b|biped', s, re.I)
    mot = re.search(r'retarget|motion generat|diffusion|flow matching|reference motion|motion prior|kinematic|trajectory optimi|text-to-motion|motion data|imitation', s, re.I)
    phy = re.search(r'physic|feasib|plausib|skat|slid|penetrat|contact|dynamic|torque|balance|executab|trackab', s, re.I)
    if not (hum and mot and phy): continue
    d = (e['date'] or '')[:10]
    if d and d[:4].isdigit() and int(d[:4]) < 2023: continue
    sc = len(e['via']) + 2 * bool(re.search(r'retarget', s, re.I)) + 2 * bool(re.search(r'diffusion|flow matching|generat', s, re.I)) + 2 * bool(re.search(r'skat|slid|penetrat|feasib|plausib', s, re.I))
    out.append((sc, d, e['arxiv'] or '-', e['title'][:100], ','.join(sorted(set(e['via'])))[:70]))
out.sort(reverse=True)
print(len(out))
for o in out[:int(sys.argv[1]) if len(sys.argv) > 1 else 120]: print(o[0], o[1], o[2], '|', o[3], '|', o[4])
