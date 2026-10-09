#!/usr/bin/env python3
"""Enter seat EA-CORPORA-17/01 (openai-math) in data/api/corpora.json and datasets/corpora/corpora.json.
Additive; the totals move by one seat. bytes and file_count count the seat as it stands once the payload is carried in
(MANIFEST.sha256 entries, sizes from the commit), with MANIFEST.sha256 itself."""
import json, hashlib, pathlib, datetime, sys
ROOT = pathlib.Path(__file__).resolve().parents[3]
SEAT = ROOT / "data/corpora/openai-math"
SRC_CLONE = pathlib.Path(sys.argv[1])  # openai/math checkout at fd4aeeb2, for payload sizes
s = json.loads((SEAT / "source.json").read_text(encoding="utf-8"))
man = (SEAT / "MANIFEST.sha256").read_text(encoding="utf-8").splitlines()
size = 0
for l in man:
    rel = l.split("  ", 1)[1][2:]
    f = SEAT / rel
    size += f.stat().st_size if f.exists() else (SRC_CLONE / rel[len("original/"):]).stat().st_size
size += (SEAT / "MANIFEST.sha256").stat().st_size
now = datetime.datetime.now(datetime.timezone.utc)
I = ROOT / "data/api/corpora.json"; d = json.loads(I.read_text(encoding="utf-8"))
assert not any(c["corpus"] == "openai-math" for c in d["corpora"])
d["corpora"].append({
 "seat": s["seat"], "corpus": s["corpus"], "edition": s["edition"], "license": s["license"]["payload"],
 "origin": s["origin"], "language": s["language"], "lines": s["lines_total"], "verified_loci": s["verified_loci"],
 "why_seated": s["why_seated"], "scope": s["scope"], "data": "https://www.alexanarch.org/data/corpora/openai-math/",
 "ruling": s["rulings"][0] + " Provenance, as the publisher records it, is carried in source.json: " + s["provenance"]["ruling"]})
d["seats"] += 1; d["count"] += 1; d["lines_total"] += s["lines_total"]; d["_generated"] = now.isoformat().replace("+00:00", "Z")
I.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
M = ROOT / "datasets/corpora/corpora.json"; m = json.loads(M.read_text(encoding="utf-8"))
assert not any(x["corpus"] == "openai-math" for x in m["seats"])
m["seats"].append({
 "corpus": s["corpus"], "seat": s["seat"], "title": s["title"], "edition": s["edition"],
 "origin": json.dumps(s["origin"], ensure_ascii=False), "language": s["language"],
 "license_verbatim": s["license"]["payload"], "license_class": "other", "fetched": s["origin"]["fetched"],
 "normalization": s["normalization"], "scope": s["scope"], "status": "seated",
 "verified_loci": json.dumps(s["verified_loci"], ensure_ascii=False), "works": "", "why_seated": s["why_seated"],
 "manifest_sha256": hashlib.sha256((SEAT / "MANIFEST.sha256").read_bytes()).hexdigest(),
 "file_count": len(man) + 1, "bytes": size})
c = m["counts"]; c["seats"] += 1; c["files"] += len(man) + 1; c["bytes"] += size; c["with_manifest_sha"] += 1; c["with_verified_loci"] += 1
m["by_license_class"]["other"] += 1; m["generated"] = now.date().isoformat()
M.write_text(json.dumps(m, ensure_ascii=False, indent=1), encoding="utf-8")
print("indexed:", len(man) + 1, "files,", size, "bytes,", s["lines_total"], "lines")
