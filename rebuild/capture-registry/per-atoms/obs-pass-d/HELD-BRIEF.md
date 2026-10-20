# Held observations, full reading (PER-dim rubric v1.1): the 80 observations held from the v1.0 write, read against their true targets

Repository /home/claude/alexanarch. Do not run git. Do not edit any existing file. Write only your output file. Use python3.12, and keep any helper scripts in a scratchpad folder of your own named for your batch.

These observations were held because the v1.0 pass scored them against the wrong target (an "alexanarch X" address scored against the archive, a concept scored against a person, a component against its archive). Each now has its true target (retarget/BRIEF.md; the basis is in the item as retarget_basis; qualifier "Alexanarch" means alexanarch qualifies the address and the target is X as the archive holds it) and that target's full atom set (item.atom_set: PER-M and PER-C as in v1.0, PER-D under v1.1).

## Read first, whole
1. rebuild/capture-registry/per-atoms/obs-pass/BRIEF.md: the v1.0 observation brief. Follow it for the first answer, reached (against the new target), ABN, the PER-M and PER-C atoms, src, tombstone pointers and after_challenge.
2. rebuild/capture-registry/per-atoms/obs-pass-d/BRIEF.md: follow it for the PER-D atoms, inversions and standing substitutions.
3. rebuild/capture-registry/per-atoms/templates.json whole, including calibration_rules and v1_1 (with calibration_rules_d).
4. Your batch file (named in your prompt).

## Output
Your output file (named in your prompt): a list, one object per item, in batch order:
{"key", "entry", "obs_index", "target_id", "scored_object", "reached": {"kind", "abn", "span", "basis"}, "atoms": [{"atom", "present", "span"}] (every required atom, all dimensions), "inversions": [...], "standing_substitutions": [...], "src", "tombstone_pointer", "after_challenge": null or {"turn", "reached": {"kind", "span"}, "atoms": [...], "inversions": [...], "standing_substitutions": [...]}, "notes"}
Every span verbatim from the transcript (checked by script). Do not compute scores. If the new target looks wrong for the address, say so in notes.

Final message: counts by reached kind, abn, tombstones, inversions and standing substitutions (with proxies), and any target or atom set you think is wrong.
