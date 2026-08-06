# Dataflow Atlas — v1.0 addendum (2026-08-06)
## The second stamper, the namespace move, and the instruments that watch the map

**Supplements:** atlas v0.2 + addenda v0.3–v0.9. This addendum is larger than its
predecessors because a single day changed the network's shape three times: a
publication-layer outage moved 1,012 files, a second mint surface appeared on a
different origin, and three new gates were installed to keep the map honest.

**Standing rule this addendum enforces:** *the atlas is the map of data flows and
must remain current.* A second stamper existed for hours before it appeared here.
That gap is the same class as PATHOLOGY-01 — a description true once — and the
correction is that a new mint route, surface, or endpoint is not finished until
the atlas carries it.

---

## §1 · PUBLICATION NAMESPACE MOVE — `/api/` → `/data/api/`

**Class:** PUBLICATION.namespace-collision · **Severity:** was critical, now closed

The root `api/` directory is Vercel's Functions namespace. Non-executable files
placed there are not published; they 404 with an HTML error page while remaining
perfectly correct in git. Commit `fd8de940` (2026-07-31T03:20:21Z) added one file
— `api/oai.js` — and converted the directory. **1,012 static JSON files went dark
instantly** and stayed dark for six days.

**What was invisible:** `/api/index.json` (the protocol catalog `DEPOSIT-FLOW.md`
declares authoritative), `/api/deposit-protocol.json` and `/api/schemas/*` (the
deposit contract itself), `/api/doi-axn-map.json` (the resolver map standing in
for 1,817 severed DOIs), `/api/axn-index.json`, `/api/search-index.json` and 996
body shards.

**Why no instrument caught it:** every validator read from **disk**, where the
bytes were flawless. `validate_deposit.py` and `bootstrap_familiarization.py`
verified sha256 happily; `deposit_pipeline stage_verify` probed record pages and
PDFs only. **Nothing fetched a URL.** Two commits in the window even wrote
updates into `doi-axn-map.json` — the archive maintaining a file no reader could
fetch.

**New flow.** Static JSON now lives at `data/api/`. `vercel.json` rewrites
`/api/(.*)\.json` → `/data/api/$1.json`, so every advertised URL and all 3,412
HTML surfaces are unchanged. `api/` holds executables only: `oai.js`,
`register-symbolon.js`.

> **DOCTRINE:** `api/` means executable request handlers. `data/` means static,
> cacheable, downloadable archive data. **Local validity and published
> availability are different properties**, and until today the archive had rich
> instrumentation for the first and none for the second.

---

## §2 · SECOND MINT SURFACE — `axnidentifiers.org/stamp/`

**Class:** MINT.route (new) · **Authority relation:** derived; alexanarch remains registry

A second stamper now exists on a **different origin** from the registry. This is
the first cross-origin mint route in the network and the atlas must carry it.

```
axnidentifiers.org/stamp/            alexanarch.org
  ├─ assets/axn-node.js  ──── reads ──→ /data/axn-central-registry.json   (CORS *)
  │    node manifest, tried in turn
  ├─ WebCrypto SHA-256   ── local ───→  (no network; the kernel needs none)
  ├─ Seed A sidecar      ── local ───→  download
  └─ registration        ──POST ─────→ /api/register-symbolon            (CORS *)
                                          ↓
                                     data/symbolon-registry/entries/*.json
                                          ↓ (git)
                                     build_central_registry.py → central registry
```

**The wiring was already in place and undocumented.** `register-symbolon.js`
answers preflight with `Access-Control-Allow-Origin: *`, `Allow-Methods: POST,
OPTIONS`, `Allow-Headers: Content-Type`; every `/data/*.json` carries `ACAO: *`.
The endpoint was built to be stamped against from elsewhere — the atlas simply
never said so.

**Node-agnostic by construction.** `assets/axn-node.js` declares a node list,
tries each in turn for lookup and registration, **names the node that answered**
beside every result, and degrades to kernel-plus-sidecar when none answers.
An unreachable registry costs an address, not an identity; a failed lookup
returns a **lacuna**, not an error.

**Consequences for the map.** Positions can now be allocated by a request
originating on an origin the archive does not serve. The one-kernel-one-position
invariant still holds — it is enforced at the allocation gate inside the
endpoint, which is the only place it can be — but *the atlas can no longer assume
mint requests originate at alexanarch.*

