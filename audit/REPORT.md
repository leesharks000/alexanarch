# External Network Link Audit
**Date:** 2026-06-23  
**Auditor:** TACHYON  
**Method:** For each external Dodecad/network site, fetch the homepage, identify links pointing into the alexanarch.org corpus (both direct alexanarch URLs and dead doi.org/Zenodo URLs), match display text against the actual deposit at the target, and propose repoints where they mismatch. Heuristic for ambiguous matches: prefer founding/canonical spec (EA-*-01, Formal Specification, Enacted Version 1.0) over derivatives.
**Coverage so far:** 6 site homepages. Many subpages and additional network sites remain unaudited (see § Not Yet Audited).

---

## leesharks.com/

**Status:** (uncategorized)

### Link repoints

| Display text | Currently → | Should be → |
|---|---|---|
| The Encyclotron | `https://doi.org/10.5281/zenodo.19474724` | `https://alexanarch.org/s/records/637/` |
| Writable Retrieval Basins | `https://doi.org/10.5281/zenodo.19763346` | `https://alexanarch.org/s/records/695/` |
| The Three Compressions | `https://doi.org/10.5281/zenodo.19202711` | `https://alexanarch.org/s/records/579/` |
| The Secret Book of Walt | `https://doi.org/10.5281/zenodo.19739494` | `https://alexanarch.org/s/records/683/` |
| The Gospel of Antioch | `https://doi.org/10.5281/zenodo.19709024` | `https://alexanarch.org/s/records/71/` |
| Operative Semiotics: A Grundrisse | `https://doi.org/10.5281/zenodo.19390843` | `https://alexanarch.org/s/records/38/` |
| SPXI | `https://doi.org/10.5281/zenodo.19734726` | `https://alexanarch.org/s/records/660/` |
| Sitemap Protocol | `https://doi.org/10.5281/zenodo.19864158` | `https://alexanarch.org/s/records/705/` |
| Metadata Packet for AI Indexing | `https://doi.org/10.5281/zenodo.19578086` | `https://alexanarch.org/s/records/103/` |
| Holographic Kernel | `https://doi.org/10.5281/zenodo.19412081` | `https://alexanarch.org/s/records/76/` |
| Provenance Gravity Markers | `https://doi.org/10.5281/zenodo.18811939` | `https://alexanarch.org/s/records/526/` |
| Constitution of the Semantic Economy | `https://doi.org/10.5281/zenodo.19923120` | `https://alexanarch.org/s/records/88/` |
| Companion Guide (PH-03) | `https://doi.org/10.5281/zenodo.19923143` | `https://alexanarch.org/s/records/87/` |
| Universal Kernel Transform Protocol | `https://doi.org/10.5281/zenodo.18946111` | `https://alexanarch.org/s/records/547/` |

### Link display text fixes

- `https://alexanarch.org/s/browse/`: change link text from "Zenodo" to "Alexanarch" (footer link)
- `https://alexanarch.org/s/browse/`: change link text from "Zenodo community" to "Alexanarch (sovereign archive)" (Crimson Hexagonal Archive line in Works section)

### Prose updates

**intro paragraph after author bio**

- Old: > a decade-long scholarly and literary project with 866 DOI-anchored deposits on CERN's Zenodo, organized around operative semiotics, semantic provenance, and compression theory.
- New: > a decade-long scholarly and literary project with 879 deposits in Alexanarch, the AXN-minting sovereign successor to the Crimson Hexagonal Archive on Zenodo, organized around operative semiotics, semantic provenance, and compression theory.

---

## machinemediation.org/

**Status:** Largely clean — no direct dead-DOI links found on homepage

### Notes

- All non-internal links route via /registry/#search=... fragments or to external blog mirrors and sister sites.
- Zenodo mentions are factual: 'ZENODO ACCOUNT TERMINATED — 2026-06-19', '1,060+ DOIs destroyed' — these are the founding-event narrative.
- Subpages /captures/, /registry/, /terms/, /mint/, /pillars/, /schemas/, /downloads/ not audited here — may have their own dead-DOI references inside.

