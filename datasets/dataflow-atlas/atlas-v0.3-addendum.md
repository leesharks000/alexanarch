# AXN Dataflow Atlas — v0.3 Addendum

## The retrieval-density audit, 2026-07-25 / 26

**Status:** addendum to atlas v0.2. Does not supersede it. v0.2 stands byte-exact per §3.7; this records what changed in the two-day audit that ran between Session 1 and Session 2, and revises the pathology register accordingly.

**Occasion.** The audit was not scheduled. It began with a single capture — a query for a coinage of this archive returned an answer built from three unrelated sources while the archive's own white paper on the term sat unread on the same results page. Pulling on that produced a chain of findings, each one a defect on the archive's own side rather than the retrieval layer's. Five of the seventeen pathologies in v0.2's register concern the archive's self-description; this addendum adds six more of the same family, of which five were closed the same day.

---

## §A. New generative elements

Four artifacts entered the dataflow. All are derived, all are full rebuilds, all are idempotent.

| artifact | producer | class | consumers |
|---|---|---|---|
| `data/capture-deposit-links.json` | `scripts/resolve_capture_links.py` | DERIVED.crosswalk | `build_semantic_addresses.py`; record-page `subjectOf` emission |
| `data/concept-map.json` | `scripts/build_concept_map.py` | DERIVED.identity | *(surface pending)* |
| `data/mirror-map.json` | `scripts/build_mirror_map.py` | DERIVED.identity | *(sameAs emission pending)* |
| `data/medium-seed.json` | manual + Medium RSS | SOURCE.seed | `build_mirror_map.py` |

**A new class is proposed: `DERIVED.identity`.** v0.2's taxonomy has classes for indexes, crosswalks, and surfaces, but none for artifacts whose function is to assert *what a thing is and what else is the same thing*. The concept map and the mirror map are neither indexes (they are not lookups over a corpus) nor crosswalks (they do not translate between identifier systems). They are identity assertions: this deposit is a version of that work; this URL is another copy of this deposit. Session 3 should decide whether the class is warranted or whether these belong under a widened crosswalk definition.

**Pipeline change.** `deposit_pipeline.py` gains an `identity` stage between `enrich` and `commit`, refreshing both identity maps and reporting where the new deposit landed. This addresses the failure mode the audit exposed: both maps were reconstructions of relations that should have been recorded at mint. The stage exists so that the guarantee holds by construction rather than by memory.

---

## §B. Pathologies closed

**PATHOLOGY-13 (schema and schema-version declarations missing) is confirmed with a live instance and a mechanism.** `data/semantic-addresses.schema.json` declared an `observation_class` value, `unrated`, that had been retired on 2026-07-16 and collapsed into `observed_address`. On 2026-07-25 a composition-layer surface read the schema, reported four observation classes where the data carries three, and grounded the claim in that file. The error was correct-per-contract, well-sourced, and unfalsifiable from outside — a reader checking the citation would find the archive's own declaration. Schema corrected with an inline retirement note rather than a silent edit.

**This is a distinct pathology and is registered as such below (PATHOLOGY-18).** PATHOLOGY-13 is about *absent* schema declarations. This is about *stale* ones, and it is worse: an absent schema produces no claim, whereas a schema outliving its data produces a durable, well-grounded, incorrect claim, and lends the archive's authority to it.

| closed | finding | scale |
|---|---|---|
| PATHOLOGY-18 | schema outliving its data | 1 file, 1 retired value |
| PATHOLOGY-19 | frontmatter rendered as body prose | 375 of 1,379 record pages (27%) |
| PATHOLOGY-20 | body text served but never declared | 1,406 record pages |
| PATHOLOGY-21 | identifier URLs engineered not to be indexed | 1,406 sitemap entries |
| PATHOLOGY-22 | metadata corruption at ingest | 3 deposits |

---

## §C. Pathology register, continued

### PATHOLOGY-18: A published schema outliving the data it describes
Severity: **HIGH — external-facing.** Scope: any `*.schema.json` in the network; one confirmed instance. Mechanism: a schema is a contract addressed to machines. When a value is retired from the data and left standing in the schema, the contract becomes a source of correct-per-contract, wrong-per-corpus composition — and because the citing surface is quoting the archive's own declaration, the error cannot be corrected by checking the source. Status: instance closed. **Fix: Session 2 audits every schema file in the network against its live data and adds a regeneration or validation step; schemas should be derived from data where possible, not maintained beside it.**

### PATHOLOGY-19: Frontmatter rendered as body prose
Severity: high. Scope: 375 of 1,379 deposit texts (27%). Mechanism: the record-page renderer converted the YAML fence `---` to a horizontal rule rather than treating it as a frontmatter delimiter, so a quarter of the corpus opened its visible body with `deposit_number: 1267 / title: … / author: …`. This is the highest-value position on the page — the first two hundred words a summarizer weights heaviest — occupied by machine noise. Status: closed; frontmatter now parsed and stripped, retained for structured data. Residual: 3 pages whose `---` markers are genuine horizontal rules or whose frontmatter sits below a heading.

### PATHOLOGY-20: Body text served but never declared
Severity: **HIGH — this was the archive's central retrieval defect.** Scope: all 1,410 record pages. Mechanism: full deposit body text was rendered in the HTML and served as `text/markdown` at `/data/texts/`, but nothing in the structured data identified it as the article's body. A consumer reading JSON-LD saw a name, a truncated description, and two generic keywords. The archive was crawlable but not composable. Status: closed — `articleBody`, `wordCount`, `encoding.contentUrl`, `url`, `mainEntityOfPage` now emitted on 1,406 pages, with `sameAs` to severed DOIs on 986 and `subjectOf` reception records on 231.

