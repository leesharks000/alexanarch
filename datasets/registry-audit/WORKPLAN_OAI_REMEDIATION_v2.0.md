# WORKPLAN — OAI Registration & Registry Remediation v2.0

**Status:** ACTIVE — this file is the source of truth for the repair program.
**Date:** 2026-07-31 · **v1.1 same day:** first-thread handoff stashed and verified · **v1.2 same day:** AXN identity policy drafted; traffic-event capture spec added · **v1.3 same day:** #1365 restored (repair ledger inaugurated, R-0001); attachments mechanism built; Phase 0 builder gating applied · **v1.4 same day:** workplan deposit un-held by MANUS and minted; EA-MRE-01 v1.1 provenance anomaly inscribed · **v1.5 same day:** anomaly RESOLVED (gapped-round parallel instance) and v1.1 RATIFIED by independent MANUS re-instruction; evidence captures attached to #1428; Files block moved to record-page foot per MANUS spec · **v1.6 (2026-08-01):** dispositions regenerated v2.0 from ledger v1.1 (928 entries; 273/527/128); OAI index rebuilt gated (1302 exposed); WAVE 1 APPLIED — 338 content_type rows, MANUS batch approval, repairs R-0002–R-0339 inscribed, date_modified bumped per row · **Maintainers:** MANUS (Lee Sharks, sole editorial authority) · TACHYON (Claude, repair engineering) · LABOR (ChatGPT, forward audit)
**Supersession rule:** at every completed phase or wave boundary, this file is regenerated in place with a version bump. Prior versions are retained in git history only. Any instance resuming work reads this file first, in full, before acting.

---

## 1. Mission

Register the Alexanarch OAI-PMH endpoint honestly, and repair the audited registry behind it. The governing principle is the archive's own theory: the difference between marked and unmarked supply. The feed does not wait for a perfect corpus; it waits for a truthful one — damage excluded or declared, repairs inscribed, every change harvestable.

**Non-goals:** no repair of unaudited deposits; no metadata change without a sealed adjudication behind it; no change that touches the frozen audit source.

## 2. Decisions log

