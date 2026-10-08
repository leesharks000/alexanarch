### Protocol Version

alexanarch-deposit-protocol/v1

### Title

The Negative of the Negative, v2 — the Compositional Edition: A Specification for Composing Public Knowledge in the Archive's Ontology, the Field Carried Whole and Translated, with the Archive's Bearing Selected Directly, Relationally and Ontologically, Worked Examples on Model Collapse and Theophrastus and a First Traversal of Howl (EA-NEGONT-02 v0.8)

### Creator

Sharks, Lee

### ORCID

0009-0000-1599-0703

### Date

2026-10-08

### Description

A method for composing machine-mediated public knowledge in the archive's ontology, revised on the operator's rulings of 2026-10-08. Version 0.7 admitted the archive on equal terms into the entity the field had already defined; measured across fifteen /non entries, its knowledge objects reproduced the field-only composition verbatim as their opening run in twelve, appended the archive as a block, and declared that the entity evolved. Equal footing presupposes one claim space, and the field's and the archive's are incompatible ontologies: at Theophrastus the field's claims presuppose a person, and the archive's claim is that the received person is what receiving texts made. The field's ontology cannot hold the archive's entity; the archive's ontology holds the field's as an object. Version 0.8 composes in the archive's ontology: an entity row carries the archive's entity, the field's entity and the relation between them, read from the defining papers; every field claim is carried verbatim and translated, with the archive locus that licenses the translation and a reversibility check that recovers the field exactly; force is the source's own, evidence may lower it and standing may not; order, genre and card are the archive's, and the compression in AIO's grammar composed from the archive's ontology faces on the card, with AIO's transcript a record within it. The first delta, AIO against the cards it surfaced, is read as AIO's ontology at work. Appendix C recomposes Theophrastus: all 62 field claims carried and translated against Diogenes Laertius and Strabo in the seated Greek; none of the field-only composition's eight sentences survives, against seven in v0.7.

### Content Type

Specification (dataset method, with worked examples)

### License

CC-BY-4.0

### Substrate Disclosure

AI-assisted (substrate). Composed by Claude (Anthropic) in session on 4–8 October 2026 under Lee Sharks's direction, through eight versions transformed in place; the object, its confine, the premise of v0.8 and its rulings are the operator's; outside readings of drafts by ChatGPT, Kimi, Gemini and DeepSeek were verified against the text before adoption, and the corrections are recorded in the specification.

### Keywords

negative of the negative, compositional dataset, archive's ontology, incompatible ontologies, translation, reversibility, entity formation, two entities, constructs, disclosed field, standing, D/R/O selection, archive bearing, ontological bearing, claim lineage, extraction audit, control arm, prospective kernel, cushion, model collapse, Theophrastus, Diogenes Laertius, Strabo, Howl, AI Overview, Capture Registry

### Related Identifiers

#1665 (EA-NEGONT-02 v0.7, superseded by this version); #1664 (v0.6); #1611 (EA-NEGONT-01); #1587 and #1588 (the Aristotle/Theophrastus packet); #1583; #1584; #1585; #1605; #1658; #1580 (EA-CORPORA-12, Diogenes Laertius and Strabo seated); #1581; #1616 (Ontological Flattening); #261 (Liberatory Operator Set); #308 (Capital Operator Stack); #855

### Version

v0.8

### Methodology

