import sys,glob,os,unicodedata,collections,re
sys.path.insert(0,'/home/claude/unfold/map'); from tisch import load
nf=lambda s:unicodedata.normalize('NFC',s)
D='/tmp/fetch/tischendorf-data/word-per-line/2.8/Unicode/'
books=[os.path.basename(f)[:-4] for f in sorted(glob.glob(D+'*.txt'))]
NT={b:load(b) for b in books}
def L(b,k): return {l for l,_,_ in NT[b][k]}
def has(pred): return [(b,k) for b in books for k in NT[b] if pred(L(b,k))]
def fam(S,*stems): return any(any(l.startswith(nf(s)) for s in stems) for l in S)
def fmt(x): return ', '.join(f'{b} {c}:{v}' for b,(c,v) in x)
def win(b,k,w):
    ks=list(NT[b]); i=ks.index(k); return set().union(*[L(b,q) for q in ks[max(0,i-w):i+w+1]])
def near(p1,p2,w):
    out=[]
    for b in books:
        for k in NT[b]:
            if p1(L(b,k)) and p2(win(b,k,w)): out.append((b,k))
    return out
def text(b,k): return ' '.join(w for _,_,w in NT[b][k])
print('P1 ἐκκλησία gospels:',fmt([x for x in has(lambda S:nf('ἐκκλησία') in S) if x[0] in('MT','MR','LU','JOH')]),'| RE count',sum(1 for k in NT['RE'] for l,_,_ in NT['RE'][k] if l==nf('ἐκκλησία')))
print('P2 ἐλέγχω in MT:',fmt([x for x in has(lambda S:nf('ἐλέγχω') in S) if x[0]=='MT']),'| near ἐκκλησία ±2:',fmt(near(lambda S:nf('ἐλέγχω') in S,lambda S:nf('ἐκκλησία') in S,2)))
see=lambda S:fam(S,'βλέπω','ὁράω','θεωρέω','εἶδον','ὀπτάνομαι','θεάομαι')
p3=has(lambda S:see(S) and nf('πρόσωπον') in S); print('P3',fmt(p3))
for b,k in p3: print('   ',b,k,text(b,k)[:150])
print('P4 σκανδαλ in RE:',fmt([x for x in has(lambda S:fam(S,'σκάνδαλ','σκανδαλ')) if x[0]=='RE']))
for b,k in [('MT',(18,6)),('MR',(9,42)),('LU',(17,2)),('RE',(18,21)),('RE',(2,14))]: print('   ',b,k,sorted(L(b,k)))
kl=lambda S:nf('κλείς') in S; dl=lambda S:nf('δέω') in S; ll=lambda S:nf('λύω') in S
print('P5 κλείς near δέω&λύω ±2:',fmt([x for x in has(kl) if dl(win(*x,2)) and ll(win(*x,2))]),'| δέω+λύω one verse:',fmt(has(lambda S:dl(S) and ll(S))))
print('P6 ἐν μέσῳ (μέσος) verses with εἰμί/ἵστημι first or third person — list μέσος in gospels+RE:',len([x for x in has(lambda S:nf('μέσος') in S)]))
for b,k in has(lambda S:nf('μέσος') in S):
    if b in('MT','LU','JOH','RE') and re.search(r'ἐν μέσῳ',text(b,k)): print('   ',b,k,text(b,k)[:110])
print('P7 Σόδομα:',fmt(has(lambda S:fam(S,'Σόδομα'))),'| with πόλις:',fmt(has(lambda S:fam(S,'Σόδομα') and nf('πόλις') in S)))
print('P8 τέλος with ὑπομένω/τηρέω/κατέχω/βέβαιος:',fmt(has(lambda S:nf('τέλος') in S and (S&{nf('ὑπομένω'),nf('τηρέω'),nf('κατέχω'),nf('βέβαιος')}))))
print('P9 φεύγω+ὀργή:',fmt(has(lambda S:nf('φεύγω') in S and nf('ὀργή') in S)),'| ὀργή with ἀπό:',fmt(has(lambda S:nf('ὀργή') in S and nf('ἀπό') in S)),'| ὀργή+ἔρχομαι/μέλλω:',fmt(has(lambda S:nf('ὀργή') in S and (S&{nf('ἔρχομαι'),nf('μέλλω')}))))
def content(b,ks): return {l for k in ks for l,t,_ in NT[b][k] if t[:2] in('N-','A-','V-')}
m3=content('MT',[(3,v) for v in range(7,13)]); r14=content('RE',[(14,v) for v in range(14,21)]); r146=content('RE',[(14,v) for v in range(6,21)])
print('P10 shared MT3:7-12 ~ RE14:14-20:',sorted(m3&r14),'| ~RE14:6-20:',sorted(m3&r146))
th=lambda S:fam(S,'θεραπ'); print('P11 θεραπ near ἔθνος ±3:',fmt(near(th,lambda S:nf('ἔθνος') in S,3)))
print('P12 dog words:',fmt(has(lambda S:S&{nf('κύων'),nf('κυνάριον')})))
print('P13 τηρέω+ἐντολή/ἐντέλλω:',fmt(has(lambda S:nf('τηρέω') in S and fam(S,'ἐντολή','ἐντέλλ'))))
for b,k in [('MT',(10,1)),('MR',(6,7)),('LU',(9,1))]: print('P14',b,k,sorted(content(b,[k])&content('RE',[(11,v) for v in range(3,7)])))
