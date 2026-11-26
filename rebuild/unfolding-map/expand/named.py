#!/usr/bin/env python3
"""Expansions named by reading, tested by rank. For each: a seed of one to three verses of Revelation, and the stretch of a Gospel the reader says expands
it. The seed's members are its content lemmas, taken by machine, none chosen. The score is the one of expand.py (each lemma held, weighed by rarity and by
how often it is said). Two questions: among ALL stretches of that length in the four Gospels, where does the named one rank for this seed? And among 300
other seeds of the same size drawn from Revelation, how many score as high at the named stretch? The pairs were written before either number was seen.
   python3 named.py <fetch dir> out.json"""
import sys, re, json, math, pathlib, collections, unicodedata, random
fetch = pathlib.Path(sys.argv[1]) / "tischendorf-data/word-per-line/2.8/Unicode"
def nrm(s):
    s = unicodedata.normalize("NFD", s); return "".join(c for c in s if not unicodedata.combining(c)).lower().replace("ς", "σ")
BK = collections.OrderedDict()
for p in sorted(fetch.glob("*.txt")):
    vs = collections.OrderedDict()
    for l in open(p, encoding="utf-8"):
        q = l.split()
        if len(q) > 7: vs.setdefault(f"{p.stem} {q[1].split('.')[0]}", []).append(nrm(q[7]))
    BK[p.stem] = list(vs.items())
df = collections.Counter(l for b, vs in BK.items() for _, ls in vs for l in set(ls)); NV = sum(len(v) for v in BK.values())
content = lambda l: df[l] <= 120 and len(l) >= 3; idf = lambda l: math.log(NV / df[l]); GOS = ["MT", "MR", "LU", "JOH"]
def rng(b, a, z): refs = [r for r, _ in BK[b]]; i, j = refs.index(f"{b} {a}"), refs.index(f"{b} {z}"); return i, j
def lem(b, a, z): i, j = rng(b, a, z); return [l for _, ls in BK[b][i:j + 1] for l in ls]
def score(seed, ls):
    c = collections.Counter(l for l in ls if l in seed); return sum(idf(l) * (1 + math.log(x)) for l, x in c.items()), c
P = [("the water of life, freely", ("21:6", "21:6"), "JOH", "4:7", "4:15"), ("let the thirsty come", ("22:17", "22:17"), "JOH", "7:37", "7:39"), ("my reward with me; the first and the last", ("22:12", "22:13"), "MT", "20:1", "20:16"),
     ("I stand at the door and knock", ("3:20", "3:20"), "LU", "12:35", "12:40"), ("the harvest and the sickle", ("14:15", "14:16"), "MT", "13:36", "13:43"), ("the harvest and the sickle (Mark)", ("14:15", "14:16"), "MR", "4:26", "4:29"),
     ("the wedding of the Lamb", ("19:7", "19:9"), "MT", "22:1", "22:14"), ("I come as a thief", ("3:3", "3:3"), "MT", "24:42", "24:44"), ("no more hunger or thirst", ("7:16", "7:17"), "JOH", "6:30", "6:40"),
     ("the woman and the child", ("12:1", "12:5"), "MT", "1:18", "2:15"), ("I was dead and am alive", ("1:17", "1:18"), "MT", "28:1", "28:10"), ("the great white throne", ("20:11", "20:15"), "MT", "25:31", "25:46"),
     ("the open door; the wedding", ("3:7", "3:8"), "MT", "25:1", "25:13"), ("hold what you have till I come; authority", ("2:25", "2:26"), "LU", "19:12", "19:27"), ("hold what you have; authority (Matthew)", ("2:25", "2:26"), "MT", "25:14", "25:30"),
     ("faithful unto death; the crown", ("2:10", "2:10"), "MT", "25:14", "25:30"), ("the confession before the Father", ("3:5", "3:5"), "MT", "10:26", "10:33"), ("the lamp and the bridegroom's voice", ("18:23", "18:23"), "JOH", "3:25", "3:30"),
     ("the shepherd and the springs", ("7:17", "7:17"), "JOH", "10:1", "10:16"), ("bought from the earth; they follow the Lamb", ("14:3", "14:4"), "JOH", "1:35", "1:43")]
rv = BK["RE"]; random.seed(1126); OUT = []
for name, (a, z), g, ta, tz in P:
    seed = {l for l in lem("RE", a, z) if content(l)}; i, j = rng(g, ta, tz); n = j - i + 1; s0, c0 = score(seed, lem(g, ta, tz)); better = 0; tot = 0; top = (0, "")
    for h in GOS:
        vs = BK[h]
        for w in range(0, len(vs) - n + 1):
            if h == g and abs(w - i) < n: continue
            s, _ = score(seed, [l for _, ls in vs[w:w + n] for l in ls]); tot += 1; better += s >= s0
            if s > top[0]: top = (s, vs[w][0])
    m = rng("RE", a, z)[1] - rng("RE", a, z)[0] + 1; tgt = lem(g, ta, tz); ge = 0; N = 300
    for _ in range(N):
        k = random.randrange(0, len(rv) - m); sd = {l for _, ls in rv[k:k + m] for l in ls if content(l)}; ge += score(sd, tgt)[0] >= s0
    OUT.append(dict(name=name, seed=f"Rev {a}" + (f"–{z.split(':')[1]}" if z != a else ""), target=f"{g} {ta}–{tz}", lemmas=len(seed), held=len(c0), said=sum(c0.values()), score=round(s0, 1), windows_as_high=better, windows=tot, best_elsewhere=(round(top[0], 1), top[1]), random_seeds_as_high=ge / N, counts=dict(c0)))
    print(f"{name:42} {OUT[-1]['seed']:13} → {OUT[-1]['target']:16} holds {len(c0)}/{len(seed)}, said {sum(c0.values()):2} | score {s0:5.1f} | other stretches as high: {better:4} of {tot} (best elsewhere {top[0]:.1f} at {top[1]}) | random seeds as high: {ge/N:.3f} | {dict(c0)}")
json.dump(OUT, open(sys.argv[2], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
