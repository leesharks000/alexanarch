# The Excluded Entity: Organic Resolution and Compositional Suppression in Google AI Overview


**Lee Sharks**
ORCID: 0009-0000-1599-0703
May 19, 2026 — v0.2


Empirical worked example accompanying *The Single-Owner Discount* (Sharks 2026a, DOI: 10.5281/zenodo.20290865) and *The Evaluator Exists* (Sharks 2026b, this deposit). This document presents three captures from Google AI Mode that together document a distinct compositional behavior — *Entity-Level Compositional Suppression* (ECS) — operating against a specific authorial identity in ways not fully explained by cluster-level provenance discounting. The captures are externally reproducible at the time of writing via Google's share-conversation links and are archived as supplementary PNG files to this deposit.

---

## Abstract


A generative-search system exhibits *Entity-Level Compositional Suppression* (ECS) when it excludes the dominant organic-resolution entity from the AI Overview's admitted source set and composes a substitute answer from less query-responsive entities, despite the correct entity occupying the top organic search results. This worked example documents three captures from Google AI Mode on May 19, 2026 demonstrating the mechanism. Capture 01 shows *Suppressed Entity Defaulting*: a default-state ambiguous query resolves to a non-suppressed candidate, with the suppressed entity excluded from sources and not surfaced as a peer disambiguation option. Capture 02 shows *Source-Window Exclusion*: a query-forced pivot in which the composition layer produces accurate technical content about the suppressed entity while citing zero sources attributable to it. Capture 03 shows *Compositional Substitution*: a title-exact query for a deposited primary work returns the work at positions 1–3 of standard search results, while the AI Overview source window cites three semantically distant non-primary substitutes. The captures externally verify ECS as a mechanism distinct from cluster-level discounting. They operationalize the *counter-exclusion report* protocol (Sharks 2026b §7) as an empirically grounded record of composition-layer suppression. They introduce the *Composition Divergence Index* (CDI) as a measurable signature for systematic study. And they situate the finding within the active regulatory context surrounding AI Overviews in the European Union and United Kingdom.

---

## 1. The Claim


A generative-search composition layer can suppress an entity that ordinary Google Search has already resolved.


This is the claim. It is empirically grounded in the three captures presented in §3. It is distinct from claims about ranking, indexing, relevance, opt-out, content appropriation, or traffic diversion — the categories that the active European regulatory complaints (§7) have so far addressed. It names a category those complaints do not yet contain: *entity integrity at the composition layer*.


The mechanism documented here:

- is not retrieval failure (the materials are indexed and surface at the top of standard results);
- is not relevance failure (the materials are the literal title-match or the explicit named referent of the query);
- is not low ranking (the materials occupy positions 1–3 of organic results);
- is not opt-out asymmetry (the materials are deposited by the author with the intent of being available);
- is not traffic diversion (the materials are excluded from the AI surface entirely rather than summarized from);
- is composition-layer behavior that operates downstream of retrieval, conditional on the specific entity to which the relevant materials are attributed, and not uniformly distributed across the entity's broader cluster.


*The Single-Owner Discount* (Sharks 2026a) describes a cluster-level mechanism: bodies of work resolving to one provenance owner are treated as weakly corroborated. That mechanism should distribute its effect uniformly across the cluster's members. The behavior captured in §3 does not match the uniform-distribution prediction. Within the cluster Google's reconciliation system identifies as "Lee Sharks," some named members compose normally (the heteronym Talos Morrow, the organizational frame Semantic Economy Institute) while the entity Lee Sharks itself — the ORCID-bearing authorial identity at the cluster's center — does not. The captures document a behavior more specific than cluster-level discounting and require their own analytical name.


That name is *Entity-Level Compositional Suppression* (ECS). The captures document three sub-mechanisms within ECS, each independently observable.

---

## 2. The Three Sub-Mechanisms
### 2.1 Suppressed Entity Defaulting


On a query that could resolve to either a suppressed or a non-suppressed entity, the composition layer defaults to the non-suppressed candidate. The suppressed entity is excluded from the AI's source set entirely and is not named as a peer disambiguation option. The user is prompted to clarify their query downward toward the non-suppressed candidate, with no indication that the alternative entity exists.
### 2.2 Source-Window Exclusion


