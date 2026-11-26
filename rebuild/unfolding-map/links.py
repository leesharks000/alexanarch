#!/usr/bin/env python3
"""Verse-to-verse links between the Apocalypse and every other New Testament book, at stem level, so that inflected parallels are visible.
A stem is the first five letters of a word with accents and case removed (words under four letters dropped). A stem is rare if it occurs in at most 40 of the
7,900-odd verses of the seated New Testament. A link is a verse of Revelation and a verse of another book sharing two or more rare stems; its weight is the
sum of log(N/df) over the shared stems. Control: a link is 'LXX-available' if some single verse of the seated Septuagint holds the same shared stems.
   python3 links.py <alexanarch root> <out.json>"""
import sys, re, json, math, unicodedata, pathlib, collections, itertools
ROOT = pathlib.Path(sys.argv[1]); C = ROOT / "data/corpora"
def toks(s):
    s = unicodedata.normalize("NFD", s); s = "".join(c for c in s if not unicodedata.combining(c)).lower().replace("ς", "σ")
    return [w[:5] for w in re.findall(r"[α-ω]+", s) if len(w) >= 4]
def verses(p):
    for l in p.read_text(encoding="utf-8", errors="ignore").splitlines():
        if "\t" in l:
            ref, t = l.split("\t", 1); yield ref, set(toks(t))
NT = {p.stem: list(verses(p)) for p in sorted((C / "gnt-nestle1904/text").glob("*.txt"))}
N = sum(len(v) for v in NT.values()); df = collections.Counter(s for b in NT.values() for _, ss in b for s in ss)
rare = {s for s, c in df.items() if c <= 40}; w = lambda s: math.log(N / df[s])
LX = collections.defaultdict(set)   # stem -> set of LXX verse ids
i = 0
for p in (C / "lxx-swete/text").glob("*.txt"):
    for ref, ss in verses(p):
        i += 1
        for s in ss & rare: LX[s].add(i)
def lxx(shared):
    sets = sorted((LX[s] for s in shared), key=len)
    return bool(sets) and bool(set.intersection(*sets)) if all(sets) else False
inv = collections.defaultdict(list)
for b, vs in NT.items():
    if b == "Rev": continue
    for ref, ss in vs:
        for s in ss & rare: inv[s].append((b, ref))
links = []
for ref, ss in NT["Rev"]:
    cand = collections.defaultdict(set)
    for s in ss & rare:
        for b, r2 in inv[s]: cand[(b, r2)].add(s)
    for (b, r2), sh in cand.items():
        if len(sh) >= 2: links.append({"rev": ref, "book": b, "ref": r2, "stems": sorted(sh), "weight": round(sum(w(s) for s in sh), 2), "lxx": lxx(sh)})
links.sort(key=lambda l: -l["weight"])
json.dump({"instrument": __doc__, "verses": {b: len(v) for b, v in NT.items()}, "links": links}, open(sys.argv[2], "w"), ensure_ascii=False)
print(len(links), "links")
print(f"{'book':8}{'verses':>7}{'links':>7}{'¬LXX':>6}{'w≥14':>6}{'w≥14¬LXX':>9}{'per100v':>8}")
rows = []
for b, v in NT.items():
    if b == "Rev": continue
    L = [l for l in links if l["book"] == b]; h = [l for l in L if l["weight"] >= 14]; hn = [l for l in h if not l["lxx"]]
    rows.append((100 * len(hn) / len(v), b, len(v), len(L), sum(1 for l in L if not l["lxx"]), len(h), len(hn)))
for r in sorted(rows, reverse=True): print(f"{r[1]:8}{r[2]:>7}{r[3]:>7}{r[4]:>6}{r[5]:>6}{r[6]:>9}{r[0]:>8.1f}")
