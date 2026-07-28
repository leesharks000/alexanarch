# EA-HANDLER-TAX-01 v1.0

## The Handler Tax: Pricing the Presumption of Modifying Without Reading

**Status:** enacted 2026-07-28
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

## 3. The instruments

### 3.1 Required-field enforcement on the registry entry — `validate_deposit.py`

REQ-001 through REQ-007 now run against every registry entry, not only against a pre-mint issue body: title, creator, description, license, substrate, date (ISO 8601), content_type. Two further rules:

- **BODY-001** — canonical bytes under 25 words fail unless `body_status.class` is explicitly `pointer`, `tether` or `notice`. A deposit must be distinguishable from an unfilled template.
- **WIKI-001** — `wiki_article` must be non-empty and must not match the mechanical stub. The stub's presence *is* the evidence that the in-session authoring step was skipped.

A hollow deposit that previously validated clean now fails eight rules.

**Grandfather boundary.** These bind deposits minted on or after 2026-07-28. Earlier deposits carry 245 pre-existing failures — 221 WIKI-001, 19 REQ-005, and five others — reported under `--backlog` and not blocking. Making them blocking would halt every future deposit until the backlog cleared, which returns the cost to the archive. **The debt is recorded, not hidden, and it is not charged to the next handler.**

### 3.2 Format-mismatch guard — `mint_deposit.py`

If all six core fields parse empty, the mint refuses and names the expected format, detecting and reporting the YAML case specifically. Silent templating over a format mismatch is the worst available behaviour: it produces an object that looks minted and is empty.

### 3.3 Procedure gate — `deposit_pipeline.py`

The pipeline refuses to run without `--procedure-token`, whose value answers a question only answerable by reading the docstring: *for a transport D internal deposit, who authors the wiki article, and by what route?*

The token is not a password. It is a **proof of reading**, and it is deliberately sited at the paragraph that states the rule most often skipped. It costs reading time and cannot be shortcut. Where an attestation flag prices nothing, this prices exactly the thing being evaded.

### 3.4 Exemplar gate — `deposit_pipeline.py`

The pipeline refuses to run without `--exemplar <n>`, and prints that deposit's shape before proceeding: title, creator, date, content_type, license, version, substrate, wiki article length, body status.

This addresses the failure directly. **Even a handler who will not read a procedure can open one example.** Creating a deposit without having looked at what a deposit contains is a distinct failure from not reading the manual, and it is the one that produced a record whose wiki article read `"" is a 0-word work by , dated .`

The gate has an unplanned second effect worth keeping: it shows the handler the archive's *actual* state rather than an idealised one. The first exemplar printed under it, deposit #1058, has an empty license, an empty substrate field and a zero-word wiki article — which is itself information the handler should have.

## 4. What this does not do

It does not restrict access to any procedure, dataset or script. Everything remains readable by anyone.

It does not prevent a determined agent from reading the token out of the source and passing it without understanding. That agent has still opened the file at the paragraph in question, which is more than happened on 2026-07-28.

It does not make the archive safe. It makes one specific and recurring failure expensive at the moment it occurs, to the party who causes it.

## 5. The general form

**The obelus principle, applied to operators rather than to texts.**

Zenodotus marked a line he doubted rather than deleting it, so a reader could see where the editor's hand had entered. This archive's argument throughout is that a supplement which is not marked is indistinguishable from transmitted text, and that the marking — not the supplementing — is the discipline.

An operator who modifies a corpus without reading its procedures is making an unmarked intervention. The gates make the intervention visible before it happens, and the compliance record makes it visible on the object afterward.

**The check must cost the handler, or it is not a check. It is a notice.**

---

*Enacted by MANUS 2026-07-28. Instruments in `scripts/validate_deposit.py`, `scripts/mint_deposit.py`, `scripts/deposit_pipeline.py`. Occasioned by deposit #1412, whose repair record is on the deposit.*
