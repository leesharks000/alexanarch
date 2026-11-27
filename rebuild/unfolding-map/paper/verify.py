import re,sys,unicodedata as U
S='/home/claude/repos/alexanarch/data/corpora/gnt-nestle1904/text/'
V={}
for b in ('Matt','Rev'):
    for l in open(S+b+'.txt',encoding='utf-8'):
        r,t=l.rstrip('\n').split('\t',1); V[r]=t
LX='/home/claude/repos/alexanarch/data/corpora/lxx-swete/text/'
for ab,fn,pre in (('Exod','tlg002-Ἔξοδος','Ἔξοδος'),('Num','tlg004-Ἀριθμοί','Ἀριθμοί'),('Deut','tlg005-Δευτερονόμιον','Δευτερονόμιον'),('Isa','tlg048-Ἠσαΐας','Ἠσαΐας'),('Ezek','tlg053-Ἰεζεκιήλ','Ἰεζεκιήλ'),('Ps','tlg027-Ψαλμοί','Ψαλμοί')):
    for l in open(LX+fn+'.txt',encoding='utf-8'):
        if '\t' not in l: continue
        r,t=l.rstrip('\n').split('\t',1)
        if r.startswith(pre+' '): V[ab+' '+r[len(pre)+1:]]=t
PHD='/home/claude/repos/alexanarch/data/corpora/philo/text/'
V['Philo Spec']=open(PHD+'tlg024-De_specialibus_legibus_lib_i_iv_.txt',encoding='utf-8').read()
V['Philo Decal']=open(PHD+'tlg023-De_decalogo.txt',encoding='utf-8').read()
for ab,fn in (('Somn','tlg019-De_somniis_lib_i_ii_'),('Fug','tlg017-De_fuga_et_inventione'),('Cher','tlg003-De_Cherubim'),('Plant','tlg010-De_plantatione'),('Her','tlg015-Quis_rerum_divinarum_heres_sit'),('Leg','tlg002-Legum_allegoriarum_libri_i_iii'),('Agr','tlg009-De_agricultura'),('Mut','tlg018-De_mutatione_nominum'),('Conf','tlg013-De_confusione_linguarum')):
    V['Philo '+ab]=open(PHD+fn+'.txt',encoding='utf-8').read()
def norm(s,loose=False):
    s=U.normalize('NFD',s)
    s=s.replace('̀','́')  # grave -> acute
    if loose: s=''.join(c for c in s if not U.combining(c))
    s=U.normalize('NFC',s).replace('’',"'").replace('᾽',"'").replace('ʼ',"'")
    return [w.lower() for w in re.findall(r"[^\W\d_]+'?",s)]
def sub(a,b):
    n=len(a); return any(b[i:i+n]==a for i in range(len(b)-n+1))
src=open('draft.src.md',encoding='utf-8').read()
bad=0;n=0
for m in re.finditer(r'⟦([^|⟧]+)\|([^⟧]+)⟧',src):
    ref,q=m.group(1),m.group(2); n+=1
    if ref not in V: print('NOREF',ref); bad+=1; continue
    if sub(norm(q),norm(V[ref])): continue
    tag='CASE/ACCENT' if sub(norm(q,True),norm(V[ref],True)) else 'FAIL'
    bad+=1; print(tag,ref,'|',q,'\n    seat:',V[ref])
print(n,'quotations;',bad,'not exact')
if '--render' in sys.argv and not bad:
    out=re.sub(r'⟦[^|⟧]+\|([^⟧]+)⟧',r'\1',src)
    T='/home/claude/unfold/tm/'
    def passage(f,start):
        t=open(T+f,encoding='utf-8').read(); t=t[t.index(start)+len(start):]
        m=re.search(r'\n(#+ |PART \d)',t); t=t[:m.start()] if m else t
        return t.strip()
    m20='\n\n'.join(f"{r.split(':')[1]} {V[r]}" for r in [f'Matt 20:{i}' for i in range(1,17)])
    app=open('appendix.head.md',encoding='utf-8').read()
    app=app.replace('{{A}}',passage('round1/a-sonnet.md','PART 2. THE PASSAGE')).replace('{{F}}',passage('round2/f-sonnet.md','# PART 2 — THE PASSAGE')).replace('{{G}}',passage('round2/g-opus.md','# PASSAGE')).replace('{{M}}',m20)
    i=out.index('## Works cited'); out=out[:i]+app+'\n---\n\n'+out[i:]
    assert '⟦' not in out and '⟧' not in out
    open('/mnt/user-data/outputs/HOW-TO-WRITE-MATTHEW-FROM-REVELATION-draft-v0.7.md','w',encoding='utf-8').write(out)
    print('rendered',len(out.split()),'words')
