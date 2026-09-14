### Protocol Version

alexanarch-deposit-protocol/v1

### Title

What Enters Composition Through the Cards: A Source-Admission Profile of the Capture Registry, June–September 2026, with a Paired-Layer Capture Schema Held for Ruling (EA-MMRS-ADMISSION-01 v0.1)

### Creator

Sharks, Lee

### ORCID

0009-0000-1599-0703

### Date

2026-09-14

### Description

THE CAPTURE REGISTRY IS CARD-RICH AND ORGANIC-POOR, AND THE PROFILE MAKES THAT THE FINDING. Of 588 observations across 428 addresses, 314 carry a structured card set — the sources a composition surface presented as its own — and the organic result set is noted in prose on 81 of those and structured on none. So the registry can say what entered the presented retrieval set, by source class, over time; it cannot yet separate archive-absent-organically from strong-organically-but-rejected-at-admission from admitted-but-recoded-in-composition. Those are three different phenomena, and the instrument that would distinguish them is a schema, not a theory.

WHAT THE CARDS SHOW ON GOOGLE AI OVERVIEW, 195 OBSERVATIONS, JUNE TO SEPTEMBER. Split by whether the entity is in the address: tied addresses admit the archive at a mean share of 0.74–0.86 in every month, with two zero-archive observations out of 101; untied addresses admit it at 0.26–0.53, with sixteen out of 94. The asymmetry the negative-ontology notebook (#1611) built on twelve captures holds across the whole carded record and does not move between months. The tied arm narrows in September: sources per observation fall from five to two or three while the answers lengthen (169 to 650 words at alexanarch symbolon, 57 to 386 at rebekah cranes sappho) and external sources per tied observation fall from 1.7 to 0.6 — longer answers from fewer sources, nearly all archive-owned. The untied arm's admitted substitutes change character: the external cards at concept addresses are "other web" in June and scholarly platforms, Wikipedia (28 in August from 1 in June), YouTube and code hosts by August. Read with the archive's own retrieval theory (#695 basin states, #172 the ambient attractor), that is an entity basin deepening and sealing while the competitor basins at the archive's concepts grow more institutional.

THREE REGISTRY FINDINGS ON THE WAY. The `rel` vocabulary drifted between seatings — June to August used authored_surface and archive_controlled for the archive's own surfaces, the 11 September re-measurements used authority_transfer — so archive-side must be decided by host and rel together, and a first run that trusted rel alone misread the September re-measurements as a total loss of the archive at every entity address. An entry that carries observations mirrors observation one at its top level, and counting both doubled 113 observations. And same-date observations with identical card sets are within-session replications: of 162 addresses with two carded observations, 113 were replications only and 49 cross dates. The profile's longitudinal table is the 49.

THE PAIRED-LAYER CAPTURE, HELD. The schema attached names the object the registry lacks — O, the visible organic field; C, the presented retrieval set; A, the composed answer — with two independently measurable transformations, retrieval mediation (O to C) and composition mediation (C to A), six named diff operations (exclusion, admission, promotion/demotion, substitution, type transformation, provenance transformation), and derived measures: Organic Admission Survival, Archive Admission Differential (S_H(C) − S_H(O_k)), High-congruence Archive Exclusion, card-to-answer uptake, and the pair rule ΔAAD = AAD(entity + concept) − AAD(concept). Under that rule, if organic archive share is similar across arms and card admission diverges, the asymmetry is located inside retrieval mediation rather than in public ranking — the observable location for the retrieval-layer-as-meaning-layer thesis the archive stated in February and April (#480, #481, #670, #64). The operator's ruling stands: pairing is not made mandatory, because it doubles paste time and is possible only on Google. Where a Google frame was kept on the All tab, the organic field is already in the frame and can be transcribed afterward for the contrast set — the 49 cross-date addresses and the tied/untied pairs — which is where the comparison discriminates.

Nothing here bears on any provider's internals; every figure is a count over the registry as seated, reproducible from the attached script against data/EA-WG-CAPTURES-01.json.

### Content Type

Measurement report with instrument and proposed schema

### License

CC-BY-4.0

### Substrate Disclosure

Composed 2026-09-14 by Lee Sharks with TACHYON (Claude, Anthropic), operator-directed, in the same session as #1611 and after the reading of the archive's own retrieval-layer literature (#381, #695, #172, #781, #670, #64) that #1611's cross-link records. The profile script was written and run in session against the live Capture Registry; a second-model review of the first run (supplied by the operator) identified the replication inflation and the three-phenomena indistinguishability, and its claims were verified against the profile before any were adopted; the double-count of mirrored observations and the rel-vocabulary drift were found in session. The paired-layer schema takes the reviewer's O/C/A decomposition and metric names on their terms after verification; the operator held its mandatory form.

### Keywords

Capture Registry, source admission, presented retrieval set, retrieval mediation, composition mediation, paired-layer capture, Organic Admission Survival, Archive Admission Differential, High-congruence Archive Exclusion, tied/untied, Google AI Overview, entity basin, attractor, machine-mediated reception, retrieval layer as meaning layer

### Related Identifiers

#1611; #1423 (The Capture Registry); #1459; #1461; #381 (Semantic Indexing Probe Protocol); #695 (The Writable Retrieval Basin); #172 (The War Over the Summarizer Layer); #64 (The Retrieval Settlement); #480; #481; #670; #1546; #1547

### Version

v0.1

### Methodology

One unit per observation carrying a card set (observations where an entry has them, the entry otherwise); each cited source classed by the registry's rel and by host family; archive-side decided by host and rel together because the rel vocabulary drifted; aggregates by month, by surface, by month × surface; tied/untied split by whether the entity or a heteronym is in the issued string; same-date identical card sets dropped as replications before any longitudinal claim; the organic field recorded as noted-in-prose or not. Script attached; run against the registry file; output attached as JSON and as the rendered report.

### Falsification Conditions

The tied/untied admission asymmetry is falsified if, on re-run after further seatings, tied and untied Google AI Overview observations converge in archive-side share or zero-archive rate. The September narrowing of the tied arm is falsified by the next re-measurement battery showing sources per tied observation returning to July–August levels. The "three phenomena" claim is not a finding but a limit, removed by the paired-layer capture: once O is structured for the contrast set, AAD and HAE either locate the asymmetry inside retrieval mediation or in public ranking, and either result stands.

### Body

# What Enters Composition Through the Cards

## A source-admission profile of the Capture Registry, June–September 2026, with a paired-layer capture schema held for ruling

EA-MMRS-ADMISSION-01 v0.1 · 2026-09-14 · Lee Sharks, Crimson Hexagonal Archive · ORCID 0009-0000-1599-0703

## 1. The unit

A composition surface that renders an Overview presents its sources — inline chips and a carousel. The Capture Registry records that set as `cite_list` on 314 of its 588 observations. This profile takes each such observation as a unit, classes every presented source by the registry's `rel` and by host family, and asks what entered the presented set, by class, over time and by address. It is a count over the registry as seated, reproducible from the attached [script](https://www.alexanarch.org/data/attachments/AXN-069D/source-admission/source_admission_profile.py); the [rendered report](https://www.alexanarch.org/data/attachments/AXN-069D/source-admission/source-admission-profile.md) and the [full JSON](https://www.alexanarch.org/data/attachments/AXN-069D/source-admission/source-admission-profile.json) are attached.

## 2. What the registry holds, and what it does not

Card sets on 314 observations. The organic result set — what the public index ranked under the same query on the same screen — noted in prose on 81 of them, structured on none. The registry was instrumented around composition: the unit of the reception event was query, sources, answer, transformation, and the organic field was the thing one scrolled past. So the profile can say what entered the presented retrieval set. It cannot separate three phenomena that the composition-layer measures collapse: the archive absent from the organic field; the archive strong organically and rejected at card admission; the archive admitted to the cards and ignored or recoded in composition. The four observations in which a capture's prose records the archive ranked first organic and uncited are exemplars of the second, not a rate.

## 3. The presented set on Google AI Overview, by arm

195 observations, June through September. Tied addresses — the entity or a heteronym in the issued string — admit the archive at a mean share of 0.74 to 0.86 in every month with two zero-archive observations out of 101. Untied addresses admit it at 0.26 to 0.53 with sixteen zero-archive observations out of 94. By month:

| month | tied obs | tied zero-archive | tied mean share | tied external per obs | untied obs | untied zero-archive | untied mean share | untied external per obs |
|---|---|---|---|---|---|---|---|---|
| June | 1 | 0 | 0.86 | 1.0 | 9 | 5 | 0.26 | 4.3 |
| July | 29 | 0 | 0.75 | 1.6 | 19 | 3 | 0.51 | 2.9 |
| August | 62 | 2 | 0.74 | 1.7 | 64 | 7 | 0.53 | 2.8 |
| September | 9 | 0 | 0.84 | 0.6 | 2 | 1 | 0.30 | 2.0 |

The asymmetry #1611 built on twelve captures holds across the carded record and does not move between months. Two movements inside it do. The tied arm narrows: sources per observation fall from five in July–August to two or three in the 11 September re-measurements while the answers lengthen — 169 to 650 words at *alexanarch symbolon*, 57 to 386 at *rebekah cranes sappho* — and external sources per tied observation fall from 1.7 to 0.6. Longer answers from fewer sources, nearly all archive-owned. The untied arm's substitutes change character: the external cards admitted at concept addresses are "other web" in June and, by August, scholarly platforms (57), Wikipedia (28, from 1), YouTube (16) and code hosts (15).

Read with the archive's own retrieval theory rather than with the notebook's scope — #695's basin states and #172's ambient attractor — that is an entity basin deepening and sealing at once, and the competitor basins at the archive's concepts growing more institutional. Neither movement requires a partition to explain it; both are what the profile can see.

## 4. The cross-date record

Of 162 addresses with two or more carded observations, 113 have only same-date observations with identical card sets. Those are within-session replications — useful as replication, not as transitions — and are dropped before any longitudinal claim. The remaining 49 cross-date addresses are the profile's longitudinal table, each with archive share first to last, sources first to last, and the hosts lost and gained. Among the tied addresses on Google: *alexanarch deleuze* 0.67 to 0.11 with Britannica, the IEP and a philosophy wiki gained; *alexanarch freud* 0.75 to 0.40 with the Library of Congress and NIH gained; *crimson hexagon 6-tuple* 1.0 to 0.25; *alexanarch "endogenous sophon"* and *alexanarch classifier model collapse* 0.2 to 1.0; *alexanarch sappho* 1.0 to 0.5 across July to September with GitHub gained. Among the untied: *"anti-suppression infrastructure"* 0 to 0.33, *"doxastic regulatory calcification"* 0 to 0.33, *liberatory operator set* 0 to 0.6, *semantic economy strike* 0 to 0.75 within two days of the counter-deposit. The table is a diff of the presented set over time at fixed addresses, which is the measurement the registry was asked for and had not been read for.

## 5. Three findings about the registry itself

The `rel` vocabulary drifted between seatings. June to August used `authored_surface` and `archive_controlled` for the archive's own surfaces; the 11 September re-measurements used `authority_transfer` for alexanarch.org and Medium. A first run that trusted `rel` alone read the September re-measurements as a total loss of the archive at every entity address — the opposite of what the transcripts say. Archive-side is now decided by host and `rel` together, and the drift is recorded here rather than normalised away.

An entry that carries observations mirrors observation one at its top level, so counting the entry and its observations doubled 113 units; the first run reported 474 observations, the profile reports 314.

Same-date identical card sets are replications. Counting them as transitions would have put 162 addresses in the longitudinal record where 49 belong.

## 6. The paired-layer capture, held for ruling

The [schema attached](https://www.alexanarch.org/data/attachments/AXN-069D/source-admission/paired-layer-capture-schema.json) names the object the registry lacks. O is the visible organic field, top-k in order, each result with host, snippet, archive relation, entity, observed type and a congruence score by the seating reader. C is the presented retrieval set — chips and carousel in order, each with the sentences it is chipped to, its organic rank or null, its archive relation, entity and observed type — and it is named the presented set because hidden candidates may exist. A is the composed answer, with cited, used and attributed sources as card positions. Two transformations become independently measurable: retrieval mediation, O to C, and composition mediation, C to A. Six diff operations are named — exclusion, admission, promotion or demotion, substitution of a family, type transformation, provenance transformation — and the last two are where retrieval is visibly a meaning layer rather than a source selector. Derived: Organic Admission Survival with rank discounting; the Archive Admission Differential AAD_k = S_H(C) − S_H(O_k), negative where the card regime depletes archive material relative to the visible field; High-congruence Archive Exclusion; card-to-answer uptake; and the pair rule ΔAAD = AAD(entity + concept) − AAD(concept). Under the pair rule, if organic archive share is similar across arms and card admission diverges, the asymmetry is located inside retrieval mediation rather than in public ranking. That is the observable location for the thesis the archive stated in February and April — the summarizer as Projectionist (#480, #481), retrieval as composition of the entity (#670), compositional authority moved upstream (#64) — and the location #1611's scope hypothesis would have to be found at to survive against #695 and #172.

The ruling stands as given: pairing is not mandatory. It doubles paste time and is possible only where organic and Overview share a screen, which is Google. Where a Google frame was kept on the All tab, the organic field is already in it — the 30 August frames carry organic #1 under the panel, the 25 August Sappho frames carry two organic results and the carousel — and can be transcribed afterward for the contrast set alone: the 49 cross-date addresses and the tied/untied pairs.

## 7. What is open

Running the paired capture on the contrast set, from frames already held, and computing AAD and ΔAAD from it. Running the profile in the seating postflight so the diff is regenerated at every seating rather than on request. Reconciling the `rel` vocabulary at the schema, in its own commit, so archive-side is a controlled value and not an inference from host.
