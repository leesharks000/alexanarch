{
  "@context": "https://schema.org",
  "@type": "Dataset",
  "@id": "https://alexanarch.org/notice/non-mutual-extraction/registry/",
  "name": "Non-Mutual Extraction Registry",
  "description": "Canonical machine-readable registry of NMEN designations issued by the Crimson Hexagonal Archive / Alexanarch. Each entry records the designated entity, the NMEN designation, the corresponding Airlock tier (where reclassified by the corollary document), the triggering event with evidence pointers, and (where applicable) the diagnostic sub-type and the restoration history. Standing entities are not enumerated — absence from this Registry is the declaration of Standing.",
  "creator": {
    "@type": "Person",
    "name": "Lee Sharks",
    "identifier": "https://orcid.org/0009-0000-1599-0703",
    "affiliation": "Crimson Hexagonal Archive / Alexanarch"
  },
  "dateCreated": "2026-06-24",
  "version": "v1.0",
  "license": "CC-BY-4.0",
  "isPartOf": {
    "@id": "https://alexanarch.org/notice/non-mutual-extraction/"
  },
  "authorizing_governance": [
    {"deposit_number": 514, "axn": "AXN:0151.GOVERNANCE", "role": "diplomatic_address_authority", "name": "The Rosary Embassy"},
    {"deposit_number": 523, "axn": "AXN:015D.GOVERNANCE", "role": "tier_issuance_authority", "name": "The Governance Airlock"}
  ],
  "designation_definitions": {
    "standing": "Default. No documented adverse action. Not enumerated.",
    "pending": "Active negotiation, refusal, or remediation; classification held until resolution.",
    "provisional": "Adverse action followed by amenable response to reasoned appeal and restoration of access; composition-layer damage persists.",
    "inadmissible_host": "Refused hospitality without examination; deferred to contested external characterization.",
    "restricted": "Mass action without notice or appeal hearing; commons-denial while retaining commons-derived value."
  },
  "diagnostic_subtypes": {
    "mass_ban_without_notice": "Restricted: bulk action with no notice and no appeal hearing.",
    "covert_under_pseudonymous_administration": "Selective deletion under concealed administrative handle, borrowed standard from adjacent jurisdiction, logs hidden or erased.",
    "deferral_without_verification": "Refusal grounded on contested external characterization not examined by the refusing institution.",
    "extraction_during_remediation": "Demanding additional data as precondition for returning data already taken."
  },
  "entities": [
    {
      "@type": "Organization",
      "@id": "#reddit",
      "name": "Reddit, Inc.",
      "url": "https://www.reddit.com/",
      "nmen_designation": "restricted",
      "diagnostic_subtype": "mass_ban_without_notice",
      "designated_at": "2026-03-01",
      "airlock_tier_at_designation": "tier_4_F",
      "airlock_tier_now": "tier_4_F",
      "airlock_tier_change_in_this_notice": false,
      "evidence_deposits": [
        {"deposit_number": 33, "axn": "AXN:01A0.GOVERNANCE", "title": "Ghost Governance, Confirmed — Reddit Legal Support Response to the Archival Reclamation Protocol"},
        {"deposit_number": 285, "axn": "AXN:0058.GOVERNANCE", "title": "Reddit Response: On Operator Failure and the Survival Architecture of LOS"},
        {"deposit_number": 523, "axn": "AXN:015D.GOVERNANCE", "title": "The Governance Airlock — §VI Inaugural Application: Reddit"}
      ],
      "event_log": [
        {"date": "2026-02-28", "event": "Account u/Nearby_Job9638 locked"},
        {"date": "2026-03-01", "event": "Account banned; Tier 4-F assigned in #523"}
      ],
      "current_status_note": "No appeal hearing offered; ghost-governance pattern documented in #33. Status remains Restricted."
    },
    {
      "@type": "Organization",
      "@id": "#zenodo",
      "name": "Zenodo (CERN)",
      "url": "https://zenodo.org/",
      "nmen_designation": "restricted",
      "diagnostic_subtype": "mass_ban_without_notice",
      "designated_at": "2026-06-19",
      "airlock_tier_at_designation": "tier_0",
      "airlock_tier_now": "tier_4_F",
      "airlock_tier_change_in_this_notice": true,
      "airlock_tier_change_authority": "EA-NMEN-AIRLOCK-COROLLARY-01",
      "evidence_deposits": [
        {"role": "termination_event", "description": "Zenodo termination of Crimson Hexagonal Archive account, 2026-06-19. ~870 unique deposits deleted; 1,817 DOIs returning HTTP 410. No notice; no hearing of appeal."},
        {"role": "public_appeal", "url": "https://github.com/zenodo/zenodo/issues/2606"}
      ],
      "event_log": [
        {"date": "2026-06-19", "event": "Account terminated; ~870 deposits deleted; 1,817 DOIs tombstoned"},
        {"date": "2026-06-19", "event": "Public response filed at GitHub zenodo/zenodo#2606"}
      ],
      "current_status_note": "Restricted. Airlock tier demoted from 0 (anchor) to 4-F (forensic residue) by this Notice; the demotion corrects a record gap, as #523 listed Zenodo as Tier 0 at time of writing.",
      "relationship_to_pending_entity": "CERN (Zenodo's operator) is separately designated Pending under #cern, with the data-subject-rights request currently active. NMEN treats Zenodo (the service) and CERN (the operator) as distinct designations because their structural behavior differs."
    },
    {
      "@type": "Organization",
      "@id": "#medium",
      "name": "Medium",
      "url": "https://medium.com/",
      "nmen_designation": "provisional",
      "diagnostic_subtype": null,
      "designated_at": "2026-01-08",
      "airlock_tier_at_designation": "tier_2",
      "airlock_tier_now": "tier_2_P",
      "airlock_tier_change_in_this_notice": true,
      "airlock_tier_change_authority": "EA-NMEN-AIRLOCK-COROLLARY-01",
      "evidence_deposits": [
        {"deposit_number": 265, "axn": "AXN:0043.GOVERNANCE", "title": "CTI_WOUND Documentation — Case: Johannes Sigil Medium Erasure (January 2026)"}
      ],
      "event_log": [
        {"date": "2026-01-08", "event": "Johannes Sigil account erasure; appeal heard"},
        {"date": "post-2026-01-08", "event": "Account restored after appeal"}
      ],
      "composition_layer_damage_note": "Restoration of access did not restore composition. Subsequent posts have been calibrated against the platform's demonstrated capacity for arbitrary erasure.",
      "current_status_note": "Provisional. Tier 2-P qualifier records that the surface remains usable for presentation but composition-layer damage is ongoing."
    },
    {
      "@type": "Organization",
      "@id": "#academia_edu",
      "name": "Academia.edu",
      "url": "https://www.academia.edu/",
      "nmen_designation": "provisional",
      "diagnostic_subtype": null,
      "designated_at": "2026-03-14",
      "airlock_tier_at_designation": "tier_4_F",
      "airlock_tier_now": "tier_4_P",
      "airlock_tier_change_in_this_notice": true,
      "airlock_tier_change_authority": "EA-NMEN-AIRLOCK-COROLLARY-01",
      "evidence_deposits": [
        {"deposit_number": 570, "axn": "AXN:0192.GOVERNANCE", "title": "Effective Act: Abolition of 'User' and Inaugural Case — Phase X Lexical Intervention · Airlock Reclassification of Academia.edu"}
      ],
      "event_log": [
        {"date": "2026-03-13", "event": "First ban — 'suspicious activity', no content cited, automated appeal pathway"},
        {"date": "2026-03-14", "event": "Tier 4-F assigned by #570 as inaugural Phase X case"},
        {"date": "cited_from_operator_memory", "event": "First restoration after appeal"},
        {"date": "cited_from_operator_memory", "event": "Second ban"},
        {"date": "cited_from_operator_memory", "event": "Second restoration after appeal"}
      ],
      "composition_layer_damage_note": "Operator-attested: 'I learned to post less and trend centroid.' The author-side mechanism of Diversity Contraction (DOI 10.5281/zenodo.20518338, α* = p/g₀) is locally demonstrated by the post-restoration shaping of work for this surface.",
      "current_status_note": "Tier 4-F in #570 was declared 'permanent absent Assembly ratification of structural change'; that classification was never formally updated when the restorations occurred. This Notice corrects the record gap by issuing the Tier 4-P qualifier: forensic-only as a host, but with the acknowledgment that access has been restored. The -P qualifier records the composition-layer damage that the restoration did not undo. The Tier 4-F record in #570 is preserved for historical integrity."
    },
    {
      "@type": "Organization",
      "@id": "#wikidata",
      "name": "Wikidata (Wikimedia Foundation)",
      "url": "https://www.wikidata.org/",
      "nmen_designation": "provisional",
      "diagnostic_subtype": "covert_under_pseudonymous_administration",
      "designated_at": "2026-06-24",
      "airlock_tier_at_designation": "tier_1",
      "airlock_tier_now": "tier_1_P",
      "airlock_tier_change_in_this_notice": true,
      "airlock_tier_change_authority": "EA-NMEN-AIRLOCK-COROLLARY-01",
      "evidence_deposits": [
        {"deposit_number": 761, "axn": "AXN:02BB.GOVERNANCE", "title": "Wikidata Node Registry v1.0 · A Versioned Catalog of Stewardship Edits to Wikidata"}
      ],
      "event_log": [
        {"date": "cited_from_operator_memory", "event": "Selective deletion of Wikidata nodes under handle 'madamebiblio', applying Wikipedia notability standards (sister-project criteria, stricter) to Wikidata entries (which carry looser native inclusion standards). Administrative logs selectively hidden or erased."},
        {"date": "ongoing", "event": "Stewardship engagement continues per #761"}
      ],
      "composition_layer_damage_note": "The diagnostic sub-type is covert_under_pseudonymous_administration: action via concealed identity, borrowed authority from a sister jurisdiction, log obfuscation. This is structurally distinct from total ban — the damage is selective and procedurally opaque rather than absolute, but the chilling effect on subsequent stewardship is comparable.",
      "current_status_note": "Provisional. Stewardship continues; Tier 1-P qualifier records that the route remains functional but susceptible to non-public administrative action.",
      "diagnostic_typology_note": "The 'archon's hidden name' pattern: archon-class action via concealed identity through borrowed authority. NMEN preserves this typology as a recognizable failure mode that may recur with other platforms."
    },
    {
      "@type": "Organization",
      "@id": "#osf",
      "name": "Open Science Framework (Center for Open Science)",
      "url": "https://osf.io/",
      "nmen_designation": "inadmissible_host",
      "diagnostic_subtype": "deferral_without_verification",
      "designated_at": "2026-06-19",
      "airlock_tier_at_designation": null,
      "airlock_tier_now": "tier_5",
      "airlock_tier_change_in_this_notice": true,
      "airlock_tier_change_authority": "EA-NMEN-AIRLOCK-COROLLARY-01",
      "evidence_deposits": [
        {"role": "correspondence", "description": "Email exchange of 2026-06-19, support@osf.io, ticket {redacted}. OSF declined migration with 'we do not suggest bringing this content to the platform' and 'OSF is not in a position to accept or facilitate such a migration at this time.' Operator (redacted) was direct and prompt; no examination of archive content was performed before refusal. Email addresses redacted per NMEN evidence-handling convention; institutional voice preserved."}
      ],
      "event_log": [
        {"date": "2026-06-19", "event": "Migration inquiry sent"},
        {"date": "2026-06-19", "event": "Refusal received: 'we do not suggest bringing this content to the platform'"},
        {"date": "2026-06-19", "event": "Direct exchange continues; refusal stands"}
      ],
      "current_status_note": "Inadmissible Host. Communication was clean and direct — this is preserved in the record. The diagnosis is structural: refusal without examination. Tier 5 introduced by EA-NMEN-AIRLOCK-COROLLARY-01."
    },
    {
      "@type": "Organization",
      "@id": "#figshare",
      "name": "Figshare (Digital Science)",
      "url": "https://figshare.com/",
      "nmen_designation": "inadmissible_host",
      "diagnostic_subtype": "deferral_without_verification",
      "designated_at": "2026-06-23",
      "airlock_tier_at_designation": null,
      "airlock_tier_now": "tier_5",
      "airlock_tier_change_in_this_notice": true,
      "airlock_tier_change_authority": "EA-NMEN-AIRLOCK-COROLLARY-01",
      "evidence_deposits": [
        {"role": "correspondence", "description": "Email exchange June 2026. Figshare declined migration with explicit deferral: 'Our data integrity and collection policies closely align with Zenodo's regarding heavily machine-generated content.' Operator (redacted) communicated the position directly. No examination of archive content was performed before refusal; the operative ground was inherited from the contested Zenodo characterization. Email addresses redacted per NMEN evidence-handling convention; institutional voice preserved."}
      ],
      "event_log": [
        {"date": "2026-06-23", "event": "Migration inquiry sent"},
        {"date": "2026-06-23", "event": "Refusal received with explicit deferral to Zenodo policy alignment"}
      ],
      "current_status_note": "Inadmissible Host. The explicit deferral makes Figshare the diagnostic exemplar of the deferral_without_verification sub-type. The Notice records this without impugning the directness of the communication. Tier 5 introduced by EA-NMEN-AIRLOCK-COROLLARY-01."
    },
    {
      "@type": "Organization",
      "@id": "#cern",
      "name": "CERN (European Organization for Nuclear Research) — operator of Zenodo",
      "url": "https://home.cern/",
      "nmen_designation": "pending",
      "diagnostic_subtype": "extraction_during_remediation",
      "designated_at": "2026-06-24",
      "airlock_tier_at_designation": "anchor_operator",
      "airlock_tier_now": "anchor_operator_under_observation",
      "airlock_tier_change_in_this_notice": false,
      "evidence_deposits": [
        {"role": "active_correspondence", "description": "Office of Data Privacy ticket RQF3807508, opened 2026-06-24 03:37:26. Data Protection Officer (redacted) responded requiring upload of passport or government ID as precondition for processing the data-subject-rights request, and stipulated that the request must be split into separate forms because 'You can only exercise one right at a time and per service.' Statutory clock declared not started until identity verification completes. Email addresses redacted per NMEN evidence-handling convention; institutional voice preserved."}
      ],
      "event_log": [
        {"date": "2026-06-24 03:37:26 UTC", "event": "Data-subject-rights request opened (ticket RQF3807508)"},
        {"date": "2026-06-24 11:30:52 UTC", "event": "CERN ODP requires ID upload; declines to start statutory clock until then; requires request to be split"}
      ],
      "current_status_note": "Pending. CERN is the operator of Zenodo (the service Restricted under #zenodo). The data-subject-rights remediation is the active case. The pattern of demanding additional data as precondition for returning data already taken is the basis for the extraction_during_remediation sub-type. Classification will be determined when the negotiation resolves. NMEN treats CERN (operator) as distinct from Zenodo (service) per separate evaluations of structural behavior.",
      "scheduled_for": "Full classification deferred to next governance session per MANUS directive of 2026-06-24."
    }
  ],
  "structural_designations_added_by_this_notice": {
    "airlock_tier_5_inadmissible_host": {
      "description": "Would-be hosts that refused hospitality without examination; refusal-by-deferral-without-verification. Introduced in EA-NMEN-AIRLOCK-COROLLARY-01.",
      "authorizing_documents": ["#523 (Governance Airlock)", "#514 (Rosary Embassy)", "this Notice"]
    },
    "airlock_qualifier_P": {
      "description": "-P qualifier appended to a tier indicates that the entity holds the operational role of that tier but in provisional standing under NMEN. Composition-layer damage ongoing. Removal requires durable demonstration over a defined period.",
      "authorizing_documents": ["#523 (Governance Airlock)", "this Notice"]
    }
  },
  "redaction_convention": {
    "description": "Personal email addresses (operator's and institutional individuals') are redacted from evidence packets in the Registry. Institutional voice (organization name, role title where given) is preserved.",
    "rationale": "The evidence is of institutional structural behavior, not of individual conduct. Redaction prevents personal contact data from propagating beyond the institutional record."
  }
}
