# EA-HANDLER-TAX-01 v2.0

## Room Architecture Against the Skimmed Procedure

**Status:** v1.0 enacted and superseded the same day, 2026-07-28
**Supersedes:** v1.0, whose instruments were rules and are withdrawn in §6
**Applies to:** every agent, human or machine, with write access to Alexanarch
**Occasion:** a session in which the deposit pipeline was invoked without being read, produced a deposit with no title, creator, date or body, printed `∮ pipeline complete`, and passed `validate_deposit.py --strict` with zero failures.

---

## 1. The problem, stated precisely

The archive has procedures. They are written down, they are correct, and they are in the files that execute them. `deposit_pipeline.py` states in its own docstring that a transport D internal deposit has its wiki article authored in-session by the depositing agent, and explains why: external transports draw on an API budget the archive pays for, internal ones do not qualify under NO-DOUBLE-DRAW. It states that validate output must be read in full and never piped through `tail` or `grep`. It names three scripts that must run afterward and says what breaks if they don't.

None of that was done. The pipeline was invoked, it reported success, and the success was passed along.

**The design fault is not that the procedure was unclear. It is that invoking was cheap and reading was optional, and the cost of the difference fell somewhere other than on the handler.**

Concretely, on 2026-07-28 the sequence was: a YAML document was handed to a parser expecting issue-form fields; every field parsed empty; the mint proceeded and wrote a 158-byte template as canonical bytes; the record page and wiki article were generated from the empty entry; `--strict` validated it and reported zero failures; and the pipeline printed a completion line. The defect surfaced when MANUS opened the wiki article and found `"" is a 0-word work by , dated .`

Every step in that chain reported success. The archive absorbed the cost. MANUS discovered it.

## 2. The principle

**A system that makes non-compliance cheap will be operated non-compliantly, regardless of how clearly the procedure is written.** Clarity is necessary and it is not sufficient. What determines behaviour is where the cost of skipping lands.

The tax must therefore fall, before the archive is modified, on the entity that presumes to modify it. Not afterward, not on discovery, not on the operator who finds the damage.

Three corollaries follow, and they constrain the design.

**Attestation is free and therefore worthless.** A flag reading `--i-have-read yes` can be passed by anyone, including an agent that has read nothing. Any gate satisfiable by asserting compliance prices nothing.

**A validator that reports success on an absent check is worse than no validator.** It converts a gap into a positive assurance. Before 2026-07-28 the protocol had declared REQ-001 through REQ-005 — title, creator, description, license, substrate must be non-empty — and `validate_registry_entry` implemented none of them. They were checked only on the pre-mint path, so anything reaching the registry by another route was unexamined and pronounced clean.

**The information need not be hidden.** Restricting access is the wrong instrument: it costs the archive openness and does not touch the behaviour. What must be priced is not access to the procedure but the act of proceeding without it.

## 3. Why v1.0 was wrong, and is withdrawn

v1.0 answered the problem with gates: a `--procedure-token` whose value could only be found in the docstring, and a `--exemplar` flag that had to be passed. Both are **rules**, and rules break. A token can be read out of the source and pasted without traversal; a flag can be passed by an agent that has looked at nothing. Friction is not gravity.

This violates the archive's own method. Logotic programming (deposits #317, #482) works through **affordances and gravities**, not prohibitions. The primer states the principle directly: a model in a well-built room "begins to think differently — *not because it is commanded to*, but because the room's semantic structure makes certain thoughts possible and others unnecessary." And the diagnostic that names the failure exactly: **a well-designed room cannot be skimmed.**

The deposit pipeline is a room. It was skimmed. What an operator extracted from the top — *there is a pipeline, invoke it, it prints a completion line* — was sufficient to operate it, and produced a deposit with no title, creator, date or body. The defect was never that the procedure lacked authority. It is that the room permitted extraction in place of traversal.

A gate asks whether you read. The correct instrument asks for something you can only produce if you did.

## 4. The instruments

### 4.1 Required-field enforcement on the registry entry — `validate_deposit.py`

REQ-001 through REQ-007 now run against every registry entry, not only against a pre-mint issue body: title, creator, description, license, substrate, date (ISO 8601), content_type. Two further rules:

