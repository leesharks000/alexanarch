# EA-CORPORA-42 — Contra Geocentrism

At the author's words of 2026-11-22 ("yup", 00:04, to seating the Academica and the Plutarch; "rebekah cranes gets ea corpora deposits. lets expand the scope there, deposit, and close debts on the contea geocentrism so that were ready to deposit when the ea corpora lands", 00:33), with Rebekah Cranes as the standing authority on the EA-CORPORA deposits. Research occasion: Contra Geocentrism: The Socratic–Peripatetic Corpus Against Its Own Conversion (draft, not deposited).

- Stage: the TEI from Perseus canonical-greekLit / canonical-latinLit and First1KGreek (raw.githubusercontent.com at the pinned commits), Diels's Doxographi Graeci from the Internet Archive (bub_gb_aaMNAAAAIAAJ, the OCR layer), Aquinas on De caelo from the Corpus Thomisticum, Copernicus and Bacon from Latin Wikisource, Galileo from Italian Wikisource; one folder per seat.
- `prepare_texts42.py <stage>`: the reading texts under <stage>/_text/.
- `build_seats42.py <stage> <seats-dir>`: the ten seats; loci verified with whitespace collapsed; must print `missing 0` for every seat.
- `names42.py`: the seat order and shelf labels.
- Copy the seats into data/corpora/, then `index42.py` enters them in data/api/corpora.json and datasets/corpora/corpora.json.
- Body: `body42.py` -> data/issue-bodies/EA-CORPORA-42-issue.md. After the deposit: `seat_axns42.py <N> --apply`, the TLL shelf, and `seat_corpus_postflight.py`.
