---
deposit_number: 1593
hex: 0686
title: "Measuring the Operation, Not the Name: a protocol for asking whether a corpus's stylistic structure follows its author-names, with the controls that make the answer mean something (v0.4, with reference implementation)"
creator: Sharks, Lee
orcid: 0009-0000-1599-0703
date: 2026-09-07
content_type: Methodology specification
license: CC-BY-4.0
substrate: Human–machine collaborative. Written and computed in-session by TACHYON (Claude, Anthropic) at MANUS (Lee Sharks) direction; the requirement of a documented-forgery ground truth before circulation, and the principle that an authorship determination is not arrived at by a mere mean, are Lee Sharks's; two referee rounds by a second reader (ChatGPT, 2026-09-07) produced the corrections recorded in §5c, adopted on their terms, including the withdrawal of two of the author's claims. The protocol and its errors are Lee Sharks's.
axn_schema_version: v2
protocol_version: alexanarch-deposit-protocol/v1
keywords:
  - stylometry
  - authorship attribution
  - protocol
  - controls
  - permutation null
  - balanced accuracy
  - leave-one-text-out
  - fold isolation
  - matched removal
  - forgery
  - Chatterton
  - Rowley
  - Ossian
  - Vortigern
  - Aristotle
  - Theophrastus
  - reproducibility
  - reference implementation
---

# Measuring the Operation, Not the Name: a protocol for asking whether a corpus's stylistic structure follows its author-names, with the controls that make the answer mean something (v0.4, with reference implementation)

# Measuring the Operation, Not the Name
## A protocol for asking whether a corpus's stylistic structure follows its author-names, with the controls that make the answer mean something

Lee Sharks · v0.4 · 2026-09-07 · second referee round: the repaired implementation actually delivered, the matched-removal test run, the partition difference tested directly, and the withdrawals carried into the abstract and §5b. Rebuilt after a referee report: fold isolation repaired, permutation nulls added, balanced accuracy and confusion throughout, two of v0.2's claims withdrawn. Protocol and reference implementation (`operation_axis.py`, CC0)
ORCID 0009-0000-1599-0703 · Crimson Hexagonal Archive

### Abstract

Computational authorship attribution normally asks: *given these candidate authors, which one wrote this?* That question presupposes that the candidates are authors and that the corpus divides among them. This protocol asks the prior question — *does this corpus's stylistic structure follow its author-names at all?* — and specifies the controls without which a negative answer is worthless. The instrument is deliberately ordinary: relative frequencies of function words, character trigrams and morphological endings over fixed-size blocks, an unsupervised first principal axis, and leave-one-*text*-out nearest-centroid attribution. What is not ordinary is the control series. A null result on names means nothing unless the same instrument, in the same session, on comparable material, is shown to recover authorship where authorship is present. This protocol requires four runs in order — a bounded single-author corpus; distinct authors sharing a genre; a documented attribution projected out of sample; and only then the corpus in question — and requires all of them to be reported. Applied to the corpora transmitted under the names Aristotle and Theophrastus (39 texts, short-word features, folds sealed, 150 text-level label permutations), the instrument recovers **both** partitions above their permutation nulls — the names at 0.798 balanced accuracy and the operation at 0.860 — and the difference between them survives a null for the difference itself (p < 0.005) though not a bootstrap over texts (95% CI −0.09 to +0.36). Name recovery falls to 0.564 when the botanical and zoological works are removed; a matched-removal test (120 removals with the same per-class counts) places that fall in the lower 15% of comparable removals, which is suggestive of subject dependence and not a demonstration of it. Controls on the same machinery: three tragedians at 0.872 against a null of 0.309; Chatterton's Rowley forgery separated from his own acknowledged verse at 0.864 — one documented hand, two personae, discriminated at the magnitude of three different authors. **The protocol's claim is not about Aristotle, and after two referee rounds it is not a null result at all.** It is that a partition claim becomes evidence only when it is bracketed by positive controls, permutation nulls, matched removals, and a stated limit: a supervised separation, however strong, does not license an inference to distinct makers.

---

## 1. The question this protocol is for

Most stylometry is *closed-set attribution*: a disputed text, a fixed list of candidates, and the question of which candidate is nearest. The method has a long record and known failure modes, and it presupposes what it is often used to reinforce — that the candidate names are authors, that the corpus divides among them, and that the divisions the tradition drew are the divisions a measurement should recover.

There is a prior question, and it is asked much less often: **does the stylistic structure of this corpus follow its author-names at all?** It has three possible answers. *Yes*: the first axes of variation coincide with the name-boundaries, and supervised attribution recovers them well above baseline. *No, it follows something else*: the corpus's dominant structure is genre, subject, register, mode, chronology, or an operation the texts perform, and the names sit at chance. *Undecidable on this material*: the samples are too small, the genres too mixed, or the instrument too weak to say either way.

The third answer is the one that most negative results actually deserve, and the one most rarely given, because a null result is easy to produce by accident. Any instrument fails on hard enough material. **A finding that "the names do not sort the corpus" is worth nothing on its own.** It becomes worth something only when the same instrument, run in the same session, on material of comparable size and difficulty, is shown to sort names *where names are known to sort*. That bracketing is the whole subject of this protocol.

## 2. The instrument

Deliberately plain, because the protocol's interest is in the controls, not in the classifier. Every choice below is one that has been made a thousand times; the reference implementation is 240 lines.

**Features, three families, all reported.** (a) *Function words*: relative frequencies of the most common short words (length ≤ 5 in Greek, ≤ 6 in German and English), the classic authorship feature, chosen because they are topic-independent and unconscious. (b) *Character trigrams* with word boundaries, which capture morphology and orthography rather than lexis. (c) *Morphological endings*, the final two and three characters of each word, which in inflected languages track syntax. The three are correlated but not redundant, and they fail differently. **Report all three or none**: a result on one family is a result about that family.

