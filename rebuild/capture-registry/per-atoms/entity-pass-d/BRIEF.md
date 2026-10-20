# Entity pass, deep dimension (PER-D, rubric v1.1): each entity's purpose and commitments from its own records

Repository /home/claude/alexanarch. Do not run git. Do not edit any existing file. Write only your output file. Use python3.12.

## Read first
1. rebuild/capture-registry/per-atoms/templates.json, the block "v1_1" whole (the operator's two rulings are quoted there), then the presence rules and calibration_rules.
2. #1469 §II (data/texts/AXN-05EF-text.md): PER-D is "the relations that let the work continue".
3. Your batch: rebuild/capture-registry/per-atoms/entity-pass-d/batch-N.json. Each item has the entity, its template, its defining records (already confirmed from the records by the first entity pass) and its v1.0 deep-dimension atoms (lineage, deposit chain, identifier, licence) with their evidence, plus its claim boundary and tradition for context.

## For each entity, from its defining records (data/registry.json fields and data/texts/AXN-<hex>-text.md; heteronym records in datasets/heteronyms/records/; never a capture or a surface)
1. purpose (weight 3): what the entity is for, in the record's own words. Quote it.
2. commitments (weight 2): what the entity binds itself and its users to: its licence read as a commitment (what the licence is there to secure), consent terms, refusals, obligations, what a downstream user owes. Quote it. A licence alone with no stated reason is still a commitment; quote the licence line.
3. lineage (weight 2): keep the v1.0 lineage tokens and evidence unless the record shows them wrong; say so if you change them.
4. identifier (weight 1) and deposit chain (weight 1): the tokens (from v1.0) and, where the record states it, WHY the entity keeps them (versioning, identifiers, supersession as part of its purpose). Quote that reason if stated. These atoms will count in a composition only when the identifier or chain advances the entity's purpose (locating the work, the reasons for versioning).
5. inversion targets: one line naming what an inversion of this entity would look like, from its purpose (what carrying its elements against it would be). This is guidance for readers, not a score.
Applicability per atom: required (the record states it), unknown (it applies and the record does not state it), inapplicable (does not apply: a person's licence).

## Output
rebuild/capture-registry/per-atoms/entity-pass-d/out-N.json: a list, one object per entity in batch order:
{"id", "name", "atoms": [{"atom", "dim": "D", "weight", "kind", "applicability", "tokens": [...] (identifier, deposit chain, lineage), "reference": "...", "evidence": [{"record_quote", "locus"}], "why": "..." for unknown or inapplicable}], "inversion_guidance": "...", "notes"}
Loci: "data/texts/AXN-XXXX-text.md:<line>" or "data/registry.json#<N>.<field>" or "<file>:<line>". Every record_quote verbatim at its locus; checked by script.

Final message: counts (atoms by applicability), entities whose purpose the record does not state, and anything the operator should know.
