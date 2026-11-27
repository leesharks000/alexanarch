import unicodedata,glob,os,collections
from tisch import load
nf=lambda s:unicodedata.normalize('NFC',s)
D='/tmp/fetch/tischendorf-data/word-per-line/2.8/Unicode/'
books=[os.path.basename(f)[:-4] for f in sorted(glob.glob(D+'*.txt'))]
NT={b:load(b) for b in books}
KEYS={b:list(NT[b]) for b in books}
def L(b,k): return {l for l,_,_ in NT[b][k]}
def dist(lems):
    S={nf(x) for x in lems}; return {b:[f'{k[0]}:{k[1]}' for k in KEYS[b] if L(b,k)&S] for b in books if any(L(b,k)&S for k in KEYS[b])}
def near(A,B,w):
    A={nf(x) for x in A}; B={nf(x) for x in B}; out=[]
    for b in books:
        ks=KEYS[b]
        for i,k in enumerate(ks):
            if L(b,k)&A:
                win=ks[max(0,i-w):i+w+1]
                if any(L(b,kk)&B for kk in win): out.append(f'{b} {k[0]}:{k[1]}')
    return out
print('ἔμπορος, ἐμπόριον, ἐμπορία, ἐμπορεύομαι:',dist(['ἔμπορος','ἐμπόριον','ἐμπορία','ἐμπορεύομαι']))
print('ζυγός:',dist(['ζυγός'])); print('μαργαρίτης:',dist(['μαργαρίτης'])); print('δηνάριον:',dist(['δηνάριον'])); print('χοῖνιξ, κριθή, κρίθινος:',dist(['χοῖνιξ','κριθή','κρίθινος']))
print('ἀγοράζω with πωλέω in one verse:',near(['ἀγοράζω'],['πωλέω'],0))
print('ἀγοράζω within one verse of αἷμα:',near(['ἀγοράζω'],['αἷμα'],1))
print('ἀγοράζω or πωλέω within three verses of πλούσιος, πλουτέω, θησαυρός, πτωχός:',near(['ἀγοράζω','πωλέω'],['πλούσιος','πλουτέω','θησαυρός','πτωχός'],3))
print('εἰκών within three verses of ἀγοράζω, πωλέω, δηνάριον:',near(['εἰκών'],['ἀγοράζω','πωλέω','δηνάριον'],3))
print('ἔλαιον within three verses of ἀγοράζω, πωλέω, δηνάριον:',near(['ἔλαιον'],['ἀγοράζω','πωλέω','δηνάριον'],3))
print('οἶνος with ἔλαιον in one verse:',near(['οἶνος'],['ἔλαιον'],0))
print('ἀγοράζω, every verse:',dist(['ἀγοράζω'])); print('πωλέω, every verse:',dist(['πωλέω']))
def txt(b,c,v): return ' '.join(w for _,_,w in NT[b][(c,v)])
for b,c,v in [('RE',3,17),('RE',3,18),('MT',19,21),('MT',19,23),('MT',19,28),('MT',13,44),('MT',13,45),('MT',13,46),('RE',18,11),('RE',18,12),('MT',27,6),('MT',27,7),('MT',27,8),('MT',21,12),('MT',22,19),('MT',22,20),('RE',13,15),('RE',13,16),('MT',25,9),('MT',11,29),('MT',11,30),('RE',6,5),('LU',10,34),('LU',10,35),('JOH',2,16),('JOH',6,7),('JOH',6,9),('JOH',12,5),('AC',1,18),('AC',1,19),('AC',20,28)]:
    print(b,f'{c}:{v}',txt(b,c,v))
