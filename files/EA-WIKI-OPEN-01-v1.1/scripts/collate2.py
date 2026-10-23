import sys, re, json
sys.path.insert(0, '/tmp/claude-0/-home-claude/97be5201-55d8-50c9-b9d9-c76c8dde5ac6/scratchpad/st')
from cases import SOURCES
R = '/home/claude/drafts/wiki-open/assembly-02/'
def norm(s):
    s = re.sub(r'【entity-([^¦】]*)¦[^】]*】', r'\1', s)  # Meta entity markup -> its text
    for a, b in [('‘‘', '"'), ('’’', '"'), ('‘', "'"), ('’', "'"), ('“', '"'), ('”', '"'), ('&nbsp;', ' ')]: s = s.replace(a, b)
    return re.sub(r'\s+', ' ', s).strip().lower()
M1 = norm(open(R + 'message-1-blind-reading.txt', encoding='utf-8').read())
FULL = {k: norm(open(v['file'], encoding='utf-8').read()) for k, v in SOURCES.items()}
SC = '/tmp/claude-0/-home-claude/97be5201-55d8-50c9-b9d9-c76c8dde5ac6/scratchpad/wiki/'
ART = {'AC-1': norm(open(SC + 'Anne_Carson.1381070638.txt').read()), 'TU-1': norm(open(SC + 'Alan_Turing.1381462563.txt').read()), 'CU-1': norm(open(SC + 'Marie_Curie.1381292352.txt').read())}
def arr(fn):
    t = open(R + 'replies/' + fn, encoding='utf-8').read()
    if '```json' in t: t = t[t.rindex('```json') + 7:]
    t = t[t.index('['):t.rindex(']') + 1]
    return json.loads(t)
res = {}
for fam, fn in [('gemini', 'gemini-m1.txt'), ('musespark', 'musespark-m1.txt'), ('deepseek', 'deepseek-a.txt')]:
    a = arr(fn); rows = []
    for o in a:
        for sp in o.get('spans', []):
            q = sp['quote']; src = sp['source']
            parts = [p.strip(' .…') for p in re.split(r'\s*(?:\.\.\.|…)\s*', q) if len(p.strip(' .…')) > 4]
            seen = all(norm(p) in M1 for p in parts)
            full = src in FULL and all(norm(p) in FULL[src] for p in parts)
            art = o['case'] in ART and all(norm(p) in ART[o['case']] for p in parts)
            rows.append(dict(case=o['case'], src=src, seen=seen, full=full or art, q=q[:100]))
    res[fam] = dict(cases={o['case']: o for o in a}, spans=rows)
    n = len(rows); s = sum(r['seen'] for r in rows); f = sum((not r['seen']) and r['full'] for r in rows); b = n - s - f
    print(f'== {fam}: {n} spans; {s} in the text it was shown; {f} only in the full source; {b} in neither')
    for r in rows:
        if not r['seen']: print(f"   {'SOURCE-ONLY' if r['full'] else 'BREACH':11} {r['case']} {r['src']} | {r['q']}")
print()
FIELDS = ['attributization', 'support']
ids = list(res['gemini']['cases'])
print(f"{'case':9}| {'attributization G/M/D':24}| retained G/M/D")
for c in ids:
    g, mu, d = (res[f]['cases'].get(c, {}) for f in ('gemini', 'musespark', 'deepseek'))
    ra = lambda o: (o.get('retained_authority') or {}).get('value', '-')
    print(f"{c:9}| {g.get('attributization','-')}/{mu.get('attributization','-')}/{d.get('attributization','-'):10}| {ra(g)}/{ra(mu)}/{ra(d)}")
print()
for c in ids:
    print(c, '|', ' || '.join(', '.join(res[f]['cases'].get(c, {}).get('support', [])) for f in ('gemini', 'musespark', 'deepseek')))
json.dump(res, open(R + 'replies/collation-m1.json', 'w'), ensure_ascii=False, indent=1)
