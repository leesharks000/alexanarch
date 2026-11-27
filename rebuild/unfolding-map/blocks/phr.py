#!/usr/bin/env python3
"""The shared-phrase count of 2AB.1 c, tried to break (2AD): more sources in Revelation's place, among them the other apocalyptic and Second Temple
Greek that is seated, and rates by words as well as by verses. Sources that are not divided into verses are cut into units of 25 words.
OCR'd editions are reduced to their Greek lines (a line counts if nine-tenths of its letters are Greek and it has five words); apparatus that
survives the filter is noise against the source, not for it.
   python3 phr.py <alexanarch root> <engine dir> phr.json"""
import sys, re, json, math, pathlib, collections, itertools
src = open(pathlib.Path(__file__).with_name("excl2.py")).read().split("def setting(")[0].split('"""', 2)[2]
exec(src)
C = root
def greek_words(text): return [w for w in E.norm(text).split() if re.fullmatch(r"[α-ω]+", w)]
def chunks(words, key, n=25): return [(("X", f"{key} #{i//n+1}"), words[i:i + n]) for i in range(0, len(words) - n + 1, n)]
def ocr(path, key):
    out = []
    for l in pathlib.Path(path).read_text(encoding="utf-8", errors="ignore").splitlines():
        a = [c for c in l if c.isalpha()]
        if len(l.split()) >= 5 and a and sum("Ͱ" <= c <= "Ͽ" or "ἀ" <= c <= "῿" for c in a) / len(a) >= 0.9 and sum(c.isdigit() for c in l) <= 2: out += greek_words(l)
    return chunks(out, key)
def tabbed(path, key, pre=None):
    w = []
    for l in pathlib.Path(path).read_text(encoding="utf-8", errors="ignore").splitlines():
        if "\t" in l and (pre is None or l.startswith(pre)): w += greek_words(l.split("\t", 1)[1])
    return chunks(w, key)
def plain(path, key): return chunks(greek_words(pathlib.Path(path).read_text(encoding="utf-8", errors="ignore")), key)
P = C / "second-temple-pseudepigrapha/text"; EXT = collections.OrderedDict()
EXT["Josephus, War"] = tabbed(C / "josephus/text/BJ.txt", "BJ"); EXT["Josephus, Antiquities"] = tabbed(C / "josephus/text/AJ.txt", "AJ"); EXT["Josephus, Life"] = tabbed(C / "josephus/text/Vita.txt", "Vita")
EXT["Philo, Life of Moses"] = plain(C / "philo/text/tlg022-De_vita_Mosis_lib_i_ii_.txt", "Mos"); EXT["Testaments of the Twelve (OCR)"] = ocr(P / "testaments-twelve-patriarchs-charles-1908.ocr.txt", "T12")
EXT["Sibylline Oracles (OCR)"] = ocr(P / "oracula-sibyllina-geffcken-1902.ocr.txt", "Sib"); EXT["later apocalypses, Tischendorf (OCR)"] = ocr(P / "apocalypses-apocryphae-tischendorf-1866.ocr.txt", "ApAp")
for k, v in EXT.items(): print(f"  {k}: {len(v)} units; sample: {' '.join(v[len(v)//2][1])[:110]}")
stem = mkstem(5); ALLR = RAW + [u for v in EXT.values() for u in v]
ST = {k: ([stem(x) for x in w], w) for k, w in ALLR}; df = collections.Counter(s for k, w in RAW if k[0] == "N" for s in set(ST[k][0]) if s); ok = {s for s, c in df.items() if c <= 120}
isg = lambda k: k[0] == "N" and k[1].split()[0] in GOS; IX = collections.defaultdict(set); GP = collections.defaultdict(list)
for k, w in RAW:
    u = sorted(set(s for s in ST[k][0] if s in ok))
    if isg(k):
        for p in itertools.combinations(u, 2): GP[p].append(k)
    else:
        for s in u: IX[s].add(k)
def close(k, a, b):
    ss = ST[k][0]; pa = [i for i, s in enumerate(ss) if s == a]; pb = [i for i, s in enumerate(ss) if s == b]; return any(abs(i - j) <= 3 for i in pa for j in pb)
