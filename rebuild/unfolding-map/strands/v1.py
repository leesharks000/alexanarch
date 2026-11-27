exec(open('../residue/r1.py').read().split("print('P1")[0])
import json,itertools,collections,random,statistics
N=nf; MT=NT['MT']; RE=NT['RE']; mi={k:i for i,k in enumerate(MT)}; ri={k:i for i,k in enumerate(RE)}
Lr=json.load(open('../map/rev-matthew-ledger.json'))['rows']
def segs(V,s):
    out=[]
    for part in re.split(r'\s*[;+]\s*',str(s)):
        m=re.match(r'(\d+):(\d+)(?:-(\d+))?$',part.strip())
        if m:
            c=int(m.group(1)); a=int(m.group(2)); b=int(m.group(3) or a); out+=[(c,v) for v in range(a,b+1) if (c,v) in V]
    return out
Q=[]
for i,r in enumerate(Lr):
    mk=segs(MT,r['matt']); rk=segs(RE,r['rev'])
    if mk and rk: Q.append((mi[mk[0]],statistics.median(ri[k] for k in rk),str(r.get('strand','')),i))
bys=collections.defaultdict(list)
for q in Q: bys[q[2]].append(q)
print('V1 strands',len(bys),'with 3+ rows:',sorted(((len(v),k) for k,v in bys.items() if len(v)>=3),reverse=True))
def conc(groups):
    c=d=0
    for v in groups:
        for a,b in itertools.combinations(v,2):
            s=(a[0]-b[0])*(a[1]-b[1])
            c+= s>0; d+= s<0
    return c,d
c,d=conc(bys.values()); print('   same-strand pairs: same order',c,'opposite',d,round(100*c/max(1,c+d)),'%')
random.seed(4); ge=0; obs=c/(c+d)
for _ in range(3000):
    g=[]
    for v in bys.values():
        rs=[x[1] for x in v]; random.shuffle(rs); g.append([(x[0],y) for x,y in zip(v,rs)])
    cc,dd=conc(g); ge+= cc/max(1,cc+dd)>=obs
print('   p (as concordant or more):',round((ge+1)/3001,3))
for k,v in sorted(bys.items(),key=lambda kv:-len(kv[1]))[:8]:
    cc,dd=conc([v]); print('   ',k,len(v),'same',cc,'opposite',dd)
def cfg(preds,w):
    out=[]
    for b in books:
        for k in NT[b]:
            W=win(b,k,w)
            if all(p(W) for p in preds) and preds[0](L(b,k)): out.append((b,k))
    return out
al=lambda *ls:(lambda S_: bool(S_&{N(x) for x in ls}))
cont=lambda b,ks:{l for k in ks for l,t,_ in NT[b][k] if t[:2] in('N-','A-','V-')}
print('V2 shared content lemmas Mt 18:21-22 ~ Rev 2:20-21; 3:19-20:',sorted(cont('MT',[(18,21),(18,22)])&cont('RE',[(2,20),(2,21),(3,19),(3,20)])))
import unicodedata
g=unicodedata.normalize('NFC',open('/home/claude/repos/alexanarch/data/corpora/lxx-swete/text/tlg001-Γένεσις.txt',encoding='utf-8').read())
m=re.search(r'Γένεσις 4:24\t[^\n]*',g); print('   Gen 4:24 LXX:',m.group(0)[:120] if m else None); print('   Mt 18:22:',text('MT',(18,22)))
ran=lambda S_: fam(S_,'λύτρον','λυτρόω','ἀντίλυτρον','λύτρωσις')
print('V3 ἄρχων near ransom-root ±3:',fmt(cfg([al('ἄρχων'),ran],3)),'| ἄρχων near λύω+αἷμα ±1:',fmt(cfg([al('ἄρχων'),al('λύω'),al('αἷμα')],1)))
print('   Rev 1:5 lemmas:',sorted(L('RE',(1,5)))); print('   Mt 20:25:',text('MT',(20,25))[:110]); print('   Mr 10:42:',text('MR',(10,42))[:120])
print('   ransom root all:',fmt(has(ran)))
print('V4 relative ἔχω + αἴρω in a verse:',fmt(has(lambda S_:N('αἴρω') in S_ and N('ἔχω') in S_ and N('δίδωμι') in S_)))
see=lambda S_:fam(S_,'βλέπω','ὁράω','θεωρέω','εἶδον','εἴδω','θεάομαι')
mk=has(al('μακρόθεν')); print('V5 μακρόθεν:',fmt(mk)); print('   with seeing in the verse:',fmt([x for x in mk if see(L(*x))])); print('   Mt 26:58:',text('MT',(26,58))); print('   Mr 14:54:',text('MR',(14,54)))
print('   μακρόθεν + seeing ±1:',fmt(cfg([al('μακρόθεν'),see],1)))
