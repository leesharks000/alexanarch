#!/usr/bin/env python3
"""Three runs. (1) The backward lean of Matthew 24 (2M.3) tested where it was not read: Rev 20:11-15 against Matt 25:31-46, patterns frozen first.
(2) Order by machine: every chapter of Revelation against every chapter of each Gospel; the word-stems they share that are rare in the New Testament, each
placed at its first word in each chapter; Kendall's tau; its z. If order is kept or turned anywhere, the z's will not be centred or will be too wide.
(3) The four cross-and-tomb narratives against Revelation by machine: every rare stem of the stretch a member, no hand; where they stand in Revelation
(13 verses); and the same for 300 other stretches of the same Gospel, as the control. Then each Gospel's own stems (not in Mark's stretch).
   python3 proceed.py <alexanarch root> <engine dir> out.json"""
import sys, re, json, pathlib, collections, random, itertools, math
sys.path.insert(0, sys.argv[2]); import midrash as E
from members20 import M20
root = pathlib.Path(sys.argv[1]) / "data/corpora/gnt-nestle1904/text"
def sq(s): return re.sub(r"\s+", " ", E.norm(s)).strip()
def book(b): return [(l.split("\t", 1)[0].strip(), sq(l.split("\t", 1)[1])) for l in (root / f"{b}.txt").read_text(encoding="utf-8").splitlines() if "\t" in l]
BOOKS = {p.stem: book(p.stem) for p in sorted(root.glob("*.txt"))}; GOS = ["Matt", "Mark", "Luke", "John"]; rev = BOOKS["Rev"]
def tau(xs, ys):
    c = d = 0
    for (a, b), (e, f) in itertools.combinations(list(zip(xs, ys)), 2):
        s = (a - e) * (b - f); c += s > 0; d += s < 0
    return ((c - d) / (c + d) if c + d else 0.0), c, d
OUT = {}
# (1)
seg = [(r, t) for r, t in BOOKS["Matt"] if re.match(r"Matt 25:(3[1-9]|4[0-6])$", r)]; res = {}
for loose in (False, True):
    pts = []
    for k, (v, mid, gloss, rx, rx2) in enumerate(M20):
        assert re.search(rx, dict(rev)["Rev " + v]), (v, mid)
        cs = [(re.compile(rx), "")] + ([(re.compile(rx2), "*")] if loose and rx2 else [])
        hit = next(((p, r, mk) for p, (r, t) in enumerate(seg) for c, mk in cs if c.search(t)), None)
        if hit: pts.append((k, hit[0], v, mid + hit[2], hit[1].split()[1]))
    o = dict(n=len(pts), pts=pts)
    if len(pts) >= 4:
        t, c, d = tau([p[0] for p in pts], [p[1] for p in pts]); random.seed(1126); ys = [p[1] for p in pts]; N = 20000
        ex = sum(1 for _ in range(N) if abs(tau([p[0] for p in pts], random.sample(ys, len(ys)))[0]) >= abs(t) - 1e-12); o.update(tau=round(t, 3), concordant=c, discordant=d, p=ex / N)
    res["loose" if loose else "own"] = o
    print(f"(1) Rev 20:11-15 against Matt 25:31-46 | {'own and loosened' if loose else 'own'} | placed {o['n']}" + (f" | tau {o['tau']:+.3f} ({o['concordant']} with, {o['discordant']} against) p={o['p']:.3f}" if 'tau' in o else " | too few to test"), [(p[2], p[3], p[4]) for p in pts])
OUT["frozen"] = res
# (2)
def stems(t): return [w[:5] for w in t.split() if len(w) >= 5]
df = collections.Counter(s for b, vs in BOOKS.items() for _, t in vs for s in set(stems(t)))
def chapters(b):
    ch = collections.OrderedDict()
    for r, t in BOOKS[b]: ch.setdefault(int(r.split()[-1].split(":")[0]), []).extend(stems(t))
    return ch
def first(ws):
    f = {}
    for i, w in enumerate(ws): f.setdefault(w, i)
    return f
RC = {c: first(ws) for c, ws in chapters("Rev").items()}; Z = []
for g in GOS:
    for gc, ws in chapters(g).items():
        fg = first(ws)
        for rc, fr in RC.items():
            sh = [s for s in fr if s in fg and df[s] <= 40]
            if len(sh) < 8: continue
            n = len(sh); t, c, d = tau([fr[s] for s in sh], [fg[s] for s in sh]); z = t / math.sqrt(2 * (2 * n + 5) / (9 * n * (n - 1))); Z.append((z, t, n, f"Rev {rc}", f"{g} {gc}"))
