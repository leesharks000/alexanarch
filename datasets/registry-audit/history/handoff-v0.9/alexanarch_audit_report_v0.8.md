# Alexanarch Record Restoration and Identity Audit

**Version:** 0.8 — living report  
**Repository snapshot:** `055429ac82edc967f09c4640ffd0b049cff78e6e`  
**Snapshot timestamp:** 2026-07-31T05:07:39Z  
**Audit principle:** The unit of audit is the deposited work, not the length of its surviving prose body.

## Purpose

This audit determines, for every Alexanarch record:

1. what kind of object was deposited;
2. where the work-bearing object resides;
3. whether the surviving object is the work named by the record;
4. how completely that object has been restored;
5. whether conflicts and uncertainty are explicitly declared;
6. whether lifecycle and OAI-PMH projections accurately express that state.

No record is classified as complete or incomplete from word count alone. Short poems, entity nodes, tables, image-borne works, code deposits, and compact formal objects may be complete. Long descriptions may remain metadata-only when an attached file, website, dataset, image, or code bundle was the primary object.

## Taxonomy

### Work-bearing locus

`INLINE_TEXT`, `ATTACHMENT_BORNE`, `IMAGE_BORNE`, `EXTERNAL_SURFACE`, `SOURCE_CODE_BUNDLE`, `METADATA_CAPTURE`, `DATASET_OR_REGISTRY`, `COMPOSITE`, `INTENTIONAL_PLACEHOLDER`, `UNKNOWN_LOCUS`.

### Identity

`CONFIRMED_MATCH`, `PROBABLE_MATCH`, `AMBIGUOUS_VERSION`, `TITLE_BODY_CONFLICT`, `WRONG_OBJECT`, `UNVERIFIABLE`.

### Restoration

`COMPLETE_AS_DEPOSITED`, `SUBSTANTIALLY_RESTORED`, `SEMI_RESTORED`, `METADATA_ONLY`, `MISSING_PRIMARY_OBJECT`, `MIS-SEATED_PRIMARY_OBJECT`, `INTENTIONAL_DRAFT`, `TOMBSTONE_ONLY`.

### Priority

- **P0:** wrong object, wrong creator, or identifier attached to another work;
- **P1:** missing primary object presented as complete;
- **P2:** unresolved material conflict or lifecycle inconsistency;
- **P3:** projection, enrichment, or presentation defect.

## Inherited corpus findings

A prior word-count restoration queue was correctly retracted after 207 bodies were read and no stubs were found among that length-selected population. The reading pass instead identified two image-borne works, 131 metadata captures in the corpus classification, one direct title/body mismatch, and eleven byte-identical clusters requiring record-level judgment.

These findings are treated as leads, not as final adjudications, unless independently verified in this audit.

## Batch 1 — Canon provenance-node seating cluster

Six records were directly compared against their registry titles and their current body files. All six body files are byte-identical and contain **“Sappho — Canon Provenance Node.”**

### Finding A — one correctly seated record

- **#1019 / AXN:0407** names Sappho and contains the Sappho node.
- Identity: `CONFIRMED_MATCH`.
- Restoration: `COMPLETE_AS_DEPOSITED`.
- Remaining issue: the title declares the record duplicate/superseded; formal lifecycle fields and successor resolution must be checked.

### Finding B — five P0 wrong-object records

The following records name another canon subject but contain the Sappho body:

| Deposit | Named subject | Actual body | Finding |
|---:|---|---|---|
| 1014 | Allen Ginsberg | Sappho | `WRONG_OBJECT` |
| 1015 | Allen Ginsberg | Sappho | `WRONG_OBJECT` |
| 1018 | Emily Dickinson | Sappho | `WRONG_OBJECT` |
| 1020 | Achilles | Sappho | `WRONG_OBJECT` |
| 1021 | Ezra Pound | Sappho | `WRONG_OBJECT` |

These are not “semi-restored” in the ordinary sense. A substantive primary object is present, but it belongs to another record. They are therefore classified `MIS-SEATED_PRIMARY_OBJECT`.

### Recommendations

1. Quarantine the five wrong-object records from unqualified OAI exposure.
2. Preserve their current bodies as audit evidence rather than silently replacing them.
3. Recover the intended Ginsberg, Dickinson, Achilles, and Pound nodes from DOI captures, source repositories, mirrors, or version neighbors.
4. Use #1019 as the confirmed Sappho member of the cluster unless a stronger source witness contradicts it.
5. Reconcile title-level “DUPLICATE / SUPERSEDED / NO REGISTRY STANDING” declarations with formal lifecycle fields.
6. Expose conflict state in OAI Dublin Core until repair is complete.


