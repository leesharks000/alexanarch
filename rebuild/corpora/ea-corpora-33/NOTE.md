# EA-CORPORA-33 — song and silence: Tacitus, and Sappho whole with the melic poets

At the operator's word of 2026-11-04 ("and I suppose we should seat tacitus"; "we need all sappho and all the melic poets ... they can go together with tacitus, song and silence at one seat"; "corinna definitely ... yet lets seat the[m]"), with Rebekah Cranes as the standing authority on the EA-CORPORA deposits (11:46 EST) and Edmonds seated with a statement of its term (11:54 EST).

- **33/01 tacitus**: Perseus canonical-latinLit phi1351.phi001–phi005 (commit bfdcd06): Agricola, Germania, Dialogus (Furneaux), Historiae (Fisher 1911), Annales (Fisher 1906); Hist. 5.1 and 5.13 verified.
- **33/02 pindar**: Perseus canonical-greekLit tlg0033.tlg001–tlg004 (commit 282e6f5), Sandys. The fragments (Bergk PLG⁴ I) queued.
- **33/03 bacchylides**: Perseus tlg0199.tlg001–tlg002, Jebb 1905.
- **33/04 poetae-melici-bergk**: Bergk, Poetae Lyrici Graeci⁴ III (1882), Internet Archive poetaelyricigrae03berguoft, the PDF (764 pages) rasterized at 300 dpi and OCR'd in session (Tesseract 5.3.4, tessdata_best grc+lat), divided into 35 sections at the running heads (split_bergk33.py, corrected by reading the boundary pages; the list is in gen_spec33.py as B_RUNS).
- **33/05 lyra-graeca-edmonds-i**: Edmonds, Lyra Graeca I (1922), Internet Archive lyragraecabeingr01edmouoft, the PDF (490 pages) OCR'd in session (grc+eng), divided at the running heads; public domain in the United States, in term elsewhere until the end of 2028, held with that statement.

Build: `python3 gen_spec33.py`, then `python3 build33.py spec33-<corpus>.json ../../../data/corpora` per seat, `python3 index_seats33.py` and `python3 body33.py` (writes data/issue-bodies/EA-CORPORA-33-issue.md). The OCR was made in the session scratchpad and is carried into each seat under original/<identifier>/ocr/. After the deposit, seat AXNs are given in the form of seat_axns32.py.
