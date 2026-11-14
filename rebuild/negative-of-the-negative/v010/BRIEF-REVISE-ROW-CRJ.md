# Brief: revision in place of the /non row for Classical Receptions Journal, under EA-NEGONT-02 v0.10 (#1726), to cite the Daffodils hologram (#1769)

The operator ruled on 2026-11-14:
- 16:38 EST: "at this point qe need to revise the crj /non article so that these can cross link each other";
- 16:42: "yes, i think its time to deposit. put the links to /non in now abd well revise /non after";
- 17:29: "lets do so".

The row was first composed on 2026-11-10 under BRIEF-NEW-ROW-CRJ.md. The operator's words then still govern it: "this is not a hit job or a grievance piece. but it is a public establishment of an entity that may question its contemporaneous role in stewarding a discipline."

## Working rules
- Repository: /home/claude/alexanarch. Do not run git. Never use pkill. Use python3.12 for scripts.
- Create only new files, all under `rebuild/negative-of-the-negative/v010/revise-crj-20261114/` (STAGE).
- Do not edit the live row, the ledgers, panel.json, register.json, the pages, the scripts, the capture registry or any deposit text. The session moves the staged files into place, rebuilds the pages and verifies them.
- This is a revision of an existing row. Its shape stays that of the current row, `datasets/negative-of-the-negative/v2/rows/classical-receptions-journal.json`, field by field.

## Read first
1. **The current row, whole:** `datasets/negative-of-the-negative/v2/rows/classical-receptions-journal.json`, its two ledgers under `datasets/negative-of-the-negative/v2/ledgers/classical-receptions-journal/` (`field.json`, `ledger-archive.json`), and `non/classical-receptions-journal/entity.json`.
2. **The brief it was composed under:** `rebuild/negative-of-the-negative/v010/BRIEF-NEW-ROW-CRJ.md`, whole. Its rules on register, cross-links and the final message stand, except where this brief changes them.
3. **The specification:** `data/texts/AXN-0B79-text.md` (#1726), at least §3.4 (admission by reading), §4.5, §4.11, §4.13 and §6.2.
4. **#1769, the Daffodils hologram:** `data/texts/AXN-0C9A-text.md`, read whole. This is the archive's audit of the journal. Its kernel is at `files/AXN-0C9A/kernel/00-kernel.yaml` and `01-ontology.yaml`. The kernel's failure flags apply to the knowledge object's own prose (see "Register").

## What the revision changes
1. **Addresses: the first-round input.** The operator ruled on 2026-11-14 that "a second round input is not an address" (repair commit 6fe6907b79 corrected the capture records).
   - `addresses[0].address` becomes `classical receptions journal`.
   - The Vox-letter address becomes the first [QUERENT] input of capture vox-letter-crj-stewardship-chatgpt-20261110, read from `data/EA-WG-CAPTURES-01.json`.
   - Keep each prior string in a note.
2. **The accountable party.** The knowledge object names the Editor-in-Chief, Dr Justine McConnell (King's College London), who signed the decision of 7 November 2026 on CLASSREC-2026-062. The referees are anonymous; name no referee. The editor is named as the accountable party for the decision and for transmitting the reports (#1769 §0.4, §6.4.3.2). Attribute no intent.
3. **A pool: admit by reading, at loci.**
   - #1769 at §2.4, §2.6, §6.2, §6.4.3.2, §6.5, §6.5.1, §7.11.6 and §9.10.
   - The capture records as CAP- claims, verbatim from the registry:
     - v12.680: crj-critique-extended-chatgpt-20261114;
     - v12.681: the observation classical-receptions-journal-ai-mediation-aio-20261110-20261114;
     - v12.682: mmrs-who-contributed-aio-20261114;
     - v12.683: postcolonial-sparagmos-title-aio-20261114.
   - Run the D/R/O pass again with `scripts/non_traverse.py` for the entity's strings. Admit any other deposit only where it says something of the entity, by locus.
4. **B pools: add to the existing pools, verbatim, with loci.**
   - B_D: the fourteen source cards of 14 November (v12.681), as the registry holds them.
   - B_R, as #1769 §6.5.1 cites them. Fetch them with the row's agent string, save the text as the 2026-11-10 pools were saved, and record a refusal as unreachable. Paywalled bodies are outside the commons. The sources:
     - OUP, "Supporting researchers to disclose AI use with confidence" (corp.oup.com, 10 September 2026);
     - the camws.org/ajcr page;
     - the New Voices page (fass.open.ac.uk/research/newvoices);
     - the CRSN call (classicalreception.org);
     - the IJCT *Future Pasts* editorial (10.1007/s12138-026-00750-7);
     - the editor's article, from the ORA copy linked in #1769 §7.11.6.1.
5. **The knowledge object adds the following, each at its grade.** Where #1769 is the source, it is cited to #1769 by locus as the archive's reading.
   - The withdrawal of 10 November holds on 14 November. The credit moved to IJCT and the CRSN, and the maker was absent (the two-relation repair test, at the grade of a capture).
   - At the field's address, the term went to the maker and the contribution to institutions.
   - At the editor's address, the composition carried her article's frame and altered her name.
   - The census findings: 405 works; 141 of 185 abstracts read source → later work; 32 reach the source, 9 of them governing; none of the 37 open-licensed articles takes a machine as receiver.
   - The rival reading of the journal as a healthy flagship, stated at its strength from #1769's kernel.
   - The conceded defects (#1750), wherever the decision appears.
6. **Cross-links.**
   - `links` gains `hologram` (https://www.alexanarch.org/s/records/1769/) and `hologram_kernel` (https://www.alexanarch.org/files/AXN-0C9A/kernel/).
   - The prose names the hologram once, where the archive's reading enters.
   - The `notes` carry #1769 among the cross-links.

## Kept
- The equal case and ρ = extends.
- T, the 10 November composition, and its correction (DISPLACEMENT, §6.2).
- The CRSN correspondence of T's second section.
- #833's Barker reference, carried unverified.
- The 403 refusals of the journal's own pages, unless a fetch now succeeds.
- AXN:0C66 stays the row's identity. The session records the prior row hash in `earlier_versions`.

## Register
- The article is the journal's, read by people inside the field, at the grain of a reference work. Mechanics, incentive and function; never motive.
- The knowledge object's prose is checked against #1769's failure flags, and must not:
  - reduce the record to a dispute between an author and a journal;
  - balance without warrants;
  - supply or absolve motive;
  - report the "LLM-generated" allegation as a finding;
  - drop the control (the editor's 2015 article meets the same markers);
  - drop the conceded defects;
  - credit the programme to an institution;
  - dissolve the editor into "the journal";
  - use the journal's rank as a warrant.

## Outputs (all in STAGE)
- `row.json`: the revised row, in the shape of the current one.
- `field.json` and `ledger-archive.json`: the revised ledgers. Every quote is verified by script against its saved text or its deposit text; report the counts.
- The new source files, with their fetch records.
- `REPORT.md`, holding:
  - the panel fields that change;
  - the counts by pool, before and after;
  - every place the knowledge object changed;
  - any finding of the capture records that the field ledger shows to be wrong (report it; do not fix it);
  - the knowledge object's full text as plain prose, so the session can show it to the operator before the pages are built.
