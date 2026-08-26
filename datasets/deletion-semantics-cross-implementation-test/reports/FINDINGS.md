# Findings — deletion-semantics cross-implementation test v1.0

Lee Sharks, 2026-08-26. Fulfils the cross-test offered on knowledge-catalog#207: *"When your
exporter ships, I'd like to run its shape against these cases and send you what breaks."*
All source artifacts are pinned in `sources/source-lock.json`; every run is captured under
`runs/`; `commands/reproduce.sh` reproduces the whole thing from clean clones.

**Two implementations, one corpus.** The producer is @andrewcrenshaw's remember/0.2 emitter
(log.md + store records + .manifest.json + tombstones.md). The consumer is @inkxel's
`never_landed.py` assertion-consistency checker. The corpus is the 111-case deletion-conformance
fixture v2.1, built before either implementation existed. Neither implementation was modified.

---

## 1. Baselines reproduce

`--fixture` mode reproduces @inkxel's 2026-07-29 result exactly: **111 cases, 1 true positive,
0 false positives, 0 missed, must-not-mark passed.** `--log/--store` mode against the published
bundle reproduces @andrewcrenshaw's 2026-07-31 result exactly: **3 claims, 7 known targets, the
planted `never-landed-999` caught and only it.** Bundle integrity verified: all 7 files match the
published `SHA256SUMS`, 0 mismatches. This is a third independent reproduction of both.

## 2. Representation portability is 1/111 — and it is not the checker's fault

Rendering the corpus into the emitter's shape in **strict** mode (refuse anything requiring a key
the emitter does not define) yields **1 expressible case of 111**. The other 110 refuse on
identity: the emitter's `id` is a producer-controlled lesson key, a DOI is a handle to a foreign
resolver, and there is no slot for the second. 98 of the corpus's identifiers are DOIs.

**Checker portability and representation portability are different properties.** Two flags —
`--claim-pattern` and `--id-key` — sufficed for every run in this package, confirming the
parameterization claim established between the two implementations on a third corpus. The
representation carried 1/111 regardless.

## 3. A clean downstream verdict is not evidence of translation fidelity

**Forced** mode translates everything and produces the *same* clean verdict as strict mode —
111 claims, 110 known, 1 never-landed, no error. It reached it by fabricating **110 write-claims
the producer never made** and dropping **451 field-level facts**. The checker cannot distinguish
the two runs. The receipt can:

| | strict | forced |
|---|---|---|
| source_cases | 111 | 111 |
| expressible | 1 | 111 |
| refused_untranslatable | 110 | 0 |
| preserved | 1 | 1 |
| coerced | 0 | 110 |
| dropped | 4 | 451 |
| fabricated | 0 | 110 |
| downstream verdict | 1 claim, 1 never-landed | 111 claims, 1 never-landed |

> **absence of an alarm is not evidence of preservation.**

`receipts/` carries both, machine-readable, with a fidelity warning that cannot be detached from
the green result. **`refused_untranslatable` is a distinct category from `coerced`**: a translator
that declines to represent what it cannot carry preserves epistemic integrity; one that silently
forces it does not. Collapsing them would make the receipt commit the semantic collapse it exists
to detect — an earlier draft did exactly that, and reported honest refusal as damage.

### Reconciliation of the 671 figure

An earlier exploratory profile reported **671 breaks** in forced mode under one coarse category.
The receipt decomposes that same total without changing it:

    451 dropped (identifier_kind 111, observation 110, successor 87, presence 75, reason 68)
    + 110 coerced (identity)
    + 110 fabricated (claim)
    = 671

The measurement became more discriminating during the experiment; the quantity did not change.

## 4. The decisive result: a recorded removal and a never-landed write are observationally identical

Three records, one convention (`fixtures/abc/`):

    A  created and present
    B  created, then removed — tombstone records presence, date, reason, successor
    C  creation asserted, never landed

**Current consumer:**

    A → present        B → never_landed        C → never_landed        B and C COLLIDE

The producer recorded the removal faithfully. The consumer correctly reported a claim with no
landing. **The information is destroyed in the gap between them**, because the removal lives in
`tombstones.md` prose and — verified in `sources/remember-bundle/bundle/.manifest.json` — the
machine-readable index references no tombstones at all. A consumer reading the index sees a
bundle in which B simply does not exist.

This is knowledge-catalog#207's title, reproduced experimentally across two independently built
implementations, using each side's own published artifact. Neither implementation is at fault.

## 5. The minimal repair, tested for necessity and sufficiency

**Payload** — a surviving absence assertion keyed to stable identity:

```yaml
id:
presence:        removed | never_landed
date:
reason:
recorded_by:
successor:       # optional
successor_kind:  # optional / profile-level
```

**Sufficiency** (`runs/06`): lift the prose tombstone into the machine index and add one consumer
lookup — before calling a claim never-landed, ask whether an absence record survives for that
identity:

    A → present        B → removed        C → never_landed        B and C DIVERGE

with A and the claim/target counts undisturbed (3 claims, 3 known).

**Necessity** (`runs/05`): strip the absence record from the index and leave `tombstones.md` fully
intact — **B and C collide again.** The repair is therefore not "record the removal," which the
producer already did. It is *expose the removal where a consumer reads.*

### The normative form of the requirement

Not "put tombstones in `.manifest.json`" — that is Remember's carrier, not an OKF primitive:

> **A surviving absence assertion must be exposed on a machine-readable discovery surface that
> ordinary consumers consult. Preserving the same information only in prose is insufficient.**

Remember can satisfy this through its manifest. Another producer may use a structured log, a
reserved absence file, or a future OKF-native mechanism.

## 6. Limits of this experiment, stated

**The corpus under-represents the case the finding turns on.** Applying the payload to all 111
cases (`runs/07`): 64 express fully; 36 carry no presence value (pre-axes v1 cases); 8 have
neither reason nor actor; 3 lack a verification date. And **every expressible case is
`presence=removed`** — the corpus contains exactly one `never_landed` case. The distinction this
package demonstrates is barely represented in the fixture built to test it. The next corpus cut
should carry the A/B/C trio as first-class cases.

**The `--id-key` failure mode is a property of the store, not the checker.** On the bundle
(filenames are summary slugs, stable ids in frontmatter) pointing `--id-key` at a nonexistent key
drops known targets 7→5 and turns all three claims into never-landed, two of them false. On a
stem-named store it is a no-op. A conformance fixture built on stem-named stores will never
exercise that path.

**Two guards confirmed on real data rather than selftest.** The default two-group claim pattern
parses zero claims against the emitter's verb-first prose and *alarms* — @andrewcrenshaw's
contributed refinement, working on his own shape. An empty log under an ordinary
`# Directory Update Log` heading reports zero claims with **no error** — @inkxel's heading-stem
fix holding, with *empty* distinguished from *unreadable*.

## 7. The structural rhyme

Two findings in this package have the same shape at adjacent boundaries:

    consumer sees no absence marker   ⇏   nothing was removed
    checker returns clean after translation   ⇏   translation preserved semantics

Both are cases of a negative result being read as a positive assurance. The repair in each case is
the same in kind: make the missing thing *say so* on a surface the consumer already reads.
