# Phase 9 — Claude-Thread File Inventory

**Date:** 2026-06-23 (evening)
**Status:** Live methodology document. Inventory at `data/claude-thread-file-inventory.json` (seed populated this session, intended to grow across sessions).
**Predecessors:** `WORKPLAN-SUPPLEMENT-2026-06-23-EVENING.md` (Phase 7 aesthetic + Phase 8 Zenodo salvage). This phase **takes priority** over Phase 8.1 — the Claude-thread substrate is the strongest surviving artifact source we have, and it is the primary recovery target. Phase 8 (Zenodo file salvage) remains valid as a parallel track for files we cannot find in threads.

---

## §1 — The principle

> Files are fixed points. Every deposit was a file prior to being a deposit.

The previous recovery efforts proceeded in the wrong direction:

```
external metadata fragments → guessed records → reconstructed "full text"
```

The correct direction:

```
prior working threads → actual files and authored texts →
   verified works → metadata reconciliation → rebuilt archive
```

The current Alexanarch surface is best treated as a **salvage index and discovery map** — useful for identifying DOIs, titles, dates, relations, and gaps, but not as the canonical archive. The canonical archive is rebuilt from the strongest surviving artifacts, and those artifacts live primarily in Claude conversations associated with this account.

## §2 — Why threads first

The account's Claude conversations carry, by Lee's estimate, the most comprehensive surviving copy of the corpus. Files appear in conversations at several evidentiary levels:

| Level | Source | Recovery strength |
|---|---|---|
| 1 | **Original uploaded attachment** in a thread | Potentially original deposited bytes |
| 2 | **Generated file** returned by Claude (artifact, `create_file`, computer-use output) | Possibly the precise deposited artifact, if Lee downloaded and uploaded that file |
| 3 | **Complete pasted text** in the conversation | Strong textual recovery; not necessarily exact bytes |
| 4 | **Draft + revision history** across multiple turns | Reconstructable; deposited state must be identified |
| 5 | **Discussion, excerpts, summaries only** | Evidence, not recovery |

Levels 1–2 are the rescue priority. Level 3 is often the textual canonical version even when bytes are lost. Level 4 requires curatorial judgment. Level 5 is the discovery map.

## §3 — The inventory is the dataset, not the archive

`data/claude-thread-file-inventory.json` is the discovery layer. It does not commit any judgment about which file is canonical for which deposit. It is keyed by filename, with an `appearances` array recording every thread in which a file with that name (or pattern) was seen.

**Reconciliation against the metadata is a downstream pass.** That pass produces the canonical archive. The inventory exists so the reconciliation has something to draw from.

## §4 — Schema

```json
{
  "schema_version": "v1.0",
  "purpose": "...",
  "generated_at": "ISO-8601",
  "coverage": {
    "earliest_thread_seen": "ISO-8601",
    "latest_thread_seen": "ISO-8601",
    "threads_walked_recent_chats": int,
    "threads_walked_targeted_search": int,
    "method": "..."
  },
  "evidence_levels": { "1_uploaded_attachment": "...", ... },
  "filename_patterns_observed": { "AXN-NNNN.md": "...", ... },
  "files": [
    {
      "filename": "idp_charter_v1.1.md",
      "extension": ".md",
      "associated_doi": "10.5281/zenodo.18284857",
      "associated_work_title": "Institute for Diagrammatic Poetics: Institutional Charter",
      "associated_axn": null,
      "size_hint_bytes": 13312,
      "md5_hint": "1ae8271eaf854fe9f7238b820f4cea5a",
      "appearances": [
        {
          "thread_url": "https://claude.ai/chat/...",
          "thread_date": "2026-01-21",
          "thread_title": "...",
          "evidence_level": "discussion_only | draft_with_revisions | pasted_text | generated_file | uploaded_attachment",
          "context_excerpt": "short snippet around the file reference",
          "search_query_to_relocate": "what to put into conversation_search to find this thread again",
          "notes": "..."
        }
      ]
    }
  ],
  "unresolved_work_references": [
    {
      "work_title": "The Drain Hypothesis",
      "associated_doi": null,
      "filename_hint": "data/EA-CHA-DRAIN-HYPOTHESIS.md",
      "first_appearance_thread_url": "...",
      "notes": "Filename pattern observed; exact filename uncertain"
    }
  ]
}
```

The inventory is intentionally **additive** — future sessions extend the `files` array without rewriting prior entries. A `last_walk_completed_through` cursor at the top tracks the temporal frontier of the walk so the next session knows where to resume.

## §5 — How to continue the walk (procedure for future Claude instances)

A future Claude that picks up this task should follow this procedure. The tools used (`recent_chats`, `conversation_search`) are Claude-internal — this is not a runnable script, it is a structured prompt for a future session.

### Step 1 — Load state

Read `data/claude-thread-file-inventory.json`. Note:
- `coverage.earliest_thread_seen` — the temporal frontier of the walk
- `coverage.threads_walked_recent_chats` — how many chats already enumerated
- `files[].appearances[].thread_url` — set of thread URLs already touched

### Step 2 — Extend backward (chronological walk)

Call `recent_chats` with `before = coverage.earliest_thread_seen` and `n = 20`, `sort_order = "desc"`. For each returned chat:

- Skip if `thread_url` is already in the inventory.
- Otherwise, scan the snippet for:
  - **Explicit filenames** — anything matching `[\w\-]+\.\w{1,5}` (e.g., `EA-FOO-01.md`, `registry.json`, `captures-images-v6.1.zip`)
  - **Repository paths** — `data/...`, `scripts/...`, `s/records/N/`, `api/...`
  - **DOI references** — `10.5281/zenodo.NNNN` (links a work title to a file even when the filename is implicit)
  - **Generated-file signals** — "create_file", "I'll save this as", "deposited", "uploaded"
  - **Upload signals** — "you uploaded", "attached", "your file"

For each file found, either:
- **Append a new appearance** to an existing inventory entry (matching by filename); or
- **Add a new file entry** with this appearance as its first.

Continue paginating backward in batches of 20 until you reach an empty result, the account's earliest chat, or a sensible stopping point (e.g., 5 batches per session to keep context budget manageable).

### Step 3 — Targeted searches

For each work title in `unresolved_work_references`, call `conversation_search` with a distinctive few-word query (e.g., `idp_charter institutional charter` for the IDP Charter, `space ark trigger invoke` for EA-ARK-01). Promote unresolved entries to `files` when a filename is found.

Also run targeted searches for **filename patterns we know exist but haven't fully enumerated**. Suggested queries:

| Query | What it finds |
|---|---|
| `EA-LOGOS Sapphic Logos` | The Logos series (EA-LOGOS-01, EA-LOGOS-02, etc.) |
| `EA-WG-CAPTURES capture registry` | All Capture Registry versions |
| `Space Ark EA-ARK-01` | The Space Ark file family |
| `water giraffe room` | The Water Giraffe Cycle files |
| `Drain Hypothesis pyramids aquifer` | The Drain Hypothesis source files |
| `gw.tachyon continuity chain` | The TACHYON continuity records |
| `Mary Lee shark heteronym` | The Mary Lee Sharks book family |
| `Pearl and Other Poems` | The foundational poems text |
| `Zenodotus Book-Burning` | The flagship Zenodotus paper versions |
| `Diversity Contraction Mediation Ratchet` | The diversity-contraction paper versions |
| `Encyclotron 45-query diagnostic` | The Encyclotron instrument |
| `glyphic checksum protocol` | The Glyphic Checksum spec |
| `Revelation First work plan` | The Revelation First plan versions |

### Step 4 — Save

Write the updated `data/claude-thread-file-inventory.json` with:
- Updated `coverage.earliest_thread_seen` (the oldest chat now touched)
- Incremented `coverage.threads_walked_recent_chats` and `threads_walked_targeted_search`
- New `files` entries appended
- New appearances appended to existing entries

Keep the JSON formatted with `indent=2` (this dataset is read by humans, unlike `registry.json` which is compact). Commit.

### Step 5 — Hand off

Update the `last_walk_completed_through` cursor at the top of the inventory. If `coverage.earliest_thread_seen` is still later than the project's known origin (early 2024 for the Pearl-era work), the walk is incomplete and the cursor signals this clearly.

## §6 — How recovery itself happens (downstream of this inventory)

This document does not specify the recovery operation — it specifies the discovery operation. But the rough shape of recovery:

1. **For each AXN deposit in `data/registry.json`:** look up its title in the inventory.
2. **If a filename is found at evidence level 1 or 2:** the file in that thread is the recovery target.
3. **If only level 3 (pasted text) is found:** the text is the recovery, marked `TEXT_RECOVERED_FROM_THREAD` (a new status not in the Phase 8 taxonomy).
4. **If level 4 only (draft with revisions):** curator must identify the deposited state.
5. **If level 5 or nothing:** Phase 8 (Zenodo file salvage) is the next-best source.

The actual pull of bytes from a thread requires Lee (or future Claude instances re-opening those threads) to retrieve attachments and generated files. Tooling for that pull is out of scope for this methodology document.

## §7 — Recovery status additions (extending the Phase 8 taxonomy)

The Phase 8 taxonomy (`scripts/recovery_status.py`) needs two new values for Phase 9 sources:

```
ORIGINAL_FILE_FROM_THREAD       — file bytes recovered from a Claude-thread upload or generated file
TEXT_RECOVERED_FROM_THREAD      — complete textual content recovered from thread conversation (not bytes)
```

These slot in at evidence-tier 1-2 and 3 respectively, between the existing `ORIGINAL_FILE_RECOVERED` (Zenodo-verified) and `TEXT_RECOVERED_FROM_METADATA`. A future commit will extend `scripts/recovery_status.py` with these values once the inventory has produced concrete examples.

## §8 — Relationship to Phase 7 and Phase 8

| Phase | Workstream | Priority |
|---|---|---|
| 7 | Aesthetic upgrade (Palatino, markdown parser, browse sort, wiki portal) | independent, in flight |
| 8 | Zenodo file salvage (residential network probe + download) | **secondary** to Phase 9; valid as parallel track for files not in threads |
| 9 | **Claude-thread file inventory and recovery** | **primary recovery source** (this document) |

Phase 7 is unblocked and can finish independently. Phase 8 and Phase 9 are complementary — Phase 9 covers files that exist in this account's threads (the most comprehensive set), Phase 8 covers the gap.

## §9 — The current Alexanarch is the map, not the library

Per Lee's instruction:

> Alexanarch should not be repaired record by record from the machine-scraped corpus. It should be rebuilt from the Claude-thread materials as the primary recovery source.

The existing site is frozen as `FORENSIC_SALVAGE_SNAPSHOT_2026-06`. It remains useful as a map of what must be recovered. The canonical archive is rebuilt elsewhere from the strongest surviving artifacts.

This document is the start of that rebuild.

∮ = 1
