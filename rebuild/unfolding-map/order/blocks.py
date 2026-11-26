#!/usr/bin/env python3
"""Matthew's own material, block by block, searched in Revelation by machine (the search of 2N.4, made general). For a block of Matthew: its word-stems that
are rare in the New Testament, are in no verse of Mark, and are in Revelation in twelve verses or fewer. Where do they stand together (13 verses of Revelation)?
Control: the same number of stems drawn at random, 400 times, from all of Matthew's such stems; how often does a random draw stand together as much?
   python3 blocks.py <alexanarch root> <engine dir> out.json"""
import sys, re, json, pathlib, collections, random
sys.path.insert(0, sys.argv[2]); import midrash as E
root = pathlib.Path(sys.argv[1]) / "data/corpora/gnt-nestle1904/text"
def sq(s): return re.sub(r"\s+", " ", E.norm(s)).strip()
def book(b): return [(l.split("\t", 1)[0].strip(), sq(l.split("\t", 1)[1])) for l in (root / f"{b}.txt").read_text(encoding="utf-8").splitlines() if "\t" in l]
BOOKS = {p.stem: book(p.stem) for p in sorted(root.glob("*.txt"))}; rev, mt = BOOKS["Rev"], BOOKS["Matt"]
def stems(t): return {w[:5] for w in t.split() if len(w) >= 5}
df = collections.Counter(s for b, vs in BOOKS.items() for _, t in vs for s in stems(t)); rdf = collections.Counter(s for _, t in rev for s in stems(t))
mark = set().union(*(stems(t) for _, t in BOOKS["Mark"])); rv = [stems(t) for _, t in rev]; W = [set().union(*rv[i:i + 13]) for i in range(len(rev) - 12)]
ok = lambda s: df[s] <= 60 and 0 < rdf[s] <= 12 and s not in mark
POOL = sorted({s for _, t in mt for s in stems(t) if ok(s)})
def best(S): sc = [len(S & w) for w in W]; return sc
refs = [r for r, _ in mt]
def block(a, z): i, j = refs.index(a), refs.index(z); return {s for _, t in mt[i:j + 1] for s in stems(t) if ok(s)}, j - i + 1
BL = [("the birth", "Matt 1:18", "Matt 2:23"), ("the Sermon, ch. 5", "Matt 5:1", "Matt 5:48"), ("the Sermon, ch. 6", "Matt 6:1", "Matt 6:34"), ("the Sermon, ch. 7", "Matt 7:1", "Matt 7:29"), ("the mission, ch. 10", "Matt 10:1", "Matt 10:42"),
      ("the parables of ch. 13", "Matt 13:24", "Matt 13:52"), ("Peter and the keys", "Matt 16:13", "Matt 16:20"), ("the community, ch. 18", "Matt 18:1", "Matt 18:35"), ("the labourers", "Matt 20:1", "Matt 20:16"), ("the wedding", "Matt 22:1", "Matt 22:14"),
      ("the woes, ch. 23", "Matt 23:1", "Matt 23:39"), ("the discourse, ch. 24", "Matt 24:1", "Matt 24:51"), ("the virgins", "Matt 25:1", "Matt 25:13"), ("the talents", "Matt 25:14", "Matt 25:30"), ("the sheep and the goats", "Matt 25:31", "Matt 25:46"),
      ("Judas's end", "Matt 27:3", "Matt 27:10"), ("the guard and the tomb", "Matt 27:62", "Matt 28:15"), ("the commission", "Matt 28:16", "Matt 28:20")]
OUT = []; random.seed(1126)
for name, a, z in BL:
    S, L = block(a, z); sc = best(S); top = max(sc) if S else 0
    ctrl = [max(best(set(random.sample(POOL, len(S))))) for _ in range(400)] if len(S) >= 4 else []
    p = sum(1 for c in ctrl if c >= top) / len(ctrl) if ctrl else None; pick, used = [], []
    for x, i in sorted(((x, i) for i, x in enumerate(sc)), reverse=True):
        if all(abs(i - j) >= 13 for j in used): used.append(i); pick.append((x, rev[i][0], rev[i + 12][0].split()[1], sorted(S & W[i])))
        if len(pick) == 3: break
    OUT.append(dict(block=name, verses=L, stems=len(S), top=top, control_mean=round(sum(ctrl) / len(ctrl), 2) if ctrl else None, p=p, windows=pick))
    print(f"\n{name} ({a.split()[1]}–{z.split()[1]}, {L} verses): own stems in Revelation {len(S)} | most together {top} | random draws: mean {OUT[-1]['control_mean']}, as many or more in {p} of draws")
    for x in pick: print(f"   {x[0]:2} {x[1]}–{x[2]}  {x[3]}")
print("\nblocks:", len(OUT), "| with p at or below 0.05:", [o["block"] for o in OUT if o["p"] is not None and o["p"] <= 0.05], "| pool of Matthew's such stems:", len(POOL))
json.dump(OUT, open(sys.argv[3], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
