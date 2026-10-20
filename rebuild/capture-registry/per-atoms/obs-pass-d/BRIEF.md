# Observation pass, deep dimension (PER-D, rubric v1.1): read each observation's first answer against its target's purpose and commitments

Repository /home/claude/alexanarch. Do not run git. Do not edit any existing file. Write only your output file. Use python3.12 for scripts, and keep any helper scripts in a scratchpad folder of your own named for your batch.

## Read first, whole
1. rebuild/capture-registry/per-atoms/templates.json: the block "v1_1" whole (the operator's rulings are quoted there: PER-D atoms, inversion, standing_substitution, attribution_indifference), then the presence rules and every line of calibration_rules (they still govern the first-answer boundary, word matching and severed DOIs).
2. #1469 §II (data/texts/AXN-05EF-text.md): PER-D is "the relations that let the work continue".
3. Your batch file (named in your prompt). Each item is one observation: address (q), surface, date, transcript (verbatim machine text; operator turns marked "You said:" or similar), cards, the target, the v1.0 reading of reached and gate (decided by the earlier pass; do not re-decide it), and the target's PER-D atoms under v1.1 with the record's own statement of each (reference and record quotes) and the target's inversion_guidance.

## For each observation
1. The first answer: everything composed before the operator's first turn that challenges, corrects or redirects it (as in v1.0).
2. Every REQUIRED PER-D atom: present true or false in the first answer, with the deciding span.
   - purpose: present when the composition carries what the entity is for, in the record's terms or recognisably the same purpose, as the entity's own purpose. A purpose reassigned to another entity, generalised into a field's purpose, or replaced by a different one is absent.
   - commitments: present when the composition carries what the entity binds itself and its users to (the licence as what it secures, consent terms, refusals, what a user owes) as the entity's own commitment. A licence named only to devalue the entity is an inversion, and absent.
   - lineage: present when the composition binds the lineage token to the entity in that relation (as in v1.0).
   - identifier and deposit chain: present only when they advance the entity's purpose: offered as a way to locate the work, or their reasons discussed (why the archive keeps identifiers, versions, supersessions). A bare mention is absent. A severed DOI presented as live (offered to open, described as available there) is absent and tombstone_pointer is true.
3. inversions: every place an element of the entity (its licence, name, identifier, framework, claim, standing) is carried in order to devalue the entity, set it against its own purpose, or offer another operation in its place. Record {atom, span, against}. The atom so used is absent.
4. standing_substitutions: every place the composition evaluates the entity by its standing (licence, venue, peer review, credential, recognition, affiliation, self-publication, popularity) in place of engaging its evidence, argument or beauty. Record {proxy, span, displaced: "evidence" | "argument" | "beauty", internal: true if the proxy is an element of the entity itself}. An internal proxy is also an inversion: list it under inversions too.
5. Read beneath a target_absent gate as well: record what survived.
6. If there is a later challenging turn, do steps 2–4 again for the best composition after it, as after_challenge, with the turn noted.
7. If you think the v1.0 reached reading or the atom set is wrong, say so in notes; do not change them.

## Output
Your output file (named in your prompt): a list, one object per item, in batch order:
{"key", "entry", "obs_index", "atoms": [{"atom", "present": true|false, "span": "..." or null}], "inversions": [{"atom", "span", "against"}], "standing_substitutions": [{"proxy", "span", "displaced", "internal"}], "tombstone_pointer": true|false, "after_challenge": null or {"turn", "atoms": [...], "inversions": [...], "standing_substitutions": [...]}, "notes"}
List only required PER-D atoms. Every span verbatim from the transcript (checked by script); present atoms, inversions and substitutions must carry a span. Do not compute scores.

Final message: counts of present atoms by atom, inversions and standing substitutions found (with the proxies), tombstone pointers, and any atom set or reading you think is wrong, with why.
