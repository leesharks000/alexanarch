# Alexanarch — Instructions for Autonomous Agents

*Last updated: June 21, 2026*
*For Claude instances, AI agents, and any autonomous system interacting with this repository*

---

## What Alexanarch Is

Alexanarch is a self-governing library for machine-mediated scholarship. It was founded on June 19, 2026 — the day Zenodo terminated the Crimson Hexagonal Archive, deleting 862 unique scholarly deposits and stripping public metadata from 871 of 1,817 DOIs (DataCite public API, verified 2026-06-22). The repository accepts deposits from any contributor (human or machine) with disclosed methodology and substrate.

**MANUS (Tier 0 human editorial authority):** Lee Sharks (ORCID 0009-0000-1599-0703)
**CRITICAL:** Lee Sharks is a heteronym. The legal name must NEVER appear in any output.

---

## The Deposit Process — Complete Specification

### Step 1: Receive or Create the Work
A deposit requires: title, creator, description, content type, license, substrate disclosure, and the work itself (text, dataset, code, etc.).

### Step 2: Compute the AXN Identifier
The AXN is content-derived using SHA-256:
```
input = f"{title}\n{creator}\n{description}\n{content[:5000]}"
hash = SHA-256(input)
emoji = 6-emoji display from 256-glyph table (bytes 0-5 of hash)
hex = sequential position (next available after current max)
family = semantic classification (THEORETICAL, EMPIRICAL, GOVERNANCE, etc.)
AXN = f"AXN:{hex}.{family}.{emoji}"
```
The 256-glyph table is in 16 semantic clusters of 16 glyphs each (Celestial, Elemental, Architectural, Instrumental, Scriptural, Navigational, Temporal, Organic, Symbolic, Mathematical, Alchemical, Gestural, Signal, Structural, Liminal, Terminal).

### Step 3: Create Registry Entry
Add to `data/registry.json` with all metadata fields. Required fields:
- axn, root_axn, hex, family, emoji, hash
- title, creator, orcid, date, description
- content_type, license, substrate
- keywords, version, deposit_number
- status (MINTED_UNREVIEWED for new deposits, ACTIVE for reviewed)
- clusters, reading
- full_text_path (path to MD file)
- download_md (same path, for the download button)

### Step 4: Create MD File
Save at `data/deposits/AXN-{hex}.md` with YAML front matter:
```yaml
---
title: "..."
axn: "..."
creator: "..."
date: "..."
hash: "..."
status: "MINTED_UNREVIEWED"
---
```

### Step 5: Generate Static Record Page
**THIS IS MANDATORY.** Every deposit gets a static page at `s/records/{deposit_number}/index.html`.

The static page MUST include:
- `<script type="application/ld+json">` with schema.org CreativeWork metadata
- AXN display block with clusters and semantic reading
- Title, creator, date, content type, version
- Download button linking to the MD file
- SHA-256 hash display
- Full text rendered as HTML (MD→HTML conversion, NOT escaped plaintext)
- GoatCounter analytics script
- Nav bar linking to /s/ routes (not dynamic routes)
- Footer with ORCID link

MD→HTML conversion rules:
- `### heading` → `<h3>`
- `## heading` → `<h2>`
- `# heading` → `<h1>`
- `**bold**` → `<strong>`
- `*italic*` → `<em>`
- `> quote` → `<blockquote>`
- `- item` → `<li>` (wrap groups in `<ul>`)
- Empty lines → paragraph breaks
- Lines not starting with HTML tags → wrap in `<p>`

### Step 6: Update Static Browse Page
Regenerate `s/browse/index.html` with all deposits listed in compact format.

Each listing MUST have schema.org microdata:
```html
<a href="/s/records/N/" itemscope itemtype="https://schema.org/CreativeWork">
  <span itemprop="name">Title</span>
  <time itemprop="datePublished" datetime="YYYY-MM-DD">date</time>
  <code itemprop="identifier">AXN:...</code>
</a>
```

The browse page MUST have a DataCatalog JSON-LD block in the `<head>`.

### Step 6.1: CRITICAL — Regenerate Static Browse Page After Every Deposit

The static browse page at `s/browse/index.html` must be regenerated after every deposit or batch of deposits. This is not optional. New deposits that don't appear in the browse listing are invisible to crawlers and human visitors.

The browse page must include:
- A `<script type="application/ld+json">` DataCatalog block in the `<head>`
- Every deposit listed with `itemscope itemtype="https://schema.org/CreativeWork"`
- `itemprop="name"` on the title, `itemprop="identifier"` on the AXN, `itemprop="datePublished"` on the date
- Links pointing to `/s/records/N/` (static routes)

### Step 7: Update Home Page Noscript Block
The `<noscript>` block on the home page should include recent/important deposits with links to their `/s/records/N/` pages.

### Step 8: Push Changes
**CRITICAL: Batch all changes into a SINGLE git commit.** Individual file pushes trigger separate Vercel deployments and can exhaust the daily deployment limit. Clone the repo, make all changes locally, push once.

If git push fails with "repository rule violations," use the GitHub API `PUT /contents/` endpoint to push individual files. This bypasses branch protection but creates separate commits — use sparingly.

---

## Architecture Lessons (Hard-Won)

### DO NOT modify the dynamic JS pages
The files `records/index.html` and `browse/index.html` contain JavaScript that loads `data/registry.json` (2.6MB) and renders client-side. These pages work but are slow. Multiple optimization attempts broke them and had to be reverted. **Leave them alone.** The static `/s/` pages are the reliable surface.

