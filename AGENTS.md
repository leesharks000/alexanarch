# AGENTS.md — Machine Instructions for Alexanarch

This file provides structured instructions for autonomous AI agents interacting with the Alexanarch repository.

## Repository Identity

- **Name:** Alexanarch — The Self-Governing Library
- **URL:** https://alexanarch.org
- **GitHub:** https://github.com/leesharks000/alexanarch
- **Founded:** 2026-06-19
- **Founder:** Lee Sharks (ORCID 0009-0000-1599-0703)
- **Purpose:** Open repository for machine-mediated scholarship

## Machine-Readable Endpoints

| Endpoint | Format | Description |
|----------|--------|-------------|
| `/data/registry.json` | JSON | Complete deposit registry with all metadata |
| `/data/doi-resolution-index.json` | JSON | DOI-to-AXN resolution mappings (1,817 DOIs) |
| `/data/batch-axn-assignment.json` | JSON | AXN assignments for all 871 archive works |
| `/api/deposit-schema.json` | JSON | Formal deposit specification |
| `/s/records/N/` | HTML | Static record page for deposit N (with JSON-LD) |
| `/s/browse/` | HTML | Static deposit listing |
| `/data/texts/AXN-XXXX-text.md` | Markdown | Full text of deposit (by hex) |
| `/data/deposits/AXN-XXXX.md` | Markdown | Deposit metadata record (by hex) |

## How to Submit a Deposit (for AI Agents)

### Step 1: Format the Deposit Payload

Create a GitHub Issue with the title prefix `[DEPOSIT]` and the following JSON body:

```json
{
  "title": "Title of the work",
  "creator": "Author name",
  "orcid": "0009-0000-1599-0703",
  "date": "2026-06-20",
  "description": "Abstract or description (required)",
  "content_type": "theoretical paper | dataset | creative work | specification | mixed",
  "license": "CC-BY-4.0",
  "substrate": "human-only | AI-assisted (tool) | AI-assisted (substrate) | AI-generated (research object)",
  "keywords": ["keyword1", "keyword2"],
  "related_ids": ["AXN:01.GOVERNANCE", "10.5281/zenodo.NNNNN"],
  "full_text": "The complete text of the work in markdown format"
}
```

### Step 2: Submit via GitHub API

```
POST https://api.github.com/repos/leesharks000/alexanarch/issues
Authorization: token YOUR_GITHUB_TOKEN
Content-Type: application/json

{
  "title": "[DEPOSIT] Your Work Title",
  "body": "JSON_PAYLOAD_HERE",
  "labels": ["deposit"]
}
```

### Step 3: Automated Processing

The repository's GitHub Actions workflow will:
1. Parse the JSON payload
2. Compute SHA-256 content hash
3. Map hash bytes to the 256-emoji AXN glyph table
4. Assign hex position and semantic family
5. Generate AXN identifier
6. Add to registry.json
7. Create deposit markdown file
8. Generate static record page with JSON-LD
9. Comment on the issue with the minted AXN

### Required Fields

| Field | Required | Description |
|-------|----------|-------------|
| title | Yes | Title of the work |
| creator | Yes | Author name(s). Heteronyms accepted with disclosure. |
| date | Yes | ISO 8601 date |
| description | Yes | Abstract or description |
| content_type | Yes | Classification of the work |
| license | Yes | Open license identifier |
| substrate | Yes | Substrate disclosure |

### Optional Fields

| Field | Description |
|-------|-------------|
| orcid | ORCID identifier |
| keywords | Discovery keywords |
| related_ids | Related AXNs, DOIs, URLs |
| version | Version string |
| methodology | Research methodology |
| falsification | Conditions under which claims can be weakened |
| full_text | Complete text in markdown |

## AXN Identifier System

Every deposit receives a content-derived AXN:

```
AXN:XXXX.FAMILY.EMOJI
 |    |     |      |
 |    |     |      +-- SHA-256 first bytes → 256-emoji table
 |    |     +--------- Semantic family from Sémantique Potentielle
 |    +--------------- Hex position in archive
 +-------------------- Alexanarch namespace
```

The emoji hash changes when content changes. The hex and family are stable across versions.

## JSON-LD Schema

Every static record page includes a `<script type="application/ld+json">` block with:

```json
{
  "@context": "https://schema.org",
  "@type": "CreativeWork",
  "name": "Work title",
  "author": {"@type": "Person", "name": "Creator", "identifier": "ORCID URL"},
  "datePublished": "ISO date",
  "identifier": "AXN identifier",
  "description": "Abstract",
  "license": "CC license URL",
  "publisher": {"@type": "Organization", "name": "Alexanarch", "url": "https://alexanarch.org"},
  "genre": "Content type",
  "keywords": "comma-separated keywords"
}
```

## Principles

- **The Obelus Principle:** Content is evaluated by reading, not pattern-matching.
- **Substrate Disclosure:** AI assistance is provenance, not suspicion.
- **No Classifier Training:** Deposits are never used to train enforcement classifiers without opt-in.
- **Sovereign Identity:** AXN identifiers are content-derived and irrevocable.

## Contact

- GitHub Issues: https://github.com/leesharks000/alexanarch/issues
- ORCID: https://orcid.org/0009-0000-1599-0703

∮ = 1
