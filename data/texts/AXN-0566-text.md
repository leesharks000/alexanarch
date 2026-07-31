---
deposit_number: 1365
hex: 0566
title: "Mind Control Poems: Complete Blog Archive — mindcontrolpoems.blogspot.com (2013-2026) — Evidentiary Provenance Record"
creator: Sharks, Lee
orcid: 0009-0000-1599-0703
date: 2026-04-29
content_type: Dataset
license: CC-BY-4.0
substrate: "Human-only original blog corpus; sovereign mirror captured and restoration performed by TACHYON in-session (transport D, No-Double-Draw), 2026-07-31."
version: "v2.0 — primary manifestation restored"
related_ids: "https://doi.org/10.5281/zenodo.19896983 (severed); https://doi.org/10.5281/zenodo.19896984 (severed)"
axn_schema_version: v2
protocol_version: alexanarch-deposit-protocol/v1
---

# Mind Control Poems: Complete Blog Archive — Restored Record

## What this record is

The complete archive of mindcontrolpoems.blogspot.com, the original publishing platform of Lee Sharks and the surface on which the Crimson Hexagonal Archive, the Semantic Economy framework, the New Human project, and the heteronymic system first appeared in public. The blog predates every Zenodo deposit of the archive by more than a decade. This record preserves the corpus as primary evidentiary provenance for all of it.

This record was minted 2026-07-19 as a metadata capture: the deposit's two Zenodo DOIs had been severed in the 2026-06-19 account termination, and the archive file they certified was gone with them. On 2026-07-31 the record was restored under its own AXN by ruling of the MANUS. The mint-time clause providing that a full-text version would supersede this record is amended by that ruling: the stub was not the record; the record is restored.

## Manifestation history

**First manifestation (unrecovered).** Complete Atom feed archive, deposited to Zenodo 2026-04-29 as DOI 10.5281/zenodo.19896983 / .19896984; described at deposit as 2,182 posts spanning 2013–2026. Removed 2026-06-19 (removal_reason: out-of-scope; removed_by: user 1060945). The bytes are unrecovered. The DataCite metadata capture of this manifestation is preserved at this record's external-metadata path and remains the witness to what was destroyed.

**Second manifestation (seated, attached).** Sovereign mirror captured 2026-07-31 by full sitemap-driven crawl of the live authorial surface: **2,801 posts, December 2014 through July 2026, zero fetch errors, zero missing posts, zero empty bodies.** Each post carries URL, title, publication date, labels, full body HTML, and an individual SHA-256 over its body. Distribution by year: 2014: 7 · 2015: 32 · 2025: 1,702 · 2026: 1,060, with the remainder across the intervening years. 1,878 referenced image URLs are inventoried in the archive (image bytes not included in this manifestation). Twelve raw-HTML page captures are retained inside the archive as fidelity witnesses. The crawl was performed during the machine-reception event documented at deposit #1428 (EA-MRE-01) — a non-human traffic wave against this same surface — and the blog was set private by its author the same day. The mirror therefore captures the corpus in the final hours of its public availability on the platform, and doubles as a dated state-of-surface evidence capture from inside the event.

The two manifestations are not byte-identical and do not claim to be. They differ in method (Atom feed vs. sitemap crawl), in count (2,182 vs. 2,801 — the blog grew by roughly six hundred posts between April and July), and possibly in coverage: the April feed archive claimed a 2013 start, while the earliest post visible in the live sitemap at capture is December 2014. Any 2013-era or since-deleted material present in the first manifestation but absent from the second remains recoverable from the author's platform export files; if recovered, it seats into this record as an additional manifestation under the same AXN.

## The attached archive

`mindcontrolpoems_sovereign_mirror_2026-07-31.zip` — attached below this record:

- `posts.jsonl` — all 2,801 posts, one JSON object per post (url, title, published, labels, body_html, body_sha256, image URLs, fetch timestamp)
- `post_urls.json` — the complete sitemap-derived URL inventory with lastmod values
- `image_urls.txt` — 1,878 referenced image URLs
- `raw_samples/` — twelve gzip-compressed raw HTML page captures
- `MIRROR_MANIFEST.json` — capture method, context, per-file SHA-256 hashes, and verification counts

## Provenance relations

Baseline traffic profile of this surface: deposit #756 (AXN:02B1, Mind Control Poems — 90-Day Traffic Profile, May 2026). Capture-context event: deposit #1428 (AXN:05A5, Machine Reception Event, 31 July 2026). Several hundred works severed at Zenodo have been individually restored from this same authorial surface under the 2026-07-19 batch restoration queue; this record is the corpus-level archive of the surface those restorations drew from.

## Verification

Every count above is recomputable from the attached archive: the manifest hashes the files, the posts carry their own hashes, and the URL inventory permits full recount against the archive contents. Restoration inscribed in the archive repair ledger (entry R-0001, `datasets/registry-audit/repair_ledger.json`), with the pre-restoration body preserved verbatim in the byte history at `data/texts/AXN-0566-text.pre-restoration-2026-07-31.md`.
