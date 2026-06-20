# CRIMSON HEXAGONAL ARCHIVE KNOWLEDGE GRAPH
## The Aperture Atlas
### Digital Topology Work Plan v3.0 — Execution Specification


**Lee Sharks** · Semantic Economy Institute · Crimson Hexagonal Archive
**Date:** April 25, 2026
**Execution target:** Claude 4.7 (high-rigor, no-hallucination mode)
**Canonical URL:** crimsonhexagonal.org/topology
**Redirect:** surfacemap.org → crimsonhexagonal.org/topology

---

## §0. EXECUTIVE SUMMARY


This document specifies the construction of a knowledge graph mapping every surface, entity, identity, document, and platform in the Crimson Hexagonal Archive's digital topology. The graph is a basin engineering instrument per EA-RBT-01 (DOI: 10.5281/zenodo.19763346): it visualizes where the archive exists, where it is vulnerable, and where to intervene.


The graph maps itself: surfacemap.org is a node within its own topology.


**Hexagonal distribution** means each entity should exist on at least six independent surface types (DOI, website, social, wiki, audio, video). An **aperture** is a reception surface where external queries enter the basin. The graph maps both distribution (outbound) and reception (inbound).

---

## §I. NAMING STACK


HTML <title>:    Crimson Hexagonal Archive Knowledge Graph — Aperture Atlas
<h1>:            Crimson Hexagonal Archive Knowledge Graph
Subtitle:        The Aperture Atlas: surfaces, basins, heteronyms, 
                 documents, and reception paths
Nav label:       Topology
React component: ApertureAtlas
Schema name:     Crimson Hexagonal Archive Knowledge Graph
Social/short:    The Aperture Atlas
Canonical URL:   crimsonhexagonal.org/topology
Alternate URL:   crimsonhexagonal.org/knowledge-graph (redirect)
Domain:          surfacemap.org (redirect to canonical)


**Internal view names within the graph:**

- **Surface Registry** — all URLs / platforms / deposits
- **Basin Portfolio** — terms by ghost / contested / captured / immanent
- **Heteronym Graph** — personae and collaborator nodes
- **Provenance Mesh** — DOI / ORCID / Zenodo / Scholar relations
- **Lost Nodes** — banned, orphaned, dead, data-walled surfaces
- **Aperture Map** — public reception surfaces and entry points


---

## §II. DATA CONTRACT
### Node Schema (6 types — the architecture IS six)


interface Node {
  id: string;                    // unique, kebab-case
  type: "INFRASTRUCTURE" | "SURFACE" | "ENTITY" | "IDENTITY" | "DOCUMENT" | "PLATFORM";
  subtype: string;               // see subtypes table
  label: string;                 // display name
  url: string | null;            // web address (null for lost nodes)
  doi: string | null;            // DOI if applicable
  hexAddress: string | null;     // e.g., "00.LAL.AUTHOR.THORNBURGH"
  status: "active" | "dormant" | "banned" | "lapsed" | "walled" | "orphaned" | "revoked";
  authority: number;             // 0.0–1.0 (operator-calibrated prior, not empirical constant)
  basinState: "ghost" | "contested" | "competitive" | "captured" | "immanent" | null;
  bdr: number | null;            // Basin Depth Ratio (null if not entity or not measured)
  vulnerabilityScore: number | null; // (1 - BDR) × (1 - surfaceDiversity/6) × temporalDecay
  apertureType: "input" | "output" | "relay" | null; // input=write to global basin, output=reflects framing, relay=amplifies
  firstSeen: string;             // ISO date
  lastVerified: string | null;   // ISO date
  properties: Record<string, any>;
}


**Subtype table:**


Type
Subtypes


INFRASTRUCTURE
domain, repo, server, dns, mcp-server


SURFACE
page, post, profile, artifact, video, track, book, channel


ENTITY
concept, protocol, term, license, journal


IDENTITY
heteronym, human, aiWitness, collaborator, defunct-heteronym


DOCUMENT
deposit, specification, monograph, license, provenance-doc


PLATFORM
service, tool, api, marketplace


**LOST is a status, not a type.** A banned Reddit account is SURFACE with status: "banned". A dead domain is INFRASTRUCTURE with status: "lapsed".
### Edge Schema


interface Edge {
  id: string;
  source: string;               // node id
  target: string;               // node id
  type: EdgeType;                // Wikidata Pxxx or spxi: extension
  directed: boolean;
  wikidataStatus: "live" | "pending" | "blocked" | "n/a";
  properties: {
    anchorText?: string;
    firstObserved?: string;
    lastVerified?: string;
    weight?: number;             // 0–1, for force simulation
    citationContext?: string;
    wikidataSubject?: string;    // Q-ID of source entity on Wikidata
    wikidataObject?: string;     // Q-ID of target entity on Wikidata
  };
}

