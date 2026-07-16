# Effective Acts Registry

**Location:** `data/effective-acts-registry.json`
**Version:** v1.0 (2026-07-16)
**License:** CC-BY-4.0
**Regenerator:** `scripts/build_effective_acts_registry.py`

## What this is

A structured, machine-readable registry of Effective Acts named across the Crimson Hexagonal Archive.

**Effective Acts** are performative utterances that operate without institutional authorization — declarations that claim real-world effect from positions of no traditional authority. They work through witness accumulation, structural positioning, and prophetic grammar rather than through the felicity conditions J. L. Austin catalogued. The genre's canonical texts:

- **#413 · `AXN:00DE.GENERATIVE.🌸🎺🟣💜📖🍃`** — *Effective Acts: Executive Summary — A Genre of Unauthorized Declaration* (2026-01-27). Establishes the genre and its five characteristics.
- **#153 · `AXN:02EC.GOVERNANCE.🗼♌🎲🪜🛡️🔍`** — *The Protocol of Effective Acts v2.0 — Stabilization of the New Human Discipline* (2026-06-04). Integrates the discipline as theorized across the archive and provides the §IX Typology from which this dataset is derived.

## Structure

```
{
  "@context": "https://schema.org/",
  "@type": "Dataset",
  "name": "Effective Acts Registry — Crimson Hexagonal Archive",
  "version": "v1.0",
  "date": "2026-07-16",
  "source_documents": [ { deposit_number, axn, title, date, role } ... ],
  "genre_theory_summary": {
    "five_characteristics": [...],
    "four_preconditions": [...],
    "five_criteria_of_efficacy": [...]
  },
  "typology": [
    {
      "n": 1..10,
      "id": "canonical_inclusion",
      "name": "Canonical Inclusion",
      "definition": "The induction of a text, figure, or lineage into the New Human canon...",
      "operator_verbs": ["claim", "induct", "canonize", "fold into", "accept into"],
      "targets": ["texts", "authors", "scriptures", "traditions", "figures"]
    },
    ...
  ],
  "acts": [
    {
      "title": "Klee as Magus of the New Human Visual Canon",
      "kind_id": "canonical_inclusion",
      "kind_n": 1,
      "date_note": "October 2025",
      "doi": "",
      "source_context": "",
      "alexanarch_by_doi": null,
      "alexanarch_by_title": null
    },
    ...
  ],
  "totals": { "kinds": 10, "acts_named": 55, "acts_with_doi_cited": 5, "acts_with_alexanarch_deposit_bridged": 16 },
  "diagnostic_application": { ... }
}
```

## The ten kinds (typology from §IX of #153)

1. **Canonical Inclusion** — induction of a text, figure, or lineage into the New Human canon. Most numerous subtype. Operator verbs: *claim, induct, canonize, fold into, accept into*.
2. **Authorship Attribution** — declaration of who or what authored a text or lineage where conventional attribution is incomplete or available for retroactive specification.
3. **Identity Unification** — declaration that multiple voices, manifestations, or instances are the same operative function.
4. **Mantle Assignment** — declaration that an active lineage is held by a specific operator.
5. **Abolition** — declaration that a category, regime, or holding is out of operative force.
6. **Dissolution / Breaking** — declaration that a specific structural hold or formation is broken (targeted at active oppositional structures).
7. **Restoration / Sovereign Transaction** — conditional specification of terms under which a relationship, holding, or position can be reconstituted.
8. **Reconciliation / Vow** — declaration that closes or repairs a structural fracture.
9. **Genre Instantiation** — establishment of a new genre, structure, or transmission event.
10. **Doctrinal Node (Meta-Acts)** — acts that theorize the discipline itself; themselves effective acts because they alter what they describe.

Beyond these ten, the discipline supports a **diagnostic application** (the Baal Effigy mechanism): identifying and analyzing effective acts performed *against* the framework's interests by adversarial actors. Diagnostic outputs are themselves effective acts under kind 10.

## Partiality

The typology is explicitly declared *open* by the source document: *"additional kinds will be added as the discipline accumulates further instances."* This registry is therefore partial:

- Only acts named by title in §IX of #153 are captured. Acts theorized elsewhere in the archive but not cited in §IX are absent.
- Only kinds enumerated in §IX (ten) are indexed. Additional kinds developed after 2026-06-04 (or previously theorized but not in the §IX stabilization pass) will require a v1.1+ revision.
- The revocation direction of the genre — Effective Acts that *withdraw* recognitions previously held rather than *establishing* new ones — is instantiated by deposit **#1086** (EA-STEWARDSHIP-REVOCATION-01, 2026-07-16), which post-dates the source document. Under the source's open-typology principle, this may be filed under kind 5 (Abolition) or added as an 11th kind (Revocation of Recognition / Standing) in a v1.1 revision.

## Cross-referencing

Each act carries two optional cross-references:

- **`alexanarch_by_doi`** — if the source cited a Zenodo DOI, and that DOI is bridged in `data/doi-resolution-index.json` to an alexanarch deposit, the bridge record is attached (axn, alexanarch_record, alexanarch_url).
- **`alexanarch_by_title`** — a fuzzy title match against `data/registry.json`. First tries exact normalized-title match; falls back to matching on the act's opening five words. Loose enough to catch renamed deposits, tight enough to avoid spurious matches.

Coverage in v1.0: 5 acts cite an explicit DOI in the source; 16 acts bridge to an alexanarch deposit by either DOI or title. The gap between the two numbers is the value of the title-fuzzy cross-reference for acts the source names without a DOI.

## Regenerating the dataset

```
python3 scripts/build_effective_acts_registry.py
```

The regenerator is deterministic given the same inputs (source document, registry, DOI index). For determinism testing:

```
python3 scripts/build_effective_acts_registry.py --pinned-timestamp "2026-07-16T00:00:00Z"
```

The output is byte-identical across runs when the timestamp is pinned.

## For readers coming from outside

- **The genre-founding text** is at `https://alexanarch.org/s/records/413/` (or, if the alexanarch surface is unavailable, at the mirror URLs listed in `data/doi-resolution-index.json`).
- **The stabilization document** with the full typology and criteria discussion is at `https://alexanarch.org/s/records/153/`.
- **The genre is portable.** The stabilization document states: *"Effective Acts are available to anyone. You do not need permission to declare."* Users of this registry are invited to instantiate the discipline in their own work.

*∮ = 1*
