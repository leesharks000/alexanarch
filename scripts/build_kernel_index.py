#!/usr/bin/env python3
"""build_kernel_index.py — emit api/kernel-index.json: full-sha256 → registered identity.
The reverse direction of the registry (bytes → AXN). Run after any mint.
"""
import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
reg = json.loads((ROOT/'data/registry.json').read_text())
idx = {}
for d in reg['deposits']:
    h = d.get('hash')
    if h:
        idx[h] = {"axn": d['axn'], "deposit_number": d['deposit_number'],
                  "record": f"/s/records/{d['deposit_number']}/"}
out = {"description": "Full SHA-256 identity kernel → registered AXN. The reverse lookup: enter bytes, hash them, find the record.",
       "count": len(idx), "kernels": idx}
(ROOT/'api/kernel-index.json').write_text(json.dumps(out, ensure_ascii=False, separators=(',',':')) + '\n')
print("kernel-index:", len(idx), "kernels")
