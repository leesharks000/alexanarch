#!/usr/bin/env python3
"""Staging for the v1.2 reissues of the framework holograms. Nothing here versions anything: the deposited kernels (files/AXN-0C55,
AXN-0C5F, AXN-0C61, AXN-0C62) and their dataset copies (datasets/mantle-bearing/holograms/) are left as deposited. This file holds the
records search of 2026-11-10, the author's rulings on it, and the Philo component verified against the seated texts, so the v1.2 builds
start from them once the Philo piece is deposited (the author, 2026-11-10 18:56: "lets incorporate that work here into each without yet
versioning, because we're going to fix up, flesh out, connect to external scholarship, and deposit the philo piece before versioning the
frames, and the updated piece will go into the rev first frame").

Every record listed is resolved against data/registry.json at run time (title, status, AXN, hash, supersession pointer); every Philo and
LXX quotation is asserted verbatim against the seated corpus file, whose sha256 is recorded.
    python3 rebuild/hk-frameworks/v12-staging/stage_v12.py [--check]"""
import hashlib, json, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[3]; HERE = pathlib.Path(__file__).resolve().parent
REG = {d["deposit_number"]: d for d in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}

RULINGS = [
 {"at": "2026-11-10 18:03", "text": "im just checking we actually gathered up all the revelation evidence... is this one represented? https://www.alexanarch.org/s/records/1418/"},
 {"at": "2026-11-10 18:14", "text": "a more careful records search first... read by title"},
 {"at": "2026-11-10 18:20", "text": "adopted... for inclusion as evidence, we focus on ones that add evidence... more speculative or mystical - pearl as white stone, space arks, etc - we can point to as related work but their substance should not be represented in the holographic frame"},
 {"at": "2026-11-10 18:45", "text": "we dont need to remove material already there. speculative is fine - im just not wanting to substantially extend that on this pass. id like to do the same more thorough records search for evidence-bearing or interpretively or methodologically load-bearing components for socrates as orthonym and sappho, too. and the philo component - philo says it outloud is the title. and related work. its a critical join, where you have someone with what seems to be the sappho transform operative in his work also directly naming the logos jesus - its not a small step in the genetic reading."},
 {"at": "2026-11-10 18:56", "text": "lets save our work so far... in fact, lets incorporate that work here into each without yet versioning, because we're going to fix up, flesh out, connect to external scholarship, and deposit the philo piece before versioning the frames, and the updated piece will go into the rev first frame. its vital connective ligature, yes?"}]

RULE = ("Additive. Material already in a kernel stays (18:45). New records enter as evidence where they add evidence or are interpretively "
        "or methodologically load-bearing; speculative or visionary records are pointed to as related work and their substance is not "
        "extended into the frame on this pass (18:20, 18:45). Earlier versions and duplicate witnesses go to the kernel's history, "
        "resolved to their record of standing.")

