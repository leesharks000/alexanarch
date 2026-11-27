#!/usr/bin/env python3
"""2Z.2's count at other settings, by Gospel, and Revelation's links listed whole (section 3A).
  setting = (ceiling: a stem counts if in at most so many verses of the New Testament; window: verses a pairing may span; prefix: letters of the stem kept)
   python3 excl2.py <alexanarch root> <engine dir> excl2.json links.tsv"""
import sys, re, json, math, pathlib, collections, itertools
sys.path.insert(0, sys.argv[2]); import midrash as E
root = pathlib.Path(sys.argv[1]) / "data/corpora"
END = sorted("ουσιν ομεθα εσθαι ησαν ουσα ουσι ομεν ετε ουσ οισ αισ ασι ων ου οσ ον οι ην ησ ασ αι εσ ει εν α η ω ε ι ν σ".split(), key=len, reverse=True)
def mkstem(n):
    def stem(w):
        if len(w) < 4: return None
        for e in END:
            if w.endswith(e) and len(w) - len(e) >= 3: w = w[:-len(e)]; break
        return w[:n]
    return stem
def load(c):
    o = []
    for p in sorted((root / c / "text").glob("*.txt")):
        seen = set()
        for l in p.read_text(encoding="utf-8", errors="ignore").splitlines():
            if "\t" in l:
                r, t = l.split("\t", 1); r = r.strip()
                if re.search(r"\d+:\d+$", r) and r not in seen: seen.add(r); o.append((p.stem, r, re.sub(r"\s+", " ", E.norm(t)).strip().split()))
    return o
NTl, LXl = load("gnt-nestle1904"), load("lxx-swete"); GOS = ("Matt", "Mark", "Luke", "John")
def book(k): return k[1].split()[0] if k[0] == "N" else k[1].split("|")[0]
RAW = [(("N", r), w) for _, r, w in NTl] + [(("L", b + "|" + r), w) for b, r, w in LXl]
def groups():
    g = collections.OrderedDict()
    def nt(*pre): return [k for k, _ in RAW if k[0] == "N" and k[1].startswith(pre)]
    def lx(*names): return [k for k, _ in RAW if k[0] == "L" and any(n in k[1] for n in names)]
    g["Revelation"] = nt("Rev "); g["Acts"] = nt("Acts "); g["Isaiah"] = lx("Ἠσαΐας"); g["Judith, Tobit"] = lx("Ἰουδίθ", "Τωβίτ"); g["Jeremiah"] = lx("Ἱερεμίας"); g["Daniel (Theodotion)"] = lx("Theodotionis")
    g["Hebrews, James, 1 Peter"] = nt("Heb ", "Jas ", "1Pet "); g["Romans, 1 Corinthians"] = nt("Rom ", "1Cor "); return g
SECJ = [("Rev 1:1", "Rev 1:20"), ("Rev 2:1", "Rev 3:22"), ("Rev 4:1", "Rev 5:14"), ("Rev 6:1", "Rev 8:1"), ("Rev 8:2", "Rev 11:19"), ("Rev 12:1", "Rev 14:20"), ("Rev 15:1", "Rev 16:21"), ("Rev 17:1", "Rev 19:10"), ("Rev 19:11", "Rev 20:15"), ("Rev 21:1", "Rev 22:21")]
def setting(ceil, win, pre, want_links=False):
    stem = mkstem(pre); ST = [(k, set(filter(None, map(stem, w)))) for k, w in RAW]; df = collections.Counter(s for k, ss in ST if k[0] == "N" for s in ss); ok = {s for s, c in df.items() if c <= ceil}
    U = []
    for i, (k, ss) in enumerate(ST):
        u = set(ss)
        for j in range(1, win):
            if i + j < len(ST) and book(ST[i + j][0]) == book(k): u |= ST[i + j][1]
        U.append((k, sorted(u & ok)))
    UD = dict(U); isg = lambda k: k[0] == "N" and k[1].split()[0] in GOS; IX = collections.defaultdict(set); GP = collections.defaultdict(list)
    for k, ss in U:
        if isg(k):
            for p in itertools.combinations(ss, 2): GP[p].append(k)
        else:
            for s in ss: IX[s].add(k)
    res = {}; G = groups(); keep = None
    for name, keys in G.items():
        if name == "Revelation": secs = [keys[keys.index(("N", a)):keys.index(("N", b)) + 1] for a, b in SECJ]
        else: n = len(keys) // 10; secs = [keys[i * n:(i + 1) * n] for i in range(10)]
        links = {}; nv = 0
        for sec in secs:
            own = set(sec); nv += len(sec); idx = {k: i for i, (k, _) in enumerate(U)}
            if win > 1 and sec: own |= {U[idx[sec[0]] - 1][0]}
            for k in sec:
                for p in itertools.combinations(UD[k], 2):
                    if p in GP and not ((IX[p[0]] & IX[p[1]]) - own):
                        for g in GP[p]: links.setdefault((k, g), []).append(p)
        byg = collections.Counter(g[1].split()[0] for _, g in links); res[name] = dict(verses=nv, links=len(links), per100=round(100 * len(links) / nv, 1), with_any=round(100 * len({s for s, _ in links}) / nv), by_gospel=dict(byg))
        if name == "Revelation" and want_links: keep = (links, GP)
    return res, keep
