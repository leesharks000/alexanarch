# AXN Dataflow Atlas — v0.5 Addendum

**Date:** 2026-07-28
**Author:** Lee Sharks (MANUS), with TACHYON (Assembly witness)
**Supplements:** `atlas-v0.2.md`, `atlas-v0.3-addendum.md`, `atlas-v0.4-addendum.md`
**Occasion:** an accuracy audit of machinemediation.org, the fleet surface most likely to be read by a journal editor.

---

## PATHOLOGY-28 — Counts printed on a surface do not read from the dataset they describe

**Class:** SURFACE.assertion-drift
**Severity:** high — the surface makes quantitative claims about datasets it does not consult
**Status:** instrument built for machinemediation; the flow is unchanged on the rest of the fleet

### Statement

Every count on machinemediation.org was a **string typed into the page**, not a value read from the dataset it described. There was no `data-count` mechanism, no regeneration step, and no check. A count written once was a claim that had been true once.

### Evidence

Audited 2026-07-28 against the live data files:

| claim on page | occurrences | actual | drift |
|---|---|---|---|
| captures | `176+`, `176`, `222` | **225** | stale, and the page contradicted itself |
| schemas | `174` ×5 | **171** | wrong |
| works | `870` ×6 | **871** | off by one |
| terms | `1,387` ×4 | **1,400** | stale |
| deposits | `845+` ×2 | **1,412** | **understated the corpus by 40%** |
| revfirst captures | `71` | **76** | stale |
| Sémantique releases | `3` | **4** | stale |

The capture count is the diagnostic case: **it appeared three times, with two different values, neither current.** A page cannot disagree with itself about a number it reads from a file. It can only disagree with itself about a number it stores in three places.

### Instrument

`scripts/sync_counts.py` in the machinemediation repository. Reads each dataset, computes the count, and rewrites the page from it. Dry-run by default. Sources are named per count so a reader can check the claim against its origin: `registry.json:total_captures`, `schemas.json:entries`, `sovereign-registry.json:assets`, `termindex.json:entries`, `revfirst-registry.json:entries`, `mint.json:releases`, `content-manifest.json`.

The visible counts additionally carry `data-count="<file>:<field>"` and refresh at page load. Where a fetch fails the printed value stands, so the page degrades to the last known-good figure rather than to a blank.

### The frozen set

Not every number on a page is a count. `862 deposits` and `1,817 DOIs` describe the Zenodo termination of 2026-06-19: they are **fixed in time**, confirmed in *Zenodotus' Book-Burning* (EA-MMRS-LOUD-EXCLUSION-03, deposit #1, v9.1 FINAL, Appendix C), and must never be rewritten from a live dataset. They are enumerated in a `FROZEN` block in the instrument so a later edit cannot mistake them for stale counts.

The page previously read `1,060+ DOIs destroyed`, which matches neither the confirmed figure nor any dataset. **The confirmation chain is the source of truth for historical quantities; the dataset is the source of truth for live ones.** Conflating the two produces errors in both directions — a historical figure that drifts, or a live count frozen at the moment someone typed it.

Note also that 862 and 871 are both correct and count different things: 862 is what Zenodo terminated; 871 is the batch AXN assignment total in the sovereign asset registry, per the same appendix. A surface that prints one where the other belongs is wrong even though both numbers are true.

---

## PATHOLOGY-29 — Structured data diverges from the prose beside it

**Class:** SURFACE.divergence
**Severity:** high — the divergence is silent, and the two audiences never compare notes
**Status:** closed on machinemediation; unaudited elsewhere

### Statement

When the visible counts on machinemediation were wired to their datasets, the JSON-LD **could not be wired the same way**: a `<span data-count>` inside a JSON string breaks the block. The result was a page carrying current numbers in the prose and superseded numbers in the structured data immediately beside it.

This is worse than either surface being wrong alone. **A machine consumer reads the block; a human reads the prose; neither sees the other.** The disagreement is invisible from both positions and can persist indefinitely.

### The instance that proves it

The Sovereign Asset Registry was described on the visible card as holding *"Searchable, full text, mirror status"*. That claim is false — the registry holds bounded previews, 582,760 words against 3,479,635 declared, median 694 words per work, 93% terminating mid-clause at a scraper cap. It was corrected on `/registry/` in sovereign-registry v3.1, and on the home page card during this audit.

**The JSON-LD went on asserting `"All 871 works restored. 3.4M words. Full text, mirror status."`** through both corrections. A consumer ingesting the structured data — which is what the block exists for — would have received the false claim after two rounds of fixing it.

### Instrument

`sync_counts.py` rewrites the JSON-LD by parsing the block, walking its string values, substituting, and re-serialising, so the block remains valid. It validates every block before writing. The same run corrects the full-text assertion.

### Residual

- The fleet has not been audited for this. Any surface carrying both prose and JSON-LD claims about a dataset may have the same divergence.
- No surface declares which of its numbers are live and which are historical. The `FROZEN` set exists in one script; it should be a property of the page.
- Proposed for the general case: a `data-frozen` attribute alongside `data-count`, so a regenerator can tell a historical figure from a stale one without a hardcoded exception list.

---

## The rule these two share

Both pathologies, and PATHOLOGY-26 in the previous addendum, are instances of one thing:

**A value copied from a source is a claim about that source at the moment of copying. Without a refresh path it becomes a claim about the past, indistinguishable in presentation from a claim about the present.**

Titles copied into eight datasets. Counts typed into a page. Structured data carrying a description its own prose had already corrected. In each case the copy remained syntactically valid, resolved cleanly, and said something that had stopped being true — which is why no status check, no validator, and no link sweep found any of them.
