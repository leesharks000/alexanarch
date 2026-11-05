# AI Overview Capture Registry — EA-WG-CAPTURES-01 v12.559

**1001 semantic addresses · 1193 captures · 104 dates · 2026-06-07 to 2026-11-04**

**Dr. Orin Trace** · ORCID 0009-0000-1599-0703 · 4 November 2026 · supersedes v12.167 (#1676)

A frozen checkpoint of the registry at its thousand-and-first address. The registry continues to accrue at its canonical store; this deposit fixes its state at v12.559 with the bundle's SHA-256, and every earlier edition points forward to it.

## 1. The citable unit

**ONE SURFACE + ONE SEMANTIC ADDRESS + ONE DATE = ONE CAPTURE.**

- **The capture** is citable at `captures/{slug}/`. Cite it for what a named system did.
- **The address** is citable at `addresses/{slug}/`. Cite it for what the address does across surfaces or over time.
- **The AXN.** Since 2026-10-27 each address holds one position in the shared allocation ledger (`AXN:<HEX>.CAPTURE`), and each observation carries an AXN whose glyphs derive from the SHA-256 of the observation sealed with its analysis and measures.

An address's slug is inherited from the first capture seated at it and is never renamed.

## 2. State at v12.559

**Sections, by address count:**

| Section | Addresses |
|---|---|
| Machine Reception | 263 |
| Works | 141 |
| Archive | 91 |
| Frameworks | 86 |
| Heteronyms | 83 |
| Semantic Economy | 49 |
| Coinages | 48 |
| Revelation & Theology | 32 |
| Classics & Philology | 29 |
| Provenance & Erasure | 25 |
| Institutions | 24 |
| Sites | 19 |
| People | 17 |
| Valuation | 17 |
| ∮ = 1 | 15 |
| Architecture | 13 |
| Platform Erosion | 12 |
| Reference & General Knowledge | 12 |
| Projects | 11 |
| Operative Semiotics | 10 |
| Concepts | 2 |
| Disciplines | 1 |
| Revelation First | 1 |

**Surfaces, by capture count:**

| Surface | Captures |
|---|---|
| Google AI Overview | 745 |
| ChatGPT (all recorded labels: 230 + 27 Luna 5.6 + 12 Luna + 8 chatgpt.com + 1 web, logged out) | 278 |
| Undetermined | 56 |
| Unresolved | 50 |
| Google AI Mode | 21 |
| Grok (8 x.com, 1 unlabelled) | 9 |
| Perplexity (one agentic) | 9 |
| Bing Copilot | 6 |
| Claude | 3 |
| Qwen (one Qwen 3.7) | 3 |
| Bing AI Overview | 2 |
| Google Knowledge panel | 2 |
| Single-capture surfaces (Bing AI Mode, Bing Copilot Search popup, Gemini, Google Scholar, a Google results page with no AI surface, ScholaRef, Domain Arrivals, SciLynk, TikTok Studio) | 9 |

Every capture now carries a surface label; at v12.167 four did not.

**Authentication state:** signed out and incognito 644; signed in 250; incognito 150; signed out 83; unrecorded 55; other recorded states 11.

**Evidence:** 1176 captures carry a verbatim transcript and 484 carry a frame. 907 carry the historical PER scalar, at a mean of 0.429 (0.506 at v12.167, 0.603 at v10.9). 1171 observations carry a dimensional PER (per_dim); 20 carry a pending record with its reason.

**Counted and held agree:** the registry declares 1193 observations and holds 1193. At v12.167 two addresses declared observations they did not hold (813 against 811); the count was corrected 2026-10-28.

## 3. The data flow

`data/EA-WG-CAPTURES-01.json` is the single writable authority (ratified 2026-08-17). The seat runs in this order:

1. `scripts/capture_intake.py --seat`, which admits, routes, normalises, validates and inserts, and derives the PER scalar from its four-unit vector;
2. `scripts/build_capture_gallery.py`;
3. `scripts/seat_capture_postflight.py`, which links, bakes, gates, builds the semantic-address layer and the address pages, allocates the AXNs, syncs the dataset projection and checks citability; a capture is seated when it exits 0.

Each batch of intake is kept as `rebuild/capture-registry/intake-YYYYMMDD-*/`, with the pastes as received, the operator's messages and the script that authored each capture, in which every quotation a finding rests on is asserted against its source before anything is written. A seated capture is revised in place by `scripts/revise_capture_entry.py`, which keeps its identity fields.

## 4. Files

Every file below is attached to this deposit and served at its link.

The **core data bundle** is [EA-WG-CAPTURES-01-v12.559.tar.gz](https://www.alexanarch.org/files/AXN-0C01/EA-WG-CAPTURES-01-v12.559.tar.gz) (41,499,991 bytes; SHA-256 `715534ba2fb483919c53142fdec1e6962aa907453faa9c78feb4dffddf3212a3`; 2,992 members). It holds:

- `data/EA-WG-CAPTURES-01.json`, the canonical store;
- `rebuild/capture-registry/`: the pipeline documents, the intake directories, the PER-dim atom sets and rubric, and the sealed rebuild store;
- `data/captures/axn.json` and `data/captures/sealed/`: the capture AXN index and the sealed observations it hashes;
- `data/capture-deposit-links.json`;
- `data/semantic-addresses.json`;
- `datasets/capture-registry/`;
- `captures/index.html`.

The **data files**, attached individually as frozen at v12.559:

- [EA-WG-CAPTURES-01-v12.559.json](https://www.alexanarch.org/files/AXN-0C01/EA-WG-CAPTURES-01-v12.559.json), the canonical store;
- [EA-WG-CAPTURES-01.schema.json](https://www.alexanarch.org/files/AXN-0C01/EA-WG-CAPTURES-01.schema.json), the entry schema;
- [semantic-addresses-v12.559.json](https://www.alexanarch.org/files/AXN-0C01/semantic-addresses-v12.559.json);
- [capture-deposit-links-v12.559.json](https://www.alexanarch.org/files/AXN-0C01/capture-deposit-links-v12.559.json);
- [captures-axn-v12.559.json](https://www.alexanarch.org/files/AXN-0C01/captures-axn-v12.559.json).

[manifest.json](https://www.alexanarch.org/files/AXN-0C01/manifest.json) lists 492 files with SHA-256, bytes, media type and role: the attached files, the bundle, and the **485 capture frames** (186.5 MB), each at its canonical path under `data/captures/{slug}/`, where the registry holds its images and galleries display them. Total manifested: 269.6 MB.

## 5. Version chain

v6.0 (#825) → v6.1 (#1397) → v7.0 (#1398) → v7.2 (#1396, #1401) → v8.3 (#3) → v8.9 (#936) → v10.9 (#1461) → v12.167 (#1676) → **v12.559 (this deposit)**

Between v12.167 and v12.559 the registry went from 633 addresses and 811 captures to 1001 and 1193. The intervening minor versions are recorded in the canonical file's correction log.

## 6. What changed in the instrument since v12.167

1. **Dimensional PER.** Written beside the historical scalar on 2026-10-19 (rubric v1.0) and re-read under rubric v1.1 on 2026-10-20, which adds the deep dimension (purpose and commitments), inversion and standing substitution. EA-PER-RECALC-01 (#1694) sets out the method across 946 observations. Since 2026-10-29 dimensional scoring is standard at intake: a capture seated without it carries a pending record with its reason, and one without a reason is counted as a breach.
2. **The scalar derived.** Since 2026-10-20 the PER scalar is computed from its four-unit vector at seating, never entered; 69 observations (2026-10-15) and 38 (2026-10-20) were re-derived where a hand-entered figure disagreed.
3. **AXNs for captures** (2026-10-27): one position per address, one AXN per observation (§1).
4. **Surfaces widened again**: ChatGPT from 167 captures to 278; Google AI Mode from 12 to 21; Bing AI Overview and Bing AI Mode; a second generated page composed from the archive's sources (Domain Arrivals, beside ScholaRef).
5. **Repairs kept to their mode**: phrases first marked untraced, traced on crimsonhexagonal.org (2026-10-17); one surface corrected (AXN:0B15, 2026-10-30); the operator's reading added to a seated capture in his words (2026-10-27).

## 7. Known defects at v12.559, recorded as data

**Defect counts, from the entries' own defect fields:**

| Defect | Count |
|---|---|
| citations-null | 243 |
| analysis-without-finding | 151 |
| truncated-by-interface | 145 |
| surface-unresolved | 50 |
| citations-unextracted | 47 |
| unsupported-citations | 10 |
| date-unresolved | 3 |
| stale-state | 2 |
| distinction-collapse | 1 |

**A stale summary field.** The registry's top-level `_defect_counts` still holds the figures of v12.167 (citations-null 166, analysis-without-finding 152, truncated-by-interface 126, surface-unresolved 50, unsupported-citations 10, date-unresolved 3); the table above is computed from the entries.

**Frames referenced and not held.** Two frames are referenced by bare filename and are held at no path in the repository: `screengrab-20260910-105838.png` and `screengrab-20260910-105901.png`; the manifest lists them under `frames_referenced_not_held`.

**Pending dimensional scores.** 20 observations carry `per_dim_pending`, each with its stated reason.

None of these is repaired in this snapshot. Repair is its own mode.
