#!/usr/bin/env python3
"""EA-CORPORA-31 (session tool): a locus whose Unicode form differs from the seated text's (the First1KGreek commentators mix
composed and decomposed Greek) is rewritten in the text's own characters, found by comparing NFC forms cluster by cluster.
    python3 nfcfix31.py <spec.json> <stage>"""
import json, sys, pathlib, unicodedata
spec_p = pathlib.Path(sys.argv[1]); sp = json.load(open(spec_p)); seat = pathlib.Path(sys.argv[2]) / sp["corpus"]
def norm(s): return " ".join(s.split())
for lo in sp["loci"]:
    t = norm((seat / lo["text"]).read_text(encoding="utf-8"))
    if norm(lo["find"]) in t:
        continue
    cl = []
    for i, c in enumerate(t):
        if cl and unicodedata.combining(c):
            cl[-1][1] = i + 1
        else:
            cl.append([i, i + 1])
    nf, mp = [], []
    for a, b in cl:
        s = unicodedata.normalize("NFC", t[a:b]); nf.append(s); mp += [(a, b)] * len(s)
    nf = "".join(nf); target = unicodedata.normalize("NFC", norm(lo["find"]))
    k = nf.find(target)
    if k < 0:
        print("NOT FOUND", lo["label"]); continue
    lo["find"] = t[mp[k][0]:mp[k + len(target) - 1][1]]
    lo["note"] = "the TEI mixes composed and decomposed Greek; the locus is given in the text's own characters"
    print("fixed", lo["label"][:60])
spec_p.write_text(json.dumps(sp, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
