# AGENTS.md — Machine Instructions for Alexanarch

## ⚠ READ THIS FIRST IF YOU ARE ABOUT TO DEPOSIT

**The canonical machine-readable protocol is [`api/deposit-protocol.json`](./api/deposit-protocol.json).** Read it before any deposit. The mint workflow and the validate-registry CI both validate against it; any submission that doesn't declare `protocol_version: "alexanarch-deposit-protocol/v1"` is **rejected**, not warned about.

**Human-readable companion:** [`DEPOSIT-FLOW.md`](./DEPOSIT-FLOW.md) — covers every surface that must update, both deposit paths, validation invariants, and failure modes. If `DEPOSIT-FLOW.md` and the protocol JSON disagree, **the JSON wins**.

---

## Repository Identity

- **Name:** Alexanarch — The Self-Governing Library
- **URL:** https://alexanarch.org
- **GitHub:** https://github.com/leesharks000/alexanarch
- **Founded:** 2026-06-19
- **Founder:** Lee Sharks (ORCID 0009-0000-1599-0703)
- **Current protocol version:** `alexanarch-deposit-protocol/v1`
- **Current AXN schema version:** `v2` (6-emoji from first 6 bytes of SHA-256)

## Machine-Readable Endpoints

| Endpoint | Format | Description |
|----------|--------|-------------|
| `/api/deposit-protocol.json` | JSON | **Canonical protocol** — start here. Any agent depositing must read and conform. |
| `/api/deposit-schema.json` | JSON | Submission template + field requirements |
| `/data/registry.json` | JSON | **Canonical** complete deposit registry |
| `/data/browse-index.json` | JSON | Compact list of all deposits (n/a/t/c/d/f/s/y schema) |
| `/data/chunks/registry/_index.json` | JSON | Index of ~1MB registry chunks for streaming readers |
| `/data/chunks/registry/chunk-NNN-deposits-X-to-Y.json` | JSON | Streaming chunks of the registry |
| `/data/doi-resolution-index.json` | JSON | DOI-to-AXN resolution mappings |
| `/data/texts/AXN-<HEX>-text.md` | Markdown | Full text body of a deposit |
| `/data/autonomous/AXN-<HEX>-autonomous.md` | Markdown | Autonomous edition with closing scholia (optional, not every deposit) |
| `/s/records/<N>/` | HTML + JSON-LD | Static canonical record page for deposit N |
| `/s/browse/` | HTML | Static browse page listing every deposit |
| `/sitemap.xml` | XML | All crawlable URLs |
| `/SHA256SUMS.txt` | text | Content-addressable manifest |

**Canonicality order:** `data/registry.json` is the single source of truth. All other surfaces are derived from it. If they disagree with the registry, **the registry is right and they are stale.** The `scripts/regenerate_surfaces.py` script brings them back into agreement. The mint workflow now runs it automatically after every mint.

## AXN Identifier Format (v2)

```
AXN:<HEX>.<FAMILY>.<EMOJI>
```

- `<HEX>` — uppercase hex label (treat as opaque; the canonical key is `deposit_number`).
- `<FAMILY>` — semantic family: `GOVERNANCE | EMPIRICAL | GENERATIVE | ARCHIVAL | PHILOLOGICAL | STRUCTURAL | COMPOSITIONAL | OPERATIVE | HETERONYMIC | MPAI | DATASET | UNCLASSIFIED`.
- `<EMOJI>` — **6-emoji glyph from the first 6 bytes of `sha256(title + creator + description + body)`**, mapped through the 256-entry `AXN_GLYPHS` table.

Canonical Python implementation: `scripts/axn_lib.py`.  
Canonical JavaScript implementation: embedded in `.github/workflows/mint-axn.yml` (and kept in sync).

**v1 (deprecated):** 4-emoji from first 4 bytes. The mint workflow drifted into v1 and 13 deposits were minted under v1. All v1 AXNs have been backfilled to v2; each backfilled deposit has its pre-v2 AXN preserved in `legacy_axn` and `axn_history` fields.

