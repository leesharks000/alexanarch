#!/usr/bin/env python3
"""The printed text itself (2P.6). Three printed texts of the New Testament set side by side, verse by verse: Nestle 1904 (seated; a reconstruction),
Tischendorf's eighth edition (1869-72; a reconstruction), and Robinson and Pierpont's Byzantine text (the reading of the majority of the manuscripts).
The two not seated were fetched today from their public repositories (byztxt/byzantine-majority-text, CC0, commit 788ffe7c; morphgnt/tischendorf-data,
public, commit 795f2f4f) and are read from the fetch, not from a seat.
(1) The loci: every derivation of the engine run again with its New Testament verses read from each text. Does a member of Revelation stand in the
    majority's verse and not in the reconstruction's, or the reverse?
(2) At each locus, the words in which the texts differ: do they bring the Gospel's verse toward the seed's wording or away?
(3) The whole: every Gospel verse where the majority and Nestle differ. Of the words only the majority has and the words only Nestle has, what share are
    Revelation's words? The same for Acts's, Romans's, Hebrews's words, as the measure of what any book's share would be.
(4) The same asked of Revelation's own text against the Gospels' words.
   python3 texts.py <alexanarch root> <engine dir> <fetch dir> out.json"""
import sys, re, json, csv, pathlib, collections
sys.path.insert(0, sys.argv[2]); import midrash as E
root, fetch = sys.argv[1], pathlib.Path(sys.argv[3])
def sq(s): return re.sub(r"\s+", " ", E.norm(s)).strip()
S0 = E.Seats(root); N = {r: t for r, t in S0._orig("gnt-nestle1904").items()}
BZ = dict(MAT="Matt", MAR="Mark", LUK="Luke", JOH="John", ACT="Acts", ROM="Rom", HEB="Heb", REV="Rev", JAM="Jas", JUD="Jude", **{"1CO": "1Cor", "2CO": "2Cor", "GAL": "Gal", "EPH": "Eph", "PHP": "Phil", "COL": "Col", "1TH": "1Thess", "2TH": "2Thess", "1TI": "1Tim", "2TI": "2Tim", "TIT": "Titus", "PHM": "Phlm", "1PE": "1Pet", "2PE": "2Pet", "1JO": "1John", "2JO": "2John", "3JO": "3John"})
B = {}
for code, nm in BZ.items():
    for row in csv.DictReader(open(fetch / "byzantine-majority-text/csv-unicode/ccat/no-variants" / f"{code}.csv", encoding="utf-8")): B[f"{nm} {row['chapter']}:{row['verse']}"] = row["text"].replace("¶", " ")
TS = dict(MT="Matt", MR="Mark", LU="Luke", JOH="John", AC="Acts", RO="Rom", HEB="Heb", RE="Rev", JAS="Jas", JUDE="Jude", GA="Gal", EPH="Eph", PHP="Phil", COL="Col", TIT="Titus", PHM="Phlm", **{"1CO": "1Cor", "2CO": "2Cor", "1TH": "1Thess", "2TH": "2Thess", "1TI": "1Tim", "2TI": "2Tim", "1PE": "1Pet", "2PE": "2Pet", "1JO": "1John", "2JO": "2John", "3JO": "3John"})
T = collections.defaultdict(list)
for code, nm in TS.items():
    for l in open(fetch / "tischendorf-data/word-per-line/2.8/Unicode" / f"{code}.txt", encoding="utf-8"):
        p = l.split()
        if len(p) > 3: T[f"{nm} {p[1].split('.')[0]}"].append(p[3])
T = {k: " ".join(v) for k, v in T.items()}
nk = set(N); print("verses: Nestle", len(N), "| Tischendorf", len(T), f"(shared refs {len(nk & set(T))})", "| Byzantine", len(B), f"(shared refs {len(nk & set(B))})")
class Alt(E.Seats):
    def __init__(self, root, D): super().__init__(root); self.D = D
    def _orig(self, corpus): return {}
    def get(self, loc):
        if not loc.startswith("gnt:"): return super().get(loc)
        refs = []
        for part in loc[4:].split(" + "):
            m = re.match(r"(.+ \d+:)(\d+)-(\d+)$", part); refs += [f"{m.group(1)}{i}" for i in range(int(m.group(2)), int(m.group(3)) + 1)] if m else [part]
        return " ".join(self.D.get(r, "") for r in refs)
DS = json.load(open(pathlib.Path(sys.argv[2]) / "derivations.json", encoding="utf-8"))["derivations"]; OUT = dict(loci=[])
def stems(t): return {w[:5] for w in sq(t).split() if len(w) >= 4}
def refs_of(loc):
    out = []
    for part in loc[4:].split(" + "):
        m = re.match(r"(.+ \d+:)(\d+)-(\d+)$", part); out += [f"{m.group(1)}{i}" for i in range(int(m.group(2)), int(m.group(3)) + 1)] if m else [part]
    return out
