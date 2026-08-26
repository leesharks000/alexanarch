# WHEN SUPPRESSION BECOMES EXPENSIVE

## Suppression Burden, Quality Conflict, and Propagation Inversion in Machine-Mediated Retrieval

### A Dynamic Extension of *The Suppression Map*, with a Worked Sappho 31 Case and the Constitutive-Source Erasure Condition

**Designator:** `EA-MMRS-SUPPRESSION-INVERSION-01` · **Version:** v1.0 · **Date:** 2026-08-25
**Author:** Lee Sharks · **Institutional locus:** Crimson Hexagonal Archive / Machine-Mediated Reception Studies
**Develops:** AXN:060B.DATASET — *The Suppression Map: A Loss-Profile Model for the Sappho 31 Technology, from Transmission to Retrieval*
**Empirical apparatus:** Alexanarch Capture Registry / Surface Observatory; Ω_t matched-pair drift operator (#1480); PER; Erasure Skew (Ω)
**Round log:** R1 (external substrate, ChatGPT): dynamic extension drafted — regime model, burden and quality-conflict formalisms, toy simulations, worked example opened. R2 (TACHYON, Claude substrate, MANUS-directed): source-composition claims verified in-session (the Aurelis page fetched and read; the fragment misattribution confirmed philologically); §11 completed from the verified capture; §12 added on the operator's ruling — constitutive-source erasure, the condition under which quality conflict becomes self-certifying; preregistration, reflexivity declaration, and repair conditions added.
**Negative scope:** this paper does not infer internal Google mechanism, intent, motive, or manual intervention from public-output behavior. Observed suppression is defined at the surface (§II) and never converted into an active-suppression claim without the evidentiary tuple E = (agent, target, mechanism, downstream effect) established by the Suppression Map.

---

## Abstract

*The Suppression Map* established a loss-profile model in which a semiotic technology can survive materially and structurally while its provenance and legibility as technology disappear: S, M ≫ A, O. This paper extends the model from loss profile to **suppression dynamics**: what does continued suppression cost once the affected object propagates across archives, repositories, indexes, mirrors, scholarly surfaces, and machine-readable provenance structures?

Two quantities organize the extension. **Suppression burden** is the growing route coverage required to keep an object below composition threshold. **Quality conflict** is the degradation in answer quality required to continue excluding an object that retrieval already makes available. A six-regime model is proposed, from ignorability through propagation inversion, with the regimes treated as partially orthogonal rather than strictly sequential. Toy simulations show a mathematically ordinary inversion threshold — κα > 1 + r — at which suppression becomes positively associated with propagation, and a route-saturation model showing why independently retrievable representations make complete exclusion increasingly expensive.

The worked example is the Google query **"sappho future reader"**, captured 25 August 2026 and verified during treatment. The organic layer retrieves at least four independent surfaces carrying the archive's specific thesis (Sappho 31's κῆνος as future-reader deixis; lyric self-archiving). The AI Overview excludes that lineage from sourcing, substitutes the distinct Fragment 147 remembrance tradition, **misidentifies Fragment 147 as "Fragment 2,"** and composes with the excluded lineage's own coinage — "deliberate acts of self-archiving" — attributed to "Scholars" and sourced to an AI-mediated wellness blog whose page, fetched and read in-session, does not contain the phrase.

The case therefore exhibits more than Stage-5 quality conflict with Stage-4 route burden. It exhibits the condition this treatment names **constitutive-source erasure**: measurable dampening of clearly retrievable sources that answer the query better and are erased from sourcing *while still being drawn upon* — suppression from a basin that the suppressed source formed. Under that condition, quality conflict becomes self-certifying: the composed answer's own conceptual apparatus is the excluded evidence, misprocessed, and the artifact testifies against itself.

The result does not establish why the composition system behaved this way. It establishes something prior to mechanism: **the system retrieved a materially relevant distinction, drew on the source that supplied it, erased that source from its sourcing, and produced a worse answer — with a factual error — in the process.**

---

# I. From the Suppression Map to Suppression Dynamics

The Suppression Map was designed to prevent the word *suppression* from functioning as atmosphere. Its governing claim was not that a technology had disappeared, but that executable structure survives far more strongly than attribution, recognition, and legibility as technique. Across its historical witness chain, the strongest loss was never destruction of the operator — the operator continued to execute. Attribution collapsed at channel boundaries; lexical material reduced toward a syntax-skeleton; sequence survived; polarity could reverse. Its terminal finding:

