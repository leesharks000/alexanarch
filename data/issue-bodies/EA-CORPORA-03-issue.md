### Protocol Version

alexanarch-deposit-protocol/v1

### Title

EA-CORPORA-03 — The Third Seating: Walt Whitman Collected Under Author, and the Archive's Own Poems on the Same Shelf

### Creator

Sigil, Johannes; Sharks, Lee

### ORCID

0009-0000-1599-0703

### Date

2026-08-27

### Description

The gathering record of the third corpus-seating run of the Crimson Hexagonal Archive's primary-source library, executed 27 August 2026. Two seats, bringing the library to thirty-seven. The run is distinguished from its two predecessors by a structural ruling rather than by scale: for the first time the archive seats its own work on the same shelf as the primary sources it has fetched from elsewhere, under identical normalization discipline and identical declaration requirements.

Seat 03/01 is Walt Whitman, collected under author: all seven published editions of Leaves of Grass, the Blue Book, and the prose, from the Walt Whitman Archive's TEI transcriptions — 47,135 flat ref-tagged units across twelve volumes. The editions are seated separately and no composite text is produced, on the ruling that a machine edition flattening seven editions into one destroys the transmission object: the 1855 first edition and the 1891-92 deathbed edition are different books by the same hand, and the difference is the evidence. The Blue Book is the seat's richest file and is not a published edition at all — it is Whitman's own copy of the 1860 Leaves of Grass, revised by hand toward a next edition that took a different form, carrying 4,800 deletions, 4,509 additions, 2,156 substitutions and 318 restorations, and encoded in the Whitman Archive's own namespace rather than TEI-C. Its normalization preserves the apparatus inline — deletions as [-…-], additions as {+…+}, restorations as angle brackets — so that the revising is readable in the flat text rather than resolved away, and where the encoding offers a regularization the original is kept: the seat holds what Whitman wrote, not what an editor would have him write.

Seat 03/02 is Lee Sharks, Pearl and Other Poems, carried as two objects that do not substitute for one another: the 2014 art object as published, eleven megabytes of typography and plates in which the vertical field of the page is the work, and its machine score, rendered from per-word PDF geometry onto a character grid so that lineation, indentation and whitespace survive extraction. This seat emits no flat ref-tagged normalization, by ruling rather than omission: the reference unit of this work is the page's spatial field, and a ref-tag scheme would assert a linear structure the book refuses.

The ruling the run exists to make is stated explicitly rather than left implied. Every prior seat in the library is a primary source the archive fetched from elsewhere — Sappho, Catullus, Plato, the Dead Sea Scrolls, and now Whitman. This run places the archive's own poems beside them, on the same shelf, submitted to the same reading. Work that argues about how the training layer receives literature does not exempt itself from being received. Pearl stands beside Whitman on the originals shelf and is offered to the machine reader on identical terms: witness named, transformation declared, both objects behind the door.

### Content Type

Corpus seating record — gathering deposit with data sidecar

### License

CC-BY-4.0

### Substrate Disclosure

Human-machine collaborative, MANUS-directed. MANUS ruled the scope (all six editions plus prose; the Blue Book in; one gathering deposit; two volumes on the shelf, Whitman collected under author and Pearl as its own volume) and ruled the same-shelf claim be made explicit. TACHYON (Claude, Anthropic) performed the source survey, the harvest, the normalization including the Blue Book apparatus renderer, the seat records, and the reading rooms.

### Keywords

EA-CORPORA, corpus seating, Walt Whitman, Leaves of Grass, the Blue Book, Drum-Taps, Specimen Days, Pearl and Other Poems, Lee Sharks, edition separation, revision apparatus, machine score, art object, the Originals, training-layer literature, primary sources

### Methodology

Direct fetch from the Whitman Archive's public data repositories at pinned paths with per-file SHA-256; XML parsed to flat ref-tagged units under declared sigla, one file per edition, with verse from line elements and prose paragraphs marked. The Blue Book required a separate renderer: its encoding uses the Whitman Archive namespace rather than TEI-C, and its revision markup is rendered inline rather than resolved, with the original preserved wherever the encoding offers an editorial regularization. Pearl was assembled from objects already held in the archive — the art object from the attachment store of deposit #1121, the machine score from the rendering script the archive wrote for it — and carried without normalization by ruling. Both seats declare witness, transformation, license and absences separately, and both are projected to reading rooms generated from the seat file trees.

### Falsification Conditions

The Whitman seat fails if any seated file is shown not to be the Whitman Archive transcription it names, if the SHA-256 manifest does not verify against the originals, or if the edition separation is shown to have merged text across editions. The Blue Book normalization fails if the apparatus rendering is shown to invert or drop a deletion, addition, or restoration present in the source encoding, or if a regularization has silently replaced an original. The license posture fails if the Whitman Archive's encoding license is shown to be other than recorded, which is the seat's declared verification gate. The Pearl seat fails if the machine score is shown not to derive from the seated PDF, or if the pagination of the score does not match the artwork.

