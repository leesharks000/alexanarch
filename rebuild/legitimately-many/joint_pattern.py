#!/usr/bin/env python3
"""Legitimately Many — the joint pattern (design §4.4, §6.1; item 6 of the plan, 2026-11-02). The observations a production model
must explain together, each stated at the grain the archive's deposits found it, with its loci (located in their seats by this
script, which refuses an element whose phrase is not found) and, for each, what the received succession model must supply to
explain it at that grain and what the one-maker reading says. The limits and the evidence that cuts the other way are rows of
their own (N1–N3), as §4.2 requires. The specification makes no finding of its own: every observation is a deposited one,
cited, or a locus read in the draft.
    python3 joint_pattern.py      -> joint-pattern.json, joint-pattern.md"""
import json, pathlib, re, sys, unicodedata
H = pathlib.Path(__file__).resolve().parent
C = H / "../../data/corpora"
T = {"apol": "plato/text/tlg002-Ἀπολογία_Σωκράτους.txt", "ep": "plato/text/tlg036-Ἐπιστολαί.txt", "dl": "diogenes-laertius/text/tlg001.txt",
     "en": "aristotle/text/tlg010-Nicomachean_Ethics.txt", "se": "aristotle/text/tlg040-De_sophisticis_elenchis.txt",
     "apr": "aristotle/text/tlg001-Analytica_priora.txt", "met": "aristotle/text/tlg025-Metaphysics.txt", "thm": "theophrastus/text/tlg006.txt",
     "rep": "plato/text/tlg030-Πολιτεία.txt", "poe": "aristotle/text/tlg034-Poetics.txt"}


def found(key, phrase):
    t = re.sub(r"\s+", " ", unicodedata.normalize("NFC", (C / T[key]).read_text(encoding="utf-8")))
    return unicodedata.normalize("NFC", phrase) in t


