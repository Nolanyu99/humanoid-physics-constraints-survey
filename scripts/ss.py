import urllib.request, urllib.parse, json, time, sys
sys.stdout.reconfigure(encoding='utf8')
B = 'https://api.semanticscholar.org/graph/v1/'
F = 'title,externalIds,publicationDate,year,abstract,venue'
def get(path, params):
    url = B + path + '?' + urllib.parse.urlencode(params)
    for k in range(6):
        try:
            r = urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'lit-survey-script'}), timeout=60)
            return json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            if e.code == 429: time.sleep(8 * (k + 1)); continue
            return {'error': e.code}
        except Exception as e:
            time.sleep(5); err = str(e)
    return {'error': 'retries'}
if __name__ == "__main__":
    SEEDS = {'2510.26236':'PHUMA','2509.26633':'OmniRetarget','2510.02252':'GMR','2603.09956':'KDMR','2603.11480':'SPARK','2603.13228':'PhysMoDPO','2603.23983':'SafeFlow',
     '2610.30500':'PhysibleMDM','2606.22998':'TEXEDO','2609.26420':'S3','2609.22611':'HIGenNTO','2603.17927':'RoboForge','2602.06827':'DynaRetarget','2508.08241':'BeyondMimic'}
    log = []; pool = {}
    for aid, name in SEEDS.items():
        for rel in ('references', 'citations'):
            d = get(f'paper/arXiv:{aid}/{rel}', {'fields': F, 'limit': 500}); time.sleep(3.2)
            if 'error' in d: log.append((name, rel, 'ERR', d['error'])); print(name, rel, 'ERR', d['error']); continue
            key = 'citedPaper' if rel == 'references' else 'citingPaper'
            items = [x[key] for x in d.get('data', []) if x.get(key) and x[key].get('title')]
            log.append((name, rel, len(items))); print(name, rel, len(items))
            for p in items:
                ax = (p.get('externalIds') or {}).get('ArXiv'); k = ax or p['title'].lower()
                e = pool.setdefault(k, dict(arxiv=ax, title=p['title'], date=p.get('publicationDate') or str(p.get('year')), abstract=(p.get('abstract') or '')[:1200], venue=p.get('venue'), via=[]))
                e['via'].append(f'{name}:{rel[:3]}')
    json.dump(dict(log=log, pool=pool), open('ss_pool.json', 'w', encoding='utf8'), ensure_ascii=False)
    print('pool', len(pool))
