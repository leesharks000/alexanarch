# Plan, frozen before any count: Mark 13 against its extant candidates

Question. The apocalyptic discourse of Mark 13 is given, in the seated critics, a reconstructed source: a Jewish apocalypse inserted into the chapter (Wellhausen 1905; Wernle 1899, "die Mr 13 zu Grunde liegende Apokalypse"), and its sayings parallel in Luke 17:22-37 is called "the Apocalypse of Q" (Streeter 1924). The census asks what the extant candidates share with the chapter at the level of the word sequence.

Texts. Mark 13:1-37, Luke 17:22-37 and Matt 24:1-51 (gnt-nestle1904); Revelation (gnt-nestle1904, Rev.txt); Daniel in the Old Greek and in Theodotion (lxx-swete, tlg056, tlg057); the whole LXX of the seat (lxx-swete/text, every file) as the scriptural matrix; the other 23 NT books as background.

Normalization. Lowercase; NFD with combining marks removed; final sigma folded; every non-letter removed; tokens split on whitespace. No lemmatization: a match is a match of surface forms after accent stripping.

Unit. Contiguous word trigrams within a verse (no trigram crosses a verse boundary).

Counts. For each of the three discourses D (Mark 13, Luke 17:22-37, Matt 24): the trigrams of D found in Revelation (set R); those found in Daniel OG or Theodotion (set A); those found anywhere in the LXX (set L). A trigram of D in R is *marked against the matrix* if it is absent from L. A trigram in R is *background-common* if it occurs in more than 4 of the 23 background NT books; those are reported but not counted as contacts.

Reported. |R|, |R − L|, |A|, |L| per discourse, the R and R − L lists with verse references in both books, and the background-common list. No significance test is run and none is claimed: the count is descriptive, and its use is to show that the extant candidate can be read at the word, in seat, against the matrix both books draw on.

Defeat. The census is not evidence for any direction. A contact of R − L would be explained more economically by a shared lost source only if that source is attested; an unattested source is recorded as reconstructed (#1735 §I).