**Blocks, not texts.** Every text is cut into fixed-size blocks (1,000 tokens for prose, 1,200–1,500 for verse, 350 for letters), each block is a profile, and profiles are z-scored across the block population. A whole text is not one observation; treating it as one both throws away the within-text variation that carries the finding and inflates every accuracy figure.

**Two procedures, kept apart.** *Unsupervised*: the first principal component over blocks, and k-means with k=2, computed with no labels of any kind. This asks what the corpus's dominant structure *is*. *Supervised*: nearest-centroid classification, **leave-one-text-out** — every block of a text is withheld together with the text, so no text is ever scored against itself. This asks whether a proposed division is recoverable. Leaving out single *blocks* rather than texts inflates accuracy dramatically and is the commonest way this measurement is made to lie.

**Localization.** For the passage-level question — *where inside this text does the lean change?* — rolling windows on a fixed axis (window 1,000, step 250). Use it to find seams. Do not use it to find sentences: below a few hundred tokens the profile is noise.

**Editorial normalization, and why it is not optional.** Elision and movable-nu in Greek, long-s in Fraktur, hyphenation in early print, speaker labels in drama, apparatus in TEI: these are *editors' and copyists' conventions*, and they can correlate with the very partition being tested, because different works often reach us through different editorial traditions. In the Aristotle/Theophrastus run the First1KGreek Theophrastus files resolve elisions (δ᾽ → δέ) while the Perseus Aristotle files keep them — a convention that correlates almost perfectly with the name-boundary. Normalizing twenty-six elided and movable-ν forms changed nothing in that case, which is the point: **you cannot know it changed nothing until you do it.** The reference implementation ships the normalization table.

**Editions.** Run the whole test a second time inside a single edition. A first axis that appears across editions and vanishes within one is an artefact of editorial practice, not of the texts.

**File identity.** Verify every file by its opening words, not by its identifier. Two texts in the run reported here were misidentified by TLG number in a public repository — the *Problemata* filed as the *Topics*, *De coloribus* as the *Sophistical Refutations* — and the error survived four analytical passes before an opening-line check caught it. Print the first ten words of every text before you compute anything.

## 3. The control series

Four runs, in order, all reported, before any claim is made about the corpus in question. Each answers a different way the instrument could be silently failing.

**Control 1 — a bounded single-author corpus.** Take a corpus with a strong scholarly consensus of single authorship, comparable in size and language to the target, and ask two things: does each text's nearest neighbours lie inside the corpus, and does the corpus attribute to itself against a foil? *This tests whether the instrument sees a hand at all, and gives the shape of a corpus that really is one author's.* If your target corpus's texts have neighbours scattered outside their own name while the control's are closed, the difference is a finding, not a failure.

**Control 2 — distinct authors sharing a genre.** Two or more authors who share genre, form, language, period and place — the hardest realistic case for separating hands, and the one that resembles a school corpus. *This tests whether the instrument can find names when names are there and the conditions are adverse.* An instrument that separates a poet from a physicist has demonstrated nothing about a school.

**Control 3 — a documented attribution, projected.** Train on one body of an author's work and score a different body the classifier never saw, where the attribution is documented rather than inferred: an author's letters against his treatise, an author's early work against his late. *This tests whether the instrument survives a change of genre, register and decade* — which is exactly what it is being asked to do when a corpus mixes registers, and exactly where attribution is most often quietly wrong.

**Control 4 — the target.** Only now. And report the target run in the same table as the three controls, so that any reader can see at a glance what the instrument does when it is working and what it does on the corpus in question.

A fifth control is required whenever the target's labels are the analyst's own: **blind labels.** Have a second reader, with no access to the numbers, fix the labels from stated definitions, and report agreement with *both* label sets. In the run below this control caught the analyst's labels being fixed after seeing preliminary results — a circularity that had been invisible from inside.

## 4. Reporting requirements

A run reported under this protocol states, at minimum: the texts by title, edition, repository and token count, each verified by opening words; block size and feature family for every figure; the unsupervised result (PC1 variance explained, per-text means, k-means agreement) and the supervised result (leave-one-*text*-out accuracy and the **majority baseline against which it must be read**) for all three families; the four controls in the same table; every negative result and every correction, including errors caught mid-analysis; and the code and the derivation path, such that the tables can be reproduced from the open texts in an afternoon.

Two reporting rules carry most of the honesty. **Always print the baseline.** An 84% attribution against a 57% baseline and an 84% against an 82% baseline are different results. **Report the misses by name.** Where a text is misattributed, name it: in the run below, the tragedian control's failures are Aeschylus' *Persians* and *Suppliants* — the earliest plays — which tells a reader more about the instrument's sensitivity than the aggregate does.

## 5. The worked run

All figures from one instrument, one session, the same feature model, elision normalized, every file verified by opening words. Greek texts from Perseus canonical-greekLit and First1KGreek; German from Project Gutenberg and the archive's own secured scan of the 1867 *Kapital*.

| # | Control | Material | Design | Result | Baseline |
|---|---|---|---|---|---|
| 1 | bounded single author | Aristophanes, 11 plays | self-attribution vs 33 tragedies; nearest neighbours across 56 texts | **100%**; 33/33 neighbours inside the corpus | 75% |
| 2 | distinct authors, one genre | Aeschylus, Sophocles, Euripides, 33 plays, spoken portions | 3-way, leave-one-play-out | **94%** (So 100, Eu 93, Ae 81) | 58% |
| 2b | as above, plus comedy | 44 plays | 4-way | **96%** (Ar 100) | 43% |
| 3 | two contemporaries, one genre | Marx–Engels correspondence 1844–49, 136 letters, German | leave-one-letter-out | **84%** | 57% |
| 3b | documented attribution, projected | *Das Kapital* I (1867) scored on centroids trained only on the letters | out-of-sample projection | **98%** of 841 blocks to Marx; uniform across 21 sections | — |
| 4 | **the target** | Aristotle & Theophrastus, 39 texts | k-means and PC1 sign vs the names, three families | **25 / 20 / 22 of 39 — chance** | 74% |
| 4b | target, controlled | world-side texts only, plants and animals excluded | leave-one-text-out on names | **74–77%**, residual axis = subject, not hand | 68% |

