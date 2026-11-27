#!/usr/bin/env python3
"""2AD, second part: quotation-like links for every source of phr.py, and the proper names each source shares with the Gospels.
   python3 phr2.py <alexanarch root> <engine dir> phr2.json"""
import sys, re, json, math, pathlib, collections, itertools, unicodedata
src = open(pathlib.Path(__file__).with_name("phr.py")).read().split('OUT = {}; print(f"')[0].split('"""', 2)[2]
exec(src)
# proper names: words the Nestle seat prints with a capital in at least four-fifths of their occurrences, at least twice, not verse-initial only
cap = collections.Counter(); low = collections.Counter(); gosp = collections.Counter()
def nrm(w): return E.norm(w).strip()
for p in sorted((root / "gnt-nestle1904" / "text").glob("*.txt")):
    for l in p.read_text(encoding="utf-8").splitlines():
        if "\t" not in l: continue
        r, t = l.split("\t", 1); toks = re.findall(r"[^\s.,;·:()\[\]«»“”\"']+", t)
        for i, w in enumerate(toks):
            n = nrm(w)
            if not re.fullmatch(r"[α-ω]+", n) or len(n) < 4: continue
            first = unicodedata.normalize("NFD", w)[0]
            if first.isupper() and i > 0: cap[stem(n)] += 1
            elif not first.isupper(): low[stem(n)] += 1
            if first.isupper() and i > 0 and r.split()[0] in GOS: gosp[stem(n)] += 1
NAMES = {s for s, c in cap.items() if s and c >= 2 and c / (c + low[s]) >= 0.8}
GN = {s for s in NAMES if gosp[s] >= 2}; print("name stems:", len(NAMES), "of which in the Gospels twice or more:", len(GN))
lxxst = collections.Counter(s for k, w in RAW if k[0] == "L" for s in set(ST[k][0]) if s)
OUT = {}; print(f"\n{'source':40}{'words':>8}{'quotation-like links (4+ stems)':>33}{'/1000w':>8}{'Gospel names, distinct':>24}{'/1000w':>8}{'of them not in LXX':>20}{'name tokens /1000w':>20}")
for name, keys in G.items():
    if not keys: continue
    n = max(1, len(keys) // 10); secs = [keys[i * n:(i + 1) * n] for i in range(10)]; links = {}; nw = sum(len(ST[k][1]) for sec in secs for k in sec)
    for sec in secs:
        own = set(sec)
        for k in sec:
            for p in itertools.combinations(sorted(set(s for s in ST[k][0] if s in ok)), 2):
                if p in GP and not ((IX[p[0]] & IX[p[1]]) - own):
                    for g in GP[p]: links.setdefault((k, g), set()).update(p)
    q = sum(1 for v in links.values() if len(v) >= 4); nm = collections.Counter(s for sec in secs for k in sec for s in ST[k][0] if s in GN); new = [s for s in nm if lxxst[s] == 0]
    OUT[name] = dict(words=nw, quot=q, quot1000=round(1000 * q / nw, 2), names=len(nm), names1000=round(1000 * len(nm) / nw, 2), names_not_lxx=sorted(new), tokens1000=round(1000 * sum(nm.values()) / nw, 1), top=nm.most_common(25))
    print(f"{name:40}{nw:>8}{q:>33}{OUT[name]['quot1000']:>8}{len(nm):>24}{OUT[name]['names1000']:>8}{len(new):>20}{OUT[name]['tokens1000']:>20}")
for name in ("Revelation", "Acts", "later apocalypses, Tischendorf (OCR)", "Josephus, Life", "Testaments of the Twelve (OCR)", "Hebrews, James, 1 Peter"):
    print(f"\n== {name}: Gospel names it has that the Septuagint has not: {OUT[name]['names_not_lxx'][:40]}\n   its commonest Gospel names: {[a for a, _ in OUT[name]['top']]}")
json.dump(OUT, open(sys.argv[3], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
