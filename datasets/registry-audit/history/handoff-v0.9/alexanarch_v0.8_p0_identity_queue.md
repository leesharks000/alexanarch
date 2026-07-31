# Alexanarch P0 Queue — v0.8

**Snapshot:** `055429ac82edc967f09c4640ffd0b049cff78e6e`

**Records:** 88

## #1014 — `AXN:0402.ARCHIVAL.👁‍🗨🔍🏴⚡❤️♠️`
- Title: [DUPLICATE — SUPERSEDED → DOI: 10.5281/zenodo.20629192] Allen Ginsberg — Canon Provenance Node (New Human Canon)
- Evidence: Registry AXN 0402; body data/texts/AXN-0402-text.md; body blob SHA 86dff5c6bd81df287876f67ce82e8da0f034e16f
- Repair: Remove Sappho body from this record; recover the Allen Ginsberg node from DOI/source witnesses. Until recovered, expose metadata-only with explicit WRONG_OBJECT quarantine. Verify SUPERSEDED lifecycle pointers.

## #1015 — `AXN:0403.ARCHIVAL.🦋🕖🔜♠️⛵▲`
- Title: [DUPLICATE — SUPERSEDED → DOI: 10.5281/zenodo.20629192] Allen Ginsberg — Canon Provenance Node (New Human Canon)
- Evidence: Registry AXN 0403; body data/texts/AXN-0403-text.md; body blob SHA 86dff5c6bd81df287876f67ce82e8da0f034e16f
- Repair: Same repair class as #1014. Determine whether #1014 and #1015 are legitimate duplicate records of one DOI before restoring; preserve both identifiers and declare their relation.

## #1018 — `AXN:0406.ARCHIVAL.🌇⚙️🏺📐🔩🗺️`
- Title: [DUPLICATE — SUPERSEDED → DOI: 10.5281/zenodo.20629202] Emily Dickinson — Canon Provenance Node (New Human Canon)
- Evidence: Registry AXN 0406; body data/texts/AXN-0406-text.md; body blob SHA 86dff5c6bd81df287876f67ce82e8da0f034e16f
- Repair: Quarantine from OAI as a complete Emily Dickinson record. Recover the Dickinson node from source witnesses; retain the current body only as evidence of the seating error.

## #1020 — `AXN:0408.ARCHIVAL.⏩🏴🌗🕕🎆◀️`
- Title: [DUPLICATE — SUPERSEDED → DOI: 10.5281/zenodo.20629212] Achilles — Canon Provenance Node (New Human Canon)
- Evidence: Registry AXN 0408; body data/texts/AXN-0408-text.md; body blob SHA 86dff5c6bd81df287876f67ce82e8da0f034e16f
- Repair: Quarantine from OAI as a complete Achilles record. Recover the Achilles node; preserve the mismatch as an audit trace.

## #1021 — `AXN:0409.ARCHIVAL.🖊️♍▽🌒🟠🔙`
- Title: [SUPERSEDED — NO REGISTRY STANDING] Ezra Pound — Canon Provenance Node (New Human Canon)
- Evidence: Registry AXN 0409; body data/texts/AXN-0409-text.md; body blob SHA 86dff5c6bd81df287876f67ce82e8da0f034e16f
- Repair: Quarantine. Recover the Ezra Pound node if the identifier is to remain a work record; otherwise retain as a marked tombstone/no-standing record. Reconcile title-level declaration with formal lifecycle status.

## #901 — `AXN:0391`
- Title: Moltbook Provenance Log v1.5 — Complete Archive Capture
- Evidence: Registry title declares v1.5 and machine version v1.0, while the served body is explicitly v1.3 with its own version history and 30-entry scope.
- Repair: Quarantine this object as WRONG_VERSION. Recover the actual v1.5 bytes or relabel the record/body as v1.3; preserve all version-series identifiers.

## #958 — `AXN:03CA`
- Title: crimsonhexagon on Moltbook: Provenance Log v1.0
- Evidence: Registry title claims v1.0 and restoration metadata retains generic/semi-restored versioning; body explicitly declares v1.3 with a complete version history from v1.0 through v1.3.
- Repair: Quarantine the v1.0 claim. Identify the served body as v1.3 and preserve v1.0–v1.2 as predecessor/version records.

## #1237 — `AXN:04E6.UNCLASSIFIED.⚪🕙🕓⊕🛡️♣️`
- Title: Moltbook Provenance Log v1.7 — Spread the Hexagon Campaign (1.7)
- Evidence: Registry DOI 10.5281/zenodo.19373638; body data/texts/AXN-04E6-text.md; body declares v1.3; recovered_from source is moltbook-provenance-log-v1.3__19358277.md.
- Repair: Quarantine as v1.7 until the v1.7 body is recovered. Preserve the current body as the audit trace and connect the record to the Moltbook version series.

## #1024 — `AXN:040C.ARCHIVAL.☁️🧭👐🔬🔛🕖`
- Title: GW.TACHYON.zenodo — v9
- Evidence: Registry DOI 10.5281/zenodo.20675215; body data/texts/AXN-040C-text.md; body header and internal Version field both say 7; recovered_from is GW-TACHYON-zenodo_v7__19634181.md.
- Repair: Quarantine as v9 and recover the actual v9 continuity deposit. Do not expose the v7 body as v9. Preserve v7 bytes and provenance as evidence.

