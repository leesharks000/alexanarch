import re, unicodedata, pathlib, collections, sys
C = pathlib.Path("/home/claude/repos/alexanarch/data/corpora/gnt-nestle1904/text")
def norm(s):
    s = unicodedata.normalize("NFD", s); s = "".join(c for c in s if not unicodedata.combining(c)).lower().replace("ς", "σ"); return re.sub(r"[^α-ω ]+", " ", s)
V = [(l.split("\t")[0], norm(l.split("\t", 1)[1])) for p in sorted(C.glob("*.txt")) for l in p.read_text(encoding="utf-8").splitlines() if "\t" in l]
def where(rx): return [r for r, t in V if re.search(rx, t)]
P = {"μεγιστᾶνες": r"μεγιστα", "χιλίαρχ-": r"χιλιαρχ", "Ἑβραϊστί": r"εβραιστι", "ὅπου … ἐσταυρώθη": r"οπου .{0,40}εσταυρωθη", "στολ- λευκ-": r"στολ\w+ λευκ", "περιβεβλημέν- … στολ": r"περιβεβλημεν\w+ στολ",
     "ἐν λευκοῖς (bare)": r"\bεν λευκοισ\b", "στρατεύματ-": r"στρατευμα", "ληνό-": r"\bληνο", "ὑπολήνιον": r"υποληνι", "κλητοί + ἐκλεκτοί": r"κλητοι.*εκλεκτοι", "μέλλ- πάσχειν": r"μελλ\w+ πασχειν",
     "καιρὸς … ἐγγύς": r"καιροσ (γαρ |μου )?εγγυσ", "σκορπί-": r"σκορπι", "ἀδικήσ-": r"αδικησ", "τηρέω ἐκ": r"τηρησ\w+ (αυτουσ )?εκ\b", "γίνου πιστός / ἄπιστος": r"γινου (πιστοσ|απιστοσ)", "ὡς νεκρ-": r"ωσ(ει)? νεκρο",
     "σάλπιγγ- (Gospels)": r"σαλπι", "λαμπρ-": r"λαμπρ", "δεῖπνον μέγα / τὸ μέγα": r"δειπνον (το )?μεγα", "ἐκράτησεν … ἔδησεν": r"(ε)?κρατησ\w* .{0,40}εδησεν", "ἀνοῖξ- … βιβλίον": r"ανοιξ\w+ (το )?βιβλιον|ηνοιξεν (το )?βιβλιον", "ἐξουσίαν ἐπὶ (authority over)": r"εξουσιαν επι\b|εξουσιαν επανω",
     "ἔδωκεν/δώσω … ἐξουσίαν": r"(εδωκεν|δωσω|διδωμι|δεδωκα)\w* (αυτω |αυτοισ |σοι |υμιν )?(την )?(δυναμιν και )?εξουσιαν", "ἔνδυμα": r"ενδυμα", "ἑτοιμ- (prepared: bride/supper)": r"γαμ\w+.{0,60}ητοιμα|ητοιμα\w+.{0,60}γαμ", "ὀνόματα … γεγραμ-/ἐγγέγραπται (heaven/book)": r"ονομα\w* .{0,30}(ε[νγ])?γεγραπται|ονομα\w* .{0,20}γεγραμμεν"}
G = ("Matt", "Mark", "Luke", "John")
for k, rx in P.items():
    w = where(rx); g = [r for r in w if r.split()[0] in G]; rv = [r for r in w if r.startswith("Rev")]; o = [r for r in w if r.split()[0] not in G and not r.startswith("Rev")]
    print(f"{k:38} Gospels {g[:9]}{'…' if len(g)>9 else ''} | Rev {rv[:7]}{'…' if len(rv)>7 else ''} | other {len(o)} {[x for x in o[:4]]}")
# special vocabulary: stems (5 letters, words of 4+) found in one Gospel alone of the four; what share of them stands in each comparison book
def stems(t): return {w[:5] for w in t.split() if len(w) >= 4}
B = collections.defaultdict(set); T = collections.Counter()
for r, t in V: B[r.split()[0]] |= stems(t); T[r.split()[0]] += len(t.split())
print()
comp = ["Rev", "Acts", "Rom", "1Cor", "Heb", "Jas", "1Pet"]
print(f"{'special stems of':18}{'n':>6}" + "".join(f"{c:>8}" for c in comp) + "   (share of the Gospel's special stems found in the book, %)")
rows = {}
for g in G:
    E = B[g] - set().union(*[B[h] for h in G if h != g]); rows[g] = [100 * len(E & B[c]) / len(E) for c in comp]
    print(f"{g:18}{len(E):>6}" + "".join(f"{x:>8.1f}" for x in rows[g]))
print(f"{'book vocabulary':18}{'':>6}" + "".join(f"{len(B[c]):>8}" for c in comp))
print("ratio to Acts (same Gospel):", {g: round(rows[g][0] / rows[g][1], 2) for g in G}, "| ratio to Romans:", {g: round(rows[g][0] / rows[g][2], 2) for g in G})
