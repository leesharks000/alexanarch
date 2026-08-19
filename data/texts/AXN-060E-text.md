---
deposit_number: 1499
hex: 060E
title: "EA-CORPORA-01 · Seat 01: Flavius Josephus — The Canonical Greek Corpus, Commit-Pinned, Normalized, Collation-Gated"
creator: Sharks, Lee
date: 2026-08-19
content_type: Corpus seating
license: "Texts: public-domain edition via Perseus (CC BY-SA packaging); this record CC-BY-4.0"
substrate: Seating executed by TACHYON (Claude substrate) per EA-OMEGA-BUILD-01 under MANUS direction; the collation gate is automated and its assertions halted the build until passed.
axn_schema_version: v2
protocol_version: ""
keywords:
  - EA-CORPORA-01
  - corpus seating
  - Josephus
  - Niese
  - Perseus
  - canonical-greekLit
  - commit pin
  - SHA-256 manifest
  - collation gate
  - primary texts
  - parsable corpus
---

# EA-CORPORA-01 · Seat 01: Flavius Josephus — The Canonical Greek Corpus, Commit-Pinned, Normalized, Collation-Gated

Seat 01 places canonical Josephus at data/corpora/josephus/ in three layers: original/ holds the four Perseus grc2 XML files exactly as fetched from PerseusDL/canonical-greekLit at commit df40bf093ec67fe3f05d3049c36af5509d2d71cb; text/ holds the normalized layer, one file per work, flat lines of the form "AJ 11.236<TAB>...", teiHeader stripped and argument divisions excluded, 12,423 referenced sections in all; source.json and MANIFEST.sha256 bind origin, edition (Niese, 1885–1895), license, normalization rule, and checksums over every file. The collation gate verified, before any commit, that the seated text carries the exact readings on which the program's Josephus results stand: the queen's speechless fall at Antiquities 11.236, the re-fired eros at Bellum 1.444, and Saul's voice lost at Antiquities 6.337. What the program tested and what the archive now hosts are certified to be the same letters. Further seats follow the work plan; projections to the reading sites carry copies of the text layer with source and manifest, citing this record as the canonical mint.