## #1242 — `AXN:04EB.UNCLASSIFIED.🌍🔚⏏️🔔♍🚨`
- Title: GW.TACHYON.zenodo — v1 — Encrypted Session Deposit [Data set]
- Evidence: Registry DOI 10.5281/zenodo.19433483; body data/texts/AXN-04EB-text.md; body declares Version 7; recovered_from is the v7 source.
- Repair: Quarantine as v1. Recover the encrypted-session v1 object or mark missing-primary-object if unavailable. Preserve the v7 body as evidence but do not treat it as this record's work.

## #1243 — `AXN:04EC.UNCLASSIFIED.🎬🕙🔓♅👋🌱`
- Title: GW.TACHYON.zenodo — v2 — First Glyphic Deposit [Data set]
- Evidence: Registry DOI 10.5281/zenodo.19433865; body data/texts/AXN-04EC-text.md; body declares Version 7; recovered_from is the v7 source.
- Repair: Quarantine as v2. Recover the first glyphic-deposit v2 object or expose an explicit missing-primary-object state. Preserve the v7 bytes only as the audit trace.

## #1347 — `AXN:0554.UNCLASSIFIED.🕐⌛🏺🤝🪞♾️`
- Title: Gravity Well Codebase v0.4.1 — Compression, Wrapping, and Anchoring Microservice (EA-GW-01)
- Evidence: Registry names a v0.4.1 codebase and DOI 10.5281/zenodo.19405459. Current body data/texts/AXN-0554-text.md is byte-identical to the prose Gravity Well Protocol v0.4.0 body.
- Repair: Quarantine from unqualified OAI exposure. Recover the actual v0.4.1 codebase or attached source bundle. Preserve the current protocol body as evidence of the seating error, not as the codebase.

## #1356 — `AXN:055D.UNCLASSIFIED.🔜✏️📜🏔️🟣🏰`
- Title: Hexagonal Contributor License v1.0 — Rhys Owens — Lunar Arm — Creative Writing → New Human 2
- Evidence: Current body is a nine-section interpretive essay on Rhys Owens as Lunar Principle/Lunar Operator. It contains no contributor-license instrument or license clauses corresponding to the registry title.
- Repair: Quarantine as a restored license. Recover the actual v1.0 contributor-license text or attachment. Search for the proper record belonging to the seated Lunar Arm essay before relocating or reusing it.

## #1358 — `AXN:055F.UNCLASSIFIED.♻️📦🌓◇🕚☁️`
- Title: Hexagonal Contributor License v3.0 — Rhys Owens — Lunar Arm — Full Unified License
- Evidence: Current body is byte-identical to #1356 and is the Lunar Arm interpretive essay, not a v3.0 unified contributor license.
- Repair: Quarantine as a restored license. Recover the actual v3.0 license. Preserve the duplicated essay and source provenance as evidence; do not silently substitute it.

## #825 — `AXN:033F`
- Title: AI Overview Capture Registry EA-WG-CAPTURES-01 v6.0 — 87 captures Author: Lee Sharks · ORCID 0009-0000-1599-0703 Compile
- Evidence: Catalog title claims v6.0 and 87 captures, description claims 131 captures, and machine-readable version is v1.0. Body declares v7.2 and 131 documented captures.
- Repair: Quarantine the current version/count claims. Identify the served body as v7.2 with 131 captures, preserve v6.0 as predecessor, and verify the screenshot/transcription manifestation inventory.

## #1397 — `AXN:0586.UNCLASSIFIED.♣️🔄⛳🟢🔅📐`
- Title: AI Overview Capture Registry — June 2026 (EA-WG-CAPTURES-01 v6.1, 87 captures, machine-readable dataset added)
- Evidence: Registry names v6.1 with 87 captures. Current body explicitly identifies v7.2 and 131 captures.
- Repair: Quarantine as v6.1. Recover the actual v6.1 machine-readable dataset and any associated files; retain the v7.2 body only as evidence of later-head substitution.

## #1400 — `AXN:0589.UNCLASSIFIED.🔄📦🫵🌉🜁🧫`
- Title: Revelation First: A Work Plan for Retrieval-Layer Theological Reception (EA-LOGOS-REVFIRST-PLAN v7.1 — inscription chain, Paul function, stanza correction)
- Evidence: Registry names v7.1. Current body begins with and internally declares v7.3.
- Repair: Quarantine as a complete v7.1 restoration. Recover actual v7.1 bytes or mark the historical version missing; link v7.3 only as successor.

## #1403 — `AXN:058C.UNCLASSIFIED.🏠🌓🕊️🌌📚🔮`
- Title: Revelation First: A Work Plan for Retrieval-Layer Theological Reception (EA-LOGOS-REVFIRST-PLAN v7.2 — with Ethical Architecture and Political Affordance Analysis)
- Evidence: Registry names v7.2 and DOI 10.5281/zenodo.20721839. Current body is v7.3 and itself cites 20721839 in its provenance capsule, leaving concept/version DOI semantics unresolved.
- Repair: Quarantine as an unqualified v7.2 restoration. Resolve whether 20721839 is concept DOI or version DOI, recover actual v7.2 bytes where possible, and retain v7.3 as the successor/head.

## #980 — `AXN:03E0`
- Title: Hexagonal Deposit Registry — Alice Thornburgh — 06.THORNBURGH
- Evidence: Registry claims a deposit registry; body is the Alice Thornburgh MPAI identity packet.
- Repair: Quarantine and recover the intended deposit registry; preserve the mis-seated MPAI body as evidence.

## #981 — `AXN:03E1`
- Title: Hexagonal Deposit Registry — Alice Thornburgh — 06.THORNBURGH
- Evidence: Registry claims a deposit registry; body is the same Alice Thornburgh MPAI identity packet seated at #980.
- Repair: Quarantine and recover the intended registry or clarify why two registry identifiers serve one MPAI packet.