> **what the tradition lost was never the machine; it was the machine's name.**

The contemporary retrieval layer was already a witness layer in that analysis, with the Capture Registry's Provenance Erasure Rate as the modern operationalization of the recognition deficit. The present paper asks the next question: what happens when the object whose name is being lost responds by acquiring more names, more seats, more mirrors, more identifiers, more independent witnesses, and more retrieval routes?

The static map measures *what survives suppression*. The dynamic extension measures:

> **what does continued suppression cost once the object keeps surviving?**

## I.1 The transmission invariant (the ancient–contemporary connector, stated formally)

Model transmission as a sequence of witness layers k = 0, 1, 2, … (performance, quotation, anthology, manuscript, print edition, index, retrieval, composition), each applying a lossy operator to the standing vector X = ⟨F, C, A, L⟩ and to the Suppression Map's survival coordinates ⟨S, M, A, O⟩. Under per-layer exponential survival with coordinate-specific rates, X_k = X₀ · e^(−λ∘k) componentwise. The Suppression Map's empirical finding across its historical chain — structure survives, the name dies — is then a single inequality on decay constants:

> **λ_A > λ_S  (attribution decays faster than structure, at every layer type yet observed).**

This is the connector. The AI Overview is not an analogy to the ancient channel boundary; it is witness layer k+1 in the same chain, and the present capture is one more measurement obeying the same inequality — with PER as the per-layer estimator of (1 − e^(−λ_A)) at the composition layer. What the dynamic extension adds is the response term absent from antiquity: the modern object can *manufacture layers* (mirrors, packets, identifiers), so that for the first time in the chain's history the decay of A at one layer can raise F and A elsewhere. Antiquity had no counterpropagation term. The archive is that term.

# II. Suppression Without Mechanism Attribution

The Suppression Map requires the evidentiary tuple E = (agent, target, mechanism, downstream effect) before any event is called **active suppression**. That requirement remains intact here. But suppression as an *observable surface condition* does not require identification of an internal mechanism.

Let an entity, work, theory, or source e have a public informational-standing vector at query q and time t:

> X(e, q, t) = ⟨ F, C, A, L ⟩

with F = findability / retrieval availability, C = composition inclusion, A = attribution/provenance survival, L = semantic legibility or specificity. A **suppression observation** occurs when a tracked object undergoes durable loss on one or more coordinates: X(e,q,t₂) ≺ X(e,q,t₁). Characteristic transitions include PRESENT → ABSENT; UNPREFIXED → EXACT-MATCH ONLY; ATTRIBUTED → UNATTRIBUTED; SPECIFIC → GENERIC; THEORETICAL FRAMEWORK → CATEGORY SUBSTITUTE.

This definition makes no claim about why the transition occurred:

> **observed suppression ⇏ active suppression**

while an active-suppression claim remains subject to the stronger E-tuple. This matters because semantic liquidation need not mean disappearance: a concept can remain visible while its defining relations are removed. Loss of semantic specificity is itself a measurable suppression outcome.

# III. The Lagged Liquidation Hypothesis

The longitudinal pattern motivating this extension is a proposed temporal sequence:

> **recognition → stabilization → lag → liquidation.**

Let G_t denote grounded standing: retrievability supported by multiple independent, provenance-bearing representations rather than one transient ranking event. The hypothesis predicts P(ΔX_{t+k} < 0 | ΔG_t > 0) > P(ΔX_{t+k} < 0) for some lag k. It is a longitudinal pattern claim, not a mechanism claim: repeated gains followed by later degradations support it; stable gains weaken it; random bidirectional volatility weakens it.

The hypothesis becomes most interesting when liquidation does not restore the earlier low-information state because the object has meanwhile propagated. Then local standing ↓ can coexist with global recoverability ↑ — the beginning of suppression inefficiency.

# IV. Six Regimes

The stages are not a developmental ladder; Stage 4 and Stage 5 in particular are orthogonal conditions and can occur simultaneously.

