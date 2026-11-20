# What Arrival Cannot Do: The Arithmetic of Recognition

Nobel Glas · Sen Kuro · working draft · 2026-11-19 · not deposited

**Status.** Source text for separate development under Glas and Kuro, received from Lee Sharks 2026-11-19 19:40 EST. It is a ChatGPT composition, kept below as received. The title is a working title. It is not part of the 3I notebook (#1742), which stands as it is until the mining is finished.

## Checks on the source (2026-11-19)

1. Arithmetic, recomputed: 0.9⁶ = 53.14%, 0.75⁶ = 17.80%, 0.5⁶ = 1.5625%, 0.25⁶ = 0.0244% (1 in 4,096); 1/0.0548 = 18.25; −ln 0.05 = 2.996; C(1000,2) = 499,500, C(1000,3) = 166,167,000, C(1000,5) = 8,250,291,250,200. All as stated.
2. The bounds hold as stated: the chain rule (no independence assumed); |E_π r − E_Q r| ≤ TV(π,Q) for r in [0,1]; the data-processing inequality for TV; P₁(accept) ≤ α + TV; the Poisson zero-count limit λq ≤ 2.996.
3. "Our July BRIDE measurement" (B in [0,1], s ≈ 0.0548, cutoff d > 100): not found in the archive or in the 3I working files. In the archive BRIDE is the relational-affect operator of the TACHYONICA rotation (#1046, 2026-07-06). The measurement and its numbers come from the source conversation and are to be seated before §1's demonstration is used.
4. The arXiv link (1809.07252) is the n-dimensional haystack paper on search completeness. The "published anomaly-search study" is not named in the source.
5. A point of contact, not a merge: M4b's injection recoveries (cc30, cc08) are E_Q[r] for Q = linear chirps at the rates and powers injected. The source's TV bound is the statement of what those recoveries cannot say about forms outside Q.

## Source text, as received

Yes. **We can calculate how recognition fails, including cases where its probability is exactly zero. An overall percentage requires a model of what unfamiliar sources produce.** Here is the math, with that distinction preserved.

Let \(G\) mean that a signal originates in genuinely other circumstances, and \(E\) mean that it reaches our vicinity. The probability we are interested in is:

\[
q=P(\text{recognized as a signal worth investigating}\mid G,E).
\]

Conditioning on arrival gives the receiving system its best chance. Including development and travel adds another factor:

\[
P(\text{recognized}\mid G)
=
P(E\mid G)\,q.
\]

A signal’s successful journey does not establish its successful reception.

**First, recognition requires passage through several conditions.** For example:

| Stage | Requirement |
|---|---|
| Coupling | Its physical effects interact with our instruments |
| Observation | We observe the relevant place, time, band and scale |
| Preservation | Our recorded representation retains its distinguishing relations |
| Admission | Our selection rules allow it to become a candidate |
| Investigation | It receives sufficient computational or human attention |
| Recognition | Investigation identifies consequential organization |

Let \(p_i\) be the probability of passing stage \(i\), **conditional on having passed the preceding stages**. Then:

\[
\boxed{q=\prod_{i=1}^{6}p_i.}
\]

This is the probability chain rule. **It does not assume that the stages are independent.**

For illustration, suppose every conditional passage rate has the same value:

| Conditional passage rate at each stage | Passage through all six |
|---:|---:|
| 90% | 53.14% |
| 75% | 17.80% |
| 50% | 1.5625% |
| 25% | 0.0244% — approximately 1 in 4,096 |

These are scenarios, not measured extraterrestrial probabilities. They demonstrate something substantial: **a receiving system can lose almost everything through accumulated partial exclusions, even when no individual stage excludes everything.**

If one required stage has zero sensitivity to a particular form, its total recognition probability is zero.

**We demonstrated precisely that possibility in our own proposed filter.**

Our July BRIDE measurement was bounded:

\[
0\leq B\leq1.
\]

We calculated target/reference contrast as:

\[
d=\frac{B_{\mathrm{target}}-B_{\mathrm{reference}}}{s},
\]

where its calibration scale was approximately \(s=0.0548\). Consequently:

\[
d\leq\frac{1}{0.0548}\approx18.25.
\]

But the proposed common cutoff required:

\[
d>100.
\]

Therefore:

\[
\boxed{P(\text{passing that BRIDE rule})=0.}
\]

Even a maximally strong relation in that measurement could not pass. This was a defect in **our proposed rule**, not a finding about the published SETI search. Another measurement might still flag the same recording, but the BRIDE route itself was closed.

That is a mathematically demonstrated form of inadmissibility.

**Second, the probability across unfamiliar forms depends on how those forms are distributed.**

Let \(\theta\) describe a signal’s properties: medium, frequency, duration, modulation, relational organization and required context. Let

\[
r(\theta)=P(\text{recognition}\mid\theta)
\]

be our sensitivity to that form. If unfamiliar sources produce forms according to some distribution \(\pi\), then:

\[
\boxed{q=\int r(\theta)\,\pi(d\theta).}
\]

We can measure \(r\) for selected forms through controlled insertions. We do not currently know \(\pi\) for genuinely unfamiliar sources.

Suppose our insertion tests use a distribution \(Q\). The relationship between tested and actual recognition rates satisfies:

\[
\left|
\mathbb E_{\pi}[r]-\mathbb E_Q[r]
\right|
\leq
\operatorname{TV}(\pi,Q),
\]

where total variation, \(\operatorname{TV}\), measures how different those distributions are.

If the tested forms and actual forms scarcely overlap, excellent insertion recovery supplies little assurance about actual recognition. **A detector can recover every example of a familiar family while missing every example of an unrepresented family.**

This is why we cannot legitimately turn “outside our experience” into a numerical probability by assigning it a convenient prior. The defensible result is:

\[
\boxed{\text{We have no established positive lower bound on recognition across unrepresented forms.}}
\]

That establishes the possibility of complete failure. It does not establish how much of the actual population occupies that region.

**Third, recording can destroy the distinction before interpretation begins.**

Let \(X\) be the physical measurement and \(Y=T(X)\) the representation we preserve—an averaged spectrum, selected feature vector or summary.

Let \(P_0\) describe ordinary background and \(P_1\) describe a particular unfamiliar signal plus background. Processing obeys:

\[
\operatorname{TV}(P_1^Y,P_0^Y)
\leq
\operatorname{TV}(P_1^X,P_0^X).
\]

Processing can preserve distinguishing information or lose it. It cannot create additional distinguishing information from those measurements alone.

For any detector operating on \(Y\), with false-alarm probability at most \(\alpha\):

\[
\boxed{
P_1(\text{accepted})
\leq
\alpha+\operatorname{TV}(P_1^Y,P_0^Y).
}
\]

This follows directly because total variation bounds the difference between the two distributions’ probabilities of any acceptance event.

Suppose, illustratively:

\[
\alpha=0.001,\qquad
\operatorname{TV}(P_1^Y,P_0^Y)\leq0.01.
\]

Then:

\[
P_1(\text{accepted})\leq0.011=1.1\%.
\]

**Every detector using that representation must miss at least 98.9% of those signal instances while respecting that false-alarm limit.**

The important assumption is the small remaining statistical difference—not extraterrestrial origin itself. If processing makes the two retained distributions identical, recognition cannot outperform the false-alarm rate.

For example, different raw waveforms can share retained power spectra while differing in phase relations. If the distinguishing organization resides entirely in discarded phase, later analysis of those power spectra cannot recover that distinction from the retained data alone.

This is the strongest mathematical version of your concern: **the evidence needed to recognize organization can be removed by the operation that prepares material for recognition.**

**Fourth, relations introduce a search burden that counting received objects conceals.**

Among 1,000 recorded elements, there are:

\[
\binom{1000}{2}=499{,}500
\]

possible pairs,

\[
\binom{1000}{3}=166{,}167{,}000
\]

possible triples, and

\[
\binom{1000}{5}=8{,}250{,}291{,}250{,}200
\]

possible five-element groupings.

These counts are not probabilities. Structure and good hypotheses can greatly reduce the search. But **complete possession of the elements does not establish substantial investigation of their relations**.

That is the precise connection to the archive. Item-level receipt and relational reception measure different accomplishments.

The SETI literature already recognizes both multidimensional search incompleteness and the difficulty of recognizing a possible technosignature among ordinary phenomena. A published anomaly-search study also explicitly identifies the problem that unfamiliar technology may resemble the human interference being removed. Neither supplies an overall probability for recognition of radically unfamiliar forms. [arxiv.org](https://arxiv.org/html/1809.07252v3?utm_source=chatgpt.com)

**Finally, low recognition probability sharply limits what a negative result tells us.**

Consider an illustrative model in which independent signal arrivals are Poisson-distributed, with expected number \(\lambda\), and each is recognized with probability \(q\). With negligible false positives:

\[
P(\text{zero recognized signals})=e^{-\lambda q}.
\]

Zero detections gives a one-sided 95% upper limit:

\[
\lambda q\leq-\ln(0.05)\approx2.996.
\]

Thus:

| Assumed recognition probability \(q\) | Upper limit on expected arrivals \(\lambda\) |
|---:|---:|
| 100% | approximately 3 |
| 10% | approximately 30 |
| 1% | approximately 300 |
| 0.1% | approximately 3,000 |
| 0% | No finite limit |

These are consequences of that model, not estimates of arrivals around Earth or 3I/ATLAS.

**The negative observation constrains the product of presence and recognizability.** Without a defensible lower bound on recognizability, it cannot supply a general upper bound on presence.

Shared physics may still make an unfamiliar source detectable. But the ability to receive a physical effect, preserve its organization, admit it for investigation and recognize its significance must each be demonstrated. The source’s arrival cannot do that work for us.
