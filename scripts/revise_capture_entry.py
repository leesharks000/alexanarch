#!/usr/bin/env python3
"""revise_capture_entry.py -- revise a seated capture in place from its re-authored intake draft.

WHY THIS EXISTS. A capture is sometimes seated from the opening turns of a session that continues. The transcript is the
capture, so the later turns belong to the same observation, and they arrive as a fuller paste of the same session. This
is a REVISION and not a re-seat: same address, same surface, same date, same observation, same slug. Identity fields are
kept; the content fields are replaced from the draft; the prior transcript length is printed and the draft records it in
transcript_complete, so the revision is visible. (Generalizes repair_capture_transcript.py, whose text is fixed to one case.)

    python3 scripts/revise_capture_entry.py <slug> <draft.json>
"""
import json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
REG = ROOT / "data" / "EA-WG-CAPTURES-01.json"
KEEP = {"slug", "addr_id", "obs_id", "q", "surface", "date", "dates", "series", "citable_unit", "cite", "links", "other_slugs",
        "observations", "n_observations", "surfaces"}

slug, dpath = sys.argv[1], sys.argv[2]
reg = json.loads(REG.read_text(encoding="utf-8"))
draft = json.loads(pathlib.Path(dpath).read_text(encoding="utf-8"))
hit = [e for e in reg["entries"] if e.get("slug") == slug]
if len(hit) != 1:
    sys.exit(f"expected one entry with slug {slug}, found {len(hit)}")
e = hit[0]
if draft.get("slug") != slug or draft.get("q") != e.get("q") or draft.get("surface") != e.get("surface") or draft.get("date") != e.get("date"):
    sys.exit("draft does not match the seated entry's slug, address, surface and date: a revision cannot re-key")
if e.get("n_observations", 1) > 1:
    sys.exit("entry has later observations; revise the observation, not the root")
old = len(e.get("transcript") or "")
changed = []
for k, v in draft.items():
    if k in KEEP or k not in e:
        continue
    if e[k] != v:
        e[k] = v; changed.append(k)
REG.write_text(json.dumps(reg, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"revised {slug}: transcript {old} -> {len(e.get('transcript') or '')} chars; fields changed: {', '.join(changed)}")
