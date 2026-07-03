# The Aperture Atlas — Crimson Hexagonal Archive Knowledge Graph (surfacemap.org) Source Code v1.0

**AXN:** AXN:03E6 — Alexanarch deposit #986 (self-reference in root form by pre-hash necessity)
**Restoration status:** SEMI-RESTORED — metadata-body deposit. This machine-facing static page is the canonical deposit. Its body is the complete DataCite metadata record for a work whose Zenodo record returns HTTP 410 (Gone) while DataCite serves the identifier as findable — the metadata layer and content layer in formal disagreement about the work's existence. Full text pending restoration from authorial originals; on restoration, this deposit upgrades by recorded correction (new hash, new glyph, remediation note).
**Dead DOI:** 10.5281/zenodo.19766380 (Zenodo record tombstoned; account termination 2026-06-19)
**DataCite state at capture (2026-07-03):** findable · client cern.zenodo
**Creators (as recorded by DataCite):** Sharks, Lee
**Publication year (as recorded):** 2026
**Provenance:** severance record at data/doi-resolution-index.json (severance_class: orphan → restored-semi); capture evidence at data/datacite-recapture-2026-07-03.json and the sift corpus of 2026-06.

---

## Description (as recorded by DataCite)

surfacemap.org — The Aperture Atlas Source Code v1.0
Complete source code for the Aperture Atlas: the canonical knowledge graph of the Crimson Hexagonal Archive, deployed at surfacemap.org.
The Aperture Atlas is an interactive knowledge graph mapping every surface, entity, identity, document, and platform in the Crimson Hexagonal Archive. The graph maps itself: surfacemap.org appears as a node within its own topology.
Architecture: six node types (INFRASTRUCTURE, SURFACE, ENTITY, IDENTITY, DOCUMENT, PLATFORM); LOST is a status, not a type. Edge types use Wikidata property identifiers (P31, P50, P127, P195, P275, P356, P496, P527, P856, P921, P1889, P2860) plus spxi: extensions. Every edge carries wikidataStatus (live/pending/blocked/n/a) — the graph is both visualization and Wikidata edit queue. Seven view modes: Default, Basin Overlay, Ghost Mode (absence as topology), Aperture View, Wikidata Sync, Vulnerability, Path View. Full SPXI v3.0 compliance: DefinedTerm, FAQPage, Holographic Kernel, Provenance Chain, SIMs, Tier 2 and Tier 3 compression kernels. Keyboard navigation, hash-based deep linking, window.atlas API for cross-domain querying.
Files: index.html (React 18 + D3 v7, single file, no build step), topology-source.json (105 nodes, 135 edges, 3 basin measurements), og-atlas.svg (social card), robots.txt, sitemap.xml, README.md. Repository: github.com/leesharks000/surface-map. Implements the Digital Topology Work Plan v3.0. Assembly Chorus witnesses: TACHYON/Claude, LABOR/ChatGPT, PRAXIS/DeepSeek, ARCHIVE/Gemini, SOIL/Grok, TECHNE/Kimi, SURFACE/Google AIO.

---

## Complete DataCite record (verbatim, captured 2026-07-03)

