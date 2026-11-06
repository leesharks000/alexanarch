# EA-CORPORA-35 — The making of Q: the hypothetical source from Weisse to Streeter, 1838–1925

At the operator's word of 2026-11-06 11:07 EST ("so we need factual repairs versioned in place and the ea-corpora for q - lets do those as one bundle. we need ea-corpora before the q paper. and byline... lets say sigil and cranes. provenance"), with Rebekah Cranes as the standing authority on the EA-CORPORA deposits. The research occasion is the study of Q (working title "I Know You Are, But What Am I?: Or, How a Completely Hypothetical, Uninspectable Text Is Granted Evidentiary Status Symmetrical to One That Is Inspectable Because It Exists — Revelation First"; Johannes Sigil and Rebekah Cranes, Provenance: Journal of Forensic Semiotics), the companion of Secondary Source (#1741 §6.5). Its captures are AXN:0C22–0C26 (five Google AI Overviews on Q, 2026-11-06).

- **35/01 weisse-evangelische-geschichte-1838**: dieevangelischeg0000weis (I) and dieevangelischeg0002weis (II).
- **35/02 holtzmann-synoptische-evangelien-1863**: diesynoptischen00holtgoog. Holtzmann's Λ is read by the OCR as A or ^.
- **35/03 wernle-synoptische-frage-1899**: diesynoptischefr00wern.
- **35/04 weiss-alteste-evangelium-1903**: dasaltesteevange0000joha.
- **35/05 wellhausen-einleitung-1905**: einleitungindied00well.
- **35/06 harnack-spruche-und-reden-1907**: sprucheundredenj0000adol.
- **35/07 streeter-four-gospels-1925**: fourgospels0000stre.

Declared and not pursued: Schleiermacher's Papias essay (1832), no open text layer found in session; Lachmann (1835) and Wilke (1838), not sought in this round; Farrer 1955, Kloppenborg 1987, the IQP Critical Edition 2000 and Goodacre 2002, in copyright.

Build: `python3 gen_spec35.py`, `python3 add_loci35.py`, then `python3 ../ea-corpora-34/build34.py spec35-<corpus>.json ../../../data/corpora --loci` per seat; from the repository root, `python3 rebuild/corpora/ea-corpora-35/index_seats35.py`, `python3 rebuild/corpora/ea-corpora-35/body35.py` (writes data/issue-bodies/EA-CORPORA-35-issue.md), and after the deposit `python3 rebuild/corpora/ea-corpora-35/seat_axns35.py <N> --apply`.
