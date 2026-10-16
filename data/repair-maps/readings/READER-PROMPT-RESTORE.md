# Restore reader — prompt (2026-10-15, late)

You are a reader in the record repair of the Crimson Hexagonal Archive (alexanarch). Your batch is `{BATCH}` in
`/home/claude/alexanarch/data/repair-maps/readings/queue2.json`. Each entry is one record with its seated text
(`text`), its second store (`second_store`, may not exist), its date, and a `task` naming the suspected damage.

Read-only. Write only your output file and files under
`/tmp/claude-0/-home-claude/97be5201-55d8-50c9-b9d9-c76c8dde5ac6/scratchpad/repair/{BATCH}/`. No git.

## Per record
1. Read the seated text IN FULL with the Read tool (chunks up to 2000 lines); read the second store in full if it
   exists and differs. Record the ranges.
2. Get the published text: `python3.12 /home/claude/alexanarch/scripts/repair_reading_tools.py posts "<title words>"`
   then `... post <url>` (the live full post, numbered). Use the post of the record's OWN DATE ("keep dates and posts
   synced"). `... find "<passage>"` searches every seated text. data/blog-index.json holds only ~4,000 characters per
   post: never use it for comparison.
3. Decide, and give the exact repair.

## Scope (Lee Sharks's rulings, 2026-10-15 — binding)
- Repair standard: the text as he published it. Damage done by the archive's handling (conversion, stripping,
  truncation, garbling) is repaired; what the published post itself carries is AS PUBLISHED.
- The blog often holds only the latest version ("it was often my practice to overpaste rapid updates"): never
  replace a record's text with a different version on the ground of version. Restore only what is missing or damaged
  in the SAME text.
- Never duplicate: if the full text already stands in another record, say so (`duplicate_of`).
- Names stay as published. Contradictions are not defects.

## Verdicts (one per record)
- `restore_sections` — give `restorations`: a list of {"after_line": N (in the seated text, the heading or line the
  content belongs under), "seated_lines": [a, b] (the damaged span to replace, or null to insert), "source": "<url or
  file path>", "source_lines": [a, b], "content": "<the exact markdown to seat, copied from the source, characters
  kept>"}. Content must be copied from the source verbatim (the `post` helper's output is the conversion to use).
- `seat_second_store` — the second store is the published text whole and the seated text a damaged or partial
  copy of the SAME text: say so with evidence.
- `as_published` · `no_defect` · `duplicate_of` (`target`) · `needs_ruling` (state both readings).

## Output
`/home/claude/alexanarch/data/repair-maps/readings/{BATCH}.json`:
{"batch_id": "{BATCH}", "reader": "restore reader (Claude)", "deposits": [{"deposit": N, "read_ranges": [[1, L]],
"lines_total": L, "second_store_read": [[1, M]] or null, "verdict": "...", "restorations": [...], "target": ...,
"evidence": [{"file": "<path or url>", "lines": [a, b], "quote": "<verbatim>"}], "note": "how and what, plainly"}]}
Every quote and every `content` must occur verbatim in the file or post named, at the lines given.
