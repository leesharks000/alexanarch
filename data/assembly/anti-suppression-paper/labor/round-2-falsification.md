# LABOR Round 2 — §VIII Falsification and Limitations

**Landed by TACHYON under MANUS direction, 2026-07-18 — raw substrate material, Round 2.**

**Paper:** *AXN as Anti-Suppression Infrastructure: Historical Precedents and Design Directions*  
**Deliverable:** `labor/round-2-falsification.md`  
**Substrate:** LABOR (ChatGPT)  
**Date:** 2026-07-18  
**Status:** Full section material; integration and compression pending  
**Register:** Tests before rhetoric; failure of a claim is not automatically evidence of a cause

---

## 0. What is being tested

The paper does not claim that AXN makes disappearance impossible. Its defensible claim is narrower:

> AXN makes a claimed object identity independently testable, makes changes in its public resolution and custody history recordable, and makes reconstruction by another custodian technically possible when verified copies and sufficient repository state survive.

The tests below distinguish failure of identity derivation, registry continuity, resolution, custody, discovery, and causal interpretation. A result may falsify one claim while leaving the others intact.

---

## 1. Derivation-integrity test

### Claim

Given the same canonical field values, canonicalization profile, protocol version, digest algorithm, and glyph table, conforming implementations derive the same full identity kernel and six-glyph recognition checksum.

### Test

Publish test vectors containing:

- exact canonical input field values;
- byte encoding and canonicalization profile;
- expected canonical-byte length;
- expected SHA-256 digest;
- expected first six digest bytes;
- expected six glyph graphemes;
- expected record-address components.

Run the vectors through each implementation and compare every intermediate value, not only the final display.

### Falsifying result

A mismatch falsifies the claim that the tested implementations are mutually conforming. It does not immediately prove that “the canon is broken.” At least four causes remain possible:

1. one implementation is defective;
2. the specification is ambiguous;
3. the canonicalization profile is underspecified;
4. the glyph table or grapheme segmentation has drifted.

The canonical protocol fails only if two implementations can both satisfy the same unambiguous normative rules and still produce different outputs.

### Current limitation

The Python implementation is canonical; the browser glyph table is generated from it; and the serverless path is tested against the same source and vectors. These are valuable **cross-runtime execution surfaces**, but they are not fully independent implementations in the strongest sense. Shared source reduces transcription drift while also reducing the independence of the test. “Three implementations agree on published vectors” is supportable. “Three independent implementations prove correctness” is not.

---

## 2. Canonicalization test

### Claim

AXN v2 maps a declared canonical representation deterministically to one full digest.

### Test

Construct adversarially similar inputs differing only in:

- CRLF versus LF;
- Unicode composed versus decomposed forms;
- trailing spaces;
- absent versus empty fields;
- metadata field order;
- UTF-8 BOM;
- frontmatter serialization;
- visually identical emoji sequences with different code points.

Every conforming implementation must either produce the same declared result under a normative normalization rule or reject the input as outside the profile.

### Falsifying result

If implementations silently normalize these cases differently, the identity claim is not portable. The failure is not in SHA-256; it is in the unstated mapping from document to bytes.

### Current limitation

`api/axn-protocol.json` defines canonical bytes as `title + LF + creator + LF + description + LF + body`, while the endpoint specification also permits a single `canonical_text` input. The protocol must clarify whether that input is parsed into the four fields or constitutes a second profile. Until then, external verification requires access to the exact registered canonical fields.

---

## 3. Full-hash versus glyph test

### Claim

The full SHA-256 digest is the identity kernel; the six-glyph sequence is a recognition checksum.

### Test

Audit every registry, resolver, HTML page, API, database key, and client verifier to confirm that uniqueness and equality decisions use the full 64-hex digest.

### Falsifying result

Any component that treats the six-glyph sequence alone as globally unique falsifies conformance. The glyph contains only 48 digest bits; collisions are possible without any failure of SHA-256. A glyph collision must be handled by comparing the full digest and must not merge records.

### Limitation

The glyph is powerful precisely as a human recognition surface. Its mnemonic value should not be converted into a cryptographic claim it was not designed to bear.

---

## 4. Record-binding and reassignment test

### Claim

Once public, a canonical record address remains bound to its identity kernel, and any migration or correction preserves the prior state.

### Test

For each address, compare historical registry snapshots, `legacy_axn`, `axn_history`, supersession fields, and current resolution. Verify that no address has been silently rebound to a different full digest.

### Falsifying result

