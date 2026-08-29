---
deposit_number: 1560
hex: 0658
title: "EA-CORPORA-05 — The Fifth Seating: Browning, Pound, Pessoa, and the Constructed Voice at Three Stages"
creator: Sharks, Lee
orcid: 0009-0000-1599-0703
date: 2026-08-29
content_type: Corpus seating record — gathering deposit with data sidecar
license: CC-BY-4.0
substrate: AI-assisted (substrate) — seats built, verified and rendered in working session with Claude (Anthropic) under MANUS direction. Sources commit-pinned or ebook-pinned; nine declared loci verified in the seated text before the claim was written; wiki article composed before minting rather than after.
axn_schema_version: v2
protocol_version: alexanarch-deposit-protocol/v1
keywords:
  - EA-CORPORA
  - corpus seating
  - Browning
  - dramatic monologue
  - Ezra Pound
  - personae
  - Homage to Sextus Propertius
  - Fernando Pessoa
  - heteronym
  - Alberto Caeiro
  - Ricardo Reis
  - Alvaro de Campos
  - constructed voice
  - positive control
  - leave-one-out
---

# EA-CORPORA-05 — The Fifth Seating: Browning, Pound, Pessoa, and the Constructed Voice at Three Stages

## The seats

| seat | corpus | lines | language | licence |
|---|---|---|---|---|
| 05/01 | **browning** | 4,598 | English | Public domain (author d. 1889); Project Gutenb |
| 05/02 | **pound** | 7,967 | English | Public domain in the United States (all volume |
| 05/03 | **pessoa** | 20,486 | Portuguese | Public domain (author d. 1935); Wikisource tra |


Data is published as a sidecar index at [api/corpora.json](https://www.alexanarch.org/api/corpora.json) with per-seat links; each seat carries its own `source.json` and SHA-256 `MANIFEST.sha256` at `alexanarch.org/data/corpora/<corpus>/`, and a rendered reading room at `traininglayerliterature.org/originals/<corpus>/`. The per-deposit external-metadata sidecar for this record is at `/data/external-metadata/AXN-0658.json`.


EA-CORPORA-05 seats three corpora that belong together because they are one practice at three stages of its development.

Browning enters at 05/01 with Men and Women (1855). The dramatic monologue is the moment a poem's speaker becomes a position distinct from the poet — with a history, a self-justification, and blind spots the poem lets the reader see past the speaker to. Fra Lippo Lippi and Andrea del Sarto argue their own cases and lose them without the poet ever appearing to judge. The gap between what the voice says and what the poem knows is the whole technique, and it is the ancestor of everything the other two seats contain.

Pound enters at 05/02 with four volumes, all published before 1930 and so public domain in the United States. Personae names the operation in its title. Cathay makes a voice by translating one. And Homage to Sextus Propertius performs, in 1919, the manoeuvre that Ginsberg would later perform on Catullus 38: a Latin source whose form is tracked closely while its register is inverted, defended by its author as something other than translation when the philologists objected that it was a bad one. Pound is the middle term, where the mask stops being a character in a poem and becomes a position the poet inhabits.

Pessoa enters at 05/03 with the heteronymic corpus taken from Portuguese Wikisource by declared category: 123 poems of Alberto Caeiro, 60 of Ricardo Reis, 107 of Álvaro de Campos. The partition is the source's and not the seat's, because that partition is precisely the object under examination and adjusting it to suit a result would destroy the only thing the corpus is good for. Pessoa is the sole case among the three with documented ground truth — the letter to Adolfo Casais Monteiro of 13 January 1935 attributes the heteronyms, so the grouping is known rather than inferred — which makes this the positive control for any instrument claiming to detect designed differentiation.

The orthonym is deliberately not seated. Fernando Pessoa's own 496 categorised pages are held out so that a leave-one-out test remains possible: whether the structure of the remaining voices implies the position that none of them occupies. Seating him alongside would foreclose the experiment. The absence is a decision and is recorded as one.

One technical finding is worth carrying forward. The Wikisource extracts API returns empty text for the short lyrics, because their bodies sit inside poem templates it does not render, while longer prose-poems extract normally. A fetch built on extracts therefore yields Campos almost complete and Caeiro and Reis almost empty, and reports no error while doing it. The seat was built from raw wikitext instead, and the normalization field records why, so that the next attempt does not spend the discovery again.
