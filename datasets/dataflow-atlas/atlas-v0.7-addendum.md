# Dataflow Atlas — v0.7 Addendum

## PATHOLOGY-30 — A record's condition is stored in ten places and derived from none

**Class:** SURFACE.assertion-drift
**Severity:** urgent — and urgent *because* PATHOLOGY-20 closed. While the archive was crawlable but not composable, a wrong `content_type` was a display nuisance. With `articleBody`, `wordCount` and `encoding.contentUrl` now emitted on 1,406 pages and the OAI-PMH endpoint live and COMPLIANT, the same string is read into `dc:type` and carried outward by every aggregator that harvests it. Closing 20 converted this from cosmetic to propagating.
**Status:** classification instrument built; derivation and gate not yet built

### Statement

v0.5 stated the rule and v0.6 restated it: *a surface may assert only what it reads.* PATHOLOGY-28 established the quantitative case — counts typed into a page rather than read from the dataset. PATHOLOGY-30 is the same mechanism on the qualitative axis.

A record's **condition** — whether the deposited object is a work or a metadata capture — is written independently into ten sites and derived from none of them.

v0.6 registered `canonical_text_status` as a flow with named writers and readers. That registration is incomplete: five further fields carry the same claim, unregistered, with no writer discipline and no refresh path.

### Evidence

Deposit #1344, *Axioms of the Emrick Phase Grid*, audited 2026-07-31. One record, one fact, asserted at ten sites:

| site | what it asserts | derived from |
|---|---|---|
| rendered banner | semi-restored capture | `body_status.class` |
| `content_type` | "Semi-restored record (metadata-only…)" | nothing — stored |
| `version` | "semi-restored v1.0" | nothing — stored |
| keywords ×2 | `semi-restored`, `metadata-only` | nothing — stored |
| `description` | "SEMI-RESTORED RECORD…" | nothing — stored |
| `wiki_article` | "is a 430-word semi-restored record…" | nothing — stored |
| body ¶1 | `## Description / SEMI-RESTORED RECORD…` | immutable bytes |
| body ¶2 | `SEMI-RESTORED RECORD — metadata capture only` | immutable bytes |
| Methodology | "no live authorial surface passed the body-head gate" | immutable bytes |
| Falsification | "Superseded on sight by any recovered canonical bytes" | immutable bytes |

Two of the ten name **different worklists** — the banner cites `semi-restored-pairing-queue.json`, the description cites `doi-work-identity/restoration-queue.json` — and the second had been retracted hours before the audit. The description text renders three times on one page.

PATHOLOGY-28's diagnostic applies unchanged: *a page cannot disagree with itself about a value it reads from a file; it can only disagree about a value it stores in several places.* #1344 disagrees with itself about which queue it is in.

**A second instance, recorded because it is the same rule failing at the level of this document.** On 2026-07-31 the Atlas was consulted at `data/specs/AXN-DATAFLOW-MAP-v0.2.md` — a frozen artifact of the v0.2 mint — and treated as current. An amendment was drafted asserting a gap that four subsequent addenda had already closed, and claiming a pathology number in a register that runs to 29. The copy was syntactically valid, resolved cleanly, and had stopped being true. **The canonical Atlas is the dataset series at `datasets/dataflow-atlas/`; the deposit and the `data/specs/` copy are artifacts.**

### Rule extension

Genre and condition are different claims and must not share a field.

**The genre of a metadata capture is `Metadata capture`.** This is not a status flag standing in for a genre — it accurately describes the object deposited. What was deposited is a capture. When canonical bytes are recovered they supersede it and declare their own genre, because that is what they are.

Therefore:

- `content_type` carries genre only. For captures: `Metadata capture`.
- `version` carries a version only. `"semi-restored v1.0"` is malformed on both axes.
- Keywords carry subject only. `semi-restored` and `metadata-only` are not subjects.
- `body_status.class` is the single stored condition. Banner, byline label, wiki descriptor and badges derive from it at render.
- The deposited body is framed as **the deposited text as captured**. Its internal declarations are the artifact's, not the record's current condition. A duplicated `## Description` block is suppressed within the frame. This is adjacent to **PATHOLOGY-19's residual** — the pages whose frontmatter sits below a heading or whose `---` markers are genuine rules — and belongs there rather than re-diagnosed here: 19 closed frontmatter *parsing*; what remains is a duplicated block the parser correctly leaves in place because it is genuine body text that happens to restate the description field.
- A record references at most one worklist, from a derived surface, never from immutable text where it cannot be corrected when the worklist is retracted.

### Instrument

**Built 2026-07-31.** `scripts/classify_bodies.py` — classification from each record's own declaration, matching both capture header forms in use, with an `image_borne` class for bodies whose content is an image reference. Applied: 1,287 full, 131 metadata captures, 2 image-borne; 27 corrections.

