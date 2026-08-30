---
deposit_number: 1565
hex: 065D
title: "EA-CORPORA-09/10/11 — Three Seatings Against the Control Problem: Theophrastus, Aquinas, and the Full Pessoan Range"
creator: Sharks, Lee
orcid: 0009-0000-1599-0703
date: 2026-08-29
content_type: Corpus seating record — gathering deposit with three data sidecars
license: CC-BY-4.0
substrate: AI-assisted (substrate) — seats built and verified in working session with Claude (Anthropic) under MANUS direction. Sources commit-pinned or site-identified; loci verified by stem search before declaration except where noted; OCR quality gated and declared per seat.
axn_schema_version: v2
protocol_version: alexanarch-deposit-protocol/v1
keywords:
  - EA-CORPORA
  - Theophrastus
  - Thomas Aquinas
  - Fernando Pessoa
  - heteronymy
  - master-student control
  - external attestation
  - corpus seating
  - locus verification
---

# EA-CORPORA-09/10/11 — Three Seatings Against the Control Problem: Theophrastus, Aquinas, and the Full Pessoan Range

# Three Seatings Against the Control Problem

| seat | corpus | works | tokens | role |
|---|---|---|---|---|
| 09/01 | **theophrastus** | 15 | 208,324 | Aristotle's successor — comparandum, NOT a control |
| 10/01 | **aquinas** | 22 | 6,698,317 | externally secured master-student succession |
| 11/01 | **pessoa-full** | 25 positions | 1,254,436 | documented one-maker, many-position system |

Data is published at [api/corpora.json](https://www.alexanarch.org/api/corpora.json); each seat carries its own `source.json` and SHA-256 manifest.

**Theophrastus was recorded as unavailable three times in one session, and the record was wrong.** The claim was that he survives only as the *Characters*, which does not divide and so gives the naming-gap measure no opportunity to fire. That was an assumption, never tested: First1KGreek was checked out on the same machine throughout and contains *Historia Plantarum*, *De causis plantarum*, *De sensibus*, *De igne* and the *Metaphysica*. Once seated, he carries the reflex — nine instances in *Historia Plantarum* alone, at a division rate of 29.9 per 10,000. The result is nonetheless void as a control result: Theophrastus is defined by his relation to Aristotle, writes continuations of the abandoned Aristotelian programme, and the two corpora reach us through a single transmission channel, so his agreement cannot be independent evidence. He is a comparandum. The seat records this rather than the number alone.

**Aquinas is the first figure admissible under the criterion the archive had already written down.** A control must be impossible to place inside the configuration under test, which requires attestation from outside it — and Thomas is secured by canonization proceedings, university registers, papal bulls and Dominican chapter records, none of which has any relation to textual style, doctrinal similarity, or a succession tradition. No Greek candidate met that: Theophrastus fails it, Xenophon and Aristophanes are held apart as candidates, and the Attic orators fail on opportunity, dividing at a median of 0.5 per 10,000 where the measure needs an order of magnitude more. The seat is split three ways rather than two, because a locus probe returning zero for "metaphysic" in a file labelled *In Metaphysicam* exposed that the initial prefix table had mislabelled every commentary — the file was *Sentencia super Meteora*, and what had been labelled *De sensu* was *In Psalmos*. Rebuilt from each text's own header, the split separates independent works from Aristotle commentaries from commentaries on other objects, and that third category turns out to be the control the design lacked: the naming-gap reflex runs 3.47 times higher where Thomas glosses Aristotle and five times lower where he glosses Scripture and Dionysius. The reflex arrives with the source text, not with the man.

**The Pessoan seat existed and was too thin to answer anything.** Four voices, 111,449 tokens, with Ricardo Reis at 5,548 — a figure that cannot fill a six-part apparatus whatever Pessoa did, so any null would have measured the seat. Arquivo Pessoa lists 39 authorial positions and 4,529 texts; 2,220 were fetched and 25 positions seated. Bernardo Soares, absent entirely, is now 139,455 tokens; Reis is 42,955; Alexander Search and António Mora are new. The orthonym is at 2,810 of 2,814. Seven signature loci were verified before seating, each by the vocabulary that identifies its voice — *pastor* and *rebanho* for Caeiro, *Lídia* and *Neera* for Reis, *Douradores* and *Vasques* for Soares.

**Two defects are declared rather than repaired silently.** The Aquinas mislabelling is recorded in the seat's locus field, including which files were wrong and how the error surfaced. The Theophrastus seat was built earlier the same day with its verified-loci field empty — declared without verification — and was verified only retroactively; the note says so.
