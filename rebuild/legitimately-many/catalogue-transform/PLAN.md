# PLAN: the catalogue transform across the Aristotle–Theophrastus line (Legitimately Many v1.1)

Frozen 2026-11-05 before any count below is computed. Its sha256 is recorded in the runner and in the results.

## Question

The Ghost Catalogues (#1590 §2c, §5) fitted a naming transform from Plato's extant dialogues to the opening of Aristotle's catalogue and measured it against a base rate: 9 of 26 opening entries by the strict first-stem rule (35 per cent) against 6 of 118 in the rest of Aristotle's list (5 per cent) and 9 of 214 in Theophrastus's (4 per cent). This test asks the same question across the second line: do the catalogue entries filed under one of the two names Aristotle and Theophrastus, and lost under it, coincide with the works extant under the other name, and at what rate against the catalogues of the same book and the next?

## Data

Diogenes Laertius as seated (data/corpora/diogenes-laertius/text/tlg001.txt, Perseus perseus-grc2). The catalogues are the runs of title lines (a line closed by a book numeral) at: Speusippus 1374–1391, Xenocrates 1420–1495, Aristotle 1799–1952, Theophrastus 1988–2210, Demetrius of Phalerum 2331–2375, Heraclides 2407–2434, Chrysippus 3489–3680 (the two runs joined). A title is the line with its numerals, editorial brackets and the words ψευδεπίγραφον and ἄλλο removed.

Extant works, as received under each name (titles in Greek, fixed here):

- Aristotle: Κατηγορίαι; Περὶ ἑρμηνείας; Ἀναλυτικὰ πρότερα; Ἀναλυτικὰ ὕστερα; Τοπικά; Περὶ σοφιστικῶν ἐλέγχων; Φυσικὴ ἀκρόασις; Περὶ οὐρανοῦ; Περὶ γενέσεως καὶ φθορᾶς; Μετεωρολογικά; Περὶ ψυχῆς; Περὶ αἰσθήσεως καὶ αἰσθητῶν; Περὶ μνήμης καὶ ἀναμνήσεως; Περὶ ὕπνου καὶ ἐγρηγόρσεως; Περὶ ἐνυπνίων; Περὶ τῆς καθ᾽ ὕπνον μαντικῆς; Περὶ μακροβιότητος καὶ βραχυβιότητος; Περὶ νεότητος καὶ γήρως; Περὶ ζωῆς καὶ θανάτου; Περὶ ἀναπνοῆς; Περὶ τὰ ζῷα ἱστορίαι; Περὶ ζῴων μορίων; Περὶ ζῴων κινήσεως; Περὶ ζῴων πορείας; Περὶ ζῴων γενέσεως; Τὰ μετὰ τὰ φυσικά; Ἠθικὰ Νικομάχεια; Ἠθικὰ Εὐδήμεια; Ἠθικὰ μεγάλα; Πολιτικά; Οἰκονομικά; Τέχνη ῥητορική; Περὶ ποιητικῆς; Ἀθηναίων πολιτεία. The spuria transmitted under the name are a second list, counted apart: Περὶ κόσμου; Περὶ χρωμάτων; Περὶ ἀκουστῶν; Φυσιογνωμονικά; Περὶ φυτῶν; Περὶ θαυμασίων ἀκουσμάτων; Μηχανικά; Προβλήματα; Περὶ ἀτόμων γραμμῶν; Ἀνέμων θέσεις καὶ προσηγορίαι; Περὶ Ξενοφάνους, Ζήνωνος, Γοργίου; Περὶ ἀρετῶν καὶ κακιῶν; Ῥητορικὴ πρὸς Ἀλέξανδρον; Περὶ πνεύματος.
- Theophrastus: Περὶ φυτῶν ἱστορίας; Περὶ φυτῶν αἰτιῶν; Χαρακτῆρες; Τὰ μετὰ τὰ φυσικά; Περὶ αἰσθήσεων; Περὶ λίθων; Περὶ πυρός; Περὶ ὀσμῶν; Περὶ ἀνέμων; Περὶ σημείων; Περὶ κόπων; Περὶ ἰλίγγων; Περὶ ἱδρώτων; Περὶ λιποψυχίας; Περὶ παραλύσεως; Περὶ τῶν ἐν ξηρῷ διαιτωμένων ἰχθύων.

## Rule (the strict rule of #1590 §5, unchanged)

Normalize: lower case, diacritics and breathings removed, final sigma as sigma, the function words removed (περι, των, του, της, τα, το, τον, την, τους, τοις, ταις, τας, της, και, η, προς, εκ, εν, υπερ, κατα, απο, επι, καθ, μετα, αλλο, ψευδεπιγραφον). A content word has four or more letters; its stem is its first five letters. A catalogue title matches a list of extant works if the stem of its first content word equals the stem of any content word of any title in the list. For each catalogue and each list: matched / total, and the matched titles printed.

Primary comparisons:

- A. Theophrastus's catalogue against Aristotle's extant works, beside the five control catalogues (Speusippus, Xenocrates, Demetrius, Heraclides, Chrysippus) against the same list, and beside Aristotle's own catalogue against his own extant works.
- B. Aristotle's catalogue against Theophrastus's extant works, beside the five controls against the same list, and beside Theophrastus's own catalogue against his own extant works.

The spuria list is run as a secondary under A. Reported as measured; the rates are descriptive, no test statistic is attached, and a hand reading of every matched title follows the counts as a separate, labelled step.

## Deviations

Recorded in RESULTS.md with their reasons.
