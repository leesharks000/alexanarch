#!/usr/bin/env python3
"""THE ALGORITHM, version 1 (the author, 19:50: "we are *building* the best algorithm we are able for turning revelation into matthew and the rest,
and then we are testing if it holds and lets us predict other things").

  TRANSFORM(seed: verses of Revelation) -> a place in the Gospels
    1. read the seed's words (crude stems; words in more than 400 verses of the New Testament are not candidates);
    2. KEEP-MODEL: for each word, the chance it is kept, from six facts about the word that can be known without any Gospel passage in view:
         its rarity in the New Testament; how much of its use is Revelation's own; whether the Gospels have it at all;
         whether it is a proper name; whether it is a number; its rarity in the Septuagint;
       the weights are LEARNED from the derivations in the engine (which words of each seed the declared transform kept, which it let go);
    3. EMIT the kept words, each weighted by chance-of-keeping times rarity;
    4. FIND the stretch of the Gospels, of a stated length, that holds most of that weight (a word said twice counts a quarter more).
  TEST 1 (does it hold): each derivation in turn is hidden, the model learned from the others, and the hidden seed transformed.
         Where does the declared target rank among every stretch of that length in the four Gospels? Against the same search with no model.
  TEST 2 (Matthew to the rest): learned from the derivations whose target is Matthew only; tested on Mark's, Luke's and John's.
  PREDICT: every pair of consecutive verses of Revelation that is in no derivation is transformed; the strongest findings are listed to be read.
   python3 algo.py <alexanarch root> <engine dir> algo.json"""
import sys, re, json, math, pathlib, collections, unicodedata
import numpy as np
sys.path.insert(0, sys.argv[2]); import midrash as E
root = pathlib.Path(sys.argv[1]) / "data/corpora"
END = sorted("ουσιν ομεθα εσθαι ησαν ουσα ουσι ομεν ετε ουσ οισ αισ ασι ων ου οσ ον οι ην ησ ασ αι εσ ει εν α η ω ε ι ν σ".split(), key=len, reverse=True)
def stem(w):
    if len(w) < 4: return None
    for e in END:
        if w.endswith(e) and len(w) - len(e) >= 3: w = w[:-len(e)]; break
    return w[:5]
def load(c, raw=False):
    o = []
    for p in sorted((root / c / "text").glob("*.txt")):
        seen = set()
        for l in p.read_text(encoding="utf-8", errors="ignore").splitlines():
            if "\t" in l:
                r, t = l.split("\t", 1); r = r.strip()
                if re.search(r"\d+:\d+$", r) and r not in seen: seen.add(r); o.append((r, t if raw else re.sub(r"\s+", " ", E.norm(t)).strip()))
    return o
NT = load("gnt-nestle1904"); NTraw = dict(load("gnt-nestle1904", raw=True)); LX = load("lxx-swete"); D = dict(NT); refs = [r for r, _ in NT]; GOS = ("Matt", "Mark", "Luke", "John")
SS = {r: [stem(w) for w in t.split()] for r, t in NT}; dfN = collections.Counter(s for r in SS for s in set(SS[r]) if s); dfR = collections.Counter(s for r in SS if r.startswith("Rev ") for s in set(SS[r]) if s)
dfG = collections.Counter(s for r in SS if r.split()[0] in GOS for s in set(SS[r]) if s); dfL = collections.Counter(s for _, t in LX for s in set(map(stem, t.split())) if s); N = len(NT)
cap = collections.Counter(); low = collections.Counter()
for r, t in NTraw.items():
    for i, w in enumerate(re.findall(r"[^\s.,;·:()\[\]«»“”\"']+", t)):
        n = E.norm(w).strip(); s = stem(n) if re.fullmatch(r"[α-ω]+", n) else None
        if not s: continue
        if unicodedata.normalize("NFD", w)[0].isupper() and i > 0: cap[s] += 1
        else: low[s] += 1
