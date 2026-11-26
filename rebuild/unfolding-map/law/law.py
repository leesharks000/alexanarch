#!/usr/bin/env python3
"""A profile of how each Gospel stands to the Apocalypse, from every verse-to-verse link in the seated Greek, with nothing chosen by hand.
A link is a verse of Revelation and a verse of a Gospel sharing two or more rare stems (first five letters; rare = in at most 60 verses of the New Testament).
Each link is described by what can be computed from the two verses: which part of Revelation the seed is in; whether the Septuagint has the same stems in one verse;
whether the shared words keep their exact form, their order, their adjacency; whether a first person in the seed is still a first person in the Gospel; whether the
seed's negation is gone or a negation has come; whether the Gospel marks the words as written; whether the same seed verse also links to another Gospel by other words.
   python3 law.py <alexanarch root> <out.json>"""
import sys, re, json, math, unicodedata, pathlib, collections
ROOT = pathlib.Path(sys.argv[1]); C = ROOT / "data/corpora"
def words(s):
    s = unicodedata.normalize("NFD", s); s = "".join(c for c in s if not unicodedata.combining(c)).lower().replace("ς", "σ"); return re.findall(r"[α-ω]+", s)
def load(p):
    out = []
    for l in p.read_text(encoding="utf-8", errors="ignore").splitlines():
        if "\t" in l:
            ref, t = l.split("\t", 1); w = words(t); out.append((ref.strip(), w, t.strip()))
    return out
NT = {p.stem: load(p) for p in sorted((C / "gnt-nestle1904/text").glob("*.txt"))}
stem = lambda w: w[:5]
N = sum(len(v) for v in NT.values()); df = collections.Counter(s for b in NT.values() for _, w, _ in b for s in {stem(x) for x in w if len(x) >= 4})
rare = {s for s, c in df.items() if c <= 60}; wt = lambda s: math.log(N / df[s])
LX = collections.defaultdict(set); i = 0
for p in (C / "lxx-swete/text").glob("*.txt"):
    for ref, w, _ in load(p):
        if not re.search(r"\d+:\d+$", ref): continue
        i += 1
        for s in {stem(x) for x in w if len(x) >= 4} & rare: LX[s].add(i)
def lxx(sh):
    sets = [LX[s] for s in sh]; return all(sets) and bool(set.intersection(*sorted(sets, key=len)))
REGIONS = [("1 the vision", 1, 1), ("2–3 the letters", 2, 3), ("4–5 the throne and the Lamb", 4, 5), ("6–7 the seals", 6, 7), ("8–11 the trumpets", 8, 11), ("12–14 the woman, the beasts", 12, 14),
           ("15–16 the plagues", 15, 16), ("17–18 Babylon", 17, 18), ("19–20 the rider, the judgment", 19, 20), ("21–22 the city", 21, 22)]
def region(ref):
    c = int(ref.split()[1].split(":")[0]); return next(n for n, a, b in REGIONS if a <= c <= b)
FIRST = re.compile(r"^(εγω|μου|εμου|μοι|εμοι|εμε|ειμι|οιδα|ερχομαι|ηξω|δωσω|ποιησω|γραψω|ομολογησω|βαλω|\w+σω|\w+ξω|\w+ψω)$")
NEG = lambda w: any(x in ("ου", "ουκ", "ουχ", "μη", "ουδεισ", "ουδε", "ουκετι", "μηκετι", "ουδεν") for x in w)
CITE = re.compile(r"γεγραπται|γεγραμμεν|γραφη|ερρεθη|ρηθεν|πληρωθη|ησαια|προφητ")
G = ("Matt", "Mark", "Luke", "John"); inv = collections.defaultdict(list)
for g in G:
    for ref, w, t in NT[g]:
        for s in {stem(x) for x in w if len(x) >= 4} & rare: inv[s].append((g, ref))
