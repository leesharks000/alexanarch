#!/usr/bin/env python3
"""The letters to the seven churches (Rev 2-3) against the night of the supper in each Gospel (2X.3).
   python3 night.py <alexanarch root> <engine dir> night.json"""
import sys, re, json, math, pathlib, collections
sys.path.insert(0, sys.argv[2]); import midrash as E
sys.argv_keep = sys.argv; root = pathlib.Path(sys.argv[1]) / "data/corpora"
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
                if re.search(r"\d+:\d+$", r) and r not in seen: seen.add(r); o.append((r, sq(t)))
    return o
NT, LXX = load("gnt-nestle1904"), load("lxx-swete"); D = dict(NT); refs = [r for r, _ in NT]; ST = {r: set(filter(None, map(stem, t.split()))) for r, t in NT}
df = collections.Counter(s for r in ST for s in ST[r]); W = {s: math.log(len(NT) / c) for s, c in df.items() if c <= 120}
def span(a, b): return refs[refs.index(a):refs.index(b) + 1]
NIGHT = dict(Matt=span("Matt 26:17", "Matt 26:75"), Mark=span("Mark 14:12", "Mark 14:72"), Luke=span("Luke 22:7", "Luke 22:65"), John=span("John 13:1", "John 18:27")); LET = span("Rev 2:1", "Rev 3:22")
def bag(vs): return set().union(*(ST[v] for v in vs))
def sc(a, b): return sum(W[s] for s in a & b if s in W)
L = bag(LET); OUT = dict(rank={}, counts={}); rv = [r for r in refs if r.startswith("Rev ")]
print("== rank. For each night: the letters against every other stretch of 51 verses of Revelation; and the night against every other stretch of its Gospel of the same length")
for g, vs in NIGHT.items():
    nb = bag(vs); mine = sc(nb, L); others = [sc(nb, bag(rv[i:i + 51])) for i in range(51, len(rv) - 50, 10)]
    gv = [r for r in refs if r.startswith(g + " ")]; n = len(vs); i0 = gv.index(vs[0]); oth2 = [sc(bag(gv[i:i + n]), L) for i in range(0, len(gv) - n + 1, 10) if abs(i - i0) >= n]
    OUT["rank"][g] = dict(score=round(mine, 1), rev_higher=sum(o >= mine for o in others), rev_of=len(others), gospel_higher=sum(o >= mine for o in oth2), gospel_of=len(oth2))
    print(f"  {g}: night ({n} verses) with the letters {mine:.1f} | other stretches of Revelation as high: {sum(o >= mine for o in others)} of {len(others)} (best {max(others):.1f}) | other stretches of {g} as high for the letters: {sum(o >= mine for o in oth2)} of {len(oth2)}" + (f" (best {max(oth2):.1f})" if oth2 else ""))
print("\n== the rarest stems the letters share with each night (stem: night verses | letters' verses)")
for g, vs in NIGHT.items():
    nb = bag(vs); sh = sorted((s for s in nb & L if s in W and df[s] <= 40), key=lambda s: df[s])[:34]; print(" ", g)
    for s in sh: print(f"     {s:7} df {df[s]:3}  {[v.split()[1] for v in vs if s in ST[v]][:5]} | {[v.split()[1] for v in LET if s in ST[v]][:5]}")
def C(lab, rx, n=18):
    c = re.compile(rx); a = [r for r, t in NT if c.search(t)]; b = [r for r, t in LXX if c.search(t)]; OUT["counts"][lab] = dict(nt=a, lxx_n=len(b), lxx=b[:6]); print(f"  # {lab}: NT {len(a)} {a[:n]} | LXX {len(b)} {b[:4]}")
print("\n== counts")
C("deny (ἀρνέομαι, ἀπαρνέομαι)", r"\b(απ)?(αρν(ησ|ουμ|εισθ|ειτ)|ηρνησ|ηρνημ|αρνησ)", 40); C("deny with name or faith, one verse", r"(αρν|ηρν).*(ονομα|πιστ)|(ονομα|πιστ).*(αρν|ηρν)")
C("stand at the door", r"(εστηκ|ιστηκ|εστωσ|εστωτ)\w* (επι|προσ) (τη[ν]? )?θυρα"); C("cold (ψῦχος, ψυχρός)", r"\bψυχ(οσ|ουσ|ει|ρ)"); C("warm, hot (θερμ-, ζεστ-)", r"θερμ|ζεστ"); C("overcome (νικάω)", r"\b(νικ(ων|ωντ|α|ησ)|ενικησ|νενικηκ)", 40)
C("keep my word(s)", r"τον λογον (μου|τησ υπομονησ μου) (ε)?τηρ|(ε)?τηρ\w+ (μου )?τον λογον|τον εμον λογον τηρ|τον λογον σου τετηρ|λογουσ μου (ου )?τηρ"); C("remember (μνημονεύω), as a command", r"μνημονευε"); C("naked", r"γυμν"); C("tribulation with 'you will have'", r"θλιψιν εχετε|εξετε θλιψιν")
C("hate, I also / they hated me", r"μισ(ω|ει|ειτε|εισ).*καγω|καγω μισω|εμισησ"); C("first love / greater love (ἀγάπη with first, greater)", r"αγαπην.*(πρωτην|μειζονα)|(πρωτην|μειζονα).*αγαπην"); C("a new name / new commandment", r"(ονομα|εντολην) (μου το )?καιν"); C("I have loved you", r"ηγαπησα (σε|υμασ)")
for r in ("John 18:16", "John 18:17", "John 18:18", "John 18:25", "Rev 3:8", "Rev 3:15", "Rev 3:16", "Rev 3:17", "Rev 3:18", "Rev 2:13", "Rev 2:4", "Rev 2:6", "Rev 3:9", "John 16:33", "John 15:18", "John 13:34", "John 15:9", "John 15:13", "John 15:20", "Mark 14:51", "Mark 14:52", "John 13:4", "Rev 2:17", "John 17:6"): print("  ", r, D[r][:300]); OUT.setdefault("verses", {})[r] = D[r]
json.dump(OUT, open(sys.argv[3], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
