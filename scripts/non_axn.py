#!/usr/bin/env python3
"""non_axn.py — the AXN mint route of the Negative of the Negative (axn/v2.3, non_entries; ruled 2026-10-24).

Every entry of /non with a composed row (datasets/negative-of-the-negative/v2/rows/<entity>.json) takes one position in
the AXN sequence and the family NON. The entry's root, AXN:<hex>.NON, is its identifier across its compositions; each
composition of the row is a version, AXN:<hex>.NON.<glyph>, the glyph derived from the first 6 bytes of sha256 of the
row file's bytes, and minted once. When the row's bytes change, a new version is minted at the same position and the
earlier version is kept in the entry's history with its hash, date and reason ("the row, with history").

The ledger is datasets/negative-of-the-negative/v2/axn.json. The AXN is not written into the row, whose bytes it is
derived from. Positions come from the shared allocation ledger (data/symbolon-registry/allocation.json), under its rule
max(registry hex, ledger) + 1, and the ledger is advanced past each allocation, so a deposit, a symbolon witness and a
/non entry never share a position.

Usage:
    python3 scripts/non_axn.py                       # mint new entries; mint a new version where a row changed
    python3 scripts/non_axn.py --reason "landed …"   # the reason recorded on any new version
    python3 scripts/non_axn.py --date 2026-10-24     # the date recorded (default: today, UTC)
    python3 scripts/non_axn.py --check               # report entries unminted or changed; write nothing (exit 0)
"""
import argparse, datetime, hashlib, json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from axn_lib import axn_glyph_from_hash, compose_axn  # noqa: E402

V2 = ROOT / "datasets/negative-of-the-negative/v2"
LEDGER = V2 / "axn.json"
ALLOC = ROOT / "data/symbolon-registry/allocation.json"
FAMILY = "NON"


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def load_ledger():
    if LEDGER.exists():
        return json.loads(LEDGER.read_text(encoding="utf-8"))
    return {"_what_this_is": ("The AXN ledger of the Negative of the Negative (axn/v2.3, non_entries): one entry per composed row. "
                              "root is the entry across its compositions; axn is the current version, derived from the row file's "
                              "sha256; history holds the earlier versions, each still an identifier of the composition it named."),
            "family": FAMILY, "protocol": "/api/axn-protocol.json#non_entries", "minted_by": "scripts/non_axn.py", "entries": {}}


def positioned_kernels():
    """sha256 values already holding a position: deposit kernels and symbolon witnesses (one kernel, one position)."""
    out = set()
    try:
        for k in json.loads((ROOT / "data/api/kernel-index.json").read_text()).get("kernels", {}):
            out.add(k)
    except Exception:
        pass
    sdir = ROOT / "data/symbolon-registry/entries"
    if sdir.is_dir():
        for f in sdir.glob("*.json"):
            try:
                t = json.loads(f.read_text()).get("tuple", {})
            except Exception:
                continue
            for k in ("axn0", "axn1"):
                if (t.get(k) or {}).get("sha256"):
                    out.add(t[k]["sha256"])
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--reason", default=None)
    ap.add_argument("--date", default=datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d"))
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()

    led = load_ledger()
    E = led["entries"]
    rows = sorted((V2 / "rows").glob("*.json"))
    # mint order for entries without a position: the row's epoch, then the entity
    def epoch(p):
        try:
            return str(json.loads(p.read_text(encoding="utf-8")).get("epoch") or "")
        except Exception:
            return ""
    new = sorted((p for p in rows if p.stem not in E), key=lambda p: (epoch(p), p.stem))
    changed = [p for p in rows if p.stem in E and sha(p) != E[p.stem]["sha256"]]
    gone = sorted(k for k in E if not (V2 / "rows" / f"{k}.json").exists())

    if a.check:
        for p in new:
            print(f"unminted: {p.stem}")
        for p in changed:
            print(f"changed since {E[p.stem]['axn']}: {p.stem} (a new version is minted on the next run)")
        for k in gone:
            print(f"row absent: {k} ({E[k]['axn']}) — the entry is kept")
        print(f"non axn: {len(E)} entries, {len(new)} unminted, {len(changed)} changed, {len(gone)} rows absent")
        return 0

    reg = json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))
    reg_max = max(int(d["hex"], 16) for d in reg["deposits"] if d.get("hex"))
    alloc = json.loads(ALLOC.read_text(encoding="utf-8"))
    taken = positioned_kernels()
    nxt = max(reg_max + 1, int(alloc["next_hex"], 16), __import__('axn_positions').next_free())  # 2026-10-28: the floor includes origin/main
    minted, versioned = [], []
    for p in new:
        h = sha(p)
        if h in taken:
            print(f"refused: {p.stem} — its sha256 {h[:16]}… already holds a position (one kernel, one position)", file=sys.stderr)
            continue
        hx = f"{nxt:04X}"; nxt += 1
        axn = compose_axn(hx, FAMILY, axn_glyph_from_hash(h))
        E[p.stem] = {"entity": p.stem, "hex": hx, "root": f"AXN:{hx}.{FAMILY}", "axn": axn, "sha256": h,
                     "row": f"datasets/negative-of-the-negative/v2/rows/{p.stem}.json", "page": f"/non/{p.stem}/",
                     "minted": a.date, "history": []}
        minted.append((p.stem, axn))
    for p in changed:
        e = E[p.stem]; h = sha(p)
        e["history"].append({"axn": e["axn"], "sha256": e["sha256"], "from": e.get("version_date") or e["minted"],
                             "until": a.date, "reason": a.reason or "the row's bytes changed (recomposition)"})
        e["axn"] = compose_axn(e["hex"], FAMILY, axn_glyph_from_hash(h))
        e["sha256"] = h
        e["version_date"] = a.date
        versioned.append((p.stem, e["axn"]))
    if minted:
        last = f"{nxt - 1:04X}"
        if int(alloc["next_hex"], 16) <= nxt - 1:
            alloc["next_hex"] = f"{nxt:04X}"
            alloc["last_allocated"] = last
            alloc["last_allocated_at"] = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
            alloc["last_allocator"] = "non-axn (scripts/non_axn.py)"
            ALLOC.write_text(json.dumps(alloc, ensure_ascii=False, indent=1))
    led["entries"] = dict(sorted(E.items()))
    LEDGER.write_text(json.dumps(led, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    for k, x in minted:
        print(f"minted {x}  {k}")
    for k, x in versioned:
        print(f"new version {x}  {k}")
    for k in gone:
        print(f"row absent: {k} ({E[k]['axn']}) — the entry is kept", file=sys.stderr)
    print(f"non axn: {len(E)} entries; {len(minted)} minted, {len(versioned)} new versions")
    return 0


if __name__ == "__main__":
    sys.exit(main())
