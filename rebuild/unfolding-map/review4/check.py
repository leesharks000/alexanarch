#!/usr/bin/env python3
"""Two reviews of v0.21 (the author, 17:43): the three expansions against multi-source scriptural controls, the residue of Matt 22 against Luke 14,
and the keys tried from Daniel. This script fetches verses and counts where a wording stands; the reading is in the file.
   python3 check.py <alexanarch root> <engine dir> out.json"""
import sys, re, json, pathlib, unicodedata
sys.path.insert(0, sys.argv[2]); import midrash as E
root = pathlib.Path(sys.argv[1]) / "data/corpora"
def sq(s): return re.sub(r"\s+", " ", E.norm(s)).strip()
def load(corpus):
    out = []
    for p in sorted((root / corpus / "text").glob("*.txt")):
        seen = set()
        for l in p.read_text(encoding="utf-8", errors="ignore").splitlines():
            if "\t" in l:
                r, t = l.split("\t", 1); r = r.strip()
                if re.search(r"\d+:\d+$", r) and r not in seen: seen.add(r); out.append((p.stem + "|" + r, sq(t)))
    return out
NT = [(r.split("|")[1], t) for r, t in load("gnt-nestle1904")]; LXX = load("lxx-swete"); D = dict(NT); OUT = {}
def lx(book, ch, a, b):
    return [(r, t) for r, t in LXX if sq(book) in sq(r) and (m := re.search(r"(\d+):(\d+)$", r)) and int(m[1]) == ch and a <= int(m[2]) <= b]
def nt(book, ch, a, b): return [(f"{book} {ch}:{v}", D[f"{book} {ch}:{v}"]) for v in range(a, b + 1) if f"{book} {ch}:{v}" in D]
def held(vs, mem):
    txt = " ".join(t for _, t in vs); return {k: len(re.findall(rx, txt)) for k, rx in mem.items()}
def count(lab, rx, show=8):
    c = re.compile(rx); a = [r for r, t in NT if c.search(t)]; b = [r.split("|")[1] for r, t in LXX if c.search(t)]
    OUT[lab] = dict(nt=a, lxx=b[:12], lxx_n=len(b)); print(f"  {lab}: NT {a[:show]} | LXX {len(b)} {b[:5]}")
print("== A. John 4: scriptural siblings, one by one and all together")
J = dict(thirst="διψ", give=r"\bδωσ[ωε]", spring="πηγ", water="υδατ|υδωρ", life=r"\bζω(η|ησ|ην)\b", gift="δωρεα", hour=r"\bωρα\b", worship="προσκυν", woman=r"\bγυν")
S = {"Gen 24:11-20": lx("Γένεσις", 24, 11, 20), "Gen 29:1-12": lx("Γένεσις", 29, 1, 12), "Exod 2:15-21": lx("Ἔξοδος", 2, 15, 21), "Exod 17:1-7": lx("Ἔξοδος", 17, 1, 7), "Num 21:16-18": lx("Ἀριθμοί", 21, 16, 18),
     "Isa 12:3": lx("Ἠσαΐας", 12, 3, 4), "Isa 49:10": lx("Ἠσαΐας", 49, 10, 10), "Isa 55:1-3": lx("Ἠσαΐας", 55, 1, 3), "Jer 2:13": lx("Ἱερεμίας", 2, 13, 13), "Jer 17:13": lx("Ἱερεμίας", 17, 13, 13), "Zech 14:8": lx("Ζαχαρίας", 14, 8, 9),
     "Ezek 47:1-12": lx("Ἰεζεκιήλ", 47, 1, 12), "Ps 35:9-10": lx("Ψαλμοί", 35, 9, 10), "Sir 24:21": lx("Ἐκκλησιαστικός", 24, 19, 22), "4 Kgdms 17:24-41": lx("Βασιλειῶν_Δʹ", 17, 24, 41), "Deut 12:5-14": lx("Δευτερονόμιον", 12, 5, 14)}
allv = []
for k, vs in S.items():
    h = held(vs, J); allv += vs; print(f"  {k:18} verses {len(vs):2} holds {sum(1 for v in h.values() if v)}/9  {dict((a, b) for a, b in h.items() if b)}")
