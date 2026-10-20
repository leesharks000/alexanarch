#!/usr/bin/env python3
"""per_scalar.py — the historical PER scalar is derived from its four-unit vector, never entered (2026-10-20).

capture_intake.per_vector: "PER is a FOUR-UNIT VECTOR. The scalar is a projection of it, never the record." per_v holds
author, inst, id, src, each True (retained) or False (lost); the scalar is the share lost.

THE DEFECT THIS CLOSES. The repair of 2026-10-15 (v12.203) re-derived 69 stored scalars that disagreed with their vectors,
but nothing derived the scalar at seating: session seatings wrote `per` and `per_v` side by side by hand, and 38
observations seated 2026-10-16 to 2026-10-19 again disagreed (most stored 0.25 where two of four units were lost). The
ruling (Lee Sharks, 2026-10-20 08:54 EDT): "yes lets correct those 38 and patch intake".

So: capture_intake.seat_flat derives `per` from `per_v` before it seats a draft, and seat_capture_postflight runs this
script first on every registry write. An observation whose stored scalar disagrees with its vector is corrected and
carries per_corrected {from, to, on, basis}; the correction log records the pass. Recorded, not refused (laws record).
An observation without a four-boolean vector is untouched. Idempotent: a registry already in agreement is not written.

    python3 scripts/per_scalar.py            # correct and record
    python3 scripts/per_scalar.py --check    # report only; exit 0 either way
"""
import datetime, json, pathlib, sys

BASIS = "re-derived from per_v, the four-unit vector that is the record (capture_intake.per_vector)"


def per_from_vector(pv):
    """The share of the four units lost, or None where the vector is not a set of booleans."""
    if not isinstance(pv, dict):
        return None
    vals = [v for v in pv.values() if isinstance(v, bool)]
    if not vals:
        return None
    return round(1 - sum(vals) / len(vals), 2)


def derive(o, on, fill=True):
    """Set o['per'] from o['per_v']; record per_corrected where a stored figure disagreed. Returns (from, to) or None.
    fill: where no figure was entered, derive one (intake). The postflight passes fill=False: a seated observation whose
    scalar is empty is left as seated."""
    lost = per_from_vector(o.get("per_v"))
    if lost is None:
        return None
    p = o.get("per")
    if isinstance(p, (int, float)) and abs(p - lost) <= 0.01:
        return None
    if isinstance(p, (int, float)):
        o["per_corrected"] = {"from": p, "to": lost, "on": on, "basis": BASIS}
        o["per"] = lost
        return (p, lost)
    if fill:
        o["per"] = lost  # no figure was entered: derived, nothing to correct
    return None


def main():
    root = pathlib.Path(__file__).resolve().parents[1]
    path = root / "data/EA-WG-CAPTURES-01.json"
    reg = json.loads(path.read_text(encoding="utf-8"))
    on = datetime.date.today().isoformat()
    fixed, seen = [], set()
    for e in reg["entries"]:
        for o in [e] + (e.get("observations") or []):
            if "--check" in sys.argv:
                lost = per_from_vector(o.get("per_v"))
                p = o.get("per")
                ch = (p, lost) if lost is not None and isinstance(p, (int, float)) and abs(p - lost) > 0.01 else None
            else:
                ch = derive(o, on, fill=False)
            if ch:
                key = o.get("obs_id") or e["slug"]
                if key not in seen:
                    seen.add(key); fixed.append((key, o.get("slug") or e["slug"], ch[0], ch[1]))
    if "--check" in sys.argv:
        print(f"[per] {len(fixed)} observation(s) whose stored scalar disagrees with its vector")
        for k, s, a, b in fixed: print("  ", k, s, a, "->", b)
        return 0
    if not fixed:
        print("[per] every stored scalar agrees with its vector")
        return 0
    reg.setdefault("correction_log", []).append({
        "date": on,
        "change": f"version {reg.get('version')}; PER re-derived from its vector on {len(fixed)} observation(s) (scripts/per_scalar.py)",
        "detail": "The stored scalar disagreed with per_v, the four-unit vector that is the record. The scalar is re-derived and each "
                  "observation carries per_corrected {from, to}. Ruling: operator, 2026-10-15 03:39 EDT, 'lets correct the scores'; "
                  "2026-10-20 08:54 EDT, 'yes lets correct those 38 and patch intake'.",
        "observations": [k for k, _, _, _ in fixed]})
    path.write_text(json.dumps(reg, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[per] re-derived on {len(fixed)} observation(s)")
    for k, s, a, b in fixed: print("  ", k, s, a, "->", b)
    return 0


if __name__ == "__main__":
    sys.exit(main())