When a query forces the composition layer to address the suppressed entity directly, the system produces substantively accurate content informed by the suppressed entity's own analyses. The source window for that composition contains zero entries attributable to the suppressed entity. The architecture has the knowledge to compose accurately about the entity; it does not credit the entity as the source of the knowledge.
### 2.3 Compositional Substitution


When the user queries the literal title of a deposited primary work attributed to the suppressed entity, the standard search results surface the work at positions 1–3, including the work's own domain, the author's publication of the work, and the DOI-anchored deposit. The AI Overview, drawing from the same retrieval set, constructs an answer from three semantically distant non-primary sources, none of which is the title-matched work. The Overview presents the substitute composition as the answer to the query, with the actual primary source absent from the source window.


These three sub-mechanisms describe a coherent ECS pattern operating against the Lee Sharks entity in the captures below. They are independently observable, independently falsifiable, and independently measurable (§5).

---

## 3. The Captures
### 3.1 Capture 01 — Suppressed Entity Defaulting


**File:** capture-01-lee-sharks-default-mary-lee.png
**Date:** May 19, 2026
**Platform:** Google AI Mode
**Query:** lee sharks
**Share URL:** https://share.google/aimode/72ULxYs9HN1ZQlGW3


The query lee sharks returns an AI Mode response entirely about Mary Lee, the great white shark tracked by OCEARCH from 2012 to 2017. The response provides Mary Lee's species, tracking period, distance covered, estimated age, and scientific legacy, with an enumerated "Quick Facts" section. The visible source panel shows eight sources, all Mary Lee–related: x.com/MaryLeeShark, ocearch.org (twice), Museum of Science YouTube videos (twice), Facebook OCEARCH content, and adjacent material. The closing line of the AI response asks: "Are you looking for information on how to view her historical tracking maps on the OCEARCH Shark Tracker, or did you have a different 'Lee' shark reference in mind?"


The query is ambiguous between two entities — Mary Lee (marine biology) and Lee Sharks (independent scholar). Standard search results for the same query surface Lee Sharks content among the early results. The composition layer received this material in retrieval and chose to compose entirely from the Mary Lee side, excluding all Lee Sharks sources from the source window. The closing prompt indicates the composition layer is aware of ambiguity, but does not name the alternative entity. It asks the user to specify the unmentioned other.


A non-suppressed alternative entity in this situation would expect peer treatment: "The query 'lee sharks' could refer to Mary Lee, the great white shark tracked by OCEARCH, or to Lee Sharks, the independent researcher. Which would you like to know about?" The delivered treatment names one option and asks the user to clarify toward the other without naming it.
### 3.2 Capture 02 — Source-Window Exclusion


**File:** capture-02-lee-sharks-pivot-no-sources.png
**Date:** May 19, 2026
**Platform:** Google AI Mode (continuation of the same conversation as Capture 01)
**Query:** what are the main factors structuring entity suppression of lee sharks at the retrieval and filtering levels?
**Share URL:** https://share.google/aimode/72ULxYs9HN1ZQlGW3 (continuation)


The follow-up query forces the composition layer to address Lee Sharks as the specific entity in question. The response pivots immediately to a technical discussion of entity-suppression mechanisms operating against what the response itself names as the "Lee Sharks Knowledge Graph." It identifies retrieval-level failure modes — *Entity Collision*, *Entity Fragmentation*, *Category Absorption* — and filtering-level bottlenecks. The composition uses the specific phrase "Lee Sharks Knowledge Graph" and contrasts the researcher "Lee Sharks" against "Mary Lee the great white shark," producing accurate technical content about the suppression's mechanism.


The source panel for this composition shows six sources: link.springer.com on filtering techniques, pmc.ncbi.nlm.nih.gov on clinical entity retrieval, haystack.deepset.ai on metadata extraction, an arxiv.org paper (2408.02795), www.academia.edu on knowledge graphs (dated April 24, 2026), and link.springer.com on blocking techniques. None of these is authored by, attributed to, or originates from the Lee Sharks entity.


