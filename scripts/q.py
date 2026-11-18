import urllib.request, urllib.parse, re, json, sys, time, html
sys.stdout.reconfigure(encoding='utf8')
Q = [
 'abs:humanoid AND abs:diffusion AND abs:physical',
 'abs:humanoid AND abs:diffusion AND (abs:"foot skating" OR abs:"foot sliding" OR abs:penetration)',
 'abs:humanoid AND abs:diffusion AND (abs:feasib* OR abs:plausib*)',
 'abs:humanoid AND (abs:"flow matching") AND abs:motion',
 'abs:humanoid AND abs:diffusion AND abs:guidance AND abs:motion',
 'abs:humanoid AND abs:"motion generation" AND (abs:physics OR abs:physical)',
 'abs:humanoid AND abs:"motion prior" AND abs:diffusion',
 'abs:humanoid AND abs:diffusion AND (abs:tracking OR abs:controller) AND abs:"physically"',
 'abs:humanoid AND abs:"text-to-motion" AND (abs:robot OR abs:physical)',
 'abs:humanoid AND abs:diffusion AND abs:"whole-body" AND abs:motion',
 'abs:humanoid AND abs:retargeting AND (abs:physical OR abs:dynamics OR abs:contact)',
 'abs:humanoid AND abs:retargeting AND abs:diffusion',
]
out = {}
for q in Q:
    url = 'http://export.arxiv.org/api/query?' + urllib.parse.urlencode({'search_query': q, 'max_results': 80, 'sortBy': 'submittedDate', 'sortOrder': 'descending'})
    for t in range(3):
        try:
            x = urllib.request.urlopen(url, timeout=60).read().decode(); break
        except Exception as e:
            print('ERR', q, e); time.sleep(5); x = ''
    ents = re.findall(r'<entry>(.*?)</entry>', x, re.S)
    n = 0
    for e in ents:
        i = re.search(r'<id>http://arxiv.org/abs/([^<v]+)', e).group(1); d = re.search(r'<published>(\d{4}-\d\d-\d\d)', e).group(1)
        if d < '2024-06-01': continue
        ti = ' '.join(html.unescape(re.search(r'<title>(.*?)</title>', e, re.S).group(1)).split())
        ab = ' '.join(html.unescape(re.search(r'<summary>(.*?)</summary>', e, re.S).group(1)).split())
        out.setdefault(i, dict(id=i, date=d, title=ti, abs=ab, q=[]))['q'].append(Q.index(q)); n += 1
    print(len(ents), n, q)
    time.sleep(3.5)
json.dump(out, open('cands.json', 'w', encoding='utf8'), ensure_ascii=False, indent=0)
print(len(out))
