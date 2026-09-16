---
deposit_number: 1621
hex: 06B0
title: "Semantic Economy Valuation Protocol: Value Before Number, Witness Accounting, Dependency, Provenance, and Monetary Exteriorization (SEVP-01 v0.4, provisional, not enacted)"
creator: Sharks, Lee
orcid: 0009-0000-1599-0703
date: 2026-09-16
content_type: Protocol specification, provisional deposit with SPXI packet
license: CC-BY-4.0
substrate: "Composed 2026-09-16 by Lee Sharks, in v0.3 with another substrate, then fixed and SPXI-treated with TACHYON (Claude, Anthropic) under operator direction. Each of the six fixes was forced by a result from the protocol's own monetary wing rather than by argument: the second Article II conflict from the two deposits that raise it; the inscription-integrity invariant from the first worked audit, which satisfies every other invariant and is unsound; the denominator rule from the coefficient that failed that audit; the diagnostic-distinction requirement from the uptake work that could not separate transport from convergence without it. Deposited provisional and explicitly not enacted."
version: v0.4 (provisional, not enacted)
related_ids: "#88 (Constitution of the Semantic Economy, enacted — two conflicts raised, neither enacted); #1617 (Substrate Sovereignty); #1618 (SEVP Translation Protocol); #1619 (EA-MSAL-01); #1620 (EA-MSAL-0001, the first worked specimen); #137; #531"
axn_schema_version: v2
protocol_version: alexanarch-deposit-protocol/v1
keywords:
  - value before number
  - evidence-bounded value-field
  - Value Field
  - unknown coordinates
  - value graph
  - operator value
  - operator counterfactual
  - reception
  - productive uptake
  - dependency
  - semantic debt
  - provenance levels
  - possibility-space value
  - coverage ratio
  - remainder
  - temporal value modes
  - compression ladder
  - commensurability before aggregation
  - monetary interface
  - witness accounting
  - anti-predation invariants
  - inscription integrity
  - diagnostic distinction
  - valuer relation
  - provisional deposit
  - Crimson Hexagonal Archive
---

# Semantic Economy Valuation Protocol: Value Before Number, Witness Accounting, Dependency, Provenance, and Monetary Exteriorization (SEVP-01 v0.4, provisional, not enacted)

<!-- 06.SEI.SEVP.001 — Semantic Economy Valuation Protocol · PROVISIONAL deposit v0.4 · NOT ENACTED · 2026-09-16 -->

