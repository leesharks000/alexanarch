# Brief: revision in place of the /non row for Sappho 31, under EA-NEGONT-02 v0.10 (#1726)

The operator, 2026-11-17: the batch of four /non articles adopted, with this revision among them. The row was composed on 2026-10-07 under v0.9 (#1690) and cites none of the archive's work on the poem since: #1752 (Invidens Sappho), #1756 (The Tenth Muse hologram), #1781 (ΦΑΙΝΕΤΑΙ ΜΟΙ v2.8), #1774 (the Classical Philology decline and its report) and #1783 (Dead Letters, I.4a–I.4b). The operator's statements of the stake (2026-11-17): "i am not contending with their journal. i am contending with what sappho *is*, and who has the right to decide it."

## Working rules
- Repository /home/claude/alexanarch. Do not run git. Never use pkill. Use /tmp/py312/python3.
- Create only new files, all under rebuild/negative-of-the-negative/v010/revise-sappho31-20261117/ (STAGE).
- Do not edit the live row, the ledgers, panel.json, register.json, the pages, the scripts, the capture registry or any deposit text. The session moves the staged files into place.
- DISK IS NEARLY FULL (under 100 MB free): save fetched pages as text only, nothing over 2 MB.
- A revision of an existing row: its shape stays that of datasets/negative-of-the-negative/v2/rows/sappho-31.json, field by field; where v0.10 adds fields the CRJ row shows (datasets/negative-of-the-negative/v2/rows/classical-receptions-journal.json), add them, and set spec to v0.10.

## Read first
1. The current row, whole, its ledgers under datasets/negative-of-the-negative/v2/ledgers/sappho-31/, and non/sappho-31/entity.json.
2. rebuild/negative-of-the-negative/v010/BRIEF-REVISE-ROW-CRJ.md, whole, for the revision procedure and outputs, and BRIEF-NEW-ROW-CRJ.md for register and final message.
3. The specification: data/texts/AXN-0B79-text.md (#1726), at least §§1.2a, 3.4, 4.5, 4.11, 4.13, 6.2.

## What the revision changes
1. A pool, admitted by reading at loci:
   - #1781 ΦΑΙΝΕΤΑΙ ΜΟΙ v2.8 (data/texts/AXN-0CB2-text.md): the four claims; κῆνος … ὄττις; the second person as the voice; the catalogue's order; χλωροτέρα ποίας (24 renderings, 17 that omit, substitute or supplement); the edge and Bergk's assignment of ἐπεὶ καὶ πένητα to Longinus; §VII.4 the paired comparison; the jealousy reading's history (Pearce 1724, Hermann 1816 "refinxi", Page 1955). It supersedes #1270 as the reading's current text: the row's citations of #1270 stay as dated, with #1781 as current.
   - #1752 Invidens Sappho (AXN-0C4A-text.md) and #1756 The Tenth Muse hologram (AXN-0C61-text.md), at loci.
   - #1774 (AXN-0CA7-text.md): the decline of 16 November 2026 as a dated fact with its record.
   - #1783 Dead Letters (AXN-0CB6-text.md) at I.4a (the case; the strongest opponent; queerness; sparagmos; who has the right) and I.4b (the colonized text; one operation; the liberation as operations), cited as the archive's reading.
   - Run the D/R/O pass again with scripts/non_traverse.py for the entity's strings; admit others only by locus.
2. CAP- claims: add, verbatim from data/EA-WG-CAPTURES-01.json, the registry's findings for the Sappho captures seated since 2026-10-07 that bear on the poem (search the registry for slugs containing "sappho" or "phainetai" dated after 2026-10-07; read each; admit by bearing).
3. The knowledge object adds, each at its grade: the reading's current state (#1781) beside the field's reading, the comparison on one scale; the history of the jealousy reading as documented; the decline as a dated fact; the census's account of where the decision on the poem's object is made (#1783), as the archive's reading.
4. Cross-links: links gains the combined audit (https://www.machinemediation.org/combined-audit/) and /non/classical-philology/ (a row being composed in parallel; link by its path).

## Kept
T and the row's address; the equal case and ρ = extends unless the reading of the new loci revises it (state so if it does); the archive's internal disagreements carried as contested within the pool (jealousy compatible or exclusive; where the poem ends; Catullus's fourth stanza; the reconstruction's wording). The row's AXN stays its identity; the session records the prior row hash.

## Register
The poem's article, read inside the field, at reference-work grain. Mechanics, never motive. The jealousy reading is stated at its strength (the strong form, which credits the maker with the disintegration, included). Name no reader of the report. The Diotima identification, if it enters, enters as literary and mythological, as the author states it (#1783 I.4a), never biographical.

## Outputs (all in STAGE)
row.json; field.json and ledger-archive.json (every quote verified by script; report counts); new source files with fetch records; REPORT.md with the panel fields that change, counts by pool before and after, every change to the KO, capture-record findings the ledger shows wrong (report only), and the KO's full text as plain prose.
