#!/usr/bin/env python3
"""Section against block (2Y): each section of Revelation against each block of each Gospel, by rank on both sides; and the dialect control from 1 John.
  score = summed rarity weight of the crude stems both hold (as conj.py).
  For a pair: A = share of other Gospel stretches of the block's length (all four Gospels, every 10 verses, not overlapping the block) that score as high with the section;
              B = share of other stretches of Revelation of the section's length (every 5 verses, not overlapping the section) that score as high with the block.
  A pair STANDS if A <= 0.10 and B <= 0.10. The same is run with Acts and with Isaiah cut in ten in Revelation's place.
   python3 blocks.py <alexanarch root> <engine dir> out.json"""
import sys, re, json, math, pathlib, collections
sys.path.insert(0, sys.argv[2]); import midrash as E
root = pathlib.Path(sys.argv[1]) / "data/corpora"
END = sorted("ουσιν ομεθα εσθαι ησαν ουσα ουσι ομεν ετε ουσ οισ αισ ασι ων ου οσ ον οι ην ησ ασ αι εσ ει εν α η ω ε ι ν σ".split(), key=len, reverse=True)
def stem(w):
    if len(w) < 4: return None
    for e in END:
        if w.endswith(e) and len(w) - len(e) >= 3: w = w[:-len(e)]; break
    return w[:5]
def sq(s): return re.sub(r"\s+", " ", E.norm(s)).strip()
def load(c):
    o = []
    for p in sorted((root / c / "text").glob("*.txt")):
        seen = set()
        for l in p.read_text(encoding="utf-8", errors="ignore").splitlines():
            if "\t" in l:
                r, t = l.split("\t", 1); r = r.strip()
                if re.search(r"\d+:\d+$", r) and r not in seen: seen.add(r); o.append((p.stem, r, sq(t)))
    return o
NTl, LXl = load("gnt-nestle1904"), load("lxx-swete"); NT = [(r, t) for _, r, t in NTl]; D = dict(NT); refs = [r for r, _ in NT]
ST = {r: set(filter(None, map(stem, t.split()))) for r, t in NT}; df = collections.Counter(s for r in ST for s in ST[r]); W = {s: math.log(len(NT) / c) for s, c in df.items() if c <= 120}
ISA = [(r, set(filter(None, map(stem, t.split())))) for b, r, t in LXl if "σα" in b and r.startswith("Ἠσα")]
def span(a, b): return refs[refs.index(a):refs.index(b) + 1]
def bag(vs, S=ST): return set().union(*(S[v] for v in vs)) if vs else set()
def sc(a, b): return sum(W[s] for s in a & b if s in W)
SEC = [("the vision of the Son of Man", "Rev 1:1", "Rev 1:20"), ("the seven letters", "Rev 2:1", "Rev 3:22"), ("the throne and the Lamb", "Rev 4:1", "Rev 5:14"), ("the seals", "Rev 6:1", "Rev 8:1"), ("the trumpets", "Rev 8:2", "Rev 11:19"),
       ("the woman, the dragon, the beasts", "Rev 12:1", "Rev 14:20"), ("the bowls", "Rev 15:1", "Rev 16:21"), ("Babylon", "Rev 17:1", "Rev 19:10"), ("the rider, the thousand years, the judgment", "Rev 19:11", "Rev 20:15"), ("the new Jerusalem", "Rev 21:1", "Rev 22:21")]
