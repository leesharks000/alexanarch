#!/usr/bin/env python3
"""The ordered run. Members of a stretch of Revelation, in Revelation's order, against a stretch of a Gospel: each member found there (own form, or loosened,
marked) is placed at its first verse; Kendall's tau between the two orders; the same with the orders shuffled 20,000 times. No member is chosen by hand: all
members of the section with a hit in the stretch are used, unless the member is in more than 3% of the Gospel's verses.
   python3 ordered.py <alexanarch root> <engine dir> out.json"""
import sys, re, json, pathlib, collections, random, itertools
sys.path.insert(0, sys.argv[2]); import midrash as E
from members import M
root = pathlib.Path(sys.argv[1]) / "data/corpora/gnt-nestle1904/text"
def sq(s): return re.sub(r"\s+", " ", E.norm(s)).strip()
def book(b): return [(l.split("\t", 1)[0].strip(), sq(l.split("\t", 1)[1])) for l in (root / f"{b}.txt").read_text(encoding="utf-8").splitlines() if "\t" in l]
def tau(xs, ys):
    c = d = 0
    for (a, b), (e, f) in itertools.combinations(list(zip(xs, ys)), 2):
        s = (a - e) * (b - f); c += s > 0; d += s < 0
    n = c + d; return ((c - d) / n if n else 0.0), c, d
def run(name, secs, vlo, vhi, b, a, z, loose):
    vs = book(b); refs = [r for r, _ in vs]; i, j = refs.index(a), refs.index(z); seg = vs[i:j + 1]; pts = []
    for k, (sec, v, mid, gloss, rx, rx2) in enumerate(M):
        ch, ve = map(int, v.split(":"))
        if sec not in secs or not (vlo <= (ch, ve) <= vhi): continue
        cs = [(re.compile(rx), "")] + ([(re.compile(rx2), "*")] if loose and rx2 else [])
        if sum(1 for _, t in vs if cs[0][0].search(t)) > 0.03 * len(vs): continue
        hit = next(((p, r, mk) for p, (r, t) in enumerate(seg) for c, mk in cs if c.search(t)), None)
        if hit: pts.append((k, hit[0], v, mid + hit[2], hit[1].split()[1]))
    if len(pts) < 4: return dict(name=name, n=len(pts), pts=pts)
    t, c, d = tau([p[0] for p in pts], [p[1] for p in pts]); random.seed(1126); ys = [p[1] for p in pts]; ex = 0; N = 20000
    for _ in range(N):
        yy = ys[:]; random.shuffle(yy); ex += abs(tau([p[0] for p in pts], yy)[0]) >= abs(t) - 1e-12
    return dict(name=name, n=len(pts), tau=round(t, 3), concordant=c, discordant=d, p=ex / N, pts=pts)
OUT = []
for loose in (False, True):
    for name, secs, lo, hi, b, a, z in (
        ("Rev 11:14-12:17 against Matthew 24", "JG", (11, 14), (12, 17), "Matt", "Matt 24:1", "Matt 24:51"),
        ("Rev 11:14-12:17 against Mark 13", "JG", (11, 14), (12, 17), "Mark", "Mark 13:1", "Mark 13:37"),
        ("Rev 11:14-12:17 against Luke 21", "JG", (11, 14), (12, 17), "Luke", "Luke 21:5", "Luke 21:36"),
        ("Rev 11:10-12:17 against John 12:20-16:33", "WJG", (11, 10), (12, 17), "John", "John 12:20", "John 16:33"),
        ("Rev 12 against Matthew 1-2", "G", (12, 1), (12, 17), "Matt", "Matt 1:18", "Matt 2:23"),
        ("Rev 11:1-13 against Matthew's cross and tomb", "W", (11, 1), (11, 13), "Matt", "Matt 27:32", "Matt 28:10"),
        ("Rev 11:1-13 against Mark's cross and tomb", "W", (11, 1), (11, 13), "Mark", "Mark 15:21", "Mark 16:8"),
        ("Rev 11:1-13 against Luke's cross and tomb", "W", (11, 1), (11, 13), "Luke", "Luke 23:26", "Luke 24:12"),
        ("Rev 11:1-12:17 against the whole of Matthew", "WJG", (11, 1), (12, 17), "Matt", "Matt 1:1", "Matt 28:20")):
        o = run(name, secs, lo, hi, b, a, z, loose); o["forms"] = "own and loosened" if loose else "own"; OUT.append(o)
        print(f"\n{name} | {o['forms']} | members placed {o['n']}" + (f" | tau {o['tau']:+.3f} (concordant {o['concordant']}, discordant {o['discordant']}) | p={o['p']:.4f}" if "tau" in o else " | too few"))
        print("   in Revelation's order:", [(p[2], p[3], p[4]) for p in o["pts"]])
json.dump(OUT, open(sys.argv[3], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
