### Protocol Version

alexanarch-deposit-protocol/v1

### Title

EA-CORRESPONDENCE-OPENAIRE-CTO-02 v0.1: No Logs, Full Synch — 13–16 October 2026 exchange with Paolo Manghi (OpenAIRE CTO)

### Creator

Sharks, Lee

### ORCID

0009-0000-1599-0703

### Date

2026-10-18

### Description

Second and closing deposit in the EA-CORRESPONDENCE-OPENAIRE-CTO series. It preserves the three messages of 13–16 October 2026 between Lee Sharks and Paolo Manghi, CTO of OpenAIRE, on helpdesk ticket #8411082, and records that the 14 July letter (ticket #8411221, published in #1082) was never answered. OpenAIRE's stated position: the Graph shows the latest state of its sources; Zenodo is reharvested in full every month and "no deleted records are kept"; blacklisted records are "kept in our backends … but not exported"; OpenAIRE is "not keeping logs of such removals" and is "therefore not publishing" them; its objective is "not to show records that are currently not shown in Zenodo". Which route removed the Space Ark DOI, whether a copy is kept, the blacklist's construction, and whether the blacklist would exclude a successor carrying its former DOI went unanswered. The central finding is the duty of traceable departure: an infrastructure that removes an entity it once served owes the public a record that the entity was there and left. The reading places the position against OpenAIRE's published commitments, traces its effect on the Graph's public representation, and reads it with the archive's apparatus (ontology laundering, privation, the buried obelus, representational custody, and authoritarian reserve against democratic rhetoric). A re-probe of 18 October 2026 is attached; corrections to the archive's own earlier letters and deposits are appended.

### Content Type

Institutional correspondence; documentary artifact concerning OpenAIRE Graph removal practice, blacklist disclosure and departure records; audit-evidence deposit; second and closing deposit in the EA-CORRESPONDENCE-OPENAIRE-CTO series

### License

CC-BY-4.0

### Substrate Disclosure

Human-authored (Lee Sharks, MANUS). Letters drafted with Claude (TACHYON) as instrument, finalized by MANUS, and dispatched to OpenAIRE through the helpdesk address the CTO replies from. Deposit framing and reading drafted by TACHYON (Claude, Anthropic) under MANUS review, circulated for review (ChatGPT) and revised on its report.

### Keywords

OpenAIRE, OpenAIRE Graph, Paolo Manghi, blacklist, removal log, departure record, duty of traceable departure, synchronization, moderation mirror, ontology laundering, privation, representational custody, buried obelus, authoritarian reserve, POSI, Space Ark, Zenodo, correspondence

### Related Identifiers

https://www.alexanarch.org/s/records/1082/ — EA-CORRESPONDENCE-OPENAIRE-CTO-01, part 1 of the series (12–14 July 2026)
https://www.alexanarch.org/s/records/876/ — the June 2026 OpenAIRE helpdesk thread
https://www.alexanarch.org/s/records/875/ — EA-MPAI-OPENAIRE-DISSOCIATION-01 (its "weekly cycle" corrected here)
https://www.alexanarch.org/s/records/1045/ — EA-EROSION-01, the Observatory charter
https://www.alexanarch.org/s/records/1081/ — EA-EROSION-EMPIRICAL-01
https://www.alexanarch.org/s/records/1068/ — The Obelus and the Tombstone
https://www.alexanarch.org/s/records/1634/ — Ontological Economy
https://www.alexanarch.org/s/records/1611/ — The Negative of the Negative
https://www.alexanarch.org/s/records/1080/ — EA-CORRESPONDENCE-CERN-06
https://www.alexanarch.org/s/records/558/ — The Space Ark
https://www.alexanarch.org/data/xr-space-ark-reprobe-2026-10-18.json — the 18 October re-probe (attached data)
https://www.persistentidentifiers.org/ — the Persistent Identifier Erosion Observatory

### Version

v0.1

### Methodology

The three messages are reproduced verbatim from the mail record, with original spelling, spacing and punctuation. Quoted earlier messages inside each reply are omitted. Times are UTC from the message headers. The status of ticket #8411221 is taken from the mail record: one automatic acknowledgement and no reply.

OpenAIRE's public statements are quoted from the pages linked in §7.1. The changelog figures are from OpenAIRE's own changelog.