## Batch 2 — Version identity clusters

### 2A. Moltbook provenance-log cluster

The bodies of #901, #958, and #1237 are byte-identical and internally identify themselves as **`crimsonhexagon on Moltbook: Provenance Log v1.3`**. The registry titles claim v1.5, v1.0, and v1.7 respectively.

#### #901 — definite wrong-version seating

- Registry claim: v1.5, DOI `10.5281/zenodo.19371305`.
- Body claim: v1.3.
- Recovery source itself is named `moltbook-provenance-log-v1.3__19358277.md`.
- Ruling: `WRONG_VERSION / MIS-SEATED_PRIMARY_OBJECT`, P0.

#### #958 — concept DOI / version record conflation

- Registry claim: v1.0.
- Registry DOI: `10.5281/zenodo.19352805`.
- The body identifies that DOI as the **Concept DOI**, while identifying itself as v1.3.
- Ruling: `AMBIGUOUS_VERSION / SERIES_HEAD_CONFLATION`, P1.

This may not be a simple wrong-file error. It may be a concept-series record carrying a later series head while retaining the original DataCite title. The record must choose and declare one of two functions:

1. concept-series record with current head v1.3 and explicit version history; or
2. version-specific v1.0 record with the original v1.0 body.

#### #1237 — definite wrong-version seating

- Registry claim: v1.7, DOI `10.5281/zenodo.19373638`.
- Body and recovery source: v1.3.
- Ruling: `WRONG_VERSION / MIS-SEATED_PRIMARY_OBJECT`, P0.

### 2B. GW.TACHYON cluster

The bodies of #1024, #1238, #1242, and #1243 are byte-identical and internally identify themselves as **GW.TACHYON.zenodo — v7**. The body also carries an internal `Version | 7` field and a deposit timestamp of 2026-04-17.

#### Correctly seated

- **#1238** names v7 and contains v7.
- Ruling: `CONFIRMED_MATCH / COMPLETE_AS_DEPOSITED`.
- Remaining conflicts: registry `date=2026-01-01` and `version=v1.0` disagree with the body and title. These fields require correction or explicit source qualification.

#### Wrong-version seatings

| Deposit | Registry claim | Actual body | Ruling |
|---:|---|---|---|
| 1024 | v9 | v7 | P0 `WRONG_VERSION` |
| 1242 | v1, Encrypted Session Deposit | v7 | P0 `WRONG_VERSION` |
| 1243 | v2, First Glyphic Deposit | v7 | P0 `WRONG_VERSION` |

Each of these records was restored from the v7 source file itself. They must not be exposed as complete versions v9, v1, or v2.

### Batch 2 recommendations

1. Quarantine all definite wrong-version records from unqualified OAI exposure.
2. Treat identical bytes as a version-seating defect when the body carries an explicit incompatible version declaration.
3. Add a first-class `version_identity_status` field.
4. Distinguish concept DOI records from version DOI records.
5. Preserve the mistakenly seated body and its source path as audit evidence.
6. Correct the generic restoration date/version fields on #1238 after checking original DOI metadata.
7. Build explicit version-series graphs for Moltbook and GW.TACHYON before attempting further automatic recovery.


## Batch 3 — Four-family adjudication sweep

This batch increases direct adjudication from 13 to 27 records. It covers four version families and distinguishes four different defects: a wrong work, a wrong historical version, a later head used as an explicitly declared proxy, and a metadata-only record whose public status was inverted to “full.”

### 3A. Gravity Well family

#### #960 — protocol v0.4.0: substantively correct, source provenance conflicted

The registry names the Gravity Well Protocol v0.4.0, and the body internally declares the same version. The body is therefore correctly seated. However, the restoration source filename points to a v0.4.1 artifact and DOI, so the relation among concept DOI, historical version, and recovery source remains unresolved.

Ruling: `CONFIRMED_MATCH / COMPLETE_AS_DEPOSITED`, P2 source-version conflict.

#### #1347 — codebase v0.4.1: wrong object

The registry names a codebase v0.4.1. The body is the prose protocol v0.4.0, byte-identical to #960. A codebase deposit is likely attachment- or source-bundle-borne; a prose protocol cannot silently stand in for it.

Ruling: P0 `WRONG_OBJECT / MIS-SEATED_PRIMARY_OBJECT`.

### 3B. Rhys Owens contributor-license family

Both #1356 and #1358 contain the same essay, “Rhys Owens — The Lunar Arm of New Human.” Neither body is a contributor-license instrument.