J = [
 dict(id="J1", element="Four positions, four operations, each with its own voice and object",
      observation="Examination by question on a received figure (the Socrates of the jurors' childhood and of the Clouds); dramatic division, a doctrine distributed across four persons with no voice of the maker's own; first-person demonstration that names its own beginning; aporia continuing another position's treatise from inside. Draft §1.2.",
      loci=[("apol", "οἳ ὑμῶν τοὺς πολλοὺς ἐκ παίδων παραλαμβάνοντες"), ("dl", "διὰ τεττάρων προσώπων"), ("se", "ἀλλ᾿ οὐδὲν παντελῶς ὑπῆρχεν"), ("thm", "μέχρι μὲν δὴ τούτων οἷον ἄρτιος ὁ λόγος")],
      deposits=[1579, 1603, 1583], status="read (draft §1.2)",
      succession_must_supply="Why three makers in sequence, with a fourth who wrote nothing, divide the operations without overlap: each takes a different operation, voice and object, and none takes another's. Different temperaments explain difference; they do not explain a partition.",
      one_maker="One investigation into one and many assigns each position an operation, voice and object of its own (§1.1's four conditions)."),
 dict(id="J2", element="Continuity on the page across the name boundary",
      observation="Theophrastus's Metaphysics writes Λ's own hinge (Λ 6–7 complete, Λ 8's question next) in Λ's transition form, contests Λ 8's count of the spheres in Λ 8's terms, and lands on Λ 10's open aporiai. The roll changes its name where the account changes status from complete to needing more. #1583; draft §3.2.",
      loci=[("thm", "τὸ δὲ μετὰ ταῦτ᾽ ἤδη λόγου δεῖται πλείονος περὶ τῆς ἐφέσεως"), ("met", "πότερον δὲ μίαν θετέον τὴν τοιαύτην οὐσίαν ἢ πλείους"), ("thm", "τῆς αἰτίας μείζονα ζητεῖ λόγον")],
      deposits=[1583, 1595, 1597], status="read (#1583); seated facing (#1595)",
      succession_must_supply="A pupil who writes the next step of the master's treatise in the treatise's own transition form, at the treatise's own level of generality, and whose book is first ascribed to the pupil by a reader three centuries later on a ground not preserved (draft §3.4a). Influence or shared vocabulary does not discharge this (design §4.4): the finding is the hinge, the position at which the text turns.",
      one_maker="The inquiry is continuous; the name changes at the joint where the work's function changes (#1583's third reading)."),
 dict(id="J3", element="Oppositions at definite loci, in the opposed position's own terms",
      observation="The dialogues answer the comic Socrates by quoting the Clouds; the treatises refute the forms and state the refutation as a duty, καὶ τὰ οἰκεῖα ἀναιρεῖν, 'to destroy one's own things'; the continuation contests Λ 8's count. None is staged and withdrawn. Draft §1.3.",
      loci=[("apol", "ἐν τῇ Ἀριστοφάνους κωμῳδίᾳ"), ("en", "καὶ τὰ οἰκεῖα ἀναιρεῖν"), ("thm", "οὐ γὰρ ὅ γε τῶν")],
      deposits=[1579, 1583], status="read (draft §1.3)",
      succession_must_supply="Ordinary disagreement between persons. At this grain the model must also explain why each opposition is conducted in the opposed position's vocabulary and at its own structural joint, and why the duty of opposing is written in the first person as the destruction of what is one's own.",
      one_maker="Real self-division: a position that could not lose to another would be a mask (§1.3), and the corpus states the duty of losing."),
 dict(id="J4", element="Division placed and terminated across the boundary",
      observation="Division by genera, practised throughout the dialogues, is 'a small part' of the inquiry SE 34 says had nothing before it; Λ 9 gives the terminus I.31 withholds, where the terms are not other. The theory of division is stated under one name and practised under the other, and the claim of no predecessor stands beside it. #1576; #1603.",
      loci=[("apr", "ἡ διὰ τῶν γενῶν διαίρεσις μικρόν τι μόριόν ἐστι τῆς εἰρημένης μεθόδου"), ("met", "οὐχ ἑτέρου οὖν ὄντος τοῦ νοουμένου καὶ τοῦ νοῦ"), ("se", "ἀλλ᾿ οὐδὲν παντελῶς ὑπῆρχεν")],
      deposits=[1576, 1603, 1574], status="read (#1576, #1603)",
      succession_must_supply="Why a pupil who learned division in the master's school both files it as a small part of his own method and says that of that method nothing existed before; the received gloss reconciles the sentence with 'what we know' (Poste, #1603), the premise the passage is read through.",
      one_maker="The same method is placed by its maker at two stations, practice and theory, and the claim of no predecessor is literal (#1603)."),
 dict(id="J5", element="The catalogues file complementary absences",
      observation="Aristotle's catalogue opens with Plato's subject-titles with the names removed, 17 of 26 entries, seven times the base rate; Plato's divisions survive whole only as Aristotle's report, opening 'Διῄρει δέ, φησὶν Ἀριστοτέλης' and closing 'κατὰ τὸν Ἀριστοτέλην'; the residue is the Socratic examination, the function with no catalogue. The Theophrastan list shares twelve titles with the Aristotelian and files one work under both names by ἤ. #1590; #1581.",
      loci=[("dl", "Διῄρει δέ, φησὶν Ἀριστοτέλης"), ("dl", "ὧδε καὶ τὰ πρῶτα διῄρει κατὰ τὸν Ἀριστοτέλην"), ("dl", "Ὑπομνημάτων Ἀριστοτελικῶν ἢ Θεοφραστείων")],
      deposits=[1590, 1581], status="measured (#1590, with a stem-rule control) and read",
      succession_must_supply="Two lost bodies of work, each with its candidates under the other name: a pupil's early dialogues that track the master's subject-titles with the names removed, and a master's technical teaching that survives only as the pupil's report. Each loss can be explained separately; the model owes the shape of the pair.",
      one_maker="One body of work filed under two names, each name's lost part found under the other (#1590's transform)."),
 dict(id="J6", element="One transmission apparatus, filled by both corpora, with no cross-reference",
      observation="A six-function specification of a transmission apparatus (encoding, substrate, decommissioning, withholding, recovery, verification), registered before any Platonic or Aristotelian text was assigned to it, is filled by both corpora at the level of the individual work, with one device closely transformed across the boundary and no cross-reference; a random control on the Johannine writings filled 0 of 6 by what a work is about and 6 of 6 by what appears in it. #1572.",
      loci=[], deposits=[1572], status="measured (#1572), the specification registered before any text was assigned to it; the deposit states the concession that keeps it from being more than it is",
      succession_must_supply="Why a device closely transformed across the boundary is never cited across it: a pupil who rebuilds the master's apparatus and names neither the apparatus nor its source.",
      one_maker="One maker does not cite itself across its own names."),
 dict(id="J7", element="Style follows operation off the seam; the names sort the texts at the seam",
      observation="Across the Aristotelian and Theophrastan corpora the first principal axis runs between the world (described, explained, what people do) and the logical-metaphysical instrument; unsupervised, 400 blocks from 39 texts split by operation and leave the names at chance; the purest 'Theophrastan' voice is the Athenaion Politeia and the Historia animalium, under Aristotle's name. At the one seam continuous on the page, the names sort the texts. #1586.",
      loci=[], deposits=[1586, 1593], status="measured (#1586), with the limits of #1593 (N2)",
      succession_must_supply="Why the stylistic boundary runs through each name's corpus by operation, and coincides with the name only at the seam where the texts are continuous.",
      one_maker="Voice is the voice of an operation; the name was assigned where the operation changes (#1586)."),
 dict(id="J8", element="One trait carried through three named functions",
      observation="Theophrastus's Characters register a disposition with name, scene, verdict and theory removed; the first Character, irony, is Socrates's method under his enemies' name; the Ethics restores the name, οἷον καὶ Σωκράτης ἐποίει. Dialogue → sketch → category; person present → removed → restored. #1584.",
      loci=[("en", "οἷον καὶ Σωκράτης ἐποίει")], deposits=[1584], status="read and measured on its control (#1584)",
      succession_must_supply="Why the pupil's catalogue of characters removes exactly what the master's ethics restores, with the teacher of the master's teacher as the restored example.",
      one_maker="One trait traversing three named authorial functions (#1584)."),
 dict(id="J9", element="The corpus marks the filing",
      observation="The Second Letter withdraws the name from the writings, 'there is no writing of Plato'; the catalogue files one work under a disjunction of two names. Locus table L01, L09.",
      loci=[("ep", "οὐδʼ ἔστιν σύγγραμμα Πλάτωνος οὐδὲν οὐδʼ ἔσται"), ("dl", "Ὑπομνημάτων Ἀριστοτελικῶν ἢ Θεοφραστείων")],
      deposits=[1579, 1581], status="read",
      succession_must_supply="A letter of disputed authenticity and a librarian's hesitation, each set aside separately; the model owes why both marks fall where the one-maker reading places the filing.",
      one_maker="The maker marks, somewhere, that the filing is a filing (§1.5)."),
 dict(id="J10", element="The instruments of legitimacy differ by name",
      observation="Four wills, four dispositions of authorship: silence (Aristotle), one heir for all the books (Theophrastus), the writer's own works withheld (Strato, πλὴν ὧν αὐτοὶ γεγράφαμεν), the unpublished ordered into publication (Lycon). Draft §1.4.1; #1581.",
      loci=[("dl", "τὰ δὲ βιβλία πάντα Νηλεῖ"), ("dl", "πλὴν ὧν αὐτοὶ γεγράφαμεν")], deposits=[1581], status="read (draft §1.4.1)",
      succession_must_supply="Four testators with four different dispositions of their writings is the ordinary expectation; the model owes nothing more here unless the dispositions are read with J5 and J9.",
      one_maker="The succession is legislated in the instruments that give each name a testator (§1.4.1)."),
 dict(id="J11", element="The corpus theorizes its own functional form, under both names",
      observation="The Republic divides the poet's speech into speaking as himself and speaking 'as though he were Chryses himself', trying to make the hearer think the speaker someone other than himself; a poet who nowhere hid himself would make narration without mimesis (393a–d). The Poetics gives the same division, imitating 'narrating, or becoming something other', as Homer does (1448a20–24), and the rule that the poet should speak as little as possible in his own person, since in that respect he is no imitator (1460a7–8). The dialogues are built on that rule: the maker never speaks in his own voice (J1; Diogenes Laertius III.52).",
      loci=[("rep", "ὥσπερ αὐτὸς ὢν ὁ Χρύσης λέγει"), ("rep", "ὡς ἄλλος τις ὁ λέγων ἢ αὐτός"), ("rep", "εἰ δέ γε μηδαμοῦ ἑαυτὸν ἀποκρύπτοιτο ὁ ποιητής"), ("poe", "ἢ ἕτερόν τι γιγνόμενον"), ("poe", "Αὐτὸν γὰρ δεῖ τὸν ποιητὴν ἐλάχιστα λέγειν")],
      deposits=[1579], status="read (operator, 2026-11-02: 'do we really believe a mind driven to range over everything from plants shapes colors politics and god would not also be driven to range over functional form in their craft?')",
      succession_must_supply="Why the theory of a maker speaking as another, stated in both corpora in the same terms, is read as a theory of poetry only, while the reception grants the same mind range over plants, colours, animals, constitutions and the prime mover. Theorizing mimesis is not practising it under several names; the model owes why the range it grants over objects stops at the craft.",
      one_maker="The maker theorizes the operation it performs: speaking as little as possible in its own person, and becoming another (§1.2.2)."),
]

