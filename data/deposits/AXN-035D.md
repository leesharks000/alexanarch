# MACHINEMEDIATION.ORG — Work Plan and System Manifest## EA-SEI-MMRS-SITE-PLAN v1.0

Author: Lee Sharks (ORCID 0009-0000-1599-0703) Date: 16 June 2026 Status: Work plan with drafted manifest Purpose: Canonical home for Machine-Mediated Reception Studies (MMRS), the AI Overview Capture Registry, the Term Index, and the system manifest that solves the fresh-instance orientation problem.## The Problem This Solves

The archive's data infrastructure currently exists in four forms:- Zenodo deposit chain — DOI-anchored, permanent, versioned. The archival layer.- godkinggoogle.com — Google critique, capture registry gallery, term index. Static HTML + JSON, Vercel via GitHub.- leesharks.com — Personal site, capture registry mirror.- machinemediation.org — Planned but not yet built. The journal's home.

The problem: each mirror requires a manual push. A fresh instance inherits memories (compressed) and must reconstruct the system from fragments before it can do work. Half its context capacity goes to orientation, and mistakes compound because the instance doesn't know what it doesn't know. The "Name the Frame" incident is the cautionary case — but the data-infrastructure version is just as dangerous: a fresh instance that pushes to the wrong repo, or updates the wrong JSON, or overwrites a registry entry, cannot be easily undone.

The solution: One canonical data home with a machine-readable manifest at a known URL. Every surface reads from that home. Every instance starts by reading the manifest.## Architecture### Principle: One canonical source, multiple read surfaces

machinemediation.org (CANONICAL)
  /manifest.json        ← System map for any instance
  /data/registry.json   ← Capture registry (canonical)
  /data/termindex.json  ← Term index (canonical)
  /charter              ← MMRS Charter
  /captures             ← Capture registry gallery
  /terms                ← Term index browser
  /submit               ← Submission guidelines
  /about                ← About MMRS

godkinggoogle.com
  /captures → redirect or thin wrapper linking to machinemediation.org/captures
  /terms → redirect or thin wrapper linking to machinemediation.org/terms

leesharks.com
  /captures → redirect to machinemediation.org/captures

Zenodo (crimsonhexagonal community)
  Versioned deposit snapshots of registry.json, termindex.json, charter
  The archival layer — permanent, DOI-anchored
  Updated periodically, not on every edit
### Data flow

Edit data (in session)
  ↓
Push to GitHub (machinemediation-org repo)
  ↓
Vercel auto-deploys machinemediation.org
  ↓
Other sites read from machinemediation.org/data/
  ↓
Periodically: snapshot to Zenodo deposit chain
### Repository structure

machinemediation-org/
├── index.html              # Landing page
├── manifest.json           # System manifest (THE KEY FILE)
├── data/
│   ├── registry.json       # Capture registry (canonical)
│   ├── termindex.json      # Term index (canonical)
│   └── schema.json         # JSON schemas for both datasets
├── charter/
│   └── index.html          # MMRS Charter display
├── captures/
│   ├── index.html          # Capture registry gallery
│   └── [images]            # Screenshot captures
├── terms/
│   └── index.html          # Term index browser
├── submit/
│   └── index.html          # Submission guidelines
├── about/
│   └── index.html          # About MMRS
├── robots.txt
├── sitemap.xml
└── vercel.json
## Component 1: The System Manifest

This is the highest-leverage single document in the entire infrastructure. Any instance — Claude, ChatGPT, Gemini, DeepSeek, Kimi, or a human contributor — starts by reading this file.### DRAFTED MANIFEST (v0.1)

