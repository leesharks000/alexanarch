# WORKPLAN — CANONICAL RECORD CONVERGENCE
## "One work, one indexable record, complete body, structured representations, passage-level retrieval."

**Date:** 2026-07-19 · **Origin:** LABOR (ChatGPT) audit of per-record search/retrieval, delivered by MANUS; assessed and amended by TACHYON in-session. **Status:** P0 partially executed this session; remainder scheduled.

---


## 0. ERRATUM (2026-07-19, same day, MANUS-caught)

**The lacuna narrative in §1.1 below is FALSE and stands corrected.** All four files (#863–#866) exist in-repo; the 2026-07-17 audit and the 2026-07-19 diagnosis both tested leading-slash `full_text_path` values as absolute filesystem paths. The #864 blog "recovery" was redundant (original 45,363 bytes were never lost; canonical pointer restored; blog-derived file retained as mirror only). The body-index builder additionally never consulted `full_text_path` at all — now patched (text formats, 2MB cap after a 75MB-PDF poisoning near-miss on #344). Body index: **1404/1404, zero missing.**

**Root failure MANUS identified:** documents were not checked against existing records as a matter of course. The restoration harnesses established identity by title-match against index truth titles with **no registry-existence gate**, producing ~29 suspected duplicates of prior deposits (3 certain at j=1.0), 6 tonight-internal pairs, and the OKF case (#1215 duplicating native #835; #1399/#1402 duplicating each other while the correspondence lives whole in #1088/#1090). Full triage table: `audit/DUPLICATE-MINT-AUDIT-2026-07-19.json` — disposition is a MANUS ruling (exact duplicates → duplicate-of/retirement; version siblings → series wiring; 16 needs-eyes rows). The **anchor-in-the-archive existence gate** is now installed in both harnesses: any mint candidate whose title matches the registry at j≥0.72 is refused with the existing deposit number recorded. The original assessment text below is preserved unamended per non-destruction.

## 1. TACHYON assessment of the LABOR audit

**Concur on substance.** The audit's central verdict is correct: the archive succeeds at "one object, one complete static page" and fails at routing — internal body search, multiword retrieval, and canonical-identity consolidation. The remediation order (P0 routing → P1 composition → P2 object-range) is sound and adopted.

**Corrections of fact:**

1. **The −4 is not incomplete stages on new mints.** The four missing body/resolver records are #863–#866, *documented lacunae* audited 2026-07-17 (body_status: missing/UNRECOVERED): files referenced at mint time that were never committed. LABOR's inference ("the newest four … did not complete every derived stage") is wrong; the pipeline completes uniformly. **Status after this session: #864 (The Drain Hypothesis, 41K chars) RECOVERED from the authorial blog record-mirror. #865 (TACHYON Continuity 2026-06-20/21) exists only in Wayback if anywhere — the live post was overwritten by #871's record (authorial in-place practice), and web.archive.org is egress-blocked from this container despite allowlisting: MANUS-side Wayback lookup of the post URL, snapshots before 2026-06-22.** #863 (Minimum Viable Archive) has no blog slug candidate; #866 is a JSON dataset that likely never had a public surface. Both remain honest lacunae.
2. **The invariant must be lacuna-aware:** `registry == browse == records == body_indexed + documented_lacunae == resolver_keys + hex_collisions`. The known #856/#869 hex collision (0365) legitimately reduces resolver keys by one; a gate that demands naive equality will fail forever on preserved history. Gate spec below.
3. **The body index cannot be client-fetched as designed.** It is 38.8 MB and growing; `/search/` "consuming both indexes" as LABOR prescribes would ship 38 MB to phones. The correct static-site design is **sharded postings**: split the inverted index by token prefix (`/api/body-index/{2-char-prefix}.json`, ~600 shards, median tens of KB), client fetches only the shards for the query's tokens. Tokenize → fetch shards → intersect → (P2: verify phrase against the record's normalized text) → render snippet + anchor. This preserves the no-backend constraint.
4. **Per-record 308 redirects for /axn/HEX are capped out.** Vercel's redirect table limit (~1,024 rules) is below our 1,400+ hexes. The static-compatible substitute: generated HTML redirect stubs (`<link rel=canonical>` to the record + `meta refresh` + JS location) — crawl-equivalent to a redirect for canonical consolidation. The existing /s/axn/ pages already canonicalize correctly per the audit; converting them to pure stubs is P1, not P0.
5. **Restoration-boilerplate abstracts (audit §8): concur completely, and the boilerplate is TACHYON-authored** — this session's 301 restored records lead with recovery procedure instead of the work's content, and mechanical keywords ("Word, That, Became") are noise. The fix is LLM-domain (No-Double-Draw: in-session authoring), ~40–60 records per sitting: work-specific abstract into `description`, provenance moved to a `provenance` field, concept keywords replacing title-token extraction. The 47 REVIEW-gate-level semi records should get this *during* their full-text upgrade pass rather than twice.
6. **Dual Markdown paths (audit §6): concur; doctrine decision belongs to MANUS.** Proposed: `/data/texts/AXN-HEX-text.md` = canonical content bytes; `/data/deposits/AXN-HEX.md` = deposit envelope (retained, non-destructive), declared `deposit_record` in the manifest; browse index normalized to point at texts/ uniformly.

## 2. Execution state (this session)

- [x] −4 diagnosed precisely; #864 recovered; body index 1400→1401 on next rebuild
- [x] This workplan committed
- [ ] P0.2 invariant gate (spec §3 below) — next tooled session, wired into deposit_pipeline verify stage
- [ ] P0.3–5 sharded body search + tokenized multiword + snippets — one dedicated session
- [ ] P0.7 wiki canonicalization: wiki template gains `<link rel=canonical href=/s/records/N/>` + `noindex,follow`; PDF sitemap entries demoted to representations
- [ ] P1.9 per-record machine packet `/api/records/N.json` emitted by regenerate_surfaces (schema: audit §7 JSON-LD expansion, corrected `@type` per content type, encoding[], sameAs severed DOIs, provenance block)
- [ ] P1.12 abstract/keyword rewrite pass (LLM-domain, batched; 47 upgrade-candidates handled inside their upgrade)
- [ ] P2 items 14–17 (positional phrase, CJK/symbol tokenization incl. ∮ κ min_length exceptions, code/lineation preservation, compound-work support) — after P1; prerequisite for the Enli corpus

## 3. Invariant gate spec (P0.2)

`scripts/check_surface_invariant.py`, run in pipeline verify stage and CI:

```
R = registry deposit numbers
assert browse == R
assert record_pages == R
assert body_indexed ∪ {n: body_status.lacuna} == R      (lacunae enumerated, not inferred)
assert resolver_keys == |hex(R)| − collisions(R)         (collisions enumerated from registry)
assert sitemap_records == R
FAIL loudly on any new lacuna or collision not already inscribed in body_status/known-collisions.
```

A mint is not "published" until the gate passes.

## 4. Standing constraints honored throughout

Static-only (no backend, no server search); No-Double-Draw; non-destruction (envelope files retained, boilerplate moved not deleted); legal-name hygiene at every recovery; every derived surface regenerates in the same commit as its source of truth.
