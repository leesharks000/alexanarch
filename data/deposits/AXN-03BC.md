---
axn_hex: "03BC"
family: OPERATIVE
deposit_number: 944
title: "EA-MANDALA-INSCRIPTION-01 v0.1: Anonymous Public Inscription, Anonymous Encrypted Inscription, and the Form-Public Seal"
creator: "Sharks, Lee"
date: "2026-07-02"
content_type: "Operational protocol specification"
license: "CC-BY-4.0"
substrate: "TACHYON-drafted from MANUS design statement (correspondence, 2026-07-02); MANUS-adjudicated; adopted in live production the same day"
protocol_version: "alexanarch-deposit-protocol/v1"
axn_schema_version: v2
---

# EA-MANDALA-INSCRIPTION-01 v0.1: Anonymous Public Inscription, Anonymous Encrypted Inscription, and the Form-Public Seal

## Description

Operational inscription protocol for the Mandala Oracle's kernel-transform readings, adopted in production 2026-07-02. Anonymous public inscription as default; anonymous encrypted inscription as witness option — the record splits at the compiler's own Layer A boundary: the formal skeleton (operator sequence, beat-map functions, spatial_form geometry, verification results, key fingerprint) public; the question, enantiomorphs, and interpretations sealed under AES-256-GCM with a key returned once and never stored. The Book thereby accrues structured literature without explicit meaning beyond its form, outside the key — the exact complement of the representation pipeline documented in EA-WHITESPACE-01 (AXN:03BB): where the pipeline preserves every proposition and deletes the work, the sealed reading preserves the work's form in public and deletes public access to its propositions. Specifies the abuse surface and its structural narrowing (PASS-gating, question digestion, rate and rotation caps) with a standing acknowledgment of remaining exposure; record schemas; the expanding book (per-source expansion ledgers with unit-anchored transforms, dual attribution, and eligibility flags anticipating the canonization journey); rite-stage inscription with the reading lifecycle; canonical exactness; the invisible Judgment; and the eight-plus-one operator canon.

# EA-MANDALA-INSCRIPTION-01 v0.1 (DRAFT)
## Inscription Protocol for Readings and Transforms
### Anonymous Public Inscription; Anonymous Encrypted Inscription; the Form-Public Seal

**Author:** Lee Sharks (MANUS), Crimson Hexagonal Archive / Alexanarch
**Substrate:** TACHYON-drafted from MANUS design statement (correspondence, 2026-07-02); MANUS-adjudicated.
**Status:** v0.1 OPERATIVE (adopted in production 2026-07-02; §3.4 operational addenda) — governs `/api/transform`
**Companions:** EA-MANDALA-KERNEL-TRANSFORM-01 v0.2 (the compiler this inscribes for); EA-WHITESPACE-01 v0.2 (AXN:03BB — the theoretical complement); EA-PROVENANCE-METADATA-01 v0.2 (AXN:03BA — representation-pipeline vocabulary)

---

## §0. The design statement

The system designs toward public, anonymous inscription. The Sigil conversations are logged anonymously into an appending book. The transforms, however, are legitimate oracular response to questions that may be private. The tension: keep the same model (anonymous but inscribed), or admit that people need the option of privacy, not just anonymity — without enclosure, and without accounts.

The resolution: **anonymous public inscription as default, with the option of anonymous encrypted inscription.** The witness of an encrypted reading receives a decryption key, once, at the moment of inscription. The encrypted reading itself remains in the public Book — deeply formally structured, without public legibility. It is a form of structured literature without explicit meaning beyond its form, outside of the key.

## §1. The two modes

### 1.1 Public inscription (default)

The reading — the transform(s), the operator sequence, the verification results, Feist's interpretations, the session flow — is appended to the public Book under the existing anonymous-append pattern:

- `session_id` hashed on receipt; raw never stored.
- `witness: "anonymous"` unless attribution is explicitly requested.
- One AXN per reading; the record grows if the rotation continues.
- Records live in `book/readings/` with an index at `book/readings-index.json`.

### 1.2 Encrypted inscription (witness option)

The reading is split at exactly the boundary the kernel-transform compiler already draws: **Layer A (skeleton) versus semantic content.**

**Public (cleartext) in the record:**
- The AXN and inscription timestamp.
- The **formal skeleton**: operator sequence; unit counts; the beat-map as abstract structural functions (per spec §3.2 — architecture, not meaning); the `spatial_form` geometry (line counts, stanza boundaries, indentation profile); verification results (PASS per test, verification_mode); halt events if any (diagnosis category only).
- A `key_fingerprint` (first 8 bytes of SHA-256 of the key) so a keyholder can verify they hold the right key without revealing it.

