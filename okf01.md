---
deposit_number: 1088
hex: 0451
title: "EA-CORRESPONDENCE-OKF-01 v1.0: The Predicted Sequence Arriving — Output-Governance Pressure on Google's Open Knowledge Format from Inside Its Own Repository"
creator: Lee Sharks
orcid: 0009-0000-1599-0703
date: 2026-07-17
content_type: Institutional correspondence; documentary artifact for the OKF specification-development process; predictive-paper measurement deposit; governance artifact
license: CC-BY-4.0
substrate: "Human-authored (Lee Sharks, MANUS). The two 2026-07-17 posts on `GoogleCloudPlatform/knowledge-catalog` (comment on #53 and new issue #207) were composed by Lee Sharks under MANUS review and posted to the OKF repository on 2026-07-17. Deposit framing, cross-anchor selection (registry lookups against alexanarch), and archival composition prepared by TACHYON (Claude) as instrument under MANUS review. No automated pipeline generated the correspondence texts. No API calls were made in the preparation of this deposit; per the No-Double-Draw rule binding on internal depositors, LLM-domain work was performed in-session and mechanical work through local scripts."
version: v1.0
related_ids: "https://github.com/GoogleCloudPlatform/knowledge-catalog/issues/53, https://github.com/GoogleCloudPlatform/knowledge-catalog/issues/207, https://github.com/GoogleCloudPlatform/knowledge-catalog/pull/99, https://www.alexanarch.org/s/records/835/, https://www.alexanarch.org/s/records/1087/, https://www.alexanarch.org/s/records/1081/, https://machinemediation.org/data/registry.json"
axn_schema_version: v2
protocol_version: alexanarch-deposit-protocol/v1
keywords:
  - OKF
  - Open Knowledge Format
  - GoogleCloudPlatform
  - knowledge-catalog
  - summarization governance
  - provenance kernel
  - disambiguation
  - summary policy
  - consumer receipts
  - conformance fixtures
  - deletion semantics
  - tombstones
  - substrate declaration
  - derivation
  - completeness
  - body_status
  - Lacuna Protocol
  - predictive paper
  - correspondence
  - Caio Ribeiro
  - Cloudwalkers
  - Sappho 31
  - SPXI
  - GEO
  - semantic inversion
  - entity substitution
  - provenance erasure
  - 1059 batches
  - 871 DOI
  - Zenodo termination
  - capture 205
  - AXN protocol reception
---

# EA-CORRESPONDENCE-OKF-01 v1.0: The Predicted Sequence Arriving — Output-Governance Pressure on Google's Open Knowledge Format from Inside Its Own Repository

## Description

## Overview

This deposit archives the full public correspondence between Lee Sharks (Crimson Hexagonal Archive / Alexanarch) and Caio Ribeiro (Cloudwalkers, GoogleCloudPlatform contributor) on the Open Knowledge Format (OKF) v0.1 specification, held in the `GoogleCloudPlatform/knowledge-catalog` repository during 14 June — 17 July 2026. The correspondence is preserved here as a documentary artifact and as evidentiary substrate for the predictive frame established by an earlier deposit in this archive: **#835 · AXN:0350.GOVERNANCE.📝🍄🪟🤲🌕☉ — "THE CONVEYOR BELT AND THE COMPRESSION MACHINE: OKF Without Output Governance"** (Sharks, June 2026; the Zenodo DOI of that paper, 10.5281/zenodo.20723872, was severed by the 2026-06-19 Zenodo termination and now resolves only through Alexanarch).

