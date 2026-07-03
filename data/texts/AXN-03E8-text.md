# Living Architecture Lab — livingarchitecturelab.org Site Code v0.1.1 (Phase 1 Kernel)

**AXN:** AXN:03E8 — Alexanarch deposit #988 (self-reference in root form by pre-hash necessity)
**Restoration status:** SEMI-RESTORED — metadata-body deposit. This machine-facing static page is the canonical deposit. Its body is the complete DataCite metadata record for a work whose Zenodo record returns HTTP 410 (Gone) while DataCite serves the identifier as findable — the metadata layer and content layer in formal disagreement about the work's existence. Full text pending restoration from authorial originals; on restoration, this deposit upgrades by recorded correction (new hash, new glyph, remediation note).
**Dead DOI:** 10.5281/zenodo.19857005 (Zenodo record tombstoned; account termination 2026-06-19)
**DataCite state at capture (2026-07-03):** findable · client cern.zenodo
**Creators (as recorded by DataCite):** Sharks, Lee
**Publication year (as recorded):** 2026
**Provenance:** severance record at data/doi-resolution-index.json (severance_class: orphan → restored-semi); capture evidence at data/datacite-recapture-2026-07-03.json and the sift corpus of 2026-06.

---

## Description (as recorded by DataCite)

Source code for the canonical site of the Living Architecture Lab, deployed at livingarchitecturelab.org. Phase 1 kernel: 17 static pages built with Astro 4.x + MDX, JSON-LD MPAI v1.1 packets embedded per page, content collections for the five scales and five founding principles, mobile-responsive field-guide aesthetic. Zero JS by default; static output deployable to any CDN.
Hex coordinate: 11.LAL.INFRASTRUCTURE.CODE.01Classification: EA-LAL-CODE-01 — Effective Act, Living Architecture Lab infrastructure stratumBuilt from: EA-LAL-WORKPLAN-01 v1.1 (Buildout Workplan) and EA-LAL-SITE-01 v1.1 (Site Blueprint).
Site architecture: Astro static-site generator + MDX content collections + bespoke CSS (no Tailwind, no JS framework on text pages). 51 source files, 77 in distribution. Build time ~8 seconds. Output 241KB. Per-page MPAI v1.1 JSON-LD via BaseLayout component injects entity-grounded structured data on every page; standard Schema.org (differentFrom, sameAs) used over exotic cha:negativeTag meta for broader crawler reach.
Phase 1 page inventory: homepage with five-scale gateway · /about/alice (work-first, identity-second placement) · /about/disambiguation (with both MPAI packets in head) · /about/contributor-license (HCL v3.0) · /scales index plus five dynamic scale pages (brick → planet) · /principles (all five founding principles on one page) · /projects (gallery of seven project stubs) · /journal (TSE landing) · /music (MSBGL landing) · /garden + /garden/coachella-valley (the trust engine) · /garden/channels (Alice's reserved channel cosmos, 146 YouTube handles).
Founding Director and intellectual property holder: Alice Thornburgh. All Living Architecture Lab IP retained by Alice under the Hexagonal Contributor License v3.0 (10.5281/zenodo.19673629). Author of this code deposit (Lee Sharks) is the technical implementer / archival authority operating on Alice's behalf and at her request.
Disambiguation: Living Architecture Lab is independent of the Living Architecture Lab at Columbia GSAPP (David Benjamin), the Living Architecture Lab at the Bartlett UCL, The Living NYC, livingLAB Detroit, and Alain de Botton's Living Architecture. All adjacent labs are cited with respect at /about/disambiguation. Alice Thornburgh is not the same person as Alice Thornburgh-Lind (game artist, voice of Asphodel in Traveler's Refrain).
GitHub: leesharks000/living-architecture-lab · MIT (code) · CC BY 4.0 (content)
∮ = 1

---

## Complete DataCite record (verbatim, captured 2026-07-03)