tw = collections.Counter(); changed = []
for D in DS:
    if not D["target"].startswith("gnt:"): continue
    row = dict(id=D["id"]); res = {}
    for name, txt in (("Nestle", N), ("Tischendorf", T), ("Byzantine", B)):
        try: r = E.run(D, Alt(root, txt)); res[name] = dict(score=r["target"]["score"], passes=r["target"]["passes"], missing=r["target"]["missing"], extra=r["target"]["kept_but_should_be_dropped"], seed=[k for k, v in r["seed"]["members_found"].items() if not v])
        except AssertionError as e: res[name] = dict(score=None, error=str(e)[:80])
    row["texts"] = res
    # (2) differing words at the target, set against the seed's wording
    if D["seed"].startswith("gnt:"):
        tr = refs_of(D["target"]); seedst = stems(" ".join(N.get(r, "") for r in refs_of(D["seed"]))) | stems(" ".join(B.get(r, "") for r in refs_of(D["seed"])))
        nt_, bt_, tt_ = (stems(" ".join(X.get(r, "") for r in tr)) for X in (N, B, T)); row["byz_only_toward"] = sorted((bt_ - nt_) & seedst); row["nestle_only_toward"] = sorted((nt_ - bt_) & seedst)
        row["tisch_vs_byz"] = (sorted((bt_ - tt_) & seedst), sorted((tt_ - bt_) & seedst)); tw["majority has the seed's word, Nestle not"] += len(row["byz_only_toward"]); tw["Nestle has the seed's word, majority not"] += len(row["nestle_only_toward"])
        tw["majority has it, Tischendorf not"] += len(row["tisch_vs_byz"][0]); tw["Tischendorf has it, majority not"] += len(row["tisch_vs_byz"][1])
    OUT["loci"].append(row); sc = [res[k].get("score") for k in ("Nestle", "Tischendorf", "Byzantine")]
    if len(set(sc)) > 1 or any(res[k].get("seed") for k in res) or row.get("byz_only_toward") or row.get("nestle_only_toward"): changed.append(row)
print(f"\n(1) derivations with a New Testament target: {len(OUT['loci'])} | passing under Nestle {sum(1 for r in OUT['loci'] if r['texts']['Nestle'].get('passes'))}, Tischendorf {sum(1 for r in OUT['loci'] if r['texts']['Tischendorf'].get('passes'))}, the majority text {sum(1 for r in OUT['loci'] if r['texts']['Byzantine'].get('passes'))}")
for r in changed:
    t = r["texts"]; print(f"   {r['id']:34} N {t['Nestle'].get('score')} T {t['Tischendorf'].get('score')} B {t['Byzantine'].get('score')} | missing T {t['Tischendorf'].get('missing')} B {t['Byzantine'].get('missing')} | seed lacks T {t['Tischendorf'].get('seed')} B {t['Byzantine'].get('seed')} | toward seed: majority only {r.get('byz_only_toward')} Nestle only {r.get('nestle_only_toward')}")
print("(2)", dict(tw)); OUT["toward"] = dict(tw)
# (3) the whole
GOS = ["Matt", "Mark", "Luke", "John"]; bk = lambda r: r.split()[0]
df = collections.Counter(s for r, t in N.items() for s in stems(t))
def vocab(book, X): return {s for r, t in X.items() if bk(r) == book for s in stems(t)}
VOC = {b: {s for s in vocab(b, N) | vocab(b, B) if df[s] <= 60} for b in ("Rev", "Acts", "Rom", "Heb", "1Cor", "Jas")}
def whole(A, Bx, la, lb, books):
    only_a, only_b, nv = collections.Counter(), collections.Counter(), 0
    for r in A:
        if bk(r) not in books or r not in Bx: continue
        a, b = stems(A[r]), stems(Bx[r])
        if a != b: nv += 1; only_a.update(a - b); only_b.update(b - a)
    return nv, only_a, only_b
nv, on, ob = whole(N, B, "Nestle", "majority", GOS); res3 = dict(verses_differing=nv, nestle_only=sum(on.values()), majority_only=sum(ob.values()), by_book={})
print(f"\n(3) Gospel verses where Nestle and the majority differ in a word-stem: {nv} | stems only Nestle has {sum(on.values())}, only the majority has {sum(ob.values())}")
for b, V in VOC.items():
    a = sum(c for s, c in on.items() if s in V); m = sum(c for s, c in ob.items() if s in V); res3["by_book"][b] = dict(nestle_only=a, majority_only=m, share_nestle=round(a / sum(on.values()), 4), share_majority=round(m / sum(ob.values()), 4), ratio=round((m / sum(ob.values())) / (a / sum(on.values())), 3))
    print(f"   words of {b:5} (rare stems, {len(V)}): among Nestle-only {a} ({a/sum(on.values()):.3f}) | among majority-only {m} ({m/sum(ob.values()):.3f}) | majority/Nestle {res3['by_book'][b]['ratio']}")
OUT["whole_gospels"] = res3
nv, tn, tb = whole(T, B, "Tischendorf", "majority", GOS); res3t = {}
for b, V in VOC.items():
    a = sum(c for s, c in tn.items() if s in V); m = sum(c for s, c in tb.items() if s in V); res3t[b] = round((m / sum(tb.values())) / (a / sum(tn.values())), 3)
print("   the same with Tischendorf for Nestle, majority/Tischendorf:", res3t); OUT["whole_gospels_tischendorf"] = res3t
# (4) Revelation's own text against other books' words
GV = {b: {s for s in vocab(b, N) | vocab(b, B) if df[s] <= 60} for b in ("Matt", "Mark", "Luke", "John", "Acts", "Rom", "Heb")}
nv, on, ob = whole(N, B, "Nestle", "majority", ["Rev"]); res4 = {}
print(f"\n(4) verses of Revelation where Nestle and the majority differ: {nv} of 405 | stems only Nestle has {sum(on.values())}, only the majority has {sum(ob.values())}")
for b, V in GV.items():
    a = sum(c for s, c in on.items() if s in V); m = sum(c for s, c in ob.items() if s in V); res4[b] = dict(nestle_only=a, majority_only=m, ratio=round((m / sum(ob.values())) / max(1e-9, a / sum(on.values())), 3))
    print(f"   words of {b:5}: among Nestle-only {a} ({a/sum(on.values()):.3f}) | among majority-only {m} ({m/sum(ob.values()):.3f}) | majority/Nestle {res4[b]['ratio']}")
OUT["whole_revelation"] = res4
json.dump(OUT, open(sys.argv[4], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
