# EA-CORPORA-40 — Philology Constituted

At the operator's words of 2026-11-16 ("oh - and we need an ea-corpora. what can and should be gathered up? philology is a rich historical field"; "first we check what we have"; "lets begin gathering for the ea corpora"; "certainly we can locate wilamowitz elsewhere... and Nietzsche - there must be copies"; 14:48 EST, "and then yes lets build the ea-corpora deposit"), with Rebekah Cranes as the standing authority on the EA-CORPORA deposits. Research occasion: The Philology Census, Classical Philology first (working notebook v0.1, not deposited). Biblical criticism is kept apart from this seating (14:53 EST: "keep biblical separate from the current question, and after we've done both separately we'll look at the combine").

- Stage: the gathering folder (books/ and books-log.json from fetch_books.py; cp/, cp-log.json and cp-jstor-items.json from fetch_cp.py) and the census folder (census_cp.py and its outputs, the notebook, the inventory, census-README.md).
- `build_seats40.py <stage> <census> <seats-dir>`: the sixteen seats; every served file checked against its fetch-log SHA-256; loci verified with whitespace collapsed.
- `index40.py` enters the sixteen in data/api/corpora.json and datasets/corpora/corpora.json.
- After the deposit: `seat_axns40.py <N> --apply`; body: `body40.py`. The seating is deposited before the census it serves.
