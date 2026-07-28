# Dataflow Atlas — v0.6 Addendum

**Date:** 2026-07-28
**Scope:** registers the EA-AVAILABILITY-INTEGRITY-01 flows (audit deposit #1413) against the pathology register, and records the new source-of-truth flows the sprint created. Extends v0.5; supersedes nothing.

---

## PATHOLOGY-28 — status update: alexanarch instrument built

**Prior status (v0.5):** instrument built for machinemediation; the flow is unchanged on the rest of the fleet.
**Status now:** instrument built for alexanarch — `scripts/coherence_sync.py`, wired into `deposit_pipeline.py stage_commit`.

Every commit now regenerates, from `data/registry.json` as the single read source: the deposit count and per-registry timestamps in `api/index.json`; the deposit count and DOI-mapping counts in `llms.txt`; and a `surface_hashes` block (sha256 of registry, search-index, body-index, axn-index, doi-resolution-index, with `hashed_at`). The governing index's "where surfaces disagree, this wins" contract is now verifiable by hash rather than asserted by prose. The pathology's rule — *a count written once is a claim that was true once* — is structurally closed for these surfaces: no count on them is typed; every count reads.

Evidence of the prior defect, recorded per the register's discipline: on 2026-07-28 the registry's own `last_updated` read `2026-07-14` while containing deposits dated `2026-07-28`; `api/index.json` carried `registries.deposits.last_updated: 2026-06-22` beside a correct count; `llms.txt` said 1410 against a registry of 1412 and `1,938 severed DOIs` against a file of 1,939 mappings. All four are now generated values.

**Residual:** the fleet beyond alexanarch and machinemediation remains uninstrumented for this class.

## PATHOLOGY-29 — status update: the archive's flagship instance closed

**The instance (v0.5's class, alexanarch's case):** record pages served well-formed `ScholarlyArticle` JSON-LD with an `articleBody` for records whose visible prose declared *SEMI-RESTORED — metadata capture only*. The structured data did not diverge from the prose by accident of drift; it diverged by omission — no field existed in which the page could tell a machine what the prose told a human. 224 records additionally carried `body_status.class: full` in the registry itself, certifying captured descriptions as recovered works (audit #1413, finding H2).

**Remediation, all live 2026-07-28:** a two-axis availability model — `body_status` (presence) and `canonical_text_status` (canonical-text state: canonical_full_text / recovered_full_text / metadata_only / attachment_only / tombstone / withdrawn) — assigned across all 1,413 deposits by instrument (`scripts/reaudit_canonical_text.py`), instrument-checked (T2b banner classifier, 10% sample, inversion sweep), and MANUS-ruled where uncertain. The value is machine-declared where machines read: `creativeWorkStatus` + `conditionsOfAccess` in every record page's JSON-LD; a `canonical_text_status_index` table in `api/search-index.json`; badges on browse cards; a warning in `llms.txt` that a well-formed `articleBody` does not imply the canonical work is held. Structured data and prose now assert the same thing because both read the same field.

**Residual:** `canonical_text_status` is asserted for the metadata-only class by absence-of-recovery, which is a live claim; the restoration queue (110 records with known blog sources at this writing) will move records out of the class, and the field must move with them — it is written by instruments, never by hand, precisely so it can.

## New flows registered

1. **`canonical_text_status`** — registry field → search-index table → record JSON-LD → browse badges → llms.txt. Writers: `reaudit_canonical_text.py` (instrument), MANUS rulings (recorded per-record in `body_status.ruled_by`), restoration passes. Readers: `wire_deposit.py`, `regenerate_surfaces.py`, any external agent.
2. **`surface_hashes`** — `coherence_sync.py` → `api/index.json`. The verification handle for surface coherence.
3. **DOI ownership gate** — `scripts/doi_ownership_gate.py` guards `data/doi-resolution-index.json` against externally-owned DOIs entering as archive dead-DOIs (precedence: ORCID → registry-creator match → FLAG for MANUS; never auto-removes). Standing sweep target: mappings with `datacite_state: findable`. Precedent ruling: T18, deposits #1382/#1383.
4. **`data/fleet-domains.json` → `/fleet/`** — the 23 network sites, relocated from `sitemap.xml` (cross-host locs are discarded by crawlers) to a crawlable HTML cross-listing. The sitemap now carries canonical-host record and first-party URLs only.
5. **`data/EA-AVAILABILITY-INTEGRITY-01-status.json`** — the sprint's canonical task tracker; task completion is recorded there with commit hashes (deposited plans record initial state only).
6. **Reaudit diff artifacts** — `data/reaudit-T2-diff-2026-07-28.json`, `data/reaudit-T2b-resolution-2026-07-28.json`: the evidence chain for every typing change.

## Two desyncs the pass surfaced (evidence the guards work)

The fleet-wide page regeneration was twice interrupted by its own guards, correctly: deposit #3 declared a `full_text_path` (a versioned filename) absent from disk — repaired to the canonical unversioned file; deposit #344 declared the book PDF itself as its text body — the binary briefly text-mangled during repair, caught, git-restored byte-identical, repointed to its true text body, typed `attachment_only`, and `wire_deposit.py` hardened so binary attachments are never inlined or decoded. Both belong to the register as instances: a declared path is a count of one — it, too, is a claim that was true once, unless something checks it.

## The rule (restated from v0.5, now with two instruments)

The dataset is the source of truth for live values; the confirmation chain is the source of truth for historical ones; and a surface may assert only what it reads. v0.5 built the machinemediation instrument. v0.6 records the alexanarch instruments. The fleet remainder is the open front.