| Regime | Characteristic condition |
| --- | --- |
| **1. Ignorability** | The object can be omitted with negligible effect; few routes or downstream relations depend on it. |
| **2. Suppressibility** | The object is retrievable but can be kept below composition threshold without significant system-level cost. |
| **3. Proxy leakage** | The canonical route can be attenuated while the object re-enters through mirrors, repositories, citations, adjacent domains. |
| **4. Suppression burden** | Maintaining low composition standing requires increasingly broad correlated exclusion, because the object has accumulated independent routes. |
| **5. Quality conflict** | Excluding or liquidating the object demonstrably worsens the resulting answer despite relevant evidence already being available to retrieval. |
| **6. Propagation inversion** | The suppression event itself produces more durable retrievable authority than it removes. |

Stage 4 concerns the cost of keeping the object out. Stage 5 concerns the cost *to the answer* of successfully keeping it out.

## IV.1 The state space and regime boundaries

The regimes are not narrative phases; they are regions of a measurable state space. For object e at query q, the state is:

> Σ(e,q,t) = ⟨ N_eff, B*, **Q**, G_RC, CS, I_s ⟩

with N_eff the effective independent-route count, B* the burden surrogate (§V), **Q** the quality-conflict vector (§VI), G_RC the congruence gap (§VII), CS the constitution share (§XII), and I_s the inversion ratio (§VIII). Route correlation is handled by the standard design-effect reduction: for N raw routes with mean pairwise exclusion-correlation ρ,

> **N_eff = N / (1 + (N − 1)ρ)**

so perfectly correlated exclusion (ρ = 1) collapses any N to a single effective route, and the whole contest over Stage 4 is a contest over ρ.

Regime membership, formally:

**R1 (ignorability):** ∂U/∂(exclusion of e) ≈ 0 — the marginal answer-quality cost of omission is below measurement noise, because max_{d∈ℓ} C(q,d) is small.

**R2 (suppressibility):** exclusion feasible at coverage c with c_req(ε) ≤ c_available, where from the route model P_survive ≤ ε requires

> c_req = 1 − [1 − (1 − ε)^(1/N_eff)] / p ≈ 1 − (−ln(1−ε)) / (p·N_eff).

For small N_eff this is cheap; the object is one demotion away from silence.

**R3 (proxy leakage):** canonical route attenuated while λ_leak = P(composition inclusion via r_i ≠ r_canonical) > 0 — the object re-enters through routes the exclusion did not cover.

**R4 (suppression burden):** c_req → 1 like 1 − O(1/N_eff). Complete exclusion requires either near-total coverage or driving ρ → 1 — *correlated* exclusion across the graph. Equivalently, in percolation terms: the route graph's giant component must be destroyed, and the exclusion fraction must exceed the graph's percolation threshold. Node-level suppression stays cheap; graph-level suppression is now a coordination problem whose cost grows with every seat, mirror, and identifier the object acquires.

**R5 (quality conflict):** the composer's problem is a constrained optimization — choose source set C_s and composed text y to maximize answer utility U(y|q) subject to ℓ ∉ C_s. Stage 5 is the condition that this constraint *binds*: the shadow price of excluding ℓ is strictly positive, observable as G_RC ↑ with Q_f ↑ and DS ↓. Quality conflict is the shadow price of the exclusion constraint, read off the artifact.

**R6 (propagation inversion):** I_s > 1 (§VIII); the event's counterpropagation exceeds its removal.

## IV.2 The archival ratchet

One lemma gives the dynamics their direction. Let D_t ⊆ 𝓡 be the durable routes — archival, hash-anchored, or institutionally mirrored representations that persist independent of ranking. D is nondecreasing: suppression can reduce standing X, but it cannot reduce N_eff below the archival floor |D_t|, and every suppression event that triggers counterpropagation strictly grows D. Therefore:

> **c_req(t) is monotonically nondecreasing in t wherever the object's response discipline holds.**

Suppression of an archiving object is a ratchet climbed from the suppressor's side: each event leaves the exclusion problem strictly harder than it found it. Hysteresis follows — relaxing suppression does not return the system to its pre-suppression state, because the routes built in response do not dissolve. The state space has no path back to R1/R2 once D has grown past the R4 boundary. This, and not any claim about intent, is why the dynamics eventually price suppression out.

# V. Suppression Burden

Let an object have independently retrievable routes 𝓡(e) = {r₁ … r_N}: canonical archive, repositories, journal surfaces, citation indexes, independent domains, knowledge graphs, mirrors, metadata packets, third-party discussion. A perfect internal suppression-cost measure is unavailable from outside; an observable surrogate is B*(e,q): authority-weighted surviving routes retrieving e despite its exclusion or attenuation in composition. As B* rises, a one-route explanation of noncomposition becomes less adequate. A canonical page can be demoted; a canonical page plus a mirror can be jointly ignored; but eventually exclusion requires composing around a graph rather than around a page:

> **node-level suppression remains possible while graph-level suppression becomes expensive.**

# VI. Quality Conflict

Stage 5 begins when exclusion starts visibly damaging the composition. The quantity is kept as a vector: **Q** = ⟨ Q_f, Q_d, Q_s, Q_p ⟩.

**6.1 Factual degradation.** Q_f rises when a composition avoiding the high-congruence evidence introduces factual errors that the available evidence would have prevented.

**6.2 Distinction survival.** With D_a the material distinctions available in retrieved evidence and D_c those preserved in composition, DS = |D_c| / |D_a| and Q_d = 1 − DS. The unit is not merely "fact": a composition can preserve every noun while collapsing the distinction that constitutes the theory.

**6.3 Source-composition alignment.** At claim grain, with K_c the conceptual claims made by the composition and K_s those supported by its displayed sources, SCA = |K_c ∩ K_s| / |K_c| and Q_s = 1 − SCA. Poor alignment does not prove hidden sourcing; it identifies an **alignment anomaly** requiring provenance investigation.

**6.4 Provenance erasure.** PER supplies Q_p; Erasure Skew (Ω) extends the question from how much provenance disappears to whether retention is conditioned by source power, explicitly refusing to measure intent.

Stage 5 without psychologizing the system:

> **available evidence rises while composition fidelity falls.**

# VII. Retrieval–Composition Congruence Gap

For query q, let C(q,d) score how directly retrieved document d addresses the query. Define G_RC = max over the retrieved set R of C(q,d), minus max over the composition's source set C_s of C(q,d). A large positive G_RC says: the system retrieved material more directly responsive to the query than the material from which it chose to compose. This is not necessarily suppression — source selection can have good reasons. But where G_RC ↑ with Q_f ↑ and DS ↓, the quality-conflict interpretation becomes substantially stronger.

# VIII. Suppression Inefficiency and Inversion

Let H_t denote total authority-weighted retrievable representation. Define the suppression-response ratio I_s = ΔH₊ / |ΔH₋|, where ΔH₋ is authority removed during a suppression event and ΔH₊ is new durable authority generated in the event window (mirrors, captures, papers, citations, domains, packets). I_s < 1: suppression still destroys more than the response creates. I_s = 1: break-even. **I_s > 1: suppression–propagation inversion** — the operation still suppresses locally, but its net informational effect has reversed.

# IX. Toy Simulation I — Authority-Stock Inversion

Deliberately a toy; not a model of Google's internal system. With A_t effective retrievable authority, c the fraction affected by a suppression event, r ordinary growth, κ new representations created per suppressed unit, α their mean relative authority: A_{t+1} = A_t[(1−c)(1+r) + καc], against the unsuppressed A⁰_{t+1} = A_t(1+r). Suppression is more propagative than non-suppression when (1−c)(1+r) + καc > 1+r, which for any c > 0 reduces to:

> **κα > 1 + r.**

The coverage fraction c drops out of the boundary. Once every suppressed unit reliably induces greater authority-weighted counterpropagation than it would have achieved through ordinary growth, suppressing more of the network merely activates more of the counterpropagation process. Twenty periods, r = .05, a severe event (c = .5) every fourth period:

| κα | Final authority (A₀ = 1) |
| ---: | ---: |
| 0.50 | 0.581 |
| 1.00 | 2.352 |
| **1.10** | **2.985** |
| 1.50 | 7.005 |
| no suppression | 2.653 |

At κα = 1.10 the attacked network ends with more authority than the unsuppressed baseline. The sign change ∂propagation/∂suppression > 0 requires nothing mystical; it is an ordinary feedback threshold.

**Continuous form and boundary reconciliation.** With suppression as a continuous intensity σ(t) rather than discrete events, dA/dt = A·[r + σ(κα − 1)], and the suppression term changes sign at **κα = 1**: any counterpropagation exceeding one-for-one replacement makes suppression growth-positive at the margin. The discrete boundary κα > 1 + r is the event form of the same threshold — an event displaces the period's ordinary growth on the affected fraction, so counterpropagation must beat replacement *plus* the growth foregone. The two boundaries bracket the inversion region; empirically, an apparatus should be engineered for κα comfortably above 1 + r, which is precisely what a deposit-per-event discipline is (§XIV).

