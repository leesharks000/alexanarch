#!/usr/bin/env python3
"""axn_positions.py — one AXN sequence, every claim on it, and no second claim on a position (2026-10-28).

MANUS, 2026-10-28: "lets make sure that position collisions arent possible going forward."

WHY COLLISIONS HAPPENED. The archive has one position sequence and several allocators: the deposit pipeline
(mint_deposit.py), the Capture Registry (capture_axn.py), /non (non_axn.py, nonreg_axn.py), releases
(release_axn.py), and the symbolon witness endpoint (api/register-symbolon.js). The endpoint allocates live,
on main, by compare-and-swap on data/symbolon-registry/allocation.json. Every other allocator runs in a session
checkout that cannot push and lands later as a bundle, reading the ledger and the registry as they stood when
the checkout was last fetched. On 2026-08-09 the endpoint allocated 05C5, 05C6, 05C9, 05CA and 05CB to five
witnesses between 16:37 and 16:39 UTC; a session minting #1441–#1447 from a stale checkout gave five of them the
same positions, and the bundle landed on top. A stale reader cannot be made fresh by care alone, so the rule is
closed at both ends:

  1. AT ALLOCATION. next_free() is the floor every session allocator uses: the highest position claimed in the
     checkout or on origin/main (fetched first, best effort), and the next_hex of both ledgers, plus one.
  2. AT LANDING. check_landing(base, head) reads every claim at main and at the bundle's head; a position the
     head claims for something other than what main holds there is a collision, and the apply-bundle workflow
     stops before pushing (.github/workflows/apply-bundle-from-issue.yml). The session re-mints from a fresh
     fetch. A position is an address: a collision is an address naming two things, so it is refused at the one
     place where it can be refused, the merge, and nothing on main moves.

WHAT COUNTS AS A CLAIM. A deposit's hex (data/registry.json); a Capture Registry address's root
(data/captures/axn.json); a /non entry (datasets/negative-of-the-negative/v2/axn.json) and a /non register
address with a position of its own (register-axn.json; addresses seated in both registers share the capture's
AXN and claim nothing further); a release object's root (data/releases/axn.json); a symbolon witness's position
(data/symbolon-registry/entries/). The seats of the originals shelf carry the hex of the deposit that numbers them
and are part of that claim. The five positions contested on 2026-08-09 are recorded in LEGACY_CONTESTED; they
await an allocation ruling (WAVE-HEXPOS-01) and are reported, never re-created.

    python3 scripts/axn_positions.py                     # report: claims by source, collisions, next free position
    python3 scripts/axn_positions.py --next              # print the next free position (fetches origin/main)
    python3 scripts/axn_positions.py --check-landing --base origin/main --head HEAD   # exit 1 on a new collision
"""
import json, pathlib, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
LEDGER = "data/symbolon-registry/allocation.json"
LEGACY_CONTESTED = {"05C5", "05C6", "05C9", "05CA", "05CB"}


def _git_show(ref, path):
    try:
        return subprocess.run(["git", "show", f"{ref}:{path}"], cwd=ROOT, capture_output=True, check=True).stdout.decode("utf-8")
    except Exception:
        return None


def _git_ls(ref, path):
    try:
        out = subprocess.run(["git", "ls-tree", "--name-only", f"{ref}:{path}"], cwd=ROOT, capture_output=True, check=True).stdout.decode()
        return [f"{path}/{x}" for x in out.split() if x.endswith(".json")]
    except Exception:
        return []


def reader(ref=None):
    """(read(path) -> text|None, ls(dir) -> [paths]) over the working tree (ref None) or a git ref."""
    if ref is None:
        def read(p):
            f = ROOT / p
            return f.read_text(encoding="utf-8") if f.exists() else None
        def ls(d):
            q = ROOT / d
            return sorted(f"{d}/{x.name}" for x in q.glob("*.json")) if q.exists() else []
        return read, ls
    return (lambda p: _git_show(ref, p)), (lambda d: _git_ls(ref, d))


def _j(read, p):
    t = read(p)
    try:
        return json.loads(t) if t else None
    except Exception:
        return None