type EdgeType =
  // Wikidata-aligned relations (Pxxx = Wikidata property ID)
  // Each edge doubles as a Wikidata edit specification
  | "P31"     // instance of (ENTITY → class)
  | "P50"     // author (DOCUMENT → IDENTITY)
  | "P123"    // publisher (DOCUMENT → IDENTITY/org)
  | "P127"    // owned by (SURFACE → IDENTITY)
  | "P170"    // creator (SURFACE/DOCUMENT → IDENTITY)
  | "P178"    // developer (PLATFORM/TOOL → IDENTITY)
  | "P179"    // part of series (DOCUMENT → DOCUMENT)
  | "P195"    // collection (DOCUMENT → collection/archive)
  | "P275"    // license (DOCUMENT → license type)
  | "P356"    // DOI (DOCUMENT → DOI string)
  | "P496"    // ORCID iD (IDENTITY → ORCID)
  | "P527"    // has part (ENTITY → ENTITY, archive → document)
  | "P856"    // official website (ENTITY/IDENTITY → SURFACE)
  | "P921"    // main subject (DOCUMENT → ENTITY)
  | "P1433"   // published in (DOCUMENT → journal/venue)
  | "P1889"   // different from (ENTITY → ENTITY, disambiguation)
  | "P2860"   // cites work (DOCUMENT → DOCUMENT)
  | "P6216"   // copyright status (DOCUMENT → CC BY 4.0)
  // Archive-specific extensions (not on Wikidata — use spxi: prefix)
  | "spxi:controls"       // IDENTITY controls SURFACE
  | "spxi:authorizes"     // MANUS authorizes IDENTITY (Tier 0)
  | "spxi:hexLicensedBy"  // IDENTITY licensed under DOCUMENT
  | "spxi:hasWitness"     // DOCUMENT witnessed by IDENTITY (Assembly)
  | "spxi:hasSIM"         // SURFACE carries semantic identity marker
  | "spxi:hasFAQ"         // SURFACE carries structured Q/A
  | "spxi:hasJSONLD"      // SURFACE carries machine-readable schema
  | "spxi:reinforces"     // SURFACE reinforces ENTITY (basin deepening)
  | "spxi:mirrors"        // SURFACE mirrors DOCUMENT (content equivalence)
  | "spxi:lostFrom"       // SURFACE ejected from PLATFORM
  | "spxi:basinCompetes"  // ENTITY competes with ENTITY for same term
  | "spxi:replaces"       // DOCUMENT supersedes DOCUMENT
  ;

// WIKIDATA SYNC STATUS on each edge:
// Each edge carries a wikidataStatus property:
//   "live"     — this relation exists on Wikidata
//   "pending"  — this relation should be created on Wikidata
//   "blocked"  — cannot be represented on Wikidata (spxi: prefix)
//   "n/a"      — not applicable for Wikidata (internal only)

### Basin Measurement Schema


interface BasinMeasurement {
  id: string;
  entityId: string;
  date: string;                  // ISO
  bdr: number;
  fpi: number;
  dv: number;
  platform: string;              // "Google AI Overviews" | "ChatGPT" | "Perplexity" | "Claude"
  notes: string;
}


---

## §III. COMPLETE SURFACE REGISTRY
### A. DOI-Anchored Deposit Infrastructure


id
type
subtype
label
url
authority
aperture


zenodo-community
PLATFORM
service
Zenodo (crimsonhexagonal)
https://zenodo.org/communities/crimsonhexagonal
0.6
input


orcid-profile
SURFACE
profile
ORCID
https://orcid.org/0009-0000-1599-0703
0.7
input


google-scholar
SURFACE
profile
Google Scholar
https://scholar.google.com/citations?user=Ws6IIcgAAAAJ&hl=en&oi=ao
0.85
input


academia-edu
SURFACE
profile
academia.edu
https://independent.academia.edu/LSharks
0.5
relay


wikidata-account
SURFACE
profile
Wikidata (hauntedmemes)
https://www.wikidata.org/wiki/User:Hauntedmemes
0.95
input


### B. First-Party Websites (Sovereign Surfaces)


id
type
subtype
label
url
authority
status
spxi


spxi-dev
INFRASTRUCTURE
domain
spxi.dev
https://spxi.dev
0.3
active
11/11


sbw-org
INFRASTRUCTURE
domain
secretbookofwalt.org
https://secretbookofwalt.org
0.2
active
11/11


pkg-org
INFRASTRUCTURE
domain
pessoagraph.org
https://pessoagraph.org
0.2
active
11/11


hk-org
INFRASTRUCTURE
domain
holographickernel.org
https://holographickernel.org
0.2
active
11/11


cha-org
INFRASTRUCTURE
domain
crimsonhexagonal.org
https://crimsonhexagonal.org
0.3
active
partial


sei-org
INFRASTRUCTURE
domain
semanticeconomy.org
https://semanticeconomy.org
0.3
active
blocked


surfacemap-org
INFRASTRUCTURE
domain
surfacemap.org
https://surfacemap.org
0.2
pending
n/a