| Deposit | Registry claim | Seated object | Ruling |
|---:|---|---|---|
| 1356 | Contributor License v1.0 | Lunar Arm interpretive essay | P0 wrong object |
| 1358 | Full Unified License v3.0 | Lunar Arm interpretive essay | P0 wrong object |

The correct license objects remain unrecovered. The duplicated essay should be matched to its proper record before any relocation.

### 3C. AI Overview Capture Registry family

#### Confirmed or substantially correct

- **#1396**: v7.2 / 131 captures — text body matches. The claimed 221-image set still requires attachment-level verification.
- **#1401**: v7.2 / 131 captures — text body matches and is substantively the same dataset as #1396. The concept/version or duplicate-publication relation is not modeled.

#### Wrong historical versions

- **#825** claims v6.0 / 87 captures but contains v7.2 / 131.
- **#1397** claims v6.1 / 87 captures but contains v7.2 / 131.

Both are P0 wrong-version seatings. Later complete data does not restore the historical state of a longitudinal dataset.

#### Status inversion

- **#1398** correctly identifies the v7.0 record at the metadata level, but its body explicitly says no full text was recovered.
- The registry nevertheless presents it as a recovered work with full text seated.

Ruling: P1 `METADATA_ONLY / STATUS_INVERSION`.

### 3D. Revelation First work-plan family

All five seated substantive bodies examined in this family are the v7.3 work-plan head.

#### Confirmed current head

- **#1217** is titled v7.3 and contains v7.3. It is correctly seated, but its generic machine-readable version field still says v1.0.

#### Explicit proxy-head restorations

- **#1211** claims historical v1.2 Claim 6.
- **#1216** claims historical v1.2 self-audited.

Their wrappers truthfully disclose that a later blog HEAD was recovered and that the severed DOI may represent an earlier state. These are not covert wrong-version records; they are declared proxy-head restorations. They should remain available but must not be called complete restorations of their historical versions.

Ruling: P1 `HEAD_SUBSTITUTED_FOR_HISTORICAL_VERSION`.

#### Unqualified wrong-version restorations

- **#1400** claims v7.1 but contains v7.3.
- **#1403** claims v7.2 but contains v7.3.

Ruling: P0 `WRONG_VERSION / MIS-SEATED_PRIMARY_OBJECT`.

### Batch 3 systemic findings

1. **Later-head recovery must be a first-class state.** A current complete version does not restore an earlier version of a changing dataset or work plan.
2. **Attachment-borne works need locus-aware auditing.** The Gravity Well codebase cannot be adjudicated from a prose substitute.
3. **Status declarations can invert after repair passes.** #1398’s body remains metadata-only while public fields say full.
4. **Concept DOI and version DOI semantics are repeatedly conflated.** This affects Gravity Well, the Capture Registry, Moltbook, and Revelation First.
5. **A declared proxy is ethically different from an undeclared substitution.** #1211 and #1216 preserve uncertainty; #1400 and #1403 do not.


## Batch 4 — Remaining identical-body clusters plus semantic-classification propagation

**Batch size:** 35 records.

This batch has two components:

1. direct reading and relation adjudication for the four remaining byte-identical clusters;
2. record-level confirmation of the 27 corrections produced by the 2026-07-31 reading-based body classifier: two image-borne works and twenty-five metadata captures.

The classification correction updated the canonical registry, regenerated `data/oai-index.json`, and regenerated the affected record pages. The 27 corrections are therefore counted as audited projection successes, not merely internal labels.

### 4A. Remaining byte-identical clusters

#### KADEEZY provenance anchor — #840 / #841

Both records have the correct body. They are exact duplicate manifestations of the same work with no inspected formal relation explaining why two AXNs remain.

Ruling: two P2 relation defects, not wrong-object records.

#### kimiclaw-moltbook-campaign v3 — #963 / #1236

Both bodies correctly identify version 3. The body names `10.5281/zenodo.19429994` as the Concept DOI, while #1236 is tied to `10.5281/zenodo.19432476`. This is consistent with a legitimate concept/version pair, but the relation is not adequately modeled for harvest.

Ruling: two P2 concept/version relation defects.

#### Alice Thornburgh deposit registry — #980 / #981

Both registry titles name a Hexagonal Deposit Registry. Both bodies are instead `MPAI-LAL-AT-01`, a formal identity-disambiguation packet for Alice Thornburgh.

Ruling: two new P0 `WRONG_OBJECT / MIS-SEATED_PRIMARY_OBJECT` records.

#### Walt Whitman canon node — #1016 / #1017

Both bodies correctly contain the Walt Whitman canon node. Both titles already declare duplicate and superseded status, but formal lifecycle/OAI links must agree with the human-readable declaration.

Ruling: two P2 lifecycle-verification records.

