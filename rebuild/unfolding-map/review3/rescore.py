#!/usr/bin/env python3
"""The engine's score taken apart (a reviewer, on v0.17, section 9). For every derivation: RETAINED, the share of the kept members a text holds, and EXCLUDED,
the share of the dropped members it lacks, reported apart; the excluded share weighted by how surprising each absence is (minus log2 of the member's rate of
absence in windows of the target's length across the New Testament). And uniqueness asked with equal windows: how many stretches of the target's own length,
in the New Testament outside Revelation and in the Septuagint, hold every kept member.
   python3 rescore.py <alexanarch root> <engine dir> out.json"""
import sys, re, json, math, pathlib, collections
sys.path.insert(0, sys.argv[2]); import midrash as E
S = E.Seats(sys.argv[1]); eng = pathlib.Path(sys.argv[2])
DS = {d["id"]: d for d in json.load(open(eng / "derivations.json", encoding="utf-8"))["derivations"]}; RUNS = json.load(open(eng / "runs.json", encoding="utf-8"))["runs"]
NT = [(r, E.norm(t)) for r, t in S._orig("gnt-nestle1904").items()]; LX = [(r, E.norm(t)) for r, t in S._orig("lxx-swete").items()]
def refs_of(loc):
    out = []
    for part in loc.split(":", 1)[1].split(" + "):
        m = re.match(r"(.+ \d+:)(\d+)-(\d+)$", part) or re.match(r"(.+ )(\d+)-(\d+)$", part); out += [f"{m.group(1)}{i}" for i in range(int(m.group(2)), int(m.group(3)) + 1)] if m else [part]
    return out
def cum(corpus, rx):
    c = re.compile(rx); a = [0]
    for _, t in corpus: a.append(a[-1] + (1 if c.search(t) else 0))
    return a
rows = []
for r in RUNS:
    D = DS[r["id"]]; M = {m["id"]: m["rx"] for m in D["members"]}; K, Dr = r["emission"]["members"], r["emission"]["dropped"]
    if not K: continue
    n = len(refs_of(D["target"])); tr = set(refs_of(D["target"])); sr = set(refs_of(D["seed"])) if D["seed"].startswith("gnt:") else set()
    def fit(loc): t = E.norm(S.get(loc)); return sum(1 for k in K if re.search(M[k], t)), sum(1 for k in Dr if not re.search(M[k], t))
    row = dict(id=r["id"], kept=len(K), dropped=len(Dr), verses=n, target=fit(D["target"]), controls=[(c["label"], *fit(c["loc"])) for c in D.get("controls", [])])
    for name, corpus in (("nt", NT), ("lxx", LX)):
        cs = {k: cum(corpus, M[k]) for k in K + Dr}; W = len(corpus) - n + 1; allk = 0; refs = []; absent = collections.Counter()
        for i in range(W):
            if name == "nt" and (corpus[i][0].startswith("Rev ") or any(corpus[j][0] in tr | sr for j in range(i, i + n))): continue
            if all(cs[k][i + n] - cs[k][i] > 0 for k in K): allk += 1; refs.append(corpus[i][0])
            for k in Dr:
                if cs[k][i + n] - cs[k][i] == 0: absent[k] += 1
        row[name + "_windows_holding_all_kept"] = allk; row[name + "_refs"] = refs[:6]
        if name == "nt": row["surprise"] = {k: round(-math.log2(max(absent[k], 1) / W), 4) for k in Dr}
    w = row["surprise"]; tot = sum(w.values())
    def wex(loc): t = E.norm(S.get(loc)); return round(sum(w[k] for k in Dr if not re.search(M[k], t)) / tot, 3) if tot > 0 else None
    row["excluded_weight_total_bits"] = round(tot, 3); rows.append(row)
print("derivations scored:", len(rows))
best = [max((c[1] / r["kept"] for c in r["controls"]), default=None) for r in rows]; bb = [b for b in best if b is not None]
print(f"RETAINED alone: every target holds all its kept members: {all(r['target'][0] == r['kept'] for r in rows)} | best control's retained share: mean {sum(bb)/len(bb):.2f}; controls retaining all: {sum(1 for b in bb if b == 1)}; retaining half or more: {sum(1 for b in bb if b >= .5)} of {len(bb)}")
print(f"what the dropped members were worth: total surprise per derivation, bits: median {sorted(r['excluded_weight_total_bits'] for r in rows)[len(rows)//2]}, max {max(r['excluded_weight_total_bits'] for r in rows)}; derivations where it is under 0.1 bit: {sum(1 for r in rows if r['excluded_weight_total_bits'] < 0.1 and r['dropped'])} of {sum(1 for r in rows if r['dropped'])}")
u0 = [r for r in rows if r["nt_windows_holding_all_kept"] == 0]; l0 = [r for r in rows if r["lxx_windows_holding_all_kept"] == 0]
print(f"equal windows, kept members only: no other New Testament stretch of the target's length holds them all: {len(u0)} of {len(rows)} | no Septuagint stretch: {len(l0)} of {len(rows)} | neither: {sum(1 for r in rows if r['nt_windows_holding_all_kept']==0 and r['lxx_windows_holding_all_kept']==0)}")
for r in rows:
    if r["nt_windows_holding_all_kept"] or r["lxx_windows_holding_all_kept"]: print(f"   {r['id']:34} kept {r['kept']} over {r['verses']}v | NT {r['nt_windows_holding_all_kept']} {r['nt_refs'][:3]} | LXX {r['lxx_windows_holding_all_kept']} {r['lxx_refs'][:2]}")
print("\ncontrols by retained share (the old score beside it):")
for r in rows[-8:]: print(f"   {r['id']:34}", [(c[0][:26], f"{c[1]}/{r['kept']}") for c in r["controls"]])
json.dump(rows, open(sys.argv[3], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