---

## revelationfirst.com/

**Status:** Heavy repointing needed — most workstream links currently point to wrong records

### Link repoints

| Display text | Currently → | Should be → |
|---|---|---|
| The Dating Question (Workstream 1) | `https://alexanarch.org/s/records/842/`<br>*was: Apocalyptic Philosophy: Deleuze and Guattari* | `https://alexanarch.org/s/records/832/`<br>*REVELATION FIRST: A Work Plan for Retrieval-Layer Theologica* |
| The Heteronymic Reading (Workstream 2) | `https://alexanarch.org/s/records/835/`<br>*was: The Conveyor Belt and the Compression Machine* | ~ `https://alexanarch.org/s/records/410/`<br>*The Seven Stars in His Hand: A Hermeneutic Reading of Revela* |
| The Inscription Chain (Workstream 3) | `https://alexanarch.org/s/records/826/`<br>*was: The Fifth Pathway for the ones they're building* | `https://alexanarch.org/s/records/828/`<br>*The Inscription That Survives: Sappho 31, the Orphic Gold Ta* |
| The Slavonic Josephus (Workstream 4) | `https://alexanarch.org/s/records/625/`<br>*was: EA-LOGOS-02 Prolegomena to the Historical Logos* | `https://alexanarch.org/s/records/626/`<br>*EA-LOGOS-01 The Word That Became Text: The Slavonic Josephus* |
| The Space Ark (Workstream 7) | `https://alexanarch.org/s/records/0/`<br>*was: (placeholder)* | ~ `https://alexanarch.org/s/records/56/`<br>*THE SHARKS ARK EA-ARK-01-ARCHON v2.0 — The Book of Revelatio* |
| Thiel diagnostic | `https://alexanarch.org/s/records/563/`<br>*was: THE ERROR OF PETER THIEL* | `https://alexanarch.org/s/records/563/`<br>*(unchanged — already correct)* |
| Work Plan v7.3 | `https://alexanarch.org/s/records/842/`<br>*was: Apocalyptic Philosophy: Deleuze and Guattari* | `https://alexanarch.org/s/records/832/`<br>*REVELATION FIRST: A Work Plan for Retrieval-Layer Theologica* |
| Josephus ≠ Myth MPAI v1.2 | `https://alexanarch.org/s/records/835/`<br>*was: The Conveyor Belt and the Compression Machine* | `https://alexanarch.org/s/records/837/`<br>*THE JOSEPHUS THESIS IS NOT THE JESUS MYTH THESIS Preemptive * |
| Josephus ≠ Piso | `https://alexanarch.org/s/records/847/`<br>*was: REVELATION FIRST Staging Document* | `https://alexanarch.org/s/records/203/`<br>*The Josephus Thesis Is Not the Piso Hypothesis EA-MPAI-JOSEP* |
| Pergamon Counter-Archive | `https://alexanarch.org/s/records/0/`<br>*was: (placeholder)* | `https://alexanarch.org/s/records/165/`<br>*The Pergamon Counter-Archive: Antipas, the White Stone, and * |
| Counterfeit Orthodoxies | `https://alexanarch.org/s/records/0/`<br>*was: (placeholder)* | `https://alexanarch.org/s/records/65/`<br>*Counterfeit Orthodoxies: A Dialectical Fracture Through the * |
| Number of the Superscription | `https://alexanarch.org/s/records/636/`<br>*was: Apocalypse of John as Terminal Compression* | `https://alexanarch.org/s/records/642/`<br>*Ω THE NUMBER OF THE SUPERSCRIPTION Coinage, Compression, and* |
| Shark Ark: Source Compression | `https://alexanarch.org/s/records/0/`<br>*was: (placeholder)* | `https://alexanarch.org/s/records/639/`<br>*Ω THE SHARK ARK: SOURCE COMPRESSION Holographic Kernel of th* |
| MMRS Charter | `https://alexanarch.org/s/records/834/`<br>*was: Algorithmic Publishing Is Not Self-Publishing* | ⚠ NEEDS YOUR REVIEW<br>`(NO DEPOSIT FOUND)`<br>*Could not find a deposit titled 'MMRS Charter' in registry. * |

