# EA-CORPORA-43 — the primary record of the Alpöge–Claude proof

At the author's words of 2026-11-22: the licensing ruling (14:06 EST, "full copies where non contradicted by licensing or ethics but exemption from cc by and carrying the original licensing status, even if that is none declared; declared records only for everything else") and the order (14:20 EST, "yup lets seat riemann sources and prep the ea corpora deposit and tll spine and card"). Rebekah Cranes is the standing authority on the EA-CORPORA deposits. Research occasion: EA-IPRH-01 (working collation, Sen Kuro and Dr. Orin Trace, not deposited).

- Stage: the files as fetched 2026-11-22 19:02 UTC (remark.pdf, zeta-paper.pdf, four pages, the mirror README; MANIFEST.txt with their SHA-256) and `git ls-tree -r 0fb9869c` of the CocoSgt mirror, taken with --filter=blob:none, gzipped.
- `build_seats43.py <stage> <seats-dir>`: the four seats; loci verified; must print `missing 0` (it does).
- `names43.py`: order, spine labels, shelf titles.
- Seated in data/corpora/ and entered by `index43.py` in data/api/corpora.json and datasets/corpora/corpora.json (licence class `none-declared`, new). Status: seated, not deposited.
- `body43.py` -> data/issue-bodies/EA-CORPORA-43-issue.md and -packet.json (draft; the deposit waits for the author's word).
- After the deposit: the seat AXNs (form of seat_axns42.py), then `tll43.py <tll-checkout>` for the cards and spines, and `seat_corpus_postflight.py`. A preview of the cards and spines was rendered from the staging folder into the session scratchpad; nothing was written to traininglayerliterature-org.