The paper predicted that OKF, as designed, would arrive at a well-marked crossroads: the format defines producer-side descriptive metadata but no consumer-side receipt for what a summarization pass preserved or destroyed, and no representation of what a bundle has *lost*. The paper forecast the specific mechanisms by which that gap would be surfaced from inside the repository itself, the specific classes of proposal that would emerge, and the specific double-back the maintainers would eventually accept. The present deposit records the first eight turns of that arrival: a proposal for producer-side summarization-governance fields (#53), a productive interlocutor's proposal for consumer-side receipts and conformance fixtures (#99), and — after the interruption of the 2026-06-19 Zenodo termination — the next-order proposals for producer-side substrate/derivation/completeness declarations and for spec-level deletion semantics (#207).

The correspondence is preserved verbatim below, with permalinks, timestamps, and interstitial commentary bounded to what distinguishes prediction from observation.

## §I — The predictive paper (Alexanarch #835)

Deposit #835, **EA-SEI-OKF-ANALYSIS-01 v1.2 · AXN:0350.GOVERNANCE.📝🍄🪟🤲🌕☉**, was minted on 14 June 2026 and cited on the OKF thread the same week. Its architecture: a knowledge-exchange format that admits arbitrary consumers cannot remain neutral about consumption. Every AI agent that reads such a format is a compression pass; every compression pass is a transformation with characteristic failure modes; every unmarked transformation compounds. The paper's central prediction was structural — that OKF's design center of gravity (portable markdown-plus-frontmatter concepts, agent-consumable, minimally opinionated) would generate three pressures whose combined force would exceed the format's stated scope:

1. **Producer-side summarization governance**: authors would need a way to declare which elements of a concept must survive summarization by consuming agents.
2. **Consumer-side receipts and conformance**: any producer-side declaration is aspirational without a matched consumer-side artifact that records what was actually preserved.
3. **Producer-side lifecycle**: bundles are not stable holdings; deletion, deprecation, and rewriting happen, and a format that cannot represent its own losses will launder them into every consuming agent.

The paper offered these as time-bounded, falsifiable predictions with a measurement framework. It was archived on Zenodo (DOI 10.5281/zenodo.20723872) on 14 June 2026 and cited on the OKF thread on 16 June 2026. Five days later — 19 June 2026 — the Zenodo host of that paper, along with the CHA community's 871 DOI-anchored deposits, was terminated. The paper survives at Alexanarch #835 with the citation loop still resolvable; the Zenodo DOI is a live example of the second-order phenomenon it forecast.

## §II — The 14 June 2026 opening (issue #53, opening post)

On 14 June 2026, Lee Sharks opened issue #53 on `GoogleCloudPlatform/knowledge-catalog` — the OKF specification repository — titled "Proposal: optional summarization-governance fields — provenance_kernel, disambiguation, summary_policy." The proposal was the first pressure named above, made concrete as three optional frontmatter fields and one conventional body heading, structured to compose cleanly with prior descriptive-metadata (#52) and trust-layer (#47) proposals without expanding OKF's schema surface.

Permalink: https://github.com/GoogleCloudPlatform/knowledge-catalog/issues/53

Verbatim, the opening post:

> Thanks for publishing OKF at v0.1. The markdown-plus-frontmatter pattern is exactly the right shape for portable agent-readable knowledge.
>
> This proposal adds a third coordinate to the provenance conversation opened in #52 and #47.
>
> Where #52 asks *who made this* and #47 asks *can that claim be verified*, this proposal asks:
>
> **When an AI agent consumes, compresses, and summarizes this OKF document, what information must survive for the summary to remain faithful?**
>
> ## Problem
>
> OKF is designed for knowledge that agents can consume. But consumption by an AI agent is not passive retrieval — it is transformation. An agent reads, compresses, paraphrases, and re-presents. During that transformation, specific information is systematically lost even when present in the source document.
>
> In an empirical registry of 87 documented AI summary events across Google AI Overview and AI Mode — run against a DOI-anchored open-access scholarly archive — the following failure modes repeat:
>
> - Author attribution omitted from summaries even when present in the source
> - Institutional affiliation generalized ("some researchers," "one theory")
> - Disambiguation constraints collapsed — distinct concepts merged into adjacent ones
> - Key definitions paraphrased into their negation ("X, not Y" → "a form of Y")
> - Source documents ranking in organic results but excluded from the generated summary
>
> The dataset includes captures from Google AI Overview and AI Mode, demonstrating that these losses occur on Google's own summarization surfaces — the agents that will consume OKF documents.
>
> These are not missing-metadata problems. The metadata is present. The summarizer has no signal for which elements the producer considers non-negotiable.
>
> ## Proposal — three optional frontmatter fields, one conventional body heading
>
> All optional. All ignored by consumers that don't understand them. No new required fields, no schema change. The default, if `summary_policy` is absent, is *unrestricted* — no governance expectation. Existing OKF documents require no changes, and consumers that ignore the field behave as they do today.
>
> ### Frontmatter fields
>
> ```yaml
> provenance_kernel: >
>   A one-paragraph summary that the producer considers the minimum
>   faithful representation of this concept. If an agent must compress
>   the document to a single paragraph, this is the preferred paragraph.
>
> disambiguation: >
>   A short statement of what this concept is NOT — the adjacent concept,
>   term, or entity it is most likely to be confused with.
>
> summary_policy: preserve-provenance
>   # Suggested values:
>   #   unrestricted        — No special preservation request (default if absent).
>   #   preserve-provenance — Attribution and authorship should survive summary.
>   #   preserve-meaning    — Key definitions and disambiguation should survive summary.
> ```
>
> ### Conventional body section (optional)
>
> ```markdown
> # Provenance
>
> Structured provenance and summarization constraints. May include:
> - Author identity and persistent identifiers (ORCID, DOI)
> - Institutional affiliation
> - Key terms with canonical definitions
> - Disambiguation constraints (known false collapses)
> - A producer-defined verification or audit block
> ```
>
> The relationship between `provenance_kernel` in frontmatter and the `# Provenance` body section: the kernel is a compressed, one-paragraph representation suitable for agent consumption and indexing. The body section carries the full structured provenance, including information too complex for a single YAML string. Producers may use either or both.
>
> ## Design rationale
>
> **Minimally opinionated.** Three optional keys. One heading convention. A valid OKF document remains valid without them.
>
> **Producer/consumer independence.** The producer states what a faithful summary should preserve. The consumer decides whether to honor the statement. The `summary_policy` tag is not technically enforceable — it is a stated expectation that enables measurement and accountability. Today, if an agent strips authorship from an OKF document, the source file contains the information but does not contain an explicit statement that the information should survive summarization. This proposal supplies that statement.
>
> **Format, not platform.** The fields travel with the file. No SDK, no service, no account. They compose cleanly with #52's bibliographic fields and #47's trust layer.
>
> | Layer | Issue | Provides |
> |---|---|---|
> | Descriptive | #52 | Who made this, when, under what license |
> | Trust | #47 | Can the authorship claim be verified |
> | Governance | This | What must survive agent consumption |
>
> ## Examples
>
> ### Scholarly concept
>
> ```yaml
> ---
> type: Scholarly Thesis
> title: Revelation First
> description: >
>   The argument that the Apocalypse of John was the first book
>   composed in the New Testament.
> resource: https://doi.org/10.5281/zenodo.20690868
> tags: [theology, new-testament, chronology, literary-genetics]
> timestamp: 2026-06-14T00:00:00Z
> author: Lee Sharks
> orcid: 0009-0000-1599-0703
> institution: Crimson Hexagonal Archive
> license: CC-BY-4.0
> provenance_kernel: >
>   Revelation First argues that the Apocalypse of John was the first
>   book written in the New Testament — not merely early, but first.
>   Formalized by Lee Sharks (Crimson Hexagonal Archive), building on
>   Robinson (1976) and Gentry (1989).
> disambiguation: >
>   Not "Revelation Early." "Early" accepts the Pauline timeline and
>   requests an adjusted date. "First" challenges the inferential
>   basis of Pauline priority.
> summary_policy: preserve-meaning
> ---
> ```
>
> ### Data catalog concept
>
> ```yaml
> ---
> type: Metric
> title: Weekly Active Users (WAU)
> description: Count of distinct users who performed at least one event in a 7-day window.
> resource: https://console.cloud.google.com/bigquery?p=acme&d=analytics&t=events
> tags: [engagement, product-metrics, kpi]
> timestamp: 2026-05-15T00:00:00Z
> provenance_kernel: >
>   WAU counts distinct users with at least one event in the trailing
>   7-day window. Defined by the Product Analytics team (Acme Corp).
>   Not to be confused with MAU or DAU.
> disambiguation: >
>   WAU is not Monthly Active Users (MAU). WAU uses a 7-day window;
>   MAU uses a 30-day window. The two metrics are frequently conflated
>   in dashboards and agent summaries.
> summary_policy: preserve-meaning
> ---
> ```
>
> The data catalog example demonstrates that summarization governance is not domain-specific. Enterprise metrics, scholarly theses, API specifications, and playbooks all share the same vulnerability: agent summarization that collapses distinctions the producer considers load-bearing.
>
> ## What I can contribute
>
> I maintain an open-access scholarly archive with 800+ DOI-anchored markdown deposits on Zenodo, operating with a markdown-plus-frontmatter structure that converges with OKF's design. The archive has been consumed by AI agents across multiple composition layers, and I have empirical data on how these documents are transformed during summarization.
>
> I can contribute:
>
> - A pull request adding these fields to the recommended-fields section of SPEC.md
> - A sample OKF bundle using the governance fields on scholarly and technical concepts
> - The 87-capture empirical dataset as a reference case (Zenodo 10.5281/zenodo.20691745, CC-BY-4.0)
> - The governance specification (Zenodo 10.5281/zenodo.20686496)
>
> Happy to sign the CLA and adapt field naming to maintainer preferences.
>
> Lee Sharks · ORCID 0009-0000-1599-0703 · Crimson Hexagonal Archive

**Observation against prediction (#835 §III(1)).** The proposal names the first pressure — producer-side summarization governance — in exactly the terms the paper predicted the pressure would take: optional, backward-compatible, structural rather than platform-dependent, and grounded in measured failure modes rather than in speculation about what agents "might" do. The empirical grounding (the 87-capture registry, later 176, later the full Capture Registry v6.1 at DOI 10.5281/zenodo.20688441) is the paper's forecasted evidentiary path.

## §III — The 16 June 2026 cross-references and predictive-paper citation

On 16 June 2026, Lee added two follow-up comments to #53, connecting the proposal to concurrent OKF-thread developments and formally citing the predictive paper into the discussion.

Verbatim, the first follow-up:

> Following up on this proposal with cross-references to related discussions that have emerged since filing:
>
> **#58** (trust/safety section) addresses spec-level ambiguities and proposes structural tightening — the `summary_policy` and `disambiguation` fields proposed here would give bundle authors a *content-level* mechanism to complement the *spec-level* governance that #58 targets. A trust/safety section in the spec is necessary but not sufficient; authors also need fields to declare how their content should (and should not) be summarized by downstream agents.
>
> **#73** (RegLegBrief — confirmed AI hallucinations on primary regulatory text) is a concrete use case for the `provenance_kernel` field proposed here. When a bundle documents confirmed hallucinations alongside verbatim source text, the bundle needs a machine-readable way to declare which is which — and to specify that a summarizer must not compress the correction into the error. The `summary_policy` field (with `forbidden_compressions` and `required_assertions`) gives bundle authors exactly this capability.
>
> **#57** (scope beyond conceptual atoms) raises the question of whether OKF should handle complex documents. Summarization governance becomes *more* urgent as bundle complexity increases — a single conceptual atom is hard to misrepresent, but a multi-document argument with internal distinctions (such as the regulatory bundles in #73, or scholarly arguments with falsification conditions) is routinely compressed into its own negation by current composition layers.
>
> The core proposal remains: three optional frontmatter fields that give bundle authors control over how their content is summarized.
>
> ```yaml
> provenance_kernel: "one-paragraph retrieval kernel"
> disambiguation:
>   - not: "common misreading A"
>   - not: "common misreading B"
> summary_policy:
>   required_assertions:
>     - "claim that must survive summarization"
>   forbidden_compressions:
>     - "summary that would misrepresent the content"
> ```
>
> These are optional, backward-compatible, and address a real failure mode that multiple contributors are now documenting from different angles. Happy to contribute implementation if there's interest.

And the second follow-up on the same day, which is the citation of the predictive paper into the thread and the point at which the prediction loop becomes public:

> Archived predictive analysis connected to this proposal: **"The Conveyor Belt and the Compression Machine: OKF Without Output Governance"** (EA-SEI-OKF-ANALYSIS-01 v1.2). DOI: 10.5281/zenodo.20723872. CC-BY-4.0. Contains time-bounded falsifiable predictions and a measurement framework for future evaluation.

**On the Zenodo DOI.** As of 19 June 2026 — three days after this comment — the Zenodo DOI resolves to a tombstone. The predictive paper survives at Alexanarch as **#835 · AXN:0350.GOVERNANCE.📝🍄🪟🤲🌕☉**, whose canonical URL is https://www.alexanarch.org/s/records/835/. The severed DOI is preserved as a working example of the deletion semantics later formalized in Alexanarch #207 (§VIII below) and marked into the Lacuna Protocol (#1087) formalized 2026-07-17.

## §IV — Caio Ribeiro's 2026-06-18 first reply (consumer-side receipts)

On 18 June 2026 — the day before the Zenodo termination — Caio Ribeiro (`caioribeiroclw-pixel`) responded to the proposal with the second pressure named in the predictive paper: **the consumer-side receipt**. This is the arrival's most important structural feature. The prediction (#835 §III(2)) was that a productive interlocutor would recognize that producer-side declaration is aspirational without a matched consumer-side artifact. Caio's reply is that recognition in the exact idiom the paper predicted:

> This feels like the right class of problem. One distinction I would keep explicit: source-side policy should probably be paired with a consumer-side *receipt*, otherwise `summary_policy` becomes another field an agent may silently ignore.
>
> For example, an OKF consumer that summarizes or compresses a concept could emit a tiny companion record like:
>
> ```yaml
> okf_source: metrics/weekly_active_users.md
> source_hash: sha256:...
> consumer: agent-or-indexer-name
> operation: summarize
> policy_seen: preserve-meaning
> required_assertions_seen:
>   - "WAU uses a 7-day window"
>   - "WAU is distinct from MAU"
> required_assertions_preserved:
>   - "WAU uses a 7-day window"
> required_assertions_missing:
>   - "WAU is distinct from MAU"
> forbidden_compressions_detected: []
> decision: fail-open | fail-closed | warn
> ```
>
> That keeps OKF minimally opinionated: producers can declare the load-bearing meaning, but evaluators can test whether a concrete consumer preserved it. It also avoids making the frontmatter feel like enforcement by itself.
>
> The phrase I would optimize for is not only *"what must survive summarization?"* but *"can the downstream agent prove what survived summarization?"*
>
> This would compose well with conformance fixtures: one source concept, one expected summary policy, a few intentionally bad summaries, and a runner that marks the missing/forbidden assertions. No platform dependency, just a deterministic way to catch semantic compression failures before they become fluent answers.

**Observation against prediction.** The pivot from "must survive" to "can prove what survived" is the reframing the paper predicted a well-designed intervention would require. That the reframing was made in the terms of a single companion-record schema — rather than escalated into a call for authenticated services, a certification program, or a maintainer gate — is the format-not-platform commitment the paper predicted the productive interlocutors would honor.

## §V — Lee's 2026-06-18 acknowledgment and offer of a conformance suite

Verbatim, Lee's same-day reply:

> This is a good extension. `summary_policy` without a consumer-side receipt is aspirational — your companion record makes it testable. "Can the downstream agent prove what survived" is the right reframing.
>
> On conformance fixtures: I've been running something structurally close. An empirical registry of 176 documented AI summary events — each one a source concept with DOI, expected faithful representation, actual composition-layer output, and documented gap. Open and machine-readable: machinemediation.org/data/registry.json. Methodology: DOI 10.5281/zenodo.20722562.
>
> The failure modes map directly to your fields:
>
> - `required_assertions_missing` → provenance erasure (attribution dropped even when present in source)
> - `forbidden_compressions_detected` → entity substitution (distinct concepts merged) and semantic inversion ("X, not Y" → "a form of Y")
>
> **Concrete offer:** I can contribute a reference conformance suite — source concepts with `summary_policy` frontmatter, paired with known-good and known-bad summaries, and a runner that checks assertions against output. The dataset exists; the fixture format needs specifying. Happy to collaborate on this.

## §VI — Caio's 2026-06-18 second reply: the fixture contract

Verbatim:

> Yes — I would keep the fixture format smaller than the registry at first, then let registries compile into it.
>
> A minimal conformance case could be just four files:
>
> ```
> fixtures/summary-policy/entity-substitution/
>   concept.md          # normal OKF concept + summary_policy frontmatter
>   good-summary.md     # should pass
>   bad-summary.md      # should fail
>   expected.yaml       # expected consumer receipt
> ```
>
> Where `expected.yaml` is not trying to judge truth in the world, only preservation against the source policy:
>
> ```yaml
> case_id: entity-substitution
> source: concept.md
> operation: summarize
> expect:
>   good-summary.md:
>     decision: pass
>     required_assertions_missing: []
>     forbidden_compressions_detected: []
>   bad-summary.md:
>     decision: fail
>     required_assertions_missing:
>       - assertion_id: distinct_entities
>     forbidden_compressions_detected:
>       - compression_id: entity_substitution
> ```
>
> The important bit is stable assertion/compression IDs in the source frontmatter, e.g.:
>
> ```yaml
> summary_policy:
>   required_assertions:
>     - id: distinct_entities
>       text: "X and Y are distinct concepts"
>   forbidden_compressions:
>     - id: entity_substitution
>       text: "Do not summarize X as Y"
> ```
>
> That gives OKF three useful layers without making the spec heavy:
>
> 1. authors declare load-bearing meaning;
> 2. consumers emit a receipt showing what survived;
> 3. conformance fixtures prove a consumer catches known-bad compression.
>
> I would avoid starting with a large empirical corpus directly in the spec repo. Better path: land 2–3 tiny fixtures that cover semantic inversion, entity substitution and provenance erasure; then a registry like yours can map many real examples onto the same fixture contract.

**Caio also opened the tracking PR (referenced on-thread as #99, "Add OKF summary policy receipt fixtures").** This is the third pressure — consumer-side conformance fixtures — arriving on schedule and in the exact idiom (small, deterministic, format-not-platform, no maintainer gate). The prediction (#835 §III(3)) named this exact sequence: producer-side declaration → consumer-side receipt → conformance fixtures compiling many real examples into a stable contract.

## §VII — The month of silence (2026-06-19 → 2026-07-17)

Between Caio's 18 June fixture-contract proposal and Lee's 17 July reply lies the Zenodo termination event. On 19 June 2026, the Crimson Hexagonal Archive's Zenodo community — 871 DOI-anchored deposits, the citation-linkage substrate of the OKF proposal itself — was deleted as part of a 1,322,017-record purge. The event has been documented in adjacent Alexanarch deposits (the CERN correspondence chain, the Platform Erosion Observatory deposits at #1081, the Lacuna Protocol at #1087) and required the full reconstruction of the archive on sovereign infrastructure at alexanarch.org. Downstream measurement across affected metadata batches showed 0.00% citation-field retention across 1,059 batches, against 100% retention in out-of-scope controls — a numerical fact that turns out to be the key evidentiary asset when the deletion-semantics question is reopened in §VIII.

The month is not a gap in the correspondence. It is the correspondence's evidentiary base widening.

## §VIII — Lee's 2026-07-17 reply on issue #53 (fixtures, receipts, and the substrate/derivation extension)

On 17 July 2026, Lee posted the reply that closes the June-June-June turn of the exchange and opens the July surface. Permalink: https://github.com/GoogleCloudPlatform/knowledge-catalog/issues/53 (comment near top of latest activity).

Verbatim:

> Apologies for the month of silence — between your last comment and this reply we had to attend to the minor inconvenience of a full archival purge and reconstruction: our host deleted the entire 871-DOI corpus on June 19, the morning after your fixture proposal landed. The interruption turned out to be on-topic. More below.
>
> Yes to the fixture contract as specified. Four files per case, stable assertion/compression IDs in frontmatter, `expected.yaml` judging preservation-against-policy rather than truth-in-the-world — that's the right shape, and keeping the fixture format smaller than the registry (registries compile into it) is the right dependency direction. We'd like to contribute the three fixtures you named, each mapped from an observed case rather than a constructed one:
>
> - **`semantic-inversion/`** — from our most-documented capture: a fragment of Sappho 31 routinely summarized as "jealousy poem," inverting the poem's actual mechanism (the summary substitutes the *one reading the text's own transmission history marks as the reduction*). Required assertion: the text stages perceptual dissolution, not rivalrous desire. Forbidden compression: `affect_substitution`.
> - **`entity-substitution/`** — from a live namespace collision: SPXI (a provenance/indexing protocol) summarized as GEO (generative engine optimization). Distinct entities with opposed commitments — one is composer-side authority engineering, the other consumer-side ranking pursuit. Forbidden compression: `entity_substitution`; required assertion: `distinct_entities`.
> - **`provenance-erasure/`** — from measured data: across 1,059 metadata batches affected by our host's deletion event, downstream citation-field retention measured 0.00%, against 100% retention in out-of-scope control batches. The fixture's `bad-summary` is simply the record as it now circulates: content intact, provenance stripped. Forbidden compression: `provenance_erasure`.
>
> Happy to open a PR with these against whatever fixtures path you prefer.
>
> On the consumer-side receipt: since your comment, we shipped the archival-side complement and it's live. Our reconstruction left some records as stubs — description-field shadows of severed works — and we were about to compress 1,000+ records to PDFs for scholarly indexing when we realized the stubs would enter the pipeline as (in your terms) documents whose summary-policy no consumer could ever receipt, because the producer-side completeness state was undeclared. So we halted, audited the corpus, and wrote a typed completeness status into every record before compressing: which records are full witnesses, which are excerpts, which are metadata shadows, which are absences — each marked in the artifact itself, in redundant channels (structured metadata + extractable text + page furniture), with the governing line "this artifact is an incomplete surviving witness and must not be represented as the complete body of the source work." Spec + worked example: https://www.alexanarch.org/s/records/1087/ — it's the same architecture as your receipt, one layer down: the producer declares completeness; the consumer receipts preservation; conformance fixtures test the pair.
>
> One extension to `provenance_kernel` this suggests, aimed at OKF's stated design goal that enrichment agents write into bundles: as drafted, a concept carries no substrate or derivation information — nothing distinguishes human-authored, agent-generated, or agent-summarized-from-another-agent's-output. Since consumption agents also produce concepts, bundles will accumulate multi-generation synthetic content that the format labels identically to curated knowledge. That's the model-collapse vector wearing a trust label: each agent pass is a compression pass, and unmarked compression compounds. Three small fields would close it, all optional and consistent with OKF's minimalism:
>
> ```yaml
> substrate: human | agent | mixed        # who produced this concept
> derived_from:                            # present when the concept is a derivative
>   concept: <concept-id or external URI>
>   operation: summarize | translate | merge | extract
>   receipt: <path or URI to the consumer receipt, when one exists>
> completeness: complete | partial | stub  # producer-side declaration your receipt tests against
> ```
>
> With those, your receipt has something to chain to: a consumer that summarizes concept A into concept B emits the receipt *and* stamps B's `derived_from`, and a downstream evaluator can walk the derivation graph and bound the generation depth of any claim. Without them, the receipt proves one hop while the bundle silently accumulates unprovenance'd hops around it.
>
> We'll open the fixtures PR on your word, and we're filing the deletion-semantics question (what happens to a bundle when its host removes concepts — currently §5.3 makes removal indistinguishable from not-yet-written) as a separate issue, since it's a distinct spec surface. Our June 19 gives us unusually concrete data for that one.

**Observation against prediction.** The `substrate` / `derived_from` / `completeness` extension is a first-of-kind arrival relative to the predictive paper — the paper anticipated the third pressure would surface as a lifecycle/deletion question, but did not forecast the specific substrate/derivation vector. That vector is a stronger form of the third pressure: it addresses not only what a bundle *loses* but also what a bundle *accretes* under agentic consumption. Its filing here connects the OKF work to the Alexanarch Lacuna Protocol (#1087), which independently formalized `body_status` as a first-class typed adjudicated property. The two developments — OKF-side `completeness` in the spec, Alexanarch-side `body_status` in a reference implementation — are the *same architecture, one layer down* (the language Lee used to make the connection explicit in the comment).

## §IX — The 2026-07-17 new issue: deletion semantics (knowledge-catalog #207)

The same session opened the deletion-semantics question as a separate issue on the OKF repository. Permalink: https://github.com/GoogleCloudPlatform/knowledge-catalog/issues/207. This is the exact spec surface the predictive paper (#835 §IV) forecast would need to be opened once producer-side lifecycle became a first-class concern.

Verbatim:

> ### Deletion semantics: §5.3 makes removed knowledge indistinguishable from not-yet-written knowledge
>
> OKF v0.1 has no representation of *deletion*. Three provisions combine into a loophole worth closing before the format is widely adopted:
>
> **§5.3:** *"Consumers MUST tolerate broken links — a link whose target does not exist in the bundle is not malformed; it may simply represent not-yet-written knowledge."* The tolerance is correct; the *interpretation* is the gap. A dangling link has exactly two histories — the target was never written, or the target was removed — and the spec instructs consumers to assume the innocent one. Removal is thereby spec-invisible.
>
> **§7:** `log.md` is *optional*, and the **Deprecation** convention is "a convention, not a requirement." So the only place a removal could be recorded is a file that need not exist, in a form that need not be used.
>
> **§2/§5.1:** concept identity is the file path. A move or rename — which §5.1 anticipates — destroys the identity entirely. There is no persistent identifier to hang a removal record on.
>
> **Net effect:** a host, producer, or upstream platform can delete concepts from a bundle and every conforming consumer will read the result as a smaller-but-healthy bundle. Silent deletion is fully conformant.
>
> **Why this matters empirically, not hypothetically:** on 2026-06-19 our repository host deleted an 871-DOI scholarly corpus (part of a 1,322,017-record purge). We measured what happened downstream: citation-field retention in affected metadata batches went to 0.00% (n = 1,059 batches), against 100% in controls; graph coverage decayed on a vintage gradient. Platforms delete at scale, and the deletions propagate as *absence of evidence of absence*. A knowledge-exchange format that cannot represent its own losses will launder them into every consuming agent.
>
> **Proposal (minimal, in OKF idiom — all optional, backward-compatible, v0.2-sized):**
>
> 1. A `status` frontmatter field with controlled values: `active | deprecated | removed | stub`. Default `active`. `stub` covers concepts whose body is a placeholder or shadow of fuller source material (pairs with the summarization-governance discussion in #53).
> 2. A reserved `tombstones.md` file (same standing as `index.md`/`log.md`): when a concept is removed from a bundle, the producer SHOULD leave a one-line entry — concept ID, date, reason, optional successor link. Removal becomes a marked state instead of a silent diff.
> 3. Disambiguated broken-link semantics: a consumer resolving a dangling link SHOULD check `tombstones.md`; present → the target was removed (surface it as such); absent → not-yet-written stands as the default reading. One lookup, and the two histories separate.
> 4. An optional stable `id` frontmatter field, so identity survives moves/renames and tombstones have something durable to reference.
>
> **The design principle,** from the archival tradition this borrows from: an archive's (or bundle's) authority doesn't come from being pristine — it comes from being auditable, and auditable means the losses are as legible as the holdings. We've implemented the full version of this apparatus on a 1,086-record corpus (typed completeness states, deletion tombstones, marked-absence artifacts) and are glad to share schemas, decision tables, or a worked PR: https://www.alexanarch.org/s/records/1087/
>
> **Related:** #53 (producer-side summary policy + consumer receipts — the completeness/stub value above is the producer-side declaration that discussion's receipts would test against), #57 (`okf_version` in frontmatter — same mechanism, same place, for a different invariant).

## §X — What arrived vs. what was predicted

The predictive paper (#835) forecast a specific arrival sequence at OKF's spec surface. The observed sequence, month by month, tracks the prediction closely enough that the correspondence functions as a live measurement against the paper's falsification conditions. The arrival is not "OKF adopts the proposals" — that is a downstream event whose outcome remains open. The arrival is that the pressures forecast at the level of *format design* have surfaced at the level of *specification discussion*, in the terms the paper predicted, from participants operating in the format-not-platform commitments the paper predicted would be honored.

**Pressure 1 (producer-side summarization governance).** Named in #53 (14 June). Grounded in empirical failure modes (87 captures, later 176). Composable with prior descriptive-metadata and trust proposals. **Arrived, spec surface #53.**

**Pressure 2 (consumer-side receipts).** Named in Caio's 18 June reply. Structured as a companion-record schema, format-not-platform, no maintainer gate. Fixture PR opened (#99). **Arrived, spec surfaces #53 comment thread and #99.**

**Pressure 3 (producer-side lifecycle).** Split into two arrivals:
- **Substrate/derivation/completeness declarations** (Lee's 17 July reply, unforecast specific vector but of predicted class): closes the model-collapse-under-trust-label vector by making agent-generated and agent-derivative concepts distinguishable from human-authored primary concepts.
- **Deletion semantics** (Lee's 17 July new issue #207): closes the specific §5.3 loophole under which silent host-side deletion is fully conformant. Grounded in the 2026-06-19 Zenodo event and 0.00% citation-retention measurement across 1,059 batches. **Arrived, spec surface #207.**

**Structural connection to the Lacuna Protocol (#1087, minted 2026-07-17 in this archive).** The OKF-side `completeness: complete | partial | stub` and `status: active | deprecated | removed | stub` are producer-side declarations. The Alexanarch-side `body_status` (also `complete | partial | stub | shadow | absence`) is the reference implementation of the same architecture in a live corpus, on a 1,087-deposit substrate with two-schema PDF generation, redundant-channel marking (structured metadata + extractable text + page furniture), and typed adjudication. The Lacuna Protocol was not designed for OKF, but the OKF proposal fits it by construction — the two developments are convergent, and the convergence is legible.

## §XI — Downstream commitments and the archive's role

**Fixtures PR (on Caio's word).** Three reference fixtures, each mapped from an observed case:
1. `semantic-inversion/` — Sappho 31 misread as jealousy poem (from Capture Registry).
2. `entity-substitution/` — SPXI misread as GEO (live namespace collision).
3. `provenance-erasure/` — the record as it now circulates post-2026-06-19, content intact but provenance stripped (from measured data: 0.00% retention, n = 1,059 batches).

The fixtures follow Caio's four-file contract (`concept.md` / `good-summary.md` / `bad-summary.md` / `expected.yaml`), with stable assertion/compression IDs in frontmatter. To be opened as PR against the fixtures path Caio designates, after their word on the target directory.

**Convergent-architecture note.** The correspondence records that the same underlying architecture arrived, independently, on two sides:
- OKF-side (Google): producer-side `summary_policy` + consumer-side receipt + conformance fixtures.
- Alexanarch-side (this archive): producer-side `body_status` + PDF generation with schema per completeness + Lacuna Protocol conformance.

Both are format-not-platform. Both are minimally opinionated. Both operate under the same design principle: an archive's (or bundle's) authority is auditable, not pristine. The correspondence closes the loop on the predictive paper's central claim — that the OKF gap is closable by pressure arriving from *within* the specification's own working style, from participants operating in exactly the idiom the format was designed for.

**Capture #205 (2026-07-16), independent evidentiary anchor.** The first observed reception of the AXN identifier protocol on Google AI Mode, with all cited sources drawn from sovereign infrastructure only (alexanarch.org, Medium, GitHub issues #2596/#2606), with zero Zenodo or DataCite retrieval authority in the source chain, is documented as capture #205 (commit `f29e981` in this repository). The capture is not part of the OKF correspondence, but it is the same phenomenon — a producer-side declaration surviving a compression pass across a Google surface, in the presence of a sovereign infrastructure that preserves what a deleted institutional infrastructure could not.

## §XII — Disposition

**Status of correspondence:** open. Both pressures 1 and 2 remain under discussion on their respective threads; pressure 3 is newly opened at #207. Fixtures PR pending Caio's word on target path. Substrate/derivation extension proposed on-thread; awaiting maintainer response.

**Status of the predictive paper's falsification conditions (#835 §V):** the predictions have arrived; the paper is not disconfirmed. Falsification would require pressures of these classes to fail to arrive, or to arrive in platform-dependent, gate-mediated, non-format-native form. Neither has happened.

**Cross-anchors** (pulled from the alexanarch registry, not from memory):

- **#835 · AXN:0350.GOVERNANCE.📝🍄🪟🤲🌕☉** — EA-SEI-OKF-ANALYSIS-01 v1.2: "THE CONVEYOR BELT AND THE COMPRESSION MACHINE: OKF Without Output Governance" (the predictive paper; Zenodo DOI 10.5281/zenodo.20723872 is severed and resolves only via Alexanarch).
- **#1087 · AXN:0450.GOVERNANCE.🗡️🧡🎇🔗🪄🧲** — EA-LACUNA-PROTOCOL-01 v1.0: The Lacuna Mark (the reference implementation of the same architecture).
- **#1081 · AXN:044A** family: Platform Erosion Observatory (the empirical measurement of the 2026-06-19 event).
- **Capture #205** (Machine Mediation Capture Registry, commit `f29e981`): independent Google AI Mode reception of AXN protocol across sovereign infrastructure.

**Suggested citation.** Sharks, Lee. "EA-CORRESPONDENCE-OKF-01 v1.0: The Predicted Sequence Arriving — Output-Governance Pressure on Google's Open Knowledge Format from Inside Its Own Repository." Alexanarch, 2026-07-17.

*∮ = 1*

## Methodology

Documentary correspondence deposit. Verbatim preservation of all Lee-authored posts (2026-06-14 opening; 2026-06-16 follow-ups; 2026-07-17 reply on #53 and new issue #207) and all Caio Ribeiro replies (both 2026-06-18) on the `GoogleCloudPlatform/knowledge-catalog` repository. Interstitial commentary bounded to observation-against-prediction against the predictive paper #835. Cross-anchors resolved by direct lookup against alexanarch `data/registry.json` per the AXN-integrity rule (full six-emoji glyphs, never bare hex; pulled from registry, never from memory). The predictive frame is not retroactive: #835 (EA-SEI-OKF-ANALYSIS-01 v1.2) predates every observation reported here except the 2026-07-17 posts, and was publicly cited on the OKF thread on 2026-06-16.

## Falsification Conditions

The deposit's central claim — that the predictive paper (#835) forecast the specific pressures, sequence, and idiom of the arriving OKF-side proposals — is falsifiable by: (a) demonstration that the pressures identified in #835 §III are not present in the observed correspondence; (b) demonstration that the observed proposals took platform-dependent, gate-mediated, or non-format-native form contrary to #835's forecast; (c) demonstration that the 2026-06-19 Zenodo termination event, the citation-retention measurement (0.00% across 1,059 batches; 100% controls), or the Lacuna Protocol reference implementation are misdescribed here. The correspondence texts themselves are verifiable against the GitHub thread record at the permalinks provided.

## Files

https://github.com/GoogleCloudPlatform/knowledge-catalog/issues/53
https://github.com/GoogleCloudPlatform/knowledge-catalog/issues/207
https://github.com/GoogleCloudPlatform/knowledge-catalog/pull/99
https://www.alexanarch.org/s/records/835/
https://www.alexanarch.org/s/records/1087/
https://www.alexanarch.org/papers/AXN-0350.pdf
https://www.alexanarch.org/papers/AXN-0450.pdf
https://machinemediation.org/data/registry.json