**Retracted the same day.** `audit_body_substance.py`'s word-count discriminator, which classified any body under 400 prose words as a stub. Reading all 207 affected bodies found zero stubs among them: it had condemned the complete Greek text of Revelation (its regex counted no Greek), a complete work in emoji notation, two-line poems, registry tables, and the canon provenance nodes whose finished form is ~3.5 KB — while missing captures using a second header form. `data/worklists/restoration-queue.json` carries status `RETRACTED` with entries retained. **Length is not evidence of condition. The declaration is written in words and must be read.**

**Not yet built.** Derivation of banner, byline label and wiki descriptor at render; the field-discipline pass over `content_type`, `version` and keywords; the gate.

### The gate

> **No record page may declare its condition more than once outside the artifact frame.**

Build-time: parse each rendered page, count condition assertions outside the framed body, fail above one. This is the counterpart of PATHOLOGY-28's `data-count` and PATHOLOGY-29's coherence check — an invariant rather than a repair.

**The precedent is PATHOLOGY-22.** Its fix was not a repair of the three corrupted deposits but ingest-time frontmatter validation, so that *a malformed parse fails the mint rather than propagating silently*. This register has already ruled that failing the build beats propagating quietly; PATHOLOGY-30's gate is the same remedy applied to condition rather than to parse.

Rationale for gating rather than trusting: across 2026-07-30–31, six automated audits produced false findings — a truncated sitemap fetch read as a truncated sitemap; 3,206 structured-data findings that were nested reference nodes; a proxy denial read as a site outage; a canonical-tag repair that created duplicates; a locator proposing to restore records from renderings of their own stubs; and the word-count backlog above. In every case the assertion was published before the artifact was opened. A build-time invariant does not depend on the auditor being right.

### Residual

- 131 metadata captures still carry condition in `content_type`, `version` and keywords.
- Derivation and gate unbuilt; until then, corrections propagate asymmetrically.
- The duplicated-description suppression was attempted four times on 2026-07-31 and failed each time, because each attempt patched against an assumed pipeline stage rather than a read one. It is unbuilt, and the render path should be read before the fifth attempt.
- Findings from the records audit in progress must be applied **through** this architecture. Applied around it, each correction lands at one of ten sites and manufactures nine new contradictions.
- One title/body mismatch (#1021: title names Ezra Pound, body is the Sappho node) and eleven byte-identical deposit clusters are recorded at `data/worklists/read-audit-findings.json`, pending ruling.

---

## New flows registered

7. **`body_status.class`** — registry field → banner, byline condition label, OAI `completeness:*` sets, wiki descriptor, browse badges. Writer: `scripts/classify_bodies.py` (declaration-read), MANUS rulings. Readers: `wire_deposit.py`, `build_oai_index.py`, `regenerate_surfaces.py`. **Condition is written here and nowhere else.**
8. **`modifications[]` + `date_modified`** — `scripts/record_modification.py` → sitemap `<lastmod>`, JSON-LD `dateModified`, ResourceSync change list, record-page modification block. Change rule: a modification is a change to the record's metadata or declared state; regeneration and enrichment are not modifications.
9. **OAI-PMH 2.0** — `data/oai-index.json` (`build_oai_index.py`) → `api/oai.js` → `/oai`. Six verbs, `oai_dc`, resumption tokens, selective harvesting by datestamp and set, `deletedRecord: persistent`. OAI validator, 2026-07-31: 38 tests, 0 warnings, 0 errors, **COMPLIANT**.
10. **ResourceSync (ANSI/NISO Z39.99)** — `build_resourcesync.py` → `/.well-known/resourcesync`, capability/resource/change lists. The change list reads `date_modified`, making flow 8 consequential for harvesting.
11. **IndexNow** — `scripts/indexnow_submit.py` → `data/indexnow-ledger.json`; pipeline stage `announce`, after `verify`. The ledger records that a notification was received — never that anything was crawled or indexed.

Pipeline stage order: mint · validate · record · pdf · body-index · wiki · sitemap · **oai** · interlink · enrich · identity · commit · verify · **announce**.

---

## The rule, restated

The dataset is the source of truth for live values; the confirmation chain for historical ones; a surface may assert only what it reads.

v0.5 built the machinemediation instrument. v0.6 recorded the alexanarch instruments. v0.7 extends the rule from **values** to **conditions**, and records that the rule failed at the level of the Atlas itself: a frozen copy was read as the living document, which is the same pathology with the map as its object.

**Canonical:** `datasets/dataflow-atlas/` — the living series.
**Artifacts:** deposit #1097, and `data/specs/AXN-DATAFLOW-MAP-v0.2.md`.