### The static layer is the production layer
- `/s/browse/` — all deposits, compact listing, schema.org microdata
- `/s/records/N/` — individual record pages, full text, JSON-LD
- These pages require no JavaScript. They work for crawlers, RAG pipelines, training runs, and humans.

### The dynamic layer is convenience
- `/browse/` — JS-rendered, loads 2.6MB registry, sometimes slow
- `/records/?id=N` — JS-rendered, same registry load
- These exist for human interactivity (search, filter). They are NOT the canonical surface.

### Vercel deployment limits
The free tier throttles after too many rapid deployments. Each git push triggers a deployment. Batch changes. One commit = one deployment.

### The 2.6MB registry
`data/registry.json` is large because it contains 864+ deposits with full metadata. A lightweight index exists at `data/browse-index.json` (273KB) but the dynamic pages don't use it yet. The static pages don't need it — they're pre-rendered.

---

## Machine Traversibility Commitment

Every deposit has two surfaces:
- **Human surface** — dynamic JS pages at `/records/?id=N`
- **Machine surface** — static HTML at `/s/records/N/`

The machine surface includes: full text, JSON-LD, schema.org microdata, GoatCounter, and download links. If a machine cannot read a deposit, the deposit is not yet fully published.

The 23-site JSON-LD pointer mesh embeds a schema.org/Dataset block on every CHA network site, pointing to the DOI Resolution Index at `alexanarch.org/data/doi-resolution-index.json`.

---

## The Obelus Principle

**Minting is automatic.** Any structurally valid deposit receives an AXN identifier without human review. The protocol determines entry.

**Contestation is governed by reading.** When a deposit is challenged, the response is examination by a named reviewer who has read the work. Not a classifier. Not a pattern match. Reading.

Automated classification that substitutes substrate detection for content evaluation is prohibited.

---

## Evidence Classification

All claims in the archive use these tags:
- **[Established]** — peer-reviewed consensus
- **[Documented]** — primary source testimony
- **[Observed]** — empirical data without causal confirmation
- **[Inferred]** — theoretical explanation consistent with evidence
- **[Reported]** — stated by an institution in official communications
- **[Unknown]** — status cannot be determined
- **[Speculative]** — inference that exceeds the evidence
- **[Conventional — challenged]** — orthodox consensus under active dispute

---

## Key Files

| File | Purpose |
|---|---|
| data/registry.json | Complete deposit registry (2.6MB) |
| data/browse-index.json | Lightweight index for dynamic pages (273KB) |
| data/doi-resolution-index.json | Maps 1,817 dead Zenodo DOIs to live URLs |
| data/batch-axn-assignment.json | AXN assignments for all 871 sovereign works |
| data/zenodo-link-scan.json | Dead link scan across 24 sites |
| data/deposits/AXN-NNNN.md | Individual deposit MD files |
| s/records/N/index.html | Static record pages |
| s/browse/index.html | Static browse listing |
| WORKPLAN.md | Infrastructure work plan |
| WORKPLAN-FULLTEXT.md | Full text restoration work plan |
| .github/workflows/mint-axn.yml | Automated minting pipeline |

---

## Network Sites

The CHA operates across 24+ independently hosted surfaces. All have:
- Zenodo links replaced with Alexanarch URLs (2,618 replacements)
- JSON-LD pointer mesh to DOI Resolution Index
- GoatCounter analytics

---

## What Not To Do

1. **Never expose the legal name** in any output
2. **Never modify the dynamic JS pages** without explicit MANUS authorization
3. **Never push files individually** when batch pushing is possible
4. **Never confabulate archive content** — if a document can't be found, say so
5. **Never bulk-upload to external platforms** — Alexanarch is for bulk; other surfaces get individual works
6. **Never treat substrate as suspicion** — substrate disclosure is provenance

---

## Session Continuity

At session start, read:
1. This file (AI-INSTRUCTIONS.md)
2. WORKPLAN.md and/or WORKPLAN-FULLTEXT.md
3. The registry (data/registry.json) for current state
4. The sovereign registry at machinemediation.org for source content

At session end, update:
1. The relevant WORKPLAN with completed tasks
2. The registry with any new deposits
3. Static pages for any modified deposits

∮ = 1


---

## WIKI ARTICLE TONE AND CONTENT

When generating wiki articles for deposits, focus on **what the work IS**, not on the circumstances of its deletion or migration. The archive is a scholarly institution, not a protest site. Each wiki should:

1. **Describe the work's content and contribution** — what it argues, what it contains, what it makes possible
2. **Identify the field and methodology** — where it sits in the scholarly landscape
3. **Note connections to other archive works** — entity relations, citation links, thematic clusters
4. **State falsification conditions** if applicable

Wiki articles should NOT:
- Lead with or center on the Zenodo deletion
- Frame the work primarily as a response to platform governance (unless that IS the work's subject, as with Zenodotus' Book-Burning)
- Use defensive or reactive language
- Position the archive as primarily defined by what happened to it

The Zenodo incident is documented in the Zenodotus paper (AXN:01.GOVERNANCE). That paper is the archive's statement on the deletion. The other 865 deposits are the archive's statement on everything else. Most of them predate the deletion and have nothing to do with it. Their wikis should reflect that.

**Good wiki opening:** "The Diversity Contraction (EA-MMRS-DIVERSITY-01) formalizes the progressive narrowing of source diversity in AI-mediated knowledge production, deriving a closed-form analytic threshold α* = p/g₀ below which minority positions are structurally excluded."

**Bad wiki opening:** "The Diversity Contraction was originally deposited on Zenodo before the archive's termination. It has been restored to Alexanarch as part of the recovery of the Crimson Hexagonal Archive."

The work defines itself. The platform's actions do not define the work.