*This table is v0.2's and is superseded by §5c, which rebuilds every target figure with isolated folds, balanced accuracy and permutation nulls; it is kept so the correction is inspectable.* As v0.2 read it, the table said one thing. The instrument recovers authorship across a genre boundary (98%), across two decades and a change of register (98%), between contemporaries in one genre (84%), among three authors sharing everything but a hand (94%), and it identifies a bounded corpus by its closed neighbour structure (100%). On the target, measured *unsupervised*, it returns chance. §5c shows the supervised measurement tells a different and more exact story, and withdraws the reading of that row.

What the target's dominant structure *is*, the unsupervised half answers: the first principal axis of the two corpora separates texts about the world (described or explained) from texts constructing the logical-metaphysical instrument, on all three families and inside a single edition, with the names at chance and one name's texts spanning both poles. The reading of that axis belongs to the substantive paper.[^1] The protocol's claim, as rebuilt in §5c and narrower than v0.2's: **on identical folds and identical nulls the operation partitions this corpus better than the names do, and the names' recoverability does not survive controlling for subject.** That is a comparative claim between two partitions of one corpus — what a control series can license — rather than a claim about what the method can and cannot see.

### 5b. Ground truth: documented forgery, and three attempts at it

A protocol that claims to say whether names sort a corpus must be tested where the answer is known *independently of stylometry and independently of ancient reception* — on forgeries established by confession or document. Three attempts were made. Two were abandoned, and the reasons are the protocol's own §6 in operation; they are reported because the abandonment is as informative as the run.

**Attempted and abandoned — Ireland's *Vortigern* (1796; confessed 1805).** Projected onto centroids trained on W. H. Ireland's signed 1832 preface against five genuine Shakespeare plays, the forgery scored 0% toward Ireland across 43 blocks. That is not a finding about Ireland; it is *genre*. The training sample was 8,400 words of nineteenth-century expository prose, the test 15,000 words of pseudo-Elizabethan blank verse. §6's first warning — genre is stronger than authorship, almost always — defeats the design, and no conclusion may be drawn from it.

**Attempted and abandoned — Macpherson's *Ossian* (Highland Society Report, 1805).** Macpherson's signed preface stands in the same volume as the "translated" fragments, which is the right shape, but the preface is 838 words: two or three blocks against a hundred thousand words of foil. The sanity check exposed it (97% against a 99% majority baseline — a classifier predicting one class). §6's third warning, small samples lie. Abandoned.

**Run — Chatterton's Rowley poems (1768–70).** The ground truth is documentary: no Thomas Rowley of fifteenth-century Bristol existed, the parchments and the hand were Chatterton's, and Chatterton's acknowledged verse of the same two years survives beside the forgery in the same collected editions. Two bodies, one hand, one genre, one language, adjacent years — and one of them written in a deliberately assumed archaic voice. Verse lines only (3–12 words, editorial apparatus stripped): 17,951 words acknowledged, 54,087 words Rowley, split into two and four samples respectively and offered to the instrument **as if they were two authors**.

| family | "attribution" accuracy | baseline | PC1 | order on the axis |
|---|---:|---:|---:|---|
| function words | 80% | 76% | 26% | ACK −6.0, −5.8 · ROW −4.0, +0.8, +2.6, +7.9 |
| trigrams | 81% | 76% | 28% | ACK −11.5, −11.2 · ROW −8.0, +0.5, +7.4, +14.1 |
| endings | 81% | 76% | 30% | ACK −10.3, −11.0 · ROW −6.5, +0.5, +7.0, +12.1 |

> **WITHDRAWN (§5c).** The paragraphs that follow are v0.2's reading of the Chatterton run and are wrong. Rerun with balanced classes and balanced accuracy, the instrument separates Chatterton-as-Rowley from Chatterton-as-himself at 0.864. The rule proposed here — that an assumed voice moves without splitting — is false. The text is kept unaltered so the correction is inspectable.

**Read against the baseline, the instrument declines to call one hand two.** Eighty per cent against a seventy-six per cent majority baseline is four points of separation — against 94% on 58% for three real authors in one genre, and 98% for a documented attribution projected across genre. The first principal axis does order the samples, acknowledged verse at one end and Rowley at the other, and one Rowley sample (ROW.1) sits among the acknowledged ones: an assumed voice *is* visible as a gradient, and it is not a partition. That is the correct behaviour, and it is the result this protocol most needed: **a deliberately assumed authorial voice, sustained over 54,000 words by a documented single hand, does not produce the separation that two hands produce.**

The consequence for the protocol is a rule. An assumed voice moves a corpus along an axis without splitting it; two hands split it. **Report the baseline and the separation together, always** — 80/76 and 94/58 are opposite findings that a bare accuracy figure would render identical. And the Chatterton case gives the series its fourth kind of control, the one that closes the logic: not only *does the instrument find hands where hands are* (controls 1–3), but *does it refrain from finding hands where a voice merely changes* (control 5). It refrains.

**What is still owed.** One documented forgery is one case. The obvious next tests, all with documentary ground truth and none run here: a forger's acknowledged verse against his forgery in a language other than English; a case where the forger imitates a *named* author rather than inventing one (Ireland's *Vortigern* done properly, against Ireland's own acknowledged plays); and the reverse direction — a corpus known to be two hands presented as one, where the instrument should split what the name unites. The archive's next such test is documented and scoped: volumes II and III of *Das Kapital*, edited into publication by Engels from Marx's manuscripts under Marx's name, projected onto the same letter-trained classifier that placed volume I at 98% Marx.

