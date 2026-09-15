"""v0.2 toys: C replicated over seeds with intervals; D swept over mechanisms (linear PA, superlinear PA,
hard gate, soft logistic gate) to compare curve shapes, not to fit one."""
import random, math, json, statistics, collections
def H(ps):
    ps=[p for p in ps if p>0]; return -sum(p*math.log(p) for p in ps)
def eff(ps): return math.exp(H(ps))

def compression_once(seed, N=400, gens=40, prune_frac=0.15, e=0.0):
    rnd=random.Random(seed)
    support={i:rnd.paretovariate(1.2) for i in range(N)}; series=[]
    for g in range(gens):
        items=sorted(support.items(),key=lambda kv:kv[1]); k=int(len(items)*prune_frac)
        for i,_ in items[:k]:
            j=items[k][0]; support[j]+=support[i]*0.5; del support[i]
        for _ in range(int(N*e)):
            d=rnd.randrange(N)
            if d not in support: support[d]=rnd.paretovariate(1.2)
        tot=sum(support.values()); series.append(eff([v/tot for v in support.values()]))
    return series
def C_replicated(seeds=200):
    out={}
    for e in (0.0,0.02,0.05,0.10,0.20):
        runs=[compression_once(s,e=e) for s in range(seeds)]
        out[str(e)]={}
        for g in (0,9,19,29,39):
            col=[r[g] for r in runs]; col.sort()
            out[str(e)][f"g{g+1}"]={"median":round(statistics.median(col),1),"q25":round(col[len(col)//4],1),"q75":round(col[3*len(col)//4],1)}
        # stationarity check: change between g30 and g40 relative to g30
        d=[ (r[39]-r[29])/max(1e-9,r[29]) for r in runs]
        out[str(e)]["rel_change_g30_to_g40_median"]=round(statistics.median(d),3)
    return out

def admission_variants(N=2000, steps=60000, seed=1):
    rnd=random.Random(seed); out={}
    def run(weight_fn, gate_fn=None, seed_n=15, seed_bonus=3.0):
        cites=[1.0]*N
        for i in range(seed_n): cites[i]=seed_bonus
        for _ in range(steps):
            w=[weight_fn(c)*(gate_fn(c) if gate_fn else 1.0) for c in cites]
            tot=sum(w); r=rnd.random()*tot; acc=0
            for i,x in enumerate(w):
                acc+=x
                if acc>=r: cites[i]+=1; break
        tot=sum(cites); ps=sorted((c/tot for c in cites),reverse=True)
        return {"eff_sources":round(eff(ps),1),"top15_share":round(sum(ps[:15]),3),"top1_share":round(ps[0],3)}
    out["linear_PA"]=run(lambda c:c)
    out["superlinear_PA_1.5"]=run(lambda c:c**1.5)
    out["superlinear_PA_2.0"]=run(lambda c:c**2.0)
    out["hard_gate_c>=8"]=run(lambda c:c, lambda c:1.0 if c>=8 else 0.02)
    out["soft_logistic_gate_k=1_c0=8"]=run(lambda c:c, lambda c:1/(1+math.exp(-(c-8))))
    out["hard_gate_seed_only"]=run(lambda c:c, lambda c:1.0 if c>=3.0 else 0.01, seed_n=15, seed_bonus=3.0)
    return out

if __name__=="__main__":
    res={"C_replicated_200_seeds":C_replicated(),"D_variants":admission_variants()}
    json.dump(res,open("toys2.json","w"),indent=1); print(json.dumps(res,indent=1))