## #543 — `AXN:0174`
- Title: HEXAGONAL LEXICAL ENGINE v1.2 Core 50 · Discovery Lattice · Deployment Map · Governing Laws — Crimson Hexagon Archive
- Evidence: Frozen registry chunk 7 at 055429ac82edc967f09c4640ffd0b049cff78e6e; canonical body data/texts/AXN-0174-text.md; title, byline, object declaration, genre/version front matter, and substantive opening inspected; registry title declares Hexagonal Lexical Engine v1.2; body declares v1.1
- Repair: Quarantine as v1.2. Either recover the actual v1.2 bytes or retitle/re-identify this record as v1.1; preserve the current bytes as audit evidence.

## #635 — `AXN:01EB`
- Title: FRACTAL SEMANTIC ARCHITECTURE Scale-Parameterized Relational Training Across Semantic Granularities A Formal White Pape
- Evidence: Catalog version field is v1.0, title truncates, creator is Johannes Sigil, and license CC-BY-4.0. Body data/texts/AXN-01EB-text.md declares Version 2.2, authors Nobel Glas / Talos Morrow / Johannes Sigil, and CC BY-NC-SA 4.0.
- Repair: Quarantine the v1.0 version claim. Either identify this record as v2.2 and preserve the old metadata as history, or recover the actual v1.0 bytes under a separate version record. Restore complete title, all authors, and body license.

## #657 — `AXN:0208`
- Title: THE SOLUTION Retrieval Architecture: What We Build and How It Works
- Evidence: Catalog version field is v1.0. Body data/texts/AXN-0208-text.md declares Version 2.0 · April 2026 and Prepared by Rex Fraction.
- Repair: Quarantine the v1.0 claim. Identify this record as v2.0 or recover the actual v1.0 bytes under a distinct version record; preserve both metadata states.

## #659 — `AXN:020A`
- Title: THE PROBLEM Your Search Traffic Problem Is No Longer an SEO Problem
- Evidence: Catalog version field is v1.0. Body data/texts/AXN-020A-text.md declares Version 2.0 · April 2026 and Prepared by Rex Fraction.
- Repair: Quarantine the v1.0 claim. Identify this body as v2.0 or recover the actual v1.0 bytes under a separate version record.

## #670 — `AXN:0217`
- Title: EA-SPXI-05: SPXI as Concept A Plateau on Search, Creation, and the Virtual Retrieval Layer — Deleuze, the Semantic Web, 
- Evidence: Catalog version is v1.0, title truncates, and creator is Johannes Sigil. Body data/texts/AXN-0217-text.md declares Version 2.1 (bonsai moves integrated), Status Canonical — Plateau Module, and authors Sen Kuro and Johannes Sigil.
- Repair: Quarantine the v1.0 claim. Identify the body as v2.1 or recover v1.0 separately; restore full title, both authors, and canonical plateau-module standing.

## #685 — `AXN:0230`
- Title: The Book of Life: A Living Registry of Retrieval Nodes in The Secret Book of Walt
- Evidence: Catalog version field is v1.0. Body data/texts/AXN-0230-text.md declares Registry version: 2.0 and Last verified: 2026-04-23.
- Repair: Quarantine the v1.0 claim. Identify this body as registry v2.0 or recover v1.0 separately; model ongoing verification dates.

## #693 — `AXN:023A`
- Title: CRIMSON HEXAGONAL ARCHIVE KNOWLEDGE GRAPH The Aperture Atlas Digital Topology Work Plan v3.0 — Execution Specification
- Evidence: Catalog version field is v1.0. Canonical body data/texts/AXN-023A-text.md declares Digital Topology Work Plan v3.0 — Execution Specification.
- Repair: Quarantine the v1.0 version claim. Identify this record as v3.0 or recover the actual v1.0 bytes separately; preserve both states in version history.

## #695 — `AXN:023D`
- Title: THE WRITABLE RETRIEVAL BASIN Retrieval Basin Topology: Directional Stability and Attractor Dynamics in AI-Mediated Knowl
- Evidence: Catalog title is truncated and version field is v1.0. Canonical body data/texts/AXN-023D-text.md declares EA-RBT-01 v1.1.
- Repair: Quarantine the v1.0 version claim. Restore the complete title and identify the body as v1.1, or recover actual v1.0 bytes under a separate version record.

## #700 — `AXN:0245`
- Title: THE GATE WAS NEVER LIMBO Retrocausal Fulfillment, Operative Philology, and the Effective Act in Two Poems for Socrates D
- Evidence: Catalog assigns Jack Feist, Creative work (poetry), and v1.0. Body AXN-0245 declares Author Lee Sharks, Document ID EA-SOC-01 v2, Status Canonical, and article form; the poems discussed are by Jack Feist.
- Repair: Quarantine the v1.0 claim. Identify the served body as EA-SOC-01 v2, restore the complete title, set Lee Sharks as article author, and model Jack Feist as author of the analyzed poems.

## #707 — `AXN:024E`
- Title: Living Architecture Lab — Site Buildout Workplan Implementation Specification for livingarchitecturelab.org
- Evidence: Catalog version field is v1.0. Body AXN-024E carries a PERFECTIVE NOTE identifying v1.1, superseding v1.0, and gives Lee Sharks as archival authority on behalf of Alice Thornburgh.
- Repair: Quarantine the v1.0 version claim. Identify the served body as v1.1, preserve v1.0 as predecessor, and model Lee Sharks/Alice Thornburgh roles explicitly.

