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
    # 2026-10-27: the hash a record carried before its AXN was re-derived still finds the record,
    # marked as a prior kernel (the bytes it names may be an earlier state of the text, or none the archive holds).
    for x in (d.get('axn_prior') or []):
        if x.get('hash') and x['hash'] not in idx:
            idx[x['hash']] = {"axn": d['axn'], "prior_axn": x.get('axn'), "deposit_number": d['deposit_number'],
                              "record": f"/s/records/{d['deposit_number']}/", "status": "prior", "why": x.get('why')}
# 2026-10-27: capture observations, each sealed with its analysis and measures (data/captures/sealed/), find their AXN.
_cl = ROOT/'data/captures/axn.json'
if _cl.exists():
    for slug, a in json.loads(_cl.read_text())['addresses'].items():
        for k, o in a['observations'].items():
            idx.setdefault(o['sha256'], {"axn": o['axn'], "root": a['root'], "observation": k, "sealed": o['file'],
                                         "record": f"/captures/{slug}/", "source": "capture"})
# 2026-10-27: releases (data/releases/axn.json): the SHA-256 of a release's manifest, or of a one-file instrument, finds its AXN.
_rl = ROOT/'data/releases/axn.json'
if _rl.exists():
    for k, L in json.loads(_rl.read_text())['objects'].items():
        for r in L.get('releases') or []:
            idx.setdefault(r['sha256'], {"axn": r['axn'], "root": L['root'], "object": k, "label": r['label'], "source": "release",
                                         "record": f"/s/axn/{L['hex']}/", **({"manifest": r['manifest']} if r.get('manifest') else {"file": r.get('file')})})
out = {"description": "Full SHA-256 identity kernel → registered AXN. The reverse lookup: enter bytes, hash them, find the record.",
       "count": len(idx), "kernels": idx}
(ROOT/'data/api/kernel-index.json').write_text(json.dumps(out, ensure_ascii=False, separators=(',',':')) + '\n')
print("kernel-index:", len(idx), "kernels")