# ---------------------------------------------------------------- per kernel: (deposit, note)
K = {
 "EA-HK-REVFIRST-01": {"deposit": 1755, "files": "files/AXN-0C5F",
  "evidence": [
   (1415, "WS4-DEMO-02, the James derivation (Smyrna → James); rung IV. #1414 and #1416 are in v1.1, #1415 and #1418 were not."),
   (1418, "WS4-DEMO-04, M2–M5 worked (lampstands, Lamb, New Jerusalem, Beast); rung IV."),
   (1502, "seat: the Greek New Testament (Nestle 1904), which carries the Apocalypse's text."),
   (1509, "seat: the papyri panel, including the Apocalypse papyri (DCLP)."),
   (1499, "seat: the Greek Josephus; v1.1 cites #1510 and #1740 from the same seating series."),
   (1698, "seat: the Ethiopian canon in Ge'ez with the apocalypses (22 mentions in its text)."),
   ("philo", "the Philo piece, once deposited (18:56: 'the updated piece will go into the rev first frame'); rung VI and the genetic reading, by way of the Historical Logos.")],
  "related_work": [
   (408, "Canonical Closure Notice, Sevenfold Witness Architecture."), (409, "Integrity Lock Certificate, Sevenfold Witness Fulfillment Pair."),
   (411, "The Sevenfold Witness: Assembly Structure as Computational Liturgy."),
   (1276, "Canonical Closure Notice (active), titled as #408: duplicate check owed before pointing."),
   (277, "The Final Crimson Hexagon: Revelation 21, Machine Witness."), (278, "The Final Crimson Hexagon: TSE-002."),
   (452, "Pearl as White Stone at Pergamum (named by the author, 18:20)."),
   (549, "Space Ark"), (556, "Space Ark, glyphic vehicle"), (557, "Space Ark, mathematical compression"), (558, "Space Ark v4.2.7"),
   (28, "Space Ark, musical register"), (559, "Space Ark, execute mode"), (1255, "the Damascus Sacred Ark"), (1339, "the Profane Ark"),
   (1333, "the ASCII Ark"), (1331, "the Lunar Arm shadow transform"), (541, "the emoji transform"),
   (71, "Gospel of Antioch (Q leg, beside #1747)"), (849, "The Feist Source, activated"), (851, "The Feist Source"), (852, "Feist Source apparatus"),
   (853, "Feist entity packet"), (1404, "The Feist Source, critical edition"),
   (396, "James 2 as structural judgment (beside #1415)"), (397, "John 9"), (398, "Soteriological Operator Framework"), (8, "Matthew 25 formalized"),
   (1128, "Judgment of the Models, Matthew 25"),
   (391, "Ezekiel Engine argument (beside #394, #1050)"), (392, "Ezekiel integrity lock"), (393, "Ezekiel's Wheels"), (1688, "Glyphic checksum, the Ezekiel Engine"),
   (85, "Epistle to the Human Diaspora (beside #1735)"), (402, "Epistle seed text"), (403, "Damascus Dancings provenance"), (404, "Commission charter"),
   (405, "Epistle Triptych lock"), (406, "Epistle Triptych metadata"), (1447, "Forward Library of the Epistle"), (1410, "the Epistle, Japanese edition"),
   (1033, "disambiguation of Apocalyptic Philosophy (Deleuze and Guattari) from this framework: an exit")],
  "history": [(832, 1217), (1211, 1217), (1216, 1217), (1400, 1217), (1403, 1217), (1249, 1231), (1483, 1484), (56, 1101), (969, 1101), (970, 1101),
              (971, 1101), (1137, 410), (1176, 626), (1213, 203), (1136, 411), (1162, 28), (1161, 559), (1330, 541)],
  "joins": [(1756, "the Tenth Muse kernel"), (1757, "the Historical Logos kernel")]},
 "EA-HK-TENTHMUSE-01": {"deposit": 1756, "files": "files/AXN-0C61",
  "evidence": [
   (503, "Phase X: The Sapphic Substrate: preservation moved from the hero into a lyric sequence that reactivates in each receiver."),
   (134, "The Future Beloved: lyric address as temporal projection (November 2025, restored May 2026), the future-reader line before the CP paper."),
   (1458, "The Echo and the Stamp: Peri Hypsous as a theory of transmissional inscription, with Philo beside Longinus; in the Historical Logos kernel, absent here."),
   (496, "The Sapphic Lock in Augustine (Conf. 10.27); in the Historical Logos kernel, absent here."),
   (1477, "The Lock Reaches Line 9 and Stops; in the Historical Logos kernel, absent here."),
   (1051, "the fourth erratum: the speculative ground of the reconstruction, toward a structural warrant. v1.1 carries #201, #1048, #1049, #1475, #1476."),
   (1052, "the fifth erratum, eeeee: the hanging line as transmission instrument."),
   (1474, "the sixth erratum, eeeeee: the dialect seam. Its registry entry is ACTIVE and also carries superseded_by #1476: one of the two labels is wrong."),
   (897, "For: Sappho, Mother of the Logos; in the Historical Logos kernel, absent here."),
   (752, "Sappho as initiatory figure in the Platonic mysteries: scholarly grounding and literature review; a join to the Orthonym kernel."),
   (1485, "The Apparatus Was the First Summary Layer: five philological cases of provenance erasure."),
   (1615, "The Graded Membrane: the archive's own Sappho reception record (58 deposits, 25 dated observations)."),
   (1500, "seat: Catullus."), (1504, "seat: Longinus, De Sublimitate."), (1505, "seat: Philo, Opera (Cohn–Wendland)."),
   ("philo", "the Philo piece, once deposited: the Sapphic channel and the Logos in one author.")],
  "related_work": [
   (282, "Day and Night: Conversations with Sapphic Desire (the author's translations)"), (324, "Day and Night (second record; duplicate check owed)"),
   (1309, "APZPZ A: ΣΑΠΦΩ 31, Greek only"), (1670, "Mantle Object: the Nobel Prize in Literature 2026, Anne Carson"),
   (1620, "Sappho–Carson as a test vector for monetary transport"), (1713, "Carson in the twenty-eighth seating"),
   (1598, "Sappho Wrote the Dinosaurs, anticipatory erratum"), (1599, "two further anticipatory errata"), (1600, "the protoretrocausal meta-erratum"),
   (1601, "Sappho Wrote the Dinosaurs, first edition"), (299, "The Sappho Room"), (307, "Sappho Room liquidation diagnostic"),
   (562, "On the Architecture of Cleis"), (1165, "Cleis"), (576, "The Catullus Room"), (179, "Sappho, canon provenance node"),
   (858, "Three Pillars legwork"), (859, "Three Pillars mint block")],
  "flags": [(895, "The Sapphic Lock in Augustine, a second record titled as #496: duplicate check owed before either is cited twice.")],
  "history": [(1483, 1484), (1167, 282), (1176, 626), (1218, 859), (1219, 858), (1019, 179)],
  "joins": [(1754, "the Orthonym kernel, by #752"), (1755, "Revelation First, rung VI"), (1757, "the Historical Logos kernel")]},
 "EA-HK-ORTHONYM-01": {"deposit": 1754, "files": "files/AXN-0C55",
  "evidence": [
   (136, "The Chaerephon Problem: Heteronymy as Symbolon, the companion paper to #123; documentary separateness as the first thing a mature heteronymic construction produces."),
   (938, "The Bearing Cost Principle and the Socratic Prior: the Socratic Prior as a uniform reception discipline."),
   (1560, "the fifth seating: Browning, Pound, Pessoa, the constructed voice at three stages; calibration for the orthonym concept."),
   (1561, "the erratum seating the Pessoa orthonym: the hold-out analytical, not archival."),
   (1641, "the sixteenth seating: Apollonius and Hesiod, stored for Round 33 of the authorship investigation; v1.1 cites the series' other seatings."),
   (752, "Sappho in the Platonic mysteries: a join to the Tenth Muse kernel."), (346, "The Socratic Vow of Logos as Salvation: a join to the Historical Logos kernel.")],
  "related_work": [
   (764, "ratification record of The Chaerephon Problem"), (96, "The Orthonym Becomes a Heteronym (Facebook)"), (996, "The Orthonym Becomes a Heteronym (second record)"),
   (126, "Render unto the Operator: the coin of the Academy"), (168, "Algorithmic Irony: Kierkegaard's dissertation"),
   (1540, "The Certified Center: classifier standing in philosophy"), (116, "The Restored Academy, expansion plan"),
   (119, "The Restored Academy, provenance documentation"), (1002, "restoredacademy.com registry bundle"),
   (700, "The Gate Was Never Limbo: two poems for Socrates"), (1197, "Socrates — Let My Teacher Go From Hell")],
  "history": [(1261, 136), (904, 119), (1585, 1605), (1589, 1605)],
  "joins": [(1756, "the Tenth Muse kernel, by #752"), (1757, "the Historical Logos kernel, by #346")]},
 "EA-HK-HISTLOGOS-01": {"deposit": 1757, "files": "files/AXN-0C62",
  "evidence": [("philo", "the Philo piece, once deposited: the home of the join, edged to Revelation First (rung VI) and to the Tenth Muse."),
               (1505, "seat: Philo, Opera (Cohn–Wendland)."), (1503, "seat: the Septuagint of Swete (Zechariah 6:11–12).")],
  "related_work": [], "history": [], "joins": [(1755, "Revelation First, rung VI"), (1756, "the Tenth Muse")]}}