zs = [z for z, *_ in Z]; m = sum(zs) / len(zs); sd = math.sqrt(sum((z - m) ** 2 for z in zs) / len(zs)); out2 = dict(pairs=len(Z), mean_z=round(m, 3), sd_z=round(sd, 3), beyond_1_96=sum(1 for z in zs if abs(z) > 1.96), expected=round(0.05 * len(zs), 1),
            most_kept=sorted(Z, reverse=True)[:6], most_turned=sorted(Z)[:6], rev11_12_matt24=[x for x in Z if x[3] in ("Rev 11", "Rev 12") and x[4] == "Matt 24"], rev11_cross=[x for x in Z if x[3] == "Rev 11" and x[4] in ("Matt 27", "Mark 15", "Luke 23", "John 19")])
print(f"\n(2) chapter pairs with 8 or more shared rare stems: {len(Z)} | z of tau: mean {m:+.3f}, sd {sd:.3f} (0 and 1 if no order anywhere) | beyond 1.96: {out2['beyond_1_96']} (expected {out2['expected']})")
print("   most kept:", [(f"{a[3]}/{a[4]}", round(a[1], 2), a[2], round(a[0], 2)) for a in out2["most_kept"]]); print("   most turned:", [(f"{a[3]}/{a[4]}", round(a[1], 2), a[2], round(a[0], 2)) for a in out2["most_turned"]])
print("   Rev 11, 12 / Matt 24:", [(a[3], round(a[1], 2), a[2], round(a[0], 2)) for a in out2["rev11_12_matt24"]], "| Rev 11 / the cross chapters:", [(a[4], round(a[1], 2), a[2], round(a[0], 2)) for a in out2["rev11_cross"]])
OUT["order_census"] = out2
# (3)
PASSION = {"Matt": ("Matt 27:32", "Matt 28:10"), "Mark": ("Mark 15:21", "Mark 16:8"), "Luke": ("Luke 23:26", "Luke 24:12"), "John": ("John 19:16", "John 20:18")}
rdf = collections.Counter(s for _, t in rev for s in set(stems(t))); rvst = [set(stems(t)) for _, t in rev]; i11 = [r for r, _ in rev].index("Rev 11:1")
def stretch(g, i, L): return set().union(*(set(stems(t)) for _, t in BOOKS[g][i:i + L]))
def usable(S): return {s for s in S if df[s] <= 60 and 0 < rdf[s] <= 12}
def wins(S):
    sc = [len(S & set().union(*rvst[i:i + 13])) for i in range(len(rev) - 12)]; return sc
out3 = {}; own = {}
for g in GOS:
    refs = [r for r, _ in BOOKS[g]]; a, z = refs.index(PASSION[g][0]), refs.index(PASSION[g][1]); L = z - a + 1; S_all = {s for s in stretch(g, a, L) if df[s] <= 60}; S = usable(S_all); sc = wins(S); w = sc[i11]; best = max(sc); bi = sc.index(best)
    random.seed(1126); ctrl = []
    for _ in range(300):
        i = random.randrange(0, len(refs) - L)
        if abs(i - a) < L: continue
        Sc = usable(stretch(g, i, L)); ctrl.append((len(Sc & set().union(*rvst[i11:i11 + 13])), len(Sc)))
    frac = w / max(1, len(S)); cf = sorted(c / max(1, n) for c, n in ctrl); pct = sum(1 for x in cf if x >= frac) / len(cf)
    out3[g] = dict(verses=L, rare_stems=len(S_all), in_revelation=len(S), at_11=w, members=sorted(S & set().union(*rvst[i11:i11 + 13])), best=best, best_at=rev[bi][0], windows_ge=sum(1 for x in sc if x >= w), n_windows=len(sc), control_mean=round(sum(c for c, _ in ctrl) / len(ctrl), 2), control_share_ge=round(pct, 3))
    own[g] = stretch(g, a, L)
    print(f"\n(3) {g} cross and tomb, {L} verses: rare stems {len(S_all)}, of them in Revelation {len(S)} | 11:1-13 holds {w} {out3[g]['members']} | best window {best} at {rev[bi][0]} | windows with as many as 11:1-13: {out3[g]['windows_ge']} of {len(sc)} | other stretches of {g}: mean at 11:1-13 {out3[g]['control_mean']}; share of them with as large a fraction there: {pct:.3f}")
for g in ("Matt", "Luke", "John"):
    S = usable(own[g] - own["Mark"]); sc = wins(S); best = max(sc); tops = sorted(((x, rev[i][0]) for i, x in enumerate(sc)), reverse=True); pick, used = [], []
    for x, r in tops:
        i = [q for q, _ in rev].index(r)
        if all(abs(i - j) >= 13 for j in used): used.append(i); pick.append((x, r, sorted(S & set().union(*rvst[i:i + 13]))))
        if len(pick) == 4: break
    out3[g + ":own"] = dict(stems=len(S), at_11=sc[i11], top=pick); print(f"\n    {g}'s stems not in Mark's cross and tomb, in Revelation: {len(S)} | 11:1-13 holds {sc[i11]} | top windows:", pick)
OUT["passions"] = out3
json.dump(OUT, open(sys.argv[3], "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=list)
