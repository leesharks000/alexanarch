"""Build the files of the v12.559 snapshot deposit (EA-WG-CAPTURES-01 at its 1001st address).
    python3 build_snapshot.py <HEX>   -> files/AXN-<HEX>/ : the core bundle, the attached data files, manifest.json
The bundle is deterministic (sorted members, fixed mtime, uid/gid 0), so it rebuilds byte-identically from the same tree."""
import sys, json, gzip, tarfile, hashlib, pathlib, io, mimetypes
H = pathlib.Path(__file__).resolve().parent; ROOT = H.parents[2]
HEX = sys.argv[1]; VER = "12.559"; OUT = ROOT / "files" / f"AXN-{HEX}"; OUT.mkdir(parents=True, exist_ok=True)
R = json.loads((ROOT / "data/EA-WG-CAPTURES-01.json").read_text(encoding="utf-8"))
assert R["version"] == VER and len(R["entries"]) == 1001, (R["version"], len(R["entries"]))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
MEMBERS = ["data/EA-WG-CAPTURES-01.json", "rebuild/capture-registry", "data/capture-deposit-links.json", "data/semantic-addresses.json",
           "data/captures/axn.json", "data/captures/sealed", "datasets/capture-registry", "captures/index.html"]
def walk(rel):
    p = ROOT / rel
    if p.is_file(): return [p]
    return sorted(q for q in p.rglob("*") if q.is_file() and "__pycache__" not in q.parts and "snapshot-v12.559" not in q.parts)
files = [q for m in MEMBERS for q in walk(m)]
bname = f"EA-WG-CAPTURES-01-v{VER}.tar.gz"; bpath = OUT / bname
with open(bpath, "wb") as fh:
    with gzip.GzipFile(filename="", mode="wb", fileobj=fh, mtime=0, compresslevel=9) as gz:
        with tarfile.open(fileobj=gz, mode="w", format=tarfile.PAX_FORMAT) as tf:
            for q in files:
                ti = tf.gettarinfo(str(q), arcname=str(q.relative_to(ROOT)))
                ti.mtime = 0; ti.uid = ti.gid = 0; ti.uname = ti.gname = ""; ti.mode = 0o644
                with open(q, "rb") as f: tf.addfile(ti, f)
ATT = [("data/EA-WG-CAPTURES-01.json", "EA-WG-CAPTURES-01-v12.559.json", "canonical store, frozen at v12.559 — the single writable authority since 2026-08-17"),
       ("rebuild/capture-registry/EA-WG-CAPTURES-01.schema.json", "EA-WG-CAPTURES-01.schema.json", "entry schema (additionalProperties false), applied at every seat"),
       ("data/semantic-addresses.json", "semantic-addresses-v12.559.json", "semantic addresses folded from every capture query"),
       ("data/capture-deposit-links.json", "capture-deposit-links-v12.559.json", "capture→deposit join"),
       ("data/captures/axn.json", "captures-axn-v12.559.json", "capture AXN index: one position per address, one AXN per observation")]
man = []
def row(path_rel, src, role):
    man.append({"filename": pathlib.Path(path_rel).name, "path": "/" + path_rel, "bytes": src.stat().st_size, "sha256": sha(src),
                "media_type": mimetypes.guess_type(src.name)[0] or "application/octet-stream", "role": role})
for src_rel, name, role in ATT:
    dst = OUT / name; dst.write_bytes((ROOT / src_rel).read_bytes()); row(f"files/AXN-{HEX}/{name}", dst, "attached data file — " + role)
row(f"files/AXN-{HEX}/{bname}", bpath, "core data bundle — canonical store, pipeline documents and intake directories, PER-dim atom sets, sealed rebuild store, sealed observations, capture AXN index, capture-deposit join, semantic addresses, published dataset mirror, rendered gallery")
frames = set()
for e in R["entries"]:
    for o in [e] + (e.get("observations") or []):
        for p in o.get("imgs") or []: frames.add(p)
held = sorted(p for p in frames if (ROOT / p).is_file()); missing = sorted(p for p in frames if not (ROOT / p).is_file())
for p in held: row(p, ROOT / p, "capture evidence — frame, held at its canonical path")
tot = sum(m["bytes"] for m in man)
M = {"registry": "EA-WG-CAPTURES-01", "version": VER, "date": R["date"], "addresses": len(R["entries"]), "captures_held": R["observation_count"],
     "files": len(man) + 1, "total_bytes": tot, "frames_held": len(held), "frames_referenced_not_held": missing,
     "bundle": {"filename": bname, "bytes": bpath.stat().st_size, "sha256": sha(bpath), "members": len(files),
                "contains": [m + ("/ (without __pycache__ and the snapshot's own working folder)" if (ROOT / m).is_dir() else "") for m in MEMBERS]},
     "files_manifest": man}
(OUT / "manifest.json").write_text(json.dumps(M, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps({k: v for k, v in M.items() if k != "files_manifest"}, ensure_ascii=False, indent=1))
print("frames MB", round(sum(m["bytes"] for m in man if m["role"].startswith("capture evidence")) / 1e6, 1), "total MB", round(tot / 1e6, 1))
