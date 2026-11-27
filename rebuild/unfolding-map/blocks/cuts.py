#!/usr/bin/env python3
"""A review of v0.28 (2AB): the links of 2Z classed by rules fixed before any list is read, and the count after quotation-like links are removed.
  For a link (a source verse and a Gospel verse sharing at least one exclusive pairing), n = the distinct stems in its exclusive pairings.
  QUOTATION-LIKE: n >= 4 (four or more rare words shared by the two verses and paired nowhere else).
  IDIOM: no pairing of the link has both stems in at most 60 verses of the New Testament.
  CLOSE: some pairing whose two stems stand within three words of each other in both verses (a shared phrase).
  SPECIFIC = not quotation-like and not idiom.
   python3 cuts.py <alexanarch root> <engine dir> cuts.json jt_links.tsv"""
import sys, re, json, math, pathlib, collections, itertools
src = open(pathlib.Path(__file__).with_name("excl2.py")).read().split("def setting(")[0].split('"""', 2)[2]
exec(src)
stem = mkstem(5); ST = [(k, [stem(x) for x in w], w) for k, w in RAW]; df = collections.Counter(s for k, ss, _ in ST if k[0] == "N" for s in set(ss) if s); ok = {s for s, c in df.items() if c <= 120}
UD = {k: (ss, w) for k, ss, w in ST}; isg = lambda k: k[0] == "N" and k[1].split()[0] in GOS; IX = collections.defaultdict(set); GP = collections.defaultdict(list)
for k, ss, _ in ST:
    u = sorted(set(s for s in ss if s in ok))
    if isg(k):
        for p in itertools.combinations(u, 2): GP[p].append(k)
    else:
        for s in u: IX[s].add(k)
def close(k, a, b):
    ss = UD[k][0]; pa = [i for i, s in enumerate(ss) if s == a]; pb = [i for i, s in enumerate(ss) if s == b]; return any(abs(i - j) <= 3 for i in pa for j in pb)
def snip(k, a, b):
    ss, w = UD[k]; idx = [i for i, s in enumerate(ss) if s in (a, b)]; return " ".join(w[max(0, min(idx) - 2):max(idx) + 3])[:90]
G = groups(); OUT = {}; LISTS = {}
print(f"{'source':26}{'links':>7}{'/100':>7}{'quot-like':>10}{'idiom':>7}{'specific':>9}{'/100':>7}{'close':>7}{'/100':>7}{'spec+close':>11}{'/100':>7}{'after cut /100':>15}{'top 5% verses hold':>19}{'max stems':>10}")
for name, keys in G.items():
    if name == "Revelation": secs = [keys[keys.index(("N", a)):keys.index(("N", b)) + 1] for a, b in SECJ]
    else: n = len(keys) // 10; secs = [keys[i * n:(i + 1) * n] for i in range(10)]
    links = {}; nv = 0
    for sec in secs:
        own = set(sec); nv += len(sec)
        for k in sec:
            for p in itertools.combinations(sorted(set(s for s in UD[k][0] if s in ok)), 2):
                if p in GP and not ((IX[p[0]] & IX[p[1]]) - own):
                    for g in GP[p]: links.setdefault((k, g), []).append(p)
    rows = []
    for (k, g), ps in links.items():
        n = len({s for p in ps for s in p}); q = n >= 4; idi = not any(df[a] <= 60 and df[b] <= 60 for a, b in ps); cl = any(close(k, a, b) and close(g, a, b) for a, b in ps)
        rows.append(dict(src=k[1], gos=g[1], n=n, quot=q, idiom=idi and not q, specific=(not q and not idi), close=cl, pairs=ps))
    qv = {r["src"] for r in rows if r["quot"]}; after = [r for r in rows if r["src"] not in qv]; per = lambda x: round(100 * x / nv, 1)
    c = collections.Counter(r["src"] for r in rows); top = sorted(c.values(), reverse=True); t5 = sum(top[:max(1, round(0.05 * len(c)))]) / max(1, len(rows))
    o = dict(verses=nv, links=len(rows), per100=per(len(rows)), quot=sum(r["quot"] for r in rows), idiom=sum(r["idiom"] for r in rows), specific=sum(r["specific"] for r in rows), specific100=per(sum(r["specific"] for r in rows)),
             close=sum(r["close"] for r in rows), close100=per(sum(r["close"] for r in rows)), speclose=sum(r["specific"] and r["close"] for r in rows), speclose100=per(sum(r["specific"] and r["close"] for r in rows)),
             after100=round(100 * len(after) / (nv - len(qv)), 1), top5=round(100 * t5), maxstems=max(r["n"] for r in rows))
    OUT[name] = o; LISTS[name] = rows
    print(f"{name:26}{o['links']:>7}{o['per100']:>7}{o['quot']:>10}{o['idiom']:>7}{o['specific']:>9}{o['specific100']:>7}{o['close']:>7}{o['close100']:>7}{o['speclose']:>11}{o['speclose100']:>7}{o['after100']:>15}{o['top5']:>18}%{o['maxstems']:>10}")
json.dump(OUT, open(sys.argv[3], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
def dump(name, path=None, show=True):
    rows = sorted((r for r in LISTS[name] if r["specific"] and r["close"]), key=lambda r: (r["src"], r["gos"])); out = []
    for r in rows:
        a, b = next((p for p in r["pairs"] if df[p[0]] <= 60 and df[p[1]] <= 60), r["pairs"][0]); sk = next(k for k in UD if k[1] == r["src"]); gk = ("N", r["gos"])
        out.append(f"{r['src'].split('|')[-1][-22:]:22} {r['gos']:11} {snip(sk, a, b):46} || {snip(gk, a, b)}")
    if path: open(path, "w", encoding="utf-8").write("\n".join(out))
    if show: print(f"\n== {name}: specific and close, {len(out)}\n" + "\n".join(out))
dump("Judith, Tobit", sys.argv[4]); dump("Revelation", sys.argv[4].replace("jt_", "rev_"))
