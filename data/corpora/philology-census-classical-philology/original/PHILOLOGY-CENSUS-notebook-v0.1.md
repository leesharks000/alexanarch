# The Philology Census: *Classical Philology* first

Working notebook v0.1, 16 November 2026. Not deposited. It is the combined audit's next station after #1770 (CRJ) and #1773 (*Ancient Philosophy*), on the same instrument (#1773 §§4.1–4.9).

---

## 0. The prediction

The author (16 November 2026): "i imagine, that philology will have less apparent flattening - it has at least to attend to language - but that it will still be there, molecular reach that holistically preserves the molar."

Stated as measures:
- the questions about the text itself (D) stay present at the grain of the locus: emendation, crux, reading, colometry;
- they thin at the grain of the work: authenticity, date, unity, transmission;
- they are near zero at the grain of the corpus: the partition of a corpus among composing persons, the author as unit;
- where the corpus grain is touched, it is touched by a locus and resolved toward the received partition.

A blind parallel census is run by ChatGPT on the same items (§3).

---

## 1. The census

**Source.** Crossref, journal ISSN 0009-837X, pulled 16 November 2026: 11,206 records, 1906–2026 (`census-cp.json`, with the raw sha256).

**Abstracts.** Crossref holds none for this journal (0 of 11,206). Reach coding is therefore from titles, and the limits of that are stated in §4.

**Filter.** Journal articles only. Reviews are removed (titles opening on an italic book title, 5,525 of them). So are the front matter, back matter, "Books Received", volume information and the like (1,010). Untitled items are dropped.

**Kept: 4,252 items** (`cp-items.json`, ids CP0001–CP4252 in date order). Items of 10 or more pages are counted as articles; shorter items are notes. In philology the note is where much locus-level work is published, so notes are kept.

| Decade | Items | of which ≥ 10 pp |
|---|---|---|
| 1900s | 190 | 57 |
| 1910s | 441 | 175 |
| 1920s | 443 | 130 |
| 1930s | 403 | 136 |
| 1940s | 324 | 96 |
| 1950s | 284 | 51 |
| 1960s | 314 | 51 |
| 1970s | 415 | 82 |
| 1980s | 320 | 108 |
| 1990s | 259 | 132 |
| 2000s | 263 | 158 |
| 2010s | 293 | 176 |
| 2020s | 303 | 190 |

The journal moves from the note to the article. Long items rise from about a third of items to about two-thirds after 1990.

---

## 2. The codebook: reach for philology

The categories are those of #1773 §4.6, kept for comparability. D is split by grain, and two categories are added for work philology does that philosophy does not.

- **A, locus.** Re-reads a passage for its sense.
- **B, repair.** Resolves an apparent inconsistency or problem inside an author.
- **C, reconstruction.** Reconstructs a doctrine, institution, practice, event or context from texts.
- **D1, text at the locus.** Emendation, conjecture, crux, reading of a manuscript at a passage, lacuna, colometry, interpolation of a line or passage.
- **D2, text at the work.** Authenticity, authorship, date, unity or composition of a work; its manuscript tradition or recension; an edition.
- **D3, text at the corpus.** The partition of a corpus among composing persons. Whether names in a corpus are one maker or several, and whether the author is the right unit.
- **E, relation.** Sources, imitation, allusion, influence, intertext between authors.
- **F, after antiquity.** Reception and transmission beyond antiquity, as an object of study.
- **G, position.** Argues a thesis not anchored to an author or text: method, theory, a general claim.
- **L, language.** Grammar, lexicon, metre, accent, dialect, style as language.
- **M, document.** Publishes or reads an inscription, papyrus or object as a document.

For each D code, also mark *confirm* or *open*. *Confirm* means the title settles toward the received standing; *open* means it puts the standing in question.

---

## 3. The blind parallel run

ChatGPT codes the same items on the same codebook, without seeing any code made here. Agreement is then measured. This is the cross-family check that #1773 §7.5 asked for, since every reach code so far has been made within one model family.

