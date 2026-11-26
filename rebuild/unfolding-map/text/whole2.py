#!/usr/bin/env python3
"""(3) again, taken apart. Which of Revelation's words are the ones only the majority, or only Nestle, has in the Gospels; and the share counted by
distinct word (each stem once per Gospel and side), so that one habit of spelling repeated forty times counts once.
   python3 whole2.py <alexanarch root> <engine dir> <fetch dir> out.json"""
import sys, re, json, csv, pathlib, collections, random
sys.path.insert(0, sys.argv[2]); import midrash as E
root, fetch = sys.argv[1], pathlib.Path(sys.argv[3])
def sq(s): return re.sub(r"\s+", " ", E.norm(s)).strip()
N = dict(E.Seats(root)._orig("gnt-nestle1904")); B = {}
BZ = dict(MAT="Matt", MAR="Mark", LUK="Luke", JOH="John", ACT="Acts", ROM="Rom", HEB="Heb", REV="Rev", JAM="Jas", **{"1CO": "1Cor"})
for code, nm in BZ.items():
    for row in csv.DictReader(open(fetch / "byzantine-majority-text/csv-unicode/ccat/no-variants" / f"{code}.csv", encoding="utf-8")): B[f"{nm} {row['chapter']}:{row['verse']}"] = row["text"].replace("¶", " ")
def stems(t): return {w[:5] for w in sq(t).split() if len(w) >= 4}
bk = lambda r: r.split()[0]; GOS = ["Matt", "Mark", "Luke", "John"]
df = collections.Counter(s for r, t in N.items() for s in stems(t))
def vocab(b): return {s for X in (N, B) for r, t in X.items() if bk(r) == b for s in stems(t) if df[s] <= 60}
VOC = {b: vocab(b) for b in ("Rev", "Acts", "Rom", "Heb", "1Cor", "Jas")}
on, ob = collections.Counter(), collections.Counter(); ton, tob = set(), set()
for r in N:
    if bk(r) in GOS and r in B:
        a, b = stems(N[r]), stems(B[r]); on.update(a - b); ob.update(b - a); ton |= {(bk(r), s) for s in a - b}; tob |= {(bk(r), s) for s in b - a}
V = VOC["Rev"]
print("Revelation's words only the majority has, by count:", [(s, c) for s, c in ob.most_common(400) if s in V][:22])
print("Revelation's words only Nestle has, by count:", [(s, c) for s, c in on.most_common(400) if s in V][:22])
out = {}
print("\ncounted by distinct word, once per Gospel and side:")
for b, Vb in VOC.items():
    a = sum(1 for g, s in ton if s in Vb); m = sum(1 for g, s in tob if s in Vb); ra = (m / len(tob)) / (a / len(ton)); out[b] = dict(nestle=a, majority=m, share_nestle=round(a / len(ton), 4), share_majority=round(m / len(tob), 4), ratio=round(ra, 3))
    print(f"   words of {b:5}: Nestle-only {a} of {len(ton)} ({a/len(ton):.3f}) | majority-only {m} of {len(tob)} ({m/len(tob):.3f}) | majority/Nestle {ra:.3f}")
# the same with the forty commonest differing stems removed from both sides
top = {s for s, _ in (on + ob).most_common(40)}
print("\nwith the forty stems that differ most often removed (spelling and habit):")
for b, Vb in VOC.items():
    a = sum(c for s, c in on.items() if s in Vb and s not in top); m = sum(c for s, c in ob.items() if s in Vb and s not in top); A = sum(c for s, c in on.items() if s not in top); Mx = sum(c for s, c in ob.items() if s not in top)
    out[b]["ratio_without_top40"] = round((m / Mx) / (a / A), 3); print(f"   words of {b:5}: {a}/{A} ({a/A:.3f}) | {m}/{Mx} ({m/Mx:.3f}) | majority/Nestle {out[b]['ratio_without_top40']}")
# a null for the ratio: 2,000 random vocabularies the size of Revelation's, drawn from all rare stems
allr = sorted({s for X in (N, B) for r, t in X.items() for s in stems(t) if df[s] <= 60}); random.seed(1126); TN, TB = len(ton), len(tob); obs = out["Rev"]["ratio"]; ge = 0; rs = []
for _ in range(2000):
    Vr = set(random.sample(allr, len(V))); a = sum(1 for g, s in ton if s in Vr); m = sum(1 for g, s in tob if s in Vr); rs.append((m / TB) / (a / TN))
rs.sort(); print(f"\nrandom vocabularies of {len(V)} rare stems: ratio mean {sum(rs)/len(rs):.3f}, 2.5%–97.5% {rs[50]:.3f}–{rs[1949]:.3f}; Revelation's {obs}; share of random at or above it {sum(1 for x in rs if x >= obs)/len(rs):.4f}")
out["null"] = dict(mean=round(sum(rs) / len(rs), 3), lo=round(rs[50], 3), hi=round(rs[1949], 3), p=sum(1 for x in rs if x >= obs) / len(rs))
json.dump(out, open(sys.argv[4], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