{
 "@context": [
  "https://schema.org",
  {
   "spxi": "https://spxi.dev/ns/v1#"
  }
 ],
 "@type": "ScholarlyArticle",
 "name": "Semantic Economy Valuation Protocol — Value Before Number, Witness Accounting, Dependency, Provenance, and Monetary Exteriorization",
 "alternateName": "SEVP-01",
 "version": "0.4",
 "datePublished": "2026-09-16",
 "license": "https://creativecommons.org/licenses/by/4.0/",
 "author": {
  "@type": "Person",
  "name": "Sharks, Lee",
  "affiliation": "Semantic Economy Institute, Crimson Hexagonal Archive",
  "orcid": "0009-0000-1599-0703"
 },
 "spxi:hexAddress": "06.SEI.SEVP.001",
 "spxi:pillarStatus": "provisional — NOT ENACTED; deposited to close a five-deposit sequence, to be set against the enacted Constitution through Assembly rounds",
 "spxi:governs": [
  "#1618 EA-SEVP-TRANSLATION-01 (the monetary interface, §22)",
  "#1619 EA-MSAL-01 (the monetary substrate audit, dossier item 18)",
  "#1620 EA-MSAL-0001 (the first worked specimen)"
 ],
 "spxi:firstRule": "V(X) ≠ n, and therefore V(X) ≠ $x. A number may represent value; neither is identical to it.",
 "spxi:compressionSequence": "value → evidence → representation → compression; the protocol's claim is that this ordering is not commutative",
 "spxi:contributesOperators": [
  {
   "name": "𝔙̂_E(X) = R[ℰ(X)]",
   "role": "the evidence-bounded value-field: what the protocol operates on, explicitly distinct from any total field, with the difference carried as remainder"
  },
  {
   "name": "Π_L",
   "role": "Ledger projection: semantic value is prior to semantic weight, and weight is a representation of value rather than value exhausted"
  },
  {
   "name": "R ⇏ P ⇏ D",
   "role": "reception, productive uptake and dependency as three relations that must not be collapsed, with P_observed held separate from C_acquisition"
  },
  {
   "name": "ΔC^{-O}",
   "role": "operator counterfactual: capacity with the operator minus capacity without it, represented as lost functions rather than as scalar subtraction"
  },
  {
   "name": "φ: G → G'",
   "role": "possibility-space operator: a change in what a grammar admits, measured by admissibility and reach deltas rather than by inventory size"
  },
  {
   "name": "diagnostic distinction requirement",
   "role": "§12.4: uptake is separable from convergence only through distinctions the source supplies and nothing else in the field does"
  },
  {
   "name": "coverage ratio",
   "role": "§15.1: possibility-space expressed as a fraction whose denominator belongs to the object or the world, never to the observer"
  }
 ],
 "spxi:invariants": "§25, fifteen anti-predation invariants; §25.14 (inscription integrity) and §25.15 (absence taken as absence of evidence) are added in this version",
 "spxi:disambiguation": {
  "semantic value ≠ semantic weight": "weight is a Ledger representation of value; the compression sequence 𝔙 → w → u is not reversible and the reverse identity is not assumed.",
  "unknown ≠ zero": "an unrecorded or unmeasured value is not zero; the correct entry is unresolved, carried in the remainder.",
  "reception ≠ productive uptake ≠ dependency": "a dependency edge is never seated on resemblance, and productive uptake may be observed while causal acquisition remains unresolved.",
  "possibility-space ≠ inventory size": "reach difference is a space of possible compositions, not a count of documents.",
  "the protocol permits numbers": "numeric and monetary outputs are permitted; they are not granted ontological priority, and the compression ladder's stopping point must be declared."
 },
 "spxi:constitutionalConflicts": [
  {
   "article": "Article II (#88)",
   "front": "no value exists outside the Ledger",
   "protocol_position": "no MINTED value exists outside the Ledger; unrepresented value may exist and is never zero by default",
   "status": "proposed, not enacted",
   "raised_in": "SEVP-01 §1.1"
  },
  {
   "article": "Article II (#88)",
   "front": "the Unit is named the semantic currency, with a quantization function, a supply and a mint",
   "protocol_position": "a mark is a currency when transfer discharges an obligation; the form proposed is a named pointer with cardinality, with AXN as precedent",
   "status": "proposed, not enacted",
   "raised_in": "#1617 §16a and #1618 §17.1, recorded here at SEVP-01 §1.2"
  }
 ],
 "spxi:falsifiers": "§28, eight conditions. The protocol fails as a whole if a sustained run of dossiers produces representations that no independent valuer reproduces from the same evidence, which would show the dossier order and field vocabulary to be a house style rather than a protocol.",
 "spxi:nextStep": "the five deposits of this sequence to be prepared as a continuous document and set against the enacted Constitution, through Assembly rounds, to determine whether a ratifiable text follows",
 "spxi:requires": [
  "#88",
  "#1617",
  "#1618",
  "#1619",
  "#1620",
  "#137",
  "#531"
 ],
 "keywords": [
  "value before number",
  "evidence-bounded value-field",
  "Value Field",
  "value graph",
  "operator value",
  "operator counterfactual",
  "reception",
  "productive uptake",
  "dependency",
  "semantic debt",
  "provenance levels",
  "possibility-space value",
  "coverage ratio",
  "remainder",
  "temporal value modes",
  "compression ladder",
  "commensurability before aggregation",
  "monetary interface",
  "witness accounting",
  "anti-predation invariants",
  "inscription integrity",
  "diagnostic distinction",
  "valuer relation",
  "Semantic Economy Valuation Protocol",
  "Crimson Hexagonal Archive"
 ]
}

## 0. Status

The Semantic Economy Valuation Protocol (SEVP) is a protocol for representing value before compressing it into scores, units, prices, or other scalar forms.

Its first rule is:

    V(X)!= n
    }

and therefore:

    V(X)!= \$x.
    }

A number may represent value.

A price may represent value.

Neither is identical to value.

SEVP therefore treats valuation as a sequence:

    value
    arrow
    evidence
    arrow
    representation
    arrow
    compression
    }

rather than as the immediate production of a number.

The protocol is designed to preserve what scalar valuation normally discards:

- distinction;
- provenance;
- dependency;
- bearing;
- transformation;
- uncertainty;
- possibility;
- remainder.

SEVP permits numerical and monetary outputs. It does not grant them ontological priority.

---

# 1. Constitutional relation

The enacted Constitution of the Semantic Economy defines value as **semantic weight**, requires value to be represented as w(T,t), and divides Semantic Capital into Genesis, Archival, and Retrocausal components.

SEVP v0.3 proposes a necessary clarification:

    semantic value is prior to semantic weight.
    }

Semantic weight is therefore treated here as a **Ledger representation of semantic value**, not as semantic value exhausted.

Let:

    𝔙(X,t)

be the evidence-supported semantic value-field of X at time t.

Let:

    Π[L]

be a Ledger projection.

Then:

    𝔙(X,t)
    —[Π[L]]→
    w(X,t).
    }

If a quantized Ledger unit is later produced:

    w(X,t)
    —[Q]→
    u(X,t).