h = held(allv, J); print("  ALL TOGETHER", sum(1 for v in h.values() if v), "/9", h); OUT["john4_union"] = h
h = held(nt("John", 4, 6, 24), J); print("  John 4:6-24", h); h = held(nt("Rev", 21, 6, 6) + nt("Rev", 14, 7, 7) + nt("Rev", 22, 17, 17) + nt("Rev", 7, 16, 17), J); print("  Rev 21:6+14:7+22:17+7:16-17", h)
for r in ("Sir",): [print("   ", a.split("|")[1], t[:200]) for a, t in S["Sir 24:21"]]
count("hour with worship, one verse", r"\bωρα\b.*προσκυν|προσκυν.*\bωρα\b"); count("spring(s) of water(s)", r"πηγ\w+ (των |του )?υδατ"); count("spring of water with life, one verse", r"πηγ\w+ (των |του )?υδατ.*\bζω|\bζω\w+ πηγ\w+ υδατ|πηγ\w+ \bζω")
count("gift (δωρεάν, δωρεά) with water, one verse", r"δωρεα.*υδ(ωρ|ατ)|υδ(ωρ|ατ).*δωρεα"); count("thirst with give, one verse", r"διψ.*\bδω[σ]|\bδω[σ]\w*.*διψ|διψ.*\bδοσ\b|\bδοσ\b.*διψ"); count("worship with spring, within a verse", r"προσκυν.*πηγ|πηγ.*προσκυν")
print("== B. The labourers: the wage and the first-and-last in Scripture")
count("wage with pay, one verse", r"μισθ.*αποδ[ιοω]|αποδ[ιοω]\w*.*μισθ"); count("wage with 'with him/me'", r"μισθοσ (μου|αυτου) μετ (εμου|αυτου)"); count("pay to each according to work(s)", r"αποδ\w+ εκαστω")
count("first with last (ἔσχατος), one verse", r"πρωτ.*εσχατ|εσχατ.*πρωτ", 30); count("the first and the last, as a name", r"πρωτοσ και (ο |εγω )?(ο )?εσχατοσ"); count("wage with first or last, one verse", r"μισθ.*(πρωτ|εσχατ)|(πρωτ|εσχατ).*μισθ")
for b, c, a, z in (("Ἠσαΐας", 40, 10, 10), ("Ἠσαΐας", 41, 4, 4), ("Ἠσαΐας", 44, 6, 6), ("Ἠσαΐας", 48, 12, 12), ("Ἠσαΐας", 62, 11, 11), ("Δευτερονόμιον", 24, 14, 15), ("Λευϊτικόν", 19, 13, 13)):
    for r, t in lx(b, c, a, z): print("   ", r.split("|")[1], t[:230])
for r in ("Matt 19:30", "Matt 20:8", "Matt 20:16", "Rev 22:12", "Rev 22:13", "Rev 2:23", "Mark 10:31", "Luke 13:30"): print("   ", r, D[r][:230])
print("== C. Matthew 22:1-14 against Luke 14:16-24: every feature Matthew has and Luke lacks")
for r, t in nt("Matt", 22, 1, 14): print("   ", r, t)
for r in ("Rev 19:7", "Rev 19:8", "Rev 19:17", "Rev 19:18", "Rev 3:4", "Rev 3:5", "Rev 16:15", "Rev 17:14", "Rev 19:16", "Rev 22:11", "Matt 21:35", "Matt 21:36", "Matt 21:41"): print("   ", r, D[r][:260])
for b, c, a, z in (("Παροιμίαι", 9, 1, 6), ("Σοφονίας", 1, 7, 8)):
    for r, t in lx(b, c, a, z): print("   ", r.split("|")[1], t[:260])
F = dict(king=r"βασιλε[ιυ]", son=r"\bυι[οω]", wedding="γαμ", called="κεκλημεν|κλητο|καλεσ", ready="ετοιμ|ητοιμασ", slaughtered="τεθυμενα|εθυσεν|εσφαξεν", insulted="υβρισ", killed="απεκτ|φονε", angry="ωργισθη", armies="στρατευμα", destroyed="απωλεσεν|απολ",
         burned="ενεπρησεν|κατακαυ", worthy="αξιο", gather="συνηγαγον|συναχθ", bad_good="πονηρ\w+ τε και αγαθ|αγαθ\w+.*πονηρ|πονηρ\w+.*αγαθ", filled="επλησθη|γεμισθη", garment="ενδυμα|βυσσιν|ιματι", friend="εταιρε", silent="εφιμωθη", bound="δησ", cast="βαλ", darkness="σκοτοσ",
         weeping="κλαυθμοσ", gnashing="βρυγμοσ", chosen="εκλεκτ", few="ολιγοι", many="πολλοι")