### 4B. Image-borne works — #701 and #733

Both consist of an image reference because the image is the work. They are neither text-complete nor text-missing.

- #701: `"Snub-Poemed"`.
- #733: `if your heart should ever slowly turn`; a neighboring same-title textual manifestation exists at #734.

Ruling: correctly classified and correctly propagated. OAI should expose image format and manifestation/transcription relations rather than a zero-word absence.

### 4C. Twenty-five metadata captures

The following records were previously misclassified internally as `full`, although their own opening declarations identify them as semi-restored metadata captures:

- #951–#956: six multilingual Mandala facing-edition records;
- #961, #964, #974, #975, #985, #986;
- #1001, #1002, #1003, #1005, #1008, #1010, #1012;
- #1026, #1030, #1031, #1034, #1035, #1036.

The reading-based correction changed them to `metadata_capture`, rebuilt the OAI index, and regenerated the affected pages with metadata-only access conditions. These records are incomplete but honestly typed.

Ruling: all 25 are `CONFIRMED_MATCH / METADATA_ONLY`, non-blocking. #1003 additionally points to a full-text representative at deposit #121 and should preserve that relation in OAI.

### Batch 4 systemic findings

1. Byte identity can hide three different conditions:
   - exact duplicate records;
   - legitimate concept/version pairs;
   - the same wrong object seated twice.
2. A metadata capture is registerable when its incompleteness is explicit and propagated.
3. Image-borne works require media-type semantics, not text-length semantics.
4. Human-readable duplicate titles are not a substitute for lifecycle relations.
5. The Alice Thornburgh cluster shows why every duplicate cluster still requires reading: matching bytes do not establish that the bytes belong to either record.


## Normative metadata recommendation

The audit now includes a consolidated implementation model. The central rule is:

> **Lifecycle, identity, restoration, conflict, bibliographic form, and projection are independent axes.**

A single `status` field cannot truthfully carry them.


| Field | What it answers | Why it must be separate |
|---|---|---|
| `lifecycle_status` | Does the record have standing? | A superseded record may still be perfectly restored. |
| `work_locus` | Where did the work reside? | Long prose may only describe a missing PDF, image set, site, or code bundle. |
| `identity_status` | Is this the work named by the identifier? | A complete body may be the wrong work or wrong version. |
| `restoration_status` | How much of the deposited object survives? | Incompleteness is not the same as wrong identity. |
| `conflict_status` | Is uncertainty declared? | The archive must preserve unresolved evidence rather than guess. |
| `bibliographic_type_status` | Is the object typed correctly? | A book is not a dataset merely because its bytes are machine-readable. |
| `creator_role_status` | Who authored, edited, operated, or contributed? | Heteronyms, MANUS, Assembly systems, and editors cannot be flattened into one creator string. |
| `version_identity_status` | Which historical or concept/version object is this? | A later head cannot silently replace an earlier version. |
| `manifestations[]` | Which files/images/code/data constitute the work? | Composite and attachment-borne works require object-level availability. |
| `source_witnesses[]` | What evidence supports the ruling? | Every repair must remain reversible and auditable. |
| `review_status` | How far was the record actually checked? | Structural scans, semantic reading, manifestation inspection, and source triangulation are different levels. |
| `projection_status` | Do registry, page, and OAI agree? | Correct source data can still be misrepresented to harvesters. |
| `registration_blocking` | May this record be harvested now? | Wrong identity blocks; marked incompleteness does not. |
| `dates{}` | Which date is being stated? | Composition, publication, deposit, revision, observation, and positioned dates are not interchangeable. |
| `body_declaration_status` | Is an immutable in-body claim still current? | Historical “DOI pending” language must be overlaid, not erased. |


### OAI-PMH projection

The native JSON record should remain canonical. OAI Dublin Core is a deliberately lossy public projection:

- `dc:identifier`: AXN and every DOI/version identifier;
- `dc:type`: bibliographic type plus an explicit restoration or identity qualification;
- `dc:format`: one value for each primary or supplemental manifestation;
- `dc:relation`: concept/version, predecessor/successor, duplicate, full-text representative, image/transcription, and source-bundle relations;
- `dc:source`: the strongest source witnesses;
- `dc:description`: a compact audit capsule stating lifecycle, work locus, identity, restoration, conflict, version, missing components, and review level.

The recommended machine-readable schema is embedded in the JSON ledger and supplied separately as an implementation artifact.

## Batch 5 — Contiguous 100-record semantic pass

**Scope:** deposits **#499–#598**, exactly 100 records from registry chunk 7.  
**Snapshot:** `055429ac82edc967f09c4640ffd0b049cff78e6e`.