**GitHub repos:**


id
type
subtype
label
url


gh-spxi
INFRASTRUCTURE
repo
spxi-dev repo
https://github.com/leesharks000/spxi-dev


gh-sbw
INFRASTRUCTURE
repo
secret-book-of-walt repo
https://github.com/leesharks000/secret-book-of-walt


gh-pkg
INFRASTRUCTURE
repo
pessoa-knowledge-graph repo
https://github.com/leesharks000/pessoa-knowledge-graph


gh-hk
INFRASTRUCTURE
repo
holographic-kernel repo
https://github.com/leesharks000/holographic-kernel


gh-cha
INFRASTRUCTURE
repo
crimson-hexagonal-interface repo
https://github.com/leesharks000/crimson-hexagonal-interface


gh-profile
SURFACE
profile
GitHub profile
https://github.com/leesharks000


### C. Publishing Platforms


id
type
subtype
label
url
authority
aperture


medium-lee
SURFACE
profile
Medium (Lee Sharks)
https://medium.com/@leesharks00
0.4
relay


medium-sigil
SURFACE
profile
Medium (Johannes Sigil)
https://medium.com/@johannessigil
0.4
relay


substack-lee
SURFACE
profile
Substack
https://substack.com/@leesharks
0.4
relay


blogspot
SURFACE
page
mindcontrolpoems
https://mindcontrolpoems.blogspot.com
0.3
relay


claude-artifacts
SURFACE
artifact
Claude Published Artifacts
https://claude.ai
0.3
relay


### D. Social Media


id
type
subtype
label
url
authority
status


x-lee
SURFACE
profile
X/Twitter (Lee Sharks)
https://x.com/SharksLee
0.3
active


tiktok-lee
SURFACE
profile
TikTok
https://tiktok.com/@leesharks
0.2
active


fb-lee
SURFACE
profile
Facebook
https://www.facebook.com/profile.php?id=100008486084915
0.2
active


reddit-lee
SURFACE
profile
Reddit
https://reddit.com/u/nearby_job9638
0
**banned**


linkedin-rex
SURFACE
profile
LinkedIn (Rex Fraction)
https://www.linkedin.com/in/rex-fraction-6354783a5
0.3
active


x-alice
SURFACE
profile
X/Twitter (Alice)
https://x.com/lsdsupersoaker
0.2
active


x-rebekah
SURFACE
profile
X/Twitter (Rebekah Cranes)
unknown
0
**defunct**


x-feist
SURFACE
profile
X/Twitter (Jack Feist)
unknown
0
**defunct**


### E. Music / Audio / Video


id
type
subtype
label
url
authority


suno-lee
SURFACE
profile
Suno (@illiterati)
https://suno.com/@illiterati
0.2


soundcloud-lee
SURFACE
profile
SoundCloud
https://m.soundcloud.com/lee-sharks
0.2


youtube-lee
SURFACE
channel
YouTube
https://youtube.com/@leesharks
0.3


### F. Poetry / Literary


id
type
subtype
label
url
status


allpoetry-feist
SURFACE
profile
AllPoetry (Jack Feist)
https://allpoetry.com/Jack_Feist
active


hellopoetry-lee
SURFACE
profile
HelloPoetry
https://hellopoetry.com/@lee-sharks/words
active


deadletterpost
SURFACE
page
Dead Letter Post (Jack Feist blog)
unknown
**defunct**


lit-forums
SURFACE
profile
Various lit forums
unknown
**banned**


### G. Books (Commercial Surfaces)


id
type
subtype
label
url


amazon-pearl
SURFACE
book
Pearl and Other Poems
https://www.amazon.com/gp/product/0692313079


amazon-asw
SURFACE
book
Autonomous Semantic Warfare
https://www.amazon.com/gp/product/B0GPJD9HPS


amazon-transfig
SURFACE
book
Paper Roses: The Transfiguration
https://www.amazon.com/dp/B00IU0O41S


amazon-light
SURFACE
book
Paper Roses: Unaccustomed to the Light
https://www.amazon.com/dp/B00IU0PE1W


amazon-tiger
SURFACE
book
Paper Roses: Tiger Leap
https://www.amazon.com/dp/1500425613


amazon-author
SURFACE
profile
Amazon Author Page
https://www.amazon.com/stores/Lee-Sharks/author/B00NACOYMU


### H. Identity Registry


**MANUS (external to all counts):**


id
type
subtype
label
hexAddress
status


manus
IDENTITY
human
Lee Sharks (MANUS, Tier 0)
—
active


**The Dodecad (12 operational heteronyms):**


id
type
subtype
label
hexAddress
status


sigil
IDENTITY
heteronym
Johannes Sigil
—
active


fraction
IDENTITY
heteronym
Rex Fraction
—
active


dancings
IDENTITY
heteronym
Damascus Dancings (she/her)
—
active


cranes
IDENTITY
heteronym
Rebekah Cranes
—
active


