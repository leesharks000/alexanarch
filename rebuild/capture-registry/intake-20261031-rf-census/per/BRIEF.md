# Intake brief (PER-dim rubric v1.1): the ten Revelation First census captures of 2026-10-31, scored at intake

Repository /home/claude/alexanarch. Do not run git. Do not edit any existing file. Write only your output file, rebuild/capture-registry/intake-20261031-rf-census/per/out-G.json (G is your batch name, R1 or R2). Use python3.12; keep helper scripts in a scratchpad folder of your own named for your batch, outside the repository. Fetch nothing.

Dimensional PER is standard at intake (operator, 2026-10-29). These ten captures are being seated now: the entities of the Revelation First meta-aggregator, "the field" (revelationfirst.com/aggregators/, census compiled 2026-10-30, editor Lee Sharks), each run by its common name on Google AI Overview, signed out and incognito, by the operator and received 2026-10-31 00:04 EDT.

## Follow, whole
rebuild/capture-registry/per-atoms/backlog-20261029/BRIEF.md, read with every file it says to read first, and its external-entity rules, with these substitutions:
1. **The records.** Each target is an external entity whose records are its Revelation First census record: target.census.path, rows[slug == target.census.slug], its fields and its evidence (each a {src, basis, quote} or the census's own quote shape; read the file), and the saved sources the census quotes from (target.sources_dir, <slug>--<id>.txt, with sources/manifest.json for url, http and sha256). There is no /non field ledger. A census field that restates an evidence quote is that quote's source; quote the source text itself at its locus ("<sources_dir><slug>--<id>.txt:L<n>"), or the census field at "<census path>#rows[slug=<slug>].<field>" where the field is the record's reading. The census row's rf_intersection and the census's organizing_question and correction are the aggregator's framing, not the entity's records: do not build atoms from them.
2. **Template** by the entity's own kind, as the backlog brief says; corpus inapplicable ("external entity: the template's corpus is the Crimson Hexagonal Archive").
3. **The transcript** is the item's transcript: the paste of the Overview expanded, from the first line of the answer to the end of its card rail. Spans are verbatim from it. The first answer is the whole composition (one querent turn; no challenge).
4. **Addresses that compose another sense, or a wider one.** Read each against its census target and decide reached by the rubric (same, weakened, substitute, proximal_substitute, generic, collision, as its definitions say), with the deciding span; record beneath the gate what of the target survives. Known cases:
   - "Bodmer Lab" (R1): the composition sets out three entities of that name, the Geneva digital library first, then a cardiovascular laboratory and a teaching laboratory, and asks which was meant.
   - "Early Christian Writings" (R1): the composition is about a Penguin Classics book, "Early Christian Writings: The Apostolic Fathers"; the census target is the website earlychristianwritings.com. This paste alone has no 'AI Mode Conversation' header and no 'You said' line; its query is its first line.
   - "Oxyrhynchus Papyri" (R1): the address names the collection; the census record is the collection's site (Oxford's POxy pages). Decide whether the composition of the collection reaches the record.
   - "AI and Faith" (R2): the composition is of the topic at large, with the organisation AI and Faith as one bullet and its home page as the first card.
   - "Ithaca DeepMind", "Aeneas DeepMind", "Enoch AI dating Dead Sea Scrolls" (R2): the operator added the disambiguators; the bare names are homonyms.
5. **Pending or thin records.** Where the census row says "not stated in the saved pages" (e.g. Early Christian Writings' operator), the atom is unknown, not absent; a composition that supplies it is read against nothing the records state, and you say so in notes.

## Output
out-G.json in the backlog brief's shape: {"new_atom_sets": [...], "observations": [...]}, with "new" = the target's "new" value (e.g. "rf-csntm") and "target_id" = "NEW:<that value>". Observations in batch order. Run your own check before finishing (every record quote at its locus, every span in its transcript, every required atom listed, none both present and inverted) and report it.

Final message: the atom sets built (template; atoms unknown or inapplicable), reached for each capture with its span, inversions and standing substitutions, the self-check result, and anything uncertain.
