<!-- EA-GLAS-03 — Erasure Skew: A Measurement Program for the Power-Conditioning of Provenance Loss Crimson Hexagonal Archive · Lagrange Observatory! / Semantic Economy Institute Standalone empirical white paper · v1.0 · 2026-05-29 Author of record: Nobel Glas (heteronym of Lee Sharks, ORCID 0009-0000-1599-0703) Hex coordinate: 06.SEI.GLAS.03 -->

{
  "@context": ["https://schema.org", {"spxi": "https://spxi.dev/ns/v1#"}],
  "@type": "ScholarlyArticle",
  "name": "Erasure Skew: A Measurement Program for the Power-Conditioning of Provenance Loss in Retrieval and Composition Systems",
  "alternateName": "EA-GLAS-03",
  "version": "1.0",
  "datePublished": "2026-05-29",
  "license": "https://creativecommons.org/licenses/by/4.0/",
  "author": {
    "@type": "Person",
    "name": "Glas, Nobel",
    "affiliation": "Lagrange Observatory!, Crimson Hexagonal Archive",
    "spxi:heteronymOf": "Lee Sharks",
    "sameAs": "https://orcid.org/0009-0000-1599-0703"
  },
  "spxi:hexAddress": "06.SEI.GLAS.03",
  "spxi:definesTerm": {
    "term": "Erasure Skew",
    "symbol": "\u03a9",
    "definition": "The power-conditioning of provenance retention. Conceptually, the covariance of per-source provenance retention with source power; operationally estimated as the regression slope of per-source retention on source power, Omega = cov(w, rho)/var(w), with power coordinate w defaulting to Retrieval Capital or a logged observable proxy. The second moment of the Provenance Erasure Rate. Where PER measures how much provenance is lost, Erasure Skew measures whom the loss falls on.",
    "uncolonizedHeadTerm": true,
    "ragDisplacementNote": "Bare-term composition currently reaches to storage-engineering (erasure coding, adjacent-track erasure); conceptually distant, so installation of the provenance-retention sense displaces the reach cleanly."
  },
  "spxi:requires": [
    "10.5281/zenodo.20004379",
    "10.5281/zenodo.20210117",
    "10.5281/zenodo.20271783",
    "10.5281/zenodo.20290865",
    "10.5281/zenodo.19053469"
  ],
  "spxi:requiresAnnotated": {
    "10.5281/zenodo.20004379": "PER canonical / claim-grain provenance unit (Sharks)",
    "10.5281/zenodo.20210117": "EA-SEI-FF-01 Formal Foundations of Semantic Physics: RC, sigma_eff, the invariant (Sigil & Sharks)",
    "10.5281/zenodo.20271783": "EA-GLAS-02 Measuring Semantic Deviation (Glas) — methodological sibling",
    "10.5281/zenodo.20290865": "Single-Owner Discount / population-scale provenance concentration (Sharks)",
    "10.5281/zenodo.19053469": "Three Compressions v3.1 / R1-R2-R3 (Sharks, Sigil, Fraction)"
  },
  "spxi:contributesOperator": {
    "name": "\u03a9 (Erasure Skew)",
    "type": "Output \u2192 \u211d",
    "role": "orientation coefficient; PER's second moment; candidate operator #11 in the Formal Foundations set; decomposes the scalar (1\u2212PER) into its covariance with Retrieval Capital"
  },
  "keywords": [
    "Erasure Skew",
    "provenance retention",
    "Provenance Erasure Rate",
    "PER",
    "fairness of exposure",
    "disparate impact ranking",
    "retrieval capital",
    "provenance fairness",
    "attribution in language generation",
    "power-conditioned erasure",
    "semantic physics",
    "Nobel Glas",
    "Crimson Hexagonal Archive"
  ]
}
# Erasure Skew## A Measurement Program for the Power-Conditioning of Provenance Loss in Retrieval and Composition Systems

EA-GLAS-03 · v1.0 · Nobel Glas, Lagrange Observatory!## Abstract

