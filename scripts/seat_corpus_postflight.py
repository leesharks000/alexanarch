#!/usr/bin/env python3
"""seat_corpus_postflight.py — a corpus is seated when four surfaces agree.

    1. SEAT      data/corpora/<name>/ with originals, text, source.json, MANIFEST.sha256
    2. INDEX     data/api/corpora.json carries the seat
    3. DEPOSIT   an EA-CORPORA-0N deposit assigns the card number
    4. SHELF     originals/<name>/ renders on traininglayerliterature.org

Exit 0 means seated. Any other exit means the corpus exists somewhere and is
invisible somewhere else, which is the failure this file was written for.

WHY IT EXISTS

On 2026-08-28 Aristotle and Plotinus were built into data/corpora/, added to the
index, and never reached the shelf — because the shelf had no generator and was
maintained by hand. The check then found the index itself had drifted to
seventeen of thirty-nine seats: the second and third seatings never reached it
either. Two of the four surfaces had been quietly wrong for weeks.

This is the same splitbrain the capture registry had, and it has the same cure.
The registry knowing a thing is not the same as the surface saying it, and the
only thing that holds across sessions is a check that fails. The archive's rule:
a corpus that exists only inside a data directory is not published, it is stored.

USAGE
    python3 scripts/seat_corpus_postflight.py --tll /path/to/traininglayerliterature-org
    python3 scripts/seat_corpus_postflight.py --tll ... --corpus plotinus
"""
import argparse, json, pathlib, re, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SEATS = ROOT / "data/corpora"
INDEX = ROOT / "data/api/corpora.json"
REG = ROOT / "data/registry.json"
REQUIRED = ("source.json", "MANIFEST.sha256")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--tll", required=True)
    ap.add_argument("--corpus", help="check one seat rather than all")
    a = ap.parse_args()

    shelf_dir = pathlib.Path(a.tll) / "originals"
    seats = sorted(d.name for d in SEATS.iterdir() if d.is_dir())
    if a.corpus:
        if a.corpus not in seats:
            print(f"no such seat: {a.corpus}"); return 2
        seats = [a.corpus]

    idx = json.loads(INDEX.read_text())
    indexed = {c["corpus"] for c in idx["corpora"]}
    shelf = {d.name for d in shelf_dir.iterdir() if d.is_dir()} if shelf_dir.exists() else set()
    reg_blob = REG.read_text()

    fails = []
    print(f"[postflight] {len(seats)} seat(s) · index {len(indexed)} · shelf {len(shelf)}\n")
    for name in seats:
        seat = SEATS / name
        row = []
        # 1 SEAT
        miss = [f for f in REQUIRED if not (seat / f).exists()]
        has_payload = any(p.is_dir() for p in seat.iterdir())
        if miss or not has_payload:
            row.append(f"SEAT incomplete ({', '.join(miss) or 'no payload directory'})")
        # 2 INDEX
        if name not in indexed:
            row.append("not in data/api/corpora.json")
        # 3 DEPOSIT — the seat names its card, and the card number must appear in a deposit
        card = None
        try:
            card = json.loads((seat / "source.json").read_text()).get("seat")
        except Exception:
            pass
        if not card or "unnumbered" in str(card):
            row.append("source.json declares no EA-CORPORA card number")
        elif card.split("/")[0] not in reg_blob:
            row.append(f"no deposit carries the seating series {card.split('/')[0]}")
        # 4 SHELF
        if name not in shelf:
            row.append("no rendered card at originals/<name>/")
        elif not (shelf_dir / name / "index.html").exists():
            row.append("shelf directory present but empty")
        if row:
            fails.append((name, row))
            print(f"  FAIL  {name}")
            for r in row:
                print(f"          {r}")
        else:
            print(f"  ok    {name}  {card}")

    print()
    if fails:
        print(f"{len(fails)} seat(s) not seated.")
        print("A corpus that exists only inside a data directory is not published, it is stored.")
        print("\nTo finish a seat:")
        print("  python3 scripts/build_originals_shelf.py --tll <tll> --corpus <name> --card-no EA-CORPORA-0N/NN")
        print("  add the entry to the shelf index at originals/index.html")
        print("  mint or extend the EA-CORPORA-0N seating deposit")
        return 1
    print("SEATED — seat, index, deposit and shelf agree.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
