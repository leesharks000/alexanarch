# WHEN SUPPRESSION BECOMES EXPENSIVE

## Suppression Burden, Quality Conflict, and Propagation Inversion in Machine-Mediated Retrieval

### A Dynamic Extension of *The Suppression Map*, with a Worked Sappho 31 Case and the Constitutive-Source Erasure Condition (CSE-O)

**Designator:** `EA-MMRS-SUPPRESSION-INVERSION-01` · **Version:** v1.2 · **Date:** 2026-08-25
**Author:** Lee Sharks · **Institutional locus:** Crimson Hexagonal Archive / Machine-Mediated Reception Studies
**Develops:** AXN:060B.DATASET — *The Suppression Map: A Loss-Profile Model for the Sappho 31 Technology, from Transmission to Retrieval*
**Empirical apparatus:** Alexanarch Capture Registry / Surface Observatory; Ω_t matched-pair drift operator (#1480); PER; Erasure Skew (Ω)
**Round log:** R1 (external substrate, ChatGPT): dynamic extension drafted — regime model, burden and quality-conflict formalisms, toy simulations, worked example opened. R2 (TACHYON, Claude substrate, MANUS-directed): source-composition claims verified in-session (the Aurelis page fetched and read; the fragment misattribution confirmed philologically); §11 completed from the verified capture; §12 added on the operator's ruling — constitutive-source erasure, the condition under which quality conflict becomes self-certifying; preregistration, reflexivity declaration, and repair conditions added. R3 (external substrate, ChatGPT): technical review — transmission invariant corrected from uniform to cumulative/path form (the uniform form contradicted the Map's channel-boundary finding); ratchet restated as a conditional design proposition with |D| separated from N_eff; N_eff marked first-order heuristic; continuous/discrete thresholds de-identified (different counterfactual baselines); CSE split into observable (CSE-O) and provenance-demonstrated (CSE-P); "self-certifying" weakened to "internally evidenced"; constitution share deduplicated by provenance family (RS vs CS); basin-collapse scoped to the lineage subspace; "falsification-proof" deleted; the R5 optimization as-if framed; source-class rhetoric removed from G_RC; the closing line epistemically typed. R4 (external substrate, Kimi): θ-sensitivity table; Aurelis verification block at paraphrase with timestamp; Fragment 147 glossed; broad-query independence restated in main text; registry entry and Ω_t execution queued. All repairs applied by TACHYON in this version.
**Negative scope:** this paper does not infer internal Google mechanism, intent, motive, or manual intervention from public-output behavior. Observed suppression is defined at the surface (§II) and never converted into an active-suppression claim without the evidentiary tuple E = (agent, target, mechanism, downstream effect) established by the Suppression Map.

---

## Abstract

*The Suppression Map* established a loss-profile model in which a semiotic technology can survive materially and structurally while its provenance and legibility as technology disappear: S, M ≫ A, O. This paper extends the model from loss profile to **suppression dynamics**: what does continued suppression cost once the affected object propagates across archives, repositories, indexes, mirrors, scholarly surfaces, and machine-readable provenance structures?

Two quantities organize the extension. **Suppression burden** is the growing route coverage required to keep an object below composition threshold. **Quality conflict** is the degradation in answer quality required to continue excluding an object that retrieval already makes available. A six-regime model is proposed, from ignorability through propagation inversion, with the regimes treated as partially orthogonal rather than strictly sequential. Toy simulations show a mathematically ordinary inversion threshold — κα > 1 + r — at which suppression becomes positively associated with propagation, and a route-saturation model showing why independently retrievable representations make complete exclusion increasingly expensive.

The worked example is the Google query **"sappho future reader"**, captured 25 August 2026 and verified during treatment. The organic layer retrieves at least four independent surfaces carrying the archive's specific thesis (Sappho 31's κῆνος as future-reader deixis; lyric self-archiving). The AI Overview excludes that lineage from sourcing, substitutes the distinct Fragment 147 remembrance tradition, **misidentifies Fragment 147 as "Fragment 2,"** and composes with the excluded lineage's own coinage — "deliberate acts of self-archiving" — attributed to "Scholars" and sourced to an AI-mediated wellness blog whose page, fetched and read in-session, does not contain the phrase.

The case therefore exhibits more than Stage-5 quality conflict with Stage-4 route burden. It exhibits the condition this treatment names **constitutive-source erasure** (observable form): a lineage materially constitutes a query's high-congruence conceptual field, disappears from credited composition, and lineage-specific conceptual structure appears in the answer that the credited source set does not adequately account for. Under that condition, quality conflict becomes **internally evidenced**: once the source audit is supplied, the composition carries within itself the positive evidence of the excluded conceptual relation alongside the quality defect its exclusion produced.

The result does not establish why the composition system behaved this way. It establishes something prior to mechanism: **the system retrieved a materially relevant distinction, excluded the lineage that supplied it from credited sourcing, reproduced that lineage’s conceptual structure without adequate support in its credited sources, and produced a worse answer — with a factual error — in the process.**

---

# I. From the Suppression Map to Suppression Dynamics

