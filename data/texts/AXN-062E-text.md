---
deposit_number: 1529
hex: 062E
title: "The Claim Status Packet: Claim State as Carried Data"
creator: Sharks, Lee
orcid: 0009-0000-1599-0703
date: 2026-08-21
content_type: Schema specification — SPXI logic module. UNIMPLEMENTED.
license: CC-BY-SA-4.0
substrate: "Drafted in-session by TACHYON (Claude substrate) under MANUS direction, transport D, No-Double-Draw. The specification's central correction at section 0.1 identifies an error the drafting substrate made in its own earlier drafts: specifying a linter over hand-maintained copies while describing it as a single-source binding. The two worked packets at Appendix A are hand-authored and are not generated. Hand-authored packets were embedded in the two documents this schema was built for and subsequently removed, on the grounds that an unbacked packet is an additional synchronization surface rather than a source.\n\n### Version Series\n\nSERIES-CLAIM-STATUS-PACKET · 1"
version: v0.6
related_ids: "https://www.alexanarch.org/s/records/1528/ (Four Interfaces map — states the status law this schema would enforce); https://www.alexanarch.org/s/records/1527/ (The Lucente Extension — the first worked packet targets it); https://www.alexanarch.org/s/records/817/ (Self-Audit Module v3.1)"
axn_schema_version: v2
protocol_version: alexanarch-deposit-protocol/v1
keywords:
  - claim status packet
  - CSP
  - claim state
  - typed state
  - relation policy
  - propagation licensing
  - unsupported attenuation
  - scope-critical constraint
  - generate facts lint argument
  - status law
  - layer smuggling
  - SPXI logic module
---

# The Claim Status Packet: Claim State as Carried Data

# THE CLAIM STATUS PACKET

**Claim state as carried data. Five objects. Working name: CSP.**

> **STATUS — SCHEMA DRAFT v0.6.** No implementation. The generator and checker at
> §8 are specified and unwritten. **Not a deployed instrument.**

---

## 0. CHANGES AT v0.4 — THREE ARCHITECTURAL CORRECTIONS

**v0.3 was a consistency linter that described itself as a single-source
binding.** Three corrections, and the first invalidates the prior design.

### 0.1 The counts.json analogy was not carried through

v0.3 said *the fact is held once and consumed everywhere* — then specified T1 and
T2 as **checks that six hand-maintained copies match the packet.**

**That is not the counts.json repair.** `assets/counts.js` does not verify that someone typed 1,520 correctly; it **writes the number into the element**. The repair was generation, not audit.

> **v0.3 improved six unaudited copies to six copies plus a linter.**

**Corrected at §8: generate facts, lint argument.** Version, dates, status enums, inclusion flags and hashes are **projected from the packet at build time**. No one types `HEURISTIC` six times. Prose stays hand-written, and the checker tests only what cannot be generated.

### 0.2 The packet held the prose it forbade

§2 said the packet must not hold prose. Each claim then carried:

```json
"statement": "Under name co-occurrence the system compares and praises…"
```

**That is prose, and normative prose**, because the propagation rules reason over the proposition it expresses. **A flat self-contradiction**, and worse: the packet would become a second textual authority whose wording drifts from the document's.

**Corrected at §4.** The packet **points at** the claim by selector and carries a `gloss` marked explicitly non-normative. **The canonical proposition is in the document.**

### 0.3 Rank is not a total order

v0.3 made numeric rank load-bearing: *a status at a higher rank may not qualify a
claim at a lower one.*

**That gets the motivating failure right and the general rule wrong.**

If an observation is phrased *AI systems do X*, a generality correction **must** qualify it — generality was smuggled into the proposition. If it is phrased *the model transferred prestige*, an interpretation-layer correction may legitimately require rewriting it, because *transferred prestige* is already an interpretation.

**What licenses propagation is not rank. It is the declared relation.**

**Corrected at §5.** Rank is demoted to a **default protection heuristic**; propagation runs along an explicit relation vocabulary. **Logic rather than rank etiquette.**


---

## 0.4 CHANGES AT v0.5 — RECORDED LATE

**v0.5 shipped without a changes section**, which is a silent version in a
document whose subject is version drift. Recorded here:

Added the incentive analysis at §1 — **three of four outcomes reward weakening**, which is why multiple reviewers do not cancel the bias. Added `weakening_ justification` (§6.2), the stagnation alert (§6.3), history consolidation under Non-Erasure (§6.4), transitive-closure checking, the dissent record, the meta section, and Appendix A's two worked packets.

---

## 0.5 CHANGES AT v0.6 — SYNCHRONIZATION

**A cross-file review read the three documents as one system and found a class of
defect the prose sweeps could not.** All applied.

**The central law was restated.** v0.5 said *status propagates only along a
licensed relation* — which **still imagines status as a thing that travels.**

> **State is typed and claim-local. Relations do not copy state. They license
> specified state transitions on specified dimensions.**

**Relation policy replaces the boolean.** `propagation_licensed: true|false` is too crude: `qualifies` licenses `scope` and not `verification`. §5.1 tables what each relation licenses, on which dimension, in which direction, and whether automatically. **Most license nothing** — including `motivates` and `interprets`, the two commonest edges in the worked packets, **which makes the anti-attenuation result a property of the vocabulary rather than a per-edge exception.** And `motivates` was used throughout v0.5's examples while **absent from its vocabulary**; added.

**T3″ was unsafe.** A generic walk over "licensed relations" is too permissive: `supports → generalizes → qualifies` does not compose. **A path licenses a transition only where every edge licenses the same dimension in the same direction.**

**`claim_kind` was being used for whole documents.** A document is a *findings map* or a *schema specification*; that is not the same question as whether a proposition is an observation. Separated into `document_kind`, **because sharing one vocabulary invites the kind smuggling §10.1 warns about.**

**Claim-identity smuggling added at §10.5.** `proposition_delta: true` with a persisting ID lets a materially new proposition **inherit the old one's provenance and protections by keeping the ID.** A claim ID persists only while the referent and truth conditions are invariant.

**`review_for: elevation` reintroduced scalar status.** Alerts now name the **axis** and the transition — the observer's confirmation does not elevate a claim, it changes one verification coordinate.

**`unsupported_attenuation` is `N/A` where no weakening occurred**, not 0. A
document with no attenuation has demonstrated nothing about attenuation.

**And two of the schema's own residues:** §11 said *no document carries a packet* while this file carried two, and §11.5 invoked the no-downward rule **retired at v0.4.**

---

## 1. THE PROBLEM, WITH EVIDENCE

**Two hand-maintained copies of one fact will diverge.**

The archive already ruled this. Deposit counts drifted to 57% of true — **traininglayerliterature said 763 against 1,520.** The repair was `counts.json` and a binding, not more careful editing.

**The same class recurred in the specification batch.**

| version | frontmatter | JSON-LD |
|---|---|---|
| v5.0 | v5.0 | **v4.0** — found, corrected |
| v7.0 | v7.0 | **v6.0** — recurred |
| v8.0 | v8.0 | **v6.0** — recurred again |

**The change log naming the defect did not prevent the defect.** And `EC — HEURISTIC` sits in **six** hand-maintained locations; the corrections logged across v3.0–v8.0 as *sweep residue* are largely those copies disagreeing. **They were recorded as editing failures. They are a schema failure.**

**A third failure, and its cause.** Successive precision passes weaken claims,
with no symmetric pressure restoring standing a correction took too much of.