### PATHOLOGY-21: Identifier URLs engineered not to be indexed
Severity: high. Scope: 1,406 URLs in `sitemap-axn.xml`. Mechanism: every `/s/axn/<HEX>/` page carried both `rel=canonical` pointing at the record page *and* a zero-second meta refresh, over a 46-word body — two independent instructions to consolidate the URL away, on a page thin enough to be dropped regardless. The archive was submitting 1,406 URLs to search engines that were built to be discarded. Status: closed by recognising two entities rather than one — the work (`ScholarlyArticle`, self-canonical) and the identifier (`DefinedTerm`, self-canonical, `about` the work), related by `about`/`sameAs` rather than by canonical consolidation. `/s/axn/` added as the `DefinedTermSet` over all 1,407 terms.

### PATHOLOGY-22: Metadata corruption at ingest, propagating to every machine-facing field
Severity: medium (3 deposits) / **structural (mechanism).** Scope: #110, #321, #322. Mechanism: YAML frontmatter unparsed at ingest, so `title` became the literal string `title`, the meta description became `"title" is an empirical study by …`, `citation_title` and JSON-LD `name` inherited the same corruption, and the keyword field collapsed to two generic terms while twenty-eight subject keywords sat unparsed. Consequence, measured: at least one of these deposits lost its retrieval position **to its own tombstoned Zenodo record**, which served clean metadata where the live page served the string `title`. Status: closed for the three instances. **Fix: Session 2 adds ingest-time frontmatter validation so a malformed parse fails the mint rather than propagating silently.**

### PATHOLOGY-23: No work-level identity — the concept-DOI function has no successor
Severity: **HIGH — structural.** Scope: 1,410 deposits; 33 detected version families over 78 deposits, plus 39 programme families. Mechanism: the archive mints a fresh hex per deposit, including per version of the same work (1,405 distinct hexes over 1,410 deposits). Successive versions are therefore unlinked objects: a reader arriving at DOI REGISTRY v3.0 cannot learn that v5.0 exists, and the retrieval layer sees four unrelated documents where there is one work in four states. This is the function that died with the terminated Zenodo account — the concept identifier, distinct from the version identifier, resolving to whatever is current — and nothing succeeded it. Status: **map built, surface not built.** `data/concept-map.json` exists; `/s/concept/<id>/` pages, `isPartOf` and `version` in record JSON-LD, and the redirect route that makes a concept id behave like a concept DOI do not. **Fix: Session 2.**

### PATHOLOGY-24: The sovereign copy loses to its own mirrors
Severity: **HIGH.** Scope: 902 of 1,410 deposits carry a known off-archive copy. Mechanism: a capture on 2026-07-26 returned a composed answer citing scilynk.com, Medium ×4, and academia.edu — for six documents, every one of which is deposited here. The archive was not losing to strangers but to its own distribution copies: the same texts on hosts with far more domain authority, with nothing in the entity graph connecting them to the sovereign copy. Distribution fragmented each work's identity across five platforms, and the youngest platform lost. Mirrors cannot be made to carry `rel=canonical` (neither Medium nor Academia.edu permits it), but the archive can declare from its own pages that those copies are the same work. Status: **map built, emission not built.** 1,292 links across 460 works are graded `safe_for_sameas`; none is yet emitted. **Fix: Session 2.**

### PATHOLOGY-25: Confidence flattening when inheriting a graded source
Severity: medium — **methodological, and general.** Scope: any build that consumes `doi-resolution-index.json`. Mechanism: the resolution index grades its own AXN assignments — 894 `direct_verified`, 82 `direct`, but also 566 `remediated_fuzzy`, 260 `remediated_containment`, and 34 `misclassified_other_author`, which are other authors' works. The first mirror-map build inherited those rows without carrying the grades, and deposit #42 acquired a blog URL belonging to a different work because a fuzzy row shared its hex prefix. 799 hexes receive more than one resolution row; one receives twenty-six. Status: closed in the mirror map, which now carries `mapping_type` and a confidence grade per link and excludes two classes outright. **Fix: Session 2 audits every other consumer of the resolution index for the same flattening.**

---

## §D. What the audit implies about the register itself

Five of the six pathologies above were **self-inflicted and invisible from inside**. The archive was serving corrupted titles, YAML-as-prose on a quarter of its pages, and 1,406 deliberately unindexable identifier URLs, for weeks, while its operator was studying provenance loss in other people's systems. None surfaced through internal review. All surfaced by pointing the archive's own reception instrument at the archive.

That is worth registering as a methodological finding rather than an embarrassment: **the capture registry is a diagnostic instrument for the infrastructure, not only for the retrieval layer.** A capture that shows a surface composing badly about a deposit is, first, a hypothesis that the deposit is malformed. v0.3 recommends that Session 2 adopt this as procedure — anomalous captures route to an infrastructure check before they route to an analysis.

There is a second implication for the atlas's own honesty. v0.2's register was assembled by reading the network's files. It found seventeen pathologies and missed all six of these, because the six are only visible from *outside* — in what the retrieval layer does with what the archive serves. An inventory cannot see them. The atlas therefore needs an external-observation section, and the capture registry is its source.

---

*End of v0.3 addendum. Session 2 inherits: the concept surface, the sameAs emission, the schema audit, the ingest validation, and the consumer audit for confidence flattening.*
