#!/usr/bin/env python3
"""conj.py made general (2X.2): other stretch sizes, and other targets in the Gospels' place.
   python3 conj2.py <alexanarch root> <engine dir> out2.json"""
import sys, re, json, math, pathlib, collections
import numpy as np
sys.path.insert(0, sys.argv[2]); import midrash as E
root = pathlib.Path(sys.argv[1]) / "data/corpora"
END = sorted("ουσιν ομεθα εσθαι ησαν ουσα ουσι ομεν ετε ουσ οισ αισ ασι ων ου οσ ον οι ην ησ ασ αι εσ ει εν α η ω ε ι ν σ".split(), key=len, reverse=True)
def stem(w):
    if len(w) < 4: return None
    for e in END:
        if w.endswith(e) and len(w) - len(e) >= 3: w = w[:-len(e)]; break
    return w[:5]
def load(corpus):
    bk = collections.OrderedDict()
    for p in sorted((root / corpus / "text").glob("*.txt")):
        seen = set(); v = []
        for l in p.read_text(encoding="utf-8", errors="ignore").splitlines():
            if "\t" in l:
                r, t = l.split("\t", 1); r = r.strip()
                if re.search(r"\d+:\d+$", r) and r not in seen: seen.add(r); v.append((r, [s for s in map(stem, E.norm(t).split()) if s]))
        if v: bk[p.stem] = v
    return bk
NT, LXX = load("gnt-nestle1904"), load("lxx-swete"); GOS = ["Matt", "Mark", "Luke", "John"]
df = collections.Counter(); N = 0
for b, v in NT.items():
    for r, ss in v: N += 1; df.update(set(ss))
W = {s: math.log(N / c) for s, c in df.items() if c <= 120}
def wins(v, size, step, IX):
    out = []
    for i in range(0, max(1, len(v) - size + step), step):
        ch = v[i:i + size]
        if len(ch) < size // 2 and i: break
        out.append((ch[0][0], ch[-1][0], collections.Counter(s for _, ss in ch for s in ss if s in IX)))
    return out
def run(name, targets, size, step, exclude=()):
    st = set(s for b in targets for r, ss in NT[b] for s in ss if s in W); IX = {s: i for i, s in enumerate(sorted(st))}; wv = np.array([W[s] for s in sorted(st)], dtype=np.float32)
    G = [(b,) + w for b in targets for w in wins(NT[b], 12, 3, IX)]; SRC = []
    for b, v in NT.items():
        if b not in targets and b not in exclude: SRC += [(b,) + w for w in wins(v, size, step, IX)]
    for b, v in LXX.items(): SRC += [("LXX:" + b.split("-", 1)[-1],) + w for w in wins(v, size, step, IX)]
    def mat(ws):
        M = np.zeros((len(ws), len(IX)), dtype=np.float32)
        for i, w in enumerate(ws):
            for s in w[3]: M[i, IX[s]] = 1
        return M
    SC = (mat(G) * wv) @ mat(SRC).T; lab = np.array([s[0] for s in SRC]); books = sorted(set(lab)); B = np.stack([SC[:, lab == b].max(1) for b in books], 1); top = B.argmax(1)
    tab = sorted(((b, int((lab == b).sum()), int((top == j).sum())) for j, b in enumerate(books)), key=lambda x: -x[2] / x[1]); rv = books.index("Rev"); rate = {b: round(n / k, 2) for b, k, n in tab if k >= 8}
    big = sorted(rate.items(), key=lambda x: -x[1]); pos = [b for b, _ in big].index("Rev") + 1
    print(f"\n== {name}: passages {len(G)}, stretches of {size} verses: {len(SRC)} (Revelation {int((lab=='Rev').sum())}). Revelation wins {int((top==rv).sum())}, {rate.get('Rev')} a stretch; place among the {len(big)} sources with eight or more stretches: {pos}")
    print("   highest rates:", ", ".join(f"{b.replace('LXX:','')} {r}" for b, r in big[:8]))
    mg = B[:, rv] - np.delete(B, rv, 1).max(1); seen = []; hits = []
    for gi in np.argsort(-mg):
        key = (G[gi][0], re.search(r"(\d+):", G[gi][1])[1])
        if key in seen: continue
        seen.append(key); j = np.where(lab == "Rev")[0]; k = j[SC[gi, j].argmax()]; sh = sorted(set(G[gi][3]) & set(SRC[k][3]), key=lambda s: -W[s])[:12]
        hits.append(dict(target=f"{G[gi][1]}–{G[gi][2].split()[-1]}", rev=f"{SRC[k][1]}–{SRC[k][2].split()[-1]}", margin=round(float(mg[gi]), 1), shared=sh))
        if len(seen) >= 12: break
    for h in hits: print(f"   {h['margin']:+5.1f} {h['target']:22} ← {h['rev']:20} {' '.join(h['shared'])}")
    return dict(name=name, passages=len(G), stretches=len(SRC), rev_wins=int((top == rv).sum()), rev_rate=rate.get("Rev"), place=pos, of=len(big), top_rates=big[:10], hits=hits)
LET = [b for b in NT if b not in GOS + ["Rev", "Acts"]]; OUT = []
OUT.append(run("Gospels, stretches of 30", GOS, 30, 8)); OUT.append(run("Gospels, stretches of 120", GOS, 120, 30))
OUT.append(run("Acts in the Gospels' place", ["Acts"], 60, 15, exclude=GOS)); OUT.append(run("the letters in the Gospels' place", LET, 60, 15, exclude=GOS))
json.dump(OUT, open(sys.argv[3], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
