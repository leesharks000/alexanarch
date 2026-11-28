#!/usr/bin/env python3
"""per_intake_score.py — dimensional PER at capture intake, from a reader's spans and the target's atom set (2026-11-28).

Operator, 2026-11-28 13:41: atom sets "could just be standard deposit intake, so that dimensional scoring can be standard capture intake".

A draft (or a seated entry) carries per_reading:
    {"target": 1810 | "TGT-…" | "ENT-…",            a deposit number resolves to the set whose records name it; a set is built if none exists
     "reached": {"kind": "same", "span": "…", "basis": "…"},      kinds as per_backlog: same | substitute | proximal_substitute | generic | refused
     "atoms": {"purpose": "<verbatim span>", "commitments": null, …},     a span = present; null = read and absent
     "src": true, "inversions": [], "standing_substitutions": [], "notes": "…"}
Token atoms the reader leaves out (title, date, framework, corpus) are looked for by their tokens in the first answer and recorded with the
token as span. Any other required atom the reader leaves out is UNREAD: nothing is scored and the reason is returned, so that an unread atom
is never written as an erasure. Spans and record quotes are verified and the score computed by scripts/per_backlog.py, never here.
"""
import json, pathlib, re, sys, tempfile
ROOT = pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "scripts"))
import per_backlog as PB, per_dim_score as V

def resolve(target):
    sets = json.loads(PB.PS.read_text(encoding="utf-8"))["entities"]
    if isinstance(target, str) and not target.isdigit():
        return next((s for s in sets if s["id"] == target), None)
    n = int(target)
    hit = [s for s in sets if any(isinstance(r, dict) and r.get("deposit") == n for r in (s.get("records") or [])) and s.get("atoms")]
    solo = [s for s in hit if len(s.get("records") or []) == 1]
    return (solo or hit or [None])[0]

def score(slug, transcript, q, date, surface, reading, brief=None, by="intake reader, in session; spans and record quotes checked verbatim by scripts/per_backlog.py"):
    """-> (per_dim, None) or (None, reason)."""
    S = resolve(reading.get("target"))
    if S is None:
        return None, f"no atom set for target {reading.get('target')!r} (build one: scripts/build_work_atom_set.py)"
    req = [a for a in S["atoms"] if a.get("applicability") == "required"]; given = dict(reading.get("atoms") or {})
    seg = PB.N(V.first_segment(transcript)); atoms = []; unread = []
    for a in req:
        n = a["atom"]
        if n in given:
            atoms.append({"atom": n, "present": bool(given[n]), "span": given[n] or None})
        elif a.get("kind") == "token":
            hit = next((t for t in a.get("tokens") or [] if t and PB.N(t) in seg), None)
            atoms.append({"atom": n, "present": bool(hit), "span": hit})
        else:
            unread.append(n)
    if unread:
        return None, "atoms unread by the intake reader: " + ", ".join(unread)
    obs = {"key": slug, "entry": slug, "obs_index": 1, "target_id": S["id"], "reached": reading.get("reached") or {"kind": "same"}, "atoms": atoms,
           "src": reading.get("src"), "inversions": reading.get("inversions") or [], "standing_substitutions": reading.get("standing_substitutions") or [],
           "notes": reading.get("notes")}
    keep = (PB.BD, PB.GROUPS)
    try:
        with tempfile.TemporaryDirectory() as td:
            PB.BD = pathlib.Path(td); PB.GROUPS = ["I"]
            (PB.BD / "batch-I.json").write_text(json.dumps([{"key": slug, "entry": slug, "obs_index": 1, "q": q, "date": date, "surface": surface, "transcript": transcript}], ensure_ascii=False), encoding="utf-8")
            (PB.BD / "out-I.json").write_text(json.dumps({"new_atom_sets": [], "observations": [obs]}, ensure_ascii=False), encoding="utf-8")
            sets, by_id, grp = PB.load(); new, bad, cnt = PB.verify(by_id, grp)
            if bad:
                return None, "verification misses: " + "; ".join(str(b) for b in bad[:6])
            row = PB.score(by_id, new, grp)[0]; pd = PB.pd_of(row, on=date)
    finally:
        PB.BD, PB.GROUPS = keep
    pd["read"]["by"] = by; pd["read"]["brief"] = brief or "the draft's per_reading"
    return pd, None
