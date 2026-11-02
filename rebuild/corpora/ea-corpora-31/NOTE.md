# EA-CORPORA-31 — the transmission of the Peripatetic corpus

At the operator's ruling of 2026-11-01 ("lets gather and seat those. with an ea-corpora"), the texts named in §5 of the design Legitimately Many (drafts/LEGITIMATELY-MANY-design-2026-11-01.md) are seated in their original languages.

- **31/01 athenaeus**: the Deipnosophistae in Kaibel's Greek (Perseus perseus-grc3, commit 341e309); I.3a–b, the sale of Neleus's books to Ptolemy Philadelphus, verified.
- **31/02 galen**: In Hippocratis De natura hominis (Kühn XV, First1KGreek, commit ed91552); the forgery of titles for the competing Attalid and Ptolemaic book-buyers verified.
- **31/03 porphyry**: the Life of Plotinus in Volkmann's volume I (1883), the Archive's OCR, the scan by reference; ch. 24 on Andronicus verified in the OCR's own readings.
- **31/04 aristotle-commentators**: Ammonius, Simplicius, Philoponus, Olympiodorus (Prolegomena and In Cat.), Elias and David from First1KGreek (CAG). The TEI mixes composed and decomposed Greek, so nfcfix31.py rewrote eleven loci in the text's own characters after the first build; gen_spec31.py would undo that, so the spec on disk is the record.
- **31/05 arabic-biobibliography**: Ibn al-Nadīm's Fihrist (Flügel), Ibn al-Qifṭī's Ikhbār and Ibn Abī Uṣaybiʿa's ʿUyūn from OpenITI, CC BY-NC-SA under the NC payload/record split of EA-CORPORA-02; Ptolemy al-Gharīb's book to Gallus verified in all three.
- **31/06 hermippus**: ninety-three fragments of Hermippus the Callimachean, FHG III, from the DFHG API (CC BY-SA 4.0 as the project states).
- **31/07 hesychian-catalogue**: Rose 1886 pp. 9–22, OCR'd in session (Tesseract 5.3.4, tessdata_best grc+lat), the page images by URL and sha256.
- **31/08 callimachus-pinakes**: Schneider, Callimachea II (1873) pp. 296–328, fr. 100d, OCR'd in session.
- **31/09 bekker-aristotle-1831**: the Praefatio of Aristoteles graece I (1831), OCR'd in session.
- **31/10 jaeger-aristoteles**: Jaeger, Aristoteles (1923), the Archive's OCR; US public domain, the EU term running to 2031.
- **31/11 transmission-wanted**: a declared absence of sixteen works (absences31_wanted.py).

Build: `python3 gen_spec31.py` (once), then `python3 build31.py spec31-<corpus>.json ../../../data/corpora` per seat, `python3 nfcfix31.py spec31-aristotle-commentators.json ../../../data/corpora`, `python3 build31.py … --loci`, `python3 absences31_wanted.py ../../../data/corpora`, and `python3 index_seats31.py`. The OCR files made in session are under ocr/. After the deposit, `seat_axns31.py <deposit> --apply` gives the seats their AXNs.