NAMES = {s for s, c in cap.items() if c >= 2 and c / (c + low[s]) >= 0.8}
NUM = {stem(w) for w in "επτα δωδεκα τεσσαρεσ τεσσαρων τεσσερα χιλια χιλιαδεσ δεκα τρεισ τριτον τεταρτον πεμπτοσ εκτοσ εβδομοσ εξηκοντα διακοσιασ τεσσερακοντα εικοσι ημισυ μυριαδεσ εκατον πεντε δευτεροσ ογδοοσ ενατοσ δεκατοσ ενδεκατοσ δωδεκατοσ".split()} - {None}
idf = lambda s: math.log(N / max(1, dfN[s]))
def feats(s): return [idf(s), math.log((dfR[s] + 1) / (dfN[s] + 1)), 1.0 if dfG[s] == 0 else 0.0, 1.0 if s in NAMES else 0.0, 1.0 if s in NUM else 0.0, math.log((dfL[s] + 1))]
FN = ["rarity in the New Testament", "share of its use that is Revelation's", "absent from the Gospels", "a proper name", "a number", "frequency in the Septuagint"]
cand = lambda s: s and dfN[s] <= 400
def verses(loc):
    out = []
    for part in loc.split(":", 1)[1].split(" + "):
        m = re.match(r"(\S+) (\d+):(\d+)(?:-(\d+))?$", part.strip())
        if m: out += [f"{m[1]} {m[2]}:{i}" for i in range(int(m[3]), int(m[4] or m[3]) + 1)]
    return [v for v in out if v in D]
DER = json.load(open(pathlib.Path(sys.argv[2]) / "derivations.json"))["derivations"]; DATA = []
for d in DER:
    if not d["seed"].startswith("gnt:Rev") or not d["target"].startswith("gnt:"): continue
    sv, tv = verses(d["seed"]), verses(d["target"])
    if not sv or not tv or tv[0].split()[0] not in GOS: continue
    M = {m["id"]: m for m in d["members"]}; state = [k for k, m in M.items() if m.get("in_seed", True)]
    for st in d["steps"]:
        if st["op"] == "PARTITION": state = [k for k in state if k in st["keep"]]
        elif "old" in st and st["old"] in state: state.remove(st["old"])
    text = " ".join(D[v] for v in sv); toks = [(m.start(), m.end(), m.group()) for m in re.finditer(r"\S+", text)]; kept = set()
    for k in state:
        for m in re.finditer(M[k]["rx"], text):
            kept |= {i for i, (a, b, w) in enumerate(toks) if a < m.end() and b > m.start()}
    rows = {}
    for i, (a, b, w) in enumerate(toks):
        s = stem(w)
        if cand(s): rows[s] = max(rows.get(s, 0), 1 if i in kept else 0)
    tv = refs[refs.index(tv[0]):refs.index(tv[-1]) + 1]; DATA.append(dict(id=d["id"], seed=sv, target=tv, rows=rows, gospel=tv[0].split()[0]))
print("derivations used:", len(DATA), "| seed words:", sum(len(d["rows"]) for d in DATA), "| kept:", sum(sum(d["rows"].values()) for d in DATA))
def fit(ds, l2=1.0, it=3000):
    X = np.array([feats(s) for d in ds for s in d["rows"]]); y = np.array([v for d in ds for v in d["rows"].values()], dtype=float); mu, sd = X.mean(0), X.std(0) + 1e-9; Z = np.c_[np.ones(len(X)), (X - mu) / sd]; w = np.zeros(Z.shape[1])
    for _ in range(it):
        p = 1 / (1 + np.exp(-Z @ w)); g = Z.T @ (p - y) / len(y) + l2 * np.r_[0, w[1:]] / len(y); w -= 0.5 * g
    return w, mu, sd
def pk(model, s):
    w, mu, sd = model; return float(1 / (1 + math.exp(-(w[0] + ((np.array(feats(s)) - mu) / sd) @ w[1:]))))
GV = [r for r in refs if r.split()[0] in GOS]; GC = [collections.Counter(s for s in SS[r] if s) for r in GV]
def search(weights, L, exclude=None):
    """weights: stem -> weight. returns scores for every start"""
    sc = np.zeros(len(GV) - L + 1); 
    for s, wt in weights.items():
        pres = np.array([1.0 if c[s] else 0.0 for c in GC]); cnt = np.array([float(c[s]) for c in GC]); cs = np.r_[0, np.cumsum(cnt)]; tot = cs[L:] - cs[:-L]
        sc += wt * ((tot >= 1) + 0.25 * (tot >= 2))
    return sc
def rank(d, weights):
    L = len(d["target"]); sc = search(weights, L); i0 = GV.index(d["target"][0]); mine = sc[i0]; far = np.array([abs(i - i0) >= L for i in range(len(sc))]); return int(((sc > mine) & far).sum()) + 1, int(far.sum()) + 1
def weights_for(seedverses, model):
    st = {s for v in seedverses for s in SS[v] if cand(s)}; return {s: (pk(model, s) if model else 1.0) * idf(s) for s in st if dfG[s] > 0}
