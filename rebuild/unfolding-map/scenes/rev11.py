import re, unicodedata, pathlib, json
C = pathlib.Path("/home/claude/repos/alexanarch/data/corpora/gnt-nestle1904/text")
def norm(s):
    s = unicodedata.normalize("NFD", s); s = "".join(c for c in s if not unicodedata.combining(c)).lower().replace("ς", "σ"); return re.sub(r"[^α-ω ]+", " ", s)
V = {p.stem: [(l.split("\t")[0], norm(l.split("\t", 1)[1])) for l in p.read_text(encoding="utf-8").splitlines() if "\t" in l] for p in C.glob("*.txt")}
RANGE = {"Matt": (27, 32, 28, 10), "Mark": (15, 21, 16, 8), "Luke": (23, 26, 24, 12), "John": (19, 16, 20, 18)}
def inr(g, ref):
    c, v = map(int, ref.split()[1].split(":")); a = RANGE[g]; return (a[0], a[1]) <= (c, v) <= (a[2], a[3])
M = [("the great city … where their Lord was crucified", r"πολεωσ.{0,60}οπου.{0,30}εσταυρωθη", r"πολεωσ οπου εσταυρωθη|οπου εσταυρωθη"),
     ("killed, and the body lying unburied / laid in a tomb (μνῆμα)", r"τεθηναι εισ μνημα", r"\bμνημα(τι)?\b"),
     ("three days (and a half)", r"ημερασ τρεισ|τρεισ ημερασ", r"ημερασ τρεισ|τρεισ ημερασ|τρισιν ημεραισ|τριτη ημερα"),
     ("those who watch (θεωρέω)", r"θεωρ", r"θεωρ"),
     ("great fear fell on them (φόβος μέγας)", r"φοβοσ μεγασ", r"φοβο\w* μεγα|εφοβηθησαν (φοβον μεγαν|σφοδρα)|φοβου και χαρασ μεγαλησ"),
     ("stood on their feet / rose", r"εστησαν επι τουσ ποδασ", r"ηγερθη|ανεστη|εκρατησαν αυτου τουσ ποδασ"),
     ("a great voice", r"φωνη\w* μεγαλη", r"φων\w+ μεγαλ"),
     ("a great earthquake (σεισμὸς μέγας)", r"σεισμοσ μεγασ", r"σεισμο\w* (εγενετο )?μεγα|εσεισθη"),
     ("the rest became afraid", r"λοιποι εμφοβοι", r"εμφοβ|εφοβηθησαν"),
     ("gave glory to God", r"εδωκαν δοξαν τω θεω", r"εδοξα\w+ τον θεον|δοξαν τω θεω"),
     ("the holy city (11:2)", r"πολιν την αγιαν", r"αγιαν πολιν|πολιν την αγιαν")]
rev = " ".join(t for r, t in V["Rev"] if r.split()[1].split(":")[0] == "11")
print(f"{'member of Rev 11:2–13':62}{'Rev 11':>7}" + "".join(f"{g:>22}" for g in RANGE))
out = []
for name, rrx, grx in M:
    row = {g: [r.split()[1] for r, t in V[g] if inr(g, r) and re.search(grx, t)] for g in RANGE}
    print(f"{name:62}{'yes' if re.search(rrx, rev) else 'NO':>7}" + "".join(f"{', '.join(row[g][:4]) or '—':>22}" for g in RANGE)); out.append({"member": name, "in_rev11": bool(re.search(rrx, rev)), **row})
json.dump(out, open("rev11.json", "w"), ensure_ascii=False, indent=1)
def where(rx): return [r for b in V for r, t in V[b] if re.search(rx, t)]
for k, rx in (("ἁγία πόλις", r"αγιαν πολιν|πολιν την αγιαν|πολεωσ τησ αγιασ|αγια πολισ"), ("ἔδωκαν/δοῦναι δόξαν τῷ θεῷ", r"(εδωκ\w+|δουναι|δοτε|δοσ) (αυτω )?δοξαν( τω θεω)?"), ("ἐδόξαζεν/ἐδόξασαν τὸν θεόν at the cross", r"εδοξα\w+ τον θεον"), ("ἔμφοβοι", r"εμφοβ"), ("μνῆμα", r"\bμνημα(τι|τοσ|σιν)?\b"), ("φόβος μέγας", r"φοβοσ μεγασ|φοβον μεγαν")):
    print(k, sorted(where(rx), key=lambda r: (r.split()[0], [int(x) for x in r.split()[1].split(":")])))