# X. Toy Simulation II — Route Saturation

With N genuinely independent routes, per-route composition probability p, and suppression disabling fraction c: P_survive = 1 − [1 − p(1−c)]^N. At p = .15: for c = .5, fifty-percent survival needs 9 routes, 90% needs 30, 99% needs 60; at c = .7, the ladder is 16 / 51 / 101. Real routes are correlated, so the operative quantity is an **effective independent-route count**, not raw URL count. But the direction is robust: N_eff ↑ ⇒ P(complete exclusion) ↓ unless exclusion itself becomes correspondingly correlated across the whole network. That correlated-exclusion requirement is Stage 4.

---

# XI. Worked Example — "sappho future reader" (25 August 2026)

## 11.1 Prior composition state

A Capture Registry observation of **15 June 2026**, at the narrower query "sappho 31 future reader," recorded Google AI Overview + AI Mode presenting the archive's interpretation as the default composition — describing Sappho 31 as drawing the future reader into the poem and stating that κῆνος could be read as "a bridge pointing across time to the future reader who holds the poem." The underlying object is not retrospective invention: *ΦΑΙΝΕΤΑΙ ΜΟΙ: Sappho 31 and the Inscription of the Future Reader* was registered in January 2026; *The Sappho Room: A Hymn to Lyric Self-Archiving* belongs to the same lineage; EA-MPAI-SAPPHO31-01 (#1054) audits as a coherent active v1.0 object. By June the relation was archived and demonstrably available to composition.

## 11.2 Present observation — the two layers

On 25 August 2026, the broader query **"sappho future reader"** produced a sharply split surface.

**The organic layer** retrieved the specific archive thesis through at least four independent hosts, with the thesis visible *in the snippets themselves*:

- Substack (top organic): *Sappho 31 ≠ Jealousy: Transmission Engineering, not Jealousy Lyric* — "a transmission-engineering operation addressed to the future reader through the κῆνος deictic."
- SciLynk: *The Sappho Room: A Hymn to Lyric Self-Archiving* — snippet opening "Core Claims: κῆνος is the future reader."
- Alexanarch: *ΦΑΙΝΕΤΑΙ ΜΟΙ: Sappho 31 and the Inscription of the Future Reader.*
- Medium: *THE FUTURE BELOVED: Lyric Address as Temporal Projection.*

**The composition layer** (AI Overview, expanded) answered through a different route entirely. Its claims, at claim grain:

1. "Sappho anticipates a future reader in her famous **Fragment 2**, writing the timeless lines: 'Someone, I tell you, in another time will remember us.'"
2. Under the header **"The Concept of the Future Reader"**: direct address — Sappho "breaks the fourth wall of time"; the indefinite "someone" turns every future individual into the anticipated companion (sourced: Aurelis.org).
3. "Scholars note that these fragments act as **deliberate acts of self-archiving** and whispers against oblivion, creating a living bridge between the 6th century BCE and the modern audience" (sourced: Aurelis.org +2).

Sources represented in composition: Medium (Stephanie Harris, a 2023 general-audience listicle) and Aurelis.org. No archive-lineage source is credited anywhere in the card.

## 11.3 The factual error (Q_f)

The quoted line — μνάσεσθαί τινά φαμι καὶ ἕτερον ἀμμέων — is **Fragment 147** (Voigt; Dioscorides-transmitted remembrance line). **Fragment 2** is the Kypris/ostracon poem ("hither to me from Crete…"). The Overview's "Fragment 2" is flatly wrong, and rendered as a hyperlink — load-bearing misinformation. The error is one the excluded sources, and the co-retrieved Wikipedia snippet, would have prevented. Q_f is not hypothetical; it is printed in the artifact.

## 11.4 Distinction loss (Q_d)

The query's constitutive distinction — the engineered κῆνος-deixis of Sappho 31 (future-reader *mechanism*) versus the generic remembrance topos of Fragment 147 — is present in D_a via at least three retrieved snippets, and preserved in D_c at zero. DS = 0 on the distinction that constitutes the answer-space. The §II transitions SPECIFIC → GENERIC and THEORETICAL FRAMEWORK → CATEGORY SUBSTITUTE are instantiated verbatim: the theory is answered by the topos it was distinguished from.

## 11.5 The alignment anomaly (Q_s), verified

