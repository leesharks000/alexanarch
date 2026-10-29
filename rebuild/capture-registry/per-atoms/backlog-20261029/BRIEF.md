# Backlog brief (PER-dim rubric v1.1): the 57 observations seated without a dimensional PER, 2026-10-20 to 2026-10-29

Repository /home/claude/alexanarch. Do not run git. Do not edit any existing file. Write only your output file, rebuild/capture-registry/per-atoms/backlog-20261029/out-G.json (G is your batch letter). Use python3.12, and keep any helper scripts in a scratchpad folder of your own named for your batch (never inside the repository).

The operator ruled on 2026-10-29 that the backlog be scored. Each of these observations entered the Capture Registry with only the historical scalar PER. This pass builds the atom sets their targets lack and reads every observation in full, as the held-observation pass of 2026-10-20 did.

## Read first, whole
1. rebuild/capture-registry/per-atoms/templates.json whole, including calibration_rules and the block v1_1 (with its rulings, calibration_rules_d, inversion and standing_substitution).
2. rebuild/capture-registry/per-atoms/entity-pass/BRIEF.md and entity-pass-d/BRIEF.md: how an atom set is built from an entity's own records (PER-M, PER-C, and PER-D under v1.1: purpose 3, commitments 2, lineage 2, identifier 1, deposit chain 1).
3. rebuild/capture-registry/per-atoms/obs-pass/BRIEF.md (first answer, reached, ABN, PER-M and PER-C atoms, src, tombstone pointers, after_challenge) and obs-pass-d/BRIEF.md (PER-D atoms, inversions, standing substitutions).
4. rebuild/capture-registry/per-atoms/obs-pass-d/HELD-BRIEF.md: this pass follows it, with the substitutions below.
5. Two atom sets in data/per-atom-sets.json as exemplars of shape: "The future reader" (ENT-f4549d6ae1) and "SPXI" (ENT-6681f64c9e).
6. Your batch: rebuild/capture-registry/per-atoms/backlog-20261029/batch-G.json. Each item is one observation: key, entry (the registry slug), obs_index, q (the address, quotation marks and operators included), date, surface, transcript (verbatim machine text; operator turns are marked), cite_list (the card rail), and target.

## Targets
- target.id: the atom set already exists in data/per-atom-sets.json. Read the observation against it as it stands; if you think it is wrong for the address, say so in notes.
- target.new with a hint (archive entities): build the atom set from the entity's defining records in data/registry.json and data/texts/AXN-<hex>-text.md, as the entity-pass brief says. Read the deposits; do not choose by title match alone. Never build from a capture or a surface's rendering. If the archive holds no defining record for the target, build no set: give the observation "target_id": null and say why in notes (it will be gated no_atom_set).
- target.new with "external": true: an entity outside the archive. Its records are, in this order:
  (a) its census record: target.census.path, rows[slug == target.census.slug]: its fields (name, aka, url, operator, kind, lineage, capability, lifecycle, version_and_time, data_access, and the rest) and its evidence list ({src, basis, quote}).
  (b) its /non field ledger: target.field_ledger, the field claims F1..Fn, each a verbatim quote from a saved source, with source id and locus; the saved sources are in target.sources_dir (Bn.txt beside Bn.html), and field.json records each source's url and origin (card, own_page, wikipedia, census_third_party).
  The entity's own pages (origin own_page) and its Wikipedia article (origin wikipedia) state its name, operator, dates, mandate, purpose and commitments; cards are admitted as the field's account. Prefer own_page, then wikipedia, then census. Do not read the /non row's delta, kernel or composition, or the Capture Registry's reading, findings or analysis for these entries: the reading of T is yours.
  Template by the entity's own kind (database or repository: dataset; standard, specification or program: protocol; organisation or initiative: institution; benchmark: dataset; tool or service: protocol unless its record makes it a site; a wiki: site). Give the choice in type_basis with a quote. The template's corpus atom names the Crimson Hexagonal Archive, which an external entity does not belong to: mark it inapplicable, "why": "external entity: the template's corpus is the Crimson Hexagonal Archive". Every other atom is instantiated from the entity's records at its own terms: author/founder/producer = the operator the records name; framework or institution = the programme, host or parent the records place it in; claim boundary = what it holds or does, at its own force and scope (stated limits included); purpose and commitments from its own statements (licence and terms of use read as commitments, as v1_1 says); lineage = its stated predecessors, model or source; identifier and deposit chain = its identifiers and versions where the records state them, with the reason where stated.
  Applicability as in the entity pass: required (a record states it), unknown (it applies and no record states it), inapplicable.
- Several observations share a target: build it once.

## Loci and quotes
Every record_quote is verbatim at its locus, checked by script. Loci: "data/texts/AXN-XXXX-text.md:L<n>", "data/registry.json #<N> field <field>", "<path>:L<n>" for a saved .txt source, or "<census path>#rows[slug=<slug>].<field>" / "<field_ledger>#<claim id>" for JSON, where the quote must occur in a string value at that path. Every transcript span verbatim from the item's transcript.

## Reading each observation
As HELD-BRIEF.md: decide the first answer, reached (against the target; same, weakened, substitute, proximal_substitute, generic, refused, as the v1.0 brief defines them), abn, every required atom of all three dimensions present or absent with its deciding span, inversions {atom, span, against}, standing_substitutions {proxy, span, displaced, internal}, src, tombstone_pointer, after_challenge. Read beneath a target_absent gate as well. Do not compute scores.

The WikiWho observation is the known case of an answer about another entity (wikiHow): read it against WikiWho as the address's target and record what it composed in reached and notes.

## Output
out-G.json: {"new_atom_sets": [{"new": "<slug>", "name", "template", "type_basis", "external": true|false, "records": [{"deposit", "title_quote"}] or [{"source", "path", "origin"}], "atoms": [...], "inversion_guidance", "notes"}],
 "observations": [{"key", "entry", "obs_index", "target_id" (an existing id, "NEW:<slug>", or null), "scored_object", "reached": {"kind", "abn", "span", "basis"}, "atoms": [{"atom", "present", "span"}], "inversions": [...], "standing_substitutions": [...], "src", "tombstone_pointer", "after_challenge", "notes"}]}
Observations in batch order. Before finishing, run your own script over the file: every record_quote at its locus, every span in its transcript, every required atom listed per observation, and no atom both present and used in an inversion. Report its result.

Final message: the atom sets built (with template and the atoms marked unknown or inapplicable), counts by reached kind, abn, tombstones, inversions and standing substitutions (with proxies), the self-check result, and anything uncertain.