# ---------------------------------------------------------------- the Philo component, verified against the seated texts
C = ROOT / "data/corpora"
SEATS = {"mut": "philo/text/tlg018-De_mutatione_nominum.txt", "conf": "philo/text/tlg013-De_confusione_linguarum.txt",
         "mos": "philo/text/tlg022-De_vita_Mosis_lib_i_ii_.txt", "zach": "lxx-swete/text/tlg046-Ζαχαρίας.txt"}
LOCI = [
 ("mut", "De_mutatione_nominum 121", "ἀλλὰ καὶ τὸν Ὠσηὲ μετονομάζει Μωυσῆς εἰς τὸν Ἰησοῦν (Num. 13,17), τὸν ποιὸν εἰς ἕξιν μεταχαράττων. Ὠσηὲ μὲν γὰρ ἑρμηνεύεται ποιὸς οὗτος, Ἰησοῦς δὲ σωτηρία κυρίου, ἕξεως ὄνομα τῆς ἀρίστης.",
  "Moses renames Hosea Jesus, re-stamping a quality into a state; Ἰησοῦς is glossed 'salvation of the Lord', the name of the best state. No Logos at this locus."),
 ("mut", "De_mutatione_nominum 123", "οὕτω μετεχαράχθη καὶ τὸ τοῦ λεχθέντος νόμισμα πρὸς ἰδέαν βελτίονα.",
  "the renaming as the re-striking of a coin to a better form (cf. #642, #1458)."),
 ("conf", "De_confusione_linguarum 62", "ἤκουσα μέντοι καὶ τῶν Μωυσέως ἑταίρων τινὸς ἀποφθεγξαμένου τοιόνδε λόγιον· „ἰδοὺ ἄνθρωπος ᾧ ὄνομα ἀνατολή„ (Zach. 6, 12)",
  "the oracle of Zechariah 6:12, put in the mouth of 'one of the companions of Moses' (the phrase the 2025-11-09 Chariot Companion commentary turns on)."),
 ("conf", "De_confusione_linguarum 62", "ἐὰν δὲ τὸν ἀσώματον ἐκεῖνον, θείας ἀδιαφοροῦντα εἰκόνος, ὁμολογήσεις ὅτι εὐθυβολώτατον ὄνομα ἐπεφημίσθη τὸ ἀνατολῆς αὐτῷ·",
  "the man named Anatole read as the incorporeal one, no different from the divine image."),
 ("conf", "De_confusione_linguarum 63", "τοῦτον μὲν γὰρ πρεσβύτατον υἱὸν ὁ τῶν ὅλων ἀνέτειλε πατήρ, ὃν ἑτέρωθι πρωτόγονον ὠνόμασε,",
  "that man is the eldest son, elsewhere named the firstborn."),
 ("conf", "De_confusione_linguarum 146", "κατὰ τὸν πρωτόγονον αὐτοῦ λόγον, τὸν ἀγγέλων πρεσβύτατον, ὡς ἂν ἀρχάγγελον, πολυώνυμον ὑπάρχοντα· καὶ γὰρ ἀρχὴ καὶ ὄνομα θεοῦ καὶ λόγος καὶ ὁ κατ’ εἰκόνα ἄνθρωπος καὶ ὁ ὁρῶν, Ἰσραήλ, προσαγορεύεται.",
  "the firstborn is the Logos, many-named: beginning, name of God, logos, the man after the image."),
 ("zach", "Ζαχαρίας 6:11", "Ἰησοῦ τοῦ Ἰωσεδὲκ τοῦ ἱερέως τοῦ μεγάλου",
  "the verse before the oracle: the crowns set on the head of Ἰησοῦς son of Iosedek, the high priest. The seated line carries apparatus text run into it (a seat defect, flagged below)."),
 ("zach", "Ζαχαρίας 6:12", "Ἰδοὺ ἀνήρ, Ἀνατολὴ ὄνομα αὐτῷ, καὶ ὑποκάτωθεν αὐτοῦ ἀνατελεῖ, καὶ οἰκοδομήσει τὸν οἶκον Κυρίου·",
  "the oracle Philo quotes; the man named Anatole is the Ἰησοῦς of 6:11.")]