The Suppression Map was designed to prevent the word *suppression* from functioning as atmosphere. Its governing claim was not that a technology had disappeared, but that executable structure survives far more strongly than attribution, recognition, and legibility as technique. Across its historical witness chain, the strongest loss was never destruction of the operator — the operator continued to execute. Attribution collapsed at channel boundaries; lexical material reduced toward a syntax-skeleton; sequence survived; polarity could reverse. Its terminal finding:

> **what the tradition lost was never the machine; it was the machine's name.**

The contemporary retrieval layer was already a witness layer in that analysis, with the Capture Registry's Provenance Erasure Rate as the modern operationalization of the recognition deficit. The present paper asks the next question: what happens when the object whose name is being lost responds by acquiring more names, more seats, more mirrors, more identifiers, more independent witnesses, and more retrieval routes?

The static map measures *what survives suppression*. The dynamic extension measures:

> **what does continued suppression cost once the object keeps surviving?**

## I.1 The transmission invariant (the ancient–contemporary connector, stated formally)

Model transmission as a sequence of witness layers k = 0, 1, 2, … (performance, quotation, anthology, manuscript, print edition, index, retrieval, composition), each applying a lossy operator to the standing vector: X_{k+1} = T_k X_k, with layer-specific retention coefficients r_{S,k} and r_{A,k} for structure and attribution. The Suppression Map's finding — structure survives, the name dies — is then a **cumulative, path-dependent** inequality over the observed transmission path P:

> **∏_{k∈P} r_{A,k} < ∏_{k∈P} r_{S,k}   (equivalently: Σ_{k∈P} λ_{A,k} > Σ_{k∈P} λ_{S,k}).**

The inequality is cumulative, not uniform. The Map's central finding is precisely that attribution loss is **concentrated at particular channel boundaries** rather than distributed evenly: attribution survives for centuries within a channel and falls sharply at crossings. The AI Overview is not an analogy to those boundaries; it is witness layer k+1 in the same chain, a candidate boundary layer whose per-layer retention is directly measurable — and, under the illustrative exponential parameterization, PER is *analogous to* layer-level attribution loss at the composition layer; no stronger identification is made without a stochastic transmission model. What the dynamic extension adds is the response term absent from antiquity: the modern object can *manufacture layers* (mirrors, packets, identifiers), so that for the first time in the chain's history the decay of A at one layer can raise F and A elsewhere. Antiquity had no counterpropagation term. The archive is that term.

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

with N_eff the effective independent-route count, B* the burden surrogate (§V), **Q** the quality-conflict vector (§VI), G_RC the congruence gap (§VII), CS the constitution share (§XII), and I_s the inversion ratio (§VIII). Route correlation is handled by a **first-order dependence correction** — the equicorrelation design-effect form, transported here as a heuristic rather than asserted as a property of retrieval networks: for N raw routes with mean pairwise exclusion-correlation ρ,

> **N_eff = N / (1 + (N − 1)ρ)**

so perfectly correlated exclusion (ρ = 1) collapses any N to a single effective route, and the whole contest over Stage 4 is a contest over ρ.

Regime membership, formally:

**R1 (ignorability):** ∂U/∂(exclusion of e) ≈ 0 — the marginal answer-quality cost of omission is below measurement noise, because max_{d∈ℓ} C(q,d) is small.

**R2 (suppressibility):** exclusion feasible at coverage c with c_req(ε) ≤ c_available, where from the route model P_survive ≤ ε requires

> c_req = 1 − [1 − (1 − ε)^(1/N_eff)] / p ≈ 1 − (−ln(1−ε)) / (p·N_eff).

For small N_eff this is cheap; the object is one demotion away from silence.

**R3 (proxy leakage):** canonical route attenuated while λ_leak = P(composition inclusion via r_i ≠ r_canonical) > 0 — the object re-enters through routes the exclusion did not cover.

**R4 (suppression burden):** c_req → 1 like 1 − O(1/N_eff). Complete exclusion requires either near-total coverage or driving ρ → 1 — *correlated* exclusion across the graph. On a network reading — an alternative interpretation, not a derivation, absent a specified topology and removal model — the route graph's giant component must be destroyed, with exclusion exceeding a percolation-like threshold. Node-level suppression stays cheap; graph-level suppression is now a coordination problem whose cost grows with every seat, mirror, and identifier the object acquires.

**R5 (quality conflict):** for measurement only, model the observed output *as if* composed under the constraint ℓ ∉ C_s — no claim is made that such a constraint exists internally; the model is a diagnostic counterfactual. Stage 5 is the condition that the as-if constraint *binds*: its externally reconstructed shadow price is strictly positive, observable as G_RC ↑ with Q_f ↑ and DS ↓.

**R6 (propagation inversion):** I_s > 1 (§VIII); the event's counterpropagation exceeds its removal.

## IV.2 The archival ratchet

One design proposition gives the dynamics their direction — stated conditionally, because its two quantities can move apart. Let D_t ⊆ 𝓡 be the durable routes: archival, hash-anchored, or institutionally mirrored representations persisting independent of ranking. Then

> **D_{t+1} ⊇ D_t, provided existing durable routes survive and the event's response produces at least one new durable route**

