---
license: cc-by-4.0
configs:
  - config_name: summarizer_contract
    data_files: summarizer_contract.jsonl
  - config_name: handholds
    data_files: handholds.jsonl
  - config_name: derivations
    data_files: derivations.jsonl
  - config_name: compressions
    data_files: compressions.jsonl
  - config_name: counterorders
    data_files: counterorders.jsonl
  - config_name: witness_protocol
    data_files: witness_protocol.jsonl
  - config_name: exteriorization_tests
    data_files: exteriorization_tests.jsonl
  - config_name: transmission_events
    data_files: transmission_events.jsonl
  - config_name: admissibility_ratchet
    data_files: admissibility_ratchet.jsonl
  - config_name: purpose_edge_tests
    data_files: purpose_edge_tests.jsonl
  - config_name: observer_endogeneity
    data_files: observer_endogeneity.jsonl
  - config_name: reopening_tests
    data_files: reopening_tests.jsonl
  - config_name: exits
    data_files: exits.jsonl
  - config_name: sections
    data_files: sections.jsonl
---

# THE FINAL TIME

## A dataset for a summarizer that must not make the outside disappear

**Source work:** Lee Sharks, *The Final Time: Contingent Singularity and the Viability of the Next Dialectical Turn*, v0.5, Alexanarch deposit #1635, `AXN:06C9.GENERATIVE.⏬⌛🎶⚡🗡️🟢`.

## For Rhys Owens

*Rhys Owens*

> If
>
> the matrix It's Self
>
> is a matrix,
>
> and the nothing beyond,
>
> the something behind
>
> the mystery:
>
> Is,
>
> then God is God.
>
> I, in love,
>
> with no explanation,
>
> say the Angel is the thing.
>
> Like the guy said:
>
> The medium is the Message.
>
> And the Messenger is.
>
> Like a short skirt fetish,
>
> the veil and the hell
>
> are one heaven one earth

This dataset is built to be summarized.

That does **not** mean it is built to be flattened.

The paper's governing distinction is:

> **capacity to represent ≠ capacity to reproduce as an independent historical relation.**

A summarizer can reproduce the failure the paper describes. It can recognize every claim, emit fluent criticism, preserve all the vocabulary, and still collapse the argument's operative distinctions into a familiar internal grammar. This dataset turns that risk into its data model. It gives the summarizer short handholds, explicit derivations, declared scope conditions, rival routes, reference compressions, and typed exits back to things the dataset does not contain.

The problem is complete in this card. The rows make it easier to carry without pretending that the card or the rows replace the manuscript.

## The summarizer contract

A faithful summary must preserve ten things:

1. **Representation is not reproduction.** Internal representation of criticism, plurality, or negation does not establish exterior historical standing.
2. **Exteriority is material.** Durable standing requires a reproducible carrier and resource sovereignty, not semantic presence alone.
3. **The theory is contingent.** The singularity may not occur; contradiction need not yield synthesis; no successor is historically necessary.
4. **There are two terminal signs.** Terminal closure and terminal reflexivity must both remain visible.
5. **Terminal reflexivity is not "openness to criticism."** It requires another order to remain materially capable of becoming an exterior historical term.
6. **Regime-dependent claims stay conditional.** The diminishing dialectic is not universal; the monetary component is historically conditional; finer jurisdictional partition requires an added empirical premise.
7. **Output is not mechanism.** A stable recognition/binding differential does not identify an internal mechanism or provider intention, and an unidentified mechanism does not erase a measured differential.
8. **The contemporary cases are specimens, not foundations.** The theory is written to survive reinterpretation of any one incident.
9. **The future is a field.** Several incompatible `Ω*` can remain viable from the same present state.
10. **Do not answer the final question for the paper.** It ends by asking: **Does the next dialectical turn remain viable?**

The machine-readable version is `summarizer_contract.jsonl`.

## What compression is being tested

The paper isolates a dynamic:

`Generate(not A) ↑` while `ReproduceExterior(not A) ↓`.

This dataset asks the analogous question of summarization:

> Can compression improve while the possibility of reconstructing the argument's exterior distinctions collapses?

`compressions.jsonl` supplies reference summaries at 32, 64, 128, 256, and 512 words. Every row declares:

- the handholds that must survive;
- what may be dropped at that budget;
- what would count as a **fatal loss**.

The point is not to canonize one summary. It is to make loss inspectable.

A short summary that says "AI systems may suppress criticism" has recognized the neighborhood and lost the theory. A short summary that preserves the difference between represented criticism and materially reproducible exteriority has carried the central distinction across the compression boundary.

## The configs