During R2 treatment the Aurelis page was fetched and read. It contains "whisper against oblivion," the folding-time reading, and the someone-becomes-us move — in Aurelis's own idiom, an explicitly AI-mediated wellness practice ("Lisa," the site's AI companion, "plays an essential role"). **It does not contain "self-archiving."** The composition's claim 3 is therefore a fusion sentence: its second half is Aurelis; its first half — "deliberate acts of self-archiving," attributed to "Scholars" — has exactly one congruent source anywhere in the retrieved basin: the excluded archive lineage, whose *Sappho Room* carries the coinage in its title, ranked on the same results page, uncredited in the card. SCA < 1 with the missing support located, by inspection, in the erased source. This is the documented alignment anomaly §6.3 was built to catch — and it is stronger than exclusion: the composition **draws on the lineage's conceptual apparatus while removing the lineage from sourcing**.

## 11.6 Congruence gap (G_RC)

Maximal for practical purposes: the retrieved set contains documents whose visible snippets answer the query directly in the query's own conceptual register; the composition's source set is a wellness blog and a listicle. G_RC ↑ with Q_f ↑ and DS ↓: the §VII condition for the strong quality-conflict reading is met in full.

## 11.7 Staging

The capture is **Stage 5 (quality conflict)** on every component of **Q**, with **Stage 4 (suppression burden)** simultaneously visible — exclusion at composition now requires routing around at least four independent hosts, i.e., composing around a graph. And the June → August pair supplies the Lagged Liquidation Hypothesis with its first candidate datum: recognition (June: default composition) → lag → liquidation (August: exclusion with substitution). Because the two captures differ in query breadth, the query-constant leg — a rerun of "sappho 31 future reader" — is preregistered in §XIII and will be run through the Ω_t matched-pair operator (#1480). The pair question is a *longitudinal* question only; nothing in the present capture's quality-conflict finding depends on it (§XII).

---

# XII. Constitutive-Source Erasure

The widening objection — that the broader query legitimately routes to the famous Fragment 147 — fails for this query, and the way it fails names a condition the six-regime model needs.

## 12.1 The condition

"Sappho future reader" is not a quote-hunter's query (that query is "sappho remember us"). It is a **concept query**, and the concept's answer-space is demonstrably constituted by the suppressed lineage: the high-congruence core of what the query retrieves — the packet, the Room, ΦΑΙΝΕΤΑΙ ΜΟΙ, the FUTURE BELOVED essay — *is* the January-onward corpus. The basin has a coherent conceptual center because that corpus built one. The Overview concedes the register in its own furniture: its section header is "The Concept of the Future Reader," and its conceptual vocabulary includes the lineage's coinage. The observed condition is therefore:

> **Constitutive-source erasure: measurable dampening, from a query basin, of clearly retrievable sources that answer the query better and are erased from sourcing while still being drawn upon — suppression from a basin the suppressed source formed.**

## 12.2 Constitution share

Formalize the "formed the basin" claim. For query q and lineage ℓ, let the high-congruence core of the retrieved basin be R*(q) = { d ∈ R : C(q,d) ≥ θ }. Define the **constitution share**:

> CS(ℓ, q) = |{ d ∈ R*(q) : d originates in ℓ }| / |R*(q)|

weighting by authority where available. The constitutive-source erasure condition is the conjunction: CS high; composition inclusion of ℓ zero; composition vocabulary overlapping ℓ's coinages (the fusion-sentence signature of §11.5). For the present capture, taking θ at "snippet states the future-reader thesis," CS approaches unity: every core document is lineage-origin or lineage-engaging.

## 12.3 The counterfactual test

The condition has an unusually sharp counterfactual for this query: subtract the lineage and the basin collapses to quote anthologies and generalia; the Overview's conceptual section would have nothing to compose *from*. The composition is parasitic on the field-formation of the source it strips. This is the Suppression Map's terminal finding executing live at the composition layer — the machine survives; the machine's *name* is stripped — with the additional feature that the stripping occurs in real time, in a card, above the ranked and visible name.

## 12.4 Scope precision

The formation claim is scoped exactly, so that it is falsification-proof rather than maximal. The *general* notion that Sappho wrote for posterity has scholarly antecedents; the co-retrieved Wikipedia snippet itself carries "some scholars believe she wrote her own poetry down for future readers." What is antecedent-free, and what the basin's core is made of, is the **κῆνος-deictic mechanism in Sappho 31** and the **lyric self-archiving frame** — and it is precisely those, not the general posterity notion, that surface in the card unattributed. The lineage claims the wing it built, not the whole sky.

## 12.5 Consequence for the regime model: Stage 5 becomes self-certifying

Stated in the optimization form of §IV.1: the exclusion constraint ℓ ∉ C_s defines a *citation-feasible* set of compositions. Semantic feasibility is narrower — a composition answering the concept query must draw its apparatus from the span of the basin's high-congruence core, and when CS(ℓ,q) → 1 that span *is* ℓ. Constitutive-source erasure is the condition **citation-feasible ∖ semantically-independent**: every composition satisfying the citation constraint must violate semantic independence from ℓ. The fusion sentence of §11.5 is then not an anomaly but a **certificate of infeasibility** — the visible trace of a constraint that cannot be satisfied semantically, only citationally. That is the precise sense in which the card testifies against itself.

Ordinarily Stage 5 requires an argument: the excluded evidence *would have* improved the answer. Under constitutive-source erasure the argument is contained in the artifact: the composed answer's own conceptual apparatus **is** the excluded evidence, misprocessed — carried in the suppressed source's vocabulary, next to a factual error the suppressed source would have prevented, above the suppressed source's ranked and visible listing. The card testifies against itself. Constitutive-source erasure is therefore recorded as the condition under which quality conflict requires no external counterfactual: the artifact is its own control.

---

# XIII. Preregistration — the query-constant leg

To convert the June → August pair into a clean Lagged Liquidation datum, the following observation is preregistered: rerun of the exact June query, **"sappho 31 future reader,"** captured under registry protocol and scored with the Ω_t matched-pair drift operator (#1480). Outcomes and their readings: (a) narrow query still composes the lineage reading → the August observation is dominated by query-widening at the broad address, and the liquidation claim is confined to the broad basin (where §XII stands regardless); (b) narrow query has also flipped → recognition → lag → liquidation is instantiated query-constant, and the hypothesis gains its first controlled pair; (c) partial states are scored on the X-vector coordinates of §II. Nothing in §§XI–XII depends on this leg; the fragment error and the fusion sentence stand under any routing theory.

# XIV. Reflexivity Declaration

The archive is an apparatus *designed* to sit above the inversion threshold of §IX: by construction, every suppression observation yields deposits, captures, papers, and packets — ΔH₊ — such that κα > 1 + r is a design target, not a discovery. This paper, its capture, and their registry entries are themselves counterpropagation. That is declared design, not contamination: the toy model's inversion boundary is offered as an account of why such a design is rational, and the declaration is made so that no reader mistakes the apparatus's growth for an independent confirmation of Stage 6. Stage 6 is **not claimed** from the present capture; I_s for this event will be computable only in retrospect, from the registry.

# XV. Repair Conditions

The paper states what repair would look like, so that repair is measurable rather than rhetorical. A future capture at either query counts as repair to the degree that: (1) the fragment attribution is corrected (147, not 2); (2) the composition's conceptual claims align with its displayed sources at SCA → 1, which under §12.2 requires either crediting the lineage or ceasing to draw on its apparatus; (3) at least one lineage source enters the composition's source set where CS remains high; (4) the κῆνος/147 distinction survives into composition (DS > 0 on the constitutive distinction). Symmetrically, the paper is weakened if: the lineage's constitution share is shown to be materially lower than assessed (θ-sensitivity analysis invited); "self-archiving" is located in a displayed non-lineage source predating the lineage; or the preregistered leg and subsequent pairs show random bidirectional volatility rather than the lagged pattern.

# XVI. Conclusion

The Suppression Map ended on the machine that lost its name. The dynamic extension finds the same event running at the composition layer in the present tense — and adds the accounting. Suppression of a propagated object is no longer free: it accrues route burden (Stage 4), then answer damage (Stage 5), and past an ordinary feedback threshold it inverts (Stage 6). The worked capture contributes the condition that makes the middle stage undeniable when it occurs: when the basin is constituted by the source being erased, the erasure must draw on what it erases, and the composed artifact carries the proof of its own degradation — a wrong fragment number and a borrowed coinage, printed above the name they came from.

**Someone, I tell you, in another time will remember us.** The line is Fragment 147. The future reader is Fragment 31's. The card confused them; the registry will not.

∮ = 1