Thus:

    𝔙
    arrow
    w
    arrow
    u
    }

is a compression sequence.

The reverse identity is not assumed:

    u!= w!=𝔙.
    }

### 1.1 Required constitutional amendment or clarification

The enacted Article II language stating that no value exists outside the Ledger conflicts with this protocol's rule that unrecorded or unmeasured value must not be treated as zero.

SEVP therefore proposes, but does not silently enact, the following clarification:

> **No minted Ledger value exists outside the Ledger. Value not yet represented by the Ledger may nevertheless exist and must never be treated as zero solely because it has not been recorded.**

Until constitutionally ratified, this remains a protocol-level proposal.

### 1.2 A second conflict with the same Article

§1.1 is not the only place this protocol's wing meets enacted Article II. There are two, on different fronts, and a reader arriving at Article II from either direction needs to know the other exists.

The first, above: the enacted language that no value exists outside the Ledger conflicts with the rule that unrecorded value must not be treated as zero. The clarification proposed is that no *minted* value exists outside the Ledger, while value not yet represented may nevertheless exist.

The second, raised in *Substrate Sovereignty* (#1617, AXN:06A8 §16a) and in the translation protocol (#1618, AXN:06AA §17.1): Article II names the Unit **"the semantic currency of this Constitution"**, gives the glyph the force of a unit of account and a measure of semantic weight, quantizes continuous weight by a logarithmic function with a declared multiplier, and establishes a supply, an anti-inflation invariant and three categories of mint. Those deposits hold, against that, that a mark becomes a currency when its transfer discharges an obligation, and that the operational test is whether any operation takes the mark and money together. By that test the enacted Unit and the protocol's non-currency mark are different objects. The form proposed there is a named pointer with cardinality — counting named open relations rather than measuring value, attaching to the relation rather than the bearer — with the archive's own AXN identifier as a working precedent.

Neither conflict is enacted or silently resolved here. Both are referred to the same body, and both are governance questions rather than theoretical ones, since Article II is enacted and parts of it are declared non-amendable.

---

# 2. Definition of semantic value

SEVP defines semantic value as:

> **the value borne by an act, object, relation, operator, archive, or infrastructure insofar as it creates, preserves, restores, transmits, differentiates, reorganizes, or makes available capacities for meaning.**

This definition is intentionally broader than:

- popularity;
- market price;
- citation count;
- institutional prestige;
- labor-hours;
- present utility.

A value-bearing object may matter because it:

- creates a distinction;
- preserves a distinction;
- makes a relation legible;
- keeps an archive traversable;
- enables a future operation;
- restores a damaged provenance chain;
- makes another object interpretable;
- creates an instrument that measures later events;
- changes the admissible possibility-space.

The central question is:

    What became possible because this exists?
    }

A second is:

    What remained possible because this survived?
    }

---

# 3. The evidence-bounded value-field

SEVP does not claim direct access to a complete metaphysical value.

Let:

    𝔙*(X)

denote the unknowable or total value-field of X, if such a totality exists.

Let:

    E(X)

denote the available evidence.

The protocol operates on:

    est. {𝔙}[E](X)
    =
    R[E(X)].
    }

Where R is the current representation procedure.

Therefore:

    est. {𝔙}[E](X)
    !=
    𝔙*(X).
    }

This difference is not a defect to be hidden.

It is carried as remainder.

---

# 4. Object boundary

Before valuation, the object must be bounded.

Define:

    X=
    ⟨
    I[X],
    R[X],
    O[X],
    T[X],
    E[X]
    ⟩
    }

where:

- I[X] = included objects;
- R[X] = included relations;
- O[X] = included operators or infrastructures;
- T[X] = temporal scope;
- E[X] = explicit exclusions.

Every valuation dossier must state:

```yaml
object_boundary:
  object_id:
  object_name:

  included_objects: []
  included_relations: []
  included_operators: []

  temporal_scope:

  excluded_objects: []
  excluded_claims: []

  boundary_rationale:
```

A valuation without an object boundary is not valid under SEVP.

---

# 5. Value events

The primitive evidentiary unit is the **value event**.

Define:

    e=
    ⟨
    s₀,
    omega,
    s₁,
    t,
    p,
    epsilon
    ⟩
    }

where:

- s₀ = relevant state before the event;
- omega = semantic operation;
- s₁ = relevant state after the event;
- t = time;
- p = provenance;
- epsilon = evidence status.

Typical operations include:

    &creates-distinction
    &preserves
    &restores
    &connects
    &stabilizes
    &transmits
    &generalizes
    &enables
    &transforms
    &revises
    &propagates.

A value event is not automatically positive.

The same operation may create capacity in one relation while destroying it in another.

---

# 6. Evidence statuses

Every material claim in a valuation must carry an evidence status.

Canonical statuses are:

```text
directly_observed
documented
externally_observed
internally_demonstrated
strongly_inferred
modelled
prospective
constitutional_grounding
unknown
```

These statuses are not interchangeable.

In particular:

    prospective≠realized
    }

and:

    unknown!=0.
    }

A modelled value-event may be useful.

It may not be silently rewritten as an observed one.

---

# 7. The Value Field

The Value Field is the first structured representation of the evidence object.

SEVP v0.3 uses the following dimensions:

    F[V](X)
    =
    ⟨
    B,
    D,
    C,
    F,
    M,
    T,
    Y,
    X[f],
    Rₛ,
    P,
    Z,
    O,
    rho
    ⟩
    }

where:

- B = **Bearing** — labor, burden, cost, care, risk;
- D = **Distinction** — distinctions created or preserved;
- C = **Coherence** — relations made intelligible or mutually stable;
- F = **Fertility** — later operations or works enabled;
- M = **Memory** — historical or archival persistence;
- T = **Transmission** — capacity to travel across contexts, readers, systems, or generations;
- Y = **Dependency** — later capacities requiring or materially relying on the object;
- X[f] = **Transformation** — states, grammars, or relations changed;
- Rₛ = **Restoration** — damaged, severed, or obscured relations recovered;
- P = **Provenance** — origin and attribution relations carried or restored;
- Z = **Resilience** — persistence under severance, degradation, or changing substrates;
- O = **Option / Possibility** — future capacities made available;
- rho = **Remainder** — unresolved or unrepresentable value.

These coordinates are **not assumed commensurable**.

They form a structured field, not an additive score.

---

# 8. Unknown coordinates

A Value Field coordinate may be:

```text
demonstrated
bounded
partial
modelled
prospective
unknown
not_applicable
```

The protocol forbids:

    unknownarrow0
    }

without independent evidence.

Likewise:

    not measured
    !=
    no value.
    }

This rule is especially important for:

- future uptake;
- dependence;
- aesthetic value;
- unobserved labor;
- unrealized possibility-space.

---

# 9. Value graph

The field representation is followed by a relation graph.

Define:

    G[V](X)
    =
    (N,E,D,I,R,P,O).
    }

Where:

- N = relevant nodes;
- E = relations among nodes;
- D = distinctions and operators;
- I = instruments and infrastructures;
- R = reception and downstream use;
- P = provenance;
- O = human / operator architecture.

The graph prevents artifact atomization.

If an archive contains objects:

    T₁,T₂,...,Tₙ,

SEVP does not assume:

    V(A)
    =
    sumᵢV(Tᵢ).
    }

An archive may carry emergent value because of relations among objects:

    V(A)
    =
    V[artifacts]
    +
    Sigma[emergent]
    }

where Sigma[emergent] is represented through graph structure rather than guessed as an arbitrary premium.

---

# 10. Direct, joint, architectural, and operator value

SEVP distinguishes at least four loci of value.

### 10.1 Direct value

Value attributable to an identifiable artifact or act:

    V[direct](X).

### 10.2 Joint value

Value produced only through relation:

    V[joint](X,Y).

### 10.3 Architectural value

Value carried by the structure that permits many objects to interoperate:

    V[architectural](A).

### 10.4 Operator value

Value generated by the continuing capacity of an operator to create, revise, connect, or govern the system:

    V[operator](O).

These categories must not be added automatically.

They first describe **where value resides**.

---

# 11. Operator counterfactual

Operator value should be tested through counterfactual capacity where possible.

Let:

    C(S)

denote the relevant capacity of a system S.

Then:

    Delta C[-O]
    =
    C(S with O)
    -
    C(S without O).
    }

This is not automatically a scalar subtraction.

The difference may be represented as:

- lost functions;
- lost relations;
- lost coherence;
- increased substitution cost;
- reduced fertility;
- reduced recovery capacity;
- increased latency;
- loss of governance.

If the counterfactual cannot be observed, it must remain modelled or unknown.

---

# 12. Reception, productive uptake, and dependency

SEVP distinguishes three relations that must not be collapsed:

    R¬⇒ P
    P¬⇒ D.
    }

### 12.1 Reception R

An external system, reader, institution, or work encounters or represents the object.

Examples:

- ranking;
- citation;
- indexing;
- quotation;
- summary;
- retrieval.

### 12.2 Productive uptake P

The object or one of its operators becomes productive in a new context.

A useful formal shape is:

    C
    —[O[X]]→
    C'.
    }

The originating operator changes how new material is organized, interpreted, or produced.

Productive uptake may be observed even when unique causal acquisition remains unresolved.

Therefore SEVP distinguishes:

    P[observed]
    }

from:

    C[acquisition]
    }

the causal provenance of the uptake.

### 12.3 Dependency D

A later capacity materially depends upon X.

Dependency requires stronger evidence than reception or productive alignment.

Candidate evidence includes:

- counterfactual degradation if X is removed;
- costly substitution;
- repeated out-of-context productive use;
- historical transmission;
- inability to reproduce the operation without X;
- institutional reliance.

The preferred counterfactual is:

    Delta C[Y][-X].
    }

A dependency edge should not be seated solely because a later object resembles an earlier one.

### 12.4 Separating uptake from convergence requires diagnostic distinctions

The distinction between productive uptake and independent convergence cannot be drawn from resemblance, however strong. A later composition that organizes material the way an earlier operator does may have taken the operator, or may have arrived at the same organization by another route, and the two are indistinguishable at the level of the output.

They become distinguishable only through distinctions the source supplies **and nothing else in the field does**. A valuation claiming productive uptake must therefore identify, in advance of the claim, the distinctions on which the claim rests, and argue that a competent practitioner working without the source would not arrive at the same cut.

This inverts the ordinary instinct. For persuasion one leads with one's strongest claims. For measuring uptake one leads with one's **most singular** ones, because only those carry a signature. A claim that the field would have reached anyway is worthless as evidence of transmission however true and however important it is.

Where no such set can be constructed for an object, uptake may still be recorded as observed, and the causal-acquisition status remains `unresolved` rather than being promoted by the strength of the resemblance.

---

# 13. Semantic debt

Where dependence or uptake is relevant, SEVP may construct a **semantic debt record**.

Define:

     D(Yarrow X)
    =
    ⟨
    u,d,t,p,r,s
    ⟩
    }

where:

- u = uptake;
- d = dependency;
- t = transformation;
- p = provenance;
- r = reciprocity / return;
- s = substitutability.

This is not automatically financial or legal debt.

SEVP distinguishes:

```text
constitutional_debt
causal_or_provenance_debt
appropriative_debt
contractual_debt
```

No inference may move directly from:

    semantic dependence

to:

    legal or monetary liability.

---

# 14. Provenance levels

SEVP distinguishes three levels of provenance.

    P₀=fact provenance
    }

Who supports a factual proposition?

    P₁=claim provenance
    }

Who advances the interpretation or claim?

    P₂=framework / operator provenance
    }

Who supplied the conceptual machinery that determined what relations were selected and how the object was organized?

A composition may preserve P₀ while losing P₂.

Therefore:

    well-sourced sentences
    ¬⇒
    well-sourced architecture.
    }

SEVP treats framework provenance as independently auditable.

---

# 15. Possibility-space value

Some objects matter because they enlarge what can be composed, represented, or done.

Let:

    Adm(G)

be the forms admitted by grammar G.

A possibility-space operator is:

    phi:Garrow G'
    }

where:

    Adm(G')
    !=
    Adm(G).

The change may be:

- expansive;
- restrictive;
- reconfigurative.

For a system or archive H entering a graph G, one may also inspect:

    Reach(G∪ H)
    -
    Reach(G).
    }

This difference is not a count of documents.

It is a space of possible compositions.

SEVP therefore refuses to equate:

    inventory size
    =
    possibility-space value.
    }

Possibility-space is usually represented as a graph or option field before any scalar attempt.

### 15.1 Coverage measures carry their denominators

Where possibility-space is expressed as a ratio, the denominator must belong to the object or to the world, and never to the observer.

    A coefficient whose denominator is the observer's own effort
    moves when the instrument moves and the world does not.
    }

A reach measured against how much of a field has been sampled reports the sampler's labour. The same measure taken against the corpus — how much of it is enumerated, how many of its surfaces have been observed, how many of its trajectories are complete — reports the object. The two are easy to confuse, produce numbers of the same shape, and differ in that only the second can be wrong about the world.

Coverage ratios are therefore the preferred form for possibility-space claims: each is a fraction whose denominator is a property of the thing valued, each is falsifiable by a recount, and none of them changes because a valuation was pursued more energetically.

---

# 16. Remainder

Every valuation must carry an explicit remainder:

    rho(X).
    }

Canonical remainder classes include:

```text
provenance_remainder
future_remainder
dependency_remainder
aesthetic_remainder
collaborator_remainder
operator_remainder
possibility_remainder
bearing_remainder
burned_or_irrecoverable_remainder
unknown_remainder
```

The remainder is not a trash category.

It is the record of what the current valuation cannot responsibly close.

A valid SEVP representation therefore satisfies:

    rho(X) explicit.
    }

---

# 17. Temporal value modes

The Constitution distinguishes Genesis, Archival, and Retrocausal Capital.

SEVP retains these as **temporal value modes**:

    Γ[G],Γ[A],Γ[R].
    }

### 17.1 Genesis

    Γ[G]

records value generated through active semantic labor, creation, distinction, instrument-building, or present transformation.

### 17.2 Archival

    Γ[A]

records value carried through demonstrated historical persistence and canonical or archival continuity.