BLK = [("Matt: birth", "Matt 1:1", "Matt 2:23"), ("Matt: the Baptist, the testing", "Matt 3:1", "Matt 4:25"), ("Matt: the Sermon", "Matt 5:1", "Matt 7:29"), ("Matt: Galilee I", "Matt 8:1", "Matt 10:42"), ("Matt: Galilee II, parables", "Matt 11:1", "Matt 13:58"),
       ("Matt: Galilee III", "Matt 14:1", "Matt 18:35"), ("Matt: the journey", "Matt 19:1", "Matt 20:34"), ("Matt: the temple days", "Matt 21:1", "Matt 23:39"), ("Matt: the discourse on the end", "Matt 24:1", "Matt 25:46"), ("Matt: the night", "Matt 26:1", "Matt 26:75"), ("Matt: cross and tomb", "Matt 27:1", "Matt 28:20"),
       ("Mark: beginnings", "Mark 1:1", "Mark 1:45"), ("Mark: Galilee I", "Mark 2:1", "Mark 5:43"), ("Mark: Galilee II", "Mark 6:1", "Mark 8:26"), ("Mark: the journey", "Mark 8:27", "Mark 10:52"), ("Mark: the temple days", "Mark 11:1", "Mark 12:44"), ("Mark: the discourse on the end", "Mark 13:1", "Mark 13:37"), ("Mark: the night", "Mark 14:1", "Mark 14:72"), ("Mark: cross and tomb", "Mark 15:1", "Mark 16:8"),
       ("Luke: birth", "Luke 1:1", "Luke 2:52"), ("Luke: the Baptist, the testing", "Luke 3:1", "Luke 4:13"), ("Luke: Galilee", "Luke 4:14", "Luke 9:50"), ("Luke: the journey I", "Luke 9:51", "Luke 13:21"), ("Luke: the journey II", "Luke 13:22", "Luke 19:27"), ("Luke: the temple days", "Luke 19:28", "Luke 21:4"), ("Luke: the discourse on the end", "Luke 21:5", "Luke 21:38"), ("Luke: the night", "Luke 22:1", "Luke 22:71"), ("Luke: cross and tomb", "Luke 23:1", "Luke 24:53"),
       ("John: the prologue and first week", "John 1:1", "John 2:12"), ("John: temple, Nicodemus, Samaria", "John 2:13", "John 4:54"), ("John: the feasts I", "John 5:1", "John 6:71"), ("John: the feasts II", "John 7:1", "John 10:42"), ("John: Lazarus, the entry", "John 11:1", "John 12:50"), ("John: the supper and discourse", "John 13:1", "John 17:26"), ("John: arrest, trial, cross", "John 18:1", "John 19:42"), ("John: the tomb, the lake", "John 20:1", "John 21:25")]
GV = [r for r in refs if r.split()[0] in ("Matt", "Mark", "Luke", "John")]
def run(name, secs, SV, S=ST):
    """secs: list of (label, [verse keys]); SV: ordered verse keys of the source; S: stems by key"""
    sb = {l: bag(v, S) for l, v in secs}; res = []
    for bl, a, b in BLK:
        bv = span(a, b); bb = bag(bv); n = len(bv); i0 = GV.index(bv[0]); oth = [bag(GV[i:i + n]) for i in range(0, len(GV) - n + 1, 10) if abs(i - i0) >= n]
        for l, v in secs:
            mine = sc(sb[l], bb); A = sum(sc(sb[l], o) >= mine for o in oth) / max(1, len(oth)); m = len(v); j0 = SV.index(v[0])
            o2 = [bag(SV[j:j + m], S) for j in range(0, len(SV) - m + 1, 5) if abs(j - j0) >= m]; B = sum(sc(o, bb) >= mine for o in o2) / max(1, len(o2))
            res.append(dict(section=l, block=bl, score=round(mine, 1), A=round(A, 3), B=round(B, 3)))
    st = [x for x in res if x["A"] <= 0.10 and x["B"] <= 0.10]; print(f"\n== {name}: pairs {len(res)}; standing on both sides at one in ten: {len(st)}; at one in twenty: {sum(1 for x in st if x['A']<=.05 and x['B']<=.05)}")
    return res, st
rv = [r for r in refs if r.startswith("Rev ")]; res, st = run("Revelation", [(l, span(a, b)) for l, a, b in SEC], rv)
for x in sorted(st, key=lambda x: x["A"] + x["B"]): print(f"   {x['section']:44} × {x['block']:36} A {x['A']:.3f}  B {x['B']:.3f}")
OUT = dict(revelation=res, standing=st)
ac = [r for r in refs if r.startswith("Acts ")]; k = len(ac) // 10; r2, s2 = run("Acts, cut in ten, in Revelation's place", [(f"Acts part {i+1}", ac[i * k:(i + 1) * k]) for i in range(10)], ac); OUT["acts_standing"] = len(s2)
ik = [r for r, _ in ISA]; IS = dict(ISA); k = len(ik) // 10; r3, s3 = run("Isaiah, cut in ten, in Revelation's place", [(f"Isa part {i+1}", ik[i * k:(i + 1) * k]) for i in range(10)], ik, IS); OUT["isaiah_standing"] = len(s3)
print("\n== for each section, its best block by A+B (whether standing or not)")
for l, _, _ in SEC:
    x = min((x for x in res if x["section"] == l), key=lambda x: x["A"] + x["B"]); print(f"   {l:44} {x['block']:36} A {x['A']:.3f} B {x['B']:.3f}")
