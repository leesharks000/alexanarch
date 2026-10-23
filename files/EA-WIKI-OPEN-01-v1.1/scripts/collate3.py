"""ChatGPT round 02: Message 1 and Message 2 spans, checked against the text shown and the full sources."""
import sys, re, json
sys.path.insert(0, '/tmp/claude-0/-home-claude/97be5201-55d8-50c9-b9d9-c76c8dde5ac6/scratchpad/st')
from collate2 import norm, M1, FULL, ART, R
M2 = norm(open(R + 'message-2-readings-and-attack.txt', encoding='utf-8').read())
t = open(R + 'replies/chatgpt-m1.txt', encoding='utf-8').read()
a = json.loads(t[t.index('['):t.rindex(']') + 1])
def chk(q, src, case, shown):
    parts = [p.strip(' .…') for p in re.split(r'\s*(?:\.\.\.|…)\s*', q) if len(p.strip(' .…')) > 4]
    seen = all(norm(p) in shown for p in parts)
    full = (src in FULL and all(norm(p) in FULL[src] for p in parts)) or (case in ART and all(norm(p) in ART[case] for p in parts))
    return seen, full
def report(name, rows):
    n=len(rows); s=sum(r[0] for r in rows); print(f'== {name}: {n} spans; {s} in the text shown; {n-s} not')
    for r in rows:
        if not r[0]: print('   ', 'SOURCE-ONLY' if r[1] else 'BREACH', r[2])
rows=[]
for o in a:
    for sp in o['spans']: rows.append((*chk(sp['quote'], sp['source'], o['case'], M1), (o['case'], sp['source'], sp['quote'][:90])))
report('chatgpt M1', rows)
b = json.load(open(R + 'replies/chatgpt-m2.json', encoding='utf-8'))
rows=[]; spans=[]
for o in b['agreement'] + b['false_positives'] + b['false_negatives']: spans.append((o['case'], o['decisive_span']))
for c, sp in spans: rows.append((*chk(sp['quote'], sp['source'], c, M1 + ' ' + M2), (c, sp['source'], sp['quote'][:90])))
report('chatgpt M2', rows)
print()
print(f"{'case':9}| attributization | retained | support")
for o in a: print(f"{o['case']:9}| {o['attributization']:15} | {o['retained_authority']['value']:8} | {', '.join(o['support'])}")
