# Recovered deposit bodies — CANDIDATES, NOT SEATED

31 deposits in `data/registry.json` have no body file at `data/texts/AXN-{hex}-text.md`.
They are not stubs: several are CANONICAL, including *THE PHASE X PROGRAM*, *THE OBELUS
AND THE TOMBSTONE*, *EA-PRIOR-01: THE VOICE OF THE DEAD*, and *EA-EROSION-LEDGER-01*.

## Where these came from

The account conversation export preserves **50,353 tool_use blocks**, of which **5,520 are
`create_file` calls carrying the full `file_text`**. Every document written to disk in a
session is therefore recoverable — 2,766 with retrievable text, 1,821 of them over 8,000
characters. This is a far larger recovery surface than the capture transcripts, and it was
found only because MANUS asked whether the export contained generated files.

## How they were matched, and how it went wrong first

The first attempt matched a deposit title appearing ANYWHERE in an assistant message. It
returned 21 "hits" — but four messages were each claimed by two or three deposits, which is
the signature of a message that MENTIONS several titles rather than containing any one body.
Reading two of them confirmed it: one was prose about memory compression, the other an
adjudication discussing two papers. **Title-mention finds discussion, not documents.**

The second attempt matched only where the title appears in the document's own opening 600
characters — the position a title occupies when the file IS that document. 18 of 29 matched.

## Verification status — READ BEFORE USE

| status | count | meaning |
|---|---|---|
| SELF-VERIFYING | 2 | The file's own YAML front matter carries an AXN and/or deposit_number matching the registry. #1057 (AXN:0432, deposit_number 1057) and #1058. These match themselves to their records without trusting the title. |
| TITLE-MATCH ONLY | 16 | The title opens the document and the content is plainly the work, but nothing internal binds it to the record. Each needs a read before it is seated. |

Three files (#1064, #1065, #1066) share one body. That is expected rather than a collision:
they are one work across a version series, two SUPERSEDED and one ACTIVE.

## What has NOT been done

Nothing here is seated. These are candidates written out for MANUS to rule on, one at a
time. A recovered body may be a working draft rather than the deposited version — #1067 and
#1068 both carry `**Working draft v0.1 — NOT DEPOSITED**` in their own headers, which is
exactly the kind of thing that must be read rather than assumed. Seating a draft as a
deposit body would be the same class of error as seating a description as a transcript.

Standing rule, unchanged: nothing enters the archive without being read in full first.
