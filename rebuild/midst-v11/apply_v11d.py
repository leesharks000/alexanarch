"""EA-MIDST-01 v1.1 draft, fourth pass: ChatGPT's substantive review of the v1.1 draft, supplied by the author 2026-11-11 04:09
("strong substantive from chatgpt"), each point checked before anything was changed: Barker 1991, 86-87 read in the PDF the review cites;
Wis 18:15-16, Isa 49:2, Judg 5:31 read in the seated Swete; Philo's introductions of non-Pentateuchal speakers inventoried from the
editors' references in the seated text layer; Rev 3:21 reread.   python3 apply_v11d.py   (after a, b, c)"""
import pathlib, re
H = pathlib.Path(__file__).parent
P = H / "EA-MIDST-01-v1.1-draft.md"; T = P.read_text(encoding="utf-8")
def sub(old, new):
    global T; assert T.count(old) == 1, (old[:70], T.count(old)); T = T.replace(old, new)
def after_para(prefix, new):
    global T
    m = [x for x in re.finditer(r"(?m)^" + re.escape(prefix) + r".*$", T)]; assert len(m) == 1, prefix
    T = T[:m[0].end()] + "\n\n" + new + T[m[0].end():]

# consolidation foregrounded, Hebrews in the argument
sub("and gives the one who conquers a name \"ὃ οὐδεὶς οἶδεν εἰ μὴ ὁ λαμβάνων\" (2:17; 7b.10).",
    "and gives the one who conquers a name \"ὃ οὐδεὶς οἶδεν εἰ μὴ ὁ λαμβάνων\" (2:17; 7b.10). What the sources distribute, the Apocalypse concentrates: names, offices, a garment, a judgment and a voice, spread across Zechariah, Philo's treatises and the Septuagint, are gathered on one named figure. Hebrews makes the same gathering in seven verses, the son of Nun, the dividing Logos and the great high priest named Ἰησοῦς (Heb 4:8–14; 7a.8).")

# the socket: Philo's other introductions, inventoried
after_para("4.4a. ", "4.4b. How Philo introduces the speakers he does not name, counted from the editors' references in the seated text layer to books outside the Pentateuch. Anonymity of the speaker is his habit. The Psalms come from \"ὁ ὑμνῳδὸς\", from \"τῶν Μωυσέως γνωρίμων τις\" (Conf. 39), from \"ὁ τοῦ Μωυσέως δὴ θιασώτης\" (Plant. 39), from \"τις τῶν ἑταίρων Μωυσέως\" (Somn. 2.245), from \"τις προφητικὸς ἀνὴρ\" (Her. 290); Jeremiah, named at Cher. 49 (\"Ἱερεμίαν τὸν προφήτην\"), is \"τοῦ προφητικοῦ θιασώτης χοροῦ\" at Conf. 44, eighteen sections before the oracle; Proverbs comes \"παρά τινι τῶν ἐκ τοῦ θείου χοροῦ\" (Ebr. 31). So the unnamed Zechariah, \"one of the companions of Moses\", is Philo's ordinary practice, and the companion formula is shared with a psalmist (Somn. 2.245). Two things set Conf. 62 apart. Where Philo gives a name, he often gives its meaning with it (Jeremiah, Samuel and Job he names without one): Solomon, \"ὄνομα εἰρηνικός, ὃς πατρίῳ γλώττῃ Σαλομὼν καλεῖται\" (Congr. 177); Hannah, whose name is \"χάρις\" (Somn. 1.254); Gideon, \"ὃς ἑρμηνεύεται πειρατήριον\" (Conf. 130). He has the meaning of Ἰησοῦς ready, \"σωτηρία κυρίου\" (Mut. 121). And among all these loci, Conf. 62 is the one oracle whose content is a name, \"ᾧ ὄνομα ἀνατολή\", and whose addressee has a name in the verse above. The prophet's anonymity is the habit; the addressee's is the cut. The receiver who restores the verse restores both, and the second changes the reading of the first: the name Rising, given to the Logos, was spoken to a Ἰησοῦς.")
sub("4.5. The companions of Moses. The commentary of 9 November 2025 turned on this phrase (\"He did not leave us names. He left only the gesture.\"). At Conf. 62 the companion is Zechariah. The phrase that stands in the place of the two withheld names names a class,",
    "4.5. The companions of Moses. The commentary of 9 November 2025 turned on this phrase (\"He did not leave us names. He left only the gesture.\"). At Conf. 62 the companion is Zechariah, and the same formula introduces a psalmist at Somn. 2.245 (4.4b). The phrase that stands in the place of the two withheld names names a class,")

