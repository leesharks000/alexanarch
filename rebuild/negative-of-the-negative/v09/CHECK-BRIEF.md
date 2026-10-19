# Independent check of one v0.9 /non composition (you have not seen it composed)

Repository /home/claude/alexanarch. Read-only, except your one report file: rebuild/negative-of-the-negative/v09/check-<ROW>.json. Do not run git; do not edit anything else.

Read: the specification data/texts/AXN-0700-text.md §0.7–0.10, §1.2a, §4.1–4.8, §5.10; the composition rebuild/negative-of-the-negative/v09/<ROW>.json; the row's ledgers (paths in datasets/negative-of-the-negative/v2/rows/<ROW>.json → ledger.field and ledger.archive); the defining papers the composition names (data/texts/AXN-<HEX>-text.md; hex from data/registry.json).

Check, and report every finding with its location (KO sentence n, P section/item, translation row, case locus):
1. Reverse entailment: each KO sentence and each P lede/item is entailed by the ledger entries it cites (read their quotes). Flag any statement not supported, any number/date/name not in the cited quotes, and any cited id that does not bear on the sentence.
2. Attribution (§4.5): the source named in the sentence for archive claims (deposit number or author as the ledger has it).
3. Force (§4.4): the archive's claims carried at their own modality, with their stated falsifiers/limits; no proviso or cushion lowering an archive claim by standing ("on a reading proposed against the received one", "the entity evolves", "closely related", "a school"); no raising of force either.
4. The case: is the case reading (equal / witness / mixed) and ρ supported by the quoted loci, and are the loci verbatim in the named texts? Would a reader of the same defining papers decide differently? Say why.
5. Structure: in the equal case, does the KO open with the field's composition as a block, or close with the archive's as a block (§4.1, §5.10)? In the witness case, does E_A's definition lead and do field claims stand where translations place them?
6. Coverage: senses present in the ledgers but absent from the KO (C_ex); kernel claims (kernel: true) cut.
7. Translation: every field claim in exactly one row; received quotes verbatim from field.json.
Output JSON: {"row": "<ROW>", "checker": "<label>", "findings": [{"id": "C1", "where": "...", "kind": "entailment|attribution|force|case|structure|coverage|translation", "severity": "must-fix|should-fix|note", "finding": "...", "evidence": "verbatim from ledger/text", "fix": "concrete replacement text or action"}], "case_agrees": true/false, "summary": "..."}
Final message: counts by severity and the one-line summary.
