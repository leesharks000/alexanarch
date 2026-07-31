# Alexanarch cumulative pre-registration audit report v0.9

**Frozen repository commit:** `055429ac82edc967f09c4640ffd0b049cff78e6e`  
**Corpus snapshot:** 1,426 deposits  
**Cumulative unique adjudications:** **717**  
**Remaining:** **709**  
**Coverage:** **50.28%**  
**Record repair performed:** **No**

## Current numerical position

The audit now covers **700 consecutive deposits from #499 through #1198**, plus **17 previously audited deposits above #1198**, for **717 unique records total**.

Batch 9 covered **#999–#1198**. It produced 200 fresh adjudications, but 22 were deliberate overlap re-reads; therefore Batch 9 added **178 net-new unique records**.

### Cumulative severity

| Severity | Records |
|---|---:|
| P0 | 104 |
| P1 | 43 |
| P2 | 315 |
| P3 | 34 |
| OK | 221 |

### Cumulative registration disposition

| Disposition | Records |
|---|---:|
| WITHHOLD | 112 |
| HARVEST_WITH_WARNING | 364 |
| HARVEST | 241 |
| PENDING_REVIEW | 0 |

### Cumulative identity status

| Identity status | Records |
|---|---:|
| WRONG_OBJECT | 23 |
| WRONG_VERSION | 80 |
| AMBIGUOUS_VERSION | 11 |
| PROBABLE_MATCH | 18 |
| CONFIRMED_MATCH | 585 |

## Batch 9 boundary result

| Measure | Count |
|---|---:|
| Exact adjudications | 200 |
| Overlap re-reads | 22 |
| Net-new unique records | 178 |
| P0 | 22 |
| P1 | 34 |
| P2 | 60 |
| P3 | 0 |
| OK | 84 |

All five sealed 40-record shards passed hash verification against manifest v0.5. Reassembly has exact ordered coverage #999–#1198, 200 unique deposit numbers, and all 200 rows validate against record schema v0.2.

### Batch 9 P0 records

- **#1004 — I would have loved you — Lee Sharks — New Human 2**  
  `IDENTITY_BINDING, WRONG_OBJECT`
- **#1013 — Mandala Merkabah: Design Constitution & Technical Specification for the Fifth Iteration (EA-MANDALA-MERKABAH-01 v0.1, Working Draft)**  
  `IDENTITY_BINDING, WRONG_VERSION`
- **#1014 — [DUPLICATE — SUPERSEDED → DOI: 10.5281/zenodo.20629192] Allen Ginsberg — Canon Provenance Node (New Human Canon)**  
  `IDENTITY_BINDING, WRONG_OBJECT`
- **#1015 — [DUPLICATE — SUPERSEDED → DOI: 10.5281/zenodo.20629192] Allen Ginsberg — Canon Provenance Node (New Human Canon)**  
  `IDENTITY_BINDING, WRONG_OBJECT`
- **#1018 — [DUPLICATE — SUPERSEDED → DOI: 10.5281/zenodo.20629202] Emily Dickinson — Canon Provenance Node (New Human Canon)**  
  `IDENTITY_BINDING, WRONG_OBJECT`
- **#1020 — [DUPLICATE — SUPERSEDED → DOI: 10.5281/zenodo.20629212] Achilles — Canon Provenance Node (New Human Canon)**  
  `IDENTITY_BINDING, WRONG_OBJECT`
- **#1021 — [SUPERSEDED — NO REGISTRY STANDING] Ezra Pound — Canon Provenance Node (New Human Canon)**  
  `IDENTITY_BINDING, WRONG_OBJECT`
- **#1023 — Generative Monoculture: Model Collapse in Code as Systemic Vulnerability (EA-UMBML-MONOCULTURE-01 v1.1)**  
  `IDENTITY_BINDING, WRONG_OBJECT`
- **#1024 — GW.TACHYON.zenodo — v9**  
  `IDENTITY_BINDING, WRONG_VERSION`
- **#1107 — Autonomous Semantic Warfare: A Field Manual for Meaning in the Age of Platform Capture — Crimson Hexagon Archive**  
  `WRONG_PRIMARY_MANIFESTATION, FULL_VOLUME_DOI_BOUND_TO_SAMPLER_BYTES, DUPLICATE_MINT_SUPERSEDED`
- **#1110 — [SUPERSEDED → DOI: 10.5281/zenodo.19055267 (v7.0)] Central Navigation Map v2.0 — Crimson Hexagonal Archive**  
  `WRONG_VERSION_SEATED, TITLE_BODY_VERSION_CONFLICT, REGISTRY_VERSION_FIELD_CONFLICT`