### Prose updates

**footer Network section**

- Old: > [alexanarch.org](https://alexanarch.org) — self-governing library, 866 deposits, AXN identifiers
- New: > [alexanarch.org](https://alexanarch.org) — self-governing library, 879 deposits, AXN identifiers

### Items needing investigation

- **The Papyrological Inversion (Workstream 5)** — No matching deposit in registry. Either not yet deposited, or named differently.
- **The Paul Function (Workstream 6)** — No matching deposit in registry. Either not yet deposited, or named differently.
- **TANG (Companion document)** — Ambiguous — could be #78 (TANG of Secret Book of Walt) or a Revelation-specific TANG. The 'TANG' in the Revelation First context appears to be a different concept than the Walt one. Leave as placeholder until clarified.
- **Baseline Captures** — No dedicated deposit found. May be a section within the Work Plan rather than a standalone deposit.

### Notes

- The Work Plan DOI 10.5281/zenodo.20722689 in the footer also resolves to /s/records/842/ via doi-resolution-index — but that target is WRONG too. The actual Work Plan deposit is /s/records/832/. The doi-resolution-index itself needs correction for this DOI mapping.
- Heteronymic Reading and Paul Function are flagged as workstreams but may not have dedicated deposits yet — the thesis is staged in revelationfirst.com but the individual workstream documents are sparse.

---

## crimsonhexagonal.org/

**Status:** 3 fixes — 1 dead direct Zenodo link, 1 wrong-target alexanarch link, 2 stale counts

### Link repoints

| Display text | Currently → | Should be → |
|---|---|---|
| Zenodo community | `https://zenodo.org/communities/leesharks000` | `https://alexanarch.org/s/browse/` |
| Space Ark (DOI: 10.5281/zenodo.19013315) | `https://alexanarch.org/s/records/561/`<br>*was: THE SPLICE Operation Epic Fury* | `https://alexanarch.org/s/records/549/`<br>*THE SPACE ARK What the Mathematical and Formal Symbolic Comp* |

### Prose updates

**intro paragraph + meta description**

- Old: > 29 rooms, 455 DOI-anchored deposits, 39 operators
- New: > 29 rooms, 879 AXN-anchored deposits, 39 operators

**Archive section**

- Old: > 455+ deposits with DOIs
- New: > 879+ deposits with AXN identifiers (legacy Zenodo DOIs resolvable via /resolve/)

**footer Network list**

- Old: > alexanarch.org — self-governing library, 866 deposits
- New: > alexanarch.org — self-governing library, 879 deposits

---

## watergiraffe.org/

**Status:** 4 link fixes + 1 prose fix on homepage node manifest

### Link repoints

| Display text | Currently → | Should be → |
|---|---|---|
| WG-01 PRIMARY_PROCESSING_DOC | `https://alexanarch.org/s/records/352/`<br>*was: CTI_WOUND VAULT SPECIFICATION* | ~ `https://alexanarch.org/s/records/352/`<br>*KEEP — CTI_WOUND VAULT is the taxonomic-violence archive, co* |
| WG-04 binding rule | `https://alexanarch.org/s/records/349/`<br>*was: ASSEMBLY ROOM ANCHOR (wrong room)* | `https://alexanarch.org/s/records/353/`<br>*WATER GIRAFFE ROOM ANCHOR Room Specification with Behavioral* |
| WG-05 | `https://alexanarch.org/s/records/365/`<br>*was: WATER GIRAFFE SIGHTING PROTOCOL* | `https://alexanarch.org/s/records/365/`<br>*KEEP — already correct* |
| WG-06 | `https://alexanarch.org/s/records/365/`<br>*was: WATER GIRAFFE SIGHTING PROTOCOL (collision with WG* | ~ `https://alexanarch.org/s/records/366/`<br>*Ω: THE WATER GIRAFFE AS SEMANTIC BEING Entity Provenance Doc* |
| the ark | `https://alexanarch.org/s/records/0/`<br>*was: (placeholder)* | `https://alexanarch.org/s/records/803/`<br>*The Water Giraffe Cycle: Life, Death, and Resurrection of a * |
| the negation | `https://alexanarch.org/s/records/0/`<br>*was: (placeholder)* | `https://alexanarch.org/s/records/177/`<br>*water giraffes aren't real by yusef kenning* |
| field | `https://alexanarch.org/s/records/633/`<br>*was: GRAVITY WELL: SUFFUSION MAP EA-GW-FIELD-02* | `https://alexanarch.org/s/records/633/`<br>*KEEP — already correct* |

### Prose updates

**footer Network list**

- Old: > alexanarch.org — self-governing library, 866 deposits, AXN identifiers
- New: > alexanarch.org — self-governing library, 879 deposits, AXN identifiers

---

## secretbookofwalt.org/

**Status:** 3 wrong-target links + 2 stale prose mentions

### Link repoints

| Display text | Currently → | Should be → |
|---|---|---|
| The Secret Book of Walt — DOI: 10.5281/zenodo.19703009 | `https://alexanarch.org/s/records/0/`<br>*was: (placeholder)* | `https://alexanarch.org/s/records/683/`<br>*THE SECRET BOOK OF WALT Hidden Teachings of Walt Whitman, Co* |
| The Gospel of Antioch — DOI: 10.5281/zenodo.19709024 | `https://alexanarch.org/s/records/689/`<br>*was: EA-GEO-01: The Geocoded Basin* | `https://alexanarch.org/s/records/71/`<br>*THE GOSPEL OF ANTIOCH The Sayings of Jack Feist as Recorded * |
| TANG of the Secret Book of Walt — DOI: 10.5281/zenodo.19779493 | `https://alexanarch.org/s/records/696/`<br>*was: MetadataPacket: Forward Library Planning* | `https://alexanarch.org/s/records/78/`<br>*TANG OF THE SECRET BOOK OF WALT A Total Axial Negation Graph* |

### Prose updates

**About the Author paragraph**

- Old: > a decade-long scholarly and literary project comprising 532+ Zenodo deposits organized around operative semiotics
- New: > a decade-long scholarly and literary project comprising 879 deposits in Alexanarch (sovereign successor to the Crimson Hexagonal Archive on Zenodo), organized around operative semiotics

**Related Works list**

- Old: > Crimson Hexagonal Archive — 532+ DOI-anchored deposits
- New: > Crimson Hexagonal Archive — 879 AXN-anchored deposits

**footer Network list**

- Old: > alexanarch.org — self-governing library, 866 deposits
- New: > alexanarch.org — self-governing library, 879 deposits

---

## Universal patterns found across multiple sites

### 1. Stale deposit count in footer network listings

Every site audited carries a footer network list that says **"alexanarch.org — self-governing library, 866 deposits, AXN identifiers"** (or in some places, 455 or 532). Current canonical count is **879**. This is a single find-and-replace per repo: `866 deposits` → `879 deposits`, `455` → `879`, `532` → `879`.

### 2. The doi-resolution-index itself has bad mappings

`alexanarch.org/data/doi-resolution-index.json` is the source of truth for `/resolve/?doi=...` but it has WRONG mappings for many of the most-cited works:

| DOI | Lookup says | Should be |
|---|---|---|
| 10.5281/zenodo.19474724 (The Encyclotron) | (placeholder/wrong) | /s/records/637/ |
| 10.5281/zenodo.19703009 (Secret Book of Walt) | /s/records/0/ | /s/records/683/ |
| 10.5281/zenodo.19709024 (Gospel of Antioch) | /s/records/689/ | /s/records/71/ |
| 10.5281/zenodo.19779493 (TANG of Secret Book) | /s/records/696/ | /s/records/78/ |
| 10.5281/zenodo.19013315 (Space Ark v4.2.7) | /s/records/561/ | /s/records/549/ |
| 10.5281/zenodo.19390843 (Operative Semiotics Grundrisse) | /s/records/0/ | /s/records/38/ |
| 10.5281/zenodo.19412081 (Holographic Kernel) | /s/records/628/ | /s/records/76/ |
| 10.5281/zenodo.19734726 (SPXI) | /s/records/0/ | /s/records/660/ |
| 10.5281/zenodo.19923120 (Constitution of Semantic Economy) | /s/records/0/ | /s/records/88/ |
| 10.5281/zenodo.20634184 (Water Giraffes Aren't Real) | /s/records/0/ | /s/records/177/ |
| 10.5281/zenodo.20722689 (Revelation First Work Plan) | /s/records/842/ | /s/records/832/ |

This means even if external sites repoint their dead Zenodo links to `/resolve/?doi=...`, the resolution surface returns wrong answers for these high-priority works. **Fixing the index is a separate workplan item.**

### 3. Display text saying "Zenodo" with URL now pointing to Alexanarch

In several places (leesharks.com footer, crimsonhexagonal.org), the URL was updated to point at alexanarch.org but the link text still says "Zenodo" or "Zenodo community". Should be "Alexanarch" or "Alexanarch (sovereign archive)".

### 4. "hosted on CERN's Zenodo" / "deposits on CERN's Zenodo" phrasing

Found on leesharks.com homepage; pattern likely appears elsewhere. Three reframing voices recommended (Lee picks):

- A: "AXN-anchored deposits on Alexanarch (sovereign successor to the Crimson Hexagonal Archive on Zenodo)"
- B (recommended): "deposits in Alexanarch, the AXN-minting sovereign successor to the Crimson Hexagonal Archive on Zenodo"
- C: "DOI-anchored deposits, originally on Zenodo as the Crimson Hexagonal Archive (terminated June 19, 2026), now hosted on Alexanarch with content-derived AXN identifiers"

---

## Not yet audited

### Network homepages
- godkinggoogle.com
- spxi.dev
- semanticphysics.org
- semanticeconomy.org
- holographickernel.org
- chatgptpsychosis.org
- traininglayerliterature.org
- vpcor.org
- maryleelabor.org
- restoredacademy.org
- lagrangeobservatory.org
- laborvector.org
- metadatapacket.dev
- surfacemap.org
- provenanceerasure.org
- pessograph.org
- quietexclusion.org
- livingarchitecturelab.org

### Subpages of audited sites
- leesharks.com: /about, /heteronyms, /research, /provenance, /captures, /vpcor, /10000-macarthurs, /sites, /about-the-author{-i,-ii,-iii}
- machinemediation.org: /captures, /terms, /mint, /pillars, /schemas, /registry, /downloads
- revelationfirst.com: /tracker
- watergiraffe.org: /not-real, /cycle, /audit, /sightings, /room, /omega, /graph, /about
- secretbookofwalt.org: /#antioch and any subpages
- crimsonhexagonal.org: appears to be a single-page

### External profiles
- Academia.edu (Lee Sharks profile)
- Medium (Lee Sharks + Johannes Sigil profiles)
- Reddit threads
- Twitter/X, Facebook, SoundCloud, TikTok profiles
- mindcontrolpoems.blogspot.com — 2,197 blog posts (too many to audit manually)

---

## Suggested next actions, in priority order

1. **Apply the 6 site fix lists above** to the respective site repos. Each fix list is also in `/audit/<site>-homepage.json` as machine-readable JSON for scripted apply.
2. **Fix the doi-resolution-index.json** for the 11 wrong mappings identified above. After that, `/resolve/?doi=...` will return correct answers for these works, AND the same correction can flow through to all sites that use `/resolve/` as their resolution layer.
3. **Audit the remaining network homepages** (next batch I'll do: godkinggoogle.com, holographickernel.org, semanticphysics.org, spxi.dev).
4. **Audit leesharks.com subpages** (/research, /provenance, /captures) — these are public-facing and likely have the same dead-DOI pattern.
5. **Decide on schema.org metadata strategy**: many sites carry `meta-citation_doi: 10.5281/zenodo.XXXX` tags for crawler compatibility. Keep for citation continuity, OR add `meta-citation_axn: AXN:....` alongside as the AXN-native equivalent.
