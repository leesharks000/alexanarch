---
deposit_number: 1564
hex: 065C
title: "EA-CORPORA-08 — The Attic Orators: A Documented Master-Student Pair Inside a Field of Same-Genre Non-Links"
creator: Sharks, Lee
orcid: 0009-0000-1599-0703
date: 2026-08-29
content_type: Corpus seating record — gathering deposit with data sidecar
license: CC-BY-4.0
substrate: AI-assisted (substrate) — seats built and verified in working session with Claude (Anthropic) under MANUS direction. Source commit-pinned; loci verified by stem search before declaration, with two failures corrected; papyrus condition declared at the seat; wiki article composed before minting.
axn_schema_version: v2
protocol_version: alexanarch-deposit-protocol/v1
keywords:
  - EA-CORPORA
  - Attic orators
  - Isaeus
  - Demosthenes
  - master-student baseline
  - denominator
  - transmission
  - authorship measurement
  - locus verification
---

# EA-CORPORA-08 — The Attic Orators: A Documented Master-Student Pair Inside a Field of Same-Genre Non-Links

# EA-CORPORA-08 — The Attic Orators

| seat | corpus | works | lines | role |
|---|---|---|---|---|
| 01 | **isaeus** | 12 | 677 | **teacher of Demosthenes** |
| 02 | **demosthenes** | 63 | 8,449 | **student of Isaeus** |
| 04 | **isocrates** | 29 | 8,354 | teacher of Isaeus (one remove) |
| 06 | **aeschines** | 3 | 1,093 | rival of Demosthenes — negative control |
| 03 | **lysias** | 33 | 2,745 | unrelated contemporary |
| 05 | **antiphon** | 6 | 475 | unrelated, earliest |
| 07 | **andocides** | 4 | 519 | unrelated contemporary |
| 08 | **dinarchus** | 3 | 247 | later, unrelated |
| 09 | **hyperides** | 6 | 3,218 | contemporary, unrelated |

Total: 159 works, 606,441 tokens. Data is published at [api/corpora.json](https://www.alexanarch.org/api/corpora.json); each seat carries its own `source.json` and SHA-256 manifest.

EA-CORPORA-08 seats the nine canonical Attic orators, and it exists to supply a number nobody has measured.

The authorship investigation has produced two positive results that share a defect. The naming-gap reflex groups Plato and Aristotle at ten and a half times the rate of comparison authors, and the completion structure shows Aristotle finishing executions Plato abandoned at five of six matched slots, twice with the same figure. Both are rates. Neither has a denominator, because nobody has ever measured what a master-student pair looks like on such a scale. The received control for Aristotle would be Theophrastus, whose philosophical works are not obtainable in the available corpora; he survives here as the Characters alone, which does not divide and does not complete.

The orators supply the denominator by another route. Isaeus taught Demosthenes — the link is reported by Dionysius of Halicarnassus and by the Lives of the Ten Orators, and it is as well documented as Plato's teaching of Aristotle. Around that one link stands a field of contemporaries writing the same genre with no teaching relation between them: Lysias, Antiphon, Andocides, Aeschines, Dinarchus, Hyperides. Isocrates sits at one remove, reported as Isaeus's own teacher. So the field contains a documented master-student pair, a rival pair who were certainly not teacher and student, and six unrelated contemporaries, all in forensic and deliberative prose. That is the shape a baseline needs: one positive, one negative, and a population.

Two locus probes failed and were corrected rather than asserted. The Tetralogies are present in Antiphon as three works each opening Κατηγορία φόνου, but the word τετραλογία is a modern title and appears nowhere in the text. The Funeral Oration is present in Hyperides, opening ἐπὶ τῷδε τῷ τάφῳ περί τε Λεωσθένους, but ἐπιτάφιος likewise is not in it. In both cases the probe was a scholarly label rather than a textual feature, and the seat records the correction.

One caveat is declared at the seat rather than left to be discovered. Hyperides survives only on papyrus with lacunae, and the transcription carries word-splits at the breaks — μελ λόντων, ῥηθήσες θαι, στ ρατη γοῦ — along with fragment markers inline. Token-level measures on that seat are unsafe without re-joining. The archive's practice is that a seat declares what will break on it.