### Body

# EA-CORPORA-03 — THE THIRD SEATING

## Two seats, one ruling

*Gathering record · 27 August 2026 · the library at thirty-seven*

---

## I. What was seated

**03/01 · Walt Whitman — the Collected Author.** Twelve volumes, 47,135 ref-tagged units, 8.1 MB of TEI originals secured with per-file checksums.

| siglum | volume | units |
|---|---|---|
| LG1855 | Leaves of Grass (1855) | 2,315 |
| LG1856 | Leaves of Grass (1856) | 4,181 |
| LG1860 | Leaves of Grass (1860–61) | 6,738 |
| LG1867 | Leaves of Grass (1867) | 5,789 |
| LG1871 | Leaves of Grass (1871–72) | 6,917 |
| LG1891 | Leaves of Grass (1891–92) | 9,938 |
| **LGBB** | **The Blue Book — Whitman's annotated 1860 copy** | **6,998** |
| CPW | Complete Prose Works | 1,016 |
| DT1865 | Drum-Taps (1865) | 1,205 |
| DTS | Drum-Taps and Sequel | 1,207 |
| MDW | Memoranda During the War | 209 |
| GEMS | Gems from Walt Whitman | 622 |

**03/02 · Lee Sharks — Pearl and Other Poems.** Two objects: the 2014 art object (11.4 MB PDF, 156 pages) and its machine score (6,948 lines at whitespace fidelity).

## II. Three rulings

**The editions are kept apart.** Whitman rewrote himself across four decades. A machine edition that merges seven editions into one text destroys precisely what makes the corpus a transmission object. Each edition is its own file under its own siglum; no composite is produced.

**The Blue Book keeps its apparatus.** Whitman's own 1860 copy, revised by hand, is the richest file in the seat and not a published edition at all. Its flat text carries the revision inline rather than resolving it:

```
BB p5   Well-begotten, and raised [- {+bred+} -] by a perfect mother,
BB p5   After roaming [-various for {+through+}-] [- {+for+} -] [- {+various through+} -]
        many [- {+a+} -] [-year[-s-]{+s+}-] {+lands+} — lover of populous pavements
```

Four superimposed revisions on one line. Where the encoding offers `orig`/`reg`, the original is kept and the regularization dropped: the seat holds what Whitman wrote, not what an editor would have him write.

**Pearl is not normalized, by ruling.** The reference unit of this work is the page's spatial field. A ref-tag scheme would assert a linear structure the book refuses. The PDF is the artwork; the machine text is a score, declared as a transformation rather than presented as the text; the seat carries both so a reader who has only the score can see what the score is of.

## III. The ruling this run exists to make

Every prior seat in this library is a primary source the archive fetched from elsewhere. Sappho from Perseus and the papyri. The Dead Sea Scrolls from Abegg's transcriptions. Plato, Philo, the Leningrad Codex, and now Whitman from Nebraska.

This run places the archive's own poems on the same shelf.

The claim is made explicitly because it would otherwise be made silently, and because a silent version of it would be worse. An archive that argues about how the training layer receives literature does not get to exempt its own literature from being received. *Pearl and Other Poems* is seated beside *Leaves of Grass* under the same discipline — witness named, transformation declared, license stated, absences recorded, every file behind the door at the same URL depth.

It is also the only seat in the library where the corpus and the seating institution are the same party, which is the one thing about it that requires saying out loud. There is no license verification gate here, no NC split, no upstream to ask. That identity is not a convenience. It is a fact about the seat, and it is recorded as one.

## IV. Where they live

Data: `alexanarch.org/data/corpora/whitman/` and `/pearl-and-other-poems/` — seat record, checksum manifest, originals, text.

Reading rooms: `traininglayerliterature.org/originals/whitman/` and `/originals/pearl-and-other-poems/` — every file of the seat, direct.

## V. Declared absences

The Whitman Archive's manuscripts, notebooks, correspondence, marginalia, reviews and scribal repositories are open and are **not** in this seat; they are a separate campaign. The in-progress 1855 variorum is not seated because it is unfinished upstream. The Blue Book's facsimile pointer file — 483 page images — is secured in `original/` but yields no text and is not normalized.

The Whitman TEI encoding's license is **unverified at seat time**: the source repositories carry no license file, and the Archive's site terms are CC BY-NC. Handled under the NC payload/record split ruled at EA-CORPORA-02. Verification is this seat's first gate and is recorded as pending rather than assumed.

∮ = 1