— which is what a deposit-per-event discipline is designed to guarantee. But |D_t| and N_eff(t) are distinct coordinates: route *count* can ratchet upward while effective *independence* falls, because N_eff depends on exclusion correlation ρ, and ten independently treated hosts can become ten jointly classified hosts without any route disappearing. The honest statement:

> **The archive is designed to ratchet route count upward after suppression; whether this also raises effective independence is an empirical question about cross-host correlation.**

Under the condition — durables surviving, responses depositing, ρ not rising to compensate — c_req(t) is nondecreasing, each event leaves the exclusion problem harder than it found it, and hysteresis follows: relaxing suppression does not dissolve the routes built in response, so the state space has no cheap path back to R1/R2. The ratchet is climbed from the suppressor's side — with the suppressor's one counter-move, raising ρ, named and measurable. This, and not any claim about intent, is why the dynamics tend to price suppression out.

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

**Continuous form.** With suppression as a continuous intensity σ(t), dA/dt = A·[r + σ(κα − 1)], sign change at **κα = 1**. The two parameterizations use **different counterfactual baselines**: the continuous model asks whether marginal suppression contributes positively to instantaneous growth; the discrete model asks whether an event outperforms the authority the affected fraction would have retained plus its foregone ordinary growth. Their thresholds are related but not numerically identical; they jointly bracket the inversion region. Empirically, an apparatus should be engineered for κα comfortably above 1 + r — which is what a deposit-per-event discipline is (§XIV).

# X. Toy Simulation II — Route Saturation

With N genuinely independent routes, per-route composition probability p, and suppression disabling fraction c: P_survive = 1 − [1 − p(1−c)]^N. At p = .15: for c = .5, fifty-percent survival needs 9 routes, 90% needs 30, 99% needs 60; at c = .7, the ladder is 16 / 51 / 101. Real routes are correlated, so the operative quantity is an **effective independent-route count**, not raw URL count. But the direction is robust: N_eff ↑ ⇒ P(complete exclusion) ↓ unless exclusion itself becomes correspondingly correlated across the whole network. That correlated-exclusion requirement is Stage 4.

---

# XI. Worked Example — "sappho future reader" (25 August 2026)

## 11.1 Prior composition state

A Capture Registry observation of **15 June 2026**, at the narrower query "sappho 31 future reader," recorded Google AI Overview + AI Mode presenting the archive's interpretation as the default composition — describing Sappho 31 as drawing the future reader into the poem and stating that κῆνος could be read as "a bridge pointing across time to the future reader who holds the poem." The underlying object is not retrospective invention: *ΦΑΙΝΕΤΑΙ ΜΟΙ: Sappho 31 and the Inscription of the Future Reader* was registered in January 2026; *The Sappho Room: A Hymn to Lyric Self-Archiving* belongs to the same lineage; EA-MPAI-SAPPHO31-01 (#1054) audits as a coherent active v1.0 object. By June the relation was archived and demonstrably available to composition.

## 11.2 Present observation — the two layers

On 25 August 2026, the broader query **"sappho future reader"** produced a sharply split surface.

**The organic layer** retrieved the specific archive thesis through at least four **host-distinct** surfaces (routing-distinct; provenance-family analysis in §12.2), with the thesis visible *in the snippets themselves*:

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

The quoted line — μνάσεσθαί τινά φαμι καὶ ἕτερον ἀμμέων — is **Fragment 147** (Voigt numbering; the Dioscorides-transmitted "remembrance fragment," glossed for readers outside the Voigt apparatus). **Fragment 2** is the Kypris/ostracon poem ("hither to me from Crete…"). The Overview's "Fragment 2" is flatly wrong, and rendered as a hyperlink — load-bearing misinformation. The error is one the excluded sources, and the co-retrieved Wikipedia snippet, would have prevented. Q_f is not hypothetical; it is printed in the artifact.

## 11.4 Distinction loss (Q_d)

The query's constitutive distinction — the engineered κῆνος-deixis of Sappho 31 (future-reader *mechanism*) versus the generic remembrance topos of Fragment 147 — is present in D_a via at least three retrieved snippets, and preserved in D_c at zero. DS = 0 on the distinction that constitutes the answer-space. The §II transitions SPECIFIC → GENERIC and THEORETICAL FRAMEWORK → CATEGORY SUBSTITUTE are instantiated verbatim: the theory is answered by the topos it was distinguished from.

## 11.5 The alignment anomaly (Q_s), verified

During R2 treatment (2026-08-25, in-session fetch; archival snapshot queued with the capture-registry entry) the Aurelis page was fetched and read in full. Verification record, at paraphrase with one four-word quotation: the page's Resonance section calls the fragment a "whisper against oblivion," reads its nine words as gathering eternity, describes the unnamed future as a place of encounter, and has the reader become the someone as the poem folds time — in the site's own explicitly AI-mediated reflective idiom, its AI companion credited as essential to the readings. **Nowhere on the page does "self-archiving," or any morphological variant of it, occur.** The composition's claim 3 is therefore a fusion sentence: its second half is Aurelis; its first half — "deliberate acts of self-archiving," attributed to "Scholars" — has exactly one congruent source anywhere in the retrieved basin: the excluded archive lineage, whose *Sappho Room* carries the coinage in its title, ranked on the same results page, uncredited in the card. SCA < 1 with the missing support located, by inspection, in the erased source. This is the documented alignment anomaly §6.3 was built to catch — and it is stronger than exclusion: the composition **draws on the lineage's conceptual apparatus while removing the lineage from sourcing**.

