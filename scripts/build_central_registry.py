#!/usr/bin/env python3
"""Central AXN registry: one index across every route a kernel can enter the
sequence — formal deposits, symbolon witnessings, and (future) mandala-book
and petition mints. Position-keyed and kernel-keyed. Regenerate after any
mint or witnessing; the witness endpoint's entries are read directly."""
import json, pathlib, datetime
ROOT = pathlib.Path(__file__).resolve().parent.parent
reg = json.loads((ROOT/"data/registry.json").read_text())
deps = reg["deposits"] if isinstance(reg, dict) else reg
try: kidx = json.loads((ROOT/"api/kernel-index.json").read_text()).get("kernels", {})
except Exception: kidx = {}
sha_by_axn = {v["axn"]: k for k, v in kidx.items()}

positions, kernels = {}, {}
for d in deps:
    hx = d.get("hex"); axn = d.get("axn")
    if not hx: continue
    e = {"axn": axn, "source": "deposit", "deposit_number": d["deposit_number"],
         "title": (d.get("title") or "")[:110], "record": f"/s/records/{d['deposit_number']}/",
         "status": "deposited"}
    positions[hx] = e
    sha = sha_by_axn.get(axn)
    if sha: kernels[sha] = {"role": "axn0", **e}

sdir = ROOT/"data/symbolon-registry/entries"
n_sym = 0
if sdir.is_dir():
    for f in sorted(sdir.glob("*.json")):
        try: s = json.loads(f.read_text())
        except Exception: continue
        hx = s.get("position")
        if not hx: continue
        e = {"axn": s.get("axn"), "source": "symbolon-witness", "status": s.get("status"),
             "entry": f"/data/symbolon-registry/entries/{f.name}",
             "filename": (s.get("seed_a") or {}).get("manifest", [{}])[0].get("filename"),
             "retrieval": s.get("retrieval")}
        positions[hx] = e; n_sym += 1
        t = s.get("tuple", {})
        if t.get("axn0", {}).get("sha256"): kernels[t["axn0"]["sha256"]] = {"role": "axn0", **e}
        if t.get("axn1", {}).get("sha256"): kernels[t["axn1"]["sha256"]] = {"role": "axn1_stamped_form", **e}

out = {"description": "Central AXN registry: every allocated position across all mint routes, position- and kernel-keyed.",
       "generated": datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
       "positions_count": len(positions), "symbolon_entries": n_sym,
       "positions": dict(sorted(positions.items())), "kernels": kernels}
(ROOT/"data/axn-central-registry.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))
print(f"central registry: {len(positions)} positions ({n_sym} symbolon) · {len(kernels)} kernels")
