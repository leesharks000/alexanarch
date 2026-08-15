#!/usr/bin/env python3
"""check_supersession_terminal.py — does every edition reach current state in ONE hop?

THE DEFECT THIS CLOSES. Forward pointers were being written as a CHAIN: v1 → v2 →
v3 → … → v7. A chain looks complete and is not. A reader who arrives at v4.1 from
a search engine and follows one pointer lands on v4.2, which is also stale. The
Central Navigation Map's v4.1 pointed to another v4.1 — sideways, to a sibling.

The archive's own instruments say why this matters: an edition a retrieval layer
is likely to hold must reach current state without requiring the reader to keep
walking. A reader who stops walking is stranded, and most readers stop.

This gate asserts that no edition of a terminal-bearing family points anywhere
except directly at its terminal, and that no terminal points onward.
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
REG = ROOT / "data" / "registry.json"


def main():
    deposits = json.loads(REG.read_text())["deposits"]
    by_num = {d["deposit_number"]: d for d in deposits}

    terminals = {d["deposit_number"]: d["supersession_terminal_for"]["family"]
                 for d in deposits if d.get("supersession_terminal_for")}
    if not terminals:
        print("no terminal-bearing families declared")
        return 0

    fails = []
    counts = {t: 0 for t in terminals}
    for d in deposits:
        tgt = d.get("superseded_by_deposit_number")
        if tgt is None:
            continue
        n = d["deposit_number"]
        if n in terminals:
            fails.append(f"#{n} is a TERMINAL for {terminals[n]} but points onward to #{tgt}")
            continue
        if tgt in terminals:
            counts[tgt] += 1
            continue
        # pointing at a non-terminal: is that non-terminal itself in a family?
        hop = by_num.get(tgt, {}).get("superseded_by_deposit_number")
        if hop is not None:
            fails.append(
                f"#{n} points to #{tgt}, which points onward to #{hop} — "
                f"CHAIN, not terminal. A reader who follows one pointer is still stale.")

    print("terminal families")
    for t, fam in sorted(terminals.items()):
        print(f"  #{t:<5} {fam:<26} ← {counts[t]} editions, all one hop")

    for f in fails:
        print(f"  FAIL  {f}", file=sys.stderr)
    if fails:
        print("\nA chain looks complete and is not. Point every edition at the terminal.",
              file=sys.stderr)
        return 1
    print("EVERY EDITION REACHES CURRENT STATE IN ONE HOP")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