def nt(*pre): return [k for k, _ in RAW if k[0] == "N" and k[1].startswith(pre)]
def lx(*names, ch=None): return [k for k, _ in RAW if k[0] == "L" and any(n in k[1] for n in names) and (ch is None or int(re.search(r"(\d+):\d+$", k[1])[1]) in ch)]
G = collections.OrderedDict()
G["Revelation"] = nt("Rev "); G["Acts"] = nt("Acts "); G["Isaiah"] = lx("Ἠσαΐας"); G["Judith, Tobit"] = lx("Ἰουδίθ", "Τωβίτ"); G["1 Maccabees"] = lx("Μακκαβαίων_Αʹ"); G["2 Maccabees"] = lx("Μακκαβαίων_Βʹ"); G["Genesis"] = lx("Γένεσις")
G["Daniel's visions (Theodotion 7–12)"] = lx("Theodotionis_versio) ", ch=range(7, 13)) or lx("Δανιήλ_(Theodotionis", ch=range(7, 13)); G["Ezekiel"] = lx("Ἰεζεκιήλ"); G["Zechariah"] = lx("Ζαχαρίας"); G["Wisdom, Sirach"] = lx("Σοφία_Σαλ", "Ἐκκλησιαστικός"); G["Hebrews, James, 1 Peter"] = nt("Heb ", "Jas ", "1Pet ")
for k, v in EXT.items(): G[k] = [u[0] for u in v]
OUT = {}; print(f"\n{'source':40}{'units':>7}{'words':>8}{'links/1000w':>12}{'spec+close':>11}{'/100 units':>11}{'/1000 words':>12}{'phrases':>9}{'/1000 words':>12}")
for name, keys in G.items():
    if not keys: print(name, "— no units"); continue
    n = max(1, len(keys) // 10); secs = [keys[i * n:(i + 1) * n] for i in range(10)]; links = {}; nw = sum(len(ST[k][1]) for sec in secs for k in sec); nv = sum(len(s_) for s_ in secs)
    for sec in secs:
        own = set(sec)
        for k in sec:
            for p in itertools.combinations(sorted(set(s for s in ST[k][0] if s in ok)), 2):
                if p in GP and not ((IX[p[0]] & IX[p[1]]) - own):
                    for g in GP[p]: links.setdefault((k, g), []).append(p)
    sc = []; 
    for (k, g), ps in links.items():
        nst = len({s for p in ps for s in p}); good = [p for p in ps if df[p[0]] <= 60 and df[p[1]] <= 60 and close(k, *p) and close(g, *p)]
        if nst < 4 and good: sc.append((k, g, good[0]))
    phr = {p for _, _, p in sc}
    o = dict(units=nv, words=nw, links=len(links), links1000=round(1000 * len(links) / nw, 1), speclose=len(sc), per100=round(100 * len(sc) / nv, 1), per1000w=round(1000 * len(sc) / nw, 2), phrases=len(phr), phr1000w=round(1000 * len(phr) / nw, 2),
             list=[(k[1], g[1], p[0] + "+" + p[1]) for k, g, p in sorted(sc)[:60]])
    OUT[name] = o; print(f"{name:40}{nv:>7}{nw:>8}{o['links1000']:>12}{len(sc):>11}{o['per100']:>11}{o['per1000w']:>12}{len(phr):>9}{o['phr1000w']:>12}")
json.dump(OUT, open(sys.argv[3], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
def snip(k, a, b):
    ss, w = ST[k]; idx = [i for i, s in enumerate(ss) if s in (a, b)]; return " ".join(w[max(0, min(idx) - 2):max(idx) + 3])[:70]
for name in ("later apocalypses, Tischendorf (OCR)", "Testaments of the Twelve (OCR)", "Josephus, Antiquities", "Josephus, War", "Sibylline Oracles (OCR)", "Daniel's visions (Theodotion 7–12)"):
    if name not in OUT: continue
    print(f"\n== {name}: the list (first 28)")
    for s, g, p in OUT[name]["list"][:28]:
        a, b = p.split("+"); sk = next(k for k in G[name] if k[1] == s); print(f"   {s[-16:]:16} {g:11} {snip(sk, a, b):48} || {snip(('N', g), a, b)}")
