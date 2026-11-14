# EA-CORPORA-38 — the reception history of inference

At the operator's words of 2026-11-14 (01:25 EST, "lets continue to assemble and we'll deposit and seat the whole thing as a massive batch"; 08:57, "lets deposit with what we have and leave pointers to the rest"), with Rebekah Cranes as the standing authority on the EA-CORPORA deposits. Research occasion: Critique of Pure Inference (working draft v1.1), §11.6 "the witnesses between", and The Production of Readers (#1767).

- Stage the originals (fetched in session; the sources are in each seat's source.json), then `prepare_texts38.py <stage>` reduces them to text layers by code.
- 38/02–38/16: `build_seats38.py <stage> <seats-dir>`.
- 38/01: `build_kant38.py <kant-ia-dir> <seats-dir>`: AA I–XVIII, Fraktur OCR made for the seat (tesseract 5, tessdata_best deu_latf) from the Internet Archive's page images; the Archive's text layers held beside it.
- 38/15's Arabic OCR: tesseract 5, tessdata_best ara, from the Archive's page images of Forget 1892.
- `index38.py` enters the sixteen in data/api/corpora.json and datasets/corpora/corpora.json.
- After the deposit: `seat_axns38.py <N> --apply`; body: `body38.py`.
