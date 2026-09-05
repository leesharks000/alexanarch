#!/usr/bin/env python3
"""seat_capture_postflight.py — a capture is not seated until this exits 0.

THE RULING (MANUS, 2026-08-27). The canonical rendered surface of the Capture
Registry is the captures tab — /captures/ on alexanarch. Writing the entry into
data/EA-WG-CAPTURES-01.json and syncing datasets/capture-registry/ is NOT a
seat: the tab is a baked static page, and until it is rebaked the capture does
not exist where the registry is read.

THE DEFECT THIS CLOSES (2026-08-27, third occurrence of the 2026-08-15 shape).
A capture was authored to the data file, the datasets projection was synced,
the commit pushed, live verification passed on the projection — and the tab
still showed 371 of 372. Three silent gaps, again:

  1. build_capture_gallery.py chained to nothing — the seat path simply did
     not include the bake.
  2. Schema drift crashed the bake invisibly (cite_list as strings where the
     renderer wants {site,title,snip} dicts; missing section field 's';
     stale top-level address_count) — and a crashed bake leaves the previous
     bytes: valid HTML, correctly served, wrong.
  3. The currency gate (check_capture_page_current.py) exists and was not run.

THE SEQUENCE, in order, each step refusing to proceed on failure:

  1. BAKE   build_capture_gallery.py        — registry -> anchored cards
  2. GATE   check_capture_page_current.py   — page count == registry count,
                                              every entry sectioned
  3. SYNC   sync_capture_dataset.py         — data/ -> datasets/ projection
                                              + regenerated manifest

Run it after EVERY registry write — new capture, edit, or removal:

    python3 scripts/seat_capture_postflight.py

Exit 0 means the tab, the data file, and the projection agree. Anything else
means the seat is incomplete and the commit should not be pushed.
"""
import subprocess, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]

STEPS = [
    ("BAKE", [sys.executable, "scripts/build_capture_gallery.py"]),
    ("GATE", [sys.executable, "scripts/check_capture_page_current.py"]),
    ("SYNC", [sys.executable, "scripts/sync_capture_dataset.py"]),
]


def main():
    # 2026-09-05: the registry gate — schema (fixed shape), no-loss (transcripts/images never discarded), order (sections grouped)
    import subprocess as _sp
    _r = _sp.run([sys.executable, str(ROOT / "scripts/check_capture_registry.py"), "--base", "origin/main"], cwd=ROOT)
    if _r.returncode: print("[postflight] REGISTRY GATE FAILED — the capture is NOT seated."); return 1
    for name, cmd in STEPS:
        print(f"[postflight] {name}: {' '.join(cmd[1:])}")
        r = subprocess.run(cmd, cwd=ROOT)
        if r.returncode != 0:
            print(f"[postflight] {name} FAILED (exit {r.returncode}) — "
                  f"the capture is NOT seated. Fix and re-run; do not push.")
            return r.returncode
    print("[postflight] SEATED — tab, data file, and projection agree.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
