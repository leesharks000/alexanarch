"""The derivations, as data. Operators and members are declared here before the run; the file is frozen by its hash in the run's output.
   python3 derivations.py > derivations.json"""
import json, hashlib, pathlib
def m(i, gloss, greek, rx, in_seed=True): return {"id": i, "gloss": gloss, "greek": greek, "rx": rx, "in_seed": in_seed}
D = []
def d(**k): D.append(k)
ZECH, DAN = "lxx:Ζαχαριας 12:10", "lxx:Δανιηλ_(Theodotionis_versio) 7:13"
R17 = [m("clouds", "with the clouds", "μετὰ τῶν νεφελῶν", r"νεφελ"), m("see", "will see", "ὄψεται", r"\bοψ(ε|ο)"), m("pierced", "they pierced", "ἐξεκέντησαν", r"εξεκεντ"),
       m("mourn", "will mourn", "κόψονται", r"κοψ"), m("tribes", "all the tribes of the earth", "πᾶσαι αἱ φυλαὶ τῆς γῆς", r"φυλαι τησ γησ")]
d(id="rev1.7→matt24.30", family="Gospels: partition", title="The mourning tribes", seed="gnt:Rev 1:7", members=R17, target="gnt:Matt 24:30",
  steps=[{"op": "PARTITION", "keep": ["clouds", "see", "mourn", "tribes"]}, {"op": "REORDER", "order": ["mourn", "tribes", "see", "clouds"]}],
  controls=[{"loc": "gnt:Mark 13:26", "label": "Mark's parallel"}, {"loc": ZECH, "label": "Septuagint, Zech 12:10"}, {"loc": DAN, "label": "Septuagint, Dan 7:13 (Theodotion)"}], records=[1746, 1747])
d(id="rev1.7→john19.37", family="Gospels: partition", title="They pierced", seed="gnt:Rev 1:7", members=R17, target="gnt:John 19:37",
  steps=[{"op": "PARTITION", "keep": ["see", "pierced"]}, {"op": "CITE-AS-SCRIPTURE", "marker": r"γραφη|γεγραπται"}],
  controls=[{"loc": ZECH, "label": "Septuagint, Zech 12:10"}, {"loc": "gnt:Matt 24:30", "label": "Matthew's half"}])
R35 = [m("confess", "I will confess", "ὁμολογήσω", r"ομολογησ"), m("father", "before my Father", "τοῦ Πατρός μου", r"πατροσ μου"), m("angels", "before the angels", "τῶν ἀγγέλων", r"αγγελων")]
d(id="rev3.5→matt10.32", family="Gospels: partition", title="The confession, Matthew's half", seed="gnt:Rev 3:5", members=R35, target="gnt:Matt 10:32",
  steps=[{"op": "PARTITION", "keep": ["confess", "father"]}], controls=[{"loc": "gnt:Luke 12:8", "label": "Luke's half"}], records=[1747])
d(id="rev3.5→luke12.8", family="Gospels: partition", title="The confession, Luke's half", seed="gnt:Rev 3:5", members=R35, target="gnt:Luke 12:8",
  steps=[{"op": "PARTITION", "keep": ["confess", "angels"]}], controls=[{"loc": "gnt:Matt 10:32", "label": "Matthew's half"}], records=[1747])
R199 = [m("supper", "the supper", "τὸ δεῖπνον", r"δειπν"), m("wedding", "of the wedding", "τοῦ γάμου", r"γαμ"), m("called", "those called", "κεκλημένοι", r"κεκλημεν")]
d(id="rev19.9→matt22.3", family="Gospels: partition", title="The wedding", seed="gnt:Rev 19:9", members=R199, target="gnt:Matt 22:3",
  steps=[{"op": "PARTITION", "keep": ["wedding", "called"]}, {"op": "REORDER", "order": ["called", "wedding"]}], controls=[{"loc": "gnt:Luke 14:17", "label": "Luke's half"}])
d(id="rev19.9→luke14.17", family="Gospels: partition", title="The supper", seed="gnt:Rev 19:9", members=R199, target="gnt:Luke 14:17",
  steps=[{"op": "PARTITION", "keep": ["supper", "called"]}], controls=[{"loc": "gnt:Matt 22:3", "label": "Matthew's half"}])
R52 = [m("strong", "strong", "ἰσχυρόν", r"ισχυρ"), m("proclaim", "proclaiming", "κηρύσσοντα", r"κηρυσσ"), m("worthy", "worthy", "ἄξιος", r"αξιοσ"), m("loose", "to loose", "λῦσαι", r"\bλυσ(αι|ω)"),
       m("seals", "its seals", "τὰς σφραγῖδας", r"σφραγιδ"), m("fit", "fit", "ἱκανός", r"ικανοσ", False), m("strap", "the strap of his sandal", "τὸν ἱμάντα", r"ιμαντα", False)]
d(id="rev5.2→mark1.7", family="Gospels: partition", title="Who is worthy to loose: the stronger one", seed="gnt:Rev 5:2", members=R52, target="gnt:Mark 1:7",
  steps=[{"op": "SUBSTITUTE", "old": "worthy", "new": "fit"}, {"op": "SUBSTITUTE-OBJECT", "old": "seals", "new": "strap"}, {"op": "REORDER", "order": ["proclaim", "strong", "fit", "loose", "strap"]}],
  controls=[{"loc": "gnt:John 1:27", "label": "John's half"}, {"loc": "gnt:Matt 3:11", "label": "Matthew's parallel"}], records=[639])
d(id="rev5.2→john1.27", family="Gospels: partition", title="Who is worthy to loose: worthy", seed="gnt:Rev 5:2", members=R52, target="gnt:John 1:27",
  steps=[{"op": "PARTITION", "keep": ["worthy", "loose", "seals"]}, {"op": "SUBSTITUTE-OBJECT", "old": "seals", "new": "strap"}], controls=[{"loc": "gnt:Mark 1:7", "label": "Mark's half"}])
