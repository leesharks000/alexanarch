import sys,json,collections
sys.path.insert(0,'/home/claude/unfold/seats')
import tisch
B=['MT','MR','LU','JOH','AC','RO','1CO','2CO','GA','EPH','PHP','COL','1TH','2TH','1TI','2TI','TIT','PHM','HEB','JAS','1PE','2PE','1JO','2JO','3JO','JUDE','RE']
D={}
for b in B:
    try: D[b]=tisch.load(b)
    except Exception as e: print('skip',b,e)
import unicodedata as U
n=lambda s:U.normalize('NFC',s)
def L(b,k): return [x[0] for x in D[b][k]]
def verses(f):
    return [(b,k) for b in D for k in D[b] if f(L(b,k))]
def near(b,k,lem,w=1):
    ks=list(D[b].keys()); i=ks.index(k)
    return any(lem in L(b,ks[j]) for j in range(max(0,i-w),min(len(ks),i+w+1)))
def vn(a,c,w=1):
    return [(b,k) for b in D for k in D[b] if a in L(b,k) and near(b,k,c,w)]
p=lambda t,x:print(t,len(x),x[:14])
p('sword twice',verses(lambda l:l.count(n('μάχαιρα'))>=2))
p('zygos',verses(lambda l:n('ζυγός') in l))
p('harvest+angel',verses(lambda l:n('θερισμός') in l and n('ἄγγελος') in l))
x=verses(lambda l:n('βάλλω') in l and n('πῦρ') in l); p('ballo+pyr',x); print(collections.Counter(b for b,_ in x))
p('emporos~pearl',vn(n('ἔμπορος'),n('μαργαρίτης')))
p('buy~blood',vn(n('ἀγοράζω'),n('αἷμα')))
p('barley',verses(lambda l:n('κριθή') in l or n('κρίθινος') in l))
p('oil+wine',verses(lambda l:n('ἔλαιον') in l and n('οἶνος') in l))
p('barley~denarius',[(b,k) for b in D for k in D[b] if (n('κριθή') in L(b,k) or n('κρίθινος') in L(b,k)) and near(b,k,n('δηνάριον'),2)])
j=json.load(open('/home/claude/unfold/map/rev-matthew-ledger.json'))
rows=j if isinstance(j,list) else j.get('rows',j)
print(len(rows)); print(collections.Counter(str(r.get('move')) for r in rows))
