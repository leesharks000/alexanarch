#!/usr/bin/env python3
"""The Gospel named from the transform alone, on read loci (2G.6; the fair form of 2F.1). Each Gospel-targeted derivation of the engine is described only by which
operators it uses and by the region of Revelation its seed lies in. Leave one derivation out, fit a naive Bayes model on the rest, name the Gospel of the one left
out. Baselines: the commonest Gospel; labels shuffled 5,000 times. Stated limit: the operators were assigned by the same reader who knew each target's Gospel.
   python3 named.py <engine dir>"""
import json, sys, math, random, collections, pathlib, re
DS = json.loads((pathlib.Path(sys.argv[1]) / "derivations.json").read_text(encoding="utf-8"))["derivations"]
BOOK = {"Matt": "Matthew", "Mark": "Mark", "Luke": "Luke", "John": "John"}
X = []
for D in DS:
    if not D["seed"].startswith("gnt:Rev"): continue
    b = D["target"].split(":", 1)[1].split()[0]
    if b not in BOOK: continue
    ch = int(re.search(r"Rev (\d+)", D["seed"]).group(1)); reg = "1-3" if ch <= 3 else "4-11" if ch <= 11 else "12-16" if ch <= 16 else "17-22"
    X.append((D["id"], b, {s["op"] for s in D["steps"]}, reg, " + " in D["seed"]))
OPS = sorted({o for _, _, ops, _, _ in X for o in ops})
def run(labels, use_region):
    ok = 0; conf = collections.Counter()
    for i, (_, _, ops, reg, multi) in enumerate(X):
        tr = [(X[j], labels[j]) for j in range(len(X)) if j != i]; prior = collections.Counter(y for _, y in tr); best, bs = None, -1e9
        for g in BOOK:
            if not prior[g]: continue
            s = math.log(prior[g] / len(tr))
            for o in OPS:
                c = sum(1 for (x, y) in tr if y == g and (o in x[2])); p = (c + 1) / (prior[g] + 2); s += math.log(p if o in ops else 1 - p)
            if use_region:
                c = sum(1 for (x, y) in tr if y == g and x[3] == reg); s += math.log((c + 1) / (prior[g] + 4))
            if s > bs: best, bs = g, s
        ok += best == labels[i]; conf[(labels[i], best)] += 1
    return ok / len(X), conf
y = [b for _, b, _, _, _ in X]; print("derivations with a Gospel target:", len(X), dict(collections.Counter(y)))
for name, ur in (("operators only", False), ("operators and seed region", True)):
    acc, conf = run(y, ur); random.seed(1126); sh = []
    for _ in range(5000):
        yy = y[:]; random.shuffle(yy); sh.append(run(yy, ur)[0])
    print(f"{name}: leave-one-out accuracy {acc:.3f} | commonest Gospel {max(collections.Counter(y).values())/len(y):.3f} | shuffled mean {sum(sh)/len(sh):.3f}, 95th {sorted(sh)[int(.95*len(sh))]:.3f} | p={sum(1 for a in sh if a>=acc)/len(sh):.4f}")
    print("   recall:", {g: f"{conf[(g,g)]}/{sum(conf[(g,h)] for h in BOOK)}" for g in BOOK})
print("operator use by Gospel (derivations using it / derivations):")
for o in OPS: print(f"  {o:20}" + "".join(f"{g}: {sum(1 for x in X if x[1]==g and o in x[2])}/{sum(1 for x in X if x[1]==g)}   " for g in BOOK))
