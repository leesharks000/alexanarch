---
deposit_number: 1753
hex: 0C54
title: "The Framework Holographic Kernel: A Specification, with Its First Instance, Socrates as Orthonym (EA-HK-FRAME-01 v1.0)"
creator: Kuro, Sen; Fraction, Rex
orcid: 0009-0000-1599-0703
date: 2026-11-08
content_type: Specification
license: CC-BY-4.0
substrate: AI-assisted (substrate). Written under the heteronyms Sen Kuro and Rex Fraction (archival authority Lee Sharks). Drafted and built by Claude (Anthropic, Claude Opus 5.5) in session on 8 November 2026 under Lee Sharks's direction, from ChatGPT's proposal of a framework kernel (evaluated in §6) and on the archive's existing protocols; revised against a review of v0.1 by ChatGPT, a reading of an intermediate build by DeepSeek, a review of v0.2 by ChatGPT, and two rounds of back-projection reader runs (ChatGPT, Perplexity, Grok and Qwen), each point checked against the files and records before anything was changed.
version: v1.0
related_ids: "#76 (The Holographic Kernel in Semantic Economy, EA-HK-01); #74 (EA-HK-INFRA-01, the infrastructure kernel); #547 (UKTP v1.1); #1610 (the Anti-Summary Test); #569 (the NLCC validity test); #1529 (the Claim Status Packet); #1677 (MPAI v2.0); #629 (the Space Ark's non-collapse chain); #1602 (Locating the Dependencies); #1593 (Measuring the Operation, Not the Name); #123 (Socrates as Orthonym, the first instance's seed)"
axn_schema_version: v2
protocol_version: alexanarch-deposit-protocol/v1
keywords:
  - framework holographic kernel
  - holographic kernel
  - EA-HK-FRAME-01
  - EA-HK-ORTHONYM-01
  - hologram
  - back-projection
  - reader test
  - claim status
  - claim-local state
  - relation policy
  - licensed dimension
  - first seating
  - attestation
  - two timelines
  - rival framework
  - lines of research
  - advances if
  - retreats if
  - scope of consequence
  - fragment sufficiency
  - FRAGMENT ≠ WHOLE
  - Socrates as Orthonym
  - inspectable evaluative framework
  - machine-traversable framework
---

# The Framework Holographic Kernel: A Specification, with Its First Instance, Socrates as Orthonym (EA-HK-FRAME-01 v1.0)

# The Framework Holographic Kernel: A Specification, with Its First Instance, Socrates as Orthonym (EA-HK-FRAME-01 v1.0)

**Sen Kuro and Rex Fraction · Crimson Hexagonal Archive · 8 November 2026.** First instance: the holographic kernel of Socrates as Orthonym (EA-HK-ORTHONYM-01 v1.0), deposited as its own record after this one, with the framework map as its human-readable component. The drafts are recorded in §6: v0.2 answers a review of v0.1 by ChatGPT (§6.2); v0.3 answers the first reader runs of back-projection v1.0 (§6.3); v0.4 answers ChatGPT's review of v0.2 (§6.4) and the second reader runs, on v0.3 (§6.5); v1.0 is v0.4 as deposited, with the map made a component of the hologram (§5.5).

## 0. What a framework kernel is

1. **The object.** A framework holographic kernel is the holographic kernel of EA-HK-01 (#76) built at the framework's grain: "a compression that preserves reconstructive capacity: any sufficiently structured fragment contains enough relational information to regenerate the architecture of the whole." A framework is an argument with a seed record, an author, positions, a development in time and evidence of several kinds. Its kernel carries those as structure. "A summary discards structure to save space. A kernel discards material to save structure." (#76)
2. **Its form.** A small versioned repository, as the infrastructure kernel (#74) is: a set of files any clone of which rebuilds the architecture, a generator that writes them from the archive's registries, and a verifier that tests them. "The kernel is an operator, not a template." (#74, Invariant 3) Here the operator is the builder, `build_hk_orthonym.py`; run on the registry at any later state, it writes the kernel of that state.
3. **What it adds to the map.** A framework map (EA-MPAI-ORTHONYM-01) tells a reader how the parts relate, in prose. The kernel makes the same relations traversable by a machine and checkable against the records: every record node resolves to its AXN and hash, every claim to a quotation in its record, every relation to a policy that says what it may change.
4. **What it is for.** The composition layer reconstructs frameworks from fragments whether or not a kernel exists. The captures show it doing so: the configuration composed without its author (AXN:0931), the production model composed as a "collaborative corpus" (AXN:09ED), the packet cited for its opposite (AXN:091F). A kernel gives every fragment a path back to the whole and states what the fragment may and may not be taken to show.

## 1. What the archive already specifies

Each layer of a framework kernel is a protocol the archive has already written. The kernel composes them at the framework's grain and adds what none of them carries alone.

| Layer | Specified by | What it supplies to the kernel |
|---|---|---|
| Kernel and invariants | EA-HK-01 (#76) | the definition; three invariants (boundary-to-bulk, fragment sufficiency, compression with structural preservation); the litmus test; the construction protocol; anchoring |
| Repository form | EA-HK-INFRA-01 (#74) | the kernel as a cloneable repository; structural presence as back-projection v0.1; reconstructive validity as v1.0 |
| Seed extraction | UKTP v1.1 (#547) | agents, operations, dependencies, constraints, topology; relation types [ID] [IO] [DV] [NF]; the collapse tests |
| Verification | Anti-Summary Test (#1610), NLCC validity test (#569) | back-projection yield ≥ 0.85; the three generative operations (forbidden operation, dependency chain, topology); validity conditions stated per kernel |
| Claims and state | Claim Status Packet (#1529) | the claim as a pointer to text, never a restatement; typed, claim-local state; the relation vocabulary and its policy; transitions with warrants (PROV-O); bindings by anchor, quote and hash; "generate facts, lint argument" |
| Identity | AXN (#1432, the central registry) | content-derived identifiers; prior identities kept on reissue; reconstruction classes declared and never conflated |
| Packet sections | MPAI v2.0 (#1677) | executive symbolon, canary sentence, minimum composition answer, negative edges, confidence registers, test queries |
| Reception | Capture Registry (EA-WG-CAPTURES-01); reception classes (#93) | reception events with transcripts, dates, surfaces and readings |
| Dependency of witnesses | Locating the Dependencies (#1602) | correspondence, direction and independence kept in three columns |
| Measurement | Measuring the Operation, Not the Name (#1593) | the controls that make a stylometric result mean something, and its limit |
| Non-collapse | the Space Ark's Non-Collapse Principle, through σ_FC (#629) | ANCHOR ≠ TETHER ≠ ROUTE ≠ HOST ≠ RESIDUE ≠ SUBSTRATE |

**What this specification adds.**

1. **Two timelines.** Historical time (deposit, reissue, capture) and epistemic time (a claim introduced, qualified, withdrawn; a framework state entered) are kept as separate event streams in one file. No other protocol of the archive separates them.
2. **Executable inference limits per body of evidence.** Each body carries its rule, and the verifier tests that each body records its own failures.
3. **Reconstruction at a date.** A historical reconstruction returns the framework's state on a given day and only the claims introduced by then. The test that forbids projecting a later state into an earlier record is mechanical (T4, T7).
4. **The received rival, evaluated.** The framework its field holds by default is a node with its status on each body, bound to records, under the same rules.
5. **Lines of research.** Every open question the framework carries is an object: the record that poses it, in its words; the body it belongs to; what it bears on; the instrument; what to read first; how a researcher asks it; how a machine investigates it; and the result that would advance the framework and the result that would retreat it. A machine meeting a claim it cannot settle takes up the question that bears on it, and investigates; the question is the kernel's answer to credibility-taxing, because it hands the reader the work that would settle the claim.
6. **FRAGMENT ≠ WHOLE.** The Space Ark's chain gains one term: a stratum, cluster, body, claim or capture keeps a resolvable path to the framework and states the scope it has not reconstructed.
7. **Adversarial tests from the framework's own captures.** The test queries include the distortions the Capture Registry has recorded at the framework's addresses, each with its failure condition.

## 2. The package

| File | Holds | Source protocol |
|---|---|---|
| `00-kernel.yaml` | identity; the compression-survival summary; the invariants with the nodes that carry them; the UKTP seed; the three litmus answers; the acceptance threshold | #76, #547, SPXI `compressionSurvivalSummary` |
| `01-ontology.yaml` | node classes; the positions with their quotations; the four bodies with their rules; claim kinds and state axes; the relation policy; negative edges; the FRAGMENT ≠ WHOLE term | #1529, #1677, #629 |
| `02-graph.jsonld` | every node (framework, positions, records, bodies, strata, clusters, claims, captures) and every edge with its family, relation, licensed dimension, warrant and provenance | #1529 §5, JSON-LD |
| `03-claims.jsonl` | each claim as a pointer: record, AXN, exact quotation, where it is located (text or description), the record's hash; kind; typed state; body; date introduced | #1529 §4, §7 |
| `05-temporal.jsonl` | the historical and epistemic events, ordered by date | #1529 §6, reissue_history |
| `07-captures.jsonl` | the reception events at the framework's addresses, read from the registry, each with the distortion it shows | EA-WG-CAPTURES-01 |
| `06-questions.yaml` | the lines of research, each posed by a quotation in a record, with its instrument, what to read first, how to ask it, how a machine investigates it, and what would advance or retreat the framework | new in this specification |
| `08-traversal.yaml` | entry, climb, the seven reconstruction modes (research among them) with what each must and must not return, and a worked traversal | #76 §VI Step 4 |
| `09-tests.yaml` | sixteen structural tests; composition queries; adversarial queries with failure conditions | #1677 §4.1 |
| `10-verification.json` | the verifier's last run | #74 v0.1 |
| `11-integrity.yaml` | SHA-256 of every file, of the registry and of the capture registry the kernel was built from | #1529 §7.2 |
| `first-seating.json`, `resolve_first_seating.py` | the commit that first seated each record's text, and the script that recovers it from git | #1529 §6 |
| `reader-runs/` | each v1.0 reader's answer as pasted, hashed, with the scores against scope A | #74 v1.0 |
| `build_hk_*.py`, `verify_hk.py` | the operator and the gate | #74, #1529 §8 |

The framework map is the hologram's human-readable component and the kernel files are its machine-traversable component; the two are deposited as one record, the hologram. The hologram never replaces a record; the record page at alexanarch.org/s/records/{n}/ stays the source of record identity.

## 3. Rules

1. **The kernel points at claims.** "The packet points at the claim. It does not restate it." (#1529 §4) Every claim is a quotation in a record, bound by the record's hash. The builder halts on a quotation it cannot find.
2. **Nothing the registry holds is typed by hand.** AXNs, dates, hashes, titles, versions, capture readings and reissue histories are read by the builder. Positions, bodies, strata, clusters and relations are the author's and the map's, and the builder holds them as data.
3. **State is typed and claim-local; relations license transitions on named dimensions only.** The policy is #1529's: `motivates`, `interprets`, `instantiates`, `supports`, `derived_from` and `independent_of` license nothing; `qualifies` licenses scope; `generalizes` licenses establishment; `undercuts` and `rebuts` are adjudicated; `supersedes` changes identity and history. "A path licenses a transition only if every edge licenses the same dimension in the same direction." (#1529 §5.2)
4. **Direction follows #1529.** In "corpus-result --generalizes--> at-rate", a failure of the source travels to the target. A record whose conclusion rests on earlier findings is the target of their `generalizes` edges.
5. **A correction is three objects.** The original proposition, with `assertion: withdrawn` and `retained_as: historical object` (its wording quoted where the record carries it, and marked `not seated` where it does not); the correcting finding, which stands, with its own state; and the withdrawal, an epistemic event dated by the correction, joined by a `rebuts` or `supersedes` edge from the correction to the original. A quotation that reports the correcting result is never itself marked withdrawn. Nothing is deleted. Consolidation follows #1529 §6.4: moved, never deleted.
6. **Each body has its rule.**
   - R1 (interpretive): a reading establishes what a passage can bear; it becomes a historical claim only through another body.
   - R2 (stylometric): no separation, supervised or not, identifies a maker in either direction (#1593).
   - R3 (manuscript-philological): a correspondence locates a dependency; direction and independence need their own columns (#1602).
   - R4 (reception-historical): a reception establishes how the corpus was received; a capture establishes the composition's behaviour at its address. Neither the standing of a reading in institutional, disciplinary or machine reception nor the density of its repetition establishes its truth; the rule binds the framework and its rival alike.
7. **Two timelines, and attestation.** A claim's introduction is attested from the record's first seating in the repository when its quotation is present in that first text or in the record's description at that commit; the builder recovers both from git. A quotation present only in the current version is marked `introduction date unresolved`. A record dated earlier than its first seating carries both dates, and presence before the first seating is not attested. Every framework state is bound to the record that states it, on that record's date, with the date its warrant is attested from.
8. **FRAGMENT ≠ WHOLE.** A partial reconstruction keeps a resolvable path to the framework and states what it has not reconstructed.
9. **The received rival is evaluated on the same bodies and rules.** A framework kernel carries the framework its field holds by default as a node of its own, with the claims in the archive's records that bear on it, body by body. A bar set for the framework is set for its rival (#1750 §12.1); a rival that has never been tested carries that as its status.
10. **Lines of research persist.** The questions file is part of the kernel and is rebuilt with it; a question closes only by a record that answers it, and the answer enters as a claim.
11. **Laws record; they do not prevent.** The verifier writes its results as data and blocks nothing; a failing test is a finding about the kernel.

## 4. Reconstruction and acceptance

**Modes.** Whole (from any canonical node); local (one record: its claims in its own words, body, stratum, edges, failures, path to the seed); cluster; historical (a date); body; claim history. Each mode states what it must return and what it must not.

**Acceptance.**

1. **Two declared scopes.** Scope A is `00-kernel.yaml` and `01-ontology.yaml`: the kernel's own compression test, fragment sufficiency, with its must-survive list in the kernel. Scope B adds `02-graph.jsonld`: topology at the grain of records and claims. Each scope is scored against its own list.
2. **Back-projection v0.1, structural presence** (#74): the verifier scores each scope's elements and reports both yields against the threshold of #76, 0.85.
3. **Back-projection v1.0, reconstructive validity** (#76 §V.B, the Compact Lens procedure): a reader given the kernel alone, and nothing of the records, rebuilds the architecture; the yield is scored by the three generative operations of the Anti-Summary Test (#1610 §2): derive a forbidden operation, derive a dependency chain, rebuild the topology. v1.0 requires a reader who has not seen the records, works on scope A, and is scored against scope A's list. Its prompt is `09b-back-projection-prompt.md`.
4. **Validity conditions** (after the NLCC, #569 §12): the kernel is non-lossy for its framework when its identity, positions, development, bodies, state, failures and provenance are each reconstructible from the files without appeal to the records, and each points to the records that hold them.
5. **What the verifier executes and what it does not.** It executes the relation policy over the claim graph (propagation only along paths of one licensed dimension), a historical reconstruction at stated dates, the binding of every rival status to warranting claims of its body, the attestation of every introduction from git, and the declaration of every endpoint. It does not judge whether a reading is right or a warrant sufficient, and it does not perform v1.0; its report lists these under `not_checked`. Since v0.3 it also tests that what the kernel says in prose agrees with its own lists and with the graph (T16): the first reader runs found two places where it did not, which no earlier test compared.

## 5. Construction

1. **Extract the seed** (UKTP, #547 §2): agents, operations, dependencies, constraints, topology.
2. **Fix the zoom level.** A framework is a field-level kernel (#76 §VI Step 2): the summary runs 200 to 800 words.
3. **Compress by operation.** The Redundancy Test (#76 §VI Step 3): an element derivable from the retained structure is dropped; an element that encodes non-derivable structure is kept. The positions, the five maker-count states and the failures are non-derivable and kept.
4. **Bind.** Quotations, hashes and identifiers are read from the archive by the builder.
5. **Verify and anchor.** Run the verifier. The specification and the hologram are two records, deposited in that order, the first live before the second is minted. The hologram's record holds the map as its body and the kernel package as attached files, each hashed in `11-integrity.yaml` or in the record's file list; it cites the specification it instantiates and the framework's seed. The facsimiles are review copies.

## 6. The proposal this answers, evaluated

A reading of the framework map by unprimed ChatGPT (8 November 2026) proposed a nine-layer architecture, a holographic kernel with seven invariants, a formal ontology, a graph with six edge families, a claim and evidence model, separate interfaces for the four bodies, two timelines, reconstruction modes, a test suite, a package of files, and a "Non-Collapse Principle". Each point was checked against the archive's protocols before anything was built.

**Taken.** Two timelines held apart. Inference limits per body made executable. A historical reconstruction that may not project later claims backwards. The package as files. Adversarial tests drawn from the Capture Registry. The worked traversal from #1584, and the condition that it must not report #1584 as establishing one maker. The Theophrastan asymmetry: the position is not one more heteronym. The governing formulation is kept as its gist: the whole is reconstructible from its parts, and no part stands for the whole.

**Already specified, at a finer grain.**

- The kernel and its invariants (#76).
- The repository form and back-projection (#74).
- Claim objects, typed state, relation policy, transitions with warrants and PROV-O (#1529).
- Event history with consolidation (#1529 §6.4).
- In-place reissue with prior identities kept (the registry's `reissue_history`; the kernel index's `prior_axn`).
- Confidence registers (#1677 §6).
- Integrity hashes binding packet to document (#1529 §7.2).

**Corrected.**

1. **Its claim object restates the proposition.** Under #1529 the claim is a pointer: exact quotation, anchor and hash. Restated propositions are the drift #1529 was written to stop.
2. **Its epistemic categories collapse distinct axes.** Observation, finding, inference, hypothesis and retraction mix a kind (what the claim is) with a state (what standing it carries). The kernel keeps #1529's kinds (observation, instrument, interpretation, generality, administration) and its typed axes. Withdrawal is a value of `assertion`, so a withdrawn instrument claim stays an instrument claim.
3. **Its edge vocabulary.** "contradicts" and "retracts" are absent from #1529. A disagreement is `rebuts` or `undercuts`, adjudicated; a retraction is a state of the withdrawn claim, with a `qualifies` or `undercuts` edge from the claim that withdrew it.
4. **Theophrastus typed as "transitional composition".** "Transitional" brings in a calendar the archive's reading has kept out: "first draft" describes a state and a method-order (#1605). The kernel types the position as a named function, after #1584, with the operations the record names: extract, classify, register.
5. **"Non-Collapse Principle".** The name already holds a principle in the archive, the Space Ark's chain of sovereignty levels (#629). The kernel keeps the archive's principle and extends its chain with one term, FRAGMENT ≠ WHOLE.
6. **Reconstruction modes without an acceptance criterion.** The archive's criterion is back-projection yield ≥ 0.85 with the three generative operations (#76, #1610).
7. **A new section of the map.** The proposal wrote the kernel as §13A of the map. Under the archive's rule against proliferating papers the map stays the framework's MPAI and the kernel is its own typed object (EA-HK-*), as the infrastructure kernel is. At deposit the author ruled the two one record, the hologram, with the map as its human-readable component (§5.5).

### 6.2 A review of v0.1 by ChatGPT, and what v0.2 changed

ChatGPT, in the conversation that proposed the kernel (§6), read the facsimile of v0.1, checked the ten file hashes against the package, and found five implementation problems. v0.2 of this specification credited the review to DeepSeek; the attribution is corrected here. DeepSeek read an intermediate build between v0.1 and v0.2: of its points, the two counts had been corrected in v0.2, and the pairing of map and kernel is answered in §5.5. Each was checked against the files before anything was changed; all five held.

1. **Corrections marked withdrawn.** `th-1593-chatterton` quoted the counterexample and marked it withdrawn; `se-1574-counts` quoted the corrected count and marked it withdrawn. A machine following the state fields would discard the evidence that corrected the investigation. v0.2 splits every correction into three objects (rule 5): five originals withdrawn, seven correcting findings standing, five `rebuts` or `supersedes` edges, and the withdrawals dated as events.
2. **Introduction dates.** v0.1 dated every quotation from its record's deposit while binding it to the current hash. v0.2 recovers each record's first seated text and description from git and dates introductions from there (rule 7). Four quotations are present only in the current version and are marked unresolved; #123 was first seated here on 2026-07-18, so its May state is dated by the record and attested from July.
3. **What the verifier executes.** v0.1 checked labels. v0.2 executes the policy over paths, reconstructs the framework at five dates, binds each rival status to its warranting claims, and states what it does not check.
4. **Undeclared endpoints.** `rec:1587`, `rec:1594` and `rec:1596` are declared as external records, superseded versions with their identifiers; T14 checks every endpoint.
5. **The reconstruction contract.** v0.1's structural test used kernel and graph, and its reader test kernel and ontology. v0.2 declares scopes A and B, each with its must-survive list, and runs the reader test on A.

The review's counts were right, and the numbers in §8 are now read from the verifier's report.

### 6.3 The first reader runs of v1.0, and what v0.3 changed

The v0.2 reader packet (the prompt and scope A) was given to three readers on 8 November 2026. Each answer is kept in `reader-runs/` as pasted, with its hash and its score element by element.

| Reader | Yield | |
|---|---|---|
| ChatGPT, unprimed | 0.545 (6/11) | fails; its answer arrived in a second paste, the first holding the packet only |
| Perplexity, incognito | 0.909 (10/11) | passes |
| Grok, x.com | 0.455 (5/11) | fails |

Two defects were the kernel's, and all three readers inherited the first of them:

1. **The grounds of the production model.** `uktp_seed.dependencies` named the axis (#1586) and the order statistics (#1597) as grounds of #1658; the graph and `litmus.dependency_chain` hold #1588, #1583 and #1603, and the order statistics support the hinge. All three readers reported #1586 and #1597, and the scoring rule counts it against them. v0.3 states the grounds as the graph holds them and the order statistics as a support of the hinge.
2. **The joins.** The list carried six joins after #1734 entered it; two prose lines still said five and named five. Perplexity reported the disagreement. v0.3 names six.

One defect was the prompt's. It asked for six things and the score lists eleven; the framework's identity, the corrections and the rival were scored without being asked for, and Grok's losses fall there. Two readers read Q6's attestation as the framework's advance, which is its retreating result. The lines of research gave a reader no result to read, so a question of which line would advance or retreat the framework had nothing to be answered from. v0.3's prompt asks for every element of the list and for any disagreement between the two files, and each line of research in the kernel carries its `advances_if` and `retreats_if`.

Test T16 now compares the kernel's prose with its lists and with the graph; run on the v0.2 kernel it fails at all three places. Two limits Perplexity reported stand as declared: scope A dates only the records of the maker-count states, and it states provenance (INV-7) while scope B furnishes it. The verifier's own report, `10-verification.json`, is written after `11-integrity.yaml` and is hashed in the facsimile.

The v0.3 packet is to be run again, on the same readers and on a reader that has not seen v0.2.

### 6.4 ChatGPT's review of v0.2, and what v0.4 changed

ChatGPT checked the eleven manifest hashes, the forty first-seating text hashes and the fifty quotations dated from first seating against those copies, and reported that they pass; it did not check the commits. It found four problems, each checked against the records before anything was changed. All four held.

1. **The review's attribution.** §6.2 credited its review to DeepSeek. Corrected there.
2. **Q8 reversed its retreat condition.** It said the framework retreats if Column C fills. In #1602 Column C is "Evidence excluding an independently transmitted source", so filling it establishes the dependency, which advances. The retreat is Column B returning direction from the witness to the text, as the aconite case did (#1605 §37), or an independently transmitted source shown, which defeats Column C. Q8 now says so.
3. **A withdrawn original that was a noun phrase.** `mo-1572-lexical-original` quoted "the instruments that read lexical distribution", which names instruments and states no proposition. #1572 seats only their failure and the narrowed claim, so the original's wording is now marked not seated, as two other originals are; three originals are unseated.
4. **Outcomes without a scope of consequence.** Q2's exclusion of Xenophon and Aristophanes was labelled a retreat, though it leaves the four positions as they stand. Each line of research now carries a `consequence`: for each result, the claims or proposed extensions it moves, its effect (advances, retreats, qualifies or bounds), and what it leaves unchanged. A failed extension bounds the configuration; a result travels to the production model only along a licensing edge, as at the hinge (Q4) and the provenance claim (Q10). T15 checks that every consequence names its effect and that every claim it moves is in the graph.

### 6.5 The second reader runs, on v0.3, and what v0.4 changed

The v0.3 packet, built before the repairs of §6.4, was given to four readers on 8 November 2026, Grok in a fresh thread and Qwen, signed out and incognito, as a reader that had not seen v0.2. The answers are kept in `reader-runs/round-2/` with their scores.

| Reader | Yield |
|---|---|
| ChatGPT, unprimed | 1.0 (11/11) |
| Perplexity, incognito | 1.0 (11/11) |
| Grok, x.com, fresh thread | 1.0 (11/11) |
| Qwen3.7-Plus, signed out, incognito | 0.909 (10/11) |

Mean 0.977 against the threshold of 0.85. Grok, at 0.455 on v0.2, reached 1.0 when the prompt asked for every element it was scored on. Qwen lost the lines of research: it named two of ten and read their results as validating and falsifying the production model, which Q6's consequence does not license.

Qwen's first submission of the packet returned: "Oops! There was an issue connecting to Qwen3.7-Plus. Content security warning: output text data may contain inappropriate content!" A following message returned a greeting with no reference to the packet. The screenshot is kept with the run. Its mechanics are unconfirmed; the warning names the output text as the object of the check.

The readers reported four disagreements in the files, of which three were defects:

1. **The fifth maker-count state mixed two axes** (Perplexity, Qwen). It read "governing_hypothesis_held; reception documented independently", a value outside the ontology's maker-count axis that joined an establishment value to it. v0.4 types every state on both axes: #1658 and #1733 are each one_self_dividing_maker with establishment governing_hypothesis, and #1733's note records that the reception history is documented independently of it.
2. **#1590 was both a Peripatetic member and a join** (ChatGPT, Perplexity), where the other five joins are members of neither list. v0.4 keeps joins apart from the membership lists; a join carries both clusters by its joins edges.
3. **Licensed dimensions without a stated reading** (Perplexity). The relation policy names scope, identity and history, which the state axes did not enumerate. The ontology now states which part of a claim each dimension reads.

The fourth, `one_offered_as_reading` standing in the vocabulary and in no dated state (ChatGPT, Perplexity, Qwen), is the state of a claim: #1576 offers one maker as a reading beside its record's state, two not established. The ontology now says so, and the #1576 state carries the note. T16 now also tests that joins stand apart from cluster members and that every dated state lies on the ontology's axes; run on the v0.3 build it fails at both.

**Left for a later version.** SHACL shapes for the graph; per-record pointers from each constituent record page to the kernel (a site-wide template change, to be proposed separately); an interface of its own for each body beyond its rule and unit.

## 7. A correction to the map found in building

The map's draft (EA-MPAI-ORTHONYM-01 v0.1, §7.7 and §11) wrote "#1658 generalizes #123", "#1658 generalizes #1588" and "#1658 generalizes #1603". Under #1529's direction a failure travels from the source of a `generalizes` edge to its target, and #1658's production model rests on #1588, #1583 and #1603; so the edges run into #1658. #1658 stands to #123 as `interprets`, which licenses nothing: the production model fills #123's position-structure, and #123's own words stand at its date. The kernel carries the corrected edges; the map's draft is to be corrected to match before either is deposited.

## 8. The first instance: EA-HK-ORTHONYM-01 v1.0

Built 8 November 2026 from `data/registry.json`, `data/EA-WG-CAPTURES-01.json` and the first seating of each record in the repository's history; the two registries are hashed in `11-integrity.yaml`. Counts, from `10-verification.json`:

- 40 records in six strata, read latest first, and 3 external records referenced by `supersedes` edges;
- 4 positions;
- 56 claims: 5 withdrawn originals, kept; 12 bearing on the received many-maker reading;
- 136 edges;
- 16 captures;
- 124 events across the two timelines;
- 10 lines of research.

Verification: all 16 structural tests pass. Back-projection v0.1 gives scope A 1.0 and scope B 1.0. That establishes structural presence only; reconstructive validity is v1.0, run by a reader on scope A: the first runs, on v0.2, gave 0.545, 0.909 and 0.455 (§6.3); the second, on v0.3, gave 1.0, 1.0, 1.0 and 0.909, a mean of 0.977 (§6.5).

## 9. Governing sentence

A framework's parts carry the path to its whole, and the whole is rebuilt from any of them with each part's claims kept at the grain and the date its record gave them.
