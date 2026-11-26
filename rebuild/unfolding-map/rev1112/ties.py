#!/usr/bin/env python3
"""Third pass. (a) What binds 11:1-13 to 12:1-17 across the joint: word-stems (first five letters, accents removed) in both, counted over Revelation's verses.
(b) The Septuagint window for Ezekiel 37-38 counted directly, with the seat's line for 37:5 as it stands. (c) Named lines.
   python3 ties.py <alexanarch root> <engine dir> census.json"""
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
NT, LXX = load("gnt-nestle1904"), load("lxx-swete"); rev = NT["Rev"]
def stems(t): return {w[:5] for w in t.split() if len(w) >= 5}
df = collections.Counter(s for _, t in rev for s in stems(t))
def sec(lo, hi): return [(r, t) for r, t in rev if lo <= (int(r.split()[1].split(":")[0]), int(r.split(":")[1])) <= hi]
W, J, G = sec((11, 1), (11, 13)), sec((11, 14), (11, 19)), sec((12, 1), (12, 17))
def where(S, s): return [r.split()[1] for r, t in S if s in stems(t)]
sw, sj, sg = (set().union(*(stems(t) for _, t in S)) for S in (W, J, G))
out = {}
for name, A, B, SA, SB in (("witnesses and sign", sw, sg, W, G), ("witnesses and joint", sw, sj, W, J), ("joint and sign", sj, sg, J, G)):
    sh = sorted((df[s], s) for s in A & B if df[s] <= 14); out[name] = [(s, n, where(SA, s), where(SB, s)) for n, s in sh]
    print(f"\n{name}: shared stems in at most 14 of Revelation's {len(rev)} verses: {len(sh)}")
    for n, s in sh: print(f"   {s:6} in {n:2} verses | {where(SA, s)} | {where(SB, s)}")
# null: the same count for other adjacent stretches of the same lengths
import random
def count(i):
    a = rev[i:i + 13]; b = rev[i + 19:i + 36]; A = set().union(*(stems(t) for _, t in a)); B = set().union(*(stems(t) for _, t in b)); return sum(1 for s in A & B if df[s] <= 14)
i0 = [r for r, _ in rev].index("Rev 11:1"); obs = count(i0); alln = [count(i) for i in range(0, len(rev) - 36)]
print(f"\nshared rare stems, witnesses and sign: {obs}; the same measure at every other position in Revelation (13 verses, a gap of 6, 17 verses): mean {sum(alln)/len(alln):.1f}, positions with as many: {sum(1 for x in alln if x >= obs)} of {len(alln)}")
ez = [(r, t) for b, vs in LXX.items() for r, t in vs if re.match(r"Ἰεζεκιήλ (37|38):", r)]
for lab, rx in (("spirit of life", r"πνε[υι]μα ζωησ"), ("stood on their feet", r"εστησαν επι τ\w+ ποδ\w+"), ("μνῆμα", r"\bμνημα(τι|τοσ|τα|των|σιν)?\b"), ("earthquake", r"\bσεισμοσ\b"), ("a great earthquake", r"σεισμοσ μεγασ"), ("prophesy", r"προφητευσ")):
    print("Ezek 37-38 |", lab, [r.split()[1] for r, t in ez if re.search(rx, t)])
for ref, rx in (("Δανιήλ_(Theodotionis_versio) 7:21", None), ("Δανιήλ_(translatio_Graeca) 7:25", None), ("Βασιλειῶν_Δʹ 1:10", None), ("Βασιλειῶν_Γʹ 17:1", None), ("Ἰεζεκιήλ 40:3", None)):
    for b, vs in LXX.items():
        for r, t in vs:
            if r == ref: print(ref, ":", t[:300])
json.dump(out, open("ties.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
