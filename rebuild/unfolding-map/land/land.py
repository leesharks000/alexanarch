import sys,re,collections,unicodedata as U
sys.path.insert(0,'/home/claude/unfold/seats'); import tisch
SP={'σῴζω':'σώζω','ἀποθνῄσκω':'ἀποθνήσκω'}
n=lambda s:U.normalize('NFC',SP.get(U.normalize('NFC',s),s))
B=['MT','MR','LU','JOH','AC','RO','1CO','2CO','GA','EPH','PHP','COL','1TH','2TH','1TI','2TI','TIT','PHM','HEB','JAS','1PE','2PE','1JO','2JO','3JO','JUDE','RE']
D={}
for b in B:
    try: D[b]=tisch.load(b)
    except Exception as e: print('skip',b)
K={b:list(D[b]) for b in D}
W={b:[D[b][k] for k in K[b]] for b in D}
LS={b:[set(x[0] for x in v) for v in W[b]] for b in D}
allL=set().union(*[s for b in LS for s in LS[b]])
def ck(*xs):
    for x in xs:
        if n(x) not in allL: print('   !! lemma not in text:',x)
def ref(b,i): return f'{b} {K[b][i][0]}:{K[b][i][1]}'
def co(*sets,w=0):
    """each arg a list of alternative lemmas; all must stand within window w of verse i (first arg in verse i)"""
    sets=[[n(x) for x in s] for s in sets]
    for s in sets: ck(*s)
    out=[]
    for b in D:
        for i in range(len(K[b])):
            if not any(x in LS[b][i] for x in sets[0]): continue
            win=set().union(*LS[b][max(0,i-w):i+w+1])
            if all(any(x in win for x in s) for s in sets[1:]): out.append(ref(b,i))
    return out
def show(t,x): print(t,len(x),x if len(x)<=28 else x[:28]+['…'])
# J1 holy city as phrase: adjacent tokens
x=[]
for b in D:
    for i,v in enumerate(W[b]):
        L=[t[0] for t in v]
        for j in range(len(L)-1):
            for a in range(1,3):
                if j+a<len(L) and {L[j],L[j+a]}=={n('ἅγιος'),n('πόλις')}:
                    x.append(ref(b,i)); break
show('J1 holy city',sorted(set(x),key=x.index))
show('J2 Egypt',co(['Αἴγυπτος'])); show('   Sodom',co(['Σόδομα']))
show('J3 libanos',co(['λίβανος'])); show('   +gold w1',co(['λίβανος'],['χρυσός','χρυσίον'],w=1))
show('J4 mountain high show',co(['ὄρος'],['ὑψηλός'],['δείκνυμι'])); show('   mountain high',co(['ὄρος'],['ὑψηλός']))
# J5
x=[]
for b in D:
    for i,v in enumerate(W[b]):
        L=[t[0] for t in v]; 
        if n('τέκνον') in L:
            fem=any(t[0]==n('αὐτός') and re.search(r'GSF|G-SF|-GSF',t[1]) for t in v)
            win=set().union(*LS[b][max(0,i-1):i+2])
            if fem and (n('ἀποκτείνω') in win or n('ἀναιρέω') in win): x.append(ref(b,i))
show('J5 her children killed',x); show('   teknon+kill w1 (any possessor)',co(['τέκνον'],['ἀποκτείνω','ἀναιρέω'],w=1))
x=[]
for b in D:
    for i,v in enumerate(W[b]):
        for t in v:
            if t[0]==n('ἀστήρ') and re.search(r'N-[NGDA]SM',t[1]): x.append(ref(b,i)+' '+t[2])
show('J6 star singular',x)
show('J7 hunger+thirst',co(['πεινάω'],['διψάω']))
show('J8 rejoice+exult',co(['χαίρω'],['ἀγαλλιάω']))
x=[]
for b in D:
    for i,v in enumerate(W[b]):
        for t in v:
            if t[0]==n('κληρονομέω') and re.search(r'V-F',t[1]): x.append(ref(b,i)+' '+t[2])
