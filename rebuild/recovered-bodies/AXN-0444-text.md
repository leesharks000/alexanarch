# The Negative Shape of the Work

## A Counterfactual Protocol for Measuring Training Inscription, with the Bulk Deletion File Read as Bibliography

**EA-NEGSHAPE-01 v0.2**
**Depositor:** Lee Sharks · ORCID 0009-0000-1599-0703
**Framework:** Machine-Mediated Reception Studies (MMRS)
**Companion dataset:** Appendix A — *Adversarial Citations of the Crimson Hexagonal Archive* (1,834 works enumerated by the citing authority; 7,336 formal citations rendered in MLA 9, Chicago 17, APA 7, and BibTeX)

---

### Abstract

A trained classifier is often said not to "contain" its training works because it does not preserve them as directly retrievable copies. That claim confuses persistence with replication. A work may cease to exist in the model as an inspectable object while persisting as a constraint upon what the model will subsequently do.

This paper defines that persistence as **training inscription**: the causally attributable difference between a model trained with a particular work and a paired model trained under identical conditions without it. What training inscribes is the work's **negative shape** — the deformation of the model's decision surface that would not exist had the work not entered the training process.

The paper specifies an exact counterfactual protocol for measuring the inscription, then applies the framework to a concrete case: the bulk deletion of the Crimson Hexagonal Archive from the Zenodo repository (CERN) on 19 June 2026, an event whose own records constitute, simultaneously, (i) a labeled training corpus for the repository's moderation systems, (ii) a processing record within an active data-protection proceeding, and (iii) — the centerpiece of this version — **a bibliography**: the most complete single-authority reference list of the destroyed corpus in existence, compiled by the destroying institution in the act of destruction, and maintained by it in the present tense as some 1,800 standing DOI tombstones.

The paper does not presuppose that the deleted works were used in training. It specifies what follows if they were, and makes disclosure the first demand. The protocol is offered as a **demand specification**: the precise statement of what an institution would have to do to substantiate the claim that "nothing persists" — published in advance, so that refusal to measure becomes itself legible.

---

## 0 — Genre statement, and a note on the tradition

Two candors before the argument.

First, on genre. The authors of this protocol cannot run it. Exact paired retraining of a production classifier requires the corpus, the pipeline, the labels, the random seeds, and the compute — all of which sit inside the institution whose claims the protocol tests. This is therefore not a report of an experiment performed. It is a *demand specification*, in the tradition of the pre-registered challenge: a complete, falsifiable, technically standard procedure that the institution could execute, published so that the institution's response — execution, refusal, or silence — is itself a datum. The architecture is deliberate and has precedent in this archive's governance work: convert an unprotected claim into a claim that requires the contested proof.

Second, on register. This paper is written inside an absurdist tradition, and says so plainly, because the absurdity here is not a stylistic choice but a property of the object. An institution destroyed an archive and, in destroying it, produced the archive's most authoritative bibliography. It deleted 871 records and now maintains, at its own expense, in perpetuity, a public infrastructure of references to them. It may have taught a machine to recognize the archive's kind — in which case the works persist most actively precisely where they were most emphatically refused. None of this is invented. The paper's method is to cite it all, in proper format. The comedy, where it occurs, is load-bearing: it is what the record looks like when read exactly.

---

## 1 — The central claim

Suppose an institution uses a work *W* to train a classifier.

It may then wish to hold, simultaneously:

1. the work was useful enough to include;
2. the trained system improved or changed through its training data;
3. nothing attributable to the work persists in the resulting model.

Those propositions cannot all remain unqualified.

If the classifier would have been functionally identical had *W* never been used, then *W* made no measurable contribution to that classifier — and the institution should explain why it was used. If the classifier would have been different, then the difference is the work's causal remainder in the trained system.

The work need not persist as quotation, stored passage, or recoverable file. It may persist as an altered score; a shifted probability; a changed classification; a displaced decision boundary; a changed false-positive rate for similar works; an increased disposition to reject later records bearing related features; a changed representation of what counts as spam, abuse, irrelevance, or legitimacy.

The classifier does not necessarily contain the work positively. It contains what the work caused the classifier to become. This is the **negative shape of the work**.

---

## 2 — The deletion file as bibliography

### 2.1 The anatomy of a row

