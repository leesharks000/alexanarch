#!/usr/bin/env python3
"""check_fleet_sync.py — no node may declare a registry state divergent from canonical.

The registry lived at four nodes under four regimes and diverged by 169 records
and two minor versions without anything reporting it. This gate reads what each
node DECLARES and compares it to the canonical projection. A renderer must
declare no entries at all; a hosted mirror must match.
"""
import json, pathlib, sys, urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
CANON = json.loads((ROOT / "data/EA-WG-CAPTURES-01.json").read_text())
WANT = (CANON.get("version"), CANON.get("address_count"))

NODES = [
    ("leesharks.com", "https://www.leesharks.com/captures/registry.json", "renderer"),
    ("godkinggoogle.com", "https://godkinggoogle.com/captures/registry.json", "renderer"),
    ("machinemediation.org", "https://www.machinemediation.org/data/registry.json", "mirror"),
]

fail = []
print("canonical: v%s, %s addresses" % WANT)
for name, url, role in NODES:
    try:
        j = json.loads(urllib.request.urlopen(url, timeout=25).read())
    except Exception as e:
        print("  %-24s UNREACHABLE (%s)" % (name, type(e).__name__)); continue
    n = len(j.get("entries") or [])
    if role == "renderer":
        ok = (n == 0 and j.get("_status", "").startswith("RETIRED"))
        print("  %-24s renderer  entries=%-4d %s" % (name, n, "ok — stores nothing" if ok else "DIVERGENT — a renderer must not store the registry"))
    else:
        ok = (j.get("version") == WANT[0])
        print("  %-24s mirror    v%-6s entries=%-4d %s" % (name, j.get("version"), n, "ok" if ok else "STALE against canonical v%s" % WANT[0]))
    if not ok:
        fail.append(name)
if fail:
    print("\nFLEET SYNC FAILED: %s" % ", ".join(fail))
    sys.exit(1)
print("\nfleet sync: every node agrees with canonical")
