#!/usr/bin/env python3
"""Draft of #1735 Revelation First v9 (not deposited): the folding-in of In the Midst of the Seven v1.1 (#1758) for Revelation First, at the author's
word of 2026-11-11 ("this is a new folding in, separate from the sappho chain, for revfirst"; 04:26 "yes, lets start the draft"). v8 is transformed in
place: VI.1 (the Philonic organization as the scene's ancestor, the alternatives counted; Zechariah 3 and the withheld name; Justin's apocalypse of
Jesus), IV.1 (the Haran Gawaita as a late witness to the seven-station form and the sealed book), VI.3 (a second arrow, to Hebrews 4.8-14, Newton's
own passage), VIII (their defeat conditions), IX, the abstract, the version history, the bibliography and the SPXI packet.
   python3 rebuild/revfirst-v9/draft_v9.py   ->  rebuild/revfirst-v9/REVFIRST-v9-draft.md"""
import json, pathlib, re
ROOT = pathlib.Path(__file__).resolve().parents[2]; H = pathlib.Path(__file__).parent
T = (ROOT / "data/texts/AXN-0BE9-text.md").read_text(encoding="utf-8")
def sub(old, new):
    global T; assert T.count(old) == 1, (old[:80], T.count(old)); T = T.replace(old, new)

# front matter and byline
sub("\nversion: v8\n", "\nversion: v9\n")
# abstract
sub("Philo’s lampstand of the dividing Logos is recorded as an extant antecedent for the figure in the midst of the seven (#1758).",
    "Philo’s lampstand of the dividing Logos is recorded as an extant antecedent for the figure in the midst of the seven (#1758). Version 9 adds, from the second version of that paper: the figure in the midst traced to Zechariah’s vision of Ἰησοῦς the high priest, robed in the ποδήρης and twice given the name Ἀνατολή, the name Philo takes for the Logos while withholding the one it was spoken to, with the Philonic organization of the scene set as its antecedent against the richer alternatives; and a second arrow, drawn and not yet run, from the opening scene to Hebrews 4.8–14, which gathers the two Joshuas, the dividing word and the great high priest named Jesus.")

# IV.1: the late witness
sub("The commission itself is in the text.\n",
    "The commission itself is in the text.\n\nA late witness keeps the same architecture in a revelation of its own. The Mandaean *Haran Gawaita*, copied in the Arab era, calls itself ‘the Great Revelation’, closes itself against change, ‘alter no word or command of the great Father of Glory’ (compare Rev. 22.18–19), and answers seven powers with seven guards, each installed over a named place and then set ‘at the seven corners of the House, upon the seven horns of the worlds’ (Drower 1953; #1758 v1.1, §§13.0, 13.6). It witnesses the seven-station form and the sealed book in a text that offers itself as a key; it is dated as late, and no dependence is claimed in either direction.\n")