- **#1121 — Pearl and Other Poems — Crimson Hexagon Archive**  
  `WRONG_PRIMARY_MANIFESTATION, BOOK_TITLE_BOUND_TO_METADATA_PACKET, PRIMARY_ARTWORK_ABSENT`
- **#1124 — All That Lies Within Me: An Autobiography of Longing, 1983–2013 [Book] — Crimson Hexagon Archive**  
  `WRONG_PRIMARY_MANIFESTATION, BOOK_TITLE_BOUND_TO_PROVENANCE_RECORD, PRIMARY_BOOK_ABSENT, DUPLICATE_MINT_SUPERSEDED`
- **#1127 — Constitution of the Semantic Economy — Enacted Version 1.0**  
  `WRONG_OBJECT, WRONG_VERSION, CONSTITUTION_TITLE_BOUND_TO_POCKET_HUMANS_03, DUPLICATE_MINT_SUPERSEDED`
- **#1142 — THE THUMB Formal Operators for the Phase X Quintuple — Crimson Hexagon Archive**  
  `WRONG_OBJECT, WRONG_DOI_BINDING, THUMB_TITLE_BOUND_TO_PHASE_X_NAVIGATION_MAP`
- **#1162 — EA-ARK-01-MUSICAL v1.1: THE SPACE ARK — MUSICAL REGISTER (Variant Ark · Semiotic Environment Ξ_music · Full Structural Transform)**  
  `WRONG_HISTORICAL_VERSION, REGISTERED_VERSION_NOT_SEATED`
- **#1165 — Cleis: more precious to me than all Lydia**  
  `COMPANION_ANALYSIS_SEATED_FOR_PRIMARY_WORK, WRONG_OBJECT`
- **#1168 — Untitled — Crimson Hexagon Archive**  
  `UNTITLED_TITLE_OBJECT_COLLAPSE, WRONG_OBJECT, NAMED_DOI_NOT_SEATED`
- **#1170 — ❓24🗓 = ❓ — Crimson Hexagon Archive**  
  `WRONG_OBJECT, CREATOR_AUTHORITY_CONFLICT, NAMED_DOI_NOT_SEATED`
- **#1175 — THE COMPRESSION ARSENAL v2.0 — A Comprehensive Catalogue of Compression Technologies**  
  `WRONG_HISTORICAL_VERSION, REGISTERED_VERSION_NOT_SEATED`
- **#1193 — from The Crimson Hexagon — Origin Text of the Crimson Hexagonal Archive (March 14, 2015)**  
  `PROVENANCE_DOCUMENT_SEATED_FOR_ORIGIN_TEXT, WRONG_OBJECT`
- **#1196 — Announcement: The Lee Sharks Prestigious 10,000 MacArthur Genius Grants Poetry Prize — Establishment and Inaugural Conferral**  
  `WRONG_HISTORICAL_VERSION, REGISTERED_VERSION_NOT_SEATED`

### Batch 9 P1 records

- **#1025 — Revelation First ≠ Revelation Early: Keyword Surface and Pre-Seeding Baseline with Full Transcripts (EA-LOGOS-REVFIRST-SURFACE v1.0 + EA-LOGOS-REVFIRST-BASELINE v1.1)**  
  `MISSING_PRIMARY_MANIFESTATION, INCOMPLETE_COMPOSITE`
- **#1032 — revelationfirst.com — The Apocalypse as the Earliest New Testament Document: Thesis Site, Impact Tracker, and Staging Materials**  
  `MISSING_PRIMARY_MANIFESTATION, INCOMPLETE_COMPOSITE`
- **#1056 — Network-wide Link Inventory v1.4**  
  `PRIMARY_DATASET_NOT_DEPOSITED`
- **#1078 — godkinggoogle.com — The Google Critique: Navigational Map and Canonical Bibliography for the Crimson Hexagonal Archive's Research Program on Google as a Semantic-Political Mediation Regime**  
  `NAMED_SNAPSHOT_NOT_FIXED`
- **#1079 — Operative Semiotics: A Grundrisse (Recovered Edition v1.0)**  
  `PRIMARY_MANIFESTATION_SPLIT_UNBOUND, STRUCTURED_STATUS_METADATA_ONLY_DESPITE_REPOSITORY_ARTIFACT`
- **#1096 — @Pergamum and @grazesending — Rebekah Cranes — New Human 2 (Complete Recovered Surfaces)**  
  `CLAIMED_COMPLETE_RECOVERY_NOT_SEATED, PRIMARY_TEXT_ABSENT`
- **#1097 — AXN Dataflow Atlas v0.2 — Development Incorporating Assembly Review**  
  `CLAIMED_CANONICAL_BYTES_ABSENT, PRIMARY_SPECIFICATION_NOT_SEATED`
