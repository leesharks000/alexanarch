"""Second baseline (2026-11-15): Plato/Aristotle titles in Philologus (1846–) and Classical Quarterly (1907–), hand-ruled S (a work's standing)
and T (text/fragment) from a lexicon pull, as in ../standing.py."""
import json,collections
S={"philologus":"1842 3670 3730 3868 4131 4968 5348 5379 5673 108 7661".split(),
   "cq":"4293 2643 5807 1218 1152 2324 2936 4539 2059 4513 4394 5513 6128 3467".split()}
T={"philologus":"1584 1765 1795 4355 6059 6062 7963 8030".split(),
   "cq":"5302 5780 1112 2342 2267 3711 2700 2065 4353 2611 3752 1605 621 5013 5036 5945 5963 6000 6170 6463 6508".split()}
def P(y): return "1846–99" if y<1900 else "1900–39" if y<1940 else "1940–69" if y<1970 else "1970–99" if y<2000 else "2000–26"
for n in ["philologus","cq"]:
    C=[c for c in json.load(open(f"codes-{n}.json")) if c["group"] in ("Plato","Aristotle") and c["year"]]
    tot=collections.Counter(); s=collections.Counter(); t=collections.Counter()
    for c in C:
        p=P(c["year"]); tot[p]+=1; s[p]+=str(c["n"]) in S[n]; t[p]+=str(c["n"]) in T[n]
    print(n); [print(f"  {p:8} P+A titles {tot[p]:4}  S {s[p]:3} ({100*s[p]/tot[p]:4.1f}%)  T {t[p]:3} ({100*t[p]/tot[p]:4.1f}%)") for p in sorted(tot) if tot[p]]