# VI.1: the dependence, the alternatives, Zechariah 3, Justin
sub("The ancestry test reads the same evidence as an attested antecedent. Dependence on Philo is not claimed; the antecedent’s availability is what the test records.",
    "The ancestry test reads the same evidence as an attested antecedent, and the second version of *In the Midst of the Seven* argues the dependence (#1758 v1.1, §16.7). The richer alternatives are counted first. Wisdom has the Logos as a warrior from the royal thrones with a sharp sword, ‘ὁ παντοδύναμός σου λόγος ἀπʼ οὐρανῶν ἐκ θρόνων βασιλείων ἀπότομος πολεμιστὴς’ (Wis. 18.15), and the cosmos on the high priest’s robe (18.24); Isaiah has the mouth made a sharp sword, ‘ἔθηκεν τὸ στόμα μου ὡς μάχαιραν ὀξεῖαν’ (Isa. 49.2); Judges has the sun going forth in its strength, ‘ὡς ἔξοδος ἡλίου ἐν δυνάμει αὐτοῦ’ (Judg. 5.31 A), close to the face of 1.16; Ezekiel has one man robed in the ποδήρης in the midst of six, ‘ἐν μέσῳ αὐτῶν ἐνδιδυκὼς ποδήρη’ (Ezek. 9.2). These account for the sword, the solar face and the robe. None of them supplies the organization: the seven lamps as the seven planets with the sun in the middle, the dividing Logos as that middle, the Logos named ἀρχή (*De confusione* 146; Rev. 3.14) and Ἀνατολή. That organization is extant in Philo, most of it in one treatise, and the opening scene and the circuit of the letters are built on it. Whether the Seer read Philo or a tradition that carried his reading stays open; Wisdom, Alexandrian and near Philo in its Logos and its robe, shows one shape such a tradition could take. On the ancestry test the organization is an extant antecedent either way.\n\n"
    "The scene has a second extant antecedent, and it carries a name. Zechariah 3 is a vision of Ἰησοῦς the high priest, son of Iosedek, a different man from Moses’ successor. He is robed by command, ‘ἐνδύσατε αὐτὸν ποδήρη’ (Zech. 3.4); he is addressed, ‘ἄκουε δή, Ἰησοῦς ὁ ἱερεὺς ὁ μέγας’, and told ‘ἰδοὺ ἐγὼ ἄγω τὸν δοῦλόν μου Ἀνατολήν’ (3.8); a stone with seven eyes is set before him (3.9); the next vision is the lampstand of seven lamps (4.2); and the crowning oracle, ‘Ἀνατολὴ ὄνομα αὐτῷ’, is spoken to him again (6.11–12). Philo takes the name Ἀνατολή for the Logos from that oracle and stops one verse below its addressee; the prophet becomes ‘one of the companions of Moses’, and neither Zechariah nor his high priest is named anywhere in the thirty-one seated works of Philo, whose every Ἰησοῦς is the son of Nun (#1758 v1.1, §§2.1, 2.6, 4.1a–4.4b). Revelation’s figure in the midst is ‘ἐνδεδυμένον ποδήρη’ (1.13), and the book’s first words name him: ‘Ἀποκάλυψις Ἰησοῦ Χριστοῦ’ (1.1). The second century read Zechariah’s scene in the same terms. Justin sets the two Joshuas side by side, the son of Nun and ‘τὴν ἐπὶ τοῦ ἐν Βαβυλῶνι Ἰησοῦ ἱερέως γενομένου ἐν τῷ λαῷ ὑμῶν ἀποκάλυψιν’ (*Dial.* 115.4), and introduces his reading of it as ‘τὸν λόγον τὸν περὶ τῆς ἀποκαλύψεως Ἰησοῦ Χριστοῦ’ (116.1). On the ancestry test this is the asymmetry at its sharpest: the figure at the head of the book, in its robe, its office, its place among the lamps and its name, has extant antecedents in one prophetic vision and in its Alexandrian reading.")

# VI.3: the Hebrews arrow
sub("whether the testing of the sent is inherited or argued afresh, and whether Laodicea receives a letter as a station already addressed (#1758, §15.3).",
    "whether the testing of the sent is inherited or argued afresh, and whether Laodicea receives a letter as a station already addressed (#1758, §15.3).\n\n"
    "A second arrow runs from the same scene, and Newton drew part of it. Among the allusions he took for the Apocalypse in Hebrews were the two-edged sword of the word and the σαββατισμός (Section I). Both stand in Hebrews 4.8–14, and the passage holds more. In seven verses it gathers the son of Nun, ‘εἰ γὰρ αὐτοὺς Ἰησοῦς κατέπαυσεν’ (Heb. 4.8); the rest that remains, ‘ἀπολείπεται σαββατισμὸς τῷ λαῷ τοῦ Θεοῦ’ (4.9); the word ‘τομώτερος ὑπὲρ πᾶσαν μάχαιραν δίστομον’ (4.12); and ‘ἀρχιερέα μέγαν διεληλυθότα τοὺς οὐρανούς, Ἰησοῦν τὸν Υἱὸν τοῦ Θεοῦ’ (4.14), with the title the Septuagint gives Zechariah’s Ἰησοῦς, ‘ὁ ἱερεὺς ὁ μέγας’ (Zech. 3.8). Revelation’s opening scene holds the elements compressed into one figure: the two-edged sword, ‘ῥομφαία δίστομος ὀξεῖα’ (1.16), the high priest’s robe (1.13) and the name (1.1). Hebrews unfolds them as argument, and names the two Joshuas apart. The unit is that cluster. The common source is the strong alternative, since the dependence of Hebrews on Philo is long argued (Williamson 1970, against direct dependence; Thurston 1986 and Grindheim 2023, for it) and the cluster is Philonic in its parts (#1758 v1.1, §7a.8). The arrow has to survive a shared Alexandrian ancestor, and the test is whether Hebrews’ arrangement presupposes the concentrated figure or only the dispersed Philonic parts. The direction is not run here.")

# VIII: conditions
sub("Its strengthening condition is the general one: the features compressed in Revelation’s address and elaborated in the letters, with no better common antecedent.",
    "Its strengthening condition is the general one: the features compressed in Revelation’s address and elaborated in the letters, with no better common antecedent.\n\n"
    "The Philonic organization of VI.1 is defeated as the scene’s antecedent by an earlier or independent text that reads the seven lamps as the planets with the sun in the middle, makes the dividing Logos that middle and names the Logos from Zechariah’s oracle, without Philo; the Zechariah antecedent is not in question, being the Septuagint’s own. The Hebrews arrow of VI.3 is removed, without reversal, if Hebrews’ arrangement of the cluster is fully explained by the Philonic parts with no trace of the concentrated figure, and reversed if Revelation’s scene is shown to compress Hebrews 4.")

