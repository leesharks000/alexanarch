# EA-CORPORA-32 — the remaining debts of Legitimately Many

At the operator's word of 2026-11-02 ("lets prepare that seating, its ea corpora deposit, and its tll spine and card"), the texts still owed in §5 of the design Legitimately Many (drafts/LEGITIMATELY-MANY-design-2026-11-01.md) are seated in their original languages. By the operator's rule of the same day ("seatings when conducted in the course of active research should mention the research in connection to which they were seated"), every seat carries a `research` field naming the study, its design and draft, and the section that owes the text; research31_backfill.py wrote the same field into the EA-CORPORA-31 seats, outside their manifests, so their AXNs are unchanged.

- **32/01 pseudo-archytas**: Mullach, Fragmenta philosophorum Graecorum I (1860), the Archive's OCR; the book on the ten categories verified in Mullach's Latin.
- **32/02 aldine-aristotle-1497**: the Aldine Aristotle vol. IV (1 June 1497), Boston Public Library copy (opera05aris), leaves n576–n588 held as images by URL and sha256; the title, running heads, scholion, register and colophons transcribed by eye in session (transcriptions/).
- **32/03 theophrastus-metaphysics-wimmer-1866**: Wimmer's Didot Theophrastus, the Archive's OCR; the preface on Brandis 1823 verified; no copy of the scholion found in the OCR layer.
- **32/04 philodemus-index-academicorum**: Mekler 1902, leaves n35–n157 OCR'd in session (grc+lat); Spengel's supplement of the pupils' names from Diogenes at Col. VI verified.
- **32/05 dionysius-ad-ammaeum**: Perseus tlg0081.tlg008 (commit 341e309).
- **32/06 cicero-ad-atticum**: Perseus phi0474.phi057 (canonical-latinLit commit 8b536bd); Att. IV.16.2 verified. The cicero seat (13/03) was checked first and holds no letters.
- **32/07 schleiermacher-platons-werke-1804**: Platons Werke I.1 (1804), BSB scan, the Archive's OCR.
- **32/08 campbell-sophistes-politicus**: Campbell 1867, the Archive's OCR.
- **32/09 tennemann-platonische-philosophie**: System I (1792) and Geschichte II (1799), the Archive's OCR.
- **32/10 hegel**: Differenzschrift (1801) leaves n7–n60 and Vorlesungen II (1833) pp. 169–241, OCR'd in session with tessdata_best deu_latf.
- **32/11 legitimately-many-wanted**: a declared absence of sixteen works (absences32_wanted.py).

Build: `python3 gen_spec32.py`, then `python3 build32.py spec32-<corpus>.json ../../../data/corpora` per seat, `python3 absences32_wanted.py ../../../data/corpora`, `python3 research31_backfill.py ../../../data/corpora` and `python3 index_seats32.py`. The OCR files made in session are under ocr/. After the deposit, `seat_axns32.py <deposit> --apply` gives the seats their AXNs.
