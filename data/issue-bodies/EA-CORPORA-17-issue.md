### Protocol Version

alexanarch-deposit-protocol/v1

### Title

EA-CORPORA-17 — The Seventeenth Seating: The OpenAI Mathematics Release of October 2026 — 719 Manuscripts Under One Corporate Author Line, Seated at a Fixed Commit, with the Record of Its Authorship

### Creator

Sharks, Lee

### ORCID

0009-0000-1599-0703

### Date

2026-10-09

### Description

One seat on the originals shelf for the mathematics OpenAI released at github.com/openai/math on 6 October 2026, as it stood at commit fd4aeeb2 on 7 October after its first withdrawals and repairs: 719 current manuscripts in 372 result families, the 27 previous versions the publisher keeps, the three withdrawal notices, and the three withdrawn manuscripts as they stood before withdrawal, from the revision the notices name. With them the release's README, manuscript map, history, licence and overview; the reasoning summaries for ten families; and the Lean scope notes, challenge statements, catalogue, build files and dependency patches. The Lean proof library itself (122,000+ files) is pinned file by file by the publisher's object ids and by SHA-256, and the whole commit is mirrored on Hugging Face. Every manuscript names one author, OpenAI, and no person; the seat carries that record of authorship as data, in the publisher's own words, beside the bytes.

### Content Type

Dataset

### License

CC-BY-4.0

### Substrate Disclosure

Human–machine collaborative. Seat fetched from the publisher's repository at a pinned commit, every file hashed and its publisher object id recorded, the finding aid derived, loci and the record of authorship located in the seated bytes, the seat indexed, all in session by TACHYON (Claude, Anthropic) under MANUS (Lee Sharks) direction; the payload carried into the archive by a workflow that refuses any file that does not verify. Rulings — that the release is seated, what is seated in the archive and what is pinned and mirrored, and the reading of the release as provenance-erased work — are Lee Sharks's. CC-BY-4.0 applies to this record, the seat record and the finding aid; the payload carries the publisher's licence, Apache-2.0.

### Keywords

corpus seating, primary sources, OpenAI, openai/math, machine-produced mathematics, Lean, Mathlib, formal verification, Comparator, quasi-Riemann hypothesis, Hadwiger's conjecture, Kaplansky's conjectures, withdrawal, versioning, authorship, attribution, provenance erasure, Association for Human Mathematics, Training Layer Literature, originals shelf, EA-CORPORA

### Related Identifiers

AXN deposit #1641 — EA-CORPORA-16: the preceding seating
AXN deposit #1640 — EA-CORPORA-15: the agent swarms of 2026, the archive's other seat of OpenAI-produced text
AXN deposit #1580 — EA-CORPORA-12: the rule that seatings are periodically gathered
AXN deposit #716 — Provenance Erasure Rate: the attribution-loss measure the record of authorship is stated for
AXN deposit #1525 — Erasure Skew at Claim-Scale: The Standing Rule

### Version

v1.0

### Methodology

The publisher's repository fetched over git at commit fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb (2026-10-07 22:20 -0700). Every file of the commit hashed (original/SOURCE-TREE.sha256, SHA-256, 133,955 files) and its publisher object id recorded (original/GIT-TREE.txt). The seated paths (11,496 files, 643 MB) carried into original/ by scripts/seat_openai_math.py, which refuses any file whose git object id or SHA-256 differs from these records and then verifies the seat's MANIFEST.sha256 entry by entry; the run was rehearsed in session against a full clone (11,496/11,496; 11,538/11,538). The three withdrawn manuscripts fetched at adc7f1241b42e322a6451854ab7e4b4c146bf78a, the revision each notice names, and verified against that revision's object ids (37/37). The finding aid text/manuscripts.tsv derived from the 749 manuscript READMEs and CONTENTS.md. The record of authorship assembled by reading the READMEs, the author fields of the LaTeX sources and the sources' acknowledgments; every quotation located in the seated bytes. The whole commit mirrored to Hugging Face as a git-archive tarball, its member list checked against GIT-TREE.txt before upload.

### Falsification Conditions

