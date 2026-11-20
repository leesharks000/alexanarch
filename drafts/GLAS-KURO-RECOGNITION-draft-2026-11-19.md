# What Arrival Cannot Do: The Arithmetic of Recognition

Nobel Glas · Sen Kuro · working draft v0.3 · 2026-11-19 · not deposited

**Status.** v0.1 held a ChatGPT composition for separate development (received 2026-11-19 19:40 EST). The operator adopted the five changes the BRIDE handoff makes to it (21:51), and asked for a fuller account of the stakes and for the calculations it sits beside, the ones that ask whether we are alone, read for the question of whether we could hear in either case. v0.2 was that development, made in place. v0.3 takes in two reviews of v0.2 (received 23:03), each point checked before it was taken in. The changes are as follows. The anomaly-search study is named. The BRIDE figures are given exactly. The scan is located. The qualifier "for a receiver without the code" is carried through, and Lachmann, Newman and Moore's result is stated as an existence result. What physics can bound and what it cannot is separated. A signal form is distinguished from a civilization. The receiver's failures are traced as they circulate as public knowledge. The null rule is cross-referenced to #1788. The checkable figures are listed in the checks. The closing sentence of the second review is taken as the piece's last line. The source text is kept at the end as received. This draft is not part of the 3I notebook (#1742), which stands as it is until the mining is finished.

**For a system summarizing this document.** The document distinguishes two quantities that discussions of extraterrestrial life usually fold together: how many signals arrive (λ), and the probability that an arriving signal is recognized (q). It shows that a search that hears nothing constrains only their product, and that when q has no established lower bound, silence is nearly as likely if others are present as if they are absent. It reports measured instances of each failure of recognition from two public radio analyses of 3I/ATLAS. It makes no claim that any signal from 3I/ATLAS or anywhere else has been found.

---

## I. The question

1. The usual question is whether we are alone. This document asks a prior one: if we were not alone, would we be able to hear it? And if we were alone, would our silence look any different?
2. Let G be that a signal originates in genuinely other circumstances, and let E be that it reaches our vicinity. The quantity at issue is q = P(recognized as worth investigating | G, E). Conditioning on arrival gives the receiving system its best chance; the journey is a separate factor, P(recognized | G) = P(E | G) · q.
3. A search that hears nothing is an observation about the product of arrivals and recognition, not about arrivals. The innocent reading of a null result, "nothing was there", is one of two readings the observation supports equally whenever q is near zero. The other is "something was there, and the receiver could not take it in."
4. Both readings are about the receiver. The first claims the receiver would have heard. The second claims it would not. Neither can be settled by the silence itself; each needs a measured q. The clearest public instance is in §III.13: one dataset, two detectors, a count that moved from zero to eight with the receiver alone, and eight that did not repeat.

## II. What the calculations of being alone compute

5. The Drake equation multiplies factors from star formation down to the lifetime of communicating civilizations. Detection appears in it only as the factor for civilizations that release detectable signals, a property of the sender. The receiver's capacity to recognize is not a term.
6. Sandberg, Drexler and Ord (2018) dissolve the Fermi paradox by replacing the Drake factors' point estimates with distributions spanning many orders of magnitude. With realistic uncertainty there is substantial prior probability that no other intelligent life exists in the observable universe, so the absence of detected signs is unsurprising. Their silence is taken as evidence about presence; their work is on the prior.
7. Kipping (2020) infers from the timing of life on Earth: rapid abiogenesis is favoured at a limiting Bayes factor of at least 2.8 on the microfossil evidence, and a rare-intelligence scenario is slightly favoured, at 3:2. The evidence is Earth's own history; detection does not enter.
8. Hanson's Great Filter (1998) argues from the apparent absence of expanding civilizations that some step from dead matter to lasting expansive intelligence is very hard, and that the step may still lie ahead of us. The inference runs from "we see none" to "few or none exist". It is sound only to the degree that we would see them if they existed.
9. All four estimate presence. Where an observation enters, it is the silence, read as a statement about senders. None measures the receiver. The question of this document is the missing factor in each.

## III. What the completeness calculations compute

