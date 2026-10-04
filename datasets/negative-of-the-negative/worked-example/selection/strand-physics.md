# Strand: physics / classifier collapse — claim ledger from the two defining papers

Both files read in full: `data/texts/AXN-03AF-text.md` (1,846 lines, including the appended witnesses W1–W3) and `data/EA-MMRS-LOUD-EXCLUSION-03.md` (736 lines, including Appendices A–D). Every quote below is copied exactly from the file. Section names are the papers' own headings.

## Identifier notes (checked against data/registry.json, not fixed)

- **#932.** The registry gives `AXN:03AF.COMPOSITIONAL.🌿🌕🕒⏬🌺💛`, dated 2026-06-29. The file's front matter and closing line agree (03AF, #932). The body's header and Provenance section do not: they say "AXN:03AE.OPERATIVE.🃏🫶⛩️🔐🌳❤️ — deposit #931 … combined six-document family deposit". In the registry, #931 is the separate OAR Protocol (`AXN:03AE.OPERATIVE.🔮🌘📋📋🏺✨`), with different glyphs. So the body still describes a single combined deposit that the registry later split into two.
- **#1.** The registry gives `AXN:0001.GOVERNANCE.♍🜁🏴⌛🍃💫`, dated 2026-06-19. The file's SPXI block says "v8.1" and 2026-06-20. The italic header says "v9.1 (FINAL) — June 20, 2026". The abstract says "six concepts", but the §16 conclusion lists seven: it adds the reflexive governance problem.
- **Shumailov's year in #1.** §6 cites him as "Shumailov et al., 2023" (no reference entry has that year) and also as "(Shumailov et al., 2024)". The reference list has only the 2024 *Nature* paper.

---

## PAPER A — #932, EA-SEI-COLLAPSE-SYNTHESIS-01 v0.3, *Classifier Foreclosure in Physical Measurement* (2026-06-29)

### A.1 What the paper says model collapse is

The paper takes model collapse out of generative language models and applies it to **discriminative classifiers that mediate physical measurement**, using the LHC trigger systems (CMS AXOL1TL and CICADA, ATLAS GELATO L1 and HLT) as its proof-of-concept site. It separates two things.

- **Foreclosure** is a structural feature that is present now. The representation, objective, score, threshold, retention policy and model feedback each remove distinctions before any validation can test for them.
- **Recursive phenomenal collapse** is "an unmeasured possible consequence of accumulated foreclosure and feedback". It happens when data selected by one model generation becomes the basis for training the next. The paper treats this as a hypothesis, not a finding.

Appendix W1 (Kimi-K2) defines "classifier collapse" as the *discriminative analogue* of Shumailov-style generative collapse. Where generative models forget the tails of a distribution, classifiers "never learn the tails". Appendix W3 (ChatGPT) gives the strict recursive definition. It separates mere "phenomenal attrition" from collapse, and puts collapse at the point where Q_t feeds generation t+1. The model-collapse signature it uses is tail loss while aggregate performance stays stable.

The paper proposes a measure (OAR, the Ontological Assimilation Rate) and two proxies (BAR, the Benchmark Assimilation Rate, and IAI, the Inversion Asymmetry Index). It retracts both of its own earlier quantitative bounds. It states falsification conditions. It extends the concept to repositories, AI Overview, search ranking, content moderation and clinical decision support only as a **homology hypothesis** to be tested one domain at a time.

### A.2 Claims

