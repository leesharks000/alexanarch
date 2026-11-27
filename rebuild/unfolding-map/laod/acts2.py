import collections,unicodedata,re,glob,io,contextlib
with contextlib.redirect_stdout(io.StringIO()): exec(open('acts.py').read().split("out={}")[0])
def nrm(s):
    s=unicodedata.normalize('NFD',s.lower()); return ''.join(c for c in s if (c.isalpha() or c.isspace()) and not unicodedata.combining(c)).replace('ς','σ')
LX=set()
for f in glob.glob('/home/claude/repos/alexanarch/data/corpora/lxx-swete/text/*.txt'):
    ws=[]
    for l in open(f,encoding='utf8',errors='ignore'):
        if '\t' in l: ws+=nrm(l.split('\t',1)[1]).split()
    LX|={tuple(ws[i:i+4]) for i in range(len(ws)-3)}
print('LXX 4-word sequences:',len(LX))
for src in ['AC','RE']:
    for g in ['MT','MR','LU','JOH']:
        sh=[x for x in G[src] if x in G[g]]; inl=[x for x in sh if x in LX]; rest=[x for x in sh if x not in LX]
        print(f"{src}x{g}: shared {len(sh)}; also in the Septuagint {len(inl)} ({100*len(inl)/len(sh):.0f}%); not in the Septuagint {len(rest)} = {1000*len(rest)/len(W[g]):.2f} per 1,000")
    three=set().union(*[set(G[o]) for o in ['MT','MR','JOH']]); r=[x for x in G[src] if x in three and x not in LX]; a=[x for x in G[src] if (x in three or x in G['LU']) and x not in LX]
    print(f"   {src}: not in the Septuagint, per 1,000 words of the source: all four {1000*len(a)/len(W[src]):.2f}; without Luke {1000*len(r)/len(W[src]):.2f}")
import random
random.seed(2)
for src in ['AC','RE']:
    three=set().union(*[set(G[o]) for o in ['MT','MR','JOH']]); r=[' '.join(x) for x in G[src] if x in three and x not in LX]; random.shuffle(r)
    print(src,'sample, shared with Matt/Mark/John and not in the Septuagint:\n   '+' | '.join(r[:28]))