show('J9 inherit future',x)
# J10 knot window 30
need=[[n('κύων')],[n('μαργαρίτης')],[n('πύλη'),n('πυλών')],[n('εἰσέρχομαι')],[n('ἅγιος')]]
ck('κύων','μαργαρίτης','πύλη','πυλών')
x=[]
for b in D:
    for i in range(len(K[b])):
        win=set().union(*LS[b][i:i+30])
        c=sum(any(a in win for a in s) for s in need)
        if c>=4 and any(a in LS[b][i] for s in need for a in s): x.append((ref(b,i),c))
print('J10 knot (>=4 of 5 in 30 verses, starting verse holds one):',[(r,c) for r,c in x])
show('    dog',co(['κύων'])); show('    pearl',co(['μαργαρίτης'])); show('    enter+gate',co(['εἰσέρχομαι'],['πύλη','πυλών']))
show('J11 peirasmos + keep/rescue/lead',co(['πειρασμός'],['τηρέω','ῥύομαι','εἰσφέρω','εἰσέρχομαι']))
show('J12 swear+heaven',co(['ὀμνύω'],['οὐρανός'])); show('    swear',co(['ὀμνύω']))
show('J13 city+mountain',co(['πόλις'],['ὄρος']))
show('    lampstand',co(['λυχνία']))
show('J15 blood+prophet',co(['αἷμα'],['προφήτης']))
show('J16 blood+pour+earth w1',co(['αἷμα'],['ἐκχέω','ἐκχύννω','ἐκχύνω'],['γῆ'],w=1)); show('    blood+pour',co(['αἷμα'],['ἐκχέω','ἐκχύννω','ἐκχύνω']))
show('J17 blind',co(['τυφλός']))
show('J18 Satan+cast',co(['Σατανᾶς'],['βάλλω','ἐκβάλλω']))
# J14: λέγω ... καὶ οὐ(κ) + εἰμί/ποιέω within 6 tokens
x=[]
for b in D:
    for i,v in enumerate(W[b]):
        L=[t[0] for t in v]
        for j,l in enumerate(L):
            if l==n('λέγω'):
                for k in range(j+1,min(len(L)-2,j+8)):
                    if L[k]==n('καί') and L[k+1]==n('οὐ') and L[k+2] in (n('εἰμί'),n('ποιέω')):
                        x.append(ref(b,i))
show('J14 say and are/do not',sorted(set(x),key=x.index))
# extras
show('E woe count by book',[]); print('   ',collections.Counter(b for b in D for v in W[b] for t in v if t[0]==n('οὐαί')))
show('E makarios by book',[]); print('   ',collections.Counter(b for b in D for v in W[b] for t in v if t[0]==n('μακάριος')))
show('E desolate house/city: eremoo',co(['ἐρημόω'])); 
show('E save in sea stories (σώζω + θάλασσα|πλοῖον w2)',co(['σώζω'],['θάλασσα','πλοῖον'],w=2))
show('E stand/walk on sea',co(['θάλασσα'],['περιπατέω','ἵστημι'],['ἐπί']))
show('E east+king|magos',co(['ἀνατολή'],['βασιλεύς','μάγος'],w=1))
show('E false prophet',co(['ψευδοπροφήτης']))
show('E given authority (didomi passive + exousia)',[ref(b,i) for b in D for i,v in enumerate(W[b]) if n('ἐξουσία') in LS[b][i] and any(t[0]==n('δίδωμι') and re.search(r'V-AP',t[1]) for t in v)])
show('E heaven+earth pass',co(['οὐρανός'],['γῆ'],['παρέρχομαι','ἀπέρχομαι']))
show('E wilderness+place',co(['ἔρημος'],['τόπος']))
show('E wilderness+nourish/feed',co(['ἔρημος','ἐρημία'],['τρέφω','χορτάζω'],w=2))
show('E come+worship',co(['προσκυνέω'],['ἥκω']))
show('E will+thy: thelema',co(['θέλημα'],['σύ']))