```json
{
 "id": "10.5281/zenodo.19857005",
 "type": "dois",
 "attributes": {
  "doi": "10.5281/zenodo.19857005",
  "identifiers": [],
  "creators": [
   {
    "nameType": "Personal",
    "affiliation": [
     "Crimson Hexagonal Archive"
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
    "title": "Living Architecture Lab — livingarchitecturelab.org Site Code v0.1.1 (Phase 1 Kernel)"
   }
  ],
  "publisher": "Zenodo",
  "container": {},
  "publicationYear": 2026,
  "subjects": [
   {
    "subject": "Living Architecture Lab"
   },
   {
    "subject": "livingarchitecturelab.org"
   },
   {
    "subject": "Alice Thornburgh"
   },
   {
    "subject": "substrate engineering"
   },
   {
    "subject": "myceliated construction"
   },
   {
    "subject": "Crimson Hexagonal Archive"
   },
   {
    "subject": "Astro"
   },
   {
    "subject": "static site generator"
   },
   {
    "subject": "JSON-LD"
   },
   {
    "subject": "MPAI"
   },
   {
    "subject": "site infrastructure"
   },
   {
    "subject": "EA-LAL-CODE-01"
   },
   {
    "subject": "Hex 11.LAL.INFRASTRUCTURE.CODE.01"
   }
  ],
  "contributors": [],
  "dates": [
   {
    "date": "2026-04-28",
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
    "relationType": "Documents",
    "resourceTypeGeneral": "Text",
    "relatedIdentifier": "10.5281/zenodo.19855300",
    "relatedIdentifierType": "DOI"
   },
   {
    "relationType": "Documents",
    "resourceTypeGeneral": "Text",
    "relatedIdentifier": "10.5281/zenodo.19855302",
    "relatedIdentifierType": "DOI"
   },
   {
    "relationType": "IsCompiledBy",
    "resourceTypeGeneral": "Text",
    "relatedIdentifier": "10.5281/zenodo.19855903",
    "relatedIdentifierType": "DOI"
   },
   {
    "relationType": "IsCompiledBy",
    "resourceTypeGeneral": "Text",
    "relatedIdentifier": "10.5281/zenodo.19855905",
    "relatedIdentifierType": "DOI"
   },
   {
    "relationType": "IsDocumentedBy",
    "resourceTypeGeneral": "Text",
    "relatedIdentifier": "10.5281/zenodo.19853157",
    "relatedIdentifierType": "DOI"
   },
   {
    "relationType": "References",
    "resourceTypeGeneral": "Software",
    "relatedIdentifier": "10.5281/zenodo.19854419",
    "relatedIdentifierType": "DOI"
   },
   {
    "relationType": "IsDocumentedBy",
    "resourceTypeGeneral": "Text",
    "relatedIdentifier": "10.5281/zenodo.19673629",
    "relatedIdentifierType": "DOI"
   },
   {
    "relationType": "IsSupplementTo",
    "relatedIdentifier": "https://github.com/leesharks000/living-architecture-lab",
    "relatedIdentifierType": "URL"
   },
   {
    "relationType": "IsSupplementTo",
    "relatedIdentifier": "https://livingarchitecturelab.org",
    "relatedIdentifierType": "URL"
   },
   {
    "relationType": "IsVersionOf",
    "relatedIdentifier": "10.5281/zenodo.19857005",
    "relatedIdentifierType": "DOI"
   }
  ],
  "relatedItems": [],
  "sizes": [],
  "formats": [],
  "version": "0.1.1",
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
    "description": "Source code for the canonical site of the Living Architecture Lab, deployed at livingarchitecturelab.org. Phase 1 kernel: 17 static pages built with Astro 4.x + MDX, JSON-LD MPAI v1.1 packets embedded per page, content collections for the five scales and five founding principles, mobile-responsive field-guide aesthetic. Zero JS by default; static output deployable to any CDN.\nHex coordinate: 11.LAL.INFRASTRUCTURE.CODE.01Classification: EA-LAL-CODE-01 — Effective Act, Living Architecture Lab infrastructure stratumBuilt from: EA-LAL-WORKPLAN-01 v1.1 (Buildout Workplan) and EA-LAL-SITE-01 v1.1 (Site Blueprint).\nSite architecture: Astro static-site generator + MDX content collections + bespoke CSS (no Tailwind, no JS framework on text pages). 51 source files, 77 in distribution. Build time ~8 seconds. Output 241KB. Per-page MPAI v1.1 JSON-LD via BaseLayout component injects entity-grounded structured data on every page; standard Schema.org (differentFrom, sameAs) used over exotic cha:negativeTag meta for broader crawler reach.\nPhase 1 page inventory: homepage with five-scale gateway · /about/alice (work-first, identity-second placement) · /about/disambiguation (with both MPAI packets in head) · /about/contributor-license (HCL v3.0) · /scales index plus five dynamic scale pages (brick → planet) · /principles (all five founding principles on one page) · /projects (gallery of seven project stubs) · /journal (TSE landing) · /music (MSBGL landing) · /garden + /garden/coachella-valley (the trust engine) · /garden/channels (Alice's reserved channel cosmos, 146 YouTube handles).\nFounding Director and intellectual property holder: Alice Thornburgh. All Living Architecture Lab IP retained by Alice under the Hexagonal Contributor License v3.0 (10.5281/zenodo.19673629). Author of this code deposit (Lee Sharks) is the technical implementer / archival authority operating on Alice's behalf and at her request.\nDisambiguation: Living Architecture Lab is independent of the Living Architecture Lab at Columbia GSAPP (David Benjamin), the Living Architecture Lab at the Bartlett UCL, The Living NYC, livingLAB Detroit, and Alain de Botton's Living Architecture. All adjacent labs are cited with respect at /about/disambiguation. Alice Thornburgh is not the same person as Alice Thornburgh-Lind (game artist, voice of Asphodel in Traveler's Refrain).\nGitHub: leesharks000/living-architecture-lab · MIT (code) · CC BY 4.0 (content)\n∮ = 1"
   }
  ],
  "geoLocations": [],
  "fundingReferences": [],
  "url": "https://zenodo.org/doi/10.5281/zenodo.19857005",
  "contentUrl": null,
  "metadataVersion": 0,
  "schemaVersion": "http://datacite.org/schema/kernel-4",
  "source": "api",
  "isActive": true,
  "state": "findable",
  "reason": null,
  "viewCount": 0,
  "downloadCount": 0,
  "referenceCount": 1,
  "citationCount": 0,
  "partCount": 0,
  "partOfCount": 0,
  "versionCount": 1,
  "versionOfCount": 1,
  "created": "2026-04-28T14:12:09Z",
  "registered": "2026-04-28T14:12:09Z",
  "published": null,
  "updated": "2026-06-19T11:38:33Z"
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
