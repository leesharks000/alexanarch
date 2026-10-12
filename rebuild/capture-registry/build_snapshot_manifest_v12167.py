#!/usr/bin/env python3
"""Build the manifest for the EA-WG-CAPTURES-01 v12.167 snapshot deposit (2026-10-12), on the v10.9 pattern (#1461):
core data listed with SHA-256, the bundle described, the capture frames manifested at their canonical paths under
data/captures/{slug}/ rather than duplicated. Usage: build_snapshot_manifest_v12167.py <bundle.tar.gz> <out manifest.json>"""
import hashlib, json, mimetypes, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[2]
bundle = pathlib.Path(sys.argv[1]); out = pathlib.Path(sys.argv[2])
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
reg = json.loads((ROOT / "data/EA-WG-CAPTURES-01.json").read_text(encoding="utf-8"))
held = sum(len(e["observations"]) if e.get("observations") else 1 for e in reg["entries"])
core = [("data/EA-WG-CAPTURES-01.json", "canonical store — the single writable authority since 2026-08-17"),
        ("rebuild/capture-registry/EA-WG-CAPTURES-01-REBUILD.json", "rebuild-era source, sealed (last written 2026-08-18)"),
        ("rebuild/capture-registry/PIPELINE.md", "pipeline — intake and repair procedure"),
        ("rebuild/capture-registry/INTAKE-CONTRACT.md", "intake contract"),
        ("data/capture-deposit-links.json", "capture→deposit join"),
        ("data/semantic-addresses.json", "semantic addresses folded from every capture query"),
        ("captures/index.html", f"rendered gallery — {len(reg['entries'])} anchored cards"),
        ("datasets/capture-registry/EA-WG-CAPTURES-01.json", "published dataset mirror")]
fm = []
for path, role in core:
    p = ROOT / path
    fm.append({"filename": p.name, "path": "/" + path, "bytes": p.stat().st_size, "sha256": sha(p),
               "media_type": mimetypes.guess_type(p.name)[0] or "application/octet-stream", "role": role})
for p in sorted((ROOT / "data/captures").glob("*/*")):
    if p.is_file():
        fm.append({"filename": p.name, "path": "/" + str(p.relative_to(ROOT)), "bytes": p.stat().st_size, "sha256": sha(p),
                   "media_type": mimetypes.guess_type(p.name)[0] or "application/octet-stream",
                   "role": f"capture evidence — frame for {p.parent.name}"})
m = {"registry": "EA-WG-CAPTURES-01", "version": reg["version"], "date": reg["date"], "addresses": len(reg["entries"]),
     "captures_held": held, "captures_declared": reg.get("observation_count"),
     "files": len(fm) + 1, "total_bytes": sum(f["bytes"] for f in fm) + bundle.stat().st_size, "files_manifest": fm,
     "bundle": {"filename": bundle.name, "bytes": bundle.stat().st_size, "sha256": sha(bundle),
                "contains": ["data/EA-WG-CAPTURES-01.json", "rebuild/capture-registry/ (without __pycache__)", "data/capture-deposit-links.json",
                             "data/semantic-addresses.json", "datasets/capture-registry/", "captures/index.html"]}}
out.write_text(json.dumps(m, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
frames = [f for f in fm if f["role"].startswith("capture evidence")]
print(m["version"], m["addresses"], held, len(fm), "files;", len(frames), "frames", round(sum(f["bytes"] for f in frames)/1e6, 1), "MB; total", round(m["total_bytes"]/1e6, 1), "MB; bundle", m["bundle"]["sha256"])
