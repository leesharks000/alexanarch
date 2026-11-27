exec(open('../residue/r1.py').read().split("print('P1")[0])
N=nf
def anyl(*ls): s={N(x) for x in ls}; return lambda S: bool(S&s)
def stem(*st): return lambda S: fam(S,*st)
def cfg(preds,w):
    out=[]
    for b in books:
        for k in NT[b]:
            W=win(b,k,w)
            if all(p(W) for p in preds) and preds[0](L(b,k)): out.append((b,k))
    return out
def P(label,x): print(label,'|',len(x),'|',fmt(x)[:330])
P('Q5 στόμα+κοιλία ±1',cfg([anyl('στόμα'),anyl('κοιλία')],1)); P('Q5 ἐκπορεύομαι+στόμα',has(lambda S:N('ἐκπορεύομαι') in S and N('στόμα') in S))
P('Q5 στόμα + unclean (ἀκάθαρτος|κοινόω|ἀκαθαρσία) ±1',cfg([anyl('στόμα'),anyl('ἀκάθαρτος','κοινόω','ἀκαθαρσία','κοινός')],1))
for b,k in [('MT',(15,11)),('MR',(7,15)),('MT',(15,17)),('MR',(7,19)),('RE',(16,13)),('RE',(10,9))]: print('   ',b,k,text(b,k)[:140])
P('Q6 βάλλω+φυλακή',has(lambda S:N('βάλλω') in S and N('φυλακή') in S)); P('Q6 with adversary ±2',cfg([lambda S:N('βάλλω') in S and N('φυλακή') in S,anyl('διάβολος','ἀντίδικος','κατήγωρ','Σατανᾶς','κατήγορος')],2))
P('Q7 ἀγάπη in MT',[x for x in has(anyl('ἀγάπη')) if x[0]=='MT']); P('Q7 ψύχω',has(anyl('ψύχω'))); P('Q7 ψυχρός',has(anyl('ψυχρός')))
P('Q8 γυνή+proph+child+ἀποκτείνω ±3',cfg([anyl('γυνή'),stem('προφῆτ','προφήτ'),anyl('τέκνον','θυγάτηρ','κοράσιον','παιδίον'),anyl('ἀποκτείνω','ἀποκεφαλίζω')],3))
for v in (28,29,30): print('   MT 13:%d'%v,text('MT',(13,v))[:170])
for b,k in [('RE',(7,3)),('RE',(9,4))]: print('   ',b,k,text(b,k)[:170])
P('Q9 ἀδικέω/ἐκριζόω + until + μή/οὔ in verse',has(lambda S:(S&{N('ἀδικέω'),N('ἐκριζόω')}) and (S&{N('ἄχρι'),N('ἕως'),N('μέχρι')})))
for b,k in [('RE',(3,16)),('MT',(5,13)),('RE',(11,2))]: print('   ',b,k,text(b,k)[:170])
P('Q10b cast out (βάλλω fam + ἔξω fam) + tramp (πατέω fam) ±0',has(lambda S:fam(S,'βάλλω','ἐκβάλλω') and fam(S,'ἔξω') and fam(S,'πατέω','καταπατέω')))
P('Q11 δωρεάν',has(anyl('δωρεάν'))); P('Q11 δωρεάν+δίδωμι|λαμβάνω',has(lambda S:N('δωρεάν') in S and (S&{N('δίδωμι'),N('λαμβάνω')})))
P('Q12 αἷμα near θυσιαστήριον ±1',cfg([anyl('αἷμα'),anyl('θυσιαστήριον')],1))
P('X1 hungry+thirsty+naked+clothe+prison ±2',cfg([anyl('πεινάω'),anyl('διψάω'),anyl('γυμνός'),anyl('περιβάλλω'),anyl('φυλακή')],2)); P('X1 γυμνός+περιβάλλω ±1',cfg([anyl('γυμνός'),anyl('περιβάλλω')],1))
P('X2 πατάσσω+ποιμ-',has(lambda S:N('πατάσσω') in S and fam(S,'ποιμ')))
P('X3 συνάγω + στρατ-',has(lambda S:N('συνάγω') in S and fam(S,'στρατ')))
P('X4 θερισμός + send/cast (πέμπω|ἐκβάλλω|ἀποστέλλω|βάλλω) ±1',cfg([anyl('θερισμός'),anyl('πέμπω','ἐκβάλλω','ἀποστέλλω','βάλλω')],1))
P('X5 vineyard/vine + ἔξω fam + ἀποκτείνω|πατέω ±1',cfg([stem('ἀμπελ','ἄμπελ','ληνός'),lambda S:fam(S,'ἔξω'),anyl('ἀποκτείνω','πατέω')],1))
for b,k in [('MT',(21,39)),('MR',(12,8)),('RE',(14,20))]: print('   ',b,k,text(b,k)[:150])