N = [
 dict(id="N1", element="The lexical instruments return a null on the maker-count",
      observation="Fifteen lexical features, every one destroyed by a control run in the same session; what the instruments return on maker-count is a null in either direction, symmetric between one maker and master-and-pupil. #1572; #1570.",
      deposits=[1572, 1570], bearing="Neither model gains credit from lexical distribution. The count is left to close reading, structural dependency and the comparator of §4.4 (design §4.2)."),
 dict(id="N2", element="The names carry recoverable signal, and separability decides nothing about makers",
      observation="Supervised attribution recovers the Aristotle/Theophrastus names at 0.798 balanced, outside the label-permutation null; operation partitions better on identical folds (0.860), the ordering descriptive; name recovery falls to 0.564 without the biological and botanical works. An assumed voice separates from its own author at 0.864 (Chatterton's Rowley), near three distinct tragedians at 0.872. No supervised separation, however strong, licenses an inference to distinct makers, in either direction. #1593.",
      deposits=[1593], bearing="Cuts against the claim, withdrawn in #1593, that the names sit at chance. The names are real stylistic signal; what produced the signal, persons or assigned functions, the instrument cannot say."),
 dict(id="N3", element="At the seam the names sort the texts",
      observation="Where the texts are continuous on the page, the stylometric profiles divide by name. #1586.",
      deposits=[1586], bearing="The local fact the succession model predicts directly. The one-maker reading must account for it as the voice of the continuation's operation (aporia against a completed account), and #1586 states which account carries which burden."),
]

