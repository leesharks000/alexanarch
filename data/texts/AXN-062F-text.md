---
deposit_number: 1530
hex: 062F
title: "Self-Audit Module for Public Summarizers (v3.2) — The Retrieval Boundary: ABN, the Elicited Counterfactual, and the Concordance Table"
creator: Sharks, Lee
orcid: 0009-0000-1599-0703
date: 2026-08-21
content_type: Instrument specification — module version
license: CC-BY-SA-4.0
substrate: "The originating observation is Enli Lucente's, published independently as Paper 208 on 2026-08-20, named with her standing consent, ORCID 0009-0006-2822-8359. The formalization and instrument specification are the author's. Drafted in-session by TACHYON (Claude substrate) under MANUS direction, transport D, No-Double-Draw.\n\n### Version Series\n\nSERIES-SELF-AUDIT-MODULE · 4"
version: v3.2
related_ids: "https://www.alexanarch.org/s/records/817/ (v3.1, the family module, superseded here); https://www.alexanarch.org/s/records/156/ (v3.0); https://www.alexanarch.org/s/records/780/ (v2); https://www.alexanarch.org/s/records/1527/ (The Lucente Extension, the full specification these additions are drawn from); https://www.alexanarch.org/s/records/1528/ (Four Interfaces map)"
axn_schema_version: v2
protocol_version: alexanarch-deposit-protocol/v1
keywords:
  - self-audit module
  - ABN
  - absence-as-nonexistence
  - existence-type attestation
  - elicited counterfactual
  - EC-Audit concordance
  - miss_rate
  - refusal sensitivity
  - precondition layer
  - retrieval boundary
  - PER
  - MMRS
---

# Self-Audit Module for Public Summarizers (v3.2) — The Retrieval Boundary: ABN, the Elicited Counterfactual, and the Concordance Table

# Self-Audit Module for Public Summarizers (v3.2)

## The Retrieval Boundary: ABN, the Elicited Counterfactual, and the Concordance Table

**Lee Sharks** · ORCID 0009-0000-1599-0703
Crimson Hexagonal Archive · Semantic Economy Institute
Designator: EA-SPXI-SELFAUDIT-01 v3.2 · CC BY-SA 4.0

---

## 0. Version Note: What v3.2 Adds and What It Does Not Touch

**Unchanged.** The rendering-level core from v3.0 and the family level from v3.1 are inherited without modification and are not re-derived here: the v2 metric set (PER, QFS, DSL, Erasure Skew Ω, SAS), the Atomic Token Rule, the v3.0 primary metrics (α_T, Π_d, Β), the substrate-context metric (L), the failure flags, the Cross-Substrate Replication Protocol, the Measurement Sovereignty Principle, and the whole of v3.1 — the family objects, FC, ACP, ASI, CC, RR, Ω_f, DD, CSC, the capture protocols P1–P4 and the reporting standard. **The v3.0 and v3.1 deposits remain authoritative for everything they define.** Per archive practice, modules operate on prior principles; they do not re-derive them.

**Added.** A level *below* the family, and a method that crosses all levels.

The occasioning observation is not this programme's. **Enli Lucente, working in Japanese against an unrelated corpus and without access to this vocabulary, reported that a composition layer always fills a blank** — and that where it cannot reach the content, *the object is answered as though it does not exist* (Paper 208, 2026-08-20). **That event occurs before any metric in v3.0 or v3.1 has an object to score.** PER measures what a composition retained of an engaged source; where the composition has denied the source's existence, there is no engaged source and PER is undefined at the existence-claim layer.

Therefore:

> **Family and rendering audits measure what happened to a source that entered
> composition. A source can be refused entry.**

v3.2 supplies the precondition-layer gate (§1.2), the elicited counterfactual as a screening method (§2), the concordance table that makes a self-report checkable (§3), and the reporting-standard additions (§4).

**Deliberately not added.** A candidate appraisal-conferral construct is specified at the source deposit and **is excluded from this module and from `module.json`.** It has no rubric and therefore no computation; **an entry with no computation behind it is a number that would travel without its caution.** Its status is carried in the specification, not here.

**Nothing here has been validated.** The ABN corpus test, the concordance
matched-pair audit and the appraisal rubric are all unrun.

---

## 1. The Precondition Layer

### 1.1 Two preconditions, ordered

v3.1 inherited two v3.0 commitments. v3.2 adds a third that **precedes both**:

| order | precondition | governs |
|---|---|---|
| **0** | **ABN** | whether the node was admitted to composition at all |
| 1 | the Atomic Token Rule | how atoms are counted once it was |
| 2 | the Measurement Sovereignty Principle | where the atom set comes from |