# IX
sub("The figure in the midst of the seven, whose form the field filed as an unconscious survival, is an attested antecedent on the ancestry test (VI.1).",
    "The figure in the midst of the seven, whose form the field filed as an unconscious survival, is an attested antecedent on the ancestry test (VI.1): its organization is extant in Philo, its robe, office and name in Zechariah’s vision of Ἰησοῦς the high priest. A fourth line, to Hebrews 4, is drawn beside the third, on ground Newton first marked.")

# version history
sub("Nothing in v7 was removed, and no finding of v7 changed.",
    "Nothing in v7 was removed, and no finding of v7 changed.\n\n"
    "v9 (11 November 2026, in place), at the author's word ('this is a new folding in, separate from the sappho chain, for revfirst'), from the second version of *In the Midst of the Seven* (#1758 v1.1). Added: in VI.1, the dependence on the Philonic organization with the richer alternatives counted (Wisdom 18.15–16 and 18.24, Isaiah 49.2, Judges 5.31, Ezekiel 9.2), Zechariah 3 and the withheld name as a second extant antecedent, and Justin's apocalypse of the high priest; in IV.1, the *Haran Gawaita* as a late witness to the seven-station form and the sealed book; in VI.3, the arrow to Hebrews 4.8–14, drawn and not yet run; their conditions in VIII; a sentence in IX; the abstract's last sentence; five entries in the bibliography; the SPXI packet. Nothing in v8 was removed, and no finding of v8 changed.")

# bibliography
sub("**Hahneman, G.M.**", "**Grindheim, S.** 2023 ‘Direct Dependence on Philo in the Epistle to the Hebrews’, NovT 65: 517–43.\n\n**Hahneman, G.M.**")
sub("**Eng, D.K.**", "**Drower, E.S.** 1953 The Haran Gawaita and the Baptism of Hibil-Ziwa (Studi e Testi, 176; Vatican City: Biblioteca Apostolica Vaticana).\n\n**Eng, D.K.**")
sub("**Koester, C.R.**", "**Justin Martyr** Dialogus cum Tryphone, ed. G. Archambault (Paris: Picard, 1909).\n\n**Koester, C.R.**")
sub("**Trobisch, D.**", "**Thurston, R.W.** 1986 ‘Philo and the Epistle to the Hebrews’, EvQ 58: 133–43.\n\n**Trobisch, D.**")
sub("**Wilson, J.C.**", "**Williamson, R.** 1970 Philo and the Epistle to the Hebrews (ALGHJ, 4; Leiden: Brill).\n\n**Wilson, J.C.**")
sub("Provenance: Journal of Forensic Semiotics (Crimson Hexagonal Archive, #1758).", "Provenance: Journal of Forensic Semiotics (Crimson Hexagonal Archive, #1758; v1.1, 11 November 2026).")

# packet
a = T.index("```json\n") + 8; b = T.index("\n```", a); P = json.loads(T[a:b])
P["version"] = "9"; P["dateModified"] = "2026-11-11"
P["spxi:pillarStatus"] = "v9, versioned in place on 2026-11-11; the seed article of the Revelation First programme's three claims, with its framework hologram EA-HK-REVFIRST-01 (#1755)"
P["spxi:contributesOperators"].append({"name": "the withheld name", "type": "ancestry case", "role": "the figure in the midst traced to Zechariah's vision of Ἰησοῦς the high priest, whose name Philo withholds where he takes Ἀνατολή for the Logos; Revelation names the figure"})
P["spxi:centralPropositions"] += ["the figure in the midst has extant antecedents in Philo's organization of the lampstand and in Zechariah's vision of Ἰησοῦς the high priest, robed in the ποδήρης and twice given the name Ἀνατολή",
                                  "Hebrews 4.8–14 gathers the son of Nun, the two-edged word and the great high priest named Jesus: an arrow drawn from Revelation's opening scene and not yet run"]
P["spxi:falsifiers"]["interpretiveChallenges"] += "; an earlier or independent text with Philo's organization of the lampstand and the Logos-name from Zechariah's oracle"
P["spxi:falsifiers"]["directionalChallenges"] += "; Hebrews 4's cluster fully explained by the Philonic parts, or Revelation's scene shown to compress Hebrews 4"
P["spxi:versionHistory"].append({"version": "9", "date": "2026-11-11", "note": "from #1758 v1.1: the Philonic organization and Zechariah 3 as the scene's antecedents, Justin's apocalypse of the high priest, the Gawaita as late witness, the arrow to Hebrews 4"})
T = T[:a] + json.dumps(P, ensure_ascii=False, indent=1) + T[b:]
(H / "REVFIRST-v9-draft.md").write_text(T, encoding="utf-8"); print("written", len(T.split()), "words")