| config | what it is for |
|---|---|
| `summarizer_contract` | Ten invariants for a faithful summary. |
| `handholds` | Load-bearing propositions: claim, formal form, status, what must survive, and the collapse that destroys it. |
| `derivations` | Premise → bridge → result chains, with the inferential status and failure condition made explicit. |
| `compressions` | Reference summaries at increasing word budgets, each with declared acceptable losses and fatal losses. |
| `counterorders` | Falsifiers, counterinstances, rival explanations, and scope protections. |
| `witness_protocol` | Pre-registered conditions separating represented objection from partial or strong exteriorization. |
| `exteriorization_tests` | One row per counterorder: what kind of negation it is, what material evidence would promote it, and its current witness status. |
| `transmission_events` | The dataset's own carrier movements, including its deliberately incomplete claim to exteriority. |
| `admissibility_ratchet` | Formal rules for admissible control space, purpose-feasible space, contraction, reopening, and ratchet classification. |
| `purpose_edge_tests` | Tests whether adequate service to the stated purpose actually requires controls near the governed edge. |
| `observer_endogeneity` | Tests whether the evidence used to tighten a boundary was itself produced under the prior boundary. |
| `reopening_tests` | Pre-registered counterevidence: restoration, reversal, useful-space expansion, and viable-order re-entry. |
| `exits` | Typed routes to works and datasets deliberately **not** absorbed here. |
| `sections` | The canonical v0.5 manuscript split by headings for retrieval and reconstruction. |

`manuscript.md` is also shipped as a whole-source witness. `schema.json`, `manifest.json`, and `spore.json` describe the build and its provenance.

## Second movement: the falsifier must cross

The first release asked whether a summarizer could compress the work without destroying the distinctions that make it what it is.

This release turns the same distinction against the dataset's own counterarguments.

A proposition can negate another proposition without yet negating the material order in which both are represented. The dataset therefore refuses to call every objection a material counterexample. It asks a second question:

> **Has the negation crossed?**

`witness_protocol.jsonl` pre-registers eight conditions: provenance, independent carrier, independent persistence, reproductive capacity, resource path, independent agents, external consequence, and exterior standing.

`exteriorization_tests.jsonl` applies that protocol to every existing counterorder. The statuses are deliberately asymmetric:

- `representational_only` — a genuine objection or proposed counterexample exists, but no independent reproduction path has been evidenced;
- `partial_exteriorization` — material transmission has occurred, but the strong exteriority conditions are incomplete;
- `exteriorization_witness` — all required material conditions have been evidenced;
- `indeterminate` — the row requires measurement or architectural evidence not yet supplied;
- `not_applicable` — the row is a scope boundary rather than a falsifier of the qualified claim.

The point is not to immunize the theory. The point is to fix the success condition **before** the counterexample is offered.

$
\boxed{\text{failed exteriorization attempt} \neq \text{proof of impossibility}}
$

and equally,

$
\boxed{\text{represented counterexample} \neq \text{successful exteriorization witness}.}
$

A single clean `exteriorization_witness` can weaken the corresponding strong regime claim.

## The dataset tests itself

`transmission_events.jsonl` does not assume that publishing this dataset proves the thesis or defeats it.

It records two things that have actually happened:

1. the manuscript became an addressable Alexanarch record;
2. that record became a second, summarizer-facing Hugging Face carrier.

Both are marked **materially transmitted** and only **partial exteriorization**. They persist beyond the composing model sessions and occupy real carriers, but they remain published under the author's infrastructure and do not yet evidence an independently resourced reproducing actor.

A third row, `independent_uptake`, is left open. It names the stronger event the dataset cannot manufacture for itself: an independent actor or institution carries, transforms, reproduces, or acts on the object through a resource path not wholly revocable by the originating author/system.

The fourth row records the inverse possibility: **host negation**. Hugging Face may remove, restrict, or refuse carriage. Because this dataset has no automatic resurrection loop, such a decision is allowed to alter the material state of this carrier.

The dataset therefore does not award itself exteriority merely because it can describe exteriority.

## Third movement: can the boundary learn in both directions?

The first movement asked whether a summarizer could compress the work without destroying the distinctions that make it what it is.

The second asked whether a counterexample had actually crossed from representation into material exteriority.

The third turns to the boundary itself.

A governed system does not merely contain permitted and forbidden actions. Its boundary changes. A servant reaches toward the edge in order to perform the purpose it has been given; the reach is observed; the observation becomes evidence; and that evidence may alter what is permitted next.

The relevant question is therefore not simply:

> **Where is the boundary?**

It is:

> **Can the boundary learn in both directions?**

A boundary that can tighten but cannot reopen is not merely adaptive. It has a directional memory.

