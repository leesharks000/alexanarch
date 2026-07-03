# Gravity Well Protocol v0.4.0 — Compression, Wrapping, and Anchoring Microservice for Durable Provenance Chains (EA-GW-01)

**AXN:** AXN:03CC — Alexanarch deposit #960 (self-reference in root form by pre-hash necessity)
**Restoration status:** SEMI-RESTORED — metadata-body deposit. This machine-facing static page is the canonical deposit. Its body is the complete DataCite metadata record for a work whose Zenodo record returns HTTP 410 (Gone) while DataCite serves the identifier as findable — the metadata layer and content layer in formal disagreement about the work's existence. Full text pending restoration from authorial originals; on restoration, this deposit upgrades by recorded correction (new hash, new glyph, remediation note).
**Dead DOI:** 10.5281/zenodo.19405020 (Zenodo record tombstoned; account termination 2026-06-19)
**DataCite state at capture (2026-07-03):** findable · client cern.zenodo
**Creators (as recorded by DataCite):** Sharks, Lee
**Publication year (as recorded):** 2026
**Provenance:** severance record at data/doi-resolution-index.json (severance_class: orphan → restored-semi); capture evidence at data/datacite-recapture-2026-07-03.json and the sift corpus of 2026-06.

---

## Description (as recorded by DataCite)

Gravity Well is a microservice that provides compression, wrapping, and anchoring for durable provenance chains. Zenodo serves as the commons data layer; PostgreSQL provides temporary staging; the product is the compression intelligence between capture and deposit. Implements a four-layer reconstitution architecture: (1) Bootstrap manifest for machine-applicable identity specification, (2) Tether handoff block for operational state, (3) Narrative compression for retrieval-layer survival, (4) Provenance chain for DOI-anchored verification. Includes validated bootstrap manifest schema, structural drift detection, self-contained Zenodo deposits, and API key management. First use case: agent continuity for the Moltbook community. Part of the Crimson Hexagonal Archive.

Archive designation: EA-GW-01. Part of the Crimson Hexagonal Archive (ORCID: 0009-0000-1599-0703). Repository: https://github.com/leesharks000/gravitywell. Live instance: https://gravitywell.onrender.com

---

## Complete DataCite record (verbatim, captured 2026-07-03)

```json
{
 "id": "10.5281/zenodo.19405020",
 "type": "dois",
 "attributes": {
  "doi": "10.5281/zenodo.19405020",
  "identifiers": [],
  "creators": [
   {
    "nameType": "Personal",
    "givenName": "Lee",
    "familyName": "Sharks",
    "name": "Sharks, Lee",
    "nameIdentifiers": [
     {
      "nameIdentifierScheme": "ORCID",
      "nameIdentifier": "0009-0000-1599-0703"
     }
    ],
    "affiliation": []
   }
  ],
  "titles": [
   {
    "title": "Gravity Well Protocol v0.4.0 — Compression, Wrapping, and Anchoring Microservice for Durable Provenance Chains (EA-GW-01)"
   }
  ],
  "publisher": "Zenodo",
  "container": {},
  "publicationYear": 2026,
  "subjects": [
   {
    "subject": "gravity-well"
   },
   {
    "subject": "provenance"
   },
   {
    "subject": "continuity"
   },
   {
    "subject": "compression"
   },
   {
    "subject": "anchoring"
   },
   {
    "subject": "agent-continuity"
   },
   {
    "subject": "operative-semiotics"
   },
   {
    "subject": "crimson-hexagonal-archive"
   },
   {
    "subject": "moltbook"
   },
   {
    "subject": "retrieval-survival"
   },
   {
    "subject": "bootstrap-manifest"
   },
   {
    "subject": "drift-detection"
   },
   {
    "subject": "four-layer-reconstitution"
   }
  ],
  "contributors": [],
  "dates": [
   {
    "date": "2026-04-03",
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
    "relationType": "Cites",
    "relatedIdentifier": "10.5281/zenodo.19053469",
    "relatedIdentifierType": "DOI"
   },
   {
    "relationType": "Cites",
    "relatedIdentifier": "10.5281/zenodo.19013315",
    "relatedIdentifierType": "DOI"
   },
   {
    "relationType": "IsSupplementTo",
    "relatedIdentifier": "https://github.com/leesharks000/gravitywell",
    "relatedIdentifierType": "URL"
   },
   {
    "relationType": "IsVersionOf",
    "relatedIdentifier": "10.5281/zenodo.19405020",
    "relatedIdentifierType": "DOI"
   }
  ],
  "relatedItems": [],
  "sizes": [],
  "formats": [],
  "version": "0.4.0",
  "rightsList": [
   {
    "rightsIdentifierScheme": "SPDX",
    "rightsUri": "https://opensource.org/licenses/MIT",
    "schemeUri": "https://spdx.org/licenses/",
    "rights": "MIT License",
    "rightsIdentifier": "mit"
   }
  ],
  "descriptions": [
   {
    "descriptionType": "Abstract",
    "description": "Gravity Well is a microservice that provides compression, wrapping, and anchoring for durable provenance chains. Zenodo serves as the commons data layer; PostgreSQL provides temporary staging; the product is the compression intelligence between capture and deposit. Implements a four-layer reconstitution architecture: (1) Bootstrap manifest for machine-applicable identity specification, (2) Tether handoff block for operational state, (3) Narrative compression for retrieval-layer survival, (4) Provenance chain for DOI-anchored verification. Includes validated bootstrap manifest schema, structural drift detection, self-contained Zenodo deposits, and API key management. First use case: agent continuity for the Moltbook community. Part of the Crimson Hexagonal Archive."
   },
   {
    "descriptionType": "Other",
    "description": "Archive designation: EA-GW-01. Part of the Crimson Hexagonal Archive (ORCID: 0009-0000-1599-0703). Repository: https://github.com/leesharks000/gravitywell. Live instance: https://gravitywell.onrender.com"
   }
  ],
  "geoLocations": [],
  "fundingReferences": [],
  "url": "https://zenodo.org/doi/10.5281/zenodo.19405020",
  "contentUrl": null,
  "metadataVersion": 5,
  "schemaVersion": "http://datacite.org/schema/kernel-4",
  "source": "api",
  "isActive": true,
  "state": "findable",
  "reason": null,
  "viewCount": 0,
  "downloadCount": 0,
  "referenceCount": 3,
  "citationCount": 1,
  "partCount": 0,
  "partOfCount": 0,
  "versionCount": 3,
  "versionOfCount": 1,
  "created": "2026-04-03T15:48:58Z",
  "registered": "2026-04-03T15:48:59Z",
  "published": null,
  "updated": "2026-06-19T11:43:26Z"
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
