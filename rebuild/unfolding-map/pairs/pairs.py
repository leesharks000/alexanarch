#!/usr/bin/env python3
"""An instrument between the stem count and the reader. A member is a PAIR: two word-stems (five letters) standing within four words of each other in one
verse, neither among the 150 commonest. A pair is rare if it stands in six verses of the New Testament or fewer. Two passages are linked by each rare pair
both hold. Each link is marked by whether the Septuagint has the pair too (within four words in a verse). No hand enters anything.
(A) Calibration on what the file already knows: for each of Matthew's blocks, its best 13 verses of Revelation by links, against 300 other stretches of
Matthew of the same length. (B) Discovery: every 12 verses of every Gospel against every 13 of Revelation; the strongest, listed. (C) The null: the same
with Acts 1-15 and with Hebrews-James-1 Peter in Revelation's place.
   python3 pairs.py <alexanarch root> <engine dir> out.json"""
import sys, re, json, pathlib, collections, random
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
NT, LXX = load("gnt-nestle1904"), load("lxx-swete")
wc = collections.Counter(w[:5] for b, vs in NT.items() for _, t in vs for w in t.split()); STOP = {w for w, _ in wc.most_common(150)}
def pairs(t):
    ws = [w[:5] for w in t.split() if len(w) >= 3]; ws = [w for w in ws if w not in STOP]; out = set()
    for i, a in enumerate(ws):
        for b in ws[i + 1:i + 5]:
            if a != b: out.add((a, b) if a < b else (b, a))
    return out
VP = {b: [(r, pairs(t)) for r, t in vs] for b, vs in NT.items()}
df = collections.Counter(p for b, vs in VP.items() for _, ps in vs for p in ps)
lxxp = set()
for b, vs in LXX.items():
    for _, t in vs: lxxp |= pairs(t)
GOS = ["Matt", "Mark", "Luke", "John"]
def rare(ps): return {p for p in ps if df[p] <= 6}
def windows(seq, L, step=1): return [(i, set().union(*(ps for _, ps in seq[i:i + L]))) for i in range(0, max(1, len(seq) - L + 1), step)]
def seed(seq): return [(r, rare(ps)) for r, ps in seq]
REV = seed(VP["Rev"]); RW = windows(REV, 13)
def best(block, RWx):
    sc = [(len(block & w), i) for i, w in RWx]; return max(sc)
OUT = {}
# (A)
mt = seed(VP["Matt"]); refs = [r for r, _ in mt]
BL = [("the birth", "Matt 1:18", "Matt 2:23"), ("the Sermon, ch. 5", "Matt 5:1", "Matt 5:48"), ("the Sermon, ch. 6", "Matt 6:1", "Matt 6:34"), ("the Sermon, ch. 7", "Matt 7:1", "Matt 7:29"), ("the mission, ch. 10", "Matt 10:1", "Matt 10:42"),
      ("the parables of ch. 13", "Matt 13:24", "Matt 13:52"), ("the community, ch. 18", "Matt 18:1", "Matt 18:35"), ("the labourers", "Matt 20:1", "Matt 20:16"), ("the wedding", "Matt 22:1", "Matt 22:14"),
      ("the woes, ch. 23", "Matt 23:1", "Matt 23:39"), ("the discourse, ch. 24", "Matt 24:1", "Matt 24:51"), ("the virgins", "Matt 25:1", "Matt 25:13"), ("the talents", "Matt 25:14", "Matt 25:30"), ("the sheep and the goats", "Matt 25:31", "Matt 25:46"),
      ("the cross and the tomb", "Matt 27:32", "Matt 28:10"), ("the guard and the tomb", "Matt 27:62", "Matt 28:15")]
A = []; random.seed(1126)
for name, a, z in BL:
    i, j = refs.index(a), refs.index(z); L = j - i + 1; blk = set().union(*(ps for _, ps in mt[i:j + 1])); n, wi = best(blk, RW); shared = sorted(blk & RW[wi][1]); ctrl = []
    for _ in range(300):
        k = random.randrange(0, len(mt) - L)
        if abs(k - i) < L: continue
        ctrl.append(best(set().union(*(ps for _, ps in mt[k:k + L])), RW)[0])
    p = sum(1 for c in ctrl if c >= n) / len(ctrl)
    A.append(dict(block=name, verses=L, links=n, at=f"{REV[wi][0]}–{REV[min(len(REV)-1, wi+12)][0].split()[1]}", pairs=[(x, y, (x, y) in lxxp) for x, y in shared], control_mean=round(sum(ctrl) / len(ctrl), 2), p=round(p, 3)))
    print(f"(A) {name:26} {L:3} verses | most links {n} at {A[-1]['at']} | other stretches of Matthew: mean {A[-1]['control_mean']}, as many in {p:.3f} | {[x+'+'+y+('°' if l else '') for x, y, l in A[-1]['pairs']][:9]}")
OUT["calibration"] = A
# (B) and (C)
def scan(SEED, label, top=30):
    SW = windows(SEED, 13, 3); res = []
    for g in GOS:
        gs = [(r, ps) for r, ps in VP[g]]
        for i, w in windows(gs, 12, 3):
            for k, sw in SW:
                sh = w & sw
                if len(sh) >= 3: res.append((sum(1 for p in sh if p not in lxxp), len(sh), g, gs[i][0], SEED[k][0], sorted(sh)))
    res.sort(key=lambda x: (-x[0], -x[1])); pick, used = [], []
    for nl, n, g, gr, sr, sh in res:
        gi = [r for r, _ in VP[g]].index(gr); si = [r for r, _ in SEED].index(sr)
        if all(not (g == ug and abs(gi - ui) < 12 and abs(si - us) < 13) for ug, ui, us in used): used.append((g, gi, si)); pick.append(dict(not_lxx=nl, links=n, gospel=gr, seed=sr, pairs=["+".join(p) + ("°" if p in lxxp else "") for p in sh]))
        if len(pick) == top: break
    dist = collections.Counter(min(x[0], 8) for x in res); return dict(label=label, verses=len(SEED), window_pairs_with_3=len(res), by_not_lxx=dict(sorted(dist.items())), top=pick)
OUT["revelation"] = scan(REV, "Revelation")
acts = seed(VP["Acts"][:405]); hjp = seed((VP["Heb"] + VP["Jas"] + VP["1Pet"])[:405]); rom = seed((VP["Rom"] + VP["1Cor"])[:405])
OUT["null_acts"] = scan(acts, "Acts, first 405 verses", 6); OUT["null_hjp"] = scan(hjp, "Hebrews, James, 1 Peter, first 405 verses", 6); OUT["null_paul"] = scan(rom, "Romans, 1 Corinthians, first 405 verses", 6)
for k in ("revelation", "null_acts", "null_hjp", "null_paul"):
    o = OUT[k]; print(f"\n(B/C) {o['label']}: window pairs with 3 or more links {o['window_pairs_with_3']} | by links the Septuagint lacks: {o['by_not_lxx']}")
    for x in o["top"][:30 if k == "revelation" else 4]: print(f"   {x['not_lxx']}/{x['links']}  {x['seed']:10} ~ {x['gospel']:11} {x['pairs'][:8]}")
json.dump(OUT, open(sys.argv[3], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