rows, missing = [], []
for j in J:
    locs = []
    for key, ph in j["loci"]:
        ok = found(key, ph)
        locs.append({"seat_text": T[key], "phrase": ph, "located": ok})
        if not ok:
            missing.append((j["id"], ph))
    rows.append({**{k: v for k, v in j.items() if k != "loci"}, "loci": locs})
if missing:
    sys.exit(f"NOT LOCATED: {missing}")
doc = {"specification": "Legitimately Many — the joint pattern (design §4.4)", "date": "2026-11-02", "elements": rows, "limits": N,
       "comparator_test": "A documented succession of distinct persons producing one corpus satisfies the test when it shows J1–J9 and J11 jointly, at the grain stated, with the succession documented independently of the texts (Locating the Dependencies, #1602). None has been supplied (design §4.4).",
       "status": "specification; every observation cited to a deposit or a located phrase; nothing new measured"}
(H / "joint-pattern.json").write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
md = ["# Legitimately Many — the joint pattern", "", "Built by joint_pattern.py; every phrase located in its seat. Design §4.4, §6.1; draft §4. 2026-11-02.", ""]
for r in rows:
    md += [f"## {r['id']}. {r['element']}", "", r["observation"], "",
           "Loci: " + ("; ".join(f"{l['phrase']} ({l['seat_text']})" for l in r["loci"]) or "none (the finding is a deposit's measurement)"),
           f"Deposits: " + ", ".join(f"#{d}" for d in r["deposits"]) + f". Status: {r['status']}.", "",
           f"*Succession must supply:* {r['succession_must_supply']}", "", f"*One-maker reading:* {r['one_maker']}", ""]
md += ["## Limits, and what cuts the other way", ""]
for n in N:
    md += [f"### {n['id']}. {n['element']}", "", n["observation"], "", f"*Bearing:* {n['bearing']}", ""]
md += ["## The comparator test", "", doc["comparator_test"], ""]
(H / "joint-pattern.md").write_text("\n".join(md), encoding="utf-8")
print(len(rows), "elements,", sum(len(r["loci"]) for r in rows), "loci located;", len(N), "limits")