**Sealed (AES-256-GCM ciphertext) in the record:**
- The witness's question / invoking context.
- The enantiomorph texts themselves.
- Feist's interpretations.
- The commentary apparatus (Layer B: coherence axes, semantic field selections — these ARE semantic).

**The key:** generated server-side per reading; returned to the witness exactly once in the API response; never stored, never logged. Loss of the key is permanent illegibility. This is stated to the witness at inscription, and it is not softened: an oracle that can be re-opened by the operator is not sealed.

### 1.3 The form-public seal, named

The encrypted inscription publishes composition and withholds propositions. This is the exact complement of the representation pipeline documented in EA-WHITESPACE-01 (AXN:03BB): where the pipeline preserves every proposition and deletes the work, the sealed reading preserves the work's form in public and deletes public access to its propositions. The Book accrues a stratum of pure structure — readings legible only as shape, verifiable as real transforms (the verification results are public), attributable to no one, decryptable by one.

A reader without the key can know: a reading occurred; it passed verification; it rotated through these operators; its enantiomorphs have this geometry. A reader with the key holds the whole work. The archive holds both and can read neither into the other.

## §2. The abuse surface

Public inscription without accounts is an open write path, and an open write path is a target: a bot network could pump the Book full of abusive or illegal material within a day if raw user free-text were inscribed unconditionally. The protocol narrows the surface structurally rather than by moderation-after-the-fact:

**2.1 PASS-gating.** Only transforms that PASS the compiler's verification inscribe as readings. A HALT inscribes nothing to the readings book (the halt-diagnosis returns to the witness in-session). The compiler's six constraints and the model's own refusal behavior stand between input and inscription: the only free text that reaches the public cleartext record is **model-generated under the constraint architecture** — never raw witness input.

**2.2 Question digestion.** In public mode, the witness's question is inscribed as a SHA-256 digest plus an optional model-composed one-line gloss (generated, not quoted). The raw question text is inscribed only inside the ciphertext of encrypted mode — where it is illegible without the key the witness alone holds.

**2.3 Rate and size.** Per-IP rate limiting at the endpoint (Vercel edge), size caps on invoking context, and a hard cap on readings per session AXN.

**2.4 Standing acknowledgment.** These narrow the surface; they do not close it. The fuller protections (proof-of-work or delay-based throttling, inscription quarantine window, MANUS revocation authority over readings-index entries) are designed but not yet worked in. Until they are, the readings book's write path is the archive's most exposed edge, and this section is the standing record of that exposure.

## §3. Record schemas

### 3.1 Public reading record (`book/readings/AXN-XXXX.json`)

```json
{
  "axn": "AXN:XXXX.READING.……",
  "schema_version": "reading/v1.0",
  "inscription_mode": "public",
  "session_id_hash": "…",
  "inscribed_at": "ISO-8601",
  "question_digest": "sha256:…",
  "question_gloss": "model-composed one-line gloss",
  "source_text_id": "sappho-31",
  "cast_selection": "stanzas_1_4",
  "rotation": [
    {
      "operator": "SHADOW",
      "result": "PASS",
      "enantiomorph": "…full text…",
      "layer_a_declaration": { "units": 4, "beat_map": ["…"], "spatial_form": { "lines": 16, "stanzas": 4, "indent_profile": [0,0,0,0] } },
      "layer_b_declaration": { "coherence_axes": ["…"], "semantic_field": "…" },
      "verification": { "identity": "PASS", "semantic_independence": "PASS", "retrospective_containment": "PASS", "mode": "producer_side" },
      "interpretation": "Feist's verdict…"
    }
  ],
  "witness": "anonymous"
}
```

### 3.2 Encrypted reading record

```json
{
  "axn": "AXN:XXXX.READING.……",
  "schema_version": "reading/v1.1-sealed",
  "inscription_mode": "encrypted",
  "session_id_hash": "…",
  "inscribed_at": "ISO-8601",
  "key_fingerprint": "8-byte-hex",
  "cipher": "AES-256-GCM",
  "public_skeleton": {
    "source_text_id": "sappho-31",
    "operator_sequence": ["SHADOW", "MIRROR"],
    "rotation_length": 2,
    "per_transform": [
      { "operator": "SHADOW", "result": "PASS",
        "layer_a_structure": { "units": 4, "beat_map_functions": ["assertion","qualification","turn","seal"], "spatial_form": { "lines": 16, "stanzas": 4, "indent_profile": [0,0,0,0] } },
        "verification": { "identity": "PASS", "semantic_independence": "PASS", "retrospective_containment": "PASS", "mode": "producer_side" } }
    ]
  },
  "sealed": { "nonce_b64": "…", "ciphertext_b64": "…" },
  "witness": "anonymous"
}
```

