#!/usr/bin/env python3
"""Held-out test of the four laws (2C; designed at 2D.6). The claim under test: each Gospel works on Revelation in its own way, so the computed features of a link
(nothing read, nothing chosen) should tell which Gospel it belongs to, on parts of Revelation the model has not seen.
Held out by region: the ten regions of Revelation, each in turn. A naive Bayes model over the link's computed features is fitted on the other nine and scores the
tenth. Baselines: always guessing the commonest Gospel; and the same procedure with the Gospel labels shuffled, 2,000 times.
   python3 heldout.py <law.json>"""
import json, sys, math, random, collections
L = json.load(open(sys.argv[1]))["links"]; G = ("Matt", "Mark", "Luke", "John")
def feats(l):
    return {"form_kept_all": l["form_kept"] == 1, "form_kept_none": l["form_kept"] == 0, "order_kept": l["order_kept"], "looser": l["span_target"] > l["span_seed"], "tighter": l["span_target"] < l["span_seed"],
            "first_seed": l["first_seed"], "first_kept": l["first_seed"] and l["first_target"], "first_added": l["first_target"] and not l["first_seed"],
            "neg_removed": l["neg_seed"] and not l["neg_target"], "neg_added": l["neg_target"] and not l["neg_seed"], "cited": l["cite_target"], "three_or_more": len(l["stems"]) >= 3}
def run(links, labels, use_region=False):
    regions = sorted({l["region"] for l in links}); correct = 0; conf = collections.Counter()
    for R in regions:
        tr = [(l, y) for l, y in zip(links, labels) if l["region"] != R]; te = [(l, y) for l, y in zip(links, labels) if l["region"] == R]
        prior = collections.Counter(y for _, y in tr); F = collections.defaultdict(lambda: collections.Counter())
        for l, y in tr:
            for k, v in feats(l).items(): F[(y, k)][bool(v)] += 1
        for l, y in te:
            best, bs = None, -1e9
            for g in G:
                if not prior[g]: continue
                s = math.log(prior[g] / len(tr))
                for k, v in feats(l).items(): s += math.log((F[(g, k)][bool(v)] + 1) / (prior[g] + 2))
                if s > bs: best, bs = g, s
            correct += best == y; conf[(y, best)] += 1
    return correct / len(links), conf
for name, sel in (("all links", lambda l: True), ("links the Septuagint cannot supply", lambda l: not l["lxx"]), ("this Gospel alone, Septuagint cannot supply", lambda l: not l["lxx"] and l["only_this_gospel"])):
    X = [l for l in L if sel(l)]; y = [l["gospel"] for l in X]; acc, conf = run(X, y); base = max(collections.Counter(y).values()) / len(y)
    random.seed(1126); sh = []
    for _ in range(2000):
        yy = y[:]; random.shuffle(yy); sh.append(run(X, yy)[0])
    p = sum(1 for a in sh if a >= acc) / len(sh)
    print(f"{name}: n={len(X)}  held-out accuracy {acc:.3f}  | commonest-Gospel baseline {base:.3f} | shuffled labels mean {sum(sh)/len(sh):.3f}, 95th pct {sorted(sh)[int(.95*len(sh))]:.3f} | p={p:.3f}")
    print("   per Gospel recall:", {g: f"{conf[(g, g)]}/{sum(conf[(g, h)] for h in G)}" for g in G})
# which features carry it: one feature at a time, chi-square-free: rate per Gospel on the non-Septuagint set
X = [l for l in L if not l["lxx"]]
print("feature rates, links the Septuagint cannot supply (%):"); print(" " * 16 + "".join(f"{g:>7}" for g in G))
for k in feats(X[0]):
    print(f"{k:16}" + "".join(f"{100*sum(1 for l in X if l['gospel']==g and feats(l)[k])/max(1,sum(1 for l in X if l['gospel']==g)):>7.0f}" for g in G))
