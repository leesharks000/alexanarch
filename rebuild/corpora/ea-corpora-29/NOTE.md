# EA-CORPORA-29 — held for the next EA-CORPORA deposit

At the operator's ruling of 2026-10-28 this seating takes no deposit of its own: its seats and repairs are recorded here and bundled into the next EA-CORPORA deposit, which assigns the new seats their AXNs.

Raised by *Belief & Technique for Telepathic Prose: A Critical Edition* (§11), at the operator's ruling of 2026-10-28.

- **29/01 jack-kerouac** — a declared absence: Belief & Technique for Modern Prose, Essentials of Spontaneous Prose, the novels and Mexico City Blues (absences29.py).
- **29/02 horace** — Horace entire in Latin, six works from PerseusDL/canonical-latinLit at commit 8b536bdf3ed1f43494055efe112433b4a58eab67 (spec29-horace.json, built with rebuild/corpora/ea-corpora-27/seat.py); the Ars Poetica with the loci of its close verified.
The pluriform bundle of arts of poetry, at the author's directions of 2026-10-28 ("an extremely pluriform ars poetica bundle … include telepathic prose"; "seat all of ovid"; "further globally, hebrew, sanskrit, korean"; "Tradition and the Individual Seismograph" beside Eliot's):

- **29/03 ovid**: Ovid in Latin, nine works from PerseusDL/canonical-latinLit at the same commit (spec29-ovid.json). The Fasti is queued: the Perseus text is Frazer's Loeb of 1931, in copyright in the United States until 2027-01-01.
- **29/04 ars-poetica**: sixty-four arts of poetry in twenty traditions: Greek, Latin, Sanskrit, Tamil, Chinese, Japanese, Korean, Hebrew, Arabic, Persian, Old Norse, Irish, Occitan, Italian, French, Spanish, Portuguese, German, Russian and English. Johannes Sigil's "Tradition and the Individual Seismograph" stands beside Eliot's essay, copied from the Pearl seat. Built from gen_spec29_ars.py with build29.py. The sources are Perseus, GRETIL, Wikisource with its revision ids, Gutenberg, Aozora Bunko and Internet Archive OCR; the six largest scans are held by reference with the Archive's md5. All 64 loci are verified. The GRETIL files are CC BY-NC-SA, so they fall under the NC payload/record split of EA-CORPORA-02.
- **29/05 avant-garde-ii**: eleven statements of method, 1913–1929. Flint and Pound in Poetry 1.6; Kora in Hell; En avant Dada; La Révolution surréaliste nos. 1 and 12; Arvatov in LEF; Hu Shi and Chen Duxiu for the New Literature; Paulo Prado's preface to Pau Brasil. Built from gen_spec29_ag.py.
- **29/06 ars-poetica-wanted**: a declared absence of fifty-nine works (absences29_wanted.py). Eleven are public domain with no copy found this session. The rest are the copyrighted moderns, Language writing, conceptual writing and the contemporary arts of poetry, each with its opening date.
- **29/07 telepathic-prose**: Belief & Technique for Telepathic Prose, Make It Human and A Telepathicist Manifesto, each in both witnesses. The P text is copied from the Pearl seat by line range and sha256; the B text is the blog page as served. The edition (#1715) is copied from data/deposits. The drafts of 2014 are held out pending the author's ruling (gen_spec29_tp.py).

The 2014 drafts were added to 29/07 at the author's ruling of 2026-10-28 ("sure i suppose the drafts can be seated"). They are the Drive connector's text exports of "BELIEF AND TECHNIQUE FOR TELEPATHIC PROSE.docx" (D2, D3, D1, with the notebook entries) and "word riot 4.docx" (W). The .docx files are recorded by Drive id.

The Buddhist canons, at the author's direction of 2026-10-28 ("we need buddhist canon, various traditions, mahayana included"):

- **29/08 pali-tipitaka**: the three piṭakas in root Pali (Mahāsaṅgīti), from suttacentral/bilara-data at commit da23a8a, in 37 collections and books. The original is a byte-reproducible git archive of root/pli/ms (pali29.py). This is the harvest 02/17 queued.
- **29/09 buddhist-sanskrit**: thirty-two GRETIL TEI files: fourteen Mahāyāna sūtras, twelve śāstras, and six works of kāvya and narrative (gen_spec29_mahayana.py).
- **29/10 east-asian-buddhism**: twenty works from Wikisource. Nine are of the Chinese canon and six of Chan. Four are of Japan: the Tannishō in the 1923 rendering, Hōnen, Hakuin, and the Heart Sūtra. One is of Korea: Han Yong-un's 님의 沈默 (1926), in ninety pages. The Shōbōgenzō and the Zuimonki are queued.
- **29/11 derge-kangyur**: eight volumes of the Digital Derge Kangyur (Esukhia, public domain by its README) (tib29.py). They carry the Aṣṭasāhasrikā, the Diamond, the Heart, the Lalitavistara, the Laṅkāvatāra, the Lotus, the Sukhāvatīvyūha and the Vimalakīrti, with the Vinaya's first volume and the catalogue. The loci are the Tohoku markers.

The seating is deposited as EA-CORPORA-29, #1716, AXN:0A9F.DATASET (body29.py writes the issue body), at the author's request of 2026-10-28. The eleven seats take their AXNs from it as AXN:0A9F.ORIGINAL (seat_axns29.py).

The source.json `seat`, `spine` and `seating` fields of 29/03–29/11 were set to the form 29/01–29/02 carry. `build29.py --loci` re-verifies a built seat's loci without refetching.

- **02/14 dickinson-mss** — the first queued print layer seated: Letters of Emily Dickinson, ed. Todd (1894), Internet Archive lettersemilydic00toadgoog, md5-checked; L265 verified at pp. 303–304 (source.json, print_layers).
- **01/13 homer, repair** — the Odyssey text layer's book tags re-derived from the TEI (every line was tagged book 1); the Greek unchanged; recorded in source.json, repairs.

Indexed in data/api/corpora.json and datasets/corpora/corpora.json (index_seats.py). The TLL shelf cards are rendered by scripts/build_originals_shelf.py in the traininglayerliterature-org repository.