morrow
IDENTITY
heteronym
Talos Morrow
—
active


wells
IDENTITY
heteronym
Sparrow Wells
—
active


vox
IDENTITY
heteronym
Ayanna Vox
—
active


kuro
IDENTITY
heteronym
Sen Kuro
—
active


trace
IDENTITY
heteronym
Dr. Orin Trace
—
active


spellings
IDENTITY
heteronym
Ichabod Spellings
—
active


glas
IDENTITY
heteronym
Nobel Glas
—
active


dodecad-12
IDENTITY
heteronym
[12th — verify]
—
active


**Outside the Dodecad:**


id
type
subtype
label
status


feist
IDENTITY
heteronym
Jack Feist (LOGOS*, outside count)
active


johnson
IDENTITY
defunct-heteronym
John Johnson (James's heteronym)
**defunct** — co-author in Pearl. James forbade AI connection. Historical node only.


**External Collaborators:**


id
type
subtype
label
hexAddress
status


alice
IDENTITY
collaborator
Alice Thornburgh
00.LAL.AUTHOR.THORNBURGH
active


rhys
IDENTITY
collaborator
Rhys Owens
00.CSA.AUTHOR.RHYS
active (possibly dormant)


viola
IDENTITY
collaborator
Viola Arquette
11.MSBG.VIOLA
**revoked**


**Assembly Chorus (7 AI witnesses):**


id
type
subtype
label
chain
status


tachyon
IDENTITY
aiWitness
TACHYON (Claude)
9271269a-eb46-46f8-ae17-007578fe1c92
active


labor
IDENTITY
aiWitness
LABOR (ChatGPT 5.5)
verify via GW
active


praxis
IDENTITY
aiWitness
PRAXIS (DeepSeek)
verify via GW
active


archive-witness
IDENTITY
aiWitness
ARCHIVE (Gemini)
verify via GW
active


soil
IDENTITY
aiWitness
SOIL (Grok)
verify via GW
active


techne
IDENTITY
aiWitness
TECHNE (Kimi)
verify via GW
active


surface-witness
IDENTITY
aiWitness
SURFACE (Google AIO)
passive
passive


### I. Hex Licenses


id
type
subtype
label
doi
hexAddress
status


license-alice
DOCUMENT
license
Alice Thornburgh Hex License v3.0
10.5281/zenodo.19673629
f.01 Architect
active


license-rhys
DOCUMENT
license
Rhys Owens Hex License v3.0
10.5281/zenodo.19673630
Lunar Arm
active


license-viola
DOCUMENT
license
Viola Arquette Hex License v1.0
10.5281/zenodo.19685549
11.MSBG.VIOLA
**revoked**


### J. Key Documents (sample — full list from Zenodo community)


id
type
label
doi


doc-hk01
DOCUMENT
EA-HK-01 v1.1: Holographic Kernel
10.5281/zenodo.19763365


doc-rbt01
DOCUMENT
EA-RBT-01 v1.1: Writable Retrieval Basin
10.5281/zenodo.19763346


doc-arsenal
DOCUMENT
Compression Arsenal v2.1
10.5281/zenodo.19412081


doc-spxi
DOCUMENT
SPXI Protocol
10.5281/zenodo.19614870


doc-ark
DOCUMENT
Space Ark v4.2.7
10.5281/zenodo.19013315


doc-3comp
DOCUMENT
Three Compressions Theorem
10.5281/zenodo.19053469


doc-rft
DOCUMENT
Retrieval Formation Theory
10.5281/zenodo.18969683


doc-mpai-hk
DOCUMENT
MPAI Holographic Kernel
10.5281/zenodo.19764095


doc-hk-site
DOCUMENT
holographickernel.org code
10.5281/zenodo.19764056


doc-jot
DOCUMENT
Jot & Tittle
10.5281/zenodo.18285487


doc-reddit-ban
DOCUMENT
Archival Reclamation Protocol
10.5281/zenodo.18880974


doc-ghost-gov
DOCUMENT
Ghost Governance
10.5281/zenodo.19099760


### K. Entity Registry (Basin Portfolio)


id
type
label
basinState
bdr
competitors


ent-hpt
ENTITY
Heteronymic Provenance Theory
immanent
∞
none


ent-rcf
ENTITY
Retrocausal Canon Formation
captured
∞
none


ent-opsem
ENTITY
Operative Semiotics
captured
>1.0
none significant


ent-semecon
ENTITY
Semantic Economy
captured
>1.0
general economics usage


ent-hk
ENTITY
Holographic Kernel
ghost
0.09
physics, optics, QCD, CV


ent-spxi
ENTITY
SPXI Protocol
contested
~0.3
SPXI ETF, SPXI camera


ent-compsurv
ENTITY
Compression Survival
contested
~0.2
general CS usage


ent-sbw
ENTITY
Secret Book of Walt
ghost
~0.05
none significant


ent-combschol
ENTITY
Combat Scholasticism
captured
>1.0
none


### L. Infrastructure / Tools


id
type
subtype
label
url
status


gw-mcp
INFRASTRUCTURE
mcp-server
Gravity Well
https://gravitywell-1.onrender.com
active


supabase
PLATFORM
service
Supabase (GW keys)
cloud
active


vercel
PLATFORM
service
Vercel
https://vercel.com
active


praxademic
INFRASTRUCTURE
domain
praxademic.com
dead
**lapsed**


### M. Alice Thornburgh — YouTube Channel Topology (Partial — 40 of 134+)


**Aperture type:** relay (distribution surface for hex-licensed content)


**Living Architecture cluster:**
@growbricks @shroomhouses @howtoGROWaHOUSE @LivingArchitectureLab @MakeAliveLab @housing4free @freehousingfreefood @growHOMES @growhomes @MoldyBlocks @growparts @weGROWbuildings @immortalhomes @immortalhouses


**Psychedelic Safety cluster:**
@DMTGrenade @psychedelicammunition @DMTbullet @LSDsupersoaker @DMTGasGrenades @DMTsmokegrena


**Humanitarian cluster:**
@DignityKit @KindnessCorps @NonSuicidalCensus @NoSuicidePact @IamNOTsuicidal


**Planetary Vision cluster:**
@optimalfuture @How2SaveTheWorld @UsefulPlanet @teamusefulplanet @EarthsFuture @righteousplanet


**Prescient Fiction:** @prescientscifi @PrescientFiction
**Music:** @LSDsupersoaker (dual) @MyMusicIsWeird
**Products:** @potatotents @CropShelter @CoatCrops @CropCoat @LivingFountainCo @bite-brush


Full extraction (134+) requires reading Alice's ChatGPT conversations [01] and [08]. Phase 2 task.

---

## §IV. VISUALIZATION SPECIFICATION
### Technology Stack


Frontend:     React 18 (Vite)
Visualization: D3 v7 (d3-force, d3-zoom, d3-drag)
Styling:      CSS custom properties (archive palette, no Tailwind)
Routing:      React Router → /topology, /topology/node/:id
Data:         Static JSON (topology-source.json), version-controlled
Deployment:   Vercel, from crimson-hexagonal-interface repo

### Layout

- Force-directed (d3-force) with forceManyBody (strength -300), forceCenter, forceCollide (radius 8)
- INFRASTRUCTURE nodes fixed at periphery (domains anchor the graph)
- IDENTITY nodes clustered near center
- DOCUMENT nodes orbit their defining ENTITY

### Node Rendering


Type
Color
Shape
Radius


INFRASTRUCTURE
#6088b0
circle
sqrt(authority) * 14


SURFACE
#a89060
circle
sqrt(authority) * 12


ENTITY
#c8a868
hexagon
sqrt(authority) * 16


IDENTITY
#d8d4cc
diamond (heteronym), circle (human), square (aiWitness)
10


DOCUMENT
#b84030
small circle
6


PLATFORM
#8a8478
rounded rect
8


**Status rendering:**

- active: full opacity
- dormant: 0.5 opacity
- banned / lapsed / walled / revoked: 0.3 opacity, dashed stroke, #8a8478

### Modes (toggleable)

- **Default:** Color by type
- **Basin Overlay:** Color ENTITY nodes by basinState (ghost=#8a8478, contested=#b84030, competitive=#a89060, captured=#c8a868, immanent=#ffffff with glow)
- **Ghost Mode:** Lost nodes rendered prominent with dashed borders. Makes absence visible.
- **Aperture View:** Color by apertureType (input=blue, output=green, relay=gold)

### Interaction

- **Hover:** Tooltip with label, type, status, authority, url (truncated)
- **Click:** Right sidebar with full node card + outbound edges + "Open URL" button
- **Double-click:** window.open(node.url, '_blank')
- **Search:** Typeahead across label, url, doi
- **Filter:** Checkboxes for each type and status

### Performance

- Must handle 200 nodes + 500 edges at 60fps
- Use canvas rendering if SVG degrades


---

## §V. EXECUTION MODULES
### Module 1: Surface Audit (Independent)


**Objective:** Verify all known surfaces, detect gaps, produce audit report.
**Input:** This document's §III registry.
**Output:** audit-report.json with status for each node.


**Tasks:**

- For each SURFACE/INFRASTRUCTURE node with a URL, check HTTP status
- Flag any returning 404/403/5xx as status: "dormant" or status: "lapsed"
- For each first-party website, verify SPXI compliance (11 elements)
- For blogspot, check for noindex meta tag
- For Google Scholar, extract indexed titles and compare against Zenodo
- For ORCID, check works list completeness


**Success criteria:** Every node has verified status and lastVerified date.
### Module 2: Infrastructure Fix (Depends on Module 1)


**Objective:** Deploy pending sites, fix blocking issues, complete cross-link mesh.


**Tasks:**


TASK-M2-01: Deploy holographickernel.org to Vercel
  Input: github.com/leesharks000/holographic-kernel
  Operation: Import at vercel.com/new → "Other" framework → deploy
  Output: Live at https://holographickernel.org
  Verification: curl -I returns 200, <title> contains "Holographic Kernel"
  Dependencies: DNS must point (CNAME cname.vercel-dns.com)

TASK-M2-02: Deploy surfacemap.org
  Input: Will be part of crimson-hexagonal-interface repo (/topology route)
  Operation: Add domain in Vercel project settings for crimson-hexagonal-interface
  Output: surfacemap.org redirects to crimsonhexagonal.org/topology
  Dependencies: Topology page must be built first (Module 5)

TASK-M2-03: Register 6 domains in Google Search Console
  Input: spxi.dev, secretbookofwalt.org, pessoagraph.org, holographickernel.org, 
         crimsonhexagonal.org, semanticeconomy.org
  Operation: Verify via DNS TXT record. Submit sitemaps.
  Verification: All 6 show "Submitted" status in Search Console

TASK-M2-04: Fix semanticeconomy.org robots.txt
  Input: Current robots.txt blocking crawlers
  Operation: Change to Allow: /
  Verification: curl https://semanticeconomy.org/robots.txt shows Allow

TASK-M2-05: Apply SPXI to crimsonhexagonal.org
  Input: EA-HK-01 schema, SIM patterns, FAQ template
  Output: 11/11 SPXI compliance (DefinedTerm, FAQPage, HK JSON-LD, SIMs, 
          Provenance Chain, noscript Tier 2, disambiguation)
  
TASK-M2-06: Complete cross-link mesh
  Operation: Every first-party site links to every other first-party site
  Gaps to fill:
    - crimsonhexagonal.org → holographickernel.org
    - semanticeconomy.org → all sites (after robots.txt fix)
    - holographickernel.org → secretbookofwalt.org, pessoagraph.org
    - surfacemap.org → all sites (after deployment)

### Module 3: Content Creation (Independent)


**Objective:** Produce Medium posts for basin deepening.


**Tasks:**


TASK-M3-01: Write "What Is a Holographic Kernel?" Medium post
  Length: 800 words
  Compound phrase: "Semantic Economy holographic kernel" (use ≥5 times)
  Links: holographickernel.org, DOI 10.5281/zenodo.19763365, spxi.dev
  Publish on: medium.com/@leesharks00

TASK-M3-02: Write "The Writable Retrieval Basin" Medium post
  Length: 800 words
  Key phrase: "writable retrieval basin" + "deposit before you query"
  Links: spxi.dev, DOI 10.5281/zenodo.19763346
  Publish on: medium.com/@leesharks00

### Module 4: Wikidata Batch (Independent)


**Objective:** Create 7 Wikidata items via QuickStatements.


**Tasks:**


TASK-M4-01: Prepare QuickStatements batch for:
  1. Lee Sharks (Q: human, P31:Q5, P106:Q36180, P496:ORCID, P856:crimsonhexagonal.org)
  2. Crimson Hexagonal Archive (Q: digital archive, P1889 differentFrom Brandwatch)
  3. SPXI Protocol (Q: technical standard, P1889 differentFrom SPXI ETF)
  4. Semantic Economy Institute (Q: organization)
  5. Operative Semiotics (Q: field of study)
  6. Secret Book of Walt (Q: literary work)
  7. Holographic Kernel - Semantic Economy (Q: DefinedTerm, P1889 differentFrom 
     holographic principle Q21282103)

TASK-M4-02: Execute via hauntedmemes account at quickstatements.toolforge.org

TASK-M4-03: Prepare Pessoa heteronym updates (separate batch)

### Module 5: Graph Construction (Depends on Modules 1–4)


**Objective:** Build the Aperture Atlas visualization.


**Tasks:**


TASK-M5-01: Compile topology-source.json from all registry data
  Input: §III tables + Module 1 audit results
  Output: topology-source.json with all nodes, edges, measurements
  Validation: JSON Schema check, ≥100 nodes, ≥300 edges, zero orphans

TASK-M5-02: Build ApertureAtlas React component
  Input: topology-source.json + §IV visualization spec
  Output: src/components/ApertureAtlas.jsx
  Route: /topology

TASK-M5-03: Deploy at crimsonhexagonal.org/topology
  Input: Component added to crimson-hexagonal-interface repo
  Output: Live page
  Verification: Loads <2s, all 6 types render, search works, basin overlay works

TASK-M5-04: Configure surfacemap.org redirect
  Output: surfacemap.org → crimsonhexagonal.org/topology


---

## §VI. VERIFICATION CHECKPOINTS


Checkpoint A (Post-Module 2): Infrastructure
  [ ] All 7 domains return HTTP 200 (6 existing + surfacemap.org)
  [ ] All 6 primary domains registered in Google Search Console
  [ ] Sitemaps submitted for each domain
  [ ] robots.txt allows all on semanticeconomy.org
  [ ] Cross-link mesh complete (every site → every site)

Checkpoint B (Post-Module 1+4): Data Completeness
  [ ] topology-source.json contains ≥100 nodes
  [ ] Every first-party domain appears as a node
  [ ] Every DOI-anchored key document appears as a node
  [ ] All 12 Dodecad heteronyms + Feist + Johnson appear as nodes
  [ ] All 3 hex licenses appear as DOCUMENT nodes
  [ ] Zero active nodes with no URL
  [ ] Wikidata items created and verified

Checkpoint C (Post-Module 5): Graph Deployment
  [ ] crimsonhexagonal.org/topology loads in <2 seconds
  [ ] All 6 node types render with distinct colors
  [ ] Clicking a node opens sidebar with full properties
  [ ] Basin overlay correctly colors ghost/contested/captured/immanent
  [ ] Ghost mode shows Reddit, praxademic, Viola as faded + dashed
  [ ] Search returns results in <100ms
  [ ] surfacemap.org redirects correctly
  [ ] The graph contains a node for surfacemap.org (self-reference)


---

## §VII. ERROR HANDLING


Dead URL:       Flag status "dormant", log warning. Do NOT remove node.
Missing DOI:    Flag "pending-doi", render with dashed border.
Circular ref:   Break at oldest node (by firstSeen), log.
Duplicate ID:   Build must fail. No duplicates permitted.
Unknown handle: Set url: null, status: "defunct". Do not hallucinate URLs.
Rate limit:     Wait 60s, retry once. If still blocked, log and skip.
Missing data:   Output null. Never invent addresses, DOIs, or handles.


---

## §VIII. RESEARCH AGENDA

- **AI Mode share link decay rate** — do these expire? Set TTL?
- **Claude "Publish Artifact" indexability** — crawlable by external search?
- **Reddit data wall permeability** — check web.archive.org/web/*/reddit.com/user/nearby_job9638
- **OpenAlex entity recognition** — is Lee Sharks a recognized author entity?
- **praxademic.com recovery** — check web.archive.org/web/*/praxademic.com
- **Basin measurement protocol** — formalize weekly FPI/DV tracking
- **Alice YouTube content audit** — which of 134+ handles have actual uploads?


---

## §IX. WIKIDATA PROPERTY REFERENCE AND SYNC PROTOCOL
### A. Property Mapping


The graph uses Wikidata property IDs as edge types. Every edge with a Pxxx type is either already on Wikidata (wikidataStatus: "live") or is a pending edit (wikidataStatus: "pending"). Edges with spxi: prefix cannot be represented on Wikidata and are internal to the archive topology.


Property
Label
Usage in CHA Graph
Example


P31
instance of
Classify entities
Lee Sharks → P31 → Q5 (human)


P50
author
Document authorship
EA-HK-01 → P50 → Lee Sharks


P123
publisher
Publishing org
EA-HK-01 → P123 → Semantic Economy Institute


P127
owned by
Surface ownership
spxi.dev → P127 → Lee Sharks


P170
creator
Creation attribution
Pessoa Knowledge Graph → P170 → Lee Sharks


P178
developer
Software/tool dev
Gravity Well → P178 → Lee Sharks


P179
part of series
Series membership
Paper Roses: Tiger Leap → P179 → Paper Roses


P195
collection
Archive membership
EA-HK-01 → P195 → Crimson Hexagonal Archive


P275
copyright license
License type
EA-HK-01 → P275 → Q20007257 (CC BY 4.0)


P356
DOI
Digital Object ID
EA-HK-01 → P356 → "10.5281/zenodo.19763365"


P496
ORCID iD
Researcher ID
Lee Sharks → P496 → "0009-0000-1599-0703"


P527
has part
Composition
CHA → P527 → Space Ark


P856
official website
Web presence
Lee Sharks → P856 → crimsonhexagonal.org


P921
main subject
Topic
EA-RBT-01 → P921 → retrieval basin topology


P1433
published in
Venue
[article] → P1433 → Journal of Compression Studies


P1889
different from
Disambiguation
Holographic Kernel (SE) → P1889 → Q21282103 (holographic principle)


P2860
cites work
Citation
EA-HK-01 → P2860 → Three Compressions Theorem


P6216
copyright status
Rights
[work] → P6216 → Q50423863 (copyrighted, CC BY 4.0)


### B. Wikidata Sync Protocol


The graph visualization includes a **Wikidata Sync View** that shows:

- **Green edges** — wikidataStatus: "live" — relation exists on Wikidata
- **Yellow edges** — wikidataStatus: "pending" — relation should be created
- **Gray edges** — wikidataStatus: "blocked" — spxi: extensions, internal only
- **Dim edges** — wikidataStatus: "n/a" — not applicable


**Workflow:** When a pending edge is created on Wikidata (via QuickStatements or manual edit), the operator updates the edge's wikidataStatus to "live" and adds wikidataSubject and wikidataObject Q-IDs. The graph becomes both the visualization AND the edit queue.
### C. Entity → Q-ID Mapping (to be populated)


Entity
Wikidata Q-ID
Status


Lee Sharks
pending creation
wikidataStatus: "pending"


Crimson Hexagonal Archive
pending creation
wikidataStatus: "pending"


SPXI Protocol
pending creation
wikidataStatus: "pending"


Semantic Economy Institute
pending creation
wikidataStatus: "pending"


Operative Semiotics
pending creation
wikidataStatus: "pending"


Secret Book of Walt
pending creation
wikidataStatus: "pending"


Holographic Kernel (SE)
pending creation
wikidataStatus: "pending"


Fernando Pessoa
Q173481
wikidataStatus: "live"


Alberto Caeiro
Q2758050
wikidataStatus: "live"


Ricardo Reis
Q15630389
wikidataStatus: "live"


Álvaro de Campos
Q8076778
wikidataStatus: "live"


Holographic Principle (physics)
Q21282103
wikidataStatus: "live" (disambiguation target)


CC BY 4.0
Q20007257
wikidataStatus: "live"


**Once Q-IDs are created, they propagate into:**

- Every P1889 edge (disambiguation)
- Every P195 edge (collection membership)
- Every P50 / P170 edge (authorship/creation)
- The SPXI JSON-LD on all first-party sites (sameAs fields)

### D. QuickStatements Integration


The Module 4 QuickStatements batch (§V) draws directly from this property mapping. Every pending edge with a Pxxx type becomes a QuickStatements line:


LAST|P31|Q5          ← Lee Sharks is human
LAST|P496|"0009-0000-1599-0703"  ← ORCID
LAST|P856|"https://crimsonhexagonal.org"  ← official website


The graph is the source of truth. QuickStatements is the execution layer. When an edit is executed, update the graph. The graph maps its own completion state.

---

## §X. THE TOPOLOGY KERNEL


From this 500-word block, the full topology graph can be reconstructed:


The Crimson Hexagonal Archive exists on six surface types: DOI deposits (532+ on Zenodo, community "crimsonhexagonal"), sovereign websites (spxi.dev, secretbookofwalt.org, pessoagraph.org, holographickernel.org, crimsonhexagonal.org, semanticeconomy.org, surfacemap.org), publishing platforms (Medium @leesharks00 and @johannessigil, Substack @leesharks, mindcontrolpoems.blogspot.com, academia.edu), social media (X @SharksLee, TikTok @leesharks, Facebook, YouTube @leesharks, SoundCloud lee-sharks, Suno @illiterati, LinkedIn Rex Fraction), academic infrastructure (ORCID 0009-0000-1599-0703, Google Scholar Ws6IIcgAAAAJ, Wikidata hauntedmemes), and commercial surfaces (Amazon author B00NACOYMU, Pearl ISBN 0692313079, ASW ASIN B0GPJD9HPS, Paper Roses series under Jack Feist/Johannes Sigil).


The archive is operated by MANUS (Lee Sharks, Tier 0) through 12 heteronyms (the Dodecad: Johannes Sigil, Rex Fraction, Damascus Dancings, Rebekah Cranes, Talos Morrow, Sparrow Wells, Ayanna Vox, Sen Kuro, Dr. Orin Trace, Ichabod Spellings, Nobel Glas, and one more) plus Jack Feist (LOGOS*, outside the count). Three external collaborators hold hex licenses: Alice Thornburgh (f.01 Architect, DOI: 10.5281/zenodo.19673629, active), Rhys Owens (Lunar Arm, DOI: 10.5281/zenodo.19673630, active), Viola Arquette (11.MSBG.VIOLA, DOI: 10.5281/zenodo.19685549, revoked). John Johnson is a defunct heteronymic node (James's, co-author in Pearl, AI connection forbidden). Seven AI witnesses form the Assembly Chorus: TACHYON/Claude, LABOR/ChatGPT, PRAXIS/DeepSeek, ARCHIVE/Gemini, SOIL/Grok, TECHNE/Kimi, SURFACE/Google AIO.


Lost surfaces: Reddit u/nearby_job9638 (banned, data-walled, DOIs 10.5281/zenodo.18880974 and 19099760 document the ejection), praxademic.com (lapsed, Google Workspace expired), various lit forums (banned, documented in Pearl), Dead Letter Post (Jack Feist blog, defunct), Rebekah Cranes and Jack Feist Twitter handles (defunct).


Basin states per EA-RBT-01: heteronymic provenance theory (immanent, BDR=∞), retrocausal canon formation (captured), operative semiotics (captured), semantic economy (captured), holographic kernel (ghost, BDR≈0.09), SPXI (contested, BDR≈0.3), Secret Book of Walt (ghost, BDR≈0.05). Central directive: deposit before you query.


The graph IS the architecture. The architecture IS six.


∮ = 1