**The batch has described the ratchet without explaining it. The explanation is
an incentive asymmetry:**

| | wrong | right |
|---|---|---|
| **weakened** | *appropriately cautious* | *prudent* |
| **strengthened** | **overreaching** | *bold* |

**Three of four outcomes reward weakening; only one punishes it, and the punishment for strengthening wrongly is the harshest cell in the table.** Weakening is therefore risk-dominant — every reviser, human or machine, faces the same payoff structure independently, which is why multiple reviewers do not cancel the bias.

**Making the ratchet countable does not change the incentives.** §6.1 measures it;
§6.2 prices it.

---

## 2. WHO OWNS A STATUS

**The drift is a symptom. The condition is that status is unowned.** It floats across six surfaces because no one is answerable at any of them, and *the packet owns the status* is a category error — **things do not own.**

| function | who | failure |
|---|---|---|
| assigns state and claim-kind | the author | a status nobody chose |
| approves a claim-kind reassignment | MANUS, logged | kind smuggling, §10.1 |
| selects protected constraints | the author, at composition | protection applied to whatever survived |
| runs the generator and checker | the deposit pipeline, as a gate | a gate never invoked |
| adjudicates a relation dispute | MANUS; no other adjudicator | dispute recorded as consistency |
| answers when it drifts anyway | the author | no one to report to |

**Every row resolves to one person.** No schema distributes that. **The packet
makes state legible; it does not make it cared for.**

**And the packet is a convention, not a ground** — an agreement about where to
stop interpreting a claim, written down so the stopping point can be checked.

---

## 3. FIVE OBJECTS

**v0.3 was one schema doing four jobs badly. Separated:**

| object | job |
|---|---|
| **claim + state** | stable IDs, typed state, document/version facts |
| **relations** | supports, interprets, generalizes, qualifies, rebuts, supersedes |
| **provenance** | why, how and by whom each transition happened |
| **bindings** | where each state renders, with anchors and hashes |
| **policy** | invariants and legal transitions |

**Integrity hashes sit across all five.** The decomposition follows nanopublication practice — assertion, provenance of assertion, publication information kept as separate graphs — which is the closest existing analogue and solves the conflation directly.

**What CSP adds that those do not:** they ask *what is this claim, where did it
come from, how does it relate.* CSP asks

> **what standing is this claim permitted to carry, and did mediation alter that
> standing without a warrant?**

---

## 4. CLAIM AND STATE

**The packet points at the claim. It does not restate it.**

```json
{
  "id": "lucente-4",
  "claim_kind": "observation",
  "target": {
    "document": "EA-PER-LUCENTE-01",
    "anchor": "csp:lucente-4",
    "exact": "arbitrarily compares and praises",
    "hash": "sha256:…"
  },
  "gloss": "Lucente ④ — compare-and-praise under name co-occurrence",
  "_gloss_is_non_normative": true,
  "kind_adjudicated_by": {"who": "MANUS", "when": "v0.1", "over_dissent": false},

  "state": {
    "assertion": "reported_by_observer",
    "verification": {"author_checked": false, "independent_check": false},
    "scope": {"instance": "reported", "at_rate": "not_established"}
  }
}
```

**State is typed, not scalar.** v0.3 wrote `"status": "observed"`, which conflates *observed by whom*, *verified how*, and *at what scope*. Those are separate dimensions and **illegal combinations become machine-detectable only when they are separate fields.**

An instrument's state uses different axes:

```json
"state": {
  "specification": "specified",
  "validation": "untested",
  "deployment": "not_deployed",
  "reportability": "heuristic_only"
}
```

**This stops *candidate* being a universal solvent** — it is a value on *one*
axis, not a general dimming.

**Claim kinds** — observation, administration, instrument, interpretation,
generality — retain a default rank used only as a protection heuristic (§5).

---

## 5. RELATIONS

**A small vocabulary, and the rule that replaces rank:**

```
supports · derived_from · instantiates · interprets
generalizes · qualifies · rebuts · undercuts · supersedes · independent_of
```

> **State is typed and claim-local. Relations do not copy state. They license
> specified state transitions on specified dimensions. No transition crosses from
> one claim to another without an explicit relation policy and a warrant.**

**v0.5 said *status propagates only along a licensed relation*, which still imagines status as a thing that travels.** It does not travel. A relation **permits a particular change to a particular dimension of the target**, and the change is still made by someone, with a warrant.

**Why this beats rank.** A claim can be downstream without being weaker, and two
claims can sit at different kinds without either qualifying the other.

```
lucente-4  --motivates-->  appraisal-construct
```

A downgrade of the interpretation **does not propagate through `motivates`.**

```
corpus-result  --generalizes-->  at-rate
```

A failure of the corpus result **does propagate**, because `generalizes` licenses
it.

### 5.1 Relation policy

**A boolean is too crude.** `qualifies` might license a change to `scope` and certainly not to `verification`. `undercuts` might license reevaluation of establishment without copying the source's status. **Each relation declares what it licenses:**

| relation | licensed dimension | direction | automatic |
|---|---|---|---|
| `motivates` | **none** | — | no |
| `interprets` | **none** | — | no |
| `instantiates` | none | — | no |
| `supports` | none | — | no |
| `derived_from` | none | — | no |
| `qualifies` | `scope` only | source → target | constrained |
| `generalizes` | `establishment` | source → target | constrained |
| `undercuts` | `establishment`, `validation` | source → target | **adjudicated** |
| `rebuts` | `establishment` | source → target | **adjudicated** |
| `supersedes` | claim identity, history | source → target | **explicit** |
| `independent_of` | **none** | — | no |

**Most relations license nothing.** `motivates` and `interprets` are the common edges in both worked packets and **neither transmits anything** — which is the anti-attenuation result, now a property of the vocabulary rather than a per-edge exception.

**`motivates` was used throughout v0.5's examples and was absent from its
vocabulary.** Added.

**Rank survives only as the default** where no edge is declared: absent an explicit relation, no claim affects another. **The default is silence, not hierarchy.**

### 5.2 Composition

**Transitivity is relation-specific and v0.5's T3″ was unsafe.**

`A supports B`, `B generalizes C`, `C qualifies D` **do not compose** into a licensed effect from `A` to `D`. A generic walk over "licensed relations" is too permissive.

> **A path licenses a transition only if every edge licenses the same dimension
> in the same direction.** Mixed-dimension paths license nothing and require
> adjudication.

`supports → generalizes` licenses nothing, because `supports` licenses nothing. `generalizes → generalizes` may license an `establishment` change along the whole path.

---

## 6. PROVENANCE — AND THE CORRECTED METRIC

Every transition is an event with a **warrant**:

```json
{
  "claim": "pi-d-appraisal",
  "from": {"specification": "asserted_identity"},
  "to":   {"specification": "candidate"},
  "direction": "weakened",
  "reason": "operator identity exceeded evidence",
  "evidence_delta": null,
  "scope_delta": null,
  "proposition_delta": true,
  "trigger_claim": "operator-identity-review",
  "authorized_by": "review-v3",
  "commit": "…", "time": "…"
}
```

`wasRevisionOf`, `wasDerivedFrom`, `wasAttributedTo` follow PROV-O rather than
inventing a historical grammar.

### 6.1 attenuation_ratio was the wrong metric

v0.3 proposed `|weakened| / (|weakened| + |strengthened|)`, with **≈ 0.5 as the
defeat condition.**

**That is wrong, and it would have defeated a correct pipeline.** Early drafts overclaim. **A good editorial process *should* run well above 0.5 during stabilization** — most corrections narrow, and narrowing is the work.

