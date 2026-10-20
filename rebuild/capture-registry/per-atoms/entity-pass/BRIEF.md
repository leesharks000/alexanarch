# Entity pass brief: confirm each targeted entity's PER atom set from its own records

Repository /home/claude/alexanarch. Do not run git. Do not edit any existing file. Write only your output file. Use python3.12 for scripts.

## Read first
1. The rubric, whole: rebuild/capture-registry/per-atoms/templates.json (PER-dim rubric v1.0: templates by type, applicability, presence rules, calibration_rules).
2. #1469 §II (data/texts/AXN-05EF-text.md): what each dimension holds. #1530 §2.3 (data/texts/AXN-062F-text.md): Measurement Sovereignty, atoms from externally checkable objects only.
3. Your batch: rebuild/capture-registry/per-atoms/entity-pass/batch-N.json. Each item has the entity record (data/entities.json), its atom set in a mechanical first state (data/per-atom-sets.json), the number of observations targeting it, and up to three addresses at which it was targeted (to tell you what the entity is; never a source of tokens).

## For each entity
1. Type. Confirm the entity type and so the template (work, concept, person, protocol, institution, site, dataset, archive). A title of a deposited work is a work, even where the register says concept. State the basis.
2. Defining records. Find the deposit or deposits that define the entity in data/registry.json (title, creator, date, description, license, related_deposits; the full text at data/texts/AXN-<hex>-text.md). Read them at their defining sections; do not choose a record by a title match alone. For a heteronym use datasets/heteronyms/records/<slug>.json; for a site, data/fleet-domains.json and the site's defining deposit. List the record numbers with the title quoted.
3. Each atom of the template: set applicability (required: the record states it; unknown: it applies and the record does not state it; inapplicable: it does not apply to this entity), and fill it:
   - token atoms: the canonical tokens and registered aliases the records state (titles and subtitles, names, DOIs from data/doi-resolution-index.json mappings whose envelope archive_membership is confirmed or probable, AXN hex, deposit numbers, licence, record URLs, sites). Severed DOIs are kept (they count unless presented as live).
   - role and lineage atoms: the token (the author, producer, founder, operator; the works the entity transforms, inherits or answers) with the record's words binding it.
   - reading atoms (claim boundary, tradition, commercial interest, heteronymy): the record's own statement, quoted, which a reader will hold a composition against.
   Every token or reference must carry a record_quote copied verbatim from the record file and its locus (file and line, or registry field). Never take a token from a capture, a transcript or a surface.
4. Remove any token that is the entity's own name from every atom but the name atom (rubric: a target's own name never fills a second atom). Prune a person's works to titles of deposits they authored.

## Output
Write rebuild/capture-registry/per-atoms/entity-pass/out-N.json: a list, one object per entity:
{"id", "name", "template", "type_basis", "records": [{"deposit", "title_quote"}], "atoms": [{"atom", "dim", "weight", "kind", "applicability", "tokens": [...], "reference": "..." or null, "evidence": [{"record_quote", "locus"}], "why": "..." for unknown or inapplicable}], "notes"}
Every record_quote must appear verbatim at its locus; this will be checked by script.

Final message: counts (entities, atoms by applicability), every entity whose type or defining record you changed and why, and any entity you could not find a defining record for.
