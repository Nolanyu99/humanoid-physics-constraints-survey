import json, time, sys
sys.stdout.reconfigure(encoding='utf8')
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ss import get, F
Q = ['humanoid motion retargeting physically feasible', 'humanoid retargeting foot sliding penetration', 'humanoid motion diffusion physical plausibility',
     'physics-guided diffusion humanoid robot motion', 'humanoid motion generation dynamic feasibility', 'text-to-motion humanoid robot physically executable',
     'humanoid reference motion trajectory optimization contact', 'diffusion humanoid whole-body motion tracking feasibility']
D = json.load(open('ss_pool.json', encoding='utf8')); pool = D['pool']
for q in Q:
    d = get('paper/search', {'query': q, 'fields': F, 'limit': 100, 'year': '2024-2026'}); time.sleep(3.2)
    if 'error' in d: print('ERR', q, d['error']); D['log'].append(('search', q, 'ERR', d['error'])); continue
    items = d.get('data', []); print(len(items), d.get('total'), q); D['log'].append(('search', q, len(items), d.get('total')))
    for p in items:
        ax = (p.get('externalIds') or {}).get('ArXiv'); k = ax or p['title'].lower()
        e = pool.setdefault(k, dict(arxiv=ax, title=p['title'], date=p.get('publicationDate') or str(p.get('year')), abstract=(p.get('abstract') or '')[:1200], venue=p.get('venue'), via=[]))
        e['via'].append('search')
json.dump(D, open('ss_pool.json', 'w', encoding='utf8'), ensure_ascii=False); print('pool', len(pool))
