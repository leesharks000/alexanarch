import sys, re, hashlib
sys.path.insert(0,'.'); from cases import *
def norm(s): return re.sub(r'\s+',' ',s)
fail=0; txt={k:norm(open(v['file'],encoding='utf-8').read()) for k,v in SOURCES.items()}
art={k:norm(open(v['file'],encoding='utf-8').read()) for k,v in ARTICLES.items()}
for c in CASES:
    if norm(c['w']) not in art[c['art']]: print('SENTENCE MISS',c['id']); fail+=1
    for s,a,n in c['windows']:
        if a not in txt[s]: print('WINDOW MISS',c['id'],s,a[:50]); fail+=1
    for s,q in c['reading']['spans']:
        if norm(q) not in txt[s]: print('SPAN MISS',c['id'],s,q[:70]); fail+=1
print('checked',len(CASES),'cases; failures',fail)
for k,v in {**SOURCES,**ARTICLES}.items(): print(k, hashlib.sha256(open(v['raw'],'rb').read()).hexdigest()[:16])
