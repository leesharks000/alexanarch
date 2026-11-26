#!/usr/bin/env python3
"""The control on 2Y.4-5 made a count (2Z.1). What distinguished the pairs read in the seat was the PAIRING THE REST LACKS: two rare words in one verse of the section
and in one verse of the block, and in no verse elsewhere. Counted here by machine, the same way for Revelation, for Acts and for Isaiah in Revelation's place.
  A pairing = two crude stems, each in at most 120 verses of the New Testament, together in a verse of the section and together in a verse of the block.
  EXCLUSIVE = together in no other verse of the New Testament outside the four Gospels, and in no verse of the Septuagint, the section's own verses apart.
   python3 excl.py <alexanarch root> <engine dir> excl.json"""
import sys, re, json, math, pathlib, collections, itertools
sys.path.insert(0, sys.argv[2]); import midrash as E
exec(open(pathlib.Path(__file__).with_name("blocks.py")).read().split("GV = [")[0].split('"""', 2)[2].replace("import sys, re, json, math, pathlib, collections", ""))
ALL = [(("N", r), ST[r]) for r in refs] + [(("L", b + r), set(filter(None, map(stem, t.split())))) for b, r, t in LXl]
GOSP = {("N", r) for r in refs if r.split()[0] in ("Matt", "Mark", "Luke", "John")}
IX = collections.defaultdict(set)
for k, ss in ALL:
    if k in GOSP: continue
    for s in ss:
        if s in W: IX[s].add(k)
SK = dict(ALL)
def pairs(keys):
    P = collections.defaultdict(list)
    for k in keys:
        ss = sorted(s for s in SK[k] if s in W)
        for a, b in itertools.combinations(ss, 2): P[(a, b)].append(k)
    return P
BP = {bl: pairs([("N", r) for r in span(a, b)]) for bl, a, b in BLK}
def run(name, secs):
    tot = 0; rows = []; nv = 0
    for l, keys in secs:
        SP = pairs(keys); ks = set(keys); nv += len(keys)
        for bl, _, _ in BLK:
            ex = [(p, SP[p], BP[bl][p]) for p in SP.keys() & BP[bl].keys() if not ((IX[p[0]] & IX[p[1]]) - ks)]
            tot += len(ex); rows.append((len(ex), l, bl, ex))
    rows.sort(key=lambda x: -x[0]); print(f"\n== {name}: source verses {nv}; exclusive pairings over all 360 section-block pairs: {tot} ({100*tot/nv:.1f} per hundred source verses); section-block pairs with five or more: {sum(1 for r in rows if r[0]>=5)}; the highest: {rows[0][0]}")
    for n, l, bl, ex in rows[:9]:
        print(f"   {n:3}  {l:42} × {bl:34} " + "; ".join(f"{a}+{b} [{v[0][1].split()[-1] if v[0][0]=='N' else v[0][1][-6:]}|{w[0][1].split(' ',1)[1]}]" for (a, b), v, w in ex[:7]))
    return dict(name=name, verses=nv, total=tot, per100=round(100 * tot / nv, 1), ge5=sum(1 for r in rows if r[0] >= 5), top=[(n, l, bl, [(a, b, v[0][1], w[0][1]) for (a, b), v, w in ex[:12]]) for n, l, bl, ex in rows[:14]])
rv = [("N", r) for r in refs if r.startswith("Rev ")]; OUT = [run("Revelation", [(l, [("N", r) for r in span(a, b)]) for l, a, b in SEC])]
ac = [("N", r) for r in refs if r.startswith("Acts ")]; k = len(ac) // 10; OUT.append(run("Acts, cut in ten", [(f"Acts part {i+1} ({ac[i*k][1]}–)", ac[i * k:(i + 1) * k]) for i in range(10)]))
ik = [("L", b + r) for b, r, t in LXl if r.startswith("Ἠσα")]; k = len(ik) // 10; OUT.append(run("Isaiah, cut in ten", [(f"Isa part {i+1} ({ik[i*k][1][-5:]}–)", ik[i * k:(i + 1) * k]) for i in range(10)]))
for nm, pre in (("Hebrews, James, 1 Peter", ("Heb ", "Jas ", "1Pet ")), ("Romans, 1 Corinthians", ("Rom ", "1Cor "))):
    v = [("N", r) for r in refs if r.startswith(pre)]; k = len(v) // 10; OUT.append(run(nm + ", cut in ten", [(f"part {i+1} ({v[i*k][1]}–)", v[i * k:(i + 1) * k]) for i in range(10)]))
json.dump(OUT, open(sys.argv[3], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