R33 = [m("watch", "watch", "γρηγορήσῃς", r"γρηγορ"), m("thief", "as a thief", "ὡς κλέπτης", r"κλεπτ"), m("hour", "what hour", "ποίαν ὥραν", r"ποια\w? ωρα"), m("nightwatch", "in what watch of the night", "ποίᾳ φυλακῇ", r"ποια φυλακη", False)]
d(id="rev3.3→matt24.43", family="Gospels: partition", title="The thief, Matthew's half", seed="gnt:Rev 3:3", members=R33, target="gnt:Matt 24:43",
  steps=[{"op": "SUBSTITUTE", "old": "hour", "new": "nightwatch"}, {"op": "REORDER", "order": ["nightwatch", "thief", "watch"]}], controls=[{"loc": "gnt:Luke 12:39", "label": "Luke's half"}], records=[1747])
d(id="rev3.3→luke12.39", family="Gospels: partition", title="The thief, Luke's half", seed="gnt:Rev 3:3", members=R33, target="gnt:Luke 12:39",
  steps=[{"op": "PARTITION", "keep": ["thief", "hour"]}, {"op": "REORDER", "order": ["hour", "thief"]}], controls=[{"loc": "gnt:Matt 24:43", "label": "Matthew's half"}], records=[1747])
d(id="rev16.18+1.14→matt28.2-3", family="Gospels: Matthew against Mark", title="The tomb", seed="gnt:Rev 16:18 + Rev 1:14",
  members=[m("quake", "an earthquake", "σεισμός", r"σεισμοσ"), m("happened", "there was", "ἐγένετο", r"εγενετο"), m("great", "great", "μέγας", r"μεγασ"), m("hair", "his hair", "αἱ τρίχες", r"τριχεσ"),
           m("snow", "white as snow", "λευκὸν ὡς χιών", r"λευκον ωσ χιων"), m("clothing", "his clothing", "τὸ ἔνδυμα", r"ενδυμα", False)],
  steps=[{"op": "PARTITION", "keep": ["quake", "happened", "great", "hair", "snow"]}, {"op": "EVENT"}, {"op": "TRANSFER-ATTRIBUTE", "old": "hair", "new": "clothing"}], target="gnt:Matt 28:2-3",
  controls=[{"loc": "gnt:Mark 16:4-5", "label": "Mark's tomb"}, {"loc": "gnt:Luke 24:2-4", "label": "Luke's tomb"}, {"loc": DAN.replace("7:13", "7:9"), "label": "Septuagint, Dan 7:9"}],
  note="The seed is two verses from two places of the Apocalypse; Matthew has them in two consecutive verses. Rev 16:18 has other words between the three kept here.")
d(id="rev6.12→matt8.24", family="Gospels: Matthew against Mark", title="The storm", seed="gnt:Rev 6:12",
  members=[m("quake", "an earthquake", "σεισμός", r"σεισμοσ"), m("great", "great", "μέγας", r"μεγασ"), m("happened", "there was", "ἐγένετο", r"εγενετο")],
  steps=[{"op": "EVENT"}], target="gnt:Matt 8:24", controls=[{"loc": "gnt:Mark 4:37", "label": "Mark's storm"}, {"loc": "gnt:Luke 8:23", "label": "Luke's storm"}])
d(id="rev13.13-14→john2.11", family="John: the signs reversed", title="Who does the signs", seed="gnt:Rev 13:13-14",
  members=[m("does", "does", "ποιεῖ", r"\bποιει\b|εποιησεν"), m("signs", "signs", "σημεῖα", r"σημει"), m("beast", "before the beast", "τοῦ θηρίου", r"θηρι"), m("jesus", "Jesus", "ὁ Ἰησοῦς", r"ιησουσ", False)],
  steps=[{"op": "REVERSE-DOER", "old": "beast", "new": "jesus"}], target="gnt:John 2:11", controls=[{"loc": "gnt:Mark 13:22", "label": "Mark: false prophets will give signs"}],
  note="In Revelation every sign that is done is the adversary's (13:13, 13:14, 16:14, 19:20); the seven plagues are a sign seen (15:1).")
JER = "lxx:Ιερεμιας 25:10"
d(id="rev18.23→john3.29", family="John: the signs reversed", title="The bridegroom's voice", seed="gnt:Rev 18:23",
  members=[m("voice", "the voice", "φωνή", r"φων"), m("groom", "of the bridegroom", "νυμφίου", r"νυμφιου"), m("heard", "heard", "ἀκουσθῇ", r"ακου")],
  steps=[{"op": "UNDO", "negation": r"ου μη ακουσθη"}, {"op": "REORDER", "order": ["heard", "voice", "groom"]}], target="gnt:John 3:29", controls=[{"loc": JER, "label": "Septuagint, Jer 25:10"}, {"loc": "gnt:Matt 9:15", "label": "Matthew: the bridegroom taken away"}])
d(id="rev18.23→john5.35", family="John: the signs reversed", title="The lamp", seed="gnt:Rev 18:23",
  members=[m("light", "light", "φῶς", r"\bφω(σ|τι)\b"), m("lamp", "of a lamp", "λύχνου", r"λυχν"), m("shine", "shine", "φάνῃ", r"\bφα(νη|ινων|ινει)")],
  steps=[{"op": "UNDO", "negation": r"ου μη φανη"}, {"op": "REORDER", "order": ["lamp", "shine", "light"]}], target="gnt:John 5:35", controls=[{"loc": JER, "label": "Septuagint, Jer 25:10"}, {"loc": "gnt:Matt 5:15", "label": "Matthew: the lamp on the stand"}])
d(id="rev18.21→john11.41", family="John: the signs reversed", title="The stone", seed="gnt:Rev 18:21",
  members=[m("took", "took up", "ἦρεν", r"\bηρ(ε|α)ν\b"), m("stone", "a stone", "λίθον", r"λιθον")],
  steps=[{"op": "UNDO", "negation": r"ου μη ευρεθη ετι"}], target="gnt:John 11:41", controls=[{"loc": "gnt:Mark 16:4", "label": "Mark: the stone rolled back"}, {"loc": "lxx:Ιερεμιας 28:63", "label": "Septuagint, Jer 28:63 (51:63)"}])