VERSE = {g: {ref: (w, t) for ref, w, t in NT[g]} for g in G}
links = []
for ref, w, t in NT["Rev"]:
    ss = {stem(x) for x in w if len(x) >= 4} & rare; cand = collections.defaultdict(set)
    for s in ss:
        for g, r2 in inv[s]: cand[(g, r2)].add(s)
    for (g, r2), sh in cand.items():
        if len(sh) < 2: continue
        w2, t2 = VERSE[g][r2]; f1 = {stem(x): set() for x in w}; f2 = {stem(x): set() for x in w2}
        for x in w: f1[stem(x)].add(x)
        for x in w2: f2[stem(x)].add(x)
        p1 = sorted(sh, key=lambda s: next(i for i, x in enumerate(w) if stem(x) == s)); p2 = sorted(sh, key=lambda s: next(i for i, x in enumerate(w2) if stem(x) == s))
        i1 = [next(i for i, x in enumerate(w) if stem(x) == s) for s in p1]; i2 = [next(i for i, x in enumerate(w2) if stem(x) == s) for s in p2]
        links.append({"rev": ref, "gospel": g, "ref": r2, "stems": sorted(sh), "weight": round(sum(wt(s) for s in sh), 2), "lxx": lxx(sh), "region": region(ref),
                      "form_kept": round(sum(1 for s in sh if f1[s] & f2[s]) / len(sh), 2), "order_kept": p1 == p2, "span_seed": i1[-1] - i1[0], "span_target": i2[-1] - i2[0],
                      "first_seed": any(FIRST.match(x) for x in w), "first_target": any(FIRST.match(x) for x in w2), "neg_seed": NEG(w), "neg_target": NEG(w2), "cite_target": bool(CITE.search(" ".join(w2))),
                      "rev_text": t, "text": t2})
byrev = collections.defaultdict(list)
for l in links: byrev[l["rev"]].append(l)
for l in links:
    others = [o for o in byrev[l["rev"]] if o["gospel"] != l["gospel"]]
    l["same_words_in_other_gospel"] = sorted({o["gospel"] for o in others if set(o["stems"]) & set(l["stems"]) and len(set(o["stems"]) & set(l["stems"])) >= 2})
    l["other_words_in_other_gospel"] = sorted({o["gospel"] for o in others if set(o["stems"]) - set(l["stems"])})
    l["only_this_gospel"] = not l["same_words_in_other_gospel"]
revn = collections.Counter(region(r) for r, _, _ in NT["Rev"])
def profile(L, g):
    n = len(L) or 1; pc = lambda f: round(100 * sum(1 for l in L if f(l)) / n)
    reg = collections.Counter(l["region"] for l in L)
    return {"links": len(L), "per_100_verses": round(100 * len(L) / len(NT[g]), 1), "septuagint_available_%": pc(lambda l: l["lxx"]), "only_this_gospel_%": pc(lambda l: l["only_this_gospel"]),
            "exact_form_kept_mean": round(sum(l["form_kept"] for l in L) / n, 2), "order_kept_%": pc(lambda l: l["order_kept"]),
            "tighter_in_gospel_%": pc(lambda l: l["span_target"] < l["span_seed"]), "looser_in_gospel_%": pc(lambda l: l["span_target"] > l["span_seed"]),
            "first_person_seed_%": pc(lambda l: l["first_seed"]), "first_person_kept_%": round(100 * sum(1 for l in L if l["first_seed"] and l["first_target"]) / (sum(1 for l in L if l["first_seed"]) or 1)),
            "negation_removed_%": pc(lambda l: l["neg_seed"] and not l["neg_target"]), "negation_added_%": pc(lambda l: l["neg_target"] and not l["neg_seed"]), "marked_as_written_%": pc(lambda l: l["cite_target"]),
            "seed_also_split_with_another_gospel_%": pc(lambda l: l["other_words_in_other_gospel"]),
            "regions_links_per_100_seed_verses": {r: round(100 * reg[r] / revn[r], 1) for r, _, _ in REGIONS}}
out = {"instrument": __doc__, "all": {g: profile([l for l in links if l["gospel"] == g], g) for g in G},
       "septuagint_not_available": {g: profile([l for l in links if l["gospel"] == g and not l["lxx"]], g) for g in G},
       "only_this_gospel_and_septuagint_not_available": {g: profile([l for l in links if l["gospel"] == g and not l["lxx"] and l["only_this_gospel"]], g) for g in G}, "links": sorted(links, key=lambda l: -l["weight"])}
json.dump(out, open(sys.argv[2], "w"), ensure_ascii=False, indent=1)
for name in ("all", "septuagint_not_available", "only_this_gospel_and_septuagint_not_available"):
    print("==", name); keys = [k for k in out[name]["Matt"] if k != "regions_links_per_100_seed_verses"]
    print(f"{'':42}" + "".join(f"{g:>7}" for g in G))
    for k in keys: print(f"{k:42}" + "".join(f"{out[name][g][k]:>7}" for g in G))
    for r, _, _ in REGIONS: print(f"  {r:40}" + "".join(f"{out[name][g]['regions_links_per_100_seed_verses'][r]:>7}" for g in G))
