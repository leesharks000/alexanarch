#!/usr/bin/env python3
"""The conjunction search (the author, 17:59: "take what we learned at this locus about how expansion works and use it to find more").
What stood at Matt 22 after controls (2V.5) was a CONJUNCTION: unlike things held together in one Gospel passage, held together in one short
stretch of Revelation, and in no other seated text. This looks for that shape blind.
  A Gospel passage = 12 verses (step 3). A source stretch = 60 verses (step 15) of Revelation, of any book of the Septuagint, or of any other
  book of the New Testament outside the Gospels. Words are crude stems, made the same way in all three corpora (no lemmas: the Septuagint
  has none seated). A stem weighs log(N/df) by its verses in the New Testament; stems in more than 120 verses are dropped.
  score(passage, stretch) = sum of weights of the stems both hold.
  A WIN for a source book: its best stretch scores higher for the passage than every stretch of every other source.
   python3 conj.py <alexanarch root> <engine dir> out.json"""
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
                if re.search(r"\d+:\d+$", r) and r not in seen:
                    seen.add(r); v.append((r, [s for s in map(stem, E.norm(t).split()) if s]))
        if v: bk[p.stem] = v
    return bk
NT, LXX = load("gnt-nestle1904"), load("lxx-swete")
GOS = [b for b in NT if b in ("Matt", "Mark", "Luke", "John")]; assert len(GOS) == 4, list(NT)[:8]
df = collections.Counter(); N = 0
for b, v in NT.items():
    for r, ss in v: N += 1; df.update(set(ss))
W = {s: math.log(N / c) for s, c in df.items() if c <= 120}
gst = set()
for b in GOS:
    for r, ss in NT[b]: gst.update(s for s in ss if s in W)
IX = {s: i for i, s in enumerate(sorted(gst))}; wv = np.array([W[s] for s in sorted(gst)], dtype=np.float32)
def wins(v, size, step):
    out = []
    for i in range(0, max(1, len(v) - size + step), step):
        ch = v[i:i + size]
        if len(ch) < size // 2 and i: break
        c = collections.Counter(s for _, ss in ch for s in ss if s in IX); out.append((ch[0][0], ch[-1][0], c))
    return out
G = [(b,) + w for b in GOS for w in wins(NT[b], 12, 3)]
SRC = [("Rev",) + w for w in wins(NT["Rev"], 60, 15)]
for b, v in NT.items():
    if b not in GOS and b != "Rev": SRC += [(b,) + w for w in wins(v, 60, 15)]
for b, v in LXX.items(): SRC += [("LXX:" + b.split("-", 1)[-1],) + w for w in wins(v, 60, 15)]
def mat(ws):
    M = np.zeros((len(ws), len(IX)), dtype=np.float32)
    for i, w in enumerate(ws):
        for s in w[3]: M[i, IX[s]] = 1
    return M
GM, SM = mat(G), mat(SRC); SC = (GM * wv) @ SM.T
lab = np.array([s[0] for s in SRC]); books = sorted(set(lab)); print("passages", len(G), "stretches", len(SRC), "of Revelation", int((lab == "Rev").sum()), "of the Septuagint", int(sum(l.startswith("LXX") for l in lab)))
# wins by source book
best = {b: SC[:, lab == b].max(1) for b in books}; B = np.stack([best[b] for b in books], 1); top = B.argmax(1); srt = np.sort(B, 1); margin = srt[:, -1] - srt[:, -2]
tab = []
for j, b in enumerate(books):
    n = int((top == j).sum())
    if n: tab.append((b, int((lab == b).sum()), n, round(float(margin[top == j].mean()), 2), int(((top == j) & (margin >= 4)).sum())))
tab.sort(key=lambda x: -x[2]); print("\nsource book | stretches | passages won | mean margin | won by 4 or more")
for t in tab[:22]: print("  %-34s %4d %5d %6.2f %4d" % t)
OUT = dict(table=tab, hits=[])
def show(gi, n=14):
    j = np.where(lab == "Rev")[0]; k = j[SC[gi, j].argmax()]; o = np.where(lab != "Rev")[0]; c = o[SC[gi, o].argmax()]
    sh = sorted(set(G[gi][3]) & set(SRC[k][3]), key=lambda s: -W[s]); shc = sorted(set(G[gi][3]) & set(SRC[c][3]), key=lambda s: -W[s])
    only = [s for s in sh if s not in SRC[c][3]]
    d = dict(gospel=f"{G[gi][1]}–{G[gi][2].split()[-1]}", rev=f"{SRC[k][1]}–{SRC[k][2].split()[-1]}", score=round(float(SC[gi, k]), 1), control=f"{SRC[c][0]} {SRC[c][1]}–{SRC[c][2].split()[-1]}", control_score=round(float(SC[gi, c]), 1),
             shared=[(s, G[gi][3][s], SRC[k][3][s]) for s in sh[:n]], not_in_control=only[:n], said_again=sum(1 for s in sh if G[gi][3][s] >= 2))
    return d
rv = books.index("Rev"); order = [i for i in np.argsort(-(B[:, rv] - np.delete(B, rv, 1).max(1)))]
print("\nGospel passages by how far Revelation's best stretch stands above the best stretch of anything else (overlapping passages merged to the best):")
seen = []
for gi in order:
    b, a = G[gi][0], G[gi][1]; key = (b, int(re.search(r"(\d+):(\d+)$", a)[1]))
    if any(k == key for k in seen): continue
    seen.append(key); d = show(gi); d["margin"] = round(d["score"] - d["control_score"], 1); OUT["hits"].append(d)
    if len(seen) <= 26: print(f"\n {d['margin']:+5.1f}  {d['gospel']:22} ← {d['rev']:20} {d['score']} | best other: {d['control']} {d['control_score']} | said again {d['said_again']}\n        {' '.join(f'{s}({a},{b})' for s, a, b in d['shared'])}")
    if len(seen) >= 60: break
print("\nCalibration, the loci already read:")
for name, bk, ch, v in (("the wedding", "Matt", 22, 1), ("Luke 14", "Luke", 14, 7), ("John 4", "John", 4, 6), ("the labourers", "Matt", 20, 1), ("Matt 24:29", "Matt", 24, 27), ("Matt 27:50", "Matt", 27, 50), ("Luke 13:10", "Luke", 13, 10), ("Matt 25:31", "Matt", 25, 31)):
    c = [(abs(int(re.search(r"(\d+):(\d+)$", g[1])[2]) - v), i) for i, g in enumerate(G) if g[0] == bk and re.search(rf" {ch}:\d+$", g[1])]
    if not c: continue
    gi = min(c)[1]; d = show(gi, 9); rank = int((B[gi] > B[gi, rv]).sum()) + 1
    print(f"  {name:14} {d['gospel']:18} Rev best {d['rev']:18} {d['score']:5} rank of Revelation among {len(books)} sources: {rank} | best other {d['control']} {d['control_score']}\n        {' '.join(s for s, _, _ in d['shared'])}"); OUT.setdefault("calibration", []).append(dict(name=name, rank=rank, **d))
json.dump(OUT, open(sys.argv[3], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