d(id="rev19.18→john6.53", family="John: the signs reversed", title="Eat the flesh", seed="gnt:Rev 19:18",
  members=[m("eat", "that you may eat", "φάγητε", r"φαγητε"), m("flesh", "the flesh", "σάρκας", r"σαρκα"), m("kings", "of kings", "βασιλέων", r"βασιλεων"), m("sonofman", "of the Son of Man", "τοῦ Υἱοῦ τοῦ ἀνθρώπου", r"υιου του ανθρωπου", False)],
  steps=[{"op": "PARTITION", "keep": ["eat", "flesh", "kings"]}, {"op": "SUBSTITUTE-OBJECT", "old": "kings", "new": "sonofman"}], target="gnt:John 6:53",
  controls=[{"loc": "lxx:Ιεζεκιηλ 39:18", "label": "Septuagint, Ezek 39:18"}, {"loc": "gnt:Mark 14:22", "label": "Mark: take, this is my body"}])
d(id="rev16.4→john2.9", family="John: the signs reversed", title="Water become", seed="gnt:Rev 16:4",
  members=[m("water", "the waters", "τῶν ὑδάτων", r"υδ(ατ|ωρ)"), m("became", "became", "ἐγένετο", r"εγενετο|γεγενημεν"), m("blood", "blood", "αἷμα", r"\bαιμα"), m("wine", "wine", "οἶνον", r"οινον", False)],
  steps=[{"op": "SUBSTITUTE-OBJECT", "old": "blood", "new": "wine"}, {"op": "REORDER", "order": ["water", "wine", "became"]}], target="gnt:John 2:9", controls=[{"loc": "lxx:Εξοδος 7:20", "label": "Septuagint, Exod 7:20"}])
# Philo upstream, and through Revelation
d(id="philo.her219→rev1.12-13", family="Philo → Revelation", title="The lampstand and the one in the midst", seed="philo:Quis_rerum_divinarum_heres_sit 219",
  members=[m("middle", "the middle", "ὑπὸ μέσου", r"\bμεσ(ου|ω)\b"), m("seventh", "the seventh", "τοῦ ἑβδόμου", r"εβδομ"), m("logos", "the Logos", "λόγου", r"\bλογου"), m("lampstand", "the lampstand", "ἡ λυχνία", r"\bλυχνια\b"),
           m("seven", "seven", "ἑπτά", r"\bεπτα\b", False), m("lampstands", "lampstands", "λυχνίας, λυχνιῶν", r"λυχνι(ασ|ων)\b", False), m("sonofman", "one like a son of man", "ὅμοιον υἱὸν ἀνθρώπου", r"υιον ανθρωπου", False)],
  steps=[{"op": "SUBSTITUTE", "old": "seventh", "new": "seven"}, {"op": "STATION", "old": "lampstand", "new": "lampstands"}, {"op": "SUBSTITUTE", "old": "logos", "new": "sonofman"}, {"op": "REORDER", "order": ["seven", "lampstands", "middle", "sonofman"]}],
  target="gnt:Rev 1:12-13", controls=[{"loc": "lxx:Ζαχαριας 4:2", "label": "Septuagint, Zech 4:2"}, {"loc": "gnt:Heb 9:2", "label": "Hebrews 9:2"}], records=[1758],
  note="#1758 §9, §11.1b; 17.1(i), (k). The Septuagint's lampstand and Hebrews' are one; the seven lampstands are the Apocalypse's.")
d(id="philo.deus75→rev2.17", family="Philo → Revelation", title="The vote", seed="philo:Quod_deus_sit_immutabilis 75",
  members=[m("condemning", "condemning", "καταδικάζουσαν", r"καταδικαζ"), m("vote", "vote", "ψῆφον", r"ψηφον"), m("bring", "will bring", "οἴσει", r"\bοισει\b|ηνεγκ"), m("white", "white", "λευκήν", r"λευκην", False), m("give", "I will give", "δώσω", r"δωσω", False)],
  steps=[{"op": "SUBSTITUTE", "old": "condemning", "new": "white"}, {"op": "SUBSTITUTE", "old": "bring", "new": "give"}, {"op": "REORDER", "order": ["give", "vote", "white"]}],
  target="gnt:Rev 2:17", controls=[{"loc": "gnt:Acts 26:10", "label": "Acts 26:10, the other ψῆφος of the New Testament"}], records=[1758], note="#1758 §7b.1, 7b.9; 17.1(q).")
d(id="philo.deus75→acts26.10", family="Philo → Revelation → downstream: which form", title="The vote in Acts: Philo's form or Revelation's", seed="philo:Quod_deus_sit_immutabilis 75",
  members=[m("vote", "vote", "ψῆφον", r"ψηφον"), m("bring", "bring (φέρω)", "οἴσει", r"\bοισει\b|ηνεγκ")], steps=[{"op": "REORDER", "order": ["bring", "vote"]}],
  target="gnt:Acts 26:10", controls=[{"loc": "gnt:Rev 2:17", "label": "Revelation's form (a white vote, given)"}],
  note="The test of 5.2: Acts has the vote in Philo's form, brought against, a vote of condemnation. It does not have Revelation's white vote. At this locus the arrow does not run through Revelation.")
d(id="philo.leg3.174-175→rev2.17", family="Philo → Revelation", title="The manna", seed="philo:Legum_allegoriarum_libri_i_iii 174-175",
  members=[m("manna", "the manna", "τὸ μάννα", r"μαννα"), m("unknown", "did not know", "οὐκ ᾔδεισαν", r"ουκ ηδεισαν"), m("fathers", "the fathers", "οἱ πατέρες", r"πατερεσ"), m("hidden", "hidden", "κεκρυμμένου", r"κεκρυμμεν", False)],
  steps=[{"op": "PARTITION", "keep": ["manna", "unknown"]}, {"op": "HIDE", "old": "unknown", "new": "hidden"}], target="gnt:Rev 2:17",
  controls=[{"loc": "lxx:Δευτερονομιον 8:3", "label": "Septuagint, Deut 8:3"}, {"loc": "gnt:John 6:31", "label": "John 6:31"}], records=[1758], note="#1758 §7b.5.")
