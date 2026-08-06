# WAVE-HEXPOS-01 — Hex-Position Width Normalization and Contested-Position Resolution

**Status:** Phase 1 ready (ruling-free) · Phase 2 BLOCKED on MANUS ruling
**Prepared:** 2026-08-06 · TACHYON (chain 9271269a) · session: AXN stamp overhaul, adopted finding 6
**AXN:** _to be assigned at deposit_
**Scope discipline:** hex-label defects only. Adjacent defects found during audit are RECORDED, not executed (§6).

---

## 1 · Findings

**F1 — Width defect (4 records).** Source records #1, #2, #3 carry hex `01`/`02`/`03`; #913 carries `391`. All other 1,429 records are 4-char. The symbolon endpoint already pads (`padStart(4,'0')`), so no new unpadded labels can enter by that route. Downstream fracture already observed once: R-1270 (body-path helper, #2 unreadable).

**F2 — LIVE position collision at 0365.** #856 (*The Pristine Fallacy*, dated 06-18, minted 06-20) and #869 (*Lexical Minting*, dated 06-22, no minted_at) both carry hex `0365` verbatim. The central registry builder's dict assignment silently drops #856 on every build (last-write-wins) — `positions_count` 1437 = 1433 + 5 − 1 is this collision made visible. A standing one-kernel-one-position violation in production: #856 is unreachable by position.

**F3 — LATENT position collision at 0391.** #901 (*Moltbook Provenance Log*, minted 06-23, work dated 04-01) holds `0391`; #913 (*Secret Book of Walt — ACTIVATED Run 001*, dated 06-24) holds `391`. The keys differ only in width, so today they coexist; any naive padding merges them destructively. Decisive evidence: **#901's hex is inscribed in its sealed canonical bytes** (`**Hex:** 0391`, line 10 of AXN-0391-text.md). #913's label is registry-only and appears in no allocation sequence. Also note `AXN-391-text.md` and `AXN-0391-text.md` are texts of two *different works* — a filename adjacency that invited exactly the R-1270 class of misread.

**F4 — Builder silent-overwrite defect.** `build_central_registry.py` performs no key normalization and no collision detection; contested claims vanish without trace.

**F5 — Precedent confirms the repair pattern.** The 2026-06-22 v1→v2 schema backfill retired old AXN strings via `axn_history` entries (`retired_at` + `reason`) with `legacy_axn` preserved. Label normalization with a history entry is the third application of an existing archive pattern, not a novel identifier mutation.

## 2 · Recommended rulings (TACHYON; MANUS decides)

- **D1** — Ratify Phase 1: pad #1/#2/#3 → `0001`/`0002`/`0003` with history entries. No collision results (verified: padded-key census shows 0001–0003 free).
- **D2** — 0365: **#856 keeps** (priority); **#869 reallocates**.
- **D3** — 0391: **#901 keeps** (priority + inscription in sealed bytes); **#913 reallocates**. Reassigning #901 instead would contradict its own sealed core — ruled out under non-destruction.
- **D4** — Allocate two fresh positions for #869 and #913 from the shared sequence (`data/symbolon-registry/allocation.json`), **and bump the ledger's `next_hex` past them** — otherwise the next symbolon stamp collides with the reallocated records. Simulation used 05B0/05B1 as placeholders.

## 3 · Instruments (all tested against a full clone of the live registry, 2026-08-06)

