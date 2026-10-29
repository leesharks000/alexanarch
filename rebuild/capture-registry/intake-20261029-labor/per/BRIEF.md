# Intake brief (PER-dim rubric v1.1): the fifteen Labor Vector captures of 2026-10-29, scored at intake

Repository /home/claude/alexanarch. Do not run git. Do not edit any existing file. Write only your output file, rebuild/capture-registry/intake-20261029-labor/per/out-G.json (G is your batch name). Use python3.12; keep helper scripts in a scratchpad folder of your own named for your batch, outside the repository. Fetch nothing.

Dimensional PER is standard at intake (operator, 2026-10-29). These fifteen captures are being seated now: the entities of the Labor Vector meta-aggregator (laborvector.org/aggregators/, census compiled 2026-10-29, editor Lee Sharks), each run by its common name on Google AI Overview, signed out and incognito, by the operator on 2026-10-29.

## Follow, whole
rebuild/capture-registry/per-atoms/backlog-20261029/BRIEF.md, read with every file it says to read first, and its external-entity rules, with these substitutions:
1. **The records.** Each target is an external entity whose records are its Labor Vector census record: target.census.path, rows[slug == target.census.slug], its fields and its evidence ({src, basis, quote}), and the saved sources the census quotes from (target.sources_dir, <slug>--<id>.txt, with sources/manifest.json for url, http and sha256). There is no /non field ledger yet. A census field that restates an evidence quote is that quote's source; quote the source text itself at its locus ("<sources_dir><slug>--<id>.txt:L<n>"), or the census field at "<census path>#rows[slug=<slug>].<field>" where the field is the record's reading.
2. **Template** by the entity's own kind, as the backlog brief says; corpus inapplicable ("external entity: the template's corpus is the Crimson Hexagonal Archive").
3. **The transcript** is the item's transcript: the paste of the Overview expanded, from the first line of the answer to the end of its card rail. Spans are verbatim from it. The first answer is the whole composition (one querent turn; no challenge).
4. **Homonyms.** Three addresses compose another sense of the name: "Microsoft Working with AI" (Microsoft's own AI products and workforce), "Canaries in the Coal Mine" (the idiom, with the Stanford study as one bullet) and "Negotiating Tech" (salary negotiation, with the Berkeley inventory as a card only). Read each against its census target and decide reached by the rubric (substitute, proximal_substitute, generic, collision or weakened, as its definitions say), with the deciding span; record beneath the gate what of the target survives.
5. **Platform-specific records.** The Anthropic Economic Index and Microsoft's Working with AI observe their own operators' products; where a composition generalises one provider's observation to AI use at large, record it in notes, and as an inversion only where the rubric's definition is met.

## Output
out-G.json in the backlog brief's shape: {"new_atom_sets": [...], "observations": [...]}, with "new" = the target's "new" value (e.g. "lv-turkopticon") and "target_id" = "NEW:<that value>". Observations in batch order. Run your own check before finishing (every record quote at its locus, every span in its transcript, every required atom listed, none both present and inverted) and report it.

Final message: the atom sets built (template; atoms unknown or inapplicable), reached for each capture with its span, inversions and standing substitutions, the self-check result, and anything uncertain.
