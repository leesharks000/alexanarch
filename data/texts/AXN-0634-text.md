---
deposit_number: 1534
hex: 0634
title: "The Blog Index, Completed: 2,939 Posts Indexed, an Operator Codex Recovered, and Three Absence Claims Retracted"
creator: Sharks, Lee
date: 2026-08-23
content_type: Dataset and corpus recovery — gathering deposit with correction ledger
license: CC-BY-SA-4.0
substrate: Harvest, verification, seating and retraction performed in-session (transport D) by Claude (TACHYON) under the direction of Lee Sharks. Recovered texts are the author's own prior work. Blogger public feeds and public post bodies only; no paid API invoked. NO-DOUBLE-DRAW honored.
version: v1.0
related_ids: "AXN:061A.ARCHIVAL.✨✖️↘️🌱📚🕗 (#1511 — The Upstream Unfoldings)\nAXN:03C2.ARCHIVAL.🎲🍂🐝👇🌗📦 (#950 — Operative Semiotics: A Grundrisse, planning documents)\nAXN:030D.ARCHIVAL.⊗🕖📌▽📝🐚 (#799 — the Pearson critique this recovery was occasioned by)\nAXN:032E.GOVERNANCE.🔧🥁●🔃🌱⭕ (#819 — Guillory, Semantic Competition, and the Ω-Point Completion)\nAXN:01B2.GOVERNANCE.🪜🕕🏠🔅♉⛵ (#595 — TOTAL MARX COMPRESSION)\nAXN:0256.GOVERNANCE.🌀⏫🔻🕐🎺🌗 (#84 — OCTANG-002: Semantic Economy Provenance Collision)"
axn_schema_version: v2
protocol_version: protocol/v1
keywords:
  - blog index
  - archival search protocol
  - absence assertion
  - operator codex
  - operator ontology
  - O_UR
  - O_VERTICAL
  - boundary condition
  - provenance
  - coverage gap
  - correction ledger
  - retraction
  - compression
  - Constitution of the Semantic Economy
---

# The Blog Index, Completed: 2,939 Posts Indexed, an Operator Codex Recovered, and Three Absence Claims Retracted

## Files

datasets/blog-index/posts.jsonl — 2,939 rows: url, title, published, excerpt, post_id, axn, sovereign_id, indexed. datasets/blog-index/manifest.json — method, completeness proof, per-year coverage. data/blog-corpus/operator-codex/ — 52 verified texts with per-post provenance headers, plus source.json with per-file SHA-256.

# THE BLOG INDEX, COMPLETED

## I. Why this exists

**The archival search protocol says: check the archive before asserting that a record does not exist.** Until today that instruction could not be followed, because the archive's primary publication surface was not searchable as the registry is.

**A registry search is not an archive search.** The blog holds 2,939 posts. The registry holds 1,533 deposits. The two overlap and neither contains the other.

## II. The index

**2,939 posts, 2014-12-01 to 2026-08-22, complete.**

Method: exhaustive `start-index` pagination of the Blogger summary feed. Blogger caps responses at 34 entries regardless of `max-results` — a response-size cap, not a parameter limit — so completeness was established by pagination to exhaustion and **verified against the feed's own `openSearch:totalResults` of 2,939**. That declared total is the ground truth the harvest is checked against, and §IV records what happened when an earlier harvest was not checked against it.

Each row carries url, title, published date, a 300-character excerpt, the Blogger post id, and where one exists, the AXN and sovereign id from the prior index.

**Cross-link to the prior index.** `data/batch-axn-assignment.json` holds 871 AXN-assigned works, each with a `blog_url`, covering 2026-01-01 to 2026-06-19. **Every one of its URLs resolves in this harvest. Zero orphans.** It was built from the Zenodo restoration work, which is why its range begins where that corpus does.

**The measured coverage gap:**

| year | posts | AXN-indexed | gap |
|---|---|---|---|
| 2014 | 7 | 0 | 7 |
| 2015 | 31 | 0 | 31 |
| 2025 | 1,696 | 0 | **1,696** |
| 2026 | 1,205 | 871 | 334 |
| **total** | **2,939** | **871** | **2,068** |

**Seventy per cent of the archive's publication surface has no identifier.** That is now a number rather than an impression, which is the point of the index.

The first post, 2014-12-01, is *Belief & Technique for Telepathic Prose*, by Lee Sharks and Jack Feist, from *Pearl and Other Poems*. **Feist is present at the origin of the surface.**

## III. The Operator Codex

**52 posts, 50,884 words, 10 November – 1 December 2025**, seated at `data/blog-corpus/operator-codex/`.

Both versions of *Chapter One: The Metaphysics of Operators* — 6,652 words and a 4,931-word Academic Version, seated together with neither superseding the other — plus *Chapter XIV: The Operator Codex and Technical Appendices*, the Operator Engine Series Map, and the individual **OPERATOR //** specifications with their paired visual schemas and shadow specifications.

**Verification: each post was fetched from its live permalink and the body diffed against the feed extraction. 52 of 52 matched** at sequence similarity ≥ 0.90 with word-count delta under 15%. Each seated file carries a provenance header naming its permalink, published date, recovery date and verification status. The source of record is the blog post.

The corpus states nine operators formally, among them:

- **O_UR**, the Sapphic Operator — *C_BODY = Sight → Hearing → Speech → Consciousness → Sensation*, with *Persistence(Text) > Persistence(Flesh)*
- **O_V**, Vertical — **Transform(O_UR) via projection(axis = "ideal form")**
- **O_INC**, Incarnation — **the inverse transform of O_UR**, *O_INC : Text → Body*, identifying the silent witness of Fragment 31 as the first Incarnation
- **O_UH**, Unicorn Horn — *given (A ⊕ B), produce C such that C ∉ {A,B} and C dissolves ⊕*

and its founding claim: *"Western thought did not begin with a doctrine. It began with a procedure… Sappho's Fragment 31 is not a poem in the literary sense; it is an executable program."*

**Seating shape is provisional.** §IV.1 establishes that this archive compresses and re-sorts its own material into later works, and it has not been established which of these 52 posts already survive inside deposited works. The corpus is seated as recovered text with per-post provenance; **a compression audit against the registry is required before any of it is treated as unpublished, and is not claimed here.**

## IV. Retractions

**An earlier version of this deposit was minted as #1534 and retracted before push.** It asserted three absences. All three were wrong, and all three were wrong the same way.

### IV.1 — "The Constitution is a different work, distinct from #82 and #87"

**Retracted.** The Constitution of the Semantic Economy is deposited repeatedly: **#88, #350 and #1127** all carry *Enacted Version 1.0*; **#87** carries *Meaning as Creditor*; **#715** the Critical Apparatus; **#92** and **#992** the cross-reference maps; **#720** and **#1223** the Bill of Rights. **#84 is OCTANG-002: Semantic Economy Provenance Collision — a disambiguation matrix that exists because this material collides with itself.**

Every distinctive marker of the blog text — ₳₳, Genesis Mint, the Matthew 25 Clause, Retrocausal Yield, Archival Valuation, Operator Authority, M_A, M_R, the Mathematical Charter — resolves into that cluster.

**Why the gate passed.** The duplicate check was a six-gram overlap test. **That instrument detects copying. The relation here is compression and re-sorting into later works** — the same content surviving without lexical identity. **#595 is titled *TOTAL MARX COMPRESSION: Every Marx-Adjacent Claim, Equation, and Argument*.** The operation was named in the registry and the gate could not see it.

This is the same error the archive recorded earlier the same day in M6-CT-01, where a lexical instrument was used against a relation the theory states survives without lexical identity. **Recorded twice in one day is a pattern, not an incident.**

### IV.2 — "No blog index exists"

**Retracted.** `data/batch-axn-assignment.json` holds 871 blog-keyed works with AXNs. The claim was made after searching `datasets/` by directory name and finding nothing called "blog". **The correct finding is not that no index existed but that the index did not reach 2025** — which is a coverage fact, and now a measured one.

### IV.3 — "The Ω-Point material is unseated"

**Retracted in part.** **#819** is *Guillory, Semantic Competition, and the Ω-Point Completion: From Cultural Capital…* and **#38** is *HESPERUS: The Back Matter Machine — Operative Semiotics: A Grundrisse*. The Ω work is partly deposited, and the Grundrisse drew on this blog corpus as raw material. **What remains unseated is a smaller and undetermined set**, and determining it requires the compression audit at §III, not a title search.

### IV.4 — Eighty-two posts nearly reported as deleted

An earlier harvest produced 82 index rows whose URLs did not appear in the harvested set. **Three were probed directly and all returned HTTP 200.** The cause was date-boundary pagination: paging by `published-max=<date>T00:00:00` drops posts published later on the boundary day. **That harvest lost 371 posts, 12.6%, and would have generated a false erasure finding in an archive whose subject is erasure.**

The repair is in §II's method: deterministic pagination, verified against a declared total.

## V. The standing rule this produces

**Proposed, and requiring its own ruling:**

> **An absence may not be asserted from a search whose completeness has not been demonstrated.** For the blog, that means the index at `datasets/blog-index/`. For duplicate detection within the archive's own corpus, it means an instrument that can detect compression, not only copying — because this archive demonstrably compresses and re-sorts its material, and a lexical test will return a false negative every time it does.

**Until such an instrument exists, "not previously deposited" is a claim this archive cannot make about its own work**, and the honest form is "no deposited copy was found by title and by six-gram overlap, which does not exclude compression into a later work."

## VI. What is not claimed

That the 52 Codex posts are unpublished — §III and §IV.1 explicitly refuse that. That the index is permanent — it is a snapshot dated 2026-08-23 and requires a regeneration cadence. That word counts exist for the index — they do not; the summary feed does not carry bodies, and a full-body harvest is a separate run. That the 2,068-post gap is all seatable material — much of it will be drafts, duplicates, and posts already compressed into deposits.