d(id="rev2.17→heb9.4", family="Philo → Revelation → downstream: which form", title="The manna in the ark (corrected: no derived state)", seed="gnt:Rev 2:17",
  members=[m("manna", "the manna", "τοῦ μάννα", r"μαννα"), m("hidden", "hidden", "κεκρυμμένου", r"κεκρυμμεν")],
  steps=[{"op": "PARTITION", "keep": ["manna"]}], target="gnt:Heb 9:4",
  controls=[{"loc": "gnt:John 6:49", "label": "John 6:49"}, {"loc": "lxx:Εξοδος 16:33", "label": "Septuagint, Exod 16:33"}],
  note="Corrected at v0.8. v0.3 read Hebrews' περικεκαλυμμένην as the manna 'covered', a state derived from Revelation's 'hidden'. In the seat the participle is the ark's: 'the ark of the covenant covered on every side with gold', and the manna is in a golden jar, as at Exod 16:33. Hebrews has the manna and not Revelation's hiddenness; the Septuagint supplies it. A control fits.")
d(id="philo.mos2.114→rev19.12", family="Philo → Revelation", title="The name on the head", seed="philo:De_vita_Mosis_lib_i_ii_ 114#2",
  members=[m("crown", "like a crown", "ὡσανεὶ στέφανος", r"στεφανοσ"), m("name", "of a name", "ὀνόματος", r"ονομα"), m("engraved", "engravings", "γλυφάς", r"γλυφασ"), m("noother", "no other at all", "ἄλλῳ δ’ οὐδενί", r"ουδενι"),
           m("diadems", "diadems", "διαδήματα", r"διαδηματα", False), m("written", "written", "γεγραμμένον", r"γεγραμμεν", False), m("noone", "no one knows but himself", "οὐδεὶς οἶδεν", r"ουδεισ οιδεν", False)],
  steps=[{"op": "SUBSTITUTE", "old": "crown", "new": "diadems"}, {"op": "SUBSTITUTE", "old": "engraved", "new": "written"}, {"op": "SUBSTITUTE", "old": "noother", "new": "noone"}, {"op": "REORDER", "order": ["diadems", "name", "written", "noone"]}],
  target="gnt:Rev 19:12", controls=[{"loc": "gnt:Rev 2:17", "label": "Rev 2:17, the new name"}, {"loc": "lxx:Εξοδος 28:32", "label": "Septuagint, Exod 28:32 (36)"}], records=[1758], note="#1758 §7b.3. Philo: 'four engravings of a name'. Rev 19:11–16 gives the rider four names.")

# ── the four Gospels, from the profile of 2026-11-26 13:45 (law.py): each Gospel's own links, read, then stated in the operators
d(id="rev1.17→matt28.4-5", family="Matthew", title="As dead; fear not", seed="gnt:Rev 1:17",
  members=[m("fell", "I fell at his feet", "ἔπεσα", r"επεσα"), m("asdead", "as dead", "ὡς νεκρός", r"ωσ νεκρο"), m("fearnot", "fear not", "Μὴ φοβοῦ", r"μη φοβ")],
  steps=[{"op": "PARTITION", "keep": ["asdead", "fearnot"]}, {"op": "EVENT"}], target="gnt:Matt 28:4-5",
  controls=[{"loc": "gnt:Mark 16:5-6", "label": "Mark's tomb"}, {"loc": "gnt:Luke 24:4-5", "label": "Luke's tomb"}], note="With the earthquake and 'white as snow' (above), Matt 28:2–5 holds Rev 1:14, 1:17 and 16:18.")
d(id="rev19.9+19.21+17.14→matt22.3-14", family="Matthew", title="The wedding parable, gathered", seed="gnt:Rev 19:9 + Rev 19:21 + Rev 17:14",
  members=[m("supper", "the supper", "τὸ δεῖπνον", r"δειπν"), m("wedding", "of the wedding", "τοῦ γάμου", r"γαμ"), m("called", "those called", "κεκλημένοι", r"κεκλημεν"), m("rest", "the rest", "οἱ λοιποί", r"\bλοιποι"),
           m("killed", "were killed", "ἀπεκτάνθησαν", r"απεκτ(ανθησαν|ειναν)"), m("kletoi", "called", "κλητοί", r"\bκλητοι"), m("chosen", "chosen", "ἐκλεκτοί", r"εκλεκτοι")],
  steps=[{"op": "PARTITION", "keep": ["wedding", "called", "rest", "killed", "kletoi", "chosen"]}, {"op": "REORDER", "order": ["called", "wedding", "rest", "killed", "kletoi", "chosen"]}], target="gnt:Matt 22:3-14",
  controls=[{"loc": "gnt:Luke 14:16-24", "label": "Luke's supper"}], note="Matthew's parable has what Luke's lacks: the wedding, the rest who kill and are destroyed by the king's armies (στρατεύματα: in the Gospels only here and Luke 23:11; Rev 19:14, 19), the garment, 'many called, few chosen'.")
d(id="rev14.19→matt21.33", family="Matthew", title="The winepress", seed="gnt:Rev 14:19",
  members=[m("vine", "the vine", "τὴν ἄμπελον", r"αμπελ"), m("press", "the winepress", "τὴν ληνόν", r"\bληνο")], steps=[{"op": "EVENT"}], target="gnt:Matt 21:33",
  controls=[{"loc": "gnt:Mark 12:1", "label": "Mark: ὑπολήνιον"}, {"loc": "lxx:Ησαιας 5:2", "label": "Septuagint, Isa 5:2: προλήνιον"}])
d(id="rev2.10→matt17.12", family="Matthew", title="About to suffer", seed="gnt:Rev 2:10",
  members=[m("you", "you are about", "μέλλεις", r"μελλεισ"), m("suffer", "to suffer", "πάσχειν", r"πασχειν"), m("he", "is about", "μέλλει", r"μελλει\b", False)],
  steps=[{"op": "PARTITION", "keep": ["you", "suffer"]}, {"op": "TRANSFER-ATTRIBUTE", "old": "you", "new": "he"}], target="gnt:Matt 17:12", controls=[{"loc": "gnt:Mark 9:12", "label": "Mark's parallel"}])
