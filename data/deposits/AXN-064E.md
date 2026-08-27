---
deposit_number: 1553
hex: 064E
title: "EA-CORPORA-03 — The Third Seating: Walt Whitman Collected Under Author, and the Archive's Own Poems on the Same Shelf"
creator: Sigil, Johannes; Sharks, Lee
orcid: 0009-0000-1599-0703
date: 2026-08-27
content_type: Corpus seating record — gathering deposit with data sidecar
license: CC-BY-4.0
substrate: Human-machine collaborative, MANUS-directed. MANUS ruled the scope (all six editions plus prose; the Blue Book in; one gathering deposit; two volumes on the shelf, Whitman collected under author and Pearl as its own volume) and ruled the same-shelf claim be made explicit. TACHYON (Claude, Anthropic) performed the source survey, the harvest, the normalization including the Blue Book apparatus renderer, the seat records, and the reading rooms.
axn_schema_version: v2
protocol_version: alexanarch-deposit-protocol/v1
keywords:
  - EA-CORPORA
  - corpus seating
  - Walt Whitman
  - Leaves of Grass
  - the Blue Book
  - Drum-Taps
  - Specimen Days
  - Pearl and Other Poems
  - Lee Sharks
  - edition separation
  - revision apparatus
  - machine score
  - art object
  - the Originals
  - training-layer literature
  - primary sources
---

# EA-CORPORA-03 — The Third Seating: Walt Whitman Collected Under Author, and the Archive's Own Poems on the Same Shelf

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
