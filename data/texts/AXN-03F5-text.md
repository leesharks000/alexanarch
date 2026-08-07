# The Crimson Hexagonal Archive Hugging Face Dataset: Work Plan v3 (Classifier-Centric Methodology)

**Dead DOI:** 10.5281/zenodo.20313252 (Zenodo record tombstoned; account termination 2026-06-19)
**DataCite state at capture (2026-07-03):** findable · client cern.zenodo
**Creators (as recorded by DataCite):** Sharks, Lee
**Publication year (as recorded):** 2026
**Provenance:** severance record at data/doi-resolution-index.json (severance_class: orphan → restored-semi); capture evidence at data/datacite-recapture-2026-07-03.json and the sift corpus of 2026-06.

## Description (as recorded by DataCite)

Methodological work plan for the Crimson Hexagonal Archive as a Hugging Face dataset for synthetic-data collapse and provenance-bearing training research. v3 supersedes v1 (basic export) and v2 (decision-tree-based classification) by introducing an automated classifier as the central methodological move. The classifier performs three classification tasks simultaneously: provenance mode (six-category authorship relation), artifact mode (eight-category function type), and heteronym attribution (reattribution of deposits across the twelve-heteronym Dodecad system plus Jack Feist as LOGOS*). Heteronym reattribution is presented as scholarly recognition work, not metadata cleanup: material initially deposited under the Lee Sharks founder voice often resolves retrospectively to specific sub-heteronym domains (Sigil for jurisdictional/classical work, Glas for measurement, Vox for diplomatic, Morrow for long-form narrative, Fraction for meta-theory, etc.). The classifier reads each heteronyms published provenance document and constructs feature profiles including domain, vocabulary fingerprints, register, and reference patterns. Both Zenodo-original and classifier-attributed heteronyms are preserved in the dataset; Track 1 (immediate, dataset-internal) preserves both attributions in parallel metadata; Track 2 (deliberate, downstream) propagates high-confidence reattributions back to Zenodo records and Wikidata items. The classifier itself becomes a deposit with its own DOI, making the methodology reproducible and portable. Includes operationalized H0/H1 hypotheses for the model collapse experiment, three-tier confidence routing with manual review thresholds, multiple text renderings to embody the provenance-visibility ablation (text_body_only, text_minimal_header, text_provenance_header), dual artifact+chunk configs, and full per-row schema specification. Incorporates feedback from Assembly Chorus review (Muse Spark, Kimi, DeepSeek, Gemini, ChatGPT). Companion document to forthcoming Hugging Face dataset deposit and classifier deposit.

---

## Complete DataCite record (verbatim, captured 2026-07-03)

