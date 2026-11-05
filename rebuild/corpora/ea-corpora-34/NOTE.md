# EA-CORPORA-34 — Secondary Source: the reception of the Apocalypse, from the fathers to the critics

At the operator's word of 2026-11-05 09:03 EST ("also - lets gather up and seat the sources we'll need for this one prior to writing. still under rebekah cranes for the ea-corpora, and with reference to the research occasion"), with Rebekah Cranes as the standing authority on the EA-CORPORA deposits. The research occasion is Secondary Source (drafts/SECONDARY-SOURCE-design-2026-11-05.md, v0.3, §5).

- **34/01 eusebius-historia-ecclesiastica**: First1KGreek tlg2018.tlg002.1st1K-grc2 (Dindorf 1871), commit ed91552c; Dindorf chosen over Lake–Oulton (Loeb, 1926–1932) for its term. HE 3.25.4, 3.28.2, 5.8.6, 7.24.1 verified.
- **34/02 irenaeus-adversus-haereses**: First1KGreek tlg1447.tlg001 (Harvey's Greek) and Harvey's two volumes at the Archive (Latin); 5.30.3 verified in the Latin.
- **34/03 justin-dialogus**: First1KGreek tlg0645.tlg003.perseus-grc2 (Archambault 1909); Dial. 81.4 verified.
- **34/04 muratorian-fragment-tregelles**: Tregelles 1867 (canonmuratorianu00treg); lines 47–50 verified in the OCR.
- **34/05 epiphanius-panarion**: First1KGreek tlg2021.tlg002 (Holl); heresy 51 verified.
- **34/06 westcott-canon-1896**: Westcott, General Survey, 7th ed. (cu31924029301582), Appendix D, the catalogues in their original languages.
- **34/07 collectio-hispana-1808**: the Collectio Hispana (A28009301); Toledo IV canon 17 verified.
- **34/08 september-testament-1522**: the 1883 facsimile (DasNeweTestamentDeutzsch1522); the text layer is unreadable black letter, the scan is the witness.
- **34/09 erasmus-annotationes-1535**: ARes162052.
- **34/10 revelation-criticism-1886-1920**: Vischer, Spitta, Gunkel, Bousset 1896 and 1913, Charles I–II.
- **34/11 gregory-textkritik-1900**: textkritikdesneu0001greg.

Declared and not pursued: Metzger 1987, Hahneman 1992, WA Deutsche Bibel 7 (in copyright); Zwingli's Sämtliche Werke (access-restricted). The Archive's PDFs are held by reference, not copied.

Build: `python3 gen_spec34.py`, then `python3 build34.py spec34-<corpus>.json ../../../data/corpora` per seat, then `python3 fix_loci34.py` (the First1KGreek TEI is not in NFC; the Greek loci are rewritten into its code points) and `python3 build34.py spec34-<corpus>.json ../../../data/corpora --loci` for the seats it changed, then `python3 index_seats34.py` and `python3 body34.py` (writes data/issue-bodies/EA-CORPORA-34-issue.md). Not deposited: the deposit waits on the operator's word.