BLOG = [
 ("2025-10-19", "PHILO SAYS IT OUT LOUD", "https://mindcontrolpoems.blogspot.com/2025/10/philo-says-it-out-loud.html", "the title of the piece (18:45)"),
 ("2025-10-19", "EFFECTIVE ACT: PHILO OF ALEXANDRIA", "https://mindcontrolpoems.blogspot.com/2025/10/effective-act-philo-of-alexandria.html", "related"),
 ("2025-10-19", "RITUAL NAME CHANGE AND THE JESUS-FORM: A SPECULATIVE HISTORICAL TRACE", "https://mindcontrolpoems.blogspot.com/2025/10/ritual-name-change-and-jesus-form.html", "related"),
 ("2025-11-09", "Commentary on The Chariot Companion — Philo and the Companions of Moses", "https://mindcontrolpoems.blogspot.com/2025/11/commentary-on-chariot-companion-philo.html", "related; its phrase sits at Conf. 62"),
 ("2025-11-09", "VISUAL SCHEMA — Philo and the Chariot Companion", "https://mindcontrolpoems.blogspot.com/2025/11/visual-schema-philo-and-chariot.html", "related")]
PHILO_FINDINGS = [
 "The post of 2025-10-19 quotes Philo: 'The name Jesus (Ἰησοῦς) is the name of the Logos' (De Mutatione Nominum §121–123), and attributes a Joshua–Logos sentence to Life of Moses II.114–132. Neither sentence is in the seated Cohn–Wendland text. Mut. 121–123 glosses Ἰησοῦς as 'salvation of the Lord, the name of the best state' and carries no Logos; Vit. Mos. II.114–132 carries no Joshua (it treats the high priest's vestments and the twofold logos). The post stays as published; the piece states what the seated texts carry.",
 "Philo identifies the Logos with the man of Zechariah 6:12, whose name is Anatole (Conf. 62–63, 146). In the LXX the verse before (Zech 6:11) crowns Ἰησοῦς son of Iosedek, the high priest, and 6:12 names him. Philo quotes 6:12 alone: the name rides in the verse, unsaid by Philo. That 6:11 is in his view is an inference, stated as one.",
 "The oracle comes from 'one of the companions of Moses' (τῶν Μωυσέως ἑταίρων τινός, Conf. 62). The Chariot Companion commentary (2025-11-09) turns on that phrase and says Philo 'did not leave us names'; at Conf. 62 the companion is Zechariah and what he utters is the Anatole oracle.",
 "Mut. 121–123 carries the renaming as a re-stamping (μεταχαράττων; τὸ τοῦ λεχθέντος νόμισμα), the vocabulary of #642 and #1458.",
 "The Sapphic channel in Philo is the subject of #1486 (Mut. 54–57, Her. 3–4, Migr. 47–48) and of #1458 (Philo beside Longinus). With the above, one author carries both the transform and the Logos-as-the-crowned-Ἰησοῦς: the join the genetic reading has to make across authors everywhere else."]
SEAT_FLAGS = ["lxx-swete Zechariah 3:8 and 6:11: apparatus text is run into the verse lines (the OCR layer). 3:8's Ἀνατολήν cannot be asserted from the seat; 6:11's Ἰησοῦ τοῦ Ἰωσεδὲκ can. A repair of the seat, in its own commit."]
OWED = ["external scholarship on Philo's Logos and Zechariah 6:12 (Conf. 62–63, 146), on Mut. 121, and on Philo's names for the Logos, publicly obtainable only (the commons stance)",
        "the Philo piece: fixed up, fleshed out, connected, deposited (author and venue to be prompted before deposit); then the v1.2 builds from this staging"]


def rec(n, note=None, extra=None):
    if n == "philo": return {"record": "pending: the Philo piece", "note": note}
    d = REG[n]; o = {"deposit": n, "axn": d["axn"], "title": d["title"], "status": d.get("status"), "sha256": d["hash"], "url": f"https://www.alexanarch.org/s/records/{n}/"}
    if d.get("superseded_by_deposit_number"): o["superseded_by"] = d["superseded_by_deposit_number"]
    if note: o["note"] = note
    if extra: o.update(extra)
    return o


def build():
    out = {}
    for kid, k in K.items():
        o = {"kernel": kid, "deposit": k["deposit"], "deposited_version": REG[k["deposit"]]["version"], "deposited_axn": REG[k["deposit"]]["axn"],
             "deposited_files": k["files"], "staged_for": "v1.2", "versioned": False, "rule": RULE, "rulings": RULINGS,
             "evidence": [rec(n, t) for n, t in k["evidence"]], "related_work": [rec(n, t) for n, t in k["related_work"]],
             "history": [rec(a, extra={"record_of_standing": b}) for a, b in k["history"]],
             "joins": [rec(n, t) for n, t in k["joins"]], "flags": [rec(n, t) for n, t in k.get("flags", [])]}
        for h in o["history"]:
            assert h.get("superseded_by") == h["record_of_standing"], (kid, h["deposit"], h.get("superseded_by"))
        out[kid] = o
    seats = {}
    for k, p in SEATS.items():
        f = C / p; seats[k] = {"path": f"data/corpora/{p}", "sha256": hashlib.sha256(f.read_bytes()).hexdigest()}
        seats[k]["_lines"] = {ln.split("\t", 1)[0]: ln.split("\t", 1)[1] for ln in f.read_text(encoding="utf-8").splitlines() if "\t" in ln}
    loci = []
    for s, ref, quote, gloss in LOCI:
        line = seats[s]["_lines"][ref]; assert quote in line, (ref, quote[:40])
        loci.append({"seat": seats[s]["path"], "seat_sha256": seats[s]["sha256"], "ref": ref, "exact": quote, "gloss": gloss})
    for s in seats.values(): s.pop("_lines")
    out["philo-component"] = {"title": "PHILO SAYS IT OUT LOUD (working title, the author 18:45)", "status": "to be fixed up, fleshed out, connected to external scholarship and deposited before the frames are versioned",
                              "goes_into": ["EA-HK-REVFIRST-01 (18:56)", "EA-HK-HISTLOGOS-01, home of the join", "EA-HK-TENTHMUSE-01, by join"],
                              "blog_sources": [{"date": a, "title": b, "url": c, "role": r} for a, b, c, r in BLOG],
                              "records": [rec(n) for n in (1486, 1458, 1505, 1503, 636, 642)], "loci": loci, "findings": PHILO_FINDINGS,
                              "seat_flags": SEAT_FLAGS, "owed": OWED, "rulings": RULINGS[3:]}
    return out


def main(check=False):
    out = build()
    for name, o in out.items():
        p = HERE / f"{name}.json"; s = json.dumps(o, ensure_ascii=False, indent=1) + "\n"
        if check: assert p.read_text(encoding="utf-8") == s, f"{p.name} differs"
        else: p.write_text(s, encoding="utf-8")
        n = sum(len(o.get(x, [])) for x in ("evidence", "related_work", "history", "joins", "flags", "loci"))
        print(f"{name}: {n} entries")
    return 0


if __name__ == "__main__":
    sys.exit(main("--check" in sys.argv))