# psephos count, right hand
sub("In the New Testament the word occurs twice: the persecutor's condemning vote,", "In the New Testament the word occurs in two passages, three times: the persecutor's condemning vote,")
sub("the white stone given to the conqueror (Rev 2:17). Philo has", "the white stone given to the conqueror, named twice in the verse (Rev 2:17). Philo has")
sub("At the Sun station, the last of the circuit (11.5b), both texts give the seat at the right hand.",
    "At the Sun station, the last of the circuit (11.5b), both texts close on enthronement, with a difference kept: the Gawaita's deliverer sets the saved at his right hand; Laodicea's speaker gives a seat on his own throne, as he sat with the Father on his.")

# the Gawaita's place relative to the mapping
sub("The Gawaita is the outside source the constraint test asks for (11.5a): profiles of the powers given by a text the archive did not write, a text that offers them as the key.",
    "The Gawaita is a source outside the archive, and it is not independent of the mapping: #1101 already drew on it (\"Mercury founded a community in Qom\", 13.1). Its further correspondences develop the source-based reading; they are not an untouched confirmation of an assignment derived without it. What it adds to the constraint test (11.5a) is profiles given by a text that offers them as the key, and the measure of 13.6: where applying its explanation to the letters yields a constrained correspondence (Ephesus, Pergamum, Thyatira, Laodicea), and where it yields none (Smyrna, Philadelphia).")
sub("the Haran Gawaita's planetary communities, 13.6)", "the Haran Gawaita's planetary communities, 13.6, which already informed the mapping)")

# 16.6: the precise claim
sub("The warrant he used is inspectable, and the letters meet it in the form he required. The governing mapping, read against the Chaldean order, runs in three downward pairs climbing from the lowest spheres to the highest and closes on the middle (11.5b): a sequence with a direction.",
    "The warrant he used is inspectable. The governing mapping now produces a directional sequence of the kind he treated as evidence: read against the Chaldean order, it runs in three downward pairs climbing from the lowest spheres to the highest and closes on the middle (11.5b). How much weight the sequence carries depends on whether profiles fixed independently recover the assignments and the sequence with them (11.5a).")

# 16.5b: Barker answered Wolfson first; publication details
sub("(Jewish Quarterly Review, pp. 89–106 as printed in the author's copy; volume and year, n.s. 51, 1960, from the standard citation, to be checked; OCR spacing normalized)",
    "(Jewish Quarterly Review n.s. 51.2, October 1960, 89–106, JSTOR 1453680, as the second ChatGPT review of v1.1 reports it; the pages are those of the author's copy; OCR spacing normalized)")
sub("The join was made at the first asking and filed by a statement the seated text does not bear out.",
    "The join was made at the first asking and filed by a statement the seated text does not bear out. The statement was answered in print. Barker (1991, 86–87) quotes Wolfson's denial, replies \"Such a statement seems incredible!\", and adduces Conf. 146; on the same page she sets Wis 18:15 beside the sword in the mouth of the Son of Man (Rev 1:16), and later reads the seven lamps with the seven spirits of Rev 1:4 (93–94). What this paper adds to Barker's correction is Her. 205 and Leg. 3.177 beside Conf. 146, and the consequence for the Apocalypse's messengers; what later work did with her answer is not traced here.")