d(id="rev1.3→matt26.18", family="Matthew", title="The time is near", seed="gnt:Rev 1:3",
  members=[m("time", "the time", "ὁ καιρός", r"καιροσ"), m("near", "near", "ἐγγύς", r"εγγυσ")], steps=[{"op": "PARTITION", "keep": ["time", "near"]}, {"op": "EVENT"}], target="gnt:Matt 26:18",
  controls=[{"loc": "gnt:Mark 14:14", "label": "Mark's parallel"}, {"loc": "gnt:Luke 21:8", "label": "Luke: ὁ καιρὸς ἤγγικεν"}])
d(id="rev7.9→mark16.5", family="Mark", title="The white robe", seed="gnt:Rev 7:9",
  members=[m("clothed", "clothed in", "περιβεβλημένους", r"περιβεβλημεν"), m("robe", "robes", "στολάς", r"στολ"), m("white", "white", "λευκάς", r"λευκ")],
  steps=[{"op": "PARTITION", "keep": ["clothed", "robe", "white"]}, {"op": "EVENT"}], target="gnt:Mark 16:5",
  controls=[{"loc": "gnt:Matt 28:3", "label": "Matthew's tomb"}, {"loc": "gnt:Luke 24:4", "label": "Luke's tomb"}, {"loc": "gnt:John 20:12", "label": "John's tomb"}],
  note="Four tombs, four whites, each with its own place in the Apocalypse: Mark's στολὴν λευκήν (7:9), Matthew's λευκὸν ὡς χιών (1:14), John's ἐν λευκοῖς (3:4), Luke's ἀστραπτούσῃ.")
d(id="rev6.15+19.17→mark6.21", family="Mark", title="Herod's supper", seed="gnt:Rev 6:15 + Rev 19:17",
  members=[m("magnates", "the great ones", "οἱ μεγιστᾶνες", r"μεγιστα"), m("chiliarchs", "the commanders of thousands", "οἱ χιλίαρχοι", r"χιλιαρχ"), m("supper", "the supper", "τὸ δεῖπνον", r"δειπνον"),
           m("god", "of God", "τοῦ Θεοῦ", r"του θεου"), m("herod", "Herod", "Ἡρῴδης", r"ηρωδησ", False)],
  steps=[{"op": "PARTITION", "keep": ["magnates", "chiliarchs", "supper", "god"]}, {"op": "REVERSE-DOER", "old": "god", "new": "herod"}, {"op": "REORDER", "order": ["herod", "supper", "magnates", "chiliarchs"]}], target="gnt:Mark 6:21",
  controls=[{"loc": "gnt:Matt 14:6", "label": "Matthew's parallel"}, {"loc": "gnt:Luke 14:16", "label": "Luke's great supper"}],
  note="μεγιστᾶνες: Mark 6:21, Rev 6:15 and 18:23, and nowhere else in the New Testament. The supper where the Baptist's head is served has the guests of the supper of God.")
d(id="rev9.3-4→luke10.19", family="Luke", title="Authority, scorpions, harm", seed="gnt:Rev 9:3-4",
  members=[m("given", "was given to them", "ἐδόθη αὐταῖς", r"εδοθη αυτ"), m("authority", "authority", "ἐξουσία", r"εξουσια"), m("scorpions", "scorpions", "οἱ σκορπίοι", r"σκορπι"), m("hurt", "hurt", "ἀδικήσουσιν", r"αδικησ"),
           m("givenyou", "I have given you", "δέδωκα ὑμῖν", r"δεδωκα υμιν", False)],
  steps=[{"op": "PARTITION", "keep": ["given", "authority", "scorpions", "hurt"]}, {"op": "REVERSE-DOER", "old": "given", "new": "givenyou"}, {"op": "NEGATE", "negation": r"ου μη αδικησ"}], target="gnt:Luke 10:19",
  controls=[{"loc": "gnt:Mark 16:18", "label": "Mark 16:18"}, {"loc": "lxx:Ψαλμοι 90:13", "label": "Septuagint, Ps 90:13"}], note="With Luke 10:18 (Satan fallen from heaven; Rev 12:9, 9:1) and 10:20 (names written in heaven; Rev 13:8, 21:27).")
d(id="rev5.4→luke4.17", family="Luke", title="The book opened", seed="gnt:Rev 5:4",
  members=[m("found", "was found", "εὑρέθη", r"ευρ(εθη|εν)\b"), m("open", "to open", "ἀνοῖξαι", r"ανοιξ"), m("book", "the book", "τὸ βιβλίον", r"βιβλιον")],
  steps=[{"op": "UNDO", "negation": r"ουδεισ"}, {"op": "REORDER", "order": ["open", "book", "found"]}], target="gnt:Luke 4:17", controls=[{"loc": "gnt:Mark 6:2", "label": "Mark's Nazareth"}, {"loc": "gnt:Matt 13:54", "label": "Matthew's Nazareth"}])
d(id="rev19.8+19.14→luke23.11", family="Luke", title="Herod's armies, the bright clothing", seed="gnt:Rev 19:8 + Rev 19:14",
  members=[m("clothed", "to be clothed", "περιβάληται", r"περιβαλ"), m("bright", "bright", "λαμπρόν", r"λαμπρ"), m("armies", "the armies", "τὰ στρατεύματα", r"στρατευμα"), m("heaven", "in heaven", "ἐν τῷ οὐρανῷ", r"ουρανω"), m("herod", "Herod", "ὁ Ἡρῴδης", r"ηρωδησ", False)],
  steps=[{"op": "PARTITION", "keep": ["clothed", "bright", "armies", "heaven"]}, {"op": "REVERSE-DOER", "old": "heaven", "new": "herod"}, {"op": "REORDER", "order": ["herod", "armies", "clothed", "bright"]}], target="gnt:Luke 23:11",
  controls=[{"loc": "gnt:Mark 15:17", "label": "Mark: the purple"}, {"loc": "gnt:Matt 27:28", "label": "Matthew: the scarlet"}])