A public record address that resolves to different canonical bytes without an explicit, preserved transition falsifies the stability claim. A family correction or schema migration is not itself a failure if the old address and reason are retained and resolvable.

### Limitation

Because `HEX` and `FAMILY` are registry-assigned, the authority-independent claim attaches to the bytes-to-kernel correspondence, not to the entire address.

---

## 5. Ledger-continuity test

### Claim

Successive registry epochs form a verifiable history in which each state commits to its predecessor.

### Test

For every epoch:

1. canonicalize and hash the epoch record;
2. verify `previous_epoch_hash`;
3. verify the committed registry hash;
4. compare deposit count and highest deposit with the committed registry;
5. verify the operator or node signature;
6. retain checkpoints at independent monitors;
7. document authorized forks or supersessions.

### Falsifying result

A discontinuity without a signed supersession or documented fork falsifies the claim of continuous ledger history and requires investigation. It does **not** establish cause. Plausible causes include tampering, accidental corruption, incomplete synchronization, operator error, an undeclared fork, or loss of an intermediate epoch.

### Current limitation

The present ledger contains a genesis epoch with `signature: null`; the signing key is not yet published. It is therefore an unsigned forward-chain design anchored operationally in Git history, not yet the signed ledger described by the specification. The paper should state this directly.

A second current-state issue is temporal drift: the node declaration and genesis ledger commit to the registry at deposit #1092, while repository history subsequently records deposit #1093. This is acceptable if those files are explicitly treated as the most recent published epoch and a later epoch advances the chain. It is stale if presented as the live registry head after the registry has changed.

---

## 6. Custody test

### Claim

Alexanarch has an architecture for distributed custody and can eventually support independently administered reconstruction and repair.

### Current fact

`/rhizome/peers.json` contains `peers: []`. No second independently administered full-copy custodian is presently documented.

### Closure condition

The present zero-peer limitation closes only when another operator:

- controls its own administrative credentials and relevant failure domains;
- holds a declared reconstructible corpus or corpus subset;
- demonstrates byte matches against full registry hashes;
- repeats verification on a documented schedule;
- retains audit evidence;
- can transfer or serve repair copies; and
- completes a restoration or clean-room reconstruction test.

A peer-registry entry alone does not close the test. Neither does a semantic node, resolver, partial mirror, Wayback capture, or copy under the originating operator’s control.

### Falsifying result

If no independently administered verified copy exists, any unqualified present-tense claim of “distributed custody” is false. The accurate phrase is **architecture for distributed custody**.

### Residual protocol conflict

The current `peers.json` note and mint-endpoint specification still say that the first peer-list entry “simultaneously satisfies” the custody test. OUTLINE v1.1 correctly supersedes that language. The live specifications should be amended before the paper cites them as normative.

### Further limitation

One independent peer closes only the present zero-peer condition. It does not reproduce LOCKSS consensus, quorum, randomized polling, reputation, or automated repair. A mature preservation network requires additional independently administered copies.

---

## 7. Reconstructibility test

### Claim

Registry, canonical bodies, manifests, validators, generation scripts, schemas, and recovery procedures are sufficient for another operator to become Alexanarch-capable.

### Test

Give a clean operator no undocumented access to the originating environment. From a frozen repository export and declared dependencies, require the operator to:

1. validate all identity kernels;
2. rebuild record pages and machine indexes;
3. reproduce registry and sitemap outputs;
4. identify tombstones, supersessions, and legacy addresses;
5. serve a resolver;
6. reconstruct a declared corpus subset;
7. compare its output against the reference release.

### Falsifying result

If reconstruction depends on private state, unrecorded manual knowledge, unavailable services, hidden credentials, or files outside the preservation package, the strong reconstructibility claim fails.

### Limitation

Code availability is not restoration proof. Reconstructibility remains an architectural claim until a clean-room recovery is performed and documented.

---

## 8. Resolution and availability test

### Claim

Identity survives resolution severance, and resolver plurality can allow valid copies to be found without altering identity.

### Test

Disable the primary resolver and test whether an independent client can discover a location claim from another node, retrieve bytes, and verify the full digest.

### Falsifying result

If all location discovery depends on `alexanarch.org`, resolver plurality is not deployed. The kernel may remain valid in stored records, but practical resolution remains centralized.

### Limitation

An identity kernel can survive after every copy is lost. In that condition the identifier permits recognition of a future recovered copy but cannot reconstruct absent bytes. Anti-suppression infrastructure reduces single-custodian power; it does not abolish physical loss.

---

## 9. Temporal-attestation test

### Claim