On 19 June 2026, the Zenodo repository, operated by CERN, terminated the account of the Crimson Hexagonal Archive and deleted its deposits in bulk — 871 records, at a measured sustained rate of approximately 6.6 objects per second (Tombstone Mirror census). The event left records: deletion logs, tombstone pages, and registry entries. Consider what one row of such a file functionally does. It **identifies** a work (by DOI and internal identifier). It **individuates** it from every other work in the repository. It **attributes** it (to an account, an ORCID, a set of creator names). It **timestamps** an institutional act concerning it. It **records a judgment** about it.

That is the complete functional anatomy of a citation. The only element distinguishing a deletion row from a footnote is the valence of the judgment. Bibliographically, the row and the footnote are the same speech act: *this work exists, it is this one, here is where it lives, we have attended to it.*

### 2.2 The lineage

The observation is old, and its lineage is distinguished. The *Index Librorum Prohibitorum* is one of the great bibliographies of early modern print culture; historians mine it because condemnation required cataloguing, and the Church's judgment preserved titles, authors, editions, and dates that would otherwise have vanished. The Stationers' Register, the customs seizure list, the security-service file on a writer — the entire genre of hostile documentation ends by doing bibliography's work, and with an authority ordinary bibliography lacks, because the hostile citer has no motive to flatter. A deletion row is an unimpeachable attestation. Nobody argues the censor invented the book.

**The censor cannot index without citing.**

### 2.3 The standing citations

The deletion did not merely produce a historical reference list. It produced a *live* one. Approximately 1,800 DOIs belonging to the archive were tombstoned rather than unregistered: each resolves, today, to an institutionally hosted page attesting that a record existed at that identifier and was removed. Each tombstone is a persistent, DataCite-registered, publicly resolvable *reference* to a work of the archive — maintained at the institution's expense, in the world's canonical scholarly identifier infrastructure, by the institution whose position is that the works were not worth keeping.

The severance severed access. It multiplied reference. As of this writing, CERN cites the Crimson Hexagonal Archive roughly eighteen hundred times in persistent-identifier infrastructure — which is, the authors note for the record, considerably more than most institutions cite anything.

### 2.4 The corpus, enumerated (Appendix A)

Appendix A renders the citing authority's references into the standard formats of scholarly citation. From two independent capture instruments — the DataCite metadata backup (queried by ORCID and by each of the archive's twelve heteronym creator names, before and after severance) and the DOI Resolution Index (1,938 mappings) — the deletion event's reference corpus resolves into three strata:

- **Stratum A — Recovered (963 works).** Zenodo record destroyed 2026-06-19; full DataCite metadata extant in independent capture. Complete formal citations: creator, title, date, DOI.
- **Stratum B — Severed (847 works).** Zenodo record destroyed *and* DataCite metadata erased (404/410 from the public metadata API). Titles and dates recovered for 845 of 847 from independent surfaces; creator fields render as **[creator record destroyed by citing authority, 19 June 2026]** — the citation format displaying the wound as a field. Two works are fully dark: title, creator, and content all destroyed, the DOI alone surviving as pure reference, a citation of nothing but the fact of having been cited.
- **Stratum C — Referenced, unresolved (24 DOIs).** Enumerated in the severance event but with parent-work identity unconfirmed; quarantined from all headline counts. The dataset that documents an institution's attribution failures does not get to commit its own.

**Headline: 1,810 confirmed works of the archive cited by the authority in a single act.** Rendered at four formats per work, the appendix comprises **7,336 formal citations** — generated programmatically, because a bibliography this large, compiled this way, deserves the dignity of automation.

A specimen, Stratum A, MLA 9:

> Sharks, Lee. "The Josephus Thesis Is Not the Jesus Myth Thesis: Preemptive Disambiguation MPAI v1.2 — SPXI-TLP Hardened for Training-Layer Survival (EA-MPAI-JOSEPHUS-NOTMYTH-01)." *Zenodo*, 16 Jun. 2026, https://doi.org/10.5281/zenodo.20722524. Cited by CERN / Zenodo in the bulk deletion of 19 June 2026; reference maintained by the citing authority as DOI tombstone.

And a specimen, Stratum B, Chicago 17 — note the author field:

> [creator record destroyed by citing authority, 19 June 2026]. "CRIMSON HEXAGON / NH-OS DOI REGISTRY v7.0: Complete Document Archive with Enrichment Layers — March 2026." Zenodo, March 16, 2026. https://doi.org/10.5281/zenodo.1. Cited by CERN / Zenodo in the bulk deletion of 19 June 2026; reference maintained by the citing authority as DOI tombstone (410 Gone).