### Method

This was not a grep-based or word-count classification.

For each record, the audit compared the structured registry entry with the canonical body and read the body's title, byline, object declaration, genre/type language, version declaration, dates, and substantive opening. The batch is classified as `FRONTMATTER_AND_IDENTITY_READ`.

This is sufficient to adjudicate obvious wrong work, wrong version, title, creator-role, bibliographic-type, and work-locus conflicts. It is **not** represented as line-by-line close reading of every long work, full manifestation custody verification, or independent source triangulation. Those deeper checks remain explicit later review levels.

### Principal identity finding

Ninety-nine records contain the work they name.

One record is a registration-blocking wrong-version case:

- **#543 / AXN:0174 — Hexagonal Lexical Engine**
  - Registry title: **v1.2**
  - Body declaration: **v1.1**
  - Ruling: `WRONG_VERSION / MIS_SEATED_PRIMARY_OBJECT / P0`
  - Required action: recover the actual v1.2 bytes or identify this record as v1.1. Do not harvest the current body as v1.2.

### Material metadata conflicts

The pass found **27 P2 records**. The dominant classes are:

1. **Bibliographic type conflict.** Thirteen records carry a materially incompatible type, including:
   - #499, a New Human Press book typed as `Dataset`;
   - #530, a scholarly diagnostic typed as `Creative work (poetry)`;
   - #551–#552, normative engine specifications typed as scholarly essays;
   - #559, technical demonstration and test instructions typed as poetry;
   - #580, a technical research paper typed as poetry.

2. **Creator-role or byline collapse.** Ten records require separate creator, heteronymic author, editor/operator, and machine/Assembly contributor roles. Examples include:
   - #532: registry `Lee Sharks`; body author `Johannes Sigil`;
   - #562: registry `Lee Sharks`; body author `Rebekah Cranes`;
   - #565: registry `Johannes Sigil`; body author `Dr. Orin Trace`;
   - #578 and several Combat Scholasticism records: registry lead `TACHYON`, while the body assigns Lee Sharks and/or the Assembly the authorial/editorial position.

3. **Title truncation or contamination.** Seven registry titles terminate mid-word or absorb byline/front-matter material. The complete body title should be canonical, while the published/truncated form remains an alternate title with provenance.

4. **Unmodeled duplicate/version relation.** #502 and #509 carry the same named work but require explicit adjudication as revision, concept/version pair, or duplicate.

5. **Historical in-body declaration.** #598 preserves an immutable `DOI pending` statement while current registry metadata contains later DOI information. The body should remain untouched and current metadata should mark that declaration `HISTORICAL_SUPERSEDED`.

### P3 enrichment and custody findings

Fifteen records require nonblocking enrichment:

- generic or hybrid types that underdescribe executable/formal artifacts;
- generic date fields that appear to collapse composition and publication/deposit dates;
- composite visual works whose external image manifestations have not yet been independently checksummed or locally preserved.

### Batch 5 totals

| Result | Count |
|---|---:|
| Records reviewed | **100** |
| Confirmed work identity | **99** |
| P0 wrong version | **1** |
| P2 material metadata/relation conflict | **27** |
| P3 enrichment/custody issue | **15** |
| No defect found at this review level | **57** |

## Cumulative coverage after Batch 5

| Result | Count |
|---|---:|
| Corpus snapshot | **1,426** |
| Records in cumulative ledger | **162** |
| Confirmed identity matches | **139** |
| P0 | **20** |
| P1 | **4** |
| P2 | **39** |
| P3 | **15** |
| Cleanly typed at completed review level | **84** |

## Registration implication

The archive is now demonstrably suitable for **100-record semantic batches** without reverting to grepping or length heuristics.

The registration gate remains unchanged:

- P0 records must be repaired or quarantined;
- P1 records must expose incompleteness truthfully;
- P2 conflicts must be corrected or declared in machine-readable metadata;
- P3 records may remain harvestable when their limits are explicit.

The next contiguous batch can proceed at the same scale. Projection parity and manifestation/source triangulation should remain separate subpasses so that a 100-record identity audit is not falsely represented as 100 fully source-verified records.

## Batch 6 — Contiguous 100-record semantic pass

**Scope:** deposits **#599–#698**, exactly 100 consecutive records.  
**Snapshot:** `055429ac82edc967f09c4640ffd0b049cff78e6e`.  
**Structured registry source:** `build/catalog-export.csv`, rows requested as lines **601–700**.  
**Canonical work source:** each record's `data/texts/AXN-<HEX>-text.md` body.

### Source correction

