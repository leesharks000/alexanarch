---
deposit_number: 1673
hex: 06EF
title: "EA-CORPORA-17 — The Seventeenth Seating: The OpenAI Mathematics Release of October 2026 — 719 Manuscripts Under One Corporate Author Line, Seated at a Fixed Commit, with the Record of Its Authorship (v1.1 — the corporate tag)"
creator: Sharks, Lee
orcid: 0009-0000-1599-0703
date: 2026-10-09
content_type: Dataset
license: CC-BY-4.0
substrate: Human–machine collaborative. Seat fetched from the publisher's repository at a pinned commit, every file hashed and its publisher object id recorded, the finding aid derived, loci and the record of authorship located in the seated bytes, the seat indexed, all in session by TACHYON (Claude, Anthropic) under MANUS (Lee Sharks) direction; the payload carried into the archive by a workflow that refuses any file that does not verify. Rulings — that the release is seated, what is seated in the archive and what is pinned and mirrored, and the reading of the release as provenance-erased work — are Lee Sharks's. CC-BY-4.0 applies to this record, the seat record and the finding aid; the payload carries the publisher's licence, Apache-2.0.
version: v1.1
related_ids: "AXN deposit #1672 — EA-CORPORA-17 v1.0, superseded by this record\nAXN deposit #1641 — EA-CORPORA-16: the preceding seating\nAXN deposit #1640 — EA-CORPORA-15: the agent swarms of 2026, the archive's other seat of OpenAI-produced text\nAXN deposit #1580 — EA-CORPORA-12: the rule that seatings are periodically gathered\nAXN deposit #716 — Provenance Erasure Rate: the attribution-loss measure the record of authorship is stated for\nAXN deposit #1525 — Erasure Skew at Claim-Scale: The Standing Rule"
axn_schema_version: v2
protocol_version: alexanarch-deposit-protocol/v1
keywords:
  - corpus seating
  - primary sources
  - OpenAI
  - openai/math
  - machine-produced mathematics
  - Lean
  - Mathlib
  - formal verification
  - Comparator
  - quasi-Riemann hypothesis
  - Hadwiger's conjecture
  - Kaplansky's conjectures
  - withdrawal
  - versioning
  - authorship
  - attribution
  - provenance erasure
  - Association for Human Mathematics
  - Training Layer Literature
  - originals shelf
  - EA-CORPORA
---

# EA-CORPORA-17 — The Seventeenth Seating: The OpenAI Mathematics Release of October 2026 — 719 Manuscripts Under One Corporate Author Line, Seated at a Fixed Commit, with the Record of Its Authorship (v1.1 — the corporate tag)

# EA-CORPORA-17 — The Seventeenth Seating

*v1.1 supersedes #1672 (v1.0). MANUS, 9 October 2026, the same evening: "its not just that somewhere along the way human mathematicians probably participated in the process. even if it was genuinely autonomous selection and solution, collapsing the provenance into just the corporate tag would still be problematic". v1.1 adds that ruling and two items to the record of authorship — the unnamed producing system, and the version standard the release applies to other papers — each located in the seated bytes. The seat, its files and its card number are unchanged; v1.0 remains the valid name of the bytes it holds.*

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

MANUS, the same evening: "its not just that somewhere along the way human mathematicians probably participated in the process. even if it was genuinely autonomous selection and solution, collapsing the provenance into just the corporate tag would still be problematic".

What the release itself records, read from the seated bytes:

- All 749 manuscript READMEs carry the author line "OpenAI". All 751 author fields in the LaTeX sources read OpenAI. No manuscript names a person.
- No LaTeX source has an acknowledgments section of its own.
- The producing system is unnamed. The README names it only as "an internal OpenAI model" and "an unreleased internal OpenAI model", and measures the effort in "three hours of ChatGPT Pro thinking compute with that model". No model name, version or configuration appears in the README, the history, the overview source or the reasoning summaries' LaTeX source.
- The procedure is stated for "the vast majority of results". Two exceptions are named, the zeta zero-free region and Hodge for CM abelian varieties, and their procedure is not described. One human edit is stated, "for readability", and its editor is not named.
- The approximately 4,000 problems posed are not published, nor the prompts. Reasoning summaries are published for 10 of 372 families, abridged.
- The release records other mathematicians' credit to machines, in its own footnotes and paragraphs: "Liu and Luo explicitly acknowledge assistance from ChatGPT Codex"; "Joshi et al. acknowledge ChatGPT's contribution to a lemma's proof idea and other interactions; Kintali discloses assistance from Claude, ChatGPT, and two open-weight models"; "Houdayer and Marrakchi credit GPT-5.6 Sol with counterexample exploration and an initial strict-outerness proof … They report checking and rewriting those proofs and retaining responsibility for their work." In those papers named people credit models. In the release, the author line names no person.
- The release holds those papers to a standard of provenance its own byline does not meet. Of Liu and Luo: "their declaration does not identify an underlying model version". Of Joshi et al. and Kintali: "Neither source specifies model versions." Where a paper names its models, the release repeats the names (GPT-5.6 Sol, GPT-6 Astra). Its own author line names no model and no person.
- The only thanks in the release goes to software authors: "We thank the authors of these packages for their work." (lean/patches/README.md)
- The manuscripts cite the prior literature (521 .bib files).

What the corporate tag stands in for, then, is the producing system, the selection of problems, the intermediate work, the people, and the decision of what counted as a result. The seat states these as data and draws no inference about intent. A reader who finds a person named as author or acknowledged as collaborator in the seated manuscripts falsifies this record.

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