| Date | Ruling | By |
|---|---|---|
| 2026-07-31 | Gating policy: exclude WITHHOLD from the OAI index; include HARVEST and HARVEST_WITH_WARNING with audit-status sets and dc:description capsules; unaudited deposits included in set `audit:pending`. | MANUS |
| 2026-07-31 | Wave order and repair-ledger discipline adopted as specified in §8. | MANUS |
| 2026-07-31 | Creator policy: drafted at §7, **pending MANUS ratification** (rulings CP-R1–CP-R4). | — |
| 2026-07-31 | Registration proceeds after Phase 0 + validator pass; repair continues behind the registered feed via datestamp bumps. | MANUS |
| 2026-07-31 | First-thread handoff (v0.8 ledgers, Batch 8 seals, v0.8 repair queues, v0.9 handoff chain) stashed under `history/handoff-v0.9/`, hash-verified. Archival, not a merge: v0.9 cumulative already contains all 539 v0.8 rows (539 + 178 = 717, verified). | MANUS/TACHYON |
| 2026-07-31 | #1365 restored under its own AXN per MANUS ruling ("the stub is not the record; the record should be restored"): mirror seated as attached primary manifestation, Tier 2. Repair ledger inaugurated (R-0001). Attachments mechanism (`files/AXN-<HEX>/`, registry `files[]`, record-page buttons) built. Mirror corpus published with file, by ruling. Workplan deposit HELD from the record (file public in repo; not minted). | MANUS |
| 2026-07-31 | Workplan deposit un-held by MANUS ("lets get these things deposited"); minted as a dated v1.4 snapshot. The living copy at this path remains canonical-current per the supersession rule. | MANUS |
| 2026-07-31 | PROVENANCE ANOMALY inscribed: commit 478f0d2c (EA-MRE-01 v1.1, #1428) was created in the TACHYON working container by an unattributed operation — no hooks, no background processes, no invoked script accounts for it; repo git identity found pre-set to the MANUS name. Content verified accurate against session facts by TACHYON before push (end-of-day tally, non-reading accrual, DoS recharacterization, byte-history preservation all correct and in-convention). Shipped with this inscription; reversible via git revert 478f0d2c. RESOLVED same day: the commit is the work of the gapped conversational round — a parallel instance processed the MANUS message that never received a reply, and its side effects persisted in the shared working container. RATIFIED: MANUS independently re-instructed the identical change after the fact. Standing: authorized. | TACHYON (disclosed) |
| 2026-07-31 | Standing-rule carve-out: repair-follows-audit governs the remediation program's batch waves. MANUS retains direct editorial authority over specific records outside the queues; such acts are inscribed in the repair ledger with basis MANUS-DIRECTED. | MANUS |
| 2026-08-01 | W1b APPROVED & APPLIED: 125 content_type rows (#359–#498). | MANUS/TACHYON |
| 2026-08-01 | W6 RULED & APPLIED — CONVENTION REVERSED: journal field carries FULL canonical names, abbreviation optionally in parentheses (exemplar: 'Machine-Mediated Reception Studies (MMRS)'). venues.json → v1.1. Applied to 511 rows in audited range; 358 rows outside range DEFERRED per repair-follows-audit. | MANUS/TACHYON |
| 2026-08-01 | BATCH-AUTHORITY RULING: MANUS is finite and rules by batch and by policy, never per-row. TACHYON executes the audit ledger's own recommendations where concrete. RECOVERY SOURCE PRIORITY for missing/wrong content: (1) in-repo staging, (2) GitHub repos (code/repo deposits), (3) past conversation threads (intermediary versions overwritten at blog), (4) blog, (5) MANUS directly — the missing-attachment class ONLY is approached individually with MANUS. | MANUS |
| 2026-08-01 | AUDIT ADVANCED: complete-thread handoff through 0359-0378 seated — 1,068/1,426 (74.89%), contiguous #359–#1426, frozen commit unchanged, 0 historical mismatches vs v1.1, method v0.4 no-drift verified. method_core_v0.4.md seated (pending shard cleared). Dispositions v3.0 (1068; 291/648/129). OAI index rebuilt (1302 exposed). Next checkpoint: #339–#358; remaining 358. | TACHYON |

| 2026-08-03 | **AUDIT COMPLETE (frozen corpus 100%)** — LABOR (ChatGPT) delivered the terminal #1–#18 checkpoint, closing the #1–#358 range. Full frozen corpus #1–#1426 now reported 1,426/1,426 (100.00%) at commit 055429ac. Terminal #1–#18: 13 P1 + 5 P2, all HARVEST_WITH_WARNING (no P0). Cumulative severity OK 284 / P0 124 / P1 519 / P2 464 / P3 35; disposition HARVEST 304 / HARVEST_WITH_WARNING 991 / WITHHOLD 131. Completion report + START_HERE stashed. **DATA GAP:** the merged 1,426-row ledger and the #1–#358 row-level adjudications were NOT in the upload — only the narrative report came through. Our seated merged ledger still holds #359–#1426 only (1,068 rows). Repairs on #1–#358 remain BLOCKED until the row-level adjudications (or the cumulative ZIP's merged ledger + #1–#18 checkpoints) are seated. Narrative findings for #1–#18 are specific and recorded but are not a substitute for sealed rows. | TACHYON |

| 2026-08-03 | **DATA GAP CLOSED — full audit seated.** The complete-thread handoff ZIP (through_0001-0018) delivered the merged 1,426-row ledger + all 18 sealed checkpoints + frozen source; SHA256SUMS verified (31/31 OK). Merged ledger is contiguous #1–#1426, no gaps; #1–#358 adjudications now seated as real rows (e.g. #1 VERSION_IDENTITY_CONFLICT+DATE, #16 CREATOR_ROLE_REVERSAL, #18 CREATOR_ROLE_CONFLICT). Dispositions regenerated **v4.0** from the full 1426-row ledger (P0 124/P1 519/P2 464/P3 35/OK 284; HARVEST 304/HWW 991/WITHHOLD 131). Checkpoints stashed under checkpoints/through_0001-0018/. **#1–#358 repairs now UNBLOCKED** — the range has sealed row bases. The frozen corpus is fully audited AND repair-ready end to end. | TACHYON |

| 2026-08-03 | **SHAPE DOCTRINE + PROPAGATOR (repair-of-the-repair-process).** MANUS caught #1308 live serving FOUR states at once (semi-restored banner + Kim's captured abstract + old wiki + registry tombstone) — the registry-only tombstone had never reached staged text, page, wiki, chunks, or OAI; staged frontmatter even carried the archive ORCID on Kim's work. RULINGS RECORDED: controlled type vocabulary = YES (draft before the 159-row compound batch); creator-role projection = project declared roles per sealed rows. BUILT: RECORD-SHAPE-AND-PROPAGATION v1.0 (nine declaration sites; ordered pipeline; "no repair is complete until propagation has run") + scripts/propagate_record_state.py (one command: tombstone-text rewrite → status_reconcile → record pages → surfaces → central registry → OAI). RENDERER taught withdrawn_external (red tombstone banner, highest priority); OAI gate excludes withdrawn_external (feed 1301→1297). All four foreign tombstones fully propagated and verified: staged texts clean (zero foreign-ORCID), pages show tombstone banner, semi-restored banner gone. Sub-batch A (8 pure type normalizations) held to run THROUGH the propagator next round. | TACHYON |

| 2026-08-03 | **WAVE A-0358 OPENER (7 rows) — first repairs through the full §5b pipeline.** Type normalizations with explicit sealed targets applied: #219 scholarly essay, #221 consulting framework/strategic brief, #223 consulting white paper/business brief, #310 metadata packet, #340 canonical visual schema, #350 constitution/governance framework, #357 integrity-lock architecture (creators retained per rulings). #23 HELD (target unstated in sealed row — not guessed; queue hold noted). Step-4 verify CAUGHT a propagator defect on first run (entity-index path wrong → 6 page regens silently failed); fixed IN THE TOOL (data/entity-index.json), re-run, all 7 pages verified old-type=0/new-type>0. Ledger →1059. Pipeline is now self-tested. Remaining #1-#358: 159 compound rows await type-vocabulary ratification; 2 P0/WITHHOLD (#339,#356) await recovery-or-reID ruling; #23 held. | TACHYON |

| 2026-08-03 | **AUTHORIAL ROUND — masks + typographic sources.** (1) #331 Antioch: the repeated slur in the untuned-noise poem edited to r******d per MANUS (6 instances: 4× base form, 2× -ness form root-masked; prior bytes in git history per non-destruction); page verified 6 masks/0 unmasked. (2) #1374 (standalone UNTUNED/NOISE OF MYSELF) is metadata-only — SEAT-EDITED-ON-RESTORE hold inscribed so any future recovery seats the revised text, never unedited bytes. (3) Source .docx originals attached as typographic source of truth (markdown disrupts lineation/whitespace): #1267 xvi-a-transfiguration-source.docx, #1165 cleis-source.docx; Files sections + download links live on both pages. OUT-OF-SCOPE INSTANCES REPORTED, NOT EDITED: #1165 Cleis prose-confession carries a different clinical 11-letter term in a biographical passage; #620 carries a verbatim Thomas Schelling quotation — both await MANUS word if any action is wanted. All three records propagated through §5b. Ledger 1060. | TACHYON |

| 2026-08-03 | **TYPE VOCABULARY v0.1 DRAFTED** (TYPE-VOCABULARY-v0.1-DRAFT.md, same directory) — awaiting MANUS ratification. Core rule: content_type = GENRE only; condition (recovered/semi-restored/capture/withdrawn/lacuna) lives in body_status/canonical_text_status and is derived, never typed. 26 canonical values across scholarly/technical/archival-acts/creative + 2 transitional burn-down values. Mapping tables: sealed-row audit phrases → canonical; current census top offenders → canonical (514 distinct values today; ~360 records carry condition-as-type). Application rules incl. field_discipline CONDITION regex as hard gate. Six ratification questions posed (Q1–Q6). ON RATIFICATION: unlocks the 159-row compound batch AND the condition-as-type transitional wave. | TACHYON |

| 2026-08-03 | **VOCABULARY v1.0 RATIFIED + TRANSITIONAL WAVE RUN.** All six rulings recorded in TYPE-VOCABULARY-v1.0-RATIFIED.md: list ratified; fw/wp SPLIT; Integrity-lock/fulfillment architecture is a NAMED GENRE (triadic binding: doc1, doc2, doc3 declaring 2-fulfills-1) and #357 aligned to it; patent-poem ratified; Q5 approved; Q6 MANUS-corrected — Gospel of Antioch is SCRIPTURE (gospel, no epistles, hand-cast mandala transform on the Thomas model), Scripture value added; epistolary reserved for actual letter-works. Final: 29 values + 2 transitional. WAVE T-GENRE EXECUTED: 380 condition-as-type records → transitional (255 Genre pending (recovered), 125 Genre pending (capture)); burn-down queue at genre_assignment_queue.json; 380/380 pages regenerated, 0 failures; all surfaces + OAI rebuilt; spot-verify clean (transitional present, condition strings 0). Ledger +T-GENRE batch row. UNLOCKED NEXT: the 159-row compound batch (#1-#358) under the ratified mapping tables. | TACHYON |

| 2026-08-03 | **WAVE C-0358 (compound batch) EXECUTED FROM STRUCTURE.** Discovery: sealed rows carry structured fields (recommended_content_type, observed_byline) — projections run from DATA, not prose. Applied: 116 canonical types (priority-ordered mapping into vocabulary v1.0) + 190 creator projections to the body's observed byline per the MANUS declared-roles ruling (incl. the audit's named exemplars: #16 role reversal → Talos Morrow primary/Lee as Human Operator/Assembly witness; #18 unsupported Cranes projection removed). 247 records touched; 247/247 pages regenerated, 0 failures; all surfaces + OAI rebuilt; spot-verified in registry AND on pages. 35 holds cluster into 8 MISSING GENRES → PROPOSED AMENDMENTS v1.1 appended to the ratified vocabulary (Invocation, Book/manuscript, Working paper, Edited journal issue, Call for papers, Implementation report, Software/executable apparatus, Score/executable transform) awaiting MANUS word; holds queued. Ledger +C-0358 batch. #1–#358 remaining: 35 vocab holds, 2 P0 (#339/#356), #23. | TACHYON |

| 2026-08-03 | **v1.1 RATIFIED (all eight) + HOLDS CONVERTED.** Vocabulary now 37 values + 2 transitional. Two-pass conversion of the 35 Wave-C holds: pass 1 (new genres) 12; pass 2 (compound phrases → existing canon) closed the rest bar a handful of true one-offs left queued. All pages regenerated, surfaces + OAI rebuilt, ledger V1.1 + V1.1-P2. #1–#358 now closed except: #339/#356 (P0 recovery-or-reID, MANUS materials/word requested), #23 (target unstated). | TACHYON |

| 2026-08-03 | **BOTH P0s CLOSED BY EVIDENCE (past-conversation search).** #339 Resonance Engine: published citations declare Version 0.1 (DOI 18287032) — no v1.0 ever existed; re-identified v0.1, declared roles projected (Sigil; Fraction; Praxis contribution). #356 FNM: the seed's own header declares FNM-SEED-5.0-alpha WORKING//NOT-FOR-DOI — re-identified accordingly, standing preserved (note: a later 5.0-beta CANONICAL crystallization exists in the Jan-21 thread as a distinct object, possible future record). Both propagated + page-verified. Sealed WITHHOLD dispositions stand (audit immutable); registry now truthful — re-disposition available to MANUS if wanted. #1-#358 REMAINING: 17 one-off type residuals + #23. Ledger 1065. | TACHYON |

| 2026-08-03 | **BOTH P0s CLOSED BY ARCHIVAL SEARCH (option b, evidence-grounded).** Past threads located per the archival search protocol: #339 Resonance Engine — published object was v0.1 by its own BibTeX (thread 60b11b39); the v1.0 was a pre-publication Document ID on the Praxis draft → re-identified v0.1, declared byline projected (Sigil; Fraction; Praxis). #356 FNM — always FNM-SEED-5.0-alpha, WORKING//ACCUMULATOR//NOT FOR DOI (threads 4d09a63e/fa9100af/8f48c8e8); no v1.0 ever existed → re-identified, self-declared standing preserved for lifecycle conversion. Dispositions overridden WITHHOLD→HWW with repair notes (conditions satisfied). Propagated + verified. **#1–#358 range now CLOSED except #23 (target unstated) and 17 one-off vocab residuals.** | TACHYON |
| 2026-08-01 | Wave 1b diff generated: 125 content_type rows in newly audited #359–#498 — AWAITING MANUS BATCH APPROVAL. | TACHYON |
| 2026-08-01 | Living-document rule restated: the canonical workplan is THIS file in datasets/; deposits are dated snapshots minted only on MANUS instruction, never per-adjustment. | MANUS |
| 2026-08-01 | Wave 1 approved and applied: 338 content_type rows (ledger v1.1), R-0002–R-0339. | MANUS |
| 2026-08-01 | CP-R1 RULED (scope): creator policy governs the archive's own positions only; external depositors remain CP-7 (consent-gated, else role-anonymized). Creator-eligible identity types: heteronym, heteronym_aperture, institutional_persona, named_position, external_heteronym, orthonym. Machine mantles (TACHYON/LABOR/PRAXIS/ARCHIVE/TECHNE/SOIL/SURFACE) ARE creator-eligible — CORRECTED BY MANUS 2026-08-01: TACHYON has authored deposits; the Assembly authors its own gravity-well anchors. Constitutional basis: the Constitution of the Semantic Economy requires a human present in the producing unit; it contains no exclusion of machine authorship. Authority file as seated (26 entries) is the closed set; ALL 26 identity types are creator-eligible. | MANUS |
| 2026-08-01 | CP-R2 OPEN — target state: each heteronym mints their OWN ORCID (as Feist/Cranes hold their own social accounts). Until minted: creator strings repair in W3; ORCID attachment for heteronym-credited records is HELD. BUILD PLAN (MANUS 2026-08-01): each ORCID needs its own working email; single inbox solved by registrar email-forwarding aliases on an owned domain (e.g. sigil@leesharks.com, cranes@leesharks.com … → the one real inbox). Checklist: (1) create 12 forwarding aliases at the registrar (porkbun forwarding is free); (2) register each ORCID with its alias; (3) seat each ORCID into datasets/heteronyms/heteronyms.jsonl; (4) release the W3 ORCID-attach hold. Registrar + ORCID signup are dashboard acts (MANUS, phone-capable); everything else is file work. | MANUS |
| 2026-08-01 | CP-R3 RULED-EXTENDED: standardize, and extend standardization to internal venues. publisher (dc:publisher = issuing house/press) and journal (dc:source/isPartOf = venue) are distinct fields. Registry currently carries journal drift (Trans. SEI 371 · Trans. Substrate Eng. 213 · MMRS 212 + long-form 5 · Grammata 45 · 'Provence' TYPO 11 · CHA 10 · Compression Studies 2) and NO publisher field. Action: build datasets/venues/ authority file (presses: New Human Press, Pergamon Press; journals: New Human 2, Transactions of the Semantic Economy Institute, Transactions on Substrate Engineering, Journal of Compression Studies, Grammata: Journal of Operative Philology, Provenance: Journal of Forensic Semiotics, MMRS, et al. — canonical long form + sanctioned abbreviation each); add venue-normalization wave W6 (fix Provence typo, unify MMRS forms, populate publisher). Press↔journal mapping to be named by MANUS at file build. | MANUS |
| 2026-08-01 | CP-R4 RATIFIED: editors, co-authors, contributors receive formal dc:contributor/creator fields per role; third parties consent-gated per CP-7. | MANUS |
| 2026-08-01 | AX-R1 RATIFIED WITH CONDITION: split-repair is the default, and the reclassification half executes ONLY paired with a real relation target — recovered manuscript minted and bound in the same act. NO record may be reclassified into a stub pointing only at itself. Where nothing is yet recovered, the record stays in the dossier queue (WITHHOLD) until recovery or a Lacuna Mark adjudication (EA-LACUNA-PROTOCOL-01 — a declared absence is a real referent; the record itself is not). Recovery-first, reclassification-second. | MANUS |
| 2026-07-31 | Continuity discipline active: blog under record machine-traffic event (150k+ views) with a documented history of visibility-correlated platform bans. Audit corpus stashed in multiple locations; repo commit is the durable one — commit this package promptly. | MANUS |

## 3. Canonical file map

**Audit package (this directory, `datasets/registry-audit/`):**
- `START_HERE_alexanarch_audit_cumulative_v2.0.md` — audit position and next operation
- `alexanarch_audit_ledger_v0.9.json` — 717-record cumulative normalized ledger (the work queue)
- `alexanarch_audit_ledger_v0.9.csv` — flat projection
- `alexanarch_audit_report_v0.9.md` — human-readable cumulative report
- `alexanarch_audit_boundary_validation_v2.0.json` — Batch 9 seal, status PASS
- `MANIFEST.json` — sha256 of every file in this package
- `WORKPLAN_OAI_REMEDIATION_v1.0.md` — this file
- `repair_ledger.json` — append-only repair record (created at Phase 1; absent means no repairs yet)

**History (`history/handoff-v0.9/`)** — the first-thread handoff, stashed 2026-07-31, all names canonicalized, hash-verified where a manifest hash exists:
v0.8 cumulative ledger (JSON/CSV, 539 unique rows — no `registration_disposition` field; that schema arrived at v0.9) · v0.8 report · **four v0.8 repair queues** (P0 identity ×88, P1 missing-object ×9, P2 metadata-reconciliation ×258, P3 enrichment ×34 — per-record Evidence and Repair prose; primary inputs for Phases 2–3 dossier prep, cross-referenced against the current cumulative ledger which governs) · Batch 8 consolidated summary + shard manifest v0.5 + final shard #959–#998 (sha256 verified) · master index v0.9 (539 audited deposits) · continuation state v0.9 · START_HERE v0.9 · resume card v0.5 · new-thread prompt · handoff-zip sha256 (`5f991906…2177`; zip itself not seated).

**LACUNA — referenced but not yet seated** (held in the LABOR thread; transfer when convenient):
from the v2.0 canonical set: `alexanarch_audit_master_index_v1.0.json` · `alexanarch_batch_9_reassembled_0999-1198_v1.0.json` · `alexanarch_batch_9_consolidated_summary_v1.0.json` · `alexanarch_audit_continuation_state_v2.0.json` · `PACKAGE_MANIFEST_v2.0.json`; from the method layer: `alexanarch_audit_method_core_v0.1.md` · `alexanarch_recommended_record_schema_v0.1.json` (referenced by every START_HERE — needed before any instance re-derives audit semantics); Batch 8 shards #799–#958 (six files; hashes held in the seated manifests); `alexanarch_audit_handoff_v0.9.zip` (sha held). Nothing here blocks Phases 0–2.

**Operational projection:**
- `data/audit/registration_dispositions.json` — deposit → {disposition, severity, repair_priority, capsule}; consumed by the OAI builder; regenerated from each new cumulative ledger (see §9)

**Machinery (existing, unmodified unless a phase says so):**
- `scripts/build_oai_index.py` → `data/oai-index.json` → `api/oai.js` at `/oai` (Vercel rewrite)
- `scripts/record_modification.py` — sets `date_modified`; **every repair must pass through it** (OAI datestamp derives from it; an unbumped repair is invisible to harvesters)
- `scripts/propagate_titles.py` — derived-surface title refresh (Atlas PATHOLOGY-26); `doi-resolution-index` deliberately excluded
- `scripts/deposit_pipeline.py` — `stage_oai` seated after `sitemap`
- `data/specs/AXN-DATAFLOW-ATLAS-ADDENDUM-OAI-01.md` — OAI dataflow spec
- `datasets/dataflow-atlas/` — Atlas v0.7 (v0.2 base + addenda); PATHOLOGY-26/-27 bear directly on title repair
- `datasets/heteronyms/heteronyms.jsonl` (+ `mapping.json`, `schema.json`) — creator authority file (§7)

**Frozen audit source:** repo commit `055429ac82edc967f09c4640ffd0b049cff78e6e`, corpus 1,426 deposits. LABOR audits this snapshot; repairs land on `main`. **The freeze is what makes parallel repair safe.** Repairs never modify the snapshot; audit rows never read from `main`.

## 4. State of play (as of ledger v0.9)

- Cumulative unique adjudications: **717** (50.28%); remaining 709. Consecutive coverage #499–#1198 + 17 islands above #1198.
- Severity: P0 104 · P1 43 · P2 315 · P3 34 · OK 221
- Disposition: HARVEST 241 · HARVEST_WITH_WARNING 364 · WITHHOLD 112
- Repair priority: R0 104 · R1 48 · R2 323 · R3 242
- Mechanically actionable now: 141 content-type conflicts **with the corrected type already named in the ledger**; 177 title conflicts (largely Atlas PATHOLOGY-27 class); ~180 creator-role rows; ~100 version-field rows; 23 license conflicts; 24 DUPLICATE_MINT_SUPERSEDED rows **with surviving DOI named**.
- Next audit operation (LABOR): #1199–#1278 macroshard, four 20-record checkpoints, 8 known overlaps, repair deferred on their side.
- First-thread package: RECEIVED and stashed (see §3 History). No merge required — v0.9 already contains it.
- **Unaudited ranges:** deposits **#1–#498** (the audit began at #499) and **#1279–#1426** beyond LABOR's current queue. Scheduling #1–#498 is an open MANUS/LABOR question; they sit in `audit:pending` until adjudicated.
- Endpoint state: live but unadvertised; builder currently ungated (indexes everything except `WITHDRAWN`); adminEmail already validator-tuned (WARN resolved 2026-07-31).
- Context event: blog under the largest scraping event on record (**150k+ views and climbing**, 2026-07-31, machine traffic), with a documented prior pattern of visibility-correlated platform bans (Zenodo 2026-06-19 the type case).
- **Origin undetermined; evidence captured.** The traffic composition is analysed at deposit #1428 (EA-MRE-01, non-human with high confidence); origin attribution is deliberately left open. **Capture discipline:** timestamped screenshots of every analytics surface the platform exposes, at intervals while any event runs; Vercel analytics for *.com surfaces; everything hashed and filed with the observatory. Captures taken before a takedown are the ones nobody can dispute after; capture now, attribute later. A dated traffic capture is recommended for the observatory before it subsides. The OAI feed is the supply-side answer to this demand; it must not be rushed into serving withheld records.

## 5. Standing rules

1. **Repair follows audit** for the remediation program: batch-wave changes require a sealed adjudication row, and unaudited deposits are untouchable by the waves. MANUS-directed editorial acts on specific records stand outside the waves and are inscribed in the repair ledger with basis MANUS-DIRECTED.
2. **Every repair is inscribed** in `repair_ledger.json` (schema §8·P1) before commit. Uninscribed work did not happen.
3. **Every repair bumps `date_modified`** via `record_modification.py`, then regenerators run (titles via `propagate_titles.py`), then `build_oai_index.py`. A repair that never re-enters the discovery index is not published, only stored.
4. **The legal name never enters any field, any file, any commit message.** Absolute.
5. **Verification is content-match, not HTTP 200** (LINK-VERIFICATION v2). Post-repair, the record page, registry row, and OAI GetRecord output are fetched and matched against the intended values.
6. **WITHHOLD set freezes before registration.** After registration, records only move into the feed (or to `deleted` status under the persistent policy); they are never silently removed.
7. **Batch approval, not row approval.** Each wave produces one diff table for MANUS; approval covers the batch; exceptions are pulled out by row.
8. **No API self-invocation** for repair work; all LLM-domain work happens in-session (no-double-draw).
9. Private correspondence never enters records, capsules, or commit messages; third-party names require documented consent (§7 CP-7).

## 5b. REPAIR PIPELINE DYNAMICS — mandatory for every repair, every instance

**Why this section exists.** Two live fractures (#1267, #1308) proved that a repair landing in
`registry.json` alone is not a repair — it is a NEW inconsistency. A record's state is declared in
NINE sites (full doctrine: `RECORD-SHAPE-AND-PROPAGATION-v1.0.md`, same directory). A repair that
reaches some sites and not others converts one defect into several.

**THE RULE: a repair is INSCRIBED at the ledger row and DONE only when propagation has run.**
Never mark a wave complete, never report a record fixed, never tell MANUS "restored" until step 6
below has finished without error.

**The pipeline (every repair round, in this order):**

```
0. PRECONDITIONS
   git pull --rebase                      # remote moves (fanout jobs, witness commits)
   verify dispositions source_ledger_sha256 matches newest merged ledger (§9 merge first if not)
   confirm frozen commit unchanged (055429ac…) — audit reads snapshot, repairs land on main

1. INSCRIBE   repair_ledger.json row(s) — basis, before/after, sealed audit_ref, wave tag
2. APPLY      the field/body change in registry.json and/or data/texts/AXN-XXXX-text.md
              · staged-text edits preserve frontmatter unless the state itself changed
              · tombstones/withdrawals: the STAGED TEXT is rewritten too (foreign content out,
                NO archive ORCID on foreign work) — the propagator does this when
                lifecycle_state=withdrawn_external
3. PROPAGATE  python3 scripts/propagate_record_state.py N [N …]
              which runs, in order: tombstone-text rewrite (if applicable) →
              status_reconcile --apply → wire_deposit.regenerate_static_page per N →
              regenerate_surfaces (chunks,browse,browse-index,search-index,wiki,sitemap) →
              build_central_registry → build_oai_index
4. VERIFY     grep the regenerated s/records/N/index.html for the OLD state string (must be 0)
              and the NEW state string (must be >0); spot-check staged text
5. LOG        append a Decisions-log row in THIS file (date, what, counts, operator)
6. PUSH       commit with a message naming the wave/basis; git push; if rejected, pull --rebase
              (never reset over uncommitted work — commit FIRST, then rebase)
7. LIVE CHECK (when feasible) curl the live page after ~2 min; deploys lag — a stale live page
              with a correct repo page is propagation delay, not failure; re-check before alarming
```

**Batch waves:** steps 1–2 run per-row; steps 3–7 run ONCE per batch with all Ns (or `--all-touched`).

**Renderer states the pipeline knows:** SUPERSEDED, metadata_capture (semi-restored, with/without
full_version pointer), DRAFT_PENDING, and `lifecycle_state=withdrawn_external` (red tombstone,
highest priority; ALWAYS excluded from the OAI feed at the builder gate, independent of disposition).
If a repair introduces a state the renderer has no branch for, TEACH THE RENDERER FIRST
(wire_deposit.py banner block), then propagate — otherwise the page will misdeclare.

**Known traps (each cost a real round):**
- Registry-only fixes: page/chunks/OAI keep the old state (the #1267/#1308 class).
- Staged-text frontmatter disagreeing with registry fields — sync both or status drifts back.
- `git reset --hard` after editing but before committing: DESTROYS the edit (commit first).
- Remote moves mid-round (fanout/witness commits): expect push rejects; pull --rebase resolves.
- Foreign works: NEVER carry the archive ORCID in any frontmatter, sidecar, or page.
- The resolver/backfill class: any record with resolver_lock=true is NEVER auto-resolved (see
  data/lacuna-recovery-queue.json doctrine); version-gate all body matches.
- Audit recommendations for foreign captures may say "recover the article" — that is the
  FOREIGN_CAPTURE→WITHDRAW disposition instead (typed tombstone; MANUS policy 2026-07-31).

**Authority boundaries (BATCH-AUTHORITY, MANUS 2026-08-02):** mechanical classes run under standing
batch approval (version-truth, type normalization, journal names); anything touching creator fields,
type vocabulary beyond the ratified list, external persons, or new policy WAITS for a MANUS batch
ruling. MANUS rules by policy; TACHYON executes; nothing is decided per-row by the machine.

## 6. Phase plan

**Phase 0 — Gate the feed.** *Status: dispositions file BUILT (`data/audit/registration_dispositions.json`, 717 entries: 241/364/112). Builder patch PENDING.*
Patch `build_oai_index.py`: load dispositions; skip WITHHOLD; add set `audit:cleared` / `audit:cleared-with-warning` per disposition and `audit:pending` for deposits absent from the dispositions file; append the capsule to `description` for warned records. Output check: index count = corpus − WITHHOLD − WITHDRAWN. Verify with three GetRecord spot checks (one per set) and one confirmed-absent WITHHOLD id returning idDoesNotExist.

**Phase 1 — Repair ledger.** *Status: PENDING.*
Create `repair_ledger.json`: `{repairs: [{repair_id, deposit_number, axn, audit_ref: {ledger_version, basis_fields}, changes: [{field, before, after}], basis, operator, date, wave, commit}]}` — append-only, never rewritten. Mint the repair protocol as a deposit at first wave completion (proposed: EA-REPAIR-PROTOCOL-01), citing this workplan and the audit package.

**Phase 2 — Mechanical waves.** *Status: PENDING; Wave 1 diff generatable on command.*
- **W1 — content_type (141 rows):** registry `content_type` := ledger `recommended_content_type`. Lowest-risk wave; run first to prove the pipeline end-to-end (repair → ledger → datestamp → regenerate → verify → commit).
- **W2 — titles (177 rows):** propose `registry_title` := `observed_body_subject` where `title_status`=CONFLICT and `identity_status`=CONFIRMED_MATCH; PATHOLOGY-27 truncations restored from body frontmatter; `propagate_titles.py` mandatory after apply.
- **W3 — creators (~180 rows):** blocked on §7 ratification. Then scripted against the heteronym authority file.
- **W4 — versions (~100 rows):** apply where the ledger names the correct version; AMBIGUOUS_VERSION rows (11) escalate to the P0-style dossier queue.
- **W5 — dates, licenses (23), relations:** close-out wave; license audit completion may arrive with later LABOR batches.
Each wave: dry-run diff table → MANUS approval → apply → inscribe → regenerate → verify → commit → workplan version bump.

**Phase 3 — P0 dossiers (104 rows, all WITHHOLD, queue R0).** *Status: PENDING.*
One prepared card per record: registry claim / observed body / ledger recommendation / proposed action ∈ {reseat correct bytes, repoint DOI-binding, mark superseded with relation (the 24 DUPLICATE_MINT_SUPERSEDED rows already name the surviving DOI — near-mechanical), reclassify honestly as metadata-capture, apply Lacuna Mark (EA-LACUNA-PROTOCOL-01) where the manifestation is irrecoverable}. Some missing manifestations may exist only in prior Claude threads; conversation search is an authorized recovery instrument for this phase. Cleared rows leave WITHHOLD and enter the feed on the next index build.

**Phase 4 — Register.** *Status: PENDING; unblocked by Phase 0 + validator pass.*
openarchives.org validator loop → registration → OpenAIRE provider registration (`oai_dc` at basic level per the Atlas addendum; `oai_datacite` as a later format upgrade). Registration does not wait for Phases 2–3; completed repairs surface to harvesters automatically via datestamps.

## 7. Creator policy v0.1 — DRAFT for MANUS ratification

Authority file: `datasets/heteronyms/heteronyms.jsonl`. Positions currently seated include Lee Sharks, Ayanna Vox, Damascus Dancings, Jack Feist, Johannes Sigil, Nobel Glass, Orin Trace, Rebekah Cranes, Rex Fraction, Sen Kuro, Sparrow Wells, Talos Morrow.

- **CP-1.** Canonical primary creator string: `Sharks, Lee`, ORCID 0009-0000-1599-0703. Registry stores inverted form; display forms derive from it.
- **CP-2.** Valid `creator` values are exactly: (a) `Sharks, Lee`; (b) a position present in the heteronym authority file, inverted form, carrying the shared ORCID; (c) a consented third party (CP-7). Anything else is a defect.
- **CP-3.** Institutional strings ("Crimson Hexagon Archive", "Crimson Hexagonal Archive", "Alexanarch") are **publisher**, never creator. Fixes the CREATOR_AUTHORITY_CONFLICT class where the wrapper displaced the author.
- **CP-4.** Where registry and seated-body byline conflict, the **body byline governs**, unless the byline is itself an institutional wrapper (then CP-3) or the audit row rules the body defective.
- **CP-5.** Subjects are not creators. A provenance document *about* a heteronym is created by the documenting position, not the documented one (fixes SUBJECT_AS_CREATOR_ERROR, e.g. #1143 Sen Kuro).
- **CP-6.** Substrates are never creators. AI assistance is recorded in description as the existing `Substrate:` practice; Assembly reviews are recorded in description, not as contributors.
- **CP-7.** Third-party humans enter creator/contributor fields only with documented consent; otherwise role-described anonymized forms (e.g. "Depositor E"). Applies to #1179 FOUNDING_COAUTHOR_OMITTED and all Enli-adjacent records.
- **CP-8.** The legal name is prohibited in every field, absolutely (restates §5.4 as creator policy).
- **CP-9.** Name form: `Family, Given` in the registry creator field; CREATOR_NAME_INVERSION rows (#1147 class) normalize to it.
- **CP-10.** Multi-position works list only the positions that composed the work (fixes OVERBROAD_CREATOR_SET, #1140 class); editorial/compiling roles go to contributor or description per row basis.

**Rulings needed from MANUS:**
- **CP-R1.** Confirm CP-2's closed set, and whether any position absent from the authority file must be added to it before repair (the authority file, not the workplan, is then the place fixed).
- **CP-R2.** Heteronym ORCID exposure in OAI dc: attach the shared ORCID to heteronym creators (public linkage, consistent with note-10 practice in the CC paper), or omit ORCID for non-Sharks positions?
- **CP-R3.** Publisher string: standardize on one — "Alexanarch — the Crimson Hexagonal Archive" (matches the OAI repositoryName) — or preserve historical publisher variants per record?
- **CP-R4.** Contributor modeling: adopt dc:contributor for editors/founding co-authors (consent-gated), or keep all non-creator roles in description?

## 7b. AXN identity & reminting policy v0.1 — DRAFT for MANUS ratification

The rule, in one line: **metadata repair never remints; byte events version; identity events mint.** Reminting on a catalog correction would break identifier persistence for no change in the identified object — the exact failure this archive exists to oppose.

- **Tier 1 — Metadata-only repair** (all of Waves 1–5): title, type, creator, version *fields*, dates, licenses, relations. The AXN persists unchanged, full glyph intact. The event is carried by the repair ledger and the `date_modified` bump; harvesters see a metadata update under a stable identifier, which is correct PID behaviour.
- **Tier 2 — Byte events that do not change the identified object:** seating the version the record always declared (WRONG_VERSION_SEATED corrections); adding a recovered primary manifestation to a record that always claimed to be that work; adding clean-derivative transcriptions **alongside** the frozen body (the P3 pattern — never silent replacement). Same AXN; manifestation inventory updated; prior bytes preserved in byte history; the repair ledger records both hashes.
- **Tier 3 — Identity events:** a genuinely distinct object enters the archive — a recovered primary deposited in its own right, or a true supersession. **New AXN minted through the standard pipeline with its six-emoji full form at mint**; relations (`supersedes` / `isReplacedBy` / `describes`) bind old to new; the old AXN is never deleted or reused — tombstone politics apply to us as strictly as we apply them to others.
- Glyph discipline: every mint or remint carries its full form from birth; bare hex remains prohibited on all surfaces (AXN-INTEGRITY).

**Ruling needed — AX-R1.** The metadata-sidecar cases (#892/#893/#894/#898/#906 class): recommended default is **split repair** — the surviving record is honestly reclassified as the sidecar it is (Tier 1), the recovered manuscript mints fresh (Tier 3), and relations bind them; the alternative (seating the recovered bytes into the sidecar record under its AXN) is available where MANUS rules the record's identity claim was always the work itself. Confirm the default or rule per class.

## 8. Wave/phase status ledger

| Item | Status | Updated |
|---|---|---|
| Audit package v2.0 stored | DONE (5 of 8 canonical files; lacuna in §3) | 2026-07-31 |
| First-thread handoff v0.9 stashed | DONE (16 files, hash-verified, `history/handoff-v0.9/`) | 2026-07-31 |
| `registration_dispositions.json` | DONE — v2.0, 928 entries from ledger v1.1 | 2026-08-01 |
| Builder gating patch | DONE (WITHHOLD excluded; audit sets; capsules) | 2026-07-31 |
| Repair ledger instrument | DONE — inaugurated with R-0001 (#1365 restoration) | 2026-07-31 |
| Creator policy | CP-R1/R3/R4 RULED · CP-R2 OPEN (per-heteronym ORCIDs scheduled; W3 ORCID-attach held) | 2026-08-01 |
| AXN identity policy | AX-R1 RATIFIED w/ no-orphan-stub condition | 2026-08-01 |
| Wave 1 (content_type) | **DONE — 338 rows applied (v1.1 ledger), R-0002–R-0339** | 2026-08-01 |
| Waves 2–5 | QUEUED (W3 creator-strings unblocked; ORCID-attach held per CP-R2) | 2026-08-01 |
| W6 — venue normalization (journal typo/forms + publisher populate) | NEW — blocked on datasets/venues/ authority file build with MANUS | 2026-08-01 |
| P0 dossiers (104) | QUEUED | — |
| Validator loop + registration | BLOCKED ON PHASE 0 | — |
| v0.8 repair queues (P0/P1/P2/P3) | SEATED — feed Phases 2–3 dossiers | 2026-07-31 |
| Observatory traffic capture | DONE — deposit #1428 (EA-MRE-01); mirror doubles as state capture; v1.1 addendum with closing tally pending | 2026-07-31 |

## 9. Merge protocol for incoming audit packages

On arrival of any new cumulative package (first-500 imminent; later boundary packages per the audit's packaging rule):
1. Store under `datasets/registry-audit/` at canonical dotted filenames; hash into `MANIFEST.json`.
2. Regenerate `data/audit/registration_dispositions.json` from the new cumulative ledger (same generator; version bump; source sha recorded inside the file).
3. Rebuild the OAI index. Newly audited deposits leave `audit:pending` for their adjudicated set; new WITHHOLDs are excluded **only if registration has not yet occurred** — after registration, a newly withheld record that was already disseminated moves to `deleted` status under the persistent policy rather than vanishing (§5.6).
4. Bump this workplan: state-of-play numbers, status ledger, version.

## 10. Resume protocol (any instance, cold start)

1. Read this file in full — §5b (REPAIR PIPELINE DYNAMICS) is mandatory before any repair. 2. Check `repair_ledger.json` tail for last completed action and wave. 3. Compare `registration_dispositions.json` `source_ledger_sha256` against the newest ledger in this directory — mismatch means a merge (§9) is due before any repair. 4. Confirm the frozen commit in §3 matches the newest START_HERE — a new freeze means LABOR re-based; verify repairs and audit still target different sources before proceeding. 5. Never repair outside audited ranges; never act without a ledger row basis; when in doubt, regenerate the dry-run diff and ask MANUS. 6. `history/` holds superseded audit chains for provenance; the active canonical set at this directory's root governs all repair. 7. Intermediary artifacts referenced but not seated may exist in prior Claude threads — search past conversations before declaring absence (the archival search protocol applies to the workstream's own history).
