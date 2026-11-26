#!/usr/bin/env python3
"""Two controls asked for by the review of v0.3.
(1) THE DELTA CENSUS. Align each verse of Mark to its best verse in Matthew and in Luke (four or more shared stems, the best match, one to one). For each aligned pair
    the delta is the borrower's stems that the Mark verse does not have. Where does the delta's vocabulary stand: in Revelation, in a comparison book, in the Septuagint?
(2) THE NULL PAIRS. The link instrument of law.py run with other books in Revelation's place as the seed, to see what it finds where no one proposes a relation.
   python3 delta.py <alexanarch root>"""
import sys, re, math, json, unicodedata, pathlib, collections
C = pathlib.Path(sys.argv[1]) / "data/corpora"
def words(s):
    s = unicodedata.normalize("NFD", s); s = "".join(c for c in s if not unicodedata.combining(c)).lower().replace("ς", "σ"); return re.findall(r"[α-ω]+", s)
st = lambda ws: {w[:5] for w in ws if len(w) >= 4}
NT = {p.stem: [(l.split("\t")[0], st(words(l.split("\t", 1)[1]))) for l in p.read_text(encoding="utf-8").splitlines() if "\t" in l] for p in sorted((C / "gnt-nestle1904/text").glob("*.txt"))}
N = sum(len(v) for v in NT.values()); df = collections.Counter(s for b in NT.values() for _, ss in b for s in ss)
VOC = {b: set().union(*[ss for _, ss in v]) for b, v in NT.items()}
LXXV = set(); LXv = collections.defaultdict(set); i = 0
for p in (C / "lxx-swete/text").glob("*.txt"):
    for l in p.read_text(encoding="utf-8", errors="ignore").splitlines():
        if "\t" in l and re.search(r"\d+:\d+$", l.split("\t")[0].strip()):
            ss = st(words(l.split("\t", 1)[1])); LXXV |= ss; i += 1
            for s in ss:
                if df.get(s, 99) <= 60: LXv[s].add(i)
def align(a, b):
    pairs = []
    for ra, sa in NT[a]:
        best = max(((len(sa & sb), rb, sb) for rb, sb in NT[b]), key=lambda x: x[0])
        if best[0] >= 4: pairs.append((best[0], ra, best[1], sa, best[2]))
    used, out = set(), []
    for n, ra, rb, sa, sb in sorted(pairs, reverse=True):
        if rb not in used: used.add(rb); out.append((ra, rb, sa, sb))
    return out
comp = ["Rev", "Acts", "Rom", "1Cor", "Heb"]; res = {}
print("(1) delta census: the borrower's stems that the aligned Mark verse lacks")
print(f"{'borrower':9}{'pairs':>6}{'delta stems':>12}{'distinct':>9}" + "".join(f"{c:>8}" for c in comp) + f"{'LXX':>8}   share of distinct delta stems found in the book, %")
for b in ("Matt", "Luke"):
    P = align("Mark", b); delta = collections.Counter()
    for ra, rb, sa, sb in P: delta.update(sb - sa)
    D = set(delta) - VOC["Mark"]      # words Mark never uses at all: the borrower's own additions to Mark's story
    row = [100 * len(D & VOC[c]) / len(D) for c in comp]; res[b] = {"pairs": len(P), "delta_tokens": sum(delta.values()), "distinct_not_in_mark": len(D), **dict(zip(comp, row)), "LXX": 100 * len(D & LXXV) / len(D),
                                                                     "in_rev_not_in_lxx": sorted(D & VOC["Rev"] - LXXV), "in_rev": len(D & VOC["Rev"])}
    print(f"{b:9}{len(P):>6}{sum(delta.values()):>12}{len(D):>9}" + "".join(f"{x:>8.1f}" for x in row) + f"{res[b]['LXX']:>8.1f}")
    print("   in Revelation and not in the Septuagint:", res[b]["in_rev_not_in_lxx"][:40])
# the same with rarity: delta stems that are rare (<=60 verses), found in Rev
for b in ("Matt", "Luke"):
    P = align("Mark", b); hits = collections.Counter()
    for ra, rb, sa, sb in P:
        for s in (sb - sa) - VOC["Mark"]:
            if df[s] <= 60 and s in VOC["Rev"]: hits[(s, rb)] += 1
    by = collections.defaultdict(list)
    for (s, rb), _ in hits.items(): by[s].append(rb)
    print(f"   {b}: rare delta stems in Revelation: {len(by)}:", {s: v[:3] for s, v in sorted(by.items(), key=lambda kv: df[kv[0]])[:30]})
print("\n(2) null pairs: links the Septuagint cannot supply (two or more rare stems in one verse of each), per 100 verses of the seed book")
G = ("Matt", "Mark", "Luke", "John"); rare = {s for s, c in df.items() if c <= 60}
inv = collections.defaultdict(list)
for g in G:
    for r, ss in NT[g]:
        for s in ss & rare: inv[s].append((g, r))
def lxxav(sh):
    sets = [LXv[s] for s in sh]; return all(sets) and bool(set.intersection(*sorted(sets, key=len)))
print(f"{'seed':8}{'verses':>7}" + "".join(f"{g:>7}" for g in G) + f"{'all four':>10}")
null = {}
for seed in ["Rev", "Heb", "Rom", "1Cor", "2Cor", "Acts", "Jas", "1Pet", "Eph"]:
    cnt = collections.Counter()
    for r, ss in NT[seed]:
        cand = collections.defaultdict(set)
        for s in ss & rare:
            for g, r2 in inv[s]: cand[(g, r2)].add(s)
        for (g, r2), sh in cand.items():
            if len(sh) >= 2 and not lxxav(sh): cnt[g] += 1
    n = len(NT[seed]); null[seed] = {g: round(100 * cnt[g] / n, 1) for g in G}; null[seed]["all"] = round(100 * sum(cnt.values()) / n, 1)
    print(f"{seed:8}{n:>7}" + "".join(f"{null[seed][g]:>7}" for g in G) + f"{null[seed]['all']:>10}")
json.dump({"delta": res, "null_pairs": null}, open("delta.json", "w"), ensure_ascii=False, indent=1)
