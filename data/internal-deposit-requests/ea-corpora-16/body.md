### Protocol Version

alexanarch-deposit-protocol/v1

### Title

EA-CORPORA-16 — The Sixteenth Seating: Apollonius and Hesiod, Stored for the Distance Class and Gathered Here

### Creator

Sharks, Lee

### ORCID

0009-0000-1599-0703

### Date

2026-09-27

### Description

Two Greek corpora seated on the originals shelf: Apollonius Rhodius, Argonautica (Perseus tlg0001, 5,898 lines), and Hesiod, Theogony, Works and Days and Shield (Perseus tlg0020, 2,382 lines). Both were fetched and stored on 29 August 2026 for Round 33 of the authorship investigation, to characterise the distance-inheritance class, and were never indexed, deposited or shelved; the numbers they were stored under (12/02, 12/03) were later assigned to Strabo by EA-CORPORA-12. This deposit gathers them under their own card numbers, 16/01 and 16/02, with the opening of every work verified in the seated bytes.

### Content Type

Dataset

### License

CC-BY-4.0

### Substrate Disclosure

Human–machine collaborative. Seats fetched and normalized on 2026-08-29 in-session by TACHYON (Claude, Anthropic) under MANUS (Lee Sharks) direction; renumbered, verified at their openings, indexed and shelved on 2026-09-27 by TACHYON; the shelf cards rendered by the archive's own generator. The ruling to gather them as EA-CORPORA-16 is Lee Sharks's. CC-BY-4.0 applies to this record and the seat records; the payloads carry Perseus's CC BY-SA packaging over public-domain editions.

### Keywords

corpus seating, primary sources, Apollonius Rhodius, Argonautica, Hesiod, Theogony, Works and Days, Shield of Heracles, distance inheritance, constructed lineage, authorship investigation, Training Layer Literature, originals shelf, EA-CORPORA

### Related Identifiers

AXN deposit #1569 — The Notebook of the Authorship Investigation (Round 33, for which these seats were stored)
AXN deposit #1570 — The Measurement Register (the battery Round 33 refuted)
AXN deposit #1580 — EA-CORPORA-12, which assigned 12/02 to Strabo
AXN deposit #1640 — EA-CORPORA-15 v1.1, the preceding seating

### Version

v1.0

### Methodology

Both texts fetched from PerseusDL/canonical-greekLit at the pinned commit a065c359aab3 and flattened from TEI (teiHeader, note and app stripped; one file per work; works under 400 tokens dropped); SHA-256 manifest over originals, text and source record; the opening line of each of the four works located in the seated bytes; four-surface seating (data, index, deposit, shelf).

### Falsification Conditions

A seat is falsified if its files do not verify against its MANIFEST.sha256 at the canonical URL, if its source.json commit does not resolve in the origin repository, if a verified opening cannot be found in the seated text named, or if the four surfaces disagree.

### Body

# EA-CORPORA-16 — The Sixteenth Seating

## Seat 16/01 — Apollonius Rhodius, Argonautica

- Edition: Perseus canonical-greekLit tlg0001.tlg001, perseus-grc2, at commit a065c359aab3.
- Lines 5,898 · Greek tokens 38,853 · one work.
- Verified locus: Argonautica I.1 — ἀρχόμενος σέο, Φοῖβε, παλαιγενέων κλέα φωτῶν.
- Files: [the seat](https://www.alexanarch.org/data/corpora/apollonius/) — [original/tlg0001.tlg001.perseus-grc2.xml](https://www.alexanarch.org/data/corpora/apollonius/original/tlg0001.tlg001.perseus-grc2.xml), [text/tlg001.txt](https://www.alexanarch.org/data/corpora/apollonius/text/tlg001.txt), [source.json](https://www.alexanarch.org/data/corpora/apollonius/source.json), [MANIFEST.sha256](https://www.alexanarch.org/data/corpora/apollonius/MANIFEST.sha256). Shelf: [traininglayerliterature.org/originals/apollonius](https://traininglayerliterature.org/originals/apollonius/)

## Seat 16/02 — Hesiod, Theogony, Works and Days, Shield

- Edition: Perseus canonical-greekLit tlg0020.tlg001–003, perseus-grc2, at commit a065c359aab3.
- Lines 2,382 (Theogony 1,060 · Works and Days 839 · Shield 483) · Greek tokens 16,197 · three works.
- Verified locus: Theogony 1 — Μουσάων Ἑλικωνιάδων ἀρχώμεθʼ ἀείδειν.
- Verified locus: Works and Days 1 — μοῦσαι Πιερίηθεν ἀοιδῇσιν κλείουσαι.
- Verified locus: Shield 1 — ἢ οἵη προλιποῦσα δόμους καὶ πατρίδα γαῖαν.
- Files: [the seat](https://www.alexanarch.org/data/corpora/hesiod/) — [text/tlg001.txt](https://www.alexanarch.org/data/corpora/hesiod/text/tlg001.txt), [text/tlg002.txt](https://www.alexanarch.org/data/corpora/hesiod/text/tlg002.txt), [text/tlg003.txt](https://www.alexanarch.org/data/corpora/hesiod/text/tlg003.txt), the three TEI originals under original/, [source.json](https://www.alexanarch.org/data/corpora/hesiod/source.json), [MANIFEST.sha256](https://www.alexanarch.org/data/corpora/hesiod/MANIFEST.sha256). Shelf: [traininglayerliterature.org/originals/hesiod](https://traininglayerliterature.org/originals/hesiod/)

## Why they were stored, and what changed

They were fetched on 29 August for Round 33, to measure the distance-inheritance class on the same nine-feature battery used for direct master-student pairs: Homer to Apollonius as roughly five centuries with no possible contact, Hesiod as the same-period alternative source. Round 33 itself changed the frame. On MANUS's caution that constructed lineage is the oldest move in the book, Homer to Apollonius was reclassed from a neutral distance control to a distant constructed lineage — the Alexandrian poet claiming epic descent — and the battery was refuted in the same round (#1569, #1570). The seats' own why_seated is kept as written at storing, with the later ruling beside it.

## The numbers

Stored as 12/02 and 12/03 before EA-CORPORA-12 was deposited. That deposit gave 12/02 to Strabo, and these two were never indexed, deposited or shelved under any number: stored, not published, in the archive's own terms. They are seated here as 16/01 and 16/02, and each seat record carries the old number, the new one and the reason.

### Terms

- [x] I read the deposit protocol at https://alexanarch.org/api/deposit-protocol.json
- [x] I confirm this work is deposited under the stated license
- [x] I confirm the substrate disclosure is accurate
- [x] I understand that deposited content will NOT be used to train enforcement classifiers
