#!/usr/bin/env python3
"""Revelation 20:1-10 whole, as 11-12 were (2L): every member, own form and loosened; searched in the four Gospels, Acts, the letters and the Septuagint.
For each hit in Luke, whether Mark or Matthew has the member too (Luke's alone or not). The loosened forms were written with a reviewer's direction in
view (Luke's own material; captivity, release, authority), so they are by reading and are reported apart.
   python3 rev20.py <alexanarch root> <engine dir> out.json"""
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
NT, LXX = load("gnt-nestle1904"), load("lxx-swete"); rev = dict(NT["Rev"])
M = [
("20:1","angel-down","an angel coming down from heaven",r"αγγελ\w+ (\w+ ){0,2}καταβ\w+ (εκ του|εξ) ουρανου",None),
("20:1","key","the key of the abyss",r"κλειν τησ αβυσσου",r"κλει(ν|δα|δασ|σ) τ(ησ|ου) "),
("20:1","chain","a great chain",r"\bαλυσ",None),
("20:2","seized","he seized",r"εκρατησ",None),
("20:2","dragon","the dragon",r"δρακοντ",None),
("20:2","serpent","the ancient serpent",r"οφισ ο αρχαιοσ",r"\bοφ(ισ|εων|εισ|ιν)\b"),
("20:2","devil","the Devil",r"διαβολ",None),
("20:2","satan","Satan",r"σαταν",None),
("20:2","bound","bound him",r"\bεδησεν",r"δησ(η|αι|ατε|αντεσ)|δεδε|εδεσμ"),
("20:2","thousand-years","a thousand years",r"χιλια ετη",None),
("20:3","into-abyss","cast him into the abyss",r"εισ την αβυσσον",None),
("20:3","shut","shut",r"\bεκλεισεν",r"εκλεισθη|κλεισ(ασ|ητε|αι)|κλειετε"),
("20:3","sealed","sealed over him",r"εσφραγισεν",r"σφραγισ"),
("20:3","over","over him",r"επανω αυτου",None),
("20:3","deceive","that he deceive the nations no more",r"πλανηση",r"\bπλαν"),
("20:3","must-loose","must be loosed",r"δει λυθηναι",r"δει \w+ λυθηναι"),
("20:3","little-time","a little time",r"μικρον χρονον",r"χρονον μικρον"),
("20:4","thrones","thrones, and they sat on them",r"θρονουσ και εκαθισαν",r"καθ\w+ επι (δωδεκα )?θρον"),
("20:4","judgment-given","judgment was given to them",r"κριμα εδοθη",r"κρινοντεσ τασ"),
("20:4","beheaded","those beheaded",r"πεπελεκισμεν",r"απεκεφαλισ"),
("20:4","testimony","for the testimony of Jesus",r"μαρτυριαν ιησου",None),
("20:4","mark","the mark on forehead and hand",r"χαραγμα",None),
("20:4","lived-reigned","they lived and reigned with the Christ",r"εζησαν και εβασιλευσαν",r"συμβασιλευσ"),
("20:5","rest-dead","the rest of the dead",r"λοιποι των νεκρων",None),
("20:5","first-resurrection","the first resurrection",r"αναστασισ η πρωτη",r"αναστασ\w+ (των δικαιων|ζωησ)"),
("20:6","blessed-holy","blessed and holy",r"μακαριοσ και αγιοσ",None),
("20:6","has-part","who has a part",r"εχων μεροσ",r"εχεισ μεροσ"),
("20:6","second-death","the second death has no authority",r"δευτεροσ θανατοσ",None),
("20:6","priests","priests of God and of the Christ",r"ιερεισ του θεου",None),
("20:6","reign-with","they will reign with him",r"βασιλευσουσιν μετ αυτου",None),
("20:7","loosed-prison","Satan loosed from his prison",r"λυθησεται ο σατανασ",r"εκ (τησ )?φυλακησ"),
("20:8","go-out-deceive","will go out to deceive",r"εξελευσεται πλανησαι",None),
("20:8","four-corners","the four corners of the earth",r"τεσσαρσιν γωνιαισ",r"τεσσαρων ανεμων"),
("20:8","gog","Gog and Magog",r"\bγωγ\b",None),
("20:8","gather-war","to gather them to the war",r"συναγαγειν αυτουσ εισ τον πολεμον",None),
("20:8","sand","as the sand of the sea",r"αμμοσ τησ θαλασσησ",None),
("20:9","breadth","went up over the breadth of the earth",r"πλατοσ τησ γησ",None),
("20:9","surrounded","surrounded the camp of the holy ones",r"εκυκλευσαν την παρεμβολην",r"κυκλουμενην υπο στρατοπεδων|περικυκλωσ"),
("20:9","beloved-city","the beloved city",r"πολιν την ηγαπημενην",None),
("20:9","fire-heaven","fire came down from heaven and devoured",r"κατεβη πυρ εκ του ουρανου",r"πυρ καταβηναι απο του ουρανου|πυρ.{0,30}απ ουρανου"),
("20:10","lake","the lake of fire and brimstone",r"λιμνην του πυροσ και θειου",r"πυρ και θειον"),
("20:10","false-prophet","the false prophet",r"ψευδοπροφητησ",r"ψευδοπροφητ"),
("20:10","tormented","tormented day and night",r"βασανισθησονται",r"βασαν"),
("20:10","ever","for ever and ever",r"εισ τουσ αιωνασ των αιωνων",None),
]
GOS = ["Matt", "Mark", "Luke", "John"]; rows, bad = [], []
def find(rx):
    c = re.compile(rx); o = {g: [r for r, t in NT[g] if c.search(t)] for g in GOS}
    o["acts"] = [r for r, t in NT["Acts"] if c.search(t)]; o["letters"] = [r for b, vs in NT.items() if b not in GOS + ["Acts", "Rev"] for r, t in vs if c.search(t)]; o["lxx"] = sum(1 for b, vs in LXX.items() for r, t in vs if c.search(t)); return o
