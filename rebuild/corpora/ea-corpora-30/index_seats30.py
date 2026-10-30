#!/usr/bin/env python3
"""Enter the EA-CORPORA-30 seats (30/01–30/11, the exact sciences and Klee's Bauhaus notebook; 30/12 the exact sciences, wanted, declared) in data/api/corpora.json and datasets/corpora/corpora.json.

Additive and idempotent: an existing row for any of the twelve corpora is replaced, totals are recomputed from the
difference. license_class follows the manifest's stated derivation, most-restrictive-first over the packaging the
seat actually carries: Wikisource transcription (CC BY-SA) > Project Gutenberg > public domain (scans only)."""
import json, hashlib, pathlib, datetime

ROOT = pathlib.Path(__file__).resolve().parents[3]
SPEC = {"seats": [{"corpus": c} for c in ("einstein", "goedel", "tesla", "copernicus", "galileo", "kepler", "newton", "arabic-mathematics", "paul-klee", "quantum-founders", "archimedes-ptolemy", "exact-wanted")]}
NAMES = [s["corpus"] for s in SPEC["seats"]]
now = datetime.datetime.now(datetime.timezone.utc)


def lclass(src):
    kinds = {i["source"] for i in src["origin"]["items"]}
    if any(k.startswith("GRETIL") for k in kinds):
        return "cc-by-nc-sa"  # GRETIL TEI: CC BY-NC-SA 4.0 at the file; the NC payload/record split of EA-CORPORA-02
    if kinds and kinds <= {"this library", "Blogger (mindcontrolpoems.blogspot.com)", "Google Drive (the author's)"}:
        return "cc-by"  # the author's own works, as at the Pearl seat
    if any(k.startswith("Wikisource") or k.startswith("PerseusDL") or k.startswith("Open Greek and Latin") for k in kinds):  # First1KGreek: CC BY-SA 4.0 at the repository  # Perseus TEI: CC BY-SA 4.0, as the Perseus seats before it
        return "cc-by-sa"
    if any(k.startswith("Wikisource") for k in kinds):
        return "cc-by-sa"
    if any(k.startswith("Project Gutenberg") for k in kinds):
        return "gutenberg"
    if "OpenITI" in kinds:
        return "cc-by-nc-sa"  # OpenITI: CC BY-NC-SA 4.0, stated by the project (see the seat's origin.release)
    if "Ganjoor" in kinds:
        return "site-terms"   # Ganjoor's own release statement (see the seat's licence); not a formal licence
    if "Alexanarch deposit" in kinds:
        return "cc-by"  # the archive's own declaration (27/07)
    return "public-domain"


I = ROOT / "data/api/corpora.json"; d = json.loads(I.read_text(encoding="utf-8"))
M = ROOT / "datasets/corpora/corpora.json"; m = json.loads(M.read_text(encoding="utf-8"))
old = {c["corpus"]: c for c in d["corpora"] if c["corpus"] in NAMES}
oldm = {x["corpus"]: x for x in m["seats"] if x["corpus"] in NAMES}
d["corpora"] = [c for c in d["corpora"] if c["corpus"] not in NAMES]
m["seats"] = [x for x in m["seats"] if x["corpus"] not in NAMES]
for c in old.values():
    d["seats"] -= 1; d["count"] -= 1; d["lines_total"] -= c.get("lines") or 0
for x in oldm.values():
    k = m["counts"]; k["seats"] -= 1; k["files"] -= x["file_count"]; k["bytes"] -= x["bytes"]
    k["with_manifest_sha"] -= 1; k["with_verified_loci"] -= 1 if x.get("verified_loci") not in ("", "[]") else 0
    m["by_license_class"][x["license_class"]] -= 1
for name in NAMES:
    seat = ROOT / "data/corpora" / name
    s = json.loads((seat / "source.json").read_text(encoding="utf-8"))
    man = (seat / "MANIFEST.sha256").read_text(encoding="utf-8").splitlines()
    files = [p for p in seat.rglob("*") if p.is_file()]
    size = sum(p.stat().st_size for p in files)
    d["corpora"].append({
        "seat": s["seat"], "corpus": name, "edition": s["edition"], "license": s["license"],
        "origin": s["origin"], "language": s["language"], "lines": s["lines_total"],
        "verified_loci": s["verified_loci"], "why_seated": s["why_seated"], "scope": s["scope"],
        "data": f"https://www.alexanarch.org/data/corpora/{name}/"})
    d["seats"] += 1; d["count"] += 1; d["lines_total"] += s["lines_total"]
    lc = lclass(s)
    m["seats"].append({
        "corpus": name, "seat": s["seat"], "title": s["title"], "edition": s["edition"],
        "origin": json.dumps(s["origin"], ensure_ascii=False), "language": s["language"],
        "license_verbatim": s["license"]["payload"], "license_class": lc, "fetched": s["fetched"],
        "normalization": s["normalization"], "scope": s["scope"], "status": "seated",
        "verified_loci": json.dumps(s["verified_loci"], ensure_ascii=False),
        "works": json.dumps({"count": s["works"]["count"], "units": s["works"]["units"]}, ensure_ascii=False),
        "why_seated": s["why_seated"],
        "manifest_sha256": hashlib.sha256((seat / "MANIFEST.sha256").read_bytes()).hexdigest(),
        "file_count": len(files), "bytes": size})
    k = m["counts"]; k["seats"] += 1; k["files"] += len(files); k["bytes"] += size; k["with_manifest_sha"] += 1
    k["with_verified_loci"] += 1 if s["verified_loci"] else 0
    m["by_license_class"][lc] = m["by_license_class"].get(lc, 0) + 1
    print(f"  {s['seat']} {name:26} {lc:13} {len(files):4} files {size/1048576:7.1f} MB {s['lines_total']:7} lines")
d["_generated"] = now.isoformat().replace("+00:00", "Z")
m["generated"] = now.date().isoformat()
I.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
M.write_text(json.dumps(m, ensure_ascii=False, indent=1), encoding="utf-8")
print("index:", d["seats"], "seats,", d["lines_total"], "lines · manifest:", m["counts"])