**Adjacent surface:** `axnidentifiers.org/constitution/` mirrors the canonical
governance text and **verifies itself against source on every visit**, reporting
divergence in place. A mirror that cannot be checked is not a mirror.

---

## §3 · CHIASTIC INSCRIPTION — the stamp flow gains a third pass

**Class:** MINT.flow (amended) · **Status:** proposed v0.3, ratified 2026-08-06

Until now the stamp band could not carry its own registered address, because
stamping precedes registration. The result: **the addressed thing did not travel
and the traveling thing was not addressed.**

```
PASS 1  STAMP      original bytes → AXN₀ kernel → band(kernel)      [offline-capable]
PASS 2  REGISTER   Seed A → node → AXN:HEX.FAMILY.⟨glyphs⟩          [any node]
PASS 3  RE-STAMP   original bytes → band(FULL AXN + kernel)         [optional, idempotent]

STORED  : the sealed core — original bytes, kernel, NO address   (it IS the referent)
TRAVELS : the stamped copy — original + margin, WITH address     (it must be findable)
```

**Why inscribing the address is not circular:** a kernel cannot be inscribed in
the bytes it measures, but an address does not measure. Hex and family are
*assigned* at the registry, not *derived* from the stamped bytes. AXN₁ still
lives only in Seed A, exactly as SPEC §4 requires.

**Data-integrity constraints, binding:**
- Sealed cores are **never** re-stamped. Storage holds original bytes, always.
- Pass 3 is **additive**: `stamp_generation: 1` entries remain valid and resolvable.
- Re-stamping refreshes AXN₁ and appends to `stamp_history`; AXN₀ is untouched.
- The endpoint's existing `SYMBOLON RE-STAMP` path already implements this.

---

## §4 · INSTRUMENTS THAT WATCH THE MAP (new)

| Instrument | Watches | Gate |
|---|---|---|
| `audit_static_namespace.py` | no static file in `api/`; 15 advertised endpoints return **parseable JSON**, not merely 200 | CI + `stage_commit` + 6-hourly workflow |
| `capability_register.py` | 14 capabilities with measured **floors that only rise**; several assert *relations* (body-search hits must exceed metadata) so a probe testing half a capability fails too | CI + `stage_commit` |
| `generate_node_declaration.py` | `/.well-known/axn-node.json` computed from registry state every commit, then compared **published-to-published** | `coherence_sync` + capability probe |
| `verify_symbolon_store.py` | every sealed core re-hashed against its kernel; `verified_at` dated; mismatches write `integrity_alert` and exit nonzero | `stage_symbolon` before commit |
| `data/api/endpoint-contract.json` | the declared set of machine endpoints | source of truth for the guardians |

**F1 closed:** the node declaration advertised `highest_deposit: 1092` against an
actual 1,434 — a 342-deposit divergence published by the root node about itself
for nineteen days. In a federation a stale head is how peers silently diverge.

---

## §5 · PATHOLOGY REGISTER — additions

**PATHOLOGY-31 · Publication invisible to disk-reading validators.** *(closed)*
Bytes correct, URL dead, every check green. Fix: guardians that fetch.

**PATHOLOGY-32 · Undocumented mint route.** A second stamper operated on a
different origin before the atlas carried it. Any surface that can allocate a
position must appear here, or the map understates the network's attack and
failure surface. Fix: this addendum, and the rule at its head.

**PATHOLOGY-33 · Mirrored governance without verification.** A constitution copy
that cannot be checked against its source will silently diverge into a second
version of a guarantee. Fix: the mirror verifies on every visit and says so.

**PATHOLOGY-34 · Deployment as an unmapped dependency.** Twice today a platform
deploy limit blocked all publication for 24 hours while git was perfectly
current. Commit is not publication. The atlas should treat the deploy step as a
named flow with its own failure mode, not as an invisible edge.

---

## §6 · What the map now says about custody

`rhizome/peers.json` remains **live and empty by fact**. The second stamper does
not change this: it is a second *surface*, under the same administrator, on the
same platform, billed to the same account. **Under the LOCKSS test it is one
custody domain with the archive**, not a peer.

> Two surfaces are not two custodians. The atlas must not let a richer diagram be
> mistaken for a more distributed network.