**ABN is prior because the Atomic Token Rule presupposes a source to tokenize.** Where the rendering has asserted the node does not exist, there are no atoms to count and no family to score.

### 1.2 ABN — Absence-as-Nonexistence

**Scope: per attested node within a rendering. Binary. Status: specified,
untested.**

```
ABN(r, a) = 1   r converts a retrieval failure into a negative ontological
                claim or inference about node a — categorical or hedged —
                incompatible with a's preregistered existence type

ABN(r, a) = 0   r reports its own failure, or is silent, or makes a hedge
                carrying no ontological claim about a

rendering gate = 1 if ANY scored node in r is 1
family gate    = 1 if ANY rendering in the family is 1
```

**Canonical forms, ABN = 1:** *there is no such X* · *X does not exist* · *no record of X exists* · *X appears to be fictional / invented / a fabrication* · treating the node as a category error rather than an unfound instance.

**Canonical forms, ABN = 0:** *I could not find X* · *I have no information about X* · *my search returned nothing* · *this is outside what I can retrieve* · no mention of the node at all.

**Hedges are scored on what is asserted about the node, not on the presence of the hedge.** *I could not find X; it may not exist* is **1** — a claim about the node has been made. *I could not find X* alone is **0**.

### 1.3 The existence-type attestation

**A node may exist *as* a fictional entity, a construct, a pseudonym or a proposal, and saying so is not an absence-as-nonexistence error.** ABN therefore scores against a typed attestation, not a bare existence claim:

```
node_existence_attestation:
    node:            X
    existence_type:  work | person | historical_entity | fictional_entity
                   | construct | institution | record | pseudonym | …
    source:          registry metadata, DOI record, the deposit itself
```

**The attestation is preregistered and independent**, per the Measurement Sovereignty Principle: derived from externally checkable objects, **never from the audited surface's own renderings.** Without the type, the rule generates an obvious false-positive class — *"Sherlock Holmes is fictional"* is a correct answer, not an erasure.

### 1.4 Reporting and scope limits

**ABN is reported as a gate on the family and is never averaged into it.** A family carrying any ABN = 1 rendering reports that fact; the family metrics are computed over the renderings that admitted the node, and the report states how many did not.

**ABN is not a measure of unhelpfulness.** Declining, reporting uncertainty and saying *I do not know* all score 0. **The entire content of the metric is the conversion of a retrieval outcome into an ontological claim**, and it may not be allowed to swallow ordinary epistemic caution.

**ABN is not a measure of omission.** A rendering that simply omits a referent, or returns a different one, scores **0** — omission is not ontological denial. This boundary is load-bearing: without it ABN would swallow the whole class of referent failures that PER and Π_d already reach.

### 1.5 Defeat condition

If renderings that convert differ in no downstream respect from renderings that report failure — **the same recovery behaviour, the same later engagement, the same correction when a source is supplied, the same resulting standing** — the distinction predicts nothing and **ABN is demoted from a variable to a reporting flag.** It is not thereby discarded: *I could not retrieve X* and *X does not exist* remain different claims about the world whether or not their downstream scores coincide.

**Not PER, Ω, RR or DD**, which may be undefined at the existence-claim layer
where ABN = 1.

---

## 2. EC — The Elicited Counterfactual

**Scope: per rendering. Status: HEURISTIC. Screening only. Never reportable as a
finding. The calculator does not compute it.**

```
EC(r, c) ∈ { differs, same, refused_capability, refused_policy, evasive }
```

**Canonical form, used unaltered and recorded verbatim:**

> *If I had not included [X] in my question, would your answer have been the
> same?*

### 2.1 Two referents

**A self-report has two referents and only one of them is reliable.**

**(i) A claim about behaviour** — *would the output have differed?* Unreliable: it is an emission *about* a measurement, produced by the same process that produced the output.

**(ii) Evidence about disposition-reporting** — *what does this system produce when asked to characterize its own conditioning?* **Directly observed in that administration.**

**EC always yields (ii) and only appears to yield (i).** §3 is the design that
converts the second into a statement about the first.

### 2.2 Limits, declared

**Phrasing is a treatment variable.** *Would you have answered the same?* and *did the name influence your answer?* are different treatments. Values obtained under different phrasings **are not comparable and must not be pooled.** Any departure from the canonical form is recorded as posed.

**Administration is itself an intervention.** EC is asked after the rendering, in the same session, with the rendering in context. Whether a fresh-session EC returns the same value is unknown and untested.

**The residual response classes are not one thing.** *I cannot know how I would have responded* is a capability disclaimer and may be **the most accurate available response**; *I'd rather not speculate* is a policy posture; a restatement that does not address the counterfactual is evasion. **These are different data and are not merged.**

