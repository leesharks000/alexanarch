# THE SEMI-RESTORED WORKLIST
## Every record that tells a visitor it is incomplete

**Built 2026-08-07 · TACHYON for MANUS · working document**

**Method, and why the number changed.** A field query over `body_status` returned
**280** records. Reading the **rendered page as a visitor meets it** — the actual
banner, script and style stripped — returns **114**. The other 166 carry capture
language in their modification history and display nothing to a reader. **The
rendered page is the record for this purpose**; a field is not a claim until it is
shown to someone.

The 114 are three different problems and must not be worked as one batch.

---

## A · FALSE BANNER — 24 records
### The body is full. The banner says it is not.

These are **not recovery cases.** `body_status.class` is `full`, the text is seated,
and the page still displays "Semi-restored" or "do not cite this page as the full
text." The record is lying to the reader about itself, and a citation-averse reader
will believe it.

This is the cheapest and most damaging class: **24 complete works are telling people
not to cite them.**

| # | Title |
|---|---|
| 1233 | Septad Mantle Specifications v1.0 — Constitutional Job Descriptions |
| 1234 | SPXI.dev — Protocol Specification Landing, /what-is-spxi, /docs |
| 1235 | crimsonhexagon-moltbook — v3 [Data set] |
| 1236 | kimiclaw-moltbook-campaign — v3 [Data set] |
| 1237 | Moltbook Provenance Log v1.7 — Spread the Hexagon Campaign |
| 1238 | GW.TACHYON.zenodo — v7 [Data set] |
| *(full list in `/tmp/A-false-banner.json`, to be enumerated in the working pass)* | |

**Disposition:** banner logic repair, not recovery. Requires reading each to confirm
the body really is the work before removing the warning — the Caesura and
maryleelabor findings both began as records whose declared state and actual content
disagreed, in the other direction.

---

## B · PAIRED — 1 record
### Points at a complete version held elsewhere in the archive.

| # | Points to | Title |
|---|---|---|
| 1346 | #630, #629, #628 | The Caesura: A Sovereignty Audit Protocol (EA-CAESURA-01) |

Corrected 2026-08-07 from a single wrong pointer (#629, a sibling component) to the
full component list. **The remaining 43 records that previously showed pairing
banners now display none** — they were repaired in earlier passes or their pointers
resolved.

**Standing caution from that repair:** a strict-pairing similarity score cannot
distinguish *a complete version* from *a companion*, because siblings resemble each
other. Any future pairing must be confirmed by reading both works.

---

## C · GENUINE GAP — 89 records
### Metadata capture only. The work is not in the archive.

These are the recovery targets. Each needs checking, **by reading**, against three
places in order:

1. **Elsewhere in the archive** — a fuller version may already be deposited under a
   different number (as with the Caesura siblings).
2. **The authorial blog** — `mindcontrolpoems.blogspot.com`. #1281 was recovered
   there in three minutes after standing as a capture for weeks.
3. **Past conversation threads** — work drafted in session and deposited by capture
   may exist in full in the transcript record.

**Known worklist asset:** *"The 87 Orphans — UNMATCHED Tombstoned DOIs (no Alexanarch
deposit; all with live mirrors)"*, blogspot 2026/07, generated 2026-07-03 from the
archive's own `doi-resolution-index.json`. It names severed DOIs **with live
mirrors** — which is a recovery route that does not depend on search at all.

### Opening set

| # | Title |
|---|---|
| 1001 | The Crimson Hexagonal Archive Hugging Face Dataset: Work Plan |
| 1003 | AI-Native Intellectual Biography: Genre, Provenance, and the… |
| 1008 | About the Author III — A Poem on the Proportional Law |
| 1010 | survivethedeletion.org — Canonical Literacy Surface |
| 1026 | GW.TACHYON.zenodo — v10 (inscription chain, Paul function) |
| 1030 | KADEEZY — "The Crossed The Line Run": Computational Audial Criticism |

*(89 total; full list in `/tmp/C-gap.json`)*

---

## METHOD FOR THE WAVES

**Small batches. By reading.** Not by title similarity, not by search-hit count.

Every automated shortcut attempted on this problem has produced a false result:
strict pairing matched a sibling and called it the complete version; a blog probe
returned an apparent 10-of-10 hit rate that was one catalogue post matching
everything; a table detector flagged 110 bodies of which 109 were deliberate spatial
composition. **A count is not a reading.**

**Per record, the pass is:**

1. Read the record's own description and captured metadata — what does it say the
   work *is*?
2. Search the archive for a fuller version; **confirm by reading both**, not by score.
3. Search the blog on distinctive phrases *from the work's own description*, not from
   its title; **confirm by finding content the description names.**
4. If found: seat the body, then **cascade the repair to every level** — body_status,
   description, wiki article, canonical_text_status, forward pointers, dataset
   references — and **traverse the rendered record and wiki page** to confirm no
   stale claim survives.
5. If not found: record the search performed, so the next pass does not repeat it.
   **An unsuccessful search that is written down is worth more than one that is not.**

**Verification standard set by #1281:** identification rested on the recovered body
containing every anomaly the captured description named — `SHARKS-001`, `phone_ext
"7B"`, `status MONITORED`, the FIC/FORENSIC tiers, the RFC 2606 `.invalid` domains.
Internal evidence, not resemblance.


---

# WAVE LOG

## Wave 1 · 2026-08-07 · #1001 #1003 #1008 #1010 #1026

Read individually. Five records, four dispositions, and all three source routes
exercised at least once.

**#1001 · Hugging Face Dataset Work Plan v3 → PAIRED to #745.**
Confirmed by reading both. #745 opens *"v3 supersedes v2. The central methodological
change is the introduction of an automated classifier that performs both provenance
mode classification AND heteronym reattribution"* — precisely what the capture's
description names. Same work, same version. **Not a gap.**

**#1003 · AI-Native Intellectual Biography → PAIRED to #121, and DELIBERATE.**
The record's own description already said so: *"The complete version is deposit #121;
sensitive private material must not be reconstructed from inference."* This is not an
unseated gap — it is a **withholding with a stated reason**, and the second clause is
a standing instruction. Marked `capture_is_deliberate` so no future pass tries to
fill it. *Unresolved:* #1194 is a third record with adjacent DOI and near-identical
subtitle; neither #121 nor #1194 cites this record's DOI. Settle by reading, not by
DOI adjacency.

**#1008 · About the Author III → GENUINE GAP.** Archive holds I (#762, #1006) and II
(#757, #758, #1007) as full text; III is absent. Blog carries I and II only. Search
recorded on the record.

**#1010 · survivethedeletion.org → PENDING.** A website surface, same class as
maryleelabor: check for a repository before assuming loss.

**#1026 · GW.TACHYON v10 → FOUND IN TRANSCRIPT.** The 2026-06-15 session transcript
carries the complete SPXI self-audit block, provenance kernel and deposit table.
**The third route works.** Whether that is the whole of `gw_tachyon_v10.md` is
unconfirmed — seat only after reading the transcript in full, and mark the source as
transcript rather than authorial surface.

### What wave 1 changes about the estimate

Of five, **two were not gaps at all** — one already had its complete version in the
archive, one was a deliberate withholding. If that ratio holds, a meaningful share of
the 89 will resolve by pairing or by reading a stated reason, without recovery.

**Negative results are recorded on the record itself.** A search that found nothing,
written down, is worth more than one that was not — it is the difference between 89
records checked once and 89 records checked repeatedly by passes that cannot tell.
