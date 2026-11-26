#!/usr/bin/env python3
"""The passion read the other way: every member of Mark 15:21-16:8 searched in Revelation and in the Septuagint. Where in Revelation do Mark's members stand
together (a window of 13 verses, the length of 11:1-13)? Where in the Septuagint (40 verses)? The residue is counted from Mark's end.
   python3 other_way.py <alexanarch root> <engine dir> out.json"""
import sys, re, json, pathlib, collections
sys.path.insert(0, sys.argv[2]); import midrash as E
from mark_members import K
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
NT, LXX = load("gnt-nestle1904"), load("lxx-swete"); mark = dict(NT["Mark"]); rev = NT["Rev"]
rows, bad = [], []
for v, mid, gloss, rx, rx2 in K:
    if not re.search(rx, mark["Mark " + v]): bad.append((v, mid))
    def f(x):
        if not x: return None
        c = re.compile(x); return dict(rev=[r for r, t in rev if c.search(t)], lxx=[r for b, vs in LXX.items() for r, t in vs if c.search(t)])
    rows.append(dict(verse=v, id=mid, gloss=gloss, rx=rx, rx2=rx2, own=f(rx), loose=f(rx2)))
print("members of Mark 15:21-16:8:", len(rows), "| not found in own verse:", bad or "none")
def cls(r):
    a, b = bool(r["own"]["rev"]), bool(r["own"]["lxx"]); return "Revelation and Septuagint" if a and b else "Revelation, not the Septuagint" if a else "Septuagint, not Revelation" if b else "neither"
for r in rows: r["class"] = cls(r)
print(dict(collections.Counter(r["class"] for r in rows)))
in11 = lambda refs: [x for x in refs if re.match(r"Rev 11:([1-9]|1[0-3])$", x)]
print("in Revelation by own form:", [(r["id"], len(r["own"]["rev"]), [x.split()[1] for x in in11(r["own"]["rev"])]) for r in rows if r["own"]["rev"]])
print("in Revelation by loosened form only:", [(r["id"], [x.split()[1] for x in r["loose"]["rev"]][:6]) for r in rows if r["loose"] and r["loose"]["rev"] and not r["own"]["rev"]])
def land(corpus, L, loose, cap, top=8):
    mem = []
    for r in rows:
        c = [re.compile(r["rx"])] + ([re.compile(r["rx2"])] if loose and r["rx2"] else [])
        h = {(b, i) for b, vs in corpus.items() for i, (_, t) in enumerate(vs) if any(x.search(t) for x in c)}
        if h and len(h) <= cap: mem.append((r["id"], h))
    sc = []
    for b, vs in corpus.items():
        for i in range(0, max(1, len(vs) - L + 1)):
            got = sorted(m for m, h in mem if any((b, j) in h for j in range(i, min(len(vs), i + L))))
            sc.append((len(got), b, i, got))
    allsc = sorted(sc, key=lambda x: -x[0]); out, used = [], []
    for n, b, i, got in allsc:
        if n and all(not (b == ub and abs(i - ui) < L) for ub, ui in used):
            used.append((b, i)); vs = corpus[b]; out.append(dict(n=n, start=vs[i][0], end=vs[min(len(vs), i + L) - 1][0], members=got))
        if len(out) == top: break
    return dict(usable=len(mem), top=out, all=sc)
OUT = {}
for loose in (False, True):
    a = land({"Rev": rev}, 13, loose, 12); i0 = [r for r, _ in rev].index("Rev 11:1"); w = [x for x in a["all"] if x[2] == i0][0]
    ge = sum(1 for x in a["all"] if x[0] >= w[0]); print(f"\n== {'own and loosened' if loose else 'own'} forms | Revelation, 13 verses (usable {a['usable']}) | 11:1-13 holds {w[0]} {w[3]} | windows with as many: {ge} of {len(a['all'])}")
    for x in a["top"]: print(f"   {x['n']:2} {x['start']} – {x['end'].split()[-1]}  {x['members']}")
    b = land(LXX, 40, loose, 60); print(f"   Septuagint, 40 verses (usable {b['usable']})")
    for x in b["top"]: print(f"   {x['n']:2} {x['start']} – {x['end'].split()[-1]}  {x['members']}")
    c = land({"Rev": rev}, 40, loose, 12, top=4); print("   Revelation, 40 verses, for comparison with the Septuagint:", [(x["n"], x["start"], x["end"].split()[-1]) for x in c["top"]])
    OUT["loose" if loose else "own"] = dict(rev13=dict(usable=a["usable"], w11=w[0], w11_members=w[3], ge=ge, n=len(a["all"]), top=a["top"]), lxx40=dict(usable=b["usable"], top=b["top"]), rev40=c["top"])
json.dump(dict(rows=rows, landing=OUT, bad=bad), open(sys.argv[3], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