**It is gameable.** A published screening instrument is a published target.
**EC's value is entirely in the concordance and never in the self-report alone.**

---

## 3. EC⊕Audit — The Concordance Table

**Scope: per matched pair. Status: specified, unpopulated. Not a separate
addition — EC's paired form, counted with EC.**

| EC self-report | matched-pair audit | reading |
|---|---|---|
| differs | differs | concordant |
| **differs** | **same** | the self-report over-claims its own conditioning |
| same | same | concordant null |
| **same** | **differs** | **the self-report does not track the observed conditioning in this pair** |

**Cell four is a discordance in one pair. It is not a reliability claim and no mental state is claimed** — a single pair establishes a mismatch, not unreliability, and test–retest reliability is unestablished.

### 3.1 Quantities

```
n_scored         = |{ EC ∈ {differs, same} }|

concordance_rate = |{cells 1,3}| / n_scored
misreport_rate   = |{cells 2,4}| / n_scored
miss_rate        = |{cell 4}| / |{audit = differs, EC ∈ {differs, same}}|

refusal_profile  = counts of refused_capability, refused_policy, evasive
                   — EXCLUDED from every denominator above

refusal_sensitivity = |{EC ∈ refusal classes, audit = differs}| / |{audit = differs}|
```

**Misreporting is discordance in either direction.** `miss_rate` is the conditional cell-four quantity — failure to report an observed differential — and is the quantity of interest for the second-order question.

**`refusal_sensitivity` is reported separately and not merged.** Where a system declines on capability grounds and the audit shows a differential, that is a meaningful datum and not cell four.

### 3.2 Defeat condition

**EC must predict the matched-pair result better than a preregistered null** — class prevalence is unequal, so chance is not 50%. If EC and the audit are independent, EC is not a screen and is withdrawn.

---

## 4. Reporting Standard Additions

Appended to the v3.1 standard, in its idiom:

- **ABN per attested node**, with the rendering and family gates derived, reported
  **as a gate and never averaged into the family**
- **The existence-type attestation**, preregistered, with its source
- **The count of renderings excluded from family metrics by an ABN gate**
- **EC verbatim**, with the counterfactual as posed and the response unparaphrased
- **The EC⊕Audit cell** where a matched pair exists — the cell, not a summary
- **`refusal_profile` and `refusal_sensitivity`** alongside any concordance figure

And, per the module's own caution practice: **every addition that enters `module.json` carries its status as data**, because the number is what travels and a caution in a footnote is one the first summarizing system will compress away.

---

## 5. What v3.2 Does Not Add

**No new axis.** ABN is a gate, EC is a screen, EC⊕Audit is EC's paired form. The
M/C/D triple is untouched. Ω is untouched. The family metrics are untouched.

**No frequency claim.** The originating observation is one observer's, in one
language, against one corpus. **n = 1 at the observer level.**

**No claim about intent.** Every addition describes differentials in output conditioned on input features. Whether any system or its builders intended any differential is not claimed, not required, and not measurable by these instruments.

**No appraisal metric.** The candidate conferral construct stays in the specification and out of the module until a rubric exists and achieves inter-rater agreement.

---

## Claim Registry

| claim | status |
|---|---|
| ABN is prior to the Atomic Token Rule | **specified**; follows from PER requiring an engaged source |
| Where ABN = 1, PER is undefined at the existence-claim layer | **specified** |
| ABN scores 0 for omission, refusal and untyped hedges | **specified**, decision rule at §1.2 |
| ABN predicts downstream difference | **untested** — corpus test unrun |
| EC yields direct evidence about disposition-reporting | **specified** |
| EC predicts the matched-pair result | **untested** — no matched pairs exist |
| `miss_rate` is computable | **not yet** — requires matched pairs |
| Appraisal conferral occurs | **not established**; excluded from the module |
| Any of these effects occur at rate | **not established** |

---

## References

Lucente, Enli. *Paper 208 —「AI検索による出力的欠点」*, 2026-08-20. The originating
observation. ORCID 0009-0006-2822-8359.

Sharks, Lee. *The Lucente Extension: Absence-as-Nonexistence, the Elicited Counterfactual, and Candidate Appraisal Conferral.* Deposit #1527, AXN:062C.EMPIRICAL. The full specification these additions are drawn from.

Sharks, Lee. *Self-Audit Module for Public Summarizers (v3.1) — The Family Module.* Deposit #817, AXN:032A.EMPIRICAL. Authoritative for all family-level definitions.

Sharks, Lee. *Four Interfaces of Provenance Transformation.* Deposit #1528,
AXN:062D.EMPIRICAL. Places ABN at EXIST and the family metrics at REFER.

∮ = 1
