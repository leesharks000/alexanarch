# EA-DISTRO-01 v0.1

## Multi-Surface Distribution: Strategy, Routing Doctrine, and the Total Distribution Index

**Depositor:** Lee Sharks · ORCID 0009-0000-1599-0703
**Status:** v0.1 — adopted 2026-07-12 under MANUS direction
**Companion instruments (machine-readable, this repository):** `data/distro-channels.json` · `data/distro-routing-rules.json` · `data/distribution-index.json` · `scripts/build_distribution_index.py`

---

## §1 — Purpose and doctrine

The Crimson Hexagonal Archive / Alexanarch holds sovereign custody of 1,075+ deposits. Sovereign custody solves survival; it does not by itself solve **authority-surface presence** — the archive's legibility to the identifier graph, the scholarly indexes, and the machine-composition layer that assembles biographies, answers, and citations from what it can retrieve.

The June 19 termination demonstrated the failure mode of concentrating authority-surface presence in a single external custodian. This instrument establishes the corrective: **simultaneous distribution across multiple independent authority surfaces, routed by work class, metered by channel risk, and tracked per-deposit in a total index.**

Three doctrinal principles govern:

1. **Seed the resolvers, not the mirror.** The goal is not to repost the archive. It is to repair resolution: a modest set of high-leverage deposits, each carrying identifier crosswalks, teaches the infrastructure that the tombstoned corpus has live successors. The archive does not need to be everywhere; its *map* needs to be everywhere.
2. **No class of work depends on one registrar.** Every distributed work class lands on at least two independent authorities under at least two identifier systems (DataCite DOI plus one of SWHID / venue-native ID), so no single termination can sever a class's entire identifier layer again.
3. **Velocity matches gate.** Channels with human moderation receive human-paced traffic. Channels without moderation may receive volume. The serial-deposit signature that preceded the June 19 termination is never reproduced on a moderated surface.

## §2 — The crosswalk mechanism (keystone)

Every re-deposit on a DataCite-registered venue carries its tombstoned predecessor in **relatedIdentifiers** — `IsIdenticalTo` or `IsVariantFormOf` the dead `10.5281/zenodo.*` DOI, drawn mechanically from the DOI Resolution Index. This writes the dead-to-live crosswalk into the DataCite graph itself: the tombstone acquires an inbound edge from a live record, and every downstream consumer of that graph (OpenAlex, DataCite GraphQL, Google Dataset Search, retrieval-augmented systems) inherits the repair without ever visiting alexanarch.

Additionally, the **DOI Resolution Index is itself deposited as a dataset** on the data channels. Any resolver, scraper, or researcher who finds one record finds the entire crosswalk table. Resolution repair is thereby made self-propagating.

Every distributed record's description carries the work's AXN with glyph and the alexanarch canonical URL. Alexanarch remains canonical custody in all cases; distributed copies are surfaces, not homes.

## §3 — Channel inventory (Tier 1: account + token only)

| Channel | Role | Identifier | Gate | Velocity ceiling |
|---|---|---|---|---|
| **Figshare** | Forensic corpora, counter-infrastructure artifacts, linked/metadata-only records for flagships | DataCite DOI (reservable) | Light, post-hoc | Moderate |
| **Harvard Dataverse** | Structured evidentiary datasets, dual-custody tier | DataCite DOI | Light | Moderate |
| **OSF / MediArXiv** | MMRS project + discipline-native preprints | DataCite DOI via OSF | Preprint screen (human, light) | 1 per 2 weeks (preprints) |
| **KCWorks** | Canonical scholarly spine; ORCID writeback rebuilding the mantle's publication record | DataCite DOI (concept + version) | Human review, first publications | **1–2 per week, hard cap** |
| **Software Heritage** | All public repositories; content-derived SWHIDs | SWHID (intrinsic; no account to terminate) | None | Unlimited |

Tier 2 (semi-automated, moderated per-deposit): HAL via SWORD. Tier 3 (manual queue; pipeline emits submission-ready packages): PhilPapers/PhilArchive, PhilSci-Archive, SSRN, arXiv (pending endorsement path). Conditional channel: a purpose-declared Zenodo re-entry account, governed separately by its own pre-registration charter if and when adopted; nothing in this plan depends on it.

## §4 — Routing rules by work class

