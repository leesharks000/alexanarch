"""Toy models of ontological flattening. Four dynamics, each a few lines, each with a number a
measurement could return. Pure stdlib + random. Nothing here is fitted to anything real."""
import random, math, json, collections
random.seed(1)

def H(ps):
    ps=[p for p in ps if p>0]; return -sum(p*math.log(p) for p in ps)
def eff(ps): return math.exp(H(ps))

# ---- A. sense collapse under a sharpening prior (resolution of a string to a sense)
# A string has K candidate senses with a Zipf prior; a system resolves to a sense by sampling
# prior^beta (beta = sharpening: 1 = faithful to prior, large = argmax). Fan-out issues m
# sub-queries and takes the majority sense. Measure the effective number of senses reached.
def sense_collapse(K=8, betas=(0.5,1,2,4,8), m_list=(1,4,8), s=1.1):
    prior=[1/(k+1)**s for k in range(K)]; Z=sum(prior); prior=[p/Z for p in prior]
    out={}
    for beta in betas:
        w=[p**beta for p in prior]; Z=sum(w); w=[x/Z for x in w]
        for m in m_list:
            counts=collections.Counter()
            for _ in range(4000):
                votes=collections.Counter(random.choices(range(K),weights=w,k=m)); counts[votes.most_common(1)[0][0]]+=1
            ps=[counts[k]/4000 for k in range(K)]
            out[(beta,m)]=round(eff(ps),2)
    return prior,out

# ---- B. fixed type system: arrivals typed by nearest existing type
# The world emits distinctions from a growing set; the ontology's type set is frozen at t0 (or
# grows only when an arrival is *read*, with probability r). Representability = share of the
# world's distinctions that have their own type.
def fixed_types(T=200, world_rate=5, read_prob=(0.0,0.02,0.1,0.5)):
    out={}
    for r in read_prob:
        types=set(range(50)); world=set(range(50)); series=[]
        for t in range(T):
            for _ in range(world_rate):
                d=len(world); world.add(d)
                if random.random()<r: types.add(d)   # read: the mismatch admitted as a new type
            series.append(len(types)/len(world))
        out[r]=[round(series[i],3) for i in (0,49,99,149,199)]
    return out

# ---- C. compression writing: compositions become sources; distinctions with support below a
# floor are pruned each generation; an exogenous floor (reading) re-injects a fraction.
def compression_loop(N=400, gens=40, prune_frac=0.15, exo=(0.0,0.02,0.05,0.10)):
    out={}
    for e in exo:
        support={i:random.paretovariate(1.2) for i in range(N)}; series=[]
        for g in range(gens):
            # composition: each distinction's support becomes its share of a compressed budget; the
            # lowest prune_frac by support are dropped (flattened into neighbours)
            items=sorted(support.items(),key=lambda kv:kv[1])
            k=int(len(items)*prune_frac)
            for i,_ in items[:k]:
                # its support is absorbed by the nearest higher-prior neighbour
                j=items[k][0]; support[j]+=support[i]*0.5; del support[i]
            # regeneration: reading re-injects a fraction of what the world still contains
            for _ in range(int(N*e)):
                d=random.randrange(N)
                if d not in support: support[d]=random.paretovariate(1.2)
            tot=sum(support.values()); ps=[v/tot for v in support.values()]
            series.append(eff(ps))
        out[e]=[round(series[i],1) for i in (0,9,19,29,39)]
    return out

# ---- D. admission concentration: rich-get-richer citation with a seed set; effective source count
def admission(N=2000, steps=60000, seed_bonus=(1.0,3.0,10.0), seed_n=15):
    out={}
    for b in seed_bonus:
        cites=[1.0]*N
        for i in range(seed_n): cites[i]=b
        for _ in range(steps):
            tot=sum(cites); r=random.random()*tot; acc=0
            for i,c in enumerate(cites):
                acc+=c
                if acc>=r: cites[i]+=1; break
        tot=sum(cites); ps=sorted((c/tot for c in cites),reverse=True)
        out[b]={'eff_sources':round(eff(ps),1),'top15_share':round(sum(ps[:15]),3)}
    return out

if __name__=='__main__':
    prior,A=sense_collapse(); B=fixed_types(); C=compression_loop(); D=admission()
    res={'A_sense_collapse':{f"beta={k[0]},fanout={k[1]}":v for k,v in A.items()},'A_prior_eff_senses':round(eff(prior),2),'B_representability_by_read_prob':{str(k):v for k,v in B.items()},'C_eff_distinctions_by_exogenous_floor':{str(k):v for k,v in C.items()},'D_admission':{str(k):v for k,v in D.items()}}
    json.dump(res,open('toys.json','w'),indent=1); print(json.dumps(res,indent=1))
