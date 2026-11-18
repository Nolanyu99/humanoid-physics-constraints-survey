import urllib.request, re, html, sys, time, os, json
sys.stdout.reconfigure(encoding='utf8')
IDS = sys.argv[1].split(',')
for i in IDS:
    p = f'txt/{i}.txt'
    if os.path.exists(p) and os.path.getsize(p) > 5000: continue
    t = ''
    for u in (f'https://arxiv.org/html/{i}', f'https://arxiv.org/html/{i}v1'):
        try:
            r = urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': 'lit-survey-script'}), timeout=60); x = r.read().decode('utf8', 'ignore')
            x = re.sub(r'<(script|style)[^>]*>.*?</\1>', ' ', x, flags=re.S); x = re.sub(r'<math.*?</math>', ' [m] ', x, flags=re.S)
            x = re.sub(r'<(h[1-6])[^>]*>', '\n\n## ', x); x = re.sub(r'</(p|div|li|tr|h[1-6])>', '\n', x)
            t = html.unescape(re.sub(r'<[^>]+>', ' ', x)); t = re.sub(r'[ \t]+', ' ', t); t = re.sub(r'\n\s*\n+', '\n\n', t)
            if len(t) > 5000: break
        except Exception as e:
            t = ''; err = str(e)
    open(p, 'w', encoding='utf8').write(t)
    print(i, len(t)); time.sleep(1.5)
