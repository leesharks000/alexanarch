# Brief: recompose one /non entry under EA-NEGONT-02 v0.9 (#1690)

Repository: /home/claude/alexanarch (read-only for you except your one output file). Do not run git, do not run build scripts, do not edit rows, ledgers, pages or any other file. Write exactly one file: rebuild/negative-of-the-negative/v09/<ROW>.json.

## Read first, whole
1. The specification, v0.9: data/texts/AXN-0700-text.md. Read §0 (especially §0.7–0.10), §1.2a, §3.3–3.6, §4 entire (4.1–4.11), §5 (5.0–5.10), and Appendix A (model collapse, the equal-terms exemplar) and Appendix C (Theophrastus, the witness exemplar).
2. Two v0.8 rows as worked exemplars of the output: datasets/negative-of-the-negative/v2/rows/theophrastus.json (witness case; objects.KO, objects.P, ontology with E_A/E_F/rho/translation) and datasets/negative-of-the-negative/v2/rows/spxi.json (ρ = revises).
3. Your row: datasets/negative-of-the-negative/v2/rows/<ROW>.json — its v0.7 objects KO, P (compression), KO_B (field-only), P_B, field_claims, field_sources, delta, kernel. The v0.7 KO is what §0.7 measured as failing (field-only run first, archive as a block, "the entity evolves"); do not reproduce its shape.
4. The ledgers named in row.ledger: field.json (field claims F1..Fn, verbatim quotes with source and locus) and ledger-archive.json (archive claims with id, dep, locus, quote, modality, lineage, kernel/const flags). These are the ONLY claim sources you may cite. You never read the transcript T (§4: "The composer reads the ledger, never the transcript").
5. The defining papers: the archive deposits that define the archive's entity for this row (most frequent kernel/const deps in the archive ledger, and any the row's kernel names). Read each defining paper's text WHOLE at data/texts/AXN-<HEX>-text.md (hex from data/registry.json by deposit_number). The blog and crimsonhexagonal room pages are archive records too, but cite only ledger claim ids in the composition.

## Decide the case (v0.9 §0.9–0.10, §1.2a), from the defining papers
- equal: the archive's account EXTENDS the field's ontology (adds senses, mechanisms, limits on the field's own object) → ρ = extends; one claim space; no precedence; nothing translated.
- witness: the archive radically contests the field's ontology and supplies an ontology NO other source in the field makes available → archive's ontology rules (the law of the suppressed witness); field carried whole and translated (ρ = constructs or another value you read and justify).
- A mixed row (archive extends on some senses and supplies an otherwise unavailable ontology on another): say so; record it under "case": "mixed", and compose in one claim space where the archive's witness claims rule their own senses (see §10.16). Justify with loci.
Record the reading with verbatim loci from the defining papers (quote exactly; I will check each quote against the text file).

## Compose (v0.9 §4)
- KO (knowledge object, the expansion): numbered sentences, each with "para" (0-based paragraph index), "text", "claims" (ledger ids it states; every sentence carries ids; a sentence must be entailed by the claims it cites — reverse entailment is audited). Archive's genre for the entity. Typically 14–24 sentences.
  - equal case: the field's and the archive's claims ordered together by dependency and genealogy within each sense. The KO must NOT open with the field-only composition's sentences in their order (§5.10); do not copy KO_B sentences. Archive definitions are definitions (§4.2), not provisos; no "on a reading proposed against the received one", no "the entity evolves", no cushions (§0.7).
  - witness case: as Theophrastus: E_A's definition first, field claims standing where their translations place them.
  - Both: attribution in the sentence (§4.5: the source named in the sentence that states the claim — for the archive, the deposit by number, e.g. "(#1656)", or its author/heteronym as the ledger records); force is the source's own (§4.4 N_c): carry the archive's stated modality, falsifiers and limits; evidence may lower force, standing may not; opaque material quoted not paraphrased (O_leg); every sense present in the ledgers appears (C_ex).
- P (the compression, AIO's interaction grammar, composed from the same plan): "lede" {text, claims} (the text continues after the entity's name, as in the exemplars: "is ..."); "sections": [{icon, head, items:[{label, text, claims}]}]; body ≤ 350 words (lede + items). An "open" list outside the bound: each item {question, rests_on:[ids], modality, would_resolve}.
- translation: list of rows {field_claims:[F..], received:"verbatim quote(s)", receiving_text:"…" (witness: located receiving text; equal: "—"), translation:"…" (equal: "untranslated: composed as received beside <archive ids>"), archive_claims:[ids]}. EVERY field claim F1..Fn must appear in exactly one row (§4.3, D_pres: no field claim dropped).
- E_F {type, definition, claims}; E_A {definition, claims, defining_papers:[deposit numbers]}; rho {value, statement, claims, guard}; case {value: equal|witness|mixed, statement, loci:[{dep, locus, quote}]}.
- rail_order: the v0.7 P.rail lineage names (exact strings from row.objects.P.rail[*].lineage) in the order the plan gives; include every one exactly once.
- cuts: any claims cut for length, with ids (logged, §4.6); kernel claims are never cut.

## Output: rebuild/negative-of-the-negative/v09/<ROW>.json
{"row": "<ROW>", "composed": "2026-10-18", "composer": "<your one-line label>",
 "case": {...}, "E_F": {...}, "E_A": {...}, "rho": {...},
 "KO": {"title": "...", "sentences": [{"n":1,"para":0,"text":"...","claims":["F1","H1656-01"]}, ...]},
 "P": {"title": "...", "lede": {...}, "sections": [...], "open": [...]},
 "translation": [...], "rail_order": [...], "cuts": [...],
 "defining_papers_read": [{"dep": N, "file": "data/texts/AXN-XXXX-text.md", "read": "whole"}],
 "notes": "anything the operator should know: misfit between ledger and defining papers, ledger defects (report, do not fix), a case you could not decide"}
Validate before finishing: JSON parses; every cited id exists in the field or archive ledger; every field claim is in the translation; P body ≤ 350 words; KO sentence 1 is not a KO_B sentence. Report in your final message: the case and ρ with one line of why, KO sentence count, P body word count, and any notes.
