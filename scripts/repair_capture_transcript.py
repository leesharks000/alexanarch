#!/usr/bin/env python3
"""repair_capture_transcript.py -- replace a partial transcript with the complete session.

WHY THIS EXISTS. A capture was seated from the first rounds of a session that continued.
The entry's transcript was therefore complete as captured and incomplete as a record of the
observation. The registry's own contract is that THE TRANSCRIPT IS THE CAPTURE, so a partial
transcript is not a lesser record of the same thing -- it is a record of a different, smaller
thing, and the remaining rounds are evidence that was thrown away.

This is a REPAIR and not a re-seat: same address, same surface, same date, same observation.
Nothing is re-keyed. The prior transcript's length is recorded so the repair is visible.

    python3 repair_capture_transcript.py <slug> <transcript-file> <description-file>
"""
import json, pathlib, sys, datetime

ROOT = pathlib.Path(__file__).resolve().parents[1] if (pathlib.Path(__file__).resolve().parents[1]/"data").exists() else pathlib.Path("/home/claude/alexanarch")
REG = ROOT / "data" / "EA-WG-CAPTURES-01.json"

slug, tpath, dpath = sys.argv[1], sys.argv[2], sys.argv[3]
reg = json.loads(REG.read_text(encoding="utf-8"))
tx = pathlib.Path(tpath).read_text(encoding="utf-8").strip()
d  = pathlib.Path(dpath).read_text(encoding="utf-8").strip()

hit = [e for e in reg["entries"] if e.get("slug") == slug]
if not hit:
    sys.exit("no entry with slug " + slug)
e = hit[0]
old_len = len(e.get("transcript") or "")
e["transcript"] = tx
e["d"] = d
e["transcript_complete"] = (
    f"COMPLETE -- the full session, nine rounds. REPAIRED {datetime.date.today().isoformat()}: "
    f"the entry was seated from the opening rounds only ({old_len} chars) while the session continued; "
    f"the remaining rounds are the substance and were being discarded. The transcript IS the capture, "
    f"so a partial one records a smaller object rather than the same object less fully."
)
e["transcript_read"] = f"READ IN FULL {datetime.date.today().isoformat()}"
REG.write_text(json.dumps(reg, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"repaired {slug}: transcript {old_len} -> {len(tx)} chars; description {len(d)} chars")