Two files go to it:
- `cp-titles-sample390.csv`: a stratified sample, 30 per decade, seed 31;
- `cp-titles-all.csv`: all 4,252 items, if it can take them.

The prompt is in the reply, ready to paste. The sample's ids are recorded (`sample390-ids.json`) so that both coders' work can be joined.

---

## 4. A first pass, and its limits

**What it is.** A lexicon over the titles, run before any reading, to see the shape. It is not the census's coding. The census's coding is the reading of §2, done by readers and adjudicated, with the blind run as its check.

**Textual and standing vocabulary in titles, by decade, as a share of items:**

| Decade | D1 terms | D2 terms | either |
|---|---|---|---|
| 1900s | 5.8% | 8.9% | 14.2% |
| 1910s | 4.8% | 5.4% | 10.0% |
| 1920s | 2.9% | 5.4% | 8.1% |
| 1930s | 3.7% | 7.9% | 11.7% |
| 1940s | 4.3% | 4.0% | 8.3% |
| 1950s | 1.8% | 6.3% | 8.1% |
| 1960s | 1.9% | 5.7% | 7.3% |
| 1970s | 3.9% | 4.8% | 8.7% |
| 1980s | 3.4% | 5.6% | 8.8% |
| 1990s | 5.8% | 2.3% | 8.1% |
| 2000s | 3.4% | 1.9% | 5.3% |
| 2010s | 4.1% | 2.4% | 6.1% |
| 2020s | 4.0% | 4.6% | 7.9% |

**The shape, provisionally.**
- *The locus grain holds.* D1 vocabulary runs at 2–6% of titles in every decade, with no trend.
- *The work grain thins and returns.* D2 vocabulary sits at 5–9% before 1990, drops to about 2% in 1990–2019, and comes back to 4.6% in the 2020s.
- *Nothing like the* Archiv. There, standing titles go from 19% in the 1890s to 0% by the 1910s (#1773 §4.12). This matches the prediction's first clause: less apparent flattening.

**The corpus grain, read by hand.** The 35 titles the D3 lexicon flagged, all of them, are read in `d3-candidates.json`.
- *Single works.* Every authorship question among them is about one work or one passage: the *Moretum* (1925), the *Laus Pisonis* (1929), the *Pervigilium Veneris* (1929), the *Epistola de Indicis Gentibus* (1926), Anthologia Latina 899 (1985), [Arist.] *De spiritu* (2015), Euripides' *Electra* 518–44 (2024).
- *One case merges names into one maker:* "The Ovidian Authorship of the Lygdamus Elegies" (1927). Lygdamus is a name inside the Tibullan corpus, with no attestation outside it. That fits the line #1773 §0A.6a draws. The field admits a merger when the second name is only a name; it has no case of persons attested apart.
- *One case reaches the Socratic partition, at a locus:* "On Separating the Socratic from the Platonic in Phaedo 118" (1975, 2 pp). The molar question is taken up at one passage, and the operation is separation.
- *One title states the direction:* "Authorship Analysis and the Authenticity of Euripides' Electra 518–44: Preserving Character Consistency" (2024).

**Limits.**
- Titles under-report D. A note titled with a locus alone ("Lysias 19. 22 and 18. 14") may be an emendation. The lexicon counts it as nothing, and the reading of §2 has to decide it.
- Crossref's typing of reviews is unreliable, and the italic rule may admit a few reviews or drop a few articles. Both filters are to be audited on the sample.
- The full text of the volumes before 1928 is public domain. Those volumes can be read whole, as the *Archiv* was (#1773 §4.12g), and that is the next measure for the early decades.

---

## 5. Next

5.1 Code the sample of 390 on §2, by hand, before the blind run returns. Then compare.

5.2 Code all 4,252 with readers, each code with its span (the title), adjudicated against the sample.

5.3 Read the pre-1928 volumes whole for D at each grain, against the titles.

5.4 The next journals: *Classical Quarterly*, *Mnemosyne*, *Hermes*, *Philologus* and *Glotta*, so that philology is measured at more than one desk.

5.5 The gate: CP's own author guidelines and its AI policy, dated, as in #1773 §4.16.