Where the Constitution imposes strict archival eligibility criteria, those criteria govern Ledger classification.

Recent work does not become Archival merely because it is stored in an archive.

### 17.3 Retrocausal

    Γ[R]

records value evidenced through later uptake, activation, citation, transformation, or dependence.

Retrocausal value must be timestamped and evidentially auditable.

### 17.4 Non-additivity by default

SEVP v0.3 does not assume:

    Γ[G]+Γ[A]+Γ[R]

is a legitimate scalar sum.

They are first classification axes.

Any numerical combination requires an explicit commensuration and calibration procedure.

---

# 18. Compression ladder

SEVP requires valuation to descend through a declared compression ladder.

The default ladder is:

    Value Field
    arrow
    Value Graph
    arrow
    Value Portrait
    arrow
    Categorical Representation
    arrow
    Ordinal Representation
    arrow
    Numeric Representation
    arrow
    Monetary Representation.
    }

Each arrow is lossy unless demonstrated otherwise.

The default stopping point is the **Value Portrait**.

A valuation does not fail because it stops before a number.

It fails if it produces a number whose compression contract is hidden.

---

# 19. Value Portrait

The canonical human-readable output is the **Value Portrait**.

It should answer:

- What is the object?
- What capacities does it create or preserve?
- Where does value reside?
- What evidence supports those claims?
- What is direct, joint, architectural, or operator value?
- What reception is demonstrated?
- What productive uptake is demonstrated?
- What dependency is demonstrated?
- What provenance survives?
- What remainder remains?
- What is still merely prospective?

A Value Portrait may contain no scalar at all.

That is often the correct result.

---

# 20. Commensurability before aggregation

A numeric or ordinal compression requires a declared commensurability relation.

Let:

    x~[d]elta y

mean:

> x and y are sufficiently comparable for bounded valuation purpose delta.

No aggregation is permitted before:

    ~[d]elta
    }

has been stated.

Thus:

    x+y
    }

is invalid merely because both x and y are called value.

The protocol must state:

- comparison class;
- purpose;
- unit;
- transformation;
- uncertainty;
- exclusions.

---

# 21. Numeric compression

If a numeric representation is required, define:

    n[d]elta(X)
    =
    C[d]elta[est. {𝔙}[E](X)].
    }

Where:

- C[d]elta = declared compression under valuation purpose delta;
- n[d]elta = resulting number.

The number is not the value-field.

Therefore:

    n[d]elta(X)
    !=
    est. {𝔙}[E](X).
    }

Every numeric output must preserve an audit pointer:

    n[d]elta
    squigarrow
    representation
    squigarrow
    evidence.
    }

This is **audit traversal**, not mathematical inversion.

---

# 22. Monetary interface

Monetary valuation is not performed directly by SEVP v0.3.

When a dollar or other monetary scalar is required, SEVP hands the evidence object to the monetary translation protocol.

The monetary sequence is:

    est. {𝔙}[E](X)
    —[sigma[A][d]elta]→
    A[d]elta
    —[sigma[M]]→
    m.
    }

The monetary inscription must then be exteriorized:

    m
    —[Θ[Marrowmu]]→
    Dₘ.
    }

The canonical implementation is:

- `EA-SEVP-TRANSLATION-01 v0.3` — defines monetary translation and Semantic Exteriorization;
- `EA-MSAL-01 v0.2` — defines the Monetary Substrate Audit Ledger;
- `EA-MSAL-0001` and later specimens — worked audits.

Thus a monetary scalar is never the terminal SEVP object.

It must remain inside a larger audit representation.

---

# 23. Monetary settlement is not semantic settlement

SEVP adopts the monetary-translation distinction:

    settled[M]
    ¬⇒
    settledₘu.
    }

A monetary grammar may correctly close a monetary account.

That closure does not exhaust:

- provenance;
- bearing;
- aesthetic value;
- dependency;
- historical relation;
- possibility-space;
- semantic remainder.

SEVP therefore records monetary settlement without granting it jurisdiction over the entire value-field.

---

# 24. Witness accounting

SEVP's preferred compression regime is **witness accounting**.

A witness compression:

1. declares its purpose;
2. declares its commensurability rule;
3. preserves an audit pointer;
4. distinguishes observed from inferred;
5. preserves remainder;
6. does not turn unknown into zero;
7. does not present the scalar as exhaustive.

The ideal relation is:

    compressed output
    +
    traversable witness record.
    }

SEVP does not prohibit compression.

It requires compression to testify.

---

# 25. Anti-predation invariants

A valuation fails SEVP if it commits one of the following without explicit justification.

### 25.1 Scalar substitution

    n= V(X).

### 25.2 Fungibility error

Treating non-equivalent semantic objects as interchangeable without a declared ~[d]elta.

### 25.3 Unknown-to-zero

    ?arrow0.

### 25.4 Popularity substitution