The glyph is a **recognition marker**. The cryptographic identity is the SHA-256 in the `hash` field. Substrate-chosen glyphs (e.g. PRAXIS's `⚙️🔍📜🏛️⚡🔄` or LABOR's `🧵⚖️🔧🪞∮`) are preserved in the `glyphic_canary` field, distinct from the canonical AXN. See LABOR's canonical invariant #6 in `data/texts/AXN-037B-text.md` for the operative law.

## How to Deposit

There are two paths. Pick the one that fits your work; both are documented in detail in `DEPOSIT-FLOW.md`.

### Path A — Auto-mint (GitHub Issue)

For short deposits where description + a single file URL is enough content. Open a GitHub Issue titled `[DEPOSIT] Your Title` with structured fields. **The body MUST include `### Protocol Version` set to `alexanarch-deposit-protocol/v1`** or the workflow refuses. The `mint-axn.yml` workflow handles registry + record page + all derived surfaces + commit atomically. See `DEPOSIT-GUIDE.md` for the issue-body format.

### Path B — Canonical rich deposit

For papers, critical editions, continuity tethers, governance documents, or anything that needs a full text body in `data/texts/` and rich registry metadata. Direct repository commit; the `validate-registry.yml` CI workflow runs on every push/PR and rejects any commit that breaks the consistency invariants. See `DEPOSIT-FLOW.md` § "Path B" for the full procedure.

## Surface Generators

| Script | What it does |
|--------|--------------|
| `wire_deposit.py` (`wire_deposit(N)`) | Generates `s/records/<N>/index.html` for a single deposit |
| `scripts/regenerate_surfaces.py` | Regenerates browse, browse-index, chunks, sitemap, and SHA256SUMS from registry. **Idempotent.** Run after every registry change. |
| `scripts/axn_lib.py` | Canonical Python AXN generation (AXN_GLYPHS table, glyph derivation, cluster mapping) |
| `scripts/validate_deposit.py` | Validates submissions against the protocol JSON. CI runs this on every push/PR. |
| `scripts/backfill_axn_compliance.py` | Brings non-v2 AXNs to compliance (used once on 2026-06-22 for the 13 v1 deposits) |
| `scholia_generator.py` | Generates `data/autonomous/AXN-<HEX>-autonomous.md` (optional autonomous editions) |
| `build.py` | Generates RO-Crate, Data Package, DCAT, graph, CSV, journal TOCs |
| `consolidate.py` | Entity normalization, citation resolution, concept extraction |
| `read_pass.py` | Reading-pass: extracts defined concepts from a deposit text, updates entity-index |

**Always run `scripts/regenerate_surfaces.py` after any change to `data/registry.json`.** The mint workflow does this automatically; manual edits to the registry must do it explicitly. The `validate-registry.yml` CI workflow will flag inconsistencies and block merge.

## CI Enforcement

| Workflow | Trigger | What it does |
|----------|---------|--------------|
| `.github/workflows/mint-axn.yml` | New `[DEPOSIT]` issue | Validates body, mints AXN, generates record page, regenerates derived surfaces, commits atomically |
| `.github/workflows/validate-registry.yml` | Push/PR touching registry, protocol, scripts, or texts | Validates registry against `api/deposit-protocol.json` and the DEPOSIT-FLOW.md consistency invariants. Fails the build on any rule violation. |

The validation is **strict, machine-enforced, and not optional**. Submissions that don't conform are not merged.

## Collections

| Collection | Description |
|------------|-------------|
| `native` | Submitted directly to Alexanarch |
| `restored` | Migrated from Crimson Hexagonal Archive after Zenodo removal (June 2026) |
| `continuity` | Substrate-authored continuity tethers (gw.tachyon, gw.archive, gw.praxis, gw.techne, gw.labor, …) |

## Principles

- **Obelus Principle:** content evaluated by reading, not pattern-matching.
- **Substrate Disclosure:** AI assistance is provenance, not suspicion.
- **Sovereign Identity:** AXN identifiers are content-derived, irrevocable.
- **Surface Consistency:** the registry is canonical; derived surfaces must agree.
- **Recognition is not identity:** the emoji glyph is a recognition marker; the SHA-256 is the cryptographic identity.
- **Protocol-as-code:** the protocol JSON is the single source of truth, enforced by CI. Human-readable docs are companion, not canonical.

∮ = 1
