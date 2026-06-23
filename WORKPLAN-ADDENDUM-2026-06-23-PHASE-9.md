# Workplan Addendum — Phase 9 declares primacy
## 2026-06-23 evening, second supplement

**Predecessor:** `WORKPLAN-SUPPLEMENT-2026-06-23-EVENING.md` (Phase 7 + Phase 8)
**Methodology:** `docs/PHASE-9-CLAUDE-THREAD-FILE-INVENTORY.md`
**Inventory:** `data/claude-thread-file-inventory.json`

---

## The correction

> "We're going about this wrong. Almost all those files exist in previous threads in this account. And that is the most comprehensive set of files. And now we have the metadata. I kinda think we need to go thru and pull every single file while we can."
>
> "Files are fixed points. Every deposit was a file prior to being a deposit. We first need to simply list out every file in the account, and dump them to a dataset — with addresses that allow quick ability to locate by Claude in its own memory, and the files themselves if possible. Then we can reconcile against the metadata."

— Lee Sharks, 2026-06-23 evening

## What this changes

### Phase priority order is reorganized

| Phase | Workstream | Priority | Status |
|---|---|---|---|
| 9 | **Claude-thread file inventory + recovery** | **PRIMARY** | seeded this session (29 files, 11 unresolved works, 35 chats walked) |
| 8 | Zenodo file salvage from residential network | secondary (parallel for files not in threads) | tooling built, awaiting run |
| 7 | Aesthetic upgrade (Palatino, markdown parser, browse sort, wiki portal) | independent, unblocked | parser built, rest pending |

### The corollary correction (from Lee's second message in this exchange)

> "Alexanarch should not be repaired record by record from the machine-scraped corpus. It should be rebuilt from the Claude-thread materials as the primary recovery source."

The current Alexanarch site is frozen as `FORENSIC_SALVAGE_SNAPSHOT_2026-06`. It remains useful as a **salvage index and discovery map** — DOIs, titles, dates, relations, gaps — but is no longer the target of repair-in-place. The canonical archive is rebuilt elsewhere from the strongest surviving artifacts.

Promotion of any recovered item into the canonical archive requires evidence:
- exact DOI in the thread;
- exact title and version;
- filename matching Zenodo metadata;
- checksum matching a Zenodo file manifest;
- contemporaneous "this is the final/deposit version" language;
- close comparison against recovered description text;
- manual confirmation where ambiguity remains.

**No recovered item enters the canonical archive merely because a machine matched its title.**

### Architecture: two layers, separated

**Canonical archive (clean):**
- verified original files
- strongly authenticated deposited versions
- clearly marked reconstructions where originals remain unavailable

**Forensic registry (messy because it records the investigation):**
- OpenAlex / DataCite / Zenodo bulk metadata
- Claude-thread file inventory (this phase)
- surviving repository pages
- local files
- machine associations
- unresolved candidates

The current `data/registry.json` becomes the forensic registry. A new canonical archive is built incrementally as recovered files reach the evidence threshold.

## Recovery status taxonomy — additions for Phase 9

`scripts/recovery_status.py` needs two new values to capture the thread-source evidence:

```
ORIGINAL_FILE_FROM_THREAD       — file bytes recovered from a thread upload or generated file
TEXT_RECOVERED_FROM_THREAD      — complete textual content recovered from thread conversation
```

These slot between `ORIGINAL_FILE_RECOVERED` (Zenodo-verified) and `TEXT_RECOVERED_FROM_METADATA`. The taxonomy module will be extended in a follow-on session once the inventory has produced concrete examples to test against.

## What landed this session

| Artifact | Purpose |
|---|---|
| `docs/PHASE-9-CLAUDE-THREAD-FILE-INVENTORY.md` | Methodology, schema, continuation procedure |
| `data/claude-thread-file-inventory.json` | Seed inventory: 29 files, 11 unresolved works, 35 chats walked Jan-Jun 2026 |
| this addendum | Workplan delta declaring Phase 9 primary |

## Next moves

1. **Continue the walk backward.** A future Claude session uses the procedure in `docs/PHASE-9-CLAUDE-THREAD-FILE-INVENTORY.md` §5 to extend coverage. Cursor: `before=2026-04-05T18:05:00Z`. Aim to reach the earliest chat in the account.

2. **Run targeted searches.** For each entry in `unresolved_work_references`, run a `conversation_search` query to find the filename. Promote to `files` when located.

3. **Build per-thread retrieval plans.** For files at evidence levels 1 (uploaded) and 2 (generated), the actual byte pull requires Lee to re-open the thread (or for future Claude to operate inside the thread and surface the attachment). Future work: a `retrieval-plans/<thread-id>.md` per-thread plan listing files to extract.

4. **Cross-reference against registry.** Once the inventory is broader, walk `data/registry.json`'s 906 deposits and match each to inventory entries. Identify the deposits with NO thread coverage — those become priority Phase 8 (Zenodo salvage) targets.

5. **Build the canonical-archive substrate.** A new repository structure separate from the existing alexanarch one — `recovered-canon/` (or similar) — with strict promotion criteria. The current alexanarch repo becomes the forensic registry as-is.

The map is not the library. The library is in the threads. Pull while you can.

∮ = 1
