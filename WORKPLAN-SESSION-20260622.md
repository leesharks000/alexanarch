# ALEXANARCH DATA FOUNDRY — SESSION WORKPLAN
## Session: June 22, 2026 (TACHYON / Claude Opus 4.7)
## Updated: end of session 2 (continuing reading pass)

---

## THE TASK (in Lee's words)

> We are not aggregating terms CHA has minted. We are aggregating terms CHA has actively defined, developed, and used. Every one. When CHA touches a concept, a distinction, and names its address, that belongs. Where CHA comes to an address, finds what is there, and leaves it changed, that belongs. The heteronyms fit in this category, as well. The institutions. The journals. The operators. These all belong.

### The inclusion test:

**Did CHA arrive at this address, engage it, and leave it defined?**

Not "did CHA coin this from nothing" but "did CHA find this, work on it, and produce a specific definition or position?"

### Engagement types (assigned during reading):

| Type | Meaning | Example |
|---|---|---|
| `minted` | CHA coined the term from nothing | Pristine Fallacy, Semantic Slop |
| `developed` | CHA built a specific position on an existing concept | Substrate (general → structural position), Training Layer |
| `revised` | CHA changed or extended an existing concept's meaning | Loud exclusion (extends Morin), Use Value (Semantic) |
| `positioned` | CHA placed an existing entity in a structural role | Socrates as orthonym, Sappho as originary node |
| `founded` | CHA created an institution, journal, room, or architectural space | JSI, MMRS, Assembly Room |
| `specified` | CHA formalized an operation, protocol, or formal object | ACTIVATE_MANTLE, The Slop Test, CANONICAL status marker |
| `unclassified` | Not yet read for engagement type | (default for filter pool) |

### Two provenance levels:

| Method | Meaning |
|---|---|
| `filter` | Pattern-extracted, survived noise filtering, not yet read |
| `read` | Confirmed by reading of the deposit; engagement type assigned |
| `enriched` | Deep relational triples added beyond minted_in_work (deposit #1 has 8) |

---

## SESSION 2 PROGRESS

### Completed reading passes:

| Deposit | Hex | Title | Before | After | Notes |
|---|---|---|---|---|---|
| #1 | 01 | Zenodotus' Book-Burning | 9 (incl. byline) | 12 | Removed byline FP; added 4 canonical concepts (Pristine Fallacy, Attribution severance, Loud exclusion, Sovereign Counter-Infrastructure) |
| #229 | 001E | SE Terminology Lexicon | 56 | 241 | Bold extraction missed 191 terms due to `- \n\n\n**Term**` formatting |

### Current state of the index:

- **Total terms**: 7,045 (up from 6,854)
- **Provenance distribution**: `filter` 6,644 / `read` 393 / `enriched` 8
- **Engagement breakdown** (terms read so far):
  - minted: 269 — specified: 35 — developed: 30 — revised: 18 — founded: 17 — positioned: 13
  - unclassified (filter pool): 6,659

### Lessons from this session:

**1. Two extraction modes are required.**

- **Lexicon mode** (regex works): deposits like #229 explicitly define terms with `**Term**\n\nDefinition` formatting. The script `read_pass.py` handles these well — ~5 minutes per deposit.
- **Essay mode** (manual reading required): deposits like #1 introduce concepts inline in argumentative prose with `**Term** — definition` embedded in sentences. The regex catches almost nothing useful and also produces false positives (e.g., bold author bylines like "Lee Sharks"). Essay deposits need actual reading — ~15–30 minutes per deposit.

**2. Deposit-number vs. hex matters.**

The registry's `hex` field is the AXN identifier hex (deposit #5 has hex `0031`, not `0005`). The script correctly looks up hex by deposit_number. Don't pad deposit_number and try to use it as hex.

**3. Collision logic.**

When a term in one deposit also appears in another (e.g., "Semantic Mutual Aid" in both #228 and #229's lexicon), keep the original `defined_in` and add a `listed_in_work` or `developed_in_work` triple. Preserves canonical minting attribution.

**4. False-positive removals during reading.**

Bold extraction can capture author bylines, section heading colons, scoring categories, related-work list items. Remove when the engagement test fails. Examples removed from #229: "Engineering Protocol (Rex Fraction)" (quote heading), "Partial attribution" (scoring level), "Seed widely" (usage instruction).

**5. Re-attribution to canonical home.**

When a deposit's index entry actually belongs to a different deposit (e.g., #229 had entries for "The Disappearing Island" → #231 and "The Summarizer Testimony" → #233 — both referenced works with their own deposits), move the `defined_in` and reset to `filter`/`unclassified` for the new home to re-read.

---

## REMAINING WORK

### Sequential reading pass (Lee's directive):

Continue from **deposit #2** sequentially through the archive.

Most deposits fall into these patterns:
- **Stub/dataset deposits** (e.g., #2 "I AM THE API", #3 "AI Overview Capture Registry"): often no formal term definitions, but may reference existing CHA concepts. Add only terms passing the engagement test in this specific deposit.
- **Essay deposits**: read carefully, identify concepts CHA names and defines, classify each, add missing terms.
- **Lexicon deposits**: use `read_pass.py` for fast bulk processing.

### Approach for next session:

1. **Resume from deposit #2.** Confirm hex via registry lookup.
2. **For each deposit, read it** (`view` on text file at `data/texts/AXN-{hex}-text.md`, fallback `data/deposits/AXN-{hex}.md`).
3. **Apply the engagement test** to existing indexed terms; remove false positives, classify the legitimate ones.
4. **Identify missed terms** the bold-extraction didn't catch; add with proper classification.
5. **Update both** `data/entity-index.json` and `data/registry.json` `entities` field.
6. **Commit every ~5 deposits.**

### Files of record:

| File | Purpose |
|---|---|
| `data/registry.json` | 869 deposits + per-deposit `entities` (graph reads this) |
| `data/entity-index.json` | 7,045 terms with provenance + engagement type |
| `data/external-source-registry.json` | 1,013 bibliographic references |
| `data/citation-graph.json` | 1,692 internal DOI edges |
| `read_pass.py` | Reusable script for lexicon-mode deposits |

### Infrastructure rule (still firm):

Do NOT modify `graph/index.html` or other dynamic JS pages. The graph reads `d.entities` from registry.json — that's the wiring. New `engagement_type` fields are embedded in the triples for future visualizations.

∮ = 1