def test(name, train_of, test_set):
    R = []
    for d in test_set:
        m = fit(train_of(d)); r1, n = rank(d, weights_for(d["seed"], m)); r0, _ = rank(d, weights_for(d["seed"], None)); R.append((d["id"], d["gospel"], len(d["target"]), r0, r1, n))
    a0 = np.array([r[3] for r in R]); a1 = np.array([r[4] for r in R])
    print(f"\n== {name}: {len(R)} hidden derivations, each against some {R[0][5]} stretches\n   the declared target is first: no model {int((a0==1).sum())}, with the model {int((a1==1).sum())} | in the first ten: {int((a0<=10).sum())}, {int((a1<=10).sum())} | in the first hundred: {int((a0<=100).sum())}, {int((a1<=100).sum())} | median rank: {int(np.median(a0))}, {int(np.median(a1))} | model better {int((a1<a0).sum())}, worse {int((a1>a0).sum())}, same {int((a1==a0).sum())}")
    return R
OUT = {}
OUT["loo"] = test("TEST 1, each derivation hidden in turn", lambda d: [x for x in DATA if x["id"] != d["id"] and not set(x["seed"]) & set(d["seed"])], DATA)
mt = [d for d in DATA if d["gospel"] == "Matt"]; rest = [d for d in DATA if d["gospel"] != "Matt"]
OUT["matt_to_rest"] = test(f"TEST 2, learned from Matthew's {len(mt)} only", lambda d: [x for x in mt if not set(x["seed"]) & set(d["seed"])], rest)
for g in ("Mark", "Luke", "John"):
    rr = [r for r in OUT["matt_to_rest"] if r[1] == g]; print(f"   {g}: {len(rr)} | first {sum(r[4]==1 for r in rr)} | first ten {sum(r[4]<=10 for r in rr)} | median {int(np.median([r[4] for r in rr])) if rr else '-'} (no model {int(np.median([r[3] for r in rr])) if rr else '-'})")
M = fit(DATA); w, mu, sd = M; print("\n== THE KEEP-MODEL, learned from all (standardized weights; positive keeps, negative lets go):")
for n, x in sorted(zip(FN, w[1:]), key=lambda z: z[1]): print(f"   {x:+.2f}  {n}")
OUT["model"] = dict(zip(FN, map(float, w[1:]))); OUT["intercept"] = float(w[0])
print("   kept by the model most surely, of Revelation's words:", [s for s, _ in sorted(((s, pk(M, s)) for s in dfR if cand(s) and dfG[s] > 0), key=lambda z: -z[1])[:24]])
print("   let go most surely:", [s for s, _ in sorted(((s, pk(M, s)) for s in dfR if cand(s)), key=lambda z: z[1])[:24]])
print("\n== the hidden derivations, worst and best with the model (id, gospel, length, rank without, rank with)")
for r in sorted(OUT["loo"], key=lambda r: -r[4])[:10]: print("   ", r[:5])
used = {v for d in DATA for v in d["seed"]}; rv = [r for r in refs if r.startswith("Rev ")]; PRED = []
for i in range(len(rv) - 1):
    sv = rv[i:i + 2]
    if set(sv) & used: continue
    wt = weights_for(sv, M); tot = sum(wt.values())
    if tot <= 0: continue
    sc = search(wt, 3); j = int(sc.argmax()); win = GV[j:j + 3]; held = sorted((s for s in wt if any(s in c for c in GC[j:j + 3])), key=lambda s: -wt[s]); z = (sc[j] - sc.mean()) / (sc.std() + 1e-9)
    PRED.append(dict(seed=f"{sv[0]}–{sv[1].split(':')[1]}", found=f"{win[0]}–{win[-1].split(':')[1]}", share=round(float(sc[j] / tot), 2), z=round(float(z), 1), held=held[:9]))
PRED.sort(key=lambda p: -p["z"]); OUT["predictions"] = PRED[:60]; print(f"\n== PREDICT: {len(PRED)} unused pairs of verses of Revelation transformed. The strongest (z = how far the best stretch stands above all stretches for that seed):")
seen = set()
for p in PRED:
    if p["found"] in seen: continue
    seen.add(p["found"]); print(f"   z {p['z']:5}  share {p['share']:.2f}  {p['seed']:14} → {p['found']:16} {' '.join(p['held'])}")
    if len(seen) >= 26: break
json.dump(OUT, open(sys.argv[3], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