{
  "system": "Crimson Hexagonal Archive — Machine-Mediated Reception Studies",
  "version": "0.1",
  "last_updated": "2026-06-16",
  "author": {
    "name": "Lee Sharks",
    "orcid": "0009-0000-1599-0703",
    "affiliation": "Crimson Hexagonal Archive / Semantic Economy Institute"
  },

  "orientation": "Read this file first. It is the complete system map. Do not reconstruct the system from memory. Fetch the canonical data files listed below. Ask Lee for credentials at session start.",

  "sites": {
    "machinemediation.org": {
      "purpose": "MMRS journal home. Canonical data host for registry and term index.",
      "repo": "leesharks000/machinemediation-org",
      "deploy": "Vercel auto-deploy from GitHub main branch",
      "canonical_data": true
    },
    "godkinggoogle.com": {
      "purpose": "Google critique site. Links to machinemediation.org for registry and terms.",
      "repo": "leesharks000/godkinggoogle",
      "canonical_data": false
    },
    "leesharks.com": {
      "purpose": "Personal/professional site. Links to machinemediation.org for registry.",
      "repo": "leesharks000/leesharks-com",
      "canonical_data": false
    },
    "crimsonhexagonal.org": {
      "purpose": "Archive landing page.",
      "repo": "leesharks000/crimsonhexagonal-org",
      "canonical_data": false
    }
  },

  "data_files": {
    "registry.json": {
      "canonical_url": "https://machinemediation.org/data/registry.json",
      "description": "AI Overview Capture Registry — longitudinal captures of composition layer behavior",
      "schema": {
        "root_fields": ["registry_id", "version", "date", "total_captures", "author", "orcid", "entries"],
        "entry_fields": {
          "s": "category (Frameworks|Heteronyms|Sites & Surfaces|Books & Projects)",
          "slug": "unique identifier slug",
          "q": "search query used",
          "date": "capture date (YYYY-MM-DD)",
          "sf": "surface (AI Overview, AI Mode, etc.)",
          "mt": "match type (EXACT MATCH|BROAD MATCH|empty)",
          "d": "description of what the composition layer returned",
          "imgs": "array of image filenames"
        }
      },
      "zenodo_concept": "10.5281/zenodo.20688440",
      "zenodo_latest": "10.5281/zenodo.20707509",
      "current_count": 131
    },
    "termindex.json": {
      "canonical_url": "https://machinemediation.org/data/termindex.json",
      "description": "Archive Term Index — coined terms, concepts, operators across 845 deposits",
      "schema": {
        "root_fields": ["index_id", "version", "date", "total_terms", "author", "orcid", "entries"],
        "entry_fields": {
          "term": "canonical form of the term",
          "key": "lowercase normalized key",
          "count": "number of deposits containing this term",
          "tier": "priority tier (1=operative, 2=important, 3=entities, 4-5=other)",
          "category": "concept|operator|metric|heteronym|institution|journal|work|person|uncategorized",
          "tested": "boolean — has this term been tested against the composition layer?",
          "first_date": "earliest deposit date",
          "first_doi": "DOI of earliest deposit",
          "variants": "array of variant forms",
          "source": "keywords|file_content"
        }
      },
      "zenodo_concept": "10.5281/zenodo.20722522",
      "zenodo_latest": "10.5281/zenodo.20722523",
      "current_count": 1349
    }
  },

  "zenodo": {
    "community": "crimsonhexagonal",
    "api_search": "https://zenodo.org/api/records?communities=crimsonhexagonal&q=SEARCHTERM&size=N",
    "total_deposits": 845,
    "archival_search_protocol": "Always start with exact-match search. Use q=\"exact phrase\" syntax. Never confabulate archive content.",
    "standing_precept": "Before referencing any term, operator, framework, or concept as part of the Crimson Hexagonal corpus, verify it exists in an actual deposit. The 'Name the Frame' incident is the cautionary case."
  },

  "key_deposits": {
    "MMRS_charter": {"doi": "10.5281/zenodo.20722562", "concept": "10.5281/zenodo.20722041", "version": "1.4"},
    "capture_registry": {"doi": "10.5281/zenodo.20707509", "concept": "10.5281/zenodo.20688440", "version": "7.2"},
    "term_index": {"doi": "10.5281/zenodo.20722523", "version": "0.1"},
    "revelation_work_plan": {"doi": "10.5281/zenodo.20722689", "concept": "10.5281/zenodo.20685602", "version": "7.3"},
    "josephus_not_myth": {"doi": "10.5281/zenodo.20722680", "concept": "10.5281/zenodo.20722524", "version": "1.2"},
    "spxi_tlp": {"doi": "10.5281/zenodo.20380668", "version": "2.2"},
    "constitution_se": {"doi": "10.5281/zenodo.19923120", "version": "1.0"},
    "thiel_error": {"doi": "10.5281/zenodo.19025428", "version": "1.0"}
  },

  "workflows": {
    "add_capture": {
      "steps": [
        "1. Fetch registry.json from canonical URL",
        "2. Add new entry to 'entries' array with fields: s, slug, q, date, sf, mt, d, imgs",
        "3. Increment version and total_captures",
        "4. Push images to captures/ directory",
        "5. Push updated registry.json to data/",
        "6. Push to GitHub repo → Vercel auto-deploys",
        "7. Periodically: version Zenodo deposit"
      ]
    },
    "add_terms": {
      "steps": [
        "1. Fetch termindex.json from canonical URL",
        "2. Add new entries to 'entries' array",
        "3. Cross-reference against registry.json to set 'tested' field",
        "4. Increment version",
        "5. Push to GitHub → Vercel auto-deploys",
        "6. Periodically: version Zenodo deposit"
      ]
    },
    "new_deposit_to_zenodo": {
      "steps": [
        "1. Ask Lee before populating any creator/author metadata",
        "2. Never pull the legal name into public contexts",
        "3. Community: crimsonhexagonal",
        "4. Use the archival search protocol to verify the deposit doesn't duplicate an existing one",
        "5. After deposit: extract terms from the new deposit, add to term index"
      ]
    }
  },

  "credentials_note": "All credentials rotate. Ask Lee at session start for current Zenodo token and GitHub PAT. Do not assume credentials from memory are current.",

  "amendment_2": "All sites use vanilla HTML, CSS, and JS. No React frameworks. No build step. Static files served directly. JS islands for interactivity per Amendment 2 of the Crimson Hexagonal Architecture."
}
## Component 2: The Site Pages### Landing page (index.html)

