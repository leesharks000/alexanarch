"""Lead-coder reach codes for the 140 generated abstracts (codebooks: ../reach5, ../cont/reachc, ../anal/reacha, unchanged), each
with a 6–30-word span. Verified by machine; a span whose only difference from the source is a straight for a curly apostrophe
is replaced by the exact source characters. Output codes-gen.jsonl."""
import json,re
from codes_in import C
G={g["id"]:g for g in json.load(open("gen.json"))}
def norm(s): return s.replace("’","'").replace("‘","'")
out=[];bad=[]
for j,L in C.items():
    assert len(L)==20,(j,len(L))
    for n,(code,q) in enumerate(L,1):
        g=G[f"gen-{j}-{n:02d}"]; t=g["text"]; k=norm(t).find(norm(q))
        if k<0 or not 6<=len(q.split())<=30: bad.append((g["id"],len(q.split()),q[:50])); continue
        out.append({"id":g["id"],"j":j,"field":g["field"],"code":code,"dir":"","quote":t[k:k+len(q)]})
open("codes-gen.jsonl","w").write("".join(json.dumps(r,ensure_ascii=False)+"\n" for r in out))
print(len(out),"valid; bad:",bad)
