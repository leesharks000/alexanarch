import sys,json,re,collections
exec(open('r1.py').read().split("print('P1")[0])
W=json.load(open('../map/rev-matthew-whole.json')); Lr=json.load(open('../map/rev-matthew-ledger.json'))['rows']
def keys(V,s):
    out=[]
    for part in re.split(r'\s*[;+]\s*',str(s)):
        m=re.match(r'(\d+):(\d+)(?:-(\d+))?$',part.strip())
        if m:
            c=int(m.group(1)); a=int(m.group(2)); b=int(m.group(3) or a); out+=[(c,v) for v in range(a,b+1) if (c,v) in V]
    return out
cov=set()
for r in Lr: cov|=set(keys(NT['MT'],r['matt']))
P=lambda s: tuple(int(x) for x in s.split(':'))
mach=[(P(a),P(b),tuple(p),o) for a,b,p,o in W['machine']]
cm={m[1] for m in mach}
print('ledger',len(cov),'machine',len(cm),'union',len(cov|cm),'machine outside ledger',len(cm-cov))
by=collections.defaultdict(list)
for a,b,p,o in mach:
    if b not in cov: by[b].append((a,p,o))
for b in sorted(by):
    print(f'MT {b[0]}:{b[1]}', '; '.join(f'RE {a[0]}:{a[1]} {"+".join(p)} [{",".join(o) or "Mt alone"}]' for a,p,o in by[b][:5]))