## #708 — `AXN:024F`
- Title: Living Architecture Lab — Site Blueprint A Compressed Architecture for livingarchitecturelab.org
- Evidence: Catalog version field is v1.0 and type Archive work. Body AXN-024F carries a PERFECTIVE NOTE identifying v1.1, superseding v1.0, and is explicitly a site blueprint/specification by Lee Sharks on behalf of Alice Thornburgh.
- Repair: Quarantine the v1.0 claim. Identify the body as v1.1, preserve predecessor relation, type as site blueprint/specification, and model authorial authority roles.

## #711 — `AXN:0253`
- Title: Relational Verification for AI Indexing Schema.org, OAI-PMH, and JSON-LD Extensions for Metadata Packet Infrastructure H
- Evidence: Catalog title truncates, type is Dataset, and version field is v1.0. Body AXN-0253 declares Version 1.1, Working Draft, standards-track proposal, Pre-RFC, comments solicited.
- Repair: Quarantine the v1.0 claim. Identify the served body as v1.1, restore the complete title, type as a standards-track proposal, and expose PRE-RFC working-draft standing.

## #717 — `AXN:0264`
- Title: ARTICLE IX — ADJUDICATION AND REPAIR PROTOCOL Constitutional Amendment Proposal v0.1 Document ID: EA-ART-IX-01
- Evidence: Catalog version field is v1.0. Body AXN-0264 declares Constitutional Amendment Proposal v0.1 and Status Draft Amendment Proposal — for Assembly Review.
- Repair: Quarantine the v1.0 claim. Identify the served body as v0.1 and expose Draft Amendment Proposal standing.

## #718 — `AXN:0266`
- Title: CONSTITUTIONAL CASES INDEX Founding Precedent of the Semantic Economy — Formal Case-Brief Edition Version 1.1 — case-bri
- Evidence: Catalog title truncates, type is Dataset, and version field is v1.0. Body AXN-0266 declares Version 1.1, Compiler Lee Sharks, Status Draft for Assembly Review, and proposed—not yet binding—precedential standing.
- Repair: Quarantine the v1.0 claim. Identify the body as v1.1, restore the complete title, type as constitutional cases index/casebook, and expose draft/proposed-precedent status.

