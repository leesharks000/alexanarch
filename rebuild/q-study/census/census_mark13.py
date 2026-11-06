#!/usr/bin/env python3
"""Run PLAN-mark13.md (sha256 6414c86c...) exactly. Writes RESULTS-mark13.json and RESULTS-mark13.md."""
import unicodedata, re, json, pathlib, hashlib, collections
ROOT = pathlib.Path(__file__).resolve().parents[3]; C = ROOT / "data/corpora"
assert hashlib.sha256((pathlib.Path(__file__).parent / "PLAN-mark13.md").read_bytes()).hexdigest().startswith("6414c86c")
def norm(s):
    s = unicodedata.normalize("NFD", s.lower()); s = "".join(ch for ch in s if not unicodedata.combining(ch)).replace("ς", "σ")
    return re.sub(r"[^\w\s]|\d|_", " ", s).split()
def verses(path):
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if "\t" in line:
            ref, t = line.split("\t", 1); out.append((ref.strip(), norm(t)))
    return out
def tri(v):
    return [tuple(v[i:i+3]) for i in range(len(v) - 2)]
def index(vs):
    ix = collections.defaultdict(list)
    for ref, w in vs:
        for t in tri(w): ix[t].append(ref)
    return ix
G = C / "gnt-nestle1904/text"; L = C / "lxx-swete/text"
def chap(vs, book, c, a=None, b=None):
    r = []
    for ref, w in vs:
        m = re.match(rf"{book} (\d+):(\d+)$", ref)
        if m and int(m.group(1)) == c and (a is None or a <= int(m.group(2)) <= b): r.append((ref, w))
    return r
mark, luke, matt = verses(G / "Mark.txt"), verses(G / "Luke.txt"), verses(G / "Matt.txt")
D = {"Mark 13": chap(mark, "Mark", 13), "Luke 17:22-37": chap(luke, "Luke", 17, 22, 37), "Matt 24": chap(matt, "Matt", 24)}
REV = index(verses(G / "Rev.txt"))
DAN = index(verses(next(L.glob("tlg056-*"))) + verses(next(L.glob("tlg057-*"))))
LXX = collections.defaultdict(list)
for f in sorted(L.glob("*.txt")):
    for t, refs in index(verses(f)).items(): LXX[t] += refs
bg_books = [p for p in sorted(G.glob("*.txt")) if p.stem not in ("Mark", "Luke", "Matt", "Rev")]
assert len(bg_books) == 23, len(bg_books)
BG = collections.Counter()
for p in bg_books:
    for t in set(index(verses(p))): BG[t] += 1
res = {"plan_sha256": hashlib.sha256((pathlib.Path(__file__).parent / "PLAN-mark13.md").read_bytes()).hexdigest(), "discourses": {}}
for name, vs in D.items():
    seen = {}
    for ref, w in vs:
        for t in tri(w): seen.setdefault(t, []).append(ref)
    R = {t: r for t, r in seen.items() if t in REV}
    common = {t for t in R if BG[t] > 4}
    Rc = {t: r for t, r in R.items() if t not in common}
    rows = [{"trigram": " ".join(t), "in": r, "rev": REV[t][:6], "lxx": len(LXX.get(t, [])), "dan": DAN.get(t, [])[:4], "bg_books": BG[t]} for t, r in sorted(Rc.items(), key=lambda x: x[1][0])]
    res["discourses"][name] = {"verses": len(vs), "trigrams": len(seen), "R": len(Rc), "R_minus_L": sum(1 for x in rows if x["lxx"] == 0),
        "A": sum(1 for t in seen if t in DAN), "L": sum(1 for t in seen if t in LXX), "background_common": sorted(" ".join(t) for t in common), "rows": rows}
(pathlib.Path(__file__).parent / "RESULTS-mark13.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
md = [f"# Results: Mark 13 against its extant candidates (plan {res['plan_sha256'][:12]}…)", ""]
for name, r in res["discourses"].items():
    md += [f"## {name}", "", f"{r['verses']} verses, {r['trigrams']} distinct trigrams. In Revelation (background-common removed): {r['R']}; of these absent from the LXX: {r['R_minus_L']}. In Daniel (OG or Theodotion): {r['A']}. Anywhere in the LXX: {r['L']}.", "", f"Background-common, not counted: {', '.join(r['background_common']) or 'none'}", "", "| trigram | discourse | Revelation | LXX hits | Daniel |", "|---|---|---|---|---|"]
    md += [f"| {x['trigram']} | {', '.join(x['in'])} | {', '.join(x['rev'])} | {x['lxx']} | {', '.join(x['dan']) or '—'} |" for x in r["rows"]] + [""]
(pathlib.Path(__file__).parent / "RESULTS-mark13.md").write_text("\n".join(md), encoding="utf-8"); print("\n".join(md))
