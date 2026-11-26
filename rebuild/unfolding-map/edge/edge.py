#!/usr/bin/env python3
"""The canon's edge (2E.3). Does Revelation stand to Christian writings just outside the canon as it stands to the letters inside it?
Targets are cut into windows of 25 words so that verse length does not matter. A link is a seed verse and a target window sharing two or more rare stems
(rare as before: at most 60 verses of the New Testament) that no single Septuagint verse holds. Reported per 1,000 words of the target.
The Didache, 1 Clement and Hermas are read from First1KGreek (OpenGreekAndLatin, GitHub; CC BY-SA), fetched 2026-11-26; they are not seated in the archive.
   python3 edge.py <alexanarch root>"""
import sys, re, unicodedata, pathlib, collections, json, html
C = pathlib.Path(sys.argv[1]) / "data/corpora"; H = pathlib.Path(__file__).parent
def words(s):
    s = unicodedata.normalize("NFD", s); s = "".join(c for c in s if not unicodedata.combining(c)).lower().replace("ς", "σ"); return re.findall(r"[α-ω]+", s)
st = lambda ws: {w[:5] for w in ws if len(w) >= 4}
NTW = {p.stem: [(l.split("\t")[0], words(l.split("\t", 1)[1])) for l in p.read_text(encoding="utf-8").splitlines() if "\t" in l] for p in sorted((C / "gnt-nestle1904/text").glob("*.txt"))}
df = collections.Counter(s for b in NTW.values() for _, w in b for s in st(w)); rare = {s for s, c in df.items() if c <= 60}
LX = collections.defaultdict(set); i = 0
for p in (C / "lxx-swete/text").glob("*.txt"):
    for l in p.read_text(encoding="utf-8", errors="ignore").splitlines():
        if "\t" in l and re.search(r"\d+:\d+$", l.split("\t")[0].strip()):
            i += 1
            for s in st(words(l.split("\t", 1)[1])) & rare: LX[s].add(i)
def lxxav(sh):
    sets = [LX[s] for s in sh]; return all(sets) and bool(set.intersection(*sorted(sets, key=len)))
def tei(f):
    x = (H / f).read_text(encoding="utf-8"); x = x[x.index("<body"):]; x = re.sub(r"<note\b.*?</note>", " ", x, flags=re.S); return words(html.unescape(re.sub(r"<[^>]+>", " ", x)))
T = {"Didache": tei("tlg1311.tlg001.1st1K-grc1.xml"), "1 Clement": tei("tlg1271.tlg001.1st1K-grc1.xml"), "Hermas": tei("tlg1419.tlg001.1st1K-grc1.xml")}
for b in ("Jas", "1Pet", "2Pet", "Jude", "Heb", "Rom", "1Cor", "Eph", "Col", "1Tim", "1John", "Acts"): T[b] = [w for _, ws in NTW[b] for w in ws]
win = lambda ws: [st(ws[i:i + 25]) for i in range(0, len(ws), 25)]
def rate(seed, ws):
    W = win(ws); inv = collections.defaultdict(list)
    for j, ss in enumerate(W):
        for s in ss & rare: inv[s].append(j)
    n = 0; ex = []
    for ref, w in NTW[seed]:
        cand = collections.defaultdict(set)
        for s in st(w) & rare:
            for j in inv[s]: cand[j].add(s)
        for j, sh in cand.items():
            if len(sh) >= 2 and not lxxav(sh): n += 1; ex.append((ref, j, sorted(sh)))
    return 1000 * n / len(ws), n, ex
out = {}
print(f"{'target':11}{'words':>7}" + "".join(f"{s:>16}" for s in ("from Rev", "from Matt", "from Rom", "from Heb")))
for name, ws in T.items():
    row = {s: rate(s, ws) for s in ("Rev", "Matt", "Rom", "Heb") if s != name}; out[name] = {"words": len(ws), **{s: {"per_1000_words": round(r[0], 2), "links": r[1], "examples": r[2][:12]} for s, r in row.items()}}
    print(f"{name:11}{len(ws):>7}" + "".join((f"{row[s][0]:>9.2f} ({row[s][1]:>3})" if s in row else f"{'—':>15}") for s in ("Rev", "Matt", "Rom", "Heb")))
json.dump(out, open(H / "edge.json", "w"), ensure_ascii=False, indent=1)
for name in ("Didache", "1 Clement", "Hermas"): print(name, "from Rev:", out[name]["Rev"]["examples"][:10])