print("\n== the rare stems of the standing pairs (stem: block verses | section verses)")
for x in sorted(st, key=lambda x: x["A"] + x["B"]):
    l, a, b = next(s for s in SEC if s[0] == x["section"]); bl, c, d = next(s for s in BLK if s[0] == x["block"]); sv, bv = span(a, b), span(c, d)
    sh = sorted((s for s in bag(sv) & bag(bv) if s in W and df[s] <= 30), key=lambda s: df[s])[:26]; print(f"\n  {x['section']} × {x['block']}")
    print("    " + "; ".join(f"{s}[{','.join(v.split()[1] for v in bv if s in ST[v])[:22]}|{','.join(v.split()[1] for v in sv if s in ST[v])[:18]}]" for s in sh))
print("\n== the dialect control: the night's wordings, counted in John's night (13:1-18:27), the rest of John, 1-3 John, the letters to the churches, the rest of Revelation")
P = [("keep my / his word", r"τον λογον (μου|αυτου|σου|τησ υπομονησ μου) (ε|τε)?τηρ|(ε|τε)?τηρ\w+ (μου |αυτου )?τον λογον|τον εμον λογον τηρ|λογουσ μου (ου )?τηρ"), ("keep out of (τηρέω ἐκ)", r"τηρησ\w+ (αυτουσ |σε )?εκ "), ("have tribulation", r"θλιψιν εχετε|εξετε θλιψιν"),
     ("overcome (νικάω)", r"\b(νικ(ων|ωντ|α|ησ)|ενικησ|νενικηκ)"), ("I have loved you", r"ηγαπησα (σε|υμασ)"), ("deny", r"\b(απ)?(αρν(ησ|ουμ|εισθ|ειτ)|ηρνησ|ηρνημ)"), ("hate", r"\bμισ(ω|ει|ειτε|εισ|ων|ησ)|εμισησ|μεμισηκ"), ("remember, a command", r"μνημονευε"),
     ("κἀγώ with the Father", r"καγω.*πατ(ηρ|ροσ|ρι|ερα)|πατ(ηρ|ροσ|ρι|ερα).*καγω"), ("keep the commandments", r"τηρ\w+ τασ εντολασ|εντολασ (μου |αυτου )?(ε|τε)?τηρ"), ("works, with know", r"οιδα (σου )?τα εργα|γινωσκ\w+ .*εργα"), ("stand at the door", r"(εστηκ|ιστηκ)\w* (επι|προσ) (τη[ν]? )?θυρα"), ("cold", r"\bψυχ(οσ|ρ)"), ("abide (μένω)", r"\bμεν(ει|ω|ετε|ων|ειν|η|ητε)\b|\bμεινα")]
night = set(span("John 13:1", "John 18:27"))
def where(r): return "night" if r in night else "John" if r.startswith("John ") else "1-3John" if re.match(r"[123]John ", r) else "letters" if re.match(r"Rev [23]:", r) else "Rev" if r.startswith("Rev ") else "other"
print(f"   {'wording':28} night  John-rest  1-3John  letters  Rev-rest  other NT"); OUT["dialect"] = {}
for lab, rx in P:
    c = collections.Counter(where(r) for r, t in NT if re.search(rx, t)); OUT["dialect"][lab] = dict(c); print(f"   {lab:28} {c['night']:4} {c['John']:9} {c['1-3John']:8} {c['letters']:8} {c['Rev']:8} {c['other']:8}")
json.dump(OUT, open(sys.argv[3], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