R1616 = [m("place", "the place", "τὸν τόπον", r"τοπον"), m("called", "called", "τὸν καλούμενον", r"καλουμενον"), m("hebrew", "in Hebrew", "Ἑβραϊστί", r"εβραιστι"), m("said", "said", "λεγόμενον", r"λεγομενον|λεγεται", False)]
d(id="rev16.16→luke23.33", family="Luke", title="The place called", seed="gnt:Rev 16:16", members=R1616, steps=[{"op": "PARTITION", "keep": ["place", "called"]}], target="gnt:Luke 23:33",
  controls=[{"loc": "gnt:John 19:17", "label": "John's half"}, {"loc": "gnt:Mark 15:22", "label": "Mark's parallel"}, {"loc": "gnt:Matt 27:33", "label": "Matthew's parallel"}])
d(id="rev16.16→john19.17", family="John", title="The place, in Hebrew", seed="gnt:Rev 16:16", members=R1616, steps=[{"op": "SUBSTITUTE", "old": "called", "new": "said"}, {"op": "REORDER", "order": ["said", "place", "hebrew"]}], target="gnt:John 19:17",
  controls=[{"loc": "gnt:Luke 23:33", "label": "Luke's half"}, {"loc": "gnt:Mark 15:22", "label": "Mark's parallel"}], note="Ἑβραϊστί: five times in John, twice in Revelation (9:11; 16:16), nowhere else in the New Testament.")
d(id="rev11.8→john19.20", family="John", title="The city where he was crucified", seed="gnt:Rev 11:8",
  members=[m("city", "of the city", "τῆς πόλεως", r"πολεωσ"), m("where", "where", "ὅπου", r"οπου"), m("lord", "their Lord", "ὁ Κύριος αὐτῶν", r"κυριοσ αυτων"), m("crucified", "was crucified", "ἐσταυρώθη", r"εσταυρωθη"), m("jesus", "Jesus", "ὁ Ἰησοῦς", r"ιησουσ", False)],
  steps=[{"op": "PARTITION", "keep": ["city", "where", "lord", "crucified"]}, {"op": "SUBSTITUTE", "old": "lord", "new": "jesus"}, {"op": "REORDER", "order": ["city", "where", "crucified", "jesus"]}], target="gnt:John 19:20",
  controls=[{"loc": "gnt:Luke 23:33", "label": "Luke"}, {"loc": "gnt:Heb 13:12", "label": "Hebrews 13:12"}])
d(id="rev2.10→john20.27", family="John", title="Be faithful", seed="gnt:Rev 2:10",
  members=[m("be", "be", "γίνου", r"γινου"), m("faithful", "faithful", "πιστός", r"\bπιστοσ"), m("unfaithful", "not unfaithful", "μὴ … ἄπιστος", r"απιστοσ", False)],
  steps=[{"op": "PARTITION", "keep": ["be", "faithful"]}, {"op": "ADD", "new": "unfaithful", "at": 1}], target="gnt:John 20:27", controls=[{"loc": "gnt:Luke 16:10", "label": "Luke 16:10"}, {"loc": "gnt:Matt 25:21", "label": "Matthew 25:21"}])
d(id="rev3.10→john17.15", family="John", title="Keep them out of", seed="gnt:Rev 3:10",
  members=[m("kept", "you kept", "ἐτήρησας", r"ετηρησασ"), m("keep", "I will keep", "τηρήσω", r"\bτηρησ(ω|ησ)\b"), m("outof", "out of", "ἐκ", r"\bεκ τ"), m("hour", "the hour of trial", "τῆς ὥρας τοῦ πειρασμοῦ", r"ωρασ του πειρασμου"), m("evil", "the evil one", "τοῦ πονηροῦ", r"του πονηρου", False)],
  steps=[{"op": "PARTITION", "keep": ["keep", "outof", "hour"]}, {"op": "SUBSTITUTE-OBJECT", "old": "hour", "new": "evil"}], target="gnt:John 17:15", controls=[{"loc": "gnt:Matt 6:13", "label": "Matthew 6:13"}, {"loc": "gnt:John 17:6", "label": "John 17:6, the other half: they have kept your word"}])
d(id="rev9.11→john19.20", family="John", title="In Hebrew, and in Greek", seed="gnt:Rev 9:11",
  members=[m("name", "his name", "ὄνομα αὐτῷ", r"ονομα"), m("hebrew", "in Hebrew", "Ἑβραϊστί", r"εβραιστι"), m("greek", "in Greek", "ἐν τῇ Ἑλληνικῇ", r"ελληνι"), m("written", "written", "γεγραμμένον", r"γεγραμμενον", False), m("roman", "in Latin", "Ῥωμαϊστί", r"ρωμαιστι", False)],
  steps=[{"op": "PARTITION", "keep": ["name", "hebrew", "greek"]}, {"op": "SUBSTITUTE", "old": "name", "new": "written"}, {"op": "ADD", "new": "roman", "at": 2}], target="gnt:John 19:20", controls=[{"loc": "gnt:Luke 23:38", "label": "Luke's title"}, {"loc": "gnt:Acts 21:40", "label": "Acts 21:40"}])

# ── the conceded cases (the author, 2026-11-26 14:03): letters that the received chronology itself sets after the received date of Revelation
LATE = "Letters the received chronology dates after Revelation"
d(id="rev21.1→2pet3.13", family=LATE, title="New heavens and a new earth, as promised", seed="gnt:Rev 21:1",
  members=[m("saw", "I saw", "εἶδον", r"\bειδον"), m("heaven", "a new heaven", "οὐρανὸν καινόν", r"ουραν"), m("earth", "and a new earth", "γῆν καινήν", r"γην καινην")],
  steps=[{"op": "PARTITION", "keep": ["heaven", "earth"]}, {"op": "CITE-AS-PROMISE", "marker": r"επαγγελμα"}], target="gnt:2Pet 3:13",
  controls=[{"loc": "lxx:Ησαιας 65:17", "label": "Septuagint, Isa 65:17"}, {"loc": "lxx:Ησαιας 66:22", "label": "Septuagint, Isa 66:22"}], records=[1418])