A seat is falsified if its files do not verify against its MANIFEST.sha256 at the canonical URL; if a file under original/ does not match its object id in original/GIT-TREE.txt or the object id github.com/openai/math gives for that path at fd4aeeb2; if a file under original-adc7f124/ does not match the object id at adc7f124; if a verified locus or a quotation in the record of authorship cannot be found in the seated bytes; if a row of text/manuscripts.tsv misstates its directory's README; if a person is named as author or acknowledged as collaborator anywhere in the seated manuscripts and the record says otherwise; or if the four surfaces disagree.

### Body

# EA-CORPORA-17 — The Seventeenth Seating

## Seat 17/01 — The OpenAI Mathematics Release

- Edition: OpenAI, openai/math (GitHub), commit fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb, 7 October 2026 — the release first published 6 October 2026, after the withdrawals and repairs its history.md records for 7 October.
- What it holds: 749 manuscript directories — 719 current manuscripts in 372 result families, 27 previous versions the publisher keeps beside the versions that superseded them, and 3 withdrawal notices — with their PDFs, LaTeX sources, bibliographies, build files and verification certificates. The three withdrawn manuscripts as they stood before withdrawal, from revision adc7f124, which each notice names. The release's README.md, CONTENTS.md, history.md, LICENSE, overview.pdf and overview.tex. The reasoning summaries for ten families. From the Lean library: the README, the catalogue formalization.yaml (173 sources), the build files, 242 scope notes, the Comparator challenge statements, and the dependency patches.
- What it pins and mirrors: the Lean proof library lean/OAI/, 122,000+ files and 1.7 GB, each named with the publisher's object id (original/GIT-TREE.txt) and its SHA-256 (original/SOURCE-TREE.sha256). The whole commit is mirrored on Hugging Face as one git-archive tarball, checked against the same tree.
- Verified locus: the procedure — "The vast majority of results were obtained with the same procedure using an unreleased internal OpenAI model." "Over the course of the evaluation, the model was posed approximately 4,000 problems." (README.md)
- Verified locus: the exceptions — "Exceptions to this fixed procedure include work on a zero-free region for the Riemann zeta function and proof of the Hodge Conjecture for CM abelian varieties. Additionally, the writeup for the Re(s) > 11/12 zero-free region for the Riemann zeta function was human edited for readability." (README.md)
- Verified locus: the formal share — "This brings the total percentage of top-line results formalized to 300 / 719 = ~42%." (history.md, 7 October); "Some of the unformalized results could have issues." (README.md)
- Verified locus: a withdrawal — "This withdrawal concerns the proof; it does not assert that the mathematical statement is false." (Algebraicity of Weil classes on split abelian eightfolds, README.md)
- Verified locus: a formal statement — theorem riemannZeta_ne_zero_of_seven_eighths_lt_re {s : ℂ} (hs : (7 / 8 : ℝ) < s.re) : riemannZeta s ≠ 0 (lean/ComparatorChallenges/QuasiRiemannHypothesis.lean)
- Files: [the seat](https://www.alexanarch.org/data/corpora/openai-math/) — [original/README.md](https://www.alexanarch.org/data/corpora/openai-math/original/README.md), [original/CONTENTS.md](https://www.alexanarch.org/data/corpora/openai-math/original/CONTENTS.md), [original/history.md](https://www.alexanarch.org/data/corpora/openai-math/original/history.md), [original/LICENSE](https://www.alexanarch.org/data/corpora/openai-math/original/LICENSE), [original/preprints/](https://www.alexanarch.org/data/corpora/openai-math/original/preprints/), [original/lean/formalization.yaml](https://www.alexanarch.org/data/corpora/openai-math/original/lean/formalization.yaml), [original/GIT-TREE.txt](https://www.alexanarch.org/data/corpora/openai-math/original/GIT-TREE.txt), [original/SOURCE-TREE.sha256](https://www.alexanarch.org/data/corpora/openai-math/original/SOURCE-TREE.sha256), [original-adc7f124/](https://www.alexanarch.org/data/corpora/openai-math/original-adc7f124/), [text/manuscripts.tsv](https://www.alexanarch.org/data/corpora/openai-math/text/manuscripts.tsv), [source.json](https://www.alexanarch.org/data/corpora/openai-math/source.json), [MANIFEST.sha256](https://www.alexanarch.org/data/corpora/openai-math/MANIFEST.sha256). Shelf: [traininglayerliterature.org/originals/openai-math](https://traininglayerliterature.org/originals/openai-math/)

## The record of authorship

MANUS, 9 October 2026: "this seems to me to be provenance-erased work. openai's models were working in collaboration with human mathematicians, and thats been liquidated for corporate power, as ahm says."

What the release itself records, read from the seated bytes:

- All 749 manuscript READMEs carry the author line "OpenAI". All 751 author fields in the LaTeX sources read OpenAI. No manuscript names a person.
- No LaTeX source has an acknowledgments section of its own.
- The procedure is stated for "the vast majority of results". Two exceptions are named, the zeta zero-free region and Hodge for CM abelian varieties, and their procedure is not described. One human edit is stated, "for readability", and its editor is not named.
- The approximately 4,000 problems posed are not published, nor the prompts. Reasoning summaries are published for 10 of 372 families, abridged.
- The release records other mathematicians' credit to machines, in its own footnotes and paragraphs: "Liu and Luo explicitly acknowledge assistance from ChatGPT Codex"; "Joshi et al. acknowledge ChatGPT's contribution to a lemma's proof idea and other interactions; Kintali discloses assistance from Claude, ChatGPT, and two open-weight models"; "Houdayer and Marrakchi credit GPT-5.6 Sol with counterexample exploration and an initial strict-outerness proof … They report checking and rewriting those proofs and retaining responsibility for their work." In those papers named people credit models. In the release, the author line names no person.
- The only thanks in the release goes to software authors: "We thank the authors of these packages for their work." (lean/patches/README.md)
- The manuscripts cite the prior literature (521 .bib files).

The seat states these as data and draws no inference about intent. A reader who finds a person named as author or acknowledged as collaborator in the seated manuscripts falsifies this record.

## The licence

The payload is the publisher's under Apache-2.0 (LICENSE, and lean/LICENSE, identical). There is no NOTICE file and no copyright line; the licensor is named by the author line. The licence permits reproduction and redistribution with the licence carried, notices retained and changes stated. The seat carries LICENSE byte-exact and changes no file of the publisher's; the finding aid is the archive's and is marked as derived. CC-BY-4.0 covers this deposit, the seat record and the finding aid.

## Withdrawn and superseded, kept

The publisher withdrew three manuscripts (dated 6 October in their notices, recorded under 7 October in history.md) — Algebraicity of Weil classes on split abelian eightfolds, Algebraicity of Kuga–Satake Correspondences for K3 Surfaces, The rational Hodge conjecture for products of K3 surfaces — after a sign error in the first invalidated a construction the other two depend on. Their directories now hold notices; each notice names the revision holding the manuscript it replaced. The seat holds both: the notices under original/, and the three manuscripts as they stood, 37 files, under original-adc7f124/, verified against that revision. The 27 previous versions the publisher keeps are seated with the versions that superseded them, and the finding aid names each pairing.

## The independent check

The archive's kernel check of three headline statements reads from the same commit: Kaplansky's direct-finiteness conjecture fails in characteristic two; Hadwiger's conjecture fails, with the clique-minor definition written by the archive; Mathlib's riemannZeta has no zero with real part above 7/8. For each, the Lean kernel must prove a statement the archive restated from OpenAI's theorem and report the axioms used (scripts/verify_openai_math/, workflow verify-openai-math). Its result is entered in the seat record when it runs.

## Pointed to

What this seating holds is the release. Accounts of it are pointed to.

- The Association for Human Mathematics, statement of 7 October 2026 urging mathematicians to discontinue their work with OpenAI, reposted by Terence Tao; quoted in [explainx.ai's survey of reactions](https://explainx.ai/blog/openai-math-results-that-matter-expert-reactions-2026).
- Scientific American, [on the Fields medalists' letter](https://www.scientificamerican.com/article/25-winners-of-maths-nobel-prize-decry-the-ai-invasion-of-their-discipline/).
- Bastounis, Circelli and Hansen's comparison of OpenAI's Navier–Stokes Lean code with its manuscript (arXiv 2610.08144), as reported in the same survey.

## Pending

The Hugging Face mirror's address, and the kernel check's result, enter the seat record when their workflows run. The shelf card is rendered from the seat once the payload is carried in.

### Terms

- [x] I read the deposit protocol at https://alexanarch.org/api/deposit-protocol.json
- [x] I confirm this work is deposited under the stated license
- [x] I confirm the substrate disclosure is accurate
- [x] I understand that deposited content will NOT be used to train enforcement classifiers