Registry states come from the archive's capture files and from a re-probe on 18 October 2026, 13:54:22–13:54:31 UTC. The re-probe is attached as [xr-space-ark-reprobe-2026-10-18.json](https://www.alexanarch.org/data/xr-space-ark-reprobe-2026-10-18.json), which records each request URL with its HTTP status and full response. It covers:
- the Zenodo record page, record API and concept record page;
- the DataCite REST API;
- the OpenAlex works endpoint;
- the OpenAIRE Graph researchProducts endpoint, queried by DOI, OpenAIRE identifier, concept DOI, title, keyword and ORCID, with a control ORCID query.

The reading in §7 applies the archive's published apparatus to the stated position. It makes no claim about intent. Its mechanism ledger follows the non-erasure rule of #1634 §25.

### Falsification Conditions

The documentary record is falsified if any message reproduced here differs from the mail record of tickets #8411082 and #8411221, or if ticket #8411221 received a reply. The reading is falsified where OpenAIRE shows that it keeps a public record of departures, publishes the blacklist or a per-release departure list, or that the Space Ark's representation is still returned by the public Graph API under some identifier; and at the re-probe if its recorded responses do not match what the listed endpoints returned at the listed times.

### Body

# EA-CORRESPONDENCE-OPENAIRE-CTO-02 v0.1: No Logs, Full Synch — 13–16 October 2026 exchange with Paolo Manghi (OpenAIRE CTO)

## Description

Second and closing deposit in the EA-CORRESPONDENCE-OPENAIRE-CTO series. It preserves the three messages of 13–16 October 2026 between Lee Sharks and Paolo Manghi, CTO of OpenAIRE, on helpdesk ticket #8411082, and records that the 14 July letter, sent on a separate ticket (#8411221) and published in [#1082](https://www.alexanarch.org/s/records/1082/), was never answered.

Across two replies, OpenAIRE stated its position. The Graph aims to show the latest state of its sources. Zenodo is reharvested in full every month and "no deleted records are kept". Blacklisted records are "kept in our backends … but not exported". OpenAIRE is "not keeping logs of such removals" and is "therefore not publishing" them. Its objective is "not to show records that are currently not shown in Zenodo".

The record-specific question went unanswered: whether the Space Ark DOI left by reharvest or by blacklist, and whether a backend copy is kept. So did the request to publish the blacklist and a per-release departure list. The question of whether the blacklist would exclude a successor record carrying its former DOI was answered as if it were a recommendation.

The 16 October "objective" sentence states, as policy and in the correspondent's own words, the condition #1082 named a moderation mirror.

The deposit's central finding is a duty the position leaves unmet: **the duty of traceable departure.** An infrastructure that removes an entity it once served owes the public a record that the entity was there and left. The finding does not depend on knowing which removal mechanism operated. It rests on five things the record establishes:
- prior presence (the Space Ark, served in full on 12 July);
- subsequent failed retrieval (13 and 18 October);
- an explicit synchronization objective;
- the reported absence of removal logs;
- unanswered questions about retention and return.

