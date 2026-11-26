#!/usr/bin/env python3
"""Census of shared word sequences between the Apocalypse and each other book of the New Testament, in the seated Greek (Nestle 1904, EA-CORPORA-01/04),
with the Septuagint (Swete, EA-CORPORA-01/05) and Philo (EA-CORPORA-01/07) as controls for an available common source.
A sequence is n consecutive words inside one verse, accents and case removed. A sequence made only of the 100 commonest words of the NT is dropped.
   python3 census.py <alexanarch root> <out.json>"""
import sys, re, json, unicodedata, pathlib, collections
ROOT = pathlib.Path(sys.argv[1]); C = ROOT / "data/corpora"
def norm(s):
    s = unicodedata.normalize("NFD", s); s = "".join(c for c in s if not unicodedata.combining(c)).lower().replace("ς", "σ")
    return re.findall(r"[α-ω]+", s)
def verses(p):
    for l in p.read_text(encoding="utf-8").splitlines():
        if "\t" in l:
            ref, t = l.split("\t", 1); yield ref, norm(t)
NT = {p.stem: list(verses(p)) for p in sorted((C / "gnt-nestle1904/text").glob("*.txt"))}
freq = collections.Counter(w for b in NT.values() for _, ws in b for w in ws); STOP = {w for w, _ in freq.most_common(100)}
def grams(ws, n): return [tuple(ws[i:i + n]) for i in range(len(ws) - n + 1)]
def keep(g): return any(w not in STOP for w in g) and sum(1 for w in g if w not in STOP) >= 2
def index(book_verses, n):
    ix = collections.defaultdict(list)
    for ref, ws in book_verses:
        for g in grams(ws, n):
            if keep(g): ix[g].append(ref)
    return ix
def flat(dirname):
    S = {3: set(), 4: set()}
    for p in (C / dirname / "text").glob("*.txt"):
        for l in p.read_text(encoding="utf-8", errors="ignore").splitlines():
            ws = norm(l.split("\t", 1)[-1])
            for n in (3, 4): S[n].update(grams(ws, n))
    return S
LXX = flat("lxx-swete"); PHILO = flat("philo")
out = {"instrument": __doc__, "books": {}, "tokens": {b: sum(len(ws) for _, ws in v) for b, v in NT.items()}}
IX = {n: {b: index(v, n) for b, v in NT.items()} for n in (3, 4)}
for b in NT:
    if b == "Rev": continue
    row = {}
    for n in (3, 4):
        sh = [g for g in IX[n][b] if g in IX[n]["Rev"]]
        items = []
        for g in sh:
            others = [o for o in NT if o not in ("Rev", b) and g in IX[n][o]]
            items.append({"seq": " ".join(g), "rev": sorted(set(IX[n]["Rev"][g]))[:6], "book": sorted(set(IX[n][b][g]))[:6], "lxx": g in LXX[n], "philo": g in PHILO[n], "other_nt": len(others)})
        row[str(n)] = {"shared": len(items), "not_in_lxx": sum(1 for i in items if not i["lxx"]), "pair_only_in_nt": sum(1 for i in items if i["other_nt"] == 0),
                       "pair_only_and_not_lxx": sum(1 for i in items if i["other_nt"] == 0 and not i["lxx"]),
                       "items": sorted([i for i in items if i["other_nt"] <= 2], key=lambda i: (i["lxx"], i["other_nt"]))}
    out["books"][b] = row
json.dump(out, open(sys.argv[2], "w"), ensure_ascii=False, indent=1)
print(f"{'book':8}{'tokens':>7}{'3g':>6}{'¬LXX':>6}{'pair':>6}{'pair¬LXX':>9}{'per10k':>8}{'4g':>5}{'4g pair¬LXX':>12}")
for b, r in sorted(out["books"].items(), key=lambda kv: -kv[1]["3"]["pair_only_and_not_lxx"] / out["tokens"][kv[0]]):
    t = out["tokens"][b]; a = r["3"]; print(f"{b:8}{t:>7}{a['shared']:>6}{a['not_in_lxx']:>6}{a['pair_only_in_nt']:>6}{a['pair_only_and_not_lxx']:>9}{10000 * a['pair_only_and_not_lxx'] / t:>8.1f}{r['4']['shared']:>5}{r['4']['pair_only_and_not_lxx']:>12}")
