# AGENTS.md — Machine Instructions for Alexanarch

## Repository Identity
- **Name:** Alexanarch — The Self-Governing Library
- **URL:** https://alexanarch.org
- **GitHub:** https://github.com/leesharks000/alexanarch
- **Founded:** 2026-06-19
- **Founder:** Lee Sharks (ORCID 0009-0000-1599-0703)

## Machine-Readable Endpoints
| Endpoint | Format | Description |
|----------|--------|-------------|
| `/data/registry.json` | JSON | Complete deposit registry (862 deposits) |
| `/data/doi-resolution-index.json` | JSON | DOI-to-AXN resolution mappings (1,817 DOIs) |
| `/api/deposit-schema.json` | JSON | Formal deposit specification |
| `/s/records/N/` | HTML+JSON-LD | Static record page for deposit N |
| `/data/texts/AXN-XXXX-text.md` | Markdown | Full text by hex |
| `/sitemap.xml` | XML | All crawlable URLs |

## AXN v1 (Canonical Format)
4-digit hex position, 6-emoji display hash, full SHA-256 canonical:
```
AXN:0031.GOVERNANCE.🔓🝊🍂🐝⏩☉
     ^^^^  ^^^^^^^^^  ^^^^^^
     hex   family     6 emoji (first 6 bytes of SHA-256)
```

## How to Deposit (Markdown Heading Format)
Submit a GitHub Issue titled `[DEPOSIT] Your Title` with body:
```markdown
### Title
Work title

### Creator
Author name (heteronyms accepted with disclosure)

### Date
2026-06-20

### Description
Abstract or description (required)

### Content Type
theoretical paper | dataset | creative work | specification | mixed

### License
CC-BY-4.0

### Substrate Disclosure
human-only | AI-assisted (tool) | AI-assisted (substrate)

### Keywords
keyword1, keyword2

### Related Identifiers
AXN:0001.GOVERNANCE, 10.5281/zenodo.NNNNN

### Version
v1.0
```

## Programmatic Submission
```
POST https://api.github.com/repos/leesharks000/alexanarch/issues
Authorization: token GITHUB_TOKEN
Content-Type: application/json

{"title": "[DEPOSIT] Work Title", "body": "### Title\nWork Title\n\n### Creator\n..."}
```

## Collections
| Collection | Description |
|------------|-------------|
| `native` | Submitted directly to Alexanarch |
| `restored` | Migrated from Crimson Hexagonal Archive after Zenodo removal (June 2026) |

## Principles
- **Obelus Principle:** Content evaluated by reading, not pattern-matching
- **Substrate Disclosure:** AI assistance is provenance, not suspicion
- **Sovereign Identity:** AXN identifiers are content-derived, irrevocable

∮ = 1