def claims(ref=None):
    """{hex: [(source, key), ...]} — every claim on the sequence at ref (None: the working tree)."""
    read, ls = reader(ref)
    out = {}
    def add(h, src, key):
        if h:
            out.setdefault(str(h).upper(), []).append((src, str(key)))
    reg = _j(read, "data/registry.json") or {}
    for d in reg.get("deposits", []):
        add(d.get("hex"), "deposit", d.get("deposit_number"))
    for k, v in ((_j(read, "data/captures/axn.json") or {}).get("addresses") or {}).items():
        add(v.get("hex"), "capture", k)
    for k, v in ((_j(read, "datasets/negative-of-the-negative/v2/axn.json") or {}).get("entries") or {}).items():
        add(v.get("hex"), "non-entry", k)
    for k, v in ((_j(read, "datasets/negative-of-the-negative/v2/register-axn.json") or {}).get("addresses") or {}).items():
        add(v.get("hex"), "non-register", k)
    for k, v in ((_j(read, "data/releases/axn.json") or {}).get("objects") or {}).items():
        add(str(v.get("root", "")).split(":")[-1].split(".")[0] or None, "release", k)
    for p in ls("data/symbolon-registry/entries"):
        e = _j(read, p) or {}
        add(e.get("position"), "symbolon", p.rsplit("/", 1)[-1][:-5])
    return out


def collisions(cl):
    return {h: c for h, c in cl.items() if len(set(c)) > 1}


def _max_claimed(cl):
    return max((int(h, 16) for h in cl if all(ch in "0123456789ABCDEF" for ch in h)), default=-1)


def _ledger_next(read):
    try:
        return int(json.loads(read(LEDGER))["next_hex"], 16)
    except Exception:
        return 0


def next_free(fetch=True):
    """The floor for every session allocator: one past the highest claim in the checkout or on origin/main,
    and never below either ledger's next_hex. Fetching is best effort; offline, the checkout alone decides."""
    if fetch:
        subprocess.run(["git", "fetch", "-q", "origin", "main"], cwd=ROOT, capture_output=True)
    local_read, _ = reader(None)
    live_read, _ = reader("origin/main")
    n = max(_max_claimed(claims(None)) + 1, _ledger_next(local_read))
    if live_read(LEDGER):
        n = max(n, _max_claimed(claims("origin/main")) + 1, _ledger_next(live_read))
    return n


def check_landing(base, head):
    """New collisions at head that base does not have: a position head claims for something other than what base
    holds there, or a position claimed twice within head. Returns a list of report lines (empty: clean)."""
    b, h = claims(base), claims(head)
    lines = []
    for hx, cs in sorted(h.items()):
        if hx in LEGACY_CONTESTED:
            continue
        mine = set(cs)
        theirs = set(b.get(hx, []))
        if len(mine) > 1 and mine != theirs:
            lines.append(f"{hx}: claimed by {sorted(mine)} at head" + (f" (main holds {sorted(theirs)})" if theirs else ""))
        elif theirs and not (mine & theirs):
            lines.append(f"{hx}: head claims {sorted(mine)}; main holds {sorted(theirs)}")
    return lines


def main(argv):
    if "--check-landing" in argv:
        base = argv[argv.index("--base") + 1] if "--base" in argv else "origin/main"
        head = argv[argv.index("--head") + 1] if "--head" in argv else "HEAD"
        lines = check_landing(base, head)
        if lines:
            print("AXN POSITION COLLISION — the bundle claims positions main already holds for something else:")
            for x in lines:
                print("  " + x)
            print("Re-mint from a fresh fetch (scripts/axn_positions.py --next gives the floor); nothing was pushed.")
            return 1
        print("axn positions: no new collision")
        return 0
    if "--next" in argv:
        print(f"{next_free():04X}")
        return 0
    cl = claims(None)
    by = {}
    for cs in cl.values():
        for s, _ in cs:
            by[s] = by.get(s, 0) + 1
    col = collisions(cl)
    print("claims:", ", ".join(f"{k} {v}" for k, v in sorted(by.items())))
    print(f"collisions: {len(col)} ({len([h for h in col if h in LEGACY_CONTESTED])} legacy contested awaiting ruling)")
    for hx, cs in sorted(col.items()):
        print(f"  {hx}{' (legacy)' if hx in LEGACY_CONTESTED else ''}: {sorted(set(cs))}")
    print(f"next free position: {next_free(fetch=False):04X} (checkout; --next fetches origin/main)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