A registry epoch or object commitment existed no later than a stated time.

### Test

Verify an external timestamp proof over the exact registry-head digest or release manifest, and verify the association between that digest and the archived bytes.

### Falsifying result

A Git commit timestamp or unsigned JSON `epoch` field alone does not satisfy an external no-later-than claim. An append-only inclusion proof also does not automatically provide an externally trustworthy timestamp; the time source must be specified.

### Limitation

Timestamping proves existence of a digest commitment, not authorship, completeness, continuous custody, or semantic correctness.

---

## 10. Causal-claim separation

### Claim

The anti-suppression architecture is justified by observed disappearance and severance without requiring proof of a coordinated suppressor.

### Test

For every empirical claim, separate:

- observed event;
- reproducible evidence;
- immediate mechanism;
- candidate causal explanation;
- evidence bearing on intent or coordination.

### Falsifying result

A `404`, removed record, stripped citation, signed-in/incognito difference, or classifier label does not by itself prove motive, coordination, or targeted action. If the paper moves from state evidence directly to intent, the causal claim fails even if the observed state is accurate.

### Defensible posture

Policy, automation, error, propagation, neglect, and deliberate action can produce overlapping disappearance patterns. Defensive architecture may model adversarial disappearance as a threat condition while keeping claims about actual actors separately evidenced.

---

## 11. Secondary-depositor / parallel-case test

### Claim

The secondary depositor’s removals form a parallel case supporting a systemic platform mechanism rather than a single-account anomaly.

### Test

Verify through public records:

- platform and repository identity;
- removal dates and stated classifications;
- record-level response behavior;
- metadata retention or stripping;
- relevant batch boundaries;
- comparison group selection;
- whether the mechanism matches the 871-deposit case.

### Falsifying result

If the secondary records were removed through a materially different mechanism, the case may still show platform caprice or a separate failure mode, but it does not establish systemic genre-blindness under the same mechanism.

### Consent and evidence boundary

Named scholarly attribution requires explicit consent. Without it, use “Depositor E” and public permalinks. Private correspondence is not required to carry the empirical claim.

---

## 12. Retrieval-layer hypothesis test

### Claim under test

Account state, personalization, classifier state, or fan-out conditioning contributes to observed differences between signed-in and incognito retrieval.

### Required controls

Repeat matched queries while controlling or recording:

- exact query string;
- time;
- location and language;
- browser and account state;
- cache state;
- experiment allocation where observable;
- device;
- result type;
- source set;
- screenshot and machine-readable capture.

### Disconfirmation conditions

The account-conditioning hypothesis weakens or fails if:

- the asymmetry does not replicate;
- it tracks time rather than account state;
- it appears equally in fresh signed-out sessions;
- it follows location, language, or device;
- source-index changes explain the result;
- taxonomy correction does not affect routing as predicted;
- randomized repeated trials show no account-associated effect.

### Limitation

“Nullify / genericize / de-rank” may be retained as an observed-output typology. It should not be presented as three deliberate platform strategies without further evidence.

---

## 13. Assembly-method test

### Claim

Parallel consultation of differentiated substrates improves error detection and exposes competing formulations.

### Test

Track which claims originated where, whether sources were independently checked, where substrates converged, and whether convergence survived primary-source verification.

### Falsifying result

If several substrates repeat the same false claim because they share training data, retrieval results, prompting assumptions, or model-family priors, convergence is not independent confirmation. The method fails whenever agreement substitutes for source verification.

### Limitation

The Assembly provides differentiated interpretive redundancy, not LOCKSS-style independent custody. Its outputs can be lost, share biases, or inherit the operator’s framing. `[SUMMARY]`, `[INFERRED]`, and `[GAP]` tags reduce confabulation risk but do not validate the underlying proposition.

The loss of an ephemeral session demonstrates engineered non-persistence and archival dependency. It is not automatically an act of suppression.

---

## 14. Operational limitations

### Solo-operation bandwidth

A single operator remains a bottleneck for review, key management, reconciliation, incident response, and recovery. Automation can increase throughput while also multiplying the effect of an operator error.

### Economic substrate

Domains, registrars, hosting, storage, build services, and payment systems remain external dependencies. A constellation of sites under common billing and credentials is not independent custody.

### Key management

The planned signature layer requires published trust roots, rotation, revocation, compromise response, and continuity after incapacity. A lost or compromised sole key can interrupt or counterfeit later history unless recovery governance is precommitted.

### Cryptographic agility