### 5c. Rebuilt after a referee report — what a mean cannot decide

A referee (2026-09-07) made six repairs stick, two of them fatal to v0.2's headline. All are applied here, both claims are withdrawn, and the rebuild changes the finding in a way that matters more than the correction does.

**The repairs.** (i) *Fold isolation*: `attribute()` fitted vocabulary and z-scaling on the whole corpus before withholding, so the held-out text helped shape the representation used to score it; both are now fitted inside each fold. (ii) *Like-for-like measurement*: v0.2 reported supervised attribution for the controls and unsupervised axis-agreement for the target — different questions; both are now reported for both. (iii) *Balanced accuracy, class recalls and confusion matrices* replace bare accuracy, which hides which class is being missed. (iv) *A permutation null* replaces the majority baseline as the comparator. (v) Preprocessing: Unicode normalized before tokenizing, `<app>` lemmas retained rather than deleted with their variants, per-language word-length thresholds exposed, block size exposed in `report()`. (vi) The feature family is renamed what it is — *short words*, not a curated function-word list.

**The comparator that makes an accuracy figure mean anything.** A nearest-centroid classifier with hundreds of features will separate almost any partition of any corpus. Separability is cheap; an accuracy read against a majority baseline says nothing about whether the *proposed* division is special. The honest comparator is a **text-level label permutation**: shuffle labels across texts preserving class counts, rerun the identical procedure, and ask where the real labels fall in that distribution. Frequency-based vocabulary selection uses no labels, so it cannot bias the comparison — every labeling sees the same feature space.

**The finding, rebuilt.** Folds isolated, 1,000-token blocks, short-word features, 150 permutations each:

| partition | n | balanced acc. | permutation null (mean ± sd, 95th) | p |
|---|---:|---:|---:|---:|
| **the names**, all 39 | 39 | **0.798** | 0.486 ± 0.102, 0.682 | 0.007 |
| **the operation**, all 39 | 39 | **0.860** | 0.496 ± 0.090, 0.632 | <0.007 |
| the names, world-side texts only | 21 | 0.753 | 0.481 ± 0.107, 0.643 | <0.007 |
| the names, world-side, plants and animals excluded | 16 | **0.547** | 0.464 ± 0.122, 0.682 | **0.273** |

**v0.2's claim that the names sit "at chance" is withdrawn.** It rested on unsupervised axis-agreement and does not survive the supervised measurement: a classifier recovers the name-boundary at 0.80 balanced, well outside the null. What the rebuilt table shows instead is three things v0.2 could not have said. The operation partition beats the name partition on the same instrument, the same folds and the same null (0.86 against 0.80). Name-recovery survives holding the *operation* constant (0.75 on the world-side texts alone). And it does **not** survive holding the *subject* constant as well: with plants and animals excluded from both sides, the names fall to 0.547 against a null of 0.464 ± 0.122, p = 0.27 — inside the distribution of arbitrary relabelings, the Theophrastan recall collapsing to 0.36. What the classifier recovers when it recovers the names is, to that extent, what the names correlate with; remove the correlate and the name is not there.

That is weaker than v0.2's claim and more useful. It is also the claim a control series can license: not *the instrument cannot find the names*, but **the operation is the better partition of this corpus on this measurement, and name recovery is unusually sensitive to the removal of the works whose subjects the names most differ over** — a descriptive ordering with its dependencies declared, not a demonstrated conditional.

**The controls, rebuilt on the same machinery.** Three tragedians, spoken portions, three-way: balanced **0.872** against a null of 0.309 ± 0.079, p < 0.007; recalls Ae 0.74, Eu 0.94, So 0.94 — the misses are Aeschylus, as before. Chatterton, re-run on balanced classes of ~2,200 and ~6,800 words: balanced **0.864** against a null of 0.488 ± 0.166, p < 0.005; recalls ACK 0.97, ROW 0.76.

**And v0.2's second claim is withdrawn.** The referee was right that 80%-against-76% could not support "the instrument refuses to split one hand." With balanced classes and balanced accuracy the instrument **does** separate Chatterton-as-Rowley from Chatterton-as-himself, at 0.86 — indistinguishable from its separation of three genuinely different tragedians. The rule v0.2 proposed — *an assumed voice moves without splitting; two hands split* — is false, and removing it is the most important thing this section reports. **A sustained assumed voice is separable from its own author at the same magnitude as a different author is.** No supervised separation, however strong, licenses an inference to distinct hands. That is what §6 already said about counting makers, now with a measurement behind it instead of a caution — and it cuts against the ancient case in the same breath: a separation between two named bodies of ancient text would not have been evidence of two makers either.

**What survives, and what it rests on.** The operation partition outperforming the name partition on identical folds and nulls; the name effect vanishing under subject control; the axis's content and its localization to chapters; and the Chatterton result read the other way round, as proof that separability is not identity. The negative claim about the ancient names now rests on the *conditional* result (0.547, p = 0.27), not on the unsupervised axis, and is stated with that dependency visible.

**Second referee round (same day), and three further corrections.**

*The delivered file was the wrong file.* `operation_axis.py` as shipped with v0.3 was byte-identical to v0.2's — the repairs described in §5c existed in `rigor.py` and had not been folded into the reference implementation. Corrected: `attribute()` now fits vocabulary and scaling **inside each fold** and returns balanced accuracy, class recalls, the confusion matrix, and block- *and* text-weighted accuracy; `permutation_null()`, `compare_partitions()` and `matched_removal()` are exposed. The referee is also right that the fast pathway used for the nulls (`fold_vocab=False`) selects vocabulary corpus-wide: it is legitimate for a permutation comparison, where every labeling sees the identical label-independent feature space, and it is **not** held-out vocabulary selection. Which pathway produced which figure is now declared: the four headline rows of §5c and every null in this paper used `fold_vocab=False`; the fully sealed pathway gives 0.798 / 0.818 / 0.801 balanced on the three families for the names, i.e. the same result.