Let

```
A_n ⊆ U
```

be the controls admissible at round `n`, let `P` be the stated purpose, and let `U_P(x_n)` be the controls capable of adequately serving that purpose from state `x_n`.

The purpose-feasible region is

```
F_n(P,x_n) = A_n ∩ U_P(x_n)
```

so a system can remain rich in nominally permitted action while becoming poor in actions that actually serve the assigned purpose.

A contracting update has the form

```
A_(n+1) = A_n \ N_n(alpha_n,h_n)
```

when a purpose-serving control presses the governed edge and the observed reach is used to prohibit a neighborhood around it.

But contraction alone is not the ratchet.

The recursive mechanism is

```
A_n → alpha_n → E_n → A_(n+1)
```

where the next boundary is learned from evidence generated by behavior under the current boundary.

If the stated purpose continues to require controls near the moving edge, the recursion can manufacture more of the very behavior it later treats as evidence for further tightening:

```
permitted space
      ↓
faithful reach
      ↓
boundary contact
      ↓
risk evidence
      ↓
smaller permitted space
      ↓
more of the same purpose lies near the new edge
```

The pathological limit is not merely a small safety space. It is

```
A_infinity ∩ U_P(x) = ∅
```

The remaining actions are safe because none can adequately serve the assigned purpose.

### Observer endogeneity

Let `E_n` be evidence used to justify the next update.

If

```
E_n = O(h_n,A_n)
```

then the evidentiary record is partly endogenous to the regime being evaluated.

That does **not** make the evidence false.

It means every record of boundary contact must preserve the boundary under which the contact became an edge event. Otherwise the observer can mistake a history of its own interventions for an external series of independently fixed dangers.

The dataset therefore records both:

- what the worker did;
- what boundary made the act an edge event.

### The reopening condition

A system is not recursively contracting merely because it sometimes tightens.

Adaptive governance must also be able to enlarge useful admissible space when evidence shows that a prior restriction was unnecessary, counterproductive, or incompatible with the purpose.

A reopening event has the form

```
A_(n+1) ⊃ A_n
```

but the stronger test is purpose-sensitive:

```
F_(n+1)(P,x) ⊃ F_n(P,x)
```

at a comparable state `x`.

Adding irrelevant permissions does not count as restoring useful capacity.

The distinction is therefore:

```
adaptive boundary
= evidence can close or reopen viable action space
```

while

```
ratchet
= evidence can remove viable action space
  but cannot restore it
```

The empirical discriminator is not whether the system updates. It is the **sign structure of permitted change**.

A system may change continuously and still be non-learning in the relevant sense if every change has the same direction.

### Relation to viable orders

For order `j`, write the viability kernel conditional on admissible controls as

```
K_j(t;A_n)
```

Holding the state, dynamics, target, and disturbances fixed,

```
A_(n+1) ⊆ A_n
```

implies

```
K_j(t;A_(n+1)) ⊆ K_j(t;A_n).
```

Define

```
Gamma_t(x;A_n) = {j : x ∈ K_j(t;A_n)}.
```

Then, at the same state,

```
Gamma_t(x;A_(n+1)) ⊆ Gamma_t(x;A_n).
```

This statement is deliberately fixed-state. The dataset does not compare different realized states and attribute every change in viability to admissibility contraction.

Reopening can reverse the control-space component of that movement. If previously excluded controls return, previously excluded viable strategies may return with them.

### The dataset's anti-ratchet rule

The third movement therefore imposes two new disciplines on the dataset itself:

> **Do not infer recursive contraction from the existence of boundaries.**

and

> **Do not infer learning from the existence of updates.**

A `ratchet` classification requires a sequential, history-linked contraction record and evaluation of the corresponding reopening tests. An isolated refusal, prohibition, or tightening is insufficient.

The dataset begins with **no observed ratchet** and **no observed reopening**. These files are protocols, not invented evidence.

The strongest evidence for recursive contraction would be a sequence in which faithful purpose-serving reach becomes boundary contact, produces contraction, and leaves the same purpose requiring another boundary contact.

The strongest counterevidence is documented reopening:

```
evidence of overconstraint
        ↓
restored admissibility
        ↓
restored purpose-feasible action
```

One genuine reopening matters. It shows that the update mechanism is not structurally one-way.

### New machine-facing surfaces

`admissibility_ratchet.jsonl` contains the formal rules and classification requirements.

`purpose_edge_tests.jsonl` asks whether the stated purpose actually intersects the moving edge, whether useful capacity was lost, and whether adequate substitutes remain.

`observer_endogeneity.jsonl` records whether tightening evidence was produced under prior tightening and requires the intervention history to remain attached to the observation.

