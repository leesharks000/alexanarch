#!/usr/bin/env python3
"""Legitimately Many — the locus table (design v0.5 §4.1). One row per locus: the stratum of §3, the seat and the exact Greek
(or Latin, or Arabic) as seated, the slot and its filler, and two codes, one for the attribution of the work(s) to a name and
one for the number of makers. The codes are those of §4.1 (does not address; presupposes; argues for; considers and excludes
an alternative; revises), with a sixth, holds open, for the catalogue's ἤ and for a rival text reported and left standing,
which none of the five fits. The coding is the session's provisional reading, marked as such; the operator rules on it.
The builder (build_table.py) locates every phrase in its seat and refuses a row whose phrase is not found.
"""
C = "../../data/corpora/"
DL = C + "diogenes-laertius/original/tlg0004.tlg001.perseus-grc2.xml"
STR = C + "strabo/original/tlg0099.tlg001.perseus-grc2.xml"
SIMP = C + "aristotle-commentators/original/first1k/tlg4013.tlg003.1st1K-grc1.xml"
OLY = C + "aristotle-commentators/original/first1k/tlg4019.tlg001.1st1K-grc1.xml"
ELI = C + "aristotle-commentators/original/first1k/tlg4020.tlg002.1st1K-grc1.xml"
AMM = C + "aristotle-commentators/original/first1k/tlg4016.tlg002.1st1K-grc1.xml"
PHI = C + "aristotle-commentators/original/first1k/tlg4015.tlg001.1st1K-grc1.xml"
GAL = C + "galen/original/first1k/tlg0057.tlg085.1st1K-grc1.xml"
ATH = C + "athenaeus/original/perseus/tlg0008.tlg001.perseus-grc3.xml"

