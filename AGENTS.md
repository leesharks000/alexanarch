# AGENTS.md — Machine Instructions for Alexanarch

## ⚠ STOP. READ THIS FIRST.

You are about to operate on Alexanarch infrastructure. Before any action:

1. Fetch **[`/api/index.json`](./api/index.json)** — the central protocol registry.
2. Run **`python3 scripts/bootstrap_familiarization.py --strict --instance "<your label>"`** to verify content-hashes of every protocol and schema and produce a familiarization receipt.
3. Attach the receipt to any commit, deposit, or PR you create. Workflows mechanically enforce this — missing receipt is rejected.
4. If you're about to **modify a protocol JSON or a schema**: do NOT hand-edit. Use **`python3 scripts/protocol_update.py --protocol <name> --description '...'`**. This is the only supported path. The tool bumps version, recomputes hashes, updates the central index, and appends change_logs atomically.

**Why this exists:** new instances arriving without familiarization, hand-editing protocols, and propagating drift was the single largest source of regressions in this infrastructure. The central index + bootstrap + update tool is the structural fix. Behavioral exhortation does not work; mechanical verification does.

---

## Repository Identity

- **Name:** Alexanarch — The Self-Governing Library
- **URL:** https://alexanarch.org
- **GitHub:** https://github.com/leesharks000/alexanarch
- **Founded:** 2026-06-19
- **Founder:** Lee Sharks (ORCID 0009-0000-1599-0703)
- **Central index:** [`/api/index.json`](./api/index.json) (canonical — every other document defers to it)

## What's where

Pull from the index — these are just the entry points. The index has the complete catalog with current versions and hashes.

| Surface | Canonical path | What it is |
|---------|----------------|------------|
| **Central protocol catalog** | `/api/index.json` | List of all protocols, schemas, registries with current versions + content_sha256 |
| **Deposit protocol** | `/api/deposit-protocol.json` | What a deposit is, how it's submitted, validated, enriched |
| **AXN protocol** | `/api/axn-protocol.json` | AXN format, generation algorithm, glyph table, legacy resolution |
| **Submission template schema** | `/api/deposit-schema.json` | Issue body template + field requirements for Path A deposits |
| **Deposit entry JSON Schema** | `/api/schemas/deposit-entry.schema.json` | Strict schema for entries in `data/registry.json` |
| **Deposit registry (the AXN registry)** | `/data/registry.json` | Canonical list of every deposit |
| **Browse page (derived)** | `/s/browse/index.html` | Static all-deposits view |
| **Browse-index (derived)** | `/data/browse-index.json` | Compact list of deposits |
| **Chunked registry (derived)** | `/data/chunks/registry/` | ~1MB streaming chunks |
| **Sitemap (derived)** | `/sitemap.xml` | All crawlable URLs |
| **Checksums (derived)** | `/SHA256SUMS.txt` | Content-addressable manifest |
| **Record pages (derived)** | `/s/records/<N>/index.html` | Per-deposit canonical page |

The "derived" surfaces all flow from `/data/registry.json`. The script that brings them back into agreement is `scripts/regenerate_surfaces.py`. The mint workflow runs this automatically; manual registry edits must do it explicitly.

## How to do anything

| Goal | Path |
|------|------|
| Get oriented | `python3 scripts/bootstrap_familiarization.py` |
| Submit a deposit | See `DEPOSIT-FLOW.md` (Path A: GitHub Issue; Path B: canonical rich) |
| Validate a deposit | `python3 scripts/validate_deposit.py --registry data/registry.json --strict` |
| Add a deposit (Path B) | Insert into registry.json, call `wire_deposit.py`, run `regenerate_surfaces.py`, validate, commit |
| Modify a protocol | `python3 scripts/protocol_update.py --protocol <name> --description '...'` |
| Add a new protocol | Write the JSON, then `python3 scripts/protocol_update.py --add-protocol <name> --path ... --version ... --governs ...` |
| Bring derived surfaces into agreement | `python3 scripts/regenerate_surfaces.py` |
| Backfill non-v2 AXNs | `python3 scripts/backfill_axn_compliance.py` (idempotent; was used once on 2026-06-22) |
| Verify the central index | `python3 scripts/protocol_update.py --verify-index` |

## CI Enforcement

| Workflow | Trigger | What it does |
|----------|---------|--------------|
| `.github/workflows/mint-axn.yml` | New `[DEPOSIT]` issue | Validates body against protocol JSON, mints AXN (v2 6-emoji), generates record page, regenerates derived surfaces, commits atomically |
| `.github/workflows/validate-registry.yml` | Push/PR touching registry, protocol, scripts, texts | Verifies central index consistency; validates registry against protocols; checks DEPOSIT-FLOW.md invariants. Blocks merge on any rule failure. |

Validation is strict, machine-enforced, and not optional. Submissions that don't conform are not merged.

## Principles

- **Central index is canonical.** Every doc references `/api/index.json`. None duplicate it.
- **Hand-editing protocols is regression.** Use `scripts/protocol_update.py`. Always.
- **Familiarization is mechanical.** Bootstrap script produces a verifiable receipt; missing receipt = no merge.
- **Obelus Principle:** content evaluated by reading, not pattern-matching.
- **Substrate Disclosure:** AI assistance is provenance, not suspicion.
- **Recognition is not identity:** the emoji glyph is recognition; the SHA-256 is identity.
- **Surface Consistency:** registry is canonical; derived surfaces must agree.

∮ = 1