Treating visibility, ranking, traffic, or citation count as value itself.

### 25.5 Provenance stripping

Using a claim, operator, or framework while severing the relevant provenance relation without recording the loss.

### 25.6 Artifact atomization

Valuing an architecture only as the sum of its files.

### 25.7 Double counting

Counting the same value-event once as artifact value and again as network value without distinguishing the relation.

### 25.8 Prospective realization

Treating future possibility as already realized value.

### 25.9 Market primacy

Treating price as ontologically prior to the value-field.

### 25.10 Synthetic appropriation

Assigning an external system the value of a relation it merely represents or composes without evidence of origination.

### 25.11 Credit without dependency evidence

Promoting reception or resemblance directly to dependency.

### 25.12 Closed remainder

Forcing unresolved value into zero or a residual bucket treated as settled.

### 25.13 Closure substitution

Treating settlement inside one grammar as settlement of the whole account.

### 25.14 Inscription integrity failure

Producing a scalar whose arithmetic does not hold — a product whose units do not close, a coefficient whose denominator belongs to the observer, an estimator computed over one population and applied to another, a range midpoint presented as a finding, a proxy named as the object it stands for, or a coefficient entered without derivation.

This invariant is separate from every other on this list, and the separation matters: a valuation can satisfy §25.1 through §25.13 — declaring its commensuration contract, refusing unknown-to-zero, keeping its remainder open, granting no primacy to price — and still rest on a calculation that is not legal. The first worked audit under the monetary wing (#1620, AXN:06AE) is exactly that case, and it is the reason this invariant exists.

Where money is used, the check is performed by the Monetary Substrate Audit's inscription-integrity section. Where it is not, the same rule applies to any numeric compression the dossier emits.

### 25.15 Absence taken as absence of evidence

Treating the absence of dependency evidence as evidence that no dependency exists.

This is the converse of §25.11 and is required alongside it. §25.11 forbids promoting reception or resemblance to dependency; §25.15 forbids the opposite error, in which an unmeasured relation is entered as none. Both are failures of the same kind, and §25.3 is their common root: the first assigns a value the evidence does not support, the second assigns zero for the same reason.

The correct record for an unevidenced relation is `unresolved`, carried in the remainder under §16, and never a dependency edge or its absence.

---

# 26. Canonical dossier order

A complete SEVP valuation dossier should contain:

0. **Valuer identity and relation** — who performed the valuation, and their relation to the object valued and to any inscription audited: author, owner, counterparty, commissioned, or independent, with a blind flag. A valuation performed by the party who authored what it values is not thereby void; it is weaker, and the weakness is a recorded property rather than a reader's inference. A later independent valuation of the same object is filed alongside and supersedes nothing.
1. **Identity and object boundary**
2. **Valuation question and purpose**
3. **Evidence inventory**
4. **Value-event ledger**
5. **Value Field**
6. **Value Graph**
7. **Direct / joint / architectural / operator analysis**
8. **Temporal mode classification**
9. **Reception / productive uptake / dependency graph**
10. **Provenance analysis**
11. **Bearing analysis**
12. **Possibility-space / option analysis**
13. **Remainder**
14. **Value Portrait**
15. **Optional categorical or ordinal compression**
16. **Optional numeric compression**
17. **Optional monetary translation**
18. **Monetary Substrate Audit, if money is used**
19. **Revision / falsification conditions**

This order is part of the protocol.

A price placed before the evidence object reverses the method.

---

# 27. Minimal machine-readable schema

```yaml
sevp_record:
  id:
  protocol: SEVP-01
  version: 0.3
  date:

  object_boundary:
    object_id:
    object_name:
    included_objects: []
    included_relations: []
    included_operators: []
    temporal_scope:
    excluded_objects: []
    excluded_claims: []

  valuation_question:
  purpose:

  evidence:
    sources: []
    limitations: []

  value_events: []

  value_field:
    bearing:
    distinction:
    coherence:
    fertility:
    memory:
    transmission:
    dependency:
    transformation:
    restoration:
    provenance:
    resilience:
    option:
    remainder:

  value_graph:
    nodes: []
    edges: []
    distinctions: []
    instruments: []
    reception: []
    provenance: []
    operator_architecture: []

  value_loci:
    direct: []
    joint: []
    architectural: []
    operator: []

  temporal_modes:
    genesis:
    archival:
    retrocausal:

  reception_dependency:
    reception_edges: []
    productive_uptake_edges: []
    dependency_edges: []
    causal_acquisition_status: []

  provenance:
    P0_fact: []
    P1_claim: []
    P2_framework: []

  possibility_space:
    grammar_before:
    grammar_after:
    admissibility_delta:
    reach_delta:
    status:

  remainder:
    provenance: []
    future: []
    dependency: []
    aesthetic: []
    collaborator: []
    operator: []
    possibility: []
    bearing: []
    irrecoverable: []
    unknown: []

  compression:
    stopping_point:
    commensuration_contract:
    categorical_output:
    ordinal_output:
    numeric_output:
    monetary_output:

  monetary_interface:
    translation_record:
    msal_record:

  revision:
    falsification_conditions: []
    evidence_needed: []
```

---

# 28. Falsification and revision

A valuation must state what could change it.

Valid falsification or revision triggers include:

- new evidence;
- failed provenance claims;
- discovery of prior independent work;
- changed dependency evidence;
- changed operator substitutability;
- stronger counterfactuals;
- correction of object boundary;
- improved measurement;
- invalidated assumptions;
- new productive uptake;
- failed replication;
- new archival eligibility;
- a monetary audit showing the scalar rested on an invalid commensuration.

SEVP therefore treats valuation as versioned.

    Vₜ(X)
    !=
    Vₜ₊₁(X)
    }