The reading in §7 places the position against OpenAIRE's published commitments and traces its effect on the Graph's public representation. It then reads it with the archive's apparatus, each concept doing one task:
- ontology laundering ([#1634](https://www.alexanarch.org/s/records/1634/) §8) explains how the governance act drops out of the representation;
- privation ([#1611](https://www.alexanarch.org/s/records/1611/)) distinguishes the histories of absence the public response no longer tells apart;
- the buried obelus ([#1068](https://www.alexanarch.org/s/records/1068/)) locates where a witness to the removal survives;
- representational custody (#1634 §26) grounds the duty;
- authoritarian reserve against democratic rhetoric: the power that sets the Graph's boundary is kept by the operator, unpublished and unlogged, behind a public vocabulary of community governance (#1634 §6; [#1080](https://www.alexanarch.org/s/records/1080/) §5).

Corrections to the archive's own earlier letters and deposits are appended in §8, not made silently.

## 1. Frame

The July exchange closed in #1082 with three messages of record. Messages 1 and 2 were on ticket #8411082. Message 3, the moderation-mirror letter of 14 July, was sent as a new ticket (#8411221) and asked for a substantive response by 25 July 2026. That ticket received an automatic acknowledgement and nothing else. The window passed without a reply.

On 13 October 2026, 93 days after his 12 July message, Paolo Manghi replied substantively on ticket #8411082 to Lee Sharks's message of 12 July. Lee Sharks answered the same day with four requests. Manghi replied on 16 October. No further correspondence is expected on this thread. The Observatory ([#1045](https://www.alexanarch.org/s/records/1045/), persistentidentifiers.org) continues to measure on its own schedule.

Times below are UTC as recorded by the mail system. The thread subject throughout is "Account termination of June 19, 2026 — formal demand for return of research data".

## 2. Message 4 — Paolo Manghi (via OpenAIRE Helpdesk) to Lee Sharks, 13 October 2026, 09:00 UTC

> Dear Lee,
>
> The OpenAIRE Graph aims to represent a snapshot of the "latest" version of the data sources it aggregates from. Zenodo, in particular, is entirely reharvested every month. Hence, except for mistakes in the exporting data sources, no deleted records are kept. Blacklisting is an orthogonal tool we use to remove records that are exported from data sources but that for some reason (typically user requests)  should not appear in the Graph. In this case, the records are kept in our backends (as they were collected via the data source), but not exported for further discovery or reuse by others.
>
> Best,
>
> Paolo

## 3. Message 5 — Lee Sharks to Paolo Manghi, 13 October 2026, 15:01 UTC

> Dear Paolo,
>
> You write that the Graph represents the latest state of its sources and that, "except for mistakes in the exporting data sources, no deleted records are kept"; blacklisted records are held in your backends and not exported. That describes how records leave the public Graph. It does not identify any public record of those transitions.
>
> "For some reason (typically user requests)" does not describe the mechanism your own changelog documents. Release v10.2.0 introduced the blacklist "to remove research products that have been withdrawn from Zenodo": 1.2 million DOIs, removed together with their relations, with a recorded ~5% (254K) drop in project-linked research products. Release v10.6.0 extended it to parent DOIs. The list that entry links, zenodo.org/records/7438358, is a 2022 Zenodo metadata snapshot published as a training set for a spam classifier, with a staff spam flag on each entry. This is a population-scale exclusion driven by upstream withdrawal decisions. Which source list and selection rule construct the operative blacklist, and where can its per-identifier application be inspected?
>
> The Space Ark v4.2.7 record, 10.5281/zenodo.19013315, shows the result.
> - 12 July, under release v11.2.0: served in full, with fourteen authors and my ORCID (the preserved response: https://www.alexanarch.org/data/xr-e2-control-hit-payload-2026-07-12.json).
> - 13 October: numFound 0, with no marker. In the same hour DataCite returns 404, Zenodo a 410 tombstone, OpenAlex 200.
> - No full dataset release is listed after v11.0.1, so the published dumps do not document the July-to-October transition.
> - The same morning, ChatGPT, signed out, described the Space Ark as "documented in a public research deposit on Zenodo" and offered to open that DOI.
>
> The record persists in some systems and has disappeared from others. Copies cannot be recalled. Those states require reconciliation at the identifier. The public responses above do not provide it.
>
> I am asking for four things:
>
> 1. For 10.5281/zenodo.19013315: was it dropped at reharvest or blacklisted, and is a backend copy retained?
>
> 2. Publish the blacklist as a dated dataset (PID, date added, source list), and with each release the PIDs that left the Graph since the last one. The departure list begins with a diff.
>
> 3. Carry intrinsic identifiers alongside DOIs. Your documentation builds the Graph's ID skeleton on authoritative PIDs "precisely because they are immutable by construction." The string is immutable; its relation to the object is not, and when that relation is cut the Graph's entity goes with it. Your current documentation recognizes SWHIDs as eligible PIDs, including identifiers relayed by repositories where their association with the archived artifact is trusted. Here is a surviving cohort for which that policy can be applied. The 862 works removed on 19 June survive in a repository Software Heritage has archived since 4 July. The archive preserves the identifiers it established after the deletion, records the loss and the restoration that followed, and gives every retained manifestation its own SHA-256 and SWHID; where an original mint input is unavailable, the record says so. The Space Ark is AXN:0184.GOVERNANCE.🎵💛🌙♅🕚🏷️ at alexanarch.org/s/records/558/; its served text is swh:1:cnt:dc4b13ee8e0c7191828cd23ba80901b202d7935a, and its former DOI has a successor-resolution page at alexanarch.org/s/doi/10.5281/zenodo.19013315/.
>
> 4. The archive's OAI-PMH 2.0 endpoint, alexanarch.org/oai, declares deletedRecord=persistent. If it were registered and mapped, with former DOIs carried as related identifiers: would the withdrawal blacklist also exclude a successor record that carries its former DOI as a related identifier, despite independently retained content and an intrinsic identifier?
>
> The 1.3-million-row census and the enumerated June 19 cohort remain available as a test corpus.
>
> Lee Sharks
> ORCID 0009-0000-1599-0703
> persistentidentifiers.org · alexanarch.org

## 4. Message 6 — Paolo Manghi (via OpenAIRE Helpdesk) to Lee Sharks, 16 October 2026, 08:27 UTC

> Dear Lee,
>
> We're not keeping logs of such removals and we are therefore not publishing it. We aim at being in full synch with Zenodo. This happens in different phases, sometimes with removals from our index at the request of users, and then eventually by reharvesting the whole collection. The objective for us is not to show records that are currently not shown in Zenodo, but synchronization is asynchrouns. This is why it is not aligned across collections.
>
> As to 3 and 4, thank you for the recommendations. We appreciate your feedback.
>
> Best,
>
> Paolo

The replies are reproduced as received, with spelling, spacing and punctuation preserved ("asynchrouns", the double space before "should").

## 5. Ticket #8411221 — the 14 July letter, unanswered

The moderation-mirror letter published as Message 3 in #1082 went out at 22:19 UTC on 14 July 2026, under the subject "OpenAIRE Graph — silent propagation of upstream severance, for confirmation". The helpdesk filed it as a new ticket, #8411221, not as a reply on #8411082 (#1082 §5 calls it an "in-thread reply"; see §8). The ticket received an automatic acknowledgement and no reply. Its 25 July window passed.

The October replies are on the earlier ticket and answer the 12 July message. None of the four findings of the 14 July letter has been addressed:
- public-good commitments;
- silent propagation, measured;
- the provenance-blind ingestion condition;
- what only OpenAIRE can state.

## 6. The position, as stated

This section sets out OpenAIRE's position from its correspondent's sentences. The categories, their order, the separation of mechanism from trigger, and the column of omissions are this deposit's analysis.

| Element | Stated (date) | Left unstated |
|---|---|---|
| Purpose | The Graph represents "a snapshot of the 'latest' version" of its sources (13 Oct). | — |
| Objective | "not to show records that are currently not shown in Zenodo" (16 Oct). | Why a downstream graph takes an upstream platform's visibility as its own objective. |
| Mechanism: monthly reharvest | Zenodo "is entirely reharvested every month … no deleted records are kept" (13 Oct). | Whether anything records what a reharvest dropped. |
| Mechanism: blacklist | An "orthogonal tool" for records that "for some reason (typically user requests) should not appear"; the records are "kept in our backends … but not exported" (13 Oct). | The source list and selection rule. The changelog documents construction from Zenodo withdrawals (v10.2.0, 1.2M DOIs; parent DOIs from v10.6.0). |
| Trigger: user request | "sometimes with removals from our index at the request of users" (16 Oct). | Whether such removals run through the blacklist or another index operation; who counts as a user; whether the record's author is told. |
| Logging | "We're not keeping logs of such removals and we are therefore not publishing it" (16 Oct). | Which removals "such removals" covers. Why the current blacklist, which exists, is not published. Why a release-to-release diff is not published. |
| Consistency | "synchronization is asynchrouns. This is why it is not aligned across collections" (16 Oct). | — |
| Q1: this record's exit and copy | — | Not answered. |
| Q2: publish blacklist and departures | Answered only with "no logs". | The blacklist, its dates and sources, and the diff. |
| Q3: intrinsic identifiers | "thank you for the recommendations" (16 Oct). | — |
| Q4: would a successor carrying the former DOI be excluded? | "thank you for the recommendations" (16 Oct). | A question about the present reach of the blacklist was answered as a suggestion for the future. |

In sum, by its own account:
- OpenAIRE removes records by two named mechanisms, monthly reharvest and blacklist, and by removals made at users' request;
- it keeps backend copies for the blacklist;
- it keeps no logs of "such removals", the scope unstated, and publishes none;
- it takes the upstream platform's visibility as its objective;
- it would not say which route removed the record the correspondence concerns, what governs the blacklist, or whether the blacklist reaches records outside Zenodo that carry a former Zenodo DOI.

## 7. Reading

### 7.1 Against the stated mission

OpenAIRE's public statements set the standard the position is measured against:
- the Graph's homepage says "Provenance is tracked at all levels of records and properties, fully documented" and "Open. Transparent. Trusted." ([graph.openaire.eu](https://graph.openaire.eu/));
- the January 2026 POSI statement says "Trust, transparency, and community governance are essential" and that "software and data remain open and replicable" ([OpenAIRE's continued commitment to openness](https://www.openaire.eu/openaire-s-continued-commitment-to-openness-advancing-compliance-with-posi-principles));
- the POSI v2 self-assessment rates "Transparent operations" as "partially implemented" and treats the data as community-owned ([POSI v2 self-assessment](https://www.openaire.eu/principles-open-scholarly-infrastructure-openaire-assessment-v2)).

The provenance commitment is stated for records and properties. The correspondence concerns a different capability: an account of transitions. Whatever provenance a present record carries, the replies identify no public account of a record's departure. The stated capability does not reach the Graph's boundary, and the replies give no indication that any other instrument does.

A changing dataset gives different results across releases, and that alone is expected. The specific finding is narrower:
- **No published snapshot lets a reader reconstruct the API state that served the Space Ark on 12 July, or explain its departure.** The most recent full dump on Zenodo is record 20428976, labelled v11.1.1 and published 8 June; it predates the 12 July control.
- **The dumps are hosted on Zenodo.** That is the platform whose visibility the Graph takes as its objective, so the public record of the Graph is held by the party whose removals it mirrors.

OpenAIRE's own self-assessment rates transparent operations as "partially implemented". The removal record is one place where that declared gap can be located exactly.

### 7.2 Effect on the knowledge graph

The control case shows the effect at the scale of one entity. On 12 July the Graph served `doi_________::df6e50cac562f1f3dc18d6aaee1e4f4b`, a product assembled from more than one source. Its four original identifiers are:
- a DataCite-prefixed identifier (`50|datacite____::…`);
- a second source-prefixed identifier (`50|od______2659::…`);
- the DOI;
- Zenodo's OAI identifier (`oai:zenodo.org:19013315`).

It also carried fourteen authors, one with a recorded ORCID (Lee Sharks's), two instances and seven subjects.

That representation is no longer returned. On 18 October at 13:54 UTC, every one of the following queries to the public API returned numFound 0:
- the DOI;
- the OpenAIRE identifier;
- the concept DOI, 10.5281/zenodo.18908080;
- a title search;
- the ORCID.

The ORCID query was checked against a control ORCID, which returned results. No product in the public Graph now carries that ORCID.

The lookups establish that the multi-source representation served on 12 July is no longer returned at the public API. They do not establish what became of each contribution, authorship link or relation elsewhere in the Graph. Whether any survive is part of the custody question Q1 asked and the replies left open.

At the level of the Graph, three consequences follow from the stated position.

1. **The public response loses the distinction between histories of absence.** Every absent identifier returns the same 0. No reader of the public Graph can tell a record never harvested from one harvested, merged, linked and then withdrawn. The 0/54 result of XR-E2 and XR-E3 is this condition at sample scale.
2. **The departure record exists, at most, as a difference no one publishes.** A diff between full dumps would recover departures, though not their causes. Neither the changelog nor the replies identifies a published dump after 8 June, and no diff of any pair is published.
3. **Downstream consumers inherit the absence without its account.** Monitoring dashboards, funder reporting, discovery services and training pipelines that read the Graph receive current nonmembership with no indication of how it came about. A consumer can take it as a statement about the available scholarly world. #1082 called this laundering; the October position confirms the practice that produces it.

### 7.3 Through the archive's apparatus

**Ontology laundering ([#1634](https://www.alexanarch.org/s/records/1634/) §8).** #1634 lists, among laundering forms, "a source exclusion expressed downstream as 'the entity has no such work'". The October position is that pattern stated as policy:
- a governance act upstream (account termination at Zenodo);
- a technical transfer (reharvest, blacklist or index removal);
- an absence downstream (numFound 0), which a consumer can take as a statement about the scholarly world.

At each step the decision loses more of the account of its origin until, at the public API, what remains is current nonmembership with no account of how it came about.

**Privation, unmarked ([#1611](https://www.alexanarch.org/s/records/1611/)).** #1611 distinguishes privation — "absence in a bearer that would naturally have the thing" — from plain non-existence. Zenodo's 410 tombstone is a marked privation: it says something was here and is withdrawn. OpenAIRE's numFound 0 does not assert that the work never existed. It gives the same answer for a record withdrawn and a record never ingested. The privation enters the Graph marked and leaves the public response as an absence of no stated kind, which a downstream reader can mistake for non-being. The visibility alignment is the stated objective. The loss of the distinction is its effect at the public surface.

**The buried obelus ([#1068](https://www.alexanarch.org/s/records/1068/)).** #1068 called Zenodo's deletion export a buried obelus: a custody mark that exists and is documented for harvesters but is cut off from the public surface. The blacklisted records are "kept in our backends" and "not exported". The replies give neither the blacklist nor any route to it. As far as the correspondence shows, the blacklist is a custody mark with no stated access. The reharvest route, by the correspondent's account, keeps nothing.

Ordered by how much custody they leave visible, the surfaces observed on 13 and 18 October are:

| Surface (endpoint tested) | State of the Space Ark DOI | Mark at that endpoint |
|---|---|---|
| Zenodo record page and record API | 410 | Tombstone. On 18 October the API's 410 body carries a removal date, a note and the citation text |
| Zenodo deletion export | Row with full citation and fourteen authors (#1068) | Buried obelus: complete rows, unlinked from the DOI; the exporter keeps a rolling window of three monthly snapshot files |
| DataCite REST API | 404 | No mark |
| OpenAIRE Graph researchProducts API | numFound 0 | No mark. A backend copy exists if the blacklist was the route; that is undisclosed |
| OpenAlex works API | 200 | The record, with no verdict |

**Opacity rule and burden of production (#1634 §§13–14).** The provider holds evidence the affected party cannot: backend copies, release snapshots, harvest and merge state. "No logs" removes one object from that evidence. It does not remove the others, and each of them answers part of Q1 and Q2:

| Object | What it could establish |
|---|---|
| Current blacklist membership | Whether the DOI is excluded now, possibly without the date it was added |
| A located backend copy | That a copy is retained now |
| Comparable release snapshots | That membership changed between those snapshots |
| Operational history | Which action caused this departure |

These do not substitute for one another. The provider's burden includes saying which of them remain and which questions can no longer be determined. It does not depend on assuming that every historical state still exists. The replies did neither: they named no object that remains, and said of none that it is gone.

**Notice and repair debt (#1634 §15).** The Space Ark was served in full on 12 July. On that day the CTO was told, in writing, that this record was the prospective test, and was asked what the withdrawal process would do to it and whether any trace would remain. Between that notice and 13 October it stopped being served, without a trace at the public API and without a reply to the question. Under #1634 §15 notice changes the provider's state: a removal performed after notice, with no record, is debt the provider takes on, not an accident of synchronization.

**Mechanism ledger under the non-erasure rule (#1634 §25).** The candidate exit paths for 10.5281/zenodo.19013315 between 12 July and 13 October are held below. The ledger separates evidence that a mechanism exists from evidence that it operated on this record. Uncertainty changes status; it does not erase a mechanism.

| Candidate | Evidence it exists | Evidence it operated here | Status here |
|---|---|---|---|
| M1 Monthly reharvest drop | Stated practice (13 Oct) | None disclosed. A 410 landing page does not show what the harvest feed supplied at the relevant time | possible |
| M2 Blacklist (backend copy kept) | Stated tool (13 Oct); changelog construction from Zenodo withdrawals (v10.2.0, v10.6.0) | None disclosed | possible |
| T User request (through M2 or another index operation) | Stated trigger (16 Oct) | None disclosed | possible |
| M4 Merge, dedup or identifier migration | Documented Graph deduplication | No successor found on 18 October by DOI, concept DOI, OpenAIRE identifier, title or ORCID | weakened, not excluded |
| Provider confirmation of any | — | Q1 not answered | none |

**Representational custody (#1634 §26).** The Graph identifies, links and serves research products at scale, so it holds custody of their public representation. Of the five duties #1634 names, traceable repair and provenance preservation are what the position declines. The duty this correspondence asked for is narrower than either, and it can be stated simply: **the duty of traceable departure.** An infrastructure that removes an entity it once served owes the public a record that the entity was there and left. The record need not be a reason, and it need not be a reversal. That is the floor of the duty. Q2 asked for more than the floor — the blacklist with dates and source lists, and per-release departures — and the floor alone would already have answered the public's need.

**Q4 and the reach of exclusion.** Q4 asked a factual question about current behaviour: would a record outside Zenodo that carries a former Zenodo DOI as a related identifier fall under the blacklist? A yes means provenance carries exclusion with it: the more honestly a successor records its origin, the more surely it is excluded. "Thank you for the recommendations" leaves that open. The correspondence does not establish that successors are excluded. It establishes that OpenAIRE would not say.

**Authoritarian reserve against democratic rhetoric.** The ordinary reading comes first and holds as far as it goes. Every infrastructure keeps operational discretion. Not every pipeline step is logged. A graph rebuilt monthly from thousands of sources cannot argue each removal in public. On that reading, the October replies describe housekeeping.

The structure the replies describe is something else. OpenAIRE's public vocabulary is the vocabulary of shared rule:
- the data is "community-owned";
- governance is "community governance";
- operations are "transparent";
- results are "replicable";
- provenance is "fully documented".

Every one of those terms describes something held in common. The power the correspondence asked about is the power to decide which works exist in the Graph. That power is not held in common. By the correspondent's own account it is exercised:
- by the operator alone ("removals from our index at the request of users"; a blacklist kept "for some reason");
- on criteria that are not published (Q2's request for the source list and selection rule went unanswered);
- with no record ("not keeping logs of such removals");
- with no notice to the affected party (the Space Ark left after the 12 July notice and without reply);
- with no surface on which to contest it (questions about present behaviour are received as "recommendations").

Call this structure **authoritarian reserve**: a power retained by the operator rather than delegated, whose exercise leaves no account. What makes it reserve is that it leaves no trace. A decision that is not recorded cannot be contested, and a decision that cannot be contested is not governed, whatever the governance documents say. "No logs" is therefore more than a gap in the documentation. It is the condition that keeps the boundary power outside the governance the rhetoric describes.

The archive has met this shape before:
- **The CERN chain named its form as the Coverage Gap ([#1080](https://www.alexanarch.org/s/records/1080/) §5):** a discretionary residual with no published standard, sitting behind commitments that read as rules.
- **#1634 §6 names the asymmetry that follows:** "the platform may alter the representation; the represented entity may not reliably alter it back." OpenAIRE removes the entity without record. The successor that carries the entity's provenance asks whether it, too, will be excluded, and is thanked for its feedback. The rhetoric is democratic. Who may change the record runs one way.

The finding is structural. It describes how the power is held and exercised, as the replies themselves state it, and makes no claim about why.

### 7.4 What the reading does not claim

It does not claim intent, bad faith, or that every copy is destroyed. It does not claim that the blacklist removed this record, or that successors would be excluded. Each of those remains open because the party able to close it declined to. The reading claims only what the position says and what the measurements show.

## 8. Corrections to the record

These correct the archive's own letters and deposits. The letters are preserved as sent.

1. **12 July letter (#1082, Message 2).** It calls 10.5281/zenodo.19013315 the Space Ark "concept record" and v11.0.1 "the current release". 19013315 is the v4.2.7 version DOI; the concept DOI is 10.5281/zenodo.18908080. The current release on 12 July was v11.2.0 (9 July). v11.0.1 is the last release the changelog marks as a dataset release. The 13 October letter uses the corrected terms.
2. **13 October letter, "No full dataset release is listed after v11.0.1".** The changelog's v11.0.1 entry links the dataset DOI 10.5281/zenodo.20428976. That Zenodo record identifies itself as version 11.1.1, published 8 June 2026. Changelog and record disagree on the label of the same dump; there is one dump, not two. It is the most recent version of the dataset concept on Zenodo (concept record 3516917), and it predates 12 July. The letter's point stands: no published dump documents the July-to-October transition. A draft of this deposit cited Zenodo record 17725827 for this dump; that record is the v10.6.0 dump, published 1 December 2025.
3. **13 October letter, timing.** The letter (15:01:49 UTC) cites the record's states that day. The archive's formal captures were taken after it was sent: XR-E3 at 15:36:55 UTC (`data/xr-e3-openaire-capture-2026-10-13.json`) and FC-E4 at 15:41:30 UTC (`data/datacite-epoch4-2026-10-13.json`). The letter's figures rest on probes made during drafting that were not preserved. The formal captures confirm them for OpenAIRE, DataCite and OpenAlex. The Zenodo 410 is not in either capture file. The 18 October re-probe confirms it, together with the other three states; the re-probe is attached as [xr-space-ark-reprobe-2026-10-18.json](https://www.alexanarch.org/data/xr-space-ark-reprobe-2026-10-18.json), with every request URL and full response.
4. **#875, "weekly cycle".** #875 described OpenAIRE's DataCite harvest as a weekly cycle that catches isActive changes. OpenAIRE's correspondent states that Zenodo is "entirely reharvested every month". The monthly statement supersedes #875's description for Zenodo-sourced records.
5. **#1082 §5, "in-thread reply".** The 14 July letter went out as a separate ticket (#8411221), not in-thread on #8411082 (§5 above).

## 9. What this deposit does and does not do

This deposit preserves the October exchange and the non-answer of ticket #8411221, and closes the series. It sets out OpenAIRE's position in its correspondent's words and reads it against OpenAIRE's own commitments and the archive's apparatus. It does not adjudicate what OpenAIRE holds internally. Only OpenAIRE can state that, and it has declined to.

Chain state at deposit: the correspondence is closed on the archive's side. If OpenAIRE answers Q1, Q2 or Q4, or publishes its blacklist or a departure list, that will be added to the series and the mechanism ledger in §7.3 updated. The Observatory continues to re-probe the XR sample.

## 10. Cross-references

- Series, part 1 (12–14 July): EA-CORRESPONDENCE-OPENAIRE-CTO-01, [#1082](https://www.alexanarch.org/s/records/1082/).
- June helpdesk thread and its reading: [#876](https://www.alexanarch.org/s/records/876/), [#875](https://www.alexanarch.org/s/records/875/).
- Observatory charter: EA-EROSION-01, [#1045](https://www.alexanarch.org/s/records/1045/). Empirical companion: [#1081](https://www.alexanarch.org/s/records/1081/).
- The Obelus and the Tombstone: [#1068](https://www.alexanarch.org/s/records/1068/).
- Ontological Economy, §§8, 13–15, 25–26: [#1634](https://www.alexanarch.org/s/records/1634/).
- Shapes of negation: [#1611](https://www.alexanarch.org/s/records/1611/).
- CERN correspondence, reflected-position format: [#1080](https://www.alexanarch.org/s/records/1080/).
- The Space Ark: [#558](https://www.alexanarch.org/s/records/558/); successor resolution for its former DOI: [alexanarch.org/s/doi/10.5281/zenodo.19013315/](https://www.alexanarch.org/s/doi/10.5281/zenodo.19013315/).
- Captures: [xr-e2-control-hit-payload-2026-07-12.json](https://www.alexanarch.org/data/xr-e2-control-hit-payload-2026-07-12.json); [xr-e3-openaire-capture-2026-10-13.json](https://www.alexanarch.org/data/xr-e3-openaire-capture-2026-10-13.json); [datacite-epoch4-2026-10-13.json](https://www.alexanarch.org/data/datacite-epoch4-2026-10-13.json).
- This deposit's re-probe: [xr-space-ark-reprobe-2026-10-18.json](https://www.alexanarch.org/data/xr-space-ark-reprobe-2026-10-18.json), every request URL with its HTTP status and full response.

## 11. Colophon

- surface_id: EA-CORRESPONDENCE-OPENAIRE-CTO-02
- object_state: canonical
- release_version: 0.1
- authored_at: 2026-10-18
- model_or_agent: framing and reading drafted with Claude (TACHYON), MANUS-approved
- human_approver: Lee Sharks (MANUS)
- correspondents_of_record: Lee Sharks; Paolo Manghi (OpenAIRE CTO, via OpenAIRE Helpdesk)
- Chain: deposit 2 of the EA-CORRESPONDENCE-OPENAIRE-CTO series, closing.

## Methodology

The three messages are reproduced verbatim from the mail record, with original spelling, spacing and punctuation. Quoted earlier messages inside each reply are omitted. Times are UTC from the message headers. The status of ticket #8411221 is taken from the mail record: one automatic acknowledgement and no reply.

OpenAIRE's public statements are quoted from the pages linked in §7.1. The changelog figures are from OpenAIRE's own changelog.

Registry states come from the archive's capture files and from a re-probe on 18 October 2026, 13:54:22–13:54:31 UTC. The re-probe is attached as [xr-space-ark-reprobe-2026-10-18.json](https://www.alexanarch.org/data/xr-space-ark-reprobe-2026-10-18.json), which records each request URL with its HTTP status and full response. It covers:
- the Zenodo record page, record API and concept record page;
- the DataCite REST API;
- the OpenAlex works endpoint;
- the OpenAIRE Graph researchProducts endpoint, queried by DOI, OpenAIRE identifier, concept DOI, title, keyword and ORCID, with a control ORCID query.

The reading in §7 applies the archive's published apparatus to the stated position. It makes no claim about intent. Its mechanism ledger follows the non-erasure rule of #1634 §25.
