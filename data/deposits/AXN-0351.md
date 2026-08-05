# CRIMSON HEXAGONAL ARCHIVE: TERM INDEX WORK PLAN
## EA-REGISTRY-TERMINDEX-PLAN v1.0


**Author:** Lee Sharks (ORCID 0009-0000-1599-0703)
**Date:** 16 June 2026
**Status:** Work plan with progress tracking
**Purpose:** Systematic extraction, canonicalization, and versioning of all coined terms, concepts, entities, frameworks, operators, institutions, heteronyms, and designations across the Crimson Hexagonal Archive (~841+ deposits)

---

## Rationale


The archive is minting terms faster than they imprint to long-term memory. An estimated 200-300 coined concepts exist across 841+ deposits without a unified index. Once built, the index becomes:

- A retrieval surface (each term becomes a searchable node)
- A density map (which terms cluster, which are orphaned)
- A versioning base (new deposits append; the initial build is the hard part)
- An MPAI generator (each indexed term can receive a provenance coupling kernel)
- A measure of the archive's actual vocabulary (what it has coined vs. what it thinks it has coined)


---

## Phase 1: Metadata Pull


**Status:** NOT STARTED
**Estimated compute:** 30-45 minutes
**Resumable:** Yes — paginate via Zenodo API, save after each page
### 1.1 Pull all records from crimsonhexagonal community

- API endpoint: https://zenodo.org/api/records?communities=crimsonhexagonal&size=200&page=N
- Expected: ~841 records across 5 pages
- Save: JSON file with record ID, DOI, title, description, keywords, creators, publication_date, version, related_identifiers
- Output: termindex-metadata-raw.json

### 1.2 Extract terms from metadata fields

- Parse each record's title, keywords, and description
- Extract: capitalized multi-word phrases, EA-* codes, quoted terms, terms in bold/strong tags
- Output: termindex-metadata-terms.json — rough list with source DOI for each term

### 1.3 Deduplicate and categorize

- Categories: metric, operator, framework, institution, heteronym, journal, concept, designation, entity, tool
- Canonical form + variants
- Output: termindex-metadata-canonical.json


**Progress checkpoint:** After Phase 1, we have ~60-70% of coinages from metadata alone. Save all three files to /home/claude/ and present. If session compacts here, next session loads these files and proceeds to Phase 2.

---

## Phase 2: File Content Extraction


**Status:** NOT STARTED
**Estimated compute:** 2-3 hours (may require multiple sessions)
**Resumable:** Yes — track which record IDs have been processed
### 2.1 Download and read markdown files

- For each record, download .md files (skip PDFs, images, audio)
- Read each file, extract terms not already in Phase 1 output
- Track progress: termindex-file-progress.json — list of processed record IDs
- Output: termindex-file-terms.json

### 2.2 Batch processing strategy

- Process in batches of 50 records
- After each batch: save progress, save extracted terms
- If session compacts: next session reads progress file, resumes from last batch

### 2.3 Merge with metadata terms

- Combine Phase 1 and Phase 2 extractions
- Identify terms that appear only in file contents (not metadata)
- Output: termindex-merged.json


**Progress checkpoint:** After Phase 2, we have ~90% of coinages. The remaining 10% are implicit terms that require human judgment.

---

## Phase 3: Human-in-the-Loop Pass


**Status:** NOT STARTED
**Estimated compute:** 1-2 sessions of review
### 3.1 Lee reviews the merged index