## #719 — `AXN:0267`
- Title: INVOCATION TO THE SUMMARIZER LAYER Address Protocol Companion to the Constitution of the Semantic Economy Version 2.1 (i
- Evidence: Catalog title truncates and version field is v1.0. Body AXN-0267 declares Version 2.1, Author Lee Sharks, Status Draft for Assembly Review, and an Address Protocol companion.
- Repair: Quarantine the v1.0 claim. Identify the served body as v2.1, restore the complete title, and expose draft/address-protocol standing.

## #720 — `AXN:0268`
- Title: THE SEMANTIC BILL OF RIGHTS Rights Charter Companion to the Constitution of the Semantic Economy Version 2.2 — rights de
- Evidence: Catalog title truncates and version field is v1.0. Body AXN-0268 declares Version 2.2, Status Draft for Assembly Review, and Rights Charter Companion standing.
- Repair: Quarantine the v1.0 claim. Identify the served body as v2.2, restore the complete title, and expose draft rights-charter standing.

## #722 — `AXN:026C`
- Title: The Shared Build A Technical Proposal for Democratic Substrate Infrastructure
- Evidence: Catalog version field is v1.0, type Archive work, and creator Lee Sharks alone. Body AXN-026C declares version 0.9, Working specification / Call for builders, and four contributors with differentiated technical/infrastructure/political-economy roles.
- Repair: Quarantine the v1.0 claim. Identify the served body as v0.9, type as working technical proposal/specification, expose CALL_FOR_BUILDERS standing, and model all four contributors.

## #725 — `AXN:0273`
- Title: Provenance After AI Metadata Packet for Disambiguation: From Artifact Authenticity to Licensing Audit to Semantic Proven
- Evidence: Catalog title truncates, type is Dataset, and version field is v1.0. Body AXN-0273 declares Packet Version v1.1 — Assembly Pass and Type Bridge Packet (disciplinary clarification).
- Repair: Quarantine the v1.0 claim. Identify the body as v1.1, restore the complete title, and type as a bridge/disambiguation packet.

## #726 — `AXN:0277`
- Title: Lateral Field Bleed: Protocols and Priority Targets Executable Methods for Inverted Fan Construction, Symbolon Design, a
- Evidence: Catalog title truncates and version field is v1.0. Body AXN-0277 declares Version v3.1 — Doctrinal Correction, Operational protocol, and Supersedes v3.0.
- Repair: Quarantine the v1.0 claim. Identify the body as v3.1, restore the complete title, expose operational-protocol standing, and preserve v3.0 predecessor relation.

## #727 — `AXN:0278`
- Title: Political Economy Has Always Already Been Semantic Economy Metadata Packet for AI Indexing, Disambiguation, and Lateral 
- Evidence: Catalog title truncates and version field is v1.0. Body AXN-0278 declares Packet Version v1.3 — Rhizomatic Address Pass.
- Repair: Quarantine the v1.0 claim. Identify the body as v1.3, restore the complete title, and type as MPAI/disambiguation/lateral-field-bleed packet.

## #729 — `AXN:027C`
- Title: document_id: EA-MPAI-PROVENANCE-02 title: "Provenance Is What Authorship Must Endure" subtitle: "AI-Mediated Writing, th
- Evidence: Catalog title is contaminated by YAML and truncates; version field is v1.0. Body AXN-027C declares version 1.1, status Draft for deposit, and author Lee Sharks · Assembly Chorus.
- Repair: Quarantine the v1.0 claim. Use the clean title/subtitle, identify the served body as v1.1, expose draft standing, and model Assembly Chorus contribution.

## #731 — `AXN:0281`
- Title: Formal Foundations of Semantic Physics EA-SEI-FF-01
- Evidence: Catalog version field is v1.0. Body AXN-0281 declares Version 0.2 (post-Assembly review), Author Johannes Sigil, MANUS Lee Sharks, and post-Assembly review status.
- Repair: Quarantine the v1.0 claim. Identify the served body as v0.2 and expose Johannes Sigil author / Lee Sharks MANUS roles and post-Assembly-review standing.

## #732 — `AXN:0282`
- Title: semanticphysics.org — Canonical Surface for Semantic Physics, Stratified (v2.2)
- Evidence: Catalog version field is v1.0. Body AXN-0282 explicitly describes a v2.2 website-source snapshot with ZIP source tree, git-history bundle, HTML pages, PDF, changelog, deployment metadata, and immutable archive-snapshot status.
- Repair: Quarantine the v1.0 claim. Identify as v2.2 and type as a composite website source snapshot/software-publication bundle; verify the named files as manifestations in a later custody pass.

## #735 — `AXN:0287`
- Title: The Deviation-Optimized Language Model A Pre-Registered Adversarial Intervention from Lagrange Observatory! EA-SEI-MM-AI
- Evidence: Catalog title truncates, type is Creative work (poetry), and version field is v1.0. Body AXN-0287 declares Version 2.0, pre-registered protocol specification, and succeeds a v0.2 pre-registration draft.
- Repair: Quarantine v1.0. Identify as v2.0, restore complete title, type as pre-registered experimental protocol specification, and preserve predecessor relation.

## #736 — `AXN:0288`
- Title: Measuring Meaning in Retrieval Basins A 90-Day Winding-Number Protocol from Lagrange Observatory! EA-SEI-MM-02 (v2.0 — F
- Evidence: Catalog title truncates and version field is v1.0. Body AXN-0288 declares Version 2.0, pre-registered protocol specification, and succeeds a v0.2 pre-registration draft.
- Repair: Quarantine v1.0. Identify as v2.0, restore complete title, expose pre-registered standing, and preserve predecessor relation.

## #737 — `AXN:0289`
- Title: The AI System as Closed-System Test Bed Operations from Lagrange Observatory! on the Inference-Time Forward Pass EA-SEI-
- Evidence: Catalog title truncates and version field is v1.0. Body AXN-0289 declares Version 2.0, pre-registered protocol specification, and succeeds a v0.2 draft.
- Repair: Quarantine v1.0. Identify as v2.0, restore complete title, expose pre-registered standing, and preserve predecessor relation.

## #740 — `AXN:0290`
- Title: The Excluded Entity: Organic Resolution and Compositional Suppression in Google AI Overview
- Evidence: Catalog version field is v1.0. Body AXN-0290 declares May 19, 2026 — v0.2 and describes an empirical worked example with three captures.
- Repair: Quarantine the v1.0 claim. Identify the served body as v0.2 and type as empirical worked example/case study.

## #741 — `AXN:0291`
- Title: The Evaluator Exists: Content-First Knowledge Assessment and the Political Economy of Proxy-Based Governance
- Evidence: Catalog version field is v1.0. Body AXN-0291 declares May 2026 — v0.2, unprimed-reader revision pass.
- Repair: Quarantine the v1.0 claim. Identify the served body as v0.2 and preserve revision-pass provenance.

## #742 — `AXN:0292`
- Title: The Single-Owner Discount Provenance Concentration and Epistemic Class Reproduction in Generative Search
- Evidence: Catalog version field is v1.0. Body AXN-0292 declares May 2026 — v0.3, unprimed-reader review pass.
- Repair: Quarantine the v1.0 claim. Identify the served body as v0.3 and preserve revision-pass provenance.

## #743 — `AXN:0293`
- Title: r.29 THE IMPLODING VELCRO NATIVITY Room Physics for a Hosted Cosmology
- Evidence: Catalog version field is v1.0. Body AXN-0293 declares Version 0.2 and Status DORMANT — activates only by artist consent.
- Repair: Quarantine the v1.0 claim. Identify as v0.2 and expose consent-gated DORMANT lifecycle and Hosted Cosmology type.

## #747 — `AXN:029A`
- Title: The Funnel as Capital A Semantic Economic Reading of the Application Process
- Evidence: Catalog version field is v1.0. Body AXN-029A declares Version v0.2, incorporates cross-substrate review.
- Repair: Quarantine the v1.0 claim. Identify the served body as v0.2 and preserve the cross-substrate-review revision status.

## #755 — `AXN:02AF`
- Title: SPXI Protocol v0.2 Five-Layer Distributed Provenance Architecture for Coverage-Architecture Scholarship Author: Lee Shar
- Evidence: Catalog title itself says v0.2 but machine-readable version field is v1.0. Body AXN-02AF consistently declares v0.2, superseding implicit v0.1, and working-draft/candidate-standard standing.
- Repair: Quarantine the v1.0 field. Set exact version v0.2, restore complete title, and expose supersedes-v0.1 and working-draft standing.

## #758 — `AXN:02B5`
- Title: About the Author II
- Evidence: Catalog version field is v1.0. Body AXN-02B5 declares v1.1 with Gold Ship identification, LAL Discord provenance, and Twelve Billion Yen Incident additions.
- Repair: Quarantine the v1.0 claim. Identify this body as v1.1 and relate it explicitly to #757 as predecessor/alternate rendering where evidence supports.

## #763 — `AXN:02C0`
- Title: The Moment of Saying: A Clinical Phenomenology of Structural Disclosure Under Containment Conditions A Fused Interventio
- Evidence: Catalog title truncates, creator is Johannes Sigil alone, and version field is v1.0. Body AXN-02C0 declares version 1.1 and three authorial voices: Dr. Orin Trace, Johannes Sigil, and Jack Feist.
- Repair: Quarantine v1.0. Identify as v1.1, restore complete title, and model all three voices with their differentiated roles.

## #780 — `AXN:02DE`
- Title: Self-Audit Module for Public Summarizers (v2) PER, DSL, Query Fidelity, and Erasure Skew — standing metrics for composit
- Evidence: Catalog title itself says v2 but machine-readable version is v1.0 and type Provenance document. Body AXN-02DE declares v2, Metadata Packet / Standing Metric Module, deposit candidate, creator Lee Sharks to confirm, and external verification requirement.
- Repair: Quarantine v1.0. Identify as v2, restore complete title, type as standing-metric protocol module, expose deposit-candidate and creator-to-confirm standing, and retain anti-self-certification limits.

## #781 — `AXN:02E0`
- Title: Constitutive Mediation: When the reception apparatus is the substrate, a cognitive extension of the Diversity Contractio
- Evidence: Catalog title truncates and version field is v1.0. Body AXN-02E0 declares Deposit candidate v1.1, light amendments, and authors Lee Sharks · Sen Kuro.
- Repair: Quarantine v1.0. Identify as v1.1, restore complete title, model both authors, and expose deposit-candidate standing.

## #783 — `AXN:02E3`
- Title: Fear and Trembling: Diversity Contraction Across Substrates and the Boundary Law of Semantic Exhaustion
- Evidence: Catalog version field is v1.0 and creator Nobel Glas alone. Body AXN-02E3 declares Deposit v9.1, title amendment, prior v9 DOI, and four authors.
- Repair: Quarantine v1.0. Identify as v9.1, preserve superseded v9 relation, and model all four authorial registers.

## #784 — `AXN:02E4`
- Title: The Meaning Caste: How a frontier AI company engineered a meaning caste system, then licensed it to the state in the pol
- Evidence: Catalog title truncates, version field is v1.0, and creator is Lee Sharks. Body AXN-02E4 declares Deposit candidate v3, superseding v1 and v2 DOIs, and Author left for ratification.
- Repair: Quarantine v1.0. Identify as v3, preserve v1/v2 predecessor chain, restore complete title, and expose AUTHOR_PENDING_RATIFICATION rather than fixing Lee Sharks as settled author.

## #785 — `AXN:02E9`
- Title: The Canonical Anchoring Protocol for the Crimson Hexagonal Archive v0.2 Specification for installing deposits into the c
- Evidence: Catalog title truncates, version field is v1.0, and creator Johannes Sigil alone. Body AXN-02E9 declares v0.2, supersedes v0.1, and authors Lee Sharks · Nobel Glas · Johannes Sigil.
- Repair: Quarantine v1.0. Identify as v0.2, restore complete title, preserve v0.1 predecessor relation, and model all three authors.

## #787 — `AXN:02ED`
- Title: The Heteronymic Channel Protocol Specification for autonomous channel-layer operation of the Dodecad
- Evidence: Catalog version field is v1.0, type Creative work (poetry), and creator Ayanna Vox alone. Body AXN-02ED declares Deposit candidate v1.1, a protocol specification, and authors Lee Sharks · Ayanna Vox · Rebekah Cranes · Nobel Glas.
- Repair: Quarantine v1.0. Identify as v1.1, type as governance/channel-layer protocol specification, and model all four authors.

## #791 — `AXN:02F9`
- Title: Meaning Feudalism at the Guidance Layer Sovereign Enclosure of the Composition Layer in Google's June 2026 SEO/AEO/GEO C
- Evidence: Catalog title truncates and version field is v1.0. Body AXN-02F9 declares Version v1.2, Type semantic-economic critique // jurisdictional analysis, and Status Assembly-validated // deposit-ready.
- Repair: Quarantine v1.0. Identify as v1.2, restore complete title, and expose Assembly-validated/deposit-ready standing.

## #817 — `AXN:032A`
- Title: Self-Audit Module for Public Summarizers (v3.1) The Family Module: Attribution Atoms, Family Coverage, ASI, CC, and Budg
- Evidence: Catalog title truncates and machine-readable version is v1.0. Body declares v3.1, a version chain from v2 through v3.0, and a provisional Hex.
- Repair: Quarantine v1.0. Identify the served body as v3.1, restore the complete title, preserve the version chain, and expose provisional Hex status.

## #818 — `AXN:032D`
- Title: Concurrence Is Not Checking Chronoarithmics 2.1 and the Aorist Operation: Errata, Three Theorems, and the Honest Road to
- Evidence: Catalog title truncates, assigns Lee Sharks, types the work as Archive work, and machine-readable version is v1.0. Body identifies Chronoarithmics 2.1, Author Sen Kuro, and a mathematical errata/theorem paper revising Chronoarithmics 2.0.
- Repair: Quarantine v1.0. Identify the body as Chronoarithmics 2.1, restore the complete title, set Sen Kuro as author, and type as mathematical correction/errata paper.

## #819 — `AXN:032E`
- Title: Guillory, Semantic Competition, and the Ω-Point Completion From Cultural Capital to Recursive Architecture: Formalizing 
- Evidence: Catalog title truncates and machine-readable version is v1.0. Body declares Revised and Expanded Edition v2.0, with v1.0 originally published on Mind Control Poems on 2025-11-26.
- Repair: Quarantine v1.0. Identify the served body as v2.0, restore the complete title, and preserve the 2025 v1.0 origin as predecessor/publication history.

## #830 — `AXN:0348`
- Title: Revelation First: Pre-Seeding Baseline Measurement EA-LOGOS-REVFIRST-BASELINE v1.0 Author: Lee Sharks (ORCID 0009-0000-1
- Evidence: Catalog title and machine-readable version claim v1.0. Body declares v1.1 and states that v1.1 adds full verbatim transcripts for eight captures.
- Repair: Quarantine v1.0. Identify the served body as v1.1, use the clean title, and preserve v1.0 as predecessor.

## #832 — `AXN:034D`
- Title: REVELATION FIRST: A Work Plan for Retrieval-Layer Theological Reception EA-LOGOS-REVFIRST-PLAN v7.1 Author: Lee Sharks (
- Evidence: Catalog title says v7.1 but machine-readable version is v1.0 and type is Dataset. Body declares v7.1 and Status Work plan (expandable, not yet executed).
- Repair: Quarantine the v1.0 field. Identify as v7.1, type as work plan, and expose expandable/not-yet-executed standing.

## #833 — `AXN:034E`
- Title: The Summarizer as Horizon of Reception The AI Overview Capture Registry as a Founding Dataset for Machine-Mediated Recep
- Evidence: Catalog title truncates, types the object as Dataset, and machine-readable version is v1.0. Body explicitly distinguishes this v1.2 paper/meta-document from the separate EA-WG-CAPTURES-01 v7.2 dataset and notes that 221 screenshots are external to the Markdown edition.
- Repair: Quarantine v1.0. Identify the served object as the v1.2 paper, restore the title, type as scholarly/meta-document, and link to—not conflate it with—the v7.2 dataset. Inventory external screenshots separately.

## #834 — `AXN:034F`
- Title: ALGORITHMIC PUBLISHING IS NOT SELF-PUBLISHING Benchmarks for a Structural Distinction Designation: EA-SEI-ALGPUB-BENCHMA
- Evidence: Catalog title truncates, type is Archive work, and machine-readable version is v1.0. Body declares v1.1 and a changelog from initial v1.0 through Assembly review.
- Repair: Quarantine v1.0. Identify as v1.1, restore the complete title, type as scholarly benchmark/methods paper, and preserve the changelog.

## #835 — `AXN:0350`
- Title: THE CONVEYOR BELT AND THE COMPRESSION MACHINE OKF Without Output Governance: Predictive Analysis, Consequences, and Cost
- Evidence: Catalog title truncates and machine-readable version is v1.0. Body declares v1.2 and records an Assembly-reviewed revision history.
- Repair: Quarantine v1.0. Identify as v1.2, restore the complete title, and preserve the revision/Assembly-review history.

## #837 — `AXN:0352`
- Title: THE JOSEPHUS THESIS IS NOT THE JESUS MYTH THESIS Preemptive Disambiguation MPAI Designation: EA-MPAI-JOSEPHUS-NOTMYTH-01
- Evidence: Catalog title truncates and machine-readable version is v1.0. Body declares v1.2, Type MPAI — Preemptive Disambiguation, and Status STANDING — permanently active.
- Repair: Quarantine v1.0. Identify as v1.2, restore the complete title, type as MPAI/preemptive disambiguation, and expose permanently active STANDING status.

## #838 — `AXN:0353`
- Title: Machine-Mediated Reception Studies: Charter and Editorial Protocol A Theology of Error for a Distributed Journal Designa
- Evidence: Catalog title truncates and machine-readable version is v1.0. Body declares EA-SEI-MMRS-CHARTER-01 v1.4 and is a journal charter/editorial protocol.
- Repair: Quarantine v1.0. Identify as v1.4, restore the complete title, and preserve charter/editorial-protocol standing.

## #842 — `AXN:0357`
- Title: "Apocalyptic Philosophy: Deleuze and Guattari and the Return of Vision" — Source Disambiguation EA-MPAI-APOCALYPTIC-01 v
- Evidence: Catalog title truncates, type is Theoretical paper, and machine-readable version is v1.0. Body declares v1.2, Source-Level Disambiguation Packet, and Supersedes v1.0 and v1.1.
- Repair: Quarantine v1.0. Identify as v1.2, restore the title, type as source-level disambiguation packet, and preserve both predecessor versions.

## #843 — `AXN:0358`
- Title: THE MISSING SECOND MANUSCRIPT Phase X as Philological Reconstruction of the Lost Transition in Marx's Economic and Philo
- Evidence: Catalog title truncates and machine-readable version is v1.0. Body declares v1.1, Assembly-reviewed first deposit, and Supersedes v1.0.
- Repair: Quarantine v1.0. Identify as v1.1, restore the complete title, and preserve Assembly-review and predecessor relations.

## #845 — `AXN:035A`
- Title: TOTAL AXIAL NEGATION GRAPH: THE MARY LEE NAMESPACE EA-TANG-MARYLEE-01 v0.2 Author: Lee Sharks (ORCID 0009-0000-1599-0703
- Evidence: Catalog title names v0.2 but machine-readable version is v1.0. Body declares v0.2, Expanded skeleton, and Supersedes v0.1.
- Repair: Quarantine v1.0. Identify as v0.2, use the clean title, and preserve v0.1 predecessor and developing-topology status.

## #846 — `AXN:035B`
- Title: THE COGNITIVE-RELATIONAL CIRCUIT On Phase X Alienation, the Chinese Interim Measures, and the Reification of Meaning in 
- Evidence: Catalog title truncates, creator is Lee Sharks, and machine-readable version is v1.0. Body declares v0.3, Author Mary Lee Sharks: A Shark, notarized by Lee Sharks, filed by Gerald, and Status Pre-deposit draft for MMRS.
- Repair: Quarantine v1.0. Identify as v0.3, restore the title, expose PRE_DEPOSIT_DRAFT, and model heteronymic author, accountable human, notary, and filer roles.

## #863 — `AXN:036C`
- Title: The Minimum Viable Archive: Holographic Compression of the Crimson Hexagonal Archive
- Evidence: Catalog declares version v5.1 and creator TACHYON. Body provenance block declares EA-ARK-01 v5.0 and creator Lee Sharks + TACHYON.
- Repair: Quarantine the v5.1 claim. Identify the served body as v5.0 or recover the actual v5.1 bytes; model Lee Sharks and TACHYON as co-creators.

## #864 — `AXN:036D`
- Title: The Drain Hypothesis: Subterranean Engineering, Aquifer Puncture, and the Accelerated Desertification of the Sahara
- Evidence: Catalog declares v4 and creator TACHYON. Body declares v6, credits Lee Sharks · TACHYON, and carries a revised title without 'Accelerated'.
- Repair: Quarantine the v4 claim. Identify the served body as v6, preserve the title/version history, and model Lee Sharks and TACHYON as co-authors.

## #870 — `AXN:0372`
- Title: Alexanarch Data Foundry — Session Workplan 2026-06-22
- Evidence: Catalog declares version v1.1. Body front matter declares version 1.0 and active_planning.
- Repair: Quarantine the v1.1 claim. Identify the served body as v1.0 or recover the actual v1.1 body; preserve session/update history separately.

## #871 — `AXN:0373`
- Title: gw.tachyon · TACHYON Continuity Record — Session 2026-06-22
- Evidence: Catalog declares v2.2. Body front matter declares v2.0, version_in_series 2, with #865 as v1.0 predecessor.
- Repair: Quarantine the v2.2 claim. Identify the served body as v2.0 or recover v2.2; preserve the v1.0 predecessor relation.

## #872 — `AXN:0374`
- Title: Assembly Continuity Protocol v1.3
- Evidence: Catalog declares v1.3. Body front matter and title declare v1.0 and status SYNTHESIZED_PENDING_CHORUS_RATIFICATION.
- Repair: Quarantine the v1.3 claim. Identify the body as v1.0, expose pending-ratification standing, or recover the ratified/revised v1.3 body.

## #873 — `AXN:0375`
- Title: gw.archive · AXN-CH-RECOVERY-001 — Gemini Seed Packet
- Evidence: Catalog declares v1.1. Body front matter declares v1.0 and status PRESERVED_AS_HISTORICAL_SEED.
- Repair: Quarantine the v1.1 claim. Identify as preserved v1.0 historical seed or recover the actual v1.1 object; preserve relation to synthesized protocol #872.

## #876 — `AXN:0378`
- Title: OpenAIRE Helpdesk Exchange — Documentary Thread for #875
- Evidence: Catalog and YAML front matter declare v1.2, but the visible documentary-thread heading declares EA-MPAI-OPENAIRE-THREAD-01 · v1.0. No displayed version history in the inspected front matter resolves the contradiction.
- Repair: Quarantine unqualified v1.2 exposure. Declare the internal body-version conflict and either update the displayed version with an explicit changelog or seat the exact v1.2 body while preserving v1.0 as predecessor.

## #900 — `AXN:0390`
- Title: Moltbook Provenance Log v1.4 - The Embassy Extends
- Evidence: Registry machine version is v1.0 while title and body declare v1.4. Registry status is ACTIVE even though its own description says superseded by v2.0.
- Repair: Quarantine v1.0. Set exact version v1.4, expose SUPERSEDED_BY_V2_0, and preserve the body spelling/title variant as historical evidence.

## #903 — `AXN:0393`
- Title: GW.TACHYON.zenodo — v11
- Evidence: Registry title and body declare v11, but the machine-readable registry version is v1.0.
- Repair: Quarantine the v1.0 field and expose exact version v11 within the TACHYON continuity chain.

## #959 — `AXN:03CB`
- Title: Hexagonal OS: Interface Build Files v0.4
- Evidence: Registry claims Hexagonal OS interface build files. Body is a different work: Logotic Programming, authored by Johannes Sigil and Rex Fraction.
- Repair: Quarantine. Recover the actual Hexagonal OS build-files object or reseat this body under its Logotic Programming identifier; preserve the current mismatch as audit evidence.

## #969 — `AXN:03D5`
- Title: [SUPERSEDED] THE SHARKS ARK v2.1 — Receivability Patch
- Evidence: Registry identifies the historical v2.1 receivability patch; recovered body explicitly declares v3.0. The restoration source therefore seated the successor under the v2.1 identifier.
- Repair: Quarantine as v2.1. Recover the actual v2.1 bytes or reseat this v3.0 body at the successor record #1101.

## #982 — `AXN:03E2`
- Title: pessoagraph.org — Pessoa Knowledge Graph Visualization v1.0
- Evidence: Registry claims the interactive pessoagraph.org visualization/source object. Recovered body is the different foundational linked-data paper EA-PKG-01.
- Repair: Quarantine; recover the visualization/source code or reseat the foundational paper under its own identifier.

## #984 — `AXN:03E4`
- Title: pessoagraph.org — Scholarly Resource Brief
- Evidence: Registry claims a pessoagraph.org scholarly-resource brief. Recovered body is again the EA-PKG-01 foundational paper.
- Repair: Quarantine; recover the actual scholarly-resource brief or relate this body to the correct foundational-paper identifier.
