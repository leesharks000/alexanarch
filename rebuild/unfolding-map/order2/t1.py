exec(open('../residue/r1.py').read().split("print('P1")[0])
import json,collections,itertools
N=nf
RE=NT['RE']; MT=NT['MT']; MR=NT['MR']
S={l for k in RE if k[0] in (2,3) for l,tg,_ in RE[k] if tg.startswith('V-') and re.search(r'-2[SP]$',tg)}
S-={N(x) for x in ['εἰμί','ἔχω','λέγω','γίνομαι','ποιέω','οἶδα']}
print('T1 second-person verbs of Rev 2–3:',len(S),sorted(S))
ks=list(MT); sc=[]
for i in range(0,len(ks)-44):
    W=set().union(*[L('MT',q) for q in ks[i:i+45]]); sc.append((len(S&W),ks[i]))
top=sorted(sc,reverse=True)[:12]; print('   top windows (count, start):',top)
tgt=[s for s,k in sc if k==(26,31)][0]; print('   window from 26:31:',tgt,'rank',1+sum(1 for s,_ in sc if s>tgt),'of',len(sc),'| lemmas:',sorted(S&set().union(*[L('MT',q) for q in ks[ks.index((26,31)):ks.index((26,31))+45]])))
def cfg(preds,w):
    out=[]
    for b in books:
        for k in NT[b]:
            W=win(b,k,w)
            if all(p(W) for p in preds) and preds[0](L(b,k)): out.append((b,k))
    return out
al=lambda *ls:(lambda S_: bool(S_&{N(x) for x in ls}))
print('T2',fmt(cfg([al('πειρασμός'),al('ὥρα')],1)))
print('T3',fmt(cfg([lambda S_:fam(S_,'μνημονεύω','μιμνῄσκ','μιμνήσκ','ἀναμιμνῄσκ','ἀναμιμνήσκ','μνάομαι'),al('μετανοέω','κλαίω')],1)))
print('   MT 26:75',sorted(L('MT',(26,75))))
kg=[(b,k) for b in books for k in NT[b] if re.search(r'βασιλε\S+ τῆς γῆς',text(b,k))]; print('T4 kings of the earth:',fmt(kg)); print('   with ἐλεύθερος ±1:',fmt([x for x in kg if N('ἐλεύθερος') in win(*x,1)]))
for b,spec in [('MR',[('promise',(14,31),'ἀποθνήσκω'),('sleep',(14,37),'γρηγορεύω'),('flee',(14,50),'φεύγω'),('deny',(14,68),'ἀρνέομαι')]),('LU',[('promise',(22,33),'θάνατος'),('sleep',(22,45),'κοιμάω'),('deny',(22,57),'ἀρνέομαι')]),('JOH',[('promise',(13,37),'τίθημι'),('deny',(18,25),'ἀρνέομαι')])]:
    print('T5',b,[(n,k,N(l) in L(b,k)) for n,k,l in spec], 'φεύγω in',b,[k for k in NT[b] if N('φεύγω') in L(b,k) and k[0] in (14,22,18)])
ev=['promise','sleep','flee','deny']; ok=[p for p in itertools.permutations(ev) if p.index('promise')<p.index('deny')]; print('T6 orders with promise before denial:',len(ok),'of 24; adding the foretelling of scattering (26:31, not one of the four) before flight changes nothing among the four')
pet=[k for k in MT if L('MT',k)&{N('Πέτρος')}]
Lr=json.load(open('../map/rev-matthew-ledger.json'))['rows']
def keys(V,s):
    out=[]
    for part in re.split(r'\s*[;+]\s*',str(s)):
        m=re.match(r'(\d+):(\d+)(?:-(\d+))?$',part.strip())
        if m:
            c=int(m.group(1)); a=int(m.group(2)); b=int(m.group(3) or a); out+=[(c,v) for v in range(a,b+1) if (c,v) in V]
    return out
cov=set()
for r in Lr: cov|=set(keys(MT,r['matt']))
print('T7 Peter named in',len(pet),'verses; reached',sum(k in cov for k in pet)); print('   unreached:',[f'{c}:{v}' for c,v in pet if (c,v) not in cov])
C=json.load(open('../rev3/matt-proxy-classes.json')); un=collections.Counter(int(k.split(':')[0]) for k,v in C.items() if v=='DOUBLE' and tuple(int(x) for x in k.split(':')) not in cov); tot=collections.Counter(int(k.split(':')[0]) for k,v in C.items() if v=='DOUBLE')
print('double tradition (proxy) unreached by chapter:',{c:f'{un[c]}/{tot[c]}' for c in sorted(tot)})
