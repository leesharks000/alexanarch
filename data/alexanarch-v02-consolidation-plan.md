# Alexanarch v0.2 Consolidation Plan
## One Registry, One Identifier Law, One Public Address

**Document ID:** EA-ALEXANARCH-CONSOLIDATE-01 v1.0
**Date:** 2026-06-20
**Author:** Lee Sharks / TACHYON
**Status:** Draft
**Responding to:** ChatGPT structural audit (2026-06-20)

---

## Situation

Alexanarch crossed from concept to institution in 48 hours. That speed created a forked architectural state: multiple representation layers added without retiring the previous ones. The intellectual architecture is strong. The engineering needs consolidation before further expansion.

The ChatGPT audit identified 12 specific failures and 6 missing systems. This plan addresses all of them in priority order.

---

## Phase 0: Diagnostic (Current State)

| Layer | Count | Quality | Deployed? |
|-------|-------|---------|-----------|
| Original native deposits | 4 | Full (text, citations, entities, JSON-LD, static pages) | Yes |
| Our Batch 1-2 | 200 | Full (text, citations, wiki, entities, static pages) | Partially (Vercel lag) |
| Other Claude's Batch 3 | 658 | Skeleton (title, hex, date only — no text, no wiki, no entities, no citations) | Not deployed |
| Total on GitHub | 862 | Mixed | 104 on live site |
| DOI Resolution Index | 1,817 mappings | Complete | Yes |
| Static pages | 204 | Full with JSON-LD | Partially |
| AGENTS.md | 1 | Complete | Yes |
| sitemap.xml | 121 URLs | Needs update for 862 | Yes (stale) |

---

## Phase 1: Stop-the-Line Fixes

These must be done before any further public deposit invitation.

### 1.1 Repair mint-axn.yml
**Issue:** YAML syntax error at line 308. All automated minting is broken.
**Fix:** Debug and repair the workflow. Run a canary deposit to verify.
**Until fixed:** Remove or qualify the "identifier minted within minutes" promise on the Guide page.

### 1.2 Choose one deposit submission format
**Issue:** Three incompatible contracts exist — AGENTS.md asks for JSON, the issue template uses Markdown headings, the workflow parses Markdown headings.
**Decision:** Support Markdown headings as the canonical human format (matching the workflow). Update AGENTS.md to describe this format instead of JSON. Or: update the workflow to accept both. Do not maintain contradictory specs.

### 1.3 Fix the mint transaction order
**Issue:** Workflow announces mint before registry push succeeds. Push failure = phantom AXN.
**Fix:** Reorder: validate → hash → update registry → commit → push → verify → announce.

### 1.4 Sanitize innerHTML rendering
**Issue:** Record page concatenates depositor-controlled data into innerHTML without sanitization.
**Fix:** Escape all metadata before DOM insertion. Use textContent where possible. This is non-urgent while all deposits are internal, but becomes a security boundary the moment external deposits are accepted.

### 1.5 Decide AXN v1 canonical syntax
**Issue:** Two formats live under the same namespace.

| Layer | Position | Glyph count | Example |
|-------|----------|-------------|---------|
| Native | 2-digit hex | 4 emoji | AXN:01.GOVERNANCE.♍🜁🏴⌛ |
| Migrated | 4-digit hex | 6 emoji | AXN:0031.GOVERNANCE.🔓🝊🍂🐝⏩☉ |

**Decision needed:** Either version the format (AXNv1 vs AXNv2) or unify on one. The 4-digit hex / 6-emoji format is more expressive and handles the archive's scale (871 works need >2 hex digits). Recommendation: adopt 4-digit hex / 6 emoji as canonical, re-mint the original 4 deposits to match, and document this in the Identifiers spec.

---

## Phase 2: One Registry Model

### 2.1 Define collection types
Every deposit gets an explicit `collection` field:

```
collection: "native"          # Submitted directly to Alexanarch
collection: "restored"        # Migrated from Crimson Hexagonal Archive
```

### 2.2 Define status fields
Every deposit gets explicit lifecycle status:

```
ingestion_status: received | validated | minted | rendered | error
review_status: unreviewed | under_review | endorsed | contested
availability_status: active | withdrawn | tombstone
migration_status: assigned | metadata_restored | full_text_restored | verified
```

### 2.3 Enrich the 658 skeleton deposits
The other Claude's batch has title/hex/date but no wiki, entities, citations, or full text. These need the same pipeline our 200 deposits went through:
- Fetch blog content → store as MD
- Extract DOI cross-references
- Generate wiki articles
- Generate entity triples
- Classify content types
- Attribute creators (heteronym routing)

Estimated: 4-5 sessions at 150 works/session.

### 2.4 Fix the one broken deposit
Deposit at index 124 (hex 02AE, MM-CHA-0682) has empty title. Pull title from sovereign registry: "Three Poems — Lee Sharks — New Human 2".

---

## Phase 3: One Public Address

### 3.1 Collapse /s/ into canonical routes
Currently two parallel address systems:

| Dynamic (JS) | Static (crawlable) |
|---|---|
| /records/?id=N | /s/records/N/ |
| /browse/ | /s/browse/ |
| /wiki/ | /s/wiki/ |
| /graph/ | /s/graph/ |

