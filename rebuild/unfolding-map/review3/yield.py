#!/usr/bin/env python3
"""Discovery yield of the pair instrument, by a rule frozen here and applied alike to every seed book. A CANDIDATE: three consecutive verses of the seed and
three consecutive verses of a Gospel sharing three or more rare pairs that the Septuagint lacks. Overlapping hits are merged. Counted for Revelation and for
three other books in its place; Revelation's are listed to be read.
   python3 yield.py <alexanarch root> <engine dir> out.json"""
import sys, re, json, pathlib, collections
sys.path.insert(0, sys.argv[2]); import midrash as E
root = pathlib.Path(sys.argv[1]) / "data/corpora"
def sq(s): return re.sub(r"\s+", " ", E.norm(s)).strip()
def load(corpus):
    out = collections.OrderedDict()
    for p in sorted((root / corpus / "text").glob("*.txt")):
        seen = set()
        for l in p.read_text(encoding="utf-8", errors="ignore").splitlines():
            if "\t" in l:
                r, t = l.split("\t", 1); r = r.strip()
                if re.search(r"\d+:\d+$", r) and r not in seen: seen.add(r); out.setdefault(p.stem, []).append((r, sq(t)))
    return out
NT, LXX = load("gnt-nestle1904"), load("lxx-swete")
wc = collections.Counter(w[:5] for b, vs in NT.items() for _, t in vs for w in t.split()); STOP = {w for w, _ in wc.most_common(150)}
def pairs(t):
    ws = [w[:5] for w in t.split() if len(w) >= 3]; ws = [w for w in ws if w not in STOP]; out = set()
    for i, a in enumerate(ws):
        for b in ws[i + 1:i + 5]:
            if a != b: out.add((a, b) if a < b else (b, a))
    return out
VP = {b: [(r, pairs(t)) for r, t in vs] for b, vs in NT.items()}; df = collections.Counter(p for b, vs in VP.items() for _, ps in vs for p in ps)
lxxp = set()
for b, vs in LXX.items():
    for _, t in vs: lxxp |= pairs(t)
def keep(ps): return {p for p in ps if df[p] <= 6 and p not in lxxp}
GOS = ["Matt", "Mark", "Luke", "John"]; G3 = []
for g in GOS:
    v = [(r, keep(ps)) for r, ps in VP[g]]
    for i in range(len(v) - 2): G3.append((g, i, v[i][0], v[i][1] | v[i + 1][1] | v[i + 2][1]))
inv = collections.defaultdict(list)
for k, (g, i, r, ps) in enumerate(G3):
    for p in ps: inv[p].append(k)
def run(seed, label):
    v = [(r, keep(ps)) for r, ps in seed]; hits = []
    for i in range(len(v) - 2):
        ps = v[i][1] | v[i + 1][1] | v[i + 2][1]; cnt = collections.Counter(k for p in ps for k in inv.get(p, ()))
        for k, n in cnt.items():
            if n >= 3: hits.append((n, i, k))
    hits.sort(reverse=True); cl = []
    for n, i, k in hits:
        g, gi = G3[k][0], G3[k][1]
        if all(not (g == c["g"] and abs(gi - c["gi"]) < 6 and abs(i - c["i"]) < 6) for c in cl): cl.append(dict(n=n, i=i, g=g, gi=gi, seed=v[i][0], gospel=G3[k][2], pairs=sorted("+".join(p) for p in (v[i][1] | v[i + 1][1] | v[i + 2][1]) & G3[k][3])))
    print(f"{label}: candidates {len(cl)}"); return cl
OUT = {}
OUT["Revelation"] = run(VP["Rev"], "Revelation (405 verses)")
OUT["Acts"] = run(VP["Acts"][:405], "Acts, first 405"); OUT["Acts 16-28"] = run(VP["Acts"][-405:], "Acts, last 405")
OUT["Rom+1Cor"] = run((VP["Rom"] + VP["1Cor"])[:405], "Romans and 1 Corinthians, first 405"); OUT["Heb+Jas+1Pet"] = run((VP["Heb"] + VP["Jas"] + VP["1Pet"])[:405], "Hebrews, James, 1 Peter, first 405")
OUT["2Cor..Phlm"] = run((VP["2Cor"] + VP["Gal"] + VP["Eph"] + VP["Phil"] + VP["Col"] + VP["1Thess"])[:405], "2 Corinthians to 1 Thessalonians, first 405")
for k in OUT:
    print(f"\n== {k}")
    for c in OUT[k][: 40 if k == "Revelation" else 8]: print(f"   {c['n']}  {c['seed']:11} ~ {c['gospel']:11} {c['pairs'][:7]}")
json.dump(OUT, open(sys.argv[3], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
