# CONTROLLED TYPE VOCABULARY v1.0 — RATIFIED (MANUS 2026-08-03)
**Rulings:** Q1 ratified · Q2 SPLIT (framework/strategic brief AND white paper/business brief are two values) ·
Q3 integrity-lock is a NAMED GENRE, identical in kind to the fulfillment-operator documents (the triadic
binding structure: doc 1, doc 2, and doc 3 declaring that 2 fulfills 1) · Q4 patent-poem ratified ·
Q5 transitional wave APPROVED ("Genre pending (recovered)") · Q6 corrected by MANUS: the Gospel of
Antioch is SCRIPTURE — a gospel, containing no epistles, a mandala transform cast by hand on the model
of the Gospel of Thomas; a Scripture value is added. Correspondence/epistolary remains for actual
letter-works (e.g. letters within the Antioch volume).
**Basis:** MANUS ruling 2026-08-03 ("we'll need a controlled type vocabulary"). Unlocks the 159-row
compound batch (#1–#358) and the re-genre of ~360 condition-as-type records.
**Sources:** registry census (514 distinct values / 1,432 records), the sealed audit rows' target
phrases, and the archive's own named genres.

## 0 · The two axes (the load-bearing rule)

**content_type answers WHAT THE WORK IS (genre). It never answers what condition the record is in.**
Condition — recovered, semi-restored, metadata-only, withdrawn, lacuna — lives in the authoritative
fields (`body_status.class`, `canonical_text_status`, `lifecycle_state`) and is *derived* onto
banners and capsules by status_reconcile and the renderer. A record that says "Recovered blog-canonical
work" in content_type is declaring a condition where its genre should be; ~360 records currently do
this. The vocabulary makes the two axes unmixable.

## 1 · The controlled list (26 values + 2 transitional)

### Scholarly
| Canonical value | Scope note |
|---|---|
| **Theoretical paper** | primary theoretical contribution |
| **Scholarly essay** | essayistic scholarship; the "Archive work" suffix is collection branding, not type |
| **Empirical study** | measurement/observation with method (XR runs, PER studies, baseline readings) |
| **Close reading / companion analysis** | operative philology on a named work (e.g. the Cleis analysis) |
| **Forensic record / case study** | incident- or event-anchored documentation with analysis (FPC cases, removal forensics) |

### Technical / operative
| **Specification** | normative technical document (chamber specs, protocol specs) |
| **Methodological specification** | a method as the object (Assembly Chorus method, audit method) |
| **Constitution / governance framework** | founding governance texts |
| **Consulting framework / strategic brief** | strategic frameworks (Q2 split ruling) |
| **Consulting white paper / business brief** | client-facing white papers and business briefs |
| **Diagnostic probe** | instrument runs designed to elicit substrate behavior |
| **Metadata packet** | MPAI / disambiguation packets, publication-declaration packets |
| **Dataset** | data as the object (capture registries, audit ledgers, indexes) |
| **Navigation map** | cartographic bibliography / semantic interface layouts (IDP maps) |
| **Traversal log / field observation** | first-person traversal and field notes |
| **Technical correction** | erratum / correction as its own object |
| **Integrity-lock / fulfillment architecture** | NAMED GENRE (Q3): documents that bind or fulfill other documents — integrity locks, non-severability bindings, and fulfillment-operator triads (doc 1, doc 2, doc 3 declaring 2-fulfills-1) |

### Archival & governance acts
| **Effective Act** | canonization, bestowal, founding acts (subsumes founding/bestowal document) |
| **Provenance document** | provenance nodes, anchors, continuity records |
| **Continuity tether** | GW-chain tethers specifically |
| **Witness documentation** | traversal-event / witness ratification records |
| **Proof dossier / evidence appendix** | evidence compilations attached to claims |
| **Lacuna Mark** | declared absence under EA-LACUNA-PROTOCOL-01 |
| **Withdrawn — external work (typed tombstone)** | foreign-capture tombstones (already in force) |

### Creative
| **Poetry** | poems and collections (subsumes "Creative work (poetry)") |
| **Patent-poem** | the named archive genre; kept distinct by MANUS practice |
| **Creative prose** | fiction, stories, creative nonfiction |
| **Creative work (mixed)** | braided/composite works (e.g. Cleis-class collections that interleave genres) |
| **Correspondence / epistolary** | letters as the object (Gospel-of-Antioch class where applicable) |
| **Visual schema / diagram** | canonical visual schema / diagrammatic metaphysics |
| **Scripture** | gospels and scripture-form works, incl. hand-cast mandala transforms on gospel models (Gospel of Antioch class; Q6 MANUS correction) |

### Transitional (temporary, burn-down targets — not ratified genres)
| **Genre pending (recovered)** | for the ~360 condition-as-type records until their genre wave runs |
| **Genre pending (capture)** | metadata captures whose underlying work's genre is not yet determined |

## 2 · Mapping table — audit target phrases → canonical

| Sealed-row phrase | Canonical |
|---|---|
| founding/bestowal document | Effective Act |
| Effective Act/canonization type | Effective Act |
| meta-deposit/Other | Metadata packet |
| chamber-specification | Specification |
| traversal-event/witness documentation | Witness documentation |
| forensic record / case study; FPC case-study | Forensic record / case study |
| proof-dossier/evidence-appendix | Proof dossier / evidence appendix |
| explicit technical-correction | Technical correction |
| cartographic-bibliography/navigation-map | Navigation map |
| canonical visual schema / diagrammatic metaphysics | Visual schema / diagram |
| constitution / governance framework | Constitution / governance framework |
| integrity-lock architecture / binding specification | Integrity-lock / fulfillment architecture |
| consulting framework/strategic brief | Consulting framework / strategic brief |
| consulting white paper/business brief | Consulting white paper / business brief |
| scholarly essay (w/ archive-suffix-as-branding) | Scholarly essay |
| diagnostic type | Diagnostic probe |
| metadata packet for a publication/declaration | Metadata packet |

## 3 · Mapping table — current census values → canonical (top offenders)

| Current | Canonical | Note |
|---|---|---|
| Recovered blog-canonical work (…) ×130 | *(genre per record)* → transitional **Genre pending (recovered)** | condition string; genre wave to follow |
| Recovered work (full text seated) ×112 | same as above | |
| Metadata capture ×117; DataCite metadata capture / semi-restored ×6 | **Genre pending (capture)** or the known genre | capture-ness → body_status |
| Creative work ×34; Creative work (poetry) ×13; (connected to research) ×5 | **Poetry** / **Creative prose** / **Creative work (mixed)** per record | |
| Short work ×21 | *(genre per record — "short" is length, not genre)* | audit rows already name targets |
| Archive work ×28 | **Scholarly essay** (suffix = branding) per sealed rows | |
| Navigation document ×10; Navigation map ×6 | **Navigation map** | |
| Traversal log ×8; Traversal log / field observation ×6 | **Traversal log / field observation** | |
| Named-position provenance anchor ×9; Continuity record ×5 | **Provenance document** | |
| Continuity tether ×4 | **Continuity tether** | |
| text/markdown ×10 | *(a MIME type, not a genre — genre per record)* | |
| Patent application / patent-poem ×4 | **Patent-poem** | |
| Specification / executable research surface ×4 | **Specification** | |

## 4 · Rules of application
1. Values are used **verbatim** from the list; no ad-hoc coinages. A needed new genre is proposed to
   MANUS and added by ratified amendment (this file, versioned), never invented row-by-row.
2. Qualifiers beyond the value go in **keywords or description**, never appended to content_type.
3. Conversions run through §5b (propagation) like any repair, ledger-backed to sealed rows or to this
   vocabulary's mapping tables under batch authority once ratified.
4. The two transitional values are burn-down targets with a standing queue; they may not be applied
   to NEW records.
5. field_discipline.py's CONDITION regex becomes a hard validator: any content_type matching a
   condition pattern fails the gate.

## 5 · Ratification record (questions as posed; rulings in header)
- **Q1.** Ratify the 26-value list as-is, or amend (add/remove/rename)?
- **Q2.** "Consulting brief" as ONE value subsuming framework/strategic/white-paper/business — or keep two (framework vs. white paper)?
- **Q3.** "Integrity-lock architecture / binding specification" → folded into **Specification** (as drafted) or kept distinct?
- **Q4.** Patent-poem distinct (as drafted) — confirm?
- **Q5.** The ~360 condition-as-type records: approve the transitional **Genre pending (recovered/capture)** wave (mechanical, restores the two-axis rule immediately), with per-record genre assignment as a follow-on wave?
- **Q6.** "Correspondence / epistolary": apply to Gospel-of-Antioch–class records, or keep those under Creative prose?


## 6 · PROPOSED AMENDMENTS v1.1 (from Wave C holds — awaiting MANUS word)
The 35 unmappable sealed recommendations cluster into genres the list lacks. Proposed additions:
| Proposed value | Evidence from holds |
|---|---|
| **Invocation** | ×2 — the archive's invocation-form works (Space Ark trigger class) |
| **Book / manuscript** | Pocket Humans book/manuscript |
| **Working paper** | Semantic Economy working paper; draft book work plan |
| **Edited journal issue** | Grammata/Trans-SEI issue objects |
| **Call for papers / announcement** | journal announcements |
| **Implementation report** | build/implementation reports |
| **Software / executable apparatus** | self-describing knowledge graph; semantic routing machine |
| **Score / executable transform** | musical-register structural transform / executable score (Musical Ark class) |
One word ratifies any subset; unratified holds keep their current values and stay queued
(vocab_v1.1_amendment_candidates.json).
