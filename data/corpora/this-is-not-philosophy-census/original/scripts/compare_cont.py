import json,collections,math
J=["manworld","cpr","rip","jbsp","phiToday","angelaki"]
def H(c):
    n=sum(c.values()); return -sum(v/n*math.log2(v/n) for v in c.values()) if n else 0
dec=lambda y:f"{(y//10)*10}s"
pool=collections.defaultdict(list)
for j in J:
    A=[o for o in json.load(open(f"codes-{j}.json")) if o["article"]]
    by=collections.defaultdict(list)
    for o in A: by[dec(o["year"])].append(o); pool[dec(o["year"])].append(o)
    print(f"== {j}\ndecade    n  named%  pair%  top1  top1%  top3%  H(names)")
    for d in sorted(by):
        r=by[d]; nm=[o for o in r if o["names"]]; c=collections.Counter(x for o in nm for x in o["names"])
        if len(r)<10: continue
        top=c.most_common(3); tot=sum(c.values())
        print(f"{d:7} {len(r):4} {100*len(nm)/len(r):6.0f} {100*sum(len(o['names'])>=2 for o in r)/len(r):6.0f}  {top[0][0][:10] if top else '-':10} {100*top[0][1]/tot if top else 0:4.0f} {100*sum(v for _,v in top)/tot if top else 0:5.0f}  {H(c):5.2f}")
print("== POOLED (six journals)")
print("decade    n  named%  pair%  top names")
for d in sorted(pool):
    r=pool[d]; nm=[o for o in r if o["names"]]; c=collections.Counter(x for o in nm for x in o["names"])
    if len(r)<20: continue
    print(f"{d:7} {len(r):4} {100*len(nm)/len(r):6.0f} {100*sum(len(o['names'])>=2 for o in r)/len(r):6.0f}  H={H(c):4.2f}  "+", ".join(f"{k} {v}" for k,v in c.most_common(6)))