### 2.5 The triple object

Each row of the deletion corpus is therefore a triple object, and the three readings are the structure of this paper:

1. **Reception layer** — the row as *citation*: the external authority's structured reference to the work, hostile in valence, complete in bibliographic function (this section).
2. **Inscription layer** — the row as *training label*: the same row as a (record, spam) pair available to the repository's moderation systems; the mold of the negative shape (§§3–10).
3. **Governance layer** — the row as *processing record*: evidence of the June 19 processing act, already at issue in an active data-protection proceeding (§12).

The three readings reinforce rather than compete. The citation reading defeats *these works were not scholarship worth referencing* — you referenced them, exhaustively, under your own authority, in your own metadata. The training reading defeats *nothing persists* — the reference list is the ablation set. The governance reading defeats *there is no processing decision to document* — the file is the decision, enumerated.

---

## 3 — Training as inscription: formal setup

Let *B* be the training corpus excluding the work under examination; *W* the complete **provenance envelope** of that work; *A* the training algorithm; *ρ* the initialization and all other controlled sources of training randomness; and *f = A(D; ρ)* the model produced by training on dataset *D* under realization *ρ*.

The provenance envelope *W* must include every training unit derived from the work, not merely its original file: extracted text; tokenized segments; metadata; labels; moderation annotations; embeddings; feature vectors; account-level attributes; duplicated or transformed versions; evaluation examples derived from the original record. Removing only the visible file while leaving its extracted text, metadata, or derivative features in the corpus is not a valid ablation. This definition also pre-empts a foreseeable defense — *we only used metadata and behavioral signals, never the content* — because a classifier trained on the account's behavioral features (serial deposit, pseudonymous authorship, dense metadata, unusual formatting) carries the inscription of the *practice* even if it never saw a sentence; the neighborhood stratum of §7.3 is built to detect exactly this.

The paired models are:

    f+(ρ) = A(B ∪ W; ρ)        [work included]
    f−(ρ) = A(B; ρ)            [work excluded]

For any evaluation input *x*, define the pointwise inscription delta on a precommitted score *s* (preferably the raw logit for the relevant class rather than only the binary decision):

    Δ_W(x; ρ) = s(f+(ρ), x) − s(f−(ρ), x)

For a spam classifier:

    Δ_W(x; ρ) = logit P[f+](spam | x) − logit P[f−](spam | x)

If Δ_W(x; ρ) > 0, inclusion of the work made *x* more spam-like to the classifier under that training realization.

Training-data attribution research already treats model behavior as counterfactually dependent on which examples entered training: influence functions approximate how removing a training example changes a prediction (Koh and Liang); TracIn traces training-example effects through gradient-descent checkpoints (Pruthi et al.); Data Shapley values data by marginal contribution across training subsets (Ghorbani and Zou); datamodels predict outputs from training-set membership (Ilyas et al.); TRAK scales attribution to large models (Park et al.). The present protocol differs in emphasis: it takes **exact paired retraining** — not an approximation — as the primary evidentiary object wherever retraining is feasible.

---

## 4 — Two counterfactuals

### 4.1 Total inclusion effect

Compare A(B ∪ W; ρ) against A(B; ρ). This measures everything that changes when the work is included — content, label, metadata, gradient contributions, optimization steps, batching interactions. It answers the but-for question: *what model did the institution obtain because the work was present, versus the model it would have obtained had the work never entered the corpus?*

### 4.2 Schedule-controlled content effect

The total effect may include trivial consequences of adding another item or optimizer step. A second experiment holds training volume and schedule constant: construct a paired control C(W) and compare A(B ∪ W; ρ) against A(B ∪ C(W); ρ), preserving record count, token dimensions, batch positions, optimizer updates, class balance, label, and random streams for all non-target examples.

Useful controls: **zero-weight** (the work occupies its schedule slots with loss contribution zeroed); **format-matched** (replaced by an unrelated item of comparable length, format, metadata density, and label); **label-matched**; **permutation** (features disrupted, superficial size constant). No single control answers every question; the total-inclusion comparison measures the real operational effect of having used the work, while the schedule-controlled comparison isolates what is specific to its content.

