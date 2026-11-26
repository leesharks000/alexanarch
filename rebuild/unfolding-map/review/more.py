#!/usr/bin/env python3
"""Runs asked for by the two reviews of v0.6. (1) A two-verse Septuagint model. (2) The grammar frozen on the late letters, tried on the Gospels.
(3) Reuse: how often a new derivation needs a new operator, and how often it needs a member supplied from outside the seed. (4) A sample of the Mark alignment.
   python3 more.py <alexanarch root> <engine dir>"""
import sys, re, json, math, pathlib, collections, random, itertools
sys.path.insert(0, sys.argv[2]); import midrash
S = midrash.Seats(sys.argv[1]); E = pathlib.Path(sys.argv[2]); DS = json.loads((E / "derivations.json").read_text(encoding="utf-8"))["derivations"]; RUN = {r["id"]: r for r in json.loads((E / "runs.json").read_text(encoding="utf-8"))["runs"]}
COST = {r["id"]: r for r in json.load(open("cost.json"))["rows"]}; T = json.load(open("cost.json"))["tariff"]; OPB, WORD = T["operator_bits"], T["supplied_member_bits"]
LXN = [(r, midrash.norm(t)) for r, t in S._orig("lxx-swete").items()]; NL = len(LXN); lf = lambda k: math.log2(math.factorial(k)) if k > 1 else 0.0
print("(1) two verses of the Septuagint joined, against forward from Revelation (Revelation-seeded derivations)")
rows = []
for D in DS:
    if not D["seed"].startswith("gnt:Rev"): continue
    M = {m["id"]: m for m in D["members"]}; em = RUN[D["id"]]["emission"]["members"]; rx = [re.compile(M[k]["rx"]) for k in em]
    masks = collections.defaultdict(list)
    for r, t in LXN:
        b = sum(1 << i for i, x in enumerate(rx) if x.search(t))
        if b: masks[b].append(r)
    best = (0, None, None)
    for a, b in itertools.combinations_with_replacement(list(masks), 2):
        c = bin(a | b).count("1")
        if c > best[0]: best = (c, masks[a][0], masks[b][0])
    two = 2 * math.log2(NL) + OPB + lf(len(em)) + (len(em) - best[0]) * (OPB + WORD)
    rows.append({"id": D["id"], "forward": COST[D["id"]]["forward"], "lxx_one": COST[D["id"]]["lxx_to_target"], "lxx_two": round(two, 1), "members": f"{best[0]} of {len(em)}", "verses": [best[1], best[2]]})
for r in rows: print(f"  {r['id'][:34]:35}{r['forward']:>7}{r['lxx_one']:>8}{r['lxx_two']:>8}  {r['members']:>7}  {r['verses']}")
print("  SUM forward %.0f | one verse %.0f | two verses %.0f ; forward cheaper than two verses in %d of %d; two verses cheaper: %s" % (sum(r["forward"] for r in rows), sum(r["lxx_one"] for r in rows), sum(r["lxx_two"] for r in rows),
      sum(1 for r in rows if r["forward"] < r["lxx_two"]), len(rows), [r["id"] for r in rows if r["lxx_two"] <= r["forward"]]))
full = [r for r in rows if r["members"].split(" of ")[0] == r["members"].split(" of ")[1]]
print("  two Septuagint verses hold every member of the emission in:", [(r["id"], r["verses"]) for r in full])
fam = lambda D: "gospel" if D["family"].startswith(("Gospels", "Matthew", "Mark", "Luke", "John")) else ("late" if D["family"].startswith("Letters") else "other")
late_ops = {s["op"] for D in DS if fam(D) == "late" for s in D["steps"]}
gos = [D for D in DS if fam(D) == "gospel"]; ok = [D for D in gos if {s["op"] for s in D["steps"]} <= late_ops]
print("\n(2) grammar of the late letters:", sorted(late_ops)); print("  Gospel derivations statable in it: %d of %d" % (len(ok), len(gos)))
need = collections.Counter(o for D in gos for o in {s["op"] for s in D["steps"]} - late_ops); print("  the others need:", dict(need))
print("  by Gospel family:", {f: f"{sum(1 for D in ok if D['family']==f)}/{sum(1 for D in gos if D['family']==f)}" for f in sorted({D['family'] for D in gos})})
print("\n(3) reuse, in the order the derivations were written")
seen = set(); firsts = []
for i, D in enumerate(DS, 1):
    new = [s["op"] for s in D["steps"] if s["op"] not in seen]
    for o in new: seen.add(o)
    if new: firsts.append((i, D["id"], sorted(set(new))))
for f in firsts: print("  new operator at derivation", f)
sup = [COST[D["id"]]["supplied_forward"] for D in DS]; q = lambda a, b: f"{sum(1 for x in sup[a:b] if x == 0)}/{len(sup[a:b])}"
print("  derivations needing no member supplied from outside the seed: first 12:", q(0, 12), "| 13–24:", q(12, 24), "| 25–36:", q(24, 36), "| 37–48:", q(36, 48), "| all:", q(0, len(sup)))
json.dump({"two_verse": rows, "late_grammar": {"operators": sorted(late_ops), "gospel_statable": len(ok), "of": len(gos), "needs": dict(need)}, "first_use": firsts, "no_supply": sum(1 for x in sup if x == 0), "n": len(sup)}, open("more.json", "w"), ensure_ascii=False, indent=1)