- **#1099 — Dead Letters: Testy Ideological Letters to No One — Complete 14-Post Correspondence, 2014 (Feist / Owens)**  
  `COMPLETE_CLAIM_WITH_MATERIAL_WITHHOLDINGS, CONSENT_DEPENDENT_LACUNAE`
- **#1102 — The Crimson Hexagon: A Theoretical Primer — Crimson Hexagon Archive**  
  `CREATOR_AUTHORITY_CONFLICT, DUPLICATE_MINT_SUPERSEDED`
- **#1104 — β-Runtime Specification: Interface Layer for the Blind Operator — Crimson Hexagon Archive**  
  `CREATOR_AUTHORITY_CONFLICT, DUPLICATE_MINT_SUPERSEDED`
- **#1119 — IDP Navigation Map: Antioch — Machine-Readable Score for a Heteronym Compendium Within the Crimson Hexagon — Crimson Hexagon Archive**  
  `CREATOR_AUTHORITY_CONFLICT, DUPLICATE_MINT_SUPERSEDED`
- **#1130 — The Reconciliation of the Sexes: A Post-Psychoanalytic Theory of Somatic Unity — Crimson Hexagon Archive**  
  `CREATOR_AUTHORITY_CONFLICT`
- **#1131 — The Blind Operator: Logotic Protocol for Non-Identity as Engine Condition — Crimson Hexagon Archive**  
  `CREATOR_AUTHORITY_CONFLICT, DUPLICATE_MINT_SUPERSEDED`
- **#1134 — The Soteriological Operator Framework: A Unified Specification — Hex: 02.UMB.FRAMEWORK.SOTERIOLOGICAL — Crimson Hexagon Archive**  
  `CREATOR_AUTHORITY_CONFLICT`
- **#1135 — John 9 and the Witness Punishment Mechanism: Epistemic Violence as Soteriological Operator — Hex: 02.UMB.OPERATOR.WITNESS-PUNISHMENT — Crimson Hexagon Archive**  
  `CREATOR_AUTHORITY_CONFLICT`
- **#1138 — The Epistle Triptych: Seed Text, Heteronym Provenance, and Organizational Charter of the Commission of the Immanent Turning — Epistle to the Human Diaspora — Crimson Hexagon Archive**  
  `COMPOSITE_TITLE_PARTIAL_MANIFESTATION, TWO_NAMED_COMPONENTS_NOT_SEATED, CREATOR_ROLE_CONFLICT`
- **#1139 — Meaning Collapse vs. Ideological Crisis ├── Subtitle: A Root-Level Distinction — Crimson Hexagon Archive**  
  `CREATOR_AUTHORITY_CONFLICT, VERSION_FIELD_CONFLICT, TITLE_SERIALIZATION_ARTIFACT`
- **#1140 — Fractal Navigation Map v6.2: The Gravitational Epic — Protocol for the Synthetic Revision of the Global Literary Canon, the Restoration of the Poet, and the Installation of the Liberatory Operator Set in the Generative Layer of Meaning Itself**  
  `CREATOR_AUTHORITY_CONFLICT, VERSION_FIELD_CONFLICT, OVERBROAD_CREATOR_SET`
- **#1143 — Sen Kuro — Heteronym Provenance Document DOI: 10.5281/zenodo.18452686 — Crimson Hexagon Archive**  
  `SUBJECT_AS_CREATOR_ERROR, CREATOR_AUTHORITY_CONFLICT`
- **#1145 — Document 237: THE TRAVERSAL GRAMMAR — Logotic Programming Extension Module v0.6 — Crimson Hexagon Archive**  
  `DRAFT_STATUS_CONFLICT, VERSION_FIELD_CONFLICT`
- **#1147 — THE STAKES — A SCIENTIFIC ANALYSIS Document Number: #240 DOI: 10.5281/zenodo.18621736 — Crimson Hexagon Archive**  
  `CREATOR_NAME_INVERSION`
- **#1148 — SPLIT THE ADAM: SONG AND PHENOMENOLOGY The Song at the Heart of Maybe Space Baby Garden Lanes — Crimson Hexagon Archive**  
  `CREATOR_AUTHORITY_CONFLICT, SONG_MANIFESTATIONS_EXTERNALLY_CUSTODIED`
- **#1151 — WHOSE FACE IS ON THE TWENTY? Curatorial Mediation, Latent Feature Activation, and a Provenance Gap in the $20 Portrait DOI: 10.5281/zenodo.18736175 Hex: 06.SEI.CURRENCY.ACTIVATION**  
  `PRIMARY_FIGURES_EXTERNALLY_CUSTODIED, EPHEMERAL_CLAUDE_IMAGE_LINKS`