L = [
 # 3.1 the corpus's self-disclosure
 dict(id="L01", stratum="3.1", work="Plato, Ep. II 314c", tei=C + "plato/original/tlg0059.tlg036.xml", text=C + "plato/text/tlg036-Ἐπιστολαί.txt",
      find="οὐδʼ ἔστιν σύγγραμμα Πλάτωνος οὐδὲν οὐδʼ ἔσται, τὰ δὲ νῦν λεγόμενα Σωκράτους ἐστὶν καλοῦ καὶ νέου γεγονότος",
      slot="author of the writings", filler="no writing of Plato; the things said are a Socrates become beautiful and new",
      code_attr="revises", code_count="revises",
      note="The letter withdraws the name from the writings and gives them to a Socrates made new (#1579). Whatever its authenticity, it is a text of the corpus disclosing the operation."),
 # 3.2 the stone
 dict(id="L02", stratum="3.2", work="Delphic decree for Aristotle and Callisthenes (as seated in #1582)", text="../../data/deposits/AXN-0671.md",
      find="ἐπαινέσαι Ἀριστοτέλη καὶ Καλλισθένη", slot="makers of the list of Pythian victors", filler="two persons, in the accusative of honour, joined by καί",
      code_attr="presupposes", code_count="presupposes", note="The civic record fills the maker-slot with two persons; it does not argue the attribution."),
 # 3.3 the wills
 dict(id="L03", stratum="3.3", work="Aristotle's will (Diogenes Laertius V)", tei=DL, find="τάδε διέθετο Ἀριστοτέλης",
      slot="testator", filler="Aristotle", code_attr="does_not_address", code_count="does_not_address",
      note="The will names no book, library, school or successor (#1581). It is part of the corpus and its investigation (operator, 2026-11-02); read in reception as the legal record of a person."),
 dict(id="L04", stratum="3.3", work="Theophrastus's will (Diogenes Laertius V)", tei=DL, find="τὰ δὲ βιβλία πάντα Νηλεῖ",
      slot="owner of the books", filler="Neleus, one person", code_attr="does_not_address", code_count="does_not_address",
      note="The books enter as property passing to one heir, beside the premises given to a commons (#1581)."),
 # 3.4 custody
 dict(id="L05", stratum="3.4", work="Strabo XIII.1.54", tei=STR, find="οἵ τε Σωκρατικοὶ γεγόνασιν Ἔραστος καὶ Κορίσκος",
      slot="the custodians' line", filler="Erastus and Coriscus, 'Socratics', and Neleus son of Coriscus", code_attr="does_not_address", code_count="does_not_address",
      note="Strabo calls the Scepsis custodians Socratics: the custody line runs through a Socratic family before it reaches the Peripatetic books."),
 dict(id="L06", stratum="3.4", work="Strabo XIII.1.54", tei=STR, find="ὁ γοῦν Ἀριστοτέλης τὴν ἑαυτοῦ Θεοφράστῳ παρέδωκεν",
      slot="custody of the library", filler="Aristotle to Theophrastus", code_attr="presupposes", code_count="presupposes",
      note="The first link of the custody, which the will does not contain (#1581); the warrant for the addition is the question (§4.3, #1602)."),
 dict(id="L07", stratum="3.4", work="Strabo XIII.1.54", tei=STR, find="τά τε Ἀριστοτέλους καὶ τὰ τοῦ Θεοφράστου βιβλία",
      slot="the books sold to Apellicon", filler="two collections under two names", code_attr="presupposes", code_count="presupposes", note=""),
 dict(id="L08", stratum="3.4", work="Athenaeus I.3a–b", tei=ATH, find="καὶ τὸν τὰ τούτων διατηρήσαντα βιβλία Νηλέα",
      slot="custody and sale", filler="Neleus, who kept the books of Aristotle and Theophrastus, selling all to Ptolemy", code_attr="presupposes", code_count="presupposes",
      note="The rival custody: Alexandria, against Strabo's Scepsis."),
 # 3.5 catalogues
 dict(id="L09", stratum="3.5", work="Diogenes Laertius V, the Theophrastan catalogue", tei=DL, find="Ὑπομνημάτων Ἀριστοτελικῶν ἢ Θεοφραστείων",
      slot="the name a title is filed under", filler="Aristotle or Theophrastus", code_attr="holds_open", code_count="does_not_address",
      note="The catalogue's one disjunction keeps the assignment open; it does not bear on the number of makers (review of 2026-11-02, point 4)."),
 dict(id="L10", stratum="3.5", work="the Hesychian catalogue (Rose 1886, p. 18)", text=C + "hesychian-catalogue/text/rose-1886-pp9-22.ocr.txt", find="ψευδεπίγραφα δὲ",
      slot="the name's list", filler="genuine titles, then pseudepigrapha, under one name", code_attr="considers_excludes", code_count="presupposes",
      note="The spurious are filed inside the one name's list as spurious."),
 dict(id="L11", stratum="3.5", work="Ibn al-Nadīm, Fihrist, on Ptolemy al-Gharīb", text=C + "arabic-biobibliography/text/ibn-al-nadim-fihrist.txt",
      find="بطليميوس الغريب وكان يتوالى ارسطاليس وينشر محاسنه", slot="the author of the catalogue and the life", filler="Ptolemy, a partisan of Aristotle", code_attr="presupposes", code_count="presupposes",
      note="The fourth catalogue travels with the life and the will as one dossier of the person."),
 dict(id="L12", stratum="3.5", work="Ibn Abī Uṣaybiʿa, ʿUyūn al-anbāʾ", text=C + "arabic-biobibliography/text/ibn-abi-usaybia-uyun.txt",
      find="وقال بطليموس في كتابه إلى غلس في سيرة أرسطوطاليس وخبره ووصيته وفهرست", slot="the dossier", filler="life, will and list of books in one book to Gallus",
      code_attr="presupposes", code_count="presupposes", note=""),
 # 3.6 the edition
 dict(id="L13", stratum="3.6", work="Plutarch, Sulla 26", tei=C + "plutarch/original/pl_tlg033.xml", text=C + "plutarch/text/tlg033.txt", find="ἀναγράψαι τοὺς νῦν φερομένους πίνακας",
      slot="the edition's tables", filler="Andronicus", code_attr="presupposes", code_count="presupposes", note=""),
 dict(id="L14", stratum="3.6", work="Plutarch, Sulla 26", tei=C + "plutarch/original/pl_tlg033.xml", text=C + "plutarch/text/tlg033.txt", find="τῶν δὲ Ἀριστοτέλους καὶ Θεοφράστου γραμμάτων",
      slot="the corpus the edition tabled", filler="two names joined by καί", code_attr="presupposes", code_count="presupposes", note=""),
 dict(id="L15", stratum="3.6", work="Porphyry, Life of Plotinus 24 (Volkmann 1883, the Archive's OCR)", text=C + "porphyry/text/volkmann-1883-vol1.ocr.txt",
      find="ναῖον καὶ ᾿Ανδρόνικαν τὸν Περιπατητικόν, ὧν ὁ", slot="the editor's model", filler="Andronicus, who divided the works of Aristotle and Theophrastus by subject",
      code_attr="presupposes", code_count="presupposes", note="The OCR reads Ἀνδρόνικον as ᾿Ανδρόνικαν."),
 dict(id="L16", stratum="3.6", work="Plutarch, Alexander 7", tei=C + "plutarch/original/pl_alex.xml", text=C + "plutarch/text/tlg047.txt", find="καὶ ἐκδεδομένων καὶ μὴ ἐκδεδομένων",
      slot="publication", filler="the doctrines both published and not published", code_attr="does_not_address", code_count="does_not_address", note=""),
 # 3.7a speakers
 dict(id="L17", stratum="3.7a", work="Diogenes Laertius III.52", tei=DL, find="διὰ τεττάρων προσώπων",
      slot="the bearer of doctrine", filler="Plato, through four persons", code_attr="argues_for", code_count="considers_excludes",
      note="Readers who took the Strangers for Plato and Parmenides are named and answered: the Strangers are 'nameless fictions'. A maker heard inside a speaker, and refused."),
 dict(id="L18", stratum="3.7a", work="Diogenes Laertius III.52", tei=DL, find="πλάσματά ἐστιν ἀνώνυμα",
      slot="the Strangers", filler="nameless fictions", code_attr="argues_for", code_count="considers_excludes", note=""),
 dict(id="L19", stratum="3.7a", work="Diogenes Laertius III.65", tei=DL, find="διπλῆ πρὸς τὰ δόγματα καὶ τὰ ἀρέσκοντα Πλάτωνι",
      slot="the sign for doctrine", filler="Plato's", code_attr="presupposes", code_count="does_not_address", note=""),
 # 3.8 market
 dict(id="L20", stratum="3.8", work="Diogenes Laertius III.66", tei=DL, find="μισθὸν ἐτέλει τοῖς κεκτημένοις",
      slot="access", filler="a fee paid to the owners", code_attr="does_not_address", code_count="does_not_address", note="Antigonus of Carystus."),
 dict(id="L21", stratum="3.8", work="Galen, In Hipp. de nat. hom.", tei=GAL, find="ῥᾳδιουργία τοῖς ἕνεκα τοῦ λαβεῖν ἀργύριον ἀναφέρουσιν ὡς τοὺς βασιλεῖς ἀνδρῶν ἐνδόξων συγγράμματα",
      slot="the title", filler="the famous name that sells", code_attr="considers_excludes", code_count="does_not_address", note=""),
 dict(id="L22", stratum="3.8", work="Simplicius, In Cat., preface", tei=SIMP, find="πολλοῦ χρυσίου τὰ ἀπεξενωμένα τῶν βιβλίων ὠνοῦντο",
      slot="acquisition", filler="kings buying for gold", code_attr="considers_excludes", code_count="does_not_address", note=""),
 # 3.9 prolegomena
 dict(id="L23", stratum="3.9", work="Olympiodorus, Prolegomena", tei=OLY, find="ἢ διὰ φιλοτιμίαν τῶν βασιλέων ἢ δι’ εὔνοιαν τῶν μαθητῶν ἢ διὰ ὁμωνυμίαν",
      slot="the causes of spuriousness", filler="kings, pupils, homonymy", code_attr="argues_for", code_count="considers_excludes",
      note="The pupils' goodwill, the many writing under the one, is named as a mechanism and filed as spuriousness."),
 dict(id="L24", stratum="3.9", work="Elias, In Cat.", tei=ELI, find="ὡς τὰ Πυθαγόρου καὶ Σωκράτους ἐπιγραφόμενα βιβλία μὴ ὄντα Σωκράτους ἢ Πυθαγόρου ἀλλὰ Σωκρατικῶν καὶ Πυθαγορικῶν",
      slot="the name on Socratic books", filler="Socrates; the makers, Socratics", code_attr="considers_excludes", code_count="considers_excludes", note=""),
 dict(id="L25", stratum="3.9", work="Elias, In Cat.", tei=ELI, find="χιλίων τὸν ἀριθμόν, ὥς φησι Πτολεμαῖος ὁ Φιλάδελφος ἀναγραφὴν αὐτῶν ποιησάμενος καὶ τὸν βίον αὐτοῦ καὶ τὴν διάθεσιν",
      slot="the catalogue", filler="Ptolemy's, with the life and the will", code_attr="presupposes", code_count="presupposes", note=""),
 dict(id="L26", stratum="3.9", work="Ammonius, In Cat.", tei=AMM, find="πολλοὶ γὰρ αὑτῶν συντιθέντες ἐπέγραφον τῷ Ἀριστοτέλους ὀνόματι",
      slot="the name on composed works", filler="Aristotle's, written by many", code_attr="considers_excludes", code_count="considers_excludes", note=""),
 dict(id="L27", stratum="3.9", work="Philoponus, In Cat.", tei=PHI, find="τρεῖς γὰρ αφορμαὶ γεγόνασι τοὐ νοθεύεσθαι τὰ συγγράμματά του Ἀριστοτέλους",
      slot="the causes of spuriousness", filler="homonymy of authors first", code_attr="argues_for", code_count="considers_excludes", note=""),
 # 3.9a Simplicius
 dict(id="L28", stratum="3.9a", work="Simplicius, In Cat., preface", tei=SIMP, find="καὶ τὸ γνήσιον δὲ, ὅπερ, ἐμοὶ δοκεῖ, πρὸ πάντων ἔδει τῶν ἄλλων βασανίζεσθαι, ἀναγκαίως προλαμβάνεται",
      slot="the order of examination", filler="the genuine first", code_attr="does_not_address", code_count="does_not_address", note="Procedural: the sentence orders the examination (v0.5 §3.9a)."),
 dict(id="L29", stratum="3.9a", work="Simplicius, In Cat., preface", tei=SIMP, find="πάσχομεν γάρ τι καὶ ὑπὸ τῆς τῶν προσώπων δόξης",
      slot="the reader", filler="affected by the reputation of persons", code_attr="does_not_address", code_count="does_not_address", note="The reason for testing first."),
 dict(id="L30", stratum="3.9a", work="Simplicius, In Cat., preface", tei=SIMP, find="καὶ τὸ γνήσιον οὐκ ἐπὶ πάντων δεῖται κατασκευῆς",
      slot="the default", filler="proof only where there is occasion for dispute", code_attr="presupposes", code_count="does_not_address", note="The default is in this rule."),
 dict(id="L31", stratum="3.9a", work="Simplicius, In Cat., on the genuineness of the Categories", tei=SIMP, find="ἢ οὖν καὶ ἐκεῖνα νοθεύειν χρὴ τὰ συγγράμματα, ἐν οἷς μέμνηται τούτου, ἢ μηδὲ τοῦτο ἀθετεῖν",
      slot="the attribution of the Categories", filler="Aristotle, by the corpus's cross-references", code_attr="considers_excludes", code_count="does_not_address", note=""),
 dict(id="L32", stratum="3.9a", work="Simplicius, In Cat., on the genuineness of the Categories", tei=SIMP, find="ἄναρχος ἂν ἦν καὶ ἀκέφαλος",
      slot="the attribution of the Categories", filler="Aristotle, by the system's need for a beginning", code_attr="argues_for", code_count="does_not_address",
      note="Architecture used as evidence; embrittlement where it stops reconsideration, to be shown (§3.9a)."),
 dict(id="L33", stratum="3.9a", work="Simplicius, In Cat., on the genuineness of the Categories", tei=SIMP, find="ὅτι φέρεται καὶ ἄλλο τῶν κατηγοριῶν βιβλίον ὡς Ἀριστοτέλους",
      slot="the name over a second Categories", filler="Aristotle's, a second text with the same line count and another opening", code_attr="holds_open", code_count="does_not_address",
      note="Adrastus reports it; Simplicius records the opening ('Τῶν ὄντων τὸ μέν ἐστιν') and the equal stichometry, and moves on without adjudicating. Two texts under one name, left standing."),
 dict(id="L34", stratum="3.9a", work="Simplicius, In Cat., preface", tei=SIMP, find="φαίνεται πανταχοῦ τῷ Ἀρχύτᾳ κατακολουθεῖν ὁ Ἀριστοτέλης βουλόμενος",
      slot="the prior maker of the ten categories", filler="Archytas the Pythagorean", code_attr="presupposes", code_count="presupposes",
      note="The pseudo-Archytas text is a debt to seat (Mullach)."),
 # 3.10 the modern edition
 dict(id="L35", stratum="3.10", work="Bekker 1831, Praefatio (OCR in session)", text=C + "bekker-aristotle-1831/text/bekker-1831-praefatio.ocr.txt",
      find="consilium ce- pisset Aristotelis ex diutino situ excitandi", slot="the edition", filler="Aristotle, raised from long neglect", code_attr="presupposes", code_count="does_not_address",
      note="The preface says nothing of genuineness, order or authorship."),
 # 3.9a Simplicius, the Archytas doublet (added 2026-11-02 with draft §2)
 dict(id="L36", stratum="3.9a", work="Simplicius, In Cat., preface", tei=SIMP, find="Ἀρχύτου γὰρ τοῦ Πυθαγορικοῦ καὶ πρὸ Ἀριστοτέλους τὴν εἰς δέκα τῶν πρώτων γενῶν ποιησαμένου διαίρεσιν",
      slot="the first maker of the ten categories", filler="Archytas, before Aristotle", code_attr="presupposes", code_count="presupposes",
      note="Iamblichus's assignment of priority, as Simplicius reports it."),
 dict(id="L37", stratum="3.9a", work="Simplicius, In Cat., preface", tei=SIMP, find="τὴν συμφωνίαν τὴν πρὸς αὐτὰ τοῦ Ἀριστοτέλους ἐπέδειξε",
      slot="the relation of the two texts", filler="Aristotle's agreement with Archytas", code_attr="presupposes", code_count="presupposes",
      note="The priority made a condition of exposition: agreement shown, the few disagreements explained."),
 dict(id="L38", stratum="3.9a", work="Simplicius, In Cat. 10 (on opposites)", tei=SIMP, find="φαίνεται δὲ καὶ περὶ ἀντικειμέων Ἀριστοτέλης ἐκ τοῦ Ἀρχυτείου βιβλίου μεταλβὼν",
      slot="the source of the chapter on opposites", filler="the Archytan book On Opposites", code_attr="argues_for", code_count="presupposes", note="The TEI's readings (ἀντικειμέων, μεταλβὼν) are kept as seated."),
 dict(id="L39", stratum="3.9a", work="Simplicius, In Cat. 10 (on opposites)", tei=SIMP, find="ἀρχέτοπα τῶν εἰρημένων ὄντα",
      slot="the status of the Archytan text", filler="archetypes of what Aristotle said", code_attr="argues_for", code_count="presupposes", note=""),
 dict(id="L40", stratum="3.9a", work="Simplicius, In Cat. 10 (on opposites)", tei=SIMP, find="καὶ ἴσως οὐκ ἦλθεν εἰς αὐτόν",
      slot="the transmission of the Archytan book", filler="a book that perhaps did not reach Iamblichus", code_attr="does_not_address", code_count="does_not_address",
      note="Simplicius has an Archytan book his authority did not use; its arrival is the occasion of the reading."),
 dict(id="L41", stratum="3.9a", work="Simplicius, In Cat., on the genuineness of the Categories", tei=SIMP,
      find="ἵνα μηδὲ ὑπονοήσωμεν τοῦ Ἀρχυτείου μνημονεύειν αὐτὸν ἄλλην ἐπιγραφὴν ἔχοντος",
      slot="the referent of Aristotle's cross-references", filler="the Categories, the Archytan book excluded by its title", code_attr="considers_excludes", code_count="presupposes",
      note="The doublet across names inside the proof: an alternative referent named and excluded."),
]