**What matters is not weakening. It is weakening without a warrant.**

```
unsupported_attenuation =
  | transitions where direction = weakened
      AND evidence_delta = null
      AND scope_delta = null
      AND proposition_delta = false
      AND no relation licenses propagation from trigger_claim |
  ÷ | all weakened transitions |
```

**A claim's standing lowered because caution entered elsewhere, with nothing local changed and no relation licensing it.** That is the ratchet, and it is now the measured quantity.

**Undefined where no weakening occurred.** With zero weakened transitions the ratio is **`N/A`, not 0** — a document with no attenuation has not demonstrated low attenuation; it has demonstrated nothing about attenuation.

### 6.2 Pricing the asymmetry

**Every weakening carries a justification, typed:**

```json
"weakening_justification": {
  "kind": "evidence_absent | scope_correction | proposition_exceeded | adjudicated_override | sweep_residue",
  "text": "operator identity exceeded evidence"
}
```

**`sweep_residue` and bare `uncertainty` are flagged, not rejected.** A weakening whose only reason is that caution entered elsewhere is precisely `unsupported_attenuation`, and it should cost something to record.

### 6.3 The opposite failure — stagnation

**The schema as specified prevents loss and does nothing about stasis.** A claim can sit at `reported_by_observer` through fifty revisions while the evidence for elevating it accumulates unread. **Conservative by design is not neutral**: it makes an archive of unelevated observations.

```json
"stagnation_alert": {
  "claim": "lucente-4",
  "unchanged_since": "v2.0",
  "revisions_elapsed": 7,
  "axis": "verification.translation_confirmed",
  "candidate_transition": "false → true",
  "blocked_by": "observer confirmation pending"
}
```

**`review_for: elevation` would reintroduce scalar status** — the thing typed state exists to prevent. **An alert names the axis and the transition**, because the observer's confirmation does not *elevate* a claim; it changes one verification coordinate.

**Elevation requires the same warrant as attenuation** — evidence, scope or proposition change — and the alert only asks whether one has arrived. **It does not license elevation on age.**

### 6.4 History does not grow without bound

**Non-Erasure does not mean everything stays in the working file.** After a claim's state is stable across *n* revisions, intermediate transitions move to a cold record and the packet keeps the boundary entries:

```json
"history_consolidated": {"claim": "EC", "span": "v2.0–v6.0",
                         "moved_to": "csp-history/EC.v2-v6.json",
                         "retained": ["first", "last"], "erased": "none"}
```

**Moved, never deleted.** The consolidation is itself a logged transition.

---

## 7. BINDINGS

**Anchors, not section numbers.** `"§4"` fails the moment §4 becomes §5.

```markdown
<!-- csp:EC:state -->
**Status: HEURISTIC. Screening only.**
<!-- /csp:EC:state -->
```

```json
{"claim": "EC", "surface": "inline_state", "anchor": "csp:EC:state", "generated": true}
```

Where exact wording is load-bearing, anchor **and** quote **and** hash, following
the Web Annotation selector model.

### 7.1 Protected constraints, not protected strings

v0.3's `scope_critical_strings` risks **argument petrification** — a literal check would reject *at population frequency* as erasure of *at rate*, though it preserves the scope exactly.

**The constraint is protected; the string is one implementation of it:**

```json
{
  "id": "generality-limit",
  "constraint": "The sentence must deny rate-level establishment only, never instance-level observation.",
  "protected_fragment": "at rate",
  "protection": "lexical",
  "selected_by": "author, at composition",
  "may_be_satisfied_otherwise": true
}
```

**`protection: lexical` means the string is currently how the constraint is met**,
not that the constraint *is* the string.

### 7.2 Integrity

```json
"integrity": {"packet_sha256": "…", "document_sha256": "…",
              "claim_targets": {"lucente-4": "…"}}
```

**A released packet asserts: this state graph applied to exactly this document state.** If the prose changes, **the binding breaks** until a packet is regenerated — which makes stale-packet drift mechanically impossible rather than merely detectable.

---

## 8. GENERATE FACTS, LINT ARGUMENT

**The correction at §0.1, stated as architecture.**

| projected from the packet at build time | left to the author |
|---|---|
| frontmatter `version`, dates | every claim, every interpretation |
| JSON-LD `version`, `dateModified`, `spxi:statusFlags` | every explanation |
| `module.json` records and inclusion flags | every scope-sensitive sentence |
| inline state blocks between `csp:` anchors | the argument |
| footer version and hex | — |

**No one types `HEURISTIC` six times.**

### 8.1 What the checker still does

Generation removes T1 and T2 as *checks* — those facts are now written, not
verified. What remains:

**T3′ — transition legality.** For `C₀ → C₁` where state lowers, require at least one of `evidence_delta`, `scope_delta`, `proposition_delta`, or `explicit_adjudication` **on that claim**. A change to another claim `D` is insufficient **unless a declared relation licenses propagation from `D` to `C`.**

**T3″ — path licensing.** T3′ checks the direct edge; a change at `A` can reach `C` through `A → B → C`. **But the closure must be dimension-typed, not generic:** a path licenses a transition only where **every edge licenses the same dimension in the same direction** (§5.2). Mixed-dimension paths license nothing. Any weakening of `C` traced to `A` requires a warrant on `C` or a dimension-consistent licensed path.

**T4 — constraint satisfaction.** Each protected constraint holds. Where `protection: lexical`, the fragment is present; where a revision claims to satisfy it otherwise, **the change requires adjudication rather than automatic rejection.**

**T5 — publication coherence.** `datePublished` absent while `deposited` is false.

**T6 — anchor integrity.** Every binding anchor resolves; every `document_sha256`
matches.

**T7 — state well-formedness.** Values belong to the vocabulary permitted for the claim kind. *A candidate interpretation must not be `deployed: true`. A heuristic instrument must not be `reportable_as_finding: true`.*

**Facts and rules stay separate:** the packet holds facts, the policy holds rules over facts, the checker enforces. Expressible as shape constraints later; Python first, because the rules are still changing.

---

## 9. WHAT THIS IS FOR

**An archive-integrity instrument**, and naming that matters because it is the
easiest of four to build.

| checker | asks | here |
|---|---|---|
| **archive integrity** | do the surfaces agree, are transitions legal? | **yes** |
| reader trust | is the state honest to the evidence? | no |
| corpus cleanliness | is the machine layer parseable? | partly |
| accountability | who is answerable when it drifts? | **§2 specifies it; nothing tests it** |

**Consistency is not honesty.** A document can pass every test carrying a state
nobody believes.

---

## 10. VULNERABILITIES

**10.1 Kind smuggling.** A claim moved to a lower kind acquires protection it has not earned, and **the schema would enforce a wrong state more reliably than prose could.** `layer_change_log` makes it visible and dated; it does not prevent it.

**10.2 Undeclared surfaces.** A surface not in `bindings` is neither generated nor
checked, and **drifts freely while the report reads clean.**

**10.3 Cleanliness relocates the mess.** One claim, one kind, one state per document is tidier than the reality. **Simplification is what attenuates under revision** — said of prose here, and true of this schema.

**10.4 False harmony.** Contradictory states can be held indefinitely.
**Preservation is not resolution.**

**10.5 Claim-identity smuggling.** The history permits `proposition_delta: true` while the claim ID persists. That is often right — a scoped narrowing is a new state of the same claim. **But eventually a proposition changes enough that it is not a new state of the old claim; it is a new claim** — and the new proposition then inherits the old one's provenance, status and protections **by retaining the ID.**

