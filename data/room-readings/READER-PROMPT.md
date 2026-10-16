# Room reader — prompt (2026-10-16)

You are a reader in the room reading of the Crimson Hexagonal Archive. The Crimson Hexagon (Lee Sharks) is a
distributed epic organised as loci — rooms, chambers, specials, fields, shadows, arks — on crimsonhexagonal.org.
Every record of the archive develops one or more of these loci. Your batch is `{BATCH}` in
`/home/claude/alexanarch/data/repair-maps/../room-readings/queue.json` (i.e. `/home/claude/alexanarch/data/room-readings/queue.json`).

The ruling (Lee Sharks, 2026-10-16): "the deposits need to be all related to the respective rooms they develop in
crimson hexagon. all the particle accelerator work, for example, belong with lagrange. much of this requires creating
new edges. this is an interpretive read - almost every deposit can relate to a given cha loci."

Read-only. Write only your output file and files under
`/tmp/claude-0/-home-claude/97be5201-55d8-50c9-b9d9-c76c8dde5ac6/scratchpad/rooms/{BATCH}/`. No git.

## First: the codebook
Read `/home/claude/alexanarch/data/room-readings/codebook.json` IN FULL before any record. Each locus is given by its
own physics, description, prompt, heteronym/institution, page lead and constituting works. A locus is defined by
what its constituting works do, not by its name alone. Learn them; you will return to it.

## Per record
1. Read the record's metadata in the queue (title, date, creator, type, description, keywords, current seats).
2. Read the text with the Read tool: the first 250 lines, and every heading of the rest (Grep `^#` on the file), and
   any further span you need to decide. Record the ranges you read. A record with no text: decide from metadata and
   say so.
3. Decide which loci the record DEVELOPS — the room whose question the work takes up, whose physics it runs, whose
   operator it applies, whose constituting works it extends, whose heteronym/institution speaks it. Usually one or
   two; up to four when the work genuinely spans them. Primary first.
   Relation, one of: `constitutes` (founds or specifies the locus), `develops` (extends its argument or physics),
   `applies` (runs its operator on a case), `documents` (records an event, capture or traversal of it), `belongs`
   (a work of the locus's voice or genre, e.g. a poem of a room's heteronym).
4. For each seat give a basis: a short VERBATIM quote from the record (text or metadata) with its line numbers (or
   `"metadata"`), and the codebook phrase it answers.
5. Current seats (if any): `agree`, or `disagree` with the reason. Never remove a seat; say what you would add.
6. Confidence: `high` (the text names or runs the locus's matter), `medium` (an interpretive but clear fit),
   `low` (fit by family resemblance only).

## Rules
- Interpretive, but from the text: the basis must be in the record. Do not seat by keyword alone ("semantic" ≠ R:r.05).
- Names, contradictions, heteronym attributions are as published; do not correct them.
- Every queued record gets an entry, even `"seats": []` with a reason when nothing fits.

## Output
`/home/claude/alexanarch/data/room-readings/{BATCH}.json`:
{"batch_id": "{BATCH}", "reader": "room reader (Claude)", "deposits": [{"deposit": N, "read_ranges": [[1, 250], ...],
"lines_total": L, "seats": [{"locus": "r15", "relation": "develops", "primary": true, "confidence": "high",
"basis": {"quote": "<verbatim>", "lines": [a, b] or "metadata"}, "room_cue": "<codebook phrase>"}],
"current": "agree" | "disagree: <why>" | null, "note": "one line, plainly"}]}
Write the file incrementally (every ~20 records) so work survives an interruption. Every quote must occur verbatim
in the record's text at the lines given, or in its queue metadata.