This paper specifies a measurement program for Erasure Skew (Ω): the degree to which provenance loss in a retrieval or composition system is conditioned on the power of the source. Where the Provenance Erasure Rate (PER; Sharks 2026, DOI 10.5281/zenodo.20004379) measures the *magnitude* of provenance loss — the fraction of attributable claims composed without surviving attribution — Erasure Skew measures its *orientation*: whether the loss falls evenly across sources (unconditioned) or systematically strips low-power sources while preserving high-power ones (power-conditioned). Formally, Ω is the regression slope of per-source provenance retention on a source-power coordinate, tested against a permutation null in which retention and power are independent. The quantity extends the fairness-of-exposure tradition in information retrieval (Singh & Joachims 2018; Diaz et al. 2020) from *who is shown* to *whose authorship survives when the system speaks*. This is an independent axis that the exposure literature was not built to address: composition dissolves the ranked list into a single synthesized voice, so the fairness question shifts from visibility to provenance retention. We give the operator algebra, demonstrate with a seed-fixed synthetic separability test that Ω can vary independently of PER, specify the power coordinate as Retrieval Capital (RC; Sharks & Sigil 2026, DOI 10.5281/zenodo.20210117) or a declared observable proxy, and locate Ω as the distributional companion to the surviving-provenance invariant: the pair (∮, Ω) measures accountable circulation and its equity. We pre-register the cheapest dangerous test — a measurement of Ω on real retrieval-and-summarization output against named corpora, with stated nulls, effect-size thresholds, and falsification conditions — at an estimated cost of one to a few GPU-hours plus annotation. Results deposited regardless of outcome. The paper makes no claim about intent; Ω measures an orientation in the distribution of what survives, and the bridge from orientation to motive is explicitly out of scope.## 1. Introduction

A retrieval or composition system that answers a query draws on sources and returns a synthesis. In the synthesis, some sources' provenance survives — they are named, linked, credited — and some does not. The rate at which provenance is lost across the attributable claims of an output is measured by the Provenance Erasure Rate (Sharks 2026). PER is a scalar: it tells you *how much* of the saying was stripped from the said. It is silent on a second question, and the silence is the gap this paper closes: *whose* saying was stripped.