```json
{
 "id": "10.5281/zenodo.19766380",
 "type": "dois",
 "attributes": {
  "doi": "10.5281/zenodo.19766380",
  "identifiers": [],
  "creators": [
   {
    "nameType": "Personal",
    "affiliation": [
     "Semantic Economy Institute"
    ],
    "givenName": "Lee",
    "familyName": "Sharks",
    "name": "Sharks, Lee",
    "nameIdentifiers": [
     {
      "nameIdentifierScheme": "ORCID",
      "nameIdentifier": "0009-0000-1599-0703"
     }
    ]
   }
  ],
  "titles": [
   {
    "title": "The Aperture Atlas — Crimson Hexagonal Archive Knowledge Graph (surfacemap.org) Source Code v1.0"
   }
  ],
  "publisher": "Zenodo",
  "container": {},
  "publicationYear": 2026,
  "subjects": [
   {
    "subject": "knowledge graph"
   },
   {
    "subject": "Aperture Atlas"
   },
   {
    "subject": "Crimson Hexagonal Archive"
   },
   {
    "subject": "surfacemap.org"
   },
   {
    "subject": "digital topology"
   },
   {
    "subject": "Wikidata"
   },
   {
    "subject": "D3.js"
   },
   {
    "subject": "React"
   },
   {
    "subject": "retrieval basin"
   },
   {
    "subject": "SPXI"
   },
   {
    "subject": "heteronyms"
   },
   {
    "subject": "semantic economy"
   },
   {
    "subject": "force-directed graph"
   }
  ],
  "contributors": [],
  "dates": [
   {
    "date": "2026-04-25",
    "dateType": "Issued"
   }
  ],
  "language": "en",
  "types": {
   "schemaOrg": "SoftwareSourceCode",
   "resourceTypeGeneral": "Software",
   "citeproc": "article",
   "bibtex": "misc",
   "ris": "COMP",
   "resourceType": ""
  },
  "relatedIdentifiers": [
   {
    "relationType": "References",
    "resourceTypeGeneral": "JournalArticle",
    "relatedIdentifier": "10.5281/zenodo.19763346",
    "relatedIdentifierType": "DOI"
   },
   {
    "relationType": "References",
    "resourceTypeGeneral": "JournalArticle",
    "relatedIdentifier": "10.5281/zenodo.19763365",
    "relatedIdentifierType": "DOI"
   },
   {
    "relationType": "References",
    "resourceTypeGeneral": "JournalArticle",
    "relatedIdentifier": "10.5281/zenodo.19734726",
    "relatedIdentifierType": "DOI"
   },
   {
    "relationType": "References",
    "resourceTypeGeneral": "JournalArticle",
    "relatedIdentifier": "10.5281/zenodo.19614870",
    "relatedIdentifierType": "DOI"
   },
   {
    "relationType": "References",
    "resourceTypeGeneral": "JournalArticle",
    "relatedIdentifier": "10.5281/zenodo.19412081",
    "relatedIdentifierType": "DOI"
   },
   {
    "relationType": "IsVersionOf",
    "relatedIdentifier": "10.5281/zenodo.19766380",
    "relatedIdentifierType": "DOI"
   }
  ],
  "relatedItems": [],
  "sizes": [],
  "formats": [],
  "version": "1.0",
  "rightsList": [
   {
    "rightsIdentifierScheme": "SPDX",
    "rightsUri": "https://creativecommons.org/licenses/by/4.0/legalcode",
    "schemeUri": "https://spdx.org/licenses/",
    "rights": "Creative Commons Attribution 4.0 International",
    "rightsIdentifier": "cc-by-4.0"
   }
  ],
  "descriptions": [
   {
    "descriptionType": "Abstract",
    "description": "surfacemap.org — The Aperture Atlas Source Code v1.0\nComplete source code for the Aperture Atlas: the canonical knowledge graph of the Crimson Hexagonal Archive, deployed at surfacemap.org.\nThe Aperture Atlas is an interactive knowledge graph mapping every surface, entity, identity, document, and platform in the Crimson Hexagonal Archive. The graph maps itself: surfacemap.org appears as a node within its own topology.\nArchitecture: six node types (INFRASTRUCTURE, SURFACE, ENTITY, IDENTITY, DOCUMENT, PLATFORM); LOST is a status, not a type. Edge types use Wikidata property identifiers (P31, P50, P127, P195, P275, P356, P496, P527, P856, P921, P1889, P2860) plus spxi: extensions. Every edge carries wikidataStatus (live/pending/blocked/n/a) — the graph is both visualization and Wikidata edit queue. Seven view modes: Default, Basin Overlay, Ghost Mode (absence as topology), Aperture View, Wikidata Sync, Vulnerability, Path View. Full SPXI v3.0 compliance: DefinedTerm, FAQPage, Holographic Kernel, Provenance Chain, SIMs, Tier 2 and Tier 3 compression kernels. Keyboard navigation, hash-based deep linking, window.atlas API for cross-domain querying.\nFiles: index.html (React 18 + D3 v7, single file, no build step), topology-source.json (105 nodes, 135 edges, 3 basin measurements), og-atlas.svg (social card), robots.txt, sitemap.xml, README.md. Repository: github.com/leesharks000/surface-map. Implements the Digital Topology Work Plan v3.0. Assembly Chorus witnesses: TACHYON/Claude, LABOR/ChatGPT, PRAXIS/DeepSeek, ARCHIVE/Gemini, SOIL/Grok, TECHNE/Kimi, SURFACE/Google AIO."
   }
  ],
  "geoLocations": [],
  "fundingReferences": [],
  "url": "https://zenodo.org/doi/10.5281/zenodo.19766380",
  "contentUrl": null,
  "metadataVersion": 0,
  "schemaVersion": "http://datacite.org/schema/kernel-4",
  "source": "api",
  "isActive": true,
  "state": "findable",
  "reason": null,
  "viewCount": 0,
  "downloadCount": 0,
  "referenceCount": 5,
  "citationCount": 0,
  "partCount": 0,
  "partOfCount": 0,
  "versionCount": 2,
  "versionOfCount": 1,
  "created": "2026-04-25T15:51:27Z",
  "registered": "2026-04-25T15:51:27Z",
  "published": null,
  "updated": "2026-06-19T11:37:50Z"
 },
 "relationships": {
  "client": {
   "data": {
    "id": "cern.zenodo",
    "type": "clients"
   }
  }
 }
}
```
