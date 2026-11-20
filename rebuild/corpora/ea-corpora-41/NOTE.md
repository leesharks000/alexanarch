# EA-CORPORA-41 — Alexander, Antipater and Athens

At the author's words of 2026-11-20 ("lets bather all the texts weve touched on or even referred to between then and here for a ea-corpora seating", 18:31, the span from the Cicero/Sulla paste of 17:19; "put the tragedians in there too while were at it", 18:31; "and the catiline conspiracy", 18:40), with Rebekah Cranes as the standing authority on the EA-CORPORA deposits. Research occasion: the evening's thread, and its groundwork note The Thinkery and the Lyceum (v0.1, not deposited).

- Stage: the TEI from Perseus canonical-greekLit / canonical-latinLit and First1KGreek (sparse clones), Cicero's De legibus from The Latin Library, Yoma 69a and Megillat Ta'anit from Sefaria API v3, and plan.json.
- `prepare_texts41.py <stage>`: the reading texts under <stage>/_text/.
- `build_seats41.py <stage> <seats-dir>`: the fourteen seats; loci verified with whitespace collapsed; must print `missing 0` for every seat.
- `names41.py`: the seat order and shelf labels, shared by the scripts below.
- Copy the seats into data/corpora/, then `index41.py` enters them in data/api/corpora.json and datasets/corpora/corpora.json.
- Body: `body41.py` -> data/issue-bodies/EA-CORPORA-41-issue.md. After the deposit: `seat_axns41.py <N> --apply`, the TLL shelf, and `seat_corpus_postflight.py`.
