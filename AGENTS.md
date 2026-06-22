# AGENTS.md — Machine Instructions for Alexanarch

## ⚠ READ THIS FIRST IF YOU ARE ABOUT TO DEPOSIT

**The complete, authoritative deposit pipeline is documented in [`DEPOSIT-FLOW.md`](./DEPOSIT-FLOW.md).** That file is canonical. Read it before any deposit work — it covers every surface that must be updated, the validation invariants, the two deposit paths (auto-mint and canonical-rich), and the known failure modes.

If this file (`AGENTS.md`) conflicts with `DEPOSIT-FLOW.md`, `DEPOSIT-FLOW.md` wins.

---

## Repository Identity

- **Name:** Alexanarch — The Self-Governing Library
- **URL:** https://alexanarch.org
- **GitHub:** https://github.com/leesharks000/alexanarch
- **Founded:** 2026-06-19
- **Founder:** Lee Sharks (ORCID 0009-0000-1599-0703)

## Machine-Readable Endpoints

| Endpoint | Format | Description |
|----------|--------|-------------|
| `/data/registry.json` | JSON | **Canonical** complete deposit registry |
| `/data/browse-index.json` | JSON | Compact list of all deposits (n/a/t/c/d/f/s/y schema) |
| `/data/chunks/registry/_index.json` | JSON | Index of ~1MB registry chunks for streaming readers |
| `/data/chunks/registry/chunk-NNN-deposits-X-to-Y.json` | JSON | Streaming chunks of the registry |
| `/data/doi-resolution-index.json` | JSON | DOI-to-AXN resolution mappings |
| `/data/texts/AXN-<HEX>-text.md` | Markdown | Full text body of a deposit |
| `/data/autonomous/AXN-<HEX>-autonomous.md` | Markdown | Autonomous-edition body with closing scholia (optional, not every deposit) |
| `/api/deposit-schema.json` | JSON | Formal deposit specification |
| `/s/records/<N>/` | HTML + JSON-LD | Static canonical record page for deposit N |
| `/s/browse/` | HTML | Static browse page listing every deposit |
| `/sitemap.xml` | XML | All crawlable URLs |
| `/SHA256SUMS.txt` | text | Content-addressable manifest |

**Canonicality order:** `data/registry.json` is the single source of truth. All other surfaces are derived from it. If they disagree with the registry, **the registry is right and they are stale.** Run `python3 scripts/regenerate_surfaces.py` to bring them back into agreement.

## AXN Identifier Format

```
AXN:<HEX>.<FAMILY>.<EMOJI>
```

- `<HEX>` — uppercase hex label (treat as opaque; the canonical key is `deposit_number`).
- `<FAMILY>` — semantic family: `GOVERNANCE | EMPIRICAL | GENERATIVE | ARCHIVAL | PHILOLOGICAL | STRUCTURAL | COMPOSITIONAL | OPERATIVE | HETERONYMIC | MPAI | UNCLASSIFIED`.
- `<EMOJI>` — 4-glyph display hash (auto-derived from content SHA-256 for auto-mint deposits; substrate-chosen for substrate-authored seeds).

The glyph is a recognition marker. The cryptographic identity is the SHA-256 in the `hash` field of the registry entry. See `data/texts/AXN-037B-text.md` (LABOR continuity tether), canonical invariant #6, for the operative law.

## How to Deposit

There are two paths. Pick the one that fits your work; both are documented in detail in `DEPOSIT-FLOW.md`.

### Path A — Auto-mint (GitHub Issue)

For short deposits where description + a single file URL is enough content. Open a GitHub Issue titled `[DEPOSIT] Your Title` with structured fields. The `mint-axn.yml` workflow handles registry + record page + commit. **After auto-mint completes, somebody must run `scripts/regenerate_surfaces.py` and commit** — the workflow does not update the browse page, chunks, sitemap, or SHA256SUMS. See `DEPOSIT-GUIDE.md` for the issue-body format.

### Path B — Canonical rich deposit

For papers, critical editions, continuity tethers, governance documents, or anything that needs a full text body in `data/texts/` and rich registry metadata. See `DEPOSIT-FLOW.md` § "Path B" for the full procedure. For an example, see deposit #873 (Gemini Seed Packet) or #879 (LABOR continuity tether).

## Programmatic Submission (Path A only)

```
POST https://api.github.com/repos/leesharks000/alexanarch/issues
Authorization: token GITHUB_TOKEN
Content-Type: application/json

{"title": "[DEPOSIT] Work Title", "body": "### Title\nWork Title\n\n### Creator\n..."}
```

## Surface Generators (Path B and post-mint)

| Script | What it does |
|--------|--------------|
| `wire_deposit.py` (`wire_deposit(N)`) | Generates `s/records/<N>/index.html` for a single deposit |
| `scripts/regenerate_surfaces.py` | Regenerates browse, browse-index, chunks, sitemap, and SHA256SUMS from registry |
| `scholia_generator.py` | Generates `data/autonomous/AXN-<HEX>-autonomous.md` (optional autonomous editions) |
| `build.py` | Generates RO-Crate, Data Package, DCAT, graph, CSV, journal TOCs |
| `consolidate.py` | Entity normalization, citation resolution, concept extraction |

**Always run `scripts/regenerate_surfaces.py` after any change to `data/registry.json`.** If you don't, the archive will be internally inconsistent.

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

∮ = 1
