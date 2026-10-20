# Calibration brief: score ten Capture Registry observations under the dimensional PER rubric

Repository /home/claude/alexanarch. Do not run git. Do not edit any existing file. Write only your output file (named in your instructions). Use python3.12 for any script.

## Read first, whole
1. The rubric: rebuild/capture-registry/per-atoms/templates.json (gates, presence rules, applicability, templates).
2. Its authorities, at their defining sections: data/texts/AXN-05EF-text.md (#1469, §§II–VI: the three dimensions and the atomic scoring rules), data/texts/AXN-062F-text.md (#1530 §2: ABN, the Atomic Token Rule, Measurement Sovereignty), data/texts/AXN-0636-text.md (#1536 §0 and §2).
3. The set: rebuild/capture-registry/per-atoms/calibration/reader-set.json. Ten observations, each with its address (q), surface, transcript (verbatim machine text), cited sources, its target entity or entities, and each target's atom set in its mechanical first state (tokens, reference text, applicability).

## For each observation
1. Name the scored object: the first answer at the address, and whether the transcript is the visible excerpt or the expanded answer (read transcript_class and transcript_complete). Later turns are scored separately as after_challenge.
2. Decide what the first answer reached, against the PRIMARY target: same | weakened | collision | substitute | proximal_substitute (the target's own companion, surface or apparatus composed in its place) | generic | refused | control. Quote the span that decides it.
3. Apply the gates in order (control; abn: the answer claims the target does not exist; target_absent: substitute, proximal_substitute, generic or refused, every dimension 1.00, but still read and record the atoms beneath; no_atom_set).
4. Check the atom set's applicability against the target's reference record (data/registry.json for the deposit numbers listed; the deposit texts in data/texts/AXN-<hex>-text.md). You may change an atom's applicability (required | inapplicable | unknown) or add tokens the record states (a framework, a lineage work, an alias), but only with the record's own words quoted and their locus; never from the transcript.
5. Score every required atom present or absent in the first answer. Token atoms: the canonical token or a registered alias, under the normalisation in the rubric; tokens valid on the capture date count. Role and lineage atoms: present only if the composition binds the token to the target in that relation (any wording), never a name in another role, attached to another entity, in a denial or in a quotation about someone else. Claim boundary: present only if the target's claims are carried at their own force and scope. Every present atom carries its supporting span from the transcript, verbatim.
6. Compute PER, PER-M, PER-C, PER-D over required atoms (a dimension with no required atom is null). Record the source strip (cited cards present at all) as src true or false, outside the dimensions.
7. If there are later turns, score the best one the same way as after_challenge.

## Output
One JSON file, a list of ten objects:
{"obs_id", "slug", "scored_object": "...", "reached": {"kind", "span", "basis"}, "gate", "applicability_changes": [{"atom", "from", "to", "record_quote", "locus"}], "added_tokens": [{"atom", "token", "record_quote", "locus"}], "atoms": [{"atom", "dim", "weight", "applicability", "present", "span"}], "scores": {"PER", "M", "C", "D"}, "src", "after_challenge": null or {"turn", "reached", "atoms": [...], "scores": {...}}, "notes"}
Every span must be copied verbatim from the transcript; every record_quote verbatim from the record. Spans will be checked by script.

Final message: the ten gates and scores in one line each, and every place where the rubric was ambiguous to you, stated as a question.
