exec(open('u2.py').read().split("name=lambda V,i")[0])
def rank(xs):
    o=sorted(range(len(xs)),key=lambda i:xs[i]); r=[0]*len(xs); i=0
    while i<len(o):
        j=i
        while j+1<len(o) and xs[o[j+1]]==xs[o[i]]: j+=1
        for k in range(i,j+1): r[o[k]]=(i+j)/2
        i=j+1
    return r
def sp(a,b):
    ra,rb=rank(a),rank(b); n=len(a); ma=sum(ra)/n; mb=sum(rb)/n
    num=sum((x-ma)*(y-mb) for x,y in zip(ra,rb)); da=sum((x-ma)**2 for x in ra)**.5; db=sum((y-mb)**2 for y in rb)**.5
    return num/(da*db)
ms=[q[0] for q in Q]; rs=[q[1] for q in Q]; nR=len(RE)
obs=sp(ms,rs); random.seed(2); N=4000; sh=rs[:]; le=0
for _ in range(N):
    random.shuffle(sh); le+= sp(ms,sh)<=obs
print('rows',len(Q),'| rank correlation Matthew with Revelation:',round(obs,3),'| p (as negative or more):',round((le+1)/(N+1),4))
cuts=[ri[(c,1)] for c in range(2,23)]
def best(r):
    out=[]
    for ci,c in enumerate(cuts):
        rot=[(x-c)%nR for x in r]; out.append((sp(ms,rot),ci+2))
    return out
B=best(rs); 
for v,c in sorted(B,key=lambda x:-abs(x[0]))[:6]: print('   cut before Rev',c,'correlation',round(v,3))
ob=max(abs(v) for v,_ in B); ge=0
for _ in range(1500):
    random.shuffle(sh); ge+= max(abs(v) for v,_ in best(sh))>=ob
print('largest |correlation| over cuts:',round(ob,3),'| corrected p:',round((ge+1)/1501,4))
# by class of evidence and without relational / unchosen
for label,f in [('sealed or blind or engine (not found by reading)',lambda k: cls(L[k]['standing']) in('sealed','blind','engine')),('read or counted',lambda k: cls(L[k]['standing']) in('read','counted'))]:
    sub=[(m,r) for m,r,k in Q if f(k)]; a=[x for x,_ in sub]; b=[y for _,y in sub]; o=sp(a,b); s2=b[:]; le=0
    for _ in range(N): random.shuffle(s2); le+= sp(a,s2)<=o
    print(label,len(sub),'correlation',round(o,3),'p',round((le+1)/(N+1),4))
# the two halves of Matthew, and thirds of Revelation
for lab,lo,hi in [('Matthew 1–13',0,mi[(14,1)]),('Matthew 14–28',mi[(14,1)],len(MT))]:
    sub=[(m,r) for m,r,k in Q if lo<=m<hi]; print(lab,len(sub),'correlation',round(sp([x for x,_ in sub],[y for _,y in sub]),3))