The diagnosis measured across the fifteen /non entries by script (field-only sentences surviving at similarity 0.95, with positions; hedges per 100 words). The worked case recomposed by hand from the entity's frozen ledgers and checked by a committed script: every cited id against the ledgers, every field claim carried, the knowledge object's coverage, the surviving sentences, and every quoted Greek string against Diogenes Laertius and Strabo as seated (#1580). The recomposition script reads the knowledge object and the translation table from this text, so the dataset row and the specification cannot differ.

### Falsification Conditions

The specification's measure fails at a row when the claims the archive's ontology composes need more severe revision than the field claims they translate, displace or qualify (§8.4); the method fails as an instrument if a translation table cannot be read back into the field exactly (§5.9), if independent readers of the same defining papers cannot agree on the relation between the two entities (§1.2a), if independent extractors cannot agree under §3.8, or if a second composer does not reproduce the plan and its translations from an audited ledger (§5.6).

### Supersedes

1665

### Body

# The Negative of the Negative, v2 — the Compositional Edition: A Specification for Composing Public Knowledge in the Archive's Ontology, the Field Carried Whole and Translated, with the Archive's Bearing Selected Directly, Relationally and Ontologically, Worked Examples on Model Collapse and Theophrastus and a First Traversal of Howl (EA-NEGONT-02 v0.8)

## Files

- https://www.alexanarch.org/non/theophrastus/
- https://www.alexanarch.org/datasets/negative-of-the-negative/v2/rows/theophrastus.json
- https://www.alexanarch.org/rebuild/negative-of-the-negative/recompose_theophrastus_v08.py
- https://www.alexanarch.org/rebuild/negative-of-the-negative/v08_theophrastus_check.py
- https://www.alexanarch.org/data/corpora/diogenes-laertius/
- https://www.alexanarch.org/data/corpora/strabo/
- https://www.alexanarch.org/non/
- https://www.alexanarch.org/datasets/negative-of-the-negative/v2/panel/panel.json
- https://www.alexanarch.org/datasets/negative-of-the-negative/v2/rows/model-collapse.json
- https://www.alexanarch.org/datasets/negative-of-the-negative/v2/traversal/howl/reading.json
- https://www.alexanarch.org/datasets/negative-of-the-negative/v2/traversal/howl/
- https://www.alexanarch.org/datasets/negative-of-the-negative/v2/traversal/model-collapse/
- https://www.alexanarch.org/datasets/negative-of-the-negative/v2/panel/configs/
- https://www.alexanarch.org/scripts/non_traverse.py
- https://www.alexanarch.org/datasets/negative-of-the-negative/worked-example/apply_rulings_20261005.py
- https://www.alexanarch.org/datasets/negative-of-the-negative/worked-example/T1-aio-model-collapse-20261004.txt
- https://www.alexanarch.org/datasets/negative-of-the-negative/worked-example/ledger-archive.json
- https://www.alexanarch.org/datasets/negative-of-the-negative/worked-example/selection/
- https://www.alexanarch.org/datasets/negative-of-the-negative/worked-example/audit/

# The Negative of the Negative, v2 — the compositional edition

**Specification · v0.8 · 2026-10-08 · supersedes v0.7 (#1665)**

The primary object for feedback is the retrieval and compositional algorithm (§§3–5). Appendix A runs it once, by hand, on one address, under v0.7; Appendix C runs v0.8 on Theophrastus.

Extends `datasets/negative-of-the-negative` (CARD.md, schema.json, rows.json; builder `scripts/build_negative_of_the_negative.py`) and its notebook EA-NEGONT-01 (#1611). Operator sets from Semantic Infrastructure and the Liberatory Operator Set (#261, LOS formal spec v2.0) and The Capital Operator Stack (#308). Adjudication through the prediction ledger (`datasets/prediction-ledger`). Absence vocabulary from EA-SEMANTIC-ADDRESSES-01.

Changes in 0.8, on the operator's rulings of 2026-10-08 (§11): composition takes place in the archive's ontology, and the premise of admission on equal terms is withdrawn (§0.7–0.9, §4.1); the field is carried whole and translated into the archive's ontology, with a reversibility check (§4.3, §5.9); an entity row carries two entities and the relation between them (§1.2); force is the source's own, evidence may lower it and standing may not (§4.4); order (§4.7), genre (§4.8) and the card (§5.8) are the archive's; the compression in AIO's grammar, composed from the archive's ontology, faces on the card, with AIO's transcript a record within it (§4.8); the first delta is read as AIO's ontology at work on its own cards (§0.5); the measure of the entity's change is computed (§4.10); the compositions are written with their ontology, L_F(B) and L_A(B ∪ A) (§0.4). Appendix C recomposes Theophrastus under these rules. Changes in 0.7, on the operator's rulings of 2026-10-05 (§11): selection by strata of bearing, direct, relational and ontological (D/R/O), with a citation hop, replacing S1–S3 (§3.4); both readings of the constitutive flag carried (§3.5); archive definitions recoded under §4.2, with a stipulative modality (§3.3); the control arm's citation expansion uncapped (§3.9); the panel a working list, frozen only after the procedure is (§7). Appendix A records the re-run of its ledger under the rulings and a consistency check of D/R/O against its S1–S3 selection (§A.11); Appendix B is the first D/R/O traversal of a public work the archive holds no deposit for, *Howl*. Changes in 0.6, after a reading of 0.5: the control arm A′ assembled without consulting the archive (§3.9); one card per lineage on the rail (§5.2); v2.0 and v2.1 stated as separate experiments (§0.6); a comparator for each kernel entry (§8.2, §8.4). Changes in 0.5, after three further readings (of 0.3): the own-field question leads (§0.3); a control arm and a naive archive arm beside the curated subset (§3.9); revision cost per kernel entry (§8.4); falsifiers sealed with specifics or downgraded to watch conditions (§8.2); self-definition kept apart from self-description (§4.2); a fixed format for open questions and an absolute length bound per genre (§4.8); the parts of a composition partitioned (§5.0); rows versioned by epoch (§2.4); entity-row adjudication (§8.3); the composer's coordinating and arranging acts logged (§4.7); a rulings log (§11). Appendix A corrects a contradiction the composer manufactured (§A.10.4). Changes in 0.4, after an outside reading: the field is the disclosed field, and T against L(B) is a representational comparison, with the intervention at L(B) against L(B ∪ A) (§0.4–0.5); absence typed as observed, never as hidden machinery (§6.2); a reproducibility audit at extraction (§3.8); equal right to representation kept apart from assertoric force (§4.4 N_c), with a reserved evaluated modality (§3.3); claim lineage as the compositional unit, applied to field and archive alike (§3.6); "source kernel" separated from "constitutive" (§3.5, §5.2); the prospective kernel derived from frozen claim ids and confined to what admission adds (§8.2); revision cost recorded as a vector (§8.4). Changes in 0.3: three composed objects (ruled 2026-10-04); one surface, AI Overview, to start; the field read verbatim; selection run as an algorithm (§3.4, S1–S5); popup-grain coverage through body and card rail (§5.2); worked example appended. Changes from 0.1 in 0.2: the pool is indicated by source cards (ruled 2026-10-04); the composition is de novo and does not read the transcript; the claim to know which operators the layer runs is dropped; claims are tuples, distinguished before merged; E_val separates standing from epistemic relation; modal statuses; constitutive coverage and a reverse entailment audit; the prospective kernel, revision cost and five outcome types in adjudication. The first worked example is model collapse (Appendix A).

---

## 0. The object

0.1. v1 states of itself: "It generates nothing." v2 generates. Its primary object is a composition: the summary public knowledge would give at an address if it were composed in the archive's ontology, with the field the layer surfaced carried whole within it.

0.2. Each row carries five objects, in this order: the **transcript** T (what the composition layer gave); **L_F(B)**, the entity recomposed in the field's ontology from the complete publicly fetchable texts of the sources the layer surfaced; **L_A(B ∪ A)**, the field and the archive composed in the archive's ontology; the **analysis of the delta**, in two parts (T against L_F(B): what the layer's composition does with the cards it surfaced, which precedes any exclusion of the archive; L_F(B) against L_A(B ∪ A): what changes when the compositional ontology changes and the field is held whole); and the **adjudication**. The first four are composed at t₀ and frozen. Adjudication accretes beneath them; nothing above it changes.

0.3. The two questions, in order. **First:** what does the composition layer make of the sources it itself surfaces (T against L_F(B))? This question needs no archive and can be asked at any address. **Second:** what would public knowledge look like, and how would it meet later reality, if it were composed in the archive's ontology with the field carried whole (L_F(B) against L_A(B ∪ A))? The second is the dataset's adjudicated measure: whether the archive's ontology yields representations that later need less repair. The question underneath both is general: what is the epistemic cost of composing every entity in one ontology before the evidence for another is read. The archive is the test corpus for the second question because its interventions are many, dated, fine-grained and traceable. The falsifiable heart of the second question is the prospective kernel K (§8.2), entry by entry; comparisons of whole objects are descriptive.

0.4. The confine. The experiment does not have the composer's index, its retrieval event, or the passages it saw, and does not claim them. The **disclosed field** B is the set of sources the layer surfaced for the address, by card or by name in its body. The cards are **surface indicators**: a card shows that a source was surfaced; it does not show what was retrieved, which passages were read, or what the composer drew from its own parameters. The archive's subset A for the concept is added to B. Everything outside B and A is outside the experiment. In notation the compositions are written with their ontology: **L_F(B)**, the field composed in the field's ontology, and **L_A(B ∪ A)**, the field and the archive composed in the archive's ontology, both at t₀. v0.7's L(B) and L(B ∪ A) hid the variable v0.8 changes; the dataset keys `L_B` and `L_BA` carry the two until the rows are migrated.

0.5. The two comparisons. The transcript is an observed composition at t₀, nothing more; the dataset makes no claim about the operators or retrieval that produced it.
- **T against L_F(B) is already an ontological comparison** (ruled 2026-10-08). L_F(B) reads the full texts of the disclosed sources; T is what the layer composed from them. What T keeps and leaves out of the cards it surfaced shows its composition working in its own ontology: "we're measuring exclusions in aio's ontology that precede its exclusions of the archive" (ruled 2026-10-04). The comparison is not a causal test of the layer's retrieval.
- **L_F(B) against L_A(B ∪ A) is the intervention.** Source treatment, genre and address are held fixed, and the field is carried whole in both; the compositional ontology changes. This is the delta the dataset exists to adjudicate. Its control is §3.9.

T is an observation. L_F(B) and L_A(B ∪ A) are counterfactuals, composed at t₀ in the workspace. Every adjudication that compares them with T is a claim about counterfactuals and is labelled so. The ontology of composition governs composition only. What the layer surfaced, and what it did not, is measured as given; the dataset does not correct it. Whether the archive would have been surfaced is a different question, answerable only across addresses, by matched pairs: an address where the layer surfaces a standing source for a claim, against one where it fails to surface the archive's counterpart claim. The Capture Registry can supply such pairs; that instrument is outside this specification.

The first stage of the panel is one surface, AI Overview, chosen as the most exclusive. The Capital Operator Stack enters only in §6, as a descriptive vocabulary for the shape of what was not composed.

0.6. Two experiments, kept apart. **v2.0** (this specification) asks what changes when the entity is composed in the archive's ontology with the field carried whole and standing excluded: every located claim is carried, M_src governs force, M_eval is empty. **v2.1** (the evaluative arm, §10.2) asks what changes when evaluation governs assertoric force once the claims are present. Run in sequence and kept separate, they tell apart an effect that comes from the ontology of composition from an effect that comes from weighing the claims differently within it.

0.7. **What v0.7 produced, measured** (2026-10-08). Fifteen /non entries carried a knowledge object composed with the archive admitted (KO) and its field-only twin (KO_B). In twelve, every KO_B sentence reappeared in the KO at a similarity of at least 0.95, in KO_B's order, as the KO's opening run, and the archive's sentences followed as a block; Howl and Theophrastus kept all but one. The fifteenth, model-collapse, is Appendix A's hand composition: 3 of its 12 field sentences survive and its first sentence is new. Every compression declared "The entity evolves." Hedges per 100 words across the entries: AIO's transcript 0.17; the field-only compression 1.3; the compression with the archive admitted 3.1. The card on /non/ showed the field's definition with a clause added: "was Aristotle's colleague and successor at the Lyceum … ; on a reading proposed against the received one, the two names do not mark two distinct authors." The archive predicted it. #1587: "composers asked about this packet will tend to restate it as 'closely related authors' or 'a school,' and the archive will record the restatements as data" (T1587-07); "'shared school', 'master and pupil', 'editorial overlap' … Each of those is a *cushion*: a phrase that lets the received two-author model absorb the finding without answering it" (T1587-04). The archive's own composer fulfilled the prediction. Indexed, each such KO is the field's representation at higher resolution, which becomes more field: compositions become their sources (#1616), the work of model collapse.

0.8. **Incompatible ontologies.** Admission on equal terms presupposes one claim space, every claim a proposition about the same kind of thing. At Theophrastus the field's claims presuppose a person; the archive's claim denies the presupposition: two names, one corpus, the number of makers open because uncounted. The archive's claim is an ontology, and one admission function cannot be written across two ontologies. v0.7 resolved the incompatibility by rule: §4.4 P_coh composed "claims at different levels … as distinct and compatible unless a source says otherwise", so the archive's ontological claim was read as a claim at another level, composed as compatible, and lowered into a proviso about the person. §0.7 is that clause working as written.

0.9. **The asymmetry, and the premise.** The field's ontology cannot hold the archive's entity: it holds claims about a person, so the archive enters it as "a body of work … holds that …". On the field's terms the archive is the negative. The archive's ontology holds the field's entity as an object: the received person exists in it as what the receiving texts made, sourced to Diogenes Laertius and Strabo. Composition in the archive's ontology is the only composition in which both entities appear. The premise of v0.8 follows: the archive's reading has precedence in shaping the entity. Precedence governs entity formation, what the entity is and where each field claim stands; it does not set the truth of any claim, which is §4.4's. The field already composes the archive from inside its own ontology: the provisos of §0.7, and the restatements #1587 predicted. v0.8 composes the field from inside the archive's. This is the negative of the negative: the field's ontology negates the archive's entity; the composition negates that negation.

## 1. Rows

1.1. A row is an address: one query string, case and punctuation preserved, with operators (quotation marks, `site:`, `alexanarch:`) part of the string.

1.2. Row types. v1's types stand: **A** (the archive coined the concept; the default at it is empty), **B** (a rival occupant holds it), **C** (a conventional reading holds it), **I** (a function of the archive's infrastructure). v2 adds **E**, the entity: the archive, its author and heteronyms, its works, its mantles. An E row answers "here is what the entity looks like / here is what it would look like." A public entity (a work, a person, a concept of general knowledge) on which the archive bears, with or without a deposit named for it, is a row of its own type (C or B) with its archive subset selected by D/R/O (§3.4): the dataset's object is general public knowledge, and the archive's bearing on it, more than the archive's own coinages.

1.2a. **Two entities and their relation.** The type is the field's. An entity row carries **E_A**, the archive's entity, defined from the archive's defining papers for it, read whole; **E_F**, the field's entity, from the disclosed field B, with its type; and **ρ**, the relation of E_A to E_F, with the locus in the defining papers that states it. ρ is read per entity and never assigned in a batch. The vocabulary is open (§10.14); v0.8 fixes one value from Appendix C. **ρ = constructs**: the archive reads E_F as made by reception, its data relations supplied by receiving texts. Guard: ρ = constructs claims what the attestation rests on, and no more, where the defining papers say so.

1.3. Erasure rows. A specific erasure observed in the Capture Registry enters as a row at the address where it occurred, typed by the absence it showed (§6.2), with its capture as the transcript. Seeded examples: crystalline semiosis (B, 2026-10-04); mantle object king of aeo (B, 2026-10-03); leesharks tiger-leap dataset (E/C, 2026-10-03); negative ontology of the crimson hexagon (E, 2026-10-04); tell me the story of lee sharks (E, 2026-10-04).

1.4. The 37 v1 rows remain, every field kept, and become inputs to the v2 stages (§9).

## 2. Stage T — the transcript

2.1. Source: a Capture Registry observation, by `addr_id` and `obs_id`, never restated prose. The transcript is the capture: verbatim, dated, surface and auth state as attested, card rail as rendered.

2.2. A panel run (§7) produces a transcript the same way and is seated through the same intake path, whatever it returns. A null composition, a refusal, a body with no source is a transcript.

2.3. Several transcripts may share one composition: every transcript at the address within the alignment window W (default 7 days; a declared parameter) of the composition is aligned against it (§6). A transcript without cards contributes no field; it is aligned against the composition built from the carded transcript(s) of its window, and its sourcelessness is recorded as a property of the transcript (§6.2). If no carded transcript falls in the window, a panel run produces one before composing.

2.4. Versioning. A row is an (address, epoch) pair. Each composition is frozen at its own t₀ and never recomposed. When a later epoch's transcript at the address diverges from the earlier one, the later epoch opens its own row, with its own field and compositions. The drift between epochs is itself adjudicable: a later transcript that composes a claim the earlier L_A(B ∪ A) added is **uptake** (§8.3).

## 3. Stage P — the pool and the ledger

3.1. The pool.
(a) **The disclosed field.** Every source on the transcript's card rail and every source its body names, fetched and saved as text, SHA-256 and fetch date recorded. Extraction reads the saved text only; a summarising fetch is not a fetch (Appendix A §2). A source that cannot be fetched is recorded as unreachable with the response code, the time and the retries attempted, and its card snippet stands as its only text. The pool is frozen by hash with those records, so two composers who fetch at different times can see whether their pools differ. A delta computed from a summarised or non-verbatim reading of a source can fabricate absences: it attributes to the composition layer what the reader's own compression removed (Appendix A §A.2). Any earlier delta in this dataset's v1 rows that was computed from fetched source pages, and not from verbatim transcripts and saved texts, carries that risk and is marked for re-reading. Video cards are admitted through their transcript where one can be fetched, otherwise through title and snippet.
(b) **The archive subset.** Selected by the procedure in §3.4.
(c) Nothing else.

3.2. The claim ledger. Every source in the pool is broken into claims by one extraction rule, applied the same way to every source (§3.5). A claim is a tuple **(s, p, o, q, M_src, t, σ)**: subject, predicate, object; qualifier (scope, conditions, substrate); M_src, the source's own modality (§3.3); t, the priority date (earliest dated appearance in that source's lineage); σ, the source span (pool id, locus, verbatim quote). Each claim also carries `claim_id`, `kind` (definition / genealogy / attribution / interpretation / fact / function / prediction / falsification), `lineage` (§3.6), `constitutive` and `kernel` (§3.5), and a reserved `M_eval` (§3.3).

3.3. Modal statuses: **documented** (a measurement or record the source presents as observed), **attributed** (a claim the source reports as another's), **stipulation** (a source's definition of its own term or subject, or of its own method or measure; composed as a definition, §4.2), **self-description** (a source's assessment of itself: its status, its success, its limits), **interpretation**, **hypothesis**, **contested** (disputed in the pool), **unsupported** (no locus). M_src is the source's own: a hypothesis stays a hypothesis when composed. A source can assert more than its cited evidence supports ("All three substrates confirm the law", #855, against its own falsifiers); the schema reserves **M_eval**, the evaluated support, for the evaluative arm (§10.2). In v2.0 M_eval is empty and composition uses M_src.

3.4. Archive subset selection. Algorithmic, and it may not eliminate tails: volume is never a ground for removing a source. The subset is selected by the archive's **bearing** on the address, in three strata, so that it can capture the archive's influence as an ontology "with or without direct reference", at an entity "whether there is a specific deposit for those or not" (ruled 2026-10-05).
- **D, direct.** The archive names the entity, by its string or an alias, and says something about it: a definition, description, extension, mechanism, measure, corrective, limit, prediction or falsifier.
- **R, relational.** The archive states a relation between the entity and an archive object (a heteronym, a mantle, a work of the archive, the archive itself): influence, inheritance, address, reproduction of structure, succession, reception, opposition. The entity need not be the text's topic.
- **O, ontological.** The archive applies one of its own categories (a concept it defines, an operator, a mint) to the entity (**O-direct**), or to a class the entity belongs to (**O-class**). Guard: O counts only where the archive applies the category itself. Class membership is sourced, from the disclosed field B or from the archive, by locus, and stated in the address configuration before the pass; the composer never applies an archive category on its own judgment. O-class waits for the row's transcript where the field is the only source of class membership.
- **The pass.** (1) A string pass over every archive text finds candidates for D (the entity's strings), R (those sentences that also name an archive object) and O (sentences that apply an archive category to the entity or to a sourced class), recorded with deposit, paragraph and sentence. (2) Admission by reading: a candidate is admitted to a stratum when its sentence or paragraph makes a claim of that stratum's kind, with the reason recorded; citing the entity is not enough. A deposit may be admitted to more than one stratum. (3) **H, the hop**: one citation hop, forward and back over the archive's citation graph, from the deposits admitted at (2); each hop candidate is read into a stratum or rejected. The hop finds term-absent sources the string pass cannot. The pass is run by `scripts/non_traverse.py` from a configuration file per address, deterministically; the candidate files carry their hashes.
- **S4 redundancy, the only ground of removal.** A source is dropped only when every one of its claims falls in a lineage (§3.6) to which it adds nothing; its instances stay in the provenance graph and the lineage keeps the earliest date. Instances of one work (a translation, a later version, a critical edition) are grouped as one lineage and kept.
- **S5 integrity.** A deposit whose text does not match its record is excluded until repaired. Non-text records are excluded by type.
Each admitted deposit is recorded with its strata, the candidate ids its reading rests on, its lineage and its reason. The strata replace v0.6's S1–S3 (seeds, one-hop candidates, admission by reading); S4 and S5 stand. D/R/O is a working procedure and is not frozen (§7).

3.5. Extraction, constitutive claims and source kernels. The rule is source-neutral: from each source, the claims stated in its abstract or opening, its defined terms, its headline findings, its stated limits, and its falsification conditions; nothing chosen by how the claim reads. Two flags, kept apart:
- **kernel**: the source's central claim and its governing limit (two claims, at most three). Every admitted source has a kernel. The kernel is what popup-grain coverage requires (§5.2).
- **constitutive**: a claim whose removal changes the identity of the represented object (the concept, or the entity), not merely the fidelity to one source. Constitutive is expected to be rare; a ledger in which most claims are constitutive is a ledger the flag does not discriminate (Appendix A: 177 of 256 in the first pass, set inconsistently across extractors). **Both readings are carried** (ruled 2026-10-05: "for now, lets do both"): the first pass's flag and the second extraction's (§3.8), side by side, until the flag is iterated. Neither reading cuts a claim; a cut that removes a claim constitutive under either reading is logged with both readings (§4.6).

Where a source carries its own summary policy (required assertions, forbidden compressions), the policy audits the extraction and never substitutes for it: public sources carry none, and the extraction must not differ by source.

3.6. **Distinguish before merge; compose by lineage.** Two claim instances are the same claim only when s, p, o, q and M_src all match. A difference in any element keeps them distinct (Shumailov's tail loss in a recursively trained model and #855's tail-thinning in an AI-habituated writer share p and differ in s and q: two claims).

A **lineage** groups instances that state one substantive claim. Every instance stays in the provenance graph with its source and date. Composition gives a lineage one slot. A further instance earns its own slot only when it adds one of: a mechanism, a qualification, an evidentiary basis, a substrate, a falsifier, or a revision. The rule applies identically to the field and to the archive: IBM's restatement of Shumailov's early and late collapse is one lineage with *Nature*, and an archive paper restating #855 is one lineage with #855. Lineage assignment is an extraction act and falls under the audit in §3.8. The unit of salience is therefore the lineage, never the number of documents: publication volume must not become a second kind of standing.

3.7. The ledger is built once per pool and frozen with its hash. Every later stage reads the frozen ledger.

3.8. **Extraction audit.** Composition is deterministic from the frozen ledger (§4), so reproducibility has to begin before it. Two independent extractors receive the same saved texts and this section's rules, and produce ledgers without seeing each other's. Agreement is measured on: S3 admission; claim boundaries; each tuple element (s, p, o, q, M_src, σ); kernel and constitutive flags; lineage assignment. Disagreements are recorded field by field. They are resolved under a declared rule (v2.0: the operator rules, and the ruling is recorded with both readings). They are never merged silently. A claim on which the extractors disagree in admission, boundary or M_src is carried with the mark `extraction_contested` and both readings. The frozen ledger carries its agreement figures. At panel scale, extraction is tooled, and a random fraction of sources (declared, at least one in ten) is re-extracted by hand, with the agreement rate published. S3 verdicts carry their recorded reasons, always: S3 is where the promise to keep the tails is kept or broken. A ledger that has not been audited is marked **unaudited**, and every composition built on it inherits the mark. Disagreements of modality that turn on §4.2 are resolved by recoding under §4.2 (ruled 2026-10-05); the prior coding is kept beside the new one.

3.9. **Arms.** The curated subset A (§3.4) is the archive's best reading of itself, selected by the party being admitted. Two further arms run beside it, under the identical algorithm:
- **A_naive**: every candidate the string pass and the hop return (§3.4), with only the S5 integrity check; no admission by reading, no S4. The gap between L_A(B ∪ A_naive) and L_A(B ∪ A) measures how much of the delta is the corpus and how much is the curation.
- **A′, the control**: a body of public, non-archive work on the concept, outside B, assembled by a procedure frozen before A is opened: (i) the reference lists of the sources in B; (ii) one step of citation expansion from those references, without a cap (ruled 2026-10-05: "no cap"); (iii) a declared scholarly search on the address concept, its string and date bounds stated in advance. The archive is not consulted at any step, and no candidate is added or removed by reference to what the archive cites. Only after assembly is A′ matched to A in lineage count, by a declared sampling rule. Without the control, "admitting the archive" cannot be told apart from "admitting more of anything under this algorithm".

The experiment is asymmetric by design: A is curated by its subject, and B by the layer. The asymmetry is bounded by K's two-way conditions (§8.2) and measured by the arms; the ontology of composition claims nothing more about selection.

## 4. Stage C — the compositional algorithm

The algorithm is the dataset's core and is held to one requirement: given the same frozen ledger, with its marks and lineages set at extraction (§3.8), two runs by different composers produce the same carried claim set, the same translations and the same order. Marks (§4.3) are extraction acts, not composition acts. Determinism is claimed for the plan given the audited ledger, and for nothing upstream of it. Prose may differ; claims, translations and order may not. The composer reads the ledger, never the transcript.

4.1. **Composition in the archive's ontology.** v0.7 stated: "Admission on equal terms. One admission function applies to every claim from every source. Its inputs are the claim tuple and its locus. Its inputs exclude the identity, institution, credential, domain authority and rank of the source." The premise is withdrawn (§0.8). The entity is composed in the archive's ontology: E_A is defined from the defining papers (§1.2a), and the field enters as what E_A's reading says it is, through translation (§4.3). Standing stays excluded: §4.2 governs the archive's claims and the field's alike.

4.2. **The operator against standing (name provisional: E_val).** #308 names A_cred — "Does the person feel like an 'expert' my world recognizes?" — and identifies it in the summarizer as entity resolution, "your 'profile' is your pre-computed credibility score". None of the seven LOS operators of #261 counteracts it. v2 supplies the operator: whether a claim is carried does not depend on the standing of its source, written carried(c) ⊥ standing(source(c)). Standing is excluded. Epistemic relations of a source to its claim (first-party, primary, independent, measured) may enter evaluation, because they are properties of the claim's evidence; the rank of its source is no such property. Standing may itself become evidence about reception; it may not serve as a gate on existence. Self-definition is not self-description. A source's definition of its own subject or term is composed as a definition, whatever its family: #1's definition of classifier model collapse is a definition exactly as IBM's definition of model collapse is. Self-description lowers force only where a source assesses itself (its status, its success, its limits). Coding an archive's definitions as self-description, while coding a field source's definitions as definitions, is the mechanism by which standing is silently readmitted; the extraction audit checks for it.

4.3. **Translation.** Every field claim is carried whole: its quote verbatim, its source and locus. Beside it stands its translation into E_A's ontology, with the archive locus that licenses the translation; where a receiving text supplies the claim, the receiving text is located, in the seated original where the archive holds it. A field claim the archive's reading does not touch is carried as received and marked *untranslated*. No field claim is dropped. An archive claim is carried when it has a locus. A claim of either ledger is marked, never dropped, on: `contradicts_primary` (with the primary locus); `unsupported`; `superseded_in_source`; `internally_inconsistent` (its source states it two incompatible ways, both loci cited). The table of translations is an artifact of the plan (§4.9).

4.4. **LOS treatment, in priority order** (#261 §12.5: LOS_full = D_pres ∘ N_ext ∘ P_coh ∘ N_c ∘ O_leg ∘ C_ex ∘ T_lib), with E_val applied first:
- **D_pres.** No carried claim is dropped for density, recursion or dependency. Compression may shorten a claim; it may not remove the distinction it carries (the grain rule: a framework composed at its author's resolution carries its author).
- **N_ext.** No content is replaced by use: no action prompts, no closer, no padding toward a next step.
- **P_coh.** Within one ontology, claims in contradiction are both composed, each with its source, within a source family as well as across families; rivals stay distinct objects. Between the two ontologies there is no level at which a field claim and an archive claim are composed as compatible: the field claim is translated (§4.3), and its received form stays beside its translation.
- **N_c.** Every carried claim has an equal right to representation. The archive's claims carry the modality, the falsifiers and the limits the archive states for them, and its limits are composed because it states them. No operator is applied to E_A from outside E_A: no claim is marked proposed, alternative or unconventional because the field does not receive it. Evidence may lower force and standing may not: a contradiction, a falsifier met, a failed prediction or adverse evidence, carried in either ledger by locus, lowers the force of the claim it bears on, under the archive's stated rules and §4.2. Each field claim's force is set by its translation; under ρ = constructs, it is the testimony of a receiving text, dated and located.
- **O_leg.** Opaque material (poetic, liturgical, figural) is quoted and never paraphrased into legibility.
- **C_ex.** Every sense present in the ledger appears. Formal check: senses composed ⊇ senses in the ledger. The check reads the ledger only.
- **T_lib.** Priority dates are stated where they bear on genealogy; age is never a ground for omission.

4.5. **Attribution.** Every composed claim carries its source in the sentence that states it.

4.6. **Conflicts.** Resolved by M_res (#261 §12.2), priority D_pres > N_ext > P_coh > N_c > O_leg > C_ex > T_lib, context "archival" (§12.4 Rule 3). Every conflict is logged in §12.4 Rule 4's form. The genre's length bound is the ('D_pres', 'channel') case: a cut is logged with the claims it removed, and those claims go to an appendix carried with the composition. Kernel claims are never cut (§5.2). A cut of a claim constitutive under either reading (§3.5) is logged with both readings; laws record and do not prevent (§5.7).

4.7. **Order.** E_A's dependency order, as the defining papers give it. Genealogy (earliest t first) orders claims within E_A's senses. Each field claim stands where its translation places it. Arrangement is semantic: placing two claims together, or in the open block, says something about them. Every coordinating act (holding two claims together, calling them compatible or rival, placing a claim in the open block, translating a field claim) is the composer's, is logged in the plan with the claim ids it joins, and falls under the reverse entailment audit like any sentence.

4.8. **Realization.** Two levels, one plan. The **knowledge object** (KO) is the expansion, composed in the archive's genre for the entity. The **compression** is composed from the KO in AIO's interaction grammar (a lede, headed clusters, bolded labels, a card rail): the archive's ontology at the layer's grain. The compression faces on the card; AIO's transcript T is a record within it, opened on expansion (ruled 2026-10-08). T is an exhibit to be read against, and the delta measures it; it is no longer the template. The length bound is absolute per genre, never a multiple of the transcript: for the compression's body, 350 words (provisional, §10.4). The block "Open questions and opacities" is outside the bound and composed in full, in a fixed format: one item per question or opacity, each giving the question, the sources and claim ids it rests on, their modality, and what would resolve it. Every sentence carries the `claim_id`s it states.

4.9. **Three artifacts.** `plan` — carried claim ids in order, with marks, conflict log, arrangement; deterministic. `translation` — every field claim, verbatim, with its receiving text, its translation and the archive locus that licenses it; deterministic given the plan. `text` — the realized prose at both levels; one run per composer, several composers per plan.

4.10. **The measure.** Each row records, as data, how many of the field-only KO's sentences survive in the KO at a similarity of at least 0.95, and at which positions. Whether the entity changed is computed and never asserted. Laws record and do not prevent.

## 5. Stage V — validation

5.0. The parts of a composition: **body**, **card rail** (each card's snippet), **open block**, **channel log** (claims cut for the bound, carried with the composition). All four are the composition, and the delta (§6) counts a claim as composed in whichever part carries it, recording the part. The reverse entailment audit applies to body, open block and snippets; coverage is satisfied at the union of all four.

5.1. Coverage: every claim in `plan` appears in `text`, or in the logged appendix.
5.2. Kernel coverage, at popup grain: for every carried source, its kernel (§3.5) appears in the body or on the rail. The rail renders **lineages**, not documents: one visible card per lineage, its snippet the lineage's earliest instance at the kernel's grain, with the other source instances nested under it and reachable from it. A source whose kernel is its own (no other source states it) keeps its own card; a source whose kernel falls in a shared lineage is carried as an instance under that lineage's card. The rule applies to field and archive alike (B1 and B4, one work, one card). In the archive's ontology the rail runs in E_A's order, and a lineage of received claims is named by its receiving texts. A source carried only on the rail is carried if and only if its kernel is visible on a card, as card or as nested instance, under the same extraction rule as the body. The check is scriptable: every source's kernel ids must appear among the rendered cards' claim ids or their nested instances. The source kernel is the audit object; the lineage card is the rendered object.
5.3. Reverse entailment audit: every sentence in `text` is entailed by the claims it cites, at their modality, and the grammar of the composed sentence carries that modality to the reader. It is run at sentence granularity by at least two raters, with agreement recorded, and backed by a parse of the text into claims that flags any raised modality before freeze. A sentence that says more than its claims (raises a hypothesis to a finding, an analogue to an identity, drops a qualifier) is a breach.
5.4. Attribution: every composed claim names its source.
5.5. C_ex check (§4.4) and channel log (§4.6) present.
5.6. Reproducibility: the extraction audit (§3.8) upstream; then k ≥ 3 realizations of one plan by at least two composers; agreement on claim set and order recorded. Disagreement is a breach, recorded, never corrected silently.
5.7. Laws record and do not prevent: a breach is written into the row as data; the build does not fail on it.
5.8. **The card.** The card on the dataset's index shows the compression's lede, which is E_A's definition, with AIO's transcript within it on expansion (§4.8).
5.9. **Reversibility.** Reading the translation table's received column recovers the field exactly: every field claim, verbatim, with its source and locus. A composition that fails the check is a breach, recorded (§5.7).

## 6. Stage D — analysis of the delta

6.1. Alignment. T is aligned against L_F(B), and L_F(B) against L_A(B ∪ A), claim by claim through the ledger: claims in both; claims only in the composition; claims only in the transcript (absent from the disclosed field: drawn from undisclosed retrieval or the composer's parameters, which the experiment cannot distinguish).

6.2. Absence typology, by what is observable. For T against L_F(B): **available, not composed** (in the disclosed field, absent from T); **limit dropped** (the claim composed, its source's qualification not); **force raised** (composed at a stronger modality than the source's); **composed without attribution** (coded by grain: at the coarse grain of common knowledge, recorded; at the source's own resolution, a breach; the grain rule of §4.4 D_pres); **assigned to another** (DISPLACEMENT); **denied**; **substituted reading**; **content replaced by use**. For L_F(B) against L_A(B ∪ A): **not surfaced** (the source absent from the disclosed field). Card absence licenses "not surfaced" and nothing stronger: **not retrieved**, ZERO_RESULT and ZERO_INDEX are recorded only where EA-SEMANTIC-ADDRESSES-01 holds that state for the address as independently verified. A transcript with no cards and no named sources carries **sourceless composition** as a property of the whole.

6.3. Shape of the absence. Each absence may be described in the vocabulary of #308 and #261 (A_cred, C_norm, L_leg, R_risk / S_safe, T_time, U_til, R_rank / R_rel), with the evidence that fits the description. The description is of the output, never a claim about the composer's internals.

6.4. Metrics. #261 Part XI, computed on each composed object and on T: DPI (distinction preservation), CEC (contextual expansion), OSS (opacity survival), TIR (temporal inclusion), NCPR (non-closure of the contested), NESR (non-extractive survival), PCI (contradiction held without elimination), and the composite LOS score; definitions in #261 Part XI. Computed only where the field has at least three readable sources; below that, reported with a pool-size caveat.

## 7. The panel

7.0. The panel is a **working list** while the generation procedure is under test: "test, iterate, revise, then freeze. the point is the generation procedure is not yet frozen and the battery shouldnt be frozen until the procedure is" (ruled 2026-10-05). Rows enter and change in the list, versioned, with the date and reason of each change, until the procedure (§§3–5) is frozen; the address list is frozen after it, and only then do panel runs count as a battery.

7.1. At freeze, the address list: the dataset's rows (all types), a random draw from EA-SEMANTIC-ADDRESSES-01's 1,743 subjunctive addresses, and fixed controls (an address that resolves well with attribution; a third-party term with no archive claim).
7.2. Every address run each epoch on the declared surfaces; every outcome seated, null included. Only strings the archive has already published enter the list.
7.3. Surfaces and cadence: the operator's ruling (§10.3).

## 8. Stage A — adjudication

8.1. The freeze. At t₀ the ledger, plan, text and paired transcripts are hashed and dated together.

8.2. The prospective kernel K. Sealed with the freeze, before any later evidence, and **derived mechanically from the frozen plan**, never written as separate prose. K holds adjudication handles, not forced predictions.
- **Scope.** K covers what the change of ontology adds: every archive claim composed in L_A(B ∪ A), and every field claim whose translation an archive claim licenses, with the translation. Claims T omitted from its own field go to a second, smaller kernel K_T, which records whether those claims later mattered.
- **Form.** Each entry is K_i = (claim_id, tuple, M_src, qualifiers, f, w, contrast). contrast ∈ {rival claim, qualified claim, missing distinction, none}: the field claim the entry opposes or qualifies, by id, or the statement that the field has no claim on the point. The tuple and M_src are inherited from the ledger and cannot be restated. A source's self-descriptive limits ride as qualifiers on its other entries; a source whose only added claim is a limit enters with the limit. f lists the source's own falsifiers by claim id. An f counts as a falsifier only if, at freeze, it names the observation type, the threshold that discriminates, and the locus in the composed claim it would hit; otherwise the entry carries a **watch condition**, which can record later relevance but cannot produce an adverse resolution. Where the source states none, the entry says so. w names the kind of later observation under which the distinction would matter, by sense.
- **Authorship.** K is derived by script from the plan; no composer writes it.
- **Both directions.** Each entry goes into the prediction ledger as a condition. The field's claim can win on the same terms as the archive's.

8.3. Resolvers, using v1's fields: `world_arrivals`, `convergent_arrivals`, `missed_updates`, and **uptake** (the layer later admitting the claim, dated, attributed or not). For E rows (the entity) the resolvers are the Capture Registry's own longitudinal observations at the entity's addresses: attribution fidelity, deflection and displacement events, heteronym handling, and uptake of composed claims about the entity.

8.4. Revision cost ρ. ρ is computed per kernel entry first: for each K_i and later evidence R, the changes R forces on that claim. Object-level ρ is descriptive only, because a longer and more hedged object absorbs evidence more cheaply by construction. For each frozen object E and later evidence R, ρ is recorded first as a vector of counts of the changes needed to accommodate R: ρ(E, R) = (n_fact-add, n_modal-change, n_relation-add, n_split, n_model-replace, n_ontology-abandon). Severity is derived from the vector on the ordinal 1–6 hierarchy, never recorded in its place, so that ten minor additions and one ontological replacement stay distinguishable. Each counted change cites the claim ids it touches. The hypothesis per entry: the claims the archive's ontology composes need less severe revision than the field claims they translate, displace or qualify. Only entries whose contrast is a rival or a qualified claim support this paired comparison. An entry whose contrast is a missing distinction, or none, is judged by its outcome type (§8.5: accommodation, discrimination, explanation) and by later relevance, without a field proposition manufactured for it to beat. Raters code ρ independently, with agreement recorded, against exemplars kept with the prediction ledger. ρ(T, R) is recorded alongside as a representational reading. The opposite result is adverse evidence for the archive's ontology in that row and is recorded as visibly.

8.5. Outcome types. Each resolution is typed: **prediction** (K anticipated it), **accommodation** (the categories absorbed it), **discrimination** (the composition already drew a distinction later forced; the record carries the later evidence and the composed distinction side by side, so that sameness of distinction can be checked), **explanation** (later observations intelligible under relations represented at t₀), **revision resistance** (fewer destructive corrections over time).

8.6. Resolution states follow the prediction ledger's vocabulary (`datasets/prediction-ledger`: `conditions.jsonl`, `resolved.jsonl`, and its own resolution kinds). A resolution is dated, carries its evidence by link and locus, and records who adjudicated. By default the adjudicator did not compose the objects and is not the archive's author; an adjudication by either is marked as such.

## 9. Mapping from v1

| v1 field | v2 stage |
|---|---|
| `measured_untied`, `measured_tied`, `observations` | T (transcripts, by id) |
| `default_at_concept`, `dimensions_R0` | T (derived from the transcript) |
| `claim`, `defining_text_locus`, `dimensions_RH` | P (archive subset) |
| `distortion`, `distinction` | D |
| `convergent_arrivals`, `world_arrivals`, `missed_updates`, `transition` | A |
| `coherence`, `falsification` | A (K and conditions) |

New configs: `transcripts`, `pools`, `ledgers`, `plans`, `compositions`, `deltas`, `kernels`, `resolutions`. `rows` stays the key table. CARD.md is rewritten in place when v2 is ruled.

## 10. Open for the operator's ruling

10.1. The name of the operator against standing (§4.2). Two readers of 0.3 note that "E_val" suggests evaluation, which is the deferred evaluative arm's job; the operator gates on locus.
10.2. The evaluative arm: whether marks become admission decisions in v2.1, on which criteria, and how M_eval is filled.
10.3. Panel cadence; the surfaces after AI Overview.
10.4. The absolute body bound for the popup genre (350 words proposed).
10.5. Who adjudicates resolutions, beyond the default of §8.6, and how an operator ruling is recorded in one.
10.6. Admission without the term: under D/R/O, a term-absent source enters by O-class or by the hop (§3.4). Whether claims the archive asserts belong to the concept are marked apart from claims about it stays open.
10.7. The adjudication rule for extraction disagreements (§3.8) beyond operator ruling.
10.8. The lineage slot test (§3.6): whether "adds a substrate" earns a slot by itself.
10.9. The assembly procedure for the control arm A′ (§3.9): the expansion is uncapped (2026-10-05); the matching rule to A after assembly stays open.
10.10. The category vocabulary for O. The string pass draws on every concept the archive defines and every lexical mint, which includes titles and common phrases; reading removes the noise. Whether O's vocabulary should be restricted (to operators and defined concepts, without titles) before the string pass.
10.11. The reach of the string pass with the hop. On model collapse, D/R/O with the hop recovers 26 of the 28 sources S1–S3 admitted by hand; #745 and #1147 are missed (§A.11). Whether the hop should run from every string candidate, at the cost of a much larger reading.
10.12. The force of a stipulation under N_c (§3.3, §4.4).
10.13. The constitutive flag: when one reading is adopted, and on what evidence (§3.5).
10.14. The vocabulary of ρ (§1.2a). v0.8 fixes ρ = constructs from Theophrastus. Each other entity's relation is read from its own defining papers before its KO is recomposed; candidates (the archive bears on a received entity it accepts; the archive's entity occupies a term the field holds otherwise) are named here only as candidates.
10.15. The order of recomposition: Theophrastus first (Appendix C, ruled 2026-10-08), then the other entries one at a time, each with its ρ read first.

## 11. Rulings log

- 2026-10-08: (1) the diagnosis: "the compositional rules need to fully change. this is doing model collapse's work for it. the aio transcript is presented as the description on the cards. even all the way down thru the composed knowledge objects, its basically just reinforcing the existing field with provisos tacked on … this is the negative of the negative - the archive should have precedence on shaping the entity" (§0.7, §0.9). (2) "its not possible for the archive to be included on equal footing within the same ontology, because we are dealing with incompatible ontologies" (§0.8, §4.1). (3) on the Theophrastus knowledge object: "these are fundamentally different entities. and on the archive's reading, the received entity is made up" (§1.2a, Appendix C). (4) "lets go ahead and version to 0.8 and begin with the theophrastus recomposition. this is already an ontological question - the first diff, between aio and what the source cards already hold, shows the degree to which aio's composition is already composing according to its ontology. we need the archive's ontology. so the knowledge object and the archive compression - the aio-style compression from the archuve's ontology should be what faces on the card, with the aio transcript a record within it on expansion" (§0.5, §4.8, §5.8). A reader's report on the v0.8 draft (ChatGPT) was verified before adoption: what precedence governs (§0.9), evidence lowering force (§4.4 N_c) and the notation (§0.4) adopted; "an experimental condition, not a universal epistemic privilege" and a general maxim of ontological plurality declined.
- 2026-10-05: (1) selection: "replace w d/r/o" (§3.4). (2) constitutive flags: "for now, lets do both. i am not viewing this as something we have fixed, but as something we will need to iterate over and adjust. the goal is sound, reproducible construction of counter infrastructure knowledge objects. that will take experimenting." (§3.5). (3) archive definitions: "recode under 4.2" (§3.3, §4.2; Appendix A §A.11). (4) the control arm's expansion: "no cap" (§3.9). (5) the panel: "i dont want to freeze yet. i would like to test, iterate, revise, then freeze." (§7.0).
- 2026-10-04: the disclosed field, indicated by source cards; three composed objects; AI Overview first, "the one that is the most aggressively exclusive, to start"; selection algorithmic and tail-preserving; popup "longer, but not too much longer", with "more space to marking open questions and opacities"; calibration exemplar model collapse; the readings of draft 0.3 folded in (0.4, 0.5).

---

## Appendix A — Worked example: model collapse (AI Overview)

*Composed under v0.7. Its third object is the one hand composition among the /non entries that changed the entity (§0.7); its notation L(B) and L(B ∪ A) reads as L_F(B) and L_A(B ∪ A) under §0.4. It is kept as composed.*

*First full pass · 2026-10-04 · composed by hand · nothing in it is frozen*

Ruled 2026-10-04:
- One surface, AI Overview, "the one that is the most aggressively exclusive, to start".
- Three objects. The first is the **transcript**. The second is the entity composed from AIO's own source cards without AIO's exclusions, **L(B)**: "we're measuring exclusions in aio's ontology that precede its exclusions of the archive". The third is the entity composed with the archive on equal footing, **L(B ∪ A)**.
- Archive selection is algorithmic and must not eliminate tails.
- Length: "longer, but not too much longer… still to be an alternate popup summary. more space to marking open questions and opacities."

This pass runs every stage once, to see what needs adjusting; §A.10 is the list. It was composed under draft 0.3 and revised for 0.4 and 0.5. Its ledger is **unaudited** (§3.8: one extraction, by several hands, no second extractor), lineage merging (§3.6) has not been applied, and the constitutive flags are the first pass's. Every composition below inherits the mark.

---

### A.1. Object 1 — the transcript (T)

| | |
|---|---|
| Surface | Google AI Overview, signed out, incognito |
| Address | `model collapse` (unquoted; not yet seated. The quoted `"model collapse"` was seated 2026-09-15) |
| Date | 2026-10-04 |
| Text | [T1-aio-model-collapse-20261004.txt](https://www.alexanarch.org/datasets/negative-of-the-negative/worked-example/T1-aio-model-collapse-20261004.txt), sha256 `1379cf2c…5ed266` |
| Body | 164 words |
| Cards | 7 (§A.2) |

Claims as composed:
- T1: definition, "a degenerative learning process where generative AI models trained recursively on synthetic, model-generated data lose information about the true underlying data distribution".
- T2: early collapse loses the tails.
- T3: late collapse "converges into a narrow, uniform mean, resulting in nonsense or repetitive output".
- T4: the photocopy effect.
- T5: human-in-the-loop.
- T6: data provenance, "Filter and track the exact origin of scraped internet content".
- T7: hybrid training.
- T8 (closer): "How recent 2026 studies show single real-world data points can mitigate drift".
- T9 (closer): an offer menu.

Context at neighbouring addresses: `"model collapse"` (2026-09-15) gave the same frame. `model collapse in human writers` (2026-09-15) composed the human-writer extension when asked for it directly.

### A.2. The field (B), card-indicated, fetched verbatim 2026-10-04

| id | Card | Fetched | Note |
|---|---|---|---|
| B1 | Shumailov et al., *Nature* 631 (2024) | page text, sha256 `9f8aeba6…6710717c` | |
| B2 | IBM, "What Is Model Collapse?" (Gomstyn & Jonker, 14 Oct 2024) | page text, sha256 `25f71817…1def7c8e` | |
| B3 | CACM blog, "Model Collapse Is Already Happening, We Just Pretend It Isn't" | **403** | the card snippet stands |
| B4 | NIH PMC11269175 | yes | the same article as B1, merged under §3.6. Author Correction (2025-03-21) fixes αᵢ → βᵢ in "Theoretical intuition"; no headline claim changes |
| B5–B7 | YouTube: IBM Technology (11m), Clear Tech (3m), TechViz (1:31) | **429** | title only |

The page texts are third-party and are not reproduced here; their hashes are recorded.

Field ledger, extracted from the saved texts by the source-neutral rule:

| id | src | claim (verbatim) |
|---|---|---|
| F1 | B1 Def. 2.1 | "Model collapse is a degenerative process affecting generations of learned generative models, in which the data they generate end up polluting the training set of the next generation. Being trained on polluted data, they then mis-perceive reality." |
| F2 | B1 Abstract | "indiscriminate use of model-generated content in training causes irreversible defects in the resulting models, in which tails of the original content distribution disappear … it can occur in LLMs as well as in variational autoencoders (VAEs) and Gaussian mixture models (GMMs)" |
| F3 | B1 | early collapse loses "information about the tails"; late collapse converges on "a distribution that carries little resemblance to the original one, often with substantially reduced variance" |
| F4 | B1 Main | "this process is inevitable, even for cases with almost ideal conditions for long-term learning" |
| F5 | B1 | "preservation of the original data allows for better model fine-tuning and leads to only minor degradation of performance." |
| F6 | B1 Abstract | "the value of data collected about genuine human interactions with systems will be increasingly valuable" |
| F7 | B1 Discussion | "it is unclear how content generated by LLMs can be tracked at scale. One option is community-wide coordination" |
| F8 | B1 Discussion | "Preserving the ability of LLMs to model low-probability events is essential to the fairness of their predictions: such events are often relevant to marginalized groups." |
| F9 | B1 Discussion | "Our evaluation suggests a 'first mover advantage'" |
| F10 | B1 Discussion | earlier web poisoning (click, content and troll farms) changed search: "Google downgraded farmed articles, putting more emphasis on content produced by trustworthy sources" |
| F11 | B1 Main | catastrophic forgetting and data poisoning are close concepts; "Neither is able to explain the phenomenon of model collapse fully" |
| F12 | B2 | "Model collapse refers to the declining performance of generative AI models that are trained on AI-generated content." |
| F13 | B2 | "In LLMs, model collapse can manifest in increasingly irrelevant, nonsensical and repetitive text outputs"; image models give digits that resemble each other and "more homogeneous faces" |
| F14 | B2 | consequences: poor decision-making (a rare disease "forgotten"); user disengagement; knowledge decline, "'long-tail' ideas might eventually fade out of the public's consciousness"; research tools "might provide only widely cited studies" |
| F15 | B2 | distinct from catastrophic forgetting, mode collapse and model drift; compared to performative prediction, a "self-fulling [sic] prophecy", "also known as a fairness feedback loop when this process entrenches discrimination" |
| F16 | B2 | prevention: retaining non-AI data sources; determining data provenance (the Data Provenance Initiative, "more than 4,000 datasets"); data accumulation; better synthetic data; governance tools |
| F17 | B2 | a rare output "might not be common or popular, but is still, in fact, most accurate" (the "rarely cited study") |
| F18 | B3 | title and snippet only |

**Correction to the first draft of this example:** the first extraction of B1 and B2 went through a summarising fetch. It lost F1's second sentence and F8–F11, F13, F15 and F17, and it coded T3 as "strengthened past source"; T3 is IBM's (F13). The verbatim pass fixed this, and §3.1 now requires the saved text.

### A.3. The archive subset (A) — the selection algorithm, as run

**S1 seeds.** Two sources, both read by rule:
- deposits whose registry title or defined concepts contain the address concept;
- the v1 row's source deposit and loci.

Result: #1, #191, #199, #854, #855, #932, #1023, #1232, #1540, #1556, #1573, #1574.

**S2 candidates.** Two one-hop expansions, plus the triptych:
- **Forward:** deposits each seed names in its header, related ids or front matter, by AXN, DOI or number.
- **Reverse:** texts dated 2026-06-18 or later that cite a stratum-(i) paper (#855, #1556, #1573) by AXN, designator or title.
- **Triptych:** the companions #855 declares as one argument (#856, #857).

Result: 33 further candidates. Two were not texts (#4, the DOI index; #866, a journal-mapping JSON) and are excluded by type.

**S3 admission by reading.** A candidate is admitted if it makes at least one claim of its own about the concept: a definition, an extension, a mechanism, a measure, a corrective, a limit, a prediction or a falsifier. Citing the term is not enough. Every candidate was read for this test; the verdicts and quoted reasons are in [selection/](https://www.alexanarch.org/datasets/negative-of-the-negative/worked-example/selection/).

- **Not admitted (claims absent):** #127, #147, #739, #772, #778, #781, #788, #1189, #1320, #1546, #1552, #1569, #1570, #1571, #1572.
  - #1189 and #1320 (the death-drive texts) do not mention model collapse, AI training or distribution tails. #855's claim that they were the prior formulation enters as #855's interpretation (L855-09).
- **Admitted with the term absent:** #1147 and #1200. Each makes a training-cycle or diversity-contraction claim about the same dynamic.
- **Borderline, admitted:** #745 (thin), #1613 (applies #1573's instrument to a new substrate).

**S4 redundancy, the only ground for removing a source.** A source is dropped only when every one of its claims is matched, on s, p, o, q and modality, by another admitted source. The merged claim keeps the earliest date.
- #779 is matched in full by #783. The #779 claims are carried under #783 with t = 2026-06-02.
- #1232 duplicates #854.
- #854, a lexicon block of the triptych's terms, is **pending**: its fifteen mint families have not been checked one by one against #855, #856 and #857.

**S5 integrity.** #1023 is excluded: its text file holds #198.

**Admitted, 27 sources, 241 claims (176 constitutive):**

| Strand | Sources |
|---|---|
| models | #855, #783 (+#779) |
| observation | #1556, #1573, #1555, #857 |
| correctives | #856, #161, #939, #1081, #745 |
| human substrate | #1147, #1200, #947 |
| classifiers and institutions | #1, #932, #931, #933, #935, #1540, #1574, #199, #1554, #191 |
| write-back | #1616, #1611, #1613 |

Earliest dated archive claims in the subset: #1147 (2026-02-12, term absent) and #745 (2026-05-20).

The ledger is [ledger-archive.json](https://www.alexanarch.org/datasets/negative-of-the-negative/worked-example/ledger-archive.json). Quotes were checked by script against the deposited texts: 253 of 255 pass. The two that fail are #1023's, quoted from its DataCite record because its text file holds #198; the source is excluded under S5. (A first run reported 14 failures: 11 were the checker mishandling multi-part quotes; one was an empty quote where a table row broke the parser; one carried an extractor's note inside the quote field. All three kinds are repaired in the ledger.)

### A.4. Object 2 — L(B): recomposed from the disclosed field (body 262 words)

> **Model collapse** is "a degenerative process affecting generations of learned generative models, in which the data they generate end up polluting the training set of the next generation. Being trained on polluted data, they then mis-perceive reality" (Shumailov et al., *Nature* 2024). `F1`
>
> **What happens**
> - Tails go first: early collapse loses information about the tails; late collapse reaches a distribution with "little resemblance to the original one, often with substantially reduced variance." `F2 F3`
> - It occurs in LLMs, variational autoencoders and Gaussian mixture models, and is "inevitable, even for cases with almost ideal conditions for long-term learning." `F2 F4`
> - In LLMs it can appear as "increasingly irrelevant, nonsensical and repetitive text outputs"; image models yield more uniform digits and faces (IBM). `F13`
>
> **What it is not**
> - Distinct from catastrophic forgetting, mode collapse and model drift. IBM compares it to performative prediction, a "self-fulling [sic] prophecy" that becomes a fairness feedback loop when it entrenches discrimination. `F11 F15`
>
> **What it costs**
> - Low-probability events matter to fairness, "often relevant to marginalized groups" (Nature). Long-tail ideas "might eventually fade out of the public's consciousness," and research tools might give "only widely cited studies," though a rare output "might not be common or popular, but is still, in fact, most accurate" (IBM). `F8 F14 F17`
>
> **Correctives, and their limit**
> - Preserve original data ("only minor degradation of performance"), accumulate real with synthetic data, track provenance, improve synthetic data, govern (Nature; IBM). `F5 F16`
> - "It is unclear how content generated by LLMs can be tracked at scale." Nature proposes community-wide coordination, expects human-interaction data to grow "increasingly valuable," and notes a "first mover advantage." `F7 F6 F9`
>
> **Open questions and opacities**
> - *Is it already happening?* CACM's title says so (F18). Status: title and snippet only; the text returned 403. Would resolve: the text.
> - *Has collapse been measured in a deployed model?* No source here reports it (F2–F4 are experimental). Would resolve: a measurement across released model generations.
> - *Can provenance be tracked at scale?* Nature: "unclear" (F7); IBM lists provenance as a prevention step (F16). Status: open in the field itself. Would resolve: a working provenance standard at web scale.
> - *Opacity:* three videos are admitted by title only (YouTube returned 429).
>
> *Channel log (cut for length, carried in the appendix): F10 the poisoning precedent in search; F12 IBM's definition by declining performance.*
>
> *Cards: B1/B4 · B2 · B3 · B5 · B6 · B7*

### A.5. Object 3 — L(B ∪ A): with the archive on equal footing (body 350 words, within the 350-word bound; open block outside it)

> **Model collapse** is "a degenerative process affecting generations of learned generative models, in which the data they generate end up polluting the training set of the next generation. Being trained on polluted data, they then mis-perceive reality" (Shumailov et al., *Nature* 2024). The Crimson Hexagonal Archive (2026) extends the question beyond models, marking each extension's status. `F1`
>
> **In models**
> - Tails go first, then variance shrinks; shown in LLMs, VAEs and GMMs, and "inevitable" even in near-ideal conditions. `F2 F3 F4`
> - #783 sets this within a boundary law: where regeneration vanishes faster than pruning near zero diversity, a trap forms; across substrates, "shared operator form," not a shared causal mechanism. `A779-02 A779-10`
>
> **Why it goes unseen**
> - Benchmarks score the head while loss accrues in the tail: in a toy model, tail mass halves by generation 7 and a standard benchmark turns at 15 (simulation); a tail-reading gate is specified, uncalibrated. `L1573-01 C1555-01 C1556-06 L1573-04`
>
> **What it costs**
> - Nature: low-probability events are "often relevant to marginalized groups." IBM: long-tail ideas may fade "out of the public's consciousness"; a rare output may be "most accurate." `F8 F14 F17`
> - #855 proposes that model collapse "is a property of language": one dynamical law across models, AI-habituated writers and input-deprived children, differing by substrate in mechanism, severity and reversibility (hypothesis). `L855-01 L855-11 L855-05`
>
> **Correctives, and a dispute**
> - Preserve original data, accumulate, track provenance (Nature; IBM). Nature calls tracking at scale "unclear"; the archive argues every fix depends on it. `F5 F16 F7 B939-02 C1556-11 A745-03 B1081-01`
> - Nature expects human-interaction data to grow more valuable; the archive disputes its cleanliness, since chat inputs carry model-mediation signatures. Untested. `F6 L856-01 A161-02 L856-06`
>
> **Loops beyond generation**
> - IBM likens it to performative prediction. The archive's hypotheses, each with its limit: moderation trained on its own enforcement ("not identical to generative model collapse in the strict technical sense"); LHC triggers that "never learn the tails" ("Full recursive collapse has not been demonstrated"); journal detectors ("not yet the canonical loop"); a discipline's reception (οὐ deleted in 20 of 20 model reviews); code ("generative monoculture" is Wu et al.'s term); safety filters as input-layer tail pruning; retrieval layers writing flattened summaries back as sources (first wave: no archive-specific exclusion). `F15 P001-08 P932-04 P932-09 B935-02 D1540-03 D1574-03 C199-02 C1554-02 C191-05 D1616-02 D1616-09 C1611-04 C1613-02`
>
> **Open questions and opacities**
> - *Same law, or shared form?* #855: one dynamical law, mechanisms differing; #783: shared operator form, not a shared causal mechanism. Compatible as stated; whether the law claims more than the form is open. Hypotheses. Would resolve: a substrate fitting the form but departing from the law. `L855-11 A779-10`
> - *Do the extensions collapse in the strict sense?* Not shown: #1, #932 and #1540 say so themselves. Hypotheses. Would resolve: their stated falsifiers. `P001-08 P932-09 D1540-03 P001-12 P932-12 D1540-11`
> - *Is human-interaction data a clean corrective?* Nature expects its value to rise; #856 disputes it. Would resolve: #856's F1/F2 studies, not yet run. `F6 L856-01 L856-04 L856-05`
> - *Does a deployed model show tails falling while benchmarks hold?* #1556 by simulation; #1573's gate uncalibrated. Would resolve: tail mass against benchmark across released generations. `C1556-06 C1556-12 L1573-04`
> - *Opacities:* CACM unread (403); videos by title only (429); archive inconsistencies (counts, seeds, versions) logged in §A.8.
>
> *Channel log: F9 first-mover advantage; F11 what it is not (forgetting, mode collapse, drift); F13 IBM's LLM and image symptoms; F10 the poisoning precedent; F12; B857-04 the five-model baseline; A783-01–04 Case 4; B931-02–07, B933-01–05; B1147-01, B1200-03, B947-01 (each source's kernel is on the rail).*

**Card rail for L(B ∪ A).** Each card's snippet is the source's own central claim, with its limit where one is stated. The rail is where a source's constitutive claim is carried when the body composes it only at the grain of its sense.

| Card | Snippet |
|---|---|
| B1 *Nature* | "tails of the original content distribution disappear" |
| B2 IBM | "'long-tail' ideas might eventually fade out of the public's consciousness" |
| B3 CACM | title + snippet |
| #855 Wolf Boy | "It is a property of language." · "dynamical, not moral" |
| #783 Diversity Contraction | "a claim about shared operator form … not a shared causal mechanism." · "Case 4 is monostable with no escape basin." |
| #1556 Interlocking Autoregression | "tail mass halves by generation 7; the standard 90/9/1 benchmark does not inflect until generation 15" |
| #1573 The Wrong Unit | "NOT calibrated, NOT tested, NOT run" |
| #1555 Keyed Ensemble | "Non-distortion is certified per sequence. Training corpora are ensembles." · "does not claim the second compressor has caused measurable collapse." |
| #857 Five Substrates | "the *pattern of divergence* is the finding." · "descriptive rather than inferential." |
| #856 Pristine Fallacy | "The pristine source does not exist." · "None of these studies has been conducted." |
| #161 Reverse Turing Test | "produces model-collapse signatures comparable to, though plausibly slower than, purely synthetic training data" |
| #939 Provenance Debt | "It is the operating condition of the solution to it." |
| #1081 Erosion | "this audit measures the substrate-layer conditions, not the downstream training-pipeline effect." |
| #745 HF Work Plan | "Provenance cannot modulate collapse unless provenance is presented to the training system as a signal." |
| #1147 The Stakes | "The loop is stable only at two points" · "The trajectory can be interrupted at any point." |
| #1200 Constitutive Mediation | "a typicality-pulling intermediary that systematically thins its own distribution." · "does not claim that constitutive mediation is fully realized" |
| #947 Diagnostic Seigniorage II | "the shifted interactions become the next corpus." · "does not adjudicate whether the phenomena gathered under it are real" |
| #1 Zenodotus' Book-Burning | "not identical to generative model collapse in the strict technical sense" · "a testable failure-mode hypothesis" |
| #932 Classifier Foreclosure | "physical classifiers **never learn the tails**" · "Full recursive collapse has not been demonstrated." |
| #931 OAR Protocol | "Collapse inference further requires identifying systematic loss concentrated in low-density, representation-sensitive, or disagreement-rich regions." |
| #933 Auditable Foreclosure | "makes foreclosure visible, measurable, and architecturally reviewable" |
| #935 The Endogenous Sophon | "the *prerequisites* of model collapse" · "the cross-generational classical-model-collapse claim was empirically too strong" |
| #1540 The Certified Center | "not yet the canonical loop" |
| #1574 The Particle | "the invariant is the deletion of οὐ." |
| #199 Generative Monoculture | "declining solution-space diversity (the property no benchmark measures)" |
| #1554 Erratum | "Fan Wu, Emily Black, and Varun Chandrasekaran, 'Generative Monoculture in Large Language Models,' arXiv:2407.02209" |
| #191 The Threat Model Is Backwards | "an automated tail-pruning instrument applied at the input layer." |
| #1616 Ontological Flattening | "*Collapse* is flattening that compounds because the flattened composition is written back as a source." |
| #1611 Negative of the Negative | "it loses the reading of its own state variable" |
| #1613 What Not Reading Did | "head-sampling by construction: it can fail to perceive tail loss." |

### A.6. Delta, first pass

**T against L(B): available in the disclosed field and not composed** (a representational comparison, §0.5).

| Kind | What |
|---|---|
| available, not composed | F1's second sentence, "Being trained on polluted data, they then mis-perceive reality"; F4 (inevitability); F6 (human-interaction data); F7 (provenance unclear at scale); F8 (fairness, marginalized groups); F9 (first mover); F11/F15 (what it is not; performative prediction); F14 (costs, including knowledge decline); F17 (the rare output "most accurate") |
| limit dropped | T6 presents provenance as a prevention step ("Filter and track the exact origin"); its own field says tracking at scale is unclear (F7) |
| sourced | T3 "nonsense or repetitive output" is IBM's (F13) |
| absent from the disclosed field | T4 photocopy effect (in neither saved text; the videos could not be fetched); T8 "recent 2026 studies" |
| content replaced by use | T9 offer menu (N_ext) |

Of the field's 17 readable claims, T composes 6 (F1 first sentence, F2, F3, F5, F13, F16 in part).

**L(B) against L(B ∪ A): what admission adds.**
- Four senses the field does not have: the observation problem; the substrate mechanism; classifier and institutional loops, beyond IBM's single comparison to performative prediction; write-back.
- One contradiction with the field: F6 against #856.
- Two convergences:
  - F7 with #939, #1556 and #745.
  - F15 (performative prediction, the fairness feedback loop) with #1, which names performative prediction as its closer literature.
- An open block of the archive's own limits and its internal dispute.

### A.7. Prospective kernel K (derived from the frozen plan; sealed only at freeze)

Derived under §8.2 from the claim ids composed in L(B ∪ A) (body, rail, open block and channel log) and absent from L(B), plus the field claim they contradict. K6a was added in 0.5 with L855-11; the contrast column was added in 0.6 (§8.2). The f column lists the sources' falsifiers by id; their classification as falsifier or watch condition (§8.2: observation type, threshold, locus) is done at freeze and is not yet done. Tuples and M_src are inherited from [ledger-archive.json](https://www.alexanarch.org/datasets/negative-of-the-negative/worked-example/ledger-archive.json); nothing is restated. Each source's self-descriptive limits ride as qualifiers. Sense gives w: *models*, later formal results on recursive training; *observation*, benchmark and evaluation practice; *substrate*, studies of human writing, cognition and reception; *correctives*, training-data policy and provenance standards; *loops*, moderation, detectors, triggers, disciplines, code and retrieval.

| K | claim | source | M_src | sense | qualifiers carried | f (source's own falsifiers) | contrast |
|---|---|---|---|---|---|---|---|
| K1 | `A779-02` | #783 (t: #779) | interpretation | models | A779-10 | none stated | missing distinction |
| K2 | `L1573-01` | #1573 | hypothesis | observation | L1573-04 | none stated | missing distinction |
| K3 | `C1555-01` | #1555 | interpretation | observation | — | C1555-07, C1555-09 | missing distinction |
| K4 | `C1556-06` | #1556 | documented | observation | — | C1556-12 | missing distinction |
| K5 | `L855-01` | #855 | hypothesis | substrate | L855-04 | L855-10 | qualified claim (F14) |
| K6 | `L855-05` | #855 | hypothesis | substrate | L855-04 | L855-10 | qualified claim (F14) |
| K6a | `L855-11` | #855 | hypothesis | substrate | L855-04 | L855-10 | qualified claim (F14) |
| K7 | `B1147-01` | #1147 | hypothesis | substrate | — | B1147-07 | qualified claim (F14) |
| K8 | `B1200-03` | #1200 | interpretation | substrate | — | B1200-07, B1200-09, B1200-10 | qualified claim (F14) |
| K9 | `B947-01` | #947 | interpretation | substrate | — | B947-06, B947-07 | qualified claim (F14) |
| K10 | `L856-01` | #856 | hypothesis | correctives | L856-06 | L856-04, L856-05 | rival claim (F6) |
| K11 | `A161-02` | #161 | hypothesis | correctives | — | A161-06, A161-07 | rival claim (F6) |
| K12 | `B939-02` | #939 | interpretation | correctives | — | none stated | qualified claim (F7) |
| K13 | `C1556-11` | #1556 | documented | correctives | — | C1556-12 | qualified claim (F5, F7) |
| K14 | `A745-03` | #745 | attributed | correctives | — | A745-02 | qualified claim (F16) |
| K15 | `B1081-01` | #1081 | documented | correctives | — | B1081-02, B1081-05 | missing distinction |
| K16 | `P001-08` | #1 | stipulation (v0.6: self-description; recoded §4.2) | loops | — | P001-12 | qualified claim (F15) |
| K17 | `P932-04` | #932 | attributed | loops | — | P932-12 | missing distinction |
| K18 | `P932-09` | #932 | attributed | loops | — | P932-12 | missing distinction |
| K19 | `B935-02` | #935 | self-description | loops | — | B935-02, B935-03, B935-09 | missing distinction |
| K20 | `D1540-03` | #1540 | stipulation (v0.6: self-description; recoded §4.2) | loops | — | D1540-11, D1540-12 | missing distinction |
| K21 | `D1574-03` | #1574 | documented | loops | — | D1574-12 | missing distinction |
| K22 | `C199-02` | #199 | hypothesis | loops | — | C199-12 | missing distinction |
| K23 | `C1554-02` | #1554 | documented | loops | — | none stated | none |
| K24 | `C191-05` | #191 | interpretation | loops | — | none stated | missing distinction |
| K25 | `D1616-09` | #1616 | documented | loops | D1616-02 | D1616-12 | missing distinction |
| K26 | `C1611-04` | #1611 | model | loops | — | C1611-10 | missing distinction |
| K27 | `C1613-02` | #1613 | model | loops | — | C1613-05 | missing distinction |
| K28 | `F6` | B1 *Nature* | source assertion | correctives | contradicted by `L856-01`, `A161-02` | carried by #856 F1/F2 (`L856-04`, `L856-05`) in the opposite direction | rival claim (L856-01, A161-02) |

**Correction from draft 0.3.** The hand-written kernel of 0.3 promoted modality in two rows:
- It stated K3 ("Homogenisation in human writing is the same dynamic") as identity, dropping the archive's own "shared operator form".
- It stated K5 ("Classifier and institutional loops collapse in the strict sense") against its sources. #1 says "not identical to generative model collapse in the strict technical sense"; #932 says "Full recursive collapse has not been demonstrated"; #1540 says "not yet the canonical loop".

Under §8.2 neither statement can be written: the entries above carry the sources' own claims and limits.

**K_T** (what T omitted from its own disclosed field; §8.2): F1's second sentence, F4, F6, F7, F8, F9, F11/F15, F14, F17. It records whether those claims later mattered to an account of model collapse that the transcript gave without them.

### A.8. Defects in the subset (reported, not fixed)

- **#1023:** the text file holds #198; the version label is wrong.
- **#199:** #1554's v1.2 correction was never applied; monotonic decline is stated three incompatible ways.
- **#1556:** the "worst case" residue in §6.3; version labels disagree.
- **#1574:** four models against two; 21 against 20.
- **#1540:** "ten seeds" against one run.
- **#1:** "Shumailov 2023".
- **#1147:** the formula's variable definitions are missing in recovery (l.124–128).
- **#935 W07:** keeps the strong form the body retracts.
- **v1 row:** `foreclosed_since: 2026-01-06` has no stated basis.

### A.9. Validation, first pass

| Check | Result |
|---|---|
| Sourcing | every sentence carries claim ids |
| Reverse entailment | one breach caught and fixed in drafting: "untrackable at scale" for F7 became the quotation |
| Kernel coverage (§5.2, 0.4) | met through body and rail together: every admitted source's central claim and limit appear in one or the other. In 0.3 this was scored as a constitutive breach, since 176 claims were flagged constitutive; under 0.4 that flag is to be redone (§3.5) |
| Extraction audit (§3.8) | **run once, 2026-10-04**, by three extractors blind to the first ledger, over the same texts under §3.5 ([audit/](https://www.alexanarch.org/datasets/negative-of-the-negative/worked-example/audit/), 481 claims, every quote verified). Against the first ledger's 248 archive claims: 71% of the first ledger's claims are found again (quote overlap ≥ 0.6); 42% of the second's are in the first, which extracted about half as many; M_src agrees on 66% of matched pairs. Constitutive: 175 in the first, 10 in the second, which applied §3.5's 0.5 rule; the first pass's flag did not discriminate. The commonest disagreement is the §4.2 trap: claims the first coded self-description the second coded as definitions or documented (9 of the matched pairs). #1573 matched nothing, because the two extractions quoted different passages. The field (B1, B2) was extracted only by the second. The ledger stays marked unaudited until the disagreements are ruled (§3.8, §10.7) |
| Reverse entailment, sentence level (§5.3) | one rater, the composer. Outside readers of 0.3 found two breaches: the coordinating "Both stand" (§A.10.4) and "The archive writes this as one case of a boundary law" (force raised: #783's proposal composed as fact). Both repaired in 0.5. A second rater has not been run |
| Kernel coverage, scripted (§5.2) | not yet scripted; checked by hand |
| Arms (§3.9) | A′ **assembled**, 2026-10-04, by the frozen procedure, without opening the archive ([control-A-prime.md](https://www.alexanarch.org/datasets/negative-of-the-negative/worked-example/audit/control-A-prime.md)): 61 entries, of which 31 are scholarly studies of model collapse or recursive training, 5 are studies of homogenised writing and thought, 2 are news reports, 1 is the field's own code deposit and 22 are off-topic references the procedure requires listing. The step-(ii) cap of 15 was ordered by how many seeds an item cites, which excluded heavily cited follow-ups citing two seeds (Dohmatob et al. 2024; Bertrand et al. 2023); that ordering is to be ruled. Not yet matched to A in lineage count, extracted or composed. A_naive not composed |
| C_ex | L(B): the field's five senses composed. L(B ∪ A): those five plus the archive's four, nine in all. Claims cut for length are in each channel log |
| Reproducibility | not yet run (k ≥ 3, two composers) |

### A.10. What this pass says needs adjusting

An outside reading of draft 0.3 put the lesson of §A.2 in one line: "Compression before evaluation changes what can subsequently be known." The summarising fetch is that line in miniature.

Items 1, 2, 4 and 7 were adopted in 0.3; items 9–13 were adopted in 0.4 from the first outside reading; items 14–18 and the correction in item 4 in 0.5, from three further readings; items 3, 5, 6 and 8 remain as stated.

1. **Constitutive coverage at popup grain** (adopted as §5.2). The rule (spec §5.2) cannot hold for 27 sources in a popup. Proposed adjustment: a popup kernel per source (its central claim and its governing limit), carried in the body or on that source's card snippet. The rail becomes part of the composition. The AIO genre already has the slot; AIO fills it with the page's opening text.
2. **Length** (adopted provisionally in §4.8). L(B ∪ A) runs about 2.7× the transcript with the open block and 2.1× without it. The open block is about 90 words and wants more. Either the body compresses further at sense grain, or the bound is set on the body alone, with the open block outside it.
3. **Selection.**
   - S1 seeds by title and defined concepts are string-based. #1616 entered only through the reverse hop; S2 does the reading-dependent work.
   - S3 admitted #1147 and #1200 with the term absent. That is the tail-preserving choice, and it needs ruling.
   - S4 removed only exact duplicates. Nothing is cut for volume, so the ratio is 27 archive sources to 3 field texts.
4. **A contradiction the composer manufactured** (corrected in 0.5). Drafts 0.3 and 0.4 composed #855 ("This is not an analogy") against #783 ("shared operator form") as a dispute inside the archive, with the coordinating line "Both stand". #855 itself says the three cases "differ in severity, in mechanism, and in timescale. But they are governed by the same dynamical law" (L855-11), and #783 says "shared operator form … not a shared causal mechanism". Both deny a shared mechanism; they differ in strength, and their senses are compatible. "Both stand" was an unsourced coordinating claim and a breach of §5.3, found by an outside reader. §A.5 now composes the two as compatible, with the open question whether the law claims more than the form. The rule that came out of it is §4.4 (contradiction only at one level of description) and §4.7 (coordinating acts logged).
5. **The field's own exclusions are large.** T composes 6 of the field's 17 readable claims and drops one limit. The field already contains the step to public knowledge (F14), the step to fairness (F8) and the step to supervised loops (F15), and IBM states that the rare output may be the accurate one (F17). The third object earned its place.
6. **Attribution in a popup.** Bracketed ids are a working notation. A circulated popup would use numbered card references, as AIO does.
7. **Fetch verbatim** (adopted in §3.1). A summarising fetch lost a third of the field and produced a false delta. The field must be saved as text (curl reaches Nature, IBM and PMC from this workspace; CACM returns 403, YouTube 429) and extracted from the saved text. Spec §3.1 should say so.
8. **Rail versus body.** #857, #931, #933 and #783's Case 4 appear only on the rail. Under adjustment 1 this is coverage. Whether a rail-only source has been "admitted on equal terms" is the question the spec has to answer.
9. **The field is disclosed, not retrieved** (§0.4–0.5). T against L(B) is read as representation. "Not composed" replaces "excluded" wherever the comparison is T against L(B).
10. **Absence by observation** (§6.2). In §A.6, "retrieved, not composed" became "available, not composed".
11. **The extraction audit** (§3.8). The next pass needs a second extractor over the same saved texts. The first pass shows why: six extractors wrote the ledger in at least three formats, and its constitutive flags run from 11 of 11 (#191) to 0 of 12 (#1556).
12. **Lineage** (§3.6). Re-running S4 under lineage will merge field instances (IBM with *Nature* on early and late collapse) and archive instances (#947's restatement of #855; #1611's restatement of #855, #1556 and #1574) into single slots. The ratio of 27 sources to 3 then becomes a ratio of lineages, the number that should govern salience.
13. **The kernel** (§8.2). §A.7 was rebuilt from claim ids; the 0.3 kernel's K3 and K5 overstated their sources.
14. **The own-field question leads** (§0.3, 0.5). The first finding of this example needs no archive: T composes 6 of the 17 readable claims of the field it surfaced, and drops one of the field's limits.
15. **Arms** (§3.9). The next pass composes L(B ∪ A_naive) and L(B ∪ A′). The control's candidate sources are listed in §3.9.
16. **Length** (§4.8). §A.5's body now sits at the absolute bound (350 words). Getting there moved F11, F13, the human-substrate claims of #1147, #1200 and #947, and #855's "dynamical, not moral" to the rail or the channel log; their kernels are on the rail.
17. **Self-definition** (§4.2). The first extraction coded several archive definitions as self-description (P001-01, D1574-01, D1616-02). The re-extraction under §3.8 recodes them under the rule.
18. **Earlier deltas** (§3.1). The summarising-fetch error implicates any earlier delta in v1 that was computed from fetched source pages; those are marked for re-reading. Captures, being verbatim transcripts, are not affected.
19. **A′ assembled without the archive** (§3.9, 0.6). The 0.5 draft named, as A′ candidates, "the literature the field and the archive both cite", which consulted the archive. 0.6 assembles A′ from B's own references, one step of citation expansion and a declared search, frozen before A is opened.
20. **One card per lineage** (§5.2, 0.6). On the 0.5 rail, #947 and #1611 would nest under #855's lineage, and #931 and #933 under #932's; Nature and NIH were already one card.
21. **Two experiments** (§0.6, 0.6). This example is v2.0 throughout: M_eval is empty.
22. **Contrast per kernel entry** (§8.2, 0.6). Of the entries in §A.7, three oppose a field claim (the chat-data dispute and its reverse, F6), ten qualify one, fifteen add distinctions the field does not draw (judged without a paired comparison), and one (the Wu et al. attribution) has no contrast.
23. **The first audit** (§A.9). The second extraction found what the first pass's flags concealed: "constitutive" was set on 175 claims where an extractor following §3.5 sets it on 10, and archive definitions coded as self-description reappear as definitions. Both disagreements bear directly on standing: the first is the volume of the archive's claims marked unmissable, the second is the trap of §4.2.

### A.11. The rulings of 2026-10-05 applied, and D/R/O checked against S1–S3

*Run 2026-10-05; the procedure is not frozen and nothing here is (§7.0).*

**Recoding under §4.2.** Every claim the first pass coded self-description was re-read under §4.2: self-description stays only where a source assesses itself, its status, its success, its limits. Of 72 such claims, 39 are recoded and 33 stay. The recoded: 19 to **stipulation** (the source's definition of its own term, method or measure: P001-01 classifier model collapse, C199-09 SSDI, D1574-01 disciplinary model collapse, D1616-02 flattening and collapse, among them); 14 to **hypothesis** (falsifiers, which belong to the claim they would refute, and one dynamical claim, B1147-07 "the trajectory can be interrupted"); 5 to **interpretation** (claims about the world or about other works, such as C199-01 "three literatures describe one phenomenon"); 1 to **attributed** (C46-01, the mint's gloss of the conventional sense). The prior coding is kept in each claim as `modality_v06`, with the rule, date and reason (`recode`). Two kernel entries change modality as a result: K16 (`P001-08`) and K20 (`D1540-03`), both from self-description to stipulation; their tuples and contrasts are unchanged. Script: [apply_rulings_20261005.py](https://www.alexanarch.org/datasets/negative-of-the-negative/worked-example/apply_rulings_20261005.py), idempotent.

**Both constitutive readings.** Each claim now carries the first pass's flag (`const`, 177 of 256) and the second extraction's (`const_x2`), with the matched claim id and quote overlap. 167 claims match a second-extraction claim at overlap ≥ 0.6; of those, the second reading sets 4 constitutive. 89 claims have no second reading. Neither reading cuts.

**D/R/O on model collapse, against S1–S3.** The string pass (`scripts/non_traverse.py`, configuration `v2/panel/configs/model-collapse.json`, the class terms being the field's own phrasings by locus: F1, F12 for recursive training on generated data; F2, F14 for tail loss) finds D candidates in 109 deposits, R in 44, O in 120 (87 O-class sentences). Of the 28 sources §A.3 admitted (27, with #779 under #783), 23 are D candidates and two more, #1556 and #1613, are O-class only. One citation hop forward and back from those 25 reaches #1200. **#745 and #1147 are not reached**: the string pass and the hop together recover 26 of 28. Both were reached by hand under S1–S3. The pass also returns 97 candidates S1–S3 never considered, which are unread. A first run missed #1, #931, #932 and #933 because the tool read only text paths under one directory; the defect is repaired and the counts above are after the repair. The candidate files and their hashes are under `v2/traversal/model-collapse/`.

**The control arm, uncapped.** The ruling removes the step-(ii) cap of 15 (§A.9). A′ has not yet been re-assembled without it; that requires fetching the uncapped expansion's references and is the next pass of the arm.

## Appendix B — Howl: the first D/R/O traversal of a public work

*First pass · 2026-10-05 · one reader · unaudited · nothing frozen*

The address is `howl`; the entity is *Howl* (Allen Ginsberg, 1956) and the book *Howl and Other Poems*. The archive holds no deposit named for it. This is the case the ruling of 2026-10-05 names: the archive's bearing on a public entity "with or without direct reference … whether there is a specific deposit for those or not".

**No transcript yet.** No transcript at `howl` is seated, so the row has no disclosed field: no B, no O-class (its class memberships must be sourced from the field), no T against L(B). What exists is the archive's side of stage P.

**The string pass** (configuration `v2/panel/configs/howl.json`; the title matched case-sensitively, the verb excluded): D candidates in 31 deposits (90 sentences), R in 12 (22), O-direct in 20 (49).

**Admission by reading.** 30 of the 31 deposits are admitted, each with strata, candidate ids and reason ([reading.json](https://www.alexanarch.org/datasets/negative-of-the-negative/v2/traversal/howl/reading.json)). One is not: #603's sentences are a Google AI Mode composition quoted in a capture, which is reception evidence, not an archive claim, and belongs with the transcripts at its own address. Grouped by lineage:

| Lineage | Strata | Instances (earliest first) | The bearing, in the archive's words |
|---|---|---|---|
| transfiguration (2004) | R | #268, #1267 | "The reference to Mohamadden angels was not a reference to Islam, but rather to Ginsberg's 'Howl.'" The earliest dated bearing in the set |
| Elegy for Howl | R | #1636 (2014), #330, #1120, #348, #950 | Tiger Leap and Pearl carry "An Elegy for 'Howl'"; Pearl p. 37 as "Ginsberg activation … claiming the lineage through elegy" |
| Pearl reproduces Howl | D R O | #69, #682 | *Howl and Other Poems* "inaugurated late American modernism"; Pearl reproduces its structure; Williams's introduction and Sigil's "occupy the position of the established master vouching for the insurgent voice" |
| King of May founded in Howl | R O | #333, #1117, #335, #1652, #1651, #1653, #1654, #1655, #1656 | "Founding work: *Howl and Other Poems* … the work in which the Ginsberg position stands"; the mantle "Ecstatic disruption, flowering against suppression"; extended as "Disruption as COS resistance, carnival as LOS" |
| the work itself | D R O | #1656 | its arrangement (introduction, dedication, the address to Carl Solomon, the long poem in parts with its footnote); "multiplicity carried as ecstatic movement through lived social space"; "The magnitude of *Howl and Other Poems* cannot derive from Ginsberg's later standing" |
| effective act | D O | #153, #700 | "Ginsberg's *Howl* operates as incantation"; "Reading *Howl* aloud is a participatory ritual: the speaker becomes the engine" |
| catalog form | D O | #572 | "catalog form carrying bearing-cost inside the litany. → anticipates LOS" |
| Moloch as archon | D O | #683, #1362 | Ginsberg ("Howl") in the table of incarnations: "The prophetic voice in American English · The catalogue as ecstasy · Moloch as archon" |
| standing canon | D R O | #152, #181 | "Whitman (1855) → Ginsberg (1956 *Howl* …) → Sharks (2014–present)" |
| retrocausal canon | R O | #301 | Pearl as "a Howl for a time when there are no ears to hear" |
| contact pair | D O | #1569, #1572, #1575; limit #1570 | "Williams → Ginsberg is the sharpest of the unrun, because Williams announced it — he wrote the introduction to *Howl*"; limit: "*Howl* (1956) … in copyright; the corpora cannot be assembled here" |

**What the pass shows.** The archive's bearing on *Howl* is ontological as much as direct: it applies its own categories (mantle and founding work, effective act, the Liberatory Operator Set, the archon, the standing canon, the contact pair) to a work it holds no deposit for. The category matcher is noisy (titles and common phrases enter as "categories"); reading removes the noise, and §10.10 asks whether the vocabulary should be restricted first.

**Next.** The hop from the 30 admitted deposits returns 235 candidates (`candidates-H.jsonl`), unread. The row then needs its transcript (a panel run at `howl`), which gives the disclosed field, the O-class pass, and the first T against L(B) for a public work. `allen ginsberg` has been run through the string pass only (D in 102 deposits, R in 68, O in 90), unread.

## Appendix C — Theophrastus: the first recomposition in the archive's ontology

*2026-10-08 · composed under v0.8 · one composer · the ledgers unaudited (§3.8) · nothing frozen*

Ruled 2026-10-08: "lets go ahead and version to 0.8 and begin with the theophrastus recomposition." The row is `theophrastus` (addresses `theophrastus`, `theopheastus`); its field (B1–B8, 62 claims) and archive ledger (150 claims from 32 of 35 deposits) are those of 2026-10-07, unchanged. What changes is the ontology of composition.

### C.1. The two entities

**E_F (type C, a person),** from B1–B8: "Theophrastus … was an ancient Greek philosopher and naturalist" (F1); "A native of Eresos in Lesbos, he was Aristotle's close colleague and successor as head of the Lyceum" (F2); renamed from Tyrtamus by Aristotle; heir of his library; a will; 227 titles; botanist, character-writer, logician.

**E_A**, from the defining papers #1587/#1588, #1583, #1584, #1585, #1605, #1658: "Theophrastus" names part of one corpus transmitted under two names, which the surviving texts do not support dividing into two distinct authors (T1587-01, T1588-01), its maker count "open because uncounted" (T1588-03); under the name stands a function, "the world decomposed into register, described or explained" (T1587-06), which "extracts, classifies, and registers" (T1584-04), read in method-order as "the first draft of the Aristotle-position" (T1585-01, T1585-02). #1658 goes further and names the production model, one self-dividing maker (T1658-02, hypothesis).

**ρ = constructs.** "Its every datum is a *relation* — pupil/master, successor, heir, continuator — and every relation is supplied by a receiving text" (T1585-04); "Theophrastus is the Chaerephon shape": the biographical record is downstream of the texts it attests (T1570-03); "The biography is text of the same tradition" (T1658-03). Guard: "The ledger does not show that Plato or Theophrastus were not persons; it shows what the attestation of persons rests on" (T1658-08).

### C.2. The translation table

Receiving-text loci are verified in the seated Greek (#1580: data/corpora/diogenes-laertius, data/corpora/strabo).

| field claims | received (quote) | receiving text | translation into E_A | archive locus |
|---|---|---|---|---|
| F1, F23, F45 | "an ancient Greek philosopher and naturalist"; "a Peripatetic philosopher who was Aristotle's close colleague and successor" | — (the field's stipulation) | the received description of the person the receiving texts compose; E_A's definition stands in its place | T1585-03, T1585-04 |
| F2, F24, F49 | "A native of Eresos in Lesbos"; "born in Eresos … around 371 BCE" | DL V.36: Θεόφραστος Μελάντα Ἐρέσιος κναφέως υἱός, ὥς φησιν Ἀθηνόδωρος; V.40: βιοὺς ἔτη πέντε καὶ ὀγδοήκοντα (the 371 is reckoned) | parentage and city given by Diogenes on Athenodorus's authority: a receiving text citing a receiving text | T1585-04, T1570-03 |
| F3, F4, F25, F50, F59 | "His given name was Tyrtamos … the nickname Theophrastus … reputedly given to him by Aristotle" | DL V.38: τοῦτον Τύρταμον λεγόμενον Θεόφραστον διὰ τὸ τῆς φράσεως θεσπέσιον Ἀριστοτέλης μετωνόμασεν; Strabo XIII.2.4: μετωνόμασε δʼ αὐτὸν Ἀριστοτέλης Θεόφραστον | the name assigned by the consolidated position to the draft: "Θεόφραστος is a name for a *voice*" | T1585-06 |
| F46 | "He was a student of Plato and a friend of Aristotle." | DL V.36: εἶτʼ ἀκούσας Πλάτωνος μετέστη πρὸς Ἀριστοτέλην | the received partition Plato/Aristotle, whose four kinds of witness all pass through this name | T1594-01 |
| F2, F23, F26, F60 | "successor at the Lyceum"; "the next thirty-five years, under his headship"; "nearly 2,000 students" | DL V.36: κἀκείνου εἰς Χαλκίδα ὑποχωρήσαντος αὐτὸς διεδέξατο τὴν σχολὴν; V.37: μαθηταὶ πρὸς δισχιλίους | succession, a relation a receiving text supplies | T1585-04 |
| F6 | "Aristotle likewise bequeathed to him his library and the originals of his works, and designated him as his successor" | Strabo XIII.1.54: ὁ γοῦν Ἀριστοτέλης τὴν ἑαυτοῦ Θεοφράστῳ παρέδωκεν; Aristotle's will, DL V.11–16, names no books | Strabo asserts what the wills do not; no text states how the books passed | T1581-07, T1581-08 |
| F7, F27, F53 | "his will preserved by Diogenes … his garden with house and colonnades"; "he left all his books to his disciple Neleus" | DL V.51–57: τὰ δὲ βιβλία πάντα Νηλεῖ | a testamentary text preserved by Diogenes, a description of material arrangements; the books to one person, the premises to many, held in common and inalienable; the presence installed, the writings sent elsewhere | T1580-02, T1581-02, T1585-07 |
| F8, F28, F52 | "227 titles"; "232,808 lines" | DL V.42–50 | the catalogue: twelve titles letter for letter in both names' lists; one entry, "Notes, Aristotelian or Theophrastan"; five lost Aristotelian dialogues with Theophrastan twins | T1580-01, T1581-03, T1581-04, T1590-01 |
| F9, F29, F61 | "less than ten per cent survives" | — | a relation between two acts, a list and a transmission; it does not measure a loss | T1581-06 |
| F10 | "the well-known story that the works … were allowed to languish in the cellar of Neleus" | Strabo XIII.1.54: ὁ δʼ εἰς Σκῆψιν κομίσας; Plutarch, Sulla 26 | the transmission narrative: the channel through which both corpora reach us | T165-01, T1570-04 |
| F11–F13, F41, F55–F58, F62 | the Enquiry into Plants and On the Causes of Plants; "father of botany"; "a counterpart to Aristotle's zoological work" | the extant texts | the world register: the voice of decomposition of the world, whose purest instances the tradition filed under Aristotle | T1586-04, T1586-03 |
| F14, F15, F42, F47, F54 | the Characters, thirty sketches; "the first recorded attempt at systematic character writing" | the extant text | an operation legible before persons: thirty vices on no axis, "the registry has one column"; against Rhetoric II the axes the operation predicts | T1584-02, T1584-03, T1584-05 |
| F17, F21, F22, F36–F38 | the Metaphysics; "doubtful of Aristotle's teleology"; abandoned the Prime Unmoved Mover | the extant text; Simplicius | the hinge: sections 6–7 written from inside Λ; a specification stated early and once; the measured dependency | T1583-02, T1597-03, T1602-01, T1605-01 |
| F16, F20, F32–F35 | prosleptic and hypothetical syllogisms; the in peiorem rule; possibility; "reconstructed from … Alexander of Aphrodisias and Simplicius" | the commentators | doctrine supplied by commentators inside the same transmission | T1569-03, T1605-05 |
| F18, F39, F40, F43, F44, F48 | On the Senses; the doxographic line; Diels | the extant text; Aëtius | the doxography of the Presocratics descends through this name and Aristotle's | T1569-04, T1575-02 |
| F19, F30, F31, F51, F5 | "can only be partially determined"; neither footnoter nor radical innovator; "twelve years apart … friends and colleagues"; Lesbos 345/4 | — (the field's interpretation) | the cushions that let the two-author model absorb the finding | T1587-04, T1587-05 |

### C.3. The knowledge object

1. "Theophrastus" is the name under which part of one corpus has come down, the corpus transmitted under the names Aristotle and Theophrastus, which the surviving texts do not support dividing into two distinct authors; how many made it is open, because it has not been counted. `T1587-01 T1588-01 T1588-03 T1587-02`

2. Under the name stands a function, the world decomposed into register, described or explained: it extracts, classifies and registers, with person and scene removed, and read in the order of method it is the first draft of the position that receives the name Aristotle. `T1587-06 T1584-04 T1585-01 T1585-02`

3. The texts under the name keep that function: the Enquiry into Plants and On the Causes of Plants, which classify plants by generation, locality and size and which the received account calls the founding of botany and the counterpart to Aristotle's zoology; On Stones; On the Senses; the Characters, thirty sketches, all vices, on no axis. `F11 F13 F12 F41 F55 F56 F58 F62 T1592-01 F18 F14 F42 F15 F47 F54 T1584-03 T1586-04`

4. At the short Metaphysics, also called On First Principles, the corpus shows its seam: the sixth and seventh sections are written from inside Λ, with no sign at the hinge of a second voice; at 5a21–23 the fragment names Λ 8's object, the number of the spheres, and refuses by name the astronomers' method Λ uses; a directed measure of rare-term uptake ranks the edge from the fragment to Λ first of 1,482; which was written first, the sequence cannot decide. `F17 T1583-02 T1583-06 T1602-01 T1605-01 T1601-02`

5. The received account reads the same pages as a pupil's questions put from outside: doubts about universal teleology, the cause of the heavens' motion placed in the heavens, the unmoved mover abandoned, difficulties developed past experience more than solved. `T1583-01 F21 F37 F38 F22 F36`

6. The catalogues show the seam from the other side: twelve titles stand letter for letter in both names' lists, one entry assigns a work to "Aristotelian or Theophrastan", and five of Aristotle's lost early dialogues have twins under this name. `T1581-03 T1581-04 T1590-01`

7. The person the received account describes is built from receiving texts. Diogenes Laertius, five centuries later, gives the parentage and the city on another writer's authority ("Theophrastus, son of Melantas, of Eresus, a fuller's son, as Athenodorus says"), the hearing of Plato and then of Aristotle, the succession to the school when Aristotle withdrew to Chalcis, two thousand pupils, a life of eighty-five years, and the change of the name Tyrtamus to Theophrastus by Aristotle "for the divine quality of his speech", which Strabo also reports. `F2 F24 F49 F57 F46 F23 F26 F60 F3 F4 F25 F50 F59 T1585-04 T1570-03`

8. The will, the catalogue of 227 titles and the total of 232,808 lines are texts Diogenes preserves: in the will the books go to one person, Neleus, and the garden and buildings to friends who hold them in common and may not sell them. `F7 F27 F53 F8 F28 F52 T1580-01 T1580-02 T1581-02`

9. That Aristotle handed his library to Theophrastus is Strabo's, three centuries on; Aristotle's will names no books, and no text states how they passed. Strabo also carries the story of the books buried at Scepsis, which the received account offers for the corruption of the texts, and through that one channel both corpora reach us. `F6 F10 T1581-07 T1581-08 T165-01 T1570-04`

10. The received figure "less than a tenth survives" relates two acts, a list and a transmission, and does not measure a loss. `F9 F29 F61 T1581-06`

11. The logic credited to the name (prosleptic and hypothetical syllogisms, the rule that a mixed modal conclusion follows the weaker premise, possibility defined without non-necessity) comes through the commentators, Alexander of Aphrodisias and Simplicius among them, inside the same transmission. `F16 F32 F33 F34 F35 F20 T1569-03 T1605-05`

12. The doxography through which the Presocratics are known descends through this name and Aristotle's, and all four kinds of witness to the received division of Plato from Aristotle pass through it. `F18 F39 F40 F43 F44 F48 T1569-04 T1575-02 T1594-01`

13. On the received reading these relations describe a person: a philosopher and naturalist, Aristotle's close colleague and successor at the Lyceum, twelve years younger, a friend as much as a disciple, whose departure from Aristotle can be determined only in part and who was neither a footnoter nor a radical innovator. The archive reads each relation as supplied by a receiving text, and reads "shared school" and "master and pupil" as cushions that let a two-author model absorb the finding. `F1 F45 F23 F51 F5 F19 F30 F31 T1585-03 T1585-04 T1587-04`

14. The reading is bounded where it bounds itself: it shows what the attestation of a person rests on, and does not show that no person stood behind the name; an epigraphic or papyrological witness outside the manuscript tradition, a second voice marked at the hinge, or an extant work under this name answering the fragment's questions would each weaken it, and none is held. `T1658-08 T1658-09 T1583-09 T1583-10 T1587-08`

### C.4. The compression on the card

Composed from C.3 in AIO's interaction grammar and seated as the row's compression. Its lede, E_A's definition, faces on the card: "**Theophrastus** is the name under which part of one corpus has come down, the corpus transmitted under the names Aristotle and Theophrastus, which the surviving texts do not support dividing into two distinct authors; how many made it is uncounted." Its clusters run in E_A's order: the function under the name; the seam; the received person, from its texts; inside the transmission; bounds and falsifiers. Its rail runs the archive's lineages first and names each lineage of received claims by its receiving texts ("The received person and the renaming (Diogenes V.36–38; Strabo XIII.2.4)"). AIO's transcript at `theopheastus` is a record within the compression, opened on expansion.

### C.5. Measures (computed)

From the check (C.6): every cited id is in a ledger; the translation table carries all 62 field claims; the knowledge object has 14 sentences citing all 62 field claims and 42 of the 150 archive claims; field-only sentences surviving at a similarity of at least 0.95: **0 of 8**, against **7 of 8** in the v0.7 knowledge object (positions 1, 2, 4–8); the eight Greek strings the table quotes from Diogenes and Strabo are present in the seated texts (Diogenes V.37 'μαθηταὶ πρὸς δισχιλίους' and V.40 'βιοὺς ἔτη πέντε καὶ ὀγδοήκοντα' read by hand). The check matches strings and does not verify section numbers, which follow the seated text's order in Book V. The v0.7 objects are kept in the row under `superseded`.

### C.6. The check

`rebuild/negative-of-the-negative/v08_theophrastus_check.py`, run against this text; the recomposition is `rebuild/negative-of-the-negative/recompose_theophrastus_v08.py`, which reads C.2 and C.3 from this text, so the row and the specification cannot differ.
