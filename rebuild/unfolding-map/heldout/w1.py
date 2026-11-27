exec(open('../residue/r1.py').read().split("print('P1")[0])
N=nf
def cfg(preds,w):
    out=[]
    for b in books:
        for k in NT[b]:
            W=win(b,k,w)
            if all(p(W) for p in preds) and preds[0](L(b,k)): out.append((b,k))
    return out
al=lambda *ls:(lambda S_: bool(S_&{N(x) for x in ls}))
def form(test):
    return [(b,k) for b in books for k in NT[b] if test(NT[b][k])]
def oerch(v):
    for i,(l,t,w) in enumerate(v):
        if l==N('ἔρχομαι') and t.startswith('V-PNP-NSM') and i>0 and v[i-1][0]==N('ὁ'): return True
    return False
a=form(oerch); print('ὁ ἐρχόμενος all:',fmt(a))
print('W1:',fmt([x for x in a if N('Ἰωάννης') in win(x[0],x[1],3)]))
print('W2:',fmt(cfg([al('ἄγγελος'),al('ἀποστέλλω'),al('Ἰωάννης')],3)))
w3=form(lambda v:any(l==N('μακάριος') and t.startswith('A-NSM') for l,t,w in v)); print('W3:',len(w3),fmt(w3))
print('W4:',fmt(has(lambda S_:{N('ἔχω'),N('οὖς'),N('ἀκούω')}<=S_)))
print('W5:',fmt(cfg([al('μετανοέω'),al('ἔργον')],2)))
print('W6:',fmt(has(lambda S_:fam(S_,'ἀποκαλύπτω','ἀποκάλυψις') and fam(S_,'δίδωμι','παραδίδωμι'))))
print('W7:',fmt(cfg([lambda S_:fam(S_,'ἀναπαύω','ἀνάπαυσις'),lambda S_:fam(S_,'κόπος','κοπιάω')],1)))
print('W8:',fmt(cfg([al('δέω'),al('Σατανᾶς','διάβολος')],3)))
print('W9:',fmt(has(lambda S_:{N('ἑπτά'),N('πνεῦμα')}<=S_)))
cont=lambda b,ks:{l for k in ks for l,t,_ in NT[b][k] if t[:2] in('N-','A-','V-')}
print('W10:',sorted(cont('MT',[(12,36),(12,37)])&cont('RE',[(20,12),(20,13)])))
for b,k in [('MT',(11,3)),('RE',(1,4)),('MT',(11,10)),('RE',(1,1)),('MT',(11,27)),('MT',(11,28)),('RE',(14,13)),('MT',(11,20)),('MT',(11,19))]: print(b,k,text(b,k)[:230])
