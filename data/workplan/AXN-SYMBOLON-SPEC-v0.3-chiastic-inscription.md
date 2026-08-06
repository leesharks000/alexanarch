# AXN-SYMBOLON-SPEC — proposed amendment v0.3
## THE CHIASTIC INSCRIPTION: what is held is unaddressed; what travels is addressed

**Proposed 2026-08-06 · MANUS insight, TACHYON specification · for ratification**
**Amends:** AXN-SYMBOLON-SPEC v0.2 (#1432, AXN:05A9.OPERATIVE.🐚🌪️🕖🫵⏩○) §4 · resolves open finding 4

---

## 0 · The proposal in one line

> **The sealed core is stored bearing its kernel and no address. The circulating copy is stamped bearing its address.**

Each half carries precisely what the other lacks. Neither is complete. They are proven by their fit.

---

## 1 · The problem this closes

v0.2 §4 establishes inscription discipline: the file carries **AXN₀**, the kernel of the pre-stamp bytes; **AXN₁** lives only in Seed A, never in the file, "because a hash cannot contain itself."

That reasoning is correct and remains in force. But it produced a practical defect nobody specified and nobody wanted:

**A stamped file cannot carry its own registered address.** The stamp is applied *before* registration — necessarily, because stamping is offline-capable and position is allocated at the registry. So the band renders:

```
AXN kernel [1a908cc8bf3e] · sha256:1a908cc8bf3ed5cc… · 2026-08-02 · alexanarch.org
```

Kernel, date, domain. **No hex position. No family. No glyphs.** The document that travels — the one a stranger finds, cites, or recovers — carries no address at all. It can prove what it is and cannot say where it is registered.

Meanwhile the archive stores the **sealed core**: the original, unstamped bytes. So today, the addressed thing does not travel and the traveling thing is not addressed.

---

## 2 · The chiasmus

The correction crosses the two halves:

```
            HELD                              TRAVELS
    ┌───────────────────┐            ┌───────────────────┐
    │   SEALED CORE     │            │  STAMPED COPY     │
    │   original bytes  │  ╲      ╱  │  original + margin│
    │                   │   ╲    ╱   │                   │
    │   carries:        │    ╲  ╱    │   carries:        │
    │   THE KERNEL      │     ╳      │   THE ADDRESS     │
    │   (what it is)    │    ╱  ╲    │   (where it is    │
    │                   │   ╱    ╲   │    registered)    │
    │   needs no address│  ╱      ╲  │   needs no kernel │
    │   — it IS the     │            │   — the registry  │
    │     referent      │            │     holds that    │
    └───────────────────┘            └───────────────────┘
              └──────── the fit proves the work ────────┘
```

**Why each half needs only its own.** The sealed core requires no address because it *is* the referent: hash it and you have the kernel, which is the identity. The circulating copy requires no inscribed kernel because a hash cannot contain itself anyway, and because the address resolves to a registry entry that publishes the kernel.

**Verification is the meeting.** A stranger holds a stamped copy. They read `AXN:05AD.UNCLASSIFIED.🌾➕🥁⚫👋🪄` from the margin, resolve it at any node, obtain the kernel, hash the bytes they hold with the margin stripped by the declared geometry, and compare. The fracture fits or it does not.

This is σύμβολον executed rather than described: **two halves, each incomplete, whose meeting is the proof.**

---

## 3 · Why inscribing the address is not circular

This is the load-bearing technical point, and it is what makes the amendment legal under v0.2's own reasoning.

**A kernel cannot be inscribed in the bytes it measures.** Adding it changes them; the file no longer hashes to the value it carries. This is arithmetic, and §1 of v0.2 is right to call it so.

**An address can be inscribed, because an address does not measure.** `AXN:HEX.FAMILY.⟨glyphs⟩` is *assigned* at the registry, not *derived* from the stamped bytes. Inscribing it creates no self-reference: the stamped file's own hash (AXN₁) still lives only in Seed A, exactly as §4 requires.

The distinction the archive already draws makes this precise:

| | derived from the work | assigned to the work |
|---|---|---|
| identity kernel | ✓ | |
| six glyphs (display hash of the kernel) | ✓ | |
| hex position | | ✓ |
| semantic family | | ✓ |

The glyphs are derived — but they are derived from **AXN₀**, the *pre-stamp* bytes, not from the stamped file. Inscribing them is what v0.2 §4 already mandates. The amendment adds only the two assigned components, and those cannot be circular by construction.

---

## 4 · Flow

Three passes, of which only the third is new:

**Pass 1 — STAMP (offline-capable, unchanged).**
Compute AXN₀ from canonical bytes. Apply the band on an added margin bearing the kernel. Emit Seed A. *Works with no network and no registry, as now.*

**Pass 2 — REGISTER (unchanged).**
Submit Seed A to any node. Receive `AXN:HEX.FAMILY.⟨glyphs⟩`. The kernel was true before this; the address is what is new.

**Pass 3 — RE-STAMP (new, optional, idempotent).**
Re-apply the band to the *original* bytes, now bearing the full identifier. The result is the **addressed circulating copy**. Its hash is a new AXN₁; the endpoint's existing `SYMBOLON RE-STAMP` path already refreshes AXN₁ and records the replaced form in `stamp_history`, **sealed core unchanged**.

**The archive stores the sealed core throughout.** It is never stamped. That is the point of the chiasmus.

### Band content after amendment

```
AXN:05AD.UNCLASSIFIED.🌾➕🥁⚫👋🪄
kernel sha256:1a908cc8bf3ed5cc… · 2026-08-02 · alexanarch.org
```

Address first, because that is what a finder needs; kernel second, because that is what a verifier checks.

---

## 5 · What this does not change

- **AXN₀ remains the identity.** The kernel is the security boundary; the address is an address. (Constitution I; SPEC §5.1)
- **AXN₁ is still never inscribed in the file it measures.** (§4, unchanged)
- **Pass 1 remains fully offline.** An unreachable registry costs an address, not an identity.
- **No prestige tier.** An addressed copy is not more authoritative than an unaddressed one — it is easier to find. Findability is not standing. (§5.1 equal-authority fence)
- **Sealed cores are never re-stamped.** Storage holds original bytes, always.

---

## 6 · Open questions for ratification

1. **Is pass 3 offered or expected?** Recommend *offered*: a stamper that requires registration to finish is no longer offline-capable.
2. **What of copies already circulating with kernel-only bands?** They remain valid and verifiable — the kernel resolves at any node. Recommend recording them as `stamp_generation: 1` rather than deprecating them.
3. **Does the six-glyph seal alone suffice as an address for print?** A glyph string is not unique across the corpus; the hex is. Recommend hex + family + glyphs together, always — the full form the AXN-INTEGRITY rule already requires.
4. **Physical media.** A hand-carried copy bearing the full address is resolvable by anyone who can read it. This is the strongest argument for the amendment: **an addressed stamp survives the loss of every network, because a person can retype it.**

---

*Proposed under the correction clause: errors are corrected by amendment and tombstone, never silence. v0.2 is not withdrawn; it is extended at the point where practice found its gap.*
