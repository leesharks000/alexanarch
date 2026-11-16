import json, glob, collections, os
D = os.path.dirname(os.path.abspath(__file__)); AP = os.path.join(D, "..")
inp = {}
for f in glob.glob(f"{D}/in-*.jsonl"):
    for l in open(f):
        r = json.loads(l); inp[r["id"]] = r
out = {}; bad = []
for f in glob.glob(f"{D}/out-*.jsonl"):
    for l in open(f):
        l = l.strip()
        if not l: continue
        r = json.loads(l)
        if r["id"] not in inp or r["quote"] not in inp[r["id"]]["abstract"]: bad.append(r["id"]); continue
        out[r["id"]] = r
print("rows", len(out), "of", len(inp), "invalid", len(bad), bad[:10])
# groups from census codes
grp = {}
for n in ["phronesis", "apeiron", "elenchos", "rhizomata", "agph"]:
    for c in json.load(open(f"{AP}/codes-{n}.json")): grp[f"{n}-{c['n']}"] = c["group"]
# agreement on AP blind set
ap = json.load(open(f"{AP}/abstract-reach.json"))
pairs = [(ap[int(k[3:])]["reach"], v["code"]) for k, v in out.items() if k.startswith("ap-")]
if pairs:
    agree = sum(a == b for a, b in pairs); print(f"AP blind agreement {agree}/{len(pairs)} = {100*agree/len(pairs):.0f}%")
    print(" confusion (lead->reader):", collections.Counter(f"{a}>{b}" for a, b in pairs if a != b).most_common(8))
P = lambda y: "2010–15" if y <= 2015 else ("2016–20" if y <= 2020 else "2021–26")
def table(sel, label):
    print(f"\n== {label}")
    print(f"{'journal':10} {'period':8} {'n':>4} " + " ".join(f"{k:>4}" for k in "ABCDEF") + "   D-open")
    tot = collections.defaultdict(collections.Counter)
    for j in ["phronesis", "apeiron", "elenchos", "rhizomata", "agph", "ALL"]:
        cs = collections.defaultdict(collections.Counter)
        for k, v in out.items():
            if k.startswith("ap-") or v["code"] in ("X", "N"): continue
            jj = k.rsplit("-", 1)[0]
            if j != "ALL" and jj != j: continue
            if not sel(k): continue
            y = inp[k]["year"]
            if y < 2010: continue
            cs[P(y)][v["code"]] += 1
            if v["code"] == "D" and v.get("dir") == "open": cs[P(y)]["Dopen"] += 1
        for p in sorted(cs):
            c = cs[p]; n = sum(c[k] for k in "ABCDEF")
            if n: print(f"{j:10} {p:8} {n:4} " + " ".join(f"{100*c[k]/n:4.0f}" for k in "ABCDEF") + f"   {c['Dopen']}")
table(lambda k: True, "all coded works with abstracts (excl. X/N), %")
table(lambda k: grp.get(k) in ("Plato", "Aristotle"), "Plato/Aristotle works only (comparable to AP 2022–26), %")
print("\nD rows:")
for k, v in sorted(out.items()):
    if v["code"] == "D" and not k.startswith("ap-"): print(f" {inp[k]['year']} [{v.get('dir')}] {inp[k]['title'][:80]}")
json.dump(out, open(f"{D}/reach5-coded-tally.json", "w"), ensure_ascii=False)
