#!/usr/bin/env python3
"""A positive control for 2Q.4. The measure there (among the words only the majority text has, and only Nestle has, the share that are a given book's words,
by distinct word) found nothing for Revelation. Can it find anything? Copyists are known to have brought Mark's and Luke's wording toward Matthew's. So: in
the verses of ONE Gospel, the share of ANOTHER Gospel's words among what only each text has. If the measure sees harmonizing, Matthew's words will be commoner
among what only the majority has in Mark. Each ratio is set against 1,000 random vocabularies of the same size.
   python3 control.py <alexanarch root> <engine dir> <fetch dir> out.json"""
import sys, re, json, csv, pathlib, collections, random
sys.path.insert(0, sys.argv[2]); import midrash as E
fetch = pathlib.Path(sys.argv[3]); N = dict(E.Seats(sys.argv[1])._orig("gnt-nestle1904")); B = {}
for code, nm in dict(MAT="Matt", MAR="Mark", LUK="Luke", JOH="John", REV="Rev", ACT="Acts", ROM="Rom").items():
    for row in csv.DictReader(open(fetch / "byzantine-majority-text/csv-unicode/ccat/no-variants" / f"{code}.csv", encoding="utf-8")): B[f"{nm} {row['chapter']}:{row['verse']}"] = row["text"].replace("¶", " ")
def stems(t): return {w[:5] for w in re.sub(r"\s+", " ", E.norm(t)).split() if len(w) >= 4}
bk = lambda r: r.split()[0]; df = collections.Counter(s for r, t in N.items() for s in stems(t))
def vocab(b): return {s for r, t in N.items() if bk(r) == b for s in stems(t) if df[s] <= 60}
allr = sorted({s for r, t in N.items() for s in stems(t) if df[s] <= 60}); random.seed(1126); OUT = {}
for g in ("Mark", "Luke", "Matt", "John"):
    ton, tob = set(), set()
    for r in N:
        if bk(r) == g and r in B: a, b = stems(N[r]), stems(B[r]); ton |= a - b; tob |= b - a
    own = vocab(g); print(f"\nin {g}: distinct stems only Nestle has {len(ton)}, only the majority has {len(tob)}")
    for h in ("Matt", "Mark", "Luke", "John", "Rev", "Acts", "Rom"):
        if h == g: continue
        V = vocab(h); a = len(ton & V); m = len(tob & V); ratio = (m / len(tob)) / (a / len(ton)); rs = []
        for _ in range(1000):
            Vr = set(random.sample(allr, len(V))); x, y = len(ton & Vr), len(tob & Vr); rs.append((y / len(tob)) / max(x / len(ton), 1e-9))
        p = sum(1 for x in rs if x >= ratio) / len(rs); OUT[f"{g}<-{h}"] = dict(nestle=a, majority=m, ratio=round(ratio, 3), p_above=p)
        print(f"   words of {h:5}: Nestle-only {a} ({a/len(ton):.3f}) | majority-only {m} ({m/len(tob):.3f}) | ratio {ratio:.2f} | random at or above: {p:.3f}")
json.dump(OUT, open(sys.argv[4], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