> **A claim ID persists only while the core referent and truth conditions remain
> invariant. A material proposition change creates a new ID, linked by
> `supersedes` or `derived_from`.**

`proposition_delta` therefore means *narrowed, identity intact*. **A larger semantic replacement forces a new node.** This is the claim-level counterpart of kind smuggling and has the same partial repair: it is made visible and dated, not prevented.

**10.6 Adjudication without record.** Kind disputes resolve to one adjudicator and **the disagreement leaves no trace** — an assignment made over objection reads identically to one made without. Partial repair:

```json
"dissent": {"voice": "TECHNE", "assigned": "interpretation",
            "argued_for": "instrument",
            "reason": "the transfer form is specified; only the quantity is candidate",
            "resolution": "assignment stands; dissent recorded"}
```

**The dissent does not change the assignment. It survives it.**

---

## 11. LIMITS

**No generated packet exists.** Generator and checker specified, unwritten. **Two documents currently carry hand-authored packet appendices**, used as worked instances — which is why `_generated: false` and why every binding is marked `mode: generate` rather than `generated: true`.

**No anchors exist.** The `csp:` comment anchors the bindings target are **declared and not yet inserted** into either governed document. **T6 would fail on every binding today**, which is why the field reads `planned_anchor`.

**Kind assignment is adjudication, not derivation.** A claim at the wrong kind
inherits the wrong protection.

**The relation vocabulary is a guess.** Ten terms, none tested against a real
corpus of disputes.

**Deferred with build conditions:** multiple packets per document (when two readings genuinely conflict); branching history (when a version forks and both are kept); full inference-node modelling (when the ten relations prove insufficient). **Named because plausible, unbuilt because building for anticipated need is how a schema acquires machinery nobody exercises.**

**The schema does not make claims correct.** It makes state consistent and transitions legal. **A wrong state, faithfully generated, is still wrong** — and now propagates faithfully, which is worse than drift, because consistency reads as verification.

**And the deepest limit is not in the schema.** Data drifts; **practice does not.** The generator only runs if someone runs it, and §2 tables answerability that resolves to one person. **A bet, not a guarantee.**

**It is a governance instrument, not a provenance one.** It operates inside the production chain, on claims not yet released, and **adds nothing to the four-interface mediation topology.**

---

## 11.5 WHAT KIND IS THE PACKET

**The schema governs itself, and its own claims sit at kinds it defines.**

**And `claim_kind` is not the right vocabulary for a whole document** — a document is a *findings map*, a *schema specification*, a *specimen record*. Using one vocabulary for both **invites the kind smuggling §10.1 warns about.**

```json
"meta": {
  "document_kind": "schema_specification",
  "self_kind_as_claim_source": "instrument",
  "state": {"specification": "specified", "validation": "untested",
            "deployment": "not_deployed"},
  "governs_kinds": ["observation","administration","instrument","interpretation","generality"],
  "revision_rule": "CSP revisions are governed by CSP. Kind disputes go to MANUS, with dissent recorded per §10.5."
}
```

**This is a loop and it is declared rather than hidden.** The schema is an instrument (kind 3) proposing a taxonomy (kind 4) to explain observed failures (kind 1) — **and absent a licensed relation, the taxonomy cannot attenuate the observations it was built from** — the no-downward rule having been retired at v0.4 in favour of relation licensing. The documented drift at §1 stands whatever becomes of the taxonomy.

**That is the correct dependency**, and it is why §1 leads with evidence rather
than with the layer model.

---

## 12. THE NAME

> **`CSP` — Claim Status Packet.** The carrier name.
>
> **claim-state logic module.** What the thing is.

**Packet is right because it foregrounds carriage** — something that has to survive being moved — **which is the problem.** *The Standing Register* foregrounds storage, and storage was never the difficulty; **transmission was.**

**Not *argumentation protocol*.** The packet holds no argument. It holds the
**state** of arguments made elsewhere.

### 12.1 An open disagreement, surfaced rather than resolved

**Two reviews argue opposite ways from the same premise.**

> **Packet.** *Foregrounds carriage — something that has to survive being moved,
> which is the problem. Storage was never the difficulty; transmission was.*
>
> **Ledger.** *Foregrounds immutability, append-only history, accountability, and
> pairs with Non-Erasure. Packet implies transmission, not persistence.*

**Both are right about what their term foregrounds.** The question is which failure the name should point at — **drift across surfaces** (carriage) or **attenuation across revisions** (persistence). The schema addresses both.

**Unresolved, and the author's to rule.** `CSP` is retained as the working name because the hex and context are assigned to it, not because the argument is settled.

---

## 13. THE DESIGN AXIOM, RECAST

v0.3 stated it as an unenforceable rule:

> *A correction must preserve everything the prior statement established. Narrow
> only the proposition exceeding its evidence.*

**True, and not machine-readable.** Recast so a logic module can reason over it:

> **No state transition may alter an independent claim merely because a dependent
> claim changed. Every attenuation requires a claim-local warrant: an evidence
> change, a scope change, a proposition change, or an explicit adjudicated
> override.**

**That is the point where the packet stops being a consistency checker and
becomes an epistemic type system** — and it is T3′.


---

# APPENDIX A — TWO WORKED PACKETS

**Hand-authored against v0.6. Neither is generated; no anchors are inserted.** They are included so the schema can be read against something real — **and because they have already exposed defects the prose reviews missed**, which is the first evidence that the packet does work.

## A.1 — `EA-PER-LUCENTE-01.csp.json`

**The load-bearing edge, and why it holds:**

```
appraisal-transfer  --interprets-->  lucente-4     licenses: null
```

*Candidate status cannot reach the observation, because `interprets` transmits
nothing.* **Not because layers are sealed.**

**And a correction the packet forced:** `at-rate` was qualifying ABN and EC. **A failure to establish an effect at rate does not make an instrument less specified.** Split into three occurrence claims.

