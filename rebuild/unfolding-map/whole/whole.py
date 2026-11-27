import json,collections,math,itertools,random
R=json.load(open('relations.json'))
REV=R['RE']; SEATS=['GOD','CHRIST','ANGEL','FAITHFUL','ADVERSARY','ALL']
def seer(x): return 'FAITHFUL' if x=='SEER' else x
REVm=[(seer(a) if a else None,v,seer(p) if p else None,k) for a,v,p,k in REV]
def cellz(tgt,slot):
    """z for each (Rev seat -> target seat) in a slot: observed = number of Rev events (seat, verb) whose verb occurs in target with target seat in that slot;
       expectation from verbs redistributed over Revelation's events of that slot."""
    i=0 if slot=='agt' else 2
    ev=[(x[i],x[1]) for x in REVm if x[i]]; verbs=[v for _,v in ev]; n=len(verbs)
    T=collections.defaultdict(set)
    for x in R[tgt]:
        if x[i]: T[x[i]].add(x[1])
    Z={}
    for rs in SEATS:
        mine=[v for s,v in ev if s==rs]
        for ts in SEATS:
            obs=sum(1 for v in mine if v in T[ts]); p=sum(1 for v in verbs if v in T[ts])/n
            e=len(mine)*p; sd=math.sqrt(len(mine)*p*(1-p)) if 0<p<1 and mine else 0
            Z[(rs,ts)]=(obs,len(mine),e,(obs-e)/sd if sd else 0.0)
    return Z
out={}
for slot,name in (('pat','PATIENT'),('agt','AGENT')):
    for tgt in ['MT','MR','LU','JOH','AC']:
        Z=cellz(tgt,slot); out[f'{slot}:{tgt}']={f'{a}>{b}':Z[(a,b)] for a,b in Z}
        print(f"\n{name} slot, Revelation's seat (rows) against {tgt}'s seat (columns): z (observed of n)")
        print(' '*11+''.join(f'{t:>15}' for t in SEATS))
        for rs in SEATS: print(f'{rs:11}'+''.join(f"{Z[(rs,ts)][3]:+7.2f} ({Z[(rs,ts)][0]:>2}/{Z[(rs,ts)][1]:<2})" for ts in SEATS))
# W5: landing of whole relations under maps
def landing(tgt,ma,mp):
    T=collections.defaultdict(set)
    for a,v,p,_ in R[tgt]: T[(a,p)].add(v)
    tv=collections.Counter()
    rel=[(a,v,p) for a,v,p,_ in REVm]; verbs=[v for _,v,_ in rel]; n=len(verbs)
    def has(a2,p2,v):
        # every seat the Revelation relation has must be matched
        if a2 and p2: return v in T[(a2,p2)]
        if a2: return any(v in T[(a2,q)] for q in SEATS+[None])
        return any(v in T[(q,p2)] for q in SEATS+[None])
    obs=0; exp=0; var=0; cache={}
    for a,v,p in rel:
        a2=ma.get(a,a) if a else None; p2=mp.get(p,p) if p else None
        if has(a2,p2,v): obs+=1
        key=(a2,p2)
        if key not in cache: cache[key]=sum(1 for u in verbs if has(a2,p2,u))/n
        q=cache[key]; exp+=q; var+=q*(1-q)
    return obs,len(rel),exp,(obs-exp)/math.sqrt(var) if var else 0
H=({'ANGEL':'ADVERSARY'},{'ADVERSARY':'CHRIST','FAITHFUL':'CHRIST'})
print('\nW5. Landing of Revelation\'s relations under the identity map and under H:')
res={}
for tgt in ['MT','MR','LU','JOH','AC']:
    i=landing(tgt,{},{}); h=landing(tgt,*H); res[tgt]=dict(identity=i,H=h)
    print(f"  {tgt}: identity {i[0]}/{i[1]} (expected {i[2]:.1f}, z {i[3]:+.2f})   H {h[0]}/{h[1]} (expected {h[2]:.1f}, z {h[3]:+.2f})")
# rank of H among all maps of its size
maps=[]
for (x,y) in itertools.combinations(SEATS,2):
    for tx in SEATS:
        for ty in SEATS:
            if tx==x or ty==y: continue
            for z in SEATS:
                for tz in SEATS:
                    if tz==z: continue
                    maps.append(({z:tz},{x:tx,y:ty}))
print('maps of the same size:',len(maps))
for tgt in ['JOH','MT','AC']:
    zs=[]
    T=None
    for ma,mp in maps: zs.append(landing(tgt,ma,mp)[3])
    hz=landing(tgt,*H)[3]; rank=1+sum(1 for z in zs if z>hz); best=sorted(zip(zs,maps),key=lambda t:-t[0])[:5]
    res[tgt]['rank']=rank; res[tgt]['of']=len(maps)
    print(f"  {tgt}: H z {hz:+.2f}, rank {rank} of {len(maps)} ({100*rank/len(maps):.1f}%); best maps: "+' | '.join(f"z {z:+.2f} agents {ma} patients {mp}" for z,(ma,mp) in best))
json.dump(dict(cells=out,landing=res),open('whole.json','w'),ensure_ascii=False)
