#!/usr/bin/env python3
"""Where the naming of 2I.2 came from. The assigned operators are split into those that state wording (PARTITION, REORDER, ADD: which members are kept, in
what order, what is added; the engine checks these against the seat) and those that state a relation (the rest: assigned by reading). Each part names the Gospel alone.
   python3 split.py relations.json"""
import sys, json, random, collections
sys.argv = [sys.argv[0], "", "../engine", sys.argv[1]] if len(sys.argv) == 2 else sys.argv
from relations import nb
R = json.load(open(sys.argv[3], encoding="utf-8"))["rows"]; y = [r["gospel"] for r in R]; G = ["Matt", "Mark", "Luke", "John"]; W = {"PARTITION", "REORDER", "ADD"}
out = {}
for name, X in (("assigned, wording operators only", [set(r["hand"]) & W for r in R]), ("assigned, relation operators only", [set(r["hand"]) - W for r in R]),
                ("computed relation operators with the wording operators", [set(r["derived"]) | (set(r["hand"]) & W) for r in R]),
                ("slot differences with the wording operators", [set(r["features"]) | (set(r["hand"]) & W) for r in R])):
    acc, conf = nb(X, y, G); random.seed(1126); sh = []
    for _ in range(5000):
        yy = y[:]; random.shuffle(yy); sh.append(nb(X, yy, G)[0])
    p = sum(1 for a in sh if a >= acc) / len(sh); out[name] = (round(acc, 3), p)
    print(f"{name}: {acc:.3f} | shuffled {sum(sh)/len(sh):.3f} (95th {sorted(sh)[int(.95*len(sh))]:.3f}) | p={p:.4f} | recall", {g: f"{conf[(g,g)]}/{y.count(g)}" for g in G})
for o in sorted(W): print(o, {g: f"{sum(1 for r in R if r['gospel']==g and o in r['hand'])}/{y.count(g)}" for g in G})
json.dump(out, open("split.json", "w"), indent=1)
