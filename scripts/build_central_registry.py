#!/usr/bin/env python3
"""Central AXN registry: one index across every route a kernel can enter the
sequence — formal deposits, symbolon witnessings, /non entries (axn/v2.3), and (future) mandala-book
and petition mints. Position-keyed and kernel-keyed. Regenerate after any
mint or witnessing; the witness endpoint's entries are read directly.

WAVE-HEXPOS-01 hardening (2026-08-06):
  (1) position keys normalized to 4-char uppercase hex at build time;
  (2) a position claimed by two records is NEVER silently overwritten —
      it is emitted as a CONTESTED entry naming every claimant, and the
      build prints a loud warning (silent last-write-wins dropped #856
      from position 0365 in every build before this one);
  (3) labels retired via axn_history are emitted as alias entries
      (status superseded-label, alias_of -> current key) so every
      identifier ever published keeps resolving."""
import json, pathlib, datetime, re, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
reg = json.loads((ROOT/"data/registry.json").read_text())
deps = reg["deposits"] if isinstance(reg, dict) else reg
try: kidx = json.loads((ROOT/"data/api/kernel-index.json").read_text()).get("kernels", {})
except Exception: kidx = {}
sha_by_axn = {v["axn"]: k for k, v in kidx.items()}

def norm(hx):
    return (hx or "").strip().upper().zfill(4)

positions, kernels, aliases, contested = {}, {}, {}, {}

def claim(hx, e):
    """Register a claim on a position; collisions become CONTESTED, never overwrites."""
    if hx in contested:
        contested[hx]["claimants"].append(e); return
    if hx in positions:
        prev = positions.pop(hx)
        contested[hx] = {"status": "CONTESTED", "note": "position claimed by multiple records; "
                         "resolution is a MANUS allocation ruling (WAVE-HEXPOS-01)",
                         "claimants": [prev, e]}
        return
    positions[hx] = e

for d in deps:
    hx = norm(d.get("hex")); axn = d.get("axn")
    if hx == "0000" and not d.get("hex"): continue
    e = {"axn": axn, "source": "deposit", "deposit_number": d["deposit_number"],
         "title": (d.get("title") or "")[:110], "record": f"/s/records/{d['deposit_number']}/",
         "status": "deposited"}
    _prior = [x for x in (d.get("axn_prior") or []) if x.get("axn")]
    if _prior:
        e["prior"] = [x["axn"] for x in _prior]  # 2026-10-27: prior forms name the same record
    claim(hx, e)
    sha = sha_by_axn.get(axn)
    if sha: kernels[sha] = {"role": "axn0", **e}
    for x in _prior:
        if x.get("hash") and x["hash"] not in kernels:
            kernels[x["hash"]] = {"role": "axn0-prior", "prior_axn": x["axn"], "until": x.get("until"), **e}
    # alias emission: any retired label whose hex differs from the current key
    for h in (d.get("axn_history") or []):
        m = re.match(r"AXN:([0-9A-Fa-f]+)\.", h.get("axn",""))
        if m:
            old = norm(m.group(1))
            if old != hx and old not in positions and old not in contested:
                aliases[old] = {"alias_of": hx, "status": "superseded-label",
                                "axn": axn, "deposit_number": d["deposit_number"],
                                "record": f"/s/records/{d['deposit_number']}/",
                                "retired": h.get("retired_at"), "reason": h.get("reason")}

sdir = ROOT/"data/symbolon-registry/entries"
n_sym = 0
if sdir.is_dir():
    for f in sorted(sdir.glob("*.json")):
        try: s = json.loads(f.read_text())
        except Exception: continue
        hx = s.get("position")
        if not hx: continue
        hx = norm(hx)
        tup = s.get("tuple", {})
        e = {"axn": s.get("axn"), "source": "symbolon-witness", "status": s.get("status"),
             "entry": f"/data/symbolon-registry/entries/{f.name}",
             "filename": (s.get("seed_a") or {}).get("manifest", [{}])[0].get("filename"),
             "retrieval": s.get("retrieval"),
             "family": (s.get("axn") or "..").split(".")[1] if s.get("axn") and "." in s.get("axn","") else None,
             "registered": s.get("registered"),
             "verified_at": s.get("verified_at"),
             "axn0_sha256": tup.get("axn0", {}).get("sha256"),
             "axn0_glyphs": tup.get("axn0", {}).get("glyphs"),
             "axn1_sha256": tup.get("axn1", {}).get("sha256"),
             "axn1_glyphs": tup.get("axn1", {}).get("glyphs"),
             "reconstruction_class": (s.get("seed_a") or {}).get("reconstruction_class")}
        claim(hx, e); n_sym += 1
        t = s.get("tuple", {})
        if t.get("axn0", {}).get("sha256"): kernels[t["axn0"]["sha256"]] = {"role": "axn0", **e}
        if t.get("axn1", {}).get("sha256"): kernels[t["axn1"]["sha256"]] = {"role": "axn1_stamped_form", **e}

