#!/usr/bin/env python3
"""Generative cost: how much has to be supplied to get the later wording from each proposed source, in bits. Asked for by the review of v0.3 (its §6, §7).
Three genealogies are priced with one tariff, for every derivation of the engine:
  FORWARD   the seed as declared -> the target, by the declared operators
  REVERSE   the target -> the seed, by the same operators inverted; for a seed with two targets, both targets -> the seed by MERGE
  SEPTUAGINT the best single verse of the seated Septuagint -> the target's emission, and -> the seed's members
Tariff: choosing a verse costs log2 of the number of verses it is chosen from; naming an operator costs log2(14) (the thirteen and MERGE); PARTITION costs one bit a
member; REORDER costs log2(k!); every member that the source does not contain and has to be supplied costs log2 of the New Testament's stem vocabulary.
The tariff is crude and is stated so that it can be changed. One bias is built into any such measure and is not a finding: dropping is cheap and supplying is dear,
so the fuller text is always the cheaper source of the shorter. The informative comparisons are the seeds with two targets, and the Septuagint column.
   python3 cost.py <alexanarch root> <engine dir>"""
import sys, re, json, math, pathlib, collections, unicodedata
sys.path.insert(0, sys.argv[2]); import midrash
S = midrash.Seats(sys.argv[1]); E = pathlib.Path(sys.argv[2]); DS = json.loads((E / "derivations.json").read_text(encoding="utf-8"))["derivations"]
NTv = S._orig("gnt-nestle1904"); LXv = S._orig("lxx-swete")
book_n = collections.Counter(r.split()[0] for r in NTv); V = len({w[:5] for t in NTv.values() for w in midrash.norm(t).split() if len(w) >= 4})
OPB, WORD = math.log2(14), math.log2(V); lf = lambda k: math.log2(math.factorial(k)) if k > 1 else 0.0
PHILO_N = sum(1 for k in S._lines("philo") if "#" not in k)
def sel(loc):
    corpus, ref = loc.split(":", 1); n = len(re.findall(r" \+ ", ref)) + 1
    if corpus == "philo": return n * math.log2(PHILO_N)
    if corpus == "lxx": return n * math.log2(len(LXv))
    return sum(math.log2(book_n[p.split()[0]]) for p in ref.split(" + "))
LXN = [(r, midrash.norm(t)) for r, t in LXv.items()]
def best_lxx(rxs):
    best = (0, None)
    for r, t in LXN:
        c = sum(1 for x in rxs if re.search(x, t))
        if c > best[0]: best = (c, r)
    return best
rows = []
for D in DS:
    M = {m["id"]: m for m in D["members"]}; seedm = [k for k, m in M.items() if m.get("in_seed", True)]; state = list(seedm); fwd = sel(D["seed"]); rev = sel(D["target"]); supplied_f = supplied_r = 0
    for st in D["steps"]:
        op = st["op"]; fwd += OPB; rev += OPB
        if op == "PARTITION": d = [k for k in state if k not in st["keep"]]; fwd += len(state); rev += len(d) * WORD; supplied_r += len(d); state = [k for k in state if k in st["keep"]]
        elif op == "REORDER": fwd += lf(len(state)); rev += lf(len(state))
        elif op == "ADD": fwd += WORD; supplied_f += 1; rev += len(state) + 1; state.append(st["new"])
        elif "old" in st: fwd += WORD + math.log2(max(len(state), 1)); rev += WORD + math.log2(max(len(state), 1)); supplied_f += 1; supplied_r += 1; state[state.index(st["old"])] = st["new"]
    ct, rt = best_lxx([M[k]["rx"] for k in state]); cs, rs = best_lxx([M[k]["rx"] for k in seedm])
    lx_t = math.log2(len(LXv)) + OPB + lf(len(state)) + (len(state) - ct) * (OPB + WORD); lx_s = math.log2(len(LXv)) + OPB + lf(len(seedm)) + (len(seedm) - cs) * (OPB + WORD)
    rows.append({"id": D["id"], "family": D["family"], "seed": D["seed"], "forward": round(fwd, 1), "reverse": round(rev, 1), "supplied_forward": supplied_f, "supplied_reverse": supplied_r,
                 "lxx_to_target": round(lx_t, 1), "lxx_best_for_target": rt, "lxx_members_of_emission": f"{ct} of {len(state)}", "lxx_to_seed": round(lx_s, 1), "lxx_best_for_seed": rs, "lxx_members_of_seed": f"{cs} of {len(seedm)}",
                 "emitted": state, "seed_members": seedm})