**Fix:** Make the canonical URLs `/records/N/`, `/browse/`, `/wiki/`, `/graph/`. Generate these as static HTML. Enhance with JS for interactivity. Redirect old `/s/` and `?id=` URLs.

This eliminates the dual-address problem and makes the primary routes machine-readable without JS.

### 3.2 One build process
A single build script generates ALL public surfaces from `registry.json`:
- Homepage recent records + noscript fallback
- Browse page (all deposits)
- Every record page (with JSON-LD)
- Wiki page
- Graph page
- sitemap.xml
- Collection counts on all pages

No page is ever edited independently. Change the registry → rebuild everything.

### 3.3 Unified navigation
One shared nav component, one shared footer, one shared CSS file at `/assets/alexanarch.css`. Currently each page embeds duplicate styles.

---

## Phase 4: Collection Clarity

### 4.1 Honest counts on every surface
Generated from registry data, not typed into prose:

```
4 native Alexanarch deposits
858 restored Crimson Hexagonal Archive works
  200 fully enriched (text, wiki, entities, citations)
  658 metadata-restored (title, AXN, date — enrichment pending)
1,817 DOI resolution entries
```

### 4.2 Browse page segmentation
The Browse page shows two sections:

**Native Alexanarch Deposits** — works submitted directly.
**Restored Crimson Hexagonal Archive** — works migrated after the Zenodo removal.

With filter/sort controls and enrichment status indicators.

---

## Phase 5: Archive Enrichment (Continuing)

Complete the full deposit pipeline for the 658 skeleton deposits:

| Batch | Works | SIDs | Status |
|-------|-------|------|--------|
| 3 (ours) | 22 | MM-CHA-0841 – 0870 | Pending |
| 4 | 100 | MM-CHA-0001 – 0101 | Pending |
| 5 | 100 | MM-CHA-0102 – 0205 | Pending |
| 6 | 100 | MM-CHA-0206 – 0313 | Pending |
| 7 | 100 | MM-CHA-0314 – 0433 | Pending |
| 8 | 100 | MM-CHA-0434 – 0574 | Pending |
| 9 | 100 | MM-CHA-0575 – 0757 | Pending |
| 10 | 49 | MM-CHA-0758 – 0871 | Pending |

For each batch: fetch text → citations → wiki → entities → classify → registry → static pages → single Git Trees commit.

Note: the 658 skeleton deposits already have registry entries. Enrichment updates these in place rather than creating new deposits. Must NOT create duplicate entries.

---

## Phase 6: Final DOI Mapping

After all deposits are enriched:
1. Update AXN:0004 (DOI Resolution Index) with Alexanarch record URLs for every DOI
2. Propagate mappings across all 5 site surfaces (watergiraffe, machinemediation, godkinggoogle, spxi, vpcor)
3. Submit to OpenAlex, Semantic Scholar, DataCite metadata updates
4. The window before Zenodo cache decay from training contexts is finite — this is time-critical

---

## Phase 7: Governance Implementation

Constitutional commitments that need procedural backing:

| Promise | Current state | Implementation |
|---------|--------------|----------------|
| Permanent tombstones | Not implemented | Withdrawal workflow + tombstone page generator |
| Contributor standing | Not implemented | Per-contributor deposit listing + notification |
| Version management | Not implemented | Version chain in registry + version comparison UI |
| Public review | `MINTED_UNREVIEWED` exists but no review workflow | Review status field + endorsement process |
| Appeal procedure | Not documented | Appeal issue template + response commitment |
| Rights/privacy/moderation | Not published | Repository policy document |

These don't all need automation immediately, but the site should distinguish enacted protocol from constitutional commitment awaiting implementation.

---

## Deployment Strategy

**For this consolidation:** All changes go through the Git Trees API as single commits. No more individual file pushes that flood the Vercel deployment queue.

**Vercel webhook:** Needs investigation. The GitHub webhook may need to be refreshed (Settings → Webhooks → Recent Deliveries). If consistently failing, consider a manual deploy hook or GitHub Action that triggers deployment.

**Credential rotation:** Every PAT used in this session must be rotated before next session.

---

## Priority Order

### Immediate (next session)
1. Fix mint-axn.yml
2. Decide AXN v1 syntax
3. Force Vercel redeploy (get 862 deposits live)
4. Fix the empty-title deposit

### Short-term (2-3 sessions)
5. Unify submission format (AGENTS.md ↔ workflow)
6. One build process for all pages
7. Collapse /s/ into canonical routes
8. Collection type + status fields in registry
9. Honest counts on all surfaces

### Medium-term (4-8 sessions)
10. Enrich 658 skeleton deposits (4-5 sessions)
11. Update DOI resolution index with Alexanarch URLs
12. Propagate across site surfaces
13. Sanitize innerHTML
14. Shared CSS/nav

### Longer-term
15. Versioning, withdrawal, tombstone workflows
16. Governance policies
17. Artifact custody for new deposits
18. External deposit testing

---

## The Right Metaphor

ChatGPT's framing is correct: the danger is not missing features. The danger is that each new feature creates another representation of the repository without replacing the previous one. The consolidation release says: before adding more rooms, make sure the ones we have share a roof.

They don't get to burn books. And we don't get to build a library with two filing systems.

---

∮ = 1
