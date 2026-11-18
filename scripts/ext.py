import re, sys, json
sys.stdout.reconfigure(encoding='utf8')
c = json.load(open('cands.json', encoding='utf8'))
K = [(r'penetrat|interpenetrat|collision', 2), (r'foot (skat|slid)|skating|sliding', 3), (r'contact', 1), (r'torque limit|joint limit|velocity limit|feasib', 2),
     (r'\bZMP\b|center of mass|CoM\b|support polygon|balance', 2), (r'guidance|guided|classifier|reward|preference|DPO', 2), (r'projection|project(ed)? onto|post-process|optimi[sz]ation', 1),
     (r'simulat|physics engine|MuJoCo|Isaac', 1), (r'track(ing)? (policy|controller)|tracker|motion tracking', 1), (r'loss', 1), (r'real[- ]world|hardware|real robot|Unitree G1|\bG1\b', 1)]
def sents(t):
    t = re.sub(r'\s+', ' ', t); return re.split(r'(?<=[.;])\s+(?=[A-Z(])', t)
for i in sys.argv[1].split(','):
    t = open(f'txt/{i}.txt', encoding='utf8').read()
    cut = re.search(r'\n## (\d+\s*)?(References|Bibliography)', t); t = t[:cut.start()] if cut else t
    ti = c.get(i, {}).get('title', t[:120])
    S = sents(t); sc = []
    for k, s in enumerate(S):
        if not 40 < len(s) < 450: continue
        v = sum(w for p, w in K if re.search(p, s, re.I))
        if re.search(r'limitation|future work|fail', s, re.I): v += 2
        sc.append((v, k, s))
    top = sorted(sorted(sc, reverse=True)[:int(sys.argv[2]) if len(sys.argv) > 2 else 12], key=lambda x: x[1])
    print(f'\n######## {i} | {ti}\nABS: {c.get(i, {}).get("abs", "")[:900]}')
    for v, k, s in top: print(f'- [{k}] {s[:420]}')
