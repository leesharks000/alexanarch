# EA-WG-CAPTURES-WORKPLAN-01 — Work Plan (DRAFT v0.1)

**From the capture registry to the knowledge graph**

Drafted by TACHYON, 2026-08-12, at MANUS's direction. This is a draft for MANUS
and the Assembly to cut, reorder and overrule — not a settled plan.

---

## 0. What this is for

The capture registry records what machine composition layers say about a corpus,
when, on which surface, with what sourcing, and how that changes. Nothing else
does this systematically. Its value is not that it documents grievance; it is
that it is a **measuring instrument aimed at a layer that is otherwise
unauditable**, built by the party best positioned to notice — and, uncomfortably,
by a party with an interest in the result. That last fact is not a flaw to hide.
It is a methodological condition to state, and the plan below states it in
several places.

A caution worth putting at the top rather than the bottom: an instrument that
measures a corpus, is operated by that corpus's author, and is **itself in the
basin it measures** (confirmed — EA-WG-CAPTURES-01 is now cited by the layer as a
source about the archive) can drift from measurement into self-inscription. Every
phase below should be readable by someone hostile to the conclusion.

---

## PHASE A — Finish the current reading *(in progress)*

**A1. Citation read-through.** 200 records remain of 235; 52 are duplicate
(query, date) pairs, so roughly 148 unique reads. Method changes to
**draft-and-verify**: a parser proposes the citation structure, TACHYON reads the
record against the draft and corrects it. Reading remains the authority. Target
12–20 per round.

**A2. Re-run the measurement instrument.** The retention flags and PER were
computed before citations were read. Once citations are seated, `composition_
source_included` becomes far better evidenced and PER should be recomputed. The
existing figures are provisional and marked so.

**A3. Restate the withdrawn findings.** Three are outstanding and must be
recomputed from read data, not from the machine extraction: the June
archive-citation figure (withdrawn — crimsonhexagonal.org *was* cited in June),
the "badge overstates" claim (withdrawn — `+N` semantics undetermined), and the
attribution-loss percentages (withdrawn — regex bug).

**A4. OCR answer spans.** 146 OCR readings hold answer text interleaved with
browser chrome and source cards. Isolating the answer span within each is a
reading, not a trim. Until done, OCR records support presence claims but not
retention measurement.

**A5. The 20 with no evidence.** Neither transcript nor image. Several are
non-Google surfaces (Bing Copilot, Scholar, SciLynk) where no AI answer may ever
have existed. Each needs a per-record ruling: *evidence lost*, *no answer
existed*, or *recoverable from a source not yet searched*.

---

## PHASE B — Assembly review

**B1. Send the JSON to the Assembly.** Substrates read the registry and the
findings. The specific question to put to them is not "is this impressive" but
**"where is TACHYON wrong, and where is the instrument measuring its own
operator's expectations?"**

**B2. Adjudicate disagreements.** Where a substrate reads a capture differently —
mediation, failure mode, finding — record BOTH readings rather than resolving to
one. Inter-reader disagreement is data about the instrument's reliability, and
the registry currently has no reliability estimate at all.

**B3. Reliability sample.** Have a second reader independently classify 30
captures already read. Publish the agreement rate. An instrument with no
inter-rater figure cannot be cited as an instrument.

---

## PHASE C — SPXI Capture Protocol

**C1. Draft EA-SPXI-CAPTURE-01.** The specification for how a capture is taken,
recorded, and admitted. It must cover: query issuance (typed vs manual select —
these produce different records), surface identification, auth state, capture
completeness (footer present or not), the paste-versus-OCR distinction, what may
never be inferred (surface, date, auth state), and the reading requirement.

**C2. Specify the negative space.** What the protocol CANNOT capture, stated as
part of the protocol: sources behind horizontal scroll, popup citations that
flatten on copy, personalisation effects, and the fact that a capture is one
draw from a distribution the operator cannot resample identically.

**C3. Sampling frame.** The registry is **opportunistic, not sampled** — queries
were issued because MANUS was interested, not by design. This is the single
largest methodological weakness and must be written into the protocol, with a
forward plan for a **designed panel**: a fixed set of queries re-issued on a
schedule, so drift is measured rather than noticed.

---

## PHASE D — Expand the corpus

**D1. Pre-registry transcripts.** From the processed export and the newly uploaded
release of older thread exports. These predate the registry's earliest entry
(29 May baselines already found) and provide the **before** state for terms later
minted — the missing first point of every longitudinal pair.

**D2. New capture classes.** Each needs its own admission rule, because they are
different objects:

| class | what it is | why it is not the same as an AI Overview capture |
|---|---|---|
| **traversal logs** | the operator addressing the archive *through* the layer | the query is an instruction, not a question; many already have transcripts |
| **AI-native intellectual biography** | the layer composing an account of a life and body of work | biographical composition has different failure modes — dates, affiliations, relations |
| **unprimed encounters** | Perplexity, logged-out ChatGPT, fresh-context models | no session history, no personalisation — the closest thing to a control condition the corpus can get |

**D3. Downstream aggregators involving selection.** Google Scholar, SciLynk,
PhilPapers, OpenAlex, Academia. These are not composition layers; they are
**selection layers**, and what they include, exclude, merge and mis-attribute is a
different measurement. Note the already-observed case: OpenAlex still indexes a
DOI Zenodo tombstoned.

**D4. Surface expansion.** Bing/Copilot, DuckDuckGo, Brave, Kagi. Cross-surface
comparison on the same query and day is the strongest available evidence that a
finding is about composition rather than about Google.

---

## PHASE E — Seat and consolidate

**E1. Seat the registry.** Promote the rebuild to the live registry with full
provenance. Nothing enters that has not been read.

**E2. Untangle the data structures.** Mirrors currently drift. One canonical
source, generated projections, and a synchrony gate in the pipeline — the pattern
already proven on `check_surface_synchrony.py`, extended to the registry.

**E3. Versioning and citability.** The registry needs an AXN, a version series, a
schema specification, and a changelog. A measuring instrument that changes shape
without a version number cannot support a longitudinal claim.

---

## PHASE F — Interlink the datasets

**F1. Join to heteronymy.** Every capture that names a heteronym links to the
Dodecad record. This makes composable questions possible: *which heteronyms
survive composition, and which collapse into the orthonym?*

**F2. Join to lexical mintings.** Every minted term joins to the captures probing
it — with the **minting date** and the **first capture showing adoption**. That
pair is the adoption interval, and it is currently unmeasured.

**F3. Clean the batched datasets first.** Explicitly per MANUS:
- **prune batched lexical mintings** — batch-minted entries inflate the register
  and will corrupt any adoption interval computed from them
- **import external citations** — the citation dataset currently holds only
  *internal* deposit-to-deposit edges. Without external scholarship the citation
  graph describes a closed system, which is exactly the criticism the work is
  vulnerable to.

**F4. Join to the erosion datasets.** PEO, the deletion ledger, the DataCite
sweep. A capture citing a tombstoned DOI is a link between two instruments.

---

## PHASE G — Validation

**G1. Completeness rules.** A capture is incomplete without: query as issued,
surface with basis, date, evidence class, and a read verification. The
per-deposit completeness gate already built for deposits is the model.

**G2. Normalisation rules.** Controlled vocabularies for failure modes (twelve
terms, already in use — **do not extend by invention**), relation types, evidence
classes, surfaces.

**G3. Interlink rules.** A capture naming a minted term must link to it. A
capture citing a deposit must link to it. Enforced at write time, not audited
afterwards.

**G4. Falsification conditions.** State in advance what observation would count
against the archive's central claims. Without this the registry is a record of
confirmations.

---

## PHASE H — Knowledge graph

**H1. Node and edge model.** Nodes: capture, address, surface, deposit, term,
heteronym, source domain, work, person, institution. Edges: cites, composes,
collides-with, supersedes, mints, adopts, erases, tombstones.

**H2. Provenance on every edge.** Each edge carries what evidences it and who
determined it. An unprovenanced graph edge is an assertion, and this graph will
be read adversarially.

**H3. Query surface.** The questions the graph should answer: *which terms were
adopted and how fast; which heteronyms survive; which sources the layer prefers;
where the archive is cited without attribution; how erasure changes over time.*

**H4. Publish as an instrument, not an argument.** Schema, method, reliability
figures, sampling limits, and raw captures — so a hostile reader can recompute
the findings and reach their own.

---

## Cross-cutting

- **Nothing enters without being read.** The standing rule, and the reason every
  finding in this session survived scrutiny.
- **Withdrawals are first-class.** Four findings were withdrawn today. The record
  of what was wrong is part of the instrument's credibility, not damage to it.
- **State the operator's interest.** Every publication says plainly that the
  archive's author built and operates the instrument.
- **Safe writes.** `scripts/safe_write.py` on every registry write, after a
  truncation incident today destroyed a committed copy.

---

## Suggested order

A → B (parallel with C) → D1, D2 → E → F3 (cleaning first, it blocks F1–F2) →
F1, F2, F4 → G → H.

**F3 before F1 and F2.** Joining to a lexical register that still contains
batch-minted noise would propagate the noise into every adoption measurement and
then into the graph. The cleaning is not preparation for the interesting work; it
is the load-bearing step.