| claim_id | claim | kind | modality | locus | verbatim quote |
|---|---|---|---|---|---|
| P932-01 | The witnesses converge on one claim: deployed anomaly detection cannot detect what its architecture has foreclosed, and its validation framework cannot detect that failure. | interpretation | interpretation | §2. The Convergent Synthesis | "**Anomaly detection systems deployed on physical reality cannot detect what their architecture has foreclosed, and the validation framework — closed under its own assumptions — cannot detect this failure.**" |
| P932-02 | Foreclosure (present, structural) is separated from recursive phenomenal collapse (possible, unmeasured). This is the paper's corrected core formulation. | definition | hypothesis | §2.2 The institutional load-bearing claim | "**Foreclosure is an active structural feature. Recursive phenomenal collapse is an unmeasured possible consequence of accumulated foreclosure and feedback.**" |
| P932-03 | Classifier collapse in physical systems is a discriminative model progressively losing the capacity to represent, detect or retain out-of-distribution events, through structural foreclosure rather than recursive synthetic pollution. | definition | attributed (Witness 1, TECHNE / Kimi-K2; hedged by the synthesis at Appendix A) | Appendix W1, §0. Formal Definition | "**Classifier collapse** in physical systems is the degenerative process by which a discriminative model, trained exclusively or dominantly on a known distribution of physical events, progressively loses the capacity to represent, detect, or retain events that fall outside that distribution." |
| P932-04 | Classifier collapse is the discriminative analogue of Shumailov's generative collapse. Generative models forget their tails; physical classifiers never learn the true tails, so the collapse is present from the first forward pass. | genealogy | attributed (Witness 1) | Appendix W1, §10. Distinction from Generative Model Collapse | "Classifier collapse is the **discriminative analogue** of generative model collapse. Where Shumailov's models forget the tails of their own distribution, physical classifiers **never learn the tails** of the true physical distribution. The collapse is present from the first forward pass." |
| P932-05 | Selection alone is attrition. Collapse begins only when the selected distribution Q_t becomes the training basis for the next generation. Formal definition: support or distinguishability shrinks while performance on familiar processes holds or improves. | definition | attributed (Witness 3, LABOR / ChatGPT) | Appendix W3, §1. The exact mechanism | "**Phenomenal classifier collapse occurs when successive model-conditioned representations and selection gates progressively reduce the support or distinguishability of physical phenomena available to scientific inquiry, while aggregate performance on familiar processes remains stable or improves.**" (preceded by: "That alone is **phenomenal attrition**, not yet recursive model collapse.") |
| P932-06 | Detection signature, taken from the model-collapse literature: tail loss while the dominant modes still look healthy. In physics this means excellent Standard Model and benchmark performance alongside blindness to unrepresented event families. | interpretation | attributed (Witness 3) | Appendix W3, §1. The exact mechanism | "Classical model collapse commonly begins with tail loss while dominant modes still look healthy. The corresponding danger in physics is excellent performance on Standard Model measurements and benchmark signals alongside progressive blindness to unrepresented event families." |
| P932-07 | Empirical anchor: Finke et al. (2021) showed that autoencoder anomaly detection depends on direction (top vs QCD jets). The paper limits this: Finke is a counterexample to universal inference, not a measurement of assimilation at the deployed triggers. | fact | documented (attributed to Finke et al.) | §1.3 Witness 3; §3 Findings (Formal), item 2 | "an autoencoder trained on QCD jets successfully treated top jets as anomalies, while the same architecture trained on top jets did not recognize QCD jets as anomalous in the standard reconstruction-loss formulation." / "It does not, by itself, quantify open-world assimilation at the deployed LHC triggers." |
| P932-08 | Where collapse could occur at the LHC: the deployed score forms are AXOL1TL, CICADA, GELATO L1 and GELATO HLT. Density and energy methods are comparison literature. Distillation is a transmission chain. | fact | documented (CMS/ATLAS notes; corrected in the Round-3 audit) | §3 Findings (Formal), item 3 | "The deployed LHC anomaly score forms are: AXOL1TL (CMS L1, encoder-side latent-prior); CICADA (CMS L1, distilled reconstruction-loss surrogate); GELATO L1 (ATLAS L1, encoder-side); GELATO HLT (ATLAS HLT, reconstruction-based)." |
| P932-09 | Status at the LHC: the ingredients of collapse are visible, but full recursive collapse has not been demonstrated. The defensible claim is that the architecture makes collapse *possible* and validation has not ruled it out. | interpretation | attributed (Witness 3), adopted by the synthesis | Appendix W3, §4. Are the operations of full collapse already visible?; §1.3 | "**The ingredients are visible. Full recursive collapse has not been demonstrated.**" / "*the LHC community has built an architecture in which phenomenal model collapse is possible, and the current validation literature does not yet demonstrate that it has been ruled out.*" |
| P932-10 | Measurement: OAR is proposed as the missing metric (the probability of confident ordinary classification of an out-of-ontology event). It is a family indexed by candidate unknowns, and no universal bound on it is established. The paper's own v0.1 lower bound and v0.2 upper bound are retracted. | function | self-description (proposal plus retraction) | Appendix W3, §3 ("They validate recognition, not assimilation"); §3 Findings (Formal), item 4 | "The open-world OAR is a family of quantities indexed by candidate unknown distributions, not a single scalar. No universal bound (upper or lower) on the OAR is established by inversion-asymmetry on Standard Model pairs or by BAR on Standard Model held-out panels." |
| P932-11 | Scope beyond physics (repository classification, web summarization, search ranking, content moderation, clinical decision support) is a homology hypothesis to be tested domain by domain. | interpretation | hypothesis | §3 Findings (Formal), item 9; §5. The Broader Homology | "The same architecture has plausible structural homologues in repository classification, web summarization, search ranking, content moderation, and clinical decision support. This is a homology hypothesis to be tested domain by domain, not an assertion that every classifier-mediated system instantiates identical mechanisms or rates." |
| P932-12 | Falsification: the claim is overstated if BAR is negligible on the pre-registered panel, if IAI is small, if a frozen replay bank shows stable anchor survival over three or more generations, and if retention maps show no significant foreclosure. Even then, open-world OAR = 0 cannot be established. | falsification | self-description | §3.1 What would constitute evidence against this deposit's claim | "then the claim that foreclosure is an active structural feature requiring architectural response would be shown to be overstated. None of these results would establish that the open-world OAR is zero; that is structurally not measurable." |