d(id="rev3.3→2pet3.10", family=LATE, title="Will come as a thief", seed="gnt:Rev 3:3", members=[m("watch", "watch", "γρηγορήσῃς", r"γρηγορ"), m("come", "I will come", "ἥξω", r"\bηξ(ω|ει)\b"), m("thief", "as a thief", "ὡς κλέπτης", r"ωσ κλεπτησ"), m("hour", "what hour", "ποίαν ὥραν", r"ποια\w? ωρα")],
  steps=[{"op": "PARTITION", "keep": ["come", "thief"]}], target="gnt:2Pet 3:10", controls=[{"loc": "gnt:1Thess 5:2", "label": "1 Thessalonians 5:2 (ἔρχεται)"}, {"loc": "gnt:Matt 24:43", "label": "Matthew's half"}])
d(id="rev5.13→1tim6.16", family=LATE, title="Honour and might", seed="gnt:Rev 5:13",
  members=[m("blessing", "blessing", "ἡ εὐλογία", r"ευλογια"), m("honour", "honour", "ἡ τιμή", r"\bτιμη\b"), m("glory", "glory", "ἡ δόξα", r"\bδοξα\b"), m("might", "might", "τὸ κράτος", r"κρατοσ"), m("ages", "to the ages", "εἰς τοὺς αἰῶνας", r"αιων")],
  steps=[{"op": "PARTITION", "keep": ["honour", "might", "ages"]}], target="gnt:1Tim 6:16", controls=[{"loc": "gnt:Rom 16:27", "label": "Romans 16:27"}, {"loc": "gnt:Gal 1:5", "label": "Galatians 1:5"}])
d(id="rev1.6→jude25", family=LATE, title="Glory and might, to the ages, amen", seed="gnt:Rev 1:6",
  members=[m("glory", "glory", "ἡ δόξα", r"\bδοξα\b"), m("might", "might", "τὸ κράτος", r"κρατοσ"), m("ages", "to the ages", "εἰς τοὺς αἰῶνας", r"αιωνασ"), m("amen", "amen", "ἀμήν", r"αμην"), m("majesty", "majesty", "μεγαλωσύνη", r"μεγαλωσυνη", False)],
  steps=[{"op": "PARTITION", "keep": ["glory", "might", "ages", "amen"]}, {"op": "ADD", "new": "majesty", "at": 1}], target="gnt:Jude 1:25", controls=[{"loc": "gnt:Rom 11:36", "label": "Romans 11:36"}, {"loc": "gnt:Phil 4:20", "label": "Philippians 4:20"}])
d(id="rev12.7→jude9", family=LATE, title="Michael and the adversary", seed="gnt:Rev 12:7",
  members=[m("war", "war", "πόλεμος", r"πολεμ"), m("michael", "Michael", "ὁ Μιχαήλ", r"μιχαηλ"), m("dragon", "the dragon", "τοῦ δράκοντος", r"δρακ"), m("devil", "the devil", "τῷ διαβόλῳ", r"διαβολ", False), m("dispute", "disputing", "διακρινόμενος", r"διακρινομεν", False)],
  steps=[{"op": "PARTITION", "keep": ["war", "michael", "dragon"]}, {"op": "SUBSTITUTE", "old": "dragon", "new": "devil"}, {"op": "SUBSTITUTE", "old": "war", "new": "dispute"}, {"op": "REORDER", "order": ["michael", "devil", "dispute"]}], target="gnt:Jude 1:9",
  controls=[{"loc": "lxx:Ζαχαριας 3:2", "label": "Septuagint, Zech 3:2"}], note="Rev 12:9 names the dragon: 'who is called the devil'. Michael is named in the New Testament here and at Rev 12:7 only.")
d(id="rev2.10→2tim4.8", family=LATE, title="The crown, given", seed="gnt:Rev 2:10",
  members=[m("give", "I will give", "δώσω", r"δωσ"), m("crown", "the crown", "τὸν στέφανον", r"στεφαν"), m("life", "of life", "τῆς ζωῆς", r"τησ ζωησ"), m("right", "of righteousness", "τῆς δικαιοσύνης", r"τησ δικαιοσυνησ", False)],
  steps=[{"op": "PARTITION", "keep": ["give", "crown", "life"]}, {"op": "SUBSTITUTE-OBJECT", "old": "life", "new": "right"}, {"op": "REORDER", "order": ["right", "crown", "give"]}], target="gnt:2Tim 4:8",
  controls=[{"loc": "gnt:Jas 1:12", "label": "James 1:12 (the crown of life, kept)"}, {"loc": "gnt:1Cor 9:25", "label": "1 Corinthians 9:25"}], records=[1414])
d(id="rev19.16→1tim6.15", family=LATE, title="King of kings and Lord of lords", seed="gnt:Rev 19:16",
  members=[m("king", "King of kings", "ΒΑΣΙΛΕΥΣ ΒΑΣΙΛΕΩΝ", r"βασιλευσ (των )?βασιλε"), m("lord", "Lord of lords", "ΚΥΡΙΟΣ ΚΥΡΙΩΝ", r"κυριοσ (των )?κυρι")], steps=[{"op": "EVENT"}], target="gnt:1Tim 6:15",
  controls=[{"loc": "lxx:Δευτερονομιον 10:17", "label": "Septuagint, Deut 10:17"}])

d(id="rev2.10→jas1.12", family="The letters: the run case", title="The crown of life, promised", seed="gnt:Rev 2:10",
  members=[m("give", "I will give", "δώσω", r"\bδωσω\b"), m("crown", "the crown of life", "τὸν στέφανον τῆς ζωῆς", r"στεφανον τησ ζωησ"), m("receive", "will receive", "λήμψεται", r"λημψεται", False)],
  steps=[{"op": "PARTITION", "keep": ["give", "crown"]}, {"op": "SUBSTITUTE", "old": "give", "new": "receive"}, {"op": "CITE-AS-PROMISE", "marker": r"επηγγειλατο"}], target="gnt:Jas 1:12",
  controls=[{"loc": "gnt:2Tim 4:8", "label": "2 Timothy 4:8"}, {"loc": "gnt:1Pet 5:4", "label": "1 Peter 5:4"}], records=[1415, 1735], note="The case run to completion in #1415 and #1735 §VII, entered here in the engine's operators: the giver's 'I will give' becomes the receiver's 'will receive … which he promised'.")

