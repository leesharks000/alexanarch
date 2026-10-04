# Model-collapse claim ledger: candidate pool A

Source: /home/claude/alexanarch/data/texts/AXN-<hex>-text.md (read-only). Every quote below was checked by exact-string grep against the text file (`grep -cF` = 1). Loci are section headings as they appear in the text.

## Summary

| # | AXN | Title (short) | Verdict |
|---|---|---|---|
| 127 | 02B2 | Inscriptions That Survive the Tokenizer (SPXI-TLP v2.2) | NOT |
| 147 | 02E1 | The Mary Lee Case | NOT |
| 161 | 02F8 | The Reverse Turing Test v1.2 | **ADMIT** |
| 739 | 028D | Narrative-Field Semantic Deviation (EA-GLAS-03) | NOT |
| 745 | 0296 | HF Dataset Work Plan v3 | **ADMIT** (thin) |
| 772 | 02D3 | The Magistrate Refuses the Mirror | NOT |
| 778 | 02DA | Reasoning Under Load · 01 | NOT |
| 779 | 02DD | Diversity Contraction Across Substrates (earlier version) | **ADMIT** |
| 781 | 02E0 | Constitutive Mediation | NOT (borderline) |
| 783 | 02E3 | Fear and Trembling: Diversity Contraction v9.1 (later version) | **ADMIT** (carries all of #779) |
| 788 | 02F1 | Measurement Sovereignty | NOT |

---

## #127 AXN-02B2: NOT
Reason: this is a training-layer provenance protocol. "Tail" here means long-tail knowledge memorization, which it uses to argue that inscriptions survive training. "Collapse" means deduplication. It makes no claim about recursive training or about the loss of distribution tails.
Best passage (§ on fictitious-entity watermarks): "They blend with the corpus, evade lexical filters, are memorized by the LM through the same long-tail-knowledge mechanism that handles legitimate factual content, and survive continued pretraining and supervised finetuning."

## #147 AXN-02E1: NOT
Reason: the paper is about entity substitution. A tail token gets resolved to the nearest high-density cluster in a single retrieval act, and the paper analyses this through the Diversity Contraction mediation orders. It never uses "collapse", and it never discusses recursion, training generations or model collapse. Its prediction is about how resolution works, not about collapse.
Best passage (§VI Implications for the institutional tail): "Prediction 1. For any authorial identity in the institutional prior's functional tail, the substrate's resolution kernel will, with high probability, substitute the identity's referent with the nearest high-density modal cluster sharing query-token overlap."

## #161 AXN-02F8: ADMIT
Reason: this is the archive's protocol for extending model collapse to AI-mediated human text, including the unaided writing of AI-habituated writers. It states a mechanism, measurement axes, a falsifier, limits, and a required revision of the mitigation literature. It calls itself "an empirical contribution to the model-collapse literature."

| claim_id | claim | kind | modality | locus | verbatim | constitutive |
|---|---|---|---|---|---|---|
| A161-01 | The model-collapse literature rests on a synthetic=contamination / human=refresh binary, and recent evidence makes that binary unstable. | interpretation | interpretation | Abstract | "It operates on a clean binary: synthetic data is the contamination; human data is the refresh. Three recent lines of work suggest the binary is unstable." | yes |
| A161-02 | Training on AI-mediated human text, including unaided text from habituated writers, produces model-collapse signatures comparable to synthetic data's, though plausibly slower. | prediction | hypothesis | Abstract | "that training on AI-mediated human text — including unaided text from cognitively-habituated writers — produces model-collapse signatures comparable to, though plausibly slower than, purely synthetic training data" | yes |
| A161-03 | The effect sits in the tails, not the means, and tails are the diagnostic instrument. | function (measurement) | hypothesis | Abstract | "The central methodological claim is that the effect is not in the means but in the tails, and that tails are the diagnostic instrument for rate under any homogenization regime." | yes |
| A161-04 | Mechanism: reduced tail variance in training data reduces exposure to low-prior productions and compounds across generations. It does not require mediated text to be identical to synthetic text. | function (mechanism) | hypothesis | §3 The Mediation Hypothesis (H3) | "The collapse mechanism is not that mediated text is identical to synthetic text; it is that reduced tail variance in training data reduces the model's exposure to low-prior productions, which compounds across generations under standard training dynamics" | yes |
| A161-05 | Collapse signatures are measured on tail-focused axes. | function (measurement) | hypothesis | §3 (H3) | "The collapse signatures manifest on tail-focused collapse axes: kurtosis of generation distributions, rare-token retention, long-tail factual recall, semantic dispersion at the 90th percentile, resistance to high-prior substitution." | no |
| A161-06 | Falsifier: if the H0, H1 and H2 corpora perform alike and all clearly better than synthetic, the cascade fails and standard filtering is enough. | falsification | hypothesis | §6.3 Stage 3 — Training Cascade | "H3 falsified: H0 ≈ H1 ≈ H2, all substantially better than S." | yes |
| A161-07 | Stated limit: mediation may produce collapse only at concentrations real corpora never reach, so H3 could fail in practice even if H1 and H2 hold. | falsification (limit) | self-description | §10 Limitations, (f) | "It is possible that mediation signatures, while present in human text, produce collapse only at very high concentrations that real-world training corpora do not approach. In this case, H3 fails for practical reasons even if H1 and H2 hold." | yes |
| A161-08 | Accumulation mitigation (Gerstgrasser et al.) assumes a stable human baseline. If the baseline drifts, its guarantees must be re-derived. | prediction (corrective) | hypothesis | §8.1 Training-Data Curation Changes | "Gerstgrasser et al.'s accumulation result depends on the assumption that the "fixed human baseline" remains stable across generations." / "The mitigation guarantees of accumulation must be re-derived under conditions of a drifting baseline." | yes |
| A161-09 | Corrective: a continuous Mediation Index replaces the synthetic/human binary in curation, and the human-data refresh gets a calculable half-life. | function (corrective) | hypothesis | §8.1 | "The synthetic-versus-human binary is replaced by a continuous Mediation Index score." / "The half-life of the human-data refresh becomes calculable." | no |
| A161-10 | Scope limit (v1.2 reframing): the claim is about rate, not kind. The control is a rate-baseline, not an "unmediated" purity-baseline. | interpretation (limit) | self-description | §4.4 The Reframed Empirical Question | "Under the rate framing, the cascade in Stage 3 is not a claim that mediated text is functionally identical to synthetic." / "The H0 condition is a rate-baseline*, not a purity-baseline*." | yes |

REDUNDANCY: not redundant. #161 (2026-06-07) is the antecedent that #855 and #856 (both 2026-06-18) build on, and #856 cites it as "the Reverse Turing Test (Sharks 2026)".
- #855 also names the AI-habituated adult as a substrate on the path to collapse. But #855 treats it as evidence within a boundary-law claim. #161's predicate is the training cascade (A161-02, A161-04), stated as a testable hypothesis with its own falsifier. Predicate and modality both differ.
- #856 limits its claim to chat data and its feedback loop. #161's object is AI-mediated human text in general, and #856 does not carry its tail-measurement axes or the drifting-baseline revision of accumulation.
- #1573 (benchmark is the wrong unit) and A161-03 (means are the wrong statistical location) are related but say different things.
- No listed deposit carries A161-06, A161-07, A161-08 or A161-10.

## #739 AXN-028D: NOT
Reason: this is an experimental design for semantic deviation in a literary test bed. "Collapse" appears once, meaning a trajectory falling back into a gravity well. It has no model-collapse content.
Best passage (closing section): "If the answer is no — if the gravity well admits only recapture or collapse — then the principle has quantified something about the structure of relational meaning"

## #745 AXN-0296: ADMIT (thin)
Reason: this is a dataset work plan. It is admitted because it states its own corrective hypothesis: provenance density modulates synthetic-data collapse. It also states the null that would falsify this, and a condition the corrective needs in order to work. It offers no wider theory.

| claim_id | claim | kind | modality | locus | verbatim | constitutive |
|---|---|---|---|---|---|---|
| A745-01 | Corrective hypothesis: fine-tuning on high-provenance-density AI-involved text degrades more slowly than fine-tuning on low-provenance-density text. | prediction (corrective) | hypothesis | Research Question, Operationalized (H₁) | "Fine-tuning on high-provenance-density AI-involved text produces measurably slower perplexity degradation and less semantic drift than fine-tuning on low-provenance-density AI-involved text." | yes |
| A745-02 | Falsifier: degradation is the same regardless of provenance density. | falsification | hypothesis | Research Question, Operationalized (H₀) | "Fine-tuning on synthetic or AI-assisted text produces equivalent perplexity degradation and semantic drift regardless of provenance density (DOI anchoring, heteronymic attribution, archival embedding, assembly review)." | yes |
| A745-03 | Condition (limit): provenance can modulate collapse only if the training system sees it as a signal, so provenance visibility must be ablated through separate text views. | function (mechanism condition) | attributed (to "Assembly review") | Research Question, Operationalized | "Provenance cannot modulate collapse unless provenance is presented to the training system as a signal." | yes |
| A745-04 | Measurement: provenance classification must be automated, because author-memory labelling would confound a collapse experiment. | function (measurement) | self-description | The Central Methodological Move, 1 | "Author memory introduces classification noise that would confound any downstream collapse experiment." | no |

REDUNDANCY: not redundant with any listed deposit. None of #855, #856, #1556, #1573, #1, #932, #199, #1540, #1574 or #1616 (by title and the given summaries) states that provenance density modulates collapse. I did not read #1540, #1574 or #1616 in full.

## #772 AXN-02D3: NOT
Reason: a close reading of a Claude 4.8 transcript as synthetic self-jurisdiction. It has no collapse, tail or recursion content; the one "recursive" hit is about field-forming definitions.
Best passage (Abstract): "It does not claim that one transcript proves a general theory of model behavior"

## #778 AXN-02DA: NOT
Reason: a reasoning-integrity evaluation. Its "collapse" is modal-scope collapse in reasoning. It mentions the Diversity Contraction paper only as the subject of a comparison between rewrites.
Best passage: "A research paper on diversity contraction across substrates was developed across approximately eight rounds with Opus 4.8 (~12,000 words, v8.1), then rewritten in a single pass by Opus 4.6 (~8,000 words)."
(This bears on the #779/#783 genealogy. #779 is ~7,850 words and opens with the boundary law in §1 plain-language form, which matches the "4.6 single-pass rewrite" #778 describes.)

## #779 AXN-02DD: ADMIT (earlier version of Diversity Contraction)
Reason: it includes recursive model collapse as a substrate under the boundary law and gives that substrate its operator form. It also claims models are endogenous by construction, that their only floor across generations is fresh human data, and that the Mediation Ratchet can gate that floor out. It lists the inclusion of model collapse among its own original contributions and states limits.

| claim_id | claim | kind | modality | locus | verbatim | constitutive |
|---|---|---|---|---|---|---|
| A779-01 | The model-collapse kernel and Eigen's error threshold are the same bifurcation seen from opposite sides. | genealogy | interpretation | §1 The Allee identification | "This ties the model-collapse kernel (Shumailov et al. 2024), where recursive resampling prunes tails, directly to the quasispecies literature, where excessive mutation dissolves concentrated types." | no |
| A779-02 | Model collapse as a substrate: transmission is resampling from the model's own output, selection is loss-minimization, and the regime is endogenous (case 3). | definition | interpretation | §4 The operator family (table) | "\| Model collapse \| Resampling from the model's own output distribution \| Loss-minimization on a fixed objective \| Endogenous (case 3) \|" | yes |
| A779-03 | Models are endogenous by construction: a model cannot place mass on a type it assigns zero probability. | function (mechanism) | interpretation | §3 Models are endogenous by construction | "The model cannot place mass on a type its current distribution assigns probability zero." | yes |
| A779-04 | Limit: the endogeneity claim covers only the base inference loop. Retrieval or tools that bring in genuinely unsupported types do floor the model. | interpretation (limit) | self-description | §3 Models are endogenous by construction | "The claim is bounded to the base inference loop — parameter-only generation without external retrieval or tool use." | yes |
| A779-05 | A model's only exogenous floor across training generations is fresh human data, and that floor can be gated out by the Mediation Ratchet. | function (corrective + its limit) | interpretation | §3 Models are endogenous by construction | "The only exogenous floor available to a model across training generations is fresh human data in the training mix." / "The model's sole floor is the human channel — which is exactly the thing the Mediation Ratchet shows can be gated out." | yes |
| A779-06 | The model-collapse literature (Shumailov, Seddik, Gerstgrasser) is the strongest support for link 1. Gerstgrasser's result supports the floor concept rather than refuting it. | attribution | attributed | §5 Model endogeneity and tail loss | "Gerstgrasser et al. (2024) show that accumulating real data alongside synthetic data can avert the collapse — directly supporting the floor concept (case-1 escape via exogenous data mixing) rather than refuting it." | no |
| A779-07 | Mediation Ratchet threshold α* = p/g0: the human floor survives only if floor-weight recovery outpaces the pruning-to-floor ratio. Shown for the simulated kernel; the empirical trigger is unmeasured. | function (mechanism) | hypothesis | §2.1 The Mediation Ratchet | "The floor survives the ratchet *if and only if* the floor-weight recovery rate exceeds the pruning-to-floor ratio." / "The result is established for the simulated kernel and proposed as a semantic mechanism; the empirical trigger — the form and steepness of $m(D)$ — remains to be measured." | yes |
| A779-08 | Self-description: placing recursive model collapse as a substrate under the classification is one of the paper's original contributions. | self-description | self-description | §8 What is imported and what is new | "(ii) The inclusion of recursive model collapse as a substrate under that classification, unified with biology, culture, institutions, and linguistic flattening." | yes |
| A779-09 | Corrective: a floor must come from outside the generative loop (pre-collapse corpora, real-data mixing, provenance reservoirs). A static archive is not a floor. | function (corrective) | interpretation | Coda: a live floor, or a museum? | "Any floor must inject diversity from outside the generative loop — preserved pre-collapse corpora, mandated real-data mixing, protected niches, provenance reservoirs — because an endogenous system cannot regenerate its own thinned tails." | yes |
| A779-10 | Limit: the substrates share an operator form, not a causal mechanism. | interpretation (limit) | self-description | §4 The operator family | "This is a claim about shared operator form — that each domain's dynamics can be written as transmission composed with selection — not a shared causal mechanism." | yes |

Further minor claim, not tabled: the coupling test should lag each substrate on its own cadence, since "model-collapse cycles run at machine speed ($\tau \sim$ milliseconds)" (§6 For the coupling thesis). Kind: prediction; modality: hypothesis.

REDUNDANCY: not redundant. #779 is the antecedent of the boundary law and Ratchet that #855 cites as "Sharks et al. 2026, Diversity Contraction".
- #855's subject is model collapse as "a property of language". Its three substrates are model, AI-habituated adult and feral child, and it says the analogy is "not an analogy". #779 puts model collapse beside biology, institutions, linguistic flattening and political economy, and qualifies the link as shared operator form, not shared mechanism (A779-10). The object and qualifier differ.
- #1556's α* = p/(w_H·g0) generalizes #779's α* = p/g0 (A779-07). The object differs.
- None of the listed deposits states A779-03, A779-04 or A779-09.

## #781 AXN-02E0: NOT (borderline)
Reason: it extends the Diversity Contraction mediation orders to the formation of receivers' categories. Its claims are about human category formation under typicality-pulling exposure, with the classroom as an exogenous floor. It never speaks of model collapse, recursive training or the model substrate. Its only touch on the self-thinning substrate is a premise taken from the parent paper.
Best passage (§II The constitutive case): "It becomes consequential for the present argument when the dominant exposure source is itself a typicality-pulling intermediary that systematically thins its own distribution."
Note for the caller: if the ledger's scope covers every Diversity-Contraction floor/ratchet claim on human substrates, two claims would qualify:
- "under constitutive mediation, the classroom is the most powerful exogenous floor available to a person with limited reach, because formation precedes mediation and therefore can shape mediation rather than be shaped by it" (Abstract).
- The generational limit: "Where teacher formation is itself substrate-shaped, the classroom operates not as an exogenous floor but as another node in the ratchet" (§V).
On the developing-cognition substrate, these would partly overlap #855.

## #783 AXN-02E3: ADMIT (later version; carries all of #779)
Version order: **#779 is earlier.** Its registry date is 2026-06-02 and its status line reads "Deposit candidate … DOI to be minted". #783 is dated 2026-06-03, with status "Deposit (v9.1, title amendment)", DOI 10.5281/zenodo.20532696 and prior version 10.5281/zenodo.20531100 (v9). #783 adds §2.3 Field Remapping, §2.4 Phenomenological Seeding, Study 5 and a Colophon, and its abstract changes "Four contributions" to "Six contributions".

Carries all of #779's model-collapse claims: **yes.** For each of A779-01 to A779-10, I grep-checked the quoted sentence in #783. Every one is present, with two formatting differences in emphasis:
- A779-07 appears in #783 without italics: "The floor survives the ratchet if and only if the floor-weight recovery rate exceeds the pruning-to-floor ratio."
- A779-10 appears in #783 with italics: "This is a claim about *shared operator form* — that each domain's dynamics can be written as transmission composed with selection — not a shared causal mechanism."

The table row, the endogeneity sentence, the base-inference-loop limit, the Gerstgrasser floor, link-1 support, contribution (ii), the coda floor and the machine-speed cadence are all present verbatim. Ledger the #783 quotes from #783's own text, using the two variants above.

#783-only claims. These extend the collapse/trap taxonomy to the reception layer. They do not concern the model substrate directly, so they count as model-collapse claims only under the archive's extension:

| claim_id | claim | kind | modality | locus | verbatim | constitutive |
|---|---|---|---|---|---|---|
| A783-01 | Case 4 "quarantine": partial mediation can remap reception so the floor's output is silenced after delivery. This is monostable, with no escape basin. | definition | hypothesis | §2.3 Field Remapping and the return channel | "Case 4 is monostable with no escape basin." | yes (for #783) |
| A783-02 | Corrective order: in Case 4, injecting variance fails until the return-channel efficiency r is restored. | function (corrective) | hypothesis | §2.3 | "Case 4 requires the prior restoration of $r$ — the return-channel efficiency must be raised before injection can have effect." | yes (for #783) |
| A783-03 | Measurement limit: the field's own instruments under-detect Case 4. Its signature is a silencing gap between production diversity and reception diversity. | function (measurement) | hypothesis | §2.3 | "Case 4 is therefore underdetectable by the very instruments the field uses to monitor itself." | no |
| A783-04 | When no floor can be built, depositing vocabulary is the achievable fallback (phenomenological seeding). | function (corrective) | self-description | Coda: a live floor, or a museum? | "The deposit is what is achievable when the building cannot be done." | no |

REDUNDANCY:
- #783 vs #779: every #779 model-collapse claim is carried in #783 with the same subject, predicate, object, qualifier and modality. If only one is ledgered, #783 is the deposited, DOI-bearing superseding version; #779 is its precursor.
- Against the listed deposits, #783 is not redundant, for the same reasons as #779.
- A783-01 to A783-04 are not made by #855, #856 or #1556. #855's "frictionless path" is close in theme to §2.4 ("Friction is the noticing-ground"), but its predicate is different: no factor adds friction on the path to collapse, versus friction being needed for noticing.

## #788 AXN-02F1: NOT
Reason: about the audit-performance bifurcation operator and the legibility threshold. It has no collapse, tail or recursion content; Diversity Contraction appears only in the reference list.
Best passage (References): "*Diversity Contraction Across Substrates* — DOI 10.5281/zenodo.20518338."