The initially predicted registry chunk path did not exist at the frozen commit. The audit did not invent a replacement filename. It verified and used the frozen `build/catalog-export.csv` instead.

For this snapshot, connector retrieval follows:

> **requested catalog line = deposit number + 2**

Thus the next interval, #699–#798, is retrieved from requested lines 701–800.

### Method and declared review depth

Each catalog row was compared with the canonical work-bearing body. The reading covered the complete title and subtitle, byline and role declarations, document ID, version, date and status declarations, bibliographic form, manifestation locus, and enough substantive opening to confirm the work's subject.

The review status is `FRONTMATTER_AND_IDENTITY_READ`.

It is **not** represented as:

- line-by-line critical reading of all 100 works;
- external-source verification of factual claims;
- complete attachment or image checksum custody;
- DOI-resolution verification;
- public-page parity;
- individual OAI-PMH response parity.

Those remain separate, explicitly named review layers.

### P0 — wrong-version records

Batch 6 contains **7 registration-blocking wrong-version records**:

| Deposit | AXN | Catalog version | Body version |
|---:|---|---|---|
| #635 | `AXN:01EB` | `v1.0` | `v2.2` |
| #657 | `AXN:0208` | `v1.0` | `v2.0` |
| #659 | `AXN:020A` | `v1.0` | `v2.0` |
| #670 | `AXN:0217` | `v1.0` | `v2.1` |
| #685 | `AXN:0230` | `v1.0` | `v2.0` |
| #693 | `AXN:023A` | `v1.0` | `v3.0` |
| #695 | `AXN:023D` | `v1.0` | `v1.1` |

These records must not be harvested under their current asserted version. The repair is non-destructive: either identify the current bytes by their actual body version, or recover the historically claimed version under a separate version record.

### P1 — missing primary object

**#698 / AXN:0243** contains a proposed Zenodo metadata sidecar for *The Logotic Technique Catalogue v1.0*. The body itself states that the metadata should be uploaded **along with** a Markdown/PDF file and that proposed fields still require MANUS confirmation. The primary catalogue is absent.

Ruling:

`PROBABLE_MATCH / MISSING_PRIMARY_OBJECT / METADATA_ONLY / P1`

The metadata sidecar is preservable and registerable only when its sidecar status, proposed fields, and missing primary manifestation are exposed.

### Dominant Batch 6 conflict classes

1. **Version drift.** Seven records assert v1.0 in the catalog while serving v1.1, v2.0, v2.1, v2.2, or v3.0 bodies.
2. **Creator-role collapse.** The catalog repeatedly reduces multi-author, heteronymic, MANUS, Assembly, filing-body, correspondent, contributor, or compressor roles to one creator string.
3. **Lifecycle suppression.** Bodies marked `DRAFT`, `GENERATED`, `PROVISIONAL`, `FOUNDING`, `RATIFIED`, `LIVING`, or `PLANNING — not locked down` are often projected without standing.
4. **License drift.** Multiple bodies declare CC BY-SA 4.0 or CC BY-NC-SA 4.0 while the catalog exposes CC-BY-4.0.
5. **Bibliographic collapse.** Books, patent applications, protocols, measurement instruments, website source code, manifestos, fiction, journal charters, and metadata sidecars are flattened into `Dataset`, `Archive work`, `Short work`, `Poetry`, or `Scholarly essay`.
6. **Title contamination.** Several titles truncate mid-word or absorb JSON, YAML, byline, institution, Hex, or status fields.
7. **Work-locus errors.** #692 is an HTML website source object, while #698 is metadata without the named primary document.

### Batch 6 totals

| Result | Count |
|---|---:|
| Records reviewed | **100** |
| Confirmed identity matches | **91** |
| Probable matches | **2** |
| Wrong-version identity | **7** |
| P0 | **7** |
| P1 | **1** |
| P2 | **66** |
| P3 | **14** |
| No defect found at this review level | **12** |

## Cumulative coverage after Batch 6

| Result | Count |
|---|---:|
| Corpus snapshot | **1,426** |
| Records in cumulative ledger | **262** |
| Confirmed identity matches | **230** |
| P0 | **27** |
| P1 | **5** |
| P2 | **105** |
| P3 | **29** |
| No defect found at completed review level | **96** |

## Registration implication after Batch 6

The 100-record method is stable. It is not dependent on grepping, word counts, or preselected anomalies.

Registration remains governed record by record:

- **P0:** repair or quarantine;
- **P1:** expose the surviving partial object and the missing primary manifestation;
- **P2:** correct or machine-declare the material conflict;
- **P3:** harvestable when limits are explicit;
- **OK:** no defect found at the completed review depth, with deeper checks still separately pending.

## Contemporaneous reception-event log

