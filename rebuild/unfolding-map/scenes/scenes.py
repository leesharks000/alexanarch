#!/usr/bin/env python3
"""The shared scenes (2G.6): the station held, the Gospel varied. Five scenes all four Gospels tell. For each Gospel's telling, the wording that is that Gospel's alone
within the scene (absent from the other three tellings of it) is looked up in Revelation, two ways: exact runs of two or three words with at least two content words;
and pairs of rare stems standing together in one verse of each. Each hit is checked for the Septuagint and for the rest of the New Testament.
Pericope bounds are the usual ones, entered from memory and printed with the output so they can be corrected.
   python3 scenes.py <alexanarch root> <out.json>"""
import sys, re, json, unicodedata, pathlib, collections
C = pathlib.Path(sys.argv[1]) / "data/corpora"
SCENES = {"the Baptist's announcement": {"Matt": (3, 1, 3, 12), "Mark": (1, 2, 1, 8), "Luke": (3, 1, 3, 18), "John": (1, 19, 1, 34)},
          "the feeding": {"Matt": (14, 13, 14, 21), "Mark": (6, 30, 6, 44), "Luke": (9, 10, 9, 17), "John": (6, 1, 6, 15)},
          "the entry": {"Matt": (21, 1, 21, 11), "Mark": (11, 1, 11, 11), "Luke": (19, 28, 19, 40), "John": (12, 12, 12, 19)},
          "the cross": {"Matt": (27, 32, 27, 56), "Mark": (15, 21, 15, 41), "Luke": (23, 26, 23, 49), "John": (19, 16, 19, 37)},
          "the tomb": {"Matt": (28, 1, 28, 10), "Mark": (16, 1, 16, 8), "Luke": (24, 1, 24, 12), "John": (20, 1, 20, 18)}}
def words(s):
    s = unicodedata.normalize("NFD", s); s = "".join(c for c in s if not unicodedata.combining(c)).lower().replace("ς", "σ"); return re.findall(r"[α-ω]+", s)
def load(p): return [(l.split("\t")[0].strip(), words(l.split("\t", 1)[1]), l.split("\t", 1)[1].strip()) for l in p.read_text(encoding="utf-8", errors="ignore").splitlines() if "\t" in l]
NT = {p.stem: load(p) for p in sorted((C / "gnt-nestle1904/text").glob("*.txt"))}
freq = collections.Counter(w for b in NT.values() for _, ws, _ in b for w in ws); STOP = {w for w, _ in freq.most_common(100)}
st = lambda w: w[:5]; df = collections.Counter(s for b in NT.values() for _, ws, _ in b for s in {st(x) for x in ws if len(x) >= 4}); rare = {s for s, c in df.items() if c <= 60}
def grams(ws):
    out = set()
    for n in (2, 3):
        for i in range(len(ws) - n + 1):
            g = tuple(ws[i:i + n])
            if sum(1 for w in g if w not in STOP and len(w) >= 4) >= 2: out.add(g)
    return out
REVG = collections.defaultdict(list); REVS = []
for ref, ws, t in NT["Rev"]:
    for g in grams(ws): REVG[g].append(ref)
    REVS.append((ref, {st(x) for x in ws if len(x) >= 4} & rare))
ALLG = collections.defaultdict(set)
for b, v in NT.items():
    if b == "Rev": continue
    for ref, ws, _ in v:
        for g in grams(ws): ALLG[g].add(b)
LXG = set(); LXS = collections.defaultdict(set); i = 0
for p in (C / "lxx-swete/text").glob("*.txt"):
    for ref, ws, _ in load(p):
        if not re.search(r"\d+:\d+$", ref): continue
        LXG |= grams(ws); i += 1
        for s in {st(x) for x in ws if len(x) >= 4} & rare: LXS[s].add(i)
def lxxpair(sh):
    sets = [LXS[s] for s in sh]; return all(sets) and bool(set.intersection(*sorted(sets, key=len)))
def peri(g, b):
    c1, v1, c2, v2 = b; out = []
    for ref, ws, t in NT[g]:
        c, v = map(int, ref.split()[1].split(":"))
        if (c, v) >= (c1, v1) and (c, v) <= (c2, v2): out.append((ref, ws, t))
    return out
REG = [("1", 1, 1), ("2–3", 2, 3), ("4–5", 4, 5), ("6–7", 6, 7), ("8–11", 8, 11), ("12–14", 12, 14), ("15–16", 15, 16), ("17–18", 17, 18), ("19–20", 19, 20), ("21–22", 21, 22)]
region = lambda ref: next(n for n, a, b in REG if a <= int(ref.split()[1].split(":")[0]) <= b)
out = {"bounds": SCENES, "scenes": {}}
for scene, B in SCENES.items():
    P = {g: peri(g, b) for g, b in B.items()}; G_ = {g: set().union(*[grams(ws) for _, ws, _ in P[g]]) for g in P}; S_ = {g: set().union(*[{st(x) for x in ws if len(x) >= 4} for _, ws, _ in P[g]]) for g in P}
    out["scenes"][scene] = {}
    print("\n==", scene, {g: f"{len(P[g])} verses" for g in P})
    for g in P:
        hits = []
        for ref, ws, t in P[g]:
            for gr in grams(ws):
                if gr in REVG and not any(gr in G_[h] for h in P if h != g):
                    hits.append({"kind": "run", "gospel_ref": ref, "wording": " ".join(gr), "rev": sorted(set(REVG[gr]))[:5], "lxx": gr in LXG, "other_nt_books": sorted(ALLG[gr] - {g})})
            own = {st(x) for x in ws if len(x) >= 4} & rare; own_only = {s for s in own if not any(s in S_[h] for h in P if h != g)}
            for rref, rs in REVS:
                sh = own & rs
                if len(sh) >= 2 and (sh & own_only) and not lxxpair(sh): hits.append({"kind": "stems", "gospel_ref": ref, "wording": " ".join(sorted(sh)), "rev": [rref], "lxx": False, "other_nt_books": None})
        # keep the longest run where a 3-run contains a 2-run
        runs = [h for h in hits if h["kind"] == "run"]; keep = [h for h in runs if not any(h is not k and h["gospel_ref"] == k["gospel_ref"] and h["wording"] in k["wording"] and len(k["wording"]) > len(h["wording"]) for k in runs)]
        hits = keep + [h for h in hits if h["kind"] == "stems"]
        out["scenes"][scene][g] = hits; regs = collections.Counter(region(r) for h in hits for r in h["rev"][:1])
        print(f"  {g}: {len(hits)} hits; regions {dict(regs)}")
        for h in hits:
            flag = ("LXX " if h["lxx"] else "    ") + ("" if h["other_nt_books"] is None else ("only here+Rev" if not h["other_nt_books"] else "+" + ",".join(h["other_nt_books"][:5])))
            print(f"     {h['kind']:5} {h['gospel_ref']:11} {h['wording']:32} ↔ {', '.join(h['rev'][:4]):34} {flag}")
json.dump(out, open(sys.argv[2], "w"), ensure_ascii=False, indent=1)
