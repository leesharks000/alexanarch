---
deposit_number: 1559
hex: 0657
title: "EA-CORPORA-04 — The Fourth Seating: Aristotle Undivided, Plotinus as Comparandum, and the Repair of the Seating Chain"
creator: Sharks, Lee
orcid: 0009-0000-1599-0703
date: 2026-08-28
content_type: Corpus seating record — gathering deposit with data sidecar
license: CC-BY-4.0
substrate: AI-assisted (substrate) — seats built, verified and rendered in working session with Claude (Anthropic) under MANUS direction. Both upstream repositories commit-pinned; five declared loci verified in the seated text; edition artifact tested and excluded (within-Aristotle same-edition and cross-edition particle distances identical to two decimal places).
axn_schema_version: v2
protocol_version: alexanarch-deposit-protocol/v1
keywords:
  - EA-CORPORA
  - corpus seating
  - Aristotle
  - Plotinus
  - Andronicus of Rhodes
  - spuria
  - authenticity as recorded field
  - stylometry
  - particle transitions
  - splitbrain
  - shelf projection
  - seating postflight
---

# EA-CORPORA-04 — The Fourth Seating: Aristotle Undivided, Plotinus as Comparandum, and the Repair of the Seating Chain

## The seats

| seat | corpus | lines | language | licence |
|---|---|---|---|---|
| 04/01 | **aristotle** | 83,110 | Ancient Greek | CC BY-SA (First1KGreek and Perseus packaging); |
| 04/02 | **plotinus** | 20,923 | Ancient Greek | CC BY-SA (First1KGreek packaging); underlying  |


Data is published as a sidecar index at [api/corpora.json](https://www.alexanarch.org/api/corpora.json) with per-seat links; each seat carries its own `source.json` and SHA-256 `MANIFEST.sha256` at `alexanarch.org/data/corpora/<corpus>/`, and a rendered reading room at `traininglayerliterature.org/originals/<corpus>/`. The per-deposit external-metadata sidecar for this record is at `/data/external-metadata/AXN-0657.json`.


# EA-CORPORA-04 — The Fourth Seating: Aristotle Undivided, and Plotinus as the Comparandum

Two corpora, seated 28 August 2026, both in service of one question that the
archive had been arguing about in prose and could not settle without them.

## 04/01 — Aristotle

Forty-eight works, 83,110 lines, united across First1KGreek (Bekker, Oxford
1837) and Perseus canonical-greekLit, both commit-pinned, Perseus preferred for
the nine works both repositories hold.

The seat carries the genuine and the spurious **undivided**, and records the received authenticity status as a field rather than applying it as a filter. The reason is in the seat's own source.json and it is not decorative. The genuine/spurious partition of this corpus is an inference, not an attestation. Andronicus of Rhodes constituted it in the first century BCE — some 250 years after Aristotle — working, on the tradition's own account, from the cross-references the texts contain and from school documents. His catalogue is not extant. And his judgments have been overturned: he held *De interpretatione* spurious, and the field now receives it as genuine. *Metaphysics* A was contested in Alexander's time and attributed by some to Pasicles of Rhodes.

So the criteria that produced the partition are the criteria whose circularity is at issue wherever authorship is the question. Any analysis that drops the spuria to sharpen a result about Aristotle has filtered its data through a category built from the very consistency it is measuring. That error was made in this archive, against this corpus, on the day the seat was built; the note exists so it is not made twice.

Flagged individually in the seat: tlg017 *De interpretatione* (Andronicus judged spurious), tlg025 *Metaphysica* (Book A contested in antiquity), tlg022 *Magna Moralia* (disputed), tlg036 *Problemata* (largely of the school).

## 04/02 — Plotinus

The *Enneades*, six units, 20,923 lines, First1KGreek.

Seated because of a result rather than for completeness. On particle-transition profiles computed across nine Greek authors, Aristotle sits closer to Plotinus (0.0310) than to Plato (0.0852) — and closer to Plotinus than Aristotle sits to himself (within-author mean 0.1028, maximum 0.3553). Seven centuries and a dialect lie between them. Plato is likewise nearer to Philo (0.0403) and to Thucydides (0.0547) than to Aristotle, and the Plato/Aristotle pair ranks tenth of thirty-six author-pairs — which is to say, unremarkable.

On the evidence so far the feature space separates verse from prose, then register, and authorship is not visibly in the ordering. The seat exists so that finding can be re-run and contested rather than believed.

## Also recorded

The Plato seat (EA-CORPORA-01/08) was extended with the *Definitiones* (tlg037, First1KGreek), the received spurium the Perseus range lacks, and its own partition recorded the same way: genuine core, nine dubia including the Letters, one spurium. The seven lesser Thrasyllan spuria — *Axiochus*, *De justo*, *De virtute*, *Demodocus*, *Sisyphus*, *Halcyon*, *Eryxias* — have no Greek edition in either upstream repository at the pinned commits. Their absence is declared in the seat rather than closed over.

Iamblichus and Damascius are unavailable in canonical-greekLit and in First1KGreek at every pin, under any author string. This is recorded because the attempt has been made before and failed for that reason, and the next instance should not spend the search again.

## On the seating chain itself

This deposit is also the occasion of a repair. A corpus seat is finished only when four surfaces agree: the seat directory, the machine index at `data/api/corpora.json`, a seating deposit that assigns the card number, and the rendered reading room at `traininglayerliterature.org/originals/<name>/`. Until today the fourth was produced by hand and no generator existed in either repository. It drifted, as hand-maintained projections do: these two corpora were seated, indexed, and never reached the shelf. The index had drifted further still, listing seventeen of thirty-nine seats.

`scripts/build_originals_shelf.py` now renders the card from the seat's own file tree, and `scripts/seat_corpus_postflight.py` runs the chain and fails if any surface disagrees. The archive's standing rule governs: a corpus that exists only inside a data directory is not published, it is stored.

∮ = 1