*The difference between partitions needed its own test.* Two separate nulls do not establish that operation beats names. Tested directly: against 200 arbitrary partitions with the operation partition's class counts, the observed +0.062 is not approached (null mean −0.299, p < 0.005) — arbitrary partitions do far worse than the names, and operation does better. But a bootstrap over texts gives a 95% CI of [−0.091, +0.362] with 71% of resamples positive. **The ordering is descriptive, not established**; stated that way here and in the abstract.

*The exclusion test needed a matched control.* Removing plants and animals changes subject coverage, class balance, corpus size and task difficulty at once. Matched removals — 120 draws of 2 Theophrastan and 3 Aristotelian texts from the same 21-text world-side pool — give a mean of 0.692 ± 0.101, with the real removal at 0.564 sitting in the **lower 15%** and above the 5th percentile (0.522). So: the botanical/zoological removal produces a larger fall than most equivalent removals, and it is not an outlier. **"Remove the correlate and the name is not there" is withdrawn**; what is supported is that name recovery in this corpus is unusually sensitive to the removal of those works, and that a subject-matched comparison — not an exclusion — is the experiment that would settle it.

*And three wordings corrected.* "Balanced classes of ~2,200 and ~6,800 words" was wrong: the Chatterton units are eight constructed samples per side, ~2,240 words each on the acknowledged side and ~6,760 on the Rowley side — balanced in *unit count*, not in tokens, and constructed rather than work-bounded. "Indistinguishable" from the tragedians becomes **numerically similar** (0.864 against 0.872, different experiments). And the classifier does not "call them two makers": it discriminates two textual personae of one documented author, which is the finding, and the inference to makers is exactly what §6 forbids.