# 16.7: the alternatives inside the test
sub("Against it, on the criteria under which the dependence of Hebrews is heard (16.4a): (a) Specificity.",
    "The richest alternatives belong inside the test. Wisdom already has the Logos as a warrior descending from royal thrones with a sharp sword, \"ὁ παντοδύναμός σου λόγος ἀπʼ οὐρανῶν ἐκ θρόνων βασιλείων ἀπότομος πολεμιστὴς\", \"ξίφος ὀξὺ τὴν ἀνυπόκριτον ἐπιταγὴν σου φέρων\" (Wis 18:15–16; Swete's seat numbers them 19:15–16), and the cosmos on the high priest's robe (18:24; 7a.8); Isaiah has the mouth made a sharp sword, \"ἔθηκεν τὸ στόμα μου ὡς μάχαιραν ὀξεῖαν\" (Isa 49:2); the Song of Deborah has the sun going forth in its strength, \"ὡς ἔξοδος ἡλίου ἐν δυνάμει αὐτοῦ\" (Judg 5:31, Alexandrinus), close to \"ὡς ὁ ἥλιος φαίνει ἐν τῇ δυνάμει αὐτοῦ\" (Rev 1:16). The sword of the mouth, the solar face and the cosmic robe are therefore explained without Philo. Against the conventional judgment, on the criteria under which the dependence of Hebrews is heard (16.4a), what remains: (a) Specificity.")
sub("Each transformation operates on the Philonic reading, and presupposes it in hand.",
    "Each transformation operates on the Philonic reading, and presupposes it in hand. What survives the alternatives is the organization: no alternative reads the seven lamps as the seven planets with the sun in the middle and the dividing Logos as that middle, names the Logos ἀρχή and Ἀνατολή, or takes the Logos-name from an oracle spoken to Ἰησοῦς the high priest; Philo does all of these, most of them in one treatise, and the Apocalypse's opening scene and its circuit of letters are built on that organization. Wisdom is Alexandrian, and close to Philo in its Logos and its robe; it is one shape the route of a carried reading could take.")

# packet: pillar status
sub('"spxi:pillarStatus": "v1.0, deposited on six outside reviews (Gemini, DeepSeek, ChatGPT four times), each point checked against the seats;',
    '"spxi:pillarStatus": "v1.1 draft (v1.0 deposited 2026-11-10 on six outside reviews, Gemini, DeepSeek, ChatGPT four times; v1.1 on the author\'s points and two further reviews, 19.9–19.11), each point checked against the seats;')

# apparatus
m = re.search(r"(?m)^19\.10\. .*$", T); assert m
T = T[:m.end()] + "\n\n19.11. ChatGPT, on the v1.1 draft (supplied by the author, 2026-11-11: \"strong substantive from chatgpt\"). Each point checked: Barker's pages read in the PDF the review cites; the Septuagint loci read in the seats; the count of 11.5b rerun. Adopted: Barker's answer to Wolfson credited, and this paper's addition distinguished (16.5b); Wolfson's publication details (16.5b); Wisdom 18:15–16, Isaiah 49:2 and Judges 5:31 set inside the dependence test, with what they explain and what survives them (16.7); 16.6 stated as a sequence of the kind Charles treated as evidence, with its weight left to the test; the Gawaita's place relative to the mapping it already informed (11.5a, 13.6); the enthronement difference at Laodicea (13.6); Philo's introductions of unnamed speakers inventoried, so that the socket is shown against his practice (4.4b); ψῆφος in two passages, three times (7b.9); the packet's pillar status; the consolidation foregrounded in the argument. The review's arithmetic for 11.5b agrees with the paper's." + T[m.end():]
sub("the socket in the argument, the sequence table and Part III's anchor, on an outside review (19.10);",
    "the socket in the argument, the sequence table and Part III's anchor, on an outside review (19.10); the alternatives inside the dependence test, Barker's answer to Wolfson, Philo's introductions inventoried, on ChatGPT's review (19.11);")
P.write_text(T, encoding="utf-8"); print("pass d written", len(T.split()), "words")