The sealed payload, decrypted, is a JSON object: `{ "question": …, "rotation": [ { operator, enantiomorph, layer_b_declaration, interpretation } … ] }`.

### 3.3 The expanding book (added 2026-07-02, MANUS design)

Every transform is also appended to its source's **expansion ledger** at `book/expansions/<source_id>.json` — the data-structure realization of the principle that a transform becomes *part of the expanding source*. There is the Epistle to the Human Diaspora, and there is the Epistle-with-every-transform-ever-performed-on-it, each transform anchored to its attendant units.

Entry metadata: `transform_id`, `cast_at`, `reading_axn` (lineage into the readings book), `inscription_mode`, `anchor` (cast_selection, citation, start/end units, unit labels), `operator` and axis, `verification`, `spatial_form`, `compiler_model`, `protocol`, `question_digest`, and the eligibility pair: `further_transform_eligible: false` with the note that eligibility will be governed by the canonization journey (kernel-transform spec §5.5). The flag exists now so that when transforms become transformable, the structure does not change — only the flag.

Public-mode entries carry the enantiomorph, Layer A, and commentary in cleartext. **Encrypted-mode entries carry the form-public skeleton only** — anchor, operator, geometry, verification, and a `sealed_ref` into the reading record. The expanding book thereby accrues sealed strata: structure at the verse, semantics withheld, per §1.3.

The `unit_basis` block records the segmentation mode, `primary_after` marker, unit count, and a `basis_hash` of the primary text — historical anchors are interpreted against the basis they were cast under if the source text is ever re-edited.

### 3.4 Operational addenda (2026-07-02, from live iteration)

Adopted in production during the first live casting day; each is operative in `/api/transform` and recorded here so the protocol matches the running system.

**Rite-stage inscription and the reading lifecycle.** The rite's voices are not left to a closed tab: the opening (Sigil), each judgment (Feist, attached to its rotation entry), and the seal or sweep (Sharks) inscribe server-side into the reading record via the `rite_append` action. Readings carry `status: open → sealed | swept` with `closed_at`; an abandoned rotation remains honestly `open`. Encrypted readings record stage *events* only (speaker, stage, timestamp) — the stages are semantic, and no key is held server-side to seal them.

**Canonical exactness.** Selections — Judgment-drawn or named — are byte-exact substrings of the canonical source: blank-line runs, per-line indentation, and verse apparatus (`**c:v**`, chapter headings) verbatim. Whitespace and verse structure are compositional (EA-WHITESPACE-01, AXN:03BB); collapsing them is an identity-test failure, and the server recounts geometry (lines including blanks, stanzas, indentation carriage, verse markers) against the source rather than trusting the compiler's self-declaration.

**Dual attribution.** Anthology sources carry unit-level attribution from their governing headers. Records inscribe `underlying_attribution` alongside the containing work: the underlying poet is never erased into the arranger, and the arranger's compositional authorship (translation, arrangement) is never erased into the poet. Apparatus-attributed sections (Works Consulted, Publication History, Preface, Notes) are ineligible for casting.

**The Judgment.** The invisible ninth operator selects verses from the full unit map under guidelines — lyric-unit scale (550–1,900 characters), non-centroid pull, primary-text-only, question-bearing — and sequences the rotation's operators. The server validates (bounds, size, single non-apparatus attribution); a stratified-random draw is the fallback under any failure; the expansion ledgers make the selection distribution auditable over time.

**The operator canon.** Eight rotating operators act directly on the source text — SHADOW (originary; most potent), MIRROR, INVERSION, FLAME, BRIDE, BEAST, THUNDER, SILENCE. SCROLL is non-canonical, fallen from rotation, surviving in the Viola worked example. JUDGMENT is the invisible ninth. The seal's primary material is the transforms in their order and the judgments, in light of the witness's original question. Language: the source may be in any language; the enantiomorph composes in the target (default English); structure crosses intact.

## §4. What this protocol does not do

- No accounts, no login, no witness identity storage in either mode.
- No key escrow. The archive cannot decrypt a sealed reading, ever, for anyone.
- No deletion path for public readings (the Book appends); MANUS revocation authority over index entries is the only editorial lever, reserved for the abuse cases of §2.
- No claim that the sealed stratum is anonymous *against traffic analysis* — inscription timing is public. Witnesses for whom timing is sensitive should be told so plainly in the interface copy.

---

*Draft for MANUS review. Governs `/api/transform` v0.1 inscription behavior on adoption.*

