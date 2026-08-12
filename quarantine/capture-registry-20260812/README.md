# Capture Registry — quarantine, 2026-08-12

Withdrawn from publication, not deleted. These are the files as they stood at
withdrawal, retained so the defective state remains auditable.

    EA-WG-CAPTURES-01.json                  v9.55, 288 entries, 207 seated transcripts
    datasets-copy-EA-WG-CAPTURES-01.json    the dataset-surface copy of the same
    captures-index.html                     the rendered gallery as published

## Why withdrawn

Automated repair passes on 2026-08-11 and 2026-08-12 extracted quoted passages from
analyst descriptions and seated them as verbatim machine transcripts. Measured against
independent copies of the same records:

  119 / 207  seated transcripts are verbatim substrings of their own entry's `d` field
   49        of those `d` values are byte-identical to `description_html` in the June
             leesharks.com registry — i.e. demonstrably analyst summaries
  130        seated transcripts are shorter than the description they came from
   15        entries carry a transcript AND a status saying none was seated
  207        entries carry a READ-VERIFIED marker asserting a per-entry comparison
             against query and description that was NOT performed; verification was a
             bulk register screen of transcript openings

The last item is the primary defect. A wrong transcript is an error; a wrong transcript
stamped read-verified is an error that instructs future readers not to re-check it.

## Responsibility

The defects were introduced by the assistant (TACHYON) executing bulk repair passes,
including a verification marker whose wording asserted more than the act performed.
They were found by MANUS on inspection and confirmed by audit against the recovered
palette.

## Recovery basis

Nothing is lost. A working database at palette/capture-palette.sqlite holds every
version of every capture-bearing file from four repositories — 138 registry versions,
330,530 field observations, 316 distinct capture keys, 55 companion and manifest file
versions, harvested across 3,235 commits. Sources are kept separate and attributed;
nothing in it is merged or preferred.

Reconstruction proceeds per record, per field, from that palette, with provenance
stated and verification claims limited to what is actually done.