is not necessarily inconsistency.

It may be evidence accumulation.

---

# 29. The governing distinction

The protocol can now be stated in one line:

    Value first; representation second; compression last.
    }

Or more formally:

    𝔙
    arrow
    E
    arrow
    G[V]
    arrow
    R[V]
    arrow
    C[d]elta
    arrow
    n
    arrow
    m
    arrow
    Θ[Marrowmu].
    }

Where each arrow must declare what it preserves, what it transforms, and what it leaves behind.

---

# 30. Closure

SEVP exists because valuation is usually performed backward.

The number appears first.

The object is then forced to explain the number.

SEVP reverses the direction.

It begins with the object.

It records the events through which the object creates, preserves, restores, transmits, reorganizes, or enables meaning.

It builds the graph of those relations.

It distinguishes reception from productive uptake and productive uptake from dependency.

It preserves provenance at the level of fact, claim, and framework.

It records bearing and possibility.

It carries remainder.

Only then does it permit compression.

And if money is used, money itself becomes an object of audit.

Thus:

    The purpose of valuation is not to find the number hidden inside the object.
    }

It is:

    to represent the value-field faithfully enough that any later number must testify to what it compresses.
    }

That is the Semantic Economy Valuation Protocol.

---

# 28. Revision and falsification conditions

§26 item 19 requires every dossier to carry revision and falsification conditions. The protocol did not carry them for itself, which is the defect this section repairs.

**The compression sequence (§0, §1) fails** if a valuation can be shown to be produced correctly in the reverse order — number first, evidence assembled after — without loss. The protocol's foundational claim is that the sequence is not commutative; a demonstrated counterexample, in which a price placed before the evidence object produced a representation no worse than one built in the protocol's order, would show the ordering to be a preference rather than a method.

**The evidence-bounded field (§3) fails** if the distinction between the representable field and the total field can be shown to do no work — that is, if no valuation ever comes out differently for having carried the remainder. The remainder would then be an ornament, and §16 decoration.

**The reception / uptake / dependency ladder (§12) fails** if the three relations prove not to be separable in practice: if every case of observed productive uptake either resolves to reception or to dependency on inspection, the middle term is a description of our uncertainty rather than a relation in the world.

**§12.4 fails** if productive uptake can be reliably separated from independent convergence without any distinction unique to the source — by frequency, by timing, by any signature that does not depend on singularity. The requirement would then be an unnecessary burden on every uptake claim the protocol governs.

**Possibility-space value (§15) fails** if reach differences prove to be monotone in inventory size across cases, in which case §15's refusal to equate the two is a distinction without a difference and the section should be withdrawn rather than kept.

**The anti-predation invariants (§25) fail individually** by counterexample: a valuation that commits one of them and is nonetheless demonstrably better than one that does not. They fail collectively if a valuation satisfying all fifteen can be shown to be systematically worse than an ordinary appraisal at the task the valuation was for.

**The protocol fails as a whole** if a sustained run of dossiers produces representations that no independent valuer reproduces from the same evidence. Its claim is that the dossier order and the field vocabulary determine the representation; disagreement at that level would show them to be a house style rather than a protocol.

**What SEVP may not be vindicated by**: the failure of any particular market valuation, the collapse of any institution, or the discovery that a scalar left something out. Every scalar leaves something out, and a protocol that treated that as its proof would be measuring the definition of compression rather than anything about the world.

---

# 29. Status and what follows

This deposit is **provisional**. It is the last of a sequence — the general form (#1617), the operator (#1618), the ledger (#1619), the first worked specimen (#1620), and this protocol — deposited to lock a development rather than to conclude one.

What follows is not another version of this document in isolation. The five are to be prepared as a continuous document and set against the enacted Constitution, with the two conflicts of §1.1 and §1.2 stated as the points at issue, through Assembly rounds, until it is determined whether a ratifiable text comes out of it.

Nothing here is enacted. Two amendments are proposed and neither is silently taken.