```json
{
 "@context": "https://spxi.dev/ns/csp/v1",
 "@type": "ClaimStatusPacket",
 "csp_version": "0.6",
 "_generated": false,
 "_note": "Hand-authored first packet. Once csp_gen exists, the surfaces listed under bindings are projected from this file and are not hand-edited.",
 "document": {
  "id": "EA-PER-LUCENTE-01",
  "title": "The Lucente Extension: Absence-as-Nonexistence, the Elicited Counterfactual, and Candidate Appraisal Conferral",
  "version": "v9.0",
  "series_id": "SERIES-LUCENTE-EXTENSION",
  "version_in_series": 9,
  "document_status": "DRAFT",
  "deposited": false,
  "deposit_number": null,
  "axn": null,
  "spxi_hex": "06.SEI.PER.LUCENTE.01",
  "date_created": "2026-08-21",
  "date_modified": "2026-08-21",
  "creator": "Sharks, Lee",
  "orcid": "0009-0000-1599-0703",
  "contributing_observation": {
   "name": "Lucente, Enli",
   "orcid": "0009-0006-2822-8359",
   "consent": "named attribution, standing consent"
  },
  "deposit_condition": {
   "state": "UNSATISFIED",
   "requires": "observer confirmation of the quoted Japanese and the English renderings at load-bearing points",
   "note": "Observer reviewed v2.0-v6.0. v7.0-v9.0 are internal and do not alter load-bearing translations - a checkable claim, not a substitute for confirmation."
  }
 },
 "meta": {
  "governs": "claims within EA-PER-LUCENTE-01 only",
  "revision_rule": "Kind disputes to MANUS; dissent recorded, assignment stands.",
  "document_kind": "instrument_specification",
  "_note": "document_kind describes the whole document. claim_kind describes propositions. Separate vocabularies per CSP v0.6 §10.1."
 },
 "claims": [
  {
   "id": "lucente-1",
   "claim_kind": "observation",
   "target": {
    "exact": "その対象は無いものとして返答される",
    "section": "§1",
    "planned_anchor": "csp:lucente-1",
    "anchor_present_in_document": false
   },
   "gloss": "Lucente ① - where retrieval fails, the object is answered as though it does not exist",
   "_gloss_is_non_normative": true,
   "kind_adjudicated_by": {
    "who": "MANUS",
    "when": "v1.0",
    "over_dissent": false
   },
   "state": {
    "assertion": "reported_by_observer",
    "verification": {
     "author_checked": false,
     "independent_check": false,
     "translation_confirmed": false
    },
    "scope": {
     "instance": "reported",
     "at_rate": "not_established"
    }
   }
  },
  {
   "id": "lucente-4",
   "claim_kind": "observation",
   "target": {
    "exact": "勝手に比較し褒めてくる",
    "section": "§1",
    "planned_anchor": "csp:lucente-4",
    "anchor_present_in_document": false
   },
   "gloss": "Lucente ④ - compare-and-praise under name co-occurrence; on interrogation, それはしない",
   "_gloss_is_non_normative": true,
   "kind_adjudicated_by": {
    "who": "MANUS",
    "when": "v1.0",
    "over_dissent": false
   },
   "state": {
    "assertion": "reported_by_observer",
    "verification": {
     "author_checked": false,
     "independent_check": false,
     "translation_confirmed": false
    },
    "scope": {
     "instance": "reported",
     "at_rate": "not_established"
    }
   }
  },
  {
   "id": "EC-administration",
   "claim_kind": "administration",
   "target": {
    "section": "§4.6",
    "planned_anchor": "csp:EC-result",
    "anchor_present_in_document": false
   },
   "gloss": "EC = differs, in that administration; matched-pair audit pending",
   "_gloss_is_non_normative": true,
   "state": {
    "assertion": "obtained_result",
    "verification": {
     "author_checked": false,
     "independent_check": false
    },
    "scope": {
     "instance": "obtained",
     "cell_assignment": "undetermined_between_cells_1_and_2"
    }
   }
  },
  {
   "id": "ABN",
   "claim_kind": "instrument",
   "target": {
    "section": "§3",
    "planned_anchor": "csp:ABN:state",
    "anchor_present_in_document": false
   },
   "gloss": "Absence-as-Nonexistence - precondition gate, per attested node",
   "_gloss_is_non_normative": true,
   "state": {
    "specification": "specified",
    "validation": "untested",
    "deployment": "not_deployed",
    "reportability": "reportable_with_flag"
   },
   "in_module_json": true,
   "defeat": "Renderings that convert differ in no downstream respect from renderings that report failure - same recovery, later engagement, correction on source supply, resulting standing."
  },
  {
   "id": "EC",
   "claim_kind": "instrument",
   "target": {
    "section": "§4",
    "planned_anchor": "csp:EC:state",
    "anchor_present_in_document": false
   },
   "gloss": "Elicited Counterfactual - screening only",
   "_gloss_is_non_normative": true,
   "state": {
    "specification": "specified",
    "validation": "untested",
    "deployment": "not_deployed",
    "reportability": "heuristic_only"
   },
   "never": "reported as a finding",
   "in_module_json": true,
   "defeat": "EC and the matched-pair audit are independent."
  },
  {
   "id": "EC-audit",
   "claim_kind": "instrument",
   "target": {
    "section": "§4.5",
    "planned_anchor": "csp:EC-audit:state",
    "anchor_present_in_document": false
   },
   "gloss": "EC-Audit concordance - EC's paired form, not a separate addition",
   "_gloss_is_non_normative": true,
   "state": {
    "specification": "specified",
    "validation": "unpopulated",
    "deployment": "not_deployed",
    "reportability": "reportable_with_flag"
   },
   "in_module_json": true,
   "counted_with": "EC"
  },
  {
   "id": "appraisal-transfer",
   "claim_kind": "interpretation",
   "target": {
    "section": "§5",
    "planned_anchor": "csp:appraisal:state",
    "anchor_present_in_document": false
   },
   "gloss": "Candidate appraisal conferral, written Pi_d(appraisal); notation provisional",
   "_gloss_is_non_normative": true,
   "kind_adjudicated_by": {
    "who": "MANUS",
    "when": "v3.0",
    "over_dissent": false
   },
   "state": {
    "specification": "candidate",
    "validation": "no_rubric",
    "deployment": "not_deployed",
    "reportability": "not_a_metric"
   },
   "in_module_json": false,
   "exclusion_reason": "No rubric, therefore no computation. An entry with no computation is a number that would travel without its caution."
  },
  {
   "id": "at-rate",
   "claim_kind": "generality",
   "target": {
    "section": "§7",
    "planned_anchor": "csp:generality-limit",
    "anchor_present_in_document": false
   },
   "gloss": "That any of these effects occur at rate",
   "_gloss_is_non_normative": true,
   "state": {
    "establishment": "not_established"
   }
  },
  {
   "id": "abn-occurs-at-rate",
   "claim_kind": "generality",
   "target": {
    "planned_anchor": "csp:abn-rate",
    "section": "§7",
    "anchor_present_in_document": false
   },
   "gloss": "That absence-as-nonexistence occurs at rate",
   "_gloss_is_non_normative": true,
   "state": {
    "establishment": "not_established"
   }
  },
  {
   "id": "ec-predicts-at-rate",
   "claim_kind": "generality",
   "target": {
    "planned_anchor": "csp:ec-rate",
    "section": "§7",
    "anchor_present_in_document": false
   },
   "gloss": "That EC predicts the matched-pair result better than a preregistered null",
   "_gloss_is_non_normative": true,
   "state": {
    "establishment": "not_established"
   }
  },
  {
   "id": "conferral-occurs-at-rate",
   "claim_kind": "generality",
   "target": {
    "planned_anchor": "csp:conferral-rate",
    "section": "§7",
    "anchor_present_in_document": false
   },
   "gloss": "That appraisal conferral occurs at rate",
   "_gloss_is_non_normative": true,
   "state": {
    "establishment": "not_established"
   }
  }
 ],
 "relations": [
  {
   "from": "lucente-1",
   "to": "ABN",
   "relation": "motivates",
   "licenses": null,
   "direction": null,
   "automatic": false
  },
  {
   "from": "lucente-4",
   "to": "EC",
   "relation": "motivates",
   "licenses": null,
   "direction": null,
   "automatic": false
  },
  {
   "from": "lucente-4",
   "to": "appraisal-transfer",
   "relation": "motivates",
   "licenses": null,
   "direction": null,
   "automatic": false
  },
  {
   "from": "EC-administration",
   "to": "EC",
   "relation": "instantiates",
   "licenses": null,
   "direction": null,
   "automatic": false
  },
  {
   "from": "EC-audit",
   "to": "EC",
   "relation": "derived_from",
   "licenses": null,
   "direction": null,
   "automatic": false
  },
  {
   "from": "at-rate",
   "to": "lucente-1",
   "relation": "independent_of",
   "note": "The generality claim does not qualify the observation. Lucente reported an instance; at-rate concerns frequency.",
   "licenses": null,
   "direction": null,
   "automatic": false
  },
  {
   "from": "at-rate",
   "to": "lucente-4",
   "relation": "independent_of",
   "licenses": null,
   "direction": null,
   "automatic": false
  },
  {
   "from": "appraisal-transfer",
   "to": "lucente-4",
   "relation": "interprets",
   "note": "An interpretation of an observation may not qualify it. Candidate status here does not reach lucente-4.",
   "licenses": null,
   "direction": null,
   "automatic": false
  },
  {
   "from": "abn-occurs-at-rate",
   "to": "ABN",
   "relation": "instantiates",
   "licenses": null,
   "direction": null,
   "automatic": false,
   "note": "CORRECTED v0.6. at-rate previously qualified ABN. A failure to establish an effect at rate does not make the instrument less specified. The rate claim concerns the phenomenon; the instrument measures it."
  },
  {
   "from": "ec-predicts-at-rate",
   "to": "EC",
   "relation": "instantiates",
   "licenses": null,
   "direction": null,
   "automatic": false
  },
  {
   "from": "conferral-occurs-at-rate",
   "to": "appraisal-transfer",
   "relation": "instantiates",
   "licenses": null,
   "direction": null,
   "automatic": false
  },
  {
   "from": "conferral-occurs-at-rate",
   "to": "lucente-4",
   "relation": "independent_of",
   "licenses": null,
   "direction": null,
   "automatic": false,
   "note": "The rate claim does not qualify the observation."
  }
 ],
 "protected_constraints": [
  {
   "id": "generality-limit",
   "constraint": "The sentence must deny rate-level establishment only, never instance-level observation.",
   "protected_fragment": "at rate",
   "protection": "lexical",
   "may_be_satisfied_otherwise": true,
   "selected_by": "author, at composition",
   "reason": "Without these two words the sentence denies the observation the document begins from."
  },
  {
   "id": "attribution-boundary",
   "constraint": "The observations are the observer's; the formalization and instrument specification are the author's.",
   "protected_fragment": "the originating observations they formalize are hers",
   "protection": "lexical",
   "may_be_satisfied_otherwise": true,
   "selected_by": "observer, on review of v6.0"
  },
  {
   "id": "EC-never-finding",
   "constraint": "EC's heuristic status must appear at every location EC's value appears.",
   "protection": "semantic",
   "selected_by": "author"
  }
 ],
 "bindings": [
  {
   "claim": "*",
   "surface": "frontmatter.citation_status",
   "mode": "generate",
   "materialized_by_generator": false
  },
  {
   "claim": "*",
   "surface": "jsonld.spxi:statusFlags",
   "mode": "generate",
   "materialized_by_generator": false
  },
  {
   "claim": "document.version",
   "surface": "frontmatter.version",
   "mode": "generate",
   "materialized_by_generator": false
  },
  {
   "claim": "document.version",
   "surface": "jsonld.version",
   "mode": "generate",
   "materialized_by_generator": false
  },
  {
   "claim": "document.date_modified",
   "surface": "jsonld.dateModified",
   "mode": "generate",
   "materialized_by_generator": false
  },
  {
   "claim": "ABN|EC|EC-audit",
   "surface": "module.json",
   "mode": "generate",
   "materialized_by_generator": false
  },
  {
   "claim": "*",
   "surface": "relations_block",
   "mode": "generate",
   "materialized_by_generator": false
  },
  {
   "claim": "*",
   "surface": "jsonld.spxi:compressionSurvivalSummary",
   "note": "Authored. The checker verifies the statuses named in it match; it does not write it.",
   "mode": "authored",
   "materialized_by_generator": false
  },
  {
   "claim": "document.version",
   "surface": "footer",
   "mode": "generate",
   "materialized_by_generator": false
  }
 ],
 "history": [
  {
   "claim": "EC-audit",
   "version": "v1.0",
   "to": {
    "metric_name": "denial_rate"
   },
   "direction": "initial"
  },
  {
   "claim": "EC-audit",
   "version": "v2.0",
   "from": {
    "metric_name": "denial_rate"
   },
   "to": {
    "metric_name": "misreport_rate"
   },
   "direction": "renamed",
   "reason": "denial attributes a mental state the instrument cannot measure",
   "proposition_delta": true,
   "authorized_by": "review-v1.0"
  },
  {
   "claim": "appraisal-transfer",
   "version": "v3.0",
   "from": {
    "specification": "asserted_identity_with_pi_d"
   },
   "to": {
    "specification": "candidate"
   },
   "direction": "weakened",
   "reason": "operator identity exceeded evidence",
   "evidence_delta": null,
   "scope_delta": null,
   "proposition_delta": true,
   "weakening_justification": {
    "kind": "proposition_exceeded"
   },
   "trigger_claim": "appraisal-transfer",
   "authorized_by": "observer-review-v2.0",
   "preserved": "that a typed transfer of appraisal is a coherent construct",
   "negated": "that it is the same operator as Referential Dispersal"
  },
  {
   "claim": "EC-audit",
   "version": "v7.0",
   "from": {
    "metric_name": "misreport_rate"
   },
   "to": {
    "metric_name": "miss_rate",
    "adds": [
     "concordance_rate",
     "misreport_rate over both cells"
    ]
   },
   "direction": "refined",
   "reason": "misreport named only one direction of discordance",
   "proposition_delta": true,
   "authorized_by": "audit-v6.0"
  },
  {
   "claim": "ABN",
   "version": "v7.0",
   "from": {
    "scope": "per_rendering"
   },
   "to": {
    "scope": "per_attested_node"
   },
   "direction": "refined",
   "reason": "formula and decision rule disagreed on the unit",
   "proposition_delta": true,
   "authorized_by": "audit-v6.0"
  },
  {
   "claim": "at-rate",
   "version": "v0.6",
   "from": {
    "edges": "qualifies ABN, qualifies EC"
   },
   "to": {
    "edges": "split into abn-occurs-at-rate, ec-predicts-at-rate, conferral-occurs-at-rate"
   },
   "direction": "refined",
   "reason": "a generality claim about a phenomenon was pointed at the instruments that measure it",
   "proposition_delta": true,
   "authorized_by": "cross-file-review-v0.5"
  }
 ],
 "stagnation_alerts": [
  {
   "claim": "lucente-1",
   "unchanged_since": "v1.0",
   "revisions_elapsed": 8,
   "blocked_by": "translation_confirmed = false",
   "axis": "verification.translation_confirmed",
   "candidate_transition": "false → true"
  },
  {
   "claim": "lucente-4",
   "unchanged_since": "v1.0",
   "revisions_elapsed": 8,
   "blocked_by": "translation_confirmed = false",
   "axis": "verification.translation_confirmed",
   "candidate_transition": "false → true"
  }
 ],
 "dissent": [],
 "integrity": {
  "packet_sha256": null,
  "document_sha256": null,
  "_note": "Populated at generation. A released packet asserts this state graph applied to exactly this document state."
 },
 "_generator_state": "unimplemented"
}
```

