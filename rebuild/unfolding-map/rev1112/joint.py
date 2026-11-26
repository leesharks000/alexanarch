#!/usr/bin/env python3
"""Second pass on Revelation 11-12. (a) Where each section lands in the Septuagint and in each New Testament book, by sliding window, own forms and then own
with loosened. (b) Named checks in the seat. Reads census.json.
   python3 joint.py <alexanarch root> <engine dir> census.json out.json"""
import sys, re, json, pathlib, collections
sys.path.insert(0, sys.argv[2]); import midrash as E
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
NT, LXX = load("gnt-nestle1904"), load("lxx-swete"); C = json.load(open(sys.argv[3], encoding="utf-8")); rows = C["rows"]
ALLNT = sum(len(v) for b, v in NT.items() if b != "Rev"); ALLLXX = sum(len(v) for v in LXX.values())
def hits(r, loose):
    c = [re.compile(r["rx"])] + ([re.compile(r["rx2"])] if loose and r["rx2"] else [])
    return lambda t: any(x.search(t) for x in c)
def land(sec, corpus, L, loose, cap, top=6):
    mem = []
    for r in rows:
        if r["section"] != sec: continue
        f = hits(r, loose); h = {(b, i) for b, vs in corpus.items() for i, (_, t) in enumerate(vs) if f(t)}
        if h and len(h) <= cap: mem.append((r["id"], h))
    sc = []
    for b, vs in corpus.items():
        for i in range(0, max(1, len(vs) - L + 1)):
            got = sorted(m for m, h in mem if any((b, j) in h for j in range(i, min(len(vs), i + L))))
            if got: sc.append((len(got), b, i, got))
    sc.sort(key=lambda x: -x[0]); out, used = [], []
    for n, b, i, got in sc:
        if all(not (b == ub and abs(i - ui) < L) for ub, ui in used):
            used.append((b, i)); vs = corpus[b]; out.append(dict(n=n, start=vs[i][0], end=vs[min(len(vs), i + L) - 1][0], members=got))
        if len(out) == top: break
    return dict(usable=len(mem), top=out)
OUT = dict(lxx={}, nt={})
NTX = collections.OrderedDict((b, v) for b, v in NT.items() if b != "Rev")
for sec, name in (("W", "the witnesses 11:1-13"), ("J", "the joint 11:14-19"), ("G", "the sign 12:1-17")):
    for loose in (False, True):
        a = land(sec, LXX, 40, loose, 60); b = land(sec, NTX, 40, loose, 30); OUT["lxx"][f"{sec}:{'loose' if loose else 'own'}"] = a; OUT["nt"][f"{sec}:{'loose' if loose else 'own'}"] = b
        print(f"\n== {name} | {'own and loosened forms' if loose else 'own forms'} | Septuagint (usable {a['usable']})")
        for x in a["top"]: print(f"   {x['n']:2} {x['start']} – {x['end'].split()[-1]}  {x['members']}")
        print(f"   New Testament outside Revelation (usable {b['usable']})")
        for x in b["top"]: print(f"   {x['n']:2} {x['start']} – {x['end'].split()[-1]}  {x['members']}")
# (b) named checks
def grep(rx, corp, books=None, n=12):
    c = re.compile(rx); return [r for b, vs in corp.items() if not books or b in books for r, t in vs if c.search(t)][:n]
def show(ref, corp):
    for b, vs in corp.items():
        for r, t in vs:
            if r == ref: return t
CH = collections.OrderedDict()
CH["after three days (μετὰ τρεῖς ἡμέρας), NT"] = grep(r"μετα (τασ )?τρεισ ημερασ", NT)
CH["on the third day (τῇ τρίτῃ ἡμέρᾳ / τῇ ἡμέρᾳ τῇ τρίτῃ), NT"] = grep(r"τη τριτη ημερα|τη ημερα τη τριτη", NT, n=20)
CH["three years and six months, NT"] = grep(r"ετη τρια και μηνασ εξ|ενιαυτουσ τρεισ και μηνασ εξ", NT)
CH["three years and six months, LXX"] = grep(r"ετη τρια και μηνασ εξ|ενιαυτουσ τρεισ και μηνασ εξ", LXX)
CH["Lord with crucify in one verse, NT"] = grep(r"κυρι\w+.{0,60}σταυρ|σταυρ.{0,60}κυρι", NT)
CH["outside the city / gate / camp, NT"] = grep(r"εξω(θεν)? τησ (πολεωσ|πυλησ|παρεμβολησ)", NT)
CH["kingdom(s) of the world, NT+LXX"] = grep(r"βασιλει\w+ του κοσμου", NT) + grep(r"βασιλει\w+ του κοσμου", LXX)
CH["a woman when she bears, NT"] = grep(r"γυν\w+.{0,40}οταν τ(ικτη|εκη)", NT)
CH["ruler of this world, NT"] = grep(r"αρχων του κοσμου", NT)
CH["voice from heaven, John"] = grep(r"φωνη εκ του ουρανου", NT, {"John"})
CH["signs great from heaven, NT"] = grep(r"ουρανου σημεια μεγαλα|σημει\w+ μεγαλ\w+", NT)
CH["veil of the temple, NT"] = grep(r"καταπετασμα", NT)
CH["tombs opened, NT+LXX"] = grep(r"μνημ\w+ ανεωχθησαν|ανοιγω (υμων )?τα μνηματα", NT) + grep(r"ανοιγω (υμων )?τα μνηματα|ανοιξαι με τουσ ταφουσ", LXX)
for k, v in CH.items(): print(f"\n{k}: {v}")
TX = {}
for ref, corp in (("Ἰεζεκιήλ 37:5", LXX), ("Ἰεζεκιήλ 37:7", LXX), ("Ἰεζεκιήλ 37:10", LXX), ("Ἰεζεκιήλ 37:12", LXX), ("Ἰεζεκιήλ 38:19", LXX), ("Βασιλειῶν_Γʹ 18:1", LXX), ("Βασιλειῶν_Γʹ 19:18", LXX), ("Μαλαχίας 4:5", LXX), ("Ζαχαρίας 4:3", LXX), ("Ζαχαρίας 4:14", LXX), ("Ψαλμοί 78:2", LXX), ("Ψαλμοί 78:3", LXX), ("Ἐσθήρ 9:19", LXX), ("Βασιλειῶν_Δʹ 2:11", LXX),
                  ("Matt 27:51", NT), ("Matt 27:52", NT), ("Matt 27:53", NT), ("Matt 4:8", NT), ("Luke 4:25", NT), ("Jas 5:17", NT), ("Luke 21:24", NT), ("1Cor 2:8", NT), ("Heb 13:12", NT), ("John 12:25", NT), ("John 12:28", NT), ("John 12:29", NT), ("John 12:31", NT), ("John 12:32", NT), ("John 14:2", NT), ("John 16:20", NT), ("John 16:21", NT), ("Luke 10:18", NT), ("Mark 15:45", NT), ("Mark 6:29", NT), ("Acts 7:58", NT), ("Rom 11:4", NT), ("Matt 2:13", NT), ("Luke 1:33", NT), ("Acts 1:9", NT)):
    TX[ref] = show(ref, corp); print(f"\n{ref}: {TX[ref]}")
json.dump(dict(landing=OUT, checks=CH, texts=TX), open(sys.argv[4], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