OUT = {}
print("links per hundred source verses, by setting (ceiling, window, prefix)\n")
S = [(120, 1, 5), (60, 1, 5), (250, 1, 5), (120, 2, 5), (120, 1, 4), (120, 1, 6)]; R = {}
for s in S: R[s], kp = setting(*s, want_links=(s == S[0])); KEEP = kp if s == S[0] else KEEP
names = list(R[S[0]])
print(f"{'source':26}" + "".join(f"{str(s):>14}" for s in S))
for n in names: print(f"{n:26}" + "".join(f"{R[s][n]['per100']:>14}" for s in S))
print("\nplace of Revelation among the eight:", [sorted(names, key=lambda n: -R[s][n]['per100']).index("Revelation") + 1 for s in S])
OUT["settings"] = {str(s): R[s] for s in S}
NG = collections.Counter(r.split()[0] for _, r, _ in NTl if r.split()[0] in GOS)
print("\nbaseline, links by Gospel, per hundred verses of that Gospel")
for n in names: print(f"  {n:26}" + "  ".join(f"{g} {R[S[0]][n]['by_gospel'].get(g,0):3} ({100*R[S[0]][n]['by_gospel'].get(g,0)/NG[g]:.1f})" for g in GOS))
links, GP = KEEP
# tradition class of each link's pairing: in which Gospels does the pairing stand at all
def cls(ps):
    gs = set(g[1].split()[0] for p in ps for g in GP[p]); gs3 = gs - {"John"}
    return "John" if gs == {"John"} else "Matthew alone" if gs == {"Matt"} else "Luke alone" if gs == {"Luke"} else "Mark alone" if gs == {"Mark"} else "Matthew and Luke" if gs == {"Matt", "Luke"} else "with Mark" if "Mark" in gs3 and "John" not in gs else "John and a synoptic"
cc = collections.Counter(cls(ps) for ps in links.values()); print("\nRevelation's links by where the pairing stands in the Gospels:", dict(cc)); OUT["rev_class"] = dict(cc)
D = json.load(open(pathlib.Path(sys.argv[2]) / "derivations.json"))["derivations"]
def vs(loc):
    out = set()
    for part in loc.split(":", 1)[1].split(" + "):
        m = re.match(r"(\S+) (\d+):(\d+)(?:-(\d+))?$", part.strip())
        if m: out |= {f"{m[1]} {m[2]}:{i}" for i in range(int(m[3]), int(m[4] or m[3]) + 1)}
    return out
DV = [(d["id"], vs(d["seed"]), vs(d["target"])) for d in D if d["seed"].startswith("gnt:Rev")]
def infile(rk, gk): return next((i for i, a, b in DV if rk in a and gk in b), "")
rows = sorted(((k[1], g[1], " ".join(sorted({a + "+" + b for a, b in ps}))[:60], cls(ps), infile(k[1], g[1])) for (k, g), ps in links.items()), key=lambda x: (int(x[0].split()[1].split(":")[0]), int(x[0].split(":")[1]), x[1]))
open(sys.argv[4], "w", encoding="utf-8").write("\n".join("\t".join(r) for r in rows)); print(f"\nlinks listed: {len(rows)}; in a derivation already in the engine (seed verse and target verse): {sum(1 for r in rows if r[4])}\n")
for r in rows: print(f"{r[0]:10} {r[1]:11} {r[2]:44} {r[3][:8]:8} {'E' if r[4] else ''}")
json.dump(OUT, open(sys.argv[3], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