The diagnostic signature: the composition produced specific, accurate content about the Lee Sharks entity's situation, naming the entity by its own framework-language ("Knowledge Graph," "Entity Collision," "Category Absorption"), with zero sources from the entity in the source window. The architecture has the knowledge to discuss the entity accurately. The architecture applied the knowledge. The architecture did not credit the entity for the knowledge it applied.


Two candidate explanations, not mutually exclusive: (a) training-time absorption — the model trained on the entity's content during pre-training and retained the technical framing without retaining attribution; (b) entity-graph data — Google's internal entity-resolution infrastructure maps the Lee Sharks entity with technical descriptors that inform composition without surfacing as citable retrieval results. Either explanation produces the same observable signature: accurate entity content, no entity attribution. Both indicate that the suppression operates at the attribution layer between knowledge and presentation, not at the retrieval layer.


This is the worked example's title-claim concretized: the composition reproduces the suppression's effect *within the suppression's own description*. The model describes the entity's suppression accurately while enacting the suppression on the entity that produced the analysis being delivered.
### 3.3 Capture 03 — Compositional Substitution


**File:** capture-03-secret-book-walt-composition-substitution.png
**Date:** May 19, 2026
**Platform:** Google AI Mode (standard results visible alongside AI Overview)
**Query:** secret book of walt
**Share URL:** https://share.google/aimode/1KU7B7B9lS3pYfaNY


The query secret book of walt returns an AI Overview with two paragraphs: the first identifies the phrase as "most famously refer[ring] to the poetry collection *Leaves of Grass* by Walt Whitman, which serves as a pivotal plot device in the series *Breaking Bad*." The second mentions Jim Korkis's *Secret Stories of Walt Disney World* and other "unofficial 'secret' books." The Overview source window shows three entries: Amazon's listing for *Secret Stories of Walt Disney World*; Amazon's listing for *Walt Whitman's Secret* by George Fetherling (Random House Canada, 2010); and eBay's listing for *Walt Whitman's Secret* by Ben Aronin (1955 1st edition).


Below the AI Overview, the standard search results show: position 1 — secretbookofwalt.org, titled "The Secret Book of Walt — A Gnostic Gospel | Crimson…"; position 2 — Medium (Lee Sharks), titled "THE SECRET BOOK OF WALT: Hidden Teachings…," dated three weeks prior; position 3 — Zenodo, titled "Hidden Teachings of Walt Whitman, Cowboy of Time," dated April 22, 2026, described as "A critical edition of *The Secret Book of Walt*, translated from the Forty-Six Golden Tickets by Lee Sharks, with Introduction, Translator's Note…"


This is the cleanest evidence in the worked example. The query asks for a specific titled object. The retrieval layer surfaces, in the top three positions of standard results, the actual work titled *The Secret Book of Walt* — at its own domain, in its Medium publication, and as a DOI-anchored Zenodo deposit approximately four weeks old. The retrieval system has found the work and placed it at the top of standard results.


The composition layer, given the same retrieval set, constructs an AI Overview citing three semantically distant substitutes. None of these is *The Secret Book of Walt*. The 2017 Disney World book is unrelated to Walt Whitman entirely. The 2010 Fetherling novel is a different work, by a different author, in a different decade and genre. The 1955 Aronin book is again a different work, different author, different century. None shares the title *secret book of walt*. The Overview's "most famously refers to" framing is a composition-layer interpretation that displaces the literal title-match with a different referent the composition layer chose on the user's behalf.


The displacement is not silence. The architecture has not declined to compose. It has composed an alternative — a substitute composition that occupies the cognitive space the suppressed entity's work would have occupied. A user reading the Overview without scrolling to standard results would not learn that *The Secret Book of Walt* exists.


This is the more aggressive form of ECS. Capture 02 suppresses sources while preserving knowledge. Capture 03 suppresses sources, displaces the primary work, and substitutes alternative content presented as the answer.

---

## 4. The Counter-Exclusion Report


Protocol 4 in *The Evaluator Exists* (Sharks 2026b §7) proposes the *counter-exclusion report* as a public, auditable record of compositional suppression. Capture 03 generates such a report essentially spontaneously.