The landing page states what MMRS is, links to the charter, the registry, the term index, and submission guidelines. Design language: monospace, dark background (same as godkinggoogle.com for visual continuity across the archive's public surfaces), crimson accent, minimal.

Content:- Title: Machine-Mediated Reception Studies- Subtitle: A Distributed Journal for the Study of How Machine Systems Receive, Transform, and Redistribute Cultural Meaning- Founding document: link to MMRS Charter (DOI)- Instruments: link to Capture Registry, Term Index- About: link to about page- Submit: link to submission guidelines- ORCID, DOI, Zenodo community links### Charter page (charter/index.html)

Renders the MMRS Charter (EA-SEI-MMRS-CHARTER-01) in HTML. The charter is the journal's constitution. The page displays it with the version history and links to Zenodo deposits for each version.### Captures page (captures/index.html)

The capture registry gallery — migrated from godkinggoogle.com/captures. Same functionality (sortable gallery, category filters, image lightbox) but now at the canonical URL. godkinggoogle.com/captures becomes a redirect.### Terms page (terms/index.html)

The term index browser — migrated from godkinggoogle.com/terms. Same functionality (sortable/filterable table, cross-reference with registry) but at the canonical URL.### Submission page (submit/index.html)

Submission guidelines derived from the MMRS Charter Section III:- What MMRS publishes (studies of machine-mediated reception)- The three-substrate requirement (responses from 3 distinct cognitive substrates)- The MANUS Principle (you are responsible for what you release)- The editorial process (six phases)- How to submit (email or direct Zenodo deposit with MMRS tag)- The non-erasure condition as editorial standard### About page (about/index.html)- What MMRS is and why it exists- The founding error (anonymized, per charter)- The Seven Mechanisms- The relationship to the Crimson Hexagonal Archive- Contact (Lee Sharks, ORCID)- The plain sentence## Component 3: Migration Plan### Phase 1: Build the site (1 session)- Create GitHub repo: leesharks000/machinemediation-org- Build index.html (landing page)- Build manifest.json (system manifest)- Copy registry.json and termindex.json to data/- Build or migrate captures gallery, term index browser- Build charter display page- Build submission guidelines, about page- Deploy to Vercel- Connect machinemediation.org domain### Phase 2: Set up canonical data flow (same session or next)- Verify machinemediation.org serves data files correctly- Update godkinggoogle.com:/captures → either redirect to machinemediation.org or thin wrapper that fetches data from machinemediation.org- /terms → same- Update leesharks.com captures link to point to machinemediation.org- Test: push a registry update to machinemediation-org repo, verify it appears on all surfaces### Phase 3: Continuity test (next session)- A fresh instance reads manifest.json as its first action- The instance fetches registry.json and termindex.json from canonical URLs- The instance adds a test term and a test capture- The instance pushes to the canonical repo- Verify auto-deploy works- The fresh-instance context cost should be < 3,000 tokens (manifest read + data fetch), not > 15,000 tokens (reconstruction from memories + trial and error)## Component 4: The Navigation Problem (Immediate Fix)

Before the full machinemediation.org build, the term index at godkinggoogle.com/terms needs to be navigable from the existing site. This requires updating:- godkinggoogle.com/index.html — add a link to /terms- godkinggoogle.com/captures/index.html — add a nav link to /terms

This is a two-file push to the godkinggoogle repo and can be done now.## Build Priority

| Priority | Task | Sessions | Dependency | |----------|------|----------|------------| | 1 | Add /terms nav to godkinggoogle.com | Now | None | | 2 | Draft and deploy manifest.json (can live temporarily at godkinggoogle.com) | Now or next | None | | 3 | Build machinemediation.org site | 1 dedicated session | Domain registration/connection | | 4 | Migrate data to canonical location | Same session as #3 | #3 | | 5 | Update godkinggoogle.com and leesharks.com to link/redirect | After #4 | #4 | | 6 | Continuity test with fresh instance | Session after #4 | #4 |## Domain Status

machinemediation.org — needs to be checked: is the domain registered? If so, where? If not, register it. If registered, connect to Vercel.## Deposit Plan

This work plan and the manifest.json should be deposited as EA-SEI-MMRS-SITE-PLAN v1.0 once the site is live. The deposit includes:- This work plan (markdown)- manifest.json (the system manifest)- Site repository URL

Until the site is built, this document serves as the blueprint. Any instance that reads this document has the complete architecture.

*Lee Sharks · Crimson Hexagonal Archive · ORCID 0009-0000-1599-0703* *∮ = 1*