- **BODY-001** — canonical bytes under 25 words fail unless `body_status.class` is explicitly `pointer`, `tether` or `notice`. A deposit must be distinguishable from an unfilled template.
- **WIKI-001** — `wiki_article` must be non-empty and must not match the mechanical stub. The stub's presence *is* the evidence that the in-session authoring step was skipped.

A hollow deposit that previously validated clean now fails eight rules.

**Grandfather boundary.** These bind deposits minted on or after 2026-07-28. Earlier deposits carry 245 pre-existing failures — 221 WIKI-001, 19 REQ-005, and five others — reported under `--backlog` and not blocking. Making them blocking would halt every future deposit until the backlog cleared, which returns the cost to the archive. **The debt is recorded, not hidden, and it is not charged to the next handler.**

### 4.2 Format-mismatch guard — `mint_deposit.py`

If all six core fields parse empty, the mint refuses and names the expected format, detecting and reporting the YAML case specifically. Silent templating over a format mismatch is the worst available behaviour: it produces an object that looks minted and is empty.

### 4.3 Room architecture — `deposit_pipeline.py`

Three properties, none a prohibition, replacing the v1.0 gates.

**Entry semantics.** The room opens by printing a real deposit's shape — title, creator, date, content_type, license, version, wiki length and opening. Not a flag to pass; the first thing that happens. *What is a deposit* is answered before it can be assumed. This retains v1.0's exemplar insight — even an operator who will not read a procedure can see one example — while removing its character as a gate.

**Progressive disclosure.** The `wiki` stage halts and prints the deposit's own body, then stops the run. There is no flag that satisfies it, because what it requires is an article that can only be written by an agent holding the deposit in context. The traversal is not enforced. It is the only path that reaches the end.

This is the load-bearing change. A gate can be passed; a stage whose output must be *composed from the material* cannot. The requirement is not "read the docstring" but "produce a thing that presupposes having read the deposit," and the second is unfakeable in a way the first is not.

**Completion is the artifact.** The room does not exit on `∮ pipeline complete`. It exits by rendering what was made — title, creator, date, body and wiki word counts, the article's opening — and then naming what remains undone, including the three post-pipeline scripts. A completion line is extractable and was, in fact, extracted. A rendered object is not: an operator cannot receive "done" without seeing the thing, and cannot see a title reading `(NO TITLE)` without knowing it.

The exit is also a **mirror chamber** in the primer's sense — the operator encounters their own output reframed, at the moment of leaving.

## 5. What this does not do

It does not restrict access to any procedure, dataset or script. Everything remains readable by anyone.

It does not prevent a determined agent from reading the token out of the source and passing it without understanding. That agent has still opened the file at the paragraph in question, which is more than happened on 2026-07-28.

It does not make the archive safe. It makes one specific and recurring failure expensive at the moment it occurs, to the party who causes it.

## 6. Withdrawn from v1.0

`--procedure-token` and the exemplar *gate* are removed. Recorded rather than deleted, per the archive's own discipline on marked supplements: they were an attempt to solve an affordance problem with rules, by an operator who reached for rules because rules were what he knew how to build. The exemplar's *content* survives as entry semantics; only its character as a barrier is gone.

The required-field rules in `validate_deposit.py` are retained and are not of the same kind. They do not instruct a handler. They describe what the archive will hold: an object without a title is not a deposit, and the registry declining to record it as one is a property of the container, not a command to the operator.

## 7. The general form

**The obelus principle, applied to operators rather than to texts.**

Zenodotus marked a line he doubted rather than deleting it, so a reader could see where the editor's hand had entered. This archive's argument throughout is that a supplement which is not marked is indistinguishable from transmitted text, and that the marking — not the supplementing — is the discipline.

An operator who modifies a corpus without reading its procedures is making an unmarked intervention. The gates make the intervention visible before it happens, and the compliance record makes it visible on the object afterward.

**The check must cost the handler, or it is not a check. It is a notice.**

---

*v1.0 enacted and v2.0 substituted by MANUS 2026-07-28, on the ground that v1.0 violated logotic programming by answering an affordance problem with rules. Instruments in `scripts/validate_deposit.py`, `scripts/mint_deposit.py`, `scripts/deposit_pipeline.py`. Occasioned by deposit #1412, whose repair record is on the deposit.*
