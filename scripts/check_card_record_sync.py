#!/usr/bin/env python3
"""check_card_record_sync.py — do the cards and the records still agree?

WHY. The nine-step card pass of 2026-08-17 corrected things in BOTH directions and
neither direction was detectable before a person looked at a page:

  RECORD WRONG, CARD RIGHT   Vox's record gave /ayanna/ as her surface. That is the
                             prose summary; the card is at /ayanna/who/. A full
                             pass was built on the wrong page before it was caught.
  CARD WRONG, RECORD RIGHT   Glas's record already read "Editor (duoviri, with
                             Talos Morrow)". His card still read "EDITOR-IN-CHIEF
                             Alice Thornburgh · ADVISORY EDITOR Nobel Glas".

A dataset and a surface that can disagree silently will. This checks the two
claims that matter and can be verified from outside: the card resolves, and the
editorial seat named on the card matches the venues data.

    python3 scripts/check_card_record_sync.py
"""
import json
import pathlib
import re
import sys
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]


def load():
    recs = {}
    for f in sorted((ROOT / "datasets/heteronyms/records").glob("*.json")):
        d = json.loads(f.read_text())
        blk = d.get("card_pass_2026_08_17") or {}
        surf = (blk.get("record_surfaces") or {})
        if surf.get("card"):
            recs[f.stem] = {"name": d["name"], "card": surf["card"], "where": surf.get("where")}
    venues = {}
    for f in sorted((ROOT / "datasets/venues/records").glob("*.json")):
        v = json.loads(f.read_text())
        for who in v["editorial"].get("duoviri") or []:
            venues.setdefault(who, []).append(v["canonical"])
    return recs, venues


def fetch(u):
    try:
        with urllib.request.urlopen(u, timeout=20) as r:
            return r.read().decode("utf-8", "replace")
    except Exception as exc:
        return f"__ERROR__{exc}"


def main():
    recs, venues = load()
    fails = 0
    for slug, r in recs.items():
        h = fetch(r["card"])
        if h.startswith("__ERROR__"):
            print(f"  {slug:<20}CARD UNREACHABLE  {r['card']}  {h[9:60]}")
            fails += 1
            continue
        seats = [c for who, cs in venues.items()
                 if r["name"].split()[-1] in who for c in cs]
        missing = [c for c in seats if c.split(":")[0][:26].lower() not in h.lower()]
        if missing:
            print(f"  {slug:<20}CARD DOES NOT NAME ITS SEAT: {missing}")
            fails += 1
        else:
            print(f"  {slug:<20}ok   {len(seats)} seat(s) named")
    print(f"\n{'FAIL' if fails else 'OK'}: {fails} card(s) out of sync with the venues data")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