# ── Revelation 11, the two witnesses: one seed region, four targets (v0.10). Unordered: a scene's members are spread over a narrative.
W = [m("city", "the great city … where their Lord was crucified", "τῆς πόλεως … ὅπου … ἐσταυρώθη", r"πολεωσ.{0,90}οπου.{0,40}εσταυρωθη|πολεωσ οπου εσταυρωθη"),
     m("holy", "the holy city", "τὴν πόλιν τὴν ἁγίαν", r"πολιν την αγιαν|αγιαν πολιν"), m("tomb", "a tomb (μνῆμα)", "μνῆμα", r"\bμνημα(τι)?\b"), m("three", "three days", "ἡμέρας τρεῖς", r"ημερασ τρεισ|τρεισ ημερασ|τρισιν ημεραισ"),
     m("watch", "those who watch", "τοὺς θεωροῦντας", r"θεωρ"), m("fear", "great fear", "φόβος μέγας", r"φοβοσ μεγασ|εφοβηθησαν σφοδρα"), m("voice", "a great voice", "φωνῆς μεγάλης", r"φων\w+ μεγαλ"),
     m("quake", "a great earthquake", "σεισμὸς μέγας", r"σεισμοσ (εγενετο )?μεγασ"), m("afraid", "afraid (ἔμφοβοι)", "ἔμφοβοι", r"εμφοβ"), m("glory", "gave glory to God", "ἔδωκαν δόξαν τῷ Θεῷ", r"εδωκαν δοξαν τω θεω|εδοξαζεν τον θεον")]
SEEDW = "gnt:Rev 11:2 + Rev 11:8-13"
TG = {"Matt": "gnt:Matt 27:50-55 + Matt 27:63 + Matt 28:2", "Mark": "gnt:Mark 15:29-47", "Luke": "gnt:Luke 23:35-53 + Luke 24:5", "John": "gnt:John 19:20 + John 20:6"}
KEEP = {"Matt": ["holy", "three", "watch", "fear", "voice", "quake"], "Mark": ["tomb", "three", "watch", "voice"], "Luke": ["tomb", "watch", "voice", "afraid", "glory"], "John": ["city", "watch"]}
for g in TG:
    d(id=f"rev11→{g.lower()}.cross-tomb", family="Revelation 11: the two witnesses, divided", title=f"The witnesses' death and rising, {dict(Matt='Matthew', Mark='Mark', Luke='Luke', John='John')[g]}'s part", seed=SEEDW, members=W, unordered=True,
      steps=[{"op": "PARTITION", "keep": KEEP[g]}], target=TG[g], controls=[{"loc": TG[h], "label": f"{h}'s cross and tomb"} for h in TG if h != g],
      note="Each Gospel's part is what it keeps of Rev 11:2–13 in its cross and tomb; the test is whether another Gospel's telling keeps the same part and lacks the same rest. Bounds chosen by reading (2H.2).")
# ── The guard at the tomb (v0.16). Found by the machine search of 2N.4, then read; entered after.
G20 = [m("angel", "an angel coming down from heaven", "ἄγγελον καταβαίνοντα ἐκ τοῦ οὐρανοῦ", r"αγγελ\w+ (\w+ ){0,2}καταβ\w+ (εκ του|εξ) ουρανου"), m("key", "the key of the abyss", "τὴν κλεῖν τῆς ἀβύσσου", r"κλειν τησ αβυσσου"),
       m("chain", "a great chain", "ἅλυσιν μεγάλην", r"αλυσιν"), m("seized", "he seized", "ἐκράτησεν", r"εκρατησ"), m("bound", "bound him", "ἔδησεν", r"εδησεν"), m("thousand", "a thousand years", "χίλια ἔτη", r"χιλια ετη"),
       m("sealed", "sealed", "ἐσφράγισεν", r"σφραγισ"), m("upon", "over him", "ἐπάνω αὐτοῦ", r"επανω αυτου"), m("deceive", "that he deceive no more", "ἵνα μὴ πλανήσῃ ἔτι", r"\bπλαν"), m("dead", "the dead", "τῶν νεκρῶν", r"νεκρ"), m("first", "the first", "ἡ πρώτη", r"πρωτ")]
DAN6 = "lxx:Δανιηλ_(Theodotionis_versio) 6:17"
d(id="rev20.1-5→matt27.63-28.9", family="Matthew", title="The seal on the deceiver", seed="gnt:Rev 20:1-3 + Rev 20:5", members=G20, unordered=True,
  steps=[{"op": "PARTITION", "keep": ["angel", "seized", "sealed", "upon", "deceive", "dead", "first"]}], target="gnt:Matt 27:63-66 + Matt 28:2 + Matt 28:9",
  controls=[{"loc": DAN6, "label": "Septuagint, Dan 6:17 (Theodotion): the stone and the king's seal"}, {"loc": "lxx:Δανιηλ_(translatio_Graeca) 6:17", "label": "Septuagint, Dan 6:17 (Old Greek)"},
            {"loc": "gnt:Mark 15:46-47 + Mark 16:1-8", "label": "Mark's tomb"}, {"loc": "gnt:Luke 23:53-56 + Luke 24:1-9", "label": "Luke's tomb"}, {"loc": "gnt:John 20:1-17", "label": "John's tomb"}],
  note="Matthew's guard and seal, which no other Gospel has. The engine states the wording kept. Who seals and who is sealed are changed, and the seal is undone: those are differences of relation and are computed in relations/guard.py, not here.")
src = json.dumps(D, ensure_ascii=False, sort_keys=True)
print(json.dumps({"frozen": {"date": "2026-11-26", "sha256_of_derivations": hashlib.sha256(src.encode()).hexdigest(), "rule": "operators and members declared before the run (#1494's rule); a derivation changed after a run is a new derivation"}, "derivations": D}, ensure_ascii=False, indent=1))
