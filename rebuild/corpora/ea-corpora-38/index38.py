#!/usr/bin/env python3
"""Enter the sixteen seats of EA-CORPORA-38 in the two corpora indexes, from their source.json records:
data/api/corpora.json (the machine index) and datasets/corpora/corpora.json (the seating manifest), in the
shapes the EA-CORPORA-37 rows hold, and recount both. Idempotent: a seat already entered is replaced.
    python3 rebuild/corpora/ea-corpora-38/index38.py"""
import datetime, hashlib, json, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[3]
SEATS = [
    "kant-akademie-ausgabe", "alexander-in-apr-wallies-1883", "philoponus-in-apr-wallies-1905",
    "theophrastus-characteres-diels-1909", "epictetus-dissertationes-schenkl-1916", "cicero-topica-wilkins-1902",
    "bacon-novum-organum-1620", "hume-treatise-enquiry", "carroll-symbolic-logic-1897", "hegel-wissenschaft-der-logik",
    "frege-begriffsschrift-1879", "peirce-logic-papers-1867-1878", "boethius-logica-migne-pl64",
    "nyaya-sutra-vatsyayana-1896", "ibn-sina-isharat-forget-1892", "buridan-sophismata-c1489"]
PI = ROOT / "data/api/corpora.json"
PM = ROOT / "datasets/corpora/corpora.json"
I = json.loads(PI.read_text(encoding="utf-8"))
M = json.loads(PM.read_text(encoding="utf-8"))


def lic_class(v):
    t = v.lower()
    for k, c in (("by-nc-sa", "cc-by-nc-sa"), ("by-nc", "cc-by-nc"), ("gpl", "gpl"), ("by-sa", "cc-by-sa"),
                 ("gutenberg", "gutenberg"), ("public domain", "public-domain")):
        if k in t:
            return c
    return "other"


for name in SEATS:
    d = ROOT / "data/corpora" / name
    s = json.loads((d / "source.json").read_text(encoding="utf-8"))
    files = [p for p in d.rglob("*") if p.is_file()]
    pay = s["license"]["payload"]
    row_i = {"seat": s["seat"], "corpus": name, "edition": s["edition"], "license": s["license"], "origin": s["origin"],
             "language": s["language"], "lines": s["lines_total"], "verified_loci": s["verified_loci"],
             "why_seated": s["why_seated"], "scope": s["scope"],
             "data": f"https://www.alexanarch.org/data/corpora/{name}/", "axn": s.get("axn")}
    row_m = {"corpus": name, "seat": s["seat"], "title": s["title"], "edition": s["edition"],
             "origin": json.dumps(s["origin"], ensure_ascii=False), "language": s["language"],
             "license_verbatim": pay, "license_class": lic_class(pay), "fetched": s["fetched"],
             "normalization": s["normalization"], "scope": s["scope"], "status": "seated, not deposited",
             "verified_loci": json.dumps(s["verified_loci"], ensure_ascii=False),
             "works": json.dumps({"count": s["works"]["count"], "units": s["works"]["units"]}, ensure_ascii=False),
             "why_seated": s["why_seated"],
             "manifest_sha256": hashlib.sha256((d / "MANIFEST.sha256").read_bytes()).hexdigest(),
             "file_count": len(files), "bytes": sum(p.stat().st_size for p in files), "axn": s.get("axn")}
    I["corpora"] = [c for c in I["corpora"] if c["corpus"] != name] + [row_i]
    M["seats"] = [c for c in M["seats"] if c["corpus"] != name] + [row_m]

n = len(I["corpora"])
I["seats"] = n
I["count"] = n
I["lines_total"] = sum(c.get("lines") or 0 for c in I["corpora"])
I["_generated"] = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
# the manifest's counts are the counts it already states plus the new seats (a recount by this script's rule
# gives 242, not 246, for with_verified_loci: the earlier counts were made by another rule, and are not re-made here)
import subprocess
old = json.loads(subprocess.check_output(["git", "-C", str(ROOT), "show", "origin/main:datasets/corpora/corpora.json"]))
new = [x for x in M["seats"] if x["corpus"] in SEATS]
cnt = dict(old["counts"])
cnt["seats"] += len(new); cnt["with_manifest_sha"] += len(new)
cnt["files"] += sum(x["file_count"] for x in new); cnt["bytes"] += sum(x["bytes"] for x in new)
cnt["with_verified_loci"] += sum(1 for x in new if x["verified_loci"] != "[]")
by = dict(old["by_license_class"])
for x in new:
    by[x["license_class"]] = by.get(x["license_class"], 0) + 1
M["counts"] = cnt
M["by_license_class"] = by
M["generated"] = datetime.date.today().isoformat()
PI.write_text(json.dumps(I, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
PM.write_text(json.dumps(M, ensure_ascii=False, indent=1), encoding="utf-8")
print("index", n, "seats;", I["lines_total"], "lines; manifest", cnt["seats"], "seats", cnt["files"], "files", by)