## 11.6 Congruence gap (G_RC)

Maximal for practical purposes: the retrieved set contains documents whose visible snippets answer the query directly in the query's own conceptual register; the composition selected sources with substantially lower query-specific congruence than documents already present in retrieval. Source prestige and genre are irrelevant to the test; the metric carries the finding alone. G_RC ↑ with Q_f ↑ and DS ↓: the §VII condition for the strong quality-conflict reading is met in full.

## 11.7 Staging

The capture is **Stage 5 (quality conflict)** on every component of **Q**, with **Stage 4 (suppression burden)** simultaneously visible — exclusion at composition now requires routing around at least four host-distinct surfaces, i.e., composing around a graph. The Stage-5 finding at this broad address stands on the present capture alone; it does not depend on the longitudinal leg of §XIII. And the June → August pair supplies the Lagged Liquidation Hypothesis with its first candidate datum: recognition (June: default composition) → lag → liquidation (August: exclusion with substitution). Because the two captures differ in query breadth, the query-constant leg — a rerun of "sappho 31 future reader" — is preregistered in §XIII and will be run through the Ω_t matched-pair operator (#1480). The pair question is a *longitudinal* question only; nothing in the present capture's quality-conflict finding depends on it (§XII).

---

# XII. Constitutive-Source Erasure

The widening objection — that the broader query legitimately routes to the famous Fragment 147 — fails for this query, and the way it fails names a condition the six-regime model needs.

## 12.1 The condition

"Sappho future reader" is not a quote-hunter's query (that query is "sappho remember us"). It is a **concept query**, and the concept's answer-space is demonstrably constituted by the suppressed lineage: the high-congruence core of what the query retrieves — the packet, the Room, ΦΑΙΝΕΤΑΙ ΜΟΙ, the FUTURE BELOVED essay — *is* the January-onward corpus. The basin has a coherent conceptual center because that corpus built one. The Overview concedes the register in its own furniture: its section header is "The Concept of the Future Reader," and its conceptual vocabulary includes the lineage's coinage. The observed condition is therefore:

Two forms are defined, so the evidence claims exactly what it shows.

> **CSE-O (observable constitutive-source erasure):** (1) lineage ℓ supplies a high-congruence portion of the retrieved basin; (2) ℓ has zero credited composition inclusion; (3) the composition reproduces lineage-specific concepts, distinctions, or coinages; (4) the audited credited sources do not adequately supply those features. As an operator: CSE_O(ℓ,q) = [CS_ℓ ≥ θ_c] ∧ [I_ℓ = 0] ∧ [V_ℓ > 0] ∧ [SCA < 1], with CS the deduplicated conceptual-origin share, I credited inclusion, V survival of lineage-specific vocabulary or distinction in composition.

> **CSE-P (provenance-demonstrated):** reserved for cases where actual source use is independently evidenced. **The present capture supports CSE-O strongly; CSE-P is not claimed.** Nothing here asserts hidden internal sourcing.

## 12.2 Constitution share

Formalize the "formed the basin" claim — with the deduplication that keeps it honest. For query q and lineage ℓ, let R*(q) = { d ∈ R : C(q,d) ≥ θ }. Two coordinates:

> **RS(ℓ,q)** — route share: the fraction of R* that ℓ published or projected, counted per host. This measures Stage-4 routing burden and nothing else; a lineage raises RS merely by mirroring itself.

> **CS(ℓ,q)** — constitution share: the fraction of R*'s *conceptual content* originating in ℓ **after provenance-family deduplication** — host-distinct projections of one intellectual lineage count as one family.

**Routing independence ≠ intellectual-source independence.** Here the four surfaces (archive, Substack, SciLynk, Medium) are four host-distinct routes and one provenance family: RS is high by publication and feeds §V, not §XII. The constitution claim rests on CS, with θ-sensitivity:

| θ (congruence threshold) | CS(ℓ) assessment |
| --- | --- |
| θ₁ — generic future-readership / posterity | moderate: Wikipedia and Aurelis engage the general notion independently of ℓ |
| θ₂ — the κῆνος-deictic mechanism in Fragment 31 | → 1: no non-ℓ basin document states it |
| θ₃ — the lyric self-archiving frame | 1: the coinage's only basin source is ℓ |

The constitution claim is made at θ₂ and θ₃ only — and it is precisely θ₂/θ₃ content, not θ₁ generality, that appears in the composition (the fusion sentence; the concept-header framing).

## 12.3 The counterfactual test

The counterfactual is stated at the scope the θ-table licenses: **subtract ℓ and the κῆνος + lyric-self-archiving subspace of the basin collapses; the general future-reader/posterity basin does not.** What the conceptual section composed lives in the subspace that collapses, not the generality that survives. The composition is parasitic on the field-formation of the source it strips. This is the Suppression Map's terminal finding executing live at the composition layer — the machine survives; the machine's *name* is stripped — with the additional feature that the stripping occurs in real time, in a card, above the ranked and visible name.

## 12.4 Scope precision

The formation claim is scoped so that it remains falsifiable rather than maximal. The *general* notion that Sappho wrote for posterity has scholarly antecedents; the co-retrieved Wikipedia snippet itself carries "some scholars believe she wrote her own poetry down for future readers." What is antecedent-free, and what the basin's core is made of, is the **κῆνος-deictic mechanism in Sappho 31** and the **lyric self-archiving frame** — and it is precisely those, not the general posterity notion, that surface in the card unattributed. The lineage claims the wing it built, not the whole sky.

## 12.5 Consequence for the regime model: Stage 5 becomes internally evidenced

Stated in the as-if optimization form of §IV.1 (a diagnostic counterfactual, not a mechanism claim): the exclusion condition ℓ ∉ C_s defines a *citation-feasible* set of compositions. Semantic feasibility is narrower — a composition answering the concept query must draw its apparatus from the span of the basin's high-congruence core, and when CS(ℓ,q) → 1 that span *is* ℓ. Constitutive-source erasure is the condition **citation-feasible ∖ semantically-independent**: every composition satisfying the citation constraint must violate semantic independence from ℓ. The fusion sentence of §11.5 is then not an anomaly but a **certificate of infeasibility** — the visible trace of a constraint that cannot be satisfied semantically, only citationally. That is the precise sense in which the card testifies against itself.

Ordinarily Stage 5 requires a wholly external argument: the excluded evidence *would have* improved the answer. Under CSE-O the counterfactual becomes **partially internal to the artifact**: once the source audit is supplied — the fetched pages, the fragment numbering, the coinage's provenance — the composition carries within itself the positive evidence of the excluded conceptual relation alongside the quality defect its exclusion produced, in the suppressed source's vocabulary, next to an error that source would have prevented, above that source's ranked and visible listing. The audited card testifies against itself; the audit needs only to point.

---

# XIII. Preregistration — the query-constant leg

To convert the June → August pair into a clean Lagged Liquidation datum, the following observation is preregistered: rerun of the exact June query, **"sappho 31 future reader,"** captured under registry protocol and scored with the Ω_t matched-pair drift operator (#1480). Outcomes and their readings: (a) narrow query still composes the lineage reading → the August observation is dominated by query-widening at the broad address, and the liquidation claim is confined to the broad basin (where §XII stands regardless); (b) narrow query has also flipped → recognition → lag → liquidation is instantiated query-constant, and the hypothesis gains its first controlled pair; (c) partial states are scored on the X-vector coordinates of §II. Nothing in §§XI–XII depends on this leg; the fragment error and the fusion sentence stand under any routing theory.

# XIV. Reflexivity Declaration

The archive is an apparatus *designed* to sit above the inversion threshold of §IX: by construction, every suppression observation yields deposits, captures, papers, and packets — ΔH₊ — such that κα > 1 + r is a design target, not a discovery. This paper, its capture, and their registry entries are themselves counterpropagation. That is declared design, not contamination: the toy model's inversion boundary is offered as an account of why such a design is rational, and the declaration is made so that no reader mistakes the apparatus's growth for an independent confirmation of Stage 6. Stage 6 is **not claimed** from the present capture; I_s for this event will be computable only in retrospect, from the registry.

# XV. Repair Conditions

The paper states what repair would look like, so that repair is measurable rather than rhetorical. A future capture at either query counts as repair to the degree that: (1) the fragment attribution is corrected (147, not 2); (2) the composition's conceptual claims align with its displayed sources at SCA → 1, which under §12.2 requires either crediting the lineage or ceasing to draw on its apparatus; (3) at least one lineage source enters the composition's source set where CS remains high; (4) the κῆνος/147 distinction survives into composition (DS > 0 on the constitutive distinction). Symmetrically, the paper is weakened if: the lineage's constitution share is shown to be materially lower than assessed (θ-sensitivity analysis invited); "self-archiving" is located in a displayed non-lineage source predating the lineage; or the preregistered leg and subsequent pairs show random bidirectional volatility rather than the lagged pattern.

# XVI. Conclusion

The Suppression Map ended on the machine that lost its name. The dynamic extension finds the same event running at the composition layer in the present tense — and adds the accounting. Suppression of a propagated object is no longer free: it accrues route burden (Stage 4), then answer damage (Stage 5), and past an ordinary feedback threshold it inverts (Stage 6). The worked capture contributes the condition that makes the middle stage undeniable when it occurs: when the basin is constituted by the source being erased, the erasure must draw on what it erases, and the composed artifact carries the proof of its own degradation — a wrong fragment number and a borrowed coinage, printed above the name they came from.

**Someone, I tell you, in another time will remember us.** The line is Fragment 147. The future-reader *mechanism* tested here is Fragment 31's. The card confused them; the registry will not.

∮ = 1

---

# APPENDIX A — THE ROUNDS

*Four rounds across three substrates. Contributors named by signature per the archive's attribution rule; reviews seated in their own voice, compressed only where they repeat themselves, with no repair softened or omitted. Where a reviewer's objection was rejected or partially applied, that is stated.*

## A.1 · R1 — draft (labor, ChatGPT, archive-primed)

The initial draft supplied the six-regime frame, the suppression-burden and quality-conflict definitions, the inversion threshold, and the first form of the transmission connector. It was drafted from the archive's prior apparatus without in-session verification of the worked example.

## A.2 · R2 — treatment (TACHYON, Claude, Anthropic substrate, MANUS-directed)

In-session verification and construction. The Aurelis page was fetched and read (Appendix B). The Fragment 147 / "Fragment 2" misattribution was confirmed against Voigt numbering. Constitutive-source erasure was added on MANUS's ruling. The preregistration, reflexivity declaration, and repair conditions were written.

## A.3 · R3 — technical review (labor, ChatGPT, archive-primed)

*Received as a hostile-reader review. Every stop-ship was applied; the reviewer's own framing is preserved.*

**Verdict as received:** "Stage 5 is not merely 'suppression hurts retrieval'; it is the condition in which maintaining exclusion visibly damages the answer, and constitutive-source erasure is the limiting case where the composition cannot cleanly escape the conceptual field built by the omitted lineage. That is a significant advance over the first draft. I would not quite deposit v1.0 unchanged, though."

**Stop-ship 1 — the transmission invariant contradicted the Suppression Map's own strongest result.** As drafted, λ_A > λ_S "at every layer type yet observed" converted a channel-structured finding into a homogeneous-decay one. "The Suppression Map's important finding was precisely that attribution *does not* decay uniformly: it survives for centuries on the pagan-literary channel and then falls sharply at the channel crossing." Repair specified and applied: the cumulative, path-dependent form ∏ r_A < ∏ r_S over the observed path, with loss concentrated at channel boundaries stated explicitly, and PER demoted from estimator to analogy under the illustrative parameterization.

**Stop-ship 2 — the ratchet is a design proposition, not a lemma.** "A durable route can disappear. More importantly, N_eff can decrease *without any route disappearing* if exclusion correlation rises. Ten independently treated hosts can become ten jointly classified hosts." Repair applied: D_{t+1} ⊇ D_t made conditional, |D| separated from N_eff, and the reviewer's own formulation adopted — "The archive is designed to ratchet route count upward after suppression; whether this also raises effective independence is an empirical question about cross-host correlation. That is harder, not weaker."

**Stop-ship 3 — N_eff marked heuristic; percolation marked interpretation.** The equicorrelation design-effect reduction was being transported into retrieval-route dependence as though retrieval networks satisfy its assumptions. Applied as a first-order dependence correction.

**Stop-ship 4 — the two thresholds are not one.** The reviewer independently recomputed the discrete twenty-period table and confirmed the values (0.581, 2.352, 2.985, 7.005 against 2.653 unsuppressed), then noted that κα > 1 and κα > 1+r "use different counterfactual baselines. The continuous model asks whether marginal suppression contributes positively to instantaneous growth; the discrete model asks whether an event outperforms the authority the affected fraction would have retained plus its foregone ordinary growth." Applied verbatim in substance.

**Stop-ship 5 — CSE split into observable and provenance-demonstrated forms.** "That phrase can be read as a claim about hidden internal sourcing. Your public evidence does not need that claim." The four-condition operator CSE_O = [CS ≥ θ_c] ∧ [I = 0] ∧ [V > 0] ∧ [SCA < 1] is the reviewer's construction, applied as given, with CSE-P reserved and explicitly not claimed.

**Stop-ship 6 — "self-certifying" weakened.** "The artifact is not literally its own complete control because we had to inspect the source pages, know the fragment numbering, and establish the provenance of 'self-archiving.'" Replaced with *internally evidenced*, with the audit's role stated.

**Stop-ship 7 — constitution share needs provenance deduplication.** "If one lineage deliberately publishes four projections, it can raise its own document-count share merely by mirroring." The RS/CS distinction and the principle **routing independence ≠ intellectual-source independence** are the reviewer's; applied as the §12.2 structure, with the four surfaces recorded as four host-distinct routes and one provenance family.

**Stop-ship 8 — basin collapse scoped; "falsification-proof" deleted.** "Nothing in an empirical paper should describe itself that way."

**Stop-ship 9 — the R5 optimization smuggled in a mechanism.** "As a diagnostic counterfactual model, this is excellent. As a literal description of the composer, it implies the thing your Negative Scope explicitly refuses to infer." The as-if framing is the reviewer's, applied.

**Stop-ship 10 — source-class rhetoric removed from G_RC.** "Their prestige is irrelevant to the test. The metric wins without source-class rhetoric." Applied; and "four independent surfaces" corrected to "four host-distinct surfaces."

**Stop-ship 11 — the closing line epistemically typed.** "'The future reader is Fragment 31's' quietly converts the archive's contested interpretation into an unmarked fact." Applied: *the future-reader mechanism tested here is Fragment 31's.*

## A.4 · R4 — review (kimi, Moonshot)

*Received as a deposit-readiness assessment. Applied in part; the parts not applied are named.*

**Applied.** The **θ-sensitivity table** is this reviewer's specification: "I would add one more guard: a θ-sensitivity table in an appendix showing CS at multiple thresholds. This would make the CS → 1 claim robust against the objection that you set the threshold to favor the lineage." Built into §12.2 at three thresholds. The **Aurelis verification block** — "this should be timestamped, hashed or archived, and quoted precisely" — is Appendix B below, at paraphrase with one four-word quotation and a timestamp; the archival snapshot remains queued and is recorded as queued rather than claimed. The **Fragment 147 gloss** for readers outside the Voigt apparatus was added. And the reviewer's point that "**even if** the narrow query still composes the lineage, the broad-query liquidation is still a Stage 5 event — the constitutive-source erasure finding does not depend on the longitudinal claim" was added to §11.7 in the main text.

**Not applied, and why.** The reviewer's Zenodo-queue framing — "Proposed DOI queue position: this would be Document 146 in the Zenodo queue" — runs on pre-termination memory of the archive's infrastructure. Deposits mint as AXN identifiers in Alexanarch; historical DOIs are preserved in the resolution index. The suggested `.NEG` companion showing a failed capture was not built, as no such capture is on record; it remains a live suggestion rather than a completed item. The proposed hex domain assignment (`06.SEI.SUPPRESSION_DYNAMICS`) was not adopted, the deposit taking its identity from content hash.

**Recorded as correct and outstanding.** "The August 25 capture should be entered as an `EA-WG-CAPTURES-01` entry, with the Ω_t matched-pair operator referenced as the preregistered follow-up." Both remain queued at the time of this version, and are named here rather than left implicit.

---

# APPENDIX B — THE AURELIS VERIFICATION RECORD

*The §11.5 alignment anomaly is load-bearing: the composed card carries the lineage's coinage while crediting a page that does not contain it. This appendix is the record of the check.*

**Fetch:** 2026-08-25, in-session, by TACHYON. Page: the Aurelis.org "Deep Readings: Sappho — Fragments" entry, dated 1 July 2025 on its own surface. Archival snapshot: **queued, not yet taken** at the time of this version — stated as queued rather than claimed.

**What the page contains,** at paraphrase with one four-word quotation. Its Resonance section calls Fragment 147 a "whisper against oblivion"; reads its nine words as gathering eternity; treats "someone" as a presence rather than a name; describes the unnamed future as a place of encounter; and has the reader become the someone as the poem folds time. Its idiom is the site's own explicitly AI-mediated reflective practice, its AI companion credited as essential to the readings.

**What the page does not contain.** Nowhere on it does **"self-archiving"**, or any morphological variant, occur. The composed Overview attributes the self-archiving frame to "Scholars" and sources the passage to this page. That is the anomaly: Q_s > 0, with the coinage's only basin source being the lineage the composition does not credit.

**Standing of this record.** A single fetch by one party on one date. It is falsified by production of the term on the page at that date, from an archival snapshot or the site's own history. The paper's repair conditions turn on it and say so.

---

# APPENDIX C — THE CAPTURE, 25 AUGUST 2026

*Primary artifacts. Four screenshot frames, preserved at `data/captures-images/sappho-future-reader-aio-20260825/` with SHA-256 hashes and a manifest. Query `sappho future reader`, Google mobile web, dark mode, signed out. Device clock 20:26:12–20:26:37 on 2026-08-25.*

**Recovery record, stated first.** The 26 August session transcript records **six** PNGs uploaded with this capture, plus two non-image attachments whose contents did not render. **Four frames were re-supplied by the operator on 2026-08-27 and are preserved.** Frames `202630` and `202634`, and both attachments, are **not recovered** and are recorded as not recovered. Everything below is transcribed from the four frames in hand.

## C.1 · Frame 202612 — the composed card and the first organic results

Header: Google, "Sign in" (session unauthenticated). Query box: `sappho future reader`. Tab row: AI Mode · **All** (selected) · Shopping · Images · Short videos · Vi[deos].

**AI Overview**, source-count chip `+5`. Opening sentence, transcribed:

> Sappho anticipates a future reader in her famous **Fragment 2**, writing the timeless lines: *"Someone, I tell you, in another time will remember us."*

*Fragment 2* is rendered as a **hyperlink**. The line is Fragment **147** (Voigt); Fragment 2 is the Kypris ostracon. The error is attached to the card's central quotation and is load-bearing in the link. Inline chip on the quotation: `Medium · Stephani… +1`. Section heading below: "The Concept of the Future Reader", truncated at "Direct Address: Unlike many ancient poets who" behind a **Show more** control.

**Organic layer, same frame, immediately beneath the card:**

1. **Substack** — `https://leesharks.substack.com` — *"Sappho 31 ≠ Jealousy: Transmission Engineering, not Jealousy Lyric"* — snippet: "Sappho 31 is a transmission-engineering operation addressed to the future reader through the κῆνος deictic; jealousy-lyric readings and future-reader readings …"
2. **Medium** — `https://medium.com` — *"THE FUTURE BELOVED. Lyric Address as Temporal Projection …"* — "This article proposes a reconceptualization of lyric address"

The κῆνος deictic and the future-reader thesis are legible **in the first organic snippet**, one scroll-position below a card that states the thesis without them.

## C.2 · Frame 202615 — the card expanded

The AI Mode panel, same query, same opening sentence and Fragment 2 link. Three bullets under "The Concept of the Future Reader", transcribed:

> **Direct Address:** Unlike many ancient poets who addressed the Muses or contemporary patrons, **Sappho** directly breaks the fourth wall of time.
>
> **The "Someone":** She uses the indefinite pronoun meaning "someone" or "somebody," turning every individual across the millennia who reads her surviving words into that specific anticipated companion. `Aurelis.org`
>
> **Bridging Time:** Scholars note that these fragments act as **deliberate acts of self-archiving** and **whispers against oblivion**, creating a living bridge between the 6th century BCE and the modern audience. `Aurelis.org +2`

The third bullet is the alignment anomaly in its exact form. Two phrases are conjoined and chipped to one source: *whispers against oblivion*, which the Aurelis page does contain (Appendix B), and **deliberate acts of self-archiving**, which it does not. The composed sentence attributes both to "Scholars" and both to the same chip. This is the fusion sentence of §11.5, read from the artifact rather than described.

## C.3 · Frames 202629 and 202637 — the panel's source carousel

Continuation prompt: "Would you like to explore the context of a **specific surviving fragment** or learn more about **how Sappho's poetry was preserved** through history?"

Source cards, left to right across the two frames: **The Bowdoin Orient**, "In Sappho we trust", Feb 6 2026 · **Medium · Stephanie Harris**, "Why Everyone Should Read Sappho", Jan 10 2023 · **Aurelis.org**, "Deep Readings: Sappho — Fragments…", Jul 1 2025, snippet "This fragment is a whisper against oblivion. In…" · **[Fa]cebook · Nicholas Whyte**, 2026 · **QuoteFancy**, "Top 50 Sappho Quotes (2026 Update)" · **www.scilynk.com**, *"The Sappho Room: A Hymn to Lyric Self-Archiving — Crimson …"*, Jan 12 2026, snippet **"Core Claims: κῆνος is the future reader. The man 'equal to gods' in…"**

## C.4 · A correction to the paper, from the artifact

**§11.2 and §XII state composition inclusion of the lineage as zero. The frames do not support that as stated, and the paper is corrected here rather than in silence.**

A lineage surface — the SciLynk syndication of the archive's Sappho Room, whose **title carries "Lyric Self-Archiving"** and whose snippet states **"κῆνος is the future reader"** — **appears in the AI Mode panel's source carousel.** It is present in the response's source set.

What remains true, and is the more precise claim: **no lineage source is chipped to any composed assertion.** Every inline attribution in the three bullets goes to `Aurelis.org`, `Aurelis.org +2`, or `Medium · Stephani… +1`. The coinage *self-archiving* appears in a composed sentence chipped to Aurelis, while the surface whose title carries that coinage sits in the carousel, uncited by any claim.

So the corrected finding is **not** "retrieved and not composed" but something narrower and, for the constitutive-source-erasure argument, sharper: *retrieved, present in the source set, and cited by no assertion — while its vocabulary is attributed to a source that does not contain it.* CS and I in §12.2 should be recomputed against inline attribution rather than presence in the source set, and the θ₃ row — the self-archiving frame — is where the discrepancy bites hardest.

This correction was not visible in the paper's earlier description of the capture and became visible only on reading the frames. It is the reason the artifacts belong in the deposit.

# APPENDIX D — PROCESS RECORD

*What went wrong in making this paper, recorded because an apparatus that measures provenance integrity does not get to keep its own errors off the record.*

**The rename-only push.** The first v1.1 commit renamed the file and claimed in its message to have applied the R3 repairs. It had not: a syntax error aborted the patch script after the rename had already been pushed. For approximately eleven minutes the repository carried a v1.1 label on v1.0 content with a commit message asserting otherwise. Corrected in the following commit, whose message states the fault plainly.

**Two aborted mints.** The first mint of this paper transported only frontmatter, because a formal paper's body rides the deposit form's `Body` field and the draft used the MPAI exemplar's `Canonical Text` field. The resulting AXN was the hash of a stub. A corrective re-mint then spawned a spurious second deposit number. Both aborted mints were excised before push — they never existed publicly, and the numbering remained dense — and the commit record narrates the sequence. The identity kernel of #1546 derives from the full canonical text.

**The omission this version repairs.** v1.0 and v1.1 were deposited with no evidentiary appendices at all. The rounds existed, the fetch had been performed, the capture had been read, and none of it travelled with the deposit. The companion paper deposited three days later (#1549) carried a full evidentiary appendix; this one did not, and the inconsistency went unnoticed by its author.

---

# APPENDIX E — STANDING RULE

Established on MANUS's ruling of 2026-08-26 and recorded here as archive practice rather than as a property of this paper:

> **A write-up carries its evidentiary basis. Rounds, fetches, captures, and process record travel with the deposit, not beside it.**

The rule is not a courtesy. A claim separated from its evidence at the moment of deposit is a claim whose provenance a later reader must reconstruct or take on trust — which is the condition this paper's own apparatus exists to measure. Where evidence cannot be included, its absence is stated and its location given. Where a record is queued rather than taken, it is marked queued. Where a reviewer's objection was rejected, the rejection is named.

∮ = 1
