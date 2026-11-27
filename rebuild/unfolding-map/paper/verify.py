import re,sys,unicodedata as U
S='/home/claude/repos/alexanarch/data/corpora/gnt-nestle1904/text/'
V={}
for b in ('Matt','Rev'):
    for l in open(S+b+'.txt',encoding='utf-8'):
        r,t=l.rstrip('\n').split('\t',1); V[r]=t
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
    assert '⟦' not in out and '⟧' not in out
    open('/mnt/user-data/outputs/HOW-TO-WRITE-MATTHEW-FROM-REVELATION-draft-v0.1.md','w',encoding='utf-8').write(out)
    print('rendered',len(out.split()),'words')