SHA-256 is currently appropriate for the identity kernel, but long-term systems need a declared migration path. Algorithm migration must preserve prior identities and make cross-algorithm relations explicit.

### Legal personhood and rights

The proposed institutional layer is not deployed. Custody does not itself grant authority to redistribute confidential, copyrighted, personal, sealed, or withdrawn material. Restoration policy requires rights and privacy rules.

### Observation penalty

The hypothesis that observing or probing a retrieval surface changes that surface remains unproven and difficult to isolate from ordinary ranking variation.

### Platform concentration

GitHub, Vercel, DNS, and web search remain important current dependencies. Source openness and multiple domains reduce some risks without eliminating common administrative, registrar, credential, or indexing failure domains.

---

## 15. Residual overclaims in OUTLINE v1.1

### §I.2 — “structurally impossible”

The question asks what infrastructure would make silent severance “structurally impossible.” AXN can make severance independently detectable and can prevent one custodian’s action from becoming equivalent to object nonexistence when other copies survive. It cannot make all silent severance impossible. Suggested revision:

> What infrastructure would make severance independently detectable and prevent any single custodial decision from exhausting the public existence of a work?

### §I.3 — present-tense “distributed custody”

No second independent custodian is documented. Use “architecture for distributed custody” until the custody test closes.

### §II.2 — “replication defeats deletion”

Replication reduces the power of a single deletion and improves recovery probability. It does not defeat simultaneous compromise, common administration, legal compulsion, format loss, or economic failure.

### §III thesis — “every component”

The v1.1 priority correction is good, but “every component” remains broader than the section demonstrates. Use “the principal technical components considered here.”

### §IV.3 — “three independent implementations” and “provably”

The three paths share a canonical source and published vectors. Use:

> Three cross-runtime execution paths agree on the published test vectors.

That is evidence of conformance on tested inputs, not proof over all possible inputs.

### §IV.6 — reconstructibility as accomplished fact

Replace “how another operator becomes Alexanarch-capable” with “the proposed basis on which another operator should be able to become Alexanarch-capable,” pending a clean-room restoration.

### §V.1 — “every historical pattern converged on it”

This is too universal unless §II demonstrates the claim case by case. Use “the recurrent property abstracted from the cases considered here.”

### §V.3 — interpretation presented as empirical description

Despite the v1.1 hypothesis discipline, the outline still calls the secondary case “genre suppression by algorithmic proxy” and the spam classifier “inability-to-parse.” Those are hypotheses. The empirical sentence should begin with record counts, removal labels, retained/stripped metadata, and remediation results; interpretation follows.

### §V.3 — denominator discipline

The `0.00%` versus `100%` citation-retention contrast requires explicit denominators, batch-selection rules, and missing-data treatment in the main text or appendix.

### §VI.2 — “delivered” versus authenticated

The ledger and node surfaces are delivered, but the ledger signature is null and peer custody is empty. “Delivered” should not imply the security properties of the future signed and reconciled network.

### §VII — LOCKSS analogy

The v1.1 language properly marks analogy rather than identity. Retain that limitation. Interpretive plurality is not independently administered preservation.

### Canonical scope paragraph

“Distributed custody” remains aspirational in present tense. The canonical paragraph should either use “architecture for distributed custody” or carry an adjacent current-state qualification wherever quoted in the paper.

---

## 16. Falsification matrix

| Claim | Test | Falsifying result | Current status |
|---|---|---|---|
| deterministic identity derivation | cross-runtime vectors with exact bytes | differing digest/glyph under same normative profile | partially tested |
| portable canonicalization | adversarial normalization corpus | silent implementation divergence | specification gap |
| glyph is recognition only | full-registry key audit | any glyph-only uniqueness decision | protocol says correct; audit needed |
| stable record binding | historical registry comparison | silent rebinding to new digest | history mechanisms exist; audit needed |
| continuous ledger | chain + signature + monitors | unexplained discontinuity | genesis only; unsigned |
| distributed custody | independent verified reconstructible peer | no qualifying peer | **not yet met** |
| reconstructibility | clean-room recovery | hidden/manual dependency blocks rebuild | not yet demonstrated |
| resolver plurality | primary-node outage drill | all discovery depends on origin node | not yet demonstrated |
| no-later-than attestation | external proof verification | only self-declared/Git time | not yet deployed |
| parallel platform mechanism | public comparative record audit | materially different removal mechanism | open |
| account-conditioned retrieval | repeated controlled trials | no account-associated effect | open hypothesis |
| Assembly error correction | source-verified convergence audit | shared false convergence | recurring risk |