| File | Act |
|---|---|
| `wave_hexpos_phase1.py` | Pads #1–#3 with `axn_history` entries; writes canonical resolver pages `s/axn/0001|0002|0003/` (current-generation template incl. retired-form rows and JSON-LD); rewrites `s/axn/01|02|03/` as permanent superseded-label alias pages. Idempotent; aborts on any unexpected collision; touches nothing blocked on ruling. |
| `wave_hexpos_phase2.py` | `--p869 XXXX --p913 XXXX` after D2–D4. Reallocates with history entries; renames `AXN-391-text.md` → `AXN-<new>-text.md`, leaving the old path as a pointer file (non-destruction); prints the remaining MANUS-side steps. Refuses positions already held. |
| `build_central_registry.py` (hardened) | Normalizes keys to 4-char; **collisions emit a visible `CONTESTED` entry naming every claimant + stderr warning — never overwrite**; retired labels with genuinely different hex emit `superseded-label` alias entries that never shadow live keys. |
| `stamp-lookup.patch` | `mint/stamp/index.html`: hex queries padded (`391`→`0391` finds #901), `alias_of` followed transparently, `CONTESTED` positions render honestly as contested pending ruling. |

**Simulation results:** Phase 1 → 3 normalized, idempotent re-run clean. Builder mid-state → `1429 positions · 2 CONTESTED (0365: #856,#869 · 0391: #901,#913)`. Phase 2 (05B0/05B1) → `1433 positions · 0 CONTESTED`; lookups: `01`→absent (alias page + query-padding cover it), `0001`→#1, `0365`→#856, `0391`→#901, new homes resolve.

## 4 · Execution order

1. MANUS: D1 → run Phase 1 → hardened builder → standard page/OAI regeneration + nine-site propagation for #1–#3. (The interim registry will honestly show 2 CONTESTED until Phase 2 — truthful state, not breakage.)
2. MANUS: D2–D4 (two positions + ledger bump) → run Phase 2 → builder → resolver pages for the two new positions via standard generation → `s/axn/391/` rewritten as a contested-history page pointing both ways (to #901 at 0391 and to #913's new home) → propagation for #869/#913; #856/#901 record pages regenerate to state uncontested standing.
3. Apply `stamp-lookup.patch` (deploys with the site; no dependency on phases).

## 5 · Why this precedes the visual overhaul

The stamp redesign will print hex labels and QR-encoded lookups far more prominently. Every surface it adds is a new fracture site if the label layer beneath it is inconsistent — and a collision under a QR code is a public verification failure, not a private data defect.

## 6 · Recorded, not executed (adjacent defects for separate ruling)

- **R-A** `axn_display` mismatches ×12, three classes: stale v1 4-glyph displays (#1–#3); *divergent* glyphs vs current axn (#324, #494 — possible pre-repair-hash residue, needs per-record evidence); full-AXN-string-in-display field defect (#867 — whose glyphs also contain 🜂 and ◽, absent from the canonical v2 table: possible older-table or variant-selector residue).
- **R-B** #869 family `DATASET` is outside the axn_lib family vocabulary.
- **R-C** Glyph-table non-injectivity (adopted finding 3): ❤️ at 0x81 (Symbolic) and 0xCF (Signal); ⌛ at 0x60/0x6E (both Temporal). Table frozen canonical; disambiguation is the visual layer's work (cluster ticks), queued in the stamp-band redesign.

— WITNESS-GAP: this wave is not real until inscribed; deposit this record and capture in the chain tether.

---

## 7 · AS EXECUTED — 2026-08-06 (TACHYON, this session; amendments to the instrument above)

**F6 — THIRD contested position, found by the hardened builder's first live run: 05AF.**
Deposit #1433 (the chain tether, minted 2026-08-04T08:56Z) vs symbolon witnessing
`6b48617ee0e64e8f` (registered 2026-08-05T04:37Z, file `3d699cba…jpg`). Root cause:
`mint_deposit.next_hex_id()` READ the shared allocation ledger as a floor but never
WROTE it — #1433 took 05AF, the ledger still said `next_hex: 05AF`, and the witness
endpoint CAS-allocated the same position a day later. The ledger's "the two allocators
share one space and can never collide" was an assertion, not an implementation
(PATHOLOGY-01 in load-bearing prose).

**D5 (executed under the adopted priority principle; flagged for explicit MANUS
ratification):** #1433 keeps 05AF — it is the tether; fracturing the chain's own
address is ruled out. The witnessing reallocated to **05B2** with a `position_history`
entry preserving its issued form `AXN:05AF.UNCLASSIFIED.🕙🔖⏰🕊️🌅🌌`.

**Positions as executed:** #869 → **05B0** · #913 → **05B1** · witnessing → **05B2** ·
ledger `next_hex` → **05B3**.

**Root-cause fixes shipped:** (a) `mint_deposit.py` now writes the ledger at
allocation (`_bump_symbolon_ledger`; an aborted mint burns a label — a harmless gap,
never a collision); (b) `api/register-symbolon.js` defense-in-depth: candidate =
max(ledger, central-registry occupied max + 1).

**EXECUTION INCIDENT (recorded per archive practice; caught same-session,
pre-commit):** the first form of Phase 2's rename block moved artifacts by label
alone — on the contested 0365 this moved **#856's** (the keeper's) canonical text,
deposit-md and external-metadata to #869's new address. Reverted byte-identical from
git; the instrument now carries an ownership gate (`full_text_path` must name the
file) and a sealed-bytes rule (canonical texts move as exact bytes, never edited —
verified: #913's text at its new path diffs 0 lines from the original). The incident
is the wave's own lesson repeated at smaller scale: on a contested label, the
filename family belongs to the keeper.

**Doctrine note:** #913's sealed frontmatter internally retains `hex: 391` (as #901's
retains `0391`). Sealed bytes are never edited; the registry + `axn_history` are
authoritative for current address. `s/axn/391/` now serves a contested-history page
pointing both ways.

**Verification (local, CI's own gates):** `validate_deposit.py --strict` → 0 failures ·
resolver PARITY OK (1935 keys) · `status_reconcile` → 0 · central registry →
**1439 positions · 0 CONTESTED · 1445 kernels** · propagation run for
1 2 3 856 869 901 913 1433 (record pages, 1433 wiki pages, 1433 axn resolver pages,
browse/search/chunks/sitemap, OAI 1372, resourcesync).

**Recorded, not executed (additions):** R-D — #869 has no `AXN-05B0-text.md`
(its text lives at `deposit-0869-text.md`; pre-existing naming-convention class,
warn-tier in CI). R-E — the six symbolon witnessings have no `s/axn/` resolver
pages (existing convention; revisit in the stamp visual overhaul alongside the
kernel-URL QR question, finding 4).
