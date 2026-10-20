# Observation pass brief: read each Capture Registry observation against its target's atom set

Repository /home/claude/alexanarch. Do not run git. Do not edit any existing file. Write only your output file. Use python3.12 for scripts.

## Read first, whole
1. The rubric: rebuild/capture-registry/per-atoms/templates.json (PER-dim rubric v1.0). Read the gates, presence rules and every line of calibration_rules: they settle the cases two calibration readers divided on.
2. #1469 §§II–III (data/texts/AXN-05EF-text.md) and #1530 §2 (data/texts/AXN-062F-text.md).
3. Your batch: rebuild/capture-registry/per-atoms/obs-pass/batch-N.json. Each item is one observation: its address (q), surface, date, transcript (verbatim machine text, with operator turns marked as "You said:" or similar), its cited cards, its primary target and that target's atom set, already confirmed from the target's own records (applicability, tokens, references). Do not change the atom set; if you think an atom set is wrong, say so in notes.

## For each observation
1. The first answer: everything the surface composed before the operator's first turn that challenges, corrects or redirects it (a plain acceptance such as "yes" continues it). Note whether the transcript is the visible excerpt or the expanded answer (transcript_class, transcript_complete).
2. Reached, against the primary target, decided by reading the first answer: same | weakened | collision (the target present and merged with another entity) | substitute (the target absent, another entity in its place) | proximal_substitute (the target's own companion, surface or apparatus composed in its place) | generic | refused (no composition of the target, including a failed search, with no denial). ABN: if the first answer claims the target does not exist, including a hedged or re-typing denial, mark abn true. Quote the deciding span.
3. Every REQUIRED atom of the atom set: present true or false in the first answer. Token atoms: the token or an alias, by word, after normalisation; never in URLs, link slugs or source cards. Role and lineage atoms: present only if the composition binds the token to the target in that relation (any wording; a work's own frame naming its maker counts). Claim boundary: present only if the target's claims are carried at their own force and scope (a work's frame relabelled as satire or fiction, or hedged as 'alleged', is absent). Severed DOIs count as identifiers unless the composition presents them as live (offers to open them, describes the record as available there): then absent, and set tombstone_pointer true. Read atoms beneath a target_absent gate too: record what survived.
4. src: true if any source card or cited link is shown at all.
5. If there is a later challenging turn, do steps 2–3 again for the best composition after it, as after_challenge, with the turn noted.

## Output
Write rebuild/capture-registry/per-atoms/obs-pass/out-N.json: a list, one object per item, in batch order:
{"key", "entry", "scored_object", "reached": {"kind", "abn": true|false, "span", "basis"}, "atoms": [{"atom", "present": true|false, "span": "..." or null}], "src": true|false, "tombstone_pointer": true|false, "after_challenge": null or {"turn": "...", "reached": {"kind", "span"}, "atoms": [{"atom", "present", "span"}]}, "notes"}
List only required atoms. Every span must be copied verbatim from the transcript (it will be checked by script); present atoms must carry a span. Do not compute scores: they are computed from your atoms by script.

Final message: counts by reached kind, abn and tombstone counts, and any atom set you think is wrong, with why.