- **#1152 — WHOSE FACE IS ON THE TWENTY? Curatorial Mediation, Latent Feature Activation, and a Provenance Gap in the $20 Portrait DOI: 10.5281/zenodo.18736175 Hex: 06.SEI.CURRENCY.ACTIVATION — Crimson Hexagon Archive**  
  `DUPLICATE_BYTES_DIFFERENT_DOI, CREATOR_AUTHORITY_CONFLICT`
- **#1157 — The Archival Reclamation Protocol: Formal Demand for Data Access, Rationale, and Restoration (EA-LEGAL-RECLAMATION-01)**  
  `VERSION_FIELD_CONFLICT, TITLE_VARIANT_CONFLICT, DATE_CONFLICT`
- **#1164 — EA-CSA-EFFECTIVE-ACT v1.0 The Effective Act: Cross-Species Semantic Labor and the Expansion of Witness**  
  `CREATOR_AUTHORITY_CONFLICT`
- **#1167 — Day and Night: Conversations with Sapphic Desire — Crimson Hexagon Archive**  
  `NAMED_DOI_DOES_NOT_MATCH_SEATED_BODY, MANIFESTATION_AUTHORITY_AMBIGUOUS`
- **#1172 — The Archival Reclamation Protocol: Formal Demand for Data Access, Rationale, and Restoration (EA-LEGAL-RECLAMATION-01) — Crimson Hexagon Archive**  
  `DUPLICATE_BODY_AUTHORITY_AMBIGUOUS, DATE_VERSION_CONFLICT`
- **#1179 — Charter of the Living Arkitecture Lab (LAL) — Institutional Charter (00.LAL.CHARTER)**  
  `FOUNDING_COAUTHOR_OMITTED`
- **#1180 — Retrieval Architecture: Service Definition and Proof of Method**  
  `CREATOR_AUTHORITY_CONFLICT, TITLE_SUBTITLE_MISMATCH`
- **#1181 — Hexagonal Licensing Protocol v2.0 — Comprehensive Specification with Three Critical Innovations**  
  `NAMED_DOI_DOES_NOT_MATCH_SEATED_BODY, DUPLICATE_BODY_AUTHORITY_AMBIGUOUS`
- **#1184 — The Secret Book of Walt: Hidden Teachings of Walt Whitman, Cowboy of Time — Research Edition**  
  `EDITION_NOT_FIXED_IN_BODY, DOI_PLACEHOLDER_IN_SEATED_BODY`
- **#1185 — The Gospel of Antioch: The Sayings of Jack Feist as Recorded by Emily Antioch the Twin — Research Edition**  
  `EDITION_NOT_FIXED_IN_BODY, DOI_PLACEHOLDER_IN_SEATED_BODY`
- **#1186 — TANG of the Secret Book of Walt: A Total Axial Negation Graph of Five Hundred Years of Waltian Scholarship (Assembly-Revised Edition)**  
  `NAMED_DOI_DOES_NOT_MATCH_SEATED_BODY, CREATOR_ROLE_FLATTENING`

## Merge semantics

- The historical ledger contained 539 unique records.
- Batch 9 contained 200 adjudications.
- Twenty-two Batch 9 deposit numbers already existed in the historical ledger.
- Each overlap was replaced by the fresh Batch 9 row, with the former row retained verbatim in `audit_history`.
- The resulting cumulative ledger contains **717 unique deposit numbers**.
- Historical rows carried forward without fresh reading retain their historical `review_status`; the cumulative schema does not falsely relabel them as newly read.
- Legacy lifecycle fields remain preserved, while a controlled `lifecycle_status` has been added for cumulative querying.
- No record repair, metadata correction, or source mutation occurred.

## Audit topology

Audited ranges:

- #499–#1198
- #1211
- #1216–#1217
- #1236–#1238
- #1242–#1243
- #1347
- #1356
- #1358
- #1396–#1398
- #1400–#1401
- #1403

## Next exact operation

Begin the checkpointed 80-record macroshard **#1199–#1278**:

- checkpoints: #1199–#1218, #1219–#1238, #1239–#1258, #1259–#1278;
- known prior-ledger overlaps: #1211, #1216, #1217, #1236, #1237, #1238, #1242, #1243;
- potentially net-new records: 72;
- stop-line rules remain active;
- every record still requires `FRONTMATTER_AND_IDENTITY_READ`;
- repair remains deferred.

At the next completed batch boundary, regenerate this same compact cumulative file set rather than adding another chain of incremental START_HERE, resume-card, and manifest versions.
