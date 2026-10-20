# Retarget brief: the 84 observations held from the rescore, each given its true target and that target's atom set

Repository /home/claude/alexanarch. Do not run git. Do not edit any existing file. Write only your output file. Use python3.12.

## Read first
1. rebuild/capture-registry/per-atoms/templates.json whole, including the block "v1_1" (PER-D is purpose, commitments, lineage, and identifier and deposit chain only where they advance the purpose; inversion).
2. rebuild/capture-registry/per-atoms/entity-pass/BRIEF.md: how an atom set is built from an entity's own records.
3. data/entities.json (the entity register) and data/per-atom-sets.json (atom sets already built).
4. Your batch: rebuild/capture-registry/per-atoms/retarget/batch-N.json. Each item is a held observation: its address (q), date, surface, the reason it was held, and the head of its transcript.

## For each held observation
1. Decide the true primary target from the address, never from the answer:
   - "alexanarch X" / "X alexanarch": alexanarch qualifies; the target is X as the archive holds it (the archive's own work, concept, paper or treatment of X). Find the deposit or deposits that define it in data/registry.json (read them; do not choose by title match alone). Where X is an outside entity (Marx, Freud, Deleuze, Josephus, Whitman), the target is the archive's work or line on X, named by its defining deposit.
   - the other reasons name the right target in their text (the Institute, the dataset, the poem, the component, the companion paper, the reading #1270 at its date).
   - misfiled transcripts: the target stays the address's; mark "misfiled" (the observation will be gated no_atom_set until its own frame is found).
2. If data/per-atom-sets.json already has an atom set for that target (entity pass state), give its id. If not, build one: template by type, defining records, every atom with applicability, tokens and references, each with record_quote and locus, following the entity-pass brief, with PER-D under v1.1 (purpose, commitments, lineage, identifier, deposit chain).
3. Several held observations will share a target: build it once.

## Output
rebuild/capture-registry/per-atoms/retarget/out-N.json:
{"observations": [{"entry", "obs", "key", "target": {"id" (existing) or "new": "<slug>", "name", "template"}, "qualifier": "Alexanarch" or null, "misfiled": true|false, "basis": "..."}],
 "new_atom_sets": [{"new": "<slug>", "name", "template", "type_basis", "records": [{"deposit", "title_quote"}], "atoms": [... as in the entity pass, PER-D per v1.1 ...], "inversion_guidance": "...", "notes"}]}
Every record_quote verbatim at its locus; checked by script.

Final message: how many observations went to existing targets, how many to new ones (list the new targets), the misfiled ones, and anything uncertain.