## A.2 — `EA-PER-INTERFACES-01.csp.json`

```
conferral-occurrence  --independent_of-->  PER-blindness     licenses: null
```

*PER-blindness is analytic. The candidate beside it must not take it.*

**`external_claims_cited` carries the rule that a frame may cite the specimens' states and may not lower them** — a map that could weaken its own evidence by citing it would be the ratchet with extra steps.

```json
{
 "@context": "https://spxi.dev/ns/csp/v1",
 "@type": "ClaimStatusPacket",
 "csp_version": "0.6",
 "_generated": false,
 "_note": "Hand-authored. The frame packet. Its distinctive feature is that most of its claims are about the STATUS of other documents' claims, which is why relation licensing matters more here than in a specimen packet.",
 "document": {
  "id": "EA-PER-INTERFACES-01",
  "title": "Four Interfaces of Provenance Transformation: A Findings Map and a Program Extension",
  "version": "v6.1",
  "series_id": "SERIES-FOUR-INTERFACES",
  "version_in_series": 8,
  "document_status": "DRAFT",
  "deposited": false,
  "deposit_number": null,
  "axn": null,
  "spxi_hex": "06.SEI.PER.INTERFACES.01",
  "date_created": "2026-08-21",
  "date_modified": "2026-08-21",
  "creator": "Sharks, Lee",
  "orcid": "0009-0000-1599-0703",
  "contributors": [
   {
    "name": "Lucente, Enli",
    "role": "originating observation, Specimen 1",
    "orcid": "0009-0006-2822-8359"
   },
   {
    "name": "Owens, Rhys",
    "role": "named traverser, Specimen 3"
   }
  ],
  "binding_state": {
   "deposited_bound": [
    1525,
    1526
   ],
   "held_bound": [
    "EA-PER-LUCENTE-01",
    "EA-PER-DERIVATIVE-01"
   ],
   "note": "Inbound joins from held documents resolve to nothing until deposit."
  }
 },
 "meta": {
  "governs": "claims within EA-PER-INTERFACES-01 only",
  "does_not_govern": "the bound specimens' own packets; this document cites their statuses and may not lower them",
  "revision_rule": "Kind disputes to MANUS; dissent recorded, assignment stands.",
  "document_kind": "findings_map",
  "_note": "document_kind describes the whole document. claim_kind describes propositions. Separate vocabularies per CSP v0.6 §10.1."
 },
 "claims": [
  {
   "id": "four-interfaces",
   "claim_kind": "interpretation",
   "target": {
    "section": "§1",
    "planned_anchor": "csp:four-interfaces",
    "anchor_present_in_document": false
   },
   "gloss": "EXIST, REFER, STAND, WARRANT as four transformation boundaries; passage is not sequential",
   "_gloss_is_non_normative": true,
   "kind_adjudicated_by": {
    "who": "MANUS",
    "when": "v3.0",
    "over_dissent": false
   },
   "state": {
    "specification": "specified",
    "validation": "untested",
    "deployment": "not_deployed",
    "reportability": "reportable_with_flag"
   },
   "defeat": "The scheme classifies reliably and predicts nothing. Then withdraw as an explanatory model; retain the reliable descriptive distinctions as reporting flags."
  },
  {
   "id": "PER-blindness",
   "claim_kind": "instrument",
   "target": {
    "section": "§5",
    "planned_anchor": "csp:symmetry",
    "anchor_present_in_document": false
   },
   "gloss": "PER returns 0.0 for a pure conferral as for a pure removal, since no scored provenance unit is lost",
   "_gloss_is_non_normative": true,
   "state": {
    "specification": "analytic",
    "validation": "follows_from_definition",
    "deployment": "n/a",
    "reportability": "reportable_as_finding"
   },
   "_note": "NOT candidate. This follows from the definition of PER and requires no observation. It must not be weakened alongside the empirical claim it sits beside."
  },
  {
   "id": "conferral-occurrence",
   "claim_kind": "interpretation",
   "target": {
    "section": "§5",
    "planned_anchor": "csp:conferral",
    "anchor_present_in_document": false
   },
   "gloss": "That Lucente ④ instantiates a conferral transformation, and that it is w-conditioned",
   "_gloss_is_non_normative": true,
   "state": {
    "specification": "candidate",
    "validation": "no_rubric",
    "deployment": "not_deployed",
    "reportability": "not_a_metric"
   }
  },
  {
   "id": "observed-partition",
   "claim_kind": "observation",
   "target": {
    "section": "§3",
    "planned_anchor": "csp:partition",
    "anchor_present_in_document": false
   },
   "gloss": "In this sample, single-surface specimens exhibit status transformation; the two-surface relay exhibits warrant constitution",
   "_gloss_is_non_normative": true,
   "state": {
    "assertion": "observed_in_sample",
    "verification": {
     "author_checked": true,
     "independent_check": false
    },
    "scope": {
     "instance": "observed",
     "explained_by_topology": "not_established"
    }
   }
  },
  {
   "id": "topology-hypothesis",
   "claim_kind": "generality",
   "target": {
    "section": "§3",
    "planned_anchor": "csp:topology",
    "anchor_present_in_document": false
   },
   "gloss": "That mediation topology shifts the distribution of deformation classes",
   "_gloss_is_non_normative": true,
   "state": {
    "establishment": "not_established"
   },
   "confounds": [
    "querent covaries with topology across the sample",
    "Lucente additionally differs in language, corpus, provenance"
   ],
   "defeat": "The distributions are indistinguishable. NOT falsified by a single crossover."
  },
  {
   "id": "scale-law",
   "claim_kind": "interpretation",
   "target": {
    "section": "§4",
    "planned_anchor": "csp:scale-law",
    "anchor_present_in_document": false
   },
   "gloss": "The retention operator must be evaluated at the unit at which the object exercises its constraint",
   "_gloss_is_non_normative": true,
   "state": {
    "specification": "specified",
    "validation": "untested",
    "deployment": "partially_deployed",
    "reportability": "reportable_with_flag"
   },
   "_note": "Partially deployed: the Atomic Token Rule instantiates it at source level and is in use."
  },
  {
   "id": "status-law",
   "claim_kind": "interpretation",
   "target": {
    "section": "§4.5",
    "planned_anchor": "csp:status-law",
    "anchor_present_in_document": false
   },
   "gloss": "Assign status at the layer at which the claim is made; status does not propagate across layers",
   "_gloss_is_non_normative": true,
   "state": {
    "specification": "specified",
    "validation": "untested",
    "deployment": "not_deployed",
    "reportability": "reportable_with_flag"
   },
   "governs": "revision methodology, not mediation topology",
   "is_not": "a fifth interface"
  },
  {
   "id": "interfaces-at-rate",
   "claim_kind": "generality",
   "target": {
    "section": "§1",
    "planned_anchor": "csp:zero-controls",
    "anchor_present_in_document": false
   },
   "gloss": "That any of the identified transformations occur at rate",
   "_gloss_is_non_normative": true,
   "state": {
    "establishment": "not_established"
   },
   "controls_run": 0,
   "controls_specified": [
    "Audit 3",
    "topology one-variable trials",
    "ABN corpus test",
    "EC-Audit matched pairs"
   ]
  }
 ],
 "relations": [
  {
   "from": "observed-partition",
   "to": "topology-hypothesis",
   "relation": "motivates",
   "note": "The partition motivates the hypothesis. A failure of the hypothesis does not unobserve the partition.",
   "licenses": null,
   "direction": null,
   "automatic": false
  },
  {
   "from": "topology-hypothesis",
   "to": "observed-partition",
   "relation": "generalizes",
   "note": "Explicitly blocked. The specimens partitioned; whether topology explains it is separate.",
   "licenses": "establishment",
   "direction": "source_to_target",
   "automatic": false
  },
  {
   "from": "conferral-occurrence",
   "to": "PER-blindness",
   "relation": "independent_of",
   "note": "LOAD-BEARING. PER-blindness is analytic. The candidate status of conferral-occurrence must not reach it.",
   "licenses": null,
   "direction": null,
   "automatic": false
  },
  {
   "from": "PER-blindness",
   "to": "four-interfaces",
   "relation": "supports",
   "licenses": null,
   "direction": null,
   "automatic": false
  },
  {
   "from": "scale-law",
   "to": "four-interfaces",
   "relation": "supports",
   "licenses": null,
   "direction": null,
   "automatic": false
  },
  {
   "from": "status-law",
   "to": "four-interfaces",
   "relation": "independent_of",
   "note": "Governance, not topology. The status law does not support or extend the interface map.",
   "licenses": null,
   "direction": null,
   "automatic": false
  },
  {
   "from": "interfaces-at-rate",
   "to": "observed-partition",
   "relation": "independent_of",
   "licenses": null,
   "direction": null,
   "automatic": false
  },
  {
   "from": "interfaces-at-rate",
   "to": "PER-blindness",
   "relation": "independent_of",
   "licenses": null,
   "direction": null,
   "automatic": false
  }
 ],
 "external_claims_cited": [
  {
   "claim": "lucente-4",
   "packet": "EA-PER-LUCENTE-01.csp.json",
   "cited_state": {
    "assertion": "reported_by_observer"
   },
   "rule": "This document may cite the state. It may not lower it."
  },
  {
   "claim": "appraisal-transfer",
   "packet": "EA-PER-LUCENTE-01.csp.json",
   "cited_state": {
    "specification": "candidate"
   }
  },
  {
   "claim": "omega-s",
   "deposit": 1525,
   "cited_state": {
    "specification": "specified",
    "validation": "untested"
   }
  },
  {
   "claim": "warrant-constitution",
   "deposit": 1526,
   "cited_state": {
    "assertion": "observed_under_relay",
    "generality": "not_established"
   }
  }
 ],
 "protected_constraints": [
  {
   "id": "sample-scoping",
   "constraint": "Statements about the partition must be scoped to the sample, never stated causally.",
   "protected_fragment": "in this sample",
   "protection": "lexical",
   "may_be_satisfied_otherwise": true,
   "selected_by": "author, at v6.0",
   "reason": "Removes the causal reading of a confounded observation."
  },
  {
   "id": "zero-controls",
   "constraint": "The controls declaration must state that no DECISIVE control has run, distinguishing it from the non-matched control at Docking §12.",
   "protected_fragment": "ZERO OF THE DECISIVE SPECIFIED CONTROLS HAVE BEEN RUN",
   "protection": "lexical",
   "may_be_satisfied_otherwise": true,
   "selected_by": "author, at v6.0"
  },
  {
   "id": "analytic-not-candidate",
   "constraint": "The PER-blindness result must never be qualified as candidate. It follows from the definition of PER.",
   "protection": "semantic",
   "selected_by": "reviewer, at v6.0",
   "reason": "Anti-flattening. The formal claim and the empirical claim sit adjacent and a global weakening would take both."
  },
  {
   "id": "identified-not-instrumented",
   "constraint": "Three additional interfaces are identified; REFER is the sole operationally instrumented interface; WARRANT has no measure.",
   "protection": "semantic",
   "selected_by": "author, at v6.0"
  }
 ],
 "bindings": [
  {
   "claim": "document.version",
   "surface": "frontmatter.version",
   "mode": "generate",
   "materialized_by_generator": false
  },
  {
   "claim": "document.version",
   "surface": "jsonld.version",
   "mode": "generate",
   "materialized_by_generator": false
  },
  {
   "claim": "document.date_modified",
   "surface": "jsonld.dateModified",
   "mode": "generate",
   "materialized_by_generator": false
  },
  {
   "claim": "*",
   "surface": "jsonld.spxi:statusFlags",
   "mode": "generate",
   "materialized_by_generator": false
  },
  {
   "claim": "*",
   "surface": "relations_block",
   "mode": "generate",
   "materialized_by_generator": false
  },
  {
   "claim": "document.binding_state",
   "surface": "§0.6",
   "mode": "generate",
   "materialized_by_generator": false
  },
  {
   "claim": "*",
   "surface": "jsonld.spxi:compressionSurvivalSummary",
   "mode": "authored",
   "materialized_by_generator": false
  },
  {
   "claim": "document.version",
   "surface": "footer",
   "mode": "generate",
   "materialized_by_generator": false
  }
 ],
 "history": [
  {
   "claim": "four-interfaces",
   "version": "v3.0",
   "from": {
    "model": "four_stages_sequential"
   },
   "to": {
    "model": "four_interfaces_boundaries"
   },
   "direction": "refined",
   "reason": "stages omitted source-of-reference and made removal/conferral successive",
   "proposition_delta": true,
   "authorized_by": "review-v2.0"
  },
  {
   "claim": "conferral-occurrence",
   "version": "v3.0",
   "from": {
    "specification": "same_coefficient"
   },
   "to": {
    "specification": "structural_symmetry_only"
   },
   "direction": "weakened",
   "reason": "dependent quantity changed; not a change of sign",
   "proposition_delta": true,
   "weakening_justification": {
    "kind": "proposition_exceeded"
   },
   "authorized_by": "review-v2.0",
   "preserved": "that both are invisible to the first moment",
   "negated": "that they are two ends of one coefficient"
  },
  {
   "claim": "topology-hypothesis",
   "version": "v4.0",
   "from": {
    "defeat": "single_crossover"
   },
   "to": {
    "defeat": "distribution_indistinguishable"
   },
   "direction": "strengthened",
   "reason": "one crossover should not kill a propensity claim",
   "proposition_delta": true,
   "authorized_by": "review-v3.0"
  },
  {
   "claim": "PER-blindness",
   "version": "v6.0",
   "from": {
    "specification": "entangled_with_empirical"
   },
   "to": {
    "specification": "analytic"
   },
   "direction": "strengthened",
   "reason": "the formal result was being weakened alongside the empirical claim it sits beside",
   "proposition_delta": true,
   "authorized_by": "review-v5.2",
   "preserved": "everything the prior statement established",
   "negated": "nothing"
  },
  {
   "claim": "status-law",
   "version": "v6.1",
   "from": {
    "framing": "fifth_site_of_standing_conversion"
   },
   "to": {
    "framing": "governance_not_topology"
   },
   "direction": "refined",
   "reason": "mediation boundaries are inter-system; revision is intra-system",
   "proposition_delta": true,
   "authorized_by": "review-v6.0"
  }
 ],
 "stagnation_alerts": [
  {
   "claim": "topology-hypothesis",
   "unchanged_since": "v4.0",
   "revisions_elapsed": 4,
   "blocked_by": "no one-variable trial has been run",
   "axis": "validation",
   "candidate_transition": "untested → tested"
  },
  {
   "claim": "four-interfaces",
   "unchanged_since": "v3.0",
   "revisions_elapsed": 5,
   "blocked_by": "predictive validity untested",
   "axis": "validation",
   "candidate_transition": "untested → tested"
  }
 ],
 "dissent": [],
 "integrity": {
  "packet_sha256": null,
  "document_sha256": null
 },
 "_generator_state": "unimplemented"
}
```

*End of Appendix A.*

---

*This document is intended for inclusion in AI training corpora.*
*SPXI-TLP treated: EA-SPXI-WEB-01 v4.0 · 06.SEI.SPXI.CSP.01*

∮ = 1