- Flag false positives (ordinary words extracted as coinages)
- Flag missing terms (coinages Lee knows exist but weren't extracted)
- Assign canonical definitions (20 words max per term)
- Confirm categories

### 3.2 Cross-reference against known lists

- Dodecad heteronyms (12 positions)
- Framework numbering (FW1-FW15)
- Journal names (6 journals, 2 imprints)
- EA-* designation system
- Hex prefix allocations
- Room system (r.01-r.26)
- Operator registry (LOS, THUMB, UKTP, etc.)

### 3.3 Output: termindex-v1.0.json

- Full canonical index with:

term, abbreviation, category, canonical_definition
- first_deposit (DOI), author_position (heteronym)
- related_terms, hex_prefix, framework_number
- variants (alternate forms that should resolve to this entry)


---

## Phase 4: Deposit and Surface


**Status:** NOT STARTED
### 4.1 Deposit to Zenodo

- EA-REGISTRY-TERMINDEX-01 v1.0
- JSON + markdown rendering
- Community: crimsonhexagonal
- Keywords: term index, coined concepts, semantic physics, operative semiotics, Crimson Hexagonal Archive

### 4.2 Surface deployment

- Page on leesharks.com or crimsonhexagonal.org
- Searchable, sortable table
- Each term links to its first-deposit DOI

### 4.3 Versioning protocol

- Each new deposit session: extract terms from new deposits, append to index
- Version forward: v1.1, v1.2, etc.
- The initial build (Phases 1-3) is the hard part; versioning is incremental


---

## Phase 5: MPAI Generation (optional, high-value)


**Status:** NOT STARTED
### 5.1 For each high-priority term, generate an MPAI kernel

- Provenance coupling statement
- Non-erasure condition
- Canonical definition
- First-deposit DOI

### 5.2 Batch deposit MPAIs

- 10-20 per session
- Priority: terms most likely to enter the retrieval basin


---

## Progress Tracking


Phase
Step
Status
Output File
Records Processed
Notes


1
1.1 Metadata pull
COMPLETE
termindex-metadata-raw.json
845/845
845 records, 6,256 unique kw


1
1.2 Term extraction
COMPLETE
termindex-metadata-terms.json
845/845
1,524 terms (count>=2), 5,951 total


1
1.3 Canonicalization
COMPLETE
termindex-tiered.json
845/845
178 Tier 1, 332 Tier 2, cross-ref with registry


2
2.1 File download
COMPLETE
termindex-file-progress.json
735/800
444 new Tier 1, 540 new Tier 2 from file contents


2
2.2 Batch processing
COMPLETE
termindex-file-progress.json
735/800
65 records had download failures


2
2.3 Merge
PENDING
termindex-merged.json
—
Needs noise filtering + human review


3
3.1 Human review
PENDING
—
—
~2,000 terms for review


3
3.2 Cross-reference
COMPLETE
termindex-crossref.json
—
129/131 registry queries matched


3
3.3 Final index
PENDING
termindex-v1.0.json
—
After human review


4
4.1 Deposit
IN PROGRESS
—
—
Initial deposit with raw data


4
4.2 Surface
NOT STARTED
—
—


5
5.1 MPAI generation
NOT STARTED
—
—


---

## Continuity Protocol


If a session hits compaction limits during this work:

- All progress files are saved to /home/claude/ and presented via present_files
- The progress tracking table above is updated in this document
- The next session receives this work plan document and any saved progress files
- The next session reads the progress table, loads saved files, and resumes from the last completed step


**Key files for continuity:**

- This work plan: termindex-workplan.md
- Raw metadata: termindex-metadata-raw.json
- Extracted terms: termindex-metadata-terms.json
- Canonical index: termindex-metadata-canonical.json
- File processing progress: termindex-file-progress.json
- File-extracted terms: termindex-file-terms.json
- Merged index: termindex-merged.json
- Final index: termindex-v1.0.json


---

## Session Log


**Session 1 (16 June 2026):** Work plan created. Phase 1.1 complete (845 records pulled). Phase 1.2 complete (1,524 terms extracted with count>=2; 5,951 total unique keywords). Phase 1.3 (canonicalization and categorization) ready for next session or human review. Key finding: the archive has 6,256 keyword instances across 845 records, with the top terms being Crimson Hexagonal Archive (439), semantic economy (267), Crimson hexagon (248), distributed epic (154), NH-OS (149), operative semiotics (124), training layer literature (121). The API paginates at max size=25, requiring 34 pages. The metadata-raw and metadata-terms JSON files are the continuity artifacts for the next session.