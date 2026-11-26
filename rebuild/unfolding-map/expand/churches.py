#!/usr/bin/env python3
"""Expansion again, on ROOTS (the first four letters of the lemma, so that ποιμαίνω joins ποιμήν and δωρεάν joins δωρεά), and with the letters to the seven
churches (Rev 2-3) taken apart from the rest: each verse a seed, and each of the seven promises 'to the one who conquers' a seed. The rule of expand.py,
unchanged: at least three of the seed's roots, at least half, said at least twice as often as there are of them. A root in more than 150 verses is not content.
   python3 churches.py <fetch dir> out.json"""
import sys, re, json, math, pathlib, collections, unicodedata
fetch = pathlib.Path(sys.argv[1]) / "tischendorf-data/word-per-line/2.8/Unicode"
def nrm(s):
    s = unicodedata.normalize("NFD", s); return "".join(c for c in s if not unicodedata.combining(c)).lower().replace("ς", "σ")
root = lambda l: l[:4]
BK = collections.OrderedDict()
for p in sorted(fetch.glob("*.txt")):
    vs = collections.OrderedDict()
    for l in open(p, encoding="utf-8"):
        q = l.split()
        if len(q) > 7 and len(nrm(q[7])) >= 3: vs.setdefault(f"{p.stem} {q[1].split('.')[0]}", []).append(root(nrm(q[7])))
        elif len(q) > 7: vs.setdefault(f"{p.stem} {q[1].split('.')[0]}", [])
    BK[p.stem] = list(vs.items())
df = collections.Counter(l for b, vs in BK.items() for _, ls in vs for l in set(ls)); NV = sum(len(v) for v in BK.values())
content = lambda l: df[l] <= 150; idf = lambda l: math.log(NV / df[l]); GOS = ["MT", "MR", "LU", "JOH"]; L = 12
POS = {g: collections.defaultdict(list) for g in GOS}
for g in GOS:
    for i, (_, ls) in enumerate(BK[g]):
        for l in ls:
            if content(l): POS[g][l].append(i)
def best(seed, need=True):
    out = None
    for g in GOS:
        n = len(BK[g]); acc = collections.defaultdict(collections.Counter)
        for l in seed:
            for i in POS[g].get(l, ()):
                for w in range(max(0, i - L + 1), min(i, n - L) + 1): acc[w][l] += 1
        for w, c in acc.items():
            k = len(c); r = sum(c.values())
            if not need or (k >= 3 and k >= len(seed) / 2 and r >= 2 * k):
                s = sum(idf(l) * (1 + math.log(x)) for l, x in c.items())
                if out is None or s > out[0]: out = (s, g, w, k, r, dict(c))
    return out
def run(name, seeds):
    res, elig = [], 0
    for ref, ls in seeds:
        seed = sorted({l for l in ls if content(l)})
        if len(seed) < 3: continue
        elig += 1; b = best(seed)
        if b: res.append(dict(seed=ref, n=len(seed), score=round(b[0], 1), start=BK[b[1]][b[2]][0], end=BK[b[1]][min(len(BK[b[1]]) - 1, b[2] + L - 1)][0], k=b[3], said=b[4], counts=b[5]))
    res.sort(key=lambda x: -x["score"]); print(f"{name}: seeds {elig} | with an expansion {len(res)} ({100*len(res)/max(elig,1):.1f} per hundred) | score 40 or more {sum(1 for x in res if x['score']>=40)}")
    return dict(eligible=elig, n=len(res), rate=round(100 * len(res) / max(elig, 1), 1), ge40=sum(1 for x in res if x["score"] >= 40), top=res[:40])
rv = BK["RE"]; ch = lambda r: int(r.split()[1].split(":")[0]); OUT = {}
OUT["letters"] = run("Revelation 2-3, the letters", [x for x in rv if ch(x[0]) in (2, 3)])
OUT["visions"] = run("Revelation 1 and 4-22", [x for x in rv if ch(x[0]) not in (2, 3)])
for nm, seq in (("Acts 1-15", BK["AC"][:405]), ("Romans, 1 Corinthians", (BK["RO"] + BK["1CO"])[:405]), ("Hebrews, James, 1 Peter", (BK["HEB"] + BK["JAS"] + BK["1PE"])[:405]), ("1 John and the rest", (BK["1JO"] + BK["2JO"] + BK["3JO"] + BK["2PE"] + BK["JUDE"] + BK["1TI"] + BK["2TI"] + BK["TIT"])[:405])): OUT[nm] = run(nm, seq)
D = dict(rv)
def unit(a, z): refs = [r for r, _ in rv]; i, j = refs.index(f"RE {a}"), refs.index(f"RE {z}"); return [l for _, ls in rv[i:j + 1] for l in ls]
PROM = [("Ephesus: the tree of life in the paradise of God", "2:7", "2:7"), ("Smyrna: the crown of life; not hurt by the second death", "2:10", "2:11"), ("Pergamum: the hidden manna, the white stone, the new name", "2:17", "2:17"),
        ("Thyatira: authority over the nations, the morning star", "2:26", "2:28"), ("Sardis: white garments; the name confessed", "3:4", "3:5"), ("Philadelphia: a pillar in the temple; the new Jerusalem; the name", "3:12", "3:12"), ("Laodicea: to sit with me on my throne", "3:20", "3:21")]
print("\nthe seven promises, each as a seed (the best stretch whether or not it meets the rule):"); OUT["promises"] = []
for nm, a, z in PROM:
    seed = sorted({l for l in unit(a, z) if content(l)}); b = best(seed, need=False); meets = b[3] >= 3 and b[3] >= len(seed) / 2 and b[4] >= 2 * b[3]
    OUT["promises"].append(dict(name=nm, seed=f"Rev {a}–{z}", roots=len(seed), score=round(b[0], 1), start=BK[b[1]][b[2]][0], end=BK[b[1]][min(len(BK[b[1]]) - 1, b[2] + L - 1)][0], held=b[3], said=b[4], meets=meets, counts=b[5]))
    print(f"  {nm:62} → {BK[b[1]][b[2]][0]:9}–{BK[b[1]][min(len(BK[b[1]])-1,b[2]+L-1)][0].split()[1]:6} holds {b[3]}/{len(seed)}, said {b[4]:2}, score {b[0]:5.1f} {'EXPANSION' if meets else ''} {b[5]}")
print("\nthe letters' strongest, to be read:")
for x in OUT["letters"]["top"][:14]: print(f"  {x['score']:5} {x['seed']:8} → {x['start']:9}–{x['end'].split()[1]:6} {x['k']}/{x['n']} said {x['said']:2} {x['counts']}")
print("\nthe visions' strongest:")
for x in OUT["visions"]["top"][:16]: print(f"  {x['score']:5} {x['seed']:8} → {x['start']:9}–{x['end'].split()[1]:6} {x['k']}/{x['n']} said {x['said']:2} {x['counts']}")
json.dump(OUT, open(sys.argv[2], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
