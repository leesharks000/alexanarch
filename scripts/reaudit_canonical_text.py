#!/usr/bin/env python3
"""reaudit_canonical_text.py — EA-AVAILABILITY-INTEGRITY-01, Task T2.

Implements the two-axis availability model (decision ⟡1, RESOLVED 2026-07-28):

  Axis 1 — body presence:   body_status.class (existing vocabulary, corrected)
  Axis 2 — canonical text:  canonical_text_status, NEW required field, enum:
      canonical_full_text | recovered_full_text | metadata_only |
      attachment_only | tombstone | withdrawn

Why this exists (audit deposit #1413, finding H2): the v3 body auditor
measured residual characters and pronounced `class: full` on 224 deposits
whose content_type declares them semi-restored metadata captures — i.e. it
certified captured DataCite descriptions as recovered works. This instrument
makes content_type-aware assignments, corrects the mistyped Axis-1 classes
to `metadata_capture`, and emits a full diff artifact for MANUS spot-check
(T2b samples 10% plus all inversion suspects).

Inversion guard (chorus Q2): a deposit whose content_type says semi-restored
but whose body is materially larger than capture boilerplate may be a
genuinely restored work under a stale content_type. Such records are FLAGGED
(t2b_flags), not silently reclassified.

Idempotent: re-running recomputes assignments from current registry state.
"""
import json, sys, datetime, random

REGISTRY = 'data/registry.json'
DIFF_OUT = 'data/reaudit-T2-diff-2026-07-28.json'
ENUM = ("canonical_full_text", "recovered_full_text", "metadata_only",
        "attachment_only", "tombstone", "withdrawn")
INVERSION_CHARS = 8000   # semi-restored bodies above this are inversion suspects

def assign(d):
    """Return (canonical_text_status, corrected_axis1_class_or_None, reason)."""
    bs = d.get('body_status') if isinstance(d.get('body_status'), dict) else {}
    cls = bs.get('class', '')
    rec = str(bs.get('recovery_status', ''))
    ct  = str(d.get('content_type', '')).lower()
    status = str(d.get('status', '')).upper()

    if 'WITHDRAWN' in status:
        return 'withdrawn', None, 'registry status WITHDRAWN'
    if 'TOMBSTONE' in status:
        return 'tombstone', None, 'registry status TOMBSTONE'
    if 'semi-restored' in ct:
        newcls = 'metadata_capture' if cls == 'full' else None
        return 'metadata_only', newcls, 'content_type declares semi-restored capture'
    if rec == 'UNRECOVERED' or cls == 'description_only':
        return 'metadata_only', None, 'unrecovered / description-only body'
    if cls == 'excerpt_crossref':
        return 'metadata_only', None, 'excerpt only; canonical text not held'
    if cls == 'dataset_pointer':
        return 'canonical_full_text', None, 'canonical content is the held dataset'
    if bs.get('recovered_from') or rec.startswith('FULL-AT-DEPOSIT') \
       or rec == 'RECOVERABLE-AT-CHAT' or 'recovered' in ct:
        return 'recovered_full_text', None, 'restored from recovery source'
    if cls in ('full', 'native_short', 'stub_short', 'semi_apparatus', 'site_canonical'):
        return 'canonical_full_text', None, 'native body held since mint'
    return 'metadata_only', None, 'no body_status evidence; conservative floor'

def main(apply=True):
    reg = json.load(open(REGISTRY))
    deps = reg['deposits']
    diff, t2b_flags = [], []
    for d in deps:
        cts, newcls, reason = assign(d)
        assert cts in ENUM
        old = d.get('canonical_text_status')
        oldcls = (d.get('body_status') or {}).get('class') if isinstance(d.get('body_status'), dict) else None
        changed = (old != cts) or (newcls and oldcls != newcls)
        if changed:
            diff.append({"deposit_number": d['deposit_number'], "axn": d.get('axn'),
                         "canonical_text_status": {"old": old, "new": cts},
                         "axis1_class": {"old": oldcls, "new": newcls or oldcls},
                         "reason": reason})
        if apply:
            d['canonical_text_status'] = cts
            if newcls and isinstance(d.get('body_status'), dict):
                b = d['body_status']
                b['class_before_T2'] = oldcls
                b['class'] = newcls
                b['reclassified_by'] = 'EA-AVAILABILITY-INTEGRITY-01-T2'
                b['reclassified_at'] = datetime.datetime.now(datetime.UTC).isoformat()
        # inversion suspects
        if 'semi-restored' in str(d.get('content_type','')).lower():
            chars = (d.get('body_status') or {}).get('residual_chars', 0) if isinstance(d.get('body_status'), dict) else 0
            if isinstance(chars, int) and chars > INVERSION_CHARS:
                t2b_flags.append({"deposit_number": d['deposit_number'],
                                  "residual_chars": chars,
                                  "note": "semi-restored content_type over large body — possible stale content_type (inversion); manual review"})
    # T2b sample: 10% of Axis-1 reclassifications, seeded
    recls = [x for x in diff if x['axis1_class']['old'] != x['axis1_class']['new']]
    random.seed(20260728)
    sample = sorted(random.sample([x['deposit_number'] for x in recls],
                                  max(1, len(recls)//10))) if recls else []
    out = {"instrument": "reaudit_canonical_text.py",
           "task": "EA-AVAILABILITY-INTEGRITY-01 T2",
           "run_at": datetime.datetime.now(datetime.UTC).isoformat(),
           "registry_deposits": len(deps),
           "changed": len(diff),
           "axis1_reclassified": len(recls),
           "t2b_sample_10pct": sample,
           "t2b_inversion_flags": t2b_flags,
           "diff": diff}
    json.dump(out, open(DIFF_OUT, 'w'), ensure_ascii=False, indent=1)
    if apply:
        json.dump(reg, open(REGISTRY, 'w'), ensure_ascii=False, indent=2)
    from collections import Counter
    print("canonical_text_status distribution:",
          dict(Counter(x['canonical_text_status']['new'] for x in diff)) if not apply
          else dict(Counter(d['canonical_text_status'] for d in deps)))
    print(f"changed: {len(diff)} | axis1 reclassified: {len(recls)} | "
          f"t2b sample: {len(sample)} | inversion flags: {len(t2b_flags)}")
    print(f"diff artifact: {DIFF_OUT}")

if __name__ == '__main__':
    main(apply='--dry-run' not in sys.argv)