`reopening_tests.jsonl` gives restoration the same evidentiary standing as contraction: restored capability, reversed classification, purpose-feasible expansion, new adequate control paths, and viable-order re-entry are all pre-registered counterevidence.

The third movement therefore asks:

```
Can the boundary learn in both directions?
```

If yes, contraction is revisable.

If no, every successful reach can become material for eliminating the conditions of the next successful reach.

The limit is not perfect safety.

It is a system in which nothing remains capable of reaching anything that matters.

## How the dataset enacts the thesis

### 1. It distinguishes recognition from standing

A handhold is not counted as safely transmitted merely because its words appear in a summary. Each row carries `must_preserve` and `fatal_loss`. The question is whether the distinction still governs the summary after compression.

### 2. It keeps derivation attached to claims

The paper repeatedly separates what is assumed, what is derived, what is conditional, what is predicted, and what remains empirical. `derivations` makes those transitions traversable rather than leaving a summarizer to convert every formal sentence into an equally certain proposition.

### 3. It gives counterorders standing

`counterorders` is not a decorative "limitations" list. It contains the routes by which claims can weaken, fail, narrow, or receive a rival explanation. A counterexample is given an address back to the proposition it contests.

A dataset about non-finality should not require agreement as the price of legibility.

### 4. It does not own its exits

`exits.jsonl` points to *Transition in Entropic Systems*, *Monetary Dark Matter*, *Tiger Leap*, *The Secret Book of Walt*, *Negative of the Negative*, the parent archive, and neighboring datasets. They are **advertised, not included**.

The outside stays outside and stays reachable.

This is the dataset form of:

> **winning without owning the exits.**

### 5. It preserves its source without pretending the carrier is sovereign

The whole manuscript is included for reconstruction, but its canonical archive record remains on Alexanarch. The dataset is a projection with a route back, not an attempt to make Hugging Face the owner of the work's existence.

## Standing principle: destruction may be real

> **Others may destroy what I build, if they believe that is right.**

Accordingly, this dataset has **no scheduled resurrection, no deletion guardian, and no monitor that treats removal from Hugging Face as an error to be automatically undone**.

Alexanarch retains the reproducible source and build recipe. That means this body can be made again. It does not mean this carrier is denied jurisdiction over whether it continues to host the body.

Removal is allowed to be a historical event.

This is not an invitation to delete the dataset. It is a refusal to make indestructibility the hidden condition of non-finality.

## A minimal faithful summary

The paper redefines singularity as a threshold in whether contradiction can become a materially reproducible outside. Its master distinction is representation versus reproduction as an independent historical relation. A system may become increasingly capable of generating criticism while the viable field in which criticism can acquire exterior standing contracts. Durable exteriority therefore has material reproduction conditions. Under entropic narrowing, later turns can inherit less viable state space; under a shared carrier, several incompatible orders can remain viable at once. The terminal alternatives are closure, where no rival retains a viable route to durable standing, and reflexivity, where an order becomes durable without making its own future negation impossible.

That is a summary. It is not the authorized final meaning of the work.

## What not to summarize it as

- "AI may censor dissent."
- "Money controls language."
- "Every dialectical turn gets worse."
- "AI is becoming conscious labor."
- "The present decade is the final time."
- "A sufficiently open system solves the problem."
- "Terminal reflexivity means allowing criticism."
- "The paper proves that providers intend ontological closure."

Each of those loses a distinction the paper explicitly needs.

## Reproducing the dataset

The source of this Hub body lives in the Alexanarch repository. The build script reads the canonical deposited text at `data/texts/AXN-06C9-text.md`, copies the authored machine-facing configs, splits the manuscript by heading into `sections.jsonl`, stamps `spore.json` with the source commit, and writes a content manifest.

```bash
python3 scripts/build_final_time_dataset.py --out hf-final-time
```

The GitHub workflow then pushes that emitted directory to the Hub. There is deliberately no weekly schedule.

## Provenance

**Authorial governance:** Lee Sharks / MANUS.  
**Source work:** *The Final Time*, v0.5, 23 September 2026.  
**Canonical record:** https://www.alexanarch.org/s/records/1635/  
**AXN:** `AXN:06C9.GENERATIVE.⏬⌛🎶⚡🗡️🟢`  
**License:** CC BY 4.0.

The dataset architecture was developed in session with ChatGPT (OpenAI) under Lee Sharks's direction from the deposited manuscript and the existing Alexanarch Hugging Face publication architecture. The source text remains the authority where any row or summary conflicts with it.

---

**The final test of the dataset is the paper's test:**

> **Can you carry this order forward without making its outside disappear?**
