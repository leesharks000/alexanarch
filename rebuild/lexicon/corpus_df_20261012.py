#!/usr/bin/env python3
"""Document frequency of every lexicon term across the deposited corpus (2026-10-12).

For each term (normalised to lowercase alphanumerics), the number of deposits whose full text contains it as a
whole-word phrase, and which deposits. Superseded deposits and duplicate witnesses are collapsed to their record of
standing, so a work's versions count once. Output: rebuild/lexicon/corpus-df-20261012.json {term_norm: [n, [deposits]]}.
"""
import json, re, pathlib, collections
ROOT = pathlib.Path(__file__).resolve().parents[2]
N = lambda s: re.sub(r"[^a-z0-9]+", " ", (s or "").lower()).strip()
R = json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]
by = {d["deposit_number"]: d for d in R}
def standing(n):
    seen = set()
    while n in by and n not in seen:
        seen.add(n); x = by[n].get("superseded_by_deposit_number") or by[n].get("superseded_by")
        if not isinstance(x, int) or x not in by: break
        n = x
    return n
T = json.loads((ROOT / "data/lexical-minting-registry.json").read_text(encoding="utf-8"))["terms"]
terms = {N(t["term"]) for t in T if N(t["term"])}
L = max(len(k.split()) for k in terms); L = min(L, 8)
df = collections.defaultdict(set)
for d in R:
    p = d.get("full_text_path")
    f = ROOT / p.lstrip("/") if p else None
    if not f or not f.exists(): continue
    w = N(f.read_text(encoding="utf-8", errors="ignore")).split()
    s = standing(d["deposit_number"]); seen = set()
    for i in range(len(w)):
        g = w[i]
        for j in range(1, L + 1):
            if j > 1:
                if i + j > len(w): break
                g = g + " " + w[i + j - 1]
            if g in terms and g not in seen:
                seen.add(g); df[g].add(s)
out = {k: [len(v), sorted(v)[:40]] for k, v in df.items()}
(pathlib.Path(__file__).parent / "corpus-df-20261012.json").write_text(json.dumps(out), encoding="utf-8")
print(len(terms), "terms;", len(out), "found in the corpus")