# seeds with two targets: forward jointly, against MERGE of the two targets into the seed
groups = collections.defaultdict(list)
for D, r in zip(DS, rows):
    if D["seed"].startswith("gnt:Rev") and " + " not in D["seed"]: groups[D["seed"]].append((D, r))
joint = []
for seed, L in groups.items():
    if len(L) < 2: continue
    M = {m["id"]: m for m in L[0][0]["members"]}; seedm = L[0][1]["seed_members"]; texts = [midrash.norm(S.get(D["target"])) for D, _ in L]
    f = sel(seed) + sum(r["forward"] - sel(seed) for _, r in L)
    missing = [k for k in seedm if not any(re.search(M[k]["rx"], t) for t in texts)]
    m = sum(sel(D["target"]) for D, _ in L) + OPB + lf(len(seedm)) + len(missing) * (OPB + WORD)
    lx = sum(r["lxx_to_target"] for _, r in L)
    joint.append({"seed": seed, "targets": [D["target"] for D, _ in L], "forward_joint": round(f, 1), "merge_into_seed": round(m, 1), "seed_members_in_neither_target": missing, "septuagint_to_each_target": round(lx, 1)})
json.dump({"tariff": {"operator_bits": round(OPB, 2), "supplied_member_bits": round(WORD, 2), "stem_vocabulary": V, "verses": {"Rev": book_n["Rev"], "LXX": len(LXv), "Philo sections": PHILO_N}}, "rows": rows, "joint": joint}, open("cost.json", "w"), ensure_ascii=False, indent=1)
print(f"tariff: operator {OPB:.2f} bits; a supplied member {WORD:.2f} bits (vocabulary {V})")
print(f"{'derivation':36}{'fwd':>7}{'rev':>7}{'LXX→tgt':>9}{'  LXX has':>10}  best Septuagint verse for the emission")
for r in rows: print(f"{r['id'][:35]:36}{r['forward']:>7}{r['reverse']:>7}{r['lxx_to_target']:>9}{r['lxx_members_of_emission']:>10}  {r['lxx_best_for_target']}")
T = lambda k, f=lambda r: True: round(sum(r[k] for r in rows if f(r)), 1)
nt = lambda r: not r["seed"].startswith("philo")
print("\nSUM, Revelation-seeded derivations (%d): forward %s | reverse %s | Septuagint→target %s" % (sum(1 for r in rows if nt(r)), T("forward", nt), T("reverse", nt), T("lxx_to_target", nt)))
print("cheaper by forward than by the Septuagint:", sum(1 for r in rows if nt(r) and r["forward"] < r["lxx_to_target"]), "of", sum(1 for r in rows if nt(r)), "| Septuagint cheaper:", [r["id"] for r in rows if nt(r) and r["lxx_to_target"] <= r["forward"]])
print("\nseeds with two targets:")
for j in joint: print(f"  {j['seed'][4:]:10} → {[t[4:] for t in j['targets']]}: forward {j['forward_joint']} | merge of the two into the seed {j['merge_into_seed']} (seed members in neither: {j['seed_members_in_neither_target']}) | Septuagint to each {j['septuagint_to_each_target']}")
print("  sums:", round(sum(j["forward_joint"] for j in joint), 1), round(sum(j["merge_into_seed"] for j in joint), 1), round(sum(j["septuagint_to_each_target"] for j in joint), 1))