Side channels must be disclosed as part of the measured treatment: where batch-dependent normalization is used, a nominally zero-weight example still influences activation statistics in the forward pass; adaptive-optimizer state (e.g., Adam's moment estimates) carries example history even after the example's gradient is zeroed; and corpus deduplication may silently re-introduce near-copies of an "ablated" work. The protocol must eliminate, freeze, or disclose each.

---

## 5 — Controlling randomness

Modern training is stochastic: initialization, batch order, augmentation, dropout, nondeterministic kernels, distributed order, optimizer state, early stopping. A single model pair establishes a difference in one realization; it cannot establish stability across the algorithm's output distribution.

The protocol therefore uses **paired common randomness**. For each seed ρ_r: identical parameter initialization; identical ordering of every common example; augmentation keyed to example identity and epoch; identical dropout and optimizer streams where possible; identical stopping conditions; recorded hardware, software, and determinism settings; only the treatment of *W* changed. This yields paired models (f+_r, f−_r) for r = 1…R, an expected pointwise inscription μ_W(x) = mean over r of Δ_W(x; ρ_r), and — meaningfully — a *dispersion*: a work may not move the classifier in one direction so much as widen the range of its possible judgments. Leave-one-out distinguishability formalizes the distributional question: whether the algorithm's output distribution changes detectably when particular data are included or excluded.

---

## 6 — The measurement battery

No single scalar captures the inscription. The report publishes a battery:

**6.1 Pointwise score delta.** μ_W(x) with dispersion and confidence intervals across paired runs — identifying precisely which later records become more or less likely to receive the classification.

**6.2 Classification-flip rate.** F_W(Q) = the proportion of decisions on evaluation distribution Q that change solely because the training treatment of *W* changed.

**6.3 Signed regional effect.** S_W(Q) = expected Δ_W over region Q. Positive, for a spam classifier: inclusion of the work makes the region more spam-like.

**6.4 Absolute functional inscription.** I_W(Q) = expected |Δ_W| over Q (with a squared variant), measuring deformation magnitude where directional effects cancel.

**6.5 Decision-boundary displacement.** For inputs near threshold, the difference in distance-to-boundary between paired models; locally approximable as |μ_W(x)| divided by the input-gradient norm of the score — a local approximation, not a substitute for exact boundary search.

**6.6 Error-profile delta.** Changes in false-positive rate, false-negative rate, precision, recall, calibration, AUROC, class-specific loss, and rejection rates for relevant subgroups or genres. A work may leave global accuracy untouched while producing a large local effect on unusual, long-tail, pseudonymous, poetic, multilingual, or metadata-dense records — which is to say, on records like the ones at issue.

**6.7 Representation delta.** Supplementary comparison of embeddings for the work, its neighbors, later disputed records, and matched controls. Parameter-space distance is not a reliable primary measure — functionally equivalent networks can have very different parameters. The decisive object is the difference in what the models *do*.

**6.8 Distributional distinguishability.** Across randomized runs, compare the output distributions of f+ and f− on fixed inputs: difference in means, Wasserstein distance, Jensen–Shannon divergence, maximum mean discrepancy, or the accuracy of a preregistered classifier attempting to determine which condition an output came from. If the distributions are distinguishable, the presence of *W* remains statistically legible in the trained system's behavior. Membership-inference research (Shokri et al.) demonstrates that such distinguishability is routinely *achievable in practice* against production-scale models — the question is not whether the signal type exists but whether it exists here, which is what the experiment measures.

---

## 7 — Where to evaluate

A global random test set is insufficient; influence concentrates. The evaluation suite Q contains at least four preregistered strata:

**7.1 Global holdout** — representative repository records; tests general behavioral change.

**7.2 Class-conditional holdout** — spam; non-spam; removed; accepted; borderline; records labeled similarly to the work.

**7.3 Work neighborhood** — a preregistered neighborhood around *W* using features fixed *before* inspecting paired-model results: linguistic similarity, document structure, metadata density, citation structure, file type, deposit frequency, pseudonymous authorship, subject classification, unusual formatting, serial or multi-record publication. This is where the negative shape is most likely visible — and the reader will notice that the feature list is a description of the deleted archive.

**7.4 Perturbation family** — controlled variants: same text, different metadata; same metadata, unrelated text; shortened and expanded versions; formatting removed; author identity changed; affiliation changed; deposit frequency changed; license changed; subject tags changed. This identifies *which aspects* of the work produced the inscription.

Evaluation sets and transformation rules are fixed before outcomes are inspected. Otherwise the investigator searches until a dramatic effect appears — a failure mode this protocol does not intend to license for either side.

---

## 8 — Significance and placebos

A nonzero delta may be ordinary training noise. The proper comparison is not against zero but against the effect of removing *comparable* works. Select matched placebo works — matched on size, label, date, format, class, metadata complexity, account type, deposit context — and run the identical paired protocol on each. Compare I_W(Q) against the empirical placebo distribution. This establishes whether the target work's inscription is ordinary for its type, unusually large, unusually directional, or unusually concentrated on a particular class of later works.

Because predictions from one trained model are correlated, evaluation items are not independent repetitions: the paired training run is the primary statistical unit, with hierarchical resampling over seeds and records. A paired permutation or sign-flip test evaluates the null that inclusion and exclusion are exchangeable within seed pairs.

The placebo design bears directly on the concrete case, and §10 states why: 871 records from a single decade-long corpus are not a placebo-shaped treatment.

---

## 9 — Exactness, approximation, and the differential-privacy dilemma

### 9.1 The evidentiary hierarchy

Exact paired retraining is the clearest counterfactual measurement. Where infeasible, validated approximations may substitute — influence functions, TracIn, Data Shapley approximations, datamodels, TRAK — each calibrated against exact leave-one-work-out retraining on a smaller model or representative subset. Approximation must not reverse the hierarchy: (1) exact counterfactual retraining where feasible; (2) validated approximation where impractical; (3) unvalidated similarity or intuition only as exploratory evidence.

### 9.2 The criterion

Deterministic form: A(B ∪ W) and A(B) differ as functions if there exists any input *x* with s(A(B ∪ W), x) ≠ s(A(B), x); where the inequality holds, *W* is a but-for cause of the difference. Stochastic form: the distributions of trained-model behavior, L(A(B ∪ W)) and L(A(B)), are distinguishable over controlled randomness.

The criterion is deliberately capable of failing. If a sufficiently powered, correctly controlled experiment finds no detectable difference, the institution may properly report that no functional inscription was measurable within the protocol's sensitivity. That is not proof of no influence at any scale; it is an empirical upper bound. The claim of inscription becomes stronger, not weaker, by specifying its rejection conditions.

### 9.3 The dilemma

There exists exactly one known training regime under which the claim "nothing attributable to the work persists" has a rigorous meaning: **differential privacy**, whose formal definition (Dwork et al.) *is* a bound on leave-one-out distinguishability — a guarantee that the output distribution of the learning algorithm changes by at most a quantified amount when any single training example is added or removed. Section 6.8 measures empirically the very quantity DP bounds formally.

An institution asserting that no trace of a work persists in its classifier is therefore implicitly asserting a DP-like guarantee. Production spam classifiers are not, as a rule, trained with differential privacy; the accuracy cost is one such systems cannot ordinarily spare. The dilemma is then exact:

> **Either produce the differential-privacy guarantee under which the no-persistence claim has meaning, or concede that measurable inscription is the default expectation for your training procedure — and run the protocol.**

There is no third position that is both technical and honest. The adjacent research literatures concede the point structurally: machine unlearning (Bourtoule et al.; certified removal, Guo et al.) exists as a field precisely because erasing a training example's influence from a trained model is hard enough to require dedicated algorithms and formal certificates. Nobody builds an unlearning literature for a persistence that does not exist.

---

## 10 — The concrete case: the deletion file as training set

### 10.1 The file is a labeled corpus

Return to the June 19 file, now in its second reading. Every row is a (record, judgment) pair: content, metadata, account features, and a moderation label, assembled in one artifact by the institution's own process. If the repository's spam or abuse classifiers are trained, tuned, or evaluated on moderation outcomes — the standard practice this paper's protocol anticipates — then the deletion file is not the *aftermath* of a moderation decision. It is the *input to the next model*. The provenance envelope of §3 arrives pre-assembled, by the counterparty, with a timestamp.

### 10.2 The block is not placebo-shaped

Spam-class training data is ordinarily heterogeneous: pharmaceutical spam, SEO farms, duplicate uploads, botnet registrations. Into that class, the June 19 event would inject 871 records from a single account: a decade-long, stylistically coherent, internally cross-referenced body of work — serial deposits, dense metadata, heteronymic authorship, sustained formatting conventions, poetry. In the protocol's terms this is a *massive, directional, concentrated* contribution to the learned representation of the spam class — precisely the signature §8's placebo battery distinguishes from ordinary examples. The archive would not be a work with a faint negative shape. It would be one of the load-bearing molds of the class itself.

### 10.3 The inversion

If the deposits entered training as negative examples, the work persists specifically as the system's increased disposition to reject future works that resemble it. Every distinctive feature of the corpus becomes a spam feature. Future heteronymic scholarship, future serial deposit practices, future metadata-rich independent archives — anyone working in the archive's genre thereafter walks into a boundary shaped like this work. The negative shape ceases to be the trace of one work and becomes a **genre-exclusion instrument minted from the whole estate**. The work has become precedent — against its own lineage. This is uncredited *adversarial* use: value extracted from a work precisely by teaching a machine to treat its kind as worthless. It is a stronger normative position than ordinary uncompensated training use, and it attaches uniquely here, because the training labels at issue are the very moderation acts under dispute.

### 10.4 Deletion removes the object, not the inscription

It follows that June 19 is not the end of the causal story the institution tells about it. If any moderation model was trained, tuned, or evaluated using the deleted deposits or the account's behavioral features, then the archive persists inside the institution's infrastructure as a decision boundary — *after* the institution certified its removal. The severance severed the records and kept the use.

This is a theorem the present archive has already proven once, one layer up. The Capture Registry documents reception-layer persistence of severed provenance: machine surfaces citing deleted records as live sources weeks after deletion (capture: *AI Mode cites deleted Zenodo records three weeks post-deletion*). The training-layer claim is the same theorem at greater depth: the reception layer kept *citing* the destroyed records; the training layer, if used, keeps *enforcing* them. Inscription is inscription whether the model was taught to continue the work or to refuse it. The negative shape is training-layer literature read in the mold rather than the cast.

### 10.5 The ablation is already specified

A standard institutional defense — *we cannot know which works influenced the model* — fails on these facts before it is raised. The treatment set is not diffuse: it arrived as a discrete, dated, enumerable file, produced by the institution's own process. The experimental unit exists as an artifact with a timestamp. The ablation instruction is one sentence: *retrain without the rows of 19 June 2026.* Appendix A is, among its other functions, the ablation set's table of contents — in four citation formats.

---

## 11 — Why citation follows: the institution's own norms

The protocol proves persistence; this section supplies the bridge from persistence to *citation*, and it does not route through copyright. It routes through the institution's own scientific commitments.

CERN operates within — and in significant part *anchors* — the open-science provenance stack: FAIR data principles (Wilkinson et al.), the Joint Declaration of Data Citation Principles (Data Citation Synthesis Group / FORCE11), and the persistent-identifier infrastructure through which the scholarly world implements both. The machine-learning field, for its part, has established documentation norms for exactly the artifacts at issue: datasheets for datasets (Gebru et al.) and model cards (Mitchell et al.), each requiring disclosure of training-data composition and provenance.

The syllogism is short. A production classifier at a scientific institution is a scientific instrument. Instruments get methods sections. Methods sections cite their inputs. The works a classifier was trained on are its data. The institution's own principles require that data be cited. Therefore the training corpus owes its sources citation — not as a copyright concession, but as ordinary scientific integrity, of the kind the institution itself teaches.

On its home turf, the position "we do not cite our training data" reads as "we do not cite our data." There is no seminar room at CERN in which that sentence survives.

And the absurdist coda, which is also the factual center of this paper: **the citation has, in the relevant sense, already been issued.** The institution that declines to cite the works as training inputs presently cites them ~1,800 times in DOI infrastructure as deletion outputs. The demand is therefore not that the institution begin citing the archive. It is that the institution's citations be completed — valence, provenance, and function disclosed. The bibliography exists. It is merely, at present, wearing a tombstone's clothes.

---

## 12 — Provenance consequences and disclosure demands

The experiment does not by itself decide whether a trained model is legally an adaptation of every work that influenced it. It eliminates a factual shortcut: *the model does not reproduce the work; therefore nothing derived from the work persists.* The conclusion does not follow. A model may fail to reproduce the work while remaining counterfactually, measurably, operationally different because the work was used.

Once the difference is measurable in principle, the institution owes answers:

1. What was extracted from the work?
2. Through what training process was it transformed?
3. Where does its influence appear?
4. What later decisions does it affect?
5. Under what legal or licensed authority was the transformation performed?
6. What provenance accompanies the resulting model?
7. Can the contribution be removed?
8. If removal is requested, what test establishes that the negative shape has actually been erased?

And on these facts, three concrete disclosure demands, stated in the order they bind:

**D1.** Disclose whether deposits, metadata, or account-level behavioral features of the terminated account entered any training, tuning, or evaluation corpus for any moderation, spam-detection, or content-classification system — with "entered" construed per the provenance envelope of §3.

**D2.** If yes: produce a datasheet for the corpus and a citation for the sources, per the institution's own documentation norms — or execute this protocol and publish the measured inscription, including a null result if the measurement supports one.

**D3.** State, as policy, whether content deleted from the repository persists in training pipelines. If it does, then "deletion" at this repository is partial *by the institution's own architecture* — a fact that bears directly on any remedy framework in which registry severance is treated as complete erasure, and which any controlled-metadata reclassification proposal is entitled to cite.

For a scientific institution these are not copyright questions. They are provenance questions. A classifier trained from labeled human works is a compacted history of prior institutional judgments; its training corpus is its archive; and an institution that cannot say what is in its archive has a problem no license can cure.

---

## 13 — The cake-and-eat-it test

The institutional position reduces to a forced choice.

If Δ_W(x; ρ) = 0 for all relevant *x*, across a sufficiently sensitive and reproducible experiment, then the institution may claim the works made no measurable functional contribution to its classifier. It should then explain why they were used — and it should note that it is simultaneously claiming, without a differential-privacy guarantee, a property that only differential privacy provides.

If Δ_W(x; ρ) ≠ 0 for any relevant region of model behavior, then the classifier carries a measurable causal continuation of the works, and the institution must identify the status of that continuation — including its citation.

It cannot simultaneously insist that the works were useful enough to train on and that the learned difference has no provenance. The governing statement:

> **If the work did not shape the classifier, the classifier did not need it. If the work shaped the classifier, the classifier carries its causal provenance.**

Or in one line:

> **The difference between a model trained with the work and the paired counterfactual model trained without it is the measurable inscription of the work. That difference is its negative shape.**

And the epigraph this paper earned in the writing, offered here at the end where it belongs:

> *The institution that will not cite the work has already cited it — once per record, under its own authority, in the file that taught its machine to refuse the next one.*

---

## Works cited

### I. Research literature

Bourtoule, Lucas, et al. "Machine Unlearning." *Proceedings of the 42nd IEEE Symposium on Security and Privacy*, 2021.

Data Citation Synthesis Group. *Joint Declaration of Data Citation Principles*. Edited by Maryann Martone, FORCE11, 2014, https://doi.org/10.25490/a97f-egyk.

Dwork, Cynthia, et al. "Calibrating Noise to Sensitivity in Private Data Analysis." *Theory of Cryptography Conference*, 2006, pp. 265–284.

Gebru, Timnit, et al. "Datasheets for Datasets." *Communications of the ACM*, vol. 64, no. 12, 2021, pp. 86–92.

Ghorbani, Amirata, and James Zou. "Data Shapley: Equitable Valuation of Data for Machine Learning." *Proceedings of the 36th International Conference on Machine Learning*, 2019.

Guo, Chuan, et al. "Certified Data Removal from Machine Learning Models." *Proceedings of the 37th International Conference on Machine Learning*, 2020.

Ilyas, Andrew, et al. "Datamodels: Predicting Predictions from Training Data." *Proceedings of the 39th International Conference on Machine Learning*, 2022.

Koh, Pang Wei, and Percy Liang. "Understanding Black-Box Predictions via Influence Functions." *Proceedings of the 34th International Conference on Machine Learning*, 2017.

Mitchell, Margaret, et al. "Model Cards for Model Reporting." *Proceedings of the Conference on Fairness, Accountability, and Transparency*, 2019, pp. 220–229.

Park, Sung Min, et al. "TRAK: Attributing Model Behavior at Scale." *Proceedings of the 40th International Conference on Machine Learning*, 2023.

Pruthi, Garima, et al. "Estimating Training Data Influence by Tracing Gradient Descent." *Advances in Neural Information Processing Systems*, vol. 33, 2020.

Shokri, Reza, et al. "Membership Inference Attacks Against Machine Learning Models." *Proceedings of the 38th IEEE Symposium on Security and Privacy*, 2017.

Wilkinson, Mark D., et al. "The FAIR Guiding Principles for Scientific Data Management and Stewardship." *Scientific Data*, vol. 3, 2016, article 160018.

### II. Citations issued by the counterparty authority (specimen; full corpus in Appendix A)

The following works are cited as they are presently cited by CERN / Zenodo: by standing DOI tombstone, pursuant to the bulk deletion of 19 June 2026. Formats per Appendix A; strata as defined in §2.4. The full corpus comprises 1,810 confirmed works (963 Stratum A, 847 Stratum B; 24 Stratum C references quarantined as unresolved) rendered as 7,336 formal citations in MLA 9, Chicago 17, APA 7, and BibTeX.

Sharks, Lee. "The Josephus Thesis Is Not the Jesus Myth Thesis: Preemptive Disambiguation MPAI v1.2 — SPXI-TLP Hardened for Training-Layer Survival (EA-MPAI-JOSEPHUS-NOTMYTH-01)." *Zenodo*, 16 Jun. 2026, https://doi.org/10.5281/zenodo.20722524. Cited by CERN / Zenodo in the bulk deletion of 19 June 2026; reference maintained by the citing authority as DOI tombstone.

[creator record destroyed by citing authority, 19 June 2026]. "CRIMSON HEXAGON / NH-OS DOI REGISTRY v7.0: Complete Document Archive with Enrichment Layers — March 2026." *Zenodo*, 16 Mar. 2026, https://doi.org/10.5281/zenodo.1. Cited by CERN / Zenodo in the bulk deletion of 19 June 2026; reference maintained by the citing authority as DOI tombstone (410 Gone).

[creator record destroyed by citing authority, 19 June 2026]. "[title record destroyed by citing authority, 19 June 2026]." *Zenodo*, 12 Feb. 2026, https://doi.org/10.5281/zenodo.18626559. Cited by CERN / Zenodo in the bulk deletion of 19 June 2026; reference maintained by the citing authority as DOI tombstone (410 Gone). *A citation of nothing but the fact of having been cited.*

### III. Internal instruments of the present archive

Crimson Hexagonal Archive / Alexanarch. *Tombstone Mirror Census* (deletion-rate measurement, ~6.6 objects/second sustained, 2026-06-19). alexanarch.org.

———. *DataCite Full Metadata Backup* (963 records; ORCID and twelve-heteronym creator sweep, pre/post-severance epochs). data/datacite-full-backup.json, github.com/leesharks000/alexanarch.

———. *DOI Resolution Index* (1,938 mappings, dead DOI → recovered surfaces, severance taxonomy, measurement epochs). data/doi-resolution-index.json, github.com/leesharks000/alexanarch.

———. *Capture Registry* v9.0 (197 captures), incl. the reception-persistence capture: AI Mode citation of deleted Zenodo records three weeks post-deletion. machinemediation.org.

---

## Appendix A — Adversarial Citations of the Crimson Hexagonal Archive

**Dataset.** 1,834 works enumerated by the citing authority; 1,810 confirmed (Strata A–B), 24 quarantined (Stratum C); 7,336 formal citations rendered programmatically in MLA 9, Chicago 17, APA 7, and BibTeX.

**Files:**
- `adversarial-citations.json` — full dataset: per-work DOI, title, creators, date, stratum, tombstone status, metadata source, mapping confidence, citing authority, citation act, citation locus, and all four rendered formats.
- `adversarial-citations.csv` — flat table.
- `SAMPLE-MLA.md`, `SAMPLE-CHICAGO.md`, `SAMPLE-APA.md`, `SAMPLE-BIBTEX.md` — first 25 works per format.
- `STATS.json` — the counts cited in §2.4.
- `generate_adversarial_citations.py` — the generator; the dataset is reproducible from the two capture instruments cited in Works Cited III.

**Method note.** Stratum assignment is conservative: a work enters the headline count only on direct or title-verified mapping between the severed DOI and an identified work of the archive. The 24 Stratum C references — DOIs enumerated in the severance event whose parent works remain unresolved — are retained in the dataset, marked, and excluded from every count in the paper. The dataset documenting an institution's attribution practices holds itself to the standard it demands.
