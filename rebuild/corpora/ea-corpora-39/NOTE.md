# EA-CORPORA-39 — the field before the flattening, and the evidence of the census

At the operator's words of 2026-11-15 (22:43 EST, "i suppose we need to gather up materials for an ea-corpora seating for this one … especially as we increase holdings beyond the recent, where the flattening is already largely accomplished"; 22:56, "adopted on all. lets build the seating. but we need to find more accessible interim journals before the 2000s"), with Rebekah Cranes as the standing authority on the EA-CORPORA deposits. Research occasion: This Is Not Philosophy: How Disciplinarity Murdered Philosophy — The Shape of the Field (working notebook, not yet deposited).

The three rulings adopted: (1) the census seat holds titles, DOIs, the codes with their 6–30-word spans, the codebooks, logs and scripts; the publishers' abstracts are reached by DOI and not reseated; (2) Philologus and the Classical Quarterly: the cited volumes only, with pointers to the rest; (3) the gate documents as dated excerpts with URLs; the editor's responses to the submissions only, under the institutional ruling, his own views excluded.

- Stage the originals (fetched in session by `fetch_ia.py`; AGPh, the construction texts, Philologus, CQ), the OCR (`ocr_par.py`, tesseract 5, tessdata_fast; Schaarschmidt deu, Tennemann deu_latf), and the census (`stage_census39.py <survey-dir> <stage>/census-seat`).
- `build_seats39.py <stage> <seats-dir>`: the thirteen seats. The Archive's text layers held once, under text/, exactly as served (operator, 2026-11-15 23:51); loci verified with whitespace collapsed.
- `index39.py` enters the thirteen in data/api/corpora.json and datasets/corpora/corpora.json.
- After the deposit: `seat_axns39.py <N> --apply`; body: `body39.py`. The seating is deposited before the notebook it serves.

Already seated and not reseated (found when the builder met the existing seat): Schleiermacher, Platons Werke I.1 (EA-CORPORA-32/07); Campbell, The Sophistes and Politicus (32/08); Tennemann, System der Platonischen Philosophie I (32/09; a second OCR, from the scan bub_gb_uuk9AAAAcAAJ, was made in session and is not seated); Jaeger, Aristoteles (31/10).

The order (operator, 2026-11-15 23:51): "the seating goes first - we have more analysis to run from it".

Pointers to the rest (to be carried into the body): AGPh XIV, XXIX, XXXII (not in the Toronto run); Philologus and CQ beyond the cited volumes (the full Crossref census of both is in 39/12); the interim journals with open full text before 2000 — the Revue philosophique de Louvain (Persée, 1894–), the Revue des Études Grecques (Persée), Museum Helveticum (e-periodica) — whose Persée metadata is in 39/12 and whose texts are for a later seating.
