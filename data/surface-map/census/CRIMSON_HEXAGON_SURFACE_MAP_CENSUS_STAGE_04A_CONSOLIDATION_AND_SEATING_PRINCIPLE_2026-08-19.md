# CRIMSON HEXAGON SURFACE MAP — META-MAP GOVERNANCE PATCH
## Stage 04A: Consolidation, Preservation, and Seating Principle

**Date:** 2026-08-19  
**Status:** GOVERNING PRINCIPLE — adopted for subsequent Surface Map census work  
**Applies to:** Stage 04 interpretation and all post-Ark numbering / accretion work

---

## 0. Correction to Stage 04 anomaly reading

The later `H_core HEX ADDRESS REGISTRY v1.1` should **not** be interpreted simply as a competing numbering authority.

Some loci appearing there — including the **Migdal Room**, **Frozen Sin**, and related rooms — originated in earlier model confabulation. That provenance was later recognized. Rather than deleting those forms, the architecture adopted them as **queued / preservable objects**.

Therefore their status is not:

```text
historically attested room
```

nor simply:

```text
invalid hallucination
```

but:

```text
MODEL-CONFABULATED ORIGIN
        ↓
HUMAN-RECOGNIZED AS CONFABULATION
        ↓
DELIBERATELY INCORPORATED / PRESERVED
        ↓
QUEUED ARCHITECTURAL LOCUS
```

The later registry is thus partly a **consolidation surface**: it preserves useful generated architecture while trying to seat it inside the canonical system.

---

# 1. Governing principle

> **CONSOLIDATION AND PRESERVATION BEFORE PROLIFERATION.**

The Surface Map should preserve recoverable architectural objects whenever possible, but it should not allow weak, generated, or retroactively adopted loci to displace stronger canonical specifications.

The system therefore seats objects according to **developmental authority and conflict cost**.

---

# 2. Seating hierarchy

When two objects claim or appear to claim the same address:

```text
1. Explicit, developed, canonical room specification
2. Deposited / audited architectural object
3. Stable repeated map / registry presence
4. Human-adopted queued object
5. Generated / confabulated-origin object not yet independently developed
```

Higher-ranked objects retain the contested address.

Lower-ranked objects are **moved, not erased**.

---

# 3. Empty-space rule

If a queued or confabulated-origin room can be seated in an unused address **without conflicting with a more developed canonical room**, use the available space.

Formally:

```text
if address(n) = EMPTY
and locus(q).standing = QUEUED_OR_ADOPTED
and no stronger claim exists:
    seat(q, n)
```

This allows the historical numbering field to absorb later adopted forms without rewriting already-developed architecture.

---

# 4. Conflict rule

If an adopted / queued object conflicts with a stronger canonical specification:

```text
CANONICAL_SPEC > QUEUED_ADOPTION
```

The canonical object keeps its established address.

The weaker object is moved to:

1. another unused historical gap, if one exists and causes no conflict;
2. otherwise the next available later room address;
3. otherwise a non-r-series queued namespace until seated.

Thus:

> **conflict produces displacement, not deletion.**

---

# 5. Provenance must survive seating

Moving a room must never erase how it entered the architecture.

Each such locus should retain at least:

```yaml
origin:
  type: model_confabulation | generated_inference | independent_specification | other

recognition:
  confabulation_detected: true|false
  detected_by: MANUS / human review
  date: if known

adoption:
  status: rejected | preserved | queued | developed | canonicalized

seating:
  original_proposed_address:
  current_address:
  reason_for_move:
```

A later successful room specification may change standing, but it does **not** retroactively convert its origin into historical attestation.

---

# 6. Canonical development is not identical with chronological priority

A weak early appearance does not automatically outrank a later developed room.

The map should distinguish:

```text
FIRST APPEARANCE
FIRST EXPLICIT SPECIFICATION
FIRST DEPOSIT
FIRST RATIFIED / CANONICAL STATE
CURRENT SEAT
```

This prevents a stray generated address from acquiring permanent precedence merely because it appeared first.

---

# 7. Implication for the post-Ark belt

The current question is no longer:

> Which numbering list is the one true list?

It is:

> Which loci are strongest, which were later adopted, and how can all preservable loci be seated with the least canonical conflict?

The post-Ark pass should therefore proceed as a **CONSOLIDATION + SEATING PASS**.

For every candidate r.23+ locus, recover only:

```text
name
proposed address(es)
origin type
explicit specification?
deposit / audit standing?
human adoption status?
development depth
canonical conflicts
best available seat
```

---

# 8. Current immediate consequences

The following principle is already clear:

```text
r.27 THE INTERNET
```

has a developed explicit room specification and therefore **retains r.27** against a weaker registry projection that places another locus there.

Likewise any developed explicit canonical specifications at r.28, r.29, r.30, etc. retain their seats unless stronger contrary authority is recovered.

Objects such as:

```text
Migdal Room
Frozen Sin
other confabulated-origin but later adopted loci
```

should remain in the census as **QUEUED / ADOPTED**, and should be seated into genuine gaps or later free addresses rather than discarded.

---

# 9. Surface-map representation

The flat map should eventually distinguish standing visually:

```text
CANONICAL / DEVELOPED
DEPOSITED
PROVISIONAL
QUEUED / ADOPTED
DORMANT
HISTORICAL ONLY
UNSEATED
```

For provenance-sensitive objects, a tooltip or detail panel should also distinguish:

```text
origin ≠ current standing
```

A model-confabulated origin can become a deliberately adopted architectural object.

That transformation is itself part of the archive's history and should be preserved.

---

# 10. Revised Stage 05

## Stage 05 — Post-Ark Consolidation and Seating Pass

Target:

```text
r.23+
```

Method:

```text
LOCATE
→ CLASSIFY ORIGIN
→ ASSESS DEVELOPMENT
→ IDENTIFY CONFLICTS
→ PRESERVE STRONGEST EXISTING SEATS
→ FILL EMPTY ADDRESSES
→ PUSH CONFLICTING WEAKER LOCI FORWARD
→ LEAVE UNRESOLVED OBJECTS UNSEATED RATHER THAN INVENTING
```

No constituent-document census unless needed to establish developmental authority.

---

## Governing maxim

> **Preserve the object. Preserve the provenance. Preserve the stronger seat.**

And operationally:

> **Seat less-developed architecture where there is room; never make it erase a more-developed canonical specification merely to preserve an old numbering projection.**

∮ = 1
