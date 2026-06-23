# Alexanarch Workplan — Supplement, 2026-06-23 Evening
## Pivot: text recovery is not file recovery
## Adds Phase 7 (aesthetic) and Phase 8 (file salvage operation) to predecessor

**Author:** Lee Sharks (MANUS), under TACHYON synthesis
**Prepared:** 2026-06-23 evening
**Status:** Live forward-looking supplement to `WORKPLAN-2026-06-23-PM-RECONCILIATION.md`
**Predecessor:** `WORKPLAN-2026-06-23-PM-RECONCILIATION.md` (1162 lines, full structural reference). Predecessor remains canonical for unchanged sections; this supplement updates §1, §7, §8, §13, §17 and adds two new phase sections.

**Read order for a fresh instance:**
1. This supplement first (the pivot is load-bearing).
2. Predecessor §11 (verification ladder) + §15 (continuity tethers).
3. Predecessor §4–§7 (architecture, operations, failures).

---

# THE PIVOT (the headline correction)

The archive has been treating **recovery of textual content** as equivalent to **recovery of the deposited object**. It is not.

Zenodo defines a record as three things: metadata, files (the actual digital research object), and an identifier. A `description` field containing the whole text preserves *words*; it does not recover the original `.md`, `.pdf`, `.docx`, `.json`, image, archive — the original filename, MIME type, paratext, embedded assets, formatting, or exact bytes. The previous reconciliation passes (Phase 1, 3.5, 4) operated at the metadata layer: they tell us what was deposited, by whom, when, under what DOI. They do not return the artifacts.

**Empirical anchor (2026-06-23):** the IDP Charter record `10.5281/zenodo.18284857` is still publicly served by Zenodo. Its landing page exposes `idp_charter_v1.1.md`, `idp_charter_zenodo_metadata.json`, sizes, original MD5s, individual download links, and a download-all endpoint. Zenodo's own policy says retraction preserves files in storage. This means the salvage window is open *right now* — and may close.

**Revised central objective:**
> Recover every original artifact byte that Zenodo accepted into custody; identify every artifact that remains missing; and prevent reconstructed text from being mistaken for the deposited object.

The previous central objective ("recover the contents of the archive") was the map. This is the library.

---

# §Δ1 — Updated headline state (replaces predecessor §1)

Origin/main HEAD: `a6d96a5` — Phase 5+6 has landed (regenerate all derived surfaces + register `external_metadata` in `api/index.json` + comprehensive predecessor workplan). Working tree clean as of this supplement's writing.

**This session's work (in flight):**
- **Phase 7** aesthetic upgrade in flight: `scripts/md_render.py` built and tested (Palatino typography + robust markdown parser handling inline `## `, smushed tables, run-on bullet lists). Other 7.x sub-phases pending.
- **Phase 8** file salvage operation defined; tooling staged at `scripts/salvage_zenodo.py`, taxonomy at `scripts/recovery_status.py`. Cannot run from the container (Zenodo blocks datacenter IPs with generic 403). Designed to run from Lee's residential machine.

**Standing items unchanged from predecessor §1:** corpus deltas, sovereign/non-sovereign frame (§2), three DRAFT_PENDING deposits #446 #532 #760, mint workflow auto-merge pending §13.6.

---

# §Δ7 — Failure modes (additions)

### §7.18 — Category confusion: text-recovery treated as file-recovery (THIS SESSION, LOAD-BEARING)

**What broke:** Phase 1 recovered text from the OpenAlex/DataCite/Zenodo bulk XML stores. Where that text came from the `description` field of the Zenodo record, the archive nonetheless rendered it as "Full Text" on the record page. A reader cannot distinguish between (a) the originally deposited `.md`/`.pdf` file and (b) a depositor's prose description that happened to be long.

**Why it matters:**
- Original filename, MIME type, embedded assets, formatting, paratext, and exact bytes are lost.
- A `.pdf` deposit with a 50-character description and a 30-page article cannot be reconstructed from the description.
- Even where the description was textually complete (a poem, an essay), it is not the file. The file may have included a colophon, typesetting, an appendix, or a different version.

**Detection:** Lee's read of the rendered surfaces against Zenodo's stated record model.

