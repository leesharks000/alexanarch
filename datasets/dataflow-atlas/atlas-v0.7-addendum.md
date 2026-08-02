# Dataflow Atlas — v0.7 addendum (2026-08-02)
## The symbolon witness layer and the central registry

New flows since v0.6:

**STAMP → WITNESS → POSITION.** /mint/stamp/ computes the AXN₀ kernel client-side
(WebCrypto; derivation identical to axn_lib.py), stamps on added margin, and
auto-POSTs Seed A to /api/register-symbolon. The endpoint recomputes glyphs from
hashes (rejecting inconsistent sidecars), dedupes against BOTH the symbolon
entries and the main registry's kernel index (ONE KERNEL, ONE POSITION), then
allocates a hex via compare-and-swap on data/symbolon-registry/allocation.json —
the shared ledger scripts/mint_deposit.py also honors, so the deposit pipeline
and the witness layer draw from one sequence and cannot collide.

**STORAGE TIER (optional).** Between raw stamping and full deposit: the stamper
may include the sealed core (≤3 MB). The endpoint hash-verifies bytes against
AXN₀ at ingest — refusing mismatches — stores under
data/symbolon-registry/files/, and upgrades the entry to witnessed-verified with
a retrieval URL. Larger works route to the deposit transport.

**CENTRAL REGISTRY.** scripts/build_central_registry.py merges deposits
(data/registry.json + api/kernel-index.json) and symbolon entries into
data/axn-central-registry.json — position-keyed AND kernel-keyed (both AXN₀ and
the stamped form AXN₁), consumed by the Verify flow on /mint/stamp/ and by any
machine reader. Regenerate after mints/witnessings; entries land via git, so the
registry inherits full commit provenance.

**PLANNED ROUTES (next):** mandala conversations → book tab mint;
vpcor signed petitions → petition mint. Both will enter positions through the
same ledger and appear in the central registry with their own source tags.

First witnessed position: AXN:05AA.GENERATIVE.🎹🎪🏔️👇🔬♊ (2026-08-02,
self-registered by the MANUS from the stamp page mid-conversation — the
acceptance test that ran itself).