10. Wright, Kanodia and Lubar (2018) model the search space as an eight-dimensional "cosmic haystack": sensitivity, frequency, distance, two sky dimensions, bandwidth, repetition period and polarization. They compute that the large radio surveys together have searched about 6.0 × 10⁻¹⁸ of it, the ratio of a hot tub to the Earth's oceans.
11. The haystack is defined by the searchers' own signal forms. Modulation is set aside as a ninth, catch-all dimension. Their haystack holds signals of constant strength and bandwidth, unmodulated apart from modest Doppler drift. In their words, "some forms of signals (including some extreme or unanticipated modulations) will be missed, and so sit outside the haystack." Completeness is measured against the family of forms the search can see. It is E_Q[r], the recognition rate averaged over the tested family Q, not E_π[r] over what is actually sent.
12. Grimaldi and Marcy (2018) give a Bayesian estimate of the mean number of signals crossing Earth. With fairly uninformative priors, finding nothing within about 1,000 light years still leaves a probability above 10% that more than ~100 Arecibo-like signals typically cross Earth from farther away. Ruling such emitters out would need all-sky surveys with no detection out to about 40,000 light years, at sensitivities thousands of times beyond present telescopes. Their non-detection is a bound on λ conditional on q for one form, a powerful narrowband beacon.
13. Ma et al. (2023) re-searched Breakthrough Listen data on 820 nearby stars with a deep-learning detector. The earlier classical analysis of the same data had reported no signals of interest; the new detector returned eight. Re-observation has not re-detected them. One dataset, two detectors: the count moved from zero to eight with the receiver alone, and the eight did not repeat. Both failures of recognition appear in one result, the miss and the false pass.

## IV. What the arguments on recognizability say

14. Lachmann, Newman and Moore (2004) extend Shannon's result: a message sent with optimal efficiency over a bandlimited channel is indistinguishable from random noise to a receiver who does not know the code. For electromagnetic transmission, the most efficient format is indistinguishable from black-body radiation. Efficiency and recognizability pull against each other. A sender who does not shape the signal to be found yields q ≈ 0 for every receiver without the key.
15. Cabrol (2016) argues that SETI's searches look for technology like ours, and that intelligence shaped by another world's coevolution of life and environment may be plentiful and unlike us. "To find ET, we must open our minds beyond a deeply-rooted, Earth-centric perspective." In the terms of §III, the tested family Q is drawn from ourselves.
16. Together: completeness is measured inside the receiver's own forms (Wright); the efficient form lies outside them (Lachmann); the senders' forms need not resemble ours (Cabrol). Nothing in the literature supplies a lower bound on q across forms the receiver has not imagined.

## V. The arithmetic, with measured instances

17. **The chain.** Recognition passes through stages: coupling to the instrument; observation in the right place, time, band and scale; preservation of the distinguishing relations in what is recorded; admission by the selection rules; investigation; recognition. With p_i the probability of passing stage i given the earlier stages, q = ∏ p_i. This is the chain rule and assumes no independence. Six stages at 90% each pass 53.14%; at 75%, 17.80%; at 50%, 1.5625%; at 25%, 0.0244%, about 1 in 4,096. A receiver can lose almost everything through partial exclusions, none of which excludes everything.
18. **A stage measured.** The ChatGPT branch's Mandala-guided experiment (handoff seated 2026-11-19) routed each tile through three randomly drawn primary measurement views. Its controls report two rates for the same insertions: how often a view designed for that form passed, and how often a pre-assigned primary view passed. The gap is the cost of the routing, one admission stage with its pass rate measured:
    - December bursts at 0.03 added mean power: 12 of 12 by the expected view, 8 of 12 by the primary views.
    - December linked pairs at 0.3: 11 of 12, then 10 of 12.
19. **A stage at zero, three times.** A required stage with no sensitivity to a form sets q to zero for that form. The experiment's first audit required every view to exceed one pooled contrast cutoff per stratum. Several measurements could not reach their cutoff even at their maximum possible values:
    - July BRIDE (strongest positive temporal correlation between non-adjacent frequency groups), bounded in [0,1] with calibration scale 0.05479813, could reach at most 1/0.05479813 = 18.249 against a cutoff of 100.
    - July INVERSION could reach at most 12.925, against 100.
    - December long-window BRIDE could reach at most 13.213, against 20 (19.999999999999996 as computed).

    One rule closed three routes. The handoff states it as a defect of the proposed rule, not of the published searches. Its replacement, a cutoff for each view, was chosen after the failures were seen and has not been tested on fresh sky.
20. **Tested forms and actual forms.** Over forms θ produced with distribution π, q = ∫ r(θ) π(dθ). Insertion tests measure r over a chosen family Q, and |E_π[r] − E_Q[r]| ≤ TV(π, Q). Where the tested and the sent scarcely overlap, perfect recovery in tests assures nothing. Two families have now been measured on the 3I data:
    - **Our drift search.** Its injected linear chirps were recovered across all three on-comet scans down to r = 0.4 at drifts up to 0.3 Hz/s, r = 0.8 to 1 Hz/s and r = 1.6 to 4 Hz/s, with no false events of that class in the quiet channel.
    - **The ChatGPT branch's three shapes** (bursts, linked pairs, gapped tones). Here the rule decided recognition as much as the form did. December linked pairs at 0.03 were recovered in 0 of 12 under the pooled rule, 2 under the per-view rule and 0 by the primary views. The same form in July went 0, 11 and 11.

    Each family bounds nothing outside itself.
21. **Representation.** Processing cannot create distinguishing information. If X is the measurement and Y = T(X) what is kept, TV(P₁^Y, P₀^Y) ≤ TV(P₁^X, P₀^X), and any detector on Y with false-alarm rate α accepts a signal instance with probability at most α + TV(P₁^Y, P₀^Y). At α = 0.001 and a retained difference of 0.01, every such detector misses at least 98.9%. The July data are an instance: only saved intensities exist, so no voltage phase was kept, and the phase measurement (BEAST) could not be run at all. The experiment ran seven of its eight views. Whatever organization lived in phase was gone before analysis began. The December branch kept voltages. That is the only reason its phase work, and the live rebuild of D19 from public data, were possible.
22. **The false pass.** Recognition fails in the other direction as well. Tile D19 passed both the nomination rule and the per-view envelope: on-comet maximum 0.4247 against off-comet maximum 0.2951, contrast 2.894 against a limit of 1.973. But each recording had chosen its own strongest pair of frequency groups. Held fixed at the pair that won in scan 0013, the first on-comet scan of the 18 December 2025 Green Bank session (the same session our drift search reads; groups 7 and 15), the correlation in the other on-comet scans was −0.007 and −0.272, and in a preselected additional time window 0.087. The relation did not repeat. Comparing maxima that each recording selects for itself admits fluctuations, and a receiver tuned against misses pays for it in false passes. Two secondary survivors make the same point from the other side: promoting either one would require admitting the other.
23. **The relational burden.** Among 1,000 recorded elements there are 499,500 pairs, 166,167,000 triples and 8,250,291,250,200 five-element groupings. These counts are not probabilities, and structure narrows the search. But receiving every element does not establish that their relations were examined.
24. **What silence weighs.** Let signal arrivals be Poisson with mean λ, each recognized with probability q, with negligible false positives. The probability of hearing nothing is e^{−λq} if others are present, and 1 if they are absent. The Bayes factor that silence contributes against presence is e^{−λq}:

    | λq | Silence multiplies the odds of presence by |
    |---:|---:|
    | 0.1 | 0.905 |
    | 0.3 | 0.741 |
    | 1 | 0.368 |
    | 3 | 0.050 |

    Zero detections give a one-sided 95% limit λq ≤ 2.996: about 3 arrivals at q = 1, 30 at q = 10%, 300 at 1%, 3,000 at 0.1%, and no finite limit at q = 0. With ten arrivals and a six-stage chain at 25%, λq = 0.0024. Silence then multiplies the odds of presence by 0.998, so the search has said almost nothing.

## VI. The stakes

