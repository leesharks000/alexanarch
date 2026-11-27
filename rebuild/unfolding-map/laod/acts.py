import collections,json,unicodedata,re
from tisch import load
def words(b):
    o=[]
    for k,t in load(b).items():
        for l,tg,w in t:
            w=unicodedata.normalize('NFD',w.lower()); w=''.join(c for c in w if c.isalpha() and not unicodedata.combining(c)).replace('ς','σ')
            if w: o.append(w)
    return o
W={b:words(b) for b in ['MT','MR','LU','JOH','AC','RE','RO','HEB','1CO']}
def grams(ws,n=4): return collections.Counter(tuple(ws[i:i+n]) for i in range(len(ws)-n+1))
G={b:grams(W[b]) for b in W}
print('words:',{b:len(W[b]) for b in W})
out={}
for src in ['AC','RE','RO','HEB','1CO']:
    row={}
    for g in ['MT','MR','LU','JOH']:
        sh=[x for x in G[src] if x in G[g]]; row[g]=(len(sh),1000*len(sh)/len(W[g]))
    # shared with a Gospel but with no other Gospel (peculiar to that Gospel)
    pec={}
    for g in ['MT','MR','LU','JOH']:
        others=[o for o in ['MT','MR','LU','JOH'] if o!=g]; pec[g]=sum(1 for x in G[src] if x in G[g] and not any(x in G[o] for o in others))
    three=set().union(*[set(G[o]) for o in ['MT','MR','JOH']]); n3=sum(1 for x in G[src] if x in three); w3=sum(len(W[o]) for o in ['MT','MR','JOH'])
    allg=set().union(*[set(G[o]) for o in ['MT','MR','LU','JOH']]); na=sum(1 for x in G[src] if x in allg)
    out[src]=dict(row=row,pec=pec,three=(n3,1000*n3/w3),per_src=1000*na/len(W[src]),per_src_noLuke=1000*n3/len(W[src]))
    print(f"{src}: shared 4-word sequences per 1,000 words of the Gospel: "+'  '.join(f"{g} {row[g][1]:.2f} ({row[g][0]})" for g in row)+f" | Matt+Mark+John together {1000*n3/w3:.2f} | peculiar to one Gospel: {pec} | per 1,000 words of the source: all four {1000*na/len(W[src]):.2f}, without Luke {1000*n3/len(W[src]):.2f}")
json.dump(out,open('acts.json','w'))