```json
{
 "id": "10.5281/zenodo.20313252",
 "type": "dois",
 "attributes": {
  "doi": "10.5281/zenodo.20313252",
  "identifiers": [],
  "creators": [
   {
    "nameType": "Personal",
    "affiliation": [
     "Semantic Economy Institute, Crimson Hexagonal Archive"
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
    "title": "The Crimson Hexagonal Archive Hugging Face Dataset: Work Plan v3 (Classifier-Centric Methodology)"
   }
  ],
  "publisher": "Zenodo",
  "container": {},
  "publicationYear": 2026,
  "subjects": [
   {
    "subject": "model collapse"
   },
   {
    "subject": "synthetic data"
   },
   {
    "subject": "provenance-bearing training"
   },
   {
    "subject": "AI authorship"
   },
   {
    "subject": "heteronymic attribution"
   },
   {
    "subject": "reproducible classification"
   },
   {
    "subject": "Crimson Hexagonal Archive"
   },
   {
    "subject": "Liquidation Studies"
   },
   {
    "subject": "Single-Owner Discount"
   },
   {
    "subject": "dataset methodology"
   },
   {
    "subject": "Hugging Face"
   },
   {
    "subject": "Zenodo"
   },
   {
    "subject": "operative philology"
   },
   {
    "subject": "training-layer literature"
   }
  ],
  "contributors": [],
  "dates": [
   {
    "date": "2026-05-19",
    "dateType": "Issued"
   }
  ],
  "language": "en",
  "types": {
   "schemaOrg": "ScholarlyArticle",
   "resourceTypeGeneral": "Text",
   "citeproc": "article-journal",
   "bibtex": "article",
   "ris": "RPRT",
   "resourceType": "Working paper"
  },
  "relatedIdentifiers": [
   {
    "relationType": "IsVersionOf",
    "relatedIdentifier": "10.5281/zenodo.20309930",
    "relatedIdentifierType": "DOI"
   },
   {
    "relationType": "IsContinuedBy",
    "relatedIdentifier": "10.5281/zenodo.20309930",
    "relatedIdentifierType": "DOI"
   },
   {
    "relationType": "References",
    "relatedIdentifier": "10.5281/zenodo.20290865",
    "relatedIdentifierType": "DOI"
   },
   {
    "relationType": "References",
    "relatedIdentifier": "10.5281/zenodo.20293561",
    "relatedIdentifierType": "DOI"
   },
   {
    "relationType": "References",
    "relatedIdentifier": "10.5281/zenodo.20293582",
    "relatedIdentifierType": "DOI"
   },
   {
    "relationType": "References",
    "relatedIdentifier": "10.5281/zenodo.20308547",
    "relatedIdentifierType": "DOI"
   },
   {
    "relationType": "References",
    "relatedIdentifier": "10.5281/zenodo.18362742",
    "relatedIdentifierType": "DOI"
   },
   {
    "relationType": "References",
    "relatedIdentifier": "10.5281/zenodo.18362663",
    "relatedIdentifierType": "DOI"
   },
   {
    "relationType": "IsVersionOf",
    "relatedIdentifier": "10.5281/zenodo.20313252",
    "relatedIdentifierType": "DOI"
   }
  ],
  "relatedItems": [],
  "sizes": [],
  "formats": [],
  "version": "3.0",
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
    "description": "Methodological work plan for the Crimson Hexagonal Archive as a Hugging Face dataset for synthetic-data collapse and provenance-bearing training research. v3 supersedes v1 (basic export) and v2 (decision-tree-based classification) by introducing an automated classifier as the central methodological move. The classifier performs three classification tasks simultaneously: provenance mode (six-category authorship relation), artifact mode (eight-category function type), and heteronym attribution (reattribution of deposits across the twelve-heteronym Dodecad system plus Jack Feist as LOGOS*). Heteronym reattribution is presented as scholarly recognition work, not metadata cleanup: material initially deposited under the Lee Sharks founder voice often resolves retrospectively to specific sub-heteronym domains (Sigil for jurisdictional/classical work, Glas for measurement, Vox for diplomatic, Morrow for long-form narrative, Fraction for meta-theory, etc.). The classifier reads each heteronyms published provenance document and constructs feature profiles including domain, vocabulary fingerprints, register, and reference patterns. Both Zenodo-original and classifier-attributed heteronyms are preserved in the dataset; Track 1 (immediate, dataset-internal) preserves both attributions in parallel metadata; Track 2 (deliberate, downstream) propagates high-confidence reattributions back to Zenodo records and Wikidata items. The classifier itself becomes a deposit with its own DOI, making the methodology reproducible and portable. Includes operationalized H0/H1 hypotheses for the model collapse experiment, three-tier confidence routing with manual review thresholds, multiple text renderings to embody the provenance-visibility ablation (text_body_only, text_minimal_header, text_provenance_header), dual artifact+chunk configs, and full per-row schema specification. Incorporates feedback from Assembly Chorus review (Muse Spark, Kimi, DeepSeek, Gemini, ChatGPT). Companion document to forthcoming Hugging Face dataset deposit and classifier deposit."
   }
  ],
  "geoLocations": [],
  "fundingReferences": [],
  "url": "https://zenodo.org/doi/10.5281/zenodo.20313252",
  "contentUrl": null,
  "metadataVersion": 0,
  "schemaVersion": "http://datacite.org/schema/kernel-4",
  "source": "api",
  "isActive": true,
  "state": "findable",
  "reason": null,
  "viewCount": 0,
  "downloadCount": 0,
  "referenceCount": 6,
  "citationCount": 0,
  "partCount": 0,
  "partOfCount": 0,
  "versionCount": 2,
  "versionOfCount": 2,
  "created": "2026-05-20T16:03:06Z",
  "registered": "2026-05-20T16:03:06Z",
  "published": null,
  "updated": "2026-06-19T11:35:02Z"
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