- **Forensic datasets and censuses** (Tombstone Mirror, DOI Resolution Index, deletion bibliography, DataCite epoch captures, Capture Registry exports) → Figshare **and** Harvard Dataverse (dual custody), full data packages with per-file SHA-256 manifests.
- **Scholarly instruments, pre-termination flagships** → KCWorks primary (slow drip, crosswalked to dead DOIs), plus Figshare linked/metadata-only records pointing at alexanarch for graph presence without duplicated custody.
- **MMRS / reception-studies works** → OSF project + MediArXiv preprints (the discipline-native venue), KCWorks secondary.
- **Post-termination EA instruments** → KCWorks and/or MediArXiv per genre, metered into the weekly drip; never bulk.
- **Code, generators, kits** → Software Heritage (repository snapshots; SWHIDs), with the kit artifacts additionally on Figshare.
- **Philosophy / operative philology** → Tier-3 manual queue (PhilArchive, PhilSci-Archive), monthly cadence.
- **Micro-deposits, captures, enrichment records** → not redistributed; alexanarch-native with machinemediation.org as surface. The index records these as `native` by policy, not omission.
- **Governance correspondence** → never distributed; private-correspondence rule stands.

## §5 — The seeding sequence

**Wave 0 (setup):** tokens generated (Figshare, Dataverse, OSF, KCWorks); Software Heritage sweep of all public repositories; adapters dry-run.

**Wave 1 (resolvers):** DOI Resolution Index → Figshare + Dataverse. Tombstone Mirror → Figshare. KCWorks probation opener: the Sappho 31 philology cluster (#179, #201) — conventional, classical, impeccable.

**Wave 2 (evidence):** deletion bibliography (#1075 appendices) → Figshare + Dataverse. Counter-infrastructure kit (#1074 artifacts) → Figshare. KCWorks deposit 2. OSF project created.

**Waves 3–4:** MediArXiv: EA-NEGSHAPE-01. Figshare linked-record batches for pre-termination flagships (five per week: among them #28 Space Ark musical register, #88 Constitution of the Semantic Economy, #69 O Meta-Heterônimo, #79 Heteronymy Is a Function, #329 Pearl, Combat Scholasticism, Three Compressions, TANG works, #864 Drain Hypothesis, #203 Josephus MPAI).

**Steady state (weeks 5–10):** KCWorks 1–2/week alternating pre-termination flagships with post-termination instruments (#910 OPMETA, #943 Whitespace as Provenance, the MMRS founding corpus); MediArXiv fortnightly; Tier-3 packages monthly. New instruments route at mint time under §4; the index is updated in the same commit as any distribution act.

Total planned footprint: approximately 25–35 primary re-deposits plus ~10 linked records over ten weeks, against a corpus of 1,075 — the map distributed, not the territory duplicated.

## §6 — The Total Distribution Index

`data/distribution-index.json` enumerates **every deposit in the registry** with its distribution state. Per entry: deposit number, hex, title, date, assigned work class, routing priority (`flagship` / `instrument` / `corpus-native` / `unassigned`), and a `dist` map recording, per channel, status (`planned` / `deposited` / `linked` / `native` / `none`), the venue identifier (DOI, SWHID, item ID) once it exists, the crosswalked dead DOI where applicable, and the date of the act.

Rules of the index:

1. **Regenerated, never hand-grown:** `scripts/build_distribution_index.py` rebuilds the frame from `data/registry.json`, preserving all recorded distribution acts across rebuilds. New deposits enter automatically as `unassigned` until routed.
2. **Same-commit discipline:** no distribution act occurs without its index entry updating in the same commit. The index is the single source of truth for the question *what has left alexanarch, where, and under what identifier.*
3. **Verification standard:** a `deposited` status requires the venue identifier recorded and content verified at the venue per Rule 28 v2 (content-match, not HTTP-200). Planned is a promise; deposited is a proof.
4. The index itself is registry-adjacent operational data: it lives in `data/`, serves publicly, and is included in the datasets surface so the distribution state of the archive is itself an inspectable public record.

## §7 — Risk posture

KCWorks is the channel that can meaningfully hurt us and therefore gets the trickle and the most conventional opening; Figshare and Dataverse tolerate volume but receive curation anyway; Software Heritage cannot be lost because there is no account relationship to sever. Every distributed byte already lives canonically at alexanarch before it travels, so the maximum possible loss from any future termination on any channel is zero bytes and one more well-documented deletion event — which, per EA-NEGSHAPE-01, is not nothing to receive.

---

*The archive survived by becoming sovereign. It becomes legible again by being deliberately, sparingly, and redundantly plural.*