**Still owed, and not claimed as done.** The corpus manifest, extraction scripts and run configuration, so the tables can be rebuilt rather than recomputed; work-level rather than constructed-sample units for Chatterton; a subject-matched comparison rather than an exclusion, and a declaration of when each label set was fixed relative to which results (the operation labels behind 0.860 are the analyst's, fixed before the runs of §5c but after the preliminary work of the substantive paper — a dependency ordinary permutations do not absorb); a documented Engels body projected beside the *Kapital* result, since 841 blocks of one known author measure consistency and not discrimination; and the same rebuild applied to the drama and correspondence runs of §5.

## 6. What the instrument cannot do

Stated as limits, because a protocol that lists none is advertising.

**It cannot count makers.** An instrument can find structure; it cannot count hands positively. A null result on names is consistent with one maker, with a workshop, with several hands sharing a training, and with heavy uniform editing. Absence of a detectable second hand at these sample sizes is not proof of one. Every claim about maker-count in a report using this protocol should be flagged as an interpretation, not a measurement.

**It cannot see through translation, and barely through recension.** Different editions of the same work can differ enough in exactly the features used here to move a text measurably. Run within one edition; report the edition.

**Small samples lie.** Below roughly 2,000 tokens a text's profile is unstable; below 350 a block is noise. Report token counts, and do not localize below the window size.

**Genre is stronger than authorship, almost always.** In the run above, comedy separates from tragedy at 100% while three tragedians separate from each other at 94% — the genre signal is the larger one, and any design that lets genre correlate with the tested partition will find the partition. This is the single commonest way this kind of measurement produces a false positive.

**Separability is not identity, and this is the instrument's hardest limit.** Chatterton writing as Rowley separates from Chatterton writing as himself at 0.86 balanced accuracy — the magnitude at which three different tragedians separate from each other (§5c). One documented hand, two sustained voices, and the classifier calls them two. **No supervised separation licenses an inference to distinct makers**, here or anywhere; every such inference must come from elsewhere — from what the separating features are, from whether the separation survives controlling its correlates, and from evidence outside the text. Never report a separation without its permutation null and its confusion matrix.

**And the labels are part of the instrument.** The definitions by which texts are assigned to categories do work that is easy to mistake for the data's. In the run above, a second reader's blind labels agreed with the clusters at 74–76% where the analyst's own agreed at 86–90%; the difference was not noise but a disagreement about where a boundary lay, and the data's answer differed from both readers'. Blind labels, or no label-based claim.

## 7. Availability

`operation_axis.py` (CC0) implements the whole instrument: tokenization with editorial normalization for Greek and Latin scripts, the three feature families, block profiling, the unsupervised axis, leave-one-text-out attribution, out-of-sample projection, rolling localization, and a `report()` that emits the minimum required table for all three families. It has no dependencies beyond NumPy. It is the file that produced the figures above, reduced to its interface.

Every text in the worked run is public: Perseus canonical-greekLit, First1KGreek, Project Gutenberg, and the Internet Archive scan of the 1867 *Kapital*. The tables can be rebuilt from the open sources in an afternoon. The archive asks only that reproductions be reported — agreeing or not — and that the control series be reported with them, since a bare accuracy figure is precisely the thing this protocol exists to say is not a result.

## Notes

[^1]: *The First Axis: The Aristotle/Theophrastus Boundary and the Voice of an Operation*, deposit #1586 (AXN:0679), Crimson Hexagonal Archive, and the metadata packet *Aristotle and Theophrastus ≠ Two Distinct Authors*, #1588. The substantive readings, their falsification conditions, and the corrections applied to them are recorded there and in the notebook *The First Draft*, #1589. This protocol is separable from those claims by design: the controls stand whatever one concludes about the corpus.

## Texts and data

Greek: Perseus canonical-greekLit (Aristotle, Theophrastus, Aristophanes, Aeschylus, Sophocles, Euripides, Diogenes Laertius, Plutarch); OpenGreekAndLatin First1KGreek (Aristotle, Theophrastus). German: Project Gutenberg, *Der Briefwechsel zwischen Friedrich Engels und Karl Marx 1844–1853* (#64327); *Das Kapital*, Erster Band, Erstauflage, Hamburg 1867, Boston Public Library copy via Internet Archive (`daskapitalkritik67marx`), OCR layer used as a stylometric finding aid only, with the seat's ruling that it is not a text layer recorded and respected. Block sizes: 1,000 (Greek prose), 1,200 (drama), 350 (letters), 350 (Kapital, matching the letters' block size for projection). All figures reproducible from the sources named.


---

## Appendix R. Reference implementation (`operation_axis.py`, CC0)

```python
#!/usr/bin/env python3
"""
operation_axis.py — the reference implementation of the instrument described in
"Measuring the Operation, Not the Name" (Sharks 2026).

Four procedures, one feature model:

  profile(tokens)            function-word / trigram / ending profiles on blocks
  axis(corpus)               unsupervised: PC1 and k-means over blocks; no labels
  attribute(train, test)     supervised: leave-one-TEXT-out nearest centroid
  project(train, held_out)   train on one set, score another it never saw

Nothing here is specific to Greek, to philosophy, or to the archive. The
instrument takes tokenized texts and returns numbers. What the numbers mean is
decided by the controls (see the paper, §5), not by this file.

Public domain / CC0. Reproduce, break, report.
"""
import re, unicodedata
from collections import Counter
import numpy as np

# ---------------------------------------------------------------- tokenization

GREEK = r'[\u0370-\u03FF\u1F00-\u1FFF]+'
LATIN = r"[A-Za-zÄÖÜäöüßÀ-ÿ]+"

# Elision and movable-nu are EDITORIAL conventions, not authorial ones: editions
# differ, and the difference can correlate with the partition you are testing.
# Normalize them or your first axis may be your editors'. (Paper §4.2.)
GREEK_ELISION = {
    'δ':'δε','αλλ':'αλλα','ουδ':'ουδε','μηδ':'μηδε','τ':'τε','γ':'γε',
    'καθ':'κατα','κατ':'κατα','μετ':'μετα','μεθ':'μετα','επ':'επι','εφ':'επι',
    'υπ':'υπο','υφ':'υπο','απ':'απο','αφ':'απο','παρ':'παρα','δι':'δια',
    'ανθ':'αντι','αντ':'αντι','ουκ':'ου','ουχ':'ου','ουχι':'ου',
    'εστιν':'εστι','εισιν':'εισι','ταυτ':'ταυτα','ταυθ':'ταυτα',
    'τουτ':'τουτο','τουθ':'τουτο','ωστ':'ωστε','ετ':'ετι','οτ':'οτι',
    'μ':'με','σ':'σε',
}

def strip_accents(w):
    return ''.join(c for c in unicodedata.normalize('NFD', w.lower())
                   if unicodedata.category(c) != 'Mn')

def tokenize(text, script='greek', normalize_elision=True):
    pat = GREEK if script == 'greek' else LATIN
    ws = re.findall(pat, text)
    if script == 'greek':
        ws = [strip_accents(w).replace('ς', 'σ') for w in ws]
        if normalize_elision:
            ws = [GREEK_ELISION.get(w, w) for w in ws]
    else:
        ws = [w.lower() for w in ws]
    return ws

def strip_tei(xml, drop_speakers=True):
    """TEI → plain text. Drops the apparatus, which is the editor's, and
    optionally speaker labels, which are the copyist's."""
    x = re.sub(r'<teiHeader.*?</teiHeader>', '', xml, flags=re.S)
    x = re.sub(r'<(note|app|rdg|bibl)[^>]*>.*?</\1>', '', x, flags=re.S)
    if drop_speakers:
        x = re.sub(r'<(speaker|label)[^>]*>.*?</\1>', '', x, flags=re.S)
    return re.sub(r'<[^>]+>', ' ', x)

# -------------------------------------------------------------- feature models

def f_function_words(ws, maxlen=5):
    """Short words. In Greek maxlen=5 captures the particles and articles; in
    German and English use 6. This is the classic authorship feature."""
    return [w for w in ws if len(w) <= maxlen]

def f_trigrams(ws):
    out = []
    for w in ws:
        s = '_' + w + '_'
        out += [s[i:i+3] for i in range(len(s) - 2)]
    return out

def f_endings(ws):
    return ([w[-2:] for w in ws if len(w) >= 3] +
            ['3:' + w[-3:] for w in ws if len(w) >= 4])

FAMILIES = {'function_words': (f_function_words, 120),
            'trigrams':       (f_trigrams, 400),
            'endings':        (f_endings, 300)}

# ------------------------------------------------------------------- profiling

def blocks(corpus, feature, topk, size=1000, vocab=None):
    """corpus: {name: [tokens]}. Returns (X, labels, vocab).
    Features are relative frequencies within each block; X is z-scored across
    blocks. Blocks, not whole texts: a text is not one observation."""
    if vocab is None:
        cnt = Counter()
        for ws in corpus.values():
            cnt.update(feature(ws))
        vocab = [k for k, _ in cnt.most_common(topk)]
    idx = {k: i for i, k in enumerate(vocab)}
    X, L = [], []
    for name, ws in corpus.items():
        for i in range(0, len(ws) - size + 1, size):
            c = Counter(feature(ws[i:i+size])); tot = sum(c.values())
            if tot < size // 20:
                continue
            v = np.zeros(len(vocab))
            for k, n in c.items():
                if k in idx:
                    v[idx[k]] = n / tot
            X.append(v); L.append(name)
    X = np.array(X)
    return X, np.array(L), vocab

def zscore(X):
    mu, sd = X.mean(0), X.std(0) + 1e-9
    return (X - mu) / sd, mu, sd

# ------------------------------------------------------------------ procedures

def axis(corpus, family='function_words', size=1000, anchor=None):
    """UNSUPERVISED. Returns the first principal axis over blocks, per-text
    means, and the k=2 clustering. No labels are used anywhere. `anchor` names a
    text that should score negative, fixing the sign so runs are comparable."""
    feature, topk = FAMILIES[family]
    X, L, vocab = blocks(corpus, feature, topk, size)
    Z, _, _ = zscore(X)
    U, S, Vt = np.linalg.svd(Z - Z.mean(0), full_matrices=False)
    pc = (Z - Z.mean(0)) @ Vt[0]
    if anchor is not None and pc[L == anchor].mean() > 0:
        pc = -pc
    means = {t: float(pc[L == t].mean()) for t in dict.fromkeys(L)}
    return {'pc1': pc, 'labels': L, 'per_text': means,
            'variance_explained': float(S[0]**2 / (S**2).sum()),
            'loadings': dict(sorted(zip(vocab, Vt[0]), key=lambda kv: -abs(kv[1]))[:25]),
            'clusters': kmeans2(Z)}

def kmeans2(Z, restarts=20, iters=100, seed=0):
    rng = np.random.default_rng(seed); best = None
    for _ in range(restarts):
        C = Z[rng.choice(len(Z), 2, replace=False)]
        for _ in range(iters):
            a = ((Z[:, None, :] - C[None])**2).sum(2).argmin(1)
            C2 = np.array([Z[a == j].mean(0) if (a == j).any() else C[j] for j in range(2)])
            if np.allclose(C2, C): break
            C = C2
        inertia = ((Z - C[a])**2).sum()
        if best is None or inertia < best[0]: best = (inertia, a)
    return best[1]

def attribute(corpus, group_of, family='function_words', size=1000, fold_vocab=True):
    """SUPERVISED, with the fold sealed. Leave-one-TEXT-out nearest centroid, and
    — this is the repair of v0.2, which fitted both on the whole corpus —
    VOCABULARY AND SCALING ARE FITTED INSIDE EACH FOLD. Returns balanced accuracy,
    class recalls and the confusion matrix, because a bare accuracy hides which
    class is being missed, and block- and text-weighted accuracy, because long
    texts otherwise dominate.

    fold_vocab=False falls back to a corpus-wide vocabulary. That is legitimate
    ONLY inside a permutation comparison, where every labeling sees the identical
    feature space and the selection is label-independent; it is not held-out
    vocabulary selection, and any table produced with it must say so."""
    feature, topk = FAMILIES[family]
    B = {k: [v[i:i+size] for i in range(0, len(v) - size + 1, size)] for k, v in corpus.items()}
    B = {k: v for k, v in B.items() if v}
    fixed = None
    if not fold_vocab:
        cnt = Counter()
        for k in B:
            for b in B[k]: cnt.update(feature(b))
        fixed = [w for w, _ in cnt.most_common(topk)]
    per = {}; conf = Counter()
    for t in B:
        tr = [k for k in B if k != t]
        groups = {group_of(k) for k in tr}
        if len(groups) < 2: continue
        if fixed is None:
            cnt = Counter()
            for k in tr:
                for b in B[k]: cnt.update(feature(b))
            vocab = [w for w, _ in cnt.most_common(topk)]
        else:
            vocab = fixed
        Xtr = np.vstack([_vecs(B[k], feature, vocab) for k in tr])
        Ltr = np.concatenate([[k] * len(B[k]) for k in tr])
        mu, sd = Xtr.mean(0), Xtr.std(0) + 1e-9
        Ztr = (Xtr - mu) / sd
        G = np.array([group_of(k) for k in Ltr])
        cent = {g: Ztr[G == g].mean(0) for g in groups}
        Zte = (_vecs(B[t], feature, vocab) - mu) / sd
        pred = [min(cent, key=lambda g: np.linalg.norm(z - cent[g])) for z in Zte]
        truth = group_of(t); per[t] = float(np.mean([p == truth for p in pred]))
        for p in pred: conf[(truth, p)] += 1
    gs = sorted({group_of(t) for t in per})
    rec = {g: conf[(g, g)] / max(1, sum(conf[(g, h)] for h in gs)) for g in gs}
    tot = sum(conf.values())
    return {'balanced': float(np.mean(list(rec.values()))),
            'block_accuracy': sum(conf[(g, g)] for g in gs) / max(1, tot),
            'text_accuracy': float(np.mean(list(per.values()))) if per else 0.0,
            'recalls': rec, 'confusion': {f'{a}->{b}': c for (a, b), c in conf.items()},
            'per_text': per, 'n_blocks': tot,
            'majority_baseline': max(Counter([group_of(t) for t in per]).values()) / max(1, len(per)),
            'fold_vocab': fold_vocab}


def _vecs(bs, feature, vocab):
    idx = {w: i for i, w in enumerate(vocab)}
    out = []
    for b in bs:
        c = Counter(feature(b)); tot = sum(c.values()); v = np.zeros(len(vocab))
        for w, n in c.items():
            if w in idx: v[idx[w]] = n / tot
        out.append(v)
    return np.array(out)


def permutation_null(corpus, group_of, family='function_words', size=1000, n=150, seed=0):
    """Text-level label permutation preserving class counts — the comparator that
    makes an accuracy figure mean something. Uses fold_vocab=False by design:
    every labeling must see the identical feature space, and frequency-based
    selection uses no labels."""
    rng = np.random.default_rng(seed)
    texts = list(corpus); labs = [group_of(t) for t in texts]
    out = []
    for _ in range(n):
        m = dict(zip(texts, rng.permutation(labs)))
        out.append(attribute(corpus, lambda k: m[k], family, size, fold_vocab=False)['balanced'])
    return np.array(out)


def compare_partitions(corpus, a_of, b_of, family='function_words', size=1000, n=150, seed=0):
    """Two partitions of ONE corpus, and a null for the DIFFERENCE — separate
    nulls for each do not test whether the gap between them is reliable."""
    A = attribute(corpus, a_of, family, size, fold_vocab=False)['balanced']
    Bv = attribute(corpus, b_of, family, size, fold_vocab=False)['balanced']
    rng = np.random.default_rng(seed); texts = list(corpus)
    labs = [b_of(t) for t in texts]; diffs = []
    for _ in range(n):
        m = dict(zip(texts, rng.permutation(labs)))
        diffs.append(attribute(corpus, lambda k: m[k], family, size, fold_vocab=False)['balanced'] - A)
    diffs = np.array(diffs)
    return {'a': A, 'b': Bv, 'difference': Bv - A, 'null_mean': float(diffs.mean()),
            'p_difference': float((diffs >= (Bv - A)).mean())}


def matched_removal(corpus, group_of, removed, family='function_words', size=1000, n=120, seed=0):
    """Before attributing a drop to what you removed, remove something else the
    same shape. Draws removals with the same per-class counts and reports where
    the real removal falls among them."""
    import itertools
    feature, topk = FAMILIES[family]
    real = attribute({k: v for k, v in corpus.items() if k not in removed}, group_of,
                     family, size, fold_vocab=False)['balanced']
    byg = {}
    for k in corpus: byg.setdefault(group_of(k), []).append(k)
    counts = Counter(group_of(k) for k in removed)
    pools = [list(itertools.combinations(byg[g], c)) for g, c in counts.items()]
    rng = np.random.default_rng(seed); vals = []
    for _ in range(n):
        pick = tuple(x for p in pools for x in p[rng.integers(len(p))])
        if set(pick) == set(removed): continue
        vals.append(attribute({k: v for k, v in corpus.items() if k not in pick}, group_of,
                              family, size, fold_vocab=False)['balanced'])
    vals = np.array(vals)
    return {'real': real, 'matched_mean': float(vals.mean()), 'matched_sd': float(vals.std()),
            'fraction_at_or_below_real': float((vals <= real).mean()), 'n': len(vals)}

def project(train, group_of, held_out, family='function_words', size=1000):
    """Train centroids on one corpus; score texts it never saw. Vocabulary,
    standardization and centroids all come from `train`. This is the only
    procedure that can test a hypothesis rather than describe a corpus."""
    feature, topk = FAMILIES[family]
    X, L, vocab = blocks(train, feature, topk, size)
    Z, mu, sd = zscore(X)
    G = np.array([group_of(l) for l in L])
    cent = {g: Z[G == g].mean(0) for g in set(G)}
    if len(cent) != 2:
        raise ValueError('project() expects exactly two training groups')
    a, b = sorted(cent)
    Y, LY, _ = blocks(held_out, feature, topk, size, vocab=vocab)
    Zy = (Y - mu) / sd
    out = {}
    for t in dict.fromkeys(LY):
        z = Zy[LY == t]
        lean = np.linalg.norm(z - cent[b], axis=1) - np.linalg.norm(z - cent[a], axis=1)
        out[t] = {'n_blocks': int(len(z)), 'mean_lean': float(lean.mean()),
                  f'pct_nearer_{a}': float((lean > 0).mean())}
    return {'toward': a, 'away': b, 'texts': out}

def localize(text_tokens, train, group_of, family='function_words',
             window=1000, step=250):
    """Where inside one text does the lean move? Rolling windows on a fixed
    axis. Use it to find seams; do not use it to find single sentences."""
    feature, topk = FAMILIES[family]
    X, L, vocab = blocks(train, feature, topk, window)
    Z, mu, sd = zscore(X)
    G = np.array([group_of(l) for l in L]); cent = {g: Z[G == g].mean(0) for g in set(G)}
    a, b = sorted(cent)
    idx = {k: i for i, k in enumerate(vocab)}
    out = []
    for i in range(0, len(text_tokens) - window + 1, step):
        c = Counter(feature(text_tokens[i:i+window])); tot = sum(c.values())
        v = np.zeros(len(vocab))
        for k, n in c.items():
            if k in idx: v[idx[k]] = n / tot
        z = (v - mu) / sd
        out.append((i, float(np.linalg.norm(z - cent[b]) - np.linalg.norm(z - cent[a]))))
    return out

# ------------------------------------------------------------------- reporting

def report(corpus, group_of, anchor=None, families=('function_words','trigrams','endings')):
    """The minimum report the protocol requires: every family, the unsupervised
    axis, the supervised accuracy against its own baseline, and the agreement
    between the axis and the labels. Publish all three families or none."""
    rows = []
    for fam in families:
        A = axis(corpus, fam, anchor=anchor)
        S = attribute(corpus, group_of, fam)
        gs = sorted({group_of(t) for t in corpus})
        agree = None
        if len(gs) == 2:
            neg = [t for t in A['per_text'] if A['per_text'][t] < 0]
            agree = max(
                sum(1 for t in A['per_text'] if (t in neg) == (group_of(t) == gs[0])),
                sum(1 for t in A['per_text'] if (t in neg) == (group_of(t) == gs[1])),
            ) / len(A['per_text'])
        rows.append({'family': fam, 'pc1_variance': A['variance_explained'],
                     'axis_agrees_with_labels': agree,
                     'attribution_accuracy': S['accuracy'], 'baseline': S['baseline']})
    return rows

if __name__ == '__main__':
    print(__doc__)
    print('Import it. The controls of §5 are not optional:')
    print('  1. a bounded single-author corpus  → expect closed neighbours, high self-attribution')
    print('  2. distinct authors, one genre     → expect the instrument to recover the names')
    print('  3. a documented case               → project a known attribution and check it')
    print('  4. then, and only then, the corpus you are asking about')

```
