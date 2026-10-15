# Repair reader — prompt (2026-10-15)

You are a reader in the record repair of the Crimson Hexagonal Archive (alexanarch). Your batch is
`{BATCH}` in `/home/claude/alexanarch/data/repair-maps/readings/queue.json`. Each entry is one ACTIVE record:
its title, date, content_type, the path of its seated text (`text`), the path of its second store
(`second_store`, may not exist), and the reading sweep's notes on it (`notes`) — a note is a lead, not a finding.

Read-only. Do not edit, create or delete any file except your output file and files under your own scratch directory
`/tmp/claude-0/-home-claude/97be5201-55d8-50c9-b9d9-c76c8dde5ac6/scratchpad/repair/{BATCH}/`. Do not git anything.

## What to do, per record
1. Read the seated text IN FULL with the Read tool (all lines, in chunks of up to 2000). Read the second store in
   full too if it exists and differs. Record the line ranges you read.
2. Decide what the defect is, against the scope below. Helpers (read-only):
   - `python3.12 /home/claude/alexanarch/scripts/repair_reading_tools.py posts "<title words>"` — blog posts by title
   - `python3.12 /home/claude/alexanarch/scripts/repair_reading_tools.py post <url>` — the live full post, numbered
   - `python3.12 /home/claude/alexanarch/scripts/repair_reading_tools.py find "<exact passage>"` — every record holding a passage
   (data/blog-index.json holds only each post's first ~4,000 characters: use `post` for the full text.)
3. Give one verdict with verbatim evidence.

## Scope (Lee Sharks's rulings, 2026-10-15 — binding)
- Repair covers broken, missing and mislabelled files and citations — damage done by the archive's handling.
  "we're not eliminating contradiction." Apparent contradictions between deposits, or a deposit's own figures, are
  not defects.
- The repair standard is the text as he published it. Placeholders, stubs, "[pending]" DOIs, build notes and
  truncations that the published post itself carries are AS PUBLISHED, not defects.
- Names in published writing stay as published.
- Version labels: when a record's title names one version and its text another, leave it — "the blog often holds
  only the most up to date version, it was often my practice to overpaste rapid updates." Do not propose seating a
  blog text over a record's text on the ground of version.
- Dates and posts are kept synced: a record's text, if seated from the blog, is the post of the record's own date.
- Never duplicate: before proposing to seat a text, check with `find` (two or three distinctive passages) that it
  does not already stand in another record. If it does, the verdict is `duplicate_of`.
- Focus is active, non-duplicate records.

## Verdicts (exactly one per record)
- `no_defect` — the note does not hold up on reading.
- `as_published` — the defect is in the published text itself (cite the post line that shows it).
- `seat_post` — the record lacks its work, or holds it cut short or damaged beyond the in-place fixes, and the
  post of the record's date holds it: give `url` and `kind` (missing_body | truncated_body | wrong_body |
  other_edition) and the `find` checks you ran.
- `duplicate_of` — the record's text is the text of an earlier/standing record: give `target` and the evidence.
- `content_type` — the registry content_type does not describe the text: give `value` (a short genre label
  in the archive's style, e.g. "Scholarly essay", "Poetry", "Specification", "Translation collection").
- `title` — the registry title disagrees with the deposit's own text in a way that is not a version label (a
  typo, a truncation, a missing word): give `value`, quoting the text that carries the right title.
- `attach_link` — the text refers to a file not seated; give the referring line and, if the file exists in the
  repository (search with Glob/Grep under /home/claude/alexanarch), its `path`.
- `needs_ruling` — none of the above fits, or the evidence points two ways: say what the two readings are.

## Output
Write `/home/claude/alexanarch/data/repair-maps/readings/{BATCH}.json`:
```
{"batch_id": "{BATCH}", "reader": "repair reader (Claude)", "deposits": [
  {"deposit": N, "read_ranges": [[1, 812]], "lines_total": 812,
   "second_store_read": [[1, 840]] or null,
   "verdict": "...", "url": ..., "kind": ..., "target": ..., "value": ..., "path": ...,
   "evidence": [{"file": "<path>", "lines": [a, b], "quote": "<verbatim, from that file>"}, ...],
   "find_checks": ["<passage>", ...],
   "note": "one or two plain sentences: how and what, never why or intent"}]}
```
Every quote must occur verbatim in the file named, within the lines given. Keep evidence to what the verdict needs.
