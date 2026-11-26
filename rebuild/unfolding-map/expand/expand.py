#!/usr/bin/env python3
"""Expanding transforms (the author, 17:07). Every transform so far is a selection: the Gospel keeps some members of a longer passage of Revelation. The
other shape: a short seed, one verse, and a long stretch of a Gospel that holds its members and works them, each said again and again. Tested blind:
every verse of a seed book is a seed; its members are its content lemmas (Tischendorf's lemmas; a lemma in more than 120 verses of the New Testament is not
content). For each seed, the 12 verses of a Gospel that expand it most. AN EXPANSION, by a rule fixed here: the stretch holds at least three of the seed's
lemmas, at least half of them, and says them at least twice as many times as there are of them. Counted for Revelation and for other books in its place.
The lemmatized text is Tischendorf's eighth edition, fetched (morphgnt/tischendorf-data, commit 795f2f4f), not seated.
   python3 expand.py <fetch dir> out.json"""
import sys, re, json, math, pathlib, collections, unicodedata
fetch = pathlib.Path(sys.argv[1]) / "tischendorf-data/word-per-line/2.8/Unicode"
def nrm(s):
    s = unicodedata.normalize("NFD", s); return "".join(c for c in s if not unicodedata.combining(c)).lower().replace("ς", "σ")
BK = collections.OrderedDict()
for p in sorted(fetch.glob("*.txt")):
    vs = collections.OrderedDict()
    for l in open(p, encoding="utf-8"):
        q = l.split()
        if len(q) > 7: vs.setdefault(f"{p.stem} {q[1].split('.')[0]}", []).append(nrm(q[7]))
    BK[p.stem] = list(vs.items())
df = collections.Counter(l for b, vs in BK.items() for _, ls in vs for l in set(ls)); NV = sum(len(v) for v in BK.values())
content = lambda l: df[l] <= 120 and len(l) >= 3
idf = lambda l: math.log(NV / df[l])
GOS = ["MT", "MR", "LU", "JOH"]; L = 12
POS = {g: collections.defaultdict(list) for g in GOS}
for g in GOS:
    for i, (_, ls) in enumerate(BK[g]):
        for l in ls:
            if content(l): POS[g][l].append(i)
def best(seed):
    out = None
    for g in GOS:
        n = len(BK[g]); cnt = [collections.Counter() for _ in range(0)]
        # counts per window by sweeping each lemma's positions
        acc = collections.defaultdict(lambda: collections.Counter())
        for l in seed:
            for i in POS[g].get(l, ()):
                for w in range(max(0, i - L + 1), min(i, n - L) + 1): acc[w][l] += 1
        for w, c in acc.items():
            k = len(c); r = sum(c.values())
            if k >= 3 and k >= len(seed) / 2 and r >= 2 * k:
                s = sum(idf(l) * (1 + math.log(x)) for l, x in c.items())
                if out is None or s > out[0]: out = (s, g, w, k, r, dict(c))
    return out
def run(name, verses):
    res, elig = [], 0
    for ref, ls in verses:
        seed = sorted({l for l in ls if content(l)})
        if len(seed) < 3: continue
        elig += 1; b = best(seed)
        if b: res.append(dict(seed=ref, lemmas=seed, score=round(b[0], 2), gospel=b[1], start=BK[b[1]][b[2]][0], end=BK[b[1]][min(len(BK[b[1]]) - 1, b[2] + L - 1)][0], k=b[3], n=len(seed), said=b[4], counts=b[5]))
    res.sort(key=lambda x: -x["score"]); sc = [x["score"] for x in res]
    print(f"{name}: seeds with three or more content lemmas {elig} | seeds with an expansion {len(res)} ({100*len(res)/elig:.1f} per hundred) | with all the seed's lemmas held {sum(1 for x in res if x['k']==x['n'])} | score 40 or more: {sum(1 for s in sc if s >= 40)}; 50 or more: {sum(1 for s in sc if s >= 50)}")
    return dict(eligible=elig, n=len(res), rate=round(100 * len(res) / elig, 2), whole=sum(1 for x in res if x["k"] == x["n"]), ge40=sum(1 for s in sc if s >= 40), ge50=sum(1 for s in sc if s >= 50), top=res[:60])
OUT = {}
OUT["Revelation"] = run("Revelation", BK["RE"])
OUT["Acts"] = run("Acts 1-15", BK["AC"][:405]); OUT["Acts2"] = run("Acts 16-28", BK["AC"][-405:])
OUT["Rom+1Cor"] = run("Romans, 1 Corinthians (first 405)", (BK["RO"] + BK["1CO"])[:405]); OUT["Heb+Jas+1Pet"] = run("Hebrews, James, 1 Peter (first 405)", (BK["HEB"] + BK["JAS"] + BK["1PE"])[:405])
OUT["2Cor.."] = run("2 Corinthians to 1 Thessalonians (first 405)", (BK["2CO"] + BK["GA"] + BK["EPH"] + BK["PHP"] + BK["COL"] + BK["1TH"])[:405])
OUT["1John.."] = run("1-3 John, 1-2 Peter, Jude, James, pastorals (first 405)", (BK["1JO"] + BK["2JO"] + BK["3JO"] + BK["2PE"] + BK["JUDE"] + BK["1TI"] + BK["2TI"] + BK["TIT"])[:405])
print("\nRevelation's strongest, to be read:")
seen = []
for x in OUT["Revelation"]["top"]:
    print(f"  {x['score']:5}  {x['seed']:9} → {x['start']:10}–{x['end'].split()[1]:6} {x['k']}/{x['n']} said {x['said']:2}  {x['counts']}")
json.dump(OUT, open(sys.argv[2], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
