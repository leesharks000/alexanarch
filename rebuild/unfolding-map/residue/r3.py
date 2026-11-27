exec(open('r1.py').read().split("print('P1")[0])
N=nf
def allin(*ls): return lambda S: all(N(x) in S for x in ls)
def nearall(ls,w):  # verses whose ±w window holds all lemmas, reported by place (book, chapter) clusters
    out=[]
    for b in books:
        for k in NT[b]:
            W=win(b,k,w)
            if all(N(x) in W for x in ls) and any(N(x) in L(b,k) for x in ls): out.append((b,k))
    return out
def P(label,x): print(label,'|',len(x),'|',fmt(x)[:400])
P('A ψευδοπροφήτης+πλανάω',has(allin('ψευδοπροφήτης','πλανάω')))
P('A σημεῖον+μέγας+πλανάω ±1',nearall(['σημεῖον','μέγας','πλανάω'],1))
P('B κάθημαι+νεφέλη+ἄνθρωπος',has(allin('κάθημαι','νεφέλη','ἄνθρωπος')))
P('C εὐαγγέλιον+πᾶς+ἔθνος',has(allin('εὐαγγέλιον','πᾶς','ἔθνος')))
P('D κληρονομέω+ἑτοιμάζω ±1',nearall(['κληρονομέω','ἑτοιμάζω'],1)); P('D καταβολή',has(allin('καταβολή')))
P('E σύνδουλος',has(allin('σύνδουλος'))); P('E σύνδουλος+πίπτω+προσκυνέω ±3',nearall(['σύνδουλος','πίπτω','προσκυνέω'],3))
P('F δεικνύω+δεῖ',has(allin('δεικνύω','δεῖ'))); P('F δεῖ+ἀποκτείνω',has(allin('δεῖ','ἀποκτείνω')))
P('G βασανίζω',has(allin('βασανίζω'))); P('G βασανίζω+καιρός',has(allin('βασανίζω','καιρός')))
P('H πωλέω+ἀγοράζω',has(allin('πωλέω','ἀγοράζω')))
P('I θύρα+κλείω+ἀνοίγω ±1',nearall(['θύρα','κλείω','ἀνοίγω'],1)); P('I λαμπάς',has(allin('λαμπάς')))
six=['θύρα','κλείω','ἀνοίγω','ἀγοράζω','γρηγορεύω','ὥρα']
best=[]
for b in books:
    ks=list(NT[b])
    for i in range(len(ks)):
        W=set().union(*[L(b,q) for q in ks[i:i+18]]); n=sum(N(x) in W for x in six)
        if n>=5: best.append((b,ks[i],n))
import itertools
print('I windows of 18 verses with >=5 of six:',sorted({(b,k[0],n) for b,k,n in best}))
P('J ποτήριον+πίνω',has(allin('ποτήριον','πίνω')))
P('K γρηγορεύω+ὥρα',has(allin('γρηγορεύω','ὥρα')))
P('L σάλπιγξ',has(allin('σάλπιγξ'))); P('L ἄγγελος+σάλπιγξ',has(allin('ἄγγελος','σάλπιγξ'))); P('L τέσσαρες+ἄνεμος',has(allin('τέσσαρες','ἄνεμος')))
P('M κάμινος',has(allin('κάμινος')))
P('N θρόνος+κάθημαι',has(allin('θρόνος','κάθημαι'))); P('N θρόνος+κάθημαι+ὀμνύω ±2',nearall(['θρόνος','κάθημαι','ὀμνύω'],2))
P('O πνέω+ἄνεμος',has(allin('πνέω','ἄνεμος'))); P('O ποταμός MT',[x for x in has(allin('ποταμός')) if x[0]=='MT'])
P('Q ὄρος+βάλλω+θάλασσα',has(allin('ὄρος','βάλλω','θάλασσα'))); P('Q συκῆ',has(allin('συκῆ'))); P('Q συκῆ near ἀστήρ+πίπτω ±4',[x for x in has(allin('συκῆ')) if N('ἀστήρ') in win(*x,4) and N('πίπτω') in win(*x,4)])
P('R βλασφημέω+βλασφημία',has(allin('βλασφημέω','βλασφημία')))
P('S κρατέω+δέω',has(allin('κρατέω','δέω'))); P('S κρατέω+δέω+φυλακή ±5',nearall(['κρατέω','δέω','φυλακή'],5))
P('T ἀκολουθέω+ὅπου',has(allin('ἀκολουθέω','ὅπου')))
P('U καυματίζω',has(allin('καυματίζω')))
P('V ἑτοιμάζω+ὁδός',has(allin('ἑτοιμάζω','ὁδός')))
P('W ἀναβαίνω+ἀνοίγω+οὐρανός+φωνή ±1',nearall(['ἀναβαίνω','ἀνοίγω','οὐρανός','φωνή'],1)); P('W ἀνοίγω+οὐρανός',has(allin('ἀνοίγω','οὐρανός')))
P('X θεραπεύω in RE',[x for x in has(allin('θεραπεύω')) if x[0]=='RE']); P('X θεραπεύω+θαυμάζω ±1',nearall(['θεραπεύω','θαυμάζω'],1)); P('X θεραπεύω+ἐξουσία',has(allin('θεραπεύω','ἐξουσία')))
P('Y ὄνομα+πατήρ',has(allin('ὄνομα','πατήρ')))
P('Z μέσος+ἀποστέλλω',has(allin('μέσος','ἀποστέλλω')))
P('P2b ἐλέγχω near ἐκκλησία ±3',near(lambda S:N('ἐλέγχω') in S,lambda S:N('ἐκκλησία') in S,3))
P('P6b ἐκκλησία+μέσος+ὄνομα ±3',nearall(['ἐκκλησία','μέσος','ὄνομα'],3))
P('P11b θεραπ+ἔθνος+ὄνομα ±3',[x for x in near(lambda S:fam(S,'θεραπ'),lambda S:N('ἔθνος') in S,3) if N('ὄνομα') in win(*x,3)])
P('P10b χείρ + (πτύον|δρέπανον)',has(lambda S:N('χείρ') in S and (S&{N('πτύον'),N('δρέπανον')})))
P('τηρέω+ἐντολή MT',[x for x in has(allin('τηρέω','ἐντολή')) if x[0] in('MT','MR','LU')])