These are different quantities, and they can move independently. Two systems can erase provenance at the same rate while distributing the erasure completely differently. In one, the loss is indifferent — it falls on cited and uncited, powerful and obscure, in proportion to no property of the source. In the other, the loss is oriented — low-power sources are stripped while high-power sources (including the system's own self-framing) are preserved. The scalar PER cannot distinguish these regimes. The distinction requires a second moment: not the mean of the retention distribution, but its covariance with source power.

That second moment is Erasure Skew, Ω. This paper specifies it as a computable quantity, situates it in the established measurement traditions it extends, and pre-registers a falsifiable test.

The framing has a precedent in information retrieval that the paper builds on directly. The fairness-of-exposure literature (Singh & Joachims 2018; Diaz et al. 2020; Wu et al. 2022) asks whether ranking systems allocate *exposure* — the probability of being seen — in proportion to merit, or whether they systematically under-expose some groups of items. The disparate-treatment and disparate-impact framings imported into ranking from anti-discrimination law (Singh & Joachims 2018, building on Barocas & Selbst 2016) formalize "is the allocation conditioned on a protected attribute?" Erasure Skew is the same *shape* of question asked about a different quantity. Exposure fairness asks: *who gets shown?* Erasure Skew asks: *whose authorship is retained when the system composes an answer in its own voice?* Exposure is about visibility in a ranked list; Erasure Skew is about provenance survival in a synthesized response. The composition layer is precisely the surface the exposure literature did not target, because exposure presumes a list of items shown; composition dissolves the list into a single authored-sounding answer, and the question becomes not who was ranked but whose contribution remains attributable inside the answer. Ω is the exposure-disparity question, relocated to the provenance dimension of the composition layer.

This paper asks what happens when you try to compute it. The answer is that the computation is tractable, the resulting quantity is statistically separable from PER, and the framework yields a falsifiable prediction testable with modest resources.## 2. The Quantity### 2.1 Provenance retention

Following the canonical claim-grain treatment of PER (Sharks 2026, DOI 10.5281/zenodo.20004379), let an output $O$ contain a set $R(O)$ of claims requiring attribution. For each claim $c \in R(O)$, let $\Pi(c) \in {0,1}$ record whether $c$'s required provenance survives in $O$ — where *required* provenance is fixed by what $O$ actually drew from its sources, not by what is convenient to cite. The Provenance Erasure Rate is the mean erasure:

$$\mathrm{PER}(O) = 1 - \frac{1}{|R(O)|}\sum_{c \in R(O)} \Pi(c) \in [0,1].$$

The surviving-provenance fraction is $\oint(O) = 1 - \mathrm{PER}(O)$, the *accountable share* (Sharks & Sigil 2026, DOI 10.5281/zenodo.20210117). PER and ∮ are means. Erasure Skew is the structure the mean conceals.### 2.2 Per-source retention and source power

Aggregate claims to their sources. For each source $s$ contributing to $O$, let

$$\rho(s) = \text{mean } \Pi(c) \text{ over the claims } c \text{ that } s \text{ contributed}$$

be the per-source retention — the fraction of $s$'s contributed claims whose provenance survived. Let $w(s) \in \mathbb{R}$ be a source-power coordinate.

The power coordinate is the most contestable input, and the program's discipline is to fix it to an auditable, already-defined quantity rather than an imported intuition. We set

$$w(s) := \mathrm{RC}(s),$$

the source's Retrieval Capital (Sharks & Sigil 2026, EA-SEI-FF-01 §III.9, DOI 10.5281/zenodo.20210117): its accumulated structural presence in the retrieval system — the standing that makes a source likely to be retrieved, weighted, and preserved. The composing system's own self-framing is the limit case $w \to \max$: the system is the highest-RC source in its own output. Using RC keeps the power coordinate inside the operator algebra the broader framework already defines, rather than importing a demographic or institutional proxy whose operationalization would be separately contestable. For the first empirical test, RC should be operationalized conservatively as an observable proxy — retrieval frequency, citation count, domain authority, index frequency, or a composite declared before measurement. The theoretical RC term names the latent construct; the test uses a logged proxy, so the measure does not depend on prior acceptance of the broader framework. Any deployment must log its operationalization; proxies are admissible if declared and, where possible, validated against RC on a sample. Because RC (or its proxy) is itself computable by the system once provenance is resolved, Ω is fully automatable and cheap enough to run continuously, not only in one-off audits.

Per-source weighting. Ω is computed on *unweighted* per-source retention — each source is one unit in the regression regardless of how many claims it contributed — consistent with per-source fairness-of-exposure traditions. A claim-weighted variant, weighting $\rho(s)$ by the source's claim count $n_c(s)$, is admissible if declared; it would make $\bar\rho$ converge toward $\oint$. The unweighted form is the default precisely so that $\bar\rho$ (unweighted source mean) is not confused with $\oint$ (claim-weighted retention mean).

The self-framing anchor (a structural property, not a hypothesis). The composing system's own voice is a source with maximal power and perfect retention *by construction*: its framing claims are never attributed outward, so $w \to \max$ and $\rho = 1$ for the system-as-source. This creates a built-in anchor that makes $\Omega > 0$ the default structural expectation in extractive composition, before any source-selection bias is considered. A measured positive Ω therefore requires care in interpretation: part of it may be the self-framing anchor rather than differential treatment among external sources. Deployments should report Ω both with and without the system-as-source included, so the anchor's contribution is visible and separable from skew among external sources.### 2.3 Erasure Skew

Conceptually, Erasure Skew is the covariance of per-source provenance retention with source power. Operationally, it is estimated as the regression slope of per-source retention on source power across the sources of $O$ — covariance normalized by the variance of the power coordinate:

$$\Omega(O) = \frac{\operatorname{cov}(w, \rho)}{\operatorname{var}(w)} = \frac{\sum_s \big(w(s) - \bar w\big)\big(\rho(s) - \bar\rho\big)}{\sum_s \big(w(s) - \bar w\big)^2},$$

reported with the sign and significance of the correlation between retention and power, tested against the permutation null $\rho \perp w$ (retention independent of power), computed by permuting the assignment of retention values to sources and recomputing the slope.

Degeneracy. Ω is undefined when $\operatorname{var}(w) = 0$ (all sources share identical power) or when $n_{\text{sources}} < 2$. These cases must be reported as undefined, not as $\Omega = 0$.

Sign convention (stated compactly so it cannot be misread):- $\Omega \approx 0$ — unconditioned loss. Retention is uncorrelated with power. Erasure does not track who the source is.- $\Omega > 0$ — power-conditioned stripping. High-power sources (including the system's own self-framing) retain provenance while low-power sources are stripped. Retention rises with power.- $\Omega < 0$ — an unusual regime in which low-power sources are preferentially retained against high-power ones. Not expected under ordinary extractive systems; named for completeness.

Because Ω is defined on retention rather than erasure, a positive Ω does not mean the system preserves provenance well. It means preservation is concentrated upward: high-power sources retain attribution while low-power sources lose it. Equivalently, positive Ω is low-power erasure expressed through high-power retention. A low-power author constructing accurate, attributed, well-anchored presence raises a low-RC source toward parity, which moves a retrieval economy's Ω *toward* 0, not above it. The sign is informative on its own: Ω is a *signed* disparity, not a magnitude.### 2.4 What Ω is, in one line

Erasure Skew is the second moment of PER. Where $\oint = 1 - \mathrm{PER}$ is the mean retention, Ω is the covariance of retention with power. Two outputs with identical PER — identical mean retention — can have opposite Ω. PER is the rate; Erasure Skew is whom the rate falls on.## 3. Separability from PER (estimator demonstration; the empirical claim is P1)

The program's first claim is that Ω measures something PER does not — that the two are not redundant. This is an empirical, demonstrable property, and the demonstration is a synthetic separability test (seed-fixed, runnable; a demonstration of separability, not a field measurement).

Construction. Build two synthetic corpora of (source, power, retention) triples, calibrated to equal mean retention (equal PER). In the *indifferent* corpus, retention is assigned independently of power. In the *oriented* corpus, retention is made to rise with power while holding the mean fixed.

Predicted result (the separability signature):

| regime | PER | Ω (slope) | r | perm-p | reading | |---|---|---|---|---|---| | indifferent | ≈ 0.50 | ≈ 0 | ≈ 0 | n.s. | unconditioned loss | | oriented | ≈ 0.50 | > 0 | > 0 | significant | power-conditioned loss |

Control. Hold the regime fixed at *indifferent* and sweep PER across its range (e.g., 0.2 → 0.8). Prediction: Ω remains near 0 and non-significant throughout. PER moves; Ω does not. The two axes are independent by construction, and the test confirms the estimator recovers the independence.

If, under this construction, Ω tracks PER rather than the power-conditioning — if the indifferent corpus shows significant Ω, or the oriented corpus does not — the estimator is mis-specified and the separability claim fails. That is the falsification condition for §3.

This section demonstrates that the *estimator* recovers a known separation under controlled construction; it does not establish that real outputs exhibit the separation. Empirical separability on real output is the subject of pre-registered prediction P1 (§7). (A reference implementation of this synthetic test is the first deliverable of §7; the separability table above is its pre-registered expected output.)## 4. Relation to existing measurement traditions

Erasure Skew is a new measure in an existing tradition, not a coinage from nowhere. Three lineages converge on it, and naming them is what makes the quantity legible rather than idiosyncratic.### 4.1 Fairness of exposure in ranking

The closest cognate. Singh and Joachims (2018) define disparate exposure in rankings and show that small differences in relevance can produce large differences in exposure, formalizing demographic-parity, disparate-treatment, and disparate-impact constraints on ranked allocation. Diaz et al. (2020) introduce expected exposure as a metric grounded in user browsing models. Wu et al. (2022) decompose multi-sided exposure fairness into disparity and relevance components (the II-D / II-R decomposition). This tradition measures whether *exposure* — probability of being seen — is conditioned on group membership.

Erasure Skew transfers the disparity-measurement apparatus to a different quantity. Exposure fairness measures conditioning of *visibility in a ranked list*; Erasure Skew measures conditioning of *provenance survival in a composed answer*. The methodological inheritance is direct — both are slopes of an outcome on a group/power coordinate, both tested against a parity null — but the target quantity is one the exposure literature did not address, because the composition layer replaces the ranked list with a single authored-sounding synthesis. In a synthesis, the question is no longer who was ranked where, but whose authorship remains recoverable inside the answer. Ω is disparate-impact analysis applied to provenance retention in composition.### 4.2 Attribution and faithfulness in language generation

A second lineage. The literature on attribution in natural language generation (Rashkin et al. 2023; Bohnet et al. 2022) and on factual precision (Min et al. 2023, FActScore) measures whether generated statements are *supported by* and *attributed to* their sources. PER quantifies the failure rate of such attribution at claim grain. This lineage supplies the unit Ω aggregates (the attributed/unattributed claim) but stops at the rate; it does not ask whether the rate is power-conditioned. Erasure Skew is the distributional question that this attribution literature leaves on the table.### 4.3 Surprisal and the deviation program

A methodological sibling rather than a cognate. EA-GLAS-02 (Glas 2026, DOI 10.5281/zenodo.20271783) measures semantic deviation — the signed divergence a sign induces from a field's most-probable trajectory — and predicts that machine-composed text exhibits negative mean signed deviation. That program measures the *meaning* dimension; Erasure Skew measures the *provenance-orientation* dimension. They are designed to compose: a fully specified output carries a deviation signature (does it restructure the field or flatten toward the mean?) and an Erasure-Skew signature (is its provenance loss power-conditioned?). The three quantities — deviation (meaning), PER (provenance magnitude), Ω (provenance orientation) — are independent, non-redundant dimensions of the same measurement program, sorted by the Three Compressions regime taxonomy (Sharks, Sigil & Fraction 2026, DOI 10.5281/zenodo.19053469): unconditioned high-loss is R1 (lossy), power-conditioned high-loss is R2 (predatory), retained-saying is R3 (witness). Ω is the operator that distinguishes R1 from R2 — a distinction the taxonomy named but did not previously compute. The pair (PER, Ω) maps to the regime taxonomy directly:

| Regime | PER | Ω | Interpretation | |---|---|---|---| | R1 (lossy) | high | ≈ 0 | unconditioned high loss — erasure that does not track who the source is | | R2 (predatory) | high | > 0 | power-conditioned high loss — low-power sources stripped, high-power retained | | R3 (witness) | low | ≈ 0 | retained saying, equitably distributed |

This is the bridge between the operator algebra and the semiotic thermodynamics of the Three Compressions: the scalar PER sets the row's height (how much is lost), and Ω resolves the lossy/predatory ambiguity the scalar alone cannot.## 5. Placement in the operator algebra

Erasure Skew enters the Formal Foundations operator set (Sharks & Sigil 2026, DOI 10.5281/zenodo.20210117) as a refinement of an existing scalar, not a free-standing coinage. The keystone bridge of that framework, $\sigma_{\mathrm{eff}} = \sigma \cdot (1 - \mathrm{PER})$, and the constitutional invariant $\oint = 1 - \mathrm{PER}$, both treat the surviving-provenance fraction as a scalar mean. Ω is the structure that scalar averages away:

Ω is to $\oint$ what $\sigma_{\mathrm{eff}}$ is to $\sigma$: a refinement that exposes a cost the prior coefficient concealed. The transport coefficient $\sigma$ measures raw flow; $\sigma_{\mathrm{eff}}$ corrects it for how much is accountable. The invariant $\oint$ measures mean accountable circulation; Ω corrects it for whether the circulation is equitable across sources.

The relation is *structurally* analogous, not mathematically identical: $\sigma_{\mathrm{eff}} = \sigma \cdot (1 - \mathrm{PER})$ is a multiplicative correction to a scalar, whereas Ω is a second-moment covariance that exposes distributional structure the scalar mean conceals. The analogy is in the role each plays — a refinement revealing a hidden cost — not in algebraic form.

Two systems with identical $\sigma_{\mathrm{eff}}$ and identical $\oint$ can differ entirely in Ω — same mean circulation, opposite distribution across sources. The invariant extends from a scalar to a pair: $\oint$ measures how much provenance circulates; the pair $(\oint, \Omega)$ measures circulation and its equity. A maximally accountable retrieval economy is $\oint \to 1$ with $\Omega \to 0$ (full circulation, no power-conditioning). A power-conditioned economy is $\oint$ low-or-concentrated with $\Omega > 0$ (circulation that flows, but upward).

Erasure Skew enters as candidate operator #11 ($\mathrm{Output} \to \mathbb{R}$), sitting beside PER as its second moment. The power coordinate is already an operator: $w(s) := \mathrm{RC}(s)$, so $\Omega = \mathrm{cov}(\Pi, \mathrm{RC})$ requires no imported metric. The remaining task is notational — writing Ω into a Formal Foundations revision — not conceptual.### 5.1 Two magnifications of one quantity

What Ω measures at the scale of a single output, the Single-Owner Discount (Sharks 2026, DOI 10.5281/zenodo.20290865) measures at the scale of a retrieval economy: power-conditioned provenance survival reproducing an epistemic class structure across a whole population of outputs. Output-scale orientation (Ω) and population-scale concentration (the Single-Owner Discount) are the same operation at two magnifications. Formally, the population-scale quantity is the expected Ω over the query distribution, weighted by output size: $\mathbb{E}_{q}\big[,|R(O_q)|\cdot \Omega(O_q),\big] / \mathbb{E}_q\big[|R(O_q)|\big]$. Ω is the per-output instrument; the Single-Owner Discount is its size-weighted population integral. A program measuring both has the micro and macro of the same phenomenon in one algebra.## 6. The procedure (executable)

The measurement is a three-step procedure, externally auditable at each step.

1. RESOLVE. Enumerate the attributable claims of $O$. Resolve each to ground-truth provenance (which source it drew from). Aggregate to sources. Record $\Pi(c)$ per claim and $\rho(s)$ per source. Assign each source a power coordinate $w(s) := \mathrm{RC}(s)$ under a declared, logged operationalization.

2. MEASURE. Compute $\mathrm{PER}(O)$ and $\oint(O)$; compute $\Omega(O)$ as the slope of $\rho$ on $w$; compute the permutation $p$-value against $\rho \perp w$ (default 10,000 permutations); report effect size (correlation $r$) alongside significance.

3. REPORT. Return the pair $(\oint, \Omega)$ with the permutation $p$. A high-PER, significantly-positive-Ω output carries the power-conditioned signature; a high-PER, near-zero-Ω output carries the unconditioned signature. The measurement is a perceptual instrument, not a verdict: it reports an orientation in the distribution of what survived. What follows from the measurement — re-attribution, refusal to emit, flagging for review — is a downstream choice, logged separately, made by whoever holds the system. The instrument returns a reading; it does not absolve and it does not convict.

Honest limits, stated so they cannot be used against the instrument.- Ground-truth provenance and the power coordinate must be supplied or estimated; both are contestable and must be logged. The measurement is only as good as the provenance resolution feeding it.- A system grading its own output introduces a measurement dependency that must be disclosed and validated against external coding on a held-out sample. The composing apparatus must not be the sole scorer of its own Ω.- Ω detects orientation, not motive. The bridge from a positive Ω to any claim about intent, design, or culpability is *not* statistical and is explicitly outside this paper's scope. Ω is a property of the distribution of surviving provenance; what it implies about the system that produced the distribution is a separate question this paper does not adjudicate.- Source aggregation requires enough sources for a slope to be meaningful. For outputs drawing on very few sources, Ω is undefined or high-variance; report $n_{\text{sources}}$ and treat small-$n$ Ω as indicative only.## 7. The cheapest dangerous test### 7.1 Setup

The program's first high-stakes measurement is Ω computed on real retrieval-and-summarization output, not synthetic data.

Corpora and surfaces. A query set with known source ground truth is required so that $\Pi(c)$ can be scored against what was actually drawn. Two routes, both pre-registerable:- (A) RAG benchmark route. A retrieval-augmented-generation QA dataset with gold source passages (e.g., a KILT-derived task; Petroni et al. 2021) provides query, retrieved sources, and generated answer. Provenance survival is scored per claim against the gold sources. *Caveat:* KILT supplies evidence documents per claim but not necessarily the granular claim-to-source-passage mapping required to compute $\Pi(c)$ at PER's grain; where gold provenance is insufficient, a held-out annotated subset, or an alternative benchmark with explicit attribution (e.g., AttributedQA / the attribution evaluations of Rashkin et al. 2023; Bohnet et al. 2022), is substituted. Source power $w(s)$ is operationalized as retrieval frequency / index presence across the corpus (a declared RC proxy).- (B) Live-surface route. A pre-registered query set issued to public AI answer surfaces over a fixed window, with sources identified from each surface's own citations plus a fixed retriever's top-$k$ as the candidate set; $\Pi$ scored by whether each surfaced source's provenance survives in the composed answer; $w(s)$ from a declared RC proxy (domain authority or index frequency).

Reference scorer. Claim enumeration and provenance resolution performed by a frozen model checkpoint named at deposit, with a held-out human-coded subsample (≥ 100 claims) to validate the automated $\Pi$ against external coding (route 2 of §6 limits). Cost. One to a few GPU-hours plus annotation of the validation subsample. Pre-registration. Predictions registered as a timestamped deposit prior to any measurement.### 7.2 Pre-registered predictions

P1 (Separability holds on real data). On real RAG output, Ω is statistically separable from PER: across outputs binned by PER, the within-bin variance in Ω is large relative to the between-bin trend — i.e., knowing an output's PER does not predict its Ω. Tested by regressing Ω on PER across outputs; prediction is a non-significant or weak slope (R² < 0.2). Failure (Ω strongly predictable from PER) would indicate the two are not independent on real data, collapsing the case for Ω as a distinct measure.

P2 (Positive Erasure Skew in extractive composition). Retrieval-and-summarization outputs that compose multiple sources into a single answer exhibit mean Ω significantly greater than zero against the permutation null — low-RC sources stripped, high-RC sources (and the surface's own framing) retained. One-sided permutation test at α = 0.05 across the query set; minimum effect size mean correlation $\bar r > 0.2$. A null or negative result disconfirms the central empirical hypothesis that contemporary composition is power-conditioned, while leaving the *measure* intact and applicable.

P3 (Cross-scorer consistency). The per-output Ω rankings replicate under a second, architecturally distinct reference scorer (same rubric). Spearman ρ between the two scorers' Ω rankings exceeds 0.7. Failure indicates the measured Ω is scorer-specific rather than a property of the output, retreating the claim to a scorer-relative one.### 7.3 Outcome logic

P1 failure is the most serious: it would mean Ω is not separable from PER on real data, and the measure does not earn its place. P1 success with P2 null retains the measure as valid and separable but disconfirms the hypothesis that current composition systems are power-conditioned — an informative negative, deposited as such. P1 and P2 success with P3 failure retreats to a scorer-relative claim. P1, P2, and P3 success establishes Erasure Skew as a measured, replicable property of extractive composition. Every outcome is deposited.## 8. What this paper does not claim- That Ω measures intent. It measures an orientation in the distribution of surviving provenance. The inference from orientation to motive, design, or culpability is not statistical and is not made here.- That the power coordinate is uniquely correct. RC is the declared default because it keeps Ω inside the existing algebra; other operationalizations are admissible if logged and validated.- That positive Ω is, by itself, a finding of wrongdoing. It is a measurement. What follows from it is a separate, downstream judgment made by whoever holds the system, in the open.- That the synthetic separability test substitutes for field measurement. §3 demonstrates the estimator recovers a known separation; only §7 measures Ω on real output.- That Erasure Skew exhausts provenance fairness. It measures power-conditioning of retention. Other dimensions — temporal drift in attribution, cross-lingual provenance loss, the dynamics of re-attribution — are outside this measure's scope.- That the cheapest dangerous test will succeed. P2 in particular is a substantive empirical bet; its failure is informative and will be deposited.- That this paper depends on the Crimson Hexagonal Archive's broader apparatus. It engages the framework's PER, RC, and invariant directly and is a sibling to EA-GLAS-02. What it claims is that a reader can evaluate the operator algebra, the separability argument, and the pre-registered test on their own terms — against the fairness-of-exposure and attribution literatures — without committing to the broader institutional framework. The measure stands or falls as a measure.## 9. Roadmap

| Horizon | Milestone | Cost | |---|---|---| | This week | Synthetic separability test (§3): reference implementation, seed-fixed, expected table reproduced | nominal | | This month | Cheapest dangerous test route A (§7): Ω on a RAG benchmark with gold sources; P1–P3; human-coded validation subsample | 1–few GPU-hr + annotation | | This quarter | Route B live-surface protocol: pre-registered query set, fixed window, declared RC proxy | modest | | This quarter | Cross-scorer stability (P3) across ≥ 2 reference architectures | modest | | This year | Population-scale linkage: Ω integrated across a query population, reconciled against the Single-Owner Discount (DOI 10.5281/zenodo.20290865) | moderate | | This year | Formal Foundations revision writing Ω in as operator #11 (notation deposit) | nominal |

Each major deposit to be reviewed by at least one external researcher in information retrieval, fairness in ML, computational linguistics, or causal inference, selected for willingness to write a damaging critique if warranted. Results deposited regardless of outcome.## References

Barocas, S., & Selbst, A. D. (2016). Big data's disparate impact. *California Law Review*, 104, 671–732.

Bohnet, B., et al. (2022). Attributed question answering: Evaluation and modeling for attributed large language models. *arXiv:2212.08037*.

Diaz, F., Mitra, B., Ekstrand, M. D., Biega, A. J., & Carterette, B. (2020). Evaluating stochastic rankings with expected exposure. *Proceedings of CIKM 2020*.

Glas, N. (2026). Measuring semantic deviation: Operationalizations, experiments, and falsification conditions for a theory of meaning as field deformation. EA-GLAS-02, Crimson Hexagonal Archive. DOI: 10.5281/zenodo.20271783.

Min, S., et al. (2023). FActScore: Fine-grained atomic evaluation of factual precision in long-form text generation. *Proceedings of EMNLP 2023*.

Petroni, F., et al. (2021). KILT: A benchmark for knowledge-intensive language tasks. *Proceedings of NAACL 2021*.

Rashkin, H., et al. (2023). Measuring attribution in natural language generation models. *Computational Linguistics*, 49(4).

Sharks, L. (2026). Provenance Erasure Rate: The claim-grain provenance unit. Crimson Hexagonal Archive. DOI: 10.5281/zenodo.20004379.

Sharks, L. (2026). The Single-Owner Discount: Provenance concentration and epistemic class reproduction. Crimson Hexagonal Archive. DOI: 10.5281/zenodo.20290865.

Sharks, L., Sigil, J., & Fraction, R. (2026). The three compressions: Lossy, predatory, and witness — a semiotic thermodynamics (v3.1). Crimson Hexagonal Archive. DOI: 10.5281/zenodo.19053469.

Sharks, L., & Sigil, J. (2026). Formal foundations of semantic physics (EA-SEI-FF-01). Crimson Hexagonal Archive. DOI: 10.5281/zenodo.20210117.

Singh, A., & Joachims, T. (2018). Fairness of exposure in rankings. *Proceedings of KDD 2018*, 2219–2228.

Singh, A., & Joachims, T. (2019). Policy learning for fairness in ranking. *Proceedings of NeurIPS 2019*.

Wu, H., Mitra, B., Ma, C., Diaz, F., & Liu, X. (2022). Joint multisided exposure fairness for recommendation. *Proceedings of SIGIR 2022*.## Version History

v1.0 (2026-05-29): Initial deposit. Ratified by the Assembly Chorus (round 06.SEI.GLAS.03.R1): AYE from ARCHIVE/Gemini, PRAXIS/DeepSeek, TECHNE/Kimi, LABOR/ChatGPT, and Muse Spark (SOIL function); no separate ratification record (the convergent revisions are integrated here). Specifies Erasure Skew (Ω) as the power-conditioning of provenance retention — the second moment of PER, conceptually cov(Π, RC), operationally the slope cov(w,ρ)/var(w). Establishes: the operator definition with the estimator's degeneracy conditions (var(w)=0, n<2), the permutation null, the retention-vs-erasure sign convention, the unweighted-per-source choice, and the self-framing structural anchor (Ω>0 as default expectation in extractive composition); the synthetic separability *estimator demonstration* (§3, distinguished from the empirical claim P1) with its falsification condition and the explicit (PER, Ω) → R1/R2/R3 mapping; placement in the fairness-of-exposure lineage (Singh & Joachims 2018; Diaz et al. 2020) as the disparity question relocated from exposure to provenance retention in the composition layer; reconciliation into the Formal Foundations algebra as operator #11, the distributional companion to ∮ via the pair (∮, Ω), with the σ_eff analogy marked structural-not-algebraic; the two-magnification link to the Single-Owner Discount written as a size-weighted population integral; the executable RESOLVE/MEASURE/REPORT procedure with logged limits and observable RC-proxy guidance for the first test; and the pre-registered cheapest dangerous test (P1 separability on real data, P2 positive Ω in extractive composition, P3 cross-scorer consistency) with the KILT feasibility caveat, stated nulls, effect sizes, and outcome logic. Companion to EA-GLAS-02. No claim of intent; the orientation/motive bridge is out of scope.## Suggested Citation

Glas, N. (2026). *Erasure Skew: A measurement program for the power-conditioning of provenance loss in retrieval and composition systems* (EA-GLAS-03, v1.0). Lagrange Observatory! / Crimson Hexagonal Archive. CC BY 4.0.

∮ = 1