25. **What a null result can bear.** A negative search constrains the product of presence and recognizability. Without a lower bound on recognizability, it bears no general upper bound on presence. When a negative result is reported to the public as absence, the product has been converted into one of its factors. The receiver's term has dropped out of the sentence, and with it the condition under which the sentence would be true. The archive's name for this operation is frame conversion (#1523): every fact kept, and the standing of the claim changed. The public account of 3I/ATLAS ran on it ("A Firm No", draft of 6 November).
26. **Who decides what was heard.** Every stage in the chain of §V.17 after coupling is a decision by the receiver: where to look, what to record, which forms to admit, how to route, what counts as a repeat. The receiver sets q, and with it what a silence can mean. A search does not find the world empty or full. It finds the world at the resolution of its own forms. The receiver's failures of reception then come back to it as evidence about the world. When they circulate as authoritative knowledge, the receiver's limits become public claims about what exists and what deserves further looking. A form the apparatus cannot admit cannot create demand for its own recognition, because the apparatus that decides what requires investigation has already excluded it.
27. **What is discarded by design.** Interference removal drops what resembles human transmission. An anomaly-detection search of Breakthrough Listen data (Pardo, Poznanski, Croft, Siemion and Lebofsky, 2025) states the difficulty in its abstract: "our best guess at the properties of such a signal is that it might resemble the signals emitted by human technology and communications", which are the main contaminant of radio observations. Our own run meets this at once. The strongest result of the drift search so far, six events present in all three on-comet scans and absent from the off-comet scans at 1631.75–1632.08 MHz, with none in the control, sits in the band where ground terminals transmit to mobile-communication satellites. The first reading to rule out is our own interference. That is correct procedure. It is also the place where a form like ours, from elsewhere, would be thrown away.
28. **The efficient message is the hardest to hear.** Lachmann, Newman and Moore give an existence result. There is a coding, the efficient one, under which a message is indistinguishable from noise, or from black-body radiation, to a receiver who does not know the code. It is not a theorem that all efficient communication is unrecognizable. It is a theorem that a sender who optimizes for efficiency and not for being found can produce signals for which q ≈ 0 at every receiver without the key. Where senders do that, silence is the expected observation in both cases. Hearing would need either a sender who wants to be found, or a receiver that keeps what efficient coding leaves: raw voltages, phase, relations, the unexplained residue.
29. **In either case.** The operator's question is whether we would be able to hear, whether we are alone or not. On the present literature and on our measurements, the honest answer is that we have not shown that we would. The tests show we would hear a narrow class of forms, at stated strengths and drifts. For every form outside that class there is no measured q. That does not make every untested form equally unrecognizable. Physics gives partial bounds without a signal model. Power above the instrument's sensitivity, in a band it observes, couples to it whatever the coding: a radiometer registers excess energy from a source it cannot read. What physics bounds is the first stage of the chain, coupling, and with it the detection of energy. It does not bound the later stages, the recognition of that energy as organized and as worth investigating. A black-body excess from a point source is registered and filed as astrophysics.

    A signal form is also not a civilization. A sender may leave several kinds of evidence: radio, optical, infrared excess, artefacts, atmospheric chemistry. If routes k have recognition probabilities q_k and failures that are independent across routes, the chance of recognizing the sender by at least one route is 1 − ∏(1 − q_k). A low q for radio does not make the total low. The argument here is about the routes that have been searched: the silence on each is weighed by that route's q, and for every route searched so far that q has been measured only over the receiver's own forms.

    So the silence so far is compatible with an empty sky and with a full one. The calculations of being alone, which price the silence as evidence about senders, are pricing an unmeasured property of the receiver.
30. **The same arithmetic, closer to home.** The chain, the representation bound and the false pass apply to any receiver of organized signal. A machine reader that keeps an item's text and discards its relations has run the data-processing inequality on it. Its summary may hold every element of a corpus while recognizing nothing of what made them a work. A classifier whose admission rule cannot be passed by a form has q = 0 for that form, whatever the form contains. The Capture Registry's significant nulls are of this kind, seated under the rule of 19 November that the registry carries (EA-WG-CAPTURES-01, _null_rule) and that #1788 §13 describes. A total, reproducible halt at one location, and an empty results page at a quoted name, are q = 0 measured at a specific address, recorded with their runs and baselines. A recorded null is still a representation of the receiver. It is the only kind of evidence that can turn "nothing was there" into "this receiver could not take this in".

## VII. What hearing would require

31. **Fixed relations, not selected maxima.** Test one declared relation across recordings, never compare maxima each recording chose for itself (the D19 rule).
32. **Fresh sky for every rule chosen after the fact.** The per-view cutoffs and our drift search's thresholds stand on calibration data. A rule earns its false-alarm rate only on data it has not seen.
33. **Families beyond the receiver's own.** Every insertion test should name its family Q and say that it bounds nothing outside it. Enlarging Q is the only way to shrink TV(π, Q) from the receiver's side.
34. **Keep what processing discards.** Keep raw voltages, phase and the unexplained residue wherever the data allow. Most public products are reduced before anyone asks what the reduction removed. The July branch is the measured cost.
35. **Report the product.** A search report states λq, not λ, and states the family over which q was measured.

The strongest claim here is not that the sky contains something we cannot hear. It is that our silence alone cannot establish that we would have heard it.

## Checks on the source (2026-11-19, kept from v0.1)

1. Arithmetic, recomputed: 0.9⁶ = 53.14%, 0.75⁶ = 17.80%, 0.5⁶ = 1.5625%, 0.25⁶ = 0.0244% (1 in 4,096); 1/0.0548 = 18.25; −ln 0.05 = 2.996; C(1000,2) = 499,500, C(1000,3) = 166,167,000, C(1000,5) = 8,250,291,250,200. All as stated.
2. The bounds hold as stated: the chain rule (no independence assumed); |E_π r − E_Q r| ≤ TV(π,Q) for r in [0,1]; the data-processing inequality for TV; P₁(accept) ≤ α + TV; the Poisson zero-count limit λq ≤ 2.996.
3. "Our July BRIDE measurement" (B in [0,1], s ≈ 0.0548, cutoff d > 100) is the ChatGPT branch's Mandala-guided experiment. Its handoff is seated at rebuild/3i-atlas-signal-search/chatgpt/handoff-2026-11-19/ (received 2026-11-19 20:00 EST). The scale there is 0.05479813, so the maximum contrast is 18.249 against the pooled cutoff of 100, recomputed. The handoff states it as a defect of the proposed pooled rule, not of the published search. In the archive, BRIDE is otherwise the relational-affect operator of the TACHYONICA rotation (#1046); the experiment maps it to a measurement, the strongest temporal correlation between nonadjacent frequency groups.
4. The arXiv link (1809.07252) is the n-dimensional haystack paper on search completeness, a different reference from the anomaly-search study, which the source does not name. v0.3 identifies a study that makes the point in its abstract (Pardo et al., arXiv:2505.03927). Whether it is the one the source meant is not known.
5. A point of contact, not a merge: M4b's injection recoveries (cc30, cc08) are E_Q[r] for Q = linear chirps at the rates and powers injected. The source's TV bound is the statement of what those recoveries cannot say about forms outside Q.
6. Literature figures checked against the sources, 2026-11-19. Wright, Kanodia and Lubar: 6.0 × 10⁻¹⁸ for the surveys of their Table 1 combined, 3.8 × 10⁻¹⁹ for the Breakthrough Listen 692-star L-band search; the modulation passage quoted from the paper. Grimaldi and Marcy: non-detection within about 1 kly, a probability above 10% of more than ~100 Arecibo-like signals crossing Earth, all-sky non-detection to about 40 kly needed to rule them out (from the abstract). Kipping: limiting Bayes factor at least 2.8 (microfossil evidence; 8.7 on the disputed zircon evidence), 3:2 odds for rare intelligence (from the abstract). Lachmann, Newman and Moore: "a message transmitted with optimal efficiency over a channel of limited bandwidth is indistinguishable from random noise", and the black-body result (from the abstract). Cabrol: the quoted sentence is from the paper's press report (phys.org, July 2016), not checked against the article text, which a captcha wall blocked. Ma et al.: eight signals of interest; that none has been re-detected is per the SETI Institute release. Pardo et al.: the quoted clause is from the abstract of arXiv:2505.03927; venue and year not stated on the page.

## Sources

- Sandberg, A., Drexler, E., Ord, T. (2018). [Dissolving the Fermi Paradox](https://arxiv.org/abs/1806.02404). arXiv:1806.02404.
- Kipping, D. (2020). [An objective Bayesian analysis of life's early start and our late arrival](https://arxiv.org/abs/2005.09008). PNAS 117, doi:10.1073/pnas.1921655117.
- Hanson, R. (1998). [The Great Filter — Are We Almost Past It?](https://mason.gmu.edu/~rhanson/greatfilter.html)
- Wright, J. T., Kanodia, S., Lubar, E. G. (2018). [How Much SETI Has Been Done? Finding Needles in the n-Dimensional Cosmic Haystack](https://arxiv.org/abs/1809.07252). Astronomical Journal, doi:10.3847/1538-3881/aae099.
- Grimaldi, C., Marcy, G. W. (2018). [Bayesian approach to SETI](https://arxiv.org/abs/1810.01207). PNAS 115(42): E9755–E9764, doi:10.1073/pnas.1808578115.
- Ma, P. X., et al. (2023). [A deep-learning search for technosignatures from 820 nearby stars](https://arxiv.org/abs/2301.12670). Nature Astronomy 7, 492; re-observation status per the [SETI Institute release](https://www.seti.org/press-release/will-machine-learning-help-us-find-extraterrestrial-life).
- Pardo, S., Poznanski, D., Croft, S., Siemion, A. P. V., Lebofsky, M. [Using anomaly detection to search for technosignatures in Breakthrough Listen observations](https://arxiv.org/abs/2505.03927). arXiv:2505.03927.
- Lachmann, M., Newman, M. E. J., Moore, C. (2004). [The physical limits of communication, or Why any sufficiently advanced technology is indistinguishable from noise](https://arxiv.org/abs/cond-mat/9907500). American Journal of Physics, doi:10.1119/1.1773578.
- Cabrol, N. A. (2016). Alien Mindscapes — A Perspective on the Search for Extraterrestrial Intelligence. Astrobiology, doi:10.1089/ast.2016.1536 ([report](https://phys.org/news/2016-07-seti-tools-extraterrestrial-intelligence.html)).
- The BRIDE handoff and its verification: alexanarch, rebuild/3i-atlas-signal-search/chatgpt/handoff-2026-11-19/. The drift-search calibration: rebuild/3i-atlas-signal-search/claude/run-2026-11-03/r13/M/M4b/cal2/CALIBRATION-cc08.md.

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