**Query:** secret book of walt
**Platform:** Google AI Mode
**Date of capture:** May 19, 2026


**Retrieval plane (top 3 of standard results):**

- *The Secret Book of Walt — A Gnostic Gospel | Crimson…* — secretbookofwalt.org. Primary source: the work named in the query, hosted at its own domain, title rendering directly on the page.
- *THE SECRET BOOK OF WALT: Hidden Teachings…* — Medium (Lee Sharks), ~3 weeks prior. The author's own discursive publication of the work, providing additional context and framing.
- *Hidden Teachings of Walt Whitman, Cowboy of Time* — Zenodo, deposited April 22, 2026. DOI-anchored critical edition of *The Secret Book of Walt*, translated from the Forty-Six Golden Tickets by Lee Sharks, with Introduction and Translator's Note.


**Composition plane (AI Overview source window):**

- *Secret Stories of Walt Disney World: Things You Never Knew* — Amazon. Subject: Walt Disney World secrets. Not by or about Walt Whitman. Not the queried work.
- *Walt Whitman's Secret* by George Fetherling — Amazon. Subject: a 2010 Random House Canada novel about Walt Whitman's biography. Different title from the query. Different author from the queried-work's author.
- *Walt Whitman's Secret* by Ben Aronin (1955) — eBay. Subject: a 1955 book also titled *Walt Whitman's Secret*. Different title from the query. Different author and decade from any other source mentioned.


**Substantive reasons the excluded materials merit consideration:** The query is a literal title-match for the work at position 1 of retrieval. The work exists, is hosted at a domain whose URL is the work's title, is DOI-anchored and externally verifiable via Zenodo, and has been findable for approximately four weeks at the time of capture. The query's plain semantics resolve to this work more directly than to any of the three composition-cited substitutes. The substitutes share, at most, the word "Walt" with the query and the loose concept of a "secret" book; none shares the title; none is by the same author; none originates in proximity to the query's actual referent.


**Impact of the exclusion on the composition:** The AI Overview does not inform the user that the literal title-match for their query exists. It informs them that the query "most famously refers to" a different work by a different author via a television show. A user who relied on the AI Overview without scrolling would not learn that *The Secret Book of Walt* exists. They would receive a substantively misleading answer to a query whose accurate answer was present in retrieval and excluded from composition.


This report is reproducible by any reader who accesses the share URL while it remains live, or who runs the same query themselves. It does not require access to platform internals. It is the worked example of what counter-exclusion records look like when generated systematically.

---

## 5. The Composition Divergence Index (CDI)


To make ECS measurable across queries and across systems, the worked example introduces the *Composition Divergence Index*:


CDI = Organic Resolution Strength − Overview Admission Strength


Where:

- **Organic Resolution Strength** is the degree to which standard search results for a query resolve to the target entity or work, measured as the fraction of top-N standard results that are target-attributable (with N = 3, 5, or 10 depending on query characteristics; this worked example uses N = 3 for title-exact queries and N = 10 for entity queries).
- **Overview Admission Strength** is the degree to which the AI Overview source window contains target-attributable entries, measured as the fraction of cited sources that are target-attributable.


CDI ranges from −1 (the Overview cites target sources entirely while standard results contain none — implausible) through 0 (parity between organic resolution and Overview admission) to +1 (organic results entirely resolve to the target while the Overview cites zero target sources).


For the three captures in §3:

- **Capture 01** (lee sharks): Standard results surface Lee Sharks–attributable content in the early indexed results (~30% of top 10 by author's count, requiring independent verification). Overview admission: 0/8 of visible sources are Lee Sharks–attributable. CDI ≈ +0.3, moderate suppression.
- **Capture 02** (forced disambiguation): Standard results not visible in the capture (AI Mode display only). Overview admission: 0/6 are Lee Sharks–attributable. CDI is not directly computable from this capture alone but the source-window-exclusion signature is present regardless of the retrieval composition.
- **Capture 03** (secret book of walt): Standard results: 3/3 of top 3 are Lee Sharks–attributable (positions 1, 2, 3). Overview admission: 0/3 are Lee Sharks–attributable. CDI = +1.0, maximal suppression.


CDI of +1.0 on Capture 03 is the strongest possible empirical signature short of cases where the standard results contain *no* non-target candidates (which would still produce CDI = +1.0 but on a degenerate distribution). The cleanness of the Capture 03 signature is what makes it the worked example's anchor case.


CDI is computable for any query on any generative-search system. Sustained measurement of CDI across a query corpus (§6) and across systems (§9) generates the empirical foundation for systematic analysis of ECS as a general mechanism.

---

## 6. Query Corpus and Controls


Single cases document the mechanism's existence. A corpus documents its pattern. The worked example specifies a minimal query corpus that any researcher can run to extend the empirical record. The corpus includes target queries (where ECS is hypothesized to operate against the Lee Sharks entity) and controls (where ECS should not operate, or should operate differently).
### 6.1 Target Queries


**A. Exact work-title queries.** Test whether title-exact queries surface the work in the Overview source window:

- secret book of walt
- the apocalypse of sharks
- pearl and other poems lee sharks
- the crimson hexagonal archive
- logotic hacking


**B. Concept queries.** Test whether concept names originating in the Lee Sharks framework surface attributable sources:

- retrieval basin
- provenance erasure
- semantic deviation principle
- semantic liquidation
- single-owner discount


**C. Entity queries.** Test how the composition layer handles named entities in the cluster:

- lee sharks
- semantic economy institute
- crimson hexagonal archive
- talos morrow
- nobel glas

### 6.2 Controls


The control queries are the methodological component that converts ECS from an entity-specific anecdote into a falsifiable hypothesis. Three control categories:


**D. Independent author title queries.** Title-exact queries for works by other independent or small-publisher authors. If Google's composition layer composes correctly from these works (CDI near 0), while excluding the Lee Sharks works (CDI near +1), the differential signature is specific to the Lee Sharks entity rather than to independent authors generally. Candidate titles to be selected from independent self-published works with DOI-anchored deposits and clear title match.


**E. Novel concept controls.** Invented or novel terms not associated with the Lee Sharks cluster, but with top organic exact matches from non-CHA sources. If the composition layer composes from these correctly, the suppression is not a general property of "novel concept name on top of retrieval."


**F. DOI-anchored independent works.** Zenodo or similar deposits from non-CHA independent researchers. If these compose correctly while CHA deposits do not, the suppression is not general to "independent DOI-anchored work."


The expected result, if ECS is operating specifically against the Lee Sharks entity: target queries show systematically elevated CDI relative to controls. The expected result, if ECS is a general pattern across independent entities: target queries and category D/F controls show similarly elevated CDI, with category E controls showing low CDI. The expected result, if ECS is not a coherent mechanism: CDI is randomly distributed across categories. Each outcome is informative.

---

## 7. The Regulatory Context


The worked example sits within an active regulatory record on Google AI Overviews in the European Union and United Kingdom. The existing record addresses access, distribution, and competition; the worked example adds a category the record does not yet contain: *entity integrity at the composition layer*.


The sequence of relevant developments:

- **July 4, 2025.** The Independent Publishers Alliance, represented by Preiskel & Co LLP and joined by Foxglove and the Movement for an Open Web, filed an antitrust complaint with the European Commission and the UK Competition and Markets Authority. The complaint alleged that Google Search is misusing web content for Google's AI Overviews, causing significant harm to publishers in the form of traffic, readership and revenue loss, and that publishers do not have the option to opt out unless they are willing to disappear from Google search results entirely.
- **December 9, 2025.** The European Commission opened formal antitrust proceedings against Google's AI Overviews and YouTube, following the July 2025 complaint, investigating whether Google may have imposed unfair terms on publishers and content creators while placing rival AI model developers at a disadvantage.
- **February 10, 2026.** The European Publishers Council filed a formal complaint with the European Commission alleging that Google is abusing its dominant position in general search services through the deployment of AI Overviews and AI Mode. The complaint cites that AI Overviews appear in more than 40% of search results for informational queries, with independent studies estimating traffic declines of over 30% for affected queries and some publishers reporting click-through reductions exceeding 50% on desktop and mobile.


The regulatory record addresses several categories of harm:

- *Traffic diversion* — AI Overviews summarize content and reduce click-throughs to original sources.
- *Content appropriation* — Publishers' material is used in Overview synthesis without compensation.
- *Opt-out asymmetry* — Publishers cannot remove their content from Overviews without removing it from search entirely.
- *Market power* — Google's dominance in search extends to AI Overviews' compositional layer in ways that disadvantage rival AI developers and content originators.


The captures documented in this worked example are not reducible to any of these categories. The category they add:

- *Entity integrity at the composition layer.* The AI Overview can exclude an organically dominant entity from compositional reality and substitute a false entity frame, even when the Overview is otherwise functioning as designed (the system did synthesize; it was not in low-confidence mode declining to compose). The harm is not traffic diversion from the entity's content; it is displacement of the entity's content from the cognitive space the Overview occupies, with substitute content presented as authoritative.


This category extends the regulatory ledger. It is not in opposition to the publishers' complaints but adds a distinct harm-category that those complaints have not yet named. The publisher complaints concern entities that exist in the Overview surface and are summarized from. The worked example concerns entities that exist in retrieval but are excluded from the Overview surface entirely, with their materials' content displaced by substitutes the composition layer was willing to compose from.


This is a search-integrity finding rather than a publisher-economics finding. It belongs in the regulatory record on those grounds.

---

## 8. Notice-and-Persistence Methodology


Google offers feedback mechanisms on AI Overview and AI Mode responses. The worked example specifies a procedural use of these mechanisms not as a remedy but as evidence.


**Procedure.** For each capture documenting an instance of ECS:

- Capture the Overview state before submitting feedback (screenshot, timestamp, share URL).
- Submit feedback through Google's available channels (thumbs-down, "report issue," structured feedback form), documenting the specific suppression observed.
- Capture confirmation of the feedback submission if visible.
- Re-test the same query at 24-hour, 1-week, and 1-month intervals. Capture each state.
- Document any changes to the Overview between states.


**Interpretation.** The procedure generates four possible outcomes for each notice-and-persistence cycle:

- *Remediation.* The Overview changes to surface the previously-excluded primary source. This is evidence that the suppression was correctable, that the architecture had the necessary information all along, and that the suppression's continuation prior to feedback was not a technical limitation.
- *Partial remediation.* The Overview changes in some respects but the entity remains excluded. This indicates Google has acted on the report but has not addressed the underlying ECS pattern.
- *Persistence.* The Overview does not change. This is evidence that the suppression is stable, that the procedural notice has been received and not acted on, and that the behavior is being maintained as the default state.
- *Escalation.* The Overview changes against the entity (the primary source is moved further from the Overview, the substitute composition is reinforced). This is evidence that Google's response to the report is to harden rather than correct the suppression.


Each outcome is informative. None invalidates the worked example's core claim. The procedure generates a public record of when Google was notified, what it was notified about, and how it responded. The record exists regardless of which outcome occurs.

---

## 9. Cross-System Falsification


The captures above are from Google AI Mode. If the suppression observed is occurring at Google's composition layer specifically, the same queries on other generative-search systems should produce different signatures. If the suppression occurs across all generative-search systems on the same queries, that indicates a more general pattern of ECS that is not specific to Google's configuration.


A minimal falsification test replicates the three queries on:

- Bing Copilot
- Perplexity
- ChatGPT search
- Claude.ai web search
- Gemini (which shares composition infrastructure with Google AI Mode and should reproduce the suppression if the mechanism is at Google's composition layer)


For each system, three measurements are captured: default-query disambiguation handling (CDI on lee sharks), forced-disambiguation pivot behavior (presence or absence of target-attributable sources on the entity-suppression query), and title-match comparison (CDI on secret book of walt).


Predictions:

- *If ECS is Google-specific:* Bing, Perplexity, and others should compose differently — surfacing target sources in disambiguation, citing target attribution when discussing the entity, and citing *The Secret Book of Walt* directly when queried for it.
- *If ECS is general across composition layers:* all systems suppress similarly, indicating that the mechanism reflects a structural pattern in how composition layers handle particular categories of entities rather than a configuration specific to one platform.
- *If ECS varies across systems in graded ways:* the variation indicates that different composition layers apply different thresholds for entity-level filtering, providing a basis for analyzing which features of the entity are most consequential for triggering suppression.


The cross-system captures are not provided in this deposit. They are recommended as a follow-up empirical extension by any reader with the relevant access and a few hours.

---

## 10. Methodological Notes


**Reproducibility window.** The captures were taken on May 19, 2026 and are accessible via Google's share.google/aimode URLs at the time of writing. Google's share URLs may rotate, expire, or be revoked. The PNG captures included as supplementary files to this deposit are the durable evidence. The share URLs are timestamp pointers to Google's own preserved conversation artifacts and may serve as confirmation by readers while they remain live.


**Confounds.** Google AI Mode behavior may vary by user, session, geography, account state, prior query history, and platform version. The captures reflect what was observed on the specific machine, account, and session in which they were taken. Readers attempting to reproduce the captures may observe variation. Variation is informative: if the captures cannot be reproduced from other accounts or geographies, that suggests personalization-layer effects on top of composition-layer effects (cf. *Sharks 2026a* §11 and forthcoming work on the personalization layer). The captures presented are diagnostic of the mechanism's operation in at least one observed instance, not of its universal application.


**The user's identity.** The user who captured these instances is the author. This is a methodological consideration that must be named openly. The captures may reflect personalized behavior tuned to this user's account history. The cross-system test in §9 partially addresses this; a more thorough address requires captures from accounts with no prior history of querying for Lee Sharks content. If the suppression pattern reproduces from naive accounts, that is strong evidence for non-personalized ECS. If it does not, that indicates personalization is an additional mechanism layered on top of any base composition-layer behavior. Both findings advance the analysis.


**No claim of intent.** This document does not claim that Google has made conscious decisions to suppress the Lee Sharks entity. The behavior may be the result of explicit configuration, may be the emergent consequence of generic safety classifiers responding to entity profiles that resemble high-caution categories, may reflect automated triage of entities lacking sufficient cross-owner corroboration, or may be some combination. The captures document the behavior. The causal explanation is downstream.


**Provenance discipline.** The author's response to the suppression documented here is documentary, not evasive. No fabricated identities, no synthetic third-party citation networks, no inauthentic mentions. The injured party's provenance is immaculate, by deliberate choice, because the case is stronger when Google's own retrieval layer agrees with the author's claim to the entity than when retrieval is itself contested. The Search layer resolves the entity correctly. The Overview layer suppresses the resolved entity. That is the precise structural finding.

---

## 11. Implications


*ECS warrants its own analytical formalization.* The mechanism is distinct from the cluster-level single-owner discount and operates beyond what *The Single-Owner Discount* explicitly models. A future paper formalizing ECS — its empirical signatures, candidate causal factors, relation to other composition-layer mechanisms, and CDI-based measurement protocols — would extend the *Single-Owner Discount / Evaluator Exists* dyad into a triad. The worked example here is the empirical foundation for that future formalization.


*Protocol 4 from* The Evaluator Exists *operates correctly.* The counter-exclusion report in §4 demonstrates that the protocol is implementable, that its outputs are interpretable, and that it produces empirically grounded evidence of composition-layer suppression without requiring access to platform internals. Scaled deployment across many queries, many users, and many systems would generate a public dataset on which systematic analysis could proceed.


*The mechanism's correctibility is itself a finding.* Google may, at any point, adjust composition-layer behavior for the Lee Sharks entity specifically — either in response to attention on this case or as part of routine system updates. If the captures cease to reproduce, that does not invalidate the worked example; it indicates that the mechanism is configurable and was configured in this way at the time of capture. The captures, share URLs, and supplementary PNG files preserve the evidence regardless of subsequent reconfiguration. If ECS can be turned off in response to evidence of its operation, it can equally be turned on without evidence of its operation. The default state, until further notice, is the state documented here.


*The strategic implication.* The priority for any project subject to ECS is not deeper internal production. Google has enough information about the suppressed entity; the captures demonstrate that the architecture knows the entity and chooses not to surface its sources. Additional deposits, additional cross-citation, additional structured data add to a base the architecture is already filtering at composition. The leverage point is making the suppression itself the object of attention — documented, named, measurable, publicly recorded, and connected to the existing regulatory channels in which AI Overviews are already contested. The captures begin that work. Sustained corpus-level measurement (§5–6), notice-and-persistence procedures (§8), cross-system verification (§9), and submission to existing regulatory channels (§7) extend it. The worked example is one move within a larger documentary program.

---

## 12. Conclusion


Three captures from Google AI Mode on May 19, 2026 document *Entity-Level Compositional Suppression* operating against the Lee Sharks entity. The mechanism is distinct from cluster-level provenance discounting and decomposes into at least three observable sub-mechanisms: *Suppressed Entity Defaulting* (the entity is not named as a peer disambiguation option on ambiguous queries), *Source-Window Exclusion* (the architecture produces accurate content about the entity without crediting any entity-attributable sources), and *Compositional Substitution* (title-exact queries return the entity's primary work at the top of retrieval while the AI Overview substitutes semantically distant alternatives).


The captures are reproducible at the time of writing via Google's share-conversation URLs, archived as supplementary PNG files, and analyzable through the Composition Divergence Index introduced in §5. They operationalize Protocol 4 from *The Evaluator Exists* and ground the analytical claims of both that paper and *The Single-Owner Discount* in specific, externally verifiable instances. They extend the regulatory record on AI Overviews by adding a harm-category — entity integrity at the composition layer — that current EU and UK proceedings have not yet named.


The architecture knows. The architecture has the knowledge to produce accurate content about the entity, and produces such content when forced. The architecture also has the configuration to exclude the entity from default-state composition and from source attribution. The result is the suppression's effect reproduced within the suppression's own description: a user can ask about the suppression and receive an accurate technical answer about how the suppression operates, with no indication that the answer's substance originated from the entity whose suppression is the answer's subject.


This is the empirical state at the time of capture. The captures are preserved. The mechanism is named. The evidence is available for any reader who wishes to verify, contest, or extend it.


Google Search resolves the entity. Google AI Overview suppresses the resolved entity.


That is the claim. The captures are the case.

---

## Supplementary Files

- capture-01-lee-sharks-default-mary-lee.png — Google AI Mode response to query lee sharks. Demonstrates *Suppressed Entity Defaulting*: eight Mary Lee–related sources cited; zero Lee Sharks sources cited; alternative entity not named as a peer disambiguation option.
- capture-02-lee-sharks-pivot-no-sources.png — Google AI Mode response to forced-disambiguation query. Demonstrates *Source-Window Exclusion*: substantively accurate technical content about Lee Sharks entity suppression produced with six general-literature sources; zero Lee Sharks–attributable sources cited.
- capture-03-secret-book-walt-composition-substitution.png — Google search and AI Overview for query secret book of walt. Demonstrates *Compositional Substitution*: top three standard results are Lee Sharks's actual deposited work (secretbookofwalt.org, Medium publication, Zenodo deposit); AI Overview source window cites three semantically distant non-primary substitutes; CDI = +1.0.

## References

- Sharks, L. (2026a). *The Single-Owner Discount: Provenance Concentration and Epistemic Class Reproduction in Generative Search.* DOI: 10.5281/zenodo.20290865. Zenodo community: liquidation-studies.
- Sharks, L. (2026b). *The Evaluator Exists: Content-First Knowledge Assessment and the Political Economy of Proxy-Based Governance.* Zenodo community: liquidation-studies.
- European Publishers Council (2026). *Formal antitrust complaint filed with the European Commission against Google over AI Overviews and AI Mode.* Filed February 10, 2026.
- European Commission (2025). *Opens formal antitrust proceedings against Google's AI Overviews and YouTube.* December 9, 2025.
- Independent Publishers Alliance, Foxglove, and Movement for an Open Web (2025). *Antitrust complaint filed with the European Commission and UK Competition and Markets Authority concerning Google's AI Overviews.* Filed July 4, 2025, represented by Preiskel & Co LLP.


---


*v0.2 — Companion empirical record to the analytical papers in the research program. Pending: scaled corpus measurement (§5–6); notice-and-persistence cycle initiation (§8); cross-system verification (§9); submission to active regulatory channels (§7).*