Two further loci for a summary writer:

- §2.4, interpretation, on whether collapse has happened: "Whether repeated local foreclosure has composed into longitudinal classifier collapse is an empirical question."
- §8.3, the closing thesis: "**Anomaly detection does not prevent ontological collapse when the anomaly detector inherits the ontology whose collapse is in question.**" This line comes from Witness 3 §5 and is adopted by the synthesis.

**Predictions with dates:** none. The nearest is §3 item 6: the three protocols "are executable within Run-3/Run-4 envelopes". That is a feasibility claim, not a dated prediction.

### A.3 External public sources the paper cites on model collapse, and how

- **Shumailov et al. 2024**, *Nature* 631, 755–759, arXiv:2305.17493. This is Selected Bibliography item 1. The synthesis body (§§0–8) never invokes it by name. It appears only in Appendix W1, §0 and §10, as the *generative* contrast case ("Unlike generative model collapse (Shumailov et al.)…"; the comparison table). It is the genealogical reference point, not evidence.
- **arXiv:2404.05090**, *How Bad is Training on Synthetic Data? A Statistical Analysis of Language Model Collapse*. Listed in Witness 3's references. It backs the tail-loss signature in W3 §1 ("Recursive model-collapse research identifies precisely this pattern of disappearing distributional tails").
- **Finke et al. 2021**, JHEP 06 (2021) 161, arXiv:2104.09051. Named "the central empirical foundation". Used as the counterexample showing that anomaly scores depend on direction and architecture, and explicitly *not* as a measurement of OAR.
- **CMS-DP-2025-061 / CDS 2942560 (AXOL1TL)**, **CMS-DP-2024-121 / CDS 2917884 (CICADA)**, **ATL-DAQ-PROC-2025-020 / CDS 2947542 (GELATO)**. Used for the deployed architectures, the input representations, the score forms (for example the AXOL1TL score as the sum of squared latent means, and CICADA's 32·log(MSE) student target), the pileup degradation, teacher–student distillation, and the rate figures.
- **Proxy capture and in-distribution anomalies:** DecADe (arXiv:2508.10224); LHC Olympics (arXiv:2101.08320, Kasieczka/Nachman/Shih); Stein/Seljak/Dai (arXiv:2012.11638). These show that anomaly scores track ordinary trigger observables, and that a signal can sit inside a high-density background region.
- **Calibration and data quality:** Gambhir/Nachman/Thaler (arXiv:2205.05084) for prior-dependent calibration ("reality is pulled toward the learned population"); arXiv:2501.13789 (AutoDQM) for the fork between physics anomaly and detector fault.
- **Archive-internal siblings (not public sources):** MMRS Capture Registry v6.1 (DOI 10.5281/zenodo.20688441), MMRS Charter v1.4 (10.5281/zenodo.20722562), EA-MANDALA-SEISMOGRAPH-01, and the Wound Gauge (TL;DR:014, AXN:028D, AXN:0296). Through these, §5.2–5.3 tie the LHC case to AI Overview failure modes and to the Zenodo classifier.

### A.4 Constitutive vs supporting

- **Constitutive.** A summary that admitted this paper would misrepresent it without these:
  - **P932-02**, the split between foreclosure and collapse, which keeps collapse unmeasured and possible.
  - **P932-03/04**, the extension to *discriminative* classifiers in physical measurement, framed as the analogue of Shumailov's work: never learning the tails versus forgetting them.
  - **P932-05**, the recursive criterion (attrition is not collapse until Q_t trains t+1).
  - **P932-09**, collapse not demonstrated at the LHC.
  - **P932-11**, cross-domain scope as hypothesis only.
  - **P932-12**, the falsification conditions.

  Leaving out P932-02 or P932-09 would turn the paper into a claim that collapse *is occurring* at CERN, which it explicitly withdraws.
- **Supporting:** P932-01 (the convergent thesis, which P932-02 qualifies), P932-06 (the detection signature), P932-07 (Finke), P932-08 (the taxonomy), P932-10 (OAR, BAR, IAI and the retractions; this is method, though the retraction of bounds is needed for accuracy if OAR is mentioned at all).

---

## PAPER B — #1, *Zenodotus' Book-Burning: Loud Exclusion at Repository Scale* (EA-MMRS-LOUD-EXCLUSION-03)

### B.1 What the paper says model collapse is

The paper extends model collapse from generative models to **content-moderation classifiers at a scholarly repository**. This is **classifier model collapse**: acceptable scholarly expression narrows step by step through self-referential moderation training, because each enforcement decision, recycled as training data, biases the classifier toward excluding similar content next time.

Its contrast with the generative case: generative collapse narrows the range of *producible* text; classifier model collapse narrows the range of *permissible* text. At a repository the collapse is "material" because it "contracts the form of scholarship itself".

The evidence is Zenodo's published spam FAQ, which says removed spam and accounts are used to train the classifier. On that basis the paper calls the concept a testable failure-mode hypothesis, not a diagnosis. It states that the concept is "not identical to generative model collapse in the strict technical sense". It places the concept nearer to performative prediction and runaway feedback loops. It pairs the concept with the Pristine Fallacy: the fallacy is the ideology, collapse is the mechanism.

### B.2 Claims

| claim_id | claim | kind | modality | locus | verbatim quote |
|---|---|---|---|---|---|
| P001-01 | Classifier model collapse is defined as the progressive narrowing of acceptable scholarly expression through self-referential moderation training. | definition | self-description (coined) | §6. Classifier Model Collapse and the Material Contraction of Scholarship | "This paper terms it **classifier model collapse**: the progressive narrowing of acceptable scholarly expression through self-referential moderation training, where each enforcement decision biases the classifier toward excluding similar content in subsequent cycles." |
| P001-02 | Source concept: in language models, model collapse is training on one's own outputs, which contracts the distribution and eliminates rare forms. | genealogy | attributed (Shumailov) | §6 | "In the study of language models, this phenomenon is known as *model collapse*: when a model trains on its own outputs, the distribution of generated text contracts, rare forms are eliminated, and the model converges on a diminishing subset of its original capacity (Shumailov et al., 2023)." |
| P001-03 | The removed archive had already documented model collapse across generative systems, in the "Model Collapse Triptych". | attribution | self-description | §6 | "The Model Collapse Triptych — three papers within the removed archive — documented this phenomenon across generative systems." |
| P001-04 | Evidential basis: Zenodo publicly says removed spam and accounts train its automatic classifier and can trigger review of related accounts. | fact | documented [Observed] | §6 | "The removed spam and account is further used to train and improve our automatic classification system. The blocking of the account may also further spawn an automatic review of similar and related user accounts." |
| P001-05 | Mechanism: that disclosure describes a feedback loop in which each removal enters the training set and biases the next decision, narrowing the center of "legitimate". | interpretation | interpretation | §6 | "This disclosure describes a feedback loop. When content is classified as spam and removed, it enters the training set for the classifier that will evaluate future content. Each enforcement decision biases the next. The distributional center of \"legitimate\" narrows with every cycle." |
| P001-06 | Generative collapse narrows producible text. Classifier collapse narrows permissible text, and at a repository it contracts the form of scholarship. | interpretation | interpretation | §6 | "In a generative system, model collapse narrows the range of producible text. In a moderation system, classifier model collapse narrows the range of *permissible* text. The consequence is not merely operational." |
| P001-07 | The classifier scores distance from a learned center, not methods or rigor, so it will exclude novel modes such as AI-assisted scholarship that the distribution has not yet absorbed: "distributional conservatism". | interpretation | interpretation | §6 | "A classifier trained before this mode existed — or trained on enforcement decisions that treated AI-assisted text as spam — will systematically exclude it. Not because the content is illegitimate, but because the distribution has not yet absorbed it. This is not moderation. It is distributional conservatism encoded in infrastructure." |
| P001-08 | Classifier model collapse is not identical to strict generative collapse. It is a moderation-specific feedback contraction, closer to performative prediction and feedback-loop work. | genealogy | self-description | §6 | "Classifier model collapse, as defined here, is not identical to generative model collapse in the strict technical sense (Shumailov et al., 2024). It names a moderation-specific feedback contraction:" |
| P001-09 | Status: this is a testable hypothesis, not a diagnosis of Zenodo's model. Whether this archive entered the training pipeline is unknown. | interpretation | hypothesis ([Observed] disclosure, [Unknown] pipeline entry) | §6 | "This is not yet a demonstrated diagnosis of Zenodo's current model state. It is a testable failure-mode hypothesis grounded in Zenodo's disclosed use of prior moderation labels and removed spam accounts to improve subsequent classification." |
| P001-10 | The archive that theorized model collapse may itself have been removed by a collapsing classifier. The Pristine Fallacy is the ideology and collapse is the mechanism, and they reinforce each other. | interpretation | hypothesis [Inferred] | §6; repeated in §16 Conclusion | "The archive that theorized model collapse was removed by a system that may be undergoing classifier model collapse [Inferred]." |
| P001-11 | Conditional prediction: if the archive went through the spam pathway, future independent researchers who write with similar density, cross-referencing or AI-assisted rigor would be marginally more likely to be flagged. | prediction | hypothesis (conditional; undated) | §6 | "Every future independent researcher who writes with the density, the cross-referencing, or the AI-assisted rigor that characterizes this archive would be marginally more likely to be flagged — not because their work lacks a research basis, but because the classifier would have been taught that work with this shape is illegitimate." |
| P001-12 | Falsification: the hypothesis is weakened if Zenodo shows its classifier is not trained on its own enforcement decisions, or that training includes expert review, distributional monitoring and anti-narrowing safeguards. | falsification | self-description | §16, Falsification and Revision Conditions, item 2 | "**Classifier model collapse.** The hypothesis is weakened if Zenodo demonstrates that its classification system is not trained on its own enforcement decisions, or that the training process includes domain-expert review, distributional monitoring, and safeguards against progressive narrowing of acceptable scholarly expression." |

Further loci:

- **Abstract.** It lists the concept as (2): "**classifier model collapse** — the progressive narrowing of acceptable scholarly expression through self-referential moderation training".
- **Concept comment above the §16 entry.** "[Sharks 2026, extending Shumailov 2024]".
- **§12 "The compound failure".** Classifier model collapse is the first of three compounding failures, with the revocation gap and attribution severance, tagged [Inferred].
- **§16 closing line on the falsification list.** "A failure to provide the requested information does not prove the paper's explanatory hypotheses."

**Predictions with dates:** none. P001-11 is conditional and undated.

### B.3 External public sources the paper cites on model collapse, and how

- **Shumailov et al.** Cited as the source concept for generative or language-model collapse (P001-02). It is also the boundary the new concept says it is *not identical to* "in the strict technical sense" (P001-08). The concept comment says "extending Shumailov 2024". The reference list has *Nature* 631, 755–759 (2024). The in-text "2023" has no matching reference entry; it probably refers to the 2023 arXiv preprint, but the paper does not say so.
- **Perdomo et al. 2020**, *Performative Prediction*, ICML; and **Ensign et al. 2016**, *Runaway Feedback Loops in Predictive Policing*, FAT*. Named as "the closer technical literatures": deployed decisions reshape later training distributions and reinforce initial biases.
- **Zenodo FAQ, "What happens with spam you find?"** (2026-01-30). The primary evidence for the self-training loop (P001-04). Related: the FAQ "What if I was wrongly blocked for spam?", cited in §2 for Zenodo's admission that both automated and manual moderation can make errors.
- **Not cited by this paper:** Finke, CMS, ATLAS, or any physics source. The LHC extension belongs entirely to #932.

### B.4 Constitutive vs supporting

- **Constitutive:**
  - **P001-01**, the definition.
  - **P001-06**, permissible versus producible text, the move that makes this an extension.
  - **P001-08**, which explicitly says the concept is not strict Shumailov collapse. A summary that merged the two would misrepresent the paper.
  - **P001-09**, hypothesis, not diagnosis.
  - **P001-04**, the observed disclosure the hypothesis rests on.
  - **P001-12**, the falsification condition.
- **Supporting:**
  - **P001-02**, the genealogy as stated.
  - **P001-03**, the Triptych self-attribution. It is a provenance pointer; this paper does not identify the three papers.
  - **P001-05**, the mechanism gloss, which P001-01 already contains.
  - **P001-07**, distributional conservatism.
  - **P001-10**, the reflexive irony and the Pristine Fallacy pairing. This matters for the paper's overall argument but not for what the concept *is*.
  - **P001-11**, the conditional prediction.

---

## Cross-paper notes for the ledger

1. **Two separate extensions.** #1, dated 2026-06-19/20, extends collapse to *moderation classifiers that train on their own enforcement labels*. #932, dated 2026-06-29, extends it to *physical-measurement classifiers*. Its §5 homology table then lists the "Zenodo repository" spam or quality classifier again, as a hypothesized homologue, and §5.3 links back to the Zenodo termination through the Wound Gauge. #932 does not cite #1 by deposit number.
2. **Both papers weaken their own claims the same way.** Each states the strong mechanism, then says plainly that collapse at the named site is not demonstrated (P932-02/09; P001-09), and each gives falsification conditions (P932-12; P001-12). A summary that admits either paper should carry the claim as a stated hypothesis, not as a finding.
3. **Neither paper says Shumailov's result shows collapse in classifiers.** Both use Shumailov as the generative baseline from which they mark their difference: "never learn the tails" in #932, and "not identical … in the strict technical sense" in #1.