for v, mid, gloss, rx, rx2 in M:
    if not re.search(rx, rev["Rev " + v]): bad.append((v, mid))
    rows.append(dict(verse=v, id=mid, gloss=gloss, own=find(rx), loose=find(rx2) if rx2 else None))
print("members of Rev 20:1-10:", len(rows), "| not found in own verse:", bad or "none")
def anyg(o): return any(o[g] for g in GOS)
print("own form: in a Gospel", sum(1 for r in rows if anyg(r["own"])), "| in the Septuagint and no Gospel", sum(1 for r in rows if not anyg(r["own"]) and r["own"]["lxx"]), "| Revelation only", sum(1 for r in rows if not anyg(r["own"]) and not r["own"]["lxx"] and not r["own"]["acts"] and not r["own"]["letters"]))
cnt = collections.Counter(); lonly = []
for r in rows:
    for form in ("own", "loose"):
        o = r[form]
        if not o: continue
        for g in GOS:
            if o[g]: cnt[(form, g)] += 1
        if o["Luke"] and not o["Mark"] and not o["Matt"]: lonly.append((r["verse"], r["id"], form, [x.split()[1] for x in o["Luke"]][:5]))
        for g in ("Matt", "Mark", "John"):
            if o[g] and not any(o[h] for h in GOS if h != g): cnt[(form, g + " alone")] += 1
    def sh(x, n=5): return ",".join(a.split()[1] for a in x[:n]) + ("…" if len(x) > n else "") if x else "—"
    o = r["own"]; l = r["loose"]
    print(f"{r['verse']:6} {r['id']:18} own: Mt {sh(o['Matt'])} | Mk {sh(o['Mark'])} | Lk {sh(o['Luke'])} | Jn {sh(o['John'])} | Acts {sh(o['acts'],3)} | letters {len(o['letters'])} | LXX {o['lxx']}" + (f"   ||  loosened: Mt {sh(l['Matt'])} | Mk {sh(l['Mark'])} | Lk {sh(l['Luke'])} | Jn {sh(l['John'])} | LXX {l['lxx']}" if l else ""))
print("\nmembers with a hit, by Gospel:", {f"{a} {b}": c for (a, b), c in sorted(cnt.items())})
print("in Luke and in neither Mark nor Matthew:", lonly)
# landing: 40 verses
def land(corpus, loose, cap):
    mem = []
    for v, mid, gloss, rx, rx2 in M:
        cs = [re.compile(rx)] + ([re.compile(rx2)] if loose and rx2 else []); h = {(b, i) for b, vs in corpus.items() for i, (_, t) in enumerate(vs) if any(c.search(t) for c in cs)}
        if h and len(h) <= cap: mem.append((mid, h))
    sc = []
    for b, vs in corpus.items():
        for i in range(0, max(1, len(vs) - 39)):
            got = sorted(m for m, h in mem if any((b, j) in h for j in range(i, min(len(vs), i + 40))))
            if len(got) >= 2: sc.append((len(got), b, i, got))
    sc.sort(key=lambda x: -x[0]); out, used = [], []
    for n, b, i, got in sc:
        if all(not (b == ub and abs(i - ui) < 40) for ub, ui in used): used.append((b, i)); out.append((n, corpus[b][i][0], corpus[b][min(len(corpus[b]), i + 40) - 1][0].split()[-1], got))
        if len(out) == 7: break
    return out
NTX = collections.OrderedDict((b, v) for b, v in NT.items() if b != "Rev")
for loose in (False, True):
    print(f"\nwhere 20:1-10 lands, {'own and loosened' if loose else 'own'} forms | New Testament:"); [print("   ", x) for x in land(NTX, loose, 30)]
    print("   Septuagint:"); [print("   ", x) for x in land(LXX, loose, 60)[:4]]
json.dump(dict(rows=rows, luke_only=lonly, counts={f"{a} {b}": c for (a, b), c in cnt.items()}), open(sys.argv[3], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
