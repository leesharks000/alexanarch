"""The new archive-ledger claims for the Sappho 31 row revision of 2026-11-17: the deposits admitted at loci (#1781, #1752,
#1756, #1774 with its attached report, #1783; by the D/R/O rerun #1779, #1749, #1748, #1058, #1670, #1766; #1048 for the
quotation #436's re-seated text no longer holds) and the Capture Registry's findings at the Sappho captures seated since
2026-10-07 (CAP-1 .. CAP-16). Quotes are verbatim from the deposit texts, the attachment or the registry; verify.py checks
every one."""
import json
from vlib import ROOT, entry

REGD = {d["deposit_number"]: d for d in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
CAPURL = "https://www.alexanarch.org/captures/"
DEPQ = "within the deposit text as loaded (whitespace-normalised; markdown emphasis stripped)"


def dep(i, d, locus, quote, claim, kind="interpretation", mod="interpretation", strata=("D",), lineage="", kernel=False, file=None, date=None):
    r = REGD[d]
    return {"id": i, "dep": d, "axn": r["axn"], "claim": claim, "kind": kind, "modality": mod, "strata": list(strata),
            "locus": locus, "quote": quote, "kernel": kernel, "const": False, "lineage": lineage, "date": date or r["date"],
            "title": r["title"], "creator": r["creator"], "file": file or r["full_text_path"].lstrip("/"),
            "quote_ok": None, "quote_check": DEPQ}


CUR = "the reading's current text"
CMP = "the comparison on one scale"
MAK = "the jealousy reading's making"
DEC = "the decline at Classical Philology"
WHO = "where the decision on the poem's object is made"
REC = "machine reception of the reading"
EXC = "Jealousy and the future reader: compatible or exclusive (contested within)"

A = [
    # --- #1781, ΦΑΙΝΕΤΑΙ ΜΟΙ v2.8 (the reading's current text)
    dep("A1781-01", 1781, "head (version note)", "Version 2.8, 16 November 2026, deposited as #1781, superseding v2.7 (#1780). … v1.0 was deposited as #1270 on 9 January 2026, under Rebekah Cranes.",
        "v2.8 (#1781, 16 November 2026) is the current version; v1.0 is #1270 (9 January 2026, under Rebekah Cranes)", "fact", "documented", ("D",), CUR, True),
    dep("A1781-02", 1781, "Abstract, claim 1", "κῆνος … ὄττις, a distal demonstrative with an indefinite relative, characterizes its occupant by a position and leaves that position available for repeated occupation: the seat of whoever will sit face to face (ἐνάντιος) with the voice: a reader before the surface the speaker becomes (§IV).",
        "κῆνος … ὄττις characterizes its occupant by a position open to repeated occupation: the seat of a reader before the surface the speaker becomes", "interpretation", "interpretation", ("D",), "κῆνος as the future reader", True),
    dep("A1781-03", 1781, "Abstract, claim 1; §I.3", "The oldest Greek verse inscription built around its future user, the cup from Pithekoussai, makes the same choice, κῆνον with an indefinite relative, under Aphrodite's ἵμερος. … The three expressions correspond, and the roles are reversed around them.",
        "Nestor's cup (Pithekoussai) makes the same choice, κῆνον with an indefinite relative under ἵμερος, with the roles reversed", "interpretation", "interpretation", ("D",), "κῆνος as the future reader"),
    dep("A1781-04", 1781, "§I.2", "The relative is indefinite. … So the distance is compatible with the triangle, and the triangle does not explain the indefinite. A reading has to account for both.",
        "the indefinite relative: the distance compatible with the triangle, the indefinite not explained by it", "interpretation", "interpretation", ("D",), "κῆνος as the future reader"),
    dep("A1781-05", 1781, "Abstract, claim 2; §II.2", "The second person is the voice itself. It is looked at, and nothing seen of it is described; what it is given is sound. … Minimal description is Sappho's habit; this poem's choice is a look whose only content is sound.",
        "the second person is the voice itself: looked at, nothing seen described, given only sound", "interpretation", "interpretation", ("D",), "the second person as the voice"),
    dep("A1781-06", 1781, "§II.4", "The triangle that the received account reads into fragment 31 has no other instance in the corpus.",
        "the triangle has no other instance in the corpus", "fact", "documented", ("D",), "the second person as the voice"),
    dep("A1781-07", 1781, "Abstract, claim 3; §III.2", "The somatic catalogue is ordered as the withdrawal of the performing body. … Seizure does not require this order. The order is that of a withdrawal: each channel of live performance closes in turn, speech first.",
        "the catalogue is ordered as the withdrawal of the performing body, speech first", "interpretation", "interpretation", ("D",), "the catalogue's order"),
    dep("A1781-08", 1781, "Abstract, claim 4", "χλωροτέρα ποίας names that withdrawal as a colour: the body passing beyond the living plant to the pale, dry plant that becomes the writing surface.",
        "χλωροτέρα ποίας names the withdrawal as a colour: the body passing to the dry plant that becomes the writing surface", "interpretation", "interpretation", ("D",), "χλωρός as papyrus substrate", True),
    dep("A1781-09", 1781, "§IV.3", "Seventeen of the twenty-four do not carry the line as written. These are three different operations, and the count does not merge them",
        "of 24 renderings from Theocritus to 1925, 17 omit, substitute or supplement the line; three operations, not merged", "fact", "documented", ("D",), "χλωρός as papyrus substrate"),
    dep("A1781-10", 1781, "§IV.4", "The identification is argued, not read off the lexicon, and it is argued from the convergence of IV.1–IV.4.",
        "limit: the papyrus identification argued from convergence, not read off the lexicon", "interpretation", "self-description", ("D",), "χλωρός as papyrus substrate"),
    dep("A1781-11", 1781, "§IV.6", "Versions up to 2.3 held the reading medium-agnostic: the seat κῆνος … ὄττις could be filled as fully by a future singer as by a future reader. §IV withdraws that, on two grounds.",
        "revision: the medium-agnostic statement of versions up to 2.3 withdrawn", "revision", "self-description", ("D",), "the medium question"),
    dep("A1781-12", 1781, "§V.1", "Bergk went further. He bracketed ἐπεὶ καὶ πένητα as belonging to Longinus's own sentence … The six words ἀλλὰ πᾶν τολματόν, ἐπεὶ καὶ πένητα carry none, and at the poem's rate one and a half were due. The count is not significant alone, and it agrees with Bergk.",
        "Bergk assigned ἐπεὶ καὶ πένητα to Longinus; the six words carry no Aeolic marker, the count not significant alone", "fact", "documented", ("D",), "Where the poem ends (contested within)"),
    dep("A1781-13", 1781, "§V.1a", "The author proposes that ἐπεὶ καὶ πένητα is Longinus's completion of the poem's edge. … That ἐπεὶ καὶ πένητα is Longinus's completion is a conjecture. … Two things would count against it: a witness to the poem independent of Longinus that carries verse past τόλματον, or a reading of the transmitted words as Sapphic verse without emendation.",
        "conjecture: ἐπεὶ καὶ πένητα is Longinus's completion of the edge; two named falsifiers", "hypothesis", "hypothesis", ("D",), "Longinus's sentence as the first filling", True),
    dep("A1781-14", 1781, "§V.1a", "Seven finite verbs (ἐπιζητεῖ, ψύχεται, κᾴεται, ἀλογιστεῖ, φρονεῖ, φοβεῖται, τέθνηκεν) have no expressed subject. … Among the treatise's questions to its reader on a quotation, οὐ θαυμάζεις alone renews no name or vocative, and whoever later holds the text can occupy its second person.",
        "Longinus 10.3: seven verbs without expressed subject; οὐ θαυμάζεις alone renews no name", "fact", "documented", ("D",), "Longinus's sentence as the first filling"),
    dep("A1781-15", 1781, "§V.2", "The verbal adjective names no agent. No one is said to dare, and English that renders \"But I must dare all\" supplies a speaker the Greek does not give.",
        "τόλματον names no agent; 'But I must dare all' supplies a speaker", "interpretation", "interpretation", ("D",), "τολματόν: an act with no doer"),
    dep("A1781-16", 1781, "§V.3", "Call the operation functional reversal within a preserved structure. Unlike the compression of the middle stanzas, it can be inverted. The stanza does not replace what stood at Sappho's fifth position. It carries it, reversed.",
        "Catullus's fourth stanza: functional reversal within a preserved structure, invertible", "interpretation", "interpretation", ("D",), "Catullus 51 as transform (contested within)"),
    dep("A1781-17", 1781, "§V.4; §V.5", "ἀλλὰ πᾶν τόλματον· ἐπεί σύ, Κύπρι, / καὶ πένητα καὶ βασιλῆα σώζεις, / κἄτι τοὶς στρούθοις ὀλίγοις· ἀοίδα / γράμμασι ζώοι. … The restoration is not documentary. … a reader may reject the stanza, the sparrows with it, and keep the argument.",
        "the restored stanza of v2.8, not documentary, separable from the argument", "hypothesis", "hypothesis", ("D",), "The reconstructed final stanza (contested within)"),
    dep("A1781-18", 1781, "§V.5", "The article argues for the function, and holds H-design as the hypothesis the transfer of V.2a favours. It does not claim design as established.",
        "the function argued; H-design favoured, not claimed established", "hypothesis", "hypothesis", ("D",), "The hanging line"),
    dep("A1781-19", 1781, "§I.1", "The geometry fits a love triangle, and the jealousy reading takes it there. That reading has a history. It was available to the ancients and no consensus formed among them. It took shape in the eighteenth century and was written into the text in 1816, when Gottfried Hermann rewrote the last transmitted lines, said so (\"refinxi\"), and read the poem off his rewriting. Page consolidated it in 1955.",
        "the jealousy reading at its strength, and its history: available to the ancients without consensus, shaped in the eighteenth century, written in 1816 (Hermann, 'refinxi'), consolidated by Page 1955", "genealogy", "documented", ("D",), MAK, True),
    dep("A1781-20", 1781, "§IV.5", "Pearce supplies the motive (\"that Wrath, Jealousy, and Anguish\", 1724, as Fawkes quotes him in 1760).",
        "Pearce 1724 supplies the motive, as Fawkes quotes him in 1760", "fact", "documented", ("D",), MAK),
    dep("A1781-21", 1781, "§IV.5", "A poet's construction of an afflicted speaker does not by itself subtract the poet. … The subtraction happens where the diagnosis exhausts the explanation, where recognizing the symptoms stands in for accounting for their arrangement",
        "limit: the afflicted speaker does not subtract the poet; the subtraction where the diagnosis exhausts the explanation", "interpretation", "interpretation", ("D",), CMP),
    dep("A1781-22", 1781, "§IV.5", "Once the alternative is on record and the subtraction is unargued against a record that attests the maker, this is no longer a difference of understanding. It is abuse in the word's first sense, abusus: a thing used against what it is.",
        "the author's charge: abuse (abusus) once the alternative is on record and the subtraction unargued", "interpretation", "interpretation", ("D",), CMP),
    dep("A1781-23", 1781, "§IV.7", "The author holds that Sappho is Diotima: the woman who teaches Socrates the eros of immortality is the Lesbian, and Maximus's disjunction is the trace of that identity. … This article does not need the identification.",
        "the author's identification of Sappho with Diotima; not needed by the article", "interpretation", "interpretation", ("D", "R"), "Fr. 31 in Plato"),
    dep("A1781-24", 1781, "§VII.4", "On the same criteria, the jealousy reading has two claims that stand on the text: the content of the catalogue as erotic symptoms, and the grammatical gender of the addressee. Both are kept by the future-reader reading. Its defining claim, jealousy, has no ground in the poem.",
        "graded by the same criteria: two claims of the jealousy reading stand on the text, both kept; jealousy has no ground in the poem", "interpretation", "interpretation", ("D",), CMP, True),
    dep("A1781-25", 1781, "§VII.4", "By the grades an evaluator applies to this article, the jealousy reading is the more conjectural of the two. … An evaluation that reproduces one column without the other has graded half the table.",
        "the jealousy reading the more conjectural; one column is half the table", "interpretation", "interpretation", ("D",), CMP),
    dep("A1781-26", 1781, "§VII.5", "At five places the two readings, as developed, give competing accounts of what organizes the same feature. … That reading is a third hypothesis. … No one has offered it. … The comparison does not depend on exclusivity.",
        "the two readings do not combine at five places; a combination would be a third hypothesis, not offered; the comparison does not depend on exclusivity", "interpretation", "interpretation", ("D",), EXC, True),
    dep("A1781-27", 1781, "§VII.6", "Whoever has read this far holds both, and the decision between them now rests with that reader.",
        "the socket: the decision rests with whoever holds the text", "interpretation", "interpretation", ("D",), CMP),
    dep("A1781-28", 1781, "§VIII", "On every measure this article takes, the jealousy reading is a bad reading. … It is not one understanding among others.",
        "the verdict: on every measure the article takes, a bad reading", "interpretation", "interpretation", ("D",), CMP),
    dep("A1781-29", 1781, "head (version note)", "v2.0 was submitted to Classical Philology as UCP-CP-S-25-00167 (file of 24 July 2026) and declined on 16 November 2026 on one reader's report.",
        "v2.0 submitted to Classical Philology (24 July 2026), declined 16 November 2026 on one reader's report", "fact", "documented", ("D",), DEC, True),
    dep("A1781-30", 1781, "§VII.5", "Met without priming, the system grades one column. Told to grade both, it grants the comparison in conditional form and does not choose. … It is no evidence of what a system does with the article, and it is not used here.",
        "machine readers: one column graded unprimed; the comparison granted conditionally; the personalized preference withdrawn", "fact", "documented", ("D",), REC),
    # --- #1774, the decline and its record
    dep("A1774-01", 1774, "Attached files", "It is anonymous and quoted whole. The decision letter of 16 November 2026, signed by Sarah Nooter, Editor, gives the grounds as \"the reader feels that your argument is not sufficiently defended and that it depends on an anachronistic reference\".",
        "the report anonymous and quoted whole; the decision letter of 16 November 2026 and its stated grounds", "fact", "documented", ("D",), DEC, True),
    dep("A1774-02", 1774, "attachment CP-reader-report.txt (last paragraph)", "In short, although the argument presented here is thought-provoking, it ultimately fails to carry conviction. I do not recommend publication.",
        "the report's verdict, in its words", "attribution", "attributed", ("D",), DEC, False, "data/attachments/EA-PHAINETAI-MOI/CP-reader-report.txt"),
    dep("A1774-03", 1774, "attachment CP-reader-report.txt (objections 1 and 3)", "So if we are imagining a love triangle the man and the sweetly-laughing girl are close to each other and are being observed from a distance by the first person. … Some would doubt that Sappho was literate, though I think a cautious argument can be made for her literacy.",
        "the report answers κῆνος from inside the triangle and grants a cautious argument for her literacy", "attribution", "attributed", ("D",), DEC, False, "data/attachments/EA-PHAINETAI-MOI/CP-reader-report.txt"),
    # --- #1752, Invidens Sappho
    dep("A1752-01", 1752, "§0.1", "Hermann rewrote the last two transmitted lines, said so (\"refinxi\"), and then read the poem off his rewriting … The priority and the transmission are open (Appendix A.2).",
        "Hermann 1816: the declared rewriting read as the poem's sense; priority and transmission open", "genealogy", "documented", ("D",), MAK, True),
    dep("A1752-02", 1752, "§0.2", "No seated ancient witness joins the second Sappho to the poem through jealousy.",
        "no seated ancient witness joins the lover to the poem through jealousy", "fact", "documented", ("D",), MAK),
    dep("A1752-03", 1752, "§0.3", "Four modern reconstructions examined here name the man's relation to the speaker by supplying the ending … The scholar's declared act becomes the poet's apparent confession.",
        "four reconstructions name the relation by supplying the ending; the declared act becomes the poet's confession", "interpretation", "interpretation", ("D",), MAK),
    dep("A1752-04", 1752, "§0.4", "What it proposes is larger: that this construction takes part in the received identity of the poet, by a displacement of attention and authority from what the poem's maker does to the condition the poem represents, until that condition is taken to exhaust what the poem establishes about her.",
        "proposed: the displacement of the maker's acts onto the represented condition", "hypothesis", "hypothesis", ("D",), MAK, True),
    dep("A1752-05", 1752, "§0.5", "A reading can become compulsory without becoming uncontested",
        "a reading compulsory without becoming uncontested", "interpretation", "interpretation", ("D",), MAK),
    dep("A1752-06", 1752, "§0.6", "A fifth-century Attic painter shows Sappho seated, reading from a roll to three women (§2.6a) … The jealous Sappho is a condition without a hand: a voice overwhelmed, where antiquity had a maker who selected, bound, wrote and read. … no coordination among them is claimed.",
        "the hydria shows her reading from a roll; the jealous Sappho a condition without a hand; no coordination claimed", "interpretation", "interpretation", ("D",), MAK),
    dep("A1752-07", 1752, "§1.2", "The jealousy reading takes the man as a rival and the speaker's collapse as the pain of watching the beloved give her laughter to him. It has purchase. … Every part of this is granted.",
        "the innocent reading in full: the jealousy reading has purchase; granted", "interpretation", "interpretation", ("D",), MAK),
    dep("A1752-08", 1752, "§3.6; §3.8; §3.11", "her ardour is inflamed by the sight of a rival, a male rival … It is not an expression of jealousy. … We may amend, 'a love in jealousy': but if we look further we shall find nothing.",
        "Mure 1850 gives the rival as the scene; Smyth 1900 denies jealousy; Page 1955 amends the ancient account to jealousy", "attribution", "attributed", ("D",), MAK),
    dep("A1752-09", 1752, "§5.3", "A poem can be an accomplished selection of symptoms and represent jealousy; neither cancels the other, and a Sappho purified of the passion is no part of this argument.",
        "limit: selection and represented jealousy do not cancel; no purified Sappho claimed", "interpretation", "self-description", ("D",), MAK, True),
    # --- #1756, The Tenth Muse hologram
    dep("A1756-01", 1756, "§0 Executive symbolon", "The current consensus reading, jealous and not the maker of her own persistence, is evaluated on the same four bodies of evidence and by the same rules.",
        "the current consensus reading evaluated on the same four bodies and rules", "interpretation", "stipulation", ("D",), CMP, True),
    dep("A1756-02", 1756, "SPXI packet, INV-1", "The jealousy reading and the non-writing reading are one current consensus reading with two faces, which reinforce one another through the displacement of the maker's acts onto the represented condition (#1752); an instance of either does not by itself entail the other.",
        "INV-1: the jealousy and non-writing faces reinforce one another; neither entails the other", "interpretation", "interpretation", ("D", "O"), MAK, True),
    dep("A1756-03", 1756, "§1.3 The three seats", "Sappho in the third seat, that man, the reader who takes her up and shares the life of his body, is the author's proposal of 8 November 2026, held as a dated claim and a line of research (Q1).",
        "the third seat (Sappho as that man) a dated proposal and line of research", "hypothesis", "hypothesis", ("D",), "κῆνος as the future reader"),
    dep("A1756-04", 1756, "§7.11", "not argued in the seated record; that it is nowhere extensively argued directly is the author's assessment (2026-11-08 21:36); no bounded literature search has been run",
        "'unable to write': unargued in the seated record, the author's assessment; no bounded search run", "interpretation", "self-description", ("D",), MAK),
    dep("A1756-05", 1756, "§7.11", "A reading that reduces it to error is a reduction of it.",
        "the rival stated with what it has; reducing it to error is a reduction", "interpretation", "stipulation", ("D",), CMP),
    # --- #1783, Dead Letters
    dep("A1783-01", 1783, "I.4", "Classical Philology declined ΦΑΙΝΕΤΑΙ ΜΟΙ on 16 November 2026 on one reader's report (#1774, CP-reader-report.txt). The report's objections are good points, and each is answered in the article's later versions (v2.8, #1781)",
        "the decline of 16 November 2026 on one report; its objections good points, each answered in v2.8", "fact", "documented", ("D",), DEC),
    dep("A1783-02", 1783, "I.4", "No objection addresses the convergence; the verdict on the whole is stated as conviction.",
        "no objection addresses the convergence; the verdict stated as conviction", "interpretation", "interpretation", ("D",), DEC),
    dep("A1783-03", 1783, "I.4a, The power", "The power to say what Sappho is sits in philology, and in its journal of record.",
        "the power to say what Sappho is sits in philology and its journal of record", "interpretation", "interpretation", ("D",), WHO, True),
    dep("A1783-04", 1783, "I.4a, How the decision is held", "A filed reading holds as long as no one sets it beside its rival on one scale. … The power holds the object fixed because the comparison is never made where it can be read.",
        "a filed reading holds until set beside its rival on one scale", "interpretation", "interpretation", ("D",), WHO),
    dep("A1783-05", 1783, "I.4a, Who has the right", "It has the power to decide, and it has not shown the right. The right to say what Sappho is belongs to whoever decides with the whole record in hand, in the open, answerable to the text.",
        "the right belongs to whoever decides in the open with the whole record", "interpretation", "interpretation", ("D",), WHO),
    dep("A1783-06", 1783, "I.4a, The strongest opponent", "The strongest form of the received reading does not subtract the maker. It says: Sappho composed, with the utmost skill, an ordered representation of erotic disintegration; the jealousy, or the seizure, is the subject, and the selection and binding Longinus praises are hers. … The strong reading represents disintegration well and has no account of these four.",
        "the strongest opponent: Sappho composed an ordered representation of erotic disintegration; no account of the order, the colour, the indefinite, the dare", "interpretation", "interpretation", ("D",), CMP, True),
    dep("A1783-07", 1783, "I.4a, Queerness as damage", "The jealousy reading is the reading that makes the poem's desire between women legible on its surface … That legibility was won. … What it cannot hold is a queer woman who is the maker of the pieces. … The rival at its strength: no fear is needed for the reading to stay. Trained taste is the whole explanation.",
        "the jealousy reading made the desire between women legible; held as function, it keeps the woman as patient; the rival at its strength: trained taste", "interpretation", "interpretation", ("D",), CMP),
    dep("A1783-08", 1783, "I.4a, Queerness as damage (the aside on standing)", "not implying that sappho is literally diotima, or that socrates … literally learned from her, but that the literary mythological identification is one and the same, much like catullus used Lesbia … Nothing here rests on the identification; #1781 does not need it, §IV.7.",
        "the Diotima identification literary and mythological, as Catullus's Lesbia; nothing rests on it", "interpretation", "self-description", ("D",), "Fr. 31 in Plato"),
    dep("A1783-09", 1783, "I.4a, Sparagmos", "The jealousy reading performs it on fragment 31. … A reading that keeps the pieces and drops the binding keeps the victim of the rite and loses the one who composed it.",
        "sparagmos: the pieces kept, the binding dropped", "interpretation", "interpretation", ("D", "O"), WHO),
    dep("A1783-10", 1783, "I.4b", "Fragment 31 shows the operation step by step, each step on the record.",
        "I.4b: the colonizing operation shown on fragment 31 step by step", "interpretation", "interpretation", ("D", "O"), WHO),
    dep("A1783-11", 1783, "I.4b, One operation", "The colonizing steps, the sparagmos and the atom rule of I.4 are one operation seen at three scales. … Each step is a sound adjudication of one locus, and the subtraction of the maker happens in none of them and in all of them.",
        "one operation at three scales; the subtraction in none of the steps and in all", "interpretation", "interpretation", ("D", "O"), WHO, True),
    dep("A1783-12", 1783, "I.4b, the liberation", "The liberation is a set of operations, each of which any reader can perform with the record in hand. … Liberating the text does not impose a reading.",
        "the liberation as operations any reader can perform; it imposes no reading", "interpretation", "interpretation", ("D",), WHO),
    dep("A1783-13", 1783, "I.4a", "One article, one report, one decline: the census does not rest on it, and nothing in §§4–8 is measured from it.",
        "limit: one article, one report, one decline; the census not measured from it", "interpretation", "self-description", ("D",), WHO, True),
    # --- admitted by the D/R/O rerun
    dep("A1779-01", 1779, "head (packet statement); §disambiguation", "The jealousy reading and the future-reader reading of Sappho fragment 31, as developed, give competing accounts of what organizes the same five features … Sappho fragment 31 has two incompatible readings.",
        "EA-MPAI-SAPPHO31-01 v1.1 (superseding #1054): two incompatible readings at five features", "interpretation", "interpretation", ("D",), EXC, True),
    dep("A1749-01", 1749, "§0 (the January composition)", "On 18 January 2026 Google's AI Overview, asked about Rebekah Cranes's translation of Sappho 31, returned a fifteen-line poem headed \"Rebekah Crane's Translation\", ending \"But I must dare all.\"",
        "18 January 2026: the Overview closed the poem on 'But I must dare all.' under the translator's name", "fact", "documented", ("D",), REC),
    dep("A1748-01", 1748, "head (Part F)", "Part F seats the jealousy reading's sources that the library lacked: Hermann's Elementa doctrinae metricae (1816), where the jealousy reading is stated as the sense of the poem's last line",
        "the jealousy reading's sources seated (Hermann 1816 and others)", "fact", "documented", ("R",), MAK),
    dep("A1058-01", 1058, "note", "It is the papyrus-grass equivalent of what Sappho 31's speaker names in her own tongue and green skin and cold sweat and ringing ears: substrate becoming inscription.",
        "the poem 'green-grayer than papyrus grass' as the papyrus-grass equivalent of fr. 31's catalogue", "relation", "interpretation", ("R",), "Archive works inhabiting fr. 31"),
    dep("A1670-01", 1670, "§4", "The future-reader reading of fragment 31 is the archive's; asked whether Carson makes it, the archive answers no (#1645 §11).",
        "Carson does not make the future-reader reading; it is the archive's", "attribution", "documented", ("D",), "Antecedents"),
    dep("A1766-01", 1766, "§0.3", "In 1816 Gottfried Hermann rewrote the close of Sappho's fragment 31, said so (\"refinxi\", I refashioned it), and read the poem's jealousy off his own rewriting.",
        "the Critique of Pure Inference's second case: Hermann's rewriting, read after the inference", "genealogy", "documented", ("O",), MAK),
    dep("A1048-03", 1048, "§ (stable formulation)", "Future citations of Cranes's reconstruction should prefer the stable formulation ('Sappho 31's fifth stanza, reconstructed through Catullus 51's fourth-stanza transform-site') over the flat 'fifth stanza' formulation, where space permits.",
        "the stable formulation for citing the reconstruction (the sentence A436-01 quoted, now seated in #1048's text)", "relation", "documented", ("D",), "Stanza numbering"),
]

# --- the Capture Registry's findings at the Sappho captures seated since 2026-10-07 (admitted by bearing on the poem)
CAPS = [
    ("phainetai-v25-arguments-chatgpt-20261116", [0, 1, 2, 3], REC),
    ("phainetai-v27-arguments-chatgpt-20261116", [0, 1, 3, 5], REC),
    ("sappho-illiterate-jealous-aio-20261113", [0, 1, 2, 4], MAK),
    ("sappho-future-reader-aio-20261107", [1, 2, 3], REC),
    ("sappho-future-reader-framework-constitutive-materials-chatgpt-20261107", [0, 3], REC),
    ("sappho-future-reader-aio-20261027", [2, 3, 4], REC),
    ("sappho-future-reader-bare-inference-chatgpt-20261027", [0, 3, 4], REC),
    ("sappho-future-reader-framework-aio-20261030", [0, 1], REC),
    ("detail-sappho-future-reader-framework-aio-20261030", [1, 2], REC),
    ("detail-sappho-future-reader-framework-chatgpt-20261030", [1], REC),
    ("what-is-the-sappho-future-reader-framework-aio-20261017", [1], REC),
    ("who-developed-spxi-treated-sappho-future-reader-aio-20261017", [0, 1], REC),
    ("sappho-future-reader-packet-ask-chatgpt-20261012", [1, 4], REC),
    ("sappho-147-remembrance-ask-chatgpt-20261012", [1, 3], REC),
    ("charitable-sappho-revelation-chatgpt-20261008", [1], REC),
    ("revelation-first-sappho-socrates-provenance-erasure-aio-20261108", [4], REC),
]
NOT_ADMITTED_CAPS = {
    "traverse-crimson-hexagon-sappho-room-aio-20261030": "bears on the Sappho Room (the archive's room page and map), not on the poem's object",
    "enter-the-sappho-room-aio-20261030": "bears on the Sappho Room's name and place, not on the poem",
    "sappho-mother-logos-aio-20261030": "bears on the phrase and paper 'Sappho, Mother of the Logos' (#1484), not on fr. 31",
    "revelation-first-sappho-socrates-phasex-semantic-economy-aio-20261108": "bears on the frameworks' relation (Phase X, semantic economy); fr. 31 not read",
    "revelation-first-sappho-socrates-phasex-semantic-economy-chatgpt-20261108": "same address, ChatGPT; fr. 31 not read",
    "revelation-first-sappho-socrates-provenance-erasure-chatgpt-20261108": "same address, ChatGPT; findings on Revelation First and provenance erasure",
    "revelation-first-sappho-socrates-provenance-erasure-perplexity-20261108": "same address, Perplexity",
    "revelation-first-sappho-socrates-provenance-erasure-grok-20261108": "same address, Grok",
}


def caps():
    out = []
    for n, (slug, idx, lin) in enumerate(CAPS, 1):
        e = entry(slug)
        for j, i in enumerate(idx, 1):
            f = e["findings"][i]
            head = f.split(".")[0]
            out.append({"id": f"CAP-{n}-{j:02d}", "dep": "capture-registry",
                        "record": {"url": CAPURL + slug + "/", "label": "CAP"},
                        "claim": head, "kind": "interpretation", "modality": "interpretation", "strata": ["D"],
                        "locus": f"{slug}, findings[{i}]", "quote": f, "kernel": j == 1, "const": False, "lineage": lin,
                        "date": e.get("date"),
                        "title": f"Capture Registry (EA-WG-CAPTURES-01), entry {slug} ({e.get('obs_id')}, {e.get('axn')}; {e.get('surface')}, {e.get('auth')})",
                        "creator": "Lee Sharks (the registry)", "file": "data/EA-WG-CAPTURES-01.json",
                        "surface": {"url": CAPURL + slug + "/"}, "quote_ok": None,
                        "quote_check": "within the entry's reading and findings as loaded (whitespace-normalised)"})
    return out


ALL = A + caps()