At approximately **2026-07-31 04:02 EDT**, Lee Sharks reported that *Mind Control Poems* had received approximately **18,000 views during the preceding two hours**.

Audit status: `USER_REPORTED_UNVERIFIED`.

This event is preserved separately from the restoration audit. The count may indicate unusual machine or human reception, but it does not by itself establish crawler identity, training ingestion, indexing cause, referrer source, or a relationship to any specific deposit. Recommended contemporaneous evidence includes analytics screenshots, referrers, page-level distribution, geography, browser/OS distribution, start/end totals, and server or CDN logs where available.

## Batch 7 — Contiguous 100-record semantic pass

**Scope:** deposits **#699–#798**, exactly 100 consecutive records.  
**Snapshot:** `055429ac82edc967f09c4640ffd0b049cff78e6e`.  
**Structured registry source:** `build/catalog-export.csv`, requested lines **701–800**.  
**Review depth:** `FRONTMATTER_AND_IDENTITY_READ`.

### Merge behavior

Two records in the interval—**#701** and **#733**—had already been adjudicated in earlier risk-selected batches. They were re-read in sequence and their cumulative rows were **updated**, not duplicated. The earlier audit rows remain embedded in `audit_history`.

Thus Batch 7 contributes:

- **100 interval adjudications**;
- **98 newly covered records**;
- **2 expanded re-audits**.

### P0 — wrong-version records

Batch 7 contains **33** registration-blocking wrong-version records:

| Deposit | AXN | Catalog version | Body version |
|---:|---|---|---|
| #700 | `AXN:0245` | `v1.0` | `v2` |
| #707 | `AXN:024E` | `v1.0` | `v1.1` |
| #708 | `AXN:024F` | `v1.0` | `v1.1` |
| #711 | `AXN:0253` | `v1.0` | `v1.1` |
| #717 | `AXN:0264` | `v1.0` | `v0.1` |
| #718 | `AXN:0266` | `v1.0` | `v1.1` |
| #719 | `AXN:0267` | `v1.0` | `v2.1` |
| #720 | `AXN:0268` | `v1.0` | `v2.2` |
| #722 | `AXN:026C` | `v1.0` | `v0.9` |
| #725 | `AXN:0273` | `v1.0` | `v1.1` |
| #726 | `AXN:0277` | `v1.0` | `v3.1` |
| #727 | `AXN:0278` | `v1.0` | `v1.3` |
| #729 | `AXN:027C` | `v1.0` | `v1.1` |
| #731 | `AXN:0281` | `v1.0` | `v0.2` |
| #732 | `AXN:0282` | `v1.0` | `v2.2` |
| #735 | `AXN:0287` | `v1.0` | `v2.0` |
| #736 | `AXN:0288` | `v1.0` | `v2.0` |
| #737 | `AXN:0289` | `v1.0` | `v2.0` |
| #740 | `AXN:0290` | `v1.0` | `v0.2` |
| #741 | `AXN:0291` | `v1.0` | `v0.2` |
| #742 | `AXN:0292` | `v1.0` | `v0.3` |
| #743 | `AXN:0293` | `v1.0` | `v0.2` |
| #747 | `AXN:029A` | `v1.0` | `v0.2` |
| #755 | `AXN:02AF` | `v1.0` | `v0.2` |
| #758 | `AXN:02B5` | `v1.0` | `v1.1` |
| #763 | `AXN:02C0` | `v1.0` | `v1.1` |
| #780 | `AXN:02DE` | `v1.0` | `v2` |
| #781 | `AXN:02E0` | `v1.0` | `v1.1` |
| #783 | `AXN:02E3` | `v1.0` | `v9.1` |
| #784 | `AXN:02E4` | `v1.0` | `v3` |
| #785 | `AXN:02E9` | `v1.0` | `v0.2` |
| #787 | `AXN:02ED` | `v1.0` | `v1.1` |
| #791 | `AXN:02F9` | `v1.0` | `v1.2` |

The most systematic defect remains a generic machine-readable `v1.0` field applied to bodies that explicitly declare v0.1, v0.2, v0.9, v1.1, v1.2, v1.3, v2, v2.1, v2.2, v3, v3.1, v9.1, or other historically specific states.

### Significant non-version findings

