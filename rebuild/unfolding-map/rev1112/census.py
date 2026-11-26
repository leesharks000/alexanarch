#!/usr/bin/env python3
"""Revelation 11-12 as one object. (1) Every member is checked in its own verse. (2) Each is searched, by its own form and apart by its loosened form, through the
Septuagint, the four Gospels (cross and tomb apart from the rest), Acts, the letters, and the rest of Revelation. (3) Each member is sorted by where it is found.
(4) For each Gospel and each section, a window is slid along the Gospel and the distinct members falling in it are counted: where does the section land?
   python3 census.py <alexanarch root> <engine dir> <out.json>"""
import sys, re, json, pathlib, collections
sys.path.insert(0, sys.argv[2]); import midrash as E
from members import M
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
GOS = ["Matt", "Mark", "Luke", "John"]
PASSION = {"Matt": ("Matt 27:32", "Matt 28:10"), "Mark": ("Mark 15:21", "Mark 16:8"), "Luke": ("Luke 23:26", "Luke 24:12"), "John": ("John 19:16", "John 20:18")}
def rng(book, a, b):
    refs = [r for r, _ in NT[book]]; return set(refs[refs.index(a): refs.index(b) + 1])
PR = {g: rng(g, *PASSION[g]) for g in GOS}
rev = dict(NT["Rev"]); R1112 = {r for r in rev if re.match(r"Rev (11|12):", r)}
def find(rx):
    c = re.compile(rx); out = dict(lxx=[], rev_else=[], acts=[], letters=[])
    for g in GOS: out[g + ":cross"] = []; out[g + ":rest"] = []
    for b, vs in LXX.items():
        for r, t in vs:
            if c.search(t): out["lxx"].append(r)
    for b, vs in NT.items():
        for r, t in vs:
            if not c.search(t): continue
            if b in GOS: out[b + (":cross" if r in PR[b] else ":rest")].append(r)
            elif b == "Rev":
                if r not in R1112: out["rev_else"].append(r)
            elif b == "Acts": out["acts"].append(r)
            else: out["letters"].append(r)
    return out
rows, bad = [], []
for sec, v, mid, gloss, rx, rx2 in M:
    if not re.search(rx, rev["Rev " + v]): bad.append((v, mid))
    rows.append(dict(section=sec, verse=v, id=mid, gloss=gloss, rx=rx, rx2=rx2, own=find(rx), loose=find(rx2) if rx2 else None))
print("members:", len(rows), dict(collections.Counter(r["section"] for r in rows)), "| not found in own verse:", bad or "none")
def cls(r):
    o = r["own"]; g = any(o[x + ":cross"] or o[x + ":rest"] for x in GOS); l = bool(o["lxx"]); n = bool(o["acts"] or o["letters"])
    return ("Septuagint and Gospels" if l and g else "Septuagint, not the Gospels" if l else "Gospels, not the Septuagint" if g else "elsewhere in the New Testament only" if n else "Revelation only")
for r in rows: r["class"] = cls(r)
for s in "WJG": print(s, dict(collections.Counter(r["class"] for r in rows if r["section"] == s)))
# (4) windows. A member counts for a Gospel if its own form is in it and in fewer than 3% of its verses.
def windows(sec, g, L):
    vs = NT[g]; mem = []
    for r in rows:
        if r["section"] != sec: continue
        hits = set(r["own"][g + ":cross"] + r["own"][g + ":rest"])
        if hits and len(hits) < 0.03 * len(vs): mem.append((r["id"], hits))
    sc = []
    for i in range(0, len(vs) - L + 1):
        w = {x for x, _ in vs[i:i + L]}; sc.append((sum(1 for _, h in mem if h & w), i))
    return mem, sc, vs
W = {}
for sec in "WJG":
    for g in GOS:
        L = len(PR[g]); mem, sc, vs = windows(sec, g, L); refs = [x for x, _ in vs]; pi = refs.index(PASSION[g][0]); ps = sc[pi][0]
        best = sorted(sc, reverse=True)[:1][0]; ge = sum(1 for s_, _ in sc if s_ >= ps); top = []
        used = []
        for s_, i in sorted(sc, reverse=True):
            if all(abs(i - j) >= L for j in used): used.append(i); top.append((s_, refs[i], refs[i + L - 1]))
            if len(top) == 3: break
        W[f"{sec}:{g}"] = dict(members_usable=len(mem), window=L, cross_score=ps, windows=len(sc), windows_at_least_cross=ge, top=top)
        print(f"{sec} {g}: usable members {len(mem)} | window {L} verses | cross and tomb holds {ps} | windows holding as many: {ge} of {len(sc)} | top:", top)
json.dump(dict(rows=rows, windows=W, bad=bad), open(sys.argv[3], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
def sh(x, n=4): return (",".join(a.split(" ",1)[1] if a[0].isascii() else a for a in x[:n]) + ("…" if len(x) > n else "")) if x else "—"
for r in rows:
    o = r["own"]; print(f"\n[{r['section']}] {r['verse']} {r['id']} — {r['gloss']} :: {r['class']}")
    print("   LXX", len(o["lxx"]), [a for a in o["lxx"][:5]], "| Rev else", len(o["rev_else"]), "| Acts", sh(o["acts"]), "| letters", sh([a for a in o["letters"]], 5))
    print("   " + " | ".join(f"{g} cross {sh(o[g+':cross'])} rest {len(o[g+':rest'])}:{sh(o[g+':rest'],5)}" for g in GOS))
    if r["loose"]:
        o = r["loose"]; print("   loosened: LXX", len(o["lxx"]), o["lxx"][:4], "| " + " | ".join(f"{g} {sh(o[g+':cross']+o[g+':rest'],5)}" for g in GOS), "| Acts", sh(o["acts"]), "| letters", sh(o["letters"]))
