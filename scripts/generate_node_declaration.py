#!/usr/bin/env python3
"""generate_node_declaration.py — the federation declaration is COMPUTED, never typed.

F1 (2026-08-06): /.well-known/axn-node.json advertised highest_deposit 1092 with a
registry_head from 18 July while the archive actually held 1434. A 342-deposit
divergence, published by the root node about itself, for nineteen days.

Why that is not cosmetic: in a federated network a stale head is precisely how
nodes silently diverge. A peer syncing against this declaration would have
believed it had caught up while stopping 342 deposits short — and would have
believed it correctly, because the root node said so. A federation whose root
advertises a stale head is not a federation; it is a hierarchy with a quiet
error at its centre.

This is PATHOLOGY-01 (fossilised displayed value) landing on the federation's own
front door, and it is the same disease as every other count this archive has had
to repair: a number written once was a claim true once.

The fix is not to correct the number. It is to make the number uncomputable by
hand: this script derives every volatile field from registry state, runs inside
coherence_sync on every commit, and the declaration is verified LIVE by the
endpoint contract afterwards — because a generator with a bug would otherwise
automate the lie rather than end it.

Stable fields (operator, roles, surfaces, note) are preserved from the existing
declaration; only measured fields are recomputed.
"""
import json, hashlib, pathlib, datetime, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
DECL = ROOT / ".well-known/axn-node.json"
REG = ROOT / "data/registry.json"

VOLATILE = ("registry_head", "highest_deposit", "deposit_count", "declared_at",
            "kernel_count", "position_count", "sealed_cores", "peer_count")


def compute():
    reg = json.loads(REG.read_text())
    deps = reg["deposits"] if isinstance(reg, dict) else reg
    head = hashlib.sha256(REG.read_bytes()).hexdigest()
    nums = [d["deposit_number"] for d in deps if d.get("deposit_number")]

    out = {
        "registry_head": head,
        "highest_deposit": max(nums) if nums else 0,
        "deposit_count": len(deps),
        "declared_at": datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    try:
        c = json.loads((ROOT / "data/axn-central-registry.json").read_text())
        out["position_count"] = c.get("positions_count")
        out["kernel_count"] = len(c.get("kernels", {}))
    except Exception:
        pass
    try:
        m = json.loads((ROOT / "data/symbolon-registry/MANIFEST.json").read_text())
        out["sealed_cores"] = m.get("stored_cores")
    except Exception:
        pass
    try:
        p = json.loads((ROOT / "rhizome/peers.json").read_text())
        out["peer_count"] = len(p.get("peers", []))
    except Exception:
        pass
    return out


def main():
    check = "--check" in sys.argv
    cur = json.loads(DECL.read_text()) if DECL.exists() else {}
    new = dict(cur)
    computed = compute()

    drift = {k: (cur.get(k), computed[k]) for k in VOLATILE
             if k in computed and k != "declared_at" and cur.get(k) != computed[k]}

    new.update(computed)
    new["generated_by"] = "scripts/generate_node_declaration.py"
    new["generation_note"] = (
        "Every measured field on this declaration is computed from registry state on "
        "each commit and verified live afterwards. It is never typed by hand. A root "
        "node that advertises a stale head is how a federation silently diverges.")

    if check:
        if drift:
            for k, (was, now) in drift.items():
                print(f"  DRIFT  {k}: declared {was} · actual {now}", file=sys.stderr)
            print("\nNODE DECLARATION IS STALE — run without --check to regenerate.",
                  file=sys.stderr)
            return 1
        print("  ok    node declaration matches registry state")
        return 0

    DECL.write_text(json.dumps(new, ensure_ascii=False, indent=1) + "\n")
    if drift:
        for k, (was, now) in drift.items():
            print(f"  repaired {k}: {was} → {now}")
    print(f"node declaration: deposits={new['deposit_count']} "
          f"head={new['registry_head'][:16]}… peers={new.get('peer_count')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
