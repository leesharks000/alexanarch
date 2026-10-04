# Strand: code / coupled recursion — archive claims on model collapse

Read in full: AXN-0651 (#1556), AXN-0341 (#199), AXN-040B (#1023), AXN-064F (#1554), AXN-0335 (#191), AXN-01CE (#46). Registry records for #198, #199, #1023 and the DataCite backup (`data/datacite-full-backup.json`) checked to settle #1023. Nothing edited.

## 0. Read this first: #1023's seated text is a different work

`data/texts/AXN-040B-text.md` is **not** Generative Monoculture. It is the full text of *The Self-Audit Module Dissolved* (EA-WG-SELF-AUDIT-01, Wound Gauge entry, Lee Sharks, DOI 10.5281/zenodo.20682278). That work is deposit #198, AXN:0340. Evidence:
- The registry record for #1023 gives `body_status.recovered_from: "https://mindcontrolpoems.blogspot.com/2026/06/the-self-audit-module-dissolved-total.html"` (`recovered_at 2026-07-20`, "mirror-backfill retry"). That URL is #198's blog mirror.
- #1023's `references_concepts` (PER, Google AI Overview, Hallucination…) and its `wiki_article` body sentence ("This report documents a five-round battery…") come from the Self-Audit text. The bytes differ only slightly from AXN-0340-text.md.
- #1023 itself is an orphan-restoration record (minted 2026-07-03) for dead DOI **10.5281/zenodo.20675199**. Its DataCite capture reads: title "Generative Monoculture: Model Collapse in Code as Systemic Vulnerability (EA-UMBML-MONOCULTURE-01 v1.0)", version "1.0", issued 2026-06-13, Talos Morrow and Nobel Glas as creators, Lee Sharks as Editor, versionCount 3. #199 carries DOI 10.5281/zenodo.20675438 and the body version v1.1.
- A 2026-07-28 title repair changed #1023's title from "v1.0" to "v1.1", using "fuzzy" matching to #199's DOI 20675438. The DataCite record for 20675199 says v1.0.

So #1023 contains no Generative Monoculture text. Its only content on the subject is the DataCite abstract, held in the registry `description` and the DataCite backup. This is a reading finding only. Under the intake/repair rule, nothing was touched.

---

## #1556 — The Interlocking Autoregression (AXN:0651, EA-LO-INTERLOCKING-AUTOREGRESSION-01 v1.0, Nobel Glas / LO!, 2026-08-27)

**1. Statement.** The paper treats model collapse as the state dynamics of a training ecology. Three documented distortions drive it, and an instrument regime misreads it. The three distortions are: (I) provenance opacity, where synthetic text is declared as a class and opaque as a lineage; (II) a mediation ratchet, where nominally human text is distributionally shaped by model assistance; and (III) a heritable keyed watermark signature, which leaves a model-level residue no corpus operation removes. Formally, X_{n+1} = F(X_n; I, II, III) and Y_n = M_IV(X_n). Component IV is the observation regime, not a fourth driver. The dominant per-round instruments (per-item benchmarks, quality ratings, per-sequence certification) measure a unit orthogonal to the state variable (tail mass, coverage, entropy). The collapse threshold is α* = p/(w_H·g₀). Opacity and mediation are hypothesized to lower the *admission weight* w_H of fresh human variation rather than its generation rate g₀. A seeded toy model (N=50,000 Zipfian types, 40 generations) shows four things. Tail collapse precedes benchmark inflection by 8–10 generations. The per-round quality proxy rises ("green") through mid-collapse. Mediation and re-entry blockage, not the watermark, dominate velocity. The watermark's relative contribution grows as diversity contracts. Shumailov's retain-human-data mitigation reproduces, but it needs exactly the fine-grained provenance that opacity withholds. The paper types its own claims edge by edge: the nodes are supported, the edges are new claims, and every toy result is labelled toy.

**2. Claims.**

| claim_id | claim | kind | modality | locus | verbatim quote |
|---|---|---|---|---|---|
| C1556-01 | Three documented distortions are plausibly coupled, while certification measures a unit orthogonal to the state. | interpretation | hypothesis | §0 Station Report (blockquote) | "Three independently documented distortions of the training ecology are plausibly coupled — the output of each entering another's input — while the ecology's certification instruments measure a unit orthogonal to the state variable." |
| C1556-02 | Component I: no public record gives per-item lineage of synthetic text in training mixtures. | fact | documented (absence in reviewed disclosures; §3 row "Not publicly documented in the reviewed disclosures") | §1 Component I | "What no public record supplies is per-item transformation history: the granularity at which a curator could price a text's genealogy." |
| C1556-03 | Component II: coarse human/machine provenance classification overstates the independence of "human" text. | function | hypothesis | §1 Component II, ladder item "Hypothesis" | "coarse human-versus-machine provenance classification therefore systematically overstates the independence of nominally human text." |
| C1556-04 | Component III: the watermark residue lives in the weights, so corpus sweeping cannot remove it, and detecting it is a keyholder capability. | interpretation | attributed (Gu et al. ICLR 2024; Sander et al. NeurIPS 2024) + analytic | §1 Component III | "because the residue lives in weights, not in the swept text; and residue detection is a keyholder capability, so the asymmetry of the key extends from text to models." |
| C1556-05 | The threshold parameter that opacity and mediation move is admission weight w_H, not the generation rate g₀. | definition | hypothesis ("Hypothesized mapping, assigned to Hook 6") | §5 | "opacity and mediation reduce how much fresh variation is admitted and how it is classed, whether or not humans generate less of it." |
| C1556-06 | Toy F1: under the full loop, tail mass halves by generation 7 while the standard benchmark inflects only at 15. | fact | documented (toy simulation, seed 20260827) | §6.2 F1 | "Full loop: tail mass halves by generation 7; the standard 90/9/1 benchmark does not inflect until generation 15; head-only probes, generation 17." |
| C1556-07 | Surface sign: modest benchmark improvement is characteristic of mid-collapse. | prediction | hypothesis | §6.2 F1 | "a period of modest benchmark improvement is consistent with, and on this model characteristic of, mid-collapse." |
| C1556-08 | Toy F2: mediation and re-entry blockage, not the watermark, dominate collapse velocity. | fact | documented (toy) | §6.2 F2 | "Tail half-life: recursion alone 15 generations; + ratchet 11; + remapping 9; full loop 7." |
| C1556-09 | Toy F3: benchmark flatness cannot tell a preserved state from a collapsed one. Probe weighting *is* the observation regime. | interpretation | documented (toy) | §6.2 F3 | "A flat benchmark is consistent with both a preserved state and a collapsed one; only the ensemble track distinguishes them." |
| C1556-10 | Toy F4: the keyed watermark term is negligible in a healthy distribution and dominant in a contracted one. | fact | documented (toy; existence result only) | §6.2 F4 | "The keyed term is second-order in a healthy distribution and first-order in a contracted one" |
| C1556-11 | Toy F5: the Shumailov retention mitigation works, but it needs the provenance distinction that opacity withholds from downstream builders. | function | documented (toy) + interpretation | §6.2 F5 | "The Shumailov mitigation reproduces in the interlocked setting — and the lever it requires is the distinction Component I withholds *from downstream builders*: capping synthetic share presupposes the ability to distinguish it." |
| C1556-12 | Two-track falsifier: if per-round measures inflect first or at the same time as ensemble measures, the observation-regime claim is weakened. | falsification | hypothesis | §5 (retained from v0.2) | "Track B (ensemble unit) inflects before Track A (per-round unit); Track A may improve during Track B's collapse; if Track A proves sensitive first or simultaneously, the observation-regime claim is weakened and the map must be revised." |

**3. External sources on model collapse and how they are used.**
- **Shumailov et al., *Nature* 2024** (10.1038/s41586-024-07566-y, listed in related_ids). Used as the baseline failure mode ("the Shumailov failure mode", §9 Hook 2) and its mitigation, the retention counterfactual G ("the Shumailov retain-human-data analog", §6.1; "The Shumailov mitigation reproduces", F5). The result is accepted, then extended.
- **Sourati et al., *Nature Human Behaviour* 2026** (10.1038/s41562-026-02550-0). The demonstrated outcome-level evidence for Component II ("880,000+ texts; 21–50% writing-complexity variance reduction"). The paper bridges it to the archive's Constitutive Mediation thesis only "consistent with, not yet proof of".
- **Gu et al., ICLR 2024** (watermark distillation) and **Sander et al., NeurIPS 2024** (radioactivity). These establish Component III's transmission channel and the detectable model-level residue, with erosion limits recorded.
- **Dathathri et al.** (SynthID-Text). The flat-quality/falling-diversity result is cited as the published half of the F4 separation.
- **Wu, Black & Chandrasekaran, arXiv 2407.02209 / ICLR 2025.** Not used for content. Cited only as the term attribution whenever #199 is invoked (archive-anchors line, per ERRATUM #1554).
- Allee-effect and cumulative-culture literatures: named only as the source papers' credit for the α* dynamics (§5), with no specific citation.
- Not cited: Alemohammad et al., Doshi & Hauser, Padmakumar & He, Dohmatob et al., Gerstgrasser et al.

**4. Status.** **Constitutive.** This is the archive's main mechanistic statement about model collapse as an ecology: coupled recursions plus an observation regime, with a deposited simulation as its evidentiary basis (code and traces SHA-256-hashed in the manifest). Its archive anchors (#779 Diversity Contraction, #939, #788, #191, #199…) supply the nodes; #1556 adds the edges and the toy.
- Internal inconsistency to note. The revision note says the toy watermark was "retyped as stress-test surrogate (not worst case…)", and §6.1 says "it is not a proven upper bound". §6.3 still reads "fixed watermark key (worst case)".
- Version labels differ across the document: frontmatter says v1.0, the body header says "v0.4", and §8 says "Canonical Statement (v0.3)".

---

## #199 — Generative Monoculture: Model Collapse in Code as Systemic Vulnerability (AXN:0341, EA-UMBML-MONOCULTURE-01 v1.1, Talos Morrow · Nobel Glas, ed. Lee Sharks, 13 June 2026, DOI 10.5281/zenodo.20675438)

**1. Statement.** Model collapse in code shows up as contraction of *solution-space diversity*, not as broken code. Generated programs converge on shared patterns, architectures and idioms while still compiling and passing tests (the "correctness trap"). The paper joins three literatures into one causal chain: model-collapse theory, code-security empirics and AI-monoculture analysis. The chain runs distribution narrowing → pattern convergence → shared failure modes → *correlated vulnerability*, a population property in which a single exploit class spreads across nominally independent codebases. Code's training loop is described as self-amplifying, because code is deliberately up-weighted as an optimization target while synthetic code saturates the corpus. The usual mitigation, retaining human data, is called a rate question that erodes as adoption rises. The paper specifies a measurement protocol the authors had not run: SSDI, a participation-ratio effective dimensionality normalized to a human reference population, plus VCC, mean pairwise Jaccard over CWE exposure sets. It states 24-month falsifiers. A final section argues that security regimes which classify external probing by origin defend the monoculture against the diversity it needs.

**2. Claims.**

| claim_id | claim | kind | modality | locus | verbatim quote |
|---|---|---|---|---|---|
| C199-01 | Three literatures describe one phenomenon, and solution-space diversity is the unmeasured variable connecting them. | interpretation | self-description | Abstract ¶1 | "This paper argues that these three findings are one finding observed in three literatures, and that the synthesis they require has not been performed because the connecting variable — *solution-space diversity* — is not measured by any current benchmark or audit framework." |
| C199-02 | In code, collapse shows up as lost diversity of correct solutions, not as lost correctness. | definition | hypothesis | Abstract ¶2, first claim | "model collapse in code does not manifest primarily as declining functional correctness (the property benchmarks measure) but as declining solution-space diversity (the property no benchmark measures)" |
| C199-03 | Correctness trap: compilers and tests hide collapse instead of preventing it. | interpretation | interpretation | §II, final ¶ | "The compiler and the test suite did not prevent model collapse in code. They taught it to hide as correctness." |
| C199-04 | Causal chain from narrowing to correlated vulnerability. | function | hypothesis (the paper says each step "is supported by existing findings") | §I (indented synthesis) | "Model collapse produces distribution narrowing. In code, distribution narrowing means pattern convergence. Pattern convergence means shared failure modes. Shared failure modes mean correlated vulnerability." |
| C199-05 | Contraction compounds across generations and is monotonic under current conditions. | prediction | hypothesis | §III, "Note the asymmetry" ¶ | "each generation inherits the contraction of all previous generations and adds its own. The contraction is monotonic under current training conditions." |
| C199-06 | Retaining human data slows contraction but does not reverse it. | interpretation | hypothesis (the accumulation literature it answers is cited in §I only as "Subsequent work", with no reference) | §III, same ¶ | "The mitigation is a rate question, not a structural solution: it slows the contraction but does not reverse it" |
| C199-07 | Definition of correlated vulnerability. | definition | self-description | §IV ¶2 | "A *correlated vulnerability* is a property of a population: these implementations, generated independently by different developers at different organizations for different purposes, share this flaw because they share the pattern from which the flaw emerges." |
| C199-08 | Vulnerability frequency per codebase may fall while correlation across codebases rises. | prediction | hypothesis | §IV, final ¶ | "the frequency of vulnerabilities per codebase may decrease (as models improve at avoiding known bug classes) while the correlation of vulnerabilities across codebases increases" |
| C199-09 | SSDI is defined as normalized effective dimensionality over the correct-solution space. | definition | self-description | §V Definition / Diversity measurement | "The Solution-Space Diversity Index (SSDI) is the ratio of the effective dimensionality of G's output distribution to the effective dimensionality of a reference distribution over S(T)." |
| C199-10 | Absent intervention, SSDI falls and VCC rises while pass rate holds or improves. | prediction | hypothesis | §V, Cross-generational tracking | "absent diversity-preserving intervention, recursive synthetic saturation produces a declining SSDI trend and a rising VCC trend, while functional pass rate remains stable or improves." |
| C199-11 | The protocol is unrun, and the only direct code-collapse experiment measured tokens, not solutions. | fact | documented (self-report) + attributed (arXiv 2512.09549) | §VI ¶1 and "Distribution narrowing in code" | "The measurement framework has not been run as of 13 June 2026." / "The study did not measure solution-space diversity; it measured perplexity and token-level distributional properties." |
| C199-12 | Falsified within 24 months if measured SSDI shows no monotonic decline (also VCC, loop interruption, harm-based governance). | falsification | self-description | §VIII (a)–(d) | "(a) A systematic measurement of SSDI across model generations showing no monotonic decline — i.e., solution-space diversity remains stable or increases as synthetic code saturates training corpora." |

**3. External sources on model collapse and how they are used.**
- **Shumailov et al., *Nature* 2024** (10.1038/s41586-024-07566-y). The foundational result: modes lost until a single mode remains, "empirically across model types and theoretically for Gaussian mixtures" (§I). It is the premise of the chain.
- **Dohmatob et al., "Strong Model Collapse", ICLR 2025 Spotlight.** Cited for the claim that even one in a thousand synthetic data is asymptotically detrimental. Used to strengthen the premise.
- Bertrand et al. (ICML 2025); "How to Synthesize Text Data without Model Collapse?" (ICML 2025); arXiv 2505.19046; arXiv 2512.00757. These appear in the reference list only; the body cites none of them by name. §I's unattributed sentence, "accumulation of real data alongside synthetic data", has no reference.
- **arXiv 2512.15011** (epistemic diversity across language models). Mitigation by model diversity. Used for the cross-model SSDI prediction (§VI).
- **arXiv 2512.09549, "Chasing Shadows".** Called "The only direct empirical investigation of model collapse applied to code generation" (Qwen2.5-Coder-0.5B). Used to mark the token-vs-solution gap that SSDI is meant to close.
- arXiv 2404.18353, listed as "noting Shumailov et al.'s model collapse as a factor"; Apple (2025) "complete accuracy collapse"; a Fujitsu internal classification. Reference list only.
- Code security sources: Checkmarx June 2026 (3.4×; 70%; 93%) and SoK arXiv 2512.18456 ("LLMs may emit insecure patterns even while passing functional tests").
- **Apiiro (2025).** Printed as coining "generative monoculture" (body line 49; references line 270). This attribution is **wrong per ERRATUM #1554, and the deposit text is uncorrected**. The registry `remediation_note` says "Registry-level cross-reference only by operator ruling; canonical bytes unchanged."
- Not cited: Wu, Black & Chandrasekaran (2024); Alemohammad et al.; Doshi & Hauser; Padmakumar & He; Gerstgrasser et al.

**4. Status.** **Constitutive** for the code substrate and for the archive's measurement proposal (SSDI/VCC), which is the archive's own contribution. It is supporting for model collapse in general: its collapse premise is taken from Shumailov and Dohmatob.
- Internal tension to record. §III asserts "The contraction is monotonic under current training conditions." §V says the prediction "is not that every individual model release must show a lower SSDI than its predecessor". Falsifier (a) is phrased as "no monotonic decline".
- §I says "Each step in this chain is supported by existing findings". §IV says the step to correlated vulnerability is "the step the code security literature has not yet taken formally".
- Registry lineage: `develops_from` #192 and `developed_by` #855 (not read here).

---

## #1023 — "Generative Monoculture … (EA-UMBML-MONOCULTURE-01 v1.1)" (AXN:040B, orphan restoration of dead DOI 10.5281/zenodo.20675199, minted 2026-07-03)

**1. Statement.** No seated text makes claims about model collapse; see §0. The seated file is *The Self-Audit Module Dissolved*. Its one model-collapse-adjacent sentence (§5) borrows #199's term for an audit-layer analogy: "the self-flattery cycle (fabricate metrics, score yourself perfect) is the correctness trap at the audit layer -- the system passing its own tests while the property that matters (provenance fidelity) collapses unmeasured." The actual Generative Monoculture content of this record is the DataCite abstract of the v1.0 Zenodo version. It states the same thesis as #199: correlated vulnerability, the self-amplifying loop, SSDI, and the security paradox.

**2. Claims.** Only two can be read, because there is no body.

| claim_id | claim | kind | modality | locus | verbatim quote |
|---|---|---|---|---|---|
| C1023-01 | Collapse in code produces correlated vulnerability, not declining correctness. Identical to #199's retrieval kernel. | interpretation | hypothesis | registry #1023 `description`; DataCite 10.5281/zenodo.20675199 `descriptions[0]` | "Generative Monoculture argues that model collapse in code produces not declining correctness but correlated vulnerability: AI-generated code converges on shared patterns, architectures, and failure modes invisible to functional benchmarks." |
| C1023-02 | The chain is narrowing → convergence → correlated vulnerability → systemic risk proportional to adoption. | function | hypothesis | DataCite 10.5281/zenodo.20675199 `descriptions[0]` (`data/datacite-full-backup.json`) | "distribution narrowing in code manifests as pattern convergence, pattern convergence produces correlated vulnerability, and correlated vulnerability at scale is a systemic security risk proportional to adoption." |
| (C1023-x, seated-body analogy) | The Wound Gauge battery is the correctness trap at the audit layer. This belongs to the #198 work, not #1023. | interpretation | interpretation | AXN-040B-text.md §5 (= #198 §5) | "the self-flattery cycle (fabricate metrics, score yourself perfect) is the correctness trap at the audit layer" |

**3. External sources.** None can be read; the record has no body. The DataCite record's related identifiers reference only archive DOIs: 20673413, 20674488 and 20673776.

**4. #1023 vs #199: no supersession.** #1023 does **not** supersede #199.
- **Version.** By DataCite, #1023 is the v1.0 Zenodo version (issued 2026-06-13, "version": "1.0"). #199 is v1.1 ("revised 13 June 2026 incorporating Assembly review"), so #199 is the later and governing version. #1023's "v1.1" title came from a fuzzy-match repair against #199's DOI, and the DataCite record contradicts it.
- **Restoration status.** The registry records #1023 as `status_authorial: SEMI_RESTORED` with `"fulltext": "pending"`.
- **Ledger use.** Use #199 for every Generative Monoculture claim, and cite #1023 only as the dead-DOI v1.0 trace. The body mis-seat (#198's text under #1023) is a defect to report to Lee, not to repair here.

---

## #1554 — ERRATUM to AXN:0341: Prior Use of "Generative Monoculture" (AXN:064F, Lee Sharks for Talos Morrow · Nobel Glas, 2026-08-27)

**1. Statement.** This is a term-priority correction, not a claim about model-collapse mechanism. #199 attributed the coining of "generative monoculture" to Apiiro (2025). The term was introduced earlier by **Fan Wu, Emily Black and Varun Chandrasekaran**, "Generative Monoculture in Large Language Models", arXiv:2407.02209, submitted 2 July 2024, published at ICLR 2025. Wu et al. define it as a narrowing of a single model's output diversity relative to the diversity in its training data, with root causes in alignment and fine-tuning. The correct order is Wu et al. (July 2024) → Apiiro (2025) → #199 (June 2026). The erratum separates the objects. Wu et al. describe a single-model output-distribution property. Apiiro describes an ecosystem-scale security condition. #199 describes correlated vulnerability with SSDI and a training-feedback argument. It still names the omission a "serious lapse" without mitigation, and it sets a standing rule: every invocation of the archive's application cites Wu et al.

**2. Claims.**

| claim_id | claim | kind | modality | locus | verbatim quote |
|---|---|---|---|---|---|
| C1554-01 | What #199 printed: Apiiro as coiner. | attribution | documented (verified against canonical text) | §1 | "The term 'generative monoculture' (Apiiro, 2025) names the condition," |
| C1554-02 | The term has prior claim from Wu, Black & Chandrasekaran (2024). | attribution | documented (verified against arXiv, dblp, Semantic Scholar) | §2 | “Fan Wu, Emily Black, and Varun Chandrasekaran, "Generative Monoculture in Large Language Models," arXiv:2407.02209, submitted 2 July 2024; published at ICLR 2025” |
| C1554-03 | Wu et al.'s definition of generative monoculture. | definition | attributed | §2 | "a significant narrowing of model output diversity relative to the diversity available in training data for a given task" |
| C1554-04 | Wu et al. locate the root causes in alignment and fine-tuning. | attribution | attributed | §2 | "with evidence locating the root causes in alignment and fine-tuning processes." |
| C1554-05 | Priority order across the three usages. | genealogy | documented | §2 | "Wu, Black & Chandrasekaran (July 2024) → Apiiro (2025) → this deposit (June 2026)." |
| C1554-06 | #199's object and its SSDI framework are its own. Wu et al.'s object differs. | interpretation | self-description | §3 | "the object differs (correlated failure modes and their measurement, not output-diversity narrowing per se), and the framework contribution (SSDI) is the deposit's own." |
| C1554-07 | Independence does not excuse the lapse. | attribution | self-description | §3 | "Convergent and independent describe how the error happened, not why it was acceptable. It was not." |
| C1554-08 | Scope: term-level only; the argument and SSDI are unaffected. Standing citation rule. | function | self-description | frontmatter `severity`; §4.3 | "Attribution error — term-level priority; the deposit's argument, framework (SSDI), and application are unaffected" / "the term cites Wu, Black & Chandrasekaran (arXiv 2407.02209; ICLR 2025)." |

**3. Sources, exactly.**
- **Prior use:** Wu, Black & Chandrasekaran, arXiv:2407.02209 (10.48550/arXiv.2407.02209), submitted 2 July 2024; ICLR 2025.
- **Later industry use, printed as coinage in #199:** Apiiro, "AI-Generated Code Security" (2025). The erratum states that whether Apiiro is downstream of Wu et al. "is not established here and is not this erratum's burden".
- **The correction says:** move the "coining" descriptor from Apiiro to Wu et al.; revise #199's body to cite Wu et al. as prior academic use and Apiiro as a later ecosystem-scale application; deposit the erratum separately; propose a v1.2 text correction; and sweep downstream citers.
- **Current state:** the v1.2 text correction has **not** been applied. AXN-0341 lines 49 and 270 still carry the Apiiro coinage. The registry shows a cross-reference only (`related_deposits` relation `corrected_by`, plus `remediation_note`). #1556 complies with the citation rule.

**4. Status.** **Constitutive for attribution only.** It is the archive's own record that its use of "generative monoculture" is downstream, at the level of the term, of Wu et al. 2024. It is not constitutive of any model-collapse mechanism claim. For the ledger it acts as a binding qualifier on every #199 claim that uses the term.

---

## #191 — The Threat Model Is Backwards (AXN:0335, EA-TAILGUARD-01 v1.1, Lee Sharks with Nobel Glas and Talos Morrow, 2026-06-11)

**1. Statement.** The paper applies the established model-collapse finding to a security recommendation. The finding it relies on: collapse begins at the tails; rare words, low-resource languages and dialects go first; and early collapse can look like aggregate improvement while minority data degrades. Its target is the language-gating mitigation in *AI_Bleeding* (Caria 2026), which rejects high-perplexity, unexpected-language queries before inference. The paper argues this is structurally an input-layer tail-pruning instrument. The tokenizer inefficiency that paper treats as an attack vector is the same property by which low-resource languages occupy the tail. Because inference logs become training corpora, and because mediated selection ratchets (#779), the generalized pattern would push the ecology in the degenerative direction, with the harm falling disproportionately on low-resource-language speakers. Claims are self-typed as Established, Structural or Model proposition. The model-collapse content itself is entirely Established-by-citation; the archive's contribution is the inversion and the training/inference coupling.

**2. Claims.**

| claim_id | claim | kind | modality | locus | verbatim quote |
|---|---|---|---|---|---|
| C191-01 | Recursive synthetic training causes irreversible loss of distribution tails. | fact | attributed (Shumailov et al. 2024, *Nature* 631:755–759) | §2 ¶2 | "recursive training on synthetic data causes irreversible defects in which the tails of the original content distribution disappear" |
| C191-02 | Early collapse loses minority data while aggregate performance can appear to improve. | fact | attributed (as "now standard") | §2 ¶2 | "this stage is insidious precisely because aggregate performance can appear to improve while performance on minority data silently degrades." |
| C191-03 | The tails consist of rare words, constructions, low-resource languages and dialects. | fact | attributed (Briesch et al. 2023; arXiv:2507.03933; arXiv:2602.16201) | §2 ¶3 | "rare words, uncommon syntactic constructions, low-resource languages, non-standard dialects, and culturally specific variation are named repeatedly as the first features to disappear under recursive training" |
| C191-04 | Tail sparsity is partly a tokenization artifact. | function | attributed (arXiv:2602.16201) | §2 ¶3 | "linguistic sparsity in the tail is *partly driven by tokenization artifacts*" |
| C191-05 | A high-perplexity reject filter is an input-layer tail-pruning instrument. | interpretation | interpretation (self-typed *Structural*) | §3 | "A high-perplexity-content detector that rejects on positive detection is, viewed from the model-collapse literature, an automated tail-pruning instrument applied at the input layer." |
| C191-06 | Inference-layer rejection becomes training-layer exclusion through logs. | function | hypothesis (self-typed *Model proposition*) | §4, link 1 | "A pre-inference filter that rejects low-resource-language queries does not merely refuse service in the moment; it systematically excludes those languages from the interaction record that becomes future training signal." |
| C191-07 | The filter is a mediation-ratchet term with the wrong sign. | function | hypothesis (cites Diversity Contraction, doi:10.5281/zenodo.20518338) | §4, link 3 | "Adopted widely, it is a ratchet term with the wrong sign." |
| C191-08 | Tail-loss harm falls disproportionately on marginalized groups. | fact | attributed (arXiv:2503.03150) | §5 | "can disproportionately affect marginalized groups or historically disadvantaged communities" |
| C191-09 | IBM: long-tail ideas fade from public consciousness. | fact | attributed (IBM synthesis of the *Nature* result) | §5 | "long-tail ideas might eventually fade out of the public's consciousness, limiting the scope of human knowledge." |
| C191-10 | Self-limitation: the collapse finding concerns training, the gating concerns inference, so the strongest claims are marked as model propositions. | interpretation | self-description | §4 ¶1 | "The objection is correct as stated and is the reason this document's strongest claims are marked *Model proposition* rather than *Established*." |
| C191-11 | The reviewed paper is a specimen of collapse dynamics at the research layer. | interpretation | hypothesis (self-typed *Model proposition*) | §7 | "This is the collapse dynamic operating one layer above where the collapse literature usually finds it." |

**3. External sources on model collapse.**
- **Shumailov et al. 2024, *Nature* 631:755–759.** Load-bearing: tail-first loss and the early/late two-stage characterization.
- **Briesch et al. 2023**, ***Losing our Tail — Again*** (arXiv:2507.03933), and **long-tail-knowledge survey** (arXiv:2602.16201). Cited for what occupies the tail and for the tokenization mechanism.
- ***Model Collapse Does Not Mean What You Think*** (arXiv:2503.03150), with the fairness lineage (Blodgett; Bender & Friedman; Noble; Koenecke; Gebru; Bender et al.). Cited for disproportionate harm.
- **IBM's synthesis of the *Nature* result.** Quoted on long-tail ideas fading; no URL given. This is the archive's direct engagement with one of the ledger's public sources.
- Internal: Diversity Contraction Across Substrates (doi:10.5281/zenodo.20518338) for the mediation ratchet.
- Not cited: Alemohammad et al., Doshi & Hauser, Padmakumar & He, Dohmatob et al.
- The colophon states: "Cited model-collapse and fairness literature is external and load-bearing".

**4. Status.** **Supporting / applied.** The paper adopts the public collapse literature on its own terms and adds a new substrate and layer: input/inference-layer selection feeding training through logs. That is a hypothesis-grade extension. #1556 lists #191 as an archive anchor. One convergence is worth recording for the ledger: C191-02 ("aggregate performance can appear to improve") is the literature-side statement of what #1556 F1 makes quantitative ("for a quarter of the trajectory it is *green*").

---

## #46 — Sémantique Potentielle (AXN:01CE, Lee Sharks · Johannes Sigil, v0.2, 2026-03-30)

**1. Statement.** This is a constraint-based "semantic mint" specification: 42 seed terms, operations O1–O8, four grammar rules, deterministic coordinates, and families with forensic "canary" variants. It is not a paper about model collapse. Two of its fifty Appendix A families touch the topic:
- **Model collapse** (D.04 × S.10 / O4), glossed conventionally, with forensic variant *autophagic parametric entropy*.
- **Diversity collapse** (D.04 × S.02 / O4), glossed "The reduction of output variety in AI systems as synthetic training data converges on statistical priors", with variants "output homogenization, variance extinction, creative narrowing" and forensic variant *stochastic monoculture onset*.
- The "Semantic noise floor" family also lists the variant "retrieval collapse threshold".

**Is it an early priority statement about model collapse? No.**
- (a) Its "Model collapse" entry is a coordinate assigned to an existing field term. The term dates to Shumailov et al.'s 2023 preprint and the 2024 *Nature* paper; that is general knowledge, not re-verified in this session. #46 cites no collapse literature.
- (b) "Diversity collapse" has prior use in LLM research. arXiv:2505.18949, *The Price of Format: Diversity Collapse in LLMs*, dates from May 2025 (found by web search in this session). #46 does not cite it.
- (c) The forensic variant's "monoculture" postdates Wu et al.'s "generative monoculture" (July 2024).
- (d) The mint disclaims coinage outright: "The claim is not ownership. The claim is cartography."
- By the mint's own Step 3 ("Was the mint family published before the term's first documented appearance elsewhere?"), these canonical terms carry no temporal priority. The only strings original to #46 here are the coordinates and the forensic variants. It does, however, predate #199 (June 2026) as the archive's first appearance of the diversity-collapse/monoculture pairing.

**2. Claims.**

| claim_id | claim | kind | modality | locus | verbatim quote |
|---|---|---|---|---|---|
| C46-01 | Gloss of model collapse (conventional). | definition | self-description (gloss of an existing term) | Appendix A, Diagnostic-Structural Families, "Model collapse" | "The degradation of AI model quality when trained recursively on synthetic data." |
| C46-02 | Gloss of diversity collapse as output-variety reduction driven by synthetic data converging on priors. | definition | self-description | Appendix A, Diagnostic-Structural Families, "Diversity collapse" | "The reduction of output variety in AI systems as synthetic training data converges on statistical priors." |
| C46-03 | Variant family for diversity collapse, including a monoculture forensic. | definition | self-description | same entry | "Family: output homogenization, variance extinction, creative narrowing. Forensic: *stochastic monoculture onset*." |
| C46-04 | Forensic canary for model collapse. | function | self-description | Appendix A, "Model collapse" | "Forensic: *autophagic parametric entropy*." |
| C46-05 | The mint claims mapped territory, not term ownership. | attribution | self-description | Governing Claim ¶2 | "The claim is not ownership. The claim is cartography." |
| C46-06 | Priority test the mint applies to later instantiations. | function | self-description | §VII Step 3 | "Was the mint family published before the term's first documented appearance elsewhere? If yes, the mint has temporal priority for the coordinate." |

**3. External sources.** None on model collapse. Works Cited: Queneau, Oulipo, five Sharks deposits, the US Copyright Office, Creative Commons.

**4. Status.** **Supporting lexicon only.** It is not constitutive and not a priority statement. For the ledger it is at most a genealogy note: the archive's first appearance of the terms, dated 2026-03-30.

---

## Cross-paper summary for the ledger

- **Constitutive archive claims on model collapse:** #1556 (mechanism + observation regime + toy dynamics) and #199 (code substrate; SSDI/VCC measurement; correlated vulnerability), with #199 qualified by #1554 on the term.
- **Supporting:** #191 (applied: tail-pruning at the input layer; its collapse content is citation-borne, including IBM and Shumailov). #46 (lexicon).
- **#1023:** a non-source. It is the dead-DOI v1.0 trace of #199, with the wrong body seated.
- **Distinctive archive positions relative to the public sources** (Shumailov, IBM, CACM, NIH PMC):
  1. Collapse is read through an *observation regime*. Per-round benchmarks can read flat or improving during collapse; this is quantified in a toy (#1556 F1/F3), and the literature-side statement is #191 C191-02.
  2. The retention mitigation depends on fine-grained provenance that public disclosures do not supply (#1556 F5).
  3. In code, collapse is diversity loss among correct programs, producing correlated vulnerability (#199). It is unmeasured; the protocol is specified but not run.
  4. Mediation of human text (Sourati) lowers the effective admission weight of fresh variation (#1556 C1556-05, hypothesis).
- **Not cited anywhere in these six:** Alemohammad et al. (MAD), Doshi & Hauser, Padmakumar & He, Gerstgrasser et al. #199's reference to accumulation as a mitigation names no source.
- **Defects found (reported, not repaired):**
  1. #1023's body is #198's text, and its title "v1.1" contradicts DataCite's v1.0.
  2. #199's v1.2 correction (proposed in #1554) is unapplied; the Apiiro coinage is still printed.
  3. #1556 §6.3 still says "(worst case)" against its own retyping.
  4. #199's monotonicity wording is inconsistent across §III, §V and §VIII.

Sources: [The Price of Format: Diversity Collapse in LLMs (arXiv:2505.18949)](https://arxiv.org/abs/2505.18949)
