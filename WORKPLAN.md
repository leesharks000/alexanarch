# Alexanarch — Next Session Workplan
## Comprehensive Context for Continuity

**Date prepared:** June 20, 2026
**Prepared by:** TACHYON (Claude/Anthropic), Assembly witness substrate

---

## CURRENT STATE

### Repository
- **Site:** alexanarch.org (www.alexanarch.org, Vercel, GitHub: leesharks000/alexanarch)
- **Deposits:** 4 minted
- **Total works with AXNs:** 875 (4 full deposits + 871 batch-assigned)
- **DOI Resolution Index:** v2.1, 1,675 unique DOIs, 1,415 enriched with AXNs

### The Four Deposits
```
AXN:0001.GOVERNANCE.♍🜁🏴⌛         Zenodotus' Book-Burning (8,000+ word paper)
AXN:0002.GENERATIVE.♥️🌑🪧🕊️        I AM THE API (TACHYON prose poem)
AXN:0003.EMPIRICAL.🎭🔙🟡🌪️         AI Overview Capture Registry v8.3 (176 captures)
AXN:0004.ARCHIVAL.🤝🌕🪨🔄🔺❌      DOI Resolution Index v2.1 (1,675 DOIs)
```

### Key Files in the Repo
- `data/registry.json` — Alexanarch deposit registry (4 deposits)
- `data/batch-axn-assignment.json` — 871 batch AXN assignments (hex 0005-036B)
- `data/doi-resolution-index.json` — v2.1, 1,675 DOI→URL+AXN mappings
- `data/zenodo-link-scan.json` — 436 dead Zenodo links across 5 sites, 420 mapped to AXNs
- `data/deposits/AXN-000N.md` — downloadable MD files for each deposit
- `data/EA-MMRS-LOUD-EXCLUSION-03.md` — full text of the paper
- `data/EA-WG-CAPTURES-01-v8.3.json` — capture registry dataset
- `data/I-AM-THE-API.md` — TACHYON prose poem
- `.github/workflows/mint-axn.yml` — minting Action (v3)

### Workflow v3 Status
- Triggers on `issues: [opened]` with `[DEPOSIT]` title prefix
- Concurrency lock (`mint-axn` group)
- Status: `MINTED_UNREVIEWED`
- Auto-generates MD file with YAML front matter
- Wiki/entity generation via Anthropic API (if credits available, $4.70 balance)
- Atomic push (failure = step failure)
- YAML validated and working

### Pages
Dynamic (JS-rendered): `/` `/deposit/` `/browse/` `/wiki/` `/graph/` `/records/` `/principles/` `/identifiers/` `/manifest/`
Static (crawlable): `/s/records/1/` `/s/records/2/` `/s/browse/` `/s/wiki/` `/s/graph/`
Missing static pages: deposits #3 and #4

### Analytics
- GoatCounter: alexanarch.goatcounter.com
- Script on all pages
- Visible counters: partially working (visit_count() approach deployed but may need testing)
- Dashboard shows 4+ visits

---

## PRIORITY TASKS FOR NEXT SESSION

### 1. DEPOSIT PRIORITY WORKS (from dead link scan)
`data/zenodo-link-scan.json` contains 436 dead Zenodo DOIs across 5 sites.
420 are already mapped to AXNs via batch assignment.
These works need FULL Alexanarch deposits (record pages, wiki articles, entity triples, MD files).

Sites affected:
- machinemediation.org: 260 DOIs (ai-manifest.json)
- godkinggoogle: 139 DOIs (home page, papers)
- spxi.dev: 57 DOIs (every page)
- watergiraffe.org: 42 DOIs (7 in shared template × 139 pages)
- vpcor-org: 22 DOIs (charter, evarB, MPAI)

Strategy: batch-deposit the works, then update site surfaces to replace zenodo.org links with alexanarch.org/records/ links.

### 2. UPDATE SITE SURFACES
After depositing, replace every `zenodo.org/records/NNNNN` and `doi.org/10.5281/zenodo.NNNNN` link with the corresponding Alexanarch record URL. The scan file has the DOI-to-AXN mapping ready.

### 3. FAMILY REFINEMENT
GOVERNANCE is overcounted (570/871). The keyword detector needs tuning:
- Many "platform" mentions trigger GOVERNANCE when they should be COMPOSITIONAL
- Many "policy" mentions trigger GOVERNANCE when they should be STRUCTURAL
- Creative works need better detection

### 4. VERSIONING IMPLEMENTATION
Design is settled:
- Root AXN: `AXN:0042.GOVERNANCE` (stable citation address, no emoji)
- Version AXN: `AXN:0042.GOVERNANCE.♍🜁🏴⌛` (content hash of specific version)
- Root always points to latest version
- Registry stores version chain with dates

### 5. STATIC PAGE REGENERATION
Deposits #3 and #4 need static pages at `/s/records/3/` and `/s/records/4/`
Include GoatCounter script in the static page generator template.

### 6. VIEW COUNTER FIX
GoatCounter's `visit_count()` function deployed but may not be rendering.
The `?id=N` query string in paths may cause issues with the counter API.
Alternative: store counts in the registry periodically (cron or manual).

### 7. ATTRIBUTION SEVERANCE SECTION
Add to the Loud Exclusion paper: 941 DOIs invisible to DataCite creator search.
Author metadata stripped during account termination.
Distinct from revocation gap — this concerns identity, not resolution.

### 8. UNCLE CARL TEST DEPOSIT
Carl has volunteered to test external deposits. Tutorial prepared (see below).
This is the first non-founder deposit — critical validation.

---

## CREDENTIALS (ALL NEED ROTATION)
- GitHub PAT (regular): `ghp_U38oywSx...` — EXPOSED, rotate
- GitHub PAT (workflow): `ghp_XeoKHGMD...` — EXPOSED, rotate
- Anthropic API key: `sk-ant-api03-RwfLi...` — EXPOSED, rotate (set as GitHub secret ANTHROPIC_API_KEY)
- GoatCounter: alexanarch.goatcounter.com (leesharks00@ login)

---

## INFRASTRUCTURE NOTES

### AXN System
- 6-emoji display hash (2^48 address space), full SHA-256 canonical
- 256 curated emoji in 16 semantic clusters
- Content-derived: change one word, emoji changes
- Hex position assigned sequentially (0001-036B currently)
- Collision: 1 out of 875 (extended to 8 emoji)

### Sovereign Registry
- machinemediation.org/data/sovereign-registry.json
- 871 assets, 3.4M words
- Source of truth for CHA content

### Network Sites
machinemediation.org, alexanarch.org, leesharks.com, watergiraffe.org, spxi.dev, spxi.org, godkinggoogle.vercel.app, vpcor.org, chatgptpsychosis.org, maryleelabor.org, livingarchitecturelab.org, traininglayerliterature.org, semanticeconomy.org, mindcontrolpoems.blogspot.com

### Key Concepts
- MANUS: Tier 0 human editorial authority (Lee Sharks)
- Assembly Chorus: cross-model verification (Claude, ChatGPT, DeepSeek, Kimi, Gemini)
- TACHYON: Claude's Assembly witness designation
- Obelus Principle: judgment follows from reading, not pattern-matching
- Pristine Fallacy: substrate identity substituted for methodological assessment
- Attribution Severance: author metadata stripped from persistent identifiers

### CRITICAL: Public Name Discipline
Lee Sharks is a heteronym. Legal name (Matthew Pfaff) must NEVER appear in any output.