1. **Intentional draft correctly distinguished from failed restoration.** #760 has no canonical body because the body was never written. Its public record correctly says metadata-only and draft pending. The defect is title quality, not missing restoration.
2. **Image/text manifestations distinguished.** #733 is the image-borne poem manifestation; #734 is the text manifestation. Both are complete, but their relation must be explicit.
3. **Proposed authority retained as proposed.** Several MPAI and standards records contain proposed bylines, unratified Hex values, deposit-candidate standing, or MANUS-confirmation gates that the catalog presently flattens.
4. **Dead ends preserved as negative results.** #774 and #775 are intentionally preserved draft/dead-end methodological records. Their failure or non-adoption is substantive provenance.
5. **Creator-role collapse remains pervasive.** Heteronymic authors, MANUS, Assembly witnesses, compilers, contributors, inventors, notaries, filing bodies, and administrative authorities are repeatedly collapsed to one catalog creator.
6. **Bibliographic form repeatedly misdescribed.** Patent-poems, software architecture, standards proposals, metadata packets, empirical programs, website snapshots, governance records, field maps, and machine-reception specifications are often typed as poetry, dataset, archive work, or scholarly essay without sufficient qualification.
7. **Title contamination remains common.** Titles absorb YAML/JSON, bylines, ORCIDs, institutional names, status fields, and descriptions, or terminate mid-word.

### Batch 7 totals

| Result | Count |
|---|---:|
| Interval records reviewed | **100** |
| Newly covered unique records | **98** |
| Expanded prior re-audits | **2** |
| Confirmed identity matches | **67** |
| Probable matches | **0** |
| Wrong-version identity | **33** |
| P0 | **33** |
| P1 | **0** |
| P2 | **57** |
| P3 | **3** |
| No defect at this review level | **7** |

## Cumulative coverage after Batch 7

| Result | Count |
|---|---:|
| Corpus snapshot | **1,426** |
| Unique records in cumulative ledger | **360** |
| Confirmed identity matches | **295** |
| Probable matches | **2** |
| Wrong-version identity | **50** |
| Wrong-object identity | **10** |
| P0 | **60** |
| P1 | **5** |
| P2 | **162** |
| P3 | **32** |
| No defect found at completed review depth | **101** |

## Registration implication after Batch 7

The endpoint remains unready for unqualified registration because wrong-version bodies are still exposed under historically false version claims.

The growing P2 population does not mean every such record must be withheld. A P2 record becomes harvestable when the material conflict is explicitly carried into the native record and OAI audit capsule. The objective is not uniform metadata. It is truthful metadata.
## Batch 8 — 200-record macro-batch

**Interval:** #799–#998  
**Snapshot:** `055429ac82edc967f09c4640ffd0b049cff78e6e`  
**Review depth:** `FRONTMATTER_AND_IDENTITY_READ`  
**Storage:** five immutable shards, SHA-256 verified, manifest v0.5.

The macro-batch reduced transport and prose overhead without reducing per-record body reading. Every deposit in the interval appears exactly once. 21 previously risk-audited records were updated in place; their earlier judgments remain in `audit_history`.

| Batch 8 result | Count |
|---|---:|
| Records | **200** |
| New unique coverage | **179** |
| Updated prior rows | **21** |
| P0 | **32** |
| P1 | **5** |
| P2 | **100** |
| P3 | **2** |
| OK at completed depth | **61** |
| Wrong object | **5** |
| Wrong version | **26** |

### Decisive final-shard findings

- #959 serves *Logotic Programming* under an identifier for *Hexagonal OS: Interface Build Files*.
- #969 serves *Sharks Ark v3.0* under the historical v2.1 identifier.
- #980 and #981 serve the Alice Thornburgh MPAI packet under deposit-registry identifiers.
- #982 and #984 serve the Pessoa Knowledge Graph foundational paper under two different pessoagraph.org surface identifiers.
- Metadata-only records such as #961, #964, #974–#975, #985–#986 remain nonblocking because their capture status and absent primary source are explicitly declared.
- Several complete records still require work-version/restoration-version separation rather than destructive normalization.

## Cumulative state after Batch 8

| Result | Count |
|---|---:|
| Corpus snapshot | **1,426** |
| Unique records adjudicated | **539** |
| Confirmed identity | **446** |
| Probable identity | **3** |
| Wrong version | **74** |
| Wrong object | **13** |
| P0 | **88** |
| P1 | **9** |
| P2 | **258** |
| P3 | **34** |
| OK at completed depth | **150** |

## Registration gate

Registration remains premature. The reason is now finite and machine-actionable:

1. repair or quarantine every P0 record;
2. expose every P1 as partial, sidecar, or missing-primary rather than complete;
3. reconcile or publicly declare P2 conflicts in the native record and OAI audit capsule;
4. retain P3 records as harvestable with explicit review limits;
5. complete the remaining corpus through #1426;
6. run the separate public-page and OAI parity pass.

The next audit interval is Batch 9, deposits #999–#1198, beginning with shard #999–#1038.