M, Lk = held(nt("Matt", 22, 1, 14), F), held(nt("Luke", 14, 16, 24), F); R = held(nt("Rev", 17, 14, 14) + nt("Rev", 18, 8, 8) + nt("Rev", 19, 7, 21) + nt("Rev", 20, 1, 3), F); R2 = held([x for x in NT if x[0].startswith("Rev ")], F)
print(f"   {'feature':12} Matt Luke Rev17:14;18:8;19:7-20:3  Rev-whole"); OUT["ledger"] = {}
for k in F: print(f"   {k:12} {M[k]:3} {Lk[k]:4} {R[k]:6} {R2[k]:10}"); OUT["ledger"][k] = [M[k], Lk[k], R[k], R2[k]]
count("weeping and gnashing of teeth", r"κλαυθμοσ και ο βρυγμοσ", 10); count("outer darkness", r"σκοτοσ το εξωτερον"); count("friend (ἑταῖρε)", r"εταιρε"); count("ready (ἕτοιμ-) with wedding or supper", r"(ετοιμ|ητοιμασ).*(γαμ|δειπν)|(γαμ|δειπν).*(ετοιμ|ητοιμασ)")
count("worthy with garments or called, one verse", r"αξιο.*(ιματι|κεκλημεν)|(ιματι|κεκλημεν).*αξιο"); count("called (κλητός) with garment, one verse", r"κλητ.*ενδυ|ενδυ.*κλητ")
print("== D. The keys from Daniel: wordings of Matthew that stand in Daniel")
DAN = [(r, t) for r, t in LXX if "Δανι" in r]; print("   Daniel verses seated:", len(DAN), sorted({r.split("|")[0] for r, _ in DAN}))
W = [("furnace of fire", r"καμινο\w+ του πυροσ"), ("will winnow, crush (λικμήσει)", r"λικμησει"), ("the righteous / wise shine out", r"εκλαμψουσιν"), ("eternal life", r"ζωην αιωνιον"), ("abomination of desolation", r"βδελυγμα (τησ |των )?ερημωσε"),
     ("affliction such as has not been", r"θλιψ\w+ (μεγαλη )?οια ου (γεγονεν|εγενηθη)"), ("authority was given", r"εδοθη (αυτω|μοι) (πασα )?(η )?εξουσια|εξουσια εδοθη"), ("all the nations", r"παντα τα εθνη"), ("son of man … clouds of heaven", r"νεφελων του ουρανου"),
     ("thrones set / sat on a throne", r"θρονοι ετεθησαν|καθισ\w+ επι (του )?θρονου|καθησεσθε.*επι.*θρονουσ"), ("birds of heaven lodge in branches", r"πετεινα του ουρανου.*(κατεσκην|κατασκην|κλαδ)|κλαδοισ αυτου.*πετειν"), ("sealed (the stone)", r"εσφραγισα\w+.*λιθ|λιθ\w+.*εσφραγισ|σφραγισαντεσ τον λιθον"),
     ("fell on the face", r"επεσ\w+ επι (το )?προσωπ\w+"), ("touched … (fear not / arise)", r"ηψατο (μου|αυτων)"), ("fear not", r"μη φοβ(ου|εισθε)"), ("face / appearance as lightning", r"(προσωπον|ειδεα|ορασισ) (αυτου )?ωσ(ει)? (ορασισ )?αστραπ"), ("white as snow", r"λευκ\w+ ωσ(ει)? χιων"),
     ("consummation (συντέλεια)", r"συντελεια"), ("mysteries", r"μυστηρι"), ("what must come to be", r"α δει γενεσθαι|δει (γαρ )?(παντα )?γενεσθαι"), ("scarlet", r"κοκκιν"), ("purple", r"πορφυρ"), ("reed", r"καλαμ"), ("deceive / deceiver", r"πλαν"), ("kingdoms of the world", r"βασιλειασ του κοσμου"), ("the holy city", r"αγιαν πολιν|πολιν την αγιαν|πολει τη αγια"), ("face as the sun", r"ωσ ο ηλιοσ")]
OUT["daniel"] = {}
for lab, rx in W:
    c = re.compile(rx); g = {b: [r for r, t in NT if r.startswith(b + " ") and c.search(t)] for b in ("Matt", "Mark", "Luke", "John", "Rev")}; d = sorted({re.sub(r".*\|", "", r) for r, t in DAN if c.search(t)})
    OUT["daniel"][lab] = dict(g, dan=d); print(f"   {lab:38} Matt {g['Matt'][:5]} Mark {len(g['Mark'])} Luke {len(g['Luke'])} John {len(g['John'])} | Rev {g['Rev'][:4]} | Dan {len(d)} {d[:4]}")
K = dict(throne="θρον", glory="δοξ", son_of_man="υιο\w+ (του )?ανθρωπου", nations="παντα τα εθνη", kingdom="βασιλει", fire=r"\bπυρ", eternal="αιωνι", judgment="κριτηρι|κρισ|κριμα", books="βιβλ", angels="αγγελ|μυριαδ|χιλιαδ", king=r"βασιλευσ\b", right="δεξι")
dv = [(r, t) for r, t in DAN if re.search(r"7:(9|1[0-4])$", r)]; print("   Dan 7:9-14 verses", len(dv)); print("   Dan 7:9-14      ", held(dv, K)); print("   Matt 25:31-46   ", held(nt("Matt", 25, 31, 46), K)); print("   Rev 20:11-15    ", held(nt("Rev", 20, 11, 15), K)); OUT["dan7_matt25"] = [held(dv, K), held(nt("Matt", 25, 31, 46), K), held(nt("Rev", 20, 11, 15), K)]
json.dump(OUT, open(sys.argv[3], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
