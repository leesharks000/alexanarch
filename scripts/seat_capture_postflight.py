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
  (2026-09-21) LINK build_capture_links.py runs before BAKE, and CITE
  audit_capture_citability.py runs after SYNC — see the STEPS comment.
  (2026-09-25) ADDR build_semantic_addresses.py and PAGE
  publish_semantic_addresses.py run after GATE and before SYNC, so every
  seated query has its /addresses/{slug}/ page in the same commit and the
  datasets/ copy of the address layer is current.

Run it after EVERY registry write — new capture, edit, or removal:

    python3 scripts/seat_capture_postflight.py

Exit 0 means the tab, the data file, and the projection agree. Anything else
means the seat is incomplete and the commit should not be pushed.
"""
import subprocess, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]

STEPS = [
    # 2026-09-21: LINK before BAKE. build_capture_links.py writes each observation's `cite`; without it a
    # newly seated observation has no citation, audit_capture_citability fails, and nothing here said so.
    # Five seatings on 2026-09-21 hit it. Links first, so the bake and the projection carry them.
    ("LINK", [sys.executable, "scripts/build_capture_links.py"]),
    ("BAKE", [sys.executable, "scripts/build_capture_gallery.py"]),
    ("GATE", [sys.executable, "scripts/check_capture_page_current.py"]),
    # 2026-09-25: ADDR and PAGE after GATE, before SYNC (SYNC copies semantic-addresses.json into datasets/). The semantic address layer (/addresses/{slug}/) is the registry's
    # per-query, machine-fetchable surface, and it regenerated only on deposit mint, so a capture seated
    # between mints had no address page: 23 on 2026-09-25, and 232 addresses had data but no page.
    # Both scripts are deterministic; unchanged addresses produce no diff.
    ("ADDR", [sys.executable, "scripts/build_semantic_addresses.py"]),
    ("PAGE", [sys.executable, "scripts/publish_semantic_addresses.py"]),
    ("SYNC", [sys.executable, "scripts/sync_capture_dataset.py"]),
    ("CITE", [sys.executable, "scripts/audit_capture_citability.py"]),
]


def main():
    # 2026-09-05: the registry gate — schema (fixed shape), no-loss (transcripts/images never discarded), order (sections grouped)
    import subprocess as _sp
    _r = _sp.run([sys.executable, str(ROOT / "scripts/check_capture_registry.py"), "--base", "origin/main"], cwd=ROOT)
    if _r.returncode: print("[postflight] REGISTRY GATE FAILED — the capture is NOT seated."); return 1
    # 2026-09-15: the transcript gate. Intake refuses thin drafts, but nothing checked the units seated
    # before the contract, so 34 citable units carried no machine text and were invisible without a hand
    # audit. The transcript IS the capture; this makes the count monotone.
    _t = _sp.run([sys.executable, str(ROOT / "scripts/audit_transcript_coverage.py"), "--check"], cwd=ROOT)
    if _t.returncode: print("[postflight] TRANSCRIPT GATE FAILED — a citable unit has no machine text. NOT seated."); return 1
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