**Recovery (Phase 8):**
- New `file_recovery_status` enum on every deposit (7 values, see §Δ8 firm rule #24).
- Live salvage scan against zenodo.org/records/N/ — files that are still served can be downloaded right now.
- Demand-letter strengthening: require return of the **byte streams**, not just the metadata content.
- Render-layer change: never display recovered text as "Full Text" without the qualifier *"Full textual content recovered from metadata; original deposited file not recovered."*

**Prevention (going forward):**
- Recovery passes always populate `file_recovery_status` explicitly. Default is `TEXT_RECOVERED_FROM_METADATA` for any text pulled from a metadata field.
- Sidecar schema additions per §Δ5.
- New firm rule (§Δ8 #24).

This failure mode is the cardinal pivot of this supplement and overrides any conflicting conventions in earlier passes.

---

# §Δ8 — Firm rules (addition)

### Rule 24 — Text recovered from metadata is never the file.

The display layer must distinguish the recovery hierarchy. Concrete requirements:

- Every deposit carries `file_recovery_status` ∈ {`ORIGINAL_FILE_RECOVERED`, `FILE_RECOVERED_UNVERIFIED`, `FILE_MANIFEST_ONLY`, `TEXT_RECOVERED_FROM_METADATA`, `TEXTUAL_RECONSTRUCTION`, `METADATA_ONLY`, `UNRECOVERED_FILE`}.
- The "Full Text" section header in record pages is replaced by status-specific headers (see §Phase 8.4).
- Reconstructed text never claims byte identity. Provenance is shown explicitly.
- Any sidecar referencing a metadata-derived text must set `text_source: "zenodo_description_field"` or similar — never `text_source: "file"`.

This rule supersedes any earlier rendering convention that conflated the two.

---

# §Δ13 — Open work (additions in priority order)

### §13.25 — Phase 8.1: salvage probe across all 1,817 record IDs  ⏳ TOP PRIORITY

**Why now:** files may stop being publicly served at any time. Every day of delay is exposure.

**Workflow:**
1. From Lee's residential machine, run `python3 scripts/salvage_zenodo.py --dry-run` to verify Zenodo reachability + see the inventory of record IDs that will be probed.
2. `python3 scripts/salvage_zenodo.py --probe-only` — fetches REST metadata + file listings for all 1,817 record IDs without downloading file content. Output: `data/file-recovery-ledger.json` with reported MD5/size/filename for every file that Zenodo will admit exists.
3. `python3 scripts/salvage_zenodo.py --download` — pulls actual bytes for every reachable file, verifies against reported MD5, writes to `recovered-originals/<record_id>/<filename>` with a per-record `manifest.json`.
4. Checkpointed and resumable. Polite rate limit (1 req/sec default).

**Status taxonomy applied to each result:**
- File downloaded + MD5 verified → `ORIGINAL_FILE_RECOVERED`
- File downloaded but no published MD5 → `FILE_RECOVERED_UNVERIFIED`
- File listing returned, bytes 403/404 → `FILE_MANIFEST_ONLY`
- Record returns 410 Gone → falls back to existing text-recovery → `TEXT_RECOVERED_FROM_METADATA` or `METADATA_ONLY`
- No record at all → `UNRECOVERED_FILE`

### §13.26 — Phase 8.2: recovery status migration on registry  ⏳ HIGH PRIORITY (post-probe)

- Add `file_recovery_status` to every deposit (additive — pure addition, never mutates).
- Default `TEXT_RECOVERED_FROM_METADATA` for deposits whose current text was pulled from a metadata field.
- Default `ORIGINAL_FILE_RECOVERED` only when the salvage probe confirmed bytes + checksum.
- DOI Resolution Index v3.4 → v3.5 includes `file_recovery_status` per mapping.

### §13.27 — Phase 8.3: render-layer status disclosure

- `wire_deposit.py` learns to read `file_recovery_status` and produce status-specific section headers and badges.
- "Full Text" becomes "Deposited File" / "Recovered File" / "Textual Content (from metadata)" / "Reconstructed Text" / etc.
- Visual signal (badge + color) makes status legible at a glance.

### §13.28 — Phase 8.4: demand letter v5

- Anchored on file return (the strict list in §Phase 8.5 below).
- Cites Zenodo's own published policy that retraction does not destroy files.
- The empirical claim of v4 (`871 DOIs return HTTP 404 from DataCite`) stays, augmented with: `the operator's stated policy commits to file preservation even on retraction`.

### §13.29 — Phase 7.x (aesthetic upgrade, in flight)

7.1 Palatino typography rolled through all surfaces (pending — small CSS change at every generator)
7.2 Robust markdown parser **built**, in `scripts/md_render.py`; integration into `wire_deposit.py` + mass re-render of 906 record pages pending
7.3 Structured External Metadata cards (pending; trivial)
7.4 Browse sort by `(date, deposit_number)` + label fix (pending; trivial)
7.5 Wiki portal (`data/wiki-portal.json` config, by-family/by-creator/alphabetic; current paginated list moves to `/s/wiki/all/`) (pending; medium scope)

**Sequencing note:** Phase 7.2 and Phase 8.3 *should land together* — re-rendering 906 record pages twice is wasteful. Either complete Phase 7.2 first and accept that the "Full Text" header is still wrong, or roll Phase 8 status field in before mass re-render. Recommended: Phase 8.1 (probe) first, then Phase 7 + 8.3 in a single mass re-render.

---

# §Δ17 — File inventory (additions)

### New directories and files

```
recovered-originals/                  — top-level, gitignored bytes by default
  <record_id>/
    <filename>                        — the actual deposited bytes
    manifest.json                     — per-record manifest with checksums + provenance
data/file-recovery-ledger.json        — master ledger across all 1,817 records
scripts/recovery_status.py            — taxonomy module + constants
scripts/salvage_zenodo.py             — salvage tool (designed for Lee's machine)
scripts/md_render.py                  — markdown parser (this session)
SALVAGE-INSTRUCTIONS.md               — how Lee runs the salvage from home
```

### New schema fields on deposit entries (additive, optional)

```
file_recovery_status        — enum value, see recovery_status.py
recovered_file_path         — "/recovered-originals/<id>/<filename>" when present
recovered_file_md5_zenodo   — Zenodo's published MD5 (string, 32 hex)
recovered_file_md5_verified — true/false (true means we computed and matched)
recovered_file_sha256       — our SHA-256 of the bytes (64 hex)
recovered_file_size_bytes   — int
recovered_file_retrieved_at — ISO-8601 UTC
recovered_file_mime_type    — string
text_source                 — "deposited_file" | "zenodo_description_field" |
                              "openalex_abstract" | "datacite_full_xml" |
                              "reconstruction" | "unknown"
```

`additionalProperties: true` on the deposit schema permits this without a schema bump.

---

# PHASE 7 — AESTHETIC AND UX UPGRADE (full section)

In flight as of this session. Stays separable from Phase 8.

## §7.1 — Typography

Move the prose stack from IBM Plex Sans to Palatino. System-font cascade (no web download):

```css
--serif: "Palatino Linotype", "Book Antiqua", Palatino, "URW Palladio L",
         "Georgia", serif;
--ui:    system-ui, -apple-system, "Segoe UI", sans-serif;   /* tiny UI bits */
--mono:  "IBM Plex Mono", "JetBrains Mono", "Menlo", monospace;
```

Application:
- Body, headings, prose, blockquotes → `--serif`
- Navbar, footer, tiny chips and badges → `--ui`
- AXN strings, code, file paths, hashes → `--mono`

The IBM Plex Sans @import can be removed entirely; pages get faster and crisper.

## §7.2 — Robust markdown parser (`scripts/md_render.py`)

Built and tested. Handles the malformations baked into AI-composed archive sources:
- Inline `##`/`###` glued mid-paragraph → split into proper headings
- Smushed tables (entire table on one line) → expanded to multi-row `<table>`
- Run-on bullet lists (`text:- one- two- three`) → expanded to `<ul>`
- Blockquotes, fenced code, links, auto-linked Zenodo DOIs

Public entry point: `from md_render import render`. Self-contained, no third-party deps.

Integration: replace the naïve inline parser in `wire_deposit.py` (lines 168–183 of the old version) with a call to `render(raw)`. Then mass re-render 906 record pages. Recommended to bundle this with §Phase 8.3 status disclosure to avoid a double re-render.

## §7.3 — Structured External Metadata cards

Replace the current vertical blob with a 2-column card grid:
- **Sidecar** — link + filename + bytes
- **DataCite severance** — coloured badge
- **OpenAlex Work IDs** — collapsed list (show 3, expand to see more)
- **Legacy Zenodo DOIs** — collapsed list (show 3, expand)
- **File recovery status** (NEW, from Phase 8) — badge with full label

## §7.4 — Browse: chronological sort + correct label

Current: sorted by `deposit_number` ascending. Label claims "oldest first" but #1 is dated 2026-06-19.
Fix: sort by `(date, deposit_number)` ascending. Label becomes "by date, oldest first" with a small affordance to also sort by deposit number on demand.

## §7.5 — Wiki portal

Current `/s/wiki/` is one paginated scroll of 861 entries. New structure (Metopedia-like):

```
/s/wiki/                       — portal: research paths + foundational entries + recent
/s/wiki/all/                   — current paginated list (moved here, unchanged behavior)
/s/wiki/family/<FAM>/          — 12 family pages (GOVERNANCE, EMPIRICAL, etc.)
/s/wiki/creator/<heteronym>/   — top 20 creator pages
/s/wiki/index/<A-Z>/           — alphabetic by title
/s/wiki/concept/<term>/        — selected concept pages from entity-index (Phase 7.5b)
```

**Curation seeded from `data/wiki-portal.json` (editable):**

Research-path seed (Lee revisable):
- Identifier infrastructure — Zenodotus' Book-Burning, DOIs ≠ Permanent Identifiers, AXN protocol
- Provenance and substrate — Compositional bystanding, Pristine Fallacy, Substrate Disclosure
- Semantic Economy — Semantic Liquidation, Inverse Prompt, Attribution Severance
- Assembly and heteronyms — Structural Distinction Protocol, the Dodecad, Lee Sharks aperture
- Capture and reception — Capture Registry, MMRS, Surface Visibility Instrument
- Continuity and tethers — gw.tachyon chain, LABOR/ARCHIVE/PRAXIS/TECHNE mantles
- Philology and historical logos — Sappho 31 / Catullus 51, Revelation First, Prolegomena to the Historical Logos
- Drain Hypothesis — pyramid/aquifer/Sahara, Atlantis Inversion

Each item links to its anchor deposit; the path is a curated tour, not an exhaustive index.

---

# PHASE 8 — FILE SALVAGE OPERATION (full section)

## §8.1 — Two parallel tracks

**Track A — Public file salvage (immediate, must run from residential IP).** For every known Zenodo record ID:

```
REST record endpoint            https://zenodo.org/api/records/<id>
OAI-PMH DCAT representation     https://zenodo.org/oai2d?verb=GetRecord&identifier=oai:zenodo.org:<id>&metadataPrefix=dcat
HTML landing page               https://zenodo.org/records/<id>
Individual file URL             https://zenodo.org/records/<id>/files/<filename>
Record file-archive endpoint    https://zenodo.org/records/<id>/files-archive
```

For every accessible file:

```
download original bytes
retain original filename
retain Zenodo record ID and DOI
retain reported MD5
verify reported MD5
compute SHA-256
record retrieval URL and timestamp
store HTTP headers
store a copy in controlled custody
```

**Track B — Backend return demand.** The existing demand letter (v4) anchors on the empirical claim about DataCite metadata severance. v5 (Phase 8.4) strengthens the file-return demand:

The required return includes:
- Original uploaded byte streams (every file, every version)
- Original filenames
- MIME types
- Sizes
- Deposited MD5 checksums
- Record and version associations
- Visibility state at time of termination
- Upload timestamps
- Internal file UUIDs / storage-object identifiers (proof of custody)

Cite Zenodo's own policy: retraction does not ordinarily destroy stored files. The operator's stated commitment is therefore: files exist; their non-return is a choice, not a constraint.

## §8.2 — Recovery status hierarchy (the canonical enum)

```
1. ORIGINAL_FILE_RECOVERED        — bytes recovered + MD5 verified against Zenodo's published checksum
2. FILE_RECOVERED_UNVERIFIED      — bytes recovered, no published MD5 to verify against
3. FILE_MANIFEST_ONLY             — filename + size + MD5 known, bytes missing
4. TEXT_RECOVERED_FROM_METADATA   — depositor-authored text from a description field (not the file)
5. TEXTUAL_RECONSTRUCTION         — new file constructed from recovered text (not the deposited artifact)
6. METADATA_ONLY                  — bibliographic record only; no substantive artifact
7. UNRECOVERED_FILE               — file existed (evidence in metadata), no bytes recovered
```

Levels 1–3 = file recovery. Level 4 = text recovery (not the file). Level 5 = a fabricated artifact (explicit, never silent). Levels 6–7 = absence with provenance.

The current archive collapses levels 1, 2, 4, 5 into "Full Text". Phase 8.3 uncollapses them.

## §8.3 — Render-layer status disclosure

For each `file_recovery_status` value, the record-page section gets a distinct header + badge:

| Status | Section header | Badge color | Note |
|---|---|---|---|
| ORIGINAL_FILE_RECOVERED | "Deposited File" | teal | "Original bytes, MD5 verified" |
| FILE_RECOVERED_UNVERIFIED | "Recovered File" | teal-dim | "Original bytes, MD5 unverified" |
| FILE_MANIFEST_ONLY | "File Manifest" | amber | "Bytes missing; manifest available" |
| TEXT_RECOVERED_FROM_METADATA | "Textual Content (from metadata)" | grey | "Depositor-authored text from the record's metadata field. Not the deposited file." |
| TEXTUAL_RECONSTRUCTION | "Reconstructed Text" | red | "Reconstructed from partial sources. Not the deposited artifact." |
| METADATA_ONLY | "Metadata Record" | grey | "No substantive content." |
| UNRECOVERED_FILE | "File Missing" | red | "Deposit existed; bytes not recovered." |

## §8.4 — Demand letter v5 (post-probe)

Compose only after the probe completes — the empirical anchor for v5 is the count and inventory of files that **Zenodo currently serves**. That number is the upper bound of what *should be in the return*.

Drafting structure (Ayanna Vox register):
1. Reference v4.
2. New empirical anchor: count of files still publicly served (proves files exist in Zenodo's custody).
3. Demand: byte-for-byte return of every file across all 1,817 DOIs in the strict list above.
4. Reference Zenodo's policy on retraction: files are preserved.
5. Compliance window.

## §8.5 — Ledger format

`data/file-recovery-ledger.json`:

```json
{
  "schema_version": "v1.0",
  "purpose": "Master ledger of file recovery state across all Zenodo records once associated with the Crimson Hexagonal Archive.",
  "generated_at": "ISO-8601",
  "tool_version": "salvage_zenodo.py v1.0",
  "total_records_probed": 0,
  "by_status": {"ORIGINAL_FILE_RECOVERED": 0, "...": 0},
  "records": [
    {
      "record_id": "18284857",
      "doi": "10.5281/zenodo.18284857",
      "deposit_number": 0,
      "axn": "AXN:...",
      "probed_at": "ISO-8601",
      "http_status_landing": 200,
      "http_status_rest": 200,
      "record_status": "published" | "tombstoned" | "404",
      "files": [
        {
          "filename": "idp_charter_v1.1.md",
          "size_zenodo": 13312,
          "md5_zenodo": "1ae8271eaf854fe9f7238b820f4cea5a",
          "mime_zenodo": "text/markdown",
          "download_url": "https://zenodo.org/records/18284857/files/idp_charter_v1.1.md",
          "local_path": "recovered-originals/18284857/idp_charter_v1.1.md",
          "size_recovered": 13312,
          "md5_recovered": "1ae8271eaf854fe9f7238b820f4cea5a",
          "md5_verified": true,
          "sha256_recovered": "...",
          "retrieved_at": "ISO-8601",
          "recovery_status": "ORIGINAL_FILE_RECOVERED"
        }
      ],
      "deposit_level_status": "ORIGINAL_FILE_RECOVERED"
    }
  ]
}
```

Per-record `recovered-originals/<id>/manifest.json` mirrors the per-record portion for portability.

## §8.6 — Custody and audit

- `recovered-originals/` is gitignored by default (large binaries, many; some may exceed GitHub size limits).
- A separate manifest tree at `data/recovery-manifests/<record_id>.json` is committed — small JSON, no bytes — so the public record of what was recovered is in-repo.
- A periodic `tar.gz` of `recovered-originals/` is uploaded to a mirror (alexanarch.org bulk-blob endpoint, or external custody) for redundancy.
- Every retrieval logs HTTP headers (the `last-modified`, `etag`, `content-md5`, `content-length`) into the per-file ledger entry for evidentiary value.

## §8.7 — Operational constraints

- **Residential IP required.** Datacenter IPs return generic 403. Lee runs the script from his home machine.
- **Polite rate limit.** Default 1 req/sec. Configurable.
- **Identifying User-Agent.** `Alexanarch-Salvage/1.0 (lee@alexanarch.org)` — makes us legible and accountable.
- **Resume-safe.** Checkpointed per record. Re-running skips completed records.
- **No authentication.** All endpoints are public.
- **No destructive operations.** Salvage is read-only against Zenodo.

---

# END OF SUPPLEMENT.

The pivot is: text recovery is not file recovery. The map is not the library. Phase 7 finishes the surface; Phase 8 retrieves the substrate. Run the probe first.

∮ = 1
