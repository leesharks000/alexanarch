#!/usr/bin/env python3
"""EA-CORPORA-36 cross-references: the strata of #1548 Part II and the witnesses of fr. 31 that the library already holds, entered by
reference to the seat that holds them, each locus asserted present (whitespace-normalized) in the seated text and the text's sha256
recorded. Nothing is re-seated.   python3 rebuild/corpora/ea-corpora-36/xref36.py  -> rebuild/corpora/ea-corpora-36/xref36.json"""
import hashlib, json, pathlib
H = pathlib.Path(__file__).resolve().parent; ROOT = H.parents[2]; C = ROOT / "data/corpora"
X = [
 # fr. 31 and its witnesses
 ("sappho", "text/fr31-diplomatic.txt", "fr. 31.17 as Longinus carries it, the line every closure answers", "31.17	ἀλλὰ πᾶν τολματόν, ἐπεὶ καὶ πένητα", "Sappho's reception"),
 ("longinus", "text/DeSublimitate.txt", "[Longinus] 10.2: the sole carrier of fr. 31, breaking off in the fifth stanza", "ἀλλὰ πᾶν τολματόν, ἐπεὶ καὶ πένητ", "Sappho's reception"),
 ("catullus", "text/Catullus.txt", "Catullus 51, the Latin answer to fr. 31", "Ille mi par esse deo videtur", "Sappho's reception"),
 ("ovid", "text/heroides.txt", "Ovid, Heroides 15 (Sappho Phaoni), the epistle Pope renders (36/04): the letter known by its hand", "Ecquid, ut adspecta est studiosae littera dextrae", "Sappho's reception"),
 # stratum II: archaic kleos-futurity
 ("homer", "text/tlg001-Iliad.txt", "Il. 6.357–58, Helen: a subject of song for men to come", "ἀνθρώποισι πελώμεθʼ ἀοίδιμοι ἐσσομένοισι", "II. kleos-futurity"),
 ("homer", "text/tlg002-Odyssey.txt", "Od. 8.579–80, Alcinous: ruin spun so that there be song for those to come", "ἵνα ᾖσι καὶ ἐσσομένοισιν ἀοιδή", "II. kleos-futurity"),
 # stratum III: the prose charter and its counter-theory
 ("herodotus", "text/book-01.txt", "Herodotus, proem: that what men have done not fade with time", "τῷ χρόνῳ ἐξίτηλα γένηται", "III. prose charter"),
 ("thucydides", "text/book-01.txt", "Thucydides 1.22.4: a possession for all time, set against the prize-piece for the moment's hearing", "κτῆμά τε ἐς αἰεὶ μᾶλλον ἢ ἀγώνισμα ἐς τὸ παραχρῆμα ἀκούειν ξύγκειται", "III. prose charter"),
 ("plato", "text/tlg012-Φαῖδρος.txt", "Phaedrus 275d–e: writing rolls about everywhere, among those who understand and those it does not concern", "κυλινδεῖται μὲν πανταχοῦ πᾶς λόγος ὁμοίως παρὰ τοῖς ἐπαΐουσιν", "III. counter-theory"),
 # stratum IV: the Roman monumentum
 ("horace", "text/carmina.txt", "Horace, Odes 3.30: a monument more lasting than bronze", "Exegi monumentum aere perennius", "IV. monumentum"),
 ("horace", "text/carmina.txt", "Horace, Odes 3.30.6: I shall not wholly die", "non omnis moriar", "IV. monumentum"),
 ("ovid", "text/metamorphoses.txt", "Ovid, Met. 15.878–79: I shall be read in the mouth of the people, and I shall live", "ore legar populi, perque omnia saecula fama,", "IV. monumentum"),
 ("ovid", "text/amores.txt", "Ovid, Amores 1.15.42: I shall live, and the greater part of me survive", "Vivam, parsque mei multa superstes erit.", "IV. monumentum"),
 # stratum V: scriptural futurity (the Westminster Leningrad Codex; Hebrew versification)
 ("hebrew-wlc", "text/Ps.txt", "Ps. 102:19 (Eng. 102:18): written for a later generation, a people yet to be created", "@Ps 102:19", "V. scriptural futurity"),
 ("hebrew-wlc", "text/Deut.txt", "Deut. 29:13–14 (Eng. 29:14–15): the covenant with whoever is not here with us today", "@Deut 29:14", "V. scriptural futurity"),
 ("hebrew-wlc", "text/Isa.txt", "Isa. 30:8: write it on a tablet, for the latter day, a witness for ever", "@Isa 30:8", "V. scriptural futurity"),
 ("hebrew-wlc", "text/Hab.txt", "Hab. 2:2–3: write the vision plain on tablets, that a reader may run; it awaits its time", "@Hab 2:2", "V. scriptural futurity"),
 ("hebrew-wlc", "text/Dan.txt", "Dan. 12:4: seal the book until the time of the end", "@Dan 12:4", "V. scriptural futurity"),
 # stratum VII and VIII
 ("nietzsche", "text/ecce-homo-pg.txt", "Nietzsche, Ecce Homo: some are born posthumously", "Ich selber bin noch nicht an der Zeit, Einige werden posthum geboren", "VII. posterity"),
 ("whitman", "text/LG1891.txt", "Whitman, Crossing Brooklyn Ferry (LG 1891–92)", "I am with you, you men and women of a generation, or ever so many generations hence,", "VIII. engineers of address"),
 ("whitman", "text/LG1891.txt", "Whitman, Full of Life Now (LG 1891–92)", "When you read these I that was visible", "VIII. engineers of address"),
 ("whitman", "text/LG1891.txt", "Whitman, Poets to Come (LG 1891–92)", "POETS to come! orators, singers, musicians to come!", "VIII. engineers of address"),
]
norm = lambda s: " ".join(s.split())
out = []
for corpus, text, label, find, stratum in X:
    p = C / corpus / text
    t = p.read_text(encoding="utf-8", errors="replace")
    if find.startswith("@"):   # a verse of the WLC seat, entered by reference: the verse's text as seated is the locus
        ref = find[1:]; find = next(l.split("\t", 1)[1] for l in t.splitlines() if l.startswith(ref + "\t")); label = f"{label} [{ref}]"
    assert norm(find) in norm(t), (corpus, find)
    s = json.loads((C / corpus / "source.json").read_text(encoding="utf-8"))
    out.append({"stratum": stratum, "label": label, "corpus": corpus, "seat": s.get("seat") or s.get("seat_id"), "axn": s.get("axn"),
                "text": text, "find": find, "text_sha256": hashlib.sha256(p.read_bytes()).hexdigest(),
                "url": f"https://www.alexanarch.org/data/corpora/{corpus}/{text}"})
    print("ok", corpus, text, find[:40])
(H / "xref36.json").write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(len(out), "cross-references")