# the /non mint route (axn/v2.3 non_entries, 2026-10-24): one position per composed /non row, family NON
n_non = 0
nl = ROOT/"datasets/negative-of-the-negative/v2/axn.json"
if nl.exists():
    for k, x in sorted(json.loads(nl.read_text(encoding="utf-8"))["entries"].items()):
        e = {"axn": x["axn"], "root": x["root"], "source": "non-entry", "entity": k, "family": "NON",
             "record": x["page"], "row": x["row"], "sha256": x["sha256"], "status": "composed, not frozen",
             "minted": x["minted"], "versions": 1 + len(x.get("history") or [])}
        claim(norm(x["hex"]), e); n_non += 1
        kernels[x["sha256"]] = {"role": "axn0", **e}
        for h in x.get("history") or []:
            kernels[h["sha256"]] = {"role": "earlier version", **e, "axn": h["axn"], "sha256": h["sha256"], "until": h["until"]}
# the capture mint route (2026-10-27, scripts/capture_axn.py): one position per address, one AXN per observation
# sealed with its analysis and measures, family CAPTURE
n_cap = 0
cl = ROOT/"data/captures/axn.json"
if cl.exists():
    for k, x in sorted(json.loads(cl.read_text(encoding="utf-8"))["addresses"].items()):
        e = {"axn": x["root"], "root": x["root"], "source": "capture", "family": "CAPTURE", "record": f"https://www.alexanarch.org/captures/{k}/",
             "q": x.get("q"), "allocated": x.get("allocated"), "observations": {s_: o["axn"] for s_, o in x["observations"].items()}}
        claim(norm(x["hex"]), e); n_cap += 1
        for s_, o in x["observations"].items():
            kernels[o["sha256"]] = {"role": "capture-observation", "axn": o["axn"], "root": x["root"], "source": "capture", "observation": s_,
                                    "sealed": o["file"], "date": o.get("date"), "surface": o.get("surface")}
            for h in o.get("history") or []:
                kernels[h["sha256"]] = {"role": "earlier version", "axn": h["axn"], "root": x["root"], "source": "capture", "observation": s_, "until": h["until"]}
# the release mint route (2026-10-27, scripts/release_axn.py): one position per continuing object (dataset, instrument,
# site), one AXN per frozen release
n_rel = 0
rl = ROOT/"data/releases/axn.json"
if rl.exists():
    for k, x in sorted(json.loads(rl.read_text(encoding="utf-8"))["objects"].items()):
        e = {"axn": x["root"], "root": x["root"], "source": "release", "kind": x["kind"], "family": x["family"], "object": k,
             "name": x.get("name"), "record": f"https://www.alexanarch.org/s/axn/{x['hex']}/", "allocated": x.get("allocated"),
             "releases": [r["axn"] for r in x.get("releases") or []]}
        claim(norm(x["hex"]), e); n_rel += 1
        for r in x.get("releases") or []:
            kernels[r["sha256"]] = {"role": "release", "axn": r["axn"], "root": x["root"], "source": "release", "object": k,
                                    "label": r["label"], "basis": r["basis"], **({"manifest": r["manifest"]} if r.get("manifest") else {})}
# aliases never shadow live or contested keys
for k in list(aliases):
    if k in positions or k in contested: del aliases[k]
merged = {**positions, **aliases, **contested}

if contested:
    print("WARNING — CONTESTED POSITIONS (visible in output, ruling required):", file=sys.stderr)
    for k, v in sorted(contested.items()):
        who = ", ".join(f"#{c.get('deposit_number','?')}" for c in v["claimants"])
        print(f"  {k}: {who}", file=sys.stderr)

out = {"description": "Central AXN registry: every allocated position across all mint routes, position- and kernel-keyed.",
       "generated": datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
       "positions_count": len(positions), "symbolon_entries": n_sym, "non_entries": n_non, "capture_positions": n_cap, "release_positions": n_rel,
       "contested_count": len(contested), "alias_count": len(aliases),
       "positions": dict(sorted(merged.items())), "kernels": kernels}
(ROOT/"data/axn-central-registry.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))
print(f"central registry: {len(positions)} positions ({n_sym} symbolon, {n_non} /non, {n_cap} capture, {n_rel} release) · {len(aliases)} aliases · {len(contested)} CONTESTED · {len(kernels)} kernels")
