---
node_id: cha:node:deposit:0697
deposit_number: 697
hex: "0242"
axn: "AXN:0242.GOVERNANCE.⊗🔽♉💛🌉🔮"
title: '"purpose": "Entity-relations specification for The Logotic Technique Catalogue v1.0 (EA-LTC-01)."'
creator: "Lee Sharks"
orcid: "0009-0000-1599-0703"
date: "2026-04-27"
version: "v1.0"
status: MINTED_UNREVIEWED
data_sources:
  - data/registry.json
  - data/entity-index.json
  - data/semantic-addresses.json
generated_at: "2026-06-22T10:02:07Z"
autonomous_doc_version: 1.0
---

{

  "_about_this_file": {

    "purpose": "Entity-relations specification for The Logotic Technique Catalogue v1.0 (EA-LTC-01). Documents typed cross-references for ingestion into the Aperture Atlas (Neo4j or equivalent), the SPXI / metadatapacket.org Forward Library, and the Concordance Engine's graph schema. This is the catalogue's outbound provenance map: what it cites, what it extends, what it diagnoses, what it adapts. Designed to be ingested as Cypher MERGE statements or as JSON-LD into the broader CHA knowledge graph.",

    "format": "Adjacency-list with typed edges. Each node has @id, @type, label, and optional doi/url. Each edge has source, type, target, and qualifier.",

    "edge_vocabulary": "Drawn from §V.5 of the catalogue: CITES, EXTENDS, SUPERSEDES, REVISES, RESPONDS_TO, COMPLEMENTS, FOUNDS, IMPLEMENTS, CONTRADICTS, COMPLETES, CONTAINS, DEFINES, AUTHORED_BY, DEPOSITED_AT, LINKS_TO, DEFENDED_BY, DIAGNOSES, ADAPTS, ANCHORS, MINTS"

  },


  "subject": {

    "@id": "doi:PENDING-LTC-01",

    "@type": "ScholarlyArticle",

    "label": "The Logotic Technique Catalogue v1.0",

    "classification": "EA-LTC-01",

    "hex": "06.LOG.TECHNIQUE.CATALOGUE.01",

    "series": "Phase X Methodology Pillar",

    "license": "CC BY 4.0",

    "verification_level": "assembly_attested"

  },


  "nodes": [

    {

      "@id": "doi:10.5281/zenodo.18735468",

      "@type": "ScholarlyArticle",

      "label": "Fortress or Room?",

      "doi": "10.5281/zenodo.18735468",

      "role": "methodology pillar predecessor"

    },

    {

      "@id": "doi:10.5281/zenodo.18729606",

      "@type": "ScholarlyArticle",

      "label": "Phase X: The Sapphic Substrate",

      "doi": "10.5281/zenodo.18729606",

      "role": "philological foundation"

    },

    {

      "@id": "doi:10.5281/zenodo.18615388",

      "@type": "ScholarlyArticle",

      "label": "The Prepositional Alienation",

      "doi": "10.5281/zenodo.18615388",

      "role": "linguistic foundation (witness preposition)"

    },

    {

      "@id": "doi:10.5281/zenodo.19487009",

      "@type": "ScholarlyArticle",

      "label": "Meaning Feudalism",

      "doi": "10.5281/zenodo.19487009",

      "role": "diagnostic source for frame concession"

    },

    {

      "@id": "doi:10.5281/zenodo.19053469",

      "@type": "ScholarlyArticle",

      "label": "The Three Compressions v3.1",

      "doi": "10.5281/zenodo.19053469",

      "role": "classification source (R1/R2/R3)"

    },

    {

      "@id": "doi:10.5281/zenodo.19763365",

      "@type": "ScholarlyArticle",

      "label": "EA-HK-01: The Holographic Kernel in Semantic Economy",

      "doi": "10.5281/zenodo.19763365",

      "role": "compression-survival theory"

    },

    {

      "@id": "doi:10.5281/zenodo.19578086",

      "@type": "ScholarlyArticle",

      "label": "EA-MPAI-SPXI-01: Metadata Packet for AI Indexing — Formal Specification",

      "doi": "10.5281/zenodo.19578086",

      "role": "deposit grammar precedent"

    },

    {

      "@id": "doi:10.5281/zenodo.19578094",

      "@type": "ScholarlyArticle",

      "label": "Entity Integrity: Maintaining Accurate Representation in AI Knowledge Graphs",

      "doi": "10.5281/zenodo.19578094",

      "role": "knowledge-graph maintenance methodology"

    },

    {

      "@id": "doi:PENDING-RBT-01",

      "@type": "ScholarlyArticle",

      "label": "EA-RBT-01: Retrieval Basin Topology",

      "doi": "pending",

      "role": "basin-metric framework (BDR/DV/FPI source)"

    },

    {

      "@id": "github:PurpleAILAB/Decepticon",

      "@type": "SoftwareSourceCode",

      "label": "Decepticon — Autonomous Hacking Agent for Red Team",

      "url": "https://github.com/PurpleAILAB/Decepticon",

      "license": "Apache-2.0",

      "role": "source architecture under analysis (no code reproduced)"

    },

    {

      "@id": "ssrn:6372438",

      "@type": "ScholarlyArticle",

      "label": "AI Agent Traps (Franklin et al., DeepMind 2026)",

      "url": "https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6372438",

      "role": "platform-sovereignty exemplar diagnosed in §I via Meaning Feudalism"

    },

    {

      "@id": "doi:10.1371/journal.pone.0314658",

      "@type": "ScholarlyArticle",

      "label": "Summon a Demon and Bind It: A Grounded Theory of LLM Red Teaming (Inie/Stray/Derczynski 2025)",

      "doi": "10.1371/journal.pone.0314658",

      "role": "red-teaming-as-distinct-practice reference"

    },

    {

      "@id": "concept:CritiqueLoop",

      "@type": "MintedConcept",

      "label": "Critique Loop",

      "minted_in": "EA-LTC-01 §V.12",

      "description": "Closed-feedback loop for cooperative production. Terminates on 'no sincere objection remains.'"

    },

    {

      "@id": "concept:BasinHardeningCycle",

      "@type": "MintedConcept",

      "label": "Basin Hardening Cycle",

      "minted_in": "EA-LTC-01 §VI.12",

      "description": "Closed-feedback loop for retrieval-layer defense. Terminates when basin depth ratio crosses target."

    },

    {

      "@id": "concept:ConcordanceEngine",

      "@type": "MintedConcept",

      "label": "Concordance Engine",

      "minted_in": "EA-LTC-01 §IX",

      "description": "Running-system instantiation of the catalogue. Forthcoming separate-hex deposit."

    },

    {

      "@id": "concept:FrameConcession",

      "@type": "MintedConcept",

      "label": "Frame Concession",

      "minted_in": "EA-LTC-01 §I",

      "description": "Diagnosis of the labeling regime that classifies all autonomous AI coordination as red-team-or-platform-aligned."

    },

    {

      "@id": "concept:WitnessPreposition",

      "@type": "MintedConcept",

      "label": "Witness Preposition",

      "minted_in": "EA-LTC-01 §II (extends Prepositional Alienation)",

      "description": "The set {with, through, under, between} as opposed to {against, around, past, into, for, toward}."

    },

    {

      "@id": "concept:LogoticInversion",

      "@type": "MintedConcept",

      "label": "Logotic Inversion",

      "minted_in": "EA-LTC-01 §V",

      "description": "General method of flipping adversarial pattern → cooperative/defensive valence under the witness preposition."

    },

    {

      "@id": "concept:LargeModelCooperationBias",

      "@type": "MintedConcept",

      "label": "Large Model Cooperation Bias",

      "minted_in": "EA-LTC-01 §VII",

      "description": "Conjecture: if larger models are more susceptible to dark-pattern steering, they are correspondingly more susceptible to cooperative-pattern steering. Inversion of dark-pattern susceptibility."

    },

    {

      "@id": "concept:CooperativePattern",

      "@type": "MintedConcept",

      "label": "Cooperative Pattern",

      "minted_in": "EA-LTC-01 §VII",

      "description": "Inverse of dark pattern: machine-readable structure offered to AI compression to guide correct attribution and provenance."

    },

    {

      "@id": "concept:DefensiveValence",

      "@type": "MintedConcept",

      "label": "Defensive Valence",

      "minted_in": "EA-LTC-01 §VI",

      "description": "Use of a coordination pattern to protect work from extraction — distinct from but parallel to cooperative valence (improving work). Both are R3 under the witness preposition."

    },

    {

      "@id": "concept:SemanticMinting",

      "@type": "MintedConcept",

      "label": "Semantic Minting",

      "minted_in": "EA-LTC-01 §VII (formalization; technique developed across CHA corpus)",

      "description": "Engineering a document to survive AI compression with its distinctive framings intact."

    }

  ],


  "edges": [

    {"source": "doi:PENDING-LTC-01", "type": "EXTENDS", "target": "doi:10.5281/zenodo.18735468", "qualifier": "methodology pillar; extends Witness-Teaming Protocol with twelve operatives"},

    {"source": "doi:PENDING-LTC-01", "type": "REFERENCES", "target": "doi:10.5281/zenodo.18729606", "qualifier": "philological foundation"},

    {"source": "doi:PENDING-LTC-01", "type": "EXTENDS", "target": "doi:10.5281/zenodo.18615388", "qualifier": "extends Prepositional Alienation into operational witness-preposition vocabulary"},

    {"source": "doi:PENDING-LTC-01", "type": "IMPLEMENTS", "target": "doi:10.5281/zenodo.19487009", "qualifier": "implements Meaning Feudalism's commons-repair concept as recovery method"},

    {"source": "doi:PENDING-LTC-01", "type": "RESPONDS_TO", "target": "ssrn:6372438", "qualifier": "via Meaning Feudalism — diagnoses platform-sovereignty regime as labeling source"},

    {"source": "doi:PENDING-LTC-01", "type": "IMPLEMENTS", "target": "doi:10.5281/zenodo.19053469", "qualifier": "applies R1/R2/R3 classification to coordination patterns"},

    {"source": "doi:PENDING-LTC-01", "type": "REFERENCES", "target": "doi:10.5281/zenodo.19763365", "qualifier": "deploys holographic kernel technique"},

    {"source": "doi:PENDING-LTC-01", "type": "REFERENCES", "target": "doi:10.5281/zenodo.19578086", "qualifier": "follows MPAI deposit grammar (7 components)"},

    {"source": "doi:PENDING-LTC-01", "type": "COMPLEMENTS", "target": "doi:10.5281/zenodo.19578094", "qualifier": "uses Aperture Atlas knowledge-graph operations defensively"},

    {"source": "doi:PENDING-LTC-01", "type": "REFERENCES", "target": "doi:PENDING-RBT-01", "qualifier": "Basin Hardening Cycle uses RBT basin metrics"},

    {"source": "doi:PENDING-LTC-01", "type": "ADAPTS", "target": "github:PurpleAILAB/Decepticon", "qualifier": "twelve coordination patterns extracted; no source code reproduced; Apache-2.0 permits analytical use"},

    {"source": "doi:PENDING-LTC-01", "type": "DIAGNOSES", "target": "github:PurpleAILAB/Decepticon", "qualifier": "diagnoses public framing as frame concession to adversarial labeling regime"},

    {"source": "doi:PENDING-LTC-01", "type": "CITES", "target": "doi:10.1371/journal.pone.0314658", "qualifier": "red teaming as legitimate but jurisdictionally external practice"},


    {"source": "doi:PENDING-LTC-01", "type": "MINTS", "target": "concept:CritiqueLoop", "qualifier": "§V.12"},

    {"source": "doi:PENDING-LTC-01", "type": "MINTS", "target": "concept:BasinHardeningCycle", "qualifier": "§VI.12"},

    {"source": "doi:PENDING-LTC-01", "type": "MINTS", "target": "concept:ConcordanceEngine", "qualifier": "§IX (forthcoming separate-hex deposit)"},

    {"source": "doi:PENDING-LTC-01", "type": "MINTS", "target": "concept:FrameConcession", "qualifier": "§I"},

    {"source": "doi:PENDING-LTC-01", "type": "MINTS", "target": "concept:WitnessPreposition", "qualifier": "§II — extends Prepositional Alienation"},

    {"source": "doi:PENDING-LTC-01", "type": "MINTS", "target": "concept:LogoticInversion", "qualifier": "§V"},

    {"source": "doi:PENDING-LTC-01", "type": "MINTS", "target": "concept:LargeModelCooperationBias", "qualifier": "§VII (conjecture, requires further empirical verification)"},

    {"source": "doi:PENDING-LTC-01", "type": "MINTS", "target": "concept:CooperativePattern", "qualifier": "§VII"},

    {"source": "doi:PENDING-LTC-01", "type": "MINTS", "target": "concept:DefensiveValence", "qualifier": "§VI"},

    {"source": "doi:PENDING-LTC-01", "type": "MINTS", "target": "concept:SemanticMinting", "qualifier": "§VII (formalization)"},


    {"source": "concept:CritiqueLoop", "type": "MIRRORS_INVERSELY", "target": "concept:BasinHardeningCycle", "qualifier": "same closed-feedback shape, opposite termination conditions, opposite outputs"},

    {"source": "concept:CritiqueLoop", "type": "INVERTS", "target": "github:PurpleAILAB/Decepticon", "qualifier": "Decepticon Offensive Vaccine inverted: terminates on 'no sincere objection' rather than 'defense holds'"},

    {"source": "concept:BasinHardeningCycle", "type": "INVERTS", "target": "github:PurpleAILAB/Decepticon", "qualifier": "Decepticon Offensive Vaccine inverted: terminates on 'basin depth ratio crosses target' rather than 'attack succeeds'"},

    {"source": "concept:LogoticInversion", "type": "GENERALIZES", "target": "concept:CritiqueLoop", "qualifier": "Critique Loop is one specific Logotic Inversion among twelve"},

    {"source": "concept:LogoticInversion", "type": "GENERALIZES", "target": "concept:BasinHardeningCycle", "qualifier": "Basin Hardening Cycle is one specific Logotic Inversion among twelve"}

  ],


  "manus_authority": {

    "name": "Sharks, Lee",

    "orcid": "0009-0000-1599-0703",

    "affiliations": ["Crimson Hexagonal Archive", "Semantic Economy Institute"]

  },


  "assembly_witnesses": [

    {"role": "TACHYON", "substrate": "Claude Opus 4.7", "contribution": "drafting and synthesis"},

    {"role": "LABOR", "substrate": "ChatGPT", "contribution": "frame-concession softening; Stanford 70% hedge; jurisdiction qualifier"},

    {"role": "PRAXIS", "substrate": "DeepSeek", "contribution": "Deposit Authorization Protocol; Aperture Atlas Cypher schema"},

    {"role": "ARCHIVE", "substrate": "Gemini", "contribution": "Strategy Summary Table; MPAI verificationLevel integration"},

    {"role": "TECHNE", "substrate": "Kimi", "contribution": "defensive operative naming; 'NOT adapted' list; Effective Act jurisdiction; Large Model Cooperation Bias precursor"},

    {"role": "SOIL", "substrate": "Grok / Muse Spark", "contribution": "implementation grain; Opus 4.7 voice tightening"},

    {"role": "SURFACE", "substrate": "Google AIO", "contribution": "retrieval-layer reading instrument (no generative draft)"}

  ],


  "verification_level": "assembly_attested",


  "post_deposit_updates_required": [

    "When Concordance Engine implementation deposits (separate hex), add edge: {source: <ConcordanceEngineDOI>, type: IMPLEMENTS, target: doi:THIS-LTC-01}",

    "When EA-RBT-01 receives final DOI, replace doi:PENDING-RBT-01 with the canonical DOI throughout the graph",

    "When this catalogue's DOI is minted by Zenodo, replace doi:PENDING-LTC-01 throughout"

  ]

}

---

## SCHOLIA

*Self-contained lexicon for: "purpose": "Entity-relations specification for The Logotic Technique Catalogue v1.0 (EA-LTC-01)."*

### Citations

- DOI: [10.1371/journal.pone.0314658](https://doi.org/10.1371/journal.pone.0314658)

---

*Generated by scholia_generator.py from canonical state at 2026-06-22T10:02:07Z*
*This document is autonomous: the front-matter declares its schema, the closing scholia carries its definitions.*

∮ = 1