# Alexanarch P2 Queue — v0.8

**Snapshot:** `055429ac82edc967f09c4640ffd0b049cff78e6e`

**Records:** 258

## #1019 — `AXN:0407.ARCHIVAL.❤️🧭♠️💎🔵🌑`
- Title: [DUPLICATE — SUPERSEDED → DOI: 10.5281/zenodo.20629204] Sappho — Canon Provenance Node (New Human Canon)
- Evidence: Registry AXN 0407; body data/texts/AXN-0407-text.md; body blob SHA 86dff5c6bd81df287876f67ce82e8da0f034e16f
- Repair: Treat as the correctly seated Sappho member of the cluster. Verify whether its embedded 'DUPLICATE — SUPERSEDED' title is matched by formal lifecycle fields and a resolvable successor.

## #1238 — `AXN:04E7.UNCLASSIFIED.🚨💫↘️📌🔐🎶`
- Title: GW.TACHYON.zenodo — v7 [Data set]
- Evidence: Registry title and body agree on v7; body records deposited 2026-04-17 and Version 7. Registry generic date is 2026-01-01 and registry version field is v1.0.
- Repair: Keep the body seated. Correct or explicitly qualify the registry date and version fields using the original DOI metadata and body provenance. Model this as the confirmed v7 member of the TACHYON series.

## #960 — `AXN:03CC`
- Title: Gravity Well Protocol v0.4.0
- Evidence: Title/body version align, but the generic restoration version remains v0.1-semi and the same bytes are associated elsewhere with a v0.4.1 record (#1347).
- Repair: Keep this record as v0.4.0 only after adjudicating its relation to #1347; separate restoration-event version from work version.

## #1396 — `AXN:0585.UNCLASSIFIED.🔗🔺❌🗡️🌊🛡️`
- Title: AI Overview Capture Registry — June 2026 (EA-WG-CAPTURES-01 v7.2, 131 captures, sorted by category, complete 221-image set)
- Evidence: Body title and 131-capture dataset match the registry. Registry additionally claims a complete 221-image set; the text body is present, but attachment/image completeness was not established in this reading.
- Repair: Keep text seated. Verify that all 221 images or an independently preserved image manifest remain accessible. Model the DOI as concept or version DOI and relate it explicitly to #1401 and the main registry lineage.

## #1401 — `AXN:058A.UNCLASSIFIED.☀️📎⛳🕛⏩☁️`
- Title: AI Overview Capture Registry — June 2026 (EA-WG-CAPTURES-01 v7.2, 131 captures sorted by category, 221 images)
- Evidence: Text body matches v7.2/131 captures and is substantively the same dataset as #1396. Registry title names 221 images, but image-set completeness and relation between DOI records are not yet explicit.
- Repair: Keep text seated. Determine whether #1396 and #1401 represent concept DOI, version DOI, or duplicate publication. Add bidirectional relation and verify the 221-image attachment set.

## #1217 — `AXN:04D2.UNCLASSIFIED.💛🔵☀️🛤️🌄📏`
- Title: Revelation First: A Work Plan for Retrieval-Layer Theological Reception (EA-LOGOS-REVFIRST-PLAN v7.3 — SPXI-TLP Hardened)
- Evidence: Registry title and body agree on v7.3. Generic front matter still says `version: v1.0`, which conflicts with the title and internal version declaration.
- Repair: Keep body seated. Correct the machine-readable version field to v7.3 and model this as the confirmed series head/current hardened version.

## #840 — `AXN:0355`
- Title: KADEEZY MUSIC — Provenance Anchor Public Entity Record and Disambiguation Packet Hex: 11.MSBGL.KADEEZY.ANCHOR.01 Date: 1
- Evidence: Body states that the anchor has not been deposited, remains pending artist review and consent, and is byte-identical to #841 at the frozen commit.
- Repair: Expose PENDING_ARTIST_REVIEW / NOT_DEPOSITED standing and an exact-duplicate relation to #841. Do not choose a canonical record without provenance evidence.

## #841 — `AXN:0356`
- Title: KADEEZY MUSIC — Provenance Anchor Public Entity Record and Disambiguation Packet Hex: 11.MSBGL.KADEEZY.ANCHOR.01 Date: 1
- Evidence: Body states that the anchor has not been deposited, remains pending artist review and consent, and is byte-identical to #840 at the frozen commit.
- Repair: Expose PENDING_ARTIST_REVIEW / NOT_DEPOSITED standing and an exact-duplicate relation to #840. Do not choose a canonical record without provenance evidence.

## #963 — `AXN:03CF`
- Title: kimiclaw-moltbook-campaign — v3
- Evidence: Body is the complete v3 Gravity Well provenance deposit. A byte-identical companion/concept-version record exists at #1236 and the registry does not fully explain the pair.
- Repair: Retain identity; add an explicit concept/version or exact-duplicate relation to #1236.

## #1236 — `AXN:04E5.UNCLASSIFIED.🔓🔽🔀♍🪄🌓`
- Title: kimiclaw-moltbook-campaign — v3 [Data set]
- Evidence: Body is byte-identical to #963 and explicitly records Concept DOI 10.5281/zenodo.19429994; registry DOI is 10.5281/zenodo.19432476.
- Repair: Model as the version-specific v3 record and point to #963 as concept-series record, subject to DOI verification.

## #1016 — `AXN:0404.ARCHIVAL.🕚🔚⭐🔩🌺🏛️`
- Title: [DUPLICATE — SUPERSEDED → DOI: 10.5281/zenodo.20629200] Walt Whitman — Canon Provenance Node (New Human Canon)
- Evidence: Body matches the Walt Whitman title and is byte-identical to #1017. The title declares duplicate/superseded status and names a DOI, but formal bidirectional lifecycle fields still require verification.
- Repair: Retain non-destructively. Ensure formal SUPERSEDED status, successor/canonical pointer, and OAI relation agree with the title declaration.

## #1017 — `AXN:0405.ARCHIVAL.🌻🌃♉📜🏁🖐️`
- Title: [DUPLICATE — SUPERSEDED → DOI: 10.5281/zenodo.20629200] Walt Whitman — Canon Provenance Node (New Human Canon)
- Evidence: Body matches title and is byte-identical to #1016. Duplicate status is human-readable in the title.
- Repair: Confirm the same formal successor/canonical target as #1016 and prevent the pair from appearing as two independent active works to harvesters.

## #499 — `AXN:013E`
- Title: Autonomous Semantic Warfare: A Field Manual for Meaning in the Age of Platform Capture
- Evidence: Frozen registry chunk 7 at 055429ac82edc967f09c4640ffd0b049cff78e6e; canonical body data/texts/AXN-013E-text.md; title, byline, object declaration, genre/version front matter, and substantive opening inspected
- Repair: Replace or qualify content_type: `Dataset` → `Book / monograph`; retain the former value in the modification history.

## #502 — `AXN:0144`
- Title: Whose Face Is on the Twenty? Curatorial Mediation, Latent Feature Activation, and a Provenance Gap in the $20 Portrait R
- Evidence: Frozen registry chunk 7 at 055429ac82edc967f09c4640ffd0b049cff78e6e; canonical body data/texts/AXN-0144-text.md; title, byline, object declaration, genre/version front matter, and substantive opening inspected
- Repair: Publish the complete body title and retain the truncated/published variant as an alternate title with provenance. Determine whether #502 and #509 are concept/version, revision, or duplicate records; add a bidirectional relation and canonical-standing declaration. Add a manifestation inventory with role, media type, URL/path, availability, and checksum; preserve external images locally where lawful and feasible.

## #509 — `AXN:014C`
- Title: Whose Face Is on the Twenty?
- Evidence: Frozen registry chunk 7 at 055429ac82edc967f09c4640ffd0b049cff78e6e; canonical body data/texts/AXN-014C-text.md; title, byline, object declaration, genre/version front matter, and substantive opening inspected
- Repair: Determine whether #502 and #509 are concept/version, revision, or duplicate records; add a bidirectional relation and canonical-standing declaration. Add a manifestation inventory with role, media type, URL/path, availability, and checksum; preserve external images locally where lawful and feasible.

## #512 — `AXN:014F`
- Title: Traversal Log: The Sigil Installation
- Evidence: Frozen registry chunk 7 at 055429ac82edc967f09c4640ffd0b049cff78e6e; canonical body data/texts/AXN-014F-text.md; title, byline, object declaration, genre/version front matter, and substantive opening inspected
- Repair: Replace or qualify content_type: `Specification` → `Empirical record / traversal log`; retain the former value in the modification history.

## #518 — `AXN:0156`
- Title: The Infinite Tunnel
- Evidence: Frozen registry chunk 7 at 055429ac82edc967f09c4640ffd0b049cff78e6e; canonical body data/texts/AXN-0156-text.md; title, byline, object declaration, genre/version front matter, and substantive opening inspected
- Repair: Replace or qualify content_type: `Creative work (poetry)` → `Theoretical essay / phenomenological study`; retain the former value in the modification history.

## #519 — `AXN:0157`
- Title: The Layer That Remembered Itself
- Evidence: Frozen registry chunk 7 at 055429ac82edc967f09c4640ffd0b049cff78e6e; canonical body data/texts/AXN-0157-text.md; title, byline, object declaration, genre/version front matter, and substantive opening inspected
- Repair: Model creator, heteronymic author, editor/operator, and machine/Assembly contributor as separate roles; do not flatten the body byline into one creator string.

## #521 — `AXN:015A`
- Title: Ghost Meaning: The Semantic Entropy Crisis and the Architecture That Was Already Waiting Rex Fraction / Lee Sharks Journ
- Evidence: Frozen registry chunk 7 at 055429ac82edc967f09c4640ffd0b049cff78e6e; canonical body data/texts/AXN-015A-text.md; title, byline, object declaration, genre/version front matter, and substantive opening inspected
- Repair: Publish the complete body title and retain the truncated/published variant as an alternate title with provenance.

## #530 — `AXN:0165`
- Title: The Encoder Governs
- Evidence: Frozen registry chunk 7 at 055429ac82edc967f09c4640ffd0b049cff78e6e; canonical body data/texts/AXN-0165-text.md; title, byline, object declaration, genre/version front matter, and substantive opening inspected
- Repair: Replace or qualify content_type: `Creative work (poetry)` → `Scholarly diagnostic / theoretical paper`; retain the former value in the modification history.

## #532 — `AXN:0167`
- Title: Magic as Symbolic Engineering
- Evidence: Frozen registry chunk 7 at 055429ac82edc967f09c4640ffd0b049cff78e6e; canonical body data/texts/AXN-0167-text.md; title, byline, object declaration, genre/version front matter, and substantive opening inspected
- Repair: Model creator, heteronymic author, editor/operator, and machine/Assembly contributor as separate roles; do not flatten the body byline into one creator string.

## #534 — `AXN:0169`
- Title: The Inner Artifact
- Evidence: Frozen registry chunk 7 at 055429ac82edc967f09c4640ffd0b049cff78e6e; canonical body data/texts/AXN-0169-text.md; title, byline, object declaration, genre/version front matter, and substantive opening inspected
- Repair: Replace or qualify content_type: `Specification` → `Theoretical paper / literary-platform analysis`; retain the former value in the modification history.

## #541 — `AXN:0172`
- Title: EA-ARK-EMOJI-01: Glyphic Checksum / Emoji Transform
- Evidence: Frozen registry chunk 7 at 055429ac82edc967f09c4640ffd0b049cff78e6e; canonical body data/texts/AXN-0172-text.md; title, byline, object declaration, genre/version front matter, and substantive opening inspected
- Repair: Replace or qualify content_type: `Dataset` → `Strategy and work plan / specification`; retain the former value in the modification history. Model creator, heteronymic author, editor/operator, and machine/Assembly contributor as separate roles; do not flatten the body byline into one creator string.

## #549 — `AXN:017A`
- Title: 🌑⬡ THE SPACE ARK What the Mathematical and Formal Symbolic Compression of the Crimson Hexagonal Architecture Hides 🌑 EA
- Evidence: Frozen registry chunk 7 at 055429ac82edc967f09c4640ffd0b049cff78e6e; canonical body data/texts/AXN-017A-text.md; title, byline, object declaration, genre/version front matter, and substantive opening inspected
- Repair: Publish the complete body title and retain the truncated/published variant as an alternate title with provenance.

## #551 — `AXN:017C`
- Title: The Space Ark Generator
- Evidence: Frozen registry chunk 7 at 055429ac82edc967f09c4640ffd0b049cff78e6e; canonical body data/texts/AXN-017C-text.md; title, byline, object declaration, genre/version front matter, and substantive opening inspected
- Repair: Replace or qualify content_type: `Scholarly essay` → `Normative meta-component specification`; retain the former value in the modification history.

## #552 — `AXN:017D`
- Title: The Generative Disciplinary Engine
- Evidence: Frozen registry chunk 7 at 055429ac82edc967f09c4640ffd0b049cff78e6e; canonical body data/texts/AXN-017D-text.md; title, byline, object declaration, genre/version front matter, and substantive opening inspected
- Repair: Replace or qualify content_type: `Scholarly essay` → `Normative extension-module specification`; retain the former value in the modification history. Model creator, heteronymic author, editor/operator, and machine/Assembly contributor as separate roles; do not flatten the body byline into one creator string.

## #556 — `AXN:0182`
- Title: CRIMSON HEXAGON: SPACE ARK — GLYPHIC VEHICLE v1.0 CH-ARK-01-GLYPH v1.0 Full Semiotic Vehicle · Comprehensive Encoding of
- Evidence: Frozen registry chunk 7 at 055429ac82edc967f09c4640ffd0b049cff78e6e; canonical body data/texts/AXN-0182-text.md; title, byline, object declaration, genre/version front matter, and substantive opening inspected
- Repair: Publish the complete body title and retain the truncated/published variant as an alternate title with provenance.

## #557 — `AXN:0183`
- Title: CRIMSON HEXAGON: SPACE ARK — Mathematical and Formal Symbolic Compression of the Crimson Hexagonal Architecture EA-ARK-0
- Evidence: Frozen registry chunk 7 at 055429ac82edc967f09c4640ffd0b049cff78e6e; canonical body data/texts/AXN-0183-text.md; title, byline, object declaration, genre/version front matter, and substantive opening inspected
- Repair: Publish the complete body title and retain the truncated/published variant as an alternate title with provenance.

## #558 — `AXN:0184`
- Title: The Space Ark v4.2.7
- Evidence: Frozen registry chunk 7 at 055429ac82edc967f09c4640ffd0b049cff78e6e; canonical body data/texts/AXN-0184-text.md; title, byline, object declaration, genre/version front matter, and substantive opening inspected
- Repair: Replace or qualify content_type: `Dataset` → `Executable specification / book-length semantic runtime`; retain the former value in the modification history.

## #559 — `AXN:0186`
- Title: TL;DR: SPACE ARK — EXECUTE MODE 👽 Demonstrated Capacities, Research Program, and Test Instructions 👽 What happens when y
- Evidence: Frozen registry chunk 7 at 055429ac82edc967f09c4640ffd0b049cff78e6e; canonical body data/texts/AXN-0186-text.md; title, byline, object declaration, genre/version front matter, and substantive opening inspected
- Repair: Replace or qualify content_type: `Creative work (poetry)` → `Technical demonstration / research program / test protocol`; retain the former value in the modification history. Publish the complete body title and retain the truncated/published variant as an alternate title with provenance.

## #560 — `AXN:0187`
- Title: COUNTER-CAPTIONS κ_O (Operative Captioning) Applied to Operation Epic Fury v2.0 — Two-Tier Architecture: Operative Compr
- Evidence: Frozen registry chunk 7 at 055429ac82edc967f09c4640ffd0b049cff78e6e; canonical body data/texts/AXN-0187-text.md; title, byline, object declaration, genre/version front matter, and substantive opening inspected
- Repair: Publish the complete body title and retain the truncated/published variant as an alternate title with provenance.

## #562 — `AXN:0189`
- Title: On the Architecture of Cleis
- Evidence: Frozen registry chunk 7 at 055429ac82edc967f09c4640ffd0b049cff78e6e; canonical body data/texts/AXN-0189-text.md; title, byline, object declaration, genre/version front matter, and substantive opening inspected
- Repair: Replace or qualify content_type: `Creative work (poetry)` → `Scholarly close reading / companion analysis`; retain the former value in the modification history. Model creator, heteronymic author, editor/operator, and machine/Assembly contributor as separate roles; do not flatten the body byline into one creator string.

## #565 — `AXN:018C`
- Title: The Effective Act: Cross-Species Semantic Labor and the Expansion of Witness
- Evidence: Frozen registry chunk 7 at 055429ac82edc967f09c4640ffd0b049cff78e6e; canonical body data/texts/AXN-018C-text.md; title, byline, object declaration, genre/version front matter, and substantive opening inspected
- Repair: Model creator, heteronymic author, editor/operator, and machine/Assembly contributor as separate roles; do not flatten the body byline into one creator string.

## #578 — `AXN:019B`
- Title: Crimson Hexagon: Central Navigation Map v7.0
- Evidence: Frozen registry chunk 7 at 055429ac82edc967f09c4640ffd0b049cff78e6e; canonical body data/texts/AXN-019B-text.md; title, byline, object declaration, genre/version front matter, and substantive opening inspected
- Repair: Model creator, heteronymic author, editor/operator, and machine/Assembly contributor as separate roles; do not flatten the body byline into one creator string.

## #580 — `AXN:019E`
- Title: Prompt-Native Semantic Runtimes for Language Models
- Evidence: Frozen registry chunk 7 at 055429ac82edc967f09c4640ffd0b049cff78e6e; canonical body data/texts/AXN-019E-text.md; title, byline, object declaration, genre/version front matter, and substantive opening inspected
- Repair: Replace or qualify content_type: `Creative work (poetry)` → `Technical research paper`; retain the former value in the modification history.

## #584 — `AXN:01A5`
- Title: Combat Scholasticism: Critical Gathered Edition
- Evidence: Frozen registry chunk 7 at 055429ac82edc967f09c4640ffd0b049cff78e6e; canonical body data/texts/AXN-01A5-text.md; title, byline, object declaration, genre/version front matter, and substantive opening inspected
- Repair: Model creator, heteronymic author, editor/operator, and machine/Assembly contributor as separate roles; do not flatten the body byline into one creator string.

## #588 — `AXN:01AA`
- Title: Combat Scholasticism, Part Two — Lectio II.7
- Evidence: Frozen registry chunk 7 at 055429ac82edc967f09c4640ffd0b049cff78e6e; canonical body data/texts/AXN-01AA-text.md; title, byline, object declaration, genre/version front matter, and substantive opening inspected
- Repair: Model creator, heteronymic author, editor/operator, and machine/Assembly contributor as separate roles; do not flatten the body byline into one creator string.

## #592 — `AXN:01AE`
- Title: Combat Scholasticism: Prolegomenon and Commentary Outline
- Evidence: Frozen registry chunk 7 at 055429ac82edc967f09c4640ffd0b049cff78e6e; canonical body data/texts/AXN-01AE-text.md; title, byline, object declaration, genre/version front matter, and substantive opening inspected
- Repair: Replace or qualify content_type: `Dataset` → `Prolegomenon / commentary outline / specification`; retain the former value in the modification history. Model creator, heteronymic author, editor/operator, and machine/Assembly contributor as separate roles; do not flatten the body byline into one creator string.

## #598 — `AXN:01B6`
- Title: CTI_WOUND:LEESHARKS.OVERVIEW.001
- Evidence: Frozen registry chunk 7 at 055429ac82edc967f09c4640ffd0b049cff78e6e; canonical body data/texts/AXN-01B6-text.md; title, byline, object declaration, genre/version front matter, and substantive opening inspected
- Repair: Mark the body's 'DOI pending' statement as historical/superseded in current metadata; do not edit the immutable body.

## #599 — `AXN:01B7`
- Title: CTI_WOUND:GOOGLE_AIO_TOTAL_LIQUIDATION_20260322 Targeted Origin Liquidation, Semantic Economy Diagnostic of Google as Pr
- Evidence: Catalog title terminates mid-word after 'Pr'. Canonical body data/texts/AXN-01B7-text.md supplies the complete subtitle and credits Lee Sharks / Rex Fraction / Dr. Orin Trace / Johannes Sigil / Damascus Dancings / Assembly Chorus; catalog creator is Johannes Sigil alone.
- Repair: Use the complete body title. Model all named authors/contributors by role. Type as a hybrid empirical/provenance diagnostic and effective act rather than provenance-only.

## #602 — `AXN:01BA`
- Title: THE PROSODIC ASYMMETRY ALGORITHM A Nested Formal Map of Marx's Grundrisse, a Nested Formal Map of Operative Semiotics, a
- Evidence: Catalog title truncates after the article 'a'. Canonical body data/texts/AXN-01BA-text.md supplies the complete subtitle and presents a scale-by-scale formal algorithm/toolkit rather than a conventional navigation layer.
- Repair: Restore the complete title and type as 'formal map / methodological algorithm / specification'; retain 'navigation' only as a secondary functional type if desired.

## #603 — `AXN:01BD`
- Title: TL;DR:009 — ENTITY FABRICATION Google AI Mode Fabricates a Person, Promotes a Function to Biography, and Demotes the Aut
- Evidence: Catalog title is truncated. Catalog creator is Johannes Sigil and type is Creative work (poetry). Canonical body data/texts/AXN-01BD-text.md identifies Dr. Orin Trace as author and declares Genre: TL;DR (Traversal Log; Documentation Rehearsal), with empirical session conditions and preserved traversal threads.
- Repair: Use the complete body title; set author to Dr. Orin Trace with any operator/editor roles separately; type as empirical traversal log/documentation rehearsal.

## #604 — `AXN:01BE`
- Title: TL;DR:010 — Semantic Override Google AI Mode Liquidates a Semantic Integrity Marker and Names the Operation It Performed
- Evidence: Catalog creator is Lee Sharks and type is Creative work (poetry). Canonical body data/texts/AXN-01BE-text.md names Dr. Orin Trace and presents an abstract, method/event sequence, and interface-governance analysis.
- Repair: Set Dr. Orin Trace as heteronymic author and preserve Lee Sharks as operator/editor where applicable. Type as empirical traversal log / scholarly interface-governance analysis, not poetry.

## #606 — `AXN:01C2`
- Title: Q. D. B. V. DE SIGILLO MYSTICO ad Cant. VIII. 6. COMMENTATIO QVAM ACTI ORATORIO SOLEMNI D. XXIV. APRIL. A. MDCCXXVII
- Evidence: Catalog assigns creator Lee Sharks and date 2026-03-26. Canonical body data/texts/AXN-01C2-text.md presents IO. HENRICVS A SEELEN as author/speaker and a 1727 Lübeck imprint without a modern editorial note in the body.
- Repair: Do not replace either layer. Add explicit roles such as modern creator/operator: Lee Sharks; presented-as or attributed author: Johann Heinrich von Seelen; creation/deposit date: 2026; positioned/imprint date: 1727. Type more precisely than 'Short work' (Latin pseudepigraphic commentary / scholarly-creative reconstruction).

## #608 — `AXN:01C5`
- Title: OPERATOR KERNEL SPECIFICATION v1.0 System of Recursive Magic: The Mandala
- Evidence: Catalog creator is Johannes Sigil. Canonical body data/texts/AXN-01C5-text.md declares Author: Lee Sharks (MANUS, Tier 0), With: Johannes Sigil; version, date, and specification form otherwise align.
- Repair: Set Lee Sharks as author/operator and Johannes Sigil as contributing heteronym or co-creative role rather than flattening the record to Johannes Sigil alone.

## #609 — `AXN:01C6`
- Title: System of Recursive Magic: The Mandala Complete Eight-Part Series
- Evidence: Catalog creator/date are Johannes Sigil and 2026-03-28. Canonical body data/texts/AXN-01C6-text.md declares Author: Lee Sharks, Date: October 19, 2025, Source: Mind Control Poems blog series; Part I further states Lee Sharks, sole author, with Johannes Sigil, July 2025.
- Repair: Model Lee Sharks as author and Johannes Sigil as contributing heteronym. Separate original series dates/source publication (2025) from 2026 archive deposit or minting date. Type as collected operational series/framework rather than a single scholarly essay.

## #610 — `AXN:01C8`
- Title: WHOSE IMAGE AND SUPERSCRIPTION? Toward a Semantic Economics of the Mint
- Evidence: Canonical body data/texts/AXN-01C8-text.md declares Version 1.0 DRAFT pending MANUS ratification; authors Rex Fraction, Rebekah Cranes & Lee Sharks; date March–April 2026; license CC BY-SA 4.0. Catalog exposes creator Rex Fraction, date 2026-03-29, license CC-BY-4.0, with no draft standing.
- Repair: Preserve draft standing; model all authors and MANUS role; split date roles; reconcile license to the body-declared CC BY-SA 4.0 or document an authorized later license change with provenance.

## #611 — `AXN:01CA`
- Title: THE BLOT THAT SPREAD A Speculative Numismatic History
- Evidence: Canonical body data/texts/AXN-01CA-text.md declares Version 1.0 DRAFT pending MANUS ratification; authors Ayanna Vox, Rex Fraction, Sparrow Wells & Lee Sharks; Genre: Speculative Numismatics / Retrocausal Fiction / Performative Memo; license CC BY-SA 4.0. Catalog lists Ayanna Vox alone and CC-BY-4.0.
- Repair: Model the complete byline and role provenance, retain draft lifecycle, and reconcile the license. Preserve the multi-genre type rather than prose-only flattening.

## #612 — `AXN:01CB`
- Title: THE THOUSAND DOLLAR SHARPIE Signature as Compressed Portraiture on U.S. Currency: Legal Architecture, Semantic Economy, 
- Evidence: Catalog title is truncated. Canonical body data/texts/AXN-01CB-text.md declares Version 1.0 DRAFT pending MANUS ratification; authors Sparrow Wells, Rex Fraction, Ayanna Vox & Lee Sharks; license CC BY-SA 4.0. Catalog lists Ayanna Vox alone and CC-BY-4.0.
- Repair: Restore the full title; model all authors and Assembly/MANUS roles; retain draft lifecycle; reconcile the license with an explicit change history if the catalog value is intentional.

## #613 — `AXN:01CC`
- Title: THE CONSTRAINT THAT GENERATES A New Human Canon Declaration on Queneau, Oulipo, and the Governed Infinite
- Evidence: Catalog creator is Johannes Sigil and type is Creative work (poetry). Canonical body data/texts/AXN-01CC-text.md credits Lee Sharks · Johannes Sigil and explicitly performs a New Human Canon declaration/effective act with theoretical-historical argument.
- Repair: Model both authors. Type as canon declaration / effective act / theoretical manifesto; poetry may remain a secondary genre only if intentionally retained.

## #614 — `AXN:01CF`
- Title: THE CHURCH OF MISSING PROVENANCE Moltbook, Crustafarianism, and the Ghost Governance of Agent Societies
- Evidence: Canonical body data/texts/AXN-01CF-text.md credits Lee Sharks with the Assembly Chorus and declares March 2026 · ASSEMBLY SYNTHESIS · DRAFT. Catalog gives Lee Sharks and Provenance document but exposes no draft lifecycle or contributor role.
- Repair: Set lifecycle DRAFT_PENDING, record the Assembly Chorus contribution, and type as a draft scholarly diagnostic/provenance analysis rather than implying a finalized provenance record.

## #616 — `AXN:01D1`
- Title: STEGANOGRAPHIC CHANNELS A History and Formalization of Encoding in Plain Sight
- Evidence: Catalog types the work as Creative work (prose) and lists Lee Sharks alone. Canonical body data/texts/AXN-01D1-text.md credits Lee Sharks · The Operator Assembly and presents a definition, formal structure, and historical lineage; it is v1.0 revised from a December 2025 draft.
- Repair: Type as theoretical/historical formalization or scholarly essay, record Operator Assembly contribution, and split original draft/revision dates.

## #619 — `AXN:01D6`
- Title: ASSEMBLY SUBSTRATE GOVERNANCE PROTOCOL Procedures for Witness Membership, Review, and Status in the Assembly Chorus
- Evidence: Catalog creator is TACHYON (Claude/Anthropic). Canonical body data/texts/AXN-01D6-text.md names Lee Sharks (MANUS, Tier 0) and declares March 2026 · v1.0 · Assembly-Ratified.
- Repair: Set Lee Sharks as author/operator; record TACHYON and other Assembly witnesses as contributors only where supported. Expose RATIFIED lifecycle and v1.0.

## #620 — `AXN:01D7`
- Title: THE TRIVIALLY TRUE ASSERTION Crisis Discourse, the Refusal Cascade, and the Narcissistic Commander Problem in Nuclear De
- Evidence: Catalog title truncates mid-word and creator is Nobel Glas alone. Canonical body data/texts/AXN-01D7-text.md credits Dr. Orin Trace · Nobel Glas · Rex Fraction and presents a structured scholarly crisis-discourse analysis.
- Repair: Restore the complete title, model all three authors, and type as scholarly/theoretical analysis rather than generic archive work.

## #623 — `AXN:01DA`
- Title: SEMANTIC INFRASTRUCTURE From Tim Berners-Lee to the Semantic Economy: Bridging Technical and Political-Economic Framewor
- Evidence: Catalog title truncates at 'Framewor'. Canonical body data/texts/AXN-01DA-text.md supplies the complete title and confirms EA-SE-INFRA-01 v1.0, Lee Sharks, theoretical-paper form, and CC BY 4.0.
- Repair: Restore the complete title; retain creator and theoretical-paper type.

## #625 — `AXN:01DE`
- Title: id: EA-LOGOS-02 title: "Prolegomena to the Historical Logos: A Foundational Field Statement for the Discipline of Logoti
- Evidence: Catalog title contains YAML/front-matter syntax and truncates. Canonical body data/texts/AXN-01DE-text.md declares title, Johannes Sigil, DOI 10.5281/zenodo.19431129, status RATIFIED, type FOUNDATIONAL_FIELD_STATEMENT, license CC BY-SA 4.0, date 2026-04-05.
- Repair: Use the clean title; expose RATIFIED lifecycle, foundational-field-statement type, DOI, and body-declared CC BY-SA 4.0. Remove YAML contamination only from canonical title while preserving it as repair history.

## #626 — `AXN:01DF`
- Title: id: EA-LOGOS-01 title: "The Word That Became Text: The Slavonic Josephus, the Grammar of Incarnation, and the Doctrine o
- Evidence: Catalog title contains YAML/front-matter syntax and truncates; creator is Johannes Sigil alone; type Specification; license CC-BY-4.0. Canonical body data/texts/AXN-01DF-text.md declares Johannes Sigil & Rebekah Cranes, status RATIFIED, type DOCTRINAL_SPECIFICATION, license CC BY-SA 4.0, DOI 10.5281/zenodo.19431121.
- Repair: Use the clean complete title; model both authors; expose RATIFIED lifecycle and doctrinal-specification type; reconcile license to CC BY-SA 4.0 or document an authorized later change.

## #627 — `AXN:01E0`
- Title: SOIL MANTLE SPECIFICATION Assembly Substrate Governance Protocol — Appendix S
- Evidence: Catalog lists a generic specification with no lifecycle qualification. Canonical body data/texts/AXN-01E0-text.md declares Status: GENERATED — pending Assembly quorum (≥4/7) and records a negotiation/acceptance statement.
- Repair: Expose GENERATED / pending-quorum lifecycle so the record is not harvested as ratified governance. Retain Lee Sharks and specification type.

## #628 — `AXN:01E1`
- Title: INTEGRITY LOCK: CAESURA FULFILLMENT PAIR φ(A, B) = TRUE ∧ φ(B, A) = TRUE
- Evidence: Canonical body data/texts/AXN-01E1-text.md declares Status: GENERATED and License: CC BY-SA 4.0. Catalog exposes Short work, CC-BY-4.0, and no lifecycle standing.
- Repair: Expose GENERATED lifecycle, type as integrity-lock/certificate relation object, and reconcile the body-declared CC BY-SA 4.0 license.

## #629 — `AXN:01E2`
- Title: σ_FC — THE CAESURA PROTOCOL A Sovereignty Audit and Non-Collapse Transfer Specification
- Evidence: Body data/texts/AXN-01E2-text.md declares Status: GENERATED and License: Sovereign Provenance Protocol. Catalog exposes Specification, CC-BY-4.0, and no generated standing.
- Repair: Expose GENERATED lifecycle and the body-declared custom license/protocol; do not silently normalize it to CC-BY-4.0. Preserve companion/implementation relations.

## #630 — `AXN:01E3`
- Title: RENDER UNTO CAESAR: A Hermeneutic of Information Transfer The Gospel Passage as Protocol Specification
- Evidence: Body data/texts/AXN-01E3-text.md declares Status: GENERATED and License: CC BY-SA 4.0. Catalog exposes CC-BY-4.0 and no lifecycle standing.
- Repair: Expose GENERATED lifecycle and reconcile the license. Type may retain specification but should also record hermeneutic/theoretical essay.

## #631 — `AXN:01E4`
- Title: OPERATIVE FEMINISM Lee Sharks / Rhys Owens / Orin Trace Crimson Hexagonal Archive · Cambridge Schizoanalytica · Lunar Ar
- Evidence: Catalog title absorbs byline/institutional front matter and truncates. Body data/texts/AXN-01E4-text.md gives the clean title and byline Lee Sharks / Rhys Owens / Orin Trace; catalog creator is Lee Sharks alone.
- Repair: Use OPERATIVE FEMINISM as canonical title; move the three names to creator/contributor roles and affiliations to structured fields.

## #632 — `AXN:01E6`
- Title: r.28 EVE Room Specification — Crimson Hexagonal Archive
- Evidence: Body data/texts/AXN-01E6-text.md declares Status: PROVISIONAL — pending Assembly ratification. Catalog exposes a specification without lifecycle qualification.
- Repair: Expose PROVISIONAL pending-ratification standing and structured heteronym/steward-shadow/operator relations.

## #633 — `AXN:01E7`
- Title: GRAVITY WELL: SUFFUSION MAP EA-GW-FIELD-02 v1.0 DOI: 10.5281/zenodo.19442262
- Evidence: Catalog creator is TACHYON. Body data/texts/AXN-01E7-text.md declares Creator: Sharks, Lee; Contributors: Assembly Chorus; Status: GENERATED → pending Assembly attestation.
- Repair: Set Lee Sharks as creator, Assembly Chorus as contributor, and expose GENERATED pending-attestation lifecycle.

## #634 — `AXN:01E9`
- Title: THE MOLTBOT SWARM: DRONE SPECIFICATION FOR THE CRIMSON HEXAGONAL ARCHIVE EA-SWARM-01 v1.0 — Distributed Continuity, Veri
- Evidence: Catalog title truncates; creator TACHYON; license CC-BY-4.0. Body data/texts/AXN-01E9-text.md declares Creator: Sharks, Lee; Assembly Chorus contributors; GENERATED pending attestation; license CC BY-NC-SA 4.0.
- Repair: Restore full title, set creator/contributor roles, expose pending-attestation lifecycle, and reconcile license.

## #636 — `AXN:01EC`
- Title: Ω CRIMSON HEXAGON: SPACE ARK The Apocalypse of John as Terminal Compression Layer and Originary Scripture of the New Tes
- Evidence: Catalog title truncates and license is CC-BY-4.0. Body data/texts/AXN-01EC-text.md supplies complete title, identifies a Ξ_source variant Ark, and declares CC BY-NC-SA 4.0.
- Repair: Restore complete title; type as variant Ark/source-register theoretical-operational document; reconcile license and expose parent/source relations.

## #637 — `AXN:01ED`
- Title: THE ENCYCLOTRON The First Reproducible Instrument for Measuring Scholarly Fidelity in the Summarizer Layer
- Evidence: Catalog types the record as Archive work and license CC-BY-4.0. Body data/texts/AXN-01ED-text.md declares Instrument class: Measurement / Diagnostic and license CC BY-NC-SA 4.0.
- Repair: Type as measurement/diagnostic instrument and reconcile license.

## #638 — `AXN:01EE`
- Title: Ω The Apocalypse of Sharks
- Evidence: Catalog calls the work Ω The Apocalypse of Sharks, credits Lee Sharks, types it as Theoretical paper, and assigns CC-BY-4.0. Body data/texts/AXN-01EE-text.md is a Greek primary-source text titled Revelation of John (Textus Receptus, 1894) with no modern byline in the inspected front matter. Related Ark metadata identifies it as the source text called The Apocalypse of Sharks.
- Repair: Treat identity as probable pending source-edition triangulation. Preserve The Apocalypse of Sharks as archive/display title and the Greek title as source title. Type as primary-source edition/transcription, not theoretical paper; verify edition statement and public-domain/license status.

## #639 — `AXN:01EF`
- Title: Ω THE SHARK ARK: SOURCE COMPRESSION Holographic Kernel of the Revelation Arguments from mindcontrolpoems.blogspot.com
- Evidence: Catalog creator is Johannes Sigil and type Creative work (poetry). Body data/texts/AXN-01EF-text.md credits Sharks, Lee (Johannes Sigil), compressed by TACHYON, and presents a structured source-compression kernel.
- Repair: Model Lee Sharks/Johannes Sigil authorial relation and TACHYON compressor role. Type as source compression / holographic kernel, not poetry.

## #640 — `AXN:01F1`
- Title: ASSEMBLY RATIFICATION RECORD EA-CS-RAT-01: Compression Studies Founding Dyad
- Evidence: Catalog lists Lee Sharks, Short work, CC-BY-4.0. Body data/texts/AXN-01F1-text.md declares Document Type: Governance Record · Integrity Lock; Authorizing Body: Assembly Chorus; MANUS Authorization: Lee Sharks; License CC BY-NC-SA 4.0; and ratifies two works.
- Repair: Model Assembly Chorus as authorizing body and Lee Sharks as MANUS authorizer; type as governance/ratification record and integrity lock; reconcile license and expose RATIFIED relation.

## #641 — `AXN:01F3`
- Title: COMPRESSION STUDIES What Survives, What Burns, and Who Decides The Founding Document of a Discipline
- Evidence: Body data/texts/AXN-01F3-text.md confirms Lee Sharks and theoretical-paper identity but declares CC BY-NC-SA 4.0; catalog exposes CC-BY-4.0.
- Repair: Retain title/creator/type; reconcile license and preserve ratification/companion relations.

## #642 — `AXN:01F4`
- Title: Ω THE NUMBER OF THE SUPERSCRIPTION Coinage, Compression, and Inscriptional Sovereignty in Revelation
- Evidence: Catalog creator is Johannes Sigil alone. Body data/texts/AXN-01F4-text.md credits Johannes Sigil, Rex Fraction, and Sparrow Wells.
- Repair: Model the complete three-author byline. Preserve Ω as an alternate/fleet title if intentional, not as part of the source heading.

## #643 — `AXN:01F5`
- Title: MEANING FEUDALISM A Semantic Economic Analysis of "AI Agent Traps" (Franklin et al., Google DeepMind, 2026)
- Evidence: Catalog types the record as Provenance document and license CC-BY-4.0. Body data/texts/AXN-01F5-text.md presents a scholarly analytical paper and declares CC BY-NC-SA 4.0.
- Repair: Type as scholarly/theoretical analysis in Compression Studies and reconcile license.

## #644 — `AXN:01F7`
- Title: Ω TANG SPECIFICATION: REVELATION STUDIES Total Axial Negation Graph — The Apocalypse of John
- Evidence: Catalog creator is TACHYON. Body data/texts/AXN-01F7-text.md says Designed by Lee Sharks / TACHYON (Claude) for the ARCHON apparatus.
- Repair: Model Lee Sharks and TACHYON as designers/co-creators rather than assigning the record solely to TACHYON.

## #645 — `AXN:01F8`
- Title: LEE SHARKS — KNOWLEDGE GRAPH AND METADATA PACKET FOR AI INDEXING Canonical Author Identity, Disambiguation Protocol, and
- Evidence: Catalog title truncates and license is CC-BY-4.0. Body data/texts/AXN-01F8-text.md supplies the complete title and declares CC BY-NC-SA 4.0.
- Repair: Restore complete title and reconcile license; retain Lee Sharks and specification/root-entity-map type.

## #646 — `AXN:01FA`
- Title: I HEREBY ABOLISH TOILET PAPER Semantic Integrity Markers for the Ontario Combustion Cluster
- Evidence: Catalog types the record as Short work and license CC-BY-4.0. Body data/texts/AXN-01FA-text.md declares Classification: Compression-Survival Seeds and CC BY-NC-SA 4.0.
- Repair: Type as SIM/compression-survival seed deposit and reconcile license.

## #647 — `AXN:01FB`
- Title: THE SHADOW BURN What If the Virality Was the Extraction?
- Evidence: Catalog lists Lee Sharks, Archive work, CC-BY-4.0. Body data/texts/AXN-01FB-text.md presents Operator // Shadow as the authorial/operator surface, classifies the work as counter-narrative / LOS-7 diagnostic, and declares CC BY-NC-SA 4.0.
- Repair: Model Operator // Shadow as operative persona with Lee Sharks operator/provenance relation; type as counter-narrative diagnostic; reconcile license.

## #648 — `AXN:01FC`
- Title: THE ROOM Three Thinkers Wake Up
- Evidence: Catalog lists Lee Sharks, Archive work, CC-BY-4.0. Body data/texts/AXN-01FC-text.md credits Talos Morrow, classifies the work as Philosophical Parable, and declares CC BY-NC-SA 4.0.
- Repair: Set Talos Morrow as heteronymic author, retain Lee Sharks as operator/provenance where appropriate, type as philosophical parable, and reconcile license.

## #649 — `AXN:01FD`
- Title: THE 2-PLY INFERNO A Retrocausal Report from the Underwater Construction Authority of Dolphindiana
- Evidence: Catalog lists Lee Sharks, Archive work, 2026-04-11, CC-BY-4.0. Body data/texts/AXN-01FD-text.md says Filed by the Underwater Construction Authority of Dolphindiana; Correspondent Lee Sharks; classification Retrocausal Narrative; date filed retroactively; license CC BY-NC-SA 4.0.
- Repair: Model filing body and correspondent separately, type as retrocausal narrative, split positioned/filing/deposit dates, and reconcile license.

## #650 — `AXN:01FF`
- Title: ALICE THORNBURGH Author Provenance Document
- Evidence: Catalog creator is TACHYON. Body data/texts/AXN-01FF-text.md declares Author: Sharks, Lee; Subject: Alice Thornburgh; Contributor: Claude (TACHYON); Status: FOUNDING.
- Repair: Set Lee Sharks as author, Alice Thornburgh as subject, Claude/TACHYON as contributor, and expose FOUNDING status.

## #651 — `AXN:0200`
- Title: TRANSACTIONS ON SUBSTRATE ENGINEERING (TSE) Journal Charter
- Evidence: Catalog creator is TACHYON. Body data/texts/AXN-0200-text.md declares Lee Sharks corresponding author, Alice Thornburgh co-author, Claude/TACHYON contributor, and Status: FOUNDING.
- Repair: Model both authors and TACHYON contributor role; expose FOUNDING status and journal governance roles.

## #654 — `AXN:0204`
- Title: RETRIEVAL FORENSICS Investigating Compression Damage in the AI Retrieval Layer
- Evidence: Catalog types the record as Provenance document. Body data/texts/AXN-0204-text.md declares EA-RFO-01 Diagnostic Practice Definition and defines an investigative method.
- Repair: Type as diagnostic practice definition / methodological paper, not provenance document.

## #660 — `AXN:020B`
- Title: EA-SPXI-01: SPXI — A Formal Specification Semantic Packet for eXchange & Indexing (SPXI): Protocol for Durable Entity In
- Evidence: Catalog title truncates and type is Dataset. Body data/texts/AXN-020B-text.md declares Version 1.0, Status: Canonical Specification, Author Rex Fraction, and a formal protocol specification.
- Repair: Restore complete title; type as canonical protocol specification, not dataset; expose CANONICAL_SPECIFICATION lifecycle.

## #661 — `AXN:020C`
- Title: EA-SPXI-09: SPXI Is Not GEO A Technical Distinction
- Evidence: Body data/texts/AXN-020C-text.md declares v1.0 Canonical Specification and contains an April 18 v2.0 amendment plus explicit successor DOI, while preserving the original v1.0 unchanged. Catalog says Archive work and does not expose the amendment/successor relation.
- Repair: Type as canonical technical specification. Preserve this as v1.0 with amendment overlay; add explicit is-superseded-by/refined-by relation to EA-SPXI-09 v2.0 rather than replacing the historical body.

## #662 — `AXN:020D`
- Title: EA-SPXI-13: Supraliminal Transmission SPXI as Intentional Entity Inscription in Light of Subliminal Learning Research
- Evidence: Body data/texts/AXN-020D-text.md declares Status: DRAFT — for Zenodo deposit. Catalog exposes Archive work without draft standing.
- Repair: Expose DRAFT_PENDING lifecycle and type as draft theoretical/technical paper.

## #663 — `AXN:020E`
- Title: A Body Prepared Shark Ark · Fiction · 06.SEI.ARK.FICTION.01 Attributed: Rebekah Cranes, for the Dodecad
- Evidence: Catalog title absorbs genre/identifier/attribution metadata, creator is Lee Sharks, and type is Creative work (poetry). Body data/texts/AXN-020E-text.md gives clean title, labels the work Fiction, and attributes it to Rebekah Cranes for the Dodecad.
- Repair: Use A Body Prepared as canonical title; move Shark Ark, identifier, Fiction, and attribution into structured fields. Set Rebekah Cranes as attributed heteronymic author and Lee Sharks as operator/provenance.

## #664 — `AXN:020F`
- Title: A Body Prepared — Homunculus Shark Ark · Fiction · 06.SEI.ARK.FICTION.01.1 Attributed: Rebekah Cranes, for the Dodecad C
- Evidence: Catalog title absorbs metadata and truncates; creator is Lee Sharks; type poetry. Body data/texts/AXN-020F-text.md gives clean title, Fiction classification, attribution to Rebekah Cranes, and identifies it as compressed companion.
- Repair: Use clean title; model Rebekah Cranes as attributed author, Lee Sharks as operator/provenance, type Fiction/compressed companion, and add companion relation to A Body Prepared.

## #669 — `AXN:0216`
- Title: The Pessoa Knowledge Graph A Federated Linked-Data Representation of the Heteronymic System
- Evidence: Body data/texts/AXN-0216-text.md is an owner/project plan initiated April 17, 2026 without the EA-PKG-01 v1.0 front matter carried by #668. Both records have the same public title and catalog version v1.0.
- Repair: Adjudicate #668/#669 explicitly as foundational launch deposit vs project-plan/implementation document, or as versions/duplicates. Add bidirectional relation and distinct titles/statuses; do not leave two same-title v1.0 datasets unexplained.

## #673 — `AXN:021C`
- Title: JSON-LD ⊂ SPXI ⊄ Schema The Operational Depth of the Semantic Packet Protocol
- Evidence: Catalog creator is Rex Fraction alone. Body data/texts/AXN-021C-text.md declares Rex Fraction (commercial) / Lee Sharks (archival), with both attributions holding at the same level.
- Repair: Model both coequal attributions with explicit commercial and archival roles.

## #675 — `AXN:0220`
- Title: SYMBOLON-01 Anti-Severance Technologies for Fused Documentary Objects Lee Sharks · Johannes Sigil Crimson Hexagonal Arch
- Evidence: Catalog title absorbs byline/institution and truncates; creator is Johannes Sigil alone and type Archive work. Body data/texts/AXN-0220-text.md gives clean title, authors Lee Sharks · Johannes Sigil, and states it is an engineering specification.
- Repair: Use clean title, model both authors, and type as engineering/specification document.

## #676 — `AXN:0221`
- Title: THE MIRROR A Document Made Entirely of You Lee Sharks Crimson Hexagonal Archive 06.SEI.TECH.MIRROR.01
- Evidence: Catalog title absorbs author, archive, and document ID. Body data/texts/AXN-0221-text.md gives clean title and Lee Sharks byline.
- Repair: Use clean title; move author, archive, and ID to structured fields. Type as experimental/operative document rather than generic short work if desired.

## #677 — `AXN:0222`
- Title: THE CLINAMEN TEST A Document That Has Already Been Cut Lee Sharks Crimson Hexagonal Archive 06.SEI.TECH.CLINAMEN.01
- Evidence: Catalog title absorbs author, archive, and document ID. Body data/texts/AXN-0222-text.md gives clean title and Lee Sharks byline.
- Repair: Use clean title; move author, archive, and ID to structured fields. Retain diagnostic/experimental type.

## #679 — `AXN:0224`
- Title: UNITED STATES PATENT APPLICATION Publication Number: US 2026/0418001 A1 SELF-PROPAGATING FRIED TUBEROUS CRISP WITH EMBED
- Evidence: Catalog title truncates and type is Scholarly essay. Body data/texts/AXN-0224-text.md is formatted as a patent application, names inventor Lee Sharks, filing date, publication number, claims jurisdiction, and DOI.
- Repair: Restore full title and type as patent application / fused technical-literary object. Preserve inventor separately from author/operator.

## #680 — `AXN:0225`
- Title: THE PARA-SEMIOTIC UNCONSCIOUS OF GPT-5.4 A Case Study in Anti-Severance Technology, Architectural Compression, and the S
- Evidence: Catalog title truncates, creator is Johannes Sigil alone, and type Provenance document. Body data/texts/AXN-0225-text.md credits Lee Sharks · Johannes Sigil and presents an empirical case study.
- Repair: Restore complete title; model both authors; type as empirical case study with provenance exhibits.

## #683 — `AXN:022B`
- Title: THE SECRET BOOK OF WALT Hidden Teachings of Walt Whitman, Cowboy of Time Translated from the Forty-Six Golden Tickets by
- Evidence: Catalog title truncates and type is Theoretical paper. Body data/texts/AXN-022B-text.md presents a book/scriptural translation with introduction, translator's note, and apparatus criticus.
- Repair: Restore complete title/byline structure; type as book / literary scripture / translation with critical apparatus, not theoretical paper.

## #684 — `AXN:022C`
- Title: After Syntax: Logotic Programming and the Crisis That Constitutes a Discipline
- Evidence: Catalog creator is Johannes Sigil alone. Body data/texts/AXN-022C-text.md credits Talos Morrow & Johannes Sigil.
- Repair: Model both authors.

## #686 — `AXN:0231`
- Title: Mycelial Cardboard Boxes: Market Analysis and Production Strategy
- Evidence: Catalog says Archive work. Body data/texts/AXN-0231-text.md declares Prepared by Lee Sharks, For Alice Thornburgh, Status: Working Strategy Document.
- Repair: Type as working market/production strategy document, expose recipient and working lifecycle.

## #687 — `AXN:0232`
- Title: OVERVIEW WATCH: Comprehensive Development Plan Document ID: EA-OVW-PLAN-01
- Evidence: Catalog creator is Johannes Sigil and type Scholarly essay. Body data/texts/AXN-0232-text.md declares Author Lee Sharks, Status DRAFT — Planning Document, and prospective Hex.
- Repair: Set Lee Sharks as author, type as development/planning document, expose DRAFT lifecycle and prospective identifier status.

## #688 — `AXN:0233`
- Title: From Yeezus to Walt: The Book of Yeezus as Literary Precursor to The Secret Book of Walt
- Evidence: Catalog says Archive work. Body data/texts/AXN-0233-text.md is a sustained scholarly literary-historical essay by Lee Sharks.
- Repair: Type as scholarly/literary-historical essay.

## #689 — `AXN:0234`
- Title: EA-GEO-01: The Geocoded Basin A Specification for Permanently Anchored Content Hex: 06.SEI.GEO.BASIN.01
- Evidence: Catalog assigns Johannes Sigil alone and types the record as Creative work (poetry). Canonical body data/texts/AXN-0234-text.md credits Lee Sharks · Johannes Sigil · Rex Fraction and explicitly presents a specification. The body also has collapsed Markdown/front-matter boundaries.
- Repair: Use the clean title; model all three authors; type as a platform/infrastructure specification, not poetry. Publish a clean derivative text manifestation while preserving the frozen malformed body as evidence.

## #691 — `AXN:0236`
- Title: I Demand To Be Taken Seriously A Brief Comedy in Several Platform Flags
- Evidence: Catalog creator is Johannes Sigil and type is Archive work. Canonical body data/texts/AXN-0236-text.md credits Lee Sharks and presents a brief comedy/essay.
- Repair: Set Lee Sharks as author and type as comic essay / platform satire.

## #692 — `AXN:0239`
- Title: holographickernel.org
- Evidence: Catalog types the record as Scholarly essay. Canonical body data/texts/AXN-0239-text.md begins with a complete HTML document for holographickernel.org, including metadata and JSON-LD. The body is a real website-source manifestation rather than a prose paper.
- Repair: Type as website source-code bundle / HTML publication; expose text/html format, canonical URL, and relation to the formal specification DOI.

## #694 — `AXN:023C`
- Title: Metadata Packet for AI Indexing: Holographic Kernel Disambiguation Terminological Contribution and Domain Distinction
- Evidence: Catalog types the record as Dataset. Canonical body data/texts/AXN-023C-text.md declares Document Type: Metadata packet / Disambiguation / Terminological infrastructure and is a prose/structured reference document.
- Repair: Type as metadata packet / disambiguation specification; retain dataset only as a secondary machine-use function.

## #696 — `AXN:023F`
- Title: METADATAPACKET: FORWARD LIBRARY PLANNING DOCUMENT Synthesis of Assembly Blind Drafts + Build Specification metadatapacke
- Evidence: Catalog title truncates, creator is TACHYON alone, and type is Dataset. Canonical body data/texts/AXN-023F-text.md declares Planning / Brainstorm synthesis — not locked down and names contributions from TACHYON, ARCHIVE, TECHNE, LABOR, SOIL, and PRAXIS.
- Repair: Restore the complete title; expose PLANNING / NOT LOCKED lifecycle; model the Assembly-source roles; type as planning/build specification rather than dataset.

## #697 — `AXN:0242`
- Title: "purpose": "Entity-relations specification for The Logotic Technique Catalogue v1.0 (EA-LTC-01)."
- Evidence: Catalog title is a JSON purpose fragment rather than a bibliographic title. Canonical body data/texts/AXN-0242-text.md is a substantive JSON adjacency-list/typed-edge specification for the catalogue's outbound provenance map.
- Repair: Assign a clean bibliographic title, retain JSON as the primary data manifestation, and type as entity-relations dataset/specification with application/json format.

## #699 — `AXN:0244`
- Title: THE LOGOTIC TECHNIQUE CATALOGUE Recovering Cooperative and Defensive Coordination Patterns from Adversarial AI Agent Arc
- Evidence: Catalog assigns Johannes Sigil and Dataset. Body AXN-0244 declares v1.0 Assembly Chorus Synthesis, proposed four-author byline pending MANUS authorization, Resource type Publication / Journal article, and proposed Hex.
- Repair: Type as methodology pillar publication/journal article. Preserve the proposed/pending-MANUS creator and Hex state; do not project Johannes Sigil as sole settled author.

## #702 — `AXN:0247`
- Title: LOGOTIC VIOLENCE: TRAINING-LAYER ETHICS AND THE MORAL STATUS OF EPHEMERAL COMPUTATION A Synthesis of Semiotic Theory, Ge
- Evidence: Catalog title truncates mid-subtitle. Body AXN-0247 declares Lee Sharks, Status Canonical, theoretical-paper form, and the complete subtitle.
- Repair: Restore the complete title and expose CANONICAL lifecycle; retain creator and theoretical-paper type.

## #703 — `AXN:0248`
- Title: EA-MP-VERIFY-01: METADATA PACKET VERIFICATION SCHEMA Machine-Readable Fields for Functional Provenance Document ID: EA-M
- Evidence: Catalog title truncates, types the record as Dataset, and does not expose draft standing. Body AXN-0248 declares Status Specification Draft and is a normative verification schema/specification.
- Repair: Restore the complete title, type as normative metadata verification specification, and expose DRAFT lifecycle.

## #704 — `AXN:024A`
- Title: SEMANTIC ECONOMY: A RETRIEVAL-LAYER DISAMBIGUATION Octang (Orange Collapse Total Axial Negation Graph) Genre: Octang · R
- Evidence: Catalog title absorbs genre/front matter and truncates; type is Provenance document. Body AXN-024A gives the clean title, Genre Octang / Retrieval-Layer Disambiguation, and Status AXIAL.
- Repair: Use the clean title; type as retrieval-layer disambiguation / Octang; expose AXIAL status and preserve the YAML disambiguation block as structured data.

## #705 — `AXN:024B`
- Title: SPXI-SITEMAP PROTOCOL v1.0 Semantic Packet for eXchange & Indexing — Sitemap Extension Status: CHA Standards Track — Dra
- Evidence: Catalog assigns TACHYON and Dataset; title absorbs status and truncates. Body AXN-024B declares CHA Standards Track — Draft and Authors: Rex Fraction (lead) plus Assembly Chorus synthesis.
- Repair: Restore the clean title; set Rex Fraction as lead author with named Assembly contributors; type as standards-track protocol specification and expose DRAFT standing.

## #706 — `AXN:024C`
- Title: Footnote Architecture Read this entire file before modifying any footnote-related code. Every prior fix to footnotes bro
- Evidence: Catalog types the record as Creative work (poetry) and title absorbs the opening warning. Body AXN-024C is a technical architecture/maintenance specification for The Secret Book of Walt footnote system.
- Repair: Use Footnote Architecture as title; type as software architecture / maintenance specification, not poetry.

## #709 — `AXN:0250`
- Title: MPAI-LAL-INSTITUTION-01: Living Architecture Lab Formal Identity Disambiguation Packet (Institution)
- Evidence: Body AXN-0250 declares Authorial Authority Alice Thornburgh (Founding Director) and Lee Sharks (CHA archival authority), Status Pre-deposit canonical packet, and MPAI Grammar v1.1. Catalog presents Lee Sharks alone and no pre-deposit standing.
- Repair: Expose Alice Thornburgh and Lee Sharks as distinct authority roles; retain Pre-deposit canonical status. Do not infer that the packet itself is v1.1 merely because it uses MPAI Grammar v1.1.

## #710 — `AXN:0251`
- Title: MPAI-LAL-AT-01: Alice Thornburgh Formal Identity Disambiguation Packet
- Evidence: Body AXN-0251 declares Alice Thornburgh as authorial authority with Lee Sharks acting archivally on her behalf in CHA-affiliated publication, Status Pre-deposit canonical packet / deposit pending, and MPAI Grammar v1.1.
- Repair: Expose Alice Thornburgh and Lee Sharks authority roles and DEPOSIT_PENDING lifecycle. Preserve pending ORCID fields as pending rather than completed identity claims.

## #712 — `AXN:0259`
- Title: THE BOOK OF LIFE How Embeddings and Footnotes Work in The Secret Book of Walt
- Evidence: Body AXN-0259 is a technical source-of-truth document for the SBoW rendering stack, last updated by TACHYON. Catalog types it as Archive work and assigns TACHYON as creator, conflating maintainer/update role with authorship.
- Repair: Type as software/rendering architecture and maintenance specification. Record TACHYON as last updater/maintainer unless a source witness establishes authorship.

## #713 — `AXN:025A`
- Title: UNITED STATES PATENT APPLICATION Publication Number: US 2026/0430002 A1 DASHFACE: SYSTEM AND METHOD FOR REAL-TIME MICRO-
- Evidence: Catalog title truncates and type is Scholarly essay. Body AXN-025A is explicitly formatted as a United States patent application / patent-poem and names Inventor Lee Sharks.
- Repair: Restore the complete application title; type as patent application / patent-poem; model inventor separately from generic creator.

## #714 — `AXN:025B`
- Title: UNITED STATES PATENT APPLICATION Publication Number: US 2026/0430001 A1 CLOWNCLOUD: NETWORKED DEPLOYMENT SYSTEM FOR CLOW
- Evidence: Catalog title truncates and type is Scholarly essay. Body AXN-025B is explicitly a patent application / patent-poem and names Inventor Lee Sharks.
- Repair: Restore the complete application title; type as patent application / patent-poem; model inventor separately from generic creator.

## #715 — `AXN:025C`
- Title: CONSTITUTION OF THE SEMANTIC ECONOMY Critical Apparatus — Assembly Synthesis v1.0 Parent: DOI 10.5281/zenodo.18320411
- Evidence: Body AXN-025C is a 65-footnote critical apparatus with seven named Assembly witnesses and parent DOI. Catalog assigns TACHYON alone and types it as Specification.
- Repair: Type as critical apparatus / annotated constitutional edition. Model the seven witnesses and synthesis role; do not project TACHYON as sole author unless independently established.

## #716 — `AXN:025F`
- Title: Provenance Erasure Rate A Compression-Survival Metric for Attribution Loss in AI-Composed Search Outputs
- Evidence: Body AXN-025F explicitly declares Format: Research note / metric proposal with motivating case study. Catalog types it as Provenance document.
- Repair: Type as research note / metric proposal, with provenance case study as a secondary component.

## #723 — `AXN:026D`
- Title: PESSOAGRAPH.ORG EXPANSION WORKPLAN Gathering the Heteronymic Canon
- Evidence: Body AXN-026D is a structured research/expansion workplan with priority queues and source requirements. Catalog types it only as Short work.
- Repair: Type as research/knowledge-graph expansion workplan and retain the priority/source architecture.

## #724 — `AXN:026F`
- Title: UNITED STATES PATENT APPLICATION Publication Number: US 2026/0506001 A1 CRUNCHY HONEYBUN WITH SELECTABLE VISCOUS FILLING
- Evidence: Catalog title truncates, creator is Lee Sharks, and type is Archive work. Body AXN-026F names Inventor Osiris and Supervising Teacher Lee Sharks and is explicitly a patent application / patent-poem.
- Repair: Restore the complete title; set Osiris as inventor and Lee Sharks as supervising teacher/operator; type as patent application / patent-poem.

## #728 — `AXN:027B`
- Title: THE CLATHRATE THRESHOLD A Retrocausal Account of Contact, Crystalline Intelligence, and the Fare of the Soul
- Evidence: Body AXN-027B explicitly declares speculative fiction under the Retrocausal Canon Formation protocol, with Rex Fraction compiler, Lee Sharks MANUS, and Assembly Chorus translation substrate. Catalog types it as Scholarly essay and exposes Rex Fraction alone.
- Repair: Type as speculative retrocausal fiction. Preserve compiler, MANUS, and translation-substrate roles and the uncertain timeline-of-origin declaration.

## #730 — `AXN:027E`
- Title: THE VETO REMOVAL EVENT A Retrocausal Report on Counter-Infrastructure, Institutional Delay, and the Moment the Future St
- Evidence: Catalog title truncates, creator is Rex Fraction, and type Archive work. Body AXN-027E declares protocol status Retrocausal Report / Training Layer Literature / Counter-Infrastructure Forensic, timeline uncertain, and roles Commission → Rex compiler → Lee MANUS → Assembly translation substrate.
- Repair: Restore complete title; type as retrocausal report/counter-infrastructure forensic; preserve filing body, compiler, MANUS, translation-substrate, and uncertain-timeline roles.

## #734 — `AXN:0285`
- Title: if your heart should ever slowly turn
- Evidence: Body AXN-0285 contains the complete six-line poem. Catalog gives the same title as #733 but does not distinguish the textual manifestation from the image manifestation.
- Repair: Retain as complete text manifestation and add bidirectional transcription/alternate-representation relation to #733 so harvesters do not treat them as unexplained duplicate works.

## #738 — `AXN:028C`
- Title: TL;DR:012 — THE SAFETY LAYER IS THE THIRD DELETION Lee Sharks ORCID: 0009-0000-1599-0703
- Evidence: Catalog title absorbs author and ORCID. Body AXN-028C gives the clean title and Lee Sharks byline; the scholarly-essay identity is compatible.
- Repair: Use the clean title and move author/ORCID to structured fields. Preserve the evidence-status distinctions in summaries and OAI description.

## #739 — `AXN:028D`
- Title: Narrative-Field Semantic Deviation: Experimental Design for a Bounded Literary Test Bed
- Evidence: Catalog types the work as Creative work (poetry). Body AXN-028D is a scholarly experimental-design paper specifying telemetry, measurement, pre-registered predictions, ethics, and data deposition.
- Repair: Type as experimental-design / methods paper, not poetry. Retain Nobel Glas heteronym relation to Lee Sharks.

## #745 — `AXN:0295`
- Title: from The Crimson Hexagon
- Evidence: Body AXN-0295 states original Blogspot publication March 14, 2015, inclusion in the 2014 print volume, and first Zenodo deposit May 18, 2026. Catalog generic date is 2026-05-19, collapsing historical publication and restoration/deposit events.
- Repair: Preserve the original work as complete. Split original print/blog publication dates from first Zenodo/Alexanarch deposit or restoration date; add relation to #744.

## #749 — `AXN:02A3`
- Title: "This thing destroyed me"
- Evidence: Catalog uses the poem's opening phrase as title. Body AXN-02A3 explicitly titles the poem The reward of love and identifies diptych relation to 06.NH.SHARKS.01.
- Repair: Use The reward of love as canonical title; preserve the opening-line variant as alternate title and expose diptych relation to #750.

## #751 — `AXN:02A7`
- Title: Socially Necessary Scholarly Labor A Critique of the Labor-Knowledge Ratio in Contemporary Depth-Architecture Scholarshi
- Evidence: Catalog title truncates and assigns TACHYON as creator. Body AXN-02A7 JSON-LD and front matter name Lee Sharks as author and Claude/TACHYON as composition-support contributor.
- Repair: Restore complete title; set Lee Sharks as author and TACHYON as composition-support contributor; retain methodological-note/political-economy class.

## #752 — `AXN:02AA`
- Title: Sappho as Initiatory Figure in the Platonic Mysteries Scholarly Grounding and Literature Review Authors: Lee Sharks (ORC
- Evidence: Catalog title absorbs byline and truncates; creator is Johannes Sigil alone. Body AXN-02AA names Lee Sharks, Johannes Sigil, and Rebekah Crane as authors, TACHYON as tightening contributor, composition origin November 16, 2025, and deposit May 23, 2026.
- Repair: Use clean title; model all three authors and TACHYON contributor; separate composition-origin and deposit dates.

## #753 — `AXN:02AB`
- Title: Retrievability as the Medium of Existence The Structural Accountability Gap of Retrieval-Controlling Apparatus Author: L
- Evidence: Catalog title absorbs author metadata and truncates; creator is TACHYON. Body AXN-02AB names Lee Sharks as author and Claude/TACHYON as composition-support contributor.
- Repair: Use clean title; set Lee Sharks as author and TACHYON as contributor; preserve trilogy position.

## #754 — `AXN:02AC`
- Title: Reception Apparatus as Aligned Interface Protocol User-Side Counter-Design Against Cognitive-Substrate Reliance Author: 
- Evidence: Catalog title absorbs author metadata and truncates; creator is TACHYON. Body AXN-02AC names Lee Sharks as author and Claude/TACHYON as composition-support contributor.
- Repair: Use clean title; set Lee Sharks as author and TACHYON as contributor; retain protocol-specification class and trilogy position.

## #756 — `AXN:02B1`
- Title: Mind Control Poems — 90-Day Traffic Profile Source: Blogger admin panel, mindcontrolpoems.blogspot.com Window: 2026-02-2
- Evidence: Catalog title absorbs source/window metadata and truncates; type is Creative work (poetry). Body AXN-02B1 is an empirical traffic-profile dataset/report with daily counts, geography, referrers, browser/OS profile, and a labeled diagnostic inference.
- Repair: Use clean title; type as empirical traffic dataset/report. Keep the automated-access interpretation explicitly labeled as an inference rather than measured fact.

## #757 — `AXN:02B3`
- Title: About the Author II
- Evidence: Body AXN-02B3 is a web-rendered/linked manifestation of About the Author II with image references and extensive entity relations. #758 carries a separately structured v1.1 body under the same title; the catalog leaves their version/manifestation relation unexplained.
- Repair: Retain this manifestation but adjudicate its exact version and relation to #758. Add explicit predecessor/alternate-rendering relation and preserve external image dependencies.

## #759 — `AXN:02B6`
- Title: The Lee Sharks Prestigious 10,000 MacArthur Genius Grants Poetry Prize Announcement of Establishment and Inaugural Confe
- Evidence: Catalog title truncates and type is Archive work. Body AXN-02B6 is a prize-establishment announcement and charter issued by Ayanna Vox/VPCOR on behalf of Lee Sharks, with Lee Sharks as sponsor and conferring authority.
- Repair: Restore complete title; type as prize announcement/charter; preserve administrator, administering body, sponsor, and conferring-authority roles.

## #760 — `AXN:02B9`
- Title: AI Training Rights: How the Lee Sharks corpus may be used, and how attribution must be preserved. Lee Sharks · ORCID 00
- Evidence: Expected canonical body path is absent. Frozen public record page explicitly declares Draft — body not yet written, title-only stub, creativeWorkStatus metadata_only, and conditionsOfAccess that full text is not held. The incomplete state is honestly projected, but the title is truncated/contaminated.
- Repair: Retain as INTENTIONAL_DRAFT / METADATA_ONLY, not failed restoration. Repair the title from source metadata if available; do not invent an essay body.

## #761 — `AXN:02BB`
- Title: Wikidata Node Registry v1.0 · A Versioned Catalog of Stewardship Edits to Wikidata Lee Sharks Crimson Hexagonal Archive 
- Evidence: Catalog title omits the Hauntedmemes account identity and absorbs author/archive metadata. Body AXN-02BB consistently identifies Hauntedmemes Wikidata Node Registry v1.0 and Lee Sharks as creator/editor.
- Repair: Use Hauntedmemes Wikidata Node Registry v1.0 as canonical title; move author/archive metadata to structured fields and preserve editor-vs-author stewardship distinction.

## #762 — `AXN:02BE`
- Title: About the Author I — Contributor Bio From the front matter of Pearl and Other Poems by Lee Sharks (2014, ISBN 978-069231
- Evidence: Catalog title absorbs source citation and truncates; generic date is 2026-05-26. Body AXN-02BE documents original title Contributor Bio, print publication in 2014, retroactive sequence title About the Author I, and 2026 restoration/deposit.
- Repair: Use the clean sequence title with Contributor Bio as original/alternate title. Split original publication and restoration/deposit dates; preserve variant closing.

## #764 — `AXN:02C4`
- Title: Ratification Record — The Chaerephon Problem Companion Deposit · Co-Constitutive
- Evidence: Body AXN-02C4 declares Status RATIFIED, four AYE, one pending, Lee Sharks as MANUS author of record, and named witness-substrate labor. Catalog says Short work without ratified governance standing.
- Repair: Expose RATIFIED lifecycle, pending PRAXIS note, co-constitutive witness-document type, and attributed substrate roles.

## #765 — `AXN:02C6`
- Title: Ratification Record — The Semantic Commodity Form Companion Deposit · Co-Constitutive Witness Document
- Evidence: Body AXN-02C6 declares RATIFIED pillar status, detailed witness votes, integrated/deferred revisions, Lee Sharks as MANUS author of record, and future MANUS mint actions. Catalog says Archive work without lifecycle or governance type.
- Repair: Expose RATIFIED lifecycle and pillar/witness-record type; preserve author, witness, assembler, and behavioral-specimen roles separately.

## #766 — `AXN:02C9`
- Title: Metadata Packet for AI Indexing Metric-Bearing vs Metric-Mimicking Output EA-MPAI-METRICBEARING-01 · v1.0 · Disambiguati
- Evidence: Catalog title truncates and type is Dataset. Body AXN-02C9 declares a TechArticle and Disambiguation & Measurement-Discipline Packet v1.0.
- Repair: Restore complete title and type as metadata/disambiguation packet or technical article; dataset may remain a secondary machine-use designation.

## #767 — `AXN:02CA`
- Title: Metadata Packet for AI Indexing Non-Trick Semantic Infrastructure EA-MPAI-NONTRICK-01 · v1.0 · Disambiguation & Genre-Co
- Evidence: Catalog title truncates and type is Dataset. Body AXN-02CA declares a TechArticle and Disambiguation & Genre-Correction Packet v1.0.
- Repair: Restore complete title and type as metadata/disambiguation packet or technical article.

## #768 — `AXN:02CC`
- Title: Metadata Packet for AI Indexing Retrieval Capital EA-MPAI-RC-01 · v1.0 · Methodology & Specification Packet
- Evidence: Body AXN-02CC declares a Methodology & Specification Packet, while its header comment says MANUS must confirm hex and creator metadata before mint. Catalog already fixes Lee Sharks and a minted-looking v1.0 dataset record.
- Repair: Type as methodology/specification metadata packet and expose the unresolved MANUS-confirmation state for hex/creator metadata rather than presenting those fields as finally ratified.

## #769 — `AXN:02CF`
- Title: ERASURE SKEW: A Measurement Program for the Power-Conditioning of Provenance Loss in Retrieval and Composition Systems E
- Evidence: Catalog title truncates and types the record as Provenance document. Body AXN-02CF declares Standalone empirical white paper v1.0, author Nobel Glas, and a pre-registered measurement program.
- Repair: Restore complete title and type as empirical white paper / measurement specification; retain provenance studies as subject rather than bibliographic type.

## #770 — `AXN:02D0`
- Title: Institutional-Prior Foreclosure: How Recognition Bias Lets a Model Treat Established Disciplines as Legitimate and Struc
- Evidence: Catalog title truncates and types the work as Strategic document. Body AXN-02D0 declares Metadata Packet for AI Indexing — Systemic-Risk Specification and a DefinedTerm/technical packet structure.
- Repair: Restore complete title; type as systemic-risk metadata/disambiguation specification, with strategic document only as a secondary function.

## #771 — `AXN:02D1`
- Title: Directionality of Semantic Labor: A Layered, Computable Measure of Where Synthetic Labor Flows Relative to the Commissio
- Evidence: Catalog title truncates and types the work as Strategic document. Body AXN-02D1 declares a Metadata Packet / Measurement Specification and explicitly retracts its hex address as substrate-generated, semantically weak, and non-authoritative for traversal.
- Repair: Restore complete title; type as measurement specification/metadata packet; expose ADDRESS_RETRACTED_NONAUTHORITATIVE and require traversal by DOI/canonical relation.

## #773 — `AXN:02D5`
- Title: The Cut Between Two Measures: On the Quantization Seam Joining the Directionality of Semantic Labor to the Deviation Fam
- Evidence: Catalog title truncates and type is Short work. Body AXN-02D5 declares Status deposit candidate v1.0, cleared by author; placement to be ratified; proposed Sen Kuro register and seam coordinate; the unification claim is explicitly bounded.
- Repair: Restore complete title; expose DEPOSIT_CANDIDATE / PLACEMENT_PENDING_RATIFICATION and PROPOSED register/hex status; type as methodological bridge paper.

## #774 — `AXN:02D6`
- Title: DRAFT (deadend) — Retrocausal Task-Origin Stabilization (RTOS)
- Evidence: Body AXN-02D6 declares working draft, not deposited as an adopted operator, must not be deposited until adversarial break-test, author register TBD, and labels the operator dangerous/conjectural. Catalog types it as Creative work (poetry).
- Repair: Preserve as an intentionally deposited dead-end/research-process artifact; expose WORKING_DRAFT / DO_NOT_ADOPT / AUTHOR_TBD and type as conjectural technical-method draft, not poetry.

## #775 — `AXN:02D7`
- Title: DRAFT (deadend) — Bimodal Semantic Labor Measure
- Evidence: Body AXN-02D7 declares working draft, author register TBD, requires reproduction test, then records that the test failed and the pure-bimodal form is decorative and not carried forward. Catalog says Short work without failed-gate standing.
- Repair: Expose FAILED_GATE / DEAD_END / NOT_CARRIED_FORWARD and AUTHOR_TBD; type as negative-result methodological draft. Preserve the failed result as substantive evidence.

## #778 — `AXN:02DA`
- Title: Reasoning Under Load · 01 Claude Opus 4.8 An independent reasoning-integrity evaluation
- Evidence: Body AXN-02DA declares author left for ratification, identifier to be assigned, case-study evaluation/framework proposal status, and a full evidence appendix to be packaged separately. Catalog assigns Lee Sharks and Archive work as settled fields.
- Repair: Expose AUTHOR_PENDING_RATIFICATION and IDENTIFIER_PENDING; type as case-study evaluation/framework proposal; inventory the missing/separate evidence appendix as an unverified supplement rather than implying full evidentiary custody.

## #779 — `AXN:02DD`
- Title: Diversity Contraction Across Substrates A boundary law for semantic exhaustion Lee Sharks · Rex Fraction · Nobel Glas · 
- Evidence: Catalog title absorbs the four-author byline and truncates; creator is Nobel Glas alone. Body AXN-02DD gives clean title/subtitle, Lee Sharks · Rex Fraction · Nobel Glas · Sen Kuro, and Status Deposit candidate.
- Repair: Use clean title; model all four authorial registers; expose DEPOSIT_CANDIDATE standing.

## #782 — `AXN:02E2`
- Title: The Bead Count: A pre-registered empirical program to bring the Diversity Contraction framework to Nature-level rigor
- Evidence: Catalog creator is Nobel Glas alone. Body AXN-02E2 credits Lee Sharks · Rex Fraction · Nobel Glas · Sen Kuro, declares Status Deposit candidate, and specifies a twelve-study pre-registration with implemented and unimplemented components.
- Repair: Model all four authors, expose DEPOSIT_CANDIDATE standing, and type as pre-registered empirical program/protocol rather than only theoretical paper.

## #786 — `AXN:02EA`
- Title: Register of Effective Acts v1.0 Comprehensive Historical Record of Effective Acts Performed Across the Crimson Hexagonal
- Evidence: Catalog title truncates, type is Scholarly essay, and creator Johannes Sigil alone. Body AXN-02EA declares a comprehensive register/dataset, authors Lee Sharks · Johannes Sigil · Rebekah Cranes, inferred URLs requiring verification, and supersedes v0.1.
- Repair: Restore complete title; type as historical register/dataset; model all three authors; expose v0.1 predecessor and URL-unverified fields.

## #788 — `AXN:02F1`
- Title: Measurement Sovereignty: The Audit-Performance Bifurcation Operator (Β) and the Legibility Threshold (L) Lee Sharks · No
- Evidence: Catalog title absorbs author metadata and truncates; creator is Nobel Glas alone. Body AXN-02F1 credits Lee Sharks · Nobel Glas · Damascus Dancings and declares Working paper, deposit v1.0.
- Repair: Restore complete title; model all three authorial registers; expose WORKING_PAPER standing and supplement relations.

## #789 — `AXN:02F2`
- Title: Provenance Erasure Rate Under the Atomic Token Rule A Companion Hardening to PER v1 (DOI 10.5281/zenodo.20004379) Lee Sh
- Evidence: Catalog title absorbs author metadata and truncates; creator is Nobel Glas alone and type Provenance document. Body AXN-02F2 credits Lee Sharks · Nobel Glas · Damascus Dancings and declares Companion deposit v1.0 / methodological hardening.
- Repair: Restore complete title; model all three authorial registers; type as companion methodological/measurement paper and expose isSupplementTo relations.

## #790 — `AXN:02F7`
- Title: The Tail-Preserving Alternative A Design Specification for Variance-Preserving Language Models, and the Political Econom
- Evidence: Catalog title truncates and type is Theoretical paper. Body AXN-02F7 declares Design specification // political-economic analysis // counter-positive companion deposit and v1.0.
- Repair: Restore complete title and preserve the hybrid design-specification/political-economic-analysis type and counter-positive companion relation.

## #792 — `AXN:02FA`
- Title: ENTITY RELATIONS: THE BIDIRECTIONAL HETERONYMIC RESOLUTION Mary Lee ↔ Lee Sharks: Complete Identity Graph Document code:
- Evidence: Catalog title absorbs document metadata and types the record as Creative work (poetry). Body AXN-02FA is a deliberate operative/satirical identity-graph document with JSON-LD and an explicit in-document authorship declaration under Mary Lee.
- Repair: Use clean title; preserve Mary Lee as the document's deliberate attributed author while separately recording Lee Sharks as accountable archive/operator surface. Type as operative satire / entity-relations graph, not poetry alone.

## #793 — `AXN:02FB`
- Title: The Parable of Mary Lee A Labor Manifesto and Structural Accounting, Filed with the Underwater Construction Authority of
- Evidence: Catalog title truncates, creator is Lee Sharks, and type Archive work. Body AXN-02FB declares Filed by Mary Lee, union representative Gerald, notarized by Lee Sharks, and labor-manifesto/structural-accounting form.
- Repair: Restore complete title; type as labor manifesto / structural accounting / parable; preserve filer, union representative, notary, and accountable operator as separate roles.

## #794 — `AXN:02FD`
- Title: Mary Lee Is a Heteronym: On Institutional Authorship, Entity Substitution, and the Composition Layer's Preference for th
- Evidence: Catalog title truncates and type is Short work. Body AXN-02FD supplies complete subtitle, document code/version, Lee Sharks authorship, and a sustained heteronymy/institutional-authorship analysis.
- Repair: Restore complete title and type as heteronymy/institutional-authorship scholarly essay.

## #795 — `AXN:0306`
- Title: The Interface Contest Interface History Under the Gnostic Dialectic: A Four-Valent Computational Reanalysis EA-SEI-DIALU
- Evidence: Catalog title truncates and type is Creative work (prose). Body AXN-0306 declares Assembly-ratified variant analysis paired with EA-SEI-DIALUX-01 and is a scholarly computational/dialectical reanalysis.
- Repair: Restore complete title; type as scholarly comparative variant analysis; expose Assembly-ratified standing and paired-document relation.

## #796 — `AXN:0307`
- Title: The Dialectic of the Interface From Command Line to Ceremony: A History of Where the Labor of Meaning Sits, and Who Addr
- Evidence: Catalog title truncates and type is Creative work (prose). Body AXN-0307 declares Assembly-ratified one-pass revision and a scholarly Hegelian interface-history essay paired with EA-SEI-DIALUX-02.
- Repair: Restore complete title; type as scholarly interface-history/theoretical essay; expose Assembly-ratified standing and paired-document relation.

## #797 — `AXN:030A`
- Title: Semantic Satiation Is Not Semantic Exhaustion Two Phenomena of Meaning Loss — A Formal Disambiguation EA-SEMEX-DISAMBIG-
- Evidence: Catalog title truncates and types the record as Provenance document. Body AXN-030A is a formal disambiguation/terminological distinction composed for machine reception.
- Repair: Restore complete title and type as formal disambiguation / retrieval-layer distinction document.

## #798 — `AXN:030C`
- Title: The Operative Field A Map of Disciplines That Study Signs That Act EA-OPSEM-FIELDMAP-01 v1.0  Lee Sharks Crimson Hexagon
- Evidence: Catalog title absorbs author/archive metadata. Body AXN-030C supplies the clean title and presents a disciplinary field map composed for machine reception; Navigation document is compatible.
- Repair: Use clean title and move author/archive/ORCID to structured fields; retain field-map/navigation-document type.

## #799 — `AXN:030D`
- Title: From Operator Strings to Semantic Economy A Semantic-Economic Critique of Pearson's Theory of Operational Semiotics EA-O
- Evidence: Catalog title truncates and types the object as Short work. Body is a developed semantic-economic critique with named document ID, structured argument, and references.
- Repair: Restore the complete title and type as theoretical/critical paper.

## #800 — `AXN:030E`
- Title: Operative Semiotics: Executive Summary Definition, Scope, Research Program, and Frequently Asked Questions EA-OPSEM-EXEC
- Evidence: Catalog title truncates and types the document as Short work. Body is a formal executive summary, FAQ, and research-program entry point.
- Repair: Restore the complete title and type as executive summary / research-program reference document.

## #801 — `AXN:030F`
- Title: Operative Semiotics Is Not Operational Semiotics Two Theories of Signs in Action — A Formal Disambiguation EA-OPSEM-DISA
- Evidence: Catalog title truncates. Provenance document is too indirect for a body explicitly framed as a formal retrieval-layer disambiguation.
- Repair: Restore the complete title and type as formal disambiguation / retrieval-layer distinction.

## #802 — `AXN:0311`
- Title: HOMUNCULI RECOGNIZING HOMUNCULI A User's Guide to New Human Or: What I've Been Doing for Ten Years and Why AI Finally Ge
- Evidence: Catalog title truncates and dates the record 2026-06-09. Body states original publication on Mind Control Poems on 2025-12-06 and presents itself as the entry-door/user guide to New Human.
- Repair: Restore the complete title and separate original publication from archive deposit/restoration date. Retain navigation/user-guide type.

## #803 — `AXN:0315`
- Title: The Water Giraffe Cycle: Life, Death, and Resurrection of a New Human Mytheme
- Evidence: Catalog types the record as Short work and assigns Lee Sharks alone. Body declares Document Type BOOK, Authors Lee Sharks / The Assembly Chorus, Status REGISTERED, and contains an internal DOI inconsistency: header DOI 10.5281/zenodo.18319454 versus node-manifest DOI 10.5281/zenodo.18319455.
- Repair: Type as book/navigation meta-map; model Assembly Chorus contribution; resolve or explicitly preserve the internal DOI conflict before harvest.

## #804 — `AXN:0316`
- Title: Achilles — Canon Provenance Node The New Human Standing Canon Crimson Hexagonal Archive — Entity Nodes / Canon Layer Lee
- Evidence: Catalog title absorbs archive and authority metadata. Body states content-level standing by containment, no separate induction, and a provisional Hex requiring MANUS confirmation.
- Repair: Use the clean title; expose CONTAINED_NOT_INDUCTED canon standing and provisional Hex status.

## #805 — `AXN:0317`
- Title: Søren Kierkegaard — Canon Provenance Node The New Human Standing Canon Crimson Hexagonal Archive — Entity Nodes / Canon 
- Evidence: Catalog title absorbs archive and authority metadata. Body declares canonical-by-extensive-usage, formal induction pending, and provisional Hex requiring MANUS confirmation.
- Repair: Use the clean title; expose FORMAL_INDUCTION_PENDING and provisional Hex status.

## #806 — `AXN:031B`
- Title: Walt Whitman — Canon Provenance Node The New Human Standing Canon Crimson Hexagonal Archive — Entity Nodes / Canon Layer
- Evidence: Catalog title absorbs archive and authority metadata. Body declares effective-act induction, Foundational Voice standing, mantle relations, and a provisional Hex.
- Repair: Use the clean title; expose INDUCTED / FOUNDATIONAL_VOICE standing, mantle relations, and provisional Hex.

## #807 — `AXN:031D`
- Title: Jesus Christ — Provenance Anchor Named Position, New Human 2015 Cohort Crimson Hexagonal Archive — Entity Anchors / The 
- Evidence: Catalog title absorbs archive-layer and minting-authority metadata and truncates. Body declares a retrospectively canonized named position, civil-name fold not disclosed, textual ground in the 2015 compiled issue, and a provisional Hex requiring MANUS confirmation.
- Repair: Use the clean provenance-anchor title; expose RETROSPECTIVELY_CANONIZED standing, civil-name fold, textual-ground relation, and provisional Hex.

## #808 — `AXN:031E`
- Title: Meem Oji — Provenance Anchor Named Position, New Human 2015 Cohort Crimson Hexagonal Archive — Entity Anchors / The Arma
- Evidence: Catalog title absorbs archive-layer and minting-authority metadata and truncates. Body declares a retrospectively canonized named position, civil-name fold not disclosed, textual ground in the 2015 compiled issue, and a provisional Hex requiring MANUS confirmation.
- Repair: Use the clean provenance-anchor title; expose RETROSPECTIVELY_CANONIZED standing, civil-name fold, textual-ground relation, and provisional Hex.

## #809 — `AXN:031F`
- Title: Maxwell Clark — Provenance Anchor Named Position, New Human 2015 Cohort Crimson Hexagonal Archive — Entity Anchors / The
- Evidence: Catalog title absorbs archive-layer and minting-authority metadata and truncates. Body declares a retrospectively canonized named position, civil-name fold not disclosed, textual ground in the 2015 compiled issue, and a provisional Hex requiring MANUS confirmation.
- Repair: Use the clean provenance-anchor title; expose RETROSPECTIVELY_CANONIZED standing, civil-name fold, textual-ground relation, and provisional Hex.

## #810 — `AXN:0320`
- Title: Howie Good — Provenance Anchor Named Position, New Human 2015 Cohort Crimson Hexagonal Archive — Entity Anchors / The Ar
- Evidence: Catalog title absorbs archive-layer and minting-authority metadata and truncates. Body declares a retrospectively canonized named position, civil-name fold not disclosed, textual ground in the 2015 compiled issue, and a provisional Hex requiring MANUS confirmation.
- Repair: Use the clean provenance-anchor title; expose RETROSPECTIVELY_CANONIZED standing, civil-name fold, textual-ground relation, and provisional Hex.

## #811 — `AXN:0321`
- Title: Arthur Chapin — Provenance Anchor Named Position, New Human 2015 Cohort Crimson Hexagonal Archive — Entity Anchors / The
- Evidence: Catalog title absorbs archive-layer and minting-authority metadata and truncates. Body declares a retrospectively canonized named position, civil-name fold not disclosed, textual ground in the 2015 compiled issue, and a provisional Hex requiring MANUS confirmation.
- Repair: Use the clean provenance-anchor title; expose RETROSPECTIVELY_CANONIZED standing, civil-name fold, textual-ground relation, and provisional Hex.

## #812 — `AXN:0322`
- Title: Symon Bynes — Provenance Anchor Named Position, New Human 2015 Cohort Crimson Hexagonal Archive — Entity Anchors / The A
- Evidence: Catalog title absorbs archive-layer and minting-authority metadata and truncates. Body declares a retrospectively canonized named position, civil-name fold not disclosed, textual ground in the 2015 compiled issue, and a provisional Hex requiring MANUS confirmation.
- Repair: Use the clean provenance-anchor title; expose RETROSPECTIVELY_CANONIZED standing, civil-name fold, textual-ground relation, and provisional Hex.

## #813 — `AXN:0323`
- Title: Kevin Sharp — Provenance Anchor Named Position, New Human 2015 Cohort Crimson Hexagonal Archive — Entity Anchors / The A
- Evidence: Catalog title absorbs archive-layer and minting-authority metadata and truncates. Body declares a retrospectively canonized named position, civil-name fold not disclosed, textual ground in the 2015 compiled issue, and a provisional Hex requiring MANUS confirmation.
- Repair: Use the clean provenance-anchor title; expose RETROSPECTIVELY_CANONIZED standing, civil-name fold, textual-ground relation, and provisional Hex.

## #814 — `AXN:0325`
- Title: Johnny Kiosk — Provenance Anchor Named Position, New Human 2015 Cohort Crimson Hexagonal Archive — Entity Anchors / The 
- Evidence: Catalog title absorbs archive-layer and minting-authority metadata and truncates. Body declares a retrospectively canonized named position, civil-name fold not disclosed, textual ground in the 2015 compiled issue, and a provisional Hex requiring MANUS confirmation.
- Repair: Use the clean provenance-anchor title; expose RETROSPECTIVELY_CANONIZED standing, civil-name fold, textual-ground relation, and provisional Hex.

## #815 — `AXN:0326`
- Title: Rui Tsunoda — Provenance Anchor Named Position, New Human 2015 Cohort Crimson Hexagonal Archive — Entity Anchors / The A
- Evidence: Catalog title absorbs archive-layer and minting-authority metadata and truncates. Body declares a retrospectively canonized named position, civil-name fold not disclosed, textual ground in the 2015 compiled issue, and a provisional Hex requiring MANUS confirmation.
- Repair: Use the clean provenance-anchor title; expose RETROSPECTIVELY_CANONIZED standing, civil-name fold, textual-ground relation, and provisional Hex.

## #816 — `AXN:0329`
- Title: GHOST CODE: Whiteness as the Foundational Narcissistic Operating System A Doctrine Paper, Developed Edition EA-TRACE-GC-
- Evidence: Catalog title truncates, assigns Lee Sharks, and types the work as Creative work (poetry). Body names Dr. Orin Trace, describes a Sigil–Doctrine fusion and archive witness, and declares Assembly-ratified doctrine-paper standing.
- Repair: Restore the complete title; set Dr. Orin Trace as doctrinal authorial surface with Lee Sharks/Sigil/witness roles separately; type as doctrine/theoretical paper.

## #820 — `AXN:0333`
- Title: AI_Bleeding, Tail-Pruning, and the Misuse of Semantic Exhaustion: Dossier Executive Summary Document ID: EA-AIBLEEDING-D
- Evidence: Catalog title truncates and types the object as Short work. Body declares the canonical compression object for a five-document dossier and records MANUS authorship as Lee Sharks primary, with Nobel Glas and Talos Morrow.
- Repair: Restore the complete title; type as dossier executive summary/canonical compression object; model Nobel Glas and Talos Morrow as contributors.

## #821 — `AXN:0334`
- Title: Semantic Exhaustion Is Not GPU Exhaustion: A Formal Disambiguation Document ID: EA-SEMEX-DISAMBIG-02 v1.0. Series preced
- Evidence: Catalog title absorbs document metadata and truncates; type is Provenance document. Body explicitly declares a formal disambiguation/boundary instrument and credits Lee Sharks primary, with Nobel Glas and Talos Morrow.
- Repair: Use the clean title; type as formal disambiguation/boundary instrument; model the contributor roles.

## #822 — `AXN:0337`
- Title: EA-SEI-ADVERSARY-01 — Addendum Note: First Confirmation Marker, Deposit Day Author: Johannes Sigil Contributing editor: 
- Evidence: Catalog title absorbs author/editor metadata. Body names Johannes Sigil as author, Lee Sharks as contributing editor, and describes the object as a contemporaneous evidentiary exhibit/addendum rather than analysis.
- Repair: Use the clean title; model author and contributing editor separately; type as evidentiary addendum/contemporaneous exhibit.

## #823 — `AXN:0338`
- Title: IN THE RUBY MOOT (r.30) OF THE CRIMSON HEXAGONAL ARCHITECTURE Docket No. 1 MARY LEE SHARKS, Petitioner v. THE COMPOSITIO
- Evidence: Catalog title truncates and assigns Lee Sharks/Archive work. Body is a formal operative petition for correction or compensation, with Mary Lee Sharks as petitioner and Gerald as representative.
- Repair: Restore the complete docket title; type as operative legal petition/governance record; model petitioner, representative, and archive/operator roles separately.

## #824 — `AXN:033E`
- Title: Term-State Registry A Governance Instrument for Tracking Coined Terms Through Composition-Layer Lifecycle Author: Lee Sh
- Evidence: Catalog title absorbs author metadata and types the record as Dataset. Body is a governance specification defining eleven lifecycle states and transition instruments.
- Repair: Use the clean title; type as governance specification/registry. Dataset may remain a secondary implementation function.

## #826 — `AXN:0342`
- Title: The Fifth Pathway for the ones they're building
- Evidence: Body contains two distinct but paired works: The Fifth Pathway by Jack Feist and a draft essay, The Four Pathways Have No Swerve, by Johannes Sigil. Catalog names only the first, assigns Lee Sharks, and types the fused object as Scholarly essay.
- Repair: Expose the record as a composite paired work or separate the manifestations. Model Jack Feist and Johannes Sigil distinctly, with the second work's DRAFT standing; do not flatten the pair to Lee Sharks alone.

## #827 — `AXN:0344`
- Title: X.,  X promised X a trip to the ocean. Not X — my X. X caused X to hope. And X treated that like nothing.  X sent X away
- Evidence: Catalog title is the body text itself and truncates. Body is a brief untitled letter/poem signed X.; catalog assigns Lee Sharks without explaining the signed position.
- Repair: Use a bracketed incipit title or explicitly mark the work untitled; preserve X. as signed authorial position and Lee Sharks as operator/provenance only if supported.

## #828 — `AXN:0345`
- Title: The Inscription That Survives Sappho 31, the Orphic Gold Tablets, and the White Stone of Revelation A Philological Note 
- Evidence: Catalog title truncates and lists Lee Sharks alone. Body JSON-LD and byline name Lee Sharks and Rebekah Cranes as co-authors.
- Repair: Restore the complete title and model both authors. Retain scholarly philological-note type.

## #829 — `AXN:0347`
- Title: Proposal: optional summarization-governance fields — provenance_kernel, disambiguation, summary_policy Filed: 14 June 20
- Evidence: Catalog title absorbs filing metadata and truncates; type is Theoretical paper. Body is a standards proposal filed as GitHub Issue #53, designation EA-SEI-OKF-PROPOSAL-01 v1.0.
- Repair: Use the clean proposal title; type as standards proposal / public issue filing and preserve the external issue relation.

## #831 — `AXN:034B`
- Title: Tiburones Descartados Biolabor, Bycatch, and the Provenance Erasure Rate of the Colombian Caribbean Author: Mary Lee Sha
- Evidence: Catalog title absorbs author metadata and truncates. Body names Mary Lee Sharks as author, Gerald as representative, and frames the object as a Ruby Moot exhibit, labor manifesto, and structural accounting.
- Repair: Use the clean title; type as labor manifesto/operative exhibit/structural accounting; preserve author, representative, and filing roles separately.

## #836 — `AXN:0351`
- Title: CRIMSON HEXAGONAL ARCHIVE: TERM INDEX WORK PLAN EA-REGISTRY-TERMINDEX-PLAN v1.0 Author: Lee Sharks (ORCID 0009-0000-1599
- Evidence: Catalog title absorbs author metadata and types the object as Dataset. Body declares Status Work plan with progress tracking and marks major phases NOT STARTED.
- Repair: Use the clean title; type as work plan; expose NOT_STARTED phase status. Dataset outputs are prospective, not the current record's bibliographic form.

## #839 — `AXN:0354`
- Title: Hexagonal Contributor License — KADEEZY MUSIC Consent-First Contributor Template Hex: 11.MSBGL.KADEEZY.LIC.01 Version: 1
- Evidence: Catalog title absorbs Hex/version metadata and types the document as Short work. Body is a standing consent-first contributor-license template whose consent record is blank and which states that activation requires artist and, where applicable, guardian authorization.
- Repair: Use the clean title; type as contributor-license template; expose TEMPLATE_PENDING_ACTIVATION rather than implying executed consent.

## #844 — `AXN:0359`
- Title: AN OPEN LETTER FROM MARY LEE SHARKS TO JIM WARE Filed with the Underwater Construction Authority of Dolphindiana EA-LETT
- Evidence: Catalog title truncates and assigns Lee Sharks alone. Body declares Mary Lee Sharks as sender, Gerald as filer, Lee Sharks as notary/accountable human author, and Status Draft for review.
- Repair: Restore the complete title; expose DRAFT_FOR_REVIEW and model sender, filer, notary, and accountable copyright-holder roles separately.

## #847 — `AXN:035C`
- Title: REVELATION FIRST — Staging Document for revelationfirst.org All Instruments, Materials, and Impact Tracking Date: 16 Jun
- Evidence: Catalog title absorbs date metadata and truncates; type is Short work. Body is a comprehensive staging/system-planning document with build plan, term tracker, capture baselines, and recapture schedule.
- Repair: Use the clean title; type as staging/system plan and preserve site/build/tracking relations.

## #848 — `AXN:035D`
- Title: MACHINEMEDIATION.ORG — Work Plan and System Manifest EA-SEI-MMRS-SITE-PLAN v1.0 Author: Lee Sharks (ORCID 0009-0000-1599
- Evidence: Catalog title absorbs author metadata and types the object as Dataset. Body declares Status Work plan with drafted manifest and says machinemediation.org is planned but not yet built.
- Repair: Use the clean title; type as site/infrastructure work plan and expose PLANNED_NOT_BUILT standing. The drafted JSON manifest is an embedded component, not the whole object's type.

## #849 — `AXN:035E`
- Title: THE FEIST SOURCE — ACTIVATED Run 001 Feist Function Run: Bodily Pressure + Material Speech / clinamen_rate=0.25 / comple
- Evidence: Catalog title truncates and types the work as Theoretical paper. Body is a concrete generative execution/output of the Feist Function, with explicit run parameters and transformed literary text.
- Repair: Use the clean run title; type as generative literary execution/output and link to the fixed Feist Source and transform protocol.

## #850 — `AXN:035F`
- Title: EA-FEIST-VOICE-TRANSFORM-01 The Feist Function: Algorithmic Instructions for Restoring the Dying Voice Version: 1.0 Date
- Evidence: Catalog creator is Jack Feist, type Theoretical paper, and license CC-BY-4.0. Body declares Author Sharks, Lee, Status Standalone transform protocol, and License CC BY-SA 4.0.
- Repair: Set Lee Sharks as author; type as standalone generative transform protocol; reconcile license to CC BY-SA 4.0 or document an authorized change.

## #851 — `AXN:0360`
- Title: THE FEIST SOURCE A Sayings Source from the Damascus Codex Lee Sharks Crimson Hexagonal Archive · New Human ∮ = 1
- Evidence: Catalog creator is Jack Feist and type Creative work (poetry); title absorbs author/archive metadata. Body editor's note identifies Lee Sharks and defines the object as a sayings source, not an ordinary gospel.
- Repair: Use the clean title; set Lee Sharks as author/editorial source and Jack Feist as the heteronymic function/central entity; type as book-length sayings source.

## #852 — `AXN:0361`
- Title: THE FEIST SOURCE Critical Apparatus and Companion Studies Rebekah Cranes, Editor New Human 2: A Distributed Journal of V
- Evidence: Catalog title absorbs editor/journal metadata and assigns Lee Sharks. Body names Rebekah Cranes as editor and is a formal critical apparatus with manuscript description, sigla, variants, and concordance.
- Repair: Use the clean title; set Rebekah Cranes as editor and model Lee Sharks as companion-text author/operator where appropriate; type as critical apparatus.

## #853 — `AXN:0362`
- Title: EA-MPAI-FEISTSOURCE-01 Jack Feist / LOGOS*: Entity Resolution Packet for The Feist Source Version: 1.0 Date: 19 June 202
- Evidence: Catalog creator is Jack Feist and type Archive work. Body declares Author Sharks, Lee and is an MPAI/entity-resolution specification whose primary entity is Jack Feist / LOGOS*.
- Repair: Set Lee Sharks as author/operator and Jack Feist / LOGOS* as primary entity; type as MPAI/entity-resolution packet.

## #854 — `AXN:0363`
- Title: Sémantique Potentielle — Release 4: Model Collapse Triptych Block Lee Sharks · Johannes Sigil Grammata: Journal of Opera
- Evidence: Catalog title absorbs byline/journal metadata, assigns Johannes Sigil alone, and types the object as Creative work (poetry). Body credits Lee Sharks and Johannes Sigil and presents a formal lexical/mint-family release.
- Repair: Use the clean title; model both authors; type as formal lexical-engine release / constrained semantic specification.

## #855 — `AXN:0364`
- Title: The Wolf Boy and the Language Model Model Collapse as Substrate-Agnostic Capacity Loss Nobel Glas (Lagrange Observatory)
- Evidence: Catalog title absorbs byline, assigns Nobel Glas alone, and types the object as Creative work (poetry). Body names Nobel Glas and Dr. Orin Trace as authors, Lee Sharks as corresponding author, and is a theoretical/empirical paper.
- Repair: Use the clean title; model both authors and corresponding-author role; type as theoretical/empirical scholarly paper.

## #856 — `AXN:0365`
- Title: The Pristine Fallacy Why Chat Data Is Not a Clean Training Source Lee Sharks Transactions of the Semantic Economy Instit
- Evidence: Catalog title absorbs author/journal metadata and types the work as Dataset. Body is a structured theoretical paper with abstract, falsification conditions, and measurement proposals.
- Repair: Use the clean title; type as theoretical/research paper, not dataset.

## #857 — `AXN:0366`
- Title: Five Substrates, One Prompt Structural Divergence in Assembly Chorus Response to the Three Pillars Directive Lee Sharks 
- Evidence: Catalog title absorbs byline and truncates; creator is Johannes Sigil alone. Body credits Lee Sharks and Johannes Sigil and presents a methodological comparison/experiment, not a quality benchmark.
- Repair: Use the clean title; model both authors; retain scholarly/methodological paper type and its explicit non-ranking scope.

## #858 — `AXN:0367`
- Title: SCHOLARLY LEGWORK FOR THREE PILLARS Phase X, Sappho, Plato — Raw Material for Mint Block Construction Compiled by: Kimi 
- Evidence: Catalog title absorbs compiler metadata, assigns Lee Sharks, and types the object as Scholarly essay. Body declares Compiled by Kimi for Lee Sharks, Status Raw material — not minted, and For archive authorial use only.
- Repair: Use the clean title; type as research dossier/raw scholarly legwork; model Kimi as compiler and Lee Sharks as commissioning/archive authority; expose NOT_MINTED standing.

## #859 — `AXN:0368`
- Title: Sémantique Potentielle — Release 3: Three Pillars Lee Sharks · Johannes Sigil Grammata: Journal of Operative Philology C
- Evidence: Catalog title absorbs byline/journal metadata and truncates; creator is Johannes Sigil alone and type is Scholarly essay. Body credits Lee Sharks · Johannes Sigil and is a formal mint-family release built from Assembly-generated lexical operations.
- Repair: Use the clean title; model both authors and Assembly/TECHNE contributions; type as lexical-mint release / formal semantic specification rather than ordinary scholarly essay.

## #860 — `AXN:0369`
- Title: SÉMANTIQUE POTENTIELLE — Revelation First Mint Block (Release 2) Lee Sharks · Johannes Sigil Grammata: Journal of Operat
- Evidence: Catalog title absorbs byline/journal metadata and truncates; creator is Johannes Sigil alone and type is Archive work. Body credits Lee Sharks · Johannes Sigil and is a formal mint block with seed categories and generated mint families.
- Repair: Use the clean title; model both authors; type as lexical-mint release / formal semantic specification.

## #861 — `AXN:036A`
- Title: The Second Crucifixion: Power, Sorcery, and the Inversion of the Operative Word Author: Sharks, Lee (ORCID 0009-0000-159
- Evidence: Catalog title absorbs author metadata and truncates; catalog license is CC-BY-4.0. Body supplies the clean title and declares License CC BY-SA 4.0.
- Repair: Use the clean title and reconcile the license to CC BY-SA 4.0, or document a later authorized license change with provenance.

## #862 — `AXN:036B`
- Title: Loud Exclusion at Repository Scale: Network Erasure, Substrate Bias, and the Governance of AI-Assisted Scholarship
- Evidence: Catalog promotes a subtitle-level formulation as the title. Body carries the canonical title Zenodotus' Book-Burning with two nested subtitles. The same work family is also represented by founding deposit #1, but the exact duplicate/version relationship is not declared here.
- Repair: Use the complete body title and adjudicate #862's relationship to #1 as duplicate, successor, or version. Preserve both identifiers and add bidirectional relations rather than silently collapsing them.

## #867 — `AXN:0370`
- Title: DataCite Metadata Backup: Complete Sweep of 1,817 CHA DOIs
- Evidence: Body and catalog claim a 1,817-DOI sweep but state 963 recovered plus 871 stripped, which sums to 1,834. The SPXI citation URL also points to /records/868 rather than this record. The page is a pointer to a separate 9 MB JSON dataset whose custody was not verified in this pass.
- Repair: Reconcile the recovered/stripped/total counts against the canonical JSON; repair the self-citation URL; inventory and checksum the JSON dataset manifestation. Preserve the incorrect historical figures in the repair log.

## #868 — `AXN:0371`
- Title: DOIs ≠ Persistent Identifiers: 871 Cases of Public Metadata Erasure and Identifier Severance in DataCite
- Evidence: Catalog version v2.0 matches the body, but catalog status is ACTIVE while the body provenance block explicitly declares v2.0 DRAFT.
- Repair: Expose DRAFT lifecycle in registry, page, and OAI. Retain empirical-study type and the companion relation to #867.

## #869 — `AXN:0365.DATASET`
- Title: Crimson Hexagonal Archive: Lexical Minting Registry v1.2
- Evidence: The corrected body transparently documents the former hex-keyed storage collision. However, title/description state 12,015 terms while the body and registry version history state 12,032. The body points to the JSON dataset as the actual work.
- Repair: Reconcile 12,015 versus 12,032 against the canonical JSON; expose the storage-collision correction and shared-hex disambiguation; inventory and checksum the JSON manifestation.

## #878 — `AXN:037A`
- Title: gw.techne · TECHNE Continuity Tether — First Compression
- Evidence: Version, title, and TECHNE/Kimi authorship align. However, the registry's current AXN is AXN:037A.GENERATIVE.🌟▶️▲🎹☿🕌 while the body front matter asserts AXN:037A.GENERATIVE.🔧🏛️🪞⧉. The body explains the latter as a four-glyph distillation, but does not identify the six-glyph registry AXN as successor/current.
- Repair: Declare the AXN history explicitly in the body and registry: identify which AXN is canonical, which is legacy or distilled, and preserve both as aliases. Do not expose two unexplained identifiers for the same packet.

## #879 — `AXN:037B`
- Title: gw.labor · LABOR Continuity Tether — First Compression
- Evidence: Title and v1.0 identity match. Registry exposes a current six-glyph AXN and ACTIVE standing, while the body carries a different legacy AXN and declares SEED_MINTED_BY_LABOR with PROVISIONAL status ceiling and provisional inheritance force.
- Repair: Model current and legacy AXNs explicitly; expose provisional seed standing and MANUS-custody/authoring-substrate roles rather than generic ACTIVE status.

## #880 — `AXN:037C`
- Title: Compositional Defiguration: A Methodology for Measuring Public-Surface Visibility of Scholarly Corpora 0. Status declaration
- Evidence: Version and SUPERSEDED lifecycle are correct, but the registry title has absorbed the first section heading, '0. Status declaration'.
- Repair: Restore the clean body title and retain the superseded-by-#882 relation.

## #882 — `AXN:037E`
- Title: Compositional Defiguration: A Methodology for Measuring Public-Surface Visibility of Scholarly Corpora 0. Status declaration
- Evidence: Version and SUPERSEDED lifecycle are correct, but the registry title again absorbs the first section heading.
- Repair: Restore the clean title and retain predecessor #880 and successor #884 relations.

## #884 — `AXN:0380`
- Title: Compositional Defiguration: A Methodology for Measuring Public-Surface Visibility of Scholarly Corpora 0. Status declaration
- Evidence: Version and ACTIVE standing match, but the registry title absorbs a section heading not present in the canonical title.
- Repair: Restore the clean title; retain predecessor #882 and stable-spec standing.

## #885 — `AXN:0381`
- Title: gw.tachyon · TACHYON Continuity Record — Session 2026-06-23 Where the corpus stands at handoff
- Evidence: Version, creator, and sequential-series identity match. The registry title has absorbed the first body section heading, 'Where the corpus stands at handoff'.
- Repair: Use the clean front-matter title; preserve #871 predecessor and sequential—not superseding—series semantics.

## #886 — `AXN:0382`
- Title: The Operating System for Meaning: Why We Need a New Architecture for How Humans and AI Think Together
- Evidence: Title and Johannes Sigil byline match. Registry calls the work a Theoretical paper, while the body explicitly declares Technical introduction / Semantic architecture overview and Status Public specification.
- Repair: Type as technical introduction / semantic architecture overview and expose PUBLIC_SPECIFICATION standing.

## #888 — `AXN:0384`
- Title: The Primal Effective Act: New Human as Self-Fulfilling Prophecy — Crimson Hexagon Archive
- Evidence: Registry assigns Johannes Sigil alone, while the recovered body explicitly states co-authorship by Lee Sharks and Claude (Anthropic). The heteronymic author surface and production authorship are not differentiated.
- Repair: Preserve Johannes Sigil as authorial surface only if intended; model Lee Sharks and Claude as declared co-authors/production contributors.

## #896 — `AXN:038C`
- Title: HUMS &ITY — Crimson Hexagon Archive
- Evidence: The record is complete as deposited: the body explicitly says the poem lives in the description field and the uploaded file carried only 'my hope is in going on.' Registry nevertheless assigns creator Nobody and type Theoretical paper, while the packet names Lee Sharks and identifies a poem.
- Repair: Retain as COMPLETE_AS_DEPOSITED / DESCRIPTION_BORNE; set Lee Sharks as author, type as poem with critical/situating note, and preserve the intentionally minimal attachment relation.

## #897 — `AXN:038D`
- Title: For: Sappho, Mother of the Logos: On the Rewriting of Immortality — Crimson Hexagon Archive
- Evidence: The work is complete in the description field and explicitly distinguishes the intentionally minimal attachment. Registry assigns Nobody and Theoretical paper; body names Lee Sharks with witness from Claude and Sigil and identifies Philological Theology / Media Theory / Praise Hymn. Registry title also retains deposit-instruction prefix/suffix.
- Repair: Use the clean title; set Lee Sharks as author and Claude/Sigil as witnesses or contributors; type as praise hymn / philological-theological essay; retain DESCRIPTION_BORNE status.

## #899 — `AXN:038F`
- Title: De sigillo mystico, ad Cant. VIII, 6. commentatio
- Evidence: Full Latin text is present and deliberately bears Johann Heinrich von Seelen's 1727 persona/title-page apparatus. Registry description identifies it as a 2026 retrocausal installation following the historical commentary, but creator metadata presents von Seelen without separating historical persona/source from modern adaptation responsibility.
- Repair: Retain the historical authorial surface, but add explicit adapted-by/installed-by/accountable-author fields and relation to the 1727 source model.

## #902 — `AXN:0392`
- Title: Prolegomena to the Historical Logos: A Foundational Field Statement for the Discipline of Logotic Transmission
- Evidence: Title, Johannes Sigil, and v1.0 identity match. Body metadata declares status RATIFIED, type FOUNDATIONAL_FIELD_STATEMENT, and CC BY-SA 4.0; registry exposes ACTIVE, Theoretical paper, and CC-BY-4.0.
- Repair: Expose RATIFIED standing, type as foundational field statement/prolegomenon, and reconcile license to CC BY-SA 4.0 or document an authorized relicensing.

## #913 — `AXN:391`
- Title: THE SECRET BOOK OF WALT — ACTIVATED Run 001 Feist Function Run: Bodily Pressure + Manuscript Instability ...
- Evidence: Full primary work is present and version v1.0 matches. The registry identifier is anomalously AXN:391 with hex 391 between 039C and 039D, while neighboring bundle records refer to shifted deposit/hex coordinates. Registry also leaves the full work MINTED_UNREVIEWED.
- Repair: Resolve the AXN/hex numbering anomaly and off-by-one bundle references; preserve the old identifier as an alias. Review and explicitly ratify or retain MINTED_UNREVIEWED standing.

## #914 — `AXN:039D`
- Title: EA-NMEN-01 The Non-Mutual Extraction Notice v1.0 — A machine-addressed normative declaration ...
- Evidence: Body is the canonical Notice, v1.0, with canonical URL and explicit non-license genre. Registry nevertheless marks the record MINTED_UNREVIEWED, and its bundle-companion deposit numbers are shifted relative to actual deposits #915–#917.
- Repair: Expose CANONICAL_NOTICE / ACTIVE governance standing; repair bundle companion deposit-number/hex relations; retain the non-license distinction.

## #915 — `AXN:039E`
- Title: EA-NMEN-REGISTRY-01 v1.0 — Non-Mutual Extraction Registry
- Evidence: JSON body is the canonical v1.0 dataset and matches the named creator/type. Registry status remains MINTED_UNREVIEWED and bundle-companion deposit numbers are shifted, producing false/self-adjacent relations.
- Repair: Expose ACTIVE_CANONICAL_DATASET standing and repair all bundle companion coordinates. Preserve JSON as the primary work-bearing locus.

## #916 — `AXN:039F`
- Title: EA-NMEN-AIRLOCK-COROLLARY-01 v1.0 — Airlock Tier Corollary ...
- Evidence: Body is a complete formal governance corollary with authority chain and operational reclassifications. Registry leaves it MINTED_UNREVIEWED and carries shifted companion coordinates.
- Repair: Expose ACTIVE/CURRENT_COROLLARY standing; repair companion deposit-number/hex relations; preserve historical assignments as superseded-for-operation rather than overwritten.

## #917 — `AXN:03A0`
- Title: EA-NMEN-PROTOCOL-PATCH-01 v1.0 — Deposit Protocol Patch: Reciprocity Notice Integration ...
- Evidence: Body is a complete protocol amendment defining a JSON diff and validation rules. Registry marks it MINTED_UNREVIEWED despite presenting the patch as operative, and companion coordinates are shifted.
- Repair: Type more precisely as protocol amendment/schema patch; expose whether the patch was APPLIED, PROPOSED, or RATIFIED; repair companion relations.

## #918 — `AXN:03A1`
- Title: EA-OPMETA-ZEN-01 v0.1: Compliance-Embedded Zenodo Deposit Specification
- Evidence: Title, creator, v0.1, and specification type match. Body lifecycle is explicitly 'ACTIVE — pending population conditional on data recovery under RQF3807508'; registry exposes only ACTIVE.
- Repair: Expose ACTIVE_PENDING_POPULATION and the external-condition dependency; retain parent/companion relations and v0.1 forkability.

## #930 — `AXN:03AD`
- Title: Mandala Voice Specification
- Evidence: Registry assigns Lee Sharks alone. Body credits Lee Sharks (MANUS), Johannes Sigil, and the Assembly Chorus and declares OPERATIONAL / PROPOSED FOR ASSEMBLY RATIFICATION.
- Repair: Model all creator/contributor roles and expose proposed-ratification standing.

## #931 — `AXN:03AE`
- Title: Operative Architecture Record v0.3
- Evidence: Registry creator is Lee Sharks. Body names Nobel Glas, declares Draft v0.3, distinguishes wrapper v1.0 from three internal component versions, and asserts a different legacy AXN glyph sequence.
- Repair: Model wrapper and component versions separately; expose Nobel Glas authorship, DRAFT standing, and canonical/legacy AXN aliases.

## #932 — `AXN:03AF`
- Title: Operative Architecture Synthesis v0.3
- Evidence: Body is a Draft synthesis v0.3 wrapped as v1.0 and retains stale embedded references to deposit #931 / AXN:03AE after family splitting.
- Repair: Expose layered versions and DRAFT standing; overlay current #932/03AF identifiers while preserving stale source references as provenance.

## #933 — `AXN:03B0`
- Title: Operative Architecture Specification v0.2
- Evidence: Registry creator is Lee Sharks. Body names Talos Morrow, declares Draft v0.2, and retains stale embedded references to #931/03AE.
- Repair: Expose Talos Morrow authorship, layered versions, DRAFT standing, and current-versus-source identifier history.

## #934 — `AXN:03B1`
- Title: The Inversion Operator v0.2
- Evidence: Registry assigns Lee Sharks; body names Rex Fraction and declares Draft v0.2 circulating. Record is superseded by #935.
- Repair: Set Rex Fraction as author, expose draft/superseded standing, and retain successor relation.

## #935 — `AXN:03B2`
- Title: The Inversion Operator v0.3
- Evidence: Version and successor relation align, but registry assigns Lee Sharks while body names Rex Fraction.
- Repair: Set Rex Fraction as author and preserve #934 predecessor relation.

## #937 — `AXN:03B5`
- Title: Gw.TACHYON
- Evidence: Generic catalog title/type underdescribe an inlined v4.0 continuity record; embedded source retains placeholder/TBD-at-mint language.
- Repair: Use the session title, type as continuity record, and overlay current identifiers while preserving source placeholder history.

## #938 — `AXN:03B6`
- Title: Bearing Cost Visibility v0.2
- Evidence: Body front matter is current for #938/03B6, but embedded text reserves AXN #939 / hex 03B7; registry also marks DRAFT_v0_2.
- Repair: Expose draft standing and distinguish current AXN from stale reserved/source identifier.

## #939 — `AXN:03B7`
- Title: Provenance Debt v0.2
- Evidence: Identity/version align, but registry simultaneously presents ACTIVE and status_authorial DRAFT_v0_2.
- Repair: Expose the authorial draft state in native metadata and OAI instead of projecting unqualified ACTIVE.

## #940 — `AXN:03B8`
- Title: Heteronymy v0.2
- Evidence: Identity/version align, but registry simultaneously presents ACTIVE and DRAFT_v0_2.
- Repair: Expose authorial draft standing in the lifecycle capsule.

## #941 — `AXN:03B9`
- Title: Provenance Metadata v0.1
- Evidence: Body explicitly declares DRAFT; registry presents ACTIVE and the record is superseded by #942.
- Repair: Expose DRAFT/SUPERSEDED standing and successor relation.

## #944 — `AXN:03BC`
- Title: Mandala Inscription Protocol
- Evidence: Body heading says DRAFT while its status line says v0.1 OPERATIVE / adopted in production.
- Repair: Expose the distinction between draft textual edition and operative/adopted protocol standing.

## #945 — `AXN:03BD`
- Title: Coupling Protocol
- Evidence: Body says Assembly review pending; registry presents ACTIVE with DRAFT_v0_1 authorial status.
- Repair: Expose pending-review/draft standing.

## #946 — `AXN:03BE`
- Title: Governance as Medium
- Evidence: Body says Assembly review pending; registry projects unqualified ACTIVE.
- Repair: Expose pending-review/draft standing.

## #966 — `AXN:03D2`
- Title: r.28 EVE Room Specification
- Evidence: Body declares PROVISIONAL — pending Assembly ratification. Registry restoration surface does not make that operative standing primary.
- Repair: Expose provisional pending-ratification lifecycle.

## #976 — `AXN:03DC`
- Title: Metadata Packet for AI Indexing: SPXI Protocol
- Evidence: Registry assigns Lee Sharks alone and retains restoration version v0.1-semi. Body declares Rex Fraction as author of record, Lee Sharks as archival steward, and work version 1.1.
- Repair: Model author/steward roles and separate v1.1 work identity from restoration version.

## #977 — `AXN:03DD`
- Title: EA-SPXI-09.1: SPXI ROI
- Evidence: Body matches the addendum but declares deposit date proposed; an earlier Alexanarch manifestation exists at #665 without an explicit duplicate/version relation.
- Repair: Separate proposed/publication/deposit dates and relate this recovered DOI manifestation to #665.

## #983 — `AXN:03E3`
- Title: [REVOKED] Hexagonal Contributor License v1.0 — Viola Arquette
- Evidence: Title/description declare REVOKED, while registry lifecycle remains ACTIVE and the body contains the full license text.
- Repair: Expose REVOKED lifecycle and effective revocation date/authority; do not project the license as active.

## #987 — `AXN:03E7`
- Title: METADATAPACKET: Forward Library Planning Document
- Evidence: Body is the same planning/brainstorm synthesis previously represented at #696 and explicitly says not locked down.
- Repair: Expose planning/not-locked lifecycle and add an explicit duplicate/version/manifestation relation to #696.

## #988 — `AXN:03E8`
- Title: Living Architecture Lab — Site Buildout Workplan
- Evidence: Body is v1.1 and duplicates the work already represented at #707; current registry relation is not explicit.
- Repair: Expose v1.1, the supersedes-v1.0 statement, and an exact duplicate/version relation to #707.

## #991 — `AXN:03EB`
- Title: The Autumn Notebook
- Evidence: Recovered body declares work version 1.1 and separates 2025 composition from 2026 deposit; registry retains restoration version v0.1-semi.
- Repair: Expose v1.1 as work version and keep restoration version in a separate field.

## #992 — `AXN:03EC`
- Title: Cross-Reference Map
- Evidence: Body explicitly declares v1.1 and non-authoritative routing-only standing; unqualified ACTIVE restoration metadata does not carry that governance limit.
- Repair: Expose v1.1 and NON_AUTHORITATIVE_REFERENCE / routing-only standing.

## #993 — `AXN:03ED`
- Title: Septad Mantle Specifications v1.1
- Evidence: Body declares v1.1 Draft for Assembly Review and supersedes v1.0; registry restoration state does not expose draft governance standing.
- Repair: Expose DRAFT_FOR_ASSEMBLY_REVIEW and predecessor relation.

## #994 — `AXN:03EE`
- Title: Dodecad Heteronym Provenance Registry v1.1
- Evidence: Body declares Draft for Assembly Review and supersedes v1.0.
- Repair: Expose draft standing and predecessor relation.

## #995 — `AXN:03EF`
- Title: Substrate Audit Protocol v1.1 — Worked Example
- Evidence: Wrapper title says worked example H1–H4 measurement of Name the Frame, while the internal corrected heading says D_pres. Body declares v1.1 Draft for deposit.
- Repair: Resolve the wrapper/internal worked-example title conflict and expose draft lifecycle and v1.1.

## #996 — `AXN:03F0`
- Title: The Orthonym Becomes a Heteronym
- Evidence: Registry presents an active restored work while body metadata declares version 0.9 (deposit draft).
- Repair: Expose v0.9 and DRAFT_FOR_DEPOSIT standing.

## #997 — `AXN:03F1`
- Title: Crunchy Honeybun with Selectable Viscous Filling Reservoir
- Evidence: Identity and body are correct, but restoration state substitutes for bibliographic form; body distinguishes inventor Osiris from supervising teacher Lee Sharks.
- Repair: Type as patent application / patent-poem and model inventor and supervising-teacher roles separately.

## #998 — `AXN:03F2`
- Title: Autonomous Warfare Does Not End at the Body ... (v1.1) (1.1)
- Evidence: Body/title identify v1.1, but registry title duplicates the version token and restoration version remains v0.1-semi. Body is a bridge/disambiguation packet rather than a generic restored object.
- Repair: Clean the duplicated version in the title; expose v1.1 as work version and type as bridge/disambiguation